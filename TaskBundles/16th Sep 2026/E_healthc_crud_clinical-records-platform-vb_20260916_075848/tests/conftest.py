"""Fixtures, domain helpers and the pinned literals for Clinical Records Platform.

No test_* function lives here (G10). Every value test_output.py asserts about the
SEEDED world is pinned in this file and appears verbatim in instruction.md (G6): a
grader that asserts a value the brief never pinned grades a working app as broken.
The per-run probe values are generated here and are only ever compared against
themselves, so they are deliberately not brief literals.

The shared grader (appclient, capabilities, _shapes) is supplied by the
deku-verifier-base image on PYTHONPATH=/tests. Nothing here re-implements it and
nothing here imports a provider SDK.
"""

from __future__ import annotations

import json
import os
import time

import httpx
import pytest

import appclient
import capabilities

CLINICIAN_EMAIL = "clinician@example.com"
CLINICIAN2_EMAIL = "clinician2@example.com"
FRONTDESK_EMAIL = "frontdesk@example.com"
BILLER_EMAIL = "biller@example.com"
PATIENT_EMAIL = "patient@example.com"
PATIENT2_EMAIL = "patient2@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"
SEEDED_ACCOUNTS = (CLINICIAN_EMAIL, CLINICIAN2_EMAIL, FRONTDESK_EMAIL,
                   BILLER_EMAIL, PATIENT_EMAIL, PATIENT2_EMAIL)

PRODUCT_NAME = "Kestrel"

ROLE_CLINICIAN = "clinician"
ROLE_FRONT_DESK = "front_desk"
ROLE_BILLER = "biller"
ROLE_PATIENT = "patient"

MRN_PRIMARY = "KH-100234"
MRN_SECOND = "KH-100235"
MRN_YEAR_ONLY = "KH-100236"
MRN_TWIN_ONE = "KH-100237"
MRN_TWIN_TWO = "KH-100238"
MRN_SUBSUMED = "KH-100239"
MRN_SURVIVOR = "KH-100240"
MRN_UNISSUED = "KH-999999"

BIRTH_DATE_PRIMARY = "1974-03-11"
BIRTH_DATE_SECOND = "1991-07-02"
BIRTH_DATE_YEAR_ONLY = "1988"
BIRTH_DATE_TWINS = "2016-05-09"
PRECISION_YEAR = "year"
PRECISION_DAY = "day"

ENCOUNTER_SIGNED = "ENC-2026-0001"
ENCOUNTER_OPEN = "ENC-2026-0002"
ORDER_RELEASED = "ORD-2026-0001"
PRESCRIPTION_SEEDED = "RX-2026-0001"
ELIGIBILITY_SEEDED = "ELG-2026-0001"
CLAIM_QUEUED = "CLM-2026-0001"
CLAIM_SUBMITTED = "CLM-2026-0002"
CLAIM_PAID = "CLM-2026-0003"
CLAIM_DENIED = "CLM-2026-0004"
REMITTANCE_BALANCED = "REM-2026-0001"
REMITTANCE_OUT = "REM-2026-0002"
APPOINTMENT_CANCELLED = "APT-2026-0002"
APPOINTMENT_NO_SHOW = "APT-2026-0003"

CONTENDED_DAY = "2026-09-21"

SYSTEM_DIAGNOSIS = "icd10cm"
SYSTEM_PROCEDURE = "cpt"
SYSTEM_LAB = "loinc"
SYSTEM_MEDICATION = "rxnorm"
CODE_DIABETES = "E11.9"
CODE_RESTRICTED = "F11.20"
CODE_PROCEDURE = "99213"
CODE_POTASSIUM = "2823-3"
CODE_MEDICATION = "860975"
DISPLAY_DIABETES = "Type 2 diabetes mellitus without complications"
VERSION_DIAGNOSIS = "2026"
VERSION_LAB = "2.76"

POTASSIUM_FIRST = 6.2
POTASSIUM_SECOND = 4.1
REFERENCE_LOW = 3.5
REFERENCE_HIGH = 5.1
UNIT_POTASSIUM = "mmol/L"
TROPONIN_VALUE = 0.01
UNIT_TROPONIN = "ng/mL"
COMPARATOR_BELOW = "<"

SENSITIVITY_NORMAL = "normal"
SENSITIVITY_RESTRICTED = "restricted"
PRIMARY_CONDITION_TOTAL = 3
BILLER_CONDITION_TOTAL = 2

STATUS_DRAFT = "draft"
STATUS_ACTIVE = "active"
STATUS_OPEN = "open"
STATUS_SIGNED = "signed"
STATUS_QUEUED = "queued"
STATUS_SUBMITTED = "submitted"
STATUS_PAID = "paid"
STATUS_DENIED = "denied"
STATUS_BOOKED = "booked"
STATUS_CANCELLED = "cancelled"
STATUS_NO_SHOW = "no_show"
STATE_POSTED = "posted"
STATE_QUARANTINED = "quarantined"
ASSERTION_ALLERGY = "allergy"
ASSERTION_NONE_KNOWN = "no_known_allergies"
ASSERTION_NOT_ASKED = "not_asked"
ALLERGY_SUBSTANCE = "penicillin"
ERROR_STATUS = "entered_in_error"

GROUP_CONTRACTUAL = "contractual"
GROUP_PATIENT = "patient_responsibility"
CHARGE_MINOR = 18500
PAID_MINOR = 12000
CONTRACTUAL_MINOR = 4500
PATIENT_MINOR = 2000
SPLIT_TOTAL = 10000
SPLIT_FIRST = 3334
SPLIT_REST = 3333
CURRENCY = "usd"

DOSE_QUANTITY = 500
DOSE_UNIT = "mg"
DISPENSE_QUANTITY = 60
DISPENSE_UNIT = "tablet"
REFILLS_AUTHORISED = 0

MODULE_TELEHEALTH = "skyline-telehealth"
MODULE_REPORTS = "ward-reports"
CORE_VERSION_TELEHEALTH = "7.0.10"
CORE_VERSION_REPORTS = "7.0.2"
MODULE_COUNT = 4
ARTICLE_COUNT = 3
ANNOUNCEMENT_COUNT = 2
RELEASE_VERSION = "8.3.0"
RELEASE_DATE_RENDERED = "18 March 2026"
ARTICLE_SLUG = "kestrel-8-3-0-is-released"

ANNOUNCEMENT_LABEL = "New:"
CARD_CONTRIBUTE = "Contribute Now"
CARD_TRY = "Try Now"
CARD_SUPPORT = "Find Support"
CARD_DOWNLOAD = "Download for Free"
OPEN_SOURCE_HEADING = "Fully Open-Source. Free Software, Always and Forever."
FEATURE_HEADING = "A Feature-Rich Solution"
ADOPTER_HEADING = "Who uses Kestrel"
APPEAL_HEADING = "Help Needed!"
APPEAL_CONTROL = "Donate Now"
FEATURE_FIRST = "Scheduling"
FEATURE_SECOND = "e-Prescribing"
FEATURE_EIGHTH = "Multilingual Support"
COPY_CONTROL = "Copy address"
COPY_CONFIRMED = "Copied"
DEMO_NOTICE = ("These demonstrations contain no real patient information. "
               "Everything in them is invented.")
TAX_BADGE = ("Registered nonprofit: donations are tax-deductible in the stated "
             "jurisdiction")
NEWS_HEADING = "Kestrel News"
CARD_LABEL_PREFIX = "Read more about"
NOT_FOUND_HEADING = "4-oh-4!"
NOT_FOUND_FIRST = "Looks like you were looking for a page that can't be found right now."
NOT_FOUND_SECOND = "Sorry about that, the mishap has been logged and we'll look into it."

TYPE_FAMILY = "Source Sans 3"
SIZE_FINE_PRINT = "11.9px"
SIZE_SECONDARY = "13.6px"
SIZE_BODY = "16px"
LINE_HEIGHT_BODY = "23.2px"
SIZE_CARD_TITLE = "22.4px"
SIZE_SECTION_HEADING = "32px"
SIZE_ARTICLE_H1 = "2.2rem"
SIZE_HERO = "3rem"
CONTRAST_BODY = "4.5:1"
CONTRAST_COMPONENT = "3:1"

SECURITY_HEADERS = {
    "strict-transport-security": None,
    "x-content-type-options": "nosniff",
    "x-frame-options": "DENY",
    "referrer-policy": "no-referrer",
    "content-security-policy": None,
}

PUBLIC_ROUTES = ("/", "/downloads", "/demo", "/support", "/blog", "/modules",
                 "/contribute", "/privacy")
WORKSPACE_ROUTES = ("/workspace", "/workspace/patients", "/workspace/schedule",
                    "/workspace/claims")
ABSENT_SURFACES = ("/signup", "/register", "/search", "/checkout", "/beds",
                   "/export")

TABLE_ACCOUNT = "account"
TABLE_PATIENT = "patient"
TABLE_PATIENT_IDENTIFIER = "patient_identifier"
TABLE_PATIENT_LINK = "patient_link"
TABLE_IDENTITY_REVIEW = "identity_review"
TABLE_APPOINTMENT = "appointment"
TABLE_OCCUPANCY = "resource_occupancy"
TABLE_ENCOUNTER = "encounter"
TABLE_NOTE = "clinical_note"
TABLE_SIGNATURE = "note_signature"
TABLE_CONDITION = "condition"
TABLE_ORDER = "service_request"
TABLE_OBSERVATION = "observation"
TABLE_UNMATCHED = "unmatched_result"
TABLE_ALLERGY = "allergy"
TABLE_PRESCRIPTION = "medication_request"
TABLE_COVERAGE = "coverage"
TABLE_ELIGIBILITY = "eligibility_check"
TABLE_CLAIM = "claim"
TABLE_CLAIM_LINE = "claim_line"
TABLE_REMITTANCE = "remittance"
TABLE_LEDGER = "ledger_entry"
TABLE_AUDIT = "audit_event"
TABLE_PAGE_VIEW = "page_view"

APP_ROOT = "/app"
CREDENTIALS_FILE = "/app/USER_README.md"
SCREENSHOT_DIR = "/app/.browser_screenshots"
DOWNLOAD_DIR = "/app/.downloads"

SETTLE_SECONDS = 0.25
POLL_TIMEOUT_SECONDS = 20.0
MIN_REASON_CHARS = 20

DENIED = (401, 403)
NOT_FOUND = (403, 404)
ACCEPTED = (200, 201, 202)
REFUSED = (400, 401, 403, 404, 409, 422, 429)
CONFLICTED = (400, 409, 422)


def settle() -> None:
    """Yield briefly so an asynchronous side effect can land."""
    time.sleep(SETTLE_SECONDS)


def poll_until(predicate, timeout: float = POLL_TIMEOUT_SECONDS):
    """Bounded poll on a monotonic clock. Returns the last value the predicate saw."""
    deadline = time.monotonic() + timeout
    value = None
    while time.monotonic() < deadline:
        value = predicate()
        if value:
            return value
        settle()
    return value


def unique_suffix() -> str:
    """A per-run identifier so a self-seeding check never collides with itself."""
    return os.urandom(5).hex()


def probe_family(suffix: str) -> str:
    return "Probe" + suffix.upper()


def probe_given(suffix: str) -> str:
    return "Given" + suffix.upper()


def probe_reason(suffix: str) -> str:
    """A typed reason comfortably past the stated minimum length."""
    return "Unresponsive in the waiting room, reference " + suffix


def probe_note(suffix: str) -> str:
    return "Probe assessment written by a run, reference " + suffix


def describe(response: httpx.Response, what: str) -> str:
    """The failure-message shape reference/J requires: anchor, request, status, body."""
    return (f"{what}: {response.request.method} {response.request.url} returned "
            f"{response.status_code}: {response.text[:400]}")


def backend() -> capabilities.Backend:
    """The persisted-state view the brief's own table names address."""
    return capabilities.make_backend()


def fetch_document(path: str) -> httpx.Response:
    """Fetch a rendered document from the app origin rather than from the API base."""
    return httpx.get(appclient.app_url() + path, timeout=appclient.TIMEOUT,
                     follow_redirects=True)


def fetch_raw(path: str) -> httpx.Response:
    """Fetch without following a redirect, so a redirect is itself observable."""
    return httpx.get(appclient.app_url() + path, timeout=appclient.TIMEOUT,
                     follow_redirects=False)


def head_of(markup: str) -> str:
    lower = markup.lower()
    end = lower.find("</head>")
    return markup[:end] if end > 0 else markup


def document_title(markup: str) -> str:
    lower = markup.lower()
    start = lower.find("<title")
    if start < 0:
        return ""
    open_end = lower.find(">", start)
    close = lower.find("</title>", open_end)
    if open_end < 0 or close < 0:
        return ""
    return markup[open_end + 1:close].strip()


def _meta_content(markup: str, marker: str) -> str:
    head = head_of(markup)
    lower = head.lower()
    cursor = 0
    while True:
        start = lower.find("<meta", cursor)
        if start < 0:
            return ""
        end = lower.find(">", start)
        if end < 0:
            return ""
        tag = head[start:end]
        if marker in tag.lower():
            for quote in ('content="', "content='"):
                at = tag.find(quote)
                if at >= 0:
                    rest = tag[at + len(quote):]
                    stop = rest.find(quote[-1])
                    return rest[:stop].strip() if stop >= 0 else rest.strip()
        cursor = end + 1


def meta_description(markup: str) -> str:
    return _meta_content(markup, 'name="description"') or _meta_content(markup, "description")


def preview_image(markup: str) -> str:
    return _meta_content(markup, "og:image")


def preview_title(markup: str) -> str:
    return _meta_content(markup, "og:title")


def internal_links(markup: str) -> list[str]:
    """Every same-origin href in a rendered document, as a path."""
    found = []
    lower = markup.lower()
    cursor = 0
    while True:
        at = lower.find('href="', cursor)
        if at < 0:
            return found
        rest = markup[at + 6:]
        stop = rest.find('"')
        if stop < 0:
            return found
        href = rest[:stop].strip()
        cursor = at + 6 + stop
        if href.startswith("/") and not href.startswith("//"):
            found.append(href.split("#")[0].split("?")[0])


def external_origins(markup: str) -> list[str]:
    """Absolute origins a rendered document reaches for, excluding the app's own."""
    own = appclient.app_url()
    found = []
    for marker in ('src="', 'href="'):
        lower = markup.lower()
        cursor = 0
        while True:
            at = lower.find(marker, cursor)
            if at < 0:
                break
            rest = markup[at + len(marker):]
            stop = rest.find('"')
            cursor = at + len(marker) + (stop if stop > 0 else 1)
            if stop < 0:
                break
            value = rest[:stop].strip()
            if value.startswith("http") and not value.startswith(own):
                found.append(value)
    return found


def payload_of(response: httpx.Response):
    """The decoded body, or None when the response carries no JSON at all.

    Deliberately not a guarded `response.json()`: a body that opens like JSON and
    then does not parse is a real defect, and swallowing it would turn a broken
    response into a silent None that the caller reads as an empty result.
    """
    body = (response.text or "").strip()
    if not body or body[0] not in "[{":
        return None
    return json.loads(body)


def as_list(payload) -> list:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "results", "data", "rows", "conditions", "patients",
                    "entries", "slots", "lines"):
            if isinstance(payload.get(key), list):
                return payload[key]
    return []


def get_json(token: str | None, path: str, **params) -> httpx.Response:
    with appclient.client(token) as client:
        return client.get(path, params=params or None)


def post_json(token: str | None, path: str, body: dict | None = None) -> httpx.Response:
    with appclient.client(token) as client:
        return client.post(path, json=body if body is not None else {})


def patch_json(token: str, path: str, body: dict) -> httpx.Response:
    with appclient.client(token) as client:
        return client.patch(path, json=body)


def open_encounter(token: str, mrn: str) -> str:
    response = post_json(token, "/encounters", {"mrn": mrn, "class": "ambulatory"})
    assert response.status_code in ACCEPTED, describe(
        response, "a clinician must be able to open an encounter")
    number = (payload_of(response) or {}).get("number")
    assert number, describe(response, "an opened encounter must carry a number")
    return str(number)


def add_condition(token: str, number: str, code: str = CODE_DIABETES) -> httpx.Response:
    return post_json(token, f"/encounters/{number}/conditions", {
        "code_system": SYSTEM_DIAGNOSIS,
        "code": code,
        "code_display": DISPLAY_DIABETES,
        "code_version": VERSION_DIAGNOSIS,
        "effective_time": "2026-09-16T09:00:00Z",
    })


def add_order(token: str, number: str) -> httpx.Response:
    return post_json(token, f"/encounters/{number}/orders", {
        "code_system": SYSTEM_LAB,
        "code": CODE_POTASSIUM,
        "code_display": "Potassium [Moles/volume] in Serum or Plasma",
        "code_version": VERSION_LAB,
        "intent": "order",
        "priority": "routine",
    })


def write_note(token: str, number: str, body: str, version_id) -> httpx.Response:
    return patch_json(token, f"/encounters/{number}/note",
                      {"body": body, "version_id": version_id})


def note_version(token: str, number: str):
    response = get_json(token, f"/encounters/{number}")
    payload = payload_of(response) or {}
    note = payload.get("note") or {}
    return note.get("version_id")


def sign_encounter(token: str, number: str) -> httpx.Response:
    return post_json(token, f"/encounters/{number}/sign")


def signed_probe_encounter(token: str, mrn: str, suffix: str) -> dict:
    """Open, document, code, order and sign one encounter created by this run."""
    number = open_encounter(token, mrn)
    write_note(token, number, probe_note(suffix), note_version(token, number))
    condition = add_condition(token, number)
    assert condition.status_code in ACCEPTED, describe(
        condition, "a coded diagnosis must be accepted on an open encounter")
    order = add_order(token, number)
    assert order.status_code in ACCEPTED, describe(
        order, "an order must be accepted on an open encounter")
    signed = sign_encounter(token, number)
    assert signed.status_code in ACCEPTED, describe(
        signed, "an encounter carrying a coded diagnosis must be signable")
    payload = payload_of(signed) or {}
    payload["number"] = number
    return payload


def store_rows(table: str, **where) -> list[dict]:
    return backend().rows(table, **where)


def store_one(table: str, **where):
    return poll_until(lambda: backend().one(table, **where))


def store_count(table: str, **where) -> int:
    return backend().count(table, **where)


@pytest.fixture()
def clinician() -> str:
    return appclient.login(CLINICIAN_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def clinician_two() -> str:
    return appclient.login(CLINICIAN2_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def front_desk() -> str:
    return appclient.login(FRONTDESK_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def biller() -> str:
    return appclient.login(BILLER_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def patient() -> str:
    return appclient.login(PATIENT_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def patient_two() -> str:
    return appclient.login(PATIENT2_EMAIL, SEEDED_PASSWORD)


@pytest.fixture()
def suffix() -> str:
    return unique_suffix()
