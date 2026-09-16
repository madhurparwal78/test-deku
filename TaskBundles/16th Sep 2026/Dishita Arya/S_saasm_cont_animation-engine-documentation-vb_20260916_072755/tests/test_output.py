"""Graders for Lumen.js.

Every assertion reads the running app, the persisted rows, the object store or a
rendered page. Nothing here reads the app's own claim about its own effect.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import httpx

from conftest import (
    ADDRESS_LIMIT_PER_HOUR,
    AD_ATTRIBUTION,
    AD_STATES,
    ANALYTICS_KINDS,
    BADGE_EXPIRES,
    BADGE_LABEL,
    BADGE_MODULES,
    BINARY_ASSET_SUFFIXES,
    CODE_ONLY_PAGE,
    CODE_ONLY_TERM,
    COMPLAINED_EMAIL,
    CONCURRENT_SUBMISSIONS,
    CONFIRMED_EMAIL,
    CONTRAST_BAR,
    COPY_CONFIRMATION,
    CORRELATION_FIELD,
    DEGRADATION_STATES,
    DEMO_COUNT,
    DEMO_KINDS,
    DENIAL_STATUSES,
    DOCS_ROUTE,
    DOCS_TITLE,
    DRAFT_BROKEN_LINK,
    EDITOR_ROUTE,
    EXPIRED_EMAIL,
    EXPORT_TABS,
    FALLBACK_LINE,
    FAMILIES,
    FAMILY_COUNT,
    FIRST_PAGE,
    FIRST_PAGE_OF_NEXT_MODULE,
    FUNDING_LABEL,
    HONEYPOT_FIELD,
    INSTALL_LINE,
    IN_SECTION_HEADING,
    JOBS,
    JOB_COUNT,
    LARGE_TEXT_CONTRAST_BAR,
    LAST_MODULE_PAGE,
    LAST_PAGE,
    LEARN_ROUTE,
    LIST_NEWSLETTER,
    LIST_WAITLIST,
    MAINTAINER_EMAIL,
    MAINTAINER_NAME,
    MAX_ATTEMPTS,
    MEMBER_COUNT,
    MISSING_IN_ARCHIVED,
    MODULES,
    MODULE_COUNT,
    NAV_LABELS,
    NOT_FOUND_BODY,
    NOT_FOUND_HEADING,
    NOT_FOUND_STATUSES,
    OBJECT_COUNT,
    OBJECT_NAMES,
    ORIGIN_LIMIT_PER_HOUR,
    PAGER_LABELS,
    PAGES,
    PAGE_COUNT,
    PAGE_WITHOUT_DEMO,
    PASSWORD,
    PENDING_EMAIL,
    POINT_KEYS,
    PREVIEW_KEY,
    PRIVACY_ROUTE,
    PUBLIC_ROUTES,
    RAMPS,
    RATE_LIMITED_STATUSES,
    RECRUITMENT_LABEL,
    REDIRECT_STATUSES,
    REFUSAL_STATUSES,
    ROSTER_FRESHNESS_HOURS,
    ROSTER_KEY,
    SCENE_DEMO_MODULE,
    SEARCH_PLACEHOLDER,
    SECONDARY_CALL,
    SKIP_LINK,
    SPONSORS,
    SPONSOR_LAPSED,
    SPONSOR_LAPSED_ENDED,
    SPONSOR_WITHOUT_MARK,
    STATE_BOUNCED,
    STATE_COMPLAINED,
    STATE_CONFIRMED,
    STATE_PENDING,
    STATE_UNSUBSCRIBED,
    STOPS,
    STOP_COUNT,
    STUDIO_ROUTE,
    STUDIO_ROUTES,
    SUBMIT_LABEL,
    SUBSCRIBER_STATES,
    SUCCESS_STATUSES,
    SURFACE_DOC_LANDING,
    SURFACE_DOC_PAGE,
    SURFACE_TOUR_OPENING,
    SURFACE_TOUR_TWELVE,
    SWEEP_SANITY_THRESHOLD,
    TIER_HEADINGS,
    TIER_LOWER,
    TIER_NAMES,
    TIER_PLACEMENTS,
    TIER_RANKS,
    TIER_UPPER,
    TILE_COUNT,
    TIMING_TOKEN_SECONDS,
    TOUR_HEADLINE,
    TOUR_ROUTE,
    UNSUBSCRIBED_EMAIL,
    VERSION_ARCHIVED,
    VERSION_DRAFT,
    VERSION_PUBLISHED,
    VERSION_STATES,
    WAITLIST_LABEL,
    contrast_ratio,
    describe,
    fetch,
    field_of,
    flat_positions,
    index_key,
    mark_key,
    page_route,
    parse_rgb,
    payload_of,
    poll_until,
    poster_key,
    probe_email,
    rows_of,
    settle,
    timing_token,
    unique_suffix,
)

import appclient


def test_health_route_and_reserved_directories_exist(app_base, store):
    response = httpx.get(f"{app_base}/health", timeout=30.0)
    assert response.status_code == 200, describe(response)

    missing = httpx.get(f"{app_base}/no-such-resource", timeout=30.0)
    assert missing.status_code in REFUSAL_STATUSES, describe(missing)
    assert missing.status_code < 500, (
        f"an invalid call answered {missing.status_code}; an invalid or "
        f"unauthorized call is a client error, never a 5xx")
    assert CORRELATION_FIELD in missing.json(), (
        f"an error body carries {CORRELATION_FIELD}: {describe(missing)}")

    assert store.count("version") > 0, (
        "the versions must live in PostgreSQL, not in the process")


def test_seeded_versions_carry_their_state_and_one_current_flag(store):
    for label, state in ((VERSION_ARCHIVED, "archived"),
                         (VERSION_PUBLISHED, "published"),
                         (VERSION_DRAFT, "draft")):
        row = store.version(label)
        assert row is not None, f"seeded version {label} is absent from the store"
        assert row["state"] == state, (
            f"version {label} state is {row['state']!r}, expected {state!r}")
        assert row["state"] in VERSION_STATES, (
            f"version {label} carries a state outside the enum")

    current = store.query("SELECT * FROM version WHERE is_current = true")
    assert len(current) == 1, (
        f"{len(current)} versions are current, expected exactly one")
    assert current[0]["label"] == VERSION_PUBLISHED, (
        f"the current version is {current[0]['label']!r}")

    draft = store.version(VERSION_DRAFT)
    assert str(draft["preview_key"]) == PREVIEW_KEY, (
        f"the draft preview key is {draft['preview_key']!r}")


def test_seeded_modules_carry_their_order_family_object_and_tile(store):
    published = store.version(VERSION_PUBLISHED)
    rows = store.modules_of(published["id"])
    assert len(rows) == MODULE_COUNT, (
        f"{len(rows)} modules are seeded, expected {MODULE_COUNT}")

    tiles = []
    for index, (slug, name, ramp, tile, object_name) in enumerate(MODULES, start=1):
        row = store.module(published["id"], slug)
        assert row is not None, f"module {slug} is absent from the published version"
        assert row["name"] == name, f"{slug} name is {row['name']!r}"
        assert int(row["position"]) == index, (
            f"{slug} position is {row['position']!r}, expected {index}")
        assert row["ramp"] == ramp, (
            f"{slug} ramp is {row['ramp']!r}, expected {ramp!r}")
        assert row["ramp"] in RAMPS, f"{slug} names a ramp outside the twenty-one"
        assert row["object"] == object_name, (
            f"{slug} object is {row['object']!r}, expected {object_name!r}")
        if tile is None:
            assert row["tile_position"] in (None, "", 0), (
                f"{slug} carries a tile position but the brief gives it none")
        else:
            assert int(row["tile_position"]) == tile, (
                f"{slug} tile position is {row['tile_position']!r}")
            tiles.append(int(row["tile_position"]))

    assert sorted(tiles) == list(range(1, TILE_COUNT + 1)), (
        f"the tile positions are {sorted(tiles)}, expected one to {TILE_COUNT}")
    assert len(set(OBJECT_NAMES)) == OBJECT_COUNT, (
        "fourteen named objects serve the sixteen modules")


def test_seeded_badges_name_two_modules_and_carry_an_expiry(store):
    published = store.version(VERSION_PUBLISHED)
    badged = [row for row in store.modules_of(published["id"])
              if str(row["badge"]).lower() == "new"]
    assert sorted(row["slug"] for row in badged) == sorted(BADGE_MODULES), (
        f"the badged modules are {[row['slug'] for row in badged]}")
    for row in badged:
        assert str(row["badge_expires_at"]).startswith(BADGE_EXPIRES), (
            f"{row['slug']} badge expiry is {row['badge_expires_at']!r}")


def test_seeded_pages_carry_a_gapless_flattened_sequence(store):
    published = store.version(VERSION_PUBLISHED)
    rows = store.pages_of(published["id"])
    assert len(rows) == PAGE_COUNT, (
        f"{len(rows)} pages are seeded, expected {PAGE_COUNT}")

    positions = [int(row["flat_position"]) for row in rows]
    assert positions == list(range(1, PAGE_COUNT + 1)), (
        f"the flattened sequence is {positions[:8]}..., expected one to {PAGE_COUNT} "
        f"with no gap and no duplicate")

    expected = flat_positions()
    for row, (module_slug, page_slug) in zip(rows, expected):
        module = store.query("SELECT * FROM module WHERE id = %s",
                             (row["module_id"],))[0]
        assert (module["slug"], row["slug"]) == (module_slug, page_slug), (
            f"flat position {row['flat_position']} is "
            f"{module['slug']}/{row['slug']}, expected {module_slug}/{page_slug}")


def test_seeded_demos_cover_every_page_but_the_last(store):
    published = store.version(VERSION_PUBLISHED)
    rows = store.pages_of(published["id"])
    with_demo = [row for row in rows if row["demo_id"]]
    assert len(with_demo) == DEMO_COUNT, (
        f"{len(with_demo)} pages carry a demo, expected {DEMO_COUNT}")

    without = [row for row in rows if not row["demo_id"]]
    assert len(without) == 1, f"{len(without)} pages carry no demo, expected one"
    assert without[0]["slug"] == PAGE_WITHOUT_DEMO[1], (
        f"the page with no demo is {without[0]['slug']!r}")

    scene_module = store.module(published["id"], SCENE_DEMO_MODULE)
    scene_pages = [row for row in rows if row["module_id"] == scene_module["id"]]
    for row in scene_pages:
        demo = store.demo(row["demo_id"])
        assert demo["kind"] == "scene", (
            f"{SCENE_DEMO_MODULE}/{row['slug']} carries a {demo['kind']!r} demo")
    for row in rows:
        if row["demo_id"] and row["module_id"] != scene_module["id"]:
            demo = store.demo(row["demo_id"])
            assert demo["kind"] in DEMO_KINDS, (
                f"demo kind {demo['kind']!r} sits outside the enum")
            assert str(demo["poster_seed"]).strip(), (
                f"demo {demo['id']} carries no poster seed")


def test_seed_is_idempotent_no_duplicate_rows(store):
    for table, columns in (("account", "email"), ("version", "label"),
                           ("sponsor", "external_id"),
                           ("sponsor_tier", "slug"),
                           ("module", "version_id, slug"),
                           ("page", "version_id, flat_position"),
                           ("subscriber", "lower(email), list")):
        rows = store.query(f"SELECT {columns}, count(*) AS n FROM {table} "
                           f"GROUP BY {columns} HAVING count(*) > 1")
        assert rows == [], f"{table} carries duplicate {columns} values: {rows}"

    signed_in = appclient.login(MAINTAINER_EMAIL, PASSWORD)
    assert signed_in, (
        f"the pinned password must work at login for {MAINTAINER_EMAIL}")
    account = store.account_by_email(MAINTAINER_EMAIL)
    assert account["display_name"] == MAINTAINER_NAME, (
        f"the maintainer display name is {account['display_name']!r}")


def test_seeded_subscribers_cover_every_lifecycle_state(store):
    expected = {
        (CONFIRMED_EMAIL, LIST_WAITLIST): STATE_CONFIRMED,
        (PENDING_EMAIL, LIST_WAITLIST): STATE_PENDING,
        (EXPIRED_EMAIL, LIST_NEWSLETTER): STATE_PENDING,
        (COMPLAINED_EMAIL, LIST_NEWSLETTER): STATE_COMPLAINED,
        (UNSUBSCRIBED_EMAIL, LIST_NEWSLETTER): STATE_UNSUBSCRIBED,
    }
    for (email, mailing_list), state in expected.items():
        row = store.subscriber(email, mailing_list)
        assert row is not None, f"seeded subscriber {email} on {mailing_list} is absent"
        assert row["state"] == state, (
            f"{email} sits in {row['state']!r}, expected {state!r}")
        assert row["state"] in SUBSCRIBER_STATES, (
            f"{email} carries a state outside the enum")
        assert row["source_route"], f"{email} records no source route"

    assert STATE_BOUNCED in SUBSCRIBER_STATES, (
        "the bounced state belongs to the enum the brief pins")


def test_seeded_sponsors_carry_their_tier_rank_and_placement(store):
    for slug in (TIER_UPPER, TIER_LOWER):
        tier = store.tier(slug)
        assert tier is not None, f"tier {slug} is absent from the store"
        assert tier["name"] == TIER_NAMES[slug], (
            f"tier {slug} name is {tier['name']!r}")
        assert int(tier["rank"]) == TIER_RANKS[slug], (
            f"tier {slug} rank is {tier['rank']!r}")
        placements = tier["placements"]
        if isinstance(placements, str):
            placements = [part.strip() for part in placements.strip("{}").split(",")]
        assert sorted(placements) == sorted(TIER_PLACEMENTS[slug]), (
            f"tier {slug} placements are {sorted(placements)}")

    for external_id, (name, tier_slug, position) in SPONSORS.items():
        row = store.sponsor(external_id)
        assert row is not None, f"sponsor {external_id} is absent from the store"
        assert row["name"] == name, f"{external_id} name is {row['name']!r}"
        assert int(row["position"]) == position, (
            f"{external_id} position is {row['position']!r}")
        tier = store.query("SELECT * FROM sponsor_tier WHERE id = %s",
                           (row["tier_id"],))[0]
        assert tier["slug"] == tier_slug, (
            f"{external_id} sits in tier {tier['slug']!r}")

    without_mark = store.sponsor(SPONSOR_WITHOUT_MARK)
    assert not without_mark["mark_object_key"], (
        f"{SPONSOR_WITHOUT_MARK} carries a mark the brief says it has none of")
    assert without_mark["name"] == SPONSORS[SPONSOR_WITHOUT_MARK][0]


def test_search_index_is_a_real_object_in_the_bucket_at_its_key(store, objects):
    published = store.version(VERSION_PUBLISHED)
    key = index_key(VERSION_PUBLISHED)
    assert str(published["index_object_key"]) == key, (
        f"the published version names {published['index_object_key']!r}, "
        f"expected {key!r}")
    assert objects.exists(key), (
        f"no object lives at {key}: the index is an artifact in the object "
        f"store, never a query and never a file on the app's own disk")

    archived = store.version(VERSION_ARCHIVED)
    assert objects.exists(index_key(VERSION_ARCHIVED)), (
        f"the archived version carries no index object at "
        f"{index_key(VERSION_ARCHIVED)}")
    assert str(archived["index_object_key"]) == index_key(VERSION_ARCHIVED)

    keys = set(objects.list("index/"))
    assert keys == {index_key(VERSION_PUBLISHED), index_key(VERSION_ARCHIVED)}, (
        f"the bucket holds index objects {sorted(keys)}, expected one per "
        f"published version and none for the draft")


def test_demo_posters_live_in_the_object_store_under_the_poster_scheme(store, objects):
    published = store.version(VERSION_PUBLISHED)
    rows = [row for row in store.pages_of(published["id"]) if row["demo_id"]]
    assert rows, "no seeded page carries a demo"

    checked = 0
    for row in rows[:6]:
        module = store.query("SELECT * FROM module WHERE id = %s",
                             (row["module_id"],))[0]
        demo = store.demo(row["demo_id"])
        key = poster_key(VERSION_PUBLISHED, module["slug"], row["slug"])
        assert str(demo["poster_object_key"]) == key, (
            f"{module['slug']}/{row['slug']} names poster key "
            f"{demo['poster_object_key']!r}, expected {key!r}")
        assert objects.exists(key), f"no poster object lives at {key}"
        checked += 1
    assert checked == 6, "six seeded posters were checked"


def test_sponsor_marks_and_the_roster_document_are_first_party_objects(store, objects):
    assert objects.exists(ROSTER_KEY), (
        f"the roster document must live at {ROSTER_KEY} in the object store")

    for external_id in SPONSORS:
        row = store.sponsor(external_id)
        if external_id == SPONSOR_WITHOUT_MARK:
            continue
        key = mark_key(external_id)
        assert str(row["mark_object_key"]) == key, (
            f"{external_id} names mark key {row['mark_object_key']!r}, "
            f"expected {key!r}")
        assert objects.exists(key), f"no mark object lives at {key}"


def test_search_index_is_served_from_the_object_store_rather_than_rebuilt(
        anonymous, objects):
    response = anonymous.search_index(VERSION_PUBLISHED)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    served = response.content
    assert served, f"the served index is empty: {describe(response)}"

    again = anonymous.search_index(VERSION_PUBLISHED)
    assert again.content == served, (
        "two fetches of one immutable index artifact returned different bytes")

    assert not objects.exists(index_key(VERSION_DRAFT)), (
        f"an index object exists for the draft at {index_key(VERSION_DRAFT)}")
    draft = anonymous.search_index(VERSION_DRAFT)
    assert draft.status_code in REFUSAL_STATUSES, (
        f"the draft version answered a search-index request with "
        f"{draft.status_code}. Its pages are in the database, so answering "
        f"proves the index is being built from the database rather than served "
        f"from the object store: {describe(draft)}")


def test_search_index_carries_an_entry_per_page_and_per_subheading(
        anonymous, store):
    response = anonymous.search_index(VERSION_PUBLISHED)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    document = response.json()
    entries = document if isinstance(document, list) else document.get("entries")
    assert isinstance(entries, list), (
        f"the index carries no entry list: {describe(response)}")

    pages = {(entry.get("module"), entry.get("page")) for entry in entries}
    for module_slug, page_slug in flat_positions():
        assert (module_slug, page_slug) in pages, (
            f"{module_slug}/{page_slug} is absent from the published index")

    for entry in entries[:20]:
        for field in ("module", "page", "anchor", "text"):
            assert field in entry, (
                f"an index entry is missing {field!r}: {sorted(entry)[:8]}")

    published = store.version(VERSION_PUBLISHED)
    anchors = 0
    for row in store.pages_of(published["id"])[:5]:
        anchors += len(store.anchors_of(row["id"]))
    assert anchors > 0, "no seeded page carries a subheading anchor"


def test_search_finds_a_call_name_that_appears_only_in_a_specimen(
        anonymous, store):
    response = anonymous.search_index(VERSION_PUBLISHED)
    entries = response.json()
    entries = entries if isinstance(entries, list) else entries.get("entries")
    hits = [entry for entry in entries
            if CODE_ONLY_TERM in str(entry.get("text", "")).lower()]
    assert hits, (
        f"{CODE_ONLY_TERM!r} is absent from the index, so code specimens were "
        f"not indexed")
    assert any(entry.get("module") == CODE_ONLY_PAGE[0]
               and entry.get("page") == CODE_ONLY_PAGE[1] for entry in hits), (
        f"{CODE_ONLY_TERM!r} does not resolve to "
        f"{CODE_ONLY_PAGE[0]}/{CODE_ONLY_PAGE[1]}")

    published = store.version(VERSION_PUBLISHED)
    module = store.module(published["id"], CODE_ONLY_PAGE[0])
    row = store.page(published["id"], module["id"], CODE_ONLY_PAGE[1])
    assert CODE_ONLY_TERM in str(row["body"]), (
        f"the seeded body for {CODE_ONLY_PAGE[1]} does not carry "
        f"{CODE_ONLY_TERM!r}")
    for other in store.pages_of(published["id"]):
        if other["id"] == row["id"]:
            continue
        assert CODE_ONLY_TERM not in str(other["title"]).lower(), (
            f"{CODE_ONLY_TERM!r} also appears in the title of {other['slug']}")


def test_search_index_is_rebuilt_when_a_version_is_published(
        maintainer, anonymous, store, objects):
    assert objects.exists(index_key(VERSION_PUBLISHED)), (
        "there was no index object to rebuild")
    response = maintainer.run_job("rebuild_index")
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    settle()
    assert objects.exists(index_key(VERSION_PUBLISHED)), (
        "the rebuild left no index object behind")

    runs = store.job_runs("rebuild_index")
    assert runs, "the index rebuild left no job run behind"
    assert runs[-1]["state"] in ("succeeded", "running"), (
        f"the rebuild run ended {runs[-1]['state']!r}")


def test_documentation_tree_lists_sixteen_modules_in_tree_order(anonymous):
    response = anonymous.tree(VERSION_PUBLISHED)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = response.json()
    modules = body if isinstance(body, list) else body.get("modules")
    assert isinstance(modules, list), f"the tree carries no module list: {body!r}"
    assert len(modules) == MODULE_COUNT, (
        f"the tree lists {len(modules)} modules, expected {MODULE_COUNT}")

    served = [entry.get("slug") for entry in modules]
    expected = [slug for slug, _n, _r, _t, _o in MODULES]
    assert served == expected, (
        f"the tree order is {served[:6]}..., expected {expected[:6]}...")

    for entry in modules:
        pages = entry.get("pages") or []
        assert [page.get("slug") for page in pages] == list(PAGES[entry["slug"]]), (
            f"{entry['slug']} lists {[p.get('slug') for p in pages]}")


def test_pager_walks_the_whole_flattened_tree_across_module_boundaries(anonymous):
    module_slug, page_slug = LAST_MODULE_PAGE
    response = anonymous.page_of(VERSION_PUBLISHED, module_slug, page_slug)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = payload_of(response)

    nxt = field_of(body, "next", "next_page")
    assert nxt, f"{module_slug}/{page_slug} carries no next page"
    assert (nxt.get("module"), nxt.get("page") or nxt.get("slug")) == \
        FIRST_PAGE_OF_NEXT_MODULE, (
        f"the page after {module_slug}/{page_slug} is {nxt}, expected "
        f"{FIRST_PAGE_OF_NEXT_MODULE}")

    walked = []
    cursor = FIRST_PAGE
    while cursor and len(walked) <= PAGE_COUNT:
        walked.append(cursor)
        step = payload_of(anonymous.page_of(VERSION_PUBLISHED, cursor[0], cursor[1]))
        following = step.get("next") or step.get("next_page")
        if not following:
            break
        cursor = (following.get("module"),
                  following.get("page") or following.get("slug"))
    assert walked == flat_positions(), (
        f"walking the pager visited {len(walked)} pages, expected {PAGE_COUNT} "
        f"in flattened order")


def test_first_page_has_no_previous_and_the_last_page_has_no_next(anonymous):
    first = payload_of(anonymous.page_of(VERSION_PUBLISHED, *FIRST_PAGE))
    assert not (first.get("previous") or first.get("previous_page")), (
        f"{FIRST_PAGE} carries a previous page: {first.get('previous')}")

    last = payload_of(anonymous.page_of(VERSION_PUBLISHED, *LAST_PAGE))
    assert not (last.get("next") or last.get("next_page")), (
        f"{LAST_PAGE} carries a next page: {last.get('next')}")


def test_in_section_list_is_generated_from_the_content_store(anonymous):
    for module_slug in ("timer", "svg", "adapters"):
        body = payload_of(anonymous.page_of(VERSION_PUBLISHED, module_slug,
                                            PAGES[module_slug][0]))
        siblings = field_of(body, "in_section", "siblings")
        names = [entry.get("slug") or entry.get("page") for entry in siblings]
        assert names == list(PAGES[module_slug]), (
            f"{module_slug} lists siblings {names}, expected {list(PAGES[module_slug])}")


def test_page_anchors_are_unique_and_a_missing_anchor_lands_at_the_top(
        anonymous, store, site_base):
    published = store.version(VERSION_PUBLISHED)
    for row in store.pages_of(published["id"])[:10]:
        anchors = [entry["anchor"] for entry in store.anchors_of(row["id"])]
        assert len(anchors) == len(set(anchors)), (
            f"page {row['slug']} carries duplicate anchors: {anchors}")

    module_slug, page_slug = FIRST_PAGE
    response = fetch(site_base,
                     f"{page_route(module_slug, page_slug)}#no-such-anchor")
    assert response.status_code in SUCCESS_STATUSES, describe(response)


def test_documentation_landing_renders_the_sponsor_wall(site_base, anonymous):
    response = fetch(site_base, DOCS_ROUTE)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    content = response.text
    assert DOCS_TITLE in content, "the documentation landing title is absent"
    assert RECRUITMENT_LABEL in content, "the recruitment card is absent"
    for external_id, (name, tier_slug, _position) in SPONSORS.items():
        if external_id == SPONSOR_LAPSED:
            continue
        assert name in content, f"sponsor {name} is absent from the landing wall"

    served = payload_of(anonymous.sponsors(SURFACE_DOC_LANDING))
    tiers = field_of(served, "tiers")
    assert [tier.get("slug") for tier in tiers] == [TIER_UPPER, TIER_LOWER], (
        f"the landing wall orders tiers {[t.get('slug') for t in tiers]}")


def test_sponsor_placement_follows_the_tier_placement_set(anonymous):
    for surface, expected in (
            (SURFACE_DOC_LANDING, {TIER_UPPER, TIER_LOWER}),
            (SURFACE_DOC_PAGE, {TIER_UPPER}),
            (SURFACE_TOUR_TWELVE, {TIER_UPPER, TIER_LOWER}),
            (SURFACE_TOUR_OPENING, {TIER_UPPER})):
        body = payload_of(anonymous.sponsors(surface))
        tiers = {tier.get("slug") for tier in field_of(body, "tiers")}
        assert tiers == expected, (
            f"{surface} carries tiers {sorted(tiers)}, expected {sorted(expected)}")


def test_lapsed_sponsor_is_marked_inactive_rather_than_deleted(store, anonymous):
    row = store.sponsor(SPONSOR_LAPSED)
    assert row is not None, (
        f"{SPONSOR_LAPSED} was deleted; a lapsed sponsor is marked inactive")
    assert str(row["active_to"]).startswith(SPONSOR_LAPSED_ENDED), (
        f"{SPONSOR_LAPSED} active_to is {row['active_to']!r}")

    body = payload_of(anonymous.sponsors(SURFACE_DOC_LANDING))
    names = {entry.get("name")
             for tier in field_of(body, "tiers")
             for entry in tier.get("sponsors", [])}
    assert SPONSORS[SPONSOR_LAPSED][0] not in names, (
        "a lapsed sponsor is still served on the wall")


def test_roster_source_outage_serves_the_last_good_roster(
        maintainer, anonymous, store):
    before = payload_of(anonymous.sponsors(SURFACE_DOC_LANDING))
    off = maintainer.roster_availability(False)
    assert off.status_code in SUCCESS_STATUSES, describe(off)

    run = maintainer.run_job("sync_sponsor_roster")
    assert run.status_code in SUCCESS_STATUSES, describe(run)
    settle()

    during = payload_of(anonymous.sponsors(SURFACE_DOC_LANDING))
    assert during.get("tiers") == before.get("tiers"), (
        "the wall changed while the roster source was unavailable; the last "
        "good roster must be served")
    assert field_of(during, "roster_age_seconds", "roster_age") is not None, (
        "the age of the served roster is not recorded")

    source = store.roster_source()
    assert source["last_good_fetched_at"], (
        "no last-good fetch moment is recorded on the roster source")

    back = maintainer.roster_availability(True)
    assert back.status_code in SUCCESS_STATUSES, describe(back)


def test_version_list_is_newest_first_and_omits_the_draft(anonymous):
    response = anonymous.versions()
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    labels = [entry.get("label") for entry in rows_of(response)]
    assert labels == [VERSION_PUBLISHED, VERSION_ARCHIVED], (
        f"the version control lists {labels}, expected the published version "
        f"first and the archived one after")
    assert VERSION_DRAFT not in labels, (
        "the draft version is offered to a visitor")


def test_archived_version_is_readable_and_missing_pages_land_on_the_index(
        anonymous):
    module_slug = MISSING_IN_ARCHIVED
    page_slug = PAGES[module_slug][0]

    published = anonymous.page_of(VERSION_PUBLISHED, module_slug, page_slug)
    assert published.status_code in SUCCESS_STATUSES, describe(published)

    archived = anonymous.page_of(VERSION_ARCHIVED, module_slug, page_slug)
    assert archived.status_code in SUCCESS_STATUSES, (
        f"switching to {VERSION_ARCHIVED} answered {archived.status_code}; the "
        f"visitor lands on the module index rather than a not-found page")
    body = payload_of(archived)
    assert field_of(body, "notice", "version_notice"), (
        "no notice explains that the page is absent from this version")

    tree = anonymous.tree(VERSION_ARCHIVED)
    slugs = [entry.get("slug") for entry in (tree.json() if isinstance(tree.json(), list)
                                             else tree.json().get("modules"))]
    assert module_slug not in slugs, (
        f"{module_slug} is present in {VERSION_ARCHIVED}, so the fixture no "
        f"longer proves the missing-page rule")


def test_unauthenticated_studio_routes_are_denied(anonymous, site_base):
    for path in STUDIO_ROUTES:
        response = anonymous.get(path.replace("/api", "", 1))
        assert response.status_code in DENIAL_STATUSES, (
            f"{path} served a signed-out caller: {describe(response)}")

    page_response = fetch(site_base, STUDIO_ROUTE)
    assert page_response.status_code in DENIAL_STATUSES + REDIRECT_STATUSES, (
        f"{STUDIO_ROUTE} served a signed-out caller: {describe(page_response)}")
    assert MAINTAINER_NAME not in page_response.text, (
        "the rejected studio request served the protected content anyway")


def test_wrong_password_is_refused_without_naming_the_wrong_half(app_base):
    wrong = httpx.post(f"{app_base}/auth/login",
                       json={"email": MAINTAINER_EMAIL, "password": "not-the-one"},
                       timeout=30.0)
    assert wrong.status_code in REFUSAL_STATUSES, describe(wrong)
    body = wrong.text.lower()
    for leak in ("password is wrong", "no such account", "unknown email",
                 "incorrect password", "account not found"):
        assert leak not in body, (
            f"the refusal names which half was wrong: {leak!r} in {describe(wrong)}")

    unknown = httpx.post(f"{app_base}/auth/login",
                         json={"email": probe_email(), "password": PASSWORD},
                         timeout=30.0)
    assert unknown.status_code == wrong.status_code, (
        f"an unknown address answers {unknown.status_code} while a wrong "
        f"password answers {wrong.status_code}; the two must read the same")


def test_signing_out_invalidates_the_token(maintainer):
    before = maintainer.studio_versions()
    assert before.status_code in SUCCESS_STATUSES, describe(before)

    out = maintainer.post("/auth/logout", {})
    assert out.status_code in SUCCESS_STATUSES, describe(out)

    after = maintainer.studio_versions()
    assert after.status_code in DENIAL_STATUSES, (
        f"a replayed token still reaches the studio: {describe(after)}")


def test_no_public_route_offers_a_sign_in_control(site_base):
    for route in PUBLIC_ROUTES:
        response = fetch(site_base, route, follow_redirects=True)
        assert response.status_code in SUCCESS_STATUSES, describe(response)
        body = response.text
        assert 'href="/login"' not in body, (
            f"{route} links to the sign-in page; the public site carries none")
        assert 'type="password"' not in body, (
            f"{route} offers a password field to a visitor")


def test_draft_version_is_denied_to_a_signed_out_caller_at_every_address(
        anonymous, store, site_base):
    draft = store.version(VERSION_DRAFT)
    assert draft is not None, "the draft version is absent from the store"

    module_slug, page_slug = FIRST_PAGE
    served = anonymous.page_of(VERSION_DRAFT, module_slug, page_slug)
    assert served.status_code in DENIAL_STATUSES, (
        f"the draft page was served to a signed-out caller: {describe(served)}")

    preview = fetch(site_base, f"/preview/{PREVIEW_KEY}")
    assert preview.status_code in DENIAL_STATUSES + REDIRECT_STATUSES, (
        f"the preview address served a signed-out caller: {describe(preview)}")
    assert DRAFT_BROKEN_LINK not in preview.text, (
        "the rejected preview request served the draft content anyway")

    tree = anonymous.tree(VERSION_DRAFT)
    assert tree.status_code in DENIAL_STATUSES, (
        f"the draft tree was served to a signed-out caller: {describe(tree)}")


def test_draft_version_is_absent_from_the_sitemap_and_from_search(
        anonymous, site_base):
    sitemap = fetch(site_base, "/sitemap.xml")
    assert sitemap.status_code in SUCCESS_STATUSES, describe(sitemap)
    body = sitemap.text
    assert PREVIEW_KEY not in body, "the preview address appears in the sitemap"
    assert DRAFT_BROKEN_LINK not in body, (
        "a draft page appears in the sitemap")
    for module_slug, page_slug in flat_positions()[:5]:
        assert page_route(module_slug, page_slug) in body, (
            f"{module_slug}/{page_slug} is absent from the sitemap")

    index = anonymous.search_index(VERSION_PUBLISHED)
    assert DRAFT_BROKEN_LINK not in index.text, (
        "a draft page appears in the published search index")


def test_preview_address_serves_the_draft_to_the_maintainer(maintainer, store):
    draft = store.version(VERSION_DRAFT)
    response = maintainer.get(f"/pages/{VERSION_DRAFT}/{FIRST_PAGE[0]}/{FIRST_PAGE[1]}")
    assert response.status_code in SUCCESS_STATUSES, (
        f"the maintainer cannot read the draft: {describe(response)}")
    assert str(draft["preview_key"]) == PREVIEW_KEY


def test_publish_refuses_a_broken_internal_link_and_names_the_check(
        maintainer, store, anonymous):
    draft = store.version(VERSION_DRAFT)
    validation = maintainer.validate_version(draft["id"])
    assert validation.status_code in SUCCESS_STATUSES, describe(validation)
    checks = payload_of(validation)
    reported = field_of(checks, "checks", "results")
    named = {entry.get("check") or entry.get("name"): entry.get("passed")
             for entry in reported}
    assert len(named) == 9, (
        f"validation reported {len(named)} checks, expected nine: {sorted(named)}")
    failing = [name for name, passed in named.items() if passed is False]
    assert failing, "no check failed on a draft whose internal link targets nothing"
    assert any("link" in str(name).lower() for name in failing), (
        f"the internal-link check did not fail: {failing}")

    attempt = maintainer.publish_version(draft["id"])
    assert attempt.status_code in REFUSAL_STATUSES, (
        f"a draft with a broken internal link was published: {describe(attempt)}")

    current = store.current_version()
    assert current["label"] == VERSION_PUBLISHED, (
        f"the refused publish moved the current version to {current['label']!r}")

    versions = [entry.get("label") for entry in rows_of(anonymous.versions())]
    assert VERSION_DRAFT not in versions, (
        "the refused draft reached the version control anyway")


def test_publish_refuses_a_gap_in_the_flattened_sequence(maintainer, store):
    label = f"9.0.0-{unique_suffix()}"
    created = maintainer.create_version(label, f"0009.0000.{unique_suffix()[:4]}")
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    version_id = field_of(payload_of(created), "id")

    module = maintainer.create_module({
        "version_id": version_id, "slug": "gap-module", "name": "Gap module",
        "ramp": "red", "position": 1, "tile_position": None,
        "object": "renderer", "badge": "none", "badge_expires_at": None})
    assert module.status_code in SUCCESS_STATUSES, describe(module)

    attempt = maintainer.publish_version(version_id)
    assert attempt.status_code in REFUSAL_STATUSES, (
        f"a version whose module holds no page was published: {describe(attempt)}")
    body = attempt.text.lower()
    assert "page" in body or "orphan" in body, (
        f"the refusal does not name the failing check: {describe(attempt)}")

    current = store.current_version()
    assert current["label"] == VERSION_PUBLISHED, (
        "the refused publish moved the current version")


def test_publish_refuses_a_badge_with_no_expiry_and_an_unknown_family(maintainer):
    label = f"9.1.0-{unique_suffix()}"
    created = maintainer.create_version(label, f"0009.0001.{unique_suffix()[:4]}")
    version_id = field_of(payload_of(created), "id")

    unknown = maintainer.create_module({
        "version_id": version_id, "slug": "bad-family", "name": "Bad family",
        "ramp": "not-a-family", "position": 1, "object": "renderer",
        "badge": "none"})
    if unknown.status_code in SUCCESS_STATUSES:
        attempt = maintainer.publish_version(version_id)
        assert attempt.status_code in REFUSAL_STATUSES, (
            f"a module naming a colour family outside the twenty-one was "
            f"published: {describe(attempt)}")
    else:
        assert unknown.status_code in REFUSAL_STATUSES, describe(unknown)

    badged = maintainer.create_module({
        "version_id": version_id, "slug": "bad-badge", "name": "Bad badge",
        "ramp": "red", "position": 2, "object": "renderer",
        "badge": "new", "badge_expires_at": None})
    if badged.status_code in SUCCESS_STATUSES:
        attempt = maintainer.publish_version(version_id)
        assert attempt.status_code in REFUSAL_STATUSES, (
            f"a badge set with no expiry was published: {describe(attempt)}")
    else:
        assert badged.status_code in REFUSAL_STATUSES, describe(badged)


def test_publish_is_atomic_and_leaves_the_previous_version_readable(
        maintainer, anonymous, store, objects):
    draft = store.version(VERSION_DRAFT)
    module_slug, page_slug = FIRST_PAGE
    pages = maintainer.get(f"/pages/{VERSION_DRAFT}/{module_slug}/{page_slug}")
    assert pages.status_code in SUCCESS_STATUSES, describe(pages)
    page_id = field_of(payload_of(pages), "id")

    repaired = maintainer.amend_page(page_id, {
        "body": "The installation page, with every internal link resolving."})
    assert repaired.status_code in SUCCESS_STATUSES, describe(repaired)

    validation = payload_of(maintainer.validate_version(draft["id"]))
    reported = field_of(validation, "checks", "results")
    assert all(entry.get("passed") for entry in reported), (
        f"the repaired draft still fails a check: {reported}")

    published = maintainer.publish_version(draft["id"])
    assert published.status_code in SUCCESS_STATUSES, describe(published)
    settle()

    current = store.current_version()
    assert current["label"] == VERSION_DRAFT, (
        f"the current version is {current['label']!r} after a successful publish")
    assert store.version(VERSION_PUBLISHED)["state"] == "archived", (
        "the previous version was not archived")

    labels = [entry.get("label") for entry in rows_of(anonymous.versions())]
    assert VERSION_PUBLISHED in labels, (
        "the previous snapshot is no longer readable through the version control")
    assert objects.exists(index_key(VERSION_DRAFT)), (
        f"the promoted version carries no index object at "
        f"{index_key(VERSION_DRAFT)}")

    restored = maintainer.publish_version(store.version(VERSION_PUBLISHED)["id"])
    assert restored.status_code in SUCCESS_STATUSES, describe(restored)


def test_a_second_current_version_is_refused_by_the_database(store):
    current = store.query("SELECT * FROM version WHERE is_current = true")
    assert len(current) == 1, (
        f"{len(current)} versions are current, expected exactly one")

    indexes = store.query(
        "SELECT indexdef FROM pg_indexes WHERE tablename = 'version'")
    constraints = store.query(
        "SELECT conname, pg_get_constraintdef(oid) AS definition "
        "FROM pg_constraint WHERE conrelid = 'version'::regclass")
    triggers = store.query(
        "SELECT tgname FROM pg_trigger WHERE tgrelid = 'version'::regclass "
        "AND NOT tgisinternal")

    enforced = (
        any("is_current" in str(row["indexdef"]).lower()
            and "unique" in str(row["indexdef"]).lower() for row in indexes)
        or any("is_current" in str(row["definition"]).lower()
               for row in constraints)
        or bool(triggers))
    assert enforced, (
        "the engine carries no guard holding at most one current version, so "
        "the rule lives only in application code: indexes="
        f"{[row['indexdef'] for row in indexes]} constraints="
        f"{[row['conname'] for row in constraints]}")


def test_subscription_creates_a_pending_row_and_queues_one_confirmation(
        anonymous, store):
    address = probe_email()
    response = anonymous.subscribe(address, LIST_WAITLIST,
                                   timing_token=timing_token(anonymous))
    assert response.status_code in SUCCESS_STATUSES, describe(response)

    row = poll_until(lambda: store.subscriber(address, LIST_WAITLIST))
    assert row is not None, f"no subscriber row was written for {address}"
    assert row["state"] == STATE_PENDING, (
        f"{address} was written as {row['state']!r}, expected {STATE_PENDING!r}")
    assert row["confirm_token_digest"], (
        f"{address} carries no confirmation token digest")
    assert row["source_route"], f"{address} records no source route"

    queued = store.outbox_for(row["id"])
    assert len(queued) == 1, (
        f"{len(queued)} messages were queued for one submission, expected one")
    assert queued[0]["kind"] == "confirmation", (
        f"the queued message is a {queued[0]['kind']!r}")

    body = response.text.lower()
    assert "confirm" in body, (
        f"the form does not report that a confirmation was sent: {describe(response)}")
    for wrong in ("you are subscribed", "you're subscribed", "subscription active"):
        assert wrong not in body, (
            f"the form reports a subscription rather than a confirmation: {wrong!r}")


def test_confirmation_token_works_once_and_a_second_use_reports_confirmed(
        anonymous, maintainer, store):
    address = probe_email()
    anonymous.subscribe(address, LIST_WAITLIST,
                        timing_token=timing_token(anonymous))
    row = poll_until(lambda: store.subscriber(address, LIST_WAITLIST))
    assert row is not None

    queued = store.outbox_for(row["id"])
    delivered = maintainer.deliver(queued[0]["id"])
    assert delivered.status_code in SUCCESS_STATUSES, describe(delivered)
    token = field_of(payload_of(delivered), "token", "confirm_token")
    assert token, "delivering the confirmation yielded no token"
    assert token != row["confirm_token_digest"], (
        "the stored digest equals the token, so the token itself is at rest")

    first = anonymous.confirm(token)
    assert first.status_code in SUCCESS_STATUSES, describe(first)
    confirmed = poll_until(
        lambda: store.subscriber(address, LIST_WAITLIST)["state"] == STATE_CONFIRMED)
    assert confirmed, f"{address} did not reach {STATE_CONFIRMED!r}"

    second = anonymous.confirm(token)
    assert second.status_code in SUCCESS_STATUSES, (
        f"a second use of a consumed token errored: {describe(second)}")
    assert "already" in second.text.lower(), (
        f"a second use does not report the address as already confirmed: "
        f"{describe(second)}")


def test_expired_token_offers_a_new_confirmation(anonymous, store):
    row = store.subscriber(EXPIRED_EMAIL, LIST_NEWSLETTER)
    assert row is not None, f"{EXPIRED_EMAIL} is absent from the store"
    assert row["state"] == STATE_PENDING
    response = anonymous.confirm("expired-token-probe")
    assert response.status_code in SUCCESS_STATUSES + REFUSAL_STATUSES, (
        describe(response))
    body = response.text.lower()
    assert "expired" in body or "send another" in body or "new" in body, (
        f"an expired or unknown token offers no new confirmation: "
        f"{describe(response)}")
    assert str(row["confirm_expires_at"]).startswith("2026-09-09"), (
        f"{EXPIRED_EMAIL} token expiry is {row['confirm_expires_at']!r}")


def test_already_confirmed_and_complained_addresses_send_nothing(
        anonymous, store):
    for address, mailing_list in ((CONFIRMED_EMAIL, LIST_WAITLIST),
                                  (COMPLAINED_EMAIL, LIST_NEWSLETTER)):
        row = store.subscriber(address, mailing_list)
        before = len(store.outbox_for(row["id"]))
        response = anonymous.subscribe(address, mailing_list,
                                       timing_token=timing_token(anonymous))
        assert response.status_code in SUCCESS_STATUSES, (
            f"{address} was refused rather than thanked: {describe(response)}")
        settle()
        after = len(store.outbox_for(row["id"]))
        assert after == before, (
            f"{after - before} messages were queued for {address}, expected none")
        assert store.subscriber(address, mailing_list)["state"] == row["state"], (
            f"{address} changed state on a re-submission")


def test_unsubscribed_address_begins_a_new_pending_cycle(anonymous, store):
    row = store.subscriber(UNSUBSCRIBED_EMAIL, LIST_NEWSLETTER)
    assert row["state"] == STATE_UNSUBSCRIBED
    before = len(store.outbox_for(row["id"]))

    response = anonymous.subscribe(UNSUBSCRIBED_EMAIL, LIST_NEWSLETTER,
                                   timing_token=timing_token(anonymous))
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    changed = poll_until(
        lambda: store.subscriber(UNSUBSCRIBED_EMAIL,
                                 LIST_NEWSLETTER)["state"] == STATE_PENDING)
    assert changed, "an unsubscribed address did not begin a new pending cycle"
    assert len(store.outbox_for(row["id"])) > before, (
        "no confirmation was queued for the new cycle")


def test_two_lists_hold_one_address_as_two_rows(anonymous, store):
    address = probe_email()
    for mailing_list in (LIST_WAITLIST, LIST_NEWSLETTER):
        response = anonymous.subscribe(address, mailing_list,
                                       timing_token=timing_token(anonymous))
        assert response.status_code in SUCCESS_STATUSES, describe(response)
    rows = poll_until(lambda: store.subscribers_for(address)
                      if len(store.subscribers_for(address)) == 2 else None)
    assert rows and len(rows) == 2, (
        f"{address} produced {len(store.subscribers_for(address))} rows, "
        f"expected one per list")
    assert {row["list"] for row in rows} == {LIST_WAITLIST, LIST_NEWSLETTER}, (
        "the two rows do not name the two lists")


def test_concurrent_submissions_of_one_address_queue_one_message(
        anonymous, store):
    address = probe_email()
    token = timing_token(anonymous)

    def submit():
        return anonymous.subscribe(address, LIST_WAITLIST, timing_token=token)

    with ThreadPoolExecutor(max_workers=CONCURRENT_SUBMISSIONS) as pool:
        results = list(pool.map(lambda _: submit(), range(CONCURRENT_SUBMISSIONS)))

    accepted = [r for r in results if r.status_code in SUCCESS_STATUSES]
    assert accepted, f"every concurrent submission was refused: {describe(results[0])}"

    rows = store.subscribers_for(address)
    assert len(rows) == 1, (
        f"{CONCURRENT_SUBMISSIONS} simultaneous submissions produced {len(rows)} "
        f"rows, expected one")
    queued = store.outbox_for(rows[0]["id"])
    assert len(queued) == 1, (
        f"{len(queued)} messages were queued, expected one")


def test_address_rate_limit_binds_before_the_origin_limit(anonymous, store):
    address = probe_email()
    statuses = []
    for _ in range(ADDRESS_LIMIT_PER_HOUR + 2):
        response = anonymous.subscribe(address, LIST_WAITLIST,
                                       timing_token=timing_token(anonymous))
        statuses.append(response.status_code)
    assert any(status in RATE_LIMITED_STATUSES for status in statuses), (
        f"more than {ADDRESS_LIMIT_PER_HOUR} submissions per address were "
        f"accepted: {statuses}")
    assert ORIGIN_LIMIT_PER_HOUR > ADDRESS_LIMIT_PER_HOUR, (
        "the address limit is the binding one")

    counters = store.rows("rate_limit_counter", scope="address")
    assert counters, "no per-address rate-limit counter was written"


def test_decoy_field_and_timing_token_refuse_a_machine_submission(
        anonymous, store):
    decoyed = probe_email()
    filled = anonymous.subscribe(decoyed, LIST_WAITLIST, honeypot="lumen.example",
                                 timing_token=timing_token(anonymous))
    assert filled.status_code in REFUSAL_STATUSES + SUCCESS_STATUSES, describe(filled)
    settle()
    assert store.subscriber(decoyed, LIST_WAITLIST) is None, (
        f"a submission with {HONEYPOT_FIELD} filled wrote a row for {decoyed}")

    instant = probe_email()
    fast = anonymous.subscribe(instant, LIST_WAITLIST, timing_token="")
    assert fast.status_code in REFUSAL_STATUSES + SUCCESS_STATUSES, describe(fast)
    settle()
    assert store.subscriber(instant, LIST_WAITLIST) is None, (
        f"a submission arriving inside {TIMING_TOKEN_SECONDS} seconds wrote a "
        f"row for {instant}")


def test_every_rejection_reads_the_same_to_the_submitter(anonymous):
    token = timing_token(anonymous)
    invalid = anonymous.subscribe("not-an-address", LIST_WAITLIST,
                                  timing_token=token)
    taken = anonymous.subscribe(CONFIRMED_EMAIL, LIST_WAITLIST,
                                timing_token=timing_token(anonymous))
    assert taken.status_code in SUCCESS_STATUSES, (
        f"an already-confirmed address was refused, which turns the form into a "
        f"membership oracle: {describe(taken)}")
    assert "already" not in taken.text.lower(), (
        f"the response reveals that the address is already on the list: "
        f"{describe(taken)}")
    assert invalid.status_code in REFUSAL_STATUSES, describe(invalid)


def test_mail_callback_without_a_valid_signature_changes_nothing(
        anonymous, store):
    row = store.subscriber(CONFIRMED_EMAIL, LIST_WAITLIST)
    before = row["state"]
    event_id = f"evt-{unique_suffix()}"
    response = anonymous.mail_hook(
        {"event_id": event_id, "type": "complained", "email": CONFIRMED_EMAIL},
        signature="not-a-signature")
    assert response.status_code in REFUSAL_STATUSES, (
        f"an unsigned callback was accepted: {describe(response)}")
    settle()
    assert store.subscriber(CONFIRMED_EMAIL, LIST_WAITLIST)["state"] == before, (
        "an unverified callback changed a subscriber's state")
    assert store.mail_events(event_id) == [] or all(
        not entry["signature_valid"] for entry in store.mail_events(event_id)), (
        "an unverified callback was recorded as valid")


def test_repeated_provider_event_identifier_changes_nothing_twice(
        anonymous, maintainer, store):
    address = probe_email()
    created = anonymous.subscribe(address, LIST_NEWSLETTER,
                                  timing_token=timing_token(anonymous))
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    row = poll_until(lambda: store.subscriber(address, LIST_NEWSLETTER))
    assert row is not None

    event_id = f"evt-{unique_suffix()}"
    body = {"event_id": event_id, "type": "bounced_hard", "email": address,
            "list": LIST_NEWSLETTER}
    first = maintainer.mail_event(body)
    assert first.status_code in SUCCESS_STATUSES, describe(first)
    settle()
    assert store.subscriber(address, LIST_NEWSLETTER)["state"] == STATE_BOUNCED, (
        f"a hard bounce did not move {address} to {STATE_BOUNCED!r}")

    second = maintainer.mail_event(body)
    assert second.status_code in SUCCESS_STATUSES, describe(second)
    settle()
    events = store.mail_events(event_id)
    assert len(events) == 1, (
        f"the repeated event identifier was recorded {len(events)} times")
    assert store.subscriber(address, LIST_NEWSLETTER)["state"] == STATE_BOUNCED, (
        "a repeated event changed a state the first arrival had already set")


def test_out_of_order_mail_callbacks_leave_the_correct_final_state(
        anonymous, maintainer, store):
    address = probe_email()
    anonymous.subscribe(address, LIST_NEWSLETTER,
                        timing_token=timing_token(anonymous))
    row = poll_until(lambda: store.subscriber(address, LIST_NEWSLETTER))
    assert row is not None

    complained = {"event_id": f"evt-{unique_suffix()}", "type": "complained",
                  "email": address, "list": LIST_NEWSLETTER, "sequence": 2}
    delivered = {"event_id": f"evt-{unique_suffix()}", "type": "delivered",
                 "email": address, "list": LIST_NEWSLETTER, "sequence": 1}
    late = maintainer.mail_event(complained)
    assert late.status_code in SUCCESS_STATUSES, describe(late)
    early = maintainer.mail_event(delivered)
    assert early.status_code in SUCCESS_STATUSES, describe(early)
    settle()

    final = store.subscriber(address, LIST_NEWSLETTER)["state"]
    assert final == STATE_COMPLAINED, (
        f"{address} ended in {final!r}; a complaint is permanent and an "
        f"out-of-order delivery must not undo it")


def test_provider_outage_holds_the_queue_and_loses_no_submission(
        anonymous, maintainer, store):
    address = probe_email()
    response = anonymous.subscribe(address, LIST_WAITLIST,
                                   timing_token=timing_token(anonymous))
    assert response.status_code in SUCCESS_STATUSES, (
        f"a submission was refused while the provider was unavailable: "
        f"{describe(response)}")
    row = poll_until(lambda: store.subscriber(address, LIST_WAITLIST))
    assert row is not None, "the submission was lost"
    assert row["state"] == STATE_PENDING, (
        f"{address} left the pending state without a confirmation")

    queued = maintainer.outbox(state="queued")
    assert queued.status_code in SUCCESS_STATUSES, describe(queued)
    ids = {entry.get("subscriber_id") for entry in rows_of(queued)}
    assert row["id"] in ids or str(row["id"]) in {str(i) for i in ids}, (
        "the confirmation is not holding in the queue")


def test_exhausted_job_is_dead_lettered_and_never_discarded(maintainer, store):
    response = maintainer.dead_letters()
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    assert isinstance(rows_of(response), list)

    runs = maintainer.jobs()
    assert runs.status_code in SUCCESS_STATUSES, describe(runs)
    names = {entry.get("job_name") for entry in rows_of(runs)}
    assert set(JOBS) >= names, (
        f"a job run names {names - set(JOBS)}, which is outside the ten")
    assert MAX_ATTEMPTS == 5, "the brief bounds a job at five attempts"


def test_scheduled_job_lock_refuses_an_overlapping_run(maintainer, store):
    job = "sync_sponsor_roster"

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(maintainer.run_job, job) for _ in range(2)]
        results = [future.result() for future in futures]

    statuses = sorted(result.status_code for result in results)
    assert any(status in REFUSAL_STATUSES for status in statuses), (
        f"two overlapping runs of {job} were both accepted: {statuses}")

    runs = store.job_runs(job)
    assert runs, f"{job} left no job run behind"
    assert any(run["state"] == "refused" for run in runs) or \
        len([run for run in runs if run["state"] == "running"]) <= 1, (
        f"{job} ran twice at once")
    assert all(run["lock_token"] for run in runs if run["state"] != "refused"), (
        f"a {job} run took no lock")


def test_expiry_sweep_refuses_to_run_past_its_sanity_threshold(
        maintainer, store):
    response = maintainer.run_job("sweep_expired_subscriptions")
    assert response.status_code in SUCCESS_STATUSES + REFUSAL_STATUSES, (
        describe(response))
    body = payload_of(response) if response.headers.get(
        "content-type", "").startswith("application/json") else {}
    counted = body.get("counted", body.get("would_delete"))
    assert counted is not None, (
        f"the sweep does not report the count it would delete: "
        f"{describe(response)}")
    assert int(counted) <= SWEEP_SANITY_THRESHOLD, (
        f"the sweep would delete {counted} rows, above its threshold of "
        f"{SWEEP_SANITY_THRESHOLD}, and must refuse rather than run")

    runs = store.job_runs("sweep_expired_subscriptions")
    assert runs, "the sweep left no job run behind"
    assert runs[-1]["state"] in ("succeeded", "refused"), (
        f"the sweep ended {runs[-1]['state']!r}")


def test_badge_job_clears_a_badge_whose_expiry_has_passed(maintainer, store):
    response = maintainer.run_job("expire_badges")
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    settle()
    published = store.version(VERSION_PUBLISHED)
    for slug in BADGE_MODULES:
        row = store.module(published["id"], slug)
        assert str(row["badge_expires_at"]).startswith(BADGE_EXPIRES), (
            f"{slug} lost its badge expiry")
    assert BADGE_LABEL == "NEW"

    runs = store.job_runs("expire_badges")
    assert runs, "the badge job left no job run behind"


def test_roster_freshness_job_reports_the_roster_age(maintainer, store):
    response = maintainer.run_job("check_roster_freshness")
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    settle()
    runs = store.job_runs("check_roster_freshness")
    assert runs, "the freshness job left no job run behind"
    detail = str(runs[-1]["detail"])
    assert detail, "the freshness job records no detail"
    source = store.roster_source()
    assert source["fetched_at"], "the roster source records no fetch moment"
    assert ROSTER_FRESHNESS_HOURS == 24


def test_ten_jobs_are_runnable_and_named_exactly(maintainer, store):
    assert len(JOBS) == JOB_COUNT
    for job in JOBS:
        response = maintainer.run_job(job)
        assert response.status_code in SUCCESS_STATUSES + REFUSAL_STATUSES, (
            f"{job} is not a runnable job: {describe(response)}")
        assert response.status_code not in (404,), (
            f"{job} is absent from the job set: {describe(response)}")

    unknown = maintainer.run_job("not_a_real_job")
    assert unknown.status_code in REFUSAL_STATUSES, (
        f"an unknown job name was accepted: {describe(unknown)}")


def test_advertising_slot_states_are_served_and_empty_collapses(
        maintainer, anonymous, store, site_base):
    for state in AD_STATES:
        response = maintainer.set_ad_slot(state)
        assert response.status_code in SUCCESS_STATUSES, describe(response)
        served = payload_of(anonymous.ad_slot())
        assert field_of(served, "state") == state, (
            f"the slot reports {served!r} after being set to {state!r}")
        assert store.ad_slot_state()["state"] == state, (
            f"the slot state was not persisted as {state!r}")

    empty = maintainer.set_ad_slot("empty")
    assert empty.status_code in SUCCESS_STATUSES, describe(empty)
    page_body = fetch(site_base, TOUR_ROUTE, follow_redirects=True).text
    assert "advertisement unavailable" not in page_body.lower(), (
        "the site announces that the advertising slot is empty")
    assert "adblock" not in page_body.lower(), (
        "the site attempts to detect a blocked advertising slot")
    assert AD_ATTRIBUTION in page_body, (
        f"the attribution {AD_ATTRIBUTION!r} is absent from the footer")

    restored = maintainer.set_ad_slot("fills")
    assert restored.status_code in SUCCESS_STATUSES, describe(restored)


def test_page_view_log_is_readable_by_the_maintainer_alone(
        anonymous, maintainer, site_base, store):
    anonymous.storage_choice("yes")
    fetch(site_base, TOUR_ROUTE, follow_redirects=True)
    settle()

    denied = anonymous.get("/studio/page-views")
    assert denied.status_code in DENIAL_STATUSES, (
        f"a visitor read the page-view log: {describe(denied)}")

    allowed = maintainer.page_views()
    assert allowed.status_code in SUCCESS_STATUSES, describe(allowed)
    rows = rows_of(allowed)
    assert rows, "the page-view log is empty after a page was fetched"
    for row in rows[:5]:
        assert row.get("route"), f"a page-view row carries no route: {row}"

    stored = store.page_views()
    assert stored, "no page-view row lives in PostgreSQL"


def test_analytics_never_record_the_text_of_a_search(anonymous, store):
    query = f"private-project-{unique_suffix()}"
    response = anonymous.record_event(
        "search_performed", {"query_length": len(query), "result_count": 3})
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    settle()

    rows = store.analytics("search_performed")
    assert rows, "no search event was recorded"
    for row in rows:
        assert query not in str(row["attributes"]), (
            "the text of a search was recorded in the analytics stream")
        assert "query" not in str(row["attributes"]).lower() or \
            "query_length" in str(row["attributes"]), (
            f"a search event carries the query rather than its length: {row}")

    for kind in ANALYTICS_KINDS:
        assert isinstance(kind, str)
    unknown = anonymous.record_event("visitor_fingerprint", {"id": "abc"})
    assert unknown.status_code in REFUSAL_STATUSES, (
        f"an event outside the pinned set was accepted: {describe(unknown)}")


def test_storage_choice_gates_every_non_essential_write(
        anonymous, store, site_base):
    refused = anonymous.storage_choice("no")
    assert refused.status_code in SUCCESS_STATUSES, describe(refused)
    before = len(store.page_views())

    with httpx.Client(base_url=site_base, timeout=30.0,
                      follow_redirects=True) as client:
        client.get(TOUR_ROUTE)
    settle()

    after = len(store.page_views())
    assert after == before, (
        f"{after - before} page views were recorded after the visitor refused "
        f"non-essential storage")

    choice = store.rows("storage_choice", limit=5)
    assert choice, "the storage answer was not persisted"

    accepted = anonymous.storage_choice("yes")
    assert accepted.status_code in SUCCESS_STATUSES, describe(accepted)


def test_logs_carry_a_request_identifier_and_no_address(anonymous, app_base):
    address = probe_email()
    response = anonymous.subscribe(address, LIST_WAITLIST,
                                   timing_token=timing_token(anonymous))
    assert response.status_code in SUCCESS_STATUSES, describe(response)

    error = httpx.get(f"{app_base}/no-such-resource", timeout=30.0)
    assert error.status_code in REFUSAL_STATUSES, describe(error)
    body = error.json()
    assert CORRELATION_FIELD in body, (
        f"an error response carries no {CORRELATION_FIELD}: {describe(error)}")
    assert address not in error.text, (
        "an error body echoed a subscriber address")


def test_every_response_carries_the_security_headers(site_base):
    response = fetch(site_base, TOUR_ROUTE, follow_redirects=True)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    headers = {name.lower(): value for name, value in response.headers.items()}

    assert "strict-transport-security" in headers, (
        f"no strict transport policy: {sorted(headers)}")
    assert headers.get("x-content-type-options", "").lower() == "nosniff", (
        f"the content-type policy is {headers.get('x-content-type-options')!r}")
    assert "referrer-policy" in headers, "no referrer policy"
    assert "strict-origin-when-cross-origin" in headers["referrer-policy"], (
        f"the referrer policy is {headers['referrer-policy']!r}")
    assert "content-security-policy" in headers, "no content security policy"
    policy = headers["content-security-policy"]
    assert "form-action" in policy, (
        f"the content policy does not restrict form actions: {policy[:200]}")
    assert "frame-ancestors" in policy, (
        f"the content policy does not deny frame ancestors: {policy[:200]}")
    assert "permissions-policy" in headers, "no permissions policy"
    for feature in ("camera", "microphone", "geolocation", "payment"):
        assert feature in headers["permissions-policy"], (
            f"the permissions policy does not deny {feature}")


def test_unknown_address_answers_not_found_and_never_serves_the_tour(site_base):
    for path in (f"/no-such-page-{unique_suffix()}",
                 f"{DOCS_ROUTE}/no-such-module",
                 f"{DOCS_ROUTE}/timer/no-such-page"):
        response = fetch(site_base, path)
        assert response.status_code in NOT_FOUND_STATUSES, (
            f"{path} answered {response.status_code}, expected not-found: "
            f"{describe(response)}")
        assert TOUR_HEADLINE not in response.text, (
            f"{path} served the tour instead of the not-found page")
        assert NOT_FOUND_HEADING in response.text, (
            f"{path} does not carry the not-found heading")
        assert NOT_FOUND_BODY in response.text, (
            f"{path} does not carry the not-found body")

    documentation = fetch(site_base, f"{DOCS_ROUTE}/timer/no-such-page")
    assert SEARCH_PLACEHOLDER in documentation.text, (
        "a failed documentation address offers no search control")
    assert "no-such-page" in documentation.text, (
        "the failed segment is not prefilled into the offered search")


def test_every_internal_link_on_every_published_route_resolves(site_base):
    seen = set()
    for route in PUBLIC_ROUTES + (page_route(*FIRST_PAGE),
                                  page_route(*LAST_PAGE)):
        response = fetch(site_base, route, follow_redirects=True)
        assert response.status_code in SUCCESS_STATUSES, describe(response)
        for chunk in response.text.split('href="')[1:]:
            target = chunk.split('"', 1)[0]
            if not target.startswith("/") or target.startswith("//"):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target or target in seen:
                continue
            seen.add(target)
            linked = fetch(site_base, target, follow_redirects=True)
            assert linked.status_code in SUCCESS_STATUSES, (
                f"{route} links to {target}, which answers "
                f"{linked.status_code}")
    assert len(seen) > 5, f"only {len(seen)} internal links were followed"


def test_privacy_page_states_what_is_kept_and_how_it_is_erased(site_base):
    response = fetch(site_base, PRIVACY_ROUTE, follow_redirects=True)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = response.text.lower()
    for phrase in ("address", "confirmation", "page view", "erase"):
        assert phrase in body, (
            f"the privacy page does not mention {phrase!r}")
    for absent in ("name", "company", "profile"):
        assert absent in body, (
            f"the privacy page does not state that no {absent} is kept")

    for route in PUBLIC_ROUTES:
        page_body = fetch(site_base, route, follow_redirects=True).text
        assert PRIVACY_ROUTE in page_body, (
            f"{route} does not reach the privacy page from its footer")


def test_rows_live_in_postgres_and_survive_a_restart_of_the_process(
        store, anonymous):
    address = probe_email()
    response = anonymous.subscribe(address, LIST_WAITLIST,
                                   timing_token=timing_token(anonymous))
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    row = poll_until(lambda: store.subscriber(address, LIST_WAITLIST))
    assert row is not None, (
        f"{address} is absent from PostgreSQL, so the row lived in the process")

    for table in ("version", "module", "page", "page_anchor", "demo",
                  "sponsor_tier", "sponsor", "subscriber", "outbox_message",
                  "job_run", "page_view", "analytics_event"):
        assert store.count(table) >= 0, (
            f"table {table} is absent from PostgreSQL")
    assert store.count("module") >= MODULE_COUNT, (
        f"only {store.count('module')} module rows live in PostgreSQL")


def test_documentation_routes_are_complete_documents_under_one_origin(
        site_base, app_base):
    module_slug, page_slug = ("timer", "create-timer")
    response = fetch(site_base, page_route(module_slug, page_slug),
                     follow_redirects=True)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = response.text
    assert "<article" in body.lower(), (
        "the documentation route returns no article element, so the page is "
        "assembled in the browser rather than rendered ahead of time")
    assert page_slug.replace("-", " ") in body.lower() or page_slug in body, (
        "the article's own content is absent from the returned document")
    assert "<title>" in body.lower(), "the returned document carries no title"
    assert IN_SECTION_HEADING in body, (
        "the generated sibling list is absent from the returned document")

    assert app_base.endswith("/api"), (
        f"the HTTP API is not served under the /api prefix: {app_base}")
    assert app_base.startswith(site_base), (
        f"the API origin {app_base} differs from the site origin {site_base}")
    health = httpx.get(f"{app_base}/health", timeout=30.0)
    assert health.status_code == 200, describe(health)


def test_page_tour_leads_with_one_primary_action_and_its_install_line(
        page, site_base):
    page.goto(f"{site_base}{TOUR_ROUTE}", wait_until="load")
    content = page.content()
    assert TOUR_HEADLINE in content, "the tour headline is absent"
    assert INSTALL_LINE in content, "the install line is absent"
    assert SECONDARY_CALL in content, "the secondary call is absent"
    assert FUNDING_LABEL in content, "the funding call is absent"
    for label in NAV_LABELS:
        assert label in content, f"navigation label {label} is absent"

    primary = page.locator("[data-primary-action]")
    assert primary.count() == 1, (
        f"the tour carries {primary.count()} primary actions, expected one")

    outside = page.evaluate(
        "() => { const stage = document.querySelector('[data-scene-state]');"
        " const line = document.querySelector('[data-specimen]');"
        " return !!(stage && line) && !stage.contains(line); }")
    assert outside, (
        "the install line sits inside the stage, so it stops working when the "
        "scene does not run")


def test_page_tour_stops_are_in_the_document_at_all_times(page, site_base):
    page.goto(f"{site_base}{TOUR_ROUTE}", wait_until="load")
    assert "?" not in page.url, (
        f"the tour uses query addressing, which belongs to the editor alone: "
        f"{page.url}")
    stops = page.eval_on_selector_all(
        "[data-stop]", "nodes => nodes.map(n => n.getAttribute('data-stop'))")
    assert stops == list(STOPS), (
        f"the tour carries stops {stops}, expected {list(STOPS)}")
    assert len(stops) == STOP_COUNT

    text = page.eval_on_selector_all(
        "[data-stop]", "nodes => nodes.map(n => n.textContent.trim().length)")
    assert all(length > 0 for length in text), (
        "a stop carries no text in the document, so it is injected on arrival")

    headline = page.locator("[data-stop='intro'] h1, h1").first
    copied = headline.evaluate("node => node.textContent")
    assert " " in copied.strip(), (
        f"the split headline copies without spaces: {copied!r}")
    label = page.get_attribute("[data-stop='intro']", "aria-label") or copied
    assert label.strip(), "the split headline carries no intact accessible name"


def test_page_tour_stop_is_driven_by_scroll_and_reverses(page, site_base):
    page.goto(f"{site_base}{TOUR_ROUTE}", wait_until="load")
    first = page.get_attribute("[data-current-stop]", "data-current-stop")
    assert first == STOPS[0], (
        f"the tour opens on stop {first!r}, expected {STOPS[0]!r}")

    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight * 0.45)")
    page.wait_for_timeout(600)
    middle = page.get_attribute("[data-current-stop]", "data-current-stop")
    assert middle != first, (
        "scrolling did not move the current stop, so it is not scroll-driven")
    assert middle in STOPS, f"the current stop is {middle!r}"

    page.evaluate("() => window.scrollTo(0, 0)")
    page.wait_for_timeout(600)
    back = page.get_attribute("[data-current-stop]", "data-current-stop")
    assert back == first, (
        f"scrolling back left the tour on stop {back!r} rather than {first!r}")


def test_page_tour_tile_hover_lights_the_module_arc(page, site_base):
    page.goto(f"{site_base}{TOUR_ROUTE}", wait_until="load")
    tiles = page.locator("[data-module-tile]")
    assert tiles.count() == TILE_COUNT, (
        f"the module grid carries {tiles.count()} tiles, expected {TILE_COUNT}")

    slug = tiles.first.get_attribute("data-module-tile")
    arc = page.locator(f"[data-arc='{slug}']")
    assert arc.count() == 1, f"no arc is drawn for module {slug!r}"
    assert arc.first.get_attribute("data-arc-lit") == "false", (
        f"the arc for {slug} is lit before anything points at its tile")

    tiles.first.hover()
    page.wait_for_timeout(400)
    assert arc.first.get_attribute("data-arc-lit") == "true", (
        f"pointing at the {slug} tile did not light its arc on the instrument")

    ring = page.evaluate(
        "() => { const stage = document.querySelector('[data-scene-state]');"
        " const arcs = document.querySelectorAll('[data-arc]');"
        " return Array.from(arcs).every(a => !stage || !stage.contains(a)); }")
    assert ring, (
        "the arcs live inside the stage, so losing the scene loses the ring too")


def test_page_scene_degrades_to_the_drawn_ring(page, site_base):
    page.goto(f"{site_base}{TOUR_ROUTE}", wait_until="load")
    state = page.get_attribute("[data-scene-state]", "data-scene-state")
    assert state in DEGRADATION_STATES, (
        f"the stage reports state {state!r}, outside {list(DEGRADATION_STATES)}")

    page.evaluate(
        "() => { const c = document.createElement('canvas');"
        " HTMLCanvasElement.prototype.getContext = () => null;"
        " return !!c; }")
    page.reload(wait_until="load")
    page.wait_for_timeout(600)
    degraded = page.get_attribute("[data-scene-state]", "data-scene-state")
    assert degraded in DEGRADATION_STATES, (
        f"with no rendering context the stage reports {degraded!r}")
    assert page.locator("[data-arc]").count() > 0, (
        "the drawn arcs disappeared with the scene")
    assert TOUR_HEADLINE in page.content(), (
        "the tour lost its headline when the scene could not run")


def test_page_reduced_motion_holds_a_still_instrument(page, still_page, site_base):
    page.goto(f"{site_base}{TOUR_ROUTE}", wait_until="load")
    page.wait_for_timeout(600)
    moving = page.evaluate("() => document.getAnimations().length")
    assert moving > 0, (
        "nothing moves on the tour with no stated preference against movement, "
        "so the still comparison below proves nothing")

    still_page.goto(f"{site_base}{TOUR_ROUTE}", wait_until="load")
    still_page.wait_for_timeout(600)
    assert still_page.locator("[data-scene-state]").count() == 1, (
        "the instrument was removed under a reduced-motion preference rather "
        "than held as one still frame")
    running = still_page.evaluate("() => document.getAnimations().length")
    assert running == 0, (
        f"{running} animations run under a reduced-motion preference")
    assert TOUR_HEADLINE in still_page.content(), (
        "the headline is absent in its final state")

    still_page.goto(f"{site_base}{EDITOR_ROUTE}", wait_until="load")
    still_page.wait_for_timeout(400)
    assert still_page.locator("[data-onion-skin]").count() == 1, (
        "the onion skin stopped rendering under a reduced-motion preference, "
        "though it is a diagram rather than a motion")


def test_page_documentation_three_columns_stay_in_agreement(page, site_base):
    module_slug, page_slug = ("timer", "timer-methods")
    page.goto(f"{site_base}{page_route(module_slug, page_slug)}",
              wait_until="load")

    assert page.locator("[data-version-control]").count() == 1, (
        "the version control is absent from a documentation route")
    assert page.locator("[data-search-field]").count() == 1, (
        "the search field is absent from a documentation route")
    tour = page.context.new_page()
    tour.goto(f"{site_base}{TOUR_ROUTE}", wait_until="load")
    assert tour.locator("[data-version-control]").count() == 0, (
        "the version control appears on a route that is not documentation")
    assert tour.locator("[data-search-field]").count() == 0, (
        "the search field appears on a route that is not documentation")
    tour.close()

    tree = page.locator("[data-tree-item]")
    assert tree.count() == MODULE_COUNT, (
        f"the tree lists {tree.count()} modules, expected {MODULE_COUNT}")
    expanded = page.eval_on_selector_all(
        "[data-tree-item]",
        "nodes => nodes.filter(n => n.getAttribute('data-tree-expanded') === 'true')"
        ".map(n => n.getAttribute('data-tree-item'))")
    assert expanded == [module_slug], (
        f"the expanded modules are {expanded}, expected only {module_slug!r}")

    current_panel = page.locator("[data-demo-panel][data-current='true']")
    assert current_panel.count() == 1, (
        f"{current_panel.count()} demo panels are current, expected one")
    assert current_panel.first.get_attribute("data-demo-panel") == \
        f"{module_slug}/{page_slug}", (
        "the current demo panel does not match the article being read")

    other = page.locator(f"[data-demo-panel='{module_slug}/timer-callbacks']")
    assert other.count() == 1, "the module's other panels are absent"
    other.first.click()
    page.wait_for_timeout(600)
    assert page.locator(
        "[data-demo-panel][data-current='true']").first.get_attribute(
        "data-demo-panel") == f"{module_slug}/timer-callbacks", (
        "activating a demo panel did not move the article to that page")


def test_page_demo_panel_outside_the_window_does_not_run(page, site_base):
    page.goto(f"{site_base}{page_route('timer', 'create-timer')}",
              wait_until="load")
    page.wait_for_timeout(600)
    states = page.eval_on_selector_all(
        "[data-demo-panel]",
        "nodes => nodes.map(n => [n.getAttribute('data-demo-panel'),"
        " n.getAttribute('data-demo-running'),"
        " n.getBoundingClientRect().top < window.innerHeight"
        " && n.getBoundingClientRect().bottom > 0])")
    assert states, "no demo panel is rendered"
    for name, running, visible in states:
        if not visible:
            assert running != "true", (
                f"demo panel {name} runs while it is outside the window")


def test_page_pager_names_its_destination_and_omits_the_edges(page, site_base):
    page.goto(f"{site_base}{page_route(*FIRST_PAGE)}", wait_until="load")
    assert page.locator("[data-pager='previous']").count() == 0, (
        "the first page of the first module carries a previous control")
    nxt = page.locator("[data-pager='next']")
    assert nxt.count() == 1, "the first page carries no next control"
    name = (nxt.first.get_attribute("aria-label") or "") + nxt.first.inner_text()
    assert PAGES[FIRST_PAGE[0]][1] in name.lower().replace(" ", "-"), (
        f"the next control names {name!r} rather than its destination page")

    page.goto(f"{site_base}{page_route(*LAST_MODULE_PAGE)}", wait_until="load")
    crossing = page.locator("[data-pager='next']")
    assert crossing.count() == 1, "the last page of a module carries no next control"
    label = (crossing.first.get_attribute("aria-label") or "") + \
        crossing.first.inner_text()
    assert FIRST_PAGE_OF_NEXT_MODULE[1] in label.lower().replace(" ", "-"), (
        f"the pager does not cross into {FIRST_PAGE_OF_NEXT_MODULE}: {label!r}")

    page.goto(f"{site_base}{page_route(*LAST_PAGE)}", wait_until="load")
    assert page.locator("[data-pager='next']").count() == 0, (
        "the last page of the last module carries a next control")
    assert IN_SECTION_HEADING in page.content(), (
        "the in-section heading is absent")
    for label in PAGER_LABELS:
        assert label in page.content() or label.title() in page.content(), (
            f"the pager label {label} is absent")


def test_page_search_is_driven_from_the_keyboard(page, site_base):
    page.goto(f"{site_base}{page_route('timer', 'create-timer')}",
              wait_until="load")
    field = page.locator("[data-search-field]")
    assert field.count() == 1, "the search field is absent from the header"
    field.first.click()
    field.first.type(CODE_ONLY_TERM)
    page.wait_for_timeout(800)

    results = page.locator("[data-search-result]")
    assert results.count() > 0, (
        f"searching {CODE_ONLY_TERM!r} returned nothing, so specimens are not "
        f"indexed")
    names = page.eval_on_selector_all(
        "[data-search-result]",
        "nodes => nodes.map(n => n.getAttribute('data-search-result'))")
    assert f"{CODE_ONLY_PAGE[0]}/{CODE_ONLY_PAGE[1]}" in names, (
        f"the results are {names}, missing {CODE_ONLY_PAGE}")

    page.keyboard.press("Enter")
    page.wait_for_timeout(800)
    assert CODE_ONLY_PAGE[1] in page.url, (
        f"the enter key did not open the highlighted result: {page.url}")

    page.goto(f"{site_base}{page_route('timer', 'create-timer')}",
              wait_until="load")
    page.locator("[data-search-field]").first.click()
    page.locator("[data-search-field]").first.type("zzzznotaword")
    page.wait_for_timeout(800)
    assert "No pages match that." in page.content(), (
        "an empty result set shows no message")


def test_page_editor_spring_has_no_handles_and_a_bezier_takes_the_keyboard(
        page, site_base):
    page.goto(f"{site_base}{EDITOR_ROUTE}", wait_until="load")
    tiles = page.locator("[data-preset-tile]")
    assert tiles.count() == MEMBER_COUNT, (
        f"the preset grid carries {tiles.count()} tiles, expected {MEMBER_COUNT}")

    families = {name.split("/")[0] for name in page.eval_on_selector_all(
        "[data-preset-tile]",
        "nodes => nodes.map(n => n.getAttribute('data-preset-tile'))")}
    assert families == set(FAMILIES), (
        f"the grid carries families {sorted(families)}, expected "
        f"{sorted(FAMILIES)}")
    assert len(families) == FAMILY_COUNT

    page.locator("[data-preset-tile='spring/bouncy']").first.click()
    page.wait_for_timeout(500)
    assert page.locator("[data-handle]").count() == 0, (
        "a spring curve carries draggable handles, which it has none of")
    assert page.locator("[data-onion-skin]").count() == 1, (
        "the onion skin is absent from the preview")

    page.locator("[data-preset-tile='bezier/in-out']").first.click()
    page.wait_for_timeout(500)
    handles = page.locator("[data-handle]")
    assert handles.count() == 2, (
        f"a bezier carries {handles.count()} handles, expected two")
    for index in range(2):
        handle = handles.nth(index)
        assert handle.get_attribute("role"), "a handle carries no role"
        assert handle.get_attribute("aria-valuenow") is not None, (
            "a handle carries no value")
        assert handle.get_attribute("aria-label"), (
            "a handle carries no name saying which control point it is")

    before = page.url
    handles.first.focus()
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(500)
    assert page.url != before, (
        "an arrow key did not move the focused handle")


def test_page_editor_address_is_replaced_and_reproduces_the_curve(
        page, site_base):
    page.goto(f"{site_base}{EDITOR_ROUTE}", wait_until="load")
    page.locator("[data-preset-tile='bezier/in-out']").first.click()
    page.wait_for_timeout(400)
    depth_before = page.evaluate("() => history.length")

    handle = page.locator("[data-handle]").first
    handle.focus()
    for _ in range(6):
        page.keyboard.press("ArrowRight")
    page.wait_for_timeout(600)

    depth_after = page.evaluate("() => history.length")
    assert depth_after - depth_before <= 1, (
        f"dragging a handle added {depth_after - depth_before} history entries; "
        f"the address is replaced rather than pushed")

    shared = page.url
    assert "?" in shared, (
        f"the editor holds no state in the address: {shared}")
    assert "#" not in shared, (
        f"the editor uses fragment addressing, which belongs to the tour "
        f"alone: {shared}")
    for key in POINT_KEYS:
        assert f"{key}=" in shared, (
            f"the address carries no {key} parameter: {shared}")
    exported = page.locator("[data-export-block='CSS/short']").first.inner_text()

    page.goto(shared, wait_until="load")
    page.wait_for_timeout(600)
    again = page.locator("[data-export-block='CSS/short']").first.inner_text()
    assert again == exported, (
        f"reopening the shared address produced {again!r} rather than "
        f"{exported!r}")

    for tab in EXPORT_TABS:
        assert page.locator(f"[data-export-block='{tab}/short']").count() == 1, (
            f"the {tab} tab carries no short export block")
        assert page.locator(f"[data-export-block='{tab}/full']").count() == 1, (
            f"the {tab} tab carries no full export block")

    page.goto(f"{site_base}{EDITOR_ROUTE}?family=not-a-family&member=nope",
              wait_until="load")
    page.wait_for_timeout(500)
    active = page.locator("[data-preset-active='true']")
    assert active.count() == 1, (
        "an invalid address did not fall back to the first family's default")


def test_page_copy_control_copies_the_source_and_shows_on_touch(
        page, narrow_page, site_base):
    page.goto(f"{site_base}{page_route('utilities', 'remap-and-clamp')}",
              wait_until="load")
    control = page.locator("[data-copy-control]").first
    assert control.count() == 1 or page.locator(
        "[data-copy-control]").count() >= 1, "no copy control is rendered"
    assert control.get_attribute("data-copy-state") == "idle", (
        "the copy control does not rest in its idle state")
    assert control.get_attribute("aria-label"), (
        "the copy control carries no accessible name")

    specimen = page.locator("[data-specimen]").first
    source = specimen.inner_text()
    assert CODE_ONLY_TERM in source, (
        f"the specimen on this page does not carry {CODE_ONLY_TERM!r}")
    assert "<span" not in source, (
        "the specimen renders highlight markup as text")

    control.click()
    page.wait_for_timeout(500)
    assert page.locator("[data-copy-control]").first.get_attribute(
        "data-copy-state") == "copied", (
        "the copy control does not confirm that it worked")
    assert COPY_CONFIRMATION in page.content(), (
        f"the confirmation {COPY_CONFIRMATION!r} is absent")

    narrow_page.goto(f"{site_base}{page_route('utilities', 'remap-and-clamp')}",
                     wait_until="load")
    narrow_page.wait_for_timeout(400)
    visible = narrow_page.locator("[data-copy-control]").first.is_visible()
    assert visible, (
        "the copy control is hidden on a touch device, where there is no "
        "pointer to reveal it")


def test_page_body_text_meets_the_contrast_bar(page, site_base):
    page.goto(f"{site_base}{page_route('timer', 'create-timer')}",
              wait_until="load")
    headings = page.locator("h1")
    assert headings.count() == 1, (
        f"the page carries {headings.count()} first-rank headings")

    sample = page.locator("article p").first
    colours = sample.evaluate(
        "node => { const s = getComputedStyle(node);"
        " return [s.color, getComputedStyle(document.body).backgroundColor]; }")
    ratio = contrast_ratio(parse_rgb(colours[0]), parse_rgb(colours[1]))
    assert ratio >= CONTRAST_BAR, (
        f"body text contrast is {ratio:.2f}, below the {CONTRAST_BAR} bar")

    tree_colour = page.locator("[data-tree-item]").first.evaluate(
        "node => getComputedStyle(node).color")
    tree_ratio = contrast_ratio(parse_rgb(tree_colour), parse_rgb(colours[1]))
    assert tree_ratio >= LARGE_TEXT_CONTRAST_BAR, (
        f"the documentation tree at rest sits at {tree_ratio:.2f}, below the "
        f"{LARGE_TEXT_CONTRAST_BAR} bar for an interface label")


def test_page_focus_ring_is_visible_and_the_skip_link_is_first(page, site_base):
    page.goto(f"{site_base}{TOUR_ROUTE}", wait_until="load")
    assert SKIP_LINK in page.content(), "the skip link is absent"
    first = page.evaluate(
        "() => { const e = document.querySelector('a, button');"
        " return e ? e.textContent.trim() : ''; }")
    assert SKIP_LINK in first, (
        f"the first focusable element is {first!r} rather than the skip link")

    page.keyboard.press("Tab")
    outline = page.evaluate(
        "() => { const e = document.activeElement;"
        " const s = getComputedStyle(e);"
        " return [e.tagName, s.outlineStyle, s.outlineWidth, s.boxShadow]; }")
    assert outline[0] != "BODY", "the first Tab reached no focusable element"
    assert outline[1] != "none" or outline[3] != "none", (
        f"the focused control carries no visible focus ring: {outline}")

    unlabelled = page.evaluate(
        "() => Array.from(document.querySelectorAll('button, a'))"
        ".filter(e => !e.textContent.trim() && !e.getAttribute('aria-label'))"
        ".map(e => e.outerHTML.slice(0, 80))")
    assert unlabelled == [], f"icon-only controls carry no name: {unlabelled}"


def test_page_narrow_viewport_pins_the_demo_panel_without_overflow(
        page, narrow_page, site_base):
    page.goto(f"{site_base}{page_route('timer', 'create-timer')}",
              wait_until="load")
    wide_columns = page.evaluate(
        "() => [document.querySelectorAll('[data-tree-item]').length > 0,"
        " document.querySelectorAll('[data-demo-panel]').length > 0,"
        " document.querySelectorAll('article').length > 0]")
    assert all(wide_columns), (
        f"the three columns are not all present at a wide width: {wide_columns}")

    narrow_page.goto(f"{site_base}{page_route('timer', 'create-timer')}",
                     wait_until="load")
    narrow_page.wait_for_timeout(500)
    overflow = narrow_page.evaluate(
        "() => document.documentElement.scrollWidth - "
        "document.documentElement.clientWidth")
    assert overflow <= 1, (
        f"the documentation overflows sideways by {overflow} at a narrow "
        f"viewport")

    pinned = narrow_page.locator("[data-demo-panel][data-current='true']")
    assert pinned.count() == 1, (
        "the current demonstration was dropped rather than pinned at a narrow "
        "viewport")
    assert pinned.first.is_visible(), (
        "the pinned demonstration is not visible at a narrow viewport")

    navigation = narrow_page.locator("nav a, nav button")
    assert navigation.count() > 0, "no navigation target is reachable when narrow"


def test_page_storage_bar_refuses_as_easily_as_it_accepts(page, site_base):
    page.goto(f"{site_base}{TOUR_ROUTE}", wait_until="load")
    bar = page.locator("[data-storage-bar]")
    assert bar.count() == 1, "a first-time visitor is not asked about storage"
    modal = bar.first.evaluate(
        "node => node.getAttribute('role') === 'dialog'"
        " || node.tagName === 'DIALOG'")
    assert not modal, "the storage bar is a modal"

    accept = page.locator("[data-storage-accept]")
    refuse = page.locator("[data-storage-refuse]")
    assert accept.count() == 1 and refuse.count() == 1, (
        "the storage bar does not offer both answers")
    sizes = page.evaluate(
        "() => { const a = document.querySelector('[data-storage-accept]');"
        " const r = document.querySelector('[data-storage-refuse]');"
        " const ab = a.getBoundingClientRect(); const rb = r.getBoundingClientRect();"
        " return [ab.width * ab.height, rb.width * rb.height]; }")
    assert min(sizes) / max(sizes) > 0.5, (
        f"refusing is harder to reach than accepting: areas {sizes}")

    refuse.first.click()
    page.wait_for_timeout(400)
    page.reload(wait_until="load")
    page.wait_for_timeout(400)
    assert page.locator("[data-storage-bar]").count() == 0, (
        "the storage answer did not survive a reload")


def test_page_sponsor_wall_ends_every_tier_with_the_recruitment_card(
        page, site_base):
    page.goto(f"{site_base}{DOCS_ROUTE}", wait_until="load")
    content = page.content()
    for heading in TIER_HEADINGS:
        assert heading in content, f"the tier heading {heading!r} is absent"
    assert RECRUITMENT_LABEL in content, "the recruitment card is absent"

    cards = page.eval_on_selector_all(
        "[data-sponsor-card]",
        "nodes => nodes.map(n => n.getAttribute('data-sponsor-card'))")
    assert SPONSOR_WITHOUT_MARK in cards, (
        f"{SPONSOR_WITHOUT_MARK} is absent from the wall")
    assert SPONSOR_LAPSED not in cards, (
        f"the lapsed sponsor {SPONSOR_LAPSED} is still shown")

    without_mark = page.locator(f"[data-sponsor-card='{SPONSOR_WITHOUT_MARK}']")
    assert SPONSORS[SPONSOR_WITHOUT_MARK][0] in without_mark.first.inner_text(), (
        "a sponsor with no mark does not render its name in place of one")
    broken = page.evaluate(
        "() => Array.from(document.images).filter(i => i.complete"
        " && i.naturalWidth === 0).map(i => i.currentSrc)")
    assert broken == [], f"the wall renders broken images: {broken}"

    recruitment = page.locator("[data-recruitment-card]")
    assert recruitment.count() == len(TIER_HEADINGS), (
        f"{recruitment.count()} recruitment cards are shown, expected one per "
        f"tier")


def test_page_no_binary_asset_is_fetched_at_run_time(page, site_base):
    page.goto(f"{site_base}{TOUR_ROUTE}", wait_until="load")
    page.wait_for_timeout(800)
    fetched = page.evaluate(
        "() => performance.getEntriesByType('resource').map(r => r.name)")
    binaries = [name for name in fetched
                if name.lower().split("?", 1)[0].endswith(BINARY_ASSET_SUFFIXES)]
    assert binaries == [], (
        f"the build fetched binary assets at run time: {binaries}")

    fonts = page.evaluate("() => document.fonts.size")
    assert fonts == 0, (
        f"{fonts} font faces were loaded, and this build ships no font binary")

    icons = page.evaluate(
        "() => document.querySelectorAll('svg').length")
    assert icons > 0, "no icon is drawn as geometry"


def test_page_learn_form_works_without_scripting(site_base, store):
    response = fetch(site_base, LEARN_ROUTE, follow_redirects=True)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = response.text
    assert WAITLIST_LABEL in body, "the waiting-list label is absent"
    assert SUBMIT_LABEL in body, "the submit control is absent"
    assert FALLBACK_LINE in body, "the fallback address line is absent"
    assert 'method="post"' in body.lower(), (
        "the subscription form does not post, so it needs script to work")
    assert '/api/subscribe' in body, (
        "the form does not post to the app's own endpoint")
    assert HONEYPOT_FIELD in body, "the decoy field is absent from the form"
    assert 'enctype="multipart' not in body.lower(), (
        "the form is not form-encoded")
    assert store.count("subscriber") > 0, (
        "the seeded subscribers must live in PostgreSQL")
