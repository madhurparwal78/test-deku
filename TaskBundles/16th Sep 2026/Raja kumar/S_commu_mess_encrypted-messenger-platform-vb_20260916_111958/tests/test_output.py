"""Observations for deku/encrypted-messenger-platform-vb.

One module, grouped by the concern each test observes: core features, data integrity,
authorization, edge cases, and the email slot. Every test creates its own accounts and
reads the app only through HTTP, the rendered page, the database adapter and the inbox.
"""

from __future__ import annotations

import base64
import json
import os
import re
import time

from conftest import (
    COPY_DECK,
    DECLARED_PAGES,
    DECRYPT_NOTICE,
    DESKTOP,
    FULL_HD,
    LAPTOP,
    TABLET,
    EMPTY_CHATS,
    FONT_STACK,
    FOOTER_COLUMNS,
    FOUNDATION,
    GROUP_UNAVAILABLE,
    HERO_LEAD,
    LANGUAGE_NAMES,
    LOCALES,
    MAIL_FROM,
    NUDGE_BODY,
    NUDGE_SUBJECT,
    PHONE,
    PRIVACY_TABLE,
    PUBLIC_ROUTES,
    RECEIPT_SUBJECT,
    SEED_ACCOUNTS,
    SEEDED_PASSWORD,
    STATUSES,
    TOP_BAR_LINKS,
    UNLINKED_BANNER,
    Person,
    account_token,
    ack,
    all_row_text,
    b64,
    bearer,
    body_of,
    bubble,
    bubble_status,
    bundle,
    by_testid,
    client,
    contrast_ratio,
    relative_luminance,
    create_group,
    decoded_blobs,
    device_send,
    document_text,
    entry,
    element_colours,
    ensure_unlocked,
    hue_chroma,
    ok,
    path_of,
    visible_testid,
    fetch,
    fresh_account,
    group_send,
    guids_of,
    is_client_error,
    key_material,
    leaks,
    leaks_bytes,
    login,
    mail_text,
    mails_to,
    make_png,
    message_texts,
    new_email,
    new_guid,
    new_username,
    normalise_quotes,
    open_chat,
    parse_rgb,
    patch_group,
    pump,
    put_requests_to,
    random_ciphertext,
    read_group,
    register_device,
    register_device_raw,
    restore,
    root_attribute,
    route_messages,
    rows_containing,
    rows_holding,
    run_together,
    safety_digits,
    same_origin,
    sealed_send,
    send_text,
    sent_ciphertexts,
    sent_guids,
    settle,
    signup,
    squash,
    storage_dump,
    style_of_text,
    tampered,
    token_hex,
    transition_seconds,
    ui_login,
    ui_set_profile_name,
    url_path,
    wait_for_mail,
    wait_sent,
    wait_until,
)
from appclient import app_url


def _post_donation(key, body):
    headers = {"Idempotency-Key": key} if key else {}
    with client(headers) as c:
        return c.post("/api/donations", json=body)


def _donation_rows(backend, email):
    return backend.query("SELECT amount_minor, currency, email FROM donations WHERE lower(email) = lower(%s)", (email,))


def _addresses(people):
    return sorted(p.get("Address", "").lower() for p in (people or []))


def test_home_documents_arrive_prerendered_with_lang_and_direction():
    """The marketing documents arrive complete before any script runs, declaring language and direction."""
    with client(follow=True) as c:
        health = c.get("/api/health")
        assert health.status_code == 200, f"GET /api/health returned {health.status_code}: {body_of(health)}"
        home = c.get("/")
        assert home.status_code == 200, f"GET / returned {home.status_code}"
        text = document_text(home.text)
        for needle in ("Speak Freely", squash(HERO_LEAD), "Get Beacon"):
            assert needle in text, f"raw HTML of / lacks {needle!r} before scripts run: {text[:300]!r}"
        assert root_attribute(home.text, "lang") == "en", f"root element of / declares lang={root_attribute(home.text, 'lang')!r}"
        assert "brandNavbar" in home.text, "raw HTML of / carries no #brandNavbar top bar"
        assert "/@vite/client" not in home.text, "GET / is served by a development server"
        for code in LOCALES:
            r = c.get(f"/{code}")
            assert r.status_code == 200, f"GET /{code} returned {r.status_code}"
            assert root_attribute(r.text, "lang") == code, f"/{code} declares lang={root_attribute(r.text, 'lang')!r}"
            assert "brandNavbar" in r.text, f"raw HTML of /{code} is not a complete prerendered document"
            assert len(document_text(r.text)) > 400, f"raw HTML of /{code} carries almost no text before scripts run"
            if code == "ar":
                assert root_attribute(r.text, "dir") == "rtl", f"/ar declares dir={root_attribute(r.text, 'dir')!r}"
        for path in DECLARED_PAGES + ("/donate", "/terms"):
            r = c.get(path)
            assert r.status_code == 200, f"GET {path} returned {r.status_code}"
            assert "brandNavbar" in r.text, f"raw HTML of {path} carries no prerendered top bar"
            assert root_attribute(r.text, "lang") == "en", f"{path} declares lang={root_attribute(r.text, 'lang')!r}"
            assert "/terms" in r.text, f"raw HTML of {path} carries no footer link to /terms"
        store_page = document_text(c.get("/get").text)
        for platform in ("Android", "iPhone", "iPad", "Windows", "Mac", "Linux"):
            assert platform in store_page, f"/get names no {platform} download"


def test_marketing_pages_request_nothing_from_other_origins(page):
    """Loading the marketing pages requests nothing from another origin and no raster image files."""
    seen = []
    page.on("request", lambda request: seen.append(request.url))
    for path in ("/", "/de", "/donate", "/terms"):
        page.goto(path, wait_until="networkidle")
    foreign = [u for u in seen if not u.startswith(("data:", "blob:")) and not same_origin(u, app_url())]
    assert not foreign, f"marketing pages requested other origins: {foreign[:5]}"
    raster = [u for u in seen if re.search(r"\.(png|jpe?g|gif|webp|avif)(\?|$)", u, re.I) and "favicon" not in u]
    assert not raster, f"the home loads raster image files: {raster[:5]}"


def test_home_copy_deck_strings_render_exactly(page):
    """Every copy deck string renders on the English home with plain hyphens and the top bar in order."""
    page.goto("/", wait_until="networkidle")
    text = squash(page.evaluate("() => document.body.textContent"))
    missing = [s for s in COPY_DECK if s != "Select your language" and squash(normalise_quotes(s)) not in squash(normalise_quotes(text))]
    assert not missing, f"copy deck strings missing from /: {missing[:3]}"
    assert "–" not in text and "—" not in text, "the English home text carries a typographic dash"
    control = by_testid(page, "language-control").first
    assert "English" in control.inner_text(), f"language control reads {control.inner_text()!r} on /"
    tops = [style_of_text(page, needle)["top"] for needle in ("Speak Freely", "Why use Beacon?", "Share Without Insecurity", "Say Anything", "No ads. No trackers. No kidding.", "Free for Everyone")]
    assert tops == sorted(tops), f"home sections run out of order: {tops}"
    assert style_of_text(page, "Why use Beacon?")["textAlign"] in ("center", "-webkit-center"), "the Why use Beacon? heading is not centred"
    assert style_of_text(page, "No ads. No trackers. No kidding.")["textAlign"] in ("left", "start"), "the no-tracking heading is not left-aligned"
    bar = parse_rgb(page.evaluate("() => { const x = document.createElement('canvas').getContext('2d'); x.fillStyle = getComputedStyle(document.getElementById('brandNavbar')).backgroundColor; x.fillRect(0, 0, 1, 1); const d = x.getImageData(0, 0, 1, 1).data; return 'rgba(' + d[0] + ',' + d[1] + ',' + d[2] + ',' + d[3] / 255 + ')'; }"))
    assert bar[3] > 0.9 and relative_luminance(bar) > 0.9, f"the top bar ground is {bar}, not white"
    anchors = [squash(t) for t in page.locator("#brandNavbar a").all_inner_texts()]
    order = [t for t in anchors if t in TOP_BAR_LINKS]
    assert order[:len(TOP_BAR_LINKS)] == list(TOP_BAR_LINKS), f"top bar links read {order}"
    for heading, entries in FOOTER_COLUMNS.items():
        assert heading.lower() in text.lower(), f"footer column heading {heading!r} missing"
        for label in entries:
            assert page.get_by_text(label, exact=True).count() > 0, f"footer item {label!r} missing"
    control.click()
    dialog = by_testid(page, "language-dialog")
    dialog.wait_for(state="visible")
    assert "Select your language" in dialog.inner_text(), "language dialog title missing"
    page.keyboard.press("Escape")
    page.get_by_text("Donate to Beacon", exact=True).first.click()
    assert wait_until(lambda: url_path(page.url) == "/donate", 15), f"Donate to Beacon led to {page.url}"


def test_type_scale_phone_tilt_and_self_hosted_fonts(browser_page):
    """Type sizes, the Inter stack with swap, the tilted phones, reserved space and the scroll shadow."""
    context, _ = browser_page.open(DESKTOP)
    tab = context.new_page()
    tab.goto("/", wait_until="domcontentloaded")
    early = [by_testid(tab, "hero-phone").nth(i).bounding_box() for i in range(by_testid(tab, "hero-phone").count())]
    tab.wait_for_load_state("networkidle")
    settle(1.5)
    phones = by_testid(tab, "hero-phone")
    assert phones.count() == 2, f"expected two hero-phone elements, found {phones.count()}"
    late = [phones.nth(i).bounding_box() for i in range(2)]
    assert len(early) == 2 and all(e and l and abs(e["width"] - l["width"]) < 4 and abs(e["height"] - l["height"]) < 4
                                   for e, l in zip(early, late)), f"phone renders changed size while loading: {early} -> {late}"
    for i in range(2):
        matrix = phones.nth(i).evaluate("e => getComputedStyle(e).transform")
        nums = [float(x) for x in re.findall(r"-?[\d.]+(?:e-?\d+)?", matrix)[:4]]
        assert len(nums) == 4 and abs(nums[0] - 0.92388) < 0.003 and abs(nums[1] - 0.382683) < 0.003 \
            and abs(nums[2] + 0.382683) < 0.003 and abs(nums[3] - 0.92388) < 0.003, f"hero-phone {i} transform is {matrix}"
    body_family = tab.evaluate("() => getComputedStyle(document.body).fontFamily")
    family = [p.strip().strip("'\"") for p in body_family.split(",")]
    assert family == [p.strip() for p in FONT_STACK.split(",")], f"body font stack is {body_family}"
    expected = {
        "Speak Freely": ("60px", "800", "64px"),
        "Why use Beacon?": ("40px", "800", "44px"),
        "No ads. No trackers. No kidding.": ("40px", "800", "44px"),
        "Say Anything": ("20px", "600", "28px"),
        "a different messaging experience": ("20px", "400", "28px"),
    }
    for needle, (size, weight, line) in expected.items():
        style = style_of_text(tab, needle)
        assert style, f"no rendered element carries {needle!r}"
        assert (style["fontSize"], style["fontWeight"], style["lineHeight"]) == (size, weight, line), (
            f"{needle!r} renders {style['fontSize']} {style['fontWeight']} {style['lineHeight']}")
        assert style["fontFamily"].strip("'\" ").startswith("Inter"), f"{needle!r} renders in {style['fontFamily']}"
    body = style_of_text(tab, "Share text, voice messages")
    assert body and (body["fontSize"], body["fontWeight"]) == ("16px", "400"), f"card body renders {body}"
    assert body["lineHeight"] == "24px", f"card body line height is {body['lineHeight']}"
    button = tab.locator(".get-app").first.evaluate("e => [getComputedStyle(e).fontSize, getComputedStyle(e).fontWeight, getComputedStyle(e).lineHeight]")
    assert button == ["16px", "600", "22px"], f".get-app renders {button}"
    base = tab.evaluate("() => { const cs = getComputedStyle(document.body); return [cs.fontSize, cs.fontWeight, cs.lineHeight, cs.textRendering]; }")
    assert base == ["16px", "400", "24px", "optimizelegibility"] or base == ["16px", "400", "24px", "optimizeLegibility"], f"body text renders {base}"
    wordmark = tab.locator("#brandNavbar").get_by_text("Beacon", exact=True).first.evaluate("e => getComputedStyle(e).fontWeight")
    assert wordmark == "800", f"the wordmark renders at weight {wordmark}"
    a, b = late
    assert a["x"] < b["x"] + b["width"] and b["x"] < a["x"] + a["width"] and a["y"] < b["y"] + b["height"] and b["y"] < a["y"] + a["height"], \
        f"the two hero phones do not overlap: {late}"
    faces = tab.evaluate("() => Array.from(document.fonts).map(f => [f.family.replace(/[\"']/g, ''), String(f.weight), f.display])")
    inter = [f for f in faces if f[0] == "Inter"]
    weights = {f[1] for f in inter}
    assert {"400", "500", "600", "800"} <= weights, f"Inter faces declared: {sorted(weights)}"
    assert all(f[2] == "swap" for f in inter), f"Inter faces without swap: {[f for f in inter if f[2] != 'swap'][:3]}"
    navbar = tab.locator("#brandNavbar")
    assert navbar.evaluate("e => getComputedStyle(e).position") in ("sticky", "fixed"), "#brandNavbar is not sticky"
    assert navbar.evaluate("e => getComputedStyle(e).boxShadow") == "none", "#brandNavbar carries a shadow before scrolling"
    tab.evaluate("() => window.scrollTo(0, 800)")
    assert wait_until(lambda: navbar.evaluate("e => getComputedStyle(e).boxShadow") != "none", 5), "#brandNavbar gains no shadow after scrolling"
    phone_context, _ = browser_page.open(PHONE)
    small = phone_context.new_page()
    small.goto("/", wait_until="networkidle")
    headline = style_of_text(small, "Speak Freely")
    assert headline and (headline["fontSize"], headline["lineHeight"]) == ("28px", "32px"), f"phone hero headline renders {headline}"


def test_language_dialog_traps_focus_and_restores_control(page):
    """The language dialog lists twelve languages, keeps focus inside and returns it to the control."""
    page.goto("/", wait_until="networkidle")
    control = by_testid(page, "language-control")
    control.focus()
    page.keyboard.press("Enter")
    dialog = by_testid(page, "language-dialog")
    dialog.wait_for(state="visible")
    assert dialog.get_attribute("role") == "dialog", "language dialog lacks role=dialog"
    assert dialog.get_attribute("aria-modal") == "true", "language dialog lacks aria-modal=true"
    assert "Select your language" in dialog.inner_text(), "language dialog title missing"
    links = dialog.locator("a")
    found = {}
    for i in range(links.count()):
        found[squash(links.nth(i).inner_text())] = url_path(links.nth(i).get_attribute("href") or "")
    for name in LANGUAGE_NAMES:
        assert name in found, f"language dialog lacks {name!r}: {sorted(found)}"
    assert found["English"] == "/", f"English links to {found['English']}"
    for code, name in LOCALES.items():
        assert found[name] == f"/{code}", f"{name} links to {found[name]}"
    language_links = [n for n, href in found.items() if re.fullmatch(r"/([a-z]{2})?", href)]
    assert len(language_links) == 12, f"language dialog lists {len(language_links)} languages"
    inside = "() => document.querySelector('[data-testid=\"language-dialog\"]').contains(document.activeElement)"
    assert page.evaluate(inside), "focus did not move into the language dialog"
    for _ in range(len(LANGUAGE_NAMES) + 4):
        page.keyboard.press("Tab")
        assert page.evaluate(inside), "Tab moved focus out of the open language dialog"
    for _ in range(4):
        page.keyboard.press("Shift+Tab")
        assert page.evaluate(inside), "Shift+Tab moved focus out of the open language dialog"
    above = page.evaluate("""() => { const bar = document.getElementById('brandNavbar').getBoundingClientRect();
        const hit = document.elementFromPoint(bar.left + bar.width / 2, bar.top + Math.min(bar.height, 20) / 2);
        return !!hit && !document.getElementById('brandNavbar').contains(hit); }""")
    assert above, "the open language dialog does not sit above the top bar"
    page.keyboard.press("Escape")
    assert wait_until(lambda: not dialog.is_visible(), 5), "Escape did not close the language dialog"
    assert page.evaluate("() => !!document.activeElement.closest('[data-testid=\"language-control\"]')"), \
        "focus did not return to the language control"
    page.goto("/de", wait_until="networkidle")
    assert "Deutsch" in by_testid(page, "language-control").inner_text(), "language control on /de does not read Deutsch"


def test_phone_viewport_menu_button_reveals_links(browser_page):
    """At a phone width the links hide behind a named menu button, targets stay large and nothing scrolls sideways."""
    context, _ = browser_page.open(PHONE)
    tab = context.new_page()
    tab.goto("/", wait_until="networkidle")
    menu = by_testid(tab, "menu-button")
    assert menu.is_visible(), "menu-button is not visible at a phone width"
    name = (menu.get_attribute("aria-label") or menu.inner_text() or "").strip()
    assert name, "menu-button carries no text alternative"
    assert menu.get_attribute("aria-expanded") == "false", "menu-button is not collapsed on load"
    visible_help = lambda: tab.locator("a:visible", has_text="Help").count()
    assert visible_help() == 0, "top bar links show at a phone width before the menu opens"
    headline = style_of_text(tab, "Speak Freely")
    phone_tops = [by_testid(tab, "hero-phone").nth(i).bounding_box()["y"] + tab.evaluate("() => window.scrollY") for i in range(2)]
    assert min(phone_tops) >= headline["top"], "on a phone the hero phones do not stack below the hero words"
    card_xs = {round(by_testid(tab, "feature-illustration").nth(i).bounding_box()["x"]) for i in range(4)}
    assert len(card_xs) == 1, f"a phone width does not show a single column of feature cards: {card_xs}"
    assert tab.evaluate("() => parseFloat(getComputedStyle(document.body).minWidth)") == 300, "the body does not keep a 300 pixel minimum width"
    box = menu.bounding_box()
    assert box["width"] >= 44 and box["height"] >= 44, f"menu-button touch target is {box}"
    menu.click()
    assert wait_until(lambda: menu.get_attribute("aria-expanded") == "true", 5), "menu-button did not expand"
    for label in ("Help", "Donate"):
        link = tab.locator("a:visible", has_text=label).first
        assert link.is_visible(), f"{label} is not reachable after opening the menu"
        lb = link.bounding_box()
        assert lb["height"] >= 44 and lb["width"] >= 44, f"{label} touch target is {lb}"
    control = by_testid(tab, "language-control")
    assert (control.get_attribute("aria-label") or control.inner_text()).strip(), "language control has no text alternative"
    overflow = tab.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
    assert overflow <= 1, f"the home scrolls sideways by {overflow}px at a phone width"
    wide, _ = browser_page.open(DESKTOP)
    desk = wide.new_page()
    desk.goto("/", wait_until="networkidle")
    assert not by_testid(desk, "menu-button").is_visible(), "menu-button shows at a desktop width"
    assert desk.locator("#brandNavbar a", has_text="Help").first.is_visible(), "top bar links hidden at a desktop width"
    scroll = desk.evaluate("() => [getComputedStyle(document.documentElement).overflowY, getComputedStyle(document.body).overflowY]")
    assert "scroll" in scroll, f"the vertical scrollbar is not always present: overflow-y {scroll}"
    for size, label in ((TABLET, "tablet"), (LAPTOP, "laptop")):
        ctx, _ = browser_page.open(size)
        view = ctx.new_page()
        view.goto("/", wait_until="networkidle")
        overflow = view.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
        assert overflow <= 1, f"the home scrolls sideways by {overflow}px at a {label} width"
        boxes = [by_testid(view, "feature-illustration").nth(i).bounding_box() for i in range(4)]
        rows = {}
        for box in boxes:
            rows.setdefault(round(box["y"] / 40), []).append(box)
        assert sorted(len(r) for r in rows.values()) == [2, 2], f"at a {label} width the feature cards do not pair two by two: {boxes}"
        if label == "tablet":
            assert view.locator("#brandNavbar a:visible", has_text="Help").count() > 0, "top bar links are not inline on a tablet"
        else:
            words = view.evaluate("""() => { const all = Array.from(document.querySelectorAll('body *')).filter(e => e.children.length === 0 && (e.textContent || '').trim() === 'Speak Freely');
                const big = all.sort((a, b) => parseFloat(getComputedStyle(b).fontSize) - parseFloat(getComputedStyle(a).fontSize))[0];
                const r = big.getBoundingClientRect(); return [r.left, r.right, r.top, r.bottom]; }""")
            phones = [by_testid(view, "hero-phone").nth(i).bounding_box() for i in range(2)]
            assert all(words[1] <= p["x"] + 4 for p in phones), f"on a laptop the hero words are not left of the phones: {words} {phones}"
            assert any(p["y"] < words[3] for p in phones), "on a laptop the hero phones stack under the words"


def test_reduced_motion_stops_shared_transition(browser_page):
    """Interactive colour changes share one short transition, and a reduced-motion preference stops it."""
    selectors = [".get-app", '[data-testid="language-control"]', '#brandNavbar a:has-text("Help")']
    context, _ = browser_page.open(DESKTOP)
    tab = context.new_page()
    tab.goto("/", wait_until="networkidle")
    durations = []
    for selector in selectors:
        raw = tab.locator(selector).first.evaluate("e => getComputedStyle(e).transitionDuration")
        durations.append(max(transition_seconds(raw) or [0.0]))
    assert all(d > 0 for d in durations), f"interactive elements carry no transition: {durations}"
    assert max(durations) - min(durations) < 0.001 and max(durations) < 1.0, f"transitions are not one shared short duration: {durations}"
    names = tab.evaluate("""() => { const out = []; const walk = (rules) => { for (const r of rules) {
        if (r.type === CSSRule.KEYFRAMES_RULE) out.push(r.name); else if (r.cssRules) walk(r.cssRules); } };
        for (const sheet of document.styleSheets) { let rules; try { rules = sheet.cssRules; } catch (e) { continue; } walk(rules); }
        return out; }""")
    link = tab.locator("#brandNavbar a:visible", has_text="Help").first
    rest = parse_rgb(link.evaluate("e => getComputedStyle(e).color"))
    link.hover()
    settle(1)
    hovered = parse_rgb(link.evaluate("e => getComputedStyle(e).color"))
    ground = parse_rgb(link.evaluate("e => getComputedStyle(e).backgroundColor"))
    hue, chroma = hue_chroma(hovered)
    assert relative_luminance(rest) < 0.06, f"top bar links rest in {rest}, not the near-black ink"
    assert 200 <= hue <= 250 and chroma >= 0.35, f"a hovered top bar link turns {hovered}, not the interactive blue"
    assert ground[3] == 0, f"a hovered top bar link gains the ground {ground}"
    for name in ("spinAround", "pulsate", "moveIndeterminate"):
        assert name in names, f"keyframes {name!r} not declared; found {sorted(set(names))[:8]}"
    reduced, _ = browser_page.open(DESKTOP, reduced_motion="reduce")
    calm = reduced.new_page()
    calm.goto("/", wait_until="networkidle")
    for selector in selectors:
        raw = calm.locator(selector).first.evaluate("e => getComputedStyle(e).transitionDuration")
        assert max(transition_seconds(raw) or [0.0]) <= 0.001, f"{selector} keeps transition {raw} under reduced motion"
    running = calm.evaluate("() => document.getAnimations().filter(a => a.playState === 'running').length")
    assert running == 0, f"{running} animations run under reduced motion"


def test_home_images_named_and_text_meets_contrast(browser_page):
    """Content images are named, decorative ones say so, and body text clears 4.5:1 in both schemes."""
    context, _ = browser_page.open(DESKTOP)
    tab = context.new_page()
    tab.goto("/", wait_until="networkidle")
    missing_alt = tab.evaluate("() => Array.from(document.images).filter(i => !i.hasAttribute('alt')).length")
    assert missing_alt == 0, f"{missing_alt} images carry no alt attribute"
    unnamed = tab.evaluate("""() => {
      const named = (e) => (e.getAttribute('aria-label') || e.getAttribute('alt') || e.getAttribute('title')
        || (e.getAttribute('aria-labelledby') && (document.getElementById(e.getAttribute('aria-labelledby')) || {}).textContent)
        || (e.querySelector && e.querySelector('title') && e.querySelector('title').textContent)
        || (e.querySelector && e.querySelector('[aria-label], img[alt]:not([alt=""])') && 'x') || '').trim();
      return Array.from(document.querySelectorAll('[data-testid="hero-phone"]'))
        .filter(e => !named(e)).length; }""")
    assert unnamed == 0, f"{unnamed} phone renders carry no alternative text"
    undeclared = tab.evaluate("""() => Array.from(document.querySelectorAll('svg, canvas')).filter(e => {
      if (e.closest('[data-testid="hero-phone"], button, a, [role="button"]')) return false;
      if (e.closest('[aria-hidden="true"], [role="presentation"], [role="none"]')) return false;
      const role = e.getAttribute('role');
      if (role === 'presentation' || role === 'none') return false;
      if (role === 'img' && ((e.getAttribute('aria-label') || '').trim() || (e.querySelector('title') || {}).textContent)) return false;
      return true; }).length""")
    assert undeclared == 0, f"{undeclared} decorative drawings neither hide from assistive tech nor carry a name"
    for needle in ("a different messaging experience", "Share text, voice messages", "2013-2026 Beacon"):
        style = style_of_text(tab, needle)
        assert style, f"no element renders {needle!r}"
        ratio = contrast_ratio(parse_rgb(style["color"]), parse_rgb(style["background"]))
        assert ratio >= 4.5, f"{needle!r} contrast is {ratio:.2f}:1 ({style['color']} on {style['background']})"
    title = style_of_text(tab, "Say Anything")
    assert relative_luminance(parse_rgb(title["color"])) <= 0.04 and relative_luminance(parse_rgb(title["background"])) >= 0.75, \
        f"card titles are not near-black ink on a near-white ground: {title['color']} on {title['background']}"
    footer = style_of_text(tab, "2013-2026 Beacon")
    assert relative_luminance(parse_rgb(footer["background"])) <= 0.05 and relative_luminance(parse_rgb(footer["color"])) >= 0.5, \
        f"the footer is not near-white text on a deep ground: {footer['color']} on {footer['background']}"
    help_link = tab.locator("#brandNavbar a:visible", has_text="Help").first
    help_link.hover()
    settle(1)
    blue = parse_rgb(tab.evaluate("""() => { const e = Array.from(document.querySelectorAll('#brandNavbar a')).find(a => a.textContent.trim() === 'Help');
        const x = document.createElement('canvas').getContext('2d'); x.fillStyle = getComputedStyle(e).color; x.fillRect(0, 0, 1, 1);
        const d = x.getImageData(0, 0, 1, 1).data; return 'rgba(' + d[0] + ',' + d[1] + ',' + d[2] + ',1)'; }"""))
    assert contrast_ratio(blue, (255, 255, 255)) >= 4.5, f"the interactive blue {blue} falls under 4.5:1 on white"
    donate = context.new_page()
    donate.goto("/donate", wait_until="networkidle")
    by_testid(donate, "donate-custom-amount").first.fill("0.50")
    by_testid(donate, "donate-email").first.fill(new_email("hue"))
    by_testid(donate, "donate-submit").first.click()
    error = by_testid(donate, "donate-error").first
    error.wait_for(state="visible")
    reds = [c for c in element_colours(error) if c[3] > 0 and (hue_chroma(c)[0] <= 12 or hue_chroma(c)[0] >= 345) and hue_chroma(c)[1] >= 0.3]
    assert reds, "the donation refusal wears no deep red"
    by_testid(donate, "donate-custom-amount").first.fill("5")
    by_testid(donate, "donate-submit").first.click()
    confirmation = by_testid(donate, "donate-confirmation").first
    confirmation.wait_for(state="visible")
    greens = [c for c in element_colours(confirmation) if c[3] > 0 and 90 <= hue_chroma(c)[0] <= 170 and hue_chroma(c)[1] >= 0.25]
    assert greens, "the recorded gift banner wears no deep green"
    dark_context, _ = browser_page.open(DESKTOP, color_scheme="dark")
    dark = dark_context.new_page()
    dark.goto("/", wait_until="networkidle")
    for needle in ("a different messaging experience", "Share text, voice messages"):
        style = style_of_text(dark, needle)
        ratio = contrast_ratio(parse_rgb(style["color"]), parse_rgb(style["background"]))
        assert ratio >= 4.5, f"under a dark preference {needle!r} contrast is {ratio:.2f}:1"


def test_terms_privacy_table_linked_from_marketing_footers(page):
    """Every English marketing page links Terms & Privacy Policy to /terms, which carries the privacy table."""
    for path in ("/", "/donate", "/get", "/help", "/blog", "/developers", "/careers", "/brand", "/terms"):
        page.goto(path, wait_until="networkidle")
        link = page.get_by_role("link", name="Terms & Privacy Policy")
        assert link.count() > 0, f"{path} has no Terms & Privacy Policy link"
        assert url_path(link.first.get_attribute("href") or "") == "/terms", f"{path} links the privacy page to {link.first.get_attribute('href')}"
    page.goto("/de", wait_until="networkidle")
    hrefs = [url_path(a.get_attribute("href") or "") for a in page.locator("a").all()]
    assert "/terms" in hrefs, "/de links nowhere to /terms"
    page.goto("/terms", wait_until="networkidle")
    text = squash(page.locator("body").inner_text())
    missing = [row for row in PRIVACY_TABLE if squash(row) not in text]
    assert not missing, f"/terms lacks privacy table rows: {missing[:3]}"


def test_sitemap_lists_public_routes_and_robots_names_it():
    """/sitemap.xml lists exactly the twenty public routes, and /robots.txt points at it."""
    with client() as c:
        sitemap = c.get("/sitemap.xml")
        robots = c.get("/robots.txt")
    assert sitemap.status_code == 200, f"GET /sitemap.xml returned {sitemap.status_code}"
    assert "<urlset" in sitemap.text and "<html" not in sitemap.text[:300].lower(), f"/sitemap.xml is not a sitemap: {sitemap.text[:200]!r}"
    locs = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", sitemap.text)
    assert locs and all(re.match(r"https?://", u) for u in locs), f"sitemap locations are not absolute: {locs[:3]}"
    assert sorted(url_path(u) for u in locs) == sorted(PUBLIC_ROUTES), f"sitemap lists {sorted(url_path(u) for u in locs)}"
    assert robots.status_code == 200, f"GET /robots.txt returned {robots.status_code}"
    match = re.search(r"(?im)^sitemap:\s*(\S+)", robots.text)
    assert match and url_path(match.group(1)) == "/sitemap.xml", f"/robots.txt names no sitemap: {robots.text[:200]!r}"


def test_message_roundtrip_leaves_no_plaintext_in_requests_or_rows(browser_page, backend):
    """A message and a profile name reach a closed recipient browser while no request or row holds them."""
    ann, ben, cal = fresh_account("ann"), fresh_account("ben"), fresh_account("cal")
    ben_context, ben_capture = browser_page.open()
    ben_tab = ben_context.new_page()
    ui_login(ben_tab, ben["email"], ben["password"])
    assert path_of(ben_tab).startswith("/chats"), f"first sign-in for a new account landed on {path_of(ben_tab)}"
    ben_tab.close()
    ann_context, ann_capture = browser_page.open()
    ann_tab = ann_context.new_page()
    ui_login(ann_tab, ann["email"], ann["password"])
    probe = Person("probe")
    published = bundle(probe.token, ann["username"]).json()
    assert published.get("access_key") and len(published.get("devices", [])) == 1, f"browser registration published {published}"
    profile_name = f"Ann Quill {token_hex(3)}"
    ui_set_profile_name(ann_tab, profile_name, ann["password"])
    text = f"secret words {token_hex(6)} for ben"
    open_chat(ann_tab, ben["username"], ann["password"])
    send_text(ann_tab, text)
    assert wait_sent(ann_tab, text, 45), f"outgoing bubble never reached Sent; status {bubble_status(ann_tab, text)!r}"
    assert len(ann_tab.workers) >= 1, "no Web Worker runs the cryptography in the web client"
    ben_tab = ben_context.new_page()
    ben_tab.goto(f"/chats/{ann['username']}")
    ensure_unlocked(ben_tab, ben["password"])
    assert wait_until(lambda: bubble(ben_tab, text, "in").count() > 0, 45), "recipient browser never showed the message"
    assert wait_until(lambda: profile_name in by_testid(ben_tab, "conversation-title").inner_text(), 30), \
        "recipient conversation header never showed the sender's profile name"
    lost = f"no session {token_hex(6)}"
    open_chat(ann_tab, cal["username"], ann["password"])
    send_text(ann_tab, lost)
    pump(ann_tab, 8)
    assert bubble(ann_tab, lost, "out").count() > 0, "a message to an account with no device left no outgoing bubble"
    assert bubble_status(ann_tab, lost) == "Sending", f"a message with no session reads {bubble_status(ann_tab, lost)!r}"
    for capture in (ann_capture, ben_capture):
        foreign = [r["url"] for r in capture.requests if r["url"].startswith("http") and not same_origin(r["url"], app_url())]
        assert not foreign, f"the messenger called another origin at runtime: {foreign[:3]}"
    for secret in (text, profile_name, lost):
        assert not ann_capture.leaked(secret), f"sender browser sent {secret!r} readable to the service"
        assert not ben_capture.leaked(secret), f"recipient browser sent {secret!r} readable to the service"
    rows = all_row_text(backend)
    for secret in (text, profile_name, lost):
        assert not any(leaks(row, secret) for row in rows), f"a database row holds {secret!r} readable"
    for message in mails_to(ben["email"]):
        assert not leaks(mail_text(message), text), "the nudge email carries the message text"


def test_sealed_send_needs_access_key_and_envelope_names_no_sender(backend):
    """A one-to-one send is accepted on the access key alone, and neither envelope nor row names the sender."""
    ann, ben = Person("ann"), Person("ben")
    with client() as c:
        anonymous = c.get(f"/api/keys/{ben.username}")
    assert is_client_error(anonymous), f"a visitor fetched a key bundle: {anonymous.status_code}"
    fetched = bundle(ann.token, ben.username)
    assert ok(fetched) and fetched.json().get("access_key") == ben.access_key, \
        f"GET /api/keys/{{username}} returned {fetched.status_code}: {body_of(fetched)}"
    wrong = sealed_send(ben.username, b64(os.urandom(16)), [entry(1)])
    assert is_client_error(wrong), f"a wrong access key was accepted: {wrong.status_code}"
    missing = sealed_send(ben.username, None, [entry(1)])
    assert is_client_error(missing), f"a send without any credential was accepted: {missing.status_code}"
    assert fetch(ben.token) == [], "a refused sealed send queued an envelope"
    guid, ciphertext = new_guid(), random_ciphertext()
    accepted = sealed_send(ben.username, ben.access_key, [entry(1, guid, ciphertext)])
    assert ok(accepted) and accepted.json().get("accepted") is True, f"sealed send returned {accepted.status_code}: {body_of(ok)}"
    envelopes = fetch(ben.token)
    assert len(envelopes) == 1, f"recipient device holds {len(envelopes)} envelopes"
    envelope = envelopes[0]
    assert set(envelope) == {"guid", "ciphertext", "server_timestamp", "group_id"}, f"envelope fields are {sorted(envelope)}"
    assert envelope["guid"] == guid and envelope["ciphertext"] == ciphertext and envelope["group_id"] is None, f"envelope is {envelope}"
    assert isinstance(envelope["server_timestamp"], int) and envelope["server_timestamp"] > 1_600_000_000_000, \
        f"server_timestamp is {envelope['server_timestamp']!r}"
    flat = json.dumps(envelope).lower()
    assert ann.username not in flat and ann.email.lower() not in flat, "the envelope names the sender"
    with client(bearer(ann.token)) as c:
        profile = c.get(f"/api/profile/{ben.username}")
    assert ok(profile) and profile.json().get("profile_ciphertext") == ben.profile_ciphertext, f"GET /api/profile/{{username}} returned {body_of(profile)}"
    assert is_client_error(bundle(ann.token, f"nosuch_{token_hex(4)}")), "a key bundle for a username with no account was served"
    tables = {r["table_name"] for r in backend.query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")}
    wanted = {"accounts", "devices", "one_time_prekeys", "link_codes", "profiles", "envelopes", "acknowledged_guids", "groups", "group_members", "recovery_records", "donations"}
    assert wanted <= tables, f"the public schema lacks {sorted(wanted - tables)}"
    columns = [r["column_name"] for r in backend.query("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'envelopes'")]
    assert not [c for c in columns if re.search(r"sender|from|source|author", c)], f"envelopes carries a sender column: {columns}"
    rows = rows_holding(backend, ciphertext)
    assert rows, "the queued ciphertext is in no database row"
    for row in rows:
        assert ann.username not in row and ann.email.lower() not in row.lower(), f"a stored envelope row names the sender: {row[:200]}"


def test_signup_stores_only_password_hash_and_refuses_duplicates(backend):
    """Signup stores a hash, refuses case-variant emails, taken usernames and malformed input, storing nothing."""
    email, username, password = new_email("sig"), new_username("sig"), f"pw-{token_hex(6)}-beacon"
    created = signup(email, username, password)
    assert created.status_code in (200, 201) and created.json().get("username") == username, \
        f"POST /api/auth/signup returned {created.status_code}: {body_of(created)}"
    assert account_token(email, password)
    assert not rows_containing(backend, password), "the plaintext password sits in a database row"
    rejected = [
        (email.upper(), new_username("dup"), f"pw-{token_hex(6)}-beacon"),
        (new_email("dup"), username, f"pw-{token_hex(6)}-beacon"),
        (new_email("bad"), f"Nova_{token_hex(2)}", f"pw-{token_hex(6)}-beacon"),
        (new_email("bad"), "ab", f"pw-{token_hex(6)}-beacon"),
        (new_email("bad"), new_username("shortpw"), "short-pw"),
        (f"nobody-{token_hex(3)}", new_username("noemail"), f"pw-{token_hex(6)}-beacon"),
    ]
    for bad_email, bad_username, bad_password in rejected:
        r = signup(bad_email, bad_username, bad_password)
        assert is_client_error(r), f"signup {bad_email}/{bad_username} was not refused: {r.status_code}"
    for bad_email, bad_username, bad_password in rejected:
        if bad_username != username:
            stored = backend.query("SELECT 1 FROM accounts WHERE lower(username) = lower(%s)", (bad_username,))
            assert not stored, f"a refused username {bad_username} was stored"
        if bad_email.lower() != email.lower():
            stored = backend.query("SELECT 1 FROM accounts WHERE lower(email) = lower(%s)", (bad_email,))
            assert not stored, f"a refused email {bad_email} was stored"
    token = account_token(email, password)
    with client(bearer(token)) as c:
        me = c.get("/api/me")
    assert ok(me) and me.json().get("username") == username and me.json().get("email", "").lower() == email.lower(), \
        f"GET /api/me with an account token returned {me.status_code}: {body_of(me)}"
    device = register_device(token, one_time=1)
    with client(bearer(device["token"])) as c:
        me_device = c.get("/api/me")
    assert ok(me_device) and me_device.json().get("username") == username, f"GET /api/me with a device token returned {body_of(me_device)}"
    assert len(backend.query("SELECT 1 FROM accounts WHERE lower(email) = lower(%s)", (email,))) == 1, \
        "the case-variant signup created a second account"


def test_sign_in_refused_after_five_wrong_passwords(backend):
    """Seeds sign in once each, five wrong passwords lock an email even when simultaneous, four do not."""
    for email in SEED_ACCOUNTS:
        r = login(email, SEEDED_PASSWORD)
        assert r.status_code == 200 and r.json().get("access_token"), f"seeded {email} cannot sign in: {r.status_code}"
        count = backend.query("SELECT count(*) AS n FROM accounts WHERE lower(email) = %s", (email,))[0]["n"]
        assert count == 1, f"seeded {email} exists {count} times"
    four = fresh_account("four")
    for _ in range(4):
        assert is_client_error(login(four["email"], "wrong-password-0000"))
    assert ok(login(four["email"], four["password"])), "four wrong passwords already locked the email"
    five = fresh_account("five")
    for _ in range(5):
        assert is_client_error(login(five["email"], "wrong-password-0000"))
    locked = login(five["email"], five["password"])
    assert is_client_error(locked), f"sign-in after five wrong passwords returned {locked.status_code}"
    burst = fresh_account("burst")
    results = run_together([lambda: login(burst["email"], "wrong-password-0000") for _ in range(8)])
    assert all(is_client_error(r) for r in results)
    after = login(burst["email"], burst["password"])
    assert is_client_error(after), f"simultaneous wrong passwords left sign-in open: {after.status_code}"


def test_linked_browser_receives_both_sides_of_conversation(browser_page, backend):
    """A browser linked by code receives new messages, mirrors its own sends, edits, deletes and archives."""
    ann, ben = fresh_account("ann"), fresh_account("ben")
    first_context, first_capture = browser_page.open()
    first = first_context.new_page()
    ui_login(first, ann["email"], ann["password"])
    first.goto("/settings/devices")
    ensure_unlocked(first, ann["password"])
    by_testid(first, "link-code-create").click()
    assert wait_until(lambda: re.fullmatch(r"[A-Z0-9]{8}", by_testid(first, "link-code-value").inner_text().strip() or ""), 20), \
        "no eight-character link code appeared"
    code = by_testid(first, "link-code-value").inner_text().strip()
    second_context, second_capture = browser_page.open()
    second = second_context.new_page()
    ui_login(second, ann["email"], ann["password"])
    second.wait_for_url(re.compile(r"/link(/|\\?|$)"), timeout=20000)
    by_testid(second, "link-code-input").fill(code)
    by_testid(second, "link-code-submit").click()
    second.wait_for_url(re.compile(r"/chats(/|\\?|$)"), timeout=30000)
    ben_context, ben_capture = browser_page.open()
    ben_tab = ben_context.new_page()
    ui_login(ben_tab, ben["email"], ben["password"])
    hello = f"hello both {token_hex(5)}"
    open_chat(ben_tab, ann["username"], ben["password"])
    send_text(ben_tab, hello)
    assert wait_sent(ben_tab, hello, 45), "message to a two-device account never reached Sent"
    open_chat(first, ben["username"], ann["password"])
    open_chat(second, ben["username"], ann["password"])
    assert wait_until(lambda: bubble(first, hello, "in").count() > 0, 20), "first browser never showed the message"
    assert wait_until(lambda: bubble(second, hello, "in").count() > 0, 20), "linked browser never showed the message"
    reply = f"reply from linked {token_hex(5)}"
    send_text(second, reply)
    assert wait_sent(second, reply, 45), "reply from the linked browser never reached Sent"
    assert wait_until(lambda: bubble(first, reply, "out").count() > 0, 20), "first browser never mirrored the linked browser's reply"
    assert wait_until(lambda: bubble(ben_tab, reply, "in").count() > 0, 20), "recipient never received the reply"
    out_box = bubble(first, reply, "out").first.bounding_box()
    in_box = bubble(first, hello, "in").first.bounding_box()
    assert out_box["x"] + out_box["width"] / 2 != in_box["x"] + in_box["width"] / 2 and \
        ((out_box["x"] > in_box["x"] and out_box["x"] + out_box["width"] > in_box["x"] + in_box["width"]) or
         (out_box["x"] < in_box["x"] and out_box["x"] + out_box["width"] < in_box["x"] + in_box["width"])), \
        f"outgoing and incoming bubbles share a side: {out_box} {in_box}"
    out_colours = [c for c in element_colours(bubble(first, reply, "out").first) if c[3] > 0.5]
    in_colours = [c for c in element_colours(bubble(first, hello, "in").first) if c[3] > 0.5]
    assert any(200 <= hue_chroma(c)[0] <= 250 and hue_chroma(c)[1] >= 0.35 for c in out_colours), f"the outgoing bubble wears no brand blue: {out_colours[:6]}"
    assert any(relative_luminance(c) >= 0.75 and hue_chroma(c)[1] <= 0.08 for c in in_colours), f"the incoming bubble wears no near-white neutral: {in_colours[:6]}"
    assert visible_testid(first, "conversation-mute"), "the conversation header offers no mute control"
    edited = f"reply edited {token_hex(5)}"
    target = bubble(second, reply, "out").first
    target.hover()
    target.locator('[data-testid="message-edit"]').click()
    by_testid(second, "message-edit-input").fill(edited)
    by_testid(second, "message-edit-save").click()
    assert wait_until(lambda: bubble(first, edited, "out").count() > 0, 20), "the edit never reached the first browser"
    assert wait_until(lambda: bubble(ben_tab, edited, "in").count() > 0, 20), "the edit never reached the other person"
    target = bubble(second, edited, "out").first
    target.hover()
    target.locator('[data-testid="message-delete"]').click()
    by_testid(second, "message-delete-confirm").click()
    assert wait_until(lambda: bubble(first, edited).count() == 0, 20), "the delete never reached the first browser"
    second.goto("/chats")
    ensure_unlocked(second, ann["password"], ("new-chat", "conversation-row"))
    row = f'[data-testid="conversation-row"][data-username="{ben["username"]}"]'
    assert wait_until(lambda: second.locator(row).count() > 0 and second.locator(row).first.is_visible(), 20), \
        "the linked browser never listed the conversation before archiving"
    by_testid(first, "conversation-mute").first.click()
    assert wait_until(lambda: second.locator(row).first.get_attribute("data-muted") == "true", 20), \
        "muting on one browser did not mark the row as muted on the linked browser"
    by_testid(first, "conversation-archive").first.click()
    assert wait_until(lambda: second.locator(row).count() == 0 or not second.locator(row).first.is_visible(), 20), \
        "archiving on one browser did not remove the conversation row on the linked browser"
    for secret in (hello, reply, edited):
        for capture in (first_capture, second_capture, ben_capture):
            assert not capture.leaked(secret), f"a browser sent {secret!r} readable to the service"
    rows = all_row_text(backend)
    assert not any(leaks(r, s) for r in rows for s in (hello, reply, edited)), "a database row holds conversation text"


def test_photo_video_and_file_attachments_arrive_sealed(browser_page, backend):
    """Photo, video and file attachments render for the recipient while their bytes never reach the service."""
    ann, ben = fresh_account("ann"), fresh_account("ben")
    ben_context, ben_capture = browser_page.open()
    ben_tab = ben_context.new_page()
    ui_login(ben_tab, ben["email"], ben["password"])
    ann_context, ann_capture = browser_page.open()
    ann_tab = ann_context.new_page()
    ui_login(ann_tab, ann["email"], ann["password"])
    open_chat(ann_tab, ben["username"], ann["password"])
    png = make_png(os.urandom(12))
    clip = b"\x1aE\xdf\xa3" + os.urandom(2048)
    file_name = f"notes-{token_hex(3)}.txt"
    file_body = f"file body {token_hex(8)}".encode()
    for payload in ({"name": "photo.png", "mimeType": "image/png", "buffer": png},
                    {"name": "clip.webm", "mimeType": "video/webm", "buffer": clip},
                    {"name": file_name, "mimeType": "text/plain", "buffer": file_body}):
        by_testid(ann_tab, "composer-attach").set_input_files(files=[payload])
        by_testid(ann_tab, "composer-send").click()
        settle(2)
    open_chat(ben_tab, ann["username"], ben["password"])
    assert wait_until(lambda: by_testid(ben_tab, "message-image").count() > 0, 45), "the photo never arrived"
    assert wait_until(lambda: ben_tab.evaluate("""() => { const e = document.querySelector('[data-testid="message-image"]');
        const img = e && (e.tagName === 'IMG' || e.tagName === 'CANVAS' ? e : e.querySelector('img, canvas'));
        return !!img && (img.tagName === 'CANVAS' ? img.width > 0 : img.naturalWidth > 0); }"""), 20), \
        "the received photo does not render"
    assert wait_until(lambda: by_testid(ben_tab, "message-video").count() > 0, 45), "the video never arrived"
    assert wait_until(lambda: file_name in " ".join(by_testid(ben_tab, "message-file").all_inner_texts()), 45), \
        "the file never arrived with its name"
    by_testid(ann_tab, "composer-sticker").first.click()
    options = by_testid(ann_tab, "sticker-option")
    assert wait_until(lambda: options.count() == 6, 10), f"the sticker picker offers {options.count()} stickers"
    names = sorted((options.nth(i).get_attribute("aria-label") or options.nth(i).get_attribute("title") or options.nth(i).inner_text() or "").strip() for i in range(6))
    assert names == sorted(["Wave", "Heart", "Thumbs Up", "Laugh", "Party", "Beacon Light"]), f"the sticker picker names {names}"
    for capture in (ann_capture, ben_capture):
        for data in (png, clip[:64], file_body):
            assert not any(leaks_bytes(blob, data) for blob in capture.blobs()), "attachment bytes reached the service readable"
    rows = all_row_text(backend)
    for data in (png, file_body):
        assert not any(leaks_bytes(row, data) for row in rows), "a database row holds attachment bytes"


def test_voice_message_call_ringing_and_read_receipt(browser_page):
    """A voice message and unread count arrive, calls ring and close on both sides, and a sealed Read receipt returns."""
    ann, ben = fresh_account("ann"), fresh_account("ben")
    ben_context, ben_capture = browser_page.open()
    ben_tab = ben_context.new_page()
    ui_login(ben_tab, ben["email"], ben["password"])
    ann_context, _ = browser_page.open()
    ann_tab = ann_context.new_page()
    ui_login(ann_tab, ann["email"], ann["password"])
    open_chat(ann_tab, ben["username"], ann["password"])
    first, second = f"first {token_hex(4)}", f"second {token_hex(4)}"
    send_text(ann_tab, first)
    assert wait_sent(ann_tab, first, 45)
    send_text(ann_tab, second)
    assert wait_sent(ann_tab, second, 45)
    by_testid(ann_tab, "composer-voice").click()
    settle(2.5)
    by_testid(ann_tab, "composer-voice").click()
    assert wait_until(lambda: ann_tab.locator('[data-testid="message-bubble"][data-direction="out"] [data-testid="message-voice"]').count() > 0, 30), \
        "the voice message never appeared as sent"
    ben_tab.goto("/chats")
    ensure_unlocked(ben_tab, ben["password"])
    row = ben_tab.locator(f'[data-testid="conversation-row"][data-username="{ann["username"]}"]')
    assert wait_until(lambda: row.count() > 0 and row.first.locator('[data-testid="unread-count"]').count() > 0
                      and row.first.locator('[data-testid="unread-count"]').inner_text().strip() == "3", 45), \
        "the chats row never showed three unread messages"
    open_chat(ben_tab, ann["username"], ben["password"])
    assert wait_until(lambda: by_testid(ben_tab, "message-voice").count() > 0, 30), "the voice message never arrived"
    assert wait_until(lambda: bubble_status(ann_tab, first) in ("Delivered", "Read"), 45), f"the delivered message reads {bubble_status(ann_tab, first)!r}"
    assert wait_until(lambda: bubble_status(ann_tab, second) == "Read", 45), f"sender status stayed {bubble_status(ann_tab, second)!r}"
    receipts = put_requests_to(ben_capture, ann["username"])
    assert receipts, "the recipient sent no sealed receipt"
    for request in receipts:
        headers = {k.lower(): v for k, v in request["headers"].items()}
        assert "unidentified-access-key" in headers and "authorization" not in headers, "a receipt was sent as an identified request"
    by_testid(ann_tab, "call-voice").click()
    assert wait_until(lambda: by_testid(ann_tab, "call-screen").count() > 0 and by_testid(ann_tab, "call-screen").first.is_visible(), 15), \
        "starting a voice call opened no call screen"
    incoming = by_testid(ben_tab, "call-incoming")
    assert wait_until(lambda: incoming.count() > 0 and incoming.first.is_visible(), 20), "the called person saw no incoming call"
    assert ann["username"] in incoming.first.inner_text() or "Ann" in incoming.first.inner_text(), "the incoming call does not name the caller"
    assert ben["username"] in by_testid(ann_tab, "call-screen").first.inner_text(), "the call screen does not name the other person"
    by_testid(ben_tab, "call-decline").click()
    assert wait_until(lambda: by_testid(ann_tab, "call-screen").count() == 0 or not by_testid(ann_tab, "call-screen").first.is_visible(), 10), \
        "declining left the caller's call screen open"
    by_testid(ann_tab, "call-voice").click()
    assert wait_until(lambda: by_testid(ben_tab, "call-incoming").count() > 0 and by_testid(ben_tab, "call-incoming").first.is_visible(), 20)
    by_testid(ben_tab, "call-answer").click()
    assert wait_until(lambda: by_testid(ben_tab, "call-screen").count() > 0 and by_testid(ben_tab, "call-screen").first.is_visible(), 15), \
        "answering opened no call screen for the called person"
    by_testid(ann_tab, "call-hang-up").first.click()
    assert wait_until(lambda: by_testid(ben_tab, "call-screen").count() == 0 or not by_testid(ben_tab, "call-screen").first.is_visible(), 10), \
        "hanging up left the other call screen open"
    group_name = f"Trail {token_hex(3)}"
    ann_tab.goto("/chats")
    ensure_unlocked(ann_tab, ann["password"], "new-group")
    by_testid(ann_tab, "new-group").first.click()
    by_testid(ann_tab, "new-group-name").first.fill(group_name)
    by_testid(ann_tab, "new-group-members").first.fill(ben["username"])
    by_testid(ann_tab, "new-group-create").first.click()
    ann_tab.wait_for_url(re.compile(r"/groups/[^/?#]+"), timeout=30000)
    ensure_unlocked(ann_tab, ann["password"], "call-video")
    ben_tab.goto("/chats")
    ensure_unlocked(ben_tab, ben["password"], ("new-chat", "conversation-row"))
    by_testid(ann_tab, "call-video").first.click()
    assert wait_until(lambda: visible_testid(ann_tab, "call-screen") and group_name in by_testid(ann_tab, "call-screen").first.inner_text(), 15), \
        "a group video call opened no call screen naming the group"
    ring = by_testid(ben_tab, "call-incoming")
    assert wait_until(lambda: ring.count() > 0 and ring.first.is_visible() and group_name in ring.first.inner_text(), 20), \
        "a group call did not ring another member with an incoming call naming the group"


def test_disappearing_timer_removes_message_from_both_browsers(browser_page):
    """A 30 second timer reaches both browsers and removes the message from both; a non-member sees the group refused."""
    ann, ben = fresh_account("ann"), fresh_account("ben")
    ben_context, _ = browser_page.open()
    ben_tab = ben_context.new_page()
    ui_login(ben_tab, ben["email"], ben["password"])
    ann_context, _ = browser_page.open()
    ann_tab = ann_context.new_page()
    ui_login(ann_tab, ann["email"], ann["password"])
    open_chat(ann_tab, ben["username"], ann["password"])
    by_testid(ann_tab, "disappearing-timer").select_option("30s")
    settle(2)
    text = f"vanishing {token_hex(5)}"
    send_text(ann_tab, text)
    assert wait_sent(ann_tab, text, 45), "timed message never reached Sent"
    open_chat(ben_tab, ann["username"], ben["password"])
    assert wait_until(lambda: bubble(ben_tab, text, "in").count() > 0, 30), "timed message never arrived"
    assert wait_until(lambda: by_testid(ben_tab, "disappearing-timer").input_value() == "30s", 20), "the timer change never reached the recipient"
    assert wait_until(lambda: bubble(ben_tab, text).count() == 0, 90), "the timed message stayed on the recipient browser"
    assert wait_until(lambda: bubble(ann_tab, text).count() == 0, 90), "the timed message stayed on the sender browser"
    ben_tab.goto("/chats")
    open_chat(ben_tab, ann["username"], ben["password"])
    settle(3)
    assert bubble(ben_tab, text).count() == 0, "the timed message came back after revisiting the conversation"
    owner, guest = Person("own"), Person("gst")
    created = create_group(owner.token, [guest.username])
    assert created.status_code in (200, 201), f"POST /api/groups returned {created.status_code}: {body_of(created)}"
    ben_tab.goto(f"/groups/{created.json()['group_id']}")
    ensure_unlocked(ben_tab, ben["password"])
    assert wait_until(lambda: GROUP_UNAVAILABLE in ben_tab.locator("body").inner_text(), 20), "a non-member opening a group saw no refusal"


def test_simultaneous_same_revision_group_changes_admit_one_winner():
    """Two simultaneous changes from one revision leave exactly one applied and one refused with the revision."""
    admin, xen, yul = Person("ada"), Person("xen"), Person("yul")
    created = create_group(admin.token, [xen.username])
    assert created.status_code in (200, 201), f"POST /api/groups returned {created.status_code}: {body_of(created)}"
    group = created.json()
    assert group["revision"] == 1, f"a new group starts at revision {group['revision']}"
    assert group["members"] == sorted([admin.username, xen.username]) and group["admins"] == [admin.username], f"new group is {group}"
    results = run_together([
        lambda: patch_group(admin.token, group["group_id"], 1, add=[yul.username]),
        lambda: patch_group(admin.token, group["group_id"], 1, remove=[xen.username]),
    ])
    winners = [r for r in results if r.status_code in (200, 201)]
    losers = [r for r in results if is_client_error(r)]
    assert len(winners) == 1 and len(losers) == 1, f"simultaneous changes returned {[r.status_code for r in results]}"
    assert winners[0].json()["revision"] == 2, f"the winning change reports {body_of(winners[0])}"
    assert losers[0].json().get("revision") == 2, f"the losing change reports {body_of(losers[0])}"
    current = read_group(admin.token, group["group_id"]).json()
    assert current["revision"] == 2, f"group revision is {current['revision']}"
    stale = patch_group(admin.token, group["group_id"], 1)
    assert is_client_error(stale) and stale.json().get("revision") == 2, f"a stale revision change returned {body_of(stale)}"
    added = yul.username in current["members"]
    removed = xen.username not in current["members"]
    assert added != removed, f"exactly one change should be applied; members are {current['members']}"
    assert current["members"] == sorted(current["members"]), "members are not in ascending order"


def test_group_message_reaches_current_members_only():
    """A group send fans out once to current member devices, never to removed, earlier-absent or stranger accounts."""
    admin, max_, oli, lee, sam = Person("ada"), Person("max"), Person("oli"), Person("lee"), Person("sam")
    max_second = max_.link_device()
    admin_second = admin.link_device()
    ghost = create_group(admin.token, [max_.username, f"ghost_{token_hex(3)}"])
    assert is_client_error(ghost), f"a group naming an unknown user was created: {ghost.status_code}"
    gid = create_group(admin.token, [max_.username, oli.username]).json()["group_id"]
    g1, c1 = new_guid(), random_ciphertext()
    sent = group_send(admin.token, gid, g1, c1)
    assert ok(sent), f"group send returned {sent.status_code}: {body_of(sent)}"
    for token, label in ((max_.token, "member device 1"), (max_second["token"], "member device 2"),
                         (oli.token, "second member"), (admin_second["token"], "sender's other device")):
        envelopes = fetch(token)
        assert [e["guid"] for e in envelopes] == [g1], f"{label} holds {guids_of(envelopes)}"
        assert envelopes[0]["group_id"] == gid, f"{label} envelope group_id is {envelopes[0]['group_id']}"
    assert fetch(admin.token) == [], "the sending device received its own group message"
    changed = patch_group(admin.token, gid, 1, add=[lee.username], remove=[oli.username])
    assert ok(changed), f"admin change returned {changed.status_code}: {body_of(changed)}"
    g2 = new_guid()
    assert ok(group_send(admin.token, gid, g2, random_ciphertext()))
    assert g2 not in guids_of(fetch(oli.token)), "a removed member received a later group message"
    lee_guids = guids_of(fetch(lee.token))
    assert g2 in lee_guids and g1 not in lee_guids, f"newly added member holds {lee_guids}"
    g3 = new_guid()
    stranger = group_send(sam.token, gid, g3, random_ciphertext())
    assert is_client_error(stranger), f"a non-member's group send returned {stranger.status_code}"
    for token in (max_.token, lee.token, admin_second["token"]):
        assert g3 not in guids_of(fetch(token)), "a non-member's group send was queued"


def test_donation_receipt_email_reaches_donor_only():
    """A recorded gift sends exactly one receipt to the donor alone, with the subject, amount, foundation and sender."""
    email = new_email("donor")
    r = _post_donation(f"gift-{token_hex(8)}", {"amount_minor": 2500, "currency": "usd", "email": email})
    assert r.status_code in (200, 201), f"POST /api/donations returned {r.status_code}: {body_of(r)}"
    data = r.json()
    assert (data.get("amount_minor"), data.get("currency"), data.get("status")) == (2500, "usd", "received"), f"donation response is {data}"
    wait_for_mail(email, 1)
    settle()
    messages = mails_to(email)
    assert len(messages) == 1, f"donor received {len(messages)} emails"
    receipt = messages[0]
    assert receipt.get("Subject") == RECEIPT_SUBJECT, f"receipt subject is {receipt.get('Subject')!r}"
    assert _addresses(receipt.get("To")) == [email.lower()], f"receipt went to {_addresses(receipt.get('To'))}"
    assert not receipt.get("Cc") and not receipt.get("Bcc"), "receipt carries cc or bcc recipients"
    body = mail_text(receipt)
    assert "$25.00" in body and FOUNDATION in body, f"receipt body lacks the amount or the foundation: {body[:300]!r}"
    assert (receipt.get("From") or {}).get("Address", "").lower() == MAIL_FROM, f"receipt sender is {receipt.get('From')}"


def test_donation_row_stored_in_minor_units(backend):
    """A gift is stored in donations as integer minor units with the currency usd."""
    email = new_email("minor")
    r = _post_donation(f"gift-{token_hex(8)}", {"amount_minor": 5000, "currency": "usd", "email": email})
    assert r.status_code in (200, 201), f"POST /api/donations returned {r.status_code}: {body_of(r)}"
    rows = _donation_rows(backend, email)
    assert len(rows) == 1, f"donations holds {len(rows)} rows for the gift"
    assert rows[0]["amount_minor"] == 5000 and rows[0]["currency"] == "usd", f"stored donation row is {rows[0]}"


def test_donation_replay_same_key_stores_one_row_one_email(backend):
    """Repeating an Idempotency-Key stores one gift and one receipt, even at the same moment; a different body is refused."""
    email, key = new_email("replay"), f"gift-{token_hex(8)}"
    body = {"amount_minor": 1000, "currency": "usd", "email": email}
    first = _post_donation(key, body)
    again = _post_donation(key, body)
    assert first.status_code in (200, 201) and again.status_code in (200, 201), f"replay returned {first.status_code}, {again.status_code}"
    for field in ("amount_minor", "currency", "status"):
        assert first.json().get(field) == again.json().get(field), f"replayed gift differs on {field}"
    assert first.json().get("amount_minor") == 1000 and first.json().get("status") == "received", f"the gift reads {body_of(first)}"
    other = _post_donation(key, {"amount_minor": 2000, "currency": "usd", "email": email})
    assert is_client_error(other), f"the same key with a different body returned {other.status_code}"
    burst_email, burst_key = new_email("burst"), f"gift-{token_hex(8)}"
    burst_body = {"amount_minor": 1000, "currency": "usd", "email": burst_email}
    results = run_together([lambda: _post_donation(burst_key, burst_body) for _ in range(6)])
    assert all(r.status_code in (200, 201) for r in results), f"simultaneous repeats returned {[r.status_code for r in results]}"
    wait_for_mail(email, 1)
    wait_for_mail(burst_email, 1)
    settle()
    rows = _donation_rows(backend, email)
    assert len(rows) == 1 and rows[0]["amount_minor"] == 1000, f"replayed key stored {rows}"
    assert len(_donation_rows(backend, burst_email)) == 1, "simultaneous repeats stored more than one gift"
    assert len(mails_to(email)) == 1, f"replay sent {len(mails_to(email))} receipts"
    assert len(mails_to(burst_email)) == 1, f"simultaneous repeats sent {len(mails_to(burst_email))} receipts"


def test_invalid_donation_stores_nothing_and_sends_no_email(backend):
    """Missing keys, bad amounts, other currencies and bad emails are refused as client errors with nothing stored or sent."""
    cases = [
        (None, {"amount_minor": 2500, "currency": "usd"}),
        (f"gift-{token_hex(8)}", {"amount_minor": 99, "currency": "usd"}),
        (f"gift-{token_hex(8)}", {"amount_minor": 1000001, "currency": "usd"}),
        (f"gift-{token_hex(8)}", {"amount_minor": 2500.5, "currency": "usd"}),
        (f"gift-{token_hex(8)}", {"amount_minor": "2500", "currency": "usd"}),
        (f"gift-{token_hex(8)}", {"amount_minor": 2500, "currency": "USD"}),
        (f"gift-{token_hex(8)}", {"amount_minor": 2500, "currency": "eur"}),
        ("short77", {"amount_minor": 2500, "currency": "usd"}),
        ("k" * 65, {"amount_minor": 2500, "currency": "usd"}),
        (f"bad key {token_hex(4)}!", {"amount_minor": 2500, "currency": "usd"}),
    ]
    emails = []
    for key, body in cases:
        email = new_email("invalid")
        emails.append(email)
        r = _post_donation(key, {**body, "email": email})
        assert is_client_error(r), f"invalid donation {body} with key {key!r} returned {r.status_code}"
    bad_email = f"not-an-email-{token_hex(3)}"
    r = _post_donation(f"gift-{token_hex(8)}", {"amount_minor": 2500, "currency": "usd", "email": bad_email})
    assert is_client_error(r), f"a donation with email {bad_email!r} returned {r.status_code}"
    settle()
    for email in emails + [bad_email]:
        assert _donation_rows(backend, email) == [], f"a refused donation for {email} was stored"
    for email in emails:
        assert mails_to(email) == [], f"a refused donation sent mail to {email}"


def test_second_device_registration_denied_without_link_code():
    """Later devices need a one-time code from the same account; bad codes get one refusal; a raced code admits one."""
    ann, other = Person("ann"), Person("oth")
    with client(bearer(ann.token)) as c:
        listed = c.get("/api/devices")
    assert ok(listed) and [d["device_id"] for d in listed.json()] == [1], f"GET /api/devices returned {body_of(listed)}"
    bare = register_device_raw(ann.account, key_material())
    assert is_client_error(bare), f"a second device without a code returned {bare.status_code}"
    with client(bearer(other.token)) as c:
        foreign_code = c.post("/api/devices/link-codes").json()["code"]
    unknown = register_device_raw(ann.account, {**key_material(), "link_code": "ZZZZ9999"})
    foreign = register_device_raw(ann.account, {**key_material(), "link_code": foreign_code})
    assert is_client_error(unknown) and is_client_error(foreign), f"bad codes returned {unknown.status_code}, {foreign.status_code}"
    with client(bearer(ann.token)) as c:
        issued = c.post("/api/devices/link-codes")
    assert issued.status_code in (200, 201), f"POST /api/devices/link-codes returned {issued.status_code}"
    code = issued.json()["code"]
    assert re.fullmatch(r"[A-Z0-9]{8}", code), f"link code {code!r} is not eight capitals or digits"
    linked = register_device_raw(ann.account, {**key_material(), "link_code": code})
    assert linked.status_code in (200, 201) and linked.json().get("device_id") == 2, f"linking returned {body_of(linked)}"
    used = register_device_raw(ann.account, {**key_material(), "link_code": code})
    assert is_client_error(used), f"a used code returned {used.status_code}"
    assert (unknown.status_code, unknown.json()) == (foreign.status_code, foreign.json()) == (used.status_code, used.json()), \
        "unknown, foreign and used link codes receive different refusals"
    with client(bearer(ann.token)) as c:
        raced_code = c.post("/api/devices/link-codes").json()["code"]
    results = run_together([lambda: register_device_raw(ann.account, {**key_material(), "link_code": raced_code}) for _ in range(2)])
    assert sorted(r.status_code in (200, 201) for r in results) == [False, True], f"a raced link code returned {[r.status_code for r in results]}"
    with client(bearer(ann.token)) as c:
        ids = [d["device_id"] for d in c.get("/api/devices").json()]
    assert ids == [1, 2, 3], f"active devices are {ids}"


def test_unlinked_device_token_denied_and_its_queue_deleted(backend):
    """Unlinking cuts a device off everywhere, deletes its queue and bundle; account tokens and other accounts are refused."""
    ben, ann = Person("ben"), Person("ann")
    second = ben.link_device()
    with client(bearer(ben.account)) as c:
        by_account = c.get("/api/messages")
    assert is_client_error(by_account), f"an account token fetched envelopes: {by_account.status_code}"
    c2 = random_ciphertext()
    queued = sealed_send(ben.username, ben.access_key, [entry(1), entry(2, ciphertext=c2)])
    assert ok(queued), f"send to two devices returned {queued.status_code}: {body_of(queued)}"
    with client(bearer(ann.token)) as c:
        foreign = c.delete(f"/api/devices/{second['device_id']}")
    assert is_client_error(foreign), f"another account unlinked a device: {foreign.status_code}"
    with client(bearer(ben.token)) as c:
        assert [d["device_id"] for d in c.get("/api/devices").json()] == [1, 2], "a refused unlink removed the device"
        removed = c.delete(f"/api/devices/{second['device_id']}")
    assert removed.status_code in (200, 204), f"unlinking returned {removed.status_code}"
    with client(bearer(second["token"])) as c:
        assert is_client_error(c.get("/api/messages")), "an unlinked device still fetches envelopes"
        assert is_client_error(c.get("/api/devices")), "an unlinked device still lists devices"
    assert rows_holding(backend, c2) == [], "the unlinked device's queued envelope is still stored"
    devices = bundle(ann.token, ben.username).json()["devices"]
    assert [d["device_id"] for d in devices] == [1], f"key bundles still list {devices}"
    stale = sealed_send(ben.username, ben.access_key, [entry(1), entry(2)])
    assert is_client_error(stale), f"a send naming the unlinked device returned {stale.status_code}"
    assert stale.json().get("extra_devices") == [2] and stale.json().get("missing_devices") == [], f"mismatch body is {body_of(stale)}"


def test_replace_existing_revokes_every_older_device(backend):
    """Replacement with the recovery verifier revokes every device and queue; a wrong verifier creates nothing and counts."""
    cam = Person("cam")
    cam.link_device()
    verifier = b64(os.urandom(32))
    with client(bearer(cam.token)) as c:
        saved = c.put("/api/recovery", json={"recovery_blob": random_ciphertext(64), "access_verifier": verifier})
    assert saved.status_code in (200, 201, 204), f"PUT /api/recovery returned {saved.status_code}"
    c1, c2 = random_ciphertext(), random_ciphertext()
    assert ok(sealed_send(cam.username, cam.access_key, [entry(1, ciphertext=c1), entry(2, ciphertext=c2)]))
    wrong = register_device_raw(cam.account, {**key_material(), "replace_existing": True, "access_verifier": b64(os.urandom(32))})
    assert is_client_error(wrong), f"replacement with a wrong verifier returned {wrong.status_code}"
    counted = restore(cam.account, b64(os.urandom(32)))
    assert counted.json().get("remaining_guesses") == 8, f"a wrong replacement verifier did not count as a guess: {body_of(counted)}"
    with client(bearer(cam.token)) as c:
        assert [d["device_id"] for d in c.get("/api/devices").json()] == [1, 2], "a refused replacement changed devices"
    fresh = register_device(cam.account, replace_existing=True, access_verifier=verifier)
    assert fresh["device_id"] == 3, f"the replacement device id is {fresh['device_id']}"
    for old in cam.devices:
        with client(bearer(old["token"])) as c:
            assert is_client_error(c.get("/api/messages")), "a replaced device still fetches envelopes"
    assert rows_holding(backend, c1) == [] and rows_holding(backend, c2) == [], "replaced devices' envelopes are still stored"
    with client(bearer(fresh["token"])) as c:
        assert [d["device_id"] for d in c.get("/api/devices").json()] == [3], "replacement left older devices active"


def test_malformed_device_keys_rejected_nothing_stored():
    """Keys of the wrong size, a missing post-quantum pre-key and bad key ids are refused; valid random keys are accepted."""
    account = fresh_account("keys")
    token = account_token(account["email"], account["password"])
    viewer = Person("view")
    empty = bundle(viewer.token, account["username"])
    assert ok(empty) and empty.json().get("access_key", "missing") is None and empty.json().get("devices") == [], f"bundle of a device-less account is {body_of(empty)}"
    good = key_material(1)
    bad = []
    bad.append({**good, "identity_key": b64(os.urandom(31))})
    bad.append({**good, "identity_key": "!!!not-base64!!!"})
    bad.append({**good, "signed_prekey": {**good["signed_prekey"], "signature": b64(os.urandom(63))}})
    bad.append({k: v for k, v in good.items() if k != "pq_prekey"})
    bad.append({**good, "pq_prekey": {**good["pq_prekey"], "public_key": b64(os.urandom(1183))}})
    bad.append({**good, "one_time_prekeys": [{"key_id": i + 1, "public_key": b64(os.urandom(32))} for i in range(101)]})
    bad.append({**good, "one_time_prekeys": [{"key_id": 7, "public_key": b64(os.urandom(32))}] * 2})
    bad.append({**good, "signed_prekey": {**good["signed_prekey"], "key_id": 0}})
    bad.append({**good, "signed_prekey": {**good["signed_prekey"], "key_id": 16777216}})
    bad.append({**good, "signed_prekey": {**good["signed_prekey"], "public_key": b64(os.urandom(33))}})
    bad.append({**good, "pq_prekey": {**good["pq_prekey"], "signature": b64(os.urandom(65))}})
    bad.append({**good, "one_time_prekeys": [{"key_id": 3, "public_key": b64(os.urandom(31))}]})
    bad.append({**good, "one_time_prekeys": [{"key_id": 0, "public_key": b64(os.urandom(32))}]})
    for body in bad:
        r = register_device_raw(token, body)
        assert is_client_error(r), f"malformed registration returned {r.status_code}: {body_of(r)}"
    still_empty = bundle(viewer.token, account["username"])
    assert still_empty.json()["devices"] == [], "a refused registration left a device behind"
    device = register_device(token, one_time=100)
    assert device["device_id"] == 1, f"the first accepted device got id {device['device_id']}"
    with client(bearer(device["token"])) as c:
        for body in ({"profile_ciphertext": random_ciphertext(32), "access_key": b64(os.urandom(15))},
                     {"profile_ciphertext": "", "access_key": b64(os.urandom(16))},
                     {"profile_ciphertext": b64(os.urandom(65537)), "access_key": b64(os.urandom(16))}):
            assert is_client_error(c.put("/api/profile", json=body)), "a malformed profile upload was accepted"
        for body in ({"recovery_blob": random_ciphertext(32), "access_verifier": b64(os.urandom(31))},
                     {"recovery_blob": "", "access_verifier": b64(os.urandom(32))}):
            assert is_client_error(c.put("/api/recovery", json=body)), "a malformed recovery upload was accepted"
        assert is_client_error(c.post("/api/groups", json={"encrypted_state": "", "members": []})), "a group with empty state was created"


def test_concurrent_bundle_fetches_never_share_a_one_time_prekey():
    """Eight simultaneous bundle fetches for five one-time pre-keys hand out five distinct keys and three nulls."""
    target = Person("tgt", one_time=5)
    fetchers = [Person("fa"), Person("fb")]
    results = run_together([lambda i=i: bundle(fetchers[i % 2].token, target.username) for i in range(8)])
    assert all(ok(r) for r in results), f"bundle fetches returned {[r.status_code for r in results]}"
    handed = []
    for r in results:
        data = r.json()
        assert {"access_key", "devices"} <= set(data) and data["access_key"] == target.access_key, f"bundle is {body_of(r)}"
        assert len(data["devices"]) == 1, f"bundle lists {len(data['devices'])} devices"
        device = data["devices"][0]
        assert {"device_id", "identity_key", "signed_prekey", "pq_prekey", "one_time_prekey"} <= set(device), f"bundle device fields are {sorted(device)}"
        assert device["identity_key"] == target.devices[0]["keys"]["identity_key"], "bundle identity key differs from the upload"
        assert set(device["signed_prekey"]) <= {"key_id", "public_key", "signature"}, "signed pre-key carries extra material"
        assert set(device["pq_prekey"]) <= {"key_id", "public_key", "signature"}, "post-quantum pre-key carries extra material"
        if device["one_time_prekey"] is not None:
            assert set(device["one_time_prekey"]) == {"key_id", "public_key"}, "one-time pre-key carries extra material"
            handed.append(device["one_time_prekey"]["key_id"])
    assert len(handed) == 5 and len(set(handed)) == 5, f"simultaneous fetches handed out {handed}"
    with client(bearer(target.token)) as c:
        count = c.get("/api/keys/count")
    assert ok(count) and count.json().get("one_time_prekeys") == 0, f"GET /api/keys/count returned {body_of(count)}"


def test_exhausted_one_time_prekeys_still_return_bundle():
    """An exhausted device still returns its bundle with a null one-time pre-key; reused key ids are refused."""
    target, fetcher = Person("tgt", one_time=1), Person("fx")
    first = bundle(fetcher.token, target.username).json()["devices"][0]
    assert first["one_time_prekey"] and first["one_time_prekey"]["key_id"] == 1, f"first bundle is {first}"
    second = bundle(fetcher.token, target.username)
    assert ok(second), f"exhausted bundle returned {second.status_code}"
    device = second.json()["devices"][0]
    assert device["one_time_prekey"] is None and device["signed_prekey"] and device["pq_prekey"] and device["identity_key"], f"exhausted bundle is {device}"
    with client(bearer(target.token)) as c:
        added = c.post("/api/keys/one-time", json={"one_time_prekeys": [{"key_id": 2, "public_key": b64(os.urandom(32))},
                                                                          {"key_id": 3, "public_key": b64(os.urandom(32))}]})
        assert added.status_code in (200, 201) and added.json() == {"one_time_prekeys": 2}, f"adding keys returned {body_of(added)}"
        handed = c.post("/api/keys/one-time", json={"one_time_prekeys": [{"key_id": 1, "public_key": b64(os.urandom(32))}]})
        assert is_client_error(handed), f"re-uploading a handed-out key id returned {handed.status_code}"
        repeat = c.post("/api/keys/one-time", json={"one_time_prekeys": [{"key_id": 2, "public_key": b64(os.urandom(32))}]})
        assert is_client_error(repeat), f"re-uploading a waiting key id returned {repeat.status_code}"
        assert c.get("/api/keys/count").json() == {"one_time_prekeys": 2}, "refused uploads changed the count"


def test_key_bundle_fetches_refused_past_limit_per_device():
    """A device's 301st bundle request inside sixty seconds is refused while another device is unaffected."""
    target, fetcher, bystander = Person("tgt", one_time=0), Person("fetch"), Person("by")
    started = time.monotonic()
    statuses = []
    for _ in range(10):
        batch = run_together([lambda: bundle(fetcher.token, target.username) for _ in range(30)])
        statuses.extend(r.status_code for r in batch)
    extra = bundle(fetcher.token, target.username)
    elapsed = time.monotonic() - started
    assert elapsed < 55, f"the burst took {elapsed:.0f}s, too long to probe a sixty-second window"
    assert sum(1 for code in statuses if 200 <= code < 300) == 300, f"the first 300 bundle requests returned {sorted(set(statuses))}"
    assert is_client_error(extra), f"the 301st bundle request returned {extra.status_code}"
    assert ok(bundle(bystander.token, target.username)), "the limit spilled onto another device"



def test_identified_send_to_another_account_is_denied():
    """A device-token send addressed to another account is denied and queues nothing."""
    ann, ben = Person("ann"), Person("ben")
    r = device_send(ann.token, ben.username, [entry(1)])
    assert is_client_error(r), f"an identified send to another account returned {r.status_code}"
    assert fetch(ben.token) == [], "a denied identified send queued an envelope"


def test_envelopes_reach_only_their_own_device():
    """Each device fetches only its own envelopes, oldest first; visitors and other accounts get nothing."""
    ben, cal = Person("ben"), Person("cal")
    second = ben.link_device()
    with client() as c:
        anonymous = c.get("/api/messages")
    assert is_client_error(anonymous), f"a visitor fetched envelopes: {anonymous.status_code}"
    g1, g2 = new_guid(), new_guid()
    a1, a2, b1, b2 = (random_ciphertext() for _ in range(4))
    assert ok(sealed_send(ben.username, ben.access_key, [entry(1, g1, a1), entry(2, g1, a2)]))
    assert ok(sealed_send(ben.username, ben.access_key, [entry(1, g2, b1), entry(2, g2, b2)]))
    first = fetch(ben.token)
    other = fetch(second["token"])
    assert [e["ciphertext"] for e in first] == [a1, b1], f"device 1 holds {[e['guid'] for e in first]}"
    assert [e["ciphertext"] for e in other] == [a2, b2], f"device 2 holds {[e['guid'] for e in other]}"
    assert not {g1, g2} & set(guids_of(fetch(cal.token))), "another account received envelopes it was not sent"
    stolen = ack(cal.token, g1)
    assert is_client_error(stolen), f"another account acknowledged a foreign guid: {stolen.status_code}"
    assert g1 in guids_of(fetch(ben.token)), "a refused acknowledgement removed the envelope"


def test_send_with_missing_or_extra_device_rejected_nothing_stored(backend):
    """A send that misses or adds a device, or targets an account with no device, is refused whole and emails no one."""
    ben = Person("ben")
    ben.link_device()
    c1 = random_ciphertext()
    short = sealed_send(ben.username, ben.access_key, [entry(1, ciphertext=c1)])
    assert is_client_error(short), f"a send missing device 2 returned {short.status_code}"
    assert short.json().get("missing_devices") == [2] and short.json().get("extra_devices") == [], f"mismatch body is {body_of(short)}"
    c3 = random_ciphertext()
    wide = sealed_send(ben.username, ben.access_key, [entry(1), entry(2), entry(4), entry(3, ciphertext=c3)])
    assert is_client_error(wide), f"a send naming devices 3 and 4 returned {wide.status_code}"
    assert wide.json().get("extra_devices") == [3, 4] and wide.json().get("missing_devices") == [], f"mismatch body is {body_of(wide)}"
    third = ben.link_device()
    gap = sealed_send(ben.username, ben.access_key, [entry(1)])
    assert is_client_error(gap) and gap.json().get("missing_devices") == [2, 3], f"a send missing devices 2 and 3 returned {body_of(gap)}"
    twice = sealed_send(ben.username, ben.access_key, [entry(1), entry(2), entry(3), entry(3)])
    assert is_client_error(twice), f"a send naming device 3 twice returned {twice.status_code}"
    assert fetch(third["token"]) == [], "a refused send queued an envelope for device 3"
    assert fetch(ben.token) == [] and fetch(ben.devices[1]["token"]) == [], "a rejected send queued envelopes"
    assert rows_holding(backend, c1) == [] and rows_holding(backend, c3) == [], "a rejected send stored ciphertext"
    lonely = fresh_account("lone")
    lone_token = account_token(lonely["email"], lonely["password"])
    helper = register_device(lone_token, one_time=1)
    lone_key = b64(os.urandom(16))
    with client(bearer(helper["token"])) as c:
        assert c.put("/api/profile", json={"profile_ciphertext": random_ciphertext(32), "access_key": lone_key}).status_code in (200, 201, 204)
        assert c.delete(f"/api/devices/{helper['device_id']}").status_code in (200, 204)
    empty = sealed_send(lonely["username"], lone_key, [entry(1)])
    assert is_client_error(empty), f"a send to an account with no device returned {empty.status_code}"
    settle()
    assert mails_to(ben.email) == [], "a rejected send emailed the recipient"
    assert mails_to(lonely["email"]) == [], "a send to a device-less account emailed the recipient"


def test_own_device_sync_send_names_other_devices_only():
    """A device-token send to the caller's own account must name every other device and never the sender."""
    ann = Person("ann")
    second, third = ann.link_device(), ann.link_device()
    accepted = device_send(ann.token, ann.username, [entry(2), entry(3)])
    assert ok(accepted), f"own-device sync send returned {accepted.status_code}: {body_of(ok)}"
    assert len(fetch(second["token"])) == 1 and len(fetch(third["token"])) == 1, "own devices did not each get one copy"
    assert fetch(ann.token) == [], "the sending device received its own sync copy"
    with_self = device_send(ann.token, ann.username, [entry(1), entry(2), entry(3)])
    assert is_client_error(with_self) and with_self.json().get("extra_devices") == [1], f"naming the sender returned {body_of(with_self)}"
    partial = device_send(ann.token, ann.username, [entry(2)])
    assert is_client_error(partial) and partial.json().get("missing_devices") == [3], f"leaving out device 3 returned {body_of(partial)}"


def test_invalid_ciphertext_or_guid_rejected_nothing_queued():
    """Malformed or oversize ciphertext and non-lowercase or malformed guids are refused; the size boundary is accepted."""
    ben = Person("ben")
    bad = [
        {**entry(1), "ciphertext": "not base64 !!"},
        {**entry(1), "ciphertext": ""},
        {**entry(1), "ciphertext": b64(os.urandom(1048577))},
        {**entry(1), "guid": "not-a-guid"},
        {**entry(1), "guid": new_guid().upper()},
    ]
    for item in bad:
        r = sealed_send(ben.username, ben.access_key, [item])
        assert is_client_error(r), f"malformed envelope {item['guid'][:12]} returned {r.status_code}"
    assert fetch(ben.token) == [], "a malformed envelope was queued"
    edge = sealed_send(ben.username, ben.access_key, [entry(1, ciphertext=b64(os.urandom(1048576)))])
    assert ok(edge), f"a 1048576-byte ciphertext returned {edge.status_code}"
    assert len(fetch(ben.token)) == 1, "the boundary-size envelope was not queued"


def test_acknowledgement_deletes_ciphertext_row_other_copy_remains(backend):
    """Acknowledging on one device deletes that ciphertext outright and leaves the other device's copy."""
    ben = Person("ben")
    second = ben.link_device()
    guid, c1, c2 = new_guid(), random_ciphertext(), random_ciphertext()
    assert ok(sealed_send(ben.username, ben.access_key, [entry(1, guid, c1), entry(2, guid, c2)]))
    done = ack(ben.token, guid)
    assert done.status_code in (200, 204), f"DELETE /api/messages/{{guid}} returned {done.status_code}"
    assert guid not in guids_of(fetch(ben.token)), "the acknowledged envelope is still delivered"
    assert guid in guids_of(fetch(second["token"])), "acknowledging on one device removed the other device's copy"
    assert rows_holding(backend, c1) == [], "the acknowledged ciphertext is still stored"
    assert rows_holding(backend, c2), "the other device's ciphertext is no longer stored"
    assert ack(second["token"], guid).status_code in (200, 204)
    assert rows_holding(backend, c2) == [], "the second acknowledged ciphertext is still stored"


def test_resend_after_acknowledgement_is_not_redelivered(backend):
    """Resending an acknowledged guid succeeds but delivers and stores nothing again."""
    ben = Person("ben")
    guid, ciphertext = new_guid(), random_ciphertext()
    assert ok(sealed_send(ben.username, ben.access_key, [entry(1, guid, ciphertext)]))
    assert guid in guids_of(fetch(ben.token))
    assert ack(ben.token, guid).status_code in (200, 204)
    again = sealed_send(ben.username, ben.access_key, [entry(1, guid, ciphertext)])
    assert ok(again), f"resending an acknowledged guid returned {again.status_code}"
    assert fetch(ben.token) == [], "an acknowledged guid was delivered a second time"
    assert rows_holding(backend, ciphertext) == [], "the resent ciphertext was stored again"


def test_duplicate_guid_sends_store_one_envelope():
    """Repeated and simultaneous sends of one guid leave exactly one queued envelope."""
    ben = Person("ben")
    guid = new_guid()
    first = sealed_send(ben.username, ben.access_key, [entry(1, guid)])
    second = sealed_send(ben.username, ben.access_key, [entry(1, guid)])
    assert ok(first) and ok(second), f"duplicate sends returned {first.status_code}, {second.status_code}"
    assert guids_of(fetch(ben.token)).count(guid) == 1, "a repeated guid was queued twice"
    burst = new_guid()
    ciphertext = random_ciphertext()
    results = run_together([lambda: sealed_send(ben.username, ben.access_key, [entry(1, burst, ciphertext)]) for _ in range(6)])
    assert all(ok(r) for r in results), f"simultaneous duplicate sends returned {[r.status_code for r in results]}"
    assert guids_of(fetch(ben.token)).count(burst) == 1, "simultaneous duplicate sends queued more than one envelope"


def test_device_queue_keeps_newest_thousand_envelopes():
    """A device keeps only its newest 1000 waiting envelopes, dropping the oldest, even under simultaneous sends."""
    ben = Person("ben")
    guids = [new_guid() for _ in range(1003)]
    statuses = []
    with client({"Unidentified-Access-Key": ben.access_key}) as c:
        for guid in guids:
            statuses.append(c.put(f"/api/messages/{ben.username}",
                                  json={"messages": [entry(1, guid, random_ciphertext(24))]}).status_code)
    assert statuses.count(200) == len(guids), f"queue sends returned {sorted(set(statuses))}"
    held = guids_of(fetch(ben.token))
    assert held == guids[3:], f"device holds {len(held)} envelopes; oldest kept is {held[:1]}"
    extra = [new_guid() for _ in range(12)]
    run_together([lambda g=g: sealed_send(ben.username, ben.access_key, [entry(1, g, random_ciphertext(24))]) for g in extra])
    held = guids_of(fetch(ben.token))
    assert len(held) == 1000, f"simultaneous sends left {len(held)} waiting envelopes"
    assert set(extra) <= set(held), "the newest simultaneous envelopes were dropped instead of the oldest"


def test_member_who_is_not_admin_denied_removing_others():
    """Non-admins cannot add, remove others or replace state; non-members cannot read; a member may leave."""
    admin, max_, mia, sam = Person("ada"), Person("max"), Person("mia"), Person("sam")
    group = create_group(admin.token, [max_.username, mia.username]).json()
    gid = group["group_id"]
    before = read_group(admin.token, gid).json()
    for attempt in (patch_group(max_.token, gid, 1, remove=[mia.username]),
                    patch_group(max_.token, gid, 1, add=[sam.username]),
                    patch_group(max_.token, gid, 1)):
        assert is_client_error(attempt), f"a non-admin change returned {attempt.status_code}"
    after = read_group(admin.token, gid).json()
    assert after == before, f"a denied change altered the group: {before} -> {after}"
    assert is_client_error(read_group(sam.token, gid)), "a non-member read the group"
    assert is_client_error(patch_group(sam.token, gid, 1, add=[sam.username])), "a non-member changed the group"
    views = [read_group(p.token, gid).json() for p in (admin, max_, mia)]
    assert all((v["members"], v["admins"], v["revision"]) == (views[0]["members"], views[0]["admins"], views[0]["revision"]) for v in views), \
        f"members see different rosters: {views}"
    left = patch_group(max_.token, gid, 1, remove=[max_.username], state=before["encrypted_state"])
    assert ok(left) and max_.username not in left.json()["members"], f"a member leaving returned {body_of(left)}"


def test_recovery_record_destroyed_after_tenth_wrong_guess():
    """Nine wrong guesses leave one, a right guess resets, and ten wrong guesses destroy the record even when simultaneous."""
    person = Person("rec")
    blob, verifier = random_ciphertext(64), b64(os.urandom(32))
    with client(bearer(person.token)) as c:
        assert c.put("/api/recovery", json={"recovery_blob": blob, "access_verifier": verifier}).status_code in (200, 201, 204)
    last = None
    for _ in range(9):
        last = restore(person.account, b64(os.urandom(32)))
        assert is_client_error(last), f"a wrong verifier returned {last.status_code}"
    assert last.json().get("remaining_guesses") == 1, f"after nine wrong guesses the refusal reads {body_of(last)}"
    right = restore(person.account, verifier)
    assert ok(right) and right.json().get("recovery_blob") == blob, f"the right verifier returned {body_of(right)}"
    results = run_together([lambda: restore(person.account, b64(os.urandom(32))) for _ in range(12)])
    assert all(is_client_error(r) for r in results), "a simultaneous wrong guess succeeded"
    gone = restore(person.account, verifier)
    assert is_client_error(gone), f"after ten wrong guesses the right verifier returned {gone.status_code}"


def test_nudge_email_reaches_recipient_only_without_sender_or_content():
    """One contentless nudge with the pinned subject and body reaches only the recipient, for direct and group sends."""
    ann, ben, cal = Person("ann"), Person("ben"), Person("cal")
    guid, ciphertext = new_guid(), random_ciphertext()
    assert ok(sealed_send(ben.username, ben.access_key, [entry(1, guid, ciphertext)]))
    wait_for_mail(ben.email, 1)
    settle()
    messages = mails_to(ben.email)
    assert len(messages) == 1, f"recipient received {len(messages)} nudges"
    nudge = messages[0]
    assert nudge.get("Subject") == NUDGE_SUBJECT, f"nudge subject is {nudge.get('Subject')!r}"
    assert squash(nudge.get("Text", "")) == NUDGE_BODY, f"nudge body is {nudge.get('Text', '')[:200]!r}"
    assert _addresses(nudge.get("To")) == [ben.email.lower()] and not nudge.get("Cc") and not nudge.get("Bcc"), \
        f"nudge recipients are {nudge.get('To')}, cc {nudge.get('Cc')}, bcc {nudge.get('Bcc')}"
    content = mail_text(nudge)
    for secret in (ann.username, ann.email, ciphertext, guid):
        assert secret not in content, f"the nudge carries {secret[:20]!r}"
    gid = create_group(ann.token, [cal.username]).json()["group_id"]
    g2, c2 = new_guid(), random_ciphertext()
    assert ok(group_send(ann.token, gid, g2, c2))
    wait_for_mail(cal.email, 1)
    settle()
    group_nudges = mails_to(cal.email)
    assert len(group_nudges) == 1, f"group member received {len(group_nudges)} nudges"
    group_content = mail_text(group_nudges[0])
    for secret in (ann.username, ann.email, str(gid), g2, c2):
        assert secret not in group_content, f"the group nudge carries {secret[:20]!r}"
    assert mails_to(ann.email) == [], "the sender received a nudge"


def test_no_second_nudge_email_while_envelopes_wait():
    """A second send while envelopes wait sends no nudge; once acknowledged, the next send nudges again."""
    ben = Person("ben")
    assert ok(sealed_send(ben.username, ben.access_key, [entry(1)]))
    wait_for_mail(ben.email, 1)
    assert ok(sealed_send(ben.username, ben.access_key, [entry(1)]))
    settle()
    assert len(mails_to(ben.email)) == 1, "a send while envelopes waited sent another nudge"
    for envelope in fetch(ben.token):
        assert ack(ben.token, envelope["guid"]).status_code in (200, 204)
    assert ok(sealed_send(ben.username, ben.access_key, [entry(1)]))
    wait_for_mail(ben.email, 2)
    assert len(mails_to(ben.email)) == 2, "a send after the queue emptied sent no nudge"


def test_no_nudge_email_for_own_rejected_or_repeated_send():
    """Own-device sends, rejected sends and idempotent resends never send a nudge."""
    ann = Person("ann")
    ann.link_device()
    assert ok(device_send(ann.token, ann.username, [entry(2)]))
    ben = Person("ben")
    ben.link_device()
    assert is_client_error(sealed_send(ben.username, ben.access_key, [entry(1)]))
    cal = Person("cal")
    guid = new_guid()
    assert ok(sealed_send(cal.username, cal.access_key, [entry(1, guid)]))
    wait_for_mail(cal.email, 1)
    assert ack(cal.token, guid).status_code in (200, 204)
    assert ok(sealed_send(cal.username, cal.access_key, [entry(1, guid)]))
    settle()
    assert mails_to(ann.email) == [], "a send to one's own devices sent a nudge"
    assert mails_to(ben.email) == [], "a rejected send sent a nudge"
    assert len(mails_to(cal.email)) == 1, "an idempotent resend sent a second nudge"


def test_tampered_ciphertext_dropped_with_notice_never_shown(browser_page, backend):
    """A message whose ciphertext changed in transit is never shown and the chats list shows the decrypt notice."""
    ann, ben = fresh_account("ann"), fresh_account("ben")
    ben_context, _ = browser_page.open()
    ben_tab = ben_context.new_page()
    ui_login(ben_tab, ben["email"], ben["password"])
    def rewrite(envelopes):
        return [{**e, "ciphertext": tampered(e["ciphertext"])} for e in envelopes]

    interception = route_messages(ben_tab, rewrite)
    ben_tab.goto("/chats")
    ensure_unlocked(ben_tab, ben["password"], ("new-chat", "conversation-row"))
    ann_context, ann_capture = browser_page.open()
    ann_tab = ann_context.new_page()
    ui_login(ann_tab, ann["email"], ann["password"])
    text = f"tamper target {token_hex(5)}"
    open_chat(ann_tab, ben["username"], ann["password"])
    send_text(ann_tab, text)
    assert wait_sent(ann_tab, text, 45), "the message to tamper never reached Sent"
    notice = by_testid(ben_tab, "decrypt-error-notice")
    assert wait_until(lambda: notice.count() > 0 and DECRYPT_NOTICE in notice.first.inner_text(), 45), \
        "no decrypt notice appeared for a tampered message"
    assert text not in ben_tab.content(), "the tampered message text appeared on /chats"
    ben_tab.goto(f"/chats/{ann['username']}")
    ensure_unlocked(ben_tab, ben["password"])
    pump(ben_tab, 6)
    assert text not in ben_tab.content() and bubble(ben_tab, text).count() == 0, "the tampered message was shown in the conversation"
    assert interception.served > 0, "the recipient browser never requested GET /api/messages"
    originals = sent_ciphertexts(ann_capture, ben["username"])
    assert originals, "the sender browser sent no envelope to the recipient"
    assert wait_until(lambda: all(rows_holding(backend, c) == [] for c in originals), 30), \
        "the tampered envelope was never acknowledged and still sits in the database"


def test_replayed_reordered_and_delayed_messages_show_once_in_order(browser_page):
    """Reordered, delayed and replayed envelopes decrypt and show once each in written order; identical texts seal differently."""
    ann, ben = fresh_account("ann"), fresh_account("ben")
    ben_context, _ = browser_page.open()
    ben_tab = ben_context.new_page()
    ui_login(ben_tab, ben["email"], ben["password"])
    ben_tab.close()
    ann_context, ann_capture = browser_page.open()
    ann_tab = ann_context.new_page()
    ui_login(ann_tab, ann["email"], ann["password"])
    open_chat(ann_tab, ben["username"], ann["password"])
    same = f"same words {token_hex(4)}"
    texts = [f"one {token_hex(4)}", f"two {token_hex(4)}", f"three {token_hex(4)}"]
    marks = {}
    for label, text in (("same1", same), ("same2", same), ("m1", texts[0]), ("m2", texts[1]), ("m3", texts[2])):
        before = len(put_requests_to(ann_capture, ben["username"]))
        send_text(ann_tab, text)
        assert wait_until(lambda: len(put_requests_to(ann_capture, ben["username"])) > before, 30), f"{label} was never sent"
        settle(1)
        marks[label] = (sent_guids(ann_capture, ben["username"], before), sent_ciphertexts(ann_capture, ben["username"], before))
    assert set(marks["same1"][1]).isdisjoint(marks["same2"][1]), "the same text sent twice produced the same ciphertext"
    delayed = set(marks["m2"][0])
    state = {"release": False, "injected": False}

    def rewrite(envelopes):
        if not state["release"]:
            return list(reversed([e for e in envelopes if e["guid"] not in delayed]))
        out = list(reversed(envelopes))
        if not state["injected"]:
            copies = [{**e, "guid": new_guid()} for e in envelopes if e["guid"] in delayed]
            if copies:
                state["injected"] = True
                out.extend(copies)
        return out

    every_sent = sent_ciphertexts(ann_capture, ben["username"])
    assert len(every_sent) == len(set(every_sent)), "two envelopes the client sent carry the same ciphertext"
    ben_tab = ben_context.new_page()
    interception = route_messages(ben_tab, rewrite)
    ben_tab.goto(f"/chats/{ann['username']}")
    ensure_unlocked(ben_tab, ben["password"], "composer-input")
    draft = f"typing while decrypting {token_hex(3)}"
    composer = by_testid(ben_tab, "composer-input").first
    composer.click()
    ben_tab.keyboard.type(draft, delay=15)
    typed = composer.evaluate("e => e.value !== undefined ? e.value : e.textContent")
    assert typed == draft, f"the composer holds {typed!r} after typing during decryption"
    composer.fill("")
    assert wait_until(lambda: all(bubble(ben_tab, t, "in").count() > 0 for t in (texts[0], texts[2])), 45), \
        "messages around the gap never arrived"
    assert bubble(ben_tab, texts[1]).count() == 0, "the delayed message appeared before it was released"
    state["release"] = True
    assert wait_until(lambda: bubble(ben_tab, texts[1], "in").count() > 0, 45), "the delayed message never appeared"
    pump(ben_tab, 6)
    shown = [t for t in message_texts(ben_tab) if t in texts or t == same]
    assert shown.count(same) == 2, f"the two identical messages show {shown.count(same)} times"
    for text in texts:
        assert shown.count(text) == 1, f"{text!r} shows {shown.count(text)} times"
    positions = [shown.index(t) for t in texts]
    assert positions == sorted(positions), f"messages show out of written order: {shown}"
    assert interception.served > 0, "the recipient browser never requested GET /api/messages"


def test_safety_numbers_match_and_identity_change_blocks_send(browser_page):
    """Both sides see one sixty-digit safety number; a newly linked device changes it and blocks sending until accepted."""
    ann, ben = fresh_account("ann"), fresh_account("ben")
    ann_context, ann_capture = browser_page.open()
    ann_tab = ann_context.new_page()
    ui_login(ann_tab, ann["email"], ann["password"])
    ben_context, _ = browser_page.open()
    ben_tab = ben_context.new_page()
    ui_login(ben_tab, ben["email"], ben["password"])
    ann_view = safety_digits(ann_tab, ben["username"], ann["password"])
    ben_view = safety_digits(ben_tab, ann["username"], ben["password"])
    assert len(ann_view) == 60, f"safety number has {len(ann_view)} digits"
    assert ann_view == ben_view, "the two people see different safety numbers"
    hello = f"first contact {token_hex(4)}"
    open_chat(ann_tab, ben["username"], ann["password"])
    send_text(ann_tab, hello)
    assert wait_sent(ann_tab, hello, 45), "the first message never reached Sent"
    open_chat(ben_tab, ann["username"], ben["password"])
    assert wait_until(lambda: bubble(ben_tab, hello, "in").count() > 0, 45), "the first message never arrived"
    ben_tab.goto("/settings/devices")
    ensure_unlocked(ben_tab, ben["password"])
    by_testid(ben_tab, "link-code-create").click()
    assert wait_until(lambda: re.fullmatch(r"[A-Z0-9]{8}", by_testid(ben_tab, "link-code-value").inner_text().strip() or ""), 20)
    code = by_testid(ben_tab, "link-code-value").inner_text().strip()
    new_context, _ = browser_page.open()
    new_tab = new_context.new_page()
    ui_login(new_tab, ben["email"], ben["password"])
    new_tab.wait_for_url(re.compile(r"/link(/|\\?|$)"), timeout=20000)
    by_testid(new_tab, "link-code-input").fill(code)
    by_testid(new_tab, "link-code-submit").click()
    new_tab.wait_for_url(re.compile(r"/chats(/|\\?|$)"), timeout=30000)
    open_chat(ann_tab, ben["username"], ann["password"])
    banner = by_testid(ann_tab, "identity-change-banner")
    blocked = f"blocked {token_hex(4)}"
    composer = by_testid(ann_tab, "composer-input")
    if not banner.count() and composer.count() and composer.first.is_editable():
        composer.first.fill(blocked)
        if by_testid(ann_tab, "composer-send").first.is_enabled():
            by_testid(ann_tab, "composer-send").first.click()
    assert wait_until(lambda: banner.count() > 0 and banner.first.is_visible(), 45), "no changed-identity warning appeared"
    colours = element_colours(banner.first)
    ambers = [c for c in colours if c[3] > 0 and 15 <= hue_chroma(c)[0] <= 65 and hue_chroma(c)[1] >= 0.18]
    assert ambers, f"the changed-identity warning wears no amber: {colours[:8]}"
    before_puts = len(put_requests_to(ann_capture, ben["username"]))
    if composer.count() and composer.first.is_editable() and bubble(ann_tab, blocked).count() == 0:
        composer.first.fill(blocked)
        send = by_testid(ann_tab, "composer-send").first
        if send.is_enabled():
            send.click()
    pump(ann_tab, 6)
    assert bubble_status(ann_tab, blocked) not in STATUSES[1:], "a message was accepted before the identity change was accepted"
    accepted_puts = [r for r in put_requests_to(ann_capture, ben["username"])[before_puts:]]
    assert not any(blocked in str(r) for r in accepted_puts), "a blocked message left the browser readable"
    new_tab.goto(f"/chats/{ann['username']}")
    ensure_unlocked(new_tab, ben["password"], ("composer-input", "identity-change-banner"))
    pump(new_tab, 3)
    assert bubble(new_tab, blocked).count() == 0, "a blocked message reached the contact's new browser"
    by_testid(ann_tab, "identity-change-accept").first.click()
    assert wait_until(lambda: banner.count() == 0 or not banner.first.is_visible(), 15), "accepting did not clear the warning"
    after = f"after accept {token_hex(4)}"
    send_text(ann_tab, after)
    assert wait_sent(ann_tab, after, 45), "sending after accepting never reached Sent"
    assert wait_until(lambda: bubble(new_tab, after, "in").count() > 0, 45), "ben's linked browser never received the message"
    ann_again = safety_digits(ann_tab, ben["username"], ann["password"])
    new_view = safety_digits(new_tab, ann["username"], ben["password"])
    assert ann_again == new_view, "after the change the two sides see different safety numbers"
    assert ann_again != ann_view, "the safety number did not change with ben's new device"
    open_chat(new_tab, ann["username"], ben["password"])
    ben_tab.goto("/settings/devices")
    ensure_unlocked(ben_tab, ben["password"])
    ben_tab.locator('[data-testid="device-row"][data-device-id="2"] [data-testid="device-unlink"]').first.click()
    by_testid(ben_tab, "device-unlink-confirm").first.click()
    new_tab.wait_for_url(re.compile(r"/login(/|\\?|$)"), timeout=45000)
    assert wait_until(lambda: UNLINKED_BANNER in new_tab.locator("body").inner_text(), 15), \
        "the unlinked browser returned to sign-in without the unlinked banner"
    assert not leaks(storage_dump(new_tab), after), "the unlinked browser kept its stored conversation"


def test_browser_store_holds_no_readable_text_and_asks_to_unlock(browser_page):
    """What the browser stores holds no readable message text or profile name, and a reload asks for the password."""
    ann, ben = fresh_account("ann"), fresh_account("ben")
    ben_context, _ = browser_page.open()
    ben_tab = ben_context.new_page()
    ui_login(ben_tab, ben["email"], ben["password"])
    ann_context, _ = browser_page.open()
    ann_tab = ann_context.new_page()
    ui_login(ann_tab, ann["email"], ann["password"])
    profile_name = f"Stored Name {token_hex(3)}"
    ui_set_profile_name(ann_tab, profile_name, ann["password"])
    text = f"kept at rest {token_hex(6)}"
    open_chat(ann_tab, ben["username"], ann["password"])
    send_text(ann_tab, text)
    assert wait_sent(ann_tab, text, 45)
    open_chat(ben_tab, ann["username"], ben["password"])
    assert wait_until(lambda: bubble(ben_tab, text, "in").count() > 0, 45), "the message never arrived"
    assert wait_until(lambda: profile_name in by_testid(ben_tab, "conversation-title").inner_text(), 30)
    settle(3)
    for tab in (ann_tab, ben_tab):
        dump = storage_dump(tab)
        assert not leaks(dump, text), "browser storage holds the message text readable"
        assert not leaks(dump, profile_name), "browser storage holds the profile name readable"
    ben_tab.reload()
    ben_tab.wait_for_url(re.compile(r"/unlock(/|\\?|$)"), timeout=20000)
    fresh_tab = ben_context.new_page()
    fresh_tab.goto(f"/chats/{ann['username']}")
    fresh_tab.wait_for_url(re.compile(r"/unlock(/|\\?|$)"), timeout=20000)
    ensure_unlocked(fresh_tab, ben["password"], "composer-input")
    assert path_of(fresh_tab) == f"/chats/{ann['username']}", f"unlocking returned to {path_of(fresh_tab)}"
    fresh_tab.goto("/chats")
    ensure_unlocked(fresh_tab, ben["password"], "new-chat")
    opener = by_testid(fresh_tab, "new-chat").first
    opener.click()
    by_testid(fresh_tab, "new-chat-username").first.fill(f"nobody_{token_hex(4)}")
    by_testid(fresh_tab, "new-chat-start").first.click()
    pump(fresh_tab, 3)
    assert not path_of(fresh_tab).startswith("/chats/nobody_"), "a conversation opened for a username with no account"
    assert visible_testid(fresh_tab, "new-chat-username"), "the new chat dialog closed without saying the username has no account"
    fresh_tab.keyboard.press("Escape")
    assert wait_until(lambda: not visible_testid(fresh_tab, "new-chat-username"), 5), "Escape did not close the new chat dialog"
    assert fresh_tab.evaluate("() => !!document.activeElement.closest('[data-testid=\"new-chat\"]')"), "focus did not return to New chat"
    probe = Person("probe")
    assert len(bundle(probe.token, ben["username"]).json().get("devices", [])) == 1, "ben's browser is not a registered device"
    fresh_tab.goto("/settings/devices")
    ensure_unlocked(fresh_tab, ben["password"], "sign-out")
    by_testid(fresh_tab, "sign-out").first.click()
    by_testid(fresh_tab, "sign-out-confirm").first.click()
    fresh_tab.wait_for_url(re.compile(r"/login(/|\\?|$)"), timeout=30000)
    assert wait_until(lambda: bundle(probe.token, ben["username"]).json().get("devices") == [], 20), "signing out left the browser's device linked"
    assert not leaks(storage_dump(fresh_tab), text) and ann["username"] not in storage_dump(fresh_tab), "signing out left the browser store in place"
