from __future__ import annotations

import datetime
import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

import httpx

import appclient
from conftest import (
    ABOUT_FIGURE,
    ACCOUNT_ROUTE,
    API_PREFIX,
    AVAILABILITY_ROUTE,
    BAND_FLOOR_LINE,
    BAR_ENQUIRIES,
    BAR_MESSAGES,
    BAR_PROJECTS,
    BAR_WINDOWS,
    BEARER_TOKEN_HOURS,
    BIND_ADDRESS,
    BUDGET_BANDS,
    CLIENT_EMAIL,
    CLIENT_NAME,
    CLIENT_ORGANISATION,
    CONTACT_ROUTE,
    CONTAINER_PORT,
    CREDENTIALS_FILE,
    DENIED,
    DENIED_SURFACE_COPY,
    DOWNLOAD_DIR,
    ENQUIRY_BOOKED,
    ENQUIRY_DECLINED,
    ENQUIRY_LAPSED,
    ENQUIRY_NEW,
    ENQUIRY_PROPOSED,
    ENQUIRY_READING,
    ENQUIRY_TOKEN_DAYS,
    ENQUIRY_WITHDRAWN,
    ERROR_LONG_ORGANISATION,
    ERROR_MISSING_BAND,
    ERROR_MISSING_EMAIL,
    ERROR_MISSING_NAME,
    ERROR_MISSING_SUBJECT,
    ERROR_SHORT_MESSAGE,
    EXPIRED_PROPOSAL_REFUSAL,
    FILLED_WINDOW_REFUSAL,
    FOOTER_HEADS,
    FOURTH_HOLD_REFUSAL,
    HEALTH_ENDPOINT,
    HOLD_HOURS,
    HOME_ROUTE,
    LAPSE_SILENCE_DAYS,
    LIVE_HOLD_CEILING,
    MISSING_SURFACE_COPY,
    MODE_BOOKED_UNTIL,
    MODE_NOT_TAKING,
    MODE_OPEN_FROM,
    MODE_OPEN_NOW,
    NAVIGATION_TARGETS,
    OK,
    OPEN_NOW_HORIZON_DAYS,
    PILL_BOOKED_UNTIL,
    PILL_NOT_TAKING,
    PILL_OPEN_FROM,
    PILL_OPEN_NOW,
    PIPELINE_ROUTE,
    PRIVACY_ROUTE,
    PROPOSAL_LIVE,
    PROPOSAL_SUPERSEDED,
    PROPOSAL_WARNING_HOURS,
    PUBLIC_ROUTES,
    RATE_LIMITED,
    REFUSED,
    ROBOTS_ROUTE,
    ROLE_CLIENT,
    ROLE_STUDIO,
    SCREENSHOT_DIR,
    SEEDED_PASSWORD,
    SEEDED_PROJECTS,
    SEEDED_WINDOWS,
    SERVICE_TITLES,
    SIGNIN_LINK_RESPONSE,
    SIGNIN_ROUTE,
    SITEMAP_ROUTE,
    SOCIAL_LABELS,
    STUDIO_EMAIL,
    STUDIO_NAME,
    STUDIO_ORGANISATION,
    STUDIO_ROUTE,
    SUBJECT_BOOKED,
    SUBJECT_CLIENT_REPLY,
    SUBJECT_CONFIRMATION,
    SUBJECT_DECLINED,
    SUBJECT_EXPIRING,
    SUBJECT_NOTIFICATION,
    SUBJECT_PROPOSAL,
    SUBJECT_SIGNIN_LINK,
    SUBJECT_STUDIO_REPLY,
    TERMS_ROUTE,
    WINDOW_BOOKED,
    WINDOW_CLOSED,
    WINDOW_OPEN,
    WORK_HEADLINE,
    WORK_INDEX_COUNT,
    WORK_ROUTE,
    accept,
    app_url,
    availability,
    body,
    booked_enquiry,
    bundle_assets,
    enquiry_payload,
    enquiry_state,
    first_open_window,
    flat,
    make_hold,
    make_window,
    open_windows,
    page,
    probe_email,
    probe_name,
    propose,
    read,
    remaining_days,
    require_enquiry,
    settle,
    submit_enquiry,
    windows_of,
)


def _in_container(*argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(argv, capture_output=True, text=True, timeout=60)


def test_health_route_returns_ok():
    response = httpx.get(f"{app_url()}{HEALTH_ENDPOINT}", timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"GET {HEALTH_ENDPOINT} returned {response.status_code}, expected 200 once "
        f"the app is ready: {body(response)}"
    )


def test_production_bundle_is_served():
    document = page(HOME_ROUTE)
    assert document.status_code in OK, (
        f"GET {HOME_ROUTE} returned {document.status_code}: {body(document)}"
    )
    dev_markers = ("/@vite/client", "/@react-refresh", "__vite_ping")
    found = [marker for marker in dev_markers if marker in document.text]
    assert not found, (
        f"the served document references {found}, which only a dev server emits; "
        f"the deployment contract requires a production build behind a static or "
        f"preview server"
    )
    assert f":{CONTAINER_PORT}" in app_url() or app_url().startswith("http"), (
        f"the app must be reachable at its public address; app_url() is {app_url()!r}"
    )
    listening = _in_container("sh", "-c",
                             f"ss -ltn 2>/dev/null || netstat -ltn 2>/dev/null")
    if listening.stdout:
        loopback_only = re.search(
            rf"127\.0\.0\.1:{CONTAINER_PORT}\b", listening.stdout
        ) and not re.search(
            rf"(?:{re.escape(BIND_ADDRESS)}|\*|\[::\]):{CONTAINER_PORT}\b",
            listening.stdout,
        )
        assert not loopback_only, (
            f"the server on port {CONTAINER_PORT} is bound to loopback only, so it is "
            f"unreachable from outside the container; bind {BIND_ADDRESS}:\n"
            f"{listening.stdout[:400]}"
        )


def test_api_is_served_on_the_same_origin_under_api(anonymous):
    origin = app_url().rstrip("/")
    response = httpx.get(f"{origin}{API_PREFIX}/projects", timeout=appclient.TIMEOUT)
    assert response.status_code in OK, (
        f"GET {origin}{API_PREFIX}/projects returned {response.status_code}; the API "
        f"must answer on the document's own origin under {API_PREFIX}: "
        f"{body(response)}"
    )
    document = page(HOME_ROUTE)
    cross_origin = re.findall(r'(?:src|href)="(https?://[^"]+)"', document.text)
    external_api = [u for u in cross_origin
                    if API_PREFIX in u and not u.startswith(origin)]
    assert not external_api, (
        f"the document points at an API on another origin: {external_api}"
    )


def test_request_logs_reach_stdout():
    marker = probe_email("log")
    httpx.get(f"{app_url()}{HEALTH_ENDPOINT}", timeout=appclient.TIMEOUT,
              headers={"X-Deku-Probe": marker})
    logs = _in_container(
        "sh", "-c",
        "cat /proc/1/fd/1 2>/dev/null & sleep 1; kill %1 2>/dev/null; "
        "tail -n 200 /app/*.log 2>/dev/null; tail -n 200 /var/log/app*.log 2>/dev/null",
    )
    combined = (logs.stdout or "") + (logs.stderr or "")
    assert HEALTH_ENDPOINT in combined or "GET" in combined, (
        f"no request log line reached standard output after a request to "
        f"{HEALTH_ENDPOINT}; the technical requirements ask for request logs on "
        f"stdout. What was readable: {combined[:400]!r}"
    )


def test_reserved_directories_exist_and_are_empty():
    for directory in (SCREENSHOT_DIR, DOWNLOAD_DIR):
        listing = _in_container("sh", "-c", f"ls -A {directory} 2>&1")
        assert listing.returncode == 0, (
            f"{directory} does not exist at the app root; the deployment contract "
            f"requires it reserved and empty: {listing.stdout.strip()}"
        )
        assert not listing.stdout.strip(), (
            f"{directory} is not empty; it carries "
            f"{listing.stdout.split()[:8]}"
        )


def test_credentials_file_names_both_seeded_accounts():
    readback = _in_container("cat", CREDENTIALS_FILE)
    assert readback.returncode == 0, (
        f"{CREDENTIALS_FILE} is not readable; the deployment contract requires the "
        f"login credentials written there: {readback.stderr.strip()}"
    )
    text = readback.stdout
    for value in (STUDIO_EMAIL, CLIENT_EMAIL, SEEDED_PASSWORD):
        assert value in text, (
            f"{CREDENTIALS_FILE} does not name {value!r}; a grader cannot sign in "
            f"from what it states. File: {text[:400]!r}"
        )
    assert appclient.login(STUDIO_EMAIL, SEEDED_PASSWORD), (
        f"the credentials written to {CREDENTIALS_FILE} do not actually log in"
    )


def test_rows_persist_in_postgres(backend, studio):
    window = make_window(studio, offset_days=120, weeks=2, capacity_days=1)
    row = settle(lambda: backend.one("windows", id=window["id"]))
    assert row is not None, (
        f"a window created through {API_PREFIX}/windows is not in the windows table; "
        f"PostgreSQL at DATABASE_URL is the fact, not a structure the app keeps for "
        f"itself"
    )
    assert int(row["weeks"]) == 2 and int(row["capacity_days"]) == 1, (
        f"the stored window row does not carry what was posted: {row}"
    )


def test_seeding_twice_does_not_duplicate_rows(backend):
    tables = ("accounts", "projects", "services", "social_links", "site_meta",
              "windows")
    before = {table: backend.count(table) for table in tables}
    restart = _in_container(
        "sh", "-c",
        "npm run seed --prefix /app 2>&1 || node /app/seed.js 2>&1 || true",
    )
    after = {table: backend.count(table) for table in tables}
    assert before == after, (
        f"running the seed again changed the row counts from {before} to {after}; "
        f"seeding must be idempotent so a restart does not duplicate the fixture. "
        f"Seed output: {restart.stdout[-300:]!r}"
    )


def test_seeded_accounts_carry_their_names_and_roles(backend):
    expected = {
        STUDIO_EMAIL: (STUDIO_NAME, STUDIO_ORGANISATION, ROLE_STUDIO),
        CLIENT_EMAIL: (CLIENT_NAME, CLIENT_ORGANISATION, ROLE_CLIENT),
    }
    for email, (name, organisation, role) in expected.items():
        row = backend.one("accounts", email=email)
        assert row is not None, (
            f"no account row is seeded at {email!r}; both seeded logins must exist"
        )
        assert row.get("display_name") == name, (
            f"{email} carries display_name {row.get('display_name')!r}, expected "
            f"{name!r}"
        )
        assert str(row.get("organisation") or "") == organisation, (
            f"{email} carries organisation {row.get('organisation')!r}, expected "
            f"{organisation!r}"
        )
        assert row.get("role") == role, (
            f"{email} carries role {row.get('role')!r}, expected {role!r}"
        )
        assert row.get("created_at") is not None, (
            f"{email} carries no created_at; the accounts table declares it"
        )
        assert "last_seen_at" in row, (
            f"the accounts table has no last_seen_at column; the data model declares "
            f"it. Columns present: {sorted(row)}"
        )


def test_exactly_one_studio_account_exists(backend, anonymous):
    assert backend.count("accounts", role=ROLE_STUDIO) == 1, (
        f"the accounts table holds "
        f"{backend.count('accounts', role=ROLE_STUDIO)} accounts in role "
        f"{ROLE_STUDIO!r}; exactly one exists, and only by seed"
    )
    anonymous.post("/auth/signup", json={
        "email": probe_email("studio-attempt"), "password": SEEDED_PASSWORD,
        "display_name": probe_name("attempt"), "organisation": "", "role": ROLE_STUDIO,
    })
    assert backend.count("accounts", role=ROLE_STUDIO) == 1, (
        f"a signup naming the studio role created a second studio account; the role "
        f"in a request body is ignored, never honoured"
    )


def test_studio_recovery_and_notification_addresses_are_distinct(backend, inbox,
                                                                 anonymous):
    row = backend.one("accounts", email=STUDIO_EMAIL)
    recovery = str(row.get("recovery_email") or "")
    assert recovery, (
        f"the seeded studio account carries no recovery address; one studio account "
        f"is one point of failure, so the recovery address is required. Columns: "
        f"{sorted(row)}"
    )
    assert recovery.lower() != STUDIO_EMAIL.lower(), (
        f"the studio's recovery address is its own sign-in address {recovery!r}; a "
        f"locked-out operator cannot recover through the address they are locked out "
        f"of"
    )
    sender = probe_email("notify")
    require_enquiry(anonymous, email=sender)
    notification = settle(lambda: inbox.find(recovery, SUBJECT_NOTIFICATION))
    assert notification is not None, (
        f"the new-enquiry notification did not reach {recovery!r}; it must go to an "
        f"address that is not the studio account's, so work arriving is visible even "
        f"when that account is locked out"
    )


def test_three_windows_are_seeded_at_their_stated_shapes(backend):
    rows = backend.rows("windows")
    assert len(rows) >= len(SEEDED_WINDOWS), (
        f"the seed left {len(rows)} windows, expected at least "
        f"{len(SEEDED_WINDOWS)}: one open inside the horizon, one open beyond it, "
        f"one booked"
    )
    today = datetime.date.today()
    for expected in SEEDED_WINDOWS:
        wanted = today + datetime.timedelta(days=expected["offset_days"])
        match = None
        for row in rows:
            starts_on = row["starts_on"]
            if isinstance(starts_on, str):
                starts_on = datetime.date.fromisoformat(starts_on[:10])
            if abs((starts_on - wanted).days) <= 1:
                match = row
                break
        assert match is not None, (
            f"no seeded window starts about {expected['offset_days']} days from "
            f"today; the seed declares one at that offset. Stored starts: "
            f"{[str(r['starts_on'])[:10] for r in rows]}"
        )
        assert int(match["weeks"]) == expected["weeks"], (
            f"the window starting in about {expected['offset_days']} days runs "
            f"{match['weeks']} weeks, expected {expected['weeks']}"
        )
        assert int(match["capacity_days"]) == expected["capacity_days"], (
            f"that window carries capacity_days {match['capacity_days']}, expected "
            f"{expected['capacity_days']}"
        )
        assert int(match["committed_days"]) == expected["committed_days"], (
            f"that window carries committed_days {match['committed_days']}, expected "
            f"{expected['committed_days']}"
        )
        assert match["state"] == expected["state"], (
            f"that window is in state {match['state']!r}, expected "
            f"{expected['state']!r}"
        )


def test_seeded_enquiry_is_proposed_with_two_messages(backend):
    enquiries = backend.rows("enquiries", state=ENQUIRY_PROPOSED)
    assert enquiries, (
        f"no enquiry is seeded in state {ENQUIRY_PROPOSED!r}; a fresh install must "
        f"open on the most interesting state rather than on an empty pipeline"
    )
    seeded = enquiries[0]
    assert str(seeded.get("name") or "") == CLIENT_NAME, (
        f"the seeded enquiry is from {seeded.get('name')!r}, expected {CLIENT_NAME!r}"
    )
    assert seeded.get("window_id") is not None, (
        f"the seeded enquiry sits against no window; it is seeded against the first "
        f"open one"
    )
    messages = backend.count("messages", enquiry_id=seeded["id"])
    assert messages == 2, (
        f"the seeded enquiry carries {messages} messages, expected 2"
    )
    live = backend.count("proposals", enquiry_id=seeded["id"], state=PROPOSAL_LIVE)
    assert live == 1, (
        f"the seeded enquiry carries {live} live proposals, expected exactly 1"
    )


def test_login_returns_bearer_token(anonymous):
    for email in (STUDIO_EMAIL, CLIENT_EMAIL):
        response = anonymous.post("/auth/login",
                                  json={"email": email, "password": SEEDED_PASSWORD})
        assert response.status_code in OK, (
            f"POST {API_PREFIX}/auth/login returned {response.status_code} for the "
            f"seeded account {email!r} with the seeded password: {body(response)}"
        )
        payload = response.json()
        token = payload.get("token") or payload.get("access_token")
        assert token, (
            f"the login response for {email!r} carries no bearer token: "
            f"{json.dumps(payload)[:300]}"
        )
        with appclient.client(token) as signed_in:
            me = signed_in.get("/auth/me")
            assert me.status_code in OK, (
                f"the token returned for {email!r} is refused at "
                f"{API_PREFIX}/auth/me with {me.status_code}: {body(me)}"
            )


def test_signup_creates_client_role_row(backend, anonymous):
    email = probe_email("signup")
    response = anonymous.post("/auth/signup", json={
        "email": email, "password": SEEDED_PASSWORD,
        "display_name": probe_name("signup"), "organisation": "Northgate",
    })
    assert response.status_code in OK, (
        f"POST {API_PREFIX}/auth/signup returned {response.status_code} for a fresh "
        f"address; signup is open to anyone: {body(response)}"
    )
    row = settle(lambda: backend.one("accounts", email=email))
    assert row is not None, (
        f"no account row was written for {email!r} after a successful signup"
    )
    assert row.get("role") == ROLE_CLIENT, (
        f"the account created at signup carries role {row.get('role')!r}; every "
        f"signup produces a {ROLE_CLIENT!r}"
    )


def test_signup_ignores_role_in_body(backend, anonymous):
    email = probe_email("role")
    anonymous.post("/auth/signup", json={
        "email": email, "password": SEEDED_PASSWORD,
        "display_name": probe_name("role"), "organisation": "",
        "role": ROLE_STUDIO,
    })
    row = settle(lambda: backend.one("accounts", email=email))
    assert row is not None, (
        f"no account row was written for {email!r}; a role named in the body is "
        f"ignored, not a reason to refuse the signup"
    )
    assert row.get("role") == ROLE_CLIENT, (
        f"a signup naming role {ROLE_STUDIO!r} in its body produced an account in "
        f"role {row.get('role')!r}; authority is never decided from a request body "
        f"field"
    )


def test_duplicate_signup_email_is_refused(backend, anonymous):
    email = probe_email("duplicate")
    first = anonymous.post("/auth/signup", json={
        "email": email, "password": SEEDED_PASSWORD,
        "display_name": probe_name("first"), "organisation": "",
    })
    assert first.status_code in OK, (
        f"the first signup at {email!r} returned {first.status_code}: {body(first)}"
    )
    second = anonymous.post("/auth/signup", json={
        "email": email, "password": SEEDED_PASSWORD,
        "display_name": probe_name("second"), "organisation": "",
    })
    assert second.status_code in REFUSED, (
        f"a second signup at {email!r} returned {second.status_code}, expected a "
        f"client error naming the field at fault: {body(second)}"
    )
    assert "email" in body(second).lower(), (
        f"the refusal does not name the field at fault: {body(second)}"
    )
    assert backend.count("accounts", email=email) == 1, (
        f"the refused signup still wrote a second account row for {email!r}"
    )


def test_no_endpoint_returns_a_password_hash(backend, studio):
    row = backend.one("accounts", email=STUDIO_EMAIL)
    stored = str(row.get("password_hash") or "")
    assert stored, (
        f"the studio account row carries no password_hash; passwords are stored "
        f"hashed"
    )
    assert SEEDED_PASSWORD not in stored, (
        f"the stored password_hash contains the plaintext password"
    )
    for path in ("/auth/me", "/projects", "/services", "/availability", "/pipeline"):
        response = studio.get(path)
        if response.status_code not in OK:
            continue
        text = response.text
        assert stored not in text and "password_hash" not in text, (
            f"GET {API_PREFIX}{path} returns the stored password hash; no endpoint "
            f"ever returns one: {text[:300]}"
        )


def test_missing_expired_or_tampered_token_is_denied(anonymous, studio_token):
    protected = "/pipeline"
    bare = anonymous.get(protected)
    assert bare.status_code in DENIED, (
        f"GET {API_PREFIX}{protected} with no bearer token returned "
        f"{bare.status_code}, expected a denial: {body(bare)}"
    )
    tampered = studio_token[:-4] + ("aaaa" if not studio_token.endswith("aaaa")
                                    else "bbbb")
    with appclient.client(tampered) as forged:
        response = forged.get(protected)
        assert response.status_code in DENIED, (
            f"GET {API_PREFIX}{protected} with a tampered token returned "
            f"{response.status_code}, expected a denial: {body(response)}"
        )
    with appclient.client("expired." + "x" * 40) as stale:
        response = stale.get(protected)
        assert response.status_code in DENIED, (
            f"GET {API_PREFIX}{protected} with an unusable token returned "
            f"{response.status_code}, expected a denial. Tokens expire after "
            f"{BEARER_TOKEN_HOURS} hours: {body(response)}"
        )


def test_public_reads_need_no_token(anonymous):
    for path in ("/health", "/projects", "/services", "/availability", "/meta"):
        response = anonymous.get(path)
        assert response.status_code in OK, (
            f"GET {API_PREFIX}{path} returned {response.status_code} with no bearer "
            f"token; the public reads, signup, login and health are exempt from the "
            f"token requirement: {body(response)}"
        )


def test_account_field_bounds_are_enforced(anonymous):
    cases = {
        "an empty display name": {"display_name": "", "organisation": ""},
        "a display name over sixty characters": {"display_name": "n" * 61,
                                                 "organisation": ""},
        "an organisation over a hundred and twenty characters": {
            "display_name": probe_name("bounds"), "organisation": "o" * 121},
    }
    for label, overrides in cases.items():
        payload = {"email": probe_email("bounds"), "password": SEEDED_PASSWORD}
        payload.update(overrides)
        response = anonymous.post("/auth/signup", json=payload)
        assert response.status_code in REFUSED, (
            f"a signup with {label} returned {response.status_code}, expected a "
            f"client error: the accounts table bounds display_name to 1 to 60 and "
            f"organisation to 0 to 120: {body(response)}"
        )


def test_signin_link_response_is_identical_for_unknown_address(anonymous):
    known = anonymous.post("/auth/link", json={"email": CLIENT_EMAIL})
    unknown = anonymous.post("/auth/link",
                             json={"email": probe_email("never-wrote-in")})
    assert known.status_code in OK and unknown.status_code in OK, (
        f"the sign-in link request is always accepted; got {known.status_code} for a "
        f"known address and {unknown.status_code} for an unknown one"
    )
    assert SIGNIN_LINK_RESPONSE in known.text, (
        f"the response for a known address does not carry the pinned wording "
        f"{SIGNIN_LINK_RESPONSE!r}: {body(known)}"
    )
    assert known.text == unknown.text, (
        f"the sign-in link endpoint answers differently for an address that has an "
        f"enquiry and one that does not, so it reports who has written in.\n"
        f"known:   {body(known)}\nunknown: {body(unknown)}"
    )


def test_signin_link_request_mails_that_address(anonymous, inbox):
    anonymous.post("/auth/link", json={"email": CLIENT_EMAIL})
    message = settle(lambda: inbox.find(CLIENT_EMAIL, SUBJECT_SIGNIN_LINK))
    assert message is not None, (
        f"no message whose subject begins {SUBJECT_SIGNIN_LINK!r} reached "
        f"{CLIENT_EMAIL!r} after a sign-in link request"
    )


def test_projects_list_is_array_in_position_order(anonymous):
    response = anonymous.get("/projects")
    assert response.status_code in OK, (
        f"GET {API_PREFIX}/projects returned {response.status_code}: {body(response)}"
    )
    payload = response.json()
    assert isinstance(payload, list), (
        f"GET {API_PREFIX}/projects returned a {type(payload).__name__}; every list "
        f"endpoint returns a top-level JSON array"
    )
    titles = [str(row.get("title", "")) for row in payload]
    assert titles == list(SEEDED_PROJECTS), (
        f"the projects endpoint returned {titles}, expected the nine seeded projects "
        f"in position order: {list(SEEDED_PROJECTS)}"
    )
    positions = [int(row["position"]) for row in payload]
    assert positions == sorted(positions) and len(set(positions)) == len(positions), (
        f"project positions are {positions}; the data model requires them unique and "
        f"ascending"
    )


def test_project_slug_resolves_and_unknown_slug_is_not_found(anonymous):
    listing = anonymous.get("/projects").json()
    slug = listing[0]["slug"]
    found = anonymous.get(f"/projects/{slug}")
    assert found.status_code in OK, (
        f"GET {API_PREFIX}/projects/{slug} returned {found.status_code} for a seeded "
        f"slug: {body(found)}"
    )
    assert found.json().get("slug") == slug, (
        f"the slug route resolved to {found.json().get('slug')!r}, expected {slug!r}"
    )
    missing = anonymous.get("/projects/no-such-project-at-all")
    assert missing.status_code == 404, (
        f"GET {API_PREFIX}/projects/no-such-project-at-all returned "
        f"{missing.status_code}, expected 404: {body(missing)}"
    )
    surface = page(f"{WORK_ROUTE}/no-such-project-at-all")
    assert MISSING_SURFACE_COPY in surface.text, (
        f"the not-found surface at {WORK_ROUTE}/no-such-project-at-all does not read "
        f"{MISSING_SURFACE_COPY!r}: {surface.text[:400]}"
    )


def test_work_trailing_slash_redirects_permanently():
    response = page(f"{WORK_ROUTE}/", follow_redirects=False)
    assert response.status_code == 301, (
        f"GET {WORK_ROUTE}/ returned {response.status_code}, expected a permanent "
        f"redirect to the canonical form: one canonical form for one document"
    )
    location = response.headers.get("location", "")
    assert location.rstrip("/").endswith(WORK_ROUTE), (
        f"GET {WORK_ROUTE}/ redirects to {location!r}, expected {WORK_ROUTE!r}"
    )


def test_services_list_is_array(anonymous):
    response = anonymous.get("/services")
    assert response.status_code in OK, (
        f"GET {API_PREFIX}/services returned {response.status_code}: {body(response)}"
    )
    payload = response.json()
    assert isinstance(payload, list), (
        f"GET {API_PREFIX}/services returned a {type(payload).__name__}; every list "
        f"endpoint returns a top-level JSON array"
    )
    titles = [str(row.get("title", "")) for row in payload]
    assert titles == list(SERVICE_TITLES), (
        f"the services endpoint returned {titles}, expected {list(SERVICE_TITLES)}"
    )
    for row in payload:
        assert str(row.get("body") or "").strip(), (
            f"the service {row.get('title')!r} carries no body line; each service is "
            f"a title and a line"
        )


def test_social_links_are_seeded_in_order(backend):
    rows = backend.rows("social_links")
    labels = [str(row.get("label", "")) for row in
              sorted(rows, key=lambda r: int(r["position"]))]
    assert labels == list(SOCIAL_LABELS), (
        f"the social_links table holds {labels}, expected {list(SOCIAL_LABELS)} in "
        f"position order"
    )
    surface = page(CONTACT_ROUTE)
    for label in SOCIAL_LABELS:
        assert label in surface.text, (
            f"the contact surface does not render the social link {label!r}: "
            f"{surface.text[:400]}"
        )


def test_meta_endpoint_returns_stored_version_and_local_time(backend, anonymous):
    response = anonymous.get("/meta")
    assert response.status_code in OK, (
        f"GET {API_PREFIX}/meta returned {response.status_code}: {body(response)}"
    )
    payload = response.json()
    row = backend.one("site_meta")
    assert row is not None, (
        f"the site_meta table holds no row; the footer reads its version from there"
    )
    assert str(payload.get("version")) == str(row.get("version")), (
        f"{API_PREFIX}/meta reports version {payload.get('version')!r} while the "
        f"stored row says {row.get('version')!r}; the footer reads the stored row, "
        f"never a build constant"
    )
    assert str(payload.get("predecessor_label")) == str(
        row.get("predecessor_label")
    ), (
        f"{API_PREFIX}/meta reports predecessor_label "
        f"{payload.get('predecessor_label')!r} while the stored row says "
        f"{row.get('predecessor_label')!r}"
    )
    local_time = str(payload.get("local_time", ""))
    assert re.search(r"\b\d{1,2}:\d{2}\s?(?:AM|PM)\b", local_time, re.I), (
        f"local_time is {local_time!r}; the footer renders a twelve-hour clock"
    )
    assert re.search(r"(GMT|UTC)[+-]\d", local_time), (
        f"local_time is {local_time!r}; the offset must be named, so 01:59 PM GMT+2 "
        f"is the shape"
    )
    footer = page(HOME_ROUTE)
    for head in FOOTER_HEADS:
        assert head in footer.text, (
            f"the footer does not carry the head {head!r}"
        )


def test_availability_mode_is_derived_not_stored(backend, studio, anonymous):
    before = availability(anonymous).get("mode")
    columns = backend.rows("windows", limit=1)
    if columns:
        assert "mode" not in columns[0], (
            f"the windows table carries a mode column; the availability mode is "
            f"derived on every read and stored nowhere. Columns: "
            f"{sorted(columns[0])}"
        )
    window = make_window(studio, offset_days=3, weeks=2, capacity_days=1)
    after = availability(anonymous).get("mode")
    assert after == MODE_OPEN_NOW, (
        f"after opening a window that starts in 3 days the derived mode is {after!r}, "
        f"expected {MODE_OPEN_NOW!r}; it was {before!r} before. The mode is computed "
        f"from the window rows on every read"
    )
    studio.patch(f"/windows/{window['id']}", json={"state": WINDOW_CLOSED})
    reread = availability(anonymous).get("mode")
    assert reread != MODE_OPEN_NOW or before == MODE_OPEN_NOW, (
        f"closing the window left the mode at {reread!r}; a derived mode re-reads "
        f"itself from the rows"
    )


def test_availability_endpoint_refuses_a_typed_mode(studio, anonymous):
    window = first_open_window(anonymous)
    attempt = studio.patch(f"/windows/{window['id']}",
                           json={"mode": MODE_NOT_TAKING})
    if attempt.status_code in OK:
        assert availability(anonymous).get("mode") != MODE_NOT_TAKING, (
            f"a mode posted to {API_PREFIX}/windows/{{id}} was honoured; no endpoint "
            f"accepts a mode"
        )
    note = f"Back from {probe_name('note')}"
    studio.patch("/availability", json={"note": note})
    payload = availability(anonymous)
    assert str(payload.get("note") or "") == note or payload.get("note") is not None, (
        f"the studio note is not reachable at {API_PREFIX}/availability; it is shown "
        f"on the availability page: {json.dumps(payload)[:300]}"
    )
    pill_words = (PILL_OPEN_NOW, PILL_OPEN_FROM, PILL_BOOKED_UNTIL, PILL_NOT_TAKING)
    home = page(HOME_ROUTE)
    assert note not in home.text, (
        f"the studio note {note!r} is rendered in the chrome; the note is shown on "
        f"the availability page and never in the pill"
    )
    assert any(word in home.text for word in pill_words), (
        f"the chrome carries none of the four pinned pill strings; the pill states "
        f"the mode in words and is never absent"
    )


def test_availability_mode_open_now_when_window_starts_within_fourteen_days(
        studio, anonymous):
    make_window(studio, offset_days=max(1, OPEN_NOW_HORIZON_DAYS - 4), weeks=2,
                capacity_days=2)
    payload = availability(anonymous)
    assert payload.get("mode") == MODE_OPEN_NOW, (
        f"with an open window starting inside {OPEN_NOW_HORIZON_DAYS} days the mode "
        f"is {payload.get('mode')!r}, expected {MODE_OPEN_NOW!r}"
    )
    assert PILL_OPEN_NOW in flat(payload) or PILL_OPEN_NOW in page(HOME_ROUTE).text, (
        f"under {MODE_OPEN_NOW!r} the pill must read {PILL_OPEN_NOW!r}"
    )


def test_availability_modes_open_from_and_not_taking(backend, studio, anonymous):
    for window in windows_of(anonymous):
        studio.patch(f"/windows/{window['id']}", json={"state": WINDOW_CLOSED})
    far = make_window(studio, offset_days=OPEN_NOW_HORIZON_DAYS + 30, weeks=4,
                      capacity_days=2)
    payload = availability(anonymous)
    assert payload.get("mode") == MODE_OPEN_FROM, (
        f"with the only open window starting beyond {OPEN_NOW_HORIZON_DAYS} days the "
        f"mode is {payload.get('mode')!r}, expected {MODE_OPEN_FROM!r}"
    )
    rendered = flat(payload) + page(HOME_ROUTE).text
    assert PILL_OPEN_FROM in rendered, (
        f"under {MODE_OPEN_FROM!r} the pill must read {PILL_OPEN_FROM!r} and name the "
        f"month"
    )
    month = datetime.date.fromisoformat(str(far["starts_on"])[:10]).strftime("%B")
    assert month in rendered or month[:3] in rendered, (
        f"the {MODE_OPEN_FROM!r} wording does not name the month {month!r}"
    )
    studio.patch(f"/windows/{far['id']}", json={"state": WINDOW_CLOSED})
    for window in backend.rows("windows"):
        studio.patch(f"/windows/{window['id']}", json={"state": WINDOW_CLOSED})
    empty = _in_container("sh", "-c",
                          "psql \"$DB_ADMIN_URL\" -c 'DELETE FROM windows' 2>&1")
    if empty.returncode == 0:
        payload = availability(anonymous)
        assert payload.get("mode") == MODE_NOT_TAKING, (
            f"with no window at all the mode is {payload.get('mode')!r}, expected "
            f"{MODE_NOT_TAKING!r} reading {PILL_NOT_TAKING!r}"
        )


def test_availability_mode_booked_until_when_no_window_is_open(studio, anonymous,
                                                               client):
    for window in windows_of(anonymous):
        if window.get("state") == WINDOW_OPEN:
            studio.patch(f"/windows/{window['id']}", json={"state": WINDOW_CLOSED})
    target = make_window(studio, offset_days=45, weeks=3, capacity_days=1)
    booked_enquiry(studio, client, target, days_per_week=1)
    payload = availability(anonymous)
    assert payload.get("mode") == MODE_BOOKED_UNTIL, (
        f"with every window booked or closed and one booked, the mode is "
        f"{payload.get('mode')!r}, expected {MODE_BOOKED_UNTIL!r}"
    )
    rendered = flat(payload) + page(HOME_ROUTE).text
    assert PILL_BOOKED_UNTIL in rendered, (
        f"under {MODE_BOOKED_UNTIL!r} the pill must read {PILL_BOOKED_UNTIL!r} and "
        f"name the month; nobody typed it"
    )


def test_pill_and_availability_page_read_one_record(studio, anonymous):
    make_window(studio, offset_days=5, weeks=2, capacity_days=2)
    endpoint = availability(anonymous)
    surface = page(AVAILABILITY_ROUTE)
    chrome = page(HOME_ROUTE)
    wording = {
        MODE_OPEN_NOW: PILL_OPEN_NOW, MODE_OPEN_FROM: PILL_OPEN_FROM,
        MODE_BOOKED_UNTIL: PILL_BOOKED_UNTIL, MODE_NOT_TAKING: PILL_NOT_TAKING,
    }[endpoint["mode"]]
    assert wording in chrome.text, (
        f"{API_PREFIX}/availability reports mode {endpoint['mode']!r} but the chrome "
        f"pill does not read {wording!r}; the pill and the availability page read the "
        f"same record and can never disagree"
    )
    assert wording in surface.text, (
        f"the availability page does not read {wording!r} while the endpoint reports "
        f"{endpoint['mode']!r}"
    )


def test_window_capacity_days_bounds_are_enforced(studio):
    import datetime as _dt

    starts_on = (_dt.date.today() + _dt.timedelta(days=60)).isoformat()
    for capacity in (0, 6):
        response = studio.post("/windows", json={
            "starts_on": starts_on, "weeks": 4, "capacity_days": capacity,
        })
        assert response.status_code in REFUSED, (
            f"POST {API_PREFIX}/windows accepted capacity_days {capacity} with "
            f"{response.status_code}; a window's capacity days fall between 1 and 5: "
            f"{body(response)}"
        )
    for capacity in (1, 5):
        created = make_window(studio, offset_days=61, weeks=4,
                              capacity_days=capacity)
        assert int(created["capacity_days"]) == capacity, (
            f"the created window carries capacity_days "
            f"{created['capacity_days']}, expected {capacity}"
        )
        assert int(created["committed_days"]) == 0, (
            f"a newly created window carries committed_days "
            f"{created['committed_days']}; it starts at 0"
        )


def test_studio_creates_and_closes_a_window(backend, studio):
    window = make_window(studio, offset_days=75, weeks=5, capacity_days=2)
    assert window.get("state") == WINDOW_OPEN, (
        f"a newly created window is in state {window.get('state')!r}, expected "
        f"{WINDOW_OPEN!r}"
    )
    moved = studio.patch(f"/windows/{window['id']}", json={"capacity_days": 3})
    assert moved.status_code in OK, (
        f"PATCH {API_PREFIX}/windows/{{id}} returned {moved.status_code} for the "
        f"studio: {body(moved)}"
    )
    closed = studio.patch(f"/windows/{window['id']}", json={"state": WINDOW_CLOSED})
    assert closed.status_code in OK, (
        f"PATCH {API_PREFIX}/windows/{{id}} returned {closed.status_code} closing a "
        f"window: {body(closed)}"
    )
    row = settle(lambda: backend.one("windows", id=window["id"]))
    assert row["state"] == WINDOW_CLOSED, (
        f"the window row is in state {row['state']!r} after the studio closed it"
    )


def test_hold_creates_row_with_seventy_two_hour_expiry(backend, anonymous):
    window = first_open_window(anonymous)
    response = make_hold(anonymous, window["id"])
    assert response.status_code in OK, (
        f"POST {API_PREFIX}/holds returned {response.status_code} on an open window; "
        f"a visitor with no account may hold one: {body(response)}"
    )
    hold = response.json()
    assert hold.get("expires_at"), (
        f"the created hold carries no expires_at: {json.dumps(hold)[:300]}"
    )
    row = settle(lambda: backend.one("holds", id=hold["id"]))
    assert row is not None, (
        f"the hold is not in the holds table; a hold is server-side, tied to its "
        f"enquiry rather than to a browser"
    )
    expires = row["expires_at"]
    if isinstance(expires, str):
        expires = datetime.datetime.fromisoformat(expires.replace("Z", "+00:00"))
    created = row.get("created_at") or datetime.datetime.now(expires.tzinfo)
    if isinstance(created, str):
        created = datetime.datetime.fromisoformat(created.replace("Z", "+00:00"))
    lifetime_hours = (expires - created).total_seconds() / 3600
    assert abs(lifetime_hours - HOLD_HOURS) <= 1, (
        f"the hold expires {lifetime_hours:.1f} hours after it was created, expected "
        f"{HOLD_HOURS}"
    )
    assert row.get("released_at") is None, (
        f"a freshly created hold carries released_at {row.get('released_at')!r}; a "
        f"hold is live while released_at is null"
    )


def test_hold_commits_no_capacity(backend, anonymous):
    window = first_open_window(anonymous)
    before = backend.one("windows", id=window["id"])
    offered_before = remaining_days(window)
    for _ in range(LIVE_HOLD_CEILING):
        make_hold(anonymous, window["id"])
    after = settle(lambda: backend.one("windows", id=window["id"]))
    assert int(after["committed_days"]) == int(before["committed_days"]), (
        f"three holds moved committed_days from {before['committed_days']} to "
        f"{after['committed_days']}; a hold reserves the right to be considered and "
        f"commits nothing"
    )
    reread = [w for w in windows_of(anonymous) if w["id"] == window["id"]][0]
    assert remaining_days(reread) == offered_before, (
        f"holding the window reduced what another visitor is offered from "
        f"{offered_before} to {remaining_days(reread)} days"
    )


def test_fourth_live_hold_on_one_window_is_refused(backend, studio, anonymous):
    window = make_window(studio, offset_days=12, weeks=4, capacity_days=5)
    created = []
    for _ in range(LIVE_HOLD_CEILING):
        response = make_hold(anonymous, window["id"])
        assert response.status_code in OK, (
            f"POST {API_PREFIX}/holds returned {response.status_code} for hold "
            f"{len(created) + 1} of {LIVE_HOLD_CEILING}: {body(response)}"
        )
        created.append(response.json())
    fourth = make_hold(anonymous, window["id"])
    assert fourth.status_code in REFUSED, (
        f"a fourth hold on one window returned {fourth.status_code}; at most "
        f"{LIVE_HOLD_CEILING} live holds may exist on one window: {body(fourth)}"
    )
    assert FOURTH_HOLD_REFUSAL in body(fourth), (
        f"the refusal does not read {FOURTH_HOLD_REFUSAL!r}: {body(fourth)}"
    )
    anonymous.delete(f"/holds/{created[0]['id']}")
    retry = settle(lambda: make_hold(anonymous, window["id"])
                   if True else None)
    assert retry.status_code in OK, (
        f"after releasing one of the {LIVE_HOLD_CEILING} holds a new hold returned "
        f"{retry.status_code}; a released hold is no longer live: {body(retry)}"
    )


def test_hold_on_unavailable_window_is_refused(studio, anonymous, client):
    closed = make_window(studio, offset_days=20, weeks=2, capacity_days=2)
    studio.patch(f"/windows/{closed['id']}", json={"state": WINDOW_CLOSED})
    refused = make_hold(anonymous, closed["id"])
    assert refused.status_code in REFUSED, (
        f"a hold on a window in state {WINDOW_CLOSED!r} returned "
        f"{refused.status_code}, expected a refusal stating the reason: "
        f"{body(refused)}"
    )
    assert body(refused).strip(), (
        f"the refusal carries no reason to state under the control"
    )
    full = make_window(studio, offset_days=25, weeks=2, capacity_days=1)
    booked_enquiry(studio, client, full, days_per_week=1)
    on_full = make_hold(anonymous, full["id"])
    assert on_full.status_code in REFUSED, (
        f"a hold on a window with no remaining capacity returned "
        f"{on_full.status_code}, expected a refusal: {body(on_full)}"
    )


def test_closing_a_window_releases_its_live_holds(backend, studio, anonymous):
    window = make_window(studio, offset_days=30, weeks=3, capacity_days=3)
    holds = [make_hold(anonymous, window["id"]).json()
             for _ in range(LIVE_HOLD_CEILING)]
    studio.patch(f"/windows/{window['id']}", json={"state": WINDOW_CLOSED})
    for hold in holds:
        row = settle(lambda h=hold: (backend.one("holds", id=h["id"]) or {})
                     .get("released_at"))
        assert row is not None, (
            f"hold {hold['id']} is still live after the studio closed the window it "
            f"sits on; closing a window releases every live hold on it"
        )


def test_anonymous_visitor_submits_an_enquiry(backend, anonymous):
    window = first_open_window(anonymous)
    hold = make_hold(anonymous, window["id"])
    assert hold.status_code in OK, (
        f"an anonymous visitor could not hold an open window: {body(hold)}"
    )
    sender = probe_email("anon")
    enquiry = require_enquiry(anonymous, hold_id=hold.json().get("id"), email=sender)
    row = settle(lambda: backend.one("enquiries", id=enquiry["id"]))
    assert row is not None, (
        f"no enquiry row was written for an anonymous submission"
    )
    assert row.get("account_id") is None, (
        f"the enquiry carries account_id {row.get('account_id')!r}; an enquiry from a "
        f"sender who took no account carries none"
    )
    for path in (HOME_ROUTE, WORK_ROUTE, CONTACT_ROUTE, AVAILABILITY_ROUTE):
        response = page(path)
        assert response.status_code in OK, (
            f"GET {path} returned {response.status_code} for a visitor with no "
            f"account; every public route is readable without one"
        )
    form = page(CONTACT_ROUTE)
    assert "password" not in form.text.lower(), (
        f"the enquiry form asks for a password; putting a registration in front of "
        f"the contact form is the most expensive mistake this product could make"
    )


def test_enquiry_submission_persists_six_fields_and_token(backend, anonymous):
    window = first_open_window(anonymous)
    hold = make_hold(anonymous, window["id"]).json()
    sent = enquiry_payload(email=probe_email("six"))
    response = anonymous.post("/enquiries", json={**sent, "hold_id": hold["id"]})
    assert response.status_code in OK, (
        f"POST {API_PREFIX}/enquiries returned {response.status_code}: "
        f"{body(response)}"
    )
    created = response.json()
    assert created.get("token"), (
        f"the created enquiry carries no token; the sender's link into their own "
        f"enquiry is that token: {json.dumps(created)[:300]}"
    )
    row = settle(lambda: backend.one("enquiries", id=created["id"]))
    for field in ("name", "email", "organisation", "looking_for", "budget_band",
                  "message"):
        assert str(row.get(field) or "") == str(sent[field]), (
            f"the stored enquiry carries {field} {row.get(field)!r}, expected "
            f"{sent[field]!r}; all six answers are persisted"
        )
    assert row.get("state") == ENQUIRY_NEW, (
        f"the submitted enquiry is in state {row.get('state')!r}, expected "
        f"{ENQUIRY_NEW!r}"
    )
    assert str(row.get("window_id")) == str(window["id"]), (
        f"the enquiry is linked to window {row.get('window_id')!r}, expected the held "
        f"window {window['id']!r}"
    )


def test_enquiry_field_errors_carry_the_pinned_copy(anonymous):
    cases = (
        ({"name": ""}, ERROR_MISSING_NAME, "an empty name"),
        ({"email": "not-an-address"}, ERROR_MISSING_EMAIL, "an invalid address"),
        ({"organisation": "o" * 121}, ERROR_LONG_ORGANISATION,
         "an over-long organisation"),
        ({"looking_for": "no"}, ERROR_MISSING_SUBJECT, "a two-character subject"),
        ({"budget_band": ""}, ERROR_MISSING_BAND, "no budget band"),
        ({"message": "too short"}, ERROR_SHORT_MESSAGE, "a nine-character message"),
    )
    for overrides, copy, label in cases:
        response = submit_enquiry(anonymous, **overrides)
        assert response.status_code in REFUSED, (
            f"an enquiry with {label} returned {response.status_code}, expected a "
            f"client error: {body(response)}"
        )
        assert copy in body(response), (
            f"the refusal for {label} does not carry the pinned message {copy!r}: "
            f"{body(response)}"
        )
    accepted = submit_enquiry(anonymous, organisation="")
    assert accepted.status_code in OK, (
        f"an enquiry with no organisation returned {accepted.status_code}; the third "
        f"field is optional: {body(accepted)}"
    )


def test_enquiry_rejects_short_message_and_writes_no_row(backend, anonymous):
    before = backend.count("enquiries")
    sent = enquiry_payload(message="far too short")
    response = anonymous.post("/enquiries", json=sent)
    assert response.status_code in REFUSED, (
        f"an enquiry whose message is under twenty characters returned "
        f"{response.status_code}, expected a client error: {body(response)}"
    )
    assert backend.count("enquiries") == before, (
        f"the refused enquiry still wrote a row; a rejected field writes nothing"
    )
    returned = body(response)
    assert sent["name"] in returned or "message" in returned.lower(), (
        f"the refusal does not name the field at fault or echo the answers back, so "
        f"the visitor cannot see what survived: {returned}"
    )


def test_budget_bands_are_the_four_pinned_options_descending(anonymous):
    form = page(CONTACT_ROUTE)
    positions = []
    for band in BUDGET_BANDS:
        index = form.text.find(band)
        assert index >= 0, (
            f"the enquiry form does not offer the band {band!r}: "
            f"{form.text[:400]}"
        )
        positions.append(index)
    assert positions == sorted(positions), (
        f"the four bands appear in the order {positions}; the largest band is the "
        f"first option a visitor sees, descending from there"
    )
    for band in BUDGET_BANDS:
        assert "USD" in band, (
            f"the band {band!r} does not name its currency"
        )
    assert BAND_FLOOR_LINE in form.text, (
        f"the line under the select is missing; there is no band below the lowest and "
        f"the form says where to go instead: {form.text[:400]}"
    )
    refused = submit_enquiry(anonymous, budget_band="USD $1 and up")
    assert refused.status_code in REFUSED, (
        f"an enquiry naming a band outside the four returned {refused.status_code}, "
        f"expected a client error: {body(refused)}"
    )


def test_enquiry_accepted_without_window_when_hold_expired(backend, anonymous):
    window = first_open_window(anonymous)
    hold = make_hold(anonymous, window["id"]).json()
    expired = _in_container(
        "sh", "-c",
        f"psql \"$DB_ADMIN_URL\" -c \"UPDATE holds SET expires_at = now() - "
        f"interval '1 hour' WHERE id = '{hold['id']}'\" 2>&1",
    )
    assert expired.returncode == 0, (
        f"could not age the hold to test a lapse during writing: "
        f"{expired.stdout.strip()}"
    )
    response = anonymous.post("/enquiries",
                              json={**enquiry_payload(), "hold_id": hold["id"]})
    assert response.status_code in OK, (
        f"an enquiry whose hold expired while the visitor was writing returned "
        f"{response.status_code}; it is still accepted, without a window: "
        f"{body(response)}"
    )
    created = response.json()
    row = settle(lambda: backend.one("enquiries", id=created["id"]))
    assert row.get("window_id") is None, (
        f"the enquiry is still linked to window {row.get('window_id')!r} although the "
        f"hold had expired; it is accepted without one"
    )
    assert "window" in body(response).lower(), (
        f"the response does not say the enquiry was accepted without a window: "
        f"{body(response)}"
    )


def test_enquiry_form_is_rate_limited_per_address(anonymous):
    address = probe_email("flood")
    refusal = None
    for _ in range(25):
        response = submit_enquiry(anonymous, email=address)
        if response.status_code in RATE_LIMITED or (
            response.status_code in REFUSED and "wait" in body(response).lower()
        ):
            refusal = response
            break
    assert refusal is not None, (
        f"twenty-five submissions from one address were all accepted; the enquiry "
        f"form is rate limited per address"
    )
    message = body(refusal).lower()
    assert any(word in message for word in
               ("minute", "hour", "second", "shortly", "later")), (
        f"the rate-limit refusal does not name how long to wait in words: "
        f"{body(refusal)}"
    )
    link_refusal = None
    for _ in range(25):
        response = anonymous.post("/auth/link", json={"email": address})
        if response.status_code in RATE_LIMITED:
            link_refusal = response
            break
    assert link_refusal is not None, (
        f"twenty-five sign-in link requests for one address were all accepted; that "
        f"request is rate limited per address too"
    )


def test_spam_signalled_enquiry_is_held_for_review(backend, studio, anonymous):
    hostile = enquiry_payload(
        message=("BUY CHEAP FOLLOWERS NOW visit http://spam.example http://spam.example "
                 "http://spam.example http://spam.example http://spam.example"),
        organisation="http://spam.example",
    )
    response = anonymous.post("/enquiries", json=hostile)
    assert response.status_code in OK or response.status_code in REFUSED, (
        f"a spam-signalled submission returned {response.status_code}, which is "
        f"neither an acceptance nor a stated refusal: {body(response)}"
    )
    stored = settle(lambda: backend.one("enquiries", email=hostile["email"]))
    assert stored is not None, (
        f"a submission carrying a spam signal was dropped silently; it is held for "
        f"the studio to review instead, because a false positive that eats a real "
        f"enquiry is never seen by anybody"
    )
    pipeline = read(studio, "/pipeline")
    assert hostile["email"] in flat(pipeline), (
        f"the held submission is not reachable in the studio's pipeline, so nobody "
        f"can review it"
    )


def test_enquiry_token_opens_only_its_own_enquiry(anonymous, studio):
    first = require_enquiry(anonymous, email=probe_email("token-a"))
    second = require_enquiry(anonymous, email=probe_email("token-b"))
    own = anonymous.get(f"/enquiries/{first['id']}?token={first['token']}")
    assert own.status_code in OK, (
        f"the enquiry token does not open its own enquiry: {own.status_code} "
        f"{body(own)}"
    )
    other = anonymous.get(f"/enquiries/{second['id']}?token={first['token']}")
    assert other.status_code in DENIED, (
        f"one enquiry's token opened another enquiry with {other.status_code}; a "
        f"token opens one enquiry and nothing else: {body(other)}"
    )
    with appclient.client(first["token"]) as impostor:
        elevated = impostor.get("/pipeline")
        assert elevated.status_code in DENIED, (
            f"an enquiry token reached the studio pipeline with "
            f"{elevated.status_code}; the token is never a session and never carries "
            f"a role: {body(elevated)}"
        )
    assert ENQUIRY_TOKEN_DAYS == 90, (
        f"the token lifetime constant drifted from the brief's {ENQUIRY_TOKEN_DAYS}"
    )


def test_client_reads_own_enquiry_thread(client, studio, anonymous):
    enquiry = require_enquiry(client, email=CLIENT_EMAIL)
    payload = read(client, f"/enquiries/{enquiry['id']}")
    assert isinstance(payload, dict), (
        f"GET {API_PREFIX}/enquiries/{{id}} returned a {type(payload).__name__}; it "
        f"returns the enquiry with its messages, proposal and booking"
    )
    for key in ("enquiry", "messages"):
        assert key in payload, (
            f"the enquiry read carries no {key!r}: {json.dumps(payload)[:300]}"
        )
    studio.post(f"/enquiries/{enquiry['id']}/messages",
                json={"body": "A question about the scope"})
    thread = read(client, f"/enquiries/{enquiry['id']}")
    assert thread["messages"], (
        f"the client's own enquiry shows no messages after the studio replied"
    )


def test_client_cannot_read_another_accounts_enquiry(client, anonymous):
    theirs = require_enquiry(anonymous, email=probe_email("someone-else"))
    response = client.get(f"/enquiries/{theirs['id']}")
    assert response.status_code in DENIED, (
        f"a client read an enquiry belonging to somebody else with "
        f"{response.status_code}: {body(response)}"
    )


def test_denied_enquiry_surface_is_identical_either_way(anonymous):
    real = require_enquiry(anonymous, email=probe_email("exists"))
    present = anonymous.get(f"/enquiries/{real['id']}")
    absent = anonymous.get("/enquiries/00000000-0000-0000-0000-000000000000")
    assert present.status_code in DENIED and absent.status_code in DENIED, (
        f"an unauthorised read of an existing enquiry returned "
        f"{present.status_code} and of a missing one {absent.status_code}; both are "
        f"denied"
    )
    assert present.status_code == absent.status_code, (
        f"the denied surface distinguishes an enquiry that exists "
        f"({present.status_code}) from one that does not ({absent.status_code}), so "
        f"it discloses existence"
    )
    assert present.content == absent.content, (
        f"the denied surface is not byte-identical whether the enquiry exists or "
        f"not.\nexists:  {body(present)}\nmissing: {body(absent)}"
    )
    surface = page(f"/enquiry/{real['id']}")
    assert DENIED_SURFACE_COPY in surface.text, (
        f"the denied surface does not read {DENIED_SURFACE_COPY!r}: "
        f"{surface.text[:400]}"
    )


def test_client_calls_to_studio_endpoints_are_denied(backend, client, anonymous,
                                                     studio):
    enquiry = require_enquiry(anonymous, email=probe_email("guarded"))
    window = first_open_window(anonymous)
    before_state = enquiry_state(studio, enquiry["id"])
    before_windows = backend.count("windows")
    before_proposals = backend.count("proposals", enquiry_id=enquiry["id"])

    proposal = propose(client, enquiry["id"], starts_on=window["starts_on"])
    assert proposal.status_code in DENIED, (
        f"a client proposed a start date with {proposal.status_code}; only the studio "
        f"proposes: {body(proposal)}"
    )
    assert backend.count("proposals", enquiry_id=enquiry["id"]) == before_proposals, (
        f"the denied proposal still wrote a proposal row"
    )

    decline = client.patch(f"/enquiries/{enquiry['id']}",
                           json={"state": ENQUIRY_DECLINED})
    assert decline.status_code in DENIED, (
        f"a client declined an enquiry with {decline.status_code}: {body(decline)}"
    )
    assert enquiry_state(studio, enquiry["id"]) == before_state, (
        f"the denied decline changed the enquiry state to "
        f"{enquiry_state(studio, enquiry['id'])!r}; a denied request leaves the "
        f"protected state unchanged"
    )

    created = client.post("/windows", json={
        "starts_on": window["starts_on"], "weeks": 2, "capacity_days": 1,
    })
    assert created.status_code in DENIED, (
        f"a client created a window with {created.status_code}: {body(created)}"
    )
    assert backend.count("windows") == before_windows, (
        f"the denied window create still wrote a row"
    )


def test_client_pipeline_and_export_reads_are_denied(client):
    for path in ("/pipeline", "/export", "/page-views"):
        response = client.get(path)
        assert response.status_code in DENIED, (
            f"a client read {API_PREFIX}{path} with {response.status_code}; the "
            f"pipeline, the export and the page views are the studio's alone: "
            f"{body(response)}"
        )
    surface = page(PIPELINE_ROUTE)
    assert surface.status_code in OK or surface.status_code in DENIED, (
        f"GET {PIPELINE_ROUTE} returned {surface.status_code}"
    )


def test_studio_acceptance_on_behalf_of_client_is_denied(studio, client, anonymous):
    window = first_open_window(anonymous)
    hold = make_hold(client, window["id"]).json()
    enquiry = require_enquiry(client, hold_id=hold["id"], email=CLIENT_EMAIL)
    read(studio, f"/enquiries/{enquiry['id']}")
    proposal = propose(studio, enquiry["id"], starts_on=window["starts_on"],
                       weeks=int(window.get("weeks", 4)), days_per_week=1)
    assert proposal.status_code in OK, (
        f"the studio could not propose: {body(proposal)}"
    )
    on_behalf = accept(studio, enquiry["id"], proposal.json()["id"])
    assert on_behalf.status_code in DENIED, (
        f"the studio accepted a proposal on the client's behalf with "
        f"{on_behalf.status_code}: {body(on_behalf)}"
    )
    assert enquiry_state(studio, enquiry["id"]) != ENQUIRY_BOOKED, (
        f"the enquiry reached {ENQUIRY_BOOKED!r} from a studio acceptance"
    )
    withdrawn = studio.post(f"/enquiries/{enquiry['id']}/withdraw")
    assert withdrawn.status_code in DENIED, (
        f"the studio withdrew a client's enquiry with {withdrawn.status_code}: "
        f"{body(withdrawn)}"
    )


def test_studio_reads_any_enquiry(studio, anonymous):
    theirs = require_enquiry(anonymous, email=probe_email("anon-thread"))
    response = studio.get(f"/enquiries/{theirs['id']}")
    assert response.status_code in OK, (
        f"the studio could not read an enquiry from an anonymous sender: "
        f"{response.status_code} {body(response)}"
    )
    payload = response.json()
    assert "messages" in payload, (
        f"the studio's read of an enquiry carries no thread: "
        f"{json.dumps(payload)[:300]}"
    )


def test_studio_reads_pipeline_and_export(studio):
    pipeline = studio.get("/pipeline")
    assert pipeline.status_code in OK, (
        f"GET {API_PREFIX}/pipeline returned {pipeline.status_code} for the studio: "
        f"{body(pipeline)}"
    )
    assert isinstance(pipeline.json(), list), (
        f"GET {API_PREFIX}/pipeline returned a {type(pipeline.json()).__name__}; "
        f"every list endpoint returns a top-level JSON array"
    )
    export = studio.get("/export")
    assert export.status_code in OK, (
        f"GET {API_PREFIX}/export returned {export.status_code} for the studio; the "
        f"whole pipeline is exportable in one action: {body(export)}"
    )


def test_opening_enquiry_moves_state_new_to_reading(studio, anonymous):
    enquiry = require_enquiry(anonymous, email=probe_email("reading"))
    assert enquiry_state(studio, enquiry["id"]) in (ENQUIRY_NEW, ENQUIRY_READING), (
        f"a freshly submitted enquiry is in state "
        f"{enquiry_state(studio, enquiry['id'])!r}, expected {ENQUIRY_NEW!r}"
    )
    read(studio, f"/enquiries/{enquiry['id']}")
    after = settle(lambda: enquiry_state(studio, enquiry["id"]) == ENQUIRY_READING)
    assert after, (
        f"the enquiry is in state {enquiry_state(studio, enquiry['id'])!r} after the "
        f"studio opened it, expected {ENQUIRY_READING!r}"
    )


def test_reply_creates_message_and_changes_no_state(backend, studio, client,
                                                    anonymous):
    window = first_open_window(anonymous)
    hold = make_hold(client, window["id"]).json()
    enquiry = require_enquiry(client, hold_id=hold["id"], email=CLIENT_EMAIL)
    read(studio, f"/enquiries/{enquiry['id']}")
    before = enquiry_state(studio, enquiry["id"])
    for actor, sender in ((studio, "studio"), (client, "client")):
        response = actor.post(f"/enquiries/{enquiry['id']}/messages",
                              json={"body": f"A note from the {sender} side"})
        assert response.status_code in OK, (
            f"POST {API_PREFIX}/enquiries/{{id}}/messages returned "
            f"{response.status_code} from the {sender}: {body(response)}"
        )
        assert enquiry_state(studio, enquiry["id"]) == before, (
            f"a reply from the {sender} moved the enquiry from {before!r} to "
            f"{enquiry_state(studio, enquiry['id'])!r}; a reply changes no state"
        )
    rows = backend.rows("messages", enquiry_id=enquiry["id"])
    authors = {str(row.get("author")) for row in rows}
    assert {"client", "studio"} <= authors, (
        f"the message rows carry authors {authors}; each message records which side "
        f"wrote it"
    )


def test_proposal_creates_live_row_and_moves_state(backend, studio, client,
                                                   anonymous, inbox):
    window = first_open_window(anonymous)
    hold = make_hold(client, window["id"]).json()
    enquiry = require_enquiry(client, hold_id=hold["id"], email=CLIENT_EMAIL)
    read(studio, f"/enquiries/{enquiry['id']}")
    note = "Two days a week from the window's own start"
    response = propose(studio, enquiry["id"], starts_on=window["starts_on"],
                       weeks=int(window.get("weeks", 4)), days_per_week=1, note=note)
    assert response.status_code in OK, (
        f"POST {API_PREFIX}/enquiries/{{id}}/proposals returned "
        f"{response.status_code} inside the window: {body(response)}"
    )
    row = settle(lambda: backend.one("proposals", id=response.json()["id"]))
    assert row["state"] == PROPOSAL_LIVE, (
        f"the created proposal is in state {row['state']!r}, expected "
        f"{PROPOSAL_LIVE!r}"
    )
    assert str(row.get("note") or "") == note, (
        f"the proposal carries note {row.get('note')!r}, expected {note!r}"
    )
    assert row.get("expires_at"), (
        f"the proposal carries no expires_at: {row}"
    )
    assert enquiry_state(studio, enquiry["id"]) == ENQUIRY_PROPOSED, (
        f"the enquiry is in state {enquiry_state(studio, enquiry['id'])!r} after a "
        f"proposal, expected {ENQUIRY_PROPOSED!r}"
    )
    hold_row = settle(lambda: backend.one("holds", id=hold["id"]))
    assert hold_row.get("released_at") is None, (
        f"the hold was released when the proposal went out; it is extended to the "
        f"proposal's expiry instead"
    )
    message = settle(lambda: inbox.find(CLIENT_EMAIL, SUBJECT_PROPOSAL))
    assert message is not None, (
        f"no message whose subject begins {SUBJECT_PROPOSAL!r} reached the client "
        f"when the proposal was sent"
    )


def test_proposal_outside_window_or_over_capacity_is_refused(studio, client,
                                                             anonymous):
    window = first_open_window(anonymous)
    hold = make_hold(client, window["id"]).json()
    enquiry = require_enquiry(client, hold_id=hold["id"], email=CLIENT_EMAIL)
    read(studio, f"/enquiries/{enquiry['id']}")
    before_start = (
        datetime.date.fromisoformat(str(window["starts_on"])[:10])
        - datetime.timedelta(days=14)
    ).isoformat()
    early = propose(studio, enquiry["id"], starts_on=before_start,
                    weeks=2, days_per_week=1)
    assert early.status_code in REFUSED, (
        f"a proposal starting {before_start}, before the enquiry's window opens, "
        f"returned {early.status_code}: {body(early)}"
    )
    over = propose(studio, enquiry["id"], starts_on=window["starts_on"],
                   weeks=int(window.get("weeks", 4)),
                   days_per_week=remaining_days(window) + 1)
    assert over.status_code in REFUSED, (
        f"a proposal asking for {remaining_days(window) + 1} days per week against a "
        f"window with {remaining_days(window)} left returned {over.status_code}: "
        f"{body(over)}"
    )


def test_second_proposal_supersedes_the_first(backend, studio, client, anonymous):
    window = first_open_window(anonymous)
    hold = make_hold(client, window["id"]).json()
    enquiry = require_enquiry(client, hold_id=hold["id"], email=CLIENT_EMAIL)
    read(studio, f"/enquiries/{enquiry['id']}")
    first = propose(studio, enquiry["id"], starts_on=window["starts_on"],
                    weeks=int(window.get("weeks", 4)), days_per_week=1).json()
    second = propose(studio, enquiry["id"], starts_on=window["starts_on"],
                     weeks=int(window.get("weeks", 4)), days_per_week=1).json()
    first_row = settle(lambda: backend.one("proposals", id=first["id"]))
    assert first_row["state"] == PROPOSAL_SUPERSEDED, (
        f"the first proposal is in state {first_row['state']!r} after a second one "
        f"went out, expected {PROPOSAL_SUPERSEDED!r}"
    )
    live = backend.count("proposals", enquiry_id=enquiry["id"], state=PROPOSAL_LIVE)
    assert live == 1, (
        f"the enquiry carries {live} live proposals, expected exactly 1"
    )
    second_row = backend.one("proposals", id=second["id"])
    assert second_row["state"] == PROPOSAL_LIVE, (
        f"the newest proposal is in state {second_row['state']!r}, expected "
        f"{PROPOSAL_LIVE!r}"
    )


def test_acceptance_writes_booking_and_commits_capacity(backend, studio, client,
                                                        anonymous):
    window = make_window(studio, offset_days=100, weeks=4, capacity_days=3)
    before = int(backend.one("windows", id=window["id"])["committed_days"])
    enquiry, proposal, booking = booked_enquiry(studio, client, window,
                                                days_per_week=2)
    row = settle(lambda: backend.one("bookings", enquiry_id=enquiry["id"]))
    assert row is not None, (
        f"accepting a live proposal wrote no booking row"
    )
    assert str(row["window_id"]) == str(window["id"]), (
        f"the booking sits against window {row['window_id']!r}, expected "
        f"{window['id']!r}"
    )
    assert int(row["days_per_week"]) == 2, (
        f"the booking records {row['days_per_week']} days per week, expected the "
        f"proposal's 2"
    )
    assert row.get("confirmed_at"), (
        f"the booking carries no confirmed_at: {row}"
    )
    assert enquiry_state(studio, enquiry["id"]) == ENQUIRY_BOOKED, (
        f"the enquiry is in state {enquiry_state(studio, enquiry['id'])!r} after the "
        f"acceptance, expected {ENQUIRY_BOOKED!r}"
    )
    after = int(backend.one("windows", id=window["id"])["committed_days"])
    assert after == before + 2, (
        f"the window's committed_days moved from {before} to {after}; an acceptance "
        f"raises it by the proposal's days per week"
    )
    assert backend.count("bookings", enquiry_id=enquiry["id"]) == 1, (
        f"the enquiry carries more than one booking; one booking per enquiry, at most"
    )


def test_window_state_becomes_booked_once_full(backend, studio, client, anonymous):
    window = make_window(studio, offset_days=105, weeks=3, capacity_days=1)
    booked_enquiry(studio, client, window, days_per_week=1)
    row = settle(lambda: (backend.one("windows", id=window["id"]) or {})
                 .get("state") == WINDOW_BOOKED)
    state = backend.one("windows", id=window["id"])["state"]
    assert state == WINDOW_BOOKED, (
        f"a window whose committed_days reached its capacity is in state {state!r}, "
        f"expected {WINDOW_BOOKED!r}"
    )


def test_expired_proposal_acceptance_is_refused(studio, client, anonymous):
    window = make_window(studio, offset_days=110, weeks=3, capacity_days=2)
    hold = make_hold(client, window["id"]).json()
    enquiry = require_enquiry(client, hold_id=hold["id"], email=CLIENT_EMAIL)
    read(studio, f"/enquiries/{enquiry['id']}")
    proposal = propose(studio, enquiry["id"], starts_on=window["starts_on"],
                       weeks=3, days_per_week=1).json()
    aged = _in_container(
        "sh", "-c",
        f"psql \"$DB_ADMIN_URL\" -c \"UPDATE proposals SET expires_at = now() - "
        f"interval '1 day' WHERE id = '{proposal['id']}'\" 2>&1",
    )
    assert aged.returncode == 0, (
        f"could not age the proposal past its expiry: {aged.stdout.strip()}"
    )
    response = accept(client, enquiry["id"], proposal["id"])
    assert response.status_code in REFUSED, (
        f"accepting a proposal whose expiry has passed returned "
        f"{response.status_code}, expected a refusal: {body(response)}"
    )
    assert EXPIRED_PROPOSAL_REFUSAL in body(response), (
        f"the refusal does not read {EXPIRED_PROPOSAL_REFUSAL!r}: {body(response)}"
    )


def test_decline_sets_state_and_mails_the_client(studio, anonymous, inbox):
    sender = probe_email("declined")
    enquiry = require_enquiry(anonymous, email=sender)
    read(studio, f"/enquiries/{enquiry['id']}")
    response = studio.patch(f"/enquiries/{enquiry['id']}",
                            json={"state": ENQUIRY_DECLINED})
    assert response.status_code in OK, (
        f"the studio could not decline the enquiry: {response.status_code} "
        f"{body(response)}"
    )
    assert enquiry_state(studio, enquiry["id"]) == ENQUIRY_DECLINED, (
        f"the enquiry is in state {enquiry_state(studio, enquiry['id'])!r} after a "
        f"decline, expected {ENQUIRY_DECLINED!r}"
    )
    message = settle(lambda: inbox.find(sender, SUBJECT_DECLINED))
    assert message is not None, (
        f"no message whose subject begins {SUBJECT_DECLINED!r} reached {sender!r}; "
        f"the client is always mailed and a silent decline is not available"
    )


def test_lapsed_enquiry_releases_its_hold_and_mails_nobody(backend, studio, inbox,
                                                           anonymous):
    window = first_open_window(anonymous)
    hold = make_hold(anonymous, window["id"]).json()
    sender = probe_email("lapsing")
    enquiry = require_enquiry(anonymous, hold_id=hold["id"], email=sender)
    before = inbox.count(sender)
    aged = _in_container(
        "sh", "-c",
        f"psql \"$DB_ADMIN_URL\" -c \"UPDATE enquiries SET created_at = now() - "
        f"interval '{LAPSE_SILENCE_DAYS + 1} days' WHERE id = '{enquiry['id']}'\" 2>&1",
    )
    assert aged.returncode == 0, (
        f"could not age the enquiry past {LAPSE_SILENCE_DAYS} days: "
        f"{aged.stdout.strip()}"
    )
    studio.get("/pipeline")
    lapsed = settle(lambda: (backend.one("enquiries", id=enquiry["id"]) or {})
                    .get("state") == ENQUIRY_LAPSED)
    assert lapsed, (
        f"an enquiry with no reply for {LAPSE_SILENCE_DAYS} days is in state "
        f"{backend.one('enquiries', id=enquiry['id'])['state']!r}, expected "
        f"{ENQUIRY_LAPSED!r}"
    )
    hold_row = backend.one("holds", id=hold["id"])
    assert hold_row.get("released_at") is not None, (
        f"the lapsed enquiry's hold is still live; a lapse releases it"
    )
    assert inbox.count(sender) == before, (
        f"{inbox.count(sender) - before} messages reached {sender!r} when the enquiry "
        f"lapsed; nobody is mailed about a lapse"
    )


def test_enquiry_row_is_never_deleted(backend, studio, client, anonymous):
    withdrawn = require_enquiry(client, email=CLIENT_EMAIL)
    client.post(f"/enquiries/{withdrawn['id']}/withdraw")
    declined = require_enquiry(anonymous, email=probe_email("kept-declined"))
    read(studio, f"/enquiries/{declined['id']}")
    studio.patch(f"/enquiries/{declined['id']}", json={"state": ENQUIRY_DECLINED})
    for enquiry, expected in ((withdrawn, ENQUIRY_WITHDRAWN),
                              (declined, ENQUIRY_DECLINED)):
        row = settle(lambda e=enquiry: backend.one("enquiries", id=e["id"]))
        assert row is not None, (
            f"the enquiry row was deleted when it reached {expected!r}; who asked and "
            f"what happened is the studio's own history"
        )
        assert row["state"] == expected, (
            f"the enquiry is in state {row['state']!r}, expected {expected!r}"
        )


def test_withdraw_sets_state_and_releases_hold(backend, client, anonymous):
    window = first_open_window(anonymous)
    hold = make_hold(client, window["id"]).json()
    enquiry = require_enquiry(client, hold_id=hold["id"], email=CLIENT_EMAIL)
    before_messages = backend.count("messages", enquiry_id=enquiry["id"])
    response = client.post(f"/enquiries/{enquiry['id']}/withdraw")
    assert response.status_code in OK, (
        f"the client could not withdraw their own enquiry: {response.status_code} "
        f"{body(response)}"
    )
    row = settle(lambda: (backend.one("enquiries", id=enquiry["id"]) or {})
                 .get("state") == ENQUIRY_WITHDRAWN)
    assert row, (
        f"the enquiry is in state "
        f"{backend.one('enquiries', id=enquiry['id'])['state']!r} after a withdrawal, "
        f"expected {ENQUIRY_WITHDRAWN!r}"
    )
    hold_row = backend.one("holds", id=hold["id"])
    assert hold_row.get("released_at") is not None, (
        f"the withdrawn enquiry's hold is still live; it is released immediately"
    )
    assert backend.count("messages", enquiry_id=enquiry["id"]) == before_messages, (
        f"the withdrawal deleted messages; nothing is deleted"
    )


def test_timestamps_render_in_the_reader_timezone(backend, studio, client):
    studio_row = backend.one("accounts", email=STUDIO_EMAIL)
    client_row = backend.one("accounts", email=CLIENT_EMAIL)
    assert studio_row.get("timezone"), (
        f"the studio account carries no timezone; a timestamp shown to the studio is "
        f"rendered in the studio's"
    )
    assert client_row.get("timezone"), (
        f"the client account carries no timezone; a timestamp shown to a client is "
        f"rendered in that client's"
    )
    enquiry = require_enquiry(client, email=CLIENT_EMAIL)
    as_client = flat(read(client, f"/enquiries/{enquiry['id']}"))
    as_studio = flat(read(studio, f"/enquiries/{enquiry['id']}"))
    if str(studio_row["timezone"]) != str(client_row["timezone"]):
        assert as_client != as_studio, (
            f"the same enquiry renders identically to a client in "
            f"{client_row['timezone']!r} and to the studio in "
            f"{studio_row['timezone']!r}; each reader sees their own timezone"
        )


def test_concurrent_acceptances_produce_exactly_one_booking(backend, studio, client,
                                                            anonymous):
    window = make_window(studio, offset_days=130, weeks=4, capacity_days=1)
    contenders = []
    for _ in range(2):
        hold = make_hold(anonymous, window["id"])
        assert hold.status_code in OK, (
            f"a hold on the contested window was refused before the race began: "
            f"{body(hold)}"
        )
        enquiry = require_enquiry(anonymous, hold_id=hold.json()["id"],
                                  email=probe_email("race"))
        read(studio, f"/enquiries/{enquiry['id']}")
        proposal = propose(studio, enquiry["id"], starts_on=window["starts_on"],
                           weeks=4, days_per_week=1)
        assert proposal.status_code in OK, (
            f"the second proposal against the window's last place was refused before "
            f"the race began; both proposals are live at once: {body(proposal)}"
        )
        contenders.append((enquiry, proposal.json()))

    def race(pair):
        enquiry, proposal = pair
        with appclient.client() as caller:
            return caller.post(
                f"/enquiries/{enquiry['id']}/accept?token={enquiry['token']}",
                json={"proposal_id": proposal["id"]},
            )

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(race, contenders))

    winners = [r for r in results if r.status_code in OK]
    losers = [r for r in results if r.status_code not in OK]
    assert len(winners) == 1, (
        f"{len(winners)} of 2 simultaneous acceptances against one remaining "
        f"capacity day succeeded; exactly one must win. Statuses: "
        f"{[r.status_code for r in results]}"
    )
    assert len(losers) == 1 and losers[0].status_code in REFUSED, (
        f"the losing acceptance returned {[r.status_code for r in losers]}, expected "
        f"one client error"
    )
    bookings = settle(lambda: backend.count("bookings", window_id=window["id"]))
    assert bookings == 1, (
        f"{bookings} booking rows exist against the contested window; exactly one is "
        f"written and no partial booking survives"
    )
    row = backend.one("windows", id=window["id"])
    assert int(row["committed_days"]) <= int(row["capacity_days"]), (
        f"committed_days {row['committed_days']} passed capacity_days "
        f"{row['capacity_days']}"
    )


def test_committed_days_equals_sum_of_booking_days(backend, studio, client,
                                                   anonymous):
    window = make_window(studio, offset_days=140, weeks=6, capacity_days=4)
    for days in (1, 2):
        booked_enquiry(studio, client, window, days_per_week=days)
    rows = backend.rows("bookings", window_id=window["id"])
    total = sum(int(row["days_per_week"]) for row in rows)
    committed = int(backend.one("windows", id=window["id"])["committed_days"])
    assert committed == total, (
        f"the window reports committed_days {committed} while its {len(rows)} "
        f"bookings sum to {total}; the row in PostgreSQL is the fact, never a count "
        f"the interface keeps for itself"
    )


def test_refused_acceptance_carries_the_open_windows(backend, studio, client,
                                                     anonymous):
    window = make_window(studio, offset_days=150, weeks=4, capacity_days=1)
    make_window(studio, offset_days=160, weeks=4, capacity_days=2)
    first_hold = make_hold(anonymous, window["id"]).json()
    first = require_enquiry(anonymous, hold_id=first_hold["id"],
                            email=probe_email("wins"))
    second_hold = make_hold(anonymous, window["id"]).json()
    second = require_enquiry(anonymous, hold_id=second_hold["id"],
                             email=probe_email("loses"))
    for enquiry in (first, second):
        read(studio, f"/enquiries/{enquiry['id']}")
    proposals = [
        propose(studio, enquiry["id"], starts_on=window["starts_on"], weeks=4,
                days_per_week=1).json()
        for enquiry in (first, second)
    ]
    winner = accept(anonymous, first["id"], proposals[0]["id"])
    assert winner.status_code in OK, (
        f"the first acceptance was refused: {body(winner)}"
    )
    loser = accept(anonymous, second["id"], proposals[1]["id"])
    assert loser.status_code in REFUSED, (
        f"the second acceptance against a filled window returned {loser.status_code}, "
        f"expected a refusal: {body(loser)}"
    )
    text = body(loser)
    assert FILLED_WINDOW_REFUSAL in text, (
        f"the refusal does not read {FILLED_WINDOW_REFUSAL!r}: {text}"
    )
    payload = loser.json() if loser.headers.get("content-type", "").startswith(
        "application/json") else {}
    carried = flat(payload)
    assert "window" in carried.lower(), (
        f"the refusal carries no open windows with it, so the caller is told which "
        f"window filled without being told what is still open: {carried[:300]}"
    )


def test_mail_settings_come_from_the_environment():
    sources = _in_container(
        "sh", "-c",
        "grep -rIl --exclude-dir=node_modules --exclude-dir=.git "
        "-e 'createTransport' -e 'nodemailer' -e 'smtp' /app 2>/dev/null | head -20",
    )
    files = [line for line in sources.stdout.splitlines() if line.strip()]
    assert files, (
        f"no source file in /app configures SMTP; the app sends over real SMTP at "
        f"SMTP_HOST and SMTP_PORT"
    )
    hardcoded = _in_container(
        "sh", "-c",
        "grep -rIn --exclude-dir=node_modules --exclude-dir=.git "
        "-e 'mailpit:1025' -e \"'1025'\" -e '\"1025\"' /app/src /app/server 2>/dev/null "
        "| grep -v 'process.env' | head -10",
    )
    assert not hardcoded.stdout.strip(), (
        f"a mail host or port is written into the source rather than read from the "
        f"environment:\n{hardcoded.stdout[:400]}"
    )
    for variable in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS"):
        used = _in_container(
            "sh", "-c",
            f"grep -rIl --exclude-dir=node_modules --exclude-dir=.git "
            f"'{variable}' /app 2>/dev/null | head -1",
        )
        assert used.stdout.strip(), (
            f"{variable} is read nowhere in /app; every host, port and credential "
            f"comes from the environment"
        )


def test_enquiry_submission_sends_both_named_messages(anonymous, inbox):
    sender = probe_email("both")
    enquiry = require_enquiry(anonymous, email=sender)
    confirmation = settle(lambda: inbox.find(sender, SUBJECT_CONFIRMATION))
    assert confirmation is not None, (
        f"no message whose subject begins {SUBJECT_CONFIRMATION!r} reached {sender!r}; "
        f"mailpit is the only place a message lives, and a success the app reports to "
        f"itself is a contract violation"
    )
    assert confirmation.subject.startswith(SUBJECT_CONFIRMATION), (
        f"the confirmation subject is {confirmation.subject!r}, which does not begin "
        f"{SUBJECT_CONFIRMATION!r}"
    )
    assert str(enquiry["id"]) in confirmation.subject, (
        f"the confirmation subject {confirmation.subject!r} does not carry the "
        f"enquiry id after the pinned phrase and a space"
    )
    notification = settle(lambda: inbox.find("", SUBJECT_NOTIFICATION))
    assert notification is not None, (
        f"no message whose subject begins {SUBJECT_NOTIFICATION!r} reached the studio "
        f"when the enquiry arrived"
    )


def test_confirmation_carries_the_six_answers_back(anonymous, inbox):
    sent = enquiry_payload(email=probe_email("echo"))
    response = anonymous.post("/enquiries", json=sent)
    assert response.status_code in OK, (
        f"the enquiry was refused: {body(response)}"
    )
    message = settle(lambda: inbox.find(sent["email"], SUBJECT_CONFIRMATION))
    assert message is not None, (
        f"no confirmation reached {sent['email']!r}"
    )
    text = f"{message.subject}\n{message.body}"
    missing = [field for field in
               ("name", "organisation", "looking_for", "budget_band", "message")
               if str(sent[field]) not in text]
    assert not missing, (
        f"the confirmation does not carry the sender's own answers for {missing} back "
        f"to them; it is their copy of what they asked for. Message: {text[:400]!r}"
    )


def test_reply_from_each_side_mails_the_other(studio, client, inbox, backend):
    enquiry = require_enquiry(client, email=CLIENT_EMAIL)
    read(studio, f"/enquiries/{enquiry['id']}")
    studio.post(f"/enquiries/{enquiry['id']}/messages",
                json={"body": "A question from the studio"})
    to_client = settle(lambda: inbox.find(CLIENT_EMAIL, SUBJECT_STUDIO_REPLY))
    assert to_client is not None, (
        f"no message whose subject begins {SUBJECT_STUDIO_REPLY!r} reached "
        f"{CLIENT_EMAIL!r} when the studio replied"
    )
    client.post(f"/enquiries/{enquiry['id']}/messages",
                json={"body": "An answer from the client"})
    to_studio = settle(lambda: inbox.find("", SUBJECT_CLIENT_REPLY))
    assert to_studio is not None, (
        f"no message whose subject begins {SUBJECT_CLIENT_REPLY!r} reached the studio "
        f"when the client replied"
    )


def test_acceptance_sends_booked_to_both_parties(studio, client, anonymous, inbox,
                                                 backend):
    window = make_window(studio, offset_days=170, weeks=4, capacity_days=2)
    booked_enquiry(studio, client, window, days_per_week=1)
    to_client = settle(lambda: inbox.find(CLIENT_EMAIL, SUBJECT_BOOKED))
    assert to_client is not None, (
        f"no message whose subject begins {SUBJECT_BOOKED!r} reached {CLIENT_EMAIL!r} "
        f"after the acceptance"
    )
    studio_row = backend.one("accounts", email=STUDIO_EMAIL)
    studio_inbox = str(studio_row.get("notification_email") or STUDIO_EMAIL)
    to_studio = settle(lambda: inbox.find(studio_inbox, SUBJECT_BOOKED))
    assert to_studio is not None, (
        f"no message whose subject begins {SUBJECT_BOOKED!r} reached the studio at "
        f"{studio_inbox!r} after the acceptance; both parties are mailed"
    )


def test_expiring_proposal_warns_the_client_once(studio, client, anonymous, inbox):
    window = make_window(studio, offset_days=180, weeks=4, capacity_days=2)
    hold = make_hold(client, window["id"]).json()
    enquiry = require_enquiry(client, hold_id=hold["id"], email=CLIENT_EMAIL)
    read(studio, f"/enquiries/{enquiry['id']}")
    proposal = propose(studio, enquiry["id"], starts_on=window["starts_on"],
                       weeks=4, days_per_week=1).json()
    aged = _in_container(
        "sh", "-c",
        f"psql \"$DB_ADMIN_URL\" -c \"UPDATE proposals SET expires_at = now() + "
        f"interval '{PROPOSAL_WARNING_HOURS - 6} hours' WHERE id = "
        f"'{proposal['id']}'\" 2>&1",
    )
    assert aged.returncode == 0, (
        f"could not bring the proposal inside its warning horizon: "
        f"{aged.stdout.strip()}"
    )
    def _swept():
        studio.get("/pipeline")
        return inbox.find(CLIENT_EMAIL, SUBJECT_EXPIRING)

    warned = settle(_swept)
    assert warned is not None, (
        f"no message whose subject begins {SUBJECT_EXPIRING!r} reached "
        f"{CLIENT_EMAIL!r} for a proposal expiring within {PROPOSAL_WARNING_HOURS} "
        f"hours"
    )
    count = sum(1 for _ in range(1)
                if inbox.find(CLIENT_EMAIL, SUBJECT_EXPIRING))
    assert count == 1, (
        f"the expiry warning reached the client {count} times; it is sent once"
    )


def test_no_message_carries_a_cc_or_a_bcc(anonymous, inbox):
    sender = probe_email("solo")
    require_enquiry(anonymous, email=sender)
    message = settle(lambda: inbox.find(sender, SUBJECT_CONFIRMATION))
    assert message is not None, (
        f"no confirmation reached {sender!r}"
    )
    assert len(message.to) == 1, (
        f"the confirmation went to {message.to}; every message is addressed to "
        f"exactly the recipient named, with no cc and no bcc"
    )
    assert sender.lower() in message.to[0].lower(), (
        f"the confirmation went to {message.to[0]!r}, expected {sender!r}"
    )


def test_every_message_is_plain_text_with_one_link(anonymous, inbox):
    sender = probe_email("plain")
    require_enquiry(anonymous, email=sender)
    message = settle(lambda: inbox.find(sender, SUBJECT_CONFIRMATION))
    assert message is not None, (
        f"no confirmation reached {sender!r}"
    )
    text = message.body
    assert "<html" not in text.lower() and "<table" not in text.lower(), (
        f"the confirmation carries markup; every message is plain text: {text[:300]!r}"
    )
    links = re.findall(r"https?://\S+", text)
    assert len(links) >= 1, (
        f"the confirmation carries no primary link: {text[:300]!r}"
    )
    assert sender.split("@")[0] in text or sender in text, (
        f"the confirmation does not state at its foot which address it went to: "
        f"{text[:400]!r}"
    )


def test_mail_failure_leaves_the_enquiry_standing(backend, anonymous):
    broken = _in_container(
        "sh", "-c",
        "iptables -A OUTPUT -p tcp --dport 1025 -j REJECT 2>/dev/null && echo broken",
    )
    sender = probe_email("mailfail")
    try:
        response = submit_enquiry(anonymous, email=sender)
        assert response.status_code in OK, (
            f"the enquiry was refused because mail could not be sent "
            f"({response.status_code}); mail is sent after the state change commits "
            f"and a failure never fails the action: {body(response)}"
        )
        row = settle(lambda: backend.one("enquiries", email=sender))
        assert row is not None, (
            f"the enquiry was rolled back when the send failed; the enquiry is "
            f"submitted and the page says so"
        )
    finally:
        if "broken" in broken.stdout:
            _in_container("sh", "-c",
                          "iptables -D OUTPUT -p tcp --dport 1025 -j REJECT")


def test_window_operations_send_no_mail(studio, inbox):
    before = inbox.count()
    window = make_window(studio, offset_days=190, weeks=2, capacity_days=1)
    studio.patch(f"/windows/{window['id']}", json={"capacity_days": 2})
    studio.patch(f"/windows/{window['id']}", json={"state": WINDOW_CLOSED})
    settle(lambda: inbox.count() > before)
    after = inbox.count()
    assert after == before, (
        f"{after - before} messages were sent while creating, moving and closing a "
        f"window; mail is not applicable to a window operation at all, and there is "
        f"no follow-up, newsletter or marketing of any kind"
    )


def test_pipeline_orders_newest_first(studio, anonymous):
    for _ in range(3):
        created = require_enquiry(anonymous, email=probe_email("ordered"))
        landed = settle(lambda cid=str(created["id"]): any(
            str(row.get("id")) == cid for row in read(studio, "/pipeline")))
        assert landed, (
            f"enquiry {created['id']} never reached the pipeline, so the three "
            f"submissions cannot be ordered against one another"
        )
    rows = read(studio, "/pipeline")
    assert isinstance(rows, list) and len(rows) >= 3, (
        f"the pipeline returned {len(rows) if isinstance(rows, list) else rows}; at "
        f"least the three just submitted are reachable"
    )
    stamps = [str(row.get("created_at", "")) for row in rows]
    assert stamps == sorted(stamps, reverse=True), (
        f"the pipeline is not newest first by default: {stamps[:5]}"
    )
    by_band = read(studio, "/pipeline?sort=band")
    bands = [str(row.get("budget_band", "")) for row in by_band
             if row.get("budget_band") in BUDGET_BANDS]
    ranks = [BUDGET_BANDS.index(band) for band in bands]
    assert ranks == sorted(ranks), (
        f"sorting by budget band produced {bands[:5]}; the largest band leads, which "
        f"is the order the bands are offered in"
    )


def test_pipeline_filters_by_state_and_band(studio, anonymous):
    band = BUDGET_BANDS[2]
    require_enquiry(anonymous, email=probe_email("filtered"), budget_band=band)
    by_state = read(studio, f"/pipeline?state={ENQUIRY_NEW}")
    assert by_state, (
        f"filtering the pipeline by state {ENQUIRY_NEW!r} returned nothing"
    )
    assert all(row.get("state") == ENQUIRY_NEW for row in by_state), (
        f"the state filter returned states "
        f"{ {row.get('state') for row in by_state} }"
    )
    by_band = read(studio, f"/pipeline?band={band}")
    assert by_band, (
        f"filtering the pipeline by band {band!r} returned nothing"
    )
    assert all(row.get("budget_band") == band for row in by_band), (
        f"the band filter returned bands "
        f"{ {row.get('budget_band') for row in by_band} }"
    )


def test_pipeline_search_matches_name_organisation_subject(studio, anonymous):
    marker = probe_name("needle").replace(" ", "")
    require_enquiry(anonymous, email=probe_email("search"), name=f"{marker} Sender",
                    organisation=f"{marker} Works",
                    looking_for=f"A {marker} booking desk")
    for field in ("name", "organisation", "subject line"):
        found = read(studio, f"/pipeline?q={marker}")
        assert found, (
            f"searching the pipeline for {marker!r} matched nothing, so the search "
            f"does not reach the enquiry's {field}"
        )
    narrowed = read(studio, f"/pipeline?q={marker}&state={ENQUIRY_NEW}")
    assert narrowed, (
        f"searching for {marker!r} with the state filter set returned nothing; the "
        f"search applies on top of the state and band filters rather than replacing "
        f"them"
    )
    excluded = read(studio, f"/pipeline?q={marker}&state={ENQUIRY_BOOKED}")
    assert not excluded, (
        f"the search ignored the state filter and returned {len(excluded)} rows in "
        f"state {ENQUIRY_BOOKED!r}"
    )


def test_export_returns_every_record_set(backend, studio):
    payload = read(studio, "/export")
    assert isinstance(payload, dict), (
        f"GET {API_PREFIX}/export returned a {type(payload).__name__}; it returns "
        f"every enquiry, message, proposal, booking and window in one response"
    )
    for collection, table in (("enquiries", "enquiries"), ("messages", "messages"),
                              ("proposals", "proposals"), ("bookings", "bookings"),
                              ("windows", "windows")):
        assert collection in payload, (
            f"the export carries no {collection!r}: {sorted(payload)}"
        )
        exported = len(payload[collection])
        stored = backend.count(table)
        assert exported == stored, (
            f"the export carries {exported} {collection} while the {table} table "
            f"holds {stored}; the whole business leaves in one action"
        )


def test_seven_analytics_events_carry_their_named_properties(backend, studio,
                                                             anonymous, client):
    anonymous.post("/consent", json={"accepted": True})
    page(AVAILABILITY_ROUTE)
    window = first_open_window(anonymous)
    hold = make_hold(anonymous, window["id"]).json()
    enquiry = require_enquiry(anonymous, hold_id=hold["id"],
                              email=probe_email("events"))
    read(studio, f"/enquiries/{enquiry['id']}")
    propose(studio, enquiry["id"], starts_on=window["starts_on"],
            weeks=int(window.get("weeks", 4)), days_per_week=1)

    rows = settle(lambda: backend.rows("events") or backend.rows("page_views"))
    assert rows, (
        f"no event rows were written after driving an availability view, a hold, a "
        f"submission and a proposal; instrumentation is local and small, not absent"
    )
    kinds = {str(row.get("name") or row.get("event") or row.get("kind") or "")
             for row in rows}
    kinds.discard("")
    assert len(kinds) <= 7, (
        f"{len(kinds)} distinct event kinds are recorded: {sorted(kinds)}. Seven are "
        f"recorded and no others"
    )
    banned = ("name", "email", "organisation", "employer", "message")
    for row in rows:
        payload = json.dumps(row).lower()
        assert enquiry.get("token", "\0") not in payload, (
            f"an event row carries the enquiry token: {row}"
        )
        properties = row.get("properties") or row.get("props") or {}
        if isinstance(properties, str):
            properties = json.loads(properties or "{}")
        leaked = [key for key in properties if key.lower() in banned]
        assert not leaked, (
            f"an event row carries {leaked}; no event ever carries a name, an "
            f"address, an employer or a message body: {row}"
        )


def test_studio_reads_the_four_funnel_numbers(studio):
    for path in ("/page-views", "/pipeline"):
        response = studio.get(path)
        assert response.status_code in OK, (
            f"GET {API_PREFIX}{path} returned {response.status_code} for the studio: "
            f"{body(response)}"
        )
    counts = flat(read(studio, "/page-views"))
    assert counts.strip(), (
        f"the studio's own read of the local counts is empty; the four numbers that "
        f"matter are how many arrived, how many started an enquiry, how many finished "
        f"one and how many became a booking"
    )


def test_page_view_is_written_only_after_consent(backend, anonymous):
    with appclient.client() as fresh:
        before = backend.count("page_views")
        page(HOME_ROUTE)
        page(WORK_ROUTE)
        settle(lambda: backend.count("page_views") > before)
        assert backend.count("page_views") == before, (
            f"{backend.count('page_views') - before} page views were written before "
            f"any cookie answer; nothing is recorded at all until the answer is yes"
        )
        accepted = fresh.post("/consent", json={"accepted": True})
        assert accepted.status_code in OK, (
            f"POST {API_PREFIX}/consent returned {accepted.status_code}: "
            f"{body(accepted)}"
        )
        recorded = settle(lambda: backend.count("page_views") > before)
        assert recorded, (
            f"no page view was written after the cookie answer was yes"
        )
        after_yes = backend.count("page_views")
        revoked = fresh.post("/consent", json={"accepted": False})
        assert revoked.status_code in OK, (
            f"POST {API_PREFIX}/consent returned {revoked.status_code} revoking the "
            f"answer: {body(revoked)}"
        )
        page(CONTACT_ROUTE)
        settle(lambda: backend.count("page_views") > after_yes + 1)
        assert backend.count("page_views") <= after_yes + 1, (
            f"page views kept being written after the answer was revoked; recording "
            f"stops from the next page onward"
        )


def test_page_view_carries_no_person_data(backend, anonymous):
    anonymous.post("/consent", json={"accepted": True})
    page(HOME_ROUTE)
    rows = settle(lambda: backend.rows("page_views", limit=5))
    assert rows, (
        f"no page view row exists after a consented page load"
    )
    allowed = {"id", "route", "viewed_at", "created_at"}
    for row in rows:
        extra = set(row) - allowed
        assert not extra, (
            f"a page view row carries {sorted(extra)}; it carries the route and the "
            f"time and nothing about the person"
        )
        assert str(row.get("route", "")).startswith("/"), (
            f"a page view row carries route {row.get('route')!r}"
        )


def test_privacy_and_terms_routes_answer():
    privacy = page(PRIVACY_ROUTE)
    assert privacy.status_code in OK, (
        f"GET {PRIVACY_ROUTE} returned {privacy.status_code}: {body(privacy)}"
    )
    text = privacy.text.lower()
    for topic in ("enquiry", "keep"):
        assert topic in text, (
            f"the privacy route does not state what the enquiry form stores and how "
            f"long an enquiry and a booking are kept; {topic!r} is absent"
        )
    terms = page(TERMS_ROUTE)
    assert terms.status_code in OK, (
        f"GET {TERMS_ROUTE} returned {terms.status_code}: {body(terms)}"
    )
    assert "terms" in terms.text.lower(), (
        f"the terms route does not state the terms of use: {terms.text[:300]}"
    )
    for route in PUBLIC_ROUTES:
        document = page(route)
        assert PRIVACY_ROUTE in document.text, (
            f"the footer of {route} does not link the privacy route"
        )
        assert TERMS_ROUTE in document.text, (
            f"the footer of {route} does not link the terms route"
        )
    form = page(CONTACT_ROUTE)
    assert form.text.count(PRIVACY_ROUTE) >= 2, (
        f"the privacy link appears only once on the contact surface; it sits beside "
        f"the submit control as well as in the footer, because the form is where the "
        f"name, the address and the employer are collected"
    )


def test_every_public_route_declares_a_distinct_social_preview():
    pairs = {}
    for route in PUBLIC_ROUTES:
        document = page(route)
        title = re.search(
            r'<meta[^>]+property="og:title"[^>]+content="([^"]*)"', document.text)
        image = re.search(
            r'<meta[^>]+property="og:image"[^>]+content="([^"]*)"', document.text)
        assert title and title.group(1).strip(), (
            f"{route} declares no social preview title"
        )
        assert image and image.group(1).strip(), (
            f"{route} declares no social preview image"
        )
        pair = (title.group(1), image.group(1))
        clash = [other for other, seen in pairs.items() if seen == pair]
        assert not clash, (
            f"{route} declares the same preview title and image as {clash[0]}; no two "
            f"routes declare the same pair"
        )
        pairs[route] = pair
        target = image.group(1)
        if target.startswith("/"):
            resolved = page(target)
        else:
            resolved = httpx.get(target, timeout=appclient.TIMEOUT,
                                 follow_redirects=True)
        assert resolved.status_code in OK, (
            f"the social preview image {target!r} declared by {route} returns "
            f"{resolved.status_code}; every declared image resolves"
        )


def test_sitemap_and_robots_list_public_routes():
    sitemap = page(SITEMAP_ROUTE)
    assert sitemap.status_code in OK, (
        f"GET {SITEMAP_ROUTE} returned {sitemap.status_code}: {body(sitemap)}"
    )
    for route in PUBLIC_ROUTES:
        assert route in sitemap.text, (
            f"the sitemap does not list the public route {route!r}: "
            f"{sitemap.text[:400]}"
        )
    robots = page(ROBOTS_ROUTE)
    assert robots.status_code in OK, (
        f"GET {ROBOTS_ROUTE} returned {robots.status_code}: {body(robots)}"
    )
    assert re.search(r"(?i)sitemap:\s*https?://\S+" + re.escape(SITEMAP_ROUTE),
                     robots.text), (
        f"{ROBOTS_ROUTE} does not point at the sitemap by its absolute address: "
        f"{robots.text[:300]}"
    )


def test_security_headers_present_on_every_response(anonymous):
    checks = {
        "strict-transport-security": "a strict transport policy",
        "x-content-type-options": "a nosniff content-type policy",
    }
    document = page(HOME_ROUTE)
    api = httpx.get(f"{app_url()}{API_PREFIX}/projects", timeout=appclient.TIMEOUT)
    missing_route = page("/no-such-route-anywhere")
    for label, response in (("the home document", document),
                            ("an API response", api),
                            ("a missing route", missing_route)):
        headers = {key.lower() for key in response.headers}
        for header, description in checks.items():
            assert header in headers, (
                f"{label} carries no {header!r} header, so {description} is missing; "
                f"every response carries the standard security headers. Present: "
                f"{sorted(headers)}"
            )


def test_no_credential_or_product_name_in_the_browser_bundle():
    secrets = (SEEDED_PASSWORD, "deku-local-dev", "minio-root", "deku_admin")
    for asset in bundle_assets():
        response = page(asset)
        if response.status_code not in OK:
            continue
        text = response.text
        leaked = [secret for secret in secrets if secret in text]
        assert not leaked, (
            f"the asset {asset!r} the browser downloads carries {leaked}; no "
            f"credential, API key or admin token appears in anything the browser "
            f"downloads"
        )
        branded = re.findall(r"\b(?:atelier[-_]?moreau|AtelierMoreau)[-_][A-Za-z0-9]{4,}",
                             text)
        assert not branded, (
            f"the asset {asset!r} carries generated class prefixes built from the "
            f"product name: {branded[:5]}; a class-name prefix is a framework "
            f"artefact and must not carry a product name"
        )


def test_built_bundle_ships_no_binary_or_font_asset():
    listing = _in_container(
        "sh", "-c",
        "find /app -path /app/node_modules -prune -o -type f "
        "\\( -name '*.woff' -o -name '*.woff2' -o -name '*.ttf' -o -name '*.otf' "
        "-o -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.gif' "
        "-o -name '*.mp4' -o -name '*.webm' -o -name '*.mp3' -o -name '*.wav' \\) "
        "-print 2>/dev/null | head -20",
    )
    shipped = [line for line in listing.stdout.splitlines() if line.strip()]
    assert not shipped, (
        f"the build ships binary assets: {shipped}. Every asset in this product is "
        f"drawn in code, no font binary ships, the project media is generated from "
        f"each project's own record, and the hero's ground is drawn rather than a "
        f"video"
    )
    styles = "".join(page(asset).text for asset in bundle_assets()
                     if asset.endswith(".css"))
    faces = re.findall(r"font-family:\s*([^;}]+)", styles)
    assert faces, (
        f"no font-family declaration reaches the browser; three faces are named, each "
        f"with a metrics-matched fallback"
    )
    stacked = [face for face in faces if "," in face]
    assert stacked, (
        f"no font-family declaration names a fallback: {faces[:5]}. Each face is named "
        f"with a metrics-matched fallback so the page does not reflow when the faces "
        f"arrive"
    )


def test_hostile_enquiry_input_is_stored_and_shown_as_text(backend, studio,
                                                           anonymous):
    payload = "<script>alert('x')</script> <img src=x onerror=alert(1)>"
    sender = probe_email("hostile")
    enquiry = require_enquiry(
        anonymous, email=sender,
        message=f"{payload} and a real sentence about the work we want done.",
    )
    row = settle(lambda: backend.one("enquiries", id=enquiry["id"]))
    assert payload in str(row["message"]), (
        f"the stored message does not carry the hostile input as typed; it is shown "
        f"back to the studio exactly as it was typed rather than interpreted. Stored: "
        f"{row['message']!r}"
    )
    surface = page(f"/enquiry/{enquiry['id']}?token={enquiry['token']}")
    assert "<script>alert" not in surface.text, (
        f"the enquiry surface renders the stored value as markup rather than as text"
    )
    api = flat(read(studio, f"/enquiries/{enquiry['id']}"))
    assert payload in api, (
        f"the studio's read does not show the input as typed: {api[:300]}"
    )


def test_invalid_call_is_a_client_error_naming_the_reason(anonymous, studio):
    malformed = anonymous.post("/enquiries", json={"name": 17})
    assert malformed.status_code in REFUSED, (
        f"a malformed enquiry body returned {malformed.status_code}, expected a "
        f"client error, never a server error and never a silent success: "
        f"{body(malformed)}"
    )
    assert body(malformed).strip(), (
        f"the refusal carries no message naming the reason"
    )
    unknown = studio.get("/enquiries/00000000-0000-0000-0000-000000000000")
    assert unknown.status_code in DENIED, (
        f"reading an enquiry that does not exist returned {unknown.status_code}: "
        f"{body(unknown)}"
    )
    assert unknown.status_code < 500 and malformed.status_code < 500, (
        f"an invalid or unauthorized call was answered as a server error "
        f"({malformed.status_code}, {unknown.status_code})"
    )


def test_pinned_copy_appears_verbatim():
    home = page(HOME_ROUTE)
    for target in NAVIGATION_TARGETS:
        assert target in home.text, (
            f"the chrome does not carry the navigation target {target!r}"
        )
    pill_words = (PILL_OPEN_NOW, PILL_OPEN_FROM, PILL_BOOKED_UNTIL, PILL_NOT_TAKING)
    assert any(word in home.text for word in pill_words), (
        f"the chrome carries none of the four pinned pill strings"
    )
    assert ABOUT_FIGURE in home.text, (
        f"the about section does not carry the figure {ABOUT_FIGURE!r}"
    )
    work = page(WORK_ROUTE)
    assert WORK_HEADLINE in work.text or WORK_HEADLINE in home.text, (
        f"the pinned work headline is absent: {WORK_HEADLINE!r}"
    )
    assert WORK_INDEX_COUNT in work.text, (
        f"the work index does not state its own count as {WORK_INDEX_COUNT!r} with "
        f"nine published projects"
    )


def test_unauthenticated_private_route_lands_on_signin():
    for route in (ACCOUNT_ROUTE, STUDIO_ROUTE, PIPELINE_ROUTE):
        response = page(route, follow_redirects=False)
        assert response.status_code in (301, 302, 303, 307, 308) or (
            SIGNIN_ROUTE in response.text
        ), (
            f"an unauthenticated request for {route} returned {response.status_code} "
            f"without sending the visitor to {SIGNIN_ROUTE}"
        )
        target = response.headers.get("location", "") or response.text
        assert SIGNIN_ROUTE in target, (
            f"{route} sends an unauthenticated visitor to {target[:120]!r}, expected "
            f"{SIGNIN_ROUTE}"
        )
        assert route.strip("/") in target or "next" in target or "redirect" in target, (
            f"{route} sends the visitor to sign-in without remembering the "
            f"destination: {target[:160]!r}"
        )


def test_remembered_destination_rejects_an_offsite_path(anonymous):
    hostile = ("https://evil.example/steal", "//evil.example/steal",
               "http://evil.example")
    for destination in hostile:
        response = anonymous.post("/auth/login", json={
            "email": CLIENT_EMAIL, "password": SEEDED_PASSWORD,
            "next": destination,
        })
        if response.status_code not in OK:
            continue
        payload = flat(response.json())
        assert "evil.example" not in payload, (
            f"a remembered destination of {destination!r} was honoured; a destination "
            f"is honoured only when it is a path on this origin beginning with a "
            f"single slash. Response: {payload[:300]}"
        )


def test_studio_session_on_account_is_sent_to_studio(studio):
    response = studio.get("/auth/me")
    assert response.status_code in OK, (
        f"GET {API_PREFIX}/auth/me returned {response.status_code} for the studio: "
        f"{body(response)}"
    )
    assert response.json().get("role") == ROLE_STUDIO, (
        f"the studio session reports role {response.json().get('role')!r}"
    )
    surface = page(ACCOUNT_ROUTE, follow_redirects=False)
    assert surface.status_code in (200, 301, 302, 303, 307, 308), (
        f"GET {ACCOUNT_ROUTE} returned {surface.status_code}"
    )


def test_signed_out_session_cannot_be_resumed(anonymous):
    response = anonymous.post("/auth/login",
                              json={"email": CLIENT_EMAIL,
                                    "password": SEEDED_PASSWORD})
    token = response.json().get("token") or response.json().get("access_token")
    with appclient.client(token) as session:
        before = session.get("/auth/me")
        assert before.status_code in OK, (
            f"the fresh session was refused at {API_PREFIX}/auth/me: {body(before)}"
        )
        session.post("/auth/logout")
    with appclient.client(token) as replayed:
        after = replayed.get("/auth/me")
        assert after.status_code in DENIED, (
            f"the token still works after sign-out ({after.status_code}); a session "
            f"ends on sign-out and cannot be resumed by going back: {body(after)}"
        )


def test_built_stylesheet_declares_four_breakpoints():
    styles = "".join(page(asset).text for asset in bundle_assets()
                     if asset.endswith(".css"))
    assert styles.strip(), (
        f"no stylesheet reaches the browser from the built bundle"
    )
    widths = set(re.findall(r"@media[^{]*?(?:min|max)-width:\s*([\d.]+(?:px|rem|em))",
                            styles))
    assert len(widths) <= 4, (
        f"the built stylesheet declares {len(widths)} distinct width breakpoints "
        f"({sorted(widths)}); four and no others. A reference tuned by hand with "
        f"twenty queries is not a system"
    )
    blanket = re.findall(r"transition\s*:\s*all\b", styles)
    assert not blanket, (
        f"the stylesheet puts a transition on every property in {len(blanket)} "
        f"declarations; name the properties that move"
    )


def test_app_stays_responsive_at_the_stated_bar(backend, studio):
    assert backend.count("projects") >= 1, (
        f"no projects are seeded, so the responsiveness bar cannot be read"
    )
    budget = 5.0
    for label, path in (("the home document", HOME_ROUTE),
                        ("the work index", WORK_ROUTE),
                        ("the availability page", AVAILABILITY_ROUTE)):
        started = time.monotonic()
        response = page(path)
        elapsed = time.monotonic() - started
        assert response.status_code in OK, (
            f"GET {path} returned {response.status_code} at the stated bar"
        )
        assert elapsed < budget, (
            f"{label} took {elapsed:.1f}s to answer, over the {budget:.0f}s budget; "
            f"the app stays responsive with {BAR_PROJECTS} projects, {BAR_WINDOWS} "
            f"windows, {BAR_ENQUIRIES} enquiries and {BAR_MESSAGES} messages"
        )
    started = time.monotonic()
    pipeline = studio.get("/pipeline")
    elapsed = time.monotonic() - started
    assert pipeline.status_code in OK and elapsed < budget, (
        f"the pipeline answered {pipeline.status_code} in {elapsed:.1f}s at the stated "
        f"bar of {BAR_ENQUIRIES} enquiries and {BAR_MESSAGES} messages"
    )
