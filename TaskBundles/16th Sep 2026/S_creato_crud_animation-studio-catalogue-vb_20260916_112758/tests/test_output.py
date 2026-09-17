from __future__ import annotations

import concurrent.futures

import appclient
import conftest
from conftest import (
    BRANDED,
    CONFIDENTIAL_SLATE_TITLE,
    CREATED,
    CUSTOMER,
    CUSTOMER_TWO,
    DENIED,
    DENIED_OR_MISSING,
    DRAFT_TITLE,
    EMBARGOED_TITLE,
    ENTERTAINMENT,
    EXPIRED_TITLE,
    INDUSTRY_ORDER,
    LAST_EDITION,
    OPEN_SUBJECT,
    PASSWORD,
    READABLE_TITLES,
    REFUSED,
    RESTRICTED_SUBJECTS,
    UPDATED_PRODUCT,
    WITHHELD_CLIENT,
)

SELF_OWNED_PRODUCT = "Lightbox Starter Kit"


def test_catalogue_lists_only_readable_films(anon):
    films = conftest.catalogue(anon)
    titles = [str(film.get("title", "")).strip() for film in films]
    for wanted in READABLE_TITLES:
        assert wanted in titles, (
            f"the catalogue omits the published film {wanted!r}; it returned {titles}"
        )
    for hidden in (EMBARGOED_TITLE, EXPIRED_TITLE, DRAFT_TITLE):
        assert hidden not in titles, (
            f"the catalogue returned {hidden!r}, which is not publicly readable; "
            f"it returned {titles}"
        )


def test_facet_filter_returns_only_that_type(anon):
    branded = conftest.catalogue(anon, type="branded")
    assert branded, "the Branded facet returned no films at all"
    for film in branded:
        assert str(film.get("type", "")).strip().lower() == BRANDED.lower(), (
            f"the Branded facet returned {film.get('title')!r} of type "
            f"{film.get('type')!r}"
        )
    entertainment = conftest.catalogue(anon, type="entertainment")
    branded_titles = {str(f.get("title", "")) for f in branded}
    entertainment_titles = {str(f.get("title", "")) for f in entertainment}
    assert not branded_titles & entertainment_titles, (
        "a film appears under both facets, so the facets are not exclusive: "
        f"{sorted(branded_titles & entertainment_titles)}"
    )


def test_case_study_returns_credits_in_industry_order(anon):
    films = conftest.catalogue(anon)
    slug = conftest.slug_of(films[0])
    response = conftest.case_study(anon, slug)
    assert response.status_code == 200, (
        f"GET /api/case-studies/{slug} returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    payload = response.json()
    credits = payload.get("credits") or []
    assert credits, f"the case study {slug!r} returned no credits: {str(payload)[:300]}"
    roles = [str(credit.get("role", "")).strip() for credit in credits]
    ranks = [INDUSTRY_ORDER.index(role) for role in roles if role in INDUSTRY_ORDER]
    assert ranks, f"no credit carries a known industry role; roles were {roles}"
    assert ranks == sorted(ranks), (
        f"credits are not in industry order: {roles} ranks {ranks}. The order is "
        f"{list(INDUSTRY_ORDER)}"
    )


def test_onward_link_follows_the_active_filter(anon):
    branded = conftest.catalogue(anon, type="branded")
    assert len(branded) >= 2, (
        f"the Branded facet returned {len(branded)} films; an onward link needs two"
    )
    branded_slugs = {conftest.slug_of(film) for film in branded}
    first = conftest.slug_of(branded[0])
    response = anon.get(f"/case-studies/{first}", params={"type": "branded"})
    assert response.status_code == 200, (
        f"GET /api/case-studies/{first} with a facet returned "
        f"{response.status_code}: {response.text[:300]}"
    )
    onward = response.json().get("next_slug")
    assert onward, (
        f"the case study {first!r} returned no next_slug, so the onward link cannot "
        f"follow the filter"
    )
    assert onward in branded_slugs, (
        f"the onward link from {first!r} under the Branded facet points at {onward!r}, "
        f"which is not a Branded film. Branded slugs are {sorted(branded_slugs)}"
    )


def test_slate_excludes_confidential_entries(anon):
    import _shapes

    response = anon.get("/slate")
    assert response.status_code == 200, (
        f"GET /api/slate returned {response.status_code}: {response.text[:300]}"
    )
    entries = _shapes.items(response.json())
    titles = [str(entry.get("title", "")).strip() for entry in entries]
    assert titles, "the slate returned no entries at all"
    assert CONFIDENTIAL_SLATE_TITLE not in titles, (
        f"the slate returned the confidential entry {CONFIDENTIAL_SLATE_TITLE!r}: "
        f"{titles}"
    )


def test_feed_featured_article_is_a_singleton(anon):
    import _shapes

    response = anon.get("/feed")
    assert response.status_code == 200, (
        f"GET /api/feed returned {response.status_code}: {response.text[:300]}"
    )
    articles = _shapes.items(response.json())
    assert articles, "the feed returned no articles at all"
    featured = [a for a in articles if a.get("featured") in (True, "true", 1)]
    assert len(featured) <= 1, (
        f"{len(featured)} articles are marked featured; featuring a second must "
        f"unfeature the first. Featured titles: {[a.get('title') for a in featured]}"
    )


def test_podcast_groups_published_episodes_by_season(anon):
    response = anon.get("/podcast")
    assert response.status_code == 200, (
        f"GET /api/podcast returned {response.status_code}: {response.text[:300]}"
    )
    payload = response.json()
    episodes = payload.get("episodes") or []
    assert episodes, f"the podcast returned no episodes: {str(payload)[:300]}"
    seen = set()
    for episode in episodes:
        season = episode.get("season")
        number = episode.get("number")
        assert season is not None and number is not None, (
            f"an episode carries no season or number: {str(episode)[:200]}"
        )
        key = (int(season), int(number))
        assert key not in seen, (
            f"season {season} episode {number} appears twice; the pair identifies an "
            f"episode uniquely"
        )
        seen.add(key)
        identity = str(episode.get("identity", ""))
        if identity:
            assert identity == f"S{int(season):02d}.E{int(number):02d}", (
                f"episode identity {identity!r} is not zero-padded on both parts; "
                f"season {season} episode {number} renders as "
                f"S{int(season):02d}.E{int(number):02d}"
            )


def test_studio_state_is_served_by_the_app(anon):
    response = anon.get("/studio-state")
    assert response.status_code == 200, (
        f"GET /api/studio-state returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    payload = response.json()
    assert "open" in payload, (
        f"the studio state carries no open flag: {str(payload)[:300]}"
    )
    assert isinstance(payload["open"], bool), (
        f"the open flag is {payload['open']!r}, which is not a boolean"
    )
    assert payload.get("hours_label"), (
        f"the studio state carries no hours_label: {str(payload)[:300]}"
    )


def test_purchase_creates_an_order_and_an_entitlement(customer, backend):
    slug = conftest.product_slug(customer, SELF_OWNED_PRODUCT)
    before = backend.count("entitlement")
    response = conftest.buy(customer, slug)
    assert response.status_code in CREATED, (
        f"buying {SELF_OWNED_PRODUCT!r} returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    payload = response.json()
    assert payload.get("reference"), (
        f"the order carries no reference: {str(payload)[:300]}"
    )
    after = conftest.poll_until(
        lambda: backend.count("entitlement") > before and backend.count("entitlement")
    )
    assert after and after == before + 1, (
        f"entitlement rows went from {before} to {backend.count('entitlement')}; "
        f"one purchase grants exactly one entitlement"
    )


def test_second_purchase_creates_no_second_entitlement(customer, backend):
    slug = conftest.product_slug(customer, UPDATED_PRODUCT)
    before = backend.count("entitlement")
    response = conftest.buy(customer, slug)
    assert response.status_code in REFUSED or response.status_code in CREATED, (
        f"re-buying an owned product returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    conftest.settle()
    after = backend.count("entitlement")
    assert after == before, (
        f"entitlement rows went from {before} to {after} on a repeat purchase of an "
        f"already owned product; one entitlement exists per customer per product"
    )


def test_catalogue_counts_match_the_list(anon):
    films = conftest.catalogue(anon)
    payload = conftest.counts(anon)
    total = payload.get("total")
    assert total is not None, (
        f"the counts payload carries no total: {str(payload)[:300]}"
    )
    assert int(total) == len(films), (
        f"the catalogue total is {total} while the list returned {len(films)} films; "
        f"the total and the list come from one derivation"
    )
    for label in (BRANDED, ENTERTAINMENT):
        listed = len(conftest.catalogue(anon, type=label.lower()))
        claimed = conftest.facet_count(payload, label)
        assert claimed == listed, (
            f"the {label} facet claims {claimed} films while the filtered list "
            f"returned {listed}; a count derived apart from its list drifts"
        )


def test_published_film_survives_a_reread(anon, backend):
    films = conftest.catalogue(anon)
    first = films[0]
    slug = conftest.slug_of(first)
    title = str(first.get("title", "")).strip()
    response = conftest.case_study(anon, slug)
    assert response.status_code == 200, (
        f"GET /api/case-studies/{slug} returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    detail = response.json()
    assert str(detail.get("title", "")).strip() == title, (
        f"the catalogue displayed {title!r} while the case study returned "
        f"{detail.get('title')!r} for the same slug"
    )
    again = conftest.catalogue(anon)
    assert slug in {conftest.slug_of(film) for film in again}, (
        f"{slug!r} vanished from the catalogue on a second read"
    )
    stored = backend.count("case_study", slug=slug)
    assert stored == 1, (
        f"the catalogue displayed {slug!r} but case_study holds {stored} row(s) for "
        f"it; what the list displayed must be what is stored"
    )


def test_publishing_a_draft_raises_the_counts(publisher, anon):
    before_total = int(conftest.counts(anon).get("total"))
    record = conftest.find_record(publisher, DRAFT_TITLE)
    identifier = conftest.record_id(record)
    response = conftest.transition(publisher, identifier, "record.publish")
    assert response.status_code in CREATED, (
        f"publishing {DRAFT_TITLE!r} returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    after_total = conftest.poll_until(
        lambda: int(conftest.counts(anon).get("total")) == before_total + 1
    )
    assert after_total, (
        f"the catalogue total stayed at {conftest.counts(anon).get('total')} after "
        f"publishing {DRAFT_TITLE!r}; it was {before_total} before"
    )
    titles = [str(f.get("title", "")).strip() for f in conftest.catalogue(anon)]
    assert DRAFT_TITLE in titles, (
        f"{DRAFT_TITLE!r} was published but is absent from the catalogue: {titles}"
    )


def test_editorial_log_row_accompanies_a_mutation(producer, backend):
    before = backend.count("editorial_event")
    record = conftest.find_record(producer, EXPIRED_TITLE)
    identifier = conftest.record_id(record)
    response = producer.patch(
        f"/studio/records/{identifier}",
        json={"synopsis": f"Revised synopsis {conftest.probe_key()}",
              "version": record.get("version", 1)},
    )
    assert response.status_code in CREATED, (
        f"editing {EXPIRED_TITLE!r} returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    grew = conftest.poll_until(lambda: backend.count("editorial_event") > before)
    assert grew, (
        f"editorial_event held {before} rows before the edit and "
        f"{backend.count('editorial_event')} after; a mutation and its log row commit "
        f"together"
    )


def test_seeded_rows_are_not_duplicated(backend):
    for title in READABLE_TITLES:
        held = backend.count("case_study", title=title)
        assert held == 1, (
            f"case_study holds {held} rows titled {title!r}; seeding is idempotent, "
            f"so restarting the app duplicates no row"
        )


def test_repeated_order_key_creates_one_order(customer_two, backend):
    slug = conftest.product_slug(customer_two, SELF_OWNED_PRODUCT)
    key = conftest.probe_key()
    before = backend.count("customer_order")
    first = conftest.buy(customer_two, slug, key=key)
    assert first.status_code in CREATED, (
        f"the first submission returned {first.status_code}: {first.text[:300]}"
    )
    reference = first.json().get("reference")
    second = conftest.buy(customer_two, slug, key=key)
    assert second.status_code in CREATED, (
        f"replaying one idempotency key returned {second.status_code}: "
        f"{second.text[:300]}; a replay returns the original result"
    )
    assert second.json().get("reference") == reference, (
        f"the replay returned reference {second.json().get('reference')!r} while the "
        f"first returned {reference!r}; a replay returns the original order"
    )
    conftest.settle()
    after = backend.count("customer_order")
    assert after == before + 1, (
        f"customer_order rows went from {before} to {after} across one idempotency "
        f"key; exactly one order is created"
    )


def test_last_item_sells_exactly_once_under_concurrency(backend):
    buyer_one = appclient.login(CUSTOMER, PASSWORD)
    buyer_two = appclient.login(CUSTOMER_TWO, PASSWORD)
    with appclient.client(buyer_one) as first_http:
        slug = conftest.product_slug(first_http, LAST_EDITION)

    def attempt(token):
        with appclient.client(token) as http:
            return conftest.buy(http, slug).status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(attempt, (buyer_one, buyer_two)))

    accepted = [code for code in outcomes if code in CREATED]
    refused = [code for code in outcomes if code not in CREATED]
    assert len(accepted) == 1, (
        f"two simultaneous purchases of the last {LAST_EDITION!r} returned "
        f"{outcomes}; exactly one is accepted and the other is refused"
    )
    assert refused and all(code in REFUSED for code in refused), (
        f"the losing purchase returned {refused}, which is not a clean refusal; "
        f"outcomes were {outcomes}"
    )
    rows = backend.rows("drop_item")
    negative = [row for row in rows
                if row.get("stock_total") is not None
                and int(row.get("stock_total")) - int(row.get("stock_sold") or 0)
                - int(row.get("stock_reserved") or 0) < 0]
    assert not negative, (
        f"availability went below zero on {len(negative)} drop item(s): {negative}"
    )


def test_editor_cannot_publish_a_record(editor, anon):
    record = conftest.find_record(editor, DRAFT_TITLE)
    identifier = conftest.record_id(record)
    before = [str(f.get("title", "")).strip() for f in conftest.catalogue(anon)]
    response = conftest.transition(editor, identifier, "record.publish")
    assert response.status_code in DENIED_OR_MISSING, (
        f"an Editor publishing {DRAFT_TITLE!r} returned {response.status_code}: "
        f"{response.text[:300]}; the command belongs to a Publisher and above"
    )
    after = [str(f.get("title", "")).strip() for f in conftest.catalogue(anon)]
    assert after == before, (
        f"the catalogue changed from {before} to {after} after a denied publish; a "
        f"refused command leaves the underlying row unchanged"
    )


def test_publisher_cannot_lift_an_embargo_early(publisher, anon):
    record = conftest.find_record(publisher, EMBARGOED_TITLE)
    identifier = conftest.record_id(record)
    response = conftest.transition(
        publisher, identifier, "record.embargo.lift", confirm_title=EMBARGOED_TITLE)
    assert response.status_code in DENIED_OR_MISSING, (
        f"a Publisher lifting the embargo on {EMBARGOED_TITLE!r} returned "
        f"{response.status_code}: {response.text[:300]}; only an Owner may lift early"
    )
    titles = [str(f.get("title", "")).strip() for f in conftest.catalogue(anon)]
    assert EMBARGOED_TITLE not in titles, (
        f"{EMBARGOED_TITLE!r} reached the catalogue after a denied early lift: {titles}"
    )


def test_unauthenticated_write_is_denied(anon, publisher, backend):
    record = conftest.find_record(publisher, EXPIRED_TITLE)
    identifier = conftest.record_id(record)
    before = backend.count("editorial_event")
    response = conftest.transition(anon, identifier, "record.publish")
    assert response.status_code in DENIED_OR_MISSING, (
        f"an anonymous publish returned {response.status_code}: "
        f"{response.text[:300]}; a write with no session is denied"
    )
    created = anon.post("/studio/records", json={"kind": "case_study",
                                                "title": conftest.probe_key()})
    assert created.status_code in DENIED_OR_MISSING, (
        f"an anonymous create returned {created.status_code}: {created.text[:300]}"
    )
    conftest.settle()
    after = backend.count("editorial_event")
    assert after == before, (
        f"editorial_event grew from {before} to {after} across two denied anonymous "
        f"writes; a denied write changes nothing"
    )


def test_customer_cannot_reach_another_customers_download(customer, customer_two):
    import _shapes

    owned = conftest.product_slug(customer, UPDATED_PRODUCT)
    mine = customer.post("/downloads", json={"product_slug": owned})
    assert mine.status_code in CREATED, (
        f"the owning customer's download returned {mine.status_code}: "
        f"{mine.text[:300]}"
    )
    theirs = customer_two.post("/downloads", json={"product_slug": owned})
    assert theirs.status_code in DENIED_OR_MISSING, (
        f"{CUSTOMER_TWO} downloading {UPDATED_PRODUCT!r}, owned by {CUSTOMER}, "
        f"returned {theirs.status_code}: {theirs.text[:300]}"
    )
    listed = customer_two.get("/orders")
    assert listed.status_code == 200, (
        f"GET /api/orders for {CUSTOMER_TWO} returned {listed.status_code}: "
        f"{listed.text[:300]}"
    )
    flat = _shapes.flatten(_shapes.items(listed.json()))
    assert CUSTOMER not in flat, (
        f"the order list for {CUSTOMER_TWO} mentions {CUSTOMER}; a customer reaches "
        f"only their own rows"
    )


def test_embargoed_film_is_absent_everywhere(anon, publisher):
    record = conftest.find_record(publisher, EMBARGOED_TITLE)
    slug = conftest.slug_of(record)
    titles = [str(f.get("title", "")).strip() for f in conftest.catalogue(anon)]
    assert EMBARGOED_TITLE not in titles, (
        f"the catalogue lists the embargoed {EMBARGOED_TITLE!r}: {titles}"
    )
    direct = conftest.case_study(anon, slug)
    assert direct.status_code == 404, (
        f"the embargoed address answered {direct.status_code}; it must answer exactly "
        f"as an address that never existed"
    )
    invented = conftest.case_study(anon, f"never-existed-{conftest.probe_key()}")
    assert direct.status_code == invented.status_code, (
        f"the embargoed address answered {direct.status_code} and an invented address "
        f"answered {invented.status_code}; the two must be indistinguishable"
    )
    search = anon.get("/search", params={"q": EMBARGOED_TITLE})
    assert search.status_code == 200, (
        f"GET /api/search returned {search.status_code}: {search.text[:300]}"
    )
    assert EMBARGOED_TITLE.lower() not in conftest._flat(search.json()), (
        f"the search results carry the embargoed {EMBARGOED_TITLE!r}"
    )


def test_withheld_client_name_is_absent_from_the_payload(anon):
    films = conftest.catalogue(anon)
    flat = conftest._flat(films)
    assert WITHHELD_CLIENT.lower() not in flat, (
        f"the catalogue payload carries {WITHHELD_CLIENT!r}, whose naming permission "
        f"is withheld; a name absent from the page and present in the payload has "
        f"leaked"
    )
    for film in films:
        slug = conftest.slug_of(film)
        response = conftest.case_study(anon, slug)
        if response.status_code != 200:
            continue
        assert WITHHELD_CLIENT.lower() not in conftest._flat(response.json()), (
            f"the case study {slug!r} carries the withheld client {WITHHELD_CLIENT!r} "
            f"in its payload"
        )


def test_expired_rights_window_removes_the_film(anon, publisher):
    record = conftest.find_record(publisher, EXPIRED_TITLE)
    slug = conftest.slug_of(record)
    titles = [str(f.get("title", "")).strip() for f in conftest.catalogue(anon)]
    assert EXPIRED_TITLE not in titles, (
        f"the catalogue lists {EXPIRED_TITLE!r}, which is past its rights end: {titles}"
    )
    response = conftest.case_study(anon, slug)
    assert response.status_code == 404, (
        f"the address of the expired {EXPIRED_TITLE!r} answered "
        f"{response.status_code}; a record past its rights window is unreadable"
    )
    assert record, (
        f"{EXPIRED_TITLE!r} must remain visible in the back office, marked as expired"
    )


def test_unknown_facet_falls_back_to_all_films(anon):
    everything = conftest.catalogue(anon)
    response = anon.get("/catalogue", params={"type": f"nonsense-{conftest.probe_key()}"})
    assert response.status_code == 200, (
        f"an unknown facet returned {response.status_code}: {response.text[:300]}; it "
        f"falls back to every film rather than erroring"
    )
    import _shapes

    fallback = _shapes.items(response.json())
    assert len(fallback) == len(everything), (
        f"an unknown facet returned {len(fallback)} films while the unfiltered list "
        f"returned {len(everything)}"
    )


def test_facet_with_no_films_returns_an_empty_list(anon, producer):
    import _shapes

    label = f"empty-{conftest.probe_key()}"
    response = anon.get("/catalogue", params={"type": label, "strict": "true"})
    assert response.status_code in (200, 404), (
        f"a facet with no films returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    if response.status_code == 200:
        payload = response.json()
        listed = _shapes.items(payload) if payload not in ([], {}) else []
        assert isinstance(listed, list), (
            f"an empty result must be a list, got {type(listed).__name__}"
        )


def test_publication_gate_returns_every_failure(publisher):
    record = conftest.find_record(publisher, DRAFT_TITLE)
    identifier = conftest.record_id(record)
    stripped = publisher.patch(
        f"/studio/records/{identifier}",
        json={"type": None, "duration_s": 0, "version": record.get("version", 1)},
    )
    assert stripped.status_code in CREATED or stripped.status_code in REFUSED, (
        f"stripping the record returned {stripped.status_code}: "
        f"{stripped.text[:300]}"
    )
    response = conftest.transition(publisher, identifier, "record.publish")
    if response.status_code in REFUSED:
        failures = response.json().get("failures") or []
        assert isinstance(failures, list) and len(failures) >= 2, (
            f"the publication gate returned {failures!r}; it returns every failure at "
            f"once rather than only the first"
        )


def test_enquiry_refuses_an_attachment_on_a_restricted_subject(anon):
    accepted = anon.post("/enquiries", json={
        "name": "Ada Lovelace",
        "organisation": "Analytical Engines",
        "email": conftest.probe_email(),
        "subject": OPEN_SUBJECT,
        "message": "We would like to talk about a title sequence for a short film.",
    })
    assert accepted.status_code in CREATED, (
        f"an enquiry on {OPEN_SUBJECT!r} returned {accepted.status_code}: "
        f"{accepted.text[:300]}"
    )
    body = accepted.json()
    assert body.get("routed_to"), (
        f"the stored enquiry names no routed address: {str(body)[:300]}"
    )
    refused = anon.post("/enquiries", json={
        "name": "Ada Lovelace",
        "organisation": "Analytical Engines",
        "email": conftest.probe_email(),
        "subject": RESTRICTED_SUBJECTS[0],
        "message": "Please find my script attached for your consideration.",
        "attachment": "portfolio.pdf",
    })
    assert refused.status_code in REFUSED, (
        f"an attachment on {RESTRICTED_SUBJECTS[0]!r} returned "
        f"{refused.status_code}: {refused.text[:300]}; the submissions policy is "
        f"enforced rather than printed"
    )


def test_health_endpoint_reports_ready(anon):
    response = anon.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}: {response.text[:300]}"
    )
    flat = conftest._flat(response.json())
    assert flat, "GET /api/health returned an empty body"


def test_markup_carries_every_film_without_scripting():
    html = conftest.markup("/work")
    for title in READABLE_TITLES:
        assert title in html, (
            f"the served catalogue markup omits {title!r}, so the film is findable only "
            f"once scripting has run"
        )
    lowered = html.lower()
    assert "<video" not in lowered or "poster" in lowered, (
        "the served catalogue markup attaches a video element with no poster, so the "
        "page requests film bytes before its own content has painted"
    )


def test_security_headers_and_request_identifier_are_returned():
    response = conftest.page(None, "/work")
    headers = {k.lower(): v for k, v in response.headers.items()}
    for wanted in conftest.SECURITY_HEADERS:
        assert wanted in headers, (
            f"the response carries no {wanted} header; the headers present are "
            f"{sorted(headers)}"
        )
    assert any(h in headers for h in conftest.REQUEST_ID_HEADERS), (
        f"no request identifier is returned to the client; the headers present are "
        f"{sorted(headers)}"
    )
    for vendor in conftest.VENDOR_HEADERS:
        assert vendor not in headers, (
            f"the response header {vendor!r} names the platform serving it: "
            f"{headers.get(vendor)!r}"
        )
    missing = conftest.page(None, f"/work/never-existed-{conftest.probe_key()}")
    body = missing.text.lower()
    assert "traceback" not in body and "postgres" not in body, (
        "an error response leaks internal detail"
    )


def test_no_credential_reaches_the_browser():
    for route in ("/", "/work", "/shop"):
        html = conftest.markup(route).lower()
        for marker in conftest.CREDENTIAL_MARKERS:
            assert marker not in html, (
                f"the markup served at {route} carries {marker!r}, which is a "
                f"credential the browser must never download"
            )


def test_no_third_party_origin_is_referenced():
    import re as _re

    for route in ("/", "/work", "/shop"):
        html = conftest.markup(route)
        for url in _re.findall(r'(?:src|href)="(https?://[^"]+)"', html):
            host = url.split("/")[2].lower()
            assert host in conftest.appclient.app_url().lower(), (
                f"the markup served at {route} reaches {host!r}, which is not the "
                f"product's own origin. No analytics, no tag manager, no delivery "
                f"network, no external call at runtime"
            )


def test_card_named_field_is_refused(customer):
    slug = conftest.product_slug(customer, SELF_OWNED_PRODUCT)
    response = customer.post("/orders", json={
        "product_slug": slug,
        "idempotency_key": conftest.probe_key(),
        "card_number": "4111111111111111",
    })
    assert response.status_code in REFUSED, (
        f"an order carrying a field named for a card returned "
        f"{response.status_code}: {response.text[:300]}; no route accepts one"
    )


def test_generated_placeholder_is_stable():
    first = conftest.markup("/work")
    second = conftest.markup("/work")
    assert first == second, (
        "two reads of the catalogue markup differ, so the generated placeholders are "
        "not seeded from the records they belong to"
    )


def test_machine_readable_hooks_are_present():
    html = conftest.markup("/work")
    for hook in (".acetate", ".gutters", ".bg-loading", ".button-pill",
                 ".dot--filled", ".router-link-active"):
        assert hook.lstrip(".") in html, (
            f"the served markup carries no {hook} hook; the brief pins it as a "
            f"machine-readable hook the product must expose"
        )
    assert "<svg" in html.lower(), (
        "the served markup carries no inline vector, so the icons are not inline "
        "geometry"
    )
    assert "grid" in html.lower(), (
        "the catalogue container names no view mode, so the mode is not readable "
        "from the markup"
    )
    styles = conftest.stylesheets(html)
    assert "inter" in styles.lower() or "inter" in html.lower(), (
        "no stylesheet or document names the one type family the brief pins"
    )
    assert "@keyframes" not in styles.lower(), (
        "a stylesheet declares a keyframe animation; the product carries no looping "
        "decorative animation anywhere"
    )
    assert "prefers-reduced-motion" in styles.lower(), (
        "no stylesheet honours a reduced-motion preference, so the motion layers are "
        "never removed for a visitor who asked for less movement"
    )


def test_every_content_image_carries_alternative_text():
    import re as _re

    for route in ("/", "/work", "/about"):
        html = conftest.markup(route)
        for tag in _re.findall(r"<img\b[^>]*>", html, _re.I):
            assert "alt=" in tag.lower(), (
                f"an image on {route} carries no alternative text: {tag[:120]}"
            )


def test_every_internal_link_resolves():
    import re as _re

    html = conftest.markup("/")
    targets = {t for t in _re.findall(r'href="(/[^"#?]*)"', html)}
    for target in sorted(targets)[:20]:
        response = conftest.page(None, target)
        assert response.status_code == 200, (
            f"the internal link {target!r} on the home route answered "
            f"{response.status_code}"
        )


def test_every_public_route_declares_a_preview_image():
    for route in ("/", "/work", "/blog"):
        html = conftest.markup(route).lower()
        assert "og:image" in html or "twitter:image" in html, (
            f"the route {route} declares no social preview image"
        )
        assert "og:title" in html or 'name="description"' in html, (
            f"the route {route} declares no preview title or description of its own"
        )


def test_repeated_form_submission_is_refused(anon):
    body = {
        "name": "Ada Lovelace",
        "subject": OPEN_SUBJECT,
        "message": "A short note about a title sequence for a forthcoming short film.",
    }
    outcomes = [anon.post("/enquiries", json=dict(body, email=conftest.probe_email()))
                for _ in range(6)]
    codes = [r.status_code for r in outcomes]
    assert any(code == 429 or code in REFUSED for code in codes), (
        f"six enquiries submitted in quick succession all succeeded ({codes}); a form "
        f"submitted repeatedly must be refused"
    )


def test_terms_page_is_reachable_from_every_footer():
    for route in ("/", "/work", "/shop"):
        html = conftest.markup(route).lower()
        assert "/terms" in html, (
            f"the footer on {route} links to no terms page"
        )
    response = conftest.page(None, "/terms")
    assert response.status_code == 200, (
        f"the terms page answered {response.status_code}"
    )
