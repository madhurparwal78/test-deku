"""Fixtures for the vvvivid task.

Composed from the vendored capability adapters only. Nothing here reads the app's
source; every observation is either an HTTP call against the running app or an
out-of-band read of the same PostgreSQL and object store the app writes to.
"""

from __future__ import annotations

import base64
import hashlib
import itertools
import json
import os
from typing import Any

import pytest

import appclient
import capabilities

CORPUS_PASSWORD = appclient.seeded_password("DEKU_SEED_PASSWORD", "deku-studio-2026")

AUTHOR_EMAIL = "mara@vvvivid.tools"
SECOND_AUTHOR_EMAIL = "tomas@vvvivid.tools"
READER_EMAIL = "visitor@vvvivid.tools"

PUBLIC_PRESET_TITLE = "Soft four-lobe"
SECOND_PUBLIC_PRESET_TITLE = "Three-layer crest"
UNLISTED_PRESET_TITLE = "Tight rule grid"
PRIVATE_PRESET_TITLE = "Dawn wash"

RENDER_PREFIX = "renders/"

_seed_counter = itertools.count(910_000)


@pytest.fixture(scope="session")
def backend() -> capabilities.Backend:
    return capabilities.make_backend()


@pytest.fixture(scope="session")
def store() -> capabilities.ObjectStore:
    return capabilities.make_store()


@pytest.fixture(scope="session")
def author_token() -> str:
    return appclient.login(AUTHOR_EMAIL, CORPUS_PASSWORD)


@pytest.fixture(scope="session")
def second_author_token() -> str:
    return appclient.login(SECOND_AUTHOR_EMAIL, CORPUS_PASSWORD)


@pytest.fixture(scope="session")
def reader_token() -> str:
    return appclient.login(READER_EMAIL, CORPUS_PASSWORD)


@pytest.fixture
def author(author_token):
    with appclient.client(author_token) as c:
        yield c


@pytest.fixture
def second_author(second_author_token):
    with appclient.client(second_author_token) as c:
        yield c


@pytest.fixture
def reader(reader_token):
    with appclient.client(reader_token) as c:
        yield c


@pytest.fixture
def anonymous():
    with appclient.client() as c:
        yield c


def _as_obj(value: Any) -> Any:
    """`params` may arrive as a dict or as a JSON string, depending on driver."""
    if isinstance(value, (str, bytes)):
        return json.loads(value)
    return value


def _fmt_number(value: Any) -> str:
    """Plain decimal, no trailing zeros, no exponent -- the brief's number rule."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if value == int(value):
            return str(int(value))
        return repr(value)
    return str(value)


def canonical_string(generator_key, version, params, schema_order, seed, width, height) -> str:
    fields = [str(generator_key), _fmt_number(version)]
    for key in schema_order:
        fields.append(f"{key}={_fmt_number(params[key])}")
    fields.append(f"seed={_fmt_number(seed)}")
    fields.append(f"w={_fmt_number(width)}")
    fields.append(f"h={_fmt_number(height)}")
    return "|".join(fields)


def derive_identifier(canonical: str) -> str:
    digest = hashlib.sha256(canonical.encode("utf-8")).digest()
    return base64.b32encode(digest).decode("ascii").lower().rstrip("=")[:19]


@pytest.fixture(scope="session")
def schema_order(anonymous_session) -> dict:
    """generator key -> the parameter keys in the generator's own schema order."""
    response = anonymous_session.get("/generators")
    assert response.status_code == 200, (
        f"GET /api/generators returned {response.status_code}: {response.text[:300]}"
    )
    order = {}
    for row in response.json():
        key = row.get("key")
        detail = anonymous_session.get(f"/generators/{key}")
        if detail.status_code != 200:
            continue
        schema = detail.json().get("param_schema")
        if not schema:
            continue
        schema = _as_obj(schema)
        order[key] = [d["key"] for d in schema]
    return order


@pytest.fixture(scope="session")
def anonymous_session():
    with appclient.client() as c:
        yield c


def preset_row_by_title(backend: capabilities.Backend, title: str) -> dict:
    row = backend.one("presets", title=title)
    assert row is not None, f"no seeded preset titled {title!r}"
    return row


@pytest.fixture
def public_preset(backend) -> dict:
    return preset_row_by_title(backend, PUBLIC_PRESET_TITLE)


@pytest.fixture
def unlisted_preset(backend) -> dict:
    return preset_row_by_title(backend, UNLISTED_PRESET_TITLE)


@pytest.fixture
def private_preset(backend) -> dict:
    return preset_row_by_title(backend, PRIVATE_PRESET_TITLE)


def settings_from(row: dict, seed: int) -> dict:
    return {
        "generator": row["generator_key"],
        "version": row["generator_version"],
        "params": _as_obj(row["params"]),
        "seed": seed,
        "ratio": row["ratio"],
        "width": row["width"],
        "height": row["height"],
    }


def fresh_seed() -> int:
    return next(_seed_counter)


@pytest.fixture
def new_settings(public_preset):
    """A settings payload nobody has saved, rebuilt fresh for each test."""
    def _make(seed: int | None = None) -> dict:
        return settings_from(public_preset, fresh_seed() if seed is None else seed)
    return _make


def expected_identifier(settings: dict, schema_order: dict) -> str:
    order = schema_order[settings["generator"]]
    return derive_identifier(
        canonical_string(
            settings["generator"], settings["version"], settings["params"],
            order, settings["seed"], settings["width"], settings["height"],
        )
    )


def save_preset(client, settings: dict, title: str | None = None,
                visibility: str | None = None):
    body = dict(settings)
    if title is not None:
        body["title"] = title
    if visibility is not None:
        body["visibility"] = visibility
    return client.post("/presets", json=body)


def object_keys(store: capabilities.ObjectStore) -> set[str]:
    return set(store.list(RENDER_PREFIX))


def db_render_keys(backend: capabilities.Backend) -> set[str]:
    return {r["object_key"] for r in backend.rows("renders")}
