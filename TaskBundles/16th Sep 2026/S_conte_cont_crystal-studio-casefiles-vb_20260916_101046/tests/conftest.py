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
EDITOR_EMAIL = "editor@example.com"
AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
VISITOR_EMAIL = "visitor@example.com"
STUDIO_CONTACT = "newwork@kelo.example.com"
PRIVACY_CONTACT = "privacy@kelo.example.com"
CAREERS_HOST = "careers.kelo.example"

PUBLISHED_SLUG = "glass-harbour"
SECOND_SLUG = "night-signal"
THIRD_SLUG = "soft-machinery"
DRAFT_SLUG = "paper-orchard"
SUBMITTED_SLUG = "quiet-engine"
PUBLISHED_TITLE = "Glass Harbour"
DRAFT_TITLE = "Paper Orchard"
SUBMITTED_TITLE = "Quiet Engine"

SECTOR_TOKENS = ("sector-1", "sector-2", "sector-3", "sector-4",
                 "sector-5", "sector-6", "sector-7")
SECTOR_LABELS = ("Technology & Futures", "Climate & Startups", "Fashion & Beauty",
                 "Chain", "Entertainment & Culture", "Automotive", "Collaborations")
AWARD_NAMES = ("Harbour Prize", "Wexel", "A&DX", "Open Show", "Acclaims", "FWX")
DISPLAY_NAMES = ("Ines Varga", "Theo Lamb", "Juno Park", "Sam Reed")
CLIENT_NAMES = ("Aster", "Gannet", "Paper Lens", "Sandbox", "Alder Labs",
                "Groundswell Energy", "Sable", "Thornfield", "harbour Classics",
                "Clarelle", "Solene", "Trelawn & Co", "KVN", "Nautilus", "Zephyr",
                "Skra", "Nightly", "OBX", "Rook Games", "Playmarket", "Younger",
                "Lexon", "Torvid", "Lumen Motors", "Sabres", "Marconti", "MCK",
                "Emery Lauden", "Gallery Research Trust")
STUDIO_PROMISE = "Making the story move."
DISCIPLINES_LINE = "Brand · Content · Experience · Digital"
WORDMARK_LINE = "Kelo · Creative Studio"
WORDMARK_SECOND = "Since 2011"
NOTICE_TITLE = "Kelo Customer Privacy Notice"
NOTICE_DESCRIPTION = ("This privacy notice tells you what to expect us to do with "
                      "your personal information.")
NOTICE_LABELS = ("What information we collect, use, and why", "LAWFUL BASES part 1",
                 "LAWFUL BASES part 2", "Where we get personal information from",
                 "HOW LONG WE KEEP INFORMATION", "who we share information with",
                 "your data protection rights", "How to complain, United States",
                 "How to complain, European Union", "How to complain, Canada",
                 "How to complain, Australia", "How to complain, New Zealand",
                 "How to complain, United Kingdom", "When this notice was last updated")
OFFICE_CITIES = ("HARBOURSIDE", "NORTHGATE")
OFFICE_PHONES = ("+00 1 234 5670", "+00 2 345 6780")
HARBOURSIDE_LINES = ("12 Quay Street", "Harbourside Works", "Floor 3", "HS1 4QA")
NORTHGATE_LINES = ("40 North Row", "NG2 7LT")
SOCIAL_LINES = ("Directory", "Pictures", "Feed")

CHAPTER_KINDS = ("headline", "text", "list", "image", "video", "video_loop",
                 "device", "split")
CASE_STATES = ("draft", "submitted", "changes_requested", "approved", "published")
BUDGET_TOKENS = ("under-25", "25-50", "50-100", "100-250", "250-up")
MESSAGE_KINDS = ("verify_address", "reset_password", "invitation", "case_file_returned",
                 "case_file_live", "enquiry_received", "enquiry_arrived")
ERROR_TOKENS = ("validation_failed", "not_authenticated", "not_authorised", "not_found",
                "conflict", "version_conflict", "state_not_allowed", "rate_limited",
                "server_error")
ERROR_BODY_KEYS = ("error", "message", "fields", "retry_after")

SIGN_IN_REFUSAL = "That combination is not one we know."
SHORT_PASSWORD_MESSAGE = "Passwords are at least twelve characters."
RESET_ANSWER = "If that address has an account, a reset link is on its way."
LOCKED_MESSAGE = "Too many tries. Give it a minute."
TITLE_MESSAGE = "Give it a title."
CLIENT_MESSAGE = "Say who it was for."
SECTOR_MESSAGE = "Pick a sector."
DESCRIPTION_MESSAGE = "The description needs to be at least forty characters."
LAUNCH_MESSAGE = "That launch address does not look right."
NO_CHAPTER_MESSAGE = "A case file needs at least one chapter."
RETURN_NOTE_MESSAGE = "Say what needs changing."
NAME_MESSAGE = "We need a name to reply to."
EMAIL_MESSAGE = "That address does not look right."
ORGANISATION_MESSAGE = "That is longer than we can store."
BRIEF_MESSAGE = "Tell us a little more, forty characters at least."
CONSENT_MESSAGE = "We need this to be able to reply."
VERIFY_SUBJECT = "Confirm your address"
RESET_SUBJECT = "Reset your password"
INVITE_SUBJECT = "Kelo has invited you"
ENQUIRY_SENDER_SUBJECT = "We got your message"
INERT_SEPARATOR = "[:]//"

EVENT_NAMES = ("site_opened", "arrival_completed", "arrival_timed_out", "crystal_dragged",
               "crystal_reseeded", "sound_toggled", "menu_opened", "menu_word_chosen",
               "surface_opened", "surface_closed", "carousel_dragged", "grid_filtered",
               "case_file_opened", "case_file_read", "chapter_interacted", "reel_played",
               "reel_completed", "shortlist_changed", "enquiry_started", "enquiry_submitted",
               "enquiry_failed", "newsletter_submitted", "newsletter_failed", "signed_in",
               "signed_out", "case_file_created", "case_file_submitted", "case_file_returned",
               "case_file_approved", "case_file_published", "case_file_republished",
               "save_failed", "offline_entered", "offline_left", "error_shown")

MEDIA_KEY_PREFIX = "case-files/"
UPLOAD_LIMIT_BYTES = 5242880
PAGE_SIZE = 24
CAROUSEL_CAP = 12
CONSOLE_WRITE_LIMIT = 120
ORDER_WRITE_LIMIT = 30
SIGNUP_LIMIT = 3
RESET_LIMIT = 3
ENQUIRY_LIMIT = 3
NEWSLETTER_LIMIT = 5
SIGN_IN_ATTEMPT_LIMIT = 5
VISITOR_SESSION_DAYS = 30
STUDIO_SESSION_HOURS = 12
STUDIO_IDLE_SECONDS = 7200
VERIFICATION_DAYS = 7
INVITATION_DAYS = 14
HOME_TRANSFER_BUDGET = 320 * 1024

SECURITY_HEADERS = ("strict-transport-security", "x-content-type-options",
                    "x-frame-options", "referrer-policy", "content-security-policy")
PUBLIC_ROUTES = ("/", "/story", "/work", "/work/all", "/reel", "/contact", "/notice")
STUDIO_ROUTES = ("/studio", "/studio/review", "/studio/grid", "/studio/enquiries",
                 "/studio/outbox", "/studio/site", "/studio/account")
CRAWLER_FRAGMENTS = ("/a/", "/a/b", "/a/i", "/wa/", "/abc/", "/url/")
BRIEF_TEXT = ("A studio with a room that carries its own weather and a lift that "
              "opens onto the harbour, photographed over one long winter.")
SETTLE_DEADLINE = 25.0
SETTLE_INTERVAL = 0.25
LIVE_DEADLINE = 5.0


def app_origin() -> str:
    return appclient.app_url()


def fresh_email(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}@example.com"


def fresh_title(prefix: str) -> str:
    return f"{prefix} {uuid.uuid4().hex[:8]}"


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


def refusal(response: httpx.Response, where: str) -> dict:
    assert is_client_error(response.status_code), (
        f"{where} answered {response.status_code}, and a refusal is a client error: "
        f"{response.text[:300]}")
    payload = body(response)
    assert isinstance(payload, dict), f"{where} carried no error body: {payload!r}"
    for key in ERROR_BODY_KEYS:
        assert key in payload, f"{where} error body is missing {key!r}: {payload}"
    assert payload["error"] in ERROR_TOKENS, (
        f"{where} carried the error token {payload['error']!r}, outside the nine tokens")
    return payload


def denied(response: httpx.Response, where: str) -> dict:
    payload = refusal(response, where)
    assert payload["error"] in ("not_authenticated", "not_authorised", "not_found"), (
        f"{where} answered {payload['error']!r} where a denial was due")
    return payload


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


def upload_image(api: httpx.Client, case_id, data: bytes | None = None,
                 name: str = "chapter.png", content_type: str = "image/png"):
    payload = data if data is not None else png_bytes(tone=7)
    files = {"file": (name, io.BytesIO(payload), content_type)}
    return api.post(f"/studio/case-files/{case_id}/media", files=files)


def new_case_file(api: httpx.Client) -> dict:
    response = api.post("/studio/case-files")
    assert response.status_code < 300, (
        f"a new case file answered {response.status_code}: {response.text[:300]}")
    record = response.json()
    assert record.get("id") is not None, f"the new case file carries no id: {record}"
    return record


def save_header(api: httpx.Client, case_id, **fields) -> httpx.Response:
    return api.patch(f"/studio/case-files/{case_id}", json=fields)


def add_chapter(api: httpx.Client, case_id, kind: str, payload: dict) -> dict:
    response = api.post(f"/studio/case-files/{case_id}/chapters",
                        json={"kind": kind, "payload": payload})
    assert response.status_code < 300, (
        f"a {kind} chapter answered {response.status_code}: {response.text[:300]}")
    return response.json()


def transition(api: httpx.Client, case_id, to: str, note: str = "") -> httpx.Response:
    return api.post(f"/studio/case-files/{case_id}/transitions",
                    json={"to": to, "note": note})


def studio_record(api: httpx.Client, case_id) -> dict:
    response = api.get(f"/studio/case-files/{case_id}")
    assert response.status_code == 200, (
        f"the studio read answered {response.status_code}: {response.text[:300]}")
    return response.json()


def ready_case_file(api: httpx.Client, title: str | None = None,
                    sector: str = "sector-6", with_image: bool = False) -> dict:
    record = new_case_file(api)
    case_id = record["id"]
    chosen = title or fresh_title("Room")
    saved = save_header(api, case_id, title=chosen, client="Lumen Motors",
                        sector=sector, description=BRIEF_TEXT)
    assert saved.status_code < 300, (
        f"the header save answered {saved.status_code}: {saved.text[:300]}")
    add_chapter(api, case_id, "headline", {"title": chosen})
    add_chapter(api, case_id, "text", {"label": "Story", "body": BRIEF_TEXT})
    if with_image:
        media = upload_image(api, case_id)
        assert media.status_code < 300, (
            f"the upload answered {media.status_code}: {media.text[:300]}")
        add_chapter(api, case_id, "image",
                    {"alt": "The harbour room", "media_id": media.json()["id"]})
    return studio_record(api, case_id)


def submit(api: httpx.Client, case_id) -> httpx.Response:
    return transition(api, case_id, "submitted")


def published_case_file(author_api: httpx.Client, editor_api: httpx.Client,
                        title: str | None = None, sector: str = "sector-6",
                        with_image: bool = False) -> dict:
    record = ready_case_file(author_api, title=title, sector=sector,
                             with_image=with_image)
    case_id = record["id"]
    moved = submit(author_api, case_id)
    assert moved.status_code < 300, (
        f"the submit answered {moved.status_code}: {moved.text[:300]}")
    approved = transition(editor_api, case_id, "approved")
    assert approved.status_code < 300, (
        f"the approval answered {approved.status_code}: {approved.text[:300]}")
    live = transition(editor_api, case_id, "published")
    assert live.status_code < 300, (
        f"the publication answered {live.status_code}: {live.text[:300]}")
    return studio_record(editor_api, case_id)


def invited_account(editor_api: httpx.Client, role: str = "author",
                    display_name: str = "Wren Abbot") -> dict:
    email = fresh_email(role)
    response = editor_api.post("/studio/invitations",
                               json={"email": email, "role": role,
                                     "display_name": display_name})
    assert response.status_code < 300, (
        f"the invitation answered {response.status_code}: {response.text[:300]}")
    invitation = response.json()
    token = token_of(invitation.get("invite_url", ""))
    assert token, f"the invitation carries no token: {invitation}"
    accepted = httpx.post(f"{appclient.api_base()}/invitations/accept",
                          json={"token": token, "password": PASSWORD,
                                "display_name": display_name},
                          timeout=appclient.TIMEOUT)
    assert accepted.status_code < 300, (
        f"accepting answered {accepted.status_code}: {accepted.text[:300]}")
    return {"email": email, "role": role, "display_name": display_name,
            "account": accepted.json()}


def token_of(link: str) -> str:
    if "token=" not in link:
        return ""
    return link.split("token=", 1)[1].split("&", 1)[0]


def messages_for(api: httpx.Client) -> list:
    response = api.get("/messages")
    assert response.status_code == 200, (
        f"the message list answered {response.status_code}: {response.text[:300]}")
    return response.json()


def message_of_kind(api: httpx.Client, kind: str) -> dict:
    rows = [row for row in messages_for(api) if row.get("kind") == kind]
    assert rows, f"no {kind} message reached this account: {messages_for(api)}"
    return rows[0]


def signed_up_visitor(display_name: str = "Rowan Ash") -> dict:
    email = fresh_email("visitor")
    response = httpx.post(f"{appclient.api_base()}/auth/signup",
                          json={"email": email, "password": PASSWORD,
                                "display_name": display_name},
                          timeout=appclient.TIMEOUT)
    assert response.status_code < 300, (
        f"the sign-up answered {response.status_code}: {response.text[:300]}")
    payload = response.json()
    assert payload.get("access_token"), f"the sign-up returned no token: {payload}"
    return {"email": email, "token": payload["access_token"],
            "account": payload.get("account") or {}}


def verified_visitor(display_name: str = "Rowan Ash") -> dict:
    created = signed_up_visitor(display_name)
    with appclient.client(created["token"]) as api:
        message = message_of_kind(api, "verify_address")
    token = token_of(message.get("link", ""))
    assert token, f"the confirmation message carries no token: {message}"
    confirmed = httpx.post(f"{appclient.api_base()}/accounts/verifications",
                           json={"token": token}, timeout=appclient.TIMEOUT)
    assert confirmed.status_code < 300, (
        f"the confirmation answered {confirmed.status_code}: {confirmed.text[:300]}")
    return created


def enquiry_payload(**fields) -> dict:
    payload = {"name": "Mira Vance", "email": fresh_email("sender"),
               "organisation": "Quay Works", "budget": "50-100",
               "brief": BRIEF_TEXT, "sector": "sector-1", "consent": True}
    payload.update(fields)
    return payload


def send_enquiry(api: httpx.Client, **fields) -> httpx.Response:
    return api.post("/enquiries", json=enquiry_payload(**fields))


def public_summaries(params: dict | None = None) -> list:
    response = httpx.get(f"{appclient.api_base()}/case-files", params=params or {},
                         timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"the public list answered {response.status_code}: {response.text[:300]}")
    payload = response.json()
    assert isinstance(payload, list), f"the public list is not an array: {payload!r}"
    return payload


def all_published() -> list:
    rows = []
    page = 1
    while True:
        batch = public_summaries({"page": page})
        if not batch:
            break
        rows += batch
        if len(batch) < PAGE_SIZE:
            break
        page += 1
    return rows


def public_case_file(slug: str) -> dict:
    response = httpx.get(f"{appclient.api_base()}/case-files/{slug}",
                         timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"the public read of {slug} answered {response.status_code}")
    return response.json()


def site_document() -> dict:
    response = httpx.get(f"{appclient.api_base()}/site", timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"the site document answered {response.status_code}: {response.text[:300]}")
    return response.json()


def flat(payload) -> str:
    return json.dumps(payload, default=str).lower()


def open_site(driver, path: str = "/"):
    driver.goto(f"{app_origin()}{path}", wait_until="networkidle")
    return driver


def sign_in_on_page(surface, email: str, password: str = PASSWORD):
    surface.fill('input[name="email"]', email)
    surface.fill('input[name="password"]', password)
    surface.keyboard.press("Enter")
    surface.wait_for_timeout(3000)
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
def editor():
    with appclient.client(appclient.login(EDITOR_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture()
def author():
    with appclient.client(appclient.login(AUTHOR_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture()
def other_author():
    with appclient.client(appclient.login(AUTHOR2_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture()
def visitor():
    with appclient.client(appclient.login(VISITOR_EMAIL, PASSWORD)) as c:
        yield c


@pytest.fixture()
def fresh_author(editor):
    account = invited_account(editor, role="author", display_name="Wren Abbot")
    with appclient.client(appclient.login(account["email"], PASSWORD)) as c:
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
