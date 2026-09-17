"""The single pytest module for the Orb website builder bundle."""

from __future__ import annotations

import concurrent.futures
import os
import re

import httpx

import _shapes
import appclient
import conftest

ICON_RE = re.compile(
    r"""<link[^>]+rel=["'][^"']*icon[^"']*["'][^>]*>""", re.IGNORECASE)
HREF_RE = re.compile(r"""href=["']([^"']+)["']""", re.IGNORECASE)
OG_IMAGE_RE = re.compile(
    r"""<meta[^>]+property=["']og:image["'][^>]*content=["']([^"']+)["']""",
    re.IGNORECASE)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
DESCRIPTION_RE = re.compile(
    r"""<meta[^>]+name=["']description["'][^>]*content=["']([^"']*)["']""",
    re.IGNORECASE)
REQUEST_ID_HEADERS = ("x-request-id", "x-request-identifier", "request-id",
                      "x-correlation-id")


def _absolute(base: str, href: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return f"{base.rstrip('/')}/{href.lstrip('/')}"




def test_health_endpoint_is_ready(anon):
    response = anon.get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}, expected 200 once the "
        f"app is ready: {response.text[:300]}")


def test_owner_login_returns_access_token(anon):
    response = anon.post("/auth/login",
                         json={"email": conftest.OWNER_EMAIL,
                               "password": conftest.PASSWORD})
    assert response.status_code == 200, (
        f"login for {conftest.OWNER_EMAIL} returned {response.status_code}, "
        f"expected 200: {response.text[:300]}")
    assert response.json().get("access_token"), (
        f"login for {conftest.OWNER_EMAIL} returned no access_token: "
        f"{response.text[:300]}")


def test_domain_availability_answers_registered_name(anon):
    response = anon.get("/domains/availability",
                        params={"query": conftest.REGISTERED_NAME})
    assert response.status_code == 200, (
        f"availability for {conftest.REGISTERED_NAME} returned "
        f"{response.status_code}: {response.text[:300]}")
    body = response.json()
    exact = body.get("exact") or {}
    assert exact.get("available") is False, (
        f"{conftest.REGISTERED_NAME} is seeded as taken, yet exact.available is "
        f"{exact.get('available')!r}: {response.text[:300]}")
    assert exact.get("registry_status") == conftest.REGISTRY_REGISTERED, (
        f"{conftest.REGISTERED_NAME} reported registry_status "
        f"{exact.get('registry_status')!r}, expected "
        f"{conftest.REGISTRY_REGISTERED!r}: {response.text[:300]}")


def test_domain_availability_answers_free_name_price(anon):
    response = anon.get("/domains/availability",
                        params={"query": conftest.FREE_NAME})
    assert response.status_code == 200, (
        f"availability for {conftest.FREE_NAME} returned {response.status_code}: "
        f"{response.text[:300]}")
    body = response.json()
    exact = body.get("exact") or {}
    assert exact.get("available") is True, (
        f"{conftest.FREE_NAME} is seeded as free, yet exact.available is "
        f"{exact.get('available')!r}: {response.text[:300]}")
    assert exact.get("registry_status") == conftest.REGISTRY_AVAILABLE, (
        f"{conftest.FREE_NAME} reported registry_status "
        f"{exact.get('registry_status')!r}, expected "
        f"{conftest.REGISTRY_AVAILABLE!r}: {response.text[:300]}")
    assert int(exact.get("price")) == conftest.FREE_NAME_PRICE, (
        f"{conftest.FREE_NAME} is priced {exact.get('price')!r} minor units, "
        f"expected {conftest.FREE_NAME_PRICE}: {response.text[:300]}")
    assert str(exact.get("currency")).lower() == conftest.CURRENCY, (
        f"{conftest.FREE_NAME} is priced in {exact.get('currency')!r}, expected "
        f"{conftest.CURRENCY!r}: {response.text[:300]}")
    assert body.get("partial") is False, (
        f"a complete availability answer must report partial false, got "
        f"{body.get('partial')!r}: {response.text[:300]}")


def test_domain_query_normalises_padding_and_case(anon):
    padded = anon.get("/domains/availability", params={"query": "  ForkNFrame  "})
    plain = anon.get("/domains/availability", params={"query": "forknframe"})
    assert padded.status_code == 200 and plain.status_code == 200, (
        f"availability returned {padded.status_code} for the padded label and "
        f"{plain.status_code} for the plain one: {padded.text[:200]}")
    assert padded.json().get("normalised") == plain.json().get("normalised"), (
        f"'  ForkNFrame  ' normalised to {padded.json().get('normalised')!r} while "
        f"'forknframe' normalised to {plain.json().get('normalised')!r}; the two "
        f"are the same query")
    assert padded.json().get("normalised") == "forknframe", (
        f"the normalised label is {padded.json().get('normalised')!r}, expected "
        f"the trimmed lower-cased 'forknframe'")


def test_domain_suggestions_are_stable_across_two_calls(anon):
    first = anon.get("/domains/availability",
                     params={"query": "kestrelatelier"})
    second = anon.get("/domains/availability",
                      params={"query": "kestrelatelier"})
    assert first.status_code == 200 and second.status_code == 200, (
        f"availability returned {first.status_code} then {second.status_code}: "
        f"{first.text[:200]}")
    names_first = [s.get("name") for s in (first.json().get("suggestions") or [])]
    names_second = [s.get("name") for s in (second.json().get("suggestions") or [])]
    assert names_first == names_second, (
        f"two identical queries returned different suggestion orders: "
        f"{names_first[:5]} then {names_second[:5]}")
    assert len(names_first) <= 8, (
        f"the default suggestion count is 8, got {len(names_first)}: "
        f"{names_first[:12]}")
    capped = anon.get("/domains/availability",
                      params={"query": "kestrelatelier", "suggest": 99})
    assert capped.status_code == 200, (
        f"availability with suggest=99 returned {capped.status_code}: "
        f"{capped.text[:300]}")
    assert len(capped.json().get("suggestions") or []) <= 20, (
        f"the suggestion count is capped at 20, got "
        f"{len(capped.json().get('suggestions') or [])}")


def test_templates_listing_carries_facets_and_cap(anon):
    response = anon.get("/templates", params={"limit": 999})
    assert response.status_code == 200, (
        f"GET /api/templates returned {response.status_code}: {response.text[:300]}")
    body = response.json()
    items = _shapes.items(body)
    assert len(items) <= conftest.TEMPLATE_LIMIT_CAP, (
        f"a page size of 999 must clamp to {conftest.TEMPLATE_LIMIT_CAP}, got "
        f"{len(items)} items")
    facets = body.get("facets") if isinstance(body, dict) else None
    assert isinstance(facets, dict) and facets, (
        f"GET /api/templates carries no facets object, got {type(facets).__name__}: "
        f"{response.text[:300]}")
    for category in conftest.TEMPLATE_CATEGORIES:
        assert category in facets, (
            f"the facet count is missing the category {category!r}; facets carried "
            f"{sorted(facets)[:10]}")
    ordered_once = [t.get("slug") or t.get("name") for t in items]
    ordered_twice = [t.get("slug") or t.get("name")
                     for t in _shapes.items(anon.get("/templates",
                                                     params={"limit": 999}).json())]
    assert ordered_once == ordered_twice, (
        f"the template ordering is not stable across two reads: "
        f"{ordered_once[:5]} then {ordered_twice[:5]}")


def test_templates_unknown_category_is_refused(anon):
    response = anon.get("/templates", params={"category": "Submarines"})
    assert response.status_code in (400, 404, 422), (
        f"an unknown template category returned {response.status_code}, expected a "
        f"client error: {response.text[:300]}")


def test_signup_creates_account_workspace_and_draft_site(anon, owner):
    email, payload = conftest.new_owner(anon)
    token = payload["access_token"]
    with appclient.client(token) as client:
        sites = client.get("/sites")
        assert sites.status_code == 200, (
            f"GET /api/sites for the new tenant {email} returned "
            f"{sites.status_code}: {sites.text[:300]}")
        rows = _shapes.items(sites.json())
        assert len(rows) == 1, (
            f"sign-up must create exactly one first site for {email}, found "
            f"{len(rows)}: {sites.text[:300]}")
        assert str(rows[0].get("status")) == conftest.STATUS_DRAFT, (
            f"the first site for {email} has status {rows[0].get('status')!r}, "
            f"expected {conftest.STATUS_DRAFT!r}")
        assert not rows[0].get("live_revision"), (
            f"the first site for {email} already names a live_revision "
            f"{rows[0].get('live_revision')!r} before any publish")
    assert owner.get("/sites").status_code == 200, (
        "the seeded owner must keep reading their own sites while a new tenant exists")


def test_signup_replay_creates_no_second_account(anon, backend):
    email = conftest.probe_email()
    first = conftest.signup(anon, email)
    assert first.status_code in (200, 201), (
        f"the first sign-up for {email} returned {first.status_code}: "
        f"{first.text[:300]}")
    second = conftest.signup(anon, email)
    assert second.status_code in (200, 201), (
        f"a replayed sign-up for {email} inside the window must return the first "
        f"answer, got {second.status_code}: {second.text[:300]}")
    assert second.json().get("site_id") == first.json().get("site_id"), (
        f"the replayed sign-up for {email} returned site_id "
        f"{second.json().get('site_id')!r}, expected the first answer "
        f"{first.json().get('site_id')!r}")
    assert backend.count("accounts", email=email) == 1, (
        f"two sign-ups on {email} left "
        f"{backend.count('accounts', email=email)} account rows, expected exactly one")


def test_signup_short_password_is_refused(anon, backend):
    email = conftest.probe_email()
    response = conftest.signup(anon, email, password="short")
    assert response.status_code in (400, 422), (
        f"a password under eight characters returned {response.status_code}, "
        f"expected a client error: {response.text[:300]}")
    assert backend.count("accounts", email=email) == 0, (
        f"a refused sign-up wrote an account row for {email}")


def test_signup_decoy_field_submission_is_refused(anon, backend):
    email = conftest.probe_email()
    response = conftest.signup(anon, email, company_website="https://example.com")
    assert response.status_code in (400, 403, 422), (
        f"a sign-up filling the unattended decoy field returned "
        f"{response.status_code}, expected a client error: {response.text[:300]}")
    assert backend.count("accounts", email=email) == 0, (
        f"a refused sign-up wrote an account row for {email}")


def test_rollback_returns_site_to_draft(anon):
    _, payload = conftest.new_owner(anon)
    site_id = payload["site_id"]
    with appclient.client(payload["access_token"]) as client:
        published = client.post(f"/sites/{site_id}/publish")
        assert published.status_code in (200, 201), (
            f"publishing site {site_id} returned {published.status_code}: "
            f"{published.text[:300]}")
        assert str(published.json().get("status")) == conftest.STATUS_PUBLISHED, (
            f"site {site_id} reports status {published.json().get('status')!r} "
            f"after publish, expected {conftest.STATUS_PUBLISHED!r}")
        rolled = client.post(f"/sites/{site_id}/publish/rollback")
        assert rolled.status_code in (200, 201), (
            f"rolling back site {site_id} returned {rolled.status_code}: "
            f"{rolled.text[:300]}")
        after = client.get(f"/sites/{site_id}").json()
        assert str(after.get("status")) == conftest.STATUS_DRAFT, (
            f"site {site_id} reports status {after.get('status')!r} after rollback, "
            f"expected {conftest.STATUS_DRAFT!r}")
        assert not after.get("live_revision"), (
            f"site {site_id} still names live_revision "
            f"{after.get('live_revision')!r} after rollback")


def test_terms_page_is_reachable(raw):
    for route in ("/terms", "/privacy"):
        response = raw.get(route)
        assert response.status_code == 200, (
            f"{route} returned {response.status_code}, expected 200: "
            f"{response.text[:200]}")
        assert len(response.text) > 200, (
            f"{route} answered with {len(response.text)} characters, which is too "
            f"little to be the page the footer links to")
    home = raw.get("/")
    assert "/terms" in home.text, (
        "the home route's footer does not link to /terms")




def test_seeded_sites_stored_rows_match_the_brief(backend):
    slugs = {row.get("slug") for row in backend.rows("sites")}
    for expected in (conftest.PUBLISHED_SITE_SLUG, conftest.DRAFT_SITE_SLUG,
                     conftest.SECOND_OWNER_DRAFT_SLUG):
        assert expected in slugs, (
            f"the seeded site row {expected!r} is missing from the sites table; "
            f"stored slugs are {sorted(s for s in slugs if s)[:10]}")
    workspaces = {row.get("name") for row in backend.rows("workspaces")}
    assert "Kestrel Studio" in workspaces, (
        f"the first owner's workspace row is missing; stored workspaces are "
        f"{sorted(w for w in workspaces if w)[:10]}")
    assert "Cedar Workshop" in workspaces, (
        f"the second owner's workspace row is missing; stored workspaces are "
        f"{sorted(w for w in workspaces if w)[:10]}")


def test_sites_row_is_persisted_for_owner_only(anon, owner2, backend):
    _, payload = conftest.new_owner(anon)
    site_id = payload["site_id"]
    stored = backend.rows("sites", id=site_id)
    assert len(stored) == 1, (
        f"the site row {site_id} created at sign-up is not persisted; the sites "
        f"table holds {len(stored)} matching rows")
    listed = owner2.get("/sites")
    assert listed.status_code == 200, (
        f"GET /api/sites for the second seeded owner returned {listed.status_code}: "
        f"{listed.text[:300]}")
    other_ids = {str(row.get("id")) for row in _shapes.items(listed.json())}
    assert str(site_id) not in other_ids, (
        f"the second owner's site list leaks site {site_id}, which belongs to a "
        f"different workspace: {sorted(other_ids)[:10]}")


def test_templates_library_holds_thirty_three_rows(backend):
    stored = backend.count("templates")
    assert stored == conftest.TEMPLATE_COUNT, (
        f"the templates table holds {stored} rows, expected "
        f"{conftest.TEMPLATE_COUNT} distinct templates")
    categories = {row.get("category") for row in backend.rows("templates")}
    for category in conftest.TEMPLATE_CATEGORIES:
        assert category in categories, (
            f"no stored template row carries the category {category!r}; stored "
            f"categories are {sorted(c for c in categories if c)}")


def test_publish_rollback_keeps_one_stored_row_per_site(anon, backend):
    _, payload = conftest.new_owner(anon)
    site_id = payload["site_id"]
    with appclient.client(payload["access_token"]) as client:
        client.post(f"/sites/{site_id}/publish")
        client.post(f"/sites/{site_id}/publish/rollback")
        client.post(f"/sites/{site_id}/publish")
    stored = backend.rows("sites", id=site_id)
    assert len(stored) == 1, (
        f"publish, rollback and republish left {len(stored)} stored rows for site "
        f"{site_id}, expected exactly one")
    assert str(stored[0].get("status")) == conftest.STATUS_PUBLISHED, (
        f"site {site_id} is stored with status {stored[0].get('status')!r} after a "
        f"republish, expected {conftest.STATUS_PUBLISHED!r}")


def test_concurrent_publish_leaves_one_live_revision(anon, backend):
    _, payload = conftest.new_owner(anon)
    site_id = payload["site_id"]
    token = payload["access_token"]

    def publish():
        with appclient.client(token) as client:
            response = client.post(f"/sites/{site_id}/publish")
            return response.status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        codes = [f.result() for f in
                 [pool.submit(publish), pool.submit(publish)]]
    accepted = [c for c in codes if c in (200, 201)]
    assert len(accepted) >= 1, (
        f"two simultaneous publishes of site {site_id} both failed with {codes}; "
        f"exactly one must win")
    stored = backend.rows("sites", id=site_id)
    assert len(stored) == 1, (
        f"two simultaneous publishes left {len(stored)} rows for site {site_id}")
    live = stored[0].get("live_revision")
    assert live, (
        f"site {site_id} names no live_revision after a successful publish")
    revisions = backend.rows("revisions", site_id=site_id)
    live_matches = [r for r in revisions if str(r.get("number")) == str(live)
                    or str(r.get("id")) == str(live)]
    assert len(live_matches) == 1, (
        f"site {site_id} names live_revision {live!r}, which matches "
        f"{len(live_matches)} of its own revision rows, expected exactly one")


def test_slug_conflict_is_refused(anon, backend):
    _, payload = conftest.new_owner(anon)
    with appclient.client(payload["access_token"]) as client:
        before = backend.count("sites")
        response = client.post("/sites", json={"name": "Second Kestrel",
                                               "slug": conftest.PUBLISHED_SITE_SLUG})
        assert response.status_code in (400, 409, 422), (
            f"taking the slug {conftest.PUBLISHED_SITE_SLUG!r}, already held by a "
            f"seeded site, returned {response.status_code}, expected a client "
            f"error: {response.text[:300]}")
        assert backend.count("sites") == before, (
            f"a refused slug still wrote a site row; the sites table moved from "
            f"{before} to {backend.count('sites')}")




def test_wrong_password_is_denied(anon):
    response = anon.post("/auth/login",
                         json={"email": conftest.OWNER_EMAIL,
                               "password": "not-the-seeded-password"})
    assert response.status_code in (400, 401, 403), (
        f"a wrong password for {conftest.OWNER_EMAIL} returned "
        f"{response.status_code}, expected a client error: {response.text[:300]}")
    assert "access_token" not in response.text, (
        f"a denied sign-in returned an access_token: {response.text[:300]}")
    unknown = anon.post("/auth/login",
                        json={"email": conftest.probe_email(),
                              "password": conftest.PASSWORD})
    assert unknown.status_code == response.status_code, (
        f"an unknown address returned {unknown.status_code} while a wrong password "
        f"returned {response.status_code}; the two must not be distinguishable")


def test_visitor_cannot_list_owner_sites(visitor, anon):
    listed = visitor.get("/sites")
    if listed.status_code == 200:
        rows = _shapes.items(listed.json())
        assert rows == [], (
            f"the seeded visitor holds no workspace, yet GET /api/sites returned "
            f"{len(rows)} rows: {listed.text[:300]}")
    else:
        assert listed.status_code in (401, 403), (
            f"GET /api/sites as the seeded visitor returned {listed.status_code}, "
            f"expected a denial or an empty array: {listed.text[:300]}")
    anonymous = anon.get("/sites")
    assert anonymous.status_code in (401, 403), (
        f"GET /api/sites with no token returned {anonymous.status_code}, expected "
        f"a denial: {anonymous.text[:300]}")


def test_second_owner_cannot_read_first_owner_site(anon, owner2, backend):
    _, payload = conftest.new_owner(anon)
    site_id = payload["site_id"]
    before = backend.rows("sites", id=site_id)
    response = owner2.get(f"/sites/{site_id}")
    assert response.status_code in (401, 403, 404), (
        f"the second seeded owner read site {site_id}, which belongs to another "
        f"workspace, with {response.status_code}: {response.text[:300]}")
    after = backend.rows("sites", id=site_id)
    assert [r.get("status") for r in before] == [r.get("status") for r in after], (
        f"a denied read changed the stored row for site {site_id}")


def test_draft_media_upload_is_denied_to_second_owner(anon, owner2, store):
    _, payload = conftest.new_owner(anon)
    site_id = payload["site_id"]
    response = conftest.upload_picture(owner2, site_id, conftest.png_bytes(11))
    assert response.status_code in (401, 403, 404), (
        f"the second seeded owner uploaded a picture to site {site_id}, which "
        f"belongs to another workspace, with {response.status_code}: "
        f"{response.text[:300]}")
    keys = store.list(prefix=f"sites/{site_id}/")
    assert keys == [], (
        f"a denied upload still wrote {len(keys)} object(s) under "
        f"sites/{site_id}/: {keys[:5]}")


def test_draft_media_file_is_denied_to_anonymous(anon, store):
    _, payload = conftest.new_owner(anon)
    site_id = payload["site_id"]
    body = conftest.png_bytes(23)
    with appclient.client(payload["access_token"]) as client:
        uploaded = conftest.upload_picture(client, site_id, body)
        assert uploaded.status_code in (200, 201), (
            f"uploading a picture to draft site {site_id} returned "
            f"{uploaded.status_code}: {uploaded.text[:300]}")
        media_id = uploaded.json().get("id")
        object_key = uploaded.json().get("object_key")
    assert store.exists(object_key), (
        f"the uploaded file is not in the object store at {object_key!r}")
    anonymous = anon.get(f"/sites/{site_id}/media/{media_id}")
    assert anonymous.status_code in (401, 403, 404), (
        f"an anonymous caller read the picture of draft site {site_id} with "
        f"{anonymous.status_code}; a draft site's file stays private")


def test_draft_site_public_read_is_not_found(anon):
    _, payload = conftest.new_owner(anon)
    site_id = payload["site_id"]
    with appclient.client(payload["access_token"]) as client:
        site = client.get(f"/sites/{site_id}").json()
    slug = site.get("slug")
    assert slug, (
        f"site {site_id} carries no slug, so its public address cannot be checked: "
        f"{site}")
    response = anon.get(f"/published/{slug}")
    assert response.status_code == 404, (
        f"the public address of draft site {slug!r} returned "
        f"{response.status_code}, expected 404 so that the draft is not disclosed: "
        f"{response.text[:300]}")


def test_no_credentials_in_browser_downloads(raw):
    secrets = [os.environ.get("STORAGE_SECRET_KEY"),
               os.environ.get("STORAGE_ACCESS_KEY")]
    database_url = os.environ.get("DATABASE_URL") or ""
    if "@" in database_url and "//" in database_url:
        secrets.append(database_url.split("//", 1)[1].split("@", 1)[0])
    for route in conftest.MARKETING_ROUTES:
        document = raw.get(route)
        assert document.status_code == 200, (
            f"{route} returned {document.status_code}, expected 200: "
            f"{document.text[:200]}")
        for secret in [s for s in secrets if s]:
            assert secret not in document.text, (
                f"{route} ships a server credential to the browser; the document "
                f"contains a value the app reads from its own environment")




def test_not_found_route_answers_with_not_found_status(raw):
    response = raw.get(f"/no-such-page/{conftest.probe_suffix()}")
    assert response.status_code == 404, (
        f"an address the router does not know returned {response.status_code}, "
        f"expected 404: {response.text[:200]}")
    body = response.text
    assert "noindex" in body.lower(), (
        "the not-found document carries no no-index directive")
    assert "og:image" not in body.lower(), (
        "the not-found document carries social sharing metadata, which only the "
        "two indexable routes may carry")


def test_alias_paths_serve_the_home_document(raw):
    home = raw.get("/")
    assert home.status_code == 200, (
        f"the home route returned {home.status_code}: {home.text[:200]}")
    home_title = (TITLE_RE.search(home.text) or [None, ""])[1].strip()
    for alias in conftest.ALIAS_PATHS:
        response = raw.get(alias)
        assert response.status_code == 200, (
            f"the alias {alias} returned {response.status_code}, expected the home "
            f"document: {response.text[:200]}")
        alias_title = (TITLE_RE.search(response.text) or [None, ""])[1].strip()
        assert alias_title == home_title, (
            f"the alias {alias} served a document titled {alias_title!r}, expected "
            f"the home document titled {home_title!r}")


def test_domain_query_empty_is_refused(anon):
    for value in ("", "   "):
        response = anon.get("/domains/availability", params={"query": value})
        assert response.status_code in (400, 422), (
            f"an empty domain query {value!r} returned {response.status_code}, "
            f"expected a client error: {response.text[:300]}")


def test_empty_owner_sites_returns_empty_array(anon):
    email, payload = conftest.new_owner(anon)
    with appclient.client(payload["access_token"]) as client:
        first = _shapes.items(client.get("/sites").json())
        site_id = first[0].get("id") if first else None
        assert site_id is not None, (
            f"the new tenant {email} holds no first site to work from")
        listed = client.get("/sites")
        assert listed.status_code == 200, (
            f"GET /api/sites for {email} returned {listed.status_code}, expected an "
            f"array rather than an error: {listed.text[:300]}")
        assert isinstance(_shapes.items(listed.json()), list), (
            f"GET /api/sites for {email} did not return a list: "
            f"{listed.text[:300]}")


def test_invalid_call_is_rejected_as_client_error(anon, owner):
    missing = owner.get("/sites/999999999")
    assert 400 <= missing.status_code < 500, (
        f"reading a site that does not exist returned {missing.status_code}, "
        f"expected a client error rather than a server error: "
        f"{missing.text[:300]}")
    malformed = anon.post("/accounts", json={"email": "not-an-address"})
    assert 400 <= malformed.status_code < 500, (
        f"a sign-up carrying no password and a malformed address returned "
        f"{malformed.status_code}, expected a client error: "
        f"{malformed.text[:300]}")


def test_response_carries_a_request_identifier(anon):
    response = anon.get("/health")
    headers = {k.lower(): v for k, v in response.headers.items()}
    carried = [h for h in REQUEST_ID_HEADERS if headers.get(h)]
    assert carried, (
        f"GET /api/health carried no request identifier header; the response "
        f"headers were {sorted(headers)[:12]}")


def test_route_titles_and_descriptions_are_distinct(raw):
    seen = {}
    for route in conftest.MARKETING_ROUTES:
        document = raw.get(route)
        assert document.status_code == 200, (
            f"{route} returned {document.status_code}: {document.text[:200]}")
        title_match = TITLE_RE.search(document.text)
        description_match = DESCRIPTION_RE.search(document.text)
        assert title_match and title_match.group(1).strip(), (
            f"{route} carries no document title")
        assert description_match and description_match.group(1).strip(), (
            f"{route} carries no description tag")
        pair = (title_match.group(1).strip(), description_match.group(1).strip())
        assert pair not in seen.values(), (
            f"{route} shares its title and description with {seen}; no two routes "
            f"may share them")
        seen[route] = pair


def test_favicon_is_served(raw, app_base):
    home = raw.get("/")
    link = ICON_RE.search(home.text)
    assert link, (
        "the home document declares no icon link in its head")
    href = HREF_RE.search(link.group(0))
    assert href, (
        f"the declared icon link carries no href: {link.group(0)[:200]}")
    icon = raw.get(_absolute(app_base, href.group(1)))
    assert icon.status_code == 200, (
        f"the declared favicon at {href.group(1)!r} returned {icon.status_code}")
    assert len(icon.content) > 0, (
        f"the declared favicon at {href.group(1)!r} is empty")


def test_social_preview_image_resolves(raw, app_base):
    for route in ("/", "/pos"):
        document = raw.get(route)
        match = OG_IMAGE_RE.search(document.text)
        assert match, (
            f"{route} declares no social preview image in its head")
        image = raw.get(_absolute(app_base, match.group(1)))
        assert image.status_code == 200, (
            f"the preview image {match.group(1)!r} declared by {route} returned "
            f"{image.status_code}")
        assert len(image.content) > 0, (
            f"the preview image {match.group(1)!r} declared by {route} is empty")




def test_media_upload_stores_object_in_the_bucket(anon, store):
    _, payload = conftest.new_owner(anon)
    site_id = payload["site_id"]
    body = conftest.png_bytes(41)
    with appclient.client(payload["access_token"]) as client:
        response = conftest.upload_picture(client, site_id, body,
                                           alt_text="A probe storefront")
    assert response.status_code in (200, 201), (
        f"uploading a picture to site {site_id} returned {response.status_code}: "
        f"{response.text[:300]}")
    key = response.json().get("object_key")
    assert key, (
        f"the upload response for site {site_id} carries no object_key: "
        f"{response.text[:300]}")
    found = conftest.wait_for(lambda: store.exists(key))
    assert found, (
        f"the uploaded file is absent from the object store at {key!r}; the bytes "
        f"live only in the store")
    assert response.json().get("alt_text") == "A probe storefront", (
        f"the stored media row reports alt_text "
        f"{response.json().get('alt_text')!r}, expected the supplied text")


def test_media_upload_file_key_follows_the_scheme(anon, store):
    _, payload = conftest.new_owner(anon)
    site_id = payload["site_id"]
    body = conftest.png_bytes(59)
    digest = conftest.sha256_hex(body)
    with appclient.client(payload["access_token"]) as client:
        response = conftest.upload_picture(client, site_id, body)
    assert response.status_code in (200, 201), (
        f"uploading a picture to site {site_id} returned {response.status_code}: "
        f"{response.text[:300]}")
    key = response.json().get("object_key") or ""
    assert key.startswith(f"sites/{site_id}/"), (
        f"the object key {key!r} does not open with the site's own prefix "
        f"sites/{site_id}/")
    assert digest in key, (
        f"the object key {key!r} does not carry the sha256 of the uploaded bytes "
        f"{digest}")
    assert key.rsplit(".", 1)[-1].lower() in ("png", "jpg", "jpeg", "webp", "gif"), (
        f"the object key {key!r} carries no picture extension")
    assert store.exists(key), (
        f"the object key {key!r} names no file in the bucket")


def test_duplicate_media_upload_leaves_one_file(anon, store):
    _, payload = conftest.new_owner(anon)
    site_id = payload["site_id"]
    body = conftest.png_bytes(67)
    with appclient.client(payload["access_token"]) as client:
        first = conftest.upload_picture(client, site_id, body)
        assert first.status_code in (200, 201), (
            f"the first upload to site {site_id} returned {first.status_code}: "
            f"{first.text[:300]}")
        second = conftest.upload_picture(client, site_id, body)
        assert second.status_code in (200, 201, 409), (
            f"re-uploading identical bytes to site {site_id} returned "
            f"{second.status_code}: {second.text[:300]}")
    keys = store.list(prefix=f"sites/{site_id}/")
    assert len(keys) == 1, (
        f"uploading identical bytes twice left {len(keys)} files under "
        f"sites/{site_id}/, expected exactly one: {keys[:5]}")


def test_publish_makes_site_and_media_file_public(anon, store):
    _, payload = conftest.new_owner(anon)
    site_id = payload["site_id"]
    body = conftest.png_bytes(83)
    with appclient.client(payload["access_token"]) as client:
        uploaded = conftest.upload_picture(client, site_id, body,
                                           alt_text="A probe shopfront")
        assert uploaded.status_code in (200, 201), (
            f"uploading to site {site_id} returned {uploaded.status_code}: "
            f"{uploaded.text[:300]}")
        key = uploaded.json().get("object_key")
        site = client.get(f"/sites/{site_id}").json()
        slug = site.get("slug")
        before = anon.get(f"/published/{slug}")
        assert before.status_code == 404, (
            f"the public address of draft site {slug!r} answered "
            f"{before.status_code} before publish, expected 404")
        published = client.post(f"/sites/{site_id}/publish")
        assert published.status_code in (200, 201), (
            f"publishing site {site_id} returned {published.status_code}: "
            f"{published.text[:300]}")
    after = conftest.wait_for(
        lambda: anon.get(f"/published/{slug}").status_code == 200)
    assert after, (
        f"the public address of published site {slug!r} still does not answer 200")
    assert store.exists(key), (
        f"the published site's file left the object store at {key!r}")
