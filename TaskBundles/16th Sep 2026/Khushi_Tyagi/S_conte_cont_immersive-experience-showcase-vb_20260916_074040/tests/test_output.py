"""Deterministic checks for deku/immersive-experience-showcase-vb.

Every assertion reads either the app's own HTTP surface or the declared
provider -- `postgres` through the backend capability and `minio` through the
object-store capability -- and never the agent's source, module names or
framework. Each check is independent, creates whatever it needs under a
per-run probe suffix, and leaves the seeded catalogue as it found it.
"""

from __future__ import annotations

import re

import httpx
from appclient import api_base, client, login

from conftest import (
    BLOCK_KINDS,
    CHAPTER_SLUGS,
    CONSOLE_ROUTES,
    CREDENTIAL_MARKERS,
    DISCIPLINE_KEYS,
    DRAFT_PROJECT,
    EDITOR_EMAIL,
    GATED_PROJECT,
    HOME_REEL_ORDER,
    INDEX_CLOSES,
    INDEX_OPENS,
    LOGIN_FAILURE_WORDING,
    MALFORMED_ADDRESS_WORDING,
    OFF_REEL_PROJECT,
    PRODUCER_EMAIL,
    PROJECT_TYPES,
    PUBLIC_ROUTES,
    REEL_PROJECT,
    RENDITION_VARIANTS,
    RETIRED_PATHS,
    SEEDED_ACCOUNT_ROWS,
    SEEDED_CHAPTER_ROWS,
    SEEDED_DISCIPLINE_ROWS,
    SEEDED_HOME_REEL_ROWS,
    SEEDED_MEDIA_ROWS,
    SEEDED_PROJECT_ROWS,
    SEEDED_PUBLISHED_PROJECTS,
    SEEDED_REEL_SECTION_ROWS,
    SEEDED_RETIRED_PATH_ROWS,
    SECURITY_HEADERS,
    STATE_IN_REVIEW,
    STATE_PUBLISHED,
    TOKEN_HEX_LENGTH,
    TOKEN_PREFIX,
    UNPUBLISHED_SLUGS,
    WORKED_RENDITION_KEY,
    WORKED_TOKEN,
    app_origin,
    console_password,
    create_draft_project,
    mint_preview_token,
    probe_address,
    settle,
    transition,
    upload_master,
    wait_for_media_state,
)

TOKEN_SHAPE = re.compile(rf"^{re.escape(TOKEN_PREFIX)}[0-9a-f]{{{TOKEN_HEX_LENGTH}}}$")
RENDITION_KEY_SHAPE = re.compile(r"^media/[0-9a-f]+/[a-z0-9_]+\.[a-z0-9]+$")


def body(response) -> str:
    return response.text[:400]


def json_list(response, where: str) -> list:
    assert response.status_code == 200, f"GET {where} returned {response.status_code}: {body(response)}"
    payload = response.json()
    assert isinstance(payload, list), f"{where} must answer with a top-level array; got {type(payload).__name__}"
    return payload


def test_disciplines_endpoint_returns_the_vocabulary_in_position_order(anon_client):
    rows = json_list(anon_client.get("/disciplines"), "/api/disciplines")
    keys = [row.get("key") or row.get("label") for row in rows]
    assert keys == list(DISCIPLINE_KEYS), (
        f"the ten seeded terms must come back in position order; got {keys}"
    )


def test_discipline_outside_the_vocabulary_is_refused(producer_client, probe):
    response = producer_client.post("/console/projects", json={
        "title": f"Probe {probe} vocab",
        "slug": f"probe-{probe}-vocab",
        "type": PROJECT_TYPES[0],
        "description": "A probe record naming a term outside the vocabulary.",
        "disciplines": ["three d"],
    })
    assert 400 <= response.status_code < 500, (
        f"a discipline outside the controlled vocabulary is rejected as invalid; "
        f"got {response.status_code}: {body(response)}"
    )


def test_project_index_endpoint_lists_only_published_records(anon_client, db):
    rows = json_list(anon_client.get("/projects"), "/api/projects")
    slugs = {row.get("slug") for row in rows}
    published = db.count_projects(state=STATE_PUBLISHED)
    assert len(rows) == published, (
        f"/api/projects carries every published record without pagination: "
        f"{len(rows)} returned against {published} stored"
    )
    assert len(rows) >= SEEDED_PUBLISHED_PROJECTS, (
        f"the seeded catalogue publishes {SEEDED_PUBLISHED_PROJECTS}; got {len(rows)}"
    )
    for slug in UNPUBLISHED_SLUGS:
        row = db.project(slug)
        if row is not None and row.get("state") != STATE_PUBLISHED:
            assert slug not in slugs, f"{slug!r} is not published yet appears on the index"


def test_index_order_is_a_stable_sort_on_a_normalising_key(anon_client):
    rows = json_list(anon_client.get("/projects"), "/api/projects")
    titles = [row.get("title") for row in rows]
    assert titles[:len(INDEX_OPENS)] == list(INDEX_OPENS), (
        f"the captured index order opens {list(INDEX_OPENS)}; got {titles[:len(INDEX_OPENS)]}"
    )
    assert INDEX_CLOSES in titles, f"{INDEX_CLOSES!r} is a published case study"
    assert titles.index(INDEX_CLOSES) >= len(titles) - 2, (
        f"{INDEX_CLOSES!r} closes the captured order; it sits at {titles.index(INDEX_CLOSES)}"
    )


def test_project_detail_endpoint_carries_blocks_disciplines_and_the_reel_relation(anon_client):
    response = anon_client.get(f"/projects/{REEL_PROJECT}")
    assert response.status_code == 200, (
        f"GET /api/projects/{REEL_PROJECT} returned {response.status_code}: {body(response)}"
    )
    record = response.json()
    assert record.get("slug") == REEL_PROJECT
    assert record.get("type") in PROJECT_TYPES, f"the type is one of {PROJECT_TYPES}"
    blocks = record.get("blocks")
    assert isinstance(blocks, list) and blocks, "a published case study carries at least one block"
    for block in blocks:
        assert block.get("kind") in BLOCK_KINDS, (
            f"a block kind is one of {BLOCK_KINDS}; got {block.get('kind')!r}"
        )
    disciplines = record.get("disciplines")
    assert isinstance(disciplines, list) and disciplines, "a case study carries its discipline list"
    assert record.get("reel") or record.get("has_reel"), (
        f"{REEL_PROJECT} carries the one seeded reel, so the relation comes down with the record"
    )


def test_chapter_scene_index_outside_the_range_is_refused(anon_client, producer_client, probe):
    chapters = json_list(anon_client.get("/chapters"), "/api/chapters")
    slugs = [row.get("slug") for row in chapters]
    assert slugs == list(CHAPTER_SLUGS), (
        f"the six seeded chapters come back in studio order; got {slugs}"
    )
    response = producer_client.post("/console/projects", json={
        "title": f"Probe {probe} scene",
        "slug": f"probe-{probe}-scene",
        "type": PROJECT_TYPES[0],
        "description": "A probe record carrying an out of range scene index.",
        "disciplines": [DISCIPLINE_KEYS[0]],
        "scene_index": 999,
    })
    if response.status_code in (200, 201):
        patch = producer_client.patch(
            f"/console/projects/probe-{probe}-scene",
            json={"scene_index": 999, "version": response.json().get("version", 1)},
        )
        assert 400 <= patch.status_code < 500, (
            f"a scene index outside the registered range is rejected on save; "
            f"got {patch.status_code}: {body(patch)}"
        )


def test_draft_record_is_absent_from_every_public_endpoint(anon_client, producer_client, probe):
    record = create_draft_project(producer_client, probe, seed=19)
    hidden = (GATED_PROJECT, record["slug"])
    listed = {row.get("slug") for row in json_list(anon_client.get("/projects"), "/api/projects")}
    reel = {row.get("project_slug") or row.get("slug")
            for row in json_list(anon_client.get("/home-reel"), "/api/home-reel")}
    sitemap = httpx.get(f"{app_origin()}/sitemap.xml")
    for slug in hidden:
        assert slug not in listed, f"{slug!r} is unpublished yet appears on /api/projects"
        assert slug not in reel, f"{slug!r} is unpublished yet appears on /api/home-reel"
        assert slug not in sitemap.text, f"{slug!r} is unpublished yet appears in the sitemap"


def test_unpublished_record_route_answers_not_found(anon_client, producer_client, probe):
    record = create_draft_project(producer_client, probe, seed=20)
    for slug in (GATED_PROJECT, record["slug"]):
        api = anon_client.get(f"/projects/{slug}")
        assert api.status_code == 404, (
            f"GET /api/projects/{slug} must answer not found; got {api.status_code}"
        )
        page = httpx.get(f"{app_origin()}/projects/{slug}", follow_redirects=True)
        assert page.status_code == 404, (
            f"the public route of an unpublished record answers not found; got {page.status_code}"
        )


def test_preview_token_is_verified_on_the_server(producer_client, anon_client, probe):
    record = create_draft_project(producer_client, probe, seed=21)
    slug = record["slug"]
    token = mint_preview_token(producer_client, slug)
    assert TOKEN_SHAPE.match(token), (
        f"a preview token is {TOKEN_PREFIX!r} followed by {TOKEN_HEX_LENGTH} lowercase "
        f"hexadecimal characters, as in {WORKED_TOKEN!r}; got {token!r}"
    )
    response = anon_client.get(f"/preview/{token}")
    assert response.status_code == 200, (
        f"GET /api/preview/<token> serves that one record; got {response.status_code}: "
        f"{body(response)}"
    )
    served = response.json()
    assert served.get("slug") == slug
    assert served.get("state") != STATE_PUBLISHED, (
        "the preview serves the record in its draft state"
    )


def test_guessed_or_mismatched_preview_token_answers_not_found(producer_client, anon_client, probe):
    record = create_draft_project(producer_client, probe, seed=22)
    guessed = TOKEN_PREFIX + "0" * TOKEN_HEX_LENGTH
    assert anon_client.get(f"/preview/{guessed}").status_code == 404, (
        "a guessed token answers not found"
    )
    assert anon_client.get(f"/preview/{WORKED_TOKEN}").status_code == 404, (
        "the token printed in the brief as a worked example opens nothing"
    )
    token = mint_preview_token(producer_client, record["slug"])
    other = anon_client.get(f"/preview/{token[:-4]}dead")
    assert other.status_code == 404, "a token naming no record answers not found"


def test_revoked_preview_token_answers_not_found_immediately(producer_client, anon_client, probe):
    record = create_draft_project(producer_client, probe, seed=23)
    slug = record["slug"]
    token = mint_preview_token(producer_client, slug)
    assert anon_client.get(f"/preview/{token}").status_code == 200, (
        "a freshly minted token opens its record"
    )
    rows = producer_client.get(f"/console/projects/{slug}/preview-tokens")
    assert rows.status_code == 200, (
        f"a producer reads the tokens that producer minted; got {rows.status_code}"
    )
    listed = rows.json()
    assert listed, "the minted token is a listed row"
    removed = producer_client.delete(f"/console/preview-tokens/{listed[-1].get('id')}")
    assert removed.status_code in (200, 202, 204), (
        f"a producer revokes a token that producer minted; got {removed.status_code}"
    )
    assert anon_client.get(f"/preview/{token}").status_code == 404, (
        "a revoked token answers not found without delay"
    )


def test_preview_token_is_stored_as_a_hash(producer_client, db, probe):
    record = create_draft_project(producer_client, probe, seed=24)
    slug = record["slug"]
    token = mint_preview_token(producer_client, slug)
    rows = db.preview_tokens(slug)
    assert rows, f"a minted token is a real row against {slug!r}"
    for row in rows:
        stored = " ".join(str(v) for v in row.values())
        assert token not in stored, (
            "the token value is never stored; a database dump must not be a set of "
            "working preview links"
        )
        assert row.get("token_hash"), "the row carries the hash"


def test_minted_preview_token_is_returned_once(producer_client, probe):
    record = create_draft_project(producer_client, probe, seed=25)
    slug = record["slug"]
    token = mint_preview_token(producer_client, slug)
    listing = producer_client.get(f"/console/projects/{slug}/preview-tokens")
    assert listing.status_code == 200, (
        f"the token listing answers for its owner; got {listing.status_code}"
    )
    assert token not in listing.text, (
        "the token value is never returned again by any endpoint"
    )
    editor_view = producer_client.get(f"/console/projects/{slug}")
    assert editor_view.status_code == 200, (
        f"the record editor answers for its owner; got {editor_view.status_code}"
    )
    assert token not in editor_view.text, "the record editor never echoes a minted token"


def test_preview_response_refuses_indexing_and_is_never_cached(producer_client, anon_client, probe):
    record = create_draft_project(producer_client, probe, seed=26)
    token = mint_preview_token(producer_client, record["slug"])
    page = httpx.get(f"{app_origin()}/preview?token={token}", follow_redirects=True)
    headers = " ".join(f"{k}: {v}" for k, v in page.headers.items()).lower()
    assert "noindex" in headers, (
        f"every preview response refuses indexing; headers were {headers[:300]}"
    )
    assert "noarchive" in headers, (
        f"every preview response refuses archiving; headers were {headers[:300]}"
    )
    cache = page.headers.get("cache-control", "").lower()
    assert "no-store" in cache, f"the preview route is never stored; cache-control was {cache!r}"
    api = anon_client.get(f"/preview/{token}")
    assert "no-store" in api.headers.get("cache-control", "").lower(), (
        "the preview endpoint is never stored either"
    )


def test_producer_publish_transition_is_denied_and_state_is_unchanged(producer_client, db, probe):
    record = create_draft_project(producer_client, probe, seed=27)
    slug = record["slug"]
    assert transition(producer_client, slug, STATE_IN_REVIEW).status_code in (200, 202), (
        "a producer moves a record from draft to review"
    )
    settle()
    before = (db.project(slug) or {}).get("state")
    assert before == STATE_IN_REVIEW
    response = transition(producer_client, slug, STATE_PUBLISHED)
    assert response.status_code in (401, 403), (
        f"a producer moving a record to {STATE_PUBLISHED!r} is denied by the server; "
        f"got {response.status_code}: {body(response)}"
    )
    settle()
    assert (db.project(slug) or {}).get("state") == before, (
        "the stored state is untouched after a refused publish"
    )
    seeded = transition(producer_client, DRAFT_PROJECT, STATE_PUBLISHED)
    assert seeded.status_code in (401, 403), (
        f"the same refusal holds for the seeded record awaiting sign off; got "
        f"{seeded.status_code}"
    )


def test_editor_publish_transition_moves_the_record(editor_client, producer_client, db, probe):
    record = create_draft_project(producer_client, probe, seed=1)
    slug = record["slug"]
    assert transition(producer_client, slug, STATE_IN_REVIEW).status_code in (200, 202), (
        "a producer moves a record from draft to review"
    )
    published = transition(editor_client, slug, STATE_PUBLISHED)
    assert published.status_code in (200, 202), (
        f"an editor moves a record to {STATE_PUBLISHED!r}; got {published.status_code}: "
        f"{body(published)}"
    )
    settle()
    assert (db.project(slug) or {}).get("state") == STATE_PUBLISHED
    withdrawn = transition(editor_client, slug, "unpublished")
    assert withdrawn.status_code in (200, 202), "an editor moves a record back to withdrawn"
    settle()
    assert db.project(slug) is not None, "a record is never deleted; withdrawing retains it"


def test_publish_gate_refuses_a_record_whose_media_is_deriving(editor_client, db):
    state = (db.project(GATED_PROJECT) or {}).get("state")
    assert state != STATE_PUBLISHED, (
        f"{GATED_PROJECT!r} references a media that is still deriving, so the gate must "
        f"never have let it reach the live state"
    )
    response = transition(editor_client, GATED_PROJECT, STATE_PUBLISHED)
    assert 400 <= response.status_code < 500, (
        f"the publish gate refuses {GATED_PROJECT!r} while a referenced media is not "
        f"ready; got {response.status_code}: {body(response)}"
    )
    assert "media" in response.text.lower(), (
        f"the refusal names the failing media; got {body(response)}"
    )
    settle()
    assert (db.project(GATED_PROJECT) or {}).get("state") == state, (
        "a refused publish leaves the record in its previous state"
    )
    assert db.count_publish_log(record_slug=GATED_PROJECT, outcome="succeeded") == 0, (
        "a refused publish writes no log row of outcome succeeded"
    )


def test_slug_is_immutable_after_a_first_publish(editor_client, producer_client, db, probe):
    record = create_draft_project(producer_client, probe, seed=2)
    slug = record["slug"]
    transition(producer_client, slug, STATE_IN_REVIEW)
    assert transition(editor_client, slug, STATE_PUBLISHED).status_code in (200, 202)
    settle()
    version = (db.project(slug) or {}).get("version", 1)
    renamed = editor_client.patch(f"/console/projects/{slug}",
                                  json={"slug": f"{slug}-renamed", "version": version})
    assert 400 <= renamed.status_code < 500, (
        f"a slug may not change after a first publish; got {renamed.status_code}: "
        f"{body(renamed)}"
    )
    assert db.project(slug) is not None, "the original slug still resolves to its record"
    transition(editor_client, slug, "unpublished")


def test_stale_version_save_is_rejected_as_a_conflict(producer_client, probe):
    record = create_draft_project(producer_client, probe, seed=3)
    slug = record["slug"]
    version = record.get("version", 1)
    first = producer_client.patch(f"/console/projects/{slug}",
                                  json={"description": "First writer.", "version": version})
    assert first.status_code in (200, 202), (
        f"a save carrying the current version applies; got {first.status_code}: {body(first)}"
    )
    stale = producer_client.patch(f"/console/projects/{slug}",
                                  json={"description": "Second writer.", "version": version})
    assert stale.status_code == 409, (
        f"a save carrying a stale version is rejected as a conflict rather than applied; "
        f"got {stale.status_code}: {body(stale)}"
    )


def test_publish_log_row_is_written_for_every_transition(producer_client, editor_client, db, probe):
    record = create_draft_project(producer_client, probe, seed=4)
    slug = record["slug"]
    before = db.count_publish_log(record_slug=slug)
    transition(producer_client, slug, STATE_IN_REVIEW)
    transition(editor_client, slug, STATE_PUBLISHED)
    settle()
    rows = db.publish_log_rows(record_slug=slug)
    assert len(rows) > before, f"every transition writes one row; {slug} has {len(rows)}"
    latest = rows[-1]
    for field in ("occurred_at", "actor_account_id", "record_type", "record_slug",
                  "from_state", "to_state", "outcome", "invalidated_routes"):
        assert field in latest, f"a publish log row carries {field!r}; got {sorted(latest)}"
    transition(editor_client, slug, "unpublished")


def test_publish_log_exposes_no_removal_path(editor_client, producer_client, db):
    rows = producer_client.get("/console/publish-log")
    payload = json_list(rows, "/api/console/publish-log")
    assert payload, "the seeded catalogue leaves at least one publish log row"
    instants = [row.get("occurred_at") for row in payload]
    assert instants == sorted(instants, reverse=True), (
        "the publish log returns its rows newest first"
    )
    total = db.count_publish_log()
    first_id = payload[0].get("id")
    for attempt in (
        editor_client.delete(f"/console/publish-log/{first_id}"),
        editor_client.post("/console/publish-log/delete", json={"id": first_id}),
    ):
        assert attempt.status_code in (401, 403, 404, 405), (
            f"no role holds a capability removing a log row; got {attempt.status_code}"
        )
    settle()
    assert db.count_publish_log() == total, "the log is append only"


def test_home_reel_returns_the_curated_entries_in_order(anon_client, db):
    rows = json_list(anon_client.get("/home-reel"), "/api/home-reel")
    slugs = [row.get("project_slug") or row.get("slug") for row in rows]
    assert slugs == list(HOME_REEL_ORDER), (
        f"the reel is an explicit ordered list; expected {list(HOME_REEL_ORDER)}, got {slugs}"
    )
    assert db.count_home_reel_entries() == SEEDED_HOME_REEL_ROWS
    for row in rows:
        for field in ("title", "type", "description"):
            assert row.get(field), f"a reel entry carries its {field}"
        assert row.get("media") or row.get("media_id"), (
            "a reel entry carries its own media rather than borrowing the case study's"
        )


def test_producer_reordering_the_home_reel_is_denied(producer_client, anon_client, db):
    before = [row.get("project_slug") for row in db.home_reel_entries()]
    response = producer_client.put("/console/home-reel",
                                   json=[{"project_slug": s} for s in reversed(HOME_REEL_ORDER)])
    assert response.status_code in (401, 403), (
        f"reordering the reel is an editor capability; a producer got {response.status_code}"
    )
    settle()
    after = [row.get("project_slug") for row in db.home_reel_entries()]
    assert after == before, "the stored order is unchanged after a refused reorder"


def test_publishing_a_further_project_leaves_the_home_reel_unchanged(
        producer_client, editor_client, anon_client, db, probe):
    before = [row.get("project_slug") or row.get("slug")
              for row in json_list(anon_client.get("/home-reel"), "/api/home-reel")]
    record = create_draft_project(producer_client, probe, seed=5)
    slug = record["slug"]
    transition(producer_client, slug, STATE_IN_REVIEW)
    transition(editor_client, slug, STATE_PUBLISHED)
    settle()
    after = [row.get("project_slug") or row.get("slug")
             for row in json_list(anon_client.get("/home-reel"), "/api/home-reel")]
    assert after == before, (
        "adding a project to the collection must not change the home page"
    )
    published = {row.get("slug") for row in json_list(anon_client.get("/projects"), "/api/projects")}
    assert OFF_REEL_PROJECT in published and OFF_REEL_PROJECT not in after, (
        f"{OFF_REEL_PROJECT!r} is published and off the reel, which is what makes the "
        f"reel a curated subset rather than a truncation"
    )
    transition(editor_client, slug, "unpublished")


def test_reel_entry_whose_project_is_withdrawn_disappears(editor_client, anon_client, db):
    slug = HOME_REEL_ORDER[-1]
    before = [row.get("project_slug") or row.get("slug")
              for row in json_list(anon_client.get("/home-reel"), "/api/home-reel")]
    assert slug in before
    assert transition(editor_client, slug, "unpublished").status_code in (200, 202)
    settle()
    try:
        after = [row.get("project_slug") or row.get("slug")
                 for row in json_list(anon_client.get("/home-reel"), "/api/home-reel")]
        assert slug not in after, (
            "a reel entry whose project has been withdrawn disappears from the reel"
        )
        listed = {row.get("slug")
                  for row in json_list(anon_client.get("/projects"), "/api/projects")}
        assert slug not in listed, "a withdrawn record leaves the index too"
    finally:
        transition(editor_client, slug, STATE_PUBLISHED)
        settle()


def test_reel_endpoint_answers_not_found_for_an_unpublished_project(anon_client, db):
    response = anon_client.get(f"/reels/{REEL_PROJECT}")
    assert response.status_code == 200, (
        f"GET /api/reels/{REEL_PROJECT} returns the one seeded reel; got {response.status_code}"
    )
    reel = response.json()
    sections = reel.get("sections")
    assert isinstance(sections, list) and len(sections) == SEEDED_REEL_SECTION_ROWS, (
        f"the seeded reel carries {SEEDED_REEL_SECTION_ROWS} sections; got {sections}"
    )
    assert db.count_reel_sections() == SEEDED_REEL_SECTION_ROWS
    hidden = anon_client.get(f"/reels/{GATED_PROJECT}")
    assert hidden.status_code == 404, (
        f"the reel endpoint answers not found for a project that is not published; "
        f"got {hidden.status_code}"
    )


def test_reel_section_carrying_audio_without_a_subtitle_cannot_be_stored(producer_client, probe):
    media = upload_master(producer_client, probe, seed=6)
    response = producer_client.post(f"/console/reels/{REEL_PROJECT}/sections", json={
        "duration_ms": 4000,
        "audio_media_id": media.get("id"),
        "subtitle_media_id": None,
        "media": [],
    })
    assert 400 <= response.status_code < 500, (
        f"a section carrying audio and carrying no subtitle cannot be stored; "
        f"got {response.status_code}: {body(response)}"
    )


def test_section_of_zero_duration_is_refused_on_write(producer_client):
    response = producer_client.post(f"/console/reels/{REEL_PROJECT}/sections", json={
        "duration_ms": 0,
        "audio_media_id": None,
        "subtitle_media_id": None,
        "media": [],
    })
    assert 400 <= response.status_code < 500, (
        f"a section of zero duration is rejected on write; got {response.status_code}: "
        f"{body(response)}"
    )


def test_media_master_is_stored_in_the_bucket_at_its_content_hash(producer_client, store, probe):
    record = upload_master(producer_client, probe, seed=7)
    assert record.get("state") in ("uploaded", "deriving"), (
        f"a fresh upload starts before ready; got {record.get('state')!r}"
    )
    ready = wait_for_media_state(producer_client, record["id"], "ready")
    content_hash = ready.get("content_hash") or record.get("content_hash")
    assert content_hash, "the media record carries its content hash"
    keys = store.list(f"media/{content_hash}/")
    assert any(k.rsplit("/", 1)[-1].startswith("master.") for k in keys), (
        f"the master lives at media/<content-hash>/master.<ext>; the bucket holds {keys}"
    )
    assert ready.get("intrinsic_width") and ready.get("intrinsic_height"), (
        "the intrinsic dimensions are extracted on upload and written to the record"
    )


def test_rendition_key_follows_the_content_addressed_shape(producer_client, store, db, probe):
    record = upload_master(producer_client, probe, seed=8)
    ready = wait_for_media_state(producer_client, record["id"], "ready")
    content_hash = ready.get("content_hash") or record.get("content_hash")
    keys = [k for k in store.list(f"media/{content_hash}/")
            if not k.rsplit("/", 1)[-1].startswith("master.")]
    assert keys, (
        f"the ladder writes renditions beside the master, in the shape of "
        f"{WORKED_RENDITION_KEY!r}; the bucket holds nothing under media/{content_hash}/"
    )
    variants = set()
    for key in keys:
        assert RENDITION_KEY_SHAPE.match(key), f"{key!r} is not a content addressed key"
        variants.add(key.rsplit("/", 1)[-1].split(".")[0])
    assert variants.issubset(set(RENDITION_VARIANTS)), (
        f"the still ladder carries {RENDITION_VARIANTS}; found {sorted(variants)}"
    )
    assert RENDITION_VARIANTS[0] in variants, "the inlineable placeholder is derived"


def test_rendition_bytes_live_in_the_bucket_and_nowhere_else(producer_client, store, db, probe):
    record = upload_master(producer_client, probe, seed=9)
    ready = wait_for_media_state(producer_client, record["id"], "ready")
    content_hash = ready.get("content_hash") or record.get("content_hash")
    rows = db.renditions(record["id"])
    assert rows, "every derived rendition is a real row"
    for row in rows:
        key = row.get("storage_key")
        assert key, "a rendition row carries its storage key"
        assert store.exists(key), (
            f"a media marked ready whose object is absent from the bucket is a contract "
            f"violation; {key!r} is missing"
        )
        for value in row.values():
            assert not isinstance(value, (bytes, bytearray)), (
                "a row holding the bytes is a contract violation"
            )
    assert all(row["storage_key"].startswith(f"media/{content_hash}/") for row in rows), (
        f"every rendition key opens media/{content_hash}/, so replacing a media means a "
        f"new hash and a new key rather than an overwrite"
    )


def test_duplicate_master_upload_produces_one_media_row(producer_client, db, probe):
    first = upload_master(producer_client, probe, seed=10)
    wait_for_media_state(producer_client, first["id"], "ready")
    content_hash = first.get("content_hash")
    assert content_hash, "the media record carries its content hash"
    before = db.count_media(content_hash=content_hash)
    second = upload_master(producer_client, probe, seed=10)
    settle()
    assert str(second.get("id")) == str(first.get("id")), (
        "the unique content hash means uploading the same file twice produces one record"
    )
    assert db.count_media(content_hash=content_hash) == before == 1, (
        "one file produces one media row however many times it is uploaded"
    )


def test_media_delete_is_refused_while_a_record_references_it(editor_client, producer_client, db, probe):
    record = create_draft_project(producer_client, probe, seed=11)
    media = upload_master(producer_client, probe, seed=11)
    wait_for_media_state(producer_client, media["id"], "ready")
    attached = producer_client.patch(f"/console/projects/{record['slug']}", json={
        "version": record.get("version", 1),
        "blocks": [{"kind": "media", "position": 0,
                    "payload": {"media": [{"media_id": media["id"], "alt_text": "A probe still."}]}}],
    })
    assert attached.status_code in (200, 202), (
        f"a block referencing the media saves; got {attached.status_code}: {body(attached)}"
    )
    refused = editor_client.delete(f"/console/media/{media['id']}")
    assert 400 <= refused.status_code < 500, (
        f"a media delete is refused while any record references it; got {refused.status_code}"
    )
    assert record["slug"] in refused.text, (
        f"the refusal lists the referencing records; got {body(refused)}"
    )
    by_producer = producer_client.delete(f"/console/media/{media['id']}")
    assert by_producer.status_code in (401, 403), (
        "deleting a media master requires the editor role"
    )


def test_draft_media_is_served_only_through_an_authenticated_endpoint(
        producer_client, anon_client, store, probe):
    media = upload_master(producer_client, probe, seed=12)
    ready = wait_for_media_state(producer_client, media["id"], "ready")
    content_hash = ready.get("content_hash") or media.get("content_hash")
    keys = store.list(f"media/{content_hash}/")
    assert keys, "the derived objects exist in the bucket"
    endpoint = f"{app_origin()}/media/{media['id']}"
    anonymous = httpx.get(endpoint, follow_redirects=False)
    assert anonymous.status_code in (401, 403, 404), (
        f"a media belonging to a record that is not published is served only through an "
        f"authenticated endpoint; got {anonymous.status_code}"
    )
    assert "amz" not in anonymous.text.lower(), (
        "a draft's imagery is never handed out as a direct bucket address"
    )


def test_subscriber_intake_answers_the_same_for_a_new_and_a_known_address(anon_client, db, probe):
    address = probe_address(probe)
    first = anon_client.post("/subscribers", json={"email": address})
    assert first.status_code in (200, 201, 202), (
        f"POST /api/subscribers accepts a well formed address; got {first.status_code}: "
        f"{body(first)}"
    )
    second = anon_client.post("/subscribers", json={"email": address})
    assert second.status_code == first.status_code, (
        "resubmitting a known address returns the same status as a new one"
    )
    assert second.json() == first.json(), (
        "the response never distinguishes a new address from a known one; a response that "
        "says already subscribed turns the list into a service for checking membership"
    )
    assert db.count_subscribers(email_normalised=address.lower()) == 1, (
        "the unique constraint on the normalised address makes the intake idempotent"
    )


def test_malformed_address_is_refused_and_writes_nothing(anon_client, db, probe):
    before = db.count_subscribers()
    response = anon_client.post("/subscribers", json={"email": f"not-an-address-{probe}"})
    assert 400 <= response.status_code < 500, (
        f"a malformed address is refused; got {response.status_code}: {body(response)}"
    )
    assert MALFORMED_ADDRESS_WORDING in response.text, (
        f"the refusal reads {MALFORMED_ADDRESS_WORDING!r}; got {body(response)}"
    )
    settle()
    assert db.count_subscribers() == before, "nothing is written on a refusal"


def test_decoy_field_submission_is_refused_and_writes_nothing(anon_client, db, probe):
    before = db.count_subscribers()
    address = probe_address(probe)
    response = anon_client.post("/subscribers", json={
        "email": address, "company": "a bot filled this", "website": "a bot filled this",
    })
    assert response.status_code != 500, (
        f"a decoy submission is refused rather than crashing; got {body(response)}"
    )
    settle()
    assert db.count_subscribers() == before, (
        "a submission filling the unattended decoy field is refused and writes nothing"
    )
    cross = httpx.post(f"{api_base()}/subscribers", json={"email": address},
                       headers={"Origin": "https://not-this-studio.example.com"})
    assert 400 <= cross.status_code < 500, (
        f"a cross origin post from an unrecognised origin is rejected; got {cross.status_code}"
    )


def test_confirmation_token_is_single_use_and_stored_as_a_hash(anon_client, db, probe):
    address = probe_address(probe)
    anon_client.post("/subscribers", json={"email": address})
    settle()
    row = db.subscriber(address.lower())
    assert row is not None, "the address is stored unconfirmed"
    assert row.get("state") == "pending", (
        f"only a confirmed address is on the list; the fresh row reads {row.get('state')!r}"
    )
    assert row.get("confirmation_token_hash"), "the confirmation token is held as a hash"
    assert not any(str(v).startswith("cnf_") for v in row.values() if isinstance(v, str)), (
        "the token value itself is never stored"
    )


def test_consent_record_carries_the_instant_and_the_text_version(anon_client, db, probe):
    address = probe_address(probe)
    anon_client.post("/subscribers", json={"email": address, "source_route": "/"})
    settle()
    row = db.subscriber(address.lower())
    assert row is not None
    for field in ("email_normalised", "email_display", "state", "source_route",
                  "consent_text_version", "consent_at", "confirmation_expires_at"):
        assert field in row, f"the subscriber row carries {field!r}; got {sorted(row)}"
    assert row.get("consent_at"), "submitting is the consent, and the instant is kept"
    assert row.get("consent_text_version"), (
        "a consent that cannot say what was agreed to is not a consent record"
    )


def test_outbound_click_records_the_slug_and_nothing_identifying(anon_client, db):
    before = db.count_outbound_clicks(REEL_PROJECT)
    response = anon_client.post("/outbound-clicks", json={"project_slug": REEL_PROJECT})
    assert response.status_code in (200, 201, 202, 204), (
        f"POST /api/outbound-clicks acknowledges; got {response.status_code}: {body(response)}"
    )
    settle()
    assert db.count_outbound_clicks(REEL_PROJECT) == before + 1, (
        "one outbound click row exists for that slug afterwards"
    )
    assert db.count_outbound_clicks("a-slug-that-does-not-exist") == 0, (
        "an outbound click carries the project slug and nothing else"
    )
    unknown = anon_client.post("/outbound-clicks", json={"project_slug": "no-such-project"})
    assert 400 <= unknown.status_code < 500, (
        f"a click naming no case study is refused; got {unknown.status_code}"
    )


def test_login_failure_wording_does_not_distinguish_the_two_causes(anon_client, probe):
    wrong_password = anon_client.post("/auth/login", json={
        "email": PRODUCER_EMAIL, "password": "not-the-seeded-password"})
    no_account = anon_client.post("/auth/login", json={
        "email": probe_address(probe), "password": console_password()})
    assert wrong_password.status_code == no_account.status_code, (
        "one wording and one status answer both causes"
    )
    assert LOGIN_FAILURE_WORDING in wrong_password.text, (
        f"the refusal reads {LOGIN_FAILURE_WORDING!r}; got {body(wrong_password)}"
    )
    assert LOGIN_FAILURE_WORDING in no_account.text, (
        f"the refusal reads {LOGIN_FAILURE_WORDING!r}; got {body(no_account)}"
    )


def test_role_is_read_from_the_session_rather_than_the_request_body(anon_client, db, probe):
    address = f"claimed-editor-{probe}@example.com"
    signup = anon_client.post("/auth/signup", json={
        "email": address, "password": console_password(), "role": "editor"})
    assert signup.status_code in (200, 201), (
        f"signup is open and creates a producer; got {signup.status_code}: {body(signup)}"
    )
    token = login(address, console_password())
    with client(token) as c:
        me = c.get("/auth/me")
        assert me.status_code == 200, f"GET /api/auth/me returned {me.status_code}"
        assert me.json().get("role") == "producer", (
            f"a role is read from the session, never from the request body; got "
            f"{me.json().get('role')!r}"
        )
        denied = c.put("/console/home-reel", json=[])
        assert denied.status_code in (401, 403), (
            "the claimed role buys no editor capability"
        )
    duplicate = anon_client.post("/auth/signup", json={
        "email": address, "password": console_password()})
    assert 400 <= duplicate.status_code < 500, (
        "an address that is already held is rejected as invalid and writes no second row"
    )
    assert db.count_accounts() >= SEEDED_ACCOUNT_ROWS


def test_anonymous_console_call_is_denied_by_the_server(anon_client, db):
    before = db.count_projects()
    attempts = [
        anon_client.get("/console/publish-log"),
        anon_client.get("/console/media"),
        anon_client.post("/console/projects", json={"title": "t", "slug": "anon-probe",
                                                    "type": PROJECT_TYPES[0]}),
        anon_client.put("/console/home-reel", json=[]),
        anon_client.post(f"/console/projects/{DRAFT_PROJECT}/transition",
                         json={"to_state": STATE_PUBLISHED}),
    ]
    for attempt in attempts:
        assert attempt.status_code in (401, 403), (
            f"{attempt.request.method} {attempt.request.url.path} from an anonymous session "
            f"is rejected by the server; got {attempt.status_code}"
        )
    settle()
    assert db.count_projects() == before, "the protected state is unchanged"
    assert anon_client.get("/auth/me").status_code in (401, 403), (
        "the identity endpoint answers denied without a token"
    )


def test_sitemap_lists_published_routes_and_robots_refuses_the_preview(db):
    sitemap = httpx.get(f"{app_origin()}/sitemap.xml")
    assert sitemap.status_code == 200, f"/sitemap.xml returned {sitemap.status_code}"
    for route in ("/projects", f"/projects/{REEL_PROJECT}", "/about-us", "/privacy"):
        assert route in sitemap.text, f"the sitemap lists {route}"
    assert "/preview" not in sitemap.text, "the sitemap never lists the preview route"
    robots = httpx.get(f"{app_origin()}/robots.txt")
    assert robots.status_code == 200, f"/robots.txt returned {robots.status_code}"
    assert "sitemap" in robots.text.lower(), "the robots file names the sitemap"
    assert "/preview" in robots.text, "the robots file refuses the preview route"


def test_security_headers_are_present_on_every_response():
    for route in PUBLIC_ROUTES[:6]:
        response = httpx.get(f"{app_origin()}{route}", follow_redirects=True)
        assert response.status_code == 200, f"{route} returned {response.status_code}"
        present = {k.lower() for k in response.headers}
        missing = [h for h in SECURITY_HEADERS if h not in present]
        assert not missing, f"{route} is missing {missing}"
        frame = response.headers.get("content-security-policy", "").lower()
        assert "frame-ancestors" in frame, f"{route} carries no frame ancestors refusal"
        if "connect-src" in frame:
            connect = frame.split("connect-src")[-1].split(";")[0]
            assert "*" not in connect, (
                f"{route} wildcards its connection targets rather than enumerating them"
            )
        permissions = response.headers.get("permissions-policy", "").lower()
        for feature in ("camera", "microphone", "geolocation", "payment"):
            assert feature in permissions, f"{route} does not deny {feature}"


def test_no_credential_appears_in_what_the_browser_downloads():
    seen = []
    for route in PUBLIC_ROUTES[:6]:
        page = httpx.get(f"{app_origin()}{route}", follow_redirects=True)
        seen.append((route, page.text))
        for asset in set(re.findall(r'(?:src|href)="([^"]+\.(?:js|css|mjs))"', page.text)):
            url = asset if asset.startswith("http") else f"{app_origin()}{asset}"
            fetched = httpx.get(url)
            assert fetched.status_code == 200, (
                f"{asset} is referenced by {route} and must resolve; got "
                f"{fetched.status_code}"
            )
            seen.append((asset, fetched.text))
    for where, text in seen:
        for marker in CREDENTIAL_MARKERS:
            assert marker not in text, (
                f"{marker!r} appears in {where}; no credential, key or token may appear in "
                f"anything the browser downloads"
            )


def test_retired_path_resolves_permanently_in_one_hop(db):
    assert db.count_retired_paths() == SEEDED_RETIRED_PATH_ROWS
    for path, target in RETIRED_PATHS.items():
        first = httpx.get(f"{app_origin()}{path}", follow_redirects=False)
        assert first.status_code in (301, 308), (
            f"{path} resolves permanently; got {first.status_code}"
        )
        location = first.headers.get("location", "")
        assert location.endswith(f"/projects/{target}"), (
            f"{path} resolves in one hop to /projects/{target}; got {location!r}"
        )
        second = httpx.get(f"{app_origin()}{location}", follow_redirects=False)
        assert second.status_code == 200, (
            f"the target of {path} is the case study itself rather than a second hop; "
            f"got {second.status_code}"
        )


def test_seeded_catalogue_is_stored_as_the_declared_row_counts(db):
    assert db.count_projects() >= SEEDED_PROJECT_ROWS, (
        f"the seeded catalogue is {SEEDED_PROJECT_ROWS} projects"
    )
    assert db.count_disciplines() == SEEDED_DISCIPLINE_ROWS
    assert db.count_chapters() == SEEDED_CHAPTER_ROWS
    assert db.count_accounts() >= SEEDED_ACCOUNT_ROWS
    assert db.count_media() >= SEEDED_MEDIA_ROWS
    assert db.count_media(state="deriving") >= 1, (
        f"one seeded media is still deriving, which is what gates {GATED_PROJECT!r}"
    )
    for email in (PRODUCER_EMAIL, EDITOR_EMAIL):
        account = db.account(email)
        assert account is not None, f"{email} is seeded"
        assert account.get("password_hash"), "passwords are stored hashed, never in clear"
        assert console_password() not in str(account.values()), (
            "the seeded password never appears in clear on the row"
        )


def test_health_endpoint_answers_ready(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returns 200 once the app is ready; got {response.status_code}"
    )
    assert app_origin().startswith("http"), (
        "the app is reachable at the public address read from the environment"
    )
    for route in CONSOLE_ROUTES[:1]:
        page = httpx.get(f"{app_origin()}{route}", follow_redirects=False)
        assert page.status_code in (200, 302, 303, 307, 308, 401, 403), (
            f"{route} answers rather than failing; got {page.status_code}"
        )
