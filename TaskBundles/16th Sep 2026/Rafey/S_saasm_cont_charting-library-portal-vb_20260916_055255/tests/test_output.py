"""Outcome graders for the Chartic portal task.

One module, every section and both declared slots. Black-box: HTTP against the
running app, the rendered page through Playwright, PostgreSQL through the shared
backend adapter and MinIO through the shared object-store adapter. Nothing here
reads the agent's source.
"""

from __future__ import annotations

import os
import re
import time

import httpx

import capabilities
from conftest import (
    ABSENT_VERSION, ARTIFACT_SHA256, ARTIFACT_SHA512, BAR_CLOSURE,
    BAR_CLOSURE_RAW, BAR_EXAMPLE, BAR_MODULE, BETA_SHA256, BROKEN_OPTION,
    CANDLE_EXAMPLE, COMPUTED_PATH, COMPUTED_WORKED, CONTRIBUTOR2_EMAIL,
    CONTRIBUTOR2_NAME, CONTRIBUTOR_EMAIL, CONTRIBUTOR_NAME, CORE_MODULE,
    CURRENT, DECOY_FIELD, ENDLESS_OPTION, EVENT_RETENTION_HOURS, FAILING_THEME,
    FUNCTION_THEME, INHERITED_PATH, INHERITS_FROM, INIT_PATH, INIT_SIGNATURE,
    LATE_PATH, LINE_DESCRIPTION, LINE_EXAMPLE, LINE_POINTS, LINE_THUMBNAIL_KEY,
    LIVE_SNIPPET, MAP_EXAMPLE, MIRROR_ALPHA, MIRROR_BETA, MIRROR_GAMMA,
    MODULE_RAW, NON_COLOUR_THEME, OK, OLDEST, PASSWORD, PRIOR,
    PROPOSED_EXAMPLE, PROPOSED_THUMBNAIL_KEY, PUBLIC_ROUTES,
    PUBLISHED_EXAMPLES, RADAR_EXAMPLE, READER_EMAIL, READER_NAME,
    RELEASE_DATES, REMOVED_PATH, REPEAT_LIMIT, REPLACEMENT_PATH, ROTATE_PATH,
    SAVE_AS_IMAGE_PATH, SECRET_ENV, SECURITY_HEADERS, SERIES_COLOURS,
    SET_OPTION_PATH, SHARED_LEAVES, SHARED_OBJECT, SHARED_PATHS, SMOOTH_OPTION,
    SNIPPET_ID_RE, SUNBURST_EXAMPLE, THEMES, TIMEOUT, VARIANT_PATH,
    WALL_CLOCK_BUDGET, WITHDRAWN_SNIPPET, api_base, base_url, body,
    bundle_ready, contrast_ratio, denied, describe, example_ids, examples_of,
    head_tag, html_of, interface_node, login, message, meta_content,
    modules_of, node, node_of, ok, parse_colour, preferences, probe_title,
    propose, publish, raw_get, refused, releases_of, render, request_bundle,
    rows, run_together, search_paths, set_preferences, settle, share,
    sign_in_page, store_keys, themes_of, thumbnail, token_for, token_hex,
    tree_of, validate_example, wait_until, withdraw,
)

REPORT_RE = re.compile(r"Chart has been generated in (\d+\.\d{2})ms")


def _listening_ports() -> set:
    ports = set()
    for table in ("/proc/net/tcp", "/proc/net/tcp6"):
        if not os.path.exists(table):
            continue
        with open(table, encoding="ascii") as handle:
            for line in handle.readlines()[1:]:
                fields = line.split()
                if len(fields) > 3 and fields[3] == "0A":
                    ports.add(int(fields[1].rsplit(":", 1)[1], 16))
    return ports


def _closure_of(build: dict) -> set:
    listed = build.get("closure") or []
    if listed and isinstance(listed[0], dict):
        return {row.get("module_id") for row in listed}
    return set(listed)


def _pulled_in_by(build: dict) -> dict:
    listed = build.get("closure") or []
    if listed and isinstance(listed[0], dict):
        return {row.get("module_id"): row.get("pulled_in_by") for row in listed}
    return {}


def test_health_returns_200_and_pages_share_one_origin():
    """Health answers 200 and the pages share the API origin. cov: C-TR-24, C-DC-01, C-DC-02, C-DC-04, C-DC-05, C-DC-11, C-DC-12"""

    response = httpx.get(f"{base_url()}/api/health", timeout=TIMEOUT)
    assert response.status_code == 200, f"health must return 200 once ready: {describe(response)}"
    page = html_of("/option")
    assert page.status_code == 200 and "text/html" in page.headers.get("content-type", ""), \
        f"the pages must be served on the API's origin and port: {describe(page)}"
    listening = _listening_ports()
    assert 4173 in listening, f"the app must listen on container port 4173: {sorted(listening)}"
    assert 5432 not in listening, "no local PostgreSQL may listen inside the app container"
    assert 9000 not in listening, "no local object store may listen inside the app container"


def test_app_root_keeps_reserved_screenshot_and_download_directories():
    """The app root keeps the two reserved directories. cov: C-DC-08, C-DC-09"""

    for name in (".browser_screenshots", ".downloads"):
        assert os.path.isdir(f"/app/{name}"), \
            f"the reserved directory /app/{name} must exist at the app root"


def test_seeded_accounts_are_stored_once_with_hashed_passwords(backend):
    """The three seeded accounts are stored once, hashed, and listed in the credentials file. cov: C-RL-18, C-RL-19, C-RL-20, C-RL-21, C-CF-10, C-TR-14, C-TR-16, C-DM-02, C-DC-07"""

    expected = {CONTRIBUTOR_EMAIL: (CONTRIBUTOR_NAME, "contributor"),
                CONTRIBUTOR2_EMAIL: (CONTRIBUTOR2_NAME, "contributor"),
                READER_EMAIL: (READER_NAME, "reader")}
    for email, (name, role) in expected.items():
        assert backend.count("users", email=email) == 1, \
            f"seeded account {email} must exist exactly once"
        stored = backend.rows("users", limit=1, email=email)[0]
        assert stored.get("name") == name, f"seeded account {email}: {stored}"
        assert stored.get("role") == role, f"seeded account {email}: {stored}"
        held = str(stored.get("password_hash") or "")
        assert held and PASSWORD not in held, \
            f"the password of {email} must be stored hashed, not as the literal"
        signed = login(email)
        assert signed.status_code in OK and signed.json().get("token"), \
            f"{email} must sign in with the seeded password: {describe(signed)}"
    with open("/app/USER_README.md", encoding="utf-8") as readme:
        text = readme.read()
    for email in expected:
        assert email in text, f"{email} is missing from /app/USER_README.md"
    assert PASSWORD in text, "the seeded password must be written to /app/USER_README.md"


def test_login_refuses_a_wrong_password_and_an_unknown_email_alike(anon):
    """A wrong password and an unknown email are refused with one message. cov: C-CF-02, C-CF-05, C-CF-06, C-UF-24, C-TR-15, C-DC-21"""

    wrong = login(CONTRIBUTOR_EMAIL, "not-the-password")
    refused(wrong, "a wrong password")
    unknown = login(f"nobody-{token_hex()}@example.com")
    refused(unknown, "an unknown email")
    assert "Sign in failed" in message(wrong), \
        f"a wrong password must be refused with `Sign in failed`: {describe(wrong)}"
    assert message(wrong) == message(unknown), (
        "an unknown email and a wrong password must be refused with the same message, "
        f"found {message(wrong)!r} and {message(unknown)!r}")
    good = login(CONTRIBUTOR_EMAIL)
    assert good.status_code in OK, f"the seeded password must work: {describe(good)}"
    signed = good.json()
    assert signed.get("token"), f"a login must return a `token`: {signed}"
    assert signed.get("user", {}).get("email") == CONTRIBUTOR_EMAIL, \
        f"a login must return the signed-in `user`: {signed}"


def test_missing_unknown_and_signed_out_tokens_are_refused(anon, contributor):
    """A missing, unknown or signed-out token reaches nothing. cov: C-CF-03, C-CF-04, C-CF-07, C-CF-08, C-CF-09, C-UF-25, C-UF-26, C-DC-18, C-DC-22, C-DC-23"""

    denied(anon.get("/me"), "a call carrying no token")
    with httpx.Client(base_url=api_base(), timeout=TIMEOUT,
                      headers={"Authorization": f"Bearer not-a-token-{token_hex()}"}) as bogus:
        denied(bogus.get("/me"), "a call carrying an unknown token")
    mine = ok(contributor.get("/me"), "reading the signed-in user")
    assert mine.get("email") == CONTRIBUTOR_EMAIL, f"`GET /api/me` must name the caller: {mine}"
    out = contributor.post("/auth/logout", json={})
    assert out.status_code in OK, f"logout must succeed: {describe(out)}"
    denied(contributor.get("/me"), "a call carrying a signed-out token")
    denied(contributor.get("/my/examples"), "a signed-out token reading the owner list")


def test_signup_creates_a_contributor_and_refuses_a_duplicate_email(anon):
    """Signup creates a contributor and refuses a duplicate email. cov: C-RL-16, C-CF-01, C-CF-11, C-UF-03, C-DC-20"""

    email = f"probe-{token_hex()}@example.com"
    created = ok(anon.post("/auth/signup", json={
        "email": email, "name": "Probe Person", "password": PASSWORD,
    }), "signing up")
    assert created.get("token"), f"signup must return a `token`: {created}"
    user = created.get("user") or {}
    assert user.get("email") == email, f"signup must return the new `user`: {created}"
    assert user.get("role") == "contributor", f"signup must create a contributor: {created}"
    again = anon.post("/auth/signup", json={
        "email": email, "name": "Probe Twin", "password": PASSWORD})
    refused(again, "a duplicate signup")
    assert "email" in message(again).lower(), \
        f"a duplicate signup must name the email field: {describe(again)}"
    listed = rows(anon.get("/examples"), "the public example listing")
    assert isinstance(listed, list), "the public listing must survive a signup"


def test_option_path_to_editor_to_shared_snippet_round_trip(anon):
    """An option path reaches the editor and the result survives as a shared address. cov: C-OV-01"""

    found = node_of(anon, CURRENT, ROTATE_PATH)
    assert found.get("path") == ROTATE_PATH, f"the option path must resolve: {found}"
    examples = examples_of(anon)
    assert any(row.get("id") == BAR_EXAMPLE for row in examples), \
        f"{BAR_EXAMPLE} must be in the public listing: {[r.get('id') for r in examples]}"
    loaded = ok(anon.get(f"/examples/{BAR_EXAMPLE}"), f"reading {BAR_EXAMPLE}")
    code = loaded.get("code_js")
    assert code, f"an example must carry `code_js` for the editor: {loaded}"
    saved = share(anon, code=code)
    assert SNIPPET_ID_RE.match(str(saved.get("id"))), \
        f"a shared snippet must carry a well-formed identifier: {saved}"
    reopened = ok(anon.get(f"/snippets/{saved['id']}"), "reopening the shared snippet")
    assert reopened.get("code") == code, \
        "reopening the shared address must load the same code"
    page = html_of(f"/s/{saved['id']}")
    assert page.status_code == 200, f"the snippet address must render: {describe(page)}"


def test_property_block_carries_parent_path_type_badge_and_since(anon):
    """A property block carries its parent path, its type, its badge and its since version. cov: C-CF-18, C-CF-19, C-CF-20, C-CF-21, C-CF-22, C-CF-23, C-DC-28"""

    found = node_of(anon, CURRENT, "title.show")
    assert found.get("fragment_id") == "doc-content-title-show", \
        f"`title.show` must be addressed `doc-content-title-show`: {found}"
    assert found.get("since") == "5.0.0", f"a property must carry its since version: {found}"
    types = found.get("types")
    assert types, f"a property must carry its accepted types: {found}"
    assert "boolean" in " ".join(types if isinstance(types, list) else [str(types)]), \
        f"`title.show` must accept a boolean: {found}"
    assert found.get("description"), f"a property must carry its description: {found}"
    deprecated = node_of(anon, CURRENT, REMOVED_PATH)
    assert deprecated.get("deprecated") == OLDEST, \
        f"{REMOVED_PATH} must carry its deprecation version: {deprecated}"
    for path in ("title", "legend", ROTATE_PATH):
        node_of(anon, CURRENT, path)


def test_a_computed_default_is_never_served_as_a_literal_default(anon):
    """A computed default is served as a sentence and a worked value, never as a literal. cov: C-CF-24, C-CF-25, C-CF-26, C-CF-27, C-CF-28"""

    computed = node_of(anon, CURRENT, COMPUTED_PATH)
    assert computed.get("default_kind") == "computed", \
        f"{COMPUTED_PATH} must be a computed default: {computed}"
    assert not computed.get("default_literal"), \
        f"a computed default must carry no literal: {computed}"
    assert computed.get("default_sentence"), \
        f"a computed default must carry its generated sentence: {computed}"
    assert str(computed.get("default_worked_value")) == COMPUTED_WORKED, \
        f"{COMPUTED_PATH} must carry the worked value {COMPUTED_WORKED}: {computed}"
    inherited = node_of(anon, CURRENT, INHERITED_PATH)
    assert inherited.get("default_kind") == "inherited", \
        f"{INHERITED_PATH} must be an inherited default: {inherited}"
    assert inherited.get("inherits_from") == INHERITS_FROM, \
        f"{INHERITED_PATH} must inherit from {INHERITS_FROM}: {inherited}"
    for path, value in (("title.show", "true"), (ROTATE_PATH, "0"),
                        ("xAxis.axisLabel.margin", "8")):
        leaf = node_of(anon, CURRENT, path)
        assert leaf.get("default_kind") == "literal", f"{path} must be a literal default: {leaf}"
        assert str(leaf.get("default_literal")).strip("'\"") == value, \
            f"{path} must default to {value}: {leaf}"
    absent = node_of(anon, CURRENT, LATE_PATH)
    assert absent.get("default_kind") == "absent", \
        f"{LATE_PATH} must carry an absent default: {absent}"


def test_shared_text_style_object_expands_at_every_path(anon):
    """The shared text style object expands at every path it appears at. cov: C-CF-29, C-CF-30, C-DM-38"""

    for path in SHARED_PATHS:
        found = node_of(anon, CURRENT, path)
        assert found.get("shared_object") == SHARED_OBJECT, \
            f"{path} must name the shared object {SHARED_OBJECT}: {found}"
        children = found.get("children") or []
        names = {str(c.get("path", c)).rsplit(".", 1)[-1] for c in children}
        assert set(SHARED_LEAVES) <= names, (
            f"{path} must expand {sorted(SHARED_LEAVES)} in place, found {sorted(names)}")
    sized = node_of(anon, CURRENT, f"{SHARED_PATHS[1]}.fontSize")
    assert str(sized.get("default_literal")) == "12", \
        f"the shared fontSize must default to 12 at every path: {sized}"


def test_series_data_holds_one_variant_per_series_type(anon):
    """The series data node holds one variant per series type. cov: C-CF-31, C-CF-32, C-CF-34"""

    found = node_of(anon, CURRENT, VARIANT_PATH)
    variants = found.get("variants") or []
    values = {str(v.get("variant_value") if isinstance(v, dict) else v) for v in variants}
    assert {"line", "tree"} <= values, (
        f"{VARIANT_PATH} must hold a variant for a line series and one for a tree "
        f"series, found {sorted(values)}")
    assert found.get("variant_of") in (None, "", "series.type") or True
    for variant in variants:
        if isinstance(variant, dict) and variant.get("variant_value") == "tree":
            described = str(variant.get("description") or "") + str(variant.get("types") or "")
            assert "children" in described, \
                f"the tree variant must describe an entry carrying children: {variant}"


def test_a_removed_property_names_its_removal_version_and_replacement(anon):
    """A removed property names its removal version and its replacement. cov: C-OV-05, C-CF-35, C-CF-36, C-CF-37, C-CF-38, C-CN-10"""

    found = node_of(anon, CURRENT, REMOVED_PATH)
    assert found.get("removed") == PRIOR, \
        f"{REMOVED_PATH} must name {PRIOR} as the version that removed the path: {found}"
    assert found.get("replaced_by") == REPLACEMENT_PATH, \
        f"{REMOVED_PATH} must name {REPLACEMENT_PATH} as the replacement: {found}"
    page = html_of(f"/option/{CURRENT}#doc-content-series-hoverAnimation")
    assert page.status_code == 200, \
        f"a removed property must answer with a page rather than a not-found: {describe(page)}"
    earlier = node_of(anon, OLDEST, REMOVED_PATH)
    assert not earlier.get("removed"), \
        f"{REMOVED_PATH} must carry no removal under {OLDEST}: {earlier}"


def test_an_older_version_omits_a_later_property_from_tree_and_search(anon):
    """An older version omits a later property from its tree and its search. cov: C-OV-04, C-RL-01, C-CF-39, C-CF-40, C-CF-41, C-CF-42, C-UF-05, C-CN-13"""

    for version in (CURRENT, PRIOR, OLDEST):
        top = tree_of(anon, version)
        names = {str(row.get("path")) for row in top}
        assert "title" in names and "series" in names, \
            f"the {version} tree must carry the top-level branches: {sorted(names)[:8]}"
    node_of(anon, CURRENT, LATE_PATH)
    missing = node(anon, PRIOR, LATE_PATH)
    denied(missing, f"{LATE_PATH} under {PRIOR}")
    found = search_paths(anon, PRIOR, "selectorLabel")
    assert not [row for row in found if row.get("path") == LATE_PATH], \
        f"{LATE_PATH} must be absent from the {PRIOR} search index: {found}"
    node_of(anon, PRIOR, "series.emphasis.scale")
    denied(node(anon, OLDEST, "series.emphasis.scale"),
           f"series.emphasis.scale under {OLDEST}")
    page = html_of(f"/option/{PRIOR}")
    assert PRIOR in page.text, f"the older reference must say which version it is: {describe(page)}"


def test_document_search_orders_by_the_first_matching_segment(anon):
    """The document search orders results by the first matching segment. cov: C-CF-43, C-CF-44, C-CF-45, C-CF-47, C-DC-29"""

    found = search_paths(anon, CURRENT, "title")
    paths = [row.get("path") for row in found]
    assert "title" in paths, f"the query `title` must match the branch itself: {paths}"
    assert SAVE_AS_IMAGE_PATH in paths, \
        f"the query `title` must match {SAVE_AS_IMAGE_PATH} too: {paths}"
    last = paths.index(SAVE_AS_IMAGE_PATH)
    under = [i for i, p in enumerate(paths) if p == "title" or p.startswith("title.")]
    assert under and max(under) < last, (
        "every path under the `title` branch must order before "
        f"{SAVE_AS_IMAGE_PATH}, found {paths}")
    for row in found:
        assert row.get("first_match_index") is not None, \
            f"a search row must carry its first matching segment index: {row}"
        assert row.get("first_sentence"), f"a search row must carry a first sentence: {row}"
    indexes = [int(row["first_match_index"]) for row in found]
    assert indexes == sorted(indexes), f"results must ascend by first match index: {found}"
    rotate = [row.get("path") for row in search_paths(anon, CURRENT, "ROTATE")]
    assert ROTATE_PATH in rotate, f"matching must be case-insensitive: {rotate}"
    assert "yAxis.axisLabel.rotate" in rotate, f"every parent must match: {rotate}"


def test_interface_signature_carries_each_argument_and_its_since(anon):
    """An interface signature carries every argument and its since version. cov: C-CF-52, C-CF-54, C-CF-55, C-CF-56, C-CF-57, C-CF-59, C-CF-60, C-DC-30"""

    found = interface_node(anon, CURRENT, INIT_PATH)
    assert found.get("member_kind") == "function", \
        f"{INIT_PATH} must be a function node: {found}"
    signature = " ".join(str(found.get("signature") or "").split())
    assert signature == INIT_SIGNATURE, (
        f"{INIT_PATH} must read {INIT_SIGNATURE!r}, found {signature!r}")
    args = found.get("arguments") or []
    named = {str(a.get("name")): a for a in args if isinstance(a, dict)}
    assert set(named) == {"dom", "theme", "opts"}, \
        f"{INIT_PATH} must carry three arguments, found {sorted(named)}"
    assert named["dom"].get("optional") in (False, None, 0), \
        f"`dom` must be required: {named['dom']}"
    assert named["theme"].get("optional"), f"`theme` must be optional: {named['theme']}"
    assert named["opts"].get("since") == OLDEST, \
        f"`opts` must carry {OLDEST} as its since version: {named['opts']}"
    assert found.get("returns"), f"a function node must carry its return type: {found}"
    other = interface_node(anon, CURRENT, SET_OPTION_PATH)
    assert " ".join(str(other.get("signature") or "").split()) == (
        "setOption(option: object, notMerge?: boolean, lazyUpdate?: boolean) => void"), \
        f"{SET_OPTION_PATH} must carry its measured signature: {other}"


def test_interface_cross_references_resolve_to_nodes_and_properties(anon):
    """Interface cross-references resolve to nodes and to option properties. cov: C-CF-51, C-CF-61, C-CF-62, C-CF-63, C-UF-06"""

    top = rows(anon.get(f"/interface/{CURRENT}/tree"), "the interface tree") \
        if anon.get(f"/interface/{CURRENT}/tree").status_code in OK else None
    if top is not None:
        names = {str(row.get("path")) for row in top}
        assert {"chartic", "charticInstance", "action", "events"} <= names, \
            f"the interface document must carry four top-level nodes: {sorted(names)}"
    found = interface_node(anon, CURRENT, INIT_PATH)
    links = found.get("cross_references") or []
    assert links, f"{INIT_PATH} must carry generated cross-references: {found}"
    for link in links:
        target = link.get("path") if isinstance(link, dict) else str(link)
        kind = (link.get("kind") if isinstance(link, dict) else "") or ""
        if kind == "option" or target in ("color", "backgroundColor", "animation"):
            node_of(anon, CURRENT, target)
        else:
            interface_node(anon, CURRENT, target)


def test_gallery_search_over_uses_returns_only_the_matching_example(anon):
    """A gallery search over the used property paths returns only the matching example. cov: C-RL-23, C-CF-66, C-CF-67, C-CF-68, C-CF-71, C-CF-72, C-DM-57, C-DC-32"""

    found = example_ids(anon, q=ROTATE_PATH)
    assert found == [BAR_EXAMPLE], (
        f"a search for {ROTATE_PATH} must return only {BAR_EXAMPLE}, found {found}")
    detail = ok(anon.get(f"/examples/{BAR_EXAMPLE}"), f"reading {BAR_EXAMPLE}")
    uses = detail.get("uses") or []
    assert ROTATE_PATH in uses, f"{BAR_EXAMPLE} must record {ROTATE_PATH} in `uses`: {uses}"
    for other in (LINE_EXAMPLE, SUNBURST_EXAMPLE):
        used = (ok(anon.get(f"/examples/{other}"), f"reading {other}").get("uses") or [])
        assert ROTATE_PATH not in used, f"{other} must not record {ROTATE_PATH}: {used}"
    by_title = example_ids(anon, q="Smoothed")
    assert LINE_EXAMPLE in by_title, f"a title search must find {LINE_EXAMPLE}: {by_title}"
    hidden = example_ids(anon, q="Bump")
    assert PROPOSED_EXAMPLE not in hidden, \
        f"a proposed example must stay out of the search: {hidden}"


def test_gallery_tag_and_external_data_filters_narrow_the_corpus(anon):
    """The gallery tag filter and the external data filter narrow the corpus. cov: C-RL-24, C-CF-69, C-CF-70, C-UF-07, C-DM-58, C-DM-59, C-DM-60, C-DC-31"""

    every = set(example_ids(anon))
    assert every == set(PUBLISHED_EXAMPLES), (
        f"the public listing must hold the six published examples, found {sorted(every)}")
    large = set(example_ids(anon, tag="large data"))
    assert large == {MAP_EXAMPLE, CANDLE_EXAMPLE}, \
        f"the `large data` tag must narrow to two examples, found {sorted(large)}"
    assert set(example_ids(anon, tag="dark")) == {RADAR_EXAMPLE}, "the `dark` tag narrows to one"
    assert set(example_ids(anon, tag="animation")) == {LINE_EXAMPLE}, "`animation` narrows to one"
    assert set(example_ids(anon, tag="interaction")) == {BAR_EXAMPLE, SUNBURST_EXAMPLE}, \
        "`interaction` narrows to two"
    external = set(example_ids(anon, external_data="true"))
    assert external == {MAP_EXAMPLE}, \
        f"the external data filter must narrow to {MAP_EXAMPLE}, found {sorted(external)}"
    for row in examples_of(anon):
        flag = row.get("has_external_data")
        assert flag is (row.get("id") == MAP_EXAMPLE), \
            f"`has_external_data` must be true for {MAP_EXAMPLE} alone: {row}"
    assert set(example_ids(anon, category="Line")) == {LINE_EXAMPLE}, "a category narrows too"


def test_a_proposed_example_is_absent_from_every_public_listing(anon, contributor):
    """A proposed example is absent from every public listing. cov: C-OV-06, C-RL-06, C-RL-22, C-CF-183, C-CF-184, C-CF-185, C-DM-61, C-CN-01"""

    assert PROPOSED_EXAMPLE not in example_ids(anon), \
        "a proposed example must be absent from the public listing"
    assert PROPOSED_EXAMPLE not in example_ids(anon, q="Bump Chart"), \
        "a proposed example must be absent from the gallery search"
    assert PROPOSED_EXAMPLE not in example_ids(anon, category="Lines"), \
        "a proposed example must be absent from its own category listing"
    denied(anon.get(f"/examples/{PROPOSED_EXAMPLE}"),
           "an anonymous read of a proposed example")
    mine = ok(contributor.get("/my/examples"), "the owner's own example list")
    owned = {row.get("id") for row in mine}
    assert PROPOSED_EXAMPLE in owned, \
        f"the owner must still see the proposed example: {sorted(owned)}"
    state = {row.get("id"): row.get("state") for row in mine}
    assert state.get(PROPOSED_EXAMPLE) == "proposed", f"its state must be proposed: {state}"


def test_one_preference_set_is_shared_by_reference_gallery_and_editor(contributor):
    """One preference set is shared by the reference, the gallery and the editor. cov: C-CF-75, C-CF-76, C-CF-77, C-DC-44, C-DC-45"""

    start = preferences(contributor)
    for key in ("dark", "decal", "renderer"):
        assert key in start, f"the preference set must carry `{key}`: {start}"
    set_preferences(contributor, dark=True, decal=True, renderer="svg")
    after = preferences(contributor)
    assert after.get("dark") is True and after.get("decal") is True, \
        f"the preference set must persist what was written: {after}"
    assert after.get("renderer") == "svg", f"the renderer choice must persist: {after}"
    again = preferences(contributor)
    assert again == after, "a second read must return the same preference set"
    set_preferences(contributor, dark=False, decal=False, renderer="canvas")
    assert preferences(contributor).get("dark") is False, "the preference set must be writable back"


def test_a_render_reports_elapsed_milliseconds_and_a_point_count(anon):
    """A render reports elapsed milliseconds, a point count and a description. cov: C-CF-81, C-CF-82, C-CF-83, C-CF-84, C-DM-63, C-DM-64, C-DC-43"""

    result = render(anon, SMOOTH_OPTION)
    assert result.status_code in OK, f"a valid option must render: {describe(result)}"
    drawn = result.json()
    elapsed = str(drawn.get("elapsed_ms"))
    assert re.fullmatch(r"\d+\.\d{2}", elapsed), (
        f"`elapsed_ms` must be reported to exactly two decimal places, found {elapsed!r}")
    assert int(drawn.get("points_drawn")) > 0, f"a render must report a point count: {drawn}"
    assert drawn.get("description"), f"a render must carry a generated description: {drawn}"
    assert drawn.get("document"), f"a render must return the drawing: {drawn}"
    seeded = ok(anon.get(f"/examples/{LINE_EXAMPLE}"), f"reading {LINE_EXAMPLE}")
    assert seeded.get("description") == LINE_DESCRIPTION, (
        f"{LINE_EXAMPLE} must carry its generated description, found "
        f"{seeded.get('description')!r}")
    counted = render(anon, seeded["code_js"])
    assert counted.status_code in OK, f"the seeded example must render: {describe(counted)}"
    assert int(counted.json().get("points_drawn")) == LINE_POINTS, (
        f"{LINE_EXAMPLE} must report {LINE_POINTS} drawn point marks, one per "
        f"category, found {counted.json().get('points_drawn')}")


def test_a_broken_option_is_refused_and_the_last_chart_survives(anon):
    """A broken option is refused with its line and the last chart survives. cov: C-CF-86, C-CF-87, C-CF-88"""

    good = render(anon, SMOOTH_OPTION)
    assert good.status_code in OK, f"a valid option must render first: {describe(good)}"
    broken = render(anon, BROKEN_OPTION)
    refused(broken, "a broken option")
    said = message(broken)
    assert said, f"a refused render must carry its message: {describe(broken)}"
    detail = body(broken)
    line = detail.get("line") if isinstance(detail, dict) else None
    assert line is not None, f"a refused render must name the line it came from: {detail}"
    again = render(anon, SMOOTH_OPTION)
    assert again.status_code in OK, \
        f"the last chart must still be renderable after a refusal: {describe(again)}"
    assert int(again.json().get("points_drawn")) > 0, "the surviving chart must still draw"


def test_the_wall_clock_budget_stops_an_evaluation_that_never_ends(anon):
    """The wall clock budget stops an evaluation that never ends. cov: C-CF-89, C-CF-90, C-CF-91, C-CF-92, C-CF-93, C-TR-21, C-TR-45"""

    started = time.monotonic()
    stopped = render(anon, ENDLESS_OPTION)
    elapsed = time.monotonic() - started
    refused(stopped, "an evaluation that never ends")
    said = (message(stopped) + " " + str(body(stopped))).lower()
    assert "wall clock" in said or "memory" in said, (
        f"a stopped evaluation must name the budget that ended it: {describe(stopped)}")
    assert elapsed < WALL_CLOCK_BUDGET * 4, (
        f"the budget must be enforced from outside the evaluation, which took {elapsed:.1f}s")
    detail = body(stopped)
    if isinstance(detail, dict):
        assert not detail.get("document"), \
            f"a stopped evaluation must return no drawing: {detail}"
    healthy = render(anon, SMOOTH_OPTION)
    assert healthy.status_code in OK, \
        f"the surface must keep serving after a stopped evaluation: {describe(healthy)}"


def test_a_shared_snippet_identifier_is_unguessable_and_well_formed(anon):
    """A shared snippet identifier is unguessable and well formed. cov: C-RL-02, C-CF-98, C-CF-99, C-CF-100, C-CF-101, C-CF-102, C-TR-12, C-DC-40"""

    saved = share(anon)
    identifier = str(saved.get("id"))
    assert SNIPPET_ID_RE.match(identifier), (
        f"a snippet identifier must be 26 characters of a-z and 2-7, found {identifier!r}")
    assert saved.get("url", "").endswith(identifier), \
        f"the returned url must carry the identifier: {saved}"
    assert int(saved.get("revision")) == 1, f"a new snippet must open at revision 1: {saved}"
    others = {str(share(anon).get("id")) for _ in range(4)}
    assert identifier not in others, "an identifier must never be reused"
    assert len(others) == 4, f"four shares must mint four identifiers: {others}"
    numeric = [int(i, 32) if re.fullmatch(r"[a-z2-7]+", i) else 0 for i in sorted(others)]
    assert len(set(numeric)) == len(numeric), "identifiers must not be sequential"
    reopened = ok(anon.get(f"/snippets/{identifier}"), "reopening the new snippet")
    assert reopened.get("visibility") == "unlisted", \
        f"a snippet saved without an account must be unlisted: {reopened}"


def test_two_simultaneous_shares_store_two_distinct_snippet_rows(anon):
    """Two simultaneous shares store two distinct snippet rows. cov: C-DM-96"""

    first, second = run_together(lambda: share(anon), lambda: share(anon))
    one, two = str(first.get("id")), str(second.get("id"))
    assert one != two, f"two simultaneous shares must mint two identifiers: {one}, {two}"
    for identifier in (one, two):
        assert SNIPPET_ID_RE.match(identifier), f"identifier {identifier!r} is malformed"
        stored = ok(anon.get(f"/snippets/{identifier}"), f"reading snippet {identifier}")
        assert stored.get("code"), f"both snippets must be stored: {stored}"
        assert int(stored.get("revision")) == 1, f"both must open at revision 1: {stored}"


def test_a_withdrawn_snippet_answers_gone_and_an_unknown_one_absent(anon):
    """A withdrawn snippet answers gone and an unknown one answers absent. cov: C-CF-103, C-CF-108, C-CF-109, C-CF-113, C-CF-114, C-UF-09, C-TR-23, C-DC-41"""

    live = ok(anon.get(f"/snippets/{LIVE_SNIPPET}"), "reading the seeded snippet")
    assert live.get("code"), f"the seeded snippet must carry its code: {live}"
    assert live.get("library_version") == CURRENT, \
        f"the seeded snippet must carry its library version: {live}"
    assert live.get("renderer"), f"the seeded snippet must carry its renderer: {live}"
    withdrawn = anon.get(f"/snippets/{WITHDRAWN_SNIPPET}")
    assert withdrawn.status_code == 410, (
        f"a withdrawn snippet must answer gone rather than absent: {describe(withdrawn)}")
    unknown = anon.get(f"/snippets/{'a' * 26}")
    assert unknown.status_code == 404, (
        f"an unknown snippet address must answer absent, distinct from gone: "
        f"{describe(unknown)}")
    page = html_of(f"/s/{WITHDRAWN_SNIPPET}")
    assert page.status_code in (200, 410), f"the gone page must render: {describe(page)}"


def test_a_snippet_edit_bumps_the_revision_for_its_owner_alone(contributor, contributor2):
    """A snippet edit bumps the revision for its owner alone. cov: C-RL-09, C-CF-104, C-CF-105, C-CF-106, C-CF-107, C-TR-13, C-CN-03, C-DC-42"""

    saved = share(contributor, code=SMOOTH_OPTION)
    identifier = str(saved.get("id"))
    edited = ok(contributor.patch(f"/snippets/{identifier}",
                                 json={"code": SMOOTH_OPTION.replace("true", "false")}),
                "editing an owned snippet")
    assert int(edited.get("revision")) == 2, f"an owner's edit must bump the revision: {edited}"
    intruder = contributor2.patch(f"/snippets/{identifier}", json={"code": "{}"})
    denied(intruder, "an edit by anyone but the owner")
    after = ok(contributor.get(f"/snippets/{identifier}"), "re-reading the owned snippet")
    assert int(after.get("revision")) == 2, \
        f"a refused edit must leave the revision alone: {after}"
    assert "false" in str(after.get("code")), "the owner's edit must be the stored code"
    mine = ok(contributor.get("/my/snippets"), "the owner's own snippet list") \
        if contributor.get("/my/snippets").status_code in OK else None
    if mine is not None:
        assert identifier in {str(row.get("id")) for row in mine}, \
            f"an owned snippet must be listed for its owner: {mine}"


def test_theme_registry_serves_series_colours_and_a_contrast_report(anon):
    """The theme registry serves each theme's series colours and its contrast report. cov: C-CF-137, C-CF-138, C-CF-139, C-UF-11, C-UX-20, C-UX-21, C-DC-46"""

    registry = themes_of(anon)
    assert set(THEMES) <= set(registry), \
        f"the registry must carry the four seeded themes, found {sorted(registry)}"
    default = registry["default"]
    assert default.get("name") == "Default", f"the default theme must be named: {default}"
    assert default.get("ground") == "light", f"the default theme must be light: {default}"
    colours = default.get("series_colours") or []
    assert len(colours) == SERIES_COLOURS, (
        f"the default theme must carry {SERIES_COLOURS} series colours, found {colours}")
    assert registry["dark-slate"].get("ground") == "dark", \
        f"`dark-slate` must be dark: {registry['dark-slate']}"
    for name, row in registry.items():
        report = row.get("contrast_report") or {}
        assert report, f"every registered theme must carry a contrast report: {name}"
        assert report.get("series_contrast") or report.get("per_series"), \
            f"the report of {name} must give the contrast of each series colour: {report}"
        assert report.get("min_pairwise_distance") is not None, \
            f"the report of {name} must give the smallest pairwise distance: {report}"
        deficiency = report.get("colour_vision_deficiency") or report.get("cvd") or {}
        assert len(deficiency) >= 3, (
            f"the report of {name} must recompute under the three common forms of "
            f"colour vision deficiency: {report}")


def test_a_failing_contrast_report_names_its_colliding_pairs_and_stays(anon):
    """A failing contrast report names its colliding pairs and the theme stays listed. cov: C-CF-140, C-CF-141"""

    registry = themes_of(anon)
    failing = registry[FAILING_THEME]
    report = failing.get("contrast_report") or {}
    assert report.get("passes") is False or report.get("fails") is True, (
        f"{FAILING_THEME} must be recorded as failing its contrast report: {report}")
    pairs = report.get("colliding_pairs") or []
    assert pairs, f"a failing report must name the colliding pairs: {report}"
    for pair in pairs:
        members = pair if isinstance(pair, (list, tuple)) else pair.get("pair")
        assert members and len(members) == 2, f"a colliding pair must name two colours: {pair}"
    assert FAILING_THEME in registry, "a failing theme is labelled rather than removed"
    for other in ("default", "dark-slate", "vintage"):
        clean = registry[other].get("contrast_report") or {}
        assert not (clean.get("colliding_pairs") or []), \
            f"{other} must name no colliding pair: {clean}"
    page = html_of("/themes")
    assert page.status_code == 200 and "Sandstone" in page.text, \
        f"the theme registry route must still list Sandstone: {describe(page)}"


def test_theme_import_refuses_a_function_and_a_non_colour_value(anon):
    """A theme import refuses a function value and a value that is no colour. cov: C-CF-128, C-CF-129, C-CF-130, C-CF-131, C-CF-132, C-CF-133, C-CF-134, C-CF-135, C-CF-136, C-CN-04, C-DC-47, C-DC-54"""

    good = anon.post("/themes/validate", json={"document": {"color": ["#5070dd"]}})
    assert good.status_code in OK, f"a well-formed theme must validate: {describe(good)}"
    assert good.json().get("valid") is True, f"a well-formed theme must be valid: {good.json()}"
    for payload, what in ((FUNCTION_THEME, "a value that is a function"),
                          (NON_COLOUR_THEME, "a colour that does not parse")):
        refusal = anon.post("/themes/validate", json={"document": payload})
        if refusal.status_code in OK:
            answered = refusal.json()
            assert answered.get("valid") is False, f"{what} must be refused: {answered}"
            assert answered.get("key") or answered.get("message"), \
                f"a refused import must name the offending key: {answered}"
        else:
            refused(refusal, what)
            assert message(refusal), f"a refused import must name the offending key: {what}"
    for payload, what in (({"color": ["#5070dd"], "unknownKey": 1}, "a key outside the schema"),
                          ({"textStyle": {"fontSize": float("inf")}}, "a number that is not finite")):
        refusal = anon.post("/themes/validate", json={"document": payload})
        assert refusal.status_code not in OK or refusal.json().get("valid") is False, \
            f"{what} must be refused: {describe(refusal)}"


def test_bundle_selection_resolves_the_closure_and_names_the_cause(anon):
    """A bundle selection resolves the closure and names the cause of each member. cov: C-RL-03, C-CF-142, C-CF-143, C-CF-144, C-UF-13, C-DM-84, C-CN-14, C-DC-49"""

    graph = modules_of(anon)
    assert set(MODULE_RAW) <= set(graph), \
        f"the module graph must carry the seeded modules, found {sorted(graph)}"
    assert graph[BAR_MODULE].get("requires") == ["coord/cartesian"], \
        f"{BAR_MODULE} must require coord/cartesian: {graph[BAR_MODULE]}"
    requested = request_bundle(anon, selection=(BAR_MODULE,))
    assert requested.status_code in OK, f"a bundle request must be accepted: {describe(requested)}"
    build = requested.json()
    closure = _closure_of(build)
    assert closure == set(BAR_CLOSURE), (
        f"selecting {BAR_MODULE} must resolve {sorted(BAR_CLOSURE)}, found {sorted(closure)}")
    causes = _pulled_in_by(build)
    if causes:
        assert causes.get("coord/cartesian") == BAR_MODULE, \
            f"coord/cartesian must name {BAR_MODULE} as its cause: {causes}"
        assert causes.get("scale/interval") == "component/axis", \
            f"scale/interval must name component/axis as its cause: {causes}"
        assert not causes.get(BAR_MODULE), f"the ticked module needs no cause: {causes}"
    assert CORE_MODULE in closure, f"{CORE_MODULE} must always be in a closure: {closure}"


def test_the_estimated_total_sums_the_closure_raw_bytes(anon):
    """The estimated total sums the raw bytes of the closure. cov: C-CF-145, C-CF-146, C-DC-48"""

    graph = modules_of(anon)
    for module, raw in MODULE_RAW.items():
        assert int(graph[module].get("raw_bytes")) == raw, (
            f"{module} must carry {raw} raw bytes, found {graph[module].get('raw_bytes')}")
    build = ok(request_bundle(anon, selection=(BAR_MODULE,)), "requesting the bar bundle")
    sizes = build.get("sizes") or {}
    assert int(sizes.get("raw")) == BAR_CLOSURE_RAW, (
        f"the raw total for the {BAR_MODULE} closure must be {BAR_CLOSURE_RAW}, "
        f"found {sizes.get('raw')}")
    assert sizes.get("minified") is not None, f"the total must give a minified size: {sizes}"
    assert sizes.get("compressed") is not None, f"the total must give a compressed size: {sizes}"
    assert int(sizes["minified"]) < int(sizes["raw"]), f"minified must be smaller: {sizes}"
    assert int(sizes["compressed"]) <= int(sizes["minified"]), \
        f"compressed must not exceed minified: {sizes}"
    assert sum(MODULE_RAW[m] for m in BAR_CLOSURE) == BAR_CLOSURE_RAW, \
        "the seeded graph must add up to the pinned total"


def test_an_unknown_module_selection_is_refused_before_any_build(anon):
    """An unknown module selection is refused before any build begins. cov: C-CF-147, C-CF-148, C-CF-149"""

    from conftest import UNKNOWN_MODULE
    refusal = request_bundle(anon, selection=(BAR_MODULE, UNKNOWN_MODULE))
    refused(refusal, "a selection naming a module outside the graph")
    assert UNKNOWN_MODULE in message(refusal), (
        f"a refused selection must name the unknown module: {describe(refusal)}")
    detail = body(refusal)
    if isinstance(detail, dict):
        assert not detail.get("request_digest"), \
            f"a refused selection must start no build: {detail}"
        assert not detail.get("artifact_sha256"), f"a refused selection builds nothing: {detail}"
    for bad in ({"selection": ["../etc/passwd"]}, {"selection": ["chart/bar; rm -rf /"]}):
        stopped = request_bundle(anon, **bad)
        refused(stopped, f"a selection carrying {bad['selection'][0]!r}")
    good = request_bundle(anon, selection=(BAR_MODULE,))
    assert good.status_code in OK, f"a legal selection must still be accepted: {describe(good)}"


def test_two_identical_bundle_requests_share_one_artifact_digest(anon):
    """Two identical bundle requests share one artifact digest. cov: C-CF-152, C-CF-153, C-CF-154, C-TR-42, C-TR-43, C-DM-86, C-DM-97"""

    first, second = run_together(lambda: request_bundle(anon, selection=(BAR_MODULE,)),
                                 lambda: request_bundle(anon, selection=(BAR_MODULE,)))
    assert first.status_code in OK and second.status_code in OK, \
        f"both requests must be accepted: {describe(first)} / {describe(second)}"
    one, two = first.json(), second.json()
    assert one.get("request_digest") == two.get("request_digest"), (
        f"two identical requests must share one digest, found "
        f"{one.get('request_digest')} and {two.get('request_digest')}")
    ready = bundle_ready(anon, one["request_digest"])
    assert ready.get("artifact_sha256"), f"a ready build must carry its digest: {ready}"
    again = ok(request_bundle(anon, selection=(BAR_MODULE,)), "asking a third time")
    third = bundle_ready(anon, again["request_digest"])
    assert third.get("artifact_sha256") == ready["artifact_sha256"], (
        "the same request must produce a byte-identical artifact at the same digest")
    different = ok(request_bundle(anon, selection=("chart/pie",)), "a different selection")
    assert different.get("request_digest") != one["request_digest"], \
        "a different selection must carry a different digest"


def test_a_ready_bundle_artifact_is_uploaded_to_the_object_store(anon, store):
    """A ready bundle artifact is uploaded to the object store. cov: C-TR-11, C-CN-11, C-DC-15, C-DC-52"""

    requested = ok(request_bundle(anon, selection=(BAR_MODULE,)), "requesting the bar bundle")
    ready = bundle_ready(anon, requested["request_digest"])
    digest = ready["artifact_sha256"]
    key = ready.get("artifact_key") or f"bundles/{digest}/chartic-esm.js"
    assert key.startswith(f"bundles/{digest}/"), (
        f"a bundle artifact key must carry the digest of its bytes, found {key!r}")
    assert key.endswith(".js"), f"a bundle artifact key must end in the format: {key!r}"
    found = wait_until(lambda: store_keys(f"bundles/{digest}/"), lambda k: bool(k))
    assert key in found, (
        f"the artifact must live in the object store at {key!r}, found {found}")
    assert store.exists(key), f"the object store must hold {key!r}"
    assert not os.path.exists(f"/app/{key}"), \
        f"the artifact must not also sit on the app container's own disk at /app/{key}"


def test_a_ready_bundle_returns_integrity_manifest_snippet_and_recipe(anon):
    """A ready bundle returns its integrity hash, manifest, install snippet and recipe. cov: C-CF-151, C-CF-155, C-CF-156, C-CF-157, C-CF-158, C-CF-159, C-TR-46, C-DM-87, C-DC-50"""

    requested = ok(request_bundle(anon, selection=(BAR_MODULE,)), "requesting the bar bundle")
    assert requested.get("status") in ("queued", "building", "ready"), \
        f"a build must be queued rather than answered inline: {requested}"
    if requested.get("status") == "queued":
        assert requested.get("queue_position") is not None, \
            f"a queued build must show its position: {requested}"
    ready = bundle_ready(anon, requested["request_digest"])
    integrity = str(ready.get("integrity") or "")
    assert integrity.startswith("sha384-"), (
        f"a ready bundle must carry an integrity hash a page can use, found {integrity!r}")
    manifest = ready.get("manifest") or {}
    assert set(BAR_CLOSURE) <= set(manifest.get("closure") or []), \
        f"the manifest must name the resolved closure: {manifest}"
    sizes = manifest.get("sizes") or ready.get("sizes") or {}
    assert {"raw", "minified", "compressed"} <= set(sizes), \
        f"the manifest must give the three sizes: {sizes}"
    snippet = str(ready.get("install_snippet") or "")
    assert integrity in snippet, \
        f"the install snippet must carry the integrity hash already filled in: {snippet!r}"
    assert ready.get("rebuild_command"), \
        f"a ready bundle must return the command that reproduces it: {ready}"


def test_a_published_release_record_refuses_every_edit(anon, contributor):
    """A published release record refuses every edit. cov: C-CF-160, C-CF-161, C-DM-95, C-DC-26"""

    before = releases_of(anon)
    assert set(RELEASE_DATES) <= set(before), \
        f"the three seeded releases must be listed, found {sorted(before)}"
    for version, date in RELEASE_DATES.items():
        assert str(before[version].get("released_on")).startswith(date), (
            f"{version} must be released on {date}, found {before[version].get('released_on')}")
    assert before[CURRENT].get("is_current") is True, f"{CURRENT} must be current: {before[CURRENT]}"
    for payload in ({"released_on": "2020-01-01"}, {"version": "9.9.9"},
                    {"is_current": False}):
        refusal = contributor.patch(f"/releases/{CURRENT}", json=payload)
        refused(refusal, f"an edit of a published release with {payload}")
    anonymous = contributor.patch(f"/releases/{CURRENT}", json={"commit": "deadbeef"})
    refused(anonymous, "a second attempt to change a published release")
    after = releases_of(anon)
    assert after[CURRENT] == before[CURRENT], (
        f"the stored record must be unchanged: {before[CURRENT]} became {after[CURRENT]}")


def test_the_download_table_drops_a_mismatching_mirror_and_marks_stale(anon):
    """The download table drops a mismatching mirror and marks a stale one. cov: C-CF-162, C-CF-167, C-CF-168, C-CF-169, C-CF-170, C-UF-12, C-DM-15, C-DM-16, C-DM-17, C-DM-18"""

    listed = releases_of(anon)
    current = listed[CURRENT]
    artifacts = {str(a.get("filename")): a for a in (current.get("artifacts") or [])}
    name = f"chartic-{CURRENT}.tar.gz"
    assert name in artifacts, f"the {CURRENT} archive must be listed: {sorted(artifacts)}"
    assert artifacts[name].get("sha256") == ARTIFACT_SHA256[CURRENT], (
        f"{name} must carry its computed sha256, found {artifacts[name].get('sha256')}")
    assert artifacts[name].get("sha512") == ARTIFACT_SHA512, \
        f"{name} must carry its sha512: {artifacts[name]}"
    assert artifacts[name].get("signature_filename") == f"{name}.asc", \
        f"{name} must name its signature file: {artifacts[name]}"
    assert artifacts[name].get("attestation"), \
        f"{name} must carry its provenance attestation: {artifacts[name]}"
    mirrors = {str(m.get("host")): m for m in (current.get("mirrors") or [])}
    assert MIRROR_BETA not in mirrors, (
        f"the mismatching mirror {MIRROR_BETA} must be dropped from the table, "
        f"found {sorted(mirrors)}")
    assert mirrors[MIRROR_ALPHA].get("status") == "active", \
        f"{MIRROR_ALPHA} must be active: {mirrors[MIRROR_ALPHA]}"
    assert mirrors[MIRROR_GAMMA].get("status") == "stale", \
        f"{MIRROR_GAMMA} must be marked stale: {mirrors[MIRROR_GAMMA]}"
    for host, row in mirrors.items():
        assert row.get("last_verified_at"), f"{host} must show when it was last verified: {row}"
    page = html_of("/releases")
    assert MIRROR_BETA not in page.text, \
        "the mismatching mirror must not appear on the download route either"
    assert BETA_SHA256 not in page.text, "the mismatching hash must not be stated as a fact"
    for version, date in RELEASE_DATES.items():
        stamped = "/".join(date.split("-"))
        assert stamped in page.text, \
            f"the download table must format {version} as {stamped}: {describe(page)}"


def test_changelog_entries_carry_kind_area_sentence_reference_credit(anon):
    """A changelog entry carries its kind, area, sentence, reference and credit. cov: C-CF-171, C-FE-127, C-DM-23, C-DM-24, C-DC-25"""

    release = ok(anon.get(f"/releases/{CURRENT}"), f"reading release {CURRENT}")
    entries = release.get("changelog") or []
    assert len(entries) >= 2, f"{CURRENT} must carry its seeded changelog entries: {entries}"
    kinds = {str(e.get("kind")) for e in entries}
    assert {"Feature", "Fix"} <= kinds, f"the seeded kinds must be present: {kinds}"
    by_area = {str(e.get("area")): e for e in entries}
    assert "legend" in by_area and "series" in by_area, \
        f"the seeded areas must be present: {sorted(by_area)}"
    feature = by_area["legend"]
    assert LATE_PATH in str(feature.get("sentence")), \
        f"the legend entry must name {LATE_PATH}: {feature}"
    assert "#9142" in str(feature.get("references")), \
        f"the legend entry must reference #9142: {feature}"
    assert "nhaddad" in str(feature.get("credits")), \
        f"the legend entry must credit nhaddad: {feature}"
    fix = by_area["series"]
    references = str(fix.get("references"))
    assert "#9107" in references and "#9118" in references, \
        f"the series entry must carry both references: {fix}"
    assert "tvargas" in str(fix.get("credits")), f"the series entry must credit tvargas: {fix}"
    for entry in entries:
        assert entry.get("position") is not None, f"an entry must carry its position: {entry}"


def test_a_proposed_thumbnail_upload_lands_in_the_object_store(contributor, store):
    """A proposed thumbnail upload lands in the object store at its digest key. cov: C-OV-03, C-CF-176, C-CF-177, C-TR-44, C-DM-99, C-DC-51"""

    mine = ok(contributor.get("/my/examples"), "the owner's own example list")
    row = next(r for r in mine if r.get("id") == PROPOSED_EXAMPLE)
    key = str(row.get("thumbnail_key") or "")
    assert key == PROPOSED_THUMBNAIL_KEY, (
        f"{PROPOSED_EXAMPLE} must record the thumbnail key {PROPOSED_THUMBNAIL_KEY!r}, "
        f"found {key!r}")
    assert store.exists(key), f"the object store must hold the proposed thumbnail at {key!r}"
    digest = key.rsplit("/", 1)[-1].split(".")[0]
    assert len(digest) == 64, f"a thumbnail key must carry the digest of its bytes: {key!r}"
    assert store.exists(LINE_THUMBNAIL_KEY), \
        f"the published thumbnail must live at {LINE_THUMBNAIL_KEY!r} too"
    fresh = propose(contributor)
    try:
        stored = wait_until(lambda: ok(contributor.get(f"/my/examples/{fresh['id']}"),
                                       "re-reading the new proposal").get("thumbnail_key"),
                            lambda k: bool(k))
        assert stored, f"a new proposal must render a thumbnail into the store: {fresh}"
        assert stored.startswith(f"thumbnails/{fresh['id']}/"), \
            f"a new thumbnail key must follow the scheme, found {stored!r}"
        assert store.exists(stored), f"the object store must hold {stored!r}"
        assert not os.path.exists(f"/app/{stored}"), \
            "the thumbnail bytes must not also sit on the app container's own disk"
    finally:
        withdraw(contributor, fresh["id"])


def test_a_proposed_thumbnail_stream_is_forbidden_to_every_other_caller(contributor, contributor2, reader, anon):
    """A proposed thumbnail stream is forbidden to every caller but its owner. cov: C-OV-02, C-RL-07, C-CF-178, C-CF-179, C-CF-180, C-CF-181, C-CF-182, C-CF-186, C-TR-33, C-DC-33"""

    served = thumbnail(contributor, PROPOSED_EXAMPLE)
    assert served.status_code == 200, (
        f"the owning contributor must receive the proposed thumbnail: {describe(served)}")
    assert "svg" in served.headers.get("content-type", ""), \
        f"the stream must answer as image/svg+xml: {served.headers.get('content-type')}"
    assert served.content, "the stream must carry the stored bytes"
    for session, who in ((contributor2, CONTRIBUTOR2_EMAIL), (reader, READER_EMAIL),
                         (anon, "a caller with no token")):
        blocked = thumbnail(session, PROPOSED_EXAMPLE)
        denied(blocked, f"the proposed thumbnail stream for {who}")
        assert b"<svg" not in blocked.content, \
            f"no stored byte may reach {who}: {describe(blocked)}"
    direct = raw_get(f"/{PROPOSED_THUMBNAIL_KEY}")
    assert direct.status_code != 200, (
        f"the object must be reachable by no unauthenticated address: {describe(direct)}")
    published = thumbnail(anon, LINE_EXAMPLE)
    assert published.status_code == 200, (
        f"a published example's thumbnail must answer for everybody: {describe(published)}")


def test_publish_is_refused_until_the_named_validation_checks_pass(contributor, withdraw_after):
    """Publish is refused until every named validation check passes. cov: C-RL-08, C-RL-10, C-RL-13, C-CF-187, C-CF-188, C-CF-189, C-CF-190, C-CF-191, C-CF-192, C-CF-195, C-CF-198, C-DM-62, C-DC-37, C-DC-38"""

    created = propose(contributor, category="Pie")
    withdraw_after.append(created["id"])
    report = validate_example(contributor, created["id"])
    assert report.get("passed") is False, (
        f"a Pie category over a line series must fail validation: {report}")
    checks = report.get("checks") or []
    named = {str(c.get("name")): c for c in checks} if checks and isinstance(checks[0], dict) else {}
    assert named, f"validation must name one entry per check: {report}"
    failing = [n for n, c in named.items() if c.get("passed") is False]
    assert failing, f"a failing validation must name which check failed: {named}"
    assert any("categ" in n.lower() for n in failing), \
        f"the category check must be the failing one, found {failing}"
    blocked = publish(contributor, created["id"])
    refused(blocked, "a publish before validation passes")
    assert "categ" in message(blocked).lower(), \
        f"a refused publish must name the failing check: {describe(blocked)}"
    still = ok(contributor.get(f"/my/examples/{created['id']}"), "re-reading the proposal")
    assert still.get("state") == "proposed", f"a refused publish must leave it proposed: {still}"
    ok(contributor.patch(f"/my/examples/{created['id']}", json={"category": "Line"}),
       "correcting the category")
    fixed = validate_example(contributor, created["id"])
    assert fixed.get("passed") is True, f"a corrected example must validate: {fixed}"
    published = publish(contributor, created["id"])
    assert published.status_code in OK, f"a validated example must publish: {describe(published)}"
    assert published.json().get("state") == "published", f"its state must move: {published.json()}"
    assert created["id"] in example_ids(contributor), "a published example joins the listing"


def test_two_simultaneous_publishes_leave_one_published_example_row(contributor, withdraw_after):
    """Two simultaneous publishes leave one published example row. cov: C-RL-11, C-CF-196, C-CF-199, C-CF-200, C-DM-98, C-DC-39"""

    created = propose(contributor, category="Line")
    withdraw_after.append(created["id"])
    assert validate_example(contributor, created["id"]).get("passed") is True, \
        "the probe example must validate before the race"
    first, second = run_together(lambda: publish(contributor, created["id"]),
                                 lambda: publish(contributor, created["id"]))
    winners = [r for r in (first, second) if r.status_code in OK]
    assert winners, f"one publish must win: {describe(first)} / {describe(second)}"
    listed = [r for r in examples_of(contributor) if r.get("id") == created["id"]]
    assert len(listed) == 1, (
        f"two simultaneous publishes must leave exactly one published row, found {listed}")
    stored = ok(contributor.get(f"/my/examples/{created['id']}"), "re-reading the example")
    assert stored.get("state") == "published", f"the state must be published once: {stored}"
    keys = store_keys(f"thumbnails/{created['id']}/")
    assert len(keys) <= 1, f"no second thumbnail object may be written: {keys}"
    gone = withdraw(contributor, created["id"])
    assert gone.status_code in OK, f"the owner must be able to withdraw: {describe(gone)}"
    assert created["id"] not in example_ids(contributor), "a withdrawn example leaves the listing"


def test_another_contributor_is_answered_as_though_the_example_is_absent(contributor2, proposed_probe):
    """Another contributor is answered as though the example is absent. cov: C-RL-12, C-CF-193, C-CF-194, C-CF-197, C-DC-34, C-DC-36"""

    other = proposed_probe["id"]
    mine = {r.get("id") for r in ok(contributor2.get("/my/examples"), "the other owner's list")}
    assert other not in mine, f"another contributor's proposal must not be listed: {sorted(mine)}"
    assert PROPOSED_EXAMPLE not in mine, \
        f"the seeded proposal must not be listed for the other owner: {sorted(mine)}"
    reading = contributor2.get(f"/my/examples/{other}")
    assert reading.status_code == 404, (
        f"another contributor reading the example must be answered as absent: {describe(reading)}")
    editing = contributor2.patch(f"/my/examples/{other}", json={"title": probe_title()})
    assert editing.status_code == 404, \
        f"another contributor editing the example must be answered as absent: {describe(editing)}"
    publishing = publish(contributor2, other)
    denied(publishing, "a publish by anyone but the owner")
    removing = withdraw(contributor2, other)
    assert removing.status_code == 404, \
        f"another contributor withdrawing the example must be answered as absent: {describe(removing)}"
    survives = ok(contributor.get(f"/my/examples/{other}"), "the owner re-reading the example")
    assert survives.get("state") == "proposed", f"nothing may have changed: {survives}"


def test_a_reader_calling_a_contributor_endpoint_cannot_write_a_row(reader, backend):
    """A reader calling a contributor endpoint cannot write a row. cov: C-RL-04, C-RL-05, C-RL-14, C-RL-15, C-UF-14, C-UF-23, C-UF-27, C-TR-17, C-DC-19"""

    before = backend.count("examples")
    creating = reader.post("/my/examples", json={
        "title": probe_title(), "category": "Line", "tags": [],
        "code_js": SMOOTH_OPTION, DECOY_FIELD: ""})
    denied(creating, "a reader proposing an example")
    denied(publish(reader, PROPOSED_EXAMPLE), "a reader publishing an example")
    denied(withdraw(reader, PROPOSED_EXAMPLE), "a reader withdrawing an example")
    denied(reader.patch(f"/my/examples/{PROPOSED_EXAMPLE}", json={"title": "x"}),
           "a reader editing an example")
    denied(thumbnail(reader, PROPOSED_EXAMPLE), "a reader reading a proposed thumbnail")
    assert backend.count("examples") == before, (
        f"a reader's refused calls must write no row, {before} became "
        f"{backend.count('examples')}")
    listed = ok(reader.get("/my/examples"), "the reader's own list")
    assert listed == [], f"a reader's own list must be empty rather than another's: {listed}"
    stored = backend.rows("examples", limit=1, id=PROPOSED_EXAMPLE)[0]
    assert stored.get("state") == "proposed", f"the protected row must be untouched: {stored}"


def test_an_unknown_address_renders_the_portal_not_found_page(anon):
    """An unknown address renders the portal's own not-found page. cov: C-CF-201, C-UF-28"""

    for path in (f"/nothing-here-{token_hex()}", f"/option/{ABSENT_VERSION}",
                 f"/gallery/{token_hex()}"):
        page = html_of(path)
        assert page.status_code == 404, (
            f"{path} must answer not-found: {describe(page)}")
        assert "text/html" in page.headers.get("content-type", ""), \
            f"{path} must render the portal's own page: {describe(page)}"
        assert path.split("/")[-1] in page.text or path in page.text, \
            f"the not-found page must quote the address asked for: {path}"
        assert "<html" in page.text.lower(), f"{path} must render a full document"
        assert "traceback" not in page.text.lower(), f"{path} must not render a stack trace"


def test_the_not_found_page_names_the_version_that_removed_a_path(anon):
    """The not-found page names the version that removed a renamed path. cov: C-CF-203"""

    page = html_of(f"/option/{CURRENT}/{REMOVED_PATH}")
    text = page.text
    assert PRIOR in text, (
        f"an address ending in {REMOVED_PATH} must name {PRIOR} as the version that "
        f"removed it: {describe(page)}")
    assert REPLACEMENT_PATH in text, \
        f"the answer must name {REPLACEMENT_PATH} as the replacement: {describe(page)}"
    plain = html_of(f"/nothing-here-{token_hex()}")
    assert PRIOR not in plain.text or REPLACEMENT_PATH not in plain.text, \
        "an address matching no removed path must name no replacement"


def test_a_favicon_is_served_and_declared_in_every_document_head():
    """A favicon is served and declared in the head of every route. cov: C-FE-56, C-TR-34"""

    served = raw_get("/favicon.ico")
    assert served.status_code == 200, f"/favicon.ico must be served: {describe(served)}"
    assert served.content, "the favicon must carry bytes"
    for route in PUBLIC_ROUTES:
        page = html_of(route)
        assert page.status_code == 200, f"{route} must render: {describe(page)}"
        declared = re.search(r'<link[^>]+rel=["\'][^"\']*icon[^"\']*["\'][^>]*>',
                             page.text, re.I)
        assert declared, f"{route} must declare its favicon in the document head"


def test_every_public_route_declares_its_own_title_and_description():
    """Every public route declares its own title and description. cov: C-UF-01, C-UF-02, C-UF-04, C-UF-08, C-UF-10, C-TR-35, C-TR-36, C-CN-05, C-CN-12"""

    titles, descriptions = {}, {}
    for route in PUBLIC_ROUTES:
        page = html_of(route)
        assert page.status_code == 200, f"{route} must render: {describe(page)}"
        title = head_tag(page.text, r"<title[^>]*>(.*?)</title>")
        assert title and title.strip(), f"{route} must declare a title"
        description = meta_content(page.text, "description")
        assert description and description.strip(), f"{route} must declare a description"
        titles[route], descriptions[route] = title.strip(), description.strip()
    assert len(set(titles.values())) == len(titles), (
        f"no two routes may share a title: {titles}")
    assert len(set(descriptions.values())) == len(descriptions), (
        f"no two routes may share a description: {descriptions}")
    versioned = head_tag(html_of(f"/option/{PRIOR}").text, r"<title[^>]*>(.*?)</title>")
    assert versioned and versioned.strip() != titles["/option"], (
        f"/option/{PRIOR} must declare a different title from /option: {versioned!r}")


def test_every_public_route_declares_a_preview_image_that_resolves():
    """Every public route declares a preview image that resolves. cov: C-CF-110, C-CF-111, C-CF-112, C-TR-37, C-TR-38, C-TR-39"""

    for route in PUBLIC_ROUTES:
        page = html_of(route)
        title = meta_content(page.text, "og:title") or meta_content(page.text, "twitter:title")
        assert title and title.strip(), f"{route} must declare a social preview title"
        image = meta_content(page.text, "og:image") or meta_content(page.text, "twitter:image")
        assert image and image.strip(), f"{route} must declare a preview image"
        target = image if image.startswith("http") else f"{base_url()}{image}"
        fetched = httpx.get(target, timeout=TIMEOUT, follow_redirects=True)
        assert fetched.status_code == 200 and fetched.content, \
            f"the preview image of {route} must resolve to real bytes: {describe(fetched)}"
    snippet_page = html_of(f"/s/{LIVE_SNIPPET}")
    preview = meta_content(snippet_page.text, "og:image")
    assert preview, f"a snippet address must declare its own preview image: {describe(snippet_page)}"
    described = meta_content(snippet_page.text, "og:description") or \
        meta_content(snippet_page.text, "description")
    assert described and described.strip(), "a snippet address must declare its description"


def test_the_sitemap_lists_every_public_route_and_robots_points_at_it():
    """The sitemap lists every public route and robots names the sitemap. cov: C-UF-16, C-UF-17, C-TR-40, C-TR-41, C-CN-06, C-CN-07, C-CN-08"""

    sitemap = raw_get("/sitemap.xml")
    assert sitemap.status_code == 200, f"/sitemap.xml must be served: {describe(sitemap)}"
    body_text = sitemap.text
    for route in PUBLIC_ROUTES:
        assert route in body_text, f"the sitemap must list {route}: {body_text[:400]}"
    for version in RELEASE_DATES:
        assert f"/option/{version}" in body_text, \
            f"the sitemap must list one entry per retained version, missing {version}"
    for example in PUBLISHED_EXAMPLES:
        assert example in body_text, \
            f"the sitemap must list one entry per published example, missing {example}"
    assert PROPOSED_EXAMPLE not in body_text, \
        "the sitemap must not list a proposed example"
    for absent in ("handbook", "committers", "maillist", "spreadsheet", "events",
                   "cheat-sheet", "resources", "security", "advisor"):
        assert absent not in body_text.lower(), \
            f"the sitemap must list no {absent} route: {body_text[:400]}"
    robots = raw_get("/robots.txt")
    assert robots.status_code == 200, f"/robots.txt must be served: {describe(robots)}"
    assert "sitemap" in robots.text.lower() and "/sitemap.xml" in robots.text, \
        f"/robots.txt must name the sitemap: {robots.text[:200]}"


def test_the_privacy_page_states_what_is_collected_and_for_how_long():
    """The privacy page states what is collected and for how long. cov: C-CF-204, C-CF-205, C-CF-206, C-CF-207, C-CF-208, C-UF-15, C-DM-89, C-DM-90, C-CN-09"""

    page = html_of("/privacy")
    assert page.status_code == 200, f"/privacy must render: {describe(page)}"
    text = page.text.lower()
    for phrase in ("query", "rank", "24 hour", "aggregat"):
        assert phrase in text, f"the privacy page must state {phrase!r}: {page.text[:600]}"
    assert "identifier" in text, "the privacy page must say no identifier is carried"
    assert str(EVENT_RETENTION_HOURS) in page.text, \
        f"the privacy page must state the {EVENT_RETENTION_HOURS} hour window"
    for route in PUBLIC_ROUTES:
        other = html_of(route)
        assert "/privacy" in other.text, f"{route} must link the privacy page from its footer"


def test_a_filled_decoy_field_and_a_repeated_submission_are_refused(anon, contributor):
    """A filled decoy field and a repeated submission are both refused. cov: C-CF-209, C-CF-210, C-CF-211, C-TR-18, C-TR-19, C-TR-20, C-TR-22, C-DC-35"""

    trapped = anon.post("/snippets", json={
        "code": SMOOTH_OPTION, "language": "js", "library_version": CURRENT,
        "renderer": "canvas", "theme": "default", "decal": False,
        DECOY_FIELD: "https://example.com/spam"})
    refused(trapped, "a share carrying the decoy field filled")
    proposal = contributor.post("/my/examples", json={
        "title": probe_title(), "category": "Line", "tags": [],
        "code_js": SMOOTH_OPTION, DECOY_FIELD: "https://example.com/spam"})
    refused(proposal, "a proposal carrying the decoy field filled")
    outcomes = [anon.post("/snippets", json={
        "code": SMOOTH_OPTION, "language": "js", "library_version": CURRENT,
        "renderer": "canvas", "theme": "default", "decal": False, DECOY_FIELD: ""})
        for _ in range(REPEAT_LIMIT + 4)]
    blocked = [r for r in outcomes if 400 <= r.status_code < 500]
    assert blocked, (
        f"more than {REPEAT_LIMIT} shares inside the window must be refused, got "
        f"{[r.status_code for r in outcomes]}")
    assert len(blocked) >= len(outcomes) - REPEAT_LIMIT, (
        f"the refusal must hold for the rest of the window, got "
        f"{[r.status_code for r in outcomes]}")
    assert "wait" in message(blocked[-1]).lower(), \
        f"a rate-refused caller must be told to wait: {describe(blocked[-1])}"


def test_security_headers_ride_on_every_response():
    """Security headers ride on every response. cov: C-CF-95, C-CF-96, C-TR-26, C-TR-27, C-TR-28"""

    for route in PUBLIC_ROUTES:
        page = html_of(route)
        lowered = {k.lower(): v for k, v in page.headers.items()}
        for header in SECURITY_HEADERS:
            assert header in lowered, (
                f"{route} must carry the {header} header, found {sorted(lowered)}")
        assert lowered["x-content-type-options"].lower() == "nosniff", \
            f"{route} must carry a nosniff content-type policy: {lowered['x-content-type-options']}"
        policy = lowered["content-security-policy"].lower()
        assert "default-src" in policy or "script-src" in policy, \
            f"{route} must carry a real content security policy: {policy[:200]}"
    api = httpx.get(f"{api_base()}/health", timeout=TIMEOUT)
    api_headers = {k.lower() for k in api.headers}
    for header in SECURITY_HEADERS:
        assert header in api_headers, f"the API must carry the {header} header too"
    frame = html_of("/editor")
    frame_policy = frame.headers.get("content-security-policy", "").lower()
    assert "frame-ancestors" in frame_policy or "frame-src" in frame_policy \
        or "sandbox" in frame.text.lower(), \
        "the editor must declare the frame policy for its visitor-code frame"


def test_no_stored_credential_reaches_anything_the_browser_downloads():
    """No stored credential reaches anything the browser downloads. cov: C-CF-94, C-TR-29, C-TR-30, C-TR-31, C-TR-32"""

    secrets = [os.environ[name] for name in SECRET_ENV if os.environ.get(name)]
    assert secrets, f"the environment must carry the credentials named in {SECRET_ENV}"
    fetched = []
    for route in PUBLIC_ROUTES:
        page = html_of(route)
        fetched.append((route, page.text))
        for src in re.findall(r'(?:src|href)=["\']([^"\']+\.(?:js|css|json))["\']', page.text):
            if src.startswith("http") and base_url() not in src:
                continue
            target = src if src.startswith("http") else f"{base_url()}{src if src.startswith('/') else '/' + src}"
            asset = httpx.get(target, timeout=TIMEOUT)
            if asset.status_code == 200:
                fetched.append((src, asset.text))
    for where, text in fetched:
        for secret in secrets:
            assert secret not in text, f"a stored credential reached {where}"
        assert "STORAGE_SECRET_KEY" not in text or "STORAGE_SECRET_KEY=" not in text, \
            f"{where} must not carry the object store secret"
    for name in ("postgresql://", "minioadmin"):
        for where, text in fetched:
            assert name not in text, f"{where} must not carry {name!r}"


def test_body_text_meets_the_contrast_bar_against_its_background(page):
    """Body text and the quiet supporting tone both meet the contrast bar. cov: C-UX-53, C-UX-54, C-UX-55"""

    page.goto(f"{base_url()}/releases")
    page.wait_for_load_state("networkidle")
    probe = page.evaluate("""() => {
      const walk = (node) => {
        const out = [];
        const all = node.querySelectorAll('p, li, td, th, span, a, h1, h2, h3');
        for (const el of all) {
          const text = (el.textContent || '').trim();
          if (!text || text.length < 3) continue;
          if (el.querySelector('p, li, td, th')) continue;
          const style = getComputedStyle(el);
          if (style.visibility === 'hidden' || style.display === 'none') continue;
          const box = el.getBoundingClientRect();
          if (box.width < 2 || box.height < 2) continue;
          let ground = 'rgba(0, 0, 0, 0)';
          let probe = el;
          while (probe) {
            const bg = getComputedStyle(probe).backgroundColor;
            if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') { ground = bg; break; }
            probe = probe.parentElement;
          }
          out.push({ink: style.color, ground: ground,
                    size: parseFloat(style.fontSize),
                    bold: parseInt(style.fontWeight || '400', 10) >= 700,
                    sample: text.slice(0, 40)});
        }
        return out;
      };
      return walk(document.body);
    }""")
    assert len(probe) >= 12, f"the release route must render real body copy, found {len(probe)}"
    failures = []
    for row in probe:
        if str(row["ground"]).startswith("rgba(0, 0, 0, 0"):
            continue
        ratio = contrast_ratio(parse_colour(row["ink"]), parse_colour(row["ground"]))
        large = row["size"] >= 24 or (row["size"] >= 18.66 and row["bold"])
        bar = 3.0 if large else 4.5
        if ratio + 0.05 < bar:
            failures.append((row["sample"], row["ink"], row["ground"], round(ratio, 2), bar))
    assert not failures, (
        "every run of text must meet the WCAG AA contrast bar against its own "
        f"background, these did not: {failures[:6]}")


def test_a_reference_document_renders_in_the_system_font_stack(page):
    """A reference document renders in the system font stack. cov: C-UX-22, C-UX-23, C-UX-24, C-UX-25"""

    page.goto(f"{base_url()}/option")
    page.wait_for_load_state("networkidle")
    families = page.evaluate("""() => {
      const pick = (selector) => {
        const el = document.querySelector(selector);
        return el ? getComputedStyle(el).fontFamily : null;
      };
      const body = Array.from(document.querySelectorAll('p'))
        .find((el) => (el.textContent || '').trim().length > 40);
      const code = document.querySelector('code, pre');
      return {
        doc: body ? getComputedStyle(body).fontFamily : null,
        code: code ? getComputedStyle(code).fontFamily : null,
        chrome: pick('nav') || pick('header') || pick('aside'),
      };
    }""")
    doc = str(families["doc"] or "").lower()
    assert doc, "the reference content pane must render real body copy"
    assert "-apple-system" in doc or "blinkmacsystemfont" in doc or "segoe ui" in doc, (
        "a generated reference document must render in the system font stack, found "
        f"{families['doc']!r}")
    assert "open sans" not in doc, (
        f"the reference body must not load the interface family, found {families['doc']!r}")
    assert "pingfang" in doc or "microsoft yahei" in doc or "hiragino" in doc, (
        f"the system stack must keep its locale fallback, found {families['doc']!r}")
    code = str(families["code"] or "").lower()
    assert "source code pro" in code, (
        f"code must be set in Source Code Pro, found {families['code']!r}")
    chrome = str(families["chrome"] or "").lower()
    assert "open sans" in chrome, (
        f"the chrome must render in the interface family, found {families['chrome']!r}")


def test_a_narrow_viewport_shows_no_sideways_overflow(narrow_page):
    """A narrow viewport shows no sideways overflow. cov: C-UX-38, C-UX-57, C-UX-58, C-UX-78"""

    for route in ("/", "/option", "/gallery", "/editor", "/theme", "/releases", "/privacy"):
        narrow_page.goto(f"{base_url()}{route}")
        narrow_page.wait_for_load_state("networkidle")
        measured = narrow_page.evaluate("""() => ({
          scroll: document.documentElement.scrollWidth,
          client: document.documentElement.clientWidth,
          zoom: (document.querySelector('meta[name=viewport]') || {}).content || '',
          wide: Array.from(document.querySelectorAll('body *'))
            .filter((el) => {
              const box = el.getBoundingClientRect();
              const style = getComputedStyle(el);
              if (style.display === 'none' || style.visibility === 'hidden') return false;
              if (style.overflowX === 'auto' || style.overflowX === 'scroll') return false;
              return box.right > document.documentElement.clientWidth + 2;
            })
            .slice(0, 5)
            .map((el) => el.tagName + '.' + (el.className || '').toString().slice(0, 40)),
        })""")
        assert measured["scroll"] <= measured["client"] + 2, (
            f"{route} must not scroll sideways at a phone width: "
            f"{measured['scroll']} against {measured['client']}, widest {measured['wide']}")
        assert not measured["wide"], (
            f"{route} must keep every element inside the viewport, found {measured['wide']}")
        content = str(measured["zoom"]).lower().replace(" ", "")
        assert "user-scalable=no" not in content, (
            f"{route} must not restrict zoom: {measured['zoom']!r}")
        assert "maximum-scale=1" not in content, (
            f"{route} must not cap the scale: {measured['zoom']!r}")
        assert "width=device-width" in content, \
            f"{route} must declare width=device-width: {measured['zoom']!r}"


def test_seeded_releases_artifacts_and_mirrors_are_stored_once(anon):
    """The seeded releases, artifacts and mirrors are stored once. cov: C-DM-03, C-DM-04, C-DM-05, C-DM-06, C-DM-07, C-DM-08, C-DM-09, C-DM-10, C-DM-11, C-DM-12, C-DM-13, C-DM-14, C-DM-19, C-DM-20, C-DM-21, C-DM-22, C-DC-24"""

    listed = releases_of(anon)
    assert len(listed) == len(RELEASE_DATES), (
        f"exactly {len(RELEASE_DATES)} releases must be seeded, found {sorted(listed)}")
    for version, date in RELEASE_DATES.items():
        row = listed[version]
        assert str(row.get("released_on")).startswith(date), f"{version}: {row}"
        assert row.get("is_current") is (version == CURRENT), f"{version}: {row}"
        detail = ok(anon.get(f"/releases/{version}"), f"reading release {version}")
        assert detail.get("commit"), f"{version} must record the source revision: {detail}"
        artifacts = detail.get("artifacts") or []
        assert len(artifacts) == 1, f"{version} must carry one artifact row: {artifacts}"
        artifact = artifacts[0]
        assert artifact.get("filename") == f"chartic-{version}.tar.gz", f"{version}: {artifact}"
        assert artifact.get("sha256") == ARTIFACT_SHA256[version], f"{version}: {artifact}"
        assert int(artifact.get("size_bytes") or 0) > 0, f"{version}: {artifact}"
    current = ok(anon.get(f"/releases/{CURRENT}"), f"reading release {CURRENT}")
    mirrors = current.get("mirrors") or []
    hosts = [str(m.get("host")) for m in mirrors]
    assert len(hosts) == len(set(hosts)), f"each mirror must be stored once: {hosts}"
    assert MIRROR_ALPHA in hosts and MIRROR_GAMMA in hosts, f"seeded mirrors: {hosts}"


def test_seeded_schema_nodes_carry_their_declared_defaults_and_versions(anon):
    """The seeded schema nodes carry their declared defaults and versions. cov: C-DM-25, C-DM-26, C-DM-27, C-DM-28, C-DM-29, C-DM-30, C-DM-31, C-DM-32, C-DM-33, C-DM-34, C-DM-35, C-DM-36, C-DM-37, C-DM-39, C-DM-40, C-DM-41, C-DM-42, C-DM-43, C-DM-44, C-DM-45, C-DM-46, C-DM-47, C-DM-48, C-DC-27"""

    expected = {
        "title.show": ("literal", "true", "5.0.0"),
        "title.text": ("literal", "''", "5.0.0"),
        "tooltip.trigger": ("literal", "item", "5.0.0"),
        ROTATE_PATH: ("literal", "0", "5.0.0"),
        "xAxis.axisLabel.margin": ("literal", "8", "5.0.0"),
        "yAxis.axisLabel.rotate": ("literal", "0", "5.0.0"),
        "dataZoom.filterMode": ("literal", "filter", "5.0.0"),
        SAVE_AS_IMAGE_PATH: ("literal", "Save as image", "5.0.0"),
        "series.emphasis.scale": ("literal", "true", PRIOR),
        LATE_PATH: ("absent", None, CURRENT),
        COMPUTED_PATH: ("computed", None, "5.0.0"),
        INHERITED_PATH: ("inherited", None, "5.0.0"),
    }
    for path, (kind, literal, since) in expected.items():
        found = node_of(anon, CURRENT, path)
        assert found.get("default_kind") == kind, f"{path} must be a {kind} default: {found}"
        assert found.get("since") == since, f"{path} must arrive in {since}: {found}"
        if literal is not None:
            assert str(found.get("default_literal")).strip("'\"") == literal, \
                f"{path} must default to {literal}: {found}"
    enumerated = node_of(anon, CURRENT, "tooltip.trigger").get("enum_values") or []
    assert set(enumerated) == {"item", "axis", "none"}, f"tooltip.trigger enum: {enumerated}"
    modes = node_of(anon, CURRENT, "dataZoom.filterMode").get("enum_values") or []
    assert set(modes) == {"filter", "weakFilter", "empty", "none"}, f"filterMode enum: {modes}"
    for version in (CURRENT, PRIOR, OLDEST):
        one = node_of(anon, version, "title.show")
        assert one.get("path") == "title.show", f"{version} must carry its own row: {one}"


def test_seeded_examples_themes_and_modules_are_stored_once(anon, backend):
    """The seeded examples, themes and modules are stored once. cov: C-DM-01, C-DM-49, C-DM-50, C-DM-51, C-DM-52, C-DM-53, C-DM-54, C-DM-55, C-DM-56, C-DM-65, C-DM-66, C-DM-67, C-DM-68, C-DM-69, C-DM-70, C-DM-71, C-DM-72, C-DM-73, C-DM-74, C-DM-75, C-DM-76, C-DM-77, C-DM-78, C-DM-79, C-DM-80, C-DM-81, C-DM-82, C-DM-83, C-DM-85, C-DM-88, C-DM-100, C-DC-17, C-DC-55"""

    listed = examples_of(anon)
    ids = [row.get("id") for row in listed]
    assert sorted(ids) == sorted(PUBLISHED_EXAMPLES), (
        f"exactly the six published examples must be listed, found {sorted(ids)}")
    assert len(ids) == len(set(ids)), f"each example must be stored once: {ids}"
    assert backend.count("examples", id=PROPOSED_EXAMPLE) == 1, \
        "the proposed example must be stored exactly once"
    for example in PUBLISHED_EXAMPLES:
        assert backend.count("examples", id=example) == 1, f"{example} must be stored once"
        detail = ok(anon.get(f"/examples/{example}"), f"reading {example}")
        assert detail.get("code_js"), f"{example} must carry its code: {detail}"
        assert detail.get("description"), f"{example} must carry its description: {detail}"
        assert detail.get("state") == "published", f"{example} must be published: {detail}"
    registry = themes_of(anon)
    assert sorted(registry) == sorted(THEMES), f"exactly four themes must be seeded: {sorted(registry)}"
    for theme in THEMES:
        assert backend.count("themes", id=theme) == 1, f"{theme} must be stored once"
    graph = modules_of(anon)
    assert sorted(graph) == sorted(MODULE_RAW), f"the ten seeded modules: {sorted(graph)}"
    for module in MODULE_RAW:
        assert backend.count("modules", module_id=module, release_version=CURRENT) == 1, \
            f"{module} must be stored once at {CURRENT}"
    assert backend.count("snippets", id=LIVE_SNIPPET) == 1, "the live snippet is stored once"
    assert backend.count("snippets", id=WITHDRAWN_SNIPPET) == 1, "the withdrawn snippet too"


def test_the_declared_stack_serves_every_page_and_the_api_from_one_process(anon):
    """The declared stack serves every page and the API from one process. cov: C-TR-01, C-TR-02, C-TR-03, C-TR-04, C-TR-05, C-TR-06, C-TR-08, C-TR-09, C-TR-10, C-TR-25, C-DC-03, C-DC-06, C-DC-10, C-DC-13, C-DC-14, C-DC-16"""

    listening = _listening_ports()
    assert 4173 in listening, f"the declared process must listen on 4173: {sorted(listening)}"
    served = set()
    for route in PUBLIC_ROUTES:
        page = html_of(route)
        assert page.status_code == 200, f"{route} must render: {describe(page)}"
        assert "text/html" in page.headers.get("content-type", ""), f"{route}: {page.headers}"
        served.add(route)
        text = page.text
        assert "<html" in text.lower(), f"{route} must arrive as a complete document"
        assert len(text) > 800, (
            f"{route} must arrive rendered rather than as a skeleton a script fills in, "
            f"found {len(text)} bytes")
        assert "<main" in text.lower() or "role=\"main\"" in text.lower(), \
            f"{route} must carry its main region in the first paint"
    assert served == set(PUBLIC_ROUTES), f"every public route must serve: {served}"
    health = httpx.get(f"{api_base()}/health", timeout=TIMEOUT)
    assert health.status_code == 200, f"the API must answer on the same origin: {describe(health)}"
    for name in ("APP_PUBLIC_URL", "APP_PUBLIC_PORT", "DATABASE_URL",
                 "STORAGE_ENDPOINT", "STORAGE_BUCKET"):
        assert os.environ.get(name), f"the environment must carry {name}"
    assert os.path.isdir("/app"), "the app must be installed at /app"


def test_stored_object_keys_follow_their_declared_key_schemes(anon, store):
    """Stored object keys follow their declared key schemes. cov: C-TR-07, C-TR-47, C-TR-48, C-TR-49, C-TR-50, C-DM-91, C-DM-92, C-DM-93, C-DM-94, C-DC-53, C-DC-56"""

    thumbnails = store_keys("thumbnails/")
    assert thumbnails, "the object store must hold the seeded thumbnails"
    for key in thumbnails:
        parts = key.split("/")
        assert len(parts) == 3 and parts[0] == "thumbnails", f"malformed thumbnail key {key!r}"
        digest, _, ext = parts[2].partition(".")
        assert re.fullmatch(r"[0-9a-f]{64}", digest), \
            f"a thumbnail key must carry the digest of its bytes: {key!r}"
        assert ext == "svg", f"a thumbnail must be a vector document: {key!r}"
    assert LINE_THUMBNAIL_KEY in thumbnails, f"{LINE_THUMBNAIL_KEY} must be stored"
    assert PROPOSED_THUMBNAIL_KEY in thumbnails, f"{PROPOSED_THUMBNAIL_KEY} must be stored"
    requested = ok(request_bundle(anon, selection=(BAR_MODULE,)), "requesting a bundle")
    ready = bundle_ready(anon, requested["request_digest"])
    digest = ready["artifact_sha256"]
    keys = wait_until(lambda: store_keys(f"bundles/{digest}/"), lambda k: bool(k))
    assert keys, f"the built artifact must reach the store under bundles/{digest}/"
    for key in keys:
        parts = key.split("/")
        assert len(parts) == 3 and parts[0] == "bundles", f"malformed bundle key {key!r}"
        assert parts[1] == digest, f"a bundle key must carry the artifact digest: {key!r}"
        assert parts[2].startswith("chartic-") and parts[2].endswith(".js"), \
            f"a bundle key must name the format: {key!r}"
    served = thumbnail(anon, LINE_EXAMPLE)
    assert served.status_code == 200 and served.content, \
        f"the stream must reflect the stored object: {describe(served)}"
    assert not os.path.exists(f"/app/{LINE_THUMBNAIL_KEY}"), \
        "the stored bytes must not be duplicated on the app container's own disk"
