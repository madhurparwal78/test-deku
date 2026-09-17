from __future__ import annotations

import datetime as dt
import json
import os
import re
from urllib.parse import urlparse

import httpx
from appclient import app_url
from conftest import (
    BANNER_PHRASE, CHANNEL, CLIENT_ERRORS, DENIALS, DEPTH, KEY_ACK, LINK_EXPIRED,
    OPERATOR_EMAIL, PASSWORD, PIECE_CLASSES, PUBLIC_ROUTES, QUOTA_BYTES, SECTION_IDS,
    SEEDED_EPOCHS, SEEDED_RELAYS, STAGES, TREASURER_EMAIL, UNOPENABLE,
    WAITING_APPROVAL, WAITLIST_ACCEPTED, WAITLIST_CONFIRMED, WAITLIST_REMOVED,
    WAITLIST_SUBJECT, WAITLIST_USED, WHITELIST_APPLIED, WHITELIST_SUBJECT, Wallet,
    Wire, app_page, b64, barrier_run, body, challenge, client, conversation,
    conversation_state, database_holds, devices_of, envelope_payload, expect,
    expected_epoch, fresh_rates, history, iso, leak_forms, login, mails_to, me,
    member_with_device, membership, now_utc, open_workspace, parse_time,
    pay_in_full, payment_event, payments, post_envelope, post_rate, quote,
    register_device, settle, signed_body, signup, sync_all, unique, unique_email,
    vested, wait_for_mail, wait_for_text, warm_clients, watcher_post, WATCHER_SEED, ed_sign,
)


def _desktop(browser_page, **extra):
    return browser_page.new_context(viewport={"width": 1280, "height": 800}, **extra)


def _intro_showing(page) -> bool:
    region = page.get_by_role("region", name="Introduction")
    return region.count() > 0 and region.first.is_visible()


def _visible_with_text(page, text: str) -> int:
    return page.evaluate(
        "t => Array.from(document.querySelectorAll('body *')).filter(e => e.textContent.trim() === t"
        " && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden').length", text)


def _visible_box_x(page, phrase: str):
    return page.evaluate(
        "p => { const hit = Array.from(document.querySelectorAll('body *')).find(e => e.children.length === 0"
        " && e.textContent.includes(p) && e.getClientRects().length > 0); return hit ? hit.getBoundingClientRect().x : null; }",
        phrase)


def _scrolls(page) -> bool:
    page.mouse.move(640, 400)
    page.mouse.wheel(0, 1600)
    page.wait_for_timeout(1500)
    return page.evaluate("() => window.scrollY") > 0


def test_skip_is_first_focus_and_deep_links_or_returning_visits_show_no_intro(browser_page):
    ctx = _desktop(browser_page)
    page = ctx.new_page()
    page.goto(f"{app_url()}/")
    page.wait_for_load_state("domcontentloaded")
    assert _intro_showing(page), "a first visit to / shows no region labelled Introduction"
    page.keyboard.press("Tab")
    focused = page.evaluate(
        "() => { const e = document.activeElement; if (!e) return '';"
        " return (e.getAttribute('aria-label') || e.innerText || e.value || '').trim(); }")
    assert "Skip the intro" in focused, (
        f"the first Tab on / focuses {focused!r}, expected the Skip the intro control")
    page.keyboard.press("Enter")
    for _ in range(20):
        if not _intro_showing(page):
            break
        page.wait_for_timeout(250)
    assert not _intro_showing(page), "pressing Enter on Skip the intro left the introduction showing"
    assert _scrolls(page), "after skipping the introduction the page does not scroll"
    page.reload()
    page.wait_for_load_state("load")
    page.wait_for_timeout(1000)
    assert not _intro_showing(page), "a returning visitor who skipped once sees the introduction again"
    ctx.close()

    ctx2 = _desktop(browser_page)
    deep = ctx2.new_page()
    deep.goto(f"{app_url()}/#tokenSaleSection")
    deep.wait_for_load_state("load")
    deep.wait_for_timeout(1500)
    assert not _intro_showing(deep), "arriving at /#tokenSaleSection shows the introduction"
    top = deep.evaluate(
        "() => { const e = document.getElementById('tokenSaleSection');"
        " return e ? e.getBoundingClientRect().top : null; }")
    assert top is not None and -400 <= top <= 400, (
        f"arriving at /#tokenSaleSection leaves the section at offset {top}, not in view")
    deep.locator('a[href$="#aboutSection"]:visible').first.click()
    deep.wait_for_timeout(1500)
    assert deep.url.endswith("#aboutSection"), f"choosing About leaves the address at {deep.url}"
    deep.go_back()
    deep.wait_for_timeout(1500)
    assert deep.url.endswith("#tokenSaleSection"), (
        f"Back after choosing About leaves the address at {deep.url}, not #tokenSaleSection")
    ctx2.close()


def test_page_without_scripts_shows_every_section_and_scrolls(browser_page):
    ctx = _desktop(browser_page, java_script_enabled=False)
    page = ctx.new_page()
    page.goto(f"{app_url()}/")
    page.wait_for_load_state("load")
    assert not _intro_showing(page), "with scripts unavailable an introduction overlay covers /"
    for section in SECTION_IDS:
        found = page.locator(f"#{section}")
        assert found.count() == 1, f"with scripts unavailable / carries no #{section}"
        seen = found.evaluate(
            "e => { let o = 1; let n = e; while (n && n.nodeType === 1) {"
            " const s = getComputedStyle(n); o *= parseFloat(s.opacity);"
            " if (s.visibility === 'hidden' || s.display === 'none') return 0; n = n.parentElement; }"
            " return o; }")
        assert seen > 0.5, f"with scripts unavailable #{section} renders at opacity {seen}"
        words = found.inner_text().strip()
        assert len(words) > 20, f"with scripts unavailable #{section} carries no readable text"
    assert _scrolls(page), "with scripts unavailable / does not scroll"
    ctx.close()

PHONE = {"width": 390, "height": 844}

ROW_OF_LABELS = """(root, names) => {
  const shown = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const found = names.map(n => [...root.querySelectorAll('*')].filter(e => shown(e)
    && e.textContent.trim() === n && ![...e.children].some(c => c.textContent.trim() === n))
    .map(e => { const r = e.getBoundingClientRect(); return {left: r.left, right: r.right, mid: r.top + r.height / 2}; }));
  return found;
}"""


def _one_row(found: list[list[dict]], tolerance: float) -> list[dict] | None:
    for anchor in found[0] if found else []:
        row = []
        for matches in found:
            near = [m for m in matches if abs(m["mid"] - anchor["mid"]) <= tolerance]
            if not near:
                break
            row.append(near[0])
        else:
            return row
    return None


def test_phone_intro_keeps_skip_on_screen_and_its_stage_labels_in_one_row(browser_page):
    ctx = browser_page.new_context(viewport=PHONE)
    page = ctx.new_page()
    page.goto(f"{app_url()}/")
    page.wait_for_load_state("load")
    page.wait_for_timeout(1500)
    assert _intro_showing(page), "a first visit to / at phone width shows no region labelled Introduction"
    skip = page.get_by_role("button", name="Skip the intro", exact=True).first
    box = skip.bounding_box()
    assert box and box["x"] >= 0 and box["y"] >= 0 and box["x"] + box["width"] <= PHONE["width"] + 1 and (
        box["y"] + box["height"] <= PHONE["height"] + 1), f"at phone width Skip the intro sits at {box}, off screen"
    region = page.get_by_role("region", name="Introduction").first
    found = region.evaluate(ROW_OF_LABELS, list(STAGES))
    missing = [name for name, matches in zip(STAGES, found) if not matches]
    assert not missing, f"at phone width the introduction shows no label for {missing}"
    row = _one_row(found, 12)
    assert row, f"at phone width the six stage labels do not share one row: {found}"
    lefts = [m["left"] for m in row]
    assert lefts == sorted(lefts), f"at phone width the stage labels run out of order: {lefts}"
    wide = page.evaluate("() => document.documentElement.scrollWidth")
    assert wide <= PHONE["width"] + 1, f"at phone width the introduction widens the page to {wide} pixels"
    ctx.close()


def test_reduced_motion_shows_stills_and_a_still_banner_read_once(browser_page):
    ctx = _desktop(browser_page, reduced_motion="reduce")
    page = ctx.new_page()
    page.goto(f"{app_url()}/")
    page.wait_for_load_state("load")
    page.wait_for_timeout(1000)
    missing = [s for s in STAGES if _visible_with_text(page, s) == 0]
    assert not missing, f"under reduced motion these intro stages are not shown as stills: {missing}"
    assert _scrolls(page), "under reduced motion the page does not scroll"
    first = _visible_box_x(page, BANNER_PHRASE)
    page.wait_for_timeout(1500)
    second = _visible_box_x(page, BANNER_PHRASE)
    assert first is not None and second is not None and abs(first - second) < 1, (
        f"under reduced motion the banner moved from {first} to {second}")
    ctx.close()

    moving = _desktop(browser_page)
    normal = moving.new_page()
    normal.goto(f"{app_url()}/#aboutSection")
    normal.wait_for_load_state("load")
    normal.wait_for_timeout(1000)
    spoken = normal.locator("body").aria_snapshot().lower().count(BANNER_PHRASE.lower())
    assert spoken == 1, f"assistive technology is given the banner phrase {spoken} times, expected once"
    moving.close()


def test_first_public_page_load_stays_inside_the_byte_budget(browser_page):
    ctx = _desktop(browser_page)
    page = ctx.new_page()
    finished = []
    page.on("requestfinished", lambda request: finished.append(request))
    page.goto(f"{app_url()}/", wait_until="load")
    origin = urlparse(app_url()).netloc
    total = scripts = fonts = 0
    foreign, media, pngs, old_fonts = [], [], [], []
    for request in list(finished):
        url = urlparse(request.url)
        if url.scheme in ("data", "blob"):
            continue
        if url.netloc != origin:
            foreign.append(request.url)
        size = max(request.sizes().get("responseBodySize", 0), 0)
        total += size
        kind = request.resource_type
        response = request.response()
        mime = (response.headers.get("content-type", "") if response else "").lower()
        if kind == "script":
            scripts += size
        if kind == "font":
            fonts += size
            if not (url.path.endswith(".woff2") or "woff2" in mime):
                old_fonts.append(request.url)
        if kind == "media" or mime.startswith("video/") or mime.startswith("audio/"):
            media.append(request.url)
        if mime.startswith("image/png") or url.path.lower().endswith(".png"):
            pngs.append(request.url)
    assert not foreign, f"the first load of / fetches from other origins: {foreign[:5]}"
    assert not media, f"the first load of / fetches video or audio: {media[:5]}"
    assert not pngs, f"the first load of / fetches PNG images: {pngs[:5]}"
    assert not old_fonts, f"the first load of / fetches fonts that are not woff2: {old_fonts[:5]}"
    assert total <= 250000, f"the first load of / fetches {total} bytes before load, over 250000"
    assert scripts <= 150000, f"the first load of / fetches {scripts} bytes of script, over 150000"
    assert fonts <= 120000, f"the first load of / fetches {fonts} bytes of fonts, over 120000"
    ctx.close()


def _waitlist(email: str, **extra):
    payload = {"email": email, "consent": True, "website": ""}
    payload.update(extra)
    with client() as c:
        return c.post("/waitlist", json=payload)


def _path_link(text: str, route: str) -> str | None:
    found = re.search(r"https?://[^\s<>\"]+" + re.escape(route) + r"\?token=[^\s<>\"]+", text)
    if not found:
        return None
    link = urlparse(found.group(0))
    return f"{link.path}?{link.query}"


def test_waitlist_confirmation_email_reaches_only_the_requester():
    address = unique_email()
    accepted = expect(_waitlist(address), (200, 201, 202), "waitlist request")
    assert accepted.get("message") == WAITLIST_ACCEPTED, (
        f"the waitlist answered {accepted}, expected message {WAITLIST_ACCEPTED!r}")
    mails = wait_for_mail(address, WAITLIST_SUBJECT)
    assert len(mails) == 1, f"{len(mails)} confirmation emails reached {address}, expected one"
    mail = mails[0]
    assert mail["to"] == [address.lower()], f"the confirmation is addressed to {mail['to']}"
    assert not mail["cc"] and not mail["bcc"], (
        f"the confirmation carries cc {mail['cc']} or bcc {mail['bcc']}")
    first_line = mail["text"].strip().splitlines()[0].strip()
    assert "/waitlist/confirm?token=" in first_line, (
        f"the confirmation body begins {first_line!r}, not with the confirmation link")
    confirm = _path_link(first_line, "/waitlist/confirm")
    remove = _path_link(mail["text"], "/waitlist/remove")
    assert confirm and remove, f"the confirmation email lacks a confirm or removal link: {mail['text'][:300]}"
    once = app_page(confirm)
    assert WAITLIST_CONFIRMED in once.text, f"opening the confirmation link shows {once.text[:200]!r}"
    twice = app_page(confirm)
    assert WAITLIST_USED in twice.text, f"opening the confirmation link again shows {twice.text[:200]!r}"
    gone = app_page(remove)
    assert WAITLIST_REMOVED in gone.text, f"opening the removal link shows {gone.text[:200]!r}"


def test_simultaneous_waitlist_requests_send_one_confirmation_email():
    address = unique_email()
    clients = warm_clients([None] * 6)
    payload = {"email": address, "consent": True, "website": ""}
    results = barrier_run(6, lambda i: clients[i].post("/waitlist", json=payload))
    for c in clients:
        c.close()
    statuses = [r.status_code for r in results if r is not None]
    assert len(statuses) == 6 and all(s < 500 for s in statuses), (
        f"six simultaneous waitlist requests answered {statuses}")
    settle(4.0)
    again = _waitlist(address)
    assert again.status_code < 500, f"a later waitlist request answered {again.status_code}"
    settle(3.0)
    mails = mails_to(address, WAITLIST_SUBJECT)
    assert len(mails) == 1, (
        f"{len(mails)} confirmation emails reached {address} after seven requests, expected one")


def test_waitlist_refuses_extra_fields_missing_consent_and_a_filled_decoy():
    extra, no_consent, missing, decoy, invalid = (unique_email() for _ in range(5))
    cases = [
        ("an extra field", _waitlist(extra, name="Ada")),
        ("consent false", _waitlist(no_consent, consent=False)),
        ("decoy filled", _waitlist(decoy, website="https://offers.example.com")),
    ]
    with client() as c:
        cases.append(("consent missing", c.post("/waitlist", json={"email": missing, "website": ""})))
    cases.append(("an invalid address", _waitlist("not-an-address")))
    for label, response in cases:
        assert response.status_code in CLIENT_ERRORS, (
            f"a waitlist request with {label} answered {response.status_code}: {response.text[:200]}")
    settle(4.0)
    for address in (extra, no_consent, missing, decoy):
        assert not mails_to(address, WAITLIST_SUBJECT), f"a refused waitlist request still mailed {address}"


def test_invalid_signup_email_is_named_inline_and_stores_no_account(browser_page):
    ctx = _desktop(browser_page)
    page = ctx.new_page()
    page.goto(f"{app_url()}/signup")
    page.get_by_label("Email", exact=True).fill("not-an-address")
    page.get_by_label("Password", exact=True).fill(PASSWORD)
    page.get_by_role("button", name="Create account", exact=True).click()
    page.wait_for_timeout(2000)
    assert "/signup" in page.url, f"an invalid signup email moved the page to {page.url}"
    messages = page.evaluate(
        "() => Array.from(document.querySelectorAll('body *')).filter(e => e.children.length === 0"
        " && e.offsetParent !== null && !['LABEL','INPUT','BUTTON'].includes(e.tagName))"
        ".map(e => e.textContent.trim()).filter(t => /email/i.test(t) && /(valid|invalid)/i.test(t))")
    assert messages, "an invalid signup email shows no inline message naming the Email field"
    ctx.close()
    with client() as c:
        refused = c.post("/auth/signup", json={"email": "not-an-address", "password": PASSWORD})
        assert refused.status_code in CLIENT_ERRORS, (
            f"signup with not-an-address answered {refused.status_code}")
        no_login = c.post("/auth/login", json={"email": "not-an-address", "password": PASSWORD})
        assert no_login.status_code in CLIENT_ERRORS, "an account exists for not-an-address"


def test_public_images_carry_alternative_text_or_declare_decoration(browser_page):
    ctx = _desktop(browser_page)
    page = ctx.new_page()
    offenders = []
    for route in ("/", "/whitelist", "/network-limits", "/whitepaper"):
        page.goto(f"{app_url()}{route}")
        page.wait_for_load_state("load")
        found = page.evaluate(
            "() => { const out = [];"
            " document.querySelectorAll('img').forEach(i => { if (i.getAttribute('alt') === null)"
            " out.push('img ' + (i.getAttribute('src') || '')); });"
            " document.querySelectorAll('svg').forEach(s => { if (s.closest('[aria-hidden=\"true\"]')) return;"
            " if (s.parentElement && s.parentElement.closest('svg')) return;"
            " const named = (s.getAttribute('aria-label') || '').trim() || s.getAttribute('aria-labelledby')"
            " || (s.querySelector(':scope > title') && s.querySelector(':scope > title').textContent.trim());"
            " const role = s.getAttribute('role');"
            " if (!named && role !== 'presentation' && role !== 'none') out.push('svg ' + s.outerHTML.slice(0, 60)); });"
            " return out; }")
        offenders.extend(f"{route}: {o}" for o in found)
    ctx.close()
    assert not offenders, f"images without alternative text or a decorative declaration: {offenders[:6]}"

NAV_BAR = """() => {
  const labels = ['About', 'Features', 'Ecosystem', 'Token Sale', 'Subscribe'];
  const links = [...document.querySelectorAll('a')].filter(a => labels.includes(a.textContent.trim()));
  if (!links.length) return null;
  const chain = [];
  let node = links[0].parentElement;
  let position = 'static';
  while (node && node !== document.body) {
    chain.push(node);
    position = getComputedStyle(node).position;
    if (position === 'fixed' || position === 'sticky') break;
    node = node.parentElement;
  }
  if (!node || node === document.body) return {position: 'static'};
  return {position, backgrounds: chain.map(e => getComputedStyle(e).backgroundColor),
          labels: links.map(a => ({text: a.textContent.trim(), color: getComputedStyle(a).color}))};
}"""


def _rgb(value: str) -> tuple[float, float, float, float] | None:
    m = re.match(r"rgba?\(([^)]*)\)", value or "")
    if not m:
        return None
    parts = [p.strip() for p in m.group(1).replace("/", ",").split(",") if p.strip()]
    if len(parts) < 3:
        return None
    r, g, b = (float(p) for p in parts[:3])
    alpha = 1.0
    if len(parts) > 3:
        alpha = float(parts[3].rstrip("%")) / (100 if parts[3].endswith("%") else 1)
    return r, g, b, alpha


def _luminance(rgb) -> float:
    out = []
    for channel in rgb[:3]:
        c = channel / 255
        out.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def _contrast(a, b) -> float:
    la, lb = _luminance(a), _luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def test_floating_navigation_has_an_opaque_backing_and_legible_labels(browser_page):
    ctx = _desktop(browser_page)
    page = ctx.new_page()
    page.goto(f"{app_url()}/")
    page.wait_for_load_state("load")
    bar = page.evaluate(NAV_BAR)
    assert bar and bar.get("position") in ("fixed", "sticky"), f"the navigation bar is not fixed or sticky: {bar}"
    grounds = [_rgb(b) for b in bar["backgrounds"]]
    ground = next((g for g in grounds if g and g[3] >= 0.999), None)
    assert ground, f"no opaque background sits between the labels and the fixed bar: {bar['backgrounds']}"
    names = {label["text"] for label in bar["labels"]}
    assert {"About", "Features", "Ecosystem", "Token Sale", "Subscribe"} <= names, f"the bar carries {sorted(names)}"
    for label in bar["labels"]:
        ink = _rgb(label["color"])
        ratio = _contrast(ink, ground) if ink else 0
        assert ratio >= 4.5, f"the label {label['text']} reads at contrast {ratio:.2f} against the bar"
    ctx.close()


def test_unknown_address_answers_not_found_and_the_sitemap_lists_public_routes():
    health = httpx.get(f"{app_url()}/api/health", timeout=30)
    assert health.status_code == 200, f"GET /api/health returned {health.status_code}"
    missing = httpx.get(f"{app_url()}/{unique('no-such-page')}", timeout=30)
    assert missing.status_code == 404, f"an unknown address answered {missing.status_code}"
    assert "Page not found" in missing.text and "Back to Nightjar" in missing.text, (
        f"the not-found page reads {missing.text[:200]!r}")
    sitemap = httpx.get(f"{app_url()}/sitemap.xml", timeout=30)
    assert sitemap.status_code == 200, f"/sitemap.xml answered {sitemap.status_code}"
    locations = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap.text)
    assert locations and all(loc.startswith("http") for loc in locations), (
        f"the sitemap lists {locations[:5]}, expected absolute addresses")
    paths = {urlparse(loc).path or "/" for loc in locations}
    assert set(PUBLIC_ROUTES) <= paths, f"the sitemap lacks {sorted(set(PUBLIC_ROUTES) - paths)}"
    assert not [p for p in paths if p.startswith("/app")], "the sitemap lists workspace addresses"
    robots = httpx.get(f"{app_url()}/robots.txt", timeout=30)
    assert robots.status_code == 200, f"/robots.txt answered {robots.status_code}"
    assert re.search(r"^Sitemap:\s*https?://\S+/sitemap\.xml\s*$", robots.text, re.M), (
        f"robots.txt names no absolute sitemap: {robots.text[:200]!r}")
    assert re.search(r"^Disallow:\s*/app", robots.text, re.M), "robots.txt does not disallow /app"


def test_used_wallet_challenge_is_denied_a_second_session():
    wallet = Wallet()
    signed = signed_body(wallet, "sign_in")
    with client() as c:
        first = expect(c.post("/auth/wallet/verify", json=signed), (200, 201), "wallet verify")
        assert first.get("access_token") and first.get("created") is True, (
            f"a first wallet sign-in answered {first}")
        replay = c.post("/auth/wallet/verify", json=signed)
    assert replay.status_code in CLIENT_ERRORS, (
        f"replaying a used challenge answered {replay.status_code}: {replay.text[:200]}")
    assert not body(replay).get("access_token"), "replaying a used challenge issued a token"
    assert wallet.address in me(first["access_token"]).get("wallets", []), (
        "the wallet-created account does not list its wallet")


def test_simultaneous_wallet_verifications_issue_one_session():
    wallet = Wallet()
    signed = signed_body(wallet, "sign_in")
    clients = warm_clients([None] * 6)
    results = barrier_run(6, lambda i: clients[i].post("/auth/wallet/verify", json=signed))
    for c in clients:
        c.close()
    statuses = [r.status_code for r in results if r is not None]
    winners = [r for r in results if r is not None and r.status_code in (200, 201)
               and body(r).get("access_token")]
    assert len(winners) == 1, f"six simultaneous uses of one challenge answered {statuses}"
    assert all(s < 500 for s in statuses), f"simultaneous verifications answered {statuses}"
    with client() as c:
        again = expect(c.post("/auth/wallet/verify", json=signed_body(wallet, "sign_in")),
                       (200, 201), "a fresh wallet sign-in")
    assert again["account_id"] == body(winners[0])["account_id"], (
        "a wallet signed in twice reached two different accounts")


def test_wallet_challenge_is_bound_to_address_purpose_and_expiry(backend):
    wallet, stranger = Wallet(), Wallet()
    with client() as c:
        ch = challenge(wallet, "sign_in")
        wrong_key = c.post("/auth/wallet/verify", json={
            "challenge_id": ch["challenge_id"], "address": wallet.address,
            "signature": stranger.sign(ch["message"])})
        assert wrong_key.status_code in CLIENT_ERRORS, (
            f"a signature from another key answered {wrong_key.status_code}")
        wrong_address = c.post("/auth/wallet/verify", json={
            "challenge_id": ch["challenge_id"], "address": stranger.address,
            "signature": stranger.sign(ch["message"])})
        assert wrong_address.status_code in CLIENT_ERRORS, (
            f"a challenge presented for another address answered {wrong_address.status_code}")
        altered = ch["message"].replace(urlparse(app_url()).hostname or "", "elsewhere.example.com")
        other_text = c.post("/auth/wallet/verify", json={
            "challenge_id": ch["challenge_id"], "address": wallet.address,
            "signature": wallet.sign(altered + "\nextra")})
        assert other_text.status_code in CLIENT_ERRORS, (
            f"a signature over a different message answered {other_text.status_code}")
        purpose = c.post("/auth/wallet/verify", json=signed_body(wallet, "whitelist"))
        assert purpose.status_code in CLIENT_ERRORS, (
            f"a whitelist challenge presented for sign-in answered {purpose.status_code}")
        stale = challenge(wallet, "sign_in")
        backend.query("UPDATE wallet_challenges SET expires_at = now() - interval '1 minute' "
                      "WHERE id::text = %s", (stale["challenge_id"],))
        expired = c.post("/auth/wallet/verify", json={
            "challenge_id": stale["challenge_id"], "address": wallet.address,
            "signature": wallet.sign(stale["message"])})
        assert expired.status_code in CLIENT_ERRORS, (
            f"an expired challenge answered {expired.status_code}")
        fine = c.post("/auth/wallet/verify", json=signed_body(wallet, "sign_in"))
        assert fine.status_code in (200, 201), (
            f"a fresh valid challenge answered {fine.status_code}: {fine.text[:200]}")


def test_connected_wallet_signs_into_the_same_account_and_its_trial_is_not_repeated():
    first = signup()
    wallet = Wallet()
    with client(first["access_token"]) as c:
        connected = expect(c.post("/me/wallets", json=signed_body(wallet, "connect")),
                           (200, 201), "connect wallet")
    assert wallet.address in connected.get("wallets", []), f"connecting answered {connected}"
    with client() as c:
        signed_in = expect(c.post("/auth/wallet/verify", json=signed_body(wallet, "sign_in")),
                           (200, 201), "wallet sign-in after connect")
    assert signed_in["account_id"] == first["account_id"], (
        "wallet sign-in after connecting reached a second account")
    assert signed_in.get("created") is False, f"wallet sign-in after connecting answered {signed_in}"
    second = signup()
    with client(second["access_token"]) as c:
        taken = c.post("/me/wallets", json=signed_body(wallet, "connect"))
    assert taken.status_code in CLIENT_ERRORS, (
        f"connecting a wallet attached elsewhere answered {taken.status_code}")
    assert wallet.address not in me(second["access_token"]).get("wallets", []), (
        "a refused connection still attached the wallet")
    with client(first["access_token"]) as c:
        expect(c.delete(f"/me/wallets/{wallet.address}"), (200, 204), "detach wallet")
    with client() as c:
        fresh = expect(c.post("/auth/wallet/verify", json=signed_body(wallet, "sign_in")),
                       (200, 201), "wallet sign-in after detaching")
    assert fresh.get("created") is True and fresh["account_id"] != first["account_id"], (
        f"wallet sign-in after detaching answered {fresh}")
    repeat = membership(fresh["access_token"])
    assert repeat.get("trial_ends_at") is None and repeat.get("state") == "suspended", (
        f"an account made by a wallet that was attached elsewhere got {repeat}")
    new_wallet = Wallet()
    with client() as c:
        newcomer = expect(c.post("/auth/wallet/verify", json=signed_body(new_wallet, "sign_in")),
                          (200, 201), "a new wallet sign-in")
    trial = membership(newcomer["access_token"])
    assert trial.get("trial_ends_at") and trial.get("state") == "trial", (
        f"an account made by a never-attached wallet got {trial}")


def test_signing_out_ends_only_that_session():
    account = signup()
    other = login(account["email"])
    with client(account["access_token"]) as c:
        expect(c.post("/auth/logout"), (200, 202, 204), "logout")
        ended = c.get("/me")
    assert ended.status_code in DENIALS, f"a signed-out token still reads /api/me: {ended.status_code}"
    with client(other) as c:
        assert c.get("/me").status_code == 200, "signing out one session ended another"


def _approve(active_token: str, device_id: str) -> httpx.Response:
    with client(active_token) as c:
        return c.post(f"/devices/{device_id}/approve")


def test_pending_device_cannot_approve_itself_denied():
    account = signup()
    token = account["access_token"]
    first = register_device(token)
    second = register_device(token)
    assert first["state"] == "active", f"the first device registered as {first['state']}"
    assert second["state"] == "pending", f"a second device registered as {second['state']}"
    itself = _approve(second["device_token"], second["device_id"])
    assert itself.status_code in CLIENT_ERRORS, (
        f"a pending device approving itself answered {itself.status_code}")
    by_account = _approve(token, second["device_id"])
    assert by_account.status_code in CLIENT_ERRORS, (
        f"an account token that is no device approving a device answered {by_account.status_code}")
    stranger = member_with_device()
    foreign = _approve(stranger["device"]["device_token"], second["device_id"])
    assert foreign.status_code in CLIENT_ERRORS, (
        f"another account's device approving answered {foreign.status_code}")
    states = {d["device_id"]: d["state"] for d in devices_of(token)}
    assert states.get(second["device_id"]) == "pending", f"device states after refusals: {states}"
    ok = _approve(first["device_token"], second["device_id"])
    assert ok.status_code in (200, 201), f"an active device approving answered {ok.status_code}"
    states = {d["device_id"]: d["state"] for d in devices_of(token)}
    assert states.get(second["device_id"]) == "active", f"device states after approval: {states}"


def test_key_directory_lists_only_active_devices(backend):
    owner = signup()
    token = owner["access_token"]
    active = register_device(token)
    pending = register_device(token)
    removed = register_device(token)
    expect(_approve(active["device_token"], removed["device_id"]), (200, 201), "approve third device")
    with client(active["device_token"]) as c:
        expect(c.delete(f"/devices/{removed['device_id']}"), (200, 204), "remove third device")
    with client(token) as c:
        listing = expect(c.get(f"/directory/{owner['contact_code']}"), (200,), "key directory")
    listed = {d["device_id"] for d in listing.get("devices", [])}
    assert listed == {active["device_id"]}, (
        f"the key directory lists {listed}, expected only the active device {active['device_id']}")
    sender = member_with_device()
    chat = conversation(sender["access_token"], "chat", [owner["contact_code"]])
    payload = envelope_payload(chat["epoch"], [sender["device"]["device_id"], active["device_id"],
                                                pending["device_id"]])
    refused = post_envelope(sender["device"]["device_token"], chat["conversation_id"], payload)
    assert refused.status_code in CLIENT_ERRORS, (
        f"an envelope sealed to a pending device answered {refused.status_code}")
    stored = backend.query("SELECT count(*) AS n FROM envelopes WHERE client_id = %s",
                           (payload["client_id"],))
    assert stored[0]["n"] == 0, "a refused envelope was stored"


def test_removed_device_token_is_refused_and_every_epoch_advances():
    owner = signup()
    token = owner["access_token"]
    first = register_device(token)
    second = register_device(token)
    expect(_approve(first["device_token"], second["device_id"]), (200, 201), "approve")
    peer = member_with_device()
    chat = conversation(token, "chat", [peer["contact_code"]])
    group = conversation(token, "private_group", [peer["contact_code"]])
    before = {c["conversation_id"]: c["epoch"] for c in (chat, group)}
    with client(first["device_token"]) as c:
        expect(c.delete(f"/devices/{second['device_id']}"), (200, 204), "remove device")
    with client(second["device_token"]) as c:
        assert c.get("/me").status_code in DENIALS, "a removed device's token still works"
    for conv_id, epoch in before.items():
        now = conversation_state(token, conv_id)["epoch"]
        assert now == epoch + 1, f"removing a device moved conversation epoch from {epoch} to {now}"
    stale = post_envelope(first["device_token"], chat["conversation_id"],
                          envelope_payload(before[chat["conversation_id"]],
                                           [first["device_id"], peer["device"]["device_id"]]))
    assert stale.status_code in CLIENT_ERRORS, f"an envelope at the old epoch answered {stale.status_code}"


def _send_in_ui(page, conversation_id: str, text: str) -> None:
    page.goto(f"{app_url()}/app/conversations/{conversation_id}")
    page.wait_for_load_state("load")
    composer = page.get_by_label("Message", exact=True)
    composer.wait_for(state="visible", timeout=30000)
    page.wait_for_timeout(1500)
    composer.fill(text)
    page.get_by_role("button", name="Send", exact=True).click()


def test_unapproved_device_cannot_open_messages_until_approved(browser_page):
    sender, reader = signup(), signup()
    ctx_a = _desktop(browser_page)
    page_a = open_workspace(ctx_a, sender["email"])
    ctx_b1 = _desktop(browser_page)
    page_b1 = open_workspace(ctx_b1, reader["email"])
    chat = conversation(sender["access_token"], "chat", [reader["contact_code"]])
    conv = chat["conversation_id"]
    before = unique("before-approval")
    _send_in_ui(page_a, conv, before)
    assert wait_for_text(page_a, before), "the sender's own message never shows in its conversation"
    page_b1.goto(f"{app_url()}/app/conversations/{conv}")
    assert wait_for_text(page_b1, before), "the reader's first device never opens the message"
    ctx_b2 = _desktop(browser_page)
    page_b2 = open_workspace(ctx_b2, reader["email"], first=False)
    assert wait_for_text(page_b2, WAITING_APPROVAL, reload_every=0), (
        "a second device of the reader shows no waiting-for-approval notice")
    page_b2.goto(f"{app_url()}/app/conversations/{conv}")
    assert wait_for_text(page_b2, UNOPENABLE), "the unapproved device shows no unopenable line"
    assert page_b2.get_by_text(before).count() == 0, "an unapproved device opened a message"
    page_b1.goto(f"{app_url()}/app/devices")
    page_b1.get_by_role("button", name="Approve Device 2").click()
    page_b1.wait_for_timeout(2000)
    after = unique("after-approval")
    _send_in_ui(page_a, conv, after)
    assert wait_for_text(page_a, after), "the sender's second message never shows"
    page_b2.goto(f"{app_url()}/app/conversations/{conv}")
    assert wait_for_text(page_b2, after), "the approved device never opens a message sent after approval"
    assert page_b2.get_by_text(before).count() == 0, (
        "the approved device opened a message sent before its approval")
    for ctx in (ctx_a, ctx_b1, ctx_b2):
        ctx.close()


def test_message_text_is_sealed_in_the_browser_and_a_tampered_copy_will_not_open(browser_page, backend):
    sender, reader = signup(), signup()
    ctx_a = _desktop(browser_page)
    wire = Wire(ctx_a)
    page_a = open_workspace(ctx_a, sender["email"])
    ctx_b = _desktop(browser_page)
    page_b = open_workspace(ctx_b, reader["email"])
    chat = conversation(sender["access_token"], "chat", [reader["contact_code"]])
    conv = chat["conversation_id"]
    words = unique("plain-words")
    _send_in_ui(page_a, conv, words)
    assert wait_for_text(page_a, words), "the sender's message never shows"
    page_b.goto(f"{app_url()}/app/conversations/{conv}")
    assert wait_for_text(page_b, words), "the reader never opens the message"
    forms = leak_forms(words)
    assert not wire.carries(forms), f"the sending browser sent the typed words: {wire.carries(forms)}"
    held = database_holds(backend, forms)
    assert not held, f"the database holds the typed words: {held[:4]}"
    page_b.close()
    tampered_words = unique("altered-words")
    _send_in_ui(page_a, conv, tampered_words)
    assert wait_for_text(page_a, tampered_words), "the sender's second message never shows"
    newest = backend.query("SELECT id::text AS id, ciphertext FROM envelopes WHERE "
                           "conversation_id::text = %s ORDER BY accepted_at DESC LIMIT 1", (conv,))
    assert newest, "no envelope row exists for the conversation"
    sealed = newest[0]["ciphertext"]
    middle = len(sealed) // 2
    flipped = sealed[:middle] + ("A" if sealed[middle] != "A" else "B") + sealed[middle + 1:]
    backend.query("UPDATE envelopes SET ciphertext = %s WHERE id::text = %s", (flipped, newest[0]["id"]))
    reopened = ctx_b.new_page()
    reopened.goto(f"{app_url()}/app/conversations/{conv}")
    assert wait_for_text(reopened, words), "the reader lost the first message"
    assert wait_for_text(reopened, UNOPENABLE), "an altered envelope shows no unopenable line"
    assert reopened.get_by_text(tampered_words).count() == 0, "an altered envelope still showed text"
    for ctx in (ctx_a, ctx_b):
        ctx.close()


def test_retried_send_stores_one_envelope_row(backend):
    sender, reader = member_with_device(), member_with_device()
    chat = conversation(sender["access_token"], "chat", [reader["contact_code"]])
    devices = [sender["device"]["device_id"], reader["device"]["device_id"]]
    token = sender["device"]["device_token"]
    payload = envelope_payload(chat["epoch"], devices)
    first = expect(post_envelope(token, chat["conversation_id"], payload), (200, 201), "send")
    again = expect(post_envelope(token, chat["conversation_id"], payload), (200, 201), "retry")
    assert again["envelope_id"] == first["envelope_id"], (
        f"a retried send returned {again['envelope_id']}, the first returned {first['envelope_id']}")
    burst = envelope_payload(chat["epoch"], devices)
    clients = warm_clients([token] * 6)
    results = barrier_run(6, lambda i: clients[i].post(
        f"/conversations/{chat['conversation_id']}/envelopes", json=burst))
    for c in clients:
        c.close()
    statuses = [r.status_code for r in results if r is not None]
    assert len(statuses) == 6 and all(s in (200, 201, 409) for s in statuses), (
        f"six simultaneous identical sends answered {statuses}")
    ids = {body(r)["envelope_id"] for r in results if r is not None and r.status_code in (200, 201)}
    assert len(ids) == 1, f"simultaneous identical sends returned envelope ids {ids}"
    for cid in (payload["client_id"], burst["client_id"]):
        rows = backend.query("SELECT count(*) AS n FROM envelopes WHERE client_id = %s", (cid,))
        assert rows[0]["n"] == 1, f"client_id {cid} is stored in {rows[0]['n']} envelope rows"


def test_history_orders_by_clock_and_flags_gaps_when_read():
    one, two = member_with_device(), member_with_device()
    chat = conversation(one["access_token"], "chat", [two["contact_code"]])
    conv, epoch = chat["conversation_id"], chat["epoch"]
    devices = [one["device"]["device_id"], two["device"]["device_id"]]
    sends = [(one, "a3", 30, 3), (one, "a1", 10, 1), (two, "b1", 20, 1),
             (two, "b2", 40, 2), (one, "a4", 40, 4)]
    tag = unique("h")
    for who, name, clock, seq in sends:
        payload = envelope_payload(epoch, devices, client_id=f"{tag}-{name}", clock=clock,
                                   sender_seq=seq)
        expect(post_envelope(who["device"]["device_token"], conv, payload), (200, 201), f"send {name}")
    listed = expect(history(one["access_token"], conv), (200,), "history")
    order = [item["client_id"].split("-")[-1] for item in listed]
    tie = sorted([(one["device"]["device_id"], "a4"), (two["device"]["device_id"], "b2")])
    expected = ["a1", "b1", "a3"] + [name for _, name in tie]
    assert order == expected, f"history lists {order}, expected {expected}"
    gaps = {item["client_id"].split("-")[-1]: item["gap_before"] for item in listed}
    assert gaps["a3"] is True and gaps["a4"] is False and gaps["a1"] is False, (
        f"gap flags read {gaps}, expected a3 gapped and a1, a4 not")
    late = envelope_payload(epoch, devices, client_id=f"{tag}-a2", clock=25, sender_seq=2)
    expect(post_envelope(one["device"]["device_token"], conv, late), (200, 201), "late send")
    replay = envelope_payload(epoch, devices, client_id=f"{tag}-a1", clock=10, sender_seq=1)
    expect(post_envelope(one["device"]["device_token"], conv, replay), (200, 201), "duplicate send")
    listed = expect(history(one["access_token"], conv), (200,), "history after the late envelope")
    order = [item["client_id"].split("-")[-1] for item in listed]
    assert order == ["a1", "b1", "a2", "a3"] + [name for _, name in tie], (
        f"history after a late and a duplicate envelope lists {order}")
    gaps = {item["client_id"].split("-")[-1]: item["gap_before"] for item in listed}
    assert gaps["a3"] is False and gaps["a2"] is False, f"gap flags after the late envelope read {gaps}"


def _group_with(owner: dict, members: list[dict]) -> dict:
    return conversation(owner["access_token"], "private_group", [m["contact_code"] for m in members])


def _remove(owner_token: str, conv: str, code: str) -> dict:
    with client(owner_token) as c:
        return expect(c.delete(f"/conversations/{conv}/members/{code}"), (200, 204), "remove member")


def _add(owner_token: str, conv: str, code: str) -> dict:
    with client(owner_token) as c:
        return expect(c.post(f"/conversations/{conv}/members", json={"contact_code": code}),
                      (200, 201), "add member")


def _seal(owner: dict, conv: str, who: list[dict], **kw) -> httpx.Response:
    epoch = conversation_state(owner["access_token"], conv)["epoch"]
    payload = envelope_payload(epoch, [w["device"]["device_id"] for w in who], **kw)
    response = post_envelope(owner["device"]["device_token"], conv, payload)
    response.payload = payload
    return response


def test_envelope_sealed_to_a_removed_member_is_denied(backend):
    owner, stays, leaves = member_with_device(), member_with_device(), member_with_device()
    group = _group_with(owner, [stays, leaves])
    conv = group["conversation_id"]
    _remove(owner["access_token"], conv, leaves["contact_code"])
    refused = _seal(owner, conv, [owner, stays, leaves])
    assert refused.status_code in CLIENT_ERRORS, (
        f"an envelope sealed to a removed member answered {refused.status_code}")
    rows = backend.query("SELECT count(*) AS n FROM envelopes WHERE client_id = %s",
                         (refused.payload["client_id"],))
    assert rows[0]["n"] == 0, "an envelope sealed to a removed member was stored"
    accepted = _seal(owner, conv, [owner, stays])
    assert accepted.status_code in (200, 201), (
        f"an envelope sealed to current members answered {accepted.status_code}")


def test_history_follows_each_period_of_membership():
    owner, stays, rejoins, outsider = (member_with_device() for _ in range(4))
    group = _group_with(owner, [stays, rejoins])
    conv = group["conversation_id"]
    first = _seal(owner, conv, [owner, stays, rejoins], client_id=unique("p1"))
    _remove(owner["access_token"], conv, rejoins["contact_code"])
    gap = _seal(owner, conv, [owner, stays], client_id=unique("gap"))
    _add(owner["access_token"], conv, rejoins["contact_code"])
    back = _seal(owner, conv, [owner, stays, rejoins], client_id=unique("p2"))
    _remove(owner["access_token"], conv, rejoins["contact_code"])
    later = _seal(owner, conv, [owner, stays], client_id=unique("later"))
    for response in (first, gap, back, later):
        assert response.status_code in (200, 201), f"a send answered {response.status_code}"
    seen = expect(history(rejoins["access_token"], conv), (200,),
                  "history for a removed member")
    ids = {item["client_id"] for item in seen}
    assert ids == {first.payload["client_id"], back.payload["client_id"]}, (
        f"a member removed twice sees {ids}, expected only the envelopes from both periods")
    everyone = {item["client_id"] for item in expect(history(stays["access_token"], conv), (200,), "history")}
    assert len(everyone) == 4, f"a continuous member sees {len(everyone)} envelopes, expected 4"
    assert history(outsider["access_token"], conv).status_code in DENIALS, (
        "an account that never belonged reads the history")


def test_stale_epoch_envelope_is_refused_with_the_current_epoch(backend):
    owner, first, joiner = member_with_device(), member_with_device(), member_with_device()
    group = _group_with(owner, [first])
    conv, old = group["conversation_id"], group["epoch"]
    _add(owner["access_token"], conv, joiner["contact_code"])
    payload = envelope_payload(old, [owner["device"]["device_id"], first["device"]["device_id"]])
    stale = post_envelope(owner["device"]["device_token"], conv, payload)
    assert stale.status_code in CLIENT_ERRORS, f"a stale epoch answered {stale.status_code}"
    detail = body(stale)
    assert detail.get("reason") == "stale_epoch" and detail.get("current_epoch") == old + 1, (
        f"a stale epoch refusal reads {detail}, expected reason stale_epoch and current_epoch {old + 1}")
    rows = backend.query("SELECT count(*) AS n FROM envelopes WHERE client_id = %s", (payload["client_id"],))
    assert rows[0]["n"] == 0, "a stale-epoch envelope was stored"


def test_offline_member_syncs_both_changes_and_a_removed_member_nothing_after():
    owner, offline, removed, joiner = (member_with_device() for _ in range(4))
    group = _group_with(owner, [offline, removed])
    conv = group["conversation_id"]
    _, offline_cursor = sync_all(offline["device"]["device_token"])
    _, removed_cursor = sync_all(removed["device"]["device_token"])
    _remove(owner["access_token"], conv, removed["contact_code"])
    _add(owner["access_token"], conv, joiner["contact_code"])
    after = _seal(owner, conv, [owner, offline, joiner])
    assert after.status_code in (200, 201), f"a send after two changes answered {after.status_code}"
    back, _ = sync_all(offline["device"]["device_token"], offline_cursor)
    changes = [i["epoch"] for i in back if i.get("type") == "membership" and i.get("conversation_id") == conv]
    assert changes == [group["epoch"] + 1, group["epoch"] + 2], (
        f"the offline member syncs membership epochs {changes}")
    assert any(i.get("type") == "envelope" and i.get("client_id") == after.payload["client_id"] for i in back), (
        "the offline member's sync lacks the envelope sealed to it")
    gone, _ = sync_all(removed["device"]["device_token"], removed_cursor)
    theirs = [i for i in gone if i.get("conversation_id") == conv]
    epochs = [i.get("epoch") for i in theirs]
    assert [i.get("type") for i in theirs] == ["membership"] and epochs == [group["epoch"] + 1], (
        f"the removed member syncs {[(i.get('type'), i.get('epoch')) for i in theirs]}")


def test_non_owner_cannot_remove_a_member_denied():
    owner, member, target = member_with_device(), member_with_device(), member_with_device()
    group = _group_with(owner, [member, target])
    conv = group["conversation_id"]
    with client(member["access_token"]) as c:
        denied = c.delete(f"/conversations/{conv}/members/{target['contact_code']}")
    assert denied.status_code in CLIENT_ERRORS, f"a non-owner removal answered {denied.status_code}"
    state = conversation_state(owner["access_token"], conv)
    codes = {m["contact_code"] for m in state["members"]}
    assert target["contact_code"] in codes and state["epoch"] == group["epoch"], (
        f"after a refused removal the group reads epoch {state['epoch']} members {codes}")


def test_channel_subscriber_post_is_forbidden(backend):
    owner, subscriber = member_with_device(), member_with_device()
    channel = conversation(owner["access_token"], "channel", [])
    conv = channel["conversation_id"]
    with client(subscriber["access_token"]) as c:
        expect(c.post(f"/conversations/{conv}/join"), (200, 201), "subscribe to channel")
    epoch = conversation_state(owner["access_token"], conv)["epoch"]
    devices = [owner["device"]["device_id"], subscriber["device"]["device_id"]]
    payload = envelope_payload(epoch, devices)
    denied = post_envelope(subscriber["device"]["device_token"], conv, payload)
    assert denied.status_code in CLIENT_ERRORS, f"a subscriber post answered {denied.status_code}"
    rows = backend.query("SELECT count(*) AS n FROM envelopes WHERE client_id = %s", (payload["client_id"],))
    assert rows[0]["n"] == 0, "a subscriber's post was stored"
    broadcast = post_envelope(owner["device"]["device_token"], conv, envelope_payload(epoch, devices))
    assert broadcast.status_code in (200, 201), f"the broadcaster's post answered {broadcast.status_code}"
    with client(subscriber["access_token"]) as c:
        listed = expect(c.get("/explore"), (200,), "explore")
    seeded = [x for x in listed if x.get("public_name") == CHANNEL]
    assert seeded, f"explore does not list the seeded channel {CHANNEL}"
    seeded_id = seeded[0]["conversation_id"]
    with client(subscriber["access_token"]) as c:
        expect(c.post(f"/conversations/{seeded_id}/join"), (200, 201), "subscribe to the seeded channel")
    seeded_epoch = conversation_state(subscriber["access_token"], seeded_id)["epoch"]
    seeded_post = post_envelope(subscriber["device"]["device_token"], seeded_id,
                                envelope_payload(seeded_epoch, [subscriber["device"]["device_id"]]))
    assert seeded_post.status_code in CLIENT_ERRORS, (
        f"a subscriber post to {CHANNEL} answered {seeded_post.status_code}")


def test_private_group_and_chat_refuse_join_requests():
    owner, member, stranger = member_with_device(), member_with_device(), member_with_device()
    group = _group_with(owner, [member])
    chat = conversation(owner["access_token"], "chat", [member["contact_code"]])
    public = conversation(owner["access_token"], "public_group", [])
    with client(stranger["access_token"]) as c:
        for conv in (group, chat):
            refused = c.post(f"/conversations/{conv['conversation_id']}/join")
            assert refused.status_code in CLIENT_ERRORS, (
                f"joining a {conv['kind']} answered {refused.status_code}")
        expect(c.post(f"/conversations/{public['conversation_id']}/join"), (200, 201), "join public group")
    for conv in (group, chat):
        codes = {m["contact_code"] for m in conversation_state(owner["access_token"], conv["conversation_id"])["members"]}
        assert stranger["contact_code"] not in codes, f"a refused join still added the stranger to a {conv['kind']}"
    public_codes = {m["contact_code"] for m in conversation_state(owner["access_token"], public["conversation_id"])["members"]}
    assert stranger["contact_code"] in public_codes, "joining a public group did not add the member"


def test_read_receipt_needs_both_reader_and_author_opted_in():
    author, reader = member_with_device(), member_with_device()
    chat = conversation(author["access_token"], "chat", [reader["contact_code"]])
    conv = chat["conversation_id"]
    sent = expect(post_envelope(author["device"]["device_token"], conv,
                                envelope_payload(chat["epoch"], [author["device"]["device_id"],
                                                                 reader["device"]["device_id"]])),
                  (200, 201), "send")
    _, cursor = sync_all(author["device"]["device_token"])

    def receipt() -> httpx.Response:
        with client(reader["device"]["device_token"]) as c:
            return c.post(f"/conversations/{conv}/receipts", json={"envelope_id": sent["envelope_id"]})

    assert receipt().status_code in CLIENT_ERRORS, "a receipt with both people opted out was recorded"
    with client(reader["access_token"]) as c:
        expect(c.patch("/me/settings", json={"read_receipts": True}), (200,), "reader opts in")
    assert receipt().status_code in CLIENT_ERRORS, "a receipt to an author who opted out was recorded"
    with client(author["access_token"]) as c:
        expect(c.patch("/me/settings", json={"read_receipts": True}), (200,), "author opts in")
    expect(receipt(), (200, 201), "a receipt with both opted in")
    items, _ = sync_all(author["device"]["device_token"], cursor)
    got = [i for i in items if i.get("type") == "receipt"]
    assert len(got) == 1 and got[0].get("envelope_id") == sent["envelope_id"] and (
        got[0].get("reader_contact_code") == reader["contact_code"]), (
        f"the author's sync carries receipts {got}, expected exactly the one recorded")


def test_closed_group_refuses_posts_and_keeps_history():
    owner, member = member_with_device(), member_with_device()
    group = _group_with(owner, [member])
    conv = group["conversation_id"]
    kept = _seal(owner, conv, [owner, member])
    assert kept.status_code in (200, 201), f"a send before closing answered {kept.status_code}"
    with client(owner["access_token"]) as c:
        closed = expect(c.post(f"/conversations/{conv}/close"), (200, 201), "close group")
    assert closed.get("closed") is True, f"closing answered {closed}"
    refused = _seal(owner, conv, [owner, member])
    assert refused.status_code in CLIENT_ERRORS, f"a post to a closed group answered {refused.status_code}"
    ids = {i["client_id"] for i in expect(history(member["access_token"], conv), (200,), "history")}
    assert kept.payload["client_id"] in ids, "closing the group removed its history"


def _board(owner: dict) -> dict:
    payload = {"client_id": unique("board"), "sealed_name": b64(os.urandom(18)),
               "columns": [{"column_id": c, "sealed_label": b64(os.urandom(9))}
                           for c in ("todo", "doing", "done")]}
    with client(owner["access_token"]) as c:
        return expect(c.post("/boards", json=payload), (200, 201), "create board")


def _task(device_token: str, board_id: str, client_id: str | None = None, column: str = "todo",
          position: str = "m", clock: int = 1) -> httpx.Response:
    payload = {"client_id": client_id or unique("task"), "sealed_title": b64(os.urandom(21)),
               "column_id": column, "position": position, "clock": clock}
    with client(device_token) as c:
        return c.post(f"/boards/{board_id}/tasks", json=payload)


def _task_state(token: str, task_id: str) -> dict:
    with client(token) as c:
        return expect(c.get(f"/tasks/{task_id}"), (200,), "GET task")


def _audience(token: str, task_id: str, members=(), groups=()) -> dict:
    with client(token) as c:
        return expect(c.put(f"/tasks/{task_id}/audience",
                            json={"members": list(members), "groups": list(groups)}),
                      (200,), "set task audience")


def test_member_added_to_a_shared_group_later_reads_the_task():
    owner, member, newcomer = member_with_device(), member_with_device(), member_with_device()
    group = _group_with(owner, [member])
    board = _board(owner)
    task = expect(_task(owner["device"]["device_token"], board["board_id"]), (200, 201), "create task")
    shared = _audience(owner["access_token"], task["task_id"], groups=[group["conversation_id"]])
    assert set(shared["readers"]) == {owner["contact_code"], member["contact_code"]}, (
        f"sharing to a group gives readers {shared['readers']}")
    _add(owner["access_token"], group["conversation_id"], newcomer["contact_code"])
    later = _task_state(owner["access_token"], task["task_id"])
    assert newcomer["contact_code"] in later["readers"], (
        f"a person added to the shared group later is not a reader: {later['readers']}")
    sealed = post_envelope(owner["device"]["device_token"], task["conversation_id"],
                           envelope_payload(later["epoch"], [owner["device"]["device_id"],
                                                             member["device"]["device_id"],
                                                             newcomer["device"]["device_id"]]))
    assert sealed.status_code in (200, 201), (
        f"sealing a task message to the newly added reader answered {sealed.status_code}")


def test_unsharing_one_group_keeps_readers_granted_by_another():
    owner, both, only_first, direct = (member_with_device() for _ in range(4))
    first = _group_with(owner, [both, only_first])
    second = _group_with(owner, [both])
    board = _board(owner)
    task = expect(_task(owner["device"]["device_token"], board["board_id"]), (200, 201), "create task")
    full = _audience(owner["access_token"], task["task_id"], members=[direct["contact_code"]],
                     groups=[first["conversation_id"], second["conversation_id"]])
    assert set(full["readers"]) == {owner["contact_code"], both["contact_code"],
                                    only_first["contact_code"], direct["contact_code"]}, (
        f"sharing to two groups and one person gives readers {full['readers']}")
    trimmed = _audience(owner["access_token"], task["task_id"], members=[direct["contact_code"]],
                        groups=[second["conversation_id"]])
    assert set(trimmed["readers"]) == {owner["contact_code"], both["contact_code"],
                                       direct["contact_code"]}, (
        f"un-sharing the first group leaves readers {trimmed['readers']}")


def test_member_removed_from_a_shared_group_cannot_be_sealed_task_messages():
    owner, stays, leaves = member_with_device(), member_with_device(), member_with_device()
    group = _group_with(owner, [stays, leaves])
    board = _board(owner)
    task = expect(_task(owner["device"]["device_token"], board["board_id"]), (200, 201), "create task")
    shared = _audience(owner["access_token"], task["task_id"], groups=[group["conversation_id"]])
    before = shared["epoch"]
    _remove(owner["access_token"], group["conversation_id"], leaves["contact_code"])
    now = _task_state(owner["access_token"], task["task_id"])
    assert leaves["contact_code"] not in now["readers"] and now["epoch"] == before + 1, (
        f"after the group removal the task reads epoch {now['epoch']} readers {now['readers']}")
    refused = post_envelope(owner["device"]["device_token"], task["conversation_id"],
                            envelope_payload(now["epoch"], [owner["device"]["device_id"],
                                                            stays["device"]["device_id"],
                                                            leaves["device"]["device_id"]]))
    assert refused.status_code in CLIENT_ERRORS, (
        f"a task message sealed to the removed group member answered {refused.status_code}")
    accepted = post_envelope(owner["device"]["device_token"], task["conversation_id"],
                             envelope_payload(now["epoch"], [owner["device"]["device_id"],
                                                             stays["device"]["device_id"]]))
    assert accepted.status_code in (200, 201), f"a task message to current readers answered {accepted.status_code}"


def test_renaming_a_task_renames_its_conversation():
    owner = member_with_device()
    board = _board(owner)
    task = expect(_task(owner["device"]["device_token"], board["board_id"]), (200, 201), "create task")
    new_title = b64(os.urandom(27))
    with client(owner["access_token"]) as c:
        renamed = expect(c.patch(f"/tasks/{task['task_id']}", json={"sealed_title": new_title}), (200,), "rename")
    assert renamed["sealed_title"] == new_title, f"renaming answered {renamed}"
    topic = conversation_state(owner["access_token"], task["conversation_id"])["sealed_topic"]
    assert topic == new_title, "renaming a task left its conversation's sealed_topic unchanged"


def _two_devices() -> tuple[dict, dict, dict]:
    owner = signup()
    first = register_device(owner["access_token"])
    second = register_device(owner["access_token"])
    expect(_approve(first["device_token"], second["device_id"]), (200, 201), "approve second device")
    owner["device"] = first
    return owner, first, second


def _move(device_token: str, task_id: str, column: str, position: str, clock: int) -> dict:
    with client(device_token) as c:
        return expect(c.post(f"/tasks/{task_id}/moves",
                             json={"column_id": column, "position": position, "clock": clock}),
                      (200, 201), "move task")


def _column_of(token: str, board_id: str, task_id: str) -> str | None:
    with client(token) as c:
        board = expect(c.get(f"/boards/{board_id}"), (200,), "GET board")
    for column in board["columns"]:
        if task_id in column["tasks"]:
            return column["column_id"]
    return None


def test_placement_with_the_higher_clock_wins_in_either_arrival_order():
    owner, first, second = _two_devices()
    outcomes = []
    for order in ("higher first", "lower first"):
        board = _board(owner)
        task = expect(_task(first["device_token"], board["board_id"]), (200, 201), "create task")
        moves = [(first, "doing", 5), (second, "done", 3)]
        if order == "lower first":
            moves.reverse()
        for device, column, clock in moves:
            _move(device["device_token"], task["task_id"], column, "m", clock)
        outcomes.append((order, _column_of(owner["access_token"], board["board_id"], task["task_id"])))
    assert all(column == "doing" for _, column in outcomes), (
        f"the move with clock 5 to doing should win in either order; boards read {outcomes}")


def test_equal_clocks_resolve_by_device_and_equal_positions_by_client_id():
    owner, first, second = _two_devices()
    winner = "doing" if first["device_id"] > second["device_id"] else "done"
    outcomes = []
    for reverse in (False, True):
        board = _board(owner)
        task = expect(_task(first["device_token"], board["board_id"]), (200, 201), "create task")
        moves = [(first, "doing"), (second, "done")]
        if reverse:
            moves.reverse()
        for device, column in moves:
            _move(device["device_token"], task["task_id"], column, "m", 7)
        outcomes.append(_column_of(owner["access_token"], board["board_id"], task["task_id"]))
    assert outcomes == [winner, winner], (
        f"equal clocks should resolve to {winner} from the higher device id; boards read {outcomes}")
    board = _board(owner)
    later = expect(_task(first["device_token"], board["board_id"], client_id="c-2-" + os.urandom(4).hex(),
                         position="k"), (200, 201), "create later-sorting task")
    earlier = expect(_task(second["device_token"], board["board_id"], client_id="c-1-" + os.urandom(4).hex(),
                           position="k"), (200, 201), "create earlier-sorting task")
    with client(owner["access_token"]) as c:
        state = expect(c.get(f"/boards/{board['board_id']}"), (200,), "GET board")
    todo = next(col["tasks"] for col in state["columns"] if col["column_id"] == "todo")
    assert todo == [earlier["task_id"], later["task_id"]], (
        f"two tasks at one position list {todo}, expected client_id order")


def test_task_replayed_with_its_client_id_is_stored_once(backend):
    owner = member_with_device()
    board = _board(owner)
    token = owner["device"]["device_token"]
    cid = unique("offline")
    first = expect(_task(token, board["board_id"], client_id=cid), (200, 201), "create task")
    again = expect(_task(token, board["board_id"], client_id=cid), (200, 201), "replay task")
    assert again["task_id"] == first["task_id"], "replaying a task's client_id returned a new task"
    burst = unique("burst")
    clients = warm_clients([token] * 5)
    payload = {"client_id": burst, "sealed_title": b64(os.urandom(12)), "column_id": "todo",
               "position": "n", "clock": 1}
    results = barrier_run(5, lambda i: clients[i].post(f"/boards/{board['board_id']}/tasks", json=payload))
    for c in clients:
        c.close()
    assert all(r is not None and r.status_code in (200, 201, 409) for r in results), (
        f"simultaneous task replays answered {[r.status_code for r in results if r is not None]}")
    for key in (cid, burst):
        rows = backend.query("SELECT count(*) AS n FROM tasks WHERE client_id = %s", (key,))
        assert rows[0]["n"] == 1, f"client_id {key} is stored in {rows[0]['n']} task rows"

def test_phone_workspace_swaps_the_sidebar_for_a_menu_and_pages_board_columns(browser_page):
    account = signup()
    ctx = browser_page.new_context(viewport=PHONE)
    page = open_workspace(ctx, account["email"])
    page.goto(f"{app_url()}/app")
    page.wait_for_load_state("load")
    page.wait_for_timeout(1500)
    landmark = page.locator('nav a[href$="/app/boards"], [role="navigation"] a[href$="/app/boards"]')
    shown = [i for i in range(landmark.count()) if landmark.nth(i).is_visible()]
    assert not shown, "at phone width the sidebar's link to /app/boards shows before Menu is pressed"
    page.get_by_role("button", name="Menu", exact=True).click()
    page.wait_for_timeout(800)
    target = page.locator('a[href$="/app/boards"]:visible')
    assert target.count() > 0, "pressing Menu at phone width shows no link to /app/boards"
    target.first.click()
    page.wait_for_url(re.compile(r".*/app/boards/?([?#].*)?$"), timeout=15000)
    page.goto(f"{app_url()}/app/boards/new")
    page.get_by_label("Board name", exact=True).fill(unique("Phone Board"))
    page.get_by_role("button", name="Next", exact=True).click()
    page.wait_for_url(re.compile(r".*/app/boards/new/columns.*"), timeout=15000)
    page.get_by_role("button", name="Create board", exact=True).click()
    page.wait_for_url(re.compile(r".*/app/boards/(?!new)[^/?#]+/?([?#].*)?$"), timeout=30000)
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)
    columns = ["To do", "Doing", "Done"]
    found = page.locator("body").evaluate(ROW_OF_LABELS, columns)
    missing = [name for name, matches in zip(columns, found) if not matches]
    assert not missing, f"the new board shows no column heading for {missing}"
    row = _one_row(found, 24)
    assert row, f"at phone width the board's columns do not sit in one row: {found}"
    lefts = [m["left"] for m in row]
    gaps = [b - a for a, b in zip(lefts, lefts[1:])]
    assert all(g >= 0.6 * PHONE["width"] for g in gaps), (
        f"at phone width the columns start {gaps} pixels apart, not each most of the screen wide")
    ctx.close()


def _file(device_token: str, piece_size: int, count: int) -> httpx.Response:
    with client(device_token) as c:
        return c.post("/files", json={"client_id": unique("file"), "sealed_name": b64(os.urandom(30)),
                                      "sealed_meta": b64(os.urandom(30)), "piece_size": piece_size,
                                      "piece_count": count})


def _piece(token: str, file_id: str, index: int, size: int) -> httpx.Response:
    with client(token) as c:
        return c.put(f"/files/{file_id}/pieces/{index}", content=os.urandom(size),
                     headers={"Content-Type": "application/octet-stream"})


def _uploaded(owner: dict, count: int = 1) -> str:
    token = owner["device"]["device_token"]
    made = expect(_file(token, 65536, count), (200, 201), "create file")
    for index in range(count):
        expect(_piece(token, made["file_id"], index, 65536), (200, 201), f"upload piece {index}")
    return made["file_id"]


def test_uploaded_file_name_and_contents_are_sealed_before_upload(browser_page, backend, tmp_path):
    owner = signup()
    ctx = _desktop(browser_page)
    wire = Wire(ctx)
    page = open_workspace(ctx, owner["email"])
    name = unique("private-name")
    contents = unique("private-contents")
    source = tmp_path / f"{name}.txt"
    source.write_text((contents + "\n") * 40)
    page.goto(f"{app_url()}/app/storage")
    page.get_by_label("Choose file").set_input_files(str(source))
    page.get_by_role("button", name="Upload", exact=True).click()
    assert wait_for_text(page, f"{name}.txt", reload_every=0), "the uploaded file is not listed by its name"
    forms = leak_forms(name) + leak_forms(contents)
    assert not wire.carries(forms), f"the browser sent the file name or contents: {wire.carries(forms)}"
    held = database_holds(backend, forms)
    assert not held, f"the database holds the file name or contents: {held[:4]}"
    with client(login(owner["email"])) as c:
        files = expect(c.get("/files"), (200,), "GET files")
    assert files, "the uploaded file is not in the file list"
    for f in files:
        assert f["piece_size"] in PIECE_CLASSES, f"a file was stored with piece_size {f['piece_size']}"
        sizes = backend.query("SELECT octet_length(bytes) AS n FROM file_pieces WHERE file_id::text = %s",
                              (f["file_id"],))
        assert sizes and all(s["n"] == f["piece_size"] for s in sizes), (
            f"stored pieces of {f['file_id']} are {[s['n'] for s in sizes]} bytes, not {f['piece_size']}")
    ctx.close()


def test_simultaneous_file_creations_cannot_exceed_the_quota():
    owner = member_with_device()
    token = owner["device"]["device_token"]
    clients = warm_clients([token] * 3)
    results = barrier_run(3, lambda i: clients[i].post("/files", json={
        "client_id": unique("big"), "sealed_name": b64(os.urandom(20)), "sealed_meta": b64(os.urandom(20)),
        "piece_size": 4194304, "piece_count": 10}))
    for c in clients:
        c.close()
    statuses = [r.status_code for r in results if r is not None]
    assert statuses.count(201) + statuses.count(200) == 1, (
        f"three simultaneous 41943040-byte files answered {statuses}, expected exactly one accepted")
    assert all(s in (200, 201) or s in CLIENT_ERRORS for s in statuses), f"answers {statuses}"
    with client(token) as c:
        storage = expect(c.get("/storage"), (200,), "GET storage")
    assert storage == {"used_bytes": 41943040, "quota_bytes": QUOTA_BYTES} or (
        storage.get("used_bytes") == 41943040 and storage.get("quota_bytes") == QUOTA_BYTES), (
        f"storage reads {storage}")


def test_piece_of_a_non_standard_length_is_refused():
    owner = member_with_device()
    token = owner["device"]["device_token"]
    made = expect(_file(token, 65536, 2), (200, 201), "create file")
    assert _piece(token, made["file_id"], 0, 1000).status_code in CLIENT_ERRORS, "a short piece was accepted"
    assert _piece(token, made["file_id"], 0, 65536).status_code in (200, 201), "a full-size piece was refused"
    assert _piece(token, made["file_id"], 1, 70000).status_code in CLIENT_ERRORS, "a long piece was accepted"
    assert _file(token, 50000, 1).status_code in CLIENT_ERRORS, "a piece size outside the classes was accepted"


def test_file_missing_a_piece_reads_unavailable(backend):
    owner = member_with_device()
    file_id = _uploaded(owner, 2)
    with client(owner["access_token"]) as c:
        assert expect(c.get(f"/files/{file_id}"), (200,), "GET file")["state"] == "available"
    backend.query("DELETE FROM file_pieces WHERE file_id::text = %s AND piece_index = 1", (file_id,))
    with client(owner["access_token"]) as c:
        state = expect(c.get(f"/files/{file_id}"), (200,), "GET file after a piece vanished")
    assert state["state"] == "unavailable", f"a file missing a piece reads {state['state']}"


def test_revoking_a_link_keeps_member_access_and_removal_keeps_the_link():
    owner, member = member_with_device(), member_with_device()
    group = _group_with(owner, [member])
    file_id = _uploaded(owner)
    with client(owner["access_token"]) as c:
        expect(c.post(f"/conversations/{group['conversation_id']}/files", json={"file_id": file_id}),
               (200, 201), "share file into group")
        first = expect(c.post(f"/files/{file_id}/links", json={"expires_in_hours": 24}), (200, 201), "link")
        second = expect(c.post(f"/files/{file_id}/links", json={"expires_in_hours": 24}), (200, 201), "link")
    with client() as anon, client(member["access_token"]) as m:
        assert anon.get(f"/links/{first['link_token']}").status_code == 200, "a fresh link does not open"
        assert m.get(f"/files/{file_id}/pieces/0").status_code == 200, "a group member cannot fetch a shared file"
    with client(owner["access_token"]) as c:
        expect(c.delete(f"/links/{first['link_token']}"), (200, 204), "revoke link")
    with client() as anon, client(member["access_token"]) as m:
        revoked = anon.get(f"/links/{first['link_token']}")
        assert revoked.status_code in CLIENT_ERRORS and body(revoked).get("reason") == "revoked", (
            f"a revoked link answered {revoked.status_code} {revoked.text[:200]}")
        assert m.get(f"/files/{file_id}/pieces/0").status_code == 200, "revoking a link removed member access"
    _remove(owner["access_token"], group["conversation_id"], member["contact_code"])
    with client() as anon, client(member["access_token"]) as m:
        assert m.get(f"/files/{file_id}/pieces/0").status_code in DENIALS, (
            "a removed member still fetches the shared file")
        assert anon.get(f"/links/{second['link_token']}").status_code == 200, "removing a member broke a link"
        assert anon.get(f"/links/{second['link_token']}/pieces/0").status_code == 200, (
            "removing a member broke a link's piece fetch")


def test_expired_link_is_refused_with_the_expiry_message(backend):
    owner = member_with_device()
    file_id = _uploaded(owner)
    with client(owner["access_token"]) as c:
        link = expect(c.post(f"/files/{file_id}/links", json={"expires_in_hours": 1}), (200, 201), "link")
    backend.query("UPDATE file_links SET expires_at = now() - interval '1 hour' WHERE link_token = %s",
                  (link["link_token"],))
    with client() as anon:
        expired = anon.get(f"/links/{link['link_token']}")
    detail = body(expired)
    assert expired.status_code in CLIENT_ERRORS and detail.get("reason") == "expired" and (
        detail.get("message") == LINK_EXPIRED), f"an expired link answered {expired.status_code} {detail}"


def _route(token: str, route: str) -> None:
    with client(token) as c:
        expect(c.patch("/me/settings", json={"call_route": route}), (200,), f"set call_route {route}")


def _call(token: str, conv: str) -> dict:
    with client(token) as c:
        return expect(c.post("/calls", json={"conversation_id": conv, "media": "voice"}), (200, 201), "place call")


def test_direct_route_requires_both_participants_to_choose_it():
    caller, callee = signup(), signup()
    assert me(caller["access_token"])["settings"]["call_route"] == "private", "a new account's call_route is not private"
    chat = conversation(caller["access_token"], "chat", [callee["contact_code"]])
    conv = chat["conversation_id"]
    _route(caller["access_token"], "direct")
    one_sided = _call(caller["access_token"], conv)
    assert one_sided["route"] == "relay" and not one_sided.get("peer_address"), (
        f"a call where only the caller chose direct answered {one_sided}")
    _route(callee["access_token"], "direct")
    both = _call(caller["access_token"], conv)
    assert both["route"] == "direct" and isinstance(both.get("peer_address"), str) and both["peer_address"], (
        f"a call where both chose direct answered {both}")
    with client(callee["access_token"]) as c:
        seen = expect(c.get(f"/calls/{one_sided['call_id']}"), (200,), "GET relayed call")
    assert not seen.get("peer_address"), f"a relayed call carries peer_address: {seen}"


def test_group_call_always_relays_without_a_peer_address():
    owner, one, two = signup(), signup(), signup()
    for account in (owner, one, two):
        _route(account["access_token"], "direct")
    group = conversation(owner["access_token"], "private_group", [one["contact_code"], two["contact_code"]])
    public = conversation(owner["access_token"], "public_group", [])
    for conv in (group, public):
        call = _call(owner["access_token"], conv["conversation_id"])
        assert call["route"] == "relay" and not call.get("peer_address"), (
            f"a {conv['kind']} call with everyone on direct answered {call}")


def test_repeated_ring_rings_once_and_a_late_ring_is_refused():
    caller, callee = signup(), signup()
    chat = conversation(caller["access_token"], "chat", [callee["contact_code"]])
    call = _call(caller["access_token"], chat["conversation_id"])
    path = f"/calls/{call['call_id']}"
    with client(caller["access_token"]) as c:
        expect(c.post(f"{path}/rings", json={"ring_id": "ring-one"}), (200, 201), "ring")
        expect(c.post(f"{path}/rings", json={"ring_id": "ring-one"}), (200, 201), "repeat ring")
        assert expect(c.get(path), (200,), "GET call")["rings"] == 1, "a repeated ring rang twice"
        expect(c.post(f"{path}/rings", json={"ring_id": "ring-two"}), (200, 201), "second ring")
        expect(c.post(f"{path}/end"), (200, 201), "end call")
        late = c.post(f"{path}/rings", json={"ring_id": "ring-three"})
        assert late.status_code in CLIENT_ERRORS, f"a ring after the call ended answered {late.status_code}"
        assert expect(c.get(path), (200,), "GET call")["rings"] == 2, "a late ring was counted"


def test_quote_is_refused_while_the_rate_is_stale():
    account = signup()
    post_rate("usdc", 1000000, now_utc() - dt.timedelta(minutes=11))
    with client(account["access_token"]) as c:
        stale = c.post("/quotes", json={"rail": "usdc"})
    assert stale.status_code in CLIENT_ERRORS and body(stale).get("reason") == "rate_stale", (
        f"a quote on an eleven-minute-old rate answered {stale.status_code} {stale.text[:200]}")
    post_rate("usdc", 999800, now_utc() - dt.timedelta(minutes=9))
    fresh = quote(account["access_token"], "usdc")
    assert fresh["rate_usd_micros"] == 999800 and fresh["amount_due"] == 3500701, (
        f"a quote on a nine-minute-old rate answered {fresh}")


def test_amount_due_rounds_up_to_the_rail_base_unit():
    account = signup()
    moment = now_utc()
    post_rate("xmr", 157300000, moment)
    post_rate("njr", 140000, moment)
    xmr = quote(account["access_token"], "xmr")
    assert xmr["amount_due"] == 22250476796 and xmr["price_usd_cents"] == 350, f"an xmr quote answered {xmr}"
    njr = quote(account["access_token"], "njr")
    assert njr["amount_due"] == 16071429 and njr["price_usd_cents"] == 225, f"an njr quote answered {njr}"
    store = quote(account["access_token"], "app_store")
    assert store["amount_due"] == 350, f"an app_store quote answered {store}"


def _payment(token: str, tx_hash: str) -> dict:
    found = [p for p in payments(token) if p["tx_hash"] == tx_hash]
    assert len(found) == 1, f"payments list {len(found)} rows for {tx_hash}"
    return found[0]


def test_block_time_decides_the_rate_of_a_late_reported_payment(backend):
    account = signup()
    token = account["access_token"]
    post_rate("njr", 150000, now_utc())
    early = quote(token, "njr")
    assert early["amount_due"] == 15000000, f"a quote at 150000 answered {early}"
    settle(1.2)
    post_rate("njr", 140000, now_utc())
    backend.query("UPDATE quotes SET expires_at = now() - interval '60 seconds' WHERE id::text = %s",
                  (early["quote_id"],))
    on_time = payment_event(early, 15000000, 12, now_utc() - dt.timedelta(seconds=120))
    expect(watcher_post("/watcher/payments", on_time), (200, 201, 202), "report on-time payment late")
    settled = _payment(token, on_time["tx_hash"])
    assert settled["state"] == "settled" and settled["amount_due"] == 15000000, (
        f"a payment in a block before expiry, reported after it, reads {settled}")
    settle(1.2)
    post_rate("njr", 150000, now_utc())
    late_quote = quote(token, "njr")
    assert late_quote["amount_due"] == 15000000, f"a second quote at 150000 answered {late_quote}"
    settle(1.2)
    rate_moment = now_utc()
    post_rate("njr", 140000, rate_moment)
    backend.query("UPDATE quotes SET expires_at = %s WHERE id::text = %s",
                  (rate_moment - dt.timedelta(milliseconds=300), late_quote["quote_id"]))
    settle(1.0)
    late = payment_event(late_quote, 15000000, 12, rate_moment + dt.timedelta(milliseconds=500))
    expect(watcher_post("/watcher/payments", late), (200, 201, 202), "report late payment")
    short = _payment(token, late["tx_hash"])
    assert short["state"] == "underpaid" and short["amount_due"] == 16071429 and short["shortfall"] == 1071429, (
        f"a payment in a block after expiry reads {short}, expected re-quoted at 140000")


def test_unsigned_or_forged_watcher_events_are_refused():
    account = signup()
    fresh_rates()
    q = quote(account["access_token"], "njr")
    event = payment_event(q, q["amount_due"], 12, now_utc() - dt.timedelta(seconds=3))
    with client() as c:
        unsigned = c.post("/watcher/payments", json=event)
    assert unsigned.status_code in CLIENT_ERRORS, f"an unsigned payment answered {unsigned.status_code}"
    forged = watcher_post("/watcher/payments", event, seed=os.urandom(32))
    assert forged.status_code in CLIENT_ERRORS, f"a payment signed by another key answered {forged.status_code}"
    altered = watcher_post("/watcher/payments", event, tamper=True)
    assert altered.status_code in CLIENT_ERRORS, f"an altered payment body answered {altered.status_code}"
    assert payments(account["access_token"]) == [], "a refused watcher event created a payment"
    assert membership(account["access_token"])["state"] == "trial", "a refused watcher event changed membership"
    fake_rate = watcher_post("/watcher/rates", {"asset": "njr", "usd_micros": 1,
                                                "observed_at": iso(now_utc())}, seed=os.urandom(32))
    assert fake_rate.status_code in CLIENT_ERRORS, f"a forged rate answered {fake_rate.status_code}"
    with client(account["access_token"]) as c:
        rates = {r["asset"]: r["usd_micros"] for r in expect(c.get("/rates"), (200,), "GET rates")}
    assert rates.get("njr") != 1, "a forged rate was stored"
    expect(watcher_post("/watcher/payments", event), (200, 201, 202), "the correctly signed payment")
    assert membership(account["access_token"])["state"] == "active", "a correctly signed payment did not settle"


def test_payment_below_its_depth_grants_nothing():
    account = signup()
    token = account["access_token"]
    fresh_rates()
    for rail in ("njr", "xmr"):
        q = quote(token, rail)
        tx = "0x" + os.urandom(32).hex()
        shallow = payment_event(q, q["amount_due"], DEPTH[rail] - 1, now_utc() - dt.timedelta(seconds=4), tx)
        expect(watcher_post("/watcher/payments", shallow), (200, 201, 202), f"{rail} below depth")
        assert _payment(token, tx)["state"] == "seen", f"a {rail} payment below depth is not seen"
        if rail == "njr":
            assert membership(token).get("paid_until") is None, "a payment below depth granted paid time"
        deep = dict(shallow, confirmations=DEPTH[rail])
        expect(watcher_post("/watcher/payments", deep), (200, 201, 202), f"{rail} at depth")
        assert _payment(token, tx)["state"] == "settled", f"a {rail} payment at depth did not settle"
    assert membership(token)["state"] == "active", "settled payments left the membership inactive"


def test_simultaneous_depth_reports_extend_membership_once():
    account = signup()
    token = account["access_token"]
    fresh_rates()
    q = quote(token, "njr")
    block = now_utc() - dt.timedelta(seconds=5)
    event = payment_event(q, q["amount_due"], 12, block)
    raw = json.dumps(event, separators=(",", ":")).encode("utf-8")
    headers = {"Content-Type": "application/json", "X-Watcher-Signature": ed_sign(WATCHER_SEED, raw).hex()}
    clients = warm_clients([None] * 6)
    results = barrier_run(6, lambda i: clients[i].post("/watcher/payments", content=raw, headers=headers))
    for c in clients:
        c.close()
    assert all(r is not None and r.status_code < 500 for r in results), (
        f"simultaneous depth reports answered {[r.status_code for r in results if r is not None]}")
    paid = parse_time(membership(token)["paid_until"])
    expected = parse_time(event["block_time"]) + dt.timedelta(days=30)
    assert abs((paid - expected).total_seconds()) < 2, (
        f"six simultaneous reports set paid_until {paid}, expected {expected} from one extension")
    second = payment_event(q, q["amount_due"], 12, now_utc() - dt.timedelta(seconds=2))
    expect(watcher_post("/watcher/payments", second), (200, 201, 202), "a second transaction on the quote")
    assert _payment(token, second["tx_hash"])["state"] == "credited", "a second transaction was not credited"
    assert parse_time(membership(token)["paid_until"]) == paid, "a second transaction extended membership"


def test_half_per_cent_shortfall_rule_decides_settled_or_underpaid():
    post_rate("njr", 140000, now_utc())
    cases = [(15991072, "settled", 0, 0), (15991071, "underpaid", 80358, 0), (16100000, "settled", 0, 28571)]
    for amount, state, shortfall, credit in cases:
        account = signup()
        q = quote(account["access_token"], "njr")
        assert q["amount_due"] == 16071429, f"a quote at 140000 answered {q}"
        event = payment_event(q, amount, 12, now_utc() - dt.timedelta(seconds=3))
        expect(watcher_post("/watcher/payments", event), (200, 201, 202), f"pay {amount}")
        row = _payment(account["access_token"], event["tx_hash"])
        assert row["state"] == state and (row.get("shortfall") or 0) == shortfall and (
            row.get("credit") or 0) == credit, f"paying {amount} against 16071429 reads {row}"
        if state == "underpaid":
            top_up = payment_event(q, 1, 12, now_utc() - dt.timedelta(seconds=2))
            expect(watcher_post("/watcher/payments", top_up), (200, 201, 202), "top up by one unit")
            assert membership(account["access_token"])["state"] == "active", (
                "a top-up that clears the half per cent rule did not settle the quote")


def _suspend(backend, account_id: str) -> None:
    backend.query("UPDATE memberships SET trial_ends_at = now() - interval '2 days', paid_until = NULL "
                  "WHERE account_id::text = %s", (account_id,))


def test_lapsed_member_reads_history_but_sending_is_refused(backend):
    sender, peer = member_with_device(), member_with_device()
    chat = conversation(sender["access_token"], "chat", [peer["contact_code"]])
    conv = chat["conversation_id"]
    devices = [sender["device"]["device_id"], peer["device"]["device_id"]]
    kept = envelope_payload(chat["epoch"], devices)
    expect(post_envelope(sender["device"]["device_token"], conv, kept), (200, 201), "send before lapse")
    _suspend(backend, sender["account_id"])
    assert membership(sender["access_token"])["state"] == "suspended", "a lapsed account does not read suspended"
    listed = {i["client_id"] for i in expect(history(sender["access_token"], conv), (200,), "history while suspended")}
    assert kept["client_id"] in listed, "a suspended account lost its history"
    blocked = envelope_payload(chat["epoch"], devices)
    refused = post_envelope(sender["device"]["device_token"], conv, blocked)
    assert refused.status_code in CLIENT_ERRORS and body(refused).get("reason") == "membership_suspended", (
        f"a suspended account sending answered {refused.status_code} {refused.text[:200]}")
    rows = backend.query("SELECT count(*) AS n FROM envelopes WHERE client_id = %s", (blocked["client_id"],))
    assert rows[0]["n"] == 0, "a suspended account's envelope was stored"
    assert _file(sender["device"]["device_token"], 65536, 1).status_code in CLIENT_ERRORS, (
        "a suspended account created a file")
    states = {d["device_id"]: d["state"] for d in devices_of(sender["access_token"])}
    assert states.get(sender["device"]["device_id"]) == "active", f"lapse changed the devices: {states}"


def test_renewal_after_lapse_restores_sending_with_devices_intact(backend):
    sender, peer = member_with_device(), member_with_device()
    chat = conversation(sender["access_token"], "chat", [peer["contact_code"]])
    devices = [sender["device"]["device_id"], peer["device"]["device_id"]]
    _suspend(backend, sender["account_id"])
    pay_in_full(sender["access_token"], "njr")
    assert membership(sender["access_token"])["state"] == "active", "paying after lapse did not restore membership"
    sent = post_envelope(sender["device"]["device_token"], chat["conversation_id"],
                         envelope_payload(chat["epoch"], devices))
    assert sent.status_code in (200, 201), f"sending after renewal answered {sent.status_code}"
    with client(sender["access_token"]) as c:
        listed = {x["conversation_id"] for x in expect(c.get("/conversations"), (200,), "GET conversations")}
    assert chat["conversation_id"] in listed, "renewal lost the account's conversations"


def test_sponsor_sees_only_the_recipient_code_and_state():
    sponsor, recipient = signup(), signup()
    pay_in_full(sponsor["access_token"], "njr", for_contact_code=recipient["contact_code"])
    theirs = membership(recipient["access_token"])
    assert theirs["state"] == "active" and theirs["sponsor_contact_code"] == sponsor["contact_code"], (
        f"a sponsored membership reads {theirs}")
    assert membership(sponsor["access_token"])["state"] == "trial", "sponsoring someone changed the sponsor's own membership"
    with client(sponsor["access_token"]) as c:
        listed = expect(c.get("/sponsorships"), (200,), "GET sponsorships")
    assert listed == [{"recipient_contact_code": recipient["contact_code"], "state": "active"}], (
        f"the sponsor's list reads {listed}, expected only the recipient code and state")


def test_declining_a_sponsorship_ends_the_sponsored_time():
    sponsor, recipient = signup(), signup()
    pay_in_full(sponsor["access_token"], "njr", for_contact_code=recipient["contact_code"])
    with client(recipient["access_token"]) as c:
        expect(c.post("/membership/sponsorship/decline"), (200, 201), "decline sponsorship")
    after = membership(recipient["access_token"])
    assert after["state"] == "trial" and not after.get("sponsor_contact_code") and not after.get("paid_until"), (
        f"after declining the membership reads {after}")
    with client(sponsor["access_token"]) as c:
        listed = expect(c.get("/sponsorships"), (200,), "GET sponsorships")
    assert listed == [{"recipient_contact_code": recipient["contact_code"], "state": "declined"}], (
        f"after a decline the sponsor's list reads {listed}")
    again = pay_in_full(sponsor["access_token"], "njr", for_contact_code=recipient["contact_code"])
    assert membership(recipient["access_token"])["state"] == "trial", "a sponsored payment after declining was applied"
    rows = [p for p in payments(sponsor["access_token"]) if p["quote_id"] == again["quote_id"]]
    assert rows and rows[0]["state"] == "credited", f"a sponsored payment after declining reads {rows}"


def _epoch(token: str, number: int) -> dict:
    with client(token) as c:
        return expect(c.get(f"/epochs/{number}"), (200,), f"GET epoch {number}")


def _settle(token: str, number: int, limit: int | None = None) -> httpx.Response:
    payload = {} if limit is None else {"limit": limit}
    with client(token) as c:
        return c.post(f"/epochs/{number}/settle", json=payload)


def _rewards(token: str, number: int) -> list[dict]:
    with client(token) as c:
        ledger = expect(c.get("/token/ledger"), (200,), "GET token ledger")
    return [t for t in ledger if t.get("kind") == "reward" and t.get("epoch") == number]


def test_audit_of_epoch_two_shows_the_seeded_inputs(treasurer_token):
    with client(treasurer_token) as c:
        listed = {e["number"]: e["state"] for e in expect(c.get("/epochs"), (200,), "GET epochs")}
    assert all(listed.get(n) == "closed" for n in (2, 3, 4)), f"epochs read {listed}"
    audit = _epoch(treasurer_token, 2)
    want = expected_epoch(2)
    assert audit["probe_rounds"] == 8 and audit["total_weight"] == want["total_weight"], (
        f"epoch 2 audit reads rounds {audit['probe_rounds']} total {audit['total_weight']}")
    assert audit["contributions_micro"] == want["contributions"] and audit["pool_micro"] == want["pool"], (
        f"epoch 2 audit reads contributions {audit['contributions_micro']} pool {audit['pool_micro']}, "
        f"expected {want['contributions']} and {want['pool']}")
    assert audit["remainder_micro"] == want["remainder"], f"epoch 2 remainder reads {audit['remainder_micro']}"
    by_name = {r["name"]: r for r in audit["relays"]}
    for name, rounds in SEEDED_EPOCHS[2]["relays"].items():
        row = by_name[name]
        shown = {k: v for k, v in row["answered_rounds_by_tier"].items() if v}
        assert shown == rounds, f"epoch 2 shows {name} answered {shown}, seeded {rounds}"
        assert row["weight"] == want["weights"][name] and row["share_micro"] == want["shares"][name], (
            f"epoch 2 shows {name} weight {row['weight']} share {row['share_micro']}")


def test_simultaneous_settlement_runs_pay_epoch_two_once(treasurer_token, operator_token):
    clients = warm_clients([treasurer_token] * 6)
    results = barrier_run(6, lambda i: clients[i].post("/epochs/2/settle", json={}))
    for c in clients:
        c.close()
    assert all(r is not None and r.status_code < 500 for r in results), (
        f"simultaneous settlements answered {[r.status_code for r in results if r is not None]}")
    want = expected_epoch(2)
    audit = _epoch(treasurer_token, 2)
    assert audit["state"] == "settled", f"epoch 2 reads {audit['state']} after settlement"
    names = {r["relay_id"]: r["name"] for r in audit["relays"]}
    paid: dict[str, list[int]] = {}
    for transfer in _rewards(operator_token, 2):
        paid.setdefault(names.get(transfer["relay_id"], transfer["relay_id"]), []).append(transfer["amount_micro"])
    expected = {n: [s] for n, s in want["shares"].items() if s > 0}
    assert paid == expected, f"epoch 2 paid {paid}, expected one transfer per relay {expected}"


def test_batched_settlement_of_epoch_three_pays_from_the_snapshot_after_a_withdrawal(treasurer_token, operator_token):
    want = expected_epoch(3)
    order = sorted(n for n, s in want["shares"].items() if s > 0)
    first = expect(_settle(treasurer_token, 3, limit=2), (200, 201), "settle epoch 3 limit 2")
    assert sorted(p["name"] for p in first["paid"]) == order[:2] and first["remaining"] == len(order) - 2, (
        f"a first run with limit 2 paid {[p['name'] for p in first['paid']]} remaining {first['remaining']}")
    assert _epoch(treasurer_token, 3)["state"] == "settling", "a partly paid epoch does not read settling"
    tern = next(r for r in _epoch(treasurer_token, 3)["relays"] if r["name"] == "Tern")
    with client(operator_token) as c:
        withdrawn = expect(c.post(f"/relays/{tern['relay_id']}/unstake", json={"tokens": 15000}), (200, 201), "unstake Tern")
    assert withdrawn["tier"] == "basic", f"Tern after withdrawing reads {withdrawn}"
    second = expect(_settle(treasurer_token, 3, limit=2), (200, 201), "settle epoch 3 again")
    assert sorted(p["name"] for p in second["paid"]) == order[2:4], f"a second run paid {[p['name'] for p in second['paid']]}"
    third = expect(_settle(treasurer_token, 3), (200, 201), "settle epoch 3 a third time")
    assert third["paid"] == [], f"a run after every share was paid still paid {third['paid']}"
    audit = _epoch(treasurer_token, 3)
    names = {r["relay_id"]: r["name"] for r in audit["relays"]}
    paid = sorted((names[t["relay_id"]], t["amount_micro"]) for t in _rewards(operator_token, 3))
    expected = sorted((n, s) for n, s in want["shares"].items() if s > 0)
    assert paid == expected, f"epoch 3 paid {paid}, expected snapshot shares {expected}"


def test_settling_epoch_four_twice_pays_rounded_down_shares_once(treasurer_token, operator_token):
    want = expected_epoch(4)
    first = expect(_settle(treasurer_token, 4), (200, 201), "settle epoch 4")
    second = expect(_settle(treasurer_token, 4), (200, 201), "settle epoch 4 again")
    assert second["paid"] == [], f"settling epoch 4 again paid {second['paid']}"
    assert sorted((p["name"], p["amount_micro"]) for p in first["paid"]) == sorted(
        (n, s) for n, s in want["shares"].items() if s > 0), f"epoch 4 paid {first['paid']}"
    audit = _epoch(treasurer_token, 4)
    assert audit["remainder_micro"] == want["remainder"], f"epoch 4 remainder reads {audit['remainder_micro']}"
    transfers = _rewards(operator_token, 4)
    assert len(transfers) == len([s for s in want["shares"].values() if s > 0]) and (
        sum(t["amount_micro"] for t in transfers) == want["pool"] - want["remainder"]), (
        f"epoch 4 ledger holds {[(t['relay_id'], t['amount_micro']) for t in transfers]}")


def test_member_cannot_run_treasury_actions_forbidden(treasurer_token):
    member = signup()
    before = _epoch(treasurer_token, 1)
    with client(treasurer_token) as c:
        event_before = expect(c.get("/token/event"), (200,), "GET token event")
        open_before = [e["number"] for e in expect(c.get("/epochs"), (200,), "GET epochs") if e["state"] == "open"]
    with client(member["access_token"]) as c:
        attempts = {
            "settle": c.post("/epochs/1/settle", json={}),
            "probe round": c.post("/epochs/current/probe-rounds"),
            "close": c.post("/epochs/current/close"),
            "token event": c.put("/token/event", json={"launch_at": "2030-01-01T00:00:00Z"}),
            "position": c.post("/token/positions", json={"contact_code": member["contact_code"],
                                                         "schedule": "visioners", "allocation_micro": 1000000}),
            "applications": c.get("/whitelist/applications"),
        }
    for label, response in attempts.items():
        assert response.status_code in CLIENT_ERRORS, f"a member's {label} request answered {response.status_code}"
    with client() as anon:
        assert anon.get("/me").status_code in DENIALS, "a visitor reads /api/me"
    after = _epoch(treasurer_token, 1)
    assert after["state"] == before["state"] and [r.get("paid") for r in after["relays"]] == [
        r.get("paid") for r in before["relays"]], "a refused settlement changed epoch 1"
    with client(treasurer_token) as c:
        assert expect(c.get("/token/event"), (200,), "GET token event") == event_before, "a refused request moved the token event"
        assert [e["number"] for e in expect(c.get("/epochs"), (200,), "GET epochs") if e["state"] == "open"] == open_before, (
            "a refused request closed the open epoch")


def test_seeded_relays_and_epochs_are_stored_once(backend):
    for name in SEEDED_RELAYS:
        rows = backend.query("SELECT count(*) AS n FROM relays WHERE name = %s", (name,))
        assert rows[0]["n"] == 1, f"relay {name} is stored {rows[0]['n']} times"
    epochs = backend.query("SELECT number, count(*) AS n FROM epochs WHERE number <= 5 GROUP BY number ORDER BY number")
    assert [(int(r["number"]), r["n"]) for r in epochs] == [(n, 1) for n in range(1, 6)], f"epochs 1 to 5 stored as {epochs}"
    for email in ("member@example.com", "member2@example.com", "member3@example.com", TREASURER_EMAIL, OPERATOR_EMAIL):
        rows = backend.query("SELECT count(*) AS n FROM accounts WHERE email = %s", (email,))
        assert rows[0]["n"] == 1, f"{email} is stored {rows[0]['n']} times"
    schedules = backend.query("SELECT count(*) AS n FROM token_schedules")
    assert schedules[0]["n"] == 11, f"token_schedules holds {schedules[0]['n']} rows"


def _relay(token: str, name: str, stake: int) -> httpx.Response:
    with client(token) as c:
        return c.post("/relays", json={"name": name, "stake_tokens": stake})


def _round(treasurer_token: str) -> dict:
    with client(treasurer_token) as c:
        return expect(c.post("/epochs/current/probe-rounds"), (200, 201), "issue probe round")


def _probe(token: str, relay_id: str) -> httpx.Response:
    with client(token) as c:
        return c.get(f"/relays/{relay_id}/probe")


def _answer(token: str, relay_id: str, probe: dict) -> httpx.Response:
    with client(token) as c:
        return c.post(f"/relays/{relay_id}/probe-answers", json={"round_id": probe["round_id"], "nonce": probe["nonce"]})


def _relay_state(token: str, relay_id: str) -> dict:
    with client(token) as c:
        return expect(c.get(f"/relays/{relay_id}"), (200,), "GET relay")


def test_duplicate_foreign_or_superseded_probe_answers_count_nothing(treasurer_token):
    operator, stranger = signup(), signup()
    token = operator["access_token"]
    one = expect(_relay(token, unique("Swift"), 15000), (200, 201), "register relay")
    two = expect(_relay(token, unique("Martin"), 10000), (200, 201), "register relay")
    _round(treasurer_token)
    probe_one = expect(_probe(token, one["relay_id"]), (200,), "probe one")
    probe_two = expect(_probe(token, two["relay_id"]), (200,), "probe two")
    assert _probe(stranger["access_token"], one["relay_id"]).status_code in DENIALS, "a stranger read another operator's probe"
    foreign = _answer(token, one["relay_id"], probe_two)
    assert foreign.status_code in CLIENT_ERRORS, f"answering with another relay's nonce answered {foreign.status_code}"
    assert _relay_state(token, one["relay_id"])["current_epoch"]["answered_rounds"] == 0, "a foreign nonce was counted"
    expect(_answer(token, one["relay_id"], probe_one), (200, 201), "answer probe")
    repeat = _answer(token, one["relay_id"], probe_one)
    assert repeat.status_code in CLIENT_ERRORS, f"a repeated answer answered {repeat.status_code}"
    assert _relay_state(token, one["relay_id"])["current_epoch"]["answered_rounds"] == 1, "a repeated answer was counted"
    _round(treasurer_token)
    superseded = _answer(token, two["relay_id"], probe_two)
    assert superseded.status_code in CLIENT_ERRORS, f"an answer to a superseded round answered {superseded.status_code}"
    assert _relay_state(token, two["relay_id"])["current_epoch"]["answered_rounds"] == 0, "a superseded answer was counted"
    latest = expect(_probe(token, two["relay_id"]), (200,), "latest probe")
    expect(_answer(token, two["relay_id"], latest), (200, 201), "answer latest round")
    assert _relay_state(token, two["relay_id"])["current_epoch"]["answered_rounds"] == 1, "the latest answer was not counted"


def test_earnings_follow_the_tier_held_when_each_round_was_issued(treasurer_token):
    operator = signup()
    token = operator["access_token"]
    relay = expect(_relay(token, unique("Harrier"), 25000), (200, 201), "register relay")
    rid = relay["relay_id"]

    def answered_round() -> None:
        _round(treasurer_token)
        expect(_answer(token, rid, expect(_probe(token, rid), (200,), "probe")), (200, 201), "answer")

    answered_round()
    assert _relay_state(token, rid)["current_epoch"]["weight"] == 25, "a level-2 round does not earn 25"
    with client(token) as c:
        lowered = expect(c.post(f"/relays/{rid}/unstake", json={"tokens": 5000}), (200, 201), "unstake")
    assert lowered["tier"] == "level-1", f"a 20000 stake reads tier {lowered['tier']}"
    answered_round()
    assert _relay_state(token, rid)["current_epoch"]["weight"] == 40, (
        f"rounds at level-2 then level-1 earn {_relay_state(token, rid)['current_epoch']['weight']}, expected 40")
    with client(token) as c:
        raised = expect(c.post(f"/relays/{rid}/stake", json={"add_tokens": 130000}), (200, 201), "add stake")
    assert raised["tier"] == "master", f"a 150000 stake reads tier {raised['tier']}"
    _round(treasurer_token)
    assert _relay_state(token, rid)["current_epoch"]["weight"] == 40, "an unanswered round earned something"
    answered_round()
    assert _relay_state(token, rid)["current_epoch"]["weight"] == 190, (
        f"a master round after 40 earns {_relay_state(token, rid)['current_epoch']['weight']}, expected 190")


def test_stake_below_the_floor_is_refused_and_heartbeats_change_nothing(treasurer_token):
    operator = signup()
    token = operator["access_token"]
    assert _relay(token, unique("Stint"), 9999).status_code in CLIENT_ERRORS, "a 9999 stake was accepted"
    relay = expect(_relay(token, unique("Knot"), 20000), (200, 201), "register relay")
    assert relay["tier"] == "level-1", f"a 20000 stake registers at {relay['tier']}"
    rid = relay["relay_id"]
    with client(token) as c:
        too_far = c.post(f"/relays/{rid}/unstake", json={"tokens": 10001})
    assert too_far.status_code in CLIENT_ERRORS, f"withdrawing below the floor answered {too_far.status_code}"
    assert _relay_state(token, rid)["stake_tokens"] == 20000, "a refused withdrawal changed the stake"
    _round(treasurer_token)
    expect(_answer(token, rid, expect(_probe(token, rid), (200,), "probe")), (200, 201), "answer")
    with client(token) as c:
        beat = c.post(f"/relays/{rid}/heartbeats", json={"uptime_seconds": 999999, "carried_bytes": 10 ** 9})
    assert beat.status_code in (200, 201, 202), f"a heartbeat answered {beat.status_code}"
    state = _relay_state(token, rid)["current_epoch"]
    assert state["answered_rounds"] == 1 and state["weight"] == 15, f"after a heartbeat the relay reads {state}"


def test_core_node_that_missed_the_latest_round_falls_back(treasurer_token):
    owner, member = member_with_device(), member_with_device()
    token = owner["access_token"]
    group = _group_with(owner, [member])
    conv = group["conversation_id"]
    relay = expect(_relay(token, unique("Dunlin"), 10000), (200, 201), "register relay")
    rid = relay["relay_id"]
    _round(treasurer_token)
    expect(_answer(token, rid, expect(_probe(token, rid), (200,), "probe")), (200, 201), "answer")
    with client(token) as c:
        chosen = expect(c.put(f"/conversations/{conv}/core-node", json={"relay_id": rid}), (200,), "choose core node")
    assert chosen["routing"]["mode"] == "core_node" and not chosen["routing"]["fell_back"], f"routing reads {chosen['routing']}"
    _round(treasurer_token)
    missed = conversation_state(token, conv)["routing"]
    assert missed["mode"] == "open_network" and missed["fell_back"] is True, (
        f"after the core node missed the latest round routing reads {missed}")
    expect(_answer(token, rid, expect(_probe(token, rid), (200,), "probe")), (200, 201), "answer latest")
    back = conversation_state(token, conv)["routing"]
    assert back["mode"] == "core_node" and not back["fell_back"], f"after answering routing reads {back}"


def _position(treasurer_token: str, contact_code: str, schedule: str, allocation: int) -> None:
    with client(treasurer_token) as c:
        expect(c.post("/token/positions", json={"contact_code": contact_code, "schedule": schedule,
                                                "allocation_micro": allocation}), (200, 201), f"create {schedule} position")


def _launch(treasurer_token: str, days_ago: float) -> dt.datetime:
    moment = now_utc() - dt.timedelta(days=days_ago)
    with client(treasurer_token) as c:
        expect(c.put("/token/event", json={"launch_at": iso(moment)}), (200,), "set token event")
    return moment


def _positions(token: str) -> dict:
    with client(token) as c:
        return {p["schedule"]: p for p in expect(c.get("/token/positions"), (200,), "GET positions")}


def _claim(token: str, position_id: str) -> dict:
    with client(token) as c:
        return expect(c.post("/token/claims", json={"position_id": position_id}), (200, 201), "claim")


def test_simultaneous_claims_transfer_the_claimable_balance_once(treasurer_token):
    holder = signup()
    allocation = 10 ** 12
    _position(treasurer_token, holder["contact_code"], "visioners", allocation)
    launched = _launch(treasurer_token, 120)
    position = _positions(holder["access_token"])["visioners"]
    low = vested("visioners", allocation, launched, now_utc())
    clients = warm_clients([holder["access_token"]] * 6)
    results = barrier_run(6, lambda i: clients[i].post("/token/claims", json={"position_id": position["position_id"]}))
    high = vested("visioners", allocation, launched, now_utc() + dt.timedelta(seconds=1))
    for c in clients:
        c.close()
    amounts = [body(r).get("transferred_micro", 0) for r in results if r is not None and r.status_code in (200, 201)]
    assert all(r is not None and r.status_code < 500 for r in results), "simultaneous claims answered a server error"
    assert len([a for a in amounts if a > 0]) == 1, f"simultaneous claims transferred {amounts}"
    assert low <= sum(amounts) <= high, f"simultaneous claims transferred {sum(amounts)}, vested was {low} to {high}"
    assert _positions(holder["access_token"])["visioners"]["claimed_micro"] == sum(amounts), "claimed_micro disagrees"


def test_claims_across_token_event_corrections_total_the_allocation(treasurer_token):
    holder = signup()
    allocation = 999999999999
    _position(treasurer_token, holder["contact_code"], "visioners", allocation)
    token = holder["access_token"]
    position_id = _positions(token)["visioners"]["position_id"]
    total = 0
    for days in (95, 101.3, 133.7, 170.05, 222.2, 299.9, 359.99):
        _launch(treasurer_token, days)
        got = _claim(token, position_id)
        total += got["transferred_micro"]
        assert got["claimed_micro"] == total, f"after claiming at day {days} claimed_micro reads {got['claimed_micro']}, sum {total}"
    _launch(treasurer_token, 100)
    back = _positions(token)["visioners"]
    assert back["claimable_micro"] == 0, f"moving the token event later leaves claimable {back['claimable_micro']}"
    assert _claim(token, position_id)["transferred_micro"] == 0, "a claim with nothing vested transferred tokens"
    _launch(treasurer_token, 400)
    final = _claim(token, position_id)
    total += final["transferred_micro"]
    assert total == allocation and final["claimed_micro"] == allocation, (
        f"claims across corrections total {total}, allocation {allocation}")
    assert _positions(token)["visioners"]["claimable_micro"] == 0, "a fully claimed position still shows claimable"


def test_cliff_accrues_and_releases_in_a_lump_for_every_schedule(treasurer_token):
    holder = signup()
    rows = {"visioners": 10 ** 12, "team": 3 * 10 ** 11, "liquidity": 5 * 10 ** 10, "community": 37 * 10 ** 9}
    for schedule, allocation in rows.items():
        _position(treasurer_token, holder["contact_code"], schedule, allocation)
    for days in (89, 91, 359, 361):
        launched = _launch(treasurer_token, days)
        low_time = now_utc()
        held = _positions(holder["access_token"])
        high_time = now_utc()
        for schedule, allocation in rows.items():
            low = vested(schedule, allocation, launched, low_time)
            high = vested(schedule, allocation, launched, high_time + dt.timedelta(seconds=2))
            claimable = held[schedule]["claimable_micro"]
            assert low <= claimable <= high, (
                f"{schedule} at day {days} shows claimable {claimable}, expected between {low} and {high}")


def test_simultaneous_whitelist_applications_from_one_wallet_file_one_and_email_once(treasurer_token):
    wallet = Wallet()
    email = unique_email()
    bodies = [dict(signed_body(wallet, "whitelist"), email=email, intended_usd_cents=1000000) for _ in range(5)]
    clients = warm_clients([None] * 5)
    results = barrier_run(5, lambda i: clients[i].post("/whitelist/applications", json=bodies[i]))
    for c in clients:
        c.close()
    statuses = [r.status_code for r in results if r is not None]
    accepted = [r for r in results if r is not None and r.status_code in (200, 201)]
    assert len(accepted) == 1 and body(accepted[0]).get("state") == "applied", (
        f"five simultaneous applications from one wallet answered {statuses}")
    assert all(s in (200, 201) or s in CLIENT_ERRORS for s in statuses), f"applications answered {statuses}"
    wait_for_mail(email, WHITELIST_SUBJECT)
    settle(3.0)
    mails = mails_to(email, WHITELIST_SUBJECT)
    assert len(mails) == 1 and mails[0]["to"] == [email.lower()] and not mails[0]["cc"] and not mails[0]["bcc"], (
        f"the applicant received {len(mails)} acknowledgement emails")
    assert mails[0]["text"].strip().startswith(WHITELIST_APPLIED), f"the acknowledgement begins {mails[0]['text'][:120]!r}"
    with client(treasurer_token) as c:
        listed = [a for a in expect(c.get("/whitelist/applications"), (200,), "GET applications") if a["address"] == wallet.address]
    assert len(listed) == 1, f"the treasurer sees {len(listed)} applications from the wallet"
    with client() as c:
        later = c.post("/whitelist/applications", json=dict(signed_body(wallet, "whitelist"), email=email,
                                                             intended_usd_cents=1000000))
    assert later.status_code in CLIENT_ERRORS, f"a second application from one wallet answered {later.status_code}"


def test_whitelist_stepper_back_keeps_entries_and_applies(browser_page):
    wallet = Wallet()
    email = unique_email()
    ctx = _desktop(browser_page)
    page = ctx.new_page()
    page.goto(f"{app_url()}/whitelist")
    page.get_by_label("Wallet address", exact=True).fill(wallet.address)
    page.get_by_role("button", name="Get message to sign", exact=True).click()
    field = page.get_by_label("Message to sign", exact=True)
    field.wait_for(state="visible", timeout=15000)
    for _ in range(30):
        if (field.input_value() if field.evaluate("e => 'value' in e") else field.inner_text()).strip():
            break
        page.wait_for_timeout(500)
    message = field.input_value() if field.evaluate("e => 'value' in e") else field.inner_text()
    assert "It cannot move funds." in message, f"the stepper shows the message {message[:200]!r}"
    page.get_by_label("Signature", exact=True).fill(wallet.sign(message))
    page.get_by_role("button", name="Continue", exact=True).click()
    page.wait_for_url(re.compile(r".*/whitelist/details.*"), timeout=15000)
    page.get_by_label("Email", exact=True).fill(email)
    page.get_by_label("Amount in USD", exact=True).fill("25000")
    page.get_by_role("button", name="Continue", exact=True).click()
    page.wait_for_url(re.compile(r".*/whitelist/review.*"), timeout=15000)
    page.get_by_role("button", name="Back", exact=True).click()
    page.wait_for_url(re.compile(r".*/whitelist/details.*"), timeout=15000)
    kept = (page.get_by_label("Email", exact=True).input_value(), page.get_by_label("Amount in USD", exact=True).input_value())
    assert kept[0] == email and kept[1].replace(",", "") == "25000", f"after Back the details read {kept}"
    page.get_by_role("button", name="Continue", exact=True).click()
    page.wait_for_url(re.compile(r".*/whitelist/review.*"), timeout=15000)
    page.get_by_role("button", name="Apply", exact=True).click()
    assert wait_for_text(page, WHITELIST_APPLIED, reload_every=0), "applying shows no not-an-allocation line"
    ctx.close()


def test_whitelist_amount_outside_the_cheque_limits_is_refused():
    with client() as c:
        for cents, ok in ((499999, False), (5000001, False), (500000, True), (5000000, True)):
            wallet = Wallet()
            response = c.post("/whitelist/applications", json=dict(signed_body(wallet, "whitelist"),
                                                                     email=unique_email(), intended_usd_cents=cents))
            if ok:
                assert response.status_code in (200, 201), f"an application for {cents} cents answered {response.status_code}"
            else:
                assert response.status_code in CLIENT_ERRORS, f"an application for {cents} cents answered {response.status_code}"


def test_payment_settling_after_close_belongs_to_the_next_epoch(treasurer_token):
    account = signup()
    fresh_rates()
    q = quote(account["access_token"], "njr")
    tx = "0x" + os.urandom(32).hex()
    seen = payment_event(q, q["amount_due"], 3, now_utc() - dt.timedelta(seconds=5), tx)
    expect(watcher_post("/watcher/payments", seen), (200, 201, 202), "report payment below depth")
    with client(treasurer_token) as c:
        open_number = next(e["number"] for e in expect(c.get("/epochs"), (200,), "GET epochs") if e["state"] == "open")
    before = _epoch(treasurer_token, open_number)["contributions_micro"]
    with client(treasurer_token) as c:
        closed = expect(c.post("/epochs/current/close"), (200, 201), "close epoch")
    assert closed["closed"]["number"] == open_number and closed["opened"]["number"] == open_number + 1, f"closing answered {closed}"
    expect(watcher_post("/watcher/payments", dict(seen, confirmations=12)), (200, 201, 202), "report payment at depth")
    assert _payment(account["access_token"], tx)["state"] == "settled", "the payment did not settle after the close"
    assert _epoch(treasurer_token, open_number)["contributions_micro"] == before, (
        "a payment settling after the close changed the closed epoch")
    assert _epoch(treasurer_token, open_number + 1)["contributions_micro"] == q["amount_due"], (
        "a payment settling after the close is not in the next epoch's contributions")
