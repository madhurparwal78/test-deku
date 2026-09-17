"""Fixtures, pinned literals and bounded-poll helpers for the Geoform platform.

No test functions live here. Every literal below appears verbatim in
instruction.md, so a grader never asserts a value the brief left the agent to
invent.
"""

from __future__ import annotations

import json
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
POLL_DEADLINE = 90.0
FLOOR_SECONDS = 0.5
DURATION_TOLERANCE = 1.0
MIN_PRERENDERED_CHARS = 400

PASSWORD = appclient.seeded_password("SEEDED_PASSWORD", "deku-demo-pw-2026")
AUTHOR_ONE = "author@example.com"
AUTHOR_TWO = "author2@example.com"
READER = "reader@example.com"
SEEDED_ACCOUNTS = (AUTHOR_ONE, AUTHOR_TWO, READER)

PROJECT_NAME = "Harbor Basemap"
NOT_FOUND_COPY = "Page Not Found"

STORAGE_ENDPOINT = os.environ.get("STORAGE_ENDPOINT", "http://minio:9000")
STORAGE_BUCKET = os.environ.get("STORAGE_BUCKET", "deku")

UPLOAD_STATES = ("queued", "processing", "complete", "failed")
TERMINAL_STATES = ("complete", "failed")
PLACE_TYPES = ("address", "place", "poi", "region")
LAYER_KINDS = ("fill", "line", "symbol", "circle", "fill-extrusion", "heatmap",
               "raster", "hillshade", "sky")
SEEDED_TABLES = ("account", "project", "tileset", "place", "road_segment")

MARKETING_ROUTES = ("/", "/ev", "/v2", "/mts", "/g/d", "/dei", "/esg", "/ja",
                    "/blog", "/pricing", "/contact")

PINNED_COPY = {
    "/": ["Do more with maps & navigation", "Explore Geoform live",
          "Flexibility and control you can trust", "BUILD with Geoform",
          "SUBSCRIBE", "HIRING"],
    "/ev": ["Geoform for EV", "Ready to get started?"],
    "/mts": ["Ready to get started?"],
}

FORBIDDEN_HOSTS = ("amazonaws.com", "googleapis.com", "openai.com", "stripe.com",
                   "mapbox.com", "openstreetmap.org")
BINARY_SUFFIXES = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif", ".mp4",
                   ".webm", ".woff", ".woff2", ".ttf", ".otf", ".glb", ".gltf")

WAYPOINTS = "-1.4700,50.9200;-1.4000,50.9000"
ORIGIN = "-1.4700,50.9200"
DESTINATION = "-1.4000,50.9000"
BUDGETS = "300,600,900"
TOO_MANY_ORIGINS = ";".join(["-1.47,50.92"] * 200)
SMALL_BOUNDS = "-1.4750,50.9150,-1.4650,50.9250"
OFF_ROUTE = {"lon": -1.6000, "lat": 51.1000}
AREA = "harbor-central"
LON, LAT = -1.4700, 50.9200
PLACE_QUERY = "Harbor"
SEARCH_PREFIX = "Har"
NEAR_PLACE = "Harbor Quay"

SAMPLE_DATASET = json.dumps({
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature",
         "geometry": {"type": "Point", "coordinates": [-1.4700, 50.9200]},
         "properties": {"name": "Harbor Quay", "berths": 12}},
        {"type": "Feature",
         "geometry": {"type": "Point", "coordinates": [-1.4650, 50.9180]},
         "properties": {"name": "North Slip", "berths": 4}},
    ],
})

_ASSET_RE = re.compile(r'(?:src|href)="([^"]+)"', re.I)
_TAG_RE = re.compile(r"<[^>]+>")


def settle() -> None:
    """The one sanctioned sleep: a bounded wait before asserting a non-event."""
    time.sleep(SETTLE_SECONDS)


def unique(stem: str) -> str:
    return f"{stem}-{os.urandom(4).hex()}"


def named_dataset(name: str) -> str:
    return json.dumps({
        "type": "FeatureCollection",
        "features": [{"type": "Feature",
                      "geometry": {"type": "Point", "coordinates": [LON, LAT]},
                      "properties": {"name": name}}],
    })


def session(email: str) -> httpx.Client:
    """A fresh bearer token per call, so no fixture caches one across a run."""
    return appclient.client(appclient.login(email, PASSWORD))


def keyed(secret: str) -> httpx.Client:
    return httpx.Client(base_url=appclient.api_base(), timeout=TIMEOUT,
                        headers={"Authorization": f"Bearer {secret}"})


def store():
    return capabilities.make_store()


def backend():
    return capabilities.make_backend()


def backend_count(table: str) -> int:
    return backend().count(table)


def visible_text(html: str) -> str:
    return " ".join(_TAG_RE.sub(" ", html).split())


def asset_refs(html: str) -> list:
    return sorted(set(_ASSET_RE.findall(html)))


def timed(call) -> float:
    started = time.monotonic()
    call()
    return time.monotonic() - started


def race(first, second) -> list:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(first), pool.submit(second)]
        return [future.result() for future in futures]


def service_total(usage, service: str) -> int:
    for row in _shapes.items(usage):
        if str(row.get("service")) == service:
            return int(row.get("count") or 0)
    return 0


def first_cell(payload) -> float:
    durations = payload.get("durations") if isinstance(payload, dict) else None
    assert durations, f"the matrix response carries no durations: {payload}"
    row = durations[0]
    return float(row[0] if isinstance(row, list) else row)


def ring_area(polygon) -> float:
    """Shoelace area of the first ring, so nesting can be compared."""
    coords = polygon.get("coordinates") if isinstance(polygon, dict) else polygon
    while coords and isinstance(coords[0], list) and coords[0] and isinstance(coords[0][0], list):
        coords = coords[0]
    total = 0.0
    for i in range(len(coords)):
        x1, y1 = coords[i][0], coords[i][1]
        x2, y2 = coords[(i + 1) % len(coords)][0], coords[(i + 1) % len(coords)][1]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2.0


def seeded_project(client: httpx.Client) -> dict:
    rows = _shapes.items(client.get("/projects").json())
    for row in rows:
        if str(row.get("name")) == PROJECT_NAME:
            return row
    assert rows, f"no project is visible; the seed carries {PROJECT_NAME!r}"
    return rows[0]


def current_version(client: httpx.Client, project_id) -> int:
    project = client.get(f"/projects/{project_id}").json()
    version = project.get("version") or project.get("current_version")
    assert version is not None, f"the project reports no current version: {project}"
    return version


def seeded_private_tileset(client: httpx.Client) -> dict:
    rows = _shapes.items(client.get("/tilesets").json())
    private = [row for row in rows if str(row.get("visibility")) == "private"]
    assert private, f"the account owns no private tileset: {rows}"
    return private[0]


def published_tileset(client: httpx.Client) -> dict:
    rows = _shapes.items(client.get("/tilesets").json())
    public = [row for row in rows if str(row.get("visibility")) == "public"]
    if public:
        return public[0]
    tileset = seeded_private_tileset(client)
    client.post(f"/tilesets/{tileset['id']}/publish")
    return tileset


def wait_for_upload(client: httpx.Client, upload_id, states) -> str:
    deadline = time.monotonic() + POLL_DEADLINE
    state = ""
    while time.monotonic() < deadline:
        response = client.get(f"/uploads/{upload_id}")
        if response.status_code == 200:
            state = str(response.json().get("state"))
            if state in states:
                return state
        settle()
    return state


def wait_for_rows(client: httpx.Client, route: str, at_least: int) -> list:
    deadline = time.monotonic() + POLL_DEADLINE
    rows = []
    while time.monotonic() < deadline:
        response = client.get(route)
        if response.status_code == 200:
            rows = _shapes.items(response.json())
            if len(rows) >= at_least:
                return rows
        settle()
    return rows


def wait_for_operations(client: httpx.Client, project_id, after, at_least: int) -> list:
    deadline = time.monotonic() + POLL_DEADLINE
    rows = []
    while time.monotonic() < deadline:
        response = client.get(f"/projects/{project_id}/operations", params={"after": after})
        if response.status_code == 200:
            rows = _shapes.items(response.json())
            if len(rows) >= at_least:
                return rows
        settle()
    return rows
