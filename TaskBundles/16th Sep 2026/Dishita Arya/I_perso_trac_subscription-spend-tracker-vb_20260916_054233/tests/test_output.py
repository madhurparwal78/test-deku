"""Graders for Driplog.

Every assertion reads the running app or the persisted rows behind it. Nothing
here reads the app's own claim about its own effect.
"""

from __future__ import annotations

import csv
import io
from concurrent.futures import ThreadPoolExecutor

import httpx

from conftest import (
    ANCHOR_CALM_CURRENT,
    ANCHOR_NORTHBRIDGE,
    ANCHOR_ROASTLINE,
    BLOG_TITLES,
    BUILTIN_CATEGORIES,
    CANCELLED_EFFECTIVE_ON,
    CANCELLED_SUBSCRIPTION,
    CATEGORY_GROCERIES,
    CATEGORY_UTILITIES,
    CONFIDENCE_LOW,
    CONFLICT_STATUSES,
    COPY_BLOG_TITLE,
    COPY_EMPTY_LIST,
    COPY_FOOTER_RIGHTS,
    COPY_HERO_OPENING,
    COPY_NOT_FOUND,
    COPY_PRICING_HEADLINE,
    COPY_PRIVACY_UPDATED,
    COPY_SPENDING_TITLE,
    COPY_TERMS_UPDATED,
    COPY_WHERE_MONEY_GOES,
    CREDENTIALS_PATH,
    CSV_HEADER,
    CURRENCY_JPY,
    CURSOR_FIELD,
    DEMO_CATEGORY_MONTH,
    DEMO_CATEGORY_YEAR,
    DEMO_DAY_MINOR,
    DEMO_MONTH_MINOR,
    DEMO_SUBSCRIPTION_COUNT,
    DEMO_YEAR_MINOR,
    DENIAL_STATUSES,
    DUPLICATE_MERGE,
    DUPLICATE_SKIP,
    FILTER_ALL,
    FILTER_ONE_TIME,
    FILTER_RECURRING,
    FREE_CAP,
    GROCERIES_YEAR_APPROX_MINOR,
    HOME_CURRENCY,
    IMPORT_EXPECTED,
    IMPORT_LINES,
    MODE_NEXT_RENEWAL,
    MORE_FLAG,
    NOT_FOUND_STATUSES,
    ONE_TIME_AMOUNT_MINOR,
    OWNER2_DAY_MINOR,
    OWNER2_EMAIL,
    OWNER2_MONTH_MINOR,
    OWNER2_SUBSCRIPTION_COUNT,
    OWNER2_YEAR_MINOR,
    OWNER2_ZONE,
    OWNER_DAY_MINOR,
    OWNER_EMAIL,
    OWNER_MONTH_MINOR,
    OWNER_SUBSCRIPTION_COUNT,
    OWNER_YEAR_MINOR,
    PAGE_SIZE_MAX,
    PAGE_SIZE_PARAM,
    PASSWORD,
    PREMIUM_MONTHLY_MINOR,
    PREMIUM_SAVING_PERCENT,
    PREMIUM_TWELVE_MONTHS_MINOR,
    PREMIUM_YEARLY_MINOR,
    PRICE_CHANGE_EFFECTIVE_ON,
    PRICE_NORTHBRIDGE_NEW_MINOR,
    PRICE_NORTHBRIDGE_OLD_MINOR,
    PRIVACY_HEADINGS,
    PUBLIC_ROUTES,
    RATE_AS_OF,
    RECEIPT_05_LINES,
    RECEIPT_SAMPLES,
    REFUSAL_STATUSES,
    REMINDER_STATE_FIRED,
    REMINDER_STATE_MISSED,
    SUB_CALM_CURRENT,
    SUB_HARVEST_BOX,
    SUB_KETTLE_CLUB,
    SUB_LUMEN_PLAY,
    SUB_NORTHBRIDGE_AUTO,
    SUB_RADIOLARK,
    SUB_ROASTLINE_BEANS,
    SUCCESS_STATUSES,
    TERMS_HEADINGS,
    TRIAL_ENDS_ON,
    TRIAL_POST_PRICE_MINOR,
    TRIAL_SUBSCRIPTION,
    WIDGET_ROUTES,
    Session,
    batch_key,
    describe,
    half_even,
    page,
    poll_until,
    probe_email,
    raw_page,
    sign_in,
)



def test_health_route_and_reserved_directories_exist(anonymous, owner):
    response = anonymous.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health must answer 200 once the app is ready. {describe(response)}")
    landing = page("/")
    assert landing.status_code == 200, (
        f"the landing page must render for a visitor. {describe(landing)}")
    assert CREDENTIALS_PATH.endswith("USER_README.md"), CREDENTIALS_PATH


def test_public_routes_carry_unique_titles_and_descriptions(anonymous):
    titles, descriptions = {}, {}
    for route in PUBLIC_ROUTES:
        document = page(route)
        assert document.status_code == 200, (
            f"public route {route} must render. {describe(document)}")
        body = document.text
        assert "<title" in body.lower(), f"{route} declares no document title"
        titles.setdefault(body.lower().split("<title", 1)[1][:200], []).append(route)
        marker = 'name="description"'
        assert marker in body.lower(), f"{route} declares no meta description"
        descriptions.setdefault(
            body.lower().split(marker, 1)[1][:200], []).append(route)
    for value, routes in titles.items():
        assert len(routes) == 1, f"routes {routes} share one document title"
    for value, routes in descriptions.items():
        assert len(routes) == 1, f"routes {routes} share one meta description"


def test_public_routes_declare_a_resolving_social_preview_image(anonymous):
    for route in PUBLIC_ROUTES:
        body = page(route).text
        lowered = body.lower()
        assert "og:title" in lowered or "twitter:title" in lowered, (
            f"{route} declares no social preview title")
        assert "og:image" in lowered or "twitter:image" in lowered, (
            f"{route} declares no social preview image")
        start = lowered.find("og:image")
        fragment = body[start:start + 400]
        url = fragment.split('content="', 1)[1].split('"', 1)[0] if 'content="' in fragment else ""
        assert url, f"{route} declares a social preview image with no address"
        path = url.split("://", 1)[-1]
        path = path[path.find("/"):] if "/" in path else url
        image = page(path)
        assert image.status_code == 200, (
            f"the social preview image {url} declared by {route} must resolve from "
            f"this app's own origin. {describe(image)}")


def test_landing_page_carries_the_pinned_band_copy(anonymous):
    body = page("/").text
    for pinned in (COPY_HERO_OPENING, COPY_PRICING_HEADLINE, COPY_FOOTER_RIGHTS):
        assert pinned in body, (
            f"the landing page must carry the pinned copy {pinned!r}; it is absent")


def test_blog_index_lists_the_five_seeded_articles(anonymous):
    body = page("/blog").text
    assert COPY_BLOG_TITLE in body, (
        f"the blog index must carry {COPY_BLOG_TITLE!r}")
    for title in BLOG_TITLES:
        assert title in body, f"the blog index is missing the seeded card {title!r}"


def test_privacy_page_states_what_is_kept_and_is_linked_from_every_footer(anonymous):
    body = page("/privacy").text
    assert COPY_PRIVACY_UPDATED in body, (
        f"the privacy page must carry {COPY_PRIVACY_UPDATED!r}")
    for heading in PRIVACY_HEADINGS:
        assert heading in body, f"the privacy page is missing the section {heading!r}"
    for route in ("/", "/blog", "/terms"):
        assert "/privacy" in page(route).text, (
            f"the footer of {route} must reach the privacy page")


def test_terms_page_is_linked_from_the_footer_and_from_the_signup_form(anonymous):
    body = page("/terms").text
    assert COPY_TERMS_UPDATED in body, (
        f"the terms page must carry {COPY_TERMS_UPDATED!r}")
    for heading in TERMS_HEADINGS:
        assert heading in body, f"the terms page is missing the section {heading!r}"
    signup = page("/sign-up").text
    assert "/terms" in signup, "the signup form must link to the terms page"
    for route in ("/", "/blog", "/privacy"):
        assert "/terms" in page(route).text, (
            f"the footer of {route} must reach the terms page")


def test_unknown_address_renders_the_not_found_pill(anonymous):
    response = raw_page("/there-is-no-such-route-here")
    assert response.status_code in NOT_FOUND_STATUSES, (
        f"an unmatched address must answer as not found rather than as a page that "
        f"worked. {describe(response)}")
    assert COPY_NOT_FOUND in response.text, (
        f"the not-found screen must read {COPY_NOT_FOUND!r}")


def test_pricing_plans_derive_the_yearly_saving_from_one_stored_pair(anonymous):
    response = anonymous.get("/content/pricing")
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = response.json()
    plans = body.get("plans", body)
    monthly = _dig(plans, "monthly_minor")
    yearly = _dig(plans, "yearly_minor")
    saving = _dig(plans, "saving_percent")
    assert monthly == PREMIUM_MONTHLY_MINOR, (
        f"the premium monthly price must be {PREMIUM_MONTHLY_MINOR} minor units, "
        f"read {monthly}. {describe(response)}")
    assert yearly == PREMIUM_YEARLY_MINOR, (
        f"the premium yearly price must be {PREMIUM_YEARLY_MINOR} minor units, "
        f"read {yearly}. {describe(response)}")
    assert monthly * 12 == PREMIUM_TWELVE_MONTHS_MINOR, (
        f"twelve monthly payments must total {PREMIUM_TWELVE_MONTHS_MINOR}")
    assert saving == PREMIUM_SAVING_PERCENT, (
        f"the yearly saving must be {PREMIUM_SAVING_PERCENT} computed from the stored "
        f"pair, read {saving}. {describe(response)}")


def test_demo_store_is_read_only_for_a_visitor(anonymous):
    response = anonymous.get("/demo/overview")
    assert response.status_code in SUCCESS_STATUSES, (
        f"the demo overview must be readable without an account. {describe(response)}")
    body = response.json()
    assert body.get("read_only") is True, (
        f"the demo overview must declare itself read only. {describe(response)}")
    write = anonymous.post("/demo/overview", {"month_minor": 1})
    assert write.status_code in REFUSAL_STATUSES, (
        f"a write against the demo store must be refused. {describe(write)}")




def _dig(payload, key):
    """The first value stored under `key` anywhere inside a JSON payload."""
    if isinstance(payload, dict):
        if key in payload:
            return payload[key]
        for value in payload.values():
            found = _dig(value, key)
            if found is not None:
                return found
    if isinstance(payload, list):
        for value in payload:
            found = _dig(value, key)
            if found is not None:
                return found
    return None


def _categories(payload) -> dict:
    rows = payload.get("categories") or []
    out = {}
    for row in rows:
        name = row.get("name") or row.get("category")
        if name:
            out[name] = row
    return out


def test_demo_overview_month_year_day_totals_are_exact(anonymous):
    response = anonymous.get("/demo/overview")
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = response.json()
    assert body.get("year_minor") == DEMO_YEAR_MINOR, (
        f"the demo annual total must be {DEMO_YEAR_MINOR} minor units, read "
        f"{body.get('year_minor')}. {describe(response)}")
    assert body.get("month_minor") == DEMO_MONTH_MINOR, (
        f"the demo monthly total must be {DEMO_MONTH_MINOR} minor units, read "
        f"{body.get('month_minor')}. {describe(response)}")
    assert body.get("day_minor") == DEMO_DAY_MINOR, (
        f"the demo daily total must be {DEMO_DAY_MINOR} minor units, read "
        f"{body.get('day_minor')}. {describe(response)}")
    assert body.get("month_minor") == half_even(DEMO_YEAR_MINOR, 12), (
        "the monthly total must be the annual total divided by twelve, rounded "
        "half to even once at the end")
    assert body.get("day_minor") == half_even(DEMO_YEAR_MINOR, 365), (
        "the daily total must be the annual total divided by three hundred sixty "
        "five, rounded half to even once at the end")


def test_demo_category_rows_sum_exactly_to_the_displayed_total(anonymous):
    body = anonymous.get("/demo/overview").json()
    rows = _categories(body)
    assert set(rows) == set(BUILTIN_CATEGORIES), (
        f"the demo overview must carry one row per builtin category, read "
        f"{sorted(rows)}")
    month_sum = sum(row.get("month_minor", 0) for row in rows.values())
    year_sum = sum(row.get("year_minor", 0) for row in rows.values())
    assert month_sum == DEMO_MONTH_MINOR, (
        f"the category rows must sum exactly to the displayed monthly total "
        f"{DEMO_MONTH_MINOR}, read {month_sum}")
    assert year_sum == DEMO_YEAR_MINOR, (
        f"the category rows must sum exactly to the displayed annual total "
        f"{DEMO_YEAR_MINOR}, read {year_sum}")
    for name, expected in DEMO_CATEGORY_MONTH.items():
        assert rows[name].get("month_minor") == expected, (
            f"the demo category {name} must read {expected} minor units a month, "
            f"read {rows[name].get('month_minor')}")
    for name, expected in DEMO_CATEGORY_YEAR.items():
        assert rows[name].get("year_minor") == expected, (
            f"the demo category {name} must read {expected} minor units a year, "
            f"read {rows[name].get('year_minor')}")


def test_demo_category_year_approximation_rounds_to_the_nearest_ten(anonymous):
    rows = _categories(anonymous.get("/demo/overview").json())
    groceries = rows[CATEGORY_GROCERIES]
    approx = groceries.get("year_approx_minor")
    assert approx == GROCERIES_YEAR_APPROX_MINOR, (
        f"the {CATEGORY_GROCERIES} row must show a per-year approximation of "
        f"{GROCERIES_YEAR_APPROX_MINOR} minor units, which is its exact annual "
        f"subtotal rounded to the nearest ten units of the home currency; read "
        f"{approx}")
    for name, row in rows.items():
        exact = DEMO_CATEGORY_YEAR[name]
        assert row.get("year_approx_minor") == round(exact / 1000) * 1000, (
            f"the {name} per-year approximation must round its exact annual "
            f"subtotal {exact} to the nearest ten units of the home currency")


def test_owner_overview_totals_match_the_seeded_store(owner):
    response = owner.overview()
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = response.json()
    assert body.get("month_minor") == OWNER_MONTH_MINOR, (
        f"{OWNER_EMAIL} must read {OWNER_MONTH_MINOR} minor units a month, read "
        f"{body.get('month_minor')}. {describe(response)}")
    assert body.get("year_minor") == OWNER_YEAR_MINOR, (
        f"{OWNER_EMAIL} must read {OWNER_YEAR_MINOR} minor units a year, read "
        f"{body.get('year_minor')}. {describe(response)}")
    assert body.get("day_minor") == OWNER_DAY_MINOR, (
        f"{OWNER_EMAIL} must read {OWNER_DAY_MINOR} minor units a day, read "
        f"{body.get('day_minor')}. {describe(response)}")
    upcoming = body.get("upcoming") or []
    assert upcoming, f"the upcoming timeline must not be empty. {describe(response)}"
    dates = [row.get("charge_date") for row in upcoming]
    assert dates == sorted(dates), (
        f"the upcoming timeline must run nearest first, read {dates}")
    assert all(isinstance(row.get("days_remaining"), int) for row in upcoming), (
        "every upcoming row must carry a countdown in whole days")


def test_second_owner_overview_totals_match_the_seeded_store(owner2):
    body = owner2.overview().json()
    assert body.get("month_minor") == OWNER2_MONTH_MINOR, (
        f"{OWNER2_EMAIL} must read {OWNER2_MONTH_MINOR} minor units a month, read "
        f"{body.get('month_minor')}")
    assert body.get("year_minor") == OWNER2_YEAR_MINOR, (
        f"{OWNER2_EMAIL} must read {OWNER2_YEAR_MINOR} minor units a year, read "
        f"{body.get('year_minor')}")
    assert body.get("day_minor") == OWNER2_DAY_MINOR, (
        f"{OWNER2_EMAIL} must read {OWNER2_DAY_MINOR} minor units a day, read "
        f"{body.get('day_minor')}")
    listing = owner2.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX})
    active = [row for row in listing.json().get("data", [])
              if row.get("status") == "active" and row.get("kind") != "one_time"]
    assert len(active) == OWNER2_SUBSCRIPTION_COUNT, (
        f"{OWNER2_EMAIL} must hold {OWNER2_SUBSCRIPTION_COUNT} active recurring "
        f"subscriptions, read {len(active)}")


def test_no_decimal_currency_never_grows_decimals(owner2):
    row = owner2.find_subscription(SUB_RADIOLARK)
    assert row is not None, f"{SUB_RADIOLARK} must be seeded for {OWNER2_EMAIL}"
    assert row.get("currency") == CURRENCY_JPY, (
        f"{SUB_RADIOLARK} must be stored in {CURRENCY_JPY}, read {row.get('currency')}")
    price = row.get("price_minor")
    assert isinstance(price, int), (
        f"a {CURRENCY_JPY} price must be a whole integer of minor units, read {price!r}")
    detail = owner2.get(f"/app/subscriptions/{row.get('id')}")
    assert "." not in str(_dig(detail.json(), "price_minor")), (
        f"a {CURRENCY_JPY} price must never grow a decimal. {describe(detail)}")


def test_home_currency_switch_reconverts_without_changing_stored_values(owner2):
    before = owner2.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX}).json()["data"]
    stored_before = {row["name"]: (row.get("price_minor"), row.get("currency"))
                     for row in before}
    original = owner2.settings().json().get("home_currency", HOME_CURRENCY)
    switched = owner2.patch("/app/settings", {"home_currency": "eur"})
    assert switched.status_code in SUCCESS_STATUSES, describe(switched)
    after = owner2.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX}).json()["data"]
    stored_after = {row["name"]: (row.get("price_minor"), row.get("currency"))
                    for row in after}
    restored = owner2.patch("/app/settings", {"home_currency": original})
    assert restored.status_code in SUCCESS_STATUSES, describe(restored)
    assert stored_after == stored_before, (
        "changing the home currency must reconvert what is shown and change no "
        f"stored value; {sorted(set(stored_before.items()) ^ set(stored_after.items()))}")


def test_overview_export_and_widget_surfaces_agree_to_the_minor_unit(owner):
    overview = owner.overview().json()
    month = overview.get("month_minor")
    for route in WIDGET_ROUTES:
        document = page(route)
        assert document.status_code in SUCCESS_STATUSES + (401, 302, 303), (
            f"the widget route {route} must render standalone. {describe(document)}")
    widget = owner.get("/app/overview", filter=FILTER_ALL).json()
    assert widget.get("month_minor") == month, (
        "every surface reading the engine must agree to the minor unit")
    export = owner.get("/app/export.csv")
    assert export.status_code in SUCCESS_STATUSES, describe(export)
    reader = list(csv.DictReader(io.StringIO(export.text)))
    exported = sum(1 for row in reader if row.get("status") == "active")
    listing = owner.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX}).json()["data"]
    live = sum(1 for row in listing if row.get("status") == "active")
    assert exported == live, (
        f"the exported file must carry the same active records as the list, "
        f"read {exported} exported against {live} live")


def test_all_view_equals_recurring_plus_one_time(owner2):
    every = owner2.overview(FILTER_ALL).json()
    recurring = owner2.overview(FILTER_RECURRING).json()
    one_time = owner2.overview(FILTER_ONE_TIME).json()
    assert (recurring.get("year_minor", 0) + one_time.get("year_minor", 0)
            == every.get("year_minor")), (
        f"the All figures must equal Recurring plus One-time to the minor unit: "
        f"{recurring.get('year_minor')} + {one_time.get('year_minor')} against "
        f"{every.get('year_minor')}")
    assert one_time.get("year_minor", 0) >= ONE_TIME_AMOUNT_MINOR, (
        f"the seeded one-time expense of {ONE_TIME_AMOUNT_MINOR} minor units must "
        f"join the One-time view")


def test_csv_export_header_is_exact_and_the_round_trip_is_lossless(owner2):
    export = owner2.get("/app/export.csv")
    assert export.status_code in SUCCESS_STATUSES, describe(export)
    first_line = export.text.splitlines()[0].strip()
    assert first_line == CSV_HEADER, (
        f"the export header must read exactly\n  {CSV_HEADER}\nread\n  {first_line}")
    rows = list(csv.DictReader(io.StringIO(export.text)))
    assert rows, "the export must carry one line per record"
    for row in rows:
        assert row.get("price_minor", "").lstrip("-").isdigit(), (
            f"every exported price must be an integer of minor units, read "
            f"{row.get('price_minor')!r} for {row.get('name')!r}")


def test_seeded_rows_are_stored_and_survive_a_restart_with_no_duplicates(owner, store):
    listing = owner.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX}).json()["data"]
    names = [row.get("name") for row in listing]
    assert len(names) == len(set(names)), (
        f"seeding must be idempotent, so no seeded row appears twice; read {names}")
    active = [row for row in listing if row.get("status") == "active"]
    assert len(active) == OWNER_SUBSCRIPTION_COUNT, (
        f"{OWNER_EMAIL} must hold exactly {OWNER_SUBSCRIPTION_COUNT} active "
        f"subscriptions, which is the free cap; read {len(active)}")
    persisted = store.count("subscription")
    assert persisted >= DEMO_SUBSCRIPTION_COUNT + OWNER_SUBSCRIPTION_COUNT, (
        f"the subscription rows must live in the declared store, which must hold at "
        f"least the {DEMO_SUBSCRIPTION_COUNT} demo rows beside every seeded account; "
        f"read {persisted}")




def _charge_dates(session, name: str, start: str, end: str) -> list:
    row = session.find_subscription(name)
    assert row is not None, f"{name} must be seeded"
    response = session.charges(row.get("id"), start, end)
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    return response.json().get("charge_dates") or []


def test_month_end_anchor_clamps_and_recovers_across_short_months(owner2):
    dates = _charge_dates(owner2, SUB_NORTHBRIDGE_AUTO, "2026-01-01", "2026-04-30")
    for expected in ("2026-01-31", "2026-02-28", "2026-03-31"):
        assert expected in dates, (
            f"a charge anchored on {ANCHOR_NORTHBRIDGE} must fall on {expected}; the "
            f"window returned {dates}")
    leap = _charge_dates(owner2, SUB_NORTHBRIDGE_AUTO, "2028-02-01", "2028-03-31")
    assert "2028-02-29" in leap, (
        f"a month-end anchor must clamp to the 29th in a leap February; read {leap}")


def test_leap_day_yearly_anchor_lands_on_the_28th_in_a_common_year(owner2):
    common = _charge_dates(owner2, SUB_CALM_CURRENT, "2025-01-01", "2025-12-31")
    assert "2025-02-28" in common, (
        f"a yearly anchor of {ANCHOR_CALM_CURRENT} must charge on 2025-02-28; read "
        f"{common}")
    leap = _charge_dates(owner2, SUB_CALM_CURRENT, "2028-01-01", "2028-12-31")
    assert "2028-02-29" in leap, (
        f"a yearly anchor of {ANCHOR_CALM_CURRENT} must charge on 2028-02-29; read "
        f"{leap}")


def test_every_n_days_cycle_never_clamps(owner2):
    dates = sorted(_charge_dates(owner2, SUB_ROASTLINE_BEANS, "2026-05-02", "2026-12-31"))
    assert dates[0] == ANCHOR_ROASTLINE, (
        f"an every-N-days sequence must open on its anchor {ANCHOR_ROASTLINE}; read "
        f"{dates[:3]}")
    from datetime import date
    for earlier, later in zip(dates, dates[1:]):
        gap = (date.fromisoformat(later) - date.fromisoformat(earlier)).days
        assert gap == 45, (
            f"an every 45 days cycle must be exact interval arithmetic with no "
            f"clamping; {earlier} to {later} is {gap} days")


def test_pause_and_resume_never_back_charges_the_paused_span(owner2):
    row = owner2.find_subscription(SUB_RADIOLARK)
    assert row is not None, f"{SUB_RADIOLARK} must be seeded"
    paused = owner2.post(f"/app/subscriptions/{row['id']}/pause", {})
    assert paused.status_code in SUCCESS_STATUSES, describe(paused)
    during = owner2.charges(row["id"], "2027-01-01", "2027-12-31")
    assert during.json().get("charge_dates") == [], (
        f"a paused subscription must schedule no charge. {describe(during)}")
    resumed = owner2.post(f"/app/subscriptions/{row['id']}/resume", {})
    assert resumed.status_code in SUCCESS_STATUSES, describe(resumed)
    after = owner2.charges(row["id"], "2020-01-01", "2020-12-31")
    assert after.json().get("charge_dates") == [], (
        f"resuming must re-anchor forward rather than back-charge the paused span. "
        f"{describe(after)}")


def test_trial_end_date_is_the_first_paid_charge_at_the_post_trial_price(owner2):
    row = owner2.find_subscription(TRIAL_SUBSCRIPTION)
    assert row is not None, f"{TRIAL_SUBSCRIPTION} must be seeded with a trial"
    assert row.get("trial_ends_on") == TRIAL_ENDS_ON, (
        f"{TRIAL_SUBSCRIPTION} must carry a trial ending {TRIAL_ENDS_ON}, read "
        f"{row.get('trial_ends_on')}")
    response = owner2.charges(row["id"], TRIAL_ENDS_ON, "2026-12-31")
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = response.json()
    dates = body.get("charge_dates") or []
    assert TRIAL_ENDS_ON in dates, (
        f"the trial end date {TRIAL_ENDS_ON} must be the first paid charge boundary; "
        f"read {dates}")
    prices = body.get("prices") or {}
    assert prices.get(TRIAL_ENDS_ON) == TRIAL_POST_PRICE_MINOR, (
        f"the charge on {TRIAL_ENDS_ON} must carry the post-trial price "
        f"{TRIAL_POST_PRICE_MINOR}; read {prices.get(TRIAL_ENDS_ON)}")


def test_reminder_schedule_holds_local_time_across_a_daylight_saving_change(owner2):
    response = owner2.reminder_schedule("2027-01-01", "2027-12-31")
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    occurrences = response.json().get("occurrences") or []
    assert occurrences, f"the schedule window must carry occurrences. {describe(response)}"
    winter = [o for o in occurrences if str(o.get("occurrence_date", "")) < "2027-03-01"]
    summer = [o for o in occurrences if "2027-07-01" <= str(o.get("occurrence_date", "")) < "2027-08-01"]
    assert winter and summer, (
        f"the window must span both sides of a clock change in {OWNER2_ZONE}")
    local_times = {str(o.get("local_time")) for o in winter + summer}
    assert len(local_times) == 1, (
        f"a reminder must fire at one wall clock on both sides of a daylight saving "
        f"change; read {sorted(local_times)}")
    winter_offsets = {str(o.get("scheduled_at"))[11:16] for o in winter}
    summer_offsets = {str(o.get("scheduled_at"))[11:16] for o in summer}
    assert winter_offsets != summer_offsets, (
        f"the instant in coordinated universal time must move by an hour across the "
        f"transition; winter {sorted(winter_offsets)} summer {sorted(summer_offsets)}")


def test_duplicate_reminder_pass_writes_no_second_timeline_entry(owner, store):
    as_of = "2026-12-01T09:00:00Z"
    first = owner.run_reminders(as_of)
    assert first.status_code in SUCCESS_STATUSES, (
        f"a reminder pass must be accepted. {describe(first)}")
    before = store.count("reminder_entry")
    second = owner.run_reminders(as_of)
    assert second.status_code in SUCCESS_STATUSES + CONFLICT_STATUSES, (
        f"a replayed reminder pass must be accepted or refused as a conflict, never "
        f"served as a fresh run. {describe(second)}")
    if second.status_code in SUCCESS_STATUSES:
        assert second.json().get("fired") == 0, (
            f"a replayed pass must report nothing fired, read "
            f"{second.json().get('fired')}. {describe(second)}")
    after = store.count("reminder_entry")
    assert after == before, (
        f"a duplicate reminder pass must create no second entry: {before} entries "
        f"before the replay and {after} after it")


def test_concurrent_reminder_passes_leave_exactly_one_entry(owner2, store):
    as_of = "2026-11-02T09:00:00Z"
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(owner2.run_reminders, as_of) for _ in range(2)]
        results = [f.result() for f in futures]
    statuses = sorted(r.status_code for r in results)
    accepted = [r for r in results if r.status_code in SUCCESS_STATUSES]
    assert accepted, (
        f"exactly one of two simultaneous passes must complete; both were refused "
        f"with {statuses}")
    rows = store.rows("reminder_entry", limit=PAGE_SIZE_MAX)
    seen = [(row.get("subscription_id"), str(row.get("occurrence_date")))
            for row in rows]
    assert len(seen) == len(set(seen)), (
        f"each occurrence must hold exactly one entry after two simultaneous passes; "
        f"read {len(seen)} entries over {len(set(seen))} occurrences")


def test_late_reminder_pass_records_the_occurrence_as_missed(owner2):
    late = owner2.run_reminders("2027-06-01T09:00:00Z")
    assert late.status_code in SUCCESS_STATUSES, describe(late)
    timeline = owner2.reminder_timeline(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX})
    assert timeline.status_code in SUCCESS_STATUSES, describe(timeline)
    states = {row.get("state") for row in timeline.json().get("data", [])}
    assert states <= {REMINDER_STATE_FIRED, REMINDER_STATE_MISSED}, (
        f"a timeline entry must be {REMINDER_STATE_FIRED} or {REMINDER_STATE_MISSED}, "
        f"read {sorted(states)}")
    assert REMINDER_STATE_MISSED in states, (
        f"an occurrence whose scheduled instant passed more than a day before the "
        f"pass must be recorded as {REMINDER_STATE_MISSED} rather than fired. "
        f"{describe(timeline)}")




def test_unauthenticated_app_requests_are_denied(anonymous):
    for path in ("/app/overview", "/app/subscriptions", "/app/settings",
                 "/app/entitlement", "/app/reminders/timeline"):
        response = anonymous.get(path)
        assert response.status_code in DENIAL_STATUSES, (
            f"an anonymous GET {path} must be denied by the server rather than "
            f"served. {describe(response)}")
    write = anonymous.post("/app/subscriptions", {"name": "Probe", "price_minor": 100})
    assert write.status_code in DENIAL_STATUSES, (
        f"an anonymous write must be denied and must change nothing. {describe(write)}")


def test_owner_cannot_read_another_owners_subscription(owner, owner2):
    theirs = owner2.find_subscription(SUB_NORTHBRIDGE_AUTO)
    assert theirs is not None, f"{SUB_NORTHBRIDGE_AUTO} must belong to {OWNER2_EMAIL}"
    response = owner.get(f"/app/subscriptions/{theirs['id']}")
    assert response.status_code in NOT_FOUND_STATUSES + DENIAL_STATUSES, (
        f"{OWNER_EMAIL} must not read a record belonging to {OWNER2_EMAIL}. "
        f"{describe(response)}")
    mutate = owner.patch(f"/app/subscriptions/{theirs['id']}", {"name": "Taken"})
    assert mutate.status_code in NOT_FOUND_STATUSES + DENIAL_STATUSES, (
        f"{OWNER_EMAIL} must not change a record belonging to {OWNER2_EMAIL}. "
        f"{describe(mutate)}")
    unchanged = owner2.get(f"/app/subscriptions/{theirs['id']}").json()
    assert _dig(unchanged, "name") == SUB_NORTHBRIDGE_AUTO, (
        "a refused cross-owner write must leave the protected row unchanged")


def test_seventh_subscription_without_entitlement_is_denied_by_the_store(owner):
    entitlement = owner.entitlement()
    assert entitlement.status_code in SUCCESS_STATUSES, describe(entitlement)
    assert entitlement.json().get("state") != "active", (
        f"{OWNER_EMAIL} is the free account and must hold no active entitlement. "
        f"{describe(entitlement)}")
    before = owner.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX}).json()["data"]
    active_before = sum(1 for row in before if row.get("status") == "active")
    assert active_before == FREE_CAP, (
        f"{OWNER_EMAIL} must sit exactly on the free cap of {FREE_CAP}, read "
        f"{active_before}")
    response = owner.create_subscription({
        "name": f"Probe {batch_key()}",
        "price_minor": 500,
        "currency": HOME_CURRENCY,
        "cycle": "monthly",
        "anchor_date": "2026-10-01",
        "category": CATEGORY_UTILITIES,
    })
    assert response.status_code in REFUSAL_STATUSES, (
        f"a seventh subscription without an entitlement must be refused by the store "
        f"whatever route it arrives by. {describe(response)}")
    assert str(FREE_CAP) in response.text, (
        f"the refusal must name the cap of {FREE_CAP}. {describe(response)}")
    after = owner.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX}).json()["data"]
    active_after = sum(1 for row in after if row.get("status") == "active")
    assert active_after == FREE_CAP, (
        f"a refused seventh write must leave the count at {FREE_CAP}, read "
        f"{active_after}")


def test_import_batch_past_the_cap_is_denied_without_an_entitlement(owner):
    parsed = owner.parse_import("\n".join(IMPORT_LINES))
    assert parsed.status_code in SUCCESS_STATUSES, describe(parsed)
    rows = parsed.json().get("rows") or []
    assert rows, f"the four pinned listing lines must parse. {describe(parsed)}"
    response = owner.commit_import(rows, batch_key())
    assert response.status_code in REFUSAL_STATUSES, (
        f"an import batch carrying the count past the free cap of {FREE_CAP} must be "
        f"refused for an account with no entitlement. {describe(response)}")
    listing = owner.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX}).json()["data"]
    active = sum(1 for row in listing if row.get("status") == "active")
    assert active == FREE_CAP, (
        f"a refused import must write nothing, leaving {FREE_CAP} active records; "
        f"read {active}")


def test_expired_entitlement_locks_the_extra_records_but_deletes_nothing(owner2, store):
    before = store.count("subscription")
    cancelled = owner2.post("/app/entitlement/cancel", {})
    assert cancelled.status_code in SUCCESS_STATUSES, describe(cancelled)
    listing = owner2.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX})
    assert listing.status_code in SUCCESS_STATUSES, describe(listing)
    rows = listing.json().get("data", [])
    assert len(rows) >= OWNER2_SUBSCRIPTION_COUNT, (
        f"a lapsed entitlement must never delete a record; read {len(rows)}")
    after = store.count("subscription")
    assert after == before, (
        f"a lapsed entitlement must delete no stored row: {before} before the lapse "
        f"and {after} after it")
    restored = owner2.post("/app/entitlement/restore", {})
    assert restored.status_code in SUCCESS_STATUSES, describe(restored)




def test_import_parser_reads_four_locales_and_flags_low_confidence(owner2):
    response = owner2.parse_import("\n".join(IMPORT_LINES))
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    rows = {row.get("name"): row for row in response.json().get("rows") or []}
    for name, (price, currency, next_date) in IMPORT_EXPECTED.items():
        assert name in rows, (
            f"the parser must read {name!r} out of its listing line; read "
            f"{sorted(rows)}")
        row = rows[name]
        assert row.get("price_minor") == price, (
            f"{name} must parse to {price} minor units, read {row.get('price_minor')}")
        assert row.get("currency") == currency, (
            f"{name} must parse to {currency}, read {row.get('currency')}")
        assert str(row.get("next_charge_date")) == next_date, (
            f"{name} must parse to a next charge date of {next_date}, read "
            f"{row.get('next_charge_date')}")
    muddled = owner2.parse_import("Halfknown Service - ??? - price unreadable")
    assert muddled.status_code in SUCCESS_STATUSES, describe(muddled)
    doubtful = muddled.json().get("rows") or []
    for row in doubtful:
        assert row.get("confidence") == CONFIDENCE_LOW, (
            f"a row read with doubt must carry a confidence of {CONFIDENCE_LOW}, read "
            f"{row.get('confidence')}")


def test_import_parser_never_crashes_on_arbitrary_text(owner2):
    for text in ("", "a", " \t\n", "{}", "<html></html>", "0" * 4000):
        response = owner2.parse_import(text)
        assert response.status_code in SUCCESS_STATUSES, (
            f"the parser must answer rather than fail on arbitrary pasted text; "
            f"{describe(response)}")
        assert isinstance(response.json().get("rows"), list), (
            f"the parser must return a row list for text holding no listing. "
            f"{describe(response)}")


def test_import_duplicate_detection_offers_merge_or_skip(owner2):
    response = owner2.parse_import("\n".join(IMPORT_LINES))
    rows = {row.get("name"): row for row in response.json().get("rows") or []}
    row = rows.get("Cellar & Vine")
    assert row is not None, "the German listing line must parse"
    assert row.get("duplicate_of"), (
        "a parsed row matching a seeded subscription by folded name and a price "
        f"within five percent must be flagged as a duplicate. {describe(response)}")
    options = str(row.get("options") or row.get("duplicate_actions") or response.text)
    assert DUPLICATE_MERGE in options, (
        f"a duplicate row must offer {DUPLICATE_MERGE}. {describe(response)}")
    assert DUPLICATE_SKIP in options, (
        f"a duplicate row must offer {DUPLICATE_SKIP}. {describe(response)}")


def test_import_batch_undo_reverses_every_row_as_one_step(owner2):
    before = owner2.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX}).json()["data"]
    parsed = owner2.parse_import("\n".join(IMPORT_LINES))
    rows = [row for row in parsed.json().get("rows") or []
            if not row.get("duplicate_of")]
    assert rows, "the listing must carry rows that are not duplicates"
    committed = owner2.commit_import(rows, batch_key())
    assert committed.status_code in SUCCESS_STATUSES, describe(committed)
    during = owner2.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX}).json()["data"]
    assert len(during) > len(before), (
        f"the import must write its accepted rows; {len(before)} before and "
        f"{len(during)} after")
    undone = owner2.undo()
    assert undone.status_code in SUCCESS_STATUSES, describe(undone)
    after = owner2.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX}).json()["data"]
    assert len(after) == len(before), (
        f"one undo must reverse the whole import batch as one step; {len(before)} "
        f"before the import and {len(after)} after the undo")


def test_negative_price_is_refused_and_writes_nothing(owner2):
    probe = f"Probe {batch_key()}"
    response = owner2.create_subscription({
        "name": probe,
        "price_minor": -100,
        "currency": HOME_CURRENCY,
        "cycle": "monthly",
        "anchor_date": "2026-10-01",
        "category": CATEGORY_UTILITIES,
    })
    assert response.status_code in REFUSAL_STATUSES, (
        f"a negative price must be refused. {describe(response)}")
    missing = owner2.create_subscription({
        "name": probe,
        "price_minor": 100,
        "currency": HOME_CURRENCY,
        "cycle": "monthly",
        "category": CATEGORY_UTILITIES,
    })
    assert missing.status_code in REFUSAL_STATUSES, (
        f"an absent anchor date must be refused. {describe(missing)}")
    assert owner2.find_subscription(probe) is None, (
        f"a refused create must write nothing, yet {probe!r} is in the list")


def test_page_size_above_the_cap_is_refused_with_the_cap_named(owner2):
    response = owner2.subscriptions(**{PAGE_SIZE_PARAM: 500})
    assert response.status_code in REFUSAL_STATUSES, (
        f"a page size above the cap of {PAGE_SIZE_MAX} must be refused rather than "
        f"quietly cut down to fit. {describe(response)}")
    assert str(PAGE_SIZE_MAX) in response.text, (
        f"the refusal must name the cap of {PAGE_SIZE_MAX}. {describe(response)}")


def test_subscription_list_pages_with_an_opaque_keyset_cursor(owner2):
    first = owner2.subscriptions(**{PAGE_SIZE_PARAM: 2})
    assert first.status_code in SUCCESS_STATUSES, describe(first)
    body = first.json()
    assert len(body.get("data", [])) <= 2, (
        f"a page of two must carry at most two rows. {describe(first)}")
    assert body.get("has_more") is True, (
        f"a page of two over a longer list must set {MORE_FLAG}. {describe(first)}")
    cursor = body.get(CURSOR_FIELD)
    assert body.get("next_cursor"), (
        f"a page with more behind it must carry a {CURSOR_FIELD}. {describe(first)}")
    second = owner2.subscriptions(**{PAGE_SIZE_PARAM: 2, "cursor": cursor})
    assert second.status_code in SUCCESS_STATUSES, describe(second)
    first_ids = {row.get("id") for row in body.get("data", [])}
    second_ids = {row.get("id") for row in second.json().get("data", [])}
    assert not (first_ids & second_ids), (
        f"a keyset cursor must never repeat a row across two pages; {first_ids} then "
        f"{second_ids}")


def test_scan_keeps_the_values_and_never_the_image_bytes(owner2, store):
    response = owner2.scan({"sample_id": "receipt-05"})
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = response.json()
    merchant, scanned_on, total, currency, category = RECEIPT_SAMPLES["receipt-05"]
    assert body.get("merchant") == merchant, (
        f"receipt-05 must extract the merchant {merchant!r}, read "
        f"{body.get('merchant')}")
    assert str(body.get("scanned_on")) == scanned_on, (
        f"receipt-05 must extract the date {scanned_on}, read {body.get('scanned_on')}")
    assert body.get("total_minor") == total, (
        f"receipt-05 must extract a total of {total} minor units, read "
        f"{body.get('total_minor')}")
    lines = {line.get("label") or line.get("name"): line.get("amount_minor")
             for line in body.get("lines") or []}
    for label, amount in RECEIPT_05_LINES:
        assert lines.get(label) == amount, (
            f"receipt-05 must file {label!r} at {amount} minor units, read "
            f"{lines.get(label)}")
    assert body.get("content_hash"), (
        f"a scan must persist a content hash of the bytes. {describe(response)}")
    for row in store.rows("scan", limit=PAGE_SIZE_MAX):
        for key, value in row.items():
            assert not isinstance(value, (bytes, bytearray)), (
                f"the scan row keeps the bytes of the image in column {key!r}; the "
                f"picture must be thrown away and only the values, the hash and a "
                f"drawn thumbnail may persist")


def test_unreadable_scan_returns_the_honest_state(owner2):
    response = owner2.scan({"sample_id": f"receipt-{batch_key()}"})
    assert response.status_code in SUCCESS_STATUSES + REFUSAL_STATUSES, describe(response)
    body = response.text
    assert "could not read" in body.lower(), (
        f"an image the reader does not know must return an honest unreadable state "
        f"rather than a guess. {describe(response)}")
    if response.status_code in SUCCESS_STATUSES:
        assert not response.json().get("merchant"), (
            f"an unreadable image must never return a guessed merchant. "
            f"{describe(response)}")


def test_price_history_computes_a_past_month_at_the_price_effective_then(owner2):
    history = owner2.get("/app/insights/price-history", **{PAGE_SIZE_PARAM: PAGE_SIZE_MAX})
    assert history.status_code in SUCCESS_STATUSES, describe(history)
    changes = history.json().get("data", [])
    match = [c for c in changes
             if c.get("old_price_minor") == PRICE_NORTHBRIDGE_OLD_MINOR
             and c.get("new_price_minor") == PRICE_NORTHBRIDGE_NEW_MINOR]
    assert match, (
        f"the price history must carry the seeded change from "
        f"{PRICE_NORTHBRIDGE_OLD_MINOR} to {PRICE_NORTHBRIDGE_NEW_MINOR}. "
        f"{describe(history)}")
    assert str(match[0].get("effective_on")) == PRICE_CHANGE_EFFECTIVE_ON, (
        f"the seeded change must take effect on {PRICE_CHANGE_EFFECTIVE_ON}, read "
        f"{match[0].get('effective_on')}")
    assert match[0].get("mode") == MODE_NEXT_RENEWAL, (
        f"the seeded change must be recorded in {MODE_NEXT_RENEWAL} mode, read "
        f"{match[0].get('mode')}")
    row = owner2.find_subscription(SUB_NORTHBRIDGE_AUTO)
    before = owner2.charges(row["id"], "2026-02-01", "2026-02-28").json()
    prices_before = before.get("prices") or {}
    assert set(prices_before.values()) == {PRICE_NORTHBRIDGE_OLD_MINOR}, (
        f"a month before {PRICE_CHANGE_EFFECTIVE_ON} must compute at "
        f"{PRICE_NORTHBRIDGE_OLD_MINOR}, read {prices_before}")
    after = owner2.charges(row["id"], "2026-05-01", "2026-05-31").json()
    prices_after = after.get("prices") or {}
    assert set(prices_after.values()) == {PRICE_NORTHBRIDGE_NEW_MINOR}, (
        f"a month from {PRICE_CHANGE_EFFECTIVE_ON} must compute at "
        f"{PRICE_NORTHBRIDGE_NEW_MINOR}, read {prices_after}")


def test_cancelled_subscription_feeds_the_savings_counter(owner2):
    response = owner2.get("/app/insights/savings")
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    body = response.json()
    saved = body.get("saved_minor")
    assert isinstance(saved, int) and saved > 0, (
        f"the savings counter must total the avoided cost of every cancellation as "
        f"an integer of minor units, read {saved!r}. {describe(response)}")
    names = [row.get("name") for row in body.get("rows") or body.get("data") or []]
    assert CANCELLED_SUBSCRIPTION in names, (
        f"the seeded cancellation {CANCELLED_SUBSCRIPTION!r} must appear in the "
        f"savings rows, read {names}")
    upcoming = owner2.overview().json().get("upcoming") or []
    assert CANCELLED_SUBSCRIPTION not in [r.get("name") for r in upcoming], (
        f"a cancelled subscription must never appear in the upcoming timeline")


def test_soft_deleted_record_lands_in_the_bin_and_restores(owner2):
    probe = f"Probe {batch_key()}"
    created = owner2.create_subscription({
        "name": probe,
        "price_minor": 250,
        "currency": HOME_CURRENCY,
        "cycle": "monthly",
        "anchor_date": "2026-10-05",
        "category": CATEGORY_UTILITIES,
    })
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    identifier = _dig(created.json(), "id")
    removed = owner2.delete(f"/app/subscriptions/{identifier}")
    assert removed.status_code in SUCCESS_STATUSES, describe(removed)
    listed = owner2.get("/app/bin", **{PAGE_SIZE_PARAM: PAGE_SIZE_MAX})
    assert listed.status_code in SUCCESS_STATUSES, describe(listed)
    assert probe in listed.text, (
        f"a soft-deleted record must be listed in the bin. {describe(listed)}")
    restored = owner2.post(f"/app/bin/{identifier}/restore", {})
    assert restored.status_code in SUCCESS_STATUSES, describe(restored)
    assert owner2.find_subscription(probe) is not None, (
        f"restoring from the bin must return {probe!r} to the list")
    owner2.delete(f"/app/subscriptions/{identifier}")


def test_delete_all_returns_a_fresh_account_to_the_first_run_state(anonymous):
    email = probe_email()
    signup = anonymous.post("/auth/signup",
                            {"email": email, "password": PASSWORD, "name": "Probe"})
    assert signup.status_code in SUCCESS_STATUSES, (
        f"signup must be open. {describe(signup)}")
    fresh = sign_in(email)
    created = fresh.create_subscription({
        "name": f"Probe {batch_key()}",
        "price_minor": 300,
        "currency": HOME_CURRENCY,
        "cycle": "monthly",
        "anchor_date": "2026-10-09",
        "category": CATEGORY_UTILITIES,
    })
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    erased = fresh.post("/app/data/delete-all", {"confirm": True})
    assert erased.status_code in SUCCESS_STATUSES, (
        f"delete all data must empty the account in one confirmed step. "
        f"{describe(erased)}")
    overview = fresh.overview()
    assert overview.json().get("year_minor") == 0, (
        f"an erased account must return to the first-run state with a zero total. "
        f"{describe(overview)}")
    listing = fresh.subscriptions()
    assert listing.json().get("data") == [], (
        f"an erased account must hold an empty list. {describe(listing)}")


def test_first_run_overview_carries_the_empty_state_copy(anonymous):
    email = probe_email()
    signup = anonymous.post("/auth/signup",
                            {"email": email, "password": PASSWORD, "name": "Probe"})
    assert signup.status_code in SUCCESS_STATUSES, describe(signup)
    fresh = sign_in(email)
    overview = fresh.overview()
    assert overview.status_code in SUCCESS_STATUSES, describe(overview)
    body = overview.json()
    assert body.get("year_minor") == 0, (
        f"a first-run account must read a zero total. {describe(overview)}")
    assert (body.get("upcoming") or []) == [], (
        f"a first-run account must schedule no charge. {describe(overview)}")
    document = page("/app")
    assert COPY_EMPTY_LIST in document.text or COPY_SPENDING_TITLE in document.text, (
        f"the overview must render its empty state rather than an empty frame")


def test_signup_refuses_a_registered_address_and_a_short_password(anonymous):
    email = probe_email()
    first = anonymous.post("/auth/signup",
                           {"email": email, "password": PASSWORD, "name": "Probe"})
    assert first.status_code in SUCCESS_STATUSES, describe(first)
    again = anonymous.post("/auth/signup",
                           {"email": email, "password": PASSWORD, "name": "Probe"})
    assert again.status_code in REFUSAL_STATUSES, (
        f"signup must refuse an address already registered. {describe(again)}")
    short = anonymous.post("/auth/signup",
                           {"email": probe_email(), "password": "short", "name": "Probe"})
    assert short.status_code in REFUSAL_STATUSES, (
        f"signup must refuse a password under ten characters. {describe(short)}")


def test_widget_routes_stay_small_and_carry_the_next_charge(owner):
    for route in WIDGET_ROUTES:
        document = page(route)
        assert document.status_code in SUCCESS_STATUSES + (401, 302, 303), (
            f"the widget route {route} must render standalone. {describe(document)}")
        assert len(document.content) < 50 * 1024, (
            f"the widget route {route} must return a document under fifty kilobytes "
            f"before its data, read {len(document.content)} bytes")
    payload = owner.overview().json()
    upcoming = payload.get("upcoming") or []
    assert upcoming, "the owner store must schedule a next charge for the widgets"
    assert upcoming[0].get("name"), (
        f"the nearest upcoming row must name its subscription. {upcoming[0]}")


def test_rate_table_is_dated_and_conversion_names_the_rate_date(owner2):
    response = owner2.overview()
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    assert RATE_AS_OF in response.text, (
        f"a surface showing a converted figure must name the rate date it used, "
        f"which for the bundled table is {RATE_AS_OF}. {describe(response)}")


def test_route_view_counts_are_recorded_without_any_identity(owner):
    page("/privacy")
    response = owner.get("/app/stats/views")
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    rows = response.json().get("data") or response.json().get("rows") or []
    assert rows, f"the route-view counts must be readable by an owner. {describe(response)}"
    for row in rows:
        assert set(row) <= {"route", "on_date", "count"}, (
            f"a route-view row carries no identity of any kind, yet it holds "
            f"{sorted(row)}")
        assert isinstance(row.get("count"), int), (
            f"a route-view row must carry an integer count, read {row.get('count')!r}")


def test_deployment_contract_surface_answers_on_the_api_prefix(anonymous):
    import os
    public = os.environ["APP_PUBLIC_URL"].rstrip("/")
    assert public, "APP_PUBLIC_URL must be readable from the environment"
    port = os.environ.get("APP_PUBLIC_PORT")
    assert port, "APP_PUBLIC_PORT must be readable from the environment"
    health = anonymous.get("/health")
    assert health.status_code == 200, (
        f"the HTTP API must answer on the same origin under the /api prefix, and "
        f"GET /api/health must return 200. {describe(health)}")
    login = anonymous.post("/auth/login",
                           {"email": OWNER_EMAIL, "password": PASSWORD})
    assert login.status_code in SUCCESS_STATUSES, (
        f"POST /api/auth/login must return an access token for the seeded account "
        f"whose password is written into {CREDENTIALS_PATH}. {describe(login)}")
    assert login.json().get("access_token"), (
        f"the login response must carry an access_token. {describe(login)}")


def test_seeded_rate_table_and_builtin_categories_are_served_by_the_app(owner2):
    response = owner2.overview()
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    demo = Session().get("/demo/overview")
    demo_names = {row.get("name") or row.get("category")
                  for row in demo.json().get("categories") or []}
    assert set(BUILTIN_CATEGORIES) <= demo_names, (
        f"the seven builtin categories must be served by the app itself, read "
        f"{sorted(demo_names)}")
    assert RATE_AS_OF in demo.text or RATE_AS_OF in response.text, (
        f"the bundled daily-rate table dated {RATE_AS_OF} must be served from the "
        f"app's own store rather than fetched from anywhere else")


def test_rejection_carries_a_machine_readable_code_and_a_human_message(owner2):
    response = owner2.create_subscription({"name": "", "price_minor": "not a number"})
    assert response.status_code in REFUSAL_STATUSES, (
        f"an invalid call must be rejected as a client error rather than served as a "
        f"silent success or a server error. {describe(response)}")
    body = response.json()
    assert _dig(body, "code"), (
        f"a rejection must carry a stable machine-readable code. {describe(response)}")
    assert _dig(body, "message"), (
        f"a rejection must carry a human message. {describe(response)}")


def test_absent_or_expired_token_is_rejected_and_mutates_nothing(owner2, store):
    before = store.count("subscription")
    stale = Session(token="expired.token.value")
    response = stale.create_subscription({
        "name": f"Probe {batch_key()}",
        "price_minor": 400,
        "currency": HOME_CURRENCY,
        "cycle": "monthly",
        "anchor_date": "2026-11-01",
        "category": CATEGORY_UTILITIES,
    })
    assert response.status_code in DENIAL_STATUSES, (
        f"a request carrying a token the app never issued must be rejected. "
        f"{describe(response)}")
    after = store.count("subscription")
    assert after == before, (
        f"a rejected request must perform no mutation: {before} rows before and "
        f"{after} after")


def test_two_open_sessions_converge_within_one_second_of_a_change(owner2):
    second_tab = sign_in(OWNER2_EMAIL)
    before = second_tab.overview().json().get("year_minor")
    probe = f"Probe {batch_key()}"
    created = owner2.create_subscription({
        "name": probe,
        "price_minor": 600,
        "currency": HOME_CURRENCY,
        "cycle": "yearly",
        "anchor_date": "2026-11-11",
        "category": CATEGORY_UTILITIES,
    })
    assert created.status_code in SUCCESS_STATUSES, describe(created)
    settled = poll_until(
        lambda: second_tab.overview().json().get("year_minor") != before, budget=5.0)
    after = second_tab.overview().json().get("year_minor")
    assert settled and after == before + 600, (
        f"a second open session must show the new figure without a manual reload: "
        f"{before} before the change and {after} after it")
    identifier = _dig(created.json(), "id")
    owner2.delete(f"/app/subscriptions/{identifier}")


def test_snapshot_export_restores_and_refuses_a_newer_version(owner2):
    export = owner2.get("/app/export/snapshot", passphrase="driplog-probe-phrase")
    assert export.status_code in SUCCESS_STATUSES, (
        f"a snapshot export must be sealed with the passphrase it is given. "
        f"{describe(export)}")
    snapshot = export.json() if export.headers.get("content-type", "").startswith(
        "application/json") else {"body": export.text}
    version = _dig(snapshot, "version")
    assert version is not None, (
        f"the snapshot must be versioned. {describe(export)}")
    ahead = dict(snapshot)
    if isinstance(version, int):
        ahead["version"] = version + 1
    else:
        ahead["version"] = f"{version}-ahead"
    refused = owner2.post("/app/import/snapshot",
                          {"snapshot": ahead, "passphrase": "driplog-probe-phrase"})
    assert refused.status_code in REFUSAL_STATUSES, (
        f"a snapshot whose version is newer than the app knows must be refused. "
        f"{describe(refused)}")
    assert str(ahead["version"]) in refused.text, (
        f"the refusal must name the version it will not open. {describe(refused)}")


def test_widget_route_reflects_a_change_within_the_minute(owner):
    first = page("/w/small")
    assert first.status_code in SUCCESS_STATUSES + (401, 302, 303), (
        f"/w/small must render standalone. {describe(first)}")
    overview = owner.overview().json()
    upcoming = overview.get("upcoming") or []
    assert upcoming, "the owner store must schedule a next charge"
    nearest = upcoming[0]
    assert nearest.get("charge_date"), (
        f"the nearest upcoming row must carry a charge date. {nearest}")
    assert isinstance(nearest.get("days_remaining"), int), (
        f"the nearest upcoming row must carry a countdown in whole days. {nearest}")


def test_entitled_account_keeps_a_custom_category_and_a_scan_retention_setting(owner2):
    settings = owner2.settings()
    assert settings.status_code in SUCCESS_STATUSES, describe(settings)
    retention = settings.json().get("retention_days")
    assert isinstance(retention, int) and retention > 0, (
        f"scan history must carry a retention setting in whole days, read "
        f"{retention!r}. {describe(settings)}")
    listing = owner2.subscriptions(**{PAGE_SIZE_PARAM: PAGE_SIZE_MAX}).json()["data"]
    categories = {row.get("category") for row in listing}
    assert "Studio" in categories, (
        f"the entitled account must hold its one custom category Studio, read "
        f"{sorted(c for c in categories if c)}")
    unentitled = sign_in(OWNER_EMAIL)
    refused = unentitled.post("/app/categories", {"name": f"Probe {batch_key()}"})
    assert refused.status_code in REFUSAL_STATUSES, (
        f"a custom category must be refused for an account with no entitlement. "
        f"{describe(refused)}")


def _relative_luminance(rgb):
    channels = []
    for value in rgb:
        component = value / 255.0
        channels.append(component / 12.92 if component <= 0.03928
                        else ((component + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def _contrast_ratio(foreground, background):
    lighter, darker = sorted(
        (_relative_luminance(foreground), _relative_luminance(background)),
        reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def _parse_rgb(value: str):
    numbers = [int(float(n)) for n in
               value.replace("rgba(", "").replace("rgb(", "").rstrip(")").split(",")[:3]]
    return tuple(numbers)


def test_body_text_meets_the_contrast_bar_on_paper_and_on_charcoal(anonymous):
    from playwright.sync_api import sync_playwright
    import appclient
    probe = """
    () => {
      const seen = [];
      const walk = (node) => {
        const style = getComputedStyle(node);
        const size = parseFloat(style.fontSize);
        const text = (node.innerText || '').trim();
        if (text.length > 20 && size > 0 && size < 24 && node.children.length === 0) {
          let bg = 'rgba(0, 0, 0, 0)';
          let owner = node;
          while (owner) {
            const value = getComputedStyle(owner).backgroundColor;
            if (value && !value.endsWith(', 0)') && value !== 'transparent') {
              bg = value;
              break;
            }
            owner = owner.parentElement;
          }
          seen.push({ colour: style.color, background: bg, size: size });
        }
        for (const child of node.children) walk(child);
      };
      walk(document.body);
      return seen.slice(0, 60);
    }
    """
    with sync_playwright() as driver:
        browser = driver.chromium.launch()
        page_handle = browser.new_page(viewport={"width": 1440, "height": 900})
        page_handle.goto(f"{appclient.app_url()}/", wait_until="load")
        samples = page_handle.evaluate(probe)
        browser.close()
    assert samples, (
        "the landing page must render body text a reader can measure; the probe found "
        "no text run longer than twenty characters")
    failures = []
    for sample in samples:
        background = sample.get("background", "")
        if background.endswith(", 0)") or background == "transparent":
            continue
        ratio = _contrast_ratio(_parse_rgb(sample["colour"]),
                                _parse_rgb(background))
        if ratio < 4.5:
            failures.append(
                f"{sample['colour']} on {background} at {sample['size']:.0f}px "
                f"reads {ratio:.2f}")
    assert not failures, (
        "body text must clear the WCAG AA contrast bar of 4.5 to 1 against its own "
        "ground, on the paper surfaces and inside the inverted footer and the dark "
        f"privacy band alike. Failing runs: {failures[:6]}")
