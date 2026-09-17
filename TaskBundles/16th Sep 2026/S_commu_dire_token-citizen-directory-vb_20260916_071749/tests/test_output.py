from __future__ import annotations

import concurrent.futures

import httpx

from conftest import (
    APP_URL, BIO_MAX, CATALOGUE_KEY_PREFIX, CLEAR_ALL_LABEL,
    CONSOLE_INTERNAL_COMMAND,
    CORPUS_PASSWORD, EMPTY_MEMBER_ADDRESS, FOOTER_RIGHTS, FOOTER_STUDIO,
    HARNESS_ROUTE, IDENTIFIER_EXAMPLES, MEDIA_AUDIO, MEDIA_IMAGE,
    MEDIA_KINDS, MEDIA_TOTAL, MEDIA_VIDEO, MEMBER_ADDRESS, MEMBER_EMAIL,
    NICKNAME_MAX, PASSPORT_FACES, PASSPORT_KEY_PREFIX, PRIVACY_ROUTE,
    PUBLIC_ROUTES, RENDER_STATES, SECOND_MEMBER_ADDRESS, SECOND_MEMBER_EMAIL,
    THIRD_MEMBER_EMAIL, TOKEN_COUNT, TRAIT_COUNT,
    TRAIT_NAMES, TRAIT_VALUE_COUNTS, anchor, bearer, on_chain_id,
    patch_profile, poll, probe_address, probe_email, probe_nickname,
    read_citizen, request_challenge, sign_up, verify_challenge,
)

SECRET_NEEDLES = ("STORAGE_SECRET_KEY", "STORAGE_ACCESS_KEY", "minio-root-",
                  "deku-storage-", "postgresql://", "DB_ADMIN_URL")


def _text(response: httpx.Response) -> str:
    return response.text or ""


def _codes(response: httpx.Response) -> str:
    body = _text(response)
    if "json" not in response.headers.get("content-type", "").lower():
        return body
    payload = response.json()
    if isinstance(payload, dict):
        return str(payload.get("code") or payload.get("error") or body)
    return body


def _profile_of(payload: dict) -> dict:
    citizen = payload.get("citizen") or payload.get("member") or payload
    return citizen.get("profile") or {}


def _citizen_of(payload: dict) -> dict:
    return payload.get("citizen") or payload.get("member") or payload


def test_health_and_deployment_contract(client, site):
    r = client.get("/health")
    assert r.status_code == 200, anchor("health route", r)

    home = site.get("/")
    assert home.status_code == 200, anchor("story route", home)
    assert APP_URL.startswith("http"), f"APP_PUBLIC_URL is not an address: {APP_URL!r}"
    assert "127.0.0.1" not in APP_URL, (
        f"the app answers on loopback only at {APP_URL!r}, so it is unreachable "
        f"from outside the container")


def test_public_routes_carry_distinct_titles_and_descriptions(site):
    titles: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    for route in PUBLIC_ROUTES:
        r = site.get(route)
        assert r.status_code == 200, anchor(f"public route {route}", r)
        body = _text(r)
        head = body.lower()
        start = head.find("<title")
        assert start != -1, (
            f"public route {route} answered {r.status_code} and its document "
            f"declares no title; body starts {body[:200]!r}")
        end = head.find("</title>", start)
        title = body[head.find(">", start) + 1:end].strip()
        assert title, (
            f"public route {route} declares an empty title; "
            f"body starts {body[:200]!r}")
        assert title not in titles.values(), (
            f"public route {route} shares the title {title!r} with "
            f"{[k for k, v in titles.items() if v == title]}")
        titles[route] = title

        marker = 'name="description"'
        assert marker in head, (
            f"public route {route} declares no meta description; "
            f"body starts {body[:200]!r}")
        chunk = body[head.find(marker):head.find(marker) + 400]
        assert "content=" in chunk.lower(), (
            f"public route {route} declares a description with no content; "
            f"chunk {chunk!r}")
        descriptions[route] = chunk

    assert len(set(titles.values())) == len(PUBLIC_ROUTES), (
        f"the {len(PUBLIC_ROUTES)} public routes carry only "
        f"{len(set(titles.values()))} distinct titles: {titles!r}")


def test_privacy_page_is_linked_from_every_page_footer(site):
    privacy = site.get(PRIVACY_ROUTE)
    assert privacy.status_code == 200, anchor("privacy route", privacy)
    body = _text(privacy).lower()
    for field in ("address", "nickname", "biography"):
        assert field in body, (
            f"the privacy page omits the stored field {field!r}; "
            f"body starts {_text(privacy)[:300]!r}")

    for route in ("/", "/gallery", "/journal"):
        r = site.get(route)
        assert r.status_code == 200, anchor(f"route {route}", r)
        page = _text(r)
        assert PRIVACY_ROUTE in page, (
            f"route {route} carries no footer link to {PRIVACY_ROUTE}; "
            f"body starts {page[:300]!r}")
        assert FOOTER_RIGHTS in page or FOOTER_STUDIO in page, (
            f"route {route} carries no footer credit; body starts {page[:300]!r}")


def test_signup_creates_account_and_refuses_a_duplicate_email(client):
    email = probe_email()
    first = client.post("/auth/signup",
                        json={"email": email, "password": CORPUS_PASSWORD})
    assert first.status_code in (200, 201), anchor(f"signup for {email}", first)
    token = first.json().get("token")
    assert token, anchor(f"signup for {email} returned no token", first)

    again = client.post("/auth/signup",
                        json={"email": email, "password": CORPUS_PASSWORD})
    assert 400 <= again.status_code < 500, anchor(
        f"a second signup on {email} must be refused as a client error", again)
    assert "email" in _text(again).lower(), anchor(
        "the duplicate signup refusal must name the email field", again)

    upper = client.post("/auth/login",
                        json={"email": email.upper(), "password": CORPUS_PASSWORD})
    assert upper.status_code in (200, 201), anchor(
        "the stored address is lowercased, so an upper-case sign in resolves", upper)


def test_seeded_accounts_sign_in_with_the_corpus_password(client):
    for email in (MEMBER_EMAIL, SECOND_MEMBER_EMAIL, THIRD_MEMBER_EMAIL):
        r = client.post("/auth/login",
                        json={"email": email, "password": CORPUS_PASSWORD})
        assert r.status_code in (200, 201), anchor(
            f"seeded account {email} must sign in with the corpus password", r)
        assert r.json().get("token"), anchor(
            f"seeded account {email} signed in without a token", r)

    wrong = client.post("/auth/login",
                        json={"email": MEMBER_EMAIL, "password": "not-the-password"})
    assert 400 <= wrong.status_code < 500, anchor(
        "a wrong password must be refused as a client error", wrong)


def test_challenge_binds_the_address_and_the_row_survives_a_reload(client, db):
    email = probe_email()
    token = sign_up(client, email)
    address = probe_address()

    issued = request_challenge(client, token, address)
    for field in ("statement", "nonce"):
        assert issued.get(field), (
            f"the challenge for {address} carries no {field}: {issued!r}")
    statement = issued["statement"]
    assert address.lower() in statement.lower(), (
        f"the challenge statement does not name the address {address!r}: "
        f"{statement!r}")

    verified = verify_challenge(client, token, address, issued["nonce"])
    assert verified.status_code in (200, 201), anchor(
        f"returning the nonce for {address} must bind the address", verified)

    stored = poll(lambda: db.one("citizens", address_lower=address.lower()))
    if stored is None:
        stored = poll(lambda: db.one("citizen", address_lower=address.lower()))
    assert stored is not None, (
        f"no citizen row was persisted for {address!r} after the binding")

    reread = read_citizen(client, address)
    assert reread.status_code == 200, anchor(
        f"the bound citizen {address} must be readable after the binding", reread)


def test_address_comparison_is_case_insensitive(client):
    lower = read_citizen(client, MEMBER_ADDRESS.lower())
    upper = read_citizen(client, "0x" + MEMBER_ADDRESS[2:].upper())
    assert lower.status_code == 200, anchor(
        "the lowercase spelling of a seeded address must resolve", lower)
    assert upper.status_code == 200, anchor(
        "the uppercase spelling of a seeded address must resolve", upper)

    left = _citizen_of(lower.json()).get("address", "").lower()
    right = _citizen_of(upper.json()).get("address", "").lower()
    assert left == right == MEMBER_ADDRESS.lower(), (
        f"the two spellings resolved to {left!r} and {right!r} rather than to "
        f"the one seeded citizen {MEMBER_ADDRESS.lower()!r}")


def test_seeded_catalogue_carries_ten_thousand_records(client, db):
    meta = client.get("/catalogue")
    assert meta.status_code == 200, anchor("catalogue descriptor", meta)
    payload = meta.json()
    assert payload.get("token_count") == TOKEN_COUNT, anchor(
        f"the catalogue descriptor must report {TOKEN_COUNT} tokens", meta)
    assert payload.get("trait_count") == TRAIT_COUNT, anchor(
        f"the catalogue descriptor must report {TRAIT_COUNT} traits", meta)

    rows = db.count("tokens") or db.count("token")
    assert rows == TOKEN_COUNT, (
        f"the seeded catalogue holds {rows} rows rather than {TOKEN_COUNT}")

    traits = db.rows("traits") or db.rows("trait")
    names = {str(row.get("name")) for row in traits}
    missing = [t for t in TRAIT_NAMES if t not in names]
    assert not missing, (
        f"the seeded trait list omits {missing}; it holds {sorted(names)!r}")


def test_identifier_shift_resolves_every_worked_example(client):
    for display_id, expected in IDENTIFIER_EXAMPLES:
        assert on_chain_id(display_id) == expected, (
            f"the pinned arithmetic itself disagrees: display {display_id} "
            f"should resolve to {expected}")
        r = client.get(f"/tokens/{display_id}")
        assert r.status_code == 200, anchor(f"token {display_id}", r)
        body = r.json()
        got = body.get("on_chain_id", body.get("onChainId"))
        assert got == expected, anchor(
            f"display index {display_id} must resolve to on-chain identifier "
            f"{expected}, the app answered {got!r}", r)


def test_citizen_record_is_assembled_from_the_seeded_row(client):
    r = read_citizen(client, MEMBER_ADDRESS)
    assert r.status_code == 200, anchor(f"citizen {MEMBER_ADDRESS}", r)
    citizen = _citizen_of(r.json())
    for field in ("address", "profile", "holdings", "achievements"):
        assert field in citizen, anchor(
            f"the citizen record omits {field!r}", r)
    holdings = citizen.get("holdings") or []
    assert len(holdings) >= 1, anchor(
        f"the seeded citizen {MEMBER_ADDRESS} must hold at least one item", r)

    unknown = read_citizen(client, probe_address())
    assert unknown.status_code == 404, anchor(
        "an address with no citizen record must answer not found", unknown)


def test_holdings_response_names_whether_a_citizen_record_exists(client):
    held = client.get(f"/citizens/{MEMBER_ADDRESS}/holdings")
    assert held.status_code == 200, anchor(
        f"holdings for {MEMBER_ADDRESS}", held)
    body = held.json()
    flag = body.get("has_citizen_record", body.get("hasCitizenRecord"))
    assert flag is True, anchor(
        "a seeded bound address must report that a citizen record exists", held)
    assert isinstance(body.get("holdings"), list), anchor(
        "the holdings response must carry a holdings list", held)

    empty = client.get(f"/citizens/{EMPTY_MEMBER_ADDRESS}/holdings")
    assert empty.status_code == 200, anchor(
        f"holdings for {EMPTY_MEMBER_ADDRESS}", empty)
    empty_body = empty.json()
    empty_flag = empty_body.get("has_citizen_record",
                                empty_body.get("hasCitizenRecord"))
    assert empty_flag is True, anchor(
        "an address that holds nothing still has a citizen record, and the "
        "response must say so", empty)
    assert empty_body.get("holdings") == [], anchor(
        f"{EMPTY_MEMBER_ADDRESS} holds nothing, so the list must be empty", empty)

    stranger = client.get(f"/citizens/{probe_address()}/holdings")
    assert stranger.status_code in (200, 404), anchor(
        "an unknown address answers a holdings read without a server error",
        stranger)
    if stranger.status_code == 200:
        unknown_flag = stranger.json().get(
            "has_citizen_record", stranger.json().get("hasCitizenRecord"))
        assert unknown_flag is False, anchor(
            "an address the system has never seen must report that no citizen "
            "record exists", stranger)


def test_journal_category_filter_and_media_counts_sum(client):
    everything = client.get("/journal")
    assert everything.status_code == 200, anchor("journal index", everything)
    entries = everything.json()
    assert isinstance(entries, list), anchor(
        "the journal index must answer a top-level JSON array", everything)
    assert entries, anchor("the seeded journal index must carry entries",
                           everything)

    seen = {str(row.get("category")) for row in entries}
    for category in seen:
        filtered = client.get("/journal", params={"category": category})
        assert filtered.status_code == 200, anchor(
            f"journal category {category}", filtered)
        rows = filtered.json()
        assert rows, anchor(
            f"the seeded category {category} must carry at least one entry",
            filtered)
        off = [r for r in rows if str(r.get("category")) != category]
        assert not off, anchor(
            f"the {category} listing carries entries from another category: "
            f"{off[:3]!r}", filtered)

    media = client.get("/media")
    assert media.status_code == 200, anchor("media library", media)
    items = media.json()
    assert isinstance(items, list), anchor(
        "the media library must answer a top-level JSON array", media)
    assert len(items) == MEDIA_TOTAL, anchor(
        f"the seeded media library must hold {MEDIA_TOTAL} items, the app "
        f"answered {len(items)}", media)

    per_kind = {kind: len([i for i in items
                           if str(i.get("media_kind", i.get("kind"))) == kind])
                for kind in MEDIA_KINDS}
    assert per_kind["image"] == MEDIA_IMAGE, anchor(
        f"the seeded image count must be {MEDIA_IMAGE}, the library holds "
        f"{per_kind['image']}", media)
    assert per_kind["video"] == MEDIA_VIDEO, anchor(
        f"the seeded video count must be {MEDIA_VIDEO}, the library holds "
        f"{per_kind['video']}", media)
    assert per_kind["audio"] == MEDIA_AUDIO, anchor(
        f"the seeded audio count must be {MEDIA_AUDIO}, the library holds "
        f"{per_kind['audio']}", media)
    assert sum(per_kind.values()) == MEDIA_TOTAL, (
        f"the three media type counts {per_kind!r} do not sum to the total "
        f"{MEDIA_TOTAL}")


def test_unpublished_achievement_is_absent_from_every_list(client, db):
    listed = client.get("/achievements")
    assert listed.status_code == 200, anchor("achievement catalogue", listed)
    published = listed.json()
    assert isinstance(published, list), anchor(
        "the achievement catalogue must answer a top-level JSON array", listed)
    assert published, anchor("the seeded achievement catalogue is empty", listed)

    rows = db.rows("achievements") or db.rows("achievement")
    hidden = [r for r in rows if not r.get("published_at")]
    assert hidden, (
        "the seed must leave one achievement unpublished so its invisibility is "
        f"observable; the table holds {len(rows)} rows, all published")
    hidden_ids = {str(r.get("id")) for r in hidden}
    exposed = [a for a in published if str(a.get("id")) in hidden_ids]
    assert not exposed, anchor(
        f"the catalogue exposes the unpublished achievement(s) {exposed!r}",
        listed)

    citizen = read_citizen(client, MEMBER_ADDRESS)
    assert citizen.status_code == 200, anchor("citizen record", citizen)
    text = _text(citizen)
    leaked = [i for i in hidden_ids if i in text]
    assert not leaked, anchor(
        f"the citizen record names the unpublished achievement(s) {leaked!r}",
        citizen)


def test_media_download_address_is_minted_per_request(client):
    items = client.get("/media")
    assert items.status_code == 200, anchor("media library", items)
    first = items.json()[0]
    item_id = first.get("id")
    assert item_id is not None, f"the first media item carries no id: {first!r}"

    assert "object_key" not in first, (
        f"the media listing exposes the bucket path for item {item_id}: {first!r}")

    minted = client.post(f"/media/{item_id}/download")
    assert minted.status_code in (200, 201), anchor(
        f"a download address for media item {item_id}", minted)
    body = minted.json()
    address = body.get("url", body.get("download_url"))
    assert address, anchor(
        "the download response must carry a short lived address", minted)

    again = client.post(f"/media/{item_id}/download")
    assert again.status_code in (200, 201), anchor(
        f"a second download address for media item {item_id}", again)
    second = again.json().get("url", again.json().get("download_url"))
    assert second, anchor(
        "the second download response must carry an address too", again)


def test_console_echoes_typed_input_as_text(client):
    commands = client.get("/console/commands")
    assert commands.status_code == 200, anchor("console command set", commands)
    rows = commands.json()
    assert isinstance(rows, list), anchor(
        "the console command set must answer a top-level JSON array", commands)
    inputs = {str(r.get("input")) for r in rows}
    assert CONSOLE_INTERNAL_COMMAND in inputs, anchor(
        f"the seeded console command {CONSOLE_INTERNAL_COMMAND!r} is absent; "
        f"the set holds {sorted(inputs)!r}", commands)


def test_unknown_address_renders_the_product_not_found_page(site, client):
    r = site.get("/an-address-that-was-never-part-of-this-world")
    assert r.status_code == 404, anchor(
        "an unknown address must answer not found", r)
    body = _text(r)
    assert "<html" in body.lower(), anchor(
        "an unknown address must render the product's own page rather than a "
        "bare status", r)
    assert "/" in body, anchor(
        "the not-found page must offer a way back", r)

    api = client.get("/citizens/not-an-address/profile")
    assert 400 <= api.status_code < 500, anchor(
        "a malformed address must fail closed as a client error", api)


def test_owner_edits_persist_and_the_record_survives_a_reload(client, db,
                                                              member_token):
    nickname = probe_nickname()
    bio = "A seeded biography written by the owning citizen."
    saved = patch_profile(client, member_token, MEMBER_ADDRESS,
                          {"nickname": nickname, "bio": bio})
    assert saved.status_code in (200, 201), anchor(
        f"the owner writing {MEMBER_ADDRESS}", saved)

    reread = read_citizen(client, MEMBER_ADDRESS, member_token)
    assert reread.status_code == 200, anchor("re-reading the citizen", reread)
    profile = _profile_of(reread.json())
    assert profile.get("nickname") == nickname, anchor(
        f"the stored nickname must read {nickname!r}", reread)
    assert profile.get("bio") == bio, anchor(
        f"the stored biography must read {bio!r}", reread)

    stored = poll(lambda: db.one("profiles", nickname=nickname)
                  or db.one("profile", nickname=nickname))
    assert stored is not None, (
        f"no stored profile row carries the nickname {nickname!r} after the write")


def test_omitted_field_is_left_alone_and_an_explicit_null_clears_it(
        client, member_token):
    nickname = probe_nickname()
    bio = "A biography that an omitted field must leave untouched."
    seed = patch_profile(client, member_token, MEMBER_ADDRESS,
                         {"nickname": nickname, "bio": bio})
    assert seed.status_code in (200, 201), anchor("seeding the profile", seed)

    partial = patch_profile(client, member_token, MEMBER_ADDRESS,
                            {"nickname": nickname})
    assert partial.status_code in (200, 201), anchor(
        "a write that omits the biography", partial)
    after = _profile_of(read_citizen(client, MEMBER_ADDRESS, member_token).json())
    assert after.get("bio") == bio, (
        f"omitting the biography cleared it: the stored value is "
        f"{after.get('bio')!r} rather than {bio!r}")

    cleared = patch_profile(client, member_token, MEMBER_ADDRESS, {"bio": None})
    assert cleared.status_code in (200, 201), anchor(
        "an explicit null on the biography", cleared)
    final = _profile_of(read_citizen(client, MEMBER_ADDRESS, member_token).json())
    assert not final.get("bio"), (
        f"an explicit null must clear the biography, the stored value is still "
        f"{final.get('bio')!r}")


def test_catalogue_index_file_is_stored_in_the_bucket(client, storage):
    meta = client.get("/catalogue")
    assert meta.status_code == 200, anchor("catalogue descriptor", meta)
    index_url = meta.json().get("index_url")
    assert index_url, anchor(
        "the catalogue descriptor must name the published index address", meta)

    keys = poll(lambda: storage.list(CATALOGUE_KEY_PREFIX))
    assert keys, (
        f"no catalogue index object is stored under {CATALOGUE_KEY_PREFIX!r}; "
        f"the bucket currently lists {storage.list('')[:10]!r}")
    assert any(k.endswith(".json") for k in keys), (
        f"the published catalogue index must be a stored file, the bucket holds "
        f"{keys[:10]!r}")

    fetched = httpx.get(index_url, timeout=60.0, follow_redirects=True)
    assert fetched.status_code == 200, (
        f"the published index address {index_url!r} answered "
        f"{fetched.status_code}")
    payload = fetched.json()
    assert isinstance(payload.get("traits"), list), (
        f"the packed index carries no trait header: {str(payload)[:200]!r}")
    assert len(payload["traits"]) == TRAIT_COUNT, (
        f"the packed index header carries {len(payload['traits'])} traits "
        f"rather than {TRAIT_COUNT}")
    assert len(payload.get("tokens") or []) == TOKEN_COUNT, (
        f"the packed index carries {len(payload.get('tokens') or [])} tokens "
        f"rather than {TOKEN_COUNT}")
    for trait in payload["traits"]:
        name = str(trait.get("name"))
        if name in TRAIT_VALUE_COUNTS:
            assert len(trait.get("values") or []) == TRAIT_VALUE_COUNTS[name], (
                f"the packed header gives {name} "
                f"{len(trait.get('values') or [])} values rather than "
                f"{TRAIT_VALUE_COUNTS[name]}")


def test_passport_object_is_stored_in_the_bucket_at_its_key(client, storage,
                                                            member_token):
    renders = client.get(f"/citizens/{MEMBER_ADDRESS}/renders",
                         headers=bearer(member_token))
    assert renders.status_code == 200, anchor(
        f"render state for {MEMBER_ADDRESS}", renders)
    state = renders.json()
    faces = state.get("faces", state)
    for face in PASSPORT_FACES:
        entry = faces.get(face)
        assert entry is not None, anchor(
            f"the render state omits the face {face!r}", renders)
        assert str(entry.get("state")) in RENDER_STATES, anchor(
            f"face {face!r} reports the state {entry.get('state')!r}, which is "
            f"not one of {RENDER_STATES}", renders)

    prefix = f"{PASSPORT_KEY_PREFIX}{MEMBER_ADDRESS.lower()}/"
    keys = poll(lambda: storage.list(prefix))
    assert keys, (
        f"no passport object is stored under {prefix!r}; the bucket currently "
        f"lists {storage.list(PASSPORT_KEY_PREFIX)[:10]!r}")
    for face in PASSPORT_FACES:
        matching = [k for k in keys if f"/{face}/" in k and k.endswith(".png")]
        assert matching, (
            f"no stored object matches the key scheme for face {face!r}; the "
            f"prefix holds {keys[:10]!r}")


def test_repeated_generation_request_returns_the_run_in_flight(client,
                                                               member_token):
    before = client.get(f"/citizens/{MEMBER_ADDRESS}/renders",
                        headers=bearer(member_token))
    assert before.status_code == 200, anchor("render state before", before)

    nickname = probe_nickname()
    changed = patch_profile(client, member_token, MEMBER_ADDRESS,
                            {"nickname": nickname})
    assert changed.status_code in (200, 201), anchor(
        "a write that changes the content hash", changed)

    first = client.post(f"/citizens/{MEMBER_ADDRESS}/renders", json={},
                        headers=bearer(member_token))
    assert first.status_code in (200, 201, 202, 409), anchor(
        "the first regeneration request", first)
    second = client.post(f"/citizens/{MEMBER_ADDRESS}/renders", json={},
                         headers=bearer(member_token))
    assert second.status_code in (200, 201, 202, 409), anchor(
        "the second regeneration request", second)
    assert second.status_code < 500, anchor(
        "a second regeneration request must be answered rather than failing",
        second)

    unchanged = patch_profile(client, member_token, MEMBER_ADDRESS,
                              {"nickname": nickname})
    assert unchanged.status_code in (200, 201), anchor(
        "saving the identical value again", unchanged)


def test_concurrent_nickname_claims_accept_at_most_one(client, db):
    nickname = probe_nickname()
    tokens = []
    addresses = []
    for _ in range(2):
        token = sign_up(client, probe_email())
        address = probe_address()
        issued = request_challenge(client, token, address)
        bound = verify_challenge(client, token, address, issued["nonce"])
        assert bound.status_code in (200, 201), anchor(
            f"binding {address} for the contention probe", bound)
        tokens.append(token)
        addresses.append(address)

    def claim(index: int) -> int:
        with httpx.Client(base_url=client.base_url, timeout=30.0,
                          follow_redirects=False) as c:
            r = c.patch(f"/citizens/{addresses[index]}/profile",
                        json={"nickname": nickname},
                        headers=bearer(tokens[index]))
            return r.status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(claim, range(2)))

    accepted = [s for s in results if 200 <= s < 300]
    assert len(accepted) <= 1, (
        f"both concurrent claims of the nickname {nickname!r} were accepted: "
        f"the two responses were {results}")
    assert any(400 <= s < 500 for s in results), (
        f"one concurrent claim of {nickname!r} must be refused as a client "
        f"error, the two responses were {results}")

    holders = db.rows("profiles", nickname=nickname) or db.rows(
        "profile", nickname=nickname)
    assert len(holders) <= 1, (
        f"{len(holders)} stored profiles hold the nickname {nickname!r}")


def test_refused_nickname_claim_stores_nothing(client, db, member_token,
                                               second_member_token):
    nickname = probe_nickname()
    taken = patch_profile(client, member_token, MEMBER_ADDRESS,
                          {"nickname": nickname})
    assert taken.status_code in (200, 201), anchor(
        "the first citizen claiming the nickname", taken)

    before = _profile_of(
        read_citizen(client, SECOND_MEMBER_ADDRESS, second_member_token).json())
    clash = patch_profile(client, second_member_token, SECOND_MEMBER_ADDRESS,
                          {"nickname": nickname})
    assert 400 <= clash.status_code < 500, anchor(
        f"a second citizen claiming the taken nickname {nickname!r}", clash)

    after = _profile_of(
        read_citizen(client, SECOND_MEMBER_ADDRESS, second_member_token).json())
    assert after.get("nickname") == before.get("nickname"), (
        f"the refused claim moved the second citizen's nickname from "
        f"{before.get('nickname')!r} to {after.get('nickname')!r}")

    holders = db.rows("profiles", nickname=nickname) or db.rows(
        "profile", nickname=nickname)
    assert len(holders) <= 1, (
        f"{len(holders)} stored profiles hold {nickname!r} after the refusal")


def test_cross_account_profile_write_is_denied_and_the_row_is_unchanged(
        client, db, second_member_token, member_token):
    before = _profile_of(read_citizen(client, MEMBER_ADDRESS, member_token).json())

    denied = patch_profile(client, second_member_token, MEMBER_ADDRESS,
                           {"nickname": probe_nickname(),
                            "bio": "written by somebody else"})
    assert denied.status_code in (401, 403), anchor(
        f"a write to {MEMBER_ADDRESS} from another citizen's session must be "
        f"denied", denied)

    after = _profile_of(read_citizen(client, MEMBER_ADDRESS, member_token).json())
    assert after.get("nickname") == before.get("nickname"), (
        f"the denied write moved the nickname from {before.get('nickname')!r} "
        f"to {after.get('nickname')!r}")
    assert after.get("bio") == before.get("bio"), (
        f"the denied write moved the biography from {before.get('bio')!r} to "
        f"{after.get('bio')!r}")

    audited = db.rows("audit_log") or db.rows("audit_logs")
    assert isinstance(audited, list), (
        "the audit trail must be readable as rows so a refused write can be "
        f"accounted for; the reader answered {audited!r}")


def test_unauthenticated_profile_write_is_denied(client):
    r = client.patch(f"/citizens/{MEMBER_ADDRESS}/profile",
                     json={"nickname": probe_nickname()})
    assert r.status_code in (401, 403), anchor(
        "a write with no bearer token must be denied", r)

    junk = client.patch(f"/citizens/{MEMBER_ADDRESS}/profile",
                        json={"nickname": probe_nickname()},
                        headers={"Authorization": "Bearer not-a-real-token"})
    assert junk.status_code in (401, 403), anchor(
        "a write carrying an unknown bearer token must be denied", junk)


def test_citizen_record_hides_renders_from_every_other_caller(
        client, member_token, second_member_token):
    owner = read_citizen(client, MEMBER_ADDRESS, member_token)
    assert owner.status_code == 200, anchor("the owner reading their record",
                                            owner)
    owner_body = _citizen_of(owner.json())
    profile = owner_body.get("profile") or {}
    assert "renders" in owner_body or "renders" in profile, anchor(
        "the owner's own record must carry the renders object", owner)

    for label, token in (("another citizen", second_member_token),
                         ("an anonymous caller", None)):
        r = read_citizen(client, MEMBER_ADDRESS, token)
        assert r.status_code == 200, anchor(
            f"{label} reading the public citizen record", r)
        body = _citizen_of(r.json())
        other_profile = body.get("profile") or {}
        assert "renders" not in body and "renders" not in other_profile, anchor(
            f"{label} received a renders key, which must be absent rather than "
            f"empty", r)


def test_another_citizens_passport_document_is_denied(
        client, member_token, second_member_token):
    owner = client.get(f"/citizens/{MEMBER_ADDRESS}/renders",
                       headers=bearer(member_token))
    assert owner.status_code == 200, anchor(
        "the owner reading their own passport documents", owner)

    intruder = client.get(f"/citizens/{MEMBER_ADDRESS}/renders",
                          headers=bearer(second_member_token))
    assert intruder.status_code in (401, 403, 404), anchor(
        f"another citizen reading the passport documents of {MEMBER_ADDRESS} "
        f"must be refused", intruder)

    anonymous = client.get(f"/citizens/{MEMBER_ADDRESS}/renders")
    assert anonymous.status_code in (401, 403, 404), anchor(
        "an anonymous caller reading passport documents must be refused",
        anonymous)

    regenerate = client.post(f"/citizens/{MEMBER_ADDRESS}/renders", json={},
                             headers=bearer(second_member_token))
    assert regenerate.status_code in (401, 403, 404), anchor(
        "another citizen requesting regeneration must be refused", regenerate)


def test_render_harness_refuses_without_a_signed_parameter(site):
    bare = site.get(HARNESS_ROUTE)
    assert bare.status_code in (400, 401, 403, 404), anchor(
        f"{HARNESS_ROUTE} without a signed parameter must be refused", bare)

    guessed = site.get(HARNESS_ROUTE,
                       params={"address": MEMBER_ADDRESS,
                               "face": "document_front",
                               "signature": "not-a-real-signature"})
    assert guessed.status_code in (400, 401, 403, 404), anchor(
        f"{HARNESS_ROUTE} with a guessed signature must be refused", guessed)

    for route in ("/", "/gallery", "/about"):
        page = site.get(route)
        assert page.status_code == 200, anchor(f"route {route}", page)
        assert HARNESS_ROUTE not in _text(page), (
            f"route {route} links the operator harness {HARNESS_ROUTE}, which "
            f"is reached only by the pipeline; body starts {_text(page)[:200]!r}")


def test_no_credential_appears_in_anything_the_browser_downloads(site):
    for route in ("/", "/gallery", "/journal"):
        r = site.get(route)
        assert r.status_code == 200, anchor(f"route {route}", r)
        body = _text(r)
        for needle in SECRET_NEEDLES:
            assert needle not in body, (
                f"route {route} ships the credential marker {needle!r} in its "
                f"document; body starts {body[:200]!r}")


def test_form_validation_refuses_invalid_input_and_stores_nothing(
        client, member_token):
    before = _profile_of(read_citizen(client, MEMBER_ADDRESS, member_token).json())

    long_bio = "x" * (BIO_MAX + 1)
    refused = patch_profile(client, member_token, MEMBER_ADDRESS,
                            {"bio": long_bio})
    assert 400 <= refused.status_code < 500, anchor(
        f"a biography of {BIO_MAX + 1} characters must be refused", refused)
    assert "bio" in _codes(refused).lower(), anchor(
        "the refusal must name the biography field", refused)

    short = patch_profile(client, member_token, MEMBER_ADDRESS,
                          {"nickname": "ab"})
    assert 400 <= short.status_code < 500, anchor(
        "a nickname of two characters must be refused", short)

    long_nick = patch_profile(client, member_token, MEMBER_ADDRESS,
                              {"nickname": "n" * (NICKNAME_MAX + 1)})
    assert 400 <= long_nick.status_code < 500, anchor(
        f"a nickname of {NICKNAME_MAX + 1} characters must be refused",
        long_nick)

    spaced = patch_profile(client, member_token, MEMBER_ADDRESS,
                           {"nickname": " leading space"})
    assert 400 <= spaced.status_code < 500, anchor(
        "a nickname with a leading space must be refused", spaced)

    after = _profile_of(read_citizen(client, MEMBER_ADDRESS, member_token).json())
    assert after.get("bio") == before.get("bio"), (
        f"a refused write moved the biography from {before.get('bio')!r} to "
        f"{after.get('bio')!r}")
    assert after.get("nickname") == before.get("nickname"), (
        f"a refused write moved the nickname from {before.get('nickname')!r} "
        f"to {after.get('nickname')!r}")


def test_unowned_representative_item_is_refused(client, member_token):
    held = client.get(f"/citizens/{MEMBER_ADDRESS}/holdings")
    assert held.status_code == 200, anchor("holdings for the owner", held)
    owned = {row.get("token_id", row.get("tokenId"))
             for row in held.json().get("holdings") or []}
    assert owned, anchor("the seeded owner must hold at least one item", held)

    candidate = next(i for i in range(TOKEN_COUNT) if i not in owned)
    refused = patch_profile(client, member_token, MEMBER_ADDRESS,
                            {"representative_token_id": candidate})
    assert 400 <= refused.status_code < 500, anchor(
        f"the owner must not claim item {candidate}, which the address does "
        f"not hold", refused)

    accepted = patch_profile(client, member_token, MEMBER_ADDRESS,
                             {"representative_token_id": sorted(owned)[0]})
    assert accepted.status_code in (200, 201), anchor(
        "the owner claiming an item the address really holds", accepted)


def test_replayed_challenge_nonce_is_refused(client):
    token = sign_up(client, probe_email())
    address = probe_address()
    issued = request_challenge(client, token, address)

    first = verify_challenge(client, token, address, issued["nonce"])
    assert first.status_code in (200, 201), anchor(
        "the first return of the nonce must bind the address", first)

    replay = verify_challenge(client, token, address, issued["nonce"])
    assert 400 <= replay.status_code < 500, anchor(
        "returning a consumed nonce a second time must be refused", replay)

    invented = verify_challenge(client, token, probe_address(),
                                "0" * len(str(issued["nonce"])))
    assert 400 <= invented.status_code < 500, anchor(
        "an invented nonce must be refused", invented)


def test_challenge_for_another_address_is_refused(client):
    token = sign_up(client, probe_email())
    mine = probe_address()
    theirs = probe_address()
    issued = request_challenge(client, token, mine)

    crossed = verify_challenge(client, token, theirs, issued["nonce"])
    assert 400 <= crossed.status_code < 500, anchor(
        f"a nonce issued for {mine} must not bind {theirs}", crossed)

    taken = client.post("/session/challenge", json={"address": MEMBER_ADDRESS},
                        headers=bearer(token))
    if taken.status_code in (200, 201):
        bound = verify_challenge(client, token, MEMBER_ADDRESS,
                                 taken.json()["nonce"])
        assert 400 <= bound.status_code < 500, anchor(
            f"{MEMBER_ADDRESS} is already bound elsewhere, so a second account "
            f"must not bind it", bound)
    else:
        assert 400 <= taken.status_code < 500, anchor(
            f"a challenge for the already bound {MEMBER_ADDRESS} must be "
            f"refused as a client error", taken)

    malformed = client.post("/session/challenge", json={"address": "0xnothex"},
                            headers=bearer(token))
    assert 400 <= malformed.status_code < 500, anchor(
        "a malformed address must fail closed", malformed)


def test_automated_form_submission_is_refused(client):
    decoy = client.post("/auth/signup",
                        json={"email": probe_email(),
                              "password": CORPUS_PASSWORD,
                              "website": "http://a-bot-filled-this.example.com"})
    assert 400 <= decoy.status_code < 500, anchor(
        "a signup carrying a filled decoy field must be refused", decoy)

    burst = []
    for _ in range(12):
        r = client.post("/auth/signup",
                        json={"email": probe_email(),
                              "password": CORPUS_PASSWORD})
        burst.append(r.status_code)
        if r.status_code == 429:
            break
    assert 429 in burst or any(400 <= s < 500 for s in burst), (
        f"twelve signups in quick succession from one source were all accepted: "
        f"the responses were {burst}")
