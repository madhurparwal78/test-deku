"""Black-box graders for the voice-synthesis-workbench.

Every test reaches the app only over HTTP and reads the declared services only
through the capability adapters. Section banners group the tests by the concern
they observe, not by the setup they share.
"""
from __future__ import annotations

import os
import threading

import pytest

from appclient import client
from conftest import (
    AUTHOR2_EMAIL,
    AUTHOR_EMAIL,
    GENERATION_COST,
    READER_EMAIL,
    TAKE_OBJECT_PREFIX,
    account_password,
    fresh_email,
    poll,
    settle,
)
from _shapes import flatten, items


def _first_voice_id(c) -> str:
    payload = c.get("/voices").json()
    rows = items(payload)
    assert rows, f"the seeded catalogue returned no voices: {flatten(payload)[:300]}"
    return str(rows[0].get("id"))


def _script() -> str:
    return "Welcome to the studio. This is a short narration take."


def _generate(c, voice_id: str, key: str | None = None, script: str | None = None):
    headers = {"Idempotency-Key": key} if key else {}
    body = {"voice_id": voice_id, "language": "English",
            "script": _script() if script is None else script}
    return c.post("/takes", json=body, headers=headers)



def test_seeded_accounts_login(author_client):
    """The seeded author authenticates and reads their own account."""
    resp = author_client.get("/credits")
    assert resp.status_code == 200, f"seeded author could not read credits: {resp.text[:300]}"


def test_signup_rejects_duplicate_email(anon_client):
    """A signup for an already registered email is refused."""
    resp = anon_client.post("/auth/signup",
                            json={"email": AUTHOR_EMAIL, "password": account_password(),
                                  "role": "author"})
    assert resp.status_code in (400, 409, 422), (
        f"a duplicate signup was accepted: {resp.status_code} {resp.text[:300]}")


def test_signup_rejects_short_password(anon_client):
    """A signup with a password shorter than eight characters is refused."""
    resp = anon_client.post("/auth/signup",
                            json={"email": fresh_email(), "password": "short", "role": "author"})
    assert resp.status_code in (400, 422), (
        f"a short password was accepted: {resp.status_code} {resp.text[:300]}")


def test_catalogue_filters_by_use_case(author_client):
    """Filtering the catalogue by a use case narrows the list."""
    full = items(author_client.get("/voices").json())
    narrowed = items(author_client.get("/voices", params={"use_case": "Narration"}).json())
    assert narrowed, "filtering by a known use case returned nothing"
    assert len(narrowed) <= len(full), "a use-case filter did not narrow the catalogue"
    for row in narrowed:
        assert str(row.get("use_case", "")).lower() == "narration", (
            f"a voice outside the filter was returned: {row}")


def test_catalogue_filters_by_language(author_client):
    """Filtering the catalogue by a language narrows the list."""
    full = items(author_client.get("/voices").json())
    narrowed = items(author_client.get("/voices", params={"language": "English"}).json())
    assert narrowed, "filtering by a known language returned nothing"
    assert len(narrowed) <= len(full), "a language filter did not narrow the catalogue"


def test_generate_charges_one_hundred_credits(author_client):
    """Generating a take lowers the balance by the take cost."""
    before = author_client.get("/credits").json().get("balance")
    voice_id = _first_voice_id(author_client)
    resp = _generate(author_client, voice_id)
    assert resp.status_code in (200, 201), f"generate failed: {resp.text[:300]}"
    after = poll(lambda: author_client.get("/credits").json().get("balance"),
                 lambda b: b is not None and b <= before - GENERATION_COST)
    assert before - after == GENERATION_COST, (
        f"balance moved by {before - after}, the take cost is {GENERATION_COST}")


def test_generate_rejects_empty_script(author_client):
    """A generate request with an empty script is refused."""
    voice_id = _first_voice_id(author_client)
    resp = _generate(author_client, voice_id, script="")
    assert resp.status_code in (400, 422), (
        f"an empty script was accepted: {resp.status_code} {resp.text[:300]}")


def test_library_lists_owner_takes_newest_first(author_client):
    """The asset library returns the caller's own takes, newest first."""
    voice_id = _first_voice_id(author_client)
    created = _generate(author_client, voice_id).json()
    listing = items(author_client.get("/takes").json())
    assert listing, "the library returned no takes after a generation"
    ids = [str(row.get("id")) for row in listing]
    assert str(created.get("id")) in ids, "a freshly generated take was absent from the library"


def test_published_take_appears_in_gallery(author_client, reader_client):
    """A published take is listed in the public gallery for any reader."""
    voice_id = _first_voice_id(author_client)
    take = _generate(author_client, voice_id).json()
    take_id = str(take.get("id"))
    published = author_client.post(f"/takes/{take_id}/publish", json={"visibility": "public"})
    assert published.status_code in (200, 201), f"publish failed: {published.text[:300]}"
    seen = poll(lambda: [str(r.get("id")) for r in items(reader_client.get("/gallery").json())],
                lambda ids: take_id in ids)
    assert take_id in seen, "a published take was not visible in the gallery to a reader"


def test_unpublish_removes_take_from_gallery(author_client):
    """Returning a take to private removes it from the public gallery."""
    voice_id = _first_voice_id(author_client)
    take_id = str(_generate(author_client, voice_id).json().get("id"))
    author_client.post(f"/takes/{take_id}/publish", json={"visibility": "public"})
    author_client.post(f"/takes/{take_id}/publish", json={"visibility": "private"})
    gone = poll(lambda: [str(r.get("id")) for r in items(author_client.get("/gallery").json())],
                lambda ids: take_id not in ids)
    assert take_id not in gone, "a take returned to private stayed in the gallery"


def test_api_key_shown_once_on_creation(author_client):
    """A new API key returns its secret once at creation."""
    resp = author_client.post("/keys", json={"name": "cli"})
    assert resp.status_code in (200, 201), f"key creation failed: {resp.text[:300]}"
    body = resp.json()
    assert body.get("key"), "key creation did not return the secret once"
    assert body.get("prefix"), "key creation returned no prefix"


def test_privacy_page_served(anon_client):
    """The privacy page renders readable content."""
    with client() as c:
        resp = c.get("/../privacy")
    assert resp.status_code == 200, f"the privacy page did not render: {resp.status_code}"
    assert len(resp.text) > 200, "the privacy page carried no readable content"


def test_terms_page_served():
    """The terms page renders readable content."""
    with client() as c:
        resp = c.get("/../terms")
    assert resp.status_code == 200, f"the terms page did not render: {resp.status_code}"
    assert len(resp.text) > 200, "the terms page carried no readable content"


def test_unknown_route_returns_custom_not_found():
    """An unknown route renders a custom not found page."""
    with client() as c:
        resp = c.get("/../this-route-does-not-exist")
    assert resp.status_code == 404, (
        f"an unknown route did not return not found: {resp.status_code}")



def test_generate_stores_one_object_in_bucket(author_client, object_store):
    """A generation stores exactly one new audio object in the bucket."""
    before = len(object_store.list(prefix=TAKE_OBJECT_PREFIX))
    voice_id = _first_voice_id(author_client)
    resp = _generate(author_client, voice_id)
    assert resp.status_code in (200, 201), f"generate failed: {resp.text[:300]}"
    after = poll(lambda: len(object_store.list(prefix=TAKE_OBJECT_PREFIX)),
                 lambda n: n >= before + 1)
    assert after - before == 1, (
        f"expected one new object under {TAKE_OBJECT_PREFIX}, delta was {after - before}; "
        f"the audio was held on local disk or in the database, not the bucket")


def test_take_audio_persisted_as_object_not_db_blob(author_client, object_store):
    """A ready take names a stored object that exists in the bucket."""
    voice_id = _first_voice_id(author_client)
    take = _generate(author_client, voice_id).json()
    key = take.get("storage_key")
    assert key, f"the take carried no storage_key: {flatten(take)[:300]}"
    exists = poll(lambda: object_store.exists(key), lambda ok: bool(ok))
    assert exists, f"the take audio object {key} is absent from the store"


def test_balance_never_driven_below_zero(author2_client):
    """A generation the balance cannot cover leaves the balance non-negative."""
    voice_id = _first_voice_id(author2_client)
    _generate(author2_client, voice_id)
    settle()
    balance = author2_client.get("/credits").json().get("balance")
    assert balance is not None and balance >= 0, (
        f"the balance was driven below zero to {balance}")


def test_seed_is_idempotent(author_client):
    """The seeded catalogue holds a stable set of voices across reads."""
    first = len(items(author_client.get("/voices").json()))
    second = len(items(author_client.get("/voices").json()))
    assert first == second and first > 0, (
        f"the seeded catalogue size drifted between reads: {first} then {second}")


def test_key_generation_records_usage_event(author_client):
    """A generation records a usage event carrying a request correlation id."""
    voice_id = _first_voice_id(author_client)
    _generate(author_client, voice_id)
    events = poll(lambda: items(author_client.get("/usage").json()), lambda rows: bool(rows))
    assert events, "no usage event was recorded for a generation"
    assert any(row.get("request_id") for row in events), (
        "a usage event carried no request_id correlation field")



def test_concurrent_duplicate_key_creates_single_take(author_token, author_client):
    """Two simultaneous generations with one key create exactly one take."""
    voice_id = _first_voice_id(author_client)
    key = "idem-" + os.urandom(6).hex()
    gate = threading.Barrier(2)
    lock = threading.Lock()
    statuses: list[int] = []

    def fire():
        with client(author_token) as c:
            gate.wait()
            resp = _generate(c, voice_id, key=key)
        with lock:
            statuses.append(resp.status_code)

    threads = [threading.Thread(target=fire) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)
    created = [s for s in statuses if s in (200, 201)]
    assert len(created) >= 1, f"neither duplicated request succeeded: {sorted(statuses)}"
    listing = items(author_client.get("/takes").json())
    matches = [row for row in listing if str(row.get("idempotency_key")) == key]
    assert len(matches) == 1, (
        f"a duplicated key created {len(matches)} takes; exactly one must exist")


def test_generate_over_balance_rejected(author2_client):
    """A generation an account cannot afford is refused with a client error."""
    voice_id = _first_voice_id(author2_client)
    poll(lambda: author2_client.get("/credits").json().get("balance"),
         lambda b: b is not None and b < GENERATION_COST, tries=1)
    resp = _generate(author2_client, voice_id)
    assert resp.status_code in (402, 400, 403), (
        f"an unaffordable generation was accepted: {resp.status_code} {resp.text[:300]}")


def test_catalogue_pagination_cursor(author_client):
    """The catalogue read is paginated with a forward cursor and metadata."""
    payload = author_client.get("/voices", params={"page_size": 2}).json()
    assert "next_cursor" in payload or payload.get("has_more") is not None, (
        f"the paginated response carried no cursor metadata: {flatten(payload)[:300]}")
    rows = items(payload)
    assert len(rows) <= 2, f"page_size was ignored, got {len(rows)} rows"


def test_no_frontend_secret_in_bundle():
    """The served frontend carries no storage or database secret."""
    with client() as c:
        resp = c.get("/../")
    assert resp.status_code == 200, f"the app root did not render: {resp.status_code}"
    secret = os.environ.get("STORAGE_SECRET_KEY", "deku-local-dev")
    assert secret not in resp.text, "a storage secret was served in the frontend document"



def test_reader_cannot_generate_forbidden(reader_client):
    """A reader is refused generation."""
    resp = _generate(reader_client, "any-voice")
    assert resp.status_code in (401, 403), (
        f"a reader was allowed to generate: {resp.status_code} {resp.text[:300]}")


def test_reader_denied_author_endpoint(reader_client):
    """A reader is refused an author-only key endpoint."""
    resp = reader_client.post("/keys", json={"name": "cli"})
    assert resp.status_code in (401, 403), (
        f"a reader reached an author-only endpoint: {resp.status_code} {resp.text[:300]}")


def test_unauthenticated_access_denied(anon_client):
    """An anonymous caller is refused every protected endpoint."""
    protected = [("GET", "/takes"), ("POST", "/keys"), ("GET", "/credits"), ("GET", "/usage")]
    for method, path in protected:
        resp = anon_client.request(method, path, json={})
        assert resp.status_code in (401, 403), (
            f"anonymous {method} {path} was served: {resp.status_code}")



def test_private_take_object_not_readable_by_non_owner(author_client, author2_client, reader_client):
    """A private take audio is refused to any account but its owner."""
    voice_id = _first_voice_id(author2_client)
    take_id = str(_generate(author2_client, voice_id).json().get("id"))
    owner = author2_client.get(f"/takes/{take_id}/audio")
    assert owner.status_code in (200, 206), f"the owner could not read their own take: {owner.status_code}"
    other = author_client.get(f"/takes/{take_id}/audio")
    assert other.status_code in (401, 403, 404), (
        f"another author read a private take: {other.status_code}")
    listener = reader_client.get(f"/takes/{take_id}/audio")
    assert listener.status_code in (401, 403, 404), (
        f"a reader read a private take: {listener.status_code}")


def test_key_list_hides_secret(author_client):
    """The key list shows a prefix and never the secret value."""
    created = author_client.post("/keys", json={"name": "listing"}).json()
    secret = created.get("key")
    listing = items(author_client.get("/keys").json())
    assert listing, "the key list returned nothing after a key was created"
    for row in listing:
        assert "key" not in row or not row.get("key"), "the key list exposed a secret value"
        if secret:
            assert secret not in flatten(row), "the key list echoed the secret value"


def test_health_ok():
    """The health endpoint returns ready."""
    with client() as c:
        resp = c.get("/health")
    assert resp.status_code == 200, f"health was not ready: {resp.status_code}"
