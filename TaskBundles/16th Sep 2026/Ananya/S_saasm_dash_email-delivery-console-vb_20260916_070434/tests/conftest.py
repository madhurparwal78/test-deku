"""Task fixtures for deku/email-delivery-console-vb.

Implementation agnostic: nothing here assumes the framework, the file layout, an
ORM or a module name. What it assumes is the App Contract and whatever
instruction.md pinned - the route shapes, the access_token login key, the seeded
accounts, the table names, the message states and the reserved relay addresses.

Provider agnostic: the domain helpers are composed from the generic primitives in
capabilities.py, never from a provider SDK. Swapping the backend or the email slot
replaces an adapter rather than this file.
"""

from __future__ import annotations

import os
import time

import pytest
from appclient import api_base, app_url, client, login, seeded_password
from capabilities import Backend, Inbox, make_backend, make_inbox

SETTLE_SECONDS = 2.0


def settle(seconds: float = SETTLE_SECONDS) -> None:
    """Give an unwanted async side effect time to land before asserting it did not."""
    time.sleep(seconds)


OWNER_EMAIL = "owner@example.com"
ADMIN_EMAIL = "admin@example.com"
MEMBER_EMAIL = "member@example.com"
OTHER_OWNER_EMAIL = "owner2@example.com"
SEEDED_PASSWORD = "deku-demo-pw-2026"

WORKSPACE_NAME = "Northwind Relay"
OTHER_WORKSPACE_NAME = "Acme Relay"
VERIFIED_DOMAIN = "mail.northwind.example.com"
PENDING_DOMAIN = "docs.northwind.example.com"
OTHER_DOMAIN = "mail.acme.example.com"
SENDER_ADDRESS = "support@mail.northwind.example.com"

DELIVERED_ADDRESS = "delivered@relay.example.com"
BOUNCED_ADDRESS = "bounced@relay.example.com"
COMPLAINED_ADDRESS = "complained@relay.example.com"

AUDIENCE_NAME = "Launch List"
CREDENTIAL_NAME = "Production sender"
SECRET_PREFIX_OPENER = "skey_"
PLAN_NAME = "starter"
MONTHLY_ALLOWANCE = 500
READY_STATES = ("queued", "sending", "sent", "delivered")
TERMINAL_STATES = ("delivered", "bounced", "complained", "canceled", "rejected")

POLL_INTERVAL = 0.5
POLL_CEILING = 30.0


def poll_until(predicate, ceiling: float = POLL_CEILING):
    """Bounded poll for an asynchronous side effect. Returns the last value seen."""
    deadline = time.monotonic() + ceiling
    value = predicate()
    while not value and time.monotonic() < deadline:
        settle(POLL_INTERVAL)
        value = predicate()
    return value


def unique_local() -> str:
    return f"probe-{os.urandom(6).hex()}"


def unique_address() -> str:
    return f"{unique_local()}@example.com"


def unique_key() -> str:
    return f"key-{os.urandom(8).hex()}"


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture(scope="session")
def owner_token() -> str:
    return login(OWNER_EMAIL, seeded_password("SEED_OWNER_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def owner_client(owner_token: str):
    with client(owner_token) as c:
        yield c


@pytest.fixture(scope="session")
def admin_token() -> str:
    return login(ADMIN_EMAIL, seeded_password("SEED_ADMIN_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def admin_client(admin_token: str):
    with client(admin_token) as c:
        yield c


@pytest.fixture(scope="session")
def member_token() -> str:
    return login(MEMBER_EMAIL, seeded_password("SEED_MEMBER_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def member_client(member_token: str):
    with client(member_token) as c:
        yield c


@pytest.fixture(scope="session")
def other_owner_token() -> str:
    return login(OTHER_OWNER_EMAIL,
                 seeded_password("SEED_OTHER_OWNER_PASSWORD", SEEDED_PASSWORD))


@pytest.fixture(scope="session")
def other_owner_client(other_owner_token: str):
    with client(other_owner_token) as c:
        yield c


class RelayStore:
    """Domain queries for this task, composed from capability primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def user_by_email(self, email: str) -> dict | None:
        return self._b.one("users", email=email)

    def count_users(self, email: str) -> int:
        return self._b.count("users", email=email)

    def workspace_by_name(self, name: str) -> dict | None:
        return self._b.one("workspaces", name=name)

    def memberships(self, workspace_id) -> list[dict]:
        return self._b.rows("memberships", workspace_id=workspace_id)

    def domain_by_name(self, name: str) -> dict | None:
        return self._b.one("domains", name=name)

    def domain_records(self, domain_id) -> list[dict]:
        return self._b.rows("domain_records", domain_id=domain_id)

    def credential_by_name(self, name: str) -> dict | None:
        return self._b.one("credentials", name=name)

    def count_credentials(self, name: str) -> int:
        return self._b.count("credentials", name=name)

    def message_by_id(self, message_id) -> dict | None:
        return self._b.one("messages", id=message_id)

    def messages_for_key(self, key: str) -> list[dict]:
        return self._b.rows("messages", idempotency_key=key)

    def count_messages_for_key(self, key: str) -> int:
        return self._b.count("messages", idempotency_key=key)

    def count_messages_to(self, address: str) -> int:
        return self._b.count("messages", to_address=address)

    def messages_in_state(self, state: str) -> list[dict]:
        return self._b.rows("messages", state=state)

    def count_messages_in_state(self, state: str) -> int:
        return self._b.count("messages", state=state)

    def events_for(self, message_id) -> list[dict]:
        return self._b.rows("message_events", message_id=message_id)

    def suppression_for(self, address: str) -> dict | None:
        return self._b.one("suppressions", address=address)

    def audience_by_name(self, name: str) -> dict | None:
        return self._b.one("audiences", name=name)

    def contacts_in(self, audience_id) -> list[dict]:
        return self._b.rows("contacts", audience_id=audience_id)

    def count_contacts(self, audience_id, email: str) -> int:
        return self._b.count("contacts", audience_id=audience_id, email=email)

    def broadcast_by_id(self, broadcast_id) -> dict | None:
        return self._b.one("broadcasts", id=broadcast_id)

    def count_broadcast_messages(self, broadcast_id) -> int:
        return self._b.count("messages", broadcast_id=broadcast_id)

    def endpoint_by_id(self, endpoint_id) -> dict | None:
        return self._b.one("notification_endpoints", id=endpoint_id)

    def deliveries_for(self, endpoint_id) -> list[dict]:
        return self._b.rows("notification_deliveries", endpoint_id=endpoint_id)

    def usage_rows(self, workspace_id) -> list[dict]:
        return self._b.rows("usage_counters", workspace_id=workspace_id)


@pytest.fixture(scope="session")
def db() -> RelayStore:
    return RelayStore(make_backend())


@pytest.fixture(scope="session")
def inbox() -> Inbox:
    """The mail-server inbox, inspected out of band. Never call smtplib here."""
    return make_inbox()


@pytest.fixture(scope="session")
def browser_context():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as driver:
        browser = driver.chromium.launch()
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        yield context
        context.close()
        browser.close()


@pytest.fixture
def page(browser_context):
    surface = browser_context.new_page()
    yield surface
    surface.close()


def base_url() -> str:
    return app_url()


def api_url() -> str:
    return api_base()


def send_body(to_address: str, subject: str = "Your receipt",
              from_address: str = SENDER_ADDRESS) -> dict:
    return {
        "from": from_address,
        "to": [to_address],
        "subject": subject,
        "html": "<p>Thanks.</p>",
        "text": "Thanks.",
    }


def mint_credential(admin, name: str | None = None, scope: str = "sending",
                    domain_id=None) -> dict:
    payload = {"name": name or f"{CREDENTIAL_NAME} {unique_local()}", "scope": scope}
    if domain_id is not None:
        payload["domain_id"] = domain_id
    response = admin.post("/credentials", json=payload)
    assert response.status_code in (200, 201), (
        f"POST /api/credentials returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    assert body.get("secret"), (
        f"POST /api/credentials returned no secret on creation: {response.text[:400]}"
    )
    return body


def send_as(secret: str, body: dict, key: str | None = None):
    with client(secret) as sender:
        headers = {"Idempotency-Key": key or unique_key()}
        return sender.post("/v1/emails", json=body, headers=headers)


def accepted_id(response) -> str:
    assert response.status_code in (200, 201, 202), (
        f"POST /api/v1/emails returned {response.status_code}: {response.text[:400]}"
    )
    body = response.json()
    identifier = body.get("id")
    assert identifier, f"send response carries no id: {response.text[:400]}"
    return identifier
