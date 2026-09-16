"""Fixtures, pinned literals and helpers for the Halden Drops task.

Black-box only: HTTP against the running app, the rendered page through Playwright,
PostgreSQL through the shared backend adapter and MinIO through the shared object-store
adapter. Nothing here reads the agent's source.

Every state-changing grader works on a probe campaign it creates for itself, so the seeded
Afterglow and Dusk Parade records are read and never rewritten by pytest.
"""

from __future__ import annotations

import datetime
import hashlib
import os
import re
import struct
import time
import uuid
import zlib
from urllib.parse import parse_qs, unquote, urlparse

import httpx
import pytest

import capabilities

TIMEOUT = 30.0
OK = (200, 201)

PASSWORD = "deku-demo-pw-2026"
OWNER = "owner@example.com"
EDITOR = "editor@example.com"
EDITOR2 = "editor2@example.com"
EDITOR3 = "editor3@example.com"
TRANSLATOR = "translator@example.com"
LEGAL = "legal@example.com"
LEGAL2 = "legal2@example.com"
MERCHANDISER = "merchandiser@example.com"
SIGN_IN_FAILED = "Sign-in failed"

MARKETS = ("fr", "en", "it", "es", "de", "be-nl", "be-fr")
HREFLANG = {"fr": "fr-FR", "en": "en", "it": "it", "es": "es", "de": "de",
            "be-nl": "nl", "be-fr": "fr-BE"}
CURRENCY = {"fr": "EUR", "en": "GBP", "it": "EUR", "es": "EUR", "de": "EUR",
            "be-nl": "EUR", "be-fr": "EUR"}
HOST = {"fr": "shop-fr.example.com", "en": "shop-uk.example.com",
        "it": "shop-it.example.com", "es": "shop-es.example.com",
        "de": "shop-de.example.com", "be-nl": "shop-be.example.com",
        "be-fr": "shop-be.example.com"}
SEGMENT = {"fr": "", "en": "", "it": "", "es": "/es", "de": "", "be-nl": "/nl",
           "be-fr": "/fr"}
LEGAL_SLUG = {"fr": "mentions-legales", "en": "legal-notice", "it": "note-legali",
              "es": "aviso-legal", "de": "impressum",
              "be-nl": "wettelijke-vermeldingen", "be-fr": "mentions-legales"}
DISPLAY_NAME = {"fr": "Français", "en": "English", "it": "Italiano", "es": "Español",
                "de": "Deutsch", "be-nl": "Nederlands (België)",
                "be-fr": "Français (Belgique)"}
LEGAL_GRANTEE = {"fr": LEGAL, "en": LEGAL, "be-nl": LEGAL, "de": LEGAL2, "it": LEGAL2,
                 "es": LEGAL2, "be-fr": LEGAL2}

AFTERGLOW = "afterglow"
DUSK_PARADE = "dusk-parade"
ATTRIBUTION_PARAM = "hscamp"
ATTRIBUTION_PREFIX = "hscamp:__drop-"
LANG_COOKIE = "drop_lang"
COOKIE_MAX_AGE = 31536000

TEE = "482913"
JACKET = "482927"
PANTS = "482940"
RX2K = "482956"
DUSK_PRODUCT = "483101"
TEE_PINK = "7310042"
TEE_WHITE = "7310043"
SLOTS = {"7310042": "p1", "7310043": "p2", "7310118": "p3", "7310119": "p4",
         "7310205": "p5", "7310377": "p6", "7310378": "p7"}
EURO_PRICES = {TEE: 2000, JACKET: 4500, PANTS: 3500, RX2K: 9000}
POUND_PRICES = {TEE: 1700, JACKET: 3900, RX2K: 7900}
DISPLAY = {"fr": "20,00 €", "it": "20,00 €", "es": "20,00 €", "de": "20,00 €",
           "be-fr": "20,00 €", "be-nl": "€ 20,00", "en": "£17.00"}

HERO_TITLE = {
    "fr": "Afterglow, la collection capsule Halden Sport x Tove Ardenne",
    "en": "Afterglow, the Halden Sport x Tove Ardenne capsule collection",
}
META_TITLE = {"fr": "Afterglow, la capsule Halden Sport x Tove Ardenne",
              "en": "Afterglow, the Halden Sport x Tove Ardenne capsule"}
META_DESCRIPTION = {
    "fr": "Quatre pièces rétro dessinées avec Tove Ardenne, en édition limitée.",
    "en": "Four retro pieces designed with Tove Ardenne, in a limited drop.",
}
COLLECTION_HEADING = {"fr": "La collection", "en": "The collection"}
ARTIST_HEADING = {"fr": "Salut, je suis Tove Ardenne", "en": "Hi, I am Tove Ardenne"}
STORY_HEADING = {"fr": "L'histoire de la RX2K", "en": "The RX2K story"}
LOOKBOOK_HEADING = "Lookbook"
LOOKBOOK_ALT = {"fr": "Deux coureurs en veste pervenche sur une piste au coucher du soleil",
                "en": "Two runners in periwinkle jackets on a track at sunset"}
WORDMARK_HOST = "halden.example.com"
WORDMARK_NAME = "Halden Sport"
LEGAL_TITLE = {"fr": "Mentions légales", "en": "Legal notice"}
LEGAL_ADDRESS = "12 rue des Tanneurs, 59000 Lille"
LANG_LABEL = {"fr": "Choisir la langue", "en": "Choose language"}
SHOP_CTA = {"fr": "Boutique", "en": "Shop"}
MENU_LABEL = {"fr": "Menu", "en": "Menu"}
MENU_CLOSE = {"fr": "Fermer", "en": "Close"}
NEWTAB_SUFFIX = {"fr": "ouvre la boutique dans un nouvel onglet",
                 "en": "opens the shop in a new tab"}
BE_FR_SHOP_CTA = "Boutique"
DE_SHOP_CTA = "Shop"
DUSK_HERO_BE_NL = "Dusk Parade, lopen na zonsondergang"
ANCHORS = ("collection", "ardenne", "rx2k", "lookbook")

SEED_COPY = {
    ("afterglow", "fr"): {
        "meta.title": "Afterglow, la capsule Halden Sport x Tove Ardenne",
        "meta.description": "Quatre pièces rétro dessinées avec Tove Ardenne, en édition limitée.",
        "hero.title": "Afterglow, la collection capsule Halden Sport x Tove Ardenne",
        "tagline.one": "À vos côtés depuis 1976",
        "collage.headline": "Plongez au cœur de la décennie la plus vibrante qui soit",
        "collection.heading": "La collection",
        "artist.heading": "Salut, je suis Tove Ardenne",
        "artist.bio": "Illustratrice née à Lyon, je dessine le sport comme un souvenir de cour de récréation.",
        "story.heading": "L'histoire de la RX2K",
        "story.body": "Une chaussure de course de 1999, redessinée trait pour trait à partir de ses plans d'origine.",
        "lookbook.heading": "Lookbook",
        "lookbook.alt": "Deux coureurs en veste pervenche sur une piste au coucher du soleil",
        "menu.label": "Menu", "menu.close": "Fermer", "shop.cta": "Boutique",
        "lang.label": "Choisir la langue",
        "newtab.suffix": "ouvre la boutique dans un nouvel onglet",
        "legal.title": "Mentions légales",
        "legal.body": "Ce site est édité par Halden Sport SA, 12 rue des Tanneurs, 59000 Lille. Conception : Parallel Studio.",
        "product.482913.name": "T-shirt graphique", "product.482927.name": "Veste de survêtement",
        "product.482940.name": "Pantalon de survêtement", "product.482956.name": "RX2K",
        "colour.7310042.name": "Rose", "colour.7310043.name": "Blanc",
        "colour.7310118.name": "Pervenche", "colour.7310119.name": "Blanc cassé",
        "colour.7310205.name": "Pervenche", "colour.7310377.name": "Sarcelle profonde",
        "colour.7310378.name": "Blanc",
    },
    ("afterglow", "en"): {
        "meta.title": "Afterglow, the Halden Sport x Tove Ardenne capsule",
        "meta.description": "Four retro pieces designed with Tove Ardenne, in a limited drop.",
        "hero.title": "Afterglow, the Halden Sport x Tove Ardenne capsule collection",
        "tagline.one": "Right beside you since 1976",
        "collage.headline": "Dive into the most vibrant decade there ever was",
        "collection.heading": "The collection",
        "artist.heading": "Hi, I am Tove Ardenne",
        "artist.bio": "An illustrator born in Lyon, I draw sport the way you remember a school playground.",
        "story.heading": "The RX2K story",
        "story.body": "A 1999 running shoe, redrawn line for line from its original plans.",
        "lookbook.heading": "Lookbook",
        "lookbook.alt": "Two runners in periwinkle jackets on a track at sunset",
        "menu.label": "Menu", "menu.close": "Close", "shop.cta": "Shop",
        "lang.label": "Choose language", "newtab.suffix": "opens the shop in a new tab",
        "legal.title": "Legal notice",
        "legal.body": "This site is published by Halden Sport SA, 12 rue des Tanneurs, 59000 Lille. Design: Parallel Studio.",
        "product.482913.name": "Graphic tee", "product.482927.name": "Track jacket",
        "product.482940.name": "Track pants", "product.482956.name": "RX2K",
        "colour.7310042.name": "Pink", "colour.7310043.name": "White",
        "colour.7310118.name": "Periwinkle", "colour.7310119.name": "Off white",
        "colour.7310205.name": "Periwinkle", "colour.7310377.name": "Deep teal",
        "colour.7310378.name": "White",
    },
    ("afterglow", "it"): {
        "lang.label": "Scegli la lingua", "shop.cta": "Negozio", "menu.label": "Menu",
        "menu.close": "Chiudi", "newtab.suffix": "apre il negozio in una nuova scheda",
        "legal.title": "Note legali",
        "hero.title": "Afterglow, la collezione capsule Halden Sport x Tove Ardenne",
    },
    ("afterglow", "es"): {
        "lang.label": "Elegir idioma", "shop.cta": "Tienda", "menu.label": "Menú",
        "menu.close": "Cerrar", "newtab.suffix": "abre la tienda en una pestaña nueva",
        "legal.title": "Aviso legal",
        "hero.title": "Afterglow, la colección cápsula Halden Sport x Tove Ardenne",
    },
    ("afterglow", "de"): {
        "lang.label": "Sprache wählen", "shop.cta": "Shop", "menu.label": "Menü",
        "menu.close": "Schließen", "newtab.suffix": "öffnet den Shop in einem neuen Tab",
        "legal.title": "Impressum",
        "hero.title": "Afterglow, die Capsule-Kollektion von Halden Sport x Tove Ardenne",
    },
    ("afterglow", "be-nl"): {
        "lang.label": "Kies je taal", "shop.cta": "Winkel", "menu.label": "Menu",
        "menu.close": "Sluiten", "newtab.suffix": "opent de winkel in een nieuw tabblad",
        "legal.title": "Wettelijke vermeldingen",
        "hero.title": "Afterglow, de capsulecollectie Halden Sport x Tove Ardenne",
    },
    ("afterglow", "be-fr"): {
        "lang.label": "Choisir la langue", "shop.cta": "Boutique", "menu.label": "Menu",
        "menu.close": "Fermer", "newtab.suffix": "ouvre la boutique dans un nouvel onglet",
        "legal.title": "Mentions légales",
        "hero.title": "Afterglow, la collection capsule Halden Sport x Tove Ardenne",
    },
    ("dusk-parade", "be-nl"): {
        "meta.title": "Dusk Parade, de avondcollectie van Halden Sport",
        "meta.description": "Een windjack voor wie na zonsondergang loopt.",
        "hero.title": "Dusk Parade, lopen na zonsondergang",
        "collection.heading": "De collectie", "menu.label": "Menu", "menu.close": "Sluiten",
        "shop.cta": "Winkel", "lang.label": "Kies je taal",
        "newtab.suffix": "opent de winkel in een nieuw tabblad",
        "legal.title": "Wettelijke vermeldingen",
        "legal.body": "Deze site wordt uitgegeven door Halden Sport SA, 12 rue des Tanneurs, 59000 Lille.",
        "product.483101.name": "Nachtloper windjack", "colour.7311550.name": "Diepgrijs",
    },
    ("dusk-parade", "de"): {
        "meta.title": "Dusk Parade, die Abendkollektion von Halden Sport",
        "meta.description": "Eine Windjacke für alle, die nach Sonnenuntergang laufen.",
        "hero.title": "Dusk Parade, Laufen nach Sonnenuntergang",
        "collection.heading": "Die Kollektion", "menu.label": "Menü", "menu.close": "Schließen",
        "shop.cta": "Shop", "lang.label": "Sprache wählen",
        "newtab.suffix": "öffnet den Shop in einem neuen Tab",
        "legal.title": "Impressum",
        "legal.body": "Diese Website wird von Halden Sport SA, 12 rue des Tanneurs, 59000 Lille herausgegeben.",
        "product.483101.name": "Nachtläufer Windjacke", "colour.7311550.name": "Tiefgrau",
    },
}

BASE_KEYS = ("meta.title", "meta.description", "hero.title", "collection.heading",
             "menu.label", "menu.close", "shop.cta", "lang.label", "newtab.suffix",
             "legal.title", "legal.body")
STATUSES = ("draft", "in_review", "approved", "published", "unpublished")
REASONS = ("not_authenticated", "role_not_permitted", "market_out_of_scope",
           "grant_expired", "explicit_deny", "field_not_permitted",
           "role_not_grantable", "invalid", "duplicate", "currency_mismatch",
           "translations_incomplete", "price_missing", "untranslated_copy",
           "machine_legal_text", "approvals_incomplete", "embargo_pending",
           "not_live", "nothing_to_roll_back", "stale_version",
           "precondition_required", "unsupported_media")
AUDIT_ACTIONS = ("campaign.create", "campaign.update", "string.create",
                 "translation.write", "product.create", "product.update",
                 "colourway.create", "price.write", "market.update", "asset.upload",
                 "market.submit", "approval.record", "market.publish",
                 "market.unpublish", "market.rollback", "grant.create", "grant.revoke",
                 "audit.export")
ZERO_HASH = "0" * 64
HEX64 = re.compile(r"^[0-9a-f]{64}$")
PRIVACY_FACTS = ("30 days", "365 days", "7 years", "drop_lang", "legitimate interest", "analytics", "advertising")
DATA_REGIONS = ("eu-west", "uk-south", "eu-central")
SEED_MARKETS = [
    ("fr", "fr-FR", "Français", "EUR", "fr-FR", "shop-fr.example.com", "", "mentions-legales", "eu-west"),
    ("en", "en", "English", "GBP", "en-GB", "shop-uk.example.com", "", "legal-notice", "uk-south"),
    ("it", "it", "Italiano", "EUR", "it-IT", "shop-it.example.com", "", "note-legali", "eu-west"),
    ("es", "es", "Español", "EUR", "es-ES", "shop-es.example.com", "/es", "aviso-legal", "eu-west"),
    ("de", "de", "Deutsch", "EUR", "de-DE", "shop-de.example.com", "", "impressum", "eu-central"),
    ("be-nl", "nl", "Nederlands (België)", "EUR", "nl-BE", "shop-be.example.com", "/nl", "wettelijke-vermeldingen", "eu-west"),
    ("be-fr", "fr-BE", "Français (Belgique)", "EUR", "fr-BE", "shop-be.example.com", "/fr", "mentions-legales", "eu-west"),
]
SEED_BUDGETS = {"meta.title": 70, "meta.description": 160, "hero.title": 90, "menu.label": 12,
                "menu.close": 12, "shop.cta": 16, "lang.label": 32, "artist.bio": 600, "story.body": 600}
SEED_PEOPLE = {"owner@example.com": "Maren Holt", "editor@example.com": "Jonas Weber",
               "editor2@example.com": "Priya Anand", "editor3@example.com": "Luca Moretti",
               "translator@example.com": "Sofia Brandt", "legal@example.com": "Camille Roux",
               "legal2@example.com": "Anke de Vries", "merchandiser@example.com": "Tomás Ibarra"}
AGENCY_REASON = "Parallel Studio design pass"
SEED_GRANTS = {"owner@example.com": ("owner", (None,)), "editor@example.com": ("editor", ("fr", "be-nl", "be-fr")),
               "editor2@example.com": ("editor", ("de",)), "translator@example.com": ("translator", ("de", "it", "es")),
               "legal@example.com": ("legal", ("fr", "en", "be-nl")),
               "legal2@example.com": ("legal", ("de", "it", "es", "be-fr")),
               "merchandiser@example.com": ("merchandiser", (None,))}
TYPEFACE = "Roboto Flex"
H1_WIDE = "48px"
H2_WIDE = "64px"
BODY_SIZE = "16px"
CACHE_PARTS = ("public", "max-age=60", "stale-while-revalidate=86400",
               "stale-if-error=604800")
REFERRER_POLICY = "strict-origin-when-cross-origin"
UPLOAD_LIMIT = 5 * 1024 * 1024
GRANT_MAX_DAYS = 90
IDEMPOTENCY_HEADER = "Idempotency-Key"
REQUEST_ID_HEADER = "X-Request-Id"


def base_url() -> str:
    return os.environ["APP_PUBLIC_URL"].rstrip("/")


def api_base() -> str:
    return f"{base_url()}/api/v1"


def describe(response: httpx.Response) -> str:
    return (f"{response.request.method} {response.request.url} -> "
            f"{response.status_code}: {response.text[:400]}")


def token_hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n]


def digits(n: int) -> str:
    return str(uuid.uuid4().int)[:n].rjust(n, "7").replace("0", "7", 1)


def login(email: str, password: str = PASSWORD) -> httpx.Response:
    return httpx.post(f"{api_base()}/auth/login",
                      json={"email": email, "password": password}, timeout=TIMEOUT)


def token_for(email: str, password: str = PASSWORD) -> str:
    response = login(email, password)
    assert response.status_code in OK, f"login for {email} failed: {describe(response)}"
    token = response.json().get("token")
    assert token, f"login for {email} returned no token: {describe(response)}"
    return token


def client_for(token: str | None) -> httpx.Client:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return httpx.Client(base_url=api_base(), timeout=TIMEOUT, headers=headers)


def body(response: httpx.Response):
    if "json" not in response.headers.get("content-type", "") or not response.content.strip():
        return {}
    return response.json()


def reason_of(response: httpx.Response) -> str | None:
    data = body(response)
    return data.get("reason") if isinstance(data, dict) else None


def ok(response: httpx.Response, what: str):
    assert response.status_code in OK, f"{what} failed: {describe(response)}"
    return body(response)


def rows(response: httpx.Response, what: str) -> list:
    data = ok(response, what)
    assert isinstance(data, list), f"{what} must return a top-level array: {data!r}"
    return data


def refused(response: httpx.Response, what: str, reason: str | None = None) -> None:
    assert 400 <= response.status_code < 500, \
        f"{what} must be refused as a client error: {describe(response)}"
    if reason is not None:
        assert reason_of(response) == reason, \
            f"{what} must carry the reason {reason!r}: {describe(response)}"


def absent(response: httpx.Response, what: str) -> None:
    assert response.status_code == 404, f"{what} must answer as not found: {describe(response)}"


def page_get(path: str, **kwargs) -> httpx.Response:
    return httpx.get(f"{base_url()}{path}", timeout=TIMEOUT, **kwargs)


def html_of(path: str) -> str:
    response = page_get(path, follow_redirects=True)
    assert response.status_code == 200, f"{path} must render: {describe(response)}"
    return response.text


def normalise_space(text: str) -> str:
    return re.sub(r"[\s   ]+", " ", text or "").strip()


def visible_text(html: str) -> str:
    stripped = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    return normalise_space(re.sub(r"<[^>]+>", " ", stripped))


def attrs_of(tag: str) -> dict:
    return {m.group(1).lower(): m.group(3) if m.group(3) is not None else m.group(4)
            for m in re.finditer(r'([\w:-]+)\s*=\s*("([^"]*)"|\'([^\']*)\')', tag)}


def tags(html: str, name: str) -> list:
    return [attrs_of(m.group(0)) for m in re.finditer(rf"<{name}\b[^>]*>", html, re.I)]


def meta_content(html: str, name: str) -> str | None:
    for attrs in tags(html, "meta"):
        if attrs.get("name") == name or attrs.get("property") == name:
            return attrs.get("content")
    return None


def title_of(html: str) -> str:
    found = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    return normalise_space(found.group(1)) if found else ""


def link_path(href: str) -> str:
    return urlparse(href).path if href else ""


def parsed_link(url: str) -> tuple:
    parsed = urlparse(url)
    query = {k: v[0] for k, v in parse_qs(parsed.query, keep_blank_values=True).items()}
    return parsed.scheme, parsed.netloc, unquote(parsed.path), query


def expected_link(market: str, product: str, model: str, slot: str,
                  campaign: str = AFTERGLOW) -> tuple:
    return ("https", HOST[market], f"{SEGMENT[market]}/p/*/_/R-p-{product}",
            {"mc": model, ATTRIBUTION_PARAM: f"{ATTRIBUTION_PREFIX}{campaign}_{slot}",
             "type": ATTRIBUTION_PARAM})


def public_payload(campaign: str, market: str) -> dict:
    response = httpx.get(f"{api_base()}/public/campaigns/{campaign}/markets/{market}",
                         timeout=TIMEOUT)
    return ok(response, f"public payload for {campaign} {market}")


def market_of(session: httpx.Client, campaign: str, market: str) -> dict:
    return ok(session.get(f"/campaigns/{campaign}/markets/{market}"),
              f"reading {campaign} {market}")


def etag_of(session: httpx.Client, campaign: str, market: str) -> str:
    response = session.get(f"/campaigns/{campaign}/markets/{market}")
    ok(response, f"reading {campaign} {market}")
    tag = response.headers.get("etag")
    assert tag, f"reading a market must return an ETag: {describe(response)}"
    return tag


def translations_of(session: httpx.Client, campaign: str, market: str) -> dict:
    listed = rows(session.get(f"/campaigns/{campaign}/translations",
                              params={"market": market}),
                  f"translations of {campaign} {market}")
    return {row["key"]: row for row in listed}


def write_translation(session: httpx.Client, campaign: str, market: str, key: str,
                      value: str, status: str = "reviewed") -> httpx.Response:
    return session.put(f"/campaigns/{campaign}/translations/{market}/{key}",
                       json={"value": value, "status": status})


def probe_value(key: str, market: str, marker: str) -> str:
    return f"{key} {market} {marker}"


def translate_market(session: httpx.Client, campaign: str, market: str, marker: str,
                     status: str = "reviewed", keys=BASE_KEYS) -> None:
    for key in keys:
        ok(write_translation(session, campaign, market, key,
                             probe_value(key, market, marker), status),
           f"translating {key} in {market}")


def create_campaign(session: httpx.Client, **extra) -> dict:
    slug = f"probe-{token_hex(10)}"
    payload = {"slug": slug, "name": f"Probe {slug[-6:]}", "default_locale": "fr",
               "attribution_slug": slug}
    payload.update(extra)
    created = ok(session.post("/campaigns", json=payload), "creating a probe campaign")
    created.setdefault("slug", slug)
    return created


def submit(session: httpx.Client, campaign: str, market: str) -> httpx.Response:
    return session.post(f"/campaigns/{campaign}/markets/{market}/submit", json={})


def approve(session: httpx.Client, campaign: str, market: str, kind: str,
            decision: str = "approved") -> httpx.Response:
    return session.post(f"/campaigns/{campaign}/markets/{market}/approvals",
                        json={"kind": kind, "decision": decision, "comment": "probe"})


def publish(session: httpx.Client, campaign: str, market: str,
            key: str | None = None) -> httpx.Response:
    headers = {IDEMPOTENCY_HEADER: key} if key else {}
    return session.post(f"/campaigns/{campaign}/markets/{market}/publish", json={},
                        headers=headers)


def unpublish(session: httpx.Client, campaign: str, market: str) -> httpx.Response:
    return session.post(f"/campaigns/{campaign}/markets/{market}/unpublish", json={})


def rollback(session: httpx.Client, campaign: str, market: str) -> httpx.Response:
    return session.post(f"/campaigns/{campaign}/markets/{market}/rollback", json={})


def approve_both(owner: httpx.Client, campaign: str, market: str) -> dict:
    with client_for(token_for(LEGAL_GRANTEE[market])) as legal:
        ok(approve(legal, campaign, market, "legal"), f"legal approval of {market}")
    ok(approve(owner, campaign, market, "owner"), f"owner approval of {market}")
    return market_of(owner, campaign, market)


def ready_market(owner: httpx.Client, campaign: str, market: str, marker: str) -> dict:
    translate_market(owner, campaign, market, marker)
    ok(submit(owner, campaign, market), f"submitting {market}")
    state = approve_both(owner, campaign, market)
    assert state.get("status") == "approved", f"{market} must be approved: {state}"
    return state


def live_market(owner: httpx.Client, campaign: str, market: str, marker: str) -> dict:
    ready_market(owner, campaign, market, marker)
    return ok(publish(owner, campaign, market), f"publishing {market}")


def create_product(session: httpx.Client, campaign: str, colourways: int = 1) -> dict:
    payload = {"commerce_product_id": digits(6),
               "colourways": [{"model_code": digits(7), "swatch_hex": "#3a6ea5"}
                              for _ in range(colourways)]}
    return ok(session.post(f"/campaigns/{campaign}/products", json=payload),
              "creating a probe product")


def set_price(session: httpx.Client, product_id, market: str, **fields) -> httpx.Response:
    return session.put(f"/products/{product_id}/markets/{market}", json=fields)


def audit_events(session: httpx.Client, **filters) -> list:
    return rows(session.get("/audit", params=filters), "reading the audit log")


def png_bytes(marker: str | None = None) -> bytes:
    marker = marker or token_hex(12)
    width, height = 4, 4
    raw = b"".join(b"\x00" + bytes([int(marker[i % len(marker)], 16) * 16, 90, 140]) * width
                   for i in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"tEXt", b"Comment\x00" + marker.encode())
            + chunk(b"IDAT", zlib.compress(raw))
            + chunk(b"IEND", b""))


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def upload(session: httpx.Client, campaign: str, data: bytes, name: str,
           market: str | None = None) -> httpx.Response:
    fields = {"market_code": market} if market else {}
    return session.post(f"/campaigns/{campaign}/assets",
                        files={"file": (name, data, "application/octet-stream")},
                        data=fields)


def store_client():
    return capabilities.make_store()._client


def store_object(key: str) -> bytes:
    found = store_client().get_object(Bucket=os.environ["STORAGE_BUCKET"], Key=key)
    return found["Body"].read()


def iso_in(seconds: float) -> str:
    moment = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def days_until(epoch_seconds: float) -> float:
    return (epoch_seconds - time.time()) / 86400


def parse_colour(value: str) -> tuple:
    numbers = [float(n) for n in re.findall(r"[\d.]+", value or "")]
    return tuple(int(round(n)) for n in numbers[:3]) if len(numbers) >= 3 else (-1, -1, -1)


def hex_colour(value: str) -> tuple:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def contrast_ratio(front: tuple, back: tuple) -> float:
    def channel(value):
        value = value / 255.0
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    def luminance(colour):
        r, g, b = (channel(c) for c in colour[:3])
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    first, second = luminance(front), luminance(back)
    return (max(first, second) + 0.05) / (min(first, second) + 0.05)


def sign_in_page(page, email: str, password: str = PASSWORD) -> None:
    page.goto(f"{base_url()}/studio/login")
    page.get_by_label("Email", exact=True).fill(email)
    page.get_by_label("Password", exact=True).fill(password)
    page.get_by_role("button", name="Sign in", exact=True).click()
    page.wait_for_url(lambda url: "/studio/login" not in url, timeout=20000)


@pytest.fixture(scope="session")
def backend():
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store():
    return capabilities.make_store()


@pytest.fixture()
def owner():
    with client_for(token_for(OWNER)) as session:
        yield session


@pytest.fixture()
def editor():
    with client_for(token_for(EDITOR)) as session:
        yield session


@pytest.fixture()
def translator():
    with client_for(token_for(TRANSLATOR)) as session:
        yield session


@pytest.fixture()
def legal():
    with client_for(token_for(LEGAL)) as session:
        yield session


@pytest.fixture()
def merchandiser():
    with client_for(token_for(MERCHANDISER)) as session:
        yield session


@pytest.fixture()
def anon():
    with client_for(None) as session:
        yield session


@pytest.fixture()
def campaign(owner):
    """A fresh probe campaign: eleven strings, seven draft markets, nothing live."""
    return create_campaign(owner)["slug"]


@pytest.fixture()
def revoke_after(owner):
    """Grants a test issued, revoked afterwards so the seeded grant set returns."""
    issued: list = []
    yield issued
    for grant_id in issued:
        owner.delete(f"/grants/{grant_id}")


@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        chromium = pw.chromium.launch()
        yield chromium
        chromium.close()


@pytest.fixture()
def page(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 900},
                                  locale="en-GB")
    tab = context.new_page()
    yield tab
    context.close()


@pytest.fixture()
def narrow_page(browser):
    context = browser.new_context(viewport={"width": 390, "height": 844}, locale="fr-FR",
                                  has_touch=True, is_mobile=True)
    tab = context.new_page()
    yield tab
    context.close()


@pytest.fixture()
def calm_page(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 900},
                                  reduced_motion="reduce", locale="fr-FR")
    tab = context.new_page()
    yield tab
    context.close()


def settle(seconds: float = 0.5) -> None:
    time.sleep(seconds)
