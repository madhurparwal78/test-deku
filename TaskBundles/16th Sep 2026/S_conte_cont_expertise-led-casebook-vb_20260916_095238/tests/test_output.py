from __future__ import annotations

import json

import _shapes
import conftest


def test_health_endpoint_reports_ready(anon):
    response = anon.get("/health")
    assert response.status_code == 200, (
        "GET /api/health must answer 200 once the app is ready: "
        + conftest.describe(response))


def test_seeded_feature_slots_hold_the_pinned_case_studies(owner):
    by_id = {str(c.get("id")): str(c.get("slug"))
             for c in _shapes.items(conftest.json_of(owner.get("/studio/work")))}
    for expertise, position, allowed in conftest.SEEDED_SLOTS:
        slot = conftest.slot_for(owner, expertise, position)
        slug = by_id.get(str(slot.get("case_study_id")))
        assert slug in allowed, (
            f"the {expertise} slot {position} starts with {allowed[0]}; it holds {slug}")


def test_public_pages_show_no_long_dash_embedded_player_or_notification_prompt(page, app_base):
    page.add_init_script(conftest.NOTIFY_PROBE)
    for path in ("/", "/work", "/company", "/contact", "/expertise/real-estate"):
        page.goto(f"{app_base}{path}")
        page.wait_for_load_state("networkidle")
        text = page.inner_text("body")
        for dash in conftest.LONG_DASHES:
            assert dash not in text, f"{path} shows a long dash"
        frames = page.eval_on_selector_all("iframe", "els => els.map(e => e.src)")
        assert not frames, f"{path} embeds a third-party player frame: {frames}"
        assert page.evaluate("window.__notifyAsked") is False, (
            f"{path} asks the browser for permission to notify")


def test_published_case_studies_are_listed_in_shelf_order(anon):
    response = anon.get("/work")
    assert response.status_code == 200, (
        "GET /api/work must be readable without signing in: "
        + conftest.describe(response))
    slugs = conftest.slugs_of(response.json())
    seeded = [s for s in slugs if s in conftest.SEEDED_PUBLISHED_SLUGS]
    assert seeded == list(conftest.SEEDED_PUBLISHED_SLUGS), (
        "the ten seeded published case studies must be listed in shelf order "
        f"{list(conftest.SEEDED_PUBLISHED_SLUGS)}; the list carried {seeded}")


def test_work_index_shows_every_published_case_study(owner, anon):
    studio = _shapes.items(conftest.json_of(owner.get("/studio/work")))
    published = {str(c.get("slug")) for c in studio if c.get("published") is True}
    listed = set(conftest.slugs_of(conftest.json_of(anon.get("/work"))))
    assert published == listed, (
        "the public work list must carry every published case study and nothing "
        f"else; published {sorted(published - listed)} missing, "
        f"unpublished {sorted(listed - published)} present")


def test_draft_case_study_is_absent_from_the_public_work_list(anon):
    slugs = conftest.slugs_of(conftest.json_of(anon.get("/work")))
    assert conftest.DRAFT_SLUG not in slugs, (
        f"the seeded draft {conftest.DRAFT_SLUG} must be absent from /api/work; "
        f"the list carried {slugs}")
    assert conftest.WITHDRAWN_SLUG not in slugs, (
        f"the seeded withdrawn case study {conftest.WITHDRAWN_SLUG} must be absent "
        f"from /api/work; the list carried {slugs}")


def test_draft_case_study_address_answers_not_found(anon):
    response = anon.get(f"/work/{conftest.DRAFT_SLUG}")
    assert response.status_code == 404, (
        "a public read of the seeded draft must answer not found: "
        + conftest.describe(response))
    assert conftest.DRAFT_TITLE not in response.text, (
        "the not found answer for a draft must reveal nothing about it: "
        + conftest.describe(response))


def test_withdrawn_case_study_address_answers_gone(anon):
    response = anon.get(f"/work/{conftest.WITHDRAWN_SLUG}")
    assert response.status_code == 410 or conftest.error_code(response) == "gone", (
        "a public read of the seeded withdrawn case study must answer gone: "
        + conftest.describe(response))
    assert conftest.WITHDRAWN_TITLE not in response.text, (
        "the gone answer must not carry the withdrawn case study: "
        + conftest.describe(response))


def test_draft_case_study_is_absent_from_every_expertise_landing(anon):
    for slug in conftest.EXPERTISE_SLUGS:
        response = anon.get(f"/expertise/{slug}")
        assert response.status_code == 200, (
            f"the {slug} landing must be public: " + conftest.describe(response))
        flat = _shapes.flatten(response.json())
        assert conftest.DRAFT_SLUG not in flat, (
            f"the draft must be absent from the {slug} landing: "
            + conftest.describe(response))


def test_draft_case_study_is_absent_from_the_front_page_site_data(anon):
    response = anon.get("/site")
    assert response.status_code == 200, "GET /api/site is public: " + conftest.describe(response)
    flat = _shapes.flatten(response.json())
    assert conftest.DRAFT_SLUG not in flat, (
        "the draft must be absent from the front page data: " + conftest.describe(response))


def test_draft_case_study_is_absent_from_every_next_link(anon):
    slugs = conftest.slugs_of(conftest.json_of(anon.get("/work")))
    for slug in slugs:
        detail = anon.get(f"/work/{slug}")
        assert detail.status_code == 200, (
            f"published case study {slug} must be readable: " + conftest.describe(detail))
        next_link = conftest.dig(detail.json(), "next")
        assert conftest.DRAFT_SLUG not in _shapes.flatten(next_link), (
            f"the next link of {slug} must never name the draft: "
            + conftest.describe(detail))
        assert conftest.WITHDRAWN_SLUG not in _shapes.flatten(next_link), (
            f"the next link of {slug} must never name the withdrawn case study: "
            + conftest.describe(detail))


def test_draft_cover_bytes_are_refused_to_public_callers(owner, editor, anon, visitor):
    created = conftest.create_case(owner, expertise="startups", tags=["saas"])
    cover = conftest.generate_cover(owner, created["id"])
    cover_id = conftest.dig(cover, "id")
    for label, client in (("a signed-out caller", anon), ("a visitor", visitor)):
        response = client.get(f"/covers/{cover_id}")
        assert response.status_code in conftest.REFUSED_CLIENT, (
            f"the cover of a draft must be refused to {label}: "
            + conftest.describe(response))
    for label, client in (("the owner", owner), ("an editor", editor)):
        response = client.get(f"/covers/{cover_id}")
        assert response.status_code == 200 and response.content, (
            f"the cover of a draft must be readable by {label}: "
            + conftest.describe(response))


def test_publish_makes_listing_address_and_cover_readable_in_one_act(owner, anon):
    case = conftest.create_published_case(owner, expertise="corporate", tags=["banking"])
    slug = case["slug"]
    assert slug in conftest.slugs_of(conftest.json_of(anon.get("/work"))), (
        f"a published case study {slug} must be on the public work list")
    detail = anon.get(f"/work/{slug}")
    assert detail.status_code == 200, (
        "a published case study address must be readable: " + conftest.describe(detail))
    cover_id = conftest.dig(case, "cover")
    cover_id = conftest.dig(cover_id, "id") if isinstance(cover_id, dict) else cover_id
    response = anon.get(f"/covers/{cover_id}")
    assert response.status_code == 200 and response.content, (
        "the cover of a published case study must be readable by anyone: "
        + conftest.describe(response))


def test_unpublish_takes_the_case_study_off_lists_and_makes_the_cover_private(owner, anon, backend):
    case = conftest.create_published_case(owner, expertise="ecommerce", tags=["online-store"])
    case_id, slug = case["id"], case["slug"]
    cover = conftest.dig(case, "cover")
    cover_id = conftest.dig(cover, "id") if isinstance(cover, dict) else cover
    response = conftest.unpublish(owner, case_id)
    assert response.status_code in (200, 201), (
        "the owner unpublishes a case study: " + conftest.describe(response))
    assert slug not in conftest.slugs_of(conftest.json_of(anon.get("/work"))), (
        "an unpublished case study must leave the public work list at once")
    landing = conftest.json_of(anon.get("/expertise/ecommerce"))
    assert slug not in _shapes.flatten(landing), (
        "an unpublished case study must leave its expertise landing at once")
    detail = anon.get(f"/work/{slug}")
    assert detail.status_code in (404, 410), (
        "the address of a withdrawn case study must stop answering: "
        + conftest.describe(detail))
    cover_read = anon.get(f"/covers/{cover_id}")
    assert cover_read.status_code in conftest.REFUSED_CLIENT, (
        "the cover of a withdrawn case study must be private again: "
        + conftest.describe(cover_read))
    row = backend.one("case_studies", slug=slug)
    assert row is not None and row.get("withdrawn_at") is not None, (
        f"withdrawn_at must be set on withdrawal; the row read {row}")
    assert row.get("published_at") is None, (
        f"published_at must be empty for an unpublished case study; the row read {row}")


def test_republish_clears_withdrawn_at(owner, backend):
    case = conftest.create_published_case(owner, expertise="ecommerce", tags=["branding"])
    conftest.unpublish(owner, case["id"])
    response = conftest.publish(owner, case["id"])
    assert response.status_code in (200, 201), (
        "the owner publishes a withdrawn case study again: " + conftest.describe(response))
    row = backend.one("case_studies", slug=case["slug"])
    assert row.get("withdrawn_at") is None and row.get("published_at") is not None, (
        f"publishing again clears withdrawn_at and stamps published_at; the row read {row}")


def test_publish_is_refused_without_an_expertise(owner, backend):
    bare = conftest.create_case(owner)
    response = conftest.publish(owner, bare["id"])
    assert conftest.MSG_NEED_EXPERTISE in response.text, (
        "with nothing set, the first missing thing named is the expertise: "
        + conftest.describe(response))
    created = conftest.create_case(owner, tags=["banking"])
    conftest.generate_cover(owner, created["id"])
    response = conftest.publish(owner, created["id"])
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a publish without an expertise must be refused: " + conftest.describe(response))
    assert conftest.MSG_NEED_EXPERTISE in response.text, (
        f"the refusal must read {conftest.MSG_NEED_EXPERTISE!r}: " + conftest.describe(response))
    row = backend.one("case_studies", slug=created["slug"])
    assert row.get("published") in (False, 0), f"a refused publish changes nothing: {row}"


def test_publish_is_refused_without_a_tag(owner, backend):
    created = conftest.create_case(owner, expertise="corporate")
    before = conftest.version_of(owner, created["id"])
    response = conftest.publish(owner, created["id"])
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a publish without a tag must be refused: " + conftest.describe(response))
    assert conftest.MSG_NEED_TAG in response.text, (
        f"with the tag and the cover both missing, the refusal names the tag first: "
        + conftest.describe(response))
    row = backend.one("case_studies", slug=created["slug"])
    assert row.get("published") in (False, 0), f"a refused publish changes nothing: {row}"
    assert conftest.version_of(owner, created["id"]) == before, (
        "a refused publish must leave the version where it was")


def test_publish_is_refused_without_a_cover(owner, backend):
    created = conftest.create_case(owner, expertise="corporate", tags=["banking"])
    response = conftest.publish(owner, created["id"])
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a publish without a cover must be refused: " + conftest.describe(response))
    assert conftest.MSG_NEED_COVER in response.text, (
        f"the refusal must read {conftest.MSG_NEED_COVER!r}: " + conftest.describe(response))
    row = backend.one("case_studies", slug=created["slug"])
    assert row.get("published") in (False, 0), f"a refused publish changes nothing: {row}"


def test_cover_without_alternative_text_is_refused(owner, backend):
    created = conftest.create_case(owner, expertise="corporate", tags=["banking"])
    response = conftest.cover_request(owner, created["id"], "")
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a cover request without alternative text must be refused: " + conftest.describe(response))
    row = backend.one("case_studies", slug=created["slug"])
    assert row.get("cover_id") is None, f"a refused cover request sets no cover: {row}"
    published = conftest.publish(owner, created["id"])
    assert published.status_code in conftest.REFUSED_CLIENT, (
        "a case study with no accepted cover cannot publish: " + conftest.describe(published))


def test_saving_a_case_study_never_publishes_it(owner, anon):
    created = conftest.create_case(owner, expertise="corporate", tags=["banking"])
    conftest.generate_cover(owner, created["id"])
    version = conftest.version_of(owner, created["id"])
    response = owner.patch(f"/studio/work/{created['id']}",
                           json={"summary": "Saved again, still a draft.", "version": version})
    assert response.status_code == 200, "saving should succeed: " + conftest.describe(response)
    assert conftest.dig(conftest.read_case(owner, created["id"]), "published") is not True, (
        "saving a case study must never publish it")
    assert anon.get(f"/work/{created['slug']}").status_code == 404, (
        "a saved but unpublished case study must stay unreadable to the public")


def test_generated_cover_file_lands_in_the_object_store_bucket(owner, store, backend):
    created = conftest.create_case(owner, cover_seed=31337, cover_palette="mono")
    cover = conftest.generate_cover(owner, created["id"])
    key = str(conftest.dig(cover, "object_key"))
    assert key.startswith(f"{conftest.COVER_KEY_PREFIX}{created['id']}/") and key.endswith(".png"), (
        f"a generated cover must be a PNG keyed under its case study: {key}")
    assert conftest.poll_until(lambda: store.exists(key)), (
        f"the generated cover file must exist in the minio bucket at {key}")
    assert backend.count("covers", object_key=key) == 1, "the object key is recorded once"


def test_generated_cover_object_key_follows_the_scheme(owner):
    created = conftest.create_case(owner, cover_seed=5150, cover_palette="warm")
    cover = conftest.generate_cover(owner, created["id"])
    response = owner.get(f"/covers/{conftest.dig(cover, 'id')}")
    assert response.status_code == 200 and response.content, (
        "the owner reads the generated cover bytes: " + conftest.describe(response))
    expected = conftest.COVER_KEY_TEMPLATE.format(
        case_id=created["id"], digest=conftest.sha256_hex(response.content), ext="png")
    assert conftest.dig(cover, "object_key") == expected, (
        f"the object key must follow the pinned scheme {expected}; got {cover}")


def test_cover_endpoint_stores_no_uploaded_file(owner, store):
    created = conftest.create_case(owner)
    payload = conftest.probe_bytes()
    owner.post(f"/studio/work/{created['id']}/cover",
               files={"file": ("cover.png", payload, "image/png")},
               data={"alt_text": "An attempted upload."})
    conftest.settle()
    keys = store.list(f"{conftest.COVER_KEY_PREFIX}{created['id']}/")
    assert all(conftest.sha256_hex(payload) not in k for k in keys), (
        f"the product offers no upload, so the sent file must not reach the bucket: {keys}")


def test_same_cover_seed_and_palette_generate_the_same_cover(owner):
    first = conftest.create_case(owner, cover_seed=777001, cover_palette="cool")
    second = conftest.create_case(owner, cover_seed=777001, cover_palette="cool")
    key_one = str(conftest.dig(conftest.generate_cover(owner, first["id"]), "object_key"))
    key_two = str(conftest.dig(conftest.generate_cover(owner, second["id"]), "object_key"))
    assert key_one.rsplit("/", 1)[-1] == key_two.rsplit("/", 1)[-1], (
        "the same cover seed in the same palette must draw the same cover bytes; "
        f"the digests differ: {key_one} and {key_two}")


def test_identical_cover_bytes_resolve_to_one_object(owner, store):
    created = conftest.create_case(owner, cover_seed=424242, cover_palette="warm")
    first = conftest.generate_cover(owner, created["id"])
    second = conftest.generate_cover(owner, created["id"])
    assert conftest.dig(first, "object_key") == conftest.dig(second, "object_key"), (
        "generating twice from one seed and palette must resolve to one object key")
    keys = store.list(f"{conftest.COVER_KEY_PREFIX}{created['id']}/")
    assert len(keys) == 1, f"the bucket must hold one object for those bytes; it holds {keys}"


def test_cover_row_records_dimensions_and_alternative_text(owner, backend):
    created = conftest.create_case(owner)
    cover = conftest.generate_cover(owner, created["id"], alt_text="Probe cover of a harbour front.")
    row = backend.one("covers", object_key=conftest.dig(cover, "object_key"))
    assert row is not None, f"a covers row must exist for {cover}"
    assert int(row.get("width") or 0) > 0 and int(row.get("height") or 0) > 0, (
        f"the cover row must record its intrinsic width and height: {row}")
    assert row.get("alt_text") == "Probe cover of a harbour front.", (
        f"the cover row must record the alternative text its author wrote: {row}")


def test_new_case_study_starts_at_version_one_and_joins_the_end_of_the_shelf(owner):
    before = _shapes.items(conftest.json_of(owner.get("/studio/work")))
    highest = max(int(c.get("position")) for c in before)
    created = conftest.create_case(owner)
    assert int(conftest.dig(created, "version")) == 1, (
        f"a new case study starts at version 1: {created}")
    assert int(conftest.dig(created, "position")) > highest, (
        f"a new case study joins the end of the shelf past {highest}: {created}")


def test_accepted_write_raises_the_version_by_one(owner):
    created = conftest.create_case(owner)
    version = conftest.version_of(owner, created["id"])
    response = owner.patch(f"/studio/work/{created['id']}",
                           json={"client": "Vantage", "version": version})
    assert response.status_code == 200, "an up-to-date write succeeds: " + conftest.describe(response)
    assert int(conftest.version_of(owner, created["id"])) == int(version) + 1, (
        "an accepted write must raise the version by exactly one")
    patched = owner.patch(f"/studio/work/{created['id']}",
                          json={"expertise": "corporate", "tags": ["banking"],
                                "version": conftest.version_of(owner, created["id"])})
    assert patched.status_code == 200, "the owner sets expertise and tag: " + conftest.describe(patched)
    for label, act in (("setting a cover", lambda: conftest.generate_cover(owner, created["id"])),
                       ("publishing", lambda: conftest.publish(owner, created["id"])),
                       ("unpublishing", lambda: conftest.unpublish(owner, created["id"]))):
        before = int(conftest.version_of(owner, created["id"]))
        act()
        assert int(conftest.version_of(owner, created["id"])) == before + 1, (
            f"{label} must raise the case study version by exactly one")


def test_stale_version_write_is_refused_as_a_conflict(owner, editor):
    created = conftest.create_case(owner)
    version = conftest.version_of(owner, created["id"])
    first = owner.patch(f"/studio/work/{created['id']}",
                        json={"title": "Owner Title Wins", "version": version})
    assert first.status_code == 200, "the first write succeeds: " + conftest.describe(first)
    second = editor.patch(f"/studio/work/{created['id']}",
                          json={"title": "Editor Title Loses", "version": version})
    assert second.status_code in conftest.REFUSED_CLIENT, (
        "a write from an older version must be refused: " + conftest.describe(second))
    assert conftest.error_code(second) == "conflict", (
        "a stale write is refused with the conflict code: " + conftest.describe(second))
    assert conftest.MSG_CONFLICT in second.text, (
        f"the conflict must read {conftest.MSG_CONFLICT!r}: " + conftest.describe(second))
    assert conftest.dig(conftest.read_case(owner, created["id"]), "title") == "Owner Title Wins", (
        "a refused stale write must change nothing and nothing is merged")


def test_write_without_a_version_is_refused(owner):
    created = conftest.create_case(owner)
    before = conftest.read_case(owner, created["id"])
    response = owner.patch(f"/studio/work/{created['id']}", json={"title": "No Version Sent"})
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a write that sends no version must be refused: " + conftest.describe(response))
    after = conftest.read_case(owner, created["id"])
    assert conftest.dig(after, "title") == conftest.dig(before, "title"), (
        "a refused write must change nothing")


def test_concurrent_writes_from_one_version_admit_exactly_one(owner, editor, app_base):
    created = conftest.create_case(owner)
    version = conftest.version_of(owner, created["id"])
    url = f"{app_base}/api/studio/work/{created['id']}"
    tokens = (owner.headers["Authorization"], editor.headers["Authorization"])

    def write(auth, title):
        return lambda: conftest.raw_call("PATCH", url, auth,
                                         {"title": title, "version": version})

    results = conftest.run_together([write(tokens[0], "Concurrent A"),
                                     write(tokens[1], "Concurrent B")])
    ok = [r for r in results if r.status_code == 200]
    refused = [r for r in results if r.status_code in conftest.REFUSED_CLIENT]
    assert len(ok) == 1 and len(refused) == 1, (
        "two concurrent writes from the same version must admit exactly one: "
        + "; ".join(conftest.describe(r) for r in results))
    assert int(conftest.version_of(owner, created["id"])) == int(version) + 1, (
        "exactly one concurrent write may raise the version")


def test_repeated_case_study_create_with_one_idempotency_key_creates_one_row(owner, backend):
    body = conftest.new_case_payload("probe-idem")
    headers = {"Idempotency-Key": f"idem-{conftest.unique_token()}"}
    first = owner.post("/studio/work", json=body, headers=headers)
    second = owner.post("/studio/work", json=body, headers=headers)
    assert first.status_code in (200, 201) and second.status_code in (200, 201), (
        "a repeated create with one idempotency key answers as the first did: "
        + conftest.describe(second))
    assert conftest.dig(first.json(), "id") == conftest.dig(second.json(), "id"), (
        "the repeat must return the first answer")
    assert backend.count("case_studies", slug=body["slug"]) == 1, (
        "a repeated create with one idempotency key must create one row")


def test_repeated_brief_with_one_idempotency_key_creates_one_brief(anon, backend):
    token = conftest.brief_token(anon)
    conftest.wait_past_form_floor()
    body = conftest.brief_payload(token)
    headers = {"Idempotency-Key": f"idem-{conftest.unique_token()}"}
    first = anon.post("/briefs", json=body, headers=headers)
    second = anon.post("/briefs", json=body, headers=headers)
    assert first.status_code in (200, 201) and second.status_code in (200, 201), (
        "a repeated brief answers as the first did: " + conftest.describe(second))
    assert conftest.poll_until(lambda: backend.count("briefs", email=body["email"]) == 1), (
        "a repeated brief with one idempotency key must store one brief")


def test_shelf_reorder_changes_the_public_work_order(owner, anon):
    first = conftest.create_published_case(owner, expertise="startups", tags=["saas"])
    second = conftest.create_published_case(owner, expertise="startups", tags=["saas"])
    version, ids = conftest.shelf_state(owner)
    order = conftest.moved_before(ids, second["id"], first["id"])
    response = conftest.put_shelf(owner, order, version)
    assert response.status_code == 200, "the owner reorders the shelf: " + conftest.describe(response)
    assert int(conftest.dig(conftest.json_of(response), "version")) == int(version) + 1, (
        "an accepted reorder raises the shelf version by one")
    slugs = conftest.slugs_of(conftest.json_of(anon.get("/work")))
    assert slugs.index(second["slug"]) < slugs.index(first["slug"]), (
        "after the reorder the public work list must follow the new shelf order")
    landing = conftest.slugs_of(conftest.dig(conftest.json_of(anon.get("/expertise/startups")), "work"))
    assert landing.index(second["slug"]) < landing.index(first["slug"]), (
        "the expertise landing must follow the new shelf order")


def test_withdrawn_case_study_keeps_its_shelf_place_when_republished(owner, anon):
    case = conftest.create_published_case(owner, expertise="real-estate", tags=["real-estate"])
    later = conftest.create_published_case(owner, expertise="real-estate", tags=["real-estate"])
    place = int(conftest.dig(conftest.read_case(owner, case["id"]), "position"))
    conftest.unpublish(owner, case["id"])
    assert int(conftest.dig(conftest.read_case(owner, case["id"]), "position")) == place, (
        "a withdrawn case study keeps its shelf place")
    conftest.publish(owner, case["id"])
    assert int(conftest.dig(conftest.read_case(owner, case["id"]), "position")) == place, (
        "publishing again returns the case study to its kept place")
    slugs = conftest.slugs_of(conftest.json_of(anon.get("/work")))
    assert slugs.index(case["slug"]) < slugs.index(later["slug"]), (
        "a republished case study returns to its kept place, not to the end")


def test_shelf_places_stay_unique_and_gap_free(owner):
    rows = _shapes.items(conftest.json_of(owner.get("/studio/work")))
    places = sorted(int(r.get("position")) for r in rows)
    assert len(places) == len(set(places)), f"shelf places must be unique: {places}"
    assert places == list(range(places[0], places[0] + len(places))), (
        f"shelf places must be gap-free: {places}")


def test_stale_shelf_version_is_refused_and_keeps_the_order(owner):
    conftest.create_case(owner)
    version, before = conftest.shelf_state(owner)
    accepted = conftest.put_shelf(owner, list(reversed(before)), version)
    assert accepted.status_code == 200, "the first reorder is accepted: " + conftest.describe(accepted)
    _, saved = conftest.shelf_state(owner)
    stale = conftest.put_shelf(owner, before, version)
    assert 400 <= stale.status_code < 500, (
        "a reorder sent with an older shelf version is refused: " + conftest.describe(stale))
    assert conftest.MSG_CONFLICT in stale.text and conftest.MSG_SHELF_STALE in stale.text, (
        "the stale reorder refusal carries the conflict line then the shelf line: " + conftest.describe(stale))
    assert conftest.shelf_state(owner)[1] == saved, "a refused reorder leaves the saved order"


def test_shelf_reorder_without_a_version_is_refused(owner):
    conftest.create_case(owner)
    _, before = conftest.shelf_state(owner)
    response = conftest.put_shelf(owner, list(reversed(before)), None)
    assert 400 <= response.status_code < 500, (
        "a reorder sent with no shelf version is refused: " + conftest.describe(response))
    assert conftest.MSG_CONFLICT in response.text and conftest.MSG_SHELF_STALE in response.text, (
        "a versionless reorder is refused as a conflict with both lines: " + conftest.describe(response))
    assert conftest.shelf_state(owner)[1] == before, "a refused reorder changes nothing"


def test_shelf_reorder_leaves_case_study_versions_unchanged(owner):
    first = conftest.create_case(owner)
    second = conftest.create_case(owner)
    version, ids = conftest.shelf_state(owner)
    response = conftest.put_shelf(owner, conftest.moved_before(ids, second["id"], first["id"]), version)
    assert response.status_code == 200, "the owner reorders the shelf: " + conftest.describe(response)
    for case in (first, second):
        assert int(conftest.dig(conftest.read_case(owner, case["id"]), "version")) == int(conftest.dig(case, "version")), (
            "a reorder changes places only, never a case study's version")


def test_editor_is_forbidden_to_reorder_the_shelf(editor, owner):
    version, before = conftest.shelf_state(owner)
    response = conftest.put_shelf(editor, list(reversed(before)), version)
    assert response.status_code in conftest.DENIED, (
        "an editor must be denied reordering the shelf: " + conftest.describe(response))
    after = conftest.ids_of(conftest.json_of(owner.get("/studio/work")))
    assert after == before, "a denied reorder leaves the shelf order unchanged"


def test_feature_slot_takes_a_published_case_study_of_its_expertise(owner, anon):
    case = conftest.create_published_case(owner, expertise="corporate", tags=["corporate-website"])
    slot = conftest.slot_for(owner, "corporate", 0)
    response = conftest.put_slot(owner, slot["id"], case["id"], slot["version"])
    assert response.status_code == 200, "the owner fills a slot: " + conftest.describe(response)
    site = conftest.json_of(anon.get("/site"))
    assert case["slug"] in _shapes.flatten(site), (
        "a featured case study must appear in the front page data")


def test_replaced_slot_occupant_stays_published_and_listed(owner, anon):
    first = conftest.create_published_case(owner, expertise="corporate", tags=["banking"])
    second = conftest.create_published_case(owner, expertise="corporate", tags=["banking"])
    slot = conftest.slot_for(owner, "corporate", 1)
    conftest.put_slot(owner, slot["id"], first["id"], slot["version"])
    slot = conftest.slot_for(owner, "corporate", 1)
    response = conftest.put_slot(owner, slot["id"], second["id"], slot["version"])
    assert response.status_code == 200, "the owner replaces a slot occupant: " + conftest.describe(response)
    assert conftest.dig(conftest.read_case(owner, first["id"]), "published") is True, (
        "the case study replaced in a feature slot must stay published")
    assert first["slug"] in conftest.slugs_of(conftest.json_of(anon.get("/work"))), (
        "the case study replaced in a feature slot must stay on the public work list")


def test_feature_slot_can_be_emptied(owner, anon):
    case = conftest.create_published_case(owner, expertise="ecommerce", tags=["online-store"])
    slot = conftest.slot_for(owner, "ecommerce", 1)
    conftest.put_slot(owner, slot["id"], case["id"], slot["version"])
    slot = conftest.slot_for(owner, "ecommerce", 1)
    response = conftest.put_slot(owner, slot["id"], None, slot["version"])
    assert response.status_code == 200, "a feature slot may hold nothing: " + conftest.describe(response)
    assert conftest.slot_for(owner, "ecommerce", 1).get("case_study_id") is None, (
        "an emptied feature slot must hold nothing")
    featured = conftest.dig(conftest.json_of(anon.get("/site")), "featured")
    assert "null" in json.dumps(featured), f"the site shows the emptied featured slot as null: {featured}"
    assert conftest.dig(conftest.read_case(owner, case["id"]), "published") is True, (
        "emptying a slot leaves the case study published")


def test_feature_slot_refuses_a_draft_case_study(owner):
    draft = conftest.create_case(owner, expertise="corporate", tags=["banking"])
    slot = conftest.slot_for(owner, "corporate", 0)
    response = conftest.put_slot(owner, slot["id"], draft["id"], slot["version"])
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a feature slot must refuse a case study that is not published: "
        + conftest.describe(response))
    assert str(conftest.slot_for(owner, "corporate", 0).get("case_study_id")) != str(draft["id"]), (
        "a refused slot write leaves the slot as it was")


def test_feature_slot_refuses_a_case_study_of_another_expertise(owner):
    other = conftest.create_published_case(owner, expertise="startups", tags=["saas"])
    slot = conftest.slot_for(owner, "corporate", 0)
    response = conftest.put_slot(owner, slot["id"], other["id"], slot["version"])
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a feature slot must refuse a case study of another expertise: "
        + conftest.describe(response))


def test_case_study_holds_at_most_one_feature_slot(owner):
    case = conftest.create_published_case(owner, expertise="startups", tags=["saas"])
    first = conftest.slot_for(owner, "startups", 0)
    conftest.put_slot(owner, first["id"], case["id"], first["version"])
    second = conftest.slot_for(owner, "startups", 1)
    response = conftest.put_slot(owner, second["id"], case["id"], second["version"])
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a case study may hold at most one feature slot: " + conftest.describe(response))


def test_slot_write_leaves_the_case_study_row_unchanged(owner, backend):
    case = conftest.create_published_case(owner, expertise="real-estate", tags=["real-estate"])
    before = backend.one("case_studies", slug=case["slug"])
    slot = conftest.slot_for(owner, "real-estate", 0)
    response = conftest.put_slot(owner, slot["id"], case["id"], slot["version"])
    assert response.status_code == 200, "the owner fills a slot: " + conftest.describe(response)
    after = backend.one("case_studies", slug=case["slug"])
    assert before == after, (
        f"writing a feature slot must never write the case study row; before {before}, after {after}")


def test_stale_slot_write_is_refused_and_slots_carry_versions(owner):
    case = conftest.create_published_case(owner, expertise="ecommerce", tags=["branding"])
    slot = conftest.slot_for(owner, "ecommerce", 0)
    assert slot.get("version") is not None, f"a feature slot carries a version: {slot}"
    first = conftest.put_slot(owner, slot["id"], case["id"], slot["version"])
    assert first.status_code == 200, "the first slot write succeeds: " + conftest.describe(first)
    stale = conftest.put_slot(owner, slot["id"], None, slot["version"])
    assert stale.status_code in conftest.REFUSED_CLIENT, (
        "a slot write from an older version must be refused: " + conftest.describe(stale))


def test_concurrent_slot_writes_from_one_version_admit_exactly_one(owner, app_base):
    one = conftest.create_published_case(owner, expertise="startups", tags=["trading-platform"])
    two = conftest.create_published_case(owner, expertise="startups", tags=["trading-platform"])
    slot = conftest.slot_for(owner, "startups", 1)
    url = f"{app_base}/api/studio/slots/{slot['id']}"
    auth = owner.headers["Authorization"]

    def write(case_id):
        return lambda: conftest.raw_call("PUT", url, auth,
                                         {"case_study_id": case_id, "version": slot["version"]})

    results = conftest.run_together([write(one["id"]), write(two["id"])])
    ok = [r for r in results if r.status_code == 200]
    assert len(ok) == 1, (
        "two concurrent slot writes from one version must admit exactly one: "
        + "; ".join(conftest.describe(r) for r in results))


def test_editor_is_forbidden_to_fill_a_feature_slot(editor, owner):
    case = conftest.create_published_case(owner, expertise="corporate", tags=["banking"])
    slot = conftest.slot_for(owner, "corporate", 0)
    response = conftest.put_slot(editor, slot["id"], case["id"], slot["version"])
    assert response.status_code in conftest.DENIED, (
        "an editor must be denied filling a feature slot: " + conftest.describe(response))
    after = conftest.slot_for(owner, "corporate", 0)
    assert str(after.get("case_study_id")) == str(slot.get("case_study_id")), (
        "a denied slot write leaves the slot unchanged")


def test_site_lists_four_expertises_in_order_with_their_sentences(anon):
    site = conftest.json_of(anon.get("/site"))
    expertises = _shapes.items(conftest.dig(site, "expertises"))
    assert [str(e.get("slug")) for e in expertises] == list(conftest.EXPERTISE_SLUGS), (
        f"the four expertises must be listed in order: {expertises}")
    assert [str(e.get("name")) for e in expertises] == list(conftest.EXPERTISE_NAMES), (
        f"the expertise names must read as pinned: {expertises}")
    assert [str(e.get("sentence")) for e in expertises] == list(conftest.EXPERTISE_SENTENCES), (
        "each expertise band carries its pinned sentence")


def test_site_features_the_owner_slot_choices(owner, anon):
    slots = conftest.studio_slots(owner)
    assert len(slots) == 8, f"a fresh installation carries eight feature slots: {slots}"
    for slug in conftest.EXPERTISE_SLUGS:
        count = sum(1 for s in slots if str(s.get("expertise")) == slug)
        assert count == 2, f"each expertise holds exactly two slots; {slug} holds {count}"
        positions = sorted(int(s.get("position")) for s in slots if str(s.get("expertise")) == slug)
        assert positions == [0, 1], f"the two slots of {slug} sit at positions 0 and 1: {positions}"
    by_id = {str(c.get("id")): str(c.get("slug"))
             for c in _shapes.items(conftest.json_of(owner.get("/studio/work")))}
    site = _shapes.flatten(conftest.json_of(anon.get("/site")))
    for slot in slots:
        if slot.get("case_study_id") is not None:
            slug = by_id[str(slot["case_study_id"])]
            assert slug.lower() in site, (
                f"the front page must show the owner's slot choice {slug}")


def test_tags_hold_exactly_the_eleven_pinned_tags(anon, backend):
    site = conftest.json_of(anon.get("/site"))
    tags = sorted(str(t.get("slug")) for t in _shapes.items(conftest.dig(site, "tags")))
    assert tags == sorted(conftest.TAG_SLUGS), f"the site carries the eleven tags: {tags}"
    assert backend.count("tags") == 11, "the tags table holds exactly eleven tags"
    names = sorted(str(t.get("name")) for t in _shapes.items(conftest.dig(site, "tags")))
    assert names == sorted(conftest.TAG_NAMES), f"the eleven tag names read as pinned: {names}"


def test_work_filter_by_expertise_keeps_only_that_expertise(anon):
    response = anon.get("/work", params={"expertise": "corporate"})
    rows = _shapes.items(conftest.json_of(response))
    assert rows, "the corporate filter must return the corporate case studies"
    assert all(str(r.get("expertise")) == "corporate" for r in rows), (
        f"an expertise filter keeps only that expertise: {rows}")
    assert conftest.REAL_ESTATE_SLUG not in conftest.slugs_of(rows), (
        "a real estate case study must be dropped by the corporate filter")


def test_two_tag_filters_show_case_studies_carrying_either_tag(anon):
    response = anon.get("/work", params=[("tag", "banking"), ("tag", "saas")])
    slugs = conftest.slugs_of(conftest.json_of(response))
    assert conftest.CASE_WITH_BANKING in slugs and conftest.SAAS_SLUG in slugs, (
        f"two tag filters show case studies carrying either tag: {slugs}")
    assert conftest.REAL_ESTATE_SLUG not in slugs, (
        f"a case study carrying neither tag is dropped: {slugs}")


def test_expertise_and_tag_filters_combine_as_both(anon):
    response = anon.get("/work", params=[("expertise", "corporate"), ("tag", "banking")])
    slugs = conftest.slugs_of(conftest.json_of(response))
    for expected in conftest.CORPORATE_BANKING_SLUGS:
        assert expected in slugs, f"{expected} carries both and must be listed: {slugs}"
    assert conftest.CORPORATE_PLAIN_SLUG not in slugs, (
        f"a corporate case study without the banking tag is dropped: {slugs}")


def test_real_estate_tag_filter_is_separate_from_the_real_estate_expertise(owner, anon):
    tagged = conftest.create_published_case(owner, expertise="corporate", tags=["real-estate"])
    untagged = conftest.create_published_case(owner, expertise="real-estate", tags=["branding"])
    by_tag = conftest.slugs_of(conftest.json_of(anon.get("/work", params={"tag": "real-estate"})))
    by_expertise = conftest.slugs_of(conftest.json_of(
        anon.get("/work", params={"expertise": "real-estate"})))
    assert tagged["slug"] in by_tag and tagged["slug"] not in by_expertise, (
        "the Real Estate tag filter never filters on the Real Estate expertise")
    assert untagged["slug"] in by_expertise and untagged["slug"] not in by_tag, (
        "the Real Estate expertise filter never filters on the Real Estate tag")


def test_unknown_filter_value_is_dropped(anon):
    plain = conftest.slugs_of(conftest.json_of(anon.get("/work")))
    unknown = conftest.slugs_of(conftest.json_of(
        anon.get("/work", params={"expertise": "no-such-expertise"})))
    assert unknown == plain, (
        "an unknown filter value must be dropped, leaving the unfiltered list")


def test_case_study_detail_carries_blocks_tags_cover_and_next(anon):
    response = anon.get(f"/work/{conftest.CASE_WITH_BANKING}")
    body = conftest.json_of(response)
    blocks = conftest.dig(body, "blocks")
    assert isinstance(blocks, list) and blocks, f"a case study carries its body blocks: {body}"
    assert all(str(b.get("kind")) in conftest.BLOCK_KINDS for b in blocks), (
        f"every block is one of the six kinds: {blocks}")
    assert "banking" in _shapes.flatten(conftest.dig(body, "tags")), f"the tags are carried: {body}"
    assert conftest.dig(body, "cover") is not None, f"the cover is carried: {body}"
    assert conftest.dig(body, "next") is not None, f"the next case study is carried: {body}"


def test_next_case_study_follows_shelf_order_and_wraps(anon):
    slugs = conftest.slugs_of(conftest.json_of(anon.get("/work")))
    first_detail = conftest.json_of(anon.get(f"/work/{slugs[0]}"))
    assert slugs[1] in _shapes.flatten(conftest.dig(first_detail, "next")), (
        f"the next link of {slugs[0]} must name {slugs[1]}")
    last_detail = conftest.json_of(anon.get(f"/work/{slugs[-1]}"))
    assert slugs[0] in _shapes.flatten(conftest.dig(last_detail, "next")), (
        f"the next link of the last case study must wrap to {slugs[0]}")


def test_seventh_block_kind_is_refused(owner, backend):
    body = conftest.new_case_payload("probe-video", blocks=[{"kind": "video", "text": "x"}])
    response = owner.post("/studio/work", json=body)
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a seventh block kind must be refused: " + conftest.describe(response))
    assert backend.count("case_studies", slug=body["slug"]) == 0, (
        "a refused write writes no row")


def test_expertise_landing_lists_its_published_work_in_shelf_order(anon):
    body = conftest.json_of(anon.get("/expertise/corporate"))
    slugs = conftest.slugs_of(conftest.dig(body, "work"))
    seeded = [s for s in slugs if s in conftest.SEEDED_PUBLISHED_SLUGS]
    assert seeded == ["kestrel-annual-review", "ostend-investor-portal", "northline-self-care"], (
        f"the corporate landing lists its published case studies in shelf order: {slugs}")


def test_valid_brief_is_stored_unread_with_its_source_path(anon, backend):
    body, response = conftest.send_brief(anon, source_path="/expertise/real-estate")
    assert response.status_code in (200, 201), "a valid brief is accepted: " + conftest.describe(response)
    assert conftest.dig(response.json(), "id") is not None, "an accepted brief answers with its id"
    row = conftest.poll_until(lambda: backend.one("briefs", email=body["email"]))
    assert row is not None, "an accepted brief must be stored"
    assert row.get("state") == "unread", f"an accepted brief lands as unread: {row}"
    assert row.get("source_path") == "/expertise/real-estate", f"the source_path is recorded: {row}"
    assert row.get("phone") == "+4712345678", f"the phone keeps only digits and a leading plus: {row}"


def test_brief_with_an_empty_name_is_refused_with_its_message(anon, backend):
    body, response = conftest.send_brief(anon, name="   ")
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a brief with an empty name is refused: " + conftest.describe(response))
    assert conftest.error_code(response) == "unprocessable", (
        "a field refusal carries the unprocessable code: " + conftest.describe(response))
    assert conftest.dig(response.json(), "name") == conftest.MSG_NAME, (
        f"the name field reads {conftest.MSG_NAME!r}: " + conftest.describe(response))
    assert backend.count("briefs", email=body["email"]) == 0, "a refused brief stores nothing"


def test_brief_with_an_incomplete_phone_is_refused_with_its_message(anon, backend):
    body, response = conftest.send_brief(anon, phone="12345")
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a brief phone with five digits is refused: " + conftest.describe(response))
    assert conftest.MSG_PHONE in response.text, (
        f"the phone field reads {conftest.MSG_PHONE!r}: " + conftest.describe(response))
    assert backend.count("briefs", email=body["email"]) == 0, "a refused brief stores nothing"


def test_brief_with_an_invalid_email_is_refused_with_its_message(anon):
    body, response = conftest.send_brief(anon, email="not an address")
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a brief with an invalid email is refused: " + conftest.describe(response))
    assert conftest.MSG_EMAIL in response.text, (
        f"the email field reads {conftest.MSG_EMAIL!r}: " + conftest.describe(response))


def test_brief_with_a_short_comment_is_refused_with_its_message(anon, backend):
    body, response = conftest.send_brief(anon, comment="   too short   ")
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a brief comment under ten characters is refused: " + conftest.describe(response))
    assert conftest.MSG_COMMENT in response.text, (
        f"the comment field reads {conftest.MSG_COMMENT!r}: " + conftest.describe(response))
    assert backend.count("briefs", email=body["email"]) == 0, "a refused brief stores nothing"


def test_brief_with_an_overlong_name_is_refused(anon, backend):
    body, response = conftest.send_brief(anon, name="N" * 81)
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a brief name over 80 characters is refused: " + conftest.describe(response))
    assert backend.count("briefs", email=body["email"]) == 0, "a refused brief stores nothing"


def test_brief_comment_with_three_web_addresses_is_refused(anon, backend):
    comment = ("See https://one.example.com and https://two.example.com "
               "and https://three.example.com for context.")
    body, response = conftest.send_brief(anon, comment=comment)
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a brief comment with more than two web addresses is refused: "
        + conftest.describe(response))
    assert conftest.FEWER_LINKS in response.text, (
        f"the refusal reads {conftest.FEWER_LINKS!r}: " + conftest.describe(response))
    assert backend.count("briefs", email=body["email"]) == 0, "a refused brief stores nothing"


def test_brief_with_a_filled_website_field_is_spam_that_stores_nothing(anon, backend):
    real, accepted = conftest.send_brief(anon)
    spam, response = conftest.send_brief(anon, website="https://spam.example.com")
    assert response.status_code == accepted.status_code, (
        "a spam brief gets the same answer an accepted brief gets: " + conftest.describe(response))
    conftest.settle()
    assert backend.count("briefs", email=spam["email"]) == 0, (
        "a brief whose hidden website field is filled stores nothing")


def test_brief_with_a_fresh_form_token_is_spam_that_stores_nothing(anon, backend):
    token = conftest.brief_token(anon)
    body = conftest.brief_payload(token)
    response = anon.post("/briefs", json=body)
    assert response.status_code in (200, 201), (
        "a spam brief gets the same answer an accepted brief gets: " + conftest.describe(response))
    conftest.settle()
    assert backend.count("briefs", email=body["email"]) == 0, (
        "a brief whose form_token is under two seconds old stores nothing")


def test_brief_without_or_with_a_forged_form_token_stores_nothing(anon, backend):
    conftest.wait_past_form_floor()
    missing = conftest.brief_payload("")
    missing.pop("form_token")
    forged = conftest.brief_payload(f"forged-{conftest.unique_token()}")
    for label, body in (("no form_token", missing), ("a forged form_token", forged)):
        response = anon.post("/briefs", json=body)
        assert response.status_code in (200, 201), (
            f"a brief with {label} gets the same answer an accepted brief gets: "
            + conftest.describe(response))
    conftest.settle()
    for body in (missing, forged):
        assert backend.count("briefs", email=body["email"]) == 0, (
            "a brief whose form_token is missing or was never issued stores nothing")


def test_reused_form_token_stores_nothing(anon, backend):
    first, accepted = conftest.send_brief(anon)
    assert accepted.status_code in (200, 201), "the first brief is accepted: " + conftest.describe(accepted)
    reuse = conftest.brief_payload(first["form_token"])
    response = anon.post("/briefs", json=reuse)
    assert response.status_code == accepted.status_code, (
        "a brief reusing a token gets the same answer: " + conftest.describe(response))
    conftest.settle()
    assert backend.count("briefs", email=reuse["email"]) == 0, (
        "a brief reusing a form_token already used stores nothing")


def test_brief_without_phone_expertise_or_budget_is_accepted(anon, backend):
    body, response = conftest.send_brief(anon, phone="", expertise=None, budget=None)
    assert response.status_code in (200, 201), (
        "phone, expertise and budget are optional: " + conftest.describe(response))
    assert conftest.poll_until(lambda: backend.count("briefs", email=body["email"]) == 1), (
        "a brief without the optional fields is stored")


def test_fourth_brief_from_one_email_within_an_hour_is_refused(anon, backend):
    email = conftest.probe_email()
    tokens = [conftest.brief_token(anon) for _ in range(4)]
    conftest.wait_past_form_floor()
    answers = [anon.post("/briefs", json=conftest.brief_payload(t, email=email)) for t in tokens]
    assert all(r.status_code in (200, 201) for r in answers[:3]), (
        "the first three briefs from one address are accepted: "
        + "; ".join(conftest.describe(r) for r in answers[:3]))
    assert answers[3].status_code in conftest.REFUSED_CLIENT, (
        "a fourth brief from one address within an hour is refused: "
        + conftest.describe(answers[3]))
    assert backend.count("briefs", email=email) == 3, "exactly three briefs are stored"


def test_brief_with_an_unknown_expertise_is_refused_under_its_field(anon, backend):
    body, response = conftest.send_brief(anon, expertise="architecture")
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a brief naming an unknown expertise is refused: " + conftest.describe(response))
    assert conftest.MSG_EXPERTISE_CHOICE in response.text, (
        f"the expertise field reads {conftest.MSG_EXPERTISE_CHOICE!r}: " + conftest.describe(response))
    assert backend.count("briefs", email=body["email"]) == 0, "a refused brief stores nothing"


def test_brief_with_an_unknown_budget_is_refused_under_its_field(anon, backend):
    body, response = conftest.send_brief(anon, budget="over_500k")
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a brief naming an unknown budget is refused: " + conftest.describe(response))
    assert conftest.MSG_BUDGET_CHOICE in response.text, (
        f"the budget field reads {conftest.MSG_BUDGET_CHOICE!r}: " + conftest.describe(response))
    assert backend.count("briefs", email=body["email"]) == 0, "a refused brief stores nothing"


def test_overlong_comment_with_three_web_addresses_shows_only_the_length_message(anon, backend):
    links = "https://one.example.com https://two.example.com https://three.example.com "
    body, response = conftest.send_brief(anon, comment=links + "x" * 4000)
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "an overlong comment with three web addresses is refused: " + conftest.describe(response))
    assert conftest.MSG_COMMENT in response.text and conftest.FEWER_LINKS not in response.text, (
        "when both comment rules fail only the length message shows: " + conftest.describe(response))
    assert backend.count("briefs", email=body["email"]) == 0, "a refused brief stores nothing"


def test_brief_comment_is_stored_exactly_as_typed(anon, backend):
    comment = "Plans attached: <b>bold</b> <img src=x> and a line\nbreak kept as typed."
    body, response = conftest.send_brief(anon, comment=comment)
    assert response.status_code in (200, 201), "the brief is accepted: " + conftest.describe(response)
    row = conftest.poll_until(lambda: backend.one("briefs", email=body["email"]))
    assert row is not None and row.get("comment") == comment, (
        f"a brief comment is stored exactly as typed: {row}")


def test_editor_is_forbidden_to_read_or_change_briefs(editor, owner, backend):
    briefs = _shapes.items(conftest.json_of(owner.get("/studio/briefs")))
    target = briefs[0]
    before = backend.one("briefs", id=target["id"])
    listing = editor.get("/studio/briefs")
    assert listing.status_code in conftest.DENIED, (
        "an editor must be denied the brief inbox: " + conftest.describe(listing))
    detail = editor.get(f"/studio/briefs/{target['id']}")
    assert detail.status_code in conftest.DENIED, (
        "an editor must be denied reading a brief: " + conftest.describe(detail))
    change = editor.patch(f"/studio/briefs/{target['id']}", json={"state": "archived"})
    assert change.status_code in conftest.DENIED, (
        "an editor must be denied changing a brief: " + conftest.describe(change))
    assert backend.one("briefs", id=target["id"]) == before, (
        "a denied brief change leaves the brief row unchanged")


def test_unauthenticated_caller_is_denied_the_brief_inbox(anon):
    response = anon.get("/studio/briefs")
    assert response.status_code in conftest.DENIED, (
        "a caller with no session is denied the brief inbox: " + conftest.describe(response))


def test_owner_marks_a_brief_read_then_archived(anon, owner, backend):
    body, response = conftest.send_brief(anon)
    brief_id = conftest.dig(response.json(), "id")
    for state in ("read", "archived"):
        change = owner.patch(f"/studio/briefs/{brief_id}", json={"state": state})
        assert change.status_code == 200, f"the owner marks the brief {state}: " + conftest.describe(change)
        row = backend.one("briefs", email=body["email"])
        assert row.get("state") == state, f"the stored brief state must be {state}: {row}"
    owner.patch(f"/studio/briefs/{brief_id}", json={"state": "unread"})
    detail = conftest.json_of(owner.get(f"/studio/briefs/{brief_id}"))
    assert backend.one("briefs", email=body["email"]).get("state") == "unread", (
        "reading a brief through the API leaves its state unchanged")
    for field in ("id", "state", "received_at", "email", "comment", "source_path"):
        assert conftest.dig(detail, field) is not None, f"a brief response carries {field}: {detail}"


def test_owner_deletes_a_brief(anon, owner, backend):
    body, response = conftest.send_brief(anon)
    brief_id = conftest.dig(response.json(), "id")
    removed = owner.delete(f"/studio/briefs/{brief_id}")
    assert removed.status_code in (200, 204), "the owner deletes a brief: " + conftest.describe(removed)
    assert backend.count("briefs", email=body["email"]) == 0, "a deleted brief is gone"


def test_brief_inbox_lists_briefs_newest_first(anon, owner):
    older, _ = conftest.send_brief(anon)
    newer, _ = conftest.send_brief(anon)
    emails = [str(b.get("email")) for b in _shapes.items(conftest.json_of(owner.get("/studio/briefs")))]
    assert emails.index(newer["email"]) < emails.index(older["email"]), (
        "the brief inbox lists briefs newest first")


def test_owner_dashboard_carries_the_unread_brief_count(owner):
    body = conftest.json_of(owner.get("/studio/dashboard"))
    assert isinstance(conftest.dig(body, "unread_briefs"), int), (
        f"the owner dashboard carries unread_briefs as a count: {body}")


def test_editor_dashboard_carries_no_unread_brief_count(editor):
    body = conftest.json_of(editor.get("/studio/dashboard"))
    assert "unread_briefs" not in _shapes.flatten(body), (
        f"an editor dashboard carries no unread brief count at all: {body}")
    assert "unread" not in _shapes.flatten(list(body.keys()) if isinstance(body, dict) else body), (
        f"an editor dashboard names no unread count: {body}")
    kinds = {str(row.get("kind")) for row in conftest.dig(body, "recent") or []}
    assert kinds <= {"case_study"}, f"an editor's recent list carries case studies only: {kinds}"


def test_dashboard_counts_published_and_draft_case_studies(owner):
    rows = _shapes.items(conftest.json_of(owner.get("/studio/work")))
    body = conftest.json_of(owner.get("/studio/dashboard"))
    published = sum(1 for r in rows if r.get("published") is True)
    assert int(conftest.dig(body, "published_count")) == published, (
        f"published_count must equal the published case studies ({published}): {body}")
    assert int(conftest.dig(body, "draft_count")) == len(rows) - published, (
        f"draft_count must equal the unpublished case studies ({len(rows) - published}): {body}")
    recent = conftest.dig(body, "recent")
    assert isinstance(recent, list) and recent, f"the dashboard lists recent changes: {body}"
    assert len(recent) <= 10, f"the recent list holds at most ten rows: {recent}"
    for row in recent:
        for field in conftest.RECENT_FIELDS:
            assert field in row, f"a recent row carries {field}: {row}"
        assert row.get("kind") in conftest.RECENT_KINDS, f"a recent row kind is case_study or brief: {row}"


def test_slug_is_kept_when_the_title_changes(owner):
    created = conftest.create_case(owner)
    version = conftest.version_of(owner, created["id"])
    response = owner.patch(f"/studio/work/{created['id']}",
                           json={"title": "A Renamed Probe", "version": version})
    assert response.status_code == 200, "renaming succeeds: " + conftest.describe(response)
    assert conftest.dig(conftest.read_case(owner, created["id"]), "slug") == created["slug"], (
        "a case study slug is kept when the title changes")


def test_duplicate_slug_is_refused_with_its_message(owner, backend):
    created = conftest.create_case(owner)
    response = owner.post("/studio/work", json=conftest.new_case_payload(slug=created["slug"]))
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "a slug already in use is refused: " + conftest.describe(response))
    assert conftest.MSG_SLUG_TAKEN in response.text, (
        f"the slug field reads {conftest.MSG_SLUG_TAKEN!r}: " + conftest.describe(response))
    assert conftest.dig(response.json(), "fields") is not None, (
        "an unprocessable refusal maps the failing field to its message: " + conftest.describe(response))
    assert backend.count("case_studies", slug=created["slug"]) == 1, "the slug stays unique"


def test_invalid_year_title_and_summary_are_refused(owner):
    for label, extra in (("a year before 1990", {"year": 1989}),
                         ("a three digit year", {"year": 999}),
                         ("a title over 120 characters", {"title": "T" * 121}),
                         ("a summary over 280 characters", {"summary": "S" * 281}),
                         ("a client over 80 characters", {"client": "C" * 81}),
                         ("a cover seed over 999999", {"cover_seed": 1000000}),
                         ("an unknown cover palette", {"cover_palette": "neon"})):
        response = owner.post("/studio/work", json=conftest.new_case_payload(**extra))
        assert response.status_code in conftest.REFUSED_CLIENT, (
            f"{label} must be refused as a client error: " + conftest.describe(response))


def test_case_study_tag_pair_is_stored_once(owner, backend):
    created = conftest.create_case(owner, tags=["banking", "banking"])
    row = backend.one("case_studies", slug=created["slug"])
    assert backend.count("case_study_tags", case_study_id=row["id"]) == 1, (
        "a tag pair appears once for a case study")


def test_signup_always_creates_a_visitor(backend):
    email = conftest.probe_email()
    response = conftest.signup(email, role="owner")
    assert response.status_code in (200, 201), "signup is open: " + conftest.describe(response)
    assert conftest.dig(response.json(), "role") == "visitor", (
        "signup always creates a visitor whatever the request says: " + conftest.describe(response))
    assert conftest.dig(response.json(), "access_token"), "signup returns an access_token"
    assert backend.one("accounts", email=email).get("role") == "visitor", (
        "the stored role of a signed-up account is visitor")
    assert backend.count("accounts", role="owner") == 1, "exactly one account holds the owner role"


def test_signup_refuses_an_existing_email_in_another_case(backend):
    response = conftest.signup(conftest.OWNER_EMAIL.upper())
    assert response.status_code in conftest.REFUSED_CLIENT, (
        "an account email is unique without regard to case: " + conftest.describe(response))
    assert backend.count("accounts", role="owner") == 1, "no second owner account exists"


def test_login_with_a_wrong_password_is_denied_with_the_shared_line():
    wrong = conftest.raw_login(conftest.EDITOR_EMAIL, "not-the-password-2026")
    unknown = conftest.raw_login(conftest.probe_email(), conftest.APP_PASSWORD)
    for response in (wrong, unknown):
        assert response.status_code in conftest.REFUSED_CLIENT, (
            "a failed sign in is refused: " + conftest.describe(response))
        assert conftest.MSG_SIGN_IN_FAILED in response.text, (
            f"a failed sign in reads {conftest.MSG_SIGN_IN_FAILED!r}: " + conftest.describe(response))


def test_five_failed_sign_ins_lock_the_account():
    email = conftest.probe_email()
    conftest.signup(email)
    for _ in range(5):
        conftest.raw_login(email, "wrong-password-2026")
    locked = conftest.raw_login(email, conftest.APP_PASSWORD)
    assert locked.status_code in conftest.REFUSED_CLIENT, (
        "a locked account refuses even the right password: " + conftest.describe(locked))
    assert conftest.MSG_LOCKED_PREFIX in locked.text, (
        f"the lockout line begins {conftest.MSG_LOCKED_PREFIX!r}: " + conftest.describe(locked))


def test_seeded_accounts_sign_in_with_their_roles_and_names():
    for email, role, name in ((conftest.OWNER_EMAIL, "owner", conftest.OWNER_NAME),
                              (conftest.EDITOR_EMAIL, "editor", conftest.EDITOR_NAME),
                              (conftest.VISITOR_EMAIL, "visitor", None)):
        response = conftest.raw_login(email, conftest.APP_PASSWORD)
        assert response.status_code == 200, f"{email} signs in: " + conftest.describe(response)
        body = response.json()
        assert conftest.dig(body, "role") == role, f"{email} holds the role {role}: {body}"
        if name is not None:
            assert name in response.text, f"{email} carries the display name {name}: {body}"


def test_passwords_and_session_tokens_are_stored_hashed(backend):
    response = conftest.raw_login(conftest.VISITOR_EMAIL, conftest.APP_PASSWORD)
    token = conftest.dig(response.json(), "access_token")
    account = backend.one("accounts", email=conftest.VISITOR_EMAIL)
    assert conftest.APP_PASSWORD not in str(account), "passwords are stored hashed"
    sessions = backend.rows("sessions", account_id=account["id"])
    assert sessions, "a sign in records a session row"
    assert all(token not in str(row) for row in sessions), (
        "the sessions table stores a hash of the token, never the token")


def test_visitor_is_denied_every_studio_endpoint(visitor, backend):
    for path in conftest.STUDIO_GET_ENDPOINTS:
        response = visitor.get(path)
        assert response.status_code in conftest.DENIED, (
            f"a visitor session must be denied {path}: " + conftest.describe(response))
    body = conftest.new_case_payload()
    response = visitor.post("/studio/work", json=body)
    assert response.status_code in conftest.DENIED, (
        "a visitor session must be denied creating a case study: " + conftest.describe(response))
    assert backend.count("case_studies", slug=body["slug"]) == 0, (
        "a refused visitor call leaves the stored state unchanged")


def test_unauthenticated_caller_is_denied_every_studio_endpoint(anon, backend):
    for path in conftest.STUDIO_GET_ENDPOINTS + ("/sessions", "/auth/me"):
        response = anon.get(path)
        assert response.status_code in conftest.DENIED, (
            f"a caller with no session must be denied {path}: " + conftest.describe(response))
        assert conftest.error_code(response) in conftest.ERROR_CODES, (
            "a refusal carries a pinned error code: " + conftest.describe(response))
    body = conftest.new_case_payload()
    response = anon.post("/studio/work", json=body)
    assert response.status_code in conftest.DENIED, (
        "a caller with no session is denied creating a case study: " + conftest.describe(response))
    assert backend.count("case_studies", slug=body["slug"]) == 0, (
        "a refused call with no session leaves the stored state unchanged")


def test_editor_is_forbidden_to_publish_or_unpublish(editor, owner, backend):
    draft = conftest.create_case(owner, expertise="corporate", tags=["banking"])
    conftest.generate_cover(owner, draft["id"])
    response = conftest.publish(editor, draft["id"])
    assert response.status_code in conftest.DENIED, (
        "an editor must be denied publishing: " + conftest.describe(response))
    assert backend.one("case_studies", slug=draft["slug"]).get("published") in (False, 0), (
        "a denied publish leaves the case study unpublished")
    live = conftest.create_published_case(owner, expertise="corporate", tags=["banking"])
    response = conftest.unpublish(editor, live["id"])
    assert response.status_code in conftest.DENIED, (
        "an editor must be denied unpublishing: " + conftest.describe(response))
    assert backend.one("case_studies", slug=live["slug"]).get("published") in (True, 1), (
        "a denied unpublish leaves the case study published")


def test_editor_is_forbidden_to_delete_a_case_study(editor, owner, backend):
    draft = conftest.create_case(owner)
    response = editor.request("DELETE", f"/studio/work/{draft['id']}",
                              json={"version": conftest.version_of(owner, draft["id"])})
    assert response.status_code in conftest.DENIED, (
        "an editor must be denied deleting: " + conftest.describe(response))
    assert backend.count("case_studies", slug=draft["slug"]) == 1, "a denied delete leaves the row"


def test_owner_deletes_a_draft_case_study(owner, backend):
    draft = conftest.create_case(owner)
    response = owner.request("DELETE", f"/studio/work/{draft['id']}",
                             json={"version": conftest.version_of(owner, draft["id"])})
    assert response.status_code in (200, 204), "the owner deletes a case study: " + conftest.describe(response)
    assert backend.count("case_studies", slug=draft["slug"]) == 0, "a deleted case study is gone"


def test_editor_creates_edits_and_covers_case_studies_and_reads_drafts(editor):
    listing = conftest.slugs_of(conftest.json_of(editor.get("/studio/work")))
    assert conftest.DRAFT_SLUG in listing, "an editor reads every case study, drafts included"
    created = conftest.create_case(editor)
    version = conftest.version_of(editor, created["id"])
    response = editor.patch(f"/studio/work/{created['id']}",
                            json={"summary": "An editor's revision.", "version": version})
    assert response.status_code == 200, "an editor edits a case study: " + conftest.describe(response)
    conftest.generate_cover(editor, created["id"])
    sessions = editor.get("/sessions")
    assert sessions.status_code == 200, "an editor sees their own sessions: " + conftest.describe(sessions)


def test_sign_out_everywhere_revokes_every_token():
    email = conftest.probe_email()
    first = conftest.dig(conftest.signup(email).json(), "access_token")
    second = conftest.dig(conftest.raw_login(email, conftest.APP_PASSWORD).json(), "access_token")
    with conftest.bearer_client(first) as c:
        listed = c.get("/sessions")
        assert listed.status_code == 200 and len(_shapes.items(listed.json())) >= 2, (
            "the session list carries every live session: " + conftest.describe(listed))
        rows = _shapes.items(listed.json())
        for row in rows:
            for field in conftest.SESSION_FIELDS:
                assert field in row, f"a session carries {field}: {row}"
        assert sum(1 for row in rows if row.get("current") is True) == 1, (
            f"exactly one session, the one making the request, is current: {rows}")
        ended = c.delete("/sessions")
        assert ended.status_code in (200, 204), "sign out everywhere succeeds: " + conftest.describe(ended)
    for token in (first, second):
        with conftest.bearer_client(token) as c:
            me = c.get("/auth/me")
            assert me.status_code in conftest.DENIED, (
                "every token of the account is refused after sign out everywhere: "
                + conftest.describe(me))


def test_page_view_is_recorded_for_a_public_route(anon, owner, backend):
    before = backend.count("page_views", route="/company")
    response = anon.post("/page-views", json={"route": "/company"})
    assert response.status_code in (200, 201), "a page view is recorded: " + conftest.describe(response)
    assert conftest.poll_until(lambda: backend.count("page_views", route="/company") == before + 1), (
        "one public page view records one row with its route")
    views = _shapes.items(conftest.json_of(owner.get("/studio/page-views")))
    assert views and str(views[0].get("route")) == "/company", (
        f"the owner reads the page-view log newest first: {views[:3]}")


def test_studio_routes_are_never_recorded_as_page_views(anon, backend):
    response = anon.post("/page-views", json={"route": "/studio/shelf"})
    assert response.status_code < 400, (
        "a studio route view is acknowledged: " + conftest.describe(response))
    conftest.settle()
    assert backend.count("page_views", route="/studio/shelf") == 0, (
        "studio routes are never recorded as page views")


def test_page_view_rows_record_nothing_beyond_route_and_time(backend):
    columns = backend.query(
        "SELECT column_name FROM information_schema.columns WHERE table_name = %s",
        ("page_views",))
    names = sorted(c["column_name"] for c in columns)
    assert names == ["id", "route", "viewed_at"], (
        f"a page view records nothing beyond the route and the time: {names}")


def test_editor_is_forbidden_the_page_view_log(editor):
    response = editor.get("/studio/page-views")
    assert response.status_code in conftest.DENIED, (
        "an editor must be denied the page-view log: " + conftest.describe(response))


def test_each_public_route_sets_its_own_title_and_description(page, app_base):
    seen_titles = []
    seen_descriptions = []
    for path, title in conftest.PUBLIC_TITLES:
        page.goto(f"{app_base}{path}")
        page.wait_for_function("t => document.title === t", arg=title, timeout=15000)
        description = page.locator("meta[name='description']").first.get_attribute("content")
        assert description, f"{path} must set a description of its own"
        seen_titles.append(page.title())
        seen_descriptions.append(description)
    assert len(set(seen_titles)) == len(seen_titles), f"no two routes share a title: {seen_titles}"
    assert len(set(seen_descriptions)) == len(seen_descriptions), (
        f"no two routes share a description: {seen_descriptions}")


def test_every_content_image_carries_alternative_text(page, app_base):
    for path in ("/", "/work", "/work/kestrel-annual-review"):
        page.goto(f"{app_base}{path}")
        page.wait_for_load_state("networkidle")
        missing = page.eval_on_selector_all(
            "img", "els => els.filter(e => !e.hasAttribute('alt')).map(e => e.outerHTML)")
        assert not missing, f"every image on {path} carries alternative text: {missing[:3]}"


def test_type_family_weights_and_sizes_follow_the_pinned_scale(page, app_base):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(f"{app_base}/")
    page.wait_for_load_state("networkidle")
    styles = page.eval_on_selector_all("body *", conftest.TEXT_STYLE_SCRIPT)
    assert styles, "the front page renders visible text"
    families = sorted({family for family, _, _ in styles})
    assert all(conftest.TYPE_FAMILY.lower() in f.lower() for f in families), (
        f"every visible text is set in {conftest.TYPE_FAMILY}: {families}")
    assert all(conftest.FALLBACK_FAMILY.lower() in f.lower() for f in families), (
        f"the family stack carries the pinned fallback {conftest.FALLBACK_FAMILY}: {families}")
    weights = sorted({weight for _, weight, _ in styles})
    assert set(weights) <= set(conftest.TYPE_WEIGHTS), (
        f"only the regular and medium cuts are used: {weights}")
    sizes = sorted({float(size.rstrip("px")) for _, _, size in styles})
    assert set(sizes) <= set(conftest.TYPE_SIZES_PX), (
        f"every text size at a wide window is a pinned step: {sizes}")
    assert conftest.DISPLAY_SIZE_PX in sizes, (
        f"the front page headline is set at the display size: {sizes}")


def test_not_found_page_answers_404_and_never_echoes_the_path(site, page, app_base):
    marker = f"no-such-page-{conftest.unique_token()}"
    response = site.get(f"/{marker}")
    assert response.status_code == 404, (
        "an unknown address answers not found: " + conftest.describe(response))
    page.goto(f"{app_base}/{marker}")
    page.wait_for_load_state("networkidle")
    assert marker not in page.inner_text("body"), (
        "the not found page never prints the requested path")


def test_sitemap_lists_published_routes_and_no_drafts(site):
    response = site.get("/sitemap.xml")
    assert response.status_code == 200, "the sitemap is served: " + conftest.describe(response)
    for slug in conftest.SEEDED_PUBLISHED_SLUGS:
        assert f"/work/{slug}" in response.text, f"the sitemap lists the published {slug}"
    for slug in conftest.EXPERTISE_SLUGS:
        assert f"/expertise/{slug}" in response.text, f"the sitemap lists the {slug} landing"
    for path in ("/company", "/contact", "/privacy-policy"):
        assert path in response.text, f"the sitemap lists {path}"
    assert conftest.DRAFT_SLUG not in response.text, "the sitemap lists no draft case study"
    assert conftest.WITHDRAWN_SLUG not in response.text, "the sitemap lists no withdrawn case study"


def test_robots_file_names_the_sitemap_and_keeps_crawlers_out_of_the_studio(site):
    response = site.get("/robots.txt")
    assert response.status_code == 200, "the robots file is served: " + conftest.describe(response)
    assert "sitemap" in response.text.lower() and "sitemap.xml" in response.text, (
        "the robots file names the sitemap: " + conftest.describe(response))
    assert "disallow: /studio" in response.text.lower(), (
        "the robots file keeps crawlers out of /studio: " + conftest.describe(response))


def test_security_headers_are_present_on_every_response(site):
    for path in ("/", "/work", "/api/health", "/api/work"):
        response = site.get(path)
        for header in conftest.SECURITY_HEADERS:
            assert header in response.headers, f"{path} must carry {header}: {dict(response.headers)}"
        assert response.headers["x-content-type-options"].lower() == "nosniff", (
            f"{path} refuses sniffing: {dict(response.headers)}")
        frame = response.headers.get("x-frame-options", "") + response.headers.get(
            "content-security-policy", "")
        assert "deny" in frame.lower() or "frame-ancestors 'none'" in frame.lower(), (
            f"{path} denies framing: {dict(response.headers)}")


def test_no_credential_is_served_to_the_browser(site):
    secrets = conftest.storage_credentials()
    home = site.get("/")
    bodies = [home.text]
    for src in conftest.script_sources(home.text):
        bodies.append(site.get(src).text)
    for body in bodies:
        for secret in secrets:
            assert secret not in body, "no object-store credential appears in a downloaded file"


def test_list_endpoints_return_top_level_arrays(anon, owner):
    for client, path in ((anon, "/work"), (owner, "/studio/work"), (owner, "/studio/slots"),
                         (owner, "/studio/briefs"), (owner, "/studio/page-views"),
                         (owner, "/sessions")):
        response = client.get(path)
        assert response.status_code == 200, f"{path} is readable: " + conftest.describe(response)
        assert isinstance(response.json(), list), f"{path} returns a top-level JSON array"


def test_case_study_response_carries_the_pinned_fields(owner):
    created = conftest.create_published_case(owner, expertise="corporate", tags=["banking"])
    for field in ("id", "slug", "title", "client", "year", "expertise", "tags", "summary",
                  "cover_seed", "cover_palette", "cover", "blocks", "position",
                  "published", "version"):
        assert field in created, f"a case study response carries {field}: {created}"
    cover = created["cover"]
    for field in ("id", "object_key", "alt_text", "width", "height"):
        assert field in cover, f"a cover response carries {field}: {cover}"


def test_schema_holds_the_named_tables_and_pinned_columns(backend):
    tables = {r["table_name"] for r in backend.query(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")}
    for name in conftest.TABLES:
        assert name in tables, f"the schema holds the table {name}: {sorted(tables)}"
    columns = {r["column_name"] for r in backend.query(
        "SELECT column_name FROM information_schema.columns WHERE table_name = %s",
        ("case_studies",))}
    for column in ("slug", "expertise_id", "cover_id", "blocks", "position", "published",
                   "published_at", "withdrawn_at", "author_id", "version"):
        assert column in columns, f"case_studies holds {column}: {sorted(columns)}"
    for table, wanted in conftest.PINNED_COLUMNS:
        have = {r["column_name"] for r in backend.query(
            "SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table,))}
        missing = sorted(set(wanted) - have)
        assert not missing, f"{table} lacks the pinned columns {missing}"


def test_seed_is_idempotent_across_a_restart(backend):
    for slug in conftest.SEEDED_ALL_SLUGS:
        assert backend.count("case_studies", slug=slug) == 1, (
            f"the seeded case study {slug} exists exactly once")
    assert backend.count("expertises") == 4, "exactly four expertises are seeded"
    assert backend.count("feature_slots") == 8, "exactly eight feature slots exist"
    for email in (conftest.OWNER_EMAIL, conftest.EDITOR_EMAIL, conftest.VISITOR_EMAIL):
        assert backend.count("accounts", email=email) == 1, f"{email} exists exactly once"
    for name in ("Ines Duval", "Tomas Berg", "Lea Park"):
        assert backend.count("briefs", name=name) == 1, f"the seeded brief from {name} exists once"
    for name, email, company, expertise, budget, comment in conftest.SEEDED_BRIEFS:
        row = backend.one("briefs", name=name)
        assert (row["email"], row["company"], row["expertise"], row["budget"], row["comment"]) == (
            email, company, expertise, budget, comment), f"the seeded brief from {name} reads as pinned: {row}"
    ines = backend.one("briefs", name="Ines Duval")
    assert conftest.INES_MARKUP in str(ines.get("comment")), (
        f"the seeded brief from Ines Duval carries the pinned markup: {ines}")


def test_seeded_case_studies_read_as_pinned(backend):
    for place, (slug, title, client, year, expertise, state) in enumerate(conftest.SEEDED_ROWS, 1):
        row = backend.one("case_studies", slug=slug)
        assert row is not None, f"the seeded case study {slug} exists"
        assert (row["title"], row["client"], int(row["year"])) == (title, client, int(year)), (
            f"the seeded case study {slug} reads as pinned: {row}")
        exp = backend.one("expertises", id=row["expertise_id"])
        assert exp is not None and exp["slug"] == expertise, (
            f"the seeded case study {slug} belongs to {expertise}: {exp}")
        assert (int(row["cover_seed"]), row["cover_palette"]) == (place, "mono"), (
            f"the seeded case study {slug} has cover seed {place} and palette mono: {row}")
        tags = backend.query(
            "SELECT t.slug FROM tags t JOIN case_study_tags ct ON ct.tag_id = t.id WHERE ct.case_study_id = %s",
            (row["id"],))
        assert sorted(t["slug"] for t in tags) == sorted(conftest.SEEDED_TAGS[slug]), (
            f"the seeded case study {slug} carries the pinned tags: {tags}")
        if state == "draft":
            assert row["published"] in (False, 0) and row.get("withdrawn_at") is None, (
                f"{slug} is seeded as a draft: {row}")
        elif state == "withdrawn":
            assert row["published"] in (False, 0) and row.get("withdrawn_at") is not None, (
                f"{slug} is seeded as withdrawn: {row}")


def test_seeded_case_studies_carry_covers_in_the_bucket(backend, store):
    for slug in conftest.SEEDED_ALL_SLUGS:
        row = backend.one("case_studies", slug=slug)
        cover = backend.one("covers", id=row["cover_id"])
        assert cover is not None and cover.get("alt_text"), (
            f"the seeded case study {slug} carries a cover with alternative text")
        assert store.exists(cover["object_key"]), (
            f"the seeded cover of {slug} exists in the bucket at {cover['object_key']}")


def test_shelf_holds_one_row_with_a_whole_version(backend, owner):
    rows = backend.query("SELECT id, version FROM shelf", ())
    assert len(rows) == 1, f"the shelf table holds one row: {rows}"
    assert int(rows[0]["version"]) >= 1, f"the shelf version starts at one and only rises: {rows}"
    version, _ = conftest.shelf_state(owner)
    assert int(version) == int(rows[0]["version"]), "the shelf version read by the studio is the stored one"
