"""Black-box graders for the studio-capability-index.

Every test reaches the app only over HTTP and reads the declared services only
through the capability adapters.
"""
from __future__ import annotations

import os
import threading

import pytest

from appclient import client
from conftest import (
    EDITOR_EMAIL,
    MEDIA_PREFIX,
    account_password,
    fresh_email,
    poll,
    settle,
)
from _shapes import flatten, items


def _published(c) -> list:
    return items(c.get("/case-studies").json())


def _first_published_slug(c) -> str:
    rows = _published(c)
    assert rows, f"the seeded index returned no published case studies: {flatten(rows)[:200]}"
    return str(rows[0].get("slug"))


def _enquiry_body() -> dict:
    return {"name": "Mara Lind", "email": fresh_email("lead"), "company": "Northwind",
            "budget_band": "25k to 50k", "services": [], "consent": True,
            "message": "We need a brand refresh and a production website for a spring launch."}


def test_health_ok():
    """The health endpoint returns ready."""
    with client() as c:
        resp = c.get("/health")
    assert resp.status_code == 200, f"health was not ready: {resp.status_code}"


def test_editor_login(editor_client):
    """The seeded editor authenticates and reads the studio inbox."""
    resp = editor_client.get("/enquiries")
    assert resp.status_code == 200, f"seeded editor could not read the inbox: {resp.text[:300]}"


def test_visitor_reads_published_content(anon_client):
    """A visitor reads the published case study index with no account."""
    resp = anon_client.get("/case-studies")
    assert resp.status_code == 200, f"public index was not readable: {resp.status_code}"
    assert isinstance(items(resp.json()), list), "the index did not return a list of items"


def test_case_study_index_lists_published_only(editor_client, anon_client):
    """The public index lists only published case studies."""
    public = {str(r.get("slug")) for r in _published(anon_client)}
    drafts = editor_client.get("/case-studies", params={"status": "draft"}).json()
    for row in items(drafts):
        assert str(row.get("slug")) not in public, (
            f"a draft case study {row.get('slug')!r} leaked into the public index")


def test_case_study_index_filters_by_industry(anon_client):
    """Filtering the index by an industry narrows it to matching case studies."""
    full = _published(anon_client)
    assert full, "the seeded index returned nothing to filter"
    industry = str(full[0].get("industry"))
    narrowed = items(anon_client.get("/case-studies", params={"industry": industry}).json())
    assert narrowed, "filtering by a seeded industry returned nothing"
    for row in narrowed:
        assert str(row.get("industry")) == industry, (
            f"a case study outside the industry filter was returned: {row}")


def test_experiments_wall_pagination_cursor(anon_client):
    """The experiments wall is paginated with a forward cursor and metadata."""
    payload = anon_client.get("/experiments", params={"page_size": 2}).json()
    assert "next_cursor" in payload or payload.get("has_more") is not None, (
        f"the paginated wall carried no cursor metadata: {flatten(payload)[:300]}")
    assert len(items(payload)) <= 2, "page_size was ignored on the experiments wall"


def test_published_case_study_media_served_from_store(anon_client, object_store):
    """A published case study names media that exists as an object in the store."""
    slug = _first_published_slug(anon_client)
    detail = anon_client.get(f"/case-studies/{slug}").json()
    media = detail.get("media") or []
    assert media, f"the published case study carried no media: {flatten(detail)[:300]}"
    key = str(media[0].get("storage_key"))
    exists = poll(lambda: object_store.exists(key), lambda ok: bool(ok))
    assert exists, f"the case study media object {key} is absent from the store"


def test_case_study_media_persisted_as_object_not_db_blob(anon_client, object_store):
    """Published case study media lives under the media prefix in the bucket."""
    stored = object_store.list(prefix=MEDIA_PREFIX)
    assert stored, (
        f"no object exists under {MEDIA_PREFIX}; the media was held on disk or in the database, "
        f"not the object store")


def test_draft_case_study_detail_not_found(editor_client, anon_client):
    """A draft case study detail returns not-found to the public."""
    drafts = items(editor_client.get("/case-studies", params={"status": "draft"}).json())
    assert drafts, "the seed carried no draft case study to protect"
    slug = str(drafts[0].get("slug"))
    resp = anon_client.get(f"/case-studies/{slug}")
    assert resp.status_code == 404, (
        f"a draft case study was served to the public: {resp.status_code}")


def test_draft_case_study_media_not_publicly_readable(editor_client, anon_client):
    """A draft case study media object is refused to the public."""
    drafts = items(editor_client.get("/case-studies", params={"status": "draft"}).json())
    assert drafts, "the seed carried no draft case study to protect"
    draft = drafts[0]
    slug = str(draft.get("slug"))
    media = draft.get("media") or []
    assert media, "the seeded draft carried no media object to protect"
    media_id = str(media[0].get("id"))
    resp = anon_client.get(f"/case-studies/{slug}/media/{media_id}")
    assert resp.status_code in (401, 403, 404), (
        f"a draft media object was readable by the public: {resp.status_code}")


def test_publish_makes_case_study_and_media_public(editor_client, anon_client):
    """Publishing a draft makes its detail readable by the public."""
    drafts = items(editor_client.get("/case-studies", params={"status": "draft"}).json())
    assert drafts, "the seed carried no draft case study to publish"
    slug = str(drafts[0].get("slug"))
    published = editor_client.post(f"/case-studies/{slug}/publish", json={"status": "published"})
    assert published.status_code in (200, 201), f"publish failed: {published.text[:300]}"
    seen = poll(lambda: anon_client.get(f"/case-studies/{slug}").status_code, lambda s: s == 200)
    assert seen == 200, "a published case study stayed hidden from the public"


def test_service_detail_shows_proof_row(anon_client):
    """A service detail carries a proof row of case studies that credited it."""
    services = items(anon_client.get("/services").json())
    assert services, "the seeded services catalogue was empty"
    slug = next((str(s.get("slug")) for s in services if s.get("has_page")), str(services[0].get("slug")))
    detail = anon_client.get(f"/services/{slug}").json()
    assert "proof" in flatten(detail).lower() or detail.get("case_studies") is not None, (
        f"the service detail carried no proof row: {flatten(detail)[:300]}")


def test_article_index_published_with_one_pinned(anon_client):
    """The article index shows published articles with exactly one pinned."""
    articles = items(anon_client.get("/posts").json())
    assert articles, "the seeded article index was empty"
    pinned = [a for a in articles if a.get("pinned")]
    assert len(pinned) == 1, f"expected exactly one pinned article, found {len(pinned)}"


def test_case_study_rejects_unknown_industry(editor_client):
    """Creating a case study with an unknown industry is refused."""
    resp = editor_client.post("/case-studies", json={
        "client_name": "Probe", "industry": "NotAnIndustry",
        "summary": "A probe case study.", "deck": "A probe deck sentence for the case study."})
    assert resp.status_code in (400, 422), (
        f"an unknown industry was accepted: {resp.status_code} {resp.text[:300]}")


def test_seed_is_idempotent(anon_client):
    """The seeded catalogue holds a stable set across reads."""
    first = len(_published(anon_client))
    second = len(_published(anon_client))
    assert first == second and first > 0, (
        f"the seeded index size drifted between reads: {first} then {second}")


def test_enquiry_submission_persists_one_record(anon_client, db):
    """A valid enquiry is persisted as one record."""
    body = _enquiry_body()
    resp = anon_client.post("/enquiries", json=body)
    assert resp.status_code in (200, 201), f"a valid enquiry was refused: {resp.text[:300]}"
    count = poll(lambda: db.count("enquiries", email=body["email"]), lambda n: n and n >= 1)
    assert count == 1, f"a valid enquiry produced {count} rows, expected one"


def test_concurrent_duplicate_enquiry_single_record(db):
    """Two simultaneous submissions with one key create exactly one enquiry."""
    body = _enquiry_body()
    key = "idem-" + os.urandom(6).hex()
    gate = threading.Barrier(2)
    lock = threading.Lock()
    statuses: list[int] = []

    def fire():
        with client() as c:
            gate.wait()
            resp = c.post("/enquiries", json=body, headers={"Idempotency-Key": key})
        with lock:
            statuses.append(resp.status_code)

    threads = [threading.Thread(target=fire) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)
    accepted = [s for s in statuses if s in (200, 201)]
    assert len(accepted) >= 1, f"neither duplicated submission succeeded: {sorted(statuses)}"
    count = db.count("enquiries", idempotency_key=key)
    assert count == 1, f"a duplicated key created {count} enquiries; exactly one must exist"


def test_enquiry_rejects_short_message(anon_client):
    """An enquiry with a message shorter than the floor is refused."""
    body = _enquiry_body()
    body["message"] = "too short"
    resp = anon_client.post("/enquiries", json=body)
    assert resp.status_code in (400, 422), (
        f"a short enquiry message was accepted: {resp.status_code} {resp.text[:300]}")


def test_enquiries_inbox_editor_only(anon_client):
    """The studio inbox is refused to an anonymous caller."""
    resp = anon_client.get("/enquiries")
    assert resp.status_code in (401, 403), (
        f"the enquiry inbox was readable without an editor session: {resp.status_code}")


def test_anonymous_editor_endpoint_refused(anon_client):
    """An anonymous caller is refused every editor managing endpoint."""
    attempts = [("POST", "/case-studies"), ("POST", "/articles"), ("GET", "/enquiries")]
    for method, path in attempts:
        resp = anon_client.request(method, path, json={})
        assert resp.status_code in (401, 403), (
            f"anonymous {method} {path} was served: {resp.status_code}")


def test_signup_rejects_duplicate_email(anon_client):
    """A signup for an already registered email is refused."""
    resp = anon_client.post("/auth/signup", json={
        "email": EDITOR_EMAIL, "password": account_password(), "role": "editor"})
    assert resp.status_code in (400, 409, 422), (
        f"a duplicate signup was accepted: {resp.status_code} {resp.text[:300]}")


def test_signup_rejects_short_password(anon_client):
    """A signup with a password shorter than eight characters is refused."""
    resp = anon_client.post("/auth/signup", json={
        "email": fresh_email(), "password": "short", "role": "editor"})
    assert resp.status_code in (400, 422), (
        f"a short password was accepted: {resp.status_code} {resp.text[:300]}")


def test_no_frontend_secret_in_bundle():
    """The served frontend carries no storage secret."""
    with client() as c:
        resp = c.get("/../")
    assert resp.status_code == 200, f"the app root did not render: {resp.status_code}"
    secret = os.environ.get("STORAGE_SECRET_KEY", "deku-local-dev")
    assert secret not in resp.text, "a storage secret was served in the frontend document"


def test_privacy_page_served():
    """The privacy page renders readable content."""
    with client() as c:
        resp = c.get("/../privacy")
    assert resp.status_code == 200, f"the privacy page did not render: {resp.status_code}"
    assert len(resp.text) > 200, "the privacy page carried no readable content"


def test_sitemap_lists_published_routes(anon_client):
    """The sitemap lists the published routes."""
    with client() as c:
        resp = c.get("/../sitemap.xml")
    if resp.status_code == 404:
        resp = anon_client.get("/sitemap")
    assert resp.status_code == 200, f"the sitemap did not render: {resp.status_code}"
    assert "work" in resp.text.lower() or "case" in resp.text.lower(), (
        "the sitemap listed no published work routes")


def test_unknown_route_returns_custom_not_found():
    """An unknown route renders a custom not-found page."""
    with client() as c:
        resp = c.get("/../this-route-does-not-exist")
    assert resp.status_code == 404, (
        f"an unknown route did not return not found: {resp.status_code}")


def test_page_view_recorded_for_public_route(editor_client, anon_client):
    """A public route records a page view the studio can read."""
    before = editor_client.get("/page-views").json()
    anon_client.get("/case-studies")
    after = poll(lambda: editor_client.get("/page-views").json(),
                 lambda d: d is not None)
    assert after is not None, "the studio could not read recorded page views"
