from __future__ import annotations

import hashlib
import html as html_lib
import json
import os
import re
import time
from urllib.parse import urlsplit

import httpx
import pytest
from _shapes import items
from appclient import api_base, app_url, client, login, seeded_password
from capabilities import make_backend

COMMERCIAL_EMAIL = "commercial@example.com"
EDITOR_EMAIL = "editor@example.com"
SUSPENDED_EMAIL = "former@example.com"
SEEDED_PASSWORD_DEFAULT = "deku-demo-pw-2026"
SENDER_ADDRESS = "hello@verdea-outdoor.com"

LOCALES = ("pt", "en", "es", "fr")
LOCALE_TOTALS = {"pt": 20, "en": 20, "es": 19, "fr": 18}
ENGLISH_COLLECTION_COUNTS = {"urban": 6, "nature": 4, "repolymer": 3, "golf": 4, "details": 3}
ARTICLE_TOTALS = {"pt": 19, "en": 19, "es": 19, "fr": 18}

TEE_SIGN_ID = "vd-tee-sign-heritage"
TEE_SIGN_SLUG = "tee-sign-heritage"
TEE_SIGN_TITLE = "Tee Sign Heritage"
TEE_SIGN_ROUTE = "/en/products/golf/tee-sign-heritage"
TEE_SIGN_PT_SLUG = "placa-de-saida-heritage"
TEE_SIGN_ES_SLUG = "senal-de-salida-heritage"
TEE_SIGN_ES_TITLE = "Señal de Salida Heritage"
TEE_SIGN_FR_SLUG = "panneau-de-depart-heritage"
PLAZA_BENCH_ID = "vd-plaza-bench-long"
PLAZA_BENCH_SLUG = "plaza-bench-long"
PLAZA_BENCH_TITLE = "Plaza Bench Long"
PLAZA_BENCH_PT_SLUG = "banco-praca-longo"
PLAZA_BENCH_PT_TITLE = "Banco Praça Longo"
FRAME_BOLLARD_ID = "vd-frame-bollard"
FRAME_BOLLARD_SLUG = "frame-bollard"
ROOM_SIGN_ID = "vd-slim-room-sign"
ROOM_SIGN_SLUG = "slim-room-sign"
ROOM_SIGN_PT_SLUG = "placa-de-sala-slim"
ROOM_SIGN_PT_TITLE = "Placa de Sala Slim"
GOLF_BAG_STAND_ID = "vd-golf-bag-stand"
TERRA_PLANTER_ID = "vd-terra-planter-box"
LINE_DOOR_PLATE_SLUG = "line-door-plate"
REUSE_BIN_SLUG = "reuse-litter-bin-duo"
WITHDRAWN_ID = "vd-withdrawn-sample"
WITHDRAWN_SLUG = "withdrawn-sample"
UNRESOLVED_COLLECTION = "No longer in the catalogue"

TEE_SIGN_SIZES = ["S", "M"]
TEE_SIGN_STRUCTURES = ["Metallised and painted steel", "Galvanised steel"]
TEE_SIGN_COLORS = [
    "Pure white RAL9010", "Anthracite grey RAL7016", "Umbra grey RAL7022",
    "Signal yellow RAL1003", "Salmon pink RAL3022", "Pastel blue RAL5024",
    "Pastel green RAL6019", "Personalised",
]
TEE_SIGN_DISPLAYS = ["HPL +", "HPL Print"]
TEE_SIGN_HPL_COLORS = [
    "Sienna brown", "Mid beige", "Spring green", "Turf green", "Dark green",
    "Dark brown", "Dark blue", "Black",
]
TEE_SIGN_DIMENSIONS = "190 x 100 x 1700 mm"
TEE_SIGN_MATERIALS = "Reinforced, brown recycled plastic; HPL+ or HPL Print."
TEE_SIGN_ADVANTAGES = ("No maintenance required; Easy component replacement; Customizable; "
                       "High resistance to shock, weather, and vandalism.")
TEE_SIGN_REFERENCES = ["HPL+ - GTEETTM010", "HPL Print - GTEETTM011"]
TEE_SIGN_DESCRIPTION_START = "Where tradition meets function"
SPEC_LABEL_ORDER = [
    "Dimensions", "Structure Options", "Structure Colors", "Display Options",
    "HPL+ Colors", "Materials", "Specifications", "Advantages", "References",
]
PLAZA_BENCH_SIZES = ["1400", "1900", "2000"]
PLAZA_BENCH_2000_DIMENSIONS = "2000 x 554 x 465 mm"
PLAZA_BENCH_STRUCTURES = ["Galvanised steel", "Metallised and painted steel"]
PLAZA_BENCH_COLORS = ["Anthracite grey RAL7016", "Umbra grey RAL7022", "Pure white RAL9010", "Personalised"]
PLAZA_BENCH_REFERENCE_CODE = "UBSCFE0000881"
AUTHORED_SIZES = {
    "frame-bollard": ["s", "m"],
    "reuse-litter-bin-duo": ["All", "Bottle", "Pet"],
    "classic-ball-washer": ["R900", "Q600"],
    "course-distance-marker": ["110", "1500"],
    "boardwalk-module": ["25", "50", "100"],
    "plaza-bike-rack-arc": ["3", "4"],
}
SINGLE_COLOR = "Anthracite grey RAL7016"

TEE_SIGN_DOCUMENT = "Tee Sign Heritage technical files"
TEE_SIGN_PDF = "tee-sign-heritage-technical-files-en.pdf"
URBAN_DOCUMENT = "Urban Catalogue"
URBAN_PDF = "urban-catalogue-en.pdf"
CATALOGUE_DOCUMENTS = {"urban": "Urban Catalogue", "nature": "Nature Catalogue",
                       "repolymer": "Repolymer Catalogue", "golf": "Golf Catalogue"}
GRANT_REDEMPTIONS = 5

REFERENCE_RE = re.compile(r"^VQ-[23456789ABCDEFGHJKMNPQRSTUVWXYZ]{6}$")
NOT_CHOSEN = "(not chosen)"

PRIVACY_SENTENCE = "I have read and understood the Privacy Policy."
NEWSLETTER_SENTENCE = "By submitting your email you agree to our Privacy Policy."

QUOTATION_SUBJECT_PREFIX = "Quotation request received: "
CONTACT_SUBJECT = "Verdea enquiry received"
GRANT_SUBJECT_PREFIX = "Your Verdea download: "
NEWSLETTER_SUBJECT = "Confirm your Verdea newsletter subscription"
STAFF_QUOTATION_PREFIX = "New quotation: "
STAFF_CONTACT_SUBJECT = "New enquiry received"
STAFF_FILE_PREFIX = "New file request: "

ROLE_VALUE = "Municipal buyer"
INDUSTRY_VALUE = "Public administration"
LEAD_LIMIT_PER_HOUR = 5
SIGNUP_LIMIT_PER_DAY = 3

CONSENT_COOKIE = "verdea_consent"
LOCALE_COOKIE = "verdea_locale"

JOB_TITLES = {"CNC Operator", "Serralheiro Civil", "Project Manager", "Installation Technician"}
CATEGORY_COUNTS = [
    ("press-releases", 1), ("sustainability", 2), ("case-studies", 13),
    ("products", 2), ("educational", 1), ("institutional", 0),
]
RIDGE_SLUG = "ridge-viewpoint-boardwalk"
RECENT_SLUGS = ["ridge-viewpoint-boardwalk", "recycled-plastic-explained",
                "hpl-in-the-open-air", "verdea-opens-spanish-establishment"]
EDUCATIONAL_SLUG = "why-galvanised-steel-lasts"

FORBIDDEN_IN_BUNDLES = ("deku-local-dev", "postgresql://", "deku_app", "deku-demo-pw-2026")

DENIED = (401, 403)
INVALID = (400, 422)
ACCEPTED = 202
INBOX_API = "api/v1"

SETTLE_SECONDS = 2.0
POLL_BUDGET_SECONDS = 90.0
SEVEN_DAYS_SECONDS = 7 * 24 * 3600
FOURTEEN_DAYS_SECONDS = 14 * 24 * 3600


def settle() -> None:
    """The only sanctioned sleep in this suite."""
    time.sleep(SETTLE_SECONDS)


def poll_until(check, budget: float = POLL_BUDGET_SECONDS):
    """Bounded poll to a monotonic deadline. Returns the first truthy result."""
    stop = time.monotonic() + budget
    last = check()
    while not last and time.monotonic() < stop:
        settle()
        last = check()
    return last


def probe_suffix() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{probe_suffix()}@example.com"


def idem_key() -> str:
    return f"idem-{os.urandom(12).hex()}"


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def api(path: str) -> str:
    return f"{api_base()}{path}"


def page(path: str) -> str:
    return f"{app_url()}{path}"


def get(path: str, **kwargs) -> httpx.Response:
    return httpx.get(page(path), timeout=60.0, follow_redirects=False, **kwargs)


def api_get(path: str, **kwargs) -> httpx.Response:
    return httpx.get(api(path), timeout=60.0, follow_redirects=False, **kwargs)


def api_post(path: str, body, **kwargs) -> httpx.Response:
    return httpx.post(api(path), json=body, timeout=60.0, follow_redirects=False, **kwargs)


def location_path(response: httpx.Response) -> str:
    target = response.headers.get("location", "")
    parts = urlsplit(target)
    return parts.path + (f"?{parts.query}" if parts.query else "")


def visible_text(markup: str) -> str:
    without = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", markup)
    without = re.sub(r"(?s)<[^>]+>", " ", without)
    return re.sub(r"\s+", " ", html_lib.unescape(without)).strip()


def link_tags(markup: str) -> list[dict]:
    found = []
    for tag in re.findall(r"(?is)<link\b[^>]*>", markup):
        attrs = {k.lower(): v for k, _, v in re.findall(r"""([\w:-]+)\s*=\s*(["'])(.*?)\2""", tag)}
        found.append(attrs)
    return found


def error_code(response: httpx.Response) -> str:
    if "json" not in response.headers.get("content-type", "").lower():
        return ""
    body = response.json()
    error = body.get("error") if isinstance(body, dict) else None
    return str(error.get("code", "")) if isinstance(error, dict) else ""


def error_fields(response: httpx.Response) -> dict:
    if "json" not in response.headers.get("content-type", "").lower():
        return {}
    body = response.json()
    error = body.get("error") if isinstance(body, dict) else None
    fields = error.get("fields") if isinstance(error, dict) else None
    return fields if isinstance(fields, dict) else {}


def products(locale: str, **facets) -> list[dict]:
    params = [("locale", locale)]
    for key, values in facets.items():
        for value in values:
            params.append((key, value))
    response = api_get("/products", params=params)
    assert response.status_code == 200, (
        f"GET /api/products {params} returned {response.status_code}: {response.text[:300]}"
    )
    return items(response.json())


def product_ids(locale: str, **facets) -> set[str]:
    return {str(p.get("id")) for p in products(locale, **facets)}


def product_detail(slug: str, locale: str = "en") -> dict:
    response = api_get(f"/products/{slug}", params={"locale": locale})
    assert response.status_code == 200, (
        f"GET /api/products/{slug}?locale={locale} returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    return response.json()


def names(values) -> list[str]:
    out = []
    for value in values or []:
        out.append(str(value.get("name")) if isinstance(value, dict) else str(value))
    return out


def labels(values) -> list[str]:
    out = []
    for value in values or []:
        out.append(str(value.get("label")) if isinstance(value, dict) else str(value))
    return out


@pytest.fixture(scope="session")
def form_token() -> str:
    response = api_get("/form-token")
    assert response.status_code == 200, (
        f"GET /api/form-token returned {response.status_code}: {response.text[:300]}"
    )
    token = response.json().get("formToken")
    assert token, f"GET /api/form-token carried no formToken: {response.text[:300]}"
    settle()
    return str(token)


def consent(sentence: str = PRIVACY_SENTENCE, privacy: bool = True) -> dict:
    return {"privacy": privacy, "textHash": sha256_hex(sentence)}


def meta(token, route: str = "/en/wishlist", website: str = "") -> dict:
    body = {"route": route, "website": website}
    if token is not None:
        body["formToken"] = token
    return body


def tee_sign_entry() -> dict:
    return {"entryId": f"entry-{probe_suffix()}", "productId": TEE_SIGN_ID, "slug": TEE_SIGN_SLUG,
            "options": {"size": "M", "structure": "Galvanised steel",
                        "color": "Anthracite grey RAL7016", "display": "HPL +",
                        "hplColor": "Dark green"}}


def plaza_bench_entry() -> dict:
    return {"entryId": f"entry-{probe_suffix()}", "productId": PLAZA_BENCH_ID,
            "slug": PLAZA_BENCH_SLUG, "options": {"size": "2000"}}


def entry(product_id: str, slug: str, **options) -> dict:
    return {"entryId": f"entry-{probe_suffix()}", "productId": product_id, "slug": slug,
            "options": options}


def quotation_body(email: str, token, entries=None, locale: str = "en", key=None,
                   **contact_over) -> dict:
    contact = {"firstName": "Ana", "lastName": "Silva", "email": email,
               "role": ROLE_VALUE, "industry": INDUSTRY_VALUE,
               "country": "Portugal", "city": "Agueda", "taxId": "0012 345"}
    contact.update(contact_over)
    return {"locale": locale, "idempotencyKey": key or idem_key(), "contact": contact,
            "wantsTechnicalFiles": True, "consent": consent(),
            "entries": entries if entries is not None else [tee_sign_entry(), plaza_bench_entry()],
            "meta": meta(token, f"/{locale}/wishlist")}


def contact_body(email: str, token, message: str = "Please call about benches.",
                 key=None, website: str = "") -> dict:
    return {"locale": "en", "idempotencyKey": key or idem_key(),
            "contact": {"firstName": "Rita", "lastName": "Costa", "email": email,
                        "country": "Spain"},
            "message": message, "consent": consent(),
            "meta": meta(token, "/en/about", website)}


def file_body(email: str, token, document=None, key=None) -> dict:
    return {"locale": "en", "idempotencyKey": key or idem_key(),
            "contact": {"firstName": "Joao", "lastName": "Reis", "email": email},
            "document": document or {"scope": "product", "productId": TEE_SIGN_ID},
            "consent": consent(), "meta": meta(token, TEE_SIGN_ROUTE)}


def subscriber_body(email: str, token, locale: str = "en") -> dict:
    return {"email": email, "locale": locale, "consent": consent(NEWSLETTER_SENTENCE),
            "meta": meta(token, f"/{locale}/journal")}


def submit_quotation(email: str, token, **kwargs) -> httpx.Response:
    return api_post("/lead/quotation", quotation_body(email, token, **kwargs))


def submit_contact(email: str, token, **kwargs) -> httpx.Response:
    return api_post("/lead/contact", contact_body(email, token, **kwargs))


def submit_file_request(email: str, token, **kwargs) -> httpx.Response:
    return api_post("/lead/file-request", file_body(email, token, **kwargs))


def sign_up(email: str, token, locale: str = "en") -> httpx.Response:
    return api_post("/subscriber", subscriber_body(email, token, locale))


def absolute(url: str) -> str:
    return url if url.startswith("http") else page(url)


def token_for(email: str) -> str:
    return login(email, seeded_password("SEED_STAFF_PASSWORD", SEEDED_PASSWORD_DEFAULT))


@pytest.fixture
def commercial_client():
    with client(token_for(COMMERCIAL_EMAIL)) as c:
        yield c


@pytest.fixture
def editor_client():
    with client(token_for(EDITOR_EMAIL)) as c:
        yield c


class RecordStore:
    """Domain queries for this task, composed from the generic primitives."""

    def __init__(self, backend) -> None:
        self._b = backend

    def leads(self, email: str) -> list[dict]:
        return self._b.rows("lead", limit=50, email=email)

    def lead(self, email: str) -> dict | None:
        found = self.leads(email)
        return found[0] if found else None

    def lead_by_id(self, lead_id) -> dict | None:
        return self._b.one("lead", id=lead_id)

    def quotation(self, lead_id) -> dict | None:
        return self._b.one("quotation", lead_id=lead_id)

    def lines(self, quotation_id) -> list[dict]:
        rows = self._b.rows("quotation_item", limit=200, quotation_id=quotation_id)
        return sorted(rows, key=lambda r: int(r["position"]))

    def file_requests(self, lead_id) -> list[dict]:
        return self._b.rows("file_request", limit=20, lead_id=lead_id)

    def subscriber(self, email: str) -> dict | None:
        return self._b.one("subscriber", email=email)

    def count_subscribers(self, email: str) -> int:
        return self._b.count("subscriber", email=email)

    def audit_count(self, action: str, subject_id) -> int:
        return self._b.count("audit_event", action=action, subject_id=str(subject_id))

    def staff(self, email: str) -> dict | None:
        return self._b.one("staff_account", email=email)

    def count_staff(self, email: str) -> int:
        return self._b.count("staff_account", email=email)

    def receipts(self, visitor_key: str) -> list[dict]:
        return self._b.rows("consent_receipt", limit=20, visitor_key=visitor_key)


@pytest.fixture(scope="session")
def db() -> RecordStore:
    return RecordStore(make_backend())


def as_json(value):
    return json.loads(value) if isinstance(value, str) else value


def blank(value) -> bool:
    return value is None or str(value) == ""


def inbox_base() -> str:
    return os.environ["EMAIL_INBOX_API_URL"].rstrip("/")


def inbox_messages() -> list[dict]:
    response = httpx.get(f"{inbox_base()}/{INBOX_API}/messages", params={"limit": 1000},
                         timeout=60.0)
    assert response.status_code == 200, (
        f"the mail inbox listing returned {response.status_code}: {response.text[:300]}"
    )
    return response.json().get("messages", []) or []


def recipients(message: dict, key: str = "To") -> list[str]:
    return [str(a.get("Address", "")).lower() for a in (message.get(key) or [])]


def mails_to(address: str, subject_contains: str = "") -> list[dict]:
    needle = subject_contains.lower()
    return [m for m in inbox_messages()
            if address.lower() in recipients(m) and needle in str(m.get("Subject", "")).lower()]


def mail_detail(message_id: str) -> dict:
    response = httpx.get(f"{inbox_base()}/{INBOX_API}/message/{message_id}", timeout=60.0)
    assert response.status_code == 200, (
        f"the mail detail for {message_id} returned {response.status_code}"
    )
    return response.json()


def mail_text(message_id: str) -> str:
    detail = mail_detail(message_id)
    return f"{detail.get('Text', '')}\n{html_lib.unescape(detail.get('HTML', '') or '')}"


def mail_headers(message_id: str) -> dict:
    response = httpx.get(f"{inbox_base()}/{INBOX_API}/message/{message_id}/headers", timeout=60.0)
    assert response.status_code == 200, (
        f"the mail headers for {message_id} returned {response.status_code}"
    )
    return {k.lower(): v for k, v in response.json().items()}


def wait_for_mail(address: str, subject_contains: str = "", budget: float = POLL_BUDGET_SECONDS):
    found = poll_until(lambda: mails_to(address, subject_contains), budget)
    assert found, (
        f"no message to {address} with a subject containing {subject_contains!r} arrived "
        f"within {budget} seconds"
    )
    return found


def staff_mail_mentioning(subject_contains: str, needle: str):
    def look():
        for message in mails_to(COMMERCIAL_EMAIL, subject_contains):
            text = mail_text(message["ID"])
            if needle in text or needle in str(message.get("Subject", "")):
                return (message, text)
        return None
    found = poll_until(look)
    assert found, (
        f"no message to {COMMERCIAL_EMAIL} with {subject_contains!r} mentions {needle!r}"
    )
    return found


def wait_for_status(db: RecordStore, email: str, status: str) -> dict:
    row = poll_until(lambda: (lambda r: r if r and str(r.get("status")) == status else None)(db.lead(email)))
    assert row, (
        f"the lead for {email} never reached status {status!r}; last row: {db.lead(email)}"
    )
    return row
