"""Fixtures, pinned literals and helpers for the Chartic portal task.

Black-box only: HTTP against the running app, the rendered page through
Playwright, PostgreSQL through the shared backend adapter and MinIO through the
shared object-store adapter. Nothing here reads the agent's source.
"""

from __future__ import annotations

import concurrent.futures
import os
import re
import threading
import time
import uuid

import httpx
import pytest

import capabilities

TIMEOUT = 30.0
SETTLE_SECONDS = 0.5
OK = (200, 201)

PASSWORD = "deku-demo-pw-2026"
CONTRIBUTOR_EMAIL = "contributor@example.com"
CONTRIBUTOR2_EMAIL = "contributor2@example.com"
READER_EMAIL = "reader@example.com"
CONTRIBUTOR_NAME = "Noor Haddad"
CONTRIBUTOR2_NAME = "Teo Vargas"
READER_NAME = "Lior Sand"

CURRENT = "5.4.3"
PRIOR = "5.3.0"
OLDEST = "5.2.1"
ABSENT_VERSION = "9.9.9"
RELEASE_DATES = {"5.4.3": "2026-02-18", "5.3.0": "2025-11-05", "5.2.1": "2025-07-22"}
ARTIFACT_SHA256 = {
    "5.4.3": "7d8968eb8880d7605fda3b6af5eaac8bac52c01423eb7d1f862ab732e9e82787",
    "5.3.0": "68ae5dcb7020eeebfe4f65558278857872e42d7da87979b884c4b5e5beb65c88",
    "5.2.1": "a47ad78a060a73e0347e48d4f425f31169ab858bd302bb4c71d05b9b95d74efe",
}
ARTIFACT_SHA512 = (
    "264915ce0335931833e3d3230344e2b1534f09ae6c179c7ffab856e44eff0e5e"
    "16c4299fe9c5be69c89a77664b8065c26374fefdada2c82aeb2ce04d136913ee")
MIRROR_ALPHA = "mirror-alpha.chartic-portal.example"
MIRROR_BETA = "mirror-beta.chartic-portal.example"
MIRROR_GAMMA = "mirror-gamma.chartic-portal.example"
BETA_SHA256 = "aec03af8d255a240eaff00776dd6a087c7a87a63faf0449357a3f179406c574b"

REMOVED_PATH = "series.hoverAnimation"
REPLACEMENT_PATH = "series.emphasis.disabled"
LATE_PATH = "legend.selectorLabel"
ROTATE_PATH = "xAxis.axisLabel.rotate"
SAVE_AS_IMAGE_PATH = "toolbox.feature.saveAsImage.title"
SHARED_OBJECT = "textStyle"
SHARED_LEAVES = ("color", "fontSize", "fontFamily", "fontWeight")
SHARED_PATHS = ("title.textStyle", "legend.textStyle", "tooltip.textStyle")
COMPUTED_PATH = "series.barWidth"
COMPUTED_WORKED = "31"
INHERITED_PATH = "series.label.position"
INHERITS_FROM = "label.position"
VARIANT_PATH = "series.data"
INIT_PATH = "chartic.init"
INIT_SIGNATURE = ("init(dom: HTMLElement | null, theme?: string | object, "
                  "opts?: object) => ChartInstance")
SET_OPTION_PATH = "charticInstance.setOption"

LINE_EXAMPLE = "basic-line-smooth"
BAR_EXAMPLE = "stacked-bar-margin"
MAP_EXAMPLE = "world-population-map"
CANDLE_EXAMPLE = "candle-volume-overlay"
SUNBURST_EXAMPLE = "sunburst-nested-budget"
RADAR_EXAMPLE = "radar-skills-compare"
PROPOSED_EXAMPLE = "bump-chart-lines"
PUBLISHED_EXAMPLES = (LINE_EXAMPLE, BAR_EXAMPLE, MAP_EXAMPLE, CANDLE_EXAMPLE,
                      SUNBURST_EXAMPLE, RADAR_EXAMPLE)
LINE_DESCRIPTION = "Line chart with 1 series. The category axis runs Mon to Sun. Values run from 120 to 260, highest on Sat, lowest on Mon."
LINE_POINTS = 7
LINE_THUMBNAIL_KEY = (
    "thumbnails/basic-line-smooth/"
    "f7b809e012ada4d2b9afdd8464ace025532124a3c9253071e5afb429da7e6780.svg")
PROPOSED_THUMBNAIL_KEY = (
    "thumbnails/bump-chart-lines/"
    "a319ed61bc2c850dc1f06b05a0f22ca22876df0af2aeb72ca80283276a58a176.svg")

LIVE_SNIPPET = "qkzm4p2vx7hd3nzr6tsw5bjy4c"
WITHDRAWN_SNIPPET = "d4pv2sx6mhk3zrqt7nwy5bgj2f"
SNIPPET_ID_RE = re.compile(r"^[a-z2-7]{26}$")

THEMES = ("default", "dark-slate", "vintage", "sandstone")
FAILING_THEME = "sandstone"
SERIES_COLOURS = 8

CORE_MODULE = "chartic/core"
BAR_MODULE = "chart/bar"
BAR_CLOSURE = ("chartic/core", "chart/bar", "coord/cartesian", "component/axis",
               "scale/interval", "util/format")
BAR_CLOSURE_RAW = 242400
MODULE_RAW = {
    "chartic/core": 118500, "chart/bar": 41200, "chart/line": 38600,
    "chart/pie": 22400, "coord/cartesian": 33800, "component/axis": 27600,
    "scale/interval": 11900, "util/format": 9400, "component/legend": 15300,
    "component/tooltip": 24700,
}
UNKNOWN_MODULE = "chart/sankey3d"

WALL_CLOCK_BUDGET = 5
MEMORY_BUDGET_MB = 256
DECOY_FIELD = "website_url"
REPEAT_LIMIT = 10
REPEAT_WINDOW = 60
RETENTION_DAYS = 90
BUNDLE_RETENTION_DAYS = 30
EVENT_RETENTION_HOURS = 24

PUBLIC_ROUTES = ("/", "/login", "/signup", "/option", "/api-reference", "/gallery",
                 "/editor", "/theme", "/themes", "/releases", "/bundle", "/privacy")
SIDEBAR_GROUPS = ("Reference", "Tools", "Project")
SECURITY_HEADERS = ("strict-transport-security", "x-content-type-options",
                    "x-frame-options", "referrer-policy", "content-security-policy")
SECRET_ENV = ("DATABASE_URL", "STORAGE_ACCESS_KEY", "STORAGE_SECRET_KEY")

SMOOTH_OPTION = ('{"xAxis":{"type":"category","data":["Mon","Tue","Wed","Thu","Fri",'
                 '"Sat","Sun"]},"yAxis":{"type":"value"},'
                 '"series":[{"type":"line","smooth":true,'
                 '"data":[120,200,150,260,190,260,130]}]}')
BROKEN_OPTION = '{"series":[{"type":"line","data":[1,2,3]}'
ENDLESS_OPTION = 'while (true) { }'
FUNCTION_THEME = '{"color":["#5070dd"],"textStyle":{"fontSize":"() => 12"}}'
NON_COLOUR_THEME = '{"color":["not-a-colour"]}'


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned pause, for a side effect the app applies asynchronously."""
    time.sleep(seconds)


def base_url() -> str:
    return os.environ["APP_PUBLIC_URL"].rstrip("/")


def api_base() -> str:
    return f"{base_url()}/api"


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code}: {response.text[:400]}")


def token_hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n]


def probe_title() -> str:
    return f"Probe Chart {token_hex(6)}"


def client_for(token: str | None) -> httpx.Client:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, headers=headers)


def login(email: str, password: str = PASSWORD) -> httpx.Response:
    return httpx.post(f"{api_base()}/auth/login",
                      json={"email": email, "password": password}, timeout=TIMEOUT)


def token_for(email: str, password: str = PASSWORD) -> str:
    response = login(email, password)
    assert response.status_code in OK, f"login for {email} failed: {describe(response)}"
    token = response.json().get("token")
    assert token, f"login for {email} returned no `token`: {describe(response)}"
    return token


def body(response: httpx.Response):
    if "json" not in response.headers.get("content-type", ""):
        return {}
    return response.json()


def message(response: httpx.Response) -> str:
    data = body(response)
    if isinstance(data, dict):
        for key in ("message", "detail", "error"):
            if data.get(key):
                return str(data[key])
    return response.text[:400]


def refused(response: httpx.Response, what: str) -> None:
    assert 400 <= response.status_code < 500, \
        f"{what} must be refused as a client error: {describe(response)}"


def denied(response: httpx.Response, what: str) -> None:
    assert response.status_code in (401, 403, 404), \
        f"{what} must be denied or answered as absent: {describe(response)}"


def ok(response: httpx.Response, what: str):
    assert response.status_code in OK, f"{what} failed: {describe(response)}"
    return response.json()


def rows(response: httpx.Response, what: str) -> list:
    data = ok(response, what)
    assert isinstance(data, list), f"{what} must return a top-level array: {data!r}"
    return data


def wait_until(read, done, timeout: float = 25.0):
    """Poll `read` toward a deadline for a side effect applied asynchronously."""
    deadline = time.monotonic() + timeout
    value = read()
    while not done(value) and time.monotonic() < deadline:
        settle()
        value = read()
    return value


def run_together(*calls):
    """Start every call at the same instant and return their results in order."""
    gate = threading.Barrier(len(calls))

    def wrap(fn):
        gate.wait()
        return fn()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(calls)) as pool:
        futures = [pool.submit(wrap, fn) for fn in calls]
        return [f.result() for f in futures]


def html_of(path: str) -> httpx.Response:
    return httpx.get(f"{base_url()}{path}", timeout=TIMEOUT, follow_redirects=True)


def raw_get(path: str) -> httpx.Response:
    return httpx.get(f"{base_url()}{path}", timeout=TIMEOUT)


def node(client: httpx.Client, version: str, path: str) -> httpx.Response:
    return client.get(f"/schema/{version}/node", params={"path": path})


def node_of(client: httpx.Client, version: str, path: str) -> dict:
    return ok(node(client, version, path), f"schema node {path} at {version}")


def tree_of(client: httpx.Client, version: str) -> list:
    return rows(client.get(f"/schema/{version}/tree"), f"schema tree at {version}")


def search_paths(client: httpx.Client, version: str, query: str) -> list:
    found = rows(client.get(f"/schema/{version}/search", params={"q": query}),
                 f"schema search {query!r} at {version}")
    return found


def interface_node(client: httpx.Client, version: str, path: str) -> dict:
    return ok(client.get(f"/interface/{version}/node", params={"path": path}),
              f"interface node {path}")


def examples_of(client: httpx.Client, **filters) -> list:
    return rows(client.get("/examples", params=filters), "example listing")


def example_ids(client: httpx.Client, **filters) -> list:
    return [row.get("id") for row in examples_of(client, **filters)]


def thumbnail(client: httpx.Client, example_id: str) -> httpx.Response:
    return client.get(f"/examples/{example_id}/thumbnail")


def propose(client: httpx.Client, category: str = "Line", **extra) -> dict:
    payload = {"title": probe_title(), "category": category,
               "tags": ["animation"], "code_js": SMOOTH_OPTION, DECOY_FIELD: ""}
    payload.update(extra)
    created = ok(client.post("/my/examples", json=payload), "proposing an example")
    assert created.get("id"), f"a proposed example must return its id: {created}"
    return created


def validate_example(client: httpx.Client, example_id: str) -> dict:
    return ok(client.post(f"/my/examples/{example_id}/validate", json={}),
              f"validating {example_id}")


def publish(client: httpx.Client, example_id: str) -> httpx.Response:
    return client.post(f"/my/examples/{example_id}/publish", json={})


def withdraw(client: httpx.Client, example_id: str) -> httpx.Response:
    return client.delete(f"/my/examples/{example_id}")


def share(client: httpx.Client, code: str = SMOOTH_OPTION, **extra) -> dict:
    payload = {"code": code, "language": "js", "library_version": CURRENT,
               "renderer": "canvas", "theme": "default", "decal": False,
               DECOY_FIELD: ""}
    payload.update(extra)
    return ok(client.post("/snippets", json=payload), "sharing a snippet")


def render(client: httpx.Client, option: str, renderer: str = "canvas") -> httpx.Response:
    return client.post("/render", json={"option": option, "renderer": renderer})


def preferences(client: httpx.Client) -> dict:
    return ok(client.get("/preferences"), "reading the preference set")


def set_preferences(client: httpx.Client, **values) -> dict:
    current = {"dark": False, "decal": False, "renderer": "canvas"}
    current.update(values)
    return ok(client.put("/preferences", json=current), "writing the preference set")


def modules_of(client: httpx.Client, version: str = CURRENT) -> dict:
    listed = rows(client.get(f"/modules/{version}"), f"module graph at {version}")
    return {row["module_id"]: row for row in listed}


def request_bundle(client: httpx.Client, selection=(BAR_MODULE,), **extra) -> httpx.Response:
    payload = {"release_version": CURRENT, "selection": list(selection),
               "renderers": ["canvas"], "locale": "en", "formats": ["esm"],
               "minify": True, "sourcemap": False}
    payload.update(extra)
    return client.post("/bundles", json=payload)


def bundle_ready(client: httpx.Client, digest: str) -> dict:
    def read():
        return ok(client.get(f"/bundles/{digest}"), f"bundle {digest}")
    final = wait_until(read, lambda b: b.get("status") in ("ready", "failed"))
    assert final.get("status") == "ready", f"the bundle must become ready: {final}"
    return final


def releases_of(client: httpx.Client) -> dict:
    listed = rows(client.get("/releases"), "release listing")
    return {row["version"]: row for row in listed}


def themes_of(client: httpx.Client) -> dict:
    listed = rows(client.get("/themes"), "theme listing")
    return {row["id"]: row for row in listed}


def store_keys(prefix: str) -> list:
    return capabilities.make_store().list(prefix)


def head_tag(html: str, pattern: str) -> str | None:
    found = re.search(pattern, html, re.I | re.S)
    return found.group(1) if found else None


def meta_content(html: str, name: str) -> str | None:
    for attr in ("name", "property"):
        found = re.search(
            rf'<meta[^>]+{attr}=["\']{re.escape(name)}["\'][^>]*content=["\']([^"\']*)["\']',
            html, re.I)
        if found:
            return found.group(1)
        found = re.search(
            rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]*{attr}=["\']{re.escape(name)}["\']',
            html, re.I)
        if found:
            return found.group(1)
    return None


def sign_in_page(page, email: str, password: str = PASSWORD) -> None:
    page.goto(f"{base_url()}/login")
    page.wait_for_load_state("networkidle")
    page.get_by_label("Email", exact=True).fill(email)
    page.get_by_label("Password", exact=True).fill(password)
    page.get_by_role("button", name=re.compile("sign in|log in|login", re.I)).click()
    page.wait_for_url(lambda url: "/login" not in url, timeout=20000)


def contrast_ratio(front: tuple, back: tuple) -> float:
    def channel(value):
        value = value / 255.0
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    def luminance(colour):
        r, g, b = (channel(c) for c in colour[:3])
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    first, second = luminance(front), luminance(back)
    lighter, darker = max(first, second), min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def parse_colour(value: str) -> tuple:
    numbers = [float(n) for n in re.findall(r"[\d.]+", value or "")]
    if len(numbers) >= 3:
        return tuple(int(round(n)) for n in numbers[:3])
    return (0, 0, 0)


@pytest.fixture(scope="session")
def app_url() -> str:
    return base_url()


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture(scope="session", autouse=True)
def seeded_state_restored():
    """Withdraw every example the browser pass proposed, so pytest starts from seed.

    The browser journeys propose and publish their own examples rather than the
    seeded ones, and this clears whatever they left behind: the seeded corpus is
    six published examples and one proposed, and several assertions below count it.
    """
    for email in (CONTRIBUTOR_EMAIL, CONTRIBUTOR2_EMAIL):
        signed = login(email)
        if signed.status_code not in OK:
            continue
        token = body(signed).get("token") if isinstance(body(signed), dict) else None
        if not token:
            continue
        with client_for(token) as session:
            listed = session.get("/my/examples")
            if listed.status_code not in OK or not isinstance(body(listed), list):
                continue
            for row in body(listed):
                title = str(row.get("title", ""))
                if title.startswith("Probe Chart") or title.startswith("Walkthrough Chart"):
                    session.delete(f"/my/examples/{row.get('id')}")
    yield


@pytest.fixture()
def contributor():
    with client_for(token_for(CONTRIBUTOR_EMAIL)) as session:
        yield session


@pytest.fixture()
def contributor2():
    with client_for(token_for(CONTRIBUTOR2_EMAIL)) as session:
        yield session


@pytest.fixture()
def reader():
    with client_for(token_for(READER_EMAIL)) as session:
        yield session


@pytest.fixture()
def anon():
    with client_for(None) as session:
        yield session


@pytest.fixture()
def withdraw_after(contributor):
    """Examples a test proposed, withdrawn afterwards so the seeded corpus returns."""
    created: list = []
    yield created
    for example_id in reversed(created):
        contributor.delete(f"/my/examples/{example_id}")


@pytest.fixture()
def proposed_probe(contributor, withdraw_after):
    """One freshly proposed example owned by the first contributor."""
    created = propose(contributor)
    withdraw_after.append(created["id"])
    return created


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        chromium = pw.chromium.launch()
        yield chromium
        chromium.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    tab = context.new_page()
    yield tab
    context.close()


@pytest.fixture()
def narrow_page(browser):
    context = browser.new_context(viewport={"width": 390, "height": 844})
    tab = context.new_page()
    yield tab
    context.close()
