"""The one pytest module for Remixable Timeline Editor.

Every section (core features, data integrity, authorization, edge cases) and both declared
slots (backend, storage) are merged here. Fixtures, pinned literals and helpers live in
conftest.py; the shared grader (appclient, capabilities, _shapes) is on PYTHONPATH=/tests
from the deku-verifier-base image. The checklist obligations each function discharges live
in the pytest-provenance-v1 sidecar beside the bundle, not in a comment.

Channel disjointness, per reference/J: the browser pass works inside projects it remixes
itself and restores every seeded count it touches. Every check here either reads seeded
state no journey mutates, works inside a per-run probe workspace, or restores the seeded
state it borrowed before it returns.
"""

from __future__ import annotations

import hashlib
import os

import httpx

import appclient
import conftest as cf


def test_health_endpoint_answers_ok() -> None:
    """The app answers its health route with status ok once its services are reachable."""
    with cf.api() as client:
        response = client.get("/health")
    assert response.status_code == 200, cf.describe(response, "health must answer 200")
    assert cf.body_of(response).get("status") == "ok", cf.describe(
        response, "health must report status ok")


def test_app_answers_at_its_public_url_after_the_session() -> None:
    """The deployed app is reachable at its public origin from another container."""
    response = cf.fetch_document("/")
    assert response.status_code == 200, cf.describe(response, "the home route must render")
    assert appclient.app_url().startswith("http"), "APP_PUBLIC_URL must name the origin"


def test_public_routes_render_on_the_server() -> None:
    """Every public route answers with complete HTML that already carries its content."""
    for route in cf.PUBLIC_ROUTES:
        response = cf.fetch_document(route)
        assert response.status_code == 200, cf.describe(response, f"{route} must render")
        assert "<html" in response.text.lower(), f"{route} must be a complete document"
    home = cf.page_text(cf.fetch_document("/").text)
    assert cf.HERO_HEADING in home, "the hero heading must be in the served document"
    assert cf.STATEMENT in home, "the statement must reach the document as one string"


def test_public_routes_carry_their_pinned_titles() -> None:
    """Each named public route carries its exact document title."""
    for route, title in cf.TITLES.items():
        response = cf.fetch_document(route)
        assert cf.document_title(response.text) == title, (
            f"{route} must carry the title {title!r}, read "
            f"{cf.document_title(response.text)!r}")


def test_public_routes_have_distinct_descriptions() -> None:
    """No two public routes share a meta description or a title."""
    seen_titles, seen_desc = {}, {}
    for route in cf.PUBLIC_ROUTES:
        markup = cf.fetch_document(route).text
        title = cf.document_title(markup)
        desc = cf.meta_description(markup)
        assert title, f"{route} must carry a title"
        assert desc, f"{route} must carry a meta description"
        assert title not in seen_titles, f"{route} shares its title with {seen_titles.get(title)}"
        assert desc not in seen_desc, f"{route} shares its description with {seen_desc.get(desc)}"
        seen_titles[title] = route
        seen_desc[desc] = route


def test_documents_declare_a_favicon_that_resolves() -> None:
    """Every public document declares a favicon, and the declared favicon is an image."""
    hrefs = set()
    for route in cf.PUBLIC_ROUTES:
        href = cf.favicon_href(cf.fetch_document(route).text)
        assert href, f"{route} must declare a favicon in its head"
        hrefs.add(href)
    for href in hrefs:
        target = href if href.startswith("http") else appclient.app_url() + href
        response = httpx.get(target, timeout=appclient.TIMEOUT, follow_redirects=True)
        assert response.status_code == 200, cf.describe(response, "the favicon must resolve")
        assert response.headers.get("content-type", "").startswith("image/"), cf.describe(
            response, "the favicon must be served as an image")


def test_internal_links_on_public_routes_resolve() -> None:
    """Every same-origin link on a public route leads to a page that exists."""
    checked = set()
    for route in cf.PUBLIC_ROUTES:
        for link in cf.internal_links(cf.fetch_document(route).text):
            if link in checked or link.startswith("/api") or link.startswith("/s/"):
                continue
            checked.add(link)
            response = cf.fetch_document(link)
            assert response.status_code in (200, 401, 403) or response.url.path.startswith(
                "/login"), cf.describe(response, f"the link {link} on {route} must resolve")


def test_footer_links_the_legal_pages_on_every_public_route() -> None:
    """Every footer links privacy, cookie and terms pages that live on this origin."""
    for route in cf.PUBLIC_ROUTES:
        links = set(cf.internal_links(cf.fetch_document(route).text))
        for legal in cf.LEGAL_ROUTES:
            assert legal in links, f"the footer of {route} must link {legal}"
    for legal in cf.LEGAL_ROUTES:
        response = cf.fetch_document(legal)
        assert response.status_code == 200, cf.describe(response, f"{legal} must be a real page")


def test_privacy_page_states_what_is_kept() -> None:
    """The privacy page names what is kept about members, reviewers and visitors."""
    text = cf.page_text(cf.fetch_document("/privacy-policy").text).lower()
    for subject in ("member", "reviewer", "visitor", "consent", "contact"):
        assert subject in text, f"the privacy page must speak about {subject}"


def test_public_documents_load_nothing_from_other_origins() -> None:
    """No public document pulls a script, style, font or image from another origin."""
    for route in cf.PUBLIC_ROUTES:
        external = cf.external_sources(cf.fetch_document(route).text)
        assert not external, f"{route} loads from other origins: {external[:5]}"


def test_no_credential_appears_in_downloaded_markup() -> None:
    """No page the browser downloads carries a store or bucket credential."""
    secrets = [os.environ.get("STORAGE_SECRET_KEY", ""), "deku-local-dev"]
    for route in cf.PUBLIC_ROUTES:
        text = cf.fetch_document(route).text
        for secret in secrets:
            if secret:
                assert secret not in text, f"{route} leaks a credential"


def test_marketing_chrome_carries_its_pinned_copy() -> None:
    """The header, footer and bands carry the fixed labels and lines the site pins."""
    home = cf.page_text(cf.fetch_document("/").text)
    for label in cf.NAV_ITEMS + cf.FOOTER_COLUMNS + cf.SOCIAL_NETWORKS + cf.PILLARS:
        assert label in home, f"the home document must carry {label!r}"
    assert cf.COPYRIGHT in home, "the footer must carry the copyright line"
    for line in cf.THREE_WAYS_LINES + cf.PRODUCTION_LINES:
        assert line in home, f"the home document must carry {line!r}"
    assert cf.PRODUCTION_LINES[0] != cf.PRODUCTION_LINES[1]
    for creator in cf.CREATOR_NAMES:
        assert creator in home, f"the showcase must credit {creator}"
    pricing = cf.page_text(cf.fetch_document("/pricing").text)
    assert cf.TAGLINE in pricing, "inner routes must carry the tagline"


def test_social_links_point_at_one_account_each() -> None:
    """Each social network is linked to the same address everywhere it appears."""
    targets = {}
    for route in ("/", "/pricing", "/product"):
        markup = cf.fetch_document(route).text
        lower = markup.lower()
        cursor = 0
        while True:
            at = lower.find('href="http', cursor)
            if at < 0:
                break
            end = markup.find('"', at + 6)
            href = markup[at + 6:end]
            cursor = end + 1
            for network in ("instagram", "youtube", "linkedin", "pinterest"):
                if network in href.lower():
                    targets.setdefault(network, set()).add(href)
    for network, hrefs in targets.items():
        assert len(hrefs) == 1, f"{network} is linked to more than one address: {hrefs}"


def test_pricing_page_renders_its_heading_and_badge() -> None:
    """The pricing route opens with its heading and carries the computed toggle badge."""
    text = cf.page_text(cf.fetch_document("/pricing").text)
    for value in (cf.PRICING_HEADING, cf.SAVE_UP_TO, cf.MOST_POPULAR, cf.PRO_MEMBER_LINE):
        assert value in text, f"the pricing route must carry {value!r}"


def test_plans_are_stored_in_order_with_their_prices() -> None:
    """The plans list returns five plans in order with integer cent prices in usd."""
    with cf.api() as client:
        plans = cf.listing(client.get("/plans"))
    assert [p.get("key") for p in plans] == list(cf.PLAN_ORDER), plans
    for plan in plans:
        if plan["key"] in cf.PRICES:
            monthly, annual = cf.PRICES[plan["key"]]
            assert plan.get("monthly_price_cents") == monthly, plan
            assert plan.get("annual_monthly_price_cents") == annual, plan
            assert isinstance(plan.get("monthly_price_cents"), int), plan
    units = {p["key"]: str(p.get("unit", "")).lower() for p in plans}
    assert "member" in units[cf.PLAN_PRO] and "member" in units[cf.PLAN_BUSINESS], units
    caps = {p["key"]: p.get("member_cap") for p in plans}
    assert caps[cf.PLAN_PRO] == 10 and caps[cf.PLAN_FREE] == 1 and caps[cf.PLAN_BASIC] == 1, caps
    popular = [p["key"] for p in plans if p.get("most_popular")]
    assert popular == [cf.PLAN_PRO], popular


def test_annual_saving_percent_is_computed_from_prices() -> None:
    """Each paid plan's annual saving is derived from its two stored prices."""
    with cf.api() as client:
        plans = {p["key"]: p for p in cf.listing(client.get("/plans"))}
    for key, expected in cf.SAVINGS.items():
        monthly, annual = cf.PRICES[key]
        derived = int((1 - annual / monthly) * 100 + 0.5)
        assert derived == expected
        assert plans[key].get("annual_saving_percent") == expected, plans[key]


def test_plan_quotas_match_the_published_table() -> None:
    """Every plan stores one limit per meter, matching the published quota table."""
    expected = {
        cf.METER_STORAGE: {"free": 2 * cf.GIGABYTE, "basic": 5 * cf.GIGABYTE,
                           "pro": 20 * cf.GIGABYTE, "business": 50 * cf.GIGABYTE,
                           "enterprise": None},
        cf.METER_VARIATIONS: {"free": 0, "basic": 20, "pro": 250, "business": 2500,
                              "enterprise": 0},
        cf.METER_CAPTION: {"free": 30, "basic": 60, "pro": 120, "business": 600,
                           "enterprise": None},
        cf.METER_SPEECH: {"free": 0, "basic": 0, "pro": 5000, "business": 20000,
                          "enterprise": 0},
        cf.METER_KITS: {"free": 0, "basic": 0, "pro": 5, "business": 10, "enterprise": 0},
        cf.METER_BLOCKS: {"free": 5, "basic": 25, "pro": 50, "business": 100,
                          "enterprise": None},
        cf.METER_MEMBERS: {"free": 1, "basic": 1, "pro": 10, "business": None},
    }
    with cf.api() as client:
        plans = {p["key"]: p for p in cf.listing(client.get("/plans"))}
    for meter, limits in expected.items():
        for plan, limit in limits.items():
            quotas = plans[plan].get("quotas")
            rows = quotas if isinstance(quotas, list) else [
                {"meter": k, "limit": v} for k, v in (quotas or {}).items()]
            found = [q for q in rows if q.get("meter") == meter]
            assert len(found) == 1, f"{plan} must store one {meter} limit: {rows}"
            value = found[0].get("limit", found[0].get("limit_value"))
            assert value == limit, f"{plan} {meter} must be {limit}, read {value}"


def test_plan_features_carry_comparison_rows_and_statuses() -> None:
    """Plan features carry every comparison row, with coming soon rows marked as such."""
    with cf.api() as client:
        plans = cf.listing(client.get("/plans"))
    labels, statuses = set(), {}
    for plan in plans:
        for feature in plan.get("features") or []:
            labels.add(feature.get("label"))
            assert feature.get("status") in (cf.FEATURE_AVAILABLE, cf.FEATURE_COMING_SOON), feature
            statuses.setdefault(feature.get("label"), set()).add(feature.get("status"))
    for row in cf.COMPARISON_ROWS:
        assert row in labels, f"the comparison row {row!r} must be a stored feature"
    for row in cf.COMING_SOON_ROWS:
        assert statuses[row] == {cf.FEATURE_COMING_SOON}, f"{row} must be coming soon: {statuses[row]}"


def test_unknown_address_renders_the_not_found_page() -> None:
    """An unknown address answers not-found with the product's own page and ways back."""
    response = cf.fetch_document("/no-such-page-" + cf.unique_suffix())
    assert response.status_code == 404, cf.describe(response, "unknown pages must answer 404")
    assert cf.NOT_FOUND_HEADING in cf.page_text(response.text), "the heading must be shown"
    links = set(cf.internal_links(response.text))
    for route in ("/", "/templates", "/pricing"):
        assert route in links, f"the not-found page must link back to {route}"


def test_unknown_api_address_answers_json_not_found() -> None:
    """An unknown API address, graphql among them, answers a JSON not-found error."""
    with cf.api() as client:
        for path in ("/graphql", "/nothing-here-" + cf.unique_suffix()):
            response = client.get(path)
            assert response.status_code == 404, cf.describe(response, "must answer 404")
            assert response.headers.get("content-type", "").startswith("application/json")
            assert cf.body_of(response).get("error") == cf.NOT_FOUND_ERROR, response.text[:200]


def test_unknown_records_render_not_found() -> None:
    """An unknown template, creator, blog post or share token answers not-found."""
    for path in ("/templates/00000000-0000-4000-8000-000000000000",
                 "/creators/no-such-creator", "/blog/no-such-post", "/s/AAAAAAAAAAAAAAAA"):
        response = cf.fetch_document(path)
        assert response.status_code == 404, cf.describe(response, f"{path} must answer 404")
    with cf.api() as client:
        response = client.get("/templates/00000000-0000-4000-8000-000000000000")
    assert response.status_code == 404, cf.describe(response, "an unknown uuid must answer 404")


def test_signed_out_projects_redirects_to_login_with_next() -> None:
    """A signed-out request for a guarded route lands on login carrying the path."""
    for route in cf.GUARDED_ROUTES:
        response = cf.fetch_document(route, follow=False)
        assert response.status_code in (301, 302, 303, 307, 308), cf.describe(
            response, f"{route} must redirect when signed out")
        location = response.headers.get("location", "")
        assert "/login" in location and "next=" in location, f"{route} redirects to {location}"


def test_production_build_is_served() -> None:
    """The app serves a production build: no development client is exposed."""
    for path in ("/@vite/client", "/__astro_dev_toolbar__"):
        response = cf.fetch_document(path)
        assert response.status_code == 404, cf.describe(response, "no dev server may answer")


def test_blog_and_customers_are_seeded_content() -> None:
    """The blog, its chips and the approved customer list come from stored content."""
    with cf.api() as client:
        posts = cf.listing(client.get("/blog/posts"))
        tutorials = cf.listing(client.get("/blog/posts", params={"category": "Tutorials"}))
        customers = cf.listing(client.get("/customers"))
    assert {p.get("slug") for p in posts} >= set(cf.BLOG_SLUGS), posts
    assert {p.get("category") for p in posts} >= set(cf.BLOG_CATEGORIES), posts
    assert [p.get("category") for p in tutorials] == ["Tutorials"], tutorials
    for slug in cf.BLOG_SLUGS:
        assert cf.fetch_document("/blog/" + slug).status_code == 200, slug
    assert [c.get("name") for c in customers] == list(cf.CUSTOMERS), customers
    home = cf.page_text(cf.fetch_document("/").text)
    assert cf.WITHDRAWN_CUSTOMER not in home, "a withdrawn customer must never be shown"


def test_contact_request_is_stored_with_its_audience() -> None:
    """A contact request is stored with its audience and answers with an FC reference."""
    suffix = cf.unique_suffix()
    body = {"audience": cf.AUDIENCE_SALES, "full_name": "Probe " + suffix,
            "email": cf.probe_address(suffix), "company": "Probe Co",
            "message": "We would like to talk about a larger plan, reference " + suffix}
    with cf.api() as client:
        first = client.post("/contact", json=body)
        second = client.post("/contact", json=body)
    assert cf.accepted(first), cf.describe(first, "a contact request must store")
    reference = cf.body_of(first).get("reference", "")
    assert reference.startswith(cf.CONTACT_PREFIX) and reference[3:].isdigit(), reference
    assert len(reference) == 9, reference
    assert cf.body_of(second).get("reference") == reference, cf.describe(
        second, "a repeat within ten minutes must return the first reference")
    rows = cf.backend().rows(cf.TABLE_CONTACT, email=body["email"])
    assert len(rows) == 1, f"one contact row must be stored, found {len(rows)}"
    assert rows[0].get("audience") == cf.AUDIENCE_SALES, rows[0]


def test_invalid_contact_request_writes_nothing() -> None:
    """A contact message under twenty characters is refused, names the field, stores nothing."""
    suffix = cf.unique_suffix()
    body = {"audience": cf.AUDIENCE_SUPPORT, "full_name": "Probe", "company": "",
            "email": cf.probe_address(suffix), "message": "too short"}
    with cf.api() as client:
        response = client.post("/contact", json=body)
    assert cf.is_client_error(response), cf.describe(response, "a short message must be refused")
    assert "message" in response.text.lower(), cf.describe(response, "the field must be named")
    assert cf.backend().count(cf.TABLE_CONTACT, email=body["email"]) == 0


def test_contact_route_asks_for_the_audience_first() -> None:
    """The contact route opens by asking what the visitor needs help with."""
    text = cf.page_text(cf.fetch_document("/contact").text)
    assert cf.CONTACT_FIRST_QUESTION in text, "the contact route must ask its first question"
    assert "Free" in cf.page_text(cf.fetch_document("/register").text), "signup names Free"
    plugin = cf.fetch_document(cf.PLUGIN_ROUTE)
    assert plugin.status_code == 200 and "not available" in plugin.text.lower()


def test_consent_is_stored_per_category_with_wording() -> None:
    """A consent choice is stored per category with its time and the exact wording shown."""
    subject = "probe-subject-" + cf.unique_suffix()
    wording = "Ferment asks before using optional cookies, probe " + subject
    choices = {"functionality": True, "experience": False, "measurement": False,
               "marketing": False}
    with cf.api() as client:
        stored = client.post("/consent", json={"subject_id": subject, "choices": choices,
                                               "wording_version": "probe", "wording": wording})
        assert cf.accepted(stored), cf.describe(stored, "consent must store")
        assert cf.body_of(stored).get("recorded_at"), stored.text[:200]
        changed = dict(choices, experience=True)
        client.post("/consent", json={"subject_id": subject, "choices": changed,
                                      "wording_version": "probe", "wording": wording})
        latest = client.get(f"/consent/{subject}")
    assert latest.status_code == 200, cf.describe(latest, "consent must be readable")
    read = cf.body_of(latest).get("choices", {})
    assert read.get("experience") is True and read.get("measurement") is False, read
    rows = cf.backend().rows(cf.TABLE_CONSENT, subject_id=subject)
    categories = {r.get("category") for r in rows}
    assert set(cf.CONSENT_OPTIONAL) <= categories, categories
    assert all(r.get("wording_shown") == wording for r in rows), "the wording must be stored"


def test_marketing_view_requires_measurement_consent() -> None:
    """A marketing view is refused and recorded nowhere until measurement is granted."""
    subject = "probe-subject-" + cf.unique_suffix()
    with cf.api() as client:
        client.post("/consent", json={"subject_id": subject,
                                      "choices": {k: False for k in cf.CONSENT_OPTIONAL},
                                      "wording_version": "probe", "wording": "probe wording"})
        refused = client.post("/marketing-views", json={"subject_id": subject, "route": "/"})
        assert cf.is_client_error(refused), cf.describe(refused, "no consent, no view")
        assert cf.backend().count(cf.TABLE_MARKETING_VIEW, subject_id=subject) == 0
        client.post("/consent", json={"subject_id": subject,
                                      "choices": {k: True for k in cf.CONSENT_OPTIONAL},
                                      "wording_version": "probe", "wording": "probe wording"})
        accepted = client.post("/marketing-views", json={"subject_id": subject, "route": "/"})
    assert cf.accepted(accepted), cf.describe(accepted, "granted consent records")
    assert cf.backend().count(cf.TABLE_MARKETING_VIEW, subject_id=subject) == 1


def test_signup_returns_a_token_and_a_member_role() -> None:
    """Open signup creates a member and returns a bearer token."""
    probe = cf.signup(cf.unique_suffix())
    assert probe["payload"].get("role") == cf.ROLE_MEMBER, probe["payload"]
    with cf.api(probe["token"]) as client:
        me = client.get("/me")
    assert me.status_code == 200 and cf.body_of(me).get("role") == cf.ROLE_MEMBER, me.text[:200]


def test_signup_creates_an_owned_free_workspace() -> None:
    """Signup creates a Free workspace owned by the new member, named as the brief says."""
    suffix = cf.unique_suffix()
    named = cf.signup(suffix, workspace_name="Probe Studio " + suffix)
    rows = cf.workspaces(named["token"])
    assert len(rows) == 1, rows
    assert rows[0].get("name") == "Probe Studio " + suffix, rows
    assert rows[0].get("relation") == cf.RELATION_OWNER and rows[0].get("plan_key") == cf.PLAN_FREE
    other = cf.unique_suffix()
    unnamed = cf.signup(other)
    default = cf.workspaces(unnamed["token"])[0]
    assert default.get("name") == "Probe " + other + "'s workspace", default


def test_duplicate_or_short_signup_is_rejected() -> None:
    """A reused address or a short password is refused, and nothing new is stored."""
    probe = cf.signup(cf.unique_suffix())
    with cf.api() as client:
        dup = client.post("/auth/signup", json={"email": probe["email"],
                                                "password": "another-long-pass",
                                                "display_name": "Twin"})
        short_email = cf.probe_address(cf.unique_suffix())
        short = client.post("/auth/signup", json={"email": short_email, "password": "short",
                                                  "display_name": "Short"})
    assert cf.is_client_error(dup), cf.describe(dup, "a reused address must be refused")
    assert cf.is_client_error(short), cf.describe(short, "a short password must be refused")
    assert "password" in short.text.lower(), cf.describe(short, "the field must be named")
    assert cf.backend().count(cf.TABLE_ACCOUNT, email=probe["email"]) == 1
    assert cf.backend().count(cf.TABLE_ACCOUNT, email=short_email) == 0


def test_signup_role_in_body_is_ignored() -> None:
    """A signup body naming a role still creates a member account."""
    suffix = cf.unique_suffix()
    with cf.api() as client:
        response = client.post("/auth/signup", json={
            "email": cf.probe_address(suffix), "password": cf.probe_password(suffix),
            "display_name": "Sneaky", "role": cf.ROLE_REVIEWER})
    assert cf.accepted(response), cf.describe(response, "signup must succeed")
    row = cf.backend().one(cf.TABLE_ACCOUNT, email=cf.probe_address(suffix))
    assert row and row.get("role") == cf.ROLE_MEMBER, row


def test_seeded_accounts_sign_in_with_the_corpus_password() -> None:
    """Every seeded account signs in with the corpus password and carries its role."""
    for email in cf.SEEDED_EMAILS:
        token = cf.login(email)
        with cf.api(token) as client:
            me = client.get("/me")
        expected = cf.ROLE_REVIEWER if email.startswith("reviewer") else cf.ROLE_MEMBER
        assert cf.body_of(me).get("role") == expected, me.text[:200]
    with cf.api() as client:
        wrong = client.post("/auth/login", json={"email": cf.MEMBER_EMAIL,
                                                 "password": "not-the-password"})
    assert cf.is_client_error(wrong), cf.describe(wrong, "a wrong password must be denied")
    assert not cf.body_of(wrong).get("access_token"), "a denied login returns no token"


def test_passwords_are_stored_hashed_and_never_returned(owner) -> None:
    """The store holds a hash, and no endpoint returns a password or its hash."""
    row = cf.backend().one(cf.TABLE_ACCOUNT, email=cf.MEMBER_EMAIL)
    assert row and row.get("password_hash"), row
    assert cf.SEEDED_PASSWORD not in str(row.get("password_hash")), "the password must be hashed"
    assert len(str(row.get("password_hash"))) > 30, "the hash must not be a short encoding"
    with cf.api(owner) as client:
        texts = [client.get("/me").text,
                 client.get(f"/workspaces/{cf.workspace_id(owner, cf.WS_JUNIPER)}/members").text]
    for text in texts:
        assert "password" not in text.lower(), text[:200]


def test_guarded_endpoints_deny_missing_or_foreign_tokens() -> None:
    """A call with no token or an invented token is denied and changes nothing."""
    ws = cf.workspace_id(cf.login(cf.MEMBER_EMAIL), cf.WS_JUNIPER)
    before = cf.backend().count(cf.TABLE_PROJECT)
    for token in (None, "invented-" + cf.unique_suffix()):
        with cf.api(token) as client:
            for response in (client.get("/workspaces"), client.get("/me"),
                             client.post(f"/workspaces/{ws}/projects",
                                         json={"name": "Nope", "canvas_width": 100,
                                               "canvas_height": 100, "fps": 30,
                                               "duration_ms": 2000})):
                assert response.status_code in (401, 403), cf.describe(response, "must be denied")
    assert cf.backend().count(cf.TABLE_PROJECT) == before


def test_workspaces_list_only_the_callers_workspaces(owner, teammate) -> None:
    """The workspace list names only the caller's workspaces and the caller's relation."""
    names = {w["name"]: w for w in cf.workspaces(owner)}
    assert cf.WS_JUNIPER in names and names[cf.WS_JUNIPER]["relation"] == cf.RELATION_OWNER
    assert cf.WS_SOLO not in names and cf.WS_BENCH not in names, names
    mate = {w["name"]: w for w in cf.workspaces(teammate)}
    assert mate[cf.WS_JUNIPER]["relation"] == "member", mate
    assert mate[cf.WS_JUNIPER]["plan_key"] == cf.PLAN_PRO, mate


def test_interface_scale_is_stored_and_validated() -> None:
    """The interface scale takes one of four values and follows the account."""
    probe = cf.signup(cf.unique_suffix())
    with cf.api(probe["token"]) as client:
        bad = client.patch("/me", json={"interface_scale": 120})
        good = client.patch("/me", json={"interface_scale": 130})
    assert cf.is_client_error(bad), cf.describe(bad, "an unlisted scale must be refused")
    assert good.status_code == 200, cf.describe(good, "a listed scale must store")
    fresh = cf.login(probe["email"], probe["password"])
    with cf.api(fresh) as client:
        me = cf.body_of(client.get("/me"))
    assert me.get("interface_scale") == 130, me
    assert set(cf.INTERFACE_SCALES) == {100, 115, 130, 150}


def test_non_owner_cannot_change_plan_invite_or_read_charges(teammate) -> None:
    """A member who does not own the workspace is denied every owner-only action."""
    ws = cf.workspace_id(teammate, cf.WS_JUNIPER)
    before = cf.subscription(teammate, ws)
    invites_before = cf.backend().count(cf.TABLE_INVITATION)
    with cf.api(teammate) as client:
        plan = client.post(f"/workspaces/{ws}/subscription",
                           json={"plan_key": cf.PLAN_BUSINESS, "billing_period": cf.MONTHLY})
        invitation = client.post(f"/workspaces/{ws}/invitations",
                                 json={"email": cf.probe_address(cf.unique_suffix())})
        money = client.get(f"/workspaces/{ws}/charges")
        views = client.get(f"/workspaces/{ws}/shares/1/views")
    for response in (plan, invitation, money, views):
        assert cf.denied(response), cf.describe(response, "a non-owner is denied")
    assert cf.subscription(teammate, ws)["plan_key"] == before["plan_key"] == cf.PLAN_PRO
    assert cf.backend().count(cf.TABLE_INVITATION) == invites_before


def test_seeded_subscription_rows_are_persisted(owner) -> None:
    """The seeded Pro workspace is persisted with its period, seats and charge."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    sub = cf.subscription(owner, ws)
    assert sub["plan_key"] == cf.PLAN_PRO and sub["billing_period"] == cf.MONTHLY, sub
    assert sub["seats"] == 2 and sub["seats_used"] == 9, sub
    start, end = cf.date_of(sub["current_period_start"]), cf.date_of(sub["current_period_end"])
    assert str(sub["current_period_start"]).endswith("Z"), sub
    assert end.day == start.day or end.day < start.day, (start, end)
    assert (end.month - start.month) % 12 == 1, (start, end)
    lines = cf.charges(owner, ws)
    plan_lines = [c for c in lines if c.get("kind") == cf.KIND_PLAN_CHANGE]
    assert plan_lines and plan_lines[-1].get("amount_cents") == cf.JUNIPER_PLAN_CHARGE, lines
    assert all(c.get("currency") == cf.CURRENCY for c in lines), lines
    stamps = [c.get("created_at") for c in lines]
    assert stamps == sorted(stamps, reverse=True), "charges must list newest first"
    row = cf.backend().one(cf.TABLE_SUBSCRIPTION, workspace_id=ws)
    assert row and row.get("plan_key") == cf.PLAN_PRO, row
    invites = cf.backend().rows(cf.TABLE_INVITATION, workspace_id=ws, state=cf.INVITE_PENDING)
    assert {i.get("email") for i in invites} >= set(cf.CREW_EMAILS), invites


def test_plan_change_restarts_the_period_and_writes_a_charge() -> None:
    """A plan change starts a period today and charges seats times the period price."""
    probe = cf.probe_workspace(cf.PLAN_BASIC, cf.MONTHLY)
    sub = cf.subscription(probe["token"], probe["ws"])
    assert sub["plan_key"] == cf.PLAN_BASIC and sub["seats"] == 1, sub
    assert cf.date_of(sub["current_period_start"]) == cf.today_utc(), sub
    first = cf.charges(probe["token"], probe["ws"])[0]
    assert first["kind"] == cf.KIND_PLAN_CHANGE and first["amount_cents"] == 2500, first
    moved = cf.change_plan(probe["token"], probe["ws"], cf.PLAN_PRO, cf.ANNUAL)
    assert cf.accepted(moved), cf.describe(moved, "an upgrade must succeed")
    sub = cf.subscription(probe["token"], probe["ws"])
    assert sub["plan_key"] == cf.PLAN_PRO and sub["seats"] == 1, sub
    assert (cf.date_of(sub["current_period_end"]).year
            - cf.date_of(sub["current_period_start"]).year) == 1, sub
    latest = cf.charges(probe["token"], probe["ws"])[0]
    assert latest["amount_cents"] == 3000 * 12 and latest["seats"] == 1, latest


def test_enterprise_plan_change_is_refused() -> None:
    """Choosing Enterprise is refused with the sales sentence and changes nothing."""
    probe = cf.probe_workspace()
    response = cf.change_plan(probe["token"], probe["ws"], cf.PLAN_ENTERPRISE)
    assert cf.is_client_error(response), cf.describe(response, "enterprise must be refused")
    assert cf.message_of(response) == cf.MSG_ENTERPRISE, response.text[:300]
    assert cf.subscription(probe["token"], probe["ws"])["plan_key"] == cf.PLAN_FREE


def test_upgrade_converts_members_into_seats() -> None:
    """Moving to Pro turns members into seats, and a multi-member downgrade is refused."""
    probe = cf.probe_workspace(cf.PLAN_PRO)
    cf.join_workspace(probe["token"], probe["ws"])
    sub = cf.subscription(probe["token"], probe["ws"])
    assert sub["seats"] == 2, sub
    refused = cf.change_plan(probe["token"], probe["ws"], cf.PLAN_FREE)
    assert cf.is_client_error(refused), cf.describe(refused, "a multi-member downgrade is refused")
    assert cf.message_of(refused) == cf.MSG_SWITCH_FREE, refused.text[:300]
    assert cf.subscription(probe["token"], probe["ws"])["plan_key"] == cf.PLAN_PRO


def test_pro_seat_cap_refuses_the_eleventh_member(owner) -> None:
    """At 10 of 10 the next invitation is refused with the seat-cap sentence."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    tenth = cf.invite(owner, ws, cf.probe_address(cf.unique_suffix()))
    assert cf.accepted(tenth), cf.describe(tenth, "the tenth place must be granted")
    try_email = cf.probe_address(cf.unique_suffix())
    eleventh = cf.invite(owner, ws, try_email)
    released = cf.revoke(owner, ws, tenth.json()["id"])
    assert cf.is_client_error(eleventh), cf.describe(eleventh, "the eleventh must be refused")
    payload = cf.body_of(eleventh)
    assert payload.get("error") == cf.QUOTA_ERROR and payload.get("meter") == cf.METER_MEMBERS
    assert payload.get("message") == cf.MSG_SEAT_CAP, payload
    assert cf.backend().count(cf.TABLE_INVITATION, email=try_email) == 0
    assert released.status_code in (200, 204), cf.describe(released, "revoking must succeed")
    assert cf.subscription(owner, ws)["seats_used"] == 9


def test_concurrent_invitations_at_the_last_seat_admit_one(owner) -> None:
    """Two invitations racing for the last Pro seat never both succeed."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    emails = [cf.probe_address(cf.unique_suffix()) for _ in range(2)]
    results = cf.run_together(lambda: cf.invite(owner, ws, emails[0]),
                              lambda: cf.invite(owner, ws, emails[1]))
    winners = [r for r in results if cf.accepted(r)]
    for won in winners:
        cf.revoke(owner, ws, won.json()["id"])
    assert len(winners) == 1, [r.status_code for r in results]
    assert cf.usage(owner, ws, cf.METER_MEMBERS)["used"] == 9


def test_single_user_plans_refuse_invitations(solo, bench) -> None:
    """Free and Basic workspaces refuse an invitation with the one-person sentence."""
    free = cf.invite(solo, cf.workspace_id(solo, cf.WS_SOLO), cf.probe_address(cf.unique_suffix()))
    basic = cf.invite(bench, cf.workspace_id(bench, cf.WS_BENCH),
                      cf.probe_address(cf.unique_suffix()))
    assert cf.is_client_error(free) and cf.message_of(free) == cf.MSG_SINGLE_FREE, free.text[:300]
    assert cf.is_client_error(basic), cf.describe(basic, "basic must refuse an invitation")
    assert cf.message_of(basic).startswith(cf.MSG_SINGLE_BASIC_OPENING), basic.text[:300]


def test_accepted_invitation_writes_a_prorated_seat_charge(owner) -> None:
    """A mid-period join on Pro writes one seat charge prorated to the remaining days."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    sub = cf.subscription(owner, ws)
    guest = cf.join_workspace(owner, ws)
    joined = cf.today_utc()
    after = cf.subscription(owner, ws)
    latest = cf.charges(owner, ws)[0]
    member = cf.account_id(owner, ws, guest["email"])
    with cf.api(owner) as client:
        removed = client.delete(f"/workspaces/{ws}/members/{member}")
    assert removed.status_code in (200, 204), cf.describe(removed, "the owner must remove")
    assert after["seats"] == sub["seats"] + 1, (sub, after)
    assert latest["kind"] == cf.KIND_SEAT_ADDED and latest["seats"] == 1, latest
    expected = cf.prorated_cents(3800, sub["current_period_start"], sub["current_period_end"],
                                 joined)
    assert latest["amount_cents"] == expected, (latest, expected)
    assert cf.prorated_cents(3800, "2026-09-01", "2026-10-01",
                             cf.date_of("2026-09-16")) == 1900
    assert cf.prorated_cents(3800, "2026-09-01", "2026-10-01",
                             cf.date_of("2026-09-21")) == 1267
    assert cf.prorated_cents(36000, "2026-01-10", "2027-01-10",
                             cf.date_of("2026-09-16")) == 11441
    final = cf.subscription(owner, ws)
    assert final["seats"] == sub["seats"] and final["seats_used"] == 9, final


def test_removing_a_member_keeps_their_work_and_frees_the_seat() -> None:
    """A removed member loses access at once, their project stays, the seat is freed."""
    probe = cf.probe_workspace(cf.PLAN_PRO)
    guest = cf.join_workspace(probe["token"], probe["ws"])
    project = cf.make_project(guest["token"], probe["ws"])
    before = cf.subscription(probe["token"], probe["ws"])
    refunds_before = len(cf.charges(probe["token"], probe["ws"]))
    assert len(cf.workspaces(guest["token"])) == 2, cf.workspaces(guest["token"])
    member = cf.account_id(probe["token"], probe["ws"], guest["email"])
    owner_id = cf.account_id(probe["token"], probe["ws"], probe["email"])
    with cf.api(probe["token"]) as client:
        own = client.delete(f"/workspaces/{probe['ws']}/members/{owner_id}")
        removed = client.delete(f"/workspaces/{probe['ws']}/members/{member}")
    assert cf.is_client_error(own), cf.describe(own, "the owner cannot be removed")
    assert removed.status_code in (200, 204), cf.describe(removed, "removal must succeed")
    with cf.api(guest["token"]) as client:
        denied = client.get(f"/workspaces/{probe['ws']}/projects")
    assert cf.denied(denied), cf.describe(denied, "the removed member is denied")
    kept = cf.get_project(probe["token"], probe["ws"], project["id"])
    assert kept["id"] == project["id"], kept
    after = cf.subscription(probe["token"], probe["ws"])
    assert after["seats"] == before["seats"] - 1, (before, after)
    assert len(cf.charges(probe["token"], probe["ws"])) == refunds_before, "no refund line"


def test_usage_lists_every_meter_with_its_window(bench) -> None:
    """Usage returns one row per meter, and older windows never count."""
    ws = cf.workspace_id(bench, cf.WS_BENCH)
    project = cf.seeded_project(bench, ws, cf.BENCH_PROMO)
    with cf.api(bench) as client:
        versions = cf.listing(client.get(f"/workspaces/{ws}/projects/{project['id']}/versions"))
        cf.listing(client.get(f"/workspaces/{ws}/versions/{versions[-1]['id']}/exports"))
        rows = cf.listing(client.get(f"/workspaces/{ws}/usage"))
    assert {r.get("meter") for r in rows} == set(cf.METERS), rows
    sub = cf.subscription(bench, ws)
    variations = [r for r in rows if r["meter"] == cf.METER_VARIATIONS][0]
    assert variations["used"] == 19 and variations["limit"] == 20, variations
    assert cf.date_of(variations["window_start"]) == cf.date_of(sub["current_period_start"])
    members = [r for r in rows if r["meter"] == cf.METER_MEMBERS][0]
    assert members["used"] == 1 and members["limit"] == 1, members
    for row in rows:
        if row.get("limit") is not None:
            assert row["used"] <= row["limit"], row


def test_stale_rendering_export_reads_failed_and_is_released(bench) -> None:
    """The seeded export left rendering for hours reads failed, and its unit is not counted."""
    ws = cf.workspace_id(bench, cf.WS_BENCH)
    project = cf.seeded_project(bench, ws, cf.BENCH_PROMO)
    with cf.api(bench) as client:
        versions = cf.listing(client.get(f"/workspaces/{ws}/projects/{project['id']}/versions"))
        jobs = cf.listing(client.get(f"/workspaces/{ws}/versions/{versions[-1]['id']}/exports"))
    stale = [j for j in jobs if j.get("request_key") == cf.STALE_KEY]
    assert len(stale) == 1 and stale[0]["status"] == cf.STATUS_FAILED, stale
    assert not any(j["status"] == cf.STATUS_READY for j in jobs), "Bench Promo has no ready export"
    assert cf.usage(bench, ws, cf.METER_VARIATIONS)["used"] == 19


def test_concurrent_variation_claims_on_the_last_unit_admit_one(bench) -> None:
    """Two variation exports racing for the last monthly unit never both succeed."""
    ws = cf.workspace_id(bench, cf.WS_BENCH)
    project = cf.seeded_project(bench, ws, cf.BENCH_PROMO)
    with cf.api(bench) as client:
        versions = cf.listing(client.get(f"/workspaces/{ws}/projects/{project['id']}/versions"))
    vid = versions[-1]["id"]
    assert cf.usage(bench, ws, cf.METER_VARIATIONS)["used"] == 19
    results = cf.run_together(lambda: cf.request_export(bench, ws, vid, 540, 540),
                              lambda: cf.request_export(bench, ws, vid, 720, 720))
    winners = [r for r in results if cf.accepted(r)]
    losers = [r for r in results if cf.is_client_error(r)]
    for won in winners:
        cf.fail_export(bench, ws, won.json()["id"])
    assert len(winners) == 1 and len(losers) == 1, [r.status_code for r in results]
    assert cf.message_of(losers[0]) == cf.MSG_MONTHLY_BASIC, losers[0].text[:300]
    assert cf.body_of(losers[0]).get("limit") == 20, losers[0].text[:300]
    assert cf.usage(bench, ws, cf.METER_VARIATIONS)["used"] == 19


def test_spent_allowance_refusal_names_meter_limit_and_plan(bench) -> None:
    """With the allowance spent, a variation is refused naming meter, limit and plan."""
    ws = cf.workspace_id(bench, cf.WS_BENCH)
    project = cf.seeded_project(bench, ws, cf.BENCH_PROMO)
    with cf.api(bench) as client:
        vid = cf.listing(client.get(f"/workspaces/{ws}/projects/{project['id']}/versions"))[-1]["id"]
    held = cf.request_export(bench, ws, vid, 540, 540)
    refused = cf.request_export(bench, ws, vid, 540, 540)
    during = cf.usage(bench, ws, cf.METER_VARIATIONS)["used"]
    cf.fail_export(bench, ws, held.json()["id"])
    assert cf.accepted(held), cf.describe(held, "the twentieth unit is reserved")
    assert during == 20, during
    payload = cf.body_of(refused)
    assert cf.is_client_error(refused), cf.describe(refused, "the twenty-first must be refused")
    assert payload.get("error") == cf.QUOTA_ERROR, payload
    assert payload.get("meter") == cf.METER_VARIATIONS and payload.get("plan"), payload
    assert payload.get("message") == cf.MSG_MONTHLY_BASIC, payload
    assert cf.usage(bench, ws, cf.METER_VARIATIONS)["used"] == 19


def test_saved_block_ceiling_refuses_the_sixth(solo, suffix) -> None:
    """At 5 of 5 saved blocks the next save is refused with the ceiling sentence."""
    ws = cf.workspace_id(solo, cf.WS_SOLO)
    fifth = cf.save_block(solo, ws, cf.custom_block_body(suffix))
    sixth = cf.save_block(solo, ws, cf.custom_block_body(suffix + "x"))
    cleanup = cf.delete_block(solo, ws, fifth.json()["id"]) if cf.accepted(fifth) else None
    assert cf.accepted(fifth), cf.describe(fifth, "the fifth block must save")
    assert cf.is_client_error(sixth), cf.describe(sixth, "the sixth block must be refused")
    assert cf.message_of(sixth) == cf.MSG_CEILING_FREE_BLOCKS, sixth.text[:300]
    assert cleanup is not None and cleanup.status_code in (200, 204)
    assert cf.usage(solo, ws, cf.METER_BLOCKS)["used"] == 4


def test_concurrent_block_saves_at_the_ceiling_admit_one(solo) -> None:
    """Two block saves racing for the last Free place never both succeed."""
    ws = cf.workspace_id(solo, cf.WS_SOLO)
    bodies = [cf.custom_block_body(cf.unique_suffix()) for _ in range(2)]
    results = cf.run_together(lambda: cf.save_block(solo, ws, bodies[0]),
                              lambda: cf.save_block(solo, ws, bodies[1]))
    winners = [r for r in results if cf.accepted(r)]
    for won in winners:
        cf.delete_block(solo, ws, won.json()["id"])
    assert len(winners) == 1, [r.status_code for r in results]
    assert cf.usage(solo, ws, cf.METER_BLOCKS)["used"] == 4


def test_brand_kits_are_not_included_on_basic(bench) -> None:
    """Basic refuses a brand kit with the not-included sentence and stores nothing."""
    ws = cf.workspace_id(bench, cf.WS_BENCH)
    before = cf.backend().count("brand_kit", workspace_id=ws)
    with cf.api(bench) as client:
        response = client.post(f"/workspaces/{ws}/brand-kits",
                               json={"name": "Nope", "colours": ["#112233"], "fonts": ["Sans"]})
    assert cf.is_client_error(response), cf.describe(response, "basic must refuse brand kits")
    assert cf.message_of(response) == cf.MSG_KITS_BASIC, response.text[:300]
    assert cf.backend().count("brand_kit", workspace_id=ws) == before


def test_concurrent_brand_kits_at_the_ceiling_admit_one(owner) -> None:
    """Two brand kits racing for the last Pro place never both succeed."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    def make(name):
        with cf.api(owner) as client:
            return client.post(f"/workspaces/{ws}/brand-kits",
                               json={"name": name, "colours": ["#223344", "#AABBCC"],
                                     "fonts": ["Probe Sans"]})
    results = cf.run_together(lambda: make("Probe Kit A"), lambda: make("Probe Kit B"))
    winners = [r for r in results if cf.accepted(r)]
    losers = [r for r in results if cf.is_client_error(r)]
    for won in winners:
        with cf.api(owner) as client:
            client.delete(f"/workspaces/{ws}/brand-kits/{won.json()['id']}")
    assert len(winners) == 1, [r.status_code for r in results]
    assert cf.message_of(losers[0]) == cf.ceiling_pattern("Pro", 5, "brand kits"), losers[0].text
    assert cf.usage(owner, ws, cf.METER_KITS)["used"] == 4


def test_brand_kit_colours_are_validated(owner) -> None:
    """A kit with a bad colour list or font list is refused and not stored."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    before = cf.backend().count("brand_kit", workspace_id=ws)
    with cf.api(owner) as client:
        for colours in ([], ["#000000"] * 9, ["red"], ["#12345G"]):
            response = client.post(f"/workspaces/{ws}/brand-kits",
                                   json={"name": "Bad Kit", "colours": colours, "fonts": ["Sans"]})
            assert cf.is_client_error(response), cf.describe(response, f"{colours} must be refused")
            assert "colour" in response.text.lower() or "color" in response.text.lower()
        for fonts in ([], ["A", "B", "C", "D", "E"]):
            response = client.post(f"/workspaces/{ws}/brand-kits",
                                   json={"name": "Bad Fonts", "colours": ["#000000"], "fonts": fonts})
            assert cf.is_client_error(response), cf.describe(response, f"{fonts} must be refused")
    assert cf.backend().count("brand_kit", workspace_id=ws) == before


def test_downgrade_keeps_existing_items_but_blocks_new_ones() -> None:
    """A smaller plan keeps what the workspace has and refuses new items over the ceiling."""
    probe = cf.probe_workspace(cf.PLAN_PRO)
    with cf.api(probe["token"]) as client:
        kit = client.post(f"/workspaces/{probe['ws']}/brand-kits",
                          json={"name": "Keep Me", "colours": ["#101010"], "fonts": ["Sans"]})
    assert cf.accepted(kit), cf.describe(kit, "pro must accept a brand kit")
    moved = cf.change_plan(probe["token"], probe["ws"], cf.PLAN_BASIC)
    assert cf.accepted(moved), cf.describe(moved, "a one-member downgrade succeeds")
    with cf.api(probe["token"]) as client:
        kits = cf.listing(client.get(f"/workspaces/{probe['ws']}/brand-kits"))
        again = client.post(f"/workspaces/{probe['ws']}/brand-kits",
                            json={"name": "New", "colours": ["#202020"], "fonts": ["Sans"]})
    assert [k.get("name") for k in kits] == ["Keep Me"], kits
    assert cf.is_client_error(again), cf.describe(again, "a new kit over the ceiling is refused")


def test_coming_soon_meters_stay_unconsumed(owner) -> None:
    """Captioning and speech allowances are published and never consumed."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    assert cf.usage(owner, ws, cf.METER_CAPTION)["used"] == 0
    assert cf.usage(owner, ws, cf.METER_SPEECH)["used"] == 0
    assert cf.usage(owner, ws, cf.METER_CAPTION)["limit"] == 120


def test_library_lists_the_eight_blocks_with_schemas() -> None:
    """The library carries the eight blocks, each with a declared parameter schema."""
    with cf.api() as client:
        rows = cf.listing(client.get("/blocks", params={"limit": 50}))
    names = {b.get("name") for b in rows}
    assert set(cf.LIBRARY_BLOCKS) <= names, names
    glow = cf.library_block(cf.BLOCK_GLOW)
    schema = {p["key"]: p for p in glow["parameter_schema"]}
    assert schema["intensity"]["control"] == "slider", schema
    assert (schema["intensity"]["min"], schema["intensity"]["max"]) == (0, 100), schema
    assert schema["hue"]["control"] == "dial" and schema["text"]["control"] == "prompt", schema
    kinds = set()
    for name in cf.LIBRARY_BLOCKS:
        for param in cf.library_block(name)["parameter_schema"]:
            kinds.add(param["control"])
    assert kinds == set(cf.CONTROL_KINDS), kinds


def test_block_list_filters_and_pages() -> None:
    """The block list filters by category and name and pages with limit and offset."""
    with cf.api() as client:
        text = cf.listing(client.get("/blocks", params={"category": cf.CATEGORY_TEXT}))
        named = cf.listing(client.get("/blocks", params={"q": "glow"}))
        page_one = cf.listing(client.get("/blocks", params={"limit": 2, "offset": 0}))
        page_two = cf.listing(client.get("/blocks", params={"limit": 2, "offset": 2}))
    assert {b["name"] for b in text} >= {"Inflate", "Glow", "Focus", "Halftone"}, text
    assert all(b.get("category") == cf.CATEGORY_TEXT for b in text), text
    assert [b["name"] for b in named] == [cf.BLOCK_GLOW], named
    assert len(page_one) == 2 and len(page_two) == 2, (page_one, page_two)
    assert not {b["id"] for b in page_one} & {b["id"] for b in page_two}


def test_templates_are_seeded_with_stable_uuids() -> None:
    """Eight templates carry stable uuids, four categories and two premium entries."""
    with cf.api() as client:
        rows = cf.listing(client.get("/templates"))
        beauty = cf.listing(client.get("/templates", params={"category": "Beauty"}))
        denim = client.get(f"/templates/{cf.DENIM_UUID}")
    assert {t.get("uuid") for t in rows} >= set(cf.TEMPLATE_UUIDS), rows
    assert {t.get("category") for t in rows} == set(cf.TEMPLATE_CATEGORIES), rows
    assert sorted(t["name"] for t in rows if t.get("premium")) == sorted(cf.PREMIUM_NAMES)
    assert len(beauty) == 3 and all(t["category"] == "Beauty" for t in beauty), beauty
    body = cf.body_of(denim)
    assert body.get("name") == cf.DENIM_NAME, body
    items = {i["id"]: i for t in body["timeline"]["tracks"] for i in t["items"]}
    assert items[cf.ITEM_TITLE]["start_ms"] == 0 and items[cf.ITEM_TITLE]["duration_ms"] == 5000
    assert items[cf.ITEM_CLIP]["start_ms"] == 10000, items
    assert (body["canvas_width"], body["canvas_height"], body["fps"]) == (1080, 1920, 30), body


def test_creator_collection_lists_credited_templates() -> None:
    """Each creator slug returns the creator and the templates credited to them."""
    for slug in cf.CREATOR_SLUGS:
        with cf.api() as client:
            response = client.get(f"/creators/{slug}")
        assert response.status_code == 200, cf.describe(response, f"{slug} must be readable")
        body = response.json()
        assert body.get("display_name") in cf.CREATOR_NAMES, body
        assert body.get("templates"), body
        assert cf.fetch_document(f"/creators/{slug}").status_code == 200


def test_favourites_are_single_per_target() -> None:
    """A favourite names one target, and favouriting twice leaves one favourite."""
    probe = cf.probe_workspace()
    glow = cf.library_block(cf.BLOCK_GLOW)
    with cf.api(probe["token"]) as client:
        both = client.post(f"/workspaces/{probe['ws']}/favorites",
                           json={"block_id": glow["id"], "template_uuid": cf.DENIM_UUID})
        client.post(f"/workspaces/{probe['ws']}/favorites", json={"block_id": glow["id"]})
        client.post(f"/workspaces/{probe['ws']}/favorites", json={"block_id": glow["id"]})
        rows = cf.listing(client.get(f"/workspaces/{probe['ws']}/favorites"))
    assert cf.is_client_error(both), cf.describe(both, "a favourite with two targets is refused")
    assert len([r for r in rows if r.get("block_id") == glow["id"]]) == 1, rows


def test_remix_copies_the_template_with_its_parameters() -> None:
    """Remix creates a project named after the template, keeping every parameter value."""
    probe = cf.probe_workspace()
    with cf.api(probe["token"]) as client:
        template = cf.body_of(client.get(f"/templates/{cf.DENIM_UUID}"))
        response = client.post(f"/workspaces/{probe['ws']}/templates/{cf.DENIM_UUID}/remix")
    assert cf.accepted(response), cf.describe(response, "remix must succeed")
    project = cf.get_project(probe["token"], probe["ws"], response.json()["id"])
    assert project["name"] == cf.DENIM_NAME + " remix", project
    assert project["remixed_from"] == cf.DENIM_UUID and project["revision"] == 1, project
    source = [i.get("params") for t in template["timeline"]["tracks"] for i in t["items"]]
    copied = [i.get("params") for t in project["timeline"]["tracks"] for i in t["items"]]
    assert source == copied, (source, copied)


def test_premium_template_remix_is_refused_on_free() -> None:
    """A Free workspace cannot remix a premium template, and nothing is created."""
    probe = cf.probe_workspace()
    before = cf.backend().count(cf.TABLE_PROJECT, workspace_id=probe["ws"])
    with cf.api(probe["token"]) as client:
        response = client.post(
            f"/workspaces/{probe['ws']}/templates/{cf.FEATURE_REVEAL_UUID}/remix")
    assert cf.is_client_error(response), cf.describe(response, "premium must be refused on Free")
    assert cf.message_of(response) == cf.MSG_PREMIUM_FREE, response.text[:300]
    assert cf.backend().count(cf.TABLE_PROJECT, workspace_id=probe["ws"]) == before


def test_describe_builds_tracks_and_consumes_a_variation() -> None:
    """Describe places one track per named block in prompt order and spends one unit."""
    probe = cf.probe_workspace(cf.PLAN_BASIC)
    source = cf.make_project(probe["token"], probe["ws"], name="Autumn Drop")
    prompt = "glow ticker for the autumn denim drop weekend launch sale"
    with cf.api(probe["token"]) as client:
        response = client.post(f"/workspaces/{probe['ws']}/projects/{source['id']}/describe",
                               json={"prompt": prompt})
    assert cf.accepted(response), cf.describe(response, "describe must succeed")
    project = cf.get_project(probe["token"], probe["ws"], response.json()["id"])
    assert project["name"] == "Autumn Drop - described 1", project
    glow, ticker = cf.library_block(cf.BLOCK_GLOW), cf.library_block(cf.BLOCK_TICKER)
    tracks = project["timeline"]["tracks"]
    assert [t["items"][0]["block_id"] for t in tracks] == [glow["id"], ticker["id"]], tracks
    first, second = tracks[0]["items"][0], tracks[1]["items"][0]
    assert first["start_ms"] == 0 and first["duration_ms"] == source["duration_ms"], first
    assert first["params"]["text"] == prompt[:40], first
    assert second["params"]["message"] == prompt, second
    assert cf.usage(probe["token"], probe["ws"], cf.METER_VARIATIONS)["used"] == 1


def test_describe_without_a_match_is_rejected_and_costs_nothing() -> None:
    """A prompt naming no block is refused with the no-match sentence and costs nothing."""
    probe = cf.probe_workspace(cf.PLAN_BASIC)
    source = cf.make_project(probe["token"], probe["ws"])
    with cf.api(probe["token"]) as client:
        response = client.post(f"/workspaces/{probe['ws']}/projects/{source['id']}/describe",
                               json={"prompt": "something calm and quiet"})
    assert cf.is_client_error(response), cf.describe(response, "no match must be refused")
    assert cf.message_of(response) == cf.MSG_DESCRIBE_NOMATCH, response.text[:300]
    assert cf.usage(probe["token"], probe["ws"], cf.METER_VARIATIONS)["used"] == 0


def test_describe_and_variations_are_not_included_on_free(solo) -> None:
    """Free refuses Describe and variation exports with the not-included sentence."""
    ws = cf.workspace_id(solo, cf.WS_SOLO)
    sketch = cf.seeded_project(solo, ws, cf.FIRST_SKETCH)
    assert (sketch["canvas_width"], sketch["canvas_height"]) == (1280, 720), sketch
    with cf.api(solo) as client:
        response = client.post(f"/workspaces/{ws}/projects/{sketch['id']}/describe",
                               json={"prompt": "glow"})
        versions = cf.listing(client.get(f"/workspaces/{ws}/projects/{sketch['id']}/versions"))
    expected = cf.refusal_pattern("Project variations", "Free", "Basic")
    assert cf.is_client_error(response), cf.describe(response, "Free must refuse describe")
    assert cf.message_of(response) == expected, response.text[:300]
    assert versions == [], versions


def test_custom_block_schema_is_validated() -> None:
    """An invalid parameter schema is refused, names the parameter, and saves nothing."""
    probe = cf.probe_workspace()
    bad = cf.custom_block_body(cf.unique_suffix(), parameter_schema=[
        {"key": "spread", "label": "Spread", "control": "slider", "min": 10, "max": 5,
         "default": 7}])
    response = cf.save_block(probe["token"], probe["ws"], bad)
    assert cf.is_client_error(response), cf.describe(response, "an inverted slider is refused")
    assert "spread" in response.text, cf.describe(response, "the failing parameter is named")
    assert cf.backend().count(cf.TABLE_BLOCK, workspace_id=probe["ws"]) == 0


def test_custom_block_versions_and_placed_items() -> None:
    """Edits add versions, a placed item keeps its version, source stays text."""
    probe = cf.probe_workspace()
    body = cf.custom_block_body(cf.unique_suffix())
    saved = cf.save_block(probe["token"], probe["ws"], body)
    assert cf.accepted(saved), cf.describe(saved, "a custom block must save")
    block = saved.json()
    assert block["version"] == 1, block
    project = cf.make_project(probe["token"], probe["ws"])
    item = {"id": "custom-1", "type": "block", "start_ms": 0, "duration_ms": 1000,
            "block_id": block["id"], "block_version": 1,
            "params": {"headline": "Hi", "slide": 30, "turn": 90}}
    placed = cf.save_timeline(probe["token"], probe["ws"], project["id"], 1, cf.timeline_of([item]))
    assert placed.status_code == 200, cf.describe(placed, "the custom block must place")
    renamed = dict(body, name=body["name"] + " Renamed")
    with cf.api(probe["token"]) as client:
        edited = client.put(f"/workspaces/{probe['ws']}/blocks/{block['id']}", json=renamed)
        versions = cf.listing(client.get(f"/workspaces/{probe['ws']}/blocks/{block['id']}/versions"))
    assert edited.status_code == 200 and edited.json()["version"] == 2, edited.text[:300]
    assert sorted(v["version"] for v in versions) == [1, 2], versions
    assert [v["source"] for v in versions if v["version"] == 1] == [body["source"]], versions
    kept = cf.get_project(probe["token"], probe["ws"], project["id"])
    assert kept["timeline"]["tracks"][0]["items"][0]["block_version"] == 1, kept
    deleted = cf.delete_block(probe["token"], probe["ws"], block["id"])
    assert deleted.status_code in (200, 204), cf.describe(deleted, "a saved block must delete")
    assert cf.usage(probe["token"], probe["ws"], cf.METER_BLOCKS)["used"] == 0
    still = cf.get_project(probe["token"], probe["ws"], project["id"])
    assert still["timeline"]["tracks"][0]["items"][0]["block_version"] == 1, still
    assert cf.backend().count(cf.TABLE_BLOCK_VERSION, block_id=block["id"]) == 2


def test_saved_blocks_stay_inside_their_workspace(owner, solo) -> None:
    """Another workspace can neither list nor place a workspace's saved block."""
    juniper = cf.workspace_id(owner, cf.WS_JUNIPER)
    with cf.api(owner) as client:
        blocks = cf.listing(client.get(f"/workspaces/{juniper}/blocks"))
    assert {b["name"] for b in blocks} >= set(cf.JUNIPER_BLOCKS), blocks
    spin = [b for b in blocks if b["name"] == cf.SPIN_FOREVER][0]
    solo_ws = cf.workspace_id(solo, cf.WS_SOLO)
    with cf.api(solo) as client:
        own = {b["name"] for b in cf.listing(client.get(f"/workspaces/{solo_ws}/blocks"))}
        peek = client.get(f"/workspaces/{juniper}/blocks")
    assert set(cf.SOLO_BLOCKS) <= own and not own & set(cf.JUNIPER_BLOCKS), own
    assert cf.denied(peek), cf.describe(peek, "another workspace is denied")
    sketch = cf.seeded_project(solo, solo_ws, cf.FIRST_SKETCH)
    item = {"id": "foreign-1", "type": "block", "start_ms": 0, "duration_ms": 1000,
            "block_id": spin["id"], "block_version": 1, "params": {}}
    response = cf.save_timeline(solo, solo_ws, sketch["id"], sketch["revision"],
                                cf.timeline_of([item]))
    assert cf.is_client_error(response), cf.describe(response, "a foreign block is refused")
    assert cf.get_project(solo, solo_ws, sketch["id"])["revision"] == sketch["revision"]


def test_new_project_starts_empty_and_validates_its_ranges() -> None:
    """A new project starts at revision 1, empty, and bad dimensions are refused."""
    probe = cf.probe_workspace()
    project = cf.make_project(probe["token"], probe["ws"])
    assert project["revision"] == 1, project
    assert cf.get_project(probe["token"], probe["ws"], project["id"])["timeline"]["tracks"] == []
    with cf.api(probe["token"]) as client:
        for bad in ({"canvas_width": 8}, {"canvas_height": 5000}, {"fps": 29},
                    {"duration_ms": 500}, {"duration_ms": 700000}):
            body = {"name": "Bad", "canvas_width": 640, "canvas_height": 360, "fps": 30,
                    "duration_ms": 2000}
            body.update(bad)
            response = client.post(f"/workspaces/{probe['ws']}/projects", json=body)
            assert cf.is_client_error(response), cf.describe(response, f"{bad} must be refused")


def test_mixed_track_saves_and_advances_the_revision() -> None:
    """A track holding a clip beside two independent Glow items saves at the next revision."""
    probe = cf.probe_workspace()
    project = cf.make_project(probe["token"], probe["ws"])
    glow = cf.library_block(cf.BLOCK_GLOW)
    with cf.api(probe["token"]) as client:
        asset = client.post(f"/workspaces/{probe['ws']}/assets",
                            files={"file": ("clip.png", cf.png_bytes(8, 8), "image/png")})
    assert cf.accepted(asset), cf.describe(asset, "an asset must upload")
    clip = {"id": "clip-1", "type": "clip", "start_ms": 0, "duration_ms": 2000,
            "asset_id": asset.json()["id"]}
    timeline = cf.timeline_of([clip, cf.glow_item("g-1", 2000, 1000, glow, hue=10),
                               cf.glow_item("g-2", 3000, 1000, glow, hue=200)])
    response = cf.save_timeline(probe["token"], probe["ws"], project["id"], 1, timeline)
    assert response.status_code == 200, cf.describe(response, "a mixed track must save")
    stored = cf.get_project(probe["token"], probe["ws"], project["id"])
    assert stored["revision"] == 2, stored
    items = stored["timeline"]["tracks"][0]["items"]
    assert [i["type"] for i in items] == ["clip", "block", "block"], items
    assert [i["params"]["hue"] for i in items[1:]] == [10, 200], items


def test_concurrent_saves_from_one_revision_admit_one() -> None:
    """Two saves made from the same revision never both land."""
    probe = cf.probe_workspace()
    project = cf.make_project(probe["token"], probe["ws"])
    glow = cf.library_block(cf.BLOCK_GLOW)
    one = cf.timeline_of([cf.glow_item("a-1", 0, 1000, glow, hue=1)])
    two = cf.timeline_of([cf.glow_item("b-1", 0, 1000, glow, hue=2)])
    results = cf.run_together(
        lambda: cf.save_timeline(probe["token"], probe["ws"], project["id"], 1, one),
        lambda: cf.save_timeline(probe["token"], probe["ws"], project["id"], 1, two))
    codes = sorted(r.status_code for r in results)
    assert codes[0] == 200 and 400 <= codes[1] < 500, codes
    winner = one if results[0].status_code == 200 else two
    stored = cf.get_project(probe["token"], probe["ws"], project["id"])
    assert stored["revision"] == 2 and stored["timeline"]["tracks"][0]["items"][0]["id"] == \
        winner["tracks"][0]["items"][0]["id"], stored


def test_stale_revision_save_is_a_conflict_carrying_the_revision() -> None:
    """A save from an old revision is refused, carries the stored revision, changes nothing."""
    probe = cf.probe_workspace()
    project = cf.make_project(probe["token"], probe["ws"])
    glow = cf.library_block(cf.BLOCK_GLOW)
    first = cf.save_timeline(probe["token"], probe["ws"], project["id"], 1,
                             cf.timeline_of([cf.glow_item("x-1", 0, 1000, glow)]))
    assert first.status_code == 200, cf.describe(first, "the first save must land")
    stale = cf.save_timeline(probe["token"], probe["ws"], project["id"], 1,
                             cf.timeline_of([cf.glow_item("y-1", 0, 1000, glow)]))
    assert cf.is_client_error(stale), cf.describe(stale, "a stale save must be refused")
    assert cf.body_of(stale).get("revision") == 2, stale.text[:300]
    stored = cf.get_project(probe["token"], probe["ws"], project["id"])
    assert stored["timeline"]["tracks"][0]["items"][0]["id"] == "x-1", stored


def test_invalid_timelines_are_rejected() -> None:
    """Out-of-range starts, durations and parameter values are refused without a write."""
    probe = cf.probe_workspace()
    project = cf.make_project(probe["token"], probe["ws"], duration_ms=6000)
    glow = cf.library_block(cf.BLOCK_GLOW)
    bad_items = [cf.glow_item("n-1", -10, 1000, glow),
                 cf.glow_item("n-2", 5500, 1000, glow),
                 cf.glow_item("n-3", 0, 1000, glow, intensity=101),
                 cf.glow_item("n-4", 0, 1000, glow, hue=360),
                 cf.glow_item("n-5", 0, 1000, glow, text="x" * 41)]
    for item in bad_items:
        response = cf.save_timeline(probe["token"], probe["ws"], project["id"], 1,
                                    cf.timeline_of([item]))
        assert cf.is_client_error(response), cf.describe(response, f"{item['id']} is refused")
    assert cf.get_project(probe["token"], probe["ws"], project["id"])["revision"] == 1


def test_uploaded_file_is_stored_in_the_bucket_under_its_digest() -> None:
    """An uploaded file lands in the bucket at its digest key, once, and the row matches."""
    probe = cf.probe_workspace()
    data = cf.png_bytes(16, 9) + cf.unique_suffix().encode()
    digest = hashlib.sha256(data).hexdigest()
    with cf.api(probe["token"]) as client:
        first = client.post(f"/workspaces/{probe['ws']}/assets",
                            files={"file": ("frame.png", data, "image/png")})
        second = client.post(f"/workspaces/{probe['ws']}/assets",
                             files={"file": ("frame.png", data, "image/png")})
    assert cf.accepted(first), cf.describe(first, "an upload must store")
    key = f"{cf.ASSET_PREFIX}{probe['ws']}/{digest}.png"
    assert cf.body_of(first).get("object_key") == key, first.text[:300]
    assert cf.poll_until(lambda: cf.object_store().exists(key)), f"{key} must be in the bucket"
    assert cf.object_store().list(f"{cf.ASSET_PREFIX}{probe['ws']}/") == [key]
    assert cf.accepted(second), cf.describe(second, "a repeat upload answers")
    assert cf.backend().count(cf.TABLE_ASSET, object_key=key) == 1
    assert cf.usage(probe["token"], probe["ws"], cf.METER_STORAGE)["used"] == len(data)


def test_unsupported_upload_is_rejected_and_writes_nothing() -> None:
    """An upload of an unsupported type is refused and no object is written."""
    probe = cf.probe_workspace()
    with cf.api(probe["token"]) as client:
        response = client.post(f"/workspaces/{probe['ws']}/assets",
                               files={"file": ("notes.txt", b"plain text", "text/plain")})
    assert cf.is_client_error(response), cf.describe(response, "text must be refused")
    assert cf.object_store().list(f"{cf.ASSET_PREFIX}{probe['ws']}/") == []


def test_asset_content_is_denied_to_other_workspaces(solo) -> None:
    """An asset streams to its own workspace and is denied to every other member."""
    probe = cf.probe_workspace()
    data = cf.png_bytes(4, 4)
    with cf.api(probe["token"]) as client:
        asset = client.post(f"/workspaces/{probe['ws']}/assets",
                            files={"file": ("a.png", data, "image/png")}).json()
        own = client.get(f"/workspaces/{probe['ws']}/assets/{asset['id']}/content")
    with cf.api(solo) as client:
        other = client.get(f"/workspaces/{probe['ws']}/assets/{asset['id']}/content")
    assert own.status_code == 200 and own.content == data, cf.describe(own, "own asset streams")
    assert cf.denied(other), cf.describe(other, "another workspace is denied")


def test_bucket_objects_are_not_publicly_readable(owner) -> None:
    """A stored export cannot be read at the object store's own address without credentials."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    keys = cf.object_store().list(f"{cf.EXPORT_PREFIX}{ws}/")
    assert keys, "the seeded exports must be in the bucket"
    response = httpx.get(cf.storage_url(keys[0]), timeout=appclient.TIMEOUT)
    assert response.status_code in (401, 403), cf.describe(response, "anonymous reads are refused")
    project = cf.seeded_project(owner, ws, cf.DENIM_REMIX)
    with cf.api(owner) as client:
        texts = [client.get(f"/workspaces/{ws}/projects/{project['id']}/versions").text,
                 client.get("/shares/" + cf.SHARE_OPEN).text]
    for text in texts:
        assert "X-Amz-Signature" not in text and "x-amz-signature" not in text, text[:200]


def test_seeded_versions_have_one_ready_export_each(owner) -> None:
    """Each seeded version holds exactly one ready png export stored in the bucket."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    project = cf.seeded_project(owner, ws, cf.DENIM_REMIX)
    assert project["revision"] == 2 and project["remixed_from"] == cf.DENIM_UUID, project
    with cf.api(owner) as client:
        versions = cf.listing(client.get(f"/workspaces/{ws}/projects/{project['id']}/versions"))
        assert [v["number"] for v in versions] == [2, 1], versions
        for version in versions:
            jobs = cf.listing(client.get(f"/workspaces/{ws}/versions/{version['id']}/exports"))
            ready = [j for j in jobs if j["status"] == cf.STATUS_READY]
            assert len(ready) == 1 and ready[0]["object_key"].endswith(".png"), jobs
            assert ready[0]["object_key"] == f"{cf.EXPORT_PREFIX}{ws}/{ready[0]['id']}.png"
            assert cf.object_store().exists(ready[0]["object_key"]), ready[0]
            assert version["project_revision"] == version["number"], version


def test_seeded_library_rows_are_persisted() -> None:
    """The seeded reference rows are stored once each, with integer ids."""
    store = cf.backend()
    assert store.count(cf.TABLE_PLAN) == 5
    assert store.count(cf.TABLE_QUOTA) >= 34
    assert store.count(cf.TABLE_TEMPLATE) == 8
    assert store.count(cf.TABLE_BLOCK, kind="library") == 8
    assert store.count(cf.TABLE_CUSTOMER) == 25
    assert store.count(cf.TABLE_CUSTOMER, approved=False) == 1
    for email in cf.SEEDED_EMAILS:
        assert store.count(cf.TABLE_ACCOUNT, email=email) == 1, email
    for table in (cf.TABLE_ACCOUNT, cf.TABLE_PLAN, cf.TABLE_TEMPLATE, cf.TABLE_SHARE):
        row = store.rows(table, limit=1)[0]
        assert isinstance(row.get("id"), int), (table, row)
    solo = store.one(cf.TABLE_WORKSPACE, name=cf.WS_SOLO)
    assert solo and store.count(cf.TABLE_BLOCK, workspace_id=solo["id"]) == 4
    juniper = store.one(cf.TABLE_WORKSPACE, name=cf.WS_JUNIPER)
    assert store.count("brand_kit", workspace_id=juniper["id"]) == 4


def test_derived_figures_are_not_stored_columns() -> None:
    """Savings, approval states and seats used are computed, not stored."""
    query = ("SELECT table_name, column_name FROM information_schema.columns "
             "WHERE table_schema = 'public'")
    columns = {(r["table_name"], r["column_name"]) for r in cf.backend().query(query)}
    for table, column in ((cf.TABLE_PLAN, "annual_saving_percent"),
                          (cf.TABLE_PROJECT, "approval_status"),
                          (cf.TABLE_VERSION, "approval_state"),
                          (cf.TABLE_SUBSCRIPTION, "seats_used")):
        assert (table, column) not in columns, f"{table}.{column} must be derived"
    for table, column in ((cf.TABLE_SHARE, "passphrase_hash"), (cf.TABLE_COMMENT, "anchor_item_id"),
                          (cf.TABLE_CONSENT, "wording_shown"), (cf.TABLE_EXPORT, "request_key")):
        assert (table, column) in columns, f"{table}.{column} must exist"


def test_export_job_starts_rendering_with_its_flags() -> None:
    """An export starts rendering at progress 0 with watermark and variation flags."""
    probe = cf.probe_workspace()
    project = cf.make_project(probe["token"], probe["ws"])
    version = cf.freeze_version(probe["token"], probe["ws"], project["id"])
    assert version["number"] == 1 and version["project_revision"] == 1, version
    response = cf.request_export(probe["token"], probe["ws"], version["id"], 1280, 720)
    assert cf.accepted(response), cf.describe(response, "an export must start")
    job = response.json()
    assert job["status"] == cf.STATUS_RENDERING and job["progress"] == 0, job
    assert job["watermarked"] is True and job["is_variation"] is False, job


def test_frames_beyond_the_plan_ceiling_create_no_job() -> None:
    """A frame larger than the plan allows is refused on Free, Basic and Business."""
    free = cf.probe_workspace()
    basic = cf.probe_workspace(cf.PLAN_BASIC)
    business = cf.probe_workspace(cf.PLAN_BUSINESS)
    cases = ((free, 1920, 1080), (basic, 1921, 1080), (basic, 1920, 1081),
             (business, 2001, 1000), (business, 3840, 2160))
    for probe, width, height in cases:
        project = cf.make_project(probe["token"], probe["ws"], width, height)
        version = cf.freeze_version(probe["token"], probe["ws"], project["id"])
        response = cf.request_export(probe["token"], probe["ws"], version["id"], width, height)
        assert cf.is_client_error(response), cf.describe(response, f"{width}x{height} is refused")
        with cf.api(probe["token"]) as client:
            jobs = cf.listing(client.get(f"/workspaces/{probe['ws']}/versions/{version['id']}/exports"))
        assert jobs == [], jobs
    pro = cf.probe_workspace(cf.PLAN_PRO)
    project = cf.make_project(pro["token"], pro["ws"], 2000, 2000)
    version = cf.freeze_version(pro["token"], pro["ws"], project["id"])
    ok = cf.request_export(pro["token"], pro["ws"], version["id"], 2000, 2000)
    assert cf.accepted(ok) and ok.json()["watermarked"] is False, ok.text[:300]
    prores = cf.request_export(pro["token"], pro["ws"], version["id"], 2000, 2000, fmt="prores")
    assert cf.is_client_error(prores), cf.describe(prores, "prores is not offered")


def test_ready_export_file_is_stored_under_its_export_key() -> None:
    """A matching png becomes ready, lands at its export key and settles its unit."""
    probe = cf.probe_workspace(cf.PLAN_BASIC)
    project = cf.make_project(probe["token"], probe["ws"], 1280, 720)
    version = cf.freeze_version(probe["token"], probe["ws"], project["id"])
    job = cf.request_export(probe["token"], probe["ws"], version["id"], 640, 360).json()
    assert job["is_variation"] is True and job["watermarked"] is False, job
    assert cf.usage(probe["token"], probe["ws"], cf.METER_VARIATIONS)["used"] == 1
    with cf.api(probe["token"]) as client:
        client.patch(f"/workspaces/{probe['ws']}/exports/{job['id']}", json={"progress": 60})
        lower = client.patch(f"/workspaces/{probe['ws']}/exports/{job['id']}", json={"progress": 20})
    assert cf.is_client_error(lower) or cf.export_job(probe["token"], probe["ws"], job["id"])["progress"] == 60
    data = cf.png_bytes(640, 360)
    done = cf.upload_export(probe["token"], probe["ws"], job["id"], data, "image/png")
    assert cf.accepted(done), cf.describe(done, "a matching file must be accepted")
    ready = cf.export_job(probe["token"], probe["ws"], job["id"])
    key = f"{cf.EXPORT_PREFIX}{probe['ws']}/{job['id']}.png"
    assert ready["status"] == cf.STATUS_READY and ready["object_key"] == key, ready
    assert ready["byte_size"] == len(data), ready
    assert cf.object_store().exists(key), f"{key} must be in the bucket"
    with cf.api(probe["token"]) as client:
        stream = client.get(f"/workspaces/{probe['ws']}/exports/{job['id']}/file")
    assert stream.status_code == 200 and stream.content == data, cf.describe(stream, "file streams")
    assert cf.usage(probe["token"], probe["ws"], cf.METER_VARIATIONS)["used"] == 1
    assert cf.usage(probe["token"], probe["ws"], cf.METER_STORAGE)["used"] == len(data)
    again = cf.upload_export(probe["token"], probe["ws"], job["id"], data, "image/png")
    assert cf.is_client_error(again), cf.describe(again, "a second upload must be refused")
    assert cf.usage(probe["token"], probe["ws"], cf.METER_VARIATIONS)["used"] == 1
    assert cf.object_store().list(f"{cf.EXPORT_PREFIX}{probe['ws']}/") == [key]


def test_repeated_request_key_returns_one_job() -> None:
    """The same request key, sent twice or twice at once, yields one job and one unit."""
    probe = cf.probe_workspace(cf.PLAN_BASIC)
    project = cf.make_project(probe["token"], probe["ws"])
    version = cf.freeze_version(probe["token"], probe["ws"], project["id"])
    key = "probe-key-" + cf.unique_suffix()
    first = cf.request_export(probe["token"], probe["ws"], version["id"], 320, 180, key=key)
    second = cf.request_export(probe["token"], probe["ws"], version["id"], 320, 180, key=key)
    assert first.json()["id"] == second.json()["id"], (first.text[:200], second.text[:200])
    together = "probe-key-" + cf.unique_suffix()
    results = cf.run_together(
        lambda: cf.request_export(probe["token"], probe["ws"], version["id"], 480, 270, key=together),
        lambda: cf.request_export(probe["token"], probe["ws"], version["id"], 480, 270, key=together))
    ids = {r.json()["id"] for r in results if cf.accepted(r)}
    assert len(ids) == 1, [r.text[:120] for r in results]
    assert cf.backend().count(cf.TABLE_EXPORT, request_key=together) == 1
    assert cf.usage(probe["token"], probe["ws"], cf.METER_VARIATIONS)["used"] == 2


def test_mismatched_export_file_fails_and_releases_the_unit() -> None:
    """A file with the wrong signature or size fails the job, stores nothing, costs nothing."""
    probe = cf.probe_workspace(cf.PLAN_BASIC)
    project = cf.make_project(probe["token"], probe["ws"])
    version = cf.freeze_version(probe["token"], probe["ws"], project["id"])
    wrong_size = cf.request_export(probe["token"], probe["ws"], version["id"], 640, 360).json()
    response = cf.upload_export(probe["token"], probe["ws"], wrong_size["id"],
                                cf.png_bytes(641, 360), "image/png")
    failed = cf.export_job(probe["token"], probe["ws"], wrong_size["id"])
    assert failed["status"] == cf.STATUS_FAILED and failed["failure_reason"], (response.text[:200], failed)
    wrong_bytes = cf.request_export(probe["token"], probe["ws"], version["id"], 640, 360, fmt="gif").json()
    cf.upload_export(probe["token"], probe["ws"], wrong_bytes["id"], cf.png_bytes(640, 360), "image/gif")
    assert cf.export_job(probe["token"], probe["ws"], wrong_bytes["id"])["status"] == cf.STATUS_FAILED
    assert cf.object_store().list(f"{cf.EXPORT_PREFIX}{probe['ws']}/") == []
    assert cf.usage(probe["token"], probe["ws"], cf.METER_VARIATIONS)["used"] == 0


def test_gif_and_mp4_exports_are_accepted_by_their_headers() -> None:
    """A gif of the right size and an mp4 with its ftyp box both become ready."""
    probe = cf.probe_workspace()
    project = cf.make_project(probe["token"], probe["ws"], 640, 360)
    version = cf.freeze_version(probe["token"], probe["ws"], project["id"])
    gif = cf.request_export(probe["token"], probe["ws"], version["id"], 640, 360, fmt="gif").json()
    mp4 = cf.request_export(probe["token"], probe["ws"], version["id"], 640, 360, fmt="mp4").json()
    cf.upload_export(probe["token"], probe["ws"], gif["id"], cf.gif_bytes(640, 360), "image/gif")
    cf.upload_export(probe["token"], probe["ws"], mp4["id"], cf.mp4_bytes(), "video/mp4")
    for job, ext in ((gif, "gif"), (mp4, "mp4")):
        ready = cf.export_job(probe["token"], probe["ws"], job["id"])
        assert ready["status"] == cf.STATUS_READY, ready
        assert ready["object_key"].endswith("." + ext), ready


def test_failed_export_costs_nothing_and_queue_positions_count() -> None:
    """The fail action releases a unit, and queue positions count earlier rendering jobs."""
    probe = cf.probe_workspace(cf.PLAN_BASIC)
    project = cf.make_project(probe["token"], probe["ws"])
    version = cf.freeze_version(probe["token"], probe["ws"], project["id"])
    first = cf.request_export(probe["token"], probe["ws"], version["id"], 200, 200).json()
    second = cf.request_export(probe["token"], probe["ws"], version["id"], 300, 300).json()
    assert cf.export_job(probe["token"], probe["ws"], first["id"])["queue_position"] == 1
    assert cf.export_job(probe["token"], probe["ws"], second["id"])["queue_position"] == 2
    assert cf.export_job(probe["token"], probe["ws"], first["id"])["message"] == cf.MSG_RENDERING
    assert cf.usage(probe["token"], probe["ws"], cf.METER_VARIATIONS)["used"] == 2
    response = cf.fail_export(probe["token"], probe["ws"], first["id"])
    assert cf.accepted(response), cf.describe(response, "fail must succeed")
    failed = cf.export_job(probe["token"], probe["ws"], first["id"])
    assert failed["status"] == cf.STATUS_FAILED and failed["message"] == cf.MSG_EXPORT_FAILED, failed
    assert cf.export_job(probe["token"], probe["ws"], second["id"])["queue_position"] == 1
    assert cf.usage(probe["token"], probe["ws"], cf.METER_VARIATIONS)["used"] == 1
    rows = cf.backend().rows(cf.TABLE_USAGE, workspace_id=probe["ws"])
    assert {r["state"] for r in rows} <= {"reserved", "settled", "released"}, rows


def test_removed_members_rendering_export_fails_and_is_released() -> None:
    """Removing a member fails the export they left rendering and releases its unit."""
    probe = cf.probe_workspace(cf.PLAN_PRO)
    guest = cf.join_workspace(probe["token"], probe["ws"])
    project = cf.make_project(guest["token"], probe["ws"], 640, 360)
    version = cf.freeze_version(guest["token"], probe["ws"], project["id"])
    done = cf.request_export(guest["token"], probe["ws"], version["id"], 640, 360).json()
    cf.upload_export(guest["token"], probe["ws"], done["id"], cf.png_bytes(640, 360), "image/png")
    pending = cf.request_export(guest["token"], probe["ws"], version["id"], 320, 180).json()
    assert cf.usage(probe["token"], probe["ws"], cf.METER_VARIATIONS)["used"] == 1
    member = cf.account_id(probe["token"], probe["ws"], guest["email"])
    with cf.api(probe["token"]) as client:
        client.delete(f"/workspaces/{probe['ws']}/members/{member}")
    assert cf.export_job(probe["token"], probe["ws"], pending["id"])["status"] == cf.STATUS_FAILED
    assert cf.usage(probe["token"], probe["ws"], cf.METER_VARIATIONS)["used"] == 0
    kept = cf.export_job(probe["token"], probe["ws"], done["id"])
    assert kept["status"] == cf.STATUS_READY and cf.object_store().exists(kept["object_key"])


def test_export_file_is_denied_to_non_members(solo) -> None:
    """A ready export file never streams to a member of another workspace."""
    probe = cf.probe_workspace()
    ready = cf.ready_version(probe["token"], probe["ws"])
    with cf.api(solo) as client:
        response = client.get(f"/workspaces/{probe['ws']}/exports/{ready['export']['id']}/file")
    assert cf.denied(response), cf.describe(response, "non-members are denied")


def test_share_requires_a_ready_export(bench) -> None:
    """A version with no ready export cannot be shared or sent for approval."""
    ws = cf.workspace_id(bench, cf.WS_BENCH)
    project = cf.seeded_project(bench, ws, cf.BENCH_PROMO)
    with cf.api(bench) as client:
        vid = cf.listing(client.get(f"/workspaces/{ws}/projects/{project['id']}/versions"))[-1]["id"]
    before = cf.backend().count(cf.TABLE_SHARE)
    share = cf.create_share(bench, ws, vid)
    approval = cf.request_approval(bench, ws, vid, [cf.probe_address(cf.unique_suffix())])
    assert cf.is_client_error(share), cf.describe(share, "an unexported version is not shared")
    assert cf.message_of(share) == cf.MSG_SHARE_NEEDS_EXPORT, share.text[:300]
    assert cf.is_client_error(approval), cf.describe(approval, "an unexported version is not sent")
    assert cf.backend().count(cf.TABLE_SHARE) == before


def test_share_creation_returns_token_url_and_message() -> None:
    """A share returns a sixteen-character token, its url and the right sentence."""
    probe = cf.probe_workspace()
    ready = cf.ready_version(probe["token"], probe["ws"])
    open_share = cf.create_share(probe["token"], probe["ws"], ready["version"]["id"])
    named = cf.create_share(probe["token"], probe["ws"], ready["version"]["id"],
                            recipients=[cf.probe_address(cf.unique_suffix())])
    body = cf.body_of(open_share)
    assert cf.accepted(open_share), cf.describe(open_share, "a share must create")
    token = body.get("token", "")
    assert len(token) == 16 and token.isalnum(), body
    assert body.get("url") == "/s/" + token and body.get("message") == cf.MSG_SHARE_OPEN, body
    assert cf.body_of(named).get("message") == cf.MSG_SHARE_NAMED, named.text[:300]
    page = cf.fetch_document("/s/" + token)
    assert page.status_code == 200, cf.describe(page, "the share page must render")
    views = cf.poll_until(lambda: cf.listing(cf.api(probe["token"]).get(
        f"/workspaces/{probe['ws']}/shares/{body['id']}/views")))
    assert views and views[0].get("route") == "/s/" + token, views
    with cf.share_client() as client:
        posted = client.post("/shares/" + token + "/comments", json={"at_ms": 0, "body": "probe note"})
    assert cf.accepted(posted), cf.describe(posted, "comments on must accept a viewer comment")
    row = cf.backend().one(cf.TABLE_SHARE, token=token)
    assert row and row.get("id") == body["id"], row


def test_share_download_is_denied_when_download_is_off() -> None:
    """The download route refuses a share whose download is off; the stream still plays."""
    with cf.share_client() as client:
        info = client.get("/shares/" + cf.SHARE_OPEN)
        stream = client.get("/shares/" + cf.SHARE_OPEN + "/stream")
        download = client.get("/shares/" + cf.SHARE_OPEN + "/download")
    assert info.status_code == 200 and cf.body_of(info).get("allow_download") is False, info.text
    assert stream.status_code == 200 and stream.content.startswith(b"\x89PNG"), cf.describe(
        stream, "the open share must play")
    assert cf.is_client_error(download), cf.describe(download, "download must be refused")
    assert not download.content.startswith(b"\x89PNG"), "no file bytes may leave"


def test_share_shows_the_version_it_was_sent() -> None:
    """The seeded share of version 1 still shows version 1 with the superseded notice."""
    with cf.share_client() as client:
        info = cf.body_of(client.get("/shares/" + cf.SHARE_OPEN))
    assert info.get("version_number") == 1 and info.get("superseded") is True, info
    assert info.get("message") == cf.MSG_SUPERSEDED, info
    assert cf.MSG_SUPERSEDED in cf.page_text(cf.fetch_document("/s/" + cf.SHARE_OPEN).text)
    views = cf.backend().count(cf.TABLE_SHARE_VIEW,
                               share_id=cf.backend().one(cf.TABLE_SHARE, token=cf.SHARE_OPEN)["id"])
    assert views >= 3, views


def test_closed_superseded_share_serves_no_media() -> None:
    """With superseded shares closed, an older version's share answers the replaced sentence."""
    probe = cf.probe_workspace()
    ready = cf.ready_version(probe["token"], probe["ws"])
    share = cf.body_of(cf.create_share(probe["token"], probe["ws"], ready["version"]["id"]))
    cf.freeze_version(probe["token"], probe["ws"], ready["project"]["id"])
    with cf.api(probe["token"]) as client:
        closed = client.patch(f"/workspaces/{probe['ws']}/projects/{ready['project']['id']}",
                              json={"superseded_shares": cf.SUPERSEDED_CLOSED})
    assert closed.status_code == 200, cf.describe(closed, "the setting must store")
    with cf.share_client() as client:
        info = client.get("/shares/" + share["token"])
        stream = client.get("/shares/" + share["token"] + "/stream")
    assert cf.message_of(info) == cf.MSG_REPLACED, info.text[:300]
    assert cf.is_client_error(stream), cf.describe(stream, "a replaced share serves no media")


def test_expired_or_revoked_shares_are_refused_everywhere() -> None:
    """An expired or revoked share answers its message and serves nothing."""
    with cf.share_client() as client:
        for path in ("", "/stream", "/download", "/comments"):
            response = client.get("/shares/" + cf.SHARE_EXPIRED + path)
            assert cf.is_client_error(response), cf.describe(response, "expired is refused")
        assert cf.message_of(client.get("/shares/" + cf.SHARE_EXPIRED)) == cf.MSG_EXPIRED
    page = cf.fetch_document("/s/" + cf.SHARE_EXPIRED)
    assert cf.MSG_EXPIRED in cf.page_text(page.text), "the expired page states its message"
    probe = cf.probe_workspace()
    ready = cf.ready_version(probe["token"], probe["ws"])
    share = cf.body_of(cf.create_share(probe["token"], probe["ws"], ready["version"]["id"]))
    with cf.api(probe["token"]) as client:
        client.delete(f"/workspaces/{probe['ws']}/shares/{share['id']}")
    with cf.share_client() as client:
        stream = client.get("/shares/" + share["token"] + "/stream")
    assert cf.is_client_error(stream), cf.describe(stream, "a revoked share serves nothing")


def test_passphrase_share_serves_nothing_until_unlocked() -> None:
    """The seeded passphrase share denies media until the right passphrase unlocks it."""
    with cf.share_client() as client:
        locked = client.get("/shares/" + cf.SHARE_PASSPHRASE_TOKEN + "/stream")
        wrong = client.post("/shares/" + cf.SHARE_PASSPHRASE_TOKEN + "/unlock",
                            json={"passphrase": "not-the-phrase"})
        right = client.post("/shares/" + cf.SHARE_PASSPHRASE_TOKEN + "/unlock",
                            json={"passphrase": cf.SHARE_PASSPHRASE})
    assert cf.is_client_error(locked), cf.describe(locked, "a locked share serves nothing")
    assert cf.is_client_error(wrong), cf.describe(wrong, "a wrong passphrase is denied")
    access = cf.body_of(right).get("access_token")
    assert access, cf.describe(right, "the right passphrase returns an access token")
    with cf.share_client(access) as client:
        stream = client.get("/shares/" + cf.SHARE_PASSPHRASE_TOKEN + "/stream")
        download = client.get("/shares/" + cf.SHARE_PASSPHRASE_TOKEN + "/download")
        comment = client.post("/shares/" + cf.SHARE_PASSPHRASE_TOKEN + "/comments",
                              json={"at_ms": 100, "body": "probe"})
    assert stream.status_code == 200 and stream.content.startswith(b"\x89PNG"), stream.text[:100]
    assert download.status_code == 200, cf.describe(download, "download on must serve")
    assert "attachment" in download.headers.get("content-disposition", "").lower()
    assert cf.is_client_error(comment), cf.describe(comment, "comments off must refuse")
    with cf.share_client() as client:
        query = client.get("/shares/" + cf.SHARE_PASSPHRASE_TOKEN + "/stream",
                           params={"access": access})
    assert query.status_code == 200, cf.describe(query, "the access query value is accepted")


def test_repeated_wrong_passphrases_lock_the_share() -> None:
    """After five wrong passphrases the right one is refused too."""
    probe = cf.probe_workspace()
    ready = cf.ready_version(probe["token"], probe["ws"])
    phrase = "probe-phrase-" + cf.unique_suffix()
    share = cf.body_of(cf.create_share(probe["token"], probe["ws"], ready["version"]["id"],
                                       passphrase=phrase))
    with cf.share_client() as client:
        for _ in range(5):
            client.post("/shares/" + share["token"] + "/unlock", json={"passphrase": "wrong-one"})
        locked = client.post("/shares/" + share["token"] + "/unlock", json={"passphrase": phrase})
    assert cf.is_client_error(locked), cf.describe(locked, "the share must be locked")
    assert not cf.body_of(locked).get("access_token"), locked.text[:200]
    row = cf.backend().one(cf.TABLE_SHARE, token=share["token"])
    assert row["passphrase_hash"] and phrase not in str(row["passphrase_hash"]), row


def test_recipient_share_is_served_only_to_named_accounts(reviewer, second_reviewer) -> None:
    """The recipients share plays for its named reviewer and is denied to everyone else."""
    with cf.share_client() as client:
        anonymous = client.get("/shares/" + cf.SHARE_NAMED + "/stream")
    with cf.share_client(second_reviewer) as client:
        stranger = client.get("/shares/" + cf.SHARE_NAMED + "/stream")
    with cf.share_client(reviewer) as client:
        named = client.get("/shares/" + cf.SHARE_NAMED + "/stream")
        download = client.get("/shares/" + cf.SHARE_NAMED + "/download")
    assert cf.denied(anonymous), cf.describe(anonymous, "anonymous is denied")
    assert cf.denied(stranger), cf.describe(stranger, "an unnamed account is denied")
    assert named.status_code == 200, cf.describe(named, "the named reviewer is served")
    assert cf.is_client_error(download), cf.describe(download, "download off still refuses")


def test_carried_comments_resolve_against_the_newer_version(owner) -> None:
    """Seeded comments on version 1 follow their item into version 2 or say they were cut."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    project = cf.seeded_project(owner, ws, cf.DENIM_REMIX)
    with cf.api(owner) as client:
        versions = {v["number"]: v for v in cf.listing(
            client.get(f"/workspaces/{ws}/projects/{project['id']}/versions"))}
        comments = cf.listing(client.get(f"/workspaces/{ws}/versions/{versions[2]['id']}/comments"))
        first = cf.listing(client.get(f"/workspaces/{ws}/versions/{versions[1]['id']}/comments"))
    by_body = {c["body"]: c for c in comments}
    glow, hold = by_body[cf.COMMENT_GLOW], by_body[cf.COMMENT_HOLD]
    assert glow["state"] == cf.COMMENT_ANCHORED and glow["at_ms"] == 3000, glow
    assert hold["state"] == cf.COMMENT_ORPHANED and hold["at_ms"] is None, hold
    assert hold.get("note") == cf.MSG_ORPHANED, hold
    original = {c["body"]: c for c in first}
    assert original[cf.COMMENT_GLOW]["at_ms"] == 2000 and original[cf.COMMENT_HOLD]["at_ms"] == 12000
    assert all(c.get("author_email") == cf.REVIEWER_EMAIL for c in (glow, hold))


def test_comment_anchoring_follows_the_item() -> None:
    """A comment anchors to the item under its moment, and an empty moment is unanchored."""
    probe = cf.probe_workspace()
    ready = cf.ready_version(probe["token"], probe["ws"])
    pid, vid = ready["project"]["id"], ready["version"]["id"]
    glow = cf.library_block(cf.BLOCK_GLOW)
    saved = cf.save_timeline(probe["token"], probe["ws"], pid, 1,
                             cf.timeline_of([cf.glow_item("anchor-1", 1000, 2000, glow)]))
    assert saved.status_code == 200, saved.text[:200]
    v2 = cf.freeze_version(probe["token"], probe["ws"], pid)
    with cf.api(probe["token"]) as client:
        client.post(f"/workspaces/{probe['ws']}/versions/{v2['id']}/comments",
                    json={"at_ms": 1500, "body": "on the glow"})
        client.post(f"/workspaces/{probe['ws']}/versions/{v2['id']}/comments",
                    json={"at_ms": 5000, "body": "on nothing"})
    moved = cf.save_timeline(probe["token"], probe["ws"], pid, 2,
                             cf.timeline_of([cf.glow_item("anchor-1", 2000, 2000, glow)]))
    assert moved.status_code == 200, moved.text[:200]
    v3 = cf.freeze_version(probe["token"], probe["ws"], pid)
    with cf.api(probe["token"]) as client:
        rows = {c["body"]: c for c in cf.listing(
            client.get(f"/workspaces/{probe['ws']}/versions/{v3['id']}/comments"))}
    assert rows["on the glow"]["state"] == cf.COMMENT_ANCHORED and rows["on the glow"]["at_ms"] == 2500
    assert rows["on nothing"]["state"] == cf.COMMENT_UNANCHORED and rows["on nothing"]["at_ms"] == 5000
    with cf.api(probe["token"]) as client:
        frozen = cf.body_of(client.get(f"/workspaces/{probe['ws']}/versions/{v2['id']}"))
    assert frozen["timeline"]["tracks"][0]["items"][0]["start_ms"] == 1000, frozen
    stored = cf.backend().one(cf.TABLE_COMMENT, body="on the glow", version_id=v2["id"])
    assert stored["anchor_item_id"] == "anchor-1" and stored["anchor_offset_ms"] == 500, stored
    assert vid != v2["id"]


def test_approval_request_is_idempotent_and_reports_waiting() -> None:
    """Two reviewers make two pending requests once, with the waiting sentence and invites."""
    probe = cf.probe_workspace()
    ready = cf.ready_version(probe["token"], probe["ws"])
    vid = ready["version"]["id"]
    emails = [cf.probe_address(cf.unique_suffix()) for _ in range(2)]
    first = cf.request_approval(probe["token"], probe["ws"], vid, emails)
    again = cf.request_approval(probe["token"], probe["ws"], vid, emails)
    body = cf.body_of(first)
    assert cf.accepted(first), cf.describe(first, "approval must be requested")
    assert body.get("approval_state") == cf.STATE_PENDING and body.get("waiting_on") == 2, body
    assert body.get("message") == cf.MSG_WAIT_TWO, body
    assert cf.accepted(again) or cf.is_client_error(again)
    assert cf.backend().count(cf.TABLE_APPROVAL, version_id=vid) == 2
    with cf.api(probe["token"]) as client:
        rows = cf.listing(client.get(f"/workspaces/{probe['ws']}/versions/{vid}/approval-requests"))
    assert all(r["state"] == cf.STATE_PENDING and "/review/invite/" in r["invite_url"] for r in rows)
    single = cf.request_approval(probe["token"], probe["ws"], cf.ready_version(
        probe["token"], probe["ws"])["version"]["id"], [emails[0]])
    assert cf.message_of(single) == cf.MSG_WAIT_ONE, single.text[:200]


def test_review_invite_creates_a_reviewer_without_a_seat() -> None:
    """A review invitation creates a reviewer who takes no seat and sees one version."""
    probe = cf.probe_workspace(cf.PLAN_PRO)
    ready = cf.ready_version(probe["token"], probe["ws"])
    suffix = cf.unique_suffix()
    email = cf.probe_address(suffix)
    before = cf.subscription(probe["token"], probe["ws"])
    cf.request_approval(probe["token"], probe["ws"], ready["version"]["id"], [email])
    with cf.api(probe["token"]) as client:
        row = cf.listing(client.get(
            f"/workspaces/{probe['ws']}/versions/{ready['version']['id']}/approval-requests"))[0]
    accepted = cf.accept_review_invite(row["invite_url"], suffix)
    assert accepted.get("role") == cf.ROLE_REVIEWER and accepted.get("access_token"), accepted
    after = cf.subscription(probe["token"], probe["ws"])
    assert (after["seats"], after["seats_used"]) == (before["seats"], before["seats_used"])
    with cf.api(accepted["access_token"]) as client:
        reviews = cf.listing(client.get("/reviews"))
        blocked = client.get(f"/workspaces/{probe['ws']}/projects")
    assert [r["version_id"] for r in reviews] == [ready["version"]["id"]], reviews
    assert cf.denied(blocked), cf.describe(blocked, "a reviewer is denied")
    assert cf.backend().one(cf.TABLE_ACCOUNT, email=email)["role"] == cf.ROLE_REVIEWER


def test_decisions_are_recorded_once_and_derive_the_state() -> None:
    """Decisions are final, others are denied, and the version state follows them."""
    probe = cf.probe_workspace()
    ready = cf.ready_version(probe["token"], probe["ws"])
    vid, pid = ready["version"]["id"], ready["project"]["id"]
    reviewers = []
    for _ in range(2):
        suffix = cf.unique_suffix()
        cf.request_approval(probe["token"], probe["ws"], vid, [cf.probe_address(suffix)])
        reviewers.append(suffix)
    with cf.api(probe["token"]) as client:
        rows = cf.listing(client.get(f"/workspaces/{probe['ws']}/versions/{vid}/approval-requests"))
        state = cf.body_of(client.get(f"/workspaces/{probe['ws']}/versions/{vid}"))["approval_state"]
    assert state == cf.STATE_PENDING, state
    tokens = {}
    for row in rows:
        suffix = [s for s in reviewers if s in row["reviewer_email"]][0]
        tokens[row["id"]] = cf.accept_review_invite(row["invite_url"], suffix)["access_token"]
    first_id, second_id = rows[0]["id"], rows[1]["id"]
    with cf.api(tokens[second_id]) as client:
        stolen = client.post(f"/reviews/{first_id}/decision", json={"decision": cf.STATE_APPROVED})
    assert cf.denied(stolen), cf.describe(stolen, "another reviewer is denied")
    with cf.api(tokens[first_id]) as client:
        ok = client.post(f"/reviews/{first_id}/decision", json={"decision": cf.STATE_APPROVED})
        twice = client.post(f"/reviews/{first_id}/decision", json={"decision": cf.STATE_CHANGES})
    assert cf.accepted(ok) and cf.is_client_error(twice), (ok.text[:200], twice.text[:200])
    with cf.api(probe["token"]) as client:
        state = cf.body_of(client.get(f"/workspaces/{probe['ws']}/versions/{vid}"))["approval_state"]
    assert state == cf.STATE_PENDING, state
    with cf.api(tokens[second_id]) as client:
        client.post(f"/reviews/{second_id}/decision", json={"decision": cf.STATE_APPROVED})
    assert cf.get_project(probe["token"], probe["ws"], pid)["approval_status"] == cf.STATE_APPROVED
    with cf.api(probe["token"]) as client:
        state = cf.body_of(client.get(f"/workspaces/{probe['ws']}/versions/{vid}"))["approval_state"]
    assert state == cf.STATE_APPROVED, state
    glow = cf.library_block(cf.BLOCK_GLOW)
    saved = cf.save_timeline(probe["token"], probe["ws"], pid, 1,
                             cf.timeline_of([cf.glow_item("late-1", 0, 1000, glow)]))
    assert saved.status_code == 200, saved.text[:200]
    assert cf.get_project(probe["token"], probe["ws"], pid)["approval_status"] == cf.PROJECT_OUTDATED
    with cf.api(probe["token"]) as client:
        state = cf.body_of(client.get(f"/workspaces/{probe['ws']}/versions/{vid}"))["approval_state"]
    assert state == cf.STATE_APPROVED, state


def test_changes_requested_marks_the_version(owner) -> None:
    """One request asking for changes marks the version changes_requested."""
    probe = cf.probe_workspace()
    ready = cf.ready_version(probe["token"], probe["ws"])
    vid = ready["version"]["id"]
    with cf.api(probe["token"]) as client:
        fresh = cf.body_of(client.get(f"/workspaces/{probe['ws']}/versions/{vid}"))
    assert fresh["approval_state"] == cf.STATE_NOT_REQUESTED, fresh
    suffix = cf.unique_suffix()
    cf.request_approval(probe["token"], probe["ws"], vid, [cf.probe_address(suffix)])
    with cf.api(probe["token"]) as client:
        row = cf.listing(client.get(f"/workspaces/{probe['ws']}/versions/{vid}/approval-requests"))[0]
    token = cf.accept_review_invite(row["invite_url"], suffix)["access_token"]
    with cf.api(token) as client:
        client.post(f"/reviews/{row['id']}/decision",
                    json={"decision": cf.STATE_CHANGES, "note": "tighten the end"})
    with cf.api(probe["token"]) as client:
        state = cf.body_of(client.get(f"/workspaces/{probe['ws']}/versions/{vid}"))["approval_state"]
    assert state == cf.STATE_CHANGES, state
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    seeded = cf.seeded_project(owner, ws, cf.DENIM_REMIX)
    assert seeded["approval_status"] == cf.STATE_PENDING, seeded


def test_notifications_are_sent_once_per_event() -> None:
    """A retried request notifies a reviewer once, and a decision notifies the requester once."""
    probe = cf.probe_workspace()
    ready = cf.ready_version(probe["token"], probe["ws"])
    vid = ready["version"]["id"]
    suffix = cf.unique_suffix()
    email = cf.probe_address(suffix)
    cf.request_approval(probe["token"], probe["ws"], vid, [email])
    cf.request_approval(probe["token"], probe["ws"], vid, [email])
    with cf.api(probe["token"]) as client:
        row = cf.listing(client.get(f"/workspaces/{probe['ws']}/versions/{vid}/approval-requests"))[0]
    token = cf.accept_review_invite(row["invite_url"], suffix)["access_token"]
    with cf.api(token) as client:
        mine = cf.listing(client.get("/notifications"))
        client.post(f"/reviews/{row['id']}/decision", json={"decision": cf.STATE_APPROVED})
        client.post(f"/reviews/{row['id']}/decision", json={"decision": cf.STATE_APPROVED})
    assert len(mine) == 1, mine
    with cf.api(probe["token"]) as client:
        theirs = cf.listing(client.get("/notifications"))
    assert len(theirs) == 1, theirs
    assert cf.backend().count(cf.TABLE_NOTIFICATION, account_email=email) == 1


def test_reviews_list_only_addressed_requests(reviewer, second_reviewer) -> None:
    """The seeded reviewer sees the two Denim Drop remix requests; the second sees none."""
    with cf.api(reviewer) as client:
        mine = cf.listing(client.get("/reviews"))
    seeded = [r for r in mine if r.get("project_name") == cf.DENIM_REMIX]
    assert sorted((r["version_number"], r["state"]) for r in seeded)[:2] == [
        (1, cf.STATE_APPROVED), (2, cf.STATE_PENDING)], seeded
    with cf.api(second_reviewer) as client:
        theirs = cf.listing(client.get("/reviews"))
    assert theirs == [], theirs


def test_reviewers_cannot_open_workspace_endpoints(reviewer, second_reviewer, owner) -> None:
    """Every workspace endpoint denies a reviewer, and nothing changes."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    before = cf.backend().count(cf.TABLE_PROJECT, workspace_id=ws)
    for token in (reviewer, second_reviewer):
        with cf.api(token) as client:
            responses = [client.get(f"/workspaces/{ws}/projects"),
                         client.get(f"/workspaces/{ws}/blocks"),
                         client.get(f"/workspaces/{ws}/brand-kits"),
                         client.get(f"/workspaces/{ws}/assets"),
                         client.get(f"/workspaces/{ws}/members"),
                         client.get(f"/workspaces/{ws}/usage"),
                         client.post(f"/workspaces/{ws}/projects",
                                     json={"name": "Intrude", "canvas_width": 100,
                                           "canvas_height": 100, "fps": 30, "duration_ms": 2000}),
                         client.post(f"/workspaces/{ws}/templates/{cf.DENIM_UUID}/remix")]
            listed = client.get("/workspaces")
            assert cf.denied(listed) or listed.json() == [], listed.text[:200]
        for response in responses:
            assert cf.denied(response), cf.describe(response, "a reviewer is denied")
    assert cf.backend().count(cf.TABLE_PROJECT, workspace_id=ws) == before


def test_reviewer_cannot_stream_an_unaddressed_version(reviewer, second_reviewer) -> None:
    """A reviewer streams an addressed version; another reviewer cannot."""
    with cf.api(reviewer) as client:
        mine = [r for r in cf.listing(client.get("/reviews"))
                if r.get("project_name") == cf.DENIM_REMIX]
        own = client.get(f"/reviews/{mine[0]['id']}/stream")
    with cf.api(second_reviewer) as client:
        other = client.get(f"/reviews/{mine[0]['id']}/stream")
        detail = client.get(f"/reviews/{mine[0]['id']}")
    assert own.status_code == 200 and own.content.startswith(b"\x89PNG"), own.text[:100]
    assert cf.denied(other), cf.describe(other, "an unaddressed reviewer is denied")
    assert cf.denied(detail), cf.describe(detail, "the request detail is denied")


def test_members_cannot_reach_other_workspaces(owner, solo) -> None:
    """A member of one workspace is denied every endpoint of another, and nothing changes."""
    juniper = cf.workspace_id(owner, cf.WS_JUNIPER)
    project = cf.seeded_project(owner, juniper, cf.DENIM_REMIX)
    before = cf.get_project(owner, juniper, project["id"])["revision"]
    with cf.api(solo) as client:
        responses = [client.get(f"/workspaces/{juniper}/projects/{project['id']}"),
                     client.put(f"/workspaces/{juniper}/projects/{project['id']}/timeline",
                                json={"base_revision": before, "timeline": {"tracks": []}}),
                     client.get(f"/workspaces/{juniper}/subscription"),
                     client.get(f"/workspaces/{juniper}/shares")]
    for response in responses:
        assert cf.denied(response), cf.describe(response, "another workspace is denied")
    assert cf.get_project(owner, juniper, project["id"])["revision"] == before


def test_list_endpoints_return_arrays_with_utc_timestamps(owner) -> None:
    """List endpoints answer top-level arrays whose timestamps are UTC and end in Z."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    with cf.api(owner) as client:
        for path in ("/plans", "/templates", "/workspaces", f"/workspaces/{ws}/charges",
                     f"/workspaces/{ws}/projects", f"/workspaces/{ws}/shares"):
            response = client.get(path)
            assert isinstance(response.json(), list), cf.describe(response, "must be an array")
        for row in cf.listing(client.get(f"/workspaces/{ws}/charges")):
            assert str(row["created_at"]).endswith("Z"), row


def test_invalid_calls_are_client_errors_with_a_message(owner) -> None:
    """A malformed body is refused as a client error naming what was wrong."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    with cf.api(owner) as client:
        response = client.post(f"/workspaces/{ws}/projects", json={"name": ""})
        broken = client.post("/auth/login", content=b"{not json",
                             headers={"Content-Type": "application/json"})
    for bad in (response, broken):
        assert cf.is_client_error(bad), cf.describe(bad, "a bad call is a client error")
        assert bad.text.strip(), cf.describe(bad, "the refusal must carry a message")


def test_store_and_bucket_hold_the_records_the_api_reports(owner) -> None:
    """What the API reports as usage and projects is what the store and bucket hold."""
    ws = cf.workspace_id(owner, cf.WS_JUNIPER)
    with cf.api(owner) as client:
        projects = cf.listing(client.get(f"/workspaces/{ws}/projects"))
    assert len(projects) == cf.backend().count(cf.TABLE_PROJECT, workspace_id=ws)
    balance = cf.backend().rows(cf.TABLE_METER, workspace_id=ws)
    assert balance, "meter balances must live in the store"
    for row in balance:
        if row.get("limit_value") is not None:
            assert row["used"] <= row["limit_value"], row
    sizes = sum(int(r.get("byte_size") or 0) for r in cf.backend().rows(cf.TABLE_ASSET, workspace_id=ws))
    ready = [r for r in cf.backend().rows(cf.TABLE_EXPORT, workspace_id=ws) if r.get("status") == cf.STATUS_READY]
    sizes += sum(int(r.get("byte_size") or 0) for r in ready)
    assert cf.usage(owner, ws, cf.METER_STORAGE)["used"] == sizes
    for job in ready:
        assert cf.object_store().exists(job["object_key"]), job
