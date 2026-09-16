"""Fixtures, domain helpers and the pinned literals for Remixable Timeline Editor.

No test_* function lives here (G10). Every value test_output.py asserts about the SEEDED
world is pinned in this file and appears verbatim in instruction.md (G6). Per-run probe
values are generated here and are only ever compared against themselves.

The shared grader (appclient, capabilities, _shapes) is supplied by the deku-verifier-base
image on PYTHONPATH=/tests. Nothing here imports a provider SDK.
"""

from __future__ import annotations

import concurrent.futures
import datetime
import os
import struct
import time
import zlib

import httpx
import pytest

import _shapes
import appclient
import capabilities

MEMBER_EMAIL = "member@example.com"
MEMBER2_EMAIL = "member2@example.com"
MEMBER3_EMAIL = "member3@example.com"
MEMBER4_EMAIL = "member4@example.com"
REVIEWER_EMAIL = "reviewer@example.com"
REVIEWER2_EMAIL = "reviewer2@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"
SEEDED_EMAILS = (MEMBER_EMAIL, MEMBER2_EMAIL, MEMBER3_EMAIL, MEMBER4_EMAIL,
                 REVIEWER_EMAIL, REVIEWER2_EMAIL)

ROLE_MEMBER = "member"
ROLE_REVIEWER = "reviewer"
RELATION_OWNER = "owner"

WS_JUNIPER = "Juniper Goods"
WS_SOLO = "Solo Sketchbook"
WS_BENCH = "Basic Bench"

PLAN_FREE = "free"
PLAN_BASIC = "basic"
PLAN_PRO = "pro"
PLAN_BUSINESS = "business"
PLAN_ENTERPRISE = "enterprise"
PLAN_ORDER = (PLAN_FREE, PLAN_BASIC, PLAN_PRO, PLAN_BUSINESS, PLAN_ENTERPRISE)
MONTHLY = "monthly"
ANNUAL = "annual"
CURRENCY = "usd"
PRICES = {PLAN_FREE: (0, 0), PLAN_BASIC: (2500, 1800), PLAN_PRO: (3800, 3000),
          PLAN_BUSINESS: (7000, 5900)}
SAVINGS = {PLAN_BASIC: 28, PLAN_PRO: 21, PLAN_BUSINESS: 16}

METER_STORAGE = "storage_bytes"
METER_VARIATIONS = "project_variations"
METER_CAPTION = "caption_minutes"
METER_SPEECH = "speech_characters"
METER_KITS = "brand_kits"
METER_BLOCKS = "saved_blocks"
METER_MEMBERS = "members"
METERS = (METER_STORAGE, METER_VARIATIONS, METER_CAPTION, METER_SPEECH, METER_KITS,
          METER_BLOCKS, METER_MEMBERS)
GIGABYTE = 1073741824

QUOTA_ERROR = "quota_exceeded"
NOT_FOUND_ERROR = "not_found"
MSG_MONTHLY_BASIC = "You've used all your project variations for this month. Basic includes 20."
MSG_CEILING_FREE_BLOCKS = "Free includes 5 saved blocks. Remove one or upgrade to add more."
MSG_KITS_BASIC = "Brand kits are not included in Basic. Upgrade to Pro to use them."
MSG_SEAT_CAP = "Pro includes up to 10 members. Upgrade to Business to add more."
MSG_SINGLE_FREE = "Free is for one person. Upgrade to Pro to invite your team."
MSG_SINGLE_BASIC_OPENING = "Basic is for one person."
MSG_ENTERPRISE = "Enterprise is arranged through Contact Sales."
MSG_SWITCH_FREE = "Free is for one person. Remove the other members before switching."
MSG_PREMIUM_FREE = "Premium templates are not included in Free. Upgrade to Basic to use them."
MSG_DESCRIBE_NOMATCH = ("Describe matched no blocks. Try naming an effect such as Glow or "
                        "Halftone.")
MSG_SHARE_OPEN = "Anyone with this link can view this version."
MSG_SHARE_NAMED = "Only the people you named can view this version."
MSG_SHARE_NEEDS_EXPORT = "Export this version before sharing it."
MSG_SUPERSEDED = "A newer version exists. You're viewing the version you were sent."
MSG_REPLACED = "This version has been replaced. Ask the sender for the latest link."
MSG_EXPIRED = "This link has expired. Ask the sender for a new one."
MSG_ORPHANED = "The moment this comment referred to has been edited out."
MSG_RENDERING = "Rendering. We'll let you know when it's ready."
MSG_EXPORT_FAILED = "That export didn't finish. We haven't counted it against your quota."
MSG_WAIT_ONE = "Waiting on 1 reviewer."
MSG_WAIT_TWO = "Waiting on 2 reviewers."
NOT_FOUND_HEADING = "We couldn't find that page."
PRICING_HEADING = "Unlimit your creativity."
SAVE_UP_TO = "Save up to 28%"
MOST_POPULAR = "Most popular"
PRO_MEMBER_LINE = "Max 10 team members"
STATEMENT = ("Ferment is the first video editor where creatives can build and remix custom "
             "design tools right on timeline.")
HERO_HEADING = "Engineered for Creativity"
TAGLINE = "Add Ferment"
COPYRIGHT = "Copyright (C) 2026 Ferment"
CONTACT_FIRST_QUESTION = "What can we help with?"
PLUGIN_ROUTE = "/figma-plugin"

TITLES = {
    "/": "Ferment Video : Online Video Editor Engineered for Creativity",
    "/product": "Creative Code Video Editor & Motion Design Tools : Ferment",
    "/pricing": "Pricing : Ferment",
    "/contact": "Contact Ferment : Video Editor Sales & Support",
    "/blog": "Ferment Blog",
    "/login": "Login to Ferment",
    "/register": "Sign up",
    "/templates": "Templates : Ferment",
    "/blocks": "Blocks : Ferment",
    "/privacy-policy": "Privacy Policy : Ferment",
}
EXPLORE_TITLE = "Explore : Ferment"
PUBLIC_ROUTES = ("/", "/product", "/pricing", "/templates", "/blocks", "/blog", "/contact",
                 "/privacy-policy", "/cookie-policy", "/terms-of-service", "/login",
                 "/register", "/figma-plugin")
LEGAL_ROUTES = ("/privacy-policy", "/cookie-policy", "/terms-of-service")
GUARDED_ROUTES = ("/projects", "/explore", "/favorites", "/brand-kits",
                  "/workspace/members", "/workspace/billing", "/settings", "/review")
NAV_ITEMS = ("Product", "Blocks", "Templates", "Pricing", "Blog")
FOOTER_COLUMNS = ("Explore", "Socials", "Resources", "Legal")
SOCIAL_NETWORKS = ("Instagram", "Youtube", "LinkedIn", "Pinterest")
PILLARS = ("Import", "Edit", "Enhance", "Ship")
THREE_WAYS_LINES = (
    "Start from templates and pre-built blocks designed for real campaigns.",
    "Name the effects you want in plain words and get a new variation to refine.",
    "Write your own block, declare its controls, and share it with your team.",
)
PRODUCTION_LINES = (
    "Ferment makes it simple to scale your creative to every common size and format and try "
    "out new variants with a few clicks.",
    "One timeline becomes every size a campaign needs, each variation counted against your "
    "plan.",
)
CREATOR_NAMES = ("Kiln Collective", "Halfstep Motion", "Oriel Park")
CREATOR_SLUGS = ("kiln-collective", "halfstep-motion", "oriel-park")

COMPARISON_ROWS = (
    "Cloud storage", "Export Quality", "AI Auto-captioning", "AI Text to Speech",
    "AI background removal", "Multiple brand kits", "Custom fonts", "Save custom components",
    "Save designs as custom templates", "Export as GIF (great for emails!)",
    "Export as JPEG and PNG", "Premium templates", "Flexible components",
    "Text presets and templates", "Free stock photos", "Free stock video",
    "Free stock audio", "Free fonts",
)
COMING_SOON_ROWS = (
    "AI Auto-captioning", "AI Text to Speech", "AI background removal",
    "Save designs as custom templates", "Free stock photos", "Free stock video",
    "Free stock audio", "Free fonts",
)
FEATURE_COMING_SOON = "coming_soon"
FEATURE_AVAILABLE = "available"

LIBRARY_BLOCKS = ("Inflate", "Glow", "Focus", "Halftone", "Carousel", "Ticker", "Orbit Card",
                  "Ripple")
BLOCK_GLOW = "Glow"
BLOCK_HALFTONE = "Halftone"
BLOCK_TICKER = "Ticker"
CONTROL_KINDS = ("dial", "slider", "prompt", "code")
CATEGORY_TEXT = "Text"
TEMPLATE_CATEGORIES = ("Apparel", "Beauty", "Food & Beverage", "Software / Apps")
TEMPLATE_UUIDS = (
    "5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b01", "5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b02",
    "5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b03", "5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b04",
    "5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b05", "5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b06",
    "5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b07", "5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b08",
)
DENIM_UUID = "5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b01"
FEATURE_REVEAL_UUID = "5b0c6f1e-2d3a-4f8b-9c71-0a1e2d3c4b06"
PREMIUM_NAMES = ("Night Cream Ritual", "Feature Reveal")
DENIM_NAME = "Denim Drop"
ITEM_TITLE = "title-1"
ITEM_CLIP = "clip-3"

DENIM_REMIX = "Denim Drop remix"
BENCH_PROMO = "Bench Promo"
FIRST_SKETCH = "First Sketch"
SPIN_FOREVER = "Spin Forever"
JUNIPER_KITS = ("Juniper Core", "Juniper Holiday", "Juniper Outdoor", "Juniper Kids")
JUNIPER_BLOCKS = ("Juniper Lower Third", "Juniper Price Tag", "Spin Forever")
SOLO_BLOCKS = ("Sketch Title", "Sketch Underline", "Sketch Sticker", "Sketch Wipe")
COMMENT_GLOW = "Can the glow start softer?"
COMMENT_HOLD = "Hold this shot a beat longer."
JUNIPER_PLAN_CHARGE = 7600
CREW_EMAILS = tuple(f"crew{n}@example.com" for n in range(1, 8))

SHARE_OPEN = "k7Qm2pVx9LwR4tNz"
SHARE_EXPIRED = "pQ4rT8vW2yZ6aB3c"
SHARE_PASSPHRASE_TOKEN = "mN5bV7cX1zL3kJ9h"
SHARE_PASSPHRASE = "orchard-lantern-42"
SHARE_NAMED = "dR2fG6hJ8kL0pQ1s"
STALE_KEY = "stale-bench-1"

CUSTOMERS = (
    "Northwind Apparel", "Kestrel Foods", "Lumen Skin", "Parcel & Pine", "Harlow Coffee",
    "Brightline Apps", "Velo Outfitters", "Marigold Beauty", "Stonefruit Kitchen",
    "Quartz Labs", "Tidewater Denim", "Orchid Cosmetics", "Copperleaf Tea", "Signal Grove",
    "Fieldnote Studio", "Saltmarsh Swim", "Juniper Goods", "Aster Pharmacy",
    "Longhand Paper", "Mosaic Media", "Pebble Toys", "Riverbend Bikes", "Cinder Candles",
    "Glasshouse Juice",
)
WITHDRAWN_CUSTOMER = "Ashgrove Motors"
BLOG_SLUGS = ("blocks-not-clips", "tuning-a-glow-in-four-moves",
              "how-juniper-goods-ships-weekly")
BLOG_CATEGORIES = ("Product", "Tutorials", "Customer Stories")
AUDIENCE_SALES = "sales"
AUDIENCE_SUPPORT = "support"
CONTACT_PREFIX = "FC-"

CONSENT_OPTIONAL = ("functionality", "experience", "measurement", "marketing")
CONSENT_MEASUREMENT = "measurement"

INTERFACE_SCALES = (100, 115, 130, 150)
STATUS_RENDERING = "rendering"
STATUS_READY = "ready"
STATUS_FAILED = "failed"
KIND_PLAN_CHANGE = "plan_change"
KIND_SEAT_ADDED = "seat_added"
STATE_PENDING = "pending"
STATE_APPROVED = "approved"
STATE_CHANGES = "changes_requested"
STATE_NOT_REQUESTED = "not_requested"
PROJECT_OUTDATED = "outdated"
COMMENT_ANCHORED = "anchored"
COMMENT_ORPHANED = "orphaned"
COMMENT_UNANCHORED = "unanchored"
INVITE_PENDING = "pending"
SUPERSEDED_CLOSED = "closed"
ASSET_PREFIX = "assets/"
EXPORT_PREFIX = "exports/"

TABLE_ACCOUNT = "account"
TABLE_WORKSPACE = "workspace"
TABLE_MEMBER = "workspace_member"
TABLE_INVITATION = "invitation"
TABLE_PLAN = "plan"
TABLE_QUOTA = "quota"
TABLE_SUBSCRIPTION = "subscription"
TABLE_CHARGE = "charge"
TABLE_METER = "meter_balance"
TABLE_USAGE = "usage_event"
TABLE_BLOCK = "block"
TABLE_BLOCK_VERSION = "block_version"
TABLE_TEMPLATE = "template"
TABLE_ASSET = "asset"
TABLE_PROJECT = "project"
TABLE_VERSION = "project_version"
TABLE_EXPORT = "export_job"
TABLE_SHARE = "share_link"
TABLE_SHARE_VIEW = "share_view"
TABLE_COMMENT = "comment"
TABLE_APPROVAL = "approval_request"
TABLE_NOTIFICATION = "notification"
TABLE_CONSENT = "consent_record"
TABLE_MARKETING_VIEW = "marketing_view"
TABLE_CONTACT = "contact_request"
TABLE_CUSTOMER = "customer_logo"

SETTLE_SECONDS = 0.25
POLL_TIMEOUT_SECONDS = 20.0



def settle() -> None:
    """Yield briefly so an asynchronous side effect can land."""
    time.sleep(SETTLE_SECONDS)


def poll_until(predicate, timeout: float = POLL_TIMEOUT_SECONDS):
    """Bounded poll on a monotonic clock; returns the last value the predicate saw."""
    deadline = time.monotonic() + timeout
    value = None
    while time.monotonic() < deadline:
        value = predicate()
        if value:
            return value
        settle()
    return value


def unique_suffix() -> str:
    return os.urandom(5).hex()


def probe_address(suffix: str) -> str:
    """A per-run address, only ever compared against itself."""
    return "probe-" + suffix + "@" + "example.com"


def probe_password(suffix: str) -> str:
    return "probe-pass-" + suffix


def describe(response: httpx.Response, what: str) -> str:
    """The failure-message shape reference/J requires: anchor, request, status, body."""
    return (f"{what}: {response.request.method} {response.request.url} returned "
            f"{response.status_code}: {response.text[:400]}")


def backend() -> capabilities.Backend:
    return capabilities.make_backend()


def object_store() -> capabilities.ObjectStore:
    return capabilities.make_store()


def api(token: str | None = None) -> httpx.Client:
    return appclient.client(token)


def login(email: str, password: str = SEEDED_PASSWORD) -> str:
    return appclient.login(email, password)


def body_of(response: httpx.Response):
    """The JSON body, or an empty object when the response carries no JSON."""
    if "json" not in response.headers.get("content-type", ""):
        return {}
    return response.json()


def message_of(response: httpx.Response) -> str:
    payload = body_of(response)
    return payload.get("message", "") if isinstance(payload, dict) else ""


def listing(response: httpx.Response) -> list:
    assert response.status_code == 200, describe(response, "a list endpoint must answer 200")
    return _shapes.items(response.json())


def is_client_error(response: httpx.Response) -> bool:
    """A refusal: any 4xx, never a 5xx and never a silent success."""
    return 400 <= response.status_code < 500


def accepted(response: httpx.Response) -> bool:
    """A successful create or action: 200, 201 or 202."""
    return 200 <= response.status_code <= 202


def denied(response: httpx.Response) -> bool:
    """Denied, forbidden, or answered as though the thing does not exist."""
    return response.status_code in (401, 403, 404)


def fetch_document(path: str, token: str | None = None,
                   follow: bool = True) -> httpx.Response:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.get(appclient.app_url() + path, timeout=appclient.TIMEOUT,
                     follow_redirects=follow, headers=headers)


def document_title(markup: str) -> str:
    lower = markup.lower()
    start = lower.find("<title")
    if start < 0:
        return ""
    open_end = lower.find(">", start)
    close = lower.find("</title>", open_end)
    if open_end < 0 or close < 0:
        return ""
    return unescape(markup[open_end + 1:close].strip())


def unescape(text: str) -> str:
    return (text.replace("&amp;", "&").replace("&#39;", "'").replace("&#x27;", "'")
            .replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">"))


def page_text(markup: str) -> str:
    return unescape(markup)


def head_tags(markup: str, tag: str) -> list[str]:
    lower = markup.lower()
    end = lower.find("</head>")
    head = markup[:end] if end > 0 else markup
    found, cursor = [], 0
    low_head = head.lower()
    while True:
        at = low_head.find("<" + tag, cursor)
        if at < 0:
            return found
        close = low_head.find(">", at)
        if close < 0:
            return found
        found.append(head[at:close + 1])
        cursor = close + 1


def attribute(tag: str, name: str) -> str:
    low = tag.lower()
    for quote in ('"', "'"):
        marker = f"{name}={quote}"
        at = low.find(marker)
        if at >= 0:
            rest = tag[at + len(marker):]
            stop = rest.find(quote)
            return rest[:stop] if stop >= 0 else rest
    return ""


def meta_description(markup: str) -> str:
    for tag in head_tags(markup, "meta"):
        if attribute(tag, "name").lower() == "description":
            return unescape(attribute(tag, "content").strip())
    return ""


def favicon_href(markup: str) -> str:
    for tag in head_tags(markup, "link"):
        rel = attribute(tag, "rel").lower().split()
        if "icon" in rel:
            return attribute(tag, "href")
    return ""


def internal_links(markup: str) -> list[str]:
    found, cursor = [], 0
    lower = markup.lower()
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
            found.append(href.split("#")[0].split("?")[0] or "/")


def external_sources(markup: str) -> list[str]:
    """Absolute script, style, font or image sources a document loads from another origin."""
    own = appclient.app_url()
    found = []
    for marker in ('src="', 'rel="stylesheet" href="', "url("):
        lower = markup.lower()
        cursor = 0
        while True:
            at = lower.find(marker, cursor)
            if at < 0:
                break
            rest = markup[at + len(marker):]
            stop = min([i for i in (rest.find('"'), rest.find(")")) if i >= 0] or [0])
            cursor = at + len(marker) + max(stop, 1)
            value = rest[:stop].strip().strip("'")
            if value.startswith("http") and not value.startswith(own):
                found.append(value)
    return found


def signup(suffix: str, **extra) -> dict:
    body = {"email": probe_address(suffix), "password": probe_password(suffix),
            "display_name": "Probe " + suffix}
    body.update(extra)
    with api() as client:
        response = client.post("/auth/signup", json=body)
    assert accepted(response), describe(response, "an open signup must succeed")
    payload = response.json()
    assert payload.get("access_token"), describe(response, "a signup must return a token")
    return {"token": payload["access_token"], "email": body["email"],
            "password": body["password"], "workspace_id": payload.get("workspace_id"),
            "payload": payload}


def workspaces(token: str) -> list:
    with api(token) as client:
        return listing(client.get("/workspaces"))


def workspace_id(token: str, name: str | None = None):
    rows = workspaces(token)
    if name is None:
        owned = [w for w in rows if w.get("relation") == RELATION_OWNER]
        assert owned, f"the caller owns no workspace: {rows}"
        return owned[0]["id"]
    named = sorted((w for w in rows if w.get("name") == name), key=lambda w: w["id"])
    assert named, f"the caller does not belong to {name!r}: {rows}"
    return named[0]["id"]


def change_plan(token: str, ws, plan: str, period: str = MONTHLY) -> httpx.Response:
    with api(token) as client:
        return client.post(f"/workspaces/{ws}/subscription",
                           json={"plan_key": plan, "billing_period": period})


def probe_workspace(plan: str = PLAN_FREE, period: str = MONTHLY) -> dict:
    """A brand-new member with a workspace of its own on the requested plan."""
    probe = signup(unique_suffix())
    ws = probe["workspace_id"] or workspace_id(probe["token"])
    probe["ws"] = ws
    if plan != PLAN_FREE:
        response = change_plan(probe["token"], ws, plan, period)
        assert accepted(response), describe(
            response, f"the owner must be able to move a workspace to {plan}")
    return probe


def subscription(token: str, ws) -> dict:
    with api(token) as client:
        response = client.get(f"/workspaces/{ws}/subscription")
    assert response.status_code == 200, describe(response, "the subscription must be readable")
    return response.json()


def usage(token: str, ws, meter: str) -> dict:
    with api(token) as client:
        rows = listing(client.get(f"/workspaces/{ws}/usage"))
    found = [r for r in rows if r.get("meter") == meter]
    assert found, f"the usage list carries no row for {meter}: {rows}"
    return found[0]


def charges(token: str, ws) -> list:
    with api(token) as client:
        return listing(client.get(f"/workspaces/{ws}/charges"))


def library_block(name: str) -> dict:
    with api() as client:
        rows = listing(client.get("/blocks", params={"q": name}))
    found = [b for b in rows if b.get("name") == name]
    assert found, f"the library carries no block named {name!r}: {rows}"
    with api() as client:
        detail = client.get(f"/blocks/{found[0]['id']}")
    assert detail.status_code == 200, describe(detail, f"the {name} block must be readable")
    return detail.json()


def make_project(token: str, ws, width: int = 1280, height: int = 720, fps: int = 30,
                 duration_ms: int = 6000, name: str | None = None) -> dict:
    body = {"name": name or "Probe Project " + unique_suffix(), "canvas_width": width,
            "canvas_height": height, "fps": fps, "duration_ms": duration_ms}
    with api(token) as client:
        response = client.post(f"/workspaces/{ws}/projects", json=body)
    assert accepted(response), describe(response, "a member must create a project")
    return response.json()


def get_project(token: str, ws, pid) -> dict:
    with api(token) as client:
        response = client.get(f"/workspaces/{ws}/projects/{pid}")
    assert response.status_code == 200, describe(response, "a project must be readable")
    return response.json()


def seeded_project(token: str, ws, name: str) -> dict:
    with api(token) as client:
        rows = listing(client.get(f"/workspaces/{ws}/projects"))
    named = sorted((p for p in rows if p.get("name") == name), key=lambda p: p["id"])
    assert named, f"no project named {name!r}: {rows}"
    return get_project(token, ws, named[0]["id"])


def glow_item(item_id: str, start: int, duration: int, glow: dict, **params) -> dict:
    values = {"text": "Glow", "intensity": 60, "hue": 45}
    values.update(params)
    return {"id": item_id, "type": "block", "start_ms": start, "duration_ms": duration,
            "block_id": glow["id"], "block_version": glow.get("current_version", 1),
            "params": values}


def timeline_of(*tracks) -> dict:
    return {"tracks": [{"id": f"track-{n}", "label": f"Track {n}", "items": list(items)}
                       for n, items in enumerate(tracks, 1)]}


def save_timeline(token: str, ws, pid, base_revision: int, timeline: dict) -> httpx.Response:
    with api(token) as client:
        return client.put(f"/workspaces/{ws}/projects/{pid}/timeline",
                          json={"base_revision": base_revision, "timeline": timeline})


def freeze_version(token: str, ws, pid) -> dict:
    with api(token) as client:
        response = client.post(f"/workspaces/{ws}/projects/{pid}/versions")
    assert accepted(response), describe(response, "a member must freeze a version")
    return response.json()


def request_export(token: str, ws, vid, width: int, height: int, fmt: str = "png",
                   key: str | None = None, fps: int = 30) -> httpx.Response:
    body = {"format": fmt, "width": width, "height": height, "fps": fps,
            "request_key": key or "probe-" + unique_suffix()}
    with api(token) as client:
        return client.post(f"/workspaces/{ws}/versions/{vid}/exports", json=body)


def export_job(token: str, ws, eid) -> dict:
    with api(token) as client:
        response = client.get(f"/workspaces/{ws}/exports/{eid}")
    assert response.status_code == 200, describe(response, "an export job must be readable")
    return response.json()


def upload_export(token: str, ws, eid, data: bytes, content_type: str) -> httpx.Response:
    with api(token) as client:
        return client.put(f"/workspaces/{ws}/exports/{eid}/file", content=data,
                          headers={"Content-Type": content_type})


def fail_export(token: str, ws, eid) -> httpx.Response:
    with api(token) as client:
        return client.post(f"/workspaces/{ws}/exports/{eid}/fail",
                           json={"reason": "probe released"})


def png_bytes(width: int, height: int) -> bytes:
    """A valid PNG whose IHDR declares width x height; the pixels are blank rows."""
    def chunk(kind: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)
    header = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)
    raw = (b"\x00" + b"\x00" * width) * height
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def gif_bytes(width: int, height: int) -> bytes:
    """A minimal GIF89a whose logical screen declares width x height."""
    return (b"GIF89a" + struct.pack("<HH", width, height) + b"\x00\x00\x00"
            + b"\x2c" + struct.pack("<HHHH", 0, 0, 1, 1) + b"\x00"
            + b"\x02\x02\x44\x01\x00" + b"\x3b")


def mp4_bytes() -> bytes:
    """An ISO base media header: an ftyp box at byte 4, then an empty mdat box."""
    ftyp = struct.pack(">I", 24) + b"ftyp" + b"isom" + struct.pack(">I", 512) + b"isomiso2"
    return ftyp + struct.pack(">I", 8) + b"mdat"


def ready_version(token: str, ws, width: int = 1280, height: int = 720) -> dict:
    """A project with one frozen version whose canvas-sized png export is ready."""
    project = make_project(token, ws, width, height)
    version = freeze_version(token, ws, project["id"])
    response = request_export(token, ws, version["id"], width, height)
    assert accepted(response), describe(response, "a canvas-sized export must start")
    job = response.json()
    upload = upload_export(token, ws, job["id"], png_bytes(width, height), "image/png")
    assert accepted(upload), describe(upload, "a matching png must be accepted")
    return {"project": project, "version": version, "export": upload.json()}


def create_share(token: str, ws, vid, **settings) -> httpx.Response:
    body = {"allow_download": False, "allow_comments": True}
    body.update(settings)
    with api(token) as client:
        return client.post(f"/workspaces/{ws}/versions/{vid}/shares", json=body)


def share_views(token: str, ws, sid) -> list:
    with api(token) as client:
        return listing(client.get(f"/workspaces/{ws}/shares/{sid}/views"))


def share_client(token: str | None = None) -> httpx.Client:
    return appclient.client(token)


def run_together(*calls):
    """Start every call at once and return their results in order."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(calls)) as pool:
        futures = [pool.submit(call) for call in calls]
        return [f.result() for f in futures]


def today_utc() -> datetime.date:
    return datetime.datetime.now(datetime.timezone.utc).date()


def date_of(stamp: str) -> datetime.date:
    return datetime.date.fromisoformat(str(stamp)[:10])


def prorated_cents(price: int, start: str, end: str, joined: datetime.date) -> int:
    """round_half_up(price x remaining_days / period_days), as the brief states it."""
    period_days = (date_of(end) - date_of(start)).days
    remaining = (date_of(end) - joined).days
    numerator = price * remaining
    whole, rest = divmod(numerator, period_days)
    return whole + (1 if rest * 2 >= period_days else 0)


def refusal_pattern(meter: str, plan: str, first_plan: str) -> str:
    """The brief's not-included pattern: <Meter> are not included in <plan>. Upgrade to ..."""
    return f"{meter} are not included in {plan}. Upgrade to {first_plan} to use them."


def ceiling_pattern(plan: str, limit: int, meter: str) -> str:
    """The brief's ceiling pattern: <plan> includes <limit> <meter>. Remove one or ..."""
    return f"{plan} includes {limit} {meter}. Remove one or upgrade to add more."


def custom_block_body(suffix: str, **overrides) -> dict:
    body = {"name": "Probe Block " + suffix, "category": CATEGORY_TEXT,
            "parameter_schema": [
                {"key": "headline", "label": "Headline", "control": "prompt",
                 "max_length": 40, "default": "Probe"},
                {"key": "slide", "label": "Slide", "control": "slider", "min": 0,
                 "max": 100, "default": 30},
                {"key": "turn", "label": "Turn", "control": "dial", "default": 90},
            ],
            "source": "export function draw(ctx, t, p) { return p.slide + " + str(len(suffix)) + "; }"}
    body.update(overrides)
    return body


def save_block(token: str, ws, body: dict) -> httpx.Response:
    with api(token) as client:
        return client.post(f"/workspaces/{ws}/blocks", json=body)


def delete_block(token: str, ws, bid) -> httpx.Response:
    with api(token) as client:
        return client.delete(f"/workspaces/{ws}/blocks/{bid}")


def invite(token: str, ws, email: str) -> httpx.Response:
    with api(token) as client:
        return client.post(f"/workspaces/{ws}/invitations", json={"email": email})


def revoke(token: str, ws, invitation_id) -> httpx.Response:
    with api(token) as client:
        return client.delete(f"/workspaces/{ws}/invitations/{invitation_id}")


def join_workspace(owner_token: str, ws) -> dict:
    """A fresh member invited by the owner who signs up and accepts."""
    guest = signup(unique_suffix())
    response = invite(owner_token, ws, guest["email"])
    assert accepted(response), describe(response, "the owner must be able to invite")
    token = response.json()["token"]
    with api(guest["token"]) as client:
        accepted = client.post(f"/invitations/{token}/accept")
    assert accepted(accepted), describe(accepted, "the invitee must be able to accept")
    guest["invitation"] = response.json()
    return guest


def account_id(token: str, ws, email: str):
    with api(token) as client:
        rows = listing(client.get(f"/workspaces/{ws}/members"))
    found = [m for m in rows if m.get("email") == email]
    assert found, f"{email} is not listed as a member: {rows}"
    return found[0]["account_id"]


def request_approval(token: str, ws, vid, emails: list[str]) -> httpx.Response:
    with api(token) as client:
        return client.post(f"/workspaces/{ws}/versions/{vid}/approval-requests",
                           json={"reviewer_emails": emails})


def accept_review_invite(invite_url: str, suffix: str) -> dict:
    token = invite_url.rstrip("/").rsplit("/", 1)[-1]
    with api() as client:
        response = client.post(f"/review-invites/{token}/accept",
                               json={"password": probe_password(suffix),
                                     "display_name": "Probe Reviewer " + suffix})
    assert accepted(response), describe(response, "a review invitation must accept")
    return response.json()


def storage_url(key: str) -> str:
    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    return f"{endpoint}/{os.environ['STORAGE_BUCKET']}/{key}"


@pytest.fixture()
def suffix() -> str:
    return unique_suffix()


@pytest.fixture()
def owner() -> str:
    return login(MEMBER_EMAIL)


@pytest.fixture()
def teammate() -> str:
    return login(MEMBER2_EMAIL)


@pytest.fixture()
def solo() -> str:
    return login(MEMBER3_EMAIL)


@pytest.fixture()
def bench() -> str:
    return login(MEMBER4_EMAIL)


@pytest.fixture()
def reviewer() -> str:
    return login(REVIEWER_EMAIL)


@pytest.fixture()
def second_reviewer() -> str:
    return login(REVIEWER2_EMAIL)
