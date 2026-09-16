"""The one pytest module for Design Agent Showcase.

Every section (core features, data integrity, authorization, edge cases) and both
declared slots (db, storage) are merged here. Fixtures, pinned literals and
helpers live in conftest.py; the shared grader (appclient, capabilities,
_shapes) is on PYTHONPATH=/tests from the deku-verifier-base image.

The checklist obligations each function discharges live in the
pytest-provenance-v1 sidecar beside the bundle, not in a comment.

Channel disjointness: the browser pass walks the public marketing routes and the
studio through their own journeys, so every check here either reads a seeded
record no journey mutates, or works inside a per-run probe record it created
itself.
"""

from __future__ import annotations

import os

import appclient
import conftest as cf


def test_health_endpoint_answers_two_hundred() -> None:
    """The app answers its health route once the app is ready."""
    with appclient.client(None) as client:
        response = client.get("/health")
    assert response.status_code == 200, cf.describe(
        response, "the health route must answer 200 once the app is ready")


def test_credentials_file_is_written_at_the_app_root() -> None:
    """The seeded logins are readable at the documented path."""
    assert os.path.isfile(cf.CREDENTIALS_FILE), (
        f"{cf.CREDENTIALS_FILE} must exist so a seeded account can be found")
    text = open(cf.CREDENTIALS_FILE, encoding="utf-8", errors="replace").read()
    assert cf.AUTHOR_EMAIL in text, (
        f"{cf.CREDENTIALS_FILE} must name the seeded author {cf.AUTHOR_EMAIL}")
    assert cf.SEEDED_PASSWORD in text, (
        f"{cf.CREDENTIALS_FILE} must carry the seeded password literal")


def test_reserved_screenshot_and_download_directories_exist_and_are_empty() -> None:
    """The two reserved directories exist at the app root and hold nothing."""
    for path in (cf.SCREENSHOT_DIR, cf.DOWNLOAD_DIR):
        assert os.path.isdir(path), f"{path} must exist at the app root"
        assert os.listdir(path) == [], f"{path} must be empty"


def test_api_is_served_under_the_api_prefix_on_the_same_origin() -> None:
    """Every record the browser reads is served under the api prefix."""
    with appclient.client(None) as client:
        response = client.get(cf.stories_path())
    assert response.status_code == 200, cf.describe(
        response, "the story list must be reachable under the api prefix")
    assert appclient.api_base().endswith("/api"), (
        "the HTTP API must be served on the app origin under the api prefix")


def test_story_list_endpoint_returns_a_top_level_json_array() -> None:
    """The published story list is a top-level JSON array."""
    with appclient.client(None) as client:
        response = client.get(cf.stories_path())
    payload = response.json()
    assert isinstance(payload, list), (
        f"the story list must be a top-level JSON array, got {type(payload).__name__}")


def test_hero_metric_line_is_served_by_the_app() -> None:
    """The home hero metric line comes from the app rather than the bundle."""
    with appclient.client(None) as client:
        response = client.get("/metrics/hero")
    assert response.status_code == 200, cf.describe(
        response, "the hero metric line must be served by the app")
    assert cf.HERO_METRIC_LINE in response.text, (
        f"the hero metric line must read {cf.HERO_METRIC_LINE!r}, got "
        f"{response.text[:200]}")


def test_login_returns_a_bearer_token_for_every_seeded_account() -> None:
    """Each seeded account signs in with the pinned password."""
    for email in (cf.AUTHOR_EMAIL, cf.AUTHOR2_EMAIL, cf.READER_EMAIL):
        token = appclient.login(email, cf.SEEDED_PASSWORD)
        assert isinstance(token, str) and token, (
            f"login for {email} must return a non-empty access_token")


def test_login_with_the_wrong_password_is_denied() -> None:
    """A login carrying the wrong password hands back no token."""
    with appclient.client(None) as client:
        response = client.post("/auth/login", json={
            "email": cf.AUTHOR_EMAIL, "password": "not-the-seeded-password-2026"})
    assert response.status_code >= 400, cf.describe(
        response, "a login with the wrong password must be denied")
    assert "access_token" not in response.text, (
        "a denied login must hand back no access_token")


def test_signup_creates_an_account_whose_role_is_reader(fresh_reader_token) -> None:
    """Signup creates a reader account, never an author account."""
    with appclient.client(fresh_reader_token) as client:
        response = client.get(cf.leads_path())
    assert response.status_code >= 400, cf.describe(
        response, "a freshly signed-up account must hold the reader role only")


def test_signup_with_an_existing_email_is_rejected_and_creates_no_second_account() -> None:
    """A signup reusing a seeded email is refused and writes nothing."""
    before = cf.backend().count("accounts", email=cf.READER_EMAIL)
    with appclient.client(None) as client:
        response = client.post("/auth/signup", json={
            "email": cf.READER_EMAIL, "password": cf.SEEDED_PASSWORD,
            "display_name": "Duplicate Reader"})
    assert response.status_code >= 400, cf.describe(
        response, f"a signup reusing {cf.READER_EMAIL} must be rejected as invalid")
    after = cf.backend().count("accounts", email=cf.READER_EMAIL)
    assert after == before == 1, (
        f"a rejected signup must create no second account, count moved "
        f"{before} to {after}")


def test_expired_token_is_refused_and_leaves_the_story_unchanged(author_token) -> None:
    """A call carrying a token the app never issued changes no record."""
    before = cf.story_row(cf.DRAFT_SLUG)
    with appclient.client("expired." + "a" * 40) as client:
        response = client.patch(
            f"{cf.studio_stories_path()}/{cf.story_id(cf.DRAFT_SLUG)}",
            json={"title": "Rewritten by an expired session"})
    assert response.status_code >= 400, cf.describe(
        response, "a call carrying an expired token must be refused")
    after = cf.story_row(cf.DRAFT_SLUG)
    assert after["title"] == before["title"], (
        "a refused call must leave the story row unchanged")


def test_reader_request_to_an_author_endpoint_is_denied_at_the_api(reader_token) -> None:
    """A reader session is denied at every author-only endpoint."""
    with appclient.client(reader_token) as client:
        listing = client.get(cf.studio_stories_path())
        creation = client.post(cf.studio_stories_path(), json={
            "title": "A reader should not write this",
            "slug": cf.probe_slug("reader-write"),
            "category": cf.CATEGORY_DESIGN,
            "intro": "no", "body": "no", "access": cf.ACCESS_OPEN})
    assert listing.status_code >= 400, cf.describe(
        listing, "a reader must be denied the author story list")
    assert creation.status_code >= 400, cf.describe(
        creation, "a reader must be denied the story create endpoint")


def test_signed_out_request_for_the_leads_desk_is_denied() -> None:
    """The leads desk refuses a caller carrying no session."""
    with appclient.client(None) as client:
        response = client.get(cf.leads_path())
    assert response.status_code >= 400, cf.describe(
        response, "a signed-out request for the leads desk must be denied")


def test_reader_request_for_the_leads_desk_is_denied(reader_token) -> None:
    """The leads desk refuses a reader session."""
    with appclient.client(reader_token) as client:
        response = client.get(cf.leads_path())
    assert response.status_code >= 400, cf.describe(
        response, "a reader must be denied the leads desk")


def test_draft_story_is_absent_from_the_public_story_index() -> None:
    """The public story index omits every draft story."""
    with appclient.client(None) as client:
        response = client.get(cf.stories_path())
    slugs = {row.get("slug") for row in cf.rows_of(response.json())}
    assert cf.DRAFT_SLUG not in slugs, (
        f"the draft story {cf.DRAFT_SLUG} must not appear on the public index, "
        f"saw {sorted(s for s in slugs if s)}")
    assert cf.OPEN_SLUG in slugs, (
        f"the published story {cf.OPEN_SLUG} must appear on the public index")


def test_draft_story_requested_by_slug_while_signed_out_is_refused() -> None:
    """A direct request for a draft story by its own slug is refused."""
    with appclient.client(None) as client:
        response = client.get(f"{cf.stories_path()}/{cf.DRAFT_SLUG}")
    assert response.status_code >= 400, cf.describe(
        response, f"the draft story {cf.DRAFT_SLUG} must not be readable while signed out")
    assert cf.DRAFT_TITLE not in response.text, (
        "a refused draft request must leak no part of the story")


def test_draft_story_requested_by_identifier_by_another_author_is_denied(author2_token) -> None:
    """A second author asking for a draft by its identifier is denied."""
    identifier = cf.story_id(cf.DRAFT_SLUG)
    with appclient.client(author2_token) as client:
        response = client.get(f"{cf.studio_stories_path()}/{identifier}")
    assert response.status_code >= 400, cf.describe(
        response, "another author must be denied a draft story by its identifier")


def test_draft_story_is_absent_from_another_authors_story_list(author2_token) -> None:
    """A second author's own story list carries no draft it does not own."""
    with appclient.client(author2_token) as client:
        response = client.get(cf.studio_stories_path())
    slugs = {row.get("slug") for row in cf.rows_of(response.json())}
    assert cf.DRAFT_SLUG not in slugs, (
        f"{cf.AUTHOR2_EMAIL} owns no draft {cf.DRAFT_SLUG} and must not see it")


def test_draft_story_cover_is_refused_to_every_caller_but_the_owner(author2_token) -> None:
    """The cover image of a draft story is refused at the streaming route."""
    identifier = cf.story_id(cf.DRAFT_SLUG)
    with appclient.client(None) as anonymous:
        signed_out = anonymous.get(f"{cf.stories_path()}/{identifier}/cover")
    with appclient.client(author2_token) as other:
        other_author = other.get(f"{cf.stories_path()}/{identifier}/cover")
    assert signed_out.status_code >= 400, cf.describe(
        signed_out, "a draft story cover must be refused to a signed-out caller")
    assert other_author.status_code >= 400, cf.describe(
        other_author, "a draft story cover must be refused to another author")


def test_members_story_body_is_withheld_from_a_signed_out_visitor() -> None:
    """A members story shows its opening to a visitor and withholds its body."""
    with appclient.client(None) as client:
        response = client.get(f"{cf.stories_path()}/{cf.MEMBERS_SLUG}")
    assert response.status_code == 200, cf.describe(
        response, f"the members story {cf.MEMBERS_SLUG} must be reachable while signed out")
    payload = response.json()
    assert payload.get("intro"), "a members story must show its intro to a visitor"
    assert not payload.get("body"), (
        "the body of a members story must be withheld from a signed-out visitor")


def test_members_story_body_is_served_to_a_signed_in_reader(reader_token) -> None:
    """A signed-in reader receives the full body of a members story."""
    with appclient.client(reader_token) as client:
        response = client.get(f"{cf.stories_path()}/{cf.MEMBERS_SLUG}")
    assert response.status_code == 200, cf.describe(
        response, "a reader must reach the members story")
    assert response.json().get("body"), (
        "a signed-in reader must receive the body of a members story")


def test_published_open_story_is_served_in_full_to_a_signed_out_visitor() -> None:
    """A published open story is readable in full with no session."""
    with appclient.client(None) as client:
        response = client.get(f"{cf.stories_path()}/{cf.OPEN_SLUG}")
    assert response.status_code == 200, cf.describe(
        response, f"the published open story {cf.OPEN_SLUG} must be readable by anybody")
    payload = response.json()
    assert payload.get("title") == cf.OPEN_TITLE, (
        f"the story title must read {cf.OPEN_TITLE!r}, got {payload.get('title')!r}")
    assert payload.get("body"), "a published open story must carry its body"


def test_story_index_lists_published_stories_newest_published_first() -> None:
    """The story index orders published stories by the moment of publication."""
    with appclient.client(None) as client:
        response = client.get(cf.stories_path())
    rows = cf.rows_of(response.json())
    stamps = [row.get("published_at") for row in rows]
    assert all(stamps), "every listed story must carry the moment it was published"
    assert stamps == sorted(stamps, reverse=True), (
        f"published stories must be listed newest first, got {stamps}")


def test_story_category_belongs_to_the_seven_named_categories() -> None:
    """Every listed story carries a category from the pinned vocabulary."""
    with appclient.client(None) as client:
        response = client.get(cf.stories_path())
    for row in cf.rows_of(response.json()):
        assert row.get("category") in cf.CATEGORIES, (
            f"story {row.get('slug')!r} carries category {row.get('category')!r}, "
            f"which is outside {list(cf.CATEGORIES)}")


def test_new_story_row_is_persisted_with_the_state_draft(author_token) -> None:
    """A newly created story is a stored row whose state is draft."""
    slug = cf.probe_slug("new-story")
    cf.create_probe_story(author_token, slug)
    row = cf.backend().one("stories", slug=slug)
    assert row is not None, f"the created story {slug} must be a stored row"
    assert row["state"] == cf.STATE_DRAFT, (
        f"a newly created story must hold state {cf.STATE_DRAFT}, got {row['state']!r}")


def test_publishing_a_story_sets_its_state_and_published_moment(author_token) -> None:
    """Publishing moves a story to published and records the moment."""
    slug = cf.probe_slug("publish")
    created = cf.create_probe_story(author_token, slug)
    identifier = created.get("id") or cf.story_id(slug)
    with appclient.client(author_token) as client:
        response = client.post(f"{cf.studio_stories_path()}/{identifier}/publish")
    assert response.status_code < 300, cf.describe(
        response, f"the owning author must be able to publish {slug}")
    row = cf.backend().one("stories", slug=slug)
    assert row["state"] == cf.STATE_PUBLISHED, (
        f"a published story must hold state {cf.STATE_PUBLISHED}, got {row['state']!r}")
    assert row["published_at"] is not None, (
        "publishing a story must record the moment of publication")


def test_unpublishing_returns_a_story_to_the_state_draft(author_token) -> None:
    """Unpublishing puts a story back behind the draft wall."""
    slug = cf.probe_slug("unpublish")
    created = cf.create_probe_story(author_token, slug)
    identifier = created.get("id") or cf.story_id(slug)
    with appclient.client(author_token) as client:
        client.post(f"{cf.studio_stories_path()}/{identifier}/publish")
        response = client.post(f"{cf.studio_stories_path()}/{identifier}/unpublish")
    assert response.status_code < 300, cf.describe(
        response, f"the owning author must be able to unpublish {slug}")
    row = cf.backend().one("stories", slug=slug)
    assert row["state"] == cf.STATE_DRAFT, (
        f"unpublishing must return the story to state {cf.STATE_DRAFT}")
    with appclient.client(None) as anonymous:
        public = anonymous.get(f"{cf.stories_path()}/{slug}")
    assert public.status_code >= 400, cf.describe(
        public, "an unpublished story must stop being publicly readable at once")


def test_second_story_claiming_a_held_slug_is_rejected(author_token) -> None:
    """A slug belongs to one story, so a second claim is refused."""
    slug = cf.probe_slug("held-slug")
    cf.create_probe_story(author_token, slug)
    with appclient.client(author_token) as client:
        response = client.post(cf.studio_stories_path(), json={
            "title": "A second story claiming a held slug",
            "slug": slug, "category": cf.CATEGORY_DESIGN,
            "intro": "no", "body": "no", "access": cf.ACCESS_OPEN})
    assert response.status_code >= 400, cf.describe(
        response, f"a second story claiming the slug {slug} must be rejected as invalid")
    assert cf.backend().count("stories", slug=slug) == 1, (
        f"the slug {slug} must belong to exactly one story row")


def test_concurrent_story_creates_on_one_slug_leave_exactly_one_row(author_token) -> None:
    """Two simultaneous creates of one slug leave exactly one story."""
    slug = cf.probe_slug("race")

    def create():
        with appclient.client(author_token) as client:
            return client.post(cf.studio_stories_path(), json={
                "title": "A racing story creation",
                "slug": slug, "category": cf.CATEGORY_DESIGN,
                "intro": "racing", "body": "racing", "access": cf.ACCESS_OPEN})

    first, second = cf.run_together(create, create)
    statuses = sorted([first.status_code, second.status_code])
    assert cf.backend().count("stories", slug=slug) == 1, (
        f"two concurrent creates on the slug {slug} must leave exactly one row, "
        f"statuses were {statuses}")
    assert statuses[0] < 300 <= statuses[1], (
        f"exactly one concurrent create must win, statuses were {statuses}")


def test_author_edit_of_another_authors_story_is_denied_and_the_row_is_unchanged(author2_token) -> None:
    """A second author cannot rewrite a story it does not own."""
    before = cf.story_row(cf.OPEN_SLUG)
    with appclient.client(author2_token) as client:
        response = client.patch(
            f"{cf.studio_stories_path()}/{before['id']}",
            json={"title": "Rewritten by somebody else"})
    assert response.status_code >= 400, cf.describe(
        response, "an author must be denied an edit of another author's story")
    after = cf.story_row(cf.OPEN_SLUG)
    assert after["title"] == before["title"] == cf.OPEN_TITLE, (
        "a denied edit must leave the underlying story row unchanged")


def test_uploaded_cover_bytes_live_in_the_object_store_at_the_key_scheme(author_token) -> None:
    """Cover bytes an author uploads are a real object in the bucket."""
    slug = cf.probe_slug("cover")
    created = cf.create_probe_story(author_token, slug)
    identifier = created.get("id") or cf.story_id(slug)
    with appclient.client(author_token) as client:
        response = client.post(
            f"{cf.studio_stories_path()}/{identifier}/cover",
            files={"file": ("cover.png", cf.PNG_BYTES, "image/png")},
            data={"alt_text": cf.COVER_ALT_TEXT})
    assert response.status_code < 300, cf.describe(
        response, f"the owning author must be able to attach a cover to {slug}")
    key = response.json().get("object_key")
    assert key, "a cover upload must answer with the object key of the stored bytes"
    assert cf.store().exists(key), (
        f"the cover bytes must live in the object store at {key}")


def test_cover_object_key_uses_the_story_identifier_and_the_byte_digest(author_token) -> None:
    """The cover object key follows the pinned scheme."""
    import hashlib
    slug = cf.probe_slug("key-scheme")
    created = cf.create_probe_story(author_token, slug)
    identifier = created.get("id") or cf.story_id(slug)
    with appclient.client(author_token) as client:
        response = client.post(
            f"{cf.studio_stories_path()}/{identifier}/cover",
            files={"file": ("cover.png", cf.PNG_BYTES, "image/png")},
            data={"alt_text": cf.COVER_ALT_TEXT})
    key = response.json().get("object_key")
    digest = hashlib.sha256(cf.PNG_BYTES).hexdigest()
    assert key == f"{cf.COVER_KEY_PREFIX}/{identifier}/{digest}.png", (
        f"the object key must follow the pinned scheme, got {key!r}")


def test_cover_upload_of_an_unaccepted_image_type_is_refused_and_stores_nothing(author_token) -> None:
    """A cover whose type is outside the three accepted types is refused."""
    slug = cf.probe_slug("bad-type")
    created = cf.create_probe_story(author_token, slug)
    identifier = created.get("id") or cf.story_id(slug)
    with appclient.client(author_token) as client:
        response = client.post(
            f"{cf.studio_stories_path()}/{identifier}/cover",
            files={"file": ("cover.gif", cf.GIF_BYTES, "image/gif")},
            data={"alt_text": cf.COVER_ALT_TEXT})
    assert response.status_code >= 400, cf.describe(
        response, "a cover upload of an unaccepted image type must be refused")
    assert cf.store().list(f"{cf.COVER_KEY_PREFIX}/{identifier}/") == [], (
        "a refused cover upload must leave nothing in the object store")


def test_cover_upload_without_alternative_text_is_refused(author_token) -> None:
    """A cover carrying no alternative text cannot be saved."""
    slug = cf.probe_slug("no-alt")
    created = cf.create_probe_story(author_token, slug)
    identifier = created.get("id") or cf.story_id(slug)
    with appclient.client(author_token) as client:
        response = client.post(
            f"{cf.studio_stories_path()}/{identifier}/cover",
            files={"file": ("cover.png", cf.PNG_BYTES, "image/png")})
    assert response.status_code >= 400, cf.describe(
        response, "a cover carrying no alternative text must be refused")


def test_second_cover_upload_leaves_exactly_one_cover_row_for_the_story(author_token) -> None:
    """Uploading a second cover replaces the first rather than adding one."""
    slug = cf.probe_slug("replace-cover")
    created = cf.create_probe_story(author_token, slug)
    identifier = created.get("id") or cf.story_id(slug)
    with appclient.client(author_token) as client:
        for payload in (cf.PNG_BYTES, cf.PNG_BYTES + b"\x00"):
            client.post(f"{cf.studio_stories_path()}/{identifier}/cover",
                        files={"file": ("cover.png", payload, "image/png")},
                        data={"alt_text": cf.COVER_ALT_TEXT})
    assert cf.backend().count("story_covers", story_id=identifier) == 1, (
        f"story {identifier} must hold exactly one cover row after two uploads")


def test_published_story_cover_is_streamed_from_the_app_own_route() -> None:
    """A published story's cover is served by the app itself."""
    identifier = cf.story_id(cf.OPEN_SLUG)
    with appclient.client(None) as client:
        response = client.get(f"{cf.stories_path()}/{identifier}/cover")
    assert response.status_code == 200, cf.describe(
        response, f"the cover of {cf.OPEN_SLUG} must be streamed to any visitor")
    assert response.headers.get("content-type", "").split(";")[0] in cf.ACCEPTED_IMAGE_TYPES, (
        f"a streamed cover must carry an accepted image type, got "
        f"{response.headers.get('content-type')!r}")
    assert response.content, "a streamed cover must carry the stored bytes"


def test_accepted_scan_submission_answers_with_a_scan_reference() -> None:
    """A well formed scan submission is accepted and answers with a reference."""
    payload = cf.submit_scan(cf.probe_email("scan-ref"))
    assert payload.get("reference"), (
        "an accepted scan submission must answer with a scan reference")
    assert payload.get("status") in (cf.SCAN_STATUS_QUEUED, cf.SCAN_STATUS_RUNNING,
                                     cf.SCAN_STATUS_COMPLETE), (
        f"a new scan must carry a known status, got {payload.get('status')!r}")


def test_scan_reference_reads_scan_followed_by_twelve_hexadecimal_characters() -> None:
    """A scan reference follows the pinned reference scheme."""
    reference = cf.submit_scan(cf.probe_email("scan-shape"))["reference"]
    assert cf.SCAN_REFERENCE_RE.match(reference), (
        f"a scan reference must read scan- followed by twelve lowercase "
        f"hexadecimal characters, got {reference!r}")


def test_scan_advances_to_complete_without_further_visitor_action() -> None:
    """A submitted scan runs itself through to completion."""
    reference = cf.submit_scan(cf.probe_email("scan-advance"))["reference"]
    payload = cf.wait_for_scan(reference)
    assert payload["status"] == cf.SCAN_STATUS_COMPLETE, (
        f"the scan {reference} must reach status {cf.SCAN_STATUS_COMPLETE}")


def test_complete_scan_carries_exactly_four_graded_sections() -> None:
    """A complete scan report carries the four named sections, never more."""
    reference = cf.submit_scan(cf.probe_email("scan-sections"))["reference"]
    payload = cf.wait_for_scan(reference)
    names = [section.get("name") for section in payload.get("sections") or []]
    assert sorted(names) == sorted(cf.SCAN_SECTIONS), (
        f"a complete scan must carry exactly {list(cf.SCAN_SECTIONS)}, got {names}")
    row = cf.backend().one("scans", reference=reference)
    assert cf.backend().count("scan_sections", scan_id=row["id"]) == 4, (
        f"the scan {reference} must hold exactly four stored section rows")


def test_complete_scan_carries_an_overall_grade_from_the_three_words() -> None:
    """The overall grade and every section grade come from one vocabulary."""
    reference = cf.submit_scan(cf.probe_email("scan-grade"))["reference"]
    payload = cf.wait_for_scan(reference)
    assert payload.get("overall") in cf.SCAN_GRADES, (
        f"the overall grade must be one of {list(cf.SCAN_GRADES)}, got "
        f"{payload.get('overall')!r}")
    for section in payload.get("sections") or []:
        assert section.get("grade") in cf.SCAN_GRADES, (
            f"section {section.get('name')!r} carries grade "
            f"{section.get('grade')!r}, outside {list(cf.SCAN_GRADES)}")
        assert section.get("finding"), (
            f"section {section.get('name')!r} must carry a written finding")


def test_two_scans_of_one_address_produce_identical_grades() -> None:
    """Scanning one address twice grades it the same both times."""
    first = cf.wait_for_scan(cf.submit_scan(cf.probe_email("same-a"))["reference"])
    second = cf.wait_for_scan(cf.submit_scan(cf.probe_email("same-b"))["reference"])
    assert first["overall"] == second["overall"], (
        f"two scans of {cf.SCAN_TARGET} must share one overall grade, got "
        f"{first['overall']!r} and {second['overall']!r}")
    grades_first = {s["name"]: s["grade"] for s in first["sections"]}
    grades_second = {s["name"]: s["grade"] for s in second["sections"]}
    assert grades_first == grades_second, (
        f"two scans of {cf.SCAN_TARGET} must share their section grades, got "
        f"{grades_first} and {grades_second}")


def test_scan_report_omits_the_name_of_the_person_who_submitted_it() -> None:
    """The public scan report carries no contact detail."""
    email = cf.probe_email("scan-private")
    reference = cf.submit_scan(email)["reference"]
    with appclient.client(None) as client:
        response = client.get(f"{cf.scans_path()}/{reference}")
    assert cf.SCAN_LAST_NAME not in response.text, (
        "a public scan report must not carry the surname of the lead")
    assert email not in response.text, (
        "a public scan report must not carry the business email of the lead")


def test_scan_address_naming_no_host_with_a_dot_is_refused_and_writes_nothing() -> None:
    """An address with no public host is refused and creates no scan."""
    before = cf.backend().count("scans")
    with appclient.client(None) as client:
        response = client.post(cf.scans_path(), json={
            "url": "localhost", "first_name": cf.SCAN_FIRST_NAME,
            "last_name": cf.SCAN_LAST_NAME,
            "business_email": cf.probe_email("bad-url")})
    assert response.status_code >= 400, cf.describe(
        response, "an address naming no host with a dot must be refused as invalid")
    assert cf.backend().count("scans") == before, (
        "a refused scan submission must write no scan row")


def test_scan_business_email_at_a_consumer_mail_domain_is_refused() -> None:
    """A consumer mail address is refused on the scanner form."""
    before = cf.backend().count("scans")
    with appclient.client(None) as client:
        response = client.post(cf.scans_path(), json={
            "url": cf.SCAN_TARGET, "first_name": cf.SCAN_FIRST_NAME,
            "last_name": cf.SCAN_LAST_NAME,
            "business_email": f"dana@{cf.CONSUMER_MAIL_DOMAINS[0]}"})
    assert response.status_code >= 400, cf.describe(
        response, "a business email at a consumer mail domain must be refused")
    assert cf.backend().count("scans") == before, (
        "a refused scan submission must write no scan row")


def test_fourth_scan_from_one_business_email_inside_an_hour_is_refused() -> None:
    """One business email may start three scans, never a fourth."""
    email = cf.probe_email("rate")
    for _ in range(3):
        cf.submit_scan(email)
    with appclient.client(None) as client:
        response = client.post(cf.scans_path(), json={
            "url": cf.SCAN_TARGET, "first_name": cf.SCAN_FIRST_NAME,
            "last_name": cf.SCAN_LAST_NAME, "business_email": email})
    assert response.status_code >= 400, cf.describe(
        response, f"a fourth scan from {email} inside an hour must be refused")
    assert cf.backend().count("scans", business_email=email) == 3, (
        f"{email} must hold exactly three scan rows")


def test_scan_lead_is_readable_on_the_leads_desk_with_its_business_email(author_token) -> None:
    """The leads desk shows each scan beside the email that started it."""
    email = cf.probe_email("lead")
    reference = cf.submit_scan(email)["reference"]
    with appclient.client(author_token) as client:
        response = client.get(cf.leads_path())
    assert response.status_code == 200, cf.describe(
        response, "an author must be able to read the leads desk")
    assert email in response.text, (
        f"the leads desk must show the business email {email} that started a scan")
    assert reference in response.text, (
        f"the leads desk must show the scan reference {reference}")


def test_new_newsletter_address_is_recorded_with_the_status_pending() -> None:
    """A new newsletter address is stored pending until confirmed."""
    email = cf.probe_email("sub-new")
    with appclient.client(None) as client:
        response = client.post(cf.subscribers_path(), json={"email": email})
    assert response.status_code < 300, cf.describe(
        response, f"a newsletter subscription for {email} must be accepted")
    row = cf.backend().one("subscribers", email=email)
    assert row is not None, f"the subscriber {email} must be a stored row"
    assert row["status"] == cf.SUBSCRIBER_PENDING, (
        f"a new subscriber must hold status {cf.SUBSCRIBER_PENDING}, got {row['status']!r}")


def test_repeated_newsletter_address_creates_no_second_subscriber_row() -> None:
    """Submitting one address twice leaves exactly one subscriber."""
    email = cf.probe_email("sub-repeat")
    with appclient.client(None) as client:
        client.post(cf.subscribers_path(), json={"email": email})
        client.post(cf.subscribers_path(), json={"email": email})
    assert cf.backend().count("subscribers", email=email) == 1, (
        f"a repeated subscription of {email} must create no second row")


def test_confirming_a_subscription_moves_the_status_to_confirmed() -> None:
    """Completing the confirmation step makes an address a subscriber."""
    email = cf.probe_email("sub-confirm")
    with appclient.client(None) as client:
        created = client.post(cf.subscribers_path(), json={"email": email})
        token = cf.backend().one("subscribers", email=email)["confirm_token"]
        response = client.post(f"{cf.subscribers_path()}/confirm", json={"token": token})
    assert created.status_code < 300, cf.describe(
        created, f"a newsletter subscription for {email} must be accepted")
    assert response.status_code < 300, cf.describe(
        response, f"the confirmation step for {email} must be accepted")
    assert cf.backend().one("subscribers", email=email)["status"] == cf.SUBSCRIBER_CONFIRMED, (
        f"{email} must hold status {cf.SUBSCRIBER_CONFIRMED} after confirmation")


def test_confirming_twice_leaves_one_confirmed_subscriber() -> None:
    """A repeated confirmation moves the stored state no second time."""
    email = cf.probe_email("sub-twice")
    with appclient.client(None) as client:
        client.post(cf.subscribers_path(), json={"email": email})
        token = cf.backend().one("subscribers", email=email)["confirm_token"]
        client.post(f"{cf.subscribers_path()}/confirm", json={"token": token})
        client.post(f"{cf.subscribers_path()}/confirm", json={"token": token})
    rows = cf.backend().rows("subscribers", email=email)
    assert len(rows) == 1, f"{email} must hold exactly one subscriber row"
    assert rows[0]["status"] == cf.SUBSCRIBER_CONFIRMED, (
        f"{email} must remain {cf.SUBSCRIBER_CONFIRMED} after a repeated confirmation")


def test_malformed_newsletter_address_is_rejected_and_writes_nothing() -> None:
    """A malformed newsletter address is refused and stores nothing."""
    before = cf.backend().count("subscribers")
    with appclient.client(None) as client:
        response = client.post(cf.subscribers_path(), json={"email": "not-an-address"})
    assert response.status_code >= 400, cf.describe(
        response, "a malformed newsletter address must be rejected as invalid")
    assert cf.backend().count("subscribers") == before, (
        "a rejected newsletter submission must write no subscriber row")


def test_contact_message_records_the_source_it_was_sent_from() -> None:
    """A contact message stores the surface that produced it."""
    email = cf.probe_email("message")
    with appclient.client(None) as client:
        response = client.post(cf.messages_path(), json={
            "name": "Dana Whitfield", "email": email,
            "body": "The pricing page moved somewhere I cannot find.",
            "source": cf.MESSAGE_SOURCE_NOT_FOUND})
    assert response.status_code < 300, cf.describe(
        response, "a contact message must be accepted")
    row = cf.backend().one("messages", email=email)
    assert row is not None, f"the contact message from {email} must be a stored row"
    assert row["source"] == cf.MESSAGE_SOURCE_NOT_FOUND, (
        f"a message sent from the not-found page must record source "
        f"{cf.MESSAGE_SOURCE_NOT_FOUND}, got {row['source']!r}")


def test_enterprise_contact_message_records_the_enterprise_source() -> None:
    """A message from the enterprise route records its own source."""
    email = cf.probe_email("enterprise")
    with appclient.client(None) as client:
        client.post(cf.messages_path(), json={
            "name": "Dana Whitfield", "email": email,
            "body": "We would like to standardise on this.",
            "source": cf.MESSAGE_SOURCE_ENTERPRISE})
    row = cf.backend().one("messages", email=email)
    assert row["source"] == cf.MESSAGE_SOURCE_ENTERPRISE, (
        f"an enterprise enquiry must record source {cf.MESSAGE_SOURCE_ENTERPRISE}")


def test_contact_message_missing_its_body_is_rejected() -> None:
    """A message with no body is refused and writes nothing."""
    email = cf.probe_email("no-body")
    with appclient.client(None) as client:
        response = client.post(cf.messages_path(), json={
            "name": "Dana Whitfield", "email": email, "body": "",
            "source": cf.MESSAGE_SOURCE_ENTERPRISE})
    assert response.status_code >= 400, cf.describe(
        response, "a contact message missing its body must be rejected as invalid")
    assert cf.backend().count("messages", email=email) == 0, (
        "a rejected contact message must write no row")


def test_page_view_row_records_the_route_and_the_moment(author_token) -> None:
    """Viewing a public route leaves a first-party page-view record."""
    before = cf.backend().count("page_views", route="/stories")
    with appclient.client(None) as client:
        client.get(cf.stories_path())
    cf.settle(1.0)
    rows = cf.backend().rows("page_views", route="/stories", limit=5)
    assert cf.backend().count("page_views", route="/stories") > before, (
        "a view of a public route must record a page view for that route")
    assert rows and rows[0].get("viewed_at") is not None, (
        "a page-view row must record the moment of the view")


def test_page_view_row_omits_the_account_when_analytics_consent_is_declined() -> None:
    """Without consent a page-view row identifies nobody."""
    with appclient.client(None) as client:
        client.post("/consent", json={"analytics": False})
        client.get(cf.stories_path())
    cf.settle(1.0)
    rows = cf.backend().rows("page_views", account_id=None, limit=5)
    assert rows, (
        "a viewer who declined the analytics cookie choice must produce a "
        "page-view row carrying no account reference")


def test_not_found_address_answers_four_hundred_four() -> None:
    """An address the site does not serve answers not found."""
    with appclient.client(None) as client:
        response = client.get("/stories/there-is-no-story-at-this-slug")
    assert response.status_code == 404, cf.describe(
        response, "an address the site does not serve must answer 404")


def test_seeded_accounts_stories_and_subscriber_are_present_once() -> None:
    """Seeding is idempotent, so a restart duplicates no seeded row."""
    backend = cf.backend()
    for email in (cf.AUTHOR_EMAIL, cf.AUTHOR2_EMAIL, cf.READER_EMAIL):
        assert backend.count("accounts", email=email) == 1, (
            f"the seeded account {email} must exist exactly once")
    for slug in (cf.OPEN_SLUG, cf.SECOND_OPEN_SLUG, cf.THIRD_OPEN_SLUG,
                 cf.MEMBERS_SLUG, cf.DRAFT_SLUG):
        assert backend.count("stories", slug=slug) == 1, (
            f"the seeded story {slug} must exist exactly once")
    assert backend.count("subscribers", email=cf.READER_EMAIL) == 1, (
        f"the seeded subscriber {cf.READER_EMAIL} must exist exactly once")


def test_seeded_story_covers_exist_in_the_object_store() -> None:
    """Every seeded story carries real cover bytes in the bucket."""
    store = cf.store()
    for slug in (cf.OPEN_SLUG, cf.MEMBERS_SLUG, cf.DRAFT_SLUG):
        identifier = cf.story_id(slug)
        keys = store.list(f"{cf.COVER_KEY_PREFIX}/{identifier}/")
        assert keys, (
            f"the seeded story {slug} must carry cover bytes in the object store")


def test_story_body_is_not_stored_in_the_cover_row() -> None:
    """Cover bytes live in the bucket, never as a database column."""
    identifier = cf.story_id(cf.OPEN_SLUG)
    row = cf.backend().one("story_covers", story_id=identifier)
    assert row is not None, f"the seeded story {cf.OPEN_SLUG} must carry a cover row"
    assert row.get("object_key"), (
        "a cover row must name the object key of the bytes in the bucket")
    assert cf.store().exists(row["object_key"]), (
        f"the cover object {row['object_key']} must exist in the bucket")


def test_database_at_the_database_url_holds_the_seeded_rows() -> None:
    """The records the app serves are rows the app reaches at DATABASE_URL."""
    row = cf.backend().one("stories", slug=cf.OPEN_SLUG)
    assert row is not None, (
        f"the story {cf.OPEN_SLUG} the app serves must be a row the app reaches "
        f"at DATABASE_URL")
    assert row["title"] == cf.OPEN_TITLE, (
        f"the stored row must carry the title the app serves, got {row['title']!r}")


def test_object_store_at_the_storage_endpoint_holds_the_cover_bytes() -> None:
    """Cover bytes live in the bucket the app reaches at STORAGE_ENDPOINT."""
    identifier = cf.story_id(cf.OPEN_SLUG)
    keys = cf.store().list(f"{cf.COVER_KEY_PREFIX}/{identifier}/")
    assert keys, (
        f"the object store the app reaches at STORAGE_ENDPOINT must hold cover "
        f"bytes for {cf.OPEN_SLUG}")
    assert cf.store().exists(keys[0]), (
        f"the object {keys[0]} must exist in the bucket the app names")


def test_every_response_carries_a_request_identifier_header() -> None:
    """Each response returns the request identifier its log line carries."""
    with appclient.client(None) as client:
        response = client.get(cf.stories_path())
    header = response.headers.get("x-request-id")
    assert header, (
        "every response must carry a request identifier in an X-Request-Id header")


def test_no_store_credential_appears_in_anything_the_browser_downloads() -> None:
    """Nothing the browser downloads carries the store access key."""
    access_key = os.environ.get("STORAGE_ACCESS_KEY", "")
    secret_key = os.environ.get("STORAGE_SECRET_KEY", "")
    assert access_key, "STORAGE_ACCESS_KEY must be set for this check to mean anything"
    with appclient.client(None) as client:
        documents = [client.get(cf.stories_path()).text,
                     client.get(f"{cf.stories_path()}/{cf.OPEN_SLUG}").text]
    for body in documents:
        assert access_key not in body, (
            "nothing the browser downloads may carry the store access key")
        assert secret_key not in body, (
            "nothing the browser downloads may carry the store secret key")


def test_concurrent_cover_uploads_for_one_story_leave_exactly_one_cover(author_token) -> None:
    """Two simultaneous cover uploads leave one cover row for the story."""
    slug = cf.probe_slug("cover-race")
    created = cf.create_probe_story(author_token, slug)
    identifier = created.get("id") or cf.story_id(slug)

    def upload(payload):
        def call():
            with appclient.client(author_token) as client:
                return client.post(
                    f"{cf.studio_stories_path()}/{identifier}/cover",
                    files={"file": ("cover.png", payload, "image/png")},
                    data={"alt_text": cf.COVER_ALT_TEXT})
        return call

    cf.run_together(upload(cf.PNG_BYTES), upload(cf.PNG_BYTES + b"\x01"))
    assert cf.backend().count("story_covers", story_id=identifier) == 1, (
        f"two concurrent cover uploads for story {identifier} must leave exactly "
        f"one cover row")


def test_concurrent_subscriptions_of_one_address_leave_exactly_one_subscriber() -> None:
    """Two simultaneous subscriptions of one address leave one subscriber."""
    email = cf.probe_email("sub-race")

    def subscribe():
        with appclient.client(None) as client:
            return client.post(cf.subscribers_path(), json={"email": email})

    cf.run_together(subscribe, subscribe)
    assert cf.backend().count("subscribers", email=email) == 1, (
        f"two concurrent subscriptions of {email} must leave exactly one "
        f"subscriber row")


def test_a_refused_story_create_leaves_no_orphaned_row(author_token) -> None:
    """A refused create writes nothing, leaving no orphaned story behind."""
    before = cf.backend().count("stories")
    with appclient.client(author_token) as client:
        response = client.post(cf.studio_stories_path(), json={
            "title": "", "slug": cf.probe_slug("orphan"),
            "category": "NotACategory", "intro": "", "body": "",
            "access": cf.ACCESS_OPEN})
    assert response.status_code >= 400, cf.describe(
        response, "a story create naming an unknown category must be refused")
    assert cf.backend().count("stories") == before, (
        "a refused story create must leave no orphaned row behind")


def test_scan_completes_for_an_address_that_does_not_resolve() -> None:
    """A scan finishes without ever fetching the address it was given."""
    reference = cf.submit_scan(cf.probe_email("no-fetch"),
                               target="this-host-does-not-resolve.example.com")["reference"]
    payload = cf.wait_for_scan(reference)
    assert payload["status"] == cf.SCAN_STATUS_COMPLETE, (
        "a scan must complete without fetching the submitted address")
    assert payload.get("overall") in cf.SCAN_GRADES, (
        "a completed scan must carry an overall grade whatever the address")


def test_no_payment_or_checkout_route_exists() -> None:
    """The app takes no payment, so no payment surface answers."""
    with appclient.client(None) as client:
        for path in ("/payments", "/checkout", "/subscriptions"):
            response = client.post(path, json={})
            assert response.status_code in (404, 405), cf.describe(
                response, f"the app takes no payment, so {path} must not answer")


def test_app_public_url_and_public_port_agree_with_the_environment() -> None:
    """The app answers on the public origin the environment names."""
    public_url = os.environ["APP_PUBLIC_URL"]
    public_port = os.environ["APP_PUBLIC_PORT"]
    assert public_port in public_url, (
        f"APP_PUBLIC_URL {public_url!r} must carry the public port {public_port!r}")
    with appclient.client(None) as client:
        response = client.get("/health")
    assert response.status_code == 200, cf.describe(
        response, f"the app must answer on the public origin {public_url}")


def test_app_answers_on_the_public_url_from_outside_the_container() -> None:
    """The app binds every interface, so it answers from another container."""
    with appclient.client(None) as client:
        response = client.get(cf.stories_path())
    assert response.status_code == 200, cf.describe(
        response, "a loopback-only listener is unreachable; the app must answer "
                  "on the public origin from outside its own container")


def test_server_still_answers_after_the_build_session_has_ended() -> None:
    """The server outlives the session that started it."""
    with appclient.client(None) as client:
        first = client.get("/health")
        cf.settle(1.0)
        second = client.get("/health")
    assert first.status_code == 200 and second.status_code == 200, (
        f"the server must still answer after the build session has ended, got "
        f"{first.status_code} then {second.status_code}")


def test_app_serves_a_production_build_rather_than_a_development_server() -> None:
    """The document the browser receives is a production build."""
    import httpx
    response = httpx.get(appclient.app_url() + "/", timeout=30.0)
    assert response.status_code == 200, cf.describe(
        response, "the app root must serve the application shell")
    body = response.text
    for marker in ("/@vite/client", "/@react-refresh", "webpack-dev-server"):
        assert marker not in body, (
            f"the app must serve a production build; the document carries the "
            f"development marker {marker!r}")


def test_invalid_call_is_rejected_as_a_client_error_rather_than_a_server_error() -> None:
    """A malformed request is refused as a client error."""
    with appclient.client(None) as client:
        response = client.post(cf.messages_path(), json={"nonsense": True})
    assert 400 <= response.status_code < 500, cf.describe(
        response, "an invalid call must be rejected as a client error, never a "
                  "server error and never a silent success")
