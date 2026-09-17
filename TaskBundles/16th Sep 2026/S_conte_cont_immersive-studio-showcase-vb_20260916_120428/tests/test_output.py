from __future__ import annotations

import concurrent.futures

import appclient
import conftest
from _shapes import flatten, items


def test_health_reports_ready(anon_client):
    """The readiness route answers once the datastore and the bucket are reachable."""
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:400]}"
    )


def test_login_returns_access_token():
    """A seeded account signs in with the pinned password and receives a bearer token."""
    token = appclient.login(conftest.AUTHOR_EMAIL, conftest.PASSWORD)
    assert isinstance(token, str) and token, (
        f"login for {conftest.AUTHOR_EMAIL} returned no usable access_token"
    )
    with appclient.client(token) as c:
        me = c.get("/me")
    assert me.status_code == 200, (
        f"GET /api/me with a fresh token returned {me.status_code}: {me.text[:400]}"
    )
    assert "author" in flatten(me.json()).lower(), (
        f"GET /api/me for {conftest.AUTHOR_EMAIL} does not report the author role: "
        f"{me.text[:400]}"
    )


def test_login_refusals_are_indistinguishable(anon_client):
    """An unknown address and a wrong password are refused in the same shape."""
    unknown = anon_client.post(
        "/auth/login",
        json={"email": conftest.unique_email(), "password": conftest.PASSWORD},
    )
    wrong = anon_client.post(
        "/auth/login",
        json={"email": conftest.AUTHOR_EMAIL, "password": "not-the-seeded-password"},
    )
    assert unknown.status_code in (400, 401, 403), (
        f"login with an unknown address returned {unknown.status_code}, which is not a "
        f"refusal: {unknown.text[:400]}"
    )
    assert unknown.status_code == wrong.status_code, (
        f"an unknown address returned {unknown.status_code} while a wrong password "
        f"returned {wrong.status_code}; the pair reveals whether the address exists"
    )
    assert flatten(unknown.text).strip() == flatten(wrong.text).strip(), (
        "the refusal body for an unknown address differs from the refusal body for a "
        f"wrong password: {unknown.text[:200]!r} versus {wrong.text[:200]!r}"
    )


def test_signup_creates_reader_only(anon_client, backend):
    """Open signup creates a reader, and a payload asking for the author role still does."""
    email = conftest.unique_email()
    response = anon_client.post(
        "/auth/signup",
        json={
            "email": email,
            "password": conftest.PASSWORD,
            "display_name": "Probe Visitor",
            "role": "author",
        },
    )
    assert response.status_code in (200, 201), (
        f"signup for {email} returned {response.status_code}: {response.text[:400]}"
    )
    body = flatten(response.json()).lower()
    assert "reader" in body, (
        f"signup for {email} did not report the reader role: {response.text[:400]}"
    )
    row = backend.one("account", email=email)
    assert row is not None, f"signup for {email} wrote no account row"
    assert row.get("role") == "reader", (
        f"the account row for {email} holds role {row.get('role')!r}; a signup asking "
        f"for author must still be a reader"
    )


def test_public_case_list_excludes_drafts(anon_client, reader_client):
    """Neither an anonymous visitor nor a reader sees the draft case in the list."""
    for label, client in (("anonymous", anon_client), ("reader", reader_client)):
        response = client.get("/cases")
        assert response.status_code == 200, (
            f"GET /api/cases as {label} returned {response.status_code}: "
            f"{response.text[:400]}"
        )
        slugs = [row.get("slug") for row in items(response.json())]
        assert conftest.DRAFT_CASE_SLUG not in slugs, (
            f"GET /api/cases as {label} lists the draft case "
            f"{conftest.DRAFT_CASE_SLUG!r}: {slugs}"
        )
        for slug in conftest.PUBLISHED_CASE_SLUGS:
            assert slug in slugs, (
                f"GET /api/cases as {label} omits the published case {slug!r}: {slugs}"
            )


def test_author_case_list_includes_drafts(author_client):
    """An author asking for drafts receives the draft case that nobody else may read."""
    response = author_client.get("/cases", params={"state": "draft"})
    assert response.status_code == 200, (
        f"GET /api/cases?state=draft as an author returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    slugs = [row.get("slug") for row in items(response.json())]
    assert conftest.DRAFT_CASE_SLUG in slugs, (
        f"an author asking for drafts does not receive {conftest.DRAFT_CASE_SLUG!r}: "
        f"{slugs}"
    )


def test_draft_case_answers_as_absent(anon_client):
    """An anonymous request for the draft case matches a request for a slug that never existed."""
    draft = anon_client.get(f"/cases/{conftest.DRAFT_CASE_SLUG}")
    absent = anon_client.get(f"/cases/{conftest.unique_slug('never-existed')}")
    assert conftest.looks_absent(draft), (
        f"GET /api/cases/{conftest.DRAFT_CASE_SLUG} as an anonymous visitor returned "
        f"{draft.status_code}: {draft.text[:400]}"
    )
    assert draft.status_code == absent.status_code, (
        f"the draft case returned {draft.status_code} while an absent slug returned "
        f"{absent.status_code}; the difference reveals that the draft exists"
    )
    assert flatten(draft.text).strip() == flatten(absent.text).strip(), (
        "the draft case body differs from the absent-slug body, so existence leaks "
        f"through the wording: {draft.text[:200]!r} versus {absent.text[:200]!r}"
    )


def test_reader_draft_case_answers_as_absent(reader_client):
    """A signed-in reader receives the same absence answer as a stranger."""
    draft = reader_client.get(f"/cases/{conftest.DRAFT_CASE_SLUG}")
    absent = reader_client.get(f"/cases/{conftest.unique_slug('never-existed')}")
    assert conftest.looks_absent(draft), (
        f"GET /api/cases/{conftest.DRAFT_CASE_SLUG} as a reader returned "
        f"{draft.status_code}: {draft.text[:400]}"
    )
    assert conftest.refusal_fingerprint(draft) == conftest.refusal_fingerprint(absent), (
        f"a reader asking for the draft case gets {draft.status_code} with a "
        f"{len(draft.text)}-character body, while an absent slug gets "
        f"{absent.status_code} with {len(absent.text)}; a reader is not a lesser author"
    )
    route = conftest.page(f"/cases/{conftest.DRAFT_CASE_SLUG}")
    assert route.status_code == 404, (
        f"the HTML route for the draft case returned {route.status_code} to a reader "
        f"rather than the not-found page"
    )


def test_author_reads_draft_case(author_client):
    """An author reads the draft case in full, headline and bands included."""
    response = author_client.get(f"/cases/{conftest.DRAFT_CASE_SLUG}")
    assert response.status_code == 200, (
        f"GET /api/cases/{conftest.DRAFT_CASE_SLUG} as an author returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    body = flatten(response.json()).lower()
    assert "draft" in body, (
        f"the draft case read by an author does not report the draft state: "
        f"{response.text[:400]}"
    )


def test_draft_asset_is_denied_by_object_key(anon_client, reader_client, author_client, store):
    """The draft case's hero object exists in the bucket and is unreadable without the author role."""
    detail = author_client.get(f"/cases/{conftest.DRAFT_CASE_SLUG}")
    assert detail.status_code == 200, (
        f"an author cannot read {conftest.DRAFT_CASE_SLUG!r} to find its hero key: "
        f"{detail.text[:400]}"
    )
    keys = [k for k in store.list(f"cases/{conftest.DRAFT_CASE_SLUG}/")]
    assert keys, (
        f"the bucket holds no object under cases/{conftest.DRAFT_CASE_SLUG}/; the draft "
        f"case must carry a real hero object in the same bucket as a published one"
    )
    key = keys[0]
    for label, client in (("anonymous", anon_client), ("reader", reader_client)):
        response = client.get(f"/assets/{key}")
        assert conftest.looks_absent(response), (
            f"GET /api/assets/{key} as {label} returned {response.status_code}; a draft "
            f"record's bytes must be unreachable by object key"
        )
    allowed = author_client.get(f"/assets/{key}")
    assert allowed.status_code == 200, (
        f"GET /api/assets/{key} as an author returned {allowed.status_code}; the author "
        f"must still be able to read the draft's own media"
    )


def test_published_asset_streams_from_store(anon_client, store):
    """A published case's hero image is served from the bucket to anybody."""
    detail = anon_client.get(f"/cases/{conftest.PUBLISHED_CASE_SLUG}")
    assert detail.status_code == 200, (
        f"GET /api/cases/{conftest.PUBLISHED_CASE_SLUG} returned {detail.status_code}: "
        f"{detail.text[:400]}"
    )
    keys = store.list(f"cases/{conftest.PUBLISHED_CASE_SLUG}/")
    assert keys, (
        f"the bucket holds no object under cases/{conftest.PUBLISHED_CASE_SLUG}/; the "
        f"published case's media must live in the object store"
    )
    body = flatten(detail.json())
    assert any(key.rsplit("/", 1)[-1] in body or key in body for key in keys), (
        f"the case payload references none of the stored objects {keys}; the page is not "
        f"serving the bytes that are actually in the bucket"
    )
    streamed = anon_client.get(f"/assets/{keys[0]}")
    assert streamed.status_code == 200, (
        f"GET /api/assets/{keys[0]} for a published case returned "
        f"{streamed.status_code}; published media is readable by anybody"
    )
    assert streamed.content, f"GET /api/assets/{keys[0]} returned an empty body"


def test_asset_object_key_carries_digest(author_client, probe_case, store, backend):
    """The object key is derived from the owning case and the digest of the bytes."""
    payload = conftest.image_bytes(probe_case)
    response = conftest.upload_asset(author_client, probe_case, payload)
    assert response.status_code in (200, 201), (
        f"uploading a hero to {probe_case!r} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    key = response.json().get("object_key")
    expected = f"cases/{probe_case}/{conftest.digest_of(payload)}.png"
    assert key == expected, (
        f"the object key is {key!r} but the pinned scheme "
        f"cases/{{case_slug}}/{{sha256_of_bytes}}.{{ext}} requires {expected!r}"
    )
    assert store.exists(key), (
        f"the object {key!r} is not in the bucket; the bytes must live in the object "
        f"store rather than on the application's own disk"
    )
    row = backend.one("asset", object_key=key)
    assert row is not None, f"no asset row carries object_key {key!r}"


def test_duplicate_upload_leaves_one_object(author_client, probe_case, store, backend):
    """Uploading identical bytes twice to one case leaves one object and one row."""
    payload = conftest.image_bytes(f"{probe_case}-duplicate")
    first = conftest.upload_asset(author_client, probe_case, payload)
    assert first.status_code in (200, 201), (
        f"the first upload to {probe_case!r} returned {first.status_code}: "
        f"{first.text[:400]}"
    )
    key = first.json().get("object_key")
    second = conftest.upload_asset(author_client, probe_case, payload)
    assert second.status_code in (200, 201, 409), (
        f"re-uploading identical bytes to {probe_case!r} returned "
        f"{second.status_code}; it must be a no-op or a refusal, never a server error"
    )
    assert backend.count("asset", object_key=key) == 1, (
        f"the asset table holds {backend.count('asset', object_key=key)} rows for "
        f"object_key {key!r}; the digest in the key makes the uniqueness rule the "
        f"deduplication rule"
    )
    stored = [k for k in store.list(f"cases/{probe_case}/") if k == key]
    assert len(stored) == 1, (
        f"the bucket holds {len(stored)} objects at {key!r} after two identical uploads"
    )


def test_concurrent_upload_leaves_one_object(author_client, probe_case, store, backend):
    """Two simultaneous uploads of identical bytes leave one object and one row."""
    payload = conftest.image_bytes(f"{probe_case}-concurrent")
    key = f"cases/{probe_case}/{conftest.digest_of(payload)}.png"
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [
            pool.submit(conftest.upload_asset, author_client, probe_case, payload)
            for _ in range(2)
        ]
        responses = [f.result() for f in futures]
    codes = [r.status_code for r in responses]
    assert all(code < 500 for code in codes), (
        f"two simultaneous uploads of identical bytes returned {codes}; a contended "
        f"upload must not become a server error"
    )
    assert backend.count("asset", object_key=key) == 1, (
        f"the asset table holds {backend.count('asset', object_key=key)} rows for "
        f"{key!r} after two simultaneous identical uploads"
    )
    assert store.exists(key), f"the object {key!r} is missing from the bucket entirely"


def test_concurrent_publish_leaves_one_published_row(author_client, backend):
    """Two simultaneous publishes of one case leave exactly one published row."""
    slug = conftest.unique_slug("probe-publish")
    created = conftest.create_case(author_client, slug)
    assert created.status_code in (200, 201), (
        f"creating {slug!r} returned {created.status_code}: {created.text[:400]}"
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(conftest.publish, author_client, slug) for _ in range(2)]
        responses = [f.result() for f in futures]
    codes = [r.status_code for r in responses]
    assert all(code < 500 for code in codes), (
        f"two simultaneous publishes of {slug!r} returned {codes}; contention must not "
        f"become a server error"
    )
    assert sum(1 for code in codes if code in (200, 201)) >= 1, (
        f"two simultaneous publishes of {slug!r} both failed: {codes}"
    )
    published = backend.count("case_study", slug=slug, state="published")
    assert published == 1, (
        f"{published} published rows carry the slug {slug!r} after two simultaneous "
        f"publishes; exactly one must win"
    )
    row = backend.one("case_study", slug=slug)
    assert row is not None and row.get("published_at") is not None, (
        f"the published case {slug!r} carries no publication time"
    )


def test_unpublish_revokes_media_immediately(author_client, anon_client, store):
    """Moving a record back to draft makes its media unreadable on the next request."""
    slug = conftest.unique_slug("probe-revoke")
    created = conftest.create_case(author_client, slug)
    assert created.status_code in (200, 201), (
        f"creating {slug!r} returned {created.status_code}: {created.text[:400]}"
    )
    payload = conftest.image_bytes(f"{slug}-hero")
    uploaded = conftest.upload_asset(author_client, slug, payload)
    assert uploaded.status_code in (200, 201), (
        f"uploading a hero to {slug!r} returned {uploaded.status_code}: "
        f"{uploaded.text[:400]}"
    )
    key = uploaded.json().get("object_key")
    published = conftest.publish(author_client, slug)
    assert published.status_code in (200, 201), (
        f"publishing {slug!r} returned {published.status_code}: {published.text[:400]}"
    )
    open_read = anon_client.get(f"/assets/{key}")
    assert open_read.status_code == 200, (
        f"a published case's media at {key!r} returned {open_read.status_code} to an "
        f"anonymous visitor"
    )
    reverted = conftest.publish(author_client, slug, state="draft")
    assert reverted.status_code in (200, 201), (
        f"unpublishing {slug!r} returned {reverted.status_code}: {reverted.text[:400]}"
    )
    closed_read = anon_client.get(f"/assets/{key}")
    assert conftest.looks_absent(closed_read), (
        f"after unpublishing {slug!r} the object {key!r} still returned "
        f"{closed_read.status_code}; a link that was legitimate a moment ago must stop "
        f"working on the next request"
    )
    assert store.exists(key), (
        f"unpublishing deleted the object {key!r} from the bucket; the record is hidden, "
        f"not destroyed"
    )


def test_enquiry_is_stored(anon_client, backend):
    """A contact enquiry submitted by a visitor is persisted."""
    email = conftest.unique_email()
    response = anon_client.post(
        "/enquiries",
        json={
            "name": "Probe Visitor",
            "email": email,
            "company": "Probe Company",
            "message": "We have a project and would like to talk about it.",
        },
    )
    assert response.status_code in (200, 201), (
        f"POST /api/enquiries returned {response.status_code}: {response.text[:400]}"
    )
    assert backend.count("enquiry", email=email) == 1, (
        f"the enquiry table holds {backend.count('enquiry', email=email)} rows for "
        f"{email!r} after one submission"
    )


def test_invalid_enquiry_stores_nothing(anon_client, backend):
    """A malformed enquiry is refused as a client error and writes nothing."""
    before = backend.count("enquiry")
    malformed = anon_client.post(
        "/enquiries",
        json={"name": "Probe Visitor", "email": "not-an-address", "company": "Probe",
              "message": "This address cannot be delivered to."},
    )
    incomplete = anon_client.post(
        "/enquiries",
        json={"name": "Probe Visitor", "email": conftest.unique_email()},
    )
    assert 400 <= malformed.status_code < 500, (
        f"a malformed address returned {malformed.status_code} rather than a client "
        f"error: {malformed.text[:400]}"
    )
    assert 400 <= incomplete.status_code < 500, (
        f"an enquiry missing a required field returned {incomplete.status_code} rather "
        f"than a client error: {incomplete.text[:400]}"
    )
    assert "email" in malformed.text.lower(), (
        f"the refusal does not name the offending field: {malformed.text[:400]}"
    )
    conftest.settle()
    assert backend.count("enquiry") == before, (
        f"the enquiry table grew from {before} to {backend.count('enquiry')} after two "
        f"refused submissions; a refused enquiry stores nothing"
    )


def test_subscriber_is_stored(anon_client, backend):
    """A newsletter subscription is persisted with its locale."""
    email = conftest.unique_email()
    response = anon_client.post("/subscribers", json={"email": email, "locale": "en"})
    assert response.status_code in (200, 201), (
        f"POST /api/subscribers returned {response.status_code}: {response.text[:400]}"
    )
    assert backend.count("subscriber", email=email) == 1, (
        f"the subscriber table holds "
        f"{backend.count('subscriber', email=email)} rows for {email!r}"
    )


def test_duplicate_subscriber_leaves_one_row(anon_client, backend):
    """Subscribing one address twice leaves one row and reports success both times."""
    email = conftest.unique_email()
    first = anon_client.post("/subscribers", json={"email": email, "locale": "en"})
    second = anon_client.post("/subscribers", json={"email": email, "locale": "en"})
    assert first.status_code in (200, 201), (
        f"the first subscription for {email!r} returned {first.status_code}: "
        f"{first.text[:400]}"
    )
    assert second.status_code in (200, 201), (
        f"subscribing {email!r} a second time returned {second.status_code}; a visitor "
        f"who subscribes twice has not made a mistake"
    )
    assert backend.count("subscriber", email=email) == 1, (
        f"the subscriber table holds "
        f"{backend.count('subscriber', email=email)} rows for {email!r} after two "
        f"identical subscriptions"
    )


def test_discipline_filter_returns_only_that_discipline(anon_client):
    """Filtering the case list by discipline returns only cases of that discipline."""
    for discipline in conftest.DISCIPLINES:
        response = anon_client.get("/cases", params={"discipline": discipline})
        assert response.status_code == 200, (
            f"GET /api/cases?discipline={discipline} returned {response.status_code}: "
            f"{response.text[:400]}"
        )
        rows = items(response.json())
        offenders = [r.get("slug") for r in rows if r.get("discipline") != discipline]
        assert not offenders, (
            f"filtering to {discipline!r} returned cases of another discipline: "
            f"{offenders}"
        )


def test_empty_discipline_filter_returns_empty_array(anon_client):
    """A filter that matches no published case returns an empty list rather than an error."""
    response = anon_client.get("/cases", params={"discipline": "Strategy", "state": "draft"})
    assert response.status_code in (200, 400, 401, 403), (
        f"an anonymous filtered request returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    unmatched = anon_client.get("/cases", params={"discipline": conftest.unique_token()})
    assert unmatched.status_code == 200, (
        f"filtering to a discipline with no case returned {unmatched.status_code} "
        f"rather than an empty list: {unmatched.text[:400]}"
    )
    assert items(unmatched.json()) == [], (
        f"filtering to a discipline with no case returned "
        f"{unmatched.text[:200]!r} rather than an empty top-level array"
    )


def test_reader_cannot_create_case(reader_client, backend):
    """A reader creating a case is refused at the API and writes nothing."""
    slug = conftest.unique_slug("reader-case")
    response = conftest.create_case(reader_client, slug)
    assert response.status_code in (401, 403, 404), (
        f"a reader creating {slug!r} returned {response.status_code}; an author-only "
        f"mutation must be refused server-side: {response.text[:400]}"
    )
    conftest.settle()
    assert backend.count("case_study", slug=slug) == 0, (
        f"the refused creation still wrote a case_study row for {slug!r}"
    )


def test_reader_cannot_upload_asset(reader_client, backend):
    """A reader uploading media is refused and no asset row appears."""
    payload = conftest.image_bytes("reader-upload")
    key = f"cases/{conftest.PUBLISHED_CASE_SLUG}/{conftest.digest_of(payload)}.png"
    response = conftest.upload_asset(reader_client, conftest.PUBLISHED_CASE_SLUG, payload)
    assert response.status_code in (401, 403, 404), (
        f"a reader uploading to {conftest.PUBLISHED_CASE_SLUG!r} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    conftest.settle()
    assert backend.count("asset", object_key=key) == 0, (
        f"the refused upload still wrote an asset row for {key!r}"
    )


def test_reader_cannot_publish_case(reader_client, backend):
    """A reader publishing the draft case is refused and the state is unchanged."""
    before = backend.one("case_study", slug=conftest.DRAFT_CASE_SLUG)
    assert before is not None, (
        f"the seeded draft case {conftest.DRAFT_CASE_SLUG!r} is missing from the "
        f"case_study table"
    )
    response = conftest.publish(reader_client, conftest.DRAFT_CASE_SLUG)
    assert response.status_code in (401, 403, 404), (
        f"a reader publishing {conftest.DRAFT_CASE_SLUG!r} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    conftest.settle()
    after = backend.one("case_study", slug=conftest.DRAFT_CASE_SLUG)
    assert after.get("state") == before.get("state"), (
        f"the refused publish changed {conftest.DRAFT_CASE_SLUG!r} from "
        f"{before.get('state')!r} to {after.get('state')!r}"
    )


def test_reader_cannot_read_page_views(reader_client, anon_client):
    """The page-view log is refused to a reader and to an anonymous visitor."""
    for label, client in (("reader", reader_client), ("anonymous", anon_client)):
        response = client.get("/page-views")
        assert response.status_code in (401, 403, 404), (
            f"GET /api/page-views as {label} returned {response.status_code}; the log "
            f"belongs to an author alone: {response.text[:400]}"
        )


def test_anonymous_cannot_reach_desk(anon_client, reader_token):
    """The desk is a redirect for a stranger and the not-found page for a reader."""
    api = anon_client.get("/page-views")
    assert api.status_code in (401, 403, 404), (
        f"an unauthenticated call to an author-only endpoint returned {api.status_code}"
    )
    stranger = conftest.raw_page("/desk")
    assert stranger.status_code in (302, 303, 307, 404), (
        f"GET /desk without a session returned {stranger.status_code}; it must redirect "
        f"to the sign-in route or answer as absent"
    )
    reader = conftest.page("/desk", reader_token)
    assert reader.status_code == 404, (
        f"GET /desk as a signed-in reader returned {reader.status_code} rather than the "
        f"not-found page"
    )
    assert conftest.NOT_FOUND_HEADING in reader.text, (
        f"the page a reader receives for /desk is not the studio's own not-found page: "
        f"{reader.text[:300]!r}"
    )


def test_duplicate_slug_is_refused(author_client, backend):
    """A slug already taken is refused as a client error naming the conflict."""
    slug = conftest.unique_slug("probe-conflict")
    first = conftest.create_case(author_client, slug)
    assert first.status_code in (200, 201), (
        f"creating {slug!r} returned {first.status_code}: {first.text[:400]}"
    )
    second = conftest.create_case(author_client, slug)
    assert 400 <= second.status_code < 500, (
        f"creating {slug!r} a second time returned {second.status_code} rather than a "
        f"client error: {second.text[:400]}"
    )
    assert backend.count("case_study", slug=slug) == 1, (
        f"the case_study table holds {backend.count('case_study', slug=slug)} rows for "
        f"{slug!r} after a refused duplicate"
    )


def test_sitemap_lists_published_routes_only():
    """The sitemap carries every published public route and no draft one."""
    response = conftest.page("/sitemap.xml")
    assert response.status_code == 200, (
        f"GET /sitemap.xml returned {response.status_code}: {response.text[:300]}"
    )
    body = response.text
    assert conftest.PUBLISHED_CASE_SLUG in body, (
        f"the sitemap omits the published case {conftest.PUBLISHED_CASE_SLUG!r}"
    )
    assert conftest.DRAFT_CASE_SLUG not in body, (
        f"the sitemap lists the draft case {conftest.DRAFT_CASE_SLUG!r}"
    )
    for route in ("/cases", "/careers", "/news", "/contact"):
        assert route in body, f"the sitemap omits the public route {route!r}"


def test_robots_names_the_sitemap():
    """The robots file names the sitemap address."""
    response = conftest.page("/robots.txt")
    assert response.status_code == 200, (
        f"GET /robots.txt returned {response.status_code}: {response.text[:300]}"
    )
    assert "sitemap" in response.text.lower(), (
        f"/robots.txt does not name the sitemap: {response.text[:300]!r}"
    )


def test_unknown_route_answers_not_found():
    """An unknown address renders the studio's own not-found page and answers as not found."""
    response = conftest.page(f"/{conftest.unique_slug('no-such-route')}")
    assert response.status_code == 404, (
        f"an unknown address returned {response.status_code} rather than not found"
    )
    for needle in (conftest.NOT_FOUND_HEADING, conftest.NOT_FOUND_LINE,
                   conftest.NOT_FOUND_LINK):
        assert needle in response.text, (
            f"the not-found page does not carry {needle!r}: {response.text[:400]!r}"
        )


def test_favicon_is_served():
    """A favicon is served and declared in every public route's document head."""
    icon = conftest.page("/favicon.ico")
    alternate = conftest.page("/favicon.svg")
    assert icon.status_code == 200 or alternate.status_code == 200, (
        f"neither /favicon.ico ({icon.status_code}) nor /favicon.svg "
        f"({alternate.status_code}) is served"
    )
    for route in conftest.PUBLIC_ROUTES:
        head = conftest.page(route)
        assert head.status_code == 200, (
            f"GET {route} returned {head.status_code}: {head.text[:200]}"
        )
        assert "icon" in head.text.lower(), (
            f"the document head of {route} declares no favicon"
        )


def test_public_routes_carry_unique_meta():
    """Every public route carries its own title and its own meta description."""
    seen_titles = {}
    seen_descriptions = {}
    for route in conftest.PUBLIC_ROUTES:
        response = conftest.page(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}: {response.text[:200]}"
        )
        body = response.text
        start = body.lower().find("<title")
        assert start >= 0, f"{route} carries no title element"
        title = body[start:body.lower().find("</title>", start)]
        assert "description" in body.lower(), (
            f"{route} carries no meta description"
        )
        marker = body.lower().find('name="description"')
        assert marker >= 0, f"{route} carries no meta description element"
        description = body[marker:marker + 300]
        assert title not in seen_titles, (
            f"{route} shares its title with {seen_titles.get(title)!r}"
        )
        assert description not in seen_descriptions, (
            f"{route} shares its meta description with "
            f"{seen_descriptions.get(description)!r}"
        )
        seen_titles[title] = route
        seen_descriptions[description] = route


def test_terms_and_privacy_routes_are_served():
    """The terms route and the privacy route are public and carry their own reading."""
    for route in ("/terms", "/privacy"):
        response = conftest.page(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}: {response.text[:300]}"
        )
        assert len(response.text) > 500, (
            f"{route} returned a {len(response.text)}-character document, which is too "
            f"short to be the policy it promises"
        )


def test_locale_prefix_serves_both_languages():
    """Every public route answers under both locale prefixes and under the bare form."""
    for route in ("/", "/cases", "/contact"):
        bare = conftest.page(route)
        english = conftest.page(f"/en{route}".rstrip("/") or "/en")
        spanish = conftest.page(f"/es{route}".rstrip("/") or "/es")
        assert bare.status_code == 200, (
            f"GET {route} returned {bare.status_code}"
        )
        assert english.status_code == 200, (
            f"GET /en{route} returned {english.status_code}; the English prefix must "
            f"answer for every public route"
        )
        assert spanish.status_code == 200, (
            f"GET /es{route} returned {spanish.status_code}; a route with no "
            f"translation still renders rather than answering as missing"
        )


def test_page_view_log_records_route_and_locale(author_client, backend):
    """A page view is recorded with its route and its locale, and an author reads the log."""
    route = "/careers"
    before = backend.count("page_view")
    visit = conftest.page(route)
    assert visit.status_code == 200, f"GET {route} returned {visit.status_code}"
    recorded = conftest.poll_until(lambda: backend.count("page_view") > before)
    assert recorded, (
        f"the page_view table stayed at {before} rows after a visit to {route}"
    )
    response = author_client.get("/page-views")
    assert response.status_code == 200, (
        f"GET /api/page-views as an author returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    rows = items(response.json())
    assert rows, "the page-view log an author reads is empty after a recorded visit"
    assert any("route" in row for row in rows), (
        f"no page-view row carries a route: {rows[:3]}"
    )


def test_posts_list_excludes_drafts(anon_client, author_client):
    """The journal index carries published posts alone, and the draft post answers as absent."""
    public = anon_client.get("/posts")
    assert public.status_code == 200, (
        f"GET /api/posts returned {public.status_code}: {public.text[:400]}"
    )
    slugs = [row.get("slug") for row in items(public.json())]
    assert conftest.PUBLISHED_POST_SLUG in slugs, (
        f"the journal index omits the published post "
        f"{conftest.PUBLISHED_POST_SLUG!r}: {slugs}"
    )
    assert conftest.DRAFT_POST_SLUG not in slugs, (
        f"the journal index lists the draft post {conftest.DRAFT_POST_SLUG!r}: {slugs}"
    )
    hidden = anon_client.get(f"/posts/{conftest.DRAFT_POST_SLUG}")
    assert conftest.looks_absent(hidden), (
        f"GET /api/posts/{conftest.DRAFT_POST_SLUG} returned {hidden.status_code} to an "
        f"anonymous visitor"
    )
    visible = author_client.get(f"/posts/{conftest.DRAFT_POST_SLUG}")
    assert visible.status_code == 200, (
        f"an author cannot read the draft post {conftest.DRAFT_POST_SLUG!r}: "
        f"{visible.status_code}"
    )


def test_roles_list_carries_offices(anon_client):
    """Each open role carries an office drawn from the three the studio keeps."""
    response = anon_client.get("/roles")
    assert response.status_code == 200, (
        f"GET /api/roles returned {response.status_code}: {response.text[:400]}"
    )
    rows = items(response.json())
    assert len(rows) >= 3, f"the careers list carries {len(rows)} open roles, not three"
    for row in rows:
        assert row.get("office") in conftest.OFFICES, (
            f"the role {row.get('slug')!r} carries office {row.get('office')!r}, which "
            f"is outside {conftest.OFFICES}"
        )


def test_config_exposes_offices_and_socials(anon_client):
    """The site configuration carries the locales, the offices and the social set."""
    response = anon_client.get("/config")
    assert response.status_code == 200, (
        f"GET /api/config returned {response.status_code}: {response.text[:400]}"
    )
    body = flatten(response.json())
    for office in conftest.OFFICES:
        assert office in body, f"the configuration omits the office {office!r}: {body[:300]}"
    for network in conftest.SOCIAL_NETWORKS:
        assert network in body, (
            f"the configuration omits the social network {network!r}: {body[:300]}"
        )


def test_seeded_cases_match_the_brief(anon_client, backend):
    """The seven published case studies and the one draft are seeded exactly once each."""
    for slug in conftest.PUBLISHED_CASE_SLUGS:
        assert backend.count("case_study", slug=slug) == 1, (
            f"the case_study table holds "
            f"{backend.count('case_study', slug=slug)} rows for {slug!r}"
        )
        response = anon_client.get(f"/cases/{slug}")
        assert response.status_code == 200, (
            f"GET /api/cases/{slug} returned {response.status_code}: "
            f"{response.text[:300]}"
        )
    assert backend.count("case_study", slug=conftest.DRAFT_CASE_SLUG) == 1, (
        f"the draft case {conftest.DRAFT_CASE_SLUG!r} is not seeded exactly once"
    )
    assert backend.count("case_study", state="published") >= 7, (
        f"only {backend.count('case_study', state='published')} published cases exist; "
        f"seven are seeded"
    )


def test_case_detail_carries_ordered_bands(anon_client):
    """A published case study carries its ordered media bands with captions."""
    response = anon_client.get(f"/cases/{conftest.PUBLISHED_CASE_SLUG}")
    assert response.status_code == 200, (
        f"GET /api/cases/{conftest.PUBLISHED_CASE_SLUG} returned "
        f"{response.status_code}: {response.text[:400]}"
    )
    payload = response.json()
    body = flatten(payload)
    assert "caption" in body.lower() or "band" in body.lower(), (
        f"the case payload carries no media bands: {body[:300]}"
    )
    assert conftest.PUBLISHED_CASE_SLUG in body, (
        f"the case payload does not identify itself as "
        f"{conftest.PUBLISHED_CASE_SLUG!r}: {body[:300]}"
    )


def test_asset_alt_text_is_stored(author_client, probe_case, backend):
    """Alternative text is stored with the asset rather than invented at render time."""
    payload = conftest.image_bytes(f"{probe_case}-alt")
    alt = f"A probe hero image for {probe_case}."
    response = conftest.upload_asset(author_client, probe_case, payload, alt_text=alt)
    assert response.status_code in (200, 201), (
        f"uploading a hero with alternative text returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    key = response.json().get("object_key")
    row = backend.one("asset", object_key=key)
    assert row is not None, f"no asset row carries object_key {key!r}"
    assert row.get("alt_text") == alt, (
        f"the asset row for {key!r} carries alt_text {row.get('alt_text')!r} rather "
        f"than the text supplied at upload"
    )


def test_rate_limit_slows_repeated_enquiries(anon_client, backend):
    """A caller submitting repeatedly from one address is slowed rather than served forever."""
    before = backend.count("enquiry")
    codes = []
    for _ in range(25):
        response = anon_client.post(
            "/enquiries",
            json={
                "name": "Probe Flood",
                "email": conftest.unique_email(),
                "company": "Probe Company",
                "message": "A repeated submission from one source address.",
            },
        )
        codes.append(response.status_code)
    assert all(code < 500 for code in codes), (
        f"repeated enquiries produced a server error: {codes}"
    )
    assert any(code == 429 for code in codes), (
        f"twenty-five enquiries in a row from one address returned {sorted(set(codes))} "
        f"and were never limited; the public forms carry the same protection as the "
        f"credential endpoints"
    )
    accepted = sum(1 for code in codes if code in (200, 201))
    assert backend.count("enquiry") - before == accepted, (
        f"the enquiry table grew by {backend.count('enquiry') - before} while "
        f"{accepted} submissions were accepted"
    )


def test_no_credential_reaches_the_browser():
    """Nothing the browser can fetch carries a credential or a storage key."""
    for route in conftest.PUBLIC_ROUTES:
        response = conftest.page(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}"
        )
        lowered = response.text.lower()
        for needle in conftest.CREDENTIAL_NEEDLES:
            assert needle.lower() not in lowered, (
                f"{route} carries {needle!r} in what the browser downloads"
            )
