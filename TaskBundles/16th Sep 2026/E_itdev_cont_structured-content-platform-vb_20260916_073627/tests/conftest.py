"""Task fixtures for deku/structured-content-platform-vb.

Implementation-agnostic (reference/J J.2): assume only the App Contract, the
literals pinned in instruction.md, and the two capability fixtures the declared
`backend` and `storage` slots earn. Observations are made over the JSON API,
over the served markup of the public routes, over the rows in postgres and over
the objects in the bucket. Nothing here imports a provider SDK, reads the
agent's source, or probes for a feature at run time. No test function lives in
this file.
"""

from __future__ import annotations

import io
import os
import re
import struct
import time
import zlib
from concurrent.futures import ThreadPoolExecutor

import httpx
import pytest
from appclient import app_url, client
from capabilities import Backend, ObjectStore, make_backend, make_store

SETTLE_SECONDS = 2.0
TIMEOUT = 30.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give a side effect time to land before asserting on it."""
    time.sleep(seconds)


PASSWORD = "deku-demo-pw-2026"

ADMIN_EMAIL = "admin@example.com"
EDITOR_EMAIL = "editor@example.com"
EDITOR2_EMAIL = "editor2@example.com"
CONTRIBUTOR_EMAIL = "contributor@example.com"
VIEWER_EMAIL = "viewer@example.com"

SEEDED_ACCOUNTS = (ADMIN_EMAIL, EDITOR_EMAIL, EDITOR2_EMAIL,
                   CONTRIBUTOR_EMAIL, VIEWER_EMAIL)

ADMIN_NAME = "Ines Haugen"
EDITOR_NAME = "Marit Solberg"
EDITOR2_NAME = "Tomas Lindqvist"
CONTRIBUTOR_NAME = "Priya Raman"
VIEWER_NAME = "Georg Almeida"

ROLE_ADMIN = "administrator"
ROLE_EDITOR = "editor"
ROLE_CONTRIBUTOR = "contributor"
ROLE_VIEWER = "viewer"
ROLES = (ROLE_ADMIN, ROLE_EDITOR, ROLE_CONTRIBUTOR, ROLE_VIEWER)

DEPARTMENT_ENGINEERING = "engineering"
DEPARTMENT_MARKETING = "marketing"
DEPARTMENTS = (DEPARTMENT_ENGINEERING, DEPARTMENT_MARKETING)

DATASET_PRODUCTION = "production"
DATASET_STAGING = "staging"
DATASETS = (DATASET_PRODUCTION, DATASET_STAGING)

VISIBILITY_PRIVATE = "private"
VISIBILITY_PUBLIC = "public"

PERSPECTIVE_PUBLISHED = "published"
PERSPECTIVE_DRAFTS = "drafts"
PERSPECTIVE_RAW = "raw"
PERSPECTIVES = (PERSPECTIVE_PUBLISHED, PERSPECTIVE_DRAFTS, PERSPECTIVE_RAW)

DRAFT_PREFIX = "drafts."

DOC_AURORA = "article-aurora-pipeline"
DOC_KEYS = "article-keys-and-arrays"
DOC_MIGRATING = "article-migrating-schemas"
DOC_RETIRED = "article-retired-notes"
DOC_QUARTERLY = "article-quarterly-letter"
DOC_EDITORIAL = "article-editorial-standards"
DOC_AUTHOR_MARIT = "author-marit"
DOC_AUTHOR_TOMAS = "author-tomas"

ENGINEERING_DOCS = (DOC_AURORA, DOC_KEYS, DOC_MIGRATING, DOC_RETIRED,
                    DOC_EDITORIAL, DOC_AUTHOR_MARIT)
MARKETING_DOCS = (DOC_QUARTERLY, DOC_AUTHOR_TOMAS)

TYPE_ARTICLE = "article"
TYPE_AUTHOR = "author"

STATE_NOT_PUBLISHED = "Not published"
STATE_PUBLISHED = "Published"
STATE_PUBLISHED_WITH_EDITS = "Published with unpublished edits"
STATE_DRAFT = "Draft"
PUBLICATION_STATES = (STATE_NOT_PUBLISHED, STATE_PUBLISHED,
                      STATE_PUBLISHED_WITH_EDITS, STATE_DRAFT)

ASSET_SEEDED = "image-9f2ae1c4d0b7-1600x900-png"
ASSET_OBJECT_KEY = "assets/production/9f2ae1c4d0b7.png"
ASSET_PREFIX = "assets/"
DERIVED_PREFIX = "derived/"
ALT_AURORA = "A layered diagram of a content pipeline"
ALT_QUARTERLY = "The quarterly figures, drawn as a bar chart"

MUTATION_CREATE = "create"
MUTATION_CREATE_OR_REPLACE = "createOrReplace"
MUTATION_CREATE_IF_NOT_EXISTS = "createIfNotExists"
MUTATION_PATCH = "patch"
MUTATION_DELETE = "delete"

FIELD_ID = "_id"
FIELD_TYPE = "_type"
FIELD_REV = "_rev"
FIELD_CREATED = "_createdAt"
FIELD_UPDATED = "_updatedAt"
RESERVED_FIELDS = (FIELD_ID, FIELD_TYPE, FIELD_REV, FIELD_CREATED, FIELD_UPDATED)
SERVICE_ASSIGNED = (FIELD_REV, FIELD_CREATED, FIELD_UPDATED)

MARK_STRONG = "strong"
MARK_EM = "em"

CODE_GRANT_ESCAPE = "grant_escape_refused"
CODE_REVISION_MISMATCH = "revision_mismatch"
CODE_PUBLISH_DEPENDENCIES = "publish_dependencies_unpublished"
CODE_DELETE_BLOCKED = "delete_blocked_by_references"
CODE_UNCONFIRMED = "mutation_by_query_unconfirmed"
CODE_UNFILTERED = "unfiltered_mutation_refused"
CODE_QUERY_BOUND = "query_bound_exceeded"
CODE_PREVIEW_EXPIRED = "preview_grant_expired"
CODE_BROWSER_WRITE_TOKEN = "browser_write_token_refused"
CODE_RELEASE_TOO_LARGE = "release_too_large"
CODE_ASSET_TYPE = "asset_type_refused"
CODE_PRODUCTION_CONFIRMATION = "production_confirmation_required"
CODE_PERSONAL_FIELDS = "personal_fields_undeclared"

MODE_DRY_RUN = "dry_run"
MODE_APPLY = "apply"
PHASE_EXPAND = "expand"
PHASE_MIGRATE = "migrate"
PHASE_CONTRACT = "contract"

SPLIT_WORD = "pipeline"
DEREFERENCE_DEPTH_BOUND = 5
QUERY_TEXT_BOUND = 16 * 1024
CONCURRENT_INCREMENTS = 100
PRESENCE_CURSOR_CEILING = 20
RECONNECT_CAP_SECONDS = 30
STALENESS_CEILING_SECONDS = 60
SEARCHABLE_SECONDS = 10
DATASET_RECOVERY_HOURS = 168

COPY_CONFLICT = "Someone else saved while you were editing. Your changes were kept."
COPY_DELETE_BLOCKED = "documents reference this. Remove those references first."
COPY_READ_ONLY = "Editing is paused. Your work so far is saved."
COPY_SEARCH_LAG = "Search is catching up. Your document is not lost."
COPY_DATASET_PUBLIC = "This dataset is public. Anyone can read its published content."
COPY_DRY_RUN = "Nothing has been written."
COPY_NOT_FOUND_TITLE = "Page not found"
COPY_SKIP_LINK = "Skip to content"
COPY_INSTALL_COMMAND = "npm create quarto@latest"
COPY_DEVELOPER_BAND = "Less talk, more code"
COPY_RAIL_FIRST = "01 CONTENT-AS-DATA"
COPY_RAIL_LAST = "05 POWER ANY APPLICATION"

ROUTE_HOME = "/"
ROUTE_DOCS = "/docs"
ROUTE_BLOG = "/blog"
ROUTE_PRICING = "/pricing"
ROUTE_ENTERPRISE = "/enterprise"
ROUTE_CONTACT = "/contact"
ROUTE_PRIVACY = "/privacy"
ROUTE_TERMS = "/terms"
ROUTE_COOKIES = "/cookie-settings"
ROUTE_SITEMAP = "/sitemap.xml"
ROUTE_ROBOTS = "/robots.txt"
ROUTE_SIGNIN = "/signin"
ROUTE_STUDIO = "/studio"
ROUTE_UNMATCHED = "/no-such-address-at-all"

PUBLIC_ROUTES = (ROUTE_HOME, ROUTE_DOCS, ROUTE_BLOG, ROUTE_PRICING,
                 ROUTE_ENTERPRISE, ROUTE_CONTACT, ROUTE_PRIVACY, ROUTE_TERMS,
                 ROUTE_COOKIES)

README_PATH = "/app/USER_README.md"

API_HEALTH = "/health"
API_LOGIN = "/auth/login"
API_ME = "/me"
API_DATASETS = "/datasets"
API_QUERY = "/data/query"
API_MUTATE = "/data/mutate"
API_DOC = "/data/doc"
API_HISTORY = "/data/history"
API_PUBLISH = "/data/publish"
API_UNPUBLISH = "/data/unpublish"
API_LISTEN = "/data/listen"
API_PREVIEW = "/data/preview-grants"
API_ASSETS = "/assets"
API_SEARCH = "/search"
API_PRESENCE = "/presence"
API_SCHEMA = "/project/schema"
API_PROJECT_DATASETS = "/project/datasets"
API_TOKENS = "/project/tokens"
API_GRANTS = "/project/grants"
API_WEBHOOKS = "/project/webhooks"
API_DELIVERIES = "/project/webhook-deliveries"
API_MIGRATIONS = "/project/migrations"
API_AUDIT = "/project/audit"
API_RELEASES = "/releases"
API_SCHEDULES = "/schedules"
API_LEADS = "/leads"

OK_READ = (200,)
OK_WRITE = (200, 201)
REFUSED = (400, 409, 422)
DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
NOT_FOUND = (404,)

TABLE_PERSON = "person"
TABLE_DATASET = "dataset"
TABLE_DOCUMENT = "document"
TABLE_REVISION = "revision"
TABLE_TRANSACTION = "transaction"
TABLE_REFERENCE_EDGE = "reference_edge"
TABLE_ASSET = "asset"
TABLE_GRANT = "grant"
TABLE_TOKEN = "token"
TABLE_PREVIEW_GRANT = "preview_grant"
TABLE_RELEASE = "release"
TABLE_SCHEDULE = "schedule"
TABLE_WEBHOOK = "webhook"
TABLE_WEBHOOK_DELIVERY = "webhook_delivery"
TABLE_MIGRATION_RUN = "migration_run"
TABLE_SEARCH_DOCUMENT = "search_document"
TABLE_AUDIT = "audit_entry"
TABLE_LEAD = "lead"
TABLE_CONSENT = "consent_decision"

SEEDED_TABLES = (TABLE_PERSON, TABLE_DATASET, TABLE_DOCUMENT, TABLE_REVISION,
                 TABLE_ASSET, TABLE_GRANT)

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
HREF_RE = re.compile(r"""href\s*=\s*["']([^"'#?]+)""", re.IGNORECASE)
SITEMAP_LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>", re.IGNORECASE)
ROBOTS_SITEMAP_RE = re.compile(r"(?im)^\s*sitemap\s*:\s*(\S+)\s*$")
LIST_ITEM_RE = re.compile(r"<li\b", re.IGNORECASE)
LIST_OPEN_RE = re.compile(r"<ul\b", re.IGNORECASE)


def preview_ttl_seconds() -> int:
    """The preview-grant lifetime the environment injects (reference/J J.9)."""
    raw = str(os.environ.get("PREVIEW_GRANT_TTL_SEC", "")).strip()
    value = int(raw) if raw.isdigit() else 0
    return value if value > 0 else 8


def replay_window_seconds() -> int:
    """The transaction replay window the environment injects."""
    raw = str(os.environ.get("TRANSACTION_REPLAY_WINDOW_SEC", "")).strip()
    value = int(raw) if raw.isdigit() else 0
    return value if value > 0 else 300


@pytest.fixture(scope="session")
def api():
    """The JSON API under /api, unauthenticated."""
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def site():
    """The site itself, for reading served markup."""
    with httpx.Client(base_url=app_url(), timeout=TIMEOUT,
                      follow_redirects=True) as c:
        yield c


@pytest.fixture(scope="session")
def raw_site():
    """The site without redirect following, so a redirect is observable."""
    with httpx.Client(base_url=app_url(), timeout=TIMEOUT,
                      follow_redirects=False) as c:
        yield c


class ContentStore:
    """Provider-agnostic domain queries composed from Backend primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def rows(self, table: str, **where) -> list[dict]:
        return self._b.rows(table, **where)

    def count(self, table: str, **where) -> int:
        return self._b.count(table, **where)

    def one(self, table: str, **where):
        return self._b.one(table, **where)

    def document(self, dataset: str, document_id: str):
        return self._b.one(TABLE_DOCUMENT, dataset=dataset, _id=document_id)

    def revisions_of(self, dataset: str, document_id: str) -> list[dict]:
        return self._b.rows(TABLE_REVISION, dataset=dataset,
                            document_id=document_id)

    def audit(self, **where) -> list[dict]:
        return self._b.rows(TABLE_AUDIT, **where)


@pytest.fixture(scope="session")
def store() -> ContentStore:
    return ContentStore(make_backend())


@pytest.fixture(scope="session")
def bucket() -> ObjectStore:
    return make_store()


def probe_token() -> str:
    """A per-run token no other run collides with (reference/J J.5)."""
    return os.urandom(6).hex()


def probe_id(prefix: str = "probe") -> str:
    return "%s-%s" % (prefix, probe_token())


def probe_transaction() -> str:
    return "txn-%s" % probe_token()


PROBE_DOMAIN = "deku.test"


def probe_email() -> str:
    return "probe-%s@%s" % (probe_token(), PROBE_DOMAIN)


def probe_title(prefix: str = "Probe article") -> str:
    return "%s %s" % (prefix, probe_token())


def login(api_client, email: str, password: str = PASSWORD):
    """Sign in, returning the raw response so a caller can assert on refusal."""
    return api_client.post(API_LOGIN, json={"email": email, "password": password})


def token_of(payload) -> str:
    if isinstance(payload, dict):
        for key in ("access_token", "token", "bearer", "accessToken"):
            if isinstance(payload.get(key), str) and payload[key]:
                return payload[key]
    return ""


def bearer(api_client, email: str, password: str = PASSWORD) -> dict:
    """Authorization header for a seeded account, acquired per call (J.11)."""
    response = login(api_client, email, password)
    assert response.status_code in OK_WRITE, (
        "%s refused the seeded account %r with the pinned password: status %s, "
        "body %r" % (API_LOGIN, email, response.status_code, response.text[:300]))
    value = token_of(response.json())
    assert value, (
        "%s returned no bearer token for %r: body %r"
        % (API_LOGIN, email, response.text[:300]))
    return {"Authorization": "Bearer %s" % value}


def dataset_path(base: str, dataset: str, *parts) -> str:
    tail = "/".join(str(p).strip("/") for p in parts if str(p).strip("/"))
    return "%s/%s%s" % (base, dataset, ("/" + tail) if tail else "")


def as_list(payload) -> list:
    """A list endpoint returns a top-level JSON array; tolerate nothing else."""
    return payload if isinstance(payload, list) else []


def field(row, *names):
    """First present value among tolerated field spellings."""
    for name in names:
        if isinstance(row, dict) and name in row and row[name] not in (None, ""):
            return row[name]
    return None


def body_text(response) -> str:
    return getattr(response, "text", "") or ""


def json_body(response):
    """The decoded body when the response declares JSON, else an empty map."""
    kind = str(response.headers.get("content-type", "")).lower()
    if "json" not in kind:
        return {}
    return response.json()


def error_code(response) -> str:
    """The stable machine-readable code out of the pinned error envelope."""
    payload = json_body(response)
    if isinstance(payload, dict):
        err = payload.get("error")
        if isinstance(err, dict):
            value = field(err, "code", "type")
            if value:
                return str(value)
        value = field(payload, "code", "error_code")
        if value:
            return str(value)
    return ""


def mentions(response, *needles) -> bool:
    """The response body names every needle, case-insensitively."""
    low = body_text(response).lower()
    return all(str(n).lower() in low for n in needles)


def run_query(api_client, headers: dict, dataset: str, query: str,
              params: dict | None = None, perspective: str | None = None):
    payload = {"query": query, "params": params or {}}
    if perspective:
        payload["perspective"] = perspective
    return api_client.post(dataset_path(API_QUERY, dataset), json=payload,
                           headers=headers)


def query_result(response) -> list:
    payload = json_body(response)
    if isinstance(payload, dict):
        value = payload.get("result")
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            return [value]
    return []


def query_cost(response) -> dict:
    payload = json_body(response)
    value = payload.get("cost") if isinstance(payload, dict) else None
    return value if isinstance(value, dict) else {}


def mutate(api_client, headers: dict, dataset: str, mutations: list,
           transaction_id: str | None = None, extra: dict | None = None):
    payload = {"transactionId": transaction_id or probe_transaction(),
               "mutations": mutations}
    if extra:
        payload.update(extra)
    return api_client.post(dataset_path(API_MUTATE, dataset), json=payload,
                           headers=headers)


def read_doc(api_client, headers: dict, dataset: str, document_id: str,
             perspective: str | None = None):
    params = {"perspective": perspective} if perspective else {}
    return api_client.get(dataset_path(API_DOC, dataset, document_id),
                          params=params, headers=headers)


def doc_body(response) -> dict:
    payload = json_body(response)
    if isinstance(payload, dict):
        inner = payload.get("document")
        if isinstance(inner, dict):
            return inner
        return payload
    return {}


def publish_doc(api_client, headers: dict, dataset: str, document_id: str,
                also: list | None = None):
    payload = {"alsoPublish": also} if also else {}
    return api_client.post(dataset_path(API_PUBLISH, dataset, document_id),
                           json=payload, headers=headers)


def unpublish_doc(api_client, headers: dict, dataset: str, document_id: str):
    return api_client.post(dataset_path(API_UNPUBLISH, dataset, document_id),
                           json={}, headers=headers)


def read_history(api_client, headers: dict, dataset: str, document_id: str):
    return api_client.get(dataset_path(API_HISTORY, dataset, document_id),
                          headers=headers)


def search(api_client, headers: dict, dataset: str, term: str,
           perspective: str | None = None):
    params = {"q": term}
    if perspective:
        params["perspective"] = perspective
    return api_client.get(dataset_path(API_SEARCH, dataset), params=params,
                          headers=headers)


def search_matches(response) -> list:
    payload = json_body(response)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("matches", "results", "hits", "result"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def article_doc(document_id: str, title: str, department: str = DEPARTMENT_ENGINEERING,
                items: int = 0, body: list | None = None) -> dict:
    """A document body the schema accepts, with an optional keyed array."""
    doc = {FIELD_ID: document_id, FIELD_TYPE: TYPE_ARTICLE, "title": title,
           "department": department}
    if items:
        doc["tags"] = [{"_type": "tag", "label": "tag-%d" % n}
                       for n in range(items)]
    if body is not None:
        doc["body"] = body
    return doc


def text_block(text: str, marks: list | None = None,
               style: str = "normal", list_item: str | None = None) -> dict:
    block = {"_type": "block", "style": style,
             "children": [{"_type": "span", "text": text,
                           "marks": marks or []}]}
    if list_item:
        block["listItem"] = list_item
        block["level"] = 1
    return block


def keys_of(items) -> list:
    out = []
    for item in items or []:
        if isinstance(item, dict):
            out.append(item.get("_key"))
    return out


def block_and_span_keys(body) -> list:
    """Every block key and span key in a rich-text array, in document order."""
    out = []
    for block in body or []:
        if not isinstance(block, dict):
            continue
        out.append(block.get("_key"))
        for span in block.get("children") or []:
            if isinstance(span, dict):
                out.append(span.get("_key"))
    return out


def spans_of(block) -> list:
    children = block.get("children") if isinstance(block, dict) else None
    return [s for s in (children or []) if isinstance(s, dict)]


def find_block_with(body, needle: str):
    for block in body or []:
        if not isinstance(block, dict):
            continue
        joined = "".join(str(s.get("text", "")) for s in spans_of(block))
        if needle in joined:
            return block
    return None


def png_bytes(width: int, height: int, tone: int = 120) -> bytes:
    """A real, minimal PNG built here so the suite ships no binary fixture."""
    raw = b""
    for _ in range(height):
        raw += b"\x00" + bytes([tone, tone, tone]) * width

    def chunk(kind: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(raw))
            + chunk(b"IEND", b""))


def upload_asset(api_client, headers: dict, dataset: str, payload: bytes,
                 filename: str = "probe.png", content_type: str = "image/png"):
    files = {"file": (filename, io.BytesIO(payload), content_type)}
    return api_client.post(dataset_path(API_ASSETS, dataset), files=files,
                           headers=headers)


def asset_id_of(response) -> str:
    payload = json_body(response)
    value = field(payload, "_id", "assetId", "id")
    if not value and isinstance(payload, dict):
        inner = payload.get("asset")
        if isinstance(inner, dict):
            value = field(inner, "_id", "assetId", "id")
    return str(value) if value else ""


def read_asset(api_client, headers: dict | None, dataset: str, asset_id: str,
               params: dict | None = None):
    return api_client.get(dataset_path(API_ASSETS, dataset, asset_id),
                          params=params or {}, headers=headers or {})


def run_migration(api_client, headers: dict, name: str, dataset: str,
                  mode: str = MODE_DRY_RUN, phase: str = PHASE_MIGRATE,
                  confirm_name: str | None = None, extra: dict | None = None):
    payload = {"name": name, "dataset": dataset, "mode": mode, "phase": phase}
    if confirm_name is not None:
        payload["confirm_name"] = confirm_name
    if extra:
        payload.update(extra)
    return api_client.post(API_MIGRATIONS, json=payload, headers=headers)


def read_audit(api_client, headers: dict, params: dict | None = None):
    return api_client.get(API_AUDIT, params=params or {}, headers=headers)


def audit_entries(response) -> list:
    payload = json_body(response)
    return payload if isinstance(payload, list) else []


def submit_lead(api_client, work_email: str, company: str,
                extra: dict | None = None):
    payload = {"work_email": work_email, "name": "Probe Reader",
               "company": company, "team_size": "2-10",
               "message": "A probe enquiry about the content platform."}
    if extra:
        payload.update(extra)
    return api_client.post(API_LEADS, json=payload)


def in_parallel(call, count: int):
    """Run one zero-argument call `count` times at once and return every result."""
    with ThreadPoolExecutor(max_workers=min(count, 16)) as pool:
        return [f.result() for f in [pool.submit(call) for _ in range(count)]]


def internal_links(markup: str) -> list:
    """Every same-origin link target on a served page, deduplicated."""
    out = []
    for href in HREF_RE.findall(markup or ""):
        target = href.strip()
        if not target or target.startswith(("http://", "https://", "mailto:",
                                            "tel:", "javascript:", "data:")):
            continue
        if not target.startswith("/"):
            continue
        if target not in out:
            out.append(target)
    return out


def page_title(markup: str) -> str:
    found = TITLE_RE.search(markup or "")
    return found.group(1).strip() if found else ""
