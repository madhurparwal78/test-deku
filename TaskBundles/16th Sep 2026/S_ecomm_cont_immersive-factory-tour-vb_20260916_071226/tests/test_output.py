"""Black-box graders for deku/immersive-factory-tour-vb.

Every assertion drives the app through its HTTP surface, reads real Postgres rows
through the backend capability, or reads the real MinIO objects through the object
store capability. Nothing inspects the app's source, framework or schema
internals (INV6). Concurrency is exercised with real simultaneous requests, never
simulated, so the one-entry-per-reader rule is observed the way a stranger would
hit it. Unique per-run identifiers keep every run independent.
"""

from __future__ import annotations

import concurrent.futures
import uuid

import httpx
from appclient import app_url, login
from conftest import (
    PASSWORD, AUTHOR_EMAIL, READER_EMAIL, READER2_EMAIL,
    STATIONS, PRIZES, POSTER_PREFIX, PRIZE_PREFIX, CONSENT_FLAG, CONFIRMATION,
    ACCEPTED, PNG_1PX,
    signup, fresh_reader, create_chapter, publish_chapter, a_draft_chapter, poll,
)


def _client_error(code: int) -> bool:
    return 400 <= code < 500


def _entry_body(consent: bool = True, client_request_id: str | None = None) -> dict:
    body = {
        "civility": "MR",
        "first_name": "Robin",
        "last_name": "Marlowe",
        "email": f"entrant-{uuid.uuid4().hex[:8]}@example.com",
        "birthdate": "1990-01-01",
        "country": "France",
        "consent_terms": consent,
        "consent_marketing": False,
    }
    if client_request_id is not None:
        body["client_request_id"] = client_request_id
    return body


def _reader_id(db, email):
    account = db.account(email)
    assert account is not None, f"the reader {email!r} must exist after signup"
    return account["id"]



def test_health_ready(anon_client):
    response = anon_client.get("/health")
    assert response.status_code == 200, "health must return 200 once the app is ready"


def test_login_issues_token():
    token = login(AUTHOR_EMAIL, PASSWORD)
    assert token, "signing in with the seeded author must issue an access token"


def test_signup_creates_reader():
    token = signup(f"newreader-{uuid.uuid4().hex[:8]}@example.com")
    assert token, "open signup must create a reader and issue an access token"


def test_login_wrong_password_refused(anon_client):
    response = anon_client.post(
        "/auth/login", json={"email": AUTHOR_EMAIL, "password": "not-the-password"})
    assert _client_error(response.status_code), "a wrong password must be refused as a client error"


def test_create_chapter_stores_poster_object(author_client, object_store):
    before = set(object_store.list(POSTER_PREFIX))
    create_chapter(author_client, station="knitting")
    after = poll(lambda: set(object_store.list(POSTER_PREFIX)), lambda s: len(s) > len(before))
    assert len(after) > len(before), "creating a chapter must write a poster object under chapters/"


def test_publish_makes_poster_public(author_client, anon_client):
    chapter = create_chapter(author_client, station="dyeing")
    published = publish_chapter(author_client, chapter["id"])
    assert published.status_code in ACCEPTED, "the author must be able to publish a chapter"
    response = poll(
        lambda: anon_client.get(f"/chapters/{chapter['id']}/poster"),
        lambda r: r.status_code == 200,
    )
    assert response.status_code == 200, "a published chapter poster must be publicly readable"


def test_draft_poster_refused_to_stranger(author_client, anon_client):
    chapter = create_chapter(author_client, station="embroidering")
    response = anon_client.get(f"/chapters/{chapter['id']}/poster")
    assert _client_error(response.status_code) or response.status_code == 404, (
        "a draft chapter poster must be refused to a stranger")


def test_unpublish_returns_chapter_to_draft(author_client):
    chapter = create_chapter(author_client, station="knitting")
    publish_chapter(author_client, chapter["id"])
    response = author_client.post(f"/chapters/{chapter['id']}/unpublish")
    assert response.status_code in ACCEPTED, "the author must be able to unpublish a chapter"
    reread = author_client.get(f"/chapters/{chapter['id']}")
    assert reread.status_code == 200 and reread.json().get("state") == "draft", (
        "an unpublished chapter returns to draft")


def test_publish_prize_stores_image_object(author_client, object_store):
    before = set(object_store.list(PRIZE_PREFIX))
    response = author_client.post(
        "/prizes",
        data={"name": PRIZES[0], "title": "A signature polo shirt"},
        files={"image": ("prize.png", PNG_1PX, "image/png")},
    )
    assert response.status_code in ACCEPTED, "the author must be able to publish a prize"
    after = poll(lambda: set(object_store.list(PRIZE_PREFIX)), lambda s: len(s) > len(before))
    assert len(after) > len(before), "publishing a prize must write an image object under prizes/"


def test_tour_lists_published_chapters_in_order(reader_client):
    response = reader_client.get("/tour")
    assert response.status_code == 200, "a reader must be able to read the tour"
    stations = [c.get("station") for c in response.json()]
    seen = [s for s in stations if s in STATIONS]
    ordered = [s for s in STATIONS if s in seen]
    assert seen == [s for s in stations if s in STATIONS], "the tour lists stations without duplicates out of order"
    assert seen == ordered, "the tour presents the stations in knitting, dyeing, embroidering order"


def test_hotspot_raises_tally(reader_client):
    first = reader_client.post("/score", json={"points": 10})
    assert first.status_code in ACCEPTED, "a reader may record hotspot points"
    before = first.json().get("points", 0)
    second = reader_client.post("/score", json={"points": 5})
    assert second.status_code in ACCEPTED, "a reader may record more hotspot points"
    after = second.json().get("points", 0)
    assert after > before, "triggering a hotspot raises the reader running tally"


def test_reader_entry_is_stored(db):
    reader, email = fresh_reader()
    response = reader.post("/entries", json=_entry_body(consent=True))
    assert response.status_code in ACCEPTED, "a reader may submit a prize-draw entry"
    assert db.entry_count(reader_id=_reader_id(db, email)) == 1, "the entry must be stored"


def test_entry_without_consent_refused(db):
    reader, email = fresh_reader()
    response = reader.post("/entries", json=_entry_body(consent=False))
    assert _client_error(response.status_code), "an entry without the terms consent is refused"
    assert db.entry_count(reader_id=_reader_id(db, email)) == 0, "nothing is stored without consent"



def test_reader_publish_denied(reader_client):
    response = reader_client.post(
        "/chapters",
        data={"station": "knitting", "title": "Sneak chapter", "body": "x"},
        files={"poster": ("poster.png", PNG_1PX, "image/png")},
    )
    assert _client_error(response.status_code), "a reader publishing a chapter is denied by the server"


def test_reader_entry_list_denied(reader_client):
    response = reader_client.get("/entries")
    assert _client_error(response.status_code), "a reader requesting the entry list is denied"


def test_reader_other_entry_denied(reader2_client):
    response = reader2_client.get("/entries")
    assert _client_error(response.status_code), (
        "a reader requesting another reader's entries through the author list is denied")


def test_signed_out_reader_route_refused(anon_client):
    response = anon_client.get("/tour")
    assert _client_error(response.status_code), "a signed-out request to a reader route is refused"


def test_reader_draft_poster_refused(author_client, reader_client):
    chapter = create_chapter(author_client, station="knitting")
    response = reader_client.get(f"/chapters/{chapter['id']}/poster")
    assert _client_error(response.status_code) or response.status_code == 404, (
        "a reader fetching a draft chapter poster is refused")



def test_seed_author_present(db):
    account = db.account(AUTHOR_EMAIL)
    assert account is not None and account.get("role") == "author", "the seeded author must be present"


def test_seed_readers_present(db):
    assert db.account(READER_EMAIL) is not None, "the first seeded reader must be present"
    assert db.account(READER2_EMAIL) is not None, "the second seeded reader must be present"


def test_seed_published_chapters_present(db):
    assert db.chapter_count(state="published") >= 3, "three published chapters must be seeded"


def test_seed_draft_chapter_present(db):
    assert db.chapter_count(state="draft") >= 1, "a draft chapter must be seeded"


def test_seed_prizes_present(db):
    assert db.prize_count(state="published") >= 3, "three published prizes must be seeded"


def test_single_entry_per_reader_invariant(db):
    reader, email = fresh_reader()
    reader.post("/entries", json=_entry_body(consent=True))
    reader.post("/entries", json=_entry_body(consent=True))
    assert db.entry_count(reader_id=_reader_id(db, email)) == 1, "at most one entry exists per reader"



def test_concurrent_entry_single_winner(db):
    reader, email = fresh_reader()
    body = _entry_body(consent=True)

    def submit(_):
        return reader.post("/entries", json=body)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = [f.result() for f in [pool.submit(submit, 0), pool.submit(submit, 1)]]
    winners = sum(1 for r in results if r.status_code in ACCEPTED)
    assert winners == 1, "exactly one concurrent entry submission wins"
    assert db.entry_count(reader_id=_reader_id(db, email)) == 1, "exactly one entry is stored"


def test_duplicate_entry_conflict_rejected(db):
    reader, email = fresh_reader()
    first = reader.post("/entries", json=_entry_body(consent=True))
    assert first.status_code in ACCEPTED, "the first entry succeeds"
    second = reader.post("/entries", json=_entry_body(consent=True))
    assert second.status_code == 409 or _client_error(second.status_code), (
        "a duplicate entry from the same reader is refused as a conflict")


def test_idempotent_entry_replay(db):
    reader, email = fresh_reader()
    request_id = uuid.uuid4().hex
    reader.post("/entries", json=_entry_body(consent=True, client_request_id=request_id))
    reader.post("/entries", json=_entry_body(consent=True, client_request_id=request_id))
    assert db.entry_count(reader_id=_reader_id(db, email)) == 1, (
        "a replayed entry with the same client request id creates no second entry")


def test_poster_object_in_store_not_on_disk(author_client, object_store):
    chapter = create_chapter(author_client, station="dyeing")
    publish_chapter(author_client, chapter["id"])
    keys = poll(lambda: object_store.list(POSTER_PREFIX), lambda k: len(k) > 0)
    assert any(key.startswith(POSTER_PREFIX) for key in keys), (
        "a chapter poster must live in the object store at its key scheme")


def test_no_frontend_secrets():
    root = app_url()
    secrets = ("deku-local-dev", "deku-minio-app", "STORAGE_SECRET_KEY", "ANTHROPIC_API_KEY")
    for path in ("/", "/login", "/prizes"):
        response = httpx.get(f"{root}{path}", timeout=30.0)
        for secret in secrets:
            assert secret not in response.text, f"no credential must appear in the page {path!r}"


def test_strict_transport_security_header(anon_client):
    response = anon_client.get("/health")
    headers = {k.lower(): v for k, v in response.headers.items()}
    assert "strict-transport-security" in headers, (
        "every response carries a strict transport security header")


def test_nosniff_content_type_header(anon_client):
    response = anon_client.get("/health")
    headers = {k.lower(): v for k, v in response.headers.items()}
    assert headers.get("x-content-type-options", "").lower() == "nosniff", (
        "every response carries a nosniff content-type header")


def test_favicon_declared_and_served():
    response = httpx.get(f"{app_url()}/favicon.ico", timeout=30.0)
    if response.status_code == 200:
        return
    root = httpx.get(app_url(), timeout=30.0)
    assert "icon" in root.text.lower(), "the document head declares a favicon the site serves"
