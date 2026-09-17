"""Capability adapters — the design move that makes the service matrix affordable.

PLAN.md 3.3: workflows and pytest substeps are written **once per capability, not
once per provider**. A substep asserts `inbox.find(to=..., subject_contains=...)`
and runs unchanged against Mailpit, MailHog or Inbucket. The **assertion** is
capability-level; only the **adapter** is provider-specific, and it lives here.

Without this, 11 slots x N providers fragments the verifier into hundreds of
bespoke test files and the matrix costs more than it returns.

Only adapters an authored task actually selects are implemented. Add a provider
when a task selects it, not before.

Provider selection comes from `[metadata.services]` in task.toml, surfaced to the
verifier as `DEKU_SERVICE_<SLOT>` environment variables.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

TIMEOUT = 30.0


class InfrastructureUnavailable(RuntimeError):
    """Backing service is unreachable or refused our credentials.

    Raised by adapters so pytest surfaces the failure as a harness/infrastructure
    fault, not an app-quality failure. If this bubbles up as a bare AssertionError
    the agent gets billed for a sidecar the harness never brought up.
    """


def selected(slot: str) -> str:
    """Provider chosen for a slot, from task.toml [metadata.services]."""
    key = f"DEKU_SERVICE_{slot.upper()}"
    provider = os.environ.get(key)
    if not provider:
        raise RuntimeError(
            f"slot {slot!r} is not selected for this task: {key} is unset. "
            f"A test may only use a capability the task declares in "
            f"[metadata.services]."
        )
    return provider


# =============================================================== backend / BaaS


class Backend:
    """Generic persisted-state primitives.

    Deliberately narrow: `count`, `rows`, `one`. Domain queries ("employees with
    no active seat") belong in a task's conftest.py, composed from these. That is
    the seam that keeps the adapter provider-swappable while task assertions stay
    readable.
    """

    def count(self, table: str, **where: Any) -> int:
        raise NotImplementedError

    def rows(self, table: str, limit: int | None = None, **where: Any) -> list[dict]:
        raise NotImplementedError

    def one(self, table: str, **where: Any) -> dict | None:
        found = self.rows(table, limit=1, **where)
        return found[0] if found else None


class PostgresBackend(Backend):
    def __init__(self, dsn: str) -> None:
        import psycopg  # imported here so tasks not using postgres need no driver

        self._psycopg = psycopg
        self._dsn = dsn

    def query(self, sql: str, params: tuple = ()) -> list[dict]:
        with self._psycopg.connect(self._dsn) as conn, conn.cursor() as cur:
            cur.execute(sql, params)
            if cur.description is None:
                return []
            columns = [column.name for column in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]

    def _where(self, where: dict) -> tuple[str, tuple]:
        if not where:
            return "", ()
        clause = " AND ".join(f"{key} = %s" for key in where)
        return f" WHERE {clause}", tuple(where.values())

    def count(self, table: str, **where: Any) -> int:
        clause, params = self._where(where)
        return self.query(f"SELECT count(*) AS n FROM {table}{clause}", params)[0]["n"]

    def rows(self, table: str, limit: int | None = None, **where: Any) -> list[dict]:
        clause, params = self._where(where)
        sql = f"SELECT * FROM {table}{clause} ORDER BY id"
        if limit:
            sql += f" LIMIT {int(limit)}"
        return self.query(sql, params)


class PocketBaseBackend(Backend):
    """PocketBase exposes collections over REST; the admin token is the escape hatch.

    `credential` is either a ready-made admin token or, more usefully,
    `email:password`. PocketBase mints admin tokens at runtime and expires them,
    so a token cannot be baked into task.toml ahead of time -- the credential
    pair is the only thing stable enough to declare. Exchange happens here so no
    task's conftest has to know PocketBase's auth endpoint.
    """

    def __init__(self, base_url: str, credential: str) -> None:
        base_url = base_url.rstrip("/")
        token = credential
        if ":" in credential and not credential.startswith("ey"):
            identity, password = credential.split(":", 1)
            try:
                response = httpx.post(
                    f"{base_url}/api/admins/auth-with-password",
                    json={"identity": identity, "password": password},
                    timeout=TIMEOUT,
                )
            except httpx.HTTPError as exc:
                raise InfrastructureUnavailable(
                    f"PocketBase sidecar at {base_url} unreachable "
                    f"({exc.__class__.__name__}: {exc}); this is a harness/"
                    f"infrastructure fault, not an app fault"
                ) from exc
            if response.status_code != 200:
                raise InfrastructureUnavailable(
                    f"PocketBase admin auth for {identity!r} at {base_url} "
                    f"returned {response.status_code}: {response.text[:300]}; "
                    f"this is a harness/infrastructure fault "
                    f"(sidecar down or wrong credentials), not an app fault"
                )
            token = response.json()["token"]
        self._client = httpx.Client(
            base_url=base_url,
            timeout=TIMEOUT,
            headers={"Authorization": token},
        )

    def _fetch(self, table: str, where: dict, per_page: int) -> dict:
        params: dict[str, Any] = {"perPage": per_page}
        if where:
            params["filter"] = " && ".join(f'{k}="{v}"' for k, v in where.items())
        response = self._client.get(f"/api/collections/{table}/records", params=params)
        assert response.status_code == 200, (
            f"PocketBase {table} query returned {response.status_code}: "
            f"{response.text[:300]}"
        )
        return response.json()

    def count(self, table: str, **where: Any) -> int:
        return int(self._fetch(table, where, per_page=1).get("totalItems", 0))

    def rows(self, table: str, limit: int | None = None, **where: Any) -> list[dict]:
        return self._fetch(table, where, per_page=limit or 200).get("items", [])


def make_backend() -> Backend:
    provider = selected("backend")
    if provider == "postgres":
        return PostgresBackend(os.environ["DB_ADMIN_URL"])
    if provider == "pocketbase":
        return PocketBaseBackend(
            os.environ["BACKEND_URL"], os.environ["BACKEND_ADMIN_KEY"]
        )
    raise RuntimeError(f"no backend adapter for provider {provider!r}")


# ========================================================================= email


@dataclass(frozen=True)
class Message:
    to: list[str]
    subject: str
    body: str


class Inbox:
    def find(self, to: str, subject_contains: str = "") -> Message | None:
        raise NotImplementedError

    def count(self, to: str | None = None) -> int:
        raise NotImplementedError


class HttpInbox(Inbox):
    """Mailpit and MailHog both expose a JSON inbox API; the shapes differ slightly."""

    def __init__(self, base_url: str, provider: str) -> None:
        self._provider = provider
        self._client = httpx.Client(base_url=base_url.rstrip("/"), timeout=TIMEOUT)

    def _messages(self) -> list[Message]:
        if self._provider == "mailpit":
            payload = self._client.get("/api/v1/messages", params={"limit": 200}).json()
            return [
                Message(
                    to=[addr.get("Address", "") for addr in item.get("To", [])],
                    subject=item.get("Subject", ""),
                    body=item.get("Snippet", ""),
                )
                for item in payload.get("messages", [])
            ]
        payload = self._client.get("/api/v2/messages", params={"limit": 200}).json()
        messages = []
        for item in payload.get("items", []):
            headers = item.get("Content", {}).get("Headers", {})
            messages.append(
                Message(
                    to=headers.get("To", []),
                    subject=" ".join(headers.get("Subject", [])),
                    body=item.get("Content", {}).get("Body", ""),
                )
            )
        return messages

    def find(self, to: str, subject_contains: str = "") -> Message | None:
        needle = subject_contains.lower()
        for message in self._messages():
            if any(to.lower() in addr.lower() for addr in message.to) and (
                needle in message.subject.lower()
            ):
                return message
        return None

    def count(self, to: str | None = None) -> int:
        messages = self._messages()
        if to is None:
            return len(messages)
        return sum(
            1
            for message in messages
            if any(to.lower() in addr.lower() for addr in message.to)
        )


def make_inbox() -> Inbox:
    provider = selected("email")
    if provider in ("mailpit", "mailhog"):
        return HttpInbox(os.environ["EMAIL_INBOX_API_URL"], provider)
    raise RuntimeError(f"no inbox adapter for provider {provider!r}")


# ====================================================================== payments


@dataclass(frozen=True)
class Charge:
    id: str
    amount: int
    currency: str
    status: str
    metadata: dict


class Payments:
    def charges(self) -> list[Charge]:
        raise NotImplementedError

    def find_charge(
        self, amount: int, currency: str = "usd", status: str | None = None
    ) -> Charge | None:
        for charge in self.charges():
            if charge.amount != amount or charge.currency.lower() != currency.lower():
                continue
            if status and charge.status != status:
                continue
            return charge
        return None

    def refunds_for(self, charge_id: str) -> list[dict]:
        raise NotImplementedError


class KillBillPayments(Payments):
    """killbill: Kill Bill, the subscription-billing platform (reference/K K.4).

    A real product with real persisted state the agent must integrate and cannot
    control, which is what keeps the no-mocks rule enforceable.

    A "charge" here is an INVOICE read back from `/1.0/kb/invoices/pagination`.
    Kill Bill is a billing platform, not a card processor: it has no charge object
    and no test-card semantics. That is a deliberate narrowing of what the payments
    slot can assert, recorded in reference/K K.4 -- the observable is "an invoice
    exists on this account for this amount", not "a card was charged".

    Only the endpoints reference/K K.4 documents are called. Kill Bill's wider API
    exists, but an endpoint this kit has not verified against the running service is
    an INVENTED-FACT waiting to happen, so `refunds_for` raises rather than guessing
    a refunds route.

    Amounts: Kill Bill reports a decimal `amount` (29.00) while `Charge.amount` is
    integer MINOR units, so the value is scaled by 100 and rounded. Currency codes
    come back uppercase; `find_charge` already compares case-insensitively.
    """

    def __init__(self, base_url: str, api_key: str, api_secret: str,
                 user: str, password: str) -> None:
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=TIMEOUT,
            auth=(user, password),
            headers={
                "X-Killbill-ApiKey": api_key,
                "X-Killbill-ApiSecret": api_secret,
            },
        )

    def charges(self) -> list[Charge]:
        response = self._client.get("/1.0/kb/invoices/pagination")
        assert response.status_code == 200, (
            f"killbill /1.0/kb/invoices/pagination returned "
            f"{response.status_code}: {response.text[:300]}"
        )
        payload = response.json()
        items = payload if isinstance(payload, list) else payload.get("items", [])
        charges = []
        for item in items:
            try:
                minor = int(round(float(item.get("amount", 0)) * 100))
            except (TypeError, ValueError):
                minor = 0
            charges.append(
                Charge(
                    id=str(item.get("invoiceId", "")),
                    amount=minor,
                    currency=str(item.get("currency", "USD")),
                    status=str(item.get("status", "")),
                    metadata=item,
                )
            )
        return charges

    def accounts(self) -> list[dict]:
        """Seeded accounts, by externalKey. The identity a brief pins."""
        response = self._client.get("/1.0/kb/accounts/pagination")
        assert response.status_code == 200, (
            f"killbill /1.0/kb/accounts/pagination returned "
            f"{response.status_code}: {response.text[:300]}"
        )
        payload = response.json()
        return payload if isinstance(payload, list) else payload.get("items", [])

    def refunds_for(self, charge_id: str) -> list[dict]:
        raise RuntimeError(
            "killbill: refunds are not part of the payments surface reference/K "
            "K.4 documents, so this adapter will not guess a route for them. A "
            "task that needs a refund observation needs K.4 extended against the "
            "running service first -- see reference/K K.4 'what is deliberately "
            "absent'."
        )


def make_payments() -> Payments:
    provider = selected("payments")
    if provider == "killbill":
        return KillBillPayments(
            os.environ["PAYMENTS_API_URL"],
            os.environ["PAYMENTS_API_KEY"],
            os.environ["PAYMENTS_API_SECRET"],
            os.environ["PAYMENTS_ADMIN_USER"],
            os.environ["PAYMENTS_ADMIN_PASSWORD"],
        )
    raise RuntimeError(f"no payments adapter for provider {provider!r}")


# ================================================================ object storage


class ObjectStore:
    def exists(self, key: str) -> bool:
        raise NotImplementedError

    def list(self, prefix: str = "") -> list[str]:
        raise NotImplementedError


class S3Store(ObjectStore):
    """MinIO, SeaweedFS, Garage and LocalStack are all S3-compatible -> one adapter."""

    def __init__(self, endpoint: str, bucket: str, access_key: str, secret_key: str) -> None:
        import boto3

        self._bucket = bucket
        self._client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def list(self, prefix: str = "") -> list[str]:
        pages = self._client.get_paginator("list_objects_v2").paginate(
            Bucket=self._bucket, Prefix=prefix
        )
        return [obj["Key"] for page in pages for obj in page.get("Contents", [])]

    def exists(self, key: str) -> bool:
        from botocore.exceptions import ClientError

        try:
            self._client.head_object(Bucket=self._bucket, Key=key)
            return True
        except ClientError:
            return False


def make_store() -> ObjectStore:
    provider = selected("storage")
    if provider in ("minio", "seaweedfs", "garage", "localstack"):
        return S3Store(
            os.environ["STORAGE_ENDPOINT"],
            os.environ["STORAGE_BUCKET"],
            os.environ["STORAGE_ACCESS_KEY"],
            os.environ["STORAGE_SECRET_KEY"],
        )
    raise RuntimeError(f"no object-store adapter for provider {provider!r}")
