"""Fixtures, pinned literals and helpers for the Tempo catalogue task.

Black-box only: HTTP against the running app, the rendered page through
Playwright, PostgreSQL through the shared backend adapter, Kill Bill through the
shared payments adapter and Mailpit through the shared inbox adapter. Nothing
here reads the agent's source.
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
MEMBER_EMAIL = "member@example.com"
MEMBER2_EMAIL = "member2@example.com"
MEMBER3_EMAIL = "member3@example.com"
MEMBER_NAME = "Nova Reyes"
MEMBER2_NAME = "Kit Alvarez"
MEMBER3_NAME = "Sol Danner"
MEMBER_HANDLE = "nova"
MEMBER2_HANDLE = "kit"
MEMBER3_HANDLE = "sol"
JOINED = {MEMBER_EMAIL: "2026-03-11", MEMBER2_EMAIL: "2026-06-02",
          MEMBER3_EMAIL: "2026-09-10"}

CURRENT = "13.1.0"
PRIOR = "13.0.4"
OLDEST = "12.8.2"
ABSENT_VERSION = "9.9.9"
RELEASES = (CURRENT, PRIOR, OLDEST)
RELEASE_DATES = {CURRENT: "2026-09-02", PRIOR: "2026-07-19", OLDEST: "2026-04-08"}
UI_VERSION = "0.0.2"

RUNTIMES = ("react", "js", "vue")
ABSENT_RUNTIME = "svelte"

CATEGORIES = (
    ("hero-sections", "Hero sections",
     "First impressions with editorial reveals and product-led motion."),
    ("pricing", "Pricing",
     "Comparison, billing and usage surfaces that explain value clearly."),
    ("navigation", "Navigation",
     "Mega menus, scroll-aware shrinking headers and command palettes."),
    ("testimonials", "Testimonials",
     "Logo tickers, coverflow carousels and draggable testimonial card stacks."),
    ("page-transitions", "Page transitions",
     "Full-page entrances and exits with a clear sense of direction."),
    ("bento-grids", "Bento grids",
     "Staggered bento reveals, app-card expands and scroll-linked spotlights."),
    ("stats-sections", "Stats sections",
     "Scroll-in counters and live engagement panels with animated trends and drawn graphs."),
    ("cta-sections", "CTA sections",
     "Signup celebrations, copy-to-clipboard install blocks and magnetic banners."),
    ("footers", "Footers",
     "Newsletter forms with live feedback, sticky under-page reveals and staggered mega-footer wordmarks."),
)
CATEGORY_PATHS = tuple(path for path, _, _ in CATEGORIES)
ABSENT_CATEGORY = "dialogs"

SECTIONS = {
    "editorial-stagger-hero": ("Editorial stagger hero", "hero-sections",
                               ("transitions.gentle", "stagger.relaxed", "travel.enter")),
    "border-beam": ("Border beam", "cta-sections", ("transitions.ambient",)),
    "confetti": ("Confetti", "cta-sections", ("transitions.lively", "travel.enter")),
    "command-palette": ("Command palette", "navigation",
                        ("transitions.snap", "stagger.tight")),
    "coverflow": ("Coverflow", "testimonials", ("transitions.ui", "travel.hover")),
    "sheet": ("Sheet", "page-transitions", ("transitions.ui", "travel.section")),
}

THEME_TRANSITIONS = {
    "transitions.snap": (1218, 70),
    "transitions.ui": (305, 33),
    "transitions.gentle": (110, 20),
    "transitions.lively": (622, 17),
    "transitions.ambient": (43, 13),
}
THEME_STAGGER = {"stagger.tight": "0.04", "stagger.base": "0.08",
                 "stagger.relaxed": "0.15"}
THEME_TRAVEL = {"travel.hover": "4", "travel.enter": "24", "travel.section": "48"}
THEME_PREFERENCE = {"reducedMotion": "calm"}
THEME_KEYS = (tuple(THEME_TRANSITIONS) + tuple(THEME_STAGGER)
              + tuple(THEME_TRAVEL) + tuple(THEME_PREFERENCE))

EXAMPLES = {
    "scroll-velocity": ("Scroll velocity", "stats-sections", "free",
                        ("react", "js", "vue"), "2026-09-01"),
    "parallax": ("Parallax", "hero-sections", "free",
                 ("react", "js", "vue"), "2026-08-22"),
    "skeleton-shimmer": ("Skeleton Shimmer", "bento-grids", "free",
                         ("react", "vue"), "2026-08-14"),
    "floating-action": ("Floating Action", "cta-sections", "free",
                        ("js",), "2026-07-30"),
    "ios-app-folder": ("iOS App Folder", "page-transitions", "paid",
                       ("react",), "2026-08-27"),
    "ios-pointer": ("iOS Pointer", "navigation", "paid",
                    ("react", "js"), "2026-08-05"),
    "ticker-marquee": ("Ticker", "testimonials", "paid",
                       ("react", "js", "vue"), "2026-06-11"),
}
FREE_EXAMPLES = tuple(s for s, row in EXAMPLES.items() if row[2] == "free")
PAID_EXAMPLES = tuple(s for s, row in EXAMPLES.items() if row[2] == "paid")
PAID_EXAMPLE = "ios-app-folder"
FREE_EXAMPLE = "parallax"
SAVED_AT_SEED = ("scroll-velocity", "parallax")
ABSENT_EXAMPLE = "no-such-example"

DOC_PAGES = {
    ("shared", "installation"): ("Installation", OLDEST, "free"),
    ("react", "use-spring"): ("useSpring", OLDEST, "free"),
    ("react", "animate-presence"): ("AnimatePresence", PRIOR, "free"),
    ("react", "layout-animation"): ("Layout animation", CURRENT, "paid"),
    ("js", "animate"): ("animate", OLDEST, "free"),
    ("js", "scroll"): ("scroll", PRIOR, "free"),
    ("vue", "motion-component"): ("Motion component", OLDEST, "free"),
}
DOC_RUNTIME = "react"
DOC_SLUG = "use-spring"
PAID_DOC_SLUG = "layout-animation"

CHANGELOG = {
    "spring-presets": (CURRENT, "feature", "Five named spring presets", "2026-09-02"),
    "exit-animation-fix": (PRIOR, "fix",
                           "Exit animations no longer skip their last frame", "2026-07-19"),
    "pointer-gesture-fix": (OLDEST, "fix",
                            "Pointer gestures respect a cancelled press", "2026-04-08"),
    "ui-registry-install": (UI_VERSION, "release",
                            "Sections install from the registry", "2026-08-30"),
}
ARTICLES = {
    "springs-over-easing": ("Springs over easing curves", "alex", "2026-08-28"),
    "the-all-problem": ("The cost of animating everything", "alex", "2026-07-15"),
    "reduced-motion-is-not-no-motion": ("Reduced motion is not no motion", "alex",
                                        "2026-06-04"),
}
ABSENT_ARTICLE = "no-such-article"

CURRENCY = "USD"
COUNTRY = "US"
LIST_MINOR = 24900
BAND_MINOR = 14900
LIST_BAND = "list"
DISCOUNT_BAND = "ppp-south-asia"
DISCOUNT_REASON = "Local discount applied"
REGION_HEADER = "X-Client-Region"
LIST_REGION = "US"
DISCOUNT_REGION = "IN"
UNKNOWN_REGION = "AQ"
LICENCE_PREFIX = "tempo-plus-"
SEEDED_LICENCE = LICENCE_PREFIX + MEMBER_HANDLE
RECEIPT_SUBJECT_PREFIX = "Tempo+ receipt "
BOOTSTRAP_BILLING_KEYS = ("orbit-amelia", "orbit-acme", "orbit-northwind")

PUBLISHED_PROJECT = "Orbit Atlas"
SUBMITTED_PROJECT = "Field Notes"
PROJECT_URL = "https://orbit-atlas.example.com"

SESSION_HOURS = 24
IDEMPOTENCY_HOURS = 24
PREVIEW_BUDGET_SECONDS = 5
PREVIEW_CONCURRENCY = 3
WIDTH_THRESHOLDS = (600, 760, 900, 1200)
FONT_FILE_CAP = 4

PUBLIC_ROUTES = ("/", "/docs", "/examples", "/ui", "/plus", "/login", "/signup",
                 "/changelog", "/magazine", "/about", "/privacy", "/terms")
SLASH_PAIRS = (("/docs", "/docs/"), ("/ui", "/ui/"))
NOT_FOUND_ROUTES = ("/div", "/svg")
NOT_FOUND_LABEL = "PAGE_NOT_FOUND"
SECURITY_HEADERS = ("strict-transport-security", "x-content-type-options",
                    "x-frame-options", "referrer-policy", "content-security-policy")
LICENCE_TABLES = ("licences", "licence", "licenses", "license")


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned pause, for a side effect the app applies asynchronously."""
    time.sleep(seconds)


def base_url() -> str:
    return os.environ["APP_PUBLIC_URL"].rstrip("/")


def api_base() -> str:
    return f"{base_url()}/api/v1"


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code}: {response.text[:400]}")


def token_hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n]


def probe_handle() -> str:
    return f"probe{token_hex(6)}"


def client_for(token: str | None, region: str | None = None) -> httpx.Client:
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if region:
        headers[REGION_HEADER] = region
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


def signup(handle: str | None = None, **extra) -> dict:
    handle = handle or probe_handle()
    payload = {"email": f"{handle}@example.com", "name": f"Probe {handle}",
               "handle": handle, "password": PASSWORD}
    payload.update(extra)
    response = httpx.post(f"{api_base()}/auth/signup", json=payload, timeout=TIMEOUT)
    assert response.status_code in OK, f"signup for {handle} failed: {describe(response)}"
    created = response.json()
    assert created.get("token"), f"signup must return a `token`: {created}"
    created["email"] = payload["email"]
    created["handle"] = handle
    created["display_name"] = payload["name"]
    return created


def who(payload) -> dict:
    """The member a response describes, whether nested under `member` or not."""
    if isinstance(payload, dict) and isinstance(payload.get("member"), dict):
        return payload["member"]
    return payload if isinstance(payload, dict) else {}


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


def raw_get(path: str, **kwargs) -> httpx.Response:
    return httpx.get(f"{base_url()}{path}", timeout=TIMEOUT, **kwargs)


def gallery(client: httpx.Client, **facets) -> dict:
    return ok(client.get("/examples", params=facets), f"gallery listing {facets}")


def gallery_slugs(client: httpx.Client, **facets) -> list:
    return [row.get("slug") for row in gallery(client, **facets).get("items", [])]


def gallery_items(client: httpx.Client, **facets) -> dict:
    return {row.get("slug"): row for row in gallery(client, **facets).get("items", [])}


def example_of(client: httpx.Client, slug: str) -> httpx.Response:
    return client.get(f"/examples/{slug}")


def example_files(client: httpx.Client, slug: str) -> list:
    return ok(example_of(client, slug), f"example {slug}").get("files") or []


def raw_file(client: httpx.Client, slug: str, path: str) -> httpx.Response:
    return client.get(f"/examples/{slug}/files/{path}")


def docs_page(client: httpx.Client, runtime: str, slug: str,
              version: str | None = None) -> httpx.Response:
    if version:
        return client.get(f"/docs/{version}/{runtime}/{slug}")
    return client.get(f"/docs/{runtime}/{slug}")


def categories_of(client: httpx.Client) -> dict:
    return {row.get("path"): row for row in rows(client.get("/categories"),
                                                 "category listing")}


def sections_of(client: httpx.Client, **params) -> dict:
    return {row.get("slug"): row for row in rows(client.get("/sections", params=params),
                                                 "section listing")}


def theme_of(client: httpx.Client) -> dict:
    return {row.get("key"): row for row in rows(client.get("/theme"),
                                                "theme value listing")}


def pricing(client: httpx.Client) -> dict:
    return ok(client.get("/pricing"), "pricing")


def purchase(client: httpx.Client, display_name: str, email: str,
             key: str | None = None) -> httpx.Response:
    return client.post("/purchases", json={
        "display_name": display_name, "email": email,
        "idempotency_key": key or token_hex(16)})


def buy(client: httpx.Client, display_name: str, email: str) -> dict:
    return ok(purchase(client, display_name, email), f"purchase for {email}")


def saved_of(client: httpx.Client) -> list:
    return [row.get("slug") or row.get("example_slug")
            for row in rows(client.get("/saved"), "saved listing")]


def save(client: httpx.Client, slug: str) -> httpx.Response:
    return client.post("/saved", json={"example_slug": slug})


def unsave(client: httpx.Client, slug: str) -> httpx.Response:
    return client.delete(f"/saved/{slug}")


def profile_of(client: httpx.Client, handle: str) -> httpx.Response:
    return client.get(f"/members/{handle}")


def projects_of(client: httpx.Client, handle: str) -> list:
    return ok(profile_of(client, handle), f"profile {handle}").get("projects") or []


def submit_project(client: httpx.Client, title: str | None = None, **extra) -> dict:
    payload = {"title": title or f"Probe Project {token_hex(6)}",
               "source_url": "https://probe.example.com",
               "description": "A probe project submitted by the outcome pass."}
    payload.update(extra)
    return ok(client.post("/showcase", json=payload), "submitting a project")


def changelog_of(client: httpx.Client) -> list:
    return ok(client.get("/changelog"), "changelog").get("items") or []


def magazine_of(client: httpx.Client) -> list:
    return ok(client.get("/magazine"), "magazine").get("items") or []


def article_of(client: httpx.Client, slug: str) -> httpx.Response:
    return client.get(f"/magazine/{slug}")


def billing_keys() -> set:
    payments = capabilities.make_payments()
    return {str(row.get("externalKey") or "") for row in payments.accounts()}


def billing_account(key: str) -> dict | None:
    payments = capabilities.make_payments()
    for row in payments.accounts():
        if str(row.get("externalKey") or "") == key:
            return row
    return None


def licence_table(backend) -> str | None:
    present = {row["table_name"] for row in backend.query(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")}
    for name in LICENCE_TABLES:
        if name in present:
            return name
    return None


def revoke_licence(backend, key: str) -> str:
    table = licence_table(backend)
    assert table, ("the brief pins a `licences` table carrying `external_key` and "
                   f"`revoked_at`; none of {LICENCE_TABLES} is queryable")
    backend.query(f"UPDATE {table} SET revoked_at = now() WHERE external_key = %s",
                  (key,))
    return table


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
def payments():
    return capabilities.make_payments()


@pytest.fixture(scope="session")
def inbox():
    return capabilities.make_inbox()


@pytest.fixture(scope="session", autouse=True)
def seeded_state_restored():
    """Undo what the browser pass left behind, so pytest starts from seed.

    The walkthroughs save examples as two of the seeded members and submit one
    showcase project, and several assertions below count the seeded rows. A
    licence and its order are deliberately NOT undone: the brief says an order is
    never deleted and a licence is never mutated, so the outcome pass buys as a
    freshly signed-up member instead of as a seeded one.
    """
    for email, keep in ((MEMBER_EMAIL, set(SAVED_AT_SEED)),
                        (MEMBER2_EMAIL, set()), (MEMBER3_EMAIL, set())):
        signed = login(email)
        if signed.status_code not in OK:
            continue
        data = body(signed)
        token = data.get("token") if isinstance(data, dict) else None
        if not token:
            continue
        with client_for(token) as session:
            listed = session.get("/saved")
            if listed.status_code in OK and isinstance(body(listed), list):
                for row in body(listed):
                    slug = row.get("slug") or row.get("example_slug")
                    if slug and slug not in keep:
                        session.delete(f"/saved/{slug}")
            handle = {MEMBER_EMAIL: MEMBER_HANDLE, MEMBER2_EMAIL: MEMBER2_HANDLE,
                      MEMBER3_EMAIL: MEMBER3_HANDLE}[email]
            mine = session.get(f"/members/{handle}")
            if mine.status_code in OK:
                for row in (body(mine) or {}).get("projects") or []:
                    title = str(row.get("title", ""))
                    if title.startswith("Probe Project") or title == "Field Study":
                        session.delete(f"/showcase/{row.get('id')}")
    yield


@pytest.fixture()
def member():
    with client_for(token_for(MEMBER_EMAIL)) as session:
        yield session


@pytest.fixture()
def member2():
    with client_for(token_for(MEMBER2_EMAIL)) as session:
        yield session


@pytest.fixture()
def member3():
    with client_for(token_for(MEMBER3_EMAIL)) as session:
        yield session


@pytest.fixture()
def anon():
    with client_for(None) as session:
        yield session


@pytest.fixture()
def anon_discounted():
    with client_for(None, region=DISCOUNT_REGION) as session:
        yield session


@pytest.fixture()
def anon_list_region():
    with client_for(None, region=LIST_REGION) as session:
        yield session


@pytest.fixture()
def fresh_member():
    """A freshly signed-up member, so a purchase writes a billing key of its own."""
    created = signup()
    with client_for(created["token"]) as session:
        session.probe = created
        yield session


@pytest.fixture()
def unsave_after(member):
    """Examples a test saved, unsaved afterwards so the seeded rows return."""
    saved: list = []
    yield saved
    for slug in reversed(saved):
        member.delete(f"/saved/{slug}")


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
