"""Fixtures, pinned literals and bounded-poll helpers for the Thirty workspace.

No test functions live here. Every literal below appears verbatim in
instruction.md, so a grader never asserts a value the brief left the agent to
invent.
"""

from __future__ import annotations

import os
import re
import time
import concurrent.futures

import httpx

import appclient
import capabilities
import _shapes

TIMEOUT = 30.0
SETTLE_SECONDS = 3.0
POLL_DEADLINE = 45.0
FLOOR_SECONDS = 0.5
CYCLE_CEILING = 25

PASSWORD = appclient.seeded_password("SEEDED_PASSWORD", "deku-demo-pw-2026")
OWNER = "owner@example.com"
ADMIN = "admin@example.com"
MEMBER_ONE = "member@example.com"
MEMBER_TWO = "member2@example.com"
SEEDED_ACCOUNTS = (OWNER, ADMIN, MEMBER_ONE, MEMBER_TWO)

WORKFLOW_NAME = "Stage change notice"
NOT_FOUND_COPY = "404: This page could not be found."

STARTER_OBJECTS = ("Companies", "People", "Opportunities", "Tasks", "Notes",
                   "Dashboards", "Workflows")

FIELD_TYPES = ("text", "number", "currency", "date", "date and time", "boolean",
               "single select", "multi select", "rating", "links",
               "electronic mail addresses", "phone numbers", "address", "relation")

SEEDED_COMPANIES = (
    ("Arcadia Labs", "arcadialabs.ai", 50000000),
    ("Meshwork", "meshwork.com", 100000000),
    ("Chatterbox", "chatterbox.com", 230000000),
    ("Papertrail", "papertrail.com", 75000000),
    ("Pixelforge", "pixelforge.com", 350000000),
    ("Codeharbor", "codeharbor.com", 90000000),
    ("Wanderstay", "wanderstay.com", 420000000),
    ("Ledgerline", "ledgerline.com", 180000000),
    ("Quartz Capital", "quartzcap.com", 600000000),
)

PUBLIC_ROUTES = ("/", "/product", "/pricing", "/customers", "/partners", "/apps",
                 "/releases", "/why-thirty", "/halftone", "/privacy-policy", "/terms")

PINNED_COPY = {
    "/": ["Build your Enterprise CRM at AI Speed", "+10k others", "55.9K", "7.2K",
          "(C) 2026 - Thirty", "All Companies - 9", "npx create-thirty-app"],
    "/pricing": ["$9", "$19", "$50k", "-25%"],
    "/apps": ["All", "Enrichment", "Productivity", "Search"],
    "/halftone": ["Idle auto-rotate is active", "Design", "Animations", "Export"],
    "/product": ["All opportunities 9", "Type is Customer", "Employees > 500",
                 "Export selection as CSV", "G then P"],
}

FORBIDDEN_IN_BROWSER = (
    "postgresql://", "deku_admin", "deku-local-dev", "deku-app-pw",
    "DB_ADMIN_URL", "SMTP_PASS",
)
FORBIDDEN_HOSTS = ("amazonaws.com", "openai.com", "anthropic.com", "sendgrid.net",
                   "stripe.com", "googleapis.com", "okta.com")

IMPORT_ROWS = [
    {"Company": "Harborline", "Domain": "harborline.com", "ARR": "125000000"},
    {"Company": "Quill Systems", "Domain": "quillsystems.com", "ARR": "64000000"},
    {"Company": "Bad Row", "Domain": "badrow.com", "ARR": "not a number"},
]

CHAT_QUESTION = "How many companies do I own?"
UNANSWERABLE_QUESTION = "What is the weather in Lisbon tomorrow?"

_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
_ASSET_RE = re.compile(r'(?:src|href)="([^"]+\.(?:js|css|mjs))"', re.I)
_LINK_RE = re.compile(r'href="(/[^"#?]*)"')


def settle() -> None:
    """The one sanctioned sleep: a bounded wait before asserting a non-event."""
    time.sleep(SETTLE_SECONDS)


def unique(stem: str) -> str:
    return f"{stem}-{os.urandom(4).hex()}"


def session(email: str) -> httpx.Client:
    """A fresh bearer token per call, so no fixture caches one across a run."""
    return appclient.client(appclient.login(email, PASSWORD))


def inbox():
    return capabilities.make_inbox()


def backend():
    return capabilities.make_backend()


def backend_count(table: str) -> int:
    return backend().count(table)


def backend_rows(table: str, limit=None) -> list:
    return backend().rows(table, limit=limit)


def absolute(reference: str) -> str:
    if reference.startswith("http://") or reference.startswith("https://"):
        return reference
    return f"{appclient.app_url()}{reference if reference.startswith('/') else '/' + reference}"


def head_title(html: str) -> str:
    found = _TITLE_RE.search(html)
    return found.group(1).strip() if found else ""


def head_meta(html: str, name: str) -> str:
    pattern = re.compile(
        r'<meta[^>]+(?:name|property)="%s"[^>]+content="([^"]*)"' % re.escape(name),
        re.I)
    found = pattern.search(html)
    if found:
        return found.group(1).strip()
    pattern = re.compile(
        r'<meta[^>]+content="([^"]*)"[^>]+(?:name|property)="%s"' % re.escape(name),
        re.I)
    found = pattern.search(html)
    return found.group(1).strip() if found else ""


def asset_urls(html: str) -> list:
    return sorted(set(_ASSET_RE.findall(html)))


def internal_links(html: str) -> list:
    return sorted({href for href in _LINK_RE.findall(html)
                   if not href.startswith("//")})


def timed(call) -> float:
    started = time.monotonic()
    call()
    return time.monotonic() - started


def race(first, second) -> list:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(first), pool.submit(second)]
        return [future.result() for future in futures]


def wait_for_email(recipient: str, subject_contains: str):
    deadline = time.monotonic() + POLL_DEADLINE
    box = inbox()
    while time.monotonic() < deadline:
        message = box.find(recipient, subject_contains)
        if message is not None:
            return message
        settle()
    return None


def wait_for_runs(client: httpx.Client, workflow_id, at_least: int) -> list:
    deadline = time.monotonic() + POLL_DEADLINE
    runs = []
    while time.monotonic() < deadline:
        response = client.get(f"/workflows/{workflow_id}/runs")
        if response.status_code == 200:
            runs = _shapes.items(response.json())
            if len(runs) >= at_least:
                return runs
        settle()
    return runs


def wait_for_events(client: httpx.Client, after, at_least: int) -> list:
    deadline = time.monotonic() + POLL_DEADLINE
    rows = []
    while time.monotonic() < deadline:
        response = client.get("/events", params={"after": after})
        if response.status_code == 200:
            rows = _shapes.items(response.json())
            if len(rows) >= at_least:
                return rows
        settle()
    return rows
