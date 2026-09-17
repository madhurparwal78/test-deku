from __future__ import annotations

import _shapes
import conftest


def _create_item(producer, kind, slug, title, **extra):
    body = {"kind": kind, "slug": slug, "title": title}
    body.update(extra)
    response = producer.post("/items", json=body)
    assert response.status_code in (200, 201), (
        f"creating a {kind} as the producer should succeed: "
        + conftest.describe(response))
    return response.json()


def _attach_poster(producer, ident, payload=None, alt_text="A probe poster."):
    payload = payload if payload is not None else conftest.probe_bytes()
    response = producer.post(
        f"/items/{ident}/media",
        files={"file": ("poster.png", payload, "image/png")},
        data={"role": "poster", "alt_text": alt_text,
              "width": "1600", "height": "900"})
    assert response.status_code in (200, 201), (
        "attaching a poster as the producer should succeed: "
        + conftest.describe(response))
    return payload, response.json()


def _publish(producer, ident):
    return producer.post(f"/items/{ident}/publish")


def _unpublish(producer, ident):
    return producer.post(f"/items/{ident}/unpublish")


def _ordinals(payload):
    out = []
    for row in _shapes.items(payload):
        value = row.get("ordinal")
        if value is not None:
            out.append(str(value))
    return out


def _slugs(payload):
    return [str(row.get("slug")) for row in _shapes.items(payload)]


def _names(payload):
    out = []
    for row in _shapes.items(payload):
        for key in ("title", "name"):
            if row.get(key) is not None:
                out.append(str(row[key]))
                break
    return out


def _disciplines(payload):
    out = []
    for row in _shapes.items(payload):
        if isinstance(row, dict):
            value = row.get("discipline") or row.get("name") or row.get("value")
            if value is not None:
                out.append(str(value))
    return out


def test_health_endpoint_reports_ready(anon):
    response = anon.get("/health")
    assert response.status_code == 200, (
        "GET /api/health must answer 200 once the app is ready: "
        + conftest.describe(response))


def test_published_works_are_listed_with_contiguous_ordinals(anon):
    response = anon.get("/works")
    assert response.status_code == 200, (
        "GET /api/works must be readable without signing in: "
        + conftest.describe(response))
    ordinals = _ordinals(response.json())
    assert ordinals == list(conftest.SEEDED_ORDINALS), (
        "the twelve seeded published works must carry the contiguous ordinals "
        f"{list(conftest.SEEDED_ORDINALS)} in order; the listing carried "
        f"{ordinals}: " + conftest.describe(response))
    slugs = _slugs(response.json())
    for expected in conftest.WORK_SLUGS:
        assert expected in slugs, (
            f"seeded published work {expected} is missing from the public "
            f"listing; listing carried {slugs}: " + conftest.describe(response))


def test_work_detail_returns_credits_media_and_neighbours(anon):
    response = anon.get(f"/works/{conftest.WORK_SLUGS[2]}")
    assert response.status_code == 200, (
        f"the published work {conftest.WORK_SLUGS[2]} must be readable by a "
        "signed-out reader: " + conftest.describe(response))
    body = response.json()
    flat = _shapes.flatten(body)
    assert "credit" in flat.lower(), (
        "a work detail must carry its credits as role and name pairs: "
        + conftest.describe(response))
    assert "poster" in flat.lower() or "media" in flat.lower(), (
        "a work detail must carry its media references: "
        + conftest.describe(response))
    assert "next" in flat.lower(), (
        "a work detail must name the following work by ordinal: "
        + conftest.describe(response))


def test_work_neighbours_wrap_from_last_to_first(anon):
    last = anon.get(f"/works/{conftest.WORK_SLUGS[11]}")
    assert last.status_code == 200, (
        "the twelfth published work must be readable: "
        + conftest.describe(last))
    flat = _shapes.flatten(last.json())
    assert conftest.WORK_SLUGS[0] in flat, (
        "the next link of the work showing 012 must wrap to the work showing "
        f"001 ({conftest.WORK_SLUGS[0]}): " + conftest.describe(last))


def test_published_talents_are_listed_for_a_visitor(anon):
    response = anon.get("/talents")
    assert response.status_code == 200, (
        "GET /api/talents must be readable without signing in: "
        + conftest.describe(response))
    names = _names(response.json())
    for expected in conftest.TALENT_NAMES:
        assert expected in names, (
            f"seeded published talent {expected} is missing from the roster; "
            f"the roster carried {names}: " + conftest.describe(response))


def test_talent_detail_returns_derived_credited_work(anon):
    response = anon.get(f"/talents/{conftest.TALENT_SLUGS[0]}")
    assert response.status_code == 200, (
        f"the published talent {conftest.TALENT_SLUGS[0]} must be readable: "
        + conftest.describe(response))
    flat = _shapes.flatten(response.json())
    assert any(slug in flat for slug in conftest.WORK_SLUGS), (
        "a talent detail must carry the works that talent is credited on, "
        "derived from the credits relation: " + conftest.describe(response))


def test_discipline_set_is_derived_from_published_talent(anon):
    response = anon.get("/disciplines")
    assert response.status_code == 200, (
        "GET /api/disciplines must be readable without signing in: "
        + conftest.describe(response))
    values = _disciplines(response.json())
    assert values == list(conftest.SEEDED_DISCIPLINES), (
        "the discipline set must be the distinct disciplines of published "
        f"talent in first-appearance order {list(conftest.SEEDED_DISCIPLINES)}; "
        f"the response carried {values}: " + conftest.describe(response))


def test_discipline_filter_narrows_the_roster(anon):
    response = anon.get("/talents", params={"discipline": "photographer"})
    assert response.status_code == 200, (
        "the roster must accept a discipline filter: "
        + conftest.describe(response))
    names = _names(response.json())
    assert conftest.TALENT_NAMES[2] in names, (
        f"filtering on photographer must keep {conftest.TALENT_NAMES[2]}: "
        + conftest.describe(response))
    assert conftest.TALENT_NAMES[0] not in names, (
        f"filtering on photographer must drop {conftest.TALENT_NAMES[0]}, who "
        "is a director: " + conftest.describe(response))


def test_publishing_a_new_discipline_adds_it_to_the_derived_set(producer, anon):
    slug = conftest.probe_slug("probe-stylist")
    created = _create_item(producer, "talent", slug, "Probe Stylist",
                           discipline="stylist")
    ident = conftest.item_id(created)
    _attach_poster(producer, ident, alt_text="Probe Stylist, stylist.")
    before = _disciplines(anon.get("/disciplines").json())
    assert "stylist" not in before, (
        "an unpublished talent must not reach the derived discipline set; the "
        f"set carried {before}")
    published = _publish(producer, ident)
    assert published.status_code in (200, 201), (
        "publishing the probe talent should succeed: "
        + conftest.describe(published))
    after = _disciplines(anon.get("/disciplines").json())
    assert "stylist" in after, (
        "publishing a talent carrying a new discipline must add that discipline "
        f"to the derived set with nobody editing a list; the set carried {after}")


def test_unpublishing_the_last_talent_removes_the_discipline(producer, anon):
    slug = conftest.probe_slug("probe-grader-of-colour")
    created = _create_item(producer, "talent", slug, "Probe Colourist",
                           discipline="colourist")
    ident = conftest.item_id(created)
    _attach_poster(producer, ident, alt_text="Probe Colourist, colourist.")
    _publish(producer, ident)
    assert "colourist" in _disciplines(anon.get("/disciplines").json()), (
        "the probe discipline must be present while its only talent is published")
    removed = _unpublish(producer, ident)
    assert removed.status_code in (200, 201, 204), (
        "unpublishing the probe talent should succeed: "
        + conftest.describe(removed))
    after = _disciplines(anon.get("/disciplines").json())
    assert "colourist" not in after, (
        "unpublishing the last talent of a discipline must remove that "
        f"discipline from the derived set; the set carried {after}")


def test_producer_creates_a_talent_unpublished(producer, anon, backend):
    slug = conftest.probe_slug("probe-director")
    created = _create_item(producer, "talent", slug, "Probe Director",
                           discipline="director")
    ident = conftest.item_id(created)
    row = backend.one("items", slug=slug)
    assert row is not None, (
        f"the created talent {slug} must exist as a stored row")
    assert not row.get("published"), (
        f"a newly created talent must be stored unpublished; the row carried "
        f"published={row.get('published')!r}")
    assert row.get("published_at") in (None, ""), (
        "an unpublished talent must carry no published time; the row carried "
        f"published_at={row.get('published_at')!r}")
    public = anon.get(f"/talents/{slug}")
    assert public.status_code == 404, (
        f"the unpublished talent {slug} must answer not-found to a signed-out "
        "reader: " + conftest.describe(public))


def test_publish_makes_the_item_readable_in_one_act(producer, anon, store):
    slug = conftest.probe_slug("probe-published")
    created = _create_item(producer, "talent", slug, "Probe Published",
                           discipline="director")
    ident = conftest.item_id(created)
    payload, _ = _attach_poster(producer, ident,
                                alt_text="Probe Published, director.")
    key = conftest.expected_object_key(ident, payload, "image/png")
    assert anon.get(f"/talents/{slug}").status_code == 404, (
        "the probe talent must be unreachable before publication")
    response = _publish(producer, ident)
    assert response.status_code in (200, 201), (
        "publishing the probe talent should succeed: "
        + conftest.describe(response))
    listed = _names(anon.get("/talents").json())
    assert "Probe Published" in listed, (
        f"publishing must add the talent to the roster; roster carried {listed}")
    detail = anon.get(f"/talents/{slug}")
    assert detail.status_code == 200, (
        "publishing must make the talent's own address readable: "
        + conftest.describe(detail))
    assert store.exists(key), (
        f"the published talent's poster must be readable from the object store "
        f"at {key}")


def test_unpublish_removes_the_item_from_every_public_read(producer, anon):
    slug = conftest.probe_slug("probe-withdrawn")
    created = _create_item(producer, "talent", slug, "Probe Withdrawn",
                           discipline="director")
    ident = conftest.item_id(created)
    _attach_poster(producer, ident, alt_text="Probe Withdrawn, director.")
    _publish(producer, ident)
    assert anon.get(f"/talents/{slug}").status_code == 200, (
        "the probe talent must be readable once published")
    response = _unpublish(producer, ident)
    assert response.status_code in (200, 201, 204), (
        "unpublishing the probe talent should succeed: "
        + conftest.describe(response))
    detail = anon.get(f"/talents/{slug}")
    assert detail.status_code == 404, (
        "unpublishing must make the talent's own address answer not-found: "
        + conftest.describe(detail))
    listed = _names(anon.get("/talents").json())
    assert "Probe Withdrawn" not in listed, (
        f"unpublishing must remove the talent from the roster; roster carried "
        f"{listed}")


def test_reordering_works_changes_the_public_ordinals(producer, anon):
    listing = anon.get("/works")
    rows = _shapes.items(listing.json())
    assert len(rows) >= 2, (
        "the seeded corpus pins twelve published works, so the listing must "
        "carry at least two rows: " + conftest.describe(listing))
    ids = [conftest.item_id(row) for row in rows]
    reordered = [ids[1], ids[0]] + ids[2:]
    response = producer.post("/works/order", json={"order": reordered})
    assert response.status_code in (200, 201), (
        "reordering the works as the producer should succeed: "
        + conftest.describe(response))
    after = _slugs(anon.get("/works").json())
    original = _slugs(listing.json())
    assert after[0] == original[1], (
        f"the reordered work must now show first; the listing carried {after}")
    assert _ordinals(anon.get("/works").json()) == list(conftest.SEEDED_ORDINALS), (
        "reordering must leave the displayed ordinals contiguous from 001")
    producer.post("/works/order", json={"order": ids})


def test_preview_returns_an_unpublished_item_for_a_producer(producer, backend):
    row = backend.one("items", slug=conftest.UNPUBLISHED_TALENT_SLUG)
    assert row is not None, (
        f"the seeded unpublished talent {conftest.UNPUBLISHED_TALENT_SLUG} must "
        "exist as a stored row")
    response = producer.get(f"/preview/{row['id']}")
    assert response.status_code == 200, (
        "a producer must be able to preview an unpublished item: "
        + conftest.describe(response))
    assert conftest.UNPUBLISHED_TALENT_NAME in _shapes.flatten(response.json()), (
        "the preview must return the unpublished item in full: "
        + conftest.describe(response))


def test_page_view_is_recorded_for_a_public_route(anon, producer, backend):
    before = backend.count("page_views")
    response = anon.post("/page-views", json={"route": "/works"})
    assert response.status_code in (200, 201), (
        "recording a public page view should succeed: "
        + conftest.describe(response))
    after = conftest.poll_until(lambda: backend.count("page_views") > before)
    assert after, (
        f"a public page view must write one page_views row; the count stayed at "
        f"{before}")
    log = producer.get("/page-views")
    assert log.status_code == 200, (
        "a producer must be able to read the page-view log: "
        + conftest.describe(log))


def test_each_public_route_carries_its_own_title_and_description(site):
    import re

    titles = {}
    descriptions = {}
    for route in conftest.PUBLIC_ROUTES:
        page = site.get(route)
        assert page.status_code == 200, (
            f"the public route {route} must render: " + conftest.describe(page))
        title = re.search(r"<title[^>]*>(.*?)</title>", page.text,
                          re.S | re.I)
        assert title, f"the public route {route} must emit its own title"
        description = re.search(
            r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']',
            page.text, re.S | re.I)
        assert description, (
            f"the public route {route} must emit its own description")
        titles[route] = title.group(1).strip()
        descriptions[route] = description.group(1).strip()
    assert len(set(titles.values())) == len(titles), (
        f"no two public routes may share a title; the routes carried {titles}")
    assert len(set(descriptions.values())) == len(descriptions), (
        "no two public routes may share a description; the routes carried "
        f"{descriptions}")


def test_not_found_response_does_not_echo_the_requested_path(site_direct):
    marker = conftest.unique_token()
    page = site_direct.get(f"/works/no-such-work-{marker}")
    assert page.status_code == 404, (
        "an address that does not resolve must answer a real not-found status: "
        + conftest.describe(page))
    assert marker not in page.text, (
        "the not-found route must never echo the requested path back into the "
        "page: " + conftest.describe(page))


def test_security_headers_are_present_on_every_response(site):
    for route in conftest.PUBLIC_ROUTES:
        page = site.get(route)
        lowered = {k.lower() for k in page.headers}
        for header in conftest.SECURITY_HEADERS:
            assert header in lowered, (
                f"the public route {route} must carry the {header} response "
                f"header; the response carried {sorted(lowered)}")


def test_preview_response_forbids_shared_cache_and_indexing(producer, backend):
    row = backend.one("items", slug=conftest.UNPUBLISHED_TALENT_SLUG)
    response = producer.get(f"/preview/{row['id']}")
    cache = response.headers.get("cache-control", "").lower()
    robots = response.headers.get("x-robots-tag", "").lower()
    assert "private" in cache or "no-store" in cache, (
        "a preview response must forbid storage by a shared cache; the response "
        f"carried cache-control={cache!r}")
    assert "noindex" in robots, (
        "a preview response must forbid indexing; the response carried "
        f"x-robots-tag={robots!r}")


def test_signup_cannot_grant_the_producer_role(anon, backend):
    email = conftest.probe_email()
    response = anon.post("/auth/signup", json={
        "email": email, "password": conftest.APP_PASSWORD, "role": "producer"})
    assert response.status_code in (200, 201, 400, 422), (
        "signup must answer rather than fail: " + conftest.describe(response))
    row = backend.one("accounts", email=email)
    if row is not None:
        assert row.get("role") != "producer", (
            "a signup must never grant the producer role however the request "
            f"body is shaped; the stored row carried role={row.get('role')!r}")


def test_login_with_a_wrong_password_is_denied(anon):
    response = anon.post("/auth/login", json={
        "email": conftest.PRODUCER_EMAIL, "password": "not-the-password"})
    assert response.status_code in (400, 401, 403, 422), (
        "signing in with a wrong password must be denied: "
        + conftest.describe(response))


def test_studio_endpoints_are_denied_to_an_unauthenticated_caller(anon):
    for route in conftest.STUDIO_API_ROUTES:
        response = anon.get(route)
        assert response.status_code in (401, 403), (
            f"the studio endpoint {route} must be denied to a signed-out "
            "caller at the API: " + conftest.describe(response))


def test_visitor_is_forbidden_the_publish_endpoint(visitor, backend):
    row = backend.one("items", slug=conftest.UNPUBLISHED_TALENT_SLUG)
    response = visitor.post(f"/items/{row['id']}/publish")
    assert response.status_code in (401, 403), (
        "a visitor must be refused the publish endpoint: "
        + conftest.describe(response))
    after = backend.one("items", slug=conftest.UNPUBLISHED_TALENT_SLUG)
    assert not after.get("published"), (
        "a refused publish must leave the stored row untouched; the row carried "
        f"published={after.get('published')!r}")


def test_visitor_is_forbidden_the_page_view_log(visitor):
    response = visitor.get("/page-views")
    assert response.status_code in (401, 403), (
        "a visitor must be refused the page-view log: "
        + conftest.describe(response))


def test_unpublished_item_is_denied_to_a_visitor_by_slug(anon, visitor,
                                                         site_direct):
    for label, client in (("a signed-out reader", anon), ("a visitor", visitor)):
        response = client.get(f"/talents/{conftest.UNPUBLISHED_TALENT_SLUG}")
        assert response.status_code == 404, (
            f"the unpublished talent must answer not-found to {label} at the "
            "API: " + conftest.describe(response))
        response = client.get(f"/works/{conftest.UNPUBLISHED_WORK_SLUG}")
        assert response.status_code == 404, (
            f"the unpublished work must answer not-found to {label} at the API: "
            + conftest.describe(response))
    page = site_direct.get(f"/talents/{conftest.UNPUBLISHED_TALENT_SLUG}")
    assert page.status_code == 404, (
        "the unpublished talent's route must answer not-found to a signed-out "
        "reader: " + conftest.describe(page))
    assert conftest.UNPUBLISHED_TALENT_NAME not in page.text, (
        "the not-found response must reveal nothing about whether the "
        "unpublished talent exists: " + conftest.describe(page))


def test_preview_is_denied_without_a_producer_session(anon, visitor, backend):
    row = backend.one("items", slug=conftest.UNPUBLISHED_TALENT_SLUG)
    for label, client in (("a signed-out reader", anon), ("a visitor", visitor)):
        response = client.get(f"/preview/{row['id']}")
        assert response.status_code in (401, 403, 404), (
            f"the preview route must be denied to {label}: "
            + conftest.describe(response))
        assert conftest.UNPUBLISHED_TALENT_NAME not in response.text, (
            f"a denied preview must reveal nothing to {label}: "
            + conftest.describe(response))


def test_seeded_works_are_stored_with_unique_slugs(backend):
    for slug in conftest.WORK_SLUGS:
        assert backend.count("items", slug=slug, kind="work") == 1, (
            f"the seeded work {slug} must be stored exactly once")
    for slug in conftest.TALENT_SLUGS:
        assert backend.count("items", slug=slug, kind="talent") == 1, (
            f"the seeded talent {slug} must be stored exactly once")


def test_seed_is_idempotent_across_a_restart(backend):
    for slug in conftest.WORK_SLUGS + conftest.TALENT_SLUGS:
        assert backend.count("items", slug=slug) == 1, (
            f"seeding must be idempotent, so {slug} must exist exactly once "
            "however many times the app has started")
    for email in (conftest.PRODUCER_EMAIL, conftest.PRODUCER2_EMAIL,
                  conftest.VISITOR_EMAIL):
        assert backend.count("accounts", email=email) == 1, (
            f"the seeded account {email} must exist exactly once")


def test_slug_survives_a_title_change(producer, anon, backend):
    slug = conftest.probe_slug("probe-renamed")
    created = _create_item(producer, "talent", slug, "Probe Before",
                           discipline="director")
    ident = conftest.item_id(created)
    response = producer.patch(f"/items/{ident}", json={"title": "Probe After"})
    assert response.status_code in (200, 201), (
        "renaming the probe talent as the producer should succeed: "
        + conftest.describe(response))
    row = backend.one("items", id=ident)
    assert str(row.get("slug")) == slug, (
        f"a title change must never change the slug; the row carried "
        f"slug={row.get('slug')!r} after the rename")
    assert str(row.get("title")) == "Probe After", (
        "the title change must persist; the row carried "
        f"title={row.get('title')!r}")


def test_changed_slug_leaves_a_permanent_redirect(producer, anon, site_direct):
    slug = conftest.probe_slug("probe-moved")
    created = _create_item(producer, "talent", slug, "Probe Moved",
                           discipline="director")
    ident = conftest.item_id(created)
    _attach_poster(producer, ident, alt_text="Probe Moved, director.")
    _publish(producer, ident)
    new_slug = conftest.probe_slug("probe-settled")
    response = producer.patch(f"/items/{ident}", json={"slug": new_slug})
    assert response.status_code in (200, 201), (
        "changing the probe talent's slug should succeed: "
        + conftest.describe(response))
    redirect = site_direct.get(f"/talents/{slug}")
    assert redirect.status_code == 301, (
        f"the old address /talents/{slug} must keep resolving with a permanent "
        "redirect: " + conftest.describe(redirect))
    assert new_slug in redirect.headers.get("location", ""), (
        "the permanent redirect must point at the new address; the response "
        f"carried location={redirect.headers.get('location')!r}")


def test_published_at_is_stamped_on_publish_and_cleared_on_unpublish(
        producer, backend):
    slug = conftest.probe_slug("probe-stamped")
    created = _create_item(producer, "talent", slug, "Probe Stamped",
                           discipline="director")
    ident = conftest.item_id(created)
    _attach_poster(producer, ident, alt_text="Probe Stamped, director.")
    _publish(producer, ident)
    row = backend.one("items", id=ident)
    assert row.get("published_at") not in (None, ""), (
        "publishing must stamp the published time; the row carried "
        f"published_at={row.get('published_at')!r}")
    _unpublish(producer, ident)
    row = backend.one("items", id=ident)
    assert row.get("published_at") in (None, ""), (
        "unpublishing must clear the published time; the row carried "
        f"published_at={row.get('published_at')!r}")


def test_credit_without_a_talent_reference_is_stored(producer, backend):
    slug = conftest.probe_slug("probe-credited")
    created = _create_item(producer, "work", slug, "Probe Credited",
                           variant="left")
    ident = conftest.item_id(created)
    response = producer.post(f"/items/{ident}/credits", json={
        "role": "Gaffer", "name": "Someone The House Does Not Represent"})
    assert response.status_code in (200, 201), (
        "a credit naming someone the house does not represent must be accepted: "
        + conftest.describe(response))
    rows = backend.rows("credits", work_id=ident)
    assert rows, f"the credit on {slug} must be stored as a row"
    assert rows[0].get("talent_id") in (None, ""), (
        "a credit naming someone the house does not represent must carry a null "
        f"talent reference; the row carried talent_id={rows[0].get('talent_id')!r}")


def test_talent_selected_work_is_derived_not_stored(anon, backend):
    row = backend.one("items", slug=conftest.TALENT_SLUGS[0])
    assert row is not None, (
        f"the seeded talent {conftest.TALENT_SLUGS[0]} must be stored")
    for forbidden in ("works", "work_ids", "selected_work", "credited_work"):
        assert forbidden not in row, (
            "a talent's selected work must be derived by reading credits, never "
            f"stored on the talent; the row carried a {forbidden} column")
    detail = anon.get(f"/talents/{conftest.TALENT_SLUGS[0]}")
    assert any(slug in _shapes.flatten(detail.json())
               for slug in conftest.WORK_SLUGS), (
        "the derived selected work must still reach the talent's own route: "
        + conftest.describe(detail))


def test_page_view_rows_survive_a_re_read(anon, producer, backend):
    marker = f"/works?probe={conftest.unique_token()}"
    anon.post("/page-views", json={"route": marker})
    found = conftest.poll_until(lambda: backend.count("page_views", route=marker))
    assert found, f"the recorded page view for {marker} must be stored as a row"
    again = producer.get("/page-views")
    assert marker in _shapes.flatten(again.json()), (
        "a recorded page view must survive a re-read through the producer's log: "
        + conftest.describe(again))


def test_ordinals_stay_contiguous_after_an_unpublish(producer, anon, backend):
    listing = anon.get("/works")
    rows = _shapes.items(listing.json())
    victim = rows[6]
    ident = conftest.item_id(victim)
    response = _unpublish(producer, ident)
    assert response.status_code in (200, 201, 204), (
        "unpublishing the seventh work should succeed: "
        + conftest.describe(response))
    try:
        after = anon.get("/works")
        ordinals = _ordinals(after.json())
        expected = [f"{n:03d}" for n in range(1, len(ordinals) + 1)]
        assert ordinals == expected, (
            "unpublishing a work must renumber the rest so a reader never sees "
            f"a gap; the listing carried {ordinals}, expected {expected}")
        assert len(ordinals) == len(rows) - 1, (
            "unpublishing one work must leave exactly one fewer published work")
        assert len(set(ordinals)) == len(ordinals), (
            f"no ordinal may be shown twice; the listing carried {ordinals}")
    finally:
        _publish(producer, ident)


def test_publish_is_refused_when_media_has_no_alt_text(producer, backend):
    slug = conftest.probe_slug("probe-unlabelled")
    created = _create_item(producer, "talent", slug, "Probe Unlabelled",
                           discipline="director")
    ident = conftest.item_id(created)
    attached = producer.post(
        f"/items/{ident}/media",
        files={"file": ("poster.png", conftest.probe_bytes(), "image/png")},
        data={"role": "poster", "alt_text": "", "width": "1600",
              "height": "900"})
    response = _publish(producer, ident)
    assert response.status_code in (400, 409, 422), (
        "publishing an item whose media carries no text alternative must be "
        "refused: " + conftest.describe(response))
    row = backend.one("items", id=ident)
    assert not row.get("published"), (
        "a refused publish must leave the item unpublished; the row carried "
        f"published={row.get('published')!r}")


def test_duplicate_slug_within_a_kind_is_refused(producer, backend):
    slug = conftest.probe_slug("probe-twice")
    _create_item(producer, "talent", slug, "Probe First", discipline="director")
    before = backend.count("items", slug=slug)
    response = producer.post("/items", json={
        "kind": "talent", "slug": slug, "title": "Probe Second",
        "discipline": "director"})
    assert response.status_code in (400, 409, 422), (
        "a second talent carrying an existing talent slug must be refused: "
        + conftest.describe(response))
    assert backend.count("items", slug=slug) == before, (
        "a refused create must write no row; the stored count moved from "
        f"{before}")


def test_same_slug_across_kinds_is_accepted(producer, backend):
    slug = conftest.probe_slug("probe-shared")
    _create_item(producer, "talent", slug, "Probe Shared Talent",
                 discipline="director")
    response = producer.post("/items", json={
        "kind": "work", "slug": slug, "title": "Probe Shared Work",
        "variant": "left"})
    assert response.status_code in (200, 201), (
        "a slug is unique within kind, so a work may carry a talent's slug: "
        + conftest.describe(response))
    assert backend.count("items", slug=slug) == 2, (
        "both the talent and the work carrying that slug must be stored")


def test_refused_write_leaves_no_row(producer, backend):
    before = backend.count("items")
    response = producer.post("/items", json={"kind": "talent"})
    assert response.status_code in (400, 422), (
        "a create missing the slug and the title must be refused: "
        + conftest.describe(response))
    assert backend.count("items") == before, (
        f"a refused write must write nothing at all; the stored count moved "
        f"from {before} to {backend.count('items')}")


def test_unknown_address_answers_not_found(site_direct):
    page = site_direct.get(f"/no-such-route-{conftest.unique_token()}")
    assert page.status_code == 404, (
        "an unknown address must answer the product's own not-found route with "
        "a real not-found status: " + conftest.describe(page))


def test_list_endpoints_return_top_level_arrays(anon):
    for route in ("/works", "/talents", "/disciplines"):
        response = anon.get(route)
        assert response.status_code == 200, (
            f"the public list endpoint {route} must answer: "
            + conftest.describe(response))
        assert isinstance(response.json(), list), (
            f"the list endpoint {route} must return a top-level JSON array; it "
            f"returned {type(response.json()).__name__}: "
            + conftest.describe(response))


def test_uploaded_bytes_land_in_the_object_store_bucket(producer, store):
    slug = conftest.probe_slug("probe-stored")
    created = _create_item(producer, "talent", slug, "Probe Stored",
                           discipline="director")
    ident = conftest.item_id(created)
    payload, _ = _attach_poster(producer, ident,
                                alt_text="Probe Stored, director.")
    key = conftest.expected_object_key(ident, payload, "image/png")
    found = conftest.poll_until(lambda: store.exists(key))
    assert found, (
        f"the uploaded poster must land in the object store bucket at {key}; "
        f"the bucket held {store.list(conftest.OBJECT_KEY_PREFIX)[:20]}")


def test_object_key_follows_the_scheme(producer, store, backend):
    slug = conftest.probe_slug("probe-keyed")
    created = _create_item(producer, "talent", slug, "Probe Keyed",
                           discipline="director")
    ident = conftest.item_id(created)
    payload, media = _attach_poster(producer, ident,
                                    alt_text="Probe Keyed, director.")
    expected = conftest.expected_object_key(ident, payload, "image/png")
    row = backend.one("media", item_id=ident)
    assert row is not None, "the attached poster must be stored as a media row"
    assert str(row.get("object_key")) == expected, (
        "the stored object key must follow items/{item_id}/{sha256}.{ext}; the "
        f"row carried object_key={row.get('object_key')!r}, expected {expected}")
    assert store.exists(expected), (
        f"the bucket must hold the object at the recorded key {expected}")


def test_identical_bytes_resolve_to_one_object(producer, store, backend):
    slug = conftest.probe_slug("probe-deduped")
    created = _create_item(producer, "talent", slug, "Probe Deduped",
                           discipline="director")
    ident = conftest.item_id(created)
    payload = conftest.probe_bytes()
    _attach_poster(producer, ident, payload=payload,
                   alt_text="Probe Deduped, director.")
    producer.post(
        f"/items/{ident}/media",
        files={"file": ("again.png", payload, "image/png")},
        data={"role": "still", "alt_text": "Probe Deduped again.",
              "width": "1600", "height": "900"})
    key = conftest.expected_object_key(ident, payload, "image/png")
    keys = [k for k in store.list(f"items/{ident}/") if k == key]
    assert len(keys) == 1, (
        "two uploads of identical bytes for one item must resolve to one "
        f"object; the bucket held {keys}")


def test_media_of_an_unpublished_item_is_not_served_publicly(
        producer, anon, visitor, backend):
    row = backend.one("items", slug=conftest.UNPUBLISHED_TALENT_SLUG)
    media = backend.one("media", item_id=row["id"])
    assert media is not None, (
        "the seeded unpublished talent must carry a poster media row")
    for label, client in (("a signed-out reader", anon), ("a visitor", visitor)):
        response = client.get(f"/media/{media['id']}")
        assert response.status_code in (401, 403, 404), (
            f"the media of an unpublished item must be refused to {label}: "
            + conftest.describe(response))
    allowed = producer.get(f"/media/{media['id']}")
    assert allowed.status_code in (200, 302, 307), (
        "the same media must be readable by a producer: "
        + conftest.describe(allowed))


def test_media_row_records_role_dimensions_one_poster_and_at_most_one_reel(
        producer, backend):
    slug = conftest.probe_slug("probe-measured")
    created = _create_item(producer, "talent", slug, "Probe Measured",
                           discipline="director")
    ident = conftest.item_id(created)
    _attach_poster(producer, ident, alt_text="Probe Measured, director.")
    rows = backend.rows("media", item_id=ident)
    assert rows, "the attached poster must be stored as a media row"
    row = rows[0]
    assert str(row.get("role")) == "poster", (
        "a media row must record its role as one of poster, still or reel; the "
        f"row carried role={row.get('role')!r}")
    for field in ("width", "height"):
        value = row.get(field)
        assert value not in (None, "", 0), (
            f"a media row must record the intrinsic {field} of the bytes so a "
            f"tile reserves space before the image arrives; the row carried "
            f"{field}={value!r}")
    producer.post(
        f"/items/{ident}/media",
        files={"file": ("second.png", conftest.probe_bytes(), "image/png")},
        data={"role": "still", "alt_text": "Probe Measured, a still.",
              "width": "1600", "height": "900"})
    posters = [r for r in backend.rows("media", item_id=ident)
               if str(r.get("role")) == "poster"]
    assert len(posters) == 1, (
        f"an item carries exactly one poster; the store held {len(posters)}")
    reels = [r for r in backend.rows("media", item_id=ident)
             if str(r.get("role")) == "reel"]
    assert len(reels) <= 1, (
        f"an item carries at most one reel; the store held {len(reels)}")


def test_schema_holds_the_named_tables_and_no_ordinal_column_on_items(backend):
    for table in ("accounts", "items", "media", "credits", "slug_redirects",
                  "page_views"):
        backend.count(table)
    row = backend.one("items", slug=conftest.WORK_SLUGS[0])
    assert row is not None, (
        f"the seeded work {conftest.WORK_SLUGS[0]} must be stored as an items row")
    assert "ordinal" not in row, (
        "the displayed ordinal is computed over the published set at read time, "
        "so no ordinal column is stored as a label; the items row carried one")
    assert str(row.get("id")) != conftest.WORK_SLUGS[0], (
        "an item id is stable and opaque and is never derived from the title or "
        f"the slug; the row carried id={row.get('id')!r}")
    account = backend.one("accounts", email=conftest.PRODUCER_EMAIL)
    assert account is not None, (
        f"the seeded account {conftest.PRODUCER_EMAIL} must be stored")
    for field in ("id", "email", "role"):
        assert field in account, (
            f"an account row records an id, an email, a password hash, a role "
            f"and a creation time; the row carried no {field}")
    assert "password" not in str(account.get("password_hash", "")).lower(), (
        "an account row stores a hash rather than the password literal; the row "
        "carried something that reads as the password")
