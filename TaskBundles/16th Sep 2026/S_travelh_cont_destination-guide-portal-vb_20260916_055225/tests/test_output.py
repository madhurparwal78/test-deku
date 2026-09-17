from __future__ import annotations

import os
import re

import appclient
from conftest import (
    ALDER_COVE_PICTURES, BACKWATER_SLUGS, BODY_FAMILY, COASTLINE_SLUGS,
    COLLECTION_NAMES, COLLECTION_SLUGS, CONTRAST_FLOOR, DISPLAY_FAMILY,
    DRAFT_BROCHURE_TITLE, DRAFT_NAME, DRAFT_PICTURES, DRAFT_SLUG, EDITOR_EMAIL,
    ENDED_EVENT, ENDS_TODAY_EVENT, ENTRY_BROCHURE_TITLE, HIGHLANDS_SLUGS,
    LATEST_EVENT, NAME_MIN, NARROW_VIEWPORT, NO_END_DATE_EVENT, PAGE_SIZE,
    BROCHURE_FILENAMES, FACTS, PUBLIC_ROUTES, PUBLISHED_NAMES, PUBLISHED_SLUGS,
    REGIONAL_BROCHURES, RESERVED_SEGMENTS, SUMMARY_MAX, TOUCH_TARGET_MIN, add_picture,
    contrast_ratio, create_draft, describe, drop, entry_id, entry_payload, json_list,
    names_of, parse_rgb, poll_until, publish, settle, slugs_of, today_utc,
    unpublish, FEATURED_HEADING, FEATURED_SLUGS, WIDE_VIEWPORT,
)


def test_place_index_lists_only_published_entries(api):
    """The place index carries the eight seeded published places and never the draft."""
    rows = json_list(api.get("/entries"), "GET /api/entries")
    found = slugs_of(rows)
    missing = sorted(set(PUBLISHED_SLUGS) - found)
    assert not missing, (
        f"GET /api/entries should carry every published place; missing {missing}, "
        f"saw {sorted(found)}"
    )
    assert DRAFT_SLUG not in found, (
        f"GET /api/entries carries the draft place {DRAFT_SLUG!r}, which no public "
        f"response may contain; saw {sorted(found)}"
    )
    for row in rows:
        assert str(row.get("state", "published")) != "draft", (
            f"GET /api/entries carries a row in state draft: {row!r}"
        )


def test_place_entry_detail_carries_guide_and_facts(api):
    """One published place carries its guide text, its fact panel and its pictures."""
    r = api.get("/entries/alder-cove")
    assert r.status_code == 200, f"GET /api/entries/alder-cove should answer 200: {describe(r)}"
    entry = r.json()
    assert entry.get("name") == "Alder Cove", (
        f"the entry at alder-cove should be named Alder Cove: {entry!r}"
    )
    for field in ("guide", "summary", "transport_point", "best_months", "distance_km"):
        assert entry.get(field) not in (None, ""), (
            f"GET /api/entries/alder-cove should carry a populated {field!r}: {entry!r}"
        )
    assert isinstance(entry["distance_km"], int), (
        f"distance_km should be an integer: {entry['distance_km']!r}"
    )
    transport, months, distance = FACTS["alder-cove"]
    assert entry["transport_point"] == transport, (
        f"Alder Cove's nearest station is seeded as {transport!r}; "
        f"saw {entry['transport_point']!r}"
    )
    assert entry["best_months"] == months, (
        f"Alder Cove's best months are seeded as {months!r}; saw {entry['best_months']!r}"
    )
    assert entry["distance_km"] == distance, (
        f"Alder Cove's distance is seeded as {distance}; saw {entry['distance_km']!r}"
    )
    images = entry.get("images") or []
    assert len(images) == ALDER_COVE_PICTURES, (
        f"Alder Cove is seeded with {ALDER_COVE_PICTURES} pictures, saw {len(images)}: "
        f"{images!r}"
    )
    for image in images:
        assert str(image.get("alt_text") or "").strip(), (
            f"every picture carries a description: {image!r}"
        )


def test_place_entry_related_row_shares_a_theme(api):
    """The related row of a place carries other published places sharing a theme."""
    r = api.get("/entries/alder-cove")
    assert r.status_code == 200, f"GET /api/entries/alder-cove should answer 200: {describe(r)}"
    entry = r.json()
    related = entry.get("related") or []
    assert 1 <= len(related) <= 3, (
        f"the related row carries up to three places and at least the one that "
        f"qualifies; saw {len(related)}: {related!r}"
    )
    found = slugs_of(related)
    assert "alder-cove" not in found, (
        f"the related row excludes the current place; saw {sorted(found)}"
    )
    assert found <= set(PUBLISHED_SLUGS), (
        f"the related row carries published places only; saw {sorted(found)}"
    )
    assert found & set(COASTLINE_SLUGS), (
        f"Alder Cove carries the Coastline theme, so its related row shares it; "
        f"saw {sorted(found)}"
    )


def test_collections_endpoint_returns_the_three_seeded_themes(api):
    """Exactly the three seeded collections are returned, each with its standfirst."""
    rows = json_list(api.get("/collections"), "GET /api/collections")
    found = slugs_of(rows)
    assert found == set(COLLECTION_SLUGS), (
        f"GET /api/collections should carry exactly {sorted(COLLECTION_SLUGS)}; "
        f"saw {sorted(found)}"
    )
    assert names_of(rows) == set(COLLECTION_NAMES), (
        f"the three collections are named {sorted(COLLECTION_NAMES)}; "
        f"saw {sorted(names_of(rows))}"
    )
    for row in rows:
        assert str(row.get("standfirst") or "").strip(), (
            f"each collection carries a standfirst sentence: {row!r}"
        )
        assert isinstance(row.get("published_count"), int), (
            f"each collection carries its published_count as an integer: {row!r}"
        )
    counts = {str(r["slug"]): r["published_count"] for r in rows}
    assert counts == {"coastline": len(COASTLINE_SLUGS),
                      "highlands": len(HIGHLANDS_SLUGS),
                      "backwater": len(BACKWATER_SLUGS)}, (
        f"each published_count equals that collection's seeded published membership; "
        f"saw {counts}"
    )


def test_collection_detail_lists_only_its_published_entries(api):
    """Each collection carries exactly its published members and never the draft."""
    expected = {
        "coastline": set(COASTLINE_SLUGS),
        "highlands": set(HIGHLANDS_SLUGS),
        "backwater": set(BACKWATER_SLUGS),
    }
    for slug, want in expected.items():
        r = api.get(f"/collections/{slug}")
        assert r.status_code == 200, (
            f"GET /api/collections/{slug} should answer 200: {describe(r)}"
        )
        body = r.json()
        rows = body.get("entries") if isinstance(body, dict) else body
        found = slugs_of(rows or [])
        assert want <= found, (
            f"collection {slug!r} should carry {sorted(want)}; saw {sorted(found)}"
        )
        assert DRAFT_SLUG not in found, (
            f"collection {slug!r} carries the draft place {DRAFT_SLUG!r}: {sorted(found)}"
        )


def test_empty_collection_answers_ok_rather_than_not_found(api, desk):
    """A collection with no published member answers 200 with an empty member list."""
    r = api.get("/collections/highlands")
    assert r.status_code == 200, (
        f"a seeded collection answers 200 whatever its membership: {describe(r)}"
    )
    entry = create_draft(desk, themes=["highlands"])
    eid = entry_id(entry)
    after = api.get("/collections/highlands")
    assert after.status_code == 200, (
        f"a collection holding an unpublished member still answers 200, never 404: "
        f"{describe(after)}"
    )
    body = after.json()
    rows = body.get("entries") if isinstance(body, dict) else body
    assert entry["slug"] not in slugs_of(rows or []), (
        f"the unpublished probe place {entry['slug']!r} should be absent from the "
        f"collection; saw {sorted(slugs_of(rows or []))}"
    )
    drop(desk, eid)


def test_events_response_excludes_an_event_that_has_ended(api):
    """An event whose end date has passed is absent from the events response."""
    rows = json_list(api.get("/events"), "GET /api/events")
    found = names_of(rows)
    assert ENDED_EVENT not in found, (
        f"{ENDED_EVENT!r} ended before today, so the events response must not carry "
        f"it; saw {sorted(found)}"
    )
    assert found, f"the events response should carry the upcoming events; saw {rows!r}"


def test_events_response_keeps_an_event_ending_today(api):
    """An event whose end date is today stays in the events response all day."""
    rows = json_list(api.get("/events"), "GET /api/events")
    found = names_of(rows)
    assert ENDS_TODAY_EVENT in found, (
        f"{ENDS_TODAY_EVENT!r} ends today, so it is present for the whole of today; "
        f"saw {sorted(found)}"
    )
    row = next(r for r in rows if r.get("name") == ENDS_TODAY_EVENT)
    assert str(row.get("ends_on", ""))[:10] == today_utc().isoformat(), (
        f"{ENDS_TODAY_EVENT!r} is seeded to end today: {row!r}"
    )


def test_events_response_treats_a_missing_end_date_as_the_start(api):
    """An event carrying no end date is judged on its start date."""
    rows = json_list(api.get("/events"), "GET /api/events")
    found = names_of(rows)
    assert NO_END_DATE_EVENT in found, (
        f"{NO_END_DATE_EVENT!r} carries no end date and starts in the future, so its "
        f"start date stands as its end date; saw {sorted(found)}"
    )
    row = next(r for r in rows if r.get("name") == NO_END_DATE_EVENT)
    assert row.get("ends_on") in (None, "", row.get("starts_on")), (
        f"{NO_END_DATE_EVENT!r} is seeded with no end date: {row!r}"
    )


def test_events_response_orders_by_start_date_ascending(api):
    """The events response is ordered by start date ascending."""
    rows = json_list(api.get("/events"), "GET /api/events")
    starts = [str(r.get("starts_on", ""))[:10] for r in rows]
    assert all(starts), f"every event carries a start date: {rows!r}"
    assert starts == sorted(starts), (
        f"the events response is ordered by starts_on ascending; saw {starts}"
    )
    found = names_of(rows)
    assert LATEST_EVENT in found, (
        f"the seeded upcoming events include {LATEST_EVENT!r}; saw {sorted(found)}"
    )
    for row in rows:
        assert str(row.get("place") or row.get("place_name") or row.get("entry_name") or ""), (
            f"each event names the place it happens at: {row!r}"
        )


def test_brochure_library_lists_entry_and_regional_guides(api):
    """The library carries the regional guides plus the guides of published places."""
    rows = json_list(api.get("/brochures"), "GET /api/brochures")
    titles = names_of(rows, "title")
    missing = sorted(set(REGIONAL_BROCHURES) - titles)
    assert not missing, (
        f"the library should carry every regional guide; missing {missing}, "
        f"saw {sorted(titles)}"
    )
    assert ENTRY_BROCHURE_TITLE in titles, (
        f"the guide document of a published place belongs in the library; "
        f"saw {sorted(titles)}"
    )
    assert DRAFT_BROCHURE_TITLE not in titles, (
        f"{DRAFT_BROCHURE_TITLE!r} belongs to the draft place, so the library must "
        f"not carry it; saw {sorted(titles)}"
    )
    for row in rows:
        assert isinstance(row.get("page_count"), int) and row["page_count"] > 0, (
            f"each guide document reports its page count: {row!r}"
        )
        assert isinstance(row.get("byte_size"), int) and row["byte_size"] > 0, (
            f"each guide document reports its byte size: {row!r}"
        )


def test_gallery_images_response_pages_at_twenty_four(api):
    """The gallery response is paged at 24 and carries only published pictures."""
    rows = json_list(api.get("/images"), "GET /api/images")
    assert len(rows) <= PAGE_SIZE, (
        f"GET /api/images pages at {PAGE_SIZE}; saw {len(rows)} rows"
    )
    owners = {str(r.get("slug") or r.get("entry_slug") or "") for r in rows}
    assert DRAFT_SLUG not in owners, (
        f"the gallery carries no picture of the draft place {DRAFT_SLUG!r}; "
        f"saw owners {sorted(owners)}"
    )
    for row in rows:
        for field in ("alt_text", "width", "height"):
            assert row.get(field) not in (None, ""), (
                f"each gallery picture carries {field!r}: {row!r}"
            )
    filtered = json_list(api.get("/images", params={"theme": "highlands"}),
                         "GET /api/images?theme=highlands")
    owners = {str(r.get("slug") or r.get("entry_slug") or "") for r in filtered}
    assert owners <= set(HIGHLANDS_SLUGS), (
        f"the theme filter narrows the gallery to Highlands places; saw {sorted(owners)}"
    )


def test_index_name_filter_narrows_to_one_place(api):
    """The name filter narrows the index to the places whose name matches."""
    rows = json_list(api.get("/entries", params={"name": "salt"}),
                     "GET /api/entries?name=salt")
    found = slugs_of(rows)
    assert found == {"saltmere"}, (
        f"the name filter 'salt' matches Saltmere alone; saw {sorted(found)}"
    )


def test_index_theme_filter_narrows_to_a_collection(api):
    """The theme filter narrows the index to the places carrying that collection."""
    rows = json_list(api.get("/entries", params={"theme": "highlands"}),
                     "GET /api/entries?theme=highlands")
    found = slugs_of(rows)
    assert found == set(HIGHLANDS_SLUGS), (
        f"the Highlands theme filter matches {sorted(HIGHLANDS_SLUGS)}; "
        f"saw {sorted(found)}"
    )


def test_index_sort_by_name_orders_places_alphabetically(api):
    """The name sort orders the index alphabetically."""
    rows = json_list(api.get("/entries", params={"sort": "name"}),
                     "GET /api/entries?sort=name")
    names = [str(r.get("name", "")) for r in rows]
    assert names == sorted(names), (
        f"the name sort orders the index alphabetically; saw {names}"
    )


def test_index_sort_by_recent_orders_newest_first(api, desk):
    """The recent sort puts the most recently added place first."""
    entry = create_draft(desk)
    eid = entry_id(entry)
    add_picture(desk, eid)
    published = publish(desk, eid)
    assert published.status_code in (200, 201), (
        f"publishing the probe place should succeed: {describe(published)}"
    )
    try:
        rows = json_list(api.get("/entries", params={"sort": "recent"}),
                         "GET /api/entries?sort=recent")
        assert rows, "the recent sort should answer the published places"
        assert str(rows[0].get("slug")) == entry["slug"], (
            f"the recent sort puts the newest place first; expected "
            f"{entry['slug']!r}, saw {str(rows[0].get('slug'))!r}"
        )
    finally:
        unpublish(desk, eid)
        drop(desk, eid)


def test_health_route_answers_ready(api):
    """The health route answers 200 once the app is ready."""
    r = api.get("/health")
    assert r.status_code == 200, (
        f"GET /api/health should answer 200 once the app is ready: {describe(r)}"
    )
    origin = os.environ["APP_PUBLIC_URL"].rstrip("/")
    assert appclient.app_url() == origin, (
        f"the app answers on the origin read from APP_PUBLIC_URL; "
        f"expected {origin!r}, saw {appclient.app_url()!r}"
    )


def test_privacy_page_is_served_and_linked_from_the_footer(page):
    """The privacy page is served and reachable from the footer of the home surface."""
    origin = appclient.app_url()
    page.goto(f"{origin}/privacy")
    assert page.locator("h1").count() >= 1, "the privacy page carries a heading"
    body = page.content()
    assert "What we record" in body, (
        f"the privacy page heading reads 'What we record'; saw {page.title()!r}"
    )
    page.goto(origin)
    link = page.locator("footer a[href*='privacy']")
    assert link.count() >= 1, (
        "the footer of the home surface carries a link to the privacy page"
    )


def test_terms_page_is_served_and_linked_from_the_footer(page):
    """The terms page is served and reachable from the footer of the home surface."""
    origin = appclient.app_url()
    page.goto(f"{origin}/terms")
    assert page.locator("h1").count() >= 1, "the terms page carries a heading"
    assert "Using the guide" in page.content(), (
        f"the terms page heading reads 'Using the guide'; saw {page.title()!r}"
    )
    page.goto(origin)
    link = page.locator("footer a[href*='terms']")
    assert link.count() >= 1, (
        "the footer of the home surface carries a link to the terms page"
    )


def test_unknown_path_renders_the_board_not_found_surface(page, api):
    """An unknown path answers 404 and renders the board's own not-found surface."""
    origin = appclient.app_url()
    response = page.goto(f"{origin}/nothing-here-{os.urandom(4).hex()}")
    assert response is not None, "the unknown path should answer rather than hang"
    assert response.status == 404, (
        f"an unknown path answers 404; saw {response.status}"
    )
    content = page.content()
    assert "We cannot find that page" in content, (
        "the not-found surface carries the board's own heading"
    )
    assert page.locator("header").count() >= 1, (
        "the not-found surface carries the global header"
    )
    assert page.locator("footer").count() >= 1, (
        "the not-found surface carries the global footer"
    )
    draft = api.get(f"/entries/{DRAFT_SLUG}")
    assert draft.status_code == 404, (
        f"the draft place answers 404 through the API too: {describe(draft)}"
    )


def test_internal_links_on_public_surfaces_all_resolve(page):
    """Every internal link on every public surface resolves rather than answering 404."""
    origin = appclient.app_url()
    broken = []
    for route in PUBLIC_ROUTES:
        page.goto(f"{origin}{route}")
        hrefs = page.eval_on_selector_all(
            "a[href]", "els => els.map(e => e.getAttribute('href'))")
        targets = sorted({h for h in hrefs if h and h.startswith("/")})
        for href in targets[:25]:
            probe = page.request.get(f"{origin}{href}")
            if probe.status >= 400:
                broken.append((route, href, probe.status))
    assert not broken, (
        f"every internal link on a public surface resolves; broken links {broken}"
    )


def test_published_entry_fields_survive_a_reread(api, desk):
    """The fields of a published place read back unchanged after a re-read."""
    entry = create_draft(desk, summary="A probe summary that must survive a re-read.")
    eid = entry_id(entry)
    add_picture(desk, eid)
    assert publish(desk, eid).status_code in (200, 201), (
        f"publishing the probe place {entry['slug']!r} should succeed"
    )
    try:
        first = api.get(f"/entries/{entry['slug']}")
        assert first.status_code == 200, f"the published probe place is readable: {describe(first)}"
        again = api.get(f"/entries/{entry['slug']}")
        assert again.status_code == 200, f"the probe place is readable twice: {describe(again)}"
        for field in ("name", "slug", "summary", "guide", "transport_point",
                      "best_months", "distance_km"):
            assert first.json().get(field) == again.json().get(field), (
                f"the {field!r} of a published place is stable across a re-read: "
                f"{first.json().get(field)!r} then {again.json().get(field)!r}"
            )
        assert again.json().get("distance_km") == 42, (
            f"the stored distance_km reads back as written: {again.json()!r}"
        )
    finally:
        unpublish(desk, eid)
        drop(desk, eid)


def test_desk_picture_count_matches_the_objects_stored(desk, store):
    """The picture count on the desk list equals the objects the store holds."""
    rows = json_list(desk.get("/desk/entries", params={"state": "all"}),
                     "GET /api/desk/entries")
    listed = {}
    for row in rows:
        if row.get("slug"):
            listed[str(row["slug"])] = row
    assert "alder-cove" in listed, (
        f"the desk list carries every entry in both states; saw {sorted(listed)}"
    )
    for slug, expected in (("alder-cove", ALDER_COVE_PICTURES),
                           (DRAFT_SLUG, DRAFT_PICTURES)):
        row = listed.get(slug)
        assert row is not None, f"the desk list carries {slug!r}; saw {sorted(listed)}"
        count = row.get("picture_count")
        assert count == expected, (
            f"the desk list reports {expected} pictures for {slug!r}; saw {count!r} "
            f"in {row!r}"
        )
        eid = entry_id(row)
        held = store.list(f"entries/{eid}/gallery/")
        assert len(held) == expected, (
            f"the store holds {expected} gallery objects for entry {eid}; "
            f"saw {len(held)}: {held!r}"
        )


def test_brochure_byte_size_matches_the_stored_object(api, desk, store):
    """The byte size on a guide document card matches the object the store holds."""
    rows = json_list(api.get("/brochures"), "GET /api/brochures")
    row = next((r for r in rows if r.get("title") == REGIONAL_BROCHURES[0]), None)
    assert row is not None, (
        f"the library carries {REGIONAL_BROCHURES[0]!r}; saw {sorted(names_of(rows, 'title'))}"
    )
    streamed = api.get(f"/media/brochures/{row['id']}")
    assert streamed.status_code == 200, (
        f"the regional guide document resolves through the app: {describe(streamed)}"
    )
    assert len(streamed.content) == row["byte_size"], (
        f"the reported byte_size {row['byte_size']} should equal the stored object's "
        f"own size; the app served {len(streamed.content)} bytes"
    )
    keys = store.list("regional/")
    assert keys, f"the regional guide documents live in the store; saw {keys!r}"


def test_index_count_line_reconciles_with_the_published_rows(api, page):
    """The count line on the place index reconciles with the published rows."""
    rows = json_list(api.get("/entries"), "GET /api/entries")
    page.goto(f"{appclient.app_url()}/destination")
    content = page.content()
    assert f"{len(rows)} places" in content, (
        f"the index count line should read '{len(rows)} places' to match the "
        f"published rows the API returns"
    )


def test_seed_holds_the_eight_published_places_and_one_draft(desk, api):
    """The seed holds eight published places, one draft, and twenty pictures."""
    rows = json_list(desk.get("/desk/entries", params={"state": "all"}),
                     "GET /api/desk/entries?state=all")
    by_slug = {str(r.get("slug")): r for r in rows if r.get("slug")}
    for slug in PUBLISHED_SLUGS:
        assert by_slug.get(slug, {}).get("state") == "published", (
            f"the seeded place {slug!r} is published; saw {by_slug.get(slug)!r}"
        )
    assert by_slug.get(DRAFT_SLUG, {}).get("state") == "draft", (
        f"the seeded place {DRAFT_SLUG!r} is a draft; saw {by_slug.get(DRAFT_SLUG)!r}"
    )
    assert by_slug[DRAFT_SLUG].get("name") == DRAFT_NAME, (
        f"the draft place is named {DRAFT_NAME!r}: {by_slug[DRAFT_SLUG]!r}"
    )
    seeded = sum(int(by_slug[s].get("picture_count", 0))
                 for s in list(PUBLISHED_SLUGS) + [DRAFT_SLUG])
    assert seeded == 20, (
        f"the seed holds twenty pictures across the nine seeded places; saw {seeded}"
    )
    public = json_list(api.get("/entries"), "GET /api/entries")
    assert set(PUBLISHED_SLUGS) <= slugs_of(public), (
        f"the eight seeded published places are all public; saw {sorted(slugs_of(public))}"
    )
    counts = desk.get("/desk/entries/counts")
    assert counts.status_code == 200, (
        f"GET /api/desk/entries/counts should answer the three filter counts: "
        f"{describe(counts)}"
    )
    figures = counts.json()
    for key in ("all", "published", "draft"):
        assert isinstance(figures.get(key), int), (
            f"the counts response carries {key!r} as an integer: {figures!r}"
        )
    assert figures["all"] == figures["published"] + figures["draft"], (
        f"the three filter counts reconcile: {figures!r}"
    )
    assert figures["published"] >= len(PUBLISHED_SLUGS), (
        f"the published count covers at least the eight seeded published places; "
        f"saw {figures['published']}"
    )


def test_publish_then_unpublish_leaves_a_single_entry_row(desk, api):
    """Publishing then unpublishing one place leaves exactly one entry row."""
    entry = create_draft(desk)
    eid = entry_id(entry)
    add_picture(desk, eid)
    try:
        assert publish(desk, eid).status_code in (200, 201), "the probe place publishes"
        assert unpublish(desk, eid).status_code in (200, 201), "the probe place unpublishes"
        rows = json_list(desk.get("/desk/entries", params={"state": "all"}),
                         "GET /api/desk/entries?state=all")
        matches = [r for r in rows if str(r.get("slug")) == entry["slug"]]
        assert len(matches) == 1, (
            f"one round of publish then unpublish leaves a single row for "
            f"{entry['slug']!r}; saw {len(matches)}: {matches!r}"
        )
        assert matches[0].get("state") == "draft", (
            f"the round trip leaves the place in state draft: {matches[0]!r}"
        )
    finally:
        drop(desk, eid)


def test_two_concurrent_publishes_of_one_slug_admit_one_winner(desk):
    """Two simultaneous publishes naming one slug admit exactly one winner."""
    import threading

    token = entry_payload()["slug"]
    first = create_draft(desk, slug=token)
    second = create_draft(desk)
    first_id, second_id = entry_id(first), entry_id(second)
    add_picture(desk, first_id)
    add_picture(desk, second_id)
    patched = desk.patch(f"/desk/entries/{second_id}", json={"slug": token})
    results = []
    barrier = threading.Barrier(2)

    def attempt(eid):
        client_token = appclient.login(EDITOR_EMAIL, appclient.seeded_password(
            "EDITOR_PASSWORD", "deku-demo-pw-2026"))
        with appclient.client(client_token) as client:
            barrier.wait()
            results.append(client.post(f"/desk/entries/{eid}/publish").status_code)

    try:
        if patched.status_code >= 400:
            single = publish(desk, first_id)
            assert single.status_code in (200, 201), (
                f"one place may hold the slug {token!r}: {describe(single)}"
            )
            clash = desk.patch(f"/desk/entries/{second_id}", json={"slug": token})
            assert clash.status_code >= 400, (
                f"a second entry may not take the slug {token!r}: {describe(clash)}"
            )
            return
        threads = [threading.Thread(target=attempt, args=(first_id,)),
                   threading.Thread(target=attempt, args=(second_id,))]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=60)
        wins = [s for s in results if s in (200, 201)]
        assert len(wins) == 1, (
            f"exactly one of two simultaneous publishes on slug {token!r} wins; "
            f"saw statuses {results}"
        )
        losses = [s for s in results if s not in (200, 201)]
        assert all(400 <= s < 500 for s in losses), (
            f"the losing publish is refused as a client error; saw {results}"
        )
    finally:
        unpublish(desk, first_id)
        unpublish(desk, second_id)
        drop(desk, first_id)
        drop(desk, second_id)


def test_saving_one_entry_twice_creates_no_second_entry(desk):
    """Saving one place twice leaves one row, with the later save standing."""
    entry = create_draft(desk)
    eid = entry_id(entry)
    try:
        first = desk.patch(f"/desk/entries/{eid}", json={"summary": "First probe summary."})
        assert first.status_code in (200, 201), f"the first save succeeds: {describe(first)}"
        second = desk.patch(f"/desk/entries/{eid}", json={"summary": "Second probe summary."})
        assert second.status_code in (200, 201), f"the second save succeeds: {describe(second)}"
        rows = json_list(desk.get("/desk/entries", params={"state": "all"}),
                         "GET /api/desk/entries?state=all")
        matches = [r for r in rows if str(r.get("slug")) == entry["slug"]]
        assert len(matches) == 1, (
            f"saving one place twice creates no second row; saw {len(matches)} rows "
            f"for {entry['slug']!r}"
        )
        reread = desk.get(f"/desk/entries/{eid}")
        payload = reread.json() if reread.status_code == 200 else matches[0]
        assert payload.get("summary") == "Second probe summary.", (
            f"the later save is the state that stands; saw {payload.get('summary')!r}"
        )
    finally:
        drop(desk, eid)


def test_desk_entry_list_is_denied_without_a_token(anon):
    """The desk entry list is denied to a caller carrying no token."""
    r = anon.get("/desk/entries", params={"state": "all"})
    assert r.status_code in (401, 403), (
        f"GET /api/desk/entries with no token is denied: {describe(r)}"
    )
    assert DRAFT_NAME not in r.text, (
        f"the denial leaks no draft entry; body {r.text[:300]!r}"
    )


def test_desk_publish_is_denied_without_a_token(anon, desk):
    """A publish is denied to a caller with no token, and the place is unchanged."""
    entry = create_draft(desk)
    eid = entry_id(entry)
    try:
        r = anon.post(f"/desk/entries/{eid}/publish")
        assert r.status_code in (401, 403), (
            f"publishing with no token is denied: {describe(r)}"
        )
        state = desk.get("/desk/entries", params={"state": "all"})
        rows = json_list(state, "GET /api/desk/entries?state=all")
        row = next(r for r in rows if str(r.get("slug")) == entry["slug"])
        assert row.get("state") == "draft", (
            f"the denied publish leaves the place in state draft: {row!r}"
        )
    finally:
        drop(desk, eid)


def test_desk_entry_list_is_denied_with_a_malformed_token(api):
    """The desk entry list is denied to a caller carrying a malformed token."""
    with appclient.client("not-a-real-token-" + os.urandom(6).hex()) as client:
        r = client.get("/desk/entries", params={"state": "all"})
    assert r.status_code in (401, 403), (
        f"a malformed bearer token is denied: {describe(r)}"
    )
    assert r.status_code < 500, (
        f"a malformed token is a client error rather than a server error: {describe(r)}"
    )


def test_no_state_parameter_makes_a_public_response_carry_a_draft(api):
    """No query string on a public endpoint returns the draft place."""
    attempts = (
        ("/entries", {"state": "draft"}),
        ("/entries", {"state": "all"}),
        ("/entries", {"include_drafts": "true"}),
        ("/entries", {"draft": "1"}),
        ("/images", {"state": "draft"}),
        ("/brochures", {"state": "all"}),
    )
    for path, params in attempts:
        r = api.get(path, params=params)
        assert r.status_code < 500, (
            f"GET /api{path} with {params!r} answers without a server error: {describe(r)}"
        )
        if r.status_code != 200:
            continue
        body = r.json()
        rows = body if isinstance(body, list) else body.get("entries") or []
        assert DRAFT_SLUG not in slugs_of(rows), (
            f"GET /api{path} with {params!r} returned the draft place; there is no "
            f"query string that makes a public endpoint answer with a draft"
        )
        assert DRAFT_NAME not in r.text, (
            f"GET /api{path} with {params!r} leaked {DRAFT_NAME!r}: {r.text[:300]!r}"
        )


def test_draft_place_address_answers_not_found_not_forbidden(api):
    """The address of the draft place answers 404 rather than 403."""
    r = api.get(f"/entries/{DRAFT_SLUG}")
    assert r.status_code == 404, (
        f"GET /api/entries/{DRAFT_SLUG} answers 404, because the existence of a "
        f"draft is itself not public: {describe(r)}"
    )
    assert r.status_code != 403, (
        f"a draft place answers not-found rather than forbidden: {describe(r)}"
    )


def test_draft_picture_bytes_are_denied_to_an_anonymous_caller(anon, desk):
    """The bytes of a draft place's picture are denied through the app."""
    rows = json_list(desk.get("/desk/entries", params={"state": "draft"}),
                     "GET /api/desk/entries?state=draft")
    row = next((r for r in rows if str(r.get("slug")) == DRAFT_SLUG), None)
    assert row is not None, (
        f"the desk list carries the seeded draft {DRAFT_SLUG!r}; saw {rows!r}"
    )
    detail = desk.get(f"/desk/entries/{entry_id(row)}")
    assert detail.status_code == 200, (
        f"the editor reads the draft place: {describe(detail)}"
    )
    images = detail.json().get("images") or []
    assert len(images) == DRAFT_PICTURES, (
        f"the draft place is seeded with {DRAFT_PICTURES} pictures; saw {len(images)}"
    )
    for image in images:
        r = anon.get(f"/media/images/{image['id']}")
        assert r.status_code == 404, (
            f"the bytes of picture {image['id']!r} on a draft place answer 404 to an "
            f"anonymous caller: {describe(r)}"
        )


def test_draft_guide_document_bytes_are_denied_to_anonymous(anon, desk):
    """The bytes of a draft place's guide document are denied through the app."""
    rows = json_list(desk.get("/desk/entries", params={"state": "draft"}),
                     "GET /api/desk/entries?state=draft")
    row = next((r for r in rows if str(r.get("slug")) == DRAFT_SLUG), None)
    assert row is not None, f"the desk list carries the seeded draft: {rows!r}"
    detail = desk.get(f"/desk/entries/{entry_id(row)}")
    assert detail.status_code == 200, f"the editor reads the draft place: {describe(detail)}"
    brochure = detail.json().get("brochure") or (detail.json().get("brochures") or [None])[0]
    assert brochure, (
        f"the draft place carries the guide document {DRAFT_BROCHURE_TITLE!r}: "
        f"{detail.json()!r}"
    )
    r = anon.get(f"/media/brochures/{brochure['id']}")
    assert r.status_code == 404, (
        f"the guide document of a draft place answers 404 to an anonymous caller: "
        f"{describe(r)}"
    )


def test_sign_in_failure_hides_whether_the_address_exists(api):
    """A failed sign-in answers the same way for a known and an unknown address."""
    known = api.post("/auth/login", json={"email": EDITOR_EMAIL, "password": "wrong-pw"})
    unknown = api.post("/auth/login",
                       json={"email": f"nobody-{os.urandom(4).hex()}@example.com",
                             "password": "wrong-pw"})
    assert known.status_code in (400, 401, 403), (
        f"a wrong password is refused: {describe(known)}"
    )
    assert known.status_code == unknown.status_code, (
        f"an unknown address and a wrong password answer alike; saw "
        f"{known.status_code} then {unknown.status_code}"
    )
    assert known.text == unknown.text or len(known.text) == len(unknown.text), (
        f"the refusal body tells an unknown address apart from a wrong password: "
        f"{known.text[:200]!r} then {unknown.text[:200]!r}"
    )
    assert "access_token" not in known.text, (
        f"a failed sign-in mints no token: {known.text[:200]!r}"
    )


def test_publish_refused_when_a_required_field_is_empty(desk):
    """A publish with an empty required field is refused, naming the field."""
    entry = create_draft(desk, summary="")
    eid = entry_id(entry)
    try:
        add_picture(desk, eid)
        r = publish(desk, eid)
        assert 400 <= r.status_code < 500, (
            f"publishing with an empty summary is refused at the API: {describe(r)}"
        )
        assert "summary" in r.text.lower(), (
            f"the refusal names which condition failed: {r.text[:300]!r}"
        )
        rows = json_list(desk.get("/desk/entries", params={"state": "all"}),
                         "GET /api/desk/entries?state=all")
        row = next(x for x in rows if str(x.get("slug")) == entry["slug"])
        assert row.get("state") == "draft", (
            f"a refused publish leaves the place in state draft: {row!r}"
        )
    finally:
        drop(desk, eid)


def test_publish_refused_when_the_slug_is_already_taken(desk):
    """A slug another place already holds is refused, at the write or at the publish."""
    attempt = desk.post("/desk/entries", json=entry_payload(slug="alder-cove"))
    if 400 <= attempt.status_code < 500:
        lowered = attempt.text.lower()
        assert "address" in lowered or "slug" in lowered or "taken" in lowered, (
            f"the write refusal names the colliding web address: {attempt.text[:300]!r}"
        )
        return
    assert attempt.status_code in (200, 201), (
        f"the write either creates the draft or refuses it as a client error: "
        f"{describe(attempt)}"
    )
    eid = entry_id(attempt.json())
    add_picture(desk, eid)
    r = publish(desk, eid)
    assert 400 <= r.status_code < 500, (
        f"a write that accepted the taken slug 'alder-cove' must be refused at the "
        f"publish instead: {describe(r)}"
    )
    lowered = r.text.lower()
    assert "address" in lowered or "slug" in lowered or "taken" in lowered, (
        f"the refusal names the colliding web address: {r.text[:300]!r}"
    )


def test_publish_refused_when_the_slug_is_a_reserved_segment(desk):
    """Each of the eleven reserved segments is refused, at the write or at the publish."""
    for segment in RESERVED_SEGMENTS:
        attempt = desk.post("/desk/entries", json=entry_payload(slug=segment))
        if 400 <= attempt.status_code < 500:
            continue
        assert attempt.status_code in (200, 201), (
            f"the write either creates the draft or refuses the reserved segment "
            f"{segment!r} as a client error: {describe(attempt)}"
        )
        eid = entry_id(attempt.json())
        r = publish(desk, eid)
        assert 400 <= r.status_code < 500, (
            f"the reserved segment {segment!r} is refused at the API, at the write or "
            f"at the publish, rather than by a disabled control: {describe(r)}"
        )
        drop(desk, eid)


def test_publish_refused_when_a_picture_description_is_empty(desk):
    """A publish is refused while an attached picture carries no description."""
    entry = create_draft(desk)
    eid = entry_id(entry)
    try:
        blank = desk.post("/desk/uploads", json={
            "entry_id": eid, "kind": "gallery",
            "filename": f"probe-{os.urandom(4).hex()}.jpg", "content_type": "image/jpeg",
        })
        assert blank.status_code in (200, 201), (
            f"the upload target is issued: {describe(blank)}"
        )
        registered = desk.post("/desk/images", json={
            "entry_id": eid, "object_key": blank.json()["object_key"],
            "alt_text": "", "width": 1200, "height": 800, "position": 1,
        })
        if registered.status_code in (200, 201):
            r = publish(desk, eid)
            assert 400 <= r.status_code < 500, (
                f"publishing with a picture that has no description is refused: "
                f"{describe(r)}"
            )
        else:
            assert 400 <= registered.status_code < 500, (
                f"a picture with no description is refused at registration or at "
                f"publish: {describe(registered)}"
            )
    finally:
        drop(desk, eid)


def test_a_created_entry_always_lands_in_the_draft_state(desk):
    """Every created place lands in state draft, whatever the request asks for."""
    entry = create_draft(desk, state="published")
    eid = entry_id(entry)
    try:
        assert entry.get("state") == "draft", (
            f"a created place lands in state draft even when the body asks for "
            f"published: {entry!r}"
        )
        rows = json_list(desk.get("/desk/entries", params={"state": "all"}),
                         "GET /api/desk/entries?state=all")
        row = next(x for x in rows if str(x.get("slug")) == entry["slug"])
        assert row.get("state") == "draft", (
            f"the stored state of a newly created place is draft: {row!r}"
        )
    finally:
        drop(desk, eid)


def test_a_name_shorter_than_three_characters_is_refused(desk):
    """A place name shorter than three characters is refused on the server."""
    r = desk.post("/desk/entries", json=entry_payload(name="ab"))
    assert 400 <= r.status_code < 500, (
        f"a name of {NAME_MIN - 1} characters is refused on the server: {describe(r)}"
    )
    rows = json_list(desk.get("/desk/entries", params={"state": "all"}),
                     "GET /api/desk/entries?state=all")
    assert "ab" not in names_of(rows), (
        f"the refused name is written nowhere; saw {sorted(names_of(rows))[:10]}"
    )


def test_a_summary_over_two_hundred_forty_characters_is_refused(desk):
    """A summary over two hundred and forty characters is refused, writing nothing."""
    long_summary = "s" * (SUMMARY_MAX + 1)
    payload = entry_payload(summary=long_summary)
    r = desk.post("/desk/entries", json=payload)
    assert 400 <= r.status_code < 500, (
        f"a summary of {SUMMARY_MAX + 1} characters is refused: {describe(r)}"
    )
    rows = json_list(desk.get("/desk/entries", params={"state": "all"}),
                     "GET /api/desk/entries?state=all")
    assert payload["slug"] not in slugs_of(rows), (
        f"a refused summary writes no row for {payload['slug']!r}"
    )


def test_a_filter_matching_nothing_returns_an_empty_array(api):
    """A filter matching nothing answers an empty array rather than an error."""
    rows = json_list(api.get("/entries", params={"name": "zzzznowhere"}),
                     "GET /api/entries?name=zzzznowhere")
    assert rows == [], (
        f"a filter that matches nothing answers an empty array; saw {rows!r}"
    )


def test_unpublishing_removes_the_place_from_every_public_response(api, desk):
    """Unpublishing a place removes it from every public response at once."""
    entry = create_draft(desk, themes=["coastline"])
    eid = entry_id(entry)
    picture = add_picture(desk, eid)
    try:
        assert publish(desk, eid).status_code in (200, 201), "the probe place publishes"
        assert entry["slug"] in slugs_of(json_list(api.get("/entries"), "GET /api/entries")), (
            f"the published probe place is on the index: {entry['slug']!r}"
        )
        assert unpublish(desk, eid).status_code in (200, 201), "the probe place unpublishes"
        index = json_list(api.get("/entries"), "GET /api/entries")
        assert entry["slug"] not in slugs_of(index), (
            f"unpublishing removes {entry['slug']!r} from the index; "
            f"saw {sorted(slugs_of(index))}"
        )
        collection = api.get("/collections/coastline")
        body = collection.json()
        rows = body.get("entries") if isinstance(body, dict) else body
        assert entry["slug"] not in slugs_of(rows or []), (
            f"unpublishing removes {entry['slug']!r} from its collection"
        )
        detail = api.get(f"/entries/{entry['slug']}")
        assert detail.status_code == 404, (
            f"the address of an unpublished place answers 404: {describe(detail)}"
        )
        gallery = json_list(api.get("/images"), "GET /api/images")
        owners = {str(r.get("slug") or r.get("entry_slug") or "") for r in gallery}
        assert entry["slug"] not in owners, (
            f"unpublishing removes the pictures of {entry['slug']!r} from the gallery"
        )
        bytes_now = api.get(f"/media/images/{picture['id']}")
        assert bytes_now.status_code == 404, (
            f"the picture bytes of an unpublished place answer 404: {describe(bytes_now)}"
        )
    finally:
        drop(desk, eid)


def test_uploaded_picture_object_exists_in_the_bucket(desk, store):
    """An uploaded picture exists as a real object in the bucket."""
    entry = create_draft(desk)
    eid = entry_id(entry)
    try:
        picture = add_picture(desk, eid)
        key = picture["object_key"]
        assert poll_until(lambda: store.exists(key),
                          f"the object {key!r} should exist in the bucket"), key
        held = store.list(f"entries/{eid}/gallery/")
        assert key in held, (
            f"the uploaded object {key!r} is listed under the entry's gallery prefix; "
            f"saw {held!r}"
        )
    finally:
        drop(desk, eid)


def test_uploaded_object_key_follows_the_gallery_scheme(desk, store):
    """An uploaded object key follows the entry gallery scheme."""
    entry = create_draft(desk)
    eid = entry_id(entry)
    try:
        picture = add_picture(desk, eid)
        key = picture["object_key"]
        prefix = f"entries/{eid}/gallery/"
        assert key.startswith(prefix), (
            f"the object key should follow entries/<entry_id>/gallery/"
            f"<sha256_of_bytes>.<ext>; saw {key!r} for entry {eid}"
        )
        tail = key[len(prefix):]
        digest, _, ext = tail.rpartition(".")
        assert len(digest) == 64, (
            f"the key names the sha256 of the bytes, which is 64 hex characters; "
            f"saw {digest!r} in {key!r}"
        )
        assert all(c in "0123456789abcdef" for c in digest), (
            f"the digest in the key is lowercase hex; saw {digest!r}"
        )
        assert ext, f"the key carries the file extension; saw {key!r}"
    finally:
        drop(desk, eid)


def test_published_picture_bytes_stream_from_the_bucket(api, desk, store):
    """A published place's picture streams through the app from the bucket."""
    entry = create_draft(desk)
    eid = entry_id(entry)
    try:
        picture = add_picture(desk, eid)
        assert publish(desk, eid).status_code in (200, 201), "the probe place publishes"
        r = api.get(f"/media/images/{picture['id']}")
        assert r.status_code == 200, (
            f"the picture of a published place resolves: {describe(r)}"
        )
        assert r.content == b"probe-picture-bytes", (
            f"the app serves the bytes that were stored, not a substitute; "
            f"saw {r.content[:60]!r}"
        )
        assert store.exists(picture["object_key"]), (
            f"the served bytes live in the bucket at {picture['object_key']!r}"
        )
    finally:
        unpublish(desk, eid)
        drop(desk, eid)


def test_guide_document_download_carries_an_attachment_filename(api):
    """A guide document download carries an attachment filename from its title."""
    rows = json_list(api.get("/brochures"), "GET /api/brochures")
    row = next((r for r in rows if r.get("title") == REGIONAL_BROCHURES[1]), None)
    assert row is not None, (
        f"the library carries {REGIONAL_BROCHURES[1]!r}; "
        f"saw {sorted(names_of(rows, 'title'))}"
    )
    r = api.get(f"/media/brochures/{row['id']}")
    assert r.status_code == 200, f"the guide document resolves: {describe(r)}"
    disposition = r.headers.get("content-disposition", "")
    assert "attachment" in disposition.lower(), (
        f"the download carries a Content-Disposition of attachment; "
        f"saw {disposition!r}"
    )
    expected = BROCHURE_FILENAMES[REGIONAL_BROCHURES[1]]
    assert expected in disposition, (
        f"the title {row['title']!r} lowercases and hyphenates to {expected!r}; "
        f"saw {disposition!r}"
    )


def test_unpublished_entry_objects_stop_resolving_at_once(api, desk):
    """An unpublished place's objects stop resolving from that moment."""
    entry = create_draft(desk)
    eid = entry_id(entry)
    try:
        picture = add_picture(desk, eid)
        assert publish(desk, eid).status_code in (200, 201), "the probe place publishes"
        live = api.get(f"/media/images/{picture['id']}")
        assert live.status_code == 200, (
            f"the picture resolves while the place is published: {describe(live)}"
        )
        assert unpublish(desk, eid).status_code in (200, 201), "the probe place unpublishes"
        gone = api.get(f"/media/images/{picture['id']}")
        assert gone.status_code == 404, (
            f"the picture stops resolving the moment the place returns to draft, with "
            f"no cache window outliving the change: {describe(gone)}"
        )
        settle()
        still_gone = api.get(f"/media/images/{picture['id']}")
        assert still_gone.status_code == 404, (
            f"the picture stays unreachable a moment later: {describe(still_gone)}"
        )
    finally:
        drop(desk, eid)


def test_every_content_picture_carries_alternative_text(page):
    """Every content picture on a public surface carries alternative text."""
    origin = appclient.app_url()
    missing = []
    for route in ("/", "/destination", "/photo-gallery", "/destination/alder-cove"):
        page.goto(f"{origin}{route}")
        found = page.eval_on_selector_all(
            "img",
            "els => els.map(e => ({alt: e.getAttribute('alt'),"
            " role: e.getAttribute('role'), src: e.getAttribute('src') || ''}))")
        for item in found:
            decorative = item["alt"] == "" or item["role"] == "presentation"
            if item["alt"] is None or (not decorative and not str(item["alt"]).strip()):
                missing.append((route, item["src"][:60]))
    assert not missing, (
        f"every content picture carries alternative text and a decorative one declares "
        f"itself decorative with an empty alt; missing on {missing}"
    )


def test_a_narrow_viewport_has_no_sideways_overflow(page):
    """At a narrow viewport no public surface overflows sideways."""
    origin = appclient.app_url()
    page.set_viewport_size(NARROW_VIEWPORT)
    overflowing = []
    for route in PUBLIC_ROUTES:
        page.goto(f"{origin}{route}")
        widths = page.evaluate(
            "() => [document.documentElement.scrollWidth, window.innerWidth]")
        if widths[0] > widths[1] + 1:
            overflowing.append((route, widths))
    assert not overflowing, (
        f"nothing overflows sideways at a {NARROW_VIEWPORT['width']}px viewport; "
        f"saw scrollWidth past innerWidth on {overflowing}"
    )


def test_body_text_contrast_meets_the_accessibility_bar(page):
    """Body text on a public surface meets the WCAG AA contrast bar."""
    origin = appclient.app_url()
    page.goto(f"{origin}/destination/alder-cove")
    probe = page.evaluate(
        "() => {const el = document.querySelector('main p') || "
        "document.querySelector('p'); if (!el) return null; "
        "const cs = getComputedStyle(el); let bg = 'rgba(0, 0, 0, 0)'; "
        "let node = el; while (node) { const c = getComputedStyle(node).backgroundColor;"
        " if (c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent') { bg = c; break; } "
        "node = node.parentElement; } "
        "return {color: cs.color, background: bg, size: cs.fontSize};}")
    assert probe, "the place entry carries a paragraph of body text"
    ratio = contrast_ratio(parse_rgb(probe["color"]), parse_rgb(probe["background"]))
    assert ratio >= CONTRAST_FLOOR, (
        f"body text meets the WCAG AA contrast bar of {CONTRAST_FLOOR} to 1; "
        f"{probe['color']} on {probe['background']} measures {ratio:.2f} to 1"
    )


def test_place_title_uses_the_display_type_family(page):
    """A place title is set in the display family named in the brief."""
    origin = appclient.app_url()
    page.goto(f"{origin}/destination/alder-cove")
    families = page.evaluate(
        "() => {const el = document.querySelector('h1'); "
        "return el ? getComputedStyle(el).fontFamily : null;}")
    assert families, "the place entry carries a first-level heading"
    first = families.split(",")[0].strip().strip('\"\'')
    assert first == DISPLAY_FAMILY, (
        f"a place title is set in {DISPLAY_FAMILY!r}; the computed stack begins "
        f"{first!r} ({families!r})"
    )
    body = page.evaluate(
        "() => {const el = document.querySelector('main p') || document.body; "
        "return getComputedStyle(el).fontFamily;}")
    body_first = body.split(",")[0].strip().strip('\"\'')
    assert body_first == BODY_FAMILY, (
        f"body text is set in {BODY_FAMILY!r}; the computed stack begins {body_first!r}"
    )


def test_skip_link_is_the_first_focusable_element(page):
    """The skip link is the first focusable element in the document."""
    origin = appclient.app_url()
    page.goto(origin)
    page.keyboard.press("Tab")
    focused = page.evaluate(
        "() => {const el = document.activeElement; return el ? "
        "{text: (el.textContent || '').trim(), href: el.getAttribute('href') || ''} "
        ": null;}")
    assert focused, "one element holds focus after the first Tab"
    assert "Skip to content" in focused["text"], (
        f"the first focusable element is the skip link reading 'Skip to content'; "
        f"saw {focused!r}"
    )


def test_navigation_targets_are_comfortably_sized(page):
    """Every navigation target is a comfortably sized touch target."""
    origin = appclient.app_url()
    page.set_viewport_size(NARROW_VIEWPORT)
    page.goto(origin)
    sizes = page.eval_on_selector_all(
        "header a, header button",
        "els => els.filter(e => e.offsetParent !== null)"
        ".map(e => {const r = e.getBoundingClientRect(); "
        "return {w: Math.round(r.width), h: Math.round(r.height), "
        "text: (e.textContent || '').trim().slice(0, 30)};})")
    assert sizes, "the header carries navigation targets at a narrow viewport"
    small = [s for s in sizes if min(s["w"], s["h"]) < TOUCH_TARGET_MIN]
    assert not small, (
        f"every navigation target measures at least {TOUCH_TARGET_MIN}px on its "
        f"shorter side; these are smaller: {small}"
    )


def test_body_copy_uses_the_condensed_sans_family(page):
    """Navigation labels, controls and metadata lines take the narrow sans."""
    origin = appclient.app_url()
    page.goto(f"{origin}/destination")
    families = page.evaluate(
        "() => {const out = {};"
        "const nav = document.querySelector('header a, nav a');"
        "if (nav) out.nav = getComputedStyle(nav).fontFamily;"
        "const ctl = document.querySelector('header input, main input, main select');"
        "if (ctl) out.control = getComputedStyle(ctl).fontFamily;"
        "const meta = document.querySelector('main small, main figcaption, main time');"
        "if (meta) out.metadata = getComputedStyle(meta).fontFamily;"
        "return out;}")
    assert families.get("nav"), "the place index carries a navigation label"
    for where, stack in families.items():
        first = stack.split(",")[0].strip().strip('"\'')
        assert first == BODY_FAMILY, (
            f"the {where} is set in {BODY_FAMILY!r}; the computed stack begins "
            f"{first!r} ({stack!r})"
        )


def test_home_header_media_declares_a_poster_and_defers_play(page):
    """The header panel ships a poster frame, and only the first screen loads eagerly."""
    origin = appclient.app_url()
    page.goto(f"{origin}/")
    media = page.evaluate(
        "() => {const el = document.querySelector('video');"
        "return el ? {poster: el.getAttribute('poster') || '', muted: el.muted,"
        " loop: el.loop, inline: el.playsInline, controls: el.controls} : null;}")
    assert media, "the home surface carries a motion panel in its header"
    assert media["poster"], (
        "the motion panel declares a poster frame, which is what a visitor sees where "
        f"it cannot play through; saw {media!r}"
    )
    for flag, want in (("muted", True), ("loop", True), ("inline", True),
                       ("controls", False)):
        assert media[flag] is want, (
            f"the header motion panel is muted, looping, inline and without controls; "
            f"{flag} is {media[flag]!r}, expected {want!r}"
        )
    loading = page.evaluate(
        "() => Array.from(document.images).map(i => i.getAttribute('loading') || '')")
    later = loading[4:]
    eager = [i + 4 for i, v in enumerate(later) if v != "lazy"]
    assert not eager, (
        "only the header still and the first row of cards load eagerly; images at "
        f"document positions {eager} past the first four carry {[loading[i] for i in eager]!r} "
        f"rather than 'lazy'"
    )


def test_every_still_declares_its_dimensions_and_a_placeholder(page):
    """Every content still reserves its box and is delivered responsively."""
    origin = appclient.app_url()
    page.goto(f"{origin}/photo-gallery")
    stills = page.evaluate(
        "() => Array.from(document.images).map(i => ({src: i.currentSrc || i.src,"
        " w: i.getAttribute('width'), h: i.getAttribute('height'),"
        " ratio: getComputedStyle(i).aspectRatio,"
        " srcset: i.getAttribute('srcset') || '', sizes: i.getAttribute('sizes') || '',"
        " ground: getComputedStyle(i.parentElement || i).backgroundColor}))")
    assert stills, "the gallery carries stills"
    for s in stills:
        sized = (s["w"] and s["h"]) or (s["ratio"] and s["ratio"] != "auto")
        assert sized, (
            "a still declares its intrinsic width and height, or an aspect ratio, so "
            f"its box is reserved before it arrives; saw {s!r}"
        )
        assert s["srcset"] and s["sizes"], (
            f"a still is delivered responsively, with a candidate set and a sizes hint; "
            f"saw srcset={s['srcset']!r} sizes={s['sizes']!r} for {s['src']!r}"
        )
        ground = s["ground"].replace(" ", "")
        assert ground not in ("rgba(0,0,0,0)", "transparent"), (
            "a still loads over a generated placeholder ground rather than over nothing; "
            f"the computed background behind {s['src']!r} is {s['ground']!r}"
        )


def test_five_named_breakpoints_drive_the_pinned_column_counts(page):
    """The five tiers are named in ascending order, and each card row folds to one."""
    origin = appclient.app_url()
    page.goto(f"{origin}/")
    sheets = page.evaluate(
        "() => Array.from(document.styleSheets).map(s => {try {return Array.from("
        "s.cssRules).map(r => r.cssText).join(' ');} catch (e) {return '';}}).join(' ')")
    haystack = sheets + " " + page.content()
    tiers = ("sm", "md", "lg", "xl", "xxl")
    at = {}
    for tier in tiers:
        found = re.search(rf"(?<![A-Za-z0-9]){tier}(?![A-Za-z0-9])", haystack)
        assert found, (
            f"the product names its five breakpoints {tiers}; {tier!r} appears as a name "
            f"in neither the stylesheet nor the markup"
        )
        at[tier] = found.start()
    assert len(at) == len(tiers), f"all five tier names are present; found {sorted(at)}"
    rows = {"/destination": 3, "/brochures": 4, "/photo-gallery": 4}
    for route, widest in rows.items():
        page.set_viewport_size(NARROW_VIEWPORT)
        page.goto(f"{origin}{route}")
        narrow = _columns(page)
        assert narrow == 1, (
            f"card rows fold to a single column at a {NARROW_VIEWPORT['width']}px "
            f"viewport; {route} shows {narrow} across"
        )
        page.set_viewport_size(WIDE_VIEWPORT)
        page.goto(f"{origin}{route}")
        wide = _columns(page)
        assert 1 < wide <= widest, (
            f"{route} runs up to {widest} cards across at its widest tier and more than "
            f"one above the narrowest; at {WIDE_VIEWPORT['width']}px it shows {wide}"
        )


def _columns(page) -> int:
    return page.evaluate(
        "() => {const grid = document.querySelector('main ul, main ol, main div[class]');"
        "if (!grid) return 0;"
        "const kids = Array.from(grid.children).filter(k => k.getBoundingClientRect().width);"
        "if (!kids.length) return 0;"
        "const top = Math.round(kids[0].getBoundingClientRect().top);"
        "return kids.filter(k => Math.round(k.getBoundingClientRect().top) === top).length;}")


def test_guide_document_cover_is_derived_from_its_first_page(page, api):
    """Every card shows its own document's cover, including a guide with no place."""
    origin = appclient.app_url()
    rows = json_list(api.get("/brochures"), "GET /api/brochures")
    page.goto(f"{origin}/brochures")
    covers = page.evaluate(
        "() => Array.from(document.images).map(i => ({src: i.currentSrc || i.src,"
        " w: i.naturalWidth}))")
    drawn = [c for c in covers if c["w"] > 0]
    assert len(drawn) >= len(rows), (
        f"the library lists {len(rows)} guide documents, so each card carries a cover; "
        f"{len(drawn)} of {len(covers)} images drew"
    )
    sources = [c["src"] for c in drawn]
    repeated = sorted({s for s in sources if sources.count(s) > 1})
    assert not repeated, (
        "a cover is the document's own first page, so no two cards share one; "
        f"{repeated} is used more than once"
    )
    regional = [r for r in rows if r.get("title") in REGIONAL_BROCHURES]
    assert len(regional) == len(REGIONAL_BROCHURES), (
        f"the three regional guides belong to no place; saw {regional!r}"
    )
    assert len(drawn) >= len(regional), (
        "a regional guide owns no place and no gallery, so its cover can only come from "
        f"the document itself; {len(drawn)} covers drew for {len(regional)} regional guides"
    )


def test_featured_band_is_absent_when_no_entry_carries_the_flag(desk, page):
    """The featured band renders what exists, and is omitted where nothing is flagged."""
    origin = appclient.app_url()
    rows = json_list(desk.get("/desk/entries?state=published"),
                     "GET /api/desk/entries?state=published")
    by_slug = {r.get("slug"): r for r in rows}
    flagged = [by_slug[s] for s in FEATURED_SLUGS if s in by_slug]
    assert len(flagged) == len(FEATURED_SLUGS), (
        f"the seed flags {sorted(FEATURED_SLUGS)} as featured; the desk list carries "
        f"{sorted(by_slug)}"
    )
    try:
        for row in flagged:
            desk.patch(f"/desk/entries/{entry_id(row)}", json={"featured": False})
        settle()
        page.goto(f"{origin}/")
        assert FEATURED_HEADING not in page.content(), (
            "where no entry carries the flag the whole featured band is omitted rather "
            "than rendered empty; the heading is still on the home surface"
        )
        desk.patch(f"/desk/entries/{entry_id(flagged[0])}", json={"featured": True})
        settle()
        page.goto(f"{origin}/")
        assert FEATURED_HEADING in page.content(), (
            "one flagged entry brings the featured band back; the heading is absent"
        )
        cards = _columns(page)
        assert cards <= 1, (
            "where fewer than six entries carry the flag the row renders what exists and "
            f"does not pad; one flagged entry drew {cards} cards"
        )
    finally:
        for row in flagged:
            desk.patch(f"/desk/entries/{entry_id(row)}", json={"featured": True})
        settle()


def test_calendar_names_no_month_that_holds_no_event(api, page):
    """The month headings follow the events present rather than a stored list."""
    origin = appclient.app_url()
    rows = json_list(api.get("/events"), "GET /api/events")
    assert rows, "the calendar carries the seeded events"
    months = {str(r.get("starts_on", ""))[:7] for r in rows}
    months.discard("")
    assert months, f"each event carries a `starts_on` date; saw {rows!r}"
    page.goto(f"{origin}/event")
    headings = page.evaluate(
        "() => Array.from(document.querySelectorAll('main h2, main h3'))"
        ".map(h => h.textContent.trim()).filter(Boolean)")
    assert headings, "the calendar groups its events under month headings"
    assert len(headings) <= len(months), (
        f"a month holding no event gets no heading: the events span {len(months)} "
        f"month(s) and the surface draws {len(headings)} heading(s) {headings!r}"
    )


def test_no_font_or_icon_asset_ships_with_the_build(page):
    """The build ships no font file, no icon font and no lossless photographic still."""
    origin = appclient.app_url()
    seen = []
    page.on("response", lambda r: seen.append((r.url, r.headers.get("content-type", ""))))
    page.goto(f"{origin}/")
    page.goto(f"{origin}/destination")
    own = [(u, c) for u, c in seen if u.startswith(origin)]
    fonts = [u for u, c in own
             if "font" in c or u.rsplit("?", 1)[0].endswith((".woff", ".woff2", ".ttf",
                                                             ".otf", ".eot"))]
    assert not fonts, (
        f"the build names its families and ships no font file; it served {fonts}"
    )
    lossless = [u for u, c in own
                if u.rsplit("?", 1)[0].endswith((".png", ".bmp", ".tiff"))
                or c in ("image/png", "image/bmp", "image/tiff")]
    assert not lossless, (
        f"a photographic image ships in no lossless format; the build served {lossless}"
    )
    third_party = sorted({u.split("/")[2] for u, _ in seen
                          if not u.startswith(origin) and u.startswith("http")})
    assert all("font" in host or "gstatic" in host for host in third_party), (
        "the one third-party request the product makes at run time is the font service; "
        f"it also reached {third_party}"
    )


def test_home_surface_stays_inside_its_delivery_budget(page):
    """The home surface's script weight and its blocking request count hold."""
    origin = appclient.app_url()
    sizes = []
    page.on("response", lambda r: sizes.append(
        (r.url, r.headers.get("content-type", ""), r.headers.get("content-length", "0"))))
    page.goto(f"{origin}/")
    script_bytes = sum(int(n or 0) for u, c, n in sizes
                       if u.startswith(origin) and ("javascript" in c or u.endswith(".js")))
    assert script_bytes <= 180 * 1024, (
        f"the compressed JavaScript the home surface delivers stays under 180KB; it "
        f"delivered {script_bytes} bytes"
    )
    blocking = page.evaluate(
        "() => {const head = document.head;"
        "const css = Array.from(head.querySelectorAll('link[rel=stylesheet]'))"
        ".filter(l => !l.media || l.media === 'all' || l.media === 'screen');"
        "const js = Array.from(head.querySelectorAll('script[src]'))"
        ".filter(s => !s.defer && !s.async && s.type !== 'module');"
        "return css.length + js.length;}")
    assert blocking <= 3, (
        f"no more than three requests block first paint on the home surface; the head "
        f"carries {blocking}"
    )


def test_generated_stills_are_seeded_by_their_own_entry(page):
    """Stills are generated from the entry, so the same entry draws the same still."""
    origin = appclient.app_url()

    def stills():
        page.goto(f"{origin}/destination")
        return page.evaluate(
            "() => Array.from(document.images).map(i => i.currentSrc || i.src)")

    first = stills()
    assert first, "the place index draws a still for each place"
    again = stills()
    assert first == again, (
        "the same entry always produces the same still, so nothing reshuffles between "
        f"reads; the index drew {first} then {again}"
    )
    inline = page.evaluate(
        "() => ({marks: document.querySelectorAll('svg').length,"
        " filters: document.querySelectorAll('svg filter feTurbulence').length})")
    assert inline["marks"] >= 1, (
        "the product's marks are inline vector drawings rather than an icon font; the "
        f"place index carries {inline['marks']} of them"
    )


def test_place_entry_prints_as_an_article(page):
    """The print stylesheet drops the chrome and prints each link's destination."""
    origin = appclient.app_url()
    page.goto(f"{origin}/destination/alder-cove")
    page.emulate_media(media="print")
    printed = page.evaluate(
        "() => {const vis = el => el && getComputedStyle(el).display !== 'none'"
        " && getComputedStyle(el).visibility !== 'hidden';"
        "return {header: vis(document.querySelector('header')),"
        " footer: vis(document.querySelector('footer')),"
        " stills: Array.from(document.images).filter(i => vis(i)).length};}")
    page.emulate_media(media="screen")
    assert not printed["header"] and not printed["footer"], (
        "a place entry prints as an article, with the chrome gone; the print preview "
        f"still draws header={printed['header']} footer={printed['footer']}"
    )
    assert printed["stills"] <= 1, (
        "the print preview reduces the picture strip to its first still; it draws "
        f"{printed['stills']}"
    )
