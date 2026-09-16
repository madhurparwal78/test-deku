from __future__ import annotations

import pathlib
import re
from urllib.parse import urlparse

import httpx

import appclient
from conftest import (
    CREATOR, CREATOR_SECOND, CURATOR, DISCIPLINES, DIVISION_SLUGS, DIVISIONS, DRAFT_SLUG, EVENT_NAMES,
    HEADLINE, JUNO_STATEMENT, LINK_KINDS, MISSION_LINE, MSG_DIVISION, MSG_DUPLICATE, MSG_EMAIL, MSG_LINK_URL,
    MSG_LINKS, MSG_NAME, MSG_NOTE, MSG_PASSWORD, MSG_PICTURE, MSG_PLACEHOLDER, MSG_STATEMENT,
    MSG_UNCONFIRMED, NARROW_VIEWPORT, NOTICES, PAGE_SIZE, PASSWORD, PORTRAIT_ORIGIN, SEEDED_ACCOUNTS,
    SEEDED_LIVE, SEEDED_LIVE_SLUGS, SUBJECT_CONFIRM, SUBJECT_PUBLISHED, SUBJECT_RETURNED,
    STORED_JS, SUBJECT_TAKEN_DOWN, TECH_PRODUCTS, UNUSED_DISCIPLINE, WIDE_VIEWPORT, WORDMARK_NAME, account_id, apply,
    application_body, complete_profile, confirmation_token, count_mail, describe, division_roster,
    error_body, event_kinds, json_object, live_slugs, login, mail_text, new_creator, open_route,
    own_profile, page_metrics, parse_moment, probe_email, probe_token, published_creator, raw_get,
    run_together, settle, site_event_count, studio_transition, transition_own, version_of,
    wait_for_mail,
)


def test_seeded_rows_persisted_once(backend):
    """Seeded accounts, divisions, disciplines, profiles and notices are stored exactly once."""
    for email, role, name in SEEDED_ACCOUNTS:
        assert backend.count("accounts", email=email) == 1, f"accounts holds {email} other than once"
        row = backend.one("accounts", email=email)
        assert row["role"] == role, f"{email} stored with role {row['role']!r}"
        assert row["email_verified_at"] is not None, f"seeded {email} has no confirmed address"
    assert backend.count("divisions") == 4, "divisions does not hold exactly four rows"
    tokens = set()
    for slug, _name, colour, *_ in DIVISIONS:
        row = backend.one("divisions", slug=slug)
        assert row is not None and row["colour_token"] == colour, f"division {slug} stored as {row}"
        tokens.add(row["colour_token"])
    assert len(tokens) == 4, f"division colour tokens are not unique: {tokens}"
    assert backend.count("disciplines") == 12, "disciplines does not hold twelve rows"
    positions = []
    for slug in SEEDED_LIVE_SLUGS:
        assert backend.count("profiles", slug=slug) == 1, f"profile {slug} not stored once"
        row = backend.one("profiles", slug=slug)
        assert row["is_live"] is True and row["state"] == "published", f"{slug} stored as {row['state']}"
    live_rows = backend.query("SELECT position FROM profiles WHERE is_live")
    positions = [r["position"] for r in live_rows]
    assert len(positions) == len(set(positions)), f"live positions repeat: {positions}"
    draft = backend.one("profiles", slug=DRAFT_SLUG)
    assert draft is not None and draft["state"] == "draft" and draft["is_live"] is False, f"draft row {draft}"
    assert draft["account_id"] == account_id(backend, CREATOR_SECOND), "ada-moreau is not owned by creator2"
    juno = backend.one("profiles", slug="juno-okafor")
    assert juno["account_id"] == account_id(backend, CREATOR), "juno-okafor is not owned by creator"
    for kind, _title in NOTICES:
        assert backend.count("notices", kind=kind) == 1, f"notice {kind} not stored once"
        assert str(backend.one("notices", kind=kind)["body"]).strip(), f"notice {kind} body is empty"


def test_app_contract_artifacts_present():
    """The credentials file and both reserved directories exist at the app root."""
    root = pathlib.Path("/app")
    readme = root / "USER_README.md"
    assert readme.is_file() and readme.read_text(encoding="utf-8", errors="replace").strip(), \
        "/app/USER_README.md is missing or empty"
    for name in (".browser_screenshots", ".downloads"):
        target = root / name
        assert target.is_dir(), f"/app/{name}/ is missing"
        assert not any(target.iterdir()), f"/app/{name}/ is not empty"


def test_health_reports_database_and_mail(anon):
    """Readiness answers 200 under /api at APP_PUBLIC_URL and names the database apart from mail."""
    assert appclient.api_base().endswith("/api"), "the API base is not the /api prefix"
    response = anon.get("/health")
    assert response.status_code == 200, f"GET /api/health: {describe(response)}"
    body = response.text.lower()
    assert any(w in body for w in ("database", "postgres", "db")), f"health omits the database: {body[:200]}"
    assert any(w in body for w in ("mail", "smtp")), f"health omits the mail server: {body[:200]}"


def test_seeded_login_returns_token_role_and_verified(anon):
    """Seeded accounts sign in with the corpus password and receive token, role and verified."""
    for email, role, name in SEEDED_ACCOUNTS:
        body = json_object(anon.post("/auth/login", json={"email": email, "password": PASSWORD}), email)
        assert body.get("access_token"), f"no access_token for {email}: {body}"
        assert body.get("role") == role, f"{email} signed in with role {body.get('role')!r}"
        assert body.get("verified") is True, f"{email} signed in unverified: {body}"
        with appclient.client(body["access_token"]) as session:
            me = json_object(session.get("/me"), f"GET /api/me for {email}")
            assert me.get("email") == email and me.get("role") == role, f"GET /api/me answered {me}"
            assert "name" in me and "verified" in me and "profile_slug" in me, f"GET /api/me shape {me}"
            if email == CURATOR:
                assert me.get("profile_slug") is None, f"curator carries a profile slug: {me}"
                missing = session.get("/me/profile")
                assert missing.status_code == 404, f"curator own profile: {describe(missing)}"
            if email == CREATOR:
                assert me.get("profile_slug") == "juno-okafor", f"creator profile slug {me}"


def test_wrong_password_or_unknown_email_is_denied(anon):
    """A wrong password and an unknown email both answer 401 not_authenticated with no token."""
    for body in ({"email": CURATOR, "password": "wrong-pass-2026-x"},
                 {"email": probe_email("nobody"), "password": PASSWORD}):
        response = anon.post("/auth/login", json=body)
        error_body(response, 401, "not_authenticated", "bad sign in")
        assert "access_token" not in response.text, f"bad sign in leaked a token: {response.text[:200]}"


def test_repeated_failed_sign_in_is_limited():
    """Five failures for one email refuse the sixth attempt with 429, even with the right password."""
    creator = new_creator(confirm=False)
    for _ in range(4):
        assert login(creator["email"], "wrong-password-xyz").status_code == 401, "failed sign in not 401"
    assert login(creator["email"], creator["password"]).status_code == 200, "right password refused early"
    assert login(creator["email"], "wrong-password-xyz").status_code == 401, \
        "a successful sign in counted towards the limit"
    limited = login(creator["email"], creator["password"])
    body = error_body(limited, 429, "rate_limited", "sixth attempt")
    assert isinstance(body.get("retry_after"), (int, float)) and body["retry_after"] > 0, \
        f"retry_after is not a positive number: {body}"


def test_error_body_carries_token_message_fields_meta(anon):
    """Refusals answer the error body shape and never a server error."""
    responses = [anon.post("/applications", json={}), anon.get("/profiles", params={"q": "x" * 61}),
                 anon.get("/profiles/does-not-exist-anywhere"), anon.post("/events", json={"name": "nope"})]
    for response in responses:
        assert 400 <= response.status_code < 500, f"refusal not a client error: {describe(response)}"
        body = response.json()
        for key in ("error", "message", "fields", "meta", "retry_after"):
            assert key in body, f"error body lacks {key}: {describe(response)}"
        assert body["retry_after"] is None, f"retry_after set outside a 429: {body}"


def test_site_lists_divisions_and_disciplines_in_order(anon):
    """The site answer carries headline, mission, four divisions and twelve disciplines in order."""
    body = json_object(anon.get("/site"), "GET /api/site")
    assert body.get("headline") == HEADLINE, f"headline {body.get('headline')!r}"
    assert body.get("mission_line") == MISSION_LINE, f"mission line {body.get('mission_line')!r}"
    divisions = body.get("divisions") or []
    assert [d.get("slug") for d in divisions] == list(DIVISION_SLUGS), f"division order {divisions}"
    for got, (slug, name, colour, proposition, kicker, heading, scene) in zip(divisions, DIVISIONS):
        assert got.get("name") == name and got.get("colour_token") == colour, f"{slug} answered {got}"
        assert got.get("proposition") == proposition and got.get("kicker") == kicker, f"{slug} copy {got}"
        assert got.get("roster_heading") == heading and got.get("scene") == scene, f"{slug} answered {got}"
        assert got.get("position") is not None and got.get("body"), f"{slug} lacks position or body"
    disciplines = [(d.get("slug"), d.get("name")) for d in body.get("disciplines") or []]
    assert disciplines == list(DISCIPLINES), f"discipline order {disciplines}"
    assert UNUSED_DISCIPLINE in dict(disciplines), "partnerships missing from the vocabulary"


def test_division_roster_lists_live_profiles_in_curated_order(anon):
    """A division answers its live roster in curated order, tech products, a discipline filter and 404."""
    media = division_roster(anon, "creator-media")
    seeded = [s for s in media if s in SEEDED_LIVE_SLUGS]
    assert seeded == ["juno-okafor", "amara-voss", "theo-lindqvist", "priya-castellano"], \
        f"media roster order {media}"
    assert DRAFT_SLUG not in division_roster(anon, "creator-tech"), "draft listed on creator-tech"
    tech = json_object(anon.get("/divisions/creator-tech"), "creator-tech division")
    products = [(p.get("name"), p.get("tagline")) for p in tech.get("products") or []]
    assert products == list(TECH_PRODUCTS), f"tech products {products}"
    for product in tech["products"]:
        expected = "https://www.example.com/" + re.sub(r"[^a-z0-9]+", "-", product["name"].lower()).strip("-")
        assert product.get("url") == expected, f"product url {product.get('url')!r}"
        assert isinstance(product.get("pills"), list) and product["pills"], f"product pills {product}"
    filtered = division_roster(anon, "creator-tech", discipline="analytics")
    assert set(filtered) >= {"kenji-aldana", "mara-oyelaran"} and "felix-brandt" not in filtered, \
        f"tech analytics roster {filtered}"
    error_body(anon.get("/divisions/creator-nothing"), 404, "not_found", "unknown division")


def test_profile_full_shape_carries_links_and_credits(anon):
    """A live profile answers statement, links, credits and UTC timestamps without an account."""
    body = json_object(anon.get("/profiles/juno-okafor"), "juno-okafor full profile")
    assert body.get("statement") == JUNO_STATEMENT, f"statement {body.get('statement')!r}"
    assert body.get("division") == "creator-media" and body.get("colour_token") == "red", f"division {body}"
    assert str(body.get("portrait_url", "")).startswith(PORTRAIT_ORIGIN), f"portrait {body.get('portrait_url')}"
    links = body.get("links") or []
    assert links and all({"kind", "label", "url"} <= set(link) for link in links), f"links {links}"
    assert isinstance(body.get("credits"), list) and body["credits"], f"credits {body.get('credits')}"
    parse_moment(body.get("published_at"))
    parse_moment(body.get("updated_at"))


def test_profile_not_live_is_unreadable_everywhere(anon, creator, curator):
    """A draft profile answers 404 for every caller and appears in no public list or sitemap."""
    unknown = anon.get("/profiles/nobody-by-this-slug")
    error_body(unknown, 404, "not_found", "unknown slug")
    for session in (anon, creator, curator):
        error_body(session.get(f"/profiles/{DRAFT_SLUG}"), 404, "not_found", "draft slug")
    assert DRAFT_SLUG not in live_slugs(anon), "draft listed on /api/profiles"
    assert DRAFT_SLUG not in live_slugs(creator), "draft listed for a creator"
    assert DRAFT_SLUG not in division_roster(anon, "creator-tech"), "draft on the division roster"
    assert f"/creator/{DRAFT_SLUG}" not in raw_get("/sitemap.xml").text, "draft in sitemap"


def test_roster_filters_intersect_and_search_ranks(anon):
    """Filters intersect, an empty match answers zero, and free text matches and ranks."""
    both = live_slugs(anon, division="creator-tech", discipline="analytics")
    assert {"kenji-aldana", "mara-oyelaran"} <= set(both) and "felix-brandt" not in both, f"intersection {both}"
    assert all(s not in both for s in ("amara-voss", "juno-okafor")), f"intersection leaked {both}"
    empty = json_object(anon.get("/profiles", params={"discipline": UNUSED_DISCIPLINE}), "partnerships")
    assert empty.get("total") == 0 and empty.get("items") == [], f"partnerships answered {empty}"
    trains = live_slugs(anon, q="night trains")
    assert trains and trains[0] == "amara-voss", f"statement search {trains}"
    ranked = live_slugs(anon, q="mara")
    assert "mara-oyelaran" in ranked and "amara-voss" in ranked, f"mara search {ranked}"
    assert ranked.index("mara-oyelaran") < ranked.index("amara-voss"), f"prefix did not rank first {ranked}"
    everyone = json_object(anon.get("/profiles"), "unfiltered")["total"]
    short = json_object(anon.get("/profiles", params={"q": "m"}), "one-character q")["total"]
    assert short == everyone, f"one-character q narrowed {everyone} to {short}"
    long = anon.get("/profiles", params={"q": "y" * 61})
    assert long.status_code == 400, f"61-character q: {describe(long)}"


def test_roster_sorts_and_pages(anon):
    """Roster pages carry the summary shape, 24 at most, and sort by position, name and newest."""
    body = json_object(anon.get("/profiles"), "GET /api/profiles")
    assert {"total", "page", "items"} <= set(body), f"roster shape {list(body)}"
    assert len(body["items"]) <= PAGE_SIZE and body["total"] >= len(SEEDED_LIVE), f"page {len(body['items'])}"
    for row in body["items"]:
        for key in ("slug", "name", "division", "division_name", "colour_token", "disciplines",
                    "portrait_url", "position"):
            assert key in row, f"summary lacks {key}: {row}"
    curated = [s for s in live_slugs(anon) if s in SEEDED_LIVE_SLUGS]
    assert curated == [s for s, _, _ in SEEDED_LIVE], f"curated order {curated}"
    named = json_object(anon.get("/profiles", params={"sort": "name"}), "sort=name")["items"]
    names = [row["name"] for row in named]
    assert names == sorted(names, key=str.casefold), f"name order {names}"
    newest = live_slugs(anon, sort="newest")[:6]
    times = [parse_moment(json_object(anon.get(f"/profiles/{s}"), s)["published_at"]) for s in newest]
    assert times == sorted(times, reverse=True), f"newest order {list(zip(newest, times))}"


def test_state_filter_from_non_curator_is_dropped(anon, creator):
    """A state filter from a visitor or a creator is dropped and the live roster answers."""
    for session in (anon, creator):
        drafts = session.get("/profiles", params={"state": "draft"})
        assert drafts.status_code == 200, f"state filter errored: {describe(drafts)}"
        slugs = [row["slug"] for row in drafts.json().get("items", [])]
        assert DRAFT_SLUG not in slugs, f"state=draft exposed the draft: {slugs}"
        assert drafts.json().get("total") == json_object(session.get("/profiles"), "plain")["total"], \
            "state filter changed the total for a non-curator"


def test_application_creates_unconfirmed_creator_and_applying_profile(backend):
    """An application answers 201 and stores one unconfirmed creator and one applying profile."""
    email = probe_email("apply")
    response = apply(application_body(email, f"Probe Applicant {probe_token()}"))
    body = json_object(response, "POST /api/applications")
    assert response.status_code == 201, f"application status {describe(response)}"
    assert body["account"].get("role") == "creator" and body["account"].get("verified") is False, body
    assert body["profile"].get("state") == "applying" and body["profile"].get("slug"), body
    assert backend.count("accounts", email=email) == 1, "application did not store one account"
    account = backend.one("accounts", email=email)
    assert account["role"] == "creator" and account["email_verified_at"] is None, f"account {account}"
    profile = backend.one("profiles", slug=body["profile"]["slug"])
    assert profile["account_id"] == account["id"] and profile["state"] == "applying", f"profile {profile}"
    assert profile["is_live"] is False, "an applying profile is live"
    assert "applied" in event_kinds(backend, profile["slug"]), "no applied profile event"


def test_application_sends_confirmation_mail():
    """A successful application mails Confirm your address with the link and the applicant's name."""
    email = probe_email("mail")
    name = f"Probe Mailed {probe_token()}"
    assert apply(application_body(email, name)).status_code == 201, "application refused"
    message = wait_for_mail(email, SUBJECT_CONFIRM)
    text = mail_text(message["ID"])
    first = next(line for line in text.splitlines() if line.strip())
    assert "/verify?token=" in first, f"confirmation mail does not open with the link: {text[:200]}"
    assert name in text, f"confirmation mail does not name {name}"
    assert [a.get("Address", "").lower() for a in message.get("To") or []] == [email], "wrong recipients"
    assert not message.get("Cc") and not message.get("Bcc"), f"confirmation mail copied others {message}"


def test_confirmation_link_confirms_address_and_moves_to_draft(backend, anon):
    """Confirming stores the confirmation time and moves the applying profile to draft."""
    email = probe_email("confirm")
    created = json_object(apply(application_body(email, f"Probe Confirm {probe_token()}")), "application")
    response = anon.post("/accounts/verifications", json={"token": confirmation_token(email)})
    assert response.status_code == 204, f"verification: {describe(response)}"
    assert backend.one("accounts", email=email)["email_verified_at"] is not None, "address still unconfirmed"
    assert backend.one("profiles", slug=created["profile"]["slug"])["state"] == "draft", "profile not draft"
    assert json_object(login(email, "probe-pass-2026-long"), "sign in")["verified"] is True, "still unverified"


def test_used_or_unknown_confirmation_token_is_refused(anon):
    """A used token answers 410 and an unknown token answers 400."""
    email = probe_email("used")
    assert apply(application_body(email, f"Probe Used {probe_token()}")).status_code == 201
    token = confirmation_token(email)
    assert anon.post("/accounts/verifications", json={"token": token}).status_code == 204
    again = anon.post("/accounts/verifications", json={"token": token})
    assert again.status_code == 410, f"reused token: {describe(again)}"
    unknown = anon.post("/accounts/verifications", json={"token": "not-a-real-token-" + probe_token()})
    assert unknown.status_code == 400, f"unknown token: {describe(unknown)}"


def test_invalid_application_is_refused_with_field_messages(backend):
    """An invalid application answers 400 with every field message and creates nothing."""
    email = "not-an-address"
    body = {"email": email, "password": "short", "name": "J", "division": "creator-nowhere",
            "disciplines": ["analytics", "discovery", "writing", "design", "commerce"],
            "statement": "Too short.", "links": [], "consent": False}
    response = apply(body)
    refused = error_body(response, 400, "validation_failed", "invalid application")
    fields = refused.get("fields") or {}
    expected = {"email": MSG_EMAIL, "password": MSG_PASSWORD, "name": MSG_NAME, "division": MSG_DIVISION,
                "statement": MSG_STATEMENT, "links": MSG_LINKS}
    for field, message in expected.items():
        assert fields.get(field) == message, f"field {field} message {fields.get(field)!r}"
    assert "disciplines" in fields and "consent" in fields, f"fields {fields}"
    good = application_body(probe_email("nomail"), "Probe Nothing", consent=False)
    assert apply(good).status_code == 400, "an application without consent was accepted"
    assert backend.count("accounts", email=good["email"]) == 0, "a refused application stored an account"
    assert count_mail(good["email"]) == 0, "a refused application sent mail"


def test_duplicate_application_email_is_refused(backend):
    """A registered email in any case answers 409 conflict and stays one lowercase account."""
    email = probe_email("dupe")
    mixed = email.replace("dupe", "DuPe")
    assert apply(application_body(mixed, f"Probe Dupe {probe_token()}")).status_code == 201
    assert backend.count("accounts", email=email) == 1, "account email not stored lowercase"
    again = apply(application_body(email.upper(), f"Probe Dupe Two {probe_token()}"))
    body = error_body(again, 409, "conflict", "duplicate application")
    assert body.get("message") == MSG_DUPLICATE, f"duplicate message {body.get('message')!r}"
    assert backend.count("accounts", email=email) == 1, "duplicate created a second account"


def test_concurrent_duplicate_applications_create_one_account(backend):
    """Two simultaneous applications with one email leave one account and one profile."""
    email = probe_email("race")
    name = f"Probe Race {probe_token()}"
    results = run_together([lambda: apply(application_body(email, name)),
                            lambda: apply(application_body(email, name))])
    assert sorted(r.status_code for r in results) == [201, 409], f"statuses {[describe(r) for r in results]}"
    assert backend.count("accounts", email=email) == 1, "two accounts for one email"
    owner = account_id(backend, email)
    assert backend.count("profiles", account_id=owner) == 1, "two profiles for one account"


def test_slug_derived_with_suffix_on_collision(backend):
    """A slug is the kebab-cased name and a collision, even simultaneous, gains a suffix."""
    token = probe_token()
    name = f"  Probe  Slug!! {token} "
    first = json_object(apply(application_body(probe_email("slug"), name)), "first")["profile"]["slug"]
    base = f"probe-slug-{token}"
    assert first == base, f"slug {first!r} is not {base!r}"
    second = json_object(apply(application_body(probe_email("slug"), name, slug="chosen")), "second")
    assert second["profile"]["slug"] == f"{base}-2", f"collision slug {second['profile']['slug']!r}"
    twin = f"Probe Twin {probe_token()}"
    results = run_together([lambda: apply(application_body(probe_email("twin"), twin)),
                            lambda: apply(application_body(probe_email("twin"), twin))])
    slugs = [json_object(r, "twin")["profile"]["slug"] for r in results]
    assert len(set(slugs)) == 2, f"simultaneous twins share a slug: {slugs}"


def test_profile_edits_persist_with_version(backend):
    """Own-profile saves raise the version by one and lists replace whole."""
    creator = new_creator()
    with appclient.client(creator["token"]) as session:
        profile = own_profile(session)
        for key in ("slug", "state", "is_live", "version", "pending", "links", "credits", "disciplines"):
            assert key in profile, f"own profile lacks {key}"
        statement = f"<b>Plain</b> {'words for a statement that runs long enough to be kept as it is. ' * 2}".strip()
        saved = json_object(session.patch("/me/profile", json={"statement": statement,
                                                               "version": profile["version"]}), "patch")
        assert saved["version"] == profile["version"] + 1 and saved["statement"] == statement, saved
        links = [{"kind": k, "label": f"Link {k}", "url": f"https://www.example.com/{k}"} for k in LINK_KINDS[:5]]
        after_links = json_object(session.put("/me/profile/links", json={"links": links,
                                                                          "version": saved["version"]}), "links")
        assert [l["kind"] for l in after_links["links"]] == list(LINK_KINDS[:5]), after_links["links"]
        last = [{"kind": LINK_KINDS[5], "label": "Press", "url": "https://www.example.com/press"}]
        after_one = json_object(session.put("/me/profile/links", json={"links": last,
                                                                        "version": after_links["version"]}), "l")
        assert [l["kind"] for l in after_one["links"]] == ["document"], "links not replaced whole"
        credits = json_object(session.put("/me/profile/credits", json={"credits": ["Host, Probe Show"],
                                                                         "version": after_one["version"]}), "c")
        assert credits["credits"] == ["Host, Probe Show"], credits["credits"]
        disc = json_object(session.put("/me/profile/disciplines", json={"disciplines": ["design"],
                                                                         "version": credits["version"]}), "d")
        assert [d["slug"] for d in disc["disciplines"]] == ["design"], disc["disciplines"]
        assert disc["version"] == profile["version"] + 5, f"version did not rise by one per write {disc['version']}"
    row = backend.one("profiles", slug=creator["slug"])
    assert row["statement"] == statement, "statement not stored as plain text"


def test_stale_version_write_is_refused(backend):
    """A write with an older version answers 409 version_conflict and stores nothing."""
    creator = new_creator()
    with appclient.client(creator["token"]) as session:
        profile = own_profile(session)
        json_object(session.patch("/me/profile", json={"name": "Probe Fresh Name",
                                                       "version": profile["version"]}), "first save")
        stale = session.patch("/me/profile", json={"name": "Probe Stale Name", "version": profile["version"]})
        error_body(stale, 409, "version_conflict", "stale write")
        assert own_profile(session)["name"] == "Probe Fresh Name", "stale write changed the name"


def test_invalid_profile_values_are_refused(backend):
    """Bad portrait, link scheme, sixth link, long credit, long statement and unknown kind are not stored."""
    creator = new_creator()
    with appclient.client(creator["token"]) as session:
        before = own_profile(session)
        version = before["version"]
        portrait = session.patch("/me/profile", json={"portrait_url": "https://elsewhere.example.org/p.jpg",
                                                      "version": version})
        assert error_body(portrait, 400, "validation_failed", "portrait")["fields"].get("portrait_url") == MSG_PICTURE
        script = session.put("/me/profile/links", json={"links": [{"kind": "site", "label": "Bad",
                                                                   "url": "javascript:alert(1)"}],
                                                        "version": version})
        assert MSG_LINK_URL in script.text and script.status_code == 400, f"script link {describe(script)}"
        six = [{"kind": "site", "label": f"Six {n}", "url": f"https://www.example.com/{n}"} for n in range(6)]
        assert session.put("/me/profile/links", json={"links": six, "version": version}).status_code == 400
        kind = [{"kind": "video", "label": "Film", "url": "https://www.example.com/film"}]
        assert session.put("/me/profile/links", json={"links": kind, "version": version}).status_code == 400
        credit = session.put("/me/profile/credits", json={"credits": ["c" * 81], "version": version})
        assert credit.status_code == 400, f"long credit {describe(credit)}"
        long = session.patch("/me/profile", json={"statement": "s" * 401, "version": version})
        assert long.status_code == 400, f"long statement {describe(long)}"
        vocab = session.put("/me/profile/disciplines", json={"disciplines": ["juggling"], "version": version})
        assert vocab.status_code == 400, f"unknown discipline {describe(vocab)}"
        after = own_profile(session)
    assert after["version"] == version and after["statement"] == before["statement"], "refused value stored"
    assert after["links"] == before["links"] and after["portrait_url"] == before["portrait_url"], after


def test_complete_profile_submits_without_mail(backend):
    """A complete confirmed profile moves to submitted with its time and nobody is mailed."""
    creator = new_creator()
    mails_before = count_mail(creator["email"])
    with appclient.client(creator["token"]) as session:
        complete_profile(session, creator["slug"])
        submitted = transition_own(session, "submitted")
    body = json_object(submitted, "submit")
    assert body.get("state") == "submitted", f"state {body.get('state')}"
    row = backend.one("profiles", slug=creator["slug"])
    assert row["state"] == "submitted" and row["submitted_at"] is not None, f"row {row}"
    assert "submitted" in event_kinds(backend, creator["slug"]), "no submitted event"
    settle(3.0)
    assert count_mail(creator["email"]) == mails_before, "a submission sent mail to the owner"
    assert count_mail(CURATOR) == 0, "a submission sent mail to the curator"


def test_editing_while_submitted_is_refused():
    """Every editor write on a submitted profile answers 422 state_not_allowed."""
    creator = new_creator()
    with appclient.client(creator["token"]) as session:
        complete_profile(session, creator["slug"])
        assert transition_own(session, "submitted").status_code == 200
        version = own_profile(session)["version"]
        error_body(session.patch("/me/profile", json={"name": "Probe Locked", "version": version}),
                   422, "state_not_allowed", "patch while submitted")
        error_body(session.put("/me/profile/credits", json={"credits": ["Locked"], "version": version}),
                   422, "state_not_allowed", "credits while submitted")


def test_unconfirmed_creator_cannot_submit(backend):
    """An unconfirmed creator may edit but a submission answers 403 not_verified and changes nothing."""
    creator = new_creator(confirm=False)
    with appclient.client(creator["token"]) as session:
        saved = complete_profile(session, creator["slug"])
        assert saved["portrait_url"].startswith(PORTRAIT_ORIGIN), "unconfirmed creator could not edit"
        refused = transition_own(session, "submitted")
    body = error_body(refused, 403, "not_verified", "unconfirmed submission")
    assert body.get("message") == MSG_UNCONFIRMED, f"message {body.get('message')!r}"
    assert backend.one("profiles", slug=creator["slug"])["state"] == "applying", "state changed"


def test_placeholder_blocks_submission_and_names_fields(backend):
    """INSERT NAME, Pill Text and whole-word TODO trip the placeholder rule; Todorov does not."""
    creator = new_creator(name=f"Mila Todorov {probe_token()}")
    with appclient.client(creator["token"]) as session:
        complete_profile(session, creator["slug"])
        profile = own_profile(session)
        placeholder = ("** INSERT NAME ** writes here about long coastal walks and the quiet pieces made "
                       "from them for late listeners.")
        profile = json_object(session.patch("/me/profile", json={"statement": placeholder,
                                                                 "version": profile["version"]}), "statement")
        json_object(session.put("/me/profile/credits", json={"credits": ["Pill Text", "Editor, TODO list"],
                                                              "version": profile["version"]}), "credits")
        refused = transition_own(session, "submitted")
        body = error_body(refused, 422, "validation_failed", "placeholder submission")
        flagged = set((body.get("meta") or {}).get("placeholder_fields") or [])
        assert "statement" in flagged and "credits" in flagged, f"placeholder fields {flagged}"
        assert "name" not in flagged, f"Todorov tripped the placeholder rule: {flagged}"
        assert MSG_PLACEHOLDER in refused.text, f"placeholder message missing: {refused.text[:300]}"
        assert own_profile(session)["state"] == "draft", "placeholder submission changed state"


def test_incomplete_submission_lists_every_failure(backend):
    """A profile missing portrait and statement answers 422 naming both and stays draft."""
    creator = new_creator()
    with appclient.client(creator["token"]) as session:
        profile = own_profile(session)
        json_object(session.patch("/me/profile", json={"statement": "Short now.", "version": profile["version"]}),
                    "short statement")
        refused = transition_own(session, "submitted")
        fields = error_body(refused, 422, "validation_failed", "incomplete submission").get("fields") or {}
        assert fields.get("portrait_url") == MSG_PICTURE, f"portrait message {fields}"
        assert fields.get("statement") == MSG_STATEMENT, f"statement message {fields}"
        assert own_profile(session)["state"] == "draft", "incomplete submission changed state"


def test_curator_review_queue_lists_submitted_profiles(curator, anon):
    """The curator state filter lists a submitted profile that no public list shows."""
    creator = new_creator()
    with appclient.client(creator["token"]) as session:
        complete_profile(session, creator["slug"])
        assert transition_own(session, "submitted").status_code == 200
    queue = live_slugs(curator, state="submitted")
    assert creator["slug"] in queue, f"submitted {creator['slug']} missing from the queue"
    assert creator["slug"] not in live_slugs(anon), "a submitted profile is public"


def test_curator_sends_back_with_note_and_owner_is_mailed(backend, curator):
    """Send back stores the note and return time, mails the owner the note and never the curator."""
    creator = new_creator()
    with appclient.client(creator["token"]) as session:
        complete_profile(session, creator["slug"])
        assert transition_own(session, "submitted").status_code == 200
    note = f"Probe note {probe_token()}: please add a second link to recent work."
    body = json_object(studio_transition(curator, backend, creator["slug"], "changes_requested", note=note),
                       "send back")
    assert body.get("state") == "changes_requested", body
    row = backend.one("profiles", slug=creator["slug"])
    assert row["return_note"] == note and row["returned_at"] is not None, f"row {row}"
    with appclient.client(creator["token"]) as session:
        assert own_profile(session).get("return_note") == note, "owner cannot read the note"
    message = wait_for_mail(creator["email"], SUBJECT_RETURNED)
    assert note in mail_text(message["ID"]), "the returned mail lacks the note"
    assert "returned" in event_kinds(backend, creator["slug"]), "no returned event"
    assert count_mail(CURATOR) == 0, "mail reached a curator"


def test_send_back_note_outside_bounds_is_refused(backend, curator):
    """Notes under ten or over five hundred characters are refused and change nothing."""
    creator = new_creator()
    with appclient.client(creator["token"]) as session:
        complete_profile(session, creator["slug"])
        assert transition_own(session, "submitted").status_code == 200
    for note in ("too short", "n" * 501):
        refused = studio_transition(curator, backend, creator["slug"], "changes_requested", note=note)
        body = error_body(refused, 400, "validation_failed", "note bounds")
        assert MSG_NOTE in refused.text, f"note message missing {body}"
    assert backend.one("profiles", slug=creator["slug"])["state"] == "submitted", "state changed"


def test_curator_publish_goes_live_everywhere_and_mails_owner(backend, curator, anon):
    """Publishing makes a profile live on every public surface, records the curator and mails the owner."""
    top = max(r["position"] for r in backend.query("SELECT position FROM profiles WHERE is_live"))
    creator = published_creator(backend, curator, "creator-products")
    row = backend.one("profiles", slug=creator["slug"])
    assert row["state"] == "published" and row["is_live"] is True, f"row {row}"
    assert row["reviewed_by"] == account_id(backend, CURATOR), "reviewed_by is not the curator"
    assert row["published_at"] is not None and row["position"] > top, f"position {row['position']} after {top}"
    json_object(anon.get(f"/profiles/{creator['slug']}"), "public profile")
    assert creator["slug"] in division_roster(anon, "creator-products"), "not on the division roster"
    assert creator["slug"] in live_slugs(anon), "not on the roster"
    assert f"/creator/{creator['slug']}" in raw_get("/sitemap.xml").text, "not in the sitemap"
    message = wait_for_mail(creator["email"], SUBJECT_PUBLISHED)
    assert f"/creator/{creator['slug']}" in mail_text(message["ID"]), "publish mail lacks the address"
    assert [a.get("Address", "").lower() for a in message.get("To") or []] == [creator["email"]]
    assert "published" in event_kinds(backend, creator["slug"]), "no published event"
    assert count_mail(CURATOR) == 0, "mail reached a curator"


def test_second_publish_with_stale_version_is_refused(backend, curator):
    """A second publish carrying the version read before the first answers 409."""
    creator = new_creator()
    with appclient.client(creator["token"]) as session:
        complete_profile(session, creator["slug"])
        assert transition_own(session, "submitted").status_code == 200
    version = version_of(backend, creator["slug"])
    first = curator.post(f"/profiles/{creator['slug']}/transitions", json={"to": "published", "version": version})
    assert first.status_code == 200, describe(first)
    second = curator.post(f"/profiles/{creator['slug']}/transitions", json={"to": "published", "version": version})
    error_body(second, 409, "version_conflict", "second publish")


def test_disallowed_transitions_are_refused(backend, curator):
    """Publishing a draft, publishing nothing pending and an owner take down answer 422."""
    creator = new_creator()
    error_body(studio_transition(curator, backend, creator["slug"], "published"), 422, "state_not_allowed",
               "publish a draft")
    live = published_creator(backend, curator)
    with appclient.client(live["token"]) as session:
        error_body(transition_own(session, "published"), 422, "state_not_allowed", "nothing pending")
        error_body(transition_own(session, "unpublished"), 422, "state_not_allowed", "owner take down")


def test_creator_is_denied_every_studio_route(backend, creator):
    """A creator is refused publish, send back, take down, move and reorder, whatever role the body names."""
    target = new_creator()
    with appclient.client(target["token"]) as session:
        complete_profile(session, target["slug"])
        assert transition_own(session, "submitted").status_code == 200
    version = version_of(backend, target["slug"])
    for to in ("published", "changes_requested", "unpublished"):
        refused = creator.post(f"/profiles/{target['slug']}/transitions",
                               json={"to": to, "version": version, "note": "Probe denied note text", "role": "curator"})
        error_body(refused, 403, "not_authorised", f"creator transition {to}")
    moved = creator.patch(f"/profiles/{target['slug']}", json={"division": "creator-tech", "version": version})
    error_body(moved, 403, "not_authorised", "creator move")
    order = creator.put("/studio/roster-order", json={"slugs": list(SEEDED_LIVE_SLUGS), "role": "curator"})
    error_body(order, 403, "not_authorised", "creator reorder")
    row = backend.one("profiles", slug=target["slug"])
    assert row["state"] == "submitted" and row["version"] == version, f"denied calls changed {row}"


def test_creator_cannot_read_or_change_another_creators_profile(backend, creator, creator_second):
    """Each creator reads only their own profile and cannot reach the other tenant's by any address."""
    assert own_profile(creator)["slug"] == "juno-okafor", "creator own profile is not juno-okafor"
    assert own_profile(creator_second)["slug"] == DRAFT_SLUG, "creator2 own profile is not ada-moreau"
    error_body(creator.get(f"/profiles/{DRAFT_SLUG}"), 404, "not_found", "read another creator draft")
    before = backend.one("profiles", slug=DRAFT_SLUG)
    refused = creator.patch(f"/profiles/{DRAFT_SLUG}", json={"division": "creator-media",
                                                             "version": before["version"]})
    assert refused.status_code == 403, f"creator changed another profile: {describe(refused)}"
    after = backend.one("profiles", slug=DRAFT_SLUG)
    assert after["version"] == before["version"] and after["division_id"] == before["division_id"], after


def test_curator_cannot_change_creator_words(backend, curator):
    """The curator move route refuses statement, name and colour fields with 403 and changes nothing."""
    before = backend.one("profiles", slug="theo-lindqvist")
    for field, value in (("statement", "Rewritten by the studio with enough words to pass length rules."),
                         ("name", "Studio Name"), ("colour_token", "red")):
        refused = curator.patch("/profiles/theo-lindqvist", json={field: value, "version": before["version"]})
        error_body(refused, 403, "not_authorised", f"curator {field}")
    after = backend.one("profiles", slug="theo-lindqvist")
    assert after["statement"] == before["statement"] and after["name"] == before["name"], "words changed"
    assert after["version"] == before["version"], "a refused curator write changed the version"


def test_anonymous_writes_are_denied(backend, anon):
    """Anonymous calls to own-profile and studio endpoints answer 401 not_authenticated."""
    version = version_of(backend, "felix-brandt")
    calls = [anon.get("/me"), anon.get("/me/profile"), anon.patch("/me/profile", json={"name": "Anon"}),
             anon.post("/me/profile/transitions", json={"to": "submitted", "version": 1}),
             anon.post("/profiles/felix-brandt/transitions", json={"to": "unpublished", "version": version}),
             anon.patch("/profiles/felix-brandt", json={"division": "creator-media", "version": version}),
             anon.put("/studio/roster-order", json={"slugs": list(SEEDED_LIVE_SLUGS)})]
    for response in calls:
        error_body(response, 401, "not_authenticated", "anonymous call")
    assert backend.one("profiles", slug="felix-brandt")["state"] == "published", "anonymous write landed"


def test_live_profile_edit_is_held_until_published(backend, curator, anon):
    """An owner edit to a live profile is held as pending while the public keeps the live copy."""
    creator = published_creator(backend, curator)
    live = json_object(anon.get(f"/profiles/{creator['slug']}"), "live")["statement"]
    rewritten = f"Rewritten {probe_token()} statement about field recordings made on night ferries."
    with appclient.client(creator["token"]) as session:
        version = own_profile(session)["version"]
        saved = json_object(session.patch("/me/profile", json={"statement": rewritten, "version": version}), "edit")
    assert saved["state"] == "published" and (saved.get("pending") or {}).get("statement") == rewritten, saved
    assert json_object(anon.get(f"/profiles/{creator['slug']}"), "public")["statement"] == live, "public changed"
    assert backend.one("profiles", slug=creator["slug"])["statement"] == live, "live copy overwritten"


def test_owner_publishes_changes_without_review(backend, curator, anon):
    """Publishing unchanged-division pending edits applies them, keeps published_at and sends no mail."""
    creator = published_creator(backend, curator)
    first = backend.one("profiles", slug=creator["slug"])
    mails = count_mail(creator["email"])
    rewritten = f"Rewritten {probe_token()} statement about slow radio pieces recorded along canal towpaths."
    with appclient.client(creator["token"]) as session:
        version = own_profile(session)["version"]
        json_object(session.patch("/me/profile", json={"statement": rewritten, "version": version}), "edit")
        published = json_object(transition_own(session, "published"), "publish changes")
    assert published["state"] == "published" and published.get("pending") is None, published
    assert json_object(anon.get(f"/profiles/{creator['slug']}"), "public")["statement"] == rewritten
    after = backend.one("profiles", slug=creator["slug"])
    assert after["published_at"] == first["published_at"], "published_at changed on republish"
    assert after["updated_at"] != first["updated_at"], "updated_at did not change"
    settle(3.0)
    assert count_mail(creator["email"]) == mails, "publishing own changes sent mail"


def test_published_slug_never_changes(backend, curator):
    """A renamed live profile keeps its slug and no request can set a slug."""
    creator = published_creator(backend, curator)
    with appclient.client(creator["token"]) as session:
        version = own_profile(session)["version"]
        session.patch("/me/profile", json={"name": f"Renamed Probe {probe_token()}", "slug": "chosen-slug",
                                           "version": version})
        assert transition_own(session, "published").status_code == 200
        assert own_profile(session)["slug"] == creator["slug"], "a live slug changed"
    assert backend.count("profiles", slug="chosen-slug") == 0, "a request set a slug"


def test_division_change_goes_through_review_and_moves_profile(backend, curator, anon):
    """A division change is refused self-publish, stays live on the old division, then moves on publish."""
    creator = published_creator(backend, curator, "creator-media")
    rewritten = f"Moved {probe_token()} statement about community radio evenings hosted in village halls."
    with appclient.client(creator["token"]) as session:
        version = own_profile(session)["version"]
        edited = json_object(session.patch("/me/profile", json={"division": "creator-communities",
                                                                "statement": rewritten, "version": version}), "edit")
        assert edited["state"] == "published", edited
        error_body(transition_own(session, "published"), 422, "state_not_allowed", "self-publish a move")
        sent = json_object(transition_own(session, "submitted"), "send changes for review")
        assert sent["state"] == "submitted" and (sent.get("pending") or {}).get("division") == "creator-communities"
    assert creator["slug"] in division_roster(anon, "creator-media"), "left the old division before review"
    assert json_object(anon.get(f"/profiles/{creator['slug']}"), "public")["division"] == "creator-media"
    published = studio_transition(curator, backend, creator["slug"], "published")
    assert published.status_code == 200, describe(published)
    assert creator["slug"] in division_roster(anon, "creator-communities"), "not on the new division"
    assert creator["slug"] not in division_roster(anon, "creator-media"), "still on the old division"
    public = json_object(anon.get(f"/profiles/{creator['slug']}"), "moved profile")
    assert public["division"] == "creator-communities" and public["colour_token"] == "green", public
    assert public["statement"] == rewritten, "the rewritten statement did not go live"
    rows = [r for r in backend.rows("profile_events", profile_id=backend.one("profiles", slug=creator["slug"])["id"])
            if r["kind"] == "moved"]
    assert rows and rows[-1]["from_division_id"] != rows[-1]["to_division_id"], f"moved events {rows}"


def test_take_down_removes_profile_and_mails_owner(backend, curator, anon):
    """Take down hides the profile everywhere, mails the owner, and an owner edit returns it to draft."""
    creator = published_creator(backend, curator, "creator-tech")
    body = json_object(studio_transition(curator, backend, creator["slug"], "unpublished"), "take down")
    assert body["state"] == "unpublished", body
    row = backend.one("profiles", slug=creator["slug"])
    assert row["state"] == "unpublished" and row["is_live"] is False, f"row {row}"
    error_body(anon.get(f"/profiles/{creator['slug']}"), 404, "not_found", "taken down profile")
    assert creator["slug"] not in division_roster(anon, "creator-tech"), "still on the division"
    assert f"/creator/{creator['slug']}" not in raw_get("/sitemap.xml").text, "still in the sitemap"
    wait_for_mail(creator["email"], SUBJECT_TAKEN_DOWN)
    assert "unpublished" in event_kinds(backend, creator["slug"]), "no unpublished event"
    with appclient.client(creator["token"]) as session:
        version = own_profile(session)["version"]
        edited = json_object(session.patch("/me/profile", json={"name": "Probe Returned Draft",
                                                                "version": version}), "edit after take down")
    assert edited["state"] == "draft", f"state after edit {edited['state']}"


def test_curator_moves_profile_between_divisions(backend, curator, anon):
    """A curator move changes the division at once, records a moved event and sends no mail."""
    creator = published_creator(backend, curator, "creator-media")
    mails = count_mail(creator["email"])
    moved = curator.patch(f"/profiles/{creator['slug']}", json={"division": "creator-tech",
                                                                "version": version_of(backend, creator["slug"])})
    json_object(moved, "curator move")
    assert json_object(anon.get(f"/profiles/{creator['slug']}"), "public")["division"] == "creator-tech"
    assert creator["slug"] in division_roster(anon, "creator-tech"), "not on the new division"
    assert "moved" in event_kinds(backend, creator["slug"]), "no moved event"
    settle(3.0)
    assert count_mail(creator["email"]) == mails, "a curator move sent mail"


def test_roster_order_is_replaced_whole(anon, curator):
    """An incomplete order is refused unchanged; a complete list sets positions from 1 and is restored."""
    original = live_slugs(anon)
    refused = curator.put("/studio/roster-order", json={"slugs": original[1:]})
    error_body(refused, 400, "validation_failed", "incomplete order")
    assert live_slugs(anon) == original, "a refused order changed the roster"
    reversed_order = list(reversed(original))
    applied_response = curator.put("/studio/roster-order", json={"slugs": reversed_order})
    assert 200 <= applied_response.status_code < 300, describe(applied_response)
    applied = live_slugs(anon)
    assert applied == reversed_order, f"order not applied: {applied[:5]}"
    positions = [row["position"] for row in json_object(anon.get("/profiles"), "positions")["items"]]
    assert positions[0] == 1, f"positions do not start at 1: {positions[:5]}"
    restored = curator.put("/studio/roster-order", json={"slugs": original})
    assert 200 <= restored.status_code < 300, describe(restored)
    assert live_slugs(anon) == original, "original order not restored"


def test_sitemap_lists_live_profiles_and_robots_names_sitemap():
    """The sitemap lists public routes and every live profile; robots names it and disallows signed-in routes."""
    sitemap = raw_get("/sitemap.xml")
    assert sitemap.status_code == 200 and "<urlset" in sitemap.text, f"sitemap: {describe(sitemap)}"
    base = appclient.app_url()
    for route in ("/", "/roster", "/join-us", "/about", "/legal/terms-and-conditions") + tuple(
            f"/{s}" for s in DIVISION_SLUGS):
        assert f"{base}{route}</loc>" in sitemap.text, f"sitemap omits {route}"
    for slug in SEEDED_LIVE_SLUGS:
        assert f"{base}/creator/{slug}</loc>" in sitemap.text, f"sitemap omits {slug}"
    assert f"/creator/{DRAFT_SLUG}" not in sitemap.text, "sitemap lists the draft"
    robots = raw_get("/robots.txt")
    assert robots.status_code == 200, describe(robots)
    lines = [line.strip() for line in robots.text.splitlines()]
    assert f"Sitemap: {base}/sitemap.xml" in lines, f"robots sitemap line: {robots.text[:300]}"
    for path in ("/you", "/sign-in", "/api/"):
        assert f"Disallow: {path}" in lines, f"robots does not disallow {path}"


def test_notices_carry_titles_and_bodies(anon):
    """The three notices answer their titles with non-empty bodies and an unknown kind is 404."""
    for kind, title in NOTICES:
        body = json_object(anon.get(f"/notices/{kind}"), f"notice {kind}")
        assert body.get("title") == title and str(body.get("body", "")).strip(), f"notice {kind}: {body}"
        parse_moment(body.get("updated_at"))
    assert anon.get("/notices/refunds").status_code == 404, "an unknown notice kind answered"


def test_security_headers_on_every_response():
    """The shell, an API read and a file answer carry the four security headers."""
    for route in ("/", "/api/site", "/robots.txt"):
        response = raw_get(route)
        headers = response.headers
        assert headers.get("x-frame-options", "").upper() == "DENY", f"{route} frame options {headers}"
        assert headers.get("x-content-type-options", "").lower() == "nosniff", f"{route} sniffing"
        assert headers.get("referrer-policy", "").lower() == "same-origin", f"{route} referrer policy"
        assert "includesubdomains" in headers.get("strict-transport-security", "").lower(), f"{route} hsts"


def test_browser_bundle_carries_no_secret():
    """No script the browser downloads carries the database address or credentials."""
    shell = raw_get("/")
    assert shell.status_code == 200, describe(shell)
    scripts = re.findall(r'<script[^>]+src="([^"]+)"', shell.text)
    assert scripts, "the shell loads no script"
    for src in scripts:
        url = src if src.startswith("http") else f"{appclient.app_url()}/{src.lstrip('/')}"
        text = httpx.get(url, timeout=appclient.TIMEOUT).text
        for secret in ("postgresql://", "deku-local-dev", "DATABASE_URL", "deku_admin"):
            assert secret not in text, f"{src} carries {secret}"


def test_front_door_is_one_window_tall_at_every_width(browser):
    """The front door reaches data-arrival done and never scrolls at wide and narrow widths."""
    for viewport in (WIDE_VIEWPORT, NARROW_VIEWPORT):
        context = browser.new_context(viewport=viewport)
        tab = context.new_page()
        open_route(tab, "/")
        metrics = page_metrics(tab)
        context.close()
        assert metrics["scrollHeight"] <= metrics["innerHeight"], f"front door scrolls at {viewport}: {metrics}"


def test_narrow_viewport_never_scrolls_sideways(narrow_page):
    """At a narrow viewport the roster, a division and join us never scroll sideways."""
    for route in ("/roster", "/creator-media", "/join-us", "/creator/juno-okafor"):
        open_route(narrow_page, route)
        metrics = page_metrics(narrow_page)
        assert metrics["scrollWidth"] <= metrics["innerWidth"], f"{route} scrolls sideways: {metrics}"


def test_each_page_has_one_primary_action(page):
    """Each page marks exactly one primary action, About Us on the front door."""
    for route in ("/", "/creator-media", "/roster", "/join-us", "/creator/juno-okafor"):
        open_route(page, route)
        count = page.locator("[data-primary-action]").count()
        assert count == 1, f"{route} marks {count} primary actions"
    open_route(page, "/")
    assert page.locator("[data-primary-action]").inner_text().strip() == "About Us", "front door primary action"


def test_terms_page_linked_from_every_footer(page):
    """The footer on a division and the roster links Terms & Conditions to its notice route."""
    for route in ("/creator-media", "/roster"):
        open_route(page, route)
        link = page.get_by_role("contentinfo").get_by_role("link", name=re.compile("Terms"))
        assert link.get_attribute("href").rstrip("/").endswith("/legal/terms-and-conditions"), f"{route} terms link"
    open_route(page, "/legal/terms-and-conditions")
    page.get_by_role("heading", name="Terms & Conditions").first.wait_for(timeout=15000)


def test_headline_reads_as_one_accessible_sentence(page):
    """The headline is one first-level heading named with the whole sentence; the wordmark is named Halden."""
    open_route(page, "/")
    heading = page.get_by_role("heading", level=1, name=HEADLINE, exact=True)
    assert heading.count() == 1, "the headline is not one accessible sentence"
    assert page.get_by_role("link", name=WORDMARK_NAME, exact=True).count() >= 1, "wordmark not named Halden"


def test_armillary_keys_step_segments_and_enter_opens_division(page):
    """The armillary opens on creator-media, steps and wraps with arrows, and Enter opens the division."""
    open_route(page, "/")
    region = page.locator("[data-acquired]").first
    assert region.get_attribute("data-acquired") == "creator-media", "the armillary did not open at rest"
    region.focus()
    page.keyboard.press("ArrowRight")
    page.wait_for_function("() => document.querySelector('[data-acquired]').dataset.acquired === 'creator-communities'")
    for _ in range(3):
        page.keyboard.press("ArrowRight")
    page.wait_for_function("() => document.querySelector('[data-acquired]').dataset.acquired === 'creator-media'")
    page.keyboard.press("ArrowLeft")
    page.wait_for_function("() => document.querySelector('[data-acquired]').dataset.acquired === 'creator-tech'")
    page.keyboard.press("Enter")
    page.wait_for_url(re.compile(r"/creator-tech/?$"), timeout=20000)


def test_front_door_fetches_nothing_from_another_origin(page):
    """Loading the front door requests nothing from another origin and opens no live connection."""
    hosts, sockets = [], []
    page.on("request", lambda request: hosts.append(urlparse(request.url).netloc))
    page.on("websocket", lambda socket: sockets.append(socket.url))
    open_route(page, "/")
    settle(3.0)
    own = urlparse(appclient.app_url()).netloc
    foreign = sorted({h for h in hosts if h and h != own})
    assert not foreign, f"the front door fetched from other origins: {foreign}"
    assert not sockets, f"the front door opened live connections: {sockets}"


def test_mode_follows_system_then_persists(browser):
    """With nothing stored the mode follows the system preference; a toggle persists under mode."""
    context = browser.new_context(viewport=WIDE_VIEWPORT, color_scheme="light")
    tab = context.new_page()
    open_route(tab, "/")
    assert tab.evaluate("document.documentElement.dataset.mode") == "light", "mode ignored the system preference"
    tab.get_by_role("button", name=re.compile("light|dark|mode", re.I)).first.click()
    tab.wait_for_function("() => document.documentElement.dataset.mode === 'dark'")
    tab.reload()
    tab.wait_for_selector('html[data-arrival="done"]', state="attached", timeout=45000)
    assert tab.evaluate("document.documentElement.dataset.mode") == "dark", "mode choice did not persist"
    assert tab.evaluate(STORED_JS, "mode") == "dark", "mode not kept under the key mode"
    context.close()


def test_sketch_mode_persists_with_identical_text(page):
    """SKETCH MODE sets data-sketch on, persists under sketch, and keeps the same proposition text."""
    open_route(page, "/creator-tech")
    proposition = DIVISIONS[3][3]
    assert page.get_by_text(proposition).count() >= 1, "proposition missing before sketch mode"
    assert page.evaluate("document.documentElement.dataset.sketch") == "off", "sketch mode did not start off"
    page.get_by_text("SKETCH MODE", exact=True).first.click()
    page.wait_for_function("() => document.documentElement.dataset.sketch === 'on'")
    page.reload()
    page.wait_for_selector('html[data-sketch="on"]', state="attached", timeout=45000)
    assert page.evaluate(STORED_JS, "sketch") is not None, "sketch not kept under sketch"
    assert page.get_by_text(proposition).count() >= 1, "sketch mode changed the proposition text"


def test_roster_cards_carry_division_hook(page):
    """Every roster card link carries data-division with a known division slug."""
    open_route(page, "/roster")
    page.locator("a[href*='/creator/']").first.wait_for(timeout=20000)
    cards = page.locator("[data-division]")
    assert cards.count() >= len(SEEDED_LIVE), f"only {cards.count()} cards carry data-division"
    values = set(cards.evaluate_all("els => els.map(e => e.dataset.division)"))
    assert values <= set(DIVISION_SLUGS), f"unknown division hooks {values}"


def test_consent_decline_records_no_site_events(browser, backend):
    """After No thanks nothing reaches site_events; after Accept All events are stored."""
    context = browser.new_context(viewport=WIDE_VIEWPORT)
    tab = context.new_page()
    before = site_event_count(backend)
    open_route(tab, "/creator-media")
    tab.get_by_role("button", name="No thanks").click()
    assert tab.evaluate(STORED_JS, "consent") == "declined", "decline not stored"
    for route in ("/roster", "/creator/juno-okafor", "/creator-tech"):
        open_route(tab, route)
    settle(3.0)
    assert site_event_count(backend) == before, "site events stored after No thanks"
    context.close()
    context = browser.new_context(viewport=WIDE_VIEWPORT)
    tab = context.new_page()
    open_route(tab, "/creator-media")
    tab.get_by_role("button", name="Accept All").click()
    for route in ("/roster", "/creator/juno-okafor"):
        open_route(tab, route)
    settle(3.0)
    assert site_event_count(backend) > before, "no site events stored after Accept All"
    context.close()


def test_site_events_accept_closed_names_only(anon, backend):
    """A closed event name answers 204 and is stored; an unknown name answers 400."""
    before = site_event_count(backend)
    stored = anon.post("/events", json={"name": EVENT_NAMES[1], "properties": {"division": "creator-media"}})
    assert stored.status_code == 204, describe(stored)
    assert site_event_count(backend) == before + 1, "the event was not stored"
    error_body(anon.post("/events", json={"name": "page_scrolled", "properties": {}}), 400,
               "validation_failed", "unknown event name")
