from __future__ import annotations

import os
import time
import uuid

import httpx
import pytest
from playwright.sync_api import sync_playwright

from capabilities import make_backend

APP_URL = os.environ.get("APP_PUBLIC_URL", "http://localhost:4173").rstrip("/")
API = f"{APP_URL}/api"

CORPUS_PASSWORD = "deku-demo-pw-2026"
OWNER_EMAIL = "owner@example.com"
ADMIN_EMAIL = "admin@example.com"
OPERATOR_EMAIL = "operator@example.com"
ANALYST_EMAIL = "analyst@example.com"
SECOND_OWNER_EMAIL = "owner2@example.com"
OWNER_NAME = "Amelia Ortega"
ADMIN_NAME = "Ravi Menon"
OPERATOR_NAME = "Lena Fischer"
ANALYST_NAME = "Tomas Silva"
SECOND_OWNER_NAME = "Priya Raman"

MEMBER_ROLES = ("owner", "admin", "operator", "analyst")
WORKSPACE_SLUG = "kestrel-demo"
SECOND_WORKSPACE_SLUG = "northmoor"
APP_SLUG = "kestrel-web"
SECOND_APP_SLUG = "northmoor-shop"

SITE_INDEX = "site_content"
STORY_INDEX = "customer_stories"
CATALOG_INDEX = "catalog"
SHIRT_INDEX = "shirts"
FIXTURE_INDEX = "fixtures"
SEEDED_INDICES = (SITE_INDEX, STORY_INDEX, CATALOG_INDEX, SHIRT_INDEX,
                  FIXTURE_INDEX)

SOURCE_FACET = "source"
SOURCE_VALUES = ("Documentation", "Support", "Blog", "Website", "Developers",
                 "Resources", "Academy", "Customer Stories")
SOURCE_COUNTS = {"Documentation": 40, "Support": 24, "Blog": 18, "Website": 12,
                 "Developers": 9, "Resources": 8, "Academy": 5,
                 "Customer Stories": 4}
SITE_RECORD_COUNT = 120

STORY_COUNT = 24
STORY_FACETS = ("Features", "Use Case", "Industry", "Region", "Integration")
INDUSTRY_COUNTS = {"Ecommerce": 10, "Media": 5, "Marketplace": 4, "B2B": 3,
                   "Travel": 2}
REGION_COUNTS = {"North America": 10, "Europe": 8, "Asia Pacific": 4,
                 "Latin America": 2}
STORY_TITLES = (
    "Northmoor Group leverages Kestrel to boost search performance",
    "Keeping it fast and cool. Culture Yard speeds up Search",
    "Halcyon Sport achieves +150% sales contribution from search",
)

CATALOG_COUNT = 36
CATALOG_BRANDS = ("acme", "zeta")
CATALOG_COLOURS = ("red", "blue")
CATALOG_CELLS = {("acme", "red"): 10, ("acme", "blue"): 5,
                 ("zeta", "red"): 20, ("zeta", "blue"): 1}
GEO_POINT = "48.8566,2.3522"
GEO_DISTANCES = (5, 8, 60)
GEO_POPULARITIES = (1, 100, 50)

SHIRT_COUNT = 1200
SHIRT_GROUPS = 300
SHIRT_ATTRIBUTE = "shirt_id"
SHIRT_PAGES = 15
SHIRT_RED_RECORDS = 300
SHIRT_RED_GROUPS = 75

TEXT_FIXTURES = {
    "t1": "Hello World",
    "t2": "Helo Word",
    "t3": "Crème Brûlée",
    "t4": "2024 Edition",
    "t5": "2025 Edition",
    "t6": "東京都庁",
    "t7": "Straße",
}
RANK_FIXTURES = {
    "r1": "Blue Running Shoes",
    "r2": "Blue Runing Shoes",
    "r3": "Shoes Running Blue",
    "r4": "Blue Shoes",
}
RANK_ORDER = ("r1", "r3", "r4", "r2")
RANK_POPULARITY = {"r1": 1, "r2": 100, "r3": 50, "r4": 90}
CUSTOM_RANKING = "desc(popularity)"

SITE_SEARCH_KEY_ID = "key_site_search"
SITE_SEARCH_KEY = "sk_site_1f6b2d8e4a"
STORY_SEARCH_KEY_ID = "key_story_search"
STORY_SEARCH_KEY = "sk_story_3c9a7e51b2"
INGEST_KEY_ID = "key_ingest_demo"
INGEST_KEY = "ik_demo_74d2c0a9f1"

HIGHLIGHT_PRE_TAG = "<em>"
HIGHLIGHT_POST_TAG = "</em>"
SNIPPET_ELLIPSIS = "..."
PAGINATION_LIMIT = 1000
DEFAULT_HITS_PER_PAGE = 20
QUERY_ID_LENGTH = 32
PROXIMITY_CAP = 8
WORD_POSITION_CAP = 63
MIN_WORD_SIZE_1_TYPO = 4
MIN_WORD_SIZE_2_TYPOS = 8
PREFIX_EXPANSION_BOUND = 1000
EARTH_RADIUS_METRES = 6371000
AROUND_PRECISION_METRES = 10
RELEVANCY_STRICTNESS = 100
RANKING_CRITERIA = ("typo", "geo", "words", "filters", "proximity",
                    "attribute", "exact", "custom")
HONESTY_FLAGS = ("exhaustiveNbHits", "exhaustiveFacetsCount", "exhaustiveTypo")

DEMO_FIELDS = ("First Name", "Last Name", "Business Email", "Phone", "Company",
               "Country")
DEMO_KEYS = ("firstName", "lastName", "email", "phone", "company", "country")
DEMO_SUBMIT = "Get In Touch"
DEMO_STATUS = "received"
COUNTRY_PLACEHOLDER = "Select..."

PLAN_NAMES = ("Elevate", "Grow Plus", "Grow", "Free")
PLAN_GROUPS = ("Annual plan", "Pay as you go")
PLAN_SUBTITLES = ("Enterprise-scale AI Search", "Keyword search with AI",
                  "Keyword search", "Search and recommendations")
PLAN_ACTIONS = ("Start for free", "Build for free", "Request pricing")
GRID_CATEGORIES = ("Search", "Analytics", "UI Components",
                   "Integrations & Data", "Crawler",
                   "Infrastructure & Plan Limits", "Support & Success")
GRID_ROWS = ("Rules", "Visual Editor", "Manual Synonyms",
             "Virtual Replicas (Relevant Sort)", "AI Synonyms",
             "Query Categorization")
GRID_LIMITS = ("10 per index", "10,000 per index")
GROW_METERING = ("10K search requests /month included then $0.50 per "
                 "additional 1K search requests")
GROW_RECORDS = "100K records included then $0.40"
FREE_BODY = ("Get started building experiences ever with some of our "
             "features.")
FREE_NOTE = "No credit card required."
UNIT_PRICE_MINOR = 50
RECORD_PRICE_MINOR = 40
CURRENCY = "usd"

SEARCH_PLACEHOLDER = "Search or Ask AI"
STORY_PLACEHOLDER = "Search for a customer story"
ROTATING_PROMPT = "How can I help you?"
FILTER_HEADING = "Filter by source"
RESULTS_HEADING = "Products & Resources"
HIT_ACTION = "Learn more →"
LOAD_MORE = "Show more results"
SUGGESTIONS_HEADING = "Suggestions"
SUGGESTION_BUTTONS = ("Kestrel API integration", "Kestrel search benefits",
                      "Kestrel scalability", "AI search for ecommerce")
SUGGESTED_QUESTIONS = (
    "How will Kestrel improve our search experience and conversions?",
    "How do I integrate Kestrel search into my app?",
    "Can Kestrel help shoppers find products faster and increase sales?",
    "Will Kestrel scale with our traffic and data size?",
)
AI_MODE = "AI mode"
ASSIST_TITLE = "Kestrel Assist"
ASSIST_ACTIONS = ("New chat", "Back to results")
ASSIST_ATTRIBUTION = "AI powered by Kestrel"
CLEAR_FILTERS = "Clear All Filters"
SHOW_ALL = "Show All"

HEADER_MENU = ("Products", "Solutions", "Pricing", "Developers", "Resources")
HEADER_SECONDARY = "Fix your search"
HEADER_PRIMARY = "Get started"
UTILITY_ITEMS = ("Company", "Partners", "Support")
LANGUAGES = ("English", "German", "French", "Brazilian Portuguese", "Spanish",
             "Italian")
DRAWER_HEADING = "Quick Access"
DRAWER_CLOSE = "Close"
FOOTER_LINKS = ("Careers", "Contact Us", "About Kestrel",
                "Anti-Modern Slavery Statement")
FOOTER_SOCIAL_HEADING = "Social networks"
FOOTER_NEWSLETTER = ("Get the latest in AI search - straight to your inbox.")
FOOTER_LEGAL = ("Cookie settings", "Trust Center", "Privacy Policy",
                "Terms of service")
PROMO_SLIDES = (
    ("Join us:", "Kestrel BuildCon 2026: Oct 1, 2026 - VIRTUAL", "Register Now"),
    ("UPDATE:", "Unlock the power of agentic AI with Agent Forge",
     "See what's new"),
)

HERO_LINES = ("Agentic.", "Generative.", "Search")
HERO_LEAD = "One AI retrieval platform to power them all"
HERO_BUTTON = "Explore the platform"
USE_CASES_HEADING = "Powering AI retrieval across use cases"
ACCORDION_ITEMS = ("AI mode search bar", "Generative AI", "Agentic commerce",
                   "Merchandising")
CAPABILITY_BUTTON = "See more capabilities"
ANALYST_HEADING = "A leader for the third consecutive year"
SOLUTIONS_HEADING = "Solutions that fulfill your business goals"
SOLUTION_TITLES = ("Quickly surface the right content", "Understand user intent",
                   "Confidently launch agentic experiences",
                   "Personalize for more engagement", "Create buying urgency")
CUSTOMERS_HEADING = "See customer success in action"
CUSTOMERS_BUTTON = "View all customer stories"
CLOSING_HEADING = "Harness the power of goal driven AI search with Kestrel"
CLOSING_BUTTONS = ("Get Started", "Get a demo")
WORDMARKS = ("Northmoor", "Culture Yard", "Halcyon Sport", "Fern & Co",
             "Petsmith", "Shoe Carousel", "Club Meridian", "DocMarket",
             "Givewell Schools", "Brightwell Group")

PRICING_HEADING = "Scalable pricing for smarter search"
PRICING_CHOOSER = "Help me choose a plan"
GRID_HEADING = "Detailed feature comparison"
GRID_JUMP = "See full features grid"
FAQ_HEADING = "Pricing FAQs"
FAQ_FIRST = "What is a search request?"

PRODUCTS_EYEBROW = "AI PRODUCT OVERVIEW"
PRODUCTS_SECTION = "Make every interaction smarter with AI retrieval"
BLOCK_TERMS = ("Hybrid Search", "AI Ranking", "Query Categorization",
               "Advanced Personalization")
BLOCK_BUTTON = "Learn more about AI Search"
VIDEO_BUTTON = "Book a live demo with our product experts"
TOOLS_HEADING = "Tools for business users"

DEMO_HEADING = "Fix your search experience"
STAT_ONE = "18,000+"
STAT_ONE_LABEL = "global brands served"
STAT_TWO = "9.3 Billion"
STAT_TWO_LABEL = "Single-day searches"
TRUST_ROW_ONE = "Trusted by 18,000+ businesses"
TRUST_ROW_TWO = "Enterprise-grade security & data privacy"
BADGES = ("CCPA", "BSI C5", "SOC 2 Type II", "ISO 27001", "GDPR")

NOT_FOUND_NUMERAL = "404"
NOT_FOUND_HEADING = "Page not found"
NOT_FOUND_SEARCH = "Search Kestrel"
NOT_FOUND_LINKS = ("API Status", "Home page", "Support")

TYPE_FAMILIES = ("Sora", "Inter")
CONTRAST_BODY_RATIO = 4.5
CONTRAST_LARGE_RATIO = 3.0
TOUCH_TARGET_PX = 44

PUBLIC_ROUTES = ("/", "/pricing", "/products", "/customers", "/privacy")
CHROME_ROUTES = ("/", "/pricing", "/products", "/customers")
BARE_ROUTES = ("/demorequest",)
NARROW_VIEWPORT = {"width": 390, "height": 844}
WIDE_VIEWPORT = {"width": 1440, "height": 900}
IDEMPOTENCY_HEADER = "Idempotency-Key"
MIN_TASK_HEADER = "X-Min-Task"
API_KEY_HEADER = "X-Kestrel-Api-Key"
SETTLE_SECONDS = 0.5
SETTLE_ATTEMPTS = 40


def settle(seconds: float = SETTLE_SECONDS) -> None:
    time.sleep(seconds)


def poll(predicate, attempts: int = SETTLE_ATTEMPTS):
    last = None
    for _ in range(attempts):
        last = predicate()
        if last:
            return last
        settle()
    return last


def probe_email() -> str:
    return f"probe-{uuid.uuid4().hex[:10]}@example.com"


def probe_token() -> str:
    return f"probe-{uuid.uuid4().hex[:12]}"


def anchor(label: str, response: httpx.Response) -> str:
    body = response.text[:400] if response.text else ""
    return (f"{label}: {response.request.method} {response.request.url} "
            f"answered {response.status_code} with body {body!r}")


@pytest.fixture(scope="session")
def api_base() -> str:
    return API


@pytest.fixture(scope="session")
def app_url() -> str:
    return APP_URL


@pytest.fixture()
def client():
    with httpx.Client(base_url=API, timeout=30.0, follow_redirects=False) as c:
        yield c


@pytest.fixture()
def site():
    with httpx.Client(base_url=APP_URL, timeout=30.0, follow_redirects=True) as c:
        yield c


def sign_in(client: httpx.Client, email: str, password: str = CORPUS_PASSWORD) -> str:
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code in (200, 201), anchor(f"sign in for {email}", r)
    token = r.json().get("token")
    assert token, anchor(f"sign in for {email} returned no token", r)
    return token


def bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def api_key(value: str) -> dict:
    return {API_KEY_HEADER: value}


@pytest.fixture()
def owner_token(client) -> str:
    return sign_in(client, OWNER_EMAIL)


@pytest.fixture()
def admin_token(client) -> str:
    return sign_in(client, ADMIN_EMAIL)


@pytest.fixture()
def operator_token(client) -> str:
    return sign_in(client, OPERATOR_EMAIL)


@pytest.fixture()
def analyst_token(client) -> str:
    return sign_in(client, ANALYST_EMAIL)


@pytest.fixture()
def second_owner_token(client) -> str:
    return sign_in(client, SECOND_OWNER_EMAIL)


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as driver:
        engine = driver.chromium.launch()
        yield engine
        engine.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context(viewport=WIDE_VIEWPORT)
    sheet = context.new_page()
    yield sheet
    context.close()


@pytest.fixture(scope="session")
def db():
    return make_backend()


def search(client: httpx.Client, index: str, key: str = SITE_SEARCH_KEY,
           **params) -> httpx.Response:
    return client.post(f"/1/indexes/{index}/query", json=params,
                       headers=api_key(key))


def object_ids(payload: dict) -> list:
    return [hit.get("objectID") for hit in payload.get("hits", [])]


def facet_counts(payload: dict, attribute: str) -> dict:
    return dict(payload.get("facets", {}).get(attribute, {}))


def demo_payload(**overrides) -> dict:
    body = {"firstName": "Amelia", "lastName": "Ortega",
            "email": probe_email(), "phone": "+1 415 555 0134",
            "company": f"Probe Labs {uuid.uuid4().hex[:6]}",
            "country": "United States"}
    body.update(overrides)
    return body
