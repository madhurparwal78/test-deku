from __future__ import annotations

import time
import uuid
from datetime import datetime, timedelta, timezone

import pytest

import appclient
import capabilities

SETTLE_SECONDS = 2.0
POLL_SECONDS = 0.5
POLL_BUDGET = 20.0

EDITOR_EMAIL = "editor@example.com"
EDITOR_PASSWORD = "deku-demo-pw-2026"

PUBLISHED_SLUGS = (
    "alder-cove", "thistle-bay", "rook-hollow", "penmara",
    "glasswater", "highfen", "saltmere", "brindle-tor",
)
PUBLISHED_NAMES = (
    "Alder Cove", "Thistle Bay", "Rook Hollow", "Penmara",
    "Glasswater", "Highfen", "Saltmere", "Brindle Tor",
)
DRAFT_SLUG = "ossary-fen"
DRAFT_NAME = "Ossary Fen"
DRAFT_BROCHURE_TITLE = "Ossary Fen in Winter"
ENTRY_BROCHURE_TITLE = "Alder Cove on Foot"
REGIONAL_BROCHURES = ("Marnavel in Three Days", "The Coast Road", "Backwater Passages")

COLLECTION_SLUGS = ("coastline", "highlands", "backwater")
COLLECTION_NAMES = ("Coastline", "Highlands", "Backwater")
COASTLINE_SLUGS = ("alder-cove", "thistle-bay", "penmara", "saltmere")
HIGHLANDS_SLUGS = ("rook-hollow", "highfen", "brindle-tor")
BACKWATER_SLUGS = ("thistle-bay", "glasswater", "saltmere")

RESERVED_SEGMENTS = (
    "desk", "api", "media", "event", "brochures",
    "photo-gallery", "collection", "destination",
)

ENDED_EVENT = "Penmara Kite Days"
ENDS_TODAY_EVENT = "Highfen Harvest Fair"
NO_END_DATE_EVENT = "Thistle Bay Regatta"
LATEST_EVENT = "Alder Lantern Nights"

FEATURED_SLUGS = ("alder-cove", "thistle-bay", "rook-hollow", "penmara",
                  "glasswater", "highfen")
FEATURED_HEADING = "Worth the detour"

ALDER_COVE_PICTURES = 3
DRAFT_PICTURES = 3
PAGE_SIZE = 24
NAME_MIN = 3
SUMMARY_MAX = 240

DISPLAY_FAMILY = "Playfair Display"
BODY_FAMILY = "IBM Plex Sans Condensed"
NARROW_VIEWPORT = {"width": 390, "height": 844}
WIDE_VIEWPORT = {"width": 1440, "height": 900}
CONTRAST_FLOOR = 4.5
TOUCH_TARGET_MIN = 44

PUBLIC_ROUTES = (
    "/", "/destination", "/collection", "/event", "/brochures", "/photo-gallery",
    "/privacy", "/terms",
)
FACTS = {
    "alder-cove": ("Alder Halt", "May to September", 12),
    "saltmere": ("Saltmere Halt", "April to September", 19),
}
BROCHURE_FILENAMES = {
    "Marnavel in Three Days": "marnavel-in-three-days.pdf",
    "The Coast Road": "the-coast-road.pdf",
}


def settle() -> None:
    time.sleep(SETTLE_SECONDS)


def today_utc():
    return datetime.now(timezone.utc).date()


def days_from_today(n: int) -> str:
    return (today_utc() + timedelta(days=n)).isoformat()


def probe_token() -> str:
    return uuid.uuid4().hex[:10]


def entry_payload(**over) -> dict:
    token = probe_token()
    body = {
        "name": f"Probe Cove {token}",
        "slug": f"probe-cove-{token}",
        "summary": "A probe place written by the checking suite.",
        "guide": "A probe place written by the checking suite, three sentences long. "
                 "It carries a guide body so the required fields are populated. "
                 "Nothing about it is drawn from the seed.",
        "themes": ["coastline"],
        "featured": False,
        "sort_index": 90,
        "transport_point": "Probe Halt",
        "best_months": "May to September",
        "distance_km": 42,
    }
    body.update(over)
    return body


def describe(response) -> str:
    return f"status {response.status_code}, body {response.text[:400]!r}"


def create_draft(client, **over) -> dict:
    payload = entry_payload(**over)
    r = client.post("/desk/entries", json=payload)
    assert r.status_code in (200, 201), (
        f"POST /api/desk/entries for slug {payload['slug']!r} should create a draft: "
        f"{describe(r)}"
    )
    body = r.json()
    assert isinstance(body, dict), (
        f"POST /api/desk/entries should answer one entry object: {describe(r)}"
    )
    return body


def entry_id(entry: dict) -> str:
    assert "id" in entry, f"an entry object carries an id: {entry!r}"
    return str(entry["id"])


def add_picture(client, eid: str, alt_text: str = "A probe picture of the coast.") -> dict:
    token = probe_token()
    target = client.post("/desk/uploads", json={
        "entry_id": eid, "kind": "gallery",
        "filename": f"probe-{token}.jpg", "content_type": "image/jpeg",
    })
    assert target.status_code in (200, 201), (
        f"POST /api/desk/uploads should issue an upload target for entry {eid}: "
        f"{describe(target)}"
    )
    issued = target.json()
    assert "object_key" in issued, (
        f"POST /api/desk/uploads should name the object_key the bytes land at: "
        f"{describe(target)}"
    )
    put_upload(issued, b"probe-picture-bytes")
    r = client.post("/desk/images", json={
        "entry_id": eid, "object_key": issued["object_key"], "alt_text": alt_text,
        "width": 1200, "height": 800, "position": 1,
    })
    assert r.status_code in (200, 201), (
        f"POST /api/desk/images should register the uploaded picture for entry {eid}: "
        f"{describe(r)}"
    )
    registered = r.json()
    registered["object_key"] = issued["object_key"]
    return registered


def put_upload(issued: dict, payload: bytes) -> None:
    import httpx

    url = issued.get("url") or issued.get("upload_url") or issued.get("target")
    assert url, (
        f"the upload target should carry the address the bytes are sent to: {issued!r}"
    )
    method = (issued.get("method") or "PUT").upper()
    headers = issued.get("headers") or {}
    fields = issued.get("fields")
    with httpx.Client(timeout=appclient.TIMEOUT) as raw:
        if fields:
            r = raw.post(url, data=fields, files={"file": payload})
        else:
            r = raw.request(method, url, content=payload, headers=headers)
    assert r.status_code < 400, (
        f"sending the bytes to the issued upload target should succeed: {describe(r)}"
    )


def drop(client, eid: str) -> None:
    client.patch(f"/desk/entries/{eid}", json={"sort_index": 99})


def publish(client, eid: str):
    return client.post(f"/desk/entries/{eid}/publish")


def unpublish(client, eid: str):
    return client.post(f"/desk/entries/{eid}/unpublish")


def slugs_of(rows) -> set:
    out = set()
    for row in rows:
        if isinstance(row, dict) and row.get("slug"):
            out.add(str(row["slug"]))
    return out


def names_of(rows, key: str = "name") -> set:
    out = set()
    for row in rows:
        if isinstance(row, dict) and row.get(key):
            out.add(str(row[key]))
    return out


def json_list(response, label: str) -> list:
    assert response.status_code == 200, f"{label} should answer 200: {describe(response)}"
    body = response.json()
    assert isinstance(body, list), (
        f"{label} should answer a top-level JSON array: {describe(response)}"
    )
    return body


def poll_until(predicate, label: str):
    deadline = time.monotonic() + POLL_BUDGET
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        settle()
    raise AssertionError(f"{label} did not hold within {POLL_BUDGET} seconds; last saw {last!r}")


def relative_luminance(rgb) -> float:
    channels = []
    for raw in rgb:
        c = raw / 255.0
        channels.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg) -> float:
    a = relative_luminance(fg) + 0.05
    b = relative_luminance(bg) + 0.05
    return max(a, b) / min(a, b)


def parse_rgb(value: str):
    digits = []
    current = ""
    for ch in value:
        if ch.isdigit() or ch == ".":
            current += ch
        elif current:
            digits.append(current)
            current = ""
    if current:
        digits.append(current)
    assert len(digits) >= 3, f"a computed colour should carry three channels: {value!r}"
    return tuple(int(float(d)) for d in digits[:3])


@pytest.fixture()
def api():
    with appclient.client() as client:
        yield client


@pytest.fixture()
def desk():
    token = appclient.login(EDITOR_EMAIL, EDITOR_PASSWORD)
    with appclient.client(token) as client:
        yield client


@pytest.fixture()
def anon():
    with appclient.client() as client:
        yield client


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture()
def page():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as driver:
        browser = driver.chromium.launch(args=["--no-sandbox"])
        context = browser.new_context(viewport=WIDE_VIEWPORT)
        opened = context.new_page()
        opened.set_default_timeout(20000)
        try:
            yield opened
        finally:
            context.close()
            browser.close()
