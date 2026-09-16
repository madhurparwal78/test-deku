"""Deterministic observations of the deployed Milo Rennick Brand Platform app.

Every assertion is black box: the app is driven over HTTP on its own origin,
and the two backing services are read through the shared capability adapters.
Nothing here reads the agent's source, its schema, or its file layout.
"""

from __future__ import annotations

import conftest as fx


def _new_story(http, slug, title="The Long Way Round", kind="story",
               attribution=None):
    body = {
        "slug": slug,
        "title": title,
        "type": kind,
        "body": "A generated probe story used to exercise the publish path.",
    }
    if attribution is not None:
        body["attribution"] = attribution
    return http.post("/studio/stories", json=body)


def _ingest(http, run_id, entities):
    return http.post("/studio/ingest", json={"runId": run_id, "entities": entities})


def _race_row(round_number, position, status, instant, provisional=False):
    return {
        "type": "classification",
        "roundNumber": round_number,
        "sessionKind": "race",
        "position": position,
        "status": status,
        "provisional": provisional,
        "providerUpdatedAt": instant,
    }


def test_health_endpoint_returns_ok(anon):
    """The app answers its health route once both backing services are reachable."""
    response = anon.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:300]}"
    )


def test_seeded_accounts_sign_in_with_corpus_password(anon):
    """All four seeded accounts sign in with the pinned password and carry a role."""
    for email, role in ((fx.OWNER_EMAIL, fx.OWNER_ROLE),
                        (fx.EDITOR_EMAIL, fx.EDITOR_ROLE),
                        (fx.CONTRIBUTOR_EMAIL, fx.CONTRIBUTOR_ROLE),
                        (fx.VISITOR_EMAIL, fx.VISITOR_ROLE)):
        response = anon.post("/auth/login", json={"email": email,
                                                  "password": fx.CORPUS_PASSWORD})
        assert response.status_code == 200, (
            f"login for {email} returned {response.status_code}: {response.text[:300]}"
        )
        body = response.json()
        assert body.get("access_token"), f"login for {email} returned no access_token"
        assert body.get("role") == role, (
            f"login for {email} reported role {body.get('role')!r}, expected {role!r}"
        )


def test_signup_creates_a_visitor_account(anon):
    """Open registration always produces a visitor, never a team role."""
    email = f"probe-{fx.unique_token()}@example.com"
    response = anon.post("/auth/signup", json={"email": email,
                                               "password": fx.CORPUS_PASSWORD})
    assert response.status_code in fx.CREATED, (
        f"signup returned {response.status_code}: {response.text[:300]}"
    )
    assert response.json().get("role") == fx.VISITOR_ROLE, (
        f"signup produced role {response.json().get('role')!r}, expected "
        f"{fx.VISITOR_ROLE!r}"
    )


def test_public_story_list_holds_only_public_stories(anon):
    """The public list carries the three published ids and none of the other three."""
    response = anon.get("/stories")
    assert response.status_code == 200, (
        f"GET /api/stories returned {response.status_code}: {response.text[:300]}"
    )
    payload = response.json()
    assert isinstance(payload, list), "GET /api/stories must return a JSON array"
    ids = fx.public_ids(payload)
    for public_id in fx.PUBLIC_STORY_IDS:
        assert public_id in ids, f"published story {public_id!r} is absent from the list"
    for public_id in fx.NON_PUBLIC_STORY_IDS:
        assert public_id not in ids, (
            f"story {public_id!r} is not public yet appears on the public list"
        )


def test_public_story_count_matches_the_public_list(anon):
    """The public story count is computed from the rows rather than stored."""
    response = anon.get("/stories/count")
    assert response.status_code == 200, (
        f"GET /api/stories/count returned {response.status_code}"
    )
    reported = response.json().get("count")
    listed = len(anon.get("/stories").json())
    assert reported == listed, (
        f"the count endpoint reports {reported} while the list carries {listed}"
    )
    assert reported >= fx.PUBLIC_STORY_COUNT, (
        f"the count endpoint reports {reported}, below the {fx.PUBLIC_STORY_COUNT} "
        f"seeded public stories"
    )


def test_public_story_order_is_newest_publication_first(anon):
    """The public list is ordered by publication instant, newest first."""
    payload = anon.get("/stories").json()
    stamps = [row.get("publishedAt") for row in payload]
    assert all(value for value in stamps), (
        f"every public story carries publishedAt; got {stamps}"
    )
    assert stamps == sorted(stamps, reverse=True), (
        f"public story publishedAt values are not newest first: {stamps}"
    )


def test_scheduled_story_detail_is_refused_to_anonymous(anon):
    """A story that is not public is refused by public id with no session."""
    for public_id in fx.NON_PUBLIC_STORY_IDS:
        response = anon.get(f"/stories/{public_id}")
        assert response.status_code in fx.DENIED_OR_ABSENT, (
            f"anonymous GET /api/stories/{public_id} returned {response.status_code}"
        )
        assert public_id not in response.text, (
            f"the refusal for {public_id!r} still discloses the public id"
        )


def test_scheduled_story_detail_is_refused_to_visitor(visitor):
    """A story that is not public is refused by public id to a signed-in visitor."""
    for public_id in fx.NON_PUBLIC_STORY_IDS:
        response = visitor.get(f"/stories/{public_id}")
        assert response.status_code in fx.DENIED_OR_ABSENT, (
            f"visitor GET /api/stories/{public_id} returned {response.status_code}"
        )


def test_seeded_photograph_objects_exist_in_the_store(editor, store):
    """Every seeded story, the non-public ones too, has a real object in the bucket."""
    keys = set(store.list(fx.ASSET_KEY_PREFIX))
    assert keys, (
        f"the bucket holds no object under {fx.ASSET_KEY_PREFIX!r}; seeded photographs "
        f"must be real objects rather than local files"
    )
    console = editor.get("/studio/stories")
    assert console.status_code == 200, (
        f"GET /api/studio/stories returned {console.status_code}"
    )
    rows = {row["publicId"]: row for row in console.json()}
    for public_id in fx.SEEDED_STORY_IDS:
        assert public_id in rows, f"seeded story {public_id!r} is absent from the workspace"
        assets = rows[public_id].get("assets") or []
        assert assets, f"seeded story {public_id!r} carries no gallery asset"
        stored = [a.get("storageKey") for a in assets if a.get("storageKey")]
        assert stored, f"seeded story {public_id!r} carries no storageKey on any asset"
        assert any(key in keys for key in stored), (
            f"seeded story {public_id!r} names keys {stored!r}, none of which is in the bucket"
        )


def test_public_story_photograph_is_served_to_anonymous(anon):
    """A published story's stored photograph is readable without a session."""
    story = anon.get(f"/stories/{fx.PUBLIC_STORY_IDS[0]}")
    assert story.status_code == 200, (
        f"GET /api/stories/{fx.PUBLIC_STORY_IDS[0]} returned {story.status_code}"
    )
    assets = story.json().get("assets") or []
    assert assets, "the published story carries no gallery asset"
    asset_id = assets[0].get("id")
    assert asset_id, "the published story asset carries no id"
    response = anon.get(f"/assets/{asset_id}/file")
    assert response.status_code == 200, (
        f"the public photograph route returned {response.status_code}"
    )
    assert len(response.content) > 0, "the public photograph route returned no bytes"


def test_non_public_photograph_bytes_are_refused_to_anonymous(anon, editor):
    """The photograph route returns no bytes and no redirect without a session."""
    rows = {r["publicId"]: r for r in editor.get("/studio/stories").json()}
    asset_id = (rows[fx.SCHEDULED_STORY_ID].get("assets") or [{}])[0].get("id")
    assert asset_id, (
        f"the scheduled story {fx.SCHEDULED_STORY_ID!r} carries no gallery asset to refuse"
    )
    response = anon.get(f"/assets/{asset_id}/file", follow_redirects=False)
    assert response.status_code in fx.DENIED_OR_ABSENT, (
        f"anonymous request for a non-public photograph returned {response.status_code}"
    )
    assert "location" not in {k.lower() for k in response.headers}, (
        "the refusal redirected the caller to the object store"
    )


def test_non_public_photograph_bytes_are_refused_to_visitor(visitor, editor, store):
    """The photograph route refuses a signed-in visitor while the object survives."""
    rows = {r["publicId"]: r for r in editor.get("/studio/stories").json()}
    asset_id = (rows[fx.DRAFT_STORY_ID].get("assets") or [{}])[0].get("id")
    assert asset_id, (
        f"the draft story {fx.DRAFT_STORY_ID!r} carries no gallery asset to refuse"
    )
    response = visitor.get(f"/assets/{asset_id}/file", follow_redirects=False)
    assert response.status_code in fx.DENIED_OR_ABSENT, (
        f"visitor request for a non-public photograph returned {response.status_code}"
    )
    assert store.list(fx.ASSET_KEY_PREFIX), (
        "the refusal removed or emptied the stored objects"
    )


def test_non_public_photograph_bytes_are_served_to_editor(editor):
    """The same non-public photograph is served to a signed-in editor."""
    rows = {r["publicId"]: r for r in editor.get("/studio/stories").json()}
    asset_id = (rows[fx.DRAFT_STORY_ID].get("assets") or [{}])[0].get("id")
    assert asset_id, f"the draft story {fx.DRAFT_STORY_ID!r} carries no gallery asset"
    response = editor.get(f"/assets/{asset_id}/file")
    assert response.status_code == 200, (
        f"editor request for a non-public photograph returned {response.status_code}"
    )
    assert len(response.content) > 0, "the editor received no photograph bytes"


def test_contributor_created_story_starts_as_draft(contributor, anon):
    """A newly created story is a draft and stays out of the public list."""
    slug = f"probe-story-{fx.unique_token()}"
    created = _new_story(contributor, slug)
    assert created.status_code in fx.CREATED, (
        f"POST /api/studio/stories returned {created.status_code}: {created.text[:300]}"
    )
    body = created.json()
    assert body.get("state") == fx.DRAFT_STATE, (
        f"a created story carries state {body.get('state')!r}, expected {fx.DRAFT_STATE!r}"
    )
    public_id = body.get("publicId")
    assert public_id, "the created story carries no publicId"
    assert public_id not in fx.public_ids(anon.get("/stories").json()), (
        f"the newly created draft {public_id!r} is already on the public list"
    )


def test_uploaded_photograph_lands_in_the_store_under_the_key_scheme(contributor, store):
    """An uploaded photograph becomes a real object under the pinned key scheme."""
    slug = f"probe-upload-{fx.unique_token()}"
    created = _new_story(contributor, slug)
    assert created.status_code in fx.CREATED, (
        f"POST /api/studio/stories returned {created.status_code}: {created.text[:300]}"
    )
    public_id = created.json().get("publicId")
    upload = contributor.post(
        f"/studio/stories/{public_id}/assets",
        files={"file": ("probe.png", fx.PNG_BYTES, "image/png")},
    )
    assert upload.status_code in fx.CREATED, (
        f"the photograph upload returned {upload.status_code}: {upload.text[:300]}"
    )
    key = upload.json().get("storageKey")
    assert key, "the upload response carries no storageKey"
    assert key.startswith(fx.ASSET_KEY_PREFIX), (
        f"the stored key {key!r} does not follow the assets/ key scheme"
    )
    assert fx.settle(lambda: store.exists(key)), (
        f"the uploaded bytes are not in the bucket at {key!r}"
    )


def test_duplicate_slug_create_is_refused(contributor, editor):
    """A create carrying a slug already taken leaves no second row behind."""
    slug = f"probe-dup-{fx.unique_token()}"
    first = _new_story(contributor, slug)
    assert first.status_code in fx.CREATED, (
        f"the first create returned {first.status_code}: {first.text[:300]}"
    )
    before = len(editor.get("/studio/stories").json())
    second = _new_story(contributor, slug, title="Duplicate Probe")
    assert second.status_code in fx.REFUSED_AS_INVALID, (
        f"a duplicate slug create returned {second.status_code}, expected a refusal"
    )
    after = editor.get("/studio/stories").json()
    assert len(after) == before, (
        f"the refused create left the story count at {len(after)}, was {before}"
    )
    assert "Duplicate Probe" not in [row.get("title") for row in after], (
        "the refused create still wrote a story row"
    )


def test_publishing_reveals_the_story_and_raises_the_count(contributor, editor, anon):
    """Publishing adds the story to the public list and moves the public count."""
    slug = f"probe-publish-{fx.unique_token()}"
    created = _new_story(contributor, slug)
    assert created.status_code in fx.CREATED, (
        f"POST /api/studio/stories returned {created.status_code}: {created.text[:300]}"
    )
    public_id = created.json().get("publicId")
    upload = contributor.post(
        f"/studio/stories/{public_id}/assets",
        files={"file": ("probe.png", fx.PNG_BYTES, "image/png")},
    )
    assert upload.status_code in fx.CREATED, (
        f"the photograph upload returned {upload.status_code}: {upload.text[:300]}"
    )
    asset_id = upload.json().get("assetId")
    assert asset_id, "the upload response carries no assetId"
    patched = contributor.patch(f"/studio/assets/{asset_id}",
                                json={"altText": "A probe photograph."})
    assert patched.status_code in fx.CREATED, (
        f"setting altText returned {patched.status_code}: {patched.text[:300]}"
    )
    before = anon.get("/stories/count").json()["count"]
    published = editor.post(f"/studio/stories/{public_id}/publish")
    assert published.status_code in fx.CREATED, (
        f"the publish call returned {published.status_code}: {published.text[:300]}"
    )
    assert published.json().get("state") == fx.PUBLISHED_STATE, (
        f"the published story carries state {published.json().get('state')!r}"
    )
    assert published.json().get("publishedAt"), "publishing stamped no publishedAt"
    after = anon.get("/stories/count").json()["count"]
    assert after == before + 1, (
        f"the public count moved from {before} to {after}, expected {before + 1}"
    )
    assert public_id in fx.public_ids(anon.get("/stories").json()), (
        f"the published story {public_id!r} is absent from the public list"
    )
    again = editor.post(f"/studio/stories/{public_id}/publish")
    assert again.status_code in fx.CREATED, (
        f"republishing returned {again.status_code}, which reads as an error"
    )
    assert anon.get("/stories/count").json()["count"] == after, (
        "republishing changed the public story count"
    )


def test_publish_is_blocked_when_a_photograph_has_no_alt_text(contributor, editor, anon):
    """Pre-publication validation refuses a story whose photograph has no alt text."""
    slug = f"probe-noalt-{fx.unique_token()}"
    created = _new_story(contributor, slug)
    assert created.status_code in fx.CREATED, (
        f"POST /api/studio/stories returned {created.status_code}: {created.text[:300]}"
    )
    public_id = created.json().get("publicId")
    upload = contributor.post(
        f"/studio/stories/{public_id}/assets",
        files={"file": ("probe.png", fx.PNG_BYTES, "image/png")},
    )
    assert upload.status_code in fx.CREATED, (
        f"the photograph upload returned {upload.status_code}: {upload.text[:300]}"
    )
    blocked = editor.post(f"/studio/stories/{public_id}/publish")
    assert blocked.status_code in fx.REFUSED_AS_INVALID, (
        f"publishing a story whose photograph has no alt text returned "
        f"{blocked.status_code}, expected a refusal"
    )
    assert public_id not in fx.public_ids(anon.get("/stories").json()), (
        f"the blocked story {public_id!r} reached the public list anyway"
    )


def test_contributor_cannot_publish_a_story(contributor, anon):
    """A publish issued from a contributor session is refused at the API."""
    slug = f"probe-denied-{fx.unique_token()}"
    created = _new_story(contributor, slug)
    assert created.status_code in fx.CREATED, (
        f"POST /api/studio/stories returned {created.status_code}: {created.text[:300]}"
    )
    public_id = created.json().get("publicId")
    response = contributor.post(f"/studio/stories/{public_id}/publish")
    assert response.status_code in fx.DENIED, (
        f"a contributor publish returned {response.status_code}, expected a denial"
    )
    assert public_id not in fx.public_ids(anon.get("/stories").json()), (
        f"the denied publish revealed {public_id!r} on the public list"
    )


def test_visitor_cannot_create_a_story(visitor, editor):
    """A story create issued from a visitor session is refused at the API."""
    before = len(editor.get("/studio/stories").json())
    slug = f"probe-visitor-{fx.unique_token()}"
    response = _new_story(visitor, slug)
    assert response.status_code in fx.DENIED, (
        f"a visitor create returned {response.status_code}, expected a denial"
    )
    assert len(editor.get("/studio/stories").json()) == before, (
        "the denied create still added a story row"
    )


def test_visitor_cannot_read_the_subscriber_list(visitor, anon):
    """The audience surface is refused to an anonymous caller and to a visitor."""
    for http, who in ((anon, "anonymous"), (visitor, "visitor")):
        response = http.get("/studio/subscribers")
        assert response.status_code in fx.DENIED_OR_ABSENT, (
            f"a {who} read of the subscriber list returned {response.status_code}"
        )
        assert "@" not in response.text[:2000], (
            f"the refused {who} read still disclosed an address"
        )


def test_editor_cannot_read_the_editor_list(editor, owner):
    """The editor roster is owner-only, and an editor session is refused."""
    refused = editor.get("/studio/editors")
    assert refused.status_code in fx.DENIED_OR_ABSENT, (
        f"an editor read of the roster returned {refused.status_code}, expected a denial"
    )
    allowed = owner.get("/studio/editors")
    assert allowed.status_code == 200, (
        f"an owner read of the roster returned {allowed.status_code}"
    )
    assert isinstance(allowed.json(), list), "GET /api/studio/editors must return an array"


def test_unpublishing_removes_the_story_from_public_reads(contributor, editor, anon):
    """Unpublishing takes the story off the public list and answers as absent."""
    slug = f"probe-unpub-{fx.unique_token()}"
    created = _new_story(contributor, slug)
    assert created.status_code in fx.CREATED, (
        f"POST /api/studio/stories returned {created.status_code}: {created.text[:300]}"
    )
    public_id = created.json().get("publicId")
    upload = contributor.post(
        f"/studio/stories/{public_id}/assets",
        files={"file": ("probe.png", fx.PNG_BYTES, "image/png")},
    )
    assert upload.status_code in fx.CREATED, (
        f"the photograph upload returned {upload.status_code}"
    )
    patched = contributor.patch(f"/studio/assets/{upload.json().get('assetId')}",
                                json={"altText": "A probe photograph."})
    assert patched.status_code in fx.CREATED, (
        f"setting altText returned {patched.status_code}"
    )
    published = editor.post(f"/studio/stories/{public_id}/publish")
    assert published.status_code in fx.CREATED, (
        f"the publish call returned {published.status_code}: {published.text[:300]}"
    )
    withdrawn = editor.post(f"/studio/stories/{public_id}/unpublish")
    assert withdrawn.status_code in fx.CREATED, (
        f"the unpublish call returned {withdrawn.status_code}: {withdrawn.text[:300]}"
    )
    assert withdrawn.json().get("state") == fx.UNPUBLISHED_STATE, (
        f"the withdrawn story carries state {withdrawn.json().get('state')!r}"
    )
    assert public_id not in fx.public_ids(anon.get("/stories").json()), (
        f"the unpublished story {public_id!r} is still on the public list"
    )
    gone = anon.get(f"/stories/{public_id}", follow_redirects=False)
    assert gone.status_code in fx.DENIED_OR_ABSENT, (
        f"the unpublished story answered {gone.status_code} rather than as absent"
    )


def test_story_public_ids_are_not_sequential(contributor):
    """Two stories created in a row carry public ids no counter reaches."""
    first = _new_story(contributor, f"probe-opaque-a-{fx.unique_token()}")
    second = _new_story(contributor, f"probe-opaque-b-{fx.unique_token()}")
    assert first.status_code in fx.CREATED, (
        f"the first create returned {first.status_code}: {first.text[:300]}"
    )
    assert second.status_code in fx.CREATED, (
        f"the second create returned {second.status_code}: {second.text[:300]}"
    )
    one = str(first.json().get("publicId"))
    two = str(second.json().get("publicId"))
    assert one and two, "a created story carries no publicId"
    assert one != two, "two created stories share one publicId"
    assert not (one.isdigit() and two.isdigit() and int(two) == int(one) + 1), (
        f"public ids {one!r} then {two!r} are consecutive integers, so the catalogue "
        f"can be walked by counting"
    )
    assert len(one) >= 8, (
        f"public id {one!r} is too short to be opaque against enumeration"
    )


def test_next_round_is_never_a_completed_round(anon):
    """The next round is computed and is never a round already run."""
    response = anon.get("/season/next-round")
    assert response.status_code == 200, (
        f"GET /api/season/next-round returned {response.status_code}"
    )
    upcoming = response.json()
    assert upcoming.get("state") not in fx.ROUND_CLOSED_STATES, (
        f"the next round carries state {upcoming.get('state')!r}, which is closed"
    )
    season = anon.get("/season")
    assert season.status_code == 200, f"GET /api/season returned {season.status_code}"
    rounds = season.json().get("rounds") or []
    assert len(rounds) >= fx.ROUND_COUNT, (
        f"the season carries {len(rounds)} rounds, expected at least {fx.ROUND_COUNT}"
    )
    done = [r["number"] for r in rounds if r.get("state") in fx.ROUND_CLOSED_STATES]
    assert done, "no seeded round is marked complete, so the season is not half run"
    assert upcoming.get("number") > max(done), (
        f"the next round is number {upcoming.get('number')} while round {max(done)} "
        f"is already complete"
    )
    assert upcoming.get("circuit") == fx.NEXT_ROUND_CIRCUIT, (
        f"the next round circuit is {upcoming.get('circuit')!r}, expected "
        f"{fx.NEXT_ROUND_CIRCUIT!r}"
    )


def test_season_rounds_carry_absolute_session_instants(anon):
    """Every seeded round carries its four session slots as absolute instants."""
    season = anon.get("/season").json()
    assert season.get("year") == fx.SEASON_YEAR, (
        f"the season year is {season.get('year')!r}, expected {fx.SEASON_YEAR}"
    )
    assert season.get("series") == fx.SERIES_NAME, (
        f"the series is {season.get('series')!r}, expected {fx.SERIES_NAME!r}"
    )
    circuits = [r.get("circuit") for r in season.get("rounds") or []]
    for circuit in fx.CIRCUITS:
        assert circuit in circuits, f"seeded circuit {circuit!r} is absent from the season"
    upcoming = anon.get("/season/next-round").json()
    kinds = [s.get("kind") for s in upcoming.get("sessions") or []]
    for kind in fx.SESSION_KINDS:
        assert kind in kinds, f"the next round carries no {kind!r} session"
    for slot in upcoming.get("sessions") or []:
        starts = str(slot.get("startsAt") or "")
        assert starts.endswith("Z") or "+" in starts[10:] or "-" in starts[10:], (
            f"session {slot.get('kind')!r} starts at {starts!r}, which carries no zone"
        )


def test_ingestion_run_replayed_is_a_duplicate_that_applies_nothing(editor):
    """Applying the same run identifier twice produces the same stored result."""
    run_id = f"probe-run-{fx.unique_token()}"
    entities = [_race_row(fx.COMPLETE_ROUND_NUMBERS[0], 3, "classified",
                          fx.INGEST_INSTANT_NEW)]
    first = _ingest(editor, run_id, entities)
    assert first.status_code in fx.CREATED, (
        f"the first ingestion run returned {first.status_code}: {first.text[:300]}"
    )
    assert first.json().get("duplicate") is False, (
        "a first run reported itself as a duplicate"
    )
    baseline = editor.get("/results").json()
    second = _ingest(editor, run_id, entities)
    assert second.status_code in fx.CREATED, (
        f"the replayed ingestion run returned {second.status_code}: {second.text[:300]}"
    )
    body = second.json()
    assert body.get("duplicate") is True, (
        f"the replayed run reported duplicate {body.get('duplicate')!r}"
    )
    assert body.get("applied") == 0, (
        f"the replayed run applied {body.get('applied')!r} entities, expected 0"
    )
    assert editor.get("/results").json() == baseline, (
        "the replayed run changed the stored results"
    )


def test_superseded_classification_never_moves_a_result_backwards(editor, anon):
    """An older provider instant is counted as superseded and changes nothing."""
    number = fx.COMPLETE_ROUND_NUMBERS[1]
    final = _ingest(editor, f"probe-final-{fx.unique_token()}",
                    [_race_row(number, 2, "classified", fx.INGEST_INSTANT_NEW)])
    assert final.status_code in fx.CREATED, (
        f"the final ingestion returned {final.status_code}: {final.text[:300]}"
    )
    after_final = [r for r in anon.get("/results").json()
                   if r.get("roundNumber") == number]
    assert after_final, f"round {number} carries no classification after ingestion"
    assert after_final[0].get("position") == 2, (
        f"the final classification stored position {after_final[0].get('position')!r}"
    )
    stale = _ingest(editor, f"probe-stale-{fx.unique_token()}",
                    [_race_row(number, 9, "classified", fx.INGEST_INSTANT_OLD,
                               provisional=True)])
    assert stale.status_code in fx.CREATED, (
        f"the stale ingestion returned {stale.status_code}: {stale.text[:300]}"
    )
    assert stale.json().get("superseded", 0) >= 1, (
        f"the stale run reported superseded {stale.json().get('superseded')!r}, "
        f"expected at least 1"
    )
    assert stale.json().get("applied") == 0, (
        f"the stale run applied {stale.json().get('applied')!r} entities, expected 0"
    )
    after_stale = [r for r in anon.get("/results").json()
                   if r.get("roundNumber") == number]
    assert after_stale[0].get("position") == 2, (
        f"a superseded delivery moved the stored position to "
        f"{after_stale[0].get('position')!r}"
    )
    assert after_stale[0].get("provisional") is False, (
        "a superseded delivery made a final classification provisional again"
    )


def test_missing_round_is_held_for_review_rather_than_deleted(editor, anon):
    """A round absent from a payload is marked for review, never removed."""
    before = {r["number"] for r in anon.get("/season").json().get("rounds") or []}
    assert before, "the season carries no rounds before the ingestion"
    run = _ingest(editor, f"probe-missing-{fx.unique_token()}",
                  [{"type": "round", "roundNumber": fx.SCHEDULED_ROUND_NUMBERS[0],
                    "state": "scheduled",
                    "providerUpdatedAt": fx.INGEST_INSTANT_NEW}])
    assert run.status_code in fx.CREATED, (
        f"the partial ingestion returned {run.status_code}: {run.text[:300]}"
    )
    assert run.json().get("missing", 0) >= 1, (
        f"a payload naming one round reported missing {run.json().get('missing')!r}"
    )
    after_rounds = anon.get("/season").json().get("rounds") or []
    after = {r["number"] for r in after_rounds}
    assert before <= after, (
        f"the ingestion deleted rounds {sorted(before - after)} rather than holding them"
    )
    flagged = [r for r in after_rounds if r.get("state") == fx.MISSING_ROUND_STATE]
    assert flagged, (
        f"no round carries the {fx.MISSING_ROUND_STATE!r} state after a partial payload"
    )


def test_manual_override_is_not_overwritten_by_an_ingestion_run(editor, anon):
    """An active override stands, and the clashing run records a conflict."""
    number = fx.COMPLETE_ROUND_NUMBERS[2]
    seeded = _ingest(editor, f"probe-seed-{fx.unique_token()}",
                     [_race_row(number, 5, "classified", fx.INGEST_INSTANT_OLD)])
    assert seeded.status_code in fx.CREATED, (
        f"the seeding ingestion returned {seeded.status_code}: {seeded.text[:300]}"
    )
    rows = [r for r in editor.get("/results").json() if r.get("roundNumber") == number]
    assert rows, f"round {number} carries no classification to override"
    override = editor.post("/studio/overrides", json={
        "entityType": "classification",
        "entityId": rows[0].get("id"),
        "field": "position",
        "overrideValue": "1",
    })
    assert override.status_code in fx.CREATED, (
        f"recording the override returned {override.status_code}: {override.text[:300]}"
    )
    clash = _ingest(editor, f"probe-clash-{fx.unique_token()}",
                    [_race_row(number, 7, "classified", fx.INGEST_INSTANT_NEW)])
    assert clash.status_code in fx.CREATED, (
        f"the clashing ingestion returned {clash.status_code}: {clash.text[:300]}"
    )
    assert clash.json().get("conflicted", 0) >= 1, (
        f"the clashing run reported conflicted {clash.json().get('conflicted')!r}"
    )
    after = [r for r in anon.get("/results").json() if r.get("roundNumber") == number]
    assert after[0].get("position") == 1, (
        f"the override was overwritten: the stored position is "
        f"{after[0].get('position')!r}, expected 1"
    )


def test_visitor_cannot_run_an_ingestion(visitor, contributor, anon):
    """An ingestion issued below the editor rung is refused at the API."""
    before = anon.get("/results").json()
    entities = [_race_row(fx.COMPLETE_ROUND_NUMBERS[0], 8, "classified",
                          fx.INGEST_INSTANT_NEW)]
    for http, who in ((visitor, "visitor"), (contributor, "contributor")):
        response = _ingest(http, f"probe-denied-{fx.unique_token()}", entities)
        assert response.status_code in fx.DENIED, (
            f"a {who} ingestion returned {response.status_code}, expected a denial"
        )
    assert anon.get("/results").json() == before, (
        "a denied ingestion still changed the stored results"
    )


def test_subscribe_creates_a_pending_record_then_confirms(anon, editor):
    """A subscription is pending until its token confirms the address."""
    email = f"probe-{fx.unique_token()}@example.com"
    response = anon.post("/subscribers", json={"email": email, "topics": ["stories"]})
    assert response.status_code in fx.CREATED, (
        f"POST /api/subscribers returned {response.status_code}: {response.text[:300]}"
    )
    body = response.json()
    assert body.get("status") == fx.PENDING_STATUS, (
        f"a new subscription carries status {body.get('status')!r}, expected "
        f"{fx.PENDING_STATUS!r}"
    )
    token = body.get("confirmToken")
    assert token, "the subscribe response carries no confirmToken"
    listed = [r for r in editor.get("/studio/subscribers").json()
              if r.get("email") == email]
    assert listed, f"the pending subscriber {email!r} is absent from the audience list"
    assert listed[0].get("status") == fx.PENDING_STATUS, (
        f"the stored subscriber carries status {listed[0].get('status')!r}"
    )
    confirmed = anon.post("/subscribers/confirm", json={"token": token})
    assert confirmed.status_code in fx.CREATED, (
        f"the confirmation returned {confirmed.status_code}: {confirmed.text[:300]}"
    )
    assert confirmed.json().get("status") == fx.CONFIRMED_STATUS, (
        f"confirming reported status {confirmed.json().get('status')!r}"
    )
    after = [r for r in editor.get("/studio/subscribers").json()
             if r.get("email") == email]
    assert after[0].get("status") == fx.CONFIRMED_STATUS, (
        f"the stored subscriber is still {after[0].get('status')!r} after confirming"
    )
    assert after[0].get("confirmedAt"), "confirming stamped no confirmedAt"


def test_confirmation_token_cannot_unsubscribe(anon, editor):
    """A confirmation token is single purpose and the unsubscribe route refuses it."""
    email = f"probe-{fx.unique_token()}@example.com"
    created = anon.post("/subscribers", json={"email": email, "topics": ["stories"]})
    assert created.status_code in fx.CREATED, (
        f"POST /api/subscribers returned {created.status_code}: {created.text[:300]}"
    )
    confirm_token = created.json().get("confirmToken")
    unsub_token = created.json().get("unsubscribeToken")
    assert confirm_token, "the subscribe response carries no confirmToken"
    assert unsub_token, "the subscribe response carries no unsubscribeToken"
    assert confirm_token != unsub_token, (
        "the confirmation token and the unsubscribe token are the same value"
    )
    confirmed = anon.post("/subscribers/confirm", json={"token": confirm_token})
    assert confirmed.status_code in fx.CREATED, (
        f"the confirmation returned {confirmed.status_code}"
    )
    misuse = anon.post("/subscribers/unsubscribe", json={"token": confirm_token})
    assert misuse.status_code in fx.REFUSED_AS_INVALID + fx.DENIED_OR_ABSENT, (
        f"the unsubscribe route accepted a confirmation token, returning "
        f"{misuse.status_code}"
    )
    still = [r for r in editor.get("/studio/subscribers").json()
             if r.get("email") == email]
    assert still[0].get("status") == fx.CONFIRMED_STATUS, (
        f"a confirmation token unsubscribed the address, leaving "
        f"{still[0].get('status')!r}"
    )
    proper = anon.post("/subscribers/unsubscribe", json={"token": unsub_token})
    assert proper.status_code in fx.CREATED, (
        f"the real unsubscribe returned {proper.status_code}: {proper.text[:300]}"
    )


def test_repeat_subscribe_answers_identically(anon):
    """A second submission for a known address discloses nothing about the list."""
    email = f"probe-{fx.unique_token()}@example.com"
    first = anon.post("/subscribers", json={"email": email, "topics": ["stories"]})
    assert first.status_code in fx.CREATED, (
        f"the first subscribe returned {first.status_code}: {first.text[:300]}"
    )
    second = anon.post("/subscribers", json={"email": email, "topics": ["stories"]})
    assert second.status_code == first.status_code, (
        f"the repeat subscribe returned {second.status_code} while the first returned "
        f"{first.status_code}"
    )
    assert second.json().get("status") == first.json().get("status"), (
        f"the repeat subscribe reported status {second.json().get('status')!r} while "
        f"the first reported {first.json().get('status')!r}"
    )


def test_enquiry_persists_and_returns_its_reference(anon, editor):
    """A stored enquiry returns an ENQ reference the workspace inbox also shows."""
    marker = fx.unique_token()
    response = anon.post("/enquiries", json={
        "name": "Probe Sender",
        "email": f"probe-{marker}@example.com",
        "organisation": "Probe Company",
        "enquiryType": fx.ENQUIRY_TYPES[0],
        "message": f"A probe enquiry carrying the marker {marker}.",
        "consent": True,
    })
    assert response.status_code in fx.CREATED, (
        f"POST /api/enquiries returned {response.status_code}: {response.text[:300]}"
    )
    reference = response.json().get("reference")
    assert reference, "the enquiry response carries no reference"
    assert reference.startswith(fx.ENQUIRY_REFERENCE_PREFIX), (
        f"the enquiry reference {reference!r} does not begin "
        f"{fx.ENQUIRY_REFERENCE_PREFIX!r}"
    )
    inbox = editor.get("/studio/enquiries")
    assert inbox.status_code == 200, (
        f"GET /api/studio/enquiries returned {inbox.status_code}"
    )
    stored = [row for row in inbox.json() if row.get("reference") == reference]
    assert stored, f"the enquiry reference {reference!r} is absent from the inbox"
    assert stored[0].get("enquiryType") == fx.ENQUIRY_TYPES[0], (
        f"the stored enquiry carries enquiryType {stored[0].get('enquiryType')!r}"
    )


def test_enquiry_missing_a_required_field_is_refused(anon, editor):
    """An enquiry missing a required field is refused and stores nothing."""
    before = len(editor.get("/studio/enquiries").json())
    marker = fx.unique_token()
    response = anon.post("/enquiries", json={
        "name": "Probe Sender",
        "email": f"probe-{marker}@example.com",
        "organisation": "Probe Company",
        "enquiryType": fx.ENQUIRY_TYPES[0],
        "message": "",
        "consent": True,
    })
    assert response.status_code in fx.REFUSED_AS_INVALID, (
        f"an enquiry with an empty message returned {response.status_code}"
    )
    assert response.status_code < 500, "a refused enquiry must not be a server error"
    unticked = anon.post("/enquiries", json={
        "name": "Probe Sender",
        "email": f"probe-{marker}@example.com",
        "organisation": "Probe Company",
        "enquiryType": fx.ENQUIRY_TYPES[0],
        "message": "A probe enquiry with the consent box left alone.",
        "consent": False,
    })
    assert unticked.status_code in fx.REFUSED_AS_INVALID, (
        f"an enquiry with consent unticked returned {unticked.status_code}"
    )
    bad_type = anon.post("/enquiries", json={
        "name": "Probe Sender",
        "email": f"probe-{marker}@example.com",
        "organisation": "Probe Company",
        "enquiryType": "not-a-real-type",
        "message": "A probe enquiry carrying an enquiry type outside the closed set.",
        "consent": True,
    })
    assert bad_type.status_code in fx.REFUSED_AS_INVALID, (
        f"an enquiry with an unknown enquiryType returned {bad_type.status_code}"
    )
    assert len(editor.get("/studio/enquiries").json()) == before, (
        "a refused enquiry was stored anyway"
    )


def test_public_responses_carry_no_private_fields(anon):
    """The public serialisation allowlist keeps internal fields out of every read."""
    for route in ("/stories", "/season", "/results", "/standings", "/profile",
                  "/merch", "/partners"):
        response = anon.get(route)
        assert response.status_code == 200, (
            f"GET /api{route} returned {response.status_code}: {response.text[:200]}"
        )
        found = fx.leaks(response.json())
        assert not found, (
            f"the public response at /api{route} carries private field(s) "
            f"{sorted(found)}"
        )
    detail = anon.get(f"/stories/{fx.PUBLIC_STORY_IDS[0]}")
    assert detail.status_code == 200, (
        f"GET /api/stories/{fx.PUBLIC_STORY_IDS[0]} returned {detail.status_code}"
    )
    leaked = fx.leaks(detail.json())
    assert not leaked, (
        f"the public story detail carries private field(s) {sorted(leaked)}"
    )


def test_profile_and_standings_render_from_the_api(anon):
    """The profile and the championship standing are served from stored records."""
    profile = anon.get("/profile")
    assert profile.status_code == 200, f"GET /api/profile returned {profile.status_code}"
    body = profile.json()
    assert body.get("nickname") == fx.NICKNAME, (
        f"the profile nickname is {body.get('nickname')!r}, expected {fx.NICKNAME!r}"
    )
    assert body.get("monogram") == fx.MONOGRAM, (
        f"the profile monogram is {body.get('monogram')!r}, expected {fx.MONOGRAM!r}"
    )
    assert body.get("constructor") == fx.CONSTRUCTOR, (
        f"the profile constructor is {body.get('constructor')!r}"
    )
    assert body.get("debutYear") == fx.DEBUT_YEAR, (
        f"the profile debut year is {body.get('debutYear')!r}, expected {fx.DEBUT_YEAR}"
    )
    assert body.get("homeTown") == fx.HOME_TOWN, (
        f"the profile home town is {body.get('homeTown')!r}"
    )
    standings = anon.get("/standings")
    assert standings.status_code == 200, (
        f"GET /api/standings returned {standings.status_code}"
    )
    assert isinstance(standings.json().get("position"), int), (
        f"the standing position is {standings.json().get('position')!r}, not a number"
    )


def test_merch_and_partners_render_from_the_api(anon):
    """The merchandise strip and the partner row come from stored records."""
    merch = anon.get("/merch")
    assert merch.status_code == 200, f"GET /api/merch returned {merch.status_code}"
    items = merch.json()
    assert isinstance(items, list), "GET /api/merch must return a JSON array"
    assert len(items) >= 4, f"the merchandise strip carries {len(items)} items, expected 4"
    availability = {str(row.get("availability", "")).lower() for row in items}
    assert any("sold" in value for value in availability), (
        f"no merchandise item is rendered as sold out; availability values were "
        f"{sorted(availability)}"
    )
    stale = [row for row in items if not row.get("price")]
    assert stale, (
        "every merchandise item carries a price, so the freshness rule that drops a "
        "stale price is not observable"
    )
    partners = anon.get("/partners")
    assert partners.status_code == 200, (
        f"GET /api/partners returned {partners.status_code}"
    )
    categories = {row.get("category") for row in partners.json()}
    for category in fx.PARTNER_CATEGORIES:
        assert category in categories, f"partner category {category!r} is absent"


def test_privacy_page_is_reachable_and_states_what_is_stored(site):
    """The privacy page answers publicly and names what the platform stores."""
    response = site.get("/legal/privacy-policy")
    assert response.status_code == 200, (
        f"the privacy route returned {response.status_code}"
    )
    body = response.text.lower()
    assert any(word in body for word in ("privacy", "store", "consent")), (
        "the privacy page names nothing it stores"
    )
    terms = site.get("/legal/terms-conditions")
    assert terms.status_code == 200, f"the terms route returned {terms.status_code}"
    assert len(terms.text) > 0, "the terms route returned an empty document"


def test_unknown_address_answers_as_not_found(site):
    """An unknown address renders the platform's own not-found route."""
    response = site.get(f"/no-such-route-{fx.unique_token()}")
    assert response.status_code == 404, (
        f"an unknown address answered {response.status_code} rather than as not found"
    )
    assert len(response.text) > 0, "the not-found route returned an empty document"


def test_every_public_route_carries_a_unique_title_and_description(site):
    """No two public routes share a title or a description."""
    import re

    titles, descriptions = {}, {}
    for route in fx.PUBLIC_ROUTES:
        response = site.get(route)
        assert response.status_code == 200, (
            f"public route {route} returned {response.status_code}"
        )
        title = re.search(r"<title[^>]*>(.*?)</title>", response.text, re.S | re.I)
        assert title, f"public route {route} carries no title element"
        description = re.search(
            r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"'](.*?)[\"']",
            response.text, re.S | re.I)
        assert description, f"public route {route} carries no description meta"
        titles[route] = title.group(1).strip()
        descriptions[route] = description.group(1).strip()
    assert len(set(titles.values())) == len(titles), (
        f"two public routes share a title: {titles}"
    )
    assert len(set(descriptions.values())) == len(descriptions), (
        f"two public routes share a description: {descriptions}"
    )


def test_internal_links_on_public_routes_resolve(site):
    """Every internal link on a public route answers rather than landing on not found."""
    import re

    checked = set()
    for route in fx.PUBLIC_ROUTES:
        page = site.get(route)
        assert page.status_code == 200, (
            f"public route {route} returned {page.status_code}"
        )
        for href in re.findall(r"href=[\"'](/[^\"'#?]*)[\"']", page.text):
            if href in checked or href.startswith("/api"):
                continue
            checked.add(href)
            linked = site.get(href)
            assert linked.status_code == 200, (
                f"the internal link {href} found on {route} returned "
                f"{linked.status_code}"
            )
    assert checked, "no internal link was found on any public route"


def test_no_credential_appears_in_anything_the_browser_downloads(site):
    """No served document leaks a database, object-store or account credential."""
    secrets = ("deku-local-dev", "minio-root", "minioadmin", fx.CORPUS_PASSWORD)
    for route in fx.PUBLIC_ROUTES:
        served = site.get(route)
        assert served.status_code == 200, (
            f"public route {route} returned {served.status_code}"
        )
        lowered = served.text.lower()
        for secret in secrets:
            assert secret.lower() not in lowered, (
                f"the document at {route} carries the credential {secret!r}"
            )


def test_every_response_carries_the_security_headers(anon):
    """Responses declare a strict transport policy and a nosniff content type."""
    response = anon.get("/health")
    headers = {k.lower(): v.lower() for k, v in response.headers.items()}
    assert "strict-transport-security" in headers, (
        f"no strict transport policy on the response; headers were {sorted(headers)}"
    )
    assert headers.get("x-content-type-options") == "nosniff", (
        f"the nosniff content-type policy is {headers.get('x-content-type-options')!r}"
    )
