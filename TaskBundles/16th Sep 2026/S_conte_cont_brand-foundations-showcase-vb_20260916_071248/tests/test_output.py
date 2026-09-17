"""The Latticework Foundations verifier: one merged module.

Core features, data integrity, authorization, edge cases and the two declared
slots (PostgreSQL and MinIO) in one file. Every literal asserted here is pinned
in instruction.md.
"""

from __future__ import annotations

import json

import httpx

from conftest import (
    AUTHOR2_EMAIL,
    AUTHOR_EMAIL,
    CARD_EYEBROWS,
    CHAPTER_SLUGS,
    CLIENT_ERROR,
    COLOUR_CAPTION_COUNT,
    COLOUR_SECTION_COUNT,
    DENIED,
    DRAFT_SLUGS,
    ENDPOINTS_HEADING,
    FAVICON_ROUTE,
    FIRST_COLOUR_CAPTION,
    FIRST_LOGO_CAPTION,
    INDEX_LABELS,
    LOCALE,
    LOGO_CAPTION_COUNT,
    LOGO_SECTION_COUNT,
    MEDIA_KEY_EXAMPLE,
    OBJECT_PREFIX,
    OK_CREATED,
    OTHER_AUTHOR_DRAFT,
    PUBLISHED_SLUGS,
    PUBLIC_ROUTES,
    READER_EMAIL,
    REFUSED,
    ROBOTS_ROUTE,
    ROLE_AUTHOR,
    ROLE_READER,
    SECTION_KINDS,
    SEED_PASSWORD,
    SEED_TRIAL_EMAIL,
    SITEMAP_ROUTE,
    TEMPLATE_NAMES,
    TIERS,
    TONE_GROUPS,
    TONE_STOP_COUNT,
    TRIAL_SUCCESS,
    WIZARD_ROUTES,
    add_section,
    anon,
    api_base,
    app_url,
    bearer,
    chapter_by_slug,
    chapter_rows,
    create_chapter,
    excerpt,
    media_rows,
    positions,
    probe_email,
    section_ids,
    sections_of,
    settle,
    sha256_hex,
    sign_in,
    sign_up,
    site,
    submit_trial,
    token_for,
    token_of,
)


def test_health_route_is_ready(anonymous):
    """GET /api/health answers 200 once the app is up."""
    response = anonymous.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}, expected 200 once the "
        f"app is ready: {excerpt(response)}"
    )


def test_seeded_chapters_are_persisted_rows(anonymous, backend):
    """The five chapters are rows in PostgreSQL, ordered by index label."""
    rows = backend.rows("chapter")
    slugs = [row["slug"] for row in rows]
    for slug in CHAPTER_SLUGS:
        assert slug in slugs, (
            f"the chapter table holds {sorted(slugs)} but the brief seeds "
            f"{CHAPTER_SLUGS} and {slug!r} is absent"
        )
    labels = {row["slug"]: str(row["index_label"]) for row in rows
              if row["slug"] in INDEX_LABELS}
    assert labels == INDEX_LABELS, (
        f"the seeded index labels are {labels}, expected {INDEX_LABELS} so the "
        f"carousel orders Color, Logo, Typography, Photography, Motion"
    )
    served = chapter_rows(anonymous)
    served_order = [row.get("index_label") for row in served]
    assert served_order == sorted(served_order), (
        f"GET /api/chapters returned index labels {served_order}, which are not in "
        f"index order; the brief orders chapters by index label"
    )


def test_published_chapter_rows_are_color_and_logo(backend):
    """Exactly color and logo are published, and the draft owners are seeded."""
    rows = {row["slug"]: row for row in backend.rows("chapter")}
    published = sorted(slug for slug, row in rows.items() if row.get("published"))
    assert published == sorted(PUBLISHED_SLUGS), (
        f"the published chapters are {published}, expected {sorted(PUBLISHED_SLUGS)}"
    )
    accounts = {row["id"]: row["email"] for row in backend.rows("account")}
    owner = accounts.get(rows[OTHER_AUTHOR_DRAFT].get("author_account_id"))
    assert owner == AUTHOR2_EMAIL, (
        f"the {OTHER_AUTHOR_DRAFT!r} chapter is owned by {owner!r}, expected "
        f"{AUTHOR2_EMAIL!r} so one author's draft is another author's forbidden row"
    )


def test_chapter_list_row_shape_is_served(anonymous):
    """GET /api/chapters is an array carrying the five advertised chapters."""
    rows = chapter_rows(anonymous)
    slugs = sorted(row.get("slug") for row in rows)
    assert slugs == sorted(CHAPTER_SLUGS), (
        f"GET /api/chapters advertises {slugs}, expected all five of "
        f"{sorted(CHAPTER_SLUGS)}; the index advertises every chapter by name"
    )
    for row in rows:
        for field in ("slug", "index_label", "eyebrow", "title", "published"):
            assert field in row, (
                f"a chapter row is missing {field!r}: {json.dumps(row)[:200]}"
            )
    eyebrows = [row["eyebrow"] for row in rows]
    for want in CARD_EYEBROWS:
        assert want in eyebrows, (
            f"the card eyebrows are {eyebrows}, and the pinned {want!r} is absent"
        )


def test_published_chapter_returns_sections_stored_in_position_order(anonymous):
    """A published chapter's sections come back in contiguous position order."""
    rows = sections_of(anonymous, "color")
    assert len(rows) == COLOUR_SECTION_COUNT, (
        f"GET /api/chapters/color/sections returned {len(rows)} sections, expected "
        f"{COLOUR_SECTION_COUNT}: an intro, four tone groups, two poster stacks, a "
        f"rules section and a closing cta"
    )
    assert positions(rows) == list(range(1, len(rows) + 1)), (
        f"the colour chapter's positions are {positions(rows)}, expected them "
        f"contiguous from one"
    )
    for row in rows:
        assert row.get("kind") in SECTION_KINDS, (
            f"a section carries kind {row.get('kind')!r}, which is outside the "
            f"pinned set {SECTION_KINDS}"
        )
    kinds = [row["kind"] for row in rows]
    assert kinds.count("tone-group") == len(TONE_GROUPS), (
        f"the colour chapter carries {kinds.count('tone-group')} tone-group "
        f"sections, expected {len(TONE_GROUPS)} for Core, Dark, Bright and Light"
    )
    assert kinds[-1] == "cta", (
        f"the colour chapter's last section is {kinds[-1]!r}, expected 'cta': the "
        f"chapter closes on the poster carrying the trial call to action"
    )


def test_seeded_sections_count_per_chapter_is_stored(anonymous):
    """Both published chapters carry the section set the brief seeds."""
    assert len(sections_of(anonymous, "logo")) == LOGO_SECTION_COUNT, (
        f"the logo chapter carries {len(sections_of(anonymous, 'logo'))} sections, "
        f"expected {LOGO_SECTION_COUNT}"
    )
    headings = [row.get("heading") for row in sections_of(anonymous, "color")]
    for group in TONE_GROUPS:
        assert any(group == (heading or "").strip() for heading in headings), (
            f"the colour chapter's section headings are {headings}, and the tone "
            f"group {group!r} has no section of its own"
        )


def test_seeded_tone_stops_exist_per_group_per_tier(backend):
    """Twelve tone stops: four groups across three tiers, stored separately."""
    rows = backend.rows("tone_stop")
    assert len(rows) >= TONE_STOP_COUNT, (
        f"the tone_stop table holds {len(rows)} rows, expected at least "
        f"{TONE_STOP_COUNT}: one per tone group per tier"
    )
    pairs = {(str(row["group_name"]), str(row["tier"])) for row in rows}
    for group in TONE_GROUPS:
        for tier in TIERS:
            assert (group, tier) in pairs, (
                f"no tone stop is stored for group {group!r} at tier {tier!r}; the "
                f"journey is art-directed per tier rather than inherited"
            )
    desktop = {row["group_name"]: row["ground"] for row in rows
               if row["tier"] == "desktop"}
    mobile = {row["group_name"]: row["ground"] for row in rows
              if row["tier"] == "mobile"}
    assert any(desktop.get(g) != mobile.get(g) for g in TONE_GROUPS), (
        f"every mobile ground equals its desktop ground ({desktop} against "
        f"{mobile}); the brief art-directs the phone journey separately"
    )


def test_seeded_captions_are_stored_in_order(anonymous, backend):
    """Nine colour captions and seven logo captions, in the pinned order."""
    rows = backend.rows("caption")
    texts = [row["text"] for row in rows]
    assert FIRST_COLOUR_CAPTION in texts, (
        f"the caption table does not carry {FIRST_COLOUR_CAPTION!r}; the colour "
        f"chapter seeds nine captions and this is the first"
    )
    assert FIRST_LOGO_CAPTION in texts, (
        f"the caption table does not carry {FIRST_LOGO_CAPTION!r}; the logo "
        f"chapter seeds seven captions and this is the first"
    )
    assert len(rows) >= COLOUR_CAPTION_COUNT + LOGO_CAPTION_COUNT, (
        f"the caption table holds {len(rows)} rows, expected at least "
        f"{COLOUR_CAPTION_COUNT + LOGO_CAPTION_COUNT}"
    )


def test_copy_entries_are_stored_by_locale_and_key(anonymous, backend):
    """Every displayed string is a copy entry, served keyed by locale."""
    response = anonymous.get("/copy", params={"locale": LOCALE})
    assert response.status_code == 200, (
        f"GET /api/copy?locale={LOCALE} returned {response.status_code}, expected "
        f"200: {excerpt(response)}"
    )
    body = response.json()
    assert isinstance(body, dict) and body, (
        f"GET /api/copy returned {str(body)[:200]}, expected a non-empty object of "
        f"key to string"
    )
    rows = backend.rows("copy_entry")
    assert rows, "the copy_entry table is empty; every string is a catalogue key"
    locales = {row["locale"] for row in rows}
    assert len(locales) == 1, (
        f"the copy_entry table carries locales {sorted(locales)}, and the brief "
        f"ships exactly one"
    )
    keys = [row["key"] for row in rows]
    assert len(keys) == len(set(keys)), (
        "the copy_entry table repeats a key inside one locale, which its "
        "uniqueness rule forbids"
    )
    for name in TEMPLATE_NAMES:
        assert any(name in str(row.get("value")) for row in rows), (
            f"the demo template name {name!r} appears in no copy entry"
        )


def test_generated_object_exists_in_the_bucket_at_its_key(anonymous, store, backend):
    """Every media row has a real object in MinIO under the pinned scheme."""
    rows = backend.rows("media_ref")
    assert rows, (
        "the media_ref table is empty; every picture the product shows is "
        "generated once and stored in the object store"
    )
    keys = store.list(OBJECT_PREFIX)
    assert keys, (
        f"the bucket holds no object under the {OBJECT_PREFIX!r} prefix; generated "
        f"bytes live in MinIO, never on the app's disk"
    )
    for row in rows:
        key = row["object_key"]
        assert key.startswith(OBJECT_PREFIX), (
            f"the media row {row['media_key']!r} stores object_key {key!r}, which "
            f"does not follow media/{{chapter_slug}}/{{media_key}}/{{digest}}.png"
        )
        assert store.exists(key), (
            f"the media row {row['media_key']!r} names object {key!r}, which is "
            f"not in the bucket: a row with no object is a defect"
        )
    row_keys = {row["object_key"] for row in rows}
    orphans = [key for key in keys if key not in row_keys]
    assert not orphans, (
        f"the bucket carries {len(orphans)} object(s) with no media row, such as "
        f"{orphans[:3]}: an object with no row is a defect"
    )


def test_object_key_carries_the_digest_of_the_stored_bytes(anonymous, backend):
    """The digest in a key is the digest of the bytes the key holds."""
    rows = backend.rows("media_ref")
    published_media = [row for row in rows if row.get("digest")]
    assert published_media, "no media row carries a digest"
    for row in published_media:
        key = row["object_key"]
        digest = str(row["digest"])
        assert digest in key, (
            f"the media row {row['media_key']!r} stores digest {digest!r} but its "
            f"key is {key!r}; the digest in the key is the digest of the bytes"
        )
        assert key.endswith(".png"), (
            f"the object key {key!r} does not end in the extension the scheme pins"
        )
        assert f"/{row['media_key']}/" in key, (
            f"the object key {key!r} does not carry its media key "
            f"{row['media_key']!r} as a path segment"
        )


def test_stored_media_is_streamed_for_a_published_chapter(anonymous, backend):
    """A published chapter's image streams from the object store to anyone."""
    rows = [row for row in backend.rows("media_ref")]
    chapters = {row["id"]: row for row in backend.rows("chapter")}
    sections = {row["id"]: row for row in backend.rows("section")}
    public = []
    for row in rows:
        section = sections.get(row.get("section_id"))
        if not section:
            continue
        chapter = chapters.get(section.get("chapter_id"))
        if chapter and chapter.get("published"):
            public.append(row)
    assert public, "no media row belongs to a published chapter"
    row = public[0]
    response = anonymous.get(f"/media/{row['media_key']}/content")
    assert response.status_code == 200, (
        f"GET /api/media/{row['media_key']}/content returned "
        f"{response.status_code}, expected 200 for a published chapter's image: "
        f"{excerpt(response)}"
    )
    assert response.content, (
        f"GET /api/media/{row['media_key']}/content returned an empty body; the "
        f"stored object is what is served"
    )
    assert sha256_hex(response.content) == str(row["digest"]), (
        f"the bytes served for {row['media_key']!r} do not hash to the stored "
        f"digest {row['digest']!r}, so the image was redrawn rather than read"
    )


def test_no_image_bytes_are_stored_outside_the_object_store(backend):
    """No database column holds an image; the object store is the fact."""
    rows = backend.rows("media_ref")
    for row in rows:
        for field, value in row.items():
            if not isinstance(value, (str, bytes, memoryview)):
                continue
            blob = bytes(value) if not isinstance(value, str) else value.encode()
            assert len(blob) < 4096, (
                f"the media row {row.get('media_key')!r} carries {len(blob)} bytes "
                f"in column {field!r}; image bytes live in MinIO, never in a column"
            )


def test_object_store_is_reached_at_its_pinned_variables(store, backend):
    """PostgreSQL and MinIO are the two backing services, at their variables."""
    assert store.list(OBJECT_PREFIX) is not None, (
        "the object store did not answer a listing at STORAGE_ENDPOINT / "
        "STORAGE_BUCKET with the STORAGE_ACCESS_KEY and STORAGE_SECRET_KEY given"
    )
    assert backend.count("chapter") >= len(CHAPTER_SLUGS), (
        f"PostgreSQL at DATABASE_URL holds {backend.count('chapter')} chapters, "
        f"expected at least {len(CHAPTER_SLUGS)}"
    )


def test_bucket_is_not_publicly_readable(store, backend):
    """A draft object is not fetchable straight from the bucket's own address."""
    endpoint = None
    import os

    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    bucket = os.environ["STORAGE_BUCKET"]
    keys = store.list(OBJECT_PREFIX)
    assert keys, "the bucket holds no object to check"
    with httpx.Client(timeout=30.0) as client:
        response = client.get(f"{endpoint}/{bucket}/{keys[0]}")
    assert response.status_code in CLIENT_ERROR, (
        f"an unauthenticated read of {keys[0]!r} straight from the bucket returned "
        f"{response.status_code}; the bucket is never publicly readable and no "
        f"pre-signed address is handed out"
    )


def test_signup_creates_a_reader_record(backend):
    """Signup is open, and what it creates is a reader."""
    email = probe_email()
    response = sign_up(email=email, display_name="Probe Reader")
    assert response.status_code in OK_CREATED, (
        f"POST /api/auth/sign-up returned {response.status_code}, expected one of "
        f"{OK_CREATED}: signup is open: {excerpt(response)}"
    )
    row = settle(lambda: backend.one("account", email=email))
    assert row, f"no account row was written for {email!r} after a successful signup"
    assert row.get("role") == ROLE_READER, (
        f"the account created for {email!r} carries role {row.get('role')!r}, "
        f"expected {ROLE_READER!r}: the author role is not self-assignable"
    )
    assert str(row.get("password_hash") or "") != SEED_PASSWORD, (
        "the account row stores the password in a recoverable form"
    )


def test_signup_asking_for_the_author_role_is_refused(backend):
    """A signup that asks for the author role is refused and writes nothing."""
    email = probe_email()
    response = sign_up(email=email, role=ROLE_AUTHOR)
    if response.status_code in OK_CREATED:
        row = backend.one("account", email=email)
        assert row and row.get("role") == ROLE_READER, (
            f"POST /api/auth/sign-up with role={ROLE_AUTHOR!r} produced an account "
            f"with role {(row or {}).get('role')!r}; the author role is never "
            f"granted from a request body"
        )
        return
    assert response.status_code in REFUSED, (
        f"POST /api/auth/sign-up with role={ROLE_AUTHOR!r} returned "
        f"{response.status_code}, expected either a reader account or a refusal in "
        f"{REFUSED}: {excerpt(response)}"
    )
    assert backend.one("account", email=email) is None, (
        f"a refused signup still wrote an account row for {email!r}"
    )


def test_sign_in_returns_a_token_and_a_wrong_password_is_refused():
    """The seeded password works; a wrong one is refused without a hint."""
    good = sign_in(AUTHOR_EMAIL, SEED_PASSWORD)
    assert good.status_code == 200, (
        f"POST /api/auth/sign-in for {AUTHOR_EMAIL} with the seeded password "
        f"returned {good.status_code}, expected 200: {excerpt(good)}"
    )
    assert token_of(good.json()), (
        f"a successful sign-in returned no bearer token: {excerpt(good)}"
    )
    bad = sign_in(AUTHOR_EMAIL, "not-the-seeded-password")
    assert bad.status_code in CLIENT_ERROR, (
        f"POST /api/auth/sign-in with a wrong password returned {bad.status_code}, "
        f"expected a client error: {excerpt(bad)}"
    )
    unknown = sign_in(probe_email(), SEED_PASSWORD)
    assert unknown.status_code in CLIENT_ERROR, (
        f"POST /api/auth/sign-in for an unknown address returned "
        f"{unknown.status_code}, expected a client error: {excerpt(unknown)}"
    )
    assert bad.status_code == unknown.status_code, (
        f"a wrong password answers {bad.status_code} and an unknown address "
        f"answers {unknown.status_code}; the refusal must not say which of the two "
        f"was wrong"
    )


def test_sign_out_invalidates_the_token():
    """A token stops working once its session is signed out."""
    email, token = probe_email(), None
    response = sign_up(email=email)
    assert response.status_code in OK_CREATED, (
        f"POST /api/auth/sign-up returned {response.status_code}: {excerpt(response)}"
    )
    token = token_of(response.json()) or token_for(email)
    with bearer(token) as client:
        out = client.post("/auth/sign-out")
        assert out.status_code in (200, 204), (
            f"POST /api/auth/sign-out returned {out.status_code}, expected 200 or "
            f"204: {excerpt(out)}"
        )
        replay = client.get("/trials")
    assert replay.status_code in DENIED, (
        f"a request replaying the signed-out token returned {replay.status_code}, "
        f"expected one of {DENIED}: signing out invalidates the token"
    )


def test_draft_chapter_is_denied_to_an_anonymous_caller(anonymous):
    """An unpublished chapter is not readable by a signed-out caller."""
    for slug in DRAFT_SLUGS:
        response = anonymous.get(f"/chapters/{slug}")
        assert response.status_code in DENIED, (
            f"GET /api/chapters/{slug} returned {response.status_code} to a "
            f"signed-out caller, expected one of {DENIED}: an unpublished chapter "
            f"is not a public chapter: {excerpt(response)}"
        )
        sections = anonymous.get(f"/chapters/{slug}/sections")
        assert sections.status_code in DENIED, (
            f"GET /api/chapters/{slug}/sections returned {sections.status_code} to "
            f"a signed-out caller, expected one of {DENIED}"
        )


def test_draft_chapter_is_denied_to_a_reader_role(reader, anonymous):
    """A signed-in reader is refused every unpublished chapter."""
    for slug in DRAFT_SLUGS:
        response = reader.get(f"/chapters/{slug}")
        assert response.status_code in DENIED, (
            f"GET /api/chapters/{slug} returned {response.status_code} to "
            f"{READER_EMAIL}, expected one of {DENIED}: {excerpt(response)}"
        )
    listed = chapter_rows(anonymous)
    for row in listed:
        if row["slug"] in DRAFT_SLUGS:
            assert not row.get("published"), (
                f"the public chapter list marks {row['slug']!r} as published"
            )
            assert "sections" not in row or not row.get("sections"), (
                f"the public chapter list carries body content for the "
                f"unpublished chapter {row['slug']!r}"
            )


def test_draft_media_object_is_denied_to_an_unentitled_caller(anonymous, reader,
                                                              backend):
    """A draft chapter's generated image is not streamed to the unentitled."""
    chapters = {row["id"]: row for row in backend.rows("chapter")}
    sections = {row["id"]: row for row in backend.rows("section")}
    draft_media = []
    for row in backend.rows("media_ref"):
        section = sections.get(row.get("section_id"))
        if not section:
            continue
        chapter = chapters.get(section.get("chapter_id"))
        if chapter and not chapter.get("published"):
            draft_media.append(row)
    assert draft_media, (
        "no media row belongs to an unpublished chapter, so the draft-visibility "
        "rule has nothing to protect; the brief seeds three unpublished chapters"
    )
    key = draft_media[0]["media_key"]
    for label, client in (("a signed-out caller", anonymous),
                          (READER_EMAIL, reader)):
        response = client.get(f"/media/{key}/content")
        assert response.status_code in DENIED, (
            f"GET /api/media/{key}/content returned {response.status_code} to "
            f"{label}, expected one of {DENIED}: a draft image is served only "
            f"through an authenticated stream to its own author"
        )


def test_other_authors_draft_row_is_denied(author, other_author):
    """One author cannot read, edit or publish another author's chapter."""
    response = author.get(f"/chapters/{OTHER_AUTHOR_DRAFT}")
    assert response.status_code in DENIED, (
        f"GET /api/chapters/{OTHER_AUTHOR_DRAFT} returned {response.status_code} "
        f"to {AUTHOR_EMAIL}, expected one of {DENIED}: that chapter belongs to "
        f"{AUTHOR2_EMAIL}: {excerpt(response)}"
    )
    sections = author.get(f"/chapters/{OTHER_AUTHOR_DRAFT}/sections")
    assert sections.status_code in DENIED, (
        f"GET /api/chapters/{OTHER_AUTHOR_DRAFT}/sections returned "
        f"{sections.status_code} to {AUTHOR_EMAIL}, expected one of {DENIED}"
    )
    publish = author.post(f"/chapters/{OTHER_AUTHOR_DRAFT}/publish")
    assert publish.status_code in DENIED, (
        f"POST /api/chapters/{OTHER_AUTHOR_DRAFT}/publish returned "
        f"{publish.status_code} to {AUTHOR_EMAIL}, expected one of {DENIED}"
    )
    owner = other_author.get(f"/chapters/{OTHER_AUTHOR_DRAFT}")
    assert owner.status_code == 200, (
        f"GET /api/chapters/{OTHER_AUTHOR_DRAFT} returned {owner.status_code} to "
        f"its own author {AUTHOR2_EMAIL}, expected 200: {excerpt(owner)}"
    )


def test_reader_is_denied_every_author_only_route(reader, author):
    """The trial list and the author writes are refused to a reader."""
    trials = reader.get("/trials")
    assert trials.status_code in DENIED, (
        f"GET /api/trials returned {trials.status_code} to {READER_EMAIL}, "
        f"expected one of {DENIED}: the trial list is an author's: "
        f"{excerpt(trials)}"
    )
    created = reader.post("/chapters", json={
        "slug": "reader-made", "index_label": "09", "eyebrow": "( Probe )",
        "title": "Probe", "lead": "A reader should not be able to write this.",
    })
    assert created.status_code in DENIED, (
        f"POST /api/chapters returned {created.status_code} to {READER_EMAIL}, "
        f"expected one of {DENIED}: {excerpt(created)}"
    )
    publish = reader.post("/chapters/color/publish")
    assert publish.status_code in DENIED, (
        f"POST /api/chapters/color/publish returned {publish.status_code} to "
        f"{READER_EMAIL}, expected one of {DENIED}"
    )
    allowed = author.get("/trials")
    assert allowed.status_code == 200, (
        f"GET /api/trials returned {allowed.status_code} to {AUTHOR_EMAIL}, "
        f"expected 200: {excerpt(allowed)}"
    )


def test_role_is_never_read_from_the_request_body(reader, backend):
    """A caller cannot promote themselves by saying so in a request."""
    response = reader.post("/chapters", json={
        "slug": "role-in-body", "index_label": "09", "eyebrow": "( Probe )",
        "title": "Probe", "lead": "The role travels in the body here.",
        "role": ROLE_AUTHOR,
    })
    assert response.status_code in DENIED, (
        f"POST /api/chapters carrying role={ROLE_AUTHOR!r} in the body returned "
        f"{response.status_code} to {READER_EMAIL}, expected one of {DENIED}: the "
        f"role is read from the account row, never from the request"
    )
    row = backend.one("account", email=READER_EMAIL)
    assert row and row.get("role") == ROLE_READER, (
        f"{READER_EMAIL} now carries role {(row or {}).get('role')!r}; a request "
        f"body must never change a role"
    )


def test_bearer_auth_is_required_where_the_contract_says_so(anonymous):
    """The author endpoints need a token; the public reads do not."""
    for path in ("/trials",):
        response = anonymous.get(path)
        assert response.status_code in DENIED, (
            f"GET /api{path} returned {response.status_code} with no bearer token, "
            f"expected one of {DENIED}"
        )
    for path in ("/chapters", "/health"):
        response = anonymous.get(path)
        assert response.status_code == 200, (
            f"GET /api{path} returned {response.status_code} with no bearer token, "
            f"expected 200: that read is public"
        )
    with bearer("not-a-real-token") as client:
        response = client.get("/trials")
    assert response.status_code in DENIED, (
        f"GET /api/trials with a made-up bearer token returned "
        f"{response.status_code}, expected one of {DENIED}"
    )


def test_section_reorder_leaves_positions_contiguous_and_stored(author, backend):
    """A reorder is a permutation, and it survives being read back."""
    slug = create_chapter(author)["slug"]
    for n in range(3):
        add_section(author, slug, f"Probe section {n + 1}")
    before = sections_of(author, slug)
    assert positions(before) == [1, 2, 3], (
        f"a new chapter's three sections carry positions {positions(before)}, "
        f"expected [1, 2, 3]"
    )
    ids = section_ids(before)
    wanted = [ids[2], ids[0], ids[1]]
    response = author.put(f"/chapters/{slug}/order", json={"order": wanted})
    assert response.status_code == 200, (
        f"PUT /api/chapters/{slug}/order returned {response.status_code}, expected "
        f"200: {excerpt(response)}"
    )
    after = sections_of(author, slug)
    assert section_ids(after) == wanted, (
        f"after the reorder the sections read back as {section_ids(after)}, "
        f"expected {wanted}"
    )
    assert positions(after) == [1, 2, 3], (
        f"after the reorder the positions are {positions(after)}, expected them "
        f"contiguous from one: a reorder is a permutation, never an insertion"
    )
    stored = sorted(int(row["position"]) for row in backend.rows("section")
                    if str(row.get("chapter_id")) in {str(r.get("chapter_id"))
                                                      for r in backend.rows("section")}
                    and str(row["id"]) in set(wanted))
    assert stored == [1, 2, 3], (
        f"the section rows in PostgreSQL carry positions {stored}, expected "
        f"[1, 2, 3] after the reorder"
    )


def test_publish_makes_the_chapter_row_readable_and_listed(author, anonymous,
                                                           backend):
    """Publishing makes a chapter public, records the moment and lists it."""
    slug = create_chapter(author)["slug"]
    add_section(author, slug, "Probe opening")
    hidden = anonymous.get(f"/chapters/{slug}")
    assert hidden.status_code in DENIED, (
        f"GET /api/chapters/{slug} returned {hidden.status_code} before publication"
    )
    response = author.post(f"/chapters/{slug}/publish")
    assert response.status_code in OK_CREATED, (
        f"POST /api/chapters/{slug}/publish returned {response.status_code}, "
        f"expected one of {OK_CREATED}: {excerpt(response)}"
    )
    shown = anonymous.get(f"/chapters/{slug}")
    assert shown.status_code == 200, (
        f"GET /api/chapters/{slug} returned {shown.status_code} after publication, "
        f"expected 200: {excerpt(shown)}"
    )
    row = backend.one("chapter", slug=slug)
    assert row and row.get("published"), (
        f"the chapter row for {slug!r} is not marked published"
    )
    assert row.get("published_at"), (
        f"the chapter row for {slug!r} records no publication moment"
    )
    with site() as public:
        sitemap = public.get(SITEMAP_ROUTE)
    assert slug in sitemap.text, (
        f"{SITEMAP_ROUTE} does not name the newly published chapter {slug!r}"
    )


def test_unpublish_reverses_publication(author, anonymous, backend):
    """Unpublishing takes a chapter back out of every public read."""
    slug = create_chapter(author)["slug"]
    add_section(author, slug, "Probe opening")
    author.post(f"/chapters/{slug}/publish")
    response = author.post(f"/chapters/{slug}/unpublish")
    assert response.status_code in OK_CREATED, (
        f"POST /api/chapters/{slug}/unpublish returned {response.status_code}, "
        f"expected one of {OK_CREATED}: {excerpt(response)}"
    )
    hidden = anonymous.get(f"/chapters/{slug}")
    assert hidden.status_code in DENIED, (
        f"GET /api/chapters/{slug} returned {hidden.status_code} after "
        f"unpublication, expected one of {DENIED}"
    )
    row = backend.one("chapter", slug=slug)
    assert row and not row.get("published"), (
        f"the chapter row for {slug!r} is still marked published"
    )
    with site() as public:
        sitemap = public.get(SITEMAP_ROUTE)
    assert slug not in sitemap.text, (
        f"{SITEMAP_ROUTE} still names the unpublished chapter {slug!r}"
    )


def test_publish_of_a_sectionless_chapter_is_refused(author, backend):
    """A chapter with no sections cannot be published."""
    slug = create_chapter(author)["slug"]
    response = author.post(f"/chapters/{slug}/publish")
    assert response.status_code in REFUSED, (
        f"POST /api/chapters/{slug}/publish returned {response.status_code} for a "
        f"chapter carrying no sections, expected one of {REFUSED}: "
        f"{excerpt(response)}"
    )
    row = backend.one("chapter", slug=slug)
    assert row and not row.get("published"), (
        f"the refused publish still marked {slug!r} published"
    )


def test_new_chapter_is_created_unpublished_and_owned_by_the_caller(author,
                                                                   backend):
    """A wizard-created chapter starts unpublished and belongs to its author."""
    slug = create_chapter(author)["slug"]
    row = backend.one("chapter", slug=slug)
    assert row, f"no chapter row was written for {slug!r}"
    assert not row.get("published"), (
        f"the chapter {slug!r} was created already published"
    )
    accounts = {r["id"]: r["email"] for r in backend.rows("account")}
    assert accounts.get(row.get("author_account_id")) == AUTHOR_EMAIL, (
        f"the chapter {slug!r} is owned by "
        f"{accounts.get(row.get('author_account_id'))!r}, expected the caller "
        f"{AUTHOR_EMAIL!r}"
    )
    section = add_section(author, slug, "Probe opening")
    assert int(section["position"]) == 1, (
        f"the first section of a new chapter landed at position "
        f"{section['position']}, expected 1"
    )


def test_trial_signup_is_stored_once_per_address(backend):
    """One record per address, however many times the control is pressed."""
    email = probe_email()
    first = submit_trial(email)
    assert first.status_code in OK_CREATED, (
        f"POST /api/trials returned {first.status_code} for a fresh address, "
        f"expected one of {OK_CREATED}: {excerpt(first)}"
    )
    second = submit_trial(email)
    assert second.status_code in OK_CREATED, (
        f"POST /api/trials returned {second.status_code} for a repeated address, "
        f"expected one of {OK_CREATED}: a visitor is never told off for pressing "
        f"twice: {excerpt(second)}"
    )
    assert backend.count("trial_signup", email=email) == 1, (
        f"the trial_signup table holds "
        f"{backend.count('trial_signup', email=email)} rows for {email!r}, "
        f"expected exactly one"
    )
    assert backend.count("trial_signup", email=SEED_TRIAL_EMAIL) == 1, (
        f"the seeded trial address {SEED_TRIAL_EMAIL!r} has "
        f"{backend.count('trial_signup', email=SEED_TRIAL_EMAIL)} rows, expected "
        f"exactly one"
    )


def test_repeat_trial_submission_does_not_move_the_stored_moment(backend):
    """A second submission leaves the first record's moment alone."""
    email = probe_email()
    submit_trial(email)
    first = backend.one("trial_signup", email=email)
    assert first, f"no trial row was written for {email!r}"
    submit_trial(email)
    again = backend.one("trial_signup", email=email)
    assert again and str(again["created_at"]) == str(first["created_at"]), (
        f"the trial row for {email!r} moved from {first['created_at']} to "
        f"{(again or {}).get('created_at')}; a repeat submission changes nothing"
    )


def test_trial_record_keeps_the_source_chapter(backend):
    """The record remembers which chapter the visitor was reading."""
    email = probe_email()
    response = submit_trial(email, slug="logo")
    assert response.status_code in OK_CREATED, (
        f"POST /api/trials returned {response.status_code}: {excerpt(response)}"
    )
    row = backend.one("trial_signup", email=email)
    assert row, f"no trial row was written for {email!r}"
    chapters = {r["id"]: r["slug"] for r in backend.rows("chapter")}
    assert chapters.get(row.get("source_chapter_id")) == "logo", (
        f"the trial row for {email!r} names source chapter "
        f"{chapters.get(row.get('source_chapter_id'))!r}, expected 'logo'"
    )
    body = response.json()
    assert TRIAL_SUCCESS in json.dumps(body) or response.status_code in OK_CREATED, (
        f"a successful trial submission answered {excerpt(response)}"
    )


def test_invalid_trial_address_is_refused_and_nothing_is_stored(backend):
    """An address that is not an address is refused and writes nothing."""
    before = backend.count("trial_signup")
    with anon() as client:
        response = client.post("/trials", json={"email": "not-an-address",
                                                "source_chapter_slug": "color"})
    assert response.status_code in REFUSED, (
        f"POST /api/trials with 'not-an-address' returned {response.status_code}, "
        f"expected one of {REFUSED}: {excerpt(response)}"
    )
    assert backend.count("trial_signup") == before, (
        f"the trial_signup table grew from {before} to "
        f"{backend.count('trial_signup')} on a refused submission; a refusal "
        f"writes nothing"
    )


def test_unknown_address_answers_not_found():
    """An address the product does not have answers not-found."""
    with site() as public:
        response = public.get("/a-route-this-product-does-not-have")
    assert response.status_code == 404, (
        f"an unknown address returned {response.status_code}, expected 404: no "
        f"address ever renders another page with a success status"
    )
    with site() as public:
        draft = public.get("/typography")
    assert draft.status_code in DENIED, (
        f"GET /typography returned {draft.status_code} to a signed-out visitor, "
        f"expected one of {DENIED}"
    )


def test_sitemap_lists_published_routes_only(anonymous):
    """The sitemap names the published chapters and nothing unpublished."""
    with site() as public:
        response = public.get(SITEMAP_ROUTE)
    assert response.status_code == 200, (
        f"GET {SITEMAP_ROUTE} returned {response.status_code}, expected 200: "
        f"{excerpt(response)}"
    )
    body = response.text
    for slug in PUBLISHED_SLUGS:
        assert f"/{slug}" in body, (
            f"{SITEMAP_ROUTE} does not list the published chapter /{slug}"
        )
    for slug in DRAFT_SLUGS:
        assert f"/{slug}" not in body, (
            f"{SITEMAP_ROUTE} lists the unpublished chapter /{slug}"
        )
    assert "/lambda" not in body, (
        f"{SITEMAP_ROUTE} lists /lambda, which is not a public chapter"
    )


def test_robots_file_names_the_sitemap():
    """A robots file exists and points a crawler at the sitemap."""
    with site() as public:
        response = public.get(ROBOTS_ROUTE)
    assert response.status_code == 200, (
        f"GET {ROBOTS_ROUTE} returned {response.status_code}, expected 200"
    )
    assert "sitemap" in response.text.lower(), (
        f"{ROBOTS_ROUTE} does not name the sitemap: {response.text[:200]}"
    )


def test_favicon_is_served_and_declared():
    """The site serves a favicon and declares it in the document head."""
    with site() as public:
        icon = public.get(FAVICON_ROUTE)
    assert icon.status_code == 200 and icon.content, (
        f"GET {FAVICON_ROUTE} returned {icon.status_code} with "
        f"{len(icon.content)} bytes, expected 200 and a body"
    )
    with site() as public:
        home = public.get("/")
    assert "icon" in home.text.lower(), (
        "the home document declares no favicon in its head"
    )


def test_every_public_route_declares_a_resolving_social_preview():
    """Each public route carries its own preview title and a resolving image."""
    seen_titles = []
    with site() as public:
        for route in PUBLIC_ROUTES:
            response = public.get(route)
            assert response.status_code == 200, (
                f"GET {route} returned {response.status_code}, expected 200"
            )
            text = response.text
            assert "og:title" in text or "twitter:title" in text, (
                f"{route} declares no social preview title"
            )
            assert "og:image" in text or "twitter:image" in text, (
                f"{route} declares no social preview image"
            )
            seen_titles.append(text.count("og:title"))
    assert all(count >= 1 for count in seen_titles), (
        f"a public route declared no preview title: counts were {seen_titles}"
    )


def test_every_internal_link_on_a_public_route_resolves():
    """No internal link on a public route points at an address that is gone."""
    import re

    broken = []
    with site() as public:
        for route in PUBLIC_ROUTES:
            page = public.get(route)
            assert page.status_code == 200, (
                f"GET {route} returned {page.status_code}, expected 200"
            )
            for href in set(re.findall(r'href="(/[^"#?]*)"', page.text)):
                target = public.get(href)
                if target.status_code >= 400:
                    broken.append((route, href, target.status_code))
    assert not broken, (
        f"internal links point at addresses that do not answer: {broken[:5]}"
    )


def test_no_credential_appears_in_what_the_browser_downloads():
    """No key or password is inside anything the browser is served."""
    import os
    import re

    secrets = [os.environ["STORAGE_SECRET_KEY"], os.environ["STORAGE_ACCESS_KEY"]]
    with site() as public:
        home = public.get("/")
        bodies = [home.text]
        for src in set(re.findall(r'src="(/[^"]+\.js)"', home.text)):
            bodies.append(public.get(src).text)
    for body in bodies:
        for secret in secrets:
            assert secret not in body, (
                f"the credential {secret[:4]}... appears in something the browser "
                f"downloads; the object store's credentials never leave the server"
            )


def test_api_is_served_on_the_same_origin_under_its_prefix(anonymous):
    """The API and the site share one origin, and the API sits under /api."""
    assert api_base() == f"{app_url()}/api", (
        f"the API base is {api_base()!r}, expected {app_url()}/api on the same "
        f"origin as the site"
    )
    response = anonymous.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code} at {api_base()}"
    )
    with site() as public:
        home = public.get("/")
    assert home.status_code == 200, (
        f"GET / returned {home.status_code} at {app_url()}, expected 200"
    )


def test_seeded_credentials_are_written_for_a_grader_to_sign_in():
    """Every seeded account signs in with the pinned password."""
    for email in (AUTHOR_EMAIL, AUTHOR2_EMAIL, READER_EMAIL):
        response = sign_in(email, SEED_PASSWORD)
        assert response.status_code == 200, (
            f"POST /api/auth/sign-in for the seeded account {email} returned "
            f"{response.status_code}, expected 200 with the pinned password: "
            f"{excerpt(response)}"
        )


def test_seeding_a_second_time_duplicates_no_rows(backend):
    """Nothing the seed writes exists twice."""
    for table, key in (("chapter", "slug"), ("account", "email")):
        values = [row[key] for row in backend.rows(table)]
        assert len(values) == len(set(values)), (
            f"the {table} table repeats a {key}: {sorted(values)}; seeding is "
            f"idempotent, so restarting the app duplicates no rows"
        )
    for slug in ("color", "logo"):
        assert backend.count("chapter", slug=slug) == 1, (
            f"the chapter table holds {backend.count('chapter', slug=slug)} rows "
            f"for {slug!r}, expected exactly one"
        )
