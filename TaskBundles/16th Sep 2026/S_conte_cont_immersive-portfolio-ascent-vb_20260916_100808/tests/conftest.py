from __future__ import annotations

import hashlib
import io
import json
import struct
import time
import uuid
import zlib

import httpx
import pytest
from playwright.sync_api import sync_playwright

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"
OWNER_EMAIL = "owner@example.com"
REVIEWER_EMAIL = "reviewer@example.com"
REVIEWER2_EMAIL = "reviewer2@example.com"
OWNER_NAME = "Elian Kais Brandtsteiner"

PUBLISHED_KEYS = ("lumenar", "stackr", "tide", "ascent", "playground")
DRAFT_KEY = "vela"
CASE_STUDY_KEYS = ("lumenar", "stackr", "tide", "ascent")
REGISTRY_ORDER = ("lumenar", "stackr", "tide", "ascent", "playground")
HUB_ORDER = ("lumenar", "tide", "stackr", "ascent")
HUB_LABELS = ("Lumenar", "Tide", "Stackr", "Ascent")
MENU_LABELS = {"lumenar": "Lumenar", "stackr": "Stackr", "tide": "Tide",
               "ascent": "Ascent", "playground": "Playground", "vela": "Vela"}
CREATION_IDS = {"lumenar": "03", "stackr": "02", "tide": "01", "ascent": "04",
                "playground": "05", "vela": "06"}
CATEGORIES = ("CREATIVE COMPUTING", "AR DEVELOPMENT", "PHYSICAL COMPUTING",
              "CREATIVE CODING", "LAB")
OPENS_VALUES = ("caseStudy", "lab", "none")
PROJECT_STATUSES = ("draft", "published")
PROJECT_RECORD_KEYS = ("id", "key", "order", "hubOrder", "menuLabel", "lines",
                       "linesMobile", "eyebrow", "category", "labels", "note",
                       "opens", "path", "status", "headline", "meta", "body",
                       "cv", "highlight", "hero", "telemetry", "publishedAt")

JOURNEY_COMPONENTS = ("scrollIndicator", "openingHeadline", "projectTiles",
                      "summitHeadline", "contactCta", "biographyPanel",
                      "caseStudyPreview")
DESKTOP_COMPONENT_BANDS = {"scrollIndicator": (0.0, 8.0),
                           "openingHeadline": (0.0, 42.0),
                           "projectTiles": (42.5, 87.0),
                           "summitHeadline": (90.0, 100.0),
                           "contactCta": (92.0, 100.0),
                           "biographyPanel": (86.0, 100.0),
                           "caseStudyPreview": (90.0, 100.0)}
MOBILE_COMPONENT_BANDS = {"scrollIndicator": (0.0, 8.0),
                          "openingHeadline": (0.0, 34.0),
                          "projectTiles": (35.0, 96.0),
                          "summitHeadline": (96.5, 100.0),
                          "contactCta": (97.0, 100.0),
                          "biographyPanel": (93.0, 100.0),
                          "caseStudyPreview": (96.5, 100.0)}
DESKTOP_BAND_EDGES = (42.5, 51.4, 60.3, 69.2, 78.1, 87.0)
DESKTOP_MENU_TARGETS = (0.4695, 0.5585, 0.6475, 0.7365, 0.8255)
MOBILE_BAND = (35.0, 96.0)
DESKTOP_FADE_IN = 0.7
DESKTOP_FADE_OUT = 0.2
MOBILE_FADE_IN = 0.86
MOBILE_FADE_OUT = 0.1
DESKTOP_PAGES_AT_900 = 4.947
DESKTOP_PAGES_AT_1110 = 4.2
MOBILE_PAGES = 5.8
JOURNEY_TRAVEL = 3552
DEFAULT_VIEWPORT_HEIGHT = 900
INVALID_BRANCH = "invalid_branch"
INVALID_VIEWPORT = "invalid_viewport"

BLOCK_TYPES = ("standfirst", "statement", "stickyMedia", "mediaPair", "caption")
STATEMENT_KINDS = ("claim", "method", "failure", "change", "forward", "close")
META_HEADINGS = ("My Role", "Built with", "Shown", "Focus")
COMPOSER_ERROR_RULES = (
    "block_type", "standfirst_first", "failure_required", "forward_required",
    "close_last", "failure_resolved", "heading_length", "paragraph_length",
    "media_caption", "media_ref", "meta_shape", "lines_shape",
    "menu_label_length", "note_length", "category", "cv_bullet_numeral")
COMPOSER_WARNING_RULES = ("heading_verb", "note_imperative")
FINDING_KEYS = ("rule", "severity", "blockIndex", "message")
SEVERITIES = ("error", "warning")

MEDIA_KEY_PREFIX = "projects/"
UPLOAD_LIMIT_BYTES = 5242880
UNSUPPORTED_MEDIA = "unsupported_media"
MEDIA_TOO_LARGE = "media_too_large"

CONTACT_MIN_ELAPSED_MS = 2000
CONTACT_MESSAGE_LIMIT = 4000
CONTACT_CODES = ("missing_field", "invalid_email", "too_long", "rate_limited")
CONTACT_PER_EMAIL_HOUR = 5

RELATIONSHIPS = ("collaborator", "tutor", "exhibitor", "client", "peer")
REVIEW_STATES = ("submitted", "awaiting_confirmation", "confirmed", "published",
                 "declined", "withdrawn")
REVIEW_CODES = ("missing_name", "missing_role", "invalid_relationship",
                "missing_scope", "invalid_scope", "body_too_short",
                "body_too_long", "field_too_long", "already_submitted")
REVIEW_BODY_MIN_WORDS = 40
REVIEW_BODY_MAX_WORDS = 220
INVITATION_TOKEN_LENGTH = 22
UNUSED_INVITATION = "Rv7Kq2Lm9Xw4Tz8Bn3Hc5D"
EXPIRED_INVITATION = "Ex4pIr3dTk9Lq2Wm7Zn5Vb"
PUBLISHED_INVITATION = "Qm8Wd3Rf6Yh1Uj5Ik9Ol2P"
CONFIRMED_INVITATION = "Hd5Jk8Lz2Qp7Rs4Tv9Wx1Y"
AWAITING_INVITATION = "Pn2Xs7Vc4Bq9Mw1Ez6Ty3K"
PUBLIC_REVIEW_KEYS = ("id", "reviewerName", "reviewerRole", "organisation",
                      "relationship", "scope", "period", "body", "decidedAt",
                      "attribution")
PRIVATE_REVIEW_KEYS = ("email", "declineReason", "revisionNote", "token")

SEEDED_RUN = "lumenar-crosswire-2026"
RUN_VISITS = 372
RUN_STAYS_BEYOND_15 = 221
RUN_COMPLETE_VIEWINGS = 67
RUN_MEDIAN_DWELL = 20
RUN_COMPLETION_RATE = 0.1801
RUN_TRUSTED_PROPORTION = 0.96
RUN_UNATTENDED_SECONDS = 345600
DWELL_BINS = ("0-5", "5-10", "10-15", "15-20", "20-30", "30-45", "45-60", "60+")
FIGURE_KEYS = ("visits", "staysBeyond15", "completeViewings", "medianDwellSeconds",
               "completionRate", "trustedProportion", "unattendedSeconds",
               "dwellHistogram")
TELEMETRY_KINDS = ("presence_start", "presence_end", "heartbeat", "sensor_health")
SESSION_OUTCOMES = ("completed", "partial", "discarded", "truncated")
HEALTH_STATUSES = ("trusted", "degraded", "untrusted")
INGEST_BATCH_LIMIT = 256
MIN_INGEST_INTERVAL_MS = 30000
TRUST_FLOOR = 0.9
LUMENAR_SEQUENCE_SECONDS = 60
LUMENAR_FLOOR_SECONDS = 3
STUCK_HIGH_MS = 600000
CHATTER_TRIGGERS = 120
BATCH_TOO_LARGE = "batch_too_large"
DEVICE_UNAUTHORIZED = "device_unauthorized"
INVALID_EVENT = "invalid_event"
DUPLICATE_DEVICE = "duplicate_device"
UNTRUSTED_RUN = "untrusted_run"

SEARCH_TYPE_WEIGHTS = (("project", 1.0), ("caseStudySection", 0.85),
                       ("cvEntry", 0.7), ("review", 0.6), ("labEntry", 0.5),
                       ("cvSkill", 0.35), ("labCaption", 0.25))
SEARCH_TYPE_ORDER = tuple(name for name, _ in SEARCH_TYPE_WEIGHTS)
SEARCH_EMPTY_COPY = "Nothing matched. Try one of these."
SUGGESTION_COUNT = 12
TOOL_TAG = "TouchDesigner"
SEARCH_RESULT_KEYS = ("id", "type", "title", "subtitle", "route", "anchor",
                      "snippet", "score")
SEARCH_DOCUMENT_KEYS = ("id", "type", "route", "anchor", "title", "subtitle",
                        "body", "tags", "year", "weight")

PUBLIC_ROUTES = ("/", "/case-study", "/lab", "/highlights", "/cv",
                 "/peer-reviews", "/search", "/flat")
PRIVATE_ROUTE_FRAGMENTS = ("/console", "/signin", "/signup", "/review/", "preview=")
NOT_FOUND_HEADING = "Nothing lives at this address"
NOT_FOUND_LINK = "Back to the portfolio"
NOT_FOUND_STATUS = 404
FLAT_FOOT = ("This is the plain version of the site. Your browser or device "
             "could not run the moving one.")
FLAT_RETURN = "Try the moving version"
MOTION_CHOICES = ("Full", "Reduced", "None")
NEXT_PROJECT_EYEBROW = "VIEW NEXT PROJECT"
PLAYGROUND_EYEBROW = "VIEW PLAYGROUND"
SELECTED_WORK_PREFIX = "SELECTED WORK | "
PLAYGROUND_EYEBROW_FULL = "OFF ROUTE | PLAYGROUND"
REVIEW_BLOCK_HEADING = "What people who were there said"
PEER_REVIEW_EMPTY = "Nothing published yet"
LAB_MASTHEAD = "OFF THE MAIN ROUTE"
HIGHLIGHTS_MASTHEAD = "PROJECT HIGHLIGHTS"
CONTACT_HEADING = "I" + chr(39) + "LL BE IN TOUCH"
CONTACT_SUCCESS = "Thanks, I" + chr(39) + "ll reply as soon as I can."
STAT_ROW_LABELS = ("visits", "stayed the full 60 seconds", "median stay",
                   "unattended")
HISTOGRAM_TITLE = "How long people stayed"
CV_FACTS = ("London, UK", "relocation across Europe",
            "German (native), English (fluent), Spanish (basic)",
            "EU citizen (Austria). Eligible for UK Graduate Route")
CV_ASIDE_SECTIONS = ("Education", "Skills", "Recognition and Talks")
CV_MAIN_SECTIONS = ("Experience", "Selected Work")
CV_ENTRY_KEYS = ("key", "title", "subtitle", "year", "context", "bullets", "tools")
AUTH_TOKEN_FIELD = "access_token"
SIGNUP_ROLE = "reviewer"
EMAIL_TAKEN = "email_taken"
SIGNUP_MIN_PASSWORD = 10
HEALTH_ROUTE = "/health"
HEALTH_STATUS = 200
SECRET_FRAGMENTS = ("deku-store-key", "deku-store-secret", "postgresql://",
                    "password_hash", "key_hash")
BINARY_ASSET_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp", ".avif", ".mp4",
                         ".webm", ".glb", ".gltf", ".wasm", ".woff", ".woff2",
                         ".ttf", ".otf", ".mp3", ".wav", ".draco")

SETTLE_DEADLINE = 25.0
SETTLE_INTERVAL = 0.25


def app_origin() -> str:
    return appclient.app_url()


def fresh_email(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}@example.com"


def fresh_token(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


def page_response(path: str, headers: dict | None = None) -> httpx.Response:
    return httpx.get(f"{app_origin()}{path}", timeout=appclient.TIMEOUT,
                     follow_redirects=False, headers=headers or {})


def page_body(path: str) -> str:
    response = page_response(path)
    assert response.status_code < 400, (
        f"GET {path} answered {response.status_code}: {response.text[:300]}")
    return response.text


def settle(predicate, what: str):
    deadline = time.monotonic() + SETTLE_DEADLINE
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        time.sleep(SETTLE_INTERVAL)
    raise AssertionError(f"{what} never settled within the deadline; last saw {last!r}")


def body(response: httpx.Response):
    if "json" in response.headers.get("content-type", "").lower():
        return response.json()
    return response.text


def is_client_error(status: int) -> bool:
    return 400 <= status < 500


def refusal(response: httpx.Response, where: str):
    assert is_client_error(response.status_code), (
        f"{where} answered {response.status_code}, and a refusal is a client error: "
        f"{response.text[:300]}")
    return body(response)


def refusal_code(response: httpx.Response, where: str) -> str:
    payload = refusal(response, where)
    assert isinstance(payload, dict), f"{where} carried no error body: {payload!r}"
    if "code" in payload:
        assert payload.get("ok") is False, (
            f"{where} carried a code without an ok of false: {payload}")
        return str(payload["code"])
    assert "detail" in payload, (
        f"{where} carried neither a code nor a detail: {payload}")
    return json.dumps(payload["detail"], default=str)


def denied(response: httpx.Response, where: str) -> httpx.Response:
    assert response.status_code in (401, 403, 404), (
        f"{where} answered {response.status_code} where a denial was due: "
        f"{response.text[:300]}")
    return response


def not_found(response: httpx.Response, where: str) -> httpx.Response:
    assert response.status_code == NOT_FOUND_STATUS, (
        f"{where} answered {response.status_code} where a not-found was due: "
        f"{response.text[:300]}")
    return response


def png_bytes(width: int = 8, height: int = 8, tone: int = 40) -> bytes:
    raw = b"".join(b"\x00" + bytes([tone, tone, tone] * width) for _ in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))


def digest_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def upload_media(api: httpx.Client, key: str, data: bytes | None = None,
                 name: str = "frame.png",
                 content_type: str = "image/png") -> httpx.Response:
    payload = data if data is not None else png_bytes(tone=11)
    files = {"file": (name, io.BytesIO(payload), content_type)}
    return api.post(f"/projects/{key}/media", files=files)


def journey(branch: str = "desktop", viewport_height: int | None = None) -> dict:
    params = {"branch": branch}
    if viewport_height is not None:
        params["viewportHeight"] = viewport_height
    response = httpx.get(f"{appclient.api_base()}/journey", params=params,
                         timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"the journey answered {response.status_code}: {response.text[:300]}")
    return response.json()


def journey_response(**params) -> httpx.Response:
    return httpx.get(f"{appclient.api_base()}/journey", params=params,
                     timeout=appclient.TIMEOUT)


def band_for(document: dict, key: str) -> dict:
    tiles = document.get("tiles") or []
    for tile in tiles:
        if tile.get("key") == key:
            return tile
    raise AssertionError(f"the journey carries no band for {key}: {tiles}")


def component_for(document: dict, name: str) -> dict:
    components = document.get("components") or []
    for component in components:
        if component.get("name") == name:
            return component
    raise AssertionError(f"the journey carries no component {name}: {components}")


def public_projects() -> list:
    response = httpx.get(f"{appclient.api_base()}/projects",
                         timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"the project list answered {response.status_code}: {response.text[:300]}")
    payload = response.json()
    assert isinstance(payload, list), f"the project list is not an array: {payload!r}"
    return payload


def public_project(key: str) -> dict:
    response = httpx.get(f"{appclient.api_base()}/projects/{key}",
                         timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"the public read of {key} answered {response.status_code}")
    return response.json()


def published_reviews() -> list:
    response = httpx.get(f"{appclient.api_base()}/reviews",
                         timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"the review wall answered {response.status_code}: {response.text[:300]}")
    return response.json()


def search(query: str) -> dict:
    response = httpx.get(f"{appclient.api_base()}/search", params={"q": query},
                         timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"the search for {query!r} answered {response.status_code}")
    return response.json()


def search_index() -> dict:
    response = httpx.get(f"{appclient.api_base()}/search-index",
                         timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"the search index answered {response.status_code}")
    return response.json()


def group_for(document: dict, kind: str) -> dict | None:
    for group in document.get("groups") or []:
        if group.get("type") == kind:
            return group
    return None


def cv_document() -> dict:
    response = httpx.get(f"{appclient.api_base()}/cv", timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"the curriculum vitae answered {response.status_code}")
    return response.json()


def contact_payload(**fields) -> dict:
    payload = {"name": "Mira Vance", "email": fresh_email("sender"),
               "message": "I saw Lumenar at Crosswire and would like to talk "
                          "about a commission for our gallery foyer.",
               "website": "", "elapsedMs": 4200}
    payload.update(fields)
    return payload


def send_contact(**fields) -> httpx.Response:
    return httpx.post(f"{appclient.api_base()}/contact",
                      json=contact_payload(**fields), timeout=appclient.TIMEOUT)


def review_body(words: int) -> str:
    stem = ("Elian carried the interaction work across two builds of this piece "
            "and kept a written record of every failure before fixing it")
    filler = stem.split()
    return " ".join((filler * 20)[:words])


def review_payload(**fields) -> dict:
    payload = {"reviewerName": "Riya Anand",
               "reviewerRole": "Coral and interaction lead",
               "organisation": "Riverbank Creative Computing Institute",
               "relationship": "collaborator", "scope": "practice",
               "period": "spring 2026", "body": review_body(80)}
    payload.update(fields)
    return payload


def presence_events(boot_seconds: int, first_seq: int = 1) -> list:
    return [{"seq": first_seq, "uptimeMs": 1000, "kind": "presence_start",
             "payload": {}},
            {"seq": first_seq + 1, "uptimeMs": 1000 + boot_seconds * 1000,
             "kind": "presence_end", "payload": {}}]


def health_event(seq: int, uptime_ms: int, **payload) -> dict:
    values = {"triggersInWindow": 14, "meanIntervalMs": 4200,
              "longestHighMs": 9000, "ambientReference": 120}
    values.update(payload)
    return {"seq": seq, "uptimeMs": uptime_ms, "kind": "sensor_health",
            "payload": values}


def ingest(device_key: str, device_id: str, boot_id: str,
           events: list) -> httpx.Response:
    return httpx.post(f"{appclient.api_base()}/ingest",
                      headers={"X-Device-Key": device_key},
                      json={"deviceId": device_id, "bootId": boot_id,
                            "events": events}, timeout=appclient.TIMEOUT)


def provision_device(api: httpx.Client, run_id: str) -> dict:
    device_id = fresh_token("device")
    response = api.post("/admin/devices", json={"deviceId": device_id,
                                                "runId": run_id})
    assert response.status_code < 300, (
        f"provisioning a device answered {response.status_code}: "
        f"{response.text[:300]}")
    record = response.json()
    assert record.get("deviceKey"), f"the device carries no key: {record}"
    return record


def open_run(api: httpx.Client, project_key: str = "lumenar") -> dict:
    run_id = fresh_token("run")
    response = api.post("/admin/runs", json={
        "runId": run_id, "projectKey": project_key,
        "title": "Lumenar studio run", "startsOn": "2026-06-11",
        "endsOn": "2026-06-14", "openFrom": "00:00", "openTo": "24:00"})
    assert response.status_code < 300, (
        f"opening a run answered {response.status_code}: {response.text[:300]}")
    return response.json()


def issue_invitation(api: httpx.Client, email: str, scope: str) -> dict:
    response = api.post("/admin/invitations", json={"email": email,
                                                    "scope": scope})
    assert response.status_code < 300, (
        f"issuing an invitation answered {response.status_code}: "
        f"{response.text[:300]}")
    record = response.json()
    assert record.get("token"), f"the invitation carries no token: {record}"
    return record


def submit_review(token: str, api: httpx.Client, **fields) -> httpx.Response:
    return api.post(f"/review/{token}", json=review_payload(**fields))


def my_reviews(api: httpx.Client) -> list:
    response = api.get("/my/reviews")
    assert response.status_code == 200, (
        f"the reviewer own list answered {response.status_code}: "
        f"{response.text[:300]}")
    return response.json()


def review_state(api: httpx.Client, review_id: str) -> str:
    for row in my_reviews(api):
        if str(row.get("id")) == str(review_id):
            return str(row.get("state"))
    raise AssertionError(f"review {review_id} is absent from the reviewer own list")


def admin_reviews(api: httpx.Client) -> list:
    response = api.get("/admin/reviews")
    assert response.status_code == 200, (
        f"the console review list answered {response.status_code}: "
        f"{response.text[:300]}")
    return response.json()


def admin_review(api: httpx.Client, state: str) -> dict:
    rows = [row for row in admin_reviews(api) if row.get("state") == state]
    assert rows, f"no seeded review is in state {state!r}"
    return rows[0]


def flat(payload) -> str:
    return json.dumps(payload, default=str).lower()


def open_site(surface, path: str = "/"):
    surface.goto(f"{app_origin()}{path}", wait_until="networkidle")
    return surface


@pytest.fixture(scope="session")
def db():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def anon():
    with appclient.client() as c:
        yield c


@pytest.fixture()
def owner():
    with appclient.client(appclient.login(OWNER_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture()
def reviewer():
    with appclient.client(appclient.login(REVIEWER_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture()
def other_reviewer():
    with appclient.client(appclient.login(REVIEWER2_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as driver:
        chromium = driver.chromium.launch(args=["--no-sandbox"])
        yield chromium
        chromium.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    surface = context.new_page()
    yield surface
    context.close()


@pytest.fixture()
def narrow_page(browser):
    context = browser.new_context(viewport={"width": 390, "height": 844})
    surface = context.new_page()
    yield surface
    context.close()
