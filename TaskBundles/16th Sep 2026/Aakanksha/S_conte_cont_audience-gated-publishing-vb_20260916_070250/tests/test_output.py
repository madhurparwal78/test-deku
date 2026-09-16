"""Black-box graders for the audience-gated-publishing workbench.

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
    AUTHOR_EMAIL,
    DISCOUNT_CODE,
    DISCOUNTED_PRICE_MINOR,
    EDITION_OBJECT_PREFIX,
    FREE_READER_EMAIL,
    MIN_COHORT,
    PREMIUM_PRICE_MINOR,
    PREMIUM_TIER,
    READER_EMAIL,
    account_password,
    fresh_email,
    poll,
    settle,
)
from _shapes import flatten, items


def _post_body() -> str:
    return ("The audience field turns a paywall into a spatial decision. "
            "This is the free opening that any visitor may read before the gate.")


def _create_post(c, free_words: int = 12):
    body = {"title": "Gating post " + os.urandom(4).hex(),
            "body": _post_body(), "free_words": free_words}
    return c.post("/posts", json=body)


def _publish_gated_post(author_client, tier: str = PREMIUM_TIER) -> dict:
    """Create, gate and publish a post; return the published post payload."""
    post = _create_post(author_client).json()
    pid = str(post.get("id"))
    author_client.post(f"/posts/{pid}/gate", json={"tier": tier})
    published = author_client.post(f"/posts/{pid}/publish", json={}).json()
    published.setdefault("id", pid)
    return published


def _new_reader_token() -> str:
    """Sign up a fresh reader and return their bearer token."""
    email = fresh_email("reader")
    with client() as c:
        resp = c.post("/auth/signup",
                      json={"email": email, "password": account_password(), "role": "reader"})
    token = resp.json().get("token")
    assert token, f"a fresh reader signup returned no token: {resp.text[:300]}"
    return token


def _ledger_transaction_count(author_client) -> int:
    rows = items(author_client.get("/ledger").json())
    return len({str(r.get("transaction_id")) for r in rows})


def test_health_ok():
    """The health endpoint returns ready."""
    with client() as c:
        resp = c.get("/health")
    assert resp.status_code == 200, f"health was not ready: {resp.status_code}"


def test_seeded_accounts_login(author_client):
    """The seeded publisher authenticates and reads their own posts."""
    resp = author_client.get("/posts")
    assert resp.status_code == 200, f"seeded author could not read posts: {resp.text[:300]}"


def test_signup_rejects_duplicate_email(anon_client):
    """A signup for an already registered email is refused."""
    resp = anon_client.post("/auth/signup",
                            json={"email": AUTHOR_EMAIL, "password": account_password(),
                                  "role": "reader"})
    assert resp.status_code in (400, 409, 422), (
        f"a duplicate signup was accepted: {resp.status_code} {resp.text[:300]}")


def test_signup_rejects_short_password(anon_client):
    """A signup with a password shorter than eight characters is refused."""
    resp = anon_client.post("/auth/signup",
                            json={"email": fresh_email(), "password": "short", "role": "reader"})
    assert resp.status_code in (400, 422), (
        f"a short password was accepted: {resp.status_code} {resp.text[:300]}")


def test_author_creates_draft_post(author_client):
    """An author creates a post as a draft."""
    resp = _create_post(author_client)
    assert resp.status_code in (200, 201), f"draft creation failed: {resp.text[:300]}"
    body = resp.json()
    assert str(body.get("status")) == "draft", (
        f"a new post was not a draft: {flatten(body)[:300]}")


def test_projection_reach_counts_cohort(author_client):
    """A free-tier projection counts the whole audience and is sufficient."""
    post_id = str(_create_post(author_client).json().get("id"))
    payload = author_client.get(f"/posts/{post_id}/projection", params={"tier": "free"}).json()
    reach = payload.get("reach")
    assert reach is not None and reach >= MIN_COHORT, (
        f"the free-tier reach was below the minimum cohort: {flatten(payload)[:300]}")
    assert payload.get("sufficient") is True, (
        f"a free-tier projection over the whole audience was not sufficient: {flatten(payload)[:300]}")


def test_projection_refuses_below_min_cohort(author_client):
    """A premium-tier projection over a cohort below the minimum refuses."""
    post_id = str(_create_post(author_client).json().get("id"))
    payload = author_client.get(f"/posts/{post_id}/projection", params={"tier": PREMIUM_TIER}).json()
    assert payload.get("sufficient") is False, (
        f"a projection below the minimum cohort claimed to be sufficient: {flatten(payload)[:300]}")
    assert payload.get("projected_revenue") in (None, 0, "", "null"), (
        f"a projection below the minimum cohort still returned a revenue figure: {flatten(payload)[:300]}")


def test_gate_commit_writes_paywall(author_client):
    """Committing the gate writes the post's paywall tier."""
    post_id = str(_create_post(author_client).json().get("id"))
    resp = author_client.post(f"/posts/{post_id}/gate", json={"tier": PREMIUM_TIER})
    assert resp.status_code in (200, 201), f"gate commit failed: {resp.text[:300]}"
    fetched = author_client.get(f"/posts/{post_id}").json()
    assert str(fetched.get("gate_tier")) == PREMIUM_TIER, (
        f"the committed gate tier was not persisted: {flatten(fetched)[:300]}")


def test_gate_rejects_unknown_tier(author_client):
    """A gate naming a tier that does not exist is refused."""
    post_id = str(_create_post(author_client).json().get("id"))
    resp = author_client.post(f"/posts/{post_id}/gate", json={"tier": "platinum"})
    assert resp.status_code in (400, 404, 422), (
        f"an unknown gate tier was accepted: {resp.status_code} {resp.text[:300]}")


def test_gated_edition_streams_to_entitled_subscriber(author_client, reader_client):
    """A gated audio edition streams to an entitled premium subscriber."""
    post = _publish_gated_post(author_client)
    post_id = str(post.get("id"))
    resp = poll(lambda: reader_client.get(f"/posts/{post_id}/audio"),
                lambda r: r.status_code in (200, 206))
    assert resp.status_code in (200, 206), (
        f"an entitled subscriber could not play the gated edition: {resp.status_code}")


def test_privacy_page_served():
    """The privacy page renders readable content."""
    with client() as c:
        resp = c.get("/../privacy")
    assert resp.status_code == 200, f"the privacy page did not render: {resp.status_code}"
    assert len(resp.text) > 200, "the privacy page carried no readable content"


def test_internal_links_resolve():
    """Every internal link on the public home page resolves."""
    with client() as c:
        home = c.get("/../")
        assert home.status_code == 200, f"the public home did not render: {home.status_code}"
        import re
        paths = []
        for href in re.findall(r'href="(/[^"#?]*)"', home.text):
            if not href.startswith("/api") and href not in paths:
                paths.append(href)
        for path in paths[:10]:
            resp = c.get("/.." + path)
            assert resp.status_code in (200, 304), (
                f"an internal link {path} did not resolve: {resp.status_code}")


def test_publish_stores_one_audio_object(author_client, object_store):
    """Publishing a post stores exactly one new audio edition object."""
    before = len(object_store.list(prefix=EDITION_OBJECT_PREFIX))
    _publish_gated_post(author_client)
    after = poll(lambda: len(object_store.list(prefix=EDITION_OBJECT_PREFIX)),
                 lambda n: n >= before + 1)
    assert after - before == 1, (
        f"expected one new object under {EDITION_OBJECT_PREFIX}, delta was {after - before}; "
        f"the audio was held on local disk or in the database, not the bucket")


def test_audio_edition_persisted_as_object_not_db_blob(author_client, object_store):
    """A published post names a stored edition object that exists in the bucket."""
    post = _publish_gated_post(author_client)
    key = post.get("audio_key")
    assert key, f"the published post carried no audio_key: {flatten(post)[:300]}"
    exists = poll(lambda: object_store.exists(key), lambda ok: bool(ok))
    assert exists, f"the audio edition object {key} is absent from the store"


def test_subscribe_books_balanced_ledger_pair(author_client):
    """A subscription charge books a balanced ledger transaction."""
    token = _new_reader_token()
    with client(token) as c:
        resp = c.post("/subscriptions", json={"tier": PREMIUM_TIER})
        assert resp.status_code in (200, 201), f"subscribe failed: {resp.text[:300]}"
    rows = poll(lambda: items(author_client.get("/ledger").json()), lambda r: bool(r))
    assert rows, "the ledger recorded no entries after a subscribe"
    by_txn: dict[str, list] = {}
    for row in rows:
        by_txn.setdefault(str(row.get("transaction_id")), []).append(row)
    for entries in by_txn.values():
        debit = sum(int(e.get("amount_minor", 0)) for e in entries
                    if str(e.get("direction")) == "debit")
        credit = sum(int(e.get("amount_minor", 0)) for e in entries
                     if str(e.get("direction")) == "credit")
        assert len(entries) >= 2, f"a ledger transaction posted fewer than two entries: {entries}"
        assert debit == credit, (
            f"a ledger transaction was unbalanced: debit {debit} credit {credit}")


def test_ledger_reconciles_debits_equal_credits(author_client):
    """Across the publication the ledger reconciles debits against credits."""
    token = _new_reader_token()
    with client(token) as c:
        c.post("/subscriptions", json={"tier": PREMIUM_TIER})
    rows = poll(lambda: items(author_client.get("/ledger").json()), lambda r: bool(r))
    assert rows, "the ledger recorded no entries"
    debit = sum(int(r.get("amount_minor", 0)) for r in rows if str(r.get("direction")) == "debit")
    credit = sum(int(r.get("amount_minor", 0)) for r in rows if str(r.get("direction")) == "credit")
    assert debit == credit and debit > 0, (
        f"the ledger did not reconcile: total debit {debit} total credit {credit}")


def test_release_creates_deliveries_no_duplicates(author_client):
    """Re-releasing a post to a segment creates no duplicate delivery."""
    post = _publish_gated_post(author_client, tier="free")
    post_id = str(post.get("id"))
    first = author_client.post(f"/posts/{post_id}/release", json={"segment": "all"})
    assert first.status_code in (200, 201), f"release failed: {first.text[:300]}"
    resolved = first.json().get("resolved_recipients")
    count_after_first = poll(
        lambda: len(items(author_client.get("/deliveries", params={"post_id": post_id}).json())),
        lambda n: n >= 1)
    author_client.post(f"/posts/{post_id}/release", json={"segment": "all"})
    settle()
    count_after_second = len(items(
        author_client.get("/deliveries", params={"post_id": post_id}).json()))
    assert count_after_second == count_after_first, (
        f"re-releasing created duplicate deliveries: {count_after_first} then {count_after_second}")
    if resolved is not None:
        assert count_after_first == resolved, (
            f"the delivery count {count_after_first} did not match the resolved recipients {resolved}")


def test_seed_is_idempotent(author_client):
    """The seeded tiers hold a stable set across reads."""
    first = len(items(author_client.get("/tiers").json()))
    second = len(items(author_client.get("/tiers").json()))
    assert first == second and first > 0, (
        f"the seeded tier set drifted between reads: {first} then {second}")


def test_premium_price_is_eight_hundred(author_client):
    """The seeded premium tier is priced at the pinned minor units."""
    tiers = items(author_client.get("/tiers").json())
    assert tiers, "the tiers endpoint returned nothing"
    premium = [t for t in tiers if str(t.get("name")) == PREMIUM_TIER]
    assert premium, f"no premium tier was seeded: {tiers}"
    assert int(premium[0].get("price_minor")) == PREMIUM_PRICE_MINOR, (
        f"the premium price was {premium[0].get('price_minor')}, expected {PREMIUM_PRICE_MINOR}")


def test_discount_resolves_amount():
    """Applying the seeded offer resolves the charged amount."""
    token = _new_reader_token()
    with client(token) as c:
        resp = c.post("/subscriptions", json={"tier": PREMIUM_TIER, "offer_code": DISCOUNT_CODE})
    assert resp.status_code in (200, 201), f"discounted subscribe failed: {resp.text[:300]}"
    amount = resp.json().get("amount_minor")
    assert int(amount) == DISCOUNTED_PRICE_MINOR, (
        f"the discounted amount was {amount}, expected {DISCOUNTED_PRICE_MINOR}")


def test_concurrent_duplicate_key_creates_single_subscription():
    """Two simultaneous subscribes with one key create exactly one subscription."""
    token = _new_reader_token()
    key = "idem-" + os.urandom(6).hex()
    gate = threading.Barrier(2)
    lock = threading.Lock()
    statuses: list[int] = []

    def fire():
        with client(token) as c:
            gate.wait()
            resp = c.post("/subscriptions", json={"tier": PREMIUM_TIER},
                          headers={"Idempotency-Key": key})
        with lock:
            statuses.append(resp.status_code)

    threads = [threading.Thread(target=fire) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)
    created = [s for s in statuses if s in (200, 201)]
    assert created, f"neither duplicated subscribe succeeded: {sorted(statuses)}"
    with client(token) as c:
        rows = items(c.get("/subscriptions").json())
    active = [r for r in rows if str(r.get("status")) == "active"
              and str(r.get("tier")) == PREMIUM_TIER]
    assert len(active) == 1, (
        f"a duplicated key created {len(active)} active subscriptions; exactly one must exist")


def test_subscribe_replay_no_second_ledger_transaction(author_client):
    """A replayed subscribe with the same key books no second ledger transaction."""
    token = _new_reader_token()
    key = "idem-" + os.urandom(6).hex()
    body = {"tier": PREMIUM_TIER}
    with client(token) as c:
        first = c.post("/subscriptions", json=body, headers={"Idempotency-Key": key})
        assert first.status_code in (200, 201), f"first subscribe failed: {first.text[:300]}"
        first_id = str(first.json().get("id"))
        settle()
        before = _ledger_transaction_count(author_client)
        replay = c.post("/subscriptions", json=body, headers={"Idempotency-Key": key})
    assert replay.status_code in (200, 201), f"replay was not accepted idempotently: {replay.text[:300]}"
    assert str(replay.json().get("id")) == first_id, (
        "a replay with the same key returned a different subscription id")
    after = _ledger_transaction_count(author_client)
    assert after == before, (
        f"a replay booked a second ledger transaction: {before} then {after}")


def test_gated_edition_denied_to_free_reader(author_client, free_reader_client, anon_client):
    """A gated audio edition is refused to a free reader and an anonymous caller."""
    post = _publish_gated_post(author_client)
    post_id = str(post.get("id"))
    owner = author_client.get(f"/posts/{post_id}/audio")
    assert owner.status_code in (200, 206), f"the author could not read their own edition: {owner.status_code}"
    free = free_reader_client.get(f"/posts/{post_id}/audio")
    assert free.status_code in (401, 403, 404), (
        f"a free reader read a gated edition: {free.status_code}")
    anon = anon_client.get(f"/posts/{post_id}/audio")
    assert anon.status_code in (401, 403, 404), (
        f"an anonymous caller read a gated edition: {anon.status_code}")


def test_reader_cannot_author_forbidden(reader_client):
    """A reader is refused writing a post."""
    resp = reader_client.post("/posts", json={"title": "x", "body": "y", "free_words": 5})
    assert resp.status_code in (401, 403), (
        f"a reader was allowed to author a post: {resp.status_code} {resp.text[:300]}")


def test_reader_denied_author_endpoint(reader_client):
    """A reader is refused an author-only audience endpoint."""
    resp = reader_client.get("/subscribers")
    assert resp.status_code in (401, 403), (
        f"a reader reached an author-only endpoint: {resp.status_code} {resp.text[:300]}")


def test_unauthenticated_access_denied(anon_client):
    """An anonymous caller is refused every protected endpoint."""
    protected = [("POST", "/posts"), ("GET", "/subscribers"), ("GET", "/ledger")]
    for method, path in protected:
        resp = anon_client.request(method, path, json={})
        assert resp.status_code in (401, 403), (
            f"anonymous {method} {path} was served: {resp.status_code}")


def test_no_frontend_secret_in_bundle():
    """The served frontend carries no storage or database secret."""
    with client() as c:
        resp = c.get("/../")
    assert resp.status_code == 200, f"the app root did not render: {resp.status_code}"
    secret = os.environ.get("STORAGE_SECRET_KEY", "deku-local-dev")
    assert secret not in resp.text, "a storage secret was served in the frontend document"


def test_posts_pagination_cursor(author_client):
    """The posts read is paginated with a forward cursor and metadata."""
    for _ in range(2):
        _create_post(author_client)
    payload = author_client.get("/posts", params={"page_size": 1}).json()
    assert "next_cursor" in payload or payload.get("has_more") is not None, (
        f"the paginated response carried no cursor metadata: {flatten(payload)[:300]}")
    rows = items(payload)
    assert len(rows) <= 1, f"page_size was ignored, got {len(rows)} rows"


def test_sitemap_lists_public_routes_and_robots():
    """A sitemap lists public routes and a robots file references it."""
    with client() as c:
        sitemap = c.get("/../sitemap.xml")
        robots = c.get("/../robots.txt")
    assert sitemap.status_code == 200, f"the sitemap did not render: {sitemap.status_code}"
    assert "/" in sitemap.text and len(sitemap.text) > 20, "the sitemap listed no routes"
    assert robots.status_code == 200, f"the robots file did not render: {robots.status_code}"
    assert "sitemap" in robots.text.lower(), "the robots file did not reference the sitemap"


def test_social_preview_tags_present():
    """The public home page declares a social preview title and a preview image."""
    with client() as c:
        home = c.get("/../")
    assert home.status_code == 200, f"the public home did not render: {home.status_code}"
    text = home.text.lower()
    assert 'og:title' in text or 'property="og:title"' in text, (
        "the page declared no social preview title")
    assert 'og:image' in text, "the page declared no social preview image"


def test_content_images_have_alt_text():
    """Every content image on the public home page carries alternative text."""
    with client() as c:
        home = c.get("/../")
    assert home.status_code == 200, f"the public home did not render: {home.status_code}"
    import re
    imgs = re.findall(r"<img\b[^>]*>", home.text, flags=re.IGNORECASE)
    for tag in imgs:
        assert re.search(r'\balt\s*=', tag, flags=re.IGNORECASE), (
            f"a content image carried no alternative text: {tag[:120]}")
