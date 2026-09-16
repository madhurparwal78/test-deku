from __future__ import annotations

import hashlib
import os
import time

import httpx
import pytest
from appclient import api_base, app_url, client, login, seeded_password
from capabilities import Backend, ObjectStore, make_backend, make_store

ATHLETE_EMAIL = "athlete@example.com"
ATHLETE2_EMAIL = "athlete2@example.com"
ATHLETE3_EMAIL = "athlete3@example.com"
ATHLETE4_EMAIL = "athlete4@example.com"
ATHLETE5_EMAIL = "athlete5@example.com"

CORPUS_PASSWORD = "deku-demo-pw-2026"

ROWAN = "Rowan Ellery"
SENA = "Sena Okafor"
DORIAN = "Dorian Vance"
MIRA = "Mira Halloran"
KIT = "Kit Bramwell"

SEEDED_SEGMENT = "Ridgeway Climb"
REFERENCE_ACTIVITY = "Ridgeway long loop"
SEEDED_CLUB = "dawn-patrol"
SEEDED_CHALLENGE = "april-ascent"
SEEDED_ROUTE = "Loch Circuit"

VISIBILITIES = ("everyone", "followers", "only_you")
ACTIVITY_TYPES = ("run", "ride", "swim", "hike", "ski", "walk")
FOLLOW_STATES = ("pending", "accepted", "blocked")
UPLOAD_STATES = ("received", "parsing", "matching", "ready", "failed",
                 "duplicate_suspected")
STREAM_TYPES = ("time", "latlng", "distance", "altitude", "heartrate", "cadence",
                "watts", "temp", "moving", "grade_smooth")
FLAG_STATES = ("clear", "flagged", "excluded")
ACHIEVEMENT_KINDS = ("overall_top_three", "segment_pr", "distance_pr")

REFERENCE_ELAPSED_S = 5400
REFERENCE_MOVING_S = 4200
REFERENCE_STOPPED_S = 1200
REFERENCE_DISTANCE_M = 32000
REFERENCE_GAIN_M = 480

SEGMENT_LENGTH_M = 1800
SEGMENT_GAIN_M = 95
CORRIDOR_TOLERANCE_M = 30
DRIFT_M = 25
SAMPLE_RATE_S = 3
ZONE_RADIUS_M = 400
FLAT_GAIN_CEILING_M = 10
EAST_TRACK_M = 10000
EAST_TRACK_LAT = 55
FASTEST_5K_START_M = 3200
AGGREGATE_MIN_ATHLETES = 3
FEED_PAGE_SIZE = 30

SETTLE_SECONDS = 1.0
POLL_BUDGET_SECONDS = 45.0

STORAGE_UPLOAD_PREFIX = "uploads/"
STORAGE_STREAM_PREFIX = "streams/"


def settle(seconds: float = SETTLE_SECONDS) -> None:
    time.sleep(seconds)


def kudos_window_budget() -> float:
    configured = float(os.environ.get("KUDOS_BATCH_WINDOW_SEC", "6"))
    return (2 * configured) + SETTLE_SECONDS + 5.0


def fanout_threshold() -> int:
    return int(os.environ.get("FANOUT_FOLLOWER_THRESHOLD", "2"))


def poll_until(predicate, budget: float = POLL_BUDGET_SECONDS):
    end = time.monotonic() + budget
    last = None
    while time.monotonic() < end:
        last = predicate()
        if last:
            return last
        settle(0.5)
    return last


def unique_ref(prefix: str = "probe") -> str:
    return f"{prefix}-{os.urandom(6).hex()}"


def unique_email() -> str:
    return f"probe-{os.urandom(6).hex()}@example.com"


def authed(email: str) -> httpx.Client:
    token = login(email, seeded_password("SEED_PASSWORD", CORPUS_PASSWORD))
    return client(token)


@pytest.fixture
def anon_client():
    with client() as c:
        yield c


@pytest.fixture
def rowan_client():
    with authed(ATHLETE_EMAIL) as c:
        yield c


@pytest.fixture
def sena_client():
    with authed(ATHLETE2_EMAIL) as c:
        yield c


@pytest.fixture
def dorian_client():
    with authed(ATHLETE3_EMAIL) as c:
        yield c


@pytest.fixture
def mira_client():
    with authed(ATHLETE4_EMAIL) as c:
        yield c


@pytest.fixture
def kit_client():
    with authed(ATHLETE5_EMAIL) as c:
        yield c


class RidgelineStore:
    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def athlete_by_email(self, email: str) -> dict | None:
        return self._b.one("athletes", email=email)

    def count_athletes(self, **where) -> int:
        return self._b.count("athletes", **where)

    def follow(self, follower_id, followee_id) -> dict | None:
        return self._b.one("follows", follower_id=follower_id,
                           followee_id=followee_id)

    def count_follows(self, **where) -> int:
        return self._b.count("follows", **where)

    def count_blocks(self, **where) -> int:
        return self._b.count("blocks", **where)

    def upload_by_id(self, upload_id) -> dict | None:
        return self._b.one("uploads", id=upload_id)

    def count_uploads(self, **where) -> int:
        return self._b.count("uploads", **where)

    def activity_by_id(self, activity_id) -> dict | None:
        return self._b.one("activities", id=activity_id)

    def activity_by_name(self, name: str) -> dict | None:
        return self._b.one("activities", name=name)

    def count_activities(self, **where) -> int:
        return self._b.count("activities", **where)

    def summary_of(self, activity_id) -> dict | None:
        return self._b.one("activity_summaries", activity_id=activity_id)

    def streams_of(self, activity_id) -> list[dict]:
        return self._b.rows("streams", activity_id=activity_id)

    def polylines_of(self, activity_id) -> list[dict]:
        return self._b.rows("polylines", activity_id=activity_id)

    def segment_by_name(self, name: str) -> dict | None:
        return self._b.one("segments", name=name)

    def efforts_of_activity(self, activity_id) -> list[dict]:
        return self._b.rows("segment_efforts", activity_id=activity_id)

    def efforts_of_segment(self, segment_id) -> list[dict]:
        return self._b.rows("segment_efforts", segment_id=segment_id)

    def count_efforts(self, **where) -> int:
        return self._b.count("segment_efforts", **where)

    def best_efforts_of(self, activity_id) -> list[dict]:
        return self._b.rows("best_efforts", activity_id=activity_id)

    def achievements_of(self, activity_id) -> list[dict]:
        return self._b.rows("achievements", activity_id=activity_id)

    def count_achievements(self, **where) -> int:
        return self._b.count("achievements", **where)

    def privacy_zones_of(self, athlete_id) -> list[dict]:
        return self._b.rows("privacy_zones", athlete_id=athlete_id)

    def count_kudos(self, **where) -> int:
        return self._b.count("kudos", **where)

    def notifications_of(self, athlete_id) -> list[dict]:
        return self._b.rows("notifications", athlete_id=athlete_id)

    def feed_entries_of(self, athlete_id) -> list[dict]:
        return self._b.rows("feed_entries", athlete_id=athlete_id)

    def count_feed_entries(self, **where) -> int:
        return self._b.count("feed_entries", **where)

    def count_clubs(self) -> int:
        return self._b.count("clubs")

    def count_challenges(self) -> int:
        return self._b.count("challenges")

    def count_routes(self, **where) -> int:
        return self._b.count("routes", **where)

    def count_plans(self) -> int:
        return self._b.count("plans")

    def gift_by_code(self, code: str) -> dict | None:
        return self._b.one("gift_purchases", redemption_code=code)


@pytest.fixture
def db() -> RidgelineStore:
    return RidgelineStore(make_backend())


@pytest.fixture
def store() -> ObjectStore:
    return make_store()


def api(path: str) -> str:
    return f"{api_base()}{path}"


def page(path: str) -> str:
    return f"{app_url()}{path}"


def fetch(path: str, **kwargs) -> httpx.Response:
    return httpx.get(page(path), timeout=30.0, follow_redirects=True, **kwargs)


GPX_HEADER = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<gpx version="1.1" creator="deku-verifier">\n  <trk>\n')
GPX_FOOTER = "  </trkseg></trk>\n</gpx>\n"


def gpx_track(points, start="2026-04-02T06:00:00Z", label=None) -> bytes:
    """A minimal track file the app can parse, built from (lat, lng, ele, offset).

    `label` rides in the track's own description, which is where a per-run
    reference belongs: every probe that uploads builds its own bytes from it, so
    no two probes collide on the content hash deduplication keys on.
    """
    from datetime import datetime, timedelta, timezone

    base = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    marker = label or "deku-verifier probe"
    body = [f"    <desc>{marker}</desc>\n",
            "    <trkseg>\n"]
    for lat, lng, ele, offset in points:
        when = (base + timedelta(seconds=offset)).strftime("%Y-%m-%dT%H:%M:%SZ")
        body.append(
            f'    <trkpt lat="{lat:.6f}" lon="{lng:.6f}">'
            f"<ele>{ele:.1f}</ele><time>{when}</time></trkpt>\n")
    return (GPX_HEADER + "".join(body) + GPX_FOOTER).encode("utf-8")


def straight_track(points=40, spacing_deg=0.0002, lat=51.5, lng=-0.12, ele=100.0,
                   start="2026-04-02T06:00:00Z", label=None):
    """An eastward run of samples at the pinned sample rate."""
    rows = []
    for i in range(points):
        rows.append((lat, lng + i * spacing_deg, ele, i * SAMPLE_RATE_S))
    return gpx_track(rows, start=start, label=label)


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def upload_file(client_, payload: bytes, activity_type="ride", name=None,
                visibility="everyone") -> dict:
    files = {"file": (f"{name or unique_ref('track')}.gpx", payload,
                      "application/gpx+xml")}
    data = {"activity_type": activity_type, "name": name or unique_ref("Probe ride"),
            "visibility": visibility}
    response = client_.post("/uploads", files=files, data=data)
    assert response.status_code in (200, 201, 202), (
        f"POST /api/uploads returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    assert body.get("upload_id") is not None, (
        f"POST /api/uploads must return an upload_id: {response.text[:400]}")
    return body


def upload_reaches(client_, upload_id, wanted, budget=POLL_BUDGET_SECONDS):
    """Poll one upload until its status is in `wanted`, then return the row."""
    wanted = tuple(wanted)

    def arrived():
        response = client_.get(f"/uploads/{upload_id}")
        if response.status_code != 200:
            return None
        body = response.json()
        return body if body.get("status") in wanted else None

    row = poll_until(arrived, budget=budget)
    assert row is not None, (
        f"upload {upload_id} never reached any of {wanted}; an upload moves through "
        f"{UPLOAD_STATES} and reports the state it is in")
    return row


def fresh_activity(client_, payload=None, activity_type="ride", visibility="everyone",
                   name=None):
    """Upload a track and return the activity it produced, once ready.

    Each probe makes its own activity. The browser pass runs before the pytest
    pass and mutates the seeded athlete's world, so a probe that asserts a
    pre-state on a seeded row is reading what another channel already consumed.
    """
    payload = payload or straight_track(label=unique_ref("fixture"))
    created = upload_file(client_, payload, activity_type=activity_type,
                          name=name, visibility=visibility)
    row = upload_reaches(client_, created["upload_id"], ("ready",))
    activity_id = row.get("activity_id")
    assert activity_id is not None, (
        f"upload {created['upload_id']} reached ready with no activity_id: {row}")
    return activity_id


def athlete_id_of(client_):
    response = client_.get("/me")
    assert response.status_code == 200, (
        f"GET /api/me returned {response.status_code}: {response.text[:400]}")
    return response.json().get("id")


def leaderboard(client_, segment_id, **params):
    response = client_.get(f"/segments/{segment_id}/leaderboard", params=params)
    assert response.status_code == 200, (
        f"GET /api/segments/{segment_id}/leaderboard returned "
        f"{response.status_code}: {response.text[:400]}")
    body = response.json()
    assert "entries" in body and "total" in body, (
        f"a leaderboard returns an object carrying total and entries: "
        f"{response.text[:400]}")
    return body


def segment_id_by_name(client_, name: str = SEEDED_SEGMENT):
    response = client_.get("/segments", params={"q": name})
    assert response.status_code == 200, (
        f"GET /api/segments returned {response.status_code}: {response.text[:400]}")
    rows = response.json().get("items", [])
    for row in rows:
        if row.get("name") == name:
            return row.get("id")
    raise AssertionError(
        f"no segment named {name!r}; the seed data pins it. "
        f"Saw: {[r.get('name') for r in rows]}")


def feed_page(client_, cursor=None, limit=None):
    params = {}
    if cursor:
        params["cursor"] = cursor
    if limit:
        params["limit"] = limit
    response = client_.get("/feed", params=params)
    assert response.status_code == 200, (
        f"GET /api/feed returned {response.status_code}: {response.text[:400]}")
    body = response.json()
    assert "items" in body, (
        f"GET /api/feed returns an object carrying items: {response.text[:400]}")
    return body


def signup(email=None, password=CORPUS_PASSWORD, display_name=None):
    """Create a throwaway athlete and return an authenticated client for them."""
    email = email or unique_email()
    with client() as anon:
        response = anon.post("/auth/signup", json={
            "email": email, "password": password,
            "display_name": display_name or unique_ref("Probe athlete")})
    assert response.status_code in (200, 201), (
        f"POST /api/auth/signup returned {response.status_code}: "
        f"{response.text[:400]}")
    token = response.json().get("access_token")
    assert token, f"signup must return an access_token: {response.text[:400]}"
    return email, client(token)
