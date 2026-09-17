from __future__ import annotations

import base64
import datetime
import hashlib
import hmac
import html as html_lib
import json
import os
import re
import struct
import threading
import time
import zlib

import httpx
import pytest

import appclient
import capabilities

SEED_PASSWORD = "deku-demo-pw-2026"

AUTHOR_EMAIL = "author@example.com"
AUTHOR2_EMAIL = "author2@example.com"
READER_EMAIL = "reader@example.com"
READER2_EMAIL = "reader2@example.com"
FRIEND_EMAIL = "friend@example.com"
AUTHOR_NAME = "Camille Rouyer"
AUTHOR2_NAME = "Damien Lorca"

STUDIO_NAME = "Doudou Fever"
CONTACT_EMAIL = "hello@example.com"
STUDIO_TIME_ZONE = "Europe/Paris"
STUDIO_CURRENCY = "usd"
DEFAULT_LOCALE = "en"
EARLY_ACCESS_THRESHOLD = 500
CREDIT_THRESHOLD = 2000
SEEDED_ASSET_VERSION = 66
EARLY_ACCESS_DAYS = 7

TIPBOX_SECRET = "tbx_whsec_5f3a9c2e81d7"
TIPBOX_SECRET_LAST_FOUR = "81d7"
TIPBOX_PAGE = "https://tipbox.example/doudou-fever"
SIGNATURE_HEADER = "Tipbox-Signature"
SIGNATURE_WINDOW_SECONDS = 300
EFFECT_DEADLINE_SECONDS = 30
SCHEDULER_DEADLINE_SECONDS = 60

SEED_TIP_ONE = "tbx_seed_001"
SEED_TIP_TWO = "tbx_seed_002"
VOLUME_ONE_LABEL = "Vol. I"
BRAND = "Doudou Fever"

LOCALES = ("en", "fr")
LANGUAGE_TAGS = {"en": "en-GB", "fr": "fr-FR"}
DISPLAY_NAMES = {"en": "English", "fr": "Francais"}
NAMESPACES = ("chrome", "index", "chapters", "reader", "locked", "about", "legal", "consent",
              "not-found", "support", "account")
CHAPTER_STATES_ALL = ("draft", "ready", "scheduled", "published", "unpublished")
TIP_ENTITLEMENT_VALUES = ("granted", "below_threshold", "unmatched", "awaiting_confirmation", "revoked")
TIP_STATE_VALUES = ("received", "refunded", "disputed")
TIP_ROW_FIELDS = ("id", "tip_id", "received_at", "source", "amount", "currency", "settled_amount", "rate",
                  "message", "supporter_email", "matched_reader_email", "match_method", "entitlement", "state")
EVENT_PARAMS = {
    "chapter_opened": ("volume", "chapter", "locale"),
    "panel_reached": ("volume", "chapter", "panel", "elapsed_seconds"),
    "chapter_completed": ("volume", "chapter", "elapsed_seconds"),
    "chapter_abandoned": ("volume", "chapter", "last_panel", "elapsed_seconds"),
    "tip_control_pressed": ("route",),
    "chapter_load_failed": ("volume", "chapter", "failure"),
    "language_switched": ("locale",),
    "fullscreen_toggled": ("state",),
}
PAGE_VIEW_ROUTES = ("index", "chapters", "chapter-id", "about", "legal", "support-return", "account", "not-found")
FUNCTIONAL_KEYS = ("dd-consent", "dd-language", "dd-last-chapter")
PROGRESS_KEY_PREFIX = "dd-progress-"
READER_SESSION_KEY = "dd-session"
AUTHOR_SESSION_KEY = "dd-studio-session"
AUDIT_ACTIONS = ("chapter.published", "chapter.scheduled", "chapter.unpublished", "layer.imported")
ALERT_KIND = "preflight_failed_at_release"
RELEASE_INPUT = "2027-03-28T20:00:00+02:00"
RELEASE_READBACK = "2027-03-28T18:00:00Z"
CHAPTER_BYTE_BUDGET = 24000000
FIRST_BOARD_BYTE_BUDGET = 3000000
DUPLICATE_ADDRESS_MESSAGE = "That address cannot be used."
SEED_TIP_ONE_MESSAGE = "go doudou go"
SEED_TIP_TWO_MESSAGE = "for the bus scene"
FONT_FALLBACK = '"Helvetica Neue", Helvetica, Arial, "Liberation Sans", system-ui, sans-serif'
PUBLIC_ROUTES = ("/", "/chapters", "/chapter/1", "/about", "/legal", "/support/return", "/account")
LEGAL_HEADINGS = ("Website Publisher", "Hosting", "Domains", "Intellectual Property", "Terms of Use",
                  "Personal Data & Privacy", "Cookies & Trackers", "Applicable Law & Jurisdiction")
HOSTING = "Nimbus Edge SAS, 12 rue des Lilas, 75011 Paris, France"
REGISTRAR = "Registre Clair SARL, 4 quai du Port, 13002 Marseille, France"
DOMAINS = ("doudoufever.example", "www.doudoufever.example", "doudou-fever.example", "doudoufever-comic.example")
SECURITY_HEADERS = ("strict-transport-security", "content-security-policy", "x-frame-options",
                    "x-content-type-options", "referrer-policy", "permissions-policy")
WIDE_VIEWPORT = {"width": 1440, "height": 900}
TABLET_VIEWPORT = {"width": 880, "height": 1000}
NARROW_TABLET_VIEWPORT = {"width": 760, "height": 1000}
PHONE_VIEWPORT = {"width": 390, "height": 844}
SMALLEST_VIEWPORT = {"width": 320, "height": 640}
PORTRAIT_VIEWPORT = {"width": 600, "height": 1000}
TINY_JPEG = ("/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP////////////////////////////////////////////////////////"
             "//////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA=")
TINY_WEBP = "UklGRhoAAABXRUJQVlA4TA0AAAAvAAAAEAcQERGIiP4HAA=="
ULID_RE = re.compile(r"^[0-9A-Za-z]{26}$")
SHA_KEY_RE = re.compile(r"^chapters/(\d+)/(\d+)/([a-z0-9-]+)/([0-9a-f]{64})\.png$")


def settle(seconds: float = 0.5) -> None:
    """The only sanctioned pause. Asynchronous effects are polled against a deadline."""
    time.sleep(seconds)


def now_unix() -> int:
    """The verifier clock, read in one place."""
    return int(time.time())


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def iso_in(seconds: float) -> str:
    """An instant `seconds` from now, written in UTC with a Z."""
    moment = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
    return moment.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_instant(value: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def deadline_after(seconds: float) -> float:
    return time.monotonic() + seconds


def before(deadline: float) -> bool:
    return time.monotonic() < deadline


def token_hex() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return "probe-" + token_hex() + "@example.com"


def describe(response: httpx.Response) -> str:
    return f"{response.request.method} {response.request.url} -> {response.status_code}: {response.text[:400]}"


def error_of(response: httpx.Response) -> dict:
    body = response.json()
    assert isinstance(body, dict) and isinstance(body.get("error"), dict), (
        f"a rejection must carry an error object. {describe(response)}")
    return body["error"]


def assert_rejected(response: httpx.Response, field: str | None = None, statuses=(400, 409, 422)) -> dict:
    assert response.status_code in statuses, f"expected a client rejection. {describe(response)}"
    error = error_of(response)
    for key in ("code", "message", "request_id"):
        assert key in error, f"error body lacks {key}. {describe(response)}"
    if field is not None:
        assert error.get("field") == field, f"rejection should name the {field} field. {describe(response)}"
    return error


def items_of(payload) -> list:
    if isinstance(payload, list):
        return payload
    assert isinstance(payload, dict) and isinstance(payload.get("items"), list), (
        f"a paged list returns items and next_cursor: {str(payload)[:300]}")
    return payload["items"]


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


def api_client(token: str | None = None) -> httpx.Client:
    return appclient.client(token)


def site_client() -> httpx.Client:
    return httpx.Client(base_url=appclient.app_url(), timeout=appclient.TIMEOUT, follow_redirects=False)


def reader_login(email: str, password: str = SEED_PASSWORD) -> str:
    return appclient.login(email, password)


def studio_login(email: str, password: str = SEED_PASSWORD) -> str:
    response = httpx.post(f"{appclient.api_base()}/studio/auth/login",
                          json={"email": email, "password": password}, timeout=appclient.TIMEOUT)
    assert response.status_code == 200, f"studio sign-in failed. {describe(response)}"
    token = response.json().get("access_token")
    assert token, f"studio sign-in returned no access_token. {describe(response)}"
    return token


def register_reader(password: str = SEED_PASSWORD, locale: str | None = None) -> dict:
    email = probe_email()
    body = {"email": email, "password": password, "website": ""}
    if locale:
        body["locale"] = locale
    with api_client() as anon:
        created = anon.post("/auth/register", json=body)
    assert created.status_code in (200, 201), f"a probe reader was refused. {describe(created)}"
    token = created.json().get("access_token")
    assert token, f"registration returned no access_token. {describe(created)}"
    return {"email": email, "password": password, "token": token}


@pytest.fixture(scope="session")
def author_token() -> str:
    return studio_login(AUTHOR_EMAIL)


@pytest.fixture
def author(author_token):
    with api_client(author_token) as session:
        yield session


@pytest.fixture(scope="session")
def reader_token() -> str:
    return reader_login(READER_EMAIL)


@pytest.fixture
def reader(reader_token):
    with api_client(reader_token) as session:
        yield session


@pytest.fixture
def anon():
    with api_client() as session:
        yield session


@pytest.fixture
def site():
    with site_client() as session:
        yield session


def sign(body: bytes, secret: str = TIPBOX_SECRET, stamp: int | None = None) -> str:
    moment = now_unix() if stamp is None else stamp
    digest = hmac.new(secret.encode(), str(moment).encode() + b"." + body, hashlib.sha256).hexdigest()
    return f"t={moment},v1={digest}"


def deliver(body: bytes, signature: str | None = None) -> httpx.Response:
    headers = {"Content-Type": "application/json", SIGNATURE_HEADER: signature or sign(body)}
    return httpx.post(f"{appclient.api_base()}/webhooks/tipbox", content=body, headers=headers,
                      timeout=appclient.TIMEOUT)


def event_body(kind: str, data: dict, event_id: str | None = None) -> bytes:
    payload = {"id": event_id or "evt_" + token_hex(), "type": kind, "created": now_unix(), "data": data}
    return json.dumps(payload, separators=(", ", ": ")).encode()


def tip_data(settled: int, email: str | None = None, token: str | None = None, tip_id: str | None = None,
             amount: int | None = None, currency: str = "usd", rate: str = "1.000000", message: str = "probe tip") -> dict:
    return {"tip_id": tip_id or "tbx_probe_" + token_hex(), "amount": settled if amount is None else amount,
            "currency": currency, "settled_amount": settled, "rate": rate,
            "supporter_email": email or probe_email(), "message": message, "return_token": token}


def return_token() -> str:
    with api_client() as anon:
        response = anon.post("/tips/return-tokens")
    assert response.status_code in (200, 201), f"return token issue failed. {describe(response)}"
    return response.json()["token"]


def claim(token_value: str, reader_token_value: str | None) -> httpx.Response:
    with api_client(reader_token_value) as session:
        return session.post("/tips/return", json={"token": token_value})


def entitlements(token_value: str) -> list:
    with api_client(token_value) as session:
        response = session.get("/me/entitlements")
    assert response.status_code == 200, f"entitlements unreadable. {describe(response)}"
    return response.json()


def active_kinds(token_value: str) -> set:
    return {e["kind"] for e in entitlements(token_value) if e.get("active")}


def wait_for(predicate, seconds: float = EFFECT_DEADLINE_SECONDS, interval: float = 1.0):
    """Poll a condition until it holds or the deadline passes; returns the last value."""
    limit = deadline_after(seconds)
    value = predicate()
    while not value and before(limit):
        settle(interval)
        value = predicate()
    return value


def manifest(order: int, number: int, token_value: str | None = None, locale: str = "en") -> httpx.Response:
    with api_client(token_value) as session:
        return session.get(f"/volumes/{order}/chapters/{number}", params={"locale": locale})


def volumes(token_value: str | None = None, locale: str = "en") -> list:
    with api_client(token_value) as session:
        response = session.get("/volumes", params={"locale": locale})
    assert response.status_code == 200, f"volume list unreadable. {describe(response)}"
    return response.json()


def layer_urls(body: dict) -> list:
    return [layer["image_url"] for board in body["boards"] for panel in board["panels"] for layer in panel["layers"]]


def fetch_absolute(url: str, token_value: str | None = None) -> httpx.Response:
    headers = {"Authorization": f"Bearer {token_value}"} if token_value else {}
    target = url if url.startswith("http") else appclient.app_url() + url
    return httpx.get(target, headers=headers, timeout=appclient.TIMEOUT)


def studio_volume(author_session: httpx.Client, order: int = 1) -> dict:
    response = author_session.get("/studio/volumes")
    assert response.status_code == 200, f"studio volumes unreadable. {describe(response)}"
    for row in response.json():
        if int(row["order"]) == order:
            return row
    raise AssertionError(f"no studio volume with order {order}")


def studio_chapters(author_session: httpx.Client, volume_id: str) -> list:
    response = author_session.get(f"/studio/volumes/{volume_id}/chapters")
    assert response.status_code == 200, f"studio chapter list unreadable. {describe(response)}"
    return response.json()


def studio_chapter_row(author_session: httpx.Client, order: int, number: int) -> dict:
    volume = studio_volume(author_session, order)
    for row in studio_chapters(author_session, volume["id"]):
        if int(row["number"]) == number:
            return row
    raise AssertionError(f"no chapter {number} in volume {order}")


def studio_chapter(author_session: httpx.Client, chapter_id: str) -> dict:
    response = author_session.get(f"/studio/chapters/{chapter_id}")
    assert response.status_code == 200, f"chapter unreadable. {describe(response)}"
    return response.json()


def settings_of(author_session: httpx.Client) -> dict:
    response = author_session.get("/studio/settings")
    assert response.status_code == 200, f"settings unreadable. {describe(response)}"
    return response.json()


def png_chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def make_png(width: int = 8, height: int = 8, rgb=(40, 80, 120), noise: bool = False, text: bytes = b"") -> bytes:
    """A real PNG built from zlib alone; `noise` makes it incompressible, `text` adds a metadata chunk."""
    rows = bytearray()
    for _ in range(height):
        rows.append(0)
        rows.extend(os.urandom(width * 3) if noise else bytes(rgb) * width)
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    chunks = png_chunk(b"IHDR", header)
    if text:
        chunks += png_chunk(b"tEXt", b"Comment\x00" + text)
    chunks += png_chunk(b"IDAT", zlib.compress(bytes(rows), 9)) + png_chunk(b"IEND", b"")
    return b"\x89PNG\r\n\x1a\n" + chunks


def tiny_jpeg() -> bytes:
    return base64.b64decode(TINY_JPEG)


def tiny_webp() -> bytes:
    return base64.b64decode(TINY_WEBP)


def frame_table() -> bytes:
    return json.dumps({"width": 16, "height": 8, "fps": 12,
                       "frames": [{"x": 0, "y": 0, "w": 8, "h": 8, "pivot_x": 4, "pivot_y": 4, "duration_ms": 80},
                                  {"x": 8, "y": 0, "w": 8, "h": 8, "pivot_x": 4, "pivot_y": 4, "duration_ms": 80}],
                       "clips": [{"name": "dance", "first": 0, "last": 1, "loop": "loop"}]}).encode()


def upload(author_session: httpx.Client, board_id: str, files: list) -> httpx.Response:
    parts = [("files", (name, data, kind)) for name, data, kind in files]
    return author_session.post(f"/studio/boards/{board_id}/imports", files=parts)


def board_detail(author_session: httpx.Client, board_id: str) -> dict:
    response = author_session.get(f"/studio/boards/{board_id}")
    assert response.status_code == 200, f"board unreadable. {describe(response)}"
    return response.json()


def new_volume(author_session: httpx.Client) -> dict:
    response = author_session.post("/studio/volumes", json={"label": "Probe " + token_hex()})
    assert response.status_code in (200, 201), f"volume creation failed. {describe(response)}"
    return response.json()


def new_chapter(author_session: httpx.Client, volume_id: str, en: str = "probe chapter", fr: str = "chapitre sonde") -> dict:
    response = author_session.post(f"/studio/volumes/{volume_id}/chapters",
                                   json={"titles": {"en": en, "fr": fr},
                                         "descriptions": {"en": "A probe chapter.", "fr": "Un chapitre sonde."}})
    assert response.status_code in (200, 201), f"chapter creation failed. {describe(response)}"
    return response.json()


def new_board(author_session: httpx.Client, chapter_id: str) -> dict:
    response = author_session.post(f"/studio/chapters/{chapter_id}/boards", json={"name": "board " + token_hex()})
    assert response.status_code in (200, 201), f"board creation failed. {describe(response)}"
    return response.json()


def describe_panels(author_session: httpx.Client, board_id: str) -> dict:
    detail = board_detail(author_session, board_id)
    for panel in detail["panels"]:
        response = author_session.patch(f"/studio/panels/{panel['id']}",
                                        json={"version": panel["version"],
                                              "descriptions": {"en": "A probe panel.", "fr": "Une case sonde."}})
        assert response.status_code == 200, f"panel description save failed. {describe(response)}"
    return board_detail(author_session, board_id)


def store_cover(author_session: httpx.Client, chapter_id: str) -> httpx.Response:
    return author_session.put(f"/studio/chapters/{chapter_id}/cover",
                              files={"file": ("cover.png", make_png(12, 16, (200, 120, 40)), "image/png")})


def build_chapter(author_session: httpx.Client, volume: dict | None = None, panels: int = 1,
                  ready: bool = True) -> dict:
    """A complete probe chapter in a probe volume: board, layered panels, descriptions, cover."""
    volume = volume or new_volume(author_session)
    chapter = new_chapter(author_session, volume["id"])
    number = int(chapter["number"])
    board = new_board(author_session, chapter["id"])
    files = []
    for p in range(1, panels + 1):
        files.append((f"c{number}b{board['number']}p{p}-back.png", make_png(8, 8, (20, 20, 60)), "image/png"))
        files.append((f"c{number}b{board['number']}p{p}-stage.png", make_png(8, 8, (90, 60, 30)), "image/png"))
    imported = upload(author_session, board["id"], files)
    assert imported.status_code in (200, 201), f"probe import failed. {describe(imported)}"
    describe_panels(author_session, board["id"])
    covered = store_cover(author_session, chapter["id"])
    assert covered.status_code in (200, 201), f"cover upload failed. {describe(covered)}"
    if ready:
        marked = author_session.post(f"/studio/chapters/{chapter['id']}/ready")
        assert marked.status_code == 200, f"probe chapter could not be marked ready. {describe(marked)}"
    return {"volume": volume, "chapter": studio_chapter(author_session, chapter["id"]), "board": board,
            "number": number, "order": int(volume["order"])}


def publish(author_session: httpx.Client, chapter_id: str) -> httpx.Response:
    return author_session.post(f"/studio/chapters/{chapter_id}/publish")


def schedule(author_session: httpx.Client, chapter_id: str, release_at: str) -> httpx.Response:
    return author_session.post(f"/studio/chapters/{chapter_id}/schedule", json={"release_at": release_at})


def chapter_state(author_session: httpx.Client, chapter_id: str) -> str:
    return studio_chapter(author_session, chapter_id)["state"]


def patch_studio_chapter(author_session: httpx.Client, chapter_id: str, **fields) -> httpx.Response:
    current = studio_chapter(author_session, chapter_id)
    return author_session.patch(f"/studio/chapters/{chapter_id}", json={"version": current["version"], **fields})


def tips_page(author_session: httpx.Client, **params) -> dict:
    response = author_session.get("/studio/tips", params=params)
    assert response.status_code == 200, f"tip list unreadable. {describe(response)}"
    return response.json()


def all_tips(author_session: httpx.Client) -> list:
    rows, cursor = [], None
    for _ in range(200):
        params = {"limit": 200}
        if cursor:
            params["cursor"] = cursor
        page_body = tips_page(author_session, **params)
        rows.extend(page_body["items"])
        cursor = page_body.get("next_cursor")
        if not cursor:
            break
    return rows


def tip_row(author_session: httpx.Client, tip_id: str) -> dict | None:
    for row in all_tips(author_session):
        if row.get("tip_id") == tip_id:
            return row
    return None


def columns_of(backend, table: str) -> set:
    rows = backend.query("SELECT column_name FROM information_schema.columns "
                         "WHERE table_schema = current_schema() AND table_name = %s", (table,))
    return {str(r["column_name"]) for r in rows}


def run_together(calls: list) -> list:
    """Start every call at one barrier so they genuinely race; returns their results in order."""
    barrier = threading.Barrier(len(calls))
    results = [None] * len(calls)

    def runner(index, call):
        barrier.wait()
        results[index] = call()

    threads = [threading.Thread(target=runner, args=(i, c)) for i, c in enumerate(calls)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results


@pytest.fixture(scope="session")
def chromium():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as driver:
        browser = driver.chromium.launch(headless=True)
        try:
            yield browser
        finally:
            browser.close()


def new_context(chromium, consent: str | None = "declined", viewport=None, **options):
    context = chromium.new_context(viewport=viewport or WIDE_VIEWPORT, **options)
    if consent:
        context.add_init_script(f"try {{ if (!window.localStorage.getItem('dd-consent')) "
                                f"window.localStorage.setItem('dd-consent', '{consent}'); }} catch (e) {{}}")
    return context


@pytest.fixture
def ui_page(chromium):
    context = new_context(chromium)
    tab = context.new_page()
    tab.set_default_timeout(30000)
    try:
        yield tab
    finally:
        context.close()


def open_route(tab, route: str, wait: float = 1.0) -> None:
    tab.goto(appclient.app_url() + route, wait_until="load")
    settle(wait)


def mark_document(tab) -> None:
    tab.evaluate("() => { window.__ddProbe = 'kept'; }")


def document_kept(tab) -> bool:
    return tab.evaluate("() => window.__ddProbe === 'kept'")


def storage_keys(tab) -> list:
    return tab.evaluate("() => { const keys = []; for (let i = 0; i < localStorage.length; i++) "
                        "{ keys.push(localStorage.key(i)); } for (let i = 0; i < sessionStorage.length; i++) "
                        "{ keys.push(sessionStorage.key(i)); } return keys; }")


def cookie_names(tab) -> list:
    return [c["name"] for c in tab.context.cookies()]


def signed_in_reader_page(chromium, email: str = READER_EMAIL, **options):
    context = new_context(chromium, **options)
    token = reader_login(email)
    context.add_init_script(f"try {{ window.localStorage.setItem('dd-session', '{token}'); }} catch (e) {{}}")
    tab = context.new_page()
    tab.set_default_timeout(30000)
    return context, tab, token


def signed_in_author_page(chromium, **options):
    context = new_context(chromium, **options)
    token = studio_login(AUTHOR_EMAIL)
    context.add_init_script(f"try {{ window.localStorage.setItem('dd-studio-session', '{token}'); }} catch (e) {{}}")
    tab = context.new_page()
    tab.set_default_timeout(30000)
    return context, tab, token


def document_meta(document: str) -> tuple:
    title = re.search(r"<title[^>]*>(.*?)</title>", document, re.S | re.I)
    tag = re.search(r"<meta\b[^>]*\bname=[\"']description[\"'][^>]*>", document, re.I)
    desc = re.search(r"\bcontent=\"([^\"]*)\"|\bcontent='([^']*)'", tag.group(0)) if tag else None
    lang = re.search(r"<html\b[^>]*\blang=[\"']([^\"']+)[\"']", document, re.I)
    return (html_lib.unescape(title.group(1).strip()) if title else None,
            html_lib.unescape(desc.group(1) if desc.group(1) is not None else desc.group(2)) if desc else None,
            lang.group(1) if lang else None)


def capitalise_words(title: str) -> str:
    return " ".join(word[:1].upper() + word[1:] for word in title.split(" "))


def two_digit(value: int) -> str:
    return f"{int(value):02d}"


@pytest.fixture(scope="session")
def early_signed_image() -> dict:
    """A signed early-access image address captured at the start of the run, with the asset version it carries."""
    token = reader_login(READER_EMAIL)
    response = manifest(1, 4, token)
    assert response.status_code == 200, describe(response)
    url = layer_urls(response.json())[0]
    return {"url": url, "captured": now_unix()}


@pytest.fixture(scope="session")
def audit_snapshot(backend) -> dict:
    """Every audit record stored when the run starts."""
    return {"rows": backend.query("SELECT * FROM audit_records")}


CATALOGUE_EN = {'chrome.chapters': 'chapters',
 'chrome.about': 'about',
 'chrome.legal': 'legal notice & terms of use',
 'chrome.byline': 'by Camille Rouyer and Damien Lorca',
 'chrome.fullscreen_enter': 'enter fullscreen',
 'chrome.fullscreen_exit': 'exit fullscreen',
 'index.button': 'read now',
 'index.credit': 'By Damien Lorca & Camille Rouyer',
 'chapters.heading': 'select a chapter',
 'chapters.tip': 'support us',
 'chapters.next_track': 'next track',
 'reader.loading': 'Next track is loading...',
 'reader.text_mode': 'read as text',
 'reader.previous_panel': 'previous panel',
 'reader.next_panel': 'next panel',
 'reader.progress': 'chapter progress',
 'reader.load_failed': 'Something went missing. Try again?',
 'reader.retry': 'try again',
 'reader.back': 'back to chapters',
 'locked.timing': 'This chapter opens {date}.',
 'locked.drawing': 'This chapter is still being drawn.',
 'locked.notify': 'notify me',
 'locked.support': 'Supporters read it as soon as it is finished.',
 'consent.message': 'Hey you ✨ This site uses cookies to measure the traffic.',
 'consent.accept': 'Accept',
 'consent.decline': 'Decline',
 'support.granted': 'Thank you. Your early access is active.',
 'support.sign_in': 'Thank you. Sign in and we will attach it to your account.',
 'support.below_threshold': 'Thank you. Every tip helps, and this one goes straight into the next chapter.',
 'support.pending': 'Thank you. Your tip is on its way to us.',
 'support.expired': 'This thank-you link has expired.',
 'support.chip_tip': '♥ give a tip ♥',
 'support.entitlement': 'Tips of {amount} or more read new chapters up to {days} days early.',
 'about.nav_intro': 'intro',
 'about.nav_legend': 'the legend',
 'about.nav_team': 'the team',
 'about.nav_support': 'support us',
 'about.scroll': 'Scroll down',
 'about.intro_title': 'the interactive adventure of a megalomaniac sheep who wants to make the world dance.',
 'about.legend_title_1': 'yes the legend,',
 'about.legend_title_2': 'is {hero}!',
 'about.team_title_1': 'behind',
 'about.team_title_2': 'the legend',
 'about.support_title_1': 'i love you too',
 'about.support_title_2': 'my friend!',
 'about.chip_contact': 'email us',
 'legal.title': 'Legal Notice & Terms of Use',
 'legal.publisher': 'Website Publisher',
 'legal.hosting': 'Hosting',
 'legal.domains': 'Domains',
 'legal.property': 'Intellectual Property',
 'legal.terms': 'Terms of Use',
 'legal.data': 'Personal Data & Privacy',
 'legal.cookies': 'Cookies & Trackers',
 'legal.law': 'Applicable Law & Jurisdiction',
 'not-found.text': 'Oopsy, page not found',
 'not-found.cta': 'Go back to home',
 'account.heading': 'Your account',
 'account.export': 'download my data',
 'account.delete': 'delete my account',
 'account.sign_in': 'sign in',
 'account.create': 'create an account',
 'account.email': 'email',
 'account.password': 'password',
 'chrome.surprise': 'surprise',
 'chapters.locked_name': '{title}, locked, opens {date}',
 'chapters.locked_plain': '{title}, locked',
 'chapters.timecode_label': 'chapter {number} of {count}',
 'reader.timecode_label': 'panel {number}',
 'reader.announce_loading': 'Chapter {number} is loading.',
 'reader.announce_ready': 'Chapter {number} is ready.',
 'reader.announce_failed': 'Chapter {number} could not be loaded.',
 'reader.end_of_volume': 'last track of the volume, back to chapters',
 'chrome.announce_locale': 'The page is now in English.',
 'about.legend_body': 'Doudou is a megalomaniac sheep, tender and dead set on becoming a DJ. With Jean-Loic, '
                      'a wild barman, and Milan, a future cooking star on socials, he mixes chaos and big '
                      "dreams in a flat full of laughs and late-night noise. It's cool, it's fun, it's "
                      'Doudou Fever.',
 'about.team_dam_title': 'Dam',
 'about.team_dam_body': 'Creative developer and animator, half-coder half-wizard. He animates images, makes '
                        'pixels move, and transforms lines of code into cool and magical experiences.',
 'about.team_ca_title': 'Ca',
 'about.team_ca_body': 'Art director, illustrator and digital brush master. She draws faster than her shadow '
                       'and gives life to each character with style, emotion...',
 'about.support_body': 'Support Doudou on his way to glory and help him become a legend. One day, maybe : a '
                       'printed edition, sweet merch, and Doudou stealing the spotlight!',
 'about.support_hidden': 'Be part of the adventure, or live with this question forever "What if I had helped '
                         'Doudou become a legend?"',
 'about.chip_photogram': 'photogram',
 'about.chip_clipclop': 'clipclop',
 'legal.publisher_body': 'The Doudou Fever website is created and published by Damien Lorca and Camille '
                         'Rouyer.',
 'legal.contact_label': 'Contact email',
 'legal.hosting_body': 'Hosted by Nimbus Edge SAS, 12 rue des Lilas, 75011 Paris, France.',
 'legal.domains_body': 'The domains doudoufever.example, www.doudoufever.example, doudou-fever.example and '
                       'doudoufever-comic.example are registered with Registre Clair SARL, 4 quai du Port, '
                       '13002 Marseille, France.',
 'legal.property_body': 'All content of this website is protected. No licence is granted, and any '
                        'reproduction, distribution, modification or exploitation without prior '
                        'authorisation is prohibited.',
 'legal.terms_body': 'Use of this website is personal. Users agree not to disrupt the site. External links '
                     "such as Tipbox are outside the publisher's responsibility, including for payment "
                     'incidents. The site may be modified or suspended without notice.',
 'legal.data_body': "A reader's address, progress and matched tips are collected only to run the reader "
                    'account. They are never resold, and can be exported, corrected or deleted from the '
                    'account page.',
 'legal.cookies_body': 'The functional keys dd-consent, dd-language, dd-last-chapter, the dd-progress- keys, '
                       'dd-session and dd-studio-session are set whatever the consent decision because they '
                       "only remember the reader's place, language and session. Measurement runs only after "
                       'Accept.',
 'legal.law_body': 'These terms are governed by French law. Any dispute falls under the courts of Paris.'}

CATALOGUE_FR = {'chrome.chapters': 'chapitres',
 'chrome.about': 'a propos',
 'chrome.legal': "mentions legales & conditions d'utilisation",
 'chrome.byline': 'par Camille Rouyer et Damien Lorca',
 'chrome.fullscreen_enter': 'plein ecran',
 'chrome.fullscreen_exit': 'quitter le plein ecran',
 'index.button': 'lire maintenant',
 'index.credit': 'Par Damien Lorca & Camille Rouyer',
 'chapters.heading': 'choisis un chapitre',
 'chapters.tip': 'soutiens-nous',
 'chapters.next_track': 'piste suivante',
 'reader.loading': 'La piste suivante arrive...',
 'reader.text_mode': 'lire en texte',
 'reader.previous_panel': 'case precedente',
 'reader.next_panel': 'case suivante',
 'reader.progress': 'progression du chapitre',
 'reader.load_failed': 'Il manque quelque chose. On reessaie ?',
 'reader.retry': 'reessayer',
 'reader.back': 'retour aux chapitres',
 'locked.timing': 'Ce chapitre sort le {date}.',
 'locked.drawing': 'Ce chapitre est encore en dessin.',
 'locked.notify': 'previens-moi',
 'locked.support': "Les soutiens le lisent des qu'il est fini.",
 'consent.message': 'Coucou ✨ Ce site utilise des cookies pour mesurer la frequentation.',
 'consent.accept': 'Accepter',
 'consent.decline': 'Refuser',
 'support.granted': 'Merci. Ton acces anticipe est actif.',
 'support.sign_in': "Merci. Connecte-toi et nous l'ajouterons a ton compte.",
 'support.below_threshold': 'Merci. Chaque pourboire aide, et celui-ci part droit dans le prochain chapitre.',
 'support.pending': 'Merci. Ton pourboire est en route.',
 'support.expired': 'Ce lien de remerciement a expire.',
 'support.chip_tip': '♥ laisse un pourboire ♥',
 'support.entitlement': "Les pourboires de {amount} ou plus lisent les nouveaux chapitres jusqu'a {days} "
                        'jours plus tot.',
 'about.nav_intro': 'intro',
 'about.nav_legend': 'la legende',
 'about.nav_team': "l'equipe",
 'about.nav_support': 'soutiens-nous',
 'about.scroll': 'Descends',
 'about.intro_title': "l'aventure interactive d'un mouton megalomane qui veut faire danser le monde.",
 'about.legend_title_1': 'oui la legende,',
 'about.legend_title_2': "c'est {hero} !",
 'about.team_title_1': 'derriere',
 'about.team_title_2': 'la legende',
 'about.support_title_1': "moi aussi je t'aime",
 'about.support_title_2': 'mon ami !',
 'about.chip_contact': 'ecris-nous',
 'legal.title': "Mentions legales & conditions d'utilisation",
 'legal.publisher': 'Editeur du site',
 'legal.hosting': 'Hebergement',
 'legal.domains': 'Domaines',
 'legal.property': 'Propriete intellectuelle',
 'legal.terms': "Conditions d'utilisation",
 'legal.data': 'Donnees personnelles & vie privee',
 'legal.cookies': 'Cookies & traceurs',
 'legal.law': 'Droit applicable & juridiction',
 'not-found.text': 'Oups, page introuvable',
 'not-found.cta': "Retour a l'accueil",
 'account.heading': 'Ton compte',
 'account.export': 'telecharger mes donnees',
 'account.delete': 'supprimer mon compte',
 'account.sign_in': 'se connecter',
 'account.create': 'creer un compte',
 'account.email': 'e-mail',
 'account.password': 'mot de passe',
 'chrome.surprise': 'surprise',
 'chapters.locked_name': '{title}, verrouille, sort le {date}',
 'chapters.locked_plain': '{title}, verrouille',
 'chapters.timecode_label': 'chapitre {number} sur {count}',
 'reader.timecode_label': 'case {number}',
 'reader.announce_loading': 'Le chapitre {number} arrive.',
 'reader.announce_ready': 'Le chapitre {number} est pret.',
 'reader.announce_failed': "Le chapitre {number} n'a pas pu etre charge.",
 'reader.end_of_volume': 'derniere piste du volume, retour aux chapitres',
 'chrome.announce_locale': 'La page est maintenant en francais.',
 'about.legend_body': 'Doudou est un mouton megalomane, tendre et bien decide a devenir DJ. Avec Jean-Loic, '
                      'un barman dechaine, et Milan, future star de la cuisine sur les reseaux, il melange '
                      "chaos et grands reves dans un appart plein de rires et de bruit tard le soir. C'est "
                      "cool, c'est drole, c'est Doudou Fever.",
 'about.team_dam_title': 'Dam',
 'about.team_dam_body': 'Developpeur creatif et animateur, moitie codeur moitie sorcier. Il anime les '
                        'images, fait bouger les pixels et transforme des lignes de code en experiences cool '
                        'et magiques.',
 'about.team_ca_title': 'Ca',
 'about.team_ca_body': 'Directrice artistique, illustratrice et maitresse du pinceau numerique. Elle dessine '
                       'plus vite que son ombre et donne vie a chaque personnage avec style, emotion...',
 'about.support_body': 'Soutiens Doudou sur le chemin de la gloire et aide-le a devenir une legende. Un '
                       'jour, peut-etre : une edition imprimee, du merch trop mignon, et Doudou sous les '
                       'projecteurs !',
 'about.support_hidden': 'Fais partie de l\'aventure, ou vis pour toujours avec cette question "Et si '
                         'j\'avais aide Doudou a devenir une legende ?"',
 'about.chip_photogram': 'photogram',
 'about.chip_clipclop': 'clipclop',
 'legal.publisher_body': 'Le site Doudou Fever est cree et publie par Damien Lorca et Camille Rouyer.',
 'legal.contact_label': 'E-mail de contact',
 'legal.hosting_body': 'Heberge par Nimbus Edge SAS, 12 rue des Lilas, 75011 Paris, France.',
 'legal.domains_body': 'Les domaines doudoufever.example, www.doudoufever.example, doudou-fever.example et '
                       'doudoufever-comic.example sont enregistres aupres de Registre Clair SARL, 4 quai du '
                       'Port, 13002 Marseille, France.',
 'legal.property_body': "Tout le contenu de ce site est protege. Aucune licence n'est accordee, et toute "
                        'reproduction, diffusion, modification ou exploitation sans autorisation prealable '
                        'est interdite.',
 'legal.terms_body': "L'utilisation de ce site est personnelle. Les utilisateurs s'engagent a ne pas "
                     'perturber le site. Les liens externes comme Tipbox ne relevent pas de la '
                     "responsabilite de l'editeur, y compris pour les incidents de paiement. Le site peut "
                     'etre modifie ou suspendu sans preavis.',
 'legal.data_body': "L'adresse, la progression et les pourboires rattaches d'un lecteur sont collectes "
                    'uniquement pour faire fonctionner le compte lecteur. Ils ne sont jamais revendus et '
                    'peuvent etre exportes, corriges ou supprimes depuis la page du compte.',
 'legal.cookies_body': 'Les cles fonctionnelles dd-consent, dd-language, dd-last-chapter, les cles '
                       'dd-progress-, dd-session et dd-studio-session sont posees quel que soit le choix de '
                       'consentement car elles retiennent seulement la place, la langue et la session du '
                       "lecteur. La mesure ne demarre qu'apres Accepter.",
 'legal.law_body': 'Ces conditions sont regies par le droit francais. Tout litige releve des tribunaux de '
                   'Paris.'}

CHAPTER_TITLES = {1: ('welcome to Varny', 'bonjour Varny'),
 2: ('under pressure', 'sous pression'),
 3: ("sheep don't sleep", 'moutons insomniaques'),
 4: ('scratch that !', 'on efface tout !'),
 5: ('wow ...', 'ouf ...'),
 6: ('the big mix', 'le grand mix')}

CHAPTER_STATES = {1: 'published', 2: 'published', 3: 'published', 4: 'scheduled', 5: 'scheduled', 6: 'draft'}

CHAPTER_DESCRIPTIONS = {1: ('Doudou arrives in Varny with a suitcase full of records.',
     'Doudou arrive a Varny avec une valise pleine de disques.'),
 2: ('The first gig goes wrong in every possible way.',
     'Le premier concert tourne mal de toutes les facons.'),
 3: ('A night without sleep before the big audition.', 'Une nuit blanche avant la grande audition.'),
 4: ('Doudou erases the whole set and starts again.', 'Doudou efface tout le set et recommence.'),
 5: ('The crowd finally dances.', 'La foule danse enfin.'),
 6: ('Jean-Loic and Milan plan the biggest party in Varny.',
     'Jean-Loic et Milan preparent la plus grande fete de Varny.')}

PANEL_DESCRIPTIONS = {(1, 1, 1): ('Doudou steps off the night bus into Varny.', 'Doudou descend du bus de nuit a Varny.'),
 (1, 1, 2): ('The flat above the bar is small and loud.',
             "L'appartement au-dessus du bar est petit et bruyant."),
 (1, 1, 3): ('Jean-Loic hands Doudou a key and a warning.',
             'Jean-Loic donne a Doudou une cle et un avertissement.'),
 (1, 2, 1): ('Milan films dinner for her followers.', 'Milan filme le diner pour ses abonnes.'),
 (1, 2, 2): ('Doudou unpacks the turntables on the kitchen table.',
             'Doudou deballe les platines sur la table de la cuisine.'),
 (2, 1, 1): ('The speakers crackle before the first song.',
             'Les enceintes gresillent avant le premier morceau.'),
 (2, 1, 2): ('Nobody on the dance floor moves.', 'Personne ne bouge sur la piste.'),
 (2, 1, 3): ('Doudou pulls the plug in a panic.', 'Doudou debranche tout en panique.'),
 (3, 1, 1): ('Doudou counts beats instead of sheep.', 'Doudou compte des temps au lieu des moutons.'),
 (3, 1, 2): ('Milan brings midnight pancakes.', 'Milan apporte des crepes de minuit.'),
 (3, 1, 3): ('The sun rises over an unfinished mix.', 'Le soleil se leve sur un mix inacheve.'),
 (4, 1, 1): ('Doudou deletes every track on the laptop.', "Doudou efface chaque morceau de l'ordinateur."),
 (4, 1, 2): ('Jean-Loic hums a tune from the bar.', 'Jean-Loic fredonne un air du bar.'),
 (4, 1, 3): ('A new beat starts with that tune.', 'Un nouveau rythme nait de cet air.'),
 (5, 1, 1): ('The whole town queues outside the bar.', 'Toute la ville fait la queue devant le bar.'),
 (5, 1, 2): ('Doudou drops the first beat.', 'Doudou lance le premier rythme.'),
 (5, 1, 3): ('Varny dances until morning.', "Varny danse jusqu'au matin."),
 (6, 1, 1): ('Posters for the big mix cover the flat.', "Les affiches du grand mix couvrent l'appartement.")}

PAGE_META_EN = {'/': ('Doudou Fever - Interactive Comic',
       'Doudou Fever is an interactive comic. Follow the adventure of a megalomaniac sheep who wants to make '
       'the world dance. Created by Camille Rouyer & Damien Lorca.'),
 '/chapters': ('Chapters | Doudou Fever - Interactive Comic',
               'Pick a track from the Doudou Fever record rack and start reading.'),
 '/chapter/1': ('Chapter #1: Welcome To Varny - Doudou Fever - Interactive Comic',
                'Read chapter 1, welcome to Varny, of the Doudou Fever interactive comic.'),
 '/about': ('About | Doudou Fever - Interactive Comic',
            'Meet Doudou, the sheep who wants to make the world dance, and the two people who draw and '
            'animate him.'),
 '/legal': ('Legal Notice and Terms of Use | Doudou Fever - Interactive Comic',
            'Publisher, hosting, rights, terms, personal data and cookies for the Doudou Fever website.'),
 '/support/return': ('Thank You | Doudou Fever - Interactive Comic', 'Thanks for tipping Doudou Fever.'),
 '/account': ('Your Account | Doudou Fever - Interactive Comic', 'Your Doudou Fever reading account.'),
 'not-found': ('Page Not Found | Doudou Fever - Interactive Comic',
               'This page of Doudou Fever does not exist.')}

PAGE_META_FR = {'/fr': ('Doudou Fever - BD interactive',
         "Doudou Fever est une BD interactive. Suis l'aventure d'un mouton megalomane qui veut faire danser "
         'le monde. Creee par Camille Rouyer & Damien Lorca.'),
 '/fr/chapters': ('Chapitres | Doudou Fever - BD interactive',
                  'Choisis une piste dans le bac a disques de Doudou Fever et commence a lire.'),
 '/fr/chapter/1': ('Chapitre #1 : Bonjour Varny - Doudou Fever - BD interactive',
                   'Lis le chapitre 1, bonjour Varny, de la BD interactive Doudou Fever.'),
 '/fr/about': ('A propos | Doudou Fever - BD interactive',
               'Rencontre Doudou, le mouton qui veut faire danser le monde, et les deux personnes qui le '
               "dessinent et l'animent."),
 '/fr/legal': ("Mentions legales et conditions d'utilisation | Doudou Fever - BD interactive",
               'Editeur, hebergement, droits, conditions, donnees personnelles et cookies du site Doudou '
               'Fever.'),
 '/fr/support/return': ('Merci | Doudou Fever - BD interactive', "Merci d'avoir soutenu Doudou Fever."),
 '/fr/account': ('Ton compte | Doudou Fever - BD interactive', 'Ton compte de lecture Doudou Fever.'),
 'not-found': ('Page introuvable | Doudou Fever - BD interactive',
               "Cette page de Doudou Fever n'existe pas.")}
