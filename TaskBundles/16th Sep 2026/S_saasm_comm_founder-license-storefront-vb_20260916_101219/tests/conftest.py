"""Fixtures, pinned literals and helpers for deku/founder-license-storefront-vb.

Every literal below is pinned verbatim in instruction.md. Provider state is read
through the capability adapters the verifier base image ships (the database,
the Mailpit inbox and the Kill Bill tenant); nothing here imports a provider SDK
and nothing reads the application's source. This module defines no tests.
"""

from __future__ import annotations

import email.utils
import json
import math
import os
import re
import threading
import time
from urllib.parse import urlparse

import httpx
import pytest
from playwright.sync_api import sync_playwright

from appclient import api_base, app_url, login, seeded_password
from capabilities import make_backend, make_inbox, make_payments

TIMEOUT = 30.0
SETTLE_SECONDS = 2.0
POLL_SECONDS = 60.0

PASSWORD = "deku-demo-pw-2026"
OPERATOR_EMAIL = "operator@example.com"
OPERATOR_NAME = "Devrim"
REGISTRANT_EMAIL = "registrant@example.com"
REGISTRANT_NAME = "Ada Registrant"
REGISTRANT2_EMAIL = "registrant2@example.com"
REGISTRANT2_NAME = "Ben Registrant"
REGISTRANT3_EMAIL = "registrant3@example.com"
REGISTRANT3_NAME = "Cy Registrant"
SUPPORT_EMAIL = "hello@example.com"

SEED_LIVE = "seed-live-4b7d9e2a61c3f085"
SEED_REVOKED = "seed-revoked-9a4d7e1f5b20"
SEED_EXPIRED = "seed-expired-7c1e2a9b4d36"
SEED_USEDUP = "seed-usedup-3f8b6d0c2e71"

SUBJECT = "Your Lumen Prompt beta access link"
LINE_FIRST = "You are registered for the Lumen Prompt beta."
LINE_LATER = "You were already on the list, so this is a fresh link."
PLACE_PREFIX = "Your founder place:"
SUCCESS_MESSAGE = "Check your inbox for your access link."
RESEND_MESSAGE = "If that address is registered, a fresh access link is on its way."
DATA_REQUEST_MESSAGE = "We will reply to that address within 30 days."
HEADING_CONFIRMED = "Your access link is confirmed"
HEADING_INVALID = "This access link is no longer valid"
HEADING_USED_UP = "This access link has been used up"
HEADING_EXPIRED = "This access link has expired"
HEADING_UNKNOWN = "We do not recognise this access link"
DOWNLOAD_CONTROL = "Download for Mac"
STATUS_NO_SESSION = "Open the link in your email to see your status"
CHECKOUT_NOTICE = "Founder checkout opens at 1.0"
LICENCE_NOTICE = "Licence activation opens at 1.0"
REVOKED_NOTICE = "This release was revoked and is no longer offered."
CLOSED_NOTICE = "Founder places are all claimed"

COHORT_CAP = 1000
TIER_SIZE = 500
TIER1_PRICE = 2900
TIER2_PRICE = 3900
CURRENCY = "usd"
KEY_PREFIX = "lumen-founder-"
MAX_OPENS = 5
LINK_DAYS = 14
HOURLY_EMAILS = 3

SEED_RELEASES = (
    {
        "version": "0.2.3", "build": 4, "published_at": "2026-08-28", "min_os": "26.1",
        "size_bytes": 24117248,
        "sha256": "08035fead80e0cfe09a8ad0bc7d7486a353c38890810acd9ed2cb8372df9bb5a",
        "ed_signature": "72hn8fG8m3U31YYqCB378cZKcpDwXR+iNhBHIvstb8USInEGvUdXHuRZdNMAK0OyBz2RmbRD7zMyOz4RQa2cRg==",
        "download_url": "https://downloads.example.com/lumen-prompt/Lumen-Prompt-0.2.3.dmg",
        "status": "published",
        "summary": "Faster search, steadier injection and a clearer version history.",
    },
    {
        "version": "0.2.2", "build": 3, "published_at": "2026-08-07", "min_os": "26.1",
        "size_bytes": 23855104,
        "sha256": "c2e5920ade47626fae119eb565b325979707e168705380a4791055818855780c",
        "ed_signature": "ltDS2MUPQgeuA+Z1N+PII/9zmDPiHSmTPikafE9dlpnhNemyHFCUH0h5024DhXw8CvuiCgTWI4YJ8vAu5cnJVA==",
        "download_url": "https://downloads.example.com/lumen-prompt/Lumen-Prompt-0.2.2.dmg",
        "status": "published",
        "summary": "Context files can now be switched on and off before sending.",
    },
    {
        "version": "0.2.1", "build": 2, "published_at": "2026-07-17", "min_os": "26.0",
        "size_bytes": 23592960,
        "sha256": "6557b3ed2d20b07757b7c5080ef611a1b0c7b4c855393417a5060d5c20f03cda",
        "ed_signature": "a6Ua7KYh1AvSwE2D4ZbgXbKkNh7S6YtbynIAOvMyv+IhhZEjWvtY+Pywy6bnrtMk+GjrOTJe8bOsyD8I+fhuxw==",
        "download_url": "https://downloads.example.com/lumen-prompt/Lumen-Prompt-0.2.1.dmg",
        "status": "published",
        "summary": "Import from four other tools, with a preview before anything is written.",
    },
    {
        "version": "0.2.0", "build": 1, "published_at": "2026-06-26", "min_os": "26.0",
        "size_bytes": 23330816,
        "sha256": "b10364b9f7d0b4a8ee44327567675ec333eafcd6d627a5935a9789c4fdb0e020",
        "ed_signature": "VVMY3peMs3lA7du1DIi98M1Wucbu3+DZhNEH87GT7jr85OT3PFh+ceOX3sYMjpGRvPhtwYSrg6q3T5I8AQXNuA==",
        "download_url": "https://downloads.example.com/lumen-prompt/Lumen-Prompt-0.2.0.dmg",
        "status": "revoked",
        "summary": "The first open beta build.",
    },
)

CONTENT_ROUTES = (
    "/",
    "/download",
    "/use-cases",
    "/use-cases/reusable-ai-prompt-templates",
    "/use-cases/prompt-version-history",
    "/use-cases/prompt-manager-for-mac",
    "/use-cases/local-first-prompt-library",
    "/use-cases/hotkey-prompt-injection-macos",
    "/changelog",
    "/release-notes/0.2.3",
    "/roadmap",
    "/blog",
    "/press",
    "/contact",
    "/privacy",
    "/terms",
)
ARTICLE_ROUTES = (
    "/blog/stop-rewriting-your-best-prompt",
    "/blog/prompts-are-work-product",
)
USE_CASE_PAGES = (
    ("/use-cases/reusable-ai-prompt-templates", "Reusable templates",
     "Reusable AI prompt templates for Mac, with variables that fill themselves."),
    ("/use-cases/prompt-version-history", "Time Machine",
     "Prompt version history that shows what changed and which version worked."),
    ("/use-cases/prompt-manager-for-mac", "Mac prompt manager",
     "A prompt manager for Mac that lives one keystroke away."),
    ("/use-cases/local-first-prompt-library", "Local-first",
     "A local-first prompt library that never leaves your Mac."),
    ("/use-cases/hotkey-prompt-injection-macos", "Hotkey launcher",
     "Hotkey prompt injection on macOS, into the app you already use."),
)
PALETTE_BLUEPRINTS = (
    ("Client brief summary", "WRITING"),
    ("Code review checklist", "ENGINEERING"),
    ("Research synthesis", "RESEARCH"),
    ("Meeting follow-up", "OPERATIONS"),
    ("Release notes draft", "PRODUCT"),
)
PALETTE_DESTINATION_ROUTES = (
    "/", "/download", "/use-cases", "/changelog", "/roadmap", "/blog", "/press",
    "/contact", "/privacy", "/release-notes/0.2.3",
    "/use-cases/reusable-ai-prompt-templates", "/use-cases/prompt-version-history",
    "/use-cases/prompt-manager-for-mac", "/use-cases/local-first-prompt-library",
    "/use-cases/hotkey-prompt-injection-macos",
    "/blog/stop-rewriting-your-best-prompt", "/blog/prompts-are-work-product",
)
HOME_HEADINGS = (
    "Any prompt, one keystroke away.",
    "One loop, not four separate chores.",
    "A native workspace for reusable prompt work.",
    "Keep your best prompts as reusable Blueprints.",
    "Attach the files and facts your prompt depends on.",
    "Every prompt iteration has a history.",
    "The prompt is not just text. It is the whole working packet.",
    "Know what you sent, when, and where.",
    "Shape what ships next",
    "Prompt work stays with your Mac.",
    "A different category, by design.",
    "Free during beta. One-time pricing at 1.0.",
    "The trust questions before you join.",
    "Build the prompt library you can keep.",
)
HOME_EYEBROWS = (
    "Command flow", "Product surfaces", "Prompt packet", "Audit trail", "Open beta",
    "Local-first", "Compare", "Pricing", "Help panel",
)
HELP_QUESTIONS = (
    "Does Lumen Prompt send my prompts anywhere?",
    "Can Halyard Labs read my library?",
    "Is there a subscription?",
    "What happens to the founder price after 1.0?",
    "How do I get the beta?",
    "How are updates delivered and verified?",
    "Which Macs are supported?",
    "Which apps can receive a prompt?",
)
RELEASE_NOTE_SECTIONS = (
    "What is new", "Also in this release", "Fixed", "Performance", "Known issues",
    "Updates", "Reporting problems",
)
TYPE_SIZES_BELOW_DISPLAY = (10.0, 11.0, 12.0, 14.0, 16.0, 18.0)
TOKEN_RE = re.compile(r"/beta/access/([A-Za-z0-9_-]{32,})")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
MAILPIT_API_ROOT = "/".join(("", "api", "v1"))
SECRET_VARIABLES = ("PAYMENTS_API_SECRET", "PAYMENTS_ADMIN_PASSWORD", "SMTP_PASS",
                    "DATABASE_URL", "DB_URL", "DB_ADMIN_URL")


def backend_secrets() -> list[str]:
    """The configured provider credentials, read from this run's environment.

    Nothing the browser downloads may carry one, and taking the values from the
    environment rather than pinning them here keeps the credential out of the
    bundle as well as out of the page.
    """
    found = []
    for name in SECRET_VARIABLES:
        value = os.environ.get(name, "").strip()
        if len(value) >= 10 and value not in found:
            found.append(value)
    return found


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned sleep.

    Used before asserting that something did NOT happen, and as the interval of
    the bounded polls below, so no raw sleep exists anywhere else in the suite.
    """
    time.sleep(seconds)


def probe_email(tag: str = "probe") -> str:
    return f"{tag}-{os.urandom(6).hex()}@example.com"


def api(token: str | None = None) -> httpx.Client:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, headers=headers,
                        follow_redirects=False)


def site() -> httpx.Client:
    return httpx.Client(base_url=app_url(), timeout=TIMEOUT, follow_redirects=False)


def registration_body(email_address: str | None, **overrides) -> dict:
    body = {
        "email": email_address,
        "name": "",
        "platform_version": "",
        "role": "",
        "primary_use": "",
        "consent": True,
        "company_website": "",
    }
    if email_address is None:
        body.pop("email")
    body.update(overrides)
    return body


def register(email_address: str | None, **overrides) -> httpx.Response:
    with api() as client:
        return client.post("/beta/register", json=registration_body(email_address, **overrides))


def resend(email_address: str) -> httpx.Response:
    with api() as client:
        return client.post("/beta/resend", json={"email": email_address})


def allocation() -> dict:
    with api() as client:
        response = client.get("/founder/allocation")
    assert response.status_code == 200, (
        f"GET /api/founder/allocation returned {response.status_code}: {response.text[:300]}"
    )
    return response.json()


def releases() -> list[dict]:
    with api() as client:
        response = client.get("/releases")
    assert response.status_code == 200, (
        f"GET /api/releases returned {response.status_code}: {response.text[:300]}"
    )
    payload = response.json()
    assert isinstance(payload, list), (
        f"GET /api/releases must return a top-level JSON array, got {str(payload)[:300]}"
    )
    return payload


def release(version: str) -> dict | None:
    for row in releases():
        if str(row.get("version")) == version:
            return row
    return None


def page_html(path: str) -> httpx.Response:
    with site() as client:
        return client.get(path)


def operator_login() -> str:
    return login(OPERATOR_EMAIL, seeded_password("SEED_OPERATOR_PASSWORD", PASSWORD))


def text_of(html: str) -> str:
    stripped = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    stripped = re.sub(r"<style\b[^>]*>.*?</style>", " ", stripped, flags=re.S | re.I)
    stripped = re.sub(r"<[^>]+>", " ", stripped)
    stripped = (stripped.replace("&amp;", "&").replace("&#39;", "'").replace("&#x27;", "'")
                .replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">")
                .replace("&nbsp;", " "))
    return " ".join(stripped.split())


def hrefs(html: str) -> list[str]:
    return re.findall(r"<a\b[^>]*\bhref\s*=\s*[\"']([^\"']+)[\"']", html, flags=re.I)


def internal_path(href: str) -> str | None:
    if href.startswith(("mailto:", "tel:", "javascript:")):
        return None
    parsed = urlparse(href)
    base = urlparse(app_url())
    if parsed.scheme and parsed.netloc and parsed.netloc != base.netloc:
        return None
    if not parsed.scheme and not href.startswith("/"):
        if href.startswith("#"):
            return None
        return None
    path = parsed.path or "/"
    return path


def open_link(token: str) -> tuple[httpx.Client, httpx.Response]:
    """Open an access link the way a browser would, following the token drop."""
    client = httpx.Client(base_url=app_url(), timeout=TIMEOUT, follow_redirects=True)
    return client, client.get(f"/beta/access/{token}")


def status_page_session(token: str) -> httpx.Client:
    client, response = open_link(token)
    assert response.status_code == 200, (
        f"opening a live access link returned {response.status_code}: {response.text[:300]}"
    )
    return client


def heading_pairs(html: str) -> list[tuple[int, str]]:
    return [(int(level), text_of(inner))
            for level, inner in re.findall(r"<h([1-6])\b[^>]*>(.*?)</h\1>",
                                           html, flags=re.S | re.I)]


def headings(html: str) -> list[str]:
    return [text for _level, text in heading_pairs(html)]


def section_after(html: str, heading: str) -> str:
    """The markup between a heading and the next heading at or above its level."""
    marks = [(m.start(), m.end(), int(m.group(1)), text_of(m.group(2)))
             for m in re.finditer(r"<h([1-6])\b[^>]*>(.*?)</h\1>", html, flags=re.S | re.I)]
    wanted = heading.strip().lower()
    for i, (_start, end, level, text) in enumerate(marks):
        if text.strip().lower() == wanted:
            stop = len(html)
            for later_start, _e, later_level, _t in marks[i + 1:]:
                if later_level <= level:
                    stop = later_start
                    break
            return html[end:stop]
    return ""


def input_tags(html: str) -> list[dict]:
    out = []
    for tag in re.findall(r"<(?:input|select|textarea|button)\b[^>]*>", html, flags=re.I):
        attrs = {k.lower(): v for k, v in
                 re.findall(r'([A-Za-z_:][-\w:.]*)\s*=\s*"([^"]*)"', tag)}
        attrs.update({k.lower(): v for k, v in
                      re.findall(r"([A-Za-z_:][-\w:.]*)\s*=\s*'([^']*)'", tag)})
        for bare in re.findall(r"(?:^|\s)([A-Za-z_:][-\w:.]*)(?=\s|/?>)", tag):
            attrs.setdefault(bare.lower(), "")
        out.append(attrs)
    return out


def json_ld(html: str) -> list[dict]:
    """Every JSON-LD block on a page, with any @graph flattened into it."""
    out: list[dict] = []
    blocks = re.findall(
        r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html, flags=re.S | re.I)
    for block in blocks:
        payload = json.loads(block.strip())
        items = payload if isinstance(payload, list) else [payload]
        for item in items:
            if isinstance(item, dict):
                out.append(item)
                for nested in item.get("@graph") or []:
                    if isinstance(nested, dict):
                        out.append(nested)
    return out


def ld_types(html: str) -> set[str]:
    found = set()
    for block in json_ld(html):
        kind = block.get("@type")
        if isinstance(kind, list):
            found.update(str(k) for k in kind)
        elif kind:
            found.add(str(kind))
    return found


def canonical_of(html: str) -> str | None:
    for tag in re.findall(r"<link\b[^>]*>", html, flags=re.I):
        attrs = {k.lower(): v for k, v in
                 re.findall(r'([A-Za-z_:][-\w:.]*)\s*=\s*["\']([^"\']*)["\']', tag)}
        if attrs.get("rel", "").lower() == "canonical":
            return attrs.get("href")
    return None


def set_cookie_headers(response) -> list[tuple[str, object]]:
    """Every Set-Cookie header of a response and of every redirect before it."""
    raw: list[tuple[str, object]] = []
    for hop in list(response.history) + [response]:
        for value in hop.headers.get_list("set-cookie"):
            raw.append((value, hop))
    return raw


def cookie_seconds(raw: str, hop) -> float | None:
    """A Set-Cookie header's lifetime, read against the response's own Date."""
    match = re.search(r"max-age=(-?\d+)", raw, re.I)
    if match:
        return float(match.group(1))
    match = re.search(r"expires=([^;]+)", raw, re.I)
    sent = hop.headers.get("date")
    if match and sent:
        return http_date_seconds(match.group(1)) - http_date_seconds(sent)
    return None


def wait_for(probe, timeout: float = POLL_SECONDS):
    """Bounded poll: call probe() until it returns something truthy or time runs out."""
    deadline = time.monotonic() + timeout
    value = probe()
    while not value and time.monotonic() < deadline:
        settle(0.5)
        value = probe()
    return value


def reading_minutes(words: int) -> int:
    return int(math.ceil(words / 200)) if words else 0


def release_payload(version: str, build: int, **overrides) -> dict:
    body = {
        "version": version,
        "build": build,
        "min_os": "26.1",
        "size_bytes": 24500000,
        "sha256": os.urandom(32).hex(),
        "ed_signature": "cHJvYmUtc2lnbmF0dXJl" + os.urandom(12).hex(),
        "download_url": ("https://downloads.example.com/lumen-prompt/"
                         f"Lumen-Prompt-{version}.dmg"),
        "summary": "A probe build published by the grader.",
        "notes": "## What is new\n\nA probe build published by the grader.\n",
    }
    body.update(overrides)
    return body


class Ledger:
    """Domain reads composed from the generic backend adapter."""

    def __init__(self, backend) -> None:
        self._b = backend

    def q(self, sql: str, params: tuple = ()) -> list[dict]:
        return self._b.query(sql, params)

    def columns(self, table: str) -> set[str]:
        rows = self.q(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema = current_schema() AND table_name = %s", (table,))
        return {r["column_name"] for r in rows}

    def table_exists(self, table: str) -> bool:
        rows = self.q(
            "SELECT count(*) AS n FROM information_schema.tables "
            "WHERE table_schema = current_schema() AND table_name = %s", (table,))
        return rows[0]["n"] == 1

    def registration(self, email_address: str) -> dict | None:
        rows = self.q("SELECT * FROM registrations WHERE email = %s", (email_address,))
        assert len(rows) <= 1, f"{len(rows)} registrations rows hold {email_address!r}"
        return rows[0] if rows else None

    def registrations_named(self, name: str) -> int:
        return self.q("SELECT count(*) AS n FROM registrations WHERE name = %s", (name,))[0]["n"]

    def registrations_like(self, email_address: str) -> int:
        return self.q("SELECT count(*) AS n FROM registrations WHERE lower(email) = lower(%s)",
                      (email_address,))[0]["n"]

    def slot_for(self, email_address: str) -> dict | None:
        rows = self.q(
            "SELECT s.* FROM founder_slots s JOIN registrations r ON r.id = s.registration_id "
            "WHERE r.email = %s", (email_address,))
        assert len(rows) <= 1, f"{email_address!r} holds {len(rows)} founder places"
        return rows[0] if rows else None

    def slots(self) -> list[dict]:
        return self.q(
            "SELECT position, tier, price_minor, currency, killbill_external_key, registration_id "
            "FROM founder_slots ORDER BY position")

    def slot_count(self) -> int:
        return self.q("SELECT count(*) AS n FROM founder_slots")[0]["n"]

    def links_for(self, email_address: str) -> list[dict]:
        return self.q(
            "SELECT l.* FROM access_links l JOIN registrations r ON r.id = l.registration_id "
            "WHERE r.email = %s ORDER BY l.created_at", (email_address,))

    def clicks_for(self, link_id) -> int:
        return self.q("SELECT count(*) AS n FROM access_clicks WHERE access_link_id = %s",
                      (link_id,))[0]["n"]

    def release_rows(self) -> int:
        return self.q("SELECT count(*) AS n FROM releases")[0]["n"]

    def download_events(self, version: str) -> int:
        return self.q("SELECT count(*) AS n FROM download_events WHERE release_version = %s",
                      (version,))[0]["n"]

    def newest_download_event(self, version: str) -> dict | None:
        rows = self.q(
            "SELECT * FROM download_events WHERE release_version = %s "
            "ORDER BY created_at DESC LIMIT 1", (version,))
        return rows[0] if rows else None

    def data_requests(self, email_address: str) -> list[dict]:
        return self.q("SELECT * FROM data_requests WHERE email = %s", (email_address,))

    def seconds_since(self, email_address: str) -> float:
        rows = self.q(
            "SELECT EXTRACT(EPOCH FROM (now() - created_at::timestamptz)) AS age "
            "FROM registrations WHERE email = %s", (email_address,))
        return float(rows[0]["age"])

    def link_lifetime_seconds(self, link_id) -> float:
        rows = self.q(
            "SELECT EXTRACT(EPOCH FROM (expires_at::timestamptz - created_at::timestamptz)) AS life "
            "FROM access_links WHERE id = %s", (link_id,))
        return float(rows[0]["life"])


class MailRoom:
    """Mailpit reads through the email capability adapter."""

    def __init__(self, inbox) -> None:
        self.inbox = inbox

    def count(self, to: str) -> int:
        return self.inbox.count(to=to)

    def wait_for_count(self, to: str, at_least: int, timeout: float = POLL_SECONDS) -> int:
        deadline = time.monotonic() + timeout
        seen = self.count(to)
        while seen < at_least and time.monotonic() < deadline:
            settle(0.5)
            seen = self.count(to)
        return seen

    def summaries(self, to: str) -> list[dict]:
        response = self.inbox._client.get(f"{MAILPIT_API_ROOT}/messages", params={"limit": 500})
        assert response.status_code == 200, (
            f"Mailpit message list returned {response.status_code}: {response.text[:300]}"
        )
        out = []
        for item in response.json().get("messages", []):
            recipients = [a.get("Address", "") for a in item.get("To") or []]
            if any(to.lower() == r.lower() for r in recipients):
                out.append(item)
        return out

    def newest(self, to: str) -> dict:
        found = self.summaries(to)
        assert found, f"no message addressed to {to!r} is in the Mailpit inbox"
        response = self.inbox._client.get(f"{MAILPIT_API_ROOT}/message/{found[0]['ID']}")
        assert response.status_code == 200, (
            f"Mailpit message read returned {response.status_code}: {response.text[:300]}"
        )
        return response.json()

    def newest_token(self, to: str) -> str:
        message = self.newest(to)
        text = message.get("Text") or ""
        match = TOKEN_RE.search(text)
        assert match, (
            f"the newest access email to {to!r} carries no /beta/access/<token> link: "
            f"{text[:300]!r}"
        )
        return match.group(1)


class BillingLedger:
    """Kill Bill reads through the payments capability adapter."""

    def __init__(self, payments) -> None:
        self.payments = payments

    def account(self, external_key: str) -> dict | None:
        response = self.payments._client.get("/1.0/kb/accounts",
                                             params={"externalKey": external_key})
        assert response.status_code in (200, 404), (
            f"killbill account lookup for {external_key!r} returned "
            f"{response.status_code}: {response.text[:300]}"
        )
        return response.json() if response.status_code == 200 else None

    def all_accounts(self) -> list[dict]:
        response = self.payments._client.get("/1.0/kb/accounts/pagination",
                                             params={"offset": 0, "limit": 20000})
        assert response.status_code == 200, (
            f"killbill account pagination returned {response.status_code}: {response.text[:300]}"
        )
        payload = response.json()
        return payload if isinstance(payload, list) else payload.get("items", [])

    def accounts_for_email(self, email_address: str) -> list[dict]:
        return [a for a in self.all_accounts()
                if str(a.get("email", "")).lower() == email_address.lower()]

    def audit_logs(self, account_id) -> list[dict]:
        response = self.payments._client.get(f"/1.0/kb/accounts/{account_id}/auditLogs")
        assert response.status_code == 200, (
            f"killbill audit log read for {account_id} returned "
            f"{response.status_code}: {response.text[:300]}"
        )
        payload = response.json()
        return payload if isinstance(payload, list) else []

    def invoice_count(self) -> int:
        response = self.payments._client.get("/1.0/kb/invoices/pagination",
                                             params={"offset": 0, "limit": 20000})
        assert response.status_code == 200, (
            f"killbill invoice pagination returned {response.status_code}: {response.text[:300]}"
        )
        payload = response.json()
        return len(payload if isinstance(payload, list) else payload.get("items", []))


def founder_key(position: int) -> str:
    return f"{KEY_PREFIX}{int(position):04d}"


def expected_tier(position: int) -> tuple[int, int]:
    return (1, TIER1_PRICE) if int(position) <= TIER_SIZE else (2, TIER2_PRICE)


def register_many(addresses: list[str], workers: int) -> list[int]:
    """Register every address with `workers` requests released together per round."""
    statuses: list[int] = []
    guard = threading.Lock()
    for start in range(0, len(addresses), workers):
        batch = addresses[start:start + workers]
        gate = threading.Barrier(len(batch))

        def one(address: str) -> None:
            with api() as client:
                gate.wait()
                response = client.post("/beta/register", json=registration_body(address))
            with guard:
                statuses.append(response.status_code)

        threads = [threading.Thread(target=one, args=(a,)) for a in batch]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=120)
    return statuses


def http_date_seconds(value: str) -> float:
    return email.utils.parsedate_to_datetime(value).timestamp()


def composite_contrast_script() -> str:
    return """
    (selector) => {
      const canvas = document.createElement('canvas');
      canvas.width = 1; canvas.height = 1;
      const ctx = canvas.getContext('2d', {willReadFrequently: true});
      const rgba = (c) => {
        ctx.clearRect(0, 0, 1, 1);
        ctx.fillStyle = '#000000';
        ctx.fillStyle = c;
        ctx.fillRect(0, 0, 1, 1);
        const d = ctx.getImageData(0, 0, 1, 1).data;
        return [d[0], d[1], d[2], d[3] / 255];
      };
      const over = (top, bottom) => {
        const a = top[3];
        return [0, 1, 2].map(i => top[i] * a + bottom[i] * (1 - a)).concat([1]);
      };
      const background = (el) => {
        const chain = [];
        for (let n = el; n; n = n.parentElement) chain.push(n);
        let base = [255, 255, 255, 1];
        for (let i = chain.length - 1; i >= 0; i--) {
          const bg = getComputedStyle(chain[i]).backgroundColor;
          if (!bg || bg === 'transparent') continue;
          const c = rgba(bg);
          if (c[3] === 0) continue;
          base = over(c, base);
        }
        return base;
      };
      const lum = (c) => {
        const f = (v) => { v = v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
        return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]);
      };
      const ratio = (a, b) => {
        const la = lum(a), lb = lum(b);
        return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
      };
      const out = [];
      for (const el of document.querySelectorAll(selector)) {
        if (el.closest('[aria-hidden="true"]')) continue;
        const text = (el.textContent || '').trim();
        if (!text) continue;
        const box = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        if (box.width === 0 || box.height === 0 || style.visibility === 'hidden' || style.display === 'none') continue;
        const bg = background(el);
        const fg = over(rgba(style.color), bg);
        out.push({text: text.slice(0, 60), ratio: ratio(fg, bg), size: parseFloat(style.fontSize)});
      }
      return out;
    }
    """


def placeholder_contrast_script() -> str:
    return """
    (selector) => {
      const canvas = document.createElement('canvas');
      canvas.width = 1; canvas.height = 1;
      const ctx = canvas.getContext('2d', {willReadFrequently: true});
      const rgba = (c) => {
        ctx.clearRect(0, 0, 1, 1);
        ctx.fillStyle = '#000000';
        ctx.fillStyle = c;
        ctx.fillRect(0, 0, 1, 1);
        const d = ctx.getImageData(0, 0, 1, 1).data;
        return [d[0], d[1], d[2], d[3] / 255];
      };
      const over = (top, bottom) => {
        const a = top[3];
        return [0, 1, 2].map(i => top[i] * a + bottom[i] * (1 - a)).concat([1]);
      };
      const background = (el) => {
        let base = [255, 255, 255, 1];
        const chain = [];
        for (let n = el; n; n = n.parentElement) chain.push(n);
        for (let i = chain.length - 1; i >= 0; i--) {
          const c = rgba(getComputedStyle(chain[i]).backgroundColor);
          if (c[3] === 0) continue;
          base = over(c, base);
        }
        return base;
      };
      const lum = (c) => {
        const f = (v) => { v = v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
        return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]);
      };
      const out = [];
      for (const el of document.querySelectorAll(selector)) {
        const holder = el.getAttribute('placeholder');
        if (!holder) continue;
        const style = getComputedStyle(el, '::placeholder');
        const bg = background(el);
        const fg = over(rgba(style.color), bg);
        const la = lum(fg), lb = lum(bg);
        out.push({text: holder.slice(0, 40),
                  ratio: (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05)});
      }
      return out;
    }
    """


@pytest.fixture
def db():
    return Ledger(make_backend())


@pytest.fixture
def mail():
    return MailRoom(make_inbox())


@pytest.fixture
def billing():
    return BillingLedger(make_payments())


@pytest.fixture
def operator_token() -> str:
    return operator_login()


@pytest.fixture(scope="session")
def browser_instance():
    origin = f"{urlparse(app_url()).scheme}://{urlparse(app_url()).netloc}"
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            args=[f"--unsafely-treat-insecure-origin-as-secure={origin}"])
        yield browser
        browser.close()


@pytest.fixture
def page(browser_instance):
    context = browser_instance.new_context(base_url=app_url(),
                                           viewport={"width": 1440, "height": 900})
    tab = context.new_page()
    tab.set_default_timeout(20000)
    yield tab
    context.close()


@pytest.fixture
def ui_page(browser_instance):
    context = browser_instance.new_context(base_url=app_url(), java_script_enabled=False,
                                           viewport={"width": 1440, "height": 900})
    tab = context.new_page()
    tab.set_default_timeout(20000)
    yield tab
    context.close()
