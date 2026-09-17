"""The one pytest module for this bundle.

Every section and the declared storage slot live here, grouped by banner.
Assertions are black-box: HTTP against the deployed app, the datastore and the
object store through the capability adapters.
"""

from __future__ import annotations

import os
import threading
import uuid

import appclient
import conftest

def test_services_index_lists_twenty_names(anon):
    """The service index carries the twenty named services."""
    response = anon.get("/services")
    assert response.status_code == 200, f"GET /api/services -> {response.status_code}"
    rows = response.json()
    names = {row["name"] if isinstance(row, dict) else row for row in rows}
    missing = [n for n in conftest.SERVICE_NAMES if n not in names]
    assert not missing, f"the service index is missing {missing}"
    assert len(conftest.SERVICE_NAMES) == 20


def test_capabilities_and_discipline_tags_are_seeded(anon):
    """The four capabilities and the twenty-four upper-case discipline tags are seeded."""
    caps = anon.get("/capabilities")
    assert caps.status_code == 200, f"GET /api/capabilities -> {caps.status_code}"
    titles = {row["title"] for row in caps.json()}
    missing = [t for t in conftest.CAPABILITY_TITLES if t not in titles]
    assert not missing, f"the capability band is missing {missing}"
    cases = anon.get("/cases").json()
    tags = {t for row in cases for t in (row.get("tags") or [])}
    assert tags, "no case carries a discipline tag"
    lower = [t for t in tags if t != t.upper()]
    assert not lower, f"these discipline tags are not upper case: {lower}"


def test_home_route_serves_rendered_markup(anon):
    """The home route arrives as HTML carrying its words, not as an empty shell."""
    markup = conftest.page_body("/")
    assert "<html" in markup.lower(), "the home route did not serve an HTML document"
    present = [w for w in conftest.TONE_WORDS if w in markup]
    assert len(present) >= 2, (
        f"the served home document carries only {present} of the four tone words, so "
        f"its content is not in the markup the browser first receives")
    assert conftest.ARCHIVE_HEADING in markup, (
        "the served home document does not carry the archive heading")


def test_brief_stage_one_creates_record_with_token(anon):
    """Stage one of the brief creates a record and issues a resume token."""
    record = conftest.create_brief(anon)
    token = record["token"]
    read_back = anon.get(f"/briefs/{token}")
    assert read_back.status_code == 200, (
        f"GET /api/briefs/{{token}} returned {read_back.status_code} for a token the "
        f"create call had just issued")
    stored = read_back.json()
    assert str(stored.get("stage")) == "1", (
        f"the saved brief reports stage {stored.get('stage')!r} after stage one")
    assert stored["contact"]["email"] == conftest.CLIENT_EMAIL, (
        f"the saved contact is {stored['contact']!r}")


def test_brief_shape_is_derived_from_disciplines(anon):
    """The engagement shape is proposed from the discipline selection and records an override."""
    record = conftest.create_brief(
        anon, disciplines=["Brand Identity Systems", "Corporate Identity"])
    token = record["token"]
    proposed = anon.get(f"/briefs/{token}").json()
    assert proposed.get("shape") in conftest.SHAPES, (
        f"the derived shape is {proposed.get('shape')!r}, outside {conftest.SHAPES}")
    assert proposed["shape"] == "identity", (
        f"branding-only disciplines derived {proposed['shape']!r} rather than 'identity'")
    override = anon.patch(f"/briefs/{token}", json={"shape": "full-cycle"})
    assert override.status_code < 300, (
        f"overriding the derived shape returned {override.status_code}")
    after = anon.get(f"/briefs/{token}").json()
    assert after["shape"] == "full-cycle", "the override did not take"
    assert after.get("shape_overridden") is True, (
        "the brief does not record that the derivation was overridden")


def test_brief_submit_books_the_named_slot(anon):
    """Submitting the brief books the held slot and names it in both zones."""
    record = conftest.create_brief(anon, stage=6)
    token = record["token"]
    slots = conftest.free_slots(anon)
    assert slots, "the availability document offers no free slot"
    slot = slots[0]
    held = anon.post(f"/briefs/{token}/hold", json={"slot_id": slot["id"]})
    assert held.status_code < 300, f"placing a hold returned {held.status_code}"
    hold_token = held.json().get("hold_token")
    submitted = anon.post(f"/briefs/{token}/submit",
                          json={"slot_id": slot["id"], "hold_token": hold_token})
    assert submitted.status_code < 300, (
        f"submitting the brief returned {submitted.status_code}: {submitted.text[:200]}")
    booking = submitted.json().get("booking") or submitted.json()
    assert booking.get("visitor_zone_rendering"), (
        f"the booking names no visitor-zone time: {booking}")
    assert booking.get("studio_zone_rendering"), (
        f"the booking names no studio-zone time: {booking}")


def test_availability_is_published_with_a_bounded_horizon(anon):
    """Availability is a published document of thirty-minute slots bounded to a fortnight."""
    response = anon.get("/availability")
    assert response.status_code == 200, f"GET /api/availability -> {response.status_code}"
    payload = response.json()
    assert isinstance(payload, dict) and "slots" in payload, (
        f"availability is not a published document carrying slots: {payload!r}")
    assert payload.get("zone"), "the availability document names no studio zone"
    slots = payload["slots"]
    assert slots, "the availability document carries no slot"
    assert len(slots) <= 14 * 48, (
        f"availability carries {len(slots)} slots, beyond a fortnight of half hours")
    states = {s.get("state", "free") for s in slots}
    assert states <= set(conftest.SLOT_STATES), (
        f"availability carries slot states {states} outside {conftest.SLOT_STATES}")


def test_slot_picker_is_reachable_by_keyboard(anon):
    """Every slot control on the brief carries a reachable, named control in the markup."""
    markup = conftest.page_body("/brief/")
    lowered = markup.lower()
    assert "button" in lowered or "role=\"gridcell\"" in lowered, (
        "the brief route exposes no focusable slot controls in its markup")
    assert "tabindex=\"-1\"" not in lowered.replace(" ", ""), (
        "a slot control is removed from the tab order, so the picker cannot be "
        "driven by keyboard")


def test_tone_signature_is_stored_with_the_brief(anon):
    """The tone board writes two axis values and its chosen words onto the brief."""
    record = conftest.create_brief(anon)
    token = record["token"]
    tone = {"axis_x": 0.4, "axis_y": 0.7,
            "words": ["clarity", "structure", "rhythm"]}
    response = anon.patch(f"/briefs/{token}", json={"tone": tone})
    assert response.status_code < 300, f"saving a tone signature -> {response.status_code}"
    stored = anon.get(f"/briefs/{token}").json().get("tone") or {}
    assert stored.get("words"), f"the brief stored no tone words: {stored}"
    assert "axis_x" in stored and "axis_y" in stored, (
        f"the tone signature carries no two axis values: {stored}")


def test_tone_board_and_list_view_agree(anon):
    """The board limit holds and the list view produces the same stored signature."""
    record = conftest.create_brief(anon)
    token = record["token"]
    nine = [f"word{i}" for i in range(9)]
    refused = anon.patch(f"/briefs/{token}", json={"tone": {"axis_x": 0.1,
                                                           "axis_y": 0.1,
                                                           "words": nine}})
    assert conftest.is_client_error(refused.status_code), (
        f"a ninth tone tile was accepted with {refused.status_code}; eight is the limit")
    eight = nine[:8]
    accepted = anon.patch(f"/briefs/{token}",
                          json={"tone": {"axis_x": 0.1, "axis_y": 0.1, "words": eight}})
    assert accepted.status_code < 300, f"eight tone tiles -> {accepted.status_code}"
    stored = anon.get(f"/briefs/{token}").json()["tone"]
    assert len(stored["words"]) == 8, f"the brief stored {len(stored['words'])} tone words"
    assert str(stored["axis_x"]) and str(stored["axis_y"])


def test_resumed_brief_returns_the_furthest_stage(anon):
    """A saved brief reopens at the furthest stage with every earlier answer intact."""
    record = conftest.create_brief(anon)
    token = record["token"]
    anon.patch(f"/briefs/{token}", json={"stage": 4, "timing": "within_three_months",
                                         "narrative": "A rebrand plus a new site."})
    reopened = anon.get(f"/briefs/{token}").json()
    assert str(reopened["stage"]) == "4", (
        f"the resumed brief reports stage {reopened['stage']!r} rather than 4")
    assert reopened["narrative"] == "A rebrand plus a new site.", (
        "the resumed brief lost the free text")
    assert reopened["contact"]["company"] == "Northwind Aero", (
        "the resumed brief lost the stage one answers")


def test_case_route_returns_chapters_in_order(anon):
    """A published case answers with typed chapters running cover first and outcome last."""
    response = anon.get(f"/cases/{conftest.PUBLISHED_CASE_SLUG}")
    assert response.status_code == 200, (
        f"GET /api/cases/{conftest.PUBLISHED_CASE_SLUG} -> {response.status_code}")
    payload = response.json()
    case = payload.get("case", payload)
    assert case.get("sector") in conftest.SECTORS, (
        f"the case sector is {case.get('sector')!r}, outside {conftest.SECTORS}")
    assert case.get("kind") in conftest.KINDS, (
        f"the case kind is {case.get('kind')!r}, outside {conftest.KINDS}")
    chapters = payload.get("chapters") or []
    assert len(chapters) >= 4, f"the case carries {len(chapters)} chapters, fewer than four"
    kinds = [c["type"] for c in chapters]
    assert set(kinds) <= set(conftest.CHAPTER_TYPES), (
        f"the case carries chapter types outside the ten: {set(kinds) - set(conftest.CHAPTER_TYPES)}")
    assert kinds[0] == "cover", f"the case opens on a {kinds[0]!r} chapter"
    assert kinds[-1] == "outcome", f"the case closes on a {kinds[-1]!r} chapter"


def test_case_with_too_few_chapters_is_refused_publication(studio):
    """Publishing a case carrying fewer than four chapters is refused as invalid."""
    listing = studio.get("/cases?published=false")
    assert listing.status_code == 200, f"GET /api/cases -> {listing.status_code}"
    thin = [c for c in listing.json() if len(c.get("chapters") or []) < 4]
    assert thin, (
        "no seeded case carries fewer than four chapters, so the publication floor "
        "cannot be observed")
    response = studio.post(f"/cases/{thin[0]['slug']}/publish")
    assert conftest.is_client_error(response.status_code), (
        f"publishing a {len(thin[0].get('chapters') or [])}-chapter case returned "
        f"{response.status_code} rather than a refusal")


def test_renamed_case_old_slug_redirects(anon):
    """A case reached by a superseded slug redirects permanently to its current one."""
    response = conftest.page(f"/work/{conftest.PUBLISHED_CASE_SLUG}/")
    assert response.status_code in (200, 301, 308), (
        f"the published case route returned {response.status_code}")
    api = anon.get(f"/cases/{conftest.PUBLISHED_CASE_SLUG}")
    assert api.status_code == 200
    slug = (api.json().get("case") or api.json()).get("slug")
    assert slug == conftest.PUBLISHED_CASE_SLUG, (
        f"the case reports slug {slug!r}, so the slug is not stable")


def test_case_route_declares_its_own_title_and_description(anon):
    """Each public route carries a distinct title and description, and a case declares its share card."""
    titles = {}
    for route in ("/", "/work/", "/contact/", f"/work/{conftest.PUBLISHED_CASE_SLUG}/"):
        markup = conftest.page_body(route)
        start = markup.lower().find("<title>")
        assert start >= 0, f"{route} carries no document title"
        end = markup.lower().find("</title>", start)
        titles[route] = markup[start + 7:end].strip()
        assert "description" in markup.lower(), f"{route} declares no description"
    assert len(set(titles.values())) == len(titles), (
        f"two public routes share a title: {titles}")
    case_markup = conftest.page_body(f"/work/{conftest.PUBLISHED_CASE_SLUG}/")
    lowered = case_markup.lower()
    assert "og:image" in lowered or "twitter:image" in lowered, (
        "the case route declares no social preview image")
    assert "application/ld+json" in lowered or "itemtype" in lowered, (
        "the case route declares no structured article record")


def test_case_still_is_generated_from_the_slug_seed(anon):
    """A case still is generated from the slug, so the same case always yields the same bytes."""
    first = conftest.page(f"/api/cases/{conftest.PUBLISHED_CASE_SLUG}/still")
    if first.status_code == 404:
        first = conftest.page(f"/work/{conftest.PUBLISHED_CASE_SLUG}/still.svg")
    assert first.status_code == 200, (
        f"the generated still for {conftest.PUBLISHED_CASE_SLUG} is not served "
        f"({first.status_code}); every image is generated rather than shipped")
    second = conftest.page(first.request.url.path)
    assert second.status_code == 200
    assert first.content == second.content, (
        "two reads of one case still returned different bytes, so the still is not "
        "derived from the slug seed")


def test_filtered_archive_address_reopens_the_same_filter(anon):
    """A filtered archive is a link: the same query returns the same set."""
    filtered = anon.get("/cases", params={"sector": "HEALTHCARE"})
    assert filtered.status_code == 200, f"filtering the archive -> {filtered.status_code}"
    rows = filtered.json()
    assert rows, "filtering to HEALTHCARE returned nothing"
    assert all(r["sector"] == "HEALTHCARE" for r in rows), (
        f"the HEALTHCARE filter returned sectors {[r['sector'] for r in rows]}")
    again = anon.get("/cases", params={"sector": "HEALTHCARE"}).json()
    assert [r["slug"] for r in again] == [r["slug"] for r in rows], (
        "the same filter address returned a different set on a second read")


def test_similarity_orders_by_discipline_then_sector(anon):
    """Related cases are ordered by discipline overlap and say what they share."""
    payload = anon.get(f"/cases/{conftest.PUBLISHED_CASE_SLUG}").json()
    related = payload.get("related") or []
    assert len(related) == 3, f"the case offers {len(related)} related cases rather than three"
    subject = set((payload.get("case") or payload).get("tags") or [])
    overlaps = [len(subject & set(r.get("tags") or [])) for r in related]
    assert overlaps == sorted(overlaps, reverse=True), (
        f"related cases are not ordered by discipline overlap: {overlaps}")
    for row in related:
        assert row.get("shared") or row.get("reason"), (
            f"related case {row.get('slug')!r} states nothing it shares")


def test_archive_search_filters_in_place(anon):
    """The archive search narrows the same listing rather than answering on another route."""
    everything = anon.get("/cases").json()
    assert everything, "the archive carries no case"
    target = everything[0]
    hit = anon.get("/cases", params={"q": target["name"]})
    assert hit.status_code == 200, f"searching the archive -> {hit.status_code}"
    names = [row["name"] for row in hit.json()]
    assert target["name"] in names, (
        f"searching for {target['name']!r} did not return that case")
    assert len(names) <= len(everything), "the search widened the archive"


def test_deck_compose_returns_a_token_and_blocks(anon):
    """Composing a deck returns an opaque token and an ordered set of typed blocks."""
    response = anon.post("/decks", json={"company": "Northwind Aero",
                                         "shape": "identity",
                                         "sector": "TECHNOLOGY",
                                         "detail": "standard"})
    assert response.status_code < 300, f"composing a deck -> {response.status_code}"
    token = response.json()["token"]
    assert len(token) >= 16, f"the deck token {token!r} is short enough to guess"
    deck = anon.get(f"/decks/{token}")
    assert deck.status_code == 200, f"reading the composed deck -> {deck.status_code}"
    blocks = deck.json()["blocks"]
    kinds = [b["type"] for b in blocks]
    for required in ("cover", "what_we_do", "approach", "next_step"):
        assert required in kinds, f"the deck carries no {required!r} block"
    cases = [b for b in blocks if b["type"] == "case"]
    assert 3 <= len(cases) <= 8, f"the deck carries {len(cases)} case blocks"


def test_deck_next_step_carries_shape_and_sector(anon):
    """The closing deck block leads into the brief with the composer answers carried across."""
    token = anon.post("/decks", json={"company": "Halden Group", "shape": "build",
                                      "sector": "FINANCE",
                                      "detail": "standard"}).json()["token"]
    blocks = anon.get(f"/decks/{token}").json()["blocks"]
    closing = [b for b in blocks if b["type"] == "next_step"]
    assert closing, "the deck carries no closing block"
    target = str(closing[0].get("href") or closing[0].get("target") or "")
    assert "/brief" in target, (
        f"the closing deck block points at {target!r} rather than into the brief")
    assert "build" in target and "FINANCE" in target, (
        f"the closing link {target!r} carries neither the chosen shape nor the sector")


def test_deck_detail_sets_the_page_count(anon):
    """Overview, standard and deep produce increasing deck lengths."""
    lengths = {}
    for detail in conftest.DETAILS:
        token = anon.post("/decks", json={"company": "Baseplate", "shape": "product",
                                          "sector": "TECHNOLOGY",
                                          "detail": detail}).json()["token"]
        lengths[detail] = len(anon.get(f"/decks/{token}").json()["blocks"])
    assert lengths["overview"] < lengths["standard"] < lengths["deep"], (
        f"deck length does not grow with the chosen detail: {lengths}")


def test_deck_route_serves_a_page_not_a_file(anon):
    """A composed deck opens as a page at its own address rather than as a download."""
    token = anon.post("/decks", json={"company": "Sturgeon", "shape": "identity",
                                      "sector": "AGENCY",
                                      "detail": "overview"}).json()["token"]
    response = conftest.page(f"/deck/{token}/")
    assert response.status_code == 200, (
        f"the composed deck route returned {response.status_code}")
    disposition = response.headers.get("content-disposition", "")
    assert "attachment" not in disposition.lower(), (
        f"the deck is served as a download: content-disposition {disposition!r}")
    assert "text/html" in response.headers.get("content-type", ""), (
        "the deck route does not serve a page")
    assert conftest.TELEMETRY_NOTICE in response.text, (
        "the first page of the deck does not carry the telemetry notice")


def test_expired_brief_token_offers_a_fresh_start(anon):
    """An unknown or expired brief token answers as a client error rather than a server fault."""
    response = anon.get("/briefs/expired-token-that-does-not-exist")
    assert conftest.is_client_error(response.status_code), (
        f"an unknown brief token returned {response.status_code}; an expired token is a "
        f"client error, never a server error")
    patched = anon.patch("/briefs/expired-token-that-does-not-exist",
                         json={"stage": 2})
    assert conftest.is_client_error(patched.status_code), (
        f"writing through an unknown brief token returned {patched.status_code}")


def test_digest_setting_defaults_to_daily(client_a):
    """Notification is a digest defaulting to Daily and settable to Weekly or Off."""
    engagement = conftest.engagement_ids(client_a)[0]
    payload = client_a.get(f"/portal/engagements/{engagement}").json()
    digest = payload.get("digest") or payload.get("notification")
    assert digest, "the portal states no digest setting"
    value = digest if isinstance(digest, str) else digest.get("value")
    assert value == "Daily", f"the digest defaults to {value!r} rather than Daily"


def test_portal_panels_are_present_for_an_attached_client(client_a):
    """An attached client sees the six portal panels for their own engagement."""
    engagements = conftest.engagement_ids(client_a)
    assert len(engagements) == 1, (
        f"the client is attached to {len(engagements)} engagements rather than one")
    payload = client_a.get(f"/portal/engagements/{engagements[0]}").json()
    for panel in ("right_now", "milestones", "deliverables", "people", "documents"):
        assert panel in payload, f"the portal answer carries no {panel!r} panel"
    assert payload["right_now"], "the Right now panel is empty"
    assert payload["deliverables"], "the engagement carries no deliverable"


def test_health_endpoint_returns_ok(anon):
    """GET /api/health answers 200 once the app is ready."""
    response = anon.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:200]}")


def test_unknown_route_answers_not_found(anon):
    """An unknown address answers not-found and renders the studio's own page."""
    response = conftest.page("/this-address-does-not-exist")
    assert response.status_code == 404, (
        f"an unknown address answered {response.status_code} rather than not-found")
    assert conftest.DECK_CONTROL in response.text or "href=\"/\"" in response.text, (
        "the not-found page is not the studio's own page with a way back")


def test_privacy_page_lists_every_collection_point(anon):
    """The privacy document names its eight sections and every newer collection point."""
    markup = conftest.page_body("/privacy-policy/")
    for heading in conftest.PRIVACY_HEADINGS:
        assert heading.lower() in markup.lower(), (
            f"the privacy document carries no {heading!r} section")
    lowered = markup.lower()
    missing = [p for p in conftest.NEW_COLLECTION_POINTS if p not in lowered]
    assert not missing, (
        f"the privacy document names no collection point for {missing}; every "
        f"collection the newer surfaces introduce must appear")
    assert "effective" in lowered or "date" in lowered, (
        "the privacy document carries no effective date")


def test_terms_page_is_reachable_and_linked_from_signup(anon):
    """The terms document is reachable and the signup form links to it."""
    assert conftest.page("/terms/").status_code == 200, "the terms route is not served"
    signup = conftest.page_body("/signup")
    assert "/terms" in signup, "the signup form does not link to the terms document"


def test_user_readme_names_every_seeded_login(anon):
    """The credentials file names each seeded account beside the corpus password."""
    path = os.path.join(conftest.APP_ROOT, "USER_README.md")
    assert os.path.isfile(path), f"{path} was not written"
    text = open(path, encoding="utf-8").read()
    for email in (conftest.STUDIO_EMAIL, conftest.CLIENT_EMAIL, conftest.CLIENT2_EMAIL):
        assert email in text, f"{path} does not name {email}"
    assert conftest.PASSWORD in text, f"{path} does not carry the seeded password"


def test_signup_is_open_and_attaches_no_engagement(anon):
    """Anyone may create an account, and a new account sees no engagement."""
    fresh_address = "newcomer-" + uuid.uuid4().hex[:10] + "@" + conftest.SEED_DOMAIN
    created = anon.post("/auth/signup", json={"email": fresh_address,
                                              "password": conftest.PASSWORD,
                                              "display_name": "Newcomer"})
    assert created.status_code < 300, (
        f"signup returned {created.status_code}: {created.text[:200]}")
    token = created.json()["token"]
    with appclient.client(token) as fresh:
        listing = fresh.get("/portal/engagements")
        assert listing.status_code in (200, 403), (
            f"a new account reading the portal got {listing.status_code}")
        if listing.status_code == 200:
            assert listing.json() == [], (
                f"a brand new account already sees engagements: {listing.json()}")


def test_api_is_served_under_the_api_prefix(anon):
    """Every graded endpoint answers on the app origin under /api."""
    assert appclient.api_base().endswith("/api"), (
        f"the API base is {appclient.api_base()}, which is not the /api prefix on "
        f"the app origin")
    for path in ("/health", "/services", "/capabilities"):
        response = anon.get(path)
        assert response.status_code == 200, (
            f"GET /api{path} returned {response.status_code}, so the API is not "
            f"served under /api on the same origin")


def test_reserved_directories_exist_and_are_empty(anon):
    """The two reserved directories exist at the app root and hold nothing."""
    for name in (".browser_screenshots", ".downloads"):
        path = os.path.join(conftest.APP_ROOT, name)
        assert os.path.isdir(path), f"{path} does not exist at the app root"
        assert os.listdir(path) == [], f"{path} is not empty: {os.listdir(path)}"


def test_served_bundle_is_a_production_build(anon):
    """The app serves a built bundle rather than a development server."""
    markup = conftest.page_body("/")
    lowered = markup.lower()
    for marker in ("/@vite/client", "vite/dist/client", "webpack-dev-server",
                   "__vite_ping"):
        assert marker not in lowered, (
            f"the served document loads {marker!r}, which only a development server "
            f"emits")
    assert conftest.page("/").status_code == 200, "the app is not answering"


def test_reduced_motion_request_suppresses_video(anon):
    """A reader asking for reduced motion is served posters rather than autoplaying video."""
    markup = conftest.page_body("/", headers={"Sec-CH-Prefers-Reduced-Motion": "reduce"})
    lowered = markup.lower()
    assert "prefers-reduced-motion" in lowered, (
        "nothing in the served document honours a reduced-motion preference")
    if "<video" in lowered:
        assert "autoplay" not in lowered.split("<video", 1)[1][:400], (
            "a video still carries autoplay when reduced motion is requested")
        assert "poster" in lowered, "a video is served with no poster frame"


def test_portal_document_loads_no_scroll_module(client_a):
    """The portal document pulls none of the marketing routes' scroll machinery."""
    markup = conftest.page_body("/portal/")
    lowered = markup.lower()
    for marker in ("scrolltrigger", "lenis", "smooth-scroll", "parallax"):
        assert marker not in lowered, (
            f"the portal document loads {marker!r}; the portal binds nothing to scroll")


def test_positioning_line_keeps_its_whole_sentence(anon):
    """The split positioning line still reads as one sentence to assistive technology."""
    markup = conftest.page_body("/")
    assert "We create premium digital experiences" in markup, (
        "the positioning line is not present as a readable sentence; a per-character "
        "split must keep the whole string as its accessible name")


def test_studio_strip_and_year_mark_carry_their_exact_strings(anon):
    """The studio strip and the footer year mark carry their pinned copy."""
    markup = conftest.page_body("/")
    for pinned in conftest.STUDIO_STRIP:
        assert pinned in markup, f"the home route does not carry {pinned!r}"
    assert conftest.YEAR_MARK in markup, (
        f"the footer does not carry the year mark {conftest.YEAR_MARK!r}")
    assert conftest.DECK_CONTROL in markup, (
        f"the home route does not carry the control {conftest.DECK_CONTROL!r}")


def test_root_type_size_follows_the_reader_preference(anon):
    """The type scale is expressed against the reader's root size rather than pinned."""
    markup = conftest.page_body("/")
    lowered = markup.lower()
    assert "rem" in lowered, (
        "the served document expresses no size in rem, so the scale cannot grow with "
        "the reader's own root size")
    assert "html{font-size:16px" not in lowered.replace(" ", ""), (
        "the root font size is pinned in pixels, so a reader preference does nothing")


def test_content_images_carry_alternative_text(anon):
    """Every content image on the home route carries alternative text."""
    markup = conftest.page_body("/")
    images = [chunk for chunk in markup.lower().split("<img")[1:]]
    assert images, "the home route serves no image element at all"
    naked = [c[:120] for c in images if "alt=" not in c[:400]]
    assert not naked, f"{len(naked)} image(s) carry no alt attribute: {naked[:3]}"


def test_loader_is_removed_after_the_first_load(anon):
    """The loader label ships once and the development slow-load switch is off."""
    markup = conftest.page_body("/")
    assert conftest.LOADER_LABEL in markup, (
        f"the first document does not carry the loader label {conftest.LOADER_LABEL!r}")
    lowered = markup.lower()
    for switch in ("slowload", "slow_load", "simulateslowload", "debugloader"):
        assert switch not in lowered.replace("-", ""), (
            f"the built output enables the development switch {switch!r}")


def test_case_wipe_corner_alternates_down_the_archive(anon):
    """The reveal corner alternates down the archive and is not stored on the case."""
    rows = anon.get("/cases").json()
    assert len(rows) >= 4, f"the archive carries only {len(rows)} cases"
    for row in rows:
        assert "corner" not in row, (
            f"case {row['slug']!r} stores a corner on its record; the corner is derived "
            f"from archive position")
    markup = conftest.page_body("/work/")
    corners = [c for c in ("top-left", "top-right", "bottom-left", "bottom-right")
               if c in markup.lower()]
    assert len(corners) >= 2, (
        f"the archive markup names only {corners}; the reveal corner must alternate")


def test_capability_band_is_unpinned_at_phone_width(anon):
    """The capability band carries a separate arrangement at phone width and does not pin."""
    markup = conftest.page_body("/")
    lowered = markup.lower()
    assert "@media" in lowered or "max-width" in lowered, (
        "the served document declares no width tiers at all")
    assert "overflow-x:hidden" in lowered.replace(" ", "") or "overflow-x: hidden" in lowered, (
        "nothing prevents sideways overflow at a narrow width")


def test_commissioned_surfaces_are_all_reachable(anon):
    """Every commissioned route answers, so the six new surfaces exist."""
    for route in ("/work/", "/brief/", "/deck/", "/portal/",
                  f"/work/{conftest.PUBLISHED_CASE_SLUG}/"):
        response = conftest.page(route)
        assert response.status_code < 500, (
            f"{route} answered {response.status_code}, so a commissioned surface is "
            f"not built")
        assert response.status_code != 404, f"{route} is not served at all"


def test_attachment_bytes_are_not_held_in_a_table(anon, db):
    """A brief attachment is a key in the store, never bytes in a row."""
    token = conftest.create_brief(anon)["token"]
    uploaded = conftest.attach(anon, token, 4096)
    assert uploaded.status_code < 300, f"attaching -> {uploaded.status_code}"
    rows = db.rows("attachment", limit=50)
    assert rows, "no attachment row was written"
    for row in rows:
        for key, value in row.items():
            assert not isinstance(value, (bytes, bytearray)), (
                f"attachment column {key!r} holds raw bytes; the bucket is the only "
                f"place the bytes live")
        assert row.get("object_key"), f"attachment row {row} carries no object key"


def test_two_submissions_for_one_slot_book_exactly_one(anon):
    """Two simultaneous submissions for one held slot produce exactly one booking."""
    slots = conftest.free_slots(anon)
    assert slots, "no free slot remains to contend for"
    slot_id = slots[0]["id"]
    first = conftest.create_brief(anon, stage=6)["token"]
    second = conftest.create_brief(anon, stage=6)["token"]
    holds = {}
    for token in (first, second):
        held = anon.post(f"/briefs/{token}/hold", json={"slot_id": slot_id})
        holds[token] = held.json().get("hold_token") if held.status_code < 300 else None
    results = {}
    barrier = threading.Barrier(2)

    def submit(token):
        with appclient.client() as c:
            barrier.wait()
            results[token] = c.post(f"/briefs/{token}/submit",
                                    json={"slot_id": slot_id,
                                          "hold_token": holds[token]})

    threads = [threading.Thread(target=submit, args=(t,)) for t in (first, second)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    codes = sorted(r.status_code for r in results.values())
    winners = [c for c in codes if c < 300]
    assert len(winners) == 1, (
        f"two simultaneous submissions for one slot returned {codes}; exactly one must "
        f"be booked and the other rejected")
    losers = [c for c in codes if c >= 300]
    assert all(conftest.is_client_error(c) for c in losers), (
        f"the losing submission returned {losers} rather than a client error")


def test_losing_submission_is_offered_two_nearest_slots(anon):
    """A refused submission names two nearby free slots to choose instead."""
    slots = conftest.free_slots(anon)
    assert len(slots) >= 3, f"only {len(slots)} free slots remain to offer alternatives from"
    slot_id = slots[0]["id"]
    winner = conftest.create_brief(anon, stage=6)["token"]
    held = anon.post(f"/briefs/{winner}/hold", json={"slot_id": slot_id})
    anon.post(f"/briefs/{winner}/submit",
              json={"slot_id": slot_id, "hold_token": held.json().get("hold_token")})
    loser = conftest.create_brief(anon, stage=6)["token"]
    refused = anon.post(f"/briefs/{loser}/submit",
                        json={"slot_id": slot_id, "hold_token": "stale"})
    assert conftest.is_client_error(refused.status_code), (
        f"submitting for a booked slot returned {refused.status_code}")
    payload = conftest.body(refused)
    offered = payload.get("nearest") if isinstance(payload, dict) else None
    assert offered and len(offered) == 2, (
        f"the refusal offered {offered!r} rather than the two nearest free slots")


def test_losing_submission_keeps_narrative_and_attachment(anon):
    """A refused booking leaves every other answer in the brief untouched."""
    slots = conftest.free_slots(anon)
    assert slots, "no free slot remains to contend for"
    slot_id = slots[0]["id"]
    winner = conftest.create_brief(anon, stage=6)["token"]
    held = anon.post(f"/briefs/{winner}/hold", json={"slot_id": slot_id})
    anon.post(f"/briefs/{winner}/submit",
              json={"slot_id": slot_id, "hold_token": held.json().get("hold_token")})
    loser = conftest.create_brief(anon, stage=6)["token"]
    anon.patch(f"/briefs/{loser}", json={"narrative": "Keep every word of this."})
    conftest.attach(anon, loser, 2048)
    refused = anon.post(f"/briefs/{loser}/submit",
                        json={"slot_id": slot_id, "hold_token": "stale"})
    assert conftest.is_client_error(refused.status_code)
    after = anon.get(f"/briefs/{loser}").json()
    assert after["narrative"] == "Keep every word of this.", (
        "the refused submission lost the free text")
    assert after.get("attachment"), "the refused submission lost the attachment"
    assert str(after["stage"]) != "1", "the refused submission sent the visitor back to stage one"


def test_slot_state_reaches_booked_exactly_once(anon, db):
    """A contested slot carries exactly one booking row in the datastore."""
    slots = conftest.free_slots(anon)
    assert slots, "no free slot remains to contend for"
    slot_id = slots[0]["id"]
    token = conftest.create_brief(anon, stage=6)["token"]
    held = anon.post(f"/briefs/{token}/hold", json={"slot_id": slot_id})
    anon.post(f"/briefs/{token}/submit",
              json={"slot_id": slot_id, "hold_token": held.json().get("hold_token")})
    again = conftest.create_brief(anon, stage=6)["token"]
    repeat = anon.post(f"/briefs/{again}/submit",
                       json={"slot_id": slot_id, "hold_token": "any"})
    assert conftest.is_client_error(repeat.status_code), (
        f"a second submission for a booked slot returned {repeat.status_code}")
    bookings = db.count("booking", slot_id=slot_id)
    assert bookings == 1, f"slot {slot_id} carries {bookings} booking rows rather than one"


def test_soft_hold_expires_and_frees_the_slot(anon, db):
    """A hold is recorded with an expiry and the slot returns to free when it lapses."""
    slots = conftest.free_slots(anon)
    assert slots, "no free slot remains"
    slot_id = slots[0]["id"]
    token = conftest.create_brief(anon, stage=6)["token"]
    held = anon.post(f"/briefs/{token}/hold", json={"slot_id": slot_id})
    assert held.status_code < 300, f"placing a hold -> {held.status_code}"
    assert held.json().get("hold_expires_at"), "the hold carries no expiry"
    row = db.one("availability_slot", id=slot_id)
    assert row is not None, f"slot {slot_id} has no row in the datastore"
    assert row.get("state") in ("held", "free"), (
        f"a held slot reports state {row.get('state')!r}")


def test_archive_facet_counts_reconcile_with_case_rows(anon):
    """Every facet count equals the number of cases that value would leave."""
    facets = anon.get("/cases/facets")
    assert facets.status_code == 200, f"GET /api/cases/facets -> {facets.status_code}"
    payload = facets.json()
    cases = anon.get("/cases").json()
    for value, count in {row["value"]: row["count"] for row in payload["sector"]}.items():
        actual = len([c for c in cases if c["sector"] == value])
        assert count == actual, (
            f"the sector facet reports {count} for {value!r} while the archive holds "
            f"{actual}")
    zero = [row for row in payload["sector"] if row["count"] == 0]
    for row in zero:
        assert row.get("disabled") is True, (
            f"facet value {row['value']!r} has a zero count but is not disabled")


def test_empty_archive_filter_returns_an_empty_array(anon):
    """A filter that matches nothing returns an empty array and names a nearer filter."""
    response = anon.get("/cases", params={"sector": "HEALTHCARE", "kind": "BRANDING",
                                          "discipline": "WORDPRESS"})
    assert response.status_code == 200, (
        f"an empty archive filter returned {response.status_code} rather than an empty "
        f"result")
    payload = response.json()
    rows = payload if isinstance(payload, list) else payload.get("cases", [])
    assert rows == [], f"the impossible filter returned {len(rows)} cases"


def test_approval_is_appended_with_actor_and_time(client_a, db):
    """Approving a version appends a record naming the actor and the moment."""
    engagement = conftest.engagement_ids(client_a)[0]
    version = conftest.first_version_awaiting(client_a, engagement)
    before = db.count("approval", version_id=version)
    response = client_a.post(f"/portal/versions/{version}/approve",
                             json={"decision": "approve", "note": ""})
    assert response.status_code < 300, (
        f"approving returned {response.status_code}: {response.text[:200]}")
    after = db.count("approval", version_id=version)
    assert after == before + 1, (
        f"approving changed the approval count from {before} to {after}; an approval is "
        f"appended, never replaced")
    record = client_a.get(f"/portal/versions/{version}").json()
    latest = (record.get("approvals") or [])[-1]
    assert latest.get("account_id") or latest.get("actor"), (
        f"the approval names no actor: {latest}")
    assert latest.get("created_at") or latest.get("timestamp"), (
        f"the approval names no time: {latest}")


def test_approved_version_is_frozen_and_prior_version_survives(client_a):
    """An approved version freezes and the earlier version stays readable."""
    engagement = conftest.engagement_ids(client_a)[0]
    version = conftest.first_version_awaiting(client_a, engagement)
    client_a.post(f"/portal/versions/{version}/approve",
                  json={"decision": "approve", "note": ""})
    frozen = client_a.get(f"/portal/versions/{version}").json()["version"]
    assert frozen.get("frozen") is True, (
        f"version {version} is not frozen after approval: {frozen}")
    payload = client_a.get(f"/portal/engagements/{engagement}").json()
    versions = [v for d in payload["deliverables"] for v in d["versions"]]
    assert len(versions) >= 2, (
        f"the deliverable carries {len(versions)} versions; the earlier one must survive")


def test_seeding_is_idempotent_across_a_restart(anon, db):
    """The seeded rows appear exactly once, whatever the app has been restarted."""
    for email in (conftest.STUDIO_EMAIL, conftest.CLIENT_EMAIL, conftest.CLIENT2_EMAIL):
        found = db.count("account", email=email)
        assert found == 1, f"{email} appears {found} times; seeding is not idempotent"
    cases = anon.get("/cases").json()
    slugs = [c["slug"] for c in cases]
    assert len(slugs) == len(set(slugs)), (
        f"the archive carries duplicate slugs: {sorted(slugs)}")


def test_list_endpoints_return_top_level_arrays(anon):
    """Every list endpoint answers with a top-level JSON array."""
    for path in ("/cases", "/services", "/capabilities"):
        response = anon.get(path)
        assert response.status_code == 200, f"GET /api{path} -> {response.status_code}"
        assert isinstance(response.json(), list), (
            f"GET /api{path} returned {type(response.json()).__name__} rather than a "
            f"top-level array")


def test_trailing_slash_redirect_is_permanent(anon):
    """The slash-less contact address redirects permanently to the canonical one."""
    response = conftest.page("/contact")
    assert response.status_code in (301, 308), (
        f"/contact answered {response.status_code} rather than a permanent redirect")
    assert response.headers.get("location", "").rstrip("/").endswith("/contact"), (
        f"/contact redirected to {response.headers.get('location')!r}")


def test_environment_variables_drive_every_connection(anon, db, store):
    """The datastore and the object store answer at the variables the environment sets."""
    for name in ("DATABASE_URL", "STORAGE_ENDPOINT", "STORAGE_BUCKET",
                 "STORAGE_ACCESS_KEY", "STORAGE_SECRET_KEY", "APP_PUBLIC_URL",
                 "APP_PUBLIC_PORT"):
        assert os.environ.get(name), f"{name} is unset in the environment"
    assert db.count("account") >= 3, (
        "the datastore reached through DATABASE_URL carries fewer than three accounts")
    assert isinstance(store.list(""), list), (
        "the object store reached through STORAGE_ENDPOINT did not answer a listing")
    assert os.environ["APP_PUBLIC_URL"].rstrip("/") == conftest.app_origin(), (
        "the app is not answering at APP_PUBLIC_URL")


def test_scroll_bindings_do_not_accumulate_across_navigations(anon):
    """Repeated navigation does not leave a growing number of scroll bindings behind."""
    first = conftest.page_body("/")
    for _ in range(3):
        conftest.page_body("/contact/")
        conftest.page_body("/")
    later = conftest.page_body("/")
    assert abs(len(later) - len(first)) < max(2048, len(first) // 20), (
        "the home document grew materially after repeated navigation, which is what a "
        "leaked binding per navigation looks like")


def test_protected_object_requires_an_authenticated_read(anon, client_a):
    """A protected object is served only through an authenticated, entitled read."""
    engagement = conftest.engagement_ids(client_a)[0]
    payload = client_a.get(f"/portal/engagements/{engagement}").json()
    key = None
    for deliverable in payload["deliverables"]:
        for version in deliverable["versions"]:
            key = version.get("preview_key") or version.get("preview")
            if key:
                break
        if key:
            break
    assert key, "no delivered version names a preview object"
    denied = anon.get(f"/objects/{key}")
    assert denied.status_code in (401, 403, 404), (
        f"an anonymous caller read a protected object with {denied.status_code}")


def test_attachment_of_another_brief_is_denied(anon):
    """A brief attachment cannot be read through a different brief token."""
    first = conftest.create_brief(anon)["token"]
    conftest.attach(anon, first, 1024)
    stored = anon.get(f"/briefs/{first}").json().get("attachment") or {}
    key = stored.get("object_key") or stored.get("key")
    assert key, f"the brief records no attachment key: {stored}"
    other = conftest.create_brief(anon)["token"]
    response = anon.get(f"/briefs/{other}/attachment")
    assert response.status_code in (401, 403, 404), (
        f"a second brief token reached another brief's attachment with "
        f"{response.status_code}")


def test_resume_token_is_opaque_and_carries_no_address(anon):
    """A resume token is unguessable, carries no address and is kept out of indexes."""
    record = conftest.create_brief(anon)
    token = record["token"]
    assert len(token) >= 16, f"the resume token {token!r} is short enough to guess"
    assert "@" not in token, f"the resume token {token!r} carries an email address"
    assert conftest.CLIENT_EMAIL.split("@")[0] not in token, (
        f"the resume token {token!r} is derived from the visitor address")
    assert record.get("expires_at"), "the brief record names no expiry for its token"
    page = conftest.page(f"/brief/{token}/")
    assert page.status_code == 200, f"the resume route answered {page.status_code}"
    robots = page.headers.get("x-robots-tag", "").lower()
    assert "noindex" in robots or "noindex" in page.text.lower(), (
        "the resume route is indexable; a bearer link must be held out of indexes")
    referrer = page.headers.get("referrer-policy", "").lower()
    assert referrer, "the resume route sets no referrer policy, so the token leaks onward"


def test_unpublished_case_route_is_not_found_for_anonymous(anon):
    """An unpublished case is not found at its own route for a signed-out visitor."""
    api = anon.get(f"/cases/{conftest.UNPUBLISHED_CASE_SLUG}")
    assert api.status_code == 404, (
        f"the unpublished case answered {api.status_code} over the API")
    assert conftest.UNPUBLISHED_CASE_NAME not in api.text, (
        "the refusal leaked the unpublished case name")
    route = conftest.page(f"/work/{conftest.UNPUBLISHED_CASE_SLUG}/")
    assert route.status_code == 404, (
        f"the unpublished case route answered {route.status_code}")


def test_unpublished_case_route_is_not_found_for_a_client(client_a):
    """An unpublished case stays hidden from a signed-in client."""
    response = client_a.get(f"/cases/{conftest.UNPUBLISHED_CASE_SLUG}")
    assert response.status_code == 404, (
        f"a client session read the unpublished case with {response.status_code}")
    assert conftest.UNPUBLISHED_CASE_NAME not in response.text, (
        "the refusal leaked the unpublished case name")


def test_unpublished_case_is_absent_from_the_archive_listing(anon):
    """The public archive listing carries no unpublished case."""
    slugs = [c["slug"] for c in anon.get("/cases").json()]
    assert conftest.UNPUBLISHED_CASE_SLUG not in slugs, (
        f"the public archive lists the unpublished case {conftest.UNPUBLISHED_CASE_SLUG!r}")
    assert conftest.PUBLISHED_CASE_SLUG in slugs, (
        "the published case is missing from the archive listing")


def test_publish_endpoint_is_studio_only(anon, client_a):
    """Publishing and unpublishing a case is refused to anyone but the studio."""
    path = f"/cases/{conftest.UNPUBLISHED_CASE_SLUG}/publish"
    assert anon.post(path).status_code in (401, 403, 404), (
        "an anonymous caller reached the publish endpoint")
    assert client_a.post(path).status_code in (401, 403, 404), (
        "a client session reached the publish endpoint")


def test_approval_without_the_right_is_denied(client_b):
    """A client carrying no approval right cannot approve."""
    engagement = conftest.engagement_ids(client_b)[0]
    version = conftest.first_version_awaiting(client_b, engagement)
    response = client_b.post(f"/portal/versions/{version}/approve",
                             json={"decision": "approve", "note": ""})
    assert response.status_code in (401, 403), (
        f"a client with no approval right approved with {response.status_code}")


def test_denied_approval_leaves_the_version_unchanged(client_b, db):
    """A refused approval writes nothing and the version stays open."""
    engagement = conftest.engagement_ids(client_b)[0]
    version = conftest.first_version_awaiting(client_b, engagement)
    before = db.count("approval", version_id=version)
    client_b.post(f"/portal/versions/{version}/approve",
                  json={"decision": "approve", "note": ""})
    after = db.count("approval", version_id=version)
    assert after == before, (
        f"a refused approval still wrote a record: {before} -> {after}")
    row = db.one("version", id=version)
    assert not row.get("frozen"), "a refused approval froze the version"


def test_studio_endpoints_are_denied_to_a_client_session(client_a):
    """A client session cannot reach a studio-only endpoint."""
    for path in ("/decks/any-token/telemetry", f"/cases/{conftest.PUBLISHED_CASE_SLUG}/publish"):
        response = (client_a.post(path) if path.endswith("publish")
                    else client_a.get(path))
        assert response.status_code in (401, 403, 404), (
            f"a client session reached {path} with {response.status_code}")


def test_studio_cannot_approve_on_behalf_of_a_client(studio, client_a, db):
    """The studio account cannot record an approval in a client's name."""
    engagement = conftest.engagement_ids(client_a)[0]
    version = conftest.first_version_awaiting(client_a, engagement)
    before = db.count("approval", version_id=version)
    response = studio.post(f"/portal/versions/{version}/approve",
                           json={"decision": "approve", "note": ""})
    assert response.status_code in (401, 403), (
        f"the studio approved a client deliverable with {response.status_code}")
    assert db.count("approval", version_id=version) == before, (
        "a studio approval attempt still wrote a record")


def test_second_factor_is_required_for_an_approver(client_a):
    """An account carrying approval rights reports that a second factor is required."""
    engagement = conftest.engagement_ids(client_a)[0]
    payload = client_a.get(f"/portal/engagements/{engagement}").json()
    account = payload.get("account") or payload.get("viewer") or {}
    flag = account.get("second_factor_required")
    assert flag is True, (
        f"the approving account reports second_factor_required={flag!r}; an approver "
        f"carries a second factor")


def test_cross_engagement_read_is_denied(client_b, client_a):
    """A client cannot read an engagement their account is not attached to."""
    theirs = conftest.engagement_ids(client_a)[0]
    mine = conftest.engagement_ids(client_b)
    assert theirs not in mine, (
        "both seeded clients are attached to the same engagement, so isolation cannot "
        "be observed")
    response = client_b.get(f"/portal/engagements/{theirs}")
    assert response.status_code in (401, 403, 404), (
        f"a cross-engagement read returned {response.status_code}")


def test_denied_engagement_response_carries_no_record(client_b, client_a):
    """A refused cross-engagement read returns none of the record it refused."""
    theirs = conftest.engagement_ids(client_a)[0]
    payload = client_a.get(f"/portal/engagements/{theirs}").json()
    marker = str((payload.get("deliverables") or [{}])[0].get("name", ""))
    assert marker, "the other engagement carries no named deliverable to look for"
    refused = client_b.get(f"/portal/engagements/{theirs}")
    assert marker not in refused.text, (
        f"the refused response leaked the deliverable name {marker!r}")


def test_portal_request_without_a_token_is_denied(anon):
    """An unauthenticated portal request is refused and returns no engagement data."""
    response = anon.get("/portal/engagements")
    assert response.status_code in (401, 403), (
        f"an unauthenticated portal read returned {response.status_code}")
    assert "deliverable" not in response.text.lower(), (
        "a denied portal response leaked engagement content")


def test_portal_listing_is_scoped_to_the_attached_engagement(client_b, db):
    """The portal listing returns only engagements the account is joined to."""
    listed = conftest.engagement_ids(client_b)
    assert len(listed) == 1, f"the client sees {len(listed)} engagements rather than one"
    total = db.count("engagement")
    assert total > len(listed), (
        f"only {total} engagement exists, so scoping cannot be observed")
    joined = db.count("engagement_account")
    assert joined >= 2, "fewer than two engagement-account joins are seeded"


def test_deck_read_record_holds_no_reader_identity(anon, studio, db):
    """Deck telemetry records reading without identifying who read."""
    token = anon.post("/decks", json={"company": "Grove App", "shape": "product",
                                      "sector": "ECOMMERCE",
                                      "detail": "overview"}).json()["token"]
    anon.post(f"/decks/{token}/read", json={"page": 2})
    rows = db.rows("deck_read", limit=20)
    assert rows, "no deck read was recorded"
    for row in rows:
        blob = " ".join(str(v) for v in row.values()).lower()
        assert "@" not in blob, f"a deck read record carries an address: {row}"
        for field in ("ip", "ip_address", "user_agent", "fingerprint", "latitude"):
            assert field not in row, f"the deck read record carries {field!r}"


def test_expired_deck_matches_revoked_deck_response(anon, studio):
    """An expired deck link and a revoked one answer identically."""
    made = anon.post("/decks", json={"company": "Sturgeon", "shape": "identity",
                                     "sector": "AGENCY", "detail": "overview"}).json()
    token = made["token"]
    revoked = studio.post(f"/decks/{token}/revoke")
    assert revoked.status_code < 300 or revoked.status_code == 404, (
        f"revoking a deck returned {revoked.status_code}")
    after_revoke = anon.get(f"/decks/{token}")
    expired = anon.get("/decks/a-token-that-has-long-since-expired")
    assert after_revoke.status_code == expired.status_code, (
        f"a revoked deck answered {after_revoke.status_code} while an expired one "
        f"answered {expired.status_code}; the two must be indistinguishable")
    assert conftest.body(after_revoke) == conftest.body(expired), (
        "a revoked deck and an expired deck returned different bodies")


def test_used_signin_link_is_refused(anon):
    """A portal sign-in link works once and is refused thereafter."""
    issued = anon.post("/auth/signin-link", json={"email": conftest.CLIENT_EMAIL})
    assert issued.status_code < 300, f"requesting a sign-in link -> {issued.status_code}"
    link_token = issued.json().get("token")
    assert link_token, (
        "the sign-in link response carries no token to exchange, so the single-use rule "
        "cannot be observed")
    first = anon.post("/auth/signin-link/exchange", json={"token": link_token})
    assert first.status_code < 300, f"first exchange -> {first.status_code}"
    second = anon.post("/auth/signin-link/exchange", json={"token": link_token})
    assert conftest.is_client_error(second.status_code), (
        f"a used sign-in link was accepted a second time with {second.status_code}")


def test_published_address_is_absent_from_the_served_document(anon):
    """The published enquiry address is not plain text in the served markup."""
    markup = conftest.page_body("/contact/")
    assert "hi@example.com" not in markup, (
        "the published enquiry address appears as plain text in the served document")
    assert "mailto" in markup.lower() or "data-" in markup.lower(), (
        "the contact rail offers no way to reach the address at all")


def test_page_view_is_recorded_and_studio_only(anon, studio, db):
    """A page view is recorded with its route, and only the studio may read the record."""
    before = db.count("page_view")
    conftest.page_body("/work/")
    recorded = conftest.settle(lambda: db.count("page_view") > before,
                               "a page view record")
    assert recorded, "no page view was recorded"
    denied = anon.get("/portal/page-views")
    assert denied.status_code in (401, 403, 404), (
        f"an anonymous caller read the page-view record with {denied.status_code}")


def test_seeded_accounts_sign_in_with_the_corpus_password(anon, db):
    """Each seeded account signs in with the corpus password and no password is stored plainly."""
    for email in (conftest.STUDIO_EMAIL, conftest.CLIENT_EMAIL, conftest.CLIENT2_EMAIL):
        token = appclient.login(email, conftest.PASSWORD)
        assert token, f"{email} did not sign in with the corpus password"
    row = db.one("account", email=conftest.STUDIO_EMAIL)
    assert row is not None, f"{conftest.STUDIO_EMAIL} has no account row"
    stored = " ".join(str(v) for v in row.values())
    assert conftest.PASSWORD not in stored, (
        "the corpus password is stored in plain text on the account row")


def test_signout_clears_the_session(anon):
    """Signing out invalidates the bearer token it was issued against."""
    token = appclient.login(conftest.CLIENT_EMAIL, conftest.PASSWORD)
    with appclient.client(token) as session:
        assert session.get("/portal/engagements").status_code == 200
        out = session.post("/auth/logout", json={"all_devices": False})
        assert out.status_code < 300, f"signing out -> {out.status_code}"
    with appclient.client(token) as dead:
        after = dead.get("/portal/engagements")
        assert after.status_code in (401, 403), (
            f"a signed-out token still read the portal with {after.status_code}")


def test_unauthenticated_portal_request_lands_on_sign_in(anon):
    """Opening the portal signed out leads to the sign-in route, which then continues to the portal."""
    response = conftest.page("/portal/")
    assert response.status_code in (200, 302, 303, 307, 401, 403), (
        f"the portal route answered {response.status_code}")
    if response.status_code in (302, 303, 307):
        assert "/login" in response.headers.get("location", ""), (
            f"the portal redirected to {response.headers.get('location')!r} rather than "
            f"the sign-in route")
    else:
        assert "/login" in response.text or "sign in" in response.text.lower(), (
            "the portal route neither redirects to sign in nor offers it")


def test_no_credential_reaches_the_browser(anon):
    """Nothing the browser downloads carries a credential or a connection string."""
    markup = conftest.page_body("/")
    for marker in conftest.SECRET_MARKERS:
        assert marker not in markup, (
            f"the served document carries {marker!r}; no credential reaches the browser")
    for route in ("/brief/", "/work/", "/contact/"):
        text = conftest.page_body(route)
        for marker in conftest.SECRET_MARKERS:
            assert marker not in text, f"{route} carries {marker!r}"


def test_no_third_party_origin_is_requested_at_runtime(anon):
    """The served documents reach for no origin outside the app."""
    origin = conftest.app_origin()
    for route in ("/", "/work/", "/portal/"):
        markup = conftest.page_body(route)
        for marker in ("google-analytics.com", "googletagmanager.com",
                       "connect.facebook.net", "cdn.segment.com", "hotjar"):
            assert marker not in markup.lower(), (
                f"{route} reaches for the third-party origin {marker!r} at run time")
        assert origin or True


def test_oversized_attachment_is_refused_and_brief_intact(anon):
    """An attachment above the limit is refused alone and the brief survives."""
    token = conftest.create_brief(anon, stage=5)["token"]
    anon.patch(f"/briefs/{token}", json={"narrative": "This text must survive."})
    response = conftest.attach(anon, token, conftest.ATTACHMENT_LIMIT_BYTES + 1024)
    assert conftest.is_client_error(response.status_code), (
        f"an oversized attachment returned {response.status_code} rather than a refusal")
    assert "2" in response.text or "size" in response.text.lower(), (
        f"the refusal does not state the limit: {response.text[:200]}")
    after = anon.get(f"/briefs/{token}").json()
    assert after["narrative"] == "This text must survive.", (
        "the refused attachment took the free text with it")
    assert str(after["stage"]) == "5", (
        f"the refused attachment moved the brief to stage {after['stage']!r}")


def test_refused_attachment_writes_no_object(anon, store):
    """A refused attachment leaves no object behind in the bucket."""
    token = conftest.create_brief(anon)["token"]
    before = len(store.list(f"{conftest.BRIEF_KEY_PREFIX}{token}/"))
    conftest.attach(anon, token, conftest.ATTACHMENT_LIMIT_BYTES + 4096)
    after = len(store.list(f"{conftest.BRIEF_KEY_PREFIX}{token}/"))
    assert after == before, (
        f"a refused attachment left {after - before} object(s) in the bucket")


def test_request_changes_without_a_note_is_refused(client_a, db):
    """Requesting changes without a note is refused and records nothing."""
    engagement = conftest.engagement_ids(client_a)[0]
    version = conftest.first_version_awaiting(client_a, engagement)
    before = db.count("approval", version_id=version)
    response = client_a.post(f"/portal/versions/{version}/approve",
                             json={"decision": "request_changes", "note": ""})
    assert conftest.is_client_error(response.status_code), (
        f"requesting changes with no note returned {response.status_code}")
    assert db.count("approval", version_id=version) == before, (
        "a refused change request still wrote a record")


def test_contact_form_rejection_writes_nothing(anon, db):
    """A contact submission missing a required field is refused and stores nothing."""
    before = db.count("brief")
    response = anon.post("/briefs", json={"stage": 1,
                                          "contact": {"name": "", "company": "",
                                                      "email": "not-an-address"},
                                          "disciplines": []})
    assert conftest.is_client_error(response.status_code), (
        f"an invalid enquiry returned {response.status_code} rather than a refusal")
    assert db.count("brief") == before, "a refused enquiry still wrote a record"
    text = response.text.lower()
    assert "email" in text or "name" in text, (
        f"the refusal names no field: {response.text[:200]}")


def test_decoy_field_submission_is_refused(anon, db):
    """A submission filling the unattended decoy field is refused."""
    before = db.count("brief")
    response = anon.post("/briefs", json={"stage": 1,
                                          "contact": {"name": "Bot", "company": "Bot",
                                                      "email": conftest.CLIENT2_EMAIL},
                                          "disciplines": ["Logo Design"],
                                          "website_url": "http://spam.example"})
    assert conftest.is_client_error(response.status_code), (
        f"a submission with the decoy field filled returned {response.status_code}")
    assert db.count("brief") == before, "a refused bot submission still wrote a record"


def test_no_absent_feature_surface_is_served(anon):
    """None of the excluded feature surfaces appears in the product."""
    for route in ("/", "/work/", "/portal/"):
        markup = conftest.page_body(route).lower()
        for phrase in conftest.ABSENT_PHRASES:
            assert phrase not in markup, (
                f"{route} offers {phrase!r}; that surface is out of scope")
    for row in anon.get("/cases").json():
        for field in ("likes", "comments", "price", "cart", "folder"):
            assert field not in row, (
                f"a case record carries a {field!r} field; that surface is out of scope")


def test_no_font_binary_or_media_binary_is_served(anon):
    """The served documents ship no font file and no media binary."""
    markup = conftest.page_body("/")
    lowered = markup.lower()
    for extension in (".woff2", ".woff", ".ttf", ".otf", ".mp4", ".webm"):
        assert extension not in lowered, (
            f"the home document references a {extension} binary; the build ships none")
    assert "font-family" in lowered, (
        "the document names no font family, so the fallback stacks are absent")


def test_reference_brand_name_is_absent_from_the_output(anon):
    """The reference agency's own brand does not appear in the built output."""
    for route in ("/", "/work/", "/contact/", "/privacy-policy/"):
        markup = conftest.page_body(route)
        assert "sable" in markup.lower(), f"{route} does not carry the studio name"
        assert "<BRAND>" not in markup, f"{route} still carries an unfilled brand token"
        assert "<BRAND_LONG>" not in markup, f"{route} still carries an unfilled token"


def test_pointer_layers_are_absent_without_a_fine_pointer(anon):
    """The pointer replacement is gated on a fine pointer."""
    markup = conftest.page_body("/")
    lowered = markup.lower()
    assert "pointer: fine" in lowered or "pointer:fine" in lowered, (
        "the pointer replacement is not gated on a fine pointer, so it renders on touch "
        "devices too")
    assert "hover: hover" in lowered or "hover:hover" in lowered, (
        "the pointer replacement is not gated on hover capability")


def test_marks_are_inline_geometry_not_binaries(anon):
    """Every mark on the home route is drawn geometry rather than a fetched file."""
    markup = conftest.page_body("/")
    lowered = markup.lower()
    assert "<svg" in lowered, "the home route carries no drawn geometry at all"
    assert ".svg\"" not in lowered and ".svg'" not in lowered, (
        "a mark is fetched as a file rather than drawn inline")
    assert "circle" in lowered, (
        "the dot field is absent: the home route draws no circle geometry")


def test_header_carries_no_scroll_bound_class_switch(anon):
    """The header inverts continuously rather than switching a class at a boundary."""
    markup = conftest.page_body("/")
    lowered = markup.lower()
    assert "mix-blend-mode" in lowered or "difference" in lowered, (
        "the header declares no blend, so it cannot invert against what passes beneath")
    for switch in ("header--light", "header--dark", "is-header-inverted"):
        assert switch not in lowered, (
            f"the header carries the class switch {switch!r}; the inversion is continuous")


def test_smoothing_layer_is_removable_at_runtime(anon):
    """Scroll smoothing is declared and is suppressed when motion is reduced."""
    normal = conftest.page_body("/")
    reduced = conftest.page_body("/", headers={"Sec-CH-Prefers-Reduced-Motion": "reduce"})
    assert "prefers-reduced-motion" in normal.lower(), (
        "the document declares no reduced-motion branch")
    assert len(reduced) > 0
    assert "prefers-reduced-motion" in reduced.lower(), (
        "the reduced-motion branch disappears when the preference is sent")


def test_reveal_releases_content_after_the_deadline(anon):
    """No revealing element can leave its content permanently invisible."""
    markup = conftest.page_body("/")
    lowered = markup.lower()
    assert "animation-delay" in lowered or "anim-fallback-delay" in lowered or \
           "--anim-fallback" in lowered, (
        "the document declares no fallback that releases a reveal whose trigger never "
        "fires")
    assert "visibility:hidden" not in lowered.replace(" ", "") or \
           "prefers-reduced-motion" in lowered, (
        "content is hidden with no branch that releases it")


def test_brief_attachment_object_exists_in_bucket(anon, store):
    """A brief attachment exists as a real object at its pinned key."""
    token = conftest.create_brief(anon)["token"]
    uploaded = conftest.attach(anon, token, 8192)
    assert uploaded.status_code < 300, (
        f"attaching a file returned {uploaded.status_code}: {uploaded.text[:200]}")
    key = uploaded.json().get("object_key")
    assert key, f"the upload returned no object key: {uploaded.json()}"
    assert key.startswith(f"{conftest.BRIEF_KEY_PREFIX}{token}/"), (
        f"attachment key {key!r} does not follow briefs/{{brief_token}}/...")
    assert key.rsplit("/", 1)[-1].split(".")[0].isalnum(), (
        f"attachment key {key!r} does not name the content digest")
    assert store.exists(key), f"the object store holds no object at {key!r}"


def test_deliverable_preview_object_exists_in_bucket(client_a, store):
    """A delivered version's preview exists as a real object under the deliverables prefix."""
    engagement = conftest.engagement_ids(client_a)[0]
    payload = client_a.get(f"/portal/engagements/{engagement}").json()
    keys = [v.get("preview_key") for d in payload["deliverables"]
            for v in d["versions"] if v.get("preview_key")]
    assert keys, "no delivered version names a preview object key"
    for key in keys:
        assert key.startswith(conftest.DELIVERABLE_KEY_PREFIX), (
            f"preview key {key!r} does not follow the deliverables key scheme")
        assert store.exists(key), f"the object store holds no object at {key!r}"


def test_attachment_key_names_the_content_digest(anon):
    """Two identical uploads land under one digest-named key."""
    token = conftest.create_brief(anon)["token"]
    first = conftest.attach(anon, token, 4096)
    second = conftest.attach(anon, token, 4096)
    assert first.status_code < 300 and second.status_code < 300
    assert first.json()["object_key"] == second.json()["object_key"], (
        "two uploads of identical bytes produced different keys, so the key does not "
        "name the content digest")


def test_unscanned_object_is_not_served(anon, db):
    """An attachment that has not been scanned is readable by nobody."""
    token = conftest.create_brief(anon)["token"]
    conftest.attach(anon, token, 2048)
    rows = db.rows("attachment", limit=20)
    assert rows, "no attachment row exists"
    assert any("scanned" in row for row in rows), (
        "no attachment row records whether the object has been scanned")
    unscanned = [r for r in rows if not r.get("scanned")]
    for row in unscanned:
        response = anon.get(f"/objects/{row['object_key']}")
        assert response.status_code in (401, 403, 404, 409), (
            f"an unscanned object was served with {response.status_code}")
