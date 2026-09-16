"""Task fixtures for deku/agency-delivery-console-vb.

Implementation agnostic: nothing here assumes the agent's framework, file layout or
module names. The assumptions are the App Contract (the app answers at APP_PUBLIC_URL
with its HTTP API under /api), the contract and seeded fixtures instruction.md pins,
and the verifier-side services the task declares: the datastore at DB_ADMIN_URL and
DATABASE_URL, and the Mailpit inbox.

Every scenario that writes provisions its own milestones, deliverables, drafts, leads
and access requests, so nothing asserted here depends on what the browser workflows
did before pytest ran.
"""

from __future__ import annotations

import os
import re
import threading
import time
from datetime import datetime, timedelta, timezone

import httpx
from appclient import api_base, app_url
from capabilities import PostgresBackend, make_inbox

PASSWORD = "deku-demo-pw-2026"

ADMIN = "admin@parallax.example.com"
FINANCE_FR = "finance.fr@parallax.example.com"
FINANCE2_FR = "finance2.fr@parallax.example.com"
FINANCE_MT = "finance.mt@parallax.example.com"
DIRECTOR_FR = "director.fr@parallax.example.com"
DIRECTOR_MT = "director.mt@parallax.example.com"
PM = "pm.fr@parallax.example.com"
DESIGNER = "designer.fr@parallax.example.com"
DEV = "dev.fr@parallax.example.com"
SECURITY = "security@parallax.example.com"
ANALYST = "analyst@parallax.example.com"
RECRUITER = "recruiter@parallax.example.com"
FREELANCE = "freelance@kite-studio.example.com"

AERO_OWNER = "owner@aeroline.example.com"
AERO_BRAND1 = "brand1@aeroline.example.com"
AERO_BRAND2 = "brand2@aeroline.example.com"
AERO_PROCUREMENT = "procurement@aeroline.example.com"
AERO_COLLAB = "collab@aeroline.example.com"
AERO_BILLING = "billing@aeroline.example.com"
VERDANE_OWNER = "owner@verdane.example.com"
INSTITUT_OWNER = "owner@institut-lumiere.example.com"

AERO_PROJECT = "AERO-2026-01"
VERDANE_PROJECT = "VERD-2026-01"
INSTITUT_PROJECT = "INST-2026-01"
INSTITUT_CONTRACT = "PXF-CT-2026-003"

FRANCE = "parallax-france"
MALTA = "parallax-malta"
FRANCE_NAME = "Parallax France SAS"
MALTA_NAME = "Parallax Malta Ltd"

OPEN_VERDANE_TICKET = "PX-2026-000142"
CLOSED_VERDANE_TICKET = "PX-2026-000143"
OPEN_AEROLINE_TICKET = "PX-2026-000150"

SECRET_VALUES = {
    "Production CMS admin@verdane": "vlt-verdane-cms-4471-QZ",
    "Hosting control panel@verdane": "vlt-verdane-host-9022-KP",
    "DNS registrar@verdane": "vlt-verdane-dns-3318-LM",
    "Production CMS admin@aeroline": "vlt-aeroline-cms-7710-RT",
}
NEVER_REVEALED = ("vlt-verdane-dns-3318-LM", "vlt-aeroline-cms-7710-RT")
CLIENT_SECRET = "parallax-client-secret-2026"
DB_PASSWORD = "deku-local-dev"

APPROVAL_SUBJECT = "Parallax: approval requested for "
EN_LEAD_SUBJECT = "Parallax: we received your brief "
FR_LEAD_SUBJECT = "Parallax : demande reçue "
NOT_FOUND_DETAIL = "Not found, or you do not have access"
ZERO_HASH = "0" * 64

SETTLE_SECONDS = 1.0
TIMEOUT = 30.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    time.sleep(seconds)


def uid(prefix: str) -> str:
    return f"{prefix}-{os.urandom(4).hex()}"


def this_year() -> int:
    return datetime.now(timezone.utc).year


def instant_in(seconds: float) -> str:
    moment = datetime.now(timezone.utc) + timedelta(seconds=seconds)
    return moment.isoformat(timespec="seconds").replace("+00:00", "Z")


def seconds_until(iso_instant: str) -> float:
    target = datetime.fromisoformat(iso_instant.replace("Z", "+00:00"))
    return (target - datetime.now(timezone.utc)).total_seconds()


def body(response: httpx.Response):
    try:
        return response.json()
    except ValueError as exc:
        raise AssertionError(
            f"{response.request.method} {response.request.url.path} answered "
            f"{response.status_code} with a non-JSON body: {response.text[:300]}") from exc


def code_of(response: httpx.Response):
    if "json" not in response.headers.get("content-type", "") or not response.content:
        return None
    payload = response.json()
    return payload.get("code") if isinstance(payload, dict) else None


def expect(response: httpx.Response, *statuses: int):
    assert response.status_code in statuses, (
        f"{response.request.method} {response.request.url.path} answered "
        f"{response.status_code}, expected {statuses}: {response.text[:400]}")
    return body(response) if response.content else {}


def refusal(response: httpx.Response, status: int, code: str) -> dict:
    assert response.status_code == status and code_of(response) == code, (
        f"{response.request.method} {response.request.url.path} answered "
        f"{response.status_code} code {code_of(response)!r}, expected {status} "
        f"{code!r}: {response.text[:400]}")
    return body(response)


def http(token: str | None = None, headers: dict | None = None) -> httpx.Client:
    merged = dict(headers or {})
    if token:
        merged["Authorization"] = f"Bearer {token}"
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, headers=merged)


def site_client() -> httpx.Client:
    return httpx.Client(base_url=app_url(), timeout=TIMEOUT, follow_redirects=False)


def login_payload(email: str) -> dict:
    with http() as c:
        payload = expect(c.post("/auth/login", json={"email": email, "password": PASSWORD}), 200)
    assert payload.get("access_token"), f"login for {email} returned no access_token: {payload}"
    return payload


def token_for(email: str) -> str:
    return login_payload(email)["access_token"]


def step_up(token: str) -> None:
    with http(token) as c:
        payload = expect(c.post("/auth/step-up", json={"password": PASSWORD}), 200)
    assert payload.get("step_up_at"), f"step-up returned no step_up_at: {payload}"


def stepped_up(email: str) -> str:
    token = token_for(email)
    step_up(token)
    return token


def get_json(token: str, path: str, **params):
    with http(token) as c:
        return expect(c.get(path, params=params or None), 200)


def org_id(token: str, slug: str) -> str:
    orgs = get_json(token, "/orgs", slug=slug)
    for org in orgs:
        if org.get("slug") == slug:
            return org["id"]
    raise AssertionError(f"GET /api/orgs?slug={slug} lists no such organisation: {orgs}")


def project_id(token: str, code: str) -> str:
    projects = get_json(token, "/projects", code=code)
    for project in projects:
        if project.get("code") == code:
            return project["id"]
    raise AssertionError(f"GET /api/projects?code={code} lists no such project: {projects}")


def contract_by_reference(token: str, client_org: str, reference: str) -> dict:
    contracts = get_json(token, "/contracts", client_org_id=client_org)
    for contract in contracts:
        if contract.get("reference") == reference:
            return contract
    raise AssertionError(f"GET /api/contracts lists no contract {reference}: {contracts}")


def invoice_by_number(token: str, entity: str, number: str) -> dict:
    invoices = get_json(token, "/invoices", agency_entity=entity)
    for invoice in invoices:
        if invoice.get("number") == number:
            return invoice
    raise AssertionError(f"GET /api/invoices lists no invoice numbered {number}")


def mutated_id(identifier: str) -> str:
    chars = list(str(identifier))
    for i in range(len(chars) - 1, -1, -1):
        ch = chars[i]
        if ch.isdigit():
            chars[i] = "7" if ch != "7" else "3"
            return "".join(chars)
        if ch.isalpha():
            swap = "b" if ch.lower() != "b" else "c"
            chars[i] = swap.upper() if ch.isupper() else swap
            return "".join(chars)
    raise AssertionError(f"identifier {identifier!r} has no character to alter")


def new_milestone(token: str, project: str, amount: int, name: str | None = None) -> dict:
    with http(token) as c:
        return expect(c.post(f"/projects/{project}/milestones",
                             json={"name": name or uid("Milestone"),
                                   "bill_amount_minor": amount}), 201)


def new_deliverable(token: str, project: str, milestone: str, name: str | None = None) -> dict:
    with http(token) as c:
        return expect(c.post(f"/projects/{project}/deliverables",
                             json={"name": name or uid("Deliverable"), "kind": "design",
                                   "milestone_id": milestone}), 201)


def upload_version(token: str, deliverable: str) -> dict:
    with http(token) as c:
        return expect(c.post(f"/deliverables/{deliverable}/versions",
                             json={"notes": "Homepage direction"}), 201)


def share(token: str, deliverable: str) -> dict:
    with http(token) as c:
        return expect(c.post(f"/deliverables/{deliverable}/share"), 201)


def decide(token: str, approval: str, version: str, decision: str = "approved",
           comment: str = "Reviewed") -> httpx.Response:
    with http(token) as c:
        return c.post(f"/approvals/{approval}/decisions",
                      json={"decision": decision, "comment": comment, "version_id": version})


def read_approval(token: str, approval: str) -> dict:
    return get_json(token, f"/approvals/{approval}")


def shared_approval(project_code: str, amount: int, uploader: str = DESIGNER,
                    name: str | None = None) -> dict:
    pm = token_for(PM)
    project = project_id(pm, project_code)
    milestone = new_milestone(pm, project, amount)
    deliverable = new_deliverable(pm, project, milestone["id"], name)
    version = upload_version(token_for(uploader), deliverable["id"])
    approval = share(pm, deliverable["id"])
    return {"pm": pm, "project": project, "milestone": milestone, "deliverable": deliverable,
            "version": version, "approval": approval}


def stage(approval: dict, number: int) -> dict:
    for entry in approval.get("stages", []):
        if entry.get("stage") == number:
            return entry
    raise AssertionError(f"approval has no stage {number}: {approval}")


def milestone_invoices(token: str, milestone: str) -> list:
    return get_json(token, "/invoices", milestone_id=milestone)


def wait_for_milestone_invoice(token: str, milestone: str, deadline_seconds: float = 10.0) -> dict:
    return poll(lambda: get_json(token, f"/milestones/{milestone}"),
                lambda m: bool(m.get("invoice_id")), deadline_seconds)


def draft_invoice(token: str, client_org: str, lines: list[tuple[int, int]],
                  po_number: str | None = None, **extra) -> dict:
    payload = {"client_org_id": client_org,
               "lines": [{"description": uid("Line"), "quantity": q, "unit_price_minor": p}
                         for q, p in lines],
               "po_number": po_number, **extra}
    with http(token) as c:
        return expect(c.post("/invoices", json=payload), 201)


def issue(token: str, invoice: str) -> httpx.Response:
    with http(token) as c:
        return c.post(f"/invoices/{invoice}/issue")


def read_invoice(token: str, invoice: str) -> dict:
    return get_json(token, f"/invoices/{invoice}")


def number_parts(number: str, prefix: str) -> tuple[int, int]:
    match = re.fullmatch(rf"{re.escape(prefix)}(\d{{4}})-(\d{{5}})", number or "")
    assert match, f"number {number!r} is not {prefix}<year>-<five digits>"
    return int(match.group(1)), int(match.group(2))


def run_together(requests: list) -> list[httpx.Response]:
    clients = [http(token, headers) for token, headers, _ in requests]
    for c in clients:
        c.get("/health")
    barrier = threading.Barrier(len(requests))
    results: list = [None] * len(requests)

    def fire(index: int) -> None:
        _, _, call = requests[index]
        barrier.wait()
        results[index] = call(clients[index])

    threads = [threading.Thread(target=fire, args=(i,)) for i in range(len(requests))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    for c in clients:
        c.close()
    assert all(r is not None for r in results), "a simultaneous request never completed"
    return results


def secret_id(token: str, client_org: str, label: str) -> str:
    secrets = get_json(token, "/vault/secrets", client_org_id=client_org)
    for secret in secrets:
        assert "value" not in secret, f"the secret list returned a value: {secret}"
        if secret.get("label") == label:
            return secret["id"]
    raise AssertionError(f"GET /api/vault/secrets lists no secret labelled {label}: {secrets}")


def access_request(token: str, secret: str, ticket: str | None = OPEN_VERDANE_TICKET,
                   ttl: int = 30, break_glass: bool = False) -> httpx.Response:
    payload = {"secret_id": secret, "justification": "Storefront outage investigation",
               "ticket_reference": ticket, "requested_ttl_minutes": ttl,
               "break_glass": break_glass}
    with http(token) as c:
        return c.post("/vault/access-requests", json=payload)


def approve_request(token: str, request: str) -> httpx.Response:
    with http(token) as c:
        return c.post(f"/vault/access-requests/{request}/approve")


def reveal(token: str, secret: str, request: str) -> httpx.Response:
    with http(token) as c:
        return c.post(f"/vault/secrets/{secret}/reveal", json={"request_id": request})


def access_log(token: str) -> list:
    return get_json(token, "/vault/access-log")


def verify_log(token: str) -> dict:
    with http(token) as c:
        return expect(c.post("/vault/access-log/verify"), 200)


def admin_db() -> PostgresBackend:
    return PostgresBackend(os.environ["DB_ADMIN_URL"])


def app_db() -> PostgresBackend:
    return PostgresBackend(os.environ["DATABASE_URL"])


def replica_statement(statement: str) -> None:
    admin_db().query(
        "DO $tamper$ BEGIN "
        "PERFORM set_config('session_replication_role', 'replica', true); "
        f"{statement}; "
        "END $tamper$")


def probe_statement(backend: PostgresBackend, statement: str) -> None:
    backend.query(
        "DO $probe$ BEGIN "
        f"{statement}; "
        "EXCEPTION WHEN OTHERS THEN NULL; "
        "END $probe$")


def lead_body(email: str, site: str = "en", country: str = "FR", phone: str = "+33612345678",
              **overrides) -> dict:
    payload = {"form": "start_a_project", "site": site, "first_name": "Camille",
               "last_name": "Rousseau", "email": email, "phone": phone,
               "company_name": "Atelier Rousseau", "company_country": country,
               "budget": "band_20_30k", "kind": "website",
               "message": "We need a new storefront before the spring collection.",
               "consent": True, "marketing_consent": False, "website": ""}
    payload.update(overrides)
    return payload


def post_lead(payload: dict, key: str | None) -> httpx.Response:
    headers = {"Idempotency-Key": key} if key else {}
    with http(headers=headers) as c:
        return c.post("/public/leads", json=payload)


def lead_rows(email: str) -> list[dict]:
    return admin_db().query(
        "SELECT reference, email, status, budget, kind, entity, gclid FROM leads "
        "WHERE lower(email) = lower(%s)", (email,))


def inbox():
    return make_inbox()


def messages_to(to: str, subject: str) -> list:
    return [m for m in inbox()._messages()
            if any(to.lower() in addr.lower() for addr in m.to) and m.subject == subject]


def messages_containing(to: str, needle: str) -> list:
    return [m for m in inbox()._messages()
            if any(to.lower() in addr.lower() for addr in m.to) and needle in m.subject]


def poll(fetch, done, deadline_seconds: float, interval: float = 0.5):
    deadline = time.monotonic() + deadline_seconds
    last = fetch()
    while not done(last):
        if time.monotonic() >= deadline:
            return last
        settle(interval)
        last = fetch()
    return last


def wait_for_mail(to: str, subject: str, deadline_seconds: float = 30.0) -> list:
    return poll(lambda: messages_to(to, subject), lambda found: len(found) > 0, deadline_seconds)


def page(path: str) -> httpx.Response:
    with site_client() as c:
        return c.get(path)


def tag_attributes(raw: str) -> dict:
    return {m.group(1).lower(): (m.group(2) if m.group(2) is not None else m.group(3))
            for m in re.finditer(r'([a-zA-Z:-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', raw)}


def link_tags(html: str) -> list[dict]:
    return [tag_attributes(raw) for raw in re.findall(r"<link\b[^>]*>", html, flags=re.I)]


def asset_paths(html: str) -> list[str]:
    paths = []
    for raw in re.findall(r"<(?:script|link)\b[^>]*>", html, flags=re.I):
        attrs = tag_attributes(raw)
        ref = attrs.get("src") or attrs.get("href") or ""
        if raw.lower().startswith("<link") and not re.search(
                r"stylesheet|modulepreload|preload|manifest", attrs.get("rel", ""), flags=re.I):
            continue
        if ref.startswith(app_url()):
            ref = ref[len(app_url()):]
        if ref.startswith("/") and not ref.startswith("//"):
            paths.append(ref)
    return paths


def meta_robots(html: str) -> list[str]:
    values = []
    for raw in re.findall(r"<meta\b[^>]*>", html, flags=re.I):
        if re.search(r'name\s*=\s*["\']robots["\']', raw, flags=re.I):
            found = re.search(r'content\s*=\s*["\']([^"\']*)["\']', raw, flags=re.I)
            values.append(found.group(1).lower() if found else "")
    return values


def location_path(response: httpx.Response) -> str:
    location = response.headers.get("location", "")
    return httpx.URL(location).path if location.startswith("http") else location.split("?")[0]
