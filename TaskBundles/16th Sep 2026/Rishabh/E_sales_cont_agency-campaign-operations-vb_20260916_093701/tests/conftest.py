from __future__ import annotations

import hashlib
import mimetypes
import os
import re
import time
import uuid

import httpx
import pytest
from playwright.sync_api import sync_playwright

import _shapes
import appclient
import capabilities

SETTLE_SECONDS = 2.0
POLL_DEADLINE_SECONDS = 30.0
RELEASE_DEADLINE_SECONDS = 240.0

APP_PASSWORD = "deku-demo-pw-2026"
ACCOUNT_DIRECTOR_EMAIL = "account_director@example.com"
ACCOUNT_DIRECTOR2_EMAIL = "account_director2@example.com"
PRODUCER_EMAIL = "producer@example.com"
PRODUCER2_EMAIL = "producer2@example.com"
CREATIVE_EMAIL = "creative@example.com"
CREATIVE2_EMAIL = "creative2@example.com"
LEGAL_EMAIL = "legal@example.com"
EDITOR_EMAIL = "editor@example.com"

HOSHINO = "hoshino-motors"
TSUBAME = "tsubame-automotive"
KAGEROU = "kagerou-beverages"
AOZORA = "aozora-airlines"
MINATO = "minato-rail"
CLIENTS_BY_READING = (AOZORA, KAGEROU, TSUBAME, HOSHINO, MINATO)
CLIENTS_BY_ENGLISH = (AOZORA, HOSHINO, KAGEROU, MINATO, TSUBAME)

WALLED_JOB_TITLE = "Hoshino EV Launch"
WALLED_CAMPAIGN_TITLE = "Midnight Charge"
RIVAL_JOB_TITLE = "Tsubame Rally Series"
SPLIT_JOB_TITLE = "Sky Tea Partnership"
SPLIT_SHARES = ((KAGEROU, 6000), (AOZORA, 4000))
APPORTIONMENT_WHOLE = 10000

HOSHINO_UNIT = "Hoshino Unit"
PLANNING_UNIT = "Planning"
WEEKLY_CAPACITY = 2400
COOLING_OFF_DAYS = 90

CURRENT_CARD = "RC-2026"
PREVIOUS_CARD = "RC-2025"
ART_DIRECTOR = "Art Director"
CREATIVE_DIRECTOR = "Creative Director"
EXAMPLE_MINUTES = 450
EXAMPLE_ART_DIRECTOR_RATE = 12000
EXAMPLE_COST = 90000
LEDGER_CURRENCY = "jpy"
FOREIGN_AMOUNT = 125000
FOREIGN_CURRENCY = "usd"
FX_RATE = "148.50"
FX_DATE = "2026-03-31"
CONVERTED_AMOUNT = 185625

CAPACITY_REFUSAL = "That person is fully committed in the weeks you selected."
SCHEDULE_REFUSAL = ("The campaign cannot be published yet: clearance for one market "
                    "expires before the scheduled date.")
NOT_FOUND_APOLOGY = "Sorry, nothing lives at that address."

REASON_CLEARANCE = "clearance"
REASON_PERMISSION = "case_study_permission"
REASON_CREDITS = "credits"
REASON_RIGHTS = "rights_expire_before_release"
REASON_EMBARGO = "embargo"

VERSION_KEY_TEMPLATE = "jobs/{job_id}/versions/{number}/{digest}{ext}"
HERO_KEY_TEMPLATE = "campaigns/{campaign_id}/{digest}{ext}"

INTERNAL = "internal"
CLIENT = "client"

NIGHT_SIGNAL = "night-signal"
NIGHT_SIGNAL_TITLE = "Night Signal"
NIGHT_SIGNAL_TITLE_JA = "夜の信号"
NIGHT_SIGNAL_FRAGMENT = "信号"
NIGHT_SIGNAL_READING_FRAGMENT = "しんごう"
NIGHT_SIGNAL_CLIENTS = ("Kagerou Beverages", "Aozora Airlines", "Minato Rail")
NIGHT_SIGNAL_PRIMARY = "Kagerou Beverages"
NIGHT_SIGNAL_ROLES = (
    "Chief Creative Officer",
    "Head of Innovation",
    "Senior Creative Director",
    "Creative Director",
    "Art Director",
    "Experience Planner",
    "Technical Director and Programmer",
    "Senior Copywriter",
    "Experience Planner",
    "Producer",
    "Account Director",
    "Editor",
)
JOINT_PRODUCERS = ("Yuto Baba", "Riko Nishi", "Sho Ota")
DEPARTED_PERSON = "Shun Kaneda"
QUIET_ENGINE = "quiet-engine"
QUIET_ENGINE_TITLE = "Quiet Engine"
WINTER_KITE = "winter-kite"
TIDE_CLOCK = "tide-clock"
SILENT_AURORA = "silent-aurora"
SILENT_AURORA_TITLE = "Silent Aurora"
SILENT_AURORA_TITLE_JA = "静かなオーロラ"
HARBOUR_LIGHTS = "harbour-lights"
BLUE_HOUR_RAIL = "blue-hour-rail"
OLDEST_SEEDED = "first-drive"
SEEDED_PUBLIC_COUNT = 30
PAGE_SIZE = 12
LISTED_YEARS = ("2026", "2025", "2024", "2023", "2022")
BEFORE_BUCKET = "before"
FIRST_UNLISTED_YEAR = 2022

LOTUS = "lotus-festival"
LOTUS_NAME = "Lotus Festival"
NORTH_STAR = "north-star-awards"
LOTUS_YEAR = 2025
LOTUS_ITEMISED = (("Grand Lotus", 1), ("Gold", 2), ("Silver", 2), ("Bronze", 2),
                  ("Jade Petal", 2))
LOTUS_HEADLINE = (("Gold", 3), ("Silver", 2), ("Bronze", 2), ("Jade Petal", 2))
LOTUS_TOTAL = 9
NIGHT_SIGNAL_LOTUS_RANKS = ("Grand Lotus", "Gold", "Silver")
SUPREME_RANK = "Grand Lotus"
TOP_RANK = "Gold"
BODY_SPECIFIC_RANK = "Jade Petal"
AWARD_ARTICLE = "lotus-festival-2025-results"

OFFICER_WITH_CONCURRENT = "Hiroshi Kudo"
OFFICER_TITLE = "Non-executive Director"
PARENT_GROUP = "Meido Group"
UNIT_COUNT = 10
UNIT_NAMES = ("Planning", "Media Experience Design", "Corporate Strategy", "Finance",
              "Executive Management", "Hoshino Unit", "Kagerou Studio", "Rupture Lab",
              "Integrated Business Leadership", "Minato Media Partners")
OFFICER_TITLES = (("Emi Hayashi", "Chief Operating Officer"), ("Ren Shibata", "Chief Creative Officer"))
KUDO_CONCURRENT = "Executive Officer, Meido Group"
DEDICATED_UNIT_COUNT = 2
OPENING_TRACKS = ("new_graduate", "internship")
COMPANY_UPDATED = "2026-04-01"
COMPANY_TELEPHONE = "+81-3-5555-0100"
FIRST_OFFICER = "Kaito Mizuno"
FIRST_OFFICER_TITLE = "President & CEO"
SEEDED_EMAILS = (ACCOUNT_DIRECTOR_EMAIL, ACCOUNT_DIRECTOR2_EMAIL, PRODUCER_EMAIL,
                 PRODUCER2_EMAIL, CREATIVE_EMAIL, CREATIVE2_EMAIL, LEGAL_EMAIL, EDITOR_EMAIL)
HOME_COPY = ("rupture is not destruction.", "RUPTURE IS CREATION.", "CREATE. INVENT. HAVE IDEAS.",
             "READY TO BREAK SOMETHING")
APPLY_PREFIX = "https://careers.example.org/"
INTERNSHIP_URL = "https://careers.example.org/kuromeido/internships"
KAGEROU_STUDIO = "Kagerou Studio"
RICE_FIELD_RADIO = "rice-field-radio"
SENIOR_CREATIVE_DIRECTOR = "Senior Creative Director"
ENTRY_FEE = 150000
NORTH_STAR_RANKS = ("Gold", "Silver", "Bronze", "Merit")
SUBMITTED = "submitted"
SHORTLISTED = "shortlisted"
CLOSED = "closed"
HOME_FACTS = ("EST. 2006", "TOKYO", "35.6581 N 139.7561 E", "We use creativity to move business",
              "We are the method company.", "1992")
COMPANY_POSTAL_CODE = "104-0061"
COMPANY_BUILDING = "Kaigan Tower 14F, 1-2-3 Kaigan, Chuo-ku, Tokyo"
OFFICER_ORDER = ("Kaito Mizuno", "Emi Hayashi", "Ren Shibata", "Hiroshi Kudo", "Laura Chen")
AUDITOR = "Masato Ide"
AUDITOR_TITLE = "Auditor"
AUDITOR_CONCURRENT = "Audit Partner, Meido Group"
GLOBAL_OFFICER = "Laura Chen"
GLOBAL_OFFICER_CONCURRENT = "Regional President, KURO Worldwide"
NEW_GRADUATE_URL = "https://careers.example.org/kuromeido/new-graduates"
CAREERS_VALUES = (("BE A PIRATE", "海賊であれ"),
                  ("CREATIVITY COMES FROM DIVERSITY", "多様性が創造性を生む"),
                  ("UNCOMMON HUMANITY", "並外れた人間らしさ"),
                  ("GOOD ENOUGH IS NOT ENOUGH", "十分では足りない"),
                  ("BE BRAVE", "勇敢であれ"))
OPENING_TITLES = ("Creative, new graduates 2027", "Summer internship 2027")
JAPANESE_FACE = "notosansjp"
HARBOUR_PERMISSION = "PERM-HARBOUR-LIGHTS"
HARBOUR_CREDIT_ROLE = "Producer"
HARBOUR_CREDIT_PERSON = "Kenji Mori"
NIGHT_SIGNAL_LEADS = (("Chief Creative Officer", "Ren Shibata"), ("Head of Innovation", "Takumi Aoki"))
NIGHT_SIGNAL_ACTIVE_CREDITED = 13
OWNED_ACCOUNTS = {
    ACCOUNT_DIRECTOR_EMAIL: (HOSHINO, KAGEROU),
    ACCOUNT_DIRECTOR2_EMAIL: (TSUBAME, AOZORA, MINATO),
}
BRIEF_CONVERTED = "converted"
JOB_OPEN = "open"
RETURNED_CAPACITY = 2400

DEFAULT_DESK = "desk@kuromeido.example.com"
NEW_BUSINESS_DESK = "newbusiness@kuromeido.example.com"
RECRUITMENT_DESK = "careers@kuromeido.example.com"
PRESS_DESK = "press@kuromeido.example.com"
DECOY_FIELD = "website"

STUDIO_READ_ROUTES = ("/jobs", "/people", "/reports/burn", "/page-views", "/briefs")
PUBLIC_PAGES = ("/", "/work/", "/company/", "/contact/")
IMAGE_PAGES = ("/", "/work/", "/work/night-signal/", "/company/")
CONTRAST_PAGES = ("/", "/work/", "/company/")
SECURITY_PAGES = ("/", "/work/", "/api/health")
CONTRAST_FLOOR = 4.5

PAGE_TEXT_SCRIPT = """
() => {
  const parts = [document.body.innerText || ''];
  for (const el of document.querySelectorAll('[aria-label]')) {
    parts.push(el.getAttribute('aria-label'));
  }
  return parts.join(' ');
}
"""

PNG_BYTES = bytes.fromhex(
    "89504e470d0a1a0a0000000d494844520000000100000001080600000"
    "01f15c4890000000a49444154789c6360000002000100ffff03000006"
    "0005570bf7050000000049454e44ae426082")

UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")

CONTRAST_SCRIPT = """
() => {
  const parse = (c) => {
    const m = c.match(/rgba?\\(([^)]+)\\)/);
    if (!m) return null;
    const p = m[1].split(',').map((x) => parseFloat(x));
    return {r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1};
  };
  const lum = (c) => {
    const ch = [c.r, c.g, c.b].map((v) => {
      const s = v / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2];
  };
  const background = (el) => {
    let node = el;
    while (node) {
      const c = parse(getComputedStyle(node).backgroundColor);
      if (c && c.a > 0.5) return c;
      node = node.parentElement;
    }
    return {r: 255, g: 255, b: 255, a: 1};
  };
  const ratios = [];
  for (const el of document.querySelectorAll('p')) {
    const text = (el.innerText || '').trim();
    const box = el.getBoundingClientRect();
    if (!text || box.width === 0 || box.height === 0) continue;
    const fg = parse(getComputedStyle(el).color);
    if (!fg) continue;
    const bg = background(el);
    const a = lum(fg);
    const b = lum(bg);
    ratios.push((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05));
  }
  return ratios;
}
"""


def settle() -> None:
    time.sleep(SETTLE_SECONDS)


def unique_token() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{unique_token()}@example.com"


def probe_bytes() -> bytes:
    return PNG_BYTES + unique_token().encode("ascii")


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def ext_for(content_type: str) -> str:
    return mimetypes.guess_extension(content_type) or ""


def version_key(job_id, number, payload: bytes, content_type: str = "image/png") -> str:
    return VERSION_KEY_TEMPLATE.format(job_id=job_id, number=number,
                                       digest=sha256_hex(payload),
                                       ext=ext_for(content_type))


def hero_key(campaign_id, payload: bytes, content_type: str = "image/png") -> str:
    return HERO_KEY_TEMPLATE.format(campaign_id=campaign_id,
                                    digest=sha256_hex(payload),
                                    ext=ext_for(content_type))


def describe(response) -> str:
    body = response.text[:400]
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code}; body: {body}")


def poll_until(predicate, deadline_seconds: float = POLL_DEADLINE_SECONDS):
    deadline = time.monotonic() + deadline_seconds
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle()
    return last


def ident(record) -> str:
    for key in ("id", "job_id", "campaign_id", "person_id"):
        if isinstance(record, dict) and record.get(key) is not None:
            return str(record[key])
    raise AssertionError(f"the created record carries no id field: {record}")


def absent_id_like(real) -> str:
    text = str(real)
    if UUID_RE.match(text):
        return str(uuid.uuid4())
    if text.isdigit():
        return str(int(text) + 7919 * 104729)
    return "".join("0" if ch.isalnum() else ch for ch in text[:-4]) + unique_token()[:4]


def ok(response, what: str):
    assert response.status_code in (200, 201), f"{what} should succeed: " + describe(response)
    return response.json() if response.content else {}


def refused(response, what: str) -> None:
    assert 400 <= response.status_code < 500, (
        f"{what} must be refused as a client error: " + describe(response))


def rows(payload) -> list:
    return _shapes.items(payload)


def flat(payload) -> str:
    return _shapes.flatten(payload)


def field(record, *names):
    for name in names:
        if isinstance(record, dict) and name in record:
            return record[name]
    return None


def client_for(email: str) -> httpx.Client:
    return appclient.client(appclient.login(email, APP_PASSWORD))


@pytest.fixture()
def anon():
    with appclient.client() as c:
        yield c


@pytest.fixture()
def account_director():
    with client_for(ACCOUNT_DIRECTOR_EMAIL) as c:
        yield c


@pytest.fixture()
def account_director2():
    with client_for(ACCOUNT_DIRECTOR2_EMAIL) as c:
        yield c


@pytest.fixture()
def producer():
    with client_for(PRODUCER_EMAIL) as c:
        yield c


@pytest.fixture()
def producer2():
    with client_for(PRODUCER2_EMAIL) as c:
        yield c


@pytest.fixture()
def creative():
    with client_for(CREATIVE_EMAIL) as c:
        yield c


@pytest.fixture()
def creative2():
    with client_for(CREATIVE2_EMAIL) as c:
        yield c


@pytest.fixture()
def legal():
    with client_for(LEGAL_EMAIL) as c:
        yield c


@pytest.fixture()
def editor():
    with client_for(EDITOR_EMAIL) as c:
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
def app_url() -> str:
    return appclient.app_url()


@pytest.fixture()
def page():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        tab = context.new_page()
        yield tab
        context.close()
        browser.close()


def me(client) -> dict:
    return ok(client.get("/auth/me"), "reading the signed-in account")


def person_id_of(client) -> str:
    value = field(me(client), "person_id")
    assert value is not None, "GET /api/auth/me must carry person_id"
    return str(value)


def find_by(items, key: str, value):
    for row in items:
        if isinstance(row, dict) and str(row.get(key)) == str(value):
            return row
    return None


def job_titled(client, title: str):
    return find_by(rows(ok(client.get("/jobs"), "listing jobs")), "title", title)


def job_id_titled(client, title: str) -> str:
    job = job_titled(client, title)
    assert job is not None, f"the seeded job {title!r} must be readable by this caller"
    return ident(job)


def campaign_by_slug(client, slug: str) -> dict:
    listing = rows(ok(client.get("/campaigns", params={"slug": slug}),
                      f"reading campaign {slug}"))
    found = find_by(listing, "slug", slug)
    assert found is not None, f"campaign {slug} must be readable by this editor: {listing}"
    return found


def make_person(producer, unit: str = PLANNING_UNIT,
                capacity: int = WEEKLY_CAPACITY) -> dict:
    token = unique_token()
    return ok(producer.post("/people", json={
        "name_en": f"Probe Person {token}",
        "name_ja": f"検証 {token}",
        "reading": f"けんしょう {token}",
        "unit": unit,
        "capacity_minutes": capacity,
    }), "adding a person as the producer")


def grant(director, person, account: str):
    return director.post(f"/people/{ident(person)}/clearances", json={
        "account": account, "starts_on": "2026-01-01", "ends_on": "2099-12-31"})


def open_brief(director, accounts=(KAGEROU,)) -> dict:
    return ok(director.post("/briefs", json={
        "accounts": list(accounts),
        "title": f"Probe brief {unique_token()}",
        "problem": "Tea is invisible after sunset.",
        "convention": "Tea is a morning drink.",
        "deliverables": "One film, three stills.",
        "deadline": "2031-12-31",
        "budget_minor": 5000000,
        "markets": ["JP", "US"],
    }), "opening a brief as the account director")


def approved_estimate(director, producer, brief) -> dict:
    estimate = ok(producer.post(f"/briefs/{ident(brief)}/estimates",
                                json={"amount_minor": 4000000}),
                  "writing an estimate as the producer")
    ok(director.post(f"/estimates/{ident(estimate)}/approve"),
       "approving the estimate as the account director")
    return estimate


def convert(director, brief, producer_person, shares):
    body = {"apportionment": [{"account": a, "share_bp": s} for a, s in shares]}
    if producer_person is not None:
        body["producer_person_id"] = producer_person
    return director.post(f"/briefs/{ident(brief)}/convert", json=body)


def make_job(director, producer, accounts=(KAGEROU,), shares=None) -> dict:
    brief = open_brief(director, accounts)
    approved_estimate(director, producer, brief)
    split = shares or ((accounts[0], APPORTIONMENT_WHOLE),)
    return ok(convert(director, brief, person_id_of(producer), split),
              "converting an approved brief into a job")


def staff(producer, job_id, person, role: str = CREATIVE_DIRECTOR,
          starts: str = "2031-01-06", ends: str = "2031-02-02", minutes: int = 600):
    return producer.post(f"/jobs/{job_id}/assignments", json={
        "person_id": ident(person), "role": role, "starts_on": starts,
        "ends_on": ends, "minutes_per_week": minutes})


def add_right(legal, job_id, markets=("JP", "US"), term_end: str = "2099-12-31",
              status: str = "cleared", right: str = "music"):
    return legal.post(f"/jobs/{job_id}/rights", json={
        "right": right, "subject": f"Probe {right} {unique_token()}",
        "licence_ref": f"LIC-{unique_token()}", "term_start": "2020-01-01",
        "term_end": term_end, "territories": list(markets), "media": ["web"],
        "status": status})


def credit_entry(role_en: str, people, pin: bool = False) -> dict:
    return {"role_en": role_en, "role_ja": f"{role_en} JA", "pin_names": pin,
            "people": [ident(p) for p in people]}


def read_credits(client, campaign_id) -> dict:
    return ok(client.get(f"/campaigns/{campaign_id}/credits"), "reading a credit list")


def save_credits(client, campaign_id, revision, entries):
    return client.put(f"/campaigns/{campaign_id}/credits",
                      json={"revision": revision, "entries": entries})


def make_campaign(director, producer, legal, editor, *, credits: bool = True,
                  permission: bool = True, right_status: str = "cleared",
                  term_end: str = "2099-12-31", markets=("JP", "US")) -> dict:
    job = make_job(director, producer)
    job_id = ident(job)
    person = make_person(producer)
    assert grant(director, person, KAGEROU).status_code in (200, 201), (
        "granting a kagerou clearance to a probe person should succeed")
    ok(staff(producer, job_id, person), "staffing the probe person")
    ok(add_right(legal, job_id, markets, term_end, right_status), "recording a right")
    slug = f"probe-campaign-{unique_token()}"
    campaign = ok(editor.post("/campaigns", json={
        "job_id": job_id, "slug": slug, "year": 2026, "month": 5,
        "categories": ["creative"],
        "clients": [{"slug": KAGEROU, "primary": True}],
        "external_url": None,
    }), "creating a campaign record as the editor")
    campaign_id = ident(campaign)
    for locale, title in (("ja", f"検証キャンペーン {slug}"), ("en", f"Probe Campaign {slug}")):
        ok(editor.put(f"/campaigns/{campaign_id}/translations/{locale}", json={
            "title": title, "description": f"{title} description.",
            "status": "published"}), f"publishing the {locale} translation")
    if credits:
        current = read_credits(editor, campaign_id)
        ok(save_credits(editor, campaign_id, current.get("revision"),
                        [credit_entry(CREATIVE_DIRECTOR, [person])]),
           "saving the probe credit list")
    if permission:
        ok(director.post(f"/campaigns/{campaign_id}/permissions", json={
            "kind": "case_study", "reference": f"PERM-{unique_token()}"}),
           "recording case-study permission")
    return {"job_id": job_id, "person": person, "campaign_id": campaign_id,
            "slug": slug}


def publish(editor, campaign_id, markets=("JP", "US"), embargo_at=None):
    body = {"markets": list(markets)}
    if embargo_at is not None:
        body["embargo_at"] = embargo_at
    return editor.post(f"/campaigns/{campaign_id}/publish", json=body)


def reasons_of(response) -> list:
    try_body = response.json() if response.content else {}
    found = field(try_body, "reasons")
    return [str(r) for r in (found or [])]


def public_index(anon, **params) -> dict:
    return ok(anon.get("/public/campaigns", params=params), "reading the public work index")


def all_public_slugs(anon, **params) -> list:
    first = public_index(anon, page=1, **params)
    slugs = [str(r.get("slug")) for r in rows(first)]
    pages = int(first.get("page_count") or 1)
    for number in range(2, pages + 1):
        slugs += [str(r.get("slug")) for r in rows(public_index(anon, page=number, **params))]
    return slugs


def tally(anon, body: str, year) -> dict:
    return ok(anon.get("/public/awards/tally", params={"body": body, "year": year}),
              "reading the public award tally")


def rank_counts(entries) -> dict:
    out = {}
    for row in entries or []:
        out[str(row.get("rank"))] = int(row.get("count") or 0)
    return {k: v for k, v in out.items() if v}


def upload_version(client, job_id, payload: bytes, label: str = "cut"):
    return client.post(f"/jobs/{job_id}/versions",
                       files={"file": ("cut.png", payload, "image/png")},
                       data={"label": label})


def enquiry_key(anon) -> str:
    key = field(ok(anon.get("/enquiries/key"), "fetching an enquiry key"), "idempotency_key")
    assert key, "GET /api/enquiries/key must return idempotency_key"
    settle()
    return str(key)


def enquiry_body(key: str, **overrides) -> dict:
    body = {"idempotency_key": key, "type": "new_business", "name": "Probe Sender",
            "company": "Probe Company", "email": probe_email(), "telephone": "",
            "message": "We would like to talk about a launch.", "consent": True,
            DECOY_FIELD: ""}
    body.update(overrides)
    return body


def secret_values() -> tuple:
    names = ("STORAGE_SECRET_KEY", "STORAGE_ACCESS_KEY")
    return tuple(v for v in (os.environ.get(n, "") for n in names) if v)


def normalised(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def script_sources(html: str) -> tuple:
    return tuple(re.findall(r"<script[^>]+src=[\"']([^\"']+)[\"']", html))
