from __future__ import annotations

import collections
import re
import urllib.parse

import _shapes
import conftest


def _hops_within(graph, start, limit):
    seen = {start: 0}
    frontier = collections.deque([start])
    while frontier:
        node = frontier.popleft()
        for nxt in graph.get(node, ()):
            if nxt not in seen:
                seen[nxt] = seen[node] + 1
                frontier.append(nxt)
    return {k: v for k, v in seen.items() if v <= limit}


def _related_graph(anon):
    listing = conftest.slugs_of(anon.get("/case-studies").json())
    graph = {}
    for slug in listing:
        response = anon.get(f"/case-studies/{slug}/related")
        assert response.status_code == 200, (
            f"the suggestion pair for {slug} must be readable: "
            + conftest.describe(response))
        graph[slug] = conftest.slugs_of(response.json())
    return listing, graph


def _account_id(backend, email_address):
    row = backend.one("accounts", email=email_address)
    assert row is not None, f"the account {email_address} must be stored"
    return row["id"]


def _case_study_row(backend, slug):
    row = backend.one("case_studies", slug=slug)
    assert row is not None, f"the case study {slug} must be stored as a row"
    return row


def test_health_endpoint_reports_ready(anon):
    response = anon.get("/health")
    assert response.status_code == 200, (
        "GET /api/health must answer 200 once the app is ready: "
        + conftest.describe(response))


def test_published_case_studies_are_listed_for_a_visitor(anon):
    response = anon.get("/case-studies")
    assert response.status_code == 200, (
        "GET /api/case-studies must be readable without signing in: "
        + conftest.describe(response))
    slugs = conftest.slugs_of(response.json())
    for expected in conftest.PUBLISHED_SLUGS:
        assert expected in slugs, (
            f"the seeded published case study {expected} is missing from the "
            f"public listing, which carried {slugs}")
    assert conftest.DRAFT_SLUG not in slugs, (
        f"the draft {conftest.DRAFT_SLUG} must be absent from the public listing, "
        f"which carried {slugs}")
    for entry in response.json():
        missing = [f for f in conftest.LIST_FIELDS if f not in entry]
        assert not missing, f"each listed case study must carry {missing}: {entry}"


def test_case_study_detail_returns_chapters_with_rail_labels(anon):
    for slug, expected in conftest.CHAPTERS.items():
        response = anon.get(f"/case-studies/{slug}")
        assert response.status_code == 200, (
            f"the published case study {slug} must be readable: "
            + conftest.describe(response))
        body = response.json()
        missing = [f for f in conftest.DETAIL_FIELDS if f not in body]
        assert not missing, f"the {slug} detail lacks {missing}: " + conftest.describe(response)
        chapters = body.get("chapters")
        assert isinstance(chapters, list), (
            f"the {slug} detail must carry a chapters array: " + conftest.describe(response))
        got = [(str(c.get("anchor")), str(c.get("rail_label")), str(c.get("heading")))
               for c in chapters]
        assert got == list(expected), (
            f"{slug} must carry its chapters with their anchors, rail labels and "
            f"headings in order; the response carried {got}")
        media = body.get("media")
        assert isinstance(media, list) and media, (
            f"the {slug} detail must list its media: " + conftest.describe(response))
        lacking = [f for f in conftest.MEDIA_FIELDS if f not in media[0]]
        assert not lacking, f"each {slug} media entry must carry {lacking}: {media[0]}"


def test_chapter_anchors_start_where_the_document_starts(anon):
    response = anon.get("/case-studies/foundry-campaign")
    assert response.status_code == 200, (
        "the published case study foundry-campaign must be readable: "
        + conftest.describe(response))
    anchors = [str(c.get("anchor")) for c in response.json().get("chapters") or []]
    assert anchors == list(conftest.CAMPAIGN_ANCHORS), (
        "foundry-campaign's chapters start at s4 and run to s8; the response "
        f"carried {anchors}")


def test_case_study_page_renders_rail_labels_beside_headings(site):
    page = site.get("/verity-biotics-product")
    assert page.status_code == 200, (
        "the case study route must render: " + conftest.describe(page))
    text = conftest.page_text(page.text)
    for anchor, label, heading in conftest.VBP_CHAPTERS:
        assert label in text, (
            f"the rendered case study must carry the rail label {label!r}")
        assert heading in text, (
            f"the rendered case study must carry the article heading {heading!r}")
        assert conftest.has_anchor(page.text, anchor), (
            f"the rendered case study must carry the chapter anchor {anchor}")


def test_campaign_page_carries_its_first_anchor_at_s4(site):
    page = site.get("/foundry-campaign")
    assert page.status_code == 200, (
        "the foundry-campaign route must render: " + conftest.describe(page))
    for anchor in conftest.CAMPAIGN_ANCHORS:
        assert conftest.has_anchor(page.text, anchor), (
            f"the foundry-campaign page must carry the chapter anchor {anchor}")
    assert not conftest.has_anchor(page.text, "s1"), (
        "the foundry-campaign page has no chapter s1, so no element may carry that "
        "anchor")


def test_home_page_orders_featured_before_numbered_work(site):
    page = site.get("/")
    assert page.status_code == 200, "the home route must render: " + conftest.describe(page)
    text = conftest.page_text(conftest.visible_markup(page.text))
    positions = []
    for slug in conftest.FEATURED_SLUGS + conftest.LIST_SLUGS:
        title = conftest.INDEX_TITLES[slug]
        where = text.find(title)
        assert where >= 0, f"the home page must show the index title {title!r}"
        positions.append(where)
    assert positions == sorted(positions), (
        "the four featured case studies must appear in position order ahead of the "
        "seven work-list case studies, also in position order")
    assert conftest.DRAFT_TITLE not in text, (
        "the draft's title must be absent from the home page")


def test_home_page_top_bar_targets_the_featured_band(site):
    page = site.get("/")
    text = conftest.page_text(page.text)
    for label in conftest.NAV_LABELS:
        assert label in text, f"the home top bar must carry the label {label!r}"
    for anchor in conftest.HOME_ANCHORS:
        assert conftest.has_anchor(page.text, anchor), (
            f"the home page must carry the anchor #{anchor}")
    assert re.search(r"""href\s*=\s*["']#featured["']""", page.text), (
        "a home top bar item must link to #featured")


def test_split_passages_remain_continuous_text(site):
    page = site.get("/")
    text = conftest.page_text(page.text)
    assert conftest.PHILOSOPHY_PASSAGE in text, (
        "the philosophy passage must be present in the page as one continuous "
        "sentence, not only as separate characters")
    assert conftest.PUNCHLINE in text, (
        "the punchline must be present in the page as one continuous sentence")


def test_mechanism_card_amplitude_comes_from_the_constant(site):
    page = site.get("/")
    text = conftest.page_text(page.text)
    assert conftest.MECHANISM_LINE in text, (
        "the mechanism card's fourth line must be present in the page, rendered from "
        f"the letter amplitude, as {conftest.MECHANISM_LINE!r}")


def test_list_endpoints_return_top_level_arrays(anon):
    for route in ("/case-studies", "/case-studies/kestra-care/related"):
        response = anon.get(route)
        assert response.status_code == 200, (
            f"the list endpoint {route} must answer: " + conftest.describe(response))
        assert isinstance(response.json(), list), (
            f"the list endpoint {route} must return a top-level JSON array: "
            + conftest.describe(response))


def test_unknown_address_answers_not_found(site_direct):
    page = site_direct.get(f"/no-such-page-{conftest.unique_token()}")
    assert page.status_code == 404, (
        "an unknown address must answer the site's own not-found page with a "
        "not-found status: " + conftest.describe(page))


def test_discipline_filter_returns_only_systems_work(anon):
    response = anon.get("/case-studies", params={"discipline": "systems"})
    assert response.status_code == 200, (
        "the listing must accept a discipline filter: " + conftest.describe(response))
    rows = _shapes.items(response.json())
    seeded = conftest.seeded_subsequence(conftest.slugs_of(rows))
    assert sorted(seeded) == sorted(conftest.SYSTEMS_SLUGS), (
        f"filtering on systems must keep exactly {conftest.SYSTEMS_SLUGS} among the "
        f"seeded case studies; the listing carried {seeded}")
    for row in rows:
        assert "systems" in [str(d) for d in row.get("disciplines") or []], (
            f"every row under the systems filter must carry systems; {row} does not")


def test_selected_filters_combine_with_and(anon):
    response = anon.get("/case-studies", params={
        "client": "verity-biotics", "discipline": "product"})
    assert response.status_code == 200, conftest.describe(response)
    seeded = conftest.seeded_subsequence(conftest.slugs_of(response.json()))
    assert sorted(seeded) == sorted(conftest.VERITY_PRODUCT_SLUGS), (
        "a case study is listed only when it carries every selected client and every "
        f"selected discipline, so verity-biotics with product yields "
        f"{conftest.VERITY_PRODUCT_SLUGS}; the listing carried {seeded}")


def test_default_sort_is_newest_first_with_title_ties(anon):
    response = anon.get("/case-studies")
    seeded = conftest.seeded_subsequence(conftest.slugs_of(response.json()))
    assert seeded == list(conftest.YEAR_DESC_ORDER), (
        "the default order is newest first with year ties by index title A to Z; "
        f"expected {list(conftest.YEAR_DESC_ORDER)}, the listing carried {seeded}")


def test_oldest_first_sort_orders_by_year_ascending(anon):
    response = anon.get("/case-studies", params={"sort": "year-asc"})
    assert response.status_code == 200, conftest.describe(response)
    seeded = conftest.seeded_subsequence(conftest.slugs_of(response.json()))
    assert seeded == list(conftest.YEAR_ASC_ORDER), (
        "year-asc orders oldest first with year ties by index title A to Z; "
        f"expected {list(conftest.YEAR_ASC_ORDER)}, the listing carried {seeded}")


def test_by_name_sort_ignores_letter_case(anon):
    response = anon.get("/case-studies", params={"sort": "title-asc"})
    assert response.status_code == 200, conftest.describe(response)
    seeded = conftest.seeded_subsequence(conftest.slugs_of(response.json()))
    assert seeded == list(conftest.TITLE_ASC_ORDER), (
        "title-asc orders by index title A to Z without regard to case; expected "
        f"{list(conftest.TITLE_ASC_ORDER)}, the listing carried {seeded}")


def test_filters_endpoint_lists_the_published_vocabulary(anon):
    response = anon.get("/filters")
    assert response.status_code == 200, (
        "GET /api/filters must be readable without signing in: "
        + conftest.describe(response))
    body = response.json()
    clients = {str(e.get("token")) for e in body.get("clients") or []}
    disciplines = {str(e.get("token")) for e in body.get("disciplines") or []}
    assert set(conftest.CLIENT_TOKENS) <= clients, (
        f"the filters must offer every client the seeded catalogue carries; got {clients}")
    assert set(conftest.DISCIPLINE_TOKENS) <= disciplines, (
        "the filters must offer every discipline the seeded catalogue carries; got "
        f"{disciplines}")
    for entry in (body.get("clients") or []) + (body.get("disciplines") or []):
        assert entry.get("label"), f"every filter entry carries a label; {entry} does not"


def test_two_clients_together_return_an_empty_list(anon):
    response = anon.get("/case-studies", params={"client": "kestra,quitkit"})
    assert response.status_code == 200, (
        "a filter that matches nothing is an empty result, never an error: "
        + conftest.describe(response))
    assert _shapes.items(response.json()) == [], (
        "every case study has one client, so two clients selected together match "
        f"nothing; the listing carried {conftest.slugs_of(response.json())}")


def test_work_index_page_shows_the_empty_state(site):
    page = site.get("/work", params={"client": "kestra,quitkit"})
    assert page.status_code == 200, (
        "the work index must render its empty state rather than fail: "
        + conftest.describe(page))
    text = conftest.page_text(page.text)
    assert conftest.EMPTY_STATE_LINE in text, (
        f"the empty work index must say {conftest.EMPTY_STATE_LINE!r}")
    assert "All Work" in text, "the empty work index keeps its heading"


def test_unknown_filter_value_is_dropped(anon):
    response = anon.get("/case-studies", params={
        "client": "no-such-client", "discipline": "systems"})
    assert response.status_code == 200, (
        "an unrecognised filter value is dropped rather than refused: "
        + conftest.describe(response))
    seeded = conftest.seeded_subsequence(conftest.slugs_of(response.json()))
    assert sorted(seeded) == sorted(conftest.SYSTEMS_SLUGS), (
        "dropping the unknown client must leave the systems filter applied; the "
        f"listing carried {seeded}")


def test_work_index_page_reports_an_ignored_parameter(site):
    page = site.get("/work", params={"discipline": "no-such-discipline"})
    assert page.status_code == 200, conftest.describe(page)
    text = conftest.page_text(page.text)
    assert conftest.IGNORED_LINE in text, (
        f"a dropped filter value must be reported with {conftest.IGNORED_LINE!r}")
    for slug in conftest.PUBLISHED_SLUGS:
        assert conftest.INDEX_TITLES[slug] in text, (
            "a malformed filter never empties the index; the page lost "
            f"{conftest.INDEX_TITLES[slug]!r}")


def test_overlong_query_string_is_ignored(anon):
    padding = "x" * (conftest.LONG_QUERY_LIMIT + 20)
    response = anon.get("/case-studies", params={"client": "kestra", "pad": padding})
    assert response.status_code == 200, conftest.describe(response)
    seeded = conftest.seeded_subsequence(conftest.slugs_of(response.json()))
    assert sorted(seeded) == sorted(conftest.PUBLISHED_SLUGS), (
        "a query string longer than 512 characters is ignored entirely, so the full "
        f"published set returns; the listing carried {seeded}")


def test_slot_one_is_the_most_similar_case_study(anon):
    for slug, expected in conftest.SLOT_ONE_EXAMPLES:
        response = anon.get(f"/case-studies/{slug}/related")
        assert response.status_code == 200, conftest.describe(response)
        pair = conftest.slugs_of(response.json())
        assert pair and pair[0] == expected, (
            f"slot one for {slug} is {expected}; the pair carried {pair}")


def test_suggestion_pair_is_two_other_published_case_studies(anon):
    listing, graph = _related_graph(anon)
    for slug, pair in graph.items():
        assert len(pair) == 2, f"{slug} must offer exactly two suggestions, not {pair}"
        assert len(set(pair)) == 2, f"{slug}'s two suggestions must differ: {pair}"
        assert slug not in pair, f"{slug} must never suggest itself: {pair}"
        for other in pair:
            assert other in listing, (
                f"{slug} suggested {other}, which is not a published case study")


def test_every_case_study_is_within_four_suggestion_hops(anon):
    listing, graph = _related_graph(anon)
    for start in listing:
        reach = _hops_within(graph, start, 4)
        missing = [s for s in listing if s not in reach]
        assert not missing, (
            f"from {start}, every published case study must be reachable in at most "
            f"four suggestion hops; unreachable: {missing}")


def test_every_published_case_study_is_suggested_somewhere(anon):
    listing, graph = _related_graph(anon)
    offered = {s for pair in graph.values() for s in pair}
    unsuggested = [s for s in listing if s not in offered]
    assert not unsuggested, (
        f"no published case study may go unsuggested; unsuggested: {unsuggested}")


def test_designer_creates_a_case_study_stored_as_a_draft(designer, anon, backend):
    slug = conftest.probe_slug("probe-draft")
    created = conftest.create_case_study(designer, slug)
    row = _case_study_row(backend, slug)
    assert str(row["id"]) == str(conftest.ident(created)), (
        "the created case study's id must be the stored row's id")
    assert not row.get("published"), (
        f"a new case study must be stored as a draft; the row carried "
        f"published={row.get('published')!r}")
    assert row.get("published_at") in (None, ""), (
        "a draft carries no published time; the row carried "
        f"published_at={row.get('published_at')!r}")
    public = anon.get(f"/case-studies/{slug}")
    assert public.status_code == 404, (
        "a new draft must answer not-found to a signed-out reader: "
        + conftest.describe(public))
    bare_slug = conftest.probe_slug("probe-bare")
    bare = conftest.case_study_body(bare_slug)
    bare.pop("home_placement")
    bare.pop("position")
    response = designer.post("/studio/case-studies", json=bare)
    assert response.status_code in (200, 201), (
        "a create with no placement or position must succeed: " + conftest.describe(response))
    placed = _case_study_row(backend, bare_slug)
    assert str(placed.get("home_placement")) == "list", (
        f"home_placement defaults to list; the row carried {placed.get('home_placement')!r}")
    assert placed.get("position") is not None, "position defaults to after the last one"
    edited = designer.patch(f"/studio/case-studies/{conftest.ident(created)}",
                            json={"summary": "An edited probe summary."})
    assert edited.status_code in (200, 201), (
        "editing a draft's summary as the designer should succeed: "
        + conftest.describe(edited))
    assert str(_case_study_row(backend, slug).get("summary")) == "An edited probe summary.", (
        "the edited summary must be stored")


def test_publish_makes_the_case_study_readable_in_one_act(designer, anon, site, store):
    slug = conftest.probe_slug("probe-published")
    created = conftest.publishable_case_study(designer, slug)
    cid = conftest.ident(created)
    try:
        assert anon.get(f"/case-studies/{slug}").status_code == 404, (
            "the probe must be unreachable before publication")
        response = conftest.publish(designer, cid)
        assert response.status_code in (200, 201), (
            "publishing a complete case study should succeed: "
            + conftest.describe(response))
        assert slug in conftest.slugs_of(anon.get("/case-studies").json()), (
            "publishing must add the case study to the public listing")
        detail = anon.get(f"/case-studies/{slug}")
        assert detail.status_code == 200, (
            "publishing must make the case study readable: " + conftest.describe(detail))
        page = site.get(f"/{slug}")
        assert page.status_code == 200, (
            "publishing must make the case study's own address answer: "
            + conftest.describe(page))
        media = [m for m in detail.json().get("media") or [] if m.get("role") == "hero"]
        assert media, "a published case study's detail must list its hero image"
        served = anon.get(f"/media/{media[0]['id']}")
        assert served.status_code in (200, 302, 307), (
            "a published case study's hero bytes must be served to anyone: "
            + conftest.describe(served))
    finally:
        conftest.unpublish(designer, cid)


def test_published_case_study_appears_on_the_home_page(designer, site):
    slug = conftest.probe_slug("probe-home")
    created = conftest.publishable_case_study(designer, slug)
    cid = conftest.ident(created)
    title = f"Probe Index {slug}"
    try:
        before = conftest.page_text(site.get("/").text)
        assert title not in before, "a draft's index title must be absent from the home page"
        conftest.publish(designer, cid)
        after = conftest.page_text(site.get("/").text)
        assert title in after, (
            "publishing a list-placed case study must add it to the home work list")
        listing = conftest.page_text(site.get("/work").text)
        assert title in listing, "publishing must add the case study to /work"
    finally:
        conftest.unpublish(designer, cid)
    gone = conftest.page_text(site.get("/").text)
    assert title not in gone, (
        "withdrawing must remove the case study from the home work list")


def test_published_at_is_stamped_on_publish_and_cleared_on_withdraw(designer, backend):
    slug = conftest.probe_slug("probe-stamped")
    created = conftest.publishable_case_study(designer, slug)
    cid = conftest.ident(created)
    conftest.publish(designer, cid)
    row = _case_study_row(backend, slug)
    assert row.get("published") and row.get("published_at") not in (None, ""), (
        "publishing must set published and stamp published_at; the row carried "
        f"published={row.get('published')!r}, published_at={row.get('published_at')!r}")
    conftest.unpublish(designer, cid)
    row = _case_study_row(backend, slug)
    assert not row.get("published") and row.get("published_at") in (None, ""), (
        "withdrawing must clear published and published_at; the row carried "
        f"published={row.get('published')!r}, published_at={row.get('published_at')!r}")


def test_withdraw_removes_the_case_study_from_every_public_read(designer, anon, site):
    slug = conftest.probe_slug("probe-withdrawn")
    created = conftest.publishable_case_study(designer, slug)
    cid = conftest.ident(created)
    conftest.publish(designer, cid)
    detail = anon.get(f"/case-studies/{slug}")
    assert detail.status_code == 200, "the probe must be readable once published"
    hero = [m for m in detail.json().get("media") or [] if m.get("role") == "hero"]
    response = conftest.unpublish(designer, cid)
    assert response.status_code in (200, 201, 204), (
        "withdrawing a case study should succeed: " + conftest.describe(response))
    assert slug not in conftest.slugs_of(anon.get("/case-studies").json()), (
        "withdrawing must remove the case study from the public listing")
    assert anon.get(f"/case-studies/{slug}").status_code == 404, (
        "withdrawing must make the case study answer not-found")
    assert site.get(f"/{slug}").status_code == 404, (
        "withdrawing must make the case study's own address answer not-found")
    if hero:
        refused = anon.get(f"/media/{hero[0]['id']}")
        assert refused.status_code in (401, 403, 404), (
            "a withdrawn case study's image must stop being served: "
            + conftest.describe(refused))


def test_designer_reads_a_draft_in_the_studio(designer, backend):
    row = _case_study_row(backend, conftest.DRAFT_SLUG)
    response = designer.get(f"/studio/case-studies/{row['id']}")
    assert response.status_code == 200, (
        "the designer must be able to read the draft in the studio: "
        + conftest.describe(response))
    assert conftest.DRAFT_TITLE.lower() in _shapes.flatten(response.json()), (
        "the studio read must return the draft in full: " + conftest.describe(response))
    assert str(row.get("template")) == "product", f"the draft is a product case study: {row}"
    assert str(row.get("home_placement")) == "list", f"the draft sits in the list: {row}"
    anchors = sorted(str(r.get("anchor")) for r in backend.rows("chapters", case_study_id=row["id"]))
    assert anchors == list(conftest.DRAFT_CHAPTERS), (
        f"the draft carries chapters s1 to s3; the rows carried {anchors}")
    listing = designer.get("/studio/case-studies")
    assert listing.status_code == 200, conftest.describe(listing)
    for field in ("id", "slug", "index_title", "published"):
        assert field in (listing.json() or [{}])[0], (
            f"each studio list entry must carry {field}: " + conftest.describe(listing))
    entry = conftest.entry_for(listing.json(), conftest.DRAFT_SLUG)
    assert entry is not None and not entry.get("published"), (
        "the studio list must carry the draft marked unpublished: "
        + conftest.describe(listing))


def test_draft_page_answers_not_found_without_naming_it(anon, reader, site_direct):
    for label, client in (("a signed-out reader", anon), ("a reader", reader)):
        response = client.get(f"/case-studies/{conftest.DRAFT_SLUG}")
        assert response.status_code == 404, (
            f"the draft must answer not-found to {label} at the API: "
            + conftest.describe(response))
    page = site_direct.get(f"/{conftest.DRAFT_SLUG}")
    assert page.status_code == 404, (
        "the draft's address must answer not-found: " + conftest.describe(page))
    assert conftest.DRAFT_TITLE not in conftest.page_text(page.text), (
        "the not-found page must never name the draft: " + conftest.describe(page))
    other = f"no-such-page-{conftest.unique_token()}"
    unknown = site_direct.get(f"/{other}")
    assert unknown.status_code == page.status_code, conftest.describe(unknown)
    assert (conftest.visible_text(page.text, conftest.DRAFT_SLUG)
            == conftest.visible_text(unknown.text, other)), (
        "the draft's not-found page must read the same as the page for an address "
        "that never existed")


def test_draft_is_absent_from_listings_and_suggestions(anon, site):
    listing, graph = _related_graph(anon)
    assert conftest.DRAFT_SLUG not in listing, "the draft must be absent from the listing"
    for slug, pair in graph.items():
        assert conftest.DRAFT_SLUG not in pair, (
            f"the draft must never be suggested; {slug} offered {pair}")
    work = conftest.page_text(site.get("/work").text)
    assert conftest.DRAFT_TITLE not in work, "the draft must be absent from /work"


def test_draft_media_is_refused_outside_the_studio(anon, reader, designer, backend):
    row = _case_study_row(backend, conftest.DRAFT_SLUG)
    media = backend.one("media", case_study_id=row["id"], role="hero")
    assert media is not None, "the seeded draft must carry a stored hero image row"
    for label, client in (("a signed-out reader", anon), ("a reader", reader)):
        response = client.get(f"/media/{media['id']}")
        assert response.status_code in (401, 403, 404), (
            f"the draft's image must be refused to {label}: " + conftest.describe(response))
    allowed = designer.get(f"/media/{media['id']}")
    assert allowed.status_code in (200, 302, 307), (
        "the draft's image must be readable by the designer: "
        + conftest.describe(allowed))


def test_uploaded_image_lands_in_the_bucket(designer, store):
    slug = conftest.probe_slug("probe-stored")
    created = conftest.create_case_study(designer, slug)
    cid = conftest.ident(created)
    payload, response = conftest.upload_media(designer, cid, alt_text="Probe hero.")
    assert response.status_code in (200, 201), (
        "uploading a hero image as the designer should succeed: "
        + conftest.describe(response))
    key = conftest.expected_object_key(cid, payload, "image/png")
    found = conftest.poll_until(lambda: store.exists(key))
    assert found, (
        f"the uploaded image must land in the object store bucket at {key}; the "
        f"bucket held {store.list(f'case-studies/{cid}/')[:20]}")


def test_object_key_follows_the_scheme(designer, backend, store):
    slug = conftest.probe_slug("probe-keyed")
    created = conftest.create_case_study(designer, slug)
    cid = conftest.ident(created)
    payload, response = conftest.upload_media(designer, cid, alt_text="Probe keyed.")
    expected = conftest.expected_object_key(cid, payload, "image/png")
    body = response.json()
    assert str(body.get("object_key")) == expected, (
        "the upload response must carry the object key "
        f"case-studies/{{case_study_id}}/{{sha256}}.png, expected {expected}: "
        + conftest.describe(response))
    row = backend.one("media", case_study_id=cid, role="hero")
    assert row is not None and str(row.get("object_key")) == expected, (
        f"the stored media row must record the key {expected}; it carried {row}")
    assert store.exists(expected), f"the bucket must hold the object at {expected}"


def test_identical_bytes_resolve_to_one_object(designer, store):
    slug = conftest.probe_slug("probe-deduped")
    created = conftest.create_case_study(designer, slug)
    cid = conftest.ident(created)
    payload = conftest.probe_bytes()
    conftest.upload_media(designer, cid, role="hero", payload=payload,
                          alt_text="Probe first.")
    conftest.upload_media(designer, cid, role="still", payload=payload,
                          alt_text="Probe second.")
    key = conftest.expected_object_key(cid, payload, "image/png")
    keys = [k for k in store.list(f"case-studies/{cid}/") if k == key]
    assert len(keys) == 1, (
        f"two uploads of identical bytes must resolve to one object; the bucket held {keys}")


def test_second_hero_image_replaces_the_first(designer, backend):
    slug = conftest.probe_slug("probe-rehero")
    created = conftest.create_case_study(designer, slug)
    cid = conftest.ident(created)
    conftest.upload_media(designer, cid, alt_text="Probe first hero.")
    _, response = conftest.upload_media(designer, cid, alt_text="Probe second hero.")
    assert response.status_code in (200, 201), conftest.describe(response)
    heroes = backend.rows("media", case_study_id=cid, role="hero")
    assert len(heroes) == 1, (
        f"a case study carries at most one hero image; the store held {len(heroes)}")
    assert str(heroes[0].get("alt_text")) == "Probe second hero.", (
        "the newer hero must replace the older one; the stored row carried "
        f"alt_text={heroes[0].get('alt_text')!r}")


def test_media_row_records_role_dimensions_and_digest(designer, backend):
    slug = conftest.probe_slug("probe-measured")
    created = conftest.create_case_study(designer, slug)
    cid = conftest.ident(created)
    payload, _ = conftest.upload_media(designer, cid, role="still",
                                       alt_text="Probe measured.")
    row = backend.one("media", case_study_id=cid, role="still")
    assert row is not None, "the uploaded still must be stored as a media row"
    assert int(row.get("width") or 0) == 1600 and int(row.get("height") or 0) == 900, (
        "a media row records the intrinsic width and height it was given; the row "
        f"carried width={row.get('width')!r}, height={row.get('height')!r}")
    assert str(row.get("sha256")) == conftest.sha256_hex(payload), (
        f"a media row records the sha256 of its bytes; the row carried {row.get('sha256')!r}")
    assert str(row.get("content_type")) == "image/png", (
        f"a media row records its content type; the row carried {row.get('content_type')!r}")
    assert str(row.get("alt_text")) == "Probe measured.", (
        f"a media row records its alternative text; the row carried {row.get('alt_text')!r}")


def test_seeded_hero_images_are_stored_in_the_bucket(backend, store):
    for slug in (conftest.DRAFT_SLUG, "kestra-care", "quitkit"):
        row = _case_study_row(backend, slug)
        media = backend.one("media", case_study_id=row["id"], role="hero")
        assert media is not None, f"the seeded case study {slug} must carry a hero row"
        key = str(media.get("object_key"))
        assert key.startswith(f"case-studies/{row['id']}/"), (
            f"the seeded hero key must follow the scheme; {slug} carried {key}")
        assert store.exists(key), f"the seeded hero for {slug} must be in the bucket at {key}"
        assert str(media.get("alt_text")) == str(row.get("index_title")), (
            f"a generated hero's alternative text is the index title; {slug} carried "
            f"{media.get('alt_text')!r}")


def test_publish_is_refused_without_a_hero_image(designer, backend):
    slug = conftest.probe_slug("probe-noimage")
    created = conftest.create_case_study(designer, slug)
    cid = conftest.ident(created)
    conftest.add_chapter(designer, cid, "s1")
    response = conftest.publish(designer, cid)
    assert 400 <= response.status_code < 500, (
        "publishing a case study with no hero image must be refused: "
        + conftest.describe(response))
    assert str(response.json().get("field")) == conftest.PUBLISH_REFUSAL_FIELDS["hero"], (
        "the refusal must name the missing hero: " + conftest.describe(response))
    assert not _case_study_row(backend, slug).get("published"), (
        "a refused publish must leave the case study a draft")


def test_publish_is_refused_when_media_has_no_alt_text(designer, backend):
    slug = conftest.probe_slug("probe-unlabelled")
    created = conftest.create_case_study(designer, slug)
    cid = conftest.ident(created)
    conftest.add_chapter(designer, cid, "s1")
    conftest.upload_media(designer, cid, role="hero", alt_text="Probe labelled hero.")
    conftest.upload_media(designer, cid, role="still", alt_text="")
    response = conftest.publish(designer, cid)
    assert 400 <= response.status_code < 500, (
        "publishing a case study whose media lacks alternative text must be refused: "
        + conftest.describe(response))
    assert str(response.json().get("field")) == conftest.PUBLISH_REFUSAL_FIELDS["alt_text"], (
        "the refusal must name the missing alternative text: " + conftest.describe(response))
    assert not _case_study_row(backend, slug).get("published"), (
        "a refused publish must leave the case study a draft")


def test_publish_is_refused_for_a_product_case_study_with_no_chapter(designer, backend):
    slug = conftest.probe_slug("probe-nochapter")
    created = conftest.create_case_study(designer, slug)
    cid = conftest.ident(created)
    conftest.upload_media(designer, cid, alt_text="Probe hero.")
    response = conftest.publish(designer, cid)
    assert 400 <= response.status_code < 500, (
        "publishing a product case study with no chapter must be refused: "
        + conftest.describe(response))
    assert str(response.json().get("field")) == conftest.PUBLISH_REFUSAL_FIELDS["chapters"], (
        "the refusal must name the missing chapters: " + conftest.describe(response))
    assert not _case_study_row(backend, slug).get("published"), (
        "a refused publish must leave the case study a draft")


def test_reserved_slug_is_refused_with_the_field_named(designer, backend):
    before = backend.count("case_studies", slug=conftest.RESERVED_SLUG)
    response = designer.post("/studio/case-studies",
                             json=conftest.case_study_body(conftest.RESERVED_SLUG))
    assert 400 <= response.status_code < 500, (
        "a case study slug that is one of the site's own words must be refused: "
        + conftest.describe(response))
    assert str(response.json().get("field")) == "slug", (
        "the refusal must name the slug field: " + conftest.describe(response))
    assert backend.count("case_studies", slug=conftest.RESERVED_SLUG) == before, (
        "a refused create must write no row")


def test_duplicate_slug_is_refused(designer, backend):
    slug = conftest.probe_slug("probe-twice")
    conftest.create_case_study(designer, slug)
    response = designer.post("/studio/case-studies", json=conftest.case_study_body(slug))
    assert 400 <= response.status_code < 500, (
        "a second case study with an existing slug must be refused: "
        + conftest.describe(response))
    assert backend.count("case_studies", slug=slug) == 1, (
        "a refused duplicate must leave exactly one row for the slug")


def test_invalid_client_is_refused_with_the_field_named(designer, backend):
    slug = conftest.probe_slug("probe-badclient")
    response = designer.post("/studio/case-studies",
                             json=conftest.case_study_body(slug, client="no-such-client"))
    assert 400 <= response.status_code < 500, (
        "a client outside the five tokens must be refused: " + conftest.describe(response))
    assert str(response.json().get("field")) == "client", (
        "the refusal must name the client field: " + conftest.describe(response))
    assert backend.count("case_studies", slug=slug) == 0, "a refused create writes no row"


def test_duplicate_chapter_anchor_is_refused(designer, backend):
    slug = conftest.probe_slug("probe-anchor")
    created = conftest.create_case_study(designer, slug)
    cid = conftest.ident(created)
    conftest.add_chapter(designer, cid, "s1")
    response = designer.post(f"/studio/case-studies/{cid}/chapters", json={
        "anchor": "s1", "rail_label": "Again", "heading": "Again",
        "body": "A second chapter with the same anchor."})
    assert 400 <= response.status_code < 500, (
        "a second chapter with an existing anchor must be refused: "
        + conftest.describe(response))
    assert backend.count("chapters", case_study_id=cid) == 1, (
        "a refused chapter writes no row")


def test_unsupported_upload_type_is_rejected(designer, backend, store):
    slug = conftest.probe_slug("probe-badtype")
    created = conftest.create_case_study(designer, slug)
    cid = conftest.ident(created)
    _, response = conftest.upload_media(designer, cid, role="still",
                                        payload=b"plain text, not an image",
                                        alt_text="Probe text.",
                                        content_type="text/plain",
                                        filename="probe.txt")
    assert 400 <= response.status_code < 500, (
        "an upload that is neither an accepted image nor an mp4 reel must be rejected: "
        + conftest.describe(response))
    assert backend.count("media", case_study_id=cid) == 0, "a rejected upload writes no row"
    assert store.list(f"case-studies/{cid}/") == [], "a rejected upload stores no object"


def test_saved_case_study_is_stored_on_the_reading_list(fresh_reader, backend):
    response = fresh_reader.post("/reading-list", json={"slug": "foundry-dashboard"})
    assert response.status_code in (200, 201), (
        "saving a published case study should succeed: " + conftest.describe(response))
    account = _account_id(backend, fresh_reader.probe_email)
    study = _case_study_row(backend, "foundry-dashboard")
    row = backend.one("reading_list", account_id=account, case_study_id=study["id"])
    assert row is not None, "the saved case study must be stored as a reading_list row"
    listing = fresh_reader.get("/reading-list")
    entry = conftest.entry_for(listing.json(), "foundry-dashboard")
    assert entry is not None, (
        "the saved case study must appear on the reader's list: "
        + conftest.describe(listing))
    missing = [f for f in conftest.ENTRY_FIELDS if f not in entry]
    assert not missing, f"a reading list entry must carry {missing}: {entry}"


def test_saving_twice_leaves_one_entry(fresh_reader, backend):
    for _ in range(2):
        fresh_reader.post("/reading-list", json={"slug": "aging-model"})
    account = _account_id(backend, fresh_reader.probe_email)
    study = _case_study_row(backend, "aging-model")
    count = backend.count("reading_list", account_id=account, case_study_id=study["id"])
    assert count == 1, f"saving the same case study twice must leave one row, not {count}"


def test_furthest_point_never_decreases(fresh_reader):
    fresh_reader.post("/reading-list", json={"slug": "kestra-home"})
    first = fresh_reader.put("/reading-list/kestra-home/progress",
                             json={"fraction": 0.6, "chapters": ["s1"]})
    assert first.status_code in (200, 201), conftest.describe(first)
    second = fresh_reader.put("/reading-list/kestra-home/progress",
                              json={"fraction": 0.3, "chapters": ["s1"]})
    assert second.status_code in (200, 201), conftest.describe(second)
    entry = conftest.entry_for(fresh_reader.get("/reading-list").json(), "kestra-home")
    assert conftest.as_float(entry.get("max_fraction")) == 0.6, (
        f"max_fraction never goes down; the entry carried {entry}")
    assert conftest.as_float(entry.get("last_fraction")) == 0.3, (
        f"last_fraction records where the reader left, even lower; the entry carried {entry}")


def test_chapters_read_only_grow(fresh_reader):
    fresh_reader.post("/reading-list", json={"slug": "kestra-home"})
    fresh_reader.put("/reading-list/kestra-home/progress",
                     json={"fraction": 0.4, "chapters": ["s1", "s2", "s3"]})
    fresh_reader.put("/reading-list/kestra-home/progress",
                     json={"fraction": 0.2, "chapters": ["s1"]})
    entry = conftest.entry_for(fresh_reader.get("/reading-list").json(), "kestra-home")
    got = set(conftest.as_list(entry.get("chapters_read")))
    assert {"s1", "s2", "s3"} <= got, (
        f"chapters_read never loses an anchor; the entry carried {entry}")


def test_completed_turns_true_at_the_threshold(fresh_reader):
    fresh_reader.post("/reading-list", json={"slug": "quitkit"})
    fresh_reader.put("/reading-list/quitkit/progress", json={"fraction": 0.94, "chapters": []})
    entry = conftest.entry_for(fresh_reader.get("/reading-list").json(), "quitkit")
    assert entry.get("completed") in (False, 0, None), (
        f"below 0.95 the entry is not completed; it carried {entry}")
    fresh_reader.put("/reading-list/quitkit/progress", json={"fraction": 0.95, "chapters": []})
    fresh_reader.put("/reading-list/quitkit/progress", json={"fraction": 0.1, "chapters": []})
    entry = conftest.entry_for(fresh_reader.get("/reading-list").json(), "quitkit")
    assert entry.get("completed") in (True, 1), (
        f"completed is true once max_fraction reaches 0.95; the entry carried {entry}")


def test_removing_an_entry_deletes_it(fresh_reader, backend):
    fresh_reader.post("/reading-list", json={"slug": "dusk-ritual"})
    response = fresh_reader.delete("/reading-list/dusk-ritual")
    assert response.status_code in (200, 202, 204), (
        "removing a saved case study should succeed: " + conftest.describe(response))
    assert conftest.entry_for(fresh_reader.get("/reading-list").json(), "dusk-ritual") is None, (
        "a removed case study must leave the reader's list")
    account = _account_id(backend, fresh_reader.probe_email)
    study = _case_study_row(backend, "dusk-ritual")
    assert backend.count("reading_list", account_id=account, case_study_id=study["id"]) == 0, (
        "a removed entry must leave no reading_list row")


def test_seeded_reading_list_entry_is_stored(backend):
    account = _account_id(backend, conftest.READER_EMAIL)
    study = _case_study_row(backend, conftest.SEEDED_ENTRY_SLUG)
    row = backend.one("reading_list", account_id=account, case_study_id=study["id"])
    assert row is not None, "reader@example.com must have kestra-care saved"
    assert conftest.as_float(row.get("max_fraction")) >= conftest.SEEDED_MAX_FRACTION, (
        f"the seeded furthest point is 0.4 and can only grow; the row carried {row}")
    assert set(conftest.SEEDED_CHAPTERS) <= set(conftest.as_list(row.get("chapters_read"))), (
        f"the seeded entry has read s1 and s2; the row carried {row}")
    assert row.get("last_seen") is not None, f"the seeded entry carries a last_seen: {row}"
    assert conftest.seconds_ago(row["last_seen"]) > conftest.RESUME_AWAY_SECONDS, (
        f"the seeded last_seen is a day before first start; the row carried {row}")
    other = _account_id(backend, conftest.READER2_EMAIL)
    assert backend.count("reading_list", account_id=other, case_study_id=study["id"]) == 0, (
        "reader2@example.com is seeded with nothing saved, so no kestra-care entry "
        "belongs to that account")


def test_chapter_change_discards_stored_positions(designer, fresh_reader, backend):
    slug = conftest.probe_slug("probe-rechapter")
    created = conftest.publishable_case_study(designer, slug)
    cid = conftest.ident(created)
    try:
        conftest.publish(designer, cid)
        saved = fresh_reader.post("/reading-list", json={"slug": slug})
        assert saved.status_code in (200, 201), conftest.describe(saved)
        fresh_reader.put(f"/reading-list/{slug}/progress",
                         json={"fraction": 0.8, "chapters": ["s1"]})
        conftest.add_chapter(designer, cid, "s2")
        entry = conftest.entry_for(fresh_reader.get("/reading-list").json(), slug)
        assert entry is not None, "the probe must still be on the reader's list"
        assert conftest.as_float(entry.get("last_fraction")) is None, (
            f"a chapter change empties last_fraction; the entry carried {entry}")
        assert conftest.as_list(entry.get("chapters_read")) == [], (
            f"a chapter change empties chapters_read; the entry carried {entry}")
        assert conftest.as_float(entry.get("max_fraction")) == conftest.RESET_CAP, (
            f"a chapter change caps max_fraction at 0.5; the entry carried {entry}")
        account = _account_id(backend, fresh_reader.probe_email)
        row = backend.one("reading_list", account_id=account, case_study_id=cid)
        assert conftest.as_float(row.get("max_fraction")) == conftest.RESET_CAP, (
            f"the stored row must carry the capped max_fraction; it carried {row}")
        added = backend.one("chapters", case_study_id=cid, anchor="s2")
        assert added is not None, "the added chapter s2 must be stored"
        removed = designer.delete(f"/studio/chapters/{added['id']}")
        assert removed.status_code in (200, 202, 204), (
            "removing a chapter as the designer should succeed: "
            + conftest.describe(removed))
        assert backend.count("chapters", case_study_id=cid) == 1, (
            "the removed chapter must leave no row")
    finally:
        conftest.unpublish(designer, cid)


def test_withdrawn_case_study_leaves_every_reading_list(designer, fresh_reader):
    slug = conftest.probe_slug("probe-leaving")
    created = conftest.publishable_case_study(designer, slug)
    cid = conftest.ident(created)
    conftest.publish(designer, cid)
    fresh_reader.post("/reading-list", json={"slug": slug})
    assert conftest.entry_for(fresh_reader.get("/reading-list").json(), slug) is not None, (
        "the published probe must be saved first")
    conftest.unpublish(designer, cid)
    assert conftest.entry_for(fresh_reader.get("/reading-list").json(), slug) is None, (
        "withdrawing a case study removes it from every reading list read")


def test_saving_a_draft_is_refused(fresh_reader, backend):
    response = fresh_reader.post("/reading-list", json={"slug": conftest.DRAFT_SLUG})
    assert 400 <= response.status_code < 500, (
        "saving a draft to a reading list must be refused: " + conftest.describe(response))
    account = _account_id(backend, fresh_reader.probe_email)
    assert backend.count("reading_list", account_id=account) == 0, (
        "a refused save writes no row")


def test_out_of_range_fraction_is_rejected(fresh_reader):
    fresh_reader.post("/reading-list", json={"slug": "mirror-lab"})
    fresh_reader.put("/reading-list/mirror-lab/progress",
                     json={"fraction": 0.2, "chapters": ["s1"]})
    response = fresh_reader.put("/reading-list/mirror-lab/progress",
                                json={"fraction": 1.5, "chapters": ["s1"]})
    assert 400 <= response.status_code < 500, (
        "a fraction outside 0 to 1 must be rejected: " + conftest.describe(response))
    entry = conftest.entry_for(fresh_reader.get("/reading-list").json(), "mirror-lab")
    assert conftest.as_float(entry.get("max_fraction")) == 0.2, (
        f"a rejected progress write changes nothing; the entry carried {entry}")


def test_unknown_chapter_in_progress_is_rejected(fresh_reader):
    fresh_reader.post("/reading-list", json={"slug": "mirror-lab"})
    response = fresh_reader.put("/reading-list/mirror-lab/progress",
                                json={"fraction": 0.3, "chapters": ["s99"]})
    assert 400 <= response.status_code < 500, (
        "a progress write naming a chapter the case study lacks must be rejected: "
        + conftest.describe(response))
    entry = conftest.entry_for(fresh_reader.get("/reading-list").json(), "mirror-lab")
    assert "s99" not in conftest.as_list(entry.get("chapters_read")), (
        f"a rejected progress write changes nothing; the entry carried {entry}")


def test_progress_for_an_unsaved_case_study_is_refused(fresh_reader):
    response = fresh_reader.put("/reading-list/verity-biotics-brand/progress",
                                json={"fraction": 0.3, "chapters": []})
    assert 400 <= response.status_code < 500, (
        "progress for a case study not on the list must be refused: "
        + conftest.describe(response))
    assert conftest.entry_for(fresh_reader.get("/reading-list").json(),
                              "verity-biotics-brand") is None, (
        "a refused progress write must not create an entry")


def test_reader_is_forbidden_the_publish_endpoint(reader, backend):
    row = _case_study_row(backend, conftest.DRAFT_SLUG)
    response = reader.post(f"/studio/case-studies/{row['id']}/publish")
    assert response.status_code in (401, 403, 404), (
        "a reader must be refused the publish endpoint: " + conftest.describe(response))
    after = _case_study_row(backend, conftest.DRAFT_SLUG)
    assert not after.get("published"), (
        "a refused publish must leave the draft unpublished")


def test_reader_is_forbidden_the_studio_list_and_writes(reader, backend):
    before = backend.count("case_studies")
    listing = reader.get("/studio/case-studies")
    assert listing.status_code in (401, 403), (
        "a reader must be refused the studio list: " + conftest.describe(listing))
    created = reader.post("/studio/case-studies",
                          json=conftest.case_study_body(conftest.probe_slug("probe-reader")))
    assert created.status_code in (401, 403), (
        "a reader must be refused a studio write: " + conftest.describe(created))
    assert backend.count("case_studies") == before, "a refused studio write writes no row"


def test_reader_cannot_see_another_readers_list(reader, reader2, backend):
    reader.post("/reading-list", json={"slug": "vitality-score"})
    theirs = reader2.get("/reading-list")
    assert theirs.status_code == 200, conftest.describe(theirs)
    assert conftest.entry_for(theirs.json(), "vitality-score") is None, (
        "reader2 must never see reader's saved case studies")
    assert conftest.entry_for(theirs.json(), conftest.SEEDED_ENTRY_SLUG) is None, (
        "reader2 must never see reader's seeded entry")
    reader2.delete(f"/reading-list/{conftest.SEEDED_ENTRY_SLUG}")
    account = _account_id(backend, conftest.READER_EMAIL)
    study = _case_study_row(backend, conftest.SEEDED_ENTRY_SLUG)
    assert backend.count("reading_list", account_id=account, case_study_id=study["id"]) == 1, (
        "a delete from reader2 must leave reader's entry untouched")


def test_preferences_are_private_to_each_account(fresh_reader, reader2):
    before = reader2.get("/preferences")
    assert before.status_code == 200, conftest.describe(before)
    fresh_reader.put("/preferences", json={"motion_level": "reduced"})
    fresh_reader.put("/preferences", json={"reveal_all": True})
    after = reader2.get("/preferences")
    assert after.json() == before.json(), (
        "one reader's preference change must leave another account's preferences "
        f"untouched; reader2 moved from {before.json()} to {after.json()}")
    mine = fresh_reader.get("/preferences").json()
    assert mine.get("motion_level") == "reduced", (
        f"a reader reads back their own choice; the response carried {mine}")


def test_studio_endpoints_are_denied_to_an_unauthenticated_caller(anon, backend):
    row = _case_study_row(backend, conftest.DRAFT_SLUG)
    for method, path in (("GET", "/studio/case-studies"),
                         ("POST", "/studio/case-studies"),
                         ("GET", f"/studio/case-studies/{row['id']}"),
                         ("POST", f"/studio/case-studies/{row['id']}/publish")):
        response = anon.request(method, path, json={})
        assert response.status_code in (401, 403), (
            f"anonymous {method} /api{path} must be denied: " + conftest.describe(response))
    assert not _case_study_row(backend, conftest.DRAFT_SLUG).get("published"), (
        "a denied anonymous publish must leave the draft unpublished")


def test_reading_list_is_denied_to_an_unauthenticated_caller(anon):
    for method, path in (("GET", "/reading-list"), ("POST", "/reading-list"),
                         ("GET", "/preferences"), ("PUT", "/preferences")):
        response = anon.request(method, path, json={"slug": "kestra-care"})
        assert response.status_code in (401, 403), (
            f"anonymous {method} /api{path} must be denied: " + conftest.describe(response))
    stale = anon.post("/reading-list", json={"slug": "kestra-care"},
                      headers={"Authorization": f"Bearer expired-{conftest.unique_token()}"})
    assert stale.status_code in (401, 403), (
        "a request carrying a token the app never issued must be denied and not "
        "applied: " + conftest.describe(stale))


def test_signup_cannot_grant_the_designer_role(backend):
    email_address = conftest.probe_email()
    response = conftest.signup(email_address, role="designer")
    assert response.status_code in (200, 201, 400, 422), (
        "signup must answer rather than fail: " + conftest.describe(response))
    row = backend.one("accounts", email=email_address)
    if row is not None:
        assert str(row.get("role")) == "reader", (
            "a signup always creates a reader whatever the body says; the stored row "
            f"carried role={row.get('role')!r}")


def test_login_with_a_wrong_password_is_denied(anon):
    response = anon.post("/auth/login", json={
        "email": conftest.DESIGNER_EMAIL, "password": "not-the-password-2026"})
    assert response.status_code in (400, 401, 403, 422), (
        "signing in with a wrong password must be denied: " + conftest.describe(response))


def test_me_returns_the_signed_in_account(designer, reader):
    for client, email_address, role in ((designer, conftest.DESIGNER_EMAIL, "designer"),
                                        (reader, conftest.READER_EMAIL, "reader")):
        response = client.get("/me")
        assert response.status_code == 200, conftest.describe(response)
        body = response.json()
        assert str(body.get("email")).lower() == email_address, (
            f"GET /api/me must return the signed-in email; it carried {body}")
        assert str(body.get("role")) == role, (
            f"GET /api/me must return the role {role}; it carried {body}")


def test_reader_chooses_a_motion_level_stored_on_the_account(fresh_reader, backend):
    response = fresh_reader.put("/preferences", json={"motion_level": "still"})
    assert response.status_code in (200, 201), conftest.describe(response)
    body = fresh_reader.get("/preferences").json()
    assert body.get("motion_level") == "still" and body.get("level_source") == "chosen", (
        f"a chosen level is stored with level_source chosen; the response carried {body}")
    account = _account_id(backend, fresh_reader.probe_email)
    row = backend.one("preferences", account_id=account)
    assert row is not None and str(row.get("motion_level")) == "still", (
        f"the chosen level must be stored in preferences; the row carried {row}")


def test_unchosen_preferences_read_back_as_system(fresh_reader):
    body = fresh_reader.get("/preferences").json()
    assert body.get("level_source") == "system", (
        f"a reader who never chose reads back level_source system; got {body}")
    assert body.get("motion_level") in (None, ""), (
        f"a reader who never chose has no stored motion level; got {body}")
    assert body.get("reveal_all") in (False, 0, None), (
        f"reveal-all is off by default; got {body}")


def test_invalid_motion_level_is_rejected(fresh_reader):
    fresh_reader.put("/preferences", json={"motion_level": "reduced"})
    response = fresh_reader.put("/preferences", json={"motion_level": "sideways"})
    assert 400 <= response.status_code < 500, (
        "a motion level outside full, reduced and still must be rejected: "
        + conftest.describe(response))
    body = fresh_reader.get("/preferences").json()
    assert body.get("motion_level") == "reduced", (
        f"a rejected level changes nothing; the response carried {body}")


def test_clearing_the_motion_level_hands_control_back(fresh_reader):
    fresh_reader.put("/preferences", json={"motion_level": "full"})
    response = fresh_reader.put("/preferences", json={"motion_level": None})
    assert response.status_code in (200, 201), conftest.describe(response)
    body = fresh_reader.get("/preferences").json()
    assert body.get("level_source") == "system" and body.get("motion_level") in (None, ""), (
        f"an empty level hands control back to the system; the response carried {body}")


def test_reveal_all_choice_is_stored(fresh_reader):
    response = fresh_reader.put("/preferences", json={"reveal_all": True})
    assert response.status_code in (200, 201), conftest.describe(response)
    body = fresh_reader.get("/preferences").json()
    assert body.get("reveal_all") in (True, 1), (
        f"the reveal-all choice travels with the account; got {body}")


def test_cookie_question_is_shown_until_answered(site_direct):
    first = site_direct.get("/")
    assert conftest.COOKIE_QUESTION in conftest.page_text(first.text), (
        f"a first-time visitor must be asked {conftest.COOKIE_QUESTION!r}")
    answered = site_direct.get("/", cookies={conftest.COOKIE_NAME: "no"})
    assert conftest.COOKIE_QUESTION not in conftest.page_text(answered.text), (
        "once the reading_memory cookie exists the question is not rendered again")


def test_consent_choice_sets_a_lasting_cookie(anon):
    response = anon.post("/consent", json={"choice": "yes"})
    assert response.status_code in (200, 201, 204), conftest.describe(response)
    cookies = [c for c in conftest.set_cookie_headers(response)
               if c.lower().startswith(f"{conftest.COOKIE_NAME}=")]
    assert cookies, (
        "POST /api/consent must set the reading_memory cookie; the response set "
        f"{conftest.set_cookie_headers(response)}")
    assert cookies[0].split(";")[0].split("=", 1)[1].strip().strip('"') == "yes", (
        f"the cookie must hold the chosen answer; it carried {cookies[0]}")
    assert conftest.cookie_lifetime_seconds(cookies[0]) >= conftest.COOKIE_MIN_SECONDS - 86400, (
        f"the reading_memory cookie must last 180 days; it carried {cookies[0]}")


def test_invalid_consent_choice_is_rejected(anon):
    response = anon.post("/consent", json={"choice": "maybe"})
    assert 400 <= response.status_code < 500, (
        "a consent choice other than yes or no must be rejected: "
        + conftest.describe(response))
    assert not [c for c in conftest.set_cookie_headers(response)
                if c.lower().startswith(f"{conftest.COOKIE_NAME}=")], (
        "a rejected consent choice sets no cookie")


def test_privacy_page_states_what_the_site_keeps(site):
    page = site.get(conftest.PRIVACY_ROUTE)
    assert page.status_code == 200, "the privacy page must render: " + conftest.describe(page)
    text = conftest.page_text(page.text)
    assert conftest.PRIVACY_SENTENCE in text, (
        f"the privacy page must say {conftest.PRIVACY_SENTENCE!r}")
    for word in ("email", "password", "reading list", "motion", "tilt", "sort", "view"):
        assert word in text.lower(), f"the privacy page must state what it keeps about {word}"


def test_every_public_page_links_to_privacy(site):
    for route in ("/", "/work", "/verity-biotics-product", "/quitkit"):
        page = site.get(route)
        hrefs = [urllib.parse.urlsplit(h).path for h in conftest.HREF_RE.findall(page.text)]
        assert conftest.PRIVACY_ROUTE in hrefs, (
            f"the public page {route} must link to /privacy from its footer")


def test_internal_links_on_public_pages_resolve(site):
    checked = set()
    for route in conftest.PUBLIC_PAGES:
        page = site.get(route)
        assert page.status_code == 200, conftest.describe(page)
        for href in conftest.HREF_RE.findall(page.text):
            parts = urllib.parse.urlsplit(href)
            if parts.scheme or parts.netloc or href.startswith(("mailto:", "tel:")):
                continue
            if not parts.path and parts.fragment:
                assert conftest.has_anchor(page.text, parts.fragment), (
                    f"the in-page link #{parts.fragment} on {route} must land on an element")
                continue
            if not parts.path.startswith("/") or parts.path in checked:
                continue
            checked.add(parts.path)
            target = site.get(parts.path)
            assert target.status_code < 400, (
                f"the internal link {parts.path} on {route} must resolve: "
                + conftest.describe(target))
            if parts.fragment:
                assert conftest.has_anchor(target.text, parts.fragment), (
                    f"the link {href} on {route} must land on #{parts.fragment}")
    assert checked, "the public pages must carry internal links"


def test_security_headers_are_present_on_every_response(site):
    for route in conftest.HEADER_ROUTES:
        response = site.get(route)
        headers = {k.lower(): v for k, v in response.headers.items()}
        assert "strict-transport-security" in headers, (
            f"{route} must carry a strict transport security header; it carried "
            f"{sorted(headers)}")
        assert headers.get("x-content-type-options", "").lower() == "nosniff", (
            f"{route} must carry X-Content-Type-Options: nosniff; it carried "
            f"{headers.get('x-content-type-options')!r}")


def test_signup_rejects_invalid_input_and_writes_nothing(backend):
    bad_email = f"not-an-email-{conftest.unique_token()}"
    response = conftest.signup(bad_email)
    assert 400 <= response.status_code < 500, (
        "a signup with a malformed email must be rejected: " + conftest.describe(response))
    assert str(response.json().get("field")) == "email", (
        "the refusal must name the email field: " + conftest.describe(response))
    assert backend.count("accounts", email=bad_email) == 0, "a refused signup writes no row"
    short = conftest.probe_email()
    response = conftest.signup(short, password="short")
    assert 400 <= response.status_code < 500, (
        "a signup with a password under 8 characters must be rejected: "
        + conftest.describe(response))
    assert str(response.json().get("field")) == "password", (
        "the refusal must name the password field: " + conftest.describe(response))
    assert backend.count("accounts", email=short) == 0, "a refused signup writes no row"


def test_duplicate_signup_email_is_refused(backend):
    response = conftest.signup(conftest.READER_EMAIL.upper())
    assert 400 <= response.status_code < 500, (
        "a signup with an existing email, in any case, must be refused: "
        + conftest.describe(response))
    rows = [r for r in backend.rows("accounts")
            if str(r.get("email")).lower() == conftest.READER_EMAIL]
    assert len(rows) == 1, f"the email must stay unique without regard to case; found {len(rows)}"


def test_seed_is_idempotent_across_a_restart(backend):
    for slug in conftest.PUBLISHED_SLUGS + (conftest.DRAFT_SLUG,):
        assert backend.count("case_studies", slug=slug) == 1, (
            f"seeding must be idempotent, so {slug} must be stored exactly once")
    for email_address in (conftest.DESIGNER_EMAIL, conftest.READER_EMAIL,
                          conftest.READER2_EMAIL):
        assert backend.count("accounts", email=email_address) == 1, (
            f"the seeded account {email_address} must be stored exactly once")
    draft = _case_study_row(backend, conftest.DRAFT_SLUG)
    assert backend.count("chapters", case_study_id=draft["id"]) == 3, (
        "the seeded draft's three chapters must be stored exactly once")


def test_schema_holds_the_seven_tables_with_opaque_ids(backend):
    for table in conftest.SEVEN_TABLES:
        backend.count(table)
    row = _case_study_row(backend, "kestra-care")
    for derived in ("work_number", "number", "tag_line", "related", "suggestions"):
        assert derived not in row, (
            f"{derived} is derived at read time and never stored; the row carried it")
    assert str(row.get("id")) != "kestra-care", (
        "a case study id is opaque and never derived from the slug")
    account = backend.one("accounts", email=conftest.DESIGNER_EMAIL)
    assert str(account.get("role")) == "designer", (
        f"the seeded designer account carries the role designer; it carried {account}")
    assert "deku-demo-pw-2026" not in str(account.get("password_hash")), (
        "an account row stores a hash, never the password literal")


def test_catalogue_values_are_stored_as_seeded(backend):
    for slug, (client, disciplines, year) in conftest.CATALOGUE.items():
        row = _case_study_row(backend, slug)
        assert str(row.get("client")) == client, (
            f"{slug} is seeded with client {client}; the row carried {row.get('client')!r}")
        assert int(row.get("year")) == year, (
            f"{slug} is seeded with year {year}; the row carried {row.get('year')!r}")
        stored = {str(r.get("discipline"))
                  for r in backend.rows("case_study_disciplines", case_study_id=row["id"])}
        assert stored == set(disciplines), (
            f"{slug} is seeded with disciplines {disciplines}; the rows carried {stored}")
    for slug, (product, year_end, ongoing, template, placement) in conftest.CATALOGUE_DETAIL.items():
        row = _case_study_row(backend, slug)
        assert str(row.get("index_title")) == conftest.INDEX_TITLES[slug], (
            f"{slug} carries its index title; the row carried {row.get('index_title')!r}")
        assert (row.get("product") or None) == product, (
            f"{slug} carries product {product!r}; the row carried {row.get('product')!r}")
        assert (int(row["year_end"]) if row.get("year_end") else None) == year_end, (
            f"{slug} ends {year_end!r}; the row carried {row.get('year_end')!r}")
        assert bool(row.get("ongoing")) is ongoing, (
            f"{slug} ongoing is {ongoing}; the row carried {row.get('ongoing')!r}")
        assert str(row.get("template")) == template, (
            f"{slug} uses the {template} template; the row carried {row.get('template')!r}")
        assert str(row.get("home_placement")) == placement, (
            f"{slug} sits in {placement}; the row carried {row.get('home_placement')!r}")
    kestra = _case_study_row(backend, "kestra-care")
    assert int(kestra.get("year_end")) == 2023, (
        f"kestra-care ends in 2023; the row carried {kestra.get('year_end')!r}")
    assert str(kestra.get("home_placement")) == "featured", (
        f"kestra-care sits in the featured band; the row carried {kestra.get('home_placement')!r}")


def test_browser_downloads_carry_no_server_secret(site):
    page = site.get("/")
    assert page.status_code == 200, conftest.describe(page)
    bodies = [page.text]
    script_bytes = 0
    for src in conftest.SCRIPT_SRC_RE.findall(page.text):
        parts = urllib.parse.urlsplit(src)
        if parts.scheme or parts.netloc:
            continue
        fetched = site.get(parts.path)
        assert fetched.status_code < 400, conftest.describe(fetched)
        script_bytes += len(fetched.content)
        bodies.append(fetched.text)
    for href in conftest.STYLE_HREF_RE.findall(page.text):
        parts = urllib.parse.urlsplit(href)
        if not (parts.scheme or parts.netloc):
            bodies.append(site.get(parts.path).text)
    for name, value in conftest.server_secrets():
        for body in bodies:
            assert value not in body, (
                f"the value of {name} must never appear in anything the browser downloads")
    assert script_bytes < conftest.HOME_SCRIPT_BUDGET, (
        f"script on the home route must stay under {conftest.HOME_SCRIPT_BUDGET} bytes; "
        f"it weighed {script_bytes}")
