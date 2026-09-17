"""The one merged pytest module for Veloce.

Every assertion is black-box: HTTP against the deployed app, plus the persisted
state read through the declared backend slot and the declared storage slot. The
verifier ships its own image, so the app is reached over APP_PUBLIC_URL alone and
nothing here reads the app container's filesystem. Nothing imports a provider SDK
and nothing inspects the agent's source.

The browser pass runs before this module. It records a cookie choice under its own
visitor key and writes articles it removes again, so the five seeded articles and
the three seeded accounts are untouched on both sides and the pinned counts hold
across two consecutive runs. Every check below that mutates works on a probe
article or a freshly signed-up probe reader, and removes the probe article before
the check ends.
"""

from __future__ import annotations

import appclient
import conftest as C


def test_health_reports_ready_on_the_public_origin(anonymous):
    """The public origin answers the health route once the app holds its services."""
    response = anonymous.get(C.HEALTH_PATH)
    assert response.status_code == 200, C.describe(
        response, "the app must answer GET /api/health with 200 on APP_PUBLIC_URL")


def test_login_returns_a_token_for_each_seeded_account(backend):
    """Each seeded account signs in with the corpus password and carries its role."""
    for email, role, name in ((C.AUTHOR_EMAIL, C.ROLE_AUTHOR, C.AUTHOR_NAME),
                              (C.AUTHOR2_EMAIL, C.ROLE_AUTHOR, C.AUTHOR2_NAME),
                              (C.READER_EMAIL, C.ROLE_READER, C.READER_NAME)):
        token = appclient.login(email, C.SEEDED_PASSWORD)
        assert token, f"the sign-in for {email} must return access_token"
        with appclient.client(token) as signed_in:
            probe = signed_in.get(C.ME_PATH)
        assert probe.status_code == 200, C.describe(
            probe, f"the token minted for {email} must be accepted as a bearer token")
        body = probe.json()
        assert body.get(C.FIELD_EMAIL) == email, C.describe(
            probe, f"the session read must name {email}")
        assert body.get(C.FIELD_ROLE) == role, C.describe(
            probe, f"{email} must carry the role {role}")
        assert body.get(C.FIELD_DISPLAY_NAME) == name, C.describe(
            probe, f"{email} must display as {name}")
        row = C.account_row(backend, email)
        assert row is not None, f"{email} must exist as a stored account row"
        assert row.get(C.FIELD_ROLE) == role, (
            f"{email} must be stored with role {role}, found {row.get(C.FIELD_ROLE)}")


def test_account_rows_store_a_hashed_password_and_a_lowercased_email(backend, suffix):
    """A stored account holds no clear password and no endpoint returns the hash."""
    email = C.probe_email(suffix)
    with appclient.client(None) as visitor:
        created = visitor.post(C.SIGNUP_PATH, json={
            C.FIELD_EMAIL: email.upper(), C.FIELD_PASSWORD: C.SEEDED_PASSWORD})
    assert created.status_code in (200, 201), C.describe(
        created, "signup must be open to any well-formed work address")
    token = created.json().get(C.TOKEN_FIELD)
    assert token, C.describe(created, "signup must answer with access_token")
    assert C.FIELD_PASSWORD_HASH not in created.text, C.describe(
        created, "no signup response may carry the stored password hash")
    row = C.account_row(backend, email)
    assert row is not None, f"{email} must be stored lowercased, not as typed"
    assert row.get(C.FIELD_ROLE) == C.ROLE_READER, (
        f"an account created through signup must be stored as {C.ROLE_READER}")
    stored_hash = row.get(C.FIELD_PASSWORD_HASH)
    assert stored_hash, f"{email} must be stored with a password hash"
    assert stored_hash != C.SEEDED_PASSWORD, (
        "the stored password must be hashed, never the clear literal")


def test_statistics_read_returns_the_five_seeded_rows_in_order(anonymous, backend):
    """The band answers five statistics with their captions and measurement dates."""
    payload = C.read_list(anonymous, C.STATISTICS_PATH)
    assert len(payload) == len(C.STATISTICS), (
        f"the band must answer {len(C.STATISTICS)} statistics, found {len(payload)}")
    for index, (qualifier, value, caption, measured) in enumerate(C.STATISTICS):
        row = payload[index]
        assert row.get(C.FIELD_POSITION) == index + 1, (
            f"statistic {index + 1} must carry position {index + 1}")
        assert row.get(C.FIELD_QUALIFIER) == qualifier, (
            f"statistic {index + 1} must read the qualifier {qualifier!r}, "
            f"found {row.get(C.FIELD_QUALIFIER)!r}")
        assert row.get(C.FIELD_VALUE) == value, (
            f"statistic {index + 1} must read the value {value!r}, "
            f"found {row.get(C.FIELD_VALUE)!r}")
        assert row.get(C.FIELD_CAPTION) == caption, (
            f"statistic {index + 1} must read the caption {caption!r}")
        assert row.get(C.FIELD_MEASURED_ON) == measured, (
            f"statistic {index + 1} must read {measured!r}")
        stored = C.statistic_rows(backend, position=index + 1)
        assert len(stored) == 1, (
            f"position {index + 1} must exist as exactly one stored statistic row")


def test_capabilities_read_returns_the_eight_result_lines(anonymous, backend):
    """Eight capability modules answer with the outcome each states in words."""
    payload = C.read_list(anonymous, C.CAPABILITIES_PATH)
    assert len(payload) == len(C.CAPABILITY_RESULT_LINES), (
        f"the site must answer {len(C.CAPABILITY_RESULT_LINES)} capability modules, "
        f"found {len(payload)}")
    for index, expected in enumerate(C.CAPABILITY_RESULT_LINES):
        row = payload[index]
        assert row.get(C.FIELD_POSITION) == index + 1, (
            f"capability {index + 1} must carry position {index + 1}")
        assert row.get(C.FIELD_RESULT_LINE) == expected, (
            f"capability {index + 1} must state {expected!r}, "
            f"found {row.get(C.FIELD_RESULT_LINE)!r}")
        assert row.get(C.FIELD_CLAIM), (
            f"capability {index + 1} must carry the claim it argues")
        stored = C.capability_rows(backend, position=index + 1)
        assert len(stored) == 1, (
            f"capability position {index + 1} must exist as exactly one stored row")


def test_services_read_returns_the_thirty_two_catalogue_rows(anonymous, backend):
    """The catalogue answers thirty-two services across the four named families."""
    payload = C.read_list(anonymous, C.SERVICES_PATH)
    assert len(payload) == C.SERVICE_TOTAL, (
        f"the catalogue must answer {C.SERVICE_TOTAL} services, found {len(payload)}")
    counts = {}
    for row in payload:
        counts[row.get(C.FIELD_FAMILY)] = counts.get(row.get(C.FIELD_FAMILY), 0) + 1
    assert counts == C.FAMILY_COUNTS, (
        f"the four families must hold {C.FAMILY_COUNTS}, found {counts}")
    blurbs = {row.get(C.FIELD_NAME): row.get(C.FIELD_BLURB) for row in payload}
    for name, blurb in C.SAMPLED_SERVICES.items():
        assert blurbs.get(name) == blurb, (
            f"the service {name!r} must read the description {blurb!r}, "
            f"found {blurbs.get(name)!r}")
    stored = C.service_rows(backend)
    assert len(stored) == C.SERVICE_TOTAL, (
        f"{C.SERVICE_TOTAL} service rows must be stored, found {len(stored)}")


def test_services_read_narrows_to_one_family(anonymous):
    """A family query answers only that family, in its own order."""
    payload = C.read_list(
        anonymous, f"{C.SERVICES_PATH}?{C.PARAM_FAMILY}={C.FAMILY_SECURITY.replace(' ', '%20')}")
    families = {row.get(C.FIELD_FAMILY) for row in payload}
    assert families == {C.FAMILY_SECURITY}, (
        f"a narrowed read must answer only {C.FAMILY_SECURITY!r}, found {families}")
    assert len(payload) == C.FAMILY_COUNTS[C.FAMILY_SECURITY], (
        f"{C.FAMILY_SECURITY} must answer {C.FAMILY_COUNTS[C.FAMILY_SECURITY]} rows, "
        f"found {len(payload)}")
    positions = [row.get(C.FIELD_POSITION) for row in payload]
    assert positions == sorted(positions), (
        f"a narrowed family must answer in position order, found {positions}")


def test_seeded_article_rows_carry_their_pinned_fields(backend):
    """Every seeded article is stored with its pinned slug, title and visibility."""
    for slug, (title, visibility, owner) in C.SEEDED_ARTICLES.items():
        row = C.article_row_by_slug(backend, slug)
        assert row is not None, f"{slug} must exist as exactly one stored article row"
        assert row.get(C.FIELD_TITLE) == title, (
            f"{slug} must be stored with the title {title!r}, "
            f"found {row.get(C.FIELD_TITLE)!r}")
        assert row.get(C.FIELD_VISIBILITY) == visibility, (
            f"{slug} must be stored at visibility {visibility}, "
            f"found {row.get(C.FIELD_VISIBILITY)}")
        owner_row = C.account_row(backend, owner)
        assert owner_row is not None, f"{owner} must exist for {slug} to belong to"
        assert row.get(C.FIELD_AUTHOR_ID) == owner_row.get(C.FIELD_ID), (
            f"{slug} must belong to {owner}")
        if visibility == C.VISIBILITY_DRAFT:
            assert not row.get(C.FIELD_PUBLISHED_AT), (
                f"{slug} is a draft, so it must carry no published date")
        else:
            assert row.get(C.FIELD_PUBLISHED_AT), (
                f"{slug} is published, so it must carry a published date")
    assert len(C.article_rows(backend)) == len(C.SEEDED_ARTICLES), (
        f"exactly {len(C.SEEDED_ARTICLES)} seeded articles may be stored")


def test_seeding_is_idempotent_across_every_seeded_table(backend):
    """Every seeded table holds its own rows once, so a restart duplicates nothing."""
    assert len(C.account_rows(backend)) >= 3, (
        "the three seeded accounts must be stored")
    assert len(C.statistic_rows(backend)) == len(C.STATISTICS), (
        "the statistics table must hold exactly the seeded rows")
    assert len(C.capability_rows(backend)) == len(C.CAPABILITY_RESULT_LINES), (
        "the capability table must hold exactly the seeded rows")
    assert len(C.service_rows(backend)) == C.SERVICE_TOTAL, (
        "the service table must hold exactly the seeded rows")
    assert len(backend.rows(C.TABLE_PRESS)) == 3, (
        "three press releases must be stored")
    assert len(backend.rows(C.TABLE_EVENT)) == 3, "three events must be stored"
    assert len(backend.rows(C.TABLE_PARTNER)) == len(C.PARTNER_TIERS), (
        f"{len(C.PARTNER_TIERS)} partner tiers must be stored")


def test_press_events_and_partner_tiers_read_their_seeded_rows(anonymous):
    """The three secondary reads answer their seeded rows with their own fields."""
    press = C.read_list(anonymous, C.PRESS_PATH)
    assert len(press) == 3, f"the press route must answer 3 releases, found {len(press)}"
    dates = [row.get(C.FIELD_DATED_ON) for row in press]
    assert dates == sorted(dates, reverse=True), (
        f"press releases must answer newest first, found {dates}")
    for row in press:
        assert row.get(C.FIELD_HEADLINE), "every release must carry a headline"
        assert row.get(C.FIELD_SUMMARY), "every release must carry a summary"
    events = C.read_list(anonymous, C.EVENTS_PATH)
    assert len(events) == 3, f"the events route must answer 3 events, found {len(events)}"
    starts = [row.get(C.FIELD_STARTS_ON) for row in events]
    assert starts == sorted(starts), (
        f"events must answer soonest first, found {starts}")
    for row in events:
        assert row.get(C.FIELD_PLACE), "every event must carry a place"
        assert row.get(C.FIELD_REGISTRATION_NOTE), (
            "every event must carry a registration note")
    tiers = C.read_list(anonymous, C.PARTNER_TIERS_PATH)
    assert [row.get(C.FIELD_NAME) for row in tiers] == list(C.PARTNER_TIERS), (
        f"the partner tiers must answer {list(C.PARTNER_TIERS)}")


def test_article_index_lists_only_published_articles_newest_first(anonymous):
    """The index answers the three published articles and never a draft."""
    payload = read_index_or_fail(anonymous)
    slugs = C.index_slugs(payload)
    assert set(slugs) == set(C.PUBLISHED_SLUGS), (
        f"the index must answer exactly {sorted(C.PUBLISHED_SLUGS)}, found {sorted(slugs)}")
    for slug in C.DRAFT_SLUGS:
        assert slug not in slugs, f"the draft {slug} must never appear in the index"
    dates = [row.get(C.FIELD_PUBLISHED_AT) for row in payload]
    assert dates == sorted(dates, reverse=True), (
        f"the index must answer newest first, found {dates}")


def read_index_or_fail(client):
    return C.read_index(client)


def test_open_article_read_returns_its_body_to_anybody(anonymous):
    """An open article answers its whole record with no session at all."""
    body = C.read_article(anonymous, C.SLUG_MODERN_CDN)
    assert body.get(C.FIELD_TITLE) == C.TITLE_MODERN_CDN, (
        f"{C.SLUG_MODERN_CDN} must read the title {C.TITLE_MODERN_CDN!r}")
    assert body.get(C.FIELD_BODY), "an open article must answer with its body"
    assert body.get(C.FIELD_EXCERPT), "an open article must answer with its excerpt"
    assert body.get(C.FIELD_CATEGORY), "an open article must answer with its category"
    assert body.get(C.FIELD_AUTHOR_NAME) == C.AUTHOR_NAME, (
        f"{C.SLUG_MODERN_CDN} must name {C.AUTHOR_NAME} as its author")
    assert body.get(C.FIELD_PUBLISHED_AT), (
        "an open article must answer with its published date")


def test_members_article_withholds_its_body_from_a_visitor(anonymous):
    """A members article answers its opening to a visitor and withholds its body."""
    body = C.read_article(anonymous, C.SLUG_SECURITY_REPORT)
    assert body.get(C.FIELD_TITLE) == C.TITLE_SECURITY_REPORT, (
        f"{C.SLUG_SECURITY_REPORT} must read its title to a visitor")
    assert body.get(C.FIELD_EXCERPT), (
        "a members article must answer its excerpt to a visitor")
    assert not body.get(C.FIELD_BODY), (
        f"a members article must withhold its body from a visitor, "
        f"found {str(body.get(C.FIELD_BODY))[:120]!r}")


def test_members_article_body_is_served_to_a_signed_in_reader(reader):
    """The same members article answers its body once a reader is signed in."""
    body = C.read_article(reader, C.SLUG_SECURITY_REPORT)
    assert body.get(C.FIELD_BODY), (
        "a signed-in reader must be answered the members article body")


def test_search_reaches_articles_services_and_routes(anonymous):
    """A query answers matching published articles, services and marketing routes."""
    response = anonymous.get(C.SEARCH_PATH, params={C.PARAM_QUERY: "edge"})
    assert response.status_code == 200, C.describe(
        response, "a search must answer with its ranked results")
    payload = response.json()
    assert isinstance(payload, list), C.describe(
        response, "a search must return a top-level JSON array")
    assert payload, "a search for a word the site uses must answer at least one result"
    for row in payload:
        assert row.get(C.FIELD_TITLE), "every result must carry a title"
        assert row.get(C.FIELD_PATH), "every result must carry the address it leads to"
        assert C.FIELD_EXCERPT in row, "every result must carry a short extract"


def test_search_never_returns_a_draft_to_anybody(anonymous, author):
    """No query answers a draft, to a visitor or to the author who owns it."""
    for client in (anonymous, author):
        response = client.get(C.SEARCH_PATH,
                              params={C.PARAM_QUERY: C.TITLE_PURGE_PATH})
        assert response.status_code == 200, C.describe(
            response, "a search must answer even when nothing matches")
        paths = [row.get(C.FIELD_PATH, "") for row in response.json()]
        assert not any(C.SLUG_PURGE_PATH in str(path) for path in paths), (
            f"no search may answer the draft {C.SLUG_PURGE_PATH}, found {paths}")
    empty = anonymous.get(C.SEARCH_PATH, params={C.PARAM_QUERY: "zzqqxx-nothing"})
    assert empty.status_code == 200, C.describe(
        empty, "a search matching nothing must still answer")
    assert empty.json() == [], C.describe(
        empty, "a search matching nothing must answer an empty array")


def test_unknown_address_answers_not_found(anonymous, suffix):
    """An address the app does not have answers not-found rather than a soft page."""
    response = anonymous.get(C.article_path(f"no-such-article-{suffix}"))
    assert response.status_code == 404, C.describe(
        response, "an address matching no article must answer not-found")


def test_cover_upload_lands_in_the_object_store_under_its_key(author, store, backend,
                                                              suffix):
    """An attached cover is a real object in the bucket at its scheme's key."""
    created = C.create_article(author, suffix)
    article_id = created[C.FIELD_ID]
    try:
        payload = C.probe_cover_bytes(suffix)
        response = C.upload_cover(author, article_id, payload, suffix)
        assert response.status_code in (200, 201), C.describe(
            response, "an author must be able to attach a cover to an owned article")
        key = response.json().get(C.FIELD_COVER_KEY)
        assert key == C.expected_cover_key(article_id, payload), (
            f"the stored cover key must be "
            f"{C.expected_cover_key(article_id, payload)}, found {key}")
        assert store.exists(key), (
            f"the cover bytes must live in the bucket at {key}")
        row = C.article_row_by_slug(backend, C.probe_slug(suffix))
        assert row.get(C.FIELD_COVER_KEY) == key, (
            f"the article record must hold the object key {key}")
    finally:
        C.remove_article(author, article_id)


def test_replacing_a_cover_stores_a_second_object_and_repoints_the_article(author,
                                                                          store,
                                                                          backend,
                                                                          suffix):
    """A replaced cover is a new object at a new key, and the article follows it."""
    created = C.create_article(author, suffix)
    article_id = created[C.FIELD_ID]
    try:
        first = C.probe_cover_bytes(suffix)
        second = first + b"-replaced"
        C.upload_cover(author, article_id, first, suffix)
        response = C.upload_cover(author, article_id, second, suffix)
        assert response.status_code in (200, 201), C.describe(
            response, "an author must be able to replace a cover")
        new_key = response.json().get(C.FIELD_COVER_KEY)
        assert new_key == C.expected_cover_key(article_id, second), (
            f"the replacement must be stored at "
            f"{C.expected_cover_key(article_id, second)}, found {new_key}")
        assert store.exists(new_key), "the replacement bytes must live in the bucket"
        row = C.article_row_by_slug(backend, C.probe_slug(suffix))
        assert row.get(C.FIELD_COVER_KEY) == new_key, (
            "the article record must hold the replacement key")
    finally:
        C.remove_article(author, article_id)


def test_published_article_cover_streams_to_an_anonymous_caller(author, anonymous,
                                                                suffix):
    """A published cover is streamed by the app to anybody who asks for it."""
    created = C.create_article(author, suffix)
    article_id = created[C.FIELD_ID]
    try:
        payload = C.probe_cover_bytes(suffix)
        C.upload_cover(author, article_id, payload, suffix)
        C.set_visibility(author, article_id, C.VISIBILITY_OPEN)
        response = anonymous.get(C.cover_path(article_id))
        assert response.status_code == 200, C.describe(
            response, "a published cover must stream to a caller with no session")
        assert response.content == payload, C.describe(
            response, "the streamed cover must be the bytes that were stored")
        assert "minio" not in response.text[:200].lower(), C.describe(
            response, "the cover must be streamed by the app, not redirected to the store")
    finally:
        C.remove_article(author, article_id)


def test_publishing_records_the_published_date_and_unpublishing_clears_it(author,
                                                                         anonymous,
                                                                         backend,
                                                                         suffix):
    """Visibility drives the published date and the article's public reachability."""
    created = C.create_article(author, suffix)
    article_id = created[C.FIELD_ID]
    slug = C.probe_slug(suffix)
    try:
        row = C.article_row_by_slug(backend, slug)
        assert not row.get(C.FIELD_PUBLISHED_AT), (
            "a draft must be stored with no published date")
        response = C.set_visibility(author, article_id, C.VISIBILITY_OPEN)
        assert response.status_code in (200, 201), C.describe(
            response, "an author must be able to publish an owned article")
        row = C.article_row_by_slug(backend, slug)
        assert row.get(C.FIELD_PUBLISHED_AT), (
            "publishing must record the published date")
        assert slug in C.index_slugs(C.read_index(anonymous)), (
            f"{slug} must appear in the public index once published")
        C.set_visibility(author, article_id, C.VISIBILITY_DRAFT)
        row = C.article_row_by_slug(backend, slug)
        assert not row.get(C.FIELD_PUBLISHED_AT), (
            "returning to draft must clear the published date")
        assert slug not in C.index_slugs(C.read_index(anonymous)), (
            f"{slug} must leave the public index when it returns to draft")
    finally:
        C.remove_article(author, article_id)


def test_cookie_choice_is_stored_once_per_visitor_key(anonymous, backend, suffix):
    """A visitor's answer is stored against their key and a second answer replaces it."""
    key = f"probe-visitor-{suffix}"
    first = anonymous.post(C.COOKIE_PATH,
                           json={C.FIELD_VISITOR_KEY: key, C.FIELD_ACCEPTED: True})
    assert first.status_code in (200, 201), C.describe(
        first, "a visitor must be able to record a cookie choice")
    read = anonymous.get(C.COOKIE_PATH, params={C.FIELD_VISITOR_KEY: key})
    assert read.status_code == 200, C.describe(
        read, "a recorded cookie choice must be readable back")
    assert read.json().get(C.FIELD_ACCEPTED) is True, C.describe(
        read, "the recorded choice must survive the read")
    second = anonymous.post(C.COOKIE_PATH,
                            json={C.FIELD_VISITOR_KEY: key, C.FIELD_ACCEPTED: False})
    assert second.status_code in (200, 201), C.describe(
        second, "a visitor may change a recorded cookie choice")
    rows = C.cookie_rows(backend, visitor_key=key)
    assert len(rows) == 1, (
        f"one visitor key must hold exactly one stored choice, found {len(rows)}")
    assert rows[0].get(C.FIELD_DECIDED_AT), (
        "a stored cookie choice must carry the moment it was decided")


def test_draft_article_is_denied_by_slug_to_every_other_caller(anonymous, reader,
                                                               author2, author):
    """A draft is refused by its own address to everybody but the owning author."""
    for client, who in ((anonymous, "a visitor"), (reader, "a reader"),
                        (author2, "another author")):
        response = client.get(C.article_path(C.SLUG_PURGE_PATH))
        assert C.is_denied(response), C.describe(
            response, f"{who} must be refused the draft {C.SLUG_PURGE_PATH}")
        assert C.TITLE_PURGE_PATH not in response.text, C.describe(
            response, f"a refusal must disclose nothing about {C.SLUG_PURGE_PATH}")
    owner = author.get(C.article_path(C.SLUG_PURGE_PATH))
    assert owner.status_code == 200, C.describe(
        owner, f"the owning author must be answered {C.SLUG_PURGE_PATH}")


def test_draft_article_is_denied_by_identifier_to_every_other_caller(anonymous,
                                                                    author2,
                                                                    author,
                                                                    backend):
    """A draft is refused by its stored identifier as firmly as by its address."""
    row = C.article_row_by_slug(backend, C.SLUG_STREAMING_DIARY)
    assert row is not None, f"{C.SLUG_STREAMING_DIARY} must be stored to be refused"
    article_id = row[C.FIELD_ID]
    for client, who in ((anonymous, "a visitor"), (author, "the other author")):
        response = client.get(C.article_id_path(article_id))
        assert C.is_denied(response), C.describe(
            response, f"{who} must be refused the draft by its identifier")
    owner = author2.get(C.article_id_path(article_id))
    assert owner.status_code == 200, C.describe(
        owner, "the owning author must be answered its own draft by identifier")


def test_draft_cover_is_denied_to_every_other_caller(anonymous, author2, author,
                                                     store, backend, suffix):
    """A draft's cover is refused even to a caller who knows the object key."""
    created = C.create_article(author, suffix)
    article_id = created[C.FIELD_ID]
    try:
        payload = C.probe_cover_bytes(suffix)
        upload = C.upload_cover(author, article_id, payload, suffix)
        key = upload.json().get(C.FIELD_COVER_KEY)
        assert store.exists(key), "the draft cover must be stored to be refused"
        for client, who in ((anonymous, "a visitor"), (author2, "another author")):
            response = client.get(C.cover_path(article_id))
            assert C.is_denied(response), C.describe(
                response, f"{who} must be refused the cover of a draft")
        owner = author.get(C.cover_path(article_id))
        assert owner.status_code == 200, C.describe(
            owner, "the owning author must be streamed its own draft cover")
    finally:
        C.remove_article(author, article_id)


def test_desk_list_returns_only_the_signed_in_authors_own_articles(author, author2):
    """Each desk answers its owner's articles, drafts included, and nobody else's."""
    mine = C.read_list(author, C.DESK_ARTICLES_PATH)
    slugs = {row.get(C.FIELD_SLUG) for row in mine}
    assert C.SLUG_PURGE_PATH in slugs, (
        f"the desk must answer the owner's draft {C.SLUG_PURGE_PATH}")
    assert C.SLUG_STREAMING_DIARY not in slugs, (
        f"the desk must not answer another author's draft {C.SLUG_STREAMING_DIARY}")
    theirs = C.read_list(author2, C.DESK_ARTICLES_PATH)
    other = {row.get(C.FIELD_SLUG) for row in theirs}
    assert C.SLUG_STREAMING_DIARY in other, (
        f"the second desk must answer its own draft {C.SLUG_STREAMING_DIARY}")
    assert C.SLUG_PURGE_PATH not in other, (
        f"the second desk must not answer {C.SLUG_PURGE_PATH}")


def test_reader_cannot_reach_the_desk_list(reader):
    """A reader session is refused every desk address by the server."""
    response = reader.get(C.DESK_ARTICLES_PATH)
    assert C.is_denied(response), C.describe(
        response, "a reader must be refused the desk list by the server")
    write = reader.post(C.ARTICLES_PATH, json=C.article_payload("reader"))
    assert C.is_denied(write), C.describe(
        write, "a reader must be refused the article write endpoint")


def test_anonymous_desk_request_is_denied(anonymous):
    """A caller with no session is refused the desk list and the article write."""
    response = anonymous.get(C.DESK_ARTICLES_PATH)
    assert C.is_denied(response), C.describe(
        response, "a caller with no session must be refused the desk list")
    write = anonymous.post(C.ARTICLES_PATH, json=C.article_payload("anonymous"))
    assert C.is_denied(write), C.describe(
        write, "a caller with no session must be refused the article write")


def test_author_cannot_edit_another_authors_article(author2, backend):
    """A write aimed at another author's article is refused and changes nothing."""
    row = C.article_row_by_slug(backend, C.SLUG_PURGE_PATH)
    assert row is not None, f"{C.SLUG_PURGE_PATH} must be stored to be protected"
    before = row.get(C.FIELD_VISIBILITY)
    response = C.set_visibility(author2, row[C.FIELD_ID], C.VISIBILITY_OPEN)
    assert C.is_denied(response), C.describe(
        response, "an author must be refused a write on another author's article")
    after = C.article_row_by_slug(backend, C.SLUG_PURGE_PATH)
    assert after.get(C.FIELD_VISIBILITY) == before, (
        f"{C.SLUG_PURGE_PATH} must still be stored at {before} after a refused write")


def test_signup_never_creates_an_author_whatever_the_body_asks(anonymous, backend,
                                                               suffix):
    """A signup body naming the author role still stores a reader."""
    email = C.probe_email(suffix)
    response = anonymous.post(C.SIGNUP_PATH, json={
        C.FIELD_EMAIL: email,
        C.FIELD_PASSWORD: C.SEEDED_PASSWORD,
        C.FIELD_ROLE: C.ROLE_AUTHOR,
    })
    assert response.status_code in (200, 201), C.describe(
        response, "signup must accept a well-formed work address")
    account = response.json().get(C.FIELD_ACCOUNT) or {}
    assert account.get(C.FIELD_ROLE) == C.ROLE_READER, C.describe(
        response, "a signup must answer with the reader role however the body reads")
    row = C.account_row(backend, email)
    assert row.get(C.FIELD_ROLE) == C.ROLE_READER, (
        f"{email} must be stored as {C.ROLE_READER}, found {row.get(C.FIELD_ROLE)}")
    assert len(C.account_rows(backend, role=C.ROLE_AUTHOR)) == 2, (
        "only the two seeded accounts may carry the author role")


def test_signed_out_token_is_no_longer_accepted(suffix):
    """A token stops being accepted the moment its holder signs out."""
    token = C.sign_up_probe_reader(suffix)
    with appclient.client(token) as signed_in:
        before = signed_in.get(C.ME_PATH)
        assert before.status_code == 200, C.describe(
            before, "a fresh token must be accepted")
        signed_in.post(f"{C.LOGIN_PATH.rsplit('/', 1)[0]}/logout")
    with appclient.client(token) as reused:
        after = reused.get(C.ME_PATH)
    assert C.is_denied(after), C.describe(
        after, "a token must stop being accepted once its holder has signed out")


def test_consumer_mailbox_signup_is_refused_and_stores_no_account(anonymous, backend,
                                                                  suffix):
    """Each named consumer mailbox is refused and no account is written."""
    for domain in C.REFUSED_MAILBOXES:
        email = f"probe-{suffix}@{domain}"
        response = anonymous.post(C.SIGNUP_PATH, json={
            C.FIELD_EMAIL: email, C.FIELD_PASSWORD: C.SEEDED_PASSWORD})
        assert C.is_client_error(response), C.describe(
            response, f"a signup at {domain} must be refused as invalid")
        assert C.FIELD_EMAIL in response.text.lower(), C.describe(
            response, "a refused signup must name the email field")
        assert C.account_row(backend, email) is None, (
            f"a refused signup at {domain} must store no account")


def test_duplicate_email_signup_is_refused_and_stores_no_second_account(anonymous,
                                                                       backend,
                                                                       suffix):
    """A second signup on one address is refused and leaves one stored account."""
    email = C.probe_email(suffix)
    first = anonymous.post(C.SIGNUP_PATH, json={
        C.FIELD_EMAIL: email, C.FIELD_PASSWORD: C.SEEDED_PASSWORD})
    assert first.status_code in (200, 201), C.describe(
        first, "the first signup on a fresh address must be accepted")
    second = anonymous.post(C.SIGNUP_PATH, json={
        C.FIELD_EMAIL: email, C.FIELD_PASSWORD: C.SEEDED_PASSWORD})
    assert C.is_client_error(second), C.describe(
        second, "a second signup on the same address must be refused as invalid")
    assert C.FIELD_EMAIL in second.text.lower(), C.describe(
        second, "a refused duplicate signup must name the email field")
    assert len(C.account_rows(backend, email=email)) == 1, (
        f"{email} must be stored exactly once")


def test_wrong_password_login_is_denied_without_a_token(anonymous):
    """A login with the wrong password is denied and hands back no token."""
    response = anonymous.post(C.LOGIN_PATH, json={
        C.FIELD_EMAIL: C.READER_EMAIL, C.FIELD_PASSWORD: "not-the-corpus-password"})
    assert C.is_client_error(response), C.describe(
        response, "a login with the wrong password must be denied")
    assert C.TOKEN_FIELD not in response.text, C.describe(
        response, "a denied login must hand back no access_token")


def test_duplicate_slug_is_refused_and_stores_no_second_article(author, backend,
                                                                suffix):
    """A slug another article already holds is refused and nothing is written."""
    response = author.post(C.ARTICLES_PATH, json=C.article_payload(
        suffix, **{C.FIELD_SLUG: C.SLUG_MODERN_CDN}))
    assert C.is_client_error(response), C.describe(
        response, f"a write reusing the slug {C.SLUG_MODERN_CDN} must be refused")
    assert C.FIELD_SLUG in response.text.lower(), C.describe(
        response, "a refused duplicate slug must name the slug field")
    assert len(C.article_rows(backend, slug=C.SLUG_MODERN_CDN)) == 1, (
        f"{C.SLUG_MODERN_CDN} must remain exactly one stored article")


def test_article_missing_a_required_field_is_refused_and_stores_nothing(author,
                                                                        backend,
                                                                        suffix):
    """A write with no title, no body or an unknown visibility is refused."""
    cases = (
        (C.FIELD_TITLE, {C.FIELD_TITLE: ""}),
        (C.FIELD_BODY, {C.FIELD_BODY: ""}),
        (C.FIELD_VISIBILITY, {C.FIELD_VISIBILITY: "archived"}),
    )
    for field, override in cases:
        response = author.post(C.ARTICLES_PATH,
                               json=C.article_payload(suffix, **override))
        assert C.is_client_error(response), C.describe(
            response, f"a write with a bad {field} must be refused as invalid")
        assert field in response.text.lower(), C.describe(
            response, f"a refused write must name the {field} field")
    assert C.article_rows(backend, slug=C.probe_slug(suffix)) == [], (
        "a refused write must store no article")
