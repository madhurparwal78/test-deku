"""Outcome graders for the Tempo catalogue task.

One module, every section and all three declared slots. Black-box: HTTP against
the running app, the rendered page through Playwright, PostgreSQL through the
shared backend adapter, Kill Bill through the shared payments adapter and Mailpit
through the shared inbox adapter. Nothing here reads the agent's source.
"""

from __future__ import annotations

import os
import re

import httpx

import capabilities
from conftest import (
    ABSENT_ARTICLE, ABSENT_CATEGORY, ABSENT_RUNTIME, ABSENT_VERSION, ARTICLES,
    BAND_MINOR, BOOTSTRAP_BILLING_KEYS, CATEGORIES, CATEGORY_PATHS, CHANGELOG,
    COUNTRY, CURRENCY, CURRENT, DISCOUNT_BAND, DISCOUNT_REASON,
    DISCOUNT_REGION, DOC_PAGES, DOC_RUNTIME, DOC_SLUG, EXAMPLES, FREE_EXAMPLE,
    FREE_EXAMPLES, JOINED, LICENCE_PREFIX, LIST_BAND, LIST_MINOR, LIST_REGION,
    MEMBER2_EMAIL, MEMBER2_HANDLE, MEMBER2_NAME, MEMBER3_EMAIL,
    MEMBER3_HANDLE, MEMBER3_NAME, MEMBER_EMAIL, MEMBER_HANDLE, MEMBER_NAME,
    NOT_FOUND_LABEL, NOT_FOUND_ROUTES, OK, OLDEST, PAID_EXAMPLE,
    PAID_EXAMPLES, PASSWORD, PRIOR, PUBLIC_ROUTES, PUBLISHED_PROJECT,
    RECEIPT_SUBJECT_PREFIX, REGION_HEADER, RELEASES, RUNTIMES, SAVED_AT_SEED,
    SECTIONS, SECURITY_HEADERS, SLASH_PAIRS, SUBMITTED_PROJECT, THEME_KEYS,
    THEME_PREFERENCE, THEME_STAGGER, THEME_TRANSITIONS, THEME_TRAVEL, TIMEOUT,
    UI_VERSION, UNKNOWN_REGION, anon, anon_discounted, anon_list_region,
    api_base, article_of, backend, base_url, billing_account, billing_keys,
    body, browser, buy, categories_of, changelog_of, client_for,
    contrast_ratio, denied, describe, docs_page, example_files, example_of,
    fresh_member, gallery, gallery_items, gallery_slugs, head_tag, html_of,
    inbox, licence_table, login, magazine_of, member, member2, message,
    meta_content, narrow_page, ok, page, parse_colour, pricing, probe_handle,
    profile_of, projects_of, purchase, raw_file, raw_get, refused,
    revoke_licence, rows, save, saved_of, sections_of, settle, signup,
    submit_project, theme_of, token_for, token_hex, unsave, unsave_after,
    wait_until, who,
)


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


def _serialised(payload) -> str:
    import json
    return json.dumps(payload, default=str)


def test_health_returns_200_and_pages_share_one_origin():
    """Health answers 200 and the pages share the app origin. cov: C-OV-01, C-TR-18, C-TR-19, C-TR-41, C-TR-42, C-CN-15, C-DC-01, C-DC-03, C-DC-09, C-DC-10"""

    response = httpx.get(f"{base_url()}/api/health", timeout=TIMEOUT)
    assert response.status_code == 200, f"health must return 200 once ready: {describe(response)}"
    page_response = html_of("/examples")
    assert page_response.status_code == 200, f"the gallery must be served: {describe(page_response)}"
    assert "text/html" in page_response.headers.get("content-type", ""), \
        f"the pages must be served on the app's own origin and port: {describe(page_response)}"
    assert str(page_response.url).startswith(base_url()), \
        f"the pages must be served from APP_PUBLIC_URL, found {page_response.url}"
    api = httpx.get(f"{api_base()}/categories", timeout=TIMEOUT)
    assert api.status_code == 200, f"the read surface must share the pages' origin: {describe(api)}"


def test_app_root_keeps_reserved_screenshot_and_download_directories():
    """The app root keeps the two reserved directories. cov: C-DC-06, C-DC-07"""

    for name in (".browser_screenshots", ".downloads"):
        assert os.path.isdir(f"/app/{name}"), \
            f"the reserved directory /app/{name} must exist at the app root"


def test_a_favicon_is_served_and_declared_in_every_document_head():
    """A favicon is served and declared in every document head. cov: C-CF-231, C-TR-47"""

    icon = raw_get("/favicon.ico")
    assert icon.status_code == 200 and icon.content, \
        f"/favicon.ico must serve real bytes: {describe(icon)}"
    for route in PUBLIC_ROUTES:
        document = html_of(route)
        assert document.status_code == 200, f"{route} must be served: {describe(document)}"
        declared = re.search(r'<link[^>]+rel=["\'][^"\']*icon[^"\']*["\']', document.text, re.I)
        assert declared, f"{route} must declare a favicon link in its head"


def test_every_public_route_declares_its_own_title_and_description():
    """Every public route declares its own title and description. cov: C-CF-226, C-CF-232, C-CF-233, C-TR-48, C-TR-49"""

    titles, descriptions = {}, {}
    for route in PUBLIC_ROUTES:
        document = html_of(route)
        assert document.status_code == 200, f"{route} must be served: {describe(document)}"
        title = head_tag(document.text, r"<title[^>]*>(.*?)</title>")
        assert title and title.strip(), f"{route} must declare a document title"
        description = meta_content(document.text, "description")
        assert description and description.strip(), f"{route} must declare a meta description"
        titles[route] = title.strip()
        descriptions[route] = description.strip()
    for holder, label in ((titles, "title"), (descriptions, "description")):
        seen = {}
        for route, value in holder.items():
            assert value not in seen, \
                f"{route} and {seen[value]} share one {label}: {value!r}"
            seen[value] = route
    current = html_of(f"/docs/{DOC_RUNTIME}/{DOC_SLUG}")
    pinned = html_of(f"/docs/{PRIOR}/{DOC_RUNTIME}/{DOC_SLUG}")
    assert meta_content(current.text, "description") != meta_content(pinned.text, "description"), \
        "a versioned documentation address must describe itself as that release"


def test_the_privacy_page_states_what_is_collected_and_for_how_long():
    """The privacy page states what is collected and for how long. cov: C-RL-12, C-CF-234, C-CN-13"""

    document = html_of("/privacy")
    assert document.status_code == 200, f"/privacy must be served: {describe(document)}"
    text = re.sub(r"<[^>]+>", " ", document.text).lower()
    for phrase in ("collect", "kept"):
        assert phrase in text, f"/privacy must state what is {phrase}ed: missing {phrase!r}"
    assert "shared" in text or "share" in text, \
        "/privacy must state that nothing recorded is shared"
    for route in ("/", "/examples", "/plus"):
        footer = html_of(route)
        assert "/privacy" in footer.text, f"{route} must link the privacy page from its footer"


def test_the_terms_page_states_the_licence_and_that_it_never_renews():
    """The terms page states the licence and that nothing renews. cov: C-CF-235, C-UF-16"""

    document = html_of("/terms")
    assert document.status_code == 200, f"/terms must be served: {describe(document)}"
    text = re.sub(r"<[^>]+>", " ", document.text).lower()
    assert "licence" in text or "license" in text, "/terms must state the licence"
    assert "perpetual" in text, "/terms must state that the paid licence is perpetual"
    assert "renew" in text, "/terms must state that nothing renews"
    for route in ("/", "/examples", "/plus"):
        footer = html_of(route)
        assert "/terms" in footer.text, f"{route} must link the terms page from its footer"


def test_security_headers_ride_on_every_response():
    """The security headers ride on every response. cov: C-CF-236, C-TR-43"""

    def carries(headers) -> list:
        names = {name.lower() for name in headers}
        policy = headers.get("content-security-policy", "").lower()
        missing = [h for h in SECURITY_HEADERS if h != "x-frame-options" and h not in names]
        if "x-frame-options" not in names and "frame-ancestors" not in policy:
            missing.append("a frame policy")
        return missing
    for route in ("/", "/examples", f"/docs/{DOC_RUNTIME}/{DOC_SLUG}", "/plus"):
        document = raw_get(route, follow_redirects=True)
        assert not carries(document.headers), \
            f"{route} must carry every security header, missing {carries(document.headers)}"
    api = httpx.get(f"{api_base()}/categories", timeout=TIMEOUT)
    assert not carries(api.headers), \
        f"the read surface must carry every security header, missing {carries(api.headers)}"


def test_an_unknown_address_renders_the_not_found_document_on_the_server():
    """An unknown address renders the not-found document on the server. cov: C-CF-228, C-CF-229, C-UF-17, C-FE-93"""

    for route in NOT_FOUND_ROUTES:
        document = raw_get(route)
        assert document.status_code == 404, \
            f"{route} must answer with the not-found status: {describe(document)}"
        assert "text/html" in document.headers.get("content-type", ""), \
            f"{route} must answer with a document: {describe(document)}"
        assert NOT_FOUND_LABEL in document.text, \
            f"{route} must carry {NOT_FOUND_LABEL} in the served markup, not after the client boots"
        home = re.search(r'href=["\'](/|' + re.escape(base_url()) + r'/?)["\']', document.text)
        assert home, f"{route} must carry a link home in the served markup"


def test_one_slash_form_is_canonical_and_the_other_redirects_permanently():
    """One slash form is canonical and the other redirects permanently. cov: C-CF-25, C-CF-26, C-CF-102, C-UF-20, C-FE-94"""

    for plain, trailing in SLASH_PAIRS:
        first = raw_get(plain)
        second = raw_get(trailing)
        codes = {plain: first.status_code, trailing: second.status_code}
        moved = [path for path, code in codes.items() if code in (301, 308)]
        served = [path for path, code in codes.items() if code == 200]
        assert len(moved) == 1 and len(served) == 1, \
            f"exactly one of {plain} and {trailing} must be canonical: {codes}"
        target = (first if moved[0] == plain else second).headers.get("location", "")
        assert served[0].rstrip("/") in target.rstrip("/") or target.endswith(served[0]), \
            f"{moved[0]} must redirect to {served[0]}, found {target!r}"
        canonical = html_of(plain)
        declared = head_tag(canonical.text, r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']')
        assert declared, f"{plain} must declare a canonical link element"
        assert declared.rstrip("/").endswith(served[0].rstrip("/")), \
            f"the canonical link on {plain} must name {served[0]}, found {declared!r}"


def test_the_sitemap_lists_every_public_route_and_robots_points_at_it():
    """The sitemap lists every public route and robots points at it. cov: C-CF-238, C-TR-54, C-CN-10"""

    sitemap = raw_get("/sitemap.xml")
    assert sitemap.status_code == 200, f"/sitemap.xml must be served: {describe(sitemap)}"
    for route in PUBLIC_ROUTES:
        assert route in sitemap.text, f"the sitemap must list {route}"
    robots = raw_get("/robots.txt")
    assert robots.status_code == 200, f"/robots.txt must be served: {describe(robots)}"
    assert "sitemap" in robots.text.lower(), "/robots.txt must point at the sitemap"


def test_no_stored_credential_reaches_anything_the_browser_downloads(anon):
    """No stored credential reaches anything the browser downloads. cov: C-CF-237, C-TR-26, C-TR-46, C-TR-55"""

    secrets = [os.environ["PAYMENTS_API_SECRET"]]
    admin = os.environ.get("DB_ADMIN_URL", "")
    held = re.search(r"://[^:]+:([^@]+)@", admin)
    if held:
        secrets.append(held.group(1))
    downloads = []
    for route in PUBLIC_ROUTES:
        document = html_of(route)
        downloads.append((route, document.text))
        for match in re.findall(r'(?:src|href)=["\']([^"\']+\.(?:js|css|json))["\']', document.text):
            if match.startswith("http") and base_url() not in match:
                continue
            asset = raw_get(match if match.startswith("/") else f"/{match}")
            if asset.status_code == 200:
                downloads.append((match, asset.text))
    for where, text in downloads:
        for value in secrets:
            assert value not in text, f"{where} carries a stored credential in what the browser downloads"
    assert os.environ["PAYMENTS_API_SECRET"] not in _serialised(gallery(anon)), \
        "the gallery payload must carry no billing secret"


def test_body_text_meets_the_contrast_bar_against_its_background(page):
    """Body text meets the contrast bar against its background. cov: C-UX-48, C-UX-49"""

    page.goto(f"{base_url()}/")
    page.wait_for_load_state("networkidle")
    sampled = page.evaluate("""() => {
        const out = [];
        for (const node of document.querySelectorAll('p, li, span, div')) {
            if (!node.textContent || node.textContent.trim().length < 24) continue;
            if (node.children.length) continue;
            const style = getComputedStyle(node);
            const size = parseFloat(style.fontSize);
            if (!size || size > 16) continue;
            let ground = 'rgb(0, 0, 0)';
            let walker = node;
            while (walker) {
                const back = getComputedStyle(walker).backgroundColor;
                if (back && back !== 'rgba(0, 0, 0, 0)' && back !== 'transparent') {
                    ground = back;
                    break;
                }
                walker = walker.parentElement;
            }
            out.push({ink: style.color, ground: ground, size: size});
            if (out.length >= 24) break;
        }
        return out;
    }""")
    assert sampled, "the homepage must render body text the contrast pass can sample"
    for row in sampled:
        ratio = contrast_ratio(parse_colour(row["ink"]), parse_colour(row["ground"]))
        assert ratio >= 4.5, (
            f"body text at {row['size']}px must meet 4.5:1, found {ratio:.2f} for "
            f"{row['ink']} on {row['ground']}")


def test_a_narrow_viewport_shows_no_sideways_overflow(narrow_page):
    """A narrow viewport shows no sideways overflow. cov: C-FE-100"""

    for route in ("/", "/examples", "/ui", "/plus", f"/@{MEMBER_HANDLE}"):
        narrow_page.goto(f"{base_url()}{route}")
        narrow_page.wait_for_load_state("networkidle")
        widths = narrow_page.evaluate(
            "() => [document.documentElement.scrollWidth, window.innerWidth]")
        assert widths[0] <= widths[1] + 1, \
            f"{route} overflows sideways at 390px: document {widths[0]}px in {widths[1]}px"


def test_the_declared_stack_serves_every_page_and_the_api_from_one_process():
    """The declared stack serves every page and the read surface from one origin. cov: C-OV-12, C-UX-13, C-FE-52, C-FE-89, C-TR-02, C-TR-07, C-TR-20, C-TR-21, C-CN-06, C-CN-14, C-DC-02, C-DC-04, C-DC-08, C-DC-11, C-DC-12"""

    for route in ("/", "/examples", "/ui", "/plus"):
        document = html_of(route)
        assert document.status_code == 200, f"{route} must be served: {describe(document)}"
        assert str(document.url).startswith(base_url()), \
            f"{route} must be served from APP_PUBLIC_URL, found {document.url}"
    for path in ("/categories", "/theme", "/releases"):
        api = httpx.get(f"{api_base()}{path}", timeout=TIMEOUT)
        assert api.status_code == 200, \
            f"the read surface {path} must answer on the pages' own origin: {describe(api)}"
        assert "json" in api.headers.get("content-type", ""), \
            f"the read surface {path} must answer JSON under /api: {describe(api)}"


def test_seeded_accounts_are_stored_once_with_hashed_passwords(backend):
    """The three seeded accounts are stored once, hashed, and listed in the credentials file. cov: C-RL-13, C-RL-14, C-RL-15, C-RL-16, C-CF-09, C-TR-30, C-DM-02, C-DM-46, C-DC-05"""

    expected = {MEMBER_EMAIL: (MEMBER_NAME, MEMBER_HANDLE),
                MEMBER2_EMAIL: (MEMBER2_NAME, MEMBER2_HANDLE),
                MEMBER3_EMAIL: (MEMBER3_NAME, MEMBER3_HANDLE)}
    for email, (name, handle) in expected.items():
        assert backend.count("accounts", email=email) == 1, \
            f"seeded account {email} must exist exactly once"
        stored = backend.rows("accounts", limit=1, email=email)[0]
        assert stored.get("handle") == handle, f"seeded account {email}: {stored}"
        assert str(stored.get("display_name") or "") == name, f"seeded account {email}: {stored}"
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


def test_login_refuses_a_wrong_password_and_an_unknown_email_alike():
    """A wrong password and an unknown email are refused alike. cov: C-CF-02, C-CF-05, C-CF-06, C-TR-35"""

    wrong = login(MEMBER_EMAIL, "not-the-password")
    refused(wrong, "a wrong password")
    unknown = login(f"nobody-{token_hex()}@example.com")
    refused(unknown, "an unknown email")
    assert "Sign in failed" in message(wrong), \
        f"a wrong password must be refused with `Sign in failed`: {describe(wrong)}"
    assert message(wrong) == message(unknown), (
        "an unknown email and a wrong password must be refused with one message, "
        f"found {message(wrong)!r} and {message(unknown)!r}")
    good = login(MEMBER_EMAIL)
    assert good.status_code in OK and good.json().get("token"), \
        f"the seeded password must work: {describe(good)}"


def test_missing_unknown_and_expired_tokens_are_refused(anon, member):
    """A missing, unknown or expired token is refused. cov: C-CF-03, C-CF-04, C-CF-07, C-CF-08, C-TR-08, C-DM-50, C-DC-14"""

    denied(anon.get("/saved"), "a read of the saved rows with no token")
    with client_for(f"not-a-real-token-{token_hex(24)}") as stranger:
        denied(stranger.get("/saved"), "a read of the saved rows with an unknown token")
        denied(stranger.post("/saved", json={"example_slug": FREE_EXAMPLE}),
               "a save with an unknown token")
    before = set(saved_of(member))
    denied(anon.post("/saved", json={"example_slug": PAID_EXAMPLE}), "a save with no token")
    assert set(saved_of(member)) == before, \
        "a refused unauthenticated write must leave the saved rows unchanged"
    live = ok(member.get("/me"), "the signed-in member")
    assert who(live).get("handle") == MEMBER_HANDLE, f"/me must name the signed-in member: {live}"


def test_signup_refuses_a_duplicate_email_and_a_duplicate_folded_handle():
    """Signup refuses a duplicate email and a duplicate folded handle. cov: C-RL-11, C-CF-01, C-CF-10, C-CF-11, C-CF-12, C-UF-13, C-TR-64"""

    created = signup()
    with client_for(created["token"]) as session:
        assert who(ok(session.get("/me"), "the new member")).get("handle") == created["handle"]
    same_email = httpx.post(f"{api_base()}/auth/signup", json={
        "email": created["email"], "name": "Another Probe",
        "handle": probe_handle(), "password": PASSWORD}, timeout=TIMEOUT)
    refused(same_email, "a signup on an email that already has an account")
    assert "email" in _serialised(body(same_email)).lower(), \
        f"the refusal must name the email field: {describe(same_email)}"
    folded = httpx.post(f"{api_base()}/auth/signup", json={
        "email": f"other-{token_hex()}@example.com", "name": "Another Probe",
        "handle": created["handle"].upper(), "password": PASSWORD}, timeout=TIMEOUT)
    refused(folded, "a signup on a handle that already has an account, in another case")
    assert "handle" in _serialised(body(folded)).lower(), \
        f"the refusal must name the handle field: {describe(folded)}"


def test_a_docs_address_without_a_version_names_the_current_release(anon):
    """A documentation address without a version names the current release. cov: C-CF-14, C-CF-15, C-CF-16, C-UF-04, C-TR-37, C-TR-62, C-DM-03, C-DM-04, C-DM-29"""

    page_body = ok(docs_page(anon, DOC_RUNTIME, DOC_SLUG), "the current documentation page")
    assert page_body.get("release") == CURRENT, \
        f"an address with no version must name the current release {CURRENT}: {page_body.get('release')}"
    title, since, tier = DOC_PAGES[(DOC_RUNTIME, DOC_SLUG)]
    assert page_body.get("title") == title, f"the page title must be {title!r}: {page_body}"
    assert page_body.get("tier") == tier, f"the page tier must be {tier!r}: {page_body}"
    document = html_of(f"/docs/{DOC_RUNTIME}/{DOC_SLUG}")
    assert CURRENT in document.text, \
        f"the rendered page must name the release {CURRENT} it is serving"
    listed = rows(anon.get("/releases"), "the release listing")
    current = [row for row in listed if row.get("is_current")]
    assert len(current) == 1 and current[0].get("version") == CURRENT, \
        f"exactly one release must be current, and it must be {CURRENT}: {listed}"


def test_a_versioned_docs_address_stays_on_the_release_it_names(anon):
    """A versioned documentation address stays on the release it names. cov: C-CF-17, C-CF-221, C-CF-222, C-UF-05, C-UF-39, C-TR-60, C-DM-05, C-DC-18"""

    for version in (PRIOR, OLDEST):
        page_body = ok(docs_page(anon, DOC_RUNTIME, DOC_SLUG, version),
                       f"the documentation page at {version}")
        assert page_body.get("release") == version, \
            f"/docs/{version}/... must name {version}: {page_body.get('release')}"
        document = html_of(f"/docs/{version}/{DOC_RUNTIME}/{DOC_SLUG}")
        assert document.status_code == 200 and version in document.text, \
            f"the rendered page at {version} must name that release: {describe(document)}"
    current = ok(docs_page(anon, DOC_RUNTIME, DOC_SLUG), "the current page")
    pinned = ok(docs_page(anon, DOC_RUNTIME, DOC_SLUG, PRIOR), "the pinned page")
    assert current.get("release") != pinned.get("release"), \
        "the versioned address must not resolve to the current release"


def test_a_runnable_block_carries_the_release_it_last_executed_against(anon):
    """A runnable block carries the release it last executed against. cov: C-CF-19, C-CF-20, C-DM-37, C-DM-38, C-DC-17"""

    page_body = ok(docs_page(anon, DOC_RUNTIME, DOC_SLUG), "the current documentation page")
    blocks = page_body.get("code_blocks") or []
    assert blocks, f"a documentation page must carry code blocks: {page_body}"
    runnable = [block for block in blocks if block.get("is_runnable")]
    assert runnable, f"a documentation page must carry a runnable block: {blocks}"
    for block in runnable:
        against = str(block.get("executed_against_version") or "")
        assert against in RELEASES, \
            f"a runnable block must name the release it last ran against: {block}"
        assert block.get("source"), f"a runnable block must carry its source: {block}"
    document = html_of(f"/docs/{DOC_RUNTIME}/{DOC_SLUG}")
    for block in runnable:
        assert str(block.get("executed_against_version")) in document.text, \
            "the rendered page must show the release each runnable block ran against"


def test_an_unknown_runtime_and_an_unretained_version_answer_not_found(anon):
    """An unknown runtime and an unretained version answer as not found. cov: C-CF-18, C-CF-21, C-CF-22, C-UF-03"""

    unknown_runtime = docs_page(anon, ABSENT_RUNTIME, DOC_SLUG)
    assert unknown_runtime.status_code == 404, \
        f"an unknown runtime must answer as not found: {describe(unknown_runtime)}"
    unretained = docs_page(anon, DOC_RUNTIME, DOC_SLUG, ABSENT_VERSION)
    assert unretained.status_code == 404, \
        f"an unretained version must answer as not found: {describe(unretained)}"
    assert CURRENT not in unretained.text, \
        "an unretained version must not fall back to the current release"
    document = raw_get(f"/docs/{ABSENT_VERSION}/{DOC_RUNTIME}/{DOC_SLUG}")
    assert document.status_code == 404, \
        f"the rendered page at an unretained version must answer 404: {describe(document)}"


def test_a_docs_page_names_the_release_it_was_introduced_in(anon):
    """A documentation page names the release it was introduced in. cov: C-CF-23, C-CF-24, C-DM-06, C-DM-30, C-DM-31, C-DM-32, C-DM-33, C-DM-34, C-DM-35, C-DM-36"""

    for (runtime, slug), (title, since, tier) in DOC_PAGES.items():
        page_body = ok(docs_page(anon, runtime, slug), f"the page {runtime}/{slug}")
        assert page_body.get("since_version") == since, \
            f"{runtime}/{slug} must name {since} as the release it arrived in: {page_body}"
        assert page_body.get("title") == title, f"{runtime}/{slug}: {page_body}"
    document = html_of(f"/docs/{DOC_RUNTIME}/{DOC_SLUG}")
    assert DOC_PAGES[(DOC_RUNTIME, DOC_SLUG)][1] in document.text, \
        "the rendered page must show the release it was introduced in"


def test_every_facet_combination_is_one_server_rendered_shareable_address(anon):
    """Every facet combination is one server-rendered shareable address. cov: C-OV-02, C-CF-31, C-CF-32, C-UF-06, C-UF-26, C-TR-05, C-TR-27, C-CN-09"""

    combinations = (
        {}, {"runtime": "react"}, {"category": "hero-sections"},
        {"runtime": "react", "category": "hero-sections"},
        {"access": "free"}, {"access": "paid"},
        {"runtime": "js", "access": "free", "sort": "title"},
    )
    for facets in combinations:
        query = "&".join(f"{key}={value}" for key, value in facets.items())
        address = "/examples" + (f"?{query}" if query else "")
        document = raw_get(address)
        assert document.status_code == 200, f"{address} must be served: {describe(document)}"
        assert "text/html" in document.headers.get("content-type", ""), \
            f"{address} must be rendered on the server: {describe(document)}"
        expected = gallery_slugs(anon, **facets)
        for slug in expected:
            assert slug in document.text, \
                f"{address} must carry {slug} in the served markup, not after the client boots"
        again = raw_get(address)
        assert [s for s in expected] == gallery_slugs(anon, **facets), \
            f"{address} must produce the same list in the same order on a second visit"
        assert again.status_code == 200, f"{address} must be shareable: {describe(again)}"


def test_the_runtime_and_category_facets_narrow_the_catalogue(anon):
    """The runtime and category facets narrow the catalogue. cov: C-RL-02, C-CF-33, C-CF-35, C-CF-44, C-CF-56, C-CF-57, C-FE-14, C-DC-19"""

    for runtime in RUNTIMES:
        expected = sorted(slug for slug, row in EXAMPLES.items() if runtime in row[3])
        assert sorted(gallery_slugs(anon, runtime=runtime)) == expected, \
            f"runtime={runtime} must narrow the catalogue to {expected}"
    for path, _, _ in CATEGORIES:
        expected = sorted(slug for slug, row in EXAMPLES.items() if row[1] == path)
        assert sorted(gallery_slugs(anon, category=path)) == expected, \
            f"category={path} must narrow the catalogue to {expected}"
    both = sorted(gallery_slugs(anon, runtime="react", category="hero-sections"))
    expected = sorted(slug for slug, row in EXAMPLES.items()
                      if "react" in row[3] and row[1] == "hero-sections")
    assert both == expected, f"the two facets together must narrow to {expected}, found {both}"


def test_the_access_facet_splits_free_examples_from_paid_ones(anon):
    """The access facet splits the free examples from the paid ones. cov: C-CF-36, C-CF-37, C-CF-54, C-CF-55, C-CF-58, C-CF-59, C-CF-60"""

    assert sorted(gallery_slugs(anon, access="free")) == sorted(FREE_EXAMPLES), \
        f"access=free must serve {sorted(FREE_EXAMPLES)}"
    assert sorted(gallery_slugs(anon, access="paid")) == sorted(PAID_EXAMPLES), \
        f"access=paid must serve {sorted(PAID_EXAMPLES)}"
    items = gallery_items(anon)
    for slug, row in EXAMPLES.items():
        assert items[slug].get("tier") == row[2], \
            f"{slug} must be listed as {row[2]}: {items[slug]}"


def test_the_saved_facet_serves_an_empty_grid_to_a_signed_out_visitor(anon, member):
    """The saved facet serves an empty grid to a signed-out visitor. cov: C-CF-38, C-CF-39"""

    listed = gallery(anon, saved="1")
    assert listed.get("items") == [], \
        f"saved=1 with no session must serve an empty grid: {listed}"
    assert listed.get("total") == 0, f"the empty grid must state a total of 0: {listed}"
    document = raw_get("/examples?saved=1")
    assert document.status_code == 200, \
        f"saved=1 with no session must serve the address rather than refuse it: {describe(document)}"
    text = re.sub(r"<[^>]+>", " ", document.text).lower()
    assert "sign in" in text or "signed in" in text or "log in" in text, \
        "the empty saved grid must say why: a visitor with no session has no saved examples"
    mine = sorted(gallery_slugs(member, saved="1"))
    assert mine == sorted(SAVED_AT_SEED), \
        f"saved=1 for the seeded member must serve {sorted(SAVED_AT_SEED)}, found {mine}"


def test_the_grid_count_line_is_counted_from_the_catalogue(anon):
    """The grid count line is counted from the catalogue. cov: C-OV-03, C-CF-40, C-CF-41, C-TR-65"""

    whole = gallery(anon)
    assert whole.get("total") == len(EXAMPLES), \
        f"the unnarrowed grid must count {len(EXAMPLES)} examples: {whole.get('total')}"
    for facets in ({"runtime": "react"}, {"access": "paid"},
                   {"category": "cta-sections"}):
        listed = gallery(anon, **facets)
        assert listed.get("total") == len(listed.get("items") or []), \
            f"the count line for {facets} must equal the rows served: {listed}"
    document = raw_get("/examples")
    assert str(len(EXAMPLES)) in document.text, \
        f"the served grid must carry the counted total {len(EXAMPLES)}"
    narrowed = raw_get("/examples?access=paid")
    assert str(len(PAID_EXAMPLES)) in narrowed.text, \
        f"the narrowed grid must carry the counted total {len(PAID_EXAMPLES)}"


def test_the_three_orderings_sort_by_title_saves_and_published_date(anon):
    """The three orderings sort by title, saves and published date. cov: C-CF-34, C-CF-42, C-CF-43, C-TR-53, C-DM-08, C-DM-09, C-DM-10, C-DM-11, C-DM-12, C-DM-13, C-DM-14, C-DM-15, C-DC-13"""

    by_title = gallery_slugs(anon, sort="title")
    expected = [slug for slug, _ in sorted(EXAMPLES.items(), key=lambda row: row[1][0].casefold())]
    assert by_title == expected, f"sort=title must order alphabetically ignoring case {expected}, found {by_title}"
    by_date = gallery_slugs(anon, sort="newest")
    expected = [slug for slug, _ in sorted(EXAMPLES.items(), key=lambda row: row[1][4], reverse=True)]
    assert by_date == expected, f"sort=newest must order {expected}, found {by_date}"
    ordered = gallery(anon, sort="most-saved").get("items") or []
    counts = [row.get("save_count") for row in ordered]
    assert counts == sorted(counts, reverse=True), \
        f"sort=most-saved must order by the saved count, found {counts}"
    assert {row.get("slug") for row in ordered} == set(EXAMPLES), \
        "every ordering must serve every example"


def test_an_unknown_facet_value_answers_not_found(anon):
    """An unknown facet value answers as not found. cov: C-CF-53, C-TR-38, C-TR-63, C-DC-15"""

    for facets in ({"runtime": ABSENT_RUNTIME}, {"category": ABSENT_CATEGORY},
                   {"access": "gratis"}):
        query = "&".join(f"{key}={value}" for key, value in facets.items())
        document = raw_get(f"/examples?{query}")
        assert document.status_code == 404, \
            f"?{query} must answer as not found rather than serve the unfiltered grid: {describe(document)}"
        listed = anon.get("/examples", params=facets)
        assert listed.status_code == 404, \
            f"the read surface must answer ?{query} as not found: {describe(listed)}"


def test_an_example_page_serves_one_source_tab_per_stored_file(anon):
    """An example page serves one source tab per stored file. cov: C-CF-50, C-UF-07, C-FE-84, C-TR-56, C-DM-17"""

    detail = ok(example_of(anon, FREE_EXAMPLE), f"the example {FREE_EXAMPLE}")
    files = detail.get("files") or []
    assert files, f"a free example must serve its files: {detail}"
    paths = [row.get("path") for row in files]
    assert len(paths) == len(set(paths)), f"one tab per file, no duplicates: {paths}"
    for row in files:
        assert row.get("source"), f"every file must carry its source: {row}"
    document = html_of(f"/examples/{FREE_EXAMPLE}")
    for path in paths:
        assert path in document.text, f"the rendered page must name the tab {path}"
    title, category, tier, runtimes, published = EXAMPLES[FREE_EXAMPLE]
    listed = gallery_items(anon)[FREE_EXAMPLE]
    assert listed.get("category") == category, f"the example must name its category: {listed}"
    assert sorted(listed.get("runtimes") or []) == sorted(runtimes), \
        f"the example must name its runtimes: {listed}"


def test_a_card_states_whether_its_source_may_be_opened(anon, member):
    """A card states whether its source may be opened. cov: C-CF-49, C-DC-20"""

    anonymous = gallery_items(anon)
    for slug in FREE_EXAMPLES:
        assert anonymous[slug].get("locked") is False, \
            f"a free card must not read as locked: {anonymous[slug]}"
    for slug in PAID_EXAMPLES:
        assert anonymous[slug].get("locked") is True, \
            f"a paid card seen with no licence must read as locked: {anonymous[slug]}"
    entitled = gallery_items(member)
    for slug in PAID_EXAMPLES:
        assert entitled[slug].get("locked") is False, \
            f"a paid card seen with the licence must not read as locked: {entitled[slug]}"


def test_the_nine_seeded_categories_carry_their_blurbs_and_their_order(anon):
    """The nine seeded categories carry their blurbs and their order. cov: C-CF-66, C-CF-67, C-CF-68, C-CF-69, C-CF-70, C-CF-71, C-CF-72, C-CF-73, C-CF-74, C-CF-75, C-CF-76, C-DM-07"""

    listed = rows(anon.get("/categories"), "the category listing")
    assert len(listed) == len(CATEGORIES), \
        f"{len(CATEGORIES)} categories must be seeded, found {len(listed)}"
    assert [row.get("path") for row in listed] == list(CATEGORY_PATHS), \
        f"the categories must be served in the seeded order: {[r.get('path') for r in listed]}"
    served = {row.get("path"): row for row in listed}
    for path, name, blurb in CATEGORIES:
        assert served[path].get("name") == name, f"{path} must be named {name!r}: {served[path]}"
        assert served[path].get("blurb") == blurb, \
            f"{path} must carry its measured blurb: {served[path].get('blurb')!r}"
    document = html_of("/ui")
    for path, name, blurb in CATEGORIES:
        assert name in document.text, f"the section library must show the category {name}"


def test_a_category_count_badge_is_counted_from_the_section_catalogue(anon):
    """A category count badge is counted from the section catalogue. cov: C-CF-65, C-CF-77, C-CF-79, C-UF-09, C-DC-23"""

    served = categories_of(anon)
    for path, _, _ in CATEGORIES:
        expected = sum(1 for row in SECTIONS.values() if row[1] == path)
        assert served[path].get("section_count") == expected, \
            f"{path} must count {expected} sections, found {served[path].get('section_count')}"
    every = sections_of(anon)
    assert sorted(every) == sorted(SECTIONS), \
        f"{len(SECTIONS)} sections must be seeded: {sorted(every)}"
    for path, _, _ in CATEGORIES:
        listed = sections_of(anon, category=path)
        expected = {slug for slug, row in SECTIONS.items() if row[1] == path}
        assert set(listed) == expected, f"/ui/{path} must serve {expected}, found {set(listed)}"
    document = raw_get("/ui")
    assert str(len(SECTIONS)) in document.text, \
        f"the section library must carry the counted total {len(SECTIONS)}"


def test_the_twelve_theme_values_are_served_with_their_kinds(anon):
    """The twelve theme values are served with their kinds. cov: C-CF-80, C-CF-81, C-CF-82, C-CF-83, C-CF-84, C-CF-85, C-CF-86, C-CF-87, C-CF-88, C-CF-89, C-CF-90, C-CF-91, C-CF-92, C-CF-93, C-CF-101, C-UF-08, C-DM-27, C-DM-28, C-DC-25"""

    served = theme_of(anon)
    assert sorted(served) == sorted(THEME_KEYS), \
        f"the twelve theme keys must be served: {sorted(served)}"
    for key, (stiffness, damping) in THEME_TRANSITIONS.items():
        row = served[key]
        assert row.get("kind") == "transition", f"{key} must be a transition: {row}"
        rendered = _serialised(row.get("value"))
        assert str(stiffness) in rendered, f"{key} must carry stiffness {stiffness}: {row}"
        assert str(damping) in rendered, f"{key} must carry damping {damping}: {row}"
    for key, value in THEME_STAGGER.items():
        assert served[key].get("kind") == "stagger", f"{key} must be a stagger: {served[key]}"
        assert value in _serialised(served[key].get("value")), \
            f"{key} must be {value}: {served[key]}"
    for key, value in THEME_TRAVEL.items():
        assert served[key].get("kind") == "travel", f"{key} must be a travel: {served[key]}"
        assert value in _serialised(served[key].get("value")), \
            f"{key} must be {value}: {served[key]}"
    for key, value in THEME_PREFERENCE.items():
        assert served[key].get("kind") == "preference", f"{key} must be a preference: {served[key]}"
        assert value in _serialised(served[key].get("value")), \
            f"{key} must be {value}: {served[key]}"


def test_a_section_names_the_theme_keys_and_the_tokens_it_reads(anon):
    """A section names the theme keys and the tokens it reads. cov: C-CF-94, C-CF-95, C-CF-96, C-CF-108, C-UF-10, C-DM-19, C-DM-20, C-DM-21, C-DM-22, C-DM-23, C-DM-24, C-DM-25, C-DM-26, C-DC-24"""

    served = sections_of(anon)
    for slug, (title, category, keys) in SECTIONS.items():
        row = served[slug]
        assert row.get("title") == title, f"{slug} must be titled {title!r}: {row}"
        assert row.get("category") == category, f"{slug} must sit in {category}: {row}"
        assert sorted(row.get("theme_keys") or []) == sorted(keys), \
            f"{slug} must name the theme keys {sorted(keys)}, found {row.get('theme_keys')}"
        for key in row.get("theme_keys") or []:
            assert key in THEME_KEYS, f"{slug} names a theme key outside the twelve: {key}"
        contract = row.get("token_contract") or []
        assert contract, f"{slug} must name the style tokens it expects: {row}"
    document = html_of(f"/ui/{SECTIONS['coverflow'][1]}/coverflow")
    for key in SECTIONS["coverflow"][2]:
        assert key in document.text, f"the section page must name the theme key {key}"


def test_two_places_quoting_one_count_read_the_same_query(anon):
    """Two places quoting one count read the same query. cov: C-OV-04, C-CF-78, C-TR-66"""

    landing = raw_get("/ui")
    assert landing.status_code == 200, f"/ui must be served: {describe(landing)}"
    total = len(SECTIONS)
    occurrences = len(re.findall(rf"\b{total}\b", landing.text))
    assert occurrences >= 2, \
        f"the hero total and the catalogue action must both read {total}: {occurrences} occurrence(s)"
    for other in range(1, 60):
        if other == total:
            continue
        claim = re.search(rf"(?:VIEW ALL|view all)\s*{other}\b", landing.text)
        assert not claim, f"the catalogue action claims {other} sections while {total} exist"
    categories = categories_of(anon)
    counted = sum(row.get("section_count") or 0 for row in categories.values())
    assert counted == total, \
        f"the per-category counts must sum to the section total {total}, found {counted}"
    gallery_total = gallery(anon).get("total")
    paid_route = raw_get("/plus")
    assert str(gallery_total) in paid_route.text, \
        f"the paid route must quote the counted example total {gallery_total}"


def test_the_preview_frame_is_served_without_the_session_cookie():
    """The preview frame is served without the session cookie. cov: C-OV-08, C-CF-111, C-CF-112, C-CF-117, C-FE-96, C-TR-10, C-TR-45, C-TR-69"""

    document = html_of(f"/examples/{FREE_EXAMPLE}")
    frame = re.search(r'<iframe[^>]+src=["\']([^"\']+)["\']', document.text, re.I)
    assert frame, f"the example page must carry a framed stage: {document.text[:400]}"
    source = frame.group(1)
    address = source if source.startswith("/") else f"/{source}"
    token = token_for(MEMBER_EMAIL)
    with httpx.Client(base_url=base_url(), timeout=TIMEOUT,
                      cookies={"session": token}) as session:
        served = session.get(address)
    assert served.status_code == 200, f"the framed document must be served: {describe(served)}"
    handed = served.headers.get("set-cookie", "")
    assert "session" not in handed.lower(), \
        f"the framed document must be served without the session cookie: {handed!r}"
    assert token not in served.text, "the framed document must not carry a session token"
    assert PASSWORD not in served.text, "the framed document must not carry a credential"


def test_the_preview_frame_policy_names_one_origin_and_denies_the_rest():
    """The preview frame policy names one origin and denies the rest. cov: C-CF-109, C-CF-110, C-TR-06, C-TR-44, C-CN-08"""

    document = html_of(f"/examples/{FREE_EXAMPLE}")
    frame = re.search(r'<iframe[^>]*>', document.text, re.I)
    assert frame, f"the example page must carry a framed stage: {document.text[:400]}"
    tag = frame.group(0)
    sandbox = re.search(r'sandbox=["\']([^"\']*)["\']', tag, re.I)
    assert sandbox, f"the framed stage must carry a sandbox attribute: {tag}"
    granted = set(sandbox.group(1).lower().split())
    assert "allow-scripts" in granted, f"the frame must be granted script execution: {granted}"
    for forbidden in ("allow-forms", "allow-top-navigation", "allow-popups",
                      "allow-downloads", "allow-same-origin", "allow-modals"):
        assert forbidden not in granted, f"the frame must be granted script execution alone, found {forbidden}"
    src = re.search(r'src=["\']([^"\']+)["\']', tag, re.I)
    assert src, f"the framed stage must load a document: {tag}"
    address = src.group(1)
    served = raw_get(address if address.startswith("/") else f"/{address}") \
        if not address.startswith("http") else httpx.get(address, timeout=TIMEOUT)
    policy = served.headers.get("content-security-policy", "")
    assert policy, f"the framed document must carry a content security policy: {dict(served.headers)}"
    origin = re.match(r"https?://[^/]+", base_url()).group(0)
    assert "'self'" in policy or origin in policy, \
        f"the frame policy must name the app's own origin: {policy}"
    for directive in re.split(r";\s*", policy):
        sources = directive.split()[1:]
        assert "*" not in sources and "https:" not in sources and "http:" not in sources, \
            f"the frame policy must name no destination beyond the app's own origin: {directive}"


def test_a_member_surface_read_from_inside_the_preview_frame_is_refused(anon):
    """A member surface read from inside the preview frame is refused. cov: C-CF-113, C-CF-114, C-TR-70, C-TR-71"""

    document = html_of(f"/examples/{FREE_EXAMPLE}")
    frame = re.search(r'<iframe[^>]+src=["\']([^"\']+)["\']', document.text, re.I)
    assert frame, "the example page must carry a framed stage"
    address = frame.group(1)
    served = raw_get(address if address.startswith("/") else f"/{address}") \
        if not address.startswith("http") else httpx.get(address, timeout=TIMEOUT)
    token = token_for(MEMBER_EMAIL)
    assert token not in served.text, "the framed document must carry no session token"
    assert "authorization" not in served.text.lower() or "bearer " not in served.text.lower(), \
        "the framed document must carry no credential to replay"
    refusal = anon.get("/saved")
    denied(refusal, "a member-surface read carrying no credential, which is all a sandboxed frame holds")
    assert MEMBER_HANDLE not in _serialised(body(refusal)), \
        "the refusal must reveal nothing about any member's saved rows"


def test_the_price_band_is_resolved_from_the_seeded_region_table(anon_discounted, anon_list_region):
    """The price band is resolved from the seeded region table. cov: C-CF-126, C-CF-127, C-CF-128, C-CF-129, C-CF-130, C-CF-131, C-DM-45"""

    discounted = pricing(anon_discounted)
    assert discounted.get("currency") == CURRENCY, f"the currency must be {CURRENCY}: {discounted}"
    assert discounted.get("list_amount_minor") == LIST_MINOR, \
        f"the list price must be {LIST_MINOR} minor units: {discounted}"
    band = discounted.get("band") or {}
    assert band.get("code") == DISCOUNT_BAND, \
        f"the region {DISCOUNT_REGION} must resolve to {DISCOUNT_BAND}: {discounted}"
    assert band.get("amount_minor") == BAND_MINOR, \
        f"the band {DISCOUNT_BAND} must be {BAND_MINOR} minor units: {band}"
    assert band.get("reason") == DISCOUNT_REASON, \
        f"the band must carry the reason {DISCOUNT_REASON!r}: {band}"
    plain = pricing(anon_list_region)
    assert (plain.get("band") or {}).get("code") == LIST_BAND, \
        f"the region {LIST_REGION} must resolve to {LIST_BAND}: {plain}"
    assert (plain.get("band") or {}).get("amount_minor") == LIST_MINOR, \
        f"the list band must be {LIST_MINOR} minor units: {plain}"
    with client_for(None, region=UNKNOWN_REGION) as nowhere:
        fallback = pricing(nowhere)
    assert (fallback.get("band") or {}).get("code") == LIST_BAND, \
        f"a region with no row must resolve to {LIST_BAND}: {fallback}"


def test_the_banner_appears_only_when_a_band_other_than_list_applies(anon_discounted, anon_list_region):
    """The banner appears only when a band other than the list band applies. cov: C-CF-132, C-CF-133, C-CF-134, C-UF-11, C-UF-31, C-DC-26"""

    discounted = pricing(anon_discounted)
    assert discounted.get("banner") is True, \
        f"a banded request must carry the banner: {discounted}"
    plain = pricing(anon_list_region)
    assert plain.get("banner") is False, \
        f"a list-band request must carry no banner: {plain}"
    served = raw_get("/plus", headers={REGION_HEADER: DISCOUNT_REGION})
    assert served.status_code == 200, f"/plus must be served: {describe(served)}"
    assert DISCOUNT_REASON in served.text, \
        f"the banner must carry the reason {DISCOUNT_REASON!r} when a band applies"
    assert "149" in served.text, "the banner must carry the banded price"
    assert "249" in served.text, "the banner must carry the struck list price in the same currency"
    without = raw_get("/plus", headers={REGION_HEADER: LIST_REGION})
    assert DISCOUNT_REASON not in without.text, \
        "no banner may appear when the list band applies"


def test_a_purchase_creates_one_billing_account_under_the_licence_key(fresh_member):
    """A purchase creates one billing account under the licence key. cov: C-RL-03, C-RL-19, C-CF-138, C-CF-141, C-CF-142, C-UF-33, C-TR-16, C-TR-22, C-TR-23, C-TR-25, C-DM-52, C-DM-68, C-DM-70, C-CN-02, C-DC-38"""

    probe = fresh_member.probe
    before = billing_keys()
    outcome = buy(fresh_member, probe["display_name"], probe["email"])
    expected_key = LICENCE_PREFIX + probe["handle"]
    assert outcome.get("licence_key") == expected_key, \
        f"the licence key must be {expected_key}: {outcome}"
    account = wait_until(lambda: billing_account(expected_key), lambda row: row is not None)
    assert account, f"a billing account must exist under the external key {expected_key}"
    assert str(account.get("name") or "") == probe["display_name"], \
        f"the billing account must carry the buyer's display name: {account}"
    assert str(account.get("email") or "").lower() == probe["email"].lower(), \
        f"the billing account must carry the buyer's address: {account}"
    assert str(account.get("currency") or "").upper() == CURRENCY, \
        f"the billing account currency must be {CURRENCY}: {account}"
    assert str(account.get("country") or "").upper() == COUNTRY, \
        f"the billing account country must be {COUNTRY}: {account}"
    after = billing_keys()
    assert after - before == {expected_key}, \
        f"a purchase must add exactly one billing account, found {sorted(after - before)}"
    for key in BOOTSTRAP_BILLING_KEYS:
        assert key in after, f"the bootstrap account {key} must be left untouched"


def test_a_repeated_purchase_is_refused_by_the_billing_key_conflict(fresh_member):
    """A repeated purchase is refused by the billing key conflict. cov: C-CF-144, C-CF-145, C-UF-34, C-TR-24, C-DM-69, C-CN-03, C-DC-27"""

    probe = fresh_member.probe
    first = buy(fresh_member, probe["display_name"], probe["email"])
    key = first.get("licence_key")
    assert key, f"the first purchase must name its licence key: {first}"
    wait_until(lambda: billing_account(key), lambda row: row is not None)
    before = billing_keys()
    again = purchase(fresh_member, probe["display_name"], probe["email"])
    refused(again, "a second purchase for a licence key already taken")
    assert key in message(again), \
        f"the refusal must name the licence key already taken: {describe(again)}"
    assert "409" in describe(again) or "conflict" in message(again).lower() \
        or "already" in message(again).lower(), \
        f"the refusal must read as the key conflict rather than a generic error: {describe(again)}"
    assert billing_keys() == before, \
        "a refused repeat must leave exactly one billing account for the key"
    assert sum(1 for row in capabilities.make_payments().accounts()
               if str(row.get("externalKey") or "") == key) == 1, \
        f"exactly one billing account may carry the external key {key}"


def test_the_order_records_the_band_the_banner_showed(fresh_member):
    """The order records the band the banner showed. cov: C-CF-135, C-CF-139, C-CF-140, C-CF-152, C-DM-54, C-DM-56, C-DM-67, C-CN-04"""

    probe = fresh_member.probe
    with client_for(fresh_member.headers["Authorization"].split()[1],
                    region=DISCOUNT_REGION) as banded:
        shown = pricing(banded)
        outcome = buy(banded, probe["display_name"], probe["email"])
    order = outcome.get("order") or {}
    assert order.get("price_band_code") == DISCOUNT_BAND, \
        f"the order must record the band {DISCOUNT_BAND}: {order}"
    assert order.get("discount_reason") == DISCOUNT_REASON, \
        f"the order must record the reason {DISCOUNT_REASON!r}: {order}"
    assert order.get("total_amount_minor") == BAND_MINOR, \
        f"the order total must be the banded {BAND_MINOR} the banner showed: {order}"
    assert order.get("currency") == CURRENCY, f"the order currency must be {CURRENCY}: {order}"
    assert (shown.get("band") or {}).get("amount_minor") == order.get("total_amount_minor"), \
        f"the banner {shown.get('band')} and the order {order} must agree on the amount"


def test_one_idempotency_key_returns_the_first_purchase_outcome(fresh_member):
    """One idempotency key returns the first purchase outcome. cov: C-CF-148, C-CF-149, C-TR-39, C-TR-40, C-DM-65"""

    probe = fresh_member.probe
    key = f"probe-{token_hex(16)}"
    first = purchase(fresh_member, probe["display_name"], probe["email"], key=key)
    outcome = ok(first, "the first purchase")
    licence = outcome.get("licence_key")
    wait_until(lambda: billing_account(licence), lambda row: row is not None)
    before = billing_keys()
    second = purchase(fresh_member, probe["display_name"], probe["email"], key=key)
    assert second.status_code in OK, \
        f"a repeat carrying the same idempotency key must return the first outcome: {describe(second)}"
    assert body(second).get("licence_key") == licence, \
        f"the repeat must return the first licence key {licence}: {body(second)}"
    assert billing_keys() == before, "the repeat must write nothing"


def test_the_receipt_mail_reaches_the_buyer_inbox_and_nobody_else(fresh_member, inbox):
    """The receipt mail reaches the buyer inbox and nobody else. cov: C-CF-143, C-CF-150, C-CF-151, C-TR-17, C-DC-39"""

    probe = fresh_member.probe
    outcome = buy(fresh_member, probe["display_name"], probe["email"])
    licence = outcome.get("licence_key")
    subject = RECEIPT_SUBJECT_PREFIX + licence
    found = wait_until(lambda: inbox.find(probe["email"], RECEIPT_SUBJECT_PREFIX),
                       lambda m: m is not None)
    assert found, f"one receipt must reach {probe['email']} with the subject {subject!r}"
    assert found.subject.startswith(RECEIPT_SUBJECT_PREFIX), \
        f"the receipt subject must begin {RECEIPT_SUBJECT_PREFIX!r}: {found.subject!r}"
    assert licence in found.subject, \
        f"the receipt subject must name the licence {licence}: {found.subject!r}"
    assert len(found.to) == 1, f"the receipt must carry one recipient alone: {found.to}"
    assert probe["email"].lower() in found.to[0].lower(), \
        f"the receipt must reach the buyer: {found.to}"
    assert inbox.count(probe["email"]) == 1, \
        f"exactly one receipt may reach {probe['email']}, found {inbox.count(probe['email'])}"
    for other in (MEMBER_EMAIL, MEMBER2_EMAIL, MEMBER3_EMAIL):
        assert inbox.find(other, RECEIPT_SUBJECT_PREFIX + licence) is None, \
            f"the receipt for {licence} must not reach {other}"


def test_a_refused_purchase_sends_no_mail_at_all(fresh_member, inbox, member2):
    """A refused purchase sends no mail at all. cov: C-CF-146, C-CF-153"""

    probe = fresh_member.probe
    outcome = buy(fresh_member, probe["display_name"], probe["email"])
    wait_until(lambda: inbox.find(probe["email"], RECEIPT_SUBJECT_PREFIX),
               lambda m: m is not None)
    before = inbox.count(probe["email"])
    again = purchase(fresh_member, probe["display_name"], probe["email"])
    refused(again, "a second purchase for a licence key already taken")
    settle(2.0)
    assert inbox.count(probe["email"]) == before, \
        f"a refused purchase must send no mail: {before} became {inbox.count(probe['email'])}"
    assert outcome.get("licence_key") in message(again), \
        f"the refusal must name the licence key already taken: {describe(again)}"


def test_money_is_stored_and_returned_as_integer_minor_units(anon, fresh_member):
    """Money is stored and returned as integer minor units. cov: C-CF-123, C-CF-124, C-CF-125, C-CF-156, C-CF-157, C-TR-50, C-TR-51, C-DM-55, C-DC-41"""

    shown = pricing(anon)
    for field in ("list_amount_minor",):
        value = shown.get(field)
        assert isinstance(value, int), f"{field} must be an integer, found {value!r}"
    assert shown.get("list_amount_minor") == LIST_MINOR, \
        f"the list price must be {LIST_MINOR}: {shown}"
    band = shown.get("band") or {}
    assert isinstance(band.get("amount_minor"), int), \
        f"the band amount must be an integer, found {band.get('amount_minor')!r}"
    probe = fresh_member.probe
    order = (buy(fresh_member, probe["display_name"], probe["email"]).get("order") or {})
    for field in ("list_amount_minor", "discount_amount_minor", "total_amount_minor"):
        value = order.get(field)
        assert isinstance(value, int), f"the order {field} must be an integer, found {value!r}"
    assert order.get("list_amount_minor") == LIST_MINOR, f"the order must record {LIST_MINOR}: {order}"
    assert (order.get("list_amount_minor") - order.get("discount_amount_minor")
            == order.get("total_amount_minor")), \
        f"the order total must be the list amount less the discount: {order}"
    assert order.get("currency") == CURRENCY, f"the order must carry {CURRENCY}: {order}"


def test_a_paid_source_is_absent_from_every_response_without_the_licence(anon, member2, member):
    """A paid source is absent from every response without the licence. cov: C-OV-05, C-CF-162, C-CF-163, C-CF-165, C-CF-166, C-CF-167, C-CF-174, C-CF-175, C-TR-09, C-DM-18, C-CN-11, C-DC-21"""

    entitled = example_files(member, PAID_EXAMPLE)
    assert entitled, f"the licence holder must receive the files of {PAID_EXAMPLE}"
    sources = [row.get("source") for row in entitled if row.get("source")]
    assert sources, f"the licence holder must receive real source: {entitled}"
    for session, who in ((anon, "a visitor with no session"),
                         (member2, "a member holding no licence")):
        detail = example_of(session, PAID_EXAMPLE)
        assert detail.status_code in OK, \
            f"{who} must still reach the example page: {describe(detail)}"
        payload = detail.json()
        assert payload.get("locked") is True, f"{who} must be told the example is locked: {payload}"
        assert "files" not in payload or not payload.get("files"), \
            f"{who} must receive no files key carrying rows: {payload}"
        rendered = _serialised(payload)
        for source in sources:
            assert source not in rendered, \
                f"{who} must not receive the paid source in the response body"
        listing = _serialised(gallery(session, access="paid"))
        for source in sources:
            assert source not in listing, f"{who} must not receive the paid source in the listing"
        document = html_of(f"/examples/{PAID_EXAMPLE}")
        for source in sources:
            assert source not in document.text, \
                f"{who} must not receive the paid source hidden in the markup"


def test_a_paid_raw_file_address_refuses_a_reader_holding_no_licence(anon, member2, member):
    """A paid raw file address refuses a reader holding no licence. cov: C-RL-05, C-CF-164, C-UF-30, C-DC-22, C-DC-42"""

    entitled = example_files(member, PAID_EXAMPLE)
    paths = [row.get("path") for row in entitled if row.get("path")]
    assert paths, f"the licence holder must receive file paths for {PAID_EXAMPLE}"
    served = raw_file(member, PAID_EXAMPLE, paths[0])
    assert served.status_code in OK, \
        f"the licence holder must read the raw file: {describe(served)}"
    held = served.text
    assert held.strip(), f"the raw file must carry real source: {describe(served)}"
    for session, who in ((anon, "a visitor with no session"),
                         (member2, "a member holding no licence")):
        refusal = raw_file(session, PAID_EXAMPLE, paths[0])
        denied(refusal, f"the raw paid file read by {who}")
        assert held not in refusal.text, f"{who} must not receive the paid source at the file address"
    free_paths = [row.get("path") for row in example_files(anon, FREE_EXAMPLE)]
    assert free_paths, f"a free example's paths must be readable: {FREE_EXAMPLE}"
    open_file = raw_file(anon, FREE_EXAMPLE, free_paths[0])
    assert open_file.status_code in OK, \
        f"a free example's raw file must stay open: {describe(open_file)}"


def test_a_revoked_licence_stops_unlocking_on_the_next_request(fresh_member, backend):
    """A revoked licence stops unlocking on the next request. cov: C-RL-18, C-CF-169, C-CF-170, C-TR-32, C-TR-33, C-DM-51, C-DM-53, C-DC-16, C-DC-37"""

    probe = fresh_member.probe
    key = buy(fresh_member, probe["display_name"], probe["email"]).get("licence_key")
    live = ok(fresh_member.get("/me"), "the buyer")
    assert live.get("entitled") is True, f"the buyer must be entitled: {live}"
    detail = ok(example_of(fresh_member, PAID_EXAMPLE), "the paid example for the buyer")
    assert detail.get("files"), f"the buyer must read the paid files: {detail}"
    revoke_licence(backend, key)
    after = ok(fresh_member.get("/me"), "the buyer after revocation")
    assert after.get("entitled") is False, f"a revoked licence must stop entitling on the next request: {after}"
    locked = ok(example_of(fresh_member, PAID_EXAMPLE), "the paid example after revocation")
    assert locked.get("locked") is True, f"the paid example must lock again: {locked}"
    assert not locked.get("files"), f"the paid source must be absent after revocation: {locked}"


def test_an_unresolvable_entitlement_refuses_and_reads_apart_from_unbought(member2, backend, fresh_member):
    """An unresolvable entitlement refuses and reads apart from unbought. cov: C-OV-06, C-CF-171, C-CF-172, C-UF-47, C-TR-12, C-TR-34, C-DC-40"""

    unbought = example_of(member2, PAID_EXAMPLE)
    assert unbought.status_code in OK, f"the never-bought example must still be served: {describe(unbought)}"
    offer = _serialised(body(unbought)).lower()
    assert body(unbought).get("locked") is True, f"the never-bought example must lock: {body(unbought)}"
    probe = fresh_member.probe
    key = buy(fresh_member, probe["display_name"], probe["email"]).get("licence_key")
    table = licence_table(backend)
    assert table, "the brief pins a `licences` table the verifier can read"
    backend.query(f"UPDATE {table} SET entitlements = NULL WHERE external_key = %s", (key,))
    unresolved = example_of(fresh_member, PAID_EXAMPLE)
    payload = body(unresolved) if isinstance(body(unresolved), dict) else {}
    assert not payload.get("files"), \
        f"an unresolvable entitlement must refuse rather than serve the paid files: {describe(unresolved)}"
    rendered = (_serialised(payload) + " " + unresolved.text).lower()
    assert "could not be confirmed" in rendered, \
        f"an unresolvable entitlement must say the licence could not be confirmed: {describe(unresolved)}"
    assert "could not be confirmed" not in offer, \
        "the never-bought answer must read apart from a failed resolution"


def test_a_saved_row_survives_a_reload_and_matches_the_grid(member, unsave_after, backend):
    """A saved row survives a reload and matches the grid. cov: C-CF-180, C-CF-182, C-UF-36, C-TR-28, C-DC-30"""

    before = set(saved_of(member))
    assert PAID_EXAMPLE not in before, f"{PAID_EXAMPLE} must not be saved at seed: {before}"
    written = save(member, PAID_EXAMPLE)
    assert written.status_code in OK, f"a save must be accepted: {describe(written)}"
    unsave_after.append(PAID_EXAMPLE)
    listed = gallery_items(member)
    assert listed[PAID_EXAMPLE].get("saved") is True, \
        f"the grid must show the card as saved after a reload: {listed[PAID_EXAMPLE]}"
    again = saved_of(member)
    assert PAID_EXAMPLE in again, f"the saved listing must survive a reload: {again}"
    panel = rows(member.get("/saved"), "the saved panel")
    shown = {row.get("slug") or row.get("example_slug"): row for row in panel}
    title, category, tier, runtimes, published = EXAMPLES[PAID_EXAMPLE]
    row = shown.get(PAID_EXAMPLE)
    assert row, f"the saved panel must carry {PAID_EXAMPLE}: {shown}"
    assert row.get("title", title) == title, f"the saved row must be the row the grid showed: {row}"
    member_id = who(ok(member.get("/me"), "the member")).get("id")
    stored = [r for r in backend.rows("saved_items") if str(r.get("account_id")) == str(member_id)]
    assert len(stored) == len(again), \
        f"the saved panel must reflect the stored rows: {len(stored)} stored, {len(again)} shown"


def test_saving_the_same_example_twice_leaves_one_stored_row(member, unsave_after, backend):
    """Saving the same example twice leaves one stored row. cov: C-RL-04, C-CF-177, C-CF-178, C-CF-179, C-TR-36, C-DM-57, C-DM-59, C-DC-29"""

    slug = PAID_EXAMPLE
    first = save(member, slug)
    assert first.status_code in OK, f"the first save must be accepted: {describe(first)}"
    unsave_after.append(slug)
    second = save(member, slug)
    assert second.status_code in OK, f"saving twice must not be an error: {describe(second)}"
    listed = [s for s in saved_of(member) if s == slug]
    assert len(listed) == 1, f"one row must remain after two saves, found {len(listed)}"
    member_id = who(ok(member.get("/me"), "the member")).get("id")
    matching = [r for r in backend.rows("saved_items") if str(r.get("account_id")) == str(member_id)]
    examples = [str(r.get("example_id")) for r in matching]
    assert len(examples) == len(set(examples)), \
        f"the stored saved rows must be unique per member and example: {matching}"
    removed = unsave(member, slug)
    assert removed.status_code in OK, f"unsave must be accepted: {describe(removed)}"
    assert slug not in saved_of(member), "the stored row must be gone after unsave"


def test_a_save_begun_signed_out_completes_after_signing_in(member2, page):
    """A save begun signed out completes after signing in. cov: C-CF-186, C-CF-187, C-UF-21, C-UF-37, C-DM-60, C-DM-66"""

    slug = FREE_EXAMPLES[0]
    assert slug not in set(saved_of(member2)), f"{slug} must not be saved for the second member"
    denied(httpx.post(f"{api_base()}/saved", json={"example_slug": slug}, timeout=TIMEOUT),
           "a save carrying no session")
    page.goto(f"{base_url()}/login?next=/examples&save={slug}")
    page.wait_for_load_state("networkidle")
    page.get_by_label(re.compile(r"^\s*email\s*$", re.I)).fill(MEMBER2_EMAIL)
    page.get_by_label(re.compile(r"^\s*password\s*$", re.I)).fill(PASSWORD)
    page.get_by_role("button", name=re.compile("sign in|log in|login", re.I)).click()
    page.wait_for_url(lambda url: "/login" not in url, timeout=20000)
    assert "/examples" in page.url, f"signing in must return to the page the save was pressed on: {page.url}"
    saved = wait_until(lambda: saved_of(member2), lambda rows_now: slug in rows_now)
    assert slug in saved, f"the carried save must be written on arrival without a second press: {saved}"
    member2.delete(f"/saved/{slug}")


def test_the_saved_count_is_read_from_the_stored_saved_rows(anon, member, unsave_after):
    """The saved count is read from the stored saved rows. cov: C-CF-188, C-CF-189, C-DM-16, C-DM-58"""

    listed = gallery_items(anon)
    for slug in SAVED_AT_SEED:
        assert listed[slug].get("save_count") >= 1, \
            f"{slug} is saved at seed and must count at least one: {listed[slug]}"
    slug = PAID_EXAMPLE
    was = listed[slug].get("save_count") or 0
    save(member, slug)
    unsave_after.append(slug)
    after = gallery_items(anon)[slug].get("save_count")
    assert after == was + 1, \
        f"the saved count for {slug} must rise from the stored rows: {was} became {after}"
    ordered = gallery(anon, sort="most-saved").get("items") or []
    counts = [row.get("save_count") for row in ordered]
    assert counts == sorted(counts, reverse=True), \
        f"the most-saved ordering must read the same stored count: {counts}"
    unsave(member, slug)
    back = gallery_items(anon)[slug].get("save_count")
    assert back == was, f"removing the row must lower the count again: {back}"


def test_another_member_cannot_read_the_saved_rows(member, member2):
    """Another member cannot read the saved rows. cov: C-RL-01, C-RL-06, C-RL-09, C-CF-190, C-CF-191, C-CF-192, C-UF-23, C-TR-31, C-DC-28"""

    mine = set(saved_of(member))
    assert set(SAVED_AT_SEED) <= mine, f"the seeded member must hold the seeded saves: {mine}"
    theirs = set(saved_of(member2))
    assert not (set(SAVED_AT_SEED) & theirs), \
        f"another member's saved listing must not carry the seeded member's rows: {theirs}"
    profile = ok(profile_of(member2, MEMBER_HANDLE), f"the public profile of {MEMBER_HANDLE}")
    rendered = _serialised(profile)
    for slug in SAVED_AT_SEED:
        assert slug not in rendered, f"the public profile must not reveal the saved example {slug}"
    document = html_of(f"/@{MEMBER_HANDLE}")
    assert document.status_code == 200, f"the profile must be served: {describe(document)}"
    assert PUBLISHED_PROJECT in document.text, \
        f"the public profile must carry the published project {PUBLISHED_PROJECT}"


def test_a_submitted_project_is_absent_from_every_public_response(member2, anon, member):
    """A submitted project is absent from every public response. cov: C-OV-09, C-RL-07, C-CF-201, C-CF-202, C-CF-203, C-CF-204, C-CF-207, C-UF-38, C-FE-76, C-DM-61, C-DM-63, C-DM-64, C-CN-07, C-DC-33"""

    created = submit_project(member2, title=f"Probe Project {token_hex(6)}")
    assert created.get("state") == "submitted", f"a new project must start submitted: {created}"
    project_id = created.get("id")
    owner_view = member2.get(f"/showcase/{project_id}")
    assert owner_view.status_code in OK, f"the owner must read their submitted project: {describe(owner_view)}"
    public = projects_of(anon, MEMBER2_HANDLE)
    assert all(row.get("id") != project_id for row in public), \
        f"a submitted project must be absent from the public profile: {public}"
    assert all(str(row.get("state", "published")) == "published" for row in public), \
        f"only published rows may reach a public response: {public}"
    assert created.get("title") not in html_of(f"/@{MEMBER2_HANDLE}").text, \
        "a submitted project must be absent from the rendered public profile"
    assert created.get("title") not in html_of("/").text, \
        "a submitted project must be absent from the homepage showcase tape"
    denied(member.get(f"/showcase/{project_id}"), "another member reading a submitted project by its own address")
    denied(anon.get(f"/showcase/{project_id}"), "a visitor reading a submitted project by its own address")
    titles = {row.get("title") for row in projects_of(anon, MEMBER_HANDLE)}
    assert PUBLISHED_PROJECT in titles, f"the published project must be public: {titles}"
    assert SUBMITTED_PROJECT not in titles, f"the submitted project {SUBMITTED_PROJECT} must stay absent: {titles}"


def test_a_member_cannot_publish_their_own_submitted_project(member):
    """A member cannot publish their own submitted project. cov: C-RL-08, C-RL-10, C-CF-205, C-DM-62, C-DC-32"""

    created = submit_project(member, title=f"Probe Project {token_hex(6)}")
    project_id = created.get("id")
    for attempt in (
            lambda: member.post(f"/showcase/{project_id}/publish", json={}),
            lambda: member.patch(f"/showcase/{project_id}", json={"state": "published"}),
            lambda: member.put(f"/showcase/{project_id}", json={"state": "published"})):
        response = attempt()
        assert response.status_code in (401, 403, 404, 405, 409, 422), \
            f"a member must not publish their own submitted project: {describe(response)}"
    still = ok(member.get(f"/showcase/{project_id}"), "the owner's submitted project")
    assert still.get("state") == "submitted", f"the refused project must stay submitted: {still}"
    public = projects_of(anon, MEMBER_HANDLE)
    assert all(row.get("id") != project_id for row in public), \
        f"the refused project must stay absent from the public profile: {public}"


def test_a_folded_handle_reaches_one_profile_and_an_unknown_one_not_found(anon):
    """A folded handle reaches one profile and an unknown one is not found. cov: C-CF-198, C-CF-208, C-CF-209, C-CF-210, C-CF-225, C-UF-12, C-UF-22, C-TR-29, C-DM-47, C-DM-48, C-DM-49, C-DC-31"""

    for handle in (MEMBER_HANDLE, MEMBER_HANDLE.upper(), MEMBER_HANDLE.capitalize()):
        found = profile_of(anon, handle)
        assert found.status_code in OK, f"the handle {handle} must reach the profile: {describe(found)}"
        assert who(found.json()).get("handle") == MEMBER_HANDLE, \
            f"every case of {MEMBER_HANDLE} must reach one profile: {found.json()}"
    profile = ok(profile_of(anon, MEMBER_HANDLE), "the profile")
    assert str(profile.get("joined_at", "")).startswith(JOINED[MEMBER_EMAIL]), \
        f"the profile must carry the joined date {JOINED[MEMBER_EMAIL]}: {profile}"
    assert "links" in profile, f"the profile must carry the member's links: {profile}"
    unknown = profile_of(anon, f"nobody{token_hex(6)}")
    assert unknown.status_code == 404, f"an unknown handle must answer as not found: {describe(unknown)}"
    document = raw_get(f"/@nobody{token_hex(6)}")
    assert document.status_code == 404, f"an unknown profile address must answer as not found: {describe(document)}"
    missing = article_of(anon, ABSENT_ARTICLE)
    assert missing.status_code == 404, f"an unknown article slug must answer as not found: {describe(missing)}"


def test_both_dated_feeds_are_ordered_newest_first(anon):
    """Both dated feeds are ordered newest first. cov: C-CF-214, C-CF-215, C-UF-14, C-TR-52, C-DC-36"""

    entries = changelog_of(anon)
    assert len(entries) == len(CHANGELOG), \
        f"{len(CHANGELOG)} changelog entries must be seeded, found {len(entries)}"
    dates = [str(row.get("published_at"))[:10] for row in entries]
    assert dates == sorted(dates, reverse=True), \
        f"the changelog must be ordered newest first: {dates}"
    articles = magazine_of(anon)
    assert len(articles) == len(ARTICLES), \
        f"{len(ARTICLES)} articles must be seeded, found {len(articles)}"
    dates = [str(row.get("published_at"))[:10] for row in articles]
    assert dates == sorted(dates, reverse=True), \
        f"the magazine must be ordered newest first: {dates}"
    for route in ("/changelog", "/magazine"):
        document = html_of(route)
        assert document.status_code == 200, f"{route} must be served: {describe(document)}"
        assert "newest" in document.text.lower(), \
            f"{route} must state that the feed is ordered newest first"


def test_a_changelog_entry_names_its_release_and_its_kind(anon):
    """A changelog entry names its release and its kind. cov: C-CF-103, C-CF-216, C-CF-217, C-CF-218, C-CF-219, C-CF-220, C-DM-39, C-DC-34"""

    entries = {row.get("slug"): row for row in changelog_of(anon)}
    for slug, (version, kind, title, published) in CHANGELOG.items():
        row = entries.get(slug)
        assert row, f"the changelog entry {slug} must be seeded: {sorted(entries)}"
        assert row.get("version") == version, f"{slug} must name {version}: {row}"
        assert row.get("kind") == kind, f"{slug} must be of the kind {kind}: {row}"
        assert row.get("title") == title, f"{slug} must be titled {title!r}: {row}"
        assert str(row.get("published_at"))[:10] == published, f"{slug}: {row}"
    document = html_of("/changelog")
    assert CURRENT in document.text, f"the changelog must name the release {CURRENT}"
    assert UI_VERSION in document.text, \
        f"the section library entry must carry its own numeral {UI_VERSION}"
    ui_entry = entries["ui-registry-install"]
    assert ui_entry.get("version") == UI_VERSION, \
        f"the section library entry must belong to {UI_VERSION}: {ui_entry}"


def test_an_article_carries_its_author_handle_and_published_date(anon):
    """An article carries its author handle and published date. cov: C-CF-223, C-CF-224, C-UF-15, C-DM-40, C-DM-41, C-DM-42, C-DM-43, C-DC-35"""

    listed = {row.get("slug"): row for row in magazine_of(anon)}
    for slug, (title, author, published) in ARTICLES.items():
        row = listed.get(slug)
        assert row, f"the article {slug} must be seeded: {sorted(listed)}"
        assert row.get("title") == title, f"{slug} must be titled {title!r}: {row}"
        assert row.get("author_handle") == author, f"{slug} must name the author {author}: {row}"
        assert str(row.get("published_at"))[:10] == published, f"{slug}: {row}"
        assert row.get("standfirst"), f"{slug} must carry a standfirst: {row}"
        detail = ok(article_of(anon, slug), f"the article {slug}")
        assert detail.get("author_handle") == author, f"{slug} detail: {detail}"
        assert str(detail.get("published_at"))[:10] == published, f"{slug} detail: {detail}"
        document = html_of(f"/magazine/{slug}")
        assert document.status_code == 200, f"/magazine/{slug} must be served: {describe(document)}"
        assert published in document.text, f"/magazine/{slug} must show its published date"


def test_seeded_content_rows_are_stored_once_per_generation(backend):
    """The seeded content rows are stored once per generation. cov: C-RL-17, C-TR-15, C-TR-57, C-TR-61, C-TR-67, C-DM-01, C-CN-01, C-CN-12, C-CN-17, C-DC-43"""

    for table, expected in (("releases", len(RELEASES)), ("categories", len(CATEGORIES)),
                            ("examples", len(EXAMPLES)), ("sections", len(SECTIONS)),
                            ("theme_values", len(THEME_KEYS)),
                            ("changelog_entries", len(CHANGELOG)),
                            ("articles", len(ARTICLES)), ("price_bands", 2)):
        stored = backend.count(table)
        assert stored == expected, \
            f"{table} must hold {expected} seeded rows, found {stored}"
    for slug in EXAMPLES:
        assert backend.count("examples", slug=slug) == 1, \
            f"the example {slug} must be stored once"
    for path, name, blurb in CATEGORIES:
        row = backend.one("categories", path=path)
        assert row and row.get("blurb") == blurb, \
            f"the category {path} must carry its seeded blurb: {row}"
    generations = {row.get("generation") for row in backend.rows("examples")}
    assert len(generations) == 1, \
        f"the seeded examples must belong to one published generation: {generations}"
    pages = backend.count("doc_pages")
    assert pages == len(DOC_PAGES) * len(RELEASES), \
        f"{len(DOC_PAGES)} pages per release across {len(RELEASES)} releases, found {pages}"


def test_no_foreign_key_crosses_from_application_rows_to_content_rows(backend):
    """No foreign key crosses from an application row to a content row. cov: C-TR-58, C-TR-59, C-DM-44, C-CN-05"""

    constraints = backend.query("""
        SELECT tc.table_name AS child, ccu.table_name AS parent
        FROM information_schema.table_constraints tc
        JOIN information_schema.constraint_column_usage ccu
          ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
          AND tc.table_schema = 'public'
    """)
    content = {"releases", "categories", "examples", "example_files", "sections",
               "theme_values", "doc_pages", "doc_code_blocks", "changelog_entries",
               "articles", "price_bands"}
    application = {"accounts", "sessions", "licences", "orders", "saved_items",
                   "pending_saves", "showcase_projects", "idempotency_records"}
    crossing = [row for row in constraints
                if row["child"] in application and row["parent"] in content]
    assert not crossing, (
        "no foreign key may cross from application data into content data, because "
        f"content rows are replaced wholesale on every release: {crossing}")
    stored = backend.rows("saved_items")
    for row in stored:
        assert row.get("generation") is not None, \
            f"a saved row must record the generation it was read at: {row}"
    orders = backend.rows("orders")
    for row in orders:
        assert row.get("price_band_code"), \
            f"an order must record the band it was sold under: {row}"
