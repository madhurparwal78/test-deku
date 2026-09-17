"""Outcome graders for the Studio AVX portfolio task.

One module, every section and both declared slots. Black-box: HTTP against the
running app, the rendered page through Playwright, PostgreSQL through the shared
backend adapter and Mailpit through the shared inbox adapter. Nothing here reads
the agent's source.
"""

from __future__ import annotations

import json
import os
import re

import httpx

from conftest import (
    ALL_LABEL, CONSENT_COOKIE, DECOY_FIELD, DETAIL_SLUG, DISCIPLINES,
    ENQUIRY_LIMIT, EYEBROWS, FACET_COUNTS, FEATURED, FOOTER_TAGLINE,
    HOME_TITLE_EN, LOCALES, MEDIA_PER_PROJECT, NAV, NOT_FOUND_ROUTES, OK,
    PASSWORD, PRIVACY_CONTROLLER, PRIVACY_SECTIONS, PRIVACY_TITLE, PROJECTS,
    PUBLIC_ROUTES, REFERENCE_RE, SEEDED_ENQUIRIES, SERVICES, SLUGS, STATEMENT,
    STUDIO2_EMAIL, STUDIO2_NAME, STUDIO_ADDRESS, STUDIO_EMAIL, STUDIO_NAME,
    STUDIO_ROLE, STUDIO_TITLE_IT, SUBJECT_PREFIX, TIMEOUT, anon, api_base,
    backend, base_url, body, browser, client_for, contrast_ratio, denied,
    describe, enquiry_count, enquiry_payload, facets_of, inbox, login,
    mail_subjects, message, narrow_page, ok, page, parse_colour, project_of,
    projects_of, raw_get, refused, rows, send_enquiry, settle, studio,
    token_for, token_hex, wait_until,
)


def _serialised(payload) -> str:
    return json.dumps(payload, default=str)


def _visible_text(page) -> str:
    return page.evaluate("() => document.body ? document.body.innerText : ''")


def test_health_returns_200_and_the_shell_shares_the_api_origin():
    """Health answers 200 and the shell shares the read surface's origin. cov: C-TR-01, C-TR-07, C-TR-15, C-CN-05, C-DC-01"""

    response = httpx.get(f"{api_base()}/health", timeout=TIMEOUT)
    assert response.status_code == 200, f"health must return 200 once ready: {describe(response)}"
    shell = raw_get("/works")
    assert shell.status_code == 200, f"the application shell must be served at /works: {describe(shell)}"
    assert "text/html" in shell.headers.get("content-type", ""), f"/works must serve a document: {describe(shell)}"
    api = httpx.get(f"{api_base()}/projects", params={"locale": "en"}, timeout=TIMEOUT)
    assert api.status_code == 200 and "json" in api.headers.get("content-type", ""), \
        f"the read surface must answer JSON on the same origin: {describe(api)}"


def test_app_root_keeps_reserved_screenshot_and_download_directories():
    """The app root keeps the two reserved directories. cov: C-DC-02"""

    for name in (".browser_screenshots", ".downloads"):
        assert os.path.isdir(f"/app/{name}"), f"the reserved directory /app/{name} must exist at the app root"


def test_root_redirects_to_the_home_in_the_preferred_language():
    """The root redirects to the home in the preferred language. cov: C-CF-75, C-UF-01, C-TR-02"""

    cases = (({"Accept-Language": "en-GB,en;q=0.9"}, "/en"),
             ({"Accept-Language": "it-IT,it;q=0.9"}, "/it"),
             ({"Accept-Language": "fr-FR,fr;q=0.9"}, "/it"),
             ({}, "/it"))
    for headers, target in cases:
        response = raw_get("/", headers=headers)
        assert 300 <= response.status_code < 400, f"/ must redirect for {headers}: {describe(response)}"
        location = response.headers.get("location", "")
        assert location.rstrip("/").endswith(target), \
            f"/ with {headers} must redirect to {target}, found {location!r}"


def test_works_and_studio_slash_forms_redirect_permanently():
    """The trailing-slash forms of Works and Studio redirect permanently. cov: C-CF-22, C-CF-39, C-UF-11, C-TR-03"""

    for bare in ("/works", "/studio"):
        response = raw_get(bare + "/")
        assert response.status_code in (301, 308), \
            f"{bare}/ must answer with a permanent redirect: {describe(response)}"
        location = response.headers.get("location", "")
        assert location.rstrip("/").endswith(bare), f"{bare}/ must redirect to {bare}, found {location!r}"
        assert raw_get(bare).status_code == 200, f"{bare} must be served"


def test_an_unknown_address_answers_with_the_not_found_status():
    """An address that is not a route answers with the not-found status. cov: C-CF-86, C-UF-09, C-TR-04"""

    for route in NOT_FOUND_ROUTES:
        response = raw_get(route)
        assert response.status_code == 404, f"{route} must answer with the not-found status: {describe(response)}"
        assert "text/html" in response.headers.get("content-type", ""), \
            f"{route} must still serve the page: {describe(response)}"


def test_every_public_route_declares_its_own_title_and_description(page):
    """Every public route declares its own title and description. cov: C-CF-80, C-CF-81"""

    titles, descriptions = {}, {}
    for route in ("/studio", "/it", "/works", "/contact", "/privacy", "/en"):
        page.goto(f"{base_url()}{route}")
        page.wait_for_load_state("networkidle")
        title = page.title().strip()
        description = (page.evaluate(
            "() => { const m = document.querySelector('meta[name=description]'); return m ? m.content : ''; }") or "").strip()
        assert title, f"{route} must declare a document title"
        assert description, f"{route} must declare a meta description"
        titles[route], descriptions[route] = title, description
    for holder, label in ((titles, "title"), (descriptions, "description")):
        seen = {}
        for route, value in holder.items():
            assert value not in seen, f"{route} and {seen[value]} share one {label}: {value!r}"
            seen[value] = route
    assert titles["/en"] == HOME_TITLE_EN, f"the English home must be titled {HOME_TITLE_EN!r}, found {titles['/en']!r}"
    assert titles["/studio"] == STUDIO_TITLE_IT, \
        f"the studio page in the default Italian must be titled {STUDIO_TITLE_IT!r}, found {titles['/studio']!r}"


def test_no_stored_credential_reaches_anything_the_browser_downloads():
    """No stored credential reaches anything the browser downloads. cov: C-TR-16"""

    secrets = []
    held = re.search(r"://[^:]+:([^@]+)@", os.environ.get("DB_ADMIN_URL", ""))
    if held:
        secrets.append(held.group(1))
    assert secrets, "the verifier must know the database password to look for it"
    downloads = []
    for route in PUBLIC_ROUTES:
        document = raw_get(route, follow_redirects=True)
        downloads.append((route, document.text))
        for match in re.findall(r'(?:src|href)=["\']([^"\']+\.(?:js|css|json))["\']', document.text):
            if match.startswith("http") and base_url() not in match:
                continue
            asset = raw_get(match if match.startswith("/") else f"/{match}")
            if asset.status_code == 200:
                downloads.append((match, asset.text))
    downloads.append(("/api/projects", raw_get("/api/projects?locale=en").text))
    for where, text in downloads:
        for value in secrets:
            assert value not in text, f"{where} carries a stored credential in what the browser downloads"


def test_body_text_meets_the_contrast_bar_against_its_background(page):
    """Body text meets the contrast bar against its background. cov: C-UX-21"""

    page.goto(f"{base_url()}/studio")
    page.wait_for_load_state("networkidle")
    page.mouse.wheel(0, 1600)
    page.wait_for_timeout(1500)
    sampled = page.evaluate("""() => {
        const out = [];
        for (const node of document.querySelectorAll('p, li, span, h2, h3')) {
            if (!node.textContent || node.textContent.trim().length < 24 || node.children.length) continue;
            const style = getComputedStyle(node);
            if (style.visibility === 'hidden' || parseFloat(style.opacity) < 0.5) continue;
            let ground = null, walker = node;
            while (walker) {
                const back = getComputedStyle(walker).backgroundColor;
                if (back && back !== 'rgba(0, 0, 0, 0)' && back !== 'transparent') { ground = back; break; }
                walker = walker.parentElement;
            }
            if (!ground) continue;
            out.push({ink: style.color, ground: ground, size: parseFloat(style.fontSize)});
            if (out.length >= 24) break;
        }
        return out;
    }""")
    assert sampled, "the studio page must render body text the contrast pass can sample"
    for row in sampled:
        need = 3.0 if row["size"] >= 24 else 4.5
        ratio = contrast_ratio(parse_colour(row["ink"]), parse_colour(row["ground"]))
        assert ratio >= need, f"text at {row['size']}px must meet {need}:1, found {ratio:.2f} for {row['ink']} on {row['ground']}"


def test_a_narrow_viewport_shows_no_sideways_overflow(narrow_page):
    """A narrow viewport shows no sideways overflow. cov: C-CF-91"""

    for route in PUBLIC_ROUTES:
        narrow_page.goto(f"{base_url()}{route}")
        narrow_page.wait_for_load_state("networkidle")
        widths = narrow_page.evaluate("() => [document.documentElement.scrollWidth, window.innerWidth]")
        assert widths[0] <= widths[1] + 1, \
            f"{route} overflows sideways at 390px: document {widths[0]}px in {widths[1]}px"


def test_every_internal_link_leads_to_a_route_that_answers_success(page):
    """Every internal link leads to a route that answers success. cov: C-RL-01, C-CF-93, C-UF-10"""

    hrefs = set()
    for route in ("/en", "/works", "/studio", "/contact", "/privacy", f"/works/{DETAIL_SLUG}"):
        page.goto(f"{base_url()}{route}")
        page.wait_for_load_state("networkidle")
        found = page.evaluate("() => Array.from(document.querySelectorAll('a[href]')).map(a => a.href)")
        for href in found:
            if href.startswith(base_url()):
                hrefs.add(href[len(base_url()):].split("#")[0] or "/")
    assert hrefs, "the public routes must carry internal links"
    for href in sorted(hrefs):
        response = raw_get(href, follow_redirects=True)
        assert response.status_code == 200, f"the internal link {href} must answer with success: {describe(response)}"


def test_every_project_image_carries_alternative_text_naming_the_project(anon, page):
    """Every project image carries alternative text naming the project. cov: C-CF-90, C-FE-17, C-DM-14"""

    for row in projects_of(anon, locale="en"):
        assert row.get("title") and row["title"] in str(row.get("cover_alt") or ""), \
            f"the cover of {row.get('slug')} must carry alternative text naming the project: {row}"
    detail = ok(project_of(anon, DETAIL_SLUG), "the project detail")
    media = detail.get("media") or []
    assert len(media) == MEDIA_PER_PROJECT, f"{DETAIL_SLUG} must carry {MEDIA_PER_PROJECT} gallery images: {media}"
    for item in media:
        assert detail["title"] in str(item.get("alt") or ""), f"a gallery image must name the project: {item}"
    page.goto(f"{base_url()}/works")
    page.wait_for_load_state("networkidle")
    missing = page.evaluate("() => Array.from(document.querySelectorAll('img')).filter(i => !(i.getAttribute('alt') || '').trim()).length")
    assert missing == 0, f"every image on /works must carry alternative text, {missing} carry none"


def test_seeded_studio_accounts_are_stored_once_with_hashed_passwords(backend):
    """The two seeded studio accounts are stored once, hashed, and listed in the credentials file. cov: C-RL-10, C-RL-11, C-RL-12, C-CF-06, C-TR-11, C-DM-01, C-DM-02, C-CN-02, C-DC-03"""

    for email, name in ((STUDIO_EMAIL, STUDIO_NAME), (STUDIO2_EMAIL, STUDIO2_NAME)):
        assert backend.count("users", email=email) == 1, f"seeded account {email} must exist exactly once"
        stored = backend.rows("users", limit=1, email=email)[0]
        assert stored.get("name") == name and stored.get("role") == STUDIO_ROLE, f"seeded account {email}: {stored}"
        held = str(stored.get("password_hash") or "")
        assert held and PASSWORD not in held, f"the password of {email} must be stored hashed"
        signed = login(email)
        assert signed.status_code in OK and signed.json().get("token"), f"{email} must sign in: {describe(signed)}"
    with open("/app/USER_README.md", encoding="utf-8") as readme:
        text = readme.read()
    for email in (STUDIO_EMAIL, STUDIO2_EMAIL):
        assert email in text, f"{email} is missing from /app/USER_README.md"
    assert PASSWORD in text, "the seeded password must be written to /app/USER_README.md"


def test_login_refuses_a_wrong_password_and_an_unknown_email_alike():
    """A wrong password and an unknown email are refused alike. cov: C-CF-01, C-CF-02"""

    wrong = login(STUDIO_EMAIL, "not-the-password")
    refused(wrong, "a wrong password")
    unknown = login(f"nobody-{token_hex()}@example.com")
    refused(unknown, "an unknown email")
    assert "Sign in failed" in message(wrong), f"a wrong password must be refused with `Sign in failed`: {describe(wrong)}"
    assert message(wrong) == message(unknown), \
        f"an unknown email and a wrong password must share one message: {message(wrong)!r} vs {message(unknown)!r}"


def test_missing_unknown_and_retired_tokens_are_refused(anon):
    """A missing, unknown or retired token is refused. cov: C-CF-03, C-CF-05, C-DM-03"""

    denied(anon.get("/me"), "/api/me with no token")
    denied(anon.get("/enquiries"), "the enquiry list with no token")
    with client_for(f"not-a-real-token-{token_hex(24)}") as stranger:
        denied(stranger.get("/enquiries"), "the enquiry list with an unknown token")
    token = token_for(STUDIO2_EMAIL)
    with client_for(token) as session:
        assert session.get("/me").status_code in OK, "a fresh token must work"
        out = session.post("/auth/logout", json={})
        assert out.status_code in OK, f"logout must succeed: {describe(out)}"
        denied(session.get("/enquiries"), "the enquiry list with a retired token")


def test_twenty_seeded_projects_are_stored_once_in_catalogue_order(backend):
    """The twenty seeded projects are stored once in catalogue order. cov: C-OV-03, C-TR-05, C-TR-08, C-DM-06, C-DM-07, C-DM-08, C-CN-01"""

    assert backend.count("projects") == len(PROJECTS), f"{len(PROJECTS)} projects must be stored"
    stored = backend.query("SELECT slug, title, year, client, featured FROM projects ORDER BY position")
    assert [row["slug"] for row in stored] == list(SLUGS), f"projects must be stored in catalogue order: {[r['slug'] for r in stored]}"
    for row, (slug, title, disciplines, year, client, featured) in zip(stored, PROJECTS):
        assert (row["title"], int(row["year"]), row["client"], bool(row["featured"])) == (title, year, client, featured), \
            f"{slug} must be stored as seeded: {row}"
    pairs = backend.query("SELECT p.slug, d.discipline_key FROM project_disciplines d JOIN projects p ON p.id = d.project_id ORDER BY p.position, d.position")
    expected = [(slug, key) for slug, _, keys, _, _, _ in PROJECTS for key in keys]
    assert [(r["slug"], r["discipline_key"]) for r in pairs] == expected, "the stored disciplines must match the seed in order"


def test_the_project_list_serves_catalogue_order_with_localised_labels(anon):
    """The project list serves catalogue order with localised labels. cov: C-CF-79, C-DM-05, C-DM-12, C-DC-06"""

    for locale in LOCALES:
        listed = projects_of(anon, locale=locale)
        assert [row.get("slug") for row in listed] == list(SLUGS), f"the {locale} list must keep catalogue order"
        labels = {key: (en, it) for key, en, it in DISCIPLINES}
        for row, (slug, title, keys, year, client, featured) in zip(listed, PROJECTS):
            assert row.get("title") == title and row.get("client") == client and int(row.get("year")) == year, f"{slug}: {row}"
            assert list(row.get("disciplines") or []) == list(keys), f"{slug} disciplines must be {keys}: {row}"
            want = [labels[k][0 if locale == "en" else 1] for k in keys]
            assert list(row.get("discipline_labels") or []) == want, f"{slug} labels in {locale} must be {want}: {row}"


def test_facet_counts_are_computed_from_stored_disciplines(anon, backend):
    """Facet counts are computed from the stored disciplines. cov: C-CF-26, C-CF-27, C-CF-28, C-CF-29, C-TR-10, C-DM-04, C-DM-13, C-DC-08, C-DC-16"""

    for locale in LOCALES:
        facets = facets_of(anon, locale)
        assert [f.get("key") for f in facets] == ["all"] + [k for k, _, _ in DISCIPLINES], f"facet order in {locale}: {facets}"
        assert facets[0].get("label") == ALL_LABEL[locale], f"the all facet must read {ALL_LABEL[locale]}: {facets[0]}"
        for facet in facets:
            assert facet.get("count") == FACET_COUNTS[facet["key"]], f"{facet['key']} must count {FACET_COUNTS[facet['key']]}: {facet}"
    backend.query("INSERT INTO project_disciplines (project_id, discipline_key, position) "
                  "SELECT id, 'packaging', 9 FROM projects WHERE slug = 'amts-card'")
    try:
        counted = {f["key"]: f["count"] for f in facets_of(anon, "en")}
        assert counted["packaging"] == FACET_COUNTS["packaging"] + 1, \
            f"a count must follow the stored disciplines rather than a stored number: {counted}"
        assert counted["all"] == FACET_COUNTS["all"], f"all must stay the project count: {counted}"
    finally:
        backend.query("DELETE FROM project_disciplines WHERE discipline_key = 'packaging' "
                      "AND project_id = (SELECT id FROM projects WHERE slug = 'amts-card')")


def test_a_discipline_facet_narrows_the_catalogue_in_order(anon):
    """A discipline facet narrows the catalogue in order. cov: C-CF-30, C-UF-03"""

    for key, _, _ in DISCIPLINES:
        expected = [slug for slug, _, keys, _, _, _ in PROJECTS if key in keys]
        narrowed = [row.get("slug") for row in projects_of(anon, locale="en", discipline=key)]
        assert narrowed == expected, f"discipline={key} must narrow to {expected}, found {narrowed}"


def test_an_unknown_discipline_or_locale_is_refused(anon):
    """An unknown discipline or locale is refused. cov: C-CF-78"""

    refused(anon.get("/projects", params={"locale": "en", "discipline": "sculpture"}), "an unknown discipline")
    refused(anon.get("/projects", params={"locale": "fr"}), "an unknown locale on the project list")
    refused(anon.get("/facets", params={"locale": "de"}), "an unknown locale on the facets")
    default = projects_of(anon)
    assert [row.get("slug") for row in default] == list(SLUGS), "the project list must default to Italian and serve every project"


def test_a_project_page_carries_its_metadata_and_wraps_previous_and_next(anon):
    """A project page carries its metadata and wraps previous and next. cov: C-CF-33, C-CF-34, C-DM-11, C-DC-07"""

    detail = ok(project_of(anon, DETAIL_SLUG, "en"), "the project detail in English")
    slug, title, keys, year, client, featured = PROJECTS[SLUGS.index(DETAIL_SLUG)]
    assert (detail.get("title"), int(detail.get("year")), detail.get("client")) == (title, year, client), f"{slug}: {detail}"
    assert list(detail.get("disciplines") or []) == list(keys), f"{slug} disciplines: {detail}"
    assert detail.get("summary") and detail.get("cover_large"), f"{slug} must carry a summary and a large cover: {detail}"
    italian = ok(project_of(anon, DETAIL_SLUG, "it"), "the project detail in Italian")
    assert italian.get("summary") and italian["summary"] != detail["summary"], "the summary must follow the locale"
    index = SLUGS.index(DETAIL_SLUG)
    assert (detail.get("previous") or {}).get("slug") == SLUGS[index - 1], f"previous of {slug}: {detail.get('previous')}"
    assert (detail.get("next") or {}).get("slug") == SLUGS[index + 1], f"next of {slug}: {detail.get('next')}"
    first = ok(project_of(anon, SLUGS[0]), "the first project")
    last = ok(project_of(anon, SLUGS[-1]), "the last project")
    assert (first.get("previous") or {}).get("slug") == SLUGS[-1], "previous must wrap from the first to the last"
    assert (last.get("next") or {}).get("slug") == SLUGS[0], "next must wrap from the last to the first"


def test_an_unknown_project_slug_answers_not_found(anon):
    """An unknown project slug answers not found. cov: C-CF-36, C-UF-04"""

    missing = project_of(anon, f"no-such-project-{token_hex(4)}")
    assert missing.status_code == 404, f"an unknown slug must answer as not found: {describe(missing)}"


def test_the_footer_counts_featured_and_total_projects_from_stored_rows(anon, backend):
    """The footer counts featured and total projects from the stored rows. cov: C-CF-19, C-TR-09, C-DM-09, C-DM-10"""

    footer = ok(anon.get("/global", params={"locale": "en"}), "the global content").get("footer") or {}
    assert footer.get("tagline") == FOOTER_TAGLINE, f"the footer tagline must read {FOOTER_TAGLINE!r}: {footer}"
    assert (footer.get("featured"), footer.get("total")) == (FEATURED, len(PROJECTS)), f"the footer must count {FEATURED} / {len(PROJECTS)}: {footer}"
    backend.query("UPDATE projects SET featured = true WHERE slug = 'marea-hotel'")
    try:
        again = ok(anon.get("/global", params={"locale": "en"}), "the global content").get("footer") or {}
        assert again.get("featured") == FEATURED + 1, f"the featured count must follow the stored rows: {again}"
    finally:
        backend.query("UPDATE projects SET featured = false WHERE slug = 'marea-hotel'")


def test_the_studio_content_serves_eyebrows_statement_and_six_services(anon):
    """The studio content serves eyebrows, the statement and six services. cov: C-CF-40, C-CF-41, C-CF-42, C-CF-43, C-UF-05, C-DM-15, C-DC-09"""

    intros = {}
    for locale in LOCALES:
        studio_content = ok(anon.get("/studio", params={"locale": locale}), f"the studio content in {locale}")
        assert list(studio_content.get("eyebrows") or []) == list(EYEBROWS), f"eyebrows in {locale}: {studio_content.get('eyebrows')}"
        assert studio_content.get("statement") == STATEMENT, f"the statement in {locale}: {studio_content.get('statement')}"
        services = studio_content.get("services") or []
        assert [s.get("label") for s in services] == list(SERVICES[locale]), f"services in {locale}: {services}"
        assert all(s.get("body") for s in services), f"every service needs a paragraph in {locale}"
        intros[locale] = studio_content.get("intro")
    assert intros["it"] and intros["en"] and intros["it"] != intros["en"], "the intro must follow the locale"


def test_navigation_labels_follow_the_requested_locale(anon):
    """Navigation labels follow the requested locale. cov: C-OV-10, C-CF-77, C-DC-10"""

    for locale in LOCALES:
        nav = ok(anon.get("/global", params={"locale": locale}), f"global {locale}").get("nav") or {}
        assert (nav.get("works"), nav.get("studio"), nav.get("contact")) == NAV[locale], f"nav in {locale}: {nav}"


def test_an_accepted_enquiry_is_stored_exactly_as_submitted(anon, studio, backend):
    """An accepted enquiry is stored exactly as submitted. cov: C-OV-05, C-RL-02, C-CF-55, C-CF-67, C-DM-16, C-DC-11, C-DC-14"""

    before = enquiry_count(backend)
    payload = enquiry_payload(message="Ciao! We'd like a new identity – budget in Q3.\nCan we talk on Monday?")
    response = anon.post("/enquiries", json=payload)
    assert response.status_code in OK, f"a valid enquiry must be accepted: {describe(response)}"
    reference = response.json().get("reference")
    assert reference and REFERENCE_RE.match(reference), f"the answer must carry a reference: {response.json()}"
    assert response.json().get("created_at"), "the answer must carry created_at"
    assert enquiry_count(backend) == before + 1, "exactly one enquiry row must be stored"
    stored = backend.rows("enquiries", limit=1, reference=reference)[0]
    for field in ("name", "email", "message", "locale"):
        assert stored.get(field) == payload[field], f"the stored {field} must match the submission: {stored.get(field)!r}"
    assert stored.get("status") == "new", f"a new enquiry must start as new: {stored}"
    shown = ok(studio.get(f"/enquiries/{reference}"), "the studio reading the enquiry")
    for field in ("name", "email", "message"):
        assert shown.get(field) == payload[field], f"the inbox must show the submitted {field}: {shown.get(field)!r}"


def test_an_enquiry_notification_mail_reaches_the_studio_inbox_alone(anon, inbox):
    """An enquiry notification mail reaches the studio inbox alone. cov: C-OV-06, C-CF-47, C-CF-60, C-CF-61, C-TR-06, C-DC-15"""

    payload = enquiry_payload()
    response = anon.post("/enquiries", json=payload)
    assert response.status_code in OK, f"a valid enquiry must be accepted: {describe(response)}"
    subject = SUBJECT_PREFIX + payload["name"]
    found = wait_until(lambda: inbox.find(STUDIO_ADDRESS, subject), lambda m: m is not None)
    assert found, f"a notification with the subject {subject!r} must reach {STUDIO_ADDRESS}"
    assert found.subject == subject, f"the subject must be {subject!r}, found {found.subject!r}"
    assert len(found.to) == 1 and STUDIO_ADDRESS in found.to[0].lower(), f"the notification must go to the studio alone: {found.to}"
    assert sum(1 for s in mail_subjects(inbox, STUDIO_ADDRESS) if s == subject) == 1, "exactly one notification per enquiry"
    assert inbox.count(payload["email"]) == 0, "nothing may be mailed to the visitor"


def test_an_invalid_enquiry_is_refused_with_field_keyed_errors_and_nothing_stored(anon, backend, inbox):
    """An invalid enquiry is refused with field-keyed errors and nothing is stored. cov: C-CF-49, C-CF-50, C-CF-51, C-TR-17"""

    before = enquiry_count(backend)
    cases = (("name", {"name": "A"}), ("email", {"email": "not-an-address"}), ("message", {"message": "short"}))
    for field, broken in cases:
        payload = enquiry_payload(**broken)
        response = anon.post("/enquiries", json=payload)
        refused(response, f"an enquiry with an invalid {field}")
        errors = body(response).get("errors") if isinstance(body(response), dict) else None
        assert isinstance(errors, dict) and field in errors, f"the refusal must key its error by {field}: {describe(response)}"
        settle(1.0)
        assert inbox.find(STUDIO_ADDRESS, SUBJECT_PREFIX + payload["name"]) is None, f"an invalid {field} must send no mail"
    assert enquiry_count(backend) == before, "an invalid enquiry must store nothing"


def test_a_filled_decoy_field_is_refused_and_nothing_is_stored_or_mailed(anon, backend, inbox):
    """A filled decoy field is refused and nothing is stored or mailed. cov: C-OV-07, C-CF-54, C-TR-13"""

    before = enquiry_count(backend)
    payload = enquiry_payload(**{DECOY_FIELD: "https://spam.example.com"})
    refused(anon.post("/enquiries", json=payload), "an enquiry whose decoy field is filled")
    settle(1.5)
    assert enquiry_count(backend) == before, "a filled decoy field must store nothing"
    assert inbox.find(STUDIO_ADDRESS, SUBJECT_PREFIX + payload["name"]) is None, "a filled decoy field must send no mail"


def test_no_response_sets_a_cookie_before_a_consent_choice(anon):
    """No response sets a cookie before a consent choice. cov: C-OV-09, C-CF-64, C-CF-82, C-TR-14, C-CN-04"""

    checked = []
    for route in PUBLIC_ROUTES + ("/",):
        checked.append((route, raw_get(route)))
    for path in ("/projects?locale=en", "/facets?locale=it", "/studio?locale=en", "/global?locale=en"):
        checked.append((path, anon.get(path)))
    checked.append(("/enquiries", send_enquiry(anon)))
    for where, response in checked:
        assert "set-cookie" not in {name.lower() for name in response.headers}, \
            f"{where} must set no cookie before a consent choice: {response.headers.get('set-cookie')!r}"


def test_a_visitor_cannot_list_or_read_any_stored_enquiry(anon, studio):
    """A visitor cannot list or read any stored enquiry. cov: C-OV-08, C-RL-03, C-RL-08, C-CF-71"""

    listed = anon.get("/enquiries")
    denied(listed, "the enquiry list for a visitor")
    single = anon.get("/enquiries/ENQ-0001")
    denied(single, "a stored enquiry by reference for a visitor")
    change = anon.patch("/enquiries/ENQ-0001", json={"status": "archived"})
    denied(change, "a status change by a visitor")
    for response in (listed, single, change):
        text = response.text.lower()
        for _, name, email, _, _ in SEEDED_ENQUIRIES:
            assert name.lower() not in text and email not in text, f"a visitor must receive no enquiry content: {describe(response)}"
    still = ok(studio.get("/enquiries/ENQ-0001"), "the seeded enquiry for the studio")
    assert still.get("status") == "new", f"a refused visitor change must leave the status unchanged: {still}"


def test_the_studio_lists_every_stored_enquiry_newest_first(studio):
    """The studio lists every stored enquiry newest first. cov: C-RL-05, C-RL-13, C-CF-66, C-DM-18, C-DC-04"""

    listed = rows(studio.get("/enquiries"), "the enquiry list")
    stamps = [str(row.get("created_at")) for row in listed]
    assert stamps == sorted(stamps, reverse=True), f"the enquiries must be newest first: {stamps}"
    by_reference = {row.get("reference"): row for row in listed}
    for reference, name, email, locale, status in SEEDED_ENQUIRIES:
        row = by_reference.get(reference)
        assert row, f"{reference} must be listed"
        assert (row.get("name"), row.get("email"), row.get("locale")) == (name, email, locale), f"{reference}: {row}"
    assert by_reference["ENQ-0002"].get("status") == "replied" and by_reference["ENQ-0003"].get("status") == "archived", \
        "the seeded statuses must be served"


def test_a_status_change_is_stored_and_survives_a_reload(anon, studio, backend):
    """A status change is stored and survives a reload. cov: C-RL-06, C-CF-68, C-DC-13"""

    created = anon.post("/enquiries", json=enquiry_payload())
    assert created.status_code in OK, f"a valid enquiry must be accepted: {describe(created)}"
    reference = created.json()["reference"]
    changed = studio.patch(f"/enquiries/{reference}", json={"status": "replied"})
    assert changed.status_code in OK and changed.json().get("status") == "replied", f"the status change must be accepted: {describe(changed)}"
    with client_for(token_for(STUDIO2_EMAIL)) as reloaded:
        again = ok(reloaded.get(f"/enquiries/{reference}"), "the enquiry after a reload")
        assert again.get("status") == "replied", f"the saved status must survive a reload: {again}"
        listed = {row.get("reference"): row for row in rows(reloaded.get("/enquiries"), "the list")}
        assert listed[reference].get("status") == "replied", "the table must show the saved status"
    stored = backend.rows("enquiries", limit=1, reference=reference)[0]
    assert stored.get("status") == "replied", f"the stored row must carry the new status: {stored}"


def test_an_unknown_status_is_refused_and_the_stored_status_is_unchanged(studio):
    """An unknown status is refused and the stored status is unchanged. cov: C-RL-09, C-CF-69, C-DM-17"""

    refused(studio.patch("/enquiries/ENQ-0002", json={"status": "spam"}), "an unknown status")
    assert ok(studio.get("/enquiries/ENQ-0002"), "ENQ-0002").get("status") == "replied", "the stored status must be unchanged"


def test_a_stored_enquiry_cannot_be_deleted(studio, backend):
    """A stored enquiry cannot be deleted. cov: C-RL-07, C-CF-70, C-CN-03"""

    response = studio.delete("/enquiries/ENQ-0003")
    assert 400 <= response.status_code < 500, f"deleting an enquiry must be refused: {describe(response)}"
    assert backend.count("enquiries", reference="ENQ-0003") == 1, "the enquiry row must remain"


def test_an_unknown_enquiry_reference_answers_not_found(studio):
    """An unknown enquiry reference answers not found. cov: C-CF-72, C-DC-12"""

    missing = studio.get("/enquiries/ENQ-9999")
    assert missing.status_code == 404, f"an unknown reference must answer as not found: {describe(missing)}"


def test_enquiry_references_are_sequential_and_well_formed(anon):
    """Enquiry references are sequential and well formed. cov: C-CF-56"""

    first = anon.post("/enquiries", json=enquiry_payload())
    second = anon.post("/enquiries", json=enquiry_payload())
    assert first.status_code in OK and second.status_code in OK, f"both enquiries must be accepted: {describe(first)} {describe(second)}"
    one, two = first.json()["reference"], second.json()["reference"]
    assert REFERENCE_RE.match(one) and REFERENCE_RE.match(two), f"references must read ENQ- and four digits: {one}, {two}"
    assert int(two[4:]) == int(one[4:]) + 1, f"references must be sequential: {one} then {two}"
    assert int(one[4:]) > 3, f"new references must follow the seeded ENQ-0003: {one}"


def test_the_home_draws_a_live_three_dimensional_canvas(page):
    """The home draws a live three dimensional canvas. cov: C-CF-09, C-CF-17, C-FE-20"""

    page.goto(f"{base_url()}/en")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(4000)
    supported = page.evaluate("() => !!document.createElement('canvas').getContext('webgl')")
    if supported:
        live = page.evaluate("""() => Array.from(document.querySelectorAll('canvas')).some(c => {
            const r = c.getBoundingClientRect();
            return r.width >= window.innerWidth * 0.8 && r.height >= window.innerHeight * 0.8 &&
                   !!(c.getContext('webgl2') || c.getContext('webgl'));
        })""")
        assert live, "the home must draw a viewport-filling canvas with a live WebGL context"
    else:
        links = page.evaluate("() => new Set(Array.from(document.querySelectorAll('a[href*=\"/works/\"]')).map(a => a.getAttribute('href'))).size")
        assert links >= len(SLUGS), f"without WebGL the home must fall back to the flat catalogue, found {links} project links"


def test_without_webgl_the_home_shows_the_flat_catalogue(browser):
    """Without WebGL the home shows the flat catalogue. cov: C-OV-04, C-CF-20, C-FE-19"""

    plain = browser.browser_type.launch(args=["--disable-webgl", "--disable-webgl2", "--disable-3d-apis"])
    try:
        context = plain.new_context(viewport={"width": 1440, "height": 900})
        tab = context.new_page()
        tab.goto(f"{base_url()}/en")
        tab.wait_for_load_state("networkidle")
        tab.wait_for_timeout(3000)
        hrefs = tab.evaluate("() => Array.from(document.querySelectorAll('a[href]')).map(a => a.getAttribute('href'))")
        reached = {slug for slug in SLUGS if any(h and h.rstrip('/').endswith('/works/' + slug) for h in hrefs)}
        assert reached == set(SLUGS), f"without WebGL the home must reach every project, missing {sorted(set(SLUGS) - reached)}"
        context.close()
    finally:
        plain.close()


def test_the_privacy_page_carries_the_controller_and_seven_sections(page):
    """The privacy page carries the controller and seven sections. cov: C-CF-94, C-CF-95, C-UF-07"""

    page.goto(f"{base_url()}/privacy")
    page.wait_for_load_state("networkidle")
    text = _visible_text(page)
    for expected in (PRIVACY_TITLE, "Note legali", "Ultimo aggiornamento: 15 giugno 2026", PRIVACY_CONTROLLER,
                     STUDIO_ADDRESS, CONSENT_COOKIE) + PRIVACY_SECTIONS:
        assert expected in text, f"/privacy must carry {expected!r}"


def test_the_inbox_sends_a_visitor_without_a_session_to_sign_in(page):
    """The inbox sends a visitor without a session to sign in. cov: C-RL-04, C-CF-07, C-UF-12, C-CN-06"""

    page.goto(f"{base_url()}/inbox")
    page.wait_for_url(lambda url: "/login" in url, timeout=20000)
    assert "/login" in page.url, f"a visitor opening /inbox must be sent to /login, found {page.url}"
    assert "Anna Rizzo" not in _visible_text(page), "no enquiry content may render for a visitor"


def test_a_consent_choice_writes_cc_cookie_and_the_banner_stays_away(browser):
    """A consent choice writes cc_cookie and the banner stays away. cov: C-CF-84"""

    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        tab = context.new_page()
        tab.goto(f"{base_url()}/en")
        tab.wait_for_load_state("networkidle")
        assert not context.cookies(), f"no cookie may exist before a choice: {context.cookies()}"
        accept = tab.get_by_role("button", name=re.compile(r"^\s*(accept|accetta)\s*$", re.I))
        accept.first.click()
        tab.wait_for_timeout(800)
        names = {c["name"] for c in context.cookies()}
        assert CONSENT_COOKIE in names, f"a consent choice must write {CONSENT_COOKIE}: {names}"
        tab.reload()
        tab.wait_for_load_state("networkidle")
        assert tab.get_by_role("button", name=re.compile(r"^\s*(accept|accetta)\s*$", re.I)).count() == 0 or \
            not tab.get_by_role("button", name=re.compile(r"^\s*(accept|accetta)\s*$", re.I)).first.is_visible(), \
            "the consent banner must not return after a choice"
    finally:
        context.close()


def test_logout_retires_the_token():
    """Logout retires the token. cov: C-CF-04, C-DC-05"""

    token = token_for(STUDIO_EMAIL)
    with client_for(token) as session:
        assert session.get("/me").status_code in OK, "a fresh token must reach /api/me"
        assert session.post("/auth/logout", json={}).status_code in OK, "logout must succeed"
        denied(session.get("/me"), "/api/me with a retired token")


def test_the_enquiry_limit_refuses_the_eleventh_and_stores_nothing(anon, backend, inbox):
    """The enquiry limit refuses the eleventh and stores nothing. cov: C-CF-62, C-CF-63, C-TR-12, C-DM-19"""

    refusal = None
    for _ in range(ENQUIRY_LIMIT + 1):
        payload = enquiry_payload()
        before = enquiry_count(backend)
        response = anon.post("/enquiries", json=payload)
        if response.status_code in OK:
            continue
        refusal = (payload, response, before)
        break
    assert refusal, f"an address may have at most {ENQUIRY_LIMIT} enquiries accepted per hour; {ENQUIRY_LIMIT + 1} were accepted"
    payload, response, before = refusal
    refused(response, "an enquiry past the limit")
    assert enquiry_count(backend) == before, "a limited enquiry must store nothing"
    settle(1.5)
    assert inbox.find(STUDIO_ADDRESS, SUBJECT_PREFIX + payload["name"]) is None, "a limited enquiry must send no mail"
    assert re.search(r"\d|retry|again|later|minute|hour", message(response), re.I), \
        f"the refusal must say when to try again: {describe(response)}"
