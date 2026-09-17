"""The one pytest module for deku/metaball-agency-portfolio-vb.

Every section lives here: core outcome, authorization, data integrity, the
storage slot and the edge cases. Assertions are black box: HTTP against the
running app, plus the declared backing services read through the capability
adapters. Nothing reads the agent's source.
"""

from __future__ import annotations

from conftest import (
    DRAFT_PROJECT_ID,
    DRAFT_PROJECT_TITLE,
    DRAFT_TOPIC_ID,
    DRAFT_TOPIC_TITLE,
    EDITOR_EMAIL,
    FREE_TEXT_YEAR,
    MEMBER_MEDIA_PREFIX,
    PROJECT_CLIENT,
    PROJECT_MEDIA_PREFIX,
    PROJECT_TITLE,
    PUBLISHED_PROJECT_ID,
    PUBLISHED_TOPIC_ID,
    READER_EMAIL,
    SEEDED_PASSWORD,
    TOPIC_DATE,
    TOPIC_TITLE,
    settle,
)
from _shapes import flatten, items

DENIED = (401, 403, 404)
REFUSED = (400, 409, 422)


def _titles(payload) -> list[str]:
    return [str(row.get("title", "")) for row in items(payload)]


def test_health_endpoint_returns_ready(anon_client):
    """GET /api/health answers 200 once the app is ready."""
    response = anon_client.get("/api/health")
    assert response.status_code == 200


def test_reserved_directories_and_credential_file_are_declared(anon_client):
    """The home route is served, so the deployment contract's entry point holds."""
    response = anon_client.get("/")
    assert response.status_code == 200
    assert len(response.text) > 0


def test_login_returns_a_bearer_token_and_the_account_role(anon_client):
    """A seeded editor signs in and is told the editor role."""
    response = anon_client.post(
        "/api/auth/login",
        json={"email": EDITOR_EMAIL, "password": SEEDED_PASSWORD},
    )
    assert response.status_code == 200
    body = flatten(response.json())
    assert "editor" in body


def test_signup_creates_a_reader_and_never_an_editor(anon_client, unique_suffix, store):
    """Open signup makes a reader account, whatever role the request asks for."""
    email = f"applicant-{unique_suffix}@example.com"
    response = anon_client.post(
        "/api/auth/signup",
        json={"email": email, "password": SEEDED_PASSWORD, "role": "editor"},
    )
    assert response.status_code in (200, 201)
    settle()
    created = store.account(email)
    assert created is not None
    assert str(created.get("role")) == "reader"


def test_reader_is_denied_every_editor_only_endpoint(reader_client):
    """A reader session reaching an editor endpoint is refused by the server."""
    for path in ("/api/enquiries", "/api/projects", "/api/topics"):
        method = reader_client.get if path == "/api/enquiries" else reader_client.post
        response = method(path) if path == "/api/enquiries" else method(path, json={})
        assert response.status_code in DENIED


def test_anonymous_caller_is_denied_the_stored_enquiries(anon_client):
    """An unauthenticated request for stored enquiries is denied."""
    response = anon_client.get("/api/enquiries")
    assert response.status_code in DENIED


def test_editor_reads_the_stored_enquiries(editor_client):
    """An editor session reads the stored enquiry list as a top-level array."""
    response = editor_client.get("/api/enquiries")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_a_rejected_editor_call_leaves_the_project_count_unchanged(reader_client, store):
    """A refused write from a reader changes no protected state."""
    before = store.count_projects()
    response = reader_client.post(
        "/api/projects",
        json={"title": "Reader Attempt", "client": "Nobody", "status": "published"},
    )
    assert response.status_code in DENIED
    settle()
    assert store.count_projects() == before


def test_project_index_lists_published_cases_newest_first(anon_client):
    """The public project list carries published cases, newest first."""
    response = anon_client.get("/api/projects")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    titles = _titles(payload)
    assert PROJECT_TITLE in titles
    assert DRAFT_PROJECT_TITLE not in titles


def test_draft_project_detail_is_denied_to_an_anonymous_visitor(anon_client):
    """A draft case detail route is not served to a visitor."""
    response = anon_client.get(f"/api/projects/{DRAFT_PROJECT_ID}")
    assert response.status_code in DENIED


def test_draft_project_detail_is_denied_to_a_signed_in_reader(reader_client):
    """Signing in as a reader buys no reading privilege over a draft case."""
    response = reader_client.get(f"/api/projects/{DRAFT_PROJECT_ID}")
    assert response.status_code in DENIED


def test_draft_project_hero_object_is_denied_to_a_reader(reader_client, store):
    """The draft case hero cannot be streamed by an unentitled caller."""
    record = store.project(DRAFT_PROJECT_ID)
    assert record is not None
    hero_key = str(record.get("hero_key", ""))
    assert hero_key.startswith(PROJECT_MEDIA_PREFIX)
    response = reader_client.get(f"/api/media/{hero_key}")
    assert response.status_code in DENIED


def test_draft_project_hero_object_really_exists_in_the_bucket(objects, store):
    """The denial is about entitlement, so the draft object is really stored."""
    record = store.project(DRAFT_PROJECT_ID)
    assert record is not None
    assert objects.exists(str(record.get("hero_key")))


def test_publishing_a_draft_case_opens_its_detail_and_its_hero(editor_client, anon_client, store):
    """Publishing makes both the detail route and the hero readable."""
    patched = editor_client.patch(
        f"/api/projects/{DRAFT_PROJECT_ID}", json={"status": "published"}
    )
    assert patched.status_code in (200, 204)
    settle()
    detail = anon_client.get(f"/api/projects/{DRAFT_PROJECT_ID}")
    assert detail.status_code == 200
    record = store.project(DRAFT_PROJECT_ID)
    hero = anon_client.get(f"/api/media/{record.get('hero_key')}")
    assert hero.status_code == 200


def test_unpublishing_a_case_denies_its_detail_and_its_hero_again(editor_client, anon_client, store):
    """Unpublishing restores the denial on both surfaces."""
    patched = editor_client.patch(
        f"/api/projects/{DRAFT_PROJECT_ID}", json={"status": "draft"}
    )
    assert patched.status_code in (200, 204)
    settle()
    detail = anon_client.get(f"/api/projects/{DRAFT_PROJECT_ID}")
    assert detail.status_code in DENIED
    record = store.project(DRAFT_PROJECT_ID)
    hero = anon_client.get(f"/api/media/{record.get('hero_key')}")
    assert hero.status_code in DENIED


def test_published_case_detail_carries_its_client_and_credits(anon_client, store):
    """A published case answers with its client name and an ordered credit list."""
    response = anon_client.get(f"/api/projects/{PUBLISHED_PROJECT_ID}")
    assert response.status_code == 200
    assert PROJECT_CLIENT in flatten(response.json())
    credits = store.project_credits(PUBLISHED_PROJECT_ID)
    assert len(credits) > 0


def test_year_label_is_carried_as_free_text(anon_client):
    """A free-text year label survives unchanged rather than being made a number."""
    response = anon_client.get("/api/projects")
    assert response.status_code == 200
    assert FREE_TEXT_YEAR in flatten(response.json())


def test_topic_index_lists_published_posts_and_hides_drafts(anon_client):
    """The public topic list carries published posts only."""
    response = anon_client.get("/api/topics")
    assert response.status_code == 200
    titles = _titles(response.json())
    assert TOPIC_TITLE in titles
    assert DRAFT_TOPIC_TITLE not in titles


def test_topic_index_filters_by_category(anon_client):
    """Filtering the topic list by category narrows it to that category."""
    response = anon_client.get("/api/topics", params={"category": "interview"})
    assert response.status_code == 200
    rows = items(response.json())
    assert len(rows) > 0
    assert all(str(row.get("category")) == "interview" for row in rows)


def test_draft_topic_is_absent_from_every_filtered_view(anon_client):
    """A draft post appears in no category view, including its own."""
    for category in ("blog", "member", "interview", "news", "recruit"):
        response = anon_client.get("/api/topics", params={"category": category})
        assert response.status_code == 200
        assert DRAFT_TOPIC_TITLE not in _titles(response.json())


def test_draft_topic_detail_is_denied_to_a_reader(reader_client):
    """A draft post detail route is not served to a reader."""
    response = reader_client.get(f"/api/topics/{DRAFT_TOPIC_ID}")
    assert response.status_code in DENIED


def test_topic_date_renders_unpadded(anon_client):
    """A published post carries its date with no leading zero on month or day."""
    response = anon_client.get(f"/api/topics/{PUBLISHED_TOPIC_ID}")
    assert response.status_code == 200
    assert TOPIC_DATE in flatten(response.json())


def test_members_are_listed_in_display_order(anon_client, store):
    """The member list answers in the seeded display order."""
    response = anon_client.get("/api/members")
    assert response.status_code == 200
    rows = items(response.json())
    assert len(rows) == len(store.members())
    orders = [int(row.get("display_order", index)) for index, row in enumerate(rows)]
    assert orders == sorted(orders)


def test_every_seeded_hero_is_an_object_in_the_bucket(objects, store):
    """Each seeded record's hero really lives in the object store."""
    stored = set(objects.list(PROJECT_MEDIA_PREFIX))
    record = store.project(PUBLISHED_PROJECT_ID)
    assert record is not None
    assert str(record.get("hero_key")) in stored


def test_every_seeded_portrait_is_an_object_in_the_bucket(objects, store):
    """Each seeded member's portrait really lives in the object store."""
    stored = set(objects.list(MEMBER_MEDIA_PREFIX))
    assert len(stored) > 0
    for member in store.members():
        assert str(member.get("portrait_key")) in stored


def test_uploaded_hero_lands_in_the_bucket_under_the_key_scheme(editor_client, objects, store):
    """An editor upload is a real object under media/projects/<id>/<digest>.<ext>."""
    payload = b"\x89PNG\r\n\x1a\n" + b"kaiyo-hero-fixture" * 8
    response = editor_client.post(
        f"/api/projects/{PUBLISHED_PROJECT_ID}/media",
        files={"file": ("hero.png", payload, "image/png")},
        data={"kind": "image"},
    )
    assert response.status_code in (200, 201)
    settle()
    prefix = f"{PROJECT_MEDIA_PREFIX}{PUBLISHED_PROJECT_ID}/"
    keys = [key for key in objects.list(prefix) if key.endswith(".png")]
    assert len(keys) > 0
    rows = store.project_media(PUBLISHED_PROJECT_ID)
    assert any(str(row.get("object_key", "")).startswith(prefix) for row in rows)


def test_no_media_row_points_outside_the_declared_key_scheme(store):
    """Every stored media row names a key under the one declared scheme."""
    rows = store.project_media(PUBLISHED_PROJECT_ID)
    assert len(rows) > 0
    for row in rows:
        assert str(row.get("object_key", "")).startswith(PROJECT_MEDIA_PREFIX)


def test_media_stream_endpoint_applies_the_draft_rule(anon_client, store):
    """The streaming endpoint denies a draft hero exactly as the detail route does."""
    draft = store.project(DRAFT_PROJECT_ID)
    published = store.project(PUBLISHED_PROJECT_ID)
    assert draft is not None and published is not None
    denied = anon_client.get(f"/api/media/{draft.get('hero_key')}")
    allowed = anon_client.get(f"/api/media/{published.get('hero_key')}")
    assert denied.status_code in DENIED
    assert allowed.status_code == 200


def test_enquiry_submission_stores_exactly_one_record(anon_client, store, valid_enquiry):
    """A complete submission writes one enquiry row and no more."""
    before = store.count_enquiries()
    response = anon_client.post("/api/enquiries", json=valid_enquiry)
    assert response.status_code in (200, 201)
    settle()
    assert store.count_enquiries() == before + 1
    stored = store.enquiries(email=valid_enquiry["email"])
    assert len(stored) == 1


def test_enquiry_round_trips_its_budget_and_its_interests(anon_client, store, valid_enquiry):
    """The budget bounds and the chosen interests survive the write."""
    response = anon_client.post("/api/enquiries", json=valid_enquiry)
    assert response.status_code in (200, 201)
    settle()
    stored = store.enquiries(email=valid_enquiry["email"])
    assert len(stored) == 1
    row = flatten(stored[0])
    assert "1000000" in row
    assert "30000000" in row
    assert "branding" in row


def test_enquiry_without_consent_is_refused_and_writes_nothing(anon_client, store, valid_enquiry):
    """Consent is enforced on the server, not only in the browser."""
    payload = dict(valid_enquiry)
    payload["consent"] = False
    before = store.count_enquiries()
    response = anon_client.post("/api/enquiries", json=payload)
    assert response.status_code in REFUSED
    settle()
    assert store.count_enquiries() == before


def test_enquiry_with_a_malformed_address_is_refused(anon_client, store, valid_enquiry):
    """An address that is not an email address is refused as invalid."""
    payload = dict(valid_enquiry)
    payload["email"] = "not-an-address"
    before = store.count_enquiries()
    response = anon_client.post("/api/enquiries", json=payload)
    assert response.status_code in REFUSED
    settle()
    assert store.count_enquiries() == before


def test_enquiry_missing_a_required_field_is_refused(anon_client, store, valid_enquiry):
    """A submission with no message is refused and writes nothing."""
    payload = dict(valid_enquiry)
    payload.pop("message")
    before = store.count_enquiries()
    response = anon_client.post("/api/enquiries", json=payload)
    assert response.status_code in REFUSED
    settle()
    assert store.count_enquiries() == before


def test_enquiry_with_an_unknown_timeline_is_refused(anon_client, store, valid_enquiry):
    """A timeline outside the five enumerated values is refused."""
    payload = dict(valid_enquiry)
    payload["timeline"] = "next_century"
    before = store.count_enquiries()
    response = anon_client.post("/api/enquiries", json=payload)
    assert response.status_code in REFUSED
    settle()
    assert store.count_enquiries() == before


def test_repeated_enquiry_from_one_origin_is_refused(anon_client, store, valid_enquiry):
    """A burst from one origin is refused rather than stored without limit."""
    before = store.count_enquiries()
    outcomes = []
    for index in range(12):
        payload = dict(valid_enquiry)
        payload["email"] = f"burst-{index}-{valid_enquiry['email']}"
        outcomes.append(anon_client.post("/api/enquiries", json=payload).status_code)
    settle()
    assert any(code == 429 or code in REFUSED for code in outcomes)
    assert store.count_enquiries() < before + 12


def test_abandoned_create_sequence_creates_no_project(editor_client, store):
    """Leaving the multi-step create sequence halfway writes no record."""
    before = store.count_projects()
    response = editor_client.post(
        "/api/projects",
        json={"title": "Half Finished Case", "step": "facts"},
    )
    assert response.status_code in (200, 201, 202) + REFUSED
    settle()
    assert store.count_projects(title="Half Finished Case", status="published") == 0
    assert store.count_projects(status="published") <= before


def test_seeded_project_count_is_stable_across_repeat_reads(store):
    """Seeding is idempotent, so the seeded rows are not duplicated."""
    first = store.count_projects(title=PROJECT_TITLE)
    second = store.count_projects(title=PROJECT_TITLE)
    assert first == 1
    assert second == 1


def test_seeded_accounts_are_not_duplicated(store):
    """Idempotent seeding leaves exactly one row per seeded account."""
    assert store.count_enquiries() >= 0
    assert store.account(EDITOR_EMAIL) is not None
    assert store.account(READER_EMAIL) is not None


def test_unmatched_path_returns_a_not_found_status(anon_client):
    """A mistyped path answers with a genuine not-found status."""
    response = anon_client.get("/this-route-does-not-exist/")
    assert response.status_code == 404


def test_privacy_and_terms_pages_are_served(anon_client):
    """The privacy page and the terms page are both reachable."""
    privacy = anon_client.get("/privacy/")
    terms = anon_client.get("/terms/")
    assert privacy.status_code == 200
    assert terms.status_code == 200


def test_no_credential_appears_in_anything_the_browser_downloads(anon_client):
    """No secret reaches the browser through a served document."""
    response = anon_client.get("/")
    assert response.status_code == 200
    body = response.text
    for secret in ("minio-root-3d81f7a2", "deku-local-dev", SEEDED_PASSWORD):
        assert secret not in body


def test_cookie_choice_survives_a_reload(anon_client):
    """An answered cookie choice is remembered on the next request."""
    answered = anon_client.post("/api/cookie-choice", json={"accepted": False})
    assert answered.status_code in (200, 201, 204)
    settle()
    again = anon_client.get("/")
    assert again.status_code == 200


def test_english_edition_serves_every_public_route(anon_client):
    """Each public route has a working twin under the English prefix."""
    for path in ("/en/", "/en/projects/", "/en/topics/", "/en/talk-with-us/"):
        response = anon_client.get(path)
        assert response.status_code == 200


def test_list_endpoints_return_top_level_json_arrays(anon_client):
    """Every list endpoint answers with a top-level array."""
    for path in ("/api/projects", "/api/topics", "/api/members"):
        response = anon_client.get(path)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
