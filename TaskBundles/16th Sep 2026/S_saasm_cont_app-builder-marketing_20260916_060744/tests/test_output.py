from __future__ import annotations

import concurrent.futures
import io
import json

from appclient import client as raw_client
from conftest import (
    ATTACHMENT_KEY_PREFIX,
    ATTACHMENT_MAX_BYTES,
    AUTHOR2_EMAIL,
    AUTHOR_EMAIL,
    CLOSED_JOB_SLUG,
    COVER_KEY_PREFIX,
    DENIED,
    DRAFT_ARTICLE_SLUG,
    FEATURED_ARTICLE_SLUG,
    GRANT_LIFETIME_SECONDS,
    OK,
    OPEN_JOB_SLUG,
    PROMPT_MAX_CHARS,
    READER_EMAIL,
    SECOND_ARTICLE_SLUG,
    SUBSCRIBER_EMAIL,
    excerpt,
    unique_email,
    unique_slug,
)


def test_health_endpoint_reports_ready(anon_client):
    r = anon_client.get("/api/health")
    assert r.status_code == 200, (
        f"GET /api/health must return 200 once the app is ready; "
        f"observed {r.status_code}: {excerpt(r)}"
    )


def test_published_articles_listed_newest_first(anon_client):
    r = anon_client.get("/api/articles")
    assert r.status_code == 200, (
        f"GET /api/articles must return 200; observed {r.status_code}: {excerpt(r)}"
    )
    body = r.json()
    assert isinstance(body, list), (
        f"GET /api/articles must return a top-level JSON array; "
        f"observed {type(body).__name__}: {excerpt(r)}"
    )
    slugs = [a.get("slug") for a in body]
    assert DRAFT_ARTICLE_SLUG not in slugs, (
        f"GET /api/articles listed the draft {DRAFT_ARTICLE_SLUG!r}; "
        f"the public list carries published records only. Observed: {slugs}"
    )
    stamps = [a.get("published_at") for a in body if a.get("published_at")]
    assert stamps == sorted(stamps, reverse=True), (
        f"GET /api/articles must order published records newest first; "
        f"observed published_at sequence {stamps}"
    )


def test_draft_article_absent_from_public_list(anon_client, store):
    row = store.article_by_slug(DRAFT_ARTICLE_SLUG)
    assert row is not None, (
        f"the seeded draft article {DRAFT_ARTICLE_SLUG!r} is missing from the "
        f"articles table; the seed did not run"
    )
    assert row.get("status") == "draft", (
        f"{DRAFT_ARTICLE_SLUG!r} must be seeded with status 'draft'; "
        f"observed {row.get('status')!r}"
    )
    r = anon_client.get(f"/api/articles/{DRAFT_ARTICLE_SLUG}")
    assert r.status_code in DENIED, (
        f"GET /api/articles/{DRAFT_ARTICLE_SLUG} from an anonymous session must be "
        f"denied; observed {r.status_code}: {excerpt(r)}"
    )


def test_featured_article_is_unique_across_the_table(store):
    featured = store.articles(featured=True)
    assert len(featured) == 1, (
        f"exactly one article carries featured true; observed {len(featured)}: "
        f"{[a.get('slug') for a in featured]}"
    )
    assert featured[0].get("slug") == FEATURED_ARTICLE_SLUG, (
        f"the seeded featured article must be {FEATURED_ARTICLE_SLUG!r}; "
        f"observed {featured[0].get('slug')!r}"
    )


def test_featuring_a_second_article_clears_the_first(author2_client, store):
    r = author2_client.patch(
        f"/api/articles/{SECOND_ARTICLE_SLUG}", json={"featured": True}
    )
    assert r.status_code in OK, (
        f"PATCH /api/articles/{SECOND_ARTICLE_SLUG} featured=true must succeed for "
        f"its owner; observed {r.status_code}: {excerpt(r)}"
    )
    featured = store.articles(featured=True)
    assert len(featured) == 1, (
        f"featuring a second article must clear the first; observed "
        f"{len(featured)} featured rows: {[a.get('slug') for a in featured]}"
    )
    assert featured[0].get("slug") == SECOND_ARTICLE_SLUG, (
        f"the newly featured article must be {SECOND_ARTICLE_SLUG!r}; "
        f"observed {featured[0].get('slug')!r}"
    )


def test_concurrent_feature_requests_leave_one_featured_row(
    author_client, author2_client, store
):
    def feature(pair):
        cl, slug = pair
        return cl.patch(f"/api/articles/{slug}", json={"featured": True})

    pairs = [(author_client, FEATURED_ARTICLE_SLUG), (author2_client, SECOND_ARTICLE_SLUG)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(feature, pairs))
    codes = [r.status_code for r in results]
    featured = store.articles(featured=True)
    assert len(featured) == 1, (
        f"two simultaneous featuring requests must leave exactly one featured row; "
        f"observed {len(featured)} rows {[a.get('slug') for a in featured]} "
        f"from responses {codes}"
    )


def test_closed_job_absent_from_the_careers_list(anon_client):
    r = anon_client.get("/api/jobs")
    assert r.status_code == 200, (
        f"GET /api/jobs must return 200; observed {r.status_code}: {excerpt(r)}"
    )
    payload = json.dumps(r.json())
    assert CLOSED_JOB_SLUG not in payload, (
        f"GET /api/jobs listed the closed job {CLOSED_JOB_SLUG!r}; a job with open "
        f"false is absent from the list. Body: {excerpt(r)}"
    )
    assert OPEN_JOB_SLUG in payload, (
        f"GET /api/jobs omitted the open job {OPEN_JOB_SLUG!r}; "
        f"observed: {excerpt(r)}"
    )


def test_closed_job_route_still_resolves(anon_client):
    r = anon_client.get(f"/api/jobs/{CLOSED_JOB_SLUG}")
    assert r.status_code == 200, (
        f"GET /api/jobs/{CLOSED_JOB_SLUG} must still resolve for a closed role; "
        f"observed {r.status_code}: {excerpt(r)}"
    )


def test_job_department_grouping_is_computed_on_read(anon_client, store):
    rows = store.jobs(open=True)
    departments = {row.get("department") for row in rows}
    r = anon_client.get("/api/jobs")
    payload = json.dumps(r.json())
    for dept in departments:
        assert dept and dept in payload, (
            f"GET /api/jobs must group open roles by department; the stored "
            f"department {dept!r} appears nowhere in the response: {excerpt(r)}"
        )


def test_press_digest_pagination_is_server_driven(anon_client):
    r = anon_client.get("/api/press", params={"page": 1})
    assert r.status_code == 200, (
        f"GET /api/press?page=1 must return 200; observed {r.status_code}: {excerpt(r)}"
    )
    body = r.json()
    assert isinstance(body, dict), (
        f"GET /api/press must return an object carrying the page and the page count; "
        f"observed {type(body).__name__}: {excerpt(r)}"
    )
    for key in ("items", "page", "pages"):
        assert key in body, (
            f"GET /api/press must carry {key!r} so the client can render first, last "
            f"and neighbouring pages without loading them; observed keys "
            f"{sorted(body)}: {excerpt(r)}"
        )


def test_question_set_served_as_structured_data(anon_client, store):
    r = anon_client.get("/api/questions")
    assert r.status_code == 200, (
        f"GET /api/questions must return 200; observed {r.status_code}: {excerpt(r)}"
    )
    body = r.json()
    assert isinstance(body, list), (
        f"GET /api/questions must return a top-level JSON array; "
        f"observed {type(body).__name__}: {excerpt(r)}"
    )
    seeded = store.qa_entries(status="published")
    assert len(body) >= len(seeded) and len(body) > 0, (
        f"GET /api/questions must serve every published entry; the table holds "
        f"{len(seeded)} and the route returned {len(body)}: {excerpt(r)}"
    )
    keys = [(e.get("group_order"), e.get("order", e.get("position"))) for e in body]
    assert keys == sorted(keys, key=lambda k: (k[0] is None, k)), (
        f"GET /api/questions must order by group then position; observed {keys}"
    )


def test_documentation_page_served_as_plain_text(anon_client):
    index = anon_client.get("/api/docs")
    assert index.status_code == 200, (
        f"a machine-readable index of every documentation page must exist; "
        f"GET /api/docs observed {index.status_code}: {excerpt(index)}"
    )
    body = index.json()
    pages = body if isinstance(body, list) else body.get("pages", [])
    assert pages, (
        f"the documentation index must name at least one page; observed: {excerpt(index)}"
    )
    first = pages[0]
    slug = first.get("slug") if isinstance(first, dict) else first
    page = anon_client.get(f"/api/docs/{slug}.txt")
    assert page.status_code == 200, (
        f"every documentation page must be retrievable as plain text at a path "
        f"derived from its own; GET /api/docs/{slug}.txt observed "
        f"{page.status_code}: {excerpt(page)}"
    )
    assert page.text.strip(), (
        f"the plain-text documentation page for {slug!r} is empty: {excerpt(page)}"
    )


def test_signup_creates_a_reader_account(anon_client, store):
    email = unique_email("signup")
    r = anon_client.post(
        "/api/auth/signup", json={"email": email, "password": "probe-pw-2026"}
    )
    assert r.status_code in OK, (
        f"POST /api/auth/signup must create an account; observed {r.status_code}: "
        f"{excerpt(r)}"
    )
    row = store.user_by_email(email)
    assert row is not None, (
        f"signup returned {r.status_code} but no users row exists for {email!r}"
    )
    assert row.get("role") == "reader", (
        f"open signup creates a reader and no path creates an author; "
        f"{email!r} was created with role {row.get('role')!r}"
    )


def test_subscription_response_reveals_no_membership(anon_client, store):
    known = anon_client.post(
        "/api/site/subscriptions",
        json={"email": SUBSCRIBER_EMAIL, "source": "blog", "locale": "en"},
    )
    fresh_email = unique_email("subscribe")
    fresh = anon_client.post(
        "/api/site/subscriptions",
        json={"email": fresh_email, "source": "blog", "locale": "en"},
    )
    assert known.status_code == fresh.status_code, (
        f"the subscription response must not differ for a known address; "
        f"{SUBSCRIBER_EMAIL!r} observed {known.status_code} and {fresh_email!r} "
        f"observed {fresh.status_code}"
    )
    assert known.text == fresh.text, (
        f"the subscription response body must not differ for a known address; "
        f"known={excerpt(known)!r} fresh={excerpt(fresh)!r}"
    )
    assert store.count_subscriptions(SUBSCRIBER_EMAIL) == 1, (
        f"resubmitting {SUBSCRIBER_EMAIL!r} must leave exactly one row; observed "
        f"{store.count_subscriptions(SUBSCRIBER_EMAIL)}"
    )


def test_article_cover_upload_is_stored_in_the_object_store(
    author_client, objects, store
):
    slug = unique_slug("cover")
    created = author_client.post(
        "/api/articles",
        json={
            "title": "Probe Cover Article",
            "slug": slug,
            "standfirst": "A probe record.",
            "body": "Probe body.",
            "tags": [],
            "status": "draft",
        },
    )
    assert created.status_code in OK, (
        f"POST /api/articles must create a record for its author; observed "
        f"{created.status_code}: {excerpt(created)}"
    )
    png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
        b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    up = author_client.post(
        f"/api/articles/{slug}/cover",
        files={"file": ("cover.png", io.BytesIO(png), "image/png")},
    )
    assert up.status_code in OK, (
        f"POST /api/articles/{slug}/cover must accept the bytes; observed "
        f"{up.status_code}: {excerpt(up)}"
    )
    row = store.article_by_slug(slug)
    assert row is not None, f"the probe article {slug!r} is absent from the articles table"
    key = row.get("cover_key")
    assert key, (
        f"the article row must carry the cover key after an upload; observed "
        f"cover_key={key!r}"
    )
    assert key.startswith(f"{COVER_KEY_PREFIX}{slug}/"), (
        f"a cover object key is covers/{{article_slug}}/{{sha256_of_bytes}}.{{ext}}; "
        f"observed {key!r}"
    )
    assert objects.exists(key), (
        f"the cover bytes must live in the bucket at {key!r}; the object store has "
        f"no object at that key. Keys under the prefix: "
        f"{objects.list(COVER_KEY_PREFIX + slug + '/')}"
    )


def test_cover_bytes_are_not_persisted_in_a_database_column(store):
    row = store.article_by_slug(DRAFT_ARTICLE_SLUG)
    assert row is not None, f"the seeded article {DRAFT_ARTICLE_SLUG!r} is missing"
    for column, value in row.items():
        if not isinstance(value, (bytes, bytearray)):
            continue
        assert len(value) < 512, (
            f"the articles row carries {len(value)} bytes in column {column!r}; "
            f"cover bytes live in the bucket and nowhere else"
        )


def test_attachment_upload_grant_is_presigned_and_short_lived(anon_client):
    r = anon_client.post(
        "/api/site/attachments",
        json={"filename": "inventory.csv", "content_type": "text/csv", "size": 2048},
    )
    assert r.status_code in OK, (
        f"POST /api/site/attachments must issue an upload grant; observed "
        f"{r.status_code}: {excerpt(r)}"
    )
    body = r.json()
    for key in ("attachment_id", "upload_url", "expires_in"):
        assert key in body, (
            f"the attachment grant must carry {key!r}; observed keys {sorted(body)}: "
            f"{excerpt(r)}"
        )
    assert int(body["expires_in"]) == GRANT_LIFETIME_SECONDS, (
        f"the upload grant expires {GRANT_LIFETIME_SECONDS} seconds after it is "
        f"issued; observed expires_in={body['expires_in']!r}"
    )
    url = str(body["upload_url"])
    assert "X-Amz-Signature" in url or "x-amz-signature" in url.lower(), (
        f"the browser writes the attachment straight into the bucket under a "
        f"presigned grant, so upload_url must be a signed object-store URL; "
        f"observed {url!r}"
    )


def test_oversized_attachment_is_refused(anon_client):
    r = anon_client.post(
        "/api/site/attachments",
        json={
            "filename": "huge.csv",
            "content_type": "text/csv",
            "size": ATTACHMENT_MAX_BYTES + 1,
        },
    )
    assert r.status_code in DENIED, (
        f"an attachment over {ATTACHMENT_MAX_BYTES} bytes is refused; "
        f"observed {r.status_code}: {excerpt(r)}"
    )


def test_attachment_type_is_decided_by_content_not_extension(anon_client, objects):
    r = anon_client.post(
        "/api/site/attachments",
        json={
            "filename": "payload.csv",
            "content_type": "application/x-executable",
            "size": 1024,
        },
    )
    assert r.status_code in DENIED, (
        f"a .csv name over an executable content type is rejected as invalid, "
        f"because the type is decided by reading the content; observed "
        f"{r.status_code}: {excerpt(r)}"
    )


def test_build_request_is_durable_and_returns_its_identifier(anon_client, store):
    prompt = "Build an inventory tracker from my warehouse sheet."
    r = anon_client.post(
        "/api/site/build-requests",
        json={
            "prompt": prompt,
            "attachment_id": None,
            "route": "/",
            "variant": "inline",
            "locale": "en",
            "client_id": unique_slug("client"),
        },
    )
    assert r.status_code in OK, (
        f"POST /api/site/build-requests must accept the prompt; observed "
        f"{r.status_code}: {excerpt(r)}"
    )
    body = r.json()
    for key in ("request_id", "next"):
        assert key in body, (
            f"the build-request response carries the request identifier and the next "
            f"step; {key!r} is absent from {sorted(body)}: {excerpt(r)}"
        )
    rows = store.build_requests(request_id=str(body["request_id"]))
    assert len(rows) == 1, (
        f"the request must be durable before the response is sent; "
        f"build_requests holds {len(rows)} rows for request_id "
        f"{body['request_id']!r}"
    )
    assert rows[0].get("prompt") == prompt, (
        f"the stored prompt must be what was submitted; observed "
        f"{rows[0].get('prompt')!r}"
    )


def test_overlong_prompt_is_refused(anon_client):
    r = anon_client.post(
        "/api/site/build-requests",
        json={
            "prompt": "x" * (PROMPT_MAX_CHARS + 1),
            "attachment_id": None,
            "route": "/",
            "variant": "pinned",
            "locale": "en",
            "client_id": unique_slug("client"),
        },
    )
    assert r.status_code in DENIED, (
        f"a prompt longer than {PROMPT_MAX_CHARS} characters is refused; "
        f"observed {r.status_code}: {excerpt(r)}"
    )


def test_reader_denied_every_authoring_endpoint(reader_client, store):
    before = store.count_articles()
    r = reader_client.post(
        "/api/articles",
        json={
            "title": "Reader Should Not Publish",
            "slug": unique_slug("reader"),
            "standfirst": "no",
            "body": "no",
            "tags": [],
            "status": "draft",
        },
    )
    assert r.status_code in DENIED, (
        f"POST /api/articles from a {READER_EMAIL!r} session must be denied by the "
        f"server; observed {r.status_code}: {excerpt(r)}"
    )
    assert store.count_articles() == before, (
        f"a denied authoring request must leave the protected state unchanged; "
        f"the articles table went from {before} to {store.count_articles()} rows"
    )


def test_cross_author_edit_denied_and_row_unchanged(author2_client, store):
    before = store.article_by_slug(DRAFT_ARTICLE_SLUG)
    assert before is not None, f"the seeded article {DRAFT_ARTICLE_SLUG!r} is missing"
    r = author2_client.patch(
        f"/api/articles/{DRAFT_ARTICLE_SLUG}",
        json={"title": "Taken Over", "status": "published"},
    )
    assert r.status_code in DENIED, (
        f"PATCH /api/articles/{DRAFT_ARTICLE_SLUG} from {AUTHOR2_EMAIL!r} must be "
        f"denied: the record belongs to {AUTHOR_EMAIL!r}. Observed "
        f"{r.status_code}: {excerpt(r)}"
    )
    after = store.article_by_slug(DRAFT_ARTICLE_SLUG)
    assert after.get("title") == before.get("title"), (
        f"the denied cross-author edit changed the title from "
        f"{before.get('title')!r} to {after.get('title')!r}"
    )
    assert after.get("status") == before.get("status"), (
        f"the denied cross-author edit changed the status from "
        f"{before.get('status')!r} to {after.get('status')!r}"
    )


def test_draft_article_denied_to_reader_and_other_author(
    reader_client, author2_client, author_client
):
    for label, cl in (("reader", reader_client), ("author2", author2_client)):
        r = cl.get(f"/api/articles/{DRAFT_ARTICLE_SLUG}")
        assert r.status_code in DENIED, (
            f"GET /api/articles/{DRAFT_ARTICLE_SLUG} from the {label} session must "
            f"be denied; observed {r.status_code}: {excerpt(r)}"
        )
    owner = author_client.get(f"/api/articles/{DRAFT_ARTICLE_SLUG}")
    assert owner.status_code == 200, (
        f"GET /api/articles/{DRAFT_ARTICLE_SLUG} must answer its own author "
        f"{AUTHOR_EMAIL!r}; observed {owner.status_code}: {excerpt(owner)}"
    )


def test_missing_draft_and_absent_slug_are_denied_alike(reader_client):
    real = reader_client.get(f"/api/articles/{DRAFT_ARTICLE_SLUG}")
    absent = reader_client.get(f"/api/articles/{unique_slug('nothing')}")
    assert real.status_code == absent.status_code, (
        f"the denial must be identical whether the draft slug exists or not; "
        f"{DRAFT_ARTICLE_SLUG!r} observed {real.status_code} and an absent slug "
        f"observed {absent.status_code}"
    )


def test_draft_cover_denied_to_everyone_but_its_author(
    anon_client, reader_client, author2_client, author_client, store
):
    row = store.article_by_slug(DRAFT_ARTICLE_SLUG)
    assert row is not None, f"the seeded article {DRAFT_ARTICLE_SLUG!r} is missing"
    assert row.get("cover_key"), (
        f"the seeded draft {DRAFT_ARTICLE_SLUG!r} must carry a cover object so the "
        f"protected-read boundary is reachable; observed cover_key="
        f"{row.get('cover_key')!r}"
    )
    for label, cl in (
        ("anonymous", anon_client),
        ("reader", reader_client),
        ("author2", author2_client),
    ):
        r = cl.get(f"/api/covers/{DRAFT_ARTICLE_SLUG}")
        assert r.status_code in DENIED, (
            f"GET /api/covers/{DRAFT_ARTICLE_SLUG} from the {label} session must be "
            f"denied: the article is a draft. Observed {r.status_code}: {excerpt(r)}"
        )
        assert "X-Amz-Signature" not in r.text, (
            f"no presigned read URL is ever issued for a cover; the {label} response "
            f"carries a signature: {excerpt(r)}"
        )
    owner = author_client.get(f"/api/covers/{DRAFT_ARTICLE_SLUG}")
    assert owner.status_code == 200, (
        f"GET /api/covers/{DRAFT_ARTICLE_SLUG} must answer its own author; "
        f"observed {owner.status_code}: {excerpt(owner)}"
    )


def test_published_cover_answers_any_requester(anon_client):
    r = anon_client.get(f"/api/covers/{FEATURED_ARTICLE_SLUG}")
    assert r.status_code == 200, (
        f"a published article's cover answers anyone; GET "
        f"/api/covers/{FEATURED_ARTICLE_SLUG} observed {r.status_code}: {excerpt(r)}"
    )


def test_unauthenticated_studio_request_is_denied(anon_client):
    r = anon_client.get("/api/studio/articles")
    assert r.status_code in DENIED, (
        f"GET /api/studio/articles without a token must be denied; observed "
        f"{r.status_code}: {excerpt(r)}"
    )


def test_reader_cannot_reach_the_studio_collection(reader_client):
    r = reader_client.get("/api/studio/articles")
    assert r.status_code in DENIED, (
        f"GET /api/studio/articles from a {READER_EMAIL!r} session must be refused; "
        f"observed {r.status_code}: {excerpt(r)}"
    )


def test_expired_token_is_rejected_and_record_unchanged(anon_client, store):
    before = store.article_by_slug(DRAFT_ARTICLE_SLUG)
    with raw_client("expired.invalid.token") as cl:
        r = cl.patch(
            f"/api/articles/{DRAFT_ARTICLE_SLUG}", json={"title": "Should Not Land"}
        )
    assert r.status_code in DENIED, (
        f"a mutating call carrying an unusable token must be rejected; observed "
        f"{r.status_code}: {excerpt(r)}"
    )
    after = store.article_by_slug(DRAFT_ARTICLE_SLUG)
    assert after.get("title") == before.get("title"), (
        f"the rejected call changed the title from {before.get('title')!r} to "
        f"{after.get('title')!r}"
    )


def test_seeded_accounts_are_persisted_rows(store):
    for email, role in (
        (AUTHOR_EMAIL, "author"),
        (AUTHOR2_EMAIL, "author"),
        (READER_EMAIL, "reader"),
    ):
        row = store.user_by_email(email)
        assert row is not None, (
            f"the seeded account {email!r} is missing from the users table"
        )
        assert row.get("role") == role, (
            f"{email!r} must be seeded with role {role!r}; observed "
            f"{row.get('role')!r}"
        )
        assert store.count_users(email) == 1, (
            f"seeding must be idempotent: {email!r} occurs "
            f"{store.count_users(email)} times in the users table"
        )


def test_article_slug_is_unique(author_client, store):
    slug = unique_slug("dupe")
    payload = {
        "title": "First Claim",
        "slug": slug,
        "standfirst": "one",
        "body": "one",
        "tags": [],
        "status": "draft",
    }
    first = author_client.post("/api/articles", json=payload)
    assert first.status_code in OK, (
        f"the first POST /api/articles must succeed; observed {first.status_code}: "
        f"{excerpt(first)}"
    )
    second = author_client.post("/api/articles", json={**payload, "title": "Second"})
    assert second.status_code in DENIED, (
        f"a second article claiming the slug {slug!r} must be refused; observed "
        f"{second.status_code}: {excerpt(second)}"
    )
    assert store.count_articles(slug=slug) == 1, (
        f"the slug {slug!r} occurs {store.count_articles(slug=slug)} times in the "
        f"articles table; it is unique"
    )


def test_published_at_is_set_only_on_published_articles(store):
    for row in store.articles():
        if row.get("status") == "published":
            assert row.get("published_at") is not None, (
                f"the published article {row.get('slug')!r} carries a null "
                f"published_at"
            )
        else:
            assert row.get("published_at") is None, (
                f"the {row.get('status')!r} article {row.get('slug')!r} carries "
                f"published_at={row.get('published_at')!r}; it is set exactly when "
                f"the status is published"
            )


def test_press_item_holds_three_to_five_summary_entries(store):
    rows = store.press_items()
    assert rows, "the press_items table is empty; the seed did not run"
    for row in rows:
        points = row.get("summary_points") or []
        if isinstance(points, str):
            points = json.loads(points)
        assert 3 <= len(points) <= 5, (
            f"the press item {row.get('slug')!r} carries {len(points)} summary "
            f"entries; a press item holds 3 to 5"
        )


def test_seed_row_counts_are_stable(store):
    first = store.count_articles(slug=DRAFT_ARTICLE_SLUG)
    second = store.count_articles(slug=DRAFT_ARTICLE_SLUG)
    assert first == second == 1, (
        f"seeding is idempotent, so {DRAFT_ARTICLE_SLUG!r} occurs exactly once; "
        f"observed {first} then {second}"
    )
    assert store.count_subscriptions(SUBSCRIBER_EMAIL) == 1, (
        f"the seeded subscription {SUBSCRIBER_EMAIL!r} occurs "
        f"{store.count_subscriptions(SUBSCRIBER_EMAIL)} times; it is seeded once"
    )


def test_invalid_request_is_a_client_error_not_a_server_error(anon_client):
    r = anon_client.post("/api/site/build-requests", json={"prompt": ""})
    assert 400 <= r.status_code < 500, (
        f"an invalid build request is rejected as a client error, never a server "
        f"error and never a silent success; observed {r.status_code}: {excerpt(r)}"
    )
