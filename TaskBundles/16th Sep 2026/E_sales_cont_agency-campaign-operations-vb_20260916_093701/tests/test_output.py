from __future__ import annotations

import math
import threading

import conftest


def test_health_endpoint_reports_ready(anon):
    response = anon.get("/health")
    assert response.status_code == 200, (
        "GET /api/health must answer 200 once the app is ready: " + conftest.describe(response))


def test_public_work_index_counts_only_published_campaigns(anon):
    first = conftest.public_index(anon, page=1)
    slugs = conftest.all_public_slugs(anon)
    total = int(first.get("total") or -1)
    assert total == len(slugs), (
        f"the work index total {total} must equal the campaigns listed across its pages "
        f"({len(slugs)})")
    assert total >= conftest.SEEDED_PUBLIC_COUNT, (
        f"the thirty seeded public campaigns must be counted; the total is {total}")
    assert conftest.NIGHT_SIGNAL in slugs, f"{conftest.NIGHT_SIGNAL} is public and must be listed"
    for hidden in (conftest.SILENT_AURORA, conftest.WINTER_KITE):
        assert hidden not in slugs, f"{hidden} is not public and must not be listed: {slugs}"
    english = conftest.all_public_slugs(anon, locale="en")
    assert sorted(english) == sorted(slugs), (
        "the English work index must list the same campaigns as the Japanese one, "
        "including a campaign published in Japanese only")
    assert conftest.RICE_FIELD_RADIO in english, "Rice Field Radio must be listed in English"


def test_work_index_pages_twelve_campaigns_at_a_time(anon):
    first = conftest.public_index(anon, page=1)
    total = int(first.get("total") or 0)
    listed = conftest.rows(first)
    assert len(listed) == conftest.PAGE_SIZE, (
        f"the first work index page must hold twelve campaigns, it held {len(listed)}")
    expected_pages = math.ceil(total / conftest.PAGE_SIZE)
    assert int(first.get("page_count") or 0) == expected_pages, (
        f"page_count must be {expected_pages} for {total} campaigns at twelve per page: {first}")


def test_work_index_page_past_the_end_falls_back_to_the_last_page(anon):
    first = conftest.public_index(anon, page=1)
    last = int(first.get("page_count") or 0)
    beyond = conftest.public_index(anon, page=999)
    assert int(beyond.get("page") or 0) == last, (
        f"page 999 must fall back to the last page {last}, got {beyond.get('page')}")
    assert conftest.rows(beyond), "the fallback page must not be empty"


def test_work_index_year_facet_carries_a_before_bucket(anon):
    first = conftest.public_index(anon, page=1)
    buckets = [str(b) for b in (first.get("year_buckets") or [])]
    assert buckets and buckets[0] == "all", f"the year facet must open with all: {buckets}"
    assert buckets[-1] == conftest.BEFORE_BUCKET, f"the year facet must end with before: {buckets}"
    assert buckets[1:-1] == list(conftest.LISTED_YEARS), (
        f"the listed years must be the five most recent holding work, newest first: {buckets}")
    older = conftest.public_index(anon, year=conftest.BEFORE_BUCKET, page=1)
    years = [int(r.get("year")) for r in conftest.rows(older)]
    assert years and all(y < conftest.FIRST_UNLISTED_YEAR for y in years), (
        f"the before bucket must hold only work older than 2022, got {years}")
    assert conftest.OLDEST_SEEDED in conftest.all_public_slugs(anon, year=conftest.BEFORE_BUCKET)
    one_year = conftest.public_index(anon, year=2025, page=1)
    assert all(int(r.get("year")) == 2025 for r in conftest.rows(one_year)), (
        "filtering the work index to 2025 must list only 2025 campaigns")


def test_campaign_detail_lists_every_client_with_one_primary(anon):
    detail = conftest.ok(anon.get(f"/public/campaigns/{conftest.NIGHT_SIGNAL}",
                                  params={"locale": "en"}), "reading Night Signal")
    clients = detail.get("clients") or []
    names = [str(c.get("name")) for c in clients]
    for expected in conftest.NIGHT_SIGNAL_CLIENTS:
        assert expected in names, f"Night Signal must list client {expected}: {names}"
    primaries = [str(c.get("name")) for c in clients if c.get("primary")]
    assert primaries == [conftest.NIGHT_SIGNAL_PRIMARY], (
        f"exactly one client, Kagerou Beverages, must be primary: {clients}")


def test_campaign_credits_keep_the_editorial_order(anon):
    detail = conftest.ok(anon.get(f"/public/campaigns/{conftest.NIGHT_SIGNAL}",
                                  params={"locale": "en"}), "reading Night Signal")
    credits = sorted(detail.get("credits") or [], key=lambda c: int(c.get("position") or 0))
    roles = [str(c.get("role")) for c in credits]
    assert roles == list(conftest.NIGHT_SIGNAL_ROLES), (
        f"Night Signal credit roles must keep the editorial order: {roles}")
    joint = [c for c in credits if c.get("role") == "Producer"]
    names = [str(p.get("name")) for p in (joint[0].get("people") if joint else [])]
    assert names == list(conftest.JOINT_PRODUCERS), (
        f"one Producer entry must credit Yuto Baba, Riko Nishi and Sho Ota together: {names}")
    assert conftest.DEPARTED_PERSON.lower() in conftest.flat(credits), (
        "the departed Shun Kaneda must still be credited on Night Signal")
    langs = {str(p.get("lang")) for c in credits for p in (c.get("people") or [])}
    assert langs and langs <= {"ja", "en"}, (
        f"every credited name must carry the locale it is shown in: {langs}")


def test_campaign_awards_hold_several_results_from_one_body_and_year(anon):
    detail = conftest.ok(anon.get(f"/public/campaigns/{conftest.NIGHT_SIGNAL}",
                                  params={"locale": "en"}), "reading Night Signal")
    groups = [g for g in (detail.get("awards") or [])
              if str(g.get("body")) == conftest.LOTUS_NAME and str(g.get("year")) == "2025"]
    assert len(groups) == 1, f"Night Signal must group its Lotus Festival 2025 results once: {detail.get('awards')}"
    results = groups[0].get("results") or []
    ranks = sorted(str(r.get("rank")) for r in results)
    assert ranks == sorted(conftest.NIGHT_SIGNAL_LOTUS_RANKS), (
        f"Night Signal holds Grand Lotus, Gold and Silver from one body and year, and the "
        f"unconfirmed shortlist must not appear: {ranks}")
    categories = {str(r.get("category")) for r in results}
    assert len(categories) == len(results), f"each result sits in its own category: {results}"


def test_english_campaign_falls_back_per_field_with_language_marker(anon):
    english = conftest.ok(anon.get(f"/public/campaigns/{conftest.QUIET_ENGINE}",
                                   params={"locale": "en"}), "reading Quiet Engine in English")
    japanese = conftest.ok(anon.get(f"/public/campaigns/{conftest.QUIET_ENGINE}",
                                    params={"locale": "ja"}), "reading Quiet Engine in Japanese")
    lang = english.get("lang") or {}
    assert english.get("title") == conftest.QUIET_ENGINE_TITLE and lang.get("title") == "en", (
        f"the English title must be shown and marked en: {english.get('title')} {lang}")
    assert lang.get("description") == "ja", (
        f"the absent English description must fall back to Japanese, marked ja: {lang}")
    assert english.get("description") == japanese.get("description"), (
        "the fallback description must be the Japanese original, field by field")


def test_campaign_absent_in_both_locales_is_not_found(anon):
    for locale in ("ja", "en"):
        response = anon.get(f"/public/campaigns/{conftest.WINTER_KITE}", params={"locale": locale})
        assert response.status_code == 404, (
            f"Winter Kite has no published translation and must be not-found in {locale}: "
            + conftest.describe(response))
    assert conftest.WINTER_KITE not in conftest.all_public_slugs(anon, locale="en")


def test_client_register_sorts_japanese_names_by_reading(producer):
    japanese = conftest.rows(conftest.ok(producer.get("/clients", params={"locale": "ja"}),
                                         "reading the client register in Japanese"))
    english = conftest.rows(conftest.ok(producer.get("/clients", params={"locale": "en"}),
                                        "reading the client register in English"))
    assert [str(c.get("slug")) for c in japanese] == list(conftest.CLIENTS_BY_READING), (
        f"Japanese collation must follow the readings: {[c.get('slug') for c in japanese]}")
    assert [str(c.get("slug")) for c in english] == list(conftest.CLIENTS_BY_ENGLISH), (
        f"English collation must be alphabetical: {[c.get('slug') for c in english]}")


def test_public_search_finds_a_japanese_title_fragment(anon):
    for query in (conftest.NIGHT_SIGNAL_FRAGMENT, conftest.NIGHT_SIGNAL_READING_FRAGMENT,
                  conftest.NIGHT_SIGNAL_TITLE):
        found = conftest.rows(conftest.ok(anon.get("/public/search", params={"q": query}),
                                          f"searching for {query}"))
        slugs = [str(r.get("slug")) for r in found]
        assert conftest.NIGHT_SIGNAL in slugs, (
            f"searching {query!r} must find Night Signal, got {slugs}")


def test_news_category_facet_matches_articles_carrying_several_categories(anon):
    for category in ("awards", "news"):
        listing = conftest.ok(anon.get("/public/news", params={"category": category}),
                              f"filtering news by {category}")
        slugs = [str(r.get("slug")) for page in [listing] for r in conftest.rows(page)]
        pages = int(listing.get("page_count") or 1)
        for number in range(2, pages + 1):
            more = conftest.ok(anon.get("/public/news", params={"category": category,
                                                                "page": number}), "paging news")
            slugs += [str(r.get("slug")) for r in conftest.rows(more)]
        assert conftest.AWARD_ARTICLE in slugs, (
            f"the article tagged awards and news must match the {category} facet: {slugs}")
    both = conftest.ok(anon.get("/public/news", params={"category": "awards", "year": 2025}),
                       "composing the category and year facets")
    assert conftest.AWARD_ARTICLE in [str(r.get("slug")) for r in conftest.rows(both)]
    empty = conftest.ok(anon.get("/public/news", params={"category": "stories", "year": 2019}),
                        "reading an empty facet intersection")
    assert int(empty.get("total") or 0) == 0 and conftest.rows(empty) == [], (
        f"stories in 2019 is an empty intersection and must list nothing: {empty}")


def test_news_award_breakdown_reads_the_same_results_as_the_campaign(anon):
    article = conftest.ok(anon.get(f"/public/news/{conftest.AWARD_ARTICLE}",
                                   params={"locale": "en"}), "reading the award article")
    breakdown = {(str(r.get("category")), str(r.get("rank")))
                 for r in (article.get("breakdown") or [])
                 if str(r.get("campaign")) in (conftest.NIGHT_SIGNAL, conftest.NIGHT_SIGNAL_TITLE)}
    detail = conftest.ok(anon.get(f"/public/campaigns/{conftest.NIGHT_SIGNAL}",
                                  params={"locale": "en"}), "reading Night Signal")
    campaign = {(str(r.get("category")), str(r.get("rank")))
                for g in (detail.get("awards") or [])
                if str(g.get("body")) == conftest.LOTUS_NAME and str(g.get("year")) == "2025"
                for r in (g.get("results") or [])}
    assert breakdown and breakdown == campaign, (
        f"the article breakdown {breakdown} and the campaign awards {campaign} must be one record")


def test_headline_top_rank_count_includes_the_supreme_award(anon):
    body = conftest.tally(anon, conftest.LOTUS, conftest.LOTUS_YEAR)
    assert int(body.get("total") or 0) == conftest.LOTUS_TOTAL, (
        f"Lotus Festival 2025 must total nine confirmed results: {body}")
    assert conftest.rank_counts(body.get("itemised")) == dict(conftest.LOTUS_ITEMISED), (
        f"the itemised results must read {dict(conftest.LOTUS_ITEMISED)}: {body.get('itemised')}")
    assert conftest.rank_counts(body.get("headline")) == dict(conftest.LOTUS_HEADLINE), (
        f"the headline must roll Grand Lotus into Gold, reading {dict(conftest.LOTUS_HEADLINE)}: "
        f"{body.get('headline')}")


def test_body_specific_rank_is_kept_as_its_own_rank(producer):
    bodies = conftest.rows(conftest.ok(producer.get("/award-bodies"), "reading award bodies"))
    lotus = conftest.find_by(bodies, "slug", conftest.LOTUS)
    north = conftest.find_by(bodies, "slug", conftest.NORTH_STAR)
    assert lotus and north, f"both seeded award bodies must be listed: {bodies}"
    lotus_ranks = {str(r.get("name")): r for r in (lotus.get("ranks") or [])}
    north_ranks = {str(r.get("name")) for r in (north.get("ranks") or [])}
    assert conftest.BODY_SPECIFIC_RANK in lotus_ranks, f"Jade Petal must be a Lotus rank: {lotus_ranks}"
    assert conftest.BODY_SPECIFIC_RANK not in north_ranks, "Jade Petal exists at no other body"
    assert str(lotus_ranks[conftest.SUPREME_RANK].get("counts_toward")) == conftest.TOP_RANK, (
        f"Grand Lotus must count toward Gold: {lotus_ranks[conftest.SUPREME_RANK]}")


def test_company_record_shows_concurrent_positions_apart_from_titles(anon):
    company = conftest.ok(anon.get("/public/company", params={"locale": "en"}),
                          "reading the company record")
    officer = conftest.find_by(company.get("officers") or [], "name",
                               conftest.OFFICER_WITH_CONCURRENT)
    assert officer is not None, f"Hiroshi Kudo must be listed: {company.get('officers')}"
    assert officer.get("title") == conftest.OFFICER_TITLE, (
        f"the title must be the position here only: {officer}")
    assert conftest.PARENT_GROUP in str(officer.get("concurrent_position")), (
        f"the Meido Group position must sit in concurrent_position: {officer}")
    assert company.get("updated") == conftest.COMPANY_UPDATED, f"last-updated date: {company}"
    assert company.get("telephone") == conftest.COMPANY_TELEPHONE, f"telephone: {company}"
    first = (company.get("officers") or [{}])[0]
    assert first.get("name") == conftest.FIRST_OFFICER and \
        first.get("title") == conftest.FIRST_OFFICER_TITLE, f"officers keep their order: {first}"
    assert "2006" in str(company.get("founded")), f"the founding year is 2006: {company}"
    address = str(company.get("address"))
    assert conftest.COMPANY_POSTAL_CODE in address and conftest.COMPANY_BUILDING in address, (
        f"the address must carry the postal code and the building: {address}")
    names = [str(o.get("name")) for o in company.get("officers") or []]
    listed = [n for n in names if n in conftest.OFFICER_ORDER]
    assert listed == list(conftest.OFFICER_ORDER), f"the officers keep their order: {names}"
    auditor = conftest.find_by(company.get("officers") or [], "name", conftest.AUDITOR)
    assert auditor and auditor.get("title") == conftest.AUDITOR_TITLE and \
        auditor.get("concurrent_position") == conftest.AUDITOR_CONCURRENT, (
            f"the auditor must be listed with the concurrent position: {auditor}")
    for name, title in conftest.OFFICER_TITLES:
        held = conftest.find_by(company.get("officers") or [], "name", name)
        assert held and held.get("title") == title, f"{name} must be listed as {title}: {held}"
    assert officer.get("concurrent_position") == conftest.KUDO_CONCURRENT, (
        f"Hiroshi Kudo's concurrent position must read exactly: {officer}")
    listed_units = sorted(str(u.get("name")) for u in company.get("units") or [])
    assert listed_units == sorted(conftest.UNIT_NAMES), f"the ten units must be named: {listed_units}"
    chen = conftest.find_by(company.get("officers") or [], "name", conftest.GLOBAL_OFFICER)
    assert chen and chen.get("concurrent_position") == conftest.GLOBAL_OFFICER_CONCURRENT, (
        f"Laura Chen's concurrent position must be listed apart from the title: {chen}")
    units = company.get("units") or []
    dedicated = [u for u in units if u.get("dedicated_client")]
    studio = conftest.find_by(units, "name", conftest.KAGEROU_STUDIO)
    assert studio and "kagerou" in str(studio.get("dedicated_client")).lower(), (
        f"Kagerou Studio must be dedicated to Kagerou Beverages: {studio}")
    assert len(units) == conftest.UNIT_COUNT and len(dedicated) == conftest.DEDICATED_UNIT_COUNT, (
        f"ten units, two dedicated to one client, must be listed: {units}")


def test_careers_openings_carry_a_track_and_an_external_apply_address(anon):
    careers = conftest.ok(anon.get("/public/careers", params={"locale": "en"}),
                          "reading the careers record")
    openings = careers.get("openings") or []
    assert {str(o.get("track")) for o in openings} == set(conftest.OPENING_TRACKS), (
        f"openings must carry the new_graduate and internship tracks: {openings}")
    for opening in openings:
        assert str(opening.get("apply_url")).startswith(conftest.APPLY_PREFIX), (
            f"each opening must carry its external apply address: {opening}")
        assert opening.get("title"), f"each opening must carry a title: {opening}"
    internship = conftest.find_by(openings, "track", "internship")
    assert internship and internship.get("apply_url") == conftest.INTERNSHIP_URL, (
        f"the internship opening must link to its pinned address: {internship}")
    graduate = conftest.find_by(openings, "track", "new_graduate")
    assert graduate and graduate.get("apply_url") == conftest.NEW_GRADUATE_URL, (
        f"the new-graduate opening must link to its pinned address: {graduate}")
    assert sorted(str(o.get("title")) for o in openings) == sorted(conftest.OPENING_TITLES), (
        f"the two seeded openings must carry their titles: {openings}")
    english = conftest.flat(careers.get("values"))
    japanese = conftest.ok(anon.get("/public/careers", params={"locale": "ja"}),
                           "reading the Japanese careers record").get("values")
    for phrase, rendering in conftest.CAREERS_VALUES:
        assert phrase.lower() in english, f"the value {phrase} must be listed: {careers.get('values')}"
        assert rendering in str(japanese), (
            f"the value {phrase} must carry the Japanese rendering {rendering}: {japanese}")


def test_brief_becomes_a_job_with_estimate_producer_and_pinned_card(account_director, producer):
    job = conftest.make_job(account_director, producer)
    assert job.get("rate_card_version"), f"the converted job must pin a rate card: {job}"
    shares = sum(int(a.get("share_bp")) for a in (job.get("apportionment") or []))
    assert shares == conftest.APPORTIONMENT_WHOLE, f"the apportionment must sum to 10000: {job}"
    listed = conftest.job_titled(account_director, job.get("title"))
    assert listed is not None, "the converted job must appear in the account director's job list"


def test_brief_conversion_without_an_approved_estimate_is_refused(account_director, producer):
    brief = conftest.open_brief(account_director)
    conftest.ok(producer.post(f"/briefs/{conftest.ident(brief)}/estimates",
                              json={"amount_minor": 4000000}), "writing an estimate")
    response = conftest.convert(account_director, brief, conftest.person_id_of(producer),
                                ((conftest.KAGEROU, conftest.APPORTIONMENT_WHOLE),))
    conftest.refused(response, "converting a brief whose estimate is unapproved")
    assert conftest.job_titled(account_director, brief.get("title")) is None, (
        "a refused conversion must create no job")


def test_brief_conversion_without_a_producer_is_refused(account_director, producer):
    brief = conftest.open_brief(account_director)
    conftest.approved_estimate(account_director, producer, brief)
    response = conftest.convert(account_director, brief, None,
                                ((conftest.KAGEROU, conftest.APPORTIONMENT_WHOLE),))
    conftest.refused(response, "converting a brief with no named producer")
    assert conftest.job_titled(account_director, brief.get("title")) is None, (
        "a refused conversion must create no job")


def test_publication_gate_passes_with_all_four_conditions(account_director, producer, legal,
                                                          editor, anon):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    published = conftest.ok(conftest.publish(editor, made["campaign_id"]),
                            "publishing a campaign that meets every condition")
    assert published.get("state") == "published", f"the campaign must be published: {published}"
    for locale in ("ja", "en"):
        detail = anon.get(f"/public/campaigns/{made['slug']}", params={"locale": locale})
        assert detail.status_code == 200, (
            f"the published campaign must be public in {locale}: " + conftest.describe(detail))
    assert made["slug"] in conftest.all_public_slugs(anon), "the published campaign must be indexed"


def test_publish_without_case_study_permission_is_refused(account_director, producer, legal,
                                                          editor, anon):
    made = conftest.make_campaign(account_director, producer, legal, editor, permission=False)
    response = conftest.publish(editor, made["campaign_id"])
    conftest.refused(response, "publishing without case-study permission")
    assert conftest.REASON_PERMISSION in conftest.reasons_of(response), (
        "the refusal must name case_study_permission: " + conftest.describe(response))
    assert anon.get(f"/public/campaigns/{made['slug']}").status_code == 404, (
        "a refused publish must leave the campaign unreachable")


def test_publish_with_an_empty_credit_list_is_refused(account_director, producer, legal, editor):
    made = conftest.make_campaign(account_director, producer, legal, editor, credits=False)
    response = conftest.publish(editor, made["campaign_id"])
    conftest.refused(response, "publishing with an empty credit list")
    assert conftest.REASON_CREDITS in conftest.reasons_of(response), (
        "the refusal must name credits: " + conftest.describe(response))


def test_publish_before_clearance_is_complete_is_refused(account_director, producer, legal,
                                                         editor):
    made = conftest.make_campaign(account_director, producer, legal, editor,
                                  right_status="pending")
    response = conftest.publish(editor, made["campaign_id"])
    conftest.refused(response, "publishing before clearance is complete")
    assert conftest.REASON_CLEARANCE in conftest.reasons_of(response), (
        "the refusal must name clearance: " + conftest.describe(response))
    state = conftest.campaign_by_slug(editor, made["slug"]).get("state")
    assert state == "draft", f"a refused publish must change nothing, state is {state}"


def test_scheduling_past_a_rights_expiry_is_refused(account_director, producer, legal, editor):
    made = conftest.make_campaign(account_director, producer, legal, editor,
                                  term_end="2031-01-01")
    response = conftest.publish(editor, made["campaign_id"],
                                embargo_at="2032-01-01T00:00:00+09:00")
    conftest.refused(response, "scheduling a release after a right has ended")
    assert conftest.REASON_RIGHTS in conftest.reasons_of(response), (
        "the refusal must name rights_expire_before_release: " + conftest.describe(response))
    assert conftest.SCHEDULE_REFUSAL in response.text, (
        "the refusal must carry the scheduling notice: " + conftest.describe(response))


def test_scheduled_embargo_releases_without_anyone_acting(anon):
    released = conftest.poll_until(
        lambda: anon.get(f"/public/campaigns/{conftest.HARBOUR_LIGHTS}").status_code == 200,
        conftest.RELEASE_DEADLINE_SECONDS)
    assert released, "Harbour Lights must become public at its release moment with nobody acting"
    assert conftest.HARBOUR_LIGHTS in conftest.all_public_slugs(anon), (
        "the released campaign must reach the work index everywhere at once")


def test_expired_right_hides_the_campaign_in_the_affected_market_only(anon):
    germany = anon.get(f"/public/campaigns/{conftest.TIDE_CLOCK}", params={"market": "DE"})
    assert germany.status_code == 404, (
        "Tide Clock's DE talent right has ended, so DE must not see it: " + conftest.describe(germany))
    assert conftest.TIDE_CLOCK not in conftest.all_public_slugs(anon, market="DE")
    japan = anon.get(f"/public/campaigns/{conftest.TIDE_CLOCK}", params={"market": "JP"})
    assert japan.status_code == 200, (
        "Tide Clock's JP right still runs, so JP must see it: " + conftest.describe(japan))


def test_festival_exhibition_is_recorded_as_a_distinct_right(account_director, producer, legal):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    conftest.ok(conftest.add_right(legal, job_id, right="music"), "recording a music right")
    conftest.ok(conftest.add_right(legal, job_id, markets=("DE",), right="festival_exhibition"),
                "recording a festival exhibition right")
    rights = conftest.rows(conftest.ok(legal.get(f"/jobs/{job_id}/rights"), "listing rights"))
    kinds = sorted(str(r.get("right")) for r in rights)
    assert kinds == ["festival_exhibition", "music"], (
        f"festival exhibition must be its own right beside the media right: {kinds}")


def test_preview_link_serves_until_revoked_and_forbids_indexing(editor, anon):
    campaign = conftest.campaign_by_slug(editor, conftest.SILENT_AURORA)
    link = conftest.ok(editor.post(f"/campaigns/{conftest.ident(campaign)}/preview-links",
                                   json={"expires_in_minutes": 30}), "creating a preview link")
    token = link.get("token")
    shown = anon.get(f"/preview/{token}")
    assert shown.status_code == 200, "a live preview link must serve: " + conftest.describe(shown)
    assert "noindex" in shown.headers.get("x-robots-tag", "").lower(), (
        f"a preview response must forbid indexing, headers: {dict(shown.headers)}")
    conftest.ok(editor.post(f"/preview-links/{token}/revoke"), "revoking the preview link")
    gone = anon.get(f"/preview/{token}")
    assert gone.status_code == 404, "a revoked preview link must answer not-found: " + conftest.describe(gone)


def test_credit_list_keeps_repeated_roles_and_joint_entries(account_director, producer, legal,
                                                            editor):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    second = conftest.make_person(producer)
    conftest.grant(account_director, second, conftest.KAGEROU)
    conftest.ok(conftest.staff(producer, made["job_id"], second, role="Producer"), "staffing")
    first = made["person"]
    current = conftest.read_credits(editor, made["campaign_id"])
    entries = [conftest.credit_entry("Experience Planner", [first]),
               conftest.credit_entry("Producer", [first, second]),
               conftest.credit_entry("Experience Planner", [second])]
    conftest.ok(conftest.save_credits(editor, made["campaign_id"], current.get("revision"),
                                      entries), "saving a credit list with a repeated role")
    stored = sorted(conftest.read_credits(editor, made["campaign_id"]).get("entries") or [],
                    key=lambda e: int(e.get("position") or 0))
    assert [e.get("role_en") for e in stored] == ["Experience Planner", "Producer",
                                                  "Experience Planner"], (
        f"the credit list must keep the editor's order with the repeated role: {stored}")
    assert len(stored[1].get("people") or []) == 2, f"the Producer entry must name two people: {stored}"


def test_credit_for_a_person_with_no_assignment_is_refused(account_director, producer, legal,
                                                           editor):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    stranger = conftest.make_person(producer)
    conftest.grant(account_director, stranger, conftest.KAGEROU)
    before = conftest.read_credits(editor, made["campaign_id"])
    response = conftest.save_credits(editor, made["campaign_id"], before.get("revision"),
                                     [conftest.credit_entry("Copywriter", [stranger])])
    conftest.refused(response, "crediting a person with no assignment on the job")
    after = conftest.read_credits(editor, made["campaign_id"])
    assert after == before, f"a refused credit save must leave the list unchanged: {after}"


def test_credit_for_a_person_without_current_clearance_is_refused(account_director, producer,
                                                                  legal, editor):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    person = made["person"]
    detail = conftest.ok(producer.get(f"/people/{conftest.ident(person)}"), "reading the person")
    clearance = conftest.find_by(detail.get("clearances") or [], "account", conftest.KAGEROU)
    assert clearance is not None, f"the probe person must hold the kagerou clearance: {detail}"
    conftest.ok(account_director.post(f"/clearances/{conftest.ident(clearance)}/revoke",
                                      json={"revoked_on": "2026-06-01"}), "revoking a clearance")
    before = conftest.read_credits(editor, made["campaign_id"])
    response = conftest.save_credits(editor, made["campaign_id"], before.get("revision"),
                                     [conftest.credit_entry("Art Director", [person])])
    conftest.refused(response, "crediting a person whose clearance was revoked")


def test_name_change_propagates_except_to_pinned_credits(account_director, producer, legal,
                                                         editor):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    person = made["person"]
    old_name = person.get("name_en")
    current = conftest.read_credits(editor, made["campaign_id"])
    conftest.ok(conftest.save_credits(editor, made["campaign_id"], current.get("revision"), [
        conftest.credit_entry("Creative Director", [person], pin=True),
        conftest.credit_entry("Copywriter", [person], pin=False)]), "saving pinned credits")
    new_name = f"Renamed {conftest.unique_token()}"
    conftest.ok(producer.patch(f"/people/{conftest.ident(person)}", json={"name_en": new_name}),
                "renaming the person")
    stored = sorted(conftest.read_credits(editor, made["campaign_id"]).get("entries") or [],
                    key=lambda e: int(e.get("position") or 0))
    pinned = [p.get("name_en") for p in stored[0].get("people") or []]
    unpinned = [p.get("name_en") for p in stored[1].get("people") or []]
    assert pinned == [old_name], f"the pinned entry must keep the name the work was made under: {pinned}"
    assert unpinned == [new_name], f"the unpinned entry must show the new name: {unpinned}"


def test_two_credit_edits_from_one_revision_admit_exactly_one(account_director, producer,
                                                              legal, editor):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    revision = conftest.read_credits(editor, made["campaign_id"]).get("revision")
    person = made["person"]
    barrier = threading.Barrier(2)
    statuses = []

    def attempt(role):
        with conftest.client_for(conftest.EDITOR_EMAIL) as client:
            barrier.wait()
            statuses.append(conftest.save_credits(
                client, made["campaign_id"], revision,
                [conftest.credit_entry(role, [person])]).status_code)

    threads = [threading.Thread(target=attempt, args=(role,))
               for role in ("Creative Director", "Art Director")]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    winners = [s for s in statuses if s in (200, 201)]
    losers = [s for s in statuses if 400 <= s < 500]
    assert len(winners) == 1 and len(losers) == 1, (
        f"two concurrent saves from one revision must admit exactly one: {statuses}")


def test_stale_credit_revision_is_refused_and_changes_nothing(account_director, producer,
                                                              legal, editor):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    person = made["person"]
    stale = conftest.read_credits(editor, made["campaign_id"]).get("revision")
    conftest.ok(conftest.save_credits(editor, made["campaign_id"], stale,
                                      [conftest.credit_entry("Art Director", [person])]),
                "saving from the current revision")
    kept = conftest.read_credits(editor, made["campaign_id"])
    response = conftest.save_credits(editor, made["campaign_id"], stale,
                                     [conftest.credit_entry("Copywriter", [person])])
    conftest.refused(response, "saving a credit list from a stale revision")
    assert conftest.read_credits(editor, made["campaign_id"]) == kept, (
        "a conflicting save must leave the credit list unchanged")


def test_departed_person_keeps_published_credits(account_director, producer, legal, editor,
                                                 anon):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    conftest.ok(conftest.publish(editor, made["campaign_id"]), "publishing the campaign")
    person = made["person"]
    name = person.get("name_en")
    departed = conftest.ok(producer.post(f"/people/{conftest.ident(person)}/depart",
                                         json={"departed_on": "2031-01-20"}),
                           "recording a departure")
    assert departed.get("status") == "departed", f"the person must be departed: {departed}"
    detail = conftest.ok(producer.get(f"/people/{conftest.ident(person)}"), "reading the person")
    assert int(detail.get("capacity_minutes") or 0) == 0, f"capacity must drop to zero: {detail}"
    assert all(c.get("revoked_on") for c in detail.get("clearances") or []), (
        f"every clearance must be revoked on departure: {detail.get('clearances')}")
    assert all(str(a.get("ends_on")) <= "2031-01-20" for a in detail.get("assignments") or []), (
        f"every assignment must end by the departure date: {detail.get('assignments')}")
    current = conftest.read_credits(editor, made["campaign_id"])
    resaved = conftest.save_credits(editor, made["campaign_id"], current.get("revision"), [
        {"role_en": e.get("role_en"), "role_ja": e.get("role_ja"), "pin_names": e.get("pin_names"),
         "people": [p.get("person_id") for p in e.get("people") or []]}
        for e in current.get("entries") or []])
    assert resaved.status_code in (200, 201), (
        "re-saving a list that already names a departed person must succeed: "
        + conftest.describe(resaved))
    public = conftest.ok(anon.get(f"/public/campaigns/{made['slug']}", params={"locale": "en"}),
                         "reading the published campaign")
    assert name.lower() in conftest.flat(public.get("credits")), (
        f"the departed person {name} must stay credited: {public.get('credits')}")


def test_seed_is_idempotent_across_a_restart(backend):
    for table, column, value in (("users", "email", conftest.PRODUCER_EMAIL),
                                 ("clients", "slug", conftest.HOSHINO),
                                 ("campaigns", "slug", conftest.NIGHT_SIGNAL)):
        count = backend.count(table, **{column: value})
        assert count == 1, f"{table} must hold exactly one {value}, found {count}"
    assert backend.count("users", email=conftest.CREATIVE2_EMAIL, role="creative") == 1, (
        "the seeded creative2 account must hold the creative role")


def test_enquiry_resubmitted_with_the_same_key_is_stored_once(anon, backend):
    key = conftest.enquiry_key(anon)
    body = conftest.enquiry_body(key)
    first = anon.post("/enquiries", json=body)
    second = anon.post("/enquiries", json=body)
    assert first.status_code in (200, 201), "the first submission must be accepted: " + conftest.describe(first)
    assert second.status_code < 500, "a repeated submission must not fail on the server"
    assert backend.count("enquiries", idempotency_key=key) == 1, (
        "one idempotency key must store exactly one enquiry")


def test_time_entry_cost_uses_the_pinned_card_rate(account_director, producer):
    job = conftest.make_job(account_director, producer)
    version = job.get("rate_card_version")
    card = conftest.ok(producer.get(f"/rate-cards/{version}"), "reading the pinned card")
    rate = int((card.get("rates") or {}).get(conftest.ART_DIRECTOR))
    entry = conftest.ok(producer.post(f"/jobs/{conftest.ident(job)}/time-entries", json={
        "person_id": conftest.person_id_of(producer), "role": conftest.ART_DIRECTOR,
        "work_date": "2031-03-03", "minutes": conftest.EXAMPLE_MINUTES}), "recording time")
    assert int(entry.get("cost_minor")) == rate * conftest.EXAMPLE_MINUTES // 60, (
        f"450 minutes at {rate} an hour must cost {rate * 450 // 60}: {entry}")
    seeded = conftest.ok(producer.get(f"/rate-cards/{conftest.CURRENT_CARD}"), "reading RC-2026")
    assert int(seeded["rates"][conftest.ART_DIRECTOR]) == conftest.EXAMPLE_ART_DIRECTOR_RATE
    assert int(seeded["rates"][conftest.SENIOR_CREATIVE_DIRECTOR]) != int(
        seeded["rates"][conftest.CREATIVE_DIRECTOR]), "senior and plain creative directors are different roles"
    cost = conftest.ok(producer.get(f"/jobs/{conftest.ident(job)}/cost"), "reading job cost")
    assert cost.get("currency") == conftest.LEDGER_CURRENCY, f"the ledger currency is jpy: {cost}"


def test_new_rate_card_leaves_an_approved_job_cost_unchanged(account_director, producer):
    job = conftest.make_job(account_director, producer)
    job_id = conftest.ident(job)
    conftest.ok(producer.post(f"/jobs/{job_id}/time-entries", json={
        "person_id": conftest.person_id_of(producer), "role": conftest.ART_DIRECTOR,
        "work_date": "2031-03-04", "minutes": 120}), "recording time")
    before = conftest.ok(producer.get(f"/jobs/{job_id}/cost"), "reading job cost")
    pinned = conftest.ok(producer.get(f"/rate-cards/{job.get('rate_card_version')}"), "reading card")
    doubled = {role: int(rate) * 2 for role, rate in (pinned.get("rates") or {}).items()}
    version = f"RC-probe-{conftest.unique_token()}"
    conftest.ok(producer.post("/rate-cards", json={"version": version,
                                                   "effective_from": "2026-01-02",
                                                   "rates": doubled}), "publishing a newer card")
    after = conftest.ok(producer.get(f"/jobs/{job_id}/cost"), "re-reading job cost")
    assert after.get("time_minor") == before.get("time_minor"), (
        f"a newer card must not move an approved job's cost: {before} -> {after}")
    assert after.get("rate_card_version") == before.get("rate_card_version")
    later = conftest.make_job(account_director, producer)
    assert later.get("rate_card_version") == version, (
        f"a job converted after the newer card must pin it: {later.get('rate_card_version')}")


def test_third_party_cost_keeps_original_currency_and_rate(account_director, producer):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    before = conftest.ok(producer.get(f"/jobs/{job_id}/cost"), "reading job cost")
    body = {"supplier": "Probe Studio", "amount_minor": conftest.FOREIGN_AMOUNT,
            "currency": conftest.FOREIGN_CURRENCY, "converted_minor": conftest.CONVERTED_AMOUNT,
            "fx_rate": conftest.FX_RATE, "fx_date": conftest.FX_DATE}
    stored = conftest.ok(producer.post(f"/jobs/{job_id}/costs", json=body), "recording a cost")
    for key in ("amount_minor", "currency", "converted_minor", "fx_date"):
        assert str(stored.get(key)) == str(body[key]), f"{key} must be stored as entered: {stored}"
    assert float(stored.get("fx_rate")) == float(conftest.FX_RATE), f"fx_rate must be kept: {stored}"
    after = conftest.ok(producer.get(f"/jobs/{job_id}/cost"), "re-reading job cost")
    moved = int(after.get("third_party_minor")) - int(before.get("third_party_minor") or 0)
    assert moved == conftest.CONVERTED_AMOUNT, f"the converted 185625 must be added: {before} -> {after}"
    assert int(after.get("total_minor")) == int(after.get("time_minor")) + int(
        after.get("third_party_minor")), f"the job total must add both parts: {after}"


def test_correction_to_a_closed_period_adds_an_adjusting_entry(account_director, producer):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    original = conftest.ok(producer.post(f"/jobs/{job_id}/time-entries", json={
        "person_id": conftest.person_id_of(producer), "role": conftest.ART_DIRECTOR,
        "work_date": "2030-01-15", "minutes": 120}), "recording time")
    conftest.ok(producer.post("/periods/2030-01/close"), "closing January 2030")
    adjusting = conftest.ok(producer.post(
        f"/time-entries/{conftest.ident(original)}/corrections", json={"minutes": 180}),
        "correcting a closed-period entry")
    assert str(adjusting.get("adjusts_entry_id")) == conftest.ident(original), (
        f"the adjusting entry must reference the original: {adjusting}")
    assert int(adjusting.get("minutes")) == 60, f"the adjusting entry carries the difference: {adjusting}"
    entries = conftest.rows(conftest.ok(producer.get(f"/jobs/{job_id}/time-entries"), "listing"))
    kept = conftest.find_by(entries, "id", conftest.ident(original))
    assert kept is not None and int(kept.get("minutes")) == 120, (
        f"the original closed-period entry must stay unchanged: {kept}")
    open_entry = conftest.ok(producer.post(f"/jobs/{job_id}/time-entries", json={
        "person_id": conftest.person_id_of(producer), "role": conftest.ART_DIRECTOR,
        "work_date": "2031-03-10", "minutes": 60}), "recording time in an open month")
    updated = conftest.ok(producer.post(
        f"/time-entries/{conftest.ident(open_entry)}/corrections", json={"minutes": 90}),
        "correcting an open-month entry")
    assert conftest.ident(updated) == conftest.ident(open_entry) and \
        int(updated.get("minutes")) == 90, f"an open-month correction updates the entry: {updated}"


def test_ending_an_assignment_keeps_the_history(account_director, producer):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    person = conftest.make_person(producer)
    conftest.grant(account_director, person, conftest.KAGEROU)
    assignment = conftest.ok(conftest.staff(producer, job_id, person), "staffing")
    conftest.ok(producer.post(f"/assignments/{conftest.ident(assignment)}/end",
                              json={"ends_on": "2031-01-13"}), "ending the assignment")
    listed = conftest.rows(conftest.ok(producer.get(f"/jobs/{job_id}/assignments"), "listing"))
    kept = conftest.find_by(listed, "id", conftest.ident(assignment))
    assert kept is not None and str(kept.get("ends_on")) == "2031-01-13", (
        f"an ended assignment must stay in the history with its end date: {listed}")


def test_assignment_cannot_be_deleted(account_director, producer):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    person = conftest.make_person(producer)
    conftest.grant(account_director, person, conftest.KAGEROU)
    assignment = conftest.ok(conftest.staff(producer, job_id, person), "staffing")
    conftest.refused(producer.delete(f"/assignments/{conftest.ident(assignment)}"),
                     "deleting an assignment")
    listed = conftest.rows(conftest.ok(producer.get(f"/jobs/{job_id}/assignments"), "listing"))
    assert conftest.find_by(listed, "id", conftest.ident(assignment)) is not None, (
        "a refused delete must leave the assignment in place")


def test_version_upload_lands_in_the_bucket_at_the_scheme_key(account_director, producer,
                                                              creative, store, backend):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    payload = conftest.probe_bytes()
    version = conftest.ok(conftest.upload_version(creative, job_id, payload), "uploading")
    expected = conftest.version_key(job_id, version.get("number"), payload)
    assert version.get("object_key") == expected, (
        f"the object key must follow jobs/job_id/versions/number/sha256.ext: {version}")
    assert store.exists(expected), f"the uploaded bytes must exist in the bucket at {expected}"
    assert backend.count("work_versions", object_key=expected) == 1, (
        "work_versions must record the object key once")


def test_new_upload_adds_a_version_and_keeps_the_old_object(account_director, producer,
                                                            creative, store):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    first = conftest.ok(conftest.upload_version(creative, job_id, conftest.probe_bytes()), "upload")
    second = conftest.ok(conftest.upload_version(creative, job_id, conftest.probe_bytes()), "upload")
    assert int(first.get("number")) == 1 and int(second.get("number")) == 2, (
        f"versions must be numbered from 1: {first.get('number')}, {second.get('number')}")
    assert store.exists(first.get("object_key")) and store.exists(second.get("object_key")), (
        "a new upload must keep the earlier version's object")
    listed = conftest.rows(conftest.ok(creative.get(f"/jobs/{job_id}/versions"), "listing"))
    kept = conftest.find_by(listed, "number", 1)
    assert kept is not None and kept.get("sha256") == first.get("sha256"), (
        "the first version's bytes must never be replaced")


def test_rollback_creates_a_new_version_with_the_earlier_content(account_director, producer,
                                                                 creative):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    first = conftest.ok(conftest.upload_version(creative, job_id, conftest.probe_bytes()), "upload")
    conftest.ok(conftest.upload_version(creative, job_id, conftest.probe_bytes()), "upload")
    restored = conftest.ok(creative.post(f"/jobs/{job_id}/versions/1/restore"), "restoring v1")
    assert int(restored.get("number")) == 3, f"a restore must add version 3: {restored}"
    assert restored.get("sha256") == first.get("sha256"), "the restored version carries v1's digest"
    assert str(restored.get("restored_from")) == "1", f"the restore must record its source: {restored}"
    listed = conftest.rows(conftest.ok(creative.get(f"/jobs/{job_id}/versions"), "listing"))
    assert sorted(int(v.get("number")) for v in listed) == [1, 2, 3], (
        "a restore must remove no intervening version")


def test_version_under_legal_hold_cannot_be_deleted(account_director, producer, creative,
                                                    legal, store):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    version = conftest.ok(conftest.upload_version(creative, job_id, conftest.probe_bytes()), "upload")
    person = conftest.make_person(producer)
    conftest.grant(account_director, person, conftest.KAGEROU)
    assignment = conftest.ok(conftest.staff(producer, job_id, person), "staffing")
    conftest.ok(legal.post(f"/jobs/{job_id}/legal-hold", json={"reason": "Probe dispute"}),
                "placing a legal hold")
    conftest.refused(producer.delete(f"/jobs/{job_id}/versions/1"),
                     "deleting a version under legal hold")
    conftest.refused(producer.post(f"/assignments/{conftest.ident(assignment)}/end",
                                   json={"ends_on": "2031-01-13"}),
                     "altering an assignment on a job under legal hold")
    listed = conftest.rows(conftest.ok(producer.get(f"/jobs/{job_id}/versions"), "listing"))
    assert conftest.find_by(listed, "number", 1) is not None, "the held version must remain"
    assert store.exists(version.get("object_key")), "the held version's bytes must remain"


def test_confirmed_result_moves_campaign_news_and_agency_totals_together(editor, anon):
    campaign = conftest.campaign_by_slug(editor, conftest.BLUE_HOUR_RAIL)
    token = conftest.unique_token()
    category = conftest.ok(editor.post(f"/award-bodies/{conftest.LOTUS}/categories", json={
        "section": "Probe", "name": f"Probe {token}"}), "adding a category")
    year = 2031
    article = conftest.ok(editor.post("/articles", json={
        "slug": f"probe-results-{token}", "date": "2026-05-01", "categories": ["awards"],
        "award_body": conftest.LOTUS, "award_year": year, "title_ja": f"検証 {token}",
        "title_en": f"Probe results {token}", "body_ja": "本文", "body_en": "Body"}),
        "creating an award article")
    conftest.ok(editor.post(f"/articles/{conftest.ident(article)}/publish", json={}),
                "publishing the award article")

    def surfaces():
        total = int(conftest.tally(anon, conftest.LOTUS, year).get("total") or 0)
        detail = conftest.ok(anon.get(f"/public/campaigns/{conftest.BLUE_HOUR_RAIL}",
                                      params={"locale": "en"}), "reading the campaign")
        on_page = sum(len(g.get("results") or []) for g in detail.get("awards") or []
                      if str(g.get("year")) == str(year))
        news = conftest.ok(anon.get(f"/public/news/{article.get('slug')}",
                                    params={"locale": "en"}), "reading the article")
        return total, on_page, len(news.get("breakdown") or [])

    before = surfaces()
    entry = conftest.ok(editor.post("/award-entries", json={
        "campaign_id": conftest.ident(campaign), "body": conftest.LOTUS,
        "category_id": conftest.ident(category), "year": year, "fee_minor": 150000,
        "client_permission_ref": f"PERM-{token}"}), "entering the campaign")
    conftest.ok(editor.post(f"/award-entries/{conftest.ident(entry)}/results",
                            json={"rank": "Silver", "confirmed": True}), "confirming a result")
    after = surfaces()
    assert after == tuple(v + 1 for v in before), (
        f"one confirmed result must move the tally, the campaign page and the article "
        f"together: {before} -> {after}")


def test_only_confirmed_results_reach_the_public_tally(editor, anon):
    campaign = conftest.campaign_by_slug(editor, conftest.BLUE_HOUR_RAIL)
    token = conftest.unique_token()
    category = conftest.ok(editor.post(f"/award-bodies/{conftest.LOTUS}/categories", json={
        "section": "Probe", "name": f"Shortlist {token}"}), "adding a category")
    year = 2032
    before = int(conftest.tally(anon, conftest.LOTUS, year).get("total") or 0)
    entry = conftest.ok(editor.post("/award-entries", json={
        "campaign_id": conftest.ident(campaign), "body": conftest.LOTUS,
        "category_id": conftest.ident(category), "year": year, "fee_minor": 150000,
        "client_permission_ref": f"PERM-{token}"}), "entering the campaign")
    result = conftest.ok(editor.post(f"/award-entries/{conftest.ident(entry)}/results",
                                     json={"rank": "Bronze", "confirmed": False}),
                         "recording a shortlisted result")
    conftest.settle()
    assert int(conftest.tally(anon, conftest.LOTUS, year).get("total") or 0) == before, (
        "an unconfirmed result must never reach the public tally")
    conftest.ok(editor.post(f"/award-results/{conftest.ident(result)}/confirm"), "confirming")
    assert int(conftest.tally(anon, conftest.LOTUS, year).get("total") or 0) == before + 1, (
        "a confirmed result must reach the public tally")


def test_duplicate_award_entry_for_one_category_is_refused(editor):
    campaign = conftest.campaign_by_slug(editor, conftest.BLUE_HOUR_RAIL)
    token = conftest.unique_token()
    category = conftest.ok(editor.post(f"/award-bodies/{conftest.LOTUS}/categories", json={
        "section": "Probe", "name": f"Duplicate {token}"}), "adding a category")
    body = {"campaign_id": conftest.ident(campaign), "body": conftest.LOTUS,
            "category_id": conftest.ident(category), "year": 2033, "fee_minor": 150000,
            "client_permission_ref": f"PERM-{token}"}
    job_id = str(campaign.get("job_id"))
    before = conftest.ok(editor.get(f"/jobs/{job_id}/cost"), "reading the campaign job cost")
    entry = conftest.ok(editor.post("/award-entries", json=body), "entering once")
    assert entry.get("status") == "submitted", f"a new entry is submitted: {entry}"
    conftest.refused(editor.post("/award-entries", json=body),
                     "entering the same campaign, body, category and year twice")
    after = conftest.ok(editor.get(f"/jobs/{job_id}/cost"), "re-reading the campaign job cost")
    moved = int(after.get("third_party_minor") or 0) - int(before.get("third_party_minor") or 0)
    assert moved == conftest.ENTRY_FEE, f"the entry fee must be a third-party cost: {before} -> {after}"
    closed = conftest.ok(editor.post(f"/award-entries/{conftest.ident(entry)}/close"), "closing")
    assert closed.get("status") == "closed", f"closing with no result sets closed: {closed}"


def test_burn_report_counts_only_permitted_jobs(creative, creative2):
    for client in (creative, creative2):
        jobs = conftest.rows(conftest.ok(client.get("/jobs"), "listing jobs"))
        report = conftest.ok(client.get("/reports/burn"), "reading the burn report")
        assert int(report.get("jobs_counted")) == len(jobs), (
            f"the burn report must count exactly the readable jobs: {report} vs {len(jobs)}")
        assert int(report.get("estimate_minor")) == sum(int(j.get("estimate_minor") or 0)
                                                        for j in jobs), (
            f"the burn estimate must equal the readable jobs' estimates: {report}")
    walled = [j for j in conftest.rows(creative2.get("/jobs").json())
              if j.get("title") == conftest.WALLED_JOB_TITLE]
    assert walled == [], "the walled job must not feed creative2's totals"


def test_page_view_is_recorded_for_a_public_route(anon, editor, backend):
    route = f"/work/probe-{conftest.unique_token()}/"
    conftest.ok(anon.post("/page-views", json={"route": route}), "recording a page view")
    assert backend.count("page_views", route=route) == 1, "one page view must write one row"
    log = conftest.rows(conftest.ok(editor.get("/page-views"), "reading the page-view log"))
    assert any(str(r.get("route")) == route for r in log), "the editor must read the recorded view"


def test_audit_log_refuses_edits(account_director, producer, legal):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    conftest.ok(legal.post(f"/jobs/{job_id}/legal-hold", json={"reason": "Probe dispute"}), "hold")
    events = conftest.rows(conftest.ok(legal.get(f"/jobs/{job_id}/audit"), "reading audit"))
    assert events, "placing a hold must write an audit event"
    event_id = conftest.ident(events[0])
    conftest.refused(legal.delete(f"/audit-events/{event_id}"), "deleting an audit event")
    again = conftest.rows(conftest.ok(legal.get(f"/jobs/{job_id}/audit"), "re-reading audit"))
    assert conftest.find_by(again, "id", event_id) is not None, "the audit event must remain"


def test_walled_job_fetch_matches_a_missing_job(creative, creative2):
    job_id = conftest.job_id_titled(creative, conftest.WALLED_JOB_TITLE)
    walled = creative2.get(f"/jobs/{job_id}")
    missing = creative2.get(f"/jobs/{conftest.absent_id_like(job_id)}")
    assert walled.status_code == 404 and missing.status_code == 404, (
        f"a walled job and a missing job must both answer not-found: "
        f"{conftest.describe(walled)} | {conftest.describe(missing)}")
    shape = lambda r: sorted(r.json().keys()) if isinstance(r.json(), dict) else type(r.json()).__name__
    assert shape(walled) == shape(missing), (
        f"the walled and missing bodies must share one shape: {walled.text} | {missing.text}")
    assert conftest.WALLED_JOB_TITLE not in walled.text


def test_walled_job_is_absent_from_list_search_and_autocomplete(creative, creative2):
    visible = [j.get("title") for j in conftest.rows(creative.get("/jobs").json())]
    assert conftest.WALLED_JOB_TITLE in visible, "the cleared creative must read the job"
    hidden = [j.get("title") for j in conftest.rows(creative2.get("/jobs").json())]
    assert conftest.WALLED_JOB_TITLE not in hidden, f"creative2's job list leaks the job: {hidden}"
    for path, query in (("/search", "Hoshino EV"), ("/search", "Midnight"),
                        ("/autocomplete", "Hoshino"), ("/autocomplete", "Midnight")):
        response = conftest.ok(creative2.get(path, params={"q": query}), f"{path} {query}")
        text = conftest.flat(response)
        assert "hoshino ev launch" not in text and "midnight charge" not in text, (
            f"{path}?q={query} leaks the walled work to creative2: {text[:300]}")
    found = conftest.flat(conftest.ok(creative.get("/search", params={"q": "Midnight"}), "search"))
    assert "midnight charge" in found, "the cleared creative's search must find Midnight Charge"


def test_walled_job_audit_log_is_denied(creative, creative2):
    job_id = conftest.job_id_titled(creative, conftest.WALLED_JOB_TITLE)
    response = creative2.get(f"/jobs/{job_id}/audit")
    assert response.status_code == 404, (
        "reading a walled job's audit trail must answer as a missing job does: "
        + conftest.describe(response))


def test_job_export_omits_walled_rows(creative, creative2):
    hidden = creative2.get("/reports/jobs.csv")
    assert hidden.status_code == 200, "the export must be readable: " + conftest.describe(hidden)
    assert conftest.WALLED_JOB_TITLE not in hidden.text, "creative2's export leaks the walled job"
    shown = creative.get("/reports/jobs.csv")
    assert conftest.WALLED_JOB_TITLE in shown.text, "the cleared creative's export must list the job"


def test_directory_history_hides_walled_assignments_without_a_count(creative, creative2):
    haru = conftest.person_id_of(creative)
    readable = {conftest.ident(j) for j in conftest.rows(creative2.get("/jobs").json())}
    profile = conftest.ok(creative2.get(f"/people/{haru}"), "reading a colleague")
    history = profile.get("assignments") or []
    assert all(str(a.get("job_id")) in readable for a in history), (
        f"creative2 must see only assignments on readable jobs: {history}")
    text = conftest.flat(profile)
    assert "hoshino ev launch" not in text and "hidden" not in text, (
        f"the profile must carry no trace or count of walled work: {text[:300]}")


def test_split_job_is_visible_only_with_clearance_for_every_account(producer, creative):
    job_id = conftest.job_id_titled(producer, conftest.SPLIT_JOB_TITLE)
    shown = producer.get(f"/jobs/{job_id}")
    assert shown.status_code == 200, "the producer cleared for both accounts must read the split job"
    shares = {str(a.get("account")): int(a.get("share_bp"))
              for a in (shown.json().get("apportionment") or [])}
    assert shares == dict(conftest.SPLIT_SHARES), f"the split must be 6000 and 4000: {shares}"
    hidden = creative.get(f"/jobs/{job_id}")
    assert hidden.status_code == 404, (
        "a creative cleared for kagerou only must get not-found on the split job: "
        + conftest.describe(hidden))


def test_split_job_apportionment_must_sum_to_the_whole(account_director2, producer, backend):
    brief = conftest.open_brief(account_director2, (conftest.AOZORA, conftest.MINATO))
    conftest.approved_estimate(account_director2, producer, brief)
    response = conftest.convert(account_director2, brief, conftest.person_id_of(producer),
                                ((conftest.AOZORA, 6000), (conftest.MINATO, 3000)))
    conftest.refused(response, "converting with shares that miss 10000")
    assert conftest.job_titled(account_director2, brief.get("title")) is None, (
        "a refused split conversion must write no job")


def test_person_cleared_for_a_rival_cannot_be_staffed(account_director2, producer):
    person = conftest.make_person(producer)
    conftest.ok(conftest.grant(account_director2, person, conftest.TSUBAME), "granting tsubame")
    job_id = conftest.job_id_titled(producer, conftest.WALLED_JOB_TITLE)
    conftest.refused(conftest.staff(producer, job_id, person),
                     "staffing a tsubame-cleared person onto a hoshino job")


def test_overcommitted_person_is_refused_without_naming_the_blocking_job(
        account_director, account_director2, producer, producer2):
    person = conftest.make_person(producer2)
    conftest.ok(conftest.grant(account_director2, person, conftest.TSUBAME), "granting tsubame")
    conftest.ok(conftest.grant(account_director, person, conftest.KAGEROU), "granting kagerou")
    rival_id = conftest.job_id_titled(producer2, conftest.RIVAL_JOB_TITLE)
    conftest.ok(conftest.staff(producer2, rival_id, person, starts="2031-06-02",
                               ends="2031-06-29", minutes=conftest.WEEKLY_CAPACITY),
                "committing the person's full week on the rival job")
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    response = conftest.staff(producer, job_id, person, starts="2031-06-09",
                              ends="2031-06-22", minutes=600)
    conftest.refused(response, "staffing a fully committed person")
    assert conftest.CAPACITY_REFUSAL in response.text, (
        "the refusal must say the person is fully committed: " + conftest.describe(response))
    assert conftest.RIVAL_JOB_TITLE not in response.text and rival_id not in response.text, (
        "the refusal must not name the walled job: " + conftest.describe(response))


def test_clearance_for_a_competitor_is_refused_during_cooling_off(account_director,
                                                                  account_director2, producer):
    person = conftest.make_person(producer)
    conftest.ok(conftest.grant(account_director, person, conftest.HOSHINO), "granting hoshino")
    conftest.refused(conftest.grant(account_director2, person, conftest.TSUBAME),
                     "granting a competitor while the rival clearance is held")
    detail = conftest.ok(producer.get(f"/people/{conftest.ident(person)}"), "reading the person")
    held = conftest.find_by(detail.get("clearances") or [], "account", conftest.HOSHINO)
    conftest.ok(account_director.post(f"/clearances/{conftest.ident(held)}/revoke",
                                      json={"revoked_on": "2026-06-01"}), "revoking hoshino")
    conftest.refused(conftest.grant(account_director2, person, conftest.TSUBAME),
                     "granting a competitor within the ninety-day cooling-off")


def test_client_dedicated_unit_derives_a_clearance(account_director2, producer):
    person = conftest.make_person(producer, unit=conftest.HOSHINO_UNIT)
    detail = conftest.ok(producer.get(f"/people/{conftest.ident(person)}"), "reading the person")
    accounts = [str(c.get("account")) for c in detail.get("clearances") or []
                if not c.get("revoked_on")]
    assert conftest.HOSHINO in accounts, (
        f"a Hoshino Unit member must hold a derived hoshino clearance: {detail.get('clearances')}")
    conftest.refused(conftest.grant(account_director2, person, conftest.TSUBAME),
                     "granting tsubame to a Hoshino Unit member")


def test_creative_is_forbidden_to_publish(account_director, producer, legal, editor, creative,
                                          anon):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    conftest.refused(conftest.publish(creative, made["campaign_id"]),
                     "a creative publishing a campaign")
    assert conftest.campaign_by_slug(editor, made["slug"]).get("state") == "draft", (
        "a denied publish must leave the campaign a draft")
    assert anon.get(f"/public/campaigns/{made['slug']}").status_code == 404


def test_creative_cannot_approve_an_estimate(account_director, producer, creative):
    brief = conftest.open_brief(account_director)
    estimate = conftest.ok(producer.post(f"/briefs/{conftest.ident(brief)}/estimates",
                                         json={"amount_minor": 4000000}), "writing an estimate")
    conftest.refused(creative.post(f"/estimates/{conftest.ident(estimate)}/approve"),
                     "a creative approving an estimate")
    response = conftest.convert(account_director, brief, conftest.person_id_of(producer),
                                ((conftest.KAGEROU, conftest.APPORTIONMENT_WHOLE),))
    conftest.refused(response, "converting after a denied approval, since the estimate stays unapproved")


def test_producer_is_denied_lifting_a_legal_hold(account_director, producer, legal):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    conftest.ok(legal.post(f"/jobs/{job_id}/legal-hold", json={"reason": "Probe dispute"}), "hold")
    conftest.refused(producer.post(f"/jobs/{job_id}/legal-hold/lift",
                                   json={"reason": "Producer tries"}), "a producer lifting a hold")
    job = conftest.ok(legal.get(f"/jobs/{job_id}"), "reading the held job")
    assert job.get("legal_hold") is True, f"a denied lift must leave the hold in place: {job}"


def test_lifting_a_hold_requires_a_reason_and_is_audited(account_director, producer, legal):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    conftest.ok(legal.post(f"/jobs/{job_id}/legal-hold", json={"reason": "Probe dispute"}), "hold")
    conftest.refused(legal.post(f"/jobs/{job_id}/legal-hold/lift", json={"reason": ""}),
                     "lifting a hold with no reason")
    assert conftest.ok(legal.get(f"/jobs/{job_id}"), "reading").get("legal_hold") is True
    reason = f"Settled {conftest.unique_token()}"
    lifted = conftest.ok(legal.post(f"/jobs/{job_id}/legal-hold/lift", json={"reason": reason}),
                         "lifting the hold with a reason")
    assert lifted.get("legal_hold") is False, f"the hold must be lifted: {lifted}"
    events = conftest.rows(conftest.ok(legal.get(f"/jobs/{job_id}/audit"), "reading audit"))
    assert any(str(e.get("reason")) == reason and e.get("actor_person_id") for e in events), (
        f"the lift must be audited with its actor and reason: {events}")


def test_studio_api_is_denied_to_an_unauthenticated_caller(anon):
    for path in conftest.STUDIO_READ_ROUTES:
        response = anon.get(path)
        assert response.status_code in (401, 403), (
            f"GET /api{path} must refuse a caller with no token: " + conftest.describe(response))


def test_login_issues_a_token_and_denies_a_wrong_password(anon):
    good = anon.post("/auth/login", json={"email": conftest.EDITOR_EMAIL,
                                          "password": conftest.APP_PASSWORD})
    assert good.status_code == 200 and good.json().get("access_token"), (
        "the seeded editor must sign in and receive access_token: " + conftest.describe(good))
    bad = anon.post("/auth/login", json={"email": conftest.EDITOR_EMAIL, "password": "wrong-pw-1"})
    assert bad.status_code in (400, 401, 403), "a wrong password must be refused: " + conftest.describe(bad)


def test_signup_is_closed(anon, backend):
    email = conftest.probe_email()
    response = anon.post("/auth/signup", json={"email": email, "password": conftest.APP_PASSWORD,
                                                "role": "editor"})
    conftest.refused(response, "signing up")
    assert backend.count("users", email=email) == 0, "a refused signup must create no account"


def test_page_view_log_is_denied_to_a_creative(creative):
    response = creative.get("/page-views")
    assert response.status_code in (401, 403, 404), (
        "only an editor reads the page-view log: " + conftest.describe(response))


def test_internal_comment_is_absent_from_the_client_view(account_director, producer, creative):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    conftest.ok(conftest.upload_version(creative, job_id, conftest.probe_bytes()), "upload")
    secret = f"internal-note-{conftest.unique_token()}"
    shared = f"client-note-{conftest.unique_token()}"
    conftest.ok(creative.post(f"/jobs/{job_id}/versions/1/comments", json={
        "body": secret, "visibility": conftest.INTERNAL, "timecode": "00:00:04"}), "commenting")
    conftest.ok(creative.post(f"/jobs/{job_id}/versions/1/comments", json={
        "body": shared, "visibility": conftest.CLIENT, "timecode": "00:00:09"}), "commenting")
    client_view = creative.get(f"/jobs/{job_id}/versions/1/client-view")
    assert client_view.status_code == 200, "the client view must be readable"
    assert secret not in client_view.text, "an internal comment must never reach the client view"
    assert shared in client_view.text, "the client comment must appear in the client view"
    internal = creative.get(f"/jobs/{job_id}/versions/1").text
    assert secret in internal and shared in internal, "the internal view carries both comments"


def test_version_bytes_are_denied_to_an_uncleared_creative(account_director, producer,
                                                            creative, creative2):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    conftest.ok(conftest.upload_version(creative, job_id, conftest.probe_bytes()), "upload")
    response = creative2.get(f"/jobs/{job_id}/versions/1/content")
    assert response.status_code == 404, (
        "a creative outside the wall must not receive the version bytes: "
        + conftest.describe(response))


def test_unknown_address_answers_the_designed_not_found(site):
    for prefix in ("", "/wp-json"):
        marker = f"no-such-page-{conftest.unique_token()}"
        response = site.get(f"{prefix}/{marker}/")
        assert response.status_code == 404, (
            f"the address {prefix}/{marker}/ must answer 404: " + conftest.describe(response))
        assert marker not in response.text, "the requested path must never be echoed into the page"


def test_embargoed_campaign_address_matches_an_unknown_address(site, anon):
    unknown = f"no-such-campaign-{conftest.unique_token()}"
    for prefix in ("", "/en"):
        page = site.get(f"{prefix}/work/{conftest.SILENT_AURORA}/")
        missing = site.get(f"{prefix}/work/{unknown}/")
        assert page.status_code == 404 == missing.status_code, (
            f"the embargoed address must answer exactly as an unknown one: "
            f"{conftest.describe(page)} | {conftest.describe(missing)}")
        assert conftest.SILENT_AURORA_TITLE not in page.text
    api = anon.get(f"/public/campaigns/{conftest.SILENT_AURORA}")
    assert api.status_code == 404 == anon.get(f"/public/campaigns/{unknown}").status_code


def test_embargoed_campaign_is_absent_from_every_public_read(anon, site):
    assert conftest.SILENT_AURORA not in conftest.all_public_slugs(anon)
    assert conftest.SILENT_AURORA not in conftest.all_public_slugs(anon, locale="en")
    for query in (conftest.SILENT_AURORA_TITLE, conftest.SILENT_AURORA_TITLE_JA):
        found = conftest.flat(conftest.ok(anon.get("/public/search", params={"q": query}), "search"))
        assert conftest.SILENT_AURORA not in found, f"public search for {query} leaks the embargo"
    sitemap = site.get("/sitemap.xml")
    assert conftest.SILENT_AURORA not in sitemap.text, "the sitemap must not list the embargoed campaign"


def test_embargoed_campaign_asset_is_not_served_publicly(editor, anon):
    campaign = conftest.campaign_by_slug(editor, conftest.SILENT_AURORA)
    asset = campaign.get("hero_asset_id")
    assert asset, f"Silent Aurora must carry a hero asset: {campaign}"
    response = anon.get(f"/public/assets/{asset}")
    assert response.status_code == 404, (
        "an embargoed campaign's hero bytes must never reach the public: " + conftest.describe(response))


def test_hero_upload_lands_in_the_bucket_and_serves_once_public(account_director, producer,
                                                                legal, editor, anon, store):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    payload = conftest.probe_bytes()
    media = conftest.ok(editor.post(f"/campaigns/{made['campaign_id']}/hero",
                                    files={"file": ("hero.png", payload, "image/png")},
                                    data={"alt_en": "A probe still.", "alt_ja": "検証の静止画"}),
                        "uploading a hero still")
    expected = conftest.hero_key(made["campaign_id"], payload)
    assert media.get("object_key") == expected, f"the hero key must follow the scheme: {media}"
    assert store.exists(expected), f"the hero bytes must exist in the bucket at {expected}"
    before = anon.get(f"/public/assets/{conftest.ident(media)}")
    assert before.status_code == 404, "an unpublished hero must not be served publicly"
    conftest.ok(conftest.publish(editor, made["campaign_id"]), "publishing")
    after = anon.get(f"/public/assets/{conftest.ident(media)}")
    assert after.status_code == 200 and after.content == payload, (
        "once public, the hero bytes must be served from the bucket unchanged")


def test_list_endpoints_return_top_level_arrays(editor):
    for path in ("/jobs", "/clients", "/people", "/rate-cards", "/award-bodies", "/page-views"):
        response = conftest.ok(editor.get(path), f"GET /api{path}")
        assert isinstance(response, list), f"GET /api{path} must return a top-level array"


def test_enquiry_without_consent_is_refused(anon, backend):
    key = conftest.enquiry_key(anon)
    conftest.refused(anon.post("/enquiries", json=conftest.enquiry_body(key, consent=False)),
                     "an enquiry without consent")
    assert backend.count("enquiries", idempotency_key=key) == 0, "a refused enquiry stores nothing"


def test_enquiry_with_the_decoy_field_filled_is_refused(anon, backend):
    key = conftest.enquiry_key(anon)
    body = conftest.enquiry_body(key, **{conftest.DECOY_FIELD: "https://spam.example.org"})
    conftest.refused(anon.post("/enquiries", json=body), "an enquiry with the decoy field filled")
    assert backend.count("enquiries", idempotency_key=key) == 0, "a refused enquiry stores nothing"


def test_enquiry_for_a_route_with_no_recipient_reaches_the_default_desk(anon):
    general = conftest.ok(anon.post("/enquiries", json=conftest.enquiry_body(
        conftest.enquiry_key(anon), type="general")), "a general enquiry")
    assert general.get("routed_to") == conftest.DEFAULT_DESK, f"general must reach the desk: {general}"
    assert general.get("routing_warning") is True, f"the fallback must record a warning: {general}"
    business = conftest.ok(anon.post("/enquiries", json=conftest.enquiry_body(
        conftest.enquiry_key(anon), type="new_business")), "a new business enquiry")
    assert business.get("routed_to") == conftest.NEW_BUSINESS_DESK, f"routing table ignored: {business}"
    for kind, desk in (("recruitment", conftest.RECRUITMENT_DESK), ("press", conftest.PRESS_DESK)):
        routed = conftest.ok(anon.post("/enquiries", json=conftest.enquiry_body(
            conftest.enquiry_key(anon), type=kind)), f"a {kind} enquiry")
        assert routed.get("routed_to") == desk, f"{kind} must route to {desk}: {routed}"


def test_internal_and_client_review_statuses_move_independently(account_director, producer,
                                                                 creative):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    conftest.ok(conftest.upload_version(creative, job_id, conftest.probe_bytes()), "upload")
    conftest.ok(account_director.post(f"/jobs/{job_id}/versions/1/client-review",
                                      json={"status": "approved"}), "client approval")
    withdrawn = conftest.ok(creative.post(f"/jobs/{job_id}/versions/1/internal-review",
                                          json={"status": "withdrawn"}), "internal withdrawal")
    assert withdrawn.get("internal_status") == "withdrawn", f"internal status must move: {withdrawn}"
    assert withdrawn.get("client_status") == "approved", (
        f"setting the internal track must leave the client approval in place: {withdrawn}")


def test_comment_stays_on_its_version_after_a_new_upload(account_director, producer, creative):
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    conftest.ok(conftest.upload_version(creative, job_id, conftest.probe_bytes()), "upload v1")
    note = f"v1-note-{conftest.unique_token()}"
    conftest.ok(creative.post(f"/jobs/{job_id}/versions/1/comments", json={
        "body": note, "visibility": conftest.INTERNAL, "region": "top-left"}), "commenting")
    conftest.ok(conftest.upload_version(creative, job_id, conftest.probe_bytes()), "upload v2")
    assert note in creative.get(f"/jobs/{job_id}/versions/1").text, "the comment stays on v1"
    assert note not in creative.get(f"/jobs/{job_id}/versions/2").text, "the comment is not on v2"


def test_public_images_carry_alternative_text(page, app_url):
    described = 0
    for path in conftest.IMAGE_PAGES:
        page.goto(f"{app_url}{path}", wait_until="networkidle")
        missing = page.eval_on_selector_all(
            "img", "els => els.filter(e => !e.hasAttribute('alt')).map(e => e.src)")
        assert missing == [], f"every image on {path} must carry alternative text: {missing}"
        unsized = page.eval_on_selector_all(
            "img", "els => els.filter(e => !(e.hasAttribute('width') && e.hasAttribute('height')))"
                   ".map(e => e.src)")
        assert unsized == [], f"every image on {path} must declare its dimensions: {unsized}"
        described += page.eval_on_selector_all(
            "img", "els => els.filter(e => (e.getAttribute('alt') || '').trim()).length")
    assert described > 0, "content images must describe what they show"


def test_body_text_meets_the_contrast_bar(page, app_url):
    for path in conftest.CONTRAST_PAGES:
        page.goto(f"{app_url}{path}", wait_until="networkidle")
        ratios = page.evaluate(conftest.CONTRAST_SCRIPT)
        assert ratios, f"{path} must render body paragraphs"
        worst = min(ratios)
        assert worst >= conftest.CONTRAST_FLOOR, (
            f"body text on {path} must reach 4.5 to 1 contrast; the lowest was {worst:.2f}")


def test_terms_page_is_linked_from_every_footer_and_the_contact_form(page, app_url):
    for path in conftest.PUBLIC_PAGES:
        page.goto(f"{app_url}{path}", wait_until="networkidle")
        footer_links = page.get_by_role("contentinfo").locator("a[href*='terms']").count()
        assert footer_links >= 1, f"the footer on {path} must link to the terms page"
    page.goto(f"{app_url}/contact/", wait_until="networkidle")
    assert page.locator("form a[href*='terms']").count() >= 1, (
        "the contact form must link to the terms page beside the consent box")


def test_sitemap_lists_public_routes_without_embargoed_work(site):
    response = site.get("/sitemap.xml")
    assert response.status_code == 200, "the sitemap must be served: " + conftest.describe(response)
    for expected in ("/work/night-signal/", "/en/work/night-signal/", "/terms/", "/en/terms/",
                     "/privacy/", "/en/privacy/"):
        assert expected in response.text, f"the sitemap must list {expected}"
    for hidden in (conftest.SILENT_AURORA, conftest.WINTER_KITE):
        assert hidden not in response.text, f"the sitemap must not list {hidden}"


def test_robots_file_points_at_the_sitemap(site):
    response = site.get("/robots.txt")
    assert response.status_code == 200, "robots.txt must be served: " + conftest.describe(response)
    lowered = response.text.lower()
    assert "sitemap:" in lowered and "sitemap.xml" in lowered, (
        f"robots.txt must name the sitemap: {response.text[:300]}")
    assert "/studio" in lowered, "robots.txt must keep the studio out of indexing"


def test_security_headers_are_present_on_every_response(site):
    for path in conftest.SECURITY_PAGES:
        response = site.get(path)
        headers = {k.lower(): v for k, v in response.headers.items()}
        assert headers.get("x-content-type-options", "").lower() == "nosniff", (
            f"{path} must refuse content sniffing: {headers}")
        assert "content-security-policy" in headers, f"{path} must carry a content security policy"
        assert "referrer-policy" in headers, f"{path} must carry a referrer policy"
        assert "frame-ancestors" in headers.get("content-security-policy", "") or \
            "x-frame-options" in headers, f"{path} must deny framing: {headers}"


def test_seeded_password_is_stored_hashed(backend):
    stored = backend.rows("users", email=conftest.EDITOR_EMAIL)
    assert stored, "the seeded editor account must exist in users"
    values = " ".join(str(v) for v in stored[0].values())
    assert conftest.APP_PASSWORD not in values, "the seeded password must be stored hashed"


def test_browser_downloads_carry_no_secret(site):
    secrets = conftest.secret_values()
    assert secrets, "the object store key pair must be present in the environment"
    shell = site.get("/")
    bodies = [shell.text]
    for source in conftest.script_sources(shell.text):
        assert source.startswith("/") and not source.startswith("//"), (
            f"every script must come from the app's own origin, found {source}")
        bodies.append(site.get(source).text)
    assert len(bodies) > 1, "the page shell must load at least one script bundle"
    for body in bodies:
        for secret in secrets:
            assert secret not in body, "a script the browser downloads carries a storage credential"


def test_enquiry_sent_immediately_after_the_key_is_refused(anon, backend):
    issued = conftest.ok(anon.get("/enquiries/key"), "fetching an enquiry key")
    key = str(issued.get("idempotency_key"))
    conftest.refused(anon.post("/enquiries", json=conftest.enquiry_body(key)),
                     "an enquiry sent less than one second after its key was issued")
    assert backend.count("enquiries", idempotency_key=key) == 0, "a refused enquiry stores nothing"



def test_overcommitment_on_a_readable_job_names_the_conflicting_job(account_director,
                                                                   producer):
    person = conftest.make_person(producer)
    conftest.ok(conftest.grant(account_director, person, conftest.KAGEROU), "granting kagerou")
    first = conftest.make_job(account_director, producer)
    conftest.ok(conftest.staff(producer, conftest.ident(first), person, starts="2031-09-01",
                               ends="2031-09-28", minutes=conftest.WEEKLY_CAPACITY),
                "committing the full week on a readable job")
    second = conftest.make_job(account_director, producer)
    response = conftest.staff(producer, conftest.ident(second), person, starts="2031-09-08",
                              ends="2031-09-21", minutes=300)
    conftest.refused(response, "staffing past capacity against a readable job")
    assert first.get("title") in response.text or conftest.ident(first) in response.text, (
        "a refusal the producer may fully read must name the conflicting job: "
        + conftest.describe(response))


def test_no_seeded_account_reads_both_rival_jobs():
    for email in conftest.SEEDED_EMAILS:
        with conftest.client_for(email) as client:
            titles = {j.get("title") for j in conftest.rows(
                conftest.ok(client.get("/jobs"), f"listing jobs as {email}"))}
        assert not ({conftest.WALLED_JOB_TITLE, conftest.RIVAL_JOB_TITLE} <= titles), (
            f"{email} reads jobs of both rival car makers, which no account may do")


def test_embargoed_article_is_absent_from_the_newsroom(editor, anon):
    token = conftest.unique_token()
    slug = f"probe-embargoed-{token}"
    article = conftest.ok(editor.post("/articles", json={
        "slug": slug, "date": "2026-05-02", "categories": ["news"], "award_body": None,
        "award_year": None, "title_ja": f"検証 {token}", "title_en": f"Probe embargo {token}",
        "body_ja": "本文", "body_en": "Body"}), "creating an article")
    conftest.ok(editor.post(f"/articles/{conftest.ident(article)}/publish",
                            json={"embargo_at": "2099-01-01T09:00:00+09:00"}),
                "scheduling the article behind an embargo")
    listing = conftest.ok(anon.get("/public/news", params={"category": "news"}), "news")
    slugs = [str(r.get("slug")) for r in conftest.rows(listing)]
    assert slug not in slugs, "an embargoed article must be absent from the newsroom"
    detail = anon.get(f"/public/news/{slug}")
    assert detail.status_code == 404, (
        "an embargoed article must answer not-found: " + conftest.describe(detail))


def test_home_page_carries_the_pinned_copy(page, app_url):
    page.goto(f"{app_url}/", wait_until="networkidle")
    text = conftest.normalised(page.evaluate(conftest.PAGE_TEXT_SCRIPT))
    for line in conftest.HOME_COPY + conftest.HOME_FACTS:
        assert conftest.normalised(line).rstrip(".") in text, (
            f"the home page must carry the pinned line {line!r}")


def test_each_role_is_refused_writes_outside_its_desk(account_director, producer, legal, editor,
                                                      creative):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    job_id = made["job_id"]
    campaign_id = made["campaign_id"]
    brief = conftest.open_brief(account_director)
    estimate = conftest.ok(producer.post(f"/briefs/{conftest.ident(brief)}/estimates",
                                         json={"amount_minor": 3000000}), "writing an estimate")
    target = conftest.make_person(producer)
    cards_before = conftest.rows(conftest.ok(producer.get("/rate-cards"), "listing rate cards"))
    conftest.refused(creative.post("/rate-cards", json={
        "version": f"RC-PROBE-{conftest.unique_token()}", "effective_from": "2032-01-01",
        "rates": {conftest.ART_DIRECTOR: 1}}), "a creative publishing a rate card")
    conftest.refused(creative.post(f"/jobs/{job_id}/legal-hold", json={"reason": "probe"}),
                     "a creative placing a legal hold")
    conftest.refused(conftest.grant(creative, target, conftest.KAGEROU),
                     "a creative granting a clearance")
    conftest.refused(account_director.post(f"/briefs/{conftest.ident(brief)}/estimates",
                                           json={"amount_minor": 1}),
                     "an account director writing an estimate")
    conftest.refused(conftest.staff(account_director, job_id, target),
                     "an account director staffing a crew")
    conftest.refused(producer.post(f"/estimates/{conftest.ident(estimate)}/approve"),
                     "a producer approving an estimate")
    conftest.refused(conftest.add_right(producer, job_id), "a producer recording rights")
    conftest.refused(creative.post(f"/estimates/{conftest.ident(estimate)}/approve"),
                     "a creative approving an estimate")
    conftest.refused(conftest.staff(creative, job_id, target), "a creative staffing a crew")
    conftest.refused(conftest.add_right(editor, job_id), "an editor recording rights")
    conftest.refused(conftest.grant(editor, target, conftest.KAGEROU),
                     "an editor granting a clearance")
    current = conftest.read_credits(editor, campaign_id)
    for client, who in ((creative, "a creative"), (legal, "a legal user")):
        conftest.refused(conftest.save_credits(client, campaign_id, current.get("revision"), []),
                         f"{who} editing credits")
    for client, who in ((account_director, "an account director"), (producer, "a producer"),
                        (legal, "a legal user"), (creative, "a creative")):
        conftest.refused(conftest.publish(client, campaign_id), f"{who} publishing a campaign")
    assert conftest.rows(producer.get("/rate-cards").json()) == cards_before, (
        "a refused rate card must leave the cards unchanged")
    job = conftest.ok(legal.get(f"/jobs/{job_id}"), "re-reading the job")
    assert job.get("legal_hold") in (False, None), f"a refused hold must leave none: {job}"
    detail = conftest.ok(producer.get(f"/people/{conftest.ident(target)}"), "re-reading the person")
    assert not detail.get("clearances"), f"refused grants must add no clearance: {detail}"
    assert not detail.get("assignments"), f"refused staffing must add no assignment: {detail}"
    rights = conftest.rows(conftest.ok(legal.get(f"/jobs/{job_id}/rights"), "listing rights"))
    assert len(rights) == 1, f"refused rights must add nothing to legal's one right: {rights}"
    after = conftest.read_credits(editor, campaign_id)
    assert after.get("revision") == current.get("revision"), (
        f"refused credit edits must leave the revision unchanged: {after}")
    campaign = conftest.campaign_by_slug(editor, made["slug"])
    assert campaign.get("state") == "draft", f"refused publishes must leave a draft: {campaign}"


def test_each_role_completes_the_writes_its_desk_owns(account_director, producer, legal, editor,
                                                      creative, anon):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    job_id = made["job_id"]
    campaign_id = made["campaign_id"]
    other = conftest.make_person(producer)
    clearance = conftest.ok(conftest.grant(account_director, other, conftest.KAGEROU),
                            "granting a clearance on an owned account")
    revoked = conftest.ok(account_director.post(f"/clearances/{conftest.ident(clearance)}/revoke",
                                                json={"revoked_on": "2031-03-01"}),
                          "revoking a clearance on an owned account")
    assert revoked.get("revoked_on") == "2031-03-01", f"the revocation date is kept: {revoked}"
    version = conftest.ok(conftest.upload_version(creative, job_id, conftest.probe_bytes()),
                          "uploading a version as the creative")
    number = version.get("number")
    reviewed = conftest.ok(account_director.post(
        f"/jobs/{job_id}/versions/{number}/client-review", json={"status": "approved"}),
        "recording the client's approval as the account director")
    assert reviewed.get("client_status") == "approved", f"client approval recorded: {reviewed}"
    conftest.ok(producer.delete(f"/jobs/{job_id}/versions/{number}"),
                "withdrawing a version not under hold as the producer")
    assignment = conftest.rows(conftest.ok(producer.get(f"/jobs/{job_id}/assignments"),
                                           "listing assignments"))[0]
    ended = conftest.ok(producer.post(f"/assignments/{conftest.ident(assignment)}/end",
                                      json={"ends_on": "2031-01-20"}),
                        "ending an assignment as the producer")
    assert ended.get("ends_on") == "2031-01-20", f"the assignment end date is kept: {ended}"
    renamed = f"Probe Campaign Renamed {conftest.unique_token()}"
    translation = conftest.ok(editor.put(f"/campaigns/{campaign_id}/translations/en", json={
        "title": renamed, "description": "Edited by the editor.", "status": "published"}),
        "editing a translation as the editor")
    assert translation.get("title") == renamed, f"the edited title is kept: {translation}"
    hero = conftest.ok(editor.post(f"/campaigns/{campaign_id}/hero",
                                   files={"file": ("hero.png", conftest.probe_bytes(), "image/png")},
                                   data={"alt_en": "A probe still", "alt_ja": "検証の静止画"}),
                       "uploading hero media as the editor")
    assert hero.get("object_key"), f"the hero lands in the store: {hero}"
    link = conftest.ok(editor.post(f"/campaigns/{campaign_id}/preview-links",
                                   json={"expires_in_minutes": 30}), "creating a preview link")
    token = str(link.get("token"))
    assert anon.get(f"/preview/{token}").status_code == 200, "a live preview link must serve"
    conftest.ok(editor.post(f"/preview-links/{token}/revoke"), "revoking the preview link")
    assert anon.get(f"/preview/{token}").status_code == 404, "a revoked preview link is not found"
    conftest.ok(conftest.publish(editor, campaign_id), "publishing as the editor")
    assert anon.get(f"/public/campaigns/{made['slug']}").status_code == 200
    conftest.ok(editor.post(f"/campaigns/{campaign_id}/unpublish"), "unpublishing as the editor")
    assert anon.get(f"/public/campaigns/{made['slug']}").status_code == 404, (
        "an unpublished campaign must leave the public site")


def test_seeded_accounts_are_owned_by_their_account_directors(account_director,
                                                              account_director2):
    for client in (account_director, account_director2):
        person = conftest.person_id_of(client)
        email = conftest.me(client).get("email")
        accounts = conftest.rows(conftest.ok(client.get("/accounts"), "listing accounts"))
        owned = sorted(str(a.get("slug")) for a in accounts
                       if str(a.get("owner_person_id")) == str(person))
        assert owned == sorted(conftest.OWNED_ACCOUNTS[email]), (
            f"{email} must own exactly {conftest.OWNED_ACCOUNTS[email]}: {accounts}")


def test_returning_person_is_active_again_without_restored_clearances(account_director,
                                                                      producer):
    person = conftest.make_person(producer)
    pid = conftest.ident(person)
    conftest.ok(conftest.grant(account_director, person, conftest.KAGEROU), "granting")
    conftest.ok(producer.post(f"/people/{pid}/depart", json={"departed_on": "2031-02-01"}),
                "recording a departure")
    back = conftest.ok(producer.post(f"/people/{pid}/return", json={"returned_on": "2031-06-01"}),
                       "recording a return")
    assert back.get("status") == "active", f"a returned person is active: {back}"
    assert int(back.get("capacity_minutes") or 0) == conftest.RETURNED_CAPACITY, (
        f"a returned person gets the weekly capacity back: {back}")
    detail = conftest.ok(producer.get(f"/people/{pid}"), "reading the returned person")
    assert all(c.get("revoked_on") for c in detail.get("clearances") or []), (
        f"clearances are never restored automatically: {detail.get('clearances')}")
    job_id = conftest.ident(conftest.make_job(account_director, producer))
    conftest.refused(conftest.staff(producer, job_id, person),
                     "staffing a returned person before a fresh clearance")
    conftest.ok(conftest.grant(account_director, person, conftest.KAGEROU), "a fresh clearance")
    conftest.ok(conftest.staff(producer, job_id, person), "staffing the returned person")


def test_immediate_publish_during_an_embargo_names_the_embargo_reason(account_director, producer,
                                                                     legal, editor, anon):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    scheduled = conftest.ok(conftest.publish(editor, made["campaign_id"],
                                             embargo_at="2099-06-01T09:00:00+09:00"),
                            "scheduling the campaign behind an embargo")
    assert scheduled.get("state") == "scheduled", f"a future embargo schedules: {scheduled}"
    response = conftest.publish(editor, made["campaign_id"])
    conftest.refused(response, "publishing immediately while the embargo is ahead")
    assert conftest.REASON_EMBARGO in conftest.reasons_of(response), (
        "the refusal must name embargo: " + conftest.describe(response))
    campaign = conftest.campaign_by_slug(editor, made["slug"])
    assert campaign.get("state") == "scheduled", f"the refusal changes nothing: {campaign}"
    assert anon.get(f"/public/campaigns/{made['slug']}").status_code == 404


def test_public_lists_run_newest_first(anon, editor):
    years = [int(r.get("year") or 0) for r in conftest.rows(conftest.public_index(anon, page=1))]
    assert years == sorted(years, reverse=True), f"the work index runs newest first: {years}"
    news = conftest.ok(anon.get("/public/news", params={"page": 1}), "reading the newsroom")
    dates = [str(r.get("date")) for r in conftest.rows(news)]
    assert dates == sorted(dates, reverse=True), f"the newsroom runs newest first: {dates}"
    for route in ("/work/probe-order-a/", "/work/probe-order-b/"):
        conftest.ok(anon.post("/page-views", json={"route": route}), "recording a page view")
        conftest.settle()
    log = conftest.rows(conftest.ok(editor.get("/page-views"), "reading the page-view log"))
    moments = [str(r.get("viewed_at")) for r in log]
    assert moments == sorted(moments, reverse=True), f"the log runs newest first: {moments[:5]}"
    assert str(log[0].get("route")) == "/work/probe-order-b/", f"the latest view is first: {log[:2]}"
    empty = conftest.ok(anon.get("/public/news", params={"category": "stories", "year": 2019}),
                        "filtering news to stories in 2019")
    assert int(empty.get("total") or 0) == 0, f"no stories article is dated 2019: {empty}"


def test_award_entry_moves_from_submitted_to_shortlisted_to_closed(editor, anon):
    bodies = conftest.rows(conftest.ok(editor.get("/award-bodies"), "listing award bodies"))
    north = conftest.find_by(bodies, "slug", conftest.NORTH_STAR)
    ranks = [str(r.get("name")) for r in sorted(north.get("ranks") or [],
                                                key=lambda r: int(r.get("ordinal") or 0))]
    assert sorted(ranks) == sorted(conftest.NORTH_STAR_RANKS), (
        f"North Star Awards awards Gold, Silver, Bronze and Merit: {ranks}")
    campaign = conftest.campaign_by_slug(editor, conftest.BLUE_HOUR_RAIL)
    token = conftest.unique_token()
    category = conftest.ok(editor.post(f"/award-bodies/{conftest.NORTH_STAR}/categories", json={
        "section": "Probe", "name": f"Shortlist {token}"}), "adding a category")
    before = conftest.tally(anon, conftest.NORTH_STAR, 2035)
    entry = conftest.ok(editor.post("/award-entries", json={
        "campaign_id": conftest.ident(campaign), "body": conftest.NORTH_STAR,
        "category_id": conftest.ident(category), "year": 2035, "fee_minor": 1000,
        "client_permission_ref": f"PERM-{token}"}), "entering the campaign")
    assert entry.get("status") == conftest.SUBMITTED, f"a new entry is submitted: {entry}"
    result = conftest.ok(editor.post(f"/award-entries/{conftest.ident(entry)}/results",
                                     json={"rank": "Merit", "confirmed": False}),
                         "recording an unconfirmed result")
    assert result.get("entry_status") == conftest.SHORTLISTED, (
        f"an unconfirmed result shortlists the entry: {result}")
    during = conftest.tally(anon, conftest.NORTH_STAR, 2035)
    assert int(during.get("total") or 0) == int(before.get("total") or 0), (
        f"a shortlist is never shown as a win: {before} -> {during}")
    confirmed = conftest.ok(editor.post(f"/award-results/{conftest.ident(result)}/confirm"),
                            "confirming the result")
    assert confirmed.get("entry_status") == conftest.CLOSED, (
        f"confirming a result closes the entry: {confirmed}")
    after = conftest.tally(anon, conftest.NORTH_STAR, 2035)
    assert int(after.get("total") or 0) == int(before.get("total") or 0) + 1, (
        f"the confirmed result reaches the tally: {before} -> {after}")


def test_seeded_campaign_records_match_the_brief(editor, producer, legal, account_director, anon):
    harbour = conftest.campaign_by_slug(editor, conftest.HARBOUR_LIGHTS)
    job_id = str(harbour.get("job_id"))
    job = conftest.ok(legal.get(f"/jobs/{job_id}"), "reading the Harbour Lights job")
    assert conftest.MINATO in conftest.flat(job.get("accounts")), (
        f"Harbour Lights sits on its own minato-rail job: {job}")
    assert job.get("rate_card_version") == conftest.CURRENT_CARD, f"pinned card: {job}"
    rights = conftest.rows(conftest.ok(legal.get(f"/jobs/{job_id}/rights"), "listing rights"))
    assert any(r.get("status") == "cleared" and r.get("right") == "music" for r in rights), (
        f"Harbour Lights carries a cleared music right: {rights}")
    credits = conftest.read_credits(editor, conftest.ident(harbour))
    entries = credits.get("entries") or []
    assert len(entries) == 1 and entries[0].get("role_en") == conftest.HARBOUR_CREDIT_ROLE, (
        f"Harbour Lights holds one Producer entry: {entries}")
    assert conftest.HARBOUR_CREDIT_PERSON.lower() in conftest.flat(entries[0].get("people")), (
        f"the Harbour Lights entry credits Kenji Mori: {entries}")
    night = conftest.campaign_by_slug(editor, conftest.NIGHT_SIGNAL)
    listed = conftest.read_credits(editor, conftest.ident(night)).get("entries") or []
    for (role, name), entry in zip(conftest.NIGHT_SIGNAL_LEADS, listed):
        assert entry.get("role_en") == role and name.lower() in conftest.flat(entry.get("people")), (
            f"the Night Signal list opens {role} {name}: {entry}")
    active = 0
    credited = {str(p.get("person_id")) for e in listed for p in e.get("people") or []}
    for person_id in sorted(credited):
        detail = conftest.ok(producer.get(f"/people/{person_id}"), "reading a credited person")
        if detail.get("status") == "active":
            active += 1
            held = [str(c.get("account")) for c in detail.get("clearances") or []
                    if not c.get("revoked_on")]
            assert conftest.KAGEROU in held, f"{detail.get('name_en')} holds kagerou: {held}"
    assert active == conftest.NIGHT_SIGNAL_ACTIVE_CREDITED, (
        f"thirteen active people are credited on Night Signal, found {active}")
    brief = conftest.open_brief(account_director)
    conftest.approved_estimate(account_director, producer, brief)
    converted = conftest.ok(conftest.convert(account_director, brief,
                                             conftest.person_id_of(producer),
                                             ((conftest.KAGEROU, conftest.APPORTIONMENT_WHOLE),)),
                            "converting the brief")
    new_job = conftest.ok(producer.get(f"/jobs/{conftest.ident(converted)}"), "reading the new job")
    assert new_job.get("status") == conftest.JOB_OPEN, f"a new job is open: {new_job}"
    briefs = conftest.rows(conftest.ok(account_director.get("/briefs"), "listing briefs"))
    mine = conftest.find_by(briefs, "id", conftest.ident(brief))
    assert mine and mine.get("status") == conftest.BRIEF_CONVERTED, (
        f"a converted brief reads converted: {mine}")


def test_japanese_copy_uses_the_named_face(page, app_url):
    page.goto(f"{app_url}/", wait_until="networkidle")
    family = str(page.evaluate("() => getComputedStyle(document.body).fontFamily")).lower()
    assert conftest.JAPANESE_FACE in family.replace(" ", "").replace("'", "").replace('"', ""), (
        f"the Japanese root must set its copy in the notosansjp face: {family}")


def test_draft_campaign_address_is_not_found(account_director, producer, legal, editor, anon,
                                             site):
    made = conftest.make_campaign(account_director, producer, legal, editor)
    for locale in ("ja", "en"):
        response = anon.get(f"/public/campaigns/{made['slug']}", params={"locale": locale})
        assert response.status_code == 404, (
            f"a draft campaign must be not-found in {locale}: " + conftest.describe(response))
    for prefix in ("", "/en"):
        page = site.get(f"{prefix}/work/{made['slug']}/")
        assert page.status_code == 404, (
            f"the draft campaign's page {prefix}/work/ must answer 404: " + conftest.describe(page))
    assert made["slug"] not in conftest.all_public_slugs(anon), "a draft must stay out of the index"

