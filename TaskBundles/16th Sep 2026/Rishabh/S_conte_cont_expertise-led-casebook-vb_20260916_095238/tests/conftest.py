from __future__ import annotations

import hashlib
import os
import re
import threading
import time

import httpx
import pytest

import _shapes
import appclient
import capabilities

SETTLE_SECONDS = 2.0
POLL_DEADLINE_SECONDS = 30.0

APP_PASSWORD = "deku-demo-pw-2026"
OWNER_EMAIL = "owner@example.com"
EDITOR_EMAIL = "editor@example.com"
VISITOR_EMAIL = "visitor@example.com"
OWNER_NAME = "Mara Lind"
EDITOR_NAME = "Jonas Weller"

STUDIO_NAME = "Northform"

EXPERTISE_SLUGS = ("real-estate", "corporate", "startups", "ecommerce")
EXPERTISE_NAMES = ("Real Estate", "Corporate", "Startups", "eCommerce")
EXPERTISE_SENTENCES = (
    "Luxury real estate website design - iconic websites for iconic properties.",
    "Inspiring, functional, and result-oriented websites for enterprises. "
    "Full-cycle award-winning solutions from strategy to launch.",
    "From idea to a product: creating successful digital services for innovative "
    "startups and established businesses.",
    "High-class eCommerce solutions with research-grounded UX design, award-class "
    "UI design and top-grade front-end.",
)
TAG_SLUGS = (
    "promo-website", "corporate-website", "online-store", "self-service", "saas",
    "banking", "customer-portal", "trading-platform", "branding",
    "3d-visualisation", "real-estate",
)

SEEDED_PUBLISHED_SLUGS = (
    "cliffside-residences",
    "kestrel-annual-review",
    "vantage-onboarding",
    "meridian-duty-free",
    "harbour-quarter",
    "ostend-investor-portal",
    "pinemark-trading-desk",
    "halden-home-store",
    "northline-self-care",
    "vantage-pitch-site",
)
SEEDED_ALL_SLUGS = (
    "cliffside-residences",
    "kestrel-annual-review",
    "vantage-onboarding",
    "meridian-duty-free",
    "harbour-quarter",
    "ostend-loyalty-store",
    "ostend-investor-portal",
    "pinemark-trading-desk",
    "halden-home-store",
    "northline-self-care",
    "vantage-pitch-site",
    "pinemark-mobile-app",
)
DRAFT_SLUG = "pinemark-mobile-app"
DRAFT_TITLE = "Pinemark Mobile App"
WITHDRAWN_SLUG = "ostend-loyalty-store"
WITHDRAWN_TITLE = "Ostend Loyalty Store"
CASE_WITH_BANKING = "kestrel-annual-review"
CORPORATE_BANKING_SLUGS = ("kestrel-annual-review", "ostend-investor-portal")
CORPORATE_PLAIN_SLUG = "northline-self-care"
REAL_ESTATE_SLUG = "cliffside-residences"
SAAS_SLUG = "vantage-onboarding"

TABLES = (
    "accounts", "sessions", "expertises", "tags", "case_studies",
    "case_study_tags", "covers", "feature_slots", "shelf", "briefs", "page_views",
)
BLOCK_KINDS = ("paragraph", "heading", "image", "image_pair", "quote", "facts")
PALETTES = ("mono", "warm", "cool")
BUDGETS = ("under_25k", "25k_to_75k", "75k_to_150k", "over_150k")
COVER_KEY_PREFIX = "covers/"
COVER_KEY_TEMPLATE = "covers/{case_id}/{digest}.{ext}"

MSG_NEED_EXPERTISE = "Choose an expertise before publishing."
MSG_NEED_TAG = "Add at least one tag before publishing."
MSG_NEED_COVER = "Add a cover before publishing."
MSG_CONFLICT = "This changed somewhere else while you were working."
MSG_SHELF_STALE = "The order changed. Yours was not saved."
MSG_SLUG_TAKEN = "That address is already used by another case study."
MSG_SIGN_IN_FAILED = "That did not match. Check both fields and try again."
MSG_LOCKED_PREFIX = "Too many attempts."
MSG_NAME = "Tell us what to call you."
MSG_PHONE = "That number looks incomplete."
MSG_EMAIL = "That address will not reach you."
MSG_COMMENT = "A few more words, please."
MSG_EXPERTISE_CHOICE = "Choose one of the listed expertises."
MSG_BUDGET_CHOICE = "Choose one of the listed budgets."
ERROR_CODES = (
    "bad_request", "unauthenticated", "forbidden", "not_found", "gone",
    "conflict", "unprocessable", "rate_limited", "locked",
)

PUBLIC_TITLES = (
    ("/", "Digital Product Design & Development Agency | Northform"),
    ("/work", "Work | Northform"),
    ("/company", "Company | Northform"),
    ("/contact", "Northform's Contact Details | Northform"),
    ("/privacy-policy", "Privacy Policy | Northform"),
    ("/work/kestrel-annual-review", "Kestrel Annual Review | Northform"),
    ("/expertise/corporate", "Corporate | Northform"),
)

STUDIO_GET_ENDPOINTS = (
    "/studio/dashboard", "/studio/work", "/studio/slots", "/studio/briefs",
    "/studio/page-views",
)
OWNER_ONLY_GET_ENDPOINTS = ("/studio/slots", "/studio/briefs", "/studio/page-views")

TYPE_FAMILY = "Inter Tight"
TYPE_WEIGHTS = ("400", "500")
TYPE_SIZES_PX = (180.0, 90.0, 38.0, 22.0, 16.0, 14.0, 12.0, 10.0)
DISPLAY_SIZE_PX = 180.0
TEXT_STYLE_SCRIPT = (
    "els => els.filter(e => e.offsetParent !== null && e.children.length === 0 "
    "&& e.innerText && e.innerText.trim()).map(e => { const s = getComputedStyle(e); "
    "return [s.fontFamily, s.fontWeight, s.fontSize]; })"
)

SECURITY_HEADERS = ("x-content-type-options", "referrer-policy",
                    "content-security-policy")

FEWER_LINKS = "Fewer links, please."
FALLBACK_FAMILY = "Helvetica Neue"
SEEDED_TAGS = {
    "cliffside-residences": ("promo-website", "real-estate"),
    "kestrel-annual-review": ("corporate-website", "banking"),
    "vantage-onboarding": ("saas", "self-service"),
    "meridian-duty-free": ("online-store", "branding"),
    "harbour-quarter": ("real-estate", "3d-visualisation"),
    "ostend-loyalty-store": ("online-store",),
    "ostend-investor-portal": ("customer-portal", "banking"),
    "pinemark-trading-desk": ("trading-platform", "saas"),
    "halden-home-store": ("online-store",),
    "northline-self-care": ("self-service", "customer-portal"),
    "vantage-pitch-site": ("promo-website",),
    "pinemark-mobile-app": ("saas",),
}
RECENT_KINDS = ("case_study", "brief")
SEEDED_ROWS = (
    ("cliffside-residences", "Cliffside Residences", "Halden", "2024", "real-estate", "published"),
    ("kestrel-annual-review", "Kestrel Annual Review", "Kestrel Bank", "2024", "corporate", "published"),
    ("vantage-onboarding", "Vantage Onboarding", "Vantage", "2025", "startups", "published"),
    ("meridian-duty-free", "Meridian Duty Free", "Meridian Air", "2024", "ecommerce", "published"),
    ("harbour-quarter", "Harbour Quarter", "Northline", "2023", "real-estate", "published"),
    ("ostend-loyalty-store", "Ostend Loyalty Store", "Ostend Credit", "2021", "ecommerce", "withdrawn"),
    ("ostend-investor-portal", "Ostend Investor Portal", "Ostend Credit", "2022", "corporate", "published"),
    ("pinemark-trading-desk", "Pinemark Trading Desk", "Pinemark", "2023", "startups", "published"),
    ("halden-home-store", "Halden Home Store", "Halden", "2022", "ecommerce", "published"),
    ("northline-self-care", "Northline Self Care", "Northline", "2021", "corporate", "published"),
    ("vantage-pitch-site", "Vantage Pitch Site", "Vantage", "2025", "startups", "published"),
    ("pinemark-mobile-app", "Pinemark Mobile App", "Pinemark", "2025", "startups", "draft"),
)
TAG_NAMES = (
    "Promo Website", "Corporate Website", "Online Store", "Self-Service", "SaaS",
    "Banking", "Customer Portal", "Trading Platform", "Branding",
    "3D & Visualisation", "Real Estate",
)
PINNED_COLUMNS = (
    ("sessions", ("id", "account_id", "token_hash", "user_agent_summary", "created_at",
                  "last_seen_at", "expires_at", "revoked_at")),
    ("expertises", ("id", "slug", "name", "sentence", "position")),
    ("tags", ("id", "slug", "name")),
    ("case_study_tags", ("id", "case_study_id", "tag_id")),
    ("covers", ("id", "case_study_id", "object_key", "content_type", "byte_size", "sha256",
                "width", "height", "alt_text", "created_at")),
    ("feature_slots", ("id", "expertise_id", "position", "case_study_id", "version")),
    ("shelf", ("id", "version")),
    ("briefs", ("id", "name", "company", "phone", "email", "comment", "expertise", "budget",
                "state", "source_path", "received_at")),
    ("accounts", ("id", "email", "password_hash", "display_name", "role",
                  "failed_attempts", "locked_until", "created_at")),
)
SEEDED_SLOTS = (
    ("real-estate", 0, ("cliffside-residences",)),
    ("real-estate", 1, ("harbour-quarter", "aster-row-residences")),
    ("corporate", 0, ("kestrel-annual-review",)),
    ("corporate", 1, ("ostend-investor-portal",)),
    ("startups", 0, ("vantage-onboarding",)),
    ("startups", 1, ("pinemark-trading-desk",)),
    ("ecommerce", 0, ("meridian-duty-free",)),
    ("ecommerce", 1, ("halden-home-store",)),
)
SEEDED_BRIEFS = (
    ("Tomas Berg", "tomas.berg@example.com", "Vantage", "startups", "25k_to_75k",
     "We need an onboarding flow for a savings app."),
    ("Lea Park", "lea.park@example.com", "Pinemark", "ecommerce", "under_25k",
     "Could you quote for a small online store refresh?"),
)
INES_MARKUP = "<b>Launch before March</b>"
SESSION_FIELDS = ("id", "user_agent_summary", "created_at", "last_seen_at", "current")
RECENT_FIELDS = ("kind", "id", "title", "changed_at")
LONG_DASHES = ("\u2013", "\u2014")
NOTIFY_PROBE = (
    "window.__notifyAsked = false; if (window.Notification) { "
    "window.Notification.requestPermission = function () { "
    "window.__notifyAsked = true; return Promise.resolve('denied'); }; }"
)

PNG_BYTES = bytes.fromhex(
    "89504e470d0a1a0a0000000d494844520000000100000001080600000"
    "01f15c4890000000a49444154789c6360000002000100ffff03000006"
    "0005570bf7050000000049454e44ae426082")

DENIED = (401, 403)
REFUSED_CLIENT = (400, 401, 403, 404, 409, 410, 412, 422, 423, 428, 429)


def settle() -> None:
    time.sleep(SETTLE_SECONDS)


def wait_past_form_floor() -> None:
    settle()
    settle()


def unique_token() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{unique_token()}@example.com"


def probe_slug(stem: str) -> str:
    return f"{stem}-{unique_token()}"


def probe_bytes() -> bytes:
    return PNG_BYTES + unique_token().encode("ascii")


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def describe(response) -> str:
    body = response.text[:400]
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code}; body: {body}")


def poll_until(predicate, deadline_seconds: float = POLL_DEADLINE_SECONDS):
    deadline = time.monotonic() + deadline_seconds
    last = predicate()
    while not last and time.monotonic() < deadline:
        settle()
        last = predicate()
    return last


def dig(payload, key):
    if isinstance(payload, dict):
        if key in payload:
            return payload[key]
        for value in payload.values():
            found = dig(value, key)
            if found is not None:
                return found
    elif isinstance(payload, list):
        for value in payload:
            found = dig(value, key)
            if found is not None:
                return found
    return None


def error_code(response):
    try:
        body = response.json()
    except ValueError as exc:
        raise AssertionError(
            "a refusal must answer with a JSON error body: " + describe(response)) from exc
    return dig(body, "code")


def error_text(response) -> str:
    return response.text


def slugs_of(payload) -> list:
    return [str(row.get("slug")) for row in _shapes.items(payload)]


def ids_of(payload) -> list:
    return [row.get("id") for row in _shapes.items(payload)]


def moved_before(order: list, moving, anchor) -> list:
    moving_raw = next(i for i in order if str(i) == str(moving))
    rest = [i for i in order if str(i) != str(moving)]
    at = next(n for n, i in enumerate(rest) if str(i) == str(anchor))
    return rest[:at] + [moving_raw] + rest[at:]


def json_of(response):
    assert response.status_code < 400, "expected a successful call: " + describe(response)
    return response.json()


def new_case_payload(stem: str = "probe-case", **extra) -> dict:
    slug = probe_slug(stem)
    body = {
        "title": f"Probe Case {slug[-12:]}",
        "slug": slug,
        "client": "Halden",
        "year": 2024,
        "summary": "A probe case study written for this run.",
        "cover_seed": 4242,
        "cover_palette": "warm",
        "blocks": [{"kind": "paragraph", "text": "A probe paragraph."}],
    }
    body.update(extra)
    return body


def create_case(client, **extra) -> dict:
    body = new_case_payload(**extra)
    response = client.post("/studio/work", json=body)
    assert response.status_code in (200, 201), (
        "creating a case study in the studio should succeed: " + describe(response))
    created = response.json()
    created.setdefault("slug", body["slug"])
    return created


def read_case(client, case_id) -> dict:
    response = client.get(f"/studio/work/{case_id}")
    assert response.status_code == 200, (
        "reading a case study in the studio should succeed: " + describe(response))
    return response.json()


def version_of(client, case_id):
    return dig(read_case(client, case_id), "version")


def cover_request(client, case_id, alt_text: str):
    return client.post(f"/studio/work/{case_id}/cover",
                       json={"generate": True, "alt_text": alt_text,
                             "version": version_of(client, case_id)})


def generate_cover(client, case_id, alt_text: str = "A generated probe cover."):
    response = cover_request(client, case_id, alt_text)
    assert response.status_code in (200, 201), (
        "generating a cover should succeed: " + describe(response))
    return response.json()


def cover_id_of(payload):
    cover = dig(payload, "cover")
    if isinstance(cover, dict):
        return cover.get("id")
    return dig(payload, "id") if cover is None else cover


def publish(client, case_id):
    return client.post(f"/studio/work/{case_id}/publish",
                       json={"version": version_of(client, case_id)})


def unpublish(client, case_id):
    return client.request("DELETE", f"/studio/work/{case_id}/publish",
                          json={"version": version_of(client, case_id)})


def create_published_case(client, expertise: str = "corporate",
                          tags=("banking",), **extra) -> dict:
    created = create_case(client, expertise=expertise, tags=list(tags), **extra)
    case_id = created["id"]
    generate_cover(client, case_id)
    response = publish(client, case_id)
    assert response.status_code in (200, 201), (
        "publishing a complete case study as the owner should succeed: "
        + describe(response))
    return read_case(client, case_id)


def studio_slots(client) -> list:
    response = client.get("/studio/slots")
    assert response.status_code == 200, "the owner reads the slots: " + describe(response)
    return _shapes.items(response.json())


def slot_for(client, expertise: str, position: int) -> dict:
    for slot in studio_slots(client):
        if str(slot.get("expertise")) == expertise and int(slot.get("position")) == position:
            return slot
    raise AssertionError(f"no feature slot for {expertise} at position {position}")


def shelf_state(client) -> tuple:
    payload = json_of(client.get("/studio/shelf"))
    return dig(payload, "version"), ids_of(dig(payload, "work"))


def put_shelf(client, order, version):
    body = {"order": order}
    if version is not None:
        body["version"] = version
    return client.put("/studio/shelf", json=body)


def put_slot(client, slot_id, case_id, version):
    return client.put(f"/studio/slots/{slot_id}",
                      json={"case_study_id": case_id, "version": version})


def brief_token(client) -> str:
    response = client.get("/briefs/token")
    assert response.status_code == 200, "the brief form token is public: " + describe(response)
    token = dig(response.json(), "form_token")
    assert token, "the token response carries a form_token: " + describe(response)
    return token


def brief_payload(token: str, **extra) -> dict:
    body = {
        "name": "Probe Sender",
        "company": "Probe Company",
        "phone": "+4712345678",
        "email": probe_email(),
        "comment": "We would like a new site for our apartments.",
        "expertise": "real-estate",
        "budget": "25k_to_75k",
        "source_path": "/contact",
        "form_token": token,
        "website": "",
    }
    body.update(extra)
    return body


def send_brief(client, headers=None, **extra):
    token = brief_token(client)
    wait_past_form_floor()
    body = brief_payload(token, **extra)
    response = client.post("/briefs", json=body, headers=headers or {})
    return body, response


def run_together(calls):
    barrier = threading.Barrier(len(calls))
    results = [None] * len(calls)

    def worker(index, call):
        barrier.wait()
        results[index] = call()

    threads = [threading.Thread(target=worker, args=(i, c)) for i, c in enumerate(calls)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results


def signup(email: str, password: str = APP_PASSWORD, **extra):
    body = {"email": email, "password": password}
    body.update(extra)
    return httpx.post(f"{appclient.api_base()}/auth/signup", json=body,
                      timeout=appclient.TIMEOUT)


def raw_login(email: str, password: str):
    return httpx.post(f"{appclient.api_base()}/auth/login",
                      json={"email": email, "password": password},
                      timeout=appclient.TIMEOUT)


def raw_call(method: str, url: str, auth: str, body: dict):
    return httpx.request(method, url, json=body, headers={"Authorization": auth},
                         timeout=appclient.TIMEOUT)


def bearer_client(token: str):
    return appclient.client(token)


def storage_credentials() -> tuple:
    values = (os.environ.get("STORAGE_SECRET_KEY", ""),
              os.environ.get("STORAGE_ACCESS_KEY", ""))
    return tuple(v for v in values if v)


def script_sources(html: str) -> list:
    return re.findall(r"<script[^>]+src=[\"']([^\"']+)[\"']", html)


@pytest.fixture(scope="session")
def app_base() -> str:
    return appclient.app_url()


@pytest.fixture()
def anon():
    with appclient.client() as c:
        yield c


@pytest.fixture()
def owner():
    with appclient.client(appclient.login(OWNER_EMAIL, APP_PASSWORD)) as c:
        yield c


@pytest.fixture()
def editor():
    with appclient.client(appclient.login(EDITOR_EMAIL, APP_PASSWORD)) as c:
        yield c


@pytest.fixture()
def visitor():
    with appclient.client(appclient.login(VISITOR_EMAIL, APP_PASSWORD)) as c:
        yield c


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def site():
    with httpx.Client(base_url=appclient.app_url(), timeout=30.0,
                      follow_redirects=True) as c:
        yield c


@pytest.fixture()
def page():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context()
        tab = context.new_page()
        yield tab
        context.close()
        browser.close()
