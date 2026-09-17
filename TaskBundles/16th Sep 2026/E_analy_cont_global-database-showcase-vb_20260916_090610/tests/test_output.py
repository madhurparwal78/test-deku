from __future__ import annotations

import os
import re

import appclient
from conftest import (
    ADMIN_EMAIL, ALLOWED_FONT_SIZES, ANALYTICS_SLUGS, ART_PAGE_SIZE, ASSISTANT_CAP,
    BLOCKING_REQUEST_MAX, BODY_FAMILY, CONSOLE_VALUE, CONTACT_INTERESTS, CONTACT_MESSAGE_MAX,
    CONTACT_REGIONS, CONTRAST_FLOOR, COOKIE_CHOICE_CONTROLS, COPY_STRINGS, CUSTOMER_NAMES,
    DATABASES_SLUGS, DATASHEET_FILENAMES, DISPLAY_FAMILY, DRAFT_ART, DRAFT_DATASHEET_TITLE,
    DRAFT_NAME, DRAFT_SLUG, EDITOR_EMAIL, FAMILY_COUNTS, FAMILY_NAMES, FAMILY_SLUGS,
    FEATURED_SLUGS, FLAGSHIP_DATASHEET_TITLE, FLAGSHIP_HIGHLIGHTS, FLAGSHIP_NAME,
    FLAGSHIP_REGIONS, FLAGSHIP_SERVICE_LEVEL, FLAGSHIP_SLUG, INDUSTRY_NAMES, MESSAGE_STACK_MAX,
    NAME_MIN, NARROW_VIEWPORT, NETWORKING_SLUGS, PAGE_TYPES, PASSWORD, PLATFORM_DATASHEETS,
    PUBLIC_ROUTES, PUBLISHED_COUNT, PUBLISHED_SLUGS, PUBLISHER_EMAIL, RAIL_HEADING, REGIONS,
    RESERVED_SEGMENTS, RHYTHM_STEP, SCRIPT_BUDGET_BYTES, SUMMARY_MAX, TIERS,
    TOUCH_TARGET_MIN, TYPE_STEPS, WIDE_VIEWPORT, add_art, contrast_ratio, create_draft,
    denied, describe, drop, json_list, names_of, parse_rgb, poll_until, product_id,
    product_payload, publish, settle, slugs_of, unpublish,
    CONSOLE_TIMESTAMP, COVER_RATIO, FAMILY_STANDFIRSTS, FLAGSHIP_ART, FLAGSHIP_ART_ALT,
    FLAGSHIP_HIGHLIGHT_FIRST, FLAGSHIP_SUBNAV_ITEM, PROBE_PDF_PAGES, probe_pdf, put_upload,
    FAMILY_INTROS,
)


def test_product_index_lists_only_published_products(api):
    """The product index answers with the eight published products and no draft."""
    rows = json_list(api.get("/products"), "GET /api/products")
    slugs = slugs_of(rows)
    missing = sorted(set(PUBLISHED_SLUGS) - slugs)
    assert not missing, (
        f"the index should carry every published product; missing {missing}, "
        f"saw {sorted(slugs)}"
    )
    assert DRAFT_SLUG not in slugs, (
        f"{DRAFT_SLUG!r} is in state draft, so the index must not carry it; "
        f"saw {sorted(slugs)}"
    )
    assert len(rows) == PUBLISHED_COUNT, (
        f"the seed holds {PUBLISHED_COUNT} published products; the index answered "
        f"{len(rows)} rows"
    )


def test_draft_product_address_answers_like_an_unknown_one(api):
    """The draft product's address answers exactly as an unknown address does."""
    draft = api.get(f"/products/{DRAFT_SLUG}")
    unknown = api.get("/products/no-such-product-" + os.urandom(3).hex())
    assert draft.status_code >= 400, (
        f"the draft address must not answer with the product: {describe(draft)}"
    )
    assert draft.status_code == unknown.status_code, (
        f"the draft address answers as an unknown address does, so its existence is not "
        f"disclosed; saw {draft.status_code} against {unknown.status_code}"
    )
    assert draft.status_code != 403, (
        f"the draft address never answers forbidden: {describe(draft)}"
    )


def test_no_state_parameter_makes_a_public_response_carry_a_draft(api):
    """No query parameter persuades a public endpoint to answer with a draft."""
    probes = ("?state=all", "?state=draft", "?include_drafts=true", "?draft=1",
              "?published=false")
    for probe in probes:
        rows = json_list(api.get("/products" + probe), "GET /api/products" + probe)
        assert DRAFT_SLUG not in slugs_of(rows), (
            f"the parameter {probe!r} must not make the public index answer with "
            f"{DRAFT_SLUG!r}; saw {sorted(slugs_of(rows))}"
        )


def test_draft_art_bytes_are_denied_to_an_anonymous_caller(anon, desk):
    """An art piece belonging to a draft product is denied to an anonymous caller."""
    drafts = json_list(desk.get("/desk/products?state=draft"),
                       "GET /api/desk/products?state=draft")
    assert drafts, "the seed holds a draft product whose art can be probed"
    pid = str(drafts[0]["id"])
    detail = desk.get(f"/desk/products/{pid}").json()
    pieces = detail.get("art") or []
    assert pieces, f"the draft product carries art pieces: {detail!r}"
    for piece in pieces:
        r = anon.get(f"/media/art/{piece['id']}")
        assert r.status_code == 404, (
            f"the bytes of a draft product's art piece are denied to an anonymous "
            f"caller: {describe(r)}"
        )


def test_draft_datasheet_bytes_are_denied_to_anonymous(anon, desk):
    """A datasheet belonging to a draft product is denied to an anonymous caller."""
    drafts = json_list(desk.get("/desk/products?state=draft"),
                       "GET /api/desk/products?state=draft")
    pid = str(drafts[0]["id"])
    detail = desk.get(f"/desk/products/{pid}").json()
    sheet = detail.get("datasheet")
    assert sheet, f"the draft product carries a datasheet: {detail!r}"
    r = anon.get(f"/media/datasheets/{sheet['id']}")
    assert r.status_code == 404, (
        f"the bytes of a draft product's datasheet are denied to an anonymous "
        f"caller: {describe(r)}"
    )


def test_the_search_overlay_lists_only_published_products(page):
    """The header search overlay filters published products and never offers a draft."""
    origin = appclient.app_url()
    page.goto(f"{origin}/")
    page.get_by_role("banner").get_by_role("button", name=re.compile("search", re.I)).first.click()
    field = page.wait_for_selector("[role=dialog] input, dialog input", timeout=5000)
    field.fill(DRAFT_NAME[:4])
    settle()
    results = page.inner_text("[role=dialog], dialog")
    assert DRAFT_NAME not in results, (
        f"the search overlay lists published products only; typing "
        f"{DRAFT_NAME[:4]!r} offered {DRAFT_NAME!r}"
    )
    field.fill("tess")
    settle()
    assert FLAGSHIP_NAME in page.inner_text("[role=dialog], dialog"), (
        f"the search overlay filters the published products by name; 'tess' did not "
        f"offer {FLAGSHIP_NAME!r}"
    )
    page.keyboard.press("Escape")
    settle()
    assert not page.query_selector("[role=dialog]:visible, dialog[open]"), (
        "Escape closes the search overlay"
    )


def test_unpublished_product_objects_stop_resolving_at_once(api, desk):
    """Returning a product to draft stops its object answers at once."""
    entry = create_draft(desk, name="Probe Revoked Engine")
    pid = product_id(entry)
    try:
        piece = add_art(desk, pid)
        assert publish(desk, pid).status_code in (200, 201), "the probe should publish"
        settle()
        assert api.get(f"/media/art/{piece['id']}").status_code == 200, (
            "the published product's art streams before the unpublish"
        )
        assert unpublish(desk, pid).status_code in (200, 201), "the probe should unpublish"

        def revoked():
            return api.get(f"/media/art/{piece['id']}").status_code == 404

        poll_until(revoked, "the art of an unpublished product stops resolving")
        public = slugs_of(json_list(api.get("/products"), "GET /api/products"))
        assert str(entry.get("slug")) not in public, (
            "the unpublished product leaves the public index together with its bytes"
        )
    finally:
        drop(desk, pid)


def test_every_art_piece_carries_alternative_text(api, page):
    """Every art piece carries alternative text, in the response and on the page."""
    rows = json_list(api.get("/art"), "GET /api/art")
    bare = [r for r in rows if not str(r.get("alt_text") or "").strip()]
    assert not bare, (
        f"every art piece carries alternative text; {[r.get('id') for r in bare]} "
        f"carry none"
    )
    origin = appclient.app_url()
    page.goto(f"{origin}/gallery")
    missing = page.evaluate(
        "() => Array.from(document.images)"
        ".filter(i => !(i.getAttribute('alt') || '').trim())"
        ".map(i => i.currentSrc || i.src)")
    assert not missing, (
        f"every image drawn in the gallery carries alternative text; saw {missing}"
    )


def test_decorative_images_declare_themselves_decorative(page):
    """Decorative images declare themselves decorative; icon-only controls carry a name."""
    origin = appclient.app_url()
    for route in ("/", "/product/tessera", "/console"):
        page.goto(f"{origin}{route}")
        found = page.evaluate(
            "() => {"
            " const deco = Array.from(document.querySelectorAll('img, svg')).filter(e =>"
            "   e.closest('[aria-hidden=true]') || e.getAttribute('role') === 'presentation');"
            " const badDeco = deco.filter(e => e.tagName === 'IMG' && (e.getAttribute('alt') || '').trim() !== '');"
            " const iconOnly = Array.from(document.querySelectorAll('button, a')).filter(e =>"
            "   !(e.textContent || '').trim() && e.querySelector('svg, img'));"
            " const unnamed = iconOnly.filter(e => !(e.getAttribute('aria-label') ||"
            "   e.getAttribute('title') || '').trim());"
            " const marks = Array.from(document.querySelectorAll('button svg, a svg')).filter(s =>"
            "   getComputedStyle(s).color !== getComputedStyle(s.parentElement).color);"
            " return {decorative: deco.length, badDeco: badDeco.length, unnamed: unnamed.length,"
            "   offColour: marks.length};}")
        assert found["badDeco"] == 0, (
            f"a decorative image on {route} declares itself decorative with empty "
            f"alternative text; {found['badDeco']} carry a description"
        )
        assert found["unnamed"] == 0, (
            f"every icon-only control on {route} carries an accessible name; "
            f"{found['unnamed']} carry none"
        )
        assert found["offColour"] == 0, (
            f"each mark on {route} takes the colour of the text around it; "
            f"{found['offColour']} do not"
        )


def test_no_analytics_cookie_is_set_before_the_visitor_chooses(page):
    """No analytics or preference cookie is set before the visitor has chosen."""
    origin = appclient.app_url()
    page.context.clear_cookies()
    page.goto(f"{origin}/")
    before = page.context.cookies()
    body = page.content()
    for control in COOKIE_CHOICE_CONTROLS:
        assert control in body, (
            f"a first-time visitor is offered the cookie choice, carrying the "
            f"{control!r} control; saw neither on the home surface"
        )
    assert len(before) <= 1, (
        f"no analytics or preference cookie is set before the visitor chooses; the "
        f"first view set {[c.get('name') for c in before]}"
    )
    page.get_by_text(COOKIE_CHOICE_CONTROLS[1], exact=True).first.click()
    settle()
    after = {c.get("name") for c in page.context.cookies()}
    assert after, (
        "the choice itself is recorded, so declining sets the one cookie that "
        "remembers the decision"
    )


def test_the_cookie_choice_is_remembered_across_routes(page):
    """A recorded cookie choice is not asked for again."""
    origin = appclient.app_url()
    page.context.clear_cookies()
    page.goto(f"{origin}/")
    page.get_by_text(COOKIE_CHOICE_CONTROLS[1], exact=True).first.click()
    settle()
    page.goto(f"{origin}/product")
    assert COOKIE_CHOICE_CONTROLS[0] not in page.content(), (
        "the cookie choice band does not return on the next public surface once the "
        "visitor has chosen"
    )
    page.reload()
    assert COOKIE_CHOICE_CONTROLS[0] not in page.content(), (
        "the cookie choice band does not return after a reload once the visitor has "
        "chosen"
    )


def test_every_public_route_carries_its_own_title_and_description(page):
    """Every public route carries a distinctive title and description."""
    origin = appclient.app_url()
    seen = {}
    for route in PUBLIC_ROUTES:
        page.goto(f"{origin}{route}")
        meta = page.evaluate(
            "() => ({title: document.title,"
            " description: (document.querySelector('meta[name=description]') || {})"
            ".content || ''})")
        assert meta["title"].strip(), f"{route} carries a page title; saw {meta!r}"
        assert meta["description"].strip(), (
            f"{route} carries a description meta tag; saw {meta!r}"
        )
        seen[route] = (meta["title"].strip(), meta["description"].strip())
    titles = [t for t, _ in seen.values()]
    assert len(set(titles)) == len(titles), (
        f"each route's title is distinctive rather than one platform-wide pair; saw "
        f"{sorted(titles)}"
    )
    descriptions = [d for _, d in seen.values()]
    assert len(set(descriptions)) == len(descriptions), (
        f"each route's description is distinctive; saw {len(set(descriptions))} "
        f"distinct across {len(descriptions)} routes"
    )
    product_title = seen["/product/tessera"][0]
    assert FLAGSHIP_NAME in product_title, (
        f"a product page title carries the product name; {product_title!r} omits "
        f"{FLAGSHIP_NAME!r}"
    )


def test_every_public_route_records_a_page_view(admin, page):
    """Every public route records a view the administrator's count list reflects."""
    origin = appclient.app_url()

    def counts():
        body = admin.get("/desk/views").json()
        return {str(r.get("route")): int(r.get("count") or 0)
                for r in (body.get("counts") or [])}

    before = counts()
    for route in PUBLIC_ROUTES:
        page.goto(f"{origin}{route}")
    settle()
    after = counts()
    missing = [r for r in PUBLIC_ROUTES if after.get(r, 0) <= before.get(r, 0)]
    assert not missing, (
        f"every public route records a view; {missing} did not rise between {before} and {after}"
    )
    ordered = [int(r.get("count") or 0)
               for r in (admin.get("/desk/views").json().get("counts") or [])]
    assert ordered == sorted(ordered, reverse=True), (
        f"the view counts are ordered by count descending; saw {ordered}"
    )

def test_the_page_view_log_carries_route_and_time(admin, page):
    """A recorded view carries the route as requested and its time."""
    origin = appclient.app_url()
    page.goto(f"{origin}/product/{FLAGSHIP_SLUG}")
    settle()
    r = admin.get("/desk/views")
    assert r.status_code == 200, f"an administrator reads the view log: {describe(r)}"
    body = r.json()
    assert isinstance(body.get("counts"), list) and isinstance(body.get("recent"), list), (
        f"the view log answers with a count list and a recent list: {body!r}"
    )
    recent = body["recent"]
    hit = [v for v in recent if v.get("route") == f"/product/{FLAGSHIP_SLUG}"]
    assert hit, (
        f"a view of /product/{FLAGSHIP_SLUG} is recorded with the route as requested; "
        f"saw {[v.get('route') for v in recent[:10]]}"
    )
    assert hit[0].get("viewed_at"), f"a recorded view carries its time: {hit[0]!r}"
    extra = set(hit[0]) - {"route", "viewed_at", "id"}
    assert not extra, (
        f"a recorded view carries a route and a time and no visitor identifier; it also "
        f"carries {sorted(extra)}"
    )


def test_body_text_contrast_meets_the_accessibility_bar(page):
    """Body text meets the pinned contrast floor against its ground."""
    origin = appclient.app_url()
    page.goto(f"{origin}/product/tessera")
    pair = page.evaluate(
        "() => {const el = document.querySelector('main p') || document.body;"
        " const s = getComputedStyle(el);"
        " let bg = s.backgroundColor, node = el;"
        " while (node && (bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent')) {"
        "   node = node.parentElement;"
        "   if (!node) break;"
        "   bg = getComputedStyle(node).backgroundColor; }"
        " return {fg: s.color, bg: bg || 'rgb(255, 255, 255)'};}")
    ratio = contrast_ratio(parse_rgb(pair["fg"]), parse_rgb(pair["bg"]))
    assert ratio >= CONTRAST_FLOOR, (
        f"body text meets {CONTRAST_FLOOR} to 1 against its ground; {pair!r} measures "
        f"{ratio:.2f} to 1"
    )


def test_strong_read_from_another_region_returns_the_last_write(api):
    """A strong read from another region returns the value just written."""
    key = f"probe-{os.urandom(4).hex()}"
    w = api.post("/console/write", json={"region": REGIONS[0], "key": key,
                                         "value": CONSOLE_VALUE})
    assert w.status_code in (200, 201), (
        f"a console write in {REGIONS[0]!r} should commit: {describe(w)}"
    )
    for region in REGIONS[1:]:
        r = api.post("/console/read", json={"region": region, "key": key,
                                            "mode": "strong"})
        assert r.status_code == 200, (
            f"a strong read from {region!r} should answer 200: {describe(r)}"
        )
        body = r.json()
        assert body.get("value") == CONSOLE_VALUE, (
            f"a strong read from {region!r} returns the value just written in "
            f"{REGIONS[0]!r}; saw {body.get('value')!r}"
        )
        assert "latency_ms" in body, (
            f"a console read reports a latency figure: {body!r}"
        )
        assert not body.get("staleness"), (
            f"a strong read reports no staleness; {region!r} answered "
            f"{body.get('staleness')!r}"
        )


def test_strong_read_never_returns_a_stale_value(api):
    """No strong read answers with a value older than an acknowledged write."""
    key = f"probe-{os.urandom(4).hex()}"
    seen = []
    for index, region in enumerate(REGIONS):
        value = f"v{index}"
        w = api.post("/console/write", json={"region": region, "key": key,
                                             "value": value})
        assert w.status_code in (200, 201), (
            f"the write of {value!r} in {region!r} should commit: {describe(w)}"
        )
        for reader in REGIONS:
            r = api.post("/console/read", json={"region": reader, "key": key,
                                                "mode": "strong"})
            assert r.status_code == 200, (
                f"a strong read from {reader!r} should answer 200: {describe(r)}"
            )
            got = r.json().get("value")
            seen.append((region, value, reader, got))
            assert got == value, (
                f"a strong read from {reader!r} must not answer with a value older "
                f"than the acknowledged write {value!r} made in {region!r}; saw "
                f"{got!r}. Trail: {seen[-4:]}"
            )


def test_commit_waits_out_an_uncertainty_above_zero(api):
    """A commit reports an uncertainty above zero and does not answer before it passes."""
    import time as _time

    key = f"probe-{os.urandom(4).hex()}"
    started = _time.monotonic()
    r = api.post("/console/write", json={"region": REGIONS[1], "key": key,
                                         "value": CONSOLE_VALUE})
    elapsed_ms = (_time.monotonic() - started) * 1000
    assert r.status_code in (200, 201), f"the write should commit: {describe(r)}"
    body = r.json()
    assert body.get("commit_timestamp"), f"a commit carries its timestamp: {body!r}"
    uncertainty = body.get("uncertainty_ms")
    assert isinstance(uncertainty, (int, float)) and uncertainty > 0, (
        f"uncertainty_ms is always greater than zero: {body!r}"
    )
    assert elapsed_ms >= uncertainty, (
        f"the write does not answer before its reported uncertainty has passed; it "
        f"reported {uncertainty} ms and answered after {elapsed_ms:.0f} ms"
    )


def test_bounded_read_stays_within_the_bound_it_is_given(api):
    """A bounded read never reports a staleness past the bound it is given."""
    key = f"probe-{os.urandom(4).hex()}"
    api.post("/console/write", json={"region": REGIONS[0], "key": key,
                                     "value": CONSOLE_VALUE})
    for bound in (50, 500, 5000):
        r = api.post("/console/read", json={"region": REGIONS[2], "key": key,
                                            "mode": "bounded", "bound": bound})
        assert r.status_code == 200, f"a bounded read should answer: {describe(r)}"
        body = r.json()
        assert "staleness" in body, f"a bounded read reports its staleness: {body!r}"
        assert 0 <= float(body["staleness"]) <= bound, (
            f"a bounded read never returns a value staler than its bound; bound {bound} "
            f"answered staleness {body['staleness']!r}"
        )


def test_exact_read_answers_at_the_timestamp_it_is_given(api):
    """An exact read answers at the timestamp it is given."""
    key = f"probe-{os.urandom(4).hex()}"
    first = api.post("/console/write", json={"region": REGIONS[0], "key": key,
                                             "value": "first"})
    assert first.status_code in (200, 201), f"the first write commits: {describe(first)}"
    stamp = first.json().get("commit_timestamp")
    api.post("/console/write", json={"region": REGIONS[0], "key": key,
                                     "value": "second"})
    r = api.post("/console/read", json={"region": REGIONS[1], "key": key,
                                        "mode": "exact", "timestamp": stamp})
    assert r.status_code == 200, f"an exact read should answer 200: {describe(r)}"
    body = r.json()
    assert body.get("value") == "first", (
        f"an exact read at the first commit timestamp answers with the value that was "
        f"current then; saw {body.get('value')!r}"
    )


def test_an_unknown_region_or_mode_is_refused(api):
    """A console request naming an unknown region or mode is refused as invalid."""
    key = f"probe-{os.urandom(4).hex()}"
    region = api.post("/console/write", json={"region": "mars-north", "key": key,
                                              "value": CONSOLE_VALUE})
    assert 400 <= region.status_code < 500, (
        f"a write naming an unknown region is refused as a client error: {describe(region)}"
    )
    mode = api.post("/console/read", json={"region": REGIONS[0], "key": key,
                                           "mode": "eventual"})
    assert 400 <= mode.status_code < 500, (
        f"a read naming an unknown mode is refused as a client error: {describe(mode)}"
    )


def test_write_against_a_severed_region_is_refused(api):
    """A write attempted against a severed region is refused."""
    region = REGIONS[2]
    try:
        cut = api.post("/console/partition", json={"region": region, "severed": True})
        assert cut.status_code in (200, 201), (
            f"severing {region!r} should answer with the region set: {describe(cut)}"
        )
        r = api.post("/console/write", json={"region": region,
                                             "key": f"probe-{os.urandom(4).hex()}",
                                             "value": CONSOLE_VALUE})
        assert r.status_code >= 400, (
            f"a write against the severed {region!r} is refused rather than accepted: "
            f"{describe(r)}"
        )
    finally:
        api.post("/console/partition", json={"region": region, "severed": False})
        api.post("/console/reset")


def test_majority_side_write_commits_while_a_region_is_severed(api):
    """A write on the majority side commits while one region stays severed."""
    severed = REGIONS[2]
    key = f"probe-{os.urandom(4).hex()}"
    try:
        api.post("/console/partition", json={"region": severed, "severed": True})
        w = api.post("/console/write", json={"region": REGIONS[1], "key": key,
                                             "value": CONSOLE_VALUE})
        assert w.status_code in (200, 201), (
            f"a write on the majority side still commits while {severed!r} is severed: "
            f"{describe(w)}"
        )
        r = api.post("/console/read", json={"region": REGIONS[0], "key": key,
                                            "mode": "strong"})
        assert r.status_code == 200 and r.json().get("value") == CONSOLE_VALUE, (
            f"a read on the majority side stays correct while {severed!r} is severed: "
            f"{describe(r)}"
        )
    finally:
        api.post("/console/partition", json={"region": severed, "severed": False})
        api.post("/console/reset")


def test_restoring_a_severed_region_resyncs_it(api):
    """A restored region re-syncs and answers with the majority value."""
    severed = REGIONS[3]
    key = f"probe-{os.urandom(4).hex()}"
    try:
        api.post("/console/partition", json={"region": severed, "severed": True})
        api.post("/console/write", json={"region": REGIONS[0], "key": key,
                                         "value": CONSOLE_VALUE})
        api.post("/console/partition", json={"region": severed, "severed": False})

        def resynced():
            r = api.post("/console/read", json={"region": severed, "key": key,
                                                "mode": "strong"})
            return r.status_code == 200 and r.json().get("value") == CONSOLE_VALUE

        poll_until(resynced, f"the restored {severed!r} re-syncs to the majority value")
    finally:
        api.post("/console/partition", json={"region": severed, "severed": False})
        api.post("/console/reset")


def test_partition_response_carries_all_five_regions(api):
    """The partition route answers with the five named regions and their flags."""
    r = api.post("/console/partition", json={"region": REGIONS[0], "severed": False})
    assert r.status_code in (200, 201), (
        f"the partition route should answer with the region set: {describe(r)}"
    )
    body = r.json()
    rows = body if isinstance(body, list) else (body.get("regions") or [])
    names = {str(row.get("region")) for row in rows}
    assert names == set(REGIONS), (
        f"the console names the five regions {sorted(REGIONS)}; saw {sorted(names)}"
    )
    for row in rows:
        assert "severed" in row, f"each region carries its severed flag: {row!r}"


def test_console_reset_returns_the_seeded_state(api):
    """A reset returns the console to its seeded state with nothing severed."""
    api.post("/console/partition", json={"region": REGIONS[4], "severed": True})
    r = api.post("/console/reset")
    assert r.status_code in (200, 201), f"the reset should answer 200: {describe(r)}"
    after = api.post("/console/partition", json={"region": REGIONS[0],
                                                 "severed": False})
    body = after.json()
    rows = body if isinstance(body, list) else (body.get("regions") or [])
    severed = [str(row.get("region")) for row in rows if row.get("severed")]
    assert not severed, (
        f"the seeded console state carries no severed region; after a reset "
        f"{severed} were still severed"
    )


def test_product_detail_carries_claims_and_highlights(api):
    """The flagship product answers with its claim set, highlights and service level."""
    r = api.get(f"/products/{FLAGSHIP_SLUG}")
    assert r.status_code == 200, (
        f"GET /api/products/{FLAGSHIP_SLUG} should answer 200: {describe(r)}"
    )
    body = r.json()
    for field in ("id", "slug", "name", "eyebrow", "summary", "claim_body"):
        assert body.get(field), (
            f"a product should carry {field!r}: {body!r}"
        )
    assert body["name"] == FLAGSHIP_NAME, (
        f"the flagship product is named {FLAGSHIP_NAME!r}; saw {body.get('name')!r}"
    )
    highlights = body.get("highlights") or []
    assert len(highlights) == FLAGSHIP_HIGHLIGHTS, (
        f"the flagship carries {FLAGSHIP_HIGHLIGHTS} highlight lines; saw "
        f"{len(highlights)}"
    )
    assert str(body.get("service_level")) == FLAGSHIP_SERVICE_LEVEL, (
        f"the flagship service level is {FLAGSHIP_SERVICE_LEVEL!r}; saw "
        f"{body.get('service_level')!r}"
    )
    assert int(body.get("regions_available") or 0) == FLAGSHIP_REGIONS, (
        f"the flagship is available in {FLAGSHIP_REGIONS} regions; saw "
        f"{body.get('regions_available')!r}"
    )
    assert body.get("art"), f"the flagship carries its art pieces: {body!r}"


def test_product_related_row_shares_a_family(api):
    """A product's related row draws only published products sharing a family."""
    body = api.get(f"/products/{FLAGSHIP_SLUG}").json()
    families = {str(f).lower() for f in (body.get("families") or [])}
    assert families, f"the flagship carries at least one family: {body!r}"
    related = body.get("related") or []
    assert related, f"the flagship carries a related row: {body!r}"
    for row in related:
        assert row.get("slug") != FLAGSHIP_SLUG, (
            f"the related row should not carry the product itself: {row!r}"
        )
        assert row.get("slug") != DRAFT_SLUG, (
            f"the related row must not carry the draft product: {row!r}"
        )
        shared = families & {str(f).lower() for f in (row.get("families") or [])}
        assert shared, (
            f"a related product shares a family with the product it sits under; "
            f"{row.get('slug')!r} carries {row.get('families')!r} against {sorted(families)}"
        )
    indexes = [int(r.get("sort_index") or 0) for r in related]
    assert indexes == sorted(indexes), (
        f"the related row is ordered by sort index ascending; saw {indexes}"
    )


def test_index_name_filter_narrows_to_one_product(api):
    """A partial, case-insensitive name filter narrows the index to one product."""
    rows = json_list(api.get("/products?name=slip"), "GET /api/products?name=slip")
    slugs = slugs_of(rows)
    assert slugs == {"slipstream"}, (
        f"the name filter 'slip' should leave Slipstream alone; saw {sorted(slugs)}"
    )
    upper = json_list(api.get("/products?name=SLIP"), "GET /api/products?name=SLIP")
    assert slugs_of(upper) == slugs, (
        f"the name filter ignores letter case; 'SLIP' answered {sorted(slugs_of(upper))}"
    )


def test_index_family_filter_narrows_to_a_family(api):
    """The family filter narrows the index to the products carrying that family."""
    rows = json_list(api.get("/products?family=analytics"),
                     "GET /api/products?family=analytics")
    slugs = slugs_of(rows)
    expected = {s for s in ANALYTICS_SLUGS if s != DRAFT_SLUG}
    assert slugs == expected, (
        f"the Analytics family carries {sorted(expected)}; the filter answered "
        f"{sorted(slugs)}"
    )


def test_index_sort_by_name_orders_products_alphabetically(api):
    """The name sort orders the index alphabetically."""
    rows = json_list(api.get("/products?sort=name"), "GET /api/products?sort=name")
    names = [str(r.get("name")) for r in rows]
    assert names == sorted(names), (
        f"the name sort orders the index alphabetically; saw {names}"
    )


def test_index_sort_by_recent_orders_newest_first(api, desk):
    """The recent sort puts the most recently added product first."""
    entry = create_draft(desk, name="Probe Recency Engine")
    pid = product_id(entry)
    try:
        add_art(desk, pid)
        assert publish(desk, pid).status_code in (200, 201), (
            "the probe product should publish so the recency sort can be read"
        )
        settle()
        rows = json_list(api.get("/products?sort=recent"),
                         "GET /api/products?sort=recent")
        assert rows, "the recent sort answers the published products"
        assert str(rows[0].get("slug")) == str(entry.get("slug")), (
            f"the most recently added product leads the recent sort; saw "
            f"{rows[0].get('slug')!r}"
        )
    finally:
        unpublish(desk, pid)
        drop(desk, pid)
        settle()


def test_a_filter_matching_nothing_returns_an_empty_array(api):
    """A filter matching nothing answers with a top-level empty array."""
    r = api.get("/products?name=zzzz")
    rows = json_list(r, "GET /api/products?name=zzzz")
    assert rows == [], (
        f"a filter matching nothing answers an empty array rather than every row: "
        f"{describe(r)}"
    )


def test_index_count_line_reconciles_with_the_published_rows(api, page):
    """The count line on the product index reads the number of published rows."""
    rows = json_list(api.get("/products"), "GET /api/products")
    origin = appclient.app_url()
    page.goto(f"{origin}/product")
    text = page.content()
    assert f"{len(rows)} products" in text, (
        f"the index count line should read '{len(rows)} products' to match the "
        f"{len(rows)} rows the API answered"
    )


def test_families_endpoint_returns_the_three_seeded_families(api):
    """The three product families answer with their names and published counts."""
    rows = json_list(api.get("/families"), "GET /api/families")
    slugs = slugs_of(rows)
    assert slugs == set(FAMILY_SLUGS), (
        f"the seed holds the families {sorted(FAMILY_SLUGS)}; saw {sorted(slugs)}"
    )
    names = names_of(rows)
    assert names == set(FAMILY_NAMES), (
        f"the family names are {sorted(FAMILY_NAMES)}; saw {sorted(names)}"
    )
    for row in rows:
        assert row.get("standfirst") == FAMILY_STANDFIRSTS.get(row.get("slug")), (
            f"each family carries its seeded standfirst: {row!r}"
        )
        assert isinstance(row.get("published_count"), int), (
            f"each family carries an integer published_count: {row!r}"
        )
        detail = api.get(f"/families/{row.get('slug')}").json()
        assert FAMILY_INTROS.get(row.get("slug")) == detail.get("intro"), (
            f"each family carries its seeded intro: {detail!r}"
        )


def test_family_detail_lists_only_its_published_products(api):
    """A family page lists the published products carrying it, and no draft."""
    r = api.get("/families/networking")
    assert r.status_code == 200, f"GET /api/families/networking should answer 200: {describe(r)}"
    body = r.json()
    assert body.get("intro"), f"a family carries an editorial intro: {body!r}"
    rows = body.get("products") or []
    slugs = slugs_of(rows)
    expected = {s for s in NETWORKING_SLUGS if s != DRAFT_SLUG}
    assert slugs == expected, (
        f"the Networking family carries the published products {sorted(expected)}; "
        f"saw {sorted(slugs)}"
    )
    assert DRAFT_SLUG not in slugs, (
        f"{DRAFT_SLUG!r} carries the Networking family but is in state draft, so it "
        f"must be absent; saw {sorted(slugs)}"
    )


def test_empty_family_answers_ok_rather_than_not_found(api, desk):
    """A family holding no published product answers 200 with an empty list."""
    slug = FAMILY_SLUGS[2]
    body = api.get(f"/families/{slug}").json()
    originals = [row for row in (body.get("products") or [])]
    assert originals, f"the {slug!r} family starts with published products: {body!r}"
    ids = []
    try:
        desk_rows = json_list(desk.get("/desk/products?state=published"),
                              "GET /api/desk/products?state=published")
        by_slug = {r.get("slug"): r for r in desk_rows}
        for row in originals:
            entry = by_slug.get(row.get("slug"))
            if entry:
                ids.append(product_id(entry))
                unpublish(desk, product_id(entry))
        settle()
        r = api.get(f"/families/{slug}")
        assert r.status_code == 200, (
            f"a family holding no published product still exists, so it answers 200 "
            f"rather than 404: {describe(r)}"
        )
        assert not (r.json().get("products") or []), (
            f"the emptied family should answer with no products: {r.json()!r}"
        )
    finally:
        for pid in ids:
            publish(desk, pid)
        settle()


def test_family_published_counts_reconcile_with_the_seed(api):
    """Each family's published count matches the seeded membership."""
    rows = json_list(api.get("/families"), "GET /api/families")
    for row in rows:
        slug = str(row.get("slug"))
        assert row.get("published_count") == FAMILY_COUNTS[slug], (
            f"the {slug!r} family holds {FAMILY_COUNTS[slug]} published products; "
            f"the response declared {row.get('published_count')!r}"
        )
        detail = api.get(f"/families/{slug}").json()
        assert len(detail.get("products") or []) == FAMILY_COUNTS[slug], (
            f"the {slug!r} family page lists {FAMILY_COUNTS[slug]} products; saw "
            f"{len(detail.get('products') or [])}"
        )


def test_the_product_rail_is_omitted_when_nothing_is_featured(desk, page):
    """The rail pads nothing where fewer are flagged and is omitted where none are."""
    origin = appclient.app_url()
    rows = json_list(desk.get("/desk/products?state=published"),
                     "GET /api/desk/products?state=published")
    by_slug = {r.get("slug"): r for r in rows}
    flagged = [by_slug[s] for s in FEATURED_SLUGS if s in by_slug]
    assert len(flagged) == len(FEATURED_SLUGS), (
        f"the seed flags {sorted(FEATURED_SLUGS)}; the desk list carries {sorted(by_slug)}"
    )
    try:
        for row in flagged:
            desk.patch(f"/desk/products/{product_id(row)}", json={"featured": False})
        settle()
        page.goto(f"{origin}/")
        assert RAIL_HEADING not in page.content(), (
            "where no product carries the flag the whole rail band is omitted rather than "
            "rendered empty; its heading is still on the home surface"
        )
        desk.patch(f"/desk/products/{product_id(flagged[0])}", json={"featured": True})
        settle()
        page.goto(f"{origin}/")
        assert RAIL_HEADING in page.content(), "one flagged product brings the rail back"
        assert DRAFT_NAME not in page.inner_text("main"), (
            "the rail never carries the draft product"
        )
    finally:
        for row in flagged:
            desk.patch(f"/desk/products/{product_id(row)}", json={"featured": True})
        settle()


def test_industries_response_returns_the_six_seeded_rows(api):
    """The six industries answer in sort order with a stat line and a customer."""
    rows = json_list(api.get("/industries"), "GET /api/industries")
    names = [str(r.get("name")) for r in rows]
    assert names == list(INDUSTRY_NAMES), (
        f"the six industries answer in the seeded order {list(INDUSTRY_NAMES)}; "
        f"saw {names}"
    )
    for row in rows:
        assert row.get("stat_line"), f"each industry carries a stat line: {row!r}"
        assert row.get("customer_name"), f"each industry carries a customer: {row!r}"


def test_customers_response_returns_the_eight_seeded_rows(api):
    """The eight proof-wall customers answer in sort order."""
    rows = json_list(api.get("/customers"), "GET /api/customers")
    names = [str(r.get("name")) for r in rows]
    assert names == list(CUSTOMER_NAMES), (
        f"the eight customers answer in the seeded order {list(CUSTOMER_NAMES)}; "
        f"saw {names}"
    )


def test_datasheet_library_lists_product_and_platform_sheets(api):
    """The library carries the platform sheets plus the sheets of published products."""
    rows = json_list(api.get("/datasheets"), "GET /api/datasheets")
    titles = names_of(rows, "title")
    missing = sorted(set(PLATFORM_DATASHEETS) - titles)
    assert not missing, (
        f"the library should carry every platform datasheet; missing {missing}, "
        f"saw {sorted(titles)}"
    )
    assert FLAGSHIP_DATASHEET_TITLE in titles, (
        f"the datasheet of a published product belongs in the library; "
        f"saw {sorted(titles)}"
    )
    assert DRAFT_DATASHEET_TITLE not in titles, (
        f"{DRAFT_DATASHEET_TITLE!r} belongs to the draft product, so the library must "
        f"not carry it; saw {sorted(titles)}"
    )
    platform = [r for r in rows if str(r.get("title")) in PLATFORM_DATASHEETS]
    for row in platform:
        assert not row.get("product_name"), (
            f"a platform datasheet belongs to no product: {row!r}"
        )
    for row in rows:
        assert isinstance(row.get("page_count"), int) and row["page_count"] > 0, (
            f"each datasheet reports its page count: {row!r}"
        )
        assert isinstance(row.get("byte_size"), int) and row["byte_size"] > 0, (
            f"each datasheet reports its byte size: {row!r}"
        )


def test_datasheet_byte_size_matches_the_stored_object(api, store):
    """A datasheet's reported byte size matches the object stored for it."""
    rows = json_list(api.get("/datasheets"), "GET /api/datasheets")
    checked = 0
    for row in rows:
        r = api.get(f"/media/datasheets/{row['id']}")
        assert r.status_code == 200, (
            f"a listed datasheet should stream: {describe(r)}"
        )
        assert len(r.content) == row["byte_size"], (
            f"{row.get('title')!r} reports {row['byte_size']} bytes but streamed "
            f"{len(r.content)}"
        )
        checked += 1
    assert checked, "the library carries at least one datasheet to compare"


def test_datasheet_download_carries_an_attachment_filename(api):
    """A datasheet download names a filename derived from its title."""
    rows = json_list(api.get("/datasheets"), "GET /api/datasheets")
    checked = 0
    for row in rows:
        title = str(row.get("title"))
        if title not in DATASHEET_FILENAMES:
            continue
        r = api.get(f"/media/datasheets/{row['id']}")
        assert r.status_code == 200, f"the datasheet should stream: {describe(r)}"
        disposition = r.headers.get("content-disposition", "")
        assert "attachment" in disposition.lower(), (
            f"a datasheet download carries a Content-Disposition of attachment; saw "
            f"{disposition!r}"
        )
        assert DATASHEET_FILENAMES[title] in disposition, (
            f"{title!r} downloads as {DATASHEET_FILENAMES[title]!r}; the header read "
            f"{disposition!r}"
        )
        checked += 1
    assert checked, (
        f"the library carries at least one of the pinned titles "
        f"{sorted(DATASHEET_FILENAMES)}"
    )


def test_art_response_pages_at_twenty_four(api):
    """The art gallery pages at twenty-four pieces and never carries a draft's art."""
    rows = json_list(api.get("/art"), "GET /api/art")
    assert len(rows) <= ART_PAGE_SIZE, (
        f"the gallery pages at {ART_PAGE_SIZE} pieces; the first page answered "
        f"{len(rows)}"
    )
    for row in rows:
        assert row.get("product_slug") != DRAFT_SLUG, (
            f"the gallery must not carry the art of the draft product: {row!r}"
        )
        assert row.get("alt_text"), (
            f"each art piece carries its alternative text: {row!r}"
        )
    narrowed = json_list(api.get("/art?family=databases"), "GET /api/art?family=databases")
    for row in narrowed:
        assert row.get("product_slug") in DATABASES_SLUGS, (
            f"the family filter narrows the gallery to that family; {row!r} is not in "
            f"{sorted(DATABASES_SLUGS)}"
        )


def test_published_art_bytes_stream_from_the_bucket(api, desk):
    """A published product's art streams through the app."""
    entry = create_draft(desk, name="Probe Streaming Engine")
    pid = product_id(entry)
    try:
        piece = add_art(desk, pid)
        assert publish(desk, pid).status_code in (200, 201), "the probe should publish"
        settle()
        r = api.get(f"/media/art/{piece['id']}")
        assert r.status_code == 200, (
            f"a published product's art should stream: {describe(r)}"
        )
        assert r.content, "the streamed art piece carries bytes"
    finally:
        unpublish(desk, pid)
        drop(desk, pid)


def test_generated_art_is_seeded_by_its_own_product(page):
    """Art is generated from the product, so the same product draws the same art."""
    origin = appclient.app_url()

    def art_of():
        page.goto(f"{origin}/product")
        return page.evaluate(
            "() => Array.from(document.images).map(i => ({src: i.currentSrc || i.src,"
            " w: i.getAttribute('width'), h: i.getAttribute('height'),"
            " ratio: getComputedStyle(i).aspectRatio,"
            " srcset: i.getAttribute('srcset') || '',"
            " loading: i.getAttribute('loading') || ''}))")

    first = art_of()
    assert first, "the product index draws art for each product"
    again = art_of()
    assert [a["src"] for a in first] == [a["src"] for a in again], (
        "the same product always produces the same art, so nothing reshuffles between "
        f"reads; saw {[a['src'] for a in first]} then {[a['src'] for a in again]}"
    )
    for piece in first:
        sized = (piece["w"] and piece["h"]) or (piece["ratio"] and piece["ratio"] != "auto")
        assert sized, (
            "a generated image declares its intrinsic width and height, or an aspect "
            f"ratio, so its box is reserved before it arrives; saw {piece!r}"
        )
        assert piece["srcset"], (
            f"a generated image is delivered with a candidate set; saw {piece!r}"
        )
    later = [p["loading"] for p in first[4:]]
    eager = [v for v in later if v != "lazy"]
    assert not eager, (
        f"every still below the first row loads lazily; saw {eager} past the first four"
    )
    inline = page.evaluate("() => document.querySelectorAll('svg').length")
    assert inline >= 1, (
        f"the product's marks are inline vector drawings rather than an icon font; the "
        f"page draws {inline} inline marks"
    )


def test_contact_submission_is_stored_and_read_by_an_administrator(api, admin):
    """A contact submission is stored and read back by an administrator, newest first."""
    token = os.urandom(4).hex()
    company = f"Probe Holdings {token}"
    r = api.post("/contact", json={
        "name": "Probe Buyer", "work_email": f"buyer-{token}@example.com",
        "company": company, "region": CONTACT_REGIONS[1], "interest": CONTACT_INTERESTS[0],
        "message": "A probe evaluation request.",
    })
    assert r.status_code in (200, 201), (
        f"a well-formed contact submission should be accepted: {describe(r)}"
    )
    assert r.json().get("enquiry_id"), f"the submission answers with an enquiry identifier: {r.json()!r}"

    def stored():
        rows = json_list(admin.get("/desk/enquiries"), "GET /api/desk/enquiries")
        return [row for row in rows if str(row.get("company")) == company]

    found = poll_until(stored, f"the submission from {company!r} reaches the administrator")
    assert found[0].get("region") == CONTACT_REGIONS[1], (
        f"the stored submission keeps its region: {found[0]!r}"
    )
    rows = json_list(admin.get("/desk/enquiries"), "GET /api/desk/enquiries")
    stamps = [str(row.get("received_at") or "") for row in rows]
    assert stamps == sorted(stamps, reverse=True), (
        f"the enquiries are listed newest first; saw {stamps[:4]}"
    )


def test_contact_refused_when_the_work_address_is_not_an_address(api):
    """A contact submission whose work address is malformed is refused."""
    r = api.post("/contact", json={
        "name": "Probe Buyer", "work_email": "notanaddress", "company": "Probe Ltd",
        "region": CONTACT_REGIONS[0], "interest": CONTACT_INTERESTS[0], "message": "A probe enquiry.",
    })
    assert r.status_code >= 400, (
        f"a malformed work address is refused: {describe(r)}"
    )
    short = api.post("/contact", json={
        "name": "x", "work_email": "probe-" + os.urandom(3).hex() + "@example.com",
        "company": "Probe Ltd",
        "region": CONTACT_REGIONS[0], "interest": CONTACT_INTERESTS[0], "message": "A probe enquiry.",
    })
    assert short.status_code >= 400, (
        f"a name shorter than two characters is refused: {describe(short)}"
    )


def test_contact_refused_when_the_message_runs_past_its_cap(api):
    """A contact message past the pinned cap is refused."""
    r = api.post("/contact", json={
        "name": "Probe Buyer", "work_email": "probe-" + os.urandom(3).hex() + "@example.com",
        "company": "Probe Ltd", "region": CONTACT_REGIONS[0], "interest": CONTACT_INTERESTS[0],
        "message": "y" * (CONTACT_MESSAGE_MAX + 1),
    })
    assert r.status_code >= 400, (
        f"a message longer than {CONTACT_MESSAGE_MAX} characters is refused: "
        f"{describe(r)}"
    )


def test_contact_refused_when_the_region_is_not_listed(api):
    """A contact submission naming an unlisted region or interest is refused."""
    base = {"name": "Probe Buyer", "work_email": "probe-" + os.urandom(3).hex() + "@example.com",
            "company": "Probe Ltd", "region": CONTACT_REGIONS[0],
            "interest": CONTACT_INTERESTS[0], "message": "A probe enquiry."}
    region = api.post("/contact", json=dict(base, region="Antarctica"))
    assert 400 <= region.status_code < 500, (
        f"a region outside {list(CONTACT_REGIONS)} is refused as invalid: {describe(region)}"
    )
    interest = api.post("/contact", json=dict(base, interest="Gossip"))
    assert 400 <= interest.status_code < 500, (
        f"an interest outside {list(CONTACT_INTERESTS)} is refused as invalid: {describe(interest)}"
    )


def test_assistant_counter_caps_at_five_hundred_characters(page):
    """The assistant field caps at the pinned character count."""
    origin = appclient.app_url()
    page.goto(f"{origin}/ask")
    assert f"0 of {ASSISTANT_CAP} characters entered" in page.content(), (
        f"the assistant counter reads '0 of {ASSISTANT_CAP} characters entered' on "
        f"arrival"
    )
    field = page.query_selector("textarea, input[type=text]")
    assert field, "the assistant surface carries a field to type into"
    field.fill("z" * (ASSISTANT_CAP + 50))
    entered = page.evaluate(
        "() => {const el = document.querySelector('textarea, input[type=text]');"
        " return el ? el.value.length : -1;}")
    assert entered == ASSISTANT_CAP, (
        f"the assistant field caps at {ASSISTANT_CAP} characters; it held {entered}"
    )


def test_desk_product_list_is_denied_without_a_token(anon):
    """The desk product list is closed to a request carrying no token."""
    r = anon.get("/desk/products")
    assert denied(r), (
        f"GET /api/desk/products with no bearer token should answer 401: {describe(r)}"
    )


def test_desk_publish_is_denied_without_a_token(anon, desk):
    """A publish is closed to a request carrying no token."""
    entry = create_draft(desk)
    pid = product_id(entry)
    try:
        r = anon.post(f"/desk/products/{pid}/publish")
        assert denied(r), (
            f"a publish with no bearer token should answer 401: {describe(r)}"
        )
        rows = json_list(desk.get("/desk/products?state=published"),
                         "GET /api/desk/products?state=published")
        assert str(entry.get("slug")) not in slugs_of(rows), (
            "the refused publish must not have published the product anyway"
        )
    finally:
        drop(desk, pid)


def test_desk_product_list_is_denied_with_a_malformed_token(anon):
    """A malformed bearer token answers 401 rather than being ignored."""
    r = anon.get("/desk/products", headers={"Authorization": "Bearer not-a-real-token"})
    assert denied(r), (
        f"a malformed bearer token should answer 401: {describe(r)}"
    )


def test_sign_in_failure_hides_whether_the_address_exists(anon):
    """A wrong password answers the same way as an unknown address."""
    known = anon.post("/auth/login", json={"email": EDITOR_EMAIL,
                                           "password": "not-the-password"})
    unknown = anon.post("/auth/login", json={"email": "no-such-" + os.urandom(3).hex() + "@example.com",
                                             "password": "not-the-password"})
    assert known.status_code == unknown.status_code, (
        f"a wrong password and an unknown address answer with the same status; saw "
        f"{known.status_code} against {unknown.status_code}"
    )
    assert known.status_code >= 400, (
        f"a wrong password is refused: {describe(known)}"
    )
    assert known.text.strip() == unknown.text.strip(), (
        f"the two refusals read identically, so neither discloses whether the address "
        f"exists; saw {known.text[:160]!r} against {unknown.text[:160]!r}"
    )


def test_a_signed_out_token_is_refused(anon):
    """A token is accepted before sign-out and refused after."""
    token = appclient.login(EDITOR_EMAIL, PASSWORD)
    with appclient.client(token) as session:
        before = session.get("/desk/products")
        assert before.status_code == 200, f"a fresh token reaches the desk: {describe(before)}"
        out = session.post("/auth/logout")
        assert out.status_code < 400, f"signing out should succeed: {describe(out)}"
        after = session.get("/desk/products")
        assert denied(after), (
            f"the ended session's token is refused afterwards: {describe(after)}"
        )


def test_an_editor_cannot_publish(editor, desk):
    """An editor's publish is denied on the server and leaves the product in draft."""
    entry = create_draft(editor, name="Probe Editor Publish")
    pid = product_id(entry)
    try:
        add_art(editor, pid)
        r = editor.post(f"/desk/products/{pid}/publish")
        assert denied(r), f"an editor's publish is denied as unauthorized: {describe(r)}"
        rows = json_list(desk.get("/desk/products?state=published"),
                         "GET /api/desk/products?state=published")
        assert str(entry.get("slug")) not in slugs_of(rows), (
            "the denied publish must leave the product in draft"
        )
    finally:
        drop(desk, pid)


def test_an_editor_cannot_return_a_product_to_draft(editor, desk):
    """An editor's return to draft is denied and leaves the product published."""
    entry = create_draft(desk, name="Probe Editor Unpublish")
    pid = product_id(entry)
    try:
        add_art(desk, pid)
        assert publish(desk, pid).status_code in (200, 201), "a publisher can publish the probe"
        r = editor.post(f"/desk/products/{pid}/unpublish")
        assert denied(r), f"an editor's return to draft is denied: {describe(r)}"
        rows = json_list(desk.get("/desk/products?state=published"),
                         "GET /api/desk/products?state=published")
        assert str(entry.get("slug")) in slugs_of(rows), (
            "the denied return to draft must leave the product published"
        )
    finally:
        unpublish(desk, pid)
        drop(desk, pid)


def test_only_an_administrator_reads_the_enquiries(editor, desk, admin):
    """An editor and a publisher are denied the enquiries; an administrator reads them."""
    assert denied(editor.get("/desk/enquiries")), "an editor is denied the enquiries"
    assert denied(desk.get("/desk/enquiries")), "a publisher is denied the enquiries"
    r = admin.get("/desk/enquiries")
    assert r.status_code == 200, f"an administrator reads the enquiries: {describe(r)}"


def test_only_an_administrator_reads_the_view_log(editor, desk, admin):
    """An editor and a publisher are denied the view log; an administrator reads it."""
    assert denied(editor.get("/desk/views")), "an editor is denied the view log"
    assert denied(desk.get("/desk/views")), "a publisher is denied the view log"
    r = admin.get("/desk/views")
    assert r.status_code == 200, f"an administrator reads the view log: {describe(r)}"


def test_enquiries_are_denied_to_an_anonymous_caller(anon):
    """The stored contact-sales submissions are closed without a token."""
    r = anon.get("/desk/enquiries")
    assert denied(r), (
        f"the stored enquiries is denied without a token: {describe(r)}"
    )


def test_view_log_is_denied_to_an_anonymous_caller(anon):
    """The page-view counts are closed without a token."""
    r = anon.get("/desk/views")
    assert denied(r), (
        f"the page-view counts is denied without a token: {describe(r)}"
    )


def test_desk_art_count_matches_the_objects_stored(desk, store):
    """Each desk row's art count matches the objects stored under that product."""
    rows = json_list(desk.get("/desk/products?state=all"),
                     "GET /api/desk/products?state=all")
    assert rows, "the desk list answers the seeded products"
    for row in rows:
        pid = str(row.get("id"))
        declared = row.get("art_count")
        assert isinstance(declared, int), (
            f"each desk row carries an integer art_count: {row!r}"
        )
        keys = store.list_keys(f"products/{pid}/art/")
        assert len(keys) == declared, (
            f"the art_count on {row.get('slug')!r} is {declared} but "
            f"{len(keys)} objects are stored under products/{pid}/art/"
        )


def test_seed_holds_the_eight_published_products_and_one_draft(desk, api):
    """The seed holds eight published products and exactly one draft."""
    published = json_list(desk.get("/desk/products?state=published"),
                          "GET /api/desk/products?state=published")
    drafts = json_list(desk.get("/desk/products?state=draft"),
                       "GET /api/desk/products?state=draft")
    assert slugs_of(published) == set(PUBLISHED_SLUGS), (
        f"the seed publishes {sorted(PUBLISHED_SLUGS)}; saw {sorted(slugs_of(published))}"
    )
    assert slugs_of(drafts) == {DRAFT_SLUG}, (
        f"the seed holds exactly one draft, {DRAFT_SLUG!r}; saw "
        f"{sorted(slugs_of(drafts))}"
    )
    draft_row = drafts[0]
    assert draft_row.get("art_count") == DRAFT_ART, (
        f"{DRAFT_NAME!r} is seeded with {DRAFT_ART} art pieces; saw "
        f"{draft_row.get('art_count')!r}"
    )
    public = slugs_of(json_list(api.get("/products"), "GET /api/products"))
    assert DRAFT_SLUG not in public, (
        f"the seeded draft must not reach the public index; saw {sorted(public)}"
    )


def test_published_product_fields_survive_a_reread(api, desk):
    """A published product answers with the same fields on a second read."""
    entry = create_draft(desk, summary="A probe summary that must survive a re-read.")
    pid = product_id(entry)
    try:
        add_art(desk, pid)
        assert publish(desk, pid).status_code in (200, 201), (
            "the probe product should publish so its fields can be re-read"
        )
        settle()
        first = api.get(f"/products/{entry['slug']}")
        assert first.status_code == 200, f"the probe product should read back: {describe(first)}"
        again = api.get(f"/products/{entry['slug']}")
        for field in ("slug", "name", "summary", "claim_body"):
            assert first.json().get(field) == again.json().get(field), (
                f"{field!r} should be identical across two reads; saw "
                f"{first.json().get(field)!r} then {again.json().get(field)!r}"
            )
    finally:
        unpublish(desk, pid)
        drop(desk, pid)


def test_a_created_product_always_lands_in_the_draft_state(desk):
    """A created product is draft whatever the request body claims."""
    payload = product_payload(state="published", name="Probe Forced State")
    r = desk.post("/desk/products", json=payload)
    assert r.status_code in (200, 201), f"the create should succeed: {describe(r)}"
    body = r.json()
    pid = product_id(body)
    try:
        assert str(body.get("state")) == "draft", (
            f"a created product lands in state draft even where the body asks for "
            f"published; saw {body.get('state')!r}"
        )
    finally:
        drop(desk, pid)


def test_publish_refused_when_a_required_field_is_empty(desk):
    """A publish is refused where a required field is empty, and a draft still saves."""
    entry = create_draft(desk)
    pid = product_id(entry)
    try:
        add_art(desk, pid)
        cleared = desk.patch(f"/desk/products/{pid}", json={"summary": ""})
        assert cleared.status_code in (200, 201), (
            f"a draft may be saved incomplete: {describe(cleared)}"
        )
        r = publish(desk, pid)
        assert r.status_code >= 400, (
            f"a publish with an empty summary is refused: {describe(r)}"
        )
    finally:
        drop(desk, pid)


def test_publish_refused_when_the_slug_is_already_taken(desk):
    """A publish naming a web address already held is refused."""
    entry = create_draft(desk, name="Probe Taken Address")
    pid = product_id(entry)
    try:
        add_art(desk, pid)
        desk.patch(f"/desk/products/{pid}", json={"slug": FLAGSHIP_SLUG})
        r = publish(desk, pid)
        assert r.status_code >= 400, (
            f"a publish naming the held address {FLAGSHIP_SLUG!r} is refused: "
            f"{describe(r)}"
        )
    finally:
        drop(desk, pid)


def test_publish_refused_when_the_slug_is_a_reserved_segment(desk):
    """A publish naming a reserved first path segment is refused."""
    entry = create_draft(desk, name="Probe Reserved Address")
    pid = product_id(entry)
    try:
        add_art(desk, pid)
        refused = []
        for segment in RESERVED_SEGMENTS:
            written = desk.patch(f"/desk/products/{pid}", json={"slug": segment})
            if written.status_code >= 400:
                refused.append(segment)
                continue
            r = publish(desk, pid)
            if r.status_code >= 400:
                refused.append(segment)
        assert set(refused) == set(RESERVED_SEGMENTS), (
            f"every reserved segment is refused, at the write or at the publish; "
            f"{sorted(set(RESERVED_SEGMENTS) - set(refused))} were accepted"
        )
    finally:
        drop(desk, pid)


def test_publish_refused_when_an_art_description_is_empty(desk):
    """A publish is refused where an art piece carries an empty description."""
    entry = create_draft(desk, name="Probe Undescribed Art")
    pid = product_id(entry)
    try:
        add_art(desk, pid, alt_text="")
        r = publish(desk, pid)
        assert r.status_code >= 400, (
            f"a publish with an art piece carrying no description is refused: "
            f"{describe(r)}"
        )
    finally:
        drop(desk, pid)


def test_publish_refused_when_the_product_carries_no_art(desk):
    """A publish is refused where the product carries no art piece at all."""
    entry = create_draft(desk, name="Probe Artless Engine")
    pid = product_id(entry)
    try:
        r = publish(desk, pid)
        assert r.status_code >= 400, (
            f"a publish of a product carrying no art piece is refused: {describe(r)}"
        )
    finally:
        drop(desk, pid)


def test_a_name_shorter_than_three_characters_is_refused(desk):
    """A product name shorter than the pinned floor is refused."""
    r = desk.post("/desk/products", json=product_payload(name="ab"))
    if r.status_code in (200, 201):
        pid = product_id(r.json())
        try:
            published = publish(desk, pid)
            assert published.status_code >= 400, (
                f"a name shorter than {NAME_MIN} characters is refused at the write or "
                f"at the publish: {describe(published)}"
            )
        finally:
            drop(desk, pid)
    else:
        assert r.status_code >= 400, f"the short name is refused: {describe(r)}"


def test_a_summary_over_two_hundred_forty_characters_is_refused(desk):
    """A summary past the pinned cap is refused."""
    long_summary = "x" * (SUMMARY_MAX + 1)
    r = desk.post("/desk/products", json=product_payload(summary=long_summary))
    if r.status_code in (200, 201):
        pid = product_id(r.json())
        try:
            published = publish(desk, pid)
            assert published.status_code >= 400, (
                f"a summary longer than {SUMMARY_MAX} characters is refused at the "
                f"write or at the publish: {describe(published)}"
            )
        finally:
            drop(desk, pid)
    else:
        assert r.status_code >= 400, f"the long summary is refused: {describe(r)}"


def test_publish_then_unpublish_leaves_a_single_product_row(desk):
    """A publish followed by an unpublish leaves one row, not two."""
    entry = create_draft(desk)
    pid = product_id(entry)
    try:
        add_art(desk, pid)
        assert publish(desk, pid).status_code in (200, 201), "the probe should publish"
        assert unpublish(desk, pid).status_code in (200, 201), "the probe should unpublish"
        rows = json_list(desk.get("/desk/products?state=all"),
                         "GET /api/desk/products?state=all")
        matching = [r for r in rows if str(r.get("slug")) == str(entry.get("slug"))]
        assert len(matching) == 1, (
            f"a publish then an unpublish leaves one row for {entry.get('slug')!r}; "
            f"saw {len(matching)}"
        )
        assert str(matching[0].get("state")) == "draft", (
            f"the row is back in state draft; saw {matching[0].get('state')!r}"
        )
    finally:
        drop(desk, pid)


def test_two_concurrent_publishes_of_one_slug_admit_one_winner(desk):
    """Two publishes naming one web address admit exactly one winner."""
    import concurrent.futures as cf

    slug = f"probe-contended-{os.urandom(3).hex()}"
    first = create_draft(desk, slug=slug, name="Probe Contended One")
    second = create_draft(desk, slug=f"{slug}-b", name="Probe Contended Two")
    a, b = product_id(first), product_id(second)
    try:
        add_art(desk, a)
        add_art(desk, b)
        desk.patch(f"/desk/products/{b}", json={"slug": slug})
        with cf.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda pid: publish(desk, pid), (a, b)))
        ok = [r for r in results if r.status_code in (200, 201)]
        assert len(ok) == 1, (
            f"exactly one of two concurrent publishes of {slug!r} may win; "
            f"{len(ok)} succeeded: {[r.status_code for r in results]}"
        )
        rows = json_list(desk.get("/desk/products?state=published"),
                         "GET /api/desk/products?state=published")
        holders = [r for r in rows if str(r.get("slug")) == slug]
        assert len(holders) == 1, (
            f"one product holds {slug!r} at any time; saw {len(holders)}"
        )
    finally:
        for pid in (a, b):
            unpublish(desk, pid)
            drop(desk, pid)


def test_saving_one_product_twice_creates_no_second_product(desk):
    """Saving one product twice updates the row rather than adding another."""
    entry = create_draft(desk, name="Probe Idempotent Engine")
    pid = product_id(entry)
    try:
        r = desk.patch(f"/desk/products/{pid}",
                       json={"summary": "A probe summary saved a second time."})
        assert r.status_code in (200, 201), f"the second save should succeed: {describe(r)}"
        rows = json_list(desk.get("/desk/products?state=all"),
                         "GET /api/desk/products?state=all")
        matching = [x for x in rows if str(x.get("slug")) == str(entry.get("slug"))]
        assert len(matching) == 1, (
            f"saving twice creates no second product; saw {len(matching)} rows for "
            f"{entry.get('slug')!r}"
        )
    finally:
        drop(desk, pid)


def test_uploaded_art_object_exists_in_the_bucket(desk, store):
    """An uploaded art piece exists in the bucket at the key the app registered."""
    entry = create_draft(desk, name="Probe Upload Engine")
    pid = product_id(entry)
    try:
        piece = add_art(desk, pid)
        key = piece["object_key"]
        keys = store.list_keys(f"products/{pid}/art/")
        assert key in keys, (
            f"the registered object key {key!r} should exist in the bucket; saw {keys}"
        )
    finally:
        drop(desk, pid)


def test_uploaded_object_key_follows_the_art_scheme(desk):
    """An art object key carries the digest of its own bytes."""
    entry = create_draft(desk, name="Probe Key Scheme Engine")
    pid = product_id(entry)
    try:
        piece = add_art(desk, pid)
        key = piece["object_key"]
        pattern = rf"^products/{re.escape(pid)}/art/[0-9a-f]{{64}}\.[a-z0-9]+$"
        assert re.match(pattern, key), (
            f"the art key should read products/<product_id>/art/"
            f"<sha256_of_bytes>.<ext> with 64 lowercase hex characters; saw {key!r}"
        )
    finally:
        drop(desk, pid)


def test_the_desk_message_stack_holds_at_most_three(page):
    """Four quick saves leave at most three messages standing; the public side raises none."""
    origin = appclient.app_url()
    page.goto(f"{origin}/")
    assert not page.query_selector("[role=status], [role=alert]"), (
        "nothing on the public side raises a desk message"
    )
    page.goto(f"{origin}/desk/login")
    page.get_by_label("Email").fill(PUBLISHER_EMAIL)
    page.get_by_label("Password").fill(PASSWORD)
    page.get_by_role("button", name="Sign in").click()
    page.wait_for_url("**/desk**", timeout=10000)
    page.goto(f"{origin}/desk/product/new")
    page.get_by_label("Product name").fill("Probe Stack " + os.urandom(2).hex())
    save = page.get_by_role("button", name="Save draft")
    for _ in range(4):
        save.click()
    settle()
    standing = page.evaluate(
        "() => document.querySelectorAll('[role=status], [role=alert]').length")
    assert 1 <= standing <= MESSAGE_STACK_MAX, (
        f"the desk message stack holds at most {MESSAGE_STACK_MAX}; four saves left "
        f"{standing} standing"
    )


def test_health_route_answers_ready(api):
    """The readiness route answers 200 once the app has its services."""
    r = api.get("/health")
    assert r.status_code == 200, f"GET /api/health should answer 200: {describe(r)}"


def test_privacy_page_is_served_and_linked_from_the_footer(page):
    """The privacy page is served and reachable from the footer."""
    origin = appclient.app_url()
    page.goto(f"{origin}/privacy")
    assert "What we record" in page.content(), (
        "the privacy page carries the heading 'What we record'"
    )
    page.goto(f"{origin}/")
    hrefs = page.evaluate(
        "() => Array.from(document.querySelectorAll('footer a')).map(a => a.getAttribute('href'))")
    assert any(h and h.rstrip('/').endswith('/privacy') for h in hrefs), (
        f"the footer reaches the privacy page; saw {hrefs}"
    )


def test_terms_page_is_served_and_linked_from_the_footer(page):
    """The site terms are served and reachable from the footer."""
    origin = appclient.app_url()
    page.goto(f"{origin}/terms")
    assert "Using the platform" in page.content(), (
        "the site terms carry the heading 'Using the platform'"
    )
    page.goto(f"{origin}/")
    hrefs = page.evaluate(
        "() => Array.from(document.querySelectorAll('footer a')).map(a => a.getAttribute('href'))")
    assert any(h and h.rstrip('/').endswith('/terms') for h in hrefs), (
        f"the footer reaches the site terms; saw {hrefs}"
    )


def test_unknown_path_renders_the_platform_not_found_surface(page):
    """An unmatched path answers 404 inside the platform's own chrome."""
    origin = appclient.app_url()
    page.goto(f"{origin}/nothing-here")
    text = page.content()
    assert "We cannot find that page" in text, (
        "an unmatched path renders the platform's own not-found surface"
    )
    shell = page.evaluate(
        "() => ({header: !!document.querySelector('header'),"
        " footer: !!document.querySelector('footer')})")
    assert shell["header"] and shell["footer"], (
        f"the not-found surface keeps the global header and footer: {shell!r}"
    )
    heads = page.evaluate("() => document.querySelectorAll('h1').length")
    assert heads == 1, f"each route carries one h1; the not-found surface carries {heads}"


def test_internal_links_on_public_surfaces_all_resolve(page):
    """Every internal destination a public surface names resolves."""
    origin = appclient.app_url()
    broken = []
    seen = set()
    for route in PUBLIC_ROUTES:
        page.goto(f"{origin}{route}")
        marks = page.evaluate(
            "() => ({banner: document.querySelectorAll('header, [role=banner]').length,"
            " main: document.querySelectorAll('main, [role=main]').length,"
            " info: document.querySelectorAll('footer, [role=contentinfo]').length,"
            " canonical: (document.querySelector('link[rel=canonical]') || {}).href || ''})")
        assert marks["main"] == 1, (
            f"{route} carries exactly one main landmark; saw {marks!r}"
        )
        assert marks["banner"] >= 1 and marks["info"] >= 1, (
            f"{route} carries a banner and a contentinfo landmark; saw {marks!r}"
        )
        assert marks["canonical"], (
            f"{route} carries a canonical link to its own address; saw {marks!r}"
        )
        hrefs = page.evaluate(
            "() => Array.from(document.querySelectorAll('a[href]'))"
            ".map(a => a.getAttribute('href'))")
        for h in hrefs:
            if not h or h.startswith(("http", "mailto:", "tel:", "#")):
                continue
            if h in seen:
                continue
            seen.add(h)
            r = page.request.get(f"{origin}{h}" if h.startswith("/") else h)
            if r.status >= 400:
                broken.append((route, h, r.status))
    assert not broken, f"every internal link resolves; saw {broken}"


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


def test_product_title_uses_the_display_type_family(page):
    """A product title is set in the display family named in the brief."""
    origin = appclient.app_url()
    page.goto(f"{origin}/product/tessera")
    families = page.evaluate(
        "() => {const el = document.querySelector('h1'); "
        "return el ? getComputedStyle(el).fontFamily : null;}")
    assert families, "the product route carries a first-level heading"
    first = families.split(",")[0].strip().strip('"\'')
    assert first == DISPLAY_FAMILY, (
        f"a product title is set in {DISPLAY_FAMILY!r}; the computed stack begins "
        f"{first!r} ({families!r})"
    )


def test_body_copy_uses_the_body_type_family(page):
    """Navigation labels, controls and metadata lines take the body family."""
    origin = appclient.app_url()
    page.goto(f"{origin}/product")
    families = page.evaluate(
        "() => {const out = {};"
        "const nav = document.querySelector('header a, nav a');"
        "if (nav) out.nav = getComputedStyle(nav).fontFamily;"
        "const ctl = document.querySelector('header input, main input, main select');"
        "if (ctl) out.control = getComputedStyle(ctl).fontFamily;"
        "const body = document.querySelector('main p');"
        "if (body) out.body = getComputedStyle(body).fontFamily;"
        "return out;}")
    assert families.get("nav"), "the product index carries a navigation label"
    for where, stack in families.items():
        first = stack.split(",")[0].strip().strip('"\'')
        assert first == BODY_FAMILY, (
            f"the {where} is set in {BODY_FAMILY!r}; the computed stack begins "
            f"{first!r} ({stack!r})"
        )


def test_type_steps_render_at_their_pinned_sizes(page):
    """Every rendered text size is one of the pinned steps, the headings at theirs."""
    origin = appclient.app_url()
    for route in ("/", "/product/tessera", "/ask"):
        page.goto(f"{origin}{route}")
        sizes = page.evaluate(
            "() => Array.from(document.querySelectorAll('main *')).filter(e =>"
            " e.childNodes.length && Array.from(e.childNodes).some(n => n.nodeType === 3 &&"
            " n.textContent.trim())).map(e => getComputedStyle(e).fontSize)")
        stray = sorted(set(sizes) - ALLOWED_FONT_SIZES)
        assert not stray, (
            f"the eleven type steps are the whole typography; {route} renders the "
            f"unpinned sizes {stray}"
        )
    page.goto(f"{origin}/product/tessera")
    h1 = page.evaluate(
        "() => {const s = getComputedStyle(document.querySelector('h1'));"
        " return [s.fontSize, s.lineHeight];}")
    assert tuple(h1) == TYPE_STEPS["display"], (
        f"a product heading sits at the display step {TYPE_STEPS['display']}; saw {h1}"
    )
    page.goto(f"{origin}/ask")
    greeting = page.evaluate(
        "() => {const e = Array.from(document.querySelectorAll('h1,h2,p')).find(x =>"
        " x.textContent.trim() === 'Hello, how can I help?');"
        " if (!e) return null; const s = getComputedStyle(e); return [s.fontSize, s.lineHeight];}")
    assert greeting and tuple(greeting) == TYPE_STEPS["heading"], (
        f"the assistant greeting sits at the heading step {TYPE_STEPS['heading']}; saw {greeting}"
    )


def test_headings_descend_without_skipping_a_level(page):
    """Each route carries one h1 and headings never skip a level."""
    origin = appclient.app_url()
    for route in PUBLIC_ROUTES:
        page.goto(f"{origin}{route}")
        levels = page.evaluate(
            "() => Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6'))"
            ".map(h => Number(h.tagName[1]))")
        assert levels.count(1) == 1, (
            f"{route} carries exactly one h1; saw {levels.count(1)}"
        )
        for before, after in zip(levels, levels[1:]):
            assert after <= before + 1, (
                f"headings on {route} descend without skipping a level; saw h{before} "
                f"followed by h{after} in {levels}"
            )
        navs = page.evaluate("() => document.querySelectorAll('nav, [role=navigation]').length")
        assert navs >= 1, f"{route} carries a navigation landmark"


def test_skip_link_is_the_first_focusable_element(page):
    """The first Tab lands on a skip link that reaches the main landmark."""
    origin = appclient.app_url()
    page.goto(f"{origin}/")
    page.keyboard.press("Tab")
    first = page.evaluate(
        "() => {const el = document.activeElement;"
        " return el ? {tag: el.tagName, text: (el.textContent || '').trim(),"
        "  href: el.getAttribute('href') || '',"
        "  ring: getComputedStyle(el).outlineStyle} : null;}")
    assert first, "a first Tab lands on a focusable element"
    assert first["tag"] == "A" and first["href"].startswith("#"), (
        f"the first focusable element is a skip link into the page; saw {first!r}"
    )
    assert first["ring"] != "none", (
        f"the focus ring is restyled rather than removed; the skip link computed "
        f"outline-style {first['ring']!r}"
    )


def test_navigation_targets_are_comfortably_sized(page):
    """Every navigation target meets the pinned minimum on its shorter side."""
    origin = appclient.app_url()
    page.set_viewport_size(NARROW_VIEWPORT)
    page.goto(f"{origin}/")
    small = page.evaluate(
        "(min) => Array.from(document.querySelectorAll('header a, header button,"
        " nav a, nav button, footer a'))"
        ".map(el => ({t: (el.textContent || '').trim().slice(0, 24),"
        "  w: el.getBoundingClientRect().width, h: el.getBoundingClientRect().height}))"
        ".filter(b => b.w > 0 && b.h > 0 && Math.min(b.w, b.h) < min)",
        TOUCH_TARGET_MIN)
    assert not small, (
        f"a navigation target is at least {TOUCH_TARGET_MIN} by {TOUCH_TARGET_MIN} on "
        f"its shorter side; saw {small}"
    )


def test_no_font_or_icon_asset_ships_with_the_build(page):
    """The build ships no font file, no icon font and no lossless photographic still."""
    origin = appclient.app_url()
    seen = []
    page.on("response", lambda r: seen.append((r.url, r.headers.get("content-type", ""))))
    page.goto(f"{origin}/")
    page.goto(f"{origin}/gallery")
    own = [(u, c) for u, c in seen if u.startswith(origin)]
    fonts = [u for u, c in own
             if "font" in c or u.rsplit("?", 1)[0].endswith((".woff", ".woff2", ".ttf",
                                                             ".otf", ".eot"))]
    assert not fonts, (
        f"the build names its families and ships no font file; it served {fonts}"
    )
    binaries = [u for u, c in own
                if u.rsplit("?", 1)[0].endswith((".png", ".jpg", ".jpeg", ".bmp",
                                                 ".tiff", ".mp4", ".webm", ".gif"))]
    assert not binaries, (
        f"the build ships no binary asset; it served {binaries}"
    )
    third_party = sorted({u.split("/")[2] for u, _ in seen
                          if not u.startswith(origin) and u.startswith("http")})
    assert all("font" in host or "gstatic" in host for host in third_party), (
        "the one third-party request the product makes at run time is the font "
        f"service; it also reached {third_party}"
    )


def test_home_surface_stays_inside_its_delivery_budget(page):
    """The home surface holds its script weight and its blocking request count."""
    origin = appclient.app_url()
    sizes = []
    page.on("response", lambda r: sizes.append(
        (r.url, r.headers.get("content-type", ""), r.headers.get("content-length", "0"))))
    page.goto(f"{origin}/")
    script_bytes = sum(int(n or 0) for u, c, n in sizes
                       if u.startswith(origin) and ("javascript" in c or u.endswith(".js")))
    assert script_bytes <= SCRIPT_BUDGET_BYTES, (
        f"the compressed JavaScript the home surface delivers stays under "
        f"{SCRIPT_BUDGET_BYTES} bytes; it delivered {script_bytes}"
    )
    blocking = page.evaluate(
        "() => {const head = document.head;"
        "const css = Array.from(head.querySelectorAll('link[rel=stylesheet]'))"
        ".filter(l => !l.media || l.media === 'all' || l.media === 'screen');"
        "const js = Array.from(head.querySelectorAll('script[src]'))"
        ".filter(s => !s.defer && !s.async && s.type !== 'module');"
        "return css.length + js.length;}")
    assert blocking <= BLOCKING_REQUEST_MAX, (
        f"no more than {BLOCKING_REQUEST_MAX} requests block first paint on the home "
        f"surface; the head carries {blocking}"
    )


def test_five_named_breakpoints_drive_the_pinned_column_counts(page):
    """The five tiers are named, and each card row folds to one column when narrow."""
    origin = appclient.app_url()
    page.goto(f"{origin}/")
    sheets = page.evaluate(
        "() => Array.from(document.styleSheets).map(s => {try {return Array.from("
        "s.cssRules).map(r => r.cssText).join(' ');} catch (e) {return '';}}).join(' ')")
    haystack = sheets + " " + page.content()
    for tier in TIERS:
        assert re.search(rf"(?<![A-Za-z0-9]){tier}(?![A-Za-z0-9])", haystack), (
            f"the product names its five breakpoints {TIERS}; {tier!r} appears as a "
            f"name in neither the stylesheet nor the markup"
        )
    rows = {"/product": 3, "/family": 3, "/datasheet": 4, "/gallery": 4, "/solution": 3}
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
            f"{route} runs up to {widest} cards across at its widest tier and more "
            f"than one above the narrowest; at {WIDE_VIEWPORT['width']}px it shows {wide}"
        )


def test_shape_and_spacing_follow_the_product_rhythm(page):
    """Radii follow the product family, spacing sits on the eight-step rhythm, the header holds."""
    origin = appclient.app_url()
    heights = set()
    for route in ("/", "/product", "/datasheet"):
        page.goto(f"{origin}{route}")
        shape = page.evaluate(
            "(step) => {"
            " const px = v => parseFloat(v) || 0;"
            " const cards = Array.from(document.querySelectorAll('main article, main [class*=card]'));"
            " const card = cards[0] ? getComputedStyle(cards[0]) : null;"
            " const btn = document.querySelector('main button, main a[class*=button]');"
            " const b = btn ? getComputedStyle(btn) : null;"
            " const offRhythm = cards.slice(0, 6).map(c => getComputedStyle(c).paddingTop)"
            "   .filter(v => px(v) % step !== 0);"
            " return {cardRadius: card ? px(card.borderTopLeftRadius) : null,"
            "   cardShadow: card ? card.boxShadow : null,"
            "   buttonRadius: b ? px(b.borderTopLeftRadius) : null, offRhythm,"
            "   header: document.querySelector('header').getBoundingClientRect().height};}",
            RHYTHM_STEP)
        heights.add(round(shape["header"]))
        if shape["cardRadius"] is not None and shape["buttonRadius"] is not None:
            assert shape["cardRadius"] >= shape["buttonRadius"] or shape["buttonRadius"] > 100, (
                f"cards on {route} take the softer product radius, buttons a tighter one or a "
                f"full pill; saw card {shape['cardRadius']} against button {shape['buttonRadius']}"
            )
        if shape["cardShadow"] is not None:
            assert shape["cardShadow"] in ("none", ""), (
                f"a resting card on {route} draws no shadow; saw {shape['cardShadow']!r}"
            )
        assert not shape["offRhythm"], (
            f"card padding on {route} sits on the {RHYTHM_STEP}-step rhythm; saw {shape['offRhythm']}"
        )
    assert len(heights) == 1, (
        f"the fixed header holds one constant height across routes; saw {sorted(heights)}"
    )


def test_only_the_skeleton_animates_indefinitely(page):
    """Only the skeleton shimmer loops; the brand gradient turns once and holds."""
    origin = appclient.app_url()
    page.goto(f"{origin}/")
    settle()
    anims = page.evaluate(
        "() => document.getAnimations().map(a => ({"
        " iterations: a.effect && a.effect.getTiming ? a.effect.getTiming().iterations : 1,"
        " target: a.effect && a.effect.target ? (a.effect.target.className || '').toString() : '',"
        " scroll: !!(a.timeline && a.timeline.constructor &&"
        "   /Scroll|View/.test(a.timeline.constructor.name))}))")
    looping = [a for a in anims if a["iterations"] == float("inf") or a["iterations"] == "Infinity"
               or (isinstance(a["iterations"], (int, float)) and a["iterations"] > 1e6)]
    stray = [a for a in looping if "skeleton" not in a["target"].lower()]
    assert not stray, (
        f"the skeleton shimmer is the one animation that loops; these also loop: {stray}"
    )
    scrubbed = [a for a in anims if a["scroll"]]
    assert not scrubbed, f"nothing is scroll-scrubbed; saw {scrubbed}"
    styles = page.evaluate(
        "() => { const e = new Set(), n = new Set();"
        " for (const el of document.querySelectorAll('*')) { const c = getComputedStyle(el);"
        "  for (const t of (c.transitionTimingFunction + ',' + c.animationTimingFunction).split(/,(?![^(]*\\))/))"
        "   { const v = t.trim(); if (v.startsWith('cubic-bezier')) e.add(v); }"
        "  if (c.animationName && c.animationName !== 'none')"
        "   c.animationName.split(',').forEach(x => n.add(x.trim())); }"
        " return {easings: Array.from(e), names: Array.from(n)}; }")
    assert len(styles["easings"]) <= 5, (
        f"five easing characters carry the whole product; saw {styles['easings']}"
    )
    assert len(styles["names"]) <= 6, (
        f"the product runs six named keyframes and no more; saw {styles['names']}"
    )
    page.emulate_media(reduced_motion="reduce")
    page.goto(f"{origin}/")
    settle()
    moving = page.evaluate(
        "() => document.getAnimations().filter(a => a.effect && a.effect.getKeyframes &&"
        " a.effect.getKeyframes().some(k => 'transform' in k || 'translate' in k || 'rotate' in k))"
        ".map(a => (a.effect.target && a.effect.target.className || '').toString())")
    assert not moving, (
        f"a request for reduced motion stops sliding and rotation everywhere; still moving: {moving}"
    )
    gradient = [a for a in anims if "gradient" in a["target"].lower()]
    for a in gradient:
        assert a["iterations"] == 1, (
            f"the brand gradient turns a half-turn once on load and holds; it runs "
            f"{a['iterations']} times"
        )


def test_the_copy_deck_renders_its_exact_strings(page):
    """Every exact string in the copy deck renders on the surface that owns it."""
    origin = appclient.app_url()
    missing = []
    for route, strings in COPY_STRINGS.items():
        page.goto(f"{origin}{route}")
        text = page.evaluate("() => document.body.innerText")
        for s in strings:
            if s not in text:
                missing.append((route, s))
    page.goto(f"{origin}/privacy")
    privacy = page.inner_text("main").lower()
    for phrase in ("page view", "contact", "cookie"):
        if phrase not in privacy:
            missing.append(("/privacy", phrase))
    assert not missing, f"every copy string renders exactly on its surface; missing {missing}"


def test_every_route_declares_its_page_type_shell(page):
    """Every route declares its shell as a page-type attribute from the four named ones."""
    origin = appclient.app_url()
    wrong = []
    for route, shell in PAGE_TYPES.items():
        page.goto(f"{origin}{route}")
        declared = page.evaluate(
            "() => { const e = document.querySelector('[data-page-type]');"
            " return e ? e.getAttribute('data-page-type') : null; }")
        if declared != shell:
            wrong.append((route, shell, declared))
    assert not wrong, (
        f"each route declares its page-type attribute; expected shell and saw: {wrong}"
    )
    crumbless = []
    for route, shell in PAGE_TYPES.items():
        if shell != "index":
            continue
        page.goto(f"{origin}{route}")
        if not page.query_selector("nav[aria-label*=readcrumb], [aria-label*=readcrumb] a"):
            crumbless.append(route)
    assert not crumbless, f"every index surface carries a breadcrumb; missing on {crumbless}"


def test_a_desk_session_reads_a_draft_art_piece(desk):
    """A request carrying a desk bearer token is served a draft product's art bytes."""
    drafts = json_list(desk.get("/desk/products?state=draft"),
                       "GET /api/desk/products?state=draft")
    halyard = [d for d in drafts if d.get("slug") == DRAFT_SLUG]
    assert halyard, f"the seeded draft {DRAFT_SLUG!r} is listed at the desk"
    detail = desk.get(f"/desk/products/{halyard[0]['id']}").json()
    pieces = detail.get("art") or []
    assert len(pieces) == DRAFT_ART, f"the draft carries {DRAFT_ART} art pieces: {detail!r}"
    r = desk.get(f"/media/art/{pieces[0]['id']}")
    assert r.status_code == 200 and r.content, (
        f"a desk session reads a draft's art so the composer can show it: {describe(r)}"
    )


def test_a_read_missing_its_bound_or_timestamp_is_refused(api):
    """A bounded read with no valid bound and an exact read with no timestamp are refused."""
    key = f"probe-{os.urandom(4).hex()}"
    api.post("/console/write", json={"region": REGIONS[0], "key": key,
                                     "value": CONSOLE_VALUE})
    probes = (
        {"region": REGIONS[1], "key": key, "mode": "bounded"},
        {"region": REGIONS[1], "key": key, "mode": "bounded", "bound": 0},
        {"region": REGIONS[1], "key": key, "mode": "bounded", "bound": "soon"},
        {"region": REGIONS[1], "key": key, "mode": "exact"},
    )
    for body in probes:
        r = api.post("/console/read", json=body)
        assert 400 <= r.status_code < 500, (
            f"a read missing or malforming its bound or timestamp is refused as invalid; "
            f"{body!r} answered {describe(r)}"
        )
        named = "bound" if body["mode"] == "bounded" else "timestamp"
        assert named in r.text.lower(), (
            f"the refusal names the field {named!r}: {describe(r)}"
        )


def test_a_write_missing_its_value_is_refused(api):
    """A console write with no key or no value is refused and names the field."""
    for body, named in (({"region": REGIONS[0], "key": "k"}, "value"),
                        ({"region": REGIONS[0], "value": CONSOLE_VALUE}, "key")):
        r = api.post("/console/write", json=body)
        assert 400 <= r.status_code < 500, (
            f"a write missing its {named} is refused as invalid: {describe(r)}"
        )
        assert named in r.text.lower(), f"the refusal names {named!r}: {describe(r)}"


def test_console_timestamps_carry_utc_milliseconds(api):
    """Console timestamps are ISO 8601 UTC strings; staleness and latency are whole milliseconds."""
    key = f"probe-{os.urandom(4).hex()}"
    w = api.post("/console/write", json={"region": REGIONS[0], "key": key,
                                         "value": CONSOLE_VALUE})
    assert w.status_code in (200, 201), f"the write commits: {describe(w)}"
    assert re.match(CONSOLE_TIMESTAMP, str(w.json().get("commit_timestamp"))), (
        f"a commit timestamp is ISO 8601 UTC with milliseconds: {w.json()!r}"
    )
    r = api.post("/console/read", json={"region": REGIONS[1], "key": key, "mode": "strong"})
    body = r.json()
    assert re.match(CONSOLE_TIMESTAMP, str(body.get("timestamp"))), (
        f"a read timestamp is ISO 8601 UTC with milliseconds: {body!r}"
    )
    assert body.get("staleness") == 0, f"a strong read reports a staleness of 0: {body!r}"
    assert isinstance(body.get("latency_ms"), int), (
        f"the latency figure is a whole number of milliseconds: {body!r}"
    )


def test_severing_a_severed_region_changes_nothing(api):
    """Severing a region twice leaves one severed region and answers all five."""
    try:
        first = api.post("/console/partition", json={"region": REGIONS[2], "severed": True})
        again = api.post("/console/partition", json={"region": REGIONS[2], "severed": True})
        assert first.status_code == 200 and again.status_code == 200, (
            f"severing an already severed region is accepted: {describe(again)}"
        )
        regions = again.json().get("regions") or []
        assert len(regions) == len(REGIONS), f"all five regions answer: {again.json()!r}"
        severed = [row.get("region") for row in regions if row.get("severed")]
        assert severed == [REGIONS[2]], f"only {REGIONS[2]!r} stays severed; saw {severed}"
        reset = api.post("/console/reset")
        calm = api.post("/console/reset")
        assert reset.json() == calm.json(), (
            f"a reset with nothing severed answers the same seeded state: {calm.json()!r}"
        )
    finally:
        api.post("/console/reset")


def test_an_unknown_sort_is_refused_and_an_unknown_family_answers_empty(api):
    """A sort outside name and recent is refused; a family slug naming nothing answers empty."""
    r = api.get("/products?sort=price")
    assert 400 <= r.status_code < 500, f"an unknown sort is refused as invalid: {describe(r)}"
    rows = json_list(api.get("/products?family=no-such-family"),
                     "GET /api/products?family=no-such-family")
    assert rows == [], f"an unknown family slug answers an empty array; saw {len(rows)} rows"
    art = json_list(api.get("/art?family=no-such-family"), "GET /api/art?family=no-such-family")
    assert art == [], f"the gallery answers empty for an unknown family; saw {len(art)} rows"


def test_an_art_page_past_the_last_answers_empty(api):
    """A gallery page past the last answers an empty array; a page below one is refused."""
    rows = json_list(api.get("/art?page=999"), "GET /api/art?page=999")
    assert rows == [], f"a page past the last answers empty; saw {len(rows)} rows"
    r = api.get("/art?page=0")
    assert 400 <= r.status_code < 500, f"a page below 1 is refused as invalid: {describe(r)}"


def test_an_empty_name_saves_as_an_incomplete_draft(desk):
    """An empty product name saves; a two-character one is refused at save."""
    r = desk.post("/desk/products", json=product_payload(name="", slug=""))
    assert r.status_code in (200, 201), f"an empty name saves as an incomplete draft: {describe(r)}"
    pid = product_id(r.json())
    try:
        assert publish(desk, pid).status_code >= 400, "the incomplete draft is refused at publish"
    finally:
        drop(desk, pid)
    short = desk.post("/desk/products", json=product_payload(name="ab"))
    assert 400 <= short.status_code < 500, (
        f"a name of two characters is refused at save: {describe(short)}"
    )


def test_a_registered_datasheet_reads_its_page_count(desk):
    """A datasheet registered after upload reports the page count of the stored document."""
    entry = create_draft(desk, name="Probe Sheet Engine")
    pid = product_id(entry)
    try:
        target = desk.post("/desk/uploads", json={
            "product_id": pid, "kind": "datasheet",
            "filename": "probe-sheet.pdf", "content_type": "application/pdf"})
        assert target.status_code in (200, 201), f"a datasheet target is issued: {describe(target)}"
        issued = target.json()
        put_upload(issued, probe_pdf(PROBE_PDF_PAGES))
        r = desk.post("/desk/datasheets", json={
            "product_id": pid, "object_key": issued["object_key"], "title": "Probe Sheet"})
        assert r.status_code in (200, 201), f"the datasheet registers: {describe(r)}"
        assert r.json().get("page_count") == PROBE_PDF_PAGES, (
            f"the page count is read from the stored document: {r.json()!r}"
        )
        ghost = desk.post("/desk/datasheets", json={
            "product_id": pid, "object_key": f"products/{pid}/datasheet/none.pdf",
            "title": "Ghost Sheet"})
        assert 400 <= ghost.status_code < 500, (
            f"a key the bucket does not hold is refused as invalid: {describe(ghost)}"
        )
    finally:
        drop(desk, pid)


def test_seeded_flagship_art_carries_its_patterned_description(api):
    """Each seeded Tessera art piece carries the patterned alternative text."""
    body = api.get(f"/products/{FLAGSHIP_SLUG}").json()
    alts = sorted(str(piece.get("alt_text")) for piece in body.get("art") or [])
    expected = sorted(FLAGSHIP_ART_ALT.format(index=n, total=FLAGSHIP_ART)
                      for n in range(1, FLAGSHIP_ART + 1))
    assert alts == expected, f"the seeded art descriptions follow the pattern; saw {alts}"


def test_product_route_moves_its_sub_nav_and_rail_below_lg(page):
    """Wide, the sub-nav sits left and the rail right; narrow, both give up their columns."""
    origin = appclient.app_url()
    probe = (
        "([rail, sub]) => { const h = document.querySelector('h1').getBoundingClientRect();"
        " const find = t => Array.from(document.querySelectorAll('a, button, option, li'))"
        "   .filter(e => e.textContent.trim() === t && e.getBoundingClientRect().width > 0)[0];"
        " const r = find(rail), s = find(sub);"
        " return {h1: {left: h.left, bottom: h.bottom},"
        "  rail: r ? r.getBoundingClientRect().toJSON() : null,"
        "  sub: s ? s.getBoundingClientRect().toJSON() : null,"
        "  width: window.innerWidth}; }"
    )
    page.set_viewport_size(WIDE_VIEWPORT)
    page.goto(f"{origin}/product/{FLAGSHIP_SLUG}")
    wide = page.evaluate(probe, [FLAGSHIP_HIGHLIGHT_FIRST, FLAGSHIP_SUBNAV_ITEM])
    assert wide["rail"] and wide["rail"]["left"] > wide["width"] / 2, (
        f"at a wide window the highlights rail sits in the right column: {wide!r}"
    )
    assert wide["sub"] and wide["sub"]["right"] <= wide["h1"]["left"] + 1, (
        f"at a wide window the sub-nav sits in the left column: {wide!r}"
    )
    page.set_viewport_size(NARROW_VIEWPORT)
    page.goto(f"{origin}/product/{FLAGSHIP_SLUG}")
    narrow = page.evaluate(probe, [FLAGSHIP_HIGHLIGHT_FIRST, FLAGSHIP_SUBNAV_ITEM])
    assert narrow["rail"] and narrow["rail"]["top"] >= narrow["h1"]["bottom"], (
        f"below lg the highlights rail moves inline below the hero: {narrow!r}"
    )
    assert not narrow["sub"] or narrow["sub"]["left"] >= narrow["h1"]["left"] - 1, (
        f"below lg the sub-nav leaves its side column for a dropdown above the content: {narrow!r}"
    )


def test_datasheet_cover_keeps_a_three_by_four_ratio(page):
    """Every datasheet cover in the library stands in a three-by-four aspect ratio."""
    origin = appclient.app_url()
    page.goto(f"{origin}/datasheet")
    boxes = page.evaluate(
        "() => Array.from(document.querySelectorAll('main img, main svg, main canvas'))"
        ".map(e => e.getBoundingClientRect()).filter(b => b.width > 80)"
        ".map(b => b.height / b.width)")
    assert boxes, "the library draws a cover per card"
    off = [round(r, 3) for r in boxes if abs(r - COVER_RATIO) > 0.05]
    assert not off, f"each cover is three wide by four tall; ratios off the mark: {off}"


def test_the_page_ground_is_near_white_on_every_surface(page):
    """The ground behind the main content of each public surface is a near-white neutral."""
    origin = appclient.app_url()
    dark = []
    for route in ("/", "/product", "/datasheet", "/console", "/contact"):
        page.goto(f"{origin}{route}")
        colour = page.evaluate(
            "() => { let e = document.querySelector('main');"
            " while (e) { const c = getComputedStyle(e).backgroundColor;"
            "  if (c && c !== 'transparent' && !c.startsWith('rgba(0, 0, 0, 0')) return c;"
            "  e = e.parentElement; } return 'rgb(255, 255, 255)'; }")
        rgb = parse_rgb(colour)
        if min(rgb) < 240 or max(rgb) - min(rgb) > 12:
            dark.append((route, colour))
    assert not dark, f"every public surface stands on a near-white neutral ground; saw {dark}"


def test_console_reads_as_a_labelled_diagram_without_scripting(page):
    """With scripting off, the console still names its regions and offers its controls."""
    origin = appclient.app_url()
    context = page.context.browser.new_context(java_script_enabled=False)
    try:
        still = context.new_page()
        still.goto(f"{origin}/console")
        text = still.inner_text("main")
        absent = [region for region in REGIONS if region not in text]
        assert not absent, f"the still console names every region as text; missing {absent}"
        controls = still.evaluate(
            "() => document.querySelectorAll('main form, main button, main select').length")
        assert controls, "the still console keeps its write, read and partition controls"
    finally:
        context.close()


def _columns(page) -> int:
    return page.evaluate(
        "() => {const grid = document.querySelector('main ul, main ol, main div[class]');"
        "if (!grid) return 0;"
        "const kids = Array.from(grid.children).filter(k => k.getBoundingClientRect().width);"
        "if (!kids.length) return 0;"
        "const top = Math.round(kids[0].getBoundingClientRect().top);"
        "return kids.filter(k => Math.round(k.getBoundingClientRect().top) === top).length;}")

