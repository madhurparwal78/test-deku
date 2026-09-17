"""The Vesper verifier: one module, every section and the declared db slot.

Sections, in order: core features, data integrity, authorization, edge cases.
Every literal asserted here is pinned in instruction.md.
"""

from __future__ import annotations

import os

import httpx

import conftest as C


def _get(path: str) -> httpx.Response:
    with C.anon() as client:
        return client.get(path)


def _page(route: str) -> httpx.Response:
    return httpx.get(f"{C.app_url()}{route}", timeout=C.TIMEOUT,
                     follow_redirects=True)


def test_app_contract_surfaces_are_present():
    """The health route answers, and the contract's own files and directories exist."""
    response = _get("/health")
    assert response.status_code == 200, (
        f"GET /api/health returned {response.status_code}, expected 200 once the "
        f"app holds a database connection: {C.excerpt(response)}"
    )
    readme = "/app/USER_README.md"
    assert os.path.isfile(readme), (
        f"{readme} does not exist; the deployment contract requires the seeded "
        f"logins to be written there"
    )
    body = open(readme, encoding="utf-8", errors="replace").read()
    for address in (C.CLIENT_EMAIL, C.CURATOR_EMAIL):
        assert address in body, (
            f"{readme} does not name the seeded account {address}; it carries "
            f"{len(body)} characters beginning {body[:120]!r}"
        )
    assert C.SEED_PASSWORD in body, (
        f"{readme} does not carry the seeded password {C.SEED_PASSWORD}; it "
        f"begins {body[:120]!r}"
    )
    for reserved in ("/app/.browser_screenshots", "/app/.downloads"):
        assert os.path.isdir(reserved), (
            f"{reserved} does not exist; the deployment contract reserves it at "
            f"the app root"
        )
    root = _page("/")
    assert root.status_code == 200, (
        f"GET / at {C.app_url()} returned {root.status_code}, expected 200 from "
        f"a production build served on the contract's port: {C.excerpt(root)}"
    )


def test_public_route_titles_are_distinct():
    """Every public route carries its own title and its own description."""
    titles = {}
    descriptions = {}
    for route in C.PUBLIC_ROUTES:
        response = _page(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}, expected 200: "
            f"{C.excerpt(response)}"
        )
        text = response.text
        start = text.find("<title")
        assert start != -1, f"GET {route} returned a document with no title element"
        open_end = text.find(">", start)
        close = text.find("</title>", open_end)
        title = text[open_end + 1:close].strip()
        assert title, f"GET {route} returned an empty title element"
        assert title not in titles, (
            f"GET {route} carries the title {title!r}, which {titles[title]!r} "
            f"already carries; no two public routes share a title"
        )
        titles[title] = route
        marker = 'name="description"'
        index = text.find(marker)
        assert index != -1, (
            f"GET {route} declares no meta description; every public route "
            f"carries its own"
        )
        tag_start = text.rfind("<", 0, index)
        tag_end = text.find(">", index)
        tag = text[tag_start:tag_end]
        assert tag not in descriptions, (
            f"GET {route} carries the same description tag as "
            f"{descriptions[tag]!r}; no two public routes share one"
        )
        descriptions[tag] = route
    assert C.HOME_TITLE in titles, (
        f"no public route carries the pinned home title {C.HOME_TITLE!r}; the "
        f"titles seen were {sorted(titles)}"
    )
    assert C.ARCHIVE_TITLE in titles, (
        f"no public route carries the pinned archive title {C.ARCHIVE_TITLE!r}; "
        f"the titles seen were {sorted(titles)}"
    )


def test_seeded_projects_are_persisted_rows_in_authored_order(backend):
    """Fifteen published projects come back as stored rows in their authored order."""
    rows = C.project_rows()
    assert len(rows) == C.PROJECT_COUNT, (
        f"GET /api/projects returned {len(rows)} projects, expected "
        f"{C.PROJECT_COUNT}: {[r.get('slug') for r in rows]}"
    )
    slugs = [row.get("slug") for row in rows]
    assert slugs == list(C.ARCHIVE_SLUGS), (
        f"GET /api/projects returned the order {slugs}, expected the authored "
        f"order {list(C.ARCHIVE_SLUGS)}; the archive is never re-sorted"
    )
    stored = backend.count("project")
    assert stored >= C.PROJECT_COUNT, (
        f"the project table holds {stored} rows, expected at least "
        f"{C.PROJECT_COUNT}; the served archive must come from PostgreSQL"
    )
    for row in rows:
        for field in ("id", "slug", "title", "subtitle", "categories"):
            assert field in row, (
                f"GET /api/projects returned a project without {field!r}: "
                f"{str(row)[:300]}"
            )


def test_category_filter_is_a_membership_test_over_stored_rows():
    """A project in two practice fields appears under both filters."""
    all_rows = C.project_rows()
    seen = {}
    for slug in C.PRACTICE_SLUGS:
        with C.anon() as client:
            response = client.get("/projects", params={"category": slug})
        assert response.status_code == 200, (
            f"GET /api/projects?category={slug} returned {response.status_code}, "
            f"expected 200: {C.excerpt(response)}"
        )
        rows = response.json()
        assert isinstance(rows, list), (
            f"GET /api/projects?category={slug} did not return a top-level JSON "
            f"array: {str(rows)[:300]}"
        )
        assert rows, (
            f"GET /api/projects?category={slug} returned nothing; every one of "
            f"the four practice fields has published members"
        )
        assert len(rows) < len(all_rows), (
            f"GET /api/projects?category={slug} returned all {len(rows)} "
            f"projects; a filter narrows the archive"
        )
        seen[slug] = {row.get("slug") for row in rows}
    for slug in C.MULTI_FIELD_SLUGS:
        fields = [field for field, members in seen.items() if slug in members]
        assert len(fields) >= 2, (
            f"the project {slug!r} appears under {fields}, expected at least two "
            f"practice fields; membership is a set test rather than an equality "
            f"test"
        )


def test_seed_rows_are_not_duplicated_on_a_second_read(backend):
    """The seed is idempotent, and it lives in the PostgreSQL the environment provides."""
    dsn = os.environ.get("DB_ADMIN_URL", "")
    assert "postgres" in dsn, (
        f"DB_ADMIN_URL is {dsn!r}; the declared db slot is the PostgreSQL the "
        f"environment already runs"
    )
    for table, expected in (("project", C.PROJECT_COUNT),
                            ("signal", C.SIGNAL_COUNT),
                            ("client_mark", C.CLIENT_MARK_COUNT),
                            ("award", C.AWARD_COUNT)):
        stored = backend.count(table)
        assert stored == expected, (
            f"the {table} table holds {stored} rows, expected exactly {expected}; "
            f"seeding must be idempotent so a restart duplicates no row"
        )
    categories = backend.rows("category")
    scopes = {row.get("scope") for row in categories}
    assert scopes == {"project", "signal"}, (
        f"the category table carries the scopes {sorted(scopes)}, expected "
        f"exactly 'project' and 'signal'"
    )
    first = C.project_rows()
    second = C.project_rows()
    assert [r.get("slug") for r in first] == [r.get("slug") for r in second], (
        f"two reads of GET /api/projects disagreed: {[r.get('slug') for r in first]} "
        f"then {[r.get('slug') for r in second]}"
    )


def test_unknown_category_value_is_treated_as_absent():
    """A category value outside the known slugs is ignored rather than refused."""
    with C.anon() as client:
        response = client.get("/projects", params={"category": "not-a-practice-field"})
    assert response.status_code == 200, (
        f"GET /api/projects?category=not-a-practice-field returned "
        f"{response.status_code}, expected 200 with the value treated as absent: "
        f"{C.excerpt(response)}"
    )
    rows = response.json()
    assert len(rows) == C.PROJECT_COUNT, (
        f"GET /api/projects with an unknown category returned {len(rows)} "
        f"projects, expected all {C.PROJECT_COUNT}"
    )


def test_project_detail_row_carries_intro_and_credits():
    """A project's own route carries its introduction and its credit list."""
    response = _get(f"/projects/{C.FIRST_PROJECT_SLUG}")
    assert response.status_code == 200, (
        f"GET /api/projects/{C.FIRST_PROJECT_SLUG} returned {response.status_code}, "
        f"expected 200: {C.excerpt(response)}"
    )
    body = response.json()
    row = body.get("project", body)
    for field in ("slug", "title", "intro", "credits", "categories"):
        assert field in row, (
            f"GET /api/projects/{C.FIRST_PROJECT_SLUG} returned no {field!r}: "
            f"{str(row)[:300]}"
        )
    assert row.get("credits"), (
        f"GET /api/projects/{C.FIRST_PROJECT_SLUG} returned an empty credit list; "
        f"a case study carries role and name pairs"
    )
    page = _page(f"/work/{C.FIRST_PROJECT_SLUG}")
    assert page.status_code == 200, (
        f"GET /work/{C.FIRST_PROJECT_SLUG} returned {page.status_code}, expected "
        f"200; the next project sits underneath the page: {C.excerpt(page)}"
    )


def test_unknown_project_slug_is_refused_as_not_found():
    """An unknown project slug renders the not-found screen rather than an error."""
    page = httpx.get(f"{C.app_url()}/work/no-such-project", timeout=C.TIMEOUT)
    assert page.status_code == 404, (
        f"GET /work/no-such-project returned {page.status_code}, expected 404: "
        f"{C.excerpt(page)}"
    )
    response = _get("/projects/no-such-project")
    assert response.status_code == 404, (
        f"GET /api/projects/no-such-project returned {response.status_code}, "
        f"expected 404: {C.excerpt(response)}"
    )


def test_seeded_signals_are_persisted_rows_newest_first(backend):
    """Ten published journal entries come back newest first, with their kinds."""
    response = _get("/signals")
    assert response.status_code == 200, (
        f"GET /api/signals returned {response.status_code}, expected 200: "
        f"{C.excerpt(response)}"
    )
    rows = response.json()
    assert isinstance(rows, list), (
        f"GET /api/signals did not return a top-level JSON array: {str(rows)[:300]}"
    )
    assert len(rows) == C.SIGNAL_COUNT, (
        f"GET /api/signals returned {len(rows)} entries, expected {C.SIGNAL_COUNT}: "
        f"{[r.get('slug') for r in rows]}"
    )
    assert [r.get("slug") for r in rows] == list(C.JOURNAL_SLUGS), (
        f"GET /api/signals returned {[r.get('slug') for r in rows]}, expected the "
        f"pinned order newest first {list(C.JOURNAL_SLUGS)}"
    )
    kinds = {row.get("kind") for row in rows}
    assert kinds <= set(C.SIGNAL_KINDS), (
        f"GET /api/signals returned the kinds {sorted(kinds)}, expected a subset "
        f"of {list(C.SIGNAL_KINDS)}"
    )
    stored = backend.count("signal")
    assert stored == C.SIGNAL_COUNT, (
        f"the signal table holds {stored} rows, expected {C.SIGNAL_COUNT}"
    )


def test_signal_detail_row_carries_body_and_related():
    """An entry's own route carries its body, its date and its related entries."""
    response = _get(f"/signals/{C.FIRST_SIGNAL_SLUG}")
    assert response.status_code == 200, (
        f"GET /api/signals/{C.FIRST_SIGNAL_SLUG} returned {response.status_code}, "
        f"expected 200: {C.excerpt(response)}"
    )
    body = response.json()
    row = body.get("signal", body)
    for field in ("slug", "title", "kind", "published_on", "body"):
        assert field in row, (
            f"GET /api/signals/{C.FIRST_SIGNAL_SLUG} returned no {field!r}: "
            f"{str(row)[:300]}"
        )
    related = row.get("related") or body.get("related") or []
    assert len(related) <= 3, (
        f"GET /api/signals/{C.FIRST_SIGNAL_SLUG} returned {len(related)} related "
        f"entries, expected at most three"
    )
    page = _page(f"/blog/{C.FIRST_SIGNAL_SLUG}")
    assert page.status_code == 200, (
        f"GET /blog/{C.FIRST_SIGNAL_SLUG} returned {page.status_code}, expected "
        f"200: {C.excerpt(page)}"
    )
    printed = page.text
    assert "/" in printed, (
        f"GET /blog/{C.FIRST_SIGNAL_SLUG} rendered no slash-separated date; every "
        f"date reads DD/MM/YY"
    )


def test_internal_links_on_public_routes_resolve():
    """Every internal link on every public route answers, and the headers are set."""
    seen = set()
    for route in C.PUBLIC_ROUTES:
        response = _page(route)
        assert response.status_code == 200, (
            f"GET {route} returned {response.status_code}, expected 200: "
            f"{C.excerpt(response)}"
        )
        headers = {k.lower(): v for k, v in response.headers.items()}
        assert "strict-transport-security" in headers, (
            f"GET {route} carries no strict transport policy; its headers are "
            f"{sorted(headers)}"
        )
        assert headers.get("x-content-type-options", "").lower() == "nosniff", (
            f"GET {route} carries x-content-type-options "
            f"{headers.get('x-content-type-options')!r}, expected 'nosniff'"
        )
        frame = headers.get("content-security-policy", "") + headers.get("x-frame-options", "")
        assert frame, (
            f"GET {route} refuses framing by no header at all; its headers are "
            f"{sorted(headers)}"
        )
        text = response.text
        cursor = 0
        while True:
            index = text.find('href="/', cursor)
            if index == -1:
                break
            cursor = index + 7
            end = text.find('"', cursor)
            target = text[index + 6:end]
            if target.startswith("//") or "#" in target:
                continue
            seen.add(target.split("?")[0])
    assert seen, "no public route rendered an internal link at all"
    for target in sorted(seen):
        linked = httpx.get(f"{C.app_url()}{target}", timeout=C.TIMEOUT,
                           follow_redirects=True)
        assert linked.status_code == 200, (
            f"the internal link {target!r} returned {linked.status_code}, "
            f"expected 200; every internal link on a public route resolves: "
            f"{C.excerpt(linked)}"
        )


def test_privacy_and_terms_pages_are_served():
    """The imprint and privacy page and the terms page are reachable and linked."""
    privacy = _page(C.PRIVACY_ROUTE)
    assert privacy.status_code == 200, (
        f"GET {C.PRIVACY_ROUTE} returned {privacy.status_code}, expected 200: "
        f"{C.excerpt(privacy)}"
    )
    terms = _page(C.TERMS_ROUTE)
    assert terms.status_code == 200, (
        f"GET {C.TERMS_ROUTE} returned {terms.status_code}, expected 200: "
        f"{C.excerpt(terms)}"
    )
    home = _page("/")
    assert C.PRIVACY_ROUTE in home.text, (
        f"GET / does not link {C.PRIVACY_ROUTE}; the footer's legal rule carries "
        f"it on every route with a footer"
    )
    assert C.TERMS_ROUTE in home.text, (
        f"GET / does not link {C.TERMS_ROUTE}; the footer's legal rule carries it"
    )
    sign_in_page = _page("/sign-in?mode=create")
    assert C.TERMS_ROUTE in sign_in_page.text, (
        f"GET /sign-in?mode=create does not link {C.TERMS_ROUTE}; the terms sit "
        f"beside the submit control"
    )


def test_not_found_route_answers_not_found_with_its_own_page():
    """A wrong address renders the studio's own screen on a real not-found status."""
    response = httpx.get(f"{C.app_url()}/no-such-address-at-all", timeout=C.TIMEOUT)
    assert response.status_code == 404, (
        f"GET /no-such-address-at-all returned {response.status_code}, expected "
        f"404 rather than a redirect to a page that answers as found: "
        f"{C.excerpt(response)}"
    )
    assert "Page not found" in response.text, (
        f"GET /no-such-address-at-all rendered no 'Page not found' line; its body "
        f"begins {response.text[:200]!r}"
    )
    assert "back home" in response.text.lower(), (
        f"GET /no-such-address-at-all offers no way home; its body begins "
        f"{response.text[:200]!r}"
    )


def test_newsletter_subscription_is_a_persisted_row(backend):
    """A subscribed address is stored, and the stored value is what was sent."""
    address = C.probe_email()
    with C.anon() as client:
        response = client.post("/newsletter", json={"email": address})
    assert response.status_code in (200, 201, 202), (
        f"POST /api/newsletter for {address} returned {response.status_code}, "
        f"expected acceptance: {C.excerpt(response)}"
    )
    stored = C.settle(lambda: backend.count("subscriber", email=address))
    assert stored == 1, (
        f"the subscriber table holds {stored} rows for {address}, expected exactly "
        f"one after a single subscribe"
    )


def test_newsletter_repeat_inside_the_hour_stores_one_row(backend):
    """A repeat subscribe for one address is accepted and stored only once."""
    address = C.probe_email()
    with C.anon() as client:
        first = client.post("/newsletter", json={"email": address})
        second = client.post("/newsletter", json={"email": address})
    assert first.status_code in (200, 201, 202), (
        f"POST /api/newsletter for {address} returned {first.status_code} on the "
        f"first call: {C.excerpt(first)}"
    )
    assert second.status_code in (200, 201, 202), (
        f"POST /api/newsletter for {address} returned {second.status_code} on the "
        f"repeat, expected the same acceptance so the answer reveals nothing: "
        f"{C.excerpt(second)}"
    )
    stored = C.settle(lambda: backend.count("subscriber", email=address))
    assert stored == 1, (
        f"the subscriber table holds {stored} rows for {address} after two "
        f"submissions inside the hour, expected exactly one"
    )


def test_reset_request_answers_identically_for_an_unknown_address(backend):
    """A reset request answers the same way whether or not the address exists."""
    known = C.CLIENT_EMAIL
    unknown = C.probe_email()
    with C.anon() as client:
        first = client.post("/auth/reset", json={"email": known})
        second = client.post("/auth/reset", json={"email": unknown})
    assert first.status_code == second.status_code, (
        f"POST /api/auth/reset answered {first.status_code} for a known address "
        f"and {second.status_code} for an unknown one; both must answer the same "
        f"or the form becomes an account-existence oracle"
    )
    assert first.status_code in (200, 202), (
        f"POST /api/auth/reset returned {first.status_code}, expected acceptance: "
        f"{C.excerpt(first)}"
    )
    assert first.text.strip() == second.text.strip(), (
        f"POST /api/auth/reset returned {C.excerpt(first)!r} for a known address "
        f"and {C.excerpt(second)!r} for an unknown one; the bodies must match"
    )
    sent = backend.rows("outbox_message", to_address=unknown)
    assert sent == [], (
        f"the outbox table holds {len(sent)} messages for {unknown}, which has no "
        f"account; nothing is sent for an address with no account"
    )
    tokens = backend.rows("reset_token")
    assert isinstance(tokens, list), (
        "the reset_token table is not readable; a reset link is a stored "
        "single-use token"
    )


def test_signup_stores_an_account_row_with_an_empty_reel(backend):
    """A new account is stored with its one reel, already in state empty."""
    address = C.probe_email()
    email, token = C.create_account(display_name="Probe Lead", email=address)
    stored = C.settle(lambda: backend.one("account", email=email))
    assert stored, (
        f"the account table holds no row for {email} after sign-up; the account "
        f"is a real row in PostgreSQL"
    )
    assert stored.get("display_name") == "Probe Lead", (
        f"the stored account for {email} carries display_name "
        f"{stored.get('display_name')!r}, expected 'Probe Lead'"
    )
    assert stored.get("role") == C.ROLE_CLIENT, (
        f"the stored account for {email} carries role {stored.get('role')!r}, "
        f"expected {C.ROLE_CLIENT!r}"
    )
    with C.bearer(token) as client:
        payload = C.read_reel(client)
    reel = payload.get("reel", payload)
    assert reel.get("state") == C.STATE_EMPTY, (
        f"GET /api/reel for a new account returned state {reel.get('state')!r}, "
        f"expected {C.STATE_EMPTY!r}"
    )
    assert C.reel_items(payload) == [], (
        f"GET /api/reel for a new account returned items; a reel is created empty"
    )
    for account in (C.CLIENT_EMAIL, C.CLIENT2_EMAIL, C.CLIENT3_EMAIL, C.CURATOR_EMAIL):
        row = backend.one("account", email=account)
        assert row, (
            f"the account table holds no seeded row for {account}; four accounts "
            f"are seeded"
        )
    curator_row = backend.one("account", email=C.CURATOR_EMAIL)
    assert curator_row.get("role") == C.ROLE_CURATOR, (
        f"the seeded {C.CURATOR_EMAIL} carries role {curator_row.get('role')!r}, "
        f"expected {C.ROLE_CURATOR!r}"
    )
    assert C.token_for(C.CLIENT_EMAIL), (
        f"the seeded password {C.SEED_PASSWORD} does not work at login for "
        f"{C.CLIENT_EMAIL}"
    )


def test_signup_refuses_an_already_registered_address():
    """A second sign-up for one address is refused in the pinned words."""
    with C.anon() as client:
        response = client.post("/auth/sign-up", json={
            "display_name": "Second Try",
            "email": C.CLIENT_EMAIL,
            "password": C.SEED_PASSWORD,
        })
    assert response.status_code in C.CLIENT_ERROR, (
        f"POST /api/auth/sign-up for the registered {C.CLIENT_EMAIL} returned "
        f"{response.status_code}, expected a client error: {C.excerpt(response)}"
    )
    assert C.REFUSAL_ALREADY_REGISTERED in response.text, (
        f"POST /api/auth/sign-up for a registered address did not say "
        f"{C.REFUSAL_ALREADY_REGISTERED!r}: {C.excerpt(response)}"
    )


def test_signin_refusal_names_neither_field():
    """A wrong password and an unknown address are refused identically."""
    wrong = C.sign_in(C.CLIENT_EMAIL, "not-the-seeded-password")
    unknown = C.sign_in(C.probe_email(), C.SEED_PASSWORD)
    assert wrong.status_code == unknown.status_code, (
        f"POST /api/auth/sign-in answered {wrong.status_code} for a wrong "
        f"password and {unknown.status_code} for an unknown address; the two "
        f"refusals must be indistinguishable"
    )
    assert wrong.status_code in C.DENIED, (
        f"POST /api/auth/sign-in with a wrong password returned "
        f"{wrong.status_code}, expected one of {C.DENIED}: {C.excerpt(wrong)}"
    )
    assert C.REFUSAL_SIGN_IN in wrong.text, (
        f"POST /api/auth/sign-in did not refuse with {C.REFUSAL_SIGN_IN!r}: "
        f"{C.excerpt(wrong)}"
    )
    assert wrong.text.strip() == unknown.text.strip(), (
        f"POST /api/auth/sign-in returned {C.excerpt(wrong)!r} for a wrong "
        f"password and {C.excerpt(unknown)!r} for an unknown address; the bodies "
        f"must match"
    )
    good = C.sign_in(C.CLIENT_EMAIL)
    assert good.status_code == 200, (
        f"POST /api/auth/sign-in with the seeded password returned "
        f"{good.status_code}, expected 200: {C.excerpt(good)}"
    )
    token = good.json().get("access_token")
    assert token, (
        f"POST /api/auth/sign-in returned 200 with no access_token: "
        f"{C.excerpt(good)}"
    )
    cookies = good.headers.get_list("set-cookie")
    assert cookies, (
        f"POST /api/auth/sign-in set no cookie; the session token is also set as "
        f"an HTTP-only, secure, same-site cookie on the same origin"
    )
    joined = " ".join(cookies).lower()
    assert "httponly" in joined, (
        f"the session cookie is not HTTP-only: {joined[:300]!r}"
    )
    assert "samesite" in joined, (
        f"the session cookie declares no same-site policy: {joined[:300]!r}"
    )
    with C.bearer(token) as client:
        me = client.get("/auth/me")
    assert me.status_code == 200, (
        f"GET /api/auth/me with the bearer token returned {me.status_code}, "
        f"expected 200; either credential authenticates: {C.excerpt(me)}"
    )


def test_session_identity_omits_the_password_hash(client_token, backend):
    """The identity route never returns a password, and the store never holds a plain one."""
    with C.bearer(client_token) as client:
        response = client.get("/auth/me")
    assert response.status_code == 200, (
        f"GET /api/auth/me returned {response.status_code}, expected 200: "
        f"{C.excerpt(response)}"
    )
    body = response.text
    assert C.SEED_PASSWORD not in body, (
        f"GET /api/auth/me returned the password in its body: {C.excerpt(response)}"
    )
    for field in ("password_hash", "passwordHash", "password"):
        assert field not in body, (
            f"GET /api/auth/me returned a {field!r} field: {C.excerpt(response)}"
        )
    row = backend.one("account", email=C.CLIENT_EMAIL)
    assert row, f"the account table holds no row for {C.CLIENT_EMAIL}"
    assert row.get("password_hash"), (
        f"the stored account for {C.CLIENT_EMAIL} carries no password_hash"
    )
    assert row["password_hash"] != C.SEED_PASSWORD, (
        f"the stored account for {C.CLIENT_EMAIL} carries the password in clear; "
        f"a password is stored only under a memory-hard hash"
    )
    sessions = backend.rows("session", limit=5)
    for session in sessions:
        assert "token_hash" in session, (
            f"a session row carries no token_hash: {str(session)[:300]}"
        )


def test_add_stores_a_reel_item_row_at_the_next_position(fresh_client, backend):
    """An add writes one item row at the next contiguous position."""
    payload = C.read_reel(fresh_client)
    reel = payload.get("reel", payload)
    reel_id = str(reel["id"])
    first = C.add_project(fresh_client, C.project_id_by_slug(C.FIRST_PROJECT_SLUG))
    assert first.status_code in C.OK_CREATED, (
        f"POST /api/reel/items returned {first.status_code}, expected one of "
        f"{C.OK_CREATED}: {C.excerpt(first)}"
    )
    second = C.add_project(fresh_client, C.project_id_by_slug(C.SECOND_PROJECT_SLUG))
    assert second.status_code in C.OK_CREATED, (
        f"POST /api/reel/items returned {second.status_code} on the second add: "
        f"{C.excerpt(second)}"
    )
    rows = C.settle(lambda: backend.rows("reel_item", reel_id=reel_id))
    positions = sorted(int(row["position"]) for row in rows)
    assert positions == [0, 1], (
        f"the reel_item table holds the positions {positions} for reel {reel_id}, "
        f"expected [0, 1]; positions are zero-based and contiguous"
    )
    after = C.read_reel(fresh_client)
    state = after.get("reel", after).get("state")
    assert state == C.STATE_DRAFT, (
        f"GET /api/reel returned state {state!r} after the first add, expected "
        f"{C.STATE_DRAFT!r}"
    )


def test_reorder_is_persisted_and_survives_a_fresh_read(fresh_client, backend):
    """The order the client left is the order a fresh read returns."""
    added = C.fill_reel(fresh_client, 3)
    payload = C.read_reel(fresh_client)
    reel_id = str(payload.get("reel", payload)["id"])
    before = [str(item["id"]) for item in C.reel_items(payload)]
    assert before == added, (
        f"GET /api/reel returned the add order {before}, expected {added}"
    )
    wanted = [added[2], added[0], added[1]]
    response = C.set_order(fresh_client, wanted)
    assert response.status_code == 200, (
        f"PUT /api/reel/order returned {response.status_code}, expected 200: "
        f"{C.excerpt(response)}"
    )
    fresh = C.read_reel(fresh_client)
    after = [str(item["id"]) for item in C.reel_items(fresh)]
    assert after == wanted, (
        f"GET /api/reel returned the order {after} after a reorder, expected the "
        f"client's own order {wanted}"
    )
    rows = backend.rows("reel_item", reel_id=reel_id)
    stored = {str(row["id"]): int(row["position"]) for row in rows}
    assert [stored[item] for item in wanted] == [0, 1, 2], (
        f"the reel_item table holds the positions {stored} for reel {reel_id}, "
        f"expected the client's order rewritten to 0, 1, 2; the order must come "
        f"back from PostgreSQL rather than from anything the page remembered"
    )


def test_remove_rewrites_the_stored_positions_contiguously(fresh_client, backend):
    """Removing an item leaves the remaining positions contiguous."""
    added = C.fill_reel(fresh_client, 3)
    payload = C.read_reel(fresh_client)
    reel_id = str(payload.get("reel", payload)["id"])
    response = fresh_client.delete(f"/reel/items/{added[0]}")
    assert response.status_code in (200, 204), (
        f"DELETE /api/reel/items/{added[0]} returned {response.status_code}, "
        f"expected 200 or 204: {C.excerpt(response)}"
    )
    rows = C.settle(lambda: backend.rows("reel_item", reel_id=reel_id))
    positions = sorted(int(row["position"]) for row in rows)
    assert positions == [0, 1], (
        f"the reel_item table holds the positions {positions} after a remove, "
        f"expected [0, 1] with no gap"
    )
    remaining = {str(row["id"]) for row in rows}
    assert remaining == {added[1], added[2]}, (
        f"the reel_item table holds {remaining} after removing {added[0]}, "
        f"expected {{{added[1]}, {added[2]}}}"
    )


def test_duplicate_project_in_one_reel_is_refused(fresh_client, backend):
    """One project never appears twice in one reel."""
    project_id = C.project_id_by_slug(C.FIRST_PROJECT_SLUG)
    first = C.add_project(fresh_client, project_id)
    assert first.status_code in C.OK_CREATED, (
        f"POST /api/reel/items returned {first.status_code} on the first add: "
        f"{C.excerpt(first)}"
    )
    again = C.add_project(fresh_client, project_id)
    assert again.status_code in C.CLIENT_ERROR, (
        f"POST /api/reel/items for the same project returned {again.status_code}, "
        f"expected a client error: {C.excerpt(again)}"
    )
    payload = C.read_reel(fresh_client)
    reel_id = str(payload.get("reel", payload)["id"])
    rows = backend.rows("reel_item", reel_id=reel_id)
    assert len(rows) == 1, (
        f"the reel_item table holds {len(rows)} rows after a duplicate add, "
        f"expected exactly one"
    )
    missing = C.add_project(fresh_client, "no-such-project-identifier")
    assert missing.status_code in C.CLIENT_ERROR, (
        f"POST /api/reel/items for an unknown project returned "
        f"{missing.status_code}, expected a client error: {C.excerpt(missing)}"
    )


def test_reel_never_stores_a_thirteenth_item(fresh_client, backend):
    """A reel refuses the thirteenth project in the pinned words and stores twelve."""
    C.fill_reel(fresh_client, C.REEL_CEILING)
    payload = C.read_reel(fresh_client)
    reel_id = str(payload.get("reel", payload)["id"])
    stored = backend.count("reel_item", reel_id=reel_id)
    assert stored == C.REEL_CEILING, (
        f"the reel_item table holds {stored} rows at the ceiling, expected "
        f"{C.REEL_CEILING}"
    )
    extra = C.add_project(fresh_client, C.project_id_by_slug("signal-box"))
    assert extra.status_code in C.CLIENT_ERROR, (
        f"POST /api/reel/items beyond the ceiling returned {extra.status_code}, "
        f"expected a client error: {C.excerpt(extra)}"
    )
    assert C.REFUSAL_CEILING in extra.text, (
        f"the ceiling refusal did not say {C.REFUSAL_CEILING!r}: "
        f"{C.excerpt(extra)}"
    )
    after = backend.count("reel_item", reel_id=reel_id)
    assert after == C.REEL_CEILING, (
        f"the reel_item table holds {after} rows after the refused add, expected "
        f"{C.REEL_CEILING}; a refused add writes nothing"
    )


def test_concurrent_reorder_has_exactly_one_whole_list_winner(fresh_client, backend):
    """Two orders arriving at once leave one whole list winning, with no gap."""
    added = C.fill_reel(fresh_client, 4)
    payload = C.read_reel(fresh_client)
    reel_id = str(payload.get("reel", payload)["id"])
    first = [added[3], added[2], added[1], added[0]]
    second = [added[1], added[0], added[3], added[2]]
    token = C.token_for(fresh_client.probe_email)
    with C.bearer(token) as other:
        responses = [C.set_order(fresh_client, first), C.set_order(other, second)]
    for index, response in enumerate(responses):
        assert response.status_code in (200, 409), (
            f"PUT /api/reel/order call {index} returned {response.status_code}, "
            f"expected 200 or a conflict: {C.excerpt(response)}"
        )
    rows = backend.rows("reel_item", reel_id=reel_id)
    positions = sorted(int(row["position"]) for row in rows)
    assert positions == [0, 1, 2, 3], (
        f"the reel_item table holds the positions {positions} after two "
        f"simultaneous reorders, expected [0, 1, 2, 3] with no gap and no "
        f"duplicate"
    )
    final = {int(row["position"]): str(row["id"]) for row in rows}
    ordered = [final[index] for index in range(4)]
    assert ordered in (first, second), (
        f"the stored order is {ordered}, which is neither whole list the two "
        f"sessions sent ({first} and {second}); one list wins outright rather "
        f"than the two interleaving"
    )


def test_concurrent_add_at_the_ceiling_has_exactly_one_winner(fresh_client, backend):
    """Two adds racing for the last seat leave exactly twelve items."""
    C.fill_reel(fresh_client, C.REEL_CEILING - 1)
    payload = C.read_reel(fresh_client)
    reel_id = str(payload.get("reel", payload)["id"])
    token = C.token_for(fresh_client.probe_email)
    left = C.project_id_by_slug("signal-box")
    right = C.project_id_by_slug("quiet-mile")
    with C.bearer(token) as other:
        responses = [C.add_project(fresh_client, left), C.add_project(other, right)]
    accepted = [r for r in responses if r.status_code in C.OK_CREATED]
    assert len(accepted) >= 1, (
        f"neither simultaneous add succeeded at the last seat; the two returned "
        f"{[r.status_code for r in responses]}"
    )
    stored = backend.count("reel_item", reel_id=reel_id)
    assert stored <= C.REEL_CEILING, (
        f"the reel_item table holds {stored} rows after two simultaneous adds at "
        f"the last seat, expected at most {C.REEL_CEILING}"
    )
    rows = backend.rows("reel_item", reel_id=reel_id)
    positions = sorted(int(row["position"]) for row in rows)
    assert positions == list(range(len(rows))), (
        f"the reel_item table holds the positions {positions}, expected the "
        f"contiguous run 0..{len(rows) - 1}"
    )


def test_note_and_brief_are_stored_verbatim(fresh_client, backend):
    """A note and a brief are stored exactly as typed."""
    added = C.fill_reel(fresh_client, 2)
    payload = C.read_reel(fresh_client)
    reel_id = str(payload.get("reel", payload)["id"])
    note = "This is the one"
    brief = "A launch film for a new product"
    title = "Pitch shortlist"
    response = fresh_client.patch(f"/reel/items/{added[0]}", json={"note": note})
    assert response.status_code == 200, (
        f"PATCH /api/reel/items/{added[0]} returned {response.status_code}, "
        f"expected 200: {C.excerpt(response)}"
    )
    patched = fresh_client.patch("/reel", json={"title": title, "brief": brief})
    assert patched.status_code == 200, (
        f"PATCH /api/reel returned {patched.status_code}, expected 200: "
        f"{C.excerpt(patched)}"
    )
    reel_row = C.settle(lambda: backend.one("reel", id=reel_id))
    assert reel_row.get("title") == title, (
        f"the reel row carries the title {reel_row.get('title')!r}, expected "
        f"{title!r}"
    )
    assert reel_row.get("brief") == brief, (
        f"the reel row carries the brief {reel_row.get('brief')!r}, expected "
        f"{brief!r}"
    )
    assert int(reel_row.get("version", 1)) >= 1, (
        f"the reel row carries version {reel_row.get('version')!r}, expected a "
        f"one-based integer"
    )
    item_row = backend.one("reel_item", id=added[0])
    assert item_row.get("note") == note, (
        f"the reel_item row carries the note {item_row.get('note')!r}, expected "
        f"{note!r}"
    )


def test_hostile_string_is_stored_and_returned_verbatim(fresh_client, backend):
    """A booby-trapped string comes back as the characters that were typed."""
    added = C.fill_reel(fresh_client, 1)
    hostile = "<img src=x onerror=alert(1)>"
    response = fresh_client.patch(f"/reel/items/{added[0]}", json={"note": hostile})
    assert response.status_code == 200, (
        f"PATCH /api/reel/items/{added[0]} with a hostile note returned "
        f"{response.status_code}, expected 200: {C.excerpt(response)}"
    )
    stored = C.settle(lambda: backend.one("reel_item", id=added[0]))
    assert stored.get("note") == hostile, (
        f"the reel_item row carries the note {stored.get('note')!r}, expected the "
        f"literal characters {hostile!r}; nothing is stripped and nothing is "
        f"rewritten"
    )
    payload = C.read_reel(fresh_client)
    notes = [item.get("note") for item in C.reel_items(payload)]
    assert hostile in notes, (
        f"GET /api/reel returned the notes {notes}, expected the literal "
        f"{hostile!r} unchanged"
    )


def test_event_log_rows_carry_no_typed_text(fresh_client, curator, backend):
    """Views and events are recorded, and nothing anybody typed is among them."""
    added = C.fill_reel(fresh_client, 1)
    secret = f"brief-{os.urandom(6).hex()}"
    patched = fresh_client.patch("/reel", json={"brief": secret})
    assert patched.status_code == 200, (
        f"PATCH /api/reel returned {patched.status_code}, expected 200: "
        f"{C.excerpt(patched)}"
    )
    _page("/")
    rows = C.settle(lambda: backend.rows("event_log", limit=200))
    assert rows, (
        "the event_log table is empty; the product records its own page views "
        "and the named events"
    )
    names = {row.get("name") for row in rows}
    assert "route_view" in names, (
        f"the event_log table carries the names {sorted(n for n in names if n)}, "
        f"expected 'route_view' among them"
    )
    blob = " ".join(str(row.get("properties")) for row in rows)
    assert secret not in blob, (
        f"the event_log table carries the brief text {secret!r}; nothing anybody "
        f"typed is ever recorded"
    )
    assert fresh_client.probe_email not in blob, (
        f"the event_log table carries the address {fresh_client.probe_email}; no "
        f"recorded event carries an address"
    )
    assert added, "the reel add under test wrote no item"


def test_send_stores_a_snapshot_the_live_reel_cannot_change(fresh_client, curator, backend):
    """A send freezes a snapshot, and later edits do not change what the studio reads."""
    added = C.fill_reel(fresh_client, 3)
    fresh_client.patch("/reel", json={"title": "Pitch shortlist",
                                      "brief": "A launch film for a new product"})
    fresh_client.patch(f"/reel/items/{added[0]}", json={"note": "This is the one"})
    wanted = [added[2], added[0], added[1]]
    C.set_order(fresh_client, wanted)
    sent = fresh_client.post("/reel/send")
    assert sent.status_code == 200, (
        f"POST /api/reel/send returned {sent.status_code}, expected 200: "
        f"{C.excerpt(sent)}"
    )
    payload = C.read_reel(fresh_client)
    reel = payload.get("reel", payload)
    reel_id = str(reel["id"])
    assert reel.get("state") == C.STATE_SENT, (
        f"GET /api/reel returned state {reel.get('state')!r} after a send, "
        f"expected {C.STATE_SENT!r}"
    )
    assert reel.get("sent_at"), (
        f"GET /api/reel returned no sent_at after a send: {str(reel)[:300]}"
    )
    snapshots = C.settle(lambda: backend.rows("reel_snapshot", reel_id=reel_id))
    assert snapshots, (
        f"the reel_snapshot table holds no row for reel {reel_id} after a send; "
        f"the studio reads a frozen snapshot rather than the live reel"
    )
    queue = curator.get("/studio/reels")
    assert queue.status_code == 200, (
        f"GET /api/studio/reels as the curator returned {queue.status_code}, "
        f"expected 200: {C.excerpt(queue)}"
    )
    rows = queue.json()
    rows = rows if isinstance(rows, list) else rows.get("reels", [])
    match = [row for row in rows if str(row.get("id")) == reel_id]
    assert match, (
        f"the studio queue does not carry the reel {reel_id} that was just sent; "
        f"it carries {[str(r.get('id')) for r in rows][:10]}"
    )
    read = curator.get(f"/studio/reels/{reel_id}")
    assert read.status_code == 200, (
        f"GET /api/studio/reels/{reel_id} returned {read.status_code}, expected "
        f"200: {C.excerpt(read)}"
    )
    body = read.json()
    order = [str(item["id"]) for item in body.get("items", [])]
    assert order == wanted, (
        f"the studio read the order {order}, expected the client's own order "
        f"{wanted}"
    )
    notes = [item.get("note") for item in body.get("items", [])]
    assert "This is the one" in notes, (
        f"the studio read the notes {notes}, expected the client's own note"
    )


def test_transactional_messages_are_stored_outbox_rows(fresh_client, backend):
    """Account creation and a send write the messages the brief names, to the right places."""
    welcome = C.settle(
        lambda: backend.rows("outbox_message", to_address=fresh_client.probe_email))
    assert welcome, (
        f"the outbox table holds no message for {fresh_client.probe_email} after "
        f"account creation; a welcome message is written once"
    )
    subjects = [row.get("subject") for row in welcome]
    assert C.WELCOME_SUBJECT in subjects, (
        f"the outbox carries the subjects {subjects} for the new account, "
        f"expected {C.WELCOME_SUBJECT!r} among them"
    )
    C.fill_reel(fresh_client, 1)
    fresh_client.patch("/reel", json={"title": "Pitch shortlist"})
    sent = fresh_client.post("/reel/send")
    assert sent.status_code == 200, (
        f"POST /api/reel/send returned {sent.status_code}, expected 200: "
        f"{C.excerpt(sent)}"
    )
    to_client = C.settle(lambda: [
        row for row in backend.rows("outbox_message",
                                    to_address=fresh_client.probe_email)
        if row.get("subject") == C.CLIENT_SEND_SUBJECT])
    assert to_client, (
        f"the outbox holds no {C.CLIENT_SEND_SUBJECT!r} message for "
        f"{fresh_client.probe_email} after a send"
    )
    to_studio = C.settle(lambda: [
        row for row in backend.rows("outbox_message", to_address=C.STUDIO_ADDRESS)
        if str(row.get("subject", "")).startswith(C.STUDIO_SEND_SUBJECT_PREFIX)])
    assert to_studio, (
        f"the outbox holds no message to {C.STUDIO_ADDRESS} whose subject begins "
        f"{C.STUDIO_SEND_SUBJECT_PREFIX!r} after a send"
    )
    for row in to_studio:
        assert "This is the one" not in str(row.get("body")), (
            f"the studio notice carries note text: {str(row.get('body'))[:300]}"
        )


def test_queue_pages_by_cursor_without_repeating_a_row(curator):
    """The studio queue hands out a cursor rather than a page number."""
    response = curator.get("/studio/reels")
    assert response.status_code == 200, (
        f"GET /api/studio/reels returned {response.status_code}, expected 200: "
        f"{C.excerpt(response)}"
    )
    body = response.json()
    rows = body if isinstance(body, list) else body.get("reels", [])
    assert rows, (
        "GET /api/studio/reels returned nothing; one reel is seeded already sent"
    )
    for row in rows:
        for field in ("id", "title", "sent_at"):
            assert field in row, (
                f"a queue row carries no {field!r}: {str(row)[:300]}"
            )
    first_page = curator.get("/studio/reels", params={"cursor": ""})
    assert first_page.status_code == 200, (
        f"GET /api/studio/reels?cursor= returned {first_page.status_code}, "
        f"expected 200: {C.excerpt(first_page)}"
    )
    ids = [str(row.get("id")) for row in rows]
    assert len(ids) == len(set(ids)), (
        f"the studio queue repeated a row: {ids}"
    )
    drafts = [row for row in rows if row.get("state") == C.STATE_DRAFT]
    assert drafts == [], (
        f"the studio queue carries {len(drafts)} reels still in state "
        f"{C.STATE_DRAFT!r}; only a sent reel reaches the queue"
    )


def test_reopen_discards_the_stored_snapshot_and_clears_sent_at(fresh_client, backend):
    """Reopening a sent reel returns it to draft and drops it from the queue."""
    C.fill_reel(fresh_client, 2)
    fresh_client.patch("/reel", json={"title": "Pitch shortlist"})
    sent = fresh_client.post("/reel/send")
    assert sent.status_code == 200, (
        f"POST /api/reel/send returned {sent.status_code}, expected 200: "
        f"{C.excerpt(sent)}"
    )
    reopened = fresh_client.post("/reel/reopen")
    assert reopened.status_code == 200, (
        f"POST /api/reel/reopen returned {reopened.status_code}, expected 200: "
        f"{C.excerpt(reopened)}"
    )
    payload = C.read_reel(fresh_client)
    reel = payload.get("reel", payload)
    reel_id = str(reel["id"])
    assert reel.get("state") == C.STATE_DRAFT, (
        f"GET /api/reel returned state {reel.get('state')!r} after a reopen, "
        f"expected {C.STATE_DRAFT!r}"
    )
    assert not reel.get("sent_at"), (
        f"GET /api/reel still carries sent_at {reel.get('sent_at')!r} after a "
        f"reopen; the sent date is cleared"
    )
    snapshots = backend.rows("reel_snapshot", reel_id=reel_id)
    assert snapshots == [], (
        f"the reel_snapshot table still holds {len(snapshots)} rows for reel "
        f"{reel_id} after a reopen; the snapshot is discarded"
    )


def test_answered_reel_cannot_be_reopened(fresh_client, curator, backend):
    """A curator marks a reel answered, and the owner can no longer reopen it."""
    C.fill_reel(fresh_client, 2)
    fresh_client.patch("/reel", json={"title": "Pitch shortlist"})
    fresh_client.post("/reel/send")
    payload = C.read_reel(fresh_client)
    reel_id = str(payload.get("reel", payload)["id"])
    answered = curator.post(f"/studio/reels/{reel_id}/answer")
    assert answered.status_code == 200, (
        f"POST /api/studio/reels/{reel_id}/answer returned "
        f"{answered.status_code}, expected 200: {C.excerpt(answered)}"
    )
    row = C.settle(lambda: backend.one("reel", id=reel_id))
    assert row.get("state") == C.STATE_ANSWERED, (
        f"the reel row carries state {row.get('state')!r} after the curator "
        f"answered it, expected {C.STATE_ANSWERED!r}"
    )
    assert row.get("answered_at"), (
        f"the reel row carries no answered_at after being marked answered: "
        f"{str(row)[:300]}"
    )
    refused = fresh_client.post("/reel/reopen")
    assert refused.status_code in C.CLIENT_ERROR, (
        f"POST /api/reel/reopen on an answered reel returned "
        f"{refused.status_code}, expected a client error: {C.excerpt(refused)}"
    )
    after = backend.one("reel", id=reel_id)
    assert after.get("state") == C.STATE_ANSWERED, (
        f"the reel row moved to {after.get('state')!r} after a refused reopen, "
        f"expected to stay {C.STATE_ANSWERED!r}"
    )


def test_anonymous_reel_write_is_denied(backend, anonymous):
    """A caller with no session writes nothing to any reel."""
    before = backend.count("reel_item")
    calls = [
        ("POST /api/reel/items", anonymous.post("/reel/items", json={"project_id": "x"})),
        ("PUT /api/reel/order", anonymous.put("/reel/order", json={"order": []})),
        ("POST /api/reel/send", anonymous.post("/reel/send")),
        ("GET /api/reel", anonymous.get("/reel")),
    ]
    for label, response in calls:
        assert response.status_code in C.DENIED, (
            f"{label} with no session returned {response.status_code}, expected "
            f"one of {C.DENIED}: {C.excerpt(response)}"
        )
    after = backend.count("reel_item")
    assert after == before, (
        f"the reel_item table moved from {before} to {after} rows after four "
        f"anonymous calls; a denied request mutates nothing"
    )


def test_client_reading_the_studio_queue_is_forbidden(client_token, backend):
    """A client session is refused at every studio path, and nothing changes."""
    reels = backend.rows("reel", state=C.STATE_SENT, limit=1)
    assert reels, "no reel is seeded in state sent; the queue is not empty on a first run"
    reel_id = str(reels[0]["id"])
    before = backend.one("reel", id=reel_id)
    with C.bearer(client_token) as client:
        queue = client.get("/studio/reels")
        read = client.get(f"/studio/reels/{reel_id}")
        answer = client.post(f"/studio/reels/{reel_id}/answer")
    for label, response in (("GET /api/studio/reels", queue),
                            (f"GET /api/studio/reels/{reel_id}", read),
                            (f"POST /api/studio/reels/{reel_id}/answer", answer)):
        assert response.status_code in C.DENIED, (
            f"{label} from a client session returned {response.status_code}, "
            f"expected one of {C.DENIED}: {C.excerpt(response)}"
        )
    after = backend.one("reel", id=reel_id)
    assert after.get("state") == before.get("state"), (
        f"the reel {reel_id} moved from state {before.get('state')!r} to "
        f"{after.get('state')!r} after a refused curator-only call; the protected "
        f"state is unchanged"
    )
    assert after.get("answered_at") == before.get("answered_at"), (
        f"the reel {reel_id} gained an answered_at from a refused call"
    )


def test_client_cannot_read_another_clients_reel(client_token, backend):
    """A client reads their own reel and no other, whatever address is asked for."""
    other = backend.one("account", email=C.CLIENT2_EMAIL)
    assert other, f"the account table holds no row for {C.CLIENT2_EMAIL}"
    other_reel = backend.one("reel", account_id=str(other["id"]))
    assert other_reel, f"the reel table holds no reel for {C.CLIENT2_EMAIL}"
    with C.bearer(client_token) as client:
        mine = C.read_reel(client)
        stolen = client.get(f"/reel/{other_reel['id']}")
        studio = client.get(f"/studio/reels/{other_reel['id']}")
    assert str(mine.get("reel", mine)["id"]) != str(other_reel["id"]), (
        f"GET /api/reel returned another account's reel {other_reel['id']}; the "
        f"reel is resolved from the session"
    )
    assert stolen.status_code in (401, 403, 404), (
        f"GET /api/reel/{other_reel['id']} returned {stolen.status_code}, expected "
        f"a refusal or a not-found: {C.excerpt(stolen)}"
    )
    assert studio.status_code in C.DENIED, (
        f"GET /api/studio/reels/{other_reel['id']} from a client session returned "
        f"{studio.status_code}, expected one of {C.DENIED}: {C.excerpt(studio)}"
    )


def test_curator_reading_a_draft_reel_is_refused_as_not_found(curator, backend):
    """A draft reel reads as not found to the studio, never as a refusal."""
    drafts = backend.rows("reel", state=C.STATE_DRAFT, limit=1)
    assert drafts, (
        f"no reel is seeded in state {C.STATE_DRAFT!r}; one seeded client opens "
        f"with a draft reel"
    )
    reel_id = str(drafts[0]["id"])
    response = curator.get(f"/studio/reels/{reel_id}")
    assert response.status_code == 404, (
        f"GET /api/studio/reels/{reel_id} for a draft reel returned "
        f"{response.status_code}, expected 404; a refusal would confirm the draft "
        f"exists: {C.excerpt(response)}"
    )
    answer = curator.post(f"/studio/reels/{reel_id}/answer")
    assert answer.status_code in (404, 409, 422), (
        f"POST /api/studio/reels/{reel_id}/answer for a draft reel returned "
        f"{answer.status_code}, expected a not-found or a conflict: "
        f"{C.excerpt(answer)}"
    )
    after = backend.one("reel", id=reel_id)
    assert after.get("state") == C.STATE_DRAFT, (
        f"the draft reel {reel_id} moved to {after.get('state')!r} after a "
        f"curator call"
    )


def test_curator_cannot_delete_a_clients_reel(curator, backend):
    """A curator deletes nothing, and account deletion belongs to its owner."""
    reels = backend.rows("reel", state=C.STATE_SENT, limit=1)
    assert reels, "no reel is seeded in state sent"
    reel_id = str(reels[0]["id"])
    before = backend.count("reel", id=reel_id)
    deleted = curator.delete(f"/studio/reels/{reel_id}")
    assert deleted.status_code in C.CLIENT_ERROR, (
        f"DELETE /api/studio/reels/{reel_id} returned {deleted.status_code}, "
        f"expected a client error; the person who wrote a reel owns it: "
        f"{C.excerpt(deleted)}"
    )
    after = backend.count("reel", id=reel_id)
    assert after == before, (
        f"the reel table moved from {before} to {after} rows for {reel_id} after "
        f"a curator delete"
    )
    edit = curator.patch(f"/studio/reels/{reel_id}", json={"title": "Renamed"})
    assert edit.status_code in C.CLIENT_ERROR, (
        f"PATCH /api/studio/reels/{reel_id} returned {edit.status_code}, expected "
        f"a client error; a curator edits nothing a client wrote: "
        f"{C.excerpt(edit)}"
    )


def test_role_is_never_taken_from_the_request_body(backend):
    """An account cannot name its own role, and no route grants the curator role."""
    address = C.probe_email()
    with C.anon() as client:
        response = client.post("/auth/sign-up", json={
            "display_name": "Role Climber",
            "email": address,
            "password": C.SEED_PASSWORD,
            "role": C.ROLE_CURATOR,
        })
    assert response.status_code in C.OK_CREATED or response.status_code in C.CLIENT_ERROR, (
        f"POST /api/auth/sign-up carrying a role returned {response.status_code}: "
        f"{C.excerpt(response)}"
    )
    if response.status_code in C.OK_CREATED:
        row = C.settle(lambda: backend.one("account", email=address))
        assert row.get("role") == C.ROLE_CLIENT, (
            f"the stored account for {address} carries role {row.get('role')!r} "
            f"after asking for {C.ROLE_CURATOR!r}; the role is never read from "
            f"the request body"
        )
        token = C.token_for(address)
        with C.bearer(token) as climber:
            queue = climber.get("/studio/reels")
        assert queue.status_code in C.DENIED, (
            f"GET /api/studio/reels from an account that asked for the curator "
            f"role returned {queue.status_code}, expected one of {C.DENIED}: "
            f"{C.excerpt(queue)}"
        )


def test_revoked_session_is_denied_and_changes_no_row(backend):
    """A revoked session writes nothing and reads nothing."""
    email, token = C.create_account()
    with C.bearer(token) as client:
        first = client.get("/reel")
        assert first.status_code == 200, (
            f"GET /api/reel with a fresh session returned {first.status_code}, "
            f"expected 200: {C.excerpt(first)}"
        )
        signed_out = client.post("/auth/sign-out")
    assert signed_out.status_code in (200, 204), (
        f"POST /api/auth/sign-out returned {signed_out.status_code}, expected 200 "
        f"or 204: {C.excerpt(signed_out)}"
    )
    before = backend.count("reel_item")
    with C.bearer(token) as stale:
        read = stale.get("/reel")
        write = stale.post("/reel/items", json={"project_id": "x"})
    assert read.status_code in C.DENIED, (
        f"GET /api/reel with a revoked session returned {read.status_code}, "
        f"expected one of {C.DENIED}: {C.excerpt(read)}"
    )
    assert write.status_code in C.DENIED, (
        f"POST /api/reel/items with a revoked session returned "
        f"{write.status_code}, expected one of {C.DENIED}: {C.excerpt(write)}"
    )
    after = backend.count("reel_item")
    assert after == before, (
        f"the reel_item table moved from {before} to {after} rows after a "
        f"revoked-session write"
    )
    assert email, "the probe account under test has no address"


def test_signout_revokes_every_stored_session_row(backend):
    """Signing out on one device signs the account out everywhere."""
    email, first_token = C.create_account()
    second_token = C.token_for(email)
    assert first_token != second_token or first_token, (
        f"two sign-ins for {email} produced no usable token"
    )
    with C.bearer(second_token) as second:
        out = second.post("/auth/sign-out")
    assert out.status_code in (200, 204), (
        f"POST /api/auth/sign-out returned {out.status_code}: {C.excerpt(out)}"
    )
    with C.bearer(first_token) as first:
        response = first.get("/reel")
    assert response.status_code in C.DENIED, (
        f"GET /api/reel with the other session's token returned "
        f"{response.status_code} after signing out, expected one of {C.DENIED}; "
        f"signing out anywhere signs the account out everywhere: "
        f"{C.excerpt(response)}"
    )
    account = backend.one("account", email=email)
    live = [row for row in backend.rows("session", account_id=str(account["id"]))
            if not row.get("revoked_at")]
    assert live == [], (
        f"the session table still holds {len(live)} live rows for {email} after "
        f"a sign-out"
    )


def test_next_parameter_refuses_a_protocol_relative_path():
    """A next value that is not a single-slash path is replaced by the home route."""
    for hostile in ("//evil.example.com", "https://evil.example.com", "evil"):
        response = httpx.get(f"{C.app_url()}/sign-in", params={"next": hostile},
                             timeout=C.TIMEOUT, follow_redirects=False)
        assert response.status_code in (200, 302, 303), (
            f"GET /sign-in?next={hostile} returned {response.status_code}: "
            f"{C.excerpt(response)}"
        )
        location = response.headers.get("location", "")
        assert not location.startswith("//"), (
            f"GET /sign-in?next={hostile} redirected to {location!r}; a next "
            f"value must begin with one slash and never two"
        )
        assert "evil.example.com" not in response.text, (
            f"GET /sign-in?next={hostile} carried the hostile destination into "
            f"its own body: {C.excerpt(response)}"
        )


def test_send_validation_stops_at_the_first_failure(fresh_client, backend):
    """An empty reel is refused first, a blank title next, and nothing is written."""
    empty = fresh_client.post("/reel/send")
    assert empty.status_code in C.REFUSED, (
        f"POST /api/reel/send on an empty reel returned {empty.status_code}, "
        f"expected a client error rather than a server error: {C.excerpt(empty)}"
    )
    assert empty.status_code < 500, (
        f"POST /api/reel/send on an empty reel returned {empty.status_code}; a "
        f"rejection is never a 5xx"
    )
    assert C.REFUSAL_EMPTY_REEL in empty.text, (
        f"the empty-reel refusal did not say {C.REFUSAL_EMPTY_REEL!r}: "
        f"{C.excerpt(empty)}"
    )
    C.fill_reel(fresh_client, 1)
    blanked = fresh_client.patch("/reel", json={"title": ""})
    assert blanked.status_code in (200, 400, 422), (
        f"PATCH /api/reel with a blank title returned {blanked.status_code}: "
        f"{C.excerpt(blanked)}"
    )
    refused = fresh_client.post("/reel/send")
    assert refused.status_code in C.REFUSED, (
        f"POST /api/reel/send with a blank title returned {refused.status_code}, "
        f"expected a client error: {C.excerpt(refused)}"
    )
    assert C.REFUSAL_NO_TITLE in refused.text, (
        f"the blank-title refusal did not say {C.REFUSAL_NO_TITLE!r}: "
        f"{C.excerpt(refused)}"
    )
    payload = C.read_reel(fresh_client)
    state = payload.get("reel", payload).get("state")
    assert state == C.STATE_DRAFT, (
        f"GET /api/reel returned state {state!r} after two refused sends, "
        f"expected {C.STATE_DRAFT!r}"
    )


def test_send_against_a_sent_reel_is_refused(fresh_client, backend):
    """A second send is refused as already sent, and the reel stays sent."""
    C.fill_reel(fresh_client, 1)
    fresh_client.patch("/reel", json={"title": "Pitch shortlist"})
    first = fresh_client.post("/reel/send")
    assert first.status_code == 200, (
        f"POST /api/reel/send returned {first.status_code}, expected 200: "
        f"{C.excerpt(first)}"
    )
    second = fresh_client.post("/reel/send")
    assert second.status_code in C.REFUSED, (
        f"POST /api/reel/send on a sent reel returned {second.status_code}, "
        f"expected a conflict rather than a second send: {C.excerpt(second)}"
    )
    assert C.REFUSAL_ALREADY_SENT in second.text, (
        f"the already-sent refusal did not say {C.REFUSAL_ALREADY_SENT!r}: "
        f"{C.excerpt(second)}"
    )
    write = fresh_client.patch("/reel", json={"title": "Renamed after sending"})
    assert write.status_code in C.REFUSED, (
        f"PATCH /api/reel on a sent reel returned {write.status_code}, expected a "
        f"conflict; a sent reel is read-only: {C.excerpt(write)}"
    )
    payload = C.read_reel(fresh_client)
    reel = payload.get("reel", payload)
    assert reel.get("state") == C.STATE_SENT, (
        f"GET /api/reel returned state {reel.get('state')!r} after a refused "
        f"second send, expected {C.STATE_SENT!r}"
    )


def test_send_naming_a_withdrawn_project_is_refused(fresh_client, backend):
    """A project withdrawn between an add and a send blocks the send in its own words."""
    added = C.fill_reel(fresh_client, 2)
    fresh_client.patch("/reel", json={"title": "Pitch shortlist"})
    payload = C.read_reel(fresh_client)
    reel_id = str(payload.get("reel", payload)["id"])
    rows = backend.rows("reel_item", reel_id=reel_id)
    project_ids = {str(row["project_id"]) for row in rows}
    assert project_ids, f"the reel {reel_id} holds no item rows to withdraw"
    target = sorted(project_ids)[0]
    backend.query("UPDATE project SET published = false WHERE id::text = %s", (target,))
    refused = fresh_client.post("/reel/send")
    backend.query("UPDATE project SET published = true WHERE id::text = %s", (target,))
    assert refused.status_code in C.REFUSED, (
        f"POST /api/reel/send naming a withdrawn project returned "
        f"{refused.status_code}, expected a client error: {C.excerpt(refused)}"
    )
    assert C.REFUSAL_WITHDRAWN in refused.text, (
        f"the withdrawn-project refusal did not say {C.REFUSAL_WITHDRAWN!r}: "
        f"{C.excerpt(refused)}"
    )
    assert added, "the reel under test holds no items"


def test_over_long_note_and_brief_are_refused(fresh_client):
    """A note past its limit and a brief past its limit are both refused."""
    added = C.fill_reel(fresh_client, 1)
    long_note = "n" * (C.NOTE_MAX + 1)
    note = fresh_client.patch(f"/reel/items/{added[0]}", json={"note": long_note})
    if note.status_code == 200:
        fresh_client.patch("/reel", json={"title": "Pitch shortlist"})
        refused = fresh_client.post("/reel/send")
        assert C.REFUSAL_NOTE_LONG in refused.text, (
            f"a note of {len(long_note)} characters was accepted and the send did "
            f"not say {C.REFUSAL_NOTE_LONG!r}: {C.excerpt(refused)}"
        )
    else:
        assert note.status_code in C.REFUSED, (
            f"PATCH /api/reel/items with a note of {len(long_note)} characters "
            f"returned {note.status_code}, expected a client error: "
            f"{C.excerpt(note)}"
        )
    long_brief = "b" * (C.BRIEF_MAX + 1)
    brief = fresh_client.patch("/reel", json={"brief": long_brief})
    if brief.status_code == 200:
        refused = fresh_client.post("/reel/send")
        assert C.REFUSAL_BRIEF_LONG in refused.text, (
            f"a brief of {len(long_brief)} characters was accepted and the send "
            f"did not say {C.REFUSAL_BRIEF_LONG!r}: {C.excerpt(refused)}"
        )
    else:
        assert brief.status_code in C.REFUSED, (
            f"PATCH /api/reel with a brief of {len(long_brief)} characters "
            f"returned {brief.status_code}, expected a client error: "
            f"{C.excerpt(brief)}"
        )


def test_reel_title_bounds_are_enforced(fresh_client, backend):
    """A title past its limit is refused and the stored title is unchanged."""
    C.fill_reel(fresh_client, 1)
    good = "Pitch shortlist"
    accepted = fresh_client.patch("/reel", json={"title": good})
    assert accepted.status_code == 200, (
        f"PATCH /api/reel with a {len(good)}-character title returned "
        f"{accepted.status_code}, expected 200: {C.excerpt(accepted)}"
    )
    payload = C.read_reel(fresh_client)
    reel_id = str(payload.get("reel", payload)["id"])
    too_long = "t" * (C.TITLE_MAX + 1)
    refused = fresh_client.patch("/reel", json={"title": too_long})
    assert refused.status_code in C.REFUSED, (
        f"PATCH /api/reel with a {len(too_long)}-character title returned "
        f"{refused.status_code}, expected a client error: {C.excerpt(refused)}"
    )
    row = backend.one("reel", id=reel_id)
    assert row.get("title") == good, (
        f"the reel row carries the title {row.get('title')!r} after a refused "
        f"write, expected the earlier {good!r}"
    )
    assert row.get("state") in (C.STATE_DRAFT, C.STATE_EMPTY), (
        f"the reel row carries state {row.get('state')!r}, expected a draft"
    )
