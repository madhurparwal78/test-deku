from __future__ import annotations

import datetime
import os
import re
import time

import httpx
import pytest
from _shapes import flatten, items
from appclient import api_base, app_url, client, login, seeded_password
from capabilities import Backend, make_backend, make_inbox

VISITOR_EMAIL = "visitor@example.com"
VISITOR2_EMAIL = "visitor2@example.com"
HOST_EMAIL = "host@example.com"
HOST2_EMAIL = "host2@example.com"
SEEDED_PASSWORD_DEFAULT = "deku-demo-pw-2026"

FLAVOUR_MARSHMALLOW = "marshmallow-coffee"
FLAVOUR_ORANGE = "orange-chocolate"
FLAVOUR_MINT = "mint-chocolate"
FLAVOUR_IDS = (FLAVOUR_MARSHMALLOW, FLAVOUR_ORANGE, FLAVOUR_MINT)
FLAVOUR_NAMES = (
    "MARSHMALLOW COFFEE & CREAM",
    "ORANGE CHOCOLATE & CREAM",
    "MINT CHOCOLATE & CREAM",
)
TINT_TOKENS = ("flavour-a", "flavour-b", "flavour-c")
TASTING_NOTES = {
    FLAVOUR_MARSHMALLOW: "Toasted marshmallow and cold brew over vanilla cream, finishing on bitter cocoa.",
    FLAVOUR_ORANGE: "Candied orange peel folded into milk chocolate and cream, with a warm clove finish.",
    FLAVOUR_MINT: "Garden mint over dark chocolate and sweet cream, cool and long.",
}
ABV_LABEL = "13% ABV"
VOLUME_LABEL = "700 ML"
COLLECTION_LABEL = "NOCTURNE N.02"

CHAPTER_KEYS = (
    "wander", "profile", "approach", "near", "hand", "target", "transition",
    "cathedral", "drink-selection", "drink-pour", "anti-gravity", "pillar-crumble",
    "colosseum", "taste", "collection", "products", "retail", "footer",
)
NARRATION_OPENING = "IN AN IMMENSE LAND OF NOTHINGNESS."
NARRATION_EMPHASIS = "IMMENSE LAND"
POSTER_PROSE = (
    "Chill your spirit. The night starts after dinner. Shake your spirit. "
    "Let the night play on. Pour your spirit. What happens next is up to you."
)
PROMISE_LINE = "INDULGE NOW"
PROMISE_SECOND = "ATONE LATER"
TITLE_LOCKUP = "THE NOCTURNE EXPERIENCE"
RETAIL_LINE = "Select Houses Forthcoming"
CONTENT_KEYS = ("releases", "flavours", "chapters", "credits", "legal")
AGE_QUESTION = "Are you of legal age?"
ROTATE_LINE = "Please rotate your device."
UNSUPPORTED_LINE = "Your browser is not supported"
CONTROL_NAMES = ("Toggle audio", "previous slide", "next slide", "left text", "right text")
PORTAL_PROMPT = "HOLD & MOVE"
POUR_PROMPT = "HOLD & POUR"

RELEASE_MAIN = "N02"
RELEASE_CASK = "N02-CASK"
RELEASE_SALON = "N02-SALON"
RELEASE_CLOSED = "N01"
RELEASE_UPCOMING = "N04"
RELEASE_EMBER = "N02-EMBER"
RELEASE_SALON_NAME = "Nocturne N.02 Salon Pour"
MAIN_TOTAL = 240
MAIN_REMAINING_AT_SEED = 239
HOLD_HOURS = 72
SESSION_DAYS = 14
SEEDED_RELEASES = 7
SEEDED_PLACES = 8

SIGN_IN_SUBJECT = "Your Vesperi sign-in link"
SIGN_IN_CODE_PREFIX = "Sign-in code:"
OFFER_SUBJECT = "A bottle came back for you:"
ALERT_SET_SUBJECT = "Alert set:"
ALERT_FIRED_SUBJECT = "It has landed near you:"
BOOKED_SUBJECT = "Tasting booked:"
CANCELLED_SUBJECT = "Tasting cancelled:"
CANCEL_LINK_PREFIX = "Cancel this alert:"
ALERT_CANCEL_ROUTE = "/alerts/cancel"
ALERT_OFF_LINE = "THAT ALERT IS OFF"

PLACE_SOHO = "Soho"
PLACE_SHOREDITCH = "Shoreditch"
PLACE_LEITH = "Leith"
PLACE_NEWPORT = "Newport"
PLACE_BERGEN = "Bergen"
NEWPORT_DETAILS = ("Wales", "Isle of Wight")
SOHO_LAT = 51.5136
SOHO_LNG = -0.1340
LEITH_LAT = 55.9755
LEITH_LNG = -3.1665
BERGEN_LAT = 60.3913
BERGEN_LNG = 5.3221
REGION_RESTRICTED = "NO"
RESTRICTED_NOTICE = "Listing where drink is sold is not permitted in this region."
VENUE_GILDED = "The Gilded Nave"
VENUE_SALT = "Salt & Vesper"
GILDED_DISTANCE = "0.2"
SALT_DISTANCE = "4.1"
STOCK_READINGS = ("in", "low", "out", "unknown")
RADIUS_MIN = 1
RADIUS_MAX = 50

SESSION_NIGHT = "Nocturne Night at The Gilded Nave"
SESSION_LATE_POUR = "Late Pour at Salt & Vesper"
SESSION_LAST_CALL = "Last Call at Salt & Vesper"
SESSION_CHAPEL = "Cellar Tasting at The Chapel Cellar"
SESSION_SOLD_OUT = "Sold Out Supper at The Gilded Nave"
SESSION_PARIS = "Soiree Nocturne at Le Confessionnal"
SESSION_EARLY = "Early Pour at Salt & Vesper"
NIGHT_PRICE = 3500
CURRENCY = "usd"
ZONE_LONDON = "Europe/London"
ZONE_PARIS = "Europe/Paris"
CHAPEL_CAPACITY = 2
PARTY_MIN = 1
PARTY_MAX = 8

MIXER_IDS = ("cold-brew", "tonic", "oat-milk", "soda", "espresso", "ginger-ale")
ICE_IDS = ("no-ice", "cubed", "crushed", "single-block")
GARNISH_IDS = ("no-garnish", "orange-twist", "mint-sprig", "grated-nutmeg", "cocoa-dust")
WITHDRAWN_GARNISH = "gold-leaf"
SEEDED_RITUAL_SLUG = "midnight-confession-a1b2"
SEEDED_RITUAL_NAME = "Midnight Confession"
RITUAL_SAVES_PER_HOUR = 5
RITUAL_SHARED_LINE = "SOMEONE POURED THIS FOR YOU"
RITUAL_GONE_LINE = "THAT ONE IS GONE. POUR YOUR OWN"
SLUG_PATTERN = r"^velvet-hour-[a-z0-9]{4}$"

REASON_INVALID_TOKEN = "invalid_token"
REASON_INVALID_FLAVOUR = "invalid_flavour"
REASON_CLOSED = "closed"
REASON_ALREADY_HELD = "already_held"
REASON_EXHAUSTED = "exhausted"
REASON_NOT_OFFERED = "not_offered"
REASON_INVALID_RADIUS = "invalid_radius"
REASON_RESTRICTED = "restricted"
REASON_INVALID_PARTY = "invalid_party_size"
REASON_INSUFFICIENT = "insufficient"
REASON_HOLD_ELSEWHERE = "hold_elsewhere"
REASON_LATE = "late"
REASON_ALREADY_RESCHEDULED = "already_rescheduled"
REASON_TOO_MANY_MIXERS = "too_many_mixers"
REASON_INVALID_INGREDIENT = "invalid_ingredient"
REASON_NAME_REFUSED = "name_refused"
REASON_RATE_LIMITED = "rate_limited"
REASON_INVALID_NAME = "invalid_name"
REASON_EDIT_WINDOW = "edit_window_closed"

TERMS_ROUTE = "/terms"
SIGN_IN_ROUTE = "/sign-in"
STILL_ROUTE = "/?mode=still"
UNSUPPORTED_ROUTE = "/unsupported"
PUBLIC_ROUTES = ("/where", "/tastings", "/ritual", "/terms")
ADDITION_ROUTES = ("/cellar", "/where", "/tastings", "/ritual")
FAVICON_ROUTE = "/favicon.ico"
SITEMAP_ROUTE = "/sitemap.xml"
ROBOTS_ROUTE = "/robots.txt"
SOCIAL_IMAGE_ROUTE = "/og/default.png"
IDEMPOTENCY_HEADER = "Idempotency-Key"

DENIED = (401, 403)
DENIED_OR_MISSING = (401, 403, 404)
CREATED = (200, 201)
ACCEPTED = (200, 202)
NO_CONTENT = (200, 204)
REFUSED = (400, 409, 422)
CONFLICT = (409,)
RATE_LIMITED_STATUS = (429,)

SETTLE_SECONDS = 1.0
POLL_BUDGET_SECONDS = 45.0


def settle() -> None:
    """The only sanctioned sleep in this suite."""
    time.sleep(SETTLE_SECONDS)


def deadline(seconds: float = POLL_BUDGET_SECONDS) -> float:
    return time.monotonic() + seconds


def poll_until(check, budget: float = POLL_BUDGET_SECONDS):
    """Bounded poll to a monotonic deadline. Returns the first truthy result."""
    stop = deadline(budget)
    last = None
    while time.monotonic() < stop:
        last = check()
        if last:
            return last
        settle()
    return last


def probe_suffix() -> str:
    return os.urandom(6).hex()


def probe_email(tag: str) -> str:
    return f"probe-{tag}-{probe_suffix()}@example.com"


def hours_until(instant: str) -> float:
    """Hours from now until an ISO-8601 instant the server issued."""
    value = datetime.datetime.fromisoformat(str(instant).replace("Z", "+00:00"))
    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.timezone.utc)
    now = datetime.datetime.now(datetime.timezone.utc)
    return (value - now).total_seconds() / 3600.0


def api(path: str) -> str:
    return f"{api_base()}{path}"


def page(path: str) -> str:
    return f"{app_url()}{path}"


def get_page(path: str) -> httpx.Response:
    return httpx.get(page(path), timeout=30.0, follow_redirects=True)


def body_of(response) -> dict:
    payload = response.json()
    if isinstance(payload, dict) and isinstance(payload.get("data"), dict):
        return payload["data"]
    return payload


def reason_of(response) -> str:
    """The stable `reason` string this brief pins on every refusal."""
    if "json" not in response.headers.get("content-type", "").lower():
        return ""
    payload = response.json()
    if not isinstance(payload, dict):
        return ""
    if payload.get("reason"):
        return str(payload["reason"])
    error = payload.get("error")
    if isinstance(error, dict) and error.get("reason"):
        return str(error["reason"])
    return ""


def unescape(text: str) -> str:
    return (text.replace("&amp;", "&").replace("&#38;", "&").replace("&#x26;", "&")
            .replace("&#39;", "'").replace("&apos;", "'").replace("&quot;", '"'))


def token_for(email: str) -> str:
    return login(email, seeded_password("SEED_VISITOR_PASSWORD", SEEDED_PASSWORD_DEFAULT))


@pytest.fixture(scope="session")
def inbox():
    return make_inbox()


def wait_for_mail(inbox_, to: str, subject: str):
    return poll_until(lambda: inbox_.find(to=to, subject_contains=subject))


def request_link(email: str) -> httpx.Response:
    return httpx.post(api("/v1/auth/link"), json={"email": email, "returnTo": "/"}, timeout=30.0)


def sign_in_code(inbox_, email: str) -> str:
    message = wait_for_mail(inbox_, email, SIGN_IN_SUBJECT)
    assert message is not None, (
        f"no message titled {SIGN_IN_SUBJECT!r} reached {email} in Mailpit after "
        f"POST /api/v1/auth/link"
    )
    found = re.search(r"Sign-in code:\s*([A-Za-z0-9_-]{24,})", message.body)
    assert found, (
        f"the sign-in message to {email} does not open with {SIGN_IN_CODE_PREFIX!r} "
        f"followed by a code: {message.body[:300]!r}"
    )
    return found.group(1)


def exchange(code: str) -> httpx.Response:
    return httpx.post(api("/v1/auth/session"), json={"token": code}, timeout=30.0)


def session_token_of(response) -> str:
    body = body_of(response)
    value = body.get("session") or body.get("access_token")
    assert value, f"the session exchange returned no session token: {response.text[:300]}"
    return str(value)


def fresh_visitor(inbox_, tag: str) -> tuple[str, str]:
    """Open a brand-new visitor account through the product's own sign-in link."""
    email = probe_email(tag)
    sent = request_link(email)
    assert sent.status_code in ACCEPTED, (
        f"POST /api/v1/auth/link for {email} returned {sent.status_code}: {sent.text[:300]}"
    )
    response = exchange(sign_in_code(inbox_, email))
    assert response.status_code in CREATED, (
        f"POST /api/v1/auth/session for {email} returned {response.status_code}: "
        f"{response.text[:300]}"
    )
    return email, session_token_of(response)


@pytest.fixture(scope="session")
def anon_client():
    with client() as c:
        yield c


@pytest.fixture
def visitor_token() -> str:
    return token_for(VISITOR_EMAIL)


@pytest.fixture
def visitor_client(visitor_token: str):
    with client(visitor_token) as c:
        yield c


@pytest.fixture
def visitor2_client():
    with client(token_for(VISITOR2_EMAIL)) as c:
        yield c


@pytest.fixture
def host_client():
    with client(token_for(HOST_EMAIL)) as c:
        yield c


@pytest.fixture
def host2_client():
    with client(token_for(HOST2_EMAIL)) as c:
        yield c


class CellarStore:
    """Domain queries for this task, composed from the generic primitives."""

    def __init__(self, backend: Backend) -> None:
        self._b = backend

    def user_row(self, email: str) -> dict | None:
        return self._b.one("app_user", email=email)

    def count_users(self, email: str) -> int:
        return self._b.count("app_user", email=email)

    def release_row(self, release_id: str) -> dict | None:
        return self._b.one("release", id=release_id)

    def count_releases(self) -> int:
        return self._b.count("release")

    def allocations_for_release(self, release_id: str) -> list[dict]:
        return self._b.rows("allocation", limit=2000, release_id=release_id)

    def allocations_for_user(self, user_id) -> list[dict]:
        return self._b.rows("allocation", limit=200, user_id=user_id)

    def allocation_row(self, allocation_id) -> dict | None:
        return self._b.one("allocation", id=allocation_id)

    def live_allocations(self, release_id: str) -> int:
        return sum(1 for row in self.allocations_for_release(release_id)
                   if str(row.get("state")) in ("held", "offered", "confirmed"))

    def count_flavours(self) -> int:
        return self._b.count("flavour")

    def count_chapters(self) -> int:
        return self._b.count("chapter")

    def venue_row(self, name: str) -> dict | None:
        return self._b.one("venue", name=name)

    def count_venues(self) -> int:
        return self._b.count("venue")

    def stock_row(self, venue_name: str, flavour_id: str) -> dict | None:
        venue = self.venue_row(venue_name)
        assert venue is not None, f"venue has no row named {venue_name!r}"
        return self._b.one("venue_stock", venue_id=venue["id"], flavour_id=flavour_id)

    def alerts_for_user(self, user_id) -> list[dict]:
        return self._b.rows("landing_alert", limit=200, user_id=user_id)

    def session_row(self, title: str) -> dict | None:
        return self._b.one("tasting_session", title=title)

    def count_sessions(self) -> int:
        return self._b.count("tasting_session")

    def bookings_for_session(self, session_id) -> list[dict]:
        return self._b.rows("booking", limit=500, session_id=session_id)

    def bookings_for_user(self, user_id) -> list[dict]:
        return self._b.rows("booking", limit=200, user_id=user_id)

    def active_holds_for_session(self, session_id) -> list[dict]:
        return self._b.rows("seat_hold", limit=500, session_id=session_id, state="active")

    def ritual_row(self, slug: str) -> dict | None:
        return self._b.one("ritual", slug=slug)

    def rituals_for_user(self, user_id) -> list[dict]:
        return self._b.rows("ritual", limit=200, user_id=user_id)

    def count_places(self) -> int:
        return self._b.count("place")

    def count_cookie_choices(self) -> int:
        return self._b.count("cookie_choice")


@pytest.fixture(scope="session")
def db() -> CellarStore:
    return CellarStore(make_backend())


def user_id_of(db_: CellarStore, email: str):
    row = db_.user_row(email)
    assert row is not None, f"app_user has no row for {email!r}"
    return row["id"]


def claim(client_, release_id: str, flavour: str, key: str | None = None):
    headers = {IDEMPOTENCY_HEADER: key} if key else {}
    return client_.post("/v1/cellar/holds", json={"releaseId": release_id, "flavour": flavour},
                        headers=headers)


def allocation_id_of(response) -> str:
    body = body_of(response)
    value = body.get("allocationId") or body.get("id")
    assert value is not None, f"the hold response carries no allocationId: {response.text[:300]}"
    return str(value)


def cellar_items(client_) -> list[dict]:
    response = client_.get("/v1/cellar")
    assert response.status_code == 200, (
        f"GET /api/v1/cellar returned {response.status_code}: {response.text[:300]}"
    )
    return items(response.json())


def item_for(client_, allocation_id: str) -> dict:
    for entry in cellar_items(client_):
        if str(entry.get("allocationId")) == str(allocation_id):
            return entry
    raise AssertionError(f"GET /api/v1/cellar lists no item with allocationId {allocation_id}")


def place_by_name(name: str, detail: str | None = None) -> dict:
    response = httpx.get(api("/v1/places"), params={"q": name}, timeout=30.0)
    assert response.status_code == 200, (
        f"GET /api/v1/places?q={name} returned {response.status_code}: {response.text[:300]}"
    )
    for entry in items(response.json()):
        if str(entry.get("name")) == name and (detail is None or detail in str(entry.get("detail"))):
            return entry
    raise AssertionError(f"GET /api/v1/places?q={name} lists no place named {name!r}")


def venues_near(lat: float, lng: float, radius, flavour: str | None = None) -> httpx.Response:
    params = {"lat": lat, "lng": lng, "radius": radius}
    if flavour:
        params["flavour"] = flavour
    return httpx.get(api("/v1/venues"), params=params, timeout=30.0)


def venue_list(response) -> list[dict]:
    body = response.json()
    assert isinstance(body, dict) and isinstance(body.get("venues"), list), (
        f"GET /api/v1/venues did not answer {{region, venues}}: {response.text[:300]}"
    )
    return body["venues"]


def set_alert(client_, place_id, radius, flavour: str | None):
    return client_.post("/v1/alerts", json={"place": place_id, "radius": radius, "flavour": flavour})


def session_by_title(title: str) -> dict:
    response = httpx.get(api("/v1/tastings"), timeout=30.0)
    assert response.status_code == 200, (
        f"GET /api/v1/tastings returned {response.status_code}: {response.text[:300]}"
    )
    for entry in items(response.json()):
        if str(entry.get("title")) == title:
            return entry
    raise AssertionError(f"GET /api/v1/tastings lists no session titled {title!r}")


def hold_seats(client_, session_id, party_size):
    return client_.post(f"/v1/tastings/{session_id}/holds", json={"partySize": party_size})


def hold_id_of(response) -> str:
    body = body_of(response)
    value = body.get("holdId") or body.get("id")
    assert value is not None, f"the seat hold response carries no holdId: {response.text[:300]}"
    return str(value)


def book(client_, hold_id, email: str, key: str | None = None):
    headers = {IDEMPOTENCY_HEADER: key} if key else {}
    return client_.post("/v1/bookings", json={"holdId": hold_id, "name": "Probe Guest",
                                               "email": email, "notes": ""}, headers=headers)


def booking_id_of(response) -> str:
    body = body_of(response)
    value = body.get("id") or body.get("bookingId")
    assert value is not None, f"the booking response carries no id: {response.text[:300]}"
    return str(value)


def ritual_body(name: str, garnish: str = "cocoa-dust", mixers=("cold-brew", "oat-milk")) -> dict:
    return {"flavour": FLAVOUR_MARSHMALLOW, "mixers": list(mixers), "ice": "crushed",
            "garnish": garnish, "name": name}


def slug_of(response) -> str:
    value = body_of(response).get("slug")
    assert value, f"the ritual save returned no slug: {response.text[:300]}"
    return str(value)


def _squash(text: str) -> str:
    return " ".join(unescape(text).split()).lower()


def has_text(html: str, needle: str) -> bool:
    """True when the needle is in the page's text, with or without its markup."""
    wanted = _squash(needle)
    if wanted in _squash(html):
        return True
    return wanted in _squash(re.sub(r"<[^>]+>", " ", html)) or wanted in _squash(re.sub(r"<[^>]+>", "", html))


def flat(payload) -> str:
    return flatten(payload)
