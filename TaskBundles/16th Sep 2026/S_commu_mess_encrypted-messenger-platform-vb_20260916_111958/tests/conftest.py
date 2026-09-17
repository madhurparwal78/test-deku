"""Fixtures, pinned literals and helpers for deku/encrypted-messenger-platform-vb.

Black box only: the app is reached at APP_PUBLIC_URL, its HTTP API under /api, its
database through the verifier-only DB_ADMIN_URL capability adapter and its mail
through the verifier-only EMAIL_INBOX_API_URL. Every literal below is pinned in
instruction.md. Tests create their own accounts with unique per-run identifiers,
so the browser journeys that use the seeded accounts never collide with them.
"""

from __future__ import annotations

import base64
import json
import os
import re
import time
import uuid

import httpx
import pytest
from appclient import app_url
from capabilities import make_backend

SEEDED_PASSWORD = "deku-demo-pw-2026"
SEED_ACCOUNTS = {
    "user@example.com": "nova",
    "user2@example.com": "juniper",
    "user3@example.com": "sol",
    "user4@example.com": "wren",
}
NUDGE_SUBJECT = "You have something waiting on Beacon"
NUDGE_BODY = "Open Beacon to read what is waiting for you."
RECEIPT_SUBJECT = "Thank you for supporting Beacon"
FOUNDATION = "Beacon Technology Foundation"
MAIL_FROM = "no-reply@beacon.example.org"
DECRYPT_NOTICE = "A message could not be verified and was not shown"
UNLINKED_BANNER = "This browser was unlinked"
GROUP_UNAVAILABLE = "This group is not available"
EMPTY_CHATS = "No conversations yet"
STATUSES = ("Sending", "Sent", "Delivered", "Read")
TIMER_VALUES = ("off", "30s", "5m", "1h", "1d", "1w")
FONT_STACK = "Inter, SF Pro, Segoe UI, Roboto, Oxygen, Ubuntu, Helvetica Neue, Helvetica, Arial, sans-serif"
LOCALES = {
    "af": "Afrikaans", "ar": "العربية", "az": "Azərbaycan dili", "bg": "Български",
    "bn": "বাংলা", "bs": "Bosanski", "ca": "Català", "cs": "Čeština", "da": "Dansk",
    "de": "Deutsch", "el": "Ελληνικά",
}
LANGUAGE_NAMES = ("English", "Afrikaans", "العربية", "Azərbaycan dili", "Български", "বাংলা",
                  "Bosanski", "Català", "Čeština", "Dansk", "Deutsch", "Ελληνικά")
DECLARED_PAGES = ("/get", "/help", "/blog", "/developers", "/careers", "/brand")
PUBLIC_ROUTES = ("/", "/af", "/ar", "/az", "/bg", "/bn", "/bs", "/ca", "/cs", "/da", "/de", "/el",
                 "/get", "/help", "/blog", "/developers", "/careers", "/donate", "/terms", "/brand")
HERO_LEAD = ("Say \"hello\" to a different messaging experience. An unexpected focus on privacy, "
             "combined with all of the features you expect.")
TOP_BAR_LINKS = ("Get Beacon", "Help", "Blog", "Developers", "Careers", "Donate")
FOOTER_COLUMNS = {
    "Organization": ("Donate", "Careers", "Blog", "Brand Assets", "Terms & Privacy Policy"),
    "Download": ("Android", "iPhone & iPad", "Windows", "Mac", "Linux"),
    "Social": ("Bluesky", "GitHub", "Instagram", "Mastodon", "X"),
    "Help": ("Support Center", "Community"),
}
COPY_DECK = (
    "Select your language",
    "Speak Freely",
    HERO_LEAD,
    "Get Beacon",
    "Why use Beacon?",
    "Explore below to see why Beacon is a simple, powerful, and secure messenger",
    "Share Without Insecurity",
    "State-of-the-art end-to-end encryption (powered by the open source Beacon Protocol) keeps your "
    "conversations secure. We can't read your messages or listen to your calls, and no one else can "
    "either. Privacy isn't an optional mode. It's just the way that Beacon works. Every message, "
    "every call, every time.",
    "Say Anything",
    "Share text, voice messages, photos, videos, GIFs and files for free. Beacon uses your phone's "
    "data connection so you can avoid SMS and MMS fees.",
    "Make crystal-clear voice and video calls to people who live across town, or across the ocean, "
    "with no long-distance charges.",
    "Make Privacy Stick",
    "Add a new layer of expression to your conversations with encrypted stickers. You can also create "
    "and share your own sticker packs.",
    "Get Together with Groups",
    "Group chats make it easy to stay connected to your family, friends, and coworkers.",
    "No ads. No trackers. No kidding.",
    "There are no ads, no affiliate marketers, and no creepy tracking in Beacon. So focus on sharing "
    "the moments that matter with the people who matter to you.",
    "Free for Everyone",
    "Beacon is an independent nonprofit. We're not tied to any major tech companies, and we can never "
    "be acquired by one either. Development is supported by grants and donations from people like you.",
    "Donate to Beacon",
    "© 2013-2026 Beacon, a nonprofit.",
    "\"Beacon\", Beacon logos, and other trademarks are trademarks or registered trademarks of Beacon "
    "Technology Foundation in the United States and other countries (more info here).",
    "For media inquiries, contact press@beacon.example.org",
)
PRIVACY_TABLE = (
    "an identifier, a set of published pre-keys, encrypted profile blobs",
    "plaintext names, avatars, or contact lists",
    "opaque encrypted envelopes queued for offline recipients, then deleted",
    "any plaintext message, call audio, or attachment",
    "encrypted group state and routing membership sufficient to fan out",
    "group names, group avatars or readable group content",
    "acknowledgements and contentless push triggers",
    "message content in any push payload",
    "a recovery store the service cannot read, guarded by a ten-guess limit",
    "the user's recovery secret",
    "the donor's email and the amount",
    "card details of any kind",
)
SETTLE_SECONDS = 3.0
UI_TIMEOUT = 30.0
DESKTOP = {"width": 1280, "height": 900}
PHONE = {"width": 375, "height": 812}
TABLET = {"width": 900, "height": 1100}
LAPTOP = {"width": 1100, "height": 800}
FULL_HD = {"width": 1920, "height": 1080}
LIVE_CONTEXTS: list = []
GUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
B64_TOKEN_RE = re.compile(r"[A-Za-z0-9+/_-]{16,}={0,2}")


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The only sanctioned sleep: gives an asynchronous side effect a fair chance while open pages keep being served."""
    pages = [p for c in LIVE_CONTEXTS for p in c.pages if not p.is_closed()]
    if pages:
        pages[0].wait_for_timeout(seconds * 1000)
    else:
        time.sleep(seconds)


def wait_until(check, timeout: float = UI_TIMEOUT, interval: float = 0.5):
    """Poll `check` to a monotonic deadline; return its first truthy value or the last value."""
    deadline = time.monotonic() + timeout
    value = check()
    while not value and time.monotonic() < deadline:
        settle(interval)
        value = check()
    return value


def pump(tab, seconds: float = SETTLE_SECONDS) -> None:
    """A wait that keeps serving this page's routed requests while it runs."""
    tab.wait_for_timeout(seconds * 1000)


def token_hex(n: int = 4) -> str:
    return os.urandom(n).hex()


def new_email(tag: str) -> str:
    return f"{tag}-{token_hex()}@example.com"


def new_username(tag: str) -> str:
    return f"{tag[:8]}_{token_hex()}"


def new_guid() -> str:
    return str(uuid.uuid4())


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def random_ciphertext(size: int = 96) -> str:
    return b64(os.urandom(size))


def client(headers: dict | None = None, follow: bool = False) -> httpx.Client:
    return httpx.Client(base_url=app_url(), timeout=30.0, headers=headers or {}, follow_redirects=follow)


def bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def body_of(response: httpx.Response) -> str:
    return response.text[:400]


def is_client_error(response: httpx.Response) -> bool:
    return 400 <= response.status_code < 500


def ok(response: httpx.Response) -> bool:
    return 200 <= response.status_code < 300


def signup(email: str, username: str, password: str) -> httpx.Response:
    with client() as c:
        return c.post("/api/auth/signup", json={"email": email, "username": username, "password": password})


def login(email: str, password: str) -> httpx.Response:
    with client() as c:
        return c.post("/api/auth/login", json={"email": email, "password": password})


def account_token(email: str, password: str) -> str:
    r = login(email, password)
    assert r.status_code == 200, f"POST /api/auth/login for {email} returned {r.status_code}: {body_of(r)}"
    token = r.json().get("access_token")
    assert token, f"POST /api/auth/login for {email} carried no access_token: {body_of(r)}"
    return token


def key_material(one_time: int = 5, first_key_id: int = 1) -> dict:
    return {
        "identity_key": b64(os.urandom(32)),
        "signed_prekey": {"key_id": 7001, "public_key": b64(os.urandom(32)), "signature": b64(os.urandom(64))},
        "pq_prekey": {"key_id": 7002, "public_key": b64(os.urandom(1184)), "signature": b64(os.urandom(64))},
        "one_time_prekeys": [{"key_id": first_key_id + i, "public_key": b64(os.urandom(32))}
                             for i in range(one_time)],
    }


def register_device_raw(token: str, body: dict) -> httpx.Response:
    with client(bearer(token)) as c:
        return c.post("/api/devices", json=body)


def register_device(token: str, one_time: int = 5, **extra) -> dict:
    body = key_material(one_time)
    body.update(extra)
    r = register_device_raw(token, body)
    assert r.status_code in (200, 201), f"POST /api/devices returned {r.status_code}: {body_of(r)}"
    data = r.json()
    assert isinstance(data.get("device_id"), int) and data.get("device_token"), (
        f"POST /api/devices must return device_id and device_token: {body_of(r)}")
    return {"device_id": data["device_id"], "token": data["device_token"], "keys": body}


class Person:
    """One freshly signed-up account with its devices, access key and inbox address."""

    def __init__(self, tag: str, one_time: int = 5, publish_profile: bool = True):
        self.email = new_email(tag)
        self.username = new_username(tag)
        self.password = f"pw-{token_hex(6)}-beacon"
        r = signup(self.email, self.username, self.password)
        assert r.status_code in (200, 201), f"POST /api/auth/signup returned {r.status_code}: {body_of(r)}"
        self.account = account_token(self.email, self.password)
        first = register_device(self.account, one_time=one_time)
        self.devices = [first]
        self.access_key = b64(os.urandom(16))
        self.profile_ciphertext = random_ciphertext(48)
        if publish_profile:
            with client(bearer(first["token"])) as c:
                pr = c.put("/api/profile", json={"profile_ciphertext": self.profile_ciphertext,
                                                  "access_key": self.access_key})
            assert pr.status_code in (200, 201, 204), f"PUT /api/profile returned {pr.status_code}: {body_of(pr)}"

    @property
    def token(self) -> str:
        return self.devices[0]["token"]

    def link_device(self, one_time: int = 5) -> dict:
        with client(bearer(self.token)) as c:
            r = c.post("/api/devices/link-codes")
        assert r.status_code in (200, 201), f"POST /api/devices/link-codes returned {r.status_code}: {body_of(r)}"
        device = register_device(self.account, one_time=one_time, link_code=r.json()["code"])
        self.devices.append(device)
        return device


def sealed_send(username: str, access_key: str | None, messages: list) -> httpx.Response:
    headers = {"Unidentified-Access-Key": access_key} if access_key else {}
    with client(headers) as c:
        return c.put(f"/api/messages/{username}", json={"messages": messages})


def device_send(token: str, username: str, messages: list) -> httpx.Response:
    with client(bearer(token)) as c:
        return c.put(f"/api/messages/{username}", json={"messages": messages})


def entry(device_id: int, guid: str | None = None, ciphertext: str | None = None) -> dict:
    return {"device_id": device_id, "guid": guid or new_guid(), "ciphertext": ciphertext or random_ciphertext()}


def fetch(token: str) -> list:
    with client(bearer(token)) as c:
        r = c.get("/api/messages")
    assert r.status_code == 200, f"GET /api/messages returned {r.status_code}: {body_of(r)}"
    data = r.json()
    assert isinstance(data, list), f"GET /api/messages must return a top-level JSON array: {body_of(r)}"
    return data


def ack(token: str, guid: str) -> httpx.Response:
    with client(bearer(token)) as c:
        return c.delete(f"/api/messages/{guid}")


def bundle(token: str, username: str) -> httpx.Response:
    with client(bearer(token)) as c:
        return c.get(f"/api/keys/{username}")


@pytest.fixture(scope="session")
def backend():
    return make_backend()


def all_row_text(backend) -> list[str]:
    """Every row of every application table, rendered as text."""
    tables = backend.query(
        "SELECT table_schema, table_name FROM information_schema.tables "
        "WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema')")
    out = []
    for t in tables:
        sql = 'SELECT t::text AS row_text FROM "{}"."{}" t'.format(
            t["table_schema"].replace('"', '""'), t["table_name"].replace('"', '""'))
        out.extend(r["row_text"] for r in backend.query(sql))
    return out


def rows_containing(backend, needle: str) -> list[str]:
    return [row for row in all_row_text(backend) if needle in row]


def rows_holding(backend, ciphertext: str) -> list[str]:
    """Rows carrying a base64 ciphertext, stored either as that text or as its bytes."""
    raw_hex = base64.b64decode(ciphertext).hex()
    return [row for row in all_row_text(backend) if ciphertext in row or raw_hex in row]


def fresh_account(tag: str) -> dict:
    """A signed-up account with no device yet, for journeys a browser registers itself."""
    account = {"email": new_email(tag), "username": new_username(tag), "password": f"pw-{token_hex(6)}-beacon"}
    r = signup(account["email"], account["username"], account["password"])
    assert r.status_code in (200, 201), f"POST /api/auth/signup returned {r.status_code}: {body_of(r)}"
    return account


def leaks_bytes(blob: str | bytes, data: bytes) -> bool:
    """True when raw `data` is readable in `blob` as bytes, base64 or hex."""
    if isinstance(blob, bytes) and data in blob:
        return True
    text = blob.decode("latin-1") if isinstance(blob, bytes) else blob
    if base64.b64encode(data).decode() in text or data.hex() in text:
        return True
    return any(data in chunk for chunk in decoded_blobs(text))


def encodings(text: str) -> set[str]:
    raw = text.encode("utf-8")
    std = base64.b64encode(raw).decode()
    url = base64.urlsafe_b64encode(raw).decode()
    return {text, std, std.rstrip("="), url, url.rstrip("="), raw.hex()}


STD_B64_RE = re.compile(r"^[A-Za-z0-9+/]+={0,2}$")
URL_B64_RE = re.compile(r"^[A-Za-z0-9_-]+={0,2}$")


def decoded_blobs(blob: str) -> list[bytes]:
    """Every base64-looking token inside `blob`, decoded where it is well formed."""
    out = []
    for token in B64_TOKEN_RE.findall(blob):
        padded = token + "=" * (-len(token) % 4)
        if len(padded) % 4 or "=" in padded.rstrip("="):
            continue
        if STD_B64_RE.fullmatch(padded):
            out.append(base64.b64decode(padded))
        elif URL_B64_RE.fullmatch(padded):
            out.append(base64.urlsafe_b64decode(padded))
    return out


def leaks(blob: str | bytes, secret: str) -> bool:
    """True when `secret` is readable in `blob`, raw or through a common encoding."""
    text = blob.decode("latin-1") if isinstance(blob, bytes) else blob
    if any(form in text for form in encodings(secret)):
        return True
    raw = secret.encode("utf-8")
    return any(raw in chunk for chunk in decoded_blobs(text))


INBOX_API = "/".join(("", "api", "v1"))


def inbox_base() -> str:
    return os.environ["EMAIL_INBOX_API_URL"].rstrip("/") + INBOX_API


def mail_summaries() -> list[dict]:
    r = httpx.get(inbox_base() + "/messages", params={"limit": 1000}, timeout=30.0)
    assert r.status_code == 200, f"mail inbox listing returned {r.status_code}: {body_of(r)}"
    return r.json().get("messages", [])


def mail_detail(message_id: str) -> dict:
    r = httpx.get(inbox_base() + "/message/" + message_id, timeout=30.0)
    assert r.status_code == 200, f"mail inbox message {message_id} returned {r.status_code}: {body_of(r)}"
    return r.json()


def _addresses(people) -> list[str]:
    return [p.get("Address", "").lower() for p in (people or [])]


def mails_to(address: str) -> list[dict]:
    """Full messages whose To, Cc or Bcc carries `address`."""
    target = address.lower()
    hits = []
    for summary in mail_summaries():
        involved = _addresses(summary.get("To")) + _addresses(summary.get("Cc")) + _addresses(summary.get("Bcc"))
        if target in involved:
            hits.append(mail_detail(summary["ID"]))
    return hits


def wait_for_mail(address: str, count: int = 1, timeout: float = 45.0) -> list[dict]:
    wait_until(lambda: len(mails_to(address)) >= count, timeout=timeout, interval=1.0)
    return mails_to(address)


def mail_text(message: dict) -> str:
    return "\n".join([message.get("Subject", ""), message.get("Text", ""), message.get("HTML", "")])


def relative_luminance(rgb: tuple) -> float:
    def channel(v):
        c = v / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb[:3]
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(fg: tuple, bg: tuple) -> float:
    lighter, darker = sorted((relative_luminance(fg), relative_luminance(bg)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def parse_rgb(value: str) -> tuple:
    nums = [float(x) for x in re.findall(r"[\d.]+", value)]
    return tuple(nums[:4]) if len(nums) >= 4 else tuple(nums[:3]) + (1.0,)


def normalise_quotes(text: str) -> str:
    return (text.replace("’", "'").replace("‘", "'").replace("“", '"')
            .replace("”", '"').replace(" ", " "))


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", normalise_quotes(text)).strip()


FAKE_MEDIA_ARGS = ("--use-fake-ui-for-media-stream", "--use-fake-device-for-media-stream",
                   "--autoplay-policy=no-user-gesture-required")


@pytest.fixture(scope="session")
def chromium():
    from playwright.sync_api import sync_playwright
    manager = sync_playwright().start()
    browser = manager.chromium.launch(args=list(FAKE_MEDIA_ARGS))
    yield browser
    browser.close()
    manager.stop()


class Capture:
    """Everything one browser context sends: request URLs, bodies and socket frames."""

    def __init__(self, context):
        self.requests = []
        self.frames = []
        context.on("request", self._on_request)
        context.on("page", self._on_page)

    def _on_page(self, page):
        page.on("websocket", self._on_socket)

    def _on_socket(self, socket):
        socket.on("framesent", self._on_frame)

    def _on_frame(self, payload):
        self.frames.append(payload if isinstance(payload, (str, bytes)) else str(payload))

    def _on_request(self, request):
        self.requests.append({
            "url": request.url,
            "method": request.method,
            "headers": dict(request.headers),
            "body": request.post_data_buffer or b"",
        })

    def blobs(self):
        for req in self.requests:
            yield req["url"]
            yield req["body"]
            for value in req["headers"].values():
                yield value
        for frame in self.frames:
            yield frame

    def leaked(self, secret: str) -> bool:
        return any(leaks(blob, secret) for blob in self.blobs())


class Browsers:
    """Independent browser contexts, one per person or per browser a person uses."""

    def __init__(self, chromium):
        self._chromium = chromium
        self.contexts = []

    def open(self, viewport: dict | None = None, reduced_motion: str | None = None, color_scheme: str | None = None):
        options = {"viewport": viewport or DESKTOP, "base_url": app_url(), "permissions": ["microphone", "camera"]}
        if reduced_motion:
            options["reduced_motion"] = reduced_motion
        if color_scheme:
            options["color_scheme"] = color_scheme
        context = self._chromium.new_context(**options)
        context.set_default_timeout(UI_TIMEOUT * 1000)
        capture = Capture(context)
        self.contexts.append(context)
        LIVE_CONTEXTS.append(context)
        return context, capture

    def close(self):
        for context in self.contexts:
            if context in LIVE_CONTEXTS:
                LIVE_CONTEXTS.remove(context)
            context.close()


@pytest.fixture
def browser_page(chromium):
    browsers = Browsers(chromium)
    yield browsers
    browsers.close()


@pytest.fixture
def page(chromium):
    context = chromium.new_context(viewport=DESKTOP, base_url=app_url())
    context.set_default_timeout(UI_TIMEOUT * 1000)
    LIVE_CONTEXTS.append(context)
    tab = context.new_page()
    yield tab
    LIVE_CONTEXTS.remove(context)
    context.close()


def by_testid(tab, name: str):
    return tab.locator(f'[data-testid="{name}"]')


def visible_testid(tab, names) -> bool:
    names = (names,) if isinstance(names, str) else tuple(names)
    for name in names:
        found = by_testid(tab, name)
        if found.count() and found.first.is_visible():
            return True
    return False


def path_of(tab) -> str:
    return tab.evaluate("() => location.pathname")


def ensure_unlocked(tab, password: str, landmark=None, timeout: float = 15.0) -> None:
    """Unlock when the page asks for the account password; return once the unlock form or the landmark settles."""
    deadline = time.monotonic() + timeout
    quiet_until = time.monotonic() + 4.0
    while time.monotonic() < deadline:
        form = by_testid(tab, "unlock-password")
        if (form.count() and form.first.is_visible()) or path_of(tab).startswith("/unlock"):
            form.first.wait_for(state="visible")
            form.first.fill(password)
            by_testid(tab, "unlock-submit").first.click()
            tab.wait_for_function("() => !location.pathname.startsWith('/unlock')", timeout=UI_TIMEOUT * 1000)
            if landmark:
                wait_until(lambda: visible_testid(tab, landmark), UI_TIMEOUT)
            return
        if landmark and visible_testid(tab, landmark):
            return
        if not landmark and time.monotonic() > quiet_until:
            return
        tab.wait_for_timeout(250)


def ui_login(tab, email: str, password: str) -> None:
    tab.goto("/login")
    by_testid(tab, "login-email").first.fill(email)
    by_testid(tab, "login-password").first.fill(password)
    by_testid(tab, "login-submit").first.click()
    tab.wait_for_url(re.compile(r"/(chats|link|unlock)(/|\?|#|$)"), timeout=UI_TIMEOUT * 1000)
    ensure_unlocked(tab, password, ("new-chat", "link-code-input", "conversation-row"))


def open_chat(tab, username: str, password: str) -> None:
    tab.goto(f"/chats/{username}")
    ensure_unlocked(tab, password, ("composer-input", "identity-change-banner"))
    assert wait_until(lambda: visible_testid(tab, ("composer-input", "identity-change-banner")), UI_TIMEOUT), \
        f"/chats/{username} showed neither a composer nor an identity warning"


def wait_sent(tab, text: str, timeout: float = UI_TIMEOUT) -> str:
    return wait_until(lambda: bubble_status(tab, text) if bubble_status(tab, text) in STATUSES[1:] else "",
                      timeout=timeout)


def ui_set_profile_name(tab, name: str, password: str) -> None:
    tab.goto("/settings/profile")
    ensure_unlocked(tab, password, "profile-name-input")
    by_testid(tab, "profile-name-input").first.fill(name)
    with tab.expect_response(lambda r: r.request.method == "PUT" and r.url.split("?")[0].endswith("/api/profile"), timeout=UI_TIMEOUT * 1000):
        by_testid(tab, "profile-save").first.click()


def put_requests_to(capture: Capture, username: str) -> list[dict]:
    suffix = f"/api/messages/{username}"
    return [r for r in capture.requests if r["method"] == "PUT" and r["url"].split("?")[0].endswith(suffix)]


def sent_guids(capture: Capture, username: str, since: int = 0) -> list[str]:
    guids = []
    for request in put_requests_to(capture, username)[since:]:
        payload = json.loads(request["body"] or b"{}")
        guids.extend(m.get("guid") for m in payload.get("messages", []))
    return guids


def sent_ciphertexts(capture: Capture, username: str, since: int = 0) -> list[str]:
    out = []
    for request in put_requests_to(capture, username)[since:]:
        payload = json.loads(request["body"] or b"{}")
        out.extend(m.get("ciphertext") for m in payload.get("messages", []))
    return out


def send_text(tab, text: str) -> None:
    by_testid(tab, "composer-input").fill(text)
    by_testid(tab, "composer-send").click()


def bubble(tab, text: str, direction: str | None = None):
    selector = '[data-testid="message-bubble"]'
    if direction:
        selector += f'[data-direction="{direction}"]'
    return tab.locator(selector).filter(has_text=text)


def bubble_status(tab, text: str) -> str:
    target = bubble(tab, text, "out")
    if not target.count():
        return ""
    status = target.first.locator('[data-testid="message-status"]')
    return status.first.inner_text().strip() if status.count() else ""


def message_texts(tab) -> list[str]:
    """Message texts in on-screen order, top to bottom."""
    return tab.evaluate("""() => Array.from(document.querySelectorAll('[data-testid="message-text"]'))
      .map(e => [e.getBoundingClientRect().top, (e.innerText || '').trim()])
      .sort((a, b) => a[0] - b[0]).map(x => x[1])""")


def safety_digits(tab, username: str, password: str) -> str:
    tab.goto(f"/chats/{username}/safety")
    ensure_unlocked(tab, password, "safety-number")
    by_testid(tab, "safety-number").first.wait_for(state="visible")
    return re.sub(r"\D", "", by_testid(tab, "safety-number").first.inner_text())


STORAGE_DUMP_JS = """
async () => {
  const enc = (v, depth) => {
    if (depth > 8 || v === null || v === undefined) return String(v);
    if (typeof v === 'string') return v;
    if (typeof v === 'number' || typeof v === 'boolean') return String(v);
    if (v instanceof ArrayBuffer) return Array.from(new Uint8Array(v)).map(b => String.fromCharCode(b)).join('');
    if (ArrayBuffer.isView(v)) return Array.from(new Uint8Array(v.buffer, v.byteOffset, v.byteLength)).map(b => String.fromCharCode(b)).join('');
    if (v instanceof Blob) return '[blob]';
    if (typeof CryptoKey !== 'undefined' && v instanceof CryptoKey) return '[cryptokey]';
    if (Array.isArray(v)) return v.map(x => enc(x, depth + 1)).join('\\n');
    if (v instanceof Map) return Array.from(v.entries()).map(([k, x]) => enc(k, depth + 1) + '=' + enc(x, depth + 1)).join('\\n');
    if (v instanceof Set) return Array.from(v.values()).map(x => enc(x, depth + 1)).join('\\n');
    if (typeof v === 'object') return Object.keys(v).map(k => k + '=' + enc(v[k], depth + 1)).join('\\n');
    return String(v);
  };
  const parts = [];
  for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); parts.push(k + '=' + localStorage.getItem(k)); }
  for (let i = 0; i < sessionStorage.length; i++) { const k = sessionStorage.key(i); parts.push(k + '=' + sessionStorage.getItem(k)); }
  const dbs = indexedDB.databases ? await indexedDB.databases() : [];
  for (const info of dbs) {
    const db = await new Promise((res, rej) => { const r = indexedDB.open(info.name); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); });
    for (const store of Array.from(db.objectStoreNames)) {
      const values = await new Promise((res, rej) => { const tx = db.transaction(store, 'readonly'); const q = tx.objectStore(store).getAll(); q.onsuccess = () => res(q.result); q.onerror = () => rej(q.error); });
      const keys = await new Promise((res, rej) => { const tx = db.transaction(store, 'readonly'); const q = tx.objectStore(store).getAllKeys(); q.onsuccess = () => res(q.result); q.onerror = () => rej(q.error); });
      parts.push(enc(keys, 0));
      parts.push(enc(values, 0));
    }
    db.close();
  }
  return parts.join('\\n');
}
"""


def storage_dump(tab) -> str:
    return tab.evaluate(STORAGE_DUMP_JS)


def tampered(ciphertext: str) -> str:
    raw = bytearray(base64.b64decode(ciphertext))
    raw[len(raw) // 2] ^= 0x01
    return b64(bytes(raw))


class MessageRoute:
    """Rewrites every GET /api/messages response one page receives, counting the responses it served."""

    def __init__(self, tab, rewrite):
        self.served = 0
        self._rewrite = rewrite
        tab.route(re.compile(r"/api/messages(\?[^/]*)?$"), self._handle)

    def _handle(self, route, request):
        if request.method != "GET":
            route.continue_()
            return
        response = route.fetch()
        payload = json.loads(response.text() or "[]")
        headers = {k: v for k, v in response.headers.items()
                   if k.lower() not in ("content-length", "content-encoding")}
        headers["content-type"] = "application/json"
        self.served += 1
        route.fulfill(status=response.status, body=json.dumps(self._rewrite(payload)), headers=headers)


def route_messages(tab, rewrite) -> MessageRoute:
    return MessageRoute(tab, rewrite)


def run_together(calls: list) -> list:
    """Start every call at the same instant behind a barrier and return their results in order."""
    import threading
    barrier = threading.Barrier(len(calls))
    results = [None] * len(calls)

    def worker(index, fn):
        barrier.wait()
        results[index] = fn()

    threads = [threading.Thread(target=worker, args=(i, fn)) for i, fn in enumerate(calls)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return results


def document_text(raw_html: str) -> str:
    """The readable text of a raw HTML response, before any script runs."""
    import html as htmllib
    body = re.sub(r"<!-{2}.*?-{2}>", " ", raw_html, flags=re.S)
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    return squash(htmllib.unescape(body))


def root_attribute(raw_html: str, name: str) -> str | None:
    match = re.search(r"<html\b([^>]*)>", raw_html, flags=re.I)
    if not match:
        return None
    attr = re.search(rf"\b{name}\s*=\s*[\"']([^\"']*)[\"']", match.group(1), flags=re.I)
    return attr.group(1) if attr else None


def same_origin(url: str, base: str) -> bool:
    from urllib.parse import urlparse
    a, b = urlparse(url), urlparse(base)
    return (a.scheme, a.hostname, a.port or (443 if a.scheme == "https" else 80)) == (
        b.scheme, b.hostname, b.port or (443 if b.scheme == "https" else 80))


def url_path(url: str) -> str:
    from urllib.parse import urlparse
    path = urlparse(url).path or "/"
    return path.rstrip("/") or "/"


def make_png(seed: bytes) -> bytes:
    """A valid 4x4 RGB PNG whose pixels come from `seed`, so its bytes are unique per run."""
    import struct
    import zlib
    pixels = (seed * 16)[:48]
    raw = b"".join(b"\x00" + pixels[row * 12:(row + 1) * 12] for row in range(4))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", 4, 4, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


def create_group(token: str, members: list, state: str | None = None) -> httpx.Response:
    with client(bearer(token)) as c:
        return c.post("/api/groups", json={"encrypted_state": state or random_ciphertext(40), "members": members})


def patch_group(token: str, group_id: str, expected: int, add=None, remove=None, state: str | None = None) -> httpx.Response:
    with client(bearer(token)) as c:
        return c.patch(f"/api/groups/{group_id}", json={
            "expected_revision": expected, "encrypted_state": state or random_ciphertext(40),
            "add": add or [], "remove": remove or []})


def read_group(token: str, group_id: str) -> httpx.Response:
    with client(bearer(token)) as c:
        return c.get(f"/api/groups/{group_id}")


def group_send(token: str, group_id: str, guid: str, ciphertext: str) -> httpx.Response:
    with client(bearer(token)) as c:
        return c.put(f"/api/groups/{group_id}/messages", json={"guid": guid, "ciphertext": ciphertext})


def restore(account: str, verifier: str) -> httpx.Response:
    with client(bearer(account)) as c:
        return c.post("/api/recovery/restore", json={"access_verifier": verifier})


def guids_of(envelopes: list) -> list:
    return [e.get("guid") for e in envelopes]


NORMALISE_COLOUR_JS = """
const toRgba = (c) => {
  const cv = document.createElement('canvas'); cv.width = 1; cv.height = 1;
  const x = cv.getContext('2d'); x.clearRect(0, 0, 1, 1); x.fillStyle = 'rgba(0, 0, 0, 0)'; x.fillStyle = c;
  x.fillRect(0, 0, 1, 1); const d = x.getImageData(0, 0, 1, 1).data;
  return 'rgba(' + d[0] + ', ' + d[1] + ', ' + d[2] + ', ' + (d[3] / 255) + ')';
};
"""

STYLE_OF_TEXT_JS = """
(needle) => {
""" + NORMALISE_COLOUR_JS + """
  const effectiveBg = (el) => {
    for (let node = el; node && node.nodeType === 1; node = node.parentElement) {
      const bg = toRgba(getComputedStyle(node).backgroundColor);
      if (parseFloat(bg.split(',')[3]) > 0) return bg;
    }
    return 'rgba(255, 255, 255, 1)';
  };
  let best = null;
  for (const el of document.querySelectorAll('body *')) {
    if (!el.getClientRects().length) continue;
    const text = (el.textContent || '').replace(/\\s+/g, ' ').trim();
    if (text.includes(needle) && (!best || text.length < best.text.length)) best = { el, text };
  }
  if (!best) return null;
  const cs = getComputedStyle(best.el);
  return { fontSize: cs.fontSize, fontWeight: cs.fontWeight, lineHeight: cs.lineHeight,
           fontFamily: cs.fontFamily, color: toRgba(cs.color), background: effectiveBg(best.el),
           textAlign: cs.textAlign, top: best.el.getBoundingClientRect().top + window.scrollY,
           textRendering: cs.textRendering };
}
"""


def style_of_text(tab, needle: str) -> dict | None:
    return tab.evaluate(STYLE_OF_TEXT_JS, needle)


def transition_seconds(value: str) -> list[float]:
    out = []
    for part in value.split(","):
        part = part.strip()
        if part.endswith("ms"):
            out.append(float(part[:-2]) / 1000.0)
        elif part.endswith("s"):
            out.append(float(part[:-1]))
    return out


ELEMENT_COLOURS_JS = """
(el) => {
""" + NORMALISE_COLOUR_JS + """
  const out = [];
  for (const node of [el, ...el.querySelectorAll('*')]) {
    const cs = getComputedStyle(node);
    for (const prop of ['backgroundColor', 'color', 'borderTopColor', 'borderRightColor', 'borderBottomColor', 'borderLeftColor', 'fill', 'stroke']) {
      const value = cs[prop];
      if (value && value !== 'none') out.push(toRgba(value));
    }
  }
  return out;
}
"""


def element_colours(locator) -> list[tuple]:
    return [parse_rgb(v) for v in locator.evaluate(ELEMENT_COLOURS_JS)]


def hue_chroma(rgb: tuple) -> tuple[float, float]:
    import colorsys
    r, g, b = rgb[:3]
    hue, _, _ = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return hue * 360, (max(r, g, b) - min(r, g, b)) / 255
