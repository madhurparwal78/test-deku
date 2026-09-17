"""Task fixtures for deku/ugc-game-platform-vb.

Implementation agnostic: nothing here assumes the agent's framework, file
layout, ORM or module names. The only assumptions are the App Contract and what
instruction.md pinned literally, which is the route set, the `access_token`
login key, the seeded accounts, the seeded packs, items and experiences, the
table names of `## Data model`, and the two pinned email subject prefixes.

Provider agnostic: every domain helper is composed from the generic primitives
in capabilities.py, never from a provider SDK. Swapping the backend, email or
payments slot replaces an adapter rather than this file.
"""

from __future__ import annotations

import os
import re
import time

import pytest
from _shapes import items
from appclient import api_base, client, login, seeded_password
from capabilities import Backend, Inbox, Payments, make_backend, make_inbox, make_payments

SETTLE_SECONDS = 2.0
POLL_DEADLINE_SECONDS = 30.0
POLL_INTERVAL_SECONDS = 0.5

CORPUS_PASSWORD = "deku-demo-pw-2026"

PLAYER_EMAIL = "player@example.com"
PLAYER2_EMAIL = "player2@example.com"
PLAYER3_EMAIL = "player3@example.com"
CREATOR_EMAIL = "creator@example.com"
CREATOR2_EMAIL = "creator2@example.com"

PLAYER_USERNAME = "Nova Pilot"
PLAYER2_USERNAME = "Tiny Comet"
PLAYER3_USERNAME = "Edge Case"
CREATOR_USERNAME = "Vale Studio"
CREATOR2_USERNAME = "Hollow Forge"

PLAYER_EXTERNAL_KEY = "kavora-nova-pilot"

STARTER_PACK = "starter-pack"
BUILDER_PACK = "builder-pack"
STUDIO_PACK = "studio-pack"
BUILDER_PACK_NAME = "Builder Pack"
BUILDER_PACK_KREDZ = 1000
BUILDER_PACK_PRICE_MINOR = 1000
STARTER_PACK_KREDZ = 400
STARTER_PACK_PRICE_MINOR = 500
STUDIO_PACK_KREDZ = 2400
STUDIO_PACK_PRICE_MINOR = 2000

AURORA_VISOR = "aurora-visor"
NEBULA_GLIDER = "nebula-glider"
COPPER_HOVERBOARD = "copper-hoverboard"
MERIDIAN_BANNER = "meridian-banner"
VAULT_KEY = "vault-key"

AURORA_VISOR_KREDZ = 75
AURORA_VISOR_PLATFORM_KREDZ = 22
AURORA_VISOR_CREATOR_KREDZ = 53
COPPER_HOVERBOARD_KREDZ = 3
NEBULA_GLIDER_KREDZ = 250
VAULT_KEY_KREDZ = 400

PLAYER_SEED_BALANCE = 1000
PLAYER2_SEED_BALANCE = 500
PLAYER3_SEED_BALANCE = 75

SKY_FORGE_ARENA = "sky-forge-arena"
DEEP_VAULT_HEIST = "deep-vault-heist"
LANTERN_DRIFT = "lantern-drift"
SKY_FORGE_CAPACITY = 8

SPLIT_RATE_VERSION = 1
PLATFORM_NUMERATOR = 30
PLATFORM_DENOMINATOR = 100
MINIMUM_PAYOUT_KREDZ = 100
DEFAULT_PAGE_LIMIT = 20
RESERVATION_TTL_SECONDS = 120
PRESENCE_LEASE_SECONDS = 60
ONE_TIME_CODE_TTL_SECONDS = 600
MIN_PASSWORD_LENGTH = 8
CHILD_THRESHOLD_YEARS = 13
ADULT_THRESHOLD_YEARS = 18
ENGAGEMENT_WINDOW_DAYS = 30

RECEIPT_SUBJECT_PREFIX = "Kredz receipt:"
SIGN_IN_SUBJECT_PREFIX = "Kavora sign-in code:"

CHILD_BAND = "child"
TEEN_BAND = "teen"
ADULT_BAND = "adult"

TAX_DOCUMENTS_CONDITION = "tax_documents"
AGE_BAND_CONDITION = "age_band"

PENDING_MODERATION = "pending_moderation"
PUBLISHED = "published"
PREVIEW_PENDING = "pending"
PREVIEW_BLOCKED = "blocked"

MALWARE_MARKER = "EICAR-STANDARD-ANTIVIRUS-TEST-FILE"
DECOY_FIELD = "nickname_confirm"

SEARCH_SCOPES = ("games", "marketplace", "communities", "creator_store")

REFUSED_STATUSES = (400, 403, 409, 422)
DENIED_STATUSES = (401, 403, 404)
OK_STATUSES = (200, 201)

_CODE_RE = re.compile(r"\b(\d{6})\b")


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """The one sanctioned sleep: give an unwanted side effect a fair chance to land."""
    time.sleep(seconds)


def today_utc() -> str:
    """The single pinned clock read, in UTC, as an ISO date string."""
    import datetime

    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def years_ago_utc(years: int, month: int = 6, day: int = 15) -> str:
    """A birth date `years` before today, on a fixed month and day."""
    import datetime

    now = datetime.datetime.now(datetime.timezone.utc).date()
    return datetime.date(now.year - years, month, day).isoformat()


def probe_email() -> str:
    return "probe-" + os.urandom(6).hex() + "@example.com"


def probe_key() -> str:
    return "probe-" + os.urandom(8).hex()


def poll_until(predicate, deadline_seconds: float = POLL_DEADLINE_SECONDS):
    """Poll a predicate to a monotonic deadline. Returns the last value seen."""
    limit = time.monotonic() + deadline_seconds
    seen = None
    while time.monotonic() < limit:
        seen = predicate()
        if seen:
            return seen
        settle(POLL_INTERVAL_SECONDS)
    return seen


def body_excerpt(response) -> str:
    return response.text[:400]


def as_list(payload) -> list:
    return items(payload)


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


def _token(email: str) -> str:
    return login(email, seeded_password("SEED_PASSWORD", CORPUS_PASSWORD))


@pytest.fixture()
def player_client():
    with client(_token(PLAYER_EMAIL)) as c:
        yield c


@pytest.fixture()
def player2_client():
    with client(_token(PLAYER2_EMAIL)) as c:
        yield c


@pytest.fixture()
def player3_client():
    with client(_token(PLAYER3_EMAIL)) as c:
        yield c


@pytest.fixture()
def creator_client():
    with client(_token(CREATOR_EMAIL)) as c:
        yield c


@pytest.fixture()
def creator2_client():
    with client(_token(CREATOR2_EMAIL)) as c:
        yield c


def fresh_client(email: str):
    return client(_token(email))


class KavoraStore:
    """Domain queries composed from the generic capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def identity_by_email(self, email: str) -> dict | None:
        return self._b.one("identities", email=email)

    def count_identities(self, email: str) -> int:
        return self._b.count("identities", email=email)

    def sessions_for(self, identity_id) -> list[dict]:
        return self._b.rows("sessions", identity_id=identity_id)

    def acceptances(self, identity_id) -> list[dict]:
        return self._b.rows("agreement_acceptances", identity_id=identity_id)

    def accounts_of_kind(self, kind: str) -> list[dict]:
        return self._b.rows("accounts", kind=kind)

    def account_for(self, owner_id, kind: str) -> dict | None:
        return self._b.one("accounts", owner_id=owner_id, kind=kind)

    def transaction_by_key(self, key: str) -> dict | None:
        return self._b.one("ledger_transactions", idempotency_key=key)

    def count_transactions_by_key(self, key: str) -> int:
        return self._b.count("ledger_transactions", idempotency_key=key)

    def transactions_of_type(self, kind: str) -> list[dict]:
        return self._b.rows("ledger_transactions", type=kind)

    def entries_for(self, transaction_id) -> list[dict]:
        return self._b.rows("ledger_entries", transaction_id=transaction_id)

    def entries_for_account(self, account_id) -> list[dict]:
        return self._b.rows("ledger_entries", account_id=account_id)

    def all_entries(self) -> list[dict]:
        return self._b.rows("ledger_entries")

    def billing_account(self, external_key: str) -> dict | None:
        return self._b.one("billing_accounts", external_key=external_key)

    def count_billing_accounts(self, external_key: str) -> int:
        return self._b.count("billing_accounts", external_key=external_key)

    def item_by_slug(self, slug: str) -> dict | None:
        return self._b.one("items", slug=slug)

    def item_versions(self, item_id) -> list[dict]:
        return self._b.rows("item_versions", item_id=item_id)

    def sales_for_item(self, item_id) -> list[dict]:
        return self._b.rows("sales", item_id=item_id)

    def all_sales(self) -> list[dict]:
        return self._b.rows("sales")

    def payout_requests_for(self, creator_id) -> list[dict]:
        return self._b.rows("payout_requests", creator_id=creator_id)

    def asset_by_id(self, asset_id) -> dict | None:
        return self._b.one("assets", id=asset_id)

    def previews_for(self, asset_id) -> list[dict]:
        return self._b.rows("asset_previews", asset_id=asset_id)

    def experience_by_slug(self, slug: str) -> dict | None:
        return self._b.one("experiences", slug=slug)

    def instances_for(self, experience_id) -> list[dict]:
        return self._b.rows("instances", experience_id=experience_id)

    def reservations_for(self, instance_id) -> list[dict]:
        return self._b.rows("reservations", instance_id=instance_id)

    def presences_for(self, instance_id) -> list[dict]:
        return self._b.rows("presences", instance_id=instance_id)

    def packs(self) -> list[dict]:
        return self._b.rows("currency_packs")

    def split_rate(self, version) -> dict | None:
        return self._b.one("split_rates", version=version)

    def sum_entries(self, rows: list[dict]) -> int:
        total = 0
        for row in rows:
            total += int(row.get("amount", 0))
        return total


@pytest.fixture(scope="session")
def store() -> KavoraStore:
    return KavoraStore(make_backend())


@pytest.fixture(scope="session")
def inbox() -> Inbox:
    return make_inbox()


@pytest.fixture(scope="session")
def payments() -> Payments:
    return make_payments()


def wait_for_email(inbox_handle: Inbox, address: str, subject_contains: str):
    """Bounded poll for a message, routed through settle()."""
    return poll_until(lambda: inbox_handle.find(address, subject_contains))


def wait_for_invoice(payments_handle: Payments, amount_minor: int, currency: str = "usd"):
    """Bounded poll for an invoice of an exact amount, routed through settle()."""
    return poll_until(lambda: payments_handle.find_charge(amount_minor, currency))


def extract_code(text: str) -> str:
    match = _CODE_RE.search(text or "")
    return match.group(1) if match else ""


def signup_payload(date_of_birth: str, username: str, email: str,
                   password: str = CORPUS_PASSWORD) -> dict:
    return {
        "date_of_birth": date_of_birth,
        "username": username,
        "email": email,
        "password": password,
    }


def signup(anon, payload: dict):
    return anon.post("/auth/signup", json=payload)


def first_instance_id(store_handle: KavoraStore, slug: str):
    experience = store_handle.experience_by_slug(slug)
    assert experience is not None, (
        "seeded experience " + slug + " is missing from the experiences table"
    )
    rows = store_handle.instances_for(experience.get("id"))
    assert rows, "experience " + slug + " has no seeded instance row"
    return rows[0].get("id")
