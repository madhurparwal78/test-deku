"""Fixtures, pinned literals and the one sanctioned sleep for the Verso task.

Every value here appears verbatim in instruction.md. Nothing in this file
inspects the application's source: the observations are HTTP responses, rows in
the declared datastore and messages on the declared mail server.
"""

from __future__ import annotations

import os
import re
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

import httpx
import pytest

import appclient
import capabilities

PASSWORD = "deku-demo-pw-2026"
EDITOR_EMAIL = "editor@example.com"
EDITOR2_EMAIL = "editor2@example.com"
COMMERCIAL_EMAIL = "commercial@example.com"
COMMERCIAL2_EMAIL = "commercial2@example.com"

FR = "fr"
EN = "en"

MAISON_CARRE = "maison-carre"
ATELIER_BRUNE = "atelier-brune"
PORT_NEUF = "port-neuf"
SERRE_VERTE = "serre-verte"
LUNE_BASSE = "lune-basse"
QUAI_DOUZE = "quai-douze"

CARRE_HOUSE = "carre-house"
BRUNE_STUDIO = "brune-studio"
NEW_HARBOUR = "new-harbour"
GREEN_GLASSHOUSE = "green-glasshouse"
LOW_MOON = "low-moon"

ART_DIRECTION = "art_direction"
DIGITAL_EXPERIENCE = "digital_experience"
SHOWCASE_SITE = "showcase_site"
COMMERCE = "commerce"
DISCIPLINES = (ART_DIRECTION, DIGITAL_EXPERIENCE, SHOWCASE_SITE, COMMERCE)

MODE_ANY = "any"
MODE_ALL = "all"

FRENCH_TOTAL = 5
FRENCH_FACET_SUM = 9

BRANCH_PROJECT = "project"
BRANCH_APPLICATION = "application"
BRANCH_QUESTION = "question"

REFERENCE_PATTERN = re.compile(r"^VRS-[A-Z0-9]{6}$")
REFERENCE_PREFIX = "VRS-"

PROJECT_SUBJECT = "Nous avons bien recu votre demande"
APPLICATION_SUBJECT = "Votre candidature est bien arrivee"
OUTCOME_SUBJECT = "Suite a votre candidature"

CONSENT_TEXT = ("J'accepte que Verso conserve ces informations pour repondre "
                "a ma demande.")
EMPTY_FILTER_TITLE = "Aucun projet ne correspond"
NOTHING_PUBLISHED_TITLE = "Bientot"
GONE_COPY = "Cette page a ete retiree volontairement."
NOT_FOUND_COPY = ("Cette page n'existe pas, ou plus. Voici trois choses qui "
                  "existent.")
SWITCH_UNAVAILABLE_FR = "Cette page n'existe pas encore en anglais"
CONFIRMATION_HEADING = "C'est envoye"

PENDING_SCAN = "pending_scan"
CLEAN = "clean"

STATE_DRAFT = "draft"
STATE_PUBLISHED = "published"
STATE_WITHDRAWN = "withdrawn"

LEAD_NEW = "new"
LEAD_CLOSED = "closed"

FRENCH_ROUTES = ("/", "/projets/", "/expertises/", "/agence/", "/contact/",
                 "/mentions-legales/", "/confidentialite/")
ENGLISH_ROUTES = ("/en/", "/en/projects/", "/en/expertise/", "/en/agency/",
                  "/en/contact/", "/en/legal/", "/en/privacy/")

SECURITY_HEADERS = ("strict-transport-security", "x-content-type-options",
                    "referrer-policy", "content-security-policy")

SETTLE_SECONDS = 2.0
POLL_CEILING_SECONDS = 90.0
CONTENDERS = 8
OK = (200, 201)
REDIRECTED = (301, 308)
REFUSED = (400, 403, 409, 422)
DENIED = (401, 403)
MISSING = (401, 403, 404)


def settle() -> None:
    """The only sanctioned sleep. A bounded wait before asserting an absence."""
    time.sleep(SETTLE_SECONDS)


def unique_key() -> str:
    return f"probe-{uuid.uuid4().hex}"


def unique_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


def unique_slug() -> str:
    return f"probe-{os.urandom(5).hex()}"


def poll_until(predicate, deadline_seconds: float):
    """Poll to a monotonic deadline. Returns the first truthy result, else None."""
    limit = min(float(deadline_seconds), POLL_CEILING_SECONDS)
    started = time.monotonic()
    result = predicate()
    while not result and (time.monotonic() - started) < limit:
        settle()
        result = predicate()
    return result


def body_excerpt(response) -> str:
    return response.text[:400]


def as_list(payload):
    if isinstance(payload, dict):
        for key in ("results", "items", "data"):
            if isinstance(payload.get(key), list):
                return payload[key]
        return []
    return payload if isinstance(payload, list) else []


def page(path: str, headers=None, follow: bool = True):
    return httpx.get(f"{appclient.app_url()}{path}", timeout=30.0,
                     headers=headers or {}, follow_redirects=follow)


def catalogue(client, locale: str = FR, **params):
    query = {"locale": locale}
    query.update(params)
    response = client.get("/catalogue", params=query)
    assert response.status_code == 200, (
        f"GET /api/catalogue?locale={locale} returned {response.status_code}: "
        f"{body_excerpt(response)}"
    )
    payload = response.json()
    assert isinstance(payload, dict), (
        f"GET /api/catalogue returned {type(payload).__name__}, expected an object "
        f"carrying total, facets and results: {body_excerpt(response)}"
    )
    return payload


def facet_counts(payload):
    facets = payload.get("facets")
    assert facets is not None, (
        f"the catalogue payload carries no facets: {payload!r}"
    )
    if isinstance(facets, dict):
        return {str(key): int(value) for key, value in facets.items()}
    counts = {}
    for row in facets:
        name = row.get("discipline", row.get("name", row.get("key")))
        assert name is not None, f"a facet row names no discipline: {row!r}"
        counts[str(name)] = int(row.get("count", row.get("total", 0)))
    return counts


def results_of(payload):
    rows = payload.get("results")
    assert isinstance(rows, list), (
        f"the catalogue payload carries no results array: {payload!r}"
    )
    return rows


def slugs_of(payload):
    return [row.get("slug") for row in results_of(payload)]


def project_detail(client, slug: str, locale: str = FR):
    response = client.get(f"/projects/{slug}", params={"locale": locale})
    assert response.status_code == 200, (
        f"GET /api/projects/{slug} returned {response.status_code}: "
        f"{body_excerpt(response)}"
    )
    return response.json()


def blocks_of(detail):
    rows = detail.get("blocks")
    assert isinstance(rows, list) and rows, (
        f"the project detail carries no blocks array: {detail!r}"
    )
    return rows


def enquiry_payload(branch: str = BRANCH_PROJECT, email: str | None = None,
                    consent: bool = True):
    return {
        "branch": branch,
        "locale": FR,
        "consent": consent,
        "answers": [
            {"question": "Que voulez-vous construire ?",
             "answer": "Un site vitrine pour une galerie."},
            {"question": "Quand, et a quelle echelle ?",
             "answer": "Au printemps, une dizaine de pages."},
            {"question": "Qui etes-vous ?",
             "answer": "Une galerie independante."},
        ],
        "email": email or unique_email(),
        "name": "Sasha Devlin",
        "company": "Galerie Devlin",
    }


def submit_enquiry(client, payload, key=None):
    return client.post("/enquiries", json=payload,
                       headers={"Idempotency-Key": key or unique_key()})


def submitted(client, payload, key=None):
    response = submit_enquiry(client, payload, key=key)
    assert response.status_code in OK, (
        f"POST /api/enquiries returned {response.status_code}: "
        f"{body_excerpt(response)}"
    )
    return response.json()


def reference_of(payload):
    for key in ("reference", "ref"):
        value = payload.get(key)
        if value:
            return value
    nested = payload.get("lead") or {}
    for key in ("reference", "ref"):
        value = nested.get(key)
        if value:
            return value
    raise AssertionError(f"the enquiry response carries no reference: {payload!r}")


def lead_rows(client, **params):
    response = client.get("/console/leads", params=params)
    assert response.status_code == 200, (
        f"GET /api/console/leads returned {response.status_code}: "
        f"{body_excerpt(response)}"
    )
    return as_list(response.json())


def lead_by_reference(client, reference: str):
    for row in lead_rows(client):
        if row.get("reference") == reference:
            return row
    return None


def console_projects(client, **params):
    response = client.get("/console/projects", params=params)
    assert response.status_code == 200, (
        f"GET /api/console/projects returned {response.status_code}: "
        f"{body_excerpt(response)}"
    )
    return as_list(response.json())


def console_project_id(client, slug: str):
    for row in console_projects(client):
        if row.get("slug") == slug:
            found = row.get("project_id", row.get("id"))
            assert found is not None, (
                f"the console row for {slug!r} carries no project_id: {row!r}"
            )
            return found
    raise AssertionError(
        f"no seeded project with the French slug {slug!r} in "
        f"GET /api/console/projects; the six seeded French slugs are "
        f"{MAISON_CARRE}, {ATELIER_BRUNE}, {PORT_NEUF}, {SERRE_VERTE}, "
        f"{LUNE_BASSE}, {QUAI_DOUZE}"
    )


def activity_rows(client, **params):
    response = client.get("/console/activity", params=params)
    assert response.status_code == 200, (
        f"GET /api/console/activity returned {response.status_code}: "
        f"{body_excerpt(response)}"
    )
    return as_list(response.json())


def redirect_rows(client):
    response = client.get("/console/redirects")
    assert response.status_code == 200, (
        f"GET /api/console/redirects returned {response.status_code}: "
        f"{body_excerpt(response)}"
    )
    return as_list(response.json())


def race(callables):
    with ThreadPoolExecutor(max_workers=len(callables)) as pool:
        return [future.result() for future in
                [pool.submit(fn) for fn in callables]]


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def inbox():
    return capabilities.make_inbox()


@pytest.fixture()
def anon():
    with httpx.Client(base_url=appclient.api_base(), timeout=30.0) as client:
        yield client


@pytest.fixture()
def editor():
    with appclient.client(appclient.login(EDITOR_EMAIL, PASSWORD)) as client:
        yield client


@pytest.fixture()
def other_editor():
    with appclient.client(appclient.login(EDITOR2_EMAIL, PASSWORD)) as client:
        yield client


@pytest.fixture()
def commercial():
    with appclient.client(appclient.login(COMMERCIAL_EMAIL, PASSWORD)) as client:
        yield client


@pytest.fixture()
def other_commercial():
    with appclient.client(appclient.login(COMMERCIAL2_EMAIL, PASSWORD)) as client:
        yield client


@pytest.fixture()
def fresh_account():
    """A signed-up account nobody else in this run shares."""
    email = unique_email()
    response = httpx.post(f"{appclient.api_base()}/auth/signup",
                          json={"email": email, "password": PASSWORD},
                          timeout=30.0)
    assert response.status_code in OK, (
        f"POST /api/auth/signup for {email} returned {response.status_code}: "
        f"{body_excerpt(response)}"
    )
    with appclient.client(appclient.login(email, PASSWORD)) as client:
        yield client
