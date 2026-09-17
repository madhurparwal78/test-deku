from __future__ import annotations

import httpx

import appclient
import conftest as fixtures


def test_health_route_answers_ready():
    """The health route answers 200 once PostgreSQL and the bucket are reachable."""
    response = httpx.get(f"{appclient.api_base()}{fixtures.HEALTH_ROUTE}",
                         timeout=appclient.TIMEOUT)
    assert response.status_code == fixtures.HEALTH_STATUS, (
        f"GET /api/health answered {response.status_code} rather than "
        f"{fixtures.HEALTH_STATUS}: {response.text[:300]}")


def test_seeded_projects_are_listed_in_registry_order():
    """The public project list carries the five published records in order."""
    records = fixtures.public_projects()
    keys = [record.get("key") for record in records]
    assert keys == list(fixtures.REGISTRY_ORDER), (
        f"GET /api/projects returned {keys}, and the registry order is "
        f"{list(fixtures.REGISTRY_ORDER)}")
    orders = [record.get("order") for record in records]
    assert orders == sorted(orders), (
        f"GET /api/projects returned the orders {orders}, which do not ascend")
    assert fixtures.DRAFT_KEY not in keys, (
        f"GET /api/projects carries the draft {fixtures.DRAFT_KEY!r}: {keys}")


def test_published_project_record_carries_its_derived_eyebrow_and_path():
    """A published case study record carries every field the contract names."""
    key = "tide"
    record = fixtures.public_project(key)
    for field in fixtures.PROJECT_RECORD_KEYS:
        assert field in record, (
            f"GET /api/projects/{key} is missing the field {field!r}: "
            f"{sorted(record)}")
    assert record["eyebrow"] == f"{fixtures.SELECTED_WORK_PREFIX}Tide", (
        f"GET /api/projects/{key} carries the eyebrow {record['eyebrow']!r}, and "
        f"the contract derives it from the menu label")
    assert record["path"] == f"/case-study/{key}", (
        f"GET /api/projects/{key} carries the path {record['path']!r} rather than "
        f"the case study route")
    assert record["id"] == fixtures.CREATION_IDS[key], (
        f"GET /api/projects/{key} carries the creation id {record['id']!r} rather "
        f"than {fixtures.CREATION_IDS[key]!r}")
    assert record["category"] in fixtures.CATEGORIES, (
        f"GET /api/projects/{key} carries the category {record['category']!r}, "
        f"outside the five the composer allows")
    assert record["opens"] in fixtures.OPENS_VALUES, (
        f"GET /api/projects/{key} carries opens {record['opens']!r}, outside the "
        f"three the record allows")


def test_case_study_hub_order_differs_from_the_registry_order():
    """The hub sorts published case studies by hubOrder, not registry order."""
    records = [record for record in fixtures.public_projects()
               if record.get("opens") == "caseStudy"]
    by_hub = sorted(records, key=lambda record: record.get("hubOrder"))
    keys = [record.get("key") for record in by_hub]
    assert keys == list(fixtures.HUB_ORDER), (
        f"the published case studies sorted by hubOrder are {keys}, and the "
        f"seeded hub order is {list(fixtures.HUB_ORDER)}")
    labels = [record.get("menuLabel") for record in by_hub]
    assert labels == list(fixtures.HUB_LABELS), (
        f"the hub cells read {labels} rather than {list(fixtures.HUB_LABELS)}")


def test_journey_desktop_tile_bands_match_the_pinned_timing_table():
    """The desktop journey returns the five pinned tile bands and menu targets."""
    document = fixtures.journey("desktop", fixtures.DEFAULT_VIEWPORT_HEIGHT)
    assert document.get("branch") == "desktop", (
        f"GET /api/journey answered the branch {document.get('branch')!r}")
    tiles = document.get("tiles") or []
    assert len(tiles) == len(fixtures.REGISTRY_ORDER), (
        f"the desktop journey carries {len(tiles)} tile bands for "
        f"{len(fixtures.REGISTRY_ORDER)} published projects: {tiles}")
    starts = [tile.get("start") for tile in tiles]
    assert starts == list(fixtures.DESKTOP_BAND_EDGES[:-1]), (
        f"the desktop tile band starts are {starts}, and the brief pins "
        f"{list(fixtures.DESKTOP_BAND_EDGES[:-1])}")
    assert tiles[-1].get("end") == fixtures.DESKTOP_BAND_EDGES[-1], (
        f"the last desktop band ends at {tiles[-1].get('end')} rather than "
        f"{fixtures.DESKTOP_BAND_EDGES[-1]}")
    targets = [tile.get("menuTarget") for tile in tiles]
    assert targets == list(fixtures.DESKTOP_MENU_TARGETS), (
        f"the desktop menu targets are {targets}, and the brief pins "
        f"{list(fixtures.DESKTOP_MENU_TARGETS)}")
    assert document.get("fadeIn") == fixtures.DESKTOP_FADE_IN, (
        f"the desktop journey carries the fade in {document.get('fadeIn')} "
        f"rather than {fixtures.DESKTOP_FADE_IN}")
    assert document.get("fadeOut") == fixtures.DESKTOP_FADE_OUT, (
        f"the desktop journey carries the fade out {document.get('fadeOut')} "
        f"rather than {fixtures.DESKTOP_FADE_OUT}")
    names = [component.get("name") for component in document.get("components") or []]
    for name in fixtures.JOURNEY_COMPONENTS:
        assert name in names, (
            f"the desktop journey names no component {name!r}: {names}")
    for name, (start, end) in fixtures.DESKTOP_COMPONENT_BANDS.items():
        component = fixtures.component_for(document, name)
        assert (component.get("start"), component.get("end")) == (start, end), (
            f"the desktop component {name!r} runs "
            f"{component.get('start')} to {component.get('end')}, and the brief "
            f"pins {start} to {end}")


def test_journey_mobile_branch_carries_its_own_band_and_pages():
    """The mobile branch runs its own tile band, fades and page count."""
    document = fixtures.journey("mobile", fixtures.DEFAULT_VIEWPORT_HEIGHT)
    assert document.get("branch") == "mobile", (
        f"the mobile journey answered the branch {document.get('branch')!r}")
    assert document.get("pages") == fixtures.MOBILE_PAGES, (
        f"the mobile journey runs {document.get('pages')} pages rather than "
        f"{fixtures.MOBILE_PAGES}")
    assert document.get("fadeIn") == fixtures.MOBILE_FADE_IN, (
        f"the mobile journey carries the fade in {document.get('fadeIn')} rather "
        f"than {fixtures.MOBILE_FADE_IN}")
    assert document.get("fadeOut") == fixtures.MOBILE_FADE_OUT, (
        f"the mobile journey carries the fade out {document.get('fadeOut')} "
        f"rather than {fixtures.MOBILE_FADE_OUT}")
    tiles = document.get("tiles") or []
    assert tiles, f"the mobile journey carries no tile bands: {document}"
    assert tiles[0].get("start") == fixtures.MOBILE_BAND[0], (
        f"the mobile tile band opens at {tiles[0].get('start')} rather than "
        f"{fixtures.MOBILE_BAND[0]}")
    assert tiles[-1].get("end") == fixtures.MOBILE_BAND[1], (
        f"the mobile tile band closes at {tiles[-1].get('end')} rather than "
        f"{fixtures.MOBILE_BAND[1]}")
    for name, (start, end) in fixtures.MOBILE_COMPONENT_BANDS.items():
        component = fixtures.component_for(document, name)
        assert (component.get("start"), component.get("end")) == (start, end), (
            f"the mobile component {name!r} runs {component.get('start')} to "
            f"{component.get('end')}, and the brief pins {start} to {end}")


def test_journey_pages_follow_the_viewport_height():
    """Journey travel is a constant distance and pages follow the window."""
    tall = fixtures.journey("desktop", 1110)
    short = fixtures.journey("desktop", fixtures.DEFAULT_VIEWPORT_HEIGHT)
    assert short.get("pages") == fixtures.DESKTOP_PAGES_AT_900, (
        f"a 900 tall window runs {short.get('pages')} pages rather than "
        f"{fixtures.DESKTOP_PAGES_AT_900}")
    assert tall.get("pages") == fixtures.DESKTOP_PAGES_AT_1110, (
        f"a 1110 tall window runs {tall.get('pages')} pages rather than "
        f"{fixtures.DESKTOP_PAGES_AT_1110}")
    assert short.get("travelPx") == fixtures.JOURNEY_TRAVEL, (
        f"a 900 tall window travels {short.get('travelPx')} rather than "
        f"{fixtures.JOURNEY_TRAVEL}")


def test_journey_refuses_an_unknown_branch_and_a_bad_viewport():
    """An unknown branch and a non-positive viewport are both client errors."""
    unknown = fixtures.journey_response(branch="holographic")
    code = fixtures.refusal_code(unknown, "GET /api/journey with an unknown branch")
    assert fixtures.INVALID_BRANCH in code, (
        f"an unknown branch answered the code {code!r} rather than "
        f"{fixtures.INVALID_BRANCH!r}")
    bad = fixtures.journey_response(branch="desktop", viewportHeight=0)
    code = fixtures.refusal_code(bad, "GET /api/journey with a zero viewport")
    assert fixtures.INVALID_VIEWPORT in code, (
        f"a zero viewport answered the code {code!r} rather than "
        f"{fixtures.INVALID_VIEWPORT!r}")


def test_journey_band_count_matches_the_published_project_count():
    """Every published project owns one equal band and a draft owns none."""
    document = fixtures.journey("desktop", fixtures.DEFAULT_VIEWPORT_HEIGHT)
    tiles = document.get("tiles") or []
    keys = [tile.get("key") for tile in tiles]
    assert keys == list(fixtures.REGISTRY_ORDER), (
        f"the journey bands are keyed {keys}, and the published registry order "
        f"is {list(fixtures.REGISTRY_ORDER)}")
    assert fixtures.DRAFT_KEY not in keys, (
        f"the draft {fixtures.DRAFT_KEY!r} received a journey band: {keys}")
    widths = [round(tile["end"] - tile["start"], 4) for tile in tiles]
    assert len(set(widths)) == 1, (
        f"the journey bands are {widths} wide, and the band is divided into "
        f"equal parts")


def test_curriculum_vitae_selected_work_is_generated_from_the_records():
    """Selected Work is built from the published case studies, never retyped."""
    document = fixtures.cv_document()
    entries = document.get("selectedWork") or []
    keys = [entry.get("key") for entry in entries]
    published = [record.get("key") for record in fixtures.public_projects()
                 if record.get("cv")]
    assert keys == [key for key in fixtures.REGISTRY_ORDER if key in published], (
        f"GET /api/cv lists the selected work {keys}, which does not follow the "
        f"published registry order {published}")
    for entry in entries:
        for field in fixtures.CV_ENTRY_KEYS:
            assert field in entry, (
                f"the selected work entry {entry.get('key')!r} is missing "
                f"{field!r}: {sorted(entry)}")
        for bullet in entry.get("bullets") or []:
            assert any(character.isdigit() for character in bullet), (
                f"the selected work bullet {bullet!r} on "
                f"{entry.get('key')!r} carries no numeral")
    for fact in fixtures.CV_FACTS:
        assert fact in fixtures.flat(document.get("facts")).replace('"', ""), (
            f"GET /api/cv states no fact matching {fact!r}: "
            f"{document.get('facts')}")


def test_search_groups_results_in_the_fixed_weight_order():
    """Search results are grouped by type in the fixed weight order."""
    document = fixtures.search(fixtures.TOOL_TAG)
    kinds = [group.get("type") for group in document.get("groups") or []]
    expected = [kind for kind in fixtures.SEARCH_TYPE_ORDER if kind in kinds]
    assert kinds == expected, (
        f"the search for {fixtures.TOOL_TAG!r} grouped {kinds}, and the fixed "
        f"weight order is {expected}")
    projects = fixtures.group_for(document, "project")
    assert projects, (
        f"the search for {fixtures.TOOL_TAG!r} found no project group: {kinds}")
    titles = [result.get("title") for result in projects.get("results") or []]
    assert titles, f"the project group carries no result: {projects}"
    scores = [result.get("score") for result in projects.get("results") or []]
    assert scores == sorted(scores, reverse=True), (
        f"the project group scores {scores} do not descend")
    for result in projects.get("results") or []:
        for field in fixtures.SEARCH_RESULT_KEYS:
            assert field in result, (
                f"a project result is missing {field!r}: {sorted(result)}")


def test_search_index_documents_carry_their_type_weight():
    """Each indexed document carries the weight its type is pinned to."""
    index = fixtures.search_index()
    documents = index.get("documents") or []
    assert documents, f"GET /api/search-index carries no document: {index}"
    weights = dict(fixtures.SEARCH_TYPE_WEIGHTS)
    for document in documents:
        for field in fixtures.SEARCH_DOCUMENT_KEYS:
            assert field in document, (
                f"an indexed document is missing {field!r}: {sorted(document)}")
        kind = document.get("type")
        assert kind in weights, (
            f"an indexed document carries the type {kind!r}, outside the seven "
            f"the brief weights")
        assert document.get("weight") == weights[kind], (
            f"a {kind!r} document carries the weight {document.get('weight')} "
            f"rather than {weights[kind]}")
    keys = {document.get("route") for document in documents}
    assert not any(f"/case-study/{fixtures.DRAFT_KEY}" == route for route in keys), (
        f"the search index carries the draft route for {fixtures.DRAFT_KEY!r}: "
        f"{sorted(keys)[:8]}")


def test_search_offers_tag_suggestions_when_nothing_matched():
    """An unmatched query returns no result and the most used tags instead."""
    document = fixtures.search(fixtures.fresh_token("zzq"))
    assert document.get("total") == 0, (
        f"an unmatched query reported {document.get('total')} results: "
        f"{document.get('groups')}")
    suggestions = document.get("suggestions") or []
    assert len(suggestions) == fixtures.SUGGESTION_COUNT, (
        f"an unmatched query offered {len(suggestions)} suggestions rather than "
        f"{fixtures.SUGGESTION_COUNT}: {suggestions}")


def test_highlights_entry_shows_the_published_run_figures():
    """The published run returns its frozen figures and its dwell histogram."""
    response = httpx.get(f"{appclient.api_base()}/runs/{fixtures.SEEDED_RUN}",
                         timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"GET /api/runs/{fixtures.SEEDED_RUN} answered {response.status_code}: "
        f"{response.text[:300]}")
    figures = response.json()
    for field in fixtures.FIGURE_KEYS:
        assert field in figures, (
            f"the published run is missing the figure {field!r}: "
            f"{sorted(figures)}")
    assert figures["visits"] == fixtures.RUN_VISITS, (
        f"the published run reports {figures['visits']} visits rather than "
        f"{fixtures.RUN_VISITS}")
    assert figures["staysBeyond15"] == fixtures.RUN_STAYS_BEYOND_15, (
        f"the published run reports {figures['staysBeyond15']} stays beyond 15 "
        f"seconds rather than {fixtures.RUN_STAYS_BEYOND_15}")
    assert figures["completeViewings"] == fixtures.RUN_COMPLETE_VIEWINGS, (
        f"the published run reports {figures['completeViewings']} complete "
        f"viewings rather than {fixtures.RUN_COMPLETE_VIEWINGS}")
    assert figures["medianDwellSeconds"] == fixtures.RUN_MEDIAN_DWELL, (
        f"the published run reports a median dwell of "
        f"{figures['medianDwellSeconds']} rather than {fixtures.RUN_MEDIAN_DWELL}")
    bins = [row.get("bin") for row in figures.get("dwellHistogram") or []]
    assert bins == list(fixtures.DWELL_BINS), (
        f"the dwell histogram carries the bins {bins} rather than "
        f"{list(fixtures.DWELL_BINS)}")


def test_flat_route_carries_the_plain_version_notice():
    """The plain version states what it is and offers the moving one."""
    markup = fixtures.page_body("/flat")
    assert fixtures.FLAT_FOOT in markup, (
        f"/flat carries no plain version notice; the foot must read "
        f"{fixtures.FLAT_FOOT!r}")
    assert fixtures.FLAT_RETURN in markup, (
        f"/flat offers no {fixtures.FLAT_RETURN!r} control")
    for key in fixtures.REGISTRY_ORDER:
        assert fixtures.MENU_LABELS[key] in markup, (
            f"/flat omits the published registry entry {fixtures.MENU_LABELS[key]!r}")
    assert fixtures.MENU_LABELS[fixtures.DRAFT_KEY] not in markup, (
        f"/flat carries the draft entry {fixtures.MENU_LABELS[fixtures.DRAFT_KEY]!r}")


def test_owner_upload_is_stored_in_the_bucket_under_its_sha256_object_key(owner, store, db):
    """An uploaded image lands in MinIO under the hash of its own bytes."""
    key = "tide"
    payload = fixtures.png_bytes(tone=29)
    digest = fixtures.digest_of(payload)
    response = fixtures.upload_media(owner, key, payload)
    assert response.status_code < 300, (
        f"POST /api/projects/{key}/media answered {response.status_code}: "
        f"{response.text[:300]}")
    record = response.json()
    object_key = record.get("objectKey")
    assert object_key == f"{fixtures.MEDIA_KEY_PREFIX}tide/{digest}.png", (
        f"the upload was stored at {object_key!r}, and the brief pins "
        f"{fixtures.MEDIA_KEY_PREFIX}tide/{digest}.png")
    assert record.get("sha256") == digest, (
        f"the upload reported the digest {record.get('sha256')!r} rather than "
        f"{digest!r}")
    assert record.get("sizeBytes") == len(payload), (
        f"the upload reported {record.get('sizeBytes')} bytes for a "
        f"{len(payload)} byte image")
    assert store.exists(object_key), (
        f"the object {object_key!r} is absent from the bucket, so the bytes were "
        f"kept somewhere other than the declared object store")
    assert db.count("project_media", object_key=object_key) == 1, (
        f"the object {object_key!r} has no single project_media row")


def test_identical_uploads_leave_exactly_one_stored_object_and_row(owner, store, db):
    """The same bytes uploaded twice leave one object and one row."""
    payload = fixtures.png_bytes(tone=31)
    digest = fixtures.digest_of(payload)
    first = fixtures.upload_media(owner, "tide", payload)
    second = fixtures.upload_media(owner, "tide", payload)
    assert first.status_code < 300 and second.status_code < 300, (
        f"the identical uploads answered {first.status_code} and "
        f"{second.status_code}: {second.text[:300]}")
    assert first.json().get("objectKey") == second.json().get("objectKey"), (
        f"the identical uploads returned the object keys "
        f"{first.json().get('objectKey')!r} and "
        f"{second.json().get('objectKey')!r}, which must be one key")
    object_key = first.json().get("objectKey")
    matches = [key for key in store.list(f"{fixtures.MEDIA_KEY_PREFIX}tide/")
               if key == object_key]
    assert len(matches) == 1, (
        f"the bucket carries {len(matches)} objects at {object_key!r}, and two "
        f"identical uploads leave exactly one")
    assert db.count("project_media", object_key=object_key) == 1, (
        f"the object {object_key!r} carries "
        f"{db.count('project_media', object_key=object_key)} project_media rows "
        f"rather than one")
    assert digest in object_key, (
        f"the object key {object_key!r} does not carry the digest {digest!r}")


def test_published_media_file_is_served_byte_for_byte_from_the_object_store(owner):
    """A published project's media is returned to anyone, unchanged."""
    key = "lumenar"
    payload = fixtures.png_bytes(tone=37)
    response = fixtures.upload_media(owner, key, payload)
    assert response.status_code < 300, (
        f"POST /api/projects/{key}/media answered {response.status_code}: "
        f"{response.text[:300]}")
    object_key = response.json().get("objectKey")
    served = httpx.get(f"{appclient.api_base()}/media/{object_key}",
                       timeout=appclient.TIMEOUT)
    assert served.status_code == 200, (
        f"GET /api/media/{object_key} answered {served.status_code} to a signed "
        f"out reader of published work: {served.text[:200]}")
    assert served.content == payload, (
        f"GET /api/media/{object_key} returned {len(served.content)} bytes for a "
        f"{len(payload)} byte upload, so the bytes are not the stored ones")
    assert "image" in served.headers.get("content-type", ""), (
        f"GET /api/media/{object_key} answered the content type "
        f"{served.headers.get('content-type')!r}")


def test_contact_message_is_persisted_as_a_row_the_owner_reads(owner, db):
    """A contact message becomes a real row the owner reads newest first."""
    sender = fixtures.fresh_email("visitor")
    response = fixtures.send_contact(email=sender)
    assert response.status_code < 300, (
        f"POST /api/contact answered {response.status_code}: "
        f"{response.text[:300]}")
    assert response.json().get("ok") is True, (
        f"POST /api/contact answered {response.json()} rather than an ok of true")
    assert db.count("contact_messages", email=sender) == 1, (
        f"the message from {sender} has no single contact_messages row")
    listed = owner.get("/admin/messages")
    assert listed.status_code == 200, (
        f"GET /api/admin/messages answered {listed.status_code}: "
        f"{listed.text[:300]}")
    rows = listed.json()
    assert any(row.get("email") == sender for row in rows), (
        f"the console does not carry the message from {sender}: "
        f"{[row.get('email') for row in rows[:5]]}")
    stamps = [row.get("createdAt") for row in rows]
    assert stamps == sorted(stamps, reverse=True), (
        f"the console lists messages {stamps[:4]}, which are not newest first")


def test_discarded_contact_submission_stores_no_row(db):
    """A filled honeypot or a fast submission is answered ok and stored nowhere."""
    trapped = fixtures.fresh_email("trapped")
    response = fixtures.send_contact(email=trapped, website="https://spam.example")
    assert response.status_code < 300, (
        f"a trapped submission answered {response.status_code}: "
        f"{response.text[:300]}")
    assert response.json().get("ok") is True, (
        f"a trapped submission answered {response.json()} rather than an ok of "
        f"true, which tells the sender it was discarded")
    assert db.count("contact_messages", email=trapped) == 0, (
        f"the trapped submission from {trapped} was stored as a row")
    hurried = fixtures.fresh_email("hurried")
    response = fixtures.send_contact(email=hurried, elapsedMs=100)
    assert response.json().get("ok") is True, (
        f"a hurried submission answered {response.json()} rather than an ok of true")
    assert db.count("contact_messages", email=hurried) == 0, (
        f"the hurried submission from {hurried} was stored as a row")


def test_page_view_is_recorded_with_its_route_and_time_only(owner, db):
    """A public page view is stored as a route and a time and nothing else."""
    before = db.count("page_views", route="/cv")
    response = httpx.post(f"{appclient.api_base()}/page-views",
                          json={"route": "/cv"}, timeout=appclient.TIMEOUT)
    assert response.status_code < 300, (
        f"POST /api/page-views answered {response.status_code}: "
        f"{response.text[:300]}")
    after = fixtures.settle(
        lambda: db.count("page_views", route="/cv") > before,
        "the page view row for /cv")
    assert after, f"the page view for /cv was never stored; count stayed {before}"
    logged = owner.get("/admin/page-views")
    assert logged.status_code == 200, (
        f"GET /api/admin/page-views answered {logged.status_code}: "
        f"{logged.text[:300]}")
    rows = logged.json()
    assert len(rows) <= 500, (
        f"the page view log returned {len(rows)} rows, and the contract caps it "
        f"at 500")
    for row in rows[:20]:
        assert set(row) <= {"route", "viewedAt"}, (
            f"a page view row carries {sorted(row)}, and only the route and the "
            f"time are kept")
        assert "?" not in str(row.get("route")), (
            f"the page view row {row.get('route')!r} carries a query string")


def test_review_body_never_changes_once_it_is_confirmed(owner, reviewer, db):
    """A confirmed review body is refused to every editing route."""
    confirmed = fixtures.admin_review(owner, "confirmed")
    review_id = confirmed.get("id")
    original = confirmed.get("body")
    assert original, f"the confirmed review carries no body: {confirmed}"
    for route in (f"/admin/reviews/{review_id}", f"/my/reviews/{review_id}"):
        response = owner.put(route, json={"body": "A rewritten endorsement."})
        assert response.status_code >= 400, (
            f"PUT {route} answered {response.status_code}, and no endpoint in any "
            f"role edits a review body: {response.text[:200]}")
    stored = db.one("reviews", public_id=review_id) or {}
    assert stored.get("body", original) == original, (
        f"the stored review body changed after an edit attempt: "
        f"{stored.get('body', '')[:80]!r}")
    again = fixtures.admin_review(owner, "confirmed")
    assert again.get("body") == original, (
        f"the console now reads the confirmed body as "
        f"{again.get('body', '')[:80]!r} rather than the writer own words")


def test_telemetry_event_triple_is_stored_exactly_once(owner, db):
    """A replayed batch stores each device, boot and seq triple one time."""
    run = fixtures.open_run(owner)
    device = fixtures.provision_device(owner, run.get("runId"))
    boot = fixtures.fresh_token("boot")
    events = fixtures.presence_events(30)
    first = fixtures.ingest(device["deviceKey"], device["deviceId"], boot, events)
    assert first.status_code < 300, (
        f"POST /api/ingest answered {first.status_code}: {first.text[:300]}")
    assert first.json().get("accepted") == len(events), (
        f"the first batch reported {first.json().get('accepted')} accepted for "
        f"{len(events)} new events")
    replay = fixtures.ingest(device["deviceKey"], device["deviceId"], boot, events)
    assert replay.status_code < 300, (
        f"the replayed batch answered {replay.status_code}: {replay.text[:300]}")
    assert replay.json().get("accepted") == 0, (
        f"the replayed batch reported {replay.json().get('accepted')} accepted, "
        f"and a replay carries no new event")
    assert replay.json().get("nextIntervalMs") >= fixtures.MIN_INGEST_INTERVAL_MS, (
        f"the ingest answered nextIntervalMs "
        f"{replay.json().get('nextIntervalMs')}, below the floor of "
        f"{fixtures.MIN_INGEST_INTERVAL_MS}")
    for event in events:
        stored = db.count("telemetry_events", device_id=device["deviceId"],
                          boot_id=boot, seq=event["seq"])
        assert stored == 1, (
            f"the event at seq {event['seq']} has {stored} telemetry_events rows "
            f"rather than one")


def test_published_run_figures_stay_frozen_after_later_events(owner):
    """Events arriving after publication never move a published run figure."""
    before = httpx.get(f"{appclient.api_base()}/runs/{fixtures.SEEDED_RUN}",
                       timeout=appclient.TIMEOUT)
    assert before.status_code == 200, (
        f"GET /api/runs/{fixtures.SEEDED_RUN} answered {before.status_code}")
    device = fixtures.provision_device(owner, fixtures.SEEDED_RUN)
    boot = fixtures.fresh_token("boot")
    late = fixtures.ingest(device["deviceKey"], device["deviceId"], boot,
                           fixtures.presence_events(45))
    assert late.status_code < 300, (
        f"a late batch answered {late.status_code}: {late.text[:300]}")
    after = httpx.get(f"{appclient.api_base()}/runs/{fixtures.SEEDED_RUN}",
                      timeout=appclient.TIMEOUT)
    assert after.json() == before.json(), (
        f"the published run figures moved after a late batch: "
        f"{before.json()} then {after.json()}")
    republished = owner.post(f"/admin/runs/{fixtures.SEEDED_RUN}/publish")
    assert republished.status_code >= 400, (
        f"republishing {fixtures.SEEDED_RUN} answered "
        f"{republished.status_code}, and a published run is frozen")


def test_publishing_through_the_composer_stores_a_draft_record(owner, db):
    """A new key saved through the composer is stored as a draft."""
    key = fixtures.fresh_token("probe").replace("_", "-")
    record = {"menuLabel": "Probe", "lines": ["A PROBE RECORD", "FOR THE COMPOSER"],
              "category": "LAB", "note": "Work the probe", "opens": "none",
              "labels": {"what": "PROBE", "tools": "CODE", "method": "PROBE"},
              "body": []}
    response = owner.put(f"/projects/{key}", json=record)
    assert response.status_code < 300, (
        f"PUT /api/projects/{key} answered {response.status_code}: "
        f"{response.text[:300]}")
    assert response.json().get("valid") is True, (
        f"the composer rejected a valid record: {response.json()}")
    stored = db.one("projects", key=key)
    assert stored, f"the composer stored no projects row for {key!r}"
    assert stored.get("status") == "draft", (
        f"the new record {key!r} was stored with the status "
        f"{stored.get('status')!r} rather than draft")
    listed = [row.get("key") for row in fixtures.public_projects()]
    assert key not in listed, (
        f"the new draft {key!r} reached the public project list: {listed}")


def test_anonymous_caller_is_denied_every_console_endpoint(anon):
    """A signed-out caller reaches no console route."""
    routes = ("/admin/messages", "/admin/projects", "/admin/invitations",
              "/admin/reviews", "/admin/page-views", "/admin/runs",
              "/my/reviews")
    for route in routes:
        fixtures.denied(anon.get(route), f"GET /api{route} with no session")
    created = anon.post("/admin/invitations",
                        json={"email": fixtures.fresh_email("guest"),
                              "scope": "tide"})
    fixtures.denied(created, "POST /api/admin/invitations with no session")


def test_reviewer_is_denied_every_admin_endpoint(reviewer):
    """A reviewer session reaches no owner console endpoint."""
    for route in ("/admin/messages", "/admin/projects", "/admin/invitations",
                  "/admin/reviews", "/admin/page-views", "/admin/runs"):
        fixtures.denied(reviewer.get(route), f"GET /api{route} as a reviewer")
    issued = reviewer.post("/admin/invitations",
                           json={"email": fixtures.fresh_email("guest"),
                                 "scope": "tide"})
    fixtures.denied(issued, "POST /api/admin/invitations as a reviewer")
    provisioned = reviewer.post("/admin/devices",
                                json={"deviceId": fixtures.fresh_token("device"),
                                      "runId": fixtures.SEEDED_RUN})
    fixtures.denied(provisioned, "POST /api/admin/devices as a reviewer")


def test_reviewer_is_denied_the_composer_endpoints(reviewer, db):
    """A reviewer writes no project record, media, preview or publication."""
    before = db.one("projects", key="tide") or {}
    key = "tide"
    edited = reviewer.put(f"/projects/{key}", json={"menuLabel": "Seized"})
    fixtures.denied(edited, f"PUT /api/projects/{key} as a reviewer")
    published = reviewer.post(f"/projects/{fixtures.DRAFT_KEY}/publish")
    fixtures.denied(published,
                    f"POST /api/projects/{fixtures.DRAFT_KEY}/publish as a reviewer")
    previewed = reviewer.post(f"/projects/{fixtures.DRAFT_KEY}/preview")
    fixtures.denied(previewed,
                    f"POST /api/projects/{fixtures.DRAFT_KEY}/preview as a reviewer")
    uploaded = fixtures.upload_media(reviewer, key)
    fixtures.denied(uploaded, f"POST /api/projects/{key}/media as a reviewer")
    after = db.one("projects", key=key) or {}
    assert after.get("menu_label") == before.get("menu_label"), (
        f"the tide record changed under a denied reviewer write: "
        f"{before.get('menu_label')!r} became {after.get('menu_label')!r}")


def test_reviewer_cannot_act_on_another_reviewers_review(owner, other_reviewer, db):
    """One reviewer neither confirms nor withdraws another writer review."""
    target = fixtures.admin_review(owner, "awaiting_confirmation")
    review_id = target.get("id")
    before = db.one("reviews", public_id=review_id) or {}
    confirmed = other_reviewer.post(f"/my/reviews/{review_id}/confirm")
    fixtures.denied(confirmed,
                    f"POST /api/my/reviews/{review_id}/confirm as another reviewer")
    withdrawn = other_reviewer.post(f"/my/reviews/{review_id}/withdraw")
    fixtures.denied(withdrawn,
                    f"POST /api/my/reviews/{review_id}/withdraw as another reviewer")
    after = db.one("reviews", public_id=review_id) or {}
    assert after.get("state") == before.get("state"), (
        f"the review {review_id} moved from {before.get('state')!r} to "
        f"{after.get('state')!r} under a denied request")
    own = fixtures.my_reviews(other_reviewer)
    assert all(str(row.get("id")) != str(review_id) for row in own), (
        f"another writer review {review_id} appears in a reviewer own list")


def test_draft_project_record_is_not_found_for_the_public(anon):
    """The seeded draft answers exactly as a key that does not exist."""
    record = httpx.get(f"{appclient.api_base()}/projects/{fixtures.DRAFT_KEY}",
                       timeout=appclient.TIMEOUT)
    fixtures.not_found(record, f"GET /api/projects/{fixtures.DRAFT_KEY} signed out")
    unknown = "no-such-key"
    missing = httpx.get(f"{appclient.api_base()}/projects/{unknown}",
                        timeout=appclient.TIMEOUT)
    fixtures.not_found(missing, f"GET /api/projects/{unknown}")
    assert record.text == missing.text, (
        f"the draft answered {record.text[:120]!r} and an unknown key answered "
        f"{missing.text[:120]!r}, and both must be identical")
    route = fixtures.page_response(f"/case-study/{fixtures.DRAFT_KEY}")
    assert route.status_code == fixtures.NOT_FOUND_STATUS, (
        f"/case-study/{fixtures.DRAFT_KEY} answered {route.status_code} to a "
        f"signed out reader")
    listed = anon.get("/admin/projects")
    fixtures.denied(listed, "GET /api/admin/projects signed out")


def test_draft_media_object_is_not_found_for_the_public(owner):
    """An image attached to a draft is unreadable until the work is published."""
    payload = fixtures.png_bytes(tone=43)
    response = fixtures.upload_media(owner, fixtures.DRAFT_KEY, payload)
    assert response.status_code < 300, (
        f"POST /api/projects/{fixtures.DRAFT_KEY}/media answered "
        f"{response.status_code}: {response.text[:300]}")
    object_key = response.json().get("objectKey")
    served = httpx.get(f"{appclient.api_base()}/media/{object_key}",
                       timeout=appclient.TIMEOUT)
    fixtures.not_found(served, f"GET /api/media/{object_key} signed out")
    with appclient.client(appclient.login(fixtures.OWNER_EMAIL,
                                          fixtures.PASSWORD)) as api:
        allowed = api.get(f"/media/{object_key}")
    assert allowed.status_code == 200, (
        f"GET /api/media/{object_key} answered {allowed.status_code} to the owner, "
        f"who may always read the draft media")


def test_unconfirmed_reviews_are_absent_from_the_public_wall(owner):
    """Only published reviews reach the wall, whatever the console holds."""
    wall = fixtures.published_reviews()
    published_ids = {str(row.get("id")) for row in wall}
    for state in ("awaiting_confirmation", "confirmed"):
        held = fixtures.admin_review(owner, state)
        assert str(held.get("id")) not in published_ids, (
            f"the review {held.get('id')} in state {state!r} appears on "
            f"GET /api/reviews")
    markup = fixtures.page_body("/peer-reviews")
    for state in ("awaiting_confirmation", "confirmed"):
        held = fixtures.admin_review(owner, state)
        excerpt = (held.get("body") or "")[:40]
        assert excerpt and excerpt not in markup, (
            f"/peer-reviews carries the text of a {state!r} review: {excerpt!r}")


def test_public_review_payload_carries_no_reviewer_email(owner):
    """The wall returns the attribution and never a private field."""
    wall = fixtures.published_reviews()
    assert wall, "GET /api/reviews returned no published review"
    for row in wall:
        for field in fixtures.PUBLIC_REVIEW_KEYS:
            assert field in row, (
                f"a published review is missing {field!r}: {sorted(row)}")
        for field in fixtures.PRIVATE_REVIEW_KEYS:
            assert field not in row, (
                f"a published review carries the private field {field!r}: "
                f"{sorted(row)}")
        assert "@" not in fixtures.flat(row), (
            f"a published review payload carries an address: {fixtures.flat(row)[:200]}")
    markup = fixtures.page_body("/peer-reviews")
    assert fixtures.REVIEWER_EMAIL not in markup, (
        f"/peer-reviews carries the reviewer address {fixtures.REVIEWER_EMAIL}")


def test_signup_ignores_a_role_sent_in_the_body():
    """Every account created through signup is a reviewer."""
    email = fixtures.fresh_email("claimant")
    response = httpx.post(f"{appclient.api_base()}/auth/signup",
                          json={"email": email, "password": fixtures.PASSWORD,
                                "name": "Ada Claimant", "role": "owner"},
                          timeout=appclient.TIMEOUT)
    assert response.status_code < 300, (
        f"POST /api/auth/signup answered {response.status_code}: "
        f"{response.text[:300]}")
    payload = response.json()
    assert payload.get(fixtures.AUTH_TOKEN_FIELD), (
        f"the signup returned no {fixtures.AUTH_TOKEN_FIELD}: {payload}")
    assert payload.get("user", {}).get("role") == fixtures.SIGNUP_ROLE, (
        f"the signup granted the role {payload.get('user', {}).get('role')!r} "
        f"rather than {fixtures.SIGNUP_ROLE!r}")
    with appclient.client(payload[fixtures.AUTH_TOKEN_FIELD]) as api:
        denied = api.get("/admin/messages")
    fixtures.denied(denied, "GET /api/admin/messages as a new signup")
    repeat = httpx.post(f"{appclient.api_base()}/auth/signup",
                        json={"email": email.upper(),
                              "password": fixtures.PASSWORD, "name": "Ada Again"},
                        timeout=appclient.TIMEOUT)
    code = fixtures.refusal_code(repeat, "a repeated signup")
    assert fixtures.EMAIL_TAKEN in code, (
        f"a repeated signup answered the code {code!r} rather than "
        f"{fixtures.EMAIL_TAKEN!r}")


def test_owner_cannot_publish_a_review_before_its_writer_confirms(owner, db):
    """Publication is refused for every state except confirmed."""
    waiting = fixtures.admin_review(owner, "awaiting_confirmation")
    review_id = waiting.get("id")
    before = db.one("reviews", public_id=review_id) or {}
    response = owner.post(f"/admin/reviews/{review_id}/publish")
    assert response.status_code >= 400, (
        f"POST /api/admin/reviews/{review_id}/publish answered "
        f"{response.status_code} for a review its writer has not confirmed: "
        f"{response.text[:200]}")
    after = db.one("reviews", public_id=review_id) or {}
    assert after.get("state") == before.get("state"), (
        f"the review {review_id} moved from {before.get('state')!r} to "
        f"{after.get('state')!r} under a refused publication")
    wall = {str(row.get("id")) for row in fixtures.published_reviews()}
    assert str(review_id) not in wall, (
        f"the unconfirmed review {review_id} reached the public wall")


def test_owner_cannot_confirm_a_review_on_a_writer_behalf(owner, db):
    """The owner never confirms or withdraws a review it did not write."""
    waiting = fixtures.admin_review(owner, "awaiting_confirmation")
    review_id = waiting.get("id")
    before = db.one("reviews", public_id=review_id) or {}
    confirmed = owner.post(f"/my/reviews/{review_id}/confirm")
    assert confirmed.status_code >= 400, (
        f"POST /api/my/reviews/{review_id}/confirm answered "
        f"{confirmed.status_code} for the owner: {confirmed.text[:200]}")
    withdrawn = owner.post(f"/my/reviews/{review_id}/withdraw")
    assert withdrawn.status_code >= 400, (
        f"POST /api/my/reviews/{review_id}/withdraw answered "
        f"{withdrawn.status_code} for the owner: {withdrawn.text[:200]}")
    after = db.one("reviews", public_id=review_id) or {}
    assert after.get("state") == before.get("state"), (
        f"the review {review_id} moved from {before.get('state')!r} to "
        f"{after.get('state')!r} under a refused owner action")


def test_preview_token_opens_the_draft_for_one_reader(owner):
    """A preview link renders the draft through the real case study template."""
    response = owner.post(f"/projects/{fixtures.DRAFT_KEY}/preview")
    assert response.status_code < 300, (
        f"POST /api/projects/{fixtures.DRAFT_KEY}/preview answered "
        f"{response.status_code}: {response.text[:300]}")
    record = response.json()
    preview_url = record.get("previewUrl") or ""
    assert preview_url.startswith(f"/case-study/{fixtures.DRAFT_KEY}?preview="), (
        f"the preview link reads {preview_url!r}, and the contract pins "
        f"/case-study/{fixtures.DRAFT_KEY}?preview=<token>")
    assert record.get("expiresAt"), f"the preview carries no expiry: {record}"
    opened = fixtures.page_response(preview_url)
    assert opened.status_code == 200, (
        f"the preview link answered {opened.status_code} to its holder: "
        f"{opened.text[:200]}")
    forged = fixtures.page_response(
        f"/case-study/{fixtures.DRAFT_KEY}?preview=not-a-real-token")
    assert forged.status_code == fixtures.NOT_FOUND_STATUS, (
        f"a forged preview token answered {forged.status_code} rather than "
        f"{fixtures.NOT_FOUND_STATUS}")


def test_unsupported_media_upload_is_refused_and_stores_no_object(owner, store):
    """A file that is not PNG, JPEG or WebP is refused and never stored."""
    payload = b"GIF89a this is not one of the three formats"
    before = set(store.list(f"{fixtures.MEDIA_KEY_PREFIX}tide/"))
    response = fixtures.upload_media(owner, "tide", payload, name="frame.gif",
                                     content_type="image/gif")
    code = fixtures.refusal_code(response, "an unsupported media upload")
    assert fixtures.UNSUPPORTED_MEDIA in code, (
        f"an unsupported upload answered the code {code!r} rather than "
        f"{fixtures.UNSUPPORTED_MEDIA!r}")
    after = set(store.list(f"{fixtures.MEDIA_KEY_PREFIX}tide/"))
    assert after == before, (
        f"the refused upload added {sorted(after - before)} to the bucket, and a "
        f"rejection stores nothing")


def test_oversize_media_upload_is_refused_and_stores_no_object(owner, store):
    """A file over the pinned byte ceiling is refused and never stored."""
    payload = b"\x89PNG\r\n\x1a\n" + b"0" * (fixtures.UPLOAD_LIMIT_BYTES + 1)
    before = set(store.list(f"{fixtures.MEDIA_KEY_PREFIX}tide/"))
    response = fixtures.upload_media(owner, "tide", payload, name="huge.png")
    code = fixtures.refusal_code(response, "an oversize media upload")
    assert fixtures.MEDIA_TOO_LARGE in code, (
        f"an upload of {len(payload)} bytes answered the code {code!r} rather "
        f"than {fixtures.MEDIA_TOO_LARGE!r}, and the ceiling is "
        f"{fixtures.UPLOAD_LIMIT_BYTES}")
    after = set(store.list(f"{fixtures.MEDIA_KEY_PREFIX}tide/"))
    assert after == before, (
        f"the refused upload added {sorted(after - before)} to the bucket")


def test_contact_form_refuses_a_missing_field_and_a_malformed_email(db):
    """Each contact rejection carries its own code and stores nothing."""
    blank = fixtures.send_contact(name="")
    code = fixtures.refusal_code(blank, "a contact submission with no name")
    assert "missing_field" in code, (
        f"a blank name answered the code {code!r} rather than 'missing_field'")
    malformed_address = "not-an-address"
    malformed = fixtures.send_contact(email=malformed_address)
    code = fixtures.refusal_code(malformed, "a contact submission with a bad email")
    assert "invalid_email" in code, (
        f"a malformed email answered the code {code!r} rather than 'invalid_email'")
    assert db.count("contact_messages", email=malformed_address) == 0, (
        f"the rejected submission from {malformed_address} was stored")
    long_sender = fixtures.fresh_email("verbose")
    overlong = fixtures.send_contact(
        email=long_sender, message="w" * (fixtures.CONTACT_MESSAGE_LIMIT + 1))
    code = fixtures.refusal_code(overlong, "an overlong contact message")
    assert "too_long" in code, (
        f"a message over {fixtures.CONTACT_MESSAGE_LIMIT} characters answered the "
        f"code {code!r} rather than 'too_long'")
    assert db.count("contact_messages", email=long_sender) == 0, (
        f"the overlong submission from {long_sender} was stored")


def test_expired_invitation_is_refused_like_an_unknown_one(reviewer):
    """An expired token and an unknown token answer identically."""
    expired = reviewer.get(f"/review/{fixtures.EXPIRED_INVITATION}")
    unknown = reviewer.get("/review/Zz0000000000000000000A")
    fixtures.not_found(expired, "GET /api/review with the expired seeded token")
    fixtures.not_found(unknown, "GET /api/review with an unknown token")
    assert expired.text == unknown.text, (
        f"the expired token answered {expired.text[:120]!r} and an unknown token "
        f"answered {unknown.text[:120]!r}, and both must be identical")
    submitted = fixtures.submit_review(fixtures.EXPIRED_INVITATION, reviewer,
                                       scope="ascent")
    assert submitted.status_code >= 400, (
        f"POST /api/review with the expired token answered "
        f"{submitted.status_code}: {submitted.text[:200]}")


def test_invitation_carries_at_most_one_live_review(owner, other_reviewer, db):
    """A second submission through one invitation leaves one live review."""
    invitation = fixtures.issue_invitation(owner, fixtures.REVIEWER2_EMAIL, "tide")
    token = invitation["token"]
    assert len(token) == fixtures.INVITATION_TOKEN_LENGTH, (
        f"the invitation token {token!r} is {len(token)} characters rather than "
        f"{fixtures.INVITATION_TOKEN_LENGTH}")
    first = fixtures.submit_review(token, other_reviewer, scope="tide")
    assert first.status_code < 300, (
        f"the first submission answered {first.status_code}: {first.text[:300]}")
    assert first.json().get("state") == "awaiting_confirmation", (
        f"a new submission entered the state {first.json().get('state')!r} rather "
        f"than 'awaiting_confirmation'")
    replacement = fixtures.submit_review(token, other_reviewer, scope="tide",
                                         body=fixtures.review_body(90))
    assert replacement.status_code < 300, (
        f"a replacement while awaiting confirmation answered "
        f"{replacement.status_code}: {replacement.text[:300]}")
    rows = db.rows("reviews", invitation_id=invitation.get("id")) or []
    live = [row for row in rows if row.get("state") != "withdrawn"]
    assert len(live) <= 1, (
        f"the invitation carries {len(live)} reviews that are not withdrawn: "
        f"{[row.get('state') for row in rows]}")


def test_review_submission_refuses_each_invalid_field(owner, other_reviewer, db):
    """Every review field violation carries its own code and stores nothing."""
    invitation = fixtures.issue_invitation(owner, fixtures.REVIEWER2_EMAIL, "ascent")
    token = invitation["token"]
    cases = (({"reviewerName": ""}, "missing_name"),
             ({"reviewerRole": ""}, "missing_role"),
             ({"relationship": "rival"}, "invalid_relationship"),
             ({"scope": ""}, "missing_scope"),
             ({"body": fixtures.review_body(10)}, "body_too_short"),
             ({"body": fixtures.review_body(240)}, "body_too_long"))
    for fields, expected in cases:
        response = fixtures.submit_review(token, other_reviewer, scope="ascent",
                                          **fields)
        code = fixtures.refusal_code(response, f"a submission with {fields}")
        assert expected in code, (
            f"a submission with {fields} answered the code {code!r} rather than "
            f"{expected!r}")
    rows = db.rows("reviews", invitation_id=invitation.get("id")) or []
    assert not rows, (
        f"a refused submission stored {len(rows)} review rows against the "
        f"invitation")


def test_composer_refuses_a_case_study_with_no_failure_statement(owner, db):
    """A case study body without a failure statement is refused and stored nowhere."""
    key = fixtures.fresh_token("story").replace("_", "-")
    record = {"menuLabel": "Story", "lines": ["A STORY WITH NO", "FAILURE IN IT"],
              "category": "CREATIVE CODING", "note": "Tell it straight",
              "opens": "caseStudy",
              "labels": {"what": "STORY", "tools": "CODE", "method": "WRITING"},
              "body": [{"type": "standfirst", "lead": "A short lead for a story "
                        "that never admits anything went wrong along the way.",
                        "body": []},
                       {"type": "statement", "kind": "claim",
                        "heading": "It all went well", "body": []},
                       {"type": "statement", "kind": "close",
                        "heading": "It closed well", "body": []}]}
    response = owner.put(f"/projects/{key}", json=record)
    assert response.status_code < 300, (
        f"PUT /api/projects/{key} answered {response.status_code}, and the "
        f"composer reports findings rather than refusing the call: "
        f"{response.text[:300]}")
    payload = response.json()
    assert payload.get("valid") is False, (
        f"the composer called a case study with no failure statement valid: "
        f"{payload}")
    rules = {finding.get("rule") for finding in payload.get("findings") or []}
    assert "failure_required" in rules, (
        f"the composer reported the rules {sorted(rules)} and named no "
        f"'failure_required'")
    assert "forward_required" in rules, (
        f"the composer reported the rules {sorted(rules)} and named no "
        f"'forward_required'")
    assert db.one("projects", key=key) is None, (
        f"the refused record {key!r} was stored as a projects row")


def test_composer_finding_carries_every_declared_field(owner):
    """Each composer finding carries its rule, severity, block index and message."""
    key = fixtures.fresh_token("shape").replace("_", "-")
    record = {"menuLabel": "A menu label that runs far past twelve characters",
              "lines": ["ONLY ONE LINE"], "category": "NOT A CATEGORY",
              "note": "too short", "opens": "caseStudy",
              "labels": {"what": "SHAPE", "tools": "CODE", "method": "SHAPE"},
              "body": [{"type": "unknownBlock"}]}
    response = owner.put(f"/projects/{key}", json=record)
    assert response.status_code < 300, (
        f"PUT /api/projects/{key} answered {response.status_code}: "
        f"{response.text[:300]}")
    payload = response.json()
    findings = payload.get("findings") or []
    assert findings, f"the composer reported no finding for a broken record: {payload}"
    for finding in findings:
        assert set(finding) == set(fixtures.FINDING_KEYS), (
            f"a finding carries {sorted(finding)} rather than "
            f"{sorted(fixtures.FINDING_KEYS)}")
        assert finding["severity"] in fixtures.SEVERITIES, (
            f"a finding carries the severity {finding['severity']!r}, outside "
            f"{list(fixtures.SEVERITIES)}")
        assert finding["rule"] in (fixtures.COMPOSER_ERROR_RULES
                                   + fixtures.COMPOSER_WARNING_RULES), (
            f"a finding names the rule {finding['rule']!r}, outside the "
            f"identifiers the brief pins")
    rules = {finding.get("rule") for finding in findings}
    for expected in ("block_type", "lines_shape", "menu_label_length", "category"):
        assert expected in rules, (
            f"the composer reported {sorted(rules)} and named no {expected!r}")


def test_duplicate_device_registration_is_refused(owner):
    """A device identifier is claimed once and a rotation retires the old key."""
    run = fixtures.open_run(owner)
    device = fixtures.provision_device(owner, run.get("runId"))
    repeat = owner.post("/admin/devices", json={"deviceId": device["deviceId"],
                                                "runId": run.get("runId")})
    code = fixtures.refusal_code(repeat, "a repeated device registration")
    assert fixtures.DUPLICATE_DEVICE in code, (
        f"a repeated device answered the code {code!r} rather than "
        f"{fixtures.DUPLICATE_DEVICE!r}")
    rotated = owner.post(f"/admin/devices/{device['deviceId']}/rotate")
    assert rotated.status_code < 300, (
        f"rotating the device key answered {rotated.status_code}: "
        f"{rotated.text[:300]}")
    fresh_key = rotated.json().get("deviceKey")
    assert fresh_key and fresh_key != device["deviceKey"], (
        f"the rotation returned the key {fresh_key!r}, which must differ from the "
        f"retired one")
    stale = fixtures.ingest(device["deviceKey"], device["deviceId"],
                            fixtures.fresh_token("boot"),
                            fixtures.presence_events(20))
    fixtures.denied(stale, "POST /api/ingest with a rotated device key")


def test_ingest_without_a_device_key_is_denied(owner, db):
    """An unauthenticated or mis-keyed batch is denied and stores nothing."""
    run = fixtures.open_run(owner)
    device = fixtures.provision_device(owner, run.get("runId"))
    boot = fixtures.fresh_token("boot")
    events = fixtures.presence_events(25)
    anonymous = httpx.post(f"{appclient.api_base()}/ingest",
                           json={"deviceId": device["deviceId"], "bootId": boot,
                                 "events": events}, timeout=appclient.TIMEOUT)
    fixtures.denied(anonymous, "POST /api/ingest with no device key")
    wrong = fixtures.ingest("not-a-real-device-key", device["deviceId"], boot,
                            events)
    code = fixtures.refusal_code(wrong, "POST /api/ingest with a wrong device key")
    assert fixtures.DEVICE_UNAUTHORIZED in code, (
        f"a wrong device key answered the code {code!r} rather than "
        f"{fixtures.DEVICE_UNAUTHORIZED!r}")
    assert db.count("telemetry_events", device_id=device["deviceId"],
                    boot_id=boot) == 0, (
        f"a denied batch stored telemetry_events rows for {device['deviceId']}")


def test_ingest_refuses_an_unknown_kind_and_an_oversize_batch(owner, db):
    """An unknown event kind and an over-long batch are both refused."""
    run = fixtures.open_run(owner)
    device = fixtures.provision_device(owner, run.get("runId"))
    boot = fixtures.fresh_token("boot")
    unknown = fixtures.ingest(device["deviceKey"], device["deviceId"], boot,
                              [{"seq": 1, "uptimeMs": 500, "kind": "teleport",
                                "payload": {}}])
    code = fixtures.refusal_code(unknown, "an unknown telemetry kind")
    assert fixtures.INVALID_EVENT in code, (
        f"an unknown kind answered the code {code!r} rather than "
        f"{fixtures.INVALID_EVENT!r}")
    oversize = [{"seq": index, "uptimeMs": index * 10, "kind": "heartbeat",
                 "payload": {}}
                for index in range(1, fixtures.INGEST_BATCH_LIMIT + 2)]
    too_many = fixtures.ingest(device["deviceKey"], device["deviceId"], boot,
                               oversize)
    code = fixtures.refusal_code(too_many, "an oversize telemetry batch")
    assert fixtures.BATCH_TOO_LARGE in code, (
        f"a batch of {len(oversize)} events answered the code {code!r} rather "
        f"than {fixtures.BATCH_TOO_LARGE!r}, and the ceiling is "
        f"{fixtures.INGEST_BATCH_LIMIT}")
    assert db.count("telemetry_events", device_id=device["deviceId"],
                    boot_id=boot) == 0, (
        f"a refused batch stored telemetry_events rows for {device['deviceId']}")


def test_untrusted_run_publication_is_refused_with_its_proportion(owner):
    """A run whose sensors cannot be trusted refuses to publish its figures."""
    run = fixtures.open_run(owner)
    run_id = run.get("runId")
    device = fixtures.provision_device(owner, run_id)
    boot = fixtures.fresh_token("boot")
    events = list(fixtures.presence_events(40))
    events.append(fixtures.health_event(3, 60000,
                                        longestHighMs=fixtures.STUCK_HIGH_MS + 1))
    events.append(fixtures.health_event(4, 120000,
                                        triggersInWindow=fixtures.CHATTER_TRIGGERS + 1))
    accepted = fixtures.ingest(device["deviceKey"], device["deviceId"], boot,
                               events)
    assert accepted.status_code < 300, (
        f"the telemetry batch answered {accepted.status_code}: "
        f"{accepted.text[:300]}")
    detail = owner.get(f"/admin/runs/{run_id}")
    assert detail.status_code == 200, (
        f"GET /api/admin/runs/{run_id} answered {detail.status_code}: "
        f"{detail.text[:300]}")
    health = detail.json().get("health") or {}
    assert health.get("status") in fixtures.HEALTH_STATUSES, (
        f"the run health reads {health.get('status')!r}, outside "
        f"{list(fixtures.HEALTH_STATUSES)}")
    assert health.get("trustedProportion") < fixtures.TRUST_FLOOR, (
        f"two untrusted windows left the trusted proportion at "
        f"{health.get('trustedProportion')}, at or above the floor of "
        f"{fixtures.TRUST_FLOOR}")
    refused = owner.post(f"/admin/runs/{run_id}/publish")
    code = fixtures.refusal_code(refused, f"publishing the untrusted run {run_id}")
    assert fixtures.UNTRUSTED_RUN in code, (
        f"publishing an untrusted run answered the code {code!r} rather than "
        f"{fixtures.UNTRUSTED_RUN!r}")
    public = httpx.get(f"{appclient.api_base()}/runs/{run_id}",
                       timeout=appclient.TIMEOUT)
    fixtures.not_found(public, f"GET /api/runs/{run_id} for an unpublished run")


def test_page_view_for_a_private_route_is_refused(db):
    """A console or sign-in route is never recorded as a page view."""
    for route in ("/console/messages", "/signin", "/review/some-token"):
        response = httpx.post(f"{appclient.api_base()}/page-views",
                              json={"route": route}, timeout=appclient.TIMEOUT)
        code = fixtures.refusal_code(response, f"a page view for {route}")
        assert "invalid_route" in code, (
            f"a page view for {route} answered the code {code!r} rather than "
            f"'invalid_route'")
        assert db.count("page_views", route=route) == 0, (
            f"a refused page view for {route} was stored as a row")


def test_unknown_address_answers_with_the_not_found_page():
    """An unknown address answers 404 with the portfolio own not-found page."""
    response = fixtures.page_response(f"/{fixtures.fresh_token('nowhere')}")
    assert response.status_code == fixtures.NOT_FOUND_STATUS, (
        f"an unknown address answered {response.status_code} rather than "
        f"{fixtures.NOT_FOUND_STATUS}")
    assert fixtures.NOT_FOUND_HEADING in response.text, (
        f"the not-found page carries no heading {fixtures.NOT_FOUND_HEADING!r}")
    assert fixtures.NOT_FOUND_LINK in response.text, (
        f"the not-found page offers no {fixtures.NOT_FOUND_LINK!r} link")


def test_sitemap_lists_every_public_route_and_no_private_one():
    """The sitemap carries the public routes under the configured origin."""
    response = fixtures.page_response("/sitemap.xml")
    assert response.status_code == 200, (
        f"GET /sitemap.xml answered {response.status_code}: {response.text[:200]}")
    body = response.text
    origin = fixtures.app_origin()
    for route in fixtures.PUBLIC_ROUTES:
        absolute = f"{origin}{route}" if route != "/" else f"{origin}/"
        assert absolute in body, (
            f"/sitemap.xml omits the public route {absolute}")
    for key in fixtures.CASE_STUDY_KEYS:
        assert f"{origin}/case-study/{key}" in body, (
            f"/sitemap.xml omits the published case study {key!r}")
    assert f"/case-study/{fixtures.DRAFT_KEY}" not in body, (
        f"/sitemap.xml lists the draft {fixtures.DRAFT_KEY!r}")
    for fragment in fixtures.PRIVATE_ROUTE_FRAGMENTS:
        assert fragment not in body, (
            f"/sitemap.xml lists a private route carrying {fragment!r}")
    robots = fixtures.page_response("/robots.txt")
    assert robots.status_code == 200, (
        f"GET /robots.txt answered {robots.status_code}")
    assert "Sitemap:" in robots.text and "/sitemap.xml" in robots.text, (
        f"/robots.txt names no sitemap: {robots.text[:200]}")


def test_public_markup_carries_no_credential_or_binary_asset():
    """No credential and no shipped binary asset reaches the browser."""
    for route in ("/", "/cv", "/flat", "/case-study"):
        markup = fixtures.page_body(route)
        for fragment in fixtures.SECRET_FRAGMENTS:
            assert fragment not in markup, (
                f"{route} sends the fragment {fragment!r} to the browser")
        for suffix in fixtures.BINARY_ASSET_SUFFIXES:
            assert f'src="/{suffix}' not in markup, (
                f"{route} references a shipped binary asset ending {suffix!r}")


def test_home_route_is_one_viewport_tall_and_never_scrolls(page):
    """The home route fits one viewport and the document never scrolls."""
    surface = fixtures.open_site(page, "/")
    overflow = surface.evaluate(
        "() => document.documentElement.scrollHeight "
        "- document.documentElement.clientHeight")
    assert overflow <= 1, (
        f"the home route document overflows its viewport by {overflow} pixels, "
        f"and the page itself never scrolls")
    title = surface.title()
    assert title.strip(), "the home route carries an empty document title"


def test_not_found_page_shows_its_heading_and_return_link(page):
    """The rendered not-found page carries its heading and its way back."""
    surface = fixtures.open_site(page, f"/{fixtures.fresh_token('missing')}")
    text = surface.inner_text("body")
    assert fixtures.NOT_FOUND_HEADING in text, (
        f"the rendered not-found page reads {text[:200]!r} and carries no "
        f"heading {fixtures.NOT_FOUND_HEADING!r}")
    assert fixtures.NOT_FOUND_LINK in text, (
        f"the rendered not-found page offers no {fixtures.NOT_FOUND_LINK!r} link")
    link = surface.get_by_role("link", name=fixtures.NOT_FOUND_LINK).first
    assert link.get_attribute("href") == "/", (
        f"the return link points at {link.get_attribute('href')!r} rather than "
        f"the home route")
