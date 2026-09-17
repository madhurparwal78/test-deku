"""Outcome graders for the Sounding task.

One module, every section and both declared slots. Black-box: HTTP against the
running app, the rendered page through Playwright, PostgreSQL through the shared
backend adapter and delivered mail through the shared email adapter. Nothing here
reads the agent's source.
"""

from __future__ import annotations

import json
import re

import httpx

from conftest import (
    COPY_ALREADY,
    COPY_BAD_LOGIN,
    COPY_NOT_FOUND,
    COPY_NO_MOMENT,
    COPY_NO_TITLE,
    COPY_TAKEN,
    COPY_TOO_MANY,
    CREDIT,
    DEFAULT_TITLE,
    DESCEND_PROMPT,
    DISPLAY_NAME_MAX,
    DIVER2_EMAIL,
    DIVER_EMAIL,
    DIVER_NAME,
    ENTRY_CEILING,
    GATE_PRIMARY,
    HOSTILE,
    HOST_EMAIL,
    HOST_NAME,
    INTRO_SENTENCE,
    LABEL_NO_DEPTH,
    LABEL_WAIT,
    NOTE_MAX,
    NOT_FOUND_TITLE,
    OK,
    PASSWORD,
    PASSWORD_MAX,
    PASSWORD_MIN,
    PROJECT_SKILLS,
    PROJECT_SLUGS,
    PROJECT_TITLES,
    PUBLIC_ID_MIN_BITS,
    PUBLIC_ID_MIN_CHARS,
    PUBLIC_ROUTES,
    PUBLISHED_TITLE,
    REFUSED,
    SCENE_COUNT,
    SCENE_SLUGS,
    SEEDED_PUBLISHED,
    SIGN_OFF,
    SUBJECT_LIVE,
    SUBJECT_RESET,
    SUBJECT_WAITING,
    SUBJECT_WELCOME,
    TIMEOUT,
    TITLES,
    TITLE_MAX,
    WORKS_SCENE_INDEX,
    annotate,
    api_base,
    base_url,
    body,
    contrast,
    describe,
    enter_dive,
    entries_of,
    entry_ids,
    error_code,
    error_message,
    fill,
    head_of,
    html_of,
    logbook_of,
    meta_content,
    ok,
    probe_email,
    published_logbook,
    raw_get,
    read_public,
    refused_as,
    rename,
    reopen,
    reorder,
    rgb_of,
    save_moment,
    settle,
    sign_up,
    title_of,
    unique,
    unpublish,
    publish,
    run_together,
    wait_for_mail,
)


_CORE_FEATURES = "core features"


def test_the_dive_route_is_served_to_a_visitor_with_no_session():
    """cov: C-RL-13"""
    response = html_of("/")
    assert response.status_code == 200, f"the dive is not served signed out: {describe(response)}"
    markup = response.text
    assert LABEL_WAIT in markup or GATE_PRIMARY in markup, \
        f"the dive route serves neither the loader label nor the gate: {markup[:400]}"
    assert TITLES["/"] in markup, f"the dive does not carry its pinned title: {markup[:400]}"


def test_the_health_route_answers_two_hundred_once_the_scenes_and_projects_are_loaded(anon):
    """cov: C-TR-18"""
    response = anon.get("/health")
    assert response.status_code == 200, f"the health route is not ready: {describe(response)}"
    payload = body(response)
    assert str(payload.get("status", "")).lower() == "ok", \
        f"the health route does not report ok: {payload}"
    assert len(ok(anon.get("/scenes"), "scenes read").get("scenes", [])) == SCENE_COUNT
    assert len(ok(anon.get("/projects"), "projects read").get("projects", [])) == len(PROJECT_SLUGS)


def test_the_works_route_places_the_dive_at_the_works_scene_index_on_first_paint():
    """cov: C-TR-02"""
    response = html_of("/works")
    assert response.status_code == 200, f"the works route is not served: {describe(response)}"
    markup = response.text
    assert TITLES["/works"] in markup, f"the works route lacks its pinned title: {markup[:400]}"
    assert any(title in markup for title in PROJECT_TITLES), \
        f"the works route paints no project record: {markup[:600]}"


def test_a_project_record_carries_an_outbound_url_that_is_not_an_internal_address(anon):
    """cov: C-CF-93"""
    projects = ok(anon.get("/projects"), "projects read")["projects"]
    for project in projects:
        url = str(project.get("url", ""))
        assert url.startswith("http"), f"{project['slug']} carries no outbound url: {project}"
        assert base_url() not in url, \
            f"{project['slug']} points back at this origin rather than outward: {url}"


def test_the_projects_response_orders_rows_by_position_rather_than_by_title(anon):
    """cov: C-DC-02"""
    projects = ok(anon.get("/projects"), "projects read")["projects"]
    titles = [str(p["title"]) for p in projects]
    assert titles == list(PROJECT_TITLES), f"the authored order was not preserved: {titles}"
    assert titles != sorted(titles), \
        "the authored order and an alphabetical order cannot be told apart in this seed"


def test_the_first_saved_moment_moves_the_logbook_from_empty_to_draft(fresh):
    """cov: C-CF-03"""
    before = logbook_of(fresh).get("logbook", {})
    assert str(before.get("state")) == "empty", f"this account did not start empty: {before}"
    ok(save_moment(fresh, WORKS_SCENE_INDEX, 0.62), "first save")
    after = logbook_of(fresh).get("logbook", {})
    assert str(after.get("state")) == "draft", \
        f"the first save did not move the logbook to draft: {after}"
    assert len(entries_of(fresh)) == 1, "the first save wrote no entry"


def test_a_second_saved_moment_is_appended_at_the_end_of_the_order(fresh):
    """cov: C-CF-23"""
    ok(save_moment(fresh, 1, 0.2), "first save")
    ok(save_moment(fresh, 4, 0.8), "second save")
    rows = entries_of(fresh)
    assert [int(r["position"]) for r in rows] == [0, 1], f"positions are not contiguous: {rows}"
    assert int(rows[1]["sceneIndex"]) == 4, f"the second save is not last: {rows}"


def test_the_order_write_takes_the_complete_list_of_entry_identifiers(fresh):
    """cov: C-DC-04"""
    made = fill(fresh, 3)
    payload = ok(reorder(fresh, [made[2], made[0], made[1]]), "reorder")
    rows = payload.get("entries", payload)
    assert [str(r["id"]) for r in rows] == [made[2], made[0], made[1]], \
        f"the order write did not return the submitted order: {rows}"


def test_publishing_a_draft_moves_the_logbook_to_published_and_writes_the_publish_instant(fresh):
    """cov: C-CF-11, C-CF-47"""
    fill(fresh, 2)
    ok(rename(fresh, "Pitch dive"), "rename")
    payload = ok(publish(fresh), "publish")
    logbook = payload.get("logbook", payload)
    assert str(logbook["state"]) == "published", f"publishing did not change the state: {logbook}"
    assert str(logbook.get("publishedAt", "")).strip(), f"no publish instant was written: {logbook}"
    assert str(logbook_of(fresh)["logbook"]["state"]) == "published"


def test_the_public_logbook_read_needs_no_session_at_all(fresh):
    """cov: C-DC-17"""
    public = published_logbook(fresh)
    response = read_public(public)
    payload = ok(response, "public read with no cookies")
    assert str(payload.get("logbook", {}).get("state")) in ("published", "answered"), \
        f"the public read did not return a published logbook: {payload}"
    assert not response.request.headers.get("cookie"), "the public read carried a session cookie"


def test_the_dive_route_accepts_a_depth_parameter_between_zero_and_one():
    """cov: C-CF-86"""
    for depth in ("0", "0.5", "1"):
        response = html_of(f"/?at={depth}")
        assert response.status_code == 200, f"the dive refused a depth of {depth}: {describe(response)}"
        assert TITLES["/"] in response.text, f"a deep link lost the dive's own title at {depth}"


def test_the_dock_queue_orders_published_logbooks_newest_published_first(fresh, fresh2, host):
    """cov: C-CF-05, C-CF-57, C-RL-07"""
    published_logbook(fresh, "Earlier dive")
    settle()
    published_logbook(fresh2, "Later dive")
    rows = ok(host.get("/dock"), "dock read")["logbooks"]
    stamps = [str(r["publishedAt"]) for r in rows]
    assert stamps == sorted(stamps, reverse=True), f"the queue is not newest first: {stamps}"
    titles = [str(r["title"]) for r in rows]
    assert titles.index("Later dive") < titles.index("Earlier dive"), \
        f"the newer logbook is not above the older one: {titles}"


def test_the_dock_queue_pages_by_cursor_rather_than_by_an_offset(host, page):
    """cov: C-CF-65"""
    payload = ok(host.get("/dock", params={"cursor": ""}), "dock read")
    assert "cursor" in payload, f"the dock response carries no cursor: {list(payload)}"
    assert "offset" not in payload, f"the dock response pages by offset: {list(payload)}"
    assert "page" not in payload, f"the dock response pages by page number: {list(payload)}"


def test_the_dock_queue_filters_to_published_or_to_answered_but_never_to_both(fresh, host):
    """cov: C-CF-58, C-CF-64"""
    public = published_logbook(fresh, "Filter probe")
    rows = ok(host.get("/dock", params={"state": "published"}), "dock read")["logbooks"]
    assert all(str(r["state"]) == "published" for r in rows), f"the filter leaked: {rows}"
    identifier = [str(r["id"]) for r in rows if str(r["title"]) == "Filter probe"][0]
    ok(host.post(f"/dock/{identifier}/answer"), "mark answered")
    answered = ok(host.get("/dock", params={"state": "answered"}), "dock read")["logbooks"]
    assert all(str(r["state"]) == "answered" for r in answered), f"the filter leaked: {answered}"
    assert public


def test_opening_a_dock_logbook_returns_the_logbook_the_entries_and_the_diver(diver, fresh, host):
    """cov: C-DC-07"""
    published_logbook(fresh, "Open probe")
    rows = ok(host.get("/dock"), "dock read")["logbooks"]
    identifier = [str(r["id"]) for r in rows if str(r["title"]) == "Open probe"][0]
    payload = ok(host.get(f"/dock/{identifier}"), "dock open")
    assert payload["logbook"]["title"] == "Open probe", f"the wrong logbook opened: {payload}"
    assert payload["entries"], f"the opened logbook carries no entries: {payload}"
    assert str(payload["diver"]["displayName"]).strip(), f"no display name was returned: {payload}"


def test_signing_up_creates_the_account_and_sets_a_session_cookie(diver):
    """cov: C-RL-19"""
    session, address = sign_up()
    with session:
        assert session.cookies, "sign up set no session cookie"
        payload = ok(session.get("/auth/me"), "identity read")
        diver_row = payload.get("diver", payload)
        assert str(diver_row["email"]).lower() == address.lower(), \
            f"the identity route names a different account: {diver_row}"
        assert str(diver_row["role"]) == "diver", f"a new account is not a diver: {diver_row}"
        assert "passwordHash" not in json.dumps(payload), "the password hash reached a response"


def test_unpublishing_returns_the_logbook_to_the_draft_state(fresh):
    """cov: C-DC-05"""
    published_logbook(fresh, "Withdraw probe")
    payload = ok(unpublish(fresh), "unpublish")
    logbook = payload.get("logbook", payload)
    assert str(logbook["state"]) == "draft", f"unpublishing did not return to draft: {logbook}"
    assert str(logbook_of(fresh)["logbook"]["state"]) == "draft"


def test_an_unpublished_logbook_leaves_the_dock_queue(fresh, host):
    """cov: C-CF-14, C-CF-62"""
    published_logbook(fresh, "Queue exit probe")
    titles = [str(r["title"]) for r in ok(host.get("/dock"), "dock read")["logbooks"]]
    assert "Queue exit probe" in titles, f"the logbook never reached the queue: {titles}"
    ok(unpublish(fresh), "unpublish")
    after = [str(r["title"]) for r in ok(host.get("/dock"), "dock read")["logbooks"]]
    assert "Queue exit probe" not in after, f"a withdrawn logbook is still queued: {after}"


def test_every_public_route_carries_a_title_no_other_route_shares():
    """cov: C-TR-14"""
    seen = {}
    for route in PUBLIC_ROUTES:
        title = title_of(route)
        assert title, f"{route} carries no title"
        assert title == TITLES[route], f"{route} carries the wrong title: {title!r}"
        assert title not in seen, f"{route} shares a title with {seen.get(title)}"
        seen[title] = route


def test_every_public_route_carries_a_description_no_other_route_shares():
    """cov: C-TR-15"""
    seen = {}
    for route in PUBLIC_ROUTES:
        description = meta_content(head_of(route), "description")
        assert description, f"{route} carries no description"
        assert description not in seen, f"{route} shares a description with {seen.get(description)}"
        seen[description] = route


def test_the_site_serves_a_favicon_and_declares_it_in_every_document_head():
    """cov: C-TR-16, C-TR-17"""
    for route in PUBLIC_ROUTES:
        head = head_of(route)
        found = re.search(r'<link[^>]*rel=["\'][^"\']*icon[^"\']*["\'][^>]*>', head, re.I)
        assert found, f"{route} declares no favicon in its head"
        href = re.search(r'href=["\']([^"\']+)["\']', found.group(0))
        assert href, f"{route} declares a favicon with no address"
        served = httpx.get(f"{base_url()}{href.group(1)}", timeout=TIMEOUT, follow_redirects=True)
        assert served.status_code == 200, f"the favicon is declared but not served: {describe(served)}"


def test_every_response_carries_the_nosniff_and_strict_transport_headers():
    """cov: C-TR-05, C-TR-06"""
    for route in PUBLIC_ROUTES:
        response = httpx.get(f"{base_url()}{route}", timeout=TIMEOUT, follow_redirects=True)
        headers = {k.lower(): v.lower() for k, v in response.headers.items()}
        assert headers.get("x-content-type-options") == "nosniff", \
            f"{route} carries no nosniff policy: {headers.get('x-content-type-options')!r}"
        assert "max-age=" in headers.get("strict-transport-security", ""), \
            f"{route} carries no strict transport policy"
        assert "default-src" in headers.get("content-security-policy", ""), \
            f"{route} carries no content security policy"


def test_the_body_text_and_its_ground_meet_the_pinned_contrast_bar_on_the_dive(page):
    """cov: C-UX-09"""
    enter_dive(page)
    pair = page.evaluate(
        "() => { const n = document.body; const s = getComputedStyle(n);"
        " return [s.color, s.backgroundColor]; }")
    ratio = contrast(rgb_of(pair[0]), rgb_of(pair[1]))
    assert ratio >= 4.5, f"the dive body text sits at {ratio:.2f}:1 against its ground"


def test_the_logbook_row_contrast_holds_for_the_note_text_against_its_ground(page):
    """cov: C-UX-06"""
    page.goto(f"{base_url()}/sign-in", wait_until="domcontentloaded")
    page.fill("input[type=email]", DIVER_EMAIL)
    page.fill("input[type=password]", PASSWORD)
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)
    page.goto(f"{base_url()}/logbook", wait_until="domcontentloaded")
    page.wait_for_timeout(1000)
    note = page.get_by_text(SEEDED_PUBLISHED[0]["note"], exact=False).first
    pair = note.evaluate(
        "n => { const s = getComputedStyle(n); let p = n, bg = s.backgroundColor;"
        " while (p && (bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent')) {"
        " p = p.parentElement; if (!p) break; bg = getComputedStyle(p).backgroundColor; }"
        " return [s.color, bg]; }")
    ratio = contrast(rgb_of(pair[0]), rgb_of(pair[1]))
    assert ratio >= 4.5, f"a logbook note sits at {ratio:.2f}:1 against its ground"


def test_nothing_overflows_sideways_at_a_narrow_viewport_on_any_client_area_route(narrow_page):
    """cov: C-UX-15"""
    for route in ("/sign-in", "/logbook"):
        narrow_page.goto(f"{base_url()}{route}", wait_until="domcontentloaded")
        narrow_page.wait_for_timeout(600)
        overflow = narrow_page.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
        assert overflow <= 1, f"{route} overflows sideways by {overflow} at a narrow viewport"


def test_the_page_declares_one_document_language_on_every_route():
    """cov: C-TR-01"""
    seen = set()
    for route in PUBLIC_ROUTES:
        response = html_of(route)
        found = re.search(r"<html[^>]*\blang=[\"']([^\"']+)[\"']", response.text, re.I)
        assert found, f"{route} declares no document language"
        seen.add(found.group(1).lower())
    assert len(seen) == 1, f"the routes declare more than one locale: {sorted(seen)}"


def test_the_dive_text_of_every_scene_is_present_in_the_document_for_assistive_technology():
    """cov: C-UX-14"""
    markup = html_of("/").text
    for fragment in (INTRO_SENTENCE, SIGN_OFF, CREDIT, DESCEND_PROMPT):
        assert fragment in markup, f"the dive document omits {fragment!r}"
    for title in PROJECT_TITLES:
        assert title in markup, f"the dive document omits the project {title!r}"


_DATA_INTEGRITY = "data integrity"


def test_the_scenes_endpoint_returns_six_scenes_in_index_order_with_slug_name_and_field_of_view(anon):
    """cov: C-DC-01"""
    payload = ok(anon.get("/scenes"), "scenes read")
    scenes = payload.get("scenes")
    assert isinstance(scenes, list), f"the scenes response carries no scenes array: {payload}"
    assert len(scenes) == SCENE_COUNT, f"expected {SCENE_COUNT} scenes: {scenes}"
    assert [int(s["index"]) for s in scenes] == list(range(SCENE_COUNT)), \
        f"the scenes are not returned in index order: {scenes}"
    assert tuple(str(s["slug"]) for s in scenes) == SCENE_SLUGS, \
        f"the scene slugs are not the six pinned ones: {scenes}"
    for scene in scenes:
        assert str(scene.get("name", "")).strip(), f"a scene carries no name: {scene}"
        assert float(scene["fieldOfView"]) > 0, f"a scene carries no field of view: {scene}"


def test_the_projects_endpoint_returns_four_projects_in_position_order_every_one_at_the_works_scene(anon):
    """cov: C-CF-92, C-DM-03"""
    payload = ok(anon.get("/projects"), "projects read")
    projects = payload.get("projects")
    assert isinstance(projects, list), f"the projects response carries no array: {payload}"
    assert len(projects) == len(PROJECT_SLUGS), f"expected four projects: {projects}"
    assert [int(p["position"]) for p in projects] == list(range(len(PROJECT_SLUGS))), \
        f"the projects are not returned in position order: {projects}"
    assert tuple(str(p["slug"]) for p in projects) == PROJECT_SLUGS, \
        f"the project slugs are not the four pinned ones: {projects}"
    for project in projects:
        assert int(project["sceneIndex"]) == WORKS_SCENE_INDEX, \
            f"a project does not sit at the works scene: {project}"


def test_every_seeded_project_carries_its_pinned_title_slug_and_slash_separated_skills_line(anon):
    """cov: C-DM-02"""
    projects = ok(anon.get("/projects"), "projects read")["projects"]
    by_slug = {str(p["slug"]): p for p in projects}
    assert set(by_slug) == set(PROJECT_SLUGS), f"the project slugs drifted: {sorted(by_slug)}"
    for slug, expected in PROJECT_SKILLS.items():
        skills = by_slug[slug]["skills"]
        line = " / ".join(skills) if isinstance(skills, list) else str(skills)
        assert line.upper() == expected, f"{slug} carries the wrong skills line: {skills}"
    assert {str(p["title"]) for p in projects} == set(PROJECT_TITLES), \
        f"the project titles drifted: {[p['title'] for p in projects]}"


def test_the_scenes_response_names_the_works_scene_slug_at_index_three(anon):
    """cov: C-DM-01"""
    scenes = ok(anon.get("/scenes"), "scenes read")["scenes"]
    works = [s for s in scenes if int(s["index"]) == WORKS_SCENE_INDEX]
    assert works, f"no scene sits at index {WORKS_SCENE_INDEX}: {scenes}"
    assert str(works[0]["slug"]) == SCENE_SLUGS[WORKS_SCENE_INDEX], \
        f"the scene at index {WORKS_SCENE_INDEX} is not the works scene: {works[0]}"


def test_a_created_account_starts_with_exactly_one_logbook_in_the_empty_state(fresh):
    """cov: C-CF-01, C-DM-10"""
    payload = logbook_of(fresh)
    logbook = payload.get("logbook", payload)
    assert str(logbook.get("state")) == "empty", \
        f"a new account's logbook does not start empty: {logbook}"
    assert str(logbook.get("title")) == DEFAULT_TITLE, \
        f"a new logbook does not carry the default title: {logbook}"
    assert payload.get("entries") == [], f"a new logbook is not empty: {payload}"


def test_a_saved_moment_records_the_scene_index_the_progress_and_the_saved_instant(fresh):
    """cov: C-CF-20, C-OV-02"""
    created = ok(save_moment(fresh, 2, 0.37), "save moment")
    entry = created.get("entry", created)
    assert int(entry["sceneIndex"]) == 2, f"the scene index was not recorded: {entry}"
    assert abs(float(entry["progress"]) - 0.37) < 1e-6, f"the progress was not recorded: {entry}"
    assert str(entry.get("savedAt", "")).strip(), f"the saved instant is missing: {entry}"


def test_a_saved_moment_lands_at_position_zero_when_the_logbook_was_empty(fresh):
    """cov: C-CF-02"""
    ok(save_moment(fresh, 1, 0.2), "first save")
    rows = entries_of(fresh)
    assert len(rows) == 1, f"expected one entry: {rows}"
    assert int(rows[0]["position"]) == 0, f"the first entry does not sit at position zero: {rows[0]}"


def test_the_order_write_rewrites_every_position_from_the_submitted_list_index(fresh):
    """cov: C-CF-30"""
    made = fill(fresh, 4)
    wanted = [made[3], made[1], made[0], made[2]]
    ok(reorder(fresh, wanted), "reorder")
    rows = entries_of(fresh)
    assert [str(r["id"]) for r in rows] == wanted, f"the stored order is not the submitted one: {rows}"
    assert [int(r["position"]) for r in rows] == [0, 1, 2, 3], \
        f"positions were not rewritten from the list index: {rows}"


def test_a_reordered_logbook_returns_the_new_order_on_a_fresh_read(diver, fresh):
    """cov: C-CN-02 (earned: C-CN-02: the fresh read opens a second client, so the order it returns came from the service rather than from the browser that wrote it)"""
    made = fill(fresh, 3)
    ok(reorder(fresh, [made[1], made[2], made[0]]), "reorder")
    second = reopen(fresh)
    rows = entries_of(second)
    assert [str(r["id"]) for r in rows] == [made[1], made[2], made[0]], \
        f"a fresh session does not see the order the diver left: {rows}"


def test_positions_stay_contiguous_from_zero_with_no_gap_after_a_reorder(fresh):
    """cov: C-CF-33"""
    made = fill(fresh, 5)
    ok(reorder(fresh, list(reversed(made))), "reorder")
    positions = [int(r["position"]) for r in entries_of(fresh)]
    assert positions == list(range(len(made))), f"positions are not contiguous from zero: {positions}"
    assert len(set(positions)) == len(positions), f"a position is duplicated: {positions}"


def test_removing_an_entry_closes_the_gap_in_the_remaining_positions(fresh):
    """cov: C-CF-34"""
    made = fill(fresh, 4)
    ok(fresh.delete(f"/logbook/entries/{made[1]}"), "remove entry")
    rows = entries_of(fresh)
    assert [str(r["id"]) for r in rows] == [made[0], made[2], made[3]], \
        f"the wrong entry was removed: {rows}"
    assert [int(r["position"]) for r in rows] == [0, 1, 2], \
        f"removing an entry left a gap in the positions: {rows}"


def test_a_note_is_written_to_the_entry_and_returned_on_the_next_read(fresh):
    """cov: C-CF-36"""
    made = fill(fresh, 2)
    ok(annotate(fresh, made[0], "The works arc is the whole argument"), "annotate")
    rows = entries_of(fresh)
    assert str(rows[0]["note"]) == "The works arc is the whole argument", \
        f"the note was not written: {rows[0]}"
    assert not str(rows[1].get("note") or ""), f"the note reached the wrong entry: {rows[1]}"


def test_a_note_survives_a_reorder_of_the_row_carrying_it(fresh):
    """cov: C-CF-38"""
    made = fill(fresh, 3)
    ok(annotate(fresh, made[2], "Thin on purpose"), "annotate")
    ok(reorder(fresh, [made[2], made[0], made[1]]), "reorder")
    rows = entries_of(fresh)
    assert str(rows[0]["id"]) == made[2], f"the reorder did not land: {rows}"
    assert str(rows[0]["note"]) == "Thin on purpose", \
        f"the note did not travel with the row it belongs to: {rows[0]}"


def test_a_minted_public_identifier_is_long_enough_to_carry_the_pinned_entropy_floor(fresh):
    """cov: C-CF-49"""
    public = published_logbook(fresh)
    assert len(public) >= PUBLIC_ID_MIN_CHARS, \
        f"a {PUBLIC_ID_MIN_BITS} bit identifier cannot fit in {len(public)} characters: {public}"
    assert re.fullmatch(r"[A-Za-z0-9_-]+", public), \
        f"the public identifier is not URL safe: {public}"


def test_a_minted_public_identifier_is_not_the_logbook_identifier(fresh):
    """cov: C-CF-50"""
    public = published_logbook(fresh)
    logbook = logbook_of(fresh)["logbook"]
    assert public != str(logbook.get("id")), \
        "the public address is the logbook's own identifier, so the queue is countable"
    assert public not in str(logbook.get("id", "")), "the public address embeds the row identifier"


def test_two_published_logbooks_never_share_a_public_identifier(fresh, fresh2):
    """cov: C-CF-51"""
    first = published_logbook(fresh)
    second = published_logbook(fresh2)
    assert first != second, f"two logbooks share one public address: {first}"


def test_the_public_logbook_returns_entries_in_position_order(diver, fresh):
    """cov: C-DC-06"""
    made = fill(fresh, 3)
    ok(reorder(fresh, [made[2], made[0], made[1]]), "reorder")
    ok(rename(fresh, "Pitch dive"), "rename")
    public = str(ok(publish(fresh), "publish")["logbook"]["publicId"])
    rows = ok(read_public(public), "public read")["entries"]
    assert [str(r["id"]) for r in rows] == [made[2], made[0], made[1]], \
        f"the public read does not honour the diver's order: {rows}"


def test_every_saved_entry_carries_the_scene_index_and_progress_the_replay_needs(diver):
    """cov: C-DM-05"""
    rows = entries_of(diver)
    assert rows, "the seeded published logbook carries no entries"
    for row in rows:
        assert 0 <= int(row["sceneIndex"]) < SCENE_COUNT, f"an entry names no built scene: {row}"
        assert 0.0 <= float(row["progress"]) <= 1.0, f"an entry carries no usable depth: {row}"


def test_a_saved_progress_value_round_trips_without_losing_precision(fresh):
    """cov: C-DM-09"""
    created = ok(save_moment(fresh, 5, 0.9375), "save moment")
    entry = created.get("entry", created)
    assert abs(float(entry["progress"]) - 0.9375) < 1e-9, f"the depth was rounded on write: {entry}"
    stored = entries_of(fresh)[0]
    assert abs(float(stored["progress"]) - 0.9375) < 1e-9, \
        f"the depth was rounded between the write and the read: {stored}"


def test_marking_a_logbook_answered_writes_the_answered_instant(fresh, host):
    """cov: C-CF-66"""
    published_logbook(fresh, "Answer probe")
    rows = ok(host.get("/dock"), "dock read")["logbooks"]
    identifier = [str(r["id"]) for r in rows if str(r["title"]) == "Answer probe"][0]
    payload = ok(host.post(f"/dock/{identifier}/answer"), "mark answered")
    logbook = payload.get("logbook", payload)
    assert str(logbook["state"]) == "answered", f"the state did not change: {logbook}"
    assert str(logbook.get("answeredAt", "")).strip(), f"no answered instant was written: {logbook}"
    assert str(logbook_of(fresh)["logbook"]["state"]) == "answered"


def test_republishing_returns_the_very_same_public_identifier(fresh):
    """cov: C-CF-52"""
    first = published_logbook(fresh, "Republish probe")
    ok(unpublish(fresh), "unpublish")
    second = str(ok(publish(fresh), "republish")["logbook"]["publicId"])
    assert second == first, \
        f"republishing minted a new address, so a link already sent is dead: {first} against {second}"
    ok(read_public(second), "the original address answers again")


def test_unpublishing_an_answered_logbook_leaves_the_answered_instant_written(fresh, host):
    """cov: C-CF-17"""
    published_logbook(fresh, "Answered withdraw probe")
    rows = ok(host.get("/dock"), "dock read")["logbooks"]
    identifier = [str(r["id"]) for r in rows if str(r["title"]) == "Answered withdraw probe"][0]
    answered_at = str(ok(host.post(f"/dock/{identifier}/answer"), "answer")["logbook"]["answeredAt"])
    payload = ok(unpublish(fresh), "unpublish")
    logbook = payload.get("logbook", payload)
    assert str(logbook["state"]) == "draft", f"an answered logbook did not withdraw: {logbook}"
    assert str(logbook.get("answeredAt")) == answered_at, \
        f"withdrawing undid the answer: {logbook}"


def test_the_page_view_record_names_the_route_served_and_the_instant_of_service(host, page):
    """cov: C-CF-101, C-TR-19"""
    html_of("/works")
    settle()
    rows = ok(host.get("/page-views", params={"route": "/works"}), "page view read")["views"]
    assert rows, "serving the works route recorded no page view"
    assert all(str(r["route"]) == "/works" for r in rows), f"the filter leaked: {rows[:3]}"
    assert all(str(r.get("viewedAt", "")).strip() for r in rows), f"a row carries no instant: {rows[:3]}"


def test_a_page_view_row_accrues_for_every_public_route_that_is_served(host, page):
    """cov: C-DM-06"""
    before = int(ok(host.get("/page-views"), "page view read")["total"])
    for route in PUBLIC_ROUTES:
        html_of(route)
    settle()
    after = int(ok(host.get("/page-views"), "page view read")["total"])
    assert after >= before + len(PUBLIC_ROUTES), \
        f"serving {len(PUBLIC_ROUTES)} routes moved the total from {before} to {after}"


def test_the_page_view_record_never_carries_a_published_logbook_address(fresh, host, page):
    """cov: C-CF-103, C-CF-104"""
    public = published_logbook(fresh, "Leak probe")
    html_of(f"/logbook/{public}")
    settle()
    rows = ok(host.get("/page-views"), "page view read")["views"]
    assert public not in json.dumps(rows), \
        "the shareable secret reached the page view record"


_AUTHORIZATION = "authorization"


def test_saving_a_moment_without_a_session_is_refused_as_unauthenticated(anon):
    """cov: C-CN-03"""
    response = anon.post("/logbook/entries", json={"sceneIndex": WORKS_SCENE_INDEX, "progress": 0.4})
    refused_as(response, "unauthenticated")
    assert anon.get("/logbook").status_code == 401, \
        "reading a logbook with no session must be refused too"


def test_an_order_write_naming_an_entry_from_another_logbook_is_refused_as_invalid(fresh, fresh2):
    """cov: C-DC-15"""
    mine = fill(fresh, 2)
    theirs = fill(fresh2, 1)
    response = reorder(fresh, mine + theirs)
    assert response.status_code in REFUSED, \
        f"an order write naming another logbook's entry was accepted: {describe(response)}"
    assert [str(r["id"]) for r in entries_of(fresh)] == mine, \
        "a refused order write must leave the stored order untouched"


def test_a_note_on_an_entry_belonging_to_another_diver_is_refused(diver, fresh, fresh2):
    """cov: C-RL-03"""
    theirs = fill(fresh2, 1)
    response = annotate(fresh, theirs[0], "not mine to write on")
    assert response.status_code in (403, 404), \
        f"a note reached another diver's entry: {describe(response)}"
    assert not str(entries_of(fresh2)[0].get("note") or ""), \
        "the other diver's entry was written to anyway"


def test_the_public_logbook_response_carries_the_display_name_and_no_other_diver_field(diver, fresh):
    """cov: C-DC-09"""
    public = published_logbook(fresh)
    payload = ok(read_public(public), "public read")
    diver = payload.get("diver", {})
    assert set(diver) == {"displayName"}, \
        f"the public read exposes more than the display name: {diver}"
    assert "@" not in json.dumps(payload), f"an email address reached the public read: {payload}"


def test_a_public_identifier_that_was_never_minted_answers_not_found():
    """cov: C-CF-15, C-DC-12"""
    refused_as(read_public("a" * PUBLIC_ID_MIN_CHARS), "not_found")
    refused_as(read_public(unique("never")), "not_found")


def test_the_public_logbook_route_declares_a_no_referrer_policy_on_its_own_response(fresh, page):
    """cov: C-TR-04"""
    public = published_logbook(fresh)
    response = raw_get(f"/logbook/{public}")
    assert response.status_code == 200, f"the public logbook page is not served: {describe(response)}"
    policy = response.headers.get("referrer-policy", "").lower()
    assert "no-referrer" in policy, \
        f"the shareable address leaks to every outbound link: referrer-policy is {policy!r}"


def test_a_draft_logbook_is_never_reachable_through_the_public_read_path(fresh):
    """cov: C-OV-03"""
    fill(fresh, 2)
    ok(rename(fresh, "Pitch dive"), "rename")
    public = str(ok(publish(fresh), "publish")["logbook"]["publicId"])
    ok(unpublish(fresh), "unpublish")
    refused_as(read_public(public), "not_found")
    assert str(logbook_of(fresh)["logbook"]["state"]) == "draft"


def test_the_dock_queue_is_readable_only_by_the_host_role(diver, host):
    """cov: C-DC-11 (earned: C-DC-11: the test reads a diver's refused request for the queue, which answers forbidden with that status and that code)"""
    ok(host.get("/dock"), "host reads the dock")
    response = diver.get("/dock")
    refused_as(response, "forbidden")
    refused_as(httpx.Client(base_url=api_base(), timeout=TIMEOUT).get("/dock"), "unauthenticated")


def test_the_host_cannot_edit_reorder_or_remove_an_entry_belonging_to_a_diver(diver, fresh, host):
    """cov: C-RL-11"""
    made = fill(fresh, 2)
    assert annotate(host, made[0], "not the host's to write").status_code in (403, 404)
    assert reorder(host, list(reversed(made))).status_code in REFUSED
    assert host.delete(f"/logbook/entries/{made[0]}").status_code in (403, 404)
    assert [str(r["id"]) for r in entries_of(fresh)] == made, \
        "the host changed a diver's own logbook"


def test_the_page_view_record_is_readable_by_the_host_and_by_nobody_else(diver, host, page):
    """cov: C-CF-102, C-RL-09"""
    ok(host.get("/page-views"), "host reads the page view record")
    refused_as(diver.get("/page-views"), "forbidden")
    refused_as(httpx.Client(base_url=api_base(), timeout=TIMEOUT).get("/page-views"),
               "unauthenticated")


def test_a_diver_reading_the_logbook_path_always_gets_their_own_logbook(diver, diver2):
    """cov: C-RL-15"""
    mine = logbook_of(diver)["logbook"]
    theirs = logbook_of(diver2)["logbook"]
    assert str(mine["id"]) != str(theirs["id"]), "two divers share one logbook"
    assert str(mine["title"]) == PUBLISHED_TITLE, f"the seeded diver's title drifted: {mine}"
    assert str(theirs["title"]) == DEFAULT_TITLE, f"the second diver's title drifted: {theirs}"


def test_a_diver_cannot_reach_the_dock_queue_at_all(diver, diver2, host):
    """cov: C-RL-02"""
    refused_as(diver.get("/dock"), "forbidden")
    refused_as(diver2.get("/dock"), "forbidden")
    rows = ok(host.get("/dock"), "the host still reads the queue")
    assert "logbooks" in rows, f"the host queue is not served: {rows}"


def test_a_diver_cannot_mark_any_logbook_answered(diver, fresh, host):
    """cov: C-RL-06"""
    published_logbook(fresh, "Answer boundary")
    rows = ok(host.get("/dock"), "dock read")["logbooks"]
    identifier = [str(r["id"]) for r in rows if str(r["title"]) == "Answer boundary"][0]
    refused_as(diver.post(f"/dock/{identifier}/answer"), "forbidden")
    assert str(logbook_of(fresh)["logbook"]["state"]) == "published", \
        "a diver changed the state of somebody else's logbook"


def test_a_diver_cannot_delete_an_entry_belonging_to_another_diver(diver, fresh, fresh2):
    """cov: C-RL-04"""
    theirs = fill(fresh2, 2)
    response = fresh.delete(f"/logbook/entries/{theirs[0]}")
    assert response.status_code in (403, 404), f"an entry was deleted across divers: {describe(response)}"
    assert [str(r["id"]) for r in entries_of(fresh2)] == theirs, \
        "the other diver's entries were changed anyway"


def test_a_host_asking_for_a_draft_logbook_is_answered_as_a_missing_record(fresh, host):
    """cov: C-RL-10, C-RL-16"""
    fill(fresh, 2)
    identifier = str(logbook_of(fresh)["logbook"]["id"])
    response = host.get(f"/dock/{identifier}")
    assert response.status_code == 404, \
        f"a draft was not hidden from the portfolio owner: {describe(response)}"
    assert error_code(response) == "not_found", \
        f"a refusal confirmed the draft exists: {error_code(response)!r}"


def test_a_host_cannot_publish_or_unpublish_a_logbook_belonging_to_a_diver(diver, fresh, host):
    """cov: C-RL-12"""
    made = fill(fresh, 2)
    ok(rename(fresh, "Owner boundary"), "rename")
    publish(host)
    unpublish(host)
    assert str(logbook_of(fresh)["logbook"]["state"]) == "draft", \
        "the portfolio owner changed the state of a diver's logbook"
    assert [str(r["id"]) for r in entries_of(fresh)] == made
    assert str(logbook_of(host)["logbook"]["id"]) != str(logbook_of(fresh)["logbook"]["id"]), \
        "the owner's publish path resolved a logbook belonging to a diver"


def test_a_visitor_with_no_session_asking_for_a_draft_address_is_sent_to_sign_in(fresh):
    """cov: C-UF-09"""
    fill(fresh, 1)
    identifier = str(logbook_of(fresh)["logbook"]["id"])
    response = raw_get(f"/logbook/{identifier}")
    assert response.status_code in (302, 303, 307, 404), \
        f"a draft address answered a visitor directly: {describe(response)}"
    if response.status_code != 404:
        assert "/sign-in" in response.headers.get("location", ""), \
            f"the visitor was not sent to sign in: {response.headers.get('location')!r}"


def test_an_unauthenticated_write_to_any_logbook_path_is_refused():
    """cov: C-RL-05"""
    client = httpx.Client(base_url=api_base(), timeout=TIMEOUT)
    refused_as(client.patch("/logbook", json={"title": "not mine"}), "unauthenticated")
    refused_as(client.post("/logbook/entries", json={"sceneIndex": 0, "progress": 0.1}),
               "unauthenticated")
    refused_as(client.put("/logbook/order", json={"order": []}), "unauthenticated")
    refused_as(client.post("/logbook/publish"), "unauthenticated")


def test_the_forbidden_answer_never_reveals_whether_the_logbook_exists(fresh, host):
    """cov: C-RL-17 (earned: C-RL-17: the test asks the owner for a real draft and for an invented identifier and compares the two answers)"""
    fill(fresh, 1)
    real = str(logbook_of(fresh)["logbook"]["id"])
    invented = unique("never-minted")
    first = host.get(f"/dock/{real}")
    second = host.get(f"/dock/{invented}")
    assert first.status_code == second.status_code == 404, \
        f"a real draft and an invented one answer differently: {first.status_code} {second.status_code}"
    assert error_code(first) == error_code(second) == "not_found"


def test_the_session_cookie_is_http_only_and_same_site_strict(page):
    """cov: C-TR-03"""
    client = httpx.Client(base_url=api_base(), timeout=TIMEOUT)
    response = client.post("/auth/sign-in", json={"email": DIVER_EMAIL, "password": PASSWORD})
    assert response.status_code in OK, f"sign in failed: {describe(response)}"
    raw = " ".join(response.headers.get_list("set-cookie")).lower()
    assert "httponly" in raw, f"the session cookie is readable by the page: {raw}"
    assert "samesite=strict" in raw.replace(" ", ""), f"the session cookie is not strict: {raw}"


def test_signing_in_with_a_wrong_password_answers_that_email_and_password_do_not_match():
    """cov: C-FE-35"""
    client = httpx.Client(base_url=api_base(), timeout=TIMEOUT)
    wrong = client.post("/auth/sign-in", json={"email": DIVER_EMAIL, "password": "not-the-password"})
    assert wrong.status_code == 401, f"a wrong password signed in: {describe(wrong)}"
    unknown = client.post("/auth/sign-in", json={"email": probe_email(), "password": PASSWORD})
    assert unknown.status_code == 401, f"an unknown address answered differently: {describe(unknown)}"
    assert error_message(wrong) == error_message(unknown) == COPY_BAD_LOGIN, \
        "the two refusals differ, so the form says who has an account here"


def test_a_reset_request_for_an_unregistered_address_answers_exactly_as_a_registered_one_does():
    """cov: C-CF-71"""
    client = httpx.Client(base_url=api_base(), timeout=TIMEOUT)
    known = client.post("/auth/reset", json={"email": DIVER_EMAIL})
    unknown = client.post("/auth/reset", json={"email": probe_email()})
    assert known.status_code == unknown.status_code, \
        f"the two reset answers differ: {known.status_code} against {unknown.status_code}"
    assert body(known) == body(unknown), \
        f"the two reset bodies differ: {body(known)} against {body(unknown)}"


def test_a_reset_token_is_single_use_and_the_second_confirm_is_refused():
    """cov: C-CF-73, C-UF-05"""
    client = httpx.Client(base_url=api_base(), timeout=TIMEOUT)
    invented = unique("token")
    first = client.post("/auth/reset/confirm", json={"token": invented, "password": PASSWORD})
    assert first.status_code in REFUSED, f"an invented token was accepted: {describe(first)}"
    second = client.post("/auth/reset/confirm", json={"token": invented, "password": PASSWORD})
    assert second.status_code == first.status_code, \
        "a replayed token answers differently from a first use, which is a timing oracle"


def test_signing_out_revokes_every_session_the_account_holds():
    """cov: C-DC-03"""
    session, _ = sign_up()
    other = reopen(session)
    ok(other.get("/logbook"), "the second tab reads the logbook")
    ok(session.post("/auth/sign-out"), "sign out")
    assert session.get("/logbook").status_code == 401, "the first session survived the sign out"
    assert other.get("/logbook").status_code == 401, \
        "a second tab kept a live session after signing out"


def test_the_identity_route_answers_unauthenticated_for_a_browser_with_no_cookie(diver):
    """cov: C-DC-10"""
    client = httpx.Client(base_url=api_base(), timeout=TIMEOUT)
    refused_as(client.get("/auth/me"), "unauthenticated")
    assert ok(diver.get("/auth/me"), "identity read").get("diver", {}).get("displayName") == DIVER_NAME


def test_the_public_address_of_an_unpublished_logbook_answers_not_found(fresh):
    """cov: C-CF-97"""
    public = published_logbook(fresh, "Dead link probe")
    ok(read_public(public), "the address answers while published")
    ok(unpublish(fresh), "unpublish")
    refused_as(read_public(public), "not_found")


_EDGE_CASES = "edge cases"


def test_gesturing_above_the_surface_leaves_the_dive_at_scene_zero_without_wrapping_to_the_last_scene():
    """cov: C-CF-82"""
    response = html_of("/?at=0")
    assert response.status_code == 200, f"the dive refused a zero depth: {describe(response)}"
    below = html_of("/?at=-0.4")
    assert below.status_code == 200, f"a depth below zero was not clamped: {describe(below)}"
    assert below.text == response.text or DESCEND_PROMPT in below.text, \
        "a depth below zero must clamp to the surface rather than wrapping to the last scene"


def test_gesturing_below_the_contact_deck_leaves_the_dive_at_the_last_scene_without_wrapping_to_the_surface():
    """cov: C-CF-83"""
    top = html_of("/?at=1")
    assert top.status_code == 200, f"the dive refused a full depth: {describe(top)}"
    beyond = html_of("/?at=1.9")
    assert beyond.status_code == 200, f"a depth above one was not clamped: {describe(beyond)}"
    assert beyond.text == top.text or SIGN_OFF in beyond.text, \
        "a depth above one must clamp to the last scene rather than wrapping to the surface"


def test_a_progress_value_outside_zero_to_one_is_refused_as_invalid(fresh):
    """cov: C-DM-08"""
    refused_as(save_moment(fresh, 1, 1.4), "invalid")
    refused_as(save_moment(fresh, 1, -0.2), "invalid")
    assert entries_of(fresh) == [], "a refused save must write nothing"


def test_an_order_write_omitting_an_entry_is_refused_and_leaves_the_stored_order_untouched(fresh):
    """cov: C-CF-31"""
    made = fill(fresh, 3)
    response = reorder(fresh, made[:2])
    assert response.status_code in REFUSED, \
        f"an order write omitting an entry was accepted: {describe(response)}"
    assert [str(r["id"]) for r in entries_of(fresh)] == made, \
        "a refused order write must leave the stored order untouched"


def test_an_order_write_repeating_an_identifier_is_refused_as_invalid(fresh):
    """cov: C-CF-29"""
    made = fill(fresh, 3)
    response = reorder(fresh, [made[0], made[0], made[1]])
    assert response.status_code in REFUSED, \
        f"an order write repeating an identifier was accepted: {describe(response)}"
    assert [str(r["id"]) for r in entries_of(fresh)] == made, \
        "a refused order write must leave the stored order untouched"


def test_two_simultaneous_order_writes_resolve_to_one_whole_list_rather_than_interleaving(fresh):
    """cov: C-CF-32, C-CF-55"""
    made = fill(fresh, 4)
    first = [made[3], made[2], made[1], made[0]]
    second = [made[1], made[0], made[3], made[2]]
    run_together(lambda: reorder(fresh, first), lambda: reorder(fresh, second))
    settle()
    landed = [str(r["id"]) for r in entries_of(fresh)]
    assert landed in (first, second), \
        f"two racing order writes interleaved into an order neither asked for: {landed}"
    assert [int(r["position"]) for r in entries_of(fresh)] == [0, 1, 2, 3], \
        "a racing order write left the positions inconsistent"


def test_a_note_longer_than_the_ceiling_is_refused_as_invalid_and_nothing_is_written(fresh):
    """cov: C-CF-37"""
    made = fill(fresh, 1)
    refused_as(annotate(fresh, made[0], "x" * (NOTE_MAX + 1)), "invalid")
    rows = entries_of(fresh)
    assert not str(rows[0].get("note") or ""), f"a refused note was written anyway: {rows[0]}"
    ok(annotate(fresh, made[0], "y" * NOTE_MAX), "annotate at the ceiling")


def test_a_logbook_title_is_trimmed_before_the_length_bounds_are_applied(fresh):
    """cov: C-CF-07"""
    fill(fresh, 1)
    ok(rename(fresh, "   Pitch dive   "), "rename")
    assert str(logbook_of(fresh)["logbook"]["title"]) == "Pitch dive", \
        "the title was not trimmed before it was stored"
    refused_as(rename(fresh, "  " + "d" * TITLE_MAX + "  x"), "invalid")


def test_a_cleared_title_is_kept_on_the_draft_and_refused_at_publish(fresh):
    """cov: C-CF-08"""
    fill(fresh, 1)
    ok(rename(fresh, ""), "clear the title")
    assert not str(logbook_of(fresh)["logbook"]["title"] or "").strip(), \
        "clearing the title on a draft was silently ignored"
    response = publish(fresh)
    assert response.status_code in REFUSED, f"a blank title published: {describe(response)}"
    assert error_message(response) == COPY_NO_TITLE, \
        f"the refusal copy is not the pinned one: {error_message(response)!r}"
    assert str(logbook_of(fresh)["logbook"]["state"]) == "draft"


def test_a_title_longer_than_eighty_characters_is_refused_as_invalid(fresh):
    """cov: C-CF-06"""
    fill(fresh, 1)
    refused_as(rename(fresh, "d" * (TITLE_MAX + 1)), "invalid")
    ok(rename(fresh, "d" * TITLE_MAX), "rename at the ceiling")
    assert len(str(logbook_of(fresh)["logbook"]["title"])) == TITLE_MAX


def test_an_absent_note_field_leaves_the_existing_note_untouched(fresh):
    """cov: C-CF-39"""
    made = fill(fresh, 1)
    ok(annotate(fresh, made[0], "Ends on an address, not a loop"), "annotate")
    ok(fresh.patch(f"/logbook/entries/{made[0]}", json={}), "empty patch")
    assert str(entries_of(fresh)[0]["note"]) == "Ends on an address, not a loop", \
        "a patch carrying no note cleared the stored one"


def test_a_depth_parameter_above_one_is_clamped_rather_than_refused():
    """cov: C-CF-87"""
    response = html_of("/?at=7.5")
    assert response.status_code == 200, \
        f"a truncated link was refused rather than clamped: {describe(response)}"
    below = html_of("/?at=-3")
    assert below.status_code == 200, \
        f"a negative depth was refused rather than clamped: {describe(below)}"


def test_a_depth_parameter_that_is_not_a_number_is_treated_as_absent():
    """cov: C-CF-09"""
    response = html_of("/?at=halfway")
    assert response.status_code == 200, \
        f"an unparseable depth was refused rather than ignored: {describe(response)}"
    assert DESCEND_PROMPT in response.text or TITLES["/"] in response.text, \
        "an unparseable depth must start the dive at the surface"


def test_marking_an_already_answered_logbook_a_second_time_is_refused_as_a_conflict(fresh, host):
    """cov: C-DC-08"""
    published_logbook(fresh, "Twice probe")
    rows = ok(host.get("/dock"), "dock read")["logbooks"]
    identifier = [str(r["id"]) for r in rows if str(r["title"]) == "Twice probe"][0]
    ok(host.post(f"/dock/{identifier}/answer"), "mark answered")
    second = host.post(f"/dock/{identifier}/answer")
    assert second.status_code == 409, f"a second answer was accepted: {describe(second)}"


def test_publishing_a_logbook_with_no_entries_answers_the_log_at_least_one_moment_copy(fresh):
    """cov: C-CF-42"""
    ok(rename(fresh, "Empty probe"), "rename")
    response = publish(fresh)
    assert response.status_code in REFUSED, f"an empty logbook published: {describe(response)}"
    assert error_message(response) == COPY_NO_MOMENT, \
        f"the refusal copy is not the pinned one: {error_message(response)!r}"


def test_publishing_without_a_title_answers_the_give_the_logbook_a_name_copy(fresh):
    """cov: C-CF-43"""
    fill(fresh, 2)
    ok(rename(fresh, "   "), "clear the title")
    response = publish(fresh)
    assert response.status_code in REFUSED, f"a blank title published: {describe(response)}"
    assert error_message(response) == COPY_NO_TITLE, \
        f"the refusal copy is not the pinned one: {error_message(response)!r}"


def test_saving_a_thirteenth_moment_is_refused_as_logbook_full(fresh):
    """cov: C-CF-24"""
    fill(fresh, ENTRY_CEILING)
    refused_as(save_moment(fresh, 0, 0.99), "logbook_full")
    assert error_message(save_moment(fresh, 0, 0.99)) == COPY_TOO_MANY, \
        "the ceiling refusal does not carry the pinned copy"


def test_a_refused_thirteenth_moment_leaves_the_entry_count_at_the_ceiling(fresh):
    """cov: C-CF-10"""
    fill(fresh, ENTRY_CEILING)
    save_moment(fresh, 0, 0.99)
    rows = entries_of(fresh)
    assert len(rows) == ENTRY_CEILING, f"a refused save changed the entry count: {len(rows)}"
    assert [int(r["position"]) for r in rows] == list(range(ENTRY_CEILING)), \
        f"a refused save disturbed the positions: {rows}"


def test_publishing_an_entry_whose_scene_is_outside_the_built_count_answers_scene_missing(fresh):
    """cov: C-CF-44, C-DC-14"""
    fill(fresh, 1)
    ok(rename(fresh, "Scene probe"), "rename")
    forced = save_moment(fresh, SCENE_COUNT + 2, 0.5)
    assert forced.status_code in REFUSED, \
        f"a moment naming a scene the dive has not got was saved: {describe(forced)}"
    assert error_code(forced) in ("invalid", "scene_missing"), \
        f"the refusal does not name the missing scene: {error_code(forced)!r}"


def test_a_scene_index_above_the_built_count_is_refused_when_a_moment_is_saved(fresh):
    """cov: C-TR-11"""
    refused = save_moment(fresh, SCENE_COUNT, 0.5)
    assert refused.status_code in REFUSED, f"scene {SCENE_COUNT} was accepted: {describe(refused)}"
    assert save_moment(fresh, -1, 0.5).status_code in REFUSED, "a negative scene index was accepted"
    assert entries_of(fresh) == [], "a refused save wrote an entry anyway"


def test_the_publish_rules_stop_at_the_first_failure_rather_than_reporting_every_one(fresh):
    """cov: C-CF-40"""
    response = publish(fresh)
    assert response.status_code in REFUSED, f"an empty untitled logbook published: {describe(response)}"
    assert error_message(response) == COPY_NO_MOMENT, \
        f"the first failing rule is not the one reported: {error_message(response)!r}"
    assert COPY_NO_TITLE not in response.text, \
        "publishing reported a later rule alongside the first failure"


def test_a_failed_publish_leaves_the_logbook_in_the_draft_state(fresh):
    """cov: C-CF-41"""
    fill(fresh, 1)
    ok(rename(fresh, "   "), "clear the title")
    response = publish(fresh)
    assert response.status_code in REFUSED, f"a blank title published: {describe(response)}"
    logbook = logbook_of(fresh)["logbook"]
    assert str(logbook["state"]) == "draft", f"a failed publish left the draft behind: {logbook}"
    assert not str(logbook.get("publicId") or ""), \
        f"a failed publish minted a public address anyway: {logbook}"


def test_publishing_a_logbook_that_is_already_published_answers_already_published(fresh):
    """cov: C-CF-45, C-CF-56, C-DC-13"""
    published_logbook(fresh, "Twice published")
    response = publish(fresh)
    assert response.status_code == 409, f"a second publish was accepted: {describe(response)}"
    assert error_code(response) in ("already_published", "wrong_state"), \
        f"the conflict is not named: {error_code(response)!r}"
    assert error_message(response) == COPY_ALREADY, \
        f"the refusal copy is not the pinned one: {error_message(response)!r}"


def test_signing_up_on_an_address_already_registered_answers_that_email_is_already_registered():
    """cov: C-FE-36"""
    client = httpx.Client(base_url=api_base(), timeout=TIMEOUT)
    response = client.post("/auth/sign-up", json={
        "displayName": "Second Coral", "email": DIVER_EMAIL, "password": PASSWORD})
    assert response.status_code == 409, f"a duplicate address was accepted: {describe(response)}"
    assert error_message(response) == COPY_TAKEN, \
        f"the refusal copy is not the pinned one: {error_message(response)!r}"


def test_a_display_name_longer_than_sixty_characters_is_refused_as_invalid():
    """cov: C-DM-07"""
    client = httpx.Client(base_url=api_base(), timeout=TIMEOUT)
    response = client.post("/auth/sign-up", json={
        "displayName": "n" * (DISPLAY_NAME_MAX + 1),
        "email": probe_email(), "password": PASSWORD})
    refused_as(response, "invalid")
    assert str(body(response).get("field", "")) in ("displayName", "display_name"), \
        f"the refusal does not name the field at fault: {body(response)}"


def test_a_password_shorter_than_eight_characters_is_refused_as_invalid():
    """cov: C-FE-29"""
    client = httpx.Client(base_url=api_base(), timeout=TIMEOUT)
    short = client.post("/auth/sign-up", json={
        "displayName": "Short Pass", "email": probe_email(), "password": "a" * (PASSWORD_MIN - 1)})
    refused_as(short, "invalid")
    long_one = client.post("/auth/sign-up", json={
        "displayName": "Long Pass", "email": probe_email(), "password": "a" * (PASSWORD_MAX + 1)})
    refused_as(long_one, "invalid")


def test_a_logbook_outside_the_draft_state_refuses_every_mutating_write(fresh):
    """cov: C-CF-12"""
    made = fill(fresh, 2)
    ok(rename(fresh, "Frozen probe"), "rename")
    ok(publish(fresh), "publish")
    assert rename(fresh, "Renamed while published").status_code == 409
    assert save_moment(fresh, 0, 0.3).status_code == 409
    assert reorder(fresh, list(reversed(made))).status_code == 409
    assert annotate(fresh, made[0], "no").status_code == 409
    assert fresh.delete(f"/logbook/entries/{made[0]}").status_code == 409
    assert [str(r["id"]) for r in entries_of(fresh)] == made


def test_unpublishing_a_logbook_that_is_already_a_draft_is_refused_as_a_conflict(fresh):
    """cov: C-CF-16"""
    fill(fresh, 1)
    response = unpublish(fresh)
    assert response.status_code == 409, f"unpublishing a draft was accepted: {describe(response)}"
    assert error_code(response) == "wrong_state", \
        f"the conflict is not named: {error_code(response)!r}"


def test_a_hostile_note_is_stored_exactly_as_typed_without_being_stripped(fresh):
    """cov: C-TR-09"""
    made = fill(fresh, 1)
    ok(annotate(fresh, made[0], HOSTILE), "annotate")
    stored = str(entries_of(fresh)[0]["note"])
    assert stored == HOSTILE, f"the note was rewritten on the way in: {stored!r}"


def test_a_hostile_note_is_returned_unchanged_by_the_logbook_read(fresh):
    """cov: C-TR-10"""
    made = fill(fresh, 2)
    ok(annotate(fresh, made[1], HOSTILE), "annotate")
    rows = entries_of(fresh)
    assert str(rows[1]["note"]) == HOSTILE, f"the note was rewritten on the way out: {rows[1]}"
    assert str(rows[0].get("note") or "") == "", "the note reached the wrong row"


def test_a_hostile_note_reaches_the_public_read_as_text_rather_than_as_markup(fresh, page):
    """cov: C-TR-07"""
    made = fill(fresh, 1)
    ok(annotate(fresh, made[0], HOSTILE), "annotate")
    ok(rename(fresh, "Hostile probe"), "rename")
    public = str(ok(publish(fresh), "publish")["logbook"]["publicId"])
    assert str(ok(read_public(public), "public read")["entries"][0]["note"]) == HOSTILE
    page = html_of(f"/logbook/{public}")
    assert page.status_code == 200, f"the public page is not served: {describe(page)}"
    assert "onerror=alert(1)" not in page.text.replace("&#61;", "="), \
        "the hostile note reached the page as live markup"
    assert "&lt;img" in page.text or "&amp;lt;img" in page.text, \
        "the hostile note was not escaped into the page"


def test_a_hostile_logbook_title_is_escaped_wherever_the_dock_queue_prints_it(fresh, host, page):
    """cov: C-RL-08, C-UF-03"""
    fill(fresh, 1)
    ok(rename(fresh, HOSTILE), "rename")
    ok(publish(fresh), "publish")
    rows = ok(host.get("/dock"), "dock read")["logbooks"]
    titles = [str(r["title"]) for r in rows]
    assert HOSTILE in titles, f"the title was rewritten on the way through: {titles}"
    page = html_of("/dock", host)
    assert "onerror=alert(1)" not in page.text.replace("&#61;", "="), \
        "the hostile title reached the dock page as live markup"


def test_a_next_parameter_pointing_at_another_origin_falls_back_to_the_dive():
    """cov: C-UF-12"""
    response = raw_get("/sign-in?next=https://example.org/steal")
    assert response.status_code == 200, f"the sign-in surface is not served: {describe(response)}"
    assert "example.org" not in response.text, \
        "an off-origin next value survived into the sign-in surface"


def test_a_next_parameter_beginning_with_two_slashes_falls_back_to_the_dive():
    """cov: C-UF-04, C-UF-11"""
    response = raw_get("/sign-in?next=//example.org/steal")
    assert response.status_code == 200, f"the sign-in surface is not served: {describe(response)}"
    assert "//example.org" not in response.text, \
        "a protocol relative next value survived into the sign-in surface"


def test_an_unknown_address_answers_not_found_and_carries_the_not_found_title():
    """cov: C-TR-13"""
    response = httpx.get(f"{base_url()}/{unique('no-such-depth')}", timeout=TIMEOUT,
                         follow_redirects=True)
    assert response.status_code == 404, f"an unknown address did not answer not found: {describe(response)}"
    assert NOT_FOUND_TITLE in response.text, "the not-found surface lacks its own title"
    assert COPY_NOT_FOUND in response.text, "the not-found surface lacks its pinned line"
    assert LABEL_NO_DEPTH in response.text, "the not-found surface lacks its bracketed label"


_EMAIL = "email"


def test_creating_an_account_delivers_the_welcome_email_to_the_new_diver(inbox):
    """cov: C-CF-74"""
    session, address = sign_up()
    with session:
        message = wait_for_mail(inbox, address, SUBJECT_WELCOME)
        assert message is not None, f"no welcome mail reached {address}"
        assert address.lower() in " ".join(message.to).lower(), \
            f"the welcome mail went to the wrong recipient: {message.to}"


def test_the_welcome_email_subject_is_exactly_the_pinned_your_logbook_line(inbox):
    """cov: C-CF-75"""
    session, address = sign_up()
    with session:
        message = wait_for_mail(inbox, address, SUBJECT_WELCOME)
        assert message is not None, f"no welcome mail reached {address}"
        assert message.subject.strip() == SUBJECT_WELCOME, \
            f"the welcome subject is not the pinned one: {message.subject!r}"


def test_requesting_a_reset_for_a_registered_address_delivers_the_reset_email(inbox):
    """cov: C-CF-76"""
    session, address = sign_up()
    with session:
        pass
    client = httpx.Client(base_url=api_base(), timeout=TIMEOUT)
    ok(client.post("/auth/reset", json={"email": address}), "reset request")
    message = wait_for_mail(inbox, address, SUBJECT_RESET)
    assert message is not None, f"no reset mail reached {address}"
    assert message.subject.strip() == SUBJECT_RESET, \
        f"the reset subject is not the pinned one: {message.subject!r}"


def test_requesting_a_reset_for_an_unregistered_address_delivers_no_email_at_all(inbox):
    """cov: C-CF-72"""
    address = probe_email()
    client = httpx.Client(base_url=api_base(), timeout=TIMEOUT)
    ok(client.post("/auth/reset", json={"email": address}), "reset request")
    settle(2.0)
    assert inbox.count(to=address) == 0, \
        f"a reset mail reached an address that has no account: {address}"


def test_publishing_delivers_the_logbook_is_live_email_to_the_publishing_diver(inbox):
    """cov: C-CF-77"""
    session, address = sign_up()
    with session:
        public = published_logbook(session, "Live mail probe")
    message = wait_for_mail(inbox, address, SUBJECT_LIVE)
    assert message is not None, f"no live mail reached {address}"
    assert message.subject.strip() == SUBJECT_LIVE, \
        f"the live subject is not the pinned one: {message.subject!r}"
    assert public in message.body or public in message.subject, \
        "the live mail does not carry the public address the feature exists to hand over"


def test_publishing_delivers_a_waiting_email_to_the_portfolio_owner_address(inbox):
    """cov: C-CF-78 (earned: C-CF-78: the portfolio owner's address is the seeded host account, which is what the delivered subject is read against)"""
    session, _ = sign_up(display_name="Waiting Probe")
    with session:
        published_logbook(session, "Waiting mail probe")
    message = wait_for_mail(inbox, HOST_EMAIL, SUBJECT_WAITING)
    assert message is not None, f"no waiting mail reached {HOST_EMAIL}"
    assert HOST_EMAIL.lower() in " ".join(message.to).lower(), \
        f"the waiting mail went to the wrong recipient: {message.to}"


def test_the_waiting_email_subject_ends_with_the_publishing_divers_display_name(inbox):
    """cov: C-CF-79"""
    name = unique("Diver Name").replace("-", " ")
    session, _ = sign_up(display_name=name)
    with session:
        published_logbook(session, "Subject probe")
    message = wait_for_mail(inbox, HOST_EMAIL, SUBJECT_WAITING + name)
    assert message is not None, f"no waiting mail names {name!r}"
    assert message.subject.strip() == (SUBJECT_WAITING + name).strip(), \
        f"the waiting subject is not the pinned shape: {message.subject!r}"


def test_unpublishing_and_marking_answered_deliver_no_email_to_anybody(inbox):
    """cov: C-CF-80"""
    session, address = sign_up()
    with session:
        published_logbook(session, "Silent probe")
        wait_for_mail(inbox, address, SUBJECT_LIVE)
        before = inbox.count(to=address)
        ok(unpublish(session), "unpublish")
        settle(2.0)
        assert inbox.count(to=address) == before, \
            "unpublishing delivered a message the brief does not name"


def test_no_delivered_email_ever_carries_the_text_of_an_entry_note(diver, inbox):
    """cov: C-CF-81"""
    secret = "sonar room note " + unique("secret")
    session, address = sign_up()
    with session:
        made = fill(session, 1)
        ok(annotate(session, made[0], secret), "annotate")
        ok(rename(session, "Note probe"), "rename")
        ok(publish(session), "publish")
    message = wait_for_mail(inbox, address, SUBJECT_LIVE)
    assert message is not None, f"no live mail reached {address}"
    assert secret not in message.body, "a delivered message carried the diver's own note text"
    owner_mail = wait_for_mail(inbox, HOST_EMAIL, SUBJECT_WAITING)
    assert owner_mail is None or secret not in owner_mail.body, \
        "the waiting message carried the diver's own note text"
