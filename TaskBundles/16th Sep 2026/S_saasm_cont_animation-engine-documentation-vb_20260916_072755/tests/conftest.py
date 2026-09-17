"""Fixtures, pinned literals and domain stores for Lumen.js.

Every literal below is pinned in instruction.md. Nothing here defines a test.
"""

from __future__ import annotations

import os
import time
import uuid
from typing import Any

import httpx
import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"

MAINTAINER_EMAIL = "maintainer@example.com"
MAINTAINER_NAME = "Elias Marchand"

BRAND = "Lumen.js"
PACKAGE = "lumenjs"
CONTACT = "hello[at]lumenjs.example"

VERSION_PUBLISHED = "4.5.0"
VERSION_ARCHIVED = "4.4.0"
VERSION_DRAFT = "4.6.0"
VERSION_STATES = ("draft", "published", "archived")
PREVIEW_KEY = "pv_9f2c41be"
SORT_KEY_PUBLISHED = "0004.0005.0000"
SORT_KEY_ARCHIVED = "0004.0004.0000"
SORT_KEY_DRAFT = "0004.0006.0000"

RAMPS = (
    "ground", "foreground", "hole", "plain",
    "citrus", "corail", "cyan", "green", "indigo", "king", "lavender", "lime",
    "magenta", "orange", "pink", "purple", "red", "sega", "sky", "turquoise",
    "yellow",
)
RAMP_COUNT = 21
RAMP_STEPS = 8

MODULES = (
    ("getting-started", "Getting started", "red", None, "renderer"),
    ("timer", "Timer", "sky", 1, "timer"),
    ("animation", "Animation", "orange", 2, "animate"),
    ("timeline", "Timeline", "yellow", 3, "timeline"),
    ("animatable", "Animatable", "lavender", 4, "spring"),
    ("draggable", "Draggable", "green", 5, "draggable"),
    ("layout", "Layout", "lime", 6, "scroll"),
    ("scope", "Scope", "turquoise", 7, "scope"),
    ("events", "Events", "corail", 8, "shield"),
    ("svg", "SVG", "cyan", 9, "svg"),
    ("text", "Text", "magenta", 10, "stagger"),
    ("utilities", "Utilities", "king", 11, "engine"),
    ("easings", "Easings", "indigo", 12, "easing"),
    ("waapi", "WAAPI", "sega", None, "waapi"),
    ("engine", "Engine", "citrus", None, "engine"),
    ("adapters", "Adapters", "purple", None, "renderer"),
)
MODULE_COUNT = 16
TILE_COUNT = 12
OBJECT_NAMES = (
    "animate", "draggable", "easing", "engine", "renderer", "scope", "scroll",
    "shield", "spring", "stagger", "svg", "timeline", "timer", "waapi",
)
OBJECT_COUNT = 14

PAGES = {
    "getting-started": ("installation", "imports", "your-first-animation"),
    "timer": ("create-timer", "timer-methods", "timer-callbacks"),
    "animation": ("create-animation", "animation-properties", "animation-playback"),
    "timeline": ("create-timeline", "timeline-positions", "timeline-playback"),
    "animatable": ("create-animatable", "animatable-settings", "animatable-methods"),
    "draggable": ("create-draggable", "draggable-axes", "draggable-callbacks"),
    "layout": ("layout-measure", "layout-transitions", "layout-callbacks"),
    "scope": ("create-scope", "scope-methods", "scope-cleanup"),
    "events": ("event-types", "event-listeners", "event-cleanup"),
    "svg": ("morph-to", "motion-path", "draw-line"),
    "text": ("split-text", "split-options", "split-cleanup"),
    "utilities": ("random-and-round", "set-and-get", "remap-and-clamp"),
    "easings": ("linear-and-power", "spring-and-elastic", "custom-curves"),
    "waapi": ("waapi-animate", "waapi-convert", "waapi-limits"),
    "engine": ("engine-settings", "engine-timing", "engine-lifecycle"),
    "adapters": ("adapter-overview", "adapter-usage", "adapter-limits"),
}
PAGE_COUNT = 48
DEMO_COUNT = 47
PAGE_WITHOUT_DEMO = ("adapters", "adapter-limits")
FIRST_PAGE = ("getting-started", "installation")
LAST_MODULE_PAGE = ("getting-started", "your-first-animation")
FIRST_PAGE_OF_NEXT_MODULE = ("timer", "create-timer")
LAST_PAGE = ("adapters", "adapter-limits")
SCENE_DEMO_MODULE = "svg"
DEMO_KINDS = ("inline", "scene")

BADGE_MODULES = ("text", "adapters")
BADGE_LABEL = "NEW"
BADGE_EXPIRES = "2026-12-01"
MISSING_IN_ARCHIVED = "text"

CODE_ONLY_TERM = "remap"
CODE_ONLY_PAGE = ("utilities", "remap-and-clamp")
DRAFT_BROKEN_LINK = "getting-started/configuration"
QUERY_LENGTH_BOUND = 120

STOPS = (
    "intro", "toolbox", "intuitive", "composition", "scroll", "staggering",
    "svg-utilities", "draggable", "clockwork", "responsive", "modules",
    "sponsors",
)
STOP_COUNT = 12
RESIDENT_OBJECTS = 2
DEGRADATION_STATES = ("full", "reduced_motion", "scene_unavailable", "low_power")

FAMILIES = {
    "spring": ("default", "snappy", "bouncy", "strong"),
    "bezier": ("in", "out", "in-out", "out-in"),
    "power": ("in", "out", "in-out", "out-in"),
    "sine": ("in", "out", "in-out", "out-in"),
    "expo": ("in", "out", "in-out", "out-in"),
    "circ": ("in", "out", "in-out", "out-in"),
    "back": ("in", "out", "in-out", "out-in"),
    "elastic": ("in", "out", "in-out", "out-in"),
    "bounce": ("in", "out", "in-out", "out-in"),
    "linear": ("linear",),
}
FAMILY_RAMPS = {
    "spring": "red", "bezier": "orange", "power": "yellow", "sine": "lime",
    "expo": "green", "circ": "turquoise", "back": "cyan", "elastic": "indigo",
    "bounce": "lavender", "linear": "pink",
}
FAMILY_COUNT = 10
MEMBER_COUNT = 37
POINT_KEYS = ("family", "member", "p1x", "p1y", "p2x", "p2y")
SPRING_KEYS = ("family", "member", "bounce", "duration")
POINT_DECIMALS = 3
SPRING_DECIMALS = 2
EXPORT_TABS = ("CSS", "JS")

LIST_WAITLIST = "course_waitlist"
LIST_NEWSLETTER = "newsletter"
LISTS = (LIST_WAITLIST, LIST_NEWSLETTER)
SUBSCRIBER_STATES = ("pending", "confirmed", "unsubscribed", "bounced",
                     "complained")
STATE_PENDING = "pending"
STATE_CONFIRMED = "confirmed"
STATE_UNSUBSCRIBED = "unsubscribed"
STATE_BOUNCED = "bounced"
STATE_COMPLAINED = "complained"

CONFIRMED_EMAIL = "confirmed@example.com"
PENDING_EMAIL = "pending@example.com"
EXPIRED_EMAIL = "expired@example.com"
COMPLAINED_EMAIL = "complained@example.com"
UNSUBSCRIBED_EMAIL = "unsubscribed@example.com"
PENDING_TOKEN_EXPIRES = "2026-09-23"
EXPIRED_TOKEN_EXPIRED = "2026-09-09"

TOKEN_BITS = 128
TOKEN_DAYS = 7
HONEYPOT_FIELD = "company_website"
TIMING_TOKEN_SECONDS = 2
ADDRESS_LIMIT_PER_HOUR = 3
ORIGIN_LIMIT_PER_HOUR = 20
RESEND_LIMIT_PER_DAY = 2
GLOBAL_SEND_CEILING = 200

OUTBOX_KINDS = ("confirmation", "welcome", "unsubscribe")
OUTBOX_STATES = ("queued", "delivered", "dead")
MAIL_EVENT_TYPES = ("delivered", "bounced_hard", "bounced_soft", "complained",
                    "unsubscribed")

TIER_UPPER = "upper"
TIER_LOWER = "lower"
TIER_NAMES = {TIER_UPPER: "Upper", TIER_LOWER: "Lower"}
TIER_RANKS = {TIER_UPPER: 1, TIER_LOWER: 2}
SURFACE_DOC_LANDING = "documentation-landing"
SURFACE_DOC_PAGE = "documentation-page"
SURFACE_TOUR_TWELVE = "tour-stop-twelve"
SURFACE_TOUR_OPENING = "tour-opening"
TIER_PLACEMENTS = {
    TIER_UPPER: (SURFACE_DOC_LANDING, SURFACE_DOC_PAGE, SURFACE_TOUR_TWELVE,
                 SURFACE_TOUR_OPENING),
    TIER_LOWER: (SURFACE_DOC_LANDING, SURFACE_TOUR_TWELVE),
}
SPONSORS = {
    "spn_northlight": ("Northlight", TIER_UPPER, 1),
    "spn_tessera": ("Tessera", TIER_UPPER, 2),
    "spn_vantive": ("Vantive", TIER_LOWER, 1),
    "spn_plinth": ("Plinth", TIER_LOWER, 2),
    "spn_ravelin": ("Ravelin", TIER_LOWER, 3),
    "spn_corvid": ("Corvid", TIER_LOWER, 4),
}
SPONSOR_WITHOUT_MARK = "spn_ravelin"
SPONSOR_LAPSED = "spn_corvid"
SPONSOR_LAPSED_ENDED = "2026-08-31"
ROSTER_FRESHNESS_HOURS = 24

AD_STATES = ("fills", "empty", "slow")

JOBS = (
    "send_confirmation", "send_welcome", "process_mail_events",
    "sync_sponsor_roster", "sweep_expired_subscriptions", "expire_badges",
    "rebuild_index", "purge_caches", "warm_caches", "check_roster_freshness",
)
JOB_COUNT = 10
JOB_STATES = ("running", "succeeded", "failed", "refused")
MAX_ATTEMPTS = 5
SWEEP_SANITY_THRESHOLD = 500
WATCHED_SIGNALS = 12

ANALYTICS_KINDS = (
    "route_viewed", "tour_stop_reached", "specimen_copied", "search_performed",
    "search_result_activated", "editor_curve_changed", "editor_export_copied",
    "subscription_submitted", "funding_call_activated", "demo_failed",
    "scene_degraded",
)
STORAGE_CHOICES = ("yes", "no")

INDEX_KEY = "index/{version}/search-index.json"
MARK_KEY = "sponsors/{external_id}/mark.svg"
POSTER_KEY = "posters/{version}/{module}/{page}.svg"
ROSTER_KEY = "roster/current.json"

TOUR_ROUTE = "/"
DOCS_ROUTE = "/documentation"
EDITOR_ROUTE = "/easing-editor"
LEARN_ROUTE = "/learn"
PRIVACY_ROUTE = "/privacy"
CONFIRM_ROUTE = "/confirm"
UNSUBSCRIBE_ROUTE = "/unsubscribe"
SITEMAP_ROUTE = "/sitemap.xml"
LOGIN_ROUTE = "/login"
STUDIO_ROUTE = "/studio"
PREVIEW_ROUTE = "/preview/{preview_key}"
HEALTH_ROUTE = "/api/health"

PUBLIC_ROUTES = (
    TOUR_ROUTE, DOCS_ROUTE, EDITOR_ROUTE, LEARN_ROUTE, PRIVACY_ROUTE,
)
STUDIO_ROUTES = (
    "/api/studio/versions", "/api/studio/outbox", "/api/studio/jobs",
    "/api/studio/dead-letters", "/api/studio/page-views",
)

NAV_LABELS = ("DOCS", "EASINGS", "LEARN", "EXAMPLES", "SOURCE")
FUNDING_LABEL = "SPONSOR"
SKIP_LINK = "Skip to content"
FOOTER_HEADINGS = ("SPONSORS", "SITE", "SOCIALS", "STAY IN TOUCH")
FOOTER_ATTRIBUTION = "Built and maintained by Elias Marchand"
AD_ATTRIBUTION = "ads via Carbonate"
TOUR_HEADLINE = "One engine for every animation."
TOUR_SUBHEADING = "A small, fast library for moving anything on the web."
INSTALL_LINE = "npm i lumenjs"
SECONDARY_CALL = "LEARN MORE"
CLOSING_HEADLINE = "Start animating"
STOP_TWELVE_HEADLINE = "Our sponsors"
DOCS_TITLE = "Documentation"
TIER_HEADINGS = ("Upper sponsors", "Lower sponsors")
RECRUITMENT_LABEL = "Become a sponsor"
IN_SECTION_HEADING = "In this section"
PAGER_LABELS = ("PREVIOUS", "NEXT")
SEARCH_PLACEHOLDER = "SEARCH"
SEARCH_EMPTY = "No pages match that."
SEARCH_UNAVAILABLE = "Search is unavailable. Use the menu on the left."
EDITOR_PANELS = ("PREVIEW", "EXPORT")
COPY_CONFIRMATION = "Copied"
COURSE_HEADLINE = "Learn how this site was built."
WAITLIST_LABEL = "Join the waiting list"
FIELD_LABEL = "Email"
SUBMIT_LABEL = "SUBSCRIBE"
FALLBACK_LINE = "If the form fails, write to hello[at]lumenjs.example."
SUCCESS_MESSAGE = "Check your inbox to confirm."
INVALID_MESSAGE = "That does not look like an email address."
RATE_LIMITED_MESSAGE = "Too many attempts. Try again shortly."
CONFIRMED_MESSAGE = "You are on the list."
NOT_FOUND_HEADING = "Nothing here"
NOT_FOUND_BODY = "That address does not exist. Try one of these."
SERVER_ERROR_HEADING = "Something broke"
RETRY_LABEL = "TRY AGAIN"

CORRELATION_FIELD = "request_id"

SUCCESS_STATUSES = (200, 201, 202)
REDIRECT_STATUSES = (301, 302, 307, 308)
REFUSAL_STATUSES = (400, 401, 403, 404, 409, 422, 429)
DENIAL_STATUSES = (401, 403, 404)
NOT_FOUND_STATUSES = (404,)
RATE_LIMITED_STATUSES = (429,)

SETTLE_SECONDS = 0.4
POLL_BUDGET_SECONDS = 25.0
CONCURRENT_SUBMISSIONS = 25
NARROW_VIEWPORT_WIDTH = 390
WIDE_VIEWPORT_WIDTH = 1280
CONTRAST_BAR = 4.5
LARGE_TEXT_CONTRAST_BAR = 3.0

APP_DB_ROLE = "deku_app"
BINARY_ASSET_SUFFIXES = (".woff", ".woff2", ".ttf", ".otf", ".png", ".jpg",
                         ".jpeg", ".gif", ".webp", ".svgz", ".mp4", ".glb",
                         ".gltf", ".lottie")


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned pause, for an effect the app writes just after replying."""
    time.sleep(seconds)


def poll_until(predicate, budget: float = POLL_BUDGET_SECONDS):
    """Bounded polling on a monotonic clock. Returns the last value the predicate saw."""
    deadline = time.monotonic() + budget
    value = predicate()
    while not value and time.monotonic() < deadline:
        settle()
        value = predicate()
    return value


def unique_suffix() -> str:
    return uuid.UUID(bytes=os.urandom(16), version=4).hex[:10]


def probe_email() -> str:
    return f"probe-{unique_suffix()}@example.com"


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code} :: {response.text[:400]}")


def flat_positions() -> list[tuple[str, str]]:
    """The whole flattened sequence, module order then page order."""
    out = []
    for slug, _name, _ramp, _tile, _object in MODULES:
        for page in PAGES[slug]:
            out.append((slug, page))
    return out


def page_route(module: str, page: str) -> str:
    return f"{DOCS_ROUTE}/{module}/{page}"


def index_key(version: str) -> str:
    return INDEX_KEY.format(version=version)


def poster_key(version: str, module: str, page: str) -> str:
    return POSTER_KEY.format(version=version, module=module, page=page)


def mark_key(external_id: str) -> str:
    return MARK_KEY.format(external_id=external_id)


def relative_luminance(rgb: tuple[float, float, float]) -> float:
    channels = []
    for raw in rgb:
        channel = raw / 255.0
        channels.append(channel / 12.92 if channel <= 0.03928
                        else ((channel + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(first: tuple[float, float, float],
                   second: tuple[float, float, float]) -> float:
    one = relative_luminance(first)
    two = relative_luminance(second)
    lighter, darker = max(one, two), min(one, two)
    return (lighter + 0.05) / (darker + 0.05)


def parse_rgb(value: str) -> tuple[float, float, float]:
    numbers = [float(part) for part in
               value.replace("rgba", "").replace("rgb", "")
                    .strip("() ").split(",")[:3]]
    return (numbers[0], numbers[1], numbers[2])


class Session:
    """One signed-in or anonymous caller against the app's own API."""

    def __init__(self, token: str | None = None, email: str | None = None) -> None:
        self.token = token
        self.email = email
        self._cookies = httpx.Cookies()

    def _client(self) -> httpx.Client:
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        return httpx.Client(base_url=appclient.api_base(), timeout=30.0,
                            headers=headers, cookies=self._cookies,
                            follow_redirects=False)

    def request(self, method: str, path: str, body: dict | None = None,
                params: dict | None = None, data: dict | None = None,
                headers: dict | None = None) -> httpx.Response:
        with self._client() as client:
            response = client.request(method, path, json=body, data=data,
                                      params=params, headers=headers or {})
        self._cookies.update(response.cookies)
        return response

    def get(self, path: str, **params: Any) -> httpx.Response:
        return self.request("GET", path,
                            params={k: v for k, v in params.items() if v is not None})

    def post(self, path: str, body: dict | None = None,
             form: dict | None = None,
             headers: dict | None = None) -> httpx.Response:
        return self.request("POST", path, body=body, data=form, headers=headers)

    def patch(self, path: str, body: dict | None = None) -> httpx.Response:
        return self.request("PATCH", path, body=body)

    def delete(self, path: str) -> httpx.Response:
        return self.request("DELETE", path)

    def versions(self) -> httpx.Response:
        return self.get("/versions")

    def tree(self, version: str) -> httpx.Response:
        return self.get(f"/documentation/{version}/tree")

    def page_of(self, version: str, module: str, page: str) -> httpx.Response:
        return self.get(f"/pages/{version}/{module}/{page}")

    def search_index(self, version: str) -> httpx.Response:
        return self.get(f"/search-index/{version}")

    def sponsors(self, surface: str) -> httpx.Response:
        return self.get("/sponsors", surface=surface)

    def ad_slot(self) -> httpx.Response:
        return self.get("/ad-slot")

    def subscribe(self, email: str, mailing_list: str,
                  honeypot: str = "", timing_token: str | None = None,
                  origin: str | None = None) -> httpx.Response:
        form = {"email": email, "list": mailing_list, HONEYPOT_FIELD: honeypot}
        if timing_token is not None:
            form["timing_token"] = timing_token
        headers = {"Origin": origin} if origin else None
        return self.post("/subscribe", form=form, headers=headers)

    def timing_token(self) -> httpx.Response:
        return self.get("/subscribe/token")

    def confirm(self, token: str) -> httpx.Response:
        return self.get("/subscribe/confirm", token=token)

    def unsubscribe(self, token: str) -> httpx.Response:
        return self.post("/unsubscribe", {"token": token})

    def record_event(self, kind: str, attributes: dict) -> httpx.Response:
        return self.post("/events", {"kind": kind, "attributes": attributes})

    def storage_choice(self, choice: str) -> httpx.Response:
        return self.post("/storage-choice", {"choice": choice})

    def studio_versions(self) -> httpx.Response:
        return self.get("/studio/versions")

    def create_version(self, label: str, sort_key: str) -> httpx.Response:
        return self.post("/studio/versions", {"label": label, "sort_key": sort_key})

    def validate_version(self, version_id: Any) -> httpx.Response:
        return self.post(f"/studio/versions/{version_id}/validate", {})

    def publish_version(self, version_id: Any) -> httpx.Response:
        return self.post(f"/studio/versions/{version_id}/publish", {})

    def create_module(self, body: dict) -> httpx.Response:
        return self.post("/studio/modules", body)

    def create_page(self, body: dict) -> httpx.Response:
        return self.post("/studio/pages", body)

    def amend_page(self, page_id: Any, body: dict) -> httpx.Response:
        return self.patch(f"/studio/pages/{page_id}", body)

    def outbox(self, state: str | None = None) -> httpx.Response:
        return self.get("/studio/outbox", state=state)

    def deliver(self, message_id: Any) -> httpx.Response:
        return self.post(f"/studio/outbox/{message_id}/deliver", {})

    def roster_availability(self, available: bool) -> httpx.Response:
        return self.post("/studio/roster/availability", {"available": available})

    def set_ad_slot(self, state: str) -> httpx.Response:
        return self.post("/studio/ad-slot", {"state": state})

    def run_job(self, job_name: str) -> httpx.Response:
        return self.post(f"/studio/jobs/{job_name}/run", {})

    def jobs(self) -> httpx.Response:
        return self.get("/studio/jobs")

    def dead_letters(self) -> httpx.Response:
        return self.get("/studio/dead-letters")

    def page_views(self, since: str | None = None) -> httpx.Response:
        return self.get("/studio/page-views", **{"from": since})

    def mail_hook(self, body: dict, signature: str | None = None) -> httpx.Response:
        headers = {"X-Signature": signature} if signature is not None else {}
        return self.post("/hooks/mail", body, headers=headers)

    def mail_event(self, body: dict) -> httpx.Response:
        return self.post("/studio/mail-events", body)


class Store:
    """Domain reads over the persisted rows the brief pins by name."""

    def __init__(self, backend: Any) -> None:
        self.backend = backend

    def query(self, sql: str, params: tuple = ()) -> list[dict]:
        return self.backend.query(sql, params)

    def count(self, table: str, **where: Any) -> int:
        return self.backend.count(table, **where)

    def rows(self, table: str, limit: int | None = None, **where: Any) -> list[dict]:
        return self.backend.rows(table, limit=limit, **where)

    def account_by_email(self, email: str) -> dict | None:
        found = self.query(
            "SELECT * FROM account WHERE lower(email) = lower(%s)", (email,))
        return found[0] if found else None

    def version(self, label: str) -> dict | None:
        found = self.query("SELECT * FROM version WHERE label = %s", (label,))
        return found[0] if found else None

    def current_version(self) -> dict | None:
        found = self.query("SELECT * FROM version WHERE is_current = true")
        return found[0] if found else None

    def modules_of(self, version_id: Any) -> list[dict]:
        return self.query(
            "SELECT * FROM module WHERE version_id = %s ORDER BY position",
            (version_id,))

    def module(self, version_id: Any, slug: str) -> dict | None:
        found = self.query(
            "SELECT * FROM module WHERE version_id = %s AND slug = %s",
            (version_id, slug))
        return found[0] if found else None

    def pages_of(self, version_id: Any) -> list[dict]:
        return self.query(
            "SELECT * FROM page WHERE version_id = %s ORDER BY flat_position",
            (version_id,))

    def page(self, version_id: Any, module_id: Any, slug: str) -> dict | None:
        found = self.query(
            "SELECT * FROM page WHERE version_id = %s AND module_id = %s "
            "AND slug = %s", (version_id, module_id, slug))
        return found[0] if found else None

    def anchors_of(self, page_id: Any) -> list[dict]:
        return self.query(
            "SELECT * FROM page_anchor WHERE page_id = %s ORDER BY position",
            (page_id,))

    def demo(self, demo_id: Any) -> dict | None:
        found = self.query("SELECT * FROM demo WHERE id = %s", (demo_id,))
        return found[0] if found else None

    def tier(self, slug: str) -> dict | None:
        found = self.query("SELECT * FROM sponsor_tier WHERE slug = %s", (slug,))
        return found[0] if found else None

    def sponsor(self, external_id: str) -> dict | None:
        found = self.query(
            "SELECT * FROM sponsor WHERE external_id = %s", (external_id,))
        return found[0] if found else None

    def roster_source(self) -> dict | None:
        found = self.query("SELECT * FROM roster_source LIMIT 1")
        return found[0] if found else None

    def subscriber(self, email: str, mailing_list: str) -> dict | None:
        found = self.query(
            "SELECT * FROM subscriber WHERE lower(email) = lower(%s) "
            "AND list = %s", (email, mailing_list))
        return found[0] if found else None

    def subscribers_for(self, email: str) -> list[dict]:
        return self.query(
            "SELECT * FROM subscriber WHERE lower(email) = lower(%s)", (email,))

    def outbox_for(self, subscriber_id: Any) -> list[dict]:
        return self.query(
            "SELECT * FROM outbox_message WHERE subscriber_id = %s ORDER BY id",
            (subscriber_id,))

    def mail_events(self, provider_event_id: str) -> list[dict]:
        return self.query(
            "SELECT * FROM mail_event WHERE provider_event_id = %s",
            (provider_event_id,))

    def job_runs(self, job_name: str) -> list[dict]:
        return self.query(
            "SELECT * FROM job_run WHERE job_name = %s ORDER BY id", (job_name,))

    def dead_letters(self) -> list[dict]:
        return self.query("SELECT * FROM dead_letter ORDER BY id")

    def page_views(self) -> list[dict]:
        return self.query("SELECT * FROM page_view ORDER BY id")

    def analytics(self, kind: str) -> list[dict]:
        return self.query(
            "SELECT * FROM analytics_event WHERE kind = %s ORDER BY id", (kind,))

    def ad_slot_state(self) -> dict | None:
        found = self.query("SELECT * FROM ad_slot_state LIMIT 1")
        return found[0] if found else None


@pytest.fixture(scope="session")
def store() -> Store:
    return Store(capabilities.make_backend())


@pytest.fixture(scope="session")
def objects():
    return capabilities.make_store()


@pytest.fixture(scope="session")
def app_base() -> str:
    return appclient.api_base()


@pytest.fixture(scope="session")
def site_base() -> str:
    return appclient.app_url()


@pytest.fixture()
def anonymous() -> Session:
    return Session()


@pytest.fixture()
def maintainer() -> Session:
    return Session(appclient.login(MAINTAINER_EMAIL, PASSWORD), MAINTAINER_EMAIL)


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as driver:
        engine = driver.chromium.launch()
        yield engine
        engine.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context(viewport={"width": WIDE_VIEWPORT_WIDTH,
                                            "height": 900})
    opened = context.new_page()
    yield opened
    context.close()


@pytest.fixture()
def narrow_page(browser):
    context = browser.new_context(
        viewport={"width": NARROW_VIEWPORT_WIDTH, "height": 780},
        has_touch=True, is_mobile=True)
    opened = context.new_page()
    yield opened
    context.close()


@pytest.fixture()
def still_page(browser):
    context = browser.new_context(viewport={"width": WIDE_VIEWPORT_WIDTH,
                                            "height": 900},
                                  reduced_motion="reduce")
    opened = context.new_page()
    yield opened
    context.close()


def payload_of(response: httpx.Response) -> dict:
    body = response.json()
    assert isinstance(body, dict), f"expected a JSON object: {describe(response)}"
    return body


def rows_of(response: httpx.Response) -> list:
    body = response.json()
    assert isinstance(body, list), (
        f"a list endpoint returns a top-level JSON array: {describe(response)}")
    return body


def field_of(payload: dict, *names: str) -> Any:
    for name in names:
        if name in payload:
            return payload[name]
    raise AssertionError(f"none of {names} present in {sorted(payload)[:20]}")


def timing_token(session: "Session") -> str:
    """The token the form is issued with, waited out past its instant-submission bound."""
    response = session.timing_token()
    assert response.status_code in SUCCESS_STATUSES, describe(response)
    token = response.json().get("timing_token")
    assert token, f"no timing token was issued: {describe(response)}"
    settle(TIMING_TOKEN_SECONDS + 0.5)
    return token


def fetch(site_base: str, path: str, **kwargs: Any) -> httpx.Response:
    with httpx.Client(base_url=site_base, timeout=30.0,
                      follow_redirects=False) as client:
        return client.get(path, **kwargs)
