"""Outcome graders for the Halden Drops task.

One module, every section and both declared slots. Black-box: HTTP against the running app,
the rendered page through Playwright, PostgreSQL through the shared backend adapter and the
application's own database role, and MinIO through the shared object-store adapter. Nothing
here reads the agent's source.
"""

from __future__ import annotations

import json
import os
import re
import time
from urllib.parse import parse_qs, urlparse

import httpx

import capabilities
from conftest import (
    AFTERGLOW, AGENCY_REASON, ANCHORS, ARTIST_HEADING, ATTRIBUTION_PARAM,
    ATTRIBUTION_PREFIX, AUDIT_ACTIONS, BASE_KEYS, BE_FR_SHOP_CTA, BODY_SIZE,
    CACHE_PARTS, COLLECTION_HEADING, COOKIE_MAX_AGE, CURRENCY, DATA_REGIONS,
    DE_SHOP_CTA, DISPLAY, DISPLAY_NAME, DUSK_HERO_BE_NL, DUSK_PARADE,
    DUSK_PRODUCT, EDITOR, EDITOR2, EDITOR3, EURO_PRICES, GRANT_MAX_DAYS,
    H1_WIDE, H2_WIDE, HERO_TITLE, HEX64, HOST, HREFLANG, LANG_COOKIE,
    LANG_LABEL, LEGAL, LEGAL2, LEGAL_ADDRESS, LEGAL_TITLE, LOOKBOOK_ALT,
    LOOKBOOK_HEADING, MARKETS, MENU_CLOSE, MERCHANDISER, META_DESCRIPTION,
    META_TITLE, NEWTAB_SUFFIX, OK, OWNER, PANTS, PASSWORD, POUND_PRICES,
    PRIVACY_FACTS, REASONS, REFERRER_POLICY, REQUEST_ID_HEADER, SEED_BUDGETS,
    SEED_COPY, SEED_GRANTS, SEED_MARKETS, SEED_PEOPLE, SEGMENT, SHOP_CTA,
    SIGN_IN_FAILED, SLOTS, STORY_HEADING, TEE, TEE_PINK, TEE_WHITE, TIMEOUT,
    TRANSLATOR, TYPEFACE, UPLOAD_LIMIT, WORDMARK_HOST, WORDMARK_NAME,
    ZERO_HASH, absent, anon, api_base, approve, approve_both, attrs_of,
    audit_events, backend, base_url, body, browser, calm_page, campaign,
    client_for, contrast_ratio, create_campaign, create_product, days_until,
    describe, digits, editor, etag_of, expected_link, hex_colour, html_of,
    iso_in, legal, link_path, live_market, login, market_of, merchandiser,
    meta_content, narrow_page, normalise_space, ok, owner, page, page_get,
    parse_colour, parsed_link, png_bytes, probe_value, public_payload,
    publish, ready_market, reason_of, refused, revoke_after, rollback, rows,
    set_price, settle, sha256_hex, sign_in_page, store, store_object, submit,
    tags, title_of, token_for, token_hex, translate_market, translations_of,
    translator, unpublish, upload, visible_text, write_translation,
)


def test_health_answers_once_the_app_is_ready():
    """The app answers its health route and serves the studio sign-in page. cov: C-TR-04, C-TR-09, C-DC-05, C-DC-06"""

    health = page_get("/api/health")
    assert health.status_code == 200, describe(health)
    login_page = page_get("/studio/login")
    assert login_page.status_code == 200, describe(login_page)
    assert "<form" in login_page.text.lower(), "the studio sign-in page must carry a form"


def test_a_live_market_page_declares_its_language_one_heading_and_its_landmarks():
    """A live market page is one document in its language with one h1 and the four landmarks. cov: C-CF-15, C-CF-19, C-CF-20, C-CF-21, C-UF-04"""

    for market in ("fr", "en"):
        html = html_of(f"/{AFTERGLOW}/{market}/")
        root = tags(html, "html")
        assert root and root[0].get("lang") == HREFLANG[market], \
            f"/{AFTERGLOW}/{market}/ must declare lang {HREFLANG[market]}: {root}"
        headings = re.findall(r"<h1\b[^>]*>(.*?)</h1>", html, re.I | re.S)
        assert len(headings) == 1, f"exactly one h1 on {market}, found {len(headings)}"
        assert normalise_space(re.sub(r"<[^>]+>", "", headings[0])) == HERO_TITLE[market]
        low = html.lower()
        for tag, role in (("header", "banner"), ("nav", "navigation"),
                          ("main", "main"), ("footer", "contentinfo")):
            assert f"<{tag}" in low or f'role="{role}"' in low, \
                f"the {role} landmark is missing on {market}"


def test_a_market_that_is_not_live_answers_not_found():
    """A market that is not live, an unknown campaign and a foreign legal slug answer not found. cov: C-RL-03, C-CF-16, C-CF-17, C-UF-22, C-DC-11"""

    for market in ("it", "de", "es", "be-nl", "be-fr"):
        absent(page_get(f"/{AFTERGLOW}/{market}/"), f"Afterglow {market}")
        absent(httpx.get(f"{api_base()}/public/campaigns/{AFTERGLOW}/markets/{market}",
                         timeout=TIMEOUT), f"the public payload of Afterglow {market}")
    absent(page_get(f"/probe-unknown-{token_hex(6)}/fr/"), "an unknown campaign")
    absent(page_get(f"/{AFTERGLOW}/fr/legal-notice/"), "a legal slug of another market")
    absent(page_get(f"/{AFTERGLOW}/de/impressum/"), "the legal notice of a market that is not live")


def test_sections_follow_the_campaign_order_with_anchors_named_by_their_heading():
    """Afterglow sections run in the campaign order and each anchored section is named by its heading. cov: C-OV-13, C-CF-22, C-CF-23, C-DM-13, C-DM-29"""

    html = html_of(f"/{AFTERGLOW}/en/")
    positions = []
    for anchor in ANCHORS:
        found = re.search(rf'<section\b[^>]*\bid="{anchor}"[^>]*>', html, re.I)
        assert found, f"the section #{anchor} must be a section element"
        positions.append(found.start())
    assert positions == sorted(positions), f"anchored sections out of order: {positions}"
    expected = {"collection": COLLECTION_HEADING["en"], "ardenne": ARTIST_HEADING["en"],
                "rx2k": STORY_HEADING["en"], "lookbook": LOOKBOOK_HEADING}
    for anchor, heading in expected.items():
        start = re.search(rf'<section\b[^>]*\bid="{anchor}"', html, re.I).start()
        chunk = html[start:start + 4000]
        opening = attrs_of(re.match(r"<section\b[^>]*>", chunk, re.I).group(0))
        label = opening.get("aria-label")
        if not label and opening.get("aria-labelledby"):
            ref = re.search(rf'id="{re.escape(opening["aria-labelledby"])}"[^>]*>(.*?)</',
                            html, re.S)
            label = normalise_space(re.sub(r"<[^>]+>", "", ref.group(1))) if ref else None
        assert label == heading, f"#{anchor} must be named {heading!r}, got {label!r}"


def test_the_served_document_carries_copy_links_prices_and_the_switcher_without_scripts():
    """The served document carries headings, links, prices and the switcher with no script run. cov: C-CF-36, C-CF-37, C-CF-65, C-CF-91, C-CF-106, C-UF-55, C-FE-09, C-TR-01, C-TR-02, C-DM-30"""

    html = html_of(f"/{AFTERGLOW}/fr/")
    text = visible_text(html)
    for heading in (HERO_TITLE["fr"], COLLECTION_HEADING["fr"], ARTIST_HEADING["fr"],
                    STORY_HEADING["fr"], LOOKBOOK_HEADING):
        assert heading in text, f"{heading!r} must be in the served document"
    payload = public_payload(AFTERGLOW, "fr")
    links = {a.get("data-colourway"): a.get("href") for a in tags(html, "a") if a.get("data-colourway")}
    models = {c["model_code"] for p in payload["products"] for c in p["colourways"]}
    assert models <= set(links), f"every colourway link must be served: {sorted(models - set(links))}"
    prices = re.findall(r"<[^>]+data-price[^>]*>(.*?)</", html, re.S)
    assert len([p for p in prices if normalise_space(re.sub(r"<[^>]+>", "", p))]) >= 4
    assert re.search(r"<select\b", html, re.I), "the language switcher must be served"
    alts = {attrs.get("alt") for attrs in tags(html, "img")}
    assert LOOKBOOK_ALT["fr"] in alts, f"the lookbook image must carry its alternative text: {alts}"
    assert not re.search(r'<(section|article)[^>]*style="[^"]*opacity:\s*0', html, re.I), \
        "no content section may be served invisible"


def test_decorative_stickers_are_hidden_from_assistive_technology():
    """Every decorative sticker is hidden from assistive technology and cannot take focus. cov: C-CF-32, C-CF-33"""

    html = html_of(f"/{AFTERGLOW}/fr/")
    stickers = [attrs for attrs in tags(html, "svg") if "data-sticker" in attrs] + \
        [attrs_of(m.group(0)) for m in re.finditer(r"<(?!svg)\w+\b[^>]*\bdata-sticker\b[^>]*>", html)]
    assert stickers, "the drop page must carry decorative stickers marked data-sticker"
    for attrs in stickers:
        assert attrs.get("aria-hidden") == "true", f"sticker announced: {attrs}"
        assert attrs.get("focusable") == "false", f"sticker focusable: {attrs}"


def test_the_menu_button_opens_a_modal_overlay_that_escape_closes(page):
    """The menu button reports its state, moves focus to the first item, and Escape closes the overlay. cov: C-CF-26, C-CF-27, C-CF-29"""

    page.goto(f"{base_url()}/{AFTERGLOW}/en/")
    button = page.locator("header button[aria-expanded], [role=banner] button[aria-expanded]").first
    assert button.get_attribute("aria-expanded") == "false"
    controls = button.get_attribute("aria-controls")
    assert controls, "the menu button must name the overlay with aria-controls"
    overlay = page.locator(f"[id='{controls}']")
    button.click()
    overlay.wait_for(state="visible", timeout=5000)
    assert button.get_attribute("aria-expanded") == "true"
    assert MENU_CLOSE["en"] in (button.inner_text() + " " + (button.get_attribute("aria-label") or ""))
    page.wait_for_function("""id => { const el = document.getElementById(id);
        const f = el.querySelector('a[href], button, [tabindex]:not([tabindex="-1"])');
        return !!f && f === document.activeElement; }""", arg=controls, timeout=5000)
    main_inert = page.evaluate("""() => { const m = document.querySelector('main');
        return !!(m && m.closest('[inert]')) || !!document.querySelector('dialog:modal'); }""")
    assert main_inert, "everything outside the open overlay must be inert"
    page.keyboard.press("Escape")
    overlay.wait_for(state="hidden", timeout=5000)
    assert button.get_attribute("aria-expanded") == "false"
    assert page.evaluate("() => document.activeElement.getAttribute('aria-controls')") == controls
    button.click()
    overlay.wait_for(state="visible", timeout=5000)
    overlay.get_by_role("link", name=COLLECTION_HEADING["en"], exact=True).click()
    overlay.wait_for(state="hidden", timeout=5000)
    page.wait_for_function("() => { const s = document.getElementById('collection'); "
                           "return !!s && s.contains(document.activeElement); }", timeout=5000)
    current = page.evaluate("id => [...document.getElementById(id).querySelectorAll('[aria-current=\"location\"]')]"
                            ".map(a => a.getAttribute('href') || '')", controls)
    assert any(href.endswith("#collection") for href in current), f"the section in view is marked current: {current}"


def test_reduced_motion_leaves_no_content_invisible(calm_page):
    """Under reduced motion every heading, card and price is opaque and inside the page width. cov: C-CF-38, C-CF-39, C-UX-33, C-TR-03"""

    calm_page.goto(f"{base_url()}/{AFTERGLOW}/fr/")
    calm_page.wait_for_load_state("networkidle")
    found = calm_page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('main h1, main h2, main [data-product], main [data-price]').forEach(el => {
            let node = el, opacity = 1;
            while (node && node.nodeType === 1) {
                opacity *= parseFloat(getComputedStyle(node).opacity);
                node = node.parentElement;
            }
            const box = el.getBoundingClientRect();
            out.push({opacity, left: box.left, right: box.right, width: window.innerWidth});
        });
        return out;
    }""")
    assert len(found) >= 6, f"the drop page must carry headings, cards and prices: {found}"
    for item in found:
        assert item["opacity"] > 0.99, f"content hidden under reduced motion: {item}"
        assert item["left"] >= -1 and item["right"] <= item["width"] + 1, \
            f"content pushed aside under reduced motion: {item}"


def test_the_legal_notice_lives_under_the_market_legal_slug():
    """Each live market's legal notice sits under its own slug with its title and body. cov: C-CF-41, C-CF-42, C-UF-05"""

    html = html_of(f"/{AFTERGLOW}/fr/mentions-legales/")
    assert LEGAL_TITLE["fr"] in visible_text(html)
    assert LEGAL_ADDRESS in visible_text(html)
    english = html_of(f"/{AFTERGLOW}/en/legal-notice/")
    assert LEGAL_TITLE["en"] in visible_text(english)
    absent(page_get(f"/{AFTERGLOW}/en/mentions-legales/"), "the French slug under en")


def test_the_campaign_index_lists_only_campaigns_with_a_live_market():
    """The campaign index lists Afterglow and only campaigns that have a live market. cov: C-CF-43, C-UF-02, C-UF-20"""

    html = html_of("/")
    hrefs = {link_path(a.get("href", "")) for a in tags(html, "a")}
    assert f"/{AFTERGLOW}/" in hrefs, "the index must link Afterglow"
    assert f"/{DUSK_PARADE}/" not in hrefs, "Dusk Parade has no live market and must be absent"
    for href in sorted(h for h in hrefs if re.fullmatch(r"/[a-z0-9-]+/", h)):
        if href in ("/privacy/", "/studio/"):
            continue
        slug = href.strip("/")
        live = httpx.get(f"{api_base()}/public/campaigns/{slug}/markets", timeout=TIMEOUT)
        if live.status_code == 200:
            assert body(live), f"{slug} is listed with no live market"


def test_the_campaign_root_prefers_the_cookie_then_accept_language_then_the_default():
    """The campaign root picks the cookie, then an exact tag, then a language, then the default. cov: C-OV-17, C-CF-54, C-CF-55, C-CF-56, C-CF-57, C-CF-58, C-UF-21"""

    def target(headers=None, cookies=None):
        response = httpx.get(f"{base_url()}/{AFTERGLOW}/", headers=headers or {},
                             cookies=cookies or {}, timeout=TIMEOUT, follow_redirects=False)
        assert response.status_code in (302, 303, 307), describe(response)
        return link_path(response.headers["location"])
    assert target({"Accept-Language": "en"}) == f"/{AFTERGLOW}/en/"
    assert target({"Accept-Language": "fr-BE"}) == f"/{AFTERGLOW}/fr/"
    assert target({"Accept-Language": "de-DE,de;q=0.9"}) == f"/{AFTERGLOW}/fr/"
    assert target({"Accept-Language": "fr"}, {LANG_COOKIE: "en"}) == f"/{AFTERGLOW}/en/"
    assert target({"Accept-Language": "en"}, {LANG_COOKIE: "it"}) == f"/{AFTERGLOW}/en/"
    absent(page_get(f"/{DUSK_PARADE}/"), "a campaign root with no live market")


def test_the_campaign_root_redirect_is_temporary_private_and_varies_by_language():
    """The campaign root redirect is temporary, private, unstored and varies by language and cookie. cov: C-CF-53, C-UF-03, C-TR-18"""

    response = page_get(f"/{AFTERGLOW}/", headers={"Accept-Language": "en"}, follow_redirects=False)
    assert response.status_code in (302, 303, 307), describe(response)
    cache = response.headers.get("cache-control", "").lower()
    assert "no-store" in cache and "private" in cache, f"root Cache-Control: {cache!r}"
    vary = response.headers.get("vary", "").lower()
    assert "accept-language" in vary and "cookie" in vary, f"root Vary: {vary!r}"


def test_the_language_switcher_lists_live_markets_and_keeps_the_same_document():
    """The switcher lists live markets in their own language and leads to the same document. cov: C-CF-59, C-CF-60, C-CF-61, C-CF-62"""

    html = html_of(f"/{AFTERGLOW}/fr/mentions-legales/")
    select = re.search(r"<select\b[^>]*>(.*?)</select>", html, re.I | re.S)
    assert select, "the legal notice must carry the language switcher"
    opening = attrs_of(re.search(r"<select\b[^>]*>", html, re.I).group(0))
    label = re.search(rf'<label[^>]*for="{re.escape(opening.get("id", "~"))}"[^>]*>(.*?)</label>', html, re.S)
    wrapping = re.search(r"<label\b[^>]*>(.*?)<select\b", html, re.I | re.S)
    texts = [normalise_space(re.sub(r"<[^>]+>", " ", m.group(1))) for m in (label, wrapping) if m]
    assert LANG_LABEL["fr"] in texts, f"the switcher label must read {LANG_LABEL['fr']!r}: {texts}"
    options = re.findall(r"<option\b([^>]*)>(.*?)</option>", select.group(1), re.S)
    seen = {}
    for raw, text in options:
        attrs = attrs_of(raw)
        value = attrs.get("value", "")
        path = parse_qs(urlparse(value).query).get("to", [value])[0]
        seen[attrs.get("lang")] = (normalise_space(text), link_path(path))
    assert seen.get("fr-FR") == (DISPLAY_NAME["fr"], f"/{AFTERGLOW}/fr/mentions-legales/"), seen
    assert seen.get("en") == (DISPLAY_NAME["en"], f"/{AFTERGLOW}/en/legal-notice/"), seen
    assert set(seen) == {"fr-FR", "en"}, f"only live markets may be listed: {seen}"


def test_choosing_a_language_sets_the_preference_cookie_and_refuses_foreign_targets():
    """Choosing a language sets drop_lang for a year and refuses a target off this site. cov: C-CF-63, C-CF-64, C-CF-66, C-UF-07"""

    target = f"/{AFTERGLOW}/en/legal-notice/"
    response = page_get("/lang", params={"to": target}, follow_redirects=False)
    assert 300 <= response.status_code < 400, describe(response)
    assert link_path(response.headers["location"]) == target
    cookie = response.headers.get("set-cookie", "")
    assert re.search(rf"\b{LANG_COOKIE}=en\b", cookie), f"cookie: {cookie!r}"
    low = cookie.lower()
    lifetime = response.cookies.jar and [c for c in response.cookies.jar if c.name == LANG_COOKIE]
    if f"max-age={COOKIE_MAX_AGE}" not in low:
        assert lifetime and lifetime[0].expires, f"cookie lifetime: {cookie!r}"
        days = days_until(lifetime[0].expires)
        assert 364 <= days <= 366, f"the preference must be kept for 365 days: {cookie!r}"
    assert "samesite=lax" in low and "path=/" in low, f"cookie attributes: {cookie!r}"
    for bad in ("https://elsewhere.example.com/", "//elsewhere.example.com/", f"/{AFTERGLOW}/it/"):
        refusal = page_get("/lang", params={"to": bad}, follow_redirects=False)
        assert 400 <= refusal.status_code < 500, f"/lang?to={bad} must be refused: {describe(refusal)}"
        assert LANG_COOKIE not in refusal.headers.get("set-cookie", ""), f"cookie set for {bad}"


def test_alternate_links_are_reciprocal_with_x_default_and_a_self_canonical():
    """Each live page lists every live market plus x-default, reciprocally, with a self canonical. cov: C-CF-67, C-CF-68, C-CF-69"""

    alternates = {}
    for market, path in (("fr", f"/{AFTERGLOW}/fr/"), ("en", f"/{AFTERGLOW}/en/")):
        html = html_of(path)
        links = [a for a in tags(html, "link") if (a.get("rel") or "").lower() == "alternate" and a.get("hreflang")]
        alternates[market] = {a["hreflang"]: link_path(a.get("href", "")) for a in links}
        canonical = [a for a in tags(html, "link") if (a.get("rel") or "").lower() == "canonical"]
        assert canonical and link_path(canonical[0].get("href", "")) == path, f"canonical on {path}"
    for market in ("fr", "en"):
        assert alternates[market].get("fr-FR") == f"/{AFTERGLOW}/fr/", alternates
        assert alternates[market].get("en") == f"/{AFTERGLOW}/en/", alternates
        assert alternates[market].get("x-default") == f"/{AFTERGLOW}/", alternates
        assert set(alternates[market]) == {"fr-FR", "en", "x-default"}, alternates


def test_every_public_route_has_its_own_title_and_description():
    """Every public route declares its own title and meta description, none shared. cov: C-CF-70, C-CF-71, C-CF-72"""

    routes = ["/", "/privacy/", f"/{AFTERGLOW}/fr/", f"/{AFTERGLOW}/en/",
              f"/{AFTERGLOW}/fr/mentions-legales/", f"/{AFTERGLOW}/en/legal-notice/"]
    titles, descriptions = {}, {}
    for route in routes:
        html = html_of(route)
        titles[route] = title_of(html)
        descriptions[route] = normalise_space(meta_content(html, "description") or "")
        assert titles[route] and descriptions[route], f"{route} lacks a title or a description"
    assert len(set(titles.values())) == len(routes), f"shared titles: {titles}"
    assert len(set(descriptions.values())) == len(routes), f"shared descriptions: {descriptions}"
    assert META_TITLE["fr"] in titles[f"/{AFTERGLOW}/fr/"]
    assert descriptions[f"/{AFTERGLOW}/en/"] == META_DESCRIPTION["en"]


def test_the_sitemap_lists_only_live_documents_and_robots_points_at_it():
    """The sitemap carries live documents only and robots names it and closes the studio and API. cov: C-CF-73, C-CF-74, C-CF-75, C-UF-09, C-UF-19"""

    sitemap = page_get("/sitemap.xml")
    assert sitemap.status_code == 200, describe(sitemap)
    paths = {link_path(loc) for loc in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", sitemap.text)}
    for live in ("/", "/privacy/", f"/{AFTERGLOW}/fr/", f"/{AFTERGLOW}/fr/mentions-legales/",
                 f"/{AFTERGLOW}/en/", f"/{AFTERGLOW}/en/legal-notice/"):
        assert live in paths, f"{live} missing from the sitemap"
    for hidden in (f"/{AFTERGLOW}/it/", f"/{AFTERGLOW}/be-fr/", f"/{DUSK_PARADE}/be-nl/"):
        assert hidden not in paths, f"{hidden} is not live and must be absent"
    robots = page_get("/robots.txt").text
    assert re.search(r"(?im)^sitemap:\s*\S*/sitemap\.xml\s*$", robots), robots
    assert re.search(r"(?im)^disallow:\s*/studio/", robots) and re.search(r"(?im)^disallow:\s*/api/", robots)


def test_every_storefront_link_is_derived_from_the_market_template(owner):
    """Every storefront link, in the payload and the page, is the market template filled in. cov: C-OV-03, C-OV-14, C-CF-78, C-CF-79, C-CF-81, C-CF-84, C-CF-85, C-CF-86, C-DM-03, C-DM-26, C-DC-10"""

    for market in ("fr", "en"):
        payload = public_payload(AFTERGLOW, market)
        html = html_of(f"/{AFTERGLOW}/{market}/")
        served = {a.get("data-colourway"): a.get("href") for a in tags(html, "a") if a.get("data-colourway")}
        for product in payload["products"]:
            for colourway in product["colourways"]:
                want = expected_link(market, product["commerce_product_id"],
                                     colourway["model_code"], SLOTS[colourway["model_code"]])
                assert parsed_link(colourway["url"]) == want, (market, colourway)
                assert parsed_link(served[colourway["model_code"]]) == want, (market, colourway)
    for market in ("es", "be-nl"):
        render = ok(owner.get(f"/campaigns/{AFTERGLOW}/markets/{market}/render"), f"render {market}")
        tee = next(p for p in render["products"] if p["commerce_product_id"] == TEE)
        pink = next(c for c in tee["colourways"] if c["model_code"] == TEE_PINK)
        assert parsed_link(pink["url"]) == expected_link(market, TEE, TEE_PINK, "p1"), pink


def test_every_market_link_carries_the_attribution_parameters(owner):
    """In every market every colourway link carries hscamp and type with its own slot. cov: C-CF-45, C-CF-80, C-CF-82, C-CF-87, C-DM-28"""

    for market in MARKETS:
        render = ok(owner.get(f"/campaigns/{AFTERGLOW}/markets/{market}/render"), f"render {market}")
        assert render["products"], f"{market} must render products"
        for product in render["products"]:
            for colourway in product["colourways"]:
                _, host, _, query = parsed_link(colourway["url"])
                assert host == HOST[market], colourway
                assert query.get("type") == ATTRIBUTION_PARAM, colourway
                assert query.get(ATTRIBUTION_PARAM) == f"{ATTRIBUTION_PREFIX}{AFTERGLOW}_{colourway['attribution_slot']}", colourway


def test_the_shop_action_leads_to_the_market_collection_page_with_attribution():
    """The shop action leads to the market collection page with the campaign attribution. cov: C-CF-88, C-CF-89, C-CF-90, C-DC-13"""

    for market in ("fr", "en"):
        payload = public_payload(AFTERGLOW, market)
        scheme, host, path, query = parsed_link(payload["shop_url"])
        assert (scheme, host, path) == ("https", HOST[market], f"{SEGMENT[market]}/c/{AFTERGLOW}"), payload["shop_url"]
        assert query == {ATTRIBUTION_PARAM: f"{ATTRIBUTION_PREFIX}{AFTERGLOW}", "type": ATTRIBUTION_PARAM}, query
        html = html_of(f"/{AFTERGLOW}/{market}/")
        shops = [a for a in tags(html, "a") if a.get("href") and parsed_link(a["href"])[:3] == (scheme, host, path)]
        assert shops, f"the {market} page must link the collection page"
        assert SHOP_CTA[market] in visible_text(html)


def test_new_tab_links_are_isolated_and_announced_to_assistive_technology():
    """New-tab links carry noopener noreferrer and leaving links announce the new tab. cov: C-CF-93, C-CF-94, C-FE-13"""

    for market in ("fr", "en"):
        html = html_of(f"/{AFTERGLOW}/{market}/")
        anchors = re.findall(r"(<a\b[^>]*>)(.*?)</a>", html, re.I | re.S)
        leaving = 0
        for opening, inner in anchors:
            attrs = attrs_of(opening)
            if attrs.get("target") == "_blank":
                rel = (attrs.get("rel") or "").lower().split()
                assert "noopener" in rel and "noreferrer" in rel, f"unsafe new-tab link: {opening}"
            href = attrs.get("href", "")
            if (href.startswith("http") and urlparse(href).netloc not in urlparse(base_url()).netloc
                    and urlparse(href).netloc != WORDMARK_HOST):
                leaving += 1
                assert NEWTAB_SUFFIX[market] in normalise_space(re.sub(r"<[^>]+>", " ", inner)), \
                    f"leaving link lacks the announcement on {market}: {opening}"
        assert leaving >= 5, f"the {market} page must carry its storefront links"
        wordmark = [attrs_of(o) for o, _ in anchors
                    if urlparse(attrs_of(o).get("href", "")).netloc == WORDMARK_HOST]
        assert wordmark and wordmark[0].get("aria-label") == WORDMARK_NAME, f"the wordmark link on {market}: {wordmark}"
        assert wordmark[0].get("target") == "_blank", f"the wordmark opens a new tab: {wordmark}"


def test_swatches_are_named_pressed_buttons_the_keyboard_operates(page):
    """Swatches are named buttons with one pressed per card, driven by Enter and the arrow keys. cov: C-CF-95, C-CF-97, C-CF-99, C-UX-36, C-FE-17"""

    page.goto(f"{base_url()}/{AFTERGLOW}/en/")
    card = page.locator(f'[data-product="{TEE}"]')
    pink = card.locator(f'button[data-swatch="{TEE_PINK}"]')
    white = card.locator(f'button[data-swatch="{TEE_WHITE}"]')
    assert pink.get_attribute("aria-pressed") == "true" and white.get_attribute("aria-pressed") == "false"
    names = page.evaluate("""(sel) => [...document.querySelectorAll(sel)].map(b =>
        (b.getAttribute('aria-label') || b.textContent || '').trim())""", f'[data-product="{TEE}"] button[data-swatch]')
    assert "Pink" in " ".join(names) and "White" in " ".join(names), names
    pink.focus()
    page.keyboard.press("ArrowRight")
    assert page.evaluate("() => document.activeElement.getAttribute('data-swatch')") == TEE_WHITE
    page.keyboard.press("Enter")
    page.wait_for_function("sel => document.querySelector(sel).getAttribute('aria-pressed') === 'true'",
                           arg=f'[data-product="{TEE}"] button[data-swatch="{TEE_WHITE}"]', timeout=5000)
    assert pink.get_attribute("aria-pressed") == "false"
    box = white.bounding_box()
    cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    hit = page.evaluate("""([x, y, sel]) => { const t = document.elementFromPoint(x, y);
        return !!(t && t.closest(sel)); }""", [cx + 21.9, cy, f'[data-product="{TEE}"] button[data-swatch="{TEE_WHITE}"]'])
    hit_v = page.evaluate("""([x, y, sel]) => { const t = document.elementFromPoint(x, y);
        return !!(t && t.closest(sel)); }""", [cx, cy + 21.9, f'[data-product="{TEE}"] button[data-swatch="{TEE_WHITE}"]'])
    assert hit and hit_v, "a swatch must offer a 44 by 44 CSS pixel hit area around its centre"


def test_an_unavailable_product_has_no_card_and_no_footer_row():
    """A product a market does not sell has no card and no footer row there. cov: C-CF-76, C-CF-100, C-CF-115, C-CN-03"""

    english = html_of(f"/{AFTERGLOW}/en/")
    assert f'data-product="{PANTS}"' not in english, "track pants are unavailable in en"
    assert len(set(re.findall(r'data-product="(\d+)"', english))) == 3
    assert "[04]" not in visible_text(english) and "[03]" in visible_text(english)
    french = html_of(f"/{AFTERGLOW}/fr/")
    assert len(set(re.findall(r'data-product="(\d+)"', french))) == 4
    assert "[04]" in visible_text(french)
    payload = public_payload(AFTERGLOW, "en")
    assert PANTS not in {p["commerce_product_id"] for p in payload["products"]}


def test_prices_are_formatted_in_the_market_currency_from_minor_units(owner):
    """Prices are formatted in each market's currency from integer minor units. cov: C-CF-102, C-CF-103, C-CF-104, C-CF-105, C-CF-112, C-CF-118, C-UF-33, C-TR-22"""

    for market in ("fr", "en"):
        payload = public_payload(AFTERGLOW, market)
        tee = next(p for p in payload["products"] if p["commerce_product_id"] == TEE)
        assert tee["price_currency"] == CURRENCY[market]
        assert tee["price_minor"] == (POUND_PRICES[TEE] if market == "en" else EURO_PRICES[TEE])
        assert normalise_space(tee["price_display"]) == DISPLAY[market], tee
        html = html_of(f"/{AFTERGLOW}/{market}/")
        start = html.find(f'data-product="{TEE}"')
        price = re.search(r"data-price[^>]*>(.*?)</", html[start:], re.S)
        assert price and normalise_space(re.sub(r"<[^>]+>", "", price.group(1))) == DISPLAY[market]
    for market in ("be-nl", "es"):
        render = ok(owner.get(f"/campaigns/{AFTERGLOW}/markets/{market}/render"), f"render {market}")
        tee = next(p for p in render["products"] if p["commerce_product_id"] == TEE)
        assert normalise_space(tee["price_display"]) == DISPLAY[market], tee


def test_a_product_without_a_price_shows_no_price_in_the_preview(owner, merchandiser, campaign):
    """An available product with no price renders its card without any price in the preview. cov: C-CF-03, C-CF-107, C-TR-08, C-DC-02"""

    product = create_product(merchandiser, campaign)
    ok(set_price(merchandiser, product["id"], "fr", available=True), "marking the probe available")
    render = ok(owner.get(f"/campaigns/{campaign}/markets/fr/render"), "probe render")
    row = next(p for p in render["products"] if p["commerce_product_id"] == product["commerce_product_id"])
    assert row["price_minor"] is None and not row.get("price_display"), row
    preview = owner.get(f"{base_url()}/studio/campaigns/{campaign}/markets/fr/preview/")
    assert preview.status_code == 200, describe(preview)
    start = preview.text.find(f'data-product="{product["commerce_product_id"]}"')
    assert start >= 0, "the unpriced product must still have a card"
    following = preview.text.find("data-product=", start + 20)
    card = preview.text[start:following if following > 0 else start + 3000]
    price = re.search(r"data-price[^>]*>(.*?)</", card, re.S)
    assert not price or not normalise_space(re.sub(r"<[^>]+>", "", price.group(1))), "no price may be shown"
    assert "€" not in visible_text(card) and "£" not in visible_text(card)


def test_a_colourway_slide_is_painted_in_its_stored_swatch(owner, page):
    """Each colourway slide is painted in the swatch colour the merchandiser stored. cov: C-CF-77, C-CF-108, C-CF-109, C-UX-13, C-CN-04"""

    listed = rows(owner.get(f"/campaigns/{AFTERGLOW}/products"), "Afterglow products")
    swatches = {c["model_code"]: c["swatch_hex"] for p in listed for c in p["colourways"]}
    page.goto(f"{base_url()}/{AFTERGLOW}/fr/")
    for model in (TEE_PINK, "7310377"):
        slide = page.locator(f'[data-slide="{model}"]').first
        colour = slide.evaluate("el => getComputedStyle(el).backgroundColor")
        assert parse_colour(colour) == hex_colour(swatches[model]), (model, colour, swatches[model])


def test_product_identifiers_and_swatches_are_validated(merchandiser, campaign):
    """Product identifiers, model codes and swatches are validated and a repeat is a duplicate. cov: C-CF-111, C-CF-119, C-CF-120, C-CF-121, C-CF-122, C-CF-149, C-DM-14"""

    def attempt(**overrides):
        payload = {"commerce_product_id": digits(6),
                   "colourways": [{"model_code": digits(7), "swatch_hex": "#3a6ea5"}]}
        payload.update(overrides)
        return merchandiser.post(f"/campaigns/{campaign}/products", json=payload)
    for bad, field in ((attempt(commerce_product_id="12a45"), "commerce_product_id"),
                       (attempt(commerce_product_id="123"), "commerce_product_id"),
                       (attempt(colourways=[{"model_code": "12345", "swatch_hex": "#3a6ea5"}]), "model_code"),
                       (attempt(colourways=[{"model_code": digits(7), "swatch_hex": "#3a6ea"}]), "swatch_hex"),
                       (attempt(colourways=[{"model_code": digits(7), "swatch_hex": "blue"}]), "swatch_hex")):
        refused(bad, f"an invalid {field}", "invalid")
        assert field in str(body(bad).get("fields", {})), f"the refusal must name {field}: {describe(bad)}"
    first = ok(attempt(commerce_product_id="55501234"), "a valid product")
    refused(attempt(commerce_product_id="55501234"), "a repeated product id", "duplicate")
    listed = rows(merchandiser.get(f"/campaigns/{campaign}/products"), "probe products")
    assert [p["commerce_product_id"] for p in listed] == [first["commerce_product_id"]]


def test_slots_are_assigned_by_the_server_and_a_sent_slot_is_refused(owner, merchandiser, campaign):
    """Slots count up per campaign from the highest used, and a sent slot is refused. cov: C-CF-123, C-CF-124, C-CF-125, C-CF-126, C-CF-266, C-DM-15, C-DC-20"""

    first = create_product(merchandiser, campaign, colourways=2)
    assert [c["attribution_slot"] for c in first["colourways"]] == ["p1", "p2"], first
    added = ok(merchandiser.post(f"/products/{first['id']}/colourways",
                                 json={"model_code": digits(7), "swatch_hex": "#112233"}), "a third colourway")
    assert added["attribution_slot"] == "p3", added
    second = create_product(merchandiser, campaign)
    assert second["colourways"][0]["attribution_slot"] == "p4", second
    refused(merchandiser.post(f"/products/{first['id']}/colourways",
                              json={"model_code": digits(7), "swatch_hex": "#112233", "attribution_slot": "p99"}),
            "a colourway sent with a slot", "field_not_permitted")
    slots = [c["attribution_slot"] for p in rows(merchandiser.get(f"/campaigns/{campaign}/products"), "products")
             for c in p["colourways"]]
    assert sorted(slots) == ["p1", "p2", "p3", "p4"], slots
    actions = {e["action"] for e in audit_events(owner, action="product.create", limit=50) if e["campaign_slug"] == campaign}
    actions |= {e["action"] for e in audit_events(owner, action="colourway.create", limit=50) if e["campaign_slug"] == campaign}
    assert actions == {"product.create", "colourway.create"}, actions
    afterglow = [c["attribution_slot"] for p in rows(owner.get(f"/campaigns/{AFTERGLOW}/products"), "Afterglow")
                 for c in p["colourways"]]
    assert sorted(afterglow, key=lambda s: int(s[1:])) == [f"p{i}" for i in range(1, 8)], afterglow


def test_creating_a_product_creates_its_name_strings(owner, merchandiser, campaign):
    """Creating a product creates its name string and one colour name string per colourway. cov: C-CF-127, C-CF-128, C-DC-19"""

    product = create_product(merchandiser, campaign, colourways=2)
    keys = {row["key"] for row in rows(owner.get(f"/campaigns/{campaign}/strings"), "probe strings")}
    assert f"product.{product['commerce_product_id']}.name" in keys, keys
    for colourway in product["colourways"]:
        assert f"colour.{colourway['model_code']}.name" in keys, keys
    french = translations_of(owner, campaign, "fr")
    assert f"product.{product['commerce_product_id']}.name" not in french


def test_a_price_is_whole_minor_units_inside_the_range(owner, merchandiser, campaign):
    """A price must be a whole number of minor units above zero and below one hundred million. cov: C-CF-129, C-CF-130, C-CF-133, C-CF-148, C-CF-267"""

    product = create_product(merchandiser, campaign)
    for bad in (20.00, "2000", 0, -5, 100000000, 12.5):
        refused(set_price(merchandiser, product["id"], "fr", available=True, price_minor=bad, price_currency="EUR"),
                f"price_minor {bad!r}", "invalid")
    refused(set_price(merchandiser, product["id"], "fr", available=True, price_minor=2000),
            "a price with no currency", "invalid")
    ok(set_price(merchandiser, product["id"], "fr", available=True, price_minor=99999999, price_currency="EUR"),
       "the largest legal price")
    stored = next(m for p in rows(merchandiser.get(f"/campaigns/{campaign}/products"), "products")
                  for m in p["markets"] if m["market_code"] == "fr")
    assert stored["price_minor"] == 99999999 and isinstance(stored["price_minor"], int), stored
    assert any(e["campaign_slug"] == campaign for e in audit_events(owner, action="price.write", decision="permit", limit=50))


def test_a_price_in_another_currency_is_refused_and_nothing_changes(merchandiser, backend):
    """A euro price on the pound market is refused and the stored pound price stays. cov: C-CF-131, C-CF-132, C-CF-150, C-UF-46, C-DM-16, C-DM-17, C-DC-14"""

    tee = next(p for p in rows(merchandiser.get(f"/campaigns/{AFTERGLOW}/products"), "Afterglow")
               if p["commerce_product_id"] == TEE)
    refused(set_price(merchandiser, tee["id"], "en", available=True, price_minor=1700, price_currency="EUR"),
            "a euro price for en", "currency_mismatch")
    after = next(p for p in rows(merchandiser.get(f"/campaigns/{AFTERGLOW}/products"), "Afterglow")
                 if p["commerce_product_id"] == TEE)
    english = next(m for m in after["markets"] if m["market_code"] == "en")
    assert (english["price_minor"], english["price_currency"]) == (POUND_PRICES[TEE], "GBP"), english
    stored = backend.query(
        "SELECT pm.price_minor, pm.price_currency FROM product_markets pm JOIN products p ON p.id = pm.product_id "
        "JOIN campaigns c ON c.id = p.campaign_id WHERE c.slug = %s AND p.commerce_product_id = %s AND pm.market_code = %s",
        (AFTERGLOW, TEE, "en"))
    assert stored and stored[0]["price_currency"].strip() == "GBP" and stored[0]["price_minor"] == POUND_PRICES[TEE], stored
    mismatched = backend.query(
        "SELECT count(*) AS n FROM product_markets pm JOIN markets m ON m.code = pm.market_code "
        "WHERE pm.price_currency IS NOT NULL AND trim(pm.price_currency) <> trim(m.currency)")
    assert mismatched[0]["n"] == 0, "a stored price carries another market's currency"


def test_only_the_merchandiser_writes_product_identity_and_prices(owner, editor, merchandiser, campaign):
    """Product identity and prices are the merchandiser's; others get field_not_permitted. cov: C-RL-08, C-RL-12, C-RL-16, C-CF-110, C-CF-134, C-CF-135"""

    product = create_product(merchandiser, campaign)
    refused(set_price(editor, product["id"], "fr", available=True, price_minor=2500, price_currency="EUR"),
            "an editor writing a price", "field_not_permitted")
    refused(set_price(owner, product["id"], "fr", price_minor=2500, price_currency="EUR"),
            "the owner writing a price", "field_not_permitted")
    refused(owner.post(f"/campaigns/{campaign}/products",
                       json={"commerce_product_id": digits(6),
                             "colourways": [{"model_code": digits(7), "swatch_hex": "#3a6ea5"}]}),
            "the owner creating a product", "field_not_permitted")
    refused(editor.patch(f"/products/{product['id']}", json={"commerce_product_id": digits(6)}),
            "an editor changing a product id", "field_not_permitted")
    ok(set_price(editor, product["id"], "fr", available=True), "an editor changing availability alone")
    row = next(m for p in rows(merchandiser.get(f"/campaigns/{campaign}/products"), "products")
               for m in p["markets"] if m["market_code"] == "fr" and p["id"] == product["id"])
    assert row["available"] is True and row["price_minor"] is None, row


def test_no_storefront_url_is_accepted_or_stored(merchandiser, campaign, backend):
    """A body carrying a url is refused and no table stores a storefront address. cov: C-CF-136, C-DM-06, C-DC-23"""

    product = create_product(merchandiser, campaign)
    refused(merchandiser.patch(f"/products/{product['id']}", json={"url": "https://shop-fr.example.com/p/1"}),
            "a product write carrying url", "field_not_permitted")
    columns = backend.query(
        "SELECT table_name, column_name FROM information_schema.columns WHERE table_schema = 'public' "
        "AND table_name IN ('markets', 'campaigns', 'campaign_markets', 'products', 'colourways', 'product_markets') "
        "AND column_name ILIKE %s", ("%url%",))
    assert columns == [], f"no storefront address may be stored: {columns}"


def test_sign_in_refuses_a_wrong_password_and_an_unknown_email_alike():
    """A wrong password and an unknown email get the same refusal message. cov: C-RL-22, C-CF-01, C-CF-02, C-CF-06, C-CF-09, C-DM-01"""

    wrong = login(OWNER, "wrong-password")
    unknown = login(f"nobody-{token_hex(6)}@example.com", PASSWORD)
    for response in (wrong, unknown):
        assert 400 <= response.status_code < 500, describe(response)
        assert SIGN_IN_FAILED in response.text, describe(response)
    assert wrong.status_code == unknown.status_code
    assert "token" not in body(wrong) and "token" not in body(unknown)
    for email in (OWNER, EDITOR, EDITOR2, EDITOR3, TRANSLATOR, LEGAL, LEGAL2, MERCHANDISER):
        assert token_for(email), email
    signed = ok(login(EDITOR), "signing in as the editor")
    principal = signed["principal"]
    assert principal["email"] == EDITOR and principal["display_name"] == SEED_PEOPLE[EDITOR], principal
    for grant in principal["grants"]:
        assert {"id", "role", "market_code", "effect", "expires_at"} <= set(grant), grant
    assert {(g["market_code"], g["effect"]) for g in principal["grants"]} >= {("fr", "permit"), ("be-fr", "deny")}


def test_passwords_and_tokens_are_stored_hashed_and_logout_retires_the_token(backend):
    """Passwords and tokens are stored hashed, and logout retires the token at once. cov: C-CF-04, C-CF-05, C-CF-08, C-CF-10, C-UF-25, C-DM-02, C-DM-07, C-DM-08"""

    token = token_for(EDITOR3)
    for row in backend.query("SELECT password_hash FROM principals"):
        assert PASSWORD not in str(row["password_hash"]), "a password is stored in the clear"
    found = backend.query("SELECT count(*) AS n FROM sessions WHERE token_hash = %s", (token,))
    assert found[0]["n"] == 0, "a bearer token is stored as itself"
    newest = backend.query("SELECT extract(epoch FROM expires_at - issued_at) AS span FROM sessions "
                           "ORDER BY issued_at DESC LIMIT 1")
    assert newest and abs(float(newest[0]["span"]) - 12 * 3600) <= 60, f"a token lives 12 hours: {newest}"
    with client_for(token) as session:
        ok(session.get("/me"), "the fresh token")
        ok(session.post("/auth/logout", json={}), "logging out")
        refused(session.get("/me"), "a retired token")
    with client_for(f"{token}x") as forged:
        refused(forged.get("/me"), "an unknown token")


def test_there_is_no_signup_and_the_staff_directory_answers_the_owner_only(owner, editor, anon, backend):
    """There is no signup, and the staff directory answers the owner only. cov: C-OV-23, C-RL-01, C-CF-11, C-CF-12, C-CF-141, C-CN-02"""

    before = backend.query("SELECT count(*) AS n FROM principals")[0]["n"]
    signup = httpx.post(f"{api_base()}/auth/signup",
                        json={"email": f"new-{token_hex(6)}@example.com", "password": PASSWORD}, timeout=TIMEOUT)
    assert 400 <= signup.status_code < 500, describe(signup)
    assert backend.query("SELECT count(*) AS n FROM principals")[0]["n"] == before
    refused(anon.get("/principals"), "an anonymous directory read", "not_authenticated")
    refused(editor.get("/principals"), "an editor directory read")
    listed = rows(owner.get("/principals"), "the owner directory read")
    assert {EDITOR, OWNER} <= {row["email"] for row in listed}


def test_a_write_outside_the_editor_grants_is_refused_as_out_of_scope(owner, editor):
    """An editor writing in a market outside its grants is refused as out of scope, unchanged. cov: C-OV-05, C-RL-11, C-CF-143, C-CF-162, C-CN-01"""

    refused(write_translation(editor, AFTERGLOW, "de", "shop.cta", "Kaufen", "reviewed"),
            "an editor writing de", "market_out_of_scope")
    assert translations_of(owner, AFTERGLOW, "de")["shop.cta"]["value"] == DE_SHOP_CTA
    refused(submit(editor, AFTERGLOW, "it"), "an editor submitting it", "market_out_of_scope")


def test_an_expired_grant_is_refused_while_the_token_still_authenticates(owner):
    """An expired grant is refused at decision time while the token still authenticates. cov: C-OV-06, C-CF-14, C-CF-144, C-CF-163, C-CF-175, C-DC-25"""

    with client_for(token_for(EDITOR2)) as agency:
        refused(write_translation(agency, AFTERGLOW, "de", "shop.cta", "Kaufen", "reviewed"),
                "the expired agency grant", "grant_expired")
        me = ok(agency.get("/me"), "the agency token")
        assert me.get("email", me.get("principal", {}).get("email")) == EDITOR2
    assert translations_of(owner, AFTERGLOW, "de")["shop.cta"]["value"] == DE_SHOP_CTA


def test_a_deny_grant_wins_over_a_permit(owner, editor):
    """A deny grant on be-fr wins over the editor's permit there. cov: C-RL-02, C-RL-25, C-CF-145, C-CF-164, C-DM-51"""

    refused(write_translation(editor, AFTERGLOW, "be-fr", "shop.cta", "Achetez", "reviewed"),
            "an editor writing be-fr", "explicit_deny")
    refused(submit(editor, AFTERGLOW, "be-fr"), "an editor submitting be-fr", "explicit_deny")
    assert translations_of(owner, AFTERGLOW, "be-fr")["shop.cta"]["value"] == BE_FR_SHOP_CTA


def test_the_translator_cannot_write_product_price_or_market_fields(owner, translator):
    """A translator writing a price, a model code, a swatch or a market field is refused. cov: C-RL-13, C-CF-146, C-CF-165"""

    tee = next(p for p in rows(owner.get(f"/campaigns/{AFTERGLOW}/products"), "Afterglow")
               if p["commerce_product_id"] == TEE)
    refused(set_price(translator, tee["id"], "de", available=True, price_minor=1, price_currency="EUR"),
            "a translator writing a price", "field_not_permitted")
    refused(set_price(translator, tee["id"], "de", available=False),
            "a translator writing availability", "field_not_permitted")
    refused(translator.post(f"/products/{tee['id']}/colourways", json={"model_code": digits(7), "swatch_hex": "#000000"}),
            "a translator adding a colourway", "field_not_permitted")
    refused(translator.patch(f"/campaigns/{AFTERGLOW}/markets/de", json={"product_order": [TEE]},
                             headers={"If-Match": etag_of(owner, AFTERGLOW, "de")}),
            "a translator writing a market field", "field_not_permitted")
    assert market_of(owner, AFTERGLOW, "de")["status"] == "in_review"


def test_the_merchandiser_cannot_submit_approve_or_publish(owner, merchandiser):
    """The merchandiser submitting, approving or publishing is refused by role. cov: C-RL-17, C-CF-142, C-CF-166"""

    refused(submit(merchandiser, AFTERGLOW, "be-nl"), "a merchandiser submit", "role_not_permitted")
    refused(approve(merchandiser, AFTERGLOW, "de", "legal"), "a merchandiser approval", "role_not_permitted")
    refused(publish(merchandiser, AFTERGLOW, "it"), "a merchandiser publish", "role_not_permitted")
    assert market_of(owner, AFTERGLOW, "be-nl")["status"] == "draft"
    assert market_of(owner, AFTERGLOW, "it")["status"] == "approved"


def test_a_market_outside_the_grants_reads_as_not_found(editor, translator, legal):
    """A market the principal holds no grant for answers as not found on every read. cov: C-RL-10, C-CF-167, C-CF-168, C-UF-13"""

    absent(editor.get(f"/campaigns/{AFTERGLOW}/markets/de"), "an editor reading de")
    absent(editor.get(f"/campaigns/{AFTERGLOW}/markets/de/render"), "an editor rendering de")
    absent(translator.get(f"/campaigns/{AFTERGLOW}/translations", params={"market": "fr"}), "a translator reading fr")
    absent(legal.get(f"/campaigns/{AFTERGLOW}/markets/de"), "legal reading de")
    studio = editor.get(f"{base_url()}/studio/campaigns/{AFTERGLOW}/markets/de/")
    absent(studio, "an editor opening the de market page")
    listed = rows(editor.get(f"/campaigns/{AFTERGLOW}/markets"), "an editor's market list")
    assert {row["market_code"] for row in listed} <= {"fr", "be-nl", "be-fr"}, listed


def test_an_owner_issued_grant_works_at_once_and_expires_mid_session(owner, campaign, revoke_after):
    """An owner-issued grant works on the next request and stops at its expiry mid-session. cov: C-OV-21, C-RL-06, C-CF-13, C-CF-169, C-CF-172, C-CF-174"""

    expiry_seconds = 12
    grant = ok(owner.post("/grants", json={"email": EDITOR3, "role": "editor", "market_code": "it",
                                           "expires_at": iso_in(expiry_seconds), "reason": "probe window"}),
               "issuing a short grant")
    revoke_after.append(grant["id"])
    with client_for(token_for(EDITOR3)) as agency:
        ok(write_translation(agency, campaign, "it", "shop.cta", "Negozio probe", "draft"), "the fresh grant")
        settle(expiry_seconds + 3)
        refused(write_translation(agency, campaign, "it", "shop.cta", "Negozio dopo", "draft"),
                "the same token after expiry", "grant_expired")
        ok(agency.get("/me"), "the token after expiry")
    assert translations_of(owner, campaign, "it")["shop.cta"]["value"] == "Negozio probe"


def test_a_grant_needs_an_expiry_a_reason_and_a_grantable_role(owner, editor):
    """A grant needs a future expiry within ninety days, a reason and a grantable role. cov: C-CF-147, C-CF-170, C-CF-171"""

    base = {"email": EDITOR3, "role": "translator", "market_code": "es", "reason": "probe"}
    for missing, payload in (("expiry", base),
                             ("past expiry", {**base, "expires_at": iso_in(-3600)}),
                             ("far expiry", {**base, "expires_at": iso_in((GRANT_MAX_DAYS + 1) * 86400)}),
                             ("reason", {k: v for k, v in {**base, "expires_at": iso_in(86400)}.items() if k != "reason"})):
        refused(owner.post("/grants", json=payload), f"a grant without a valid {missing}", "invalid")
    for role in ("owner", "legal", "merchandiser"):
        refused(owner.post("/grants", json={**base, "role": role, "expires_at": iso_in(86400)}),
                f"a {role} grant", "role_not_grantable")
    refused(editor.post("/grants", json={**base, "expires_at": iso_in(86400)}), "an editor issuing a grant", "role_not_permitted")
    issued = [g for g in rows(owner.get("/grants"), "grants") if g["email"] == EDITOR3 and g["market_code"] == "es"
              and not g.get("revoked_at")]
    assert issued == [], issued


def test_a_revoked_grant_stops_the_next_request(owner, translator, campaign, revoke_after):
    """Revoking a grant stops the grantee's very next request in that market. cov: C-CF-173, C-CF-265, C-DM-09, C-DC-21"""

    grant = ok(owner.post("/grants", json={"email": TRANSLATOR, "role": "translator", "market_code": "fr",
                                           "expires_at": iso_in(86400), "reason": "probe revoke"}), "issuing")
    revoke_after.append(grant["id"])
    ok(write_translation(translator, campaign, "fr", "shop.cta", "Boutique probe", "draft"), "the new grant")
    ok(owner.delete(f"/grants/{grant['id']}"), "revoking")
    refused(write_translation(translator, campaign, "fr", "shop.cta", "Boutique apres", "draft"),
            "the next request after revocation", "market_out_of_scope")
    revoked = next(g for g in rows(owner.get("/grants"), "grants") if g["id"] == grant["id"])
    assert revoked.get("revoked_at"), revoked
    for action in ("grant.create", "grant.revoke"):
        assert any(str(e["resource_id"]) == str(grant["id"]) for e in audit_events(owner, action=action, limit=50)), action


def test_every_refusal_carries_its_reason_and_the_request_id(owner, editor, anon):
    """Every refusal body carries title, reason and the request id echoed in X-Request-Id. cov: C-CF-137, C-CF-138, C-CF-139, C-CF-274, C-TR-10, C-DC-07, C-DC-08"""

    for response in (write_translation(editor, AFTERGLOW, "de", "shop.cta", "x", "draft"),
                     anon.get(f"/campaigns/{AFTERGLOW}/markets"),
                     owner.post("/grants", json={"email": EDITOR3})):
        assert 400 <= response.status_code < 500, describe(response)
        data = body(response)
        assert data.get("title") and data.get("reason") in REASONS, describe(response)
        assert data.get("request_id") and response.headers.get(REQUEST_ID_HEADER) == data["request_id"], describe(response)
    invalid = owner.post("/grants", json={"email": EDITOR3})
    assert body(invalid).get("fields"), f"a validation refusal names its fields: {describe(invalid)}"
    refused(anon.put(f"/campaigns/{AFTERGLOW}/translations/de/shop.cta", json={"value": "", "status": "bogus"}),
            "an anonymous invalid write", "not_authenticated")
    refused(write_translation(editor, AFTERGLOW, "de", "shop.cta", "", "bogus"),
            "an out-of-scope write with an invalid body", "invalid")
    success = owner.get("/me")
    assert success.headers.get(REQUEST_ID_HEADER), "a success also carries a request id"


def test_a_translation_longer_than_its_budget_is_rejected(owner, campaign):
    """A translation longer than its string's budget is rejected naming value. cov: C-CF-179, C-CF-268, C-DM-18, C-DC-15"""

    key = f"probe.budget{token_hex(4)}"
    ok(owner.post(f"/campaigns/{campaign}/strings", json={"key": key, "context": "probe", "max_length": 10}),
       "a budgeted string")
    too_long = write_translation(owner, campaign, "fr", key, "x" * 11, "draft")
    refused(too_long, "a value over max_length", "invalid")
    assert "value" in str(body(too_long).get("fields", {})), describe(too_long)
    assert key not in translations_of(owner, campaign, "fr")
    ok(write_translation(owner, campaign, "fr", key, "x" * 10, "draft"), "a value at max_length")
    assert any(e["campaign_slug"] == campaign for e in audit_events(owner, action="string.create", limit=50))
    refused(owner.post(f"/campaigns/{campaign}/strings", json={"key": key, "context": "again", "max_length": 10}),
            "a repeated key", "duplicate")


def test_untranslated_default_copy_is_refused_in_another_language(owner, campaign):
    """Default copy repeated word for word in another language is refused; short labels and be-fr pass. cov: C-CF-153, C-CF-180, C-CF-181, C-CF-182"""

    source = f"Une phrase source assez longue {token_hex(6)}"
    ok(write_translation(owner, campaign, "fr", "meta.description", source, "reviewed"), "the default copy")
    refused(write_translation(owner, campaign, "de", "meta.description", f"{source} und mehr", "reviewed"),
            "the French copy inside the German value", "untranslated_copy")
    ok(write_translation(owner, campaign, "be-fr", "meta.description", source, "reviewed"),
       "the same language in be-fr")
    ok(write_translation(owner, campaign, "fr", "menu.label", "Menu", "reviewed"), "a short default label")
    ok(write_translation(owner, campaign, "en", "menu.label", "Menu", "reviewed"), "a short label repeated")
    assert "meta.description" not in translations_of(owner, campaign, "de")


def test_legal_text_is_never_accepted_as_machine_translation(owner, campaign):
    """legal.body and legal.title are never accepted with the status machine. cov: C-CF-154, C-CF-183"""

    for key in ("legal.body", "legal.title"):
        refused(write_translation(owner, campaign, "de", key, f"Rechtlicher Text {token_hex(4)}", "machine"),
                f"machine {key}", "machine_legal_text")
        assert key not in translations_of(owner, campaign, "de")
    ok(write_translation(owner, campaign, "de", "hero.title", f"Maschinell {token_hex(4)}", "machine"),
       "machine copy outside the legal text")


def test_a_source_edit_requeues_every_other_market(owner, campaign):
    """A default-locale edit moves other markets' reviewed copy to draft and their workflow back to draft. cov: C-CF-184, C-CF-185"""

    marker = token_hex(6)
    for market in ("fr", "de", "it"):
        translate_market(owner, campaign, market, marker)
    ok(submit(owner, campaign, "de"), "submitting de")
    with client_for(token_for(LEGAL2)) as reviewer:
        ok(approve(reviewer, campaign, "de", "legal"), "legal approval of de")
    ok(write_translation(owner, campaign, "fr", "hero.title", f"hero.title fr changed {marker}", "reviewed"),
       "editing the default copy")
    for market in ("de", "it"):
        assert translations_of(owner, campaign, market)["hero.title"]["status"] == "draft", market
        assert translations_of(owner, campaign, market)["meta.title"]["status"] == "reviewed", market
    german = market_of(owner, campaign, "de")
    assert german["status"] == "draft", german
    assert german["approvals"] and all(a["superseded"] for a in german["approvals"]), german


def test_a_new_campaign_starts_with_eleven_strings_and_seven_draft_markets(owner, campaign, backend):
    """A new campaign has the eleven base strings, the four sections and seven draft markets. cov: C-CF-176, C-CF-188, C-CF-189, C-CF-190, C-DM-12, C-DC-16"""

    keys = sorted(row["key"] for row in rows(owner.get(f"/campaigns/{campaign}/strings"), "probe strings"))
    assert keys == sorted(BASE_KEYS), keys
    markets = rows(owner.get(f"/campaigns/{campaign}/markets"), "probe markets")
    assert sorted(m["market_code"] for m in markets) == sorted(MARKETS), markets
    assert all(m["status"] == "draft" and m["live_version"] is None for m in markets), markets
    assert all(HEX64.match(m["content_hash"]) for m in markets), markets
    sections = backend.query(
        "SELECT s.kind, s.anchor FROM page_sections s JOIN campaigns c ON c.id = s.campaign_id "
        "WHERE c.slug = %s ORDER BY s.sort_order", (campaign,))
    assert [s["kind"] for s in sections] == ["hero", "collection", "footer_list", "legal_footer"], sections
    assert sections[1]["anchor"] == "collection", sections


def test_the_preview_marks_untranslated_strings_and_carries_noindex(owner, campaign):
    """The preview marks each missing string data-untranslated and tells robots to stay away. cov: C-CF-191, C-CF-192, C-UF-14, C-DM-19"""

    ok(write_translation(owner, campaign, "fr", "hero.title", f"Titre probe {token_hex(6)}", "reviewed"), "default copy")
    preview = owner.get(f"{base_url()}/studio/campaigns/{campaign}/markets/de/preview/")
    assert preview.status_code == 200, describe(preview)
    robots = (meta_content(preview.text, "robots") or "") + " " + preview.headers.get("x-robots-tag", "")
    assert "noindex" in robots.lower(), "the preview must carry noindex"
    marked = set(re.findall(r'data-untranslated="([^"]+)"', preview.text))
    assert "hero.title" in marked, marked
    afterglow = owner.get(f"{base_url()}/studio/campaigns/{AFTERGLOW}/markets/es/preview/")
    assert {"legal.body", "story.body"} <= set(re.findall(r'data-untranslated="([^"]+)"', afterglow.text))
    assert 'data-untranslated' not in html_of(f"/{AFTERGLOW}/fr/")


def test_submit_is_refused_while_translations_or_prices_are_incomplete(owner, merchandiser, campaign):
    """Submit is refused while strings or prices are incomplete, and only a draft submits. cov: C-CF-151, C-CF-152, C-CF-178, C-CF-199, C-CF-207, C-CF-208, C-CF-209, C-CF-210"""

    incomplete = submit(owner, AFTERGLOW, "es")
    refused(incomplete, "submitting Afterglow es", "translations_incomplete")
    assert {"legal.body", "story.body", "artist.bio"} <= set(body(incomplete).get("keys", [])), describe(incomplete)
    assert market_of(owner, AFTERGLOW, "es")["status"] == "draft"
    product = create_product(merchandiser, campaign)
    ok(set_price(merchandiser, product["id"], "fr", available=True), "an available unpriced product")
    marker = token_hex(6)
    translate_market(owner, campaign, "fr", marker)
    names = [f"product.{product['commerce_product_id']}.name"] + [f"colour.{c['model_code']}.name" for c in product["colourways"]]
    translate_market(owner, campaign, "fr", marker, keys=names)
    unpriced = submit(owner, campaign, "fr")
    refused(unpriced, "submitting with an unpriced product", "price_missing")
    assert product["commerce_product_id"] in str(body(unpriced).get("products", [])), describe(unpriced)
    refused(submit(owner, AFTERGLOW, "it"), "submitting an approved market", "invalid")


def test_the_seeded_market_states_and_approvals_match(owner):
    """The seeded Afterglow markets hold the pinned statuses, live versions and approvals. cov: C-CF-193, C-CF-194, C-CF-195, C-CF-196, C-CF-198, C-CF-200, C-CF-201, C-DM-11, C-DM-33, C-DC-09"""

    expected = {"fr": ("published", 1), "en": ("published", 1), "it": ("approved", None),
                "de": ("in_review", None), "es": ("draft", None), "be-nl": ("draft", None),
                "be-fr": ("unpublished", None)}
    for market, (status, live) in expected.items():
        state = market_of(owner, AFTERGLOW, market)
        assert (state["status"], state["live_version"]) == (status, live), (market, state)
        current = {a["kind"] for a in state["approvals"] if not a["superseded"] and a["decision"] == "approved"
                   and a["content_hash"] == state["content_hash"]}
        want = {"legal", "owner"} if market in ("fr", "en", "it", "be-fr") else ({"legal"} if market == "de" else set())
        assert current == want, (market, state["approvals"])
    stored = rows(owner.get(f"/campaigns/{AFTERGLOW}/markets/be-fr/artifacts"), "be-fr artifacts")
    assert [(a["version"], a["live"]) for a in stored] == [(1, False)], stored
    assert {row["status"] for row in translations_of(owner, AFTERGLOW, "it").values()} == {"reviewed"}
    translations = translations_of(owner, AFTERGLOW, "es")
    assert "legal.body" not in translations and translations["artist.bio"]["status"] == "machine"


def test_approvals_bind_to_the_content_hash_and_an_edit_supersedes_them(owner, campaign, backend):
    """Each approval records the market hash and an edit supersedes both, back to draft. cov: C-OV-19, C-CF-203, C-CF-204, C-CF-215, C-CF-218, C-DM-21, C-DM-22, C-DC-26"""

    marker = token_hex(6)
    translate_market(owner, campaign, "fr", marker)
    ok(submit(owner, campaign, "fr"), "submitting fr")
    before = market_of(owner, campaign, "fr")
    assert before["status"] == "in_review"
    approved = approve_both(owner, campaign, "fr")
    assert approved["status"] == "approved", approved
    assert {a["content_hash"] for a in approved["approvals"]} == {before["content_hash"]}, approved
    stored = backend.query(
        "SELECT a.kind, a.content_hash, a.superseded FROM approvals a JOIN campaigns c ON c.id = a.campaign_id "
        "WHERE c.slug = %s AND a.market_code = 'fr'", (campaign,))
    assert sorted(r["kind"] for r in stored) == ["legal", "owner"], stored
    ok(write_translation(owner, campaign, "fr", "meta.title", f"meta.title fr edited {marker}", "reviewed"), "editing")
    after = market_of(owner, campaign, "fr")
    assert after["status"] == "draft" and after["content_hash"] != before["content_hash"], after
    assert all(a["superseded"] for a in after["approvals"]), after
    refused(publish(owner, campaign, "fr"), "publishing after the edit", "approvals_incomplete")


def test_approving_and_publishing_one_market_leaves_every_other_untouched(owner, campaign):
    """Approving and publishing fr leaves de's status, approvals, hash and page untouched. cov: C-OV-18, C-CF-219, C-CF-220, C-DC-12"""

    marker = token_hex(6)
    for market in ("fr", "de"):
        translate_market(owner, campaign, market, marker)
        ok(submit(owner, campaign, market), f"submitting {market}")
    with client_for(token_for(LEGAL2)) as reviewer:
        ok(approve(reviewer, campaign, "de", "legal"), "legal approval of de")
    german = market_of(owner, campaign, "de")
    approve_both(owner, campaign, "fr")
    published = ok(publish(owner, campaign, "fr"), "publishing fr")
    assert published["status"] == "published" and published["live_version"] == 1, published
    assert market_of(owner, campaign, "de") == german
    assert page_get(f"/{campaign}/fr/").status_code == 200
    absent(page_get(f"/{campaign}/de/"), "the untouched de page")
    live = rows(httpx.get(f"{api_base()}/public/campaigns/{campaign}/markets", timeout=TIMEOUT), "live markets")
    assert [m["market_code"] for m in live] == ["fr"], live


def test_a_legal_approval_needs_a_legal_grant_covering_the_market(owner, legal, campaign):
    """A legal approval needs a legal grant for the market and each kind belongs to its role. cov: C-RL-07, C-RL-14, C-CF-212, C-CF-213, C-CF-214"""

    marker = token_hex(6)
    for market in ("fr", "de"):
        translate_market(owner, campaign, market, marker)
        ok(submit(owner, campaign, market), f"submitting {market}")
    refused(approve(legal, campaign, "de", "legal"), "legal approving de", "market_out_of_scope")
    refused(approve(legal, campaign, "fr", "owner"), "legal recording the owner kind", "role_not_permitted")
    refused(approve(owner, campaign, "fr", "legal"), "the owner recording the legal kind", "role_not_permitted")
    assert market_of(owner, campaign, "de")["approvals"] == []
    assert market_of(owner, campaign, "fr")["approvals"] == []


def test_publish_is_refused_without_both_current_approvals(owner, legal, campaign):
    """Publish is refused unless a current legal and a current owner approval both exist. cov: C-OV-07, C-CF-155, C-CF-217, C-CF-222"""

    marker = token_hex(6)
    translate_market(owner, campaign, "fr", marker)
    refused(publish(owner, campaign, "fr"), "publishing a draft", "approvals_incomplete")
    ok(submit(owner, campaign, "fr"), "submitting fr")
    ok(approve(legal, campaign, "fr", "legal"), "legal approval")
    refused(publish(owner, campaign, "fr"), "publishing with legal only", "approvals_incomplete")
    rejected = ok(approve(owner, campaign, "fr", "owner", "rejected"), "an owner rejection")
    assert rejected["status"] == "draft", rejected
    refused(publish(owner, campaign, "fr"), "publishing after a rejection", "approvals_incomplete")
    absent(page_get(f"/{campaign}/fr/"), "a page never published")


def test_publish_is_refused_before_the_embargo(owner):
    """Publishing before the campaign embargo is refused, and allowed once the embargo passes. cov: C-CF-156, C-CF-223, C-CF-269, C-DM-10, C-DC-17"""

    embargoed = create_campaign(owner, embargo_at=iso_in(86400))["slug"]
    ready_market(owner, embargoed, "fr", token_hex(6))
    refused(publish(owner, embargoed, "fr"), "publishing before the embargo", "embargo_pending")
    absent(page_get(f"/{embargoed}/fr/"), "the embargoed page")
    ok(owner.patch(f"/campaigns/{embargoed}", json={"embargo_at": iso_in(-60)}), "moving the embargo into the past")
    ok(publish(owner, embargoed, "fr"), "publishing after the embargo")
    assert page_get(f"/{embargoed}/fr/").status_code == 200
    for action in ("campaign.create", "campaign.update"):
        assert any(e["campaign_slug"] == embargoed for e in audit_events(owner, action=action, limit=50)), action


def test_a_repeated_idempotency_key_publishes_once(owner, campaign, backend):
    """A repeated Idempotency-Key returns the first publish and writes one version and one event. cov: C-CF-225, C-CF-226, C-TR-20, C-DM-25"""

    ready_market(owner, campaign, "fr", token_hex(6))
    key = f"probe-{token_hex(12)}"
    first = publish(owner, campaign, "fr", key)
    second = publish(owner, campaign, "fr", key)
    assert first.status_code in OK and second.status_code == first.status_code, (describe(first), describe(second))
    assert body(second).get("live_version") == body(first).get("live_version") == 1
    artifacts = rows(owner.get(f"/campaigns/{campaign}/markets/fr/artifacts"), "artifacts")
    assert [a["version"] for a in artifacts] == [1], artifacts
    events = backend.query("SELECT count(*) AS n FROM audit_events WHERE action = 'market.publish' "
                           "AND campaign_slug = %s AND decision = 'permit'", (campaign,))
    assert events[0]["n"] == 1, events


def test_unpublish_takes_the_page_down_at_once_without_approval(owner, legal, campaign):
    """Unpublish by a legal reviewer takes the page down at once, and a second unpublish is not_live. cov: C-CF-157, C-CF-227, C-CF-228, C-CF-229, C-CF-230"""

    live_market(owner, campaign, "fr", token_hex(6))
    assert page_get(f"/{campaign}/fr/").status_code == 200
    state = ok(unpublish(legal, campaign, "fr"), "legal unpublishing fr")
    assert state["status"] == "unpublished" and state["live_version"] is None, state
    absent(page_get(f"/{campaign}/fr/"), "the unpublished page")
    absent(httpx.get(f"{api_base()}/public/campaigns/{campaign}/markets/fr", timeout=TIMEOUT), "the unpublished payload")
    assert any(e["campaign_slug"] == campaign and e["actor_email"] == LEGAL
               for e in audit_events(owner, action="market.unpublish", limit=50))
    refused(unpublish(owner, campaign, "fr"), "unpublishing again", "not_live")
    republished = ok(publish(owner, campaign, "fr"), "republishing with current approvals")
    assert republished["live_version"] == 2, republished


def test_rollback_makes_the_previous_artifact_live(owner, campaign):
    """Rollback makes the previous artifact version live, then has nothing further to roll back. cov: C-CF-158, C-CF-232, C-CF-233, C-CF-234, C-CF-264"""

    marker = token_hex(6)
    live_market(owner, campaign, "fr", marker)
    first_title = public_payload(campaign, "fr")["strings"]["hero.title"]
    ok(write_translation(owner, campaign, "fr", "hero.title", f"hero.title fr second {marker}", "reviewed"), "editing")
    ok(submit(owner, campaign, "fr"), "resubmitting")
    approve_both(owner, campaign, "fr")
    second = ok(publish(owner, campaign, "fr"), "publishing version 2")
    assert second["live_version"] == 2
    assert f"second {marker}" in html_of(f"/{campaign}/fr/")
    rolled = ok(rollback(owner, campaign, "fr"), "rolling back")
    assert rolled["live_version"] == 1 and rolled["status"] == second["status"], rolled
    assert public_payload(campaign, "fr")["strings"]["hero.title"] == first_title
    assert first_title in html_of(f"/{campaign}/fr/")
    refused(rollback(owner, campaign, "fr"), "rolling back past version 1", "nothing_to_roll_back")
    for action in ("translation.write", "market.submit", "approval.record", "market.publish", "market.rollback"):
        assert any(e["campaign_slug"] == campaign and e["decision"] == "permit"
                   for e in audit_events(owner, action=action, limit=50)), action


def test_the_live_page_shows_the_artifact_rather_than_later_edits(owner, campaign):
    """After publishing, an edit changes nothing on the live page until the next publish. cov: C-CF-186, C-CF-235, C-CF-236"""

    marker = token_hex(6)
    live_market(owner, campaign, "fr", marker)
    published_title = probe_value("hero.title", "fr", marker)
    ok(write_translation(owner, campaign, "fr", "hero.title", f"hero.title fr unpublished edit {marker}", "reviewed"), "editing")
    state = market_of(owner, campaign, "fr")
    assert state["status"] == "draft" and state["live_version"] == 1, state
    html = html_of(f"/{campaign}/fr/")
    assert published_title in html and "unpublished edit" not in html
    assert public_payload(campaign, "fr")["strings"]["hero.title"] == published_title


def test_a_market_change_needs_a_current_if_match(owner, merchandiser, campaign):
    """A market change without If-Match, or with a stale one, is refused and writes nothing. cov: C-CF-159, C-CF-160, C-CF-237, C-CF-238, C-CF-239, C-CF-240, C-CF-255, C-CF-270, C-CF-271, C-CF-272, C-DC-03"""

    products = [create_product(merchandiser, campaign) for _ in range(3)]
    for rank, product in enumerate(products, start=1):
        ok(merchandiser.patch(f"/products/{product['id']}", json={"sort_order": rank}), "setting the campaign order")
        ok(set_price(merchandiser, product["id"], "fr", available=True, price_minor=1000 * rank, price_currency="EUR"),
           "pricing a probe product")
    assert any(e["campaign_slug"] == campaign and e["decision"] == "permit"
               for e in audit_events(owner, action="product.update", limit=50))
    ok(set_price(merchandiser, products[0]["id"], "fr", available=True), "writing availability alone")
    listed = rows(merchandiser.get(f"/campaigns/{campaign}/products"), "the probe products")
    kept = next(m for p in listed if p["id"] == products[0]["id"] for m in p["markets"] if m["market_code"] == "fr")
    assert (kept["price_minor"], kept["price_currency"]) == (1000, "EUR"), f"a field left out keeps its value: {kept}"
    ids = [p["commerce_product_id"] for p in products]

    def rendered():
        payload = ok(owner.get(f"/campaigns/{campaign}/markets/fr/render"), "the probe render")
        return [p["commerce_product_id"] for p in payload["products"] if p["commerce_product_id"] in ids]
    order = [ids[2]]
    refused(owner.patch(f"/campaigns/{campaign}/markets/fr", json={"product_order": order}),
            "a market change without If-Match", "precondition_required")
    etag = etag_of(owner, campaign, "fr")
    first = owner.patch(f"/campaigns/{campaign}/markets/fr", json={"product_order": order}, headers={"If-Match": etag})
    ok(first, "the first save")
    assert first.headers.get("etag") and first.headers["etag"] != etag, describe(first)
    with client_for(token_for(EDITOR)) as second_editor:
        stale = second_editor.patch(f"/campaigns/{campaign}/markets/fr", json={"product_order": []},
                                    headers={"If-Match": etag})
        refused(stale, "the second save from the same read", "stale_version")
    assert market_of(owner, campaign, "fr")["product_order"] == order
    assert rendered() == [ids[2], ids[0], ids[1]], f"a partial order puts the listed product first: {rendered()}"
    restored = owner.patch(f"/campaigns/{campaign}/markets/fr", json={"product_order": []},
                           headers={"If-Match": first.headers["etag"]})
    ok(restored, "restoring the campaign order")
    assert rendered() == ids, f"an empty order restores the campaign order: {rendered()}"
    assert any(e["campaign_slug"] == campaign and e["decision"] == "permit"
               for e in audit_events(owner, action="market.update", limit=50))


def test_the_content_hash_ignores_status_and_other_markets(owner, campaign):
    """A status change alone or another market's edit never changes a market's content hash. cov: C-CF-187, C-CF-205, C-DM-27"""

    marker = token_hex(6)
    translate_market(owner, campaign, "fr", marker)
    translate_market(owner, campaign, "de", marker)
    french = market_of(owner, campaign, "fr")["content_hash"]
    german = market_of(owner, campaign, "de")["content_hash"]
    assert HEX64.match(french) and french != german
    ok(write_translation(owner, campaign, "fr", "shop.cta", probe_value("shop.cta", "fr", marker), "approved"), "status only")
    assert market_of(owner, campaign, "fr")["content_hash"] == french
    ok(write_translation(owner, campaign, "de", "shop.cta", f"Shop geändert {marker}", "reviewed"), "a de edit")
    assert market_of(owner, campaign, "fr")["content_hash"] == french
    assert market_of(owner, campaign, "de")["content_hash"] != german


def test_an_upload_is_stored_at_its_digest_key_in_the_object_store(owner, campaign, store, backend):
    """An upload lands in the bucket at its digest key once, with the digest recorded. cov: C-OV-08, C-CF-241, C-CF-245, C-CF-246, C-CF-247, C-CF-248, C-CF-249, C-CF-273, C-TR-05, C-DM-20, C-DC-22"""

    data = png_bytes()
    digest = sha256_hex(data)
    created = ok(upload(owner, campaign, data, "hero.png", "fr"), "uploading a market image")
    key = f"assets/{campaign}/fr/{digest}.png"
    assert created["object_key"] == key and created["checksum"] == digest, created
    assert created["byte_size"] == len(data) and created["content_type"] == "image/png", created
    assert store.exists(key), f"{key} must exist in the bucket"
    assert store_object(key) == data
    again = ok(upload(owner, campaign, data, "copy.png", "fr"), "uploading the same bytes")
    assert again["id"] == created["id"], (created, again)
    assert store.list(f"assets/{campaign}/") == [key]
    assert any(e["campaign_slug"] == campaign for e in audit_events(owner, action="asset.upload", limit=50))
    row = backend.query("SELECT checksum, object_key FROM assets WHERE id = %s", (created["id"],))
    assert row and row[0]["checksum"] == digest and row[0]["object_key"] == key, row
    for column in backend.query("SELECT column_name, data_type FROM information_schema.columns "
                                "WHERE table_schema = 'public' AND table_name = 'assets'"):
        assert column["data_type"] != "bytea", f"image bytes may not live in the database: {column}"


def test_an_image_of_a_market_that_is_not_live_is_not_public(owner, campaign, store):
    """A market image stays unreadable in public until that market is live, and again once unpublished. cov: C-OV-09, C-CF-251, C-CF-252, C-CF-253, C-CF-254, C-UF-08"""

    market_image = ok(upload(owner, campaign, png_bytes(), "market.png", "fr"), "a market image")
    shared_image = ok(upload(owner, campaign, png_bytes(), "shared.png"), "a shared image")
    for asset in (market_image, shared_image):
        absent(page_get(f"/media/{asset['id']}"), "an image before any market is live")
    live_market(owner, campaign, "fr", token_hex(6))
    for asset in (market_image, shared_image):
        served = page_get(f"/media/{asset['id']}")
        assert served.status_code == 200 and sha256_hex(served.content) == asset["checksum"], describe(served)
        assert served.headers.get("content-type", "").startswith("image/png")
    other = ok(upload(owner, campaign, png_bytes(), "german.png", "de"), "an image of a market that is not live")
    absent(page_get(f"/media/{other['id']}"), "the de image")
    ok(unpublish(owner, campaign, "fr"), "unpublishing fr")
    absent(page_get(f"/media/{market_image['id']}"), "the fr image after unpublish")
    absent(page_get(f"/media/{shared_image['id']}"), "the shared image with no live market")
    assert store.exists(market_image["object_key"])


def test_the_bucket_refuses_an_anonymous_read(owner, campaign):
    """The bucket refuses an anonymous read of a stored object. cov: C-OV-10, C-CF-250, C-TR-06"""

    asset = ok(upload(owner, campaign, png_bytes(), "private.png", "fr"), "an image")
    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    bucket = os.environ["STORAGE_BUCKET"]
    direct = httpx.get(f"{endpoint}/{bucket}/{asset['object_key']}", timeout=TIMEOUT)
    assert direct.status_code in (401, 403), describe(direct)
    listing = httpx.get(f"{endpoint}/{bucket}?list-type=2", timeout=TIMEOUT)
    assert listing.status_code in (401, 403), describe(listing)


def test_uploads_are_typed_by_their_bytes(owner, campaign):
    """Uploads are typed by their bytes: a renamed PNG is accepted, text and GIF are not. cov: C-CF-161, C-CF-242, C-CF-243, C-CF-244"""

    refused(upload(owner, campaign, b"plain text pretending", "fake.png", "fr"), "text named png", "unsupported_media")
    refused(upload(owner, campaign, b"GIF89a" + bytes(40), "anim.gif", "fr"), "a GIF", "unsupported_media")
    renamed = ok(upload(owner, campaign, png_bytes(), "notes.txt", "fr"), "PNG bytes named txt")
    assert renamed["content_type"] == "image/png" and renamed["object_key"].endswith(".png"), renamed
    too_big = upload(owner, campaign, png_bytes() + bytes(UPLOAD_LIMIT + 1), "huge.png", "fr")
    refused(too_big, "an image over 5 MB")
    with client_for(token_for(EDITOR)) as scoped:
        refused(upload(scoped, campaign, png_bytes(), "shared.png"), "an editor uploading a shared image")
        refused(upload(scoped, campaign, png_bytes(), "de.png", "de"), "an editor uploading for de", "market_out_of_scope")


def test_each_publish_stores_a_versioned_artifact_in_the_object_store(owner, campaign, store):
    """Each publish stores a JSON artifact at artifacts/campaign/market/version in the bucket. cov: C-OV-20, C-CF-256, C-CF-257, C-CF-258, C-DM-23, C-DC-18, C-DC-27"""

    marker = token_hex(6)
    live_market(owner, campaign, "fr", marker)
    state = market_of(owner, campaign, "fr")
    artifacts = rows(owner.get(f"/campaigns/{campaign}/markets/fr/artifacts"), "artifacts")
    assert len(artifacts) == 1, artifacts
    artifact = artifacts[0]
    assert artifact["object_key"] == f"artifacts/{campaign}/fr/1.json" and artifact["live"] is True, artifact
    assert artifact["content_hash"] == state["content_hash"], (artifact, state)
    assert artifact["published_by"] and artifact["published_at"], artifact
    stored = json.loads(store_object(artifact["object_key"]))
    assert stored["strings"]["hero.title"] == probe_value("hero.title", "fr", marker), stored.get("strings")
    assert store.list(f"artifacts/{campaign}/") == [f"artifacts/{campaign}/fr/1.json"]


def test_every_write_and_every_refusal_records_one_audit_event(owner, editor, campaign, backend):
    """One permitted write adds one permit event and one refused write adds one deny event. cov: C-OV-11, C-CF-140, C-CF-260, C-CF-261, C-CF-262, C-CF-263, C-CF-275, C-CF-286"""

    top = backend.query("SELECT coalesce(max(id), 0) AS n FROM audit_events")[0]["n"]
    written = write_translation(owner, campaign, "fr", "shop.cta", f"Boutique {token_hex(4)}", "draft")
    ok(written, "a permitted write")
    events = backend.query("SELECT * FROM audit_events WHERE id > %s ORDER BY id", (top,))
    assert len(events) == 1, events
    assert (events[0]["action"], events[0]["decision"], events[0]["actor_email"]) == ("translation.write", "permit", OWNER)
    assert events[0]["campaign_slug"] == campaign and events[0]["market_code"] == "fr", events[0]
    assert events[0]["request_id"] == written.headers.get(REQUEST_ID_HEADER), events[0]
    top = events[0]["id"]
    denied = write_translation(editor, campaign, "de", "shop.cta", "Kaufen", "draft")
    refused(denied, "an out-of-scope write", "market_out_of_scope")
    events = backend.query("SELECT * FROM audit_events WHERE id > %s ORDER BY id", (top,))
    assert len(events) == 1, events
    assert (events[0]["decision"], events[0]["reason"], events[0]["actor_email"]) == ("deny", "market_out_of_scope", EDITOR)
    assert events[0]["request_id"] == body(denied)["request_id"], events[0]
    assert events[0]["action"] in AUDIT_ACTIONS, events[0]
    tokens = [token_for(OWNER), token_for(EDITOR)]
    dump = json.dumps(backend.query("SELECT before, after, reason FROM audit_events ORDER BY id DESC LIMIT 500"), default=str)
    assert PASSWORD not in dump and not any(t in dump for t in tokens), "an audit event carries a credential"


def test_the_audit_chain_links_every_event_to_its_predecessor(owner, backend):
    """The audit chain starts at sixty-four zeros and every event names its predecessor's hash. cov: C-CF-276, C-CF-277, C-DM-55, C-DC-04"""

    events = backend.query("SELECT id, prev_hash, hash FROM audit_events ORDER BY id")
    assert len(events) > 10, "the seed must have written the audit log"
    assert events[0]["prev_hash"].strip() == ZERO_HASH
    for previous, current in zip(events, events[1:]):
        assert current["prev_hash"].strip() == previous["hash"].strip(), (previous["id"], current["id"])
        assert HEX64.match(current["hash"].strip()), current
    verified = ok(owner.get("/audit/verify"), "verifying the chain")
    assert verified["intact"] is True and verified["first_broken_id"] is None, verified
    assert verified["events"] >= len(events) and HEX64.match(verified["head"]), verified
    known = {row["hash"].strip() for row in backend.query("SELECT hash FROM audit_events")}
    assert verified["head"] in known, verified


def test_the_database_refuses_to_rewrite_audit_rows_for_the_app_role(backend):
    """The app's own database role cannot update or delete an audit row. cov: C-OV-12, C-CF-278, C-DM-24, C-DC-24"""

    app_role = capabilities.PostgresBackend(os.environ["DATABASE_URL"])
    top = backend.query("SELECT max(id) AS top FROM audit_events")[0]["top"]
    before = backend.query("SELECT count(*) AS n FROM audit_events")[0]["n"]
    for statement in ("UPDATE audit_events SET reason = 'rewritten' WHERE id = %s",
                      "DELETE FROM audit_events WHERE id = %s"):
        try:
            app_role.query(statement, (top,))
        except Exception as refusal:
            assert str(refusal), "the database refusal must carry a message"
        stored = backend.query("SELECT reason FROM audit_events WHERE id = %s", (top,))
        assert stored, f"the application role deleted audit row {top}"
        assert stored[0]["reason"] != "rewritten", f"the application role rewrote audit row {top}"
    assert backend.query("SELECT count(*) AS n FROM audit_events")[0]["n"] >= before


def test_verification_names_the_first_altered_audit_event(owner, campaign, backend):
    """A row altered outside the app breaks verification at exactly that event. cov: C-OV-22, C-CF-282, C-CF-283"""

    ok(write_translation(owner, campaign, "fr", "shop.cta", f"Boutique {token_hex(4)}", "draft"), "a fresh event")
    target = backend.query("SELECT id, reason FROM audit_events WHERE campaign_slug = %s ORDER BY id DESC LIMIT 1",
                           (campaign,))[0]

    def rewrite(value):
        literal = "NULL" if value is None else "'" + str(value).replace("'", "''") + "'"
        backend.query(
            "SET session_replication_role = replica; "
            "ALTER TABLE audit_events DISABLE TRIGGER ALL; "
            f"UPDATE audit_events SET reason = {literal} WHERE id = {int(target['id'])}; "
            "ALTER TABLE audit_events ENABLE TRIGGER ALL;")
    rewrite("tampered after the fact")
    try:
        broken = ok(owner.get("/audit/verify"), "verifying a tampered chain")
        assert broken["intact"] is False and broken["first_broken_id"] == target["id"], broken
    finally:
        rewrite(target["reason"])
    restored = ok(owner.get("/audit/verify"), "verifying the restored chain")
    assert restored["intact"] is True, restored


def test_audit_reads_are_scoped_to_the_reader_and_filtered(owner, editor, legal, merchandiser, campaign):
    """Legal reads only its own markets' events, others are refused, and filters narrow the owner's view. cov: C-RL-05, C-RL-15, C-CF-279, C-CF-280, C-CF-281"""

    refused(write_translation(editor, campaign, "be-fr", "shop.cta", "Achetez", "draft"),
            "an editor writing be-fr of the probe", "explicit_deny")
    translate_market(owner, campaign, "fr", token_hex(6))
    ok(submit(owner, campaign, "fr"), "submitting the probe fr")
    ok(approve(legal, campaign, "fr", "legal"), "legal approving the probe fr")
    for event in audit_events(legal, limit=200):
        assert event["market_code"] in ("fr", "en", "be-nl"), event
    refused(editor.get("/audit"), "an editor reading the audit log", "role_not_permitted")
    refused(merchandiser.get("/audit"), "a merchandiser reading the audit log", "role_not_permitted")
    refused(legal.get("/audit/verify"), "legal verifying the chain")
    narrowed = audit_events(owner, market="be-fr", decision="deny", limit=50)
    assert narrowed and all(e["market_code"] == "be-fr" and e["decision"] == "deny" for e in narrowed), narrowed
    assert any(e["reason"] == "explicit_deny" and e["actor_email"] == EDITOR and e["campaign_slug"] == campaign
               for e in narrowed), narrowed
    limited = audit_events(owner, limit=5)
    ids = [e["id"] for e in limited]
    assert len(limited) == 5 and ids == sorted(ids, reverse=True), ids
    by_actor = audit_events(owner, actor=LEGAL, action="approval.record", limit=20)
    assert by_actor and all(e["actor_email"] == LEGAL and e["action"] == "approval.record" for e in by_actor)
    assert any(e["campaign_slug"] == campaign for e in by_actor), by_actor


def test_an_audit_export_is_itself_audited(owner, legal):
    """An audit export returns CSV with a header row and records itself. cov: C-CF-284, C-CF-285"""

    exported = owner.post("/audit/exports", json={})
    assert exported.status_code in OK, describe(exported)
    assert "csv" in exported.headers.get("content-type", ""), exported.headers
    header = exported.text.splitlines()[0].lower()
    for column in ("id", "occurred_at", "actor_email", "action", "decision", "hash"):
        assert column in header, header
    newest = audit_events(owner, action="audit.export", limit=1)
    assert newest and newest[0]["actor_email"] == OWNER and newest[0]["decision"] == "permit", newest
    refused(legal.post("/audit/exports", json={}), "legal exporting the audit log")


def test_the_privacy_page_states_the_inventory_and_every_public_page_links_it():
    """The privacy page states retention for logs, the cookie and audit records and every public page links it. cov: C-CF-289, C-CF-290, C-CF-291, C-CF-295, C-UF-06"""

    privacy = visible_text(html_of("/privacy/"))
    for fact in PRIVACY_FACTS + ("third parties", "erasure"):
        assert fact.lower() in privacy.lower(), f"the privacy page must state {fact!r}"
    for region in DATA_REGIONS:
        assert region in privacy, f"the privacy page must name the residency region {region!r}"
    for route in ("/", f"/{AFTERGLOW}/fr/", f"/{AFTERGLOW}/en/", f"/{AFTERGLOW}/fr/mentions-legales/"):
        html = html_of(route)
        footer = html[html.lower().rfind("<footer"):] if "<footer" in html.lower() else html
        assert any(link_path(a.get("href", "")) == "/privacy/" for a in tags(footer, "a")), f"{route} footer lacks privacy"


def test_a_narrow_viewport_never_scrolls_sideways_and_keeps_navigation_reachable(page, narrow_page):
    """At a phone width nothing scrolls sideways and the menu, switcher and shop action stay reachable. cov: C-CF-299, C-CF-300, C-CF-301, C-CF-302, C-UX-40, C-UX-41, C-FE-01, C-FE-02"""

    for path in (f"/{AFTERGLOW}/fr/", f"/{AFTERGLOW}/fr/mentions-legales/", "/privacy/", "/", "/studio/login"):
        narrow_page.goto(f"{base_url()}{path}")
        narrow_page.wait_for_load_state("networkidle")
        overflow = narrow_page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        assert overflow <= 1, f"{path} scrolls sideways by {overflow}px"
    narrow_page.goto(f"{base_url()}/{AFTERGLOW}/fr/")
    assert narrow_page.locator("header button[aria-expanded]").first.is_visible()
    assert narrow_page.locator("select").first.is_visible()
    shop = narrow_page.evaluate("""(host) => [...document.querySelectorAll('a[href]')]
        .filter(a => a.href.includes(host) && a.href.includes('/c/'))
        .map(a => { const r = a.getBoundingClientRect(); const s = getComputedStyle(a);
                    return {visible: r.width > 0 && r.height > 0 && s.visibility !== 'hidden', top: r.top, bottom: r.bottom}; })
        .filter(b => b.visible)""", HOST["fr"])
    assert shop and any(b["bottom"] <= 844 and b["top"] >= 844 * 0.5 for b in shop), f"the shop action must float low: {shop}"
    tops = narrow_page.evaluate("() => [...document.querySelectorAll('[data-product]')].slice(0, 3)"
                                ".map(c => Math.round(c.getBoundingClientRect().top + window.scrollY))")
    assert len(tops) == 3 and tops[0] == tops[1] and tops[2] > tops[1], f"cards sit two across: {tops}"
    radius = narrow_page.evaluate("() => { const s = document.querySelector('[data-swatch]');"
                                  " const r = parseFloat(getComputedStyle(s).borderTopLeftRadius);"
                                  " const w = s.getBoundingClientRect().width; return {r, w}; }")
    circle = narrow_page.evaluate("() => { const s = document.querySelector('[data-swatch]');"
                                  " const st = getComputedStyle(s, '::before'); const own = getComputedStyle(s);"
                                  " return own.borderTopLeftRadius.includes('%') || parseFloat(own.borderTopLeftRadius) >= 8"
                                  " || [...s.querySelectorAll('*')].some(c => parseFloat(getComputedStyle(c).borderTopLeftRadius) >= 4); }")
    assert circle, f"swatches become circles at a narrow viewport: {radius}"
    copies = """(host) => { const all = [...document.querySelectorAll('a[href]')]
        .filter(a => a.href.includes(host) && a.href.includes('/c/'));
        const shown = all.filter(a => { const r = a.getBoundingClientRect(); const s = getComputedStyle(a);
            return r.width > 0 && r.height > 0 && s.visibility !== 'hidden'; });
        return {total: all.length, shown: shown.length, inBar: shown.filter(a => !!a.closest('header, [role=banner]')).length}; }"""
    narrow_copies = narrow_page.evaluate(copies, HOST["fr"])
    assert narrow_copies["total"] == 2 and narrow_copies["shown"] == 1, narrow_copies
    page.goto(f"{base_url()}/{AFTERGLOW}/fr/")
    page.wait_for_load_state("networkidle")
    wide_copies = page.evaluate(copies, HOST["fr"])
    assert wide_copies["total"] == 2 and wide_copies["shown"] == 1 and wide_copies["inBar"] == 1, wide_copies
    menu_button = narrow_page.locator("header button[aria-expanded]").first
    controls = menu_button.get_attribute("aria-controls")
    menu_button.click()
    narrow_page.wait_for_function("""id => { const el = document.getElementById(id);
        return !!el && el.getBoundingClientRect().height > 0; }""", arg=controls, timeout=5000)
    narrow_page.wait_for_timeout(600)
    menu_tops = narrow_page.evaluate("""id => [...document.getElementById(id).querySelectorAll('a[href*="#"]')]
        .map(a => Math.round(a.getBoundingClientRect().top))""", controls)
    assert len(menu_tops) == 4 and all(b > a for a, b in zip(menu_tops, menu_tops[1:])), \
        f"the menu list becomes a single column: {menu_tops}"
    narrow_page.keyboard.press("Escape")
    sign_in_page(narrow_page, OWNER)
    narrow_page.goto(f"{base_url()}/studio/campaigns/{AFTERGLOW}/")
    narrow_page.wait_for_load_state("networkidle")
    overflow = narrow_page.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
    assert overflow <= 1, f"the studio scrolls sideways by {overflow}px"
    for label in ("Campaigns", "Audit", "Grants"):
        link = narrow_page.get_by_role("link", name=label, exact=True).first
        link.scroll_into_view_if_needed()
        assert link.is_visible(), f"the studio navigation link {label} must stay reachable"


def test_studio_forms_mark_invalid_fields_inline_and_write_nothing(owner, page):
    """A studio form marks the invalid field inline and writes nothing. cov: C-CF-296, C-CF-297, C-FE-28, C-FE-29, C-FE-30"""

    page.goto(f"{base_url()}/studio/login")
    page.get_by_label("Email", exact=True).fill(OWNER)
    page.get_by_role("button", name="Sign in", exact=True).click()
    password = page.get_by_label("Password", exact=True)
    page.wait_for_function("el => el.getAttribute('aria-invalid') === 'true'",
                           arg=password.element_handle(), timeout=5000)
    assert "/studio/login" in page.url
    before = len(rows(owner.get("/grants"), "grants"))
    sign_in_page(page, OWNER)
    page.goto(f"{base_url()}/studio/grants/")
    page.get_by_role("button", name="Add", exact=True).first.click()
    page.get_by_label("Email", exact=True).last.fill(EDITOR3)
    assert page.get_by_label("Role", exact=True).count() >= 1 and page.get_by_label("Market", exact=True).count() >= 1
    expires = page.get_by_label("Expires", exact=True).last
    kind = expires.evaluate("el => el.type")
    stamp = iso_in(3 * 86400)
    expires.fill(stamp[:10] if kind == "date" else stamp[:16] if kind == "datetime-local" else stamp)
    page.get_by_role("button", name="Save", exact=True).last.click()
    reason = page.get_by_label("Reason", exact=True).last
    page.wait_for_function("el => el.getAttribute('aria-invalid') === 'true'",
                           arg=reason.element_handle(), timeout=5000)
    assert page.get_by_text(re.compile("reason", re.I)).count() >= 2, "a message beside the field names Reason"
    assert len(rows(owner.get("/grants"), "grants")) == before


def test_security_headers_ride_on_every_response():
    """Nosniff, the referrer policy, the permissions policy and a strict content policy ride on every response. cov: C-TR-11, C-TR-12, C-TR-13, C-TR-14, C-TR-15"""

    for path in (f"/{AFTERGLOW}/fr/", "/api/health", "/studio/login", "/api/v1/campaigns", "/privacy/"):
        response = page_get(path)
        headers = {k.lower(): v for k, v in response.headers.items()}
        assert headers.get("x-content-type-options", "").lower() == "nosniff", (path, headers)
        assert headers.get("referrer-policy", "").lower() == REFERRER_POLICY, (path, headers)
        permissions = headers.get("permissions-policy", "").replace(" ", "").lower()
        for feature in ("camera=()", "microphone=()", "geolocation=()", "payment=()"):
            assert feature in permissions, (path, permissions)
        policy = headers.get("content-security-policy", "")
        directives = {d.strip().split(" ")[0]: d.strip() for d in policy.split(";") if d.strip()}
        script = directives.get("script-src", directives.get("default-src", ""))
        assert script and "'unsafe-inline'" not in script, (path, policy)
        assert "'none'" in directives.get("frame-ancestors", ""), (path, policy)
        assert "'self'" in directives.get("base-uri", "") and "'self'" in directives.get("form-action", ""), (path, policy)


def test_live_pages_carry_shared_cache_headers_without_varying_on_cookie():
    """A live page and a legal notice carry the shared cache policy and never vary on Cookie. cov: C-TR-16, C-TR-17"""

    for path in (f"/{AFTERGLOW}/fr/", f"/{AFTERGLOW}/en/legal-notice/"):
        response = page_get(path)
        assert response.status_code == 200, describe(response)
        cache = response.headers.get("cache-control", "").replace(" ", "").lower()
        for part in CACHE_PARTS:
            assert part in cache.split(","), (path, cache)
        vary = [v.strip().lower() for v in response.headers.get("vary", "").split(",")]
        assert "accept-encoding" in vary and "cookie" not in vary, (path, vary)


def test_a_public_page_requests_nothing_from_another_host(page):
    """Loading a drop page requests nothing from any other host. cov: C-OV-24, C-CF-307, C-TR-19, C-CN-05"""

    requested = []
    page.on("request", lambda request: requested.append(request.url))
    page.goto(f"{base_url()}/{AFTERGLOW}/fr/")
    page.wait_for_load_state("networkidle")
    page.mouse.wheel(0, 6000)
    page.wait_for_timeout(1500)
    own = urlparse(base_url()).netloc
    foreign = [url for url in requested if urlparse(url).scheme in ("http", "https") and urlparse(url).netloc != own]
    assert requested and foreign == [], f"requests to other hosts: {foreign}"


def test_no_secret_reaches_anything_the_browser_downloads():
    """No database address, object store key or other token reaches anything the browser fetches. cov: C-TR-24"""

    secrets = [os.environ.get("STORAGE_SECRET_KEY", ""), os.environ.get("STORAGE_ACCESS_KEY", "")]
    database = urlparse(os.environ.get("DATABASE_URL", ""))
    secrets += [database.password or "", os.environ.get("DATABASE_URL", "")]
    secrets = [s for s in secrets if len(s) >= 6]
    html = html_of(f"/{AFTERGLOW}/fr/")
    fetched = [html, json.dumps(public_payload(AFTERGLOW, "fr")), html_of("/studio/login")]
    for tag, attr in (("script", "src"), ("link", "href")):
        for attrs in tags(html, tag):
            ref = attrs.get(attr, "")
            if ref.startswith("/") and not ref.startswith("//"):
                fetched.append(page_get(ref).text)
    assert secrets, "the verifier must know the credentials it looks for"
    for blob in fetched:
        for secret in secrets:
            assert secret not in blob, "a credential reached a browser-fetchable response"


def test_an_anonymous_studio_request_is_sent_to_sign_in_with_next():
    """An anonymous studio request goes to sign-in carrying next, and a slashless address redirects permanently. cov: C-RL-04, C-UF-01, C-UF-10, C-UF-18, C-UF-23, C-TR-07"""

    response = page_get(f"/studio/campaigns/{AFTERGLOW}/", follow_redirects=False)
    assert 300 <= response.status_code < 400, describe(response)
    location = urlparse(response.headers["location"])
    assert location.path == "/studio/login", response.headers["location"]
    assert parse_qs(location.query).get("next") == [f"/studio/campaigns/{AFTERGLOW}/"], response.headers["location"]
    slashless = page_get(f"/{AFTERGLOW}/fr", follow_redirects=False)
    assert slashless.status_code in (301, 308) and link_path(slashless.headers["location"]) == f"/{AFTERGLOW}/fr/", describe(slashless)


def test_the_typeface_is_roboto_flex_at_the_pinned_heading_sizes(page, narrow_page):
    """The drop page sets Roboto Flex at the pinned heading, body and narrow-layout sizes. cov: C-UX-16, C-UX-17, C-UX-18, C-UX-19, C-UX-20"""

    probe = """() => {
        const read = sel => { const el = document.querySelector(sel); if (!el) return null;
            const s = getComputedStyle(el); return {family: s.fontFamily, size: s.fontSize, line: s.lineHeight}; };
        return {h1: read('main h1'), h2: read('main section#collection h2'), p: read('main section#ardenne p')};
    }"""
    page.goto(f"{base_url()}/{AFTERGLOW}/en/")
    page.wait_for_load_state("networkidle")
    wide = page.evaluate(probe)
    for role in ("h1", "h2", "p"):
        assert wide[role], (role, wide)
        first = wide[role]["family"].split(",")[0].strip().strip("'\"")
        assert first == TYPEFACE, (role, wide[role])
    def px(value):
        return float(str(value).replace("px", "")) if str(value).endswith("px") else -1.0

    def near(pair, size, line):
        return abs(px(pair["size"]) - px(size)) <= 0.5 and abs(px(pair["line"]) - px(line)) <= 0.5
    assert near(wide["h1"], H1_WIDE, "52px") and near(wide["h2"], H2_WIDE, "64px"), wide
    assert near(wide["p"], BODY_SIZE, "24px"), wide
    narrow_page.goto(f"{base_url()}/{AFTERGLOW}/en/")
    narrow_page.wait_for_load_state("networkidle")
    narrow = narrow_page.evaluate(probe)
    assert near(narrow["h1"], "32px", "36px") and near(narrow["h2"], "36px", "40px"), narrow


def test_money_and_time_are_returned_in_their_pinned_forms(owner):
    """Money comes back as integer minor units with uppercase codes and times as UTC with a Z. cov: C-TR-21, C-TR-23"""

    for product in rows(owner.get(f"/campaigns/{AFTERGLOW}/products"), "Afterglow products"):
        for market in product["markets"]:
            if market["price_minor"] is not None:
                assert isinstance(market["price_minor"], int) and market["price_currency"] == market["price_currency"].upper()
    french = market_of(owner, AFTERGLOW, "fr")
    for approval in french["approvals"]:
        assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$", approval["decided_at"]), approval
    for event in audit_events(owner, limit=10):
        assert event["occurred_at"].endswith("Z"), event


def test_text_meets_the_contrast_bar_against_its_ground(page):
    """Headings, paragraphs and prices meet the WCAG AA contrast bar against the ground behind them. cov: C-UX-34"""

    for path in (f"/{AFTERGLOW}/fr/", "/privacy/", "/studio/login"):
        page.goto(f"{base_url()}{path}")
        page.wait_for_load_state("networkidle")
        pairs = page.evaluate("""() => {
            const rgb = v => (v.match(/[0-9.]+/g) || []).map(Number);
            const ground = el => { for (let n = el; n; n = n.parentElement) {
                const c = rgb(getComputedStyle(n).backgroundColor);
                if (c.length >= 3 && (c.length < 4 || c[3] > 0.5)) return c.slice(0, 3); }
                return [255, 255, 255]; };
            return [...document.querySelectorAll('h1, h2, p, label, [data-price]')]
                .filter(el => el.offsetParent !== null && el.textContent.trim())
                .map(el => ({text: el.textContent.trim().slice(0, 40), fg: rgb(getComputedStyle(el).color).slice(0, 3),
                             bg: ground(el), size: parseFloat(getComputedStyle(el).fontSize)}));
        }""")
        assert pairs, f"{path} must carry visible text"
        for pair in pairs:
            ratio = contrast_ratio(tuple(pair["fg"]), tuple(pair["bg"]))
            floor = 3.0 if pair["size"] >= 24 else 4.5
            assert ratio >= floor, f"{path}: {pair['text']!r} contrast {ratio:.2f} below {floor}"


def test_the_seeded_copy_of_every_market_matches_the_copy_deck(owner):
    """The seeded translations of both campaigns hold the pinned copy deck values and statuses. cov: C-CF-113, C-CF-114, C-CF-116, C-CF-177, C-DM-34, C-DM-35, C-DM-36, C-DM-37, C-DM-38, C-DM-39, C-DM-40, C-DM-41, C-DM-42, C-DM-44, C-DM-45, C-DM-46, C-DM-47, C-DM-48, C-DM-49, C-DM-50, C-DM-52, C-DM-53, C-DM-54, C-DC-01"""

    for (campaign_slug, market), expected in SEED_COPY.items():
        stored = translations_of(owner, campaign_slug, market)
        for key, value in expected.items():
            assert key in stored, f"{campaign_slug} {market} lacks {key}"
            assert stored[key]["value"] == value, (campaign_slug, market, key, stored[key]["value"])
    afterglow_keys = {row["key"] for row in rows(owner.get(f"/campaigns/{AFTERGLOW}/strings"), "Afterglow strings")}
    assert len(afterglow_keys) == 30, sorted(afterglow_keys)
    dusk_keys = {row["key"] for row in rows(owner.get(f"/campaigns/{DUSK_PARADE}/strings"), "Dusk Parade strings")}
    assert len(dusk_keys) == 13, sorted(dusk_keys)
    french = translations_of(owner, AFTERGLOW, "fr")
    assert {row["status"] for row in french.values()} == {"approved"}, french
    assert translations_of(owner, DUSK_PARADE, "be-nl")["hero.title"]["value"] == DUSK_HERO_BE_NL
    assert translations_of(owner, DUSK_PARADE, "fr") == {}


def test_the_seeded_markets_hold_the_locale_matrix_once(owner, backend):
    """The seeded market rows hold the locale matrix exactly once, with no duplicate seed rows. cov: C-CF-46, C-CF-47, C-CF-48, C-CF-49, C-CF-50, C-CF-51, C-CF-52, C-TR-25, C-TR-26, C-DM-04, C-DM-05, C-DM-43"""

    markets = backend.query("SELECT code, hreflang, display_name, currency, locale_tag, commerce_host, "
                            "commerce_locale_segment, legal_page_slug, data_region FROM markets ORDER BY sort_order")
    got = [(m["code"], m["hreflang"], m["display_name"], m["currency"].strip(), m["locale_tag"], m["commerce_host"],
            m["commerce_locale_segment"] or "", m["legal_page_slug"], m["data_region"]) for m in markets]
    assert got == SEED_MARKETS, got
    for table, where in (("campaigns", "slug = 'afterglow'"), ("campaigns", "slug = 'dusk-parade'")):
        assert backend.query(f"SELECT count(*) AS n FROM {table} WHERE {where}")[0]["n"] == 1, table
    counts = backend.query("SELECT count(*) AS n FROM products p JOIN campaigns c ON c.id = p.campaign_id "
                           "WHERE c.slug IN ('afterglow', 'dusk-parade')")
    assert counts[0]["n"] == 5, counts
    strings = backend.query("SELECT c.slug, s.key, count(*) AS n FROM translatable_strings s JOIN campaigns c "
                            "ON c.id = s.campaign_id WHERE c.slug = 'afterglow' GROUP BY c.slug, s.key HAVING count(*) > 1")
    assert strings == [], strings
    dusk = next(c for c in rows(owner.get("/campaigns"), "campaigns") if c["slug"] == DUSK_PARADE)
    assert dusk["default_locale"] == "be-nl" and not dusk.get("embargo_at"), dusk
    products = rows(owner.get(f"/campaigns/{DUSK_PARADE}/products"), "Dusk Parade products")
    assert [p["commerce_product_id"] for p in products] == [DUSK_PRODUCT], products
    assert [(c["model_code"], c["attribution_slot"]) for c in products[0]["colourways"]] == [("7311550", "p1")], products
    available = {m["market_code"]: (m["price_minor"], m["price_currency"]) for m in products[0]["markets"] if m["available"]}
    assert available == {"be-nl": (6500, "EUR"), "de": (6500, "EUR")}, available
    sections = backend.query("SELECT s.kind, s.anchor FROM page_sections s JOIN campaigns c ON c.id = s.campaign_id "
                             "WHERE c.slug = %s ORDER BY s.sort_order", (DUSK_PARADE,))
    assert [s["kind"] for s in sections] == ["hero", "collection", "footer_list", "legal_footer"], sections
    budgets = {row["key"]: row["max_length"] for row in rows(owner.get(f"/campaigns/{AFTERGLOW}/strings"), "strings")}
    for key, limit in SEED_BUDGETS.items():
        assert budgets.get(key) == limit, (key, budgets.get(key))


def test_the_seeded_staff_grants_and_media_match_the_seed(owner, store):
    """The seeded staff, their grants and the Afterglow media inventory match the pinned seed. cov: C-RL-23, C-RL-24, C-RL-26, C-RL-27, C-RL-28, C-RL-29, C-RL-30, C-RL-31, C-RL-32, C-DM-31, C-DM-32"""

    directory = {row["email"]: row["display_name"] for row in rows(owner.get("/principals"), "directory")}
    for email, name in SEED_PEOPLE.items():
        assert directory.get(email) == name, (email, directory.get(email))
    grants = rows(owner.get("/grants"), "grants")
    agency = [g for g in grants if g["email"] == EDITOR2 and g["market_code"] == "de"]
    assert agency and agency[0]["reason"] == AGENCY_REASON and agency[0]["expires_at"], agency
    live = [g for g in grants if not g.get("revoked_at") and g["effect"] == "permit"]
    for email, (role, markets) in SEED_GRANTS.items():
        held = {g["market_code"] for g in live if g["email"] == email and g["role"] == role}
        assert held == set(markets), (email, held)
    assert not [g for g in live if g["email"] == EDITOR3], "editor3 holds no grant in the seed"
    denies = [g for g in grants if g["email"] == EDITOR and g["effect"] == "deny"]
    assert [g["market_code"] for g in denies] == ["be-fr"], denies
    keys = store.list(f"assets/{AFTERGLOW}/")
    shared = [k for k in keys if k.startswith(f"assets/{AFTERGLOW}/shared/")]
    per_market = {m: [k for k in keys if k.startswith(f"assets/{AFTERGLOW}/{m}/")] for m in MARKETS}
    assert len(shared) >= 4, shared
    assert all(per_market[m] for m in MARKETS), per_market
    assert all(re.search(r"/[0-9a-f]{64}\.png$", k) for k in keys), keys


def test_each_role_outside_its_writable_set_is_refused_by_role(owner, editor, legal, merchandiser, translator, campaign):
    """Each role outside its writable set is refused by role and the protected state is unchanged. cov: C-RL-18, C-RL-19, C-RL-20, C-RL-21"""

    translate_market(owner, campaign, "fr", token_hex(6))
    ok(submit(owner, campaign, "fr"), "submitting the probe fr")
    refused(approve(editor, campaign, "fr", "legal"), "an editor approving", "role_not_permitted")
    refused(publish(editor, campaign, "fr"), "an editor publishing", "role_not_permitted")
    refused(publish(legal, campaign, "fr"), "legal publishing", "role_not_permitted")
    refused(rollback(editor, campaign, "fr"), "an editor rolling back", "role_not_permitted")
    for session, who in ((legal, "legal"), (merchandiser, "a merchandiser")):
        attempt = write_translation(session, campaign, "fr", "shop.cta", "Boutique", "draft")
        refused(attempt, f"{who} writing copy")
        assert reason_of(attempt) in ("role_not_permitted", "field_not_permitted"), describe(attempt)
    refused(translator.post("/grants", json={"email": EDITOR3, "role": "editor", "market_code": "de",
                                             "expires_at": iso_in(86400), "reason": "probe"}),
            "a translator issuing a grant", "role_not_permitted")
    refused(editor.get("/audit/verify"), "an editor verifying the audit chain")
    state = market_of(owner, campaign, "fr")
    assert state["status"] == "in_review" and state["approvals"] == [] and state["live_version"] is None, state


def test_the_fixed_bar_holds_on_scroll_and_a_dark_preference_changes_nothing(page):
    """The fixed bar keeps its size and ground while the page scrolls, and a dark preference changes nothing. cov: C-UX-31, C-UX-32"""

    page.goto(f"{base_url()}/{AFTERGLOW}/en/")
    page.wait_for_load_state("networkidle")
    probe = "() => { const h = document.querySelector('header') || document.querySelector('[role=banner]');" \
            " const r = h.getBoundingClientRect(); const s = getComputedStyle(h);" \
            " return {top: Math.round(r.top), height: Math.round(r.height), ground: s.backgroundColor, ink: s.color," \
            " visible: getComputedStyle(h).visibility !== 'hidden' && getComputedStyle(h).opacity !== '0'}; }"
    ground = "() => getComputedStyle(document.body).backgroundColor"
    light = page.evaluate(ground)
    before = page.evaluate(probe)
    page.mouse.wheel(0, 4000)
    page.wait_for_timeout(1200)
    after = page.evaluate(probe)
    assert before["visible"] and after["visible"] and after["top"] == before["top"], (before, after)
    assert abs(after["height"] - before["height"]) <= 1, (before, after)
    assert (after["ground"], after["ink"]) == (before["ground"], before["ink"]), f"the bar never inverts: {before} {after}"
    context = page.context.browser.new_context(viewport={"width": 1440, "height": 900}, color_scheme="dark")
    dark_page = context.new_page()
    dark_page.goto(f"{base_url()}/{AFTERGLOW}/en/")
    dark_page.wait_for_load_state("networkidle")
    dark = dark_page.evaluate(ground)
    context.close()
    assert parse_colour(dark) == parse_colour(light), f"no dark scheme: light {light}, dark {dark}"
