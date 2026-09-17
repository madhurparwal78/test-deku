from __future__ import annotations

import hashlib
import math
import os
import re
import struct
import threading
import time
from urllib.parse import urljoin, urlparse

import httpx
import pytest
from playwright.sync_api import sync_playwright

import appclient
import capabilities
import _shapes

TIMEOUT = 30.0
SETTLE_STEP = 0.25
SETTLE_LIMIT = 20.0
BENCH_DEADLINE_LIMIT = 45.0

CORPUS_PASSWORD = "deku-demo-pw-2026"
OWNER_EMAIL = "creator@example.com"
SECOND_STUDIO_EMAIL = "creator2@example.com"
MEMBER_EMAIL = "creator3@example.com"
CLIENT_EMAIL = "client@example.com"
SEEDED_EMAILS = (OWNER_EMAIL, SECOND_STUDIO_EMAIL, MEMBER_EMAIL, CLIENT_EMAIL)
SEEDED_NAMES = {OWNER_EMAIL: "Noa Lindqvist", SECOND_STUDIO_EMAIL: "Rafael Moura",
                MEMBER_EMAIL: "Aiko Tanaka", CLIENT_EMAIL: "Jonas Weber"}

NORTHLIGHT = "Northlight Studio"
SALTMARSH = "Saltmarsh Cut"
CITRUS_LAUNCH = "Citrus Launch"
AUTUMN_LOOKBOOK = "Autumn Lookbook"
TRAILER_CUT = "Trailer Cut"
FIRST_CANVAS_NAME = "My first canvas"
SEEDED_DELIVERY_NOTE = "Billboard for sign-off"
NORTHLIGHT_BALANCE = 108596
SALTMARSH_BALANCE = 20000
TRIAL_CREDITS = 500

PLAN_CODES = ("free", "creator", "growth", "professional", "enterprise")
PLAN_NAMES = ("Free", "Creator", "Growth", "Professional", "Enterprise")
PLAN_DESCRIPTORS = (
    "Try every model on the canvas",
    "Deliver client work every week",
    "Scale a busy solo practice fast",
    "Run a studio on one shared canvas",
    "Bring the whole team and its rules",
)
MONTHLY_MINOR = {"free": 0, "creator": 2000, "growth": 5000, "professional": 11000}
ANNUAL_MINOR = {"free": 0, "creator": 1700, "growth": 4300, "professional": 9300}
PLAN_CREDITS = {"free": 500, "creator": 20000, "growth": 50000, "professional": 110000}
PROFESSIONAL_OPTIONS = {
    "110k": {"credits": 110000, "monthly": 11000, "annual": 9300,
             "yield_images": 1527, "yield_videos": 110},
    "300k": {"credits": 300000, "monthly": 30000, "annual": 25500,
             "yield_images": 4166, "yield_videos": 300},
}
PLAN_YIELDS = {"creator": (277, 20), "growth": (694, 50)}
PACK_CREDITS = 1000
PACK_PRICE_MINOR = 1000
SAVING_CHIP = "Save up to 15%"

CURRENT_RATE_VERSION = "2026-09"
RETIRED_RATE_VERSION = "2026-06"
RATES = {
    "2026-06": {("image", "standard"): 80, ("image", "high"): 160,
                ("video", "standard"): 1100, ("video", "high"): 2200,
                ("audio", "standard"): 40, ("audio", "high"): 80,
                ("text", "standard"): 4, ("text", "high"): 8},
    "2026-09": {("image", "standard"): 72, ("image", "high"): 144,
                ("video", "standard"): 1000, ("video", "high"): 2000,
                ("audio", "standard"): 40, ("audio", "high"): 80,
                ("text", "standard"): 4, ("text", "high"): 8},
}

MODELS = (
    ("halcyon-2-1", "Halcyon 2.1", "Brightwater Labs", "image", "standard", "available"),
    ("prism-xl-1-5", "Prism XL 1.5", "Oakline AI", "image", "slow", "available"),
    ("vesper-3", "Vesper 3", "Parallax Works", "image", "standard", "available"),
    ("lumen-preview", "Lumen Preview", "Sable Research", "image", "fast", "degraded"),
    ("grain-4-turbo", "Grain 4 Turbo", "Kestrel Systems", "image", "fast", "available"),
    ("atlas-image-1", "Atlas Image 1", "Marlow Studio", "image", "standard", "available"),
    ("tessera-0-9", "Tessera 0.9", "Cinder Labs", "image", "slow", "available"),
    ("folio-2", "Folio 2", "Quillon", "image", "standard", "available"),
    ("drift-1-6", "Drift 1.6", "Brightwater Labs", "video", "fast", "available"),
    ("kinetic-3-pro", "Kinetic 3 Pro", "Oakline AI", "video", "slow", "available"),
    ("reel-2-5", "Reel 2.5", "Parallax Works", "video", "standard", "available"),
    ("driftwood-beta", "Driftwood Beta", "Sable Research", "video", "slow", "degraded"),
    ("strata-video-2", "Strata Video 2", "Kestrel Systems", "video", "standard", "available"),
    ("montage-1", "Montage 1", "Cinder Labs", "video", "slow", "available"),
    ("chorus-2", "Chorus 2", "Marlow Studio", "audio", "standard", "available"),
    ("timbre-1-1", "Timbre 1.1", "Quillon", "audio", "slow", "available"),
    ("echo-voice-3", "Echo Voice 3", "Oakline AI", "audio", "standard", "available"),
    ("score-lite", "Score Lite", "Kestrel Systems", "audio", "fast", "available"),
    ("ivo-writer-4", "Ivo Writer 4", "Quarro", "text", "standard", "available"),
    ("lexicon-7", "Lexicon 7", "Brightwater Labs", "text", "slow", "available"),
    ("quill-3-mini", "Quill 3 Mini", "Quillon", "text", "fast", "available"),
    ("parley-2", "Parley 2", "Parallax Works", "text", "standard", "available"),
)
MODEL_SLUGS = tuple(m[0] for m in MODELS)
AUTO_RESOLUTION = {"image": "grain-4-turbo", "video": "drift-1-6",
                   "audio": "score-lite", "text": "quill-3-mini"}
ASPECTS = {"image": ["4:5", "16:9", "1:1"], "video": ["16:9", "9:16"],
           "audio": [], "text": []}
IMAGE_MAX_DIMENSIONS = "2048 x 2048"
VIDEO_MAX_DIMENSIONS = "1920 x 1080"
FAILING_ENGINE_REASON = "Engine unavailable"

GRAPH_KEYS = ("advertising", "e-commerce", "filmmaking", "fashion", "branding")
GRAPH_LABELS = ("Advertising", "E-commerce", "Filmmaking", "Fashion", "Branding")
ADVERTISING_BRIEF = (
    "Launch Fizzwell, a sparkling citrus soda, for summer: one hero pack shot, "
    "a billboard and a fifteen-second cut."
)
ADVERTISING_NODES = {
    "product-mockup": ("Product Mockup", "image", "halcyon-2-1", "4:5", 1, ()),
    "studio-shot": ("Studio Shot", "image", "prism-xl-1-5", "4:5", 2, ("product-mockup",)),
    "pack-shot": ("Pack Shot", "image", "vesper-3", "4:5", 2, ("product-mockup",)),
    "tagline": ("Tagline", "text", "lexicon-7", None, 2, ("product-mockup",)),
    "lifestyle-scene": ("Lifestyle Scene", "image", "grain-4-turbo", "16:9", 3, ("studio-shot",)),
    "jingle": ("Jingle", "audio", "chorus-2", None, 3, ("tagline",)),
    "ooh-billboard": ("OOH Billboard", "image", "atlas-image-1", "16:9", 4,
                      ("lifestyle-scene", "pack-shot")),
    "movie-cut-1": ("Movie Cut 1", "video", "kinetic-3-pro", "16:9", 5, ("ooh-billboard",)),
}
OTHER_GRAPH_TITLES = {
    "e-commerce": ("Product Cutout", "Colourway Grid", "Pack Shot", "Listing Copy",
                   "Unboxing Clip"),
    "filmmaking": ("Storyboard", "Location Plate", "Character Study", "Temp Score",
                   "Movie Cut 1"),
    "fashion": ("Croquis", "Fabric Swatch", "Lookbook Still", "Runway Loop",
                "Collection Notes"),
    "branding": ("Moodboard", "Logo Study", "Brand Voice", "Sonic Logo", "Launch Film"),
}
NEARBY_LINE = "Showing a nearby result"
REPLAY_SESSION_LIMIT = 30

POSTS = (
    ("series-a-for-one-canvas", "Quarro raises its Series A to build the one canvas",
     "company-news", "Sep 10, 2026", "4 min read"),
    ("vesper-3-lands", "Vesper 3 lands on the canvas", "company-news", "Sep 3, 2026",
     "3 min read"),
    ("halcyon-vs-prism-xl", "Halcyon 2.1 against Prism XL 1.5 on product stills",
     "comparisons", "Aug 27, 2026", "9 min read"),
    ("storyboard-to-trailer", "Chaining a storyboard into a trailer in one graph",
     "guides", "Aug 20, 2026", "7 min read"),
    ("kinetic-vs-reel", "Kinetic 3 Pro against Reel 2.5 for fifteen-second cuts",
     "comparisons", "Aug 13, 2026", "8 min read"),
    ("how-credits-are-counted", "How credits are counted, run by run", "guides",
     "Aug 6, 2026", "5 min read"),
    ("desktop-watches-folders", "The desktop app now watches your folders",
     "company-news", "Jul 30, 2026", "3 min read"),
    ("briefs-ivo-can-route", "Writing briefs Ivo can route", "guides", "Jul 23, 2026",
     "6 min read"),
    ("chorus-vs-timbre", "Chorus 2 against Timbre 1.1 for sonic logos", "comparisons",
     "Jul 16, 2026", "6 min read"),
    ("delivering-without-attachments", "Delivering work to clients without an attachment",
     "guides", "Jul 9, 2026", "5 min read"),
    ("why-we-price-in-credits", "Why we price in credits", "company-news", "Jul 2, 2026",
     "4 min read"),
    ("lexicon-vs-quill", "Lexicon 7 against Quill 3 Mini for taglines", "comparisons",
     "Jun 25, 2026", "7 min read"),
    ("lookbook-from-a-croquis", "Building a lookbook from a single croquis", "guides",
     "Jun 18, 2026", "6 min read"),
    ("opening-the-porto-studio", "Opening our Porto studio", "company-news",
     "Jun 11, 2026", "3 min read"),
)
BLOG_PAGE_SIZE = 12

DESKTOP_VERSION = "2.4.0"
DESKTOP_RELEASES = {
    ("macos", "arm64"): "Download for macOS (Apple silicon)",
    ("macos", "x64"): "Download for macOS (Intel)",
    ("windows", "x64"): "Download for Windows",
    ("linux", "x64"): "Download for Linux",
}
NATIVE_CAPABILITIES = ("Watch a folder", "Capture anything on screen", "Queue runs offline")
TEAM_NAMES = ("Ines Carvalho", "Tomas Reyes", "Hana Okafor", "Luca Brandt",
              "Mira Solberg", "Dev Anand", "Clara Voss", "Sami Haddad")
OPEN_ROLES = ("Senior Graphics Engineer", "Product Designer, Canvas",
              "Model Partnerships Lead", "Staff Backend Engineer, Billing",
              "Community Producer")
INVESTOR_NAMES = ("Amara Whitfield", "Kenji Morrow", "Sofia Brennan", "Owen Castell",
                  "Lena Hartmann", "Marcus Obi", "Yara Lindgren", "Theo Marchetti")
VIGNETTES = ("The team", "The office", "The adventures", "The dog")
ENTERPRISE_TABS = ("Platform", "Controls", "Support")
ENTERPRISE_CARDS = ("Collaborative canvas", "Agent connector", "Brand kits",
                    "Chat-tool creation", "Shared asset library")
ENTERPRISE_ACTION = "Book a call"
TEAM_SIZES = ("1-10", "11-50", "51-200", "201+")
ANNOUNCEMENT_TEXT = "Vesper 3 is now on Quarro."
NOT_FOUND_LINE = "This page is not on the canvas."
NOT_FOUND_ACTION = "Back to home"
PRIVACY_ROUTE = "/privacy"
PRIVACY_EMAIL = "privacy@quarro.dev"
CANVAS_TABLE_COLUMNS = ("Name", "Nodes", "Last run", "Credits spent")
CANVAS_INLINE_PLACEHOLDER = "Name a new canvas"
CANVAS_EMPTY_LINE = "No canvases yet. Name one above to start."
DELIVERY_COLUMNS = ("Output", "Client", "Sent", "State")
FOOTER_TEXT = ("Product", "Company", "Resources", "Legal", "Quarro, Porto")
PLAN_ARITHMETIC = "Creator buys 277 standard runs a month"
MODELS_HEADLINE = "Every model, one canvas."
PRICING_TEXT = (
    "One plan, every model.", "Credits that follow the work.", "Usage and limits",
    "Creative tools", "Support", "Monthly credits", "Additional credit packs", "Queue priority",
    "All models", "Custom agent skills", "Unlimited seats", "Multiplayer canvas",
    "Community support", "Priority email support", "Dedicated success manager", "500 once",
    "$10 per 1,000 credits", "110,000 to 300,000", "Limited trial", "Custom",
    "277 images or 20 videos", "694 images or 50 videos", "1,527 images or 110 videos",
    "How many credits does your work need?",
)
ROUTE_COPY = {
    "/": ("Make it once.", "Then make it everywhere.",
          "One canvas, one subscription, every image, video, sound and language model worth "
          "using. Ivo picks one when you do not.",
          "Agencies", "Creative directors and filmmakers", "Marketers", "E-commerce",
          "Go-to-market", "Campaign variants", "Launch films"),
    "/bench": ("One brief. Up to four models.", "Run the comparison"),
    "/desktop-app": ("Quarro for your desktop.",),
    "/manifesto": ("Made by hand, at the speed of thought.",),
    "/blog": ("Field notes, guides", "and model comparisons."),
    "/enterprise": ("Your studio, one canvas.",
                    "One shared canvas for the whole studio, with the controls, support and "
                    "procurement path a team needs before it moves its client work onto it."),
}
UNNAMED_PROBE = (
    "els => els.filter(e => !(e.innerText.trim() || e.getAttribute('aria-label') || "
    "e.getAttribute('aria-labelledby') || e.getAttribute('title'))).length"
)
SMALL_TARGET_PROBE = (
    "els => els.filter(e => e.offsetParent !== null).map(e => e.getBoundingClientRect())"
    ".filter(r => r.width < 44 || r.height < 44).length"
)
CONTRAST_PROBE = (
    "() => { const bg = (el) => { while (el) { const c = getComputedStyle(el).backgroundColor; "
    "if (c && c !== 'transparent' && !c.startsWith('rgba(0, 0, 0, 0)')) return c; "
    "el = el.parentElement; } return 'rgb(255, 255, 255)'; }; "
    "return Array.from(document.querySelectorAll('main p'))"
    ".filter(p => p.offsetParent !== null && p.innerText.trim()).slice(0, 20)"
    ".map(p => [getComputedStyle(p).color, bg(p)]); }"
)

ERROR_CODES = ("invalid_request", "unauthenticated", "forbidden", "not_found",
               "conflict", "insufficient_credits", "limit_reached", "plan_required",
               "stale_generation")

PUBLIC_ROUTES = (
    "/", "/pricing", "/models", "/bench", "/enterprise", "/desktop-app", "/manifesto",
    "/blog", "/about", "/about/roles", "/privacy", "/terms", "/acceptable-use",
    "/sign-in", "/sign-up",
)
SIGNED_IN_ROUTES = ("/canvases", "/account/billing", "/account/team", "/deliveries")

OBJECT_KEY_RE = re.compile(r"^outputs/(\d+)/(\d+)/([0-9a-f]{64})\.(png|svg|wav|txt)$")
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
META_RE = re.compile(r"<meta\b[^>]*>", re.IGNORECASE)
LINK_RE = re.compile(r"<link\b[^>]*>", re.IGNORECASE)
ATTR_RE = re.compile(r"([a-zA-Z:-]+)\s*=\s*[\"']([^\"']*)[\"']")
NARROW_VIEWPORT = {"width": 390, "height": 844}
WINDOWS_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def settle(seconds: float = SETTLE_STEP) -> None:
    """The one sanctioned pause. A raw sleep in the test module is a finding."""
    time.sleep(seconds)


def unique_suffix() -> str:
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{unique_suffix()}@example.com"


def idem_key() -> str:
    return f"idem-{unique_suffix()}"


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def app_url() -> str:
    return appclient.app_url()


def api_base() -> str:
    return appclient.api_base()


def page_response(path: str, **headers) -> httpx.Response:
    return httpx.get(f"{app_url()}{path}", timeout=TIMEOUT, headers=headers,
                     follow_redirects=False)


def rendered_html(path: str) -> str:
    response = page_response(path)
    assert response.status_code == 200, (
        f"GET {path} returned {response.status_code} rather than a page: "
        f"{response.text[:300]}"
    )
    return response.text


def head_tags(html: str) -> dict:
    """Title, meta and link declarations of a served document, by name."""
    found = {"title": None, "meta": {}, "icons": []}
    title = TITLE_RE.search(html)
    if title:
        found["title"] = title.group(1).strip()
    for tag in META_RE.findall(html):
        attrs = dict((k.lower(), v) for k, v in ATTR_RE.findall(tag))
        key = attrs.get("name") or attrs.get("property")
        if key:
            found["meta"][key.lower()] = attrs.get("content", "")
    for tag in LINK_RE.findall(html):
        attrs = dict((k.lower(), v) for k, v in ATTR_RE.findall(tag))
        if "icon" in attrs.get("rel", "").lower():
            found["icons"].append(attrs.get("href", ""))
    return found


def absolute(path_or_url: str) -> str:
    return urljoin(f"{app_url()}/", path_or_url)


def is_internal(href: str) -> bool:
    if not href or href.startswith(("mailto:", "tel:", "javascript:", "#")):
        return False
    target = urlparse(absolute(href))
    return target.netloc == urlparse(app_url()).netloc


def token_for(email: str) -> str:
    return appclient.login(email, CORPUS_PASSWORD)


def client_for(email: str) -> httpx.Client:
    return appclient.client(token_for(email))


def anonymous() -> httpx.Client:
    return appclient.client(None)


def with_headers(client: httpx.Client, **extra) -> dict:
    merged = dict(client.headers)
    merged.update(extra)
    return merged


def sign_up(account_type: str | None = "creator", display_name: str = "Probe Maker",
            email: str | None = None) -> tuple[str, str, dict]:
    address = email or probe_email()
    payload = {"email": address, "password": CORPUS_PASSWORD,
               "display_name": display_name}
    if account_type is not None:
        payload["account_type"] = account_type
    response = httpx.post(f"{api_base()}/auth/sign-up", json=payload, timeout=TIMEOUT)
    assert response.status_code in (200, 201), (
        f"POST /api/auth/sign-up for {address} returned {response.status_code}: "
        f"{response.text[:400]}"
    )
    body = response.json()
    token = body.get("access_token")
    assert token, f"sign-up for {address} returned no access_token: {response.text[:300]}"
    return address, token, body


def fresh_creator(display_name: str = "Probe Maker") -> httpx.Client:
    _, token, _ = sign_up("creator", display_name)
    return appclient.client(token)


def error_code(response: httpx.Response) -> str | None:
    body = response.json()
    error = body.get("error") if isinstance(body, dict) else None
    return error.get("code") if isinstance(error, dict) else None


def refused(response: httpx.Response) -> bool:
    return 400 <= response.status_code < 500


def listed(response: httpx.Response) -> list[dict]:
    assert response.status_code == 200, (
        f"{response.request.method} {response.request.url} returned "
        f"{response.status_code}: {response.text[:300]}"
    )
    return _shapes.items(response.json())


def balance(client: httpx.Client) -> int:
    response = client.get("/v1/credits")
    assert response.status_code == 200, (
        f"GET /api/v1/credits returned {response.status_code}: {response.text[:300]}"
    )
    return int(response.json()["balance"])


def workspace(client: httpx.Client) -> dict:
    response = client.get("/v1/workspace")
    assert response.status_code == 200, (
        f"GET /api/v1/workspace returned {response.status_code}: {response.text[:300]}"
    )
    return response.json()


def canvases(client: httpx.Client) -> list[dict]:
    return listed(client.get("/v1/canvases"))


def canvas_named(client: httpx.Client, name: str) -> dict:
    match = [c for c in canvases(client) if c.get("name") == name]
    assert match, f"no canvas named {name!r} is visible to this studio"
    response = client.get(f"/v1/canvases/{match[0]['id']}")
    assert response.status_code == 200, (
        f"GET /api/v1/canvases/{match[0]['id']} returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    return response.json()


def node_by_key(canvas: dict, node_key: str) -> dict:
    match = [n for n in canvas.get("nodes", []) if n.get("node_key") == node_key]
    assert match, f"canvas {canvas.get('name')!r} carries no node {node_key!r}"
    return match[0]


def node_by_title(canvas: dict, title: str) -> dict:
    match = [n for n in canvas.get("nodes", []) if n.get("title") == title]
    assert match, f"canvas {canvas.get('name')!r} carries no node titled {title!r}"
    return match[0]


def new_canvas(client: httpx.Client, stem: str = "Probe canvas") -> dict:
    response = client.post("/v1/canvases", json={"name": f"{stem} {unique_suffix()}"})
    assert response.status_code in (200, 201), (
        f"POST /api/v1/canvases returned {response.status_code}: {response.text[:300]}"
    )
    return response.json()


def add_node(client: httpx.Client, canvas_id, *, title: str = "Probe node",
             prompt: str | None = None, model_slug: str = "halcyon-2-1",
             tier: str = "standard", aspect_ratio: str | None = "4:5",
             output_kind: str | None = None) -> dict:
    payload = {"title": title, "prompt": prompt or f"probe prompt {unique_suffix()}",
               "model_slug": model_slug, "tier": tier, "aspect_ratio": aspect_ratio,
               "pos_x": 0, "pos_y": 0}
    if output_kind is not None:
        payload["output_kind"] = output_kind
    response = client.post(f"/v1/canvases/{canvas_id}/nodes", json=payload)
    assert response.status_code in (200, 201), (
        f"POST /api/v1/canvases/{canvas_id}/nodes returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    return response.json()


def wire(client: httpx.Client, canvas_id, from_id, to_id) -> httpx.Response:
    return client.post(f"/v1/canvases/{canvas_id}/edges",
                       json={"from_node_id": from_id, "to_node_id": to_id})


def run_node(client: httpx.Client, canvas_id, node_id, key: str | None = None) -> httpx.Response:
    return client.post(f"/v1/canvases/{canvas_id}/nodes/{node_id}/runs",
                       headers=with_headers(client, **{"Idempotency-Key": key or idem_key()}))


def succeeded_run(client: httpx.Client, canvas_id, node_id, key: str | None = None) -> dict:
    response = run_node(client, canvas_id, node_id, key)
    assert response.status_code in (200, 201), (
        f"running node {node_id} returned {response.status_code}: {response.text[:400]}"
    )
    run = response.json()
    assert run.get("status") == "succeeded", (
        f"running node {node_id} reported status {run.get('status')!r}: {response.text[:300]}"
    )
    return run


def fetch_output(client: httpx.Client, asset_id) -> httpx.Response:
    return client.get(f"/v1/assets/{asset_id}/content")


def chain(client: httpx.Client, length: int, model_slug: str = "grain-4-turbo") -> tuple[dict, list[dict]]:
    canvas = new_canvas(client, "Probe chain")
    nodes = []
    for index in range(length):
        node = add_node(client, canvas["id"], title=f"Link {index + 1}",
                        model_slug=model_slug, aspect_ratio="16:9")
        if nodes:
            response = wire(client, canvas["id"], nodes[-1]["id"], node["id"])
            assert response.status_code in (200, 201), (
                f"wiring link {index} to link {index + 1} returned "
                f"{response.status_code}: {response.text[:300]}"
            )
        nodes.append(node)
    return canvas, nodes


def run_chain(client: httpx.Client, canvas: dict, nodes: list[dict]) -> list[dict]:
    return [succeeded_run(client, canvas["id"], node["id"]) for node in nodes]


def at_the_same_moment(*calls):
    """Release every call through one barrier and collect the responses in order."""
    barrier = threading.Barrier(len(calls))
    results = [None] * len(calls)

    def runner(index, call):
        barrier.wait()
        results[index] = call()

    threads = [threading.Thread(target=runner, args=(i, c)) for i, c in enumerate(calls)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(TIMEOUT)
    return results


def subscribe(client: httpx.Client, plan_code: str, period: str, option: str | None = None,
              key: str | None = None) -> httpx.Response:
    payload = {"plan_code": plan_code, "billing_period": period}
    if option is not None:
        payload["credit_option"] = option
    return client.post("/v1/subscription", json=payload,
                       headers=with_headers(client, **{"Idempotency-Key": key or idem_key()}))


def buy_packs(client: httpx.Client, packs: int, key: str | None = None) -> httpx.Response:
    return client.post("/v1/credit-packs", json={"packs": packs},
                       headers=with_headers(client, **{"Idempotency-Key": key or idem_key()}))


def storage_host() -> str:
    return urlparse(os.environ.get("STORAGE_ENDPOINT", "http://minio:9000")).netloc


def create_delivery(client: httpx.Client, asset_id, email: str,
                    note: str = "Probe delivery") -> dict:
    response = client.post("/v1/deliveries",
                           json={"asset_id": asset_id, "client_email": email, "note": note})
    assert response.status_code in (200, 201), (
        f"POST /api/v1/deliveries returned {response.status_code}: {response.text[:300]}"
    )
    body = response.json()
    assert body.get("state") == "delivered", (
        f"a new delivery reports state {body.get('state')!r}: {response.text[:300]}"
    )
    return body


def start_bench(client: httpx.Client, slugs, key: str | None = None,
                brief: str = "A glass bottle of citrus soda on a sunlit table") -> httpx.Response:
    return client.post("/v1/bench/runs", json={"brief": brief, "model_slugs": list(slugs)},
                       headers=with_headers(client, **{"Idempotency-Key": key or idem_key()}))


def await_bench(client: httpx.Client, run_id, limit: float = SETTLE_LIMIT) -> dict:
    """Bounded polling until the run leaves `running`, reporting what it saw."""
    deadline = time.monotonic() + limit
    latest = {}
    while time.monotonic() < deadline:
        response = client.get(f"/v1/bench/runs/{run_id}")
        assert response.status_code == 200, (
            f"GET /api/v1/bench/runs/{run_id} returned {response.status_code}: "
            f"{response.text[:300]}"
        )
        latest = response.json()
        if latest.get("status") in ("completed", "voided"):
            return latest
        settle()
    raise AssertionError(
        f"bench run {run_id} never left running within {limit} seconds; last seen "
        f"{str(latest)[:400]}"
    )


def frame_for(run: dict, slug: str) -> dict:
    match = [f for f in run.get("frames", []) if f.get("model_slug") == slug]
    assert match, f"bench run {run.get('id')} carries no frame for {slug}"
    return match[0]


def regenerate(session_id: str, node_key: str, prompt: str, token: int,
               model_slug: str | None = None, graph_key: str = "advertising") -> httpx.Response:
    model = model_slug or ADVERTISING_NODES[node_key][2]
    return httpx.post(f"{api_base()}/v1/replay/regenerate", timeout=TIMEOUT, json={
        "session_id": session_id, "graph_key": graph_key, "node_key": node_key,
        "prompt": prompt, "model_slug": model, "generation_token": token})


def replay_graphs() -> list[dict]:
    return listed(httpx.get(f"{api_base()}/v1/replay/graphs", timeout=TIMEOUT))


def graph(key: str) -> dict:
    match = [g for g in replay_graphs() if g.get("key") == key]
    assert match, f"GET /api/v1/replay/graphs lists no graph {key!r}"
    return match[0]


def forecast(rows, version: str = CURRENT_RATE_VERSION) -> httpx.Response:
    return httpx.post(f"{api_base()}/v1/forecasts", timeout=TIMEOUT, json={
        "visitor_id": f"visitor-{unique_suffix()}", "rate_version": version,
        "rows": [{"output_kind": k, "monthly_quantity": q, "tier": t} for k, q, t in rows]})


def two_significant(quantity: int) -> int:
    if quantity == 0:
        return 0
    magnitude = 10 ** (int(math.floor(math.log10(quantity))) - 1)
    return int(math.floor(quantity / magnitude + 0.5)) * magnitude


def png_size(payload: bytes) -> tuple[int, int]:
    assert payload[:8] == b"\x89PNG\r\n\x1a\n", "the output does not start with a PNG signature"
    width, height = struct.unpack(">II", payload[16:24])
    return width, height


def ratio_of(aspect: str) -> float:
    left, right = aspect.split(":")
    return int(left) / int(right)


def luminance(rgb) -> float:
    def channel(value):
        value = value / 255
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(fg, bg) -> float:
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def parse_rgb(css: str):
    numbers = re.findall(r"[\d.]+", css)
    return tuple(int(float(n)) for n in numbers[:3])


@pytest.fixture(scope="session")
def store() -> capabilities.ObjectStore:
    return capabilities.make_store()


@pytest.fixture(scope="session")
def backend() -> capabilities.Backend:
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def _chromium():
    with sync_playwright() as driver:
        browser = driver.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(_chromium):
    context = _chromium.new_context(viewport={"width": 1440, "height": 900})
    opened = context.new_page()
    opened.set_default_timeout(TIMEOUT * 1000)
    yield opened
    context.close()


@pytest.fixture
def browser_page(_chromium):
    """A factory: open a page in a fresh context with the given options."""
    contexts = []

    def open_page(**options):
        context = _chromium.new_context(**options)
        contexts.append(context)
        opened = context.new_page()
        opened.set_default_timeout(TIMEOUT * 1000)
        return opened

    yield open_page
    for context in contexts:
        context.close()


@pytest.fixture
def owner():
    with client_for(OWNER_EMAIL) as client:
        yield client


@pytest.fixture
def second_studio():
    with client_for(SECOND_STUDIO_EMAIL) as client:
        yield client


@pytest.fixture
def member():
    with client_for(MEMBER_EMAIL) as client:
        yield client


@pytest.fixture
def client_user():
    with client_for(CLIENT_EMAIL) as client:
        yield client


@pytest.fixture
def guest():
    with anonymous() as client:
        yield client


@pytest.fixture
def citrus(owner) -> dict:
    return canvas_named(owner, CITRUS_LAUNCH)
