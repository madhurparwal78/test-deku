from __future__ import annotations

import os
import time
import uuid

import httpx
import pytest

import appclient
import capabilities

SEED_PASSWORD = appclient.seeded_password("DEKU_SEED_PASSWORD", "deku-demo-pw-2026")

MEMBER_EMAIL = "member@example.com"
MEMBER2_EMAIL = "member2@example.com"
SUBSCRIBER_EMAIL = "subscriber@example.com"

MEMBER_USERNAME = "nadia_roux"
MEMBER2_USERNAME = "tomas_iversen"
SUBSCRIBER_USERNAME = "priya_shah"

CATALOGUE_TOTAL = 240
PAGE_SIZE = 50
TOPIC_TAG_COUNT = 47

DAILY_PROBLEM_TITLE = "3568. Minimum Moves to Clean the Classroom"
SEEDED_ROWS = {
    "1. Two Sum": ("58.1%", "Easy"),
    "2. Add Two Numbers": ("49.2%", "Med."),
    "4. Median of Two Sorted Arrays": ("47.5%", "Hard"),
    "37. Sudoku Solver": ("65.6%", "Hard"),
    "8. String to Integer (atoi)": ("21.7%", "Med."),
}

VERDICTS = (
    "Accepted",
    "Wrong Answer",
    "Time Limit Exceeded",
    "Memory Limit Exceeded",
    "Runtime Error",
    "Compile Error",
    "Output Limit Exceeded",
    "Internal Error",
    "Rejected",
)
SUBMISSION_STATES = ("pending", "judging", "done")
STATUS_VALUES = ("all", "unsolved", "solved", "attempted")
OVERLAY_VALUES = ("solved", "attempted", "unsolved")
DIFFICULTY_FILTER_WORDS = ("Easy", "Medium", "Hard")
DIFFICULTY_ROW_WORDS = ("Easy", "Med.", "Hard")
CATEGORIES = ("algorithms", "database", "shell", "concurrency", "javascript", "pandas")
CATEGORY_PILLS = (
    "All Topics",
    "Algorithms",
    "Database",
    "Shell",
    "Concurrency",
    "JavaScript",
    "Pandas",
)
LANGUAGES = ("python3", "javascript")

SOURCE_CAP_BYTES = 65536
OUTPUT_LIMIT_BYTES = 65536
REVEAL_TRUNCATION = 1000
DUPLICATE_WINDOW_SECONDS = 10
BASE_TIME_LIMIT_MS = 2000
BASE_MEMORY_LIMIT_KB = 262144
MULTIPLIERS = {"javascript": "2.0", "python3": "3.0"}
CONTEST_PENALTY_SECONDS = 300
VERDICT_DEADLINE_SECONDS = 120
INTAKE_BUDGET_SECONDS = 15.0

PRICE_MONTHLY_MINOR = 3500
PRICE_YEARLY_MINOR = 15900
PRICE_YEARLY_LIST_MINOR = 42000
PRICE_YEARLY_PER_MONTH_MINOR = 1325
PRICE_REGION = "US"
PRICE_CURRENCY = "usd"

FINISHED_CONTEST = "weekly-contest-431"
SCHEDULED_CONTEST = "weekly-contest-432"
RUNNING_CONTEST = "biweekly-contest-150"
RUNNING_CONTEST_SCORES = {
    "two-sum": 3,
    "add-two-numbers": 4,
    "median-of-two-sorted-arrays": 5,
    "sudoku-solver": 6,
}
STUDY_PLAN_NAMES = ("Bytefold 75", "Top Interview 150", "SQL 50", "Introduction to Pandas")
STUDY_PLAN_GROUPS = ("Cracking Coding Interview", "Advanced Algorithms", "Most Liked")
STUDY_PLAN_SUBTITLES = ("Crack SQL Interview in 50 Qs", "Learn Basic Pandas in 15 Qs")
FEATURED_PLAN_SLUG = "bytefold-75"
PREMIUM_PLAN_SLUG = "top-interview-150"
EXPLORE_CARD_SLUGS = ("crash-course", "beginners-guide", "cheatsheet")
SEEDED_POST_MINIMUM = 3
DISCUSSION_ORDERS = ("Best", "Hot", "Newest", "Most Votes")
EU_REGION = "EU"
EU_CURRENCY = "eur"
EU_MONTHLY_MINOR = 3200
EU_YEARLY_MINOR = 14900
PRICE_DISPLAY = ("$35.00", "$159.00", "$420.00", "62%", "$13.25", "Most Popular")
LOCKOUT_ATTEMPTS = 5
PASSWORD_MINIMUM = 8
PASSWORD_MAXIMUM_FLOOR = 128
CUSTOM_CASE_CAP = 10
COMPARATORS = ("exact", "numeric-tolerance", "unordered", "unordered-deep", "any-of")
MEDIAN_TOLERANCE = 1e-5
MEMBER_STATES = ("unverified", "active", "restricted", "locked", "deleted")
FAILURE_TYPES = (
    "invalid_data",
    "not_found",
    "not_allowed",
    "unauthorized",
    "conflict",
    "payment_required",
    "unexpected_state",
    "rate_limited",
    "judge_unavailable",
)
COIN_REASONS = ("daily", "streak_milestone", "contest", "redemption", "purchase", "adjustment", "refund")
SEEDED_ACCEPTANCE = {
    2: ("Add Two Numbers", "49.2%", "Med."),
    3: ("Longest Substring Without Repeating Characters", "39.9%", "Med."),
    4: ("Median of Two Sorted Arrays", "47.5%", "Hard"),
    8: ("String to Integer (atoi)", "21.7%", "Med."),
    37: ("Sudoku Solver", "65.6%", "Hard"),
    42: ("Trapping Rain Water", "68.1%", "Hard"),
    51: ("N-Queens", "76.4%", "Hard"),
    3568: ("Minimum Moves to Clean the Classroom", "47.4%", "Med."),
}
TOPIC_TAG_NAMES = (
    "Array", "String", "Hash Table", "Math", "Dynamic Programming", "Sorting", "Greedy",
    "Depth-First Search", "Binary Search", "Database", "Bit Manipulation", "Matrix",
    "Prefix Sum", "Tree", "Two Pointers", "Breadth-First Search", "Heap (Priority Queue)",
    "Simulation", "Counting", "Graph Theory", "Binary Tree", "Stack", "Sliding Window",
    "Enumeration", "Design", "Backtracking", "Number Theory", "Union-Find", "Segment Tree",
    "Linked List", "Ordered Set", "Monotonic Stack", "Divide and Conquer", "Combinatorics",
    "Trie", "Queue", "Bitmask", "Recursion", "Binary Indexed Tree", "Geometry",
    "Hash Function", "Memoization", "Binary Search Tree", "Shortest Path",
    "Topological Sort", "String Matching", "Rolling Hash",
)
FOOTER_ROUTES = ("/privacy/", "/terms/", "/help/", "/bug-bounty/", "/download/")
INTERVIEW_ROUTES = ("/interview/online-interview/", "/interview/assessment/")
MEMBER_ONLY_ROUTES = ("/list/", "/quest/", "/playground/", "/store/", "/store/redeem/")
NARROW_VIEWPORT = {"width": 375, "height": 812}
WIDE_VIEWPORT = {"width": 1920, "height": 1200}

PUBLIC_ROUTES = (
    "/",
    "/problemset/",
    "/contest/",
    "/explore/",
    "/discuss/",
    "/studyplan/",
    "/subscribe/",
    "/accounts/login/",
    "/accounts/signup/",
)
FOOTER_LABELS = ("Help Center", "Bug Bounty", "Terms", "Privacy Policy")
RAIL_LABELS = ("Library", "Quest", "Explore", "Study Plan")

NON_TERMINATING_SOURCE = "def {entry}(nums, target):\n    while True:\n        pass\n"
SIGNAL_IGNORING_SOURCE = (
    "import signal\n"
    "def {entry}(nums, target):\n"
    "    for name in ('SIGALRM', 'SIGTERM', 'SIGINT', 'SIGXCPU', 'SIGVTALRM', 'SIGPROF'):\n"
    "        number = getattr(signal, name, None)\n"
    "        if number is not None:\n"
    "            try:\n"
    "                signal.signal(number, signal.SIG_IGN)\n"
    "            except Exception:\n"
    "                pass\n"
    "    while True:\n"
    "        pass\n"
)
SLEEPING_SOURCE = "import time\ndef {entry}(nums, target):\n    time.sleep(30)\n    return []\n"
UNBOUNDED_ALLOCATION_SOURCE = (
    "def {entry}(nums, target):\n"
    "    blob = []\n"
    "    while True:\n"
    "        blob.append(bytearray(1048576))\n"
)
SILENT_SOURCE = "def {entry}(nums, target):\n    return None\n"
WRONG_SOURCE = "def {entry}(nums, target):\n    return [-987654321, -987654321]\n"
SYNTAX_ERROR_SOURCE = "def {entry}(nums, target):\n    return [\n"
RUNTIME_ERROR_SOURCE = (
    "import sys\n"
    "def {entry}(nums, target):\n"
    "    sys.stderr.write('bytefold-stderr-marker ' + 'e' * 9000 + chr(10))\n"
    "    raise ValueError('bytefold-runtime-marker')\n"
)
OVERSIZED_OUTPUT_SOURCE = "def {entry}(nums, target):\n    return list(range(200000))\n"
STDERR_CAP_BYTES = 4096


def settle(seconds: float = 0.5) -> None:
    """The only sanctioned pause. Async side effects are polled, never slept on."""
    time.sleep(seconds)


def probe_token() -> str:
    """A per-run identifier, so two identical runs never collide on a record."""
    return os.urandom(6).hex()


def probe_email() -> str:
    return f"probe-{probe_token()}@example.com"


def idempotency_key() -> str:
    return str(uuid.uuid4())


@pytest.fixture(scope="session")
def base_url() -> str:
    return appclient.app_url()


@pytest.fixture(scope="session")
def api() -> str:
    return appclient.api_base()


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def member_token() -> str:
    return appclient.login(MEMBER_EMAIL, SEED_PASSWORD)


@pytest.fixture(scope="session")
def member2_token() -> str:
    return appclient.login(MEMBER2_EMAIL, SEED_PASSWORD)


@pytest.fixture(scope="session")
def subscriber_token() -> str:
    return appclient.login(SUBSCRIBER_EMAIL, SEED_PASSWORD)


@pytest.fixture
def member(member_token: str):
    with appclient.client(member_token) as session:
        yield session


@pytest.fixture
def member2(member2_token: str):
    with appclient.client(member2_token) as session:
        yield session


@pytest.fixture
def subscriber(subscriber_token: str):
    with appclient.client(subscriber_token) as session:
        yield session


@pytest.fixture
def anon():
    with appclient.client(None) as session:
        yield session


@pytest.fixture
def page():
    with httpx.Client(base_url=appclient.app_url(), timeout=appclient.TIMEOUT,
                      follow_redirects=True) as session:
        yield session


def describe(response: httpx.Response) -> str:
    """The failure-message tail: what was asked, what came back, and a body excerpt."""
    return (
        f"{response.request.method} {response.request.url} -> "
        f"{response.status_code}: {response.text[:400]}"
    )


def rows_of(payload):
    """The catalogue list, whichever shape the app chose to wrap it in."""
    if isinstance(payload, list):
        return payload
    assert isinstance(payload, dict), f"catalogue payload is neither a list nor an object: {payload!r}"
    for key in ("rows", "results", "items", "data", "problems"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    raise AssertionError(f"catalogue payload carries no row list: {sorted(payload)[:12]}")


def cursor_of(payload):
    if not isinstance(payload, dict):
        return None
    for key in ("next_cursor", "next", "cursor", "after"):
        if key in payload:
            return payload[key]
    return None


def field(record: dict, *names, required: bool = True):
    for name in names:
        if name in record:
            return record[name]
    if required:
        raise AssertionError(
            f"record carries none of {names!r}; it has {sorted(record)[:12]}"
        )
    return None


def catalogue(session: httpx.Client, **params):
    response = session.get("/problems", params=params)
    assert response.status_code == 200, f"catalogue query failed. {describe(response)}"
    return response.json()


def facets(session: httpx.Client, **params):
    response = session.get("/problems/facets", params=params)
    assert response.status_code == 200, f"facet query failed. {describe(response)}"
    return response.json()


def facet_count(payload, axis: str, value: str):
    axes = payload if isinstance(payload, dict) else {}
    entries = axes.get(axis)
    assert isinstance(entries, list), (
        f"facet payload has no list for axis {axis!r}; it has {sorted(axes)[:12]}"
    )
    wanted = "".join(ch if ch.isalnum() else "-" for ch in value.lower()).strip("-")
    for entry in entries:
        name = str(field(entry, "value", "name", "slug")).lower()
        if "".join(ch if ch.isalnum() else "-" for ch in name).strip("-") == wanted:
            return int(field(entry, "count", "total"))
    raise AssertionError(f"facet axis {axis!r} carries no value {value!r}")


def a_problem_slug(session: httpx.Client, **params) -> str:
    payload = catalogue(session, limit=PAGE_SIZE, **params)
    rows = rows_of(payload)
    assert rows, f"catalogue returned no rows for {params!r}"
    return str(field(rows[0], "slug"))


def submit(session: httpx.Client, slug: str, language: str, source: str,
           key: str | None = None):
    headers = {"Idempotency-Key": key or idempotency_key()}
    return session.post(
        "/submissions",
        json={"problem_slug": slug, "language": language, "source": source,
              "context": "practice"},
        headers=headers,
    )


def await_verdict(session: httpx.Client, submission_id: str,
                  deadline: float = VERDICT_DEADLINE_SECONDS) -> dict:
    """Bounded polling. The brief pins a client wait ceiling; this honours it."""
    waited = 0.0
    interval = 1.0
    last = {}
    while waited <= deadline:
        response = session.get(f"/submissions/{submission_id}")
        assert response.status_code == 200, (
            f"submission {submission_id} could not be read back. {describe(response)}"
        )
        last = response.json()
        if str(field(last, "state")) == "done":
            return last
        settle(interval)
        waited += interval
        interval = min(interval * 1.5, 8.0)
    raise AssertionError(
        f"submission {submission_id} never reached state 'done' within {deadline}s; "
        f"last read was {last!r}"
    )


def judge(session: httpx.Client, slug: str, language: str, source: str) -> dict:
    response = submit(session, slug, language, source)
    assert response.status_code in (200, 201, 202), (
        f"submission intake refused a valid submission. {describe(response)}"
    )
    body = response.json()
    return await_verdict(session, str(field(body, "submission_id", "id")))


TWO_SUM_SLUG_CANDIDATES = ("two-sum",)

_TWO_SUM_PYTHON = (
    "def {entry}(nums, target):\n"
    "    seen = {{}}\n"
    "    for index, value in enumerate(nums):\n"
    "        want = target - value\n"
    "        if want in seen:\n"
    "            return [seen[want], index]\n"
    "        seen[value] = index\n"
    "    return []\n"
)

_TWO_SUM_JAVASCRIPT = (
    "function {entry}(nums, target) {{\n"
    "  const seen = new Map();\n"
    "  for (let index = 0; index < nums.length; index += 1) {{\n"
    "    const want = target - nums[index];\n"
    "    if (seen.has(want)) return [seen.get(want), index];\n"
    "    seen.set(nums[index], index);\n"
    "  }}\n"
    "  return [];\n"
    "}}\n"
)

_TWO_SUM_BODY = {"python3": _TWO_SUM_PYTHON, "javascript": _TWO_SUM_JAVASCRIPT}


def signature(session: httpx.Client, slug: str, language: str) -> dict:
    response = session.get(f"/problems/{slug}/signature", params={"language": language})
    assert response.status_code == 200, (
        f"signature for {slug} in {language} is unreadable. {describe(response)}"
    )
    return response.json()


def two_sum_slug(session: httpx.Client) -> str:
    """The brief pins `1. Two Sum` with a fixed parameter shape, which is what lets this
    layer submit a real solution rather than an invented one."""
    payload = catalogue(session, search="1", limit=PAGE_SIZE)
    for row in rows_of(payload):
        if str(field(row, "title")).strip() == "Two Sum" or str(
                field(row, "number")) == "1":
            return str(field(row, "slug"))
    raise AssertionError(
        "the seeded row `1. Two Sum` was not found by a catalogue search for its number"
    )


def accepted_source(session: httpx.Client, slug: str, language: str) -> str:
    """A real Two Sum solution, written against the entry point the app itself declares."""
    entry = str(field(signature(session, slug, language), "entry_point"))
    assert entry, f"signature for {slug} in {language} declares no entry_point"
    marker = ("# " if language == "python3" else "// ") + f"probe {probe_token()}\n"
    return marker + _TWO_SUM_BODY[language].format(entry=entry)


def problem_detail(session: httpx.Client, slug: str, **params) -> dict:
    response = session.get(f"/problems/{slug}", params=params)
    assert response.status_code == 200, f"problem {slug} is unreadable. {describe(response)}"
    return response.json()


def submission_id_of(response: httpx.Response) -> str:
    assert response.status_code in (200, 201, 202), (
        f"submission intake refused a valid submission. {describe(response)}"
    )
    return str(field(response.json(), "submission_id", "id"))


def submit_in(session: httpx.Client, slug: str, language: str, source: str, context: str):
    return session.post(
        "/submissions",
        json={"problem_slug": slug, "language": language, "source": source, "context": context},
        headers={"Idempotency-Key": idempotency_key()},
    )


def judge_in(session: httpx.Client, slug: str, language: str, source: str, context: str) -> dict:
    return await_verdict(session, submission_id_of(submit_in(session, slug, language, source, context)))


def register_probe(verified: bool = False, password: str | None = None) -> dict:
    """A fresh account per call, so a test that changes account state never touches a seed."""
    email = probe_email()
    username = f"probe{probe_token()}"
    secret = password or SEED_PASSWORD
    with appclient.client(None) as anon_session:
        created = anon_session.post("/auth/register",
                                    json={"email": email, "username": username,
                                          "password": secret})
    assert created.status_code in (200, 201), f"a probe account was refused. {describe(created)}"
    token = appclient.login(email, secret)
    if verified:
        with appclient.client(token) as session:
            done = session.post("/auth/verify")
            assert done.status_code in (200, 201), (
                f"in-product verification was refused for a fresh account. {describe(done)}"
            )
    return {"email": email, "username": username, "password": secret, "token": token}


def drain(sessions, slug: str, deadline: float = 180.0) -> None:
    """Wait until none of these members has a submission for `slug` still in flight."""
    waited = 0.0
    while waited <= deadline:
        busy = False
        for session in sessions:
            response = session.get("/submissions", params={"problem": slug, "limit": PAGE_SIZE})
            assert response.status_code == 200, f"the submission list is unreadable. {describe(response)}"
            for row in rows_of(response.json()):
                if str(field(row, "state")) in ("pending", "judging"):
                    busy = True
        if not busy:
            return
        settle(2.0)
        waited += 2.0
    raise AssertionError(f"submissions for {slug} were still in flight after {deadline}s")


def counters(session: httpx.Client, slug: str) -> tuple[int, int]:
    detail = problem_detail(session, slug)
    return int(field(detail, "submission_count")), int(field(detail, "accepted_count"))


def utc_today(backend) -> str:
    """Today's date in UTC, read from the database clock rather than the verifier's."""
    return str(backend.query("SELECT (now() AT TIME ZONE 'utc')::date AS d")[0]["d"])


def seconds_to_utc_midnight(backend) -> float:
    row = backend.query(
        "SELECT EXTRACT(EPOCH FROM (date_trunc('day', now() AT TIME ZONE 'utc') "
        "+ interval '1 day' - (now() AT TIME ZONE 'utc'))) AS s"
    )[0]
    return float(row["s"])


def member_id_for(backend, email: str):
    rows = backend.query("SELECT id FROM members WHERE email = %s", (email,))
    assert len(rows) == 1, f"members holds {len(rows)} rows for {email}"
    return rows[0]["id"]


def problem_id_for(backend, slug: str):
    rows = backend.query("SELECT id FROM problems WHERE slug = %s", (slug,))
    assert len(rows) == 1, f"problems holds {len(rows)} rows for {slug}"
    return rows[0]["id"]


def columns_of(backend, table: str) -> set:
    rows = backend.query(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_schema = current_schema() AND table_name = %s",
        (table,),
    )
    return {str(r["column_name"]) for r in rows}


def distinct_values(backend, table: str, column: str) -> set:
    rows = backend.query(f'SELECT DISTINCT "{column}" AS v FROM {table}')
    return {r["v"] for r in rows if r["v"] is not None}


def first_post_id(session: httpx.Client) -> str:
    response = session.get("/posts", params={"limit": PAGE_SIZE})
    assert response.status_code == 200, f"the discussion feed is unreadable. {describe(response)}"
    posts = rows_of(response.json())
    assert posts, f"the discussion feed carries no post. {describe(response)}"
    return str(field(posts[0], "id"))


def entry_point(session: httpx.Client, slug: str, language: str = "python3") -> str:
    entry = str(field(signature(session, slug, language), "entry_point"))
    assert entry, f"signature for {slug} in {language} declares no entry_point"
    return entry


def premium_slug(session: httpx.Client) -> str:
    cursor = None
    for _ in range(10):
        query = {"limit": PAGE_SIZE}
        if cursor:
            query["after"] = cursor
        payload = catalogue(session, **query)
        for row in rows_of(payload):
            if field(row, "is_premium", required=False):
                return str(field(row, "slug"))
        cursor = cursor_of(payload)
        if not cursor:
            break
    raise AssertionError("the catalogue carries no premium row")


def save_draft(session: httpx.Client, slug: str, language: str, body: str) -> httpx.Response:
    """Write a draft against the version last read, as the editor does."""
    current = session.get(f"/drafts/{slug}", params={"language": language})
    version = int(field(current.json(), "version")) if current.status_code == 200 else 0
    return session.put(f"/drafts/{slug}", json={"language": language, "body": body, "version": version})


def two_sum_with(session: httpx.Client, slug: str, preamble: str, guard: str) -> str:
    """A correct Two Sum whose answer is spoiled whenever `guard` evaluates true."""
    entry = entry_point(session, slug)
    return (
        preamble
        + f"def {entry}(nums, target):\n"
        + f"    if {guard}:\n"
        + "        return [-1, -1]\n"
        + "    seen = {}\n"
        + "    for index, value in enumerate(nums):\n"
        + "        want = target - value\n"
        + "        if want in seen:\n"
        + "            return [seen[want], index]\n"
        + "        seen[value] = index\n"
        + "    return []\n"
    )


def program(session: httpx.Client, slug: str, template: str, language: str = "python3") -> str:
    """A deliberate program shape, written against the entry point the app declares."""
    return template.format(entry=entry_point(session, slug, language))


def median_source(entry: str, offset: str) -> str:
    return (
        f"def {entry}(nums1, nums2):\n"
        "    merged = sorted(list(nums1) + list(nums2))\n"
        "    size = len(merged)\n"
        "    middle = size // 2\n"
        "    if size % 2:\n"
        f"        return float(merged[middle]) + {offset}\n"
        f"    return (merged[middle - 1] + merged[middle]) / 2.0 + {offset}\n"
    )


def permutations_source(entry: str, repeat_one: bool) -> str:
    extra = "    orderings.append(list(orderings[0]))\n" if repeat_one else ""
    return (
        "import itertools\n"
        f"def {entry}(nums):\n"
        "    orderings = [list(p) for p in itertools.permutations(nums)]\n"
        "    orderings.reverse()\n"
        + extra
        + "    return orderings\n"
    )


def stylesheet_texts(page_session: httpx.Client, html: str) -> list[str]:
    import re as _re
    texts = _re.findall(r"<style[^>]*>(.*?)</style>", html, _re.I | _re.S)
    for href in _re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"', html, _re.I):
        response = page_session.get(href)
        if response.status_code == 200:
            texts.append(response.text)
    return texts


@pytest.fixture(scope="session")
def chromium():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as driver:
        browser = driver.chromium.launch(headless=True)
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def browser_page(chromium):
    context = chromium.new_context(viewport=WIDE_VIEWPORT)
    tab = context.new_page()
    tab.set_default_timeout(30000)
    try:
        yield tab
    finally:
        context.close()


def open_route(tab, route: str) -> None:
    tab.goto(appclient.app_url() + route, wait_until="load")
    settle(0.5)
