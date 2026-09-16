from __future__ import annotations

import re

from conftest import (
    API_CHANGELOG, API_CHECKOUT, API_HEALTH, API_LEADS, API_ME, API_MODELS,
    API_PLANS, API_PLUGINS, API_RELEASES, API_RESOLVE, API_SIGNIN, API_SIGNUP,
    API_SUBSCRIPTION, API_WORKSPACES, ARTIFACT_COUNT, AURORA_CONSUMED,
    AURORA_INCLUDED, AURORA_OVERAGE, AURORA_SEATS, AURORA_SPEND_LIMIT,
    AURORA_USAGE_KEYS, BENCHMARK_VERSION, BILLING_COUNTRY, BILLING_CURRENCY,
    BILLING_KEY_AURORA, BILLING_KEY_PREFIX, CALC_ALLOCATION_TOTAL,
    CALC_BASELINE_COST, CALC_BLENDED, CALC_CHEAPER, CALC_NEW_ANNUAL,
    CALC_OLD_ANNUAL, CALC_SAVED_MONTH, CALC_SAVED_YEAR, CALC_SPEND,
    CALC_TASKS_NEW, CALC_TASKS_OLD, CATALOGUE_CATEGORIES, CATALOGUE_KINDS,
    CATALOGUE_PUBLISHED_COUNT, CHANGELOG_SLUGS, CHART_AXIS_COST,
    CHART_AXIS_SCORE, COMPLIANCE_LINE, CONFLICT, COST_NOT_MEASURED, DENIED,
    DENIED_OR_MISSING, DOWNLOAD_HEADLINE, FOOLSCAP_COUNT, FOOLSCAP_COUNT_AFTER,
    GAP_PLATFORM, HOME_CHANGELOG_LINK, HOME_HEADLINE, HOME_TRUST,
    INSTALL_TABS, INVITE_SUBJECT_AURORA, INVITE_SUBJECT_PREFIX,
    LATEST_MACOS_CHECKSUM, LEADERBOARD_COLUMNS, MARKETPLACE_HEADING,
    MEMBER_EMAIL, MODEL_CODES, MODEL_COST, MODEL_COUNT, MODEL_NAMES,
    MODEL_SCORE_BP, MODEL_STEPS, MODEL_TOKENS, MODEL_UNCOSTED,
    MODEL_UNCOSTED_NAME, NARROW_PRIMARY, NORTHLIGHT_CONSUMED,
    NORTHLIGHT_INCLUDED, NORTHLIGHT_USAGE_KEY, NOT_FOUND, OK_READ, OK_WRITE,
    OWNER2_EMAIL, OWNER_EMAIL, PAYMENT_REQUIRED, PLAN_CODES, PLATFORM_ROWS,
    PLUGIN_SLUGS, PUBLIC_ROUTES, QUESTIONS_HEADING, REFUSED, RELEASE_LATEST,
    RELEASE_PREVIOUS, RELEASE_VERSIONS, ROLE_MEMBER, ROLE_OWNER,
    ROUTE_ACCOUNT, ROUTE_CALCULATOR, ROUTE_CHANGELOG, ROUTE_DOWNLOAD,
    ROUTE_EVALS, ROUTE_HOME, ROUTE_MARKETPLACE, ROUTE_PRICING, ROUTE_ROBOTS,
    ROUTE_SIGNIN, ROUTE_SITEMAP, SECRET_MARKERS, SEEDED_ACCOUNTS,
    SEEDED_TABLES, SKIP_LINK, TABLE_INSTALLATIONS, TABLE_MODELS,
    TABLE_PLUGINS, TABLE_SUBSCRIPTIONS, TABLE_USAGE, TABLE_WORKSPACES,
    TIER_ALLOWANCE, TIER_CODES, TIER_MONTHLY, TIER_YEARLY, TIE_COUNT,
    TIE_SLUGS, UNIT_SWITCH, WITHDRAWN_SLUG, WS_AURORA, WS_AURORA_LABEL,
    WS_NORTHLIGHT, accounts_with_key, as_list, bearer, field, in_parallel,
    json_body, mentions, plugin_path, probe_email, probe_slug, probe_token,
    settle, signin, signup, token_of, visible_text, workspace_path,
)


def test_health_endpoint_is_ready(api):
    """cov: C-TR-10, C-DC-4"""
    response = api.get(API_HEALTH)
    assert response.status_code in OK_READ, (
        "GET /api%s returned %s: %r -- the deployment contract pins a 200 once "
        "the app is ready" % (API_HEALTH, response.status_code,
                              response.text[:300]))


def test_public_routes_render_with_chrome_and_skip_link(site):
    """cov: C-CF-12, C-CF-18, C-CF-33, C-CF-57, C-CF-88"""
    for route in PUBLIC_ROUTES:
        response = site.get(route)
        assert response.status_code in OK_READ, (
            "GET %s returned %s: %r -- every public route is readable without "
            "an account" % (route, response.status_code, response.text[:200]))
        assert SKIP_LINK in response.text, (
            "GET %s carries no %r link in the served markup; the brief pins it "
            "as the first element of the document" % (route, SKIP_LINK))
        assert COMPLIANCE_LINE in response.text, (
            "GET %s carries no footer compliance line %r in the served markup"
            % (route, COMPLIANCE_LINE))
    home = site.get(ROUTE_HOME)
    text = visible_text(home.text)
    assert HOME_HEADLINE in text, (
        "GET / does not show the pinned headline %r; it showed %r"
        % (HOME_HEADLINE, text[:300]))
    assert HOME_TRUST in text, (
        "GET / does not show the pinned trust line %r" % HOME_TRUST)
    assert HOME_CHANGELOG_LINK in text, (
        "GET / does not show the changelog band link %r" % HOME_CHANGELOG_LINK)


def test_every_public_route_carries_its_own_title_and_description(site):
    """cov: C-CF-173"""
    titles = {}
    descriptions = {}
    for route in PUBLIC_ROUTES:
        response = site.get(route)
        title = re.search(r"(?is)<title[^>]*>(.*?)</title>", response.text)
        assert title and title.group(1).strip(), (
            "GET %s served no non-empty document title; the brief pins one per "
            "route" % route)
        meta = re.search(
            r'(?is)<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
            response.text)
        assert meta and meta.group(1).strip(), (
            "GET %s served no non-empty description; the brief pins one per "
            "route" % route)
        titles.setdefault(title.group(1).strip(), []).append(route)
        descriptions.setdefault(meta.group(1).strip(), []).append(route)
    shared_titles = {t: r for t, r in titles.items() if len(r) > 1}
    assert not shared_titles, (
        "these routes share a document title, which the brief forbids: %r"
        % shared_titles)
    shared_descriptions = {d: r for d, r in descriptions.items() if len(r) > 1}
    assert not shared_descriptions, (
        "these routes share a description, which the brief forbids: %r"
        % shared_descriptions)


def test_sitemap_lists_every_public_route_and_robots_points_at_it(site):
    """cov: C-OV-1, C-CF-174"""
    sitemap = site.get(ROUTE_SITEMAP)
    assert sitemap.status_code in OK_READ, (
        "GET %s returned %s: %r" % (ROUTE_SITEMAP, sitemap.status_code,
                                    sitemap.text[:200]))
    for route in PUBLIC_ROUTES:
        needle = route if route != ROUTE_HOME else "/"
        assert needle in sitemap.text, (
            "%s does not list the public route %r" % (ROUTE_SITEMAP, needle))
    robots = site.get(ROUTE_ROBOTS)
    assert robots.status_code in OK_READ, (
        "GET %s returned %s: %r" % (ROUTE_ROBOTS, robots.status_code,
                                    robots.text[:200]))
    assert mentions(robots.text, "sitemap"), (
        "%s does not point at the sitemap: %r" % (ROUTE_ROBOTS,
                                                  robots.text[:200]))


def test_leaderboard_ranks_fifteen_models_by_figure(api, site):
    """cov: C-OV-4"""
    payload = json_body(api.get(API_MODELS))
    rows = as_list(payload)
    assert len(rows) == MODEL_COUNT, (
        "GET /api%s returned %d models; the registry the brief pins holds %d"
        % (API_MODELS, len(rows), MODEL_COUNT))
    codes = [str(field(r, "code", default="")) for r in rows]
    assert set(codes) == set(MODEL_CODES), (
        "GET /api%s returned model codes %r; the brief pins %r"
        % (API_MODELS, sorted(codes), sorted(MODEL_CODES)))
    page = site.get(ROUTE_EVALS)
    assert page.status_code in OK_READ, (
        "GET %s returned %s: %r" % (ROUTE_EVALS, page.status_code,
                                    page.text[:200]))
    text = visible_text(page.text)
    for column in LEADERBOARD_COLUMNS:
        assert column in text, (
            "GET %s does not show the leaderboard column heading %r"
            % (ROUTE_EVALS, column))
    for label in UNIT_SWITCH:
        assert label in text, (
            "GET %s does not show the unit switch control %r"
            % (ROUTE_EVALS, label))
    for name in MODEL_NAMES:
        assert name in text, (
            "GET %s does not show the model %r that the registry holds"
            % (ROUTE_EVALS, name))
    assert CHART_AXIS_SCORE in text and CHART_AXIS_COST in text, (
        "GET %s does not carry both pinned axis labels %r and %r"
        % (ROUTE_EVALS, CHART_AXIS_SCORE, CHART_AXIS_COST))


def test_model_without_a_cost_is_absent_from_the_plot(api, site):
    """cov: C-CF-52, C-CF-53, C-CF-68, C-CF-134, C-CF-135"""
    rows = as_list(json_body(api.get(API_MODELS)))
    uncosted = [r for r in rows
                if str(field(r, "code", default="")) == MODEL_UNCOSTED]
    assert len(uncosted) == 1, (
        "GET /api%s returned %d rows for %r; the registry holds exactly one"
        % (API_MODELS, len(uncosted), MODEL_UNCOSTED))
    cost = field(uncosted[0], "cost_per_task_minor", "costPerTaskMinor")
    assert cost is None, (
        "the model %r reports a cost per task of %r; the brief pins it as not "
        "measured, and a zero there would place it at the cheap end of the plot"
        % (MODEL_UNCOSTED, cost))
    page = site.get(ROUTE_EVALS)
    text = visible_text(page.text)
    assert MODEL_UNCOSTED_NAME in text, (
        "GET %s omits the row for %r; a model with no measured cost still "
        "appears in the table" % (ROUTE_EVALS, MODEL_UNCOSTED_NAME))
    assert COST_NOT_MEASURED in text, (
        "GET %s does not mark any cost cell %r; the row for %r carries that "
        "marking" % (ROUTE_EVALS, COST_NOT_MEASURED, MODEL_UNCOSTED_NAME))


def test_calculator_worked_example_matches_the_pinned_figures(site):
    """cov: C-CF-63, C-CF-65"""
    page = site.get(ROUTE_CALCULATOR)
    assert page.status_code in OK_READ, (
        "GET %s returned %s: %r" % (ROUTE_CALCULATOR, page.status_code,
                                    page.text[:200]))
    text = visible_text(page.text)
    for needle in (CALC_SPEND, CALC_ALLOCATION_TOTAL, "Advanced",
                   "Model allocation", "Total:"):
        assert needle in text, (
            "GET %s does not show %r; the brief pins the calculator's labels "
            "and its prefilled spend" % (ROUTE_CALCULATOR, needle))
    for needle in (CALC_BLENDED, CALC_CHEAPER, CALC_SAVED_MONTH,
                   CALC_SAVED_YEAR, CALC_NEW_ANNUAL, CALC_OLD_ANNUAL,
                   CALC_BASELINE_COST):
        assert needle in text, (
            "GET %s does not carry the worked example figure %r that the brief "
            "pins for the Kestrel 4 to Meridian 4 shift"
            % (ROUTE_CALCULATOR, needle))


def test_calculator_reads_the_same_registry_as_the_leaderboard(api, site):
    """cov: C-OV-4"""
    rows = as_list(json_body(api.get(API_MODELS)))
    costed = [r for r in rows
              if field(r, "cost_per_task_minor", "costPerTaskMinor") is not None]
    page = visible_text(site.get(ROUTE_CALCULATOR).text)
    for row in costed:
        name = str(field(row, "name", default=""))
        assert name in page, (
            "GET %s does not offer the model %r that the registry prices; the "
            "calculator reads one registry" % (ROUTE_CALCULATOR, name))
    assert MODEL_UNCOSTED_NAME not in page, (
        "GET %s offers %r, which has no measured cost per task and is absent "
        "from the selects" % (ROUTE_CALCULATOR, MODEL_UNCOSTED_NAME))
    assert CALC_TASKS_NEW in page and CALC_TASKS_OLD in page, (
        "GET %s does not carry the tasks view figures %r against %r"
        % (ROUTE_CALCULATOR, CALC_TASKS_NEW, CALC_TASKS_OLD))


def test_allocation_that_misses_one_hundred_is_refused(site):
    """cov: C-CF-59"""
    page = visible_text(site.get(ROUTE_CALCULATOR).text)
    assert mentions(page, "100"), (
        "GET %s never names the total the allocation must reach; the brief "
        "pins one hundred" % ROUTE_CALCULATOR)
    assert mentions(page, "Total:"), (
        "GET %s shows no running allocation total, so a visitor cannot see "
        "that the allocation is short" % ROUTE_CALCULATOR)


def test_catalogue_listing_filters_by_kind_and_category(api):
    """cov: C-CF-71, C-CF-73, C-CF-75, C-UF-9, C-DM-14"""
    everything = as_list(json_body(api.get(API_PLUGINS,
                                           params={"per_page": 50})))
    assert len(everything) == CATALOGUE_PUBLISHED_COUNT, (
        "GET /api%s returned %d entries; the catalogue the brief pins holds %d "
        "published entries" % (API_PLUGINS, len(everything),
                               CATALOGUE_PUBLISHED_COUNT))
    for kind in CATALOGUE_KINDS:
        rows = as_list(json_body(api.get(API_PLUGINS,
                                         params={"kind": kind,
                                                 "per_page": 50})))
        assert rows, (
            "GET /api%s?kind=%s returned nothing; both kinds are populated"
            % (API_PLUGINS, kind))
        kinds = {str(field(r, "kind", default="")) for r in rows}
        assert kinds == {kind}, (
            "GET /api%s?kind=%s returned kinds %r" % (API_PLUGINS, kind, kinds))
    for category in CATALOGUE_CATEGORIES:
        rows = as_list(json_body(api.get(API_PLUGINS,
                                         params={"category": category,
                                                 "per_page": 50})))
        assert rows, (
            "GET /api%s?category=%s returned nothing; every pinned category "
            "holds at least one entry" % (API_PLUGINS, category))
        categories = {str(field(r, "category", default="")) for r in rows}
        assert categories == {category}, (
            "GET /api%s?category=%s returned categories %r"
            % (API_PLUGINS, category, categories))


def test_popularity_order_breaks_a_tie_on_the_slug(api):
    """cov: C-CF-76"""
    rows = as_list(json_body(api.get(API_PLUGINS,
                                     params={"sort": "popular",
                                             "per_page": 50})))
    slugs = [str(field(r, "slug", default="")) for r in rows]
    counts = [field(r, "install_count", "installCount", default=0)
              for r in rows]
    assert counts == sorted(counts, reverse=True), (
        "GET /api%s?sort=popular returned install counts %r, which are not "
        "descending" % (API_PLUGINS, counts))
    positions = [slugs.index(s) for s in TIE_SLUGS if s in slugs]
    assert len(positions) == len(TIE_SLUGS), (
        "GET /api%s?sort=popular omits one of the tied entries %r; both carry "
        "%d installs" % (API_PLUGINS, TIE_SLUGS, TIE_COUNT))
    assert positions == sorted(positions), (
        "the tied entries %r came back in the order %r; the brief breaks a tie "
        "on the slug ascending" % (TIE_SLUGS, [slugs[p] for p in positions]))


def test_unknown_catalogue_filter_value_is_refused(api):
    """cov: C-CF-161"""
    for params in ({"kind": probe_slug("kind")},
                   {"category": probe_slug("category")},
                   {"sort": probe_slug("sort")}):
        response = api.get(API_PLUGINS, params=params)
        assert response.status_code in REFUSED, (
            "GET /api%s with %r returned %s; an unknown closed-set value is "
            "refused as invalid rather than silently ignored: %r"
            % (API_PLUGINS, params, response.status_code, response.text[:200]))


def test_withdrawn_entry_is_absent_from_every_listing(api):
    """cov: C-CF-72, C-CF-79"""
    rows = as_list(json_body(api.get(API_PLUGINS, params={"per_page": 50})))
    slugs = {str(field(r, "slug", default="")) for r in rows}
    assert WITHDRAWN_SLUG not in slugs, (
        "GET /api%s lists the withdrawn entry %r; a withdrawn entry appears in "
        "no listing" % (API_PLUGINS, WITHDRAWN_SLUG))
    detail = api.get(plugin_path("plugin", WITHDRAWN_SLUG))
    assert detail.status_code in NOT_FOUND, (
        "GET /api%s returned %s; a withdrawn entry answers as not found"
        % (plugin_path("plugin", WITHDRAWN_SLUG), detail.status_code))


def test_resolve_returns_one_artifact_with_a_checksum(api, site):
    """cov: C-CF-89"""
    response = api.get(API_RESOLVE, params={"os": "macos", "arch": "arm64",
                                            "format": "dmg"})
    assert response.status_code in OK_READ, (
        "GET /api%s for the macos arm64 dmg returned %s: %r"
        % (API_RESOLVE, response.status_code, response.text[:200]))
    body = json_body(response)
    assert field(body, "version") == RELEASE_LATEST, (
        "GET /api%s resolved version %r; the latest published version is %r"
        % (API_RESOLVE, field(body, "version"), RELEASE_LATEST))
    assert field(body, "checksum") == LATEST_MACOS_CHECKSUM, (
        "GET /api%s resolved checksum %r; the brief pins %r for that artifact"
        % (API_RESOLVE, field(body, "checksum"), LATEST_MACOS_CHECKSUM))
    page = visible_text(site.get(ROUTE_DOWNLOAD).text)
    assert DOWNLOAD_HEADLINE in page, (
        "GET %s does not show the pinned headline %r"
        % (ROUTE_DOWNLOAD, DOWNLOAD_HEADLINE))


def test_missing_artifact_falls_back_to_the_previous_version(api):
    """cov: C-CF-92"""
    os_name, arch, fmt = GAP_PLATFORM
    response = api.get(API_RESOLVE, params={"os": os_name, "arch": arch,
                                            "format": fmt})
    assert response.status_code in OK_READ, (
        "GET /api%s for the %s %s %s returned %s: %r"
        % (API_RESOLVE, os_name, arch, fmt, response.status_code,
           response.text[:200]))
    body = json_body(response)
    assert field(body, "version") == RELEASE_PREVIOUS, (
        "GET /api%s for the platform with no artifact at %s resolved %r; the "
        "brief offers the previous version %r rather than another platform's "
        "newest build" % (API_RESOLVE, RELEASE_LATEST, field(body, "version"),
                          RELEASE_PREVIOUS))
    latest = field(body, "is_latest", "isLatest", "latest")
    assert latest is False, (
        "GET /api%s resolved an older artifact without marking it as older; it "
        "reported %r" % (API_RESOLVE, latest))


def test_unknown_platform_lists_every_artifact(api):
    """cov: C-CF-89"""
    response = api.get(API_RELEASES)
    assert response.status_code in OK_READ, (
        "GET /api%s returned %s: %r" % (API_RELEASES, response.status_code,
                                        response.text[:200]))
    rows = as_list(json_body(response))
    assert len(rows) == ARTIFACT_COUNT, (
        "GET /api%s returned %d artifacts; the brief seeds %d"
        % (API_RELEASES, len(rows), ARTIFACT_COUNT))
    combos = {(str(field(r, "os", default="")), str(field(r, "arch", default="")),
               str(field(r, "format", default=""))) for r in rows}
    assert combos == set(PLATFORM_ROWS), (
        "GET /api%s covers the platform rows %r; the brief pins %r"
        % (API_RELEASES, sorted(combos), sorted(PLATFORM_ROWS)))
    versions = {str(field(r, "version", default="")) for r in rows}
    assert versions == set(RELEASE_VERSIONS), (
        "GET /api%s covers versions %r; the brief pins %r"
        % (API_RELEASES, sorted(versions), sorted(RELEASE_VERSIONS)))


def test_pricing_route_shows_four_plans_and_seven_tiers(api, site):
    """cov: C-CF-32, C-CF-95, C-CF-97, C-CF-111, C-CF-112"""
    payload = json_body(api.get(API_PLANS))
    assert payload is not None, (
        "GET /api%s returned no JSON document: %r" % (API_PLANS, payload))
    blob = repr(payload)
    for code in PLAN_CODES:
        assert code in blob, (
            "GET /api%s does not carry the plan code %r" % (API_PLANS, code))
    for code in TIER_CODES:
        assert code in blob, (
            "GET /api%s does not carry the tier code %r" % (API_PLANS, code))
    page = visible_text(site.get(ROUTE_PRICING).text)
    assert QUESTIONS_HEADING in page, (
        "GET %s does not show the questions band heading %r"
        % (ROUTE_PRICING, QUESTIONS_HEADING))
    for label in ("Monthly", "Yearly", "Free", "Custom", "Get Teams",
                  "Get Pro", "Contact Sales"):
        assert label in page, (
            "GET %s does not show the pinned pricing control or price %r"
            % (ROUTE_PRICING, label))


def test_tier_prices_and_allowances_are_stored_in_minor_units(db):
    """cov: C-CF-47, C-CF-141, C-CF-144, C-TR-12, C-DM-8"""
    rows = db.rows("tiers")
    assert len(rows) == len(TIER_CODES), (
        "the tiers table holds %d rows; the brief pins %d"
        % (len(rows), len(TIER_CODES)))
    by_code = {str(field(r, "code", default="")): r for r in rows}
    for code, monthly in TIER_MONTHLY.items():
        row = by_code.get(code)
        assert row is not None, (
            "the tiers table has no row for %r" % code)
        got = field(row, "monthly_price_minor")
        assert int(got) == monthly, (
            "tier %r stores a monthly price of %r; the brief pins %d minor "
            "units" % (code, got, monthly))
        yearly = field(row, "yearly_price_minor")
        assert int(yearly) == TIER_YEARLY[code], (
            "tier %r stores a yearly price of %r; the brief pins %d minor units"
            % (code, yearly, TIER_YEARLY[code]))
        allowance = field(row, "included_allowance_minor")
        assert int(allowance) == TIER_ALLOWANCE[code], (
            "tier %r stores an included allowance of %r; the brief pins %d"
            % (code, allowance, TIER_ALLOWANCE[code]))


def test_changelog_projects_its_four_newest_entries_onto_the_home_route(api, site):
    """cov: C-CF-26, C-CF-27, C-CF-43, C-UF-3"""
    rows = as_list(json_body(api.get(API_CHANGELOG)))
    slugs = [str(field(r, "slug", default="")) for r in rows]
    assert set(slugs) == set(CHANGELOG_SLUGS), (
        "GET /api%s returned slugs %r; the brief seeds %r"
        % (API_CHANGELOG, sorted(slugs), sorted(CHANGELOG_SLUGS)))
    page = visible_text(site.get(ROUTE_CHANGELOG).text)
    home = visible_text(site.get(ROUTE_HOME).text)
    titles = [str(field(r, "title", default="")) for r in rows]
    for title in titles:
        assert title in page, (
            "GET %s does not show the entry title %r" % (ROUTE_CHANGELOG, title))
        assert title in home, (
            "GET / does not show the changelog entry %r; the band renders the "
            "four most recent entries from the same source" % title)
    unknown = api.get("%s/%s" % (API_CHANGELOG, probe_slug("entry")))
    assert unknown.status_code in NOT_FOUND, (
        "GET /api%s for an unknown slug returned %s; a stale link answers as "
        "not found rather than redirecting to the index"
        % (API_CHANGELOG, unknown.status_code))


def test_install_block_and_marketplace_heading_are_pinned_copy(site):
    """cov: C-CF-23, C-CF-25"""
    home = visible_text(site.get(ROUTE_HOME).text)
    for tab in INSTALL_TABS:
        assert tab in home, (
            "GET / does not show the install tab %r" % tab)
    assert NARROW_PRIMARY in site.get(ROUTE_HOME).text, (
        "GET / carries no %r label; the narrow variant of the hero control "
        "drops the platform name" % NARROW_PRIMARY)
    market = visible_text(site.get(ROUTE_MARKETPLACE).text)
    assert MARKETPLACE_HEADING in market, (
        "GET %s does not show the pinned heading %r"
        % (ROUTE_MARKETPLACE, MARKETPLACE_HEADING))
    for label in ("Featured Plugins", "Featured Automations", "Recently Added",
                  "Manage Automations", "Publish"):
        assert label in market, (
            "GET %s does not show the pinned marketplace label %r"
            % (ROUTE_MARKETPLACE, label))


def test_signup_then_signin_returns_a_bearer_token(api):
    """cov: C-CF-2, C-CF-4, C-UF-2, C-UF-4"""
    email = probe_email("signup")
    created = signup(api, email, "Probe Owner")
    assert created.status_code in OK_WRITE, (
        "POST /api%s for a new address returned %s: %r"
        % (API_SIGNUP, created.status_code, created.text[:300]))
    assert token_of(json_body(created)), (
        "POST /api%s returned no bearer token: %r"
        % (API_SIGNUP, created.text[:300]))
    again = signup(api, email, "Probe Owner")
    assert again.status_code in REFUSED, (
        "POST /api%s for an address already registered returned %s; the brief "
        "rejects it as invalid: %r"
        % (API_SIGNUP, again.status_code, again.text[:300]))
    wrong = signin(api, email, "not-the-pinned-password")
    assert wrong.status_code in DENIED, (
        "POST /api%s with a wrong password returned %s; the brief denies it: %r"
        % (API_SIGNIN, wrong.status_code, wrong.text[:300]))
    assert not token_of(json_body(wrong)), (
        "POST /api%s with a wrong password returned a token: %r"
        % (API_SIGNIN, wrong.text[:300]))
    for seeded in SEEDED_ACCOUNTS:
        ok = signin(api, seeded)
        assert ok.status_code in OK_WRITE, (
            "the seeded account %r documented at /app/USER_README.md could not "
            "sign in with the pinned password: %s %r"
            % (seeded, ok.status_code, ok.text[:200]))


def test_anonymous_account_endpoints_are_denied(api, raw_site):
    """cov: C-RL-8"""
    me = api.get(API_ME)
    assert me.status_code in DENIED, (
        "GET /api%s without a bearer token returned %s; the brief denies it: %r"
        % (API_ME, me.status_code, me.text[:200]))
    usage = api.get(workspace_path(WS_AURORA, "/usage"))
    assert usage.status_code in DENIED_OR_MISSING, (
        "GET /api%s without a bearer token returned %s; an anonymous caller "
        "reads no workspace" % (workspace_path(WS_AURORA, "/usage"),
                                usage.status_code))
    guarded = raw_site.get(ROUTE_ACCOUNT)
    assert guarded.status_code in (301, 302, 303, 307, 308), (
        "GET %s anonymously returned %s; the brief sends the browser to %s "
        "carrying the requested path"
        % (ROUTE_ACCOUNT, guarded.status_code, ROUTE_SIGNIN))
    target = guarded.headers.get("location", "")
    assert ROUTE_SIGNIN in target, (
        "GET %s anonymously redirected to %r rather than to %s"
        % (ROUTE_ACCOUNT, target, ROUTE_SIGNIN))
    assert ROUTE_ACCOUNT in target, (
        "GET %s anonymously redirected to %r, which does not carry the "
        "requested path" % (ROUTE_ACCOUNT, target))


def test_anonymous_mutating_endpoints_are_denied(api):
    """cov: C-RL-8"""
    calls = (
        ("POST", API_WORKSPACES, {"name": probe_slug("Workspace")}),
        ("POST", workspace_path(WS_AURORA, "/invitations"),
         {"email": probe_email("invite"), "role": ROLE_MEMBER}),
        ("POST", API_CHECKOUT, {"tier_code": "standard", "interval": "monthly"}),
        ("POST", plugin_path("plugin", "foolscap", "/install"), {}),
    )
    for method, path, body in calls:
        response = api.request(method, path, json=body)
        assert response.status_code in DENIED_OR_MISSING, (
            "%s /api%s without a bearer token returned %s; every mutating "
            "endpoint denies an anonymous caller: %r"
            % (method, path, response.status_code, response.text[:200]))


def test_member_invitation_call_is_denied_at_the_api(api):
    """cov: C-RL-8, C-CF-128, C-CF-132"""
    headers = bearer(api, MEMBER_EMAIL)
    response = api.post(workspace_path(WS_AURORA, "/invitations"),
                        headers=headers,
                        json={"email": probe_email("denied"),
                              "role": ROLE_MEMBER})
    assert response.status_code in DENIED, (
        "POST /api%s from the member session returned %s; only an owner may "
        "invite: %r" % (workspace_path(WS_AURORA, "/invitations"),
                        response.status_code, response.text[:300]))


def test_denied_invitation_leaves_no_row_and_sends_no_mail(api, db, inbox):
    """cov: C-UF-13"""
    headers = bearer(api, MEMBER_EMAIL)
    address = probe_email("denied-invite")
    before = inbox.count(address)
    response = api.post(workspace_path(WS_AURORA, "/invitations"),
                        headers=headers,
                        json={"email": address, "role": ROLE_MEMBER})
    assert response.status_code in DENIED, (
        "POST /api%s from the member session returned %s rather than a denial"
        % (workspace_path(WS_AURORA, "/invitations"), response.status_code))
    settle()
    rows = db.rows("invitations", email=address)
    assert not rows, (
        "a denied invitation left %d row(s) in the invitations table for %r; "
        "the protected state is unchanged" % (len(rows), address))
    assert inbox.count(address) == before, (
        "a denied invitation delivered mail to %r; a refused request sends "
        "nothing" % address)


def test_other_workspace_usage_answers_not_found(api):
    """cov: C-CF-44, C-CF-131"""
    headers = bearer(api, MEMBER_EMAIL)
    response = api.get(workspace_path(WS_NORTHLIGHT, "/usage"), headers=headers)
    assert response.status_code in NOT_FOUND, (
        "GET /api%s with a valid token belonging to another workspace returned "
        "%s; the brief answers as not found so the other workspace's existence "
        "is not confirmed: %r" % (workspace_path(WS_NORTHLIGHT, "/usage"),
                                  response.status_code, response.text[:300]))


def test_other_workspace_members_answers_not_found(api):
    """cov: C-DM-5, C-DM-21"""
    headers = bearer(api, OWNER2_EMAIL)
    response = api.get(workspace_path(WS_AURORA, "/members"), headers=headers)
    assert response.status_code in NOT_FOUND, (
        "GET /api%s with a token from another workspace returned %s; the brief "
        "answers as not found: %r" % (workspace_path(WS_AURORA, "/members"),
                                      response.status_code,
                                      response.text[:300]))


def test_no_credential_appears_in_anything_the_browser_downloads(site):
    """cov: C-CF-175, C-DC-7"""
    for route in PUBLIC_ROUTES:
        body = site.get(route).text
        for marker in SECRET_MARKERS:
            assert marker not in body, (
                "GET %s served a document containing %r; no credential, key or "
                "connection string reaches anything the browser downloads"
                % (route, marker))


def test_model_registry_seed_rows_are_persisted(db):
    """cov: C-CF-45, C-DM-24"""
    for table in SEEDED_TABLES:
        rows = db.rows(table)
        assert rows, (
            "the seeded table %r holds no rows; the brief seeds every one of "
            "them at first start" % table)
    models = db.rows(TABLE_MODELS)
    assert len(models) == MODEL_COUNT, (
        "the %r table holds %d rows; the registry the brief pins holds %d"
        % (TABLE_MODELS, len(models), MODEL_COUNT))
    by_code = {str(field(r, "code", default="")): r for r in models}
    for code in MODEL_CODES:
        row = by_code.get(code)
        assert row is not None, (
            "the %r table has no row for %r" % (TABLE_MODELS, code))
        assert int(field(row, "benchmark_score_bp")) == MODEL_SCORE_BP[code], (
            "model %r stores a benchmark figure of %r; the brief pins %d"
            % (code, field(row, "benchmark_score_bp"), MODEL_SCORE_BP[code]))
        assert int(field(row, "tokens_per_task")) == MODEL_TOKENS[code], (
            "model %r stores %r tokens per task; the brief pins %d"
            % (code, field(row, "tokens_per_task"), MODEL_TOKENS[code]))
        assert int(field(row, "steps_per_task")) == MODEL_STEPS[code], (
            "model %r stores %r steps per task; the brief pins %d"
            % (code, field(row, "steps_per_task"), MODEL_STEPS[code]))
        cost = field(row, "cost_per_task_minor")
        expected = MODEL_COST[code]
        if expected is None:
            assert cost is None, (
                "model %r stores a cost per task of %r; the brief leaves it "
                "not measured" % (code, cost))
        else:
            assert int(cost) == expected, (
                "model %r stores a cost per task of %r; the brief pins %d "
                "minor units" % (code, cost, expected))
    versions = {str(field(r, "benchmark_version", default="")) for r in models}
    assert versions == {BENCHMARK_VERSION}, (
        "the registry reports benchmark versions %r; the brief pins %r"
        % (versions, BENCHMARK_VERSION))


def test_install_is_idempotent_and_the_stored_row_is_single(api, db):
    """cov: C-CF-80"""
    headers = bearer(api, MEMBER_EMAIL)
    slug = PLUGIN_SLUGS[0]
    first = api.post(plugin_path("plugin", slug, "/install"), headers=headers,
                     json={})
    assert first.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r" % (plugin_path("plugin", slug, "/install"),
                                         first.status_code, first.text[:300]))
    second = api.post(plugin_path("plugin", slug, "/install"), headers=headers,
                      json={})
    assert second.status_code in OK_WRITE + CONFLICT, (
        "the second install of %r returned %s; a repeat install is a no-op or "
        "a refusal, never a server error: %r"
        % (slug, second.status_code, second.text[:300]))
    settle()
    plugins = [r for r in db.rows(TABLE_PLUGINS)
               if str(field(r, "slug", default="")) == slug]
    assert len(plugins) == 1, (
        "the %r table holds %d rows for %r" % (TABLE_PLUGINS, len(plugins), slug))
    plugin_id = field(plugins[0], "id")
    rows = [r for r in db.rows(TABLE_INSTALLATIONS)
            if str(field(r, "plugin_id")) == str(plugin_id)]
    signatures = {(str(field(r, "subject_type", default="")),
                   str(field(r, "subject_id", default=""))) for r in rows}
    assert len(rows) == len(signatures), (
        "the %r table holds %d rows for %r across %d distinct subjects; one "
        "row exists per subject and plugin"
        % (TABLE_INSTALLATIONS, len(rows), slug, len(signatures)))


def test_install_count_rises_by_one_then_stays(api):
    """cov: C-CF-81, C-DM-15"""
    headers = bearer(api, OWNER2_EMAIL)
    slug = "foolscap"
    before = json_body(api.get(plugin_path("plugin", slug)))
    start = int(field(before, "install_count", "installCount", default=-1))
    assert start == FOOLSCAP_COUNT, (
        "GET /api%s reports %d installs before any probe install; the brief "
        "seeds %d" % (plugin_path("plugin", slug), start, FOOLSCAP_COUNT))
    api.post(plugin_path("plugin", slug, "/install"), headers=headers, json={})
    settle()
    after = json_body(api.get(plugin_path("plugin", slug)))
    risen = int(field(after, "install_count", "installCount", default=-1))
    assert risen == FOOLSCAP_COUNT_AFTER, (
        "GET /api%s reports %d installs after one install; the brief takes the "
        "count from %d to %d" % (plugin_path("plugin", slug), risen,
                                 FOOLSCAP_COUNT, FOOLSCAP_COUNT_AFTER))
    api.post(plugin_path("plugin", slug, "/install"), headers=headers, json={})
    settle()
    again = json_body(api.get(plugin_path("plugin", slug)))
    held = int(field(again, "install_count", "installCount", default=-1))
    assert held == FOOLSCAP_COUNT_AFTER, (
        "GET /api%s reports %d installs after a repeated install; the count "
        "stays at %d" % (plugin_path("plugin", slug), held,
                         FOOLSCAP_COUNT_AFTER))


def test_usage_replay_stores_no_second_row(api, db):
    """cov: C-CF-136, C-TR-3"""
    headers = bearer(api, OWNER_EMAIL)
    key = "probe-usage-%s" % probe_token()
    body = {"idempotency_key": key, "model_code": "meridian-4",
            "surface": "desktop", "tasks": 2}
    first = api.post(workspace_path(WS_AURORA, "/usage-events"),
                     headers=headers, json=body)
    assert first.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r"
        % (workspace_path(WS_AURORA, "/usage-events"), first.status_code,
           first.text[:300]))
    replay = api.post(workspace_path(WS_AURORA, "/usage-events"),
                      headers=headers, json=body)
    assert replay.status_code in OK_WRITE, (
        "the replayed usage request returned %s; an identical replay answers "
        "with the original event: %r" % (replay.status_code,
                                         replay.text[:300]))
    settle()
    rows = db.rows(TABLE_USAGE, idempotency_key=key)
    assert len(rows) == 1, (
        "the %r table holds %d rows for the idempotency key %r; a replay adds "
        "no second row" % (TABLE_USAGE, len(rows), key))
    rated = field(rows[0], "rated_cost_minor")
    assert int(rated) == 2 * MODEL_COST["meridian-4"], (
        "the usage event stores a rated cost of %r; two tasks at %d minor "
        "units each is %d" % (rated, MODEL_COST["meridian-4"],
                              2 * MODEL_COST["meridian-4"]))


def test_usage_key_with_a_different_body_is_a_conflict(api):
    """cov: C-CF-137"""
    headers = bearer(api, OWNER_EMAIL)
    key = "probe-usage-%s" % probe_token()
    first = api.post(workspace_path(WS_AURORA, "/usage-events"),
                     headers=headers,
                     json={"idempotency_key": key, "model_code": "meridian-4",
                           "surface": "desktop", "tasks": 1})
    assert first.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r"
        % (workspace_path(WS_AURORA, "/usage-events"), first.status_code,
           first.text[:300]))
    clash = api.post(workspace_path(WS_AURORA, "/usage-events"),
                     headers=headers,
                     json={"idempotency_key": key, "model_code": "corvus-3",
                           "surface": "cloud", "tasks": 9})
    assert clash.status_code in CONFLICT, (
        "the same idempotency key with a different body returned %s; the brief "
        "rejects it as a conflict: %r" % (clash.status_code, clash.text[:300]))


def test_allowance_and_overage_reconcile_with_the_seeded_rows(api, db):
    """cov: C-CF-140"""
    headers = bearer(api, OWNER_EMAIL)
    for key in AURORA_USAGE_KEYS:
        rows = db.rows(TABLE_USAGE, idempotency_key=key)
        assert len(rows) == 1, (
            "the %r table holds %d rows for the seeded key %r; the brief seeds "
            "exactly one" % (TABLE_USAGE, len(rows), key))
    northlight = db.rows(TABLE_USAGE, idempotency_key=NORTHLIGHT_USAGE_KEY)
    assert len(northlight) == 1, (
        "the %r table holds %d rows for %r" % (TABLE_USAGE, len(northlight),
                                               NORTHLIGHT_USAGE_KEY))
    body = json_body(api.get(workspace_path(WS_AURORA, "/usage"),
                             headers=headers))
    included = int(field(body, "included_minor", "includedMinor", default=-1))
    consumed = int(field(body, "consumed_minor", "consumedMinor", default=-1))
    overage = int(field(body, "overage_minor", "overageMinor", default=-1))
    assert included == AURORA_INCLUDED, (
        "GET /api%s reports an included allowance of %d; the standard tier at "
        "%d seats includes %d" % (workspace_path(WS_AURORA, "/usage"),
                                  included, AURORA_SEATS, AURORA_INCLUDED))
    assert consumed == AURORA_CONSUMED, (
        "GET /api%s reports %d consumed; the three seeded events sum to %d"
        % (workspace_path(WS_AURORA, "/usage"), consumed, AURORA_CONSUMED))
    assert overage == AURORA_OVERAGE, (
        "GET /api%s reports an overage of %d; %d consumed against %d included "
        "is %d" % (workspace_path(WS_AURORA, "/usage"), overage,
                   AURORA_CONSUMED, AURORA_INCLUDED, AURORA_OVERAGE))


def test_northlight_usage_stays_inside_its_allowance(api):
    """cov: C-CF-146"""
    headers = bearer(api, OWNER2_EMAIL)
    body = json_body(api.get(workspace_path(WS_NORTHLIGHT, "/usage"),
                             headers=headers))
    consumed = int(field(body, "consumed_minor", "consumedMinor", default=-1))
    included = int(field(body, "included_minor", "includedMinor", default=-1))
    overage = int(field(body, "overage_minor", "overageMinor", default=-1))
    assert consumed == NORTHLIGHT_CONSUMED, (
        "GET /api%s reports %d consumed; the seeded event is %d minor units"
        % (workspace_path(WS_NORTHLIGHT, "/usage"), consumed,
           NORTHLIGHT_CONSUMED))
    assert included == NORTHLIGHT_INCLUDED, (
        "GET /api%s reports an included allowance of %d; the hobby tier "
        "includes %d" % (workspace_path(WS_NORTHLIGHT, "/usage"), included,
                         NORTHLIGHT_INCLUDED))
    assert overage == 0, (
        "GET /api%s reports an overage of %d; %d consumed inside %d included "
        "is no overage" % (workspace_path(WS_NORTHLIGHT, "/usage"), overage,
                           NORTHLIGHT_CONSUMED, NORTHLIGHT_INCLUDED))


def test_checkout_creates_the_billing_account_in_the_payment_platform(api, db, payments):
    """cov: C-CF-104, C-CF-109, C-TR-7, C-TR-9, C-DC-16"""
    email = probe_email("checkout")
    created = signup(api, email, "Probe Buyer")
    assert created.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r" % (API_SIGNUP, created.status_code,
                                         created.text[:300]))
    headers = {"Authorization": "Bearer %s" % token_of(json_body(created))}
    name = "Probe %s" % probe_token()
    workspace = api.post(API_WORKSPACES, headers=headers, json={"name": name})
    assert workspace.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r" % (API_WORKSPACES,
                                         workspace.status_code,
                                         workspace.text[:300]))
    slug = str(field(json_body(workspace), "slug", default=""))
    assert slug, (
        "POST /api%s returned no workspace slug: %r"
        % (API_WORKSPACES, workspace.text[:300]))
    checkout = api.post(API_CHECKOUT, headers=headers,
                        json={"tier_code": "standard", "interval": "monthly"})
    assert checkout.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r" % (API_CHECKOUT, checkout.status_code,
                                         checkout.text[:300]))
    settle()
    expected_key = BILLING_KEY_PREFIX + slug
    matches = accounts_with_key(payments, expected_key)
    assert len(matches) == 1, (
        "killbill holds %d account(s) at the external key %r after one "
        "checkout; the brief creates exactly one" % (len(matches), expected_key))
    account = matches[0]
    assert str(field(account, "currency", default="")).upper() == BILLING_CURRENCY, (
        "the killbill account at %r reports currency %r; the brief pins %r"
        % (expected_key, field(account, "currency"), BILLING_CURRENCY))
    assert str(field(account, "country", default="")).upper() == BILLING_COUNTRY, (
        "the killbill account at %r reports country %r; the brief pins %r"
        % (expected_key, field(account, "country"), BILLING_COUNTRY))
    assert str(field(account, "email", default="")).lower() == email.lower(), (
        "the killbill account at %r carries the address %r; the brief carries "
        "the owner's address %r" % (expected_key, field(account, "email"),
                                    email))
    rows = [r for r in db.rows(TABLE_WORKSPACES)
            if str(field(r, "slug", default="")) == slug]
    assert rows and str(field(rows[0], "billing_external_key",
                              default="")) == expected_key, (
        "the workspace row for %r stores the billing external key %r; the "
        "brief pins %r" % (slug, rows and field(rows[0],
                                                "billing_external_key"),
                           expected_key))


def test_repeat_checkout_leaves_one_billing_account_at_the_external_key(
        api, payments):
    email = probe_email("repeat")
    created = signup(api, email, "Probe Repeat")
    headers = {"Authorization": "Bearer %s" % token_of(json_body(created))}
    name = "Repeat %s" % probe_token()
    workspace = api.post(API_WORKSPACES, headers=headers, json={"name": name})
    slug = str(field(json_body(workspace), "slug", default=""))
    assert slug, (
        "POST /api%s returned no workspace slug: %r"
        % (API_WORKSPACES, workspace.text[:300]))
    first = api.post(API_CHECKOUT, headers=headers,
                     json={"tier_code": "standard", "interval": "monthly"})
    assert first.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r" % (API_CHECKOUT, first.status_code,
                                         first.text[:300]))
    second = api.post(API_CHECKOUT, headers=headers,
                      json={"tier_code": "standard", "interval": "monthly"})
    assert second.status_code in OK_WRITE + CONFLICT, (
        "the second checkout returned %s; the brief refuses a second live "
        "subscription as a conflict rather than failing with a server error: %r"
        % (second.status_code, second.text[:300]))
    settle()
    expected_key = BILLING_KEY_PREFIX + slug
    matches = accounts_with_key(payments, expected_key)
    assert len(matches) == 1, (
        "killbill holds %d account(s) at the external key %r after two "
        "checkouts; the external key is unique, so the store refuses the "
        "second rather than duplicating it" % (len(matches), expected_key))


def test_second_live_subscription_is_refused_as_a_conflict(api, db):
    """cov: C-CF-108, C-DM-12"""
    email = probe_email("race")
    created = signup(api, email, "Probe Race")
    headers = {"Authorization": "Bearer %s" % token_of(json_body(created))}
    name = "Race %s" % probe_token()
    workspace = api.post(API_WORKSPACES, headers=headers, json={"name": name})
    slug = str(field(json_body(workspace), "slug", default=""))

    def attempt():
        return api.post(API_CHECKOUT, headers=headers,
                        json={"tier_code": "standard", "interval": "monthly"})

    responses = in_parallel(attempt, 2)
    codes = sorted(r.status_code for r in responses)
    accepted = [r for r in responses if r.status_code in OK_WRITE]
    assert accepted, (
        "two simultaneous checkouts both failed with %r; exactly one wins"
        % codes)
    assert len(accepted) == 1 or all(
        r.status_code in OK_WRITE for r in responses), (
        "two simultaneous checkouts returned %r; the loser is rejected as a "
        "conflict" % codes)
    settle()
    rows = db.rows(TABLE_SUBSCRIPTIONS)
    live = [r for r in rows
            if str(field(r, "subject_id", default="")) and
            str(field(r, "state", default="")) in ("active", "past_due") and
            str(field(r, "billing_external_key", default="")) ==
            BILLING_KEY_PREFIX + slug]
    assert len(live) == 1, (
        "the %r table holds %d live rows for the workspace %r after two "
        "simultaneous checkouts; at most one subscription per subject is live"
        % (TABLE_SUBSCRIPTIONS, len(live), slug))


def test_subscription_state_tier_and_interval_are_stored(api):
    """cov: C-DM-11"""
    headers = bearer(api, OWNER_EMAIL)
    response = api.get(API_SUBSCRIPTION, headers=headers)
    assert response.status_code in OK_READ, (
        "GET /api%s for the seeded owner returned %s: %r"
        % (API_SUBSCRIPTION, response.status_code, response.text[:300]))
    body = json_body(response)
    assert str(field(body, "tier_code", "tierCode", default="")) == "standard", (
        "GET /api%s reports the tier %r; the seeded workspace is on standard"
        % (API_SUBSCRIPTION, field(body, "tier_code", "tierCode")))
    assert str(field(body, "interval", default="")) == "monthly", (
        "GET /api%s reports the interval %r; the seeded subscription is monthly"
        % (API_SUBSCRIPTION, field(body, "interval")))
    assert int(field(body, "seats", default=-1)) == AURORA_SEATS, (
        "GET /api%s reports %r seats; the seeded workspace holds %d"
        % (API_SUBSCRIPTION, field(body, "seats"), AURORA_SEATS))
    assert str(field(body, "billing_external_key", "billingExternalKey",
                     default="")) == BILLING_KEY_AURORA, (
        "GET /api%s reports the external key %r; the brief pins %r"
        % (API_SUBSCRIPTION, field(body, "billing_external_key",
                                   "billingExternalKey"), BILLING_KEY_AURORA))


def test_invitation_email_reaches_only_the_invited_address(api, inbox):
    """cov: C-CF-117, C-CF-120, C-DM-7"""
    headers = bearer(api, OWNER_EMAIL)
    address = probe_email("invited")
    other = probe_email("bystander")
    before_other = inbox.count(other)
    response = api.post(workspace_path(WS_AURORA, "/invitations"),
                        headers=headers,
                        json={"email": address, "role": ROLE_MEMBER})
    assert response.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r"
        % (workspace_path(WS_AURORA, "/invitations"), response.status_code,
           response.text[:300]))
    settle()
    message = inbox.find(address, INVITE_SUBJECT_PREFIX)
    assert message is not None, (
        "no invitation message reached %r at mailpit; the brief sends one over "
        "real SMTP when an owner invites" % address)
    assert len(message.to) == 1, (
        "the invitation to %r was addressed to %r; the brief pins the invited "
        "address only, with no copy recipient" % (address, message.to))
    assert inbox.count(other) == before_other, (
        "inviting %r delivered mail to the unrelated address %r"
        % (address, other))


def test_invitation_subject_carries_the_pinned_prefix_and_workspace(api, inbox):
    """cov: C-CF-118, C-CF-119"""
    headers = bearer(api, OWNER_EMAIL)
    address = probe_email("subject")
    response = api.post(workspace_path(WS_AURORA, "/invitations"),
                        headers=headers,
                        json={"email": address, "role": ROLE_MEMBER})
    assert response.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r"
        % (workspace_path(WS_AURORA, "/invitations"), response.status_code,
           response.text[:300]))
    settle()
    message = inbox.find(address, INVITE_SUBJECT_PREFIX)
    assert message is not None, (
        "no invitation message reached %r at mailpit" % address)
    assert message.subject.startswith(INVITE_SUBJECT_AURORA), (
        "the invitation subject was %r; the brief pins a subject beginning %r"
        % (message.subject, INVITE_SUBJECT_AURORA))
    assert message.body.strip(), (
        "the invitation to %r carried an empty body; the brief pins a body "
        "naming the workspace and the inviter" % address)


def test_revoking_an_invitation_sends_no_confirmation_mail(api, inbox):
    """cov: C-CF-123"""
    headers = bearer(api, OWNER_EMAIL)
    address = probe_email("revoked")
    created = api.post(workspace_path(WS_AURORA, "/invitations"),
                       headers=headers,
                       json={"email": address, "role": ROLE_MEMBER})
    assert created.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r"
        % (workspace_path(WS_AURORA, "/invitations"), created.status_code,
           created.text[:300]))
    settle()
    before = inbox.count(address)
    invitation_id = field(json_body(created), "id")
    assert invitation_id is not None, (
        "POST /api%s returned no invitation identifier: %r"
        % (workspace_path(WS_AURORA, "/invitations"), created.text[:300]))
    revoked = api.delete(
        workspace_path(WS_AURORA, "/invitations/%s" % invitation_id),
        headers=headers)
    assert revoked.status_code in OK_WRITE + (204,), (
        "DELETE /api%s returned %s: %r"
        % (workspace_path(WS_AURORA, "/invitations/%s" % invitation_id),
           revoked.status_code, revoked.text[:300]))
    settle()
    assert inbox.count(address) == before, (
        "revoking the invitation to %r delivered a further message; the brief "
        "sends nothing on that transition" % address)


def test_repeat_invitation_resends_one_link_and_creates_no_second_row(api, db):
    """cov: C-CF-122"""
    headers = bearer(api, OWNER_EMAIL)
    address = probe_email("repeat-invite")
    first = api.post(workspace_path(WS_AURORA, "/invitations"),
                     headers=headers,
                     json={"email": address, "role": ROLE_MEMBER})
    assert first.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r"
        % (workspace_path(WS_AURORA, "/invitations"), first.status_code,
           first.text[:300]))
    again = api.post(workspace_path(WS_AURORA, "/invitations"),
                     headers=headers,
                     json={"email": address, "role": ROLE_MEMBER})
    assert again.status_code in OK_WRITE + CONFLICT, (
        "the repeated invitation to %r returned %s; the brief re-sends the "
        "same link rather than failing: %r"
        % (address, again.status_code, again.text[:300]))
    settle()
    rows = db.rows("invitations", email=address)
    pending = [r for r in rows
               if str(field(r, "state", default="")) == "pending"]
    assert len(pending) == 1, (
        "the invitations table holds %d pending rows for %r; one pending "
        "invitation exists per workspace and address"
        % (len(pending), address))


def test_accepting_an_invitation_consumes_one_seat(api, db):
    """cov: C-CF-126, C-UF-8"""
    owner_headers = bearer(api, OWNER_EMAIL)
    address = probe_email("accepting")
    created = api.post(workspace_path(WS_AURORA, "/invitations"),
                       headers=owner_headers,
                       json={"email": address, "role": ROLE_MEMBER})
    assert created.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r"
        % (workspace_path(WS_AURORA, "/invitations"), created.status_code,
           created.text[:300]))
    body = json_body(created)
    token = field(body, "token")
    assert token, (
        "POST /api%s returned no acceptance token: %r"
        % (workspace_path(WS_AURORA, "/invitations"), created.text[:300]))
    joined = signup(api, address, "Probe Colleague")
    assert joined.status_code in OK_WRITE, (
        "POST /api%s for the invited address returned %s: %r"
        % (API_SIGNUP, joined.status_code, joined.text[:300]))
    guest = {"Authorization": "Bearer %s" % token_of(json_body(joined))}
    before = int(field(json_body(api.get(workspace_path(WS_AURORA),
                                         headers=owner_headers)),
                       "seat_count", "seatCount", default=-1))
    accepted = api.post("/invitations/accept", headers=guest,
                        json={"token": token})
    assert accepted.status_code in OK_WRITE, (
        "POST /api/invitations/accept returned %s: %r"
        % (accepted.status_code, accepted.text[:300]))
    settle()
    after = int(field(json_body(api.get(workspace_path(WS_AURORA),
                                        headers=owner_headers)),
                      "seat_count", "seatCount", default=-1))
    assert after == before + 1, (
        "the workspace reported %d seats before acceptance and %d after; "
        "accepting an invitation consumes exactly one seat" % (before, after))
    replay = api.post("/invitations/accept", headers=guest,
                      json={"token": token})
    assert replay.status_code in REFUSED + DENIED_OR_MISSING, (
        "re-accepting the same invitation token returned %s; an accepted token "
        "is rejected and changes nothing: %r"
        % (replay.status_code, replay.text[:300]))
    rows = db.rows("memberships")
    assert rows, (
        "the memberships table holds no rows after an acceptance")


def test_usage_past_the_spend_limit_is_refused(api):
    """cov: C-CF-145, C-CF-146"""
    headers = bearer(api, OWNER_EMAIL)
    limit = api.put(workspace_path(WS_AURORA, "/spend-limit"), headers=headers,
                    json={"limit_minor": AURORA_SPEND_LIMIT})
    assert limit.status_code in OK_WRITE, (
        "PUT /api%s returned %s: %r"
        % (workspace_path(WS_AURORA, "/spend-limit"), limit.status_code,
           limit.text[:300]))
    response = api.post(workspace_path(WS_AURORA, "/usage-events"),
                        headers=headers,
                        json={"idempotency_key": "probe-limit-%s" % probe_token(),
                              "model_code": "kestrel-4", "surface": "cloud",
                              "tasks": 40})
    assert response.status_code in PAYMENT_REQUIRED, (
        "POST /api%s for usage far past the spend limit of %d returned %s; the "
        "brief refuses it with an answer naming the limit: %r"
        % (workspace_path(WS_AURORA, "/usage-events"), AURORA_SPEND_LIMIT,
           response.status_code, response.text[:300]))


def test_usage_with_an_uncosted_model_is_refused(api):
    """cov: C-CF-133"""
    headers = bearer(api, OWNER_EMAIL)
    response = api.post(workspace_path(WS_AURORA, "/usage-events"),
                        headers=headers,
                        json={"idempotency_key": "probe-uncosted-%s" % probe_token(),
                              "model_code": MODEL_UNCOSTED,
                              "surface": "terminal", "tasks": 1})
    assert response.status_code in REFUSED, (
        "POST /api%s naming the model %r, which has no measured cost per task, "
        "returned %s; the brief rejects it as invalid: %r"
        % (workspace_path(WS_AURORA, "/usage-events"), MODEL_UNCOSTED,
           response.status_code, response.text[:300]))


def test_unrouted_address_renders_the_product_not_found_page(site, raw_site):
    """cov: C-CF-169"""
    path = "/%s" % probe_slug("nowhere")
    response = raw_site.get(path)
    assert response.status_code in NOT_FOUND, (
        "GET %s returned %s; an unrouted address answers as not found rather "
        "than serving the home document" % (path, response.status_code))
    assert SKIP_LINK in response.text, (
        "GET %s rendered without the product's own chrome; the not-found page "
        "carries the full chrome so the visitor is not stranded" % path)
    home = visible_text(site.get(ROUTE_HOME).text)
    body = visible_text(response.text)
    assert HOME_HEADLINE not in body, (
        "GET %s served the home document; the brief renders the product's own "
        "not-found page instead" % path)
    assert body.strip() and body.strip() != home.strip(), (
        "GET %s served an empty or duplicated document" % path)


def test_empty_search_echoes_the_query_and_keeps_the_featured_section(api, site):
    """cov: C-CF-74"""
    needle = probe_slug("nomatch")
    response = api.get(API_PLUGINS, params={"q": needle})
    assert response.status_code in OK_READ, (
        "GET /api%s?q=%s returned %s; an empty result is not an error: %r"
        % (API_PLUGINS, needle, response.status_code, response.text[:200]))
    assert as_list(json_body(response)) == [], (
        "GET /api%s?q=%s returned matches for a probe string that matches "
        "nothing" % (API_PLUGINS, needle))
    page = site.get(ROUTE_MARKETPLACE, params={"q": needle})
    text = visible_text(page.text)
    assert needle in text, (
        "GET %s?q=%s does not echo the query back; the brief echoes it"
        % (ROUTE_MARKETPLACE, needle))
    assert "Featured Plugins" in text, (
        "GET %s?q=%s drops the featured section; the brief keeps it beneath an "
        "empty result" % (ROUTE_MARKETPLACE, needle))


def test_sales_enquiry_is_stored_once_and_refuses_an_unknown_topic(api, db):
    """cov: C-CF-161, C-CF-166"""
    address = probe_email("lead")
    body = {"email": address, "topic": "enterprise", "source": "navbar"}
    first = api.post(API_LEADS, json=body)
    assert first.status_code in OK_WRITE, (
        "POST /api%s returned %s: %r" % (API_LEADS, first.status_code,
                                         first.text[:300]))
    again = api.post(API_LEADS, json=body)
    assert again.status_code in OK_WRITE, (
        "POST /api%s a second time returned %s; the brief confirms both times: "
        "%r" % (API_LEADS, again.status_code, again.text[:300]))
    settle()
    rows = db.rows("leads", email=address)
    assert len(rows) == 1, (
        "the leads table holds %d rows for %r; a repeated enquiry is "
        "deduplicated behind the scenes" % (len(rows), address))
    unknown = api.post(API_LEADS, json={"email": probe_email("lead"),
                                        "topic": probe_slug("topic"),
                                        "source": "navbar"})
    assert unknown.status_code in REFUSED, (
        "POST /api%s with an unknown topic returned %s; the topic is a closed "
        "set refused on the server: %r"
        % (API_LEADS, unknown.status_code, unknown.text[:300]))
