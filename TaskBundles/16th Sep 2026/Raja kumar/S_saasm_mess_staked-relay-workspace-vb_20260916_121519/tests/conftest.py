"""Task fixtures for deku/staked-relay-workspace-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout or
module names. The only assumptions are the App Contract and the literals
instruction.md pins: routes, field names, seeded accounts, table and column names,
the watcher public key and the pinned copy.

Wallet and watcher signatures are Ed25519, produced here by a plain RFC 8032
implementation because the verifier image carries no signing library.
"""

from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
import os
import re
import threading
import time

import httpx
import pytest
from appclient import api_base, app_url
from capabilities import Backend, make_backend

TIMEOUT = 30.0
PASSWORD = "deku-demo-pw-2026"
MEMBER_EMAIL = "member@example.com"
MEMBER2_EMAIL = "member2@example.com"
MEMBER3_EMAIL = "member3@example.com"
TREASURER_EMAIL = "treasurer@example.com"
OPERATOR_EMAIL = "member4@example.com"
OPERATOR_CODE = "NJ-OPERATOR"
TREASURER_CODE = "NJ-TREASURY"
PUBLIC_GROUP = "Open Relay Commons"
CHANNEL = "Relay Bulletins"

WATCHER_SEED = bytes.fromhex(
    "3db9d9ca0340e9953b13e20e9c3b6c6617d7bf50723dd2f8d05d9fffa0129b2a")
WATCHER_PUBLIC_KEY = "efe6e71259fd773f94f0a96ae30a706f1a74dc8a5fd275b71942f37b5f75ab1f"

KEY_WARNING = "This key is the only way into your account. Nobody can restore it, including us."
KEY_ACK = "I understand that nobody can restore this key"
WAITING_APPROVAL = "Waiting for approval from one of your other devices."
UNOPENABLE = "This message can't be opened on this device."
LINK_EXPIRED = "This link has expired."
WAITLIST_SUBJECT = "Confirm your Nightjar waitlist place"
WAITLIST_ACCEPTED = "Check your inbox to confirm."
WAITLIST_CONFIRMED = "You are on the Nightjar waitlist."
WAITLIST_USED = "This confirmation link has already been used."
WAITLIST_REMOVED = "Removed. Nightjar no longer holds your address."
WHITELIST_SUBJECT = "Nightjar whitelist application received"
WHITELIST_APPLIED = "Application received. It is not an allocation, and we'll be in touch."
BANNER_PHRASE = "get to know Nightjar better"
STAGES = ("Security", "Chat", "Voice messages", "Storage", "Task setup", "Planner")
SECTION_IDS = ("aboutSection", "featuresSection", "ecosystemSection", "tokenSaleSection",
               "roadmapSection", "faqSection", "subscribeSection")
PUBLIC_ROUTES = ("/", "/whitelist", "/network-limits", "/whitepaper", "/signin", "/signup")

QUOTA_BYTES = 67108864
PIECE_CLASSES = (65536, 1048576, 4194304)
STAKE_FLOOR = 10000
TIER_WEIGHT = {"basic": 10, "level-1": 15, "level-2": 25, "master": 150}
PRICE_MICRO = {"njr": 2250000, "usdc": 3500000, "usdt": 3500000, "xmr": 3500000,
               "app_store": 3500000}
DECIMALS = {"njr": 6, "usdc": 6, "usdt": 6, "xmr": 12}
DEPTH = {"njr": 12, "usdc": 12, "usdt": 12, "xmr": 10}
MONTH_SECONDS = 30 * 86400

SEEDED_RELAYS = ("Kestrel", "Heron", "Osprey", "Plover", "Wren", "Tern", "Avocet", "Sanderling")
SEEDED_EPOCHS = {
    2: {"rounds": 8,
        "relays": {"Heron": {"basic": 8}, "Kestrel": {"level-2": 7}, "Osprey": {"level-1": 5},
                   "Wren": {"master": 2, "level-2": 1}},
        "receipts": [("njr", 15000000, 15000000)] * 4 + [("njr", 14925000, 15000000)]
        + [("usdt", 145000)] * 3 + [("app_store", 155000)] * 2},
    3: {"rounds": 10,
        "relays": {"Plover": {"level-1": 9}, "Tern": {"level-2": 6, "basic": 4},
                   "Wren": {"master": 10}, "Avocet": {"basic": 7}, "Sanderling": {}},
        "receipts": [("njr", 16071429, 16071429)] * 6 + [("xmr", 138500)] * 4
        + [("usdc", 151250)] * 5},
    4: {"rounds": 5,
        "relays": {"Avocet": {"level-1": 5}, "Heron": {"basic": 3},
                   "Kestrel": {"level-2": 2, "level-1": 2}, "Tern": {"basic": 5}},
        "receipts": [("usdc", 147000)] * 7 + [("njr", 15000000, 15000000)] * 2},
}

SCHEDULES = {
    "team": (1500, 0, 12, 24), "treasury": (2000, 0, 6, 36), "visioners": (1000, 1000, 3, 9),
    "seed": (500, 500, 6, 12), "private": (800, 1000, 3, 12), "strategic": (400, 1500, 3, 9),
    "public": (300, 2500, 0, 6), "liquidity": (1000, 10000, 0, 0), "bounty": (200, 5000, 0, 6),
    "community": (1300, 0, 1, 36), "genesis": (1000, 2000, 0, 24),
}


def expected_epoch(number: int) -> dict:
    """Contributions, pool, weights, shares and remainder by the brief's settlement rule."""
    seeded = SEEDED_EPOCHS[number]
    contributions = 0
    for receipt in seeded["receipts"]:
        if receipt[0] == "njr":
            contributions += min(receipt[1], receipt[2])
        else:
            contributions += PRICE_MICRO[receipt[0]] * 10 ** 6 // receipt[1]
    pool = contributions * 80 // 100
    weights = {name: sum(TIER_WEIGHT[tier] * count for tier, count in rounds.items())
               for name, rounds in seeded["relays"].items()}
    total = sum(weights.values())
    shares = {name: (pool * w // total if total else 0) for name, w in weights.items()}
    return {"contributions": contributions, "pool": pool, "weights": weights, "total_weight": total,
            "shares": shares, "remainder": pool - sum(shares.values())}


def vested(schedule: str, allocation: int, launch: dt.datetime, at: dt.datetime) -> int:
    """The brief's vesting calculation for one position at one instant."""
    _, event_bp, cliff_months, linear_months = SCHEDULES[schedule]
    elapsed = (at - launch).total_seconds()
    if elapsed < 0:
        return 0
    event_part = allocation * event_bp // 10000
    rest = allocation - event_part
    cliff = cliff_months * MONTH_SECONDS
    whole = (cliff_months + linear_months) * MONTH_SECONDS
    if elapsed < cliff:
        return event_part
    if whole == 0 or elapsed >= whole:
        return allocation
    return event_part + int(rest * int(elapsed) // whole)


CLIENT_ERRORS = tuple(range(400, 500))
DENIALS = (401, 403, 404)


def unique(prefix: str) -> str:
    return f"{prefix}-{os.urandom(5).hex()}"


def unique_email() -> str:
    return f"{unique('probe')}@example.com"


def settle(seconds: float = 1.0) -> None:
    """The one sanctioned pause, for mail and background work that lands out of band."""
    time.sleep(seconds)


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso(moment: dt.datetime) -> str:
    return moment.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def parse_time(text: str) -> dt.datetime:
    return dt.datetime.fromisoformat(text.replace("Z", "+00:00"))


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def client(token: str | None = None) -> httpx.Client:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, headers=headers)


def body(response: httpx.Response):
    if "json" in response.headers.get("content-type", "") and response.content:
        return response.json()
    return {}


def expect(response: httpx.Response, statuses, what: str) -> dict:
    assert response.status_code in statuses, (
        f"{what}: {response.request.method} {response.request.url.path} returned "
        f"{response.status_code}: {response.text[:300]}"
    )
    return body(response)


def barrier_run(count: int, action) -> list:
    """Run `action(index)` from `count` threads released together."""
    gate = threading.Barrier(count)
    results: list = [None] * count

    def worker(i: int) -> None:
        gate.wait()
        results[i] = action(i)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(120)
    return results


def warm_clients(tokens: list[str | None]) -> list[httpx.Client]:
    """One client per simultaneous request, each with a warm connection."""
    made = []
    for token in tokens:
        c = client(token)
        c.get("/health")
        made.append(c)
    return made


_P = 2 ** 255 - 19
_L = 2 ** 252 + 27742317777372353535851937790883648493
_D = (-121665 * pow(121666, _P - 2, _P)) % _P
_GY = (4 * pow(5, _P - 2, _P)) % _P


def _xrecover(y: int) -> int:
    xx = (y * y - 1) * pow(_D * y * y + 1, _P - 2, _P)
    x = pow(xx, (_P + 3) // 8, _P)
    if (x * x - xx) % _P != 0:
        x = (x * pow(2, (_P - 1) // 4, _P)) % _P
    if x % 2 != 0:
        x = _P - x
    return x


_G = (_xrecover(_GY), _GY, 1, (_xrecover(_GY) * _GY) % _P)


def _add(a, b):
    x1, y1, z1, t1 = a
    x2, y2, z2, t2 = b
    aa = (y1 - x1) * (y2 - x2) % _P
    bb = (y1 + x1) * (y2 + x2) % _P
    cc = 2 * t1 * t2 * _D % _P
    dd = 2 * z1 * z2 % _P
    e, f, g, h = bb - aa, dd - cc, dd + cc, bb + aa
    return (e * f % _P, g * h % _P, f * g % _P, e * h % _P)


def _mul(s: int, point):
    q = (0, 1, 1, 0)
    while s > 0:
        if s & 1:
            q = _add(q, point)
        point = _add(point, point)
        s >>= 1
    return q


def _encode(point) -> bytes:
    x, y, z, _ = point
    zi = pow(z, _P - 2, _P)
    x, y = x * zi % _P, y * zi % _P
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def _clamp(seed: bytes) -> tuple[int, bytes]:
    h = hashlib.sha512(seed).digest()
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return a, h[32:]


def ed_public(seed: bytes) -> bytes:
    a, _ = _clamp(seed)
    return _encode(_mul(a, _G))


def ed_sign(seed: bytes, message: bytes) -> bytes:
    a, prefix = _clamp(seed)
    public = _encode(_mul(a, _G))
    r = int.from_bytes(hashlib.sha512(prefix + message).digest(), "little") % _L
    big_r = _encode(_mul(r, _G))
    k = int.from_bytes(hashlib.sha512(big_r + public + message).digest(), "little") % _L
    s = (r + k * a) % _L
    return big_r + int.to_bytes(s, 32, "little")


class Wallet:
    def __init__(self) -> None:
        self.seed = os.urandom(32)
        self.address = "0x" + ed_public(self.seed).hex()

    def sign(self, message: str) -> str:
        return ed_sign(self.seed, message.encode("utf-8")).hex()


def challenge(wallet: Wallet, purpose: str) -> dict:
    with client() as c:
        return expect(c.post("/auth/wallet/challenge",
                             json={"address": wallet.address, "purpose": purpose}),
                      (200, 201), f"{purpose} challenge for {wallet.address}")


def signed_body(wallet: Wallet, purpose: str) -> dict:
    ch = challenge(wallet, purpose)
    return {"challenge_id": ch["challenge_id"], "address": wallet.address,
            "signature": wallet.sign(ch["message"])}


def signup(email: str | None = None) -> dict:
    email = email or unique_email()
    with client() as c:
        data = expect(c.post("/auth/signup", json={"email": email, "password": PASSWORD}),
                      (200, 201), f"signup for {email}")
    assert data.get("access_token"), f"signup for {email} returned no access_token: {data}"
    data["email"] = email
    return data


def login(email: str, password: str = PASSWORD) -> str:
    with client() as c:
        data = expect(c.post("/auth/login", json={"email": email, "password": password}),
                      (200,), f"login for {email}")
    assert data.get("access_token"), f"login for {email} returned no access_token"
    return data["access_token"]


def me(token: str) -> dict:
    with client(token) as c:
        return expect(c.get("/me"), (200,), "GET /api/me")


def register_device(token: str) -> dict:
    with client(token) as c:
        data = expect(c.post("/devices", json={"identity_key": b64(os.urandom(32))}),
                      (200, 201), "device registration")
    assert data.get("device_id") and data.get("device_token"), (
        f"device registration returned {data}")
    return data


def member_with_device() -> dict:
    account = signup()
    device = register_device(account["access_token"])
    account["device"] = device
    return account


def conversation(token: str, kind: str, members: list[str], **extra) -> dict:
    payload = {"kind": kind, "members": members}
    if kind in ("public_group", "channel"):
        payload["public_name"] = extra.get("public_name", unique("Public"))
    else:
        payload["sealed_topic"] = extra.get("sealed_topic", b64(os.urandom(24)))
    with client(token) as c:
        return expect(c.post("/conversations", json=payload), (200, 201),
                      f"create {kind}")


def conversation_state(token: str, conversation_id: str) -> dict:
    with client(token) as c:
        return expect(c.get(f"/conversations/{conversation_id}"), (200,),
                      f"GET conversation {conversation_id}")


def envelope_payload(epoch: int, devices: list[str], client_id: str | None = None,
                     clock: int = 1, sender_seq: int = 1) -> dict:
    return {"client_id": client_id or unique("msg"), "epoch": epoch, "clock": clock,
            "sender_seq": sender_seq, "ciphertext": b64(os.urandom(48)),
            "sealed_keys": [{"device_id": d, "sealed_key": b64(os.urandom(40))}
                            for d in devices]}


def post_envelope(device_token: str, conversation_id: str, payload: dict) -> httpx.Response:
    with client(device_token) as c:
        return c.post(f"/conversations/{conversation_id}/envelopes", json=payload)


def history(token: str, conversation_id: str, limit: int = 200) -> httpx.Response:
    with client(token) as c:
        return c.get(f"/conversations/{conversation_id}/history", params={"limit": limit})


def sync_all(device_token: str, after: str | None = None) -> tuple[list[dict], str | None]:
    items: list[dict] = []
    cursor = after
    with client(device_token) as c:
        for _ in range(200):
            params = {"limit": 100}
            if cursor:
                params["after"] = cursor
            page = expect(c.get("/sync", params=params), (200,), "GET /api/sync")
            items.extend(page.get("items", []))
            cursor = page.get("next_cursor") or cursor
            if not page.get("has_more"):
                break
    return items, cursor


@pytest.fixture(scope="session")
def treasurer_token() -> str:
    return login(TREASURER_EMAIL)


@pytest.fixture(scope="session")
def operator_token() -> str:
    return login(OPERATOR_EMAIL)


@pytest.fixture(scope="session")
def backend() -> Backend:
    return make_backend()


def watcher_post(path: str, payload: dict, seed: bytes = WATCHER_SEED,
                 tamper: bool = False) -> httpx.Response:
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    signature = ed_sign(seed, raw).hex()
    if tamper:
        raw = json.dumps(dict(payload, amount=payload.get("amount", 0) + 1),
                         separators=(",", ":")).encode("utf-8")
    with client() as c:
        return c.post(path, content=raw, headers={"Content-Type": "application/json",
                                                  "X-Watcher-Signature": signature})


def post_rate(asset: str, usd_micros: int, observed_at: dt.datetime) -> None:
    response = watcher_post("/watcher/rates", {"asset": asset, "usd_micros": usd_micros,
                                               "observed_at": iso(observed_at)})
    expect(response, (200, 201, 202), f"signed rate for {asset}")


def fresh_rates() -> None:
    moment = now_utc()
    for asset, rate in (("njr", 150000), ("usdc", 1000000), ("usdt", 1000000),
                        ("xmr", 157300000)):
        post_rate(asset, rate, moment)


def quote(token: str, rail: str, for_contact_code: str | None = None) -> dict:
    payload = {"rail": rail}
    if for_contact_code:
        payload["for_contact_code"] = for_contact_code
    with client(token) as c:
        return expect(c.post("/quotes", json=payload), (200, 201), f"quote on {rail}")


def payment_event(q: dict, amount: int, confirmations: int, block_time: dt.datetime,
                  tx_hash: str | None = None) -> dict:
    return {"rail": q["rail"], "tx_hash": tx_hash or ("0x" + os.urandom(32).hex()),
            "deposit_reference": q["deposit_reference"], "amount": amount,
            "block_time": iso(block_time), "confirmations": confirmations}


def membership(token: str) -> dict:
    with client(token) as c:
        return expect(c.get("/membership"), (200,), "GET /api/membership")


def payments(token: str) -> list[dict]:
    with client(token) as c:
        return expect(c.get("/payments"), (200,), "GET /api/payments")


def pay_in_full(token: str, rail: str = "njr", for_contact_code: str | None = None) -> dict:
    fresh_rates()
    q = quote(token, rail, for_contact_code)
    event = payment_event(q, q["amount_due"], DEPTH[rail], now_utc() - dt.timedelta(seconds=2))
    expect(watcher_post("/watcher/payments", event), (200, 201, 202), "settling payment")
    return q


def db_rows(backend: Backend, sql: str, params: tuple = ()) -> list[dict]:
    return backend.query(sql, params)


def leak_forms(marker: str) -> list[str]:
    raw = marker.encode("utf-8")
    forms = {marker, raw.hex(), raw.hex().upper()}
    for pad in (b"", b"a", b"ab"):
        text = base64.b64encode(pad + raw).decode("ascii")
        trimmed = text[len(base64.b64encode(pad).decode()) + 1:-4] if pad else text[:-4]
        if len(trimmed) >= 12:
            forms.add(trimmed)
            forms.add(trimmed.replace("+", "-").replace("/", "_"))
    return sorted(forms)


def database_holds(backend: Backend, forms: list[str]) -> list[str]:
    """Every user table, whole row cast to text, searched for each form."""
    tables = backend.query(
        "SELECT table_schema, table_name FROM information_schema.tables "
        "WHERE table_type = 'BASE TABLE' AND table_schema NOT IN "
        "('pg_catalog', 'information_schema')")
    hits = []
    for t in tables:
        name = f'"{t["table_schema"]}"."{t["table_name"]}"'
        for form in forms:
            found = backend.query(f"SELECT count(*) AS n FROM {name} AS r "
                                  f"WHERE r::text ILIKE %s", (f"%{form}%",))
            if found and found[0]["n"]:
                hits.append(f"{name} contains {form!r}")
    return hits


def _inbox_base() -> str:
    return os.environ["EMAIL_INBOX_API_URL"].rstrip("/")


def mails_to(address: str, subject_prefix: str = "") -> list[dict]:
    listing = httpx.get(f"{_inbox_base()}/messages", params={"limit": 1000},
                        timeout=TIMEOUT).json()
    found = []
    for item in listing.get("messages", []):
        recipients = [a.get("Address", "").lower() for a in item.get("To", [])]
        subject = item.get("Subject", "")
        if address.lower() in recipients and subject.startswith(subject_prefix):
            full = httpx.get(f"{_inbox_base()}/message/{item['ID']}", timeout=TIMEOUT).json()
            found.append({"subject": subject, "text": full.get("Text", ""),
                          "to": [a.get("Address", "").lower() for a in full.get("To") or []],
                          "cc": full.get("Cc") or [], "bcc": full.get("Bcc") or []})
    return found


def wait_for_mail(address: str, subject_prefix: str, at_least: int = 1,
                  rounds: int = 20) -> list[dict]:
    found: list[dict] = []
    for _ in range(rounds):
        found = mails_to(address, subject_prefix)
        if len(found) >= at_least:
            break
        settle(1.0)
    return found


def app_page(path: str = "/") -> httpx.Response:
    return httpx.get(f"{app_url()}{path}", timeout=TIMEOUT, follow_redirects=True)


@pytest.fixture(scope="session")
def browser_page():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        yield browser
        browser.close()


class Wire:
    """Everything a browser context sends: request bodies and socket frames."""

    def __init__(self, context) -> None:
        self.sent: list[bytes] = []
        self.frames: list[bytes] = []
        context.on("request", self._request)
        context.on("websocket", self._socket)

    def _request(self, request) -> None:
        data = request.post_data_buffer
        self.sent.append((request.url + "\n").encode("utf-8") + (data or b""))

    def _socket(self, ws) -> None:
        ws.on("framesent", self._frame)

    def _frame(self, payload) -> None:
        self.frames.append(payload if isinstance(payload, bytes) else str(payload).encode())

    def carries(self, forms: list[str]) -> list[str]:
        hits = []
        for blob in self.sent + self.frames:
            text = blob.decode("utf-8", "ignore")
            for form in forms:
                if form in text:
                    hits.append(form)
        return sorted(set(hits))


def open_workspace(context, email: str, password: str = PASSWORD, first: bool = True):
    """Sign in through /signin. A first device acknowledges the key dialog; a later
    device lands on the waiting notice."""
    page = context.new_page()
    page.goto(f"{app_url()}/signin")
    page.get_by_label("Email", exact=True).fill(email)
    page.get_by_label("Password", exact=True).fill(password)
    page.get_by_role("button", name="Sign in", exact=True).click()
    if first:
        ack = page.get_by_label(KEY_ACK)
        ack.wait_for(state="visible", timeout=30000)
        ack.check()
        page.get_by_role("button", name="Continue", exact=True).click()
    page.wait_for_url(re.compile(r".*/app.*"), timeout=30000)
    page.wait_for_load_state("load")
    page.wait_for_timeout(1500)
    return page


def wait_for_text(page, text: str, seconds: int = 30, reload_every: int = 5) -> bool:
    for i in range(seconds):
        if page.get_by_text(text, exact=False).count() > 0:
            return True
        if reload_every and i and i % reload_every == 0:
            page.reload()
        page.wait_for_timeout(1000)
    return page.get_by_text(text, exact=False).count() > 0


def devices_of(token: str) -> list[dict]:
    with client(token) as c:
        return expect(c.get("/devices"), (200,), "GET /api/devices")
