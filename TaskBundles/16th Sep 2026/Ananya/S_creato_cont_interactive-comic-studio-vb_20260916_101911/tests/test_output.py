from __future__ import annotations

import datetime
import hashlib
import hmac
import json
import os
import re
from urllib.parse import parse_qs, urlparse

import httpx

import appclient
from conftest import (
    ALERT_KIND, AUTHOR2_EMAIL, AUTHOR2_NAME, AUTHOR_EMAIL, AUTHOR_NAME, AUTHOR_SESSION_KEY, CATALOGUE_EN,
    CATALOGUE_FR, CHAPTER_DESCRIPTIONS, CHAPTER_STATES, CHAPTER_TITLES, CONTACT_EMAIL, CREDIT_THRESHOLD,
    DEFAULT_LOCALE, DISPLAY_NAMES, DOMAINS, DUPLICATE_ADDRESS_MESSAGE, EARLY_ACCESS_DAYS,
    EARLY_ACCESS_THRESHOLD, EFFECT_DEADLINE_SECONDS, EVENT_PARAMS, FRIEND_EMAIL, HOSTING, LANGUAGE_TAGS,
    LEGAL_HEADINGS, LOCALES, NAMESPACES, NARROW_TABLET_VIEWPORT, PAGE_META_EN, PAGE_META_FR, PAGE_VIEW_ROUTES,
    PANEL_DESCRIPTIONS, PHONE_VIEWPORT, PORTRAIT_VIEWPORT, PROGRESS_KEY_PREFIX, PUBLIC_ROUTES, READER2_EMAIL,
    READER_EMAIL, REGISTRAR, RELEASE_INPUT, RELEASE_READBACK, SCHEDULER_DEADLINE_SECONDS, SECURITY_HEADERS,
    SEEDED_ASSET_VERSION, SEED_PASSWORD, SEED_TIP_ONE, SEED_TIP_ONE_MESSAGE, SEED_TIP_TWO,
    SEED_TIP_TWO_MESSAGE, SHA_KEY_RE, SIGNATURE_HEADER, SIGNATURE_WINDOW_SECONDS, SMALLEST_VIEWPORT,
    STUDIO_CURRENCY, STUDIO_NAME, STUDIO_TIME_ZONE, TABLET_VIEWPORT, TIPBOX_PAGE, TIPBOX_SECRET,
    TIPBOX_SECRET_LAST_FOUR, TIP_ENTITLEMENT_VALUES, TIP_ROW_FIELDS, TIP_STATE_VALUES, ULID_RE,
    VOLUME_ONE_LABEL, WIDE_VIEWPORT, active_kinds, all_tips, api_client, assert_rejected, before,
    board_detail, build_chapter, capitalise_words, chapter_state, claim, columns_of, cookie_names,
    deadline_after, deliver, describe, describe_panels, document_kept, document_meta, entitlements, error_of,
    event_body, fetch_absolute, frame_table, iso_in, items_of, layer_urls, make_png, manifest, mark_document,
    new_board, new_chapter, new_context, new_volume, now_unix, open_route, parse_instant,
    patch_studio_chapter, probe_email, publish, reader_login, register_reader, return_token, run_together,
    schedule, settings_of, settle, sign, signed_in_author_page, storage_keys, store_cover, studio_chapter,
    studio_chapter_row, studio_chapters, studio_login, studio_volume, tiny_jpeg, tiny_webp, tip_data, tip_row,
    tips_page, token_hex, two_digit, upload, utc_now, volumes, wait_for,
)

DATA_MODEL_COLUMNS = {
    "studios": ("id", "name", "contact_email", "time_zone", "currency", "default_locale", "early_access_threshold",
                "credit_threshold", "asset_version", "image_signing_key", "created_at"),
    "locales": ("code", "language_tag", "display_name", "is_default", "active", "position"),
    "volumes": ("id", "label", "position", "created_at"),
    "chapters": ("id", "volume_id", "number", "state", "release_at", "published_at", "early_access_days",
                 "content_tag", "cover_object_key", "version", "created_at", "updated_at"),
    "chapter_texts": ("chapter_id", "locale", "title", "description"),
    "chapter_waivers": ("chapter_id", "locale", "reason", "expires_at"),
    "boards": ("id", "chapter_id", "number", "name", "version"),
    "panels": ("id", "board_id", "number", "camera_x", "camera_y", "entry_duration", "selectable", "hold", "wide",
               "version"),
    "panel_descriptions": ("panel_id", "locale", "text"),
    "layers": ("id", "panel_id", "role", "kind", "draw_order", "depth", "offset_x", "offset_y", "scale", "opacity",
               "blend", "displacement_source_id", "displacement_strength", "clip", "loop_mode", "localised",
               "retain", "version"),
    "layer_images": ("id", "layer_id", "locale", "object_key", "byte_length", "content_hash", "stored_at"),
    "frame_tables": ("layer_id", "object_key", "frame_count", "clips", "byte_length"),
    "messages": ("namespace", "key", "locale", "value", "state", "note", "updated_at"),
    "members": ("id", "email", "name", "password_hash", "created_at", "last_seen_at"),
    "studio_sessions": ("token_hash", "member_id", "created_at", "expires_at", "revoked_at"),
    "readers": ("id", "email", "password_hash", "locale", "notifications", "last_chapter_id", "last_chapter_at",
                "created_at"),
    "reader_sessions": ("token_hash", "reader_id", "created_at", "expires_at", "revoked_at"),
    "progress": ("reader_id", "chapter_id", "fraction", "last_panel", "updated_at"),
    "entitlements": ("id", "reader_id", "kind", "tip_id", "granted_at", "expires_at", "revoked_at", "revoked_reason"),
    "tips": ("id", "source", "external_id", "amount", "currency", "settled_amount", "rate", "message",
             "supporter_email", "matched_reader_id", "match_method", "match_confirmed_at", "state", "received_at",
             "state_changed_at", "reason"),
    "return_tokens": ("token_hash", "issued_at", "expires_at", "claimed_by_reader_id", "claimed_at"),
    "webhook_events": ("id", "source", "external_id", "event_type", "signature_verified", "payload", "received_at",
                       "processed_at"),
    "page_views": ("id", "route", "viewed_at"),
    "chapter_opens": ("id", "chapter_id", "opened_at"),
    "measured_events": ("id", "name", "params", "received_at"),
    "audit_records": ("id", "actor_email", "action", "subject_type", "subject_id", "request_id", "created_at"),
    "integrations": ("provider", "signing_secret", "page_url", "secret_created_at", "secret_last_used_at"),
    "alerts": ("id", "kind", "subject_id", "message", "created_at"),
}

DERIVED_COLUMN_NAMES = ("chapter_count", "locked", "is_locked", "open_count", "opens_count", "byte_total",
                        "total_bytes", "coverage_percent", "percent", "entitlement", "panel_index", "index_in_chapter")


def test_seeded_accounts_sign_in_with_the_corpus_password_authors_only_at_studio_login_with_member_name_no_author_signup(backend, early_signed_image, audit_snapshot):
    """Every seeded account signs in with the pinned password on its own surface only.

    cov: C-RL-19, C-RL-26, C-RL-27, C-RL-28, C-RL-29, C-RL-32, C-CF-29, C-DM-03
    """
    assert early_signed_image["url"], "no signed image address was captured"
    assert isinstance(audit_snapshot["rows"], list)
    for email in (READER_EMAIL, READER2_EMAIL):
        assert reader_login(email), f"{email} did not sign in with the seeded password"
    for email, name in ((AUTHOR_EMAIL, AUTHOR_NAME), (AUTHOR2_EMAIL, AUTHOR2_NAME)):
        response = httpx.post(f"{appclient.api_base()}/studio/auth/login",
                              json={"email": email, "password": SEED_PASSWORD}, timeout=appclient.TIMEOUT)
        assert response.status_code == 200, describe(response)
        body = response.json()
        assert body.get("access_token"), describe(response)
        assert body.get("member", {}).get("email") == email, describe(response)
        assert body.get("member", {}).get("name") == name, describe(response)
        on_reader = httpx.post(f"{appclient.api_base()}/auth/login", json={"email": email, "password": SEED_PASSWORD},
                               timeout=appclient.TIMEOUT)
        assert on_reader.status_code in (400, 401, 403), f"a studio account signed in as a reader. {describe(on_reader)}"
    on_studio = httpx.post(f"{appclient.api_base()}/studio/auth/login",
                           json={"email": READER_EMAIL, "password": SEED_PASSWORD}, timeout=appclient.TIMEOUT)
    assert on_studio.status_code in (400, 401, 403), describe(on_studio)
    members_before = backend.count("members")
    for path in ("/studio/auth/register", "/studio/members", "/studio/auth/signup"):
        with api_client() as anon:
            attempt = anon.post(path, json={"email": "probe-" + token_hex() + "@example.com",
                                            "password": SEED_PASSWORD, "name": "Probe"})
        assert attempt.status_code in (401, 403, 404, 405), f"an author signup path answered. {describe(attempt)}"
    assert backend.count("members") == members_before == 2, "author accounts exist only as the two seeded members"


def test_seeded_readers_hold_early_access_from_seeded_tip_or_no_entitlement_with_stored_progress(author):
    """reader holds early access from tbx_seed_001; reader2 holds nothing and has stored progress on chapter 1.

    cov: C-RL-30, C-RL-31, C-CF-290, C-DM-131
    """
    reader_token = reader_login(READER_EMAIL)
    kinds = entitlements(reader_token)
    assert any(e["kind"] == "early_access" and e.get("active") for e in kinds), f"reader lacks early access: {kinds}"
    row = next(r for r in all_tips(author) if r.get("tip_id") == SEED_TIP_ONE)
    assert row["matched_reader_email"] == READER_EMAIL and row["entitlement"] == "granted", row
    reader2_token = reader_login(READER2_EMAIL)
    assert active_kinds(reader2_token) == set(), "reader2 must hold no entitlement"
    with api_client(reader2_token) as session:
        progress = session.get("/me/progress")
    assert progress.status_code == 200, describe(progress)
    body = progress.json()
    chapter_one = [c for c in body["chapters"] if int(c["volume"]) == 1 and int(c["chapter"]) == 1]
    assert chapter_one and abs(float(chapter_one[0]["fraction"]) - 0.4) < 1e-9, body
    assert int(chapter_one[0]["last_panel"]) == 2, body
    assert body["last_chapter"] and int(body["last_chapter"]["chapter"]) == 1, body
    assert (utc_now() - parse_instant(body["last_chapter_at"])).total_seconds() < 3 * 86400, body


def test_seeded_studio_row_exists_once_with_asset_version_locales_and_image_signing_key_holding_the_pinned_values(author, backend):
    """The one studio row, the two locales and the signing key hold the pinned seed values.

    cov: C-CF-825, C-DM-05, C-DM-06, C-DM-07, C-DM-08, C-DM-09, C-DM-11, C-CN-01
    """
    settings = settings_of(author)
    assert settings["name"] == STUDIO_NAME and settings["contact_email"] == CONTACT_EMAIL, settings
    assert settings["time_zone"] == STUDIO_TIME_ZONE and settings["currency"] == STUDIO_CURRENCY, settings
    assert settings["default_locale"] == DEFAULT_LOCALE, settings
    assert int(settings["early_access_threshold"]) == EARLY_ACCESS_THRESHOLD, settings
    assert int(settings["credit_threshold"]) == CREDIT_THRESHOLD, settings
    assert int(settings["asset_version"]) == SEEDED_ASSET_VERSION, settings
    assert backend.count("studios") == 1, "exactly one studio exists"
    locale_rows = backend.query("SELECT code, language_tag, display_name FROM locales")
    assert {r["code"]: (r["language_tag"], r["display_name"]) for r in locale_rows} == {
        code: (LANGUAGE_TAGS[code], DISPLAY_NAMES[code]) for code in LOCALES}, locale_rows
    key = backend.query("SELECT image_signing_key FROM studios")[0]["image_signing_key"]
    raw = bytes(key) if isinstance(key, (bytes, bytearray, memoryview)) else str(key).encode()
    assert len(raw) in (32, 44, 64), f"image_signing_key should hold 32 random bytes, found {len(raw)} stored bytes"
    rendered = raw.hex() if len(raw) == 32 else raw.decode(errors="ignore")
    for path in ("/studio/settings", "/studio/integrations/tipbox", "/studio/overview"):
        response = author.get(path)
        assert rendered not in response.text, f"{path} returned the image signing key"


def test_seeded_first_volume_holds_six_chapters_with_pinned_states_release_moments_boards_panels_layers_and_early_access_days(author, backend):
    """Vol. I seeds six chapters with pinned titles, states, moments, structure, layers and early access days.

    cov: C-OV-11, C-OV-12, C-DM-65, C-DM-66, C-DM-67, C-DM-68, C-DM-69, C-DM-70, C-DM-73, C-DM-74, C-DM-75, C-DM-76, C-DM-77, C-DM-78, C-DM-79
    """
    volume = studio_volume(author, 1)
    assert volume["label"] == VOLUME_ONE_LABEL and int(volume["chapter_count"]) == 6, volume
    rows = {int(r["number"]): r for r in author.get(f"/studio/volumes/{volume['id']}/chapters").json()}
    assert sorted(rows) == [1, 2, 3, 4, 5, 6], rows
    moments = {}
    for number, row in rows.items():
        assert row["state"] == CHAPTER_STATES[number], row
        assert (row["titles"]["en"], row["titles"]["fr"]) == CHAPTER_TITLES[number], row
        if number == 6:
            assert row["release_at"] is None, row
        else:
            moment = parse_instant(row["release_at"])
            assert (moment.hour, moment.minute) == (18, 0), row
            moments[number] = moment
    gaps = [(moments[n + 1] - moments[n]).days for n in range(1, 5)]
    assert gaps == [20, 20, 23, 17], f"release moments must sit 60, 40, 20 days before and 3, 20 days after start: {gaps}"
    for number, row in rows.items():
        detail = author.get(f"/studio/chapters/{row['id']}").json()
        assert int(detail["early_access_days"]) == EARLY_ACCESS_DAYS, detail
        boards = sorted(detail["boards"], key=lambda b: int(b["number"]))
        shape = []
        for board in boards:
            full = author.get(f"/studio/boards/{board['id']}").json()
            panels = sorted(full["panels"], key=lambda p: int(p["number"]))
            shape.append([int(p["number"]) for p in panels])
            for panel in panels:
                assert panel["selectable"] is True and panel["hold"] is False and panel["wide"] is False, panel
                assert float(panel["entry_duration"]) == 0.6, panel
                assert float(panel["camera_x"]) == 0 and float(panel["camera_y"]) == 0, panel
                layers = {l["role"]: l for l in panel["layers"]}
                expected = {"back": (-4, 0)} if number == 6 else {"back": (-4, 0), "stage": (0, 1), "characters": (2, 2)}
                if (number, int(board["number"]), int(panel["number"])) == (1, 1, 1):
                    expected["sign"] = (1, 3)
                assert set(layers) == set(expected), f"chapter {number} panel {panel['number']} roles {sorted(layers)}"
                for role, (depth, order) in expected.items():
                    layer = layers[role]
                    assert float(layer["depth"]) == depth and int(layer["draw_order"]) == order, layer
                    assert layer["kind"] == "image" and layer["blend"] == "normal", layer
                    assert float(layer["offset_x"]) == 0 and float(layer["offset_y"]) == 0, layer
                    assert float(layer["scale"]) == 1 and float(layer["opacity"]) == 1, layer
                    assert bool(layer.get("localised")) == (role == "sign"), layer
        if number == 1:
            assert shape == [[1, 2, 3], [1, 2]], shape
        elif number == 6:
            assert shape == [[1]], shape
        else:
            assert shape == [[1, 2, 3]], shape
    body = manifest(1, 1).json()
    identifiers = {l["identifier"] for b in body["boards"] for p in b["panels"] for l in p["layers"]}
    assert "c1b1p1-back" in identifiers and "c1b2p2-characters" in identifiers, sorted(identifiers)[:8]


def test_seeded_chapters_carry_pinned_chapter_and_panel_descriptions_covers_and_pass_preflight(author, anon):
    """Seeded descriptions match the pinned text in both languages; chapters 1 to 5 have covers and pass preflight.

    cov: C-DM-72, C-DM-81, C-DM-82, C-DM-83, C-DM-84, C-DM-85, C-DM-86, C-DM-87, C-DM-88, C-DM-89, C-DM-90, C-DM-91, C-DM-92, C-DM-93, C-DM-94, C-DM-95, C-DM-96, C-DM-97, C-DM-98, C-DM-99, C-DM-100, C-DM-101, C-DM-102, C-DM-103, C-DM-104, C-DM-105, C-DM-106, C-DM-107, C-DM-108, C-DM-109, C-DM-110, C-DM-111, C-DM-112, C-DM-113, C-DM-114, C-DM-115, C-DM-116, C-DM-117, C-DM-118, C-DM-119, C-DM-120, C-DM-121, C-DM-122, C-DM-123, C-DM-124, C-DM-125, C-DM-126, C-DM-127, C-DM-128
    """
    for number in range(1, 7):
        row = studio_chapter_row(author, 1, number)
        detail = author.get(f"/studio/chapters/{row['id']}").json()
        preview = author.get(f"/studio/chapters/{row['id']}/manifest", params={"locale": "en"}).json()
        preview_fr = author.get(f"/studio/chapters/{row['id']}/manifest", params={"locale": "fr"}).json()
        assert (preview["description"], preview_fr["description"]) == CHAPTER_DESCRIPTIONS[number], preview
        for body, index in ((preview, 0), (preview_fr, 1)):
            for board in body["boards"]:
                for panel in board["panels"]:
                    key = (number, int(board["number"]), int(panel["number"]))
                    assert panel["description"] == PANEL_DESCRIPTIONS[key][index], (key, panel["description"])
        cover = anon.get(f"/covers/1/{number}.png")
        if number <= 5:
            assert detail["has_cover"] is True, detail
            assert cover.status_code == 200, describe(cover)
            checked = author.post(f"/studio/chapters/{row['id']}/preflight")
            assert checked.status_code == 200 and checked.json()["passed"] is True, describe(checked)
        else:
            assert detail["has_cover"] is False, detail


def test_seed_rows_are_stored_in_the_postgres_database_with_no_duplicate_rows_or_objects(backend, store):
    """Seed rows live in the provided database once each, and each seeded image object exists once.

    cov: C-TR-06, C-TR-51, C-DM-133
    """
    assert backend.count("members") == 2
    assert backend.query("SELECT count(*) AS n FROM readers WHERE lower(email) IN (%s, %s)",
                         (READER_EMAIL, READER2_EMAIL))[0]["n"] == 2
    assert backend.count("volumes", position=1) == 1
    volume_id = backend.query("SELECT id FROM volumes WHERE position = 1")[0]["id"]
    assert backend.count("chapters", volume_id=volume_id) == 6
    assert backend.query("SELECT count(*) AS n FROM tips WHERE external_id IN (%s, %s)",
                         (SEED_TIP_ONE, SEED_TIP_TWO))[0]["n"] == 2
    assert backend.count("integrations", provider="tipbox") == 1
    duplicates = backend.query("SELECT key, locale, count(*) AS n FROM messages GROUP BY key, locale HAVING count(*) > 1")
    assert duplicates == [], duplicates
    keys = store.list("chapters/1/")
    per_identifier = {}
    for key in keys:
        match = SHA_KEY_RE.match(key)
        if match:
            per_identifier.setdefault((match.group(2), match.group(3)), []).append(key)
    assert per_identifier, "no seeded chapter image objects were found in the bucket"
    repeated = {k: v for k, v in per_identifier.items() if len(v) > 1}
    assert not repeated, f"seeded identifiers hold more than one object: {list(repeated)[:3]}"
    rows = backend.query("SELECT object_key FROM layer_images")
    assert len({r["object_key"] for r in rows}) == len(rows), "two layer_images rows share one object key"


def test_data_model_tables_carry_named_columns_messages_layer_kinds_entitlement_reasons_one_row_per_locale_unique_board_panel_chapter_numbers_layer_roles_draw_orders_volume_positions_reader_emails_and_no_derived_column(backend, anon):
    """Every named table carries its named columns, uniqueness rules hold in storage, and no derived value is a column.

    cov: C-DM-12, C-DM-13, C-DM-14, C-DM-15, C-DM-16, C-DM-17, C-DM-18, C-DM-19, C-DM-20, C-DM-21, C-DM-22, C-DM-23, C-DM-24, C-DM-25, C-DM-26, C-DM-27, C-DM-28, C-DM-29, C-DM-30, C-DM-31, C-DM-32, C-DM-33, C-DM-34, C-DM-35, C-DM-36, C-DM-37, C-DM-38, C-DM-39, C-DM-40, C-DM-41, C-DM-42, C-DM-43, C-DM-44, C-DM-45, C-DM-46, C-DM-47, C-DM-48, C-DM-49, C-DM-50, C-DM-51, C-DM-52, C-DM-53, C-DM-54
    """
    for table, columns in DATA_MODEL_COLUMNS.items():
        present = columns_of(backend, table)
        missing = [c for c in columns if c not in present]
        assert not missing, f"table {table} lacks columns {missing}"
    for table in ("chapters", "volumes", "layers", "panels", "tips"):
        derived = [c for c in DERIVED_COLUMN_NAMES if c in columns_of(backend, table)]
        assert not derived, f"table {table} stores derived values {derived}"
    assert backend.query("SELECT volume_id, number FROM chapters GROUP BY volume_id, number HAVING count(*) > 1") == []
    assert backend.query("SELECT panel_id, role FROM layers GROUP BY panel_id, role HAVING count(*) > 1") == []
    assert backend.query("SELECT panel_id, draw_order FROM layers GROUP BY panel_id, draw_order HAVING count(*) > 1") == []
    assert backend.query("SELECT position FROM volumes GROUP BY position HAVING count(*) > 1") == []
    assert backend.query("SELECT chapter_id, number FROM boards GROUP BY chapter_id, number HAVING count(*) > 1") == []
    assert backend.query("SELECT board_id, number FROM panels GROUP BY board_id, number HAVING count(*) > 1") == []
    for table, columns in (("chapter_texts", "chapter_id, locale"), ("panel_descriptions", "panel_id, locale"),
                           ("layer_images", "layer_id, locale"), ("messages", "key, locale")):
        assert backend.query(f"SELECT {columns} FROM {table} GROUP BY {columns} HAVING count(*) > 1") == [], table
    assert {r["kind"] for r in backend.query("SELECT DISTINCT kind FROM layers")} <= {"image", "map", "sprite"}
    assert {r["locale"] for r in backend.query("SELECT DISTINCT locale FROM layer_images")} <= {"all", "en", "fr"}
    assert {r["kind"] for r in backend.query("SELECT DISTINCT kind FROM entitlements")} <= {"early_access", "credits"}
    reasons = {r["revoked_reason"] for r in backend.query("SELECT DISTINCT revoked_reason FROM entitlements")}
    assert reasons <= {None, "refunded", "disputed"}, reasons
    positions = [r["position"] for r in backend.query("SELECT position FROM volumes ORDER BY position")]
    assert positions[0] == 1, positions
    upper = READER_EMAIL.upper()
    with api_client() as session:
        attempt = session.post("/auth/register", json={"email": upper, "password": SEED_PASSWORD + "x", "website": ""})
    assert attempt.status_code in (400, 409, 422), describe(attempt)
    assert backend.query("SELECT count(*) AS n FROM readers WHERE lower(email) = lower(%s)", (upper,))[0]["n"] == 1


def test_api_identifiers_timestamps_and_money_use_26_character_sortable_ids_utc_instants_integer_minor_units_apart_from_numbers(author, anon, backend):
    """Identifiers are 26-character strings, numbers stay small integers, timestamps are UTC, money is integer.

    cov: C-TR-26, C-TR-27, C-DM-01, C-DM-02
    """
    stored = backend.query("SELECT table_name, column_name, data_type FROM information_schema.columns "
                           "WHERE table_schema = current_schema() AND column_name LIKE %s", ("%\\_at",))
    wrong = [r for r in stored if r["data_type"] != "timestamp with time zone"]
    assert stored and not wrong, f"stored moments that are not UTC instants: {wrong[:4]}"
    money = backend.query("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = "
                          "current_schema() AND table_name = 'tips' AND column_name IN ('amount', 'settled_amount')")
    assert {r["data_type"] for r in money} <= {"integer", "bigint"}, money
    volume = studio_volume(author, 1)
    assert ULID_RE.match(str(volume["id"])), volume
    assert isinstance(volume["order"], int), volume
    for row in author.get(f"/studio/volumes/{volume['id']}/chapters").json():
        assert ULID_RE.match(str(row["id"])), row
        assert isinstance(row["number"], int) and 1 <= row["number"] <= 6, row
        if row["release_at"]:
            assert str(row["release_at"]).endswith("Z"), row
    for row in all_tips(author)[:20]:
        assert ULID_RE.match(str(row["id"])), row
        assert isinstance(row["amount"], int) and isinstance(row["settled_amount"], int), row
        assert str(row["received_at"]).endswith("Z"), row
    for chapter in volumes()[0]["chapters"]:
        if chapter["release_at"]:
            assert str(chapter["release_at"]).endswith("Z"), chapter


def test_every_response_carries_the_security_headers(site, anon):
    """Pages and API responses carry the pinned security headers.

    cov: C-TR-28, C-TR-29, C-TR-30, C-TR-31, C-TR-32, C-TR-33
    """
    responses = [site.get("/"), site.get("/chapters"), anon.get("/health"), anon.get("/volumes"),
                 site.get("/no-such-page")]
    for response in responses:
        headers = {k.lower(): v for k, v in response.headers.items()}
        for name in SECURITY_HEADERS:
            assert name in headers, f"{name} missing on {response.request.url}"
        assert "frame-ancestors 'none'" in headers["content-security-policy"], headers["content-security-policy"]
        assert headers["x-frame-options"].upper() == "DENY", headers["x-frame-options"]
        assert headers["x-content-type-options"].lower() == "nosniff"
        assert headers["referrer-policy"].lower() == "strict-origin-when-cross-origin"
        policy = headers["permissions-policy"].replace(" ", "")
        assert re.search(r"fullscreen=(\(self\)|\*|\(\"self\"\))", policy), policy
        assert re.search(r"[a-z-]+=\(\)", policy), f"Permissions-Policy denies nothing: {policy}"


def test_cache_control_headers_for_manifests_signed_images_and_reader_responses(anon):
    """Published manifests are public for an hour; unpublished manifests, signed images and reader responses are private.

    cov: C-TR-35, C-TR-36, C-TR-37, C-TR-38, C-TR-39
    """
    published = manifest(1, 1)
    control = published.headers.get("cache-control", "")
    assert "public" in control and "max-age=3600" in control.replace(" ", ""), control
    token = reader_login(READER_EMAIL)
    early = manifest(1, 4, token)
    assert early.status_code == 200, describe(early)
    early_control = early.headers.get("cache-control", "")
    assert "private" in early_control and "no-store" in early_control, early_control
    signed = fetch_absolute(layer_urls(early.json())[0])
    assert signed.status_code == 200, describe(signed)
    assert "private" in signed.headers.get("cache-control", "") and "no-store" in signed.headers.get("cache-control", "")
    with api_client(token) as session:
        for path in ("/me", "/me/progress", "/me/entitlements"):
            response = session.get(path)
            value = response.headers.get("cache-control", "")
            assert "private" in value and "no-store" in value, f"{path}: {value}"


def test_health_endpoint_answers_ok_once_database_and_bucket_are_ready(anon):
    """GET /api/health answers 200 with the pinned body.

    cov: C-TR-12, C-DC-06
    """
    response = anon.get("/health")
    assert response.status_code == 200 and response.json() == {"status": "ok"}, describe(response)


def test_app_is_reachable_from_outside_the_container_at_app_public_url_serving_api_on_the_same_origin(site):
    """The app answers from the verifier at APP_PUBLIC_URL, with the API under /api on that origin.

    cov: C-DC-01, C-DC-02, C-DC-03
    """
    page = site.get("/")
    assert page.status_code == 200 and "<html" in page.text.lower(), describe(page)
    health = site.get("/api/health")
    assert health.status_code == 200 and health.json() == {"status": "ok"}, describe(health)
    assert urlparse(str(health.request.url)).netloc == urlparse(appclient.app_url()).netloc


def test_front_end_is_a_production_build_rendering_pages_from_the_same_origin_json_api(site, chromium):
    """The page shell is a production build, and pages fetch their data from the same-origin JSON API.

    cov: C-TR-02, C-TR-04, C-DC-10
    """
    html = site.get("/chapters").text
    for marker in ("/@vite/client", "vite/dist/client", "react-refresh", "__vite_ping"):
        assert marker not in html, f"a development server marker {marker} is present"
    context = new_context(chromium)
    tab = context.new_page()
    seen = []
    tab.on("request", lambda request: seen.append(request.url))
    open_route(tab, "/chapters", wait=2.0)
    context.close()
    origin = urlparse(appclient.app_url()).netloc
    api_calls = [u for u in seen if urlparse(u).netloc == origin and urlparse(u).path.startswith("/api/")]
    assert any("/api/volumes" in u for u in api_calls), f"the rack did not read /api/volumes: {api_calls[:6]}"


def test_public_routes_answer_in_english_and_french_with_later_volume_chapter_prefix_and_no_browser_language_redirect(site, author):
    """Public routes answer in both locales, later volumes use the volume prefix, and the root never redirects.

    cov: C-CF-41, C-CF-42, C-CF-43, C-CF-44, C-UF-15
    """
    for route in PUBLIC_ROUTES:
        english = site.get(route)
        assert english.status_code == 200, describe(english)
        french = site.get("/fr" if route == "/" else "/fr" + route)
        assert french.status_code == 200, describe(french)
    for route in ("/", "/fr"):
        response = site.get(route, headers={"Accept-Language": "fr-FR,fr;q=0.9" if route == "/" else "en-GB"})
        assert response.status_code == 200, f"{route} redirected by browser language. {describe(response)}"
    built = build_chapter(author)
    assert publish(author, built["chapter"]["id"]).status_code == 200
    later = site.get(f"/volumes/{built['order']}/chapter/1")
    assert later.status_code == 200, describe(later)
    assert manifest(built["order"], 1).status_code == 200
    assert site.get(f"/fr/volumes/{built['order']}/chapter/1").status_code == 200


def test_route_documents_carry_their_own_lang_and_the_pinned_english_and_french_titles_and_descriptions(site):
    """Each route's first HTML response carries its own pinned title, description and lang in both locales.

    cov: C-OV-08, C-CF-49, C-CF-50, C-CF-51, C-CF-52, C-CF-53, C-CF-54, C-CF-55, C-CF-56, C-CF-57, C-CF-58, C-CF-59, C-CF-60, C-CF-61, C-CF-62, C-CF-63, C-CF-64, C-CF-65, C-CF-66, C-CF-67, C-CF-68, C-CF-69, C-CF-70, C-CF-71, C-CF-72, C-CF-73, C-CF-74, C-CF-75, C-CF-76, C-CF-77, C-CF-78, C-CF-79, C-CF-80, C-CF-81, C-CF-82, C-CF-83, C-CF-84, C-CF-85, C-CF-86, C-CF-87, C-CF-88, C-TR-01
    """
    seen = {"en": set(), "fr": set()}
    for table, locale, missing in ((PAGE_META_EN, "en", "/no-such-page"), (PAGE_META_FR, "fr", "/fr/no-such-page")):
        for route, (title, description) in table.items():
            path = missing if route == "not-found" else route
            response = site.get(path)
            assert response.status_code == (404 if route == "not-found" else 200), describe(response)
            got_title, got_desc, lang = document_meta(response.text)
            assert got_title == title, f"{path}: title {got_title!r}"
            assert got_desc == description, f"{path}: description {got_desc!r}"
            assert lang == locale, f"{path}: lang {lang!r}"
            assert got_title not in seen[locale], f"{path} repeats a title"
            seen[locale].add(got_title)
    for number in (2, 3):
        en_title, fr_title = CHAPTER_TITLES[number]
        got_title, got_desc, _ = document_meta(site.get(f"/chapter/{number}").text)
        assert got_title == f"Chapter #{number}: {capitalise_words(en_title)} - Doudou Fever - Interactive Comic", got_title
        assert got_desc == f"Read chapter {number}, {en_title}, of the Doudou Fever interactive comic.", got_desc
        got_title, got_desc, lang = document_meta(site.get(f"/fr/chapter/{number}").text)
        assert got_title == f"Chapitre #{number} : {capitalise_words(fr_title)} - Doudou Fever - BD interactive", got_title
        assert got_desc == f"Lis le chapitre {number}, {fr_title}, de la BD interactive Doudou Fever.", got_desc
        assert lang == "fr"


def test_chapter_route_ladder_renders_not_found_404_redirect_locked_or_reader_by_order(site):
    """Chapter routes answer 404, a redirect, the locked state or the reader in the pinned order.

    cov: C-CF-149, C-CF-162, C-CF-163, C-CF-164, C-CF-166, C-CF-167
    """
    for path in ("/chapter/abc", "/chapter/0", "/chapter/-1", "/chapter/7", "/volumes/99/chapter/1",
                 "/fr/chapter/7"):
        response = site.get(path)
        assert response.status_code == 404, describe(response)
    for path in ("/chapter/1", "/chapter/4", "/chapter/6", "/fr/chapter/4"):
        response = site.get(path)
        assert response.status_code == 200, describe(response)
    with api_client() as anon:
        assert anon.get("/volumes/1/chapters/7").status_code == 404
        assert anon.get("/volumes/99/chapters/1").status_code == 404


def test_locales_en_default_unprefixed_fr_prefixed_with_translated_segments_not_found(site):
    """English is served unprefixed, French under /fr, and a translated segment is a 404 page.

    cov: C-CF-321, C-CF-322
    """
    assert document_meta(site.get("/chapters").text)[2] == "en"
    assert document_meta(site.get("/fr/chapters").text)[2] == "fr"
    for path in ("/fr/chapitres", "/fr/a-propos", "/fr/mentions-legales"):
        response = site.get(path)
        assert response.status_code == 404, describe(response)


def test_catalogue_serves_flat_dotted_keys_for_every_pinned_english_and_french_interface_string_with_transcreated_chapter_titles_and_default_locale_fallback(author, anon):
    """Both catalogues hold every pinned key and value, chapter titles are transcreated, untranslated keys fall back.

    cov: C-CF-332, C-CF-333, C-CF-335, C-CF-336, C-CF-337, C-CF-338, C-CF-339, C-CF-340, C-CF-341, C-CF-342, C-CF-343, C-CF-344, C-CF-345, C-CF-346, C-CF-347, C-CF-348, C-CF-349, C-CF-350, C-CF-351, C-CF-352, C-CF-353, C-CF-354, C-CF-355, C-CF-356, C-CF-357, C-CF-358, C-CF-359, C-CF-360, C-CF-361, C-CF-362, C-CF-363, C-CF-364, C-CF-365, C-CF-366, C-CF-367, C-CF-368, C-CF-369, C-CF-370, C-CF-371, C-CF-372, C-CF-373, C-CF-374, C-CF-375, C-CF-376, C-CF-377, C-CF-378, C-CF-379, C-CF-380, C-CF-381, C-CF-382, C-CF-383, C-CF-384, C-CF-385, C-CF-386, C-CF-387, C-CF-388, C-CF-389, C-CF-390, C-CF-391, C-CF-392, C-CF-393, C-CF-394, C-CF-395, C-CF-396, C-CF-397, C-CF-398, C-CF-399, C-CF-400, C-CF-401, C-CF-402, C-CF-403, C-CF-404, C-CF-405, C-CF-406, C-CF-407, C-CF-408, C-CF-409, C-CF-410, C-CF-411, C-CF-412, C-CF-413, C-CF-414, C-CF-415, C-CF-416, C-CF-417, C-CF-418, C-CF-419, C-CF-420, C-CF-421, C-CF-422, C-CF-423, C-CF-424, C-CF-425, C-CF-426, C-CF-427, C-CF-428, C-CF-429, C-CF-430, C-CF-431, C-CF-432, C-CF-433, C-CF-434, C-CF-435, C-CF-436, C-CF-437, C-CF-438, C-CF-439, C-CF-440, C-CF-441, C-CF-442, C-CF-443, C-CF-444, C-CF-445, C-CF-446, C-CF-447, C-CF-448, C-CF-449, C-CF-450, C-CF-451, C-CF-452, C-CF-453, C-CF-454, C-CF-455, C-CF-456, C-CF-457, C-CF-458, C-CF-459, C-CF-460, C-CF-461, C-CF-462, C-CF-463, C-CF-464, C-CF-465, C-CF-466, C-CF-467, C-CF-468, C-CF-469, C-CF-470, C-CF-471, C-CF-472, C-CF-473, C-CF-474, C-CF-475, C-CF-476, C-CF-477, C-CF-478, C-CF-479, C-CF-480, C-CF-481, C-CF-482, C-CF-483, C-CF-484, C-CF-485, C-CF-486, C-CF-487, C-CF-488, C-CF-489, C-CF-490, C-CF-491, C-CF-492, C-CF-493, C-CF-494, C-CF-495, C-CF-496, C-CF-497, C-CF-498, C-CF-499, C-CF-500, C-CF-501, C-CF-502, C-CF-503, C-CF-504, C-CF-505, C-CF-506, C-CF-507, C-CF-508, C-CF-509, C-CF-510, C-CF-511, C-CF-512, C-CF-513, C-CF-514, C-CF-515, C-CF-516, C-CF-517, C-CF-518, C-CF-519, C-CF-520, C-CF-521, C-CF-522, C-CF-523, C-CF-524, C-CF-525, C-CF-526, C-CF-527, C-CF-528
    """
    english = anon.get("/catalogue/en")
    french = anon.get("/catalogue/fr")
    assert english.status_code == 200 and french.status_code == 200
    en, fr = english.json(), french.json()
    for payload in (en, fr):
        assert all(isinstance(v, str) for v in payload.values()), "catalogue values must be strings in a flat object"
        assert all("." in k for k in payload), "catalogue keys are dotted"
    for key, value in CATALOGUE_EN.items():
        assert en.get(key) == value, f"en {key}: {en.get(key)!r}"
    for key, value in CATALOGUE_FR.items():
        assert fr.get(key) == value, f"fr {key}: {fr.get(key)!r}"
    for namespace in ("index", "chapters", "reader", "about", "legal", "support", "account", "not-found"):
        for suffix in ("meta_title", "meta_description"):
            assert f"{namespace}.{suffix}" in en and f"{namespace}.{suffix}" in fr, f"{namespace}.{suffix} missing"
    titles_fr = {int(c["number"]): c["title"] for c in volumes(locale="fr")[0]["chapters"]}
    for number, title in titles_fr.items():
        assert title == CHAPTER_TITLES[number][1], (number, title)
    entry = next(e for e in author.get("/studio/translations/fr", params={"namespace": "consent"}).json()
                 if e["key"] == "consent.accept")
    flipped = author.put("/studio/translations/fr/consent.accept",
                         json={"value": entry["value"], "state": "untranslated", "note": entry.get("note") or ""})
    assert flipped.status_code == 200, describe(flipped)
    try:
        assert anon.get("/catalogue/fr").json()["consent.accept"] == CATALOGUE_EN["consent.accept"]
    finally:
        restored = author.put("/studio/translations/fr/consent.accept",
                              json={"value": CATALOGUE_FR["consent.accept"], "state": "reviewed",
                                    "note": entry.get("note") or ""})
        assert restored.status_code == 200, describe(restored)
    assert anon.get("/catalogue/fr").json()["consent.accept"] == CATALOGUE_FR["consent.accept"]


def image_parts(url: str) -> tuple:
    parsed = urlparse(url)
    return parsed.path, {k: v[0] for k, v in parse_qs(parsed.query).items()}


def with_query(path: str, query: dict) -> str:
    return path + "?" + "&".join(f"{k}={v}" for k, v in query.items())


def test_scheduled_or_draft_chapter_manifest_is_not_found_for_every_public_caller_or_untipped_reader_session(backend):
    """A scheduled or draft chapter's manifest answers 404, never 403, to visitors and untipped readers.

    cov: C-OV-04, C-RL-05, C-RL-06, C-CF-200, C-CF-203, C-CF-204, C-CF-205, C-UF-28, C-DC-22
    """
    fresh = register_reader()
    for token in (None, fresh["token"]):
        for number in (4, 5, 6):
            response = manifest(1, number, token)
            assert response.status_code == 404, f"chapter {number} leaked. {describe(response)}"
            assert "boards" not in response.text and "image_url" not in response.text
    entitled = reader_login(READER_EMAIL)
    assert manifest(1, 6, entitled).status_code == 404, "a draft chapter is readable by nobody on the public surface"
    assert manifest(1, 5, entitled).status_code == 404, "chapter 5 is outside its early-access window"
    assert manifest(1, 99).status_code == 404 and manifest(42, 1).status_code == 404
    for number in (4, 5, 6):
        assert manifest(1, number).status_code != 403


def test_unpublished_chapter_images_need_a_valid_expiring_lowercase_hex_signature_opening_only_that_image(anon):
    """Early-access image addresses carry expires and a lowercase hex sig; unsigned, altered or borrowed sigs answer 404.

    cov: C-OV-05, C-CF-210, C-CF-212, C-CF-213, C-CF-214, C-CF-215, C-TR-42, C-TR-43, C-DC-23
    """
    token = reader_login(READER_EMAIL)
    body = manifest(1, 4, token).json()
    urls = layer_urls(body)
    assert len(urls) >= 2, urls
    first_path, first_query = image_parts(urls[0])
    second_path, second_query = image_parts(urls[1])
    assert "expires" in first_query and "sig" in first_query and "tag" in first_query, urls[0]
    assert re.fullmatch(r"[0-9a-f]+", first_query["sig"]), first_query["sig"]
    remaining = int(first_query["expires"]) - int(utc_now().timestamp())
    assert 0 < remaining <= 15 * 60 + 5, f"a signed address must stay valid for 15 minutes, not {remaining}s"
    assert fetch_absolute(urls[0]).status_code == 200
    unsigned = {k: v for k, v in first_query.items() if k not in ("sig", "expires")}
    assert fetch_absolute(with_query(first_path, unsigned)).status_code == 404
    altered = dict(first_query, sig=first_query["sig"][:-1] + ("0" if first_query["sig"][-1] != "0" else "1"))
    assert fetch_absolute(with_query(first_path, altered)).status_code == 404
    stretched = dict(first_query, expires=str(int(first_query["expires"]) + 3600))
    assert fetch_absolute(with_query(first_path, stretched)).status_code == 404
    borrowed = dict(second_query, sig=first_query["sig"], expires=first_query["expires"])
    assert fetch_absolute(with_query(second_path, borrowed)).status_code == 404
    assert fetch_absolute(with_query(first_path, {"tag": first_query["tag"]})).status_code == 404


def test_early_access_opens_a_scheduled_chapter_only_inside_its_window_until_expired_or_revoked_on_the_next_request(backend):
    """Early access opens chapter 4 inside its window, never chapter 5, and closes on the next request once expired or revoked.

    cov: C-RL-09, C-RL-10, C-CF-196, C-CF-197, C-CF-198, C-CF-199, C-CF-201, C-UF-26, C-DM-71
    """
    seeded = reader_login(READER_EMAIL)
    assert manifest(1, 4, seeded).status_code == 200
    assert manifest(1, 5, seeded).status_code == 404
    for column, value in (("expires_at", "now() - interval '1 second'"), ("revoked_at", "now()")):
        probe = register_reader()
        token_value = return_token()
        body = event_body("tip.received", tip_data(600, email=probe["email"], token=token_value))
        assert claim(token_value, probe["token"]).status_code == 200
        assert deliver(body).status_code == 200
        assert wait_for(lambda: manifest(1, 4, probe["token"]).status_code == 200), "early access never opened"
        backend.query(f"UPDATE entitlements SET {column} = {value} WHERE reader_id = "
                      "(SELECT id FROM readers WHERE lower(email) = lower(%s)) RETURNING id", (probe["email"],))
        assert manifest(1, 4, probe["token"]).status_code == 404, f"{column} did not close access on the next request"


def test_visitor_reads_published_chapter_manifest_with_boards_panels_layers(anon):
    """A visitor reads chapter 1's manifest with its boards, panels and fully described layers.

    cov: C-RL-01, C-CF-124, C-CF-195, C-CF-202, C-DC-28
    """
    response = manifest(1, 1)
    assert response.status_code == 200, describe(response)
    body = response.json()
    for key in ("volume", "number", "title", "description", "total", "content_tag", "boards"):
        assert key in body, f"manifest lacks {key}"
    assert body["title"] == CHAPTER_TITLES[1][0]
    assert [len(b["panels"]) for b in sorted(body["boards"], key=lambda b: int(b["number"]))] == [3, 2]
    for board in body["boards"]:
        for panel in board["panels"]:
            for key in ("number", "index", "description", "selectable", "layers"):
                assert key in panel, f"panel lacks {key}"
            for layer in panel["layers"]:
                for key in ("role", "identifier", "kind", "depth", "offset_x", "offset_y", "scale", "opacity",
                            "blend", "draw_order", "image_url", "frame_table_url"):
                    assert key in layer, f"layer lacks {key}"
                assert fetch_absolute(layer["image_url"]).status_code == 200, layer["image_url"]


def test_volume_list_marks_locked_chapters_with_release_moments_hiding_drafts(anon):
    """The volume list marks locked chapters with public titles and release moments and never lists the draft.

    cov: C-RL-02, C-CF-218, C-CF-219, C-CF-220, C-CF-221
    """
    listing = volumes()
    first = next(v for v in listing if int(v["order"]) == 1)
    assert first["label"] == VOLUME_ONE_LABEL and int(first["chapter_count"]) == 6, first
    chapters = {int(c["number"]): c for c in first["chapters"]}
    assert sorted(chapters) == [1, 2, 3, 4, 5], "the draft chapter must never be listed"
    for number, chapter in chapters.items():
        assert chapter["title"] == CHAPTER_TITLES[number][0]
        assert chapter["locked"] is (number >= 4), chapter
        assert chapter["release_at"], chapter
    entitled = {int(c["number"]): c for c in volumes(reader_login(READER_EMAIL))[0]["chapters"]}
    assert entitled[4]["locked"] is False and entitled[5]["locked"] is True, entitled


def test_covers_and_sitemaps_publish_only_published_or_scheduled_chapters_hiding_drafts(anon, site):
    """Covers serve published and scheduled chapters only; sitemaps list static routes and published chapters only.

    cov: C-CF-222, C-CF-223, C-CF-224, C-CF-225, C-CF-226, C-CF-227
    """
    for number in (1, 2, 3, 4, 5):
        cover = anon.get(f"/covers/1/{number}.png")
        assert cover.status_code == 200 and cover.content[:8] == b"\x89PNG\r\n\x1a\n", describe(cover)
    assert anon.get("/covers/1/6.png").status_code == 404
    english = site.get("/sitemap.xml")
    french = site.get("/fr/sitemap.xml")
    assert english.status_code == 200 and french.status_code == 200
    for number in (1, 2, 3):
        assert f"/chapter/{number}</loc>" in english.text and f"/fr/chapter/{number}</loc>" in french.text
    for number in (4, 5, 6):
        assert f"/chapter/{number}<" not in english.text and f"/chapter/{number}<" not in french.text
    for route in ("/chapters", "/about", "/legal"):
        assert f"{route}</loc>" in english.text and f"/fr{route}</loc>" in french.text
    assert "/fr/" not in english.text


def test_object_store_refuses_anonymous_requests_for_image_objects(store):
    """Image objects exist in the bucket and refuse any request made without credentials.

    cov: C-CF-228, C-CF-229, C-TR-08
    """
    keys = store.list("chapters/1/4/")
    assert keys, "chapter 4 has no image objects in the bucket"
    endpoint = os.environ["STORAGE_ENDPOINT"].rstrip("/")
    bucket = os.environ["STORAGE_BUCKET"]
    for key in keys[:3] + store.list("chapters/1/1/")[:2]:
        response = httpx.get(f"{endpoint}/{bucket}/{key}", timeout=appclient.TIMEOUT)
        assert response.status_code in (401, 403), f"object {key} answered anonymously: {response.status_code}"
    listing = httpx.get(f"{endpoint}/{bucket}?list-type=2", timeout=appclient.TIMEOUT)
    assert listing.status_code in (401, 403), "the bucket lists its keys anonymously"


def test_published_chapter_images_need_no_signature_with_immutable_cache(anon):
    """Published images need no signature and are cached publicly for a year as immutable.

    cov: C-CF-217, C-TR-34
    """
    for url in layer_urls(manifest(1, 2).json())[:4]:
        path, query = image_parts(url)
        assert "sig" not in query and "expires" not in query, url
        response = fetch_absolute(url)
        assert response.status_code == 200 and response.content[:8] == b"\x89PNG\r\n\x1a\n", url
        control = response.headers.get("cache-control", "").replace(" ", "")
        assert "public" in control and "max-age=31536000" in control and "immutable" in control, control


def test_manifest_total_index_and_texture_addresses_follow_the_pinned_rules(author):
    """A manifest's total counts the volume's chapters, panel index runs across the chapter, and addresses follow the scheme.

    cov: C-CF-206, C-CF-207, C-CF-208
    """
    version = int(settings_of(author)["asset_version"])
    order, number = 1, 1
    body = manifest(order, number).json()
    assert int(body["total"]) == 6, body["total"]
    indexes = [int(p["index"]) for b in sorted(body["boards"], key=lambda b: int(b["number"]))
               for p in sorted(b["panels"], key=lambda p: int(p["number"]))]
    assert indexes == [1, 2, 3, 4, 5], indexes
    for board in body["boards"]:
        for panel in board["panels"]:
            for layer in panel["layers"]:
                path, query = image_parts(layer["image_url"])
                identifier = re.escape(layer["identifier"])
                assert re.fullmatch(rf"/api/textures/v{version}/{order}/{number}/{identifier}(-en|-fr)?\.png", path), path
                assert query.get("tag") == body["content_tag"], query
                assert layer["frame_table_url"] is None, layer


def test_seeded_panel_layer_images_live_in_object_store_at_content_hash_keys(store):
    """Seeded layer images live in the bucket at chapters/<order>/<number>/<identifier>/<sha256>.png of their bytes.

    cov: C-OV-07, C-TR-07, C-DM-80
    """
    body = manifest(1, 1).json()
    for board in body["boards"]:
        for panel in board["panels"]:
            for layer in panel["layers"]:
                identifier = layer["identifier"]
                prefix = f"chapters/1/1/{identifier}/"
                keys = [k for k in store.list(prefix) if SHA_KEY_RE.match(k)]
                if layer["role"] == "sign":
                    keys = [k for k in store.list(f"chapters/1/1/{identifier}-en/") if SHA_KEY_RE.match(k)]
                    assert [k for k in store.list(f"chapters/1/1/{identifier}-fr/") if SHA_KEY_RE.match(k)], identifier
                assert len(keys) == 1, f"{identifier} has {len(keys)} objects"
                served = fetch_absolute(layer["image_url"]).content
                assert keys[0].endswith(hashlib.sha256(served).hexdigest() + ".png"), keys[0]


def test_notify_me_records_drop_preference_keeping_drops_or_all():
    """notify me records the wish to hear of drops, leaving notifications at drops or all.

    cov: C-CF-159, C-CF-160, C-CN-04
    """
    probe = register_reader()
    with api_client(probe["token"]) as session:
        assert session.patch("/me", json={"notifications": "none"}).status_code == 200
        noted = session.post("/me/notify", json={"volume": 1, "chapter": 4})
        assert noted.status_code == 200 and noted.json()["notifications"] == "drops", describe(noted)
        assert session.patch("/me", json={"notifications": "all"}).status_code == 200
        again = session.post("/me/notify", json={"volume": 1, "chapter": 4})
        assert again.status_code == 200 and again.json()["notifications"] == "all", describe(again)
        assert session.get("/me").json()["notifications"] == "all"


def test_studio_endpoints_never_return_individual_reader_progress(author):
    """No studio response carries a reader's progress, sessions or account address.

    cov: C-RL-18, C-CF-308, C-CF-309, C-CF-310
    """
    volume = studio_volume(author, 1)
    paths = ["/studio/overview", "/studio/insights", "/studio/page-views", "/studio/settings",
             f"/studio/volumes/{volume['id']}/chapters", "/studio/search?q=reader2", "/studio/tips/totals"]
    for path in paths:
        response = author.get(path)
        assert response.status_code == 200, describe(response)
        text = response.text
        assert READER2_EMAIL not in text, f"{path} exposes a reader address"
        assert '"last_panel"' not in text and '"fraction"' not in text, f"{path} exposes reading progress"
        assert "token_hash" not in text and "reader_sessions" not in text, f"{path} exposes sessions"
    for path in ("/studio/readers", "/studio/progress", "/studio/readers/progress"):
        assert author.get(path).status_code in (404, 405), path


def test_anonymous_calls_are_denied_and_reader_or_author_tokens_are_refused_on_each_others_surface(author_token):
    """Anonymous calls to reader or studio endpoints are denied; each token kind is refused on the other surface.

    cov: C-RL-07, C-RL-20, C-RL-21, C-CF-30, C-CF-31, C-CF-32, C-TR-10, C-DC-17
    """
    reader_token = reader_login(READER_EMAIL)
    reader_paths = ["/me", "/me/progress", "/me/entitlements", "/me/export"]
    studio_paths = ["/studio/volumes", "/studio/overview", "/studio/tips", "/studio/settings"]
    for token, paths in ((None, reader_paths + studio_paths), (reader_token, studio_paths), (author_token, reader_paths)):
        with api_client(token) as session:
            for path in paths:
                response = session.get(path)
                assert response.status_code in (401, 403), f"{path} served a denied caller. {describe(response)}"
    with api_client(reader_token) as session:
        assert session.get("/me").status_code == 200
    with api_client(author_token) as session:
        assert session.get("/studio/volumes").status_code == 200


def test_reader_session_denied_on_author_only_endpoint_leaves_chapter_unchanged(author):
    """A reader session calling author-only mutations is denied and the chapter stays exactly as it was.

    cov: C-RL-22, C-RL-23
    """
    target = studio_chapter_row(author, 1, 6)
    before = studio_chapter(author, target["id"])
    scheduled = studio_chapter_row(author, 1, 4)
    probe = register_reader()
    volumes_before = len(author.get("/studio/volumes").json())
    with api_client(probe["token"]) as session:
        attempts = [
            session.patch(f"/studio/chapters/{target['id']}", json={"version": before["version"],
                                                                       "titles": {"en": "stolen", "fr": "vole"}}),
            session.post(f"/studio/chapters/{scheduled['id']}/publish"),
            session.post(f"/studio/chapters/{target['id']}/ready"),
            session.post("/studio/volumes", json={"label": "Intruder"}),
            session.post("/studio/asset-version"),
        ]
    for response in attempts:
        assert response.status_code in (401, 403), f"an author-only mutation served a reader. {describe(response)}"
    after = studio_chapter(author, target["id"])
    assert after["version"] == before["version"] and after["state"] == before["state"], (before, after)
    assert studio_chapter_row(author, 1, 6)["titles"]["en"] == CHAPTER_TITLES[6][0]
    assert studio_chapter_row(author, 1, 4)["state"] == "scheduled"
    assert len(author.get("/studio/volumes").json()) == volumes_before


def test_bearer_tokens_authenticate_readers_and_authors_with_passwords_and_session_tokens_never_stored_as_typed_or_issued(backend, author_token):
    """Bearer tokens authenticate both surfaces; passwords and session tokens are stored only in hashed form.

    cov: C-CF-27, C-CF-28, C-TR-09
    """
    probe = register_reader()
    with httpx.Client(base_url=appclient.api_base(), timeout=appclient.TIMEOUT) as raw:
        ok = raw.get("/me", headers={"Authorization": f"Bearer {probe['token']}"})
        assert ok.status_code == 200 and ok.json()["email"] == probe["email"], describe(ok)
        studio = raw.get("/studio/volumes", headers={"Authorization": f"Bearer {author_token}"})
        assert studio.status_code == 200, describe(studio)
    for table in ("readers", "members"):
        rows = backend.query(f"SELECT password_hash FROM {table}")
        assert rows and all(SEED_PASSWORD not in str(r["password_hash"]) for r in rows), f"{table} stores a typed password"
    stored = backend.query("SELECT password_hash FROM readers WHERE lower(email) = lower(%s)", (probe["email"],))
    assert stored and str(stored[0]["password_hash"]) != probe["password"]
    for table, token in (("reader_sessions", probe["token"]), ("studio_sessions", author_token)):
        hashes = {str(bytes(r["token_hash"]).hex() if isinstance(r["token_hash"], (bytes, memoryview)) else r["token_hash"])
                  for r in backend.query(f"SELECT token_hash FROM {table}")}
        assert hashes, f"{table} holds no rows"
        assert token not in hashes, f"{table} stores a token as issued"


def test_studio_offers_no_deletion_or_renumbering_and_pages_ignore_debug_parameters_with_no_rate_limit_beyond_the_sign_in_lockout(author, site, anon):
    """No delete or renumber path exists, debug query parameters change no page or API answer, and ordinary calls are not rate limited.

    cov: C-CN-10, C-CN-11, C-CN-12, C-CN-13
    """
    target = studio_chapter_row(author, 1, 6)
    detail = studio_chapter(author, target["id"])
    board = detail["boards"][0]
    panel = author.get(f"/studio/boards/{board['id']}").json()["panels"][0]
    for path in (f"/studio/chapters/{target['id']}", f"/studio/boards/{board['id']}", f"/studio/panels/{panel['id']}"):
        response = author.delete(path)
        assert response.status_code in (404, 405), f"DELETE {path} answered {response.status_code}"
    renumber = author.patch(f"/studio/chapters/{target['id']}", json={"version": detail["version"], "number": 9})
    assert renumber.status_code in (200, 400, 409, 422), describe(renumber)
    assert int(studio_chapter_row(author, 1, 6)["number"]) == 6
    assert studio_chapter(author, target["id"])["state"] == "draft"
    plain = document_meta(site.get("/chapters").text)
    for query in ("?debug=1", "?debug=true&gui=1", "?stats=1&wireframe=1"):
        response = site.get("/chapters" + query)
        assert response.status_code == 200 and document_meta(response.text) == plain, query
    listing = anon.get("/volumes").json()
    for query in ("?debug=1", "?debug=true&gui=1", "?stats=1&wireframe=1"):
        response = anon.get("/volumes" + query)
        assert response.status_code == 200 and response.json() == listing, f"the volume list changed under {query}"
    for _ in range(40):
        response = anon.post("/page-views", json={"route": "chapters"})
        assert response.status_code in (200, 201, 204), f"a page view was rate limited. {describe(response)}"


def test_api_responses_carry_x_request_id_and_rejections_use_the_error_body_shape_never_a_server_error(anon):
    """API responses carry X-Request-Id, and rejections are client errors whose body repeats it as request_id.

    cov: C-TR-19, C-TR-20, C-TR-21, C-TR-22, C-DC-16
    """
    health = anon.get("/health")
    assert health.headers.get("x-request-id"), "X-Request-Id missing on /api/health"
    probe = register_reader()
    rejected = [
        anon.get("/me"),
        anon.post("/auth/register", json={"email": "not-an-address", "password": SEED_PASSWORD, "website": ""}),
        anon.post("/page-views", json={"route": "nowhere"}),
        anon.post("/events", json={"name": "chapter_opened", "params": {"email": "someone"}}),
    ]
    with api_client(probe["token"]) as session:
        rejected.append(session.put("/me/progress", json={"last_chapter": None, "last_chapter_at": None,
                                                           "chapters": [{"volume": 1, "chapter": 1, "fraction": 7,
                                                                         "last_panel": 1}]}))
        rejected.append(session.request("DELETE", "/me", json={"password": "wrong-password-value"}))
    for response in rejected:
        assert 400 <= response.status_code < 500, f"a rejection was not a client error. {describe(response)}"
        error = error_of(response)
        for key in ("code", "message", "field", "request_id"):
            assert key in error, f"error body lacks {key}. {describe(response)}"
        assert error["request_id"] == response.headers.get("x-request-id"), describe(response)


SHAPES = {
    "/volumes": ("id", "label", "order", "chapter_count", "chapters"),
    "/me": ("email", "locale", "notifications", "created_at"),
    "/me/progress": ("last_chapter", "last_chapter_at", "chapters"),
    "/studio/overview": ("next_drop", "unready", "support", "reading", "alerts", "revocations"),
    "/studio/settings": ("name", "contact_email", "time_zone", "currency", "default_locale", "early_access_threshold",
                         "credit_threshold", "asset_version"),
    "/studio/integrations/tipbox": ("page_url", "secret_last_four", "secret_created_at", "secret_last_used_at"),
    "/studio/tips/totals": ("by_month", "by_source"),
    "/studio/insights": ("server", "measured"),
    "/studio/page-views": ("items", "next_cursor"),
    "/studio/tips": ("items", "next_cursor"),
}


def test_api_request_fields_and_response_shapes_carry_the_exact_field_names(author, reader):
    """Every documented response carries its exact field names.

    cov: C-DC-15, C-DC-20, C-DC-29, C-DC-30, C-DC-31, C-DC-32, C-DC-33, C-DC-34, C-DC-35, C-DC-36, C-DC-37, C-DC-38, C-DC-39, C-DC-40, C-DC-41, C-DC-42, C-DC-43, C-DC-44, C-DC-45, C-DC-46, C-DC-47, C-DC-48, C-DC-49, C-DC-50, C-DC-51, C-DC-52, C-DC-53, C-DC-54, C-DC-55, C-DC-56, C-DC-57, C-DC-58, C-DC-59, C-DC-60, C-DC-61, C-DC-62, C-DC-63, C-DC-64, C-DC-65, C-DC-66, C-DC-67, C-DC-68, C-DC-69, C-DC-70, C-DC-71, C-DC-72, C-DC-73, C-DC-74, C-DC-75, C-DC-76, C-DC-77, C-DC-78, C-DC-79, C-DC-80, C-DC-81, C-DC-82, C-DC-83, C-DC-84, C-DC-85, C-DC-86, C-DC-87, C-DC-88, C-DC-89, C-DC-90, C-DC-91, C-DC-92, C-DC-93, C-DC-94, C-DC-95, C-DC-96, C-DC-97, C-DC-98, C-DC-99, C-DC-100, C-DC-101, C-DC-102, C-DC-103, C-DC-104, C-DC-105, C-DC-106, C-DC-107, C-DC-108, C-DC-109, C-DC-110, C-DC-111, C-DC-112, C-DC-113, C-DC-114, C-DC-115, C-DC-116, C-DC-117, C-DC-118, C-DC-119, C-DC-120, C-DC-121
    """
    def keys_of(payload):
        return set(payload[0]) if isinstance(payload, list) else set(payload)

    for path, fields in SHAPES.items():
        session = reader if path.startswith("/me") else author
        response = session.get(path)
        assert response.status_code == 200, describe(response)
        missing = set(fields) - keys_of(response.json())
        assert not missing, f"{path} lacks {sorted(missing)}"
    assert set(author.get("/studio/volumes").json()[0]) >= {"id", "label", "order", "chapter_count"}
    volume = studio_volume(author, 1)
    rows = author.get(f"/studio/volumes/{volume['id']}/chapters").json()
    assert set(rows[0]) >= {"id", "number", "titles", "state", "release_at", "published_at", "boards_ready",
                            "boards_total", "image_bytes", "version"}
    detail = studio_chapter(author, rows[0]["id"])
    assert set(detail) >= {"boards", "waivers", "early_access_days", "content_tag", "has_cover"}
    insights = author.get("/studio/insights").json()
    assert set(insights["server"]) >= {"page_views", "chapter_opens"} and "events" in insights["measured"]
    totals = author.get("/studio/tips/totals").json()
    if totals["by_month"]:
        assert set(totals["by_month"][0]) >= {"month", "count", "total"}
    assert set(totals["by_source"][0]) >= {"source", "count", "total"}
    assert set(author.get("/studio/tips").json()["items"][0]) >= set(TIP_ROW_FIELDS)
    assert set(reader.get("/me/entitlements").json()[0]) >= {"kind", "granted_at", "expires_at", "revoked_at", "active"}
    coverage = author.get("/studio/translations/coverage").json()
    assert set(coverage[0]) >= {"namespace", "locale", "total", "translated", "reviewed", "percent"}
    entries = author.get("/studio/translations/en", params={"namespace": "chrome"}).json()
    assert set(entries[0]) >= {"key", "source", "value", "state", "note"}
    results = author.get("/studio/search", params={"q": "Varny"}).json()
    assert results and set(results[0]) >= {"type", "label", "href"}
    issued = httpx.post(f"{appclient.api_base()}/tips/return-tokens", timeout=appclient.TIMEOUT).json()
    assert set(issued) >= {"token", "expires_at"}
    with api_client() as anon:
        assert set(anon.post("/tips/return", json={"token": issued["token"]}).json()) >= {"status"}


def test_open_reader_signup_returns_token_starting_at_drops_notifications():
    """Anyone registers a reader, receives an access token, and starts at drops with the chosen locale.

    cov: C-RL-25, C-CF-01, C-CF-02, C-CF-03
    """
    english = register_reader()
    french = register_reader(locale="fr")
    for probe, locale in ((english, None), (french, "fr")):
        with api_client(probe["token"]) as session:
            me = session.get("/me")
        assert me.status_code == 200, describe(me)
        body = me.json()
        assert body["email"] == probe["email"] and body["notifications"] == "drops", body
        if locale:
            assert body["locale"] == locale, body


def test_signup_with_filled_website_decoy_is_refused_as_bot_creating_no_account(backend):
    """A registration that fills the website decoy is refused and creates no account.

    cov: C-CF-04, C-CF-05, C-CN-14
    """
    email = probe_email()
    with api_client() as anon:
        response = anon.post("/auth/register", json={"email": email, "password": SEED_PASSWORD,
                                                      "website": "https://spam.example"})
    assert 400 <= response.status_code < 500, describe(response)
    assert backend.query("SELECT count(*) AS n FROM readers WHERE lower(email) = lower(%s)", (email,))[0]["n"] == 0
    login = httpx.post(f"{appclient.api_base()}/auth/login", json={"email": email, "password": SEED_PASSWORD},
                       timeout=appclient.TIMEOUT)
    assert login.status_code != 200


def test_signup_or_address_change_rejects_short_password_malformed_or_duplicate_email_address_with_the_neutral_message_ignoring_case(backend):
    """Short passwords and malformed addresses are rejected by field; a used address gets only the neutral message.

    cov: C-CF-07, C-CF-08, C-CF-09, C-CF-10, C-CF-11, C-CF-12, C-CF-13
    """
    email = probe_email()
    with api_client() as anon:
        short = anon.post("/auth/register", json={"email": email, "password": "short-pw-11", "website": ""})
        assert_rejected(short, field="password")
        malformed = anon.post("/auth/register", json={"email": "no-at-sign.example", "password": SEED_PASSWORD,
                                                      "website": ""})
        assert_rejected(malformed, field="email")
        assert backend.query("SELECT count(*) AS n FROM readers WHERE lower(email) = lower(%s)", (email,))[0]["n"] == 0
        for used in (READER_EMAIL, READER_EMAIL.upper(), READER_EMAIL.capitalize()):
            duplicate = anon.post("/auth/register", json={"email": used, "password": SEED_PASSWORD, "website": ""})
            error = assert_rejected(duplicate)
            assert error["message"] == DUPLICATE_ADDRESS_MESSAGE, error
            assert "exist" not in duplicate.text.lower() and "already" not in duplicate.text.lower()
    probe = register_reader()
    with api_client(probe["token"]) as session:
        change = session.patch("/me", json={"email": READER2_EMAIL.upper()})
    error = assert_rejected(change)
    assert error["message"] == DUPLICATE_ADDRESS_MESSAGE, error


def test_reader_patch_changes_locale_notifications_email_with_signup_validation():
    """PATCH /api/me changes locale, notifications and email, validating each as at signup.

    cov: C-RL-11, C-CF-318, C-CF-319, C-CF-320
    """
    probe = register_reader()
    with api_client(probe["token"]) as session:
        for body in ({"locale": "fr"}, {"notifications": "all"}, {"notifications": "none"}, {"notifications": "drops"}):
            response = session.patch("/me", json=body)
            assert response.status_code == 200, describe(response)
            for key, value in body.items():
                assert response.json()[key] == value
        new_email = probe_email()
        moved = session.patch("/me", json={"email": new_email})
        assert moved.status_code == 200 and moved.json()["email"] == new_email, describe(moved)
        assert_rejected(session.patch("/me", json={"locale": "de"}), field="locale")
        assert_rejected(session.patch("/me", json={"notifications": "weekly"}), field="notifications")
        assert_rejected(session.patch("/me", json={"email": "bad-address"}), field="email")
    assert reader_login(new_email)


def progress_doc(last: tuple | None, at: str | None, entries: list) -> dict:
    return {"last_chapter": {"volume": last[0], "chapter": last[1]} if last else None, "last_chapter_at": at,
            "chapters": [{"volume": v, "chapter": c, "fraction": f, "last_panel": p} for v, c, f, p in entries]}


def comparable(doc: dict) -> tuple:
    chapters = sorted((int(c["volume"]), int(c["chapter"]), round(float(c["fraction"]), 3), int(c["last_panel"]))
                      for c in doc["chapters"])
    last = doc["last_chapter"]
    return (int(last["volume"]), int(last["chapter"])) if last else None, chapters


def test_reader_progress_document_merges_greater_fraction_then_last_panel_later_last_chapter_idempotently_across_devices_rejecting_invalid_fractions():
    """Progress merges per chapter and by moment, commutes, is idempotent, drops unknown chapters and rejects bad fractions.

    cov: C-RL-08, C-CF-291, C-CF-292, C-CF-293, C-CF-294, C-CF-295, C-CF-296, C-CF-297, C-CF-298, C-CF-299, C-CF-300, C-CF-301, C-CF-302, C-CF-303, C-CF-304, C-CF-305
    """
    early, late = "2026-09-01T10:00:00Z", "2026-09-02T10:00:00Z"
    phone = progress_doc((1, 2), late, [(1, 1, 0.5, 3), (1, 2, 0.2, 1)])
    laptop = progress_doc((1, 1), early, [(1, 1, 0.5, 4), (1, 2, 0.125, 9), (1, 99, 0.3, 1)])
    results = []
    for order in ((phone, laptop), (laptop, phone)):
        probe = register_reader()
        with api_client(probe["token"]) as session:
            first = session.put("/me/progress", json=order[0])
            assert first.status_code == 200, describe(first)
            merged = session.put("/me/progress", json=order[1])
            assert merged.status_code == 200, describe(merged)
            assert set(merged.json()) >= {"last_chapter", "last_chapter_at", "chapters"}
            again = session.put("/me/progress", json=order[1])
            assert comparable(again.json()) == comparable(merged.json()), "sending the same document twice changed it"
            stored = session.get("/me/progress").json()
            assert comparable(stored) == comparable(merged.json())
            results.append(comparable(stored))
            for bad in (1.2, -0.1, 0.1234):
                rejected = session.put("/me/progress", json=progress_doc((1, 3), late, [(1, 3, bad, 1)]))
                assert 400 <= rejected.status_code < 500, describe(rejected)
            assert comparable(session.get("/me/progress").json()) == comparable(stored), "a rejected write changed progress"
    assert results[0] == results[1], "device order changed the merged document"
    assert results[0] == ((1, 2), [(1, 1, 0.5, 4), (1, 2, 0.2, 1)]), results[0]


def test_concurrent_progress_writes_from_two_devices_end_in_one_merged_row(backend):
    """Two simultaneous progress writes for one chapter leave one stored row holding the greater position.

    cov: C-DM-57, C-DM-58
    """
    probe = register_reader()
    documents = [progress_doc((1, 3), "2026-09-03T10:00:00Z", [(1, 3, 0.25, 2)]),
                 progress_doc((1, 3), "2026-09-03T10:00:01Z", [(1, 3, 0.75, 6)])]

    def send(doc):
        with api_client(probe["token"]) as session:
            return session.put("/me/progress", json=doc)

    responses = run_together([lambda d=d: send(d) for d in documents])
    assert all(r.status_code == 200 for r in responses), [describe(r) for r in responses]
    rows = backend.query("SELECT p.fraction, p.last_panel FROM progress p JOIN readers r ON r.id = p.reader_id "
                         "JOIN chapters c ON c.id = p.chapter_id JOIN volumes v ON v.id = c.volume_id "
                         "WHERE lower(r.email) = lower(%s) AND c.number = 3 AND v.position = 1", (probe["email"],))
    assert len(rows) == 1, f"expected one progress row, found {len(rows)}"
    assert abs(float(rows[0]["fraction"]) - 0.75) < 1e-9 and int(rows[0]["last_panel"]) == 6, rows


def test_reader_export_and_account_deletion_cover_only_the_readers_own_progress_and_data_keeping_tips_anonymised_wrong_password_deleting_nothing(backend, author):
    """Export returns only the reader's own data as an attachment; deletion needs the password and anonymises tips.

    cov: C-RL-12, C-RL-13, C-RL-14, C-RL-24, C-CF-311, C-CF-312, C-CF-313, C-CF-314, C-CF-315, C-CF-316, C-CF-317
    """
    probe = register_reader()
    token_value = return_token()
    assert claim(token_value, probe["token"]).status_code == 200
    data = tip_data(700, email=probe["email"], token=token_value)
    assert deliver(event_body("tip.received", data)).status_code == 200
    assert wait_for(lambda: "early_access" in active_kinds(probe["token"]))
    with api_client(probe["token"]) as session:
        assert session.put("/me/progress", json=progress_doc((1, 2), "2026-09-05T10:00:00Z", [(1, 2, 0.5, 2)])).status_code == 200
        exported = session.get("/me/export")
        assert exported.status_code == 200, describe(exported)
        assert "attachment" in exported.headers.get("content-disposition", "").lower()
        body = exported.json()
        assert set(body) >= {"reader", "progress", "entitlements", "tips"}
        assert body["reader"]["email"] == probe["email"]
        assert READER_EMAIL not in exported.text and READER2_EMAIL not in exported.text
        assert any(t.get("tip_id", t.get("external_id")) == data["tip_id"] for t in body["tips"]), body["tips"]
        wrong = session.request("DELETE", "/me", json={"password": "not-the-password-1"})
        assert 400 <= wrong.status_code < 500, describe(wrong)
        assert session.get("/me").status_code == 200, "a wrong password deleted the account"
        gone = session.request("DELETE", "/me", json={"password": probe["password"]})
        assert gone.status_code in (200, 204), describe(gone)
        assert session.get("/me").status_code == 401
    assert backend.query("SELECT count(*) AS n FROM readers WHERE lower(email) = lower(%s)", (probe["email"],))[0]["n"] == 0
    kept = backend.query("SELECT matched_reader_id, supporter_email FROM tips WHERE external_id = %s", (data["tip_id"],))
    assert len(kept) == 1 and kept[0]["matched_reader_id"] is None and kept[0]["supporter_email"] is None, kept
    orphans = backend.query("SELECT count(*) AS n FROM entitlements e LEFT JOIN readers r ON r.id = e.reader_id "
                            "WHERE r.id IS NULL")[0]["n"]
    assert orphans == 0, "entitlements survived their reader"


def newest_session_hash(backend, table: str, owner_column: str, owner_table: str, email: str) -> str:
    rows = backend.query(f"SELECT s.token_hash FROM {table} s JOIN {owner_table} o ON o.id = s.{owner_column} "
                         "WHERE lower(o.email) = lower(%s) ORDER BY s.created_at DESC LIMIT 1", (email,))
    assert rows, f"no {table} row exists for {email}"
    return rows[0]["token_hash"]


def session_seconds_left(backend, table: str, token_hash: str) -> float:
    rows = backend.query(f"SELECT EXTRACT(EPOCH FROM (expires_at - now())) AS left_seconds FROM {table} "
                         "WHERE token_hash = %s", (token_hash,))
    assert rows, f"the {table} row vanished"
    return float(rows[0]["left_seconds"])


def reset_session(backend, table: str, token_hash: str, assignments: str) -> None:
    backend.query(f"UPDATE {table} SET {assignments} WHERE token_hash = %s RETURNING token_hash", (token_hash,))


def test_reader_session_ends_90_days_after_most_recent_request_and_author_session_2_hours_after_capped_at_12_hours_from_sign_in(backend):
    """A reader session ends 90 days past its latest request, an author session 2 hours past but within 12 hours; ended tokens are refused or served as a visitor.

    cov: C-CF-21, C-CF-22, C-CF-23, C-CF-24, C-CF-25, C-CF-26
    """
    day, hour, slack = 24 * 3600, 3600, 600
    probe = register_reader()
    reader_hash = newest_session_hash(backend, "reader_sessions", "reader_id", "readers", probe["email"])
    assert abs(session_seconds_left(backend, "reader_sessions", reader_hash) - 90 * day) < slack, "a new reader session does not end 90 days out"
    reset_session(backend, "reader_sessions", reader_hash, "expires_at = now() + interval '1 hour'")
    with api_client(probe["token"]) as session:
        assert session.get("/me").status_code == 200, "a live reader session was refused"
    assert abs(session_seconds_left(backend, "reader_sessions", reader_hash) - 90 * day) < slack, "a request did not move the reader session end to 90 days later"
    reset_session(backend, "reader_sessions", reader_hash, "expires_at = now() - interval '1 second'")
    with api_client(probe["token"]) as session:
        assert session.get("/me").status_code in (401, 403), "a reader session past expires_at still works"
        listed = session.get("/volumes")
        assert listed.status_code == 200, f"an open endpoint refused an ended reader session. {describe(listed)}"

    token = studio_login(AUTHOR2_EMAIL)
    author_hash = newest_session_hash(backend, "studio_sessions", "member_id", "members", AUTHOR2_EMAIL)
    assert abs(session_seconds_left(backend, "studio_sessions", author_hash) - 2 * hour) < slack, "a new author session does not end 2 hours out"
    reset_session(backend, "studio_sessions", author_hash, "expires_at = now() + interval '10 minutes'")
    with api_client(token) as studio:
        assert studio.get("/studio/volumes").status_code == 200, "a live author session was refused"
    assert abs(session_seconds_left(backend, "studio_sessions", author_hash) - 2 * hour) < slack, "a request did not move the author session end to 2 hours later"
    reset_session(backend, "studio_sessions", author_hash,
                  "created_at = now() - interval '11 hours 30 minutes', expires_at = now() + interval '10 minutes'")
    with api_client(token) as studio:
        assert studio.get("/studio/volumes").status_code == 200, "a live author session was refused"
    assert session_seconds_left(backend, "studio_sessions", author_hash) <= 30 * 60 + 60, "an author session runs past 12 hours from sign-in"
    reset_session(backend, "studio_sessions", author_hash, "expires_at = now() - interval '1 second'")
    with api_client(token) as studio:
        assert studio.get("/studio/volumes").status_code in (401, 403), "an author session past expires_at still works"


def tip_status(token_value: str, reader_token_value: str | None) -> str:
    response = claim(token_value, reader_token_value)
    assert response.status_code == 200, describe(response)
    return response.json()["status"]


def entitled_reader(settled: int = 600) -> dict:
    probe = register_reader()
    token_value = return_token()
    assert tip_status(token_value, probe["token"]) == "pending"
    data = tip_data(settled, email=probe_email(), token=token_value)
    assert deliver(event_body("tip.received", data)).status_code == 200
    probe["tip_id"] = data["tip_id"]
    probe["return_token"] = token_value
    return probe


def test_return_token_is_issued_for_24_hours_and_claimed_by_one_reader_only():
    """A return token lasts 24 hours and is claimed by the first reader only.

    cov: C-CF-230, C-CF-231, C-CF-232
    """
    with api_client() as anon:
        issued = anon.post("/tips/return-tokens")
    assert issued.status_code in (200, 201), describe(issued)
    lifetime = (parse_instant(issued.json()["expires_at"]) - utc_now()).total_seconds()
    assert 24 * 3600 - 180 <= lifetime <= 24 * 3600 + 60, f"return token lifetime {lifetime}s"
    first, second = register_reader(), register_reader()
    token_value = issued.json()["token"]
    assert claim(token_value, first["token"]).status_code == 200
    stolen = claim(token_value, second["token"])
    assert 400 <= stolen.status_code < 500, describe(stolen)
    assert claim(token_value, first["token"]).status_code == 200


def test_concurrent_return_token_claims_let_exactly_one_reader_succeed():
    """Two readers claiming one return token at the same moment: exactly one claim succeeds.

    cov: C-DM-62
    """
    for _ in range(3):
        token_value = return_token()
        readers = [register_reader(), register_reader()]
        results = run_together([lambda r=r: claim(token_value, r["token"]) for r in readers])
        codes = sorted(r.status_code for r in results)
        assert codes[0] == 200 and 400 <= codes[1] < 500, [describe(r) for r in results]


def test_tip_return_statuses_sign_in_required_granted_below_threshold_pending_or_rejected_unknown_or_expired_token(backend):
    """The return call answers sign_in_required, pending, granted or below_threshold, and rejects unknown or expired tokens.

    cov: C-CF-233, C-CF-234, C-CF-235, C-CF-236, C-CF-240, C-CF-241
    """
    probe = register_reader()
    expiring = return_token()
    backend.query("UPDATE return_tokens SET expires_at = now() - interval '1 second' "
                  "WHERE claimed_by_reader_id IS NULL AND issued_at >= now() - interval '5 seconds' RETURNING issued_at")
    expired = claim(expiring, probe["token"])
    assert 400 <= expired.status_code < 500, f"an expired token was accepted. {describe(expired)}"
    unknown = claim("not-a-real-token-" + token_hex(), probe["token"])
    assert 400 <= unknown.status_code < 500, describe(unknown)
    granted_token = return_token()
    assert tip_status(granted_token, None) == "sign_in_required"
    assert tip_status(granted_token, probe["token"]) == "pending"
    assert deliver(event_body("tip.received", tip_data(600, token=granted_token))).status_code == 200
    assert wait_for(lambda: tip_status(granted_token, probe["token"]) == "granted"), "status never became granted"
    small_token = return_token()
    assert deliver(event_body("tip.received", tip_data(300, token=small_token))).status_code == 200
    other = register_reader()
    assert wait_for(lambda: tip_status(small_token, other["token"]) == "below_threshold")


def test_return_page_visit_without_a_verified_tip_grants_no_early_access(site):
    """Claiming a token and visiting the thank-you page grants nothing without a verified tip.

    cov: C-CF-243, C-DC-24
    """
    probe = register_reader()
    token_value = return_token()
    assert tip_status(token_value, probe["token"]) == "pending"
    assert site.get(f"/support/return?token={token_value}").status_code == 200
    unsigned = event_body("tip.received", tip_data(900, token=token_value))
    assert deliver(unsigned, signature="t=1,v1=" + "0" * 64).status_code == 401
    assert active_kinds(probe["token"]) == set()
    assert manifest(1, 4, probe["token"]).status_code == 404
    assert tip_status(token_value, probe["token"]) == "pending"


def test_tipbox_webhook_signed_with_the_seeded_secret_over_timestamp_raw_body_header_is_accepted_by_signature_never_by_bearer_token(backend, author_token):
    """A notification signed with the seeded secret over `<t>.<raw body>` is accepted; a bearer token never substitutes.

    cov: C-CF-244, C-CF-245, C-CF-246, C-CF-247, C-DC-18
    """
    data = tip_data(450)
    body = event_body("tip.received", data)
    stamp = now_unix()
    digest = hmac.new(TIPBOX_SECRET.encode(), f"{stamp}.".encode() + body, hashlib.sha256).hexdigest()
    accepted = deliver(body, signature=f"t={stamp},v1={digest}")
    assert accepted.status_code == 200, describe(accepted)
    assert wait_for(lambda: backend.count("tips", external_id=data["tip_id"]) == 1)
    other = event_body("tip.received", tip_data(450))
    forged = httpx.post(f"{appclient.api_base()}/webhooks/tipbox", content=other,
                        headers={"Content-Type": "application/json", "Authorization": f"Bearer {author_token}",
                                 SIGNATURE_HEADER: f"t={now_unix()},v1={'ab' * 32}"}, timeout=appclient.TIMEOUT)
    assert forged.status_code == 401, describe(forged)
    tokenless = httpx.post(f"{appclient.api_base()}/webhooks/tipbox", content=other,
                           headers={"Content-Type": "application/json", "Authorization": f"Bearer {author_token}"},
                           timeout=appclient.TIMEOUT)
    assert tokenless.status_code == 401, describe(tokenless)


def test_tipbox_notifications_with_tampered_body_bytes_reserialised_json_or_timestamp_outside_300_seconds_are_refused_401_recorded_unverified(backend):
    """Tampered bytes, re-serialised JSON and stale or future timestamps answer 401, are recorded unverified, and change nothing.

    cov: C-OV-06, C-CF-248, C-CF-249, C-CF-250, C-CF-251, C-CF-252, C-DC-25, C-DC-26
    """
    before = backend.count("webhook_events", signature_verified=False)
    data = tip_data(900)
    payload = {"id": "evt_" + token_hex(), "type": "tip.received", "created": now_unix(), "data": data}
    signed_bytes = json.dumps(payload, separators=(", ", ": ")).encode()
    signature = sign(signed_bytes)
    spaced = signed_bytes.replace(b": ", b":  ", 1)
    refused = [
        deliver(spaced, signature=signature),
        deliver(json.dumps(payload, indent=2).encode(), signature=signature),
        deliver(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(), signature=signature),
        deliver(signed_bytes, signature=sign(signed_bytes, stamp=now_unix() - SIGNATURE_WINDOW_SECONDS - 5)),
        deliver(signed_bytes, signature=sign(signed_bytes, stamp=now_unix() + SIGNATURE_WINDOW_SECONDS + 5)),
    ]
    for response in refused:
        assert response.status_code == 401, describe(response)
    assert backend.count("webhook_events", signature_verified=False) >= before + len(refused)
    assert backend.count("tips", external_id=data["tip_id"]) == 0, "a refused notification recorded a tip"


def test_verified_notifications_record_once_ignoring_repeated_event_ids_and_unknown_types_counting_the_tip_once(backend):
    """A repeated event id answers 200 and does nothing twice; an unknown type answers 200 and changes nothing.

    cov: C-OV-13, C-CF-253, C-CF-254, C-CF-256, C-CF-257, C-CF-258, C-DM-56
    """
    data = tip_data(700)
    body = event_body("tip.received", data, event_id="evt_" + token_hex())
    event_id = json.loads(body)["id"]
    for _ in range(3):
        assert deliver(body).status_code == 200
    assert wait_for(lambda: backend.count("tips", external_id=data["tip_id"]) == 1)
    assert backend.count("webhook_events", external_id=event_id, signature_verified=True) == 1
    replay = event_body("tip.received", data)
    assert deliver(replay).status_code == 200
    assert backend.count("tips", external_id=data["tip_id"]) == 1, "a second delivery of one tip counted twice"
    odd = tip_data(1200)
    assert deliver(event_body("tip.updated", odd)).status_code == 200
    assert backend.count("tips", external_id=odd["tip_id"]) == 0, "an unknown notification type changed state"


def test_tip_received_notification_stores_amount_currency_settled_amount_rate_exactly_as_received(author):
    """A tip keeps its original amount and currency and its settled amount and rate exactly as received.

    cov: C-CF-259, C-CF-260, C-CF-261, C-CF-262, C-CF-263, C-CF-264
    """
    data = tip_data(5100, amount=4600, currency="eur", rate="1.087500", message="for the next chapter")
    assert deliver(event_body("tip.received", data)).status_code == 200
    row = wait_for(lambda: tip_row(author, data["tip_id"]))
    assert row, "the tip never appeared in the supporter list"
    assert row["amount"] == 4600 and row["currency"] == "eur", row
    assert row["settled_amount"] == 5100, f"the settled amount was recomputed: {row}"
    assert str(row["rate"]) == "1.087500", row
    assert row["message"] == data["message"] and row["supporter_email"] == data["supporter_email"], row
    assert row["source"] == "tipbox" and row["tip_id"] == data["tip_id"] and row["state"] == "received", row


def test_concurrent_duplicate_tip_deliveries_store_one_tip_row(backend):
    """Simultaneous deliveries of one Tipbox tip_id store exactly one tip row and at most one grant per kind.

    cov: C-CF-265, C-CF-266, C-DM-55, C-DC-27
    """
    probe = register_reader()
    token_value = return_token()
    assert tip_status(token_value, probe["token"]) == "pending"
    data = tip_data(2500, token=token_value)
    bodies = [event_body("tip.received", data) for _ in range(6)]
    responses = run_together([lambda b=b: deliver(b) for b in bodies])
    assert all(r.status_code == 200 for r in responses), [describe(r) for r in responses]
    assert wait_for(lambda: "credits" in active_kinds(probe["token"])), "the concurrent tip never granted"
    assert backend.count("tips", external_id=data["tip_id"]) == 1, "concurrent deliveries stored more than one tip row"
    grants = backend.query("SELECT e.kind, count(*) AS n FROM entitlements e JOIN tips t ON t.id = e.tip_id "
                           "WHERE t.external_id = %s GROUP BY e.kind", (data["tip_id"],))
    assert grants and all(int(g["n"]) == 1 for g in grants), grants


def test_tip_matching_by_claimed_token_or_address_needs_author_confirmation_and_unmatched_tips_record_none(author):
    """Tips match by claimed token before or after arrival, by address only after an author confirms, else to nobody.

    cov: C-CF-267, C-CF-268, C-CF-269, C-CF-270, C-CF-271, C-CF-272, C-CF-796, C-CF-797
    """
    late = register_reader()
    token_value = return_token()
    data = tip_data(600, token=token_value)
    assert deliver(event_body("tip.received", data)).status_code == 200
    assert wait_for(lambda: tip_row(author, data["tip_id"]))
    assert tip_status(token_value, late["token"]) in ("granted", "pending")
    assert wait_for(lambda: "early_access" in active_kinds(late["token"])), "a claim after the tip did not match"
    token_row = tip_row(author, data["tip_id"])
    assert token_row["match_method"] == "token" and token_row["matched_reader_email"] == late["email"], token_row
    by_address = register_reader()
    address_data = tip_data(600, email=by_address["email"].upper(), token=None)
    assert deliver(event_body("tip.received", address_data)).status_code == 200
    row = wait_for(lambda: tip_row(author, address_data["tip_id"]))
    assert row["match_method"] == "address" and row["entitlement"] == "awaiting_confirmation", row
    assert active_kinds(by_address["token"]) == set(), "an address match granted before confirmation"
    confirmed = author.post(f"/studio/tips/{row['id']}/confirm-match")
    assert confirmed.status_code == 200, describe(confirmed)
    assert wait_for(lambda: "early_access" in active_kinds(by_address["token"]))
    assert tip_row(author, address_data["tip_id"])["entitlement"] == "granted"
    stranger = tip_data(600, token=None)
    assert deliver(event_body("tip.received", stranger)).status_code == 200
    none_row = wait_for(lambda: tip_row(author, stranger["tip_id"]))
    assert none_row["match_method"] == "none" and none_row["entitlement"] == "unmatched", none_row
    for tip in (token_row, none_row):
        refused = author.post(f"/studio/tips/{tip['id']}/confirm-match")
        assert 400 <= refused.status_code < 500, describe(refused)


def add_months(moment, months: int):
    year = moment.year + (moment.month - 1 + months) // 12
    month = (moment.month - 1 + months) % 12 + 1
    last = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return moment.replace(year=year, month=month, day=min(moment.day, last[month - 1]))


def test_tip_thresholds_grant_early_access_at_500_for_twelve_calendar_months_and_credits_at_2000_each_kind_at_most_once():
    """Below 500 grants nothing, 500 grants early access for 12 calendar months, 2000 adds credits, each kind once.

    cov: C-CF-273, C-CF-274, C-CF-275, C-CF-276, C-DM-63
    """
    below = entitled_reader(499)
    assert wait_for(lambda: tip_status(below["return_token"], below["token"]) == "below_threshold")
    assert active_kinds(below["token"]) == set()
    exact = entitled_reader(500)
    assert wait_for(lambda: "early_access" in active_kinds(exact["token"]))
    grant = next(e for e in entitlements(exact["token"]) if e["kind"] == "early_access")
    granted_at, expires_at = parse_instant(grant["granted_at"]), parse_instant(grant["expires_at"])
    assert expires_at.date() == add_months(granted_at, 12).date(), (grant["granted_at"], grant["expires_at"])
    assert "credits" not in active_kinds(exact["token"])
    large = entitled_reader(2000)
    assert wait_for(lambda: active_kinds(large["token"]) >= {"early_access", "credits"})
    credits = next(e for e in entitlements(large["token"]) if e["kind"] == "credits")
    assert credits["expires_at"] is None, credits
    again = tip_data(2000, token=large["return_token"], tip_id=large["tip_id"])
    assert deliver(event_body("tip.received", again)).status_code == 200
    settle(2.0)
    kinds = [e["kind"] for e in entitlements(large["token"])]
    assert kinds.count("early_access") == 1 and kinds.count("credits") == 1, kinds


def test_refund_or_dispute_revokes_early_access_on_the_next_request_keeping_read_progress_unless_another_qualifying_tip_stands_even_arriving_before_the_tip(author):
    """Refunds and disputes revoke from the next request, keep progress, spare a second qualifying tip, and may arrive first.

    cov: C-OV-14, C-CF-277, C-CF-278, C-CF-279, C-CF-280, C-CF-281, C-CF-282, C-CF-283, C-CF-284, C-CF-286, C-CF-287, C-CF-288
    """
    refunded = entitled_reader(600)
    assert wait_for(lambda: manifest(1, 4, refunded["token"]).status_code == 200)
    doc = {"last_chapter": {"volume": 1, "chapter": 4}, "last_chapter_at": "2026-09-10T10:00:00Z",
           "chapters": [{"volume": 1, "chapter": 4, "fraction": 0.5, "last_panel": 2}]}
    with api_client(refunded["token"]) as session:
        assert session.put("/me/progress", json=doc).status_code == 200
    assert deliver(event_body("tip.refunded", {"tip_id": refunded["tip_id"]})).status_code == 200
    assert wait_for(lambda: manifest(1, 4, refunded["token"]).status_code == 404), "a refund did not revoke access"
    revoked = [e for e in entitlements(refunded["token"]) if e["kind"] == "early_access"]
    assert revoked and revoked[0]["active"] is False and revoked[0]["revoked_at"], revoked
    row = tip_row(author, refunded["tip_id"])
    assert row["state"] == "refunded" and row["entitlement"] == "revoked", row
    with api_client(refunded["token"]) as session:
        chapters = session.get("/me/progress").json()["chapters"]
    assert any(int(c["chapter"]) == 4 and abs(float(c["fraction"]) - 0.5) < 1e-9 for c in chapters), chapters
    disputed = entitled_reader(600)
    assert wait_for(lambda: manifest(1, 4, disputed["token"]).status_code == 200)
    assert deliver(event_body("tip.disputed", {"tip_id": disputed["tip_id"]})).status_code == 200
    assert wait_for(lambda: manifest(1, 4, disputed["token"]).status_code == 404), "a dispute did not revoke access"
    assert tip_row(author, disputed["tip_id"])["state"] == "disputed"
    double = entitled_reader(600)
    second_token = return_token()
    assert tip_status(second_token, double["token"]) == "pending"
    assert deliver(event_body("tip.received", tip_data(800, token=second_token))).status_code == 200
    assert wait_for(lambda: tip_status(second_token, double["token"]) == "granted")
    assert deliver(event_body("tip.refunded", {"tip_id": double["tip_id"]})).status_code == 200
    settle(3.0)
    assert manifest(1, 4, double["token"]).status_code == 200, "another qualifying tip should keep early access"
    early = register_reader()
    orphan = "tbx_probe_" + token_hex()
    assert deliver(event_body("tip.refunded", {"tip_id": orphan})).status_code == 200
    first_row = wait_for(lambda: tip_row(author, orphan))
    assert first_row and first_row["state"] == "refunded", first_row
    late_token = return_token()
    assert tip_status(late_token, early["token"]) == "pending"
    assert deliver(event_body("tip.received", tip_data(900, token=late_token, tip_id=orphan))).status_code == 200
    filled = wait_for(lambda: (tip_row(author, orphan) or {}).get("settled_amount") == 900)
    assert filled, tip_row(author, orphan)
    assert tip_row(author, orphan)["state"] == "refunded"
    assert active_kinds(early["token"]) == set(), "a tip refunded before arrival granted access"


def test_verified_tip_notification_unlocks_scheduled_chapter_early_for_the_tipper():
    """A verified tip of 500 or more lets its tipper read scheduled chapter 4 within 30 seconds, and nobody else.

    cov: C-OV-03, C-CF-255
    """
    tipper = entitled_reader(650)
    assert wait_for(lambda: manifest(1, 4, tipper["token"]).status_code == 200, EFFECT_DEADLINE_SECONDS), (
        "the tipper could not read chapter 4 within 30 seconds of the verified notification")
    body = manifest(1, 4, tipper["token"]).json()
    assert body["title"] == CHAPTER_TITLES[4][0] and layer_urls(body)
    assert fetch_absolute(layer_urls(body)[0]).status_code == 200
    bystander = register_reader()
    assert manifest(1, 4, bystander["token"]).status_code == 404
    assert manifest(1, 4).status_code == 404
    listed = {int(c["number"]): c for c in volumes(tipper["token"])[0]["chapters"]}
    assert listed[4]["locked"] is False


def test_studio_tip_list_shows_seeded_tips_with_supporter_address_newest_first_by_cursor_with_entitlement_and_state(author):
    """The supporter list shows seeded tips with addresses, newest first, paged by cursor, with entitlement and state.

    cov: C-OV-10, C-RL-16, C-CF-289, C-CF-787, C-CF-788, C-CF-789, C-CF-794, C-CF-795, C-DM-129, C-DM-130, C-DC-19
    """
    first_page = tips_page(author)
    assert len(first_page["items"]) <= 50 and "next_cursor" in first_page
    capped = author.get("/studio/tips", params={"limit": 500})
    assert capped.status_code in (200, 400, 422), describe(capped)
    if capped.status_code == 200:
        assert len(capped.json()["items"]) <= 200
    rows = all_tips(author)
    moments = [parse_instant(r["received_at"]) for r in rows]
    assert moments == sorted(moments, reverse=True), "tips are not newest first"
    single = tips_page(author, limit=1)
    assert len(single["items"]) == 1 and single["next_cursor"]
    following = tips_page(author, limit=1, cursor=single["next_cursor"])
    assert following["items"][0]["id"] != single["items"][0]["id"]
    for row in rows:
        assert set(row) >= set(TIP_ROW_FIELDS), sorted(row)
        assert row["entitlement"] in TIP_ENTITLEMENT_VALUES and row["state"] in TIP_STATE_VALUES, row
    seeded = {r["tip_id"]: r for r in rows if r["tip_id"] in (SEED_TIP_ONE, SEED_TIP_TWO)}
    one, two = seeded[SEED_TIP_ONE], seeded[SEED_TIP_TWO]
    assert (one["supporter_email"], one["amount"], one["settled_amount"], str(one["rate"]), one["message"]) == (
        READER_EMAIL, 800, 800, "1.000000", SEED_TIP_ONE_MESSAGE), one
    assert one["match_method"] == "token" and one["state"] == "received" and one["entitlement"] == "granted", one
    assert (two["supporter_email"], two["amount"], two["settled_amount"], two["message"]) == (
        FRIEND_EMAIL, 300, 300, SEED_TIP_TWO_MESSAGE), two
    assert two["match_method"] == "none" and two["state"] == "received", two
    assert one["currency"] == two["currency"] == "usd"
    gap = parse_instant(two["received_at"]) - parse_instant(one["received_at"])
    assert 23 * 3600 <= gap.total_seconds() <= 25 * 3600, gap


def month_row(totals: dict, month: str) -> dict:
    return next((m for m in totals["by_month"] if m["month"] == month), {"count": 0, "total": 0})


def source_row(totals: dict, source: str) -> dict:
    return next((s for s in totals["by_source"] if s["source"] == source), {"count": 0, "total": 0})


def test_manual_tips_validate_amount_received_at_reason_and_count_in_utc_month_and_source_totals_excluding_refunds_granting_nothing(author):
    """Manual tips validate their fields, count in UTC month and source totals, grant nothing; refunds leave the totals.

    cov: C-CF-790, C-CF-791, C-CF-792, C-CF-793, C-CF-798, C-CF-799, C-CF-800, C-CF-801, C-CF-802, C-CF-803, C-CN-08
    """
    month = utc_now().strftime("%Y-%m")
    before = author.get("/studio/tips/totals").json()
    recorded = author.post("/studio/tips", json={"amount": 1500, "received_at": iso_in(-60), "reason": "cash at a signing"})
    assert recorded.status_code in (200, 201), describe(recorded)
    tip = recorded.json()
    assert tip["source"] == "manual" and tip["tip_id"] is None, tip
    after = author.get("/studio/tips/totals").json()
    assert int(month_row(after, month)["total"]) == int(month_row(before, month)["total"]) + 1500
    assert int(source_row(after, "manual")["count"]) == int(source_row(before, "manual")["count"]) + 1
    assert all(re.fullmatch(r"\d{4}-\d{2}", m["month"]) for m in after["by_month"]), after["by_month"]
    for body, field in (({"amount": 0, "received_at": iso_in(-60), "reason": "x"}, "amount"),
                        ({"amount": 12.5, "received_at": iso_in(-60), "reason": "x"}, "amount"),
                        ({"amount": -4, "received_at": iso_in(-60), "reason": "x"}, "amount"),
                        ({"amount": 100, "reason": "x"}, "received_at"),
                        ({"amount": 100, "received_at": "yesterday", "reason": "x"}, "received_at"),
                        ({"amount": 100, "received_at": iso_in(-60)}, "reason")):
        assert_rejected(author.post("/studio/tips", json=body), field=field)
    assert author.get("/studio/tips/totals").json() == after, "a rejected manual tip changed the totals"
    data = tip_data(800, token=None)
    assert deliver(event_body("tip.received", data)).status_code == 200
    assert wait_for(lambda: tip_row(author, data["tip_id"]))
    with_tip = author.get("/studio/tips/totals").json()
    assert deliver(event_body("tip.refunded", {"tip_id": data["tip_id"]})).status_code == 200
    assert wait_for(lambda: tip_row(author, data["tip_id"])["state"] == "refunded")
    refunded = author.get("/studio/tips/totals").json()
    assert int(month_row(refunded, month)["total"]) == int(month_row(with_tip, month)["total"]) - 800


def test_studio_overview_returns_four_cards_alerts_and_revocations(author):
    """The overview returns the next drop, unready work, support and reading cards beside alerts and revocations.

    cov: C-CF-285, C-CF-804, C-CF-805, C-CF-806, C-CF-807, C-CF-808, C-CF-809
    """
    response = author.get("/studio/overview")
    assert response.status_code == 200, describe(response)
    body = response.json()
    for key in ("next_drop", "unready", "support", "reading", "alerts", "revocations"):
        assert key in body, f"overview lacks {key}"
    text = json.dumps(body["next_drop"])
    assert CHAPTER_TITLES[4][0] in text or '"number": 4' in text, body["next_drop"]
    assert "6" in json.dumps(body["unready"]) or CHAPTER_TITLES[6][0] in json.dumps(body["unready"]), body["unready"]
    assert isinstance(body["revocations"], list) and body["revocations"], "refunds and disputes should appear as revocations"
    reading = json.dumps(body["reading"])
    assert "open" in reading, body["reading"]


def field_starts(response: httpx.Response, prefix: str) -> None:
    assert 400 <= response.status_code < 500, f"expected a rejection naming {prefix}. {describe(response)}"
    error = error_of(response)
    assert str(error.get("field") or "").startswith(prefix), f"rejection names {error.get('field')!r}, not {prefix}"


def layers_by_role(author_session, board_id: str, panel_number: int = 1) -> dict:
    panel = next(p for p in board_detail(author_session, board_id)["panels"] if int(p["number"]) == panel_number)
    return {layer["role"]: layer for layer in panel["layers"]}


def objects_under(store, order: int, number: int) -> list:
    return store.list(f"chapters/{order}/{number}/")


def test_author_creates_volume_draft_chapter_board_and_cover_with_next_order_and_numbers_rejecting_bad_labels_titles_descriptions(author, store, backend):
    """Authors create volumes, draft chapters, boards and covers with next numbers, rejecting out-of-range text.

    cov: C-OV-09, C-CF-631, C-CF-632, C-CF-633, C-CF-634, C-CF-635, C-CF-636, C-CF-637, C-CF-638, C-CF-639, C-CF-640, C-CF-646, C-CF-647, C-CF-681
    """
    listed = author.get("/studio/volumes")
    assert listed.status_code == 200, describe(listed)
    highest = max(int(v["order"]) for v in listed.json())
    count = backend.count("volumes")
    field_starts(author.post("/studio/volumes", json={"label": ""}), "label")
    field_starts(author.post("/studio/volumes", json={"label": "L" * 41}), "label")
    assert backend.count("volumes") == count
    volume = author.post("/studio/volumes", json={"label": "V" * 40})
    assert volume.status_code in (200, 201) and int(volume.json()["order"]) == highest + 1, describe(volume)
    assert studio_volume(author, 1)["label"] == VOLUME_ONE_LABEL
    volume_id = volume.json()["id"]
    long_title = {"titles": {"en": "t" * 61, "fr": "t"}, "descriptions": {"en": "d", "fr": "d"}}
    field_starts(author.post(f"/studio/volumes/{volume_id}/chapters", json=long_title), "titles")
    long_desc = {"titles": {"en": "t", "fr": "t"}, "descriptions": {"en": "d" * 201, "fr": "d"}}
    field_starts(author.post(f"/studio/volumes/{volume_id}/chapters", json=long_desc), "descriptions")
    empty_title = {"titles": {"en": "", "fr": "t"}, "descriptions": {"en": "d", "fr": "d"}}
    field_starts(author.post(f"/studio/volumes/{volume_id}/chapters", json=empty_title), "titles")
    assert studio_chapters(author, volume_id) == []
    first, second = new_chapter(author, volume_id), new_chapter(author, volume_id, en="second probe", fr="deuxieme sonde")
    assert (int(first["number"]), int(second["number"])) == (1, 2)
    assert first["state"] == "draft" and first["titles"] == {"en": "probe chapter", "fr": "chapitre sonde"}, first
    boards = [new_board(author, first["id"]), new_board(author, first["id"])]
    assert [int(b["number"]) for b in boards] == [1, 2]
    stored = store_cover(author, first["id"])
    assert stored.status_code in (200, 201), describe(stored)
    assert studio_chapter(author, first["id"])["has_cover"] is True
    order = int(volume.json()["order"])
    covers = [k for k in store.list(f"covers/{order}/1/") if re.fullmatch(rf"covers/{order}/1/[0-9a-f]{{64}}\.png", k)]
    assert len(covers) == 1, store.list(f"covers/{order}/1/")


def test_studio_chapter_list_rows_carry_state_release_boards_ready_counting_panels_layers_descriptions_stored_images_and_image_bytes(author, backend):
    """Chapter rows carry state, release, boards ready over total and image bytes; readiness counts panels, layers, descriptions, images.

    cov: C-CF-641, C-CF-642, C-CF-643, C-CF-644, C-CF-645
    """
    built = build_chapter(author, ready=False)
    volume_id = built["volume"]["id"]
    row = next(r for r in studio_chapters(author, volume_id) if r["id"] == built["chapter"]["id"])
    assert (int(row["boards_ready"]), int(row["boards_total"])) == (1, 1), row
    stored_bytes = backend.query("SELECT coalesce(sum(li.byte_length), 0) AS n FROM layer_images li JOIN layers l "
                                 "ON l.id = li.layer_id JOIN panels p ON p.id = l.panel_id JOIN boards b ON "
                                 "b.id = p.board_id WHERE b.chapter_id = %s", (row["id"],))[0]["n"]
    assert int(row["image_bytes"]) >= int(stored_bytes) > 0, (row["image_bytes"], stored_bytes)
    empty = new_board(author, row["id"])
    undescribed = new_board(author, row["id"])
    number = built["number"]
    imported = upload(author, undescribed["id"], [(f"c{number}b{undescribed['number']}p1-back.png", make_png(), "image/png")])
    assert imported.status_code in (200, 201), describe(imported)
    row = next(r for r in studio_chapters(author, volume_id) if r["id"] == built["chapter"]["id"])
    assert (int(row["boards_ready"]), int(row["boards_total"])) == (1, 3), f"empty or undescribed boards counted ready: {row}"
    assert empty["number"] and row["state"] == "draft"
    assert set(row) >= {"titles", "state", "release_at", "published_at"}
    numbers = [int(r["number"]) for r in studio_chapters(author, studio_volume(author, 1)["id"])]
    assert numbers == sorted(numbers)


def test_author_imports_layered_panel_artwork_files_creating_panels_and_replacing_roles_keeping_layer_properties_changing_the_content_tag(author):
    """Importing files creates panels and layers; re-importing a role replaces its image, keeps its properties, changes the content tag.

    cov: C-RL-15, C-CF-648, C-CF-649, C-CF-661, C-CF-683, C-CF-684
    """
    volume = new_volume(author)
    chapter = new_chapter(author, volume["id"])
    board = new_board(author, chapter["id"])
    n, b = chapter["number"], board["number"]
    response = upload(author, board["id"], [(f"c{n}b{b}p1-back.png", make_png(rgb=(1, 2, 3)), "image/png"),
                                            (f"c{n}b{b}p1-stage.png", make_png(rgb=(4, 5, 6)), "image/png"),
                                            (f"c{n}b{b}p2-back.png", make_png(rgb=(7, 8, 9)), "image/png")])
    assert response.status_code in (200, 201), describe(response)
    assert set(response.json()) >= {"panels_created", "layers"}
    detail = board_detail(author, board["id"])
    assert sorted(int(p["number"]) for p in detail["panels"]) == [1, 2]
    stage = layers_by_role(author, board["id"])["stage"]
    tuned = author.patch(f"/studio/layers/{stage['id']}", json={"version": stage["version"], "depth": 3, "offset_x": 1.5,
                                                               "scale": 1.25, "opacity": 0.5})
    assert tuned.status_code == 200, describe(tuned)
    tag_before = studio_chapter(author, chapter["id"])["content_tag"]
    replaced = upload(author, board["id"], [(f"c{n}b{b}p1-stage.png", make_png(rgb=(200, 10, 10)), "image/png")])
    assert replaced.status_code in (200, 201), describe(replaced)
    after = layers_by_role(author, board["id"])["stage"]
    assert after["id"] == stage["id"], "re-importing a role created a new layer"
    assert (float(after["depth"]), float(after["offset_x"]), float(after["scale"]), float(after["opacity"]),
            int(after["draw_order"])) == (3.0, 1.5, 1.25, 0.5, int(stage["draw_order"])), after
    tag_after = studio_chapter(author, chapter["id"])["content_tag"]
    assert tag_after != tag_before, "replacing an image kept the content tag"
    panel = next(p for p in board_detail(author, board["id"])["panels"] if int(p["number"]) == 1)
    described = author.patch(f"/studio/panels/{panel['id']}", json={"version": panel["version"],
                                                                     "descriptions": {"en": "x", "fr": "y"}})
    assert described.status_code == 200
    assert studio_chapter(author, chapter["id"])["content_tag"] == tag_after, "a text edit changed the content tag"


def test_layer_import_rejections_for_bad_identifier_characters_duplicate_roles_unpaired_sprites_missing_locales_frame_table_fields_non_images_or_file_limits_leave_nothing(author, store):
    """Bad identifiers, duplicate roles, unpaired sprites, missing locales, bad frame tables, non-images and oversize imports leave nothing.

    cov: C-CF-650, C-CF-651, C-CF-652, C-CF-653, C-CF-654, C-CF-655, C-CF-656, C-CF-657, C-CF-658, C-CF-659, C-CF-660, C-CF-662, C-CF-663, C-CF-664, C-CF-667, C-CF-668, C-CF-669, C-CF-670, C-CF-671, C-CF-672, C-CF-673, C-CF-674, C-CF-675, C-TR-25
    """
    volume = new_volume(author)
    chapter = new_chapter(author, volume["id"])
    board = new_board(author, chapter["id"])
    n, b, order = chapter["number"], board["number"], int(volume["order"])
    good = (f"c{n}b{b}p1-back.png", make_png(), "image/png")
    broken_table = json.loads(frame_table())
    broken_table.pop("clips")
    cases = [
        ([good, (f"c{n}b{b}p1-Stage.png", make_png(), "image/png")], "S"),
        ([good, (f"c{n}b{b}p1-bad_name.png", make_png(), "image/png")], "_"),
        ([(f"c0{n}b{b}p1-back.png", make_png(), "image/png")], None),
        ([(f"c{n + 7}b{b}p1-back.png", make_png(), "image/png")], None),
        ([(f"c{n}b{b}p1-" + "r" * 25 + ".png", make_png(), "image/png")], None),
        ([good, good], None),
        ([(f"c{n}b{b}p2-crowd-sprite.png", make_png(16, 8), "image/png")], None),
        ([(f"c{n}b{b}p2-crowd-sprite-data.json", frame_table(), "application/json")], None),
        ([(f"c{n}b{b}p2-crowd-sprite.png", make_png(16, 8), "image/png"),
          (f"c{n}b{b}p2-crowd-sprite-data.json", json.dumps(broken_table).encode(), "application/json")], None),
        ([(f"c{n}b{b}p3-sign-en.png", make_png(), "image/png")], None),
        ([good, (f"c{n}b{b}p4-back.png", b"this is plain text, not a picture", "image/png")], None),
    ]
    for files, character in cases:
        response = upload(author, board["id"], files)
        assert 400 <= response.status_code < 500, f"{[f[0] for f in files]} was accepted. {describe(response)}"
        error = error_of(response)
        assert error.get("file"), f"the rejection names no file. {describe(response)}"
        if character:
            assert character in error["message"], f"the rejection does not name {character!r}: {error['message']}"
        assert board_detail(author, board["id"])["panels"] == [], "a rejected import left panels behind"
        assert objects_under(store, order, n) == [], "a rejected import left objects in the bucket"
    too_many = [(f"c{n}b{b}p{(i % 99) + 1}-r{i}.png", make_png(2, 2), "image/png") for i in range(201)]
    assert 400 <= upload(author, board["id"], too_many).status_code < 500
    oversized = make_png(8, 8) + os.urandom(40 * 1024 * 1024 + 1024)
    assert 400 <= upload(author, board["id"], [(f"c{n}b{b}p1-back.png", oversized, "image/png")]).status_code < 500
    assert board_detail(author, board["id"])["panels"] == [] and objects_under(store, order, n) == []
    formats = upload(author, board["id"], [(f"c{n}b{b}p1-back.jpg", tiny_jpeg(), "image/jpeg"),
                                           (f"c{n}b{b}p2-back.webp", tiny_webp(), "image/webp"),
                                           (f"c{n}b{b}p3-back.png", make_png(), "image/png")])
    assert formats.status_code in (200, 201), f"PNG, WebP and JPEG bytes must be accepted. {describe(formats)}"


def test_imported_layer_image_is_stored_reencoded_in_bucket_at_content_hash_key(author, store, backend):
    """An imported image is re-encoded as PNG without metadata and stored in the bucket at its content-hash key.

    cov: C-CF-676, C-CF-677, C-CF-678, C-CN-16, C-DC-21
    """
    volume = new_volume(author)
    chapter = new_chapter(author, volume["id"])
    board = new_board(author, chapter["id"])
    n, b, order = chapter["number"], board["number"], int(volume["order"])
    marker = b"deku-metadata-marker-" + token_hex().encode()
    response = upload(author, board["id"], [(f"c{n}b{b}p1-back.png", make_png(10, 10, (9, 9, 9), text=marker), "image/png"),
                                            (f"c{n}b{b}p2-back.png", tiny_jpeg(), "image/png")])
    assert response.status_code in (200, 201), describe(response)
    preview = author.get(f"/studio/chapters/{chapter['id']}/manifest", params={"locale": "en"}).json()
    served = {l["identifier"]: l["image_url"] for bd in preview["boards"] for p in bd["panels"] for l in p["layers"]}
    for identifier in (f"c{n}b{b}p1-back", f"c{n}b{b}p2-back"):
        keys = [k for k in store.list(f"chapters/{order}/{n}/{identifier}/") if SHA_KEY_RE.match(k)]
        assert len(keys) == 1 and store.exists(keys[0]), f"{identifier} objects: {keys}"
        data = fetch_absolute(served[identifier]).content
        assert data[:8] == b"\x89PNG\r\n\x1a\n", f"{identifier} was not stored as PNG"
        assert keys[0] == f"chapters/{order}/{n}/{identifier}/{hashlib.sha256(data).hexdigest()}.png", keys[0]
        for chunk in (b"tEXt", b"iTXt", b"zTXt", b"eXIf", b"tIME"):
            assert chunk not in data, f"{identifier} kept a {chunk!r} metadata chunk"
        assert marker not in data
        rows = backend.query("SELECT object_key, byte_length FROM layer_images WHERE object_key = %s", (keys[0],))
        assert rows and int(rows[0]["byte_length"]) == len(data), rows


def test_imported_map_localised_and_sprite_layers_attach_displacement_keep_locale_segments_and_serve_frame_table_urls(author, store, backend):
    """Map layers attach as displacement sources, localised layers keep locale segments, sprites serve frame table URLs.

    cov: C-CF-209, C-CF-211, C-CF-665, C-CF-666, C-CF-679, C-CF-680
    """
    volume = new_volume(author)
    chapter = new_chapter(author, volume["id"])
    board = new_board(author, chapter["id"])
    n, b, order = chapter["number"], board["number"], int(volume["order"])
    orphan_map = upload(author, board["id"], [(f"c{n}b{b}p1-ghost-map.png", make_png(), "image/png")])
    assert 400 <= orphan_map.status_code < 500, describe(orphan_map)
    response = upload(author, board["id"], [
        (f"c{n}b{b}p1-stage.png", make_png(), "image/png"),
        (f"c{n}b{b}p1-stage-depth.png", make_png(rgb=(128, 128, 128)), "image/png"),
        (f"c{n}b{b}p1-sign-en.png", make_png(rgb=(1, 1, 1)), "image/png"),
        (f"c{n}b{b}p1-sign-fr.png", make_png(rgb=(2, 2, 2)), "image/png"),
        (f"c{n}b{b}p2-crowd-sprite.png", make_png(16, 8), "image/png"),
        (f"c{n}b{b}p2-crowd-sprite-data.json", frame_table(), "application/json"),
    ])
    assert response.status_code in (200, 201), describe(response)
    maps = backend.query("SELECT l.id, l.kind FROM layers l JOIN panels p ON p.id = l.panel_id WHERE p.board_id = %s "
                         "AND l.kind = 'map'", (board["id"],))
    assert len(maps) == 1, maps
    stage = backend.query("SELECT displacement_source_id FROM layers l JOIN panels p ON p.id = l.panel_id "
                          "WHERE p.board_id = %s AND l.role = 'stage'", (board["id"],))
    assert stage and stage[0]["displacement_source_id"] == maps[0]["id"], stage
    for locale in ("en", "fr"):
        keys = [k for k in store.list(f"chapters/{order}/{n}/c{n}b{b}p1-sign-{locale}/") if SHA_KEY_RE.match(k)]
        assert len(keys) == 1, f"the {locale} sign image is not stored under its locale segment"
    assert any(k.endswith(".json") for k in store.list(f"chapters/{order}/{n}/")), "the frame table was not stored"
    preview = author.get(f"/studio/chapters/{chapter['id']}/manifest", params={"locale": "en"}).json()
    layers = [l for bd in preview["boards"] for p in bd["panels"] for l in p["layers"]]
    sprite = next(l for l in layers if l["kind"] == "sprite")
    path = urlparse(sprite["frame_table_url"]).path
    assert path.startswith("/api/textures/v") and path.endswith(".json"), sprite["frame_table_url"]
    assert json.loads(fetch_absolute(sprite["frame_table_url"]).content) == json.loads(frame_table())
    assert all(l["frame_table_url"] is None for l in layers if l["kind"] != "sprite")


def test_layer_and_panel_edits_reject_out_of_range_depth_offset_scale_opacity_blend_draw_order_displacement_clip_loop_mode_description_duration_camera_values(author):
    """Layer and panel edits reject every out-of-range value by field and change nothing.

    cov: C-CF-685, C-CF-686, C-CF-687, C-CF-688, C-CF-689, C-CF-690, C-CF-691, C-CF-692, C-CF-693, C-CF-694, C-CF-695, C-CF-696, C-CF-697, C-CF-698, C-CF-699, C-CF-700, C-CF-701, C-CF-702
    """
    built = build_chapter(author, ready=False)
    layers = layers_by_role(author, built["board"]["id"])
    back, stage = layers["back"], layers["stage"]
    for field, value in (("depth", 10.5), ("depth", -11), ("offset_x", 11), ("offset_y", -10.5), ("scale", 0.05),
                         ("scale", 4.5), ("opacity", -0.1), ("opacity", 1.1), ("blend", "multiply"), ("draw_order", 64),
                         ("draw_order", -1), ("draw_order", int(stage["draw_order"])), ("displacement_source", "stage"),
                         ("displacement_strength", 1.5), ("clip", "dance"), ("loop_mode", "bounce")):
        response = author.patch(f"/studio/layers/{back['id']}", json={"version": back["version"], field: value})
        field_starts(response, field)
    unchanged = layers_by_role(author, built["board"]["id"])["back"]
    assert unchanged["version"] == back["version"] and float(unchanged["depth"]) == float(back["depth"])
    good = author.patch(f"/studio/layers/{back['id']}", json={"version": back["version"], "depth": -10, "offset_x": 10,
                                                             "scale": 4, "opacity": 0, "blend": "additive",
                                                             "draw_order": 63, "displacement_strength": 1,
                                                             "loop_mode": "ping-pong", "retain": True})
    assert good.status_code == 200 and good.json()["version"] != back["version"], describe(good)
    panel = board_detail(author, built["board"]["id"])["panels"][0]
    for body, field in (({"descriptions": {"en": "", "fr": "ok"}}, "descriptions"),
                        ({"descriptions": {"en": "x" * 301, "fr": "ok"}}, "descriptions"),
                        ({"entry_duration": 0.05}, "entry_duration"), ({"entry_duration": 3.5}, "entry_duration"),
                        ({"camera_x": 11}, "camera_x"), ({"camera_y": -11}, "camera_y")):
        field_starts(author.patch(f"/studio/panels/{panel['id']}", json={"version": panel["version"], **body}), field)
    accepted = author.patch(f"/studio/panels/{panel['id']}", json={"version": panel["version"], "selectable": False,
                                                                   "hold": True, "wide": True, "entry_duration": 3.0,
                                                                   "camera_x": -10, "camera_y": 10})
    assert accepted.status_code == 200, describe(accepted)


def test_stale_version_edits_answer_409_version_conflict_and_ready_or_scheduled_chapter_edits_return_to_draft_or_are_refused(author):
    """A stale version answers 409 version_conflict with the current row; ready edits return to draft; scheduled edits are refused.

    cov: C-CF-704, C-CF-705, C-CF-706, C-CF-707, C-CF-708, C-CF-711, C-CF-712, C-TR-23
    """
    built = build_chapter(author)
    layer = layers_by_role(author, built["board"]["id"])["back"]
    first = author.patch(f"/studio/layers/{layer['id']}", json={"version": layer["version"], "depth": -2})
    assert first.status_code == 200, describe(first)
    assert studio_chapter(author, built["chapter"]["id"])["state"] == "draft", "a layer edit left the chapter ready"
    stale = author.patch(f"/studio/layers/{layer['id']}", json={"version": layer["version"], "depth": 5})
    assert stale.status_code == 409, describe(stale)
    error = error_of(stale)
    assert error["code"] == "version_conflict" and error["current"]["version"] == first.json()["version"], error
    assert float(layers_by_role(author, built["board"]["id"])["back"]["depth"]) == -2.0
    chapter = studio_chapter(author, built["chapter"]["id"])
    assert author.post(f"/studio/chapters/{chapter['id']}/ready").status_code == 200
    ready = studio_chapter(author, chapter["id"])
    stale_chapter = author.patch(f"/studio/chapters/{chapter['id']}", json={"version": chapter["version"],
                                                                             "titles": {"en": "late", "fr": "tard"}})
    assert stale_chapter.status_code == 409 and error_of(stale_chapter)["code"] == "version_conflict"
    edited = author.patch(f"/studio/chapters/{chapter['id']}", json={"version": ready["version"],
                                                                      "titles": {"en": "renamed", "fr": "renomme"}})
    assert edited.status_code == 200 and studio_chapter(author, chapter["id"])["state"] == "draft", describe(edited)
    assert author.post(f"/studio/chapters/{chapter['id']}/ready").status_code == 200
    assert schedule(author, chapter["id"], iso_in(2 * 86400)).status_code == 200
    scheduled = studio_chapter(author, chapter["id"])
    refused = author.patch(f"/studio/chapters/{chapter['id']}", json={"version": scheduled["version"],
                                                                       "titles": {"en": "again", "fr": "encore"}})
    assert 400 <= refused.status_code < 500 and studio_chapter(author, chapter["id"])["state"] == "scheduled", describe(refused)
    assert author.post(f"/studio/chapters/{chapter['id']}/cancel").status_code == 200
    assert studio_chapter(author, chapter["id"])["state"] == "ready"


def test_concurrent_same_version_layer_edits_accept_exactly_one(author):
    """Two edits carrying the same version at the same moment: exactly one is accepted and the other answers 409.

    cov: C-DM-61
    """
    built = build_chapter(author, ready=False)
    for attempt in range(3):
        layer = layers_by_role(author, built["board"]["id"])["stage"]
        calls = [lambda d=d: author.patch(f"/studio/layers/{layer['id']}", json={"version": layer["version"], "depth": d})
                 for d in (attempt + 1, -(attempt + 1))]
        codes = sorted(r.status_code for r in run_together(calls))
        assert codes == [200, 409], codes


def test_studio_search_ranks_chapters_panels_layers_translations_and_preview_manifest_includes_drafts_with_signed_images(author):
    """Studio search types and ranks its results; the preview manifest serves any chapter, drafts included, with signed images.

    cov: C-RL-17, C-CF-713, C-CF-714, C-CF-715, C-CF-716, C-CF-717
    """
    chapters = author.get("/studio/search", params={"q": "welcome to Varny"}).json()
    assert chapters and chapters[0]["type"] == "chapter", chapters
    layer = author.get("/studio/search", params={"q": "c1b1p1-back"}).json()
    assert layer and "panel" in layer[0]["href"], f"a full layer identifier must return the composer address first: {layer[:2]}"
    translation = author.get("/studio/search", params={"q": "consent.accept"}).json()
    assert any(r["type"] == "translation" for r in translation), translation
    for results in (chapters, layer, translation):
        assert all(r["type"] in ("chapter", "panel", "layer", "translation") for r in results)
    draft = studio_chapter_row(author, 1, 6)
    preview = author.get(f"/studio/chapters/{draft['id']}/manifest", params={"locale": "en"})
    assert preview.status_code == 200, describe(preview)
    urls = layer_urls(preview.json())
    assert urls and all("sig=" in u and "expires=" in u for u in urls), urls
    assert fetch_absolute(urls[0]).status_code == 200


def test_translation_strings_per_namespace_list_states_in_the_editor_count_reviewed_only_in_legal_coverage_and_reject_translated_values_with_bad_placeholders_or_markup(author):
    """Strings sit per namespace with states; legal coverage counts reviewed only; bad placeholders and markup are rejected.

    cov: C-CF-773, C-CF-774, C-CF-775, C-CF-776, C-CF-777, C-CF-778, C-CF-779, C-CF-780, C-CF-781, C-CF-782, C-CF-783, C-UF-09, C-DM-132
    """
    coverage = author.get("/studio/translations/coverage").json()
    namespaces = {(c["namespace"], c["locale"]) for c in coverage}
    for namespace in NAMESPACES:
        for locale in LOCALES:
            assert (namespace, locale) in namespaces, f"coverage lacks {namespace} {locale}"
    for row in coverage:
        assert int(row["reviewed"]) == int(row["total"]) and int(row["percent"]) == 100, row
    entries = author.get("/studio/translations/fr", params={"namespace": "legal"}).json()
    entry = next(e for e in entries if e["key"] == "legal.law_body")
    assert entry["source"] == CATALOGUE_EN["legal.law_body"] and entry["value"] == CATALOGUE_FR["legal.law_body"]
    assert entry["state"] in ("untranslated", "translated", "reviewed")
    chrome_entry = next(e for e in author.get("/studio/translations/fr", params={"namespace": "chrome"}).json()
                        if e["key"] == "chrome.about")
    try:
        assert author.put("/studio/translations/fr/legal.law_body",
                          json={"value": entry["value"], "state": "translated", "note": "probe"}).status_code == 200
        assert author.put("/studio/translations/fr/chrome.about",
                          json={"value": chrome_entry["value"], "state": "translated", "note": "probe"}).status_code == 200
        after = {(c["namespace"], c["locale"]): c for c in author.get("/studio/translations/coverage").json()}
        assert int(after[("legal", "fr")]["percent"]) < 100, after[("legal", "fr")]
        assert int(after[("chrome", "fr")]["percent"]) == 100, after[("chrome", "fr")]
    finally:
        for key, item in (("legal.law_body", entry), ("chrome.about", chrome_entry)):
            restored = author.put(f"/studio/translations/fr/{key}",
                                  json={"value": item["value"], "state": "reviewed", "note": item.get("note") or ""})
            assert restored.status_code == 200, describe(restored)
    for bad in ("c'est !", "c'est {hero} {hero} !", "c'est <b>{hero}</b> !", "c'est {heros} !"):
        rejected = author.put("/studio/translations/fr/about.legend_title_2",
                              json={"value": bad, "state": "reviewed", "note": ""})
        assert 400 <= rejected.status_code < 500, f"{bad!r} was saved. {describe(rejected)}"
    kept = next(e for e in author.get("/studio/translations/fr", params={"namespace": "about"}).json()
                if e["key"] == "about.legend_title_2")
    assert kept["value"] == CATALOGUE_FR["about.legend_title_2"]


def test_studio_settings_time_zone_thresholds_and_tipbox_integration_read_change_reject_bad_values_never_returning_the_secret(author):
    """Settings change and reject bad thresholds or zones; the Tipbox integration shows the last four and never the secret.

    cov: C-CF-746, C-CF-810, C-CF-811, C-CF-812, C-CF-813, C-CF-814, C-CF-815, C-CF-816, C-CF-817, C-CF-818, C-DM-64
    """
    settings = settings_of(author)
    for body in ({"early_access_threshold": -1}, {"early_access_threshold": 5.5}, {"credit_threshold": 400},
                 {"time_zone": "Mars/Olympus_Mons"}):
        response = author.patch("/studio/settings", json=body)
        assert 400 <= response.status_code < 500, f"{body} was accepted. {describe(response)}"
    assert settings_of(author) == settings
    changed = author.patch("/studio/settings", json={"time_zone": "Europe/Berlin", "name": STUDIO_NAME})
    assert changed.status_code == 200 and changed.json()["time_zone"] == "Europe/Berlin", describe(changed)
    restored = author.patch("/studio/settings", json={"time_zone": STUDIO_TIME_ZONE})
    assert restored.status_code == 200 and settings_of(author)["time_zone"] == STUDIO_TIME_ZONE
    integration = author.get("/studio/integrations/tipbox")
    assert integration.status_code == 200, describe(integration)
    body = integration.json()
    assert body["page_url"] == TIPBOX_PAGE and body["secret_last_four"] == TIPBOX_SECRET_LAST_FOUR, body
    assert "secret" not in body and TIPBOX_SECRET not in integration.text
    for path in ("/studio/settings", "/studio/overview", "/studio/insights"):
        assert TIPBOX_SECRET not in author.get(path).text
    field_starts(author.put("/studio/integrations/tipbox/secret", json={"secret": "too-short-1234"}), "secret")
    assert author.get("/studio/integrations/tipbox").json()["secret_last_four"] == TIPBOX_SECRET_LAST_FOUR


def test_chapter_state_machine_allows_only_listed_transitions_guarded_by_preflight_failed_rejections(author):
    """Only the listed chapter transitions happen; guards reject failing chapters with preflight_failed and failures.

    cov: C-CF-718, C-CF-719, C-CF-720, C-CF-721, C-CF-722, C-CF-723, C-CF-724, C-CF-725, C-CF-726, C-CF-738, C-CF-739, C-CF-740, C-CF-741, C-TR-24
    """
    built = build_chapter(author, ready=False)
    chapter_id = built["chapter"]["id"]
    assert chapter_state(author, chapter_id) == "draft"
    for action in ("publish", "cancel", "unpublish"):
        response = author.post(f"/studio/chapters/{chapter_id}/{action}")
        assert 400 <= response.status_code < 500 and chapter_state(author, chapter_id) == "draft", f"draft {action}"
    assert author.post(f"/studio/chapters/{chapter_id}/ready").status_code == 200
    assert chapter_state(author, chapter_id) == "ready"
    assert patch_studio_chapter(author, chapter_id, titles={"en": "edited", "fr": "modifie"}).status_code == 200
    assert chapter_state(author, chapter_id) == "draft"
    assert author.post(f"/studio/chapters/{chapter_id}/ready").status_code == 200
    assert schedule(author, chapter_id, iso_in(86400)).status_code == 200 and chapter_state(author, chapter_id) == "scheduled"
    assert 400 <= author.post(f"/studio/chapters/{chapter_id}/unpublish").status_code < 500
    assert author.post(f"/studio/chapters/{chapter_id}/cancel").status_code == 200 and chapter_state(author, chapter_id) == "ready"
    assert publish(author, chapter_id).status_code == 200 and chapter_state(author, chapter_id) == "published"
    for action in ("ready", "cancel"):
        assert 400 <= author.post(f"/studio/chapters/{chapter_id}/{action}").status_code < 500
        assert chapter_state(author, chapter_id) == "published"
    assert author.post(f"/studio/chapters/{chapter_id}/unpublish").status_code == 200
    assert chapter_state(author, chapter_id) == "unpublished"
    assert author.post(f"/studio/chapters/{chapter_id}/ready").status_code == 200 and chapter_state(author, chapter_id) == "ready"
    coverless = new_chapter(author, built["volume"]["id"])
    board = new_board(author, coverless["id"])
    number = coverless["number"]
    assert upload(author, board["id"], [(f"c{number}b{board['number']}p1-back.png", make_png(), "image/png")]).status_code in (200, 201)
    describe_panels(author, board["id"])
    refused = author.post(f"/studio/chapters/{coverless['id']}/ready")
    assert 400 <= refused.status_code < 500, describe(refused)
    error = error_of(refused)
    assert error["code"] == "preflight_failed" and any(int(f["rule"]) == 8 for f in error["failures"]), error
    assert chapter_state(author, coverless["id"]) == "draft"
    assert store_cover(author, coverless["id"]).status_code in (200, 201)
    assert author.post(f"/studio/chapters/{coverless['id']}/ready").status_code == 200
    assert author.post(f"/studio/chapters/{chapter_id}/unpublish").status_code in (400, 409, 422)
    for request in (lambda: publish(author, coverless["id"]), lambda: schedule(author, coverless["id"], iso_in(3600))):
        blocked = request()
        assert 400 <= blocked.status_code < 500, describe(blocked)
        body = error_of(blocked)
        assert body["code"] == "preflight_failed" and any(int(f["rule"]) == 9 for f in body["failures"]), body
        assert chapter_state(author, coverless["id"]) == "ready"


def preflight_rules(author_session, chapter_id: str) -> tuple:
    response = author_session.post(f"/studio/chapters/{chapter_id}/preflight")
    assert response.status_code == 200, describe(response)
    body = response.json()
    assert set(body) >= {"passed", "failures"}
    for failure in body["failures"]:
        assert isinstance(failure["rule"], int) and 1 <= failure["rule"] <= 10 and failure["message"], failure
    return body["passed"], {int(f["rule"]) for f in body["failures"]}


def test_preflight_reports_every_failing_rule_number_with_a_message(author):
    """Preflight lists every failing rule by number with a message, and passes a complete chapter on all ten rules.

    cov: C-CF-727, C-CF-728, C-CF-729, C-CF-730, C-CF-731, C-CF-732, C-CF-733, C-CF-734, C-CF-735, C-CF-736, C-CF-737
    """
    volume = new_volume(author)
    empty = new_chapter(author, volume["id"])
    passed, rules = preflight_rules(author, empty["id"])
    assert passed is False and {1, 8} <= rules, rules
    board = new_board(author, empty["id"])
    assert 1 in preflight_rules(author, empty["id"])[1]
    n = empty["number"]
    assert upload(author, board["id"], [(f"c{n}b{board['number']}p1-back.png", make_png(), "image/png")]).status_code in (200, 201)
    panel = board_detail(author, board["id"])["panels"][0]
    assert author.patch(f"/studio/panels/{panel['id']}", json={"version": panel["version"],
                                                               "descriptions": {"en": "only english"}}).status_code == 200
    assert 4 in preflight_rules(author, empty["id"])[1]
    heavy = new_board(author, empty["id"])
    complete = build_chapter(author, volume=volume, ready=False)
    passed, rules = preflight_rules(author, complete["chapter"]["id"])
    assert 9 in rules, "chapter 2 cannot pass rule 9 while chapter 1 is a draft"
    solo = build_chapter(author, ready=False)
    passed, rules = preflight_rules(author, solo["chapter"]["id"])
    assert passed is True and rules == set(), rules
    big = build_chapter(author, ready=False)
    first_board = board_detail(author, big["board"]["id"])
    number = big["number"]
    noisy = upload(author, first_board["id"], [(f"c{number}b{first_board['number']}p2-back.png",
                                                make_png(1100, 1000, noise=True), "image/png")])
    assert noisy.status_code in (200, 201), describe(noisy)
    describe_panels(author, first_board["id"])
    passed, rules = preflight_rules(author, big["chapter"]["id"])
    assert 6 in rules and 5 not in rules, rules
    assert heavy["number"] == 2


def test_release_at_in_the_future_with_utc_offset_normalised_to_an_instant_early_access_days_range_and_locale_waivers_skipping_rule_4(author):
    """release_at takes any offset and reads back in UTC; bad moments, day counts and reasonless waivers are rejected.

    cov: C-CF-742, C-CF-743, C-CF-744, C-CF-745, C-CF-757, C-CF-758, C-CF-759, C-CF-760, C-CF-761, C-CF-762
    """
    built = build_chapter(author)
    chapter_id = built["chapter"]["id"]
    for moment in ("2027-03-28T20:00:00", iso_in(-3600), iso_in(6 * 366 * 86400)):
        field_starts(schedule(author, chapter_id, moment), "release_at")
        assert chapter_state(author, chapter_id) == "ready"
    accepted = schedule(author, chapter_id, RELEASE_INPUT)
    assert accepted.status_code == 200, describe(accepted)
    assert studio_chapter(author, chapter_id)["release_at"] == RELEASE_READBACK
    assert author.post(f"/studio/chapters/{chapter_id}/cancel").status_code == 200
    draft = build_chapter(author, ready=False)
    detail = studio_chapter(author, draft["chapter"]["id"])
    assert int(detail["early_access_days"]) == EARLY_ACCESS_DAYS
    for days in (-1, 31):
        field_starts(patch_studio_chapter(author, draft["chapter"]["id"], early_access_days=days), "early_access_days")
    assert patch_studio_chapter(author, draft["chapter"]["id"], early_access_days=30).status_code == 200
    board = board_detail(author, draft["board"]["id"])
    panel = board["panels"][0]
    assert author.patch(f"/studio/panels/{panel['id']}", json={"version": panel["version"],
                                                               "descriptions": {"en": "english only"}}).status_code == 200
    assert 4 in preflight_rules(author, draft["chapter"]["id"])[1]
    shapes = ([{"locale": "fr", "reason": "{reason}"}], {"fr": {"reason": "{reason}"}})
    shape = None
    for candidate in shapes:
        probe = json.loads(json.dumps(candidate).replace("{reason}", ""))
        response = patch_studio_chapter(author, draft["chapter"]["id"], waivers=probe)
        assert 400 <= response.status_code < 500, f"a waiver without a reason was accepted. {describe(response)}"
        if str(error_of(response).get("field") or "").startswith("waivers") and "reason" in str(error_of(response)):
            shape = candidate
            break
    shape = shape or shapes[0]
    too_long = json.loads(json.dumps(shape).replace("{reason}", "r" * 201))
    assert 400 <= patch_studio_chapter(author, draft["chapter"]["id"], waivers=too_long).status_code < 500
    valid = json.loads(json.dumps(shape).replace("{reason}", "French pass next week"))
    saved = patch_studio_chapter(author, draft["chapter"]["id"], waivers=valid)
    assert saved.status_code == 200, describe(saved)
    assert 4 not in preflight_rules(author, draft["chapter"]["id"])[1], "a live waiver must let rule 4 skip the locale"
    waivers = studio_chapter(author, draft["chapter"]["id"])["waivers"]
    text = json.dumps(waivers)
    expiry = re.search(r"\d{4}-\d{2}-\d{2}T[\d:.]+Z", text)
    assert expiry, waivers
    assert 29 <= (parse_instant(expiry.group(0)) - utc_now()).days <= 30, waivers


def test_publishing_twice_keeps_published_at_with_one_audit_record_and_unpublishing_removes_the_chapter_from_sitemaps_and_readers_with_a_redirect(author, backend, site):
    """Publishing twice keeps published_at and one audit record; unpublishing hides the chapter and redirects its page.

    cov: C-CF-751, C-CF-752, C-CF-753, C-CF-754, C-CF-755, C-CF-756, C-UF-27, C-DM-59
    """
    built = build_chapter(author)
    chapter_id, order = built["chapter"]["id"], built["order"]
    assert publish(author, chapter_id).status_code == 200
    stamped = studio_chapter(author, chapter_id)["published_at"]
    assert stamped
    again = publish(author, chapter_id)
    assert again.status_code == 200, describe(again)
    assert studio_chapter(author, chapter_id)["published_at"] == stamped
    assert backend.count("audit_records", action="chapter.published", subject_id=chapter_id) == 1
    assert manifest(order, 1).status_code == 200
    assert f"/volumes/{order}/chapter/1<" in site.get("/sitemap.xml").text
    assert author.post(f"/studio/chapters/{chapter_id}/unpublish").status_code == 200
    assert chapter_state(author, chapter_id) == "unpublished"
    assert manifest(order, 1).status_code == 404
    assert f"/volumes/{order}/chapter/1<" not in site.get("/sitemap.xml").text
    assert f"/volumes/{order}/chapter/1<" not in site.get("/fr/sitemap.xml").text
    for path, target in ((f"/volumes/{order}/chapter/1", "/chapters"), (f"/fr/volumes/{order}/chapter/1", "/fr/chapters")):
        response = site.get(path)
        assert response.status_code in (302, 303, 307), describe(response)
        assert urlparse(response.headers["location"]).path == target, response.headers["location"]


def test_concurrent_publish_requests_leave_one_published_audit_record(author, backend):
    """Simultaneous publish requests stamp one published_at and leave exactly one chapter.published audit record.

    cov: C-DM-60
    """
    built = build_chapter(author)
    chapter_id = built["chapter"]["id"]
    results = run_together([lambda: publish(author, chapter_id) for _ in range(5)])
    assert any(r.status_code == 200 for r in results), [describe(r) for r in results]
    assert all(r.status_code < 500 for r in results)
    assert chapter_state(author, chapter_id) == "published"
    assert backend.count("audit_records", action="chapter.published", subject_id=chapter_id) == 1


def test_studio_mutations_write_one_audit_record_with_request_id(author, backend):
    """Each studio mutation writes one audit record with the author, action, subject and the request's identifier.

    cov: C-CF-763, C-CF-764, C-CF-765, C-CF-766, C-CF-767
    """
    before = backend.count("audit_records")
    built = build_chapter(author)
    chapter_id = built["chapter"]["id"]
    assert backend.count("audit_records", action="layer.imported") >= 1
    scheduled = schedule(author, chapter_id, iso_in(86400))
    assert scheduled.status_code == 200
    rows = backend.query("SELECT actor_email, subject_id, request_id FROM audit_records WHERE action = %s "
                         "AND subject_id = %s", ("chapter.scheduled", chapter_id))
    assert len(rows) == 1 and rows[0]["actor_email"] == AUTHOR_EMAIL, rows
    assert rows[0]["request_id"] == scheduled.headers.get("x-request-id"), rows
    assert author.post(f"/studio/chapters/{chapter_id}/cancel").status_code == 200
    assert publish(author, chapter_id).status_code == 200
    unpublished = author.post(f"/studio/chapters/{chapter_id}/unpublish")
    assert unpublished.status_code == 200
    assert backend.count("audit_records", action="chapter.unpublished", subject_id=chapter_id) == 1
    layer = layers_by_role(author, built["board"]["id"])["back"]
    count = backend.count("audit_records")
    edited = author.patch(f"/studio/layers/{layer['id']}", json={"version": layer["version"], "depth": 1})
    assert edited.status_code == 200
    assert backend.count("audit_records") == count + 1, "a layer edit did not write exactly one audit record"
    assert backend.count("audit_records") > before


def test_scheduled_chapter_publishes_itself_within_60_seconds_of_release(author):
    """A scheduled chapter becomes published no later than 60 seconds after its release moment, with nobody asking.

    cov: C-CF-748, C-TR-41
    """
    built = build_chapter(author)
    release = iso_in(15)
    assert schedule(author, built["chapter"]["id"], release).status_code == 200
    limit = deadline_after(15 + SCHEDULER_DEADLINE_SECONDS + 10)
    state = chapter_state(author, built["chapter"]["id"])
    while state != "published" and before(limit):
        settle(3.0)
        state = chapter_state(author, built["chapter"]["id"])
    assert state == "published", f"the chapter was still {state} 60 seconds after its release moment"
    stamped = parse_instant(studio_chapter(author, built["chapter"]["id"])["published_at"])
    assert (stamped - parse_instant(release)).total_seconds() <= SCHEDULER_DEADLINE_SECONDS + 5
    assert manifest(built["order"], 1).status_code == 200


def test_scheduled_chapter_failing_preflight_at_release_returns_to_ready_with_an_alert(author):
    """A scheduled chapter failing preflight at its moment returns to ready and raises the pinned overview alert.

    cov: C-CF-749, C-CF-750
    """
    volume = new_volume(author)
    first = build_chapter(author, volume=volume)
    second = build_chapter(author, volume=volume)
    assert schedule(author, first["chapter"]["id"], iso_in(3600)).status_code == 200
    release = iso_in(20)
    assert 400 <= schedule(author, second["chapter"]["id"], release).status_code < 500, (
        "chapter 2 cannot be scheduled before chapter 1")
    assert author.post(f"/studio/chapters/{first['chapter']['id']}/cancel").status_code == 200
    assert schedule(author, first["chapter"]["id"], iso_in(10)).status_code == 200
    assert schedule(author, second["chapter"]["id"], iso_in(20)).status_code == 200
    assert author.post(f"/studio/chapters/{first['chapter']['id']}/cancel").status_code == 200
    limit = deadline_after(20 + SCHEDULER_DEADLINE_SECONDS + 10)
    alert = None
    while before(limit):
        overview = author.get("/studio/overview").json()
        alert = next((a for a in overview["alerts"] if a.get("kind") == ALERT_KIND
                      and second["chapter"]["id"] in json.dumps(a)), None)
        if alert and chapter_state(author, second["chapter"]["id"]) == "ready":
            break
        settle(3.0)
    assert chapter_state(author, second["chapter"]["id"]) == "ready", "the failing chapter was not returned to ready"
    assert alert, f"no {ALERT_KIND} alert names the chapter"


def test_measured_events_accept_only_the_closed_set_of_names_and_params(anon, backend):
    """Only the eight named events with their own params are stored; any other name or key is rejected and stored nowhere.

    cov: C-CF-546, C-CF-547, C-CF-548, C-CF-549, C-CF-550, C-CF-551, C-CF-552, C-CF-553, C-CF-554, C-CF-555
    """
    samples = {"volume": 1, "chapter": 1, "locale": "en", "panel": 2, "elapsed_seconds": 12, "last_panel": 3,
               "route": "chapters", "failure": "network", "state": "on"}
    before = backend.count("measured_events")
    for name, params in EVENT_PARAMS.items():
        response = anon.post("/events", json={"name": name, "params": {k: samples[k] for k in params}})
        assert response.status_code in (200, 201, 202, 204), describe(response)
    assert backend.count("measured_events") == before + len(EVENT_PARAMS)
    stored = backend.count("measured_events")
    for body in ({"name": "chapter_shared", "params": {"volume": 1}},
                 {"name": "chapter_opened", "params": {"volume": 1, "chapter": 1, "locale": "en", "email": READER_EMAIL}},
                 {"name": "tip_control_pressed", "params": {"route": "chapters", "comment": "free text"}}):
        assert 400 <= anon.post("/events", json=body).status_code < 500, body
    assert backend.count("measured_events") == stored


def test_page_view_route_names_outside_the_list_are_rejected_carrying_no_visitor_identifier_and_studio_lists_views_newest_first_by_route(anon, author, backend):
    """Page views accept only the listed route names, store no identifier, and list newest first by route in the studio.

    cov: C-CF-560, C-CF-561, C-CF-562, C-CF-565, C-CF-566
    """
    for route in PAGE_VIEW_ROUTES:
        assert anon.post("/page-views", json={"route": route}).status_code in (200, 201, 202, 204), route
    count = backend.count("page_views")
    for bad in ("home", "chapter/1", "/about", "admin"):
        assert 400 <= anon.post("/page-views", json={"route": bad}).status_code < 500, bad
    assert backend.count("page_views") == count
    assert columns_of(backend, "page_views") <= {"id", "route", "viewed_at"}, columns_of(backend, "page_views")
    listed = author.get("/studio/page-views", params={"route": "about", "limit": 20}).json()
    items = items_of(listed)
    assert items and all(i["route"] == "about" for i in items), items[:3]
    moments = [parse_instant(i["viewed_at"]) for i in items]
    assert moments == sorted(moments, reverse=True)
    assert "next_cursor" in listed


def opens_for(author_session, number: int) -> int:
    server = author_session.get("/studio/insights").json()["server"]
    return sum(int(row["count"]) for row in server["chapter_opens"]
               if int(row["volume"]) == 1 and int(row["chapter"]) == number)


def test_studio_insights_count_one_chapter_open_per_served_manifest_beside_measured_events_never_summed(author, anon, backend):
    """Each served manifest counts one chapter open with no identifier; insights keep server counts beside measured events.

    cov: C-CF-563, C-CF-564, C-CF-567, C-CF-568, C-CF-569, C-CF-570
    """
    before = opens_for(author, 3)
    for _ in range(3):
        assert manifest(1, 3).status_code == 200
    assert wait_for(lambda: opens_for(author, 3) == before + 3), "three manifests did not count three chapter opens"
    assert columns_of(backend, "chapter_opens") <= {"id", "chapter_id", "opened_at"}
    insights = author.get("/studio/insights").json()
    assert set(insights) >= {"server", "measured"}
    assert set(insights["server"]) >= {"page_views", "chapter_opens"}
    for row in insights["server"]["page_views"]:
        assert set(row) >= {"route", "hour", "count"}
    assert anon.post("/events", json={"name": "chapter_completed",
                                      "params": {"volume": 1, "chapter": 3, "elapsed_seconds": 40}}).status_code < 300
    events = author.get("/studio/insights").json()["measured"]["events"]
    assert any(e["name"] == "chapter_completed" and int(e["count"]) >= 1 for e in events), events
    assert opens_for(author, 3) == before + 3, "a measured event was added to the server counts"


MONTHS_EN = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December")
MONTHS_FR = ("janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre",
             "novembre", "decembre")
ALLOWED_STORAGE = ("dd-consent", "dd-language", "dd-last-chapter")
KEY_PATH_RE = re.compile(r"\b(chrome|index|chapters|reader|locked|consent|support|about|legal|account|not-found)\.[a-z]+_[a-z_]+\b")


def visible_text(tab) -> str:
    return tab.evaluate("() => document.body.innerText")


def timecode(tab, chapter: int) -> str:
    prefix = two_digit(chapter)
    return tab.get_by_text(re.compile(rf"^{prefix}:\d\d$")).first.inner_text().strip()


def wait_timecode(tab, expected: str, seconds: float = 10.0) -> bool:
    chapter = int(expected.split(":")[0])
    return bool(wait_for(lambda: timecode(tab, chapter) == expected, seconds, 0.3))


def in_viewport(tab, locator) -> bool:
    box = locator.bounding_box()
    size = tab.viewport_size
    return bool(box) and box["x"] >= -1 and box["y"] >= -1 and box["x"] + box["width"] <= size["width"] + 1 \
        and box["y"] + box["height"] <= size["height"] + 1


def style_of(locator, prop: str) -> str:
    return locator.evaluate(f"el => getComputedStyle(el).getPropertyValue('{prop}')")


def luminance(color: str) -> float:
    parts = [float(x) for x in re.findall(r"[\d.]+", color)[:3]]
    channels = []
    for value in parts:
        c = value / 255
        channels.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def ground_of(locator) -> str:
    return locator.evaluate("el => { let n = el; while (n) { const c = getComputedStyle(n).backgroundColor; "
                            "if (c && !c.endsWith(', 0)') && c !== 'transparent') return c; n = n.parentElement; } "
                            "return 'rgb(255, 255, 255)'; }")


def running_long_animations(tab) -> int:
    return tab.evaluate("() => document.getAnimations().filter(a => a.playState === 'running' && "
                        "(a.effect.getComputedTiming().iterations === Infinity || "
                        "a.effect.getComputedTiming().duration > 100)).length")


def test_shell_keeps_one_img_role_canvas_named_after_the_chapter_across_in_app_navigation_without_reloading_the_document(chromium):
    """One shell and one image-role canvas survive every in-app navigation without reloading the document.

    cov: C-CF-45, C-CF-46, C-CF-47, C-CF-48, C-CF-119
    """
    fresh = new_context(chromium, consent=None)
    tab = fresh.new_page()
    open_route(tab, "/", wait=2.0)
    assert tab.get_by_role("button", name="Accept").is_visible(), "the shell carries the consent strip"
    fresh.close()
    context = new_context(chromium)
    tab = context.new_page()
    open_route(tab, "/", wait=2.0)
    assert tab.locator("canvas").count() == 1
    tab.evaluate("() => { window.__ddCanvas = document.querySelector('canvas'); }")
    mark_document(tab)
    assert tab.get_by_role("link", name="chapters").first.is_visible()
    assert tab.get_by_role("link", name="legal notice & terms of use").is_visible()
    assert tab.get_by_role("button", name="EN").is_visible() and tab.get_by_role("button", name="FR").is_visible()
    assert tab.get_by_role("button", name="enter fullscreen").count() == 1
    tab.get_by_role("link", name="chapters").first.click()
    tab.wait_for_url("**/chapters")
    settle(1.5)
    tab.get_by_role("listbox").focus()
    tab.keyboard.press("Home")
    tab.keyboard.press("Enter")
    tab.wait_for_url("**/chapter/1")
    settle(2.0)
    assert document_kept(tab), "in-app navigation reloaded the document"
    assert tab.evaluate("() => window.__ddCanvas === document.querySelector('canvas')"), "the canvas was recreated"
    canvas = tab.locator("canvas")
    assert canvas.get_attribute("role") == "img"
    assert CHAPTER_TITLES[1][0].lower() in (canvas.get_attribute("aria-label") or "").lower()
    box = canvas.bounding_box()
    assert box["width"] >= tab.viewport_size["width"] - 2 and box["height"] >= tab.viewport_size["height"] - 2
    context.close()


def test_title_heading_credit_header_wordmark_byline_links_footer_language_selector_fullscreen_corner_controls_wait_for_consent(chromium):
    """The title screen, header, footer and corner controls carry their pinned copy, positions and consent wait.

    cov: C-CF-91, C-CF-92, C-FE-01, C-FE-02, C-FE-03, C-FE-04, C-FE-05, C-FE-08, C-FE-10, C-FE-11, C-FE-12, C-FE-13
    """
    context = new_context(chromium, consent=None)
    tab = context.new_page()
    open_route(tab, "/", wait=2.0)
    assert tab.get_by_role("heading", level=1, name="Doudou Fever").count() == 1
    assert tab.get_by_text("By Damien Lorca & Camille Rouyer", exact=True).count() >= 1
    assert tab.get_by_text(CATALOGUE_EN["chrome.byline"], exact=True).count() >= 1
    selector = tab.get_by_role("button", name="EN")
    assert not in_viewport(tab, selector), "corner controls must wait off screen until consent is answered"
    tab.get_by_role("button", name="Decline").click()
    settle(1.5)
    assert in_viewport(tab, tab.get_by_role("button", name="EN")) and in_viewport(tab, tab.get_by_role("button", name="FR"))
    assert in_viewport(tab, tab.get_by_role("link", name="legal notice & terms of use"))
    assert in_viewport(tab, tab.get_by_role("button", name="enter fullscreen"))
    footer = tab.get_by_role("link", name="legal notice & terms of use").bounding_box()
    size = tab.viewport_size
    assert footer["x"] > size["width"] / 2 and footer["y"] > size["height"] / 2, footer
    assert tab.locator("header a[href='/']").count() == 0, "the wordmark navigates on the title screen"
    open_route(tab, "/chapters", wait=2.0)
    wordmark = tab.locator("header a[href='/']").first
    assert wordmark.count() == 1 and "doudou" in wordmark.inner_text().lower()
    chapters_link = tab.get_by_role("link", name="chapters").first
    about_link = tab.get_by_role("link", name="about").first
    left, middle, right = chapters_link.bounding_box(), wordmark.bounding_box(), about_link.bounding_box()
    assert left["x"] < middle["x"] < right["x"], (left, middle, right)
    assert int(style_of(chapters_link, "font-weight")) > int(style_of(about_link, "font-weight"))
    context.close()
    hidden = new_context(chromium)
    hidden.add_init_script("Object.defineProperty(Document.prototype, 'fullscreenEnabled', { get: () => false });")
    tab = hidden.new_page()
    open_route(tab, "/chapters", wait=2.0)
    assert tab.get_by_role("button", name="enter fullscreen").count() == 0
    hidden.close()


def test_rack_lists_open_and_locked_sleeves_with_pinned_title_subtitle_timecode_padlock_and_accessible_names_hiding_the_draft(chromium, anon):
    """The rack lists open and locked sleeves with pinned formats, padlocks, no links on locked sleeves, and no draft.

    cov: C-CF-96, C-CF-97, C-CF-98, C-CF-99, C-CF-100, C-CF-101, C-CF-102, C-CF-103, C-CF-104, C-CF-105, C-UX-17, C-FE-31
    """
    releases = {int(c["number"]): parse_instant(c["release_at"]) for c in volumes()[0]["chapters"]}
    context = new_context(chromium, timezone_id="UTC")
    tab = context.new_page()
    open_route(tab, "/chapters", wait=2.5)
    assert tab.get_by_role("heading", name="select a chapter").count() == 1
    options = tab.get_by_role("option")
    names = [options.nth(i).get_attribute("aria-label") or options.nth(i).inner_text() for i in range(options.count())]
    text = visible_text(tab) + " " + " ".join(names)
    for number in (1, 2, 3):
        assert f"{two_digit(number)}.{CHAPTER_TITLES[number][0]}" in text
    assert "Doudou FeverVol. I" in text and "01:06" in text
    assert "chapter 1 of 6" in tab.content(), "an open sleeve timecode is announced as chapter 1 of 6"
    assert CHAPTER_TITLES[6][0] not in text, "the draft chapter has a sleeve"
    for number in (4, 5):
        moment = releases[number]
        expected = f"{CHAPTER_TITLES[number][0]}, locked, opens {moment.day} {MONTHS_EN[moment.month - 1]} {moment.year}"
        sleeve = tab.get_by_role("option", name=expected)
        assert sleeve.count() == 1, f"no locked sleeve named {expected!r}: {names}"
        assert sleeve.locator("a").count() == 0, "a locked sleeve carries a link"
        assert sleeve.locator("svg").count() >= 1, "a locked sleeve shows no padlock"
        assert "not-allowed" in style_of(sleeve, "cursor") or sleeve.locator("[style*='not-allowed']").count() >= 0
    open_sleeve = tab.get_by_role("option").first
    assert "not-allowed" not in style_of(open_sleeve, "cursor")
    context.close()


def test_unpublished_chapter_sleeve_is_named_title_locked_with_a_redirecting_page(chromium, author, site):
    """An unpublished chapter's sleeve is named `<title>, locked` and its page redirects to the rack.

    cov: C-CF-106, C-CF-165
    """
    built = build_chapter(author)
    title = "unpublished " + token_hex()
    assert patch_studio_chapter(author, built["chapter"]["id"], titles={"en": title, "fr": title}).status_code == 200
    assert author.post(f"/studio/chapters/{built['chapter']['id']}/ready").status_code == 200
    assert publish(author, built["chapter"]["id"]).status_code == 200
    assert author.post(f"/studio/chapters/{built['chapter']['id']}/unpublish").status_code == 200
    response = site.get(f"/volumes/{built['order']}/chapter/1")
    assert response.status_code in (302, 303, 307) and urlparse(response.headers["location"]).path == "/chapters"
    context = new_context(chromium)
    tab = context.new_page()
    open_route(tab, "/chapters", wait=2.5)
    assert tab.get_by_role("option", name=f"{title}, locked", exact=True).count() == 1
    context.close()


def selected_index(tab) -> int:
    return tab.evaluate("() => [...document.querySelectorAll('[role=option]')].findIndex(o => "
                        "o.getAttribute('aria-selected') === 'true')")


def test_rack_listbox_keys_enter_opens_home_end_jump_and_wheel_drag_sleeve_arrows_settle_on_the_nearest_sleeve(ui_page):
    """Rack keys, wheel, drag and sleeve arrows move a single settled selection; Enter opens the selected chapter.

    cov: C-CF-107, C-CF-108, C-CF-109, C-CF-110, C-CF-111, C-CF-112, C-CF-113, C-FE-30, C-FE-36
    """
    open_route(ui_page, "/chapters", wait=2.5)
    listbox = ui_page.get_by_role("listbox")
    listbox.focus()
    ui_page.keyboard.press("Home")
    settle(0.8)
    assert selected_index(ui_page) == 0
    ui_page.keyboard.press("ArrowRight")
    settle(0.8)
    assert selected_index(ui_page) == 1
    ui_page.keyboard.press("End")
    settle(0.8)
    assert selected_index(ui_page) == ui_page.get_by_role("option").count() - 1
    ui_page.keyboard.press("Home")
    settle(0.8)
    box = listbox.bounding_box()
    ui_page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    ui_page.mouse.wheel(0, 400)
    settle(1.5)
    after_wheel = selected_index(ui_page)
    assert after_wheel > 0, "the wheel did not move the rack"
    ui_page.mouse.move(box["x"] + box["width"] * 0.7, box["y"] + box["height"] / 2)
    ui_page.mouse.down()
    ui_page.mouse.move(box["x"] + box["width"] * 0.2, box["y"] + box["height"] / 2, steps=12)
    ui_page.mouse.up()
    settle(1.5)
    after_drag = selected_index(ui_page)
    assert after_drag != after_wheel, "dragging did not move the rack"
    assert ui_page.evaluate("() => document.querySelectorAll('[role=option][aria-selected=true]').length") == 1
    ui_page.keyboard.press("Home")
    settle(0.8)
    arrows = ui_page.get_by_role("option").first.get_by_role("button")
    assert arrows.count() == 2, "an open sleeve on a wide screen carries two small arrows"
    assert arrows.first.is_disabled(), "the first arrow is disabled on the first sleeve"
    arrows.last.click()
    settle(1.0)
    assert selected_index(ui_page) == 1
    ui_page.get_by_role("listbox").focus()
    ui_page.keyboard.press("Home")
    ui_page.keyboard.press("Enter")
    ui_page.wait_for_url("**/chapter/1")


def test_reader_moves_by_arrow_keys_wheel_drag_panel_controls_and_progress_slider_with_the_timeline_capsule_timecode(ui_page):
    """The reader moves by keys, wheel, drag, panel controls and the slider, shown in a capsule with cover, titles and timecode.

    cov: C-OV-15, C-CF-120, C-CF-121, C-CF-122, C-CF-123, C-CF-125, C-CF-126, C-CF-127, C-CF-128, C-CF-129, C-CF-130, C-CF-131, C-CF-132, C-CF-133, C-CF-134, C-UX-63, C-FE-35, C-FE-39
    """
    open_route(ui_page, "/chapter/1", wait=3.0)
    assert wait_timecode(ui_page, "01:01")
    capsule_text = visible_text(ui_page)
    assert CHAPTER_TITLES[1][0] in capsule_text and "Doudou FeverVol. I" in capsule_text
    order, number = 1, 1
    assert ui_page.locator(f"img[src*='/api/covers/{order}/{number}']").count() >= 1, "the capsule shows the chapter cover"
    assert "panel 1" in ui_page.content()
    previous = ui_page.get_by_role("button", name="previous panel")
    following = ui_page.get_by_role("button", name="next panel")
    assert previous.is_disabled(), "previous panel is enabled on the first panel"
    capsule = ui_page.get_by_role("slider", name="chapter progress")
    assert following.bounding_box()["x"] > capsule.bounding_box()["x"], "the arrow controls sit right of the capsule"
    for key, expected in (("ArrowRight", "01:02"), ("ArrowUp", "01:03"), ("ArrowLeft", "01:02"), ("ArrowDown", "01:01")):
        ui_page.keyboard.press(key)
        assert wait_timecode(ui_page, expected), f"{key} did not reach {expected}"
        settle(0.5)
    following.click()
    assert wait_timecode(ui_page, "01:02")
    settle(0.5)
    previous.click()
    assert wait_timecode(ui_page, "01:01")
    assert capsule.get_attribute("aria-valuemin") == "0" and capsule.get_attribute("aria-valuemax") == "100"
    capsule.focus()
    ui_page.keyboard.press("End")
    assert wait_timecode(ui_page, "01:05"), "the slider's keys did not move the view"
    track = capsule.bounding_box()
    ui_page.mouse.click(track["x"] + 2, track["y"] + track["height"] / 2)
    assert wait_timecode(ui_page, "01:01"), "pressing the start of the track did not move the view"
    settle(0.5)
    size = ui_page.viewport_size
    ui_page.mouse.move(size["width"] / 2, size["height"] / 2)
    ui_page.mouse.wheel(0, 900)
    settle(2.0)
    assert timecode(ui_page, 1) != "01:01", "wheel down did not move forward"
    before_drag = timecode(ui_page, 1)
    ui_page.mouse.move(size["width"] * 0.8, size["height"] / 2)
    ui_page.mouse.down()
    ui_page.mouse.move(size["width"] * 0.1, size["height"] / 2, steps=20)
    ui_page.mouse.up()
    settle(2.0)
    assert timecode(ui_page, 1) != before_drag, "dragging did not move the reader"


def test_next_track_face_repeats_the_next_title_four_times_linking_without_reload_except_on_the_last_chapter_of_a_volume(ui_page, author):
    """The last panel shows the next-track face linking to the next chapter without reload; a volume's last chapter offers the rack.

    cov: C-CF-136, C-CF-137, C-CF-138, C-CF-139, C-CF-140, C-CF-141
    """
    open_route(ui_page, "/chapter/1", wait=3.0)
    ui_page.get_by_role("slider", name="chapter progress").focus()
    ui_page.keyboard.press("End")
    assert wait_timecode(ui_page, "01:05")
    settle(1.5)
    assert ui_page.get_by_text("next track", exact=True).count() >= 1
    face = ui_page.locator("a[href$='/chapter/2']").filter(has_text=CHAPTER_TITLES[2][0]).first
    assert face.inner_text().count(CHAPTER_TITLES[2][0]) == 4, face.inner_text()
    assert face.inner_text().count(" _ ") >= 4 or face.inner_text().count("_") >= 4
    mark_document(ui_page)
    face.click()
    ui_page.wait_for_url("**/chapter/2")
    assert wait_timecode(ui_page, "02:01") and document_kept(ui_page)
    built = build_chapter(author)
    assert publish(author, built["chapter"]["id"]).status_code == 200
    open_route(ui_page, f"/volumes/{built['order']}/chapter/1", wait=3.0)
    ui_page.get_by_role("slider", name="chapter progress").focus()
    ui_page.keyboard.press("End")
    settle(2.5)
    assert ui_page.get_by_text("next track", exact=True).count() == 0
    rack_line = ui_page.get_by_role("link", name=CATALOGUE_EN["reader.end_of_volume"])
    assert rack_line.count() == 1 and urlparse(rack_line.get_attribute("href")).path.endswith("/chapters")


def test_text_mode_lists_panel_descriptions_in_order_in_the_page_language(ui_page):
    """Text mode lists the chapter's panel descriptions in reading order in the page language.

    cov: C-CF-144
    """
    open_route(ui_page, "/fr/chapter/1", wait=3.0)
    ui_page.get_by_role("button", name=CATALOGUE_FR["reader.text_mode"]).click()
    settle(1.0)
    items = ui_page.locator("ol li")
    expected = [PANEL_DESCRIPTIONS[k][1] for k in sorted(k for k in PANEL_DESCRIPTIONS if k[0] == 1)]
    assert [items.nth(i).inner_text().strip() for i in range(items.count())] == expected


def test_locked_state_release_date_follows_page_language_and_reader_time_zone(chromium, site):
    """The locked state's opening line writes the release date in the page language and the reader's own time zone.

    cov: C-CF-156, C-CF-529, C-CF-747
    """
    release = parse_instant(next(c for c in volumes()[0]["chapters"] if int(c["number"]) == 4)["release_at"])
    shifted = release + datetime.timedelta(hours=14)
    assert site.get("/chapter/4").status_code == 200
    context = new_context(chromium, timezone_id="Pacific/Kiritimati")
    tab = context.new_page()
    open_route(tab, "/chapter/4", wait=3.0)
    text = visible_text(tab)
    assert "04. scratch that !" in text
    assert f"This chapter opens {shifted.day} {MONTHS_EN[shifted.month - 1]} {shifted.year}." in text, text[:400]
    assert CATALOGUE_EN["locked.support"] in text
    open_route(tab, "/fr/chapter/4", wait=3.0)
    assert f"Ce chapitre sort le {shifted.day} {MONTHS_FR[shifted.month - 1]} {shifted.year}." in visible_text(tab)
    context.close()


def test_unknown_paths_render_not_found_404_pages_that_request_no_manifest_or_image_and_draw_no_scene(chromium, site):
    """Unknown paths answer 404 with the not-found page, request no manifest or image, and draw no scene.

    cov: C-CF-168, C-CF-171, C-CF-172
    """
    for path in ("/nothing-here", "/chapters/extra/segment", "/fr/nothing-here"):
        assert site.get(path).status_code == 404, path
    context = new_context(chromium)
    tab = context.new_page()
    seen = []
    tab.on("request", lambda request: seen.append(urlparse(request.url).path))
    open_route(tab, "/nothing-here", wait=3.0)
    assert "Oopsy, page not found" in visible_text(tab)
    home = tab.get_by_role("link", name="Go back to home")
    assert home.count() == 1 and urlparse(home.get_attribute("href")).path == "/"
    assert not [p for p in seen if re.match(r"^/api/(volumes/\d+/chapters|textures|covers)", p)], seen
    context.close()


def test_failed_layer_image_is_dropped_and_failed_chapter_load_offers_try_again(chromium):
    """A failed layer image is skipped while reading continues; a failed chapter offers try again and back to chapters.

    cov: C-CF-173, C-CF-174, C-CF-175, C-CF-176
    """
    context = new_context(chromium)
    tab = context.new_page()
    tab.route(re.compile(r".*/api/textures/.*c1b1p1-stage.*"), lambda route: route.abort())
    open_route(tab, "/chapter/1", wait=3.0)
    assert wait_timecode(tab, "01:01")
    tab.keyboard.press("ArrowRight")
    assert wait_timecode(tab, "01:02"), "reading stopped after one layer image failed"
    failing = {"on": True}

    def maybe_fail(route):
        if failing["on"]:
            route.fulfill(status=500, body="{}")
        else:
            route.continue_()

    order, number = 1, 2
    tab.route(re.compile(rf".*/api/volumes/{order}/chapters/{number}(\?.*)?$"), maybe_fail)
    open_route(tab, "/chapter/2", wait=3.0)
    assert CATALOGUE_EN["reader.load_failed"] in visible_text(tab)
    assert tab.get_by_role("link", name="back to chapters").count() + tab.get_by_role("button", name="back to chapters").count() >= 1
    mark_document(tab)
    failing["on"] = False
    tab.get_by_role("button", name="try again").click()
    assert wait_timecode(tab, "02:01") and document_kept(tab), "try again did not recover without a reload"
    context.close()


def test_without_a_drawing_context_routes_fall_back_to_a_plain_readable_site(chromium):
    """Without a drawing context every route falls back to plain readable pages, links, text mode and prose.

    cov: C-CF-177, C-CF-178, C-CF-179, C-CF-180, C-CF-181, C-CF-182, C-CF-183
    """
    context = new_context(chromium)
    context.add_init_script("HTMLCanvasElement.prototype.getContext = function () { return null; };")
    tab = context.new_page()
    open_route(tab, "/", wait=2.0)
    assert tab.get_by_role("heading", name="Doudou Fever").is_visible()
    assert tab.get_by_text("By Damien Lorca & Camille Rouyer").first.is_visible()
    open_route(tab, "/chapters", wait=2.0)
    for number in (1, 2, 3):
        assert tab.locator(f"a[href$='/chapter/{number}']").count() >= 1
    locked = tab.get_by_text(CHAPTER_TITLES[4][0]).first
    assert locked.is_visible() and locked.evaluate("el => !el.closest('a')")
    open_route(tab, "/chapter/1", wait=2.0)
    assert PANEL_DESCRIPTIONS[(1, 1, 1)][0] in visible_text(tab)
    open_route(tab, "/about", wait=2.0)
    assert CATALOGUE_EN["about.legend_body"][:40] in visible_text(tab)
    open_route(tab, "/legal", wait=2.0)
    assert CATALOGUE_EN["legal.publisher_body"] in visible_text(tab)
    context.close()


def test_support_us_tip_link_carries_return_token_opening_tipbox_in_a_new_browsing_context(ui_page):
    """The support us link on the rack and in the reader goes to Tipbox with a return token, a new tab and safe rel.

    cov: C-RL-03, C-CF-185, C-CF-186, C-CF-187, C-CF-188, C-CF-189
    """
    for route in ("/chapters", "/chapter/1"):
        open_route(ui_page, route, wait=2.5)
        link = ui_page.get_by_role("link", name="support us").first
        href = link.get_attribute("href")
        assert href.startswith(TIPBOX_PAGE), href
        assert parse_qs(urlparse(href).query).get("return_token"), href
        assert link.get_attribute("target") == "_blank"
        rel = (link.get_attribute("rel") or "").split()
        assert "noopener" in rel and "noreferrer" in rel, rel


def test_account_page_shows_changes_reader_settings_offering_export_delete(chromium):
    """The account page shows and changes a reader's address, language and notifications and offers export and deletion.

    cov: C-CF-190, C-CF-191, C-CF-192, C-CF-193
    """
    probe = register_reader()
    context = new_context(chromium)
    context.add_init_script(f"try {{ window.localStorage.setItem('dd-session', '{probe['token']}'); }} catch (e) {{}}")
    tab = context.new_page()
    open_route(tab, "/account", wait=3.0)
    text = visible_text(tab)
    assert probe["email"] in text and "drops" in text.lower()
    assert tab.get_by_role("button", name="download my data").count() + tab.get_by_role("link", name="download my data").count() == 1
    assert tab.get_by_role("button", name="delete my account").count() == 1
    choice = tab.get_by_label(re.compile("notification", re.I)).first
    if choice.evaluate("el => el.tagName") == "SELECT":
        choice.select_option("all")
    else:
        tab.get_by_label("all", exact=True).check()
    settle(0.5)
    saver = tab.get_by_role("button", name=re.compile("save", re.I))
    if saver.count():
        saver.first.click()
    assert wait_for(lambda: api_client(probe["token"]).get("/me").json()["notifications"] == "all", 10)
    context.close()


def test_reader_sign_in_dialog_is_offered_in_three_places_with_no_header_link_hides_the_website_decoy_uploads_browser_progress_and_survives_a_revoked_session(chromium):
    """Sign-in is offered only where pinned, hides the decoy, uploads browser progress and recovers from a revoked session.

    cov: C-CF-06, C-CF-306, C-CF-307, C-UF-20, C-UF-21, C-UF-22, C-UF-23, C-UF-24, C-UF-25
    """
    probe = register_reader()
    context = new_context(chromium)
    context.add_init_script("try { localStorage.setItem('dd-progress-1-2', '0.600'); localStorage.setItem('dd-last-chapter', '1/2'); } catch (e) {}")
    tab = context.new_page()
    for route in ("/", "/chapters", "/about"):
        open_route(tab, route, wait=2.0)
        assert tab.locator("header").get_by_text(re.compile("sign in", re.I)).count() == 0, f"{route} header offers sign-in"
    open_route(tab, "/chapter/4", wait=3.0)
    tab.get_by_role("button", name="notify me").click()
    dialog = tab.get_by_role("dialog", name="sign in")
    assert dialog.is_visible()
    tab.get_by_role("button", name="create an account").click()
    decoy = tab.locator("input[name='website']")
    assert decoy.count() == 1 and not decoy.is_visible(), "the website decoy is visible"
    tab.get_by_role("button", name="sign in").first.click() if tab.get_by_role("button", name="sign in").count() else None
    open_route(tab, "/chapter/4", wait=3.0)
    tab.get_by_role("button", name="notify me").click()
    tab.get_by_label("email").fill(probe["email"])
    tab.get_by_label("password").fill(probe["password"])
    tab.get_by_role("dialog").get_by_role("button", name="sign in").click()
    assert wait_for(lambda: any(int(c["chapter"]) == 2 and abs(float(c["fraction"]) - 0.6) < 1e-9
                                for c in api_client(probe["token"]).get("/me/progress").json()["chapters"]), 15), (
        "signing in did not upload the browser progress")
    assert tab.url.endswith("/chapter/4"), "signing in moved the reader off the page"
    assert tab.evaluate("() => localStorage.getItem('dd-progress-1-2')") == "0.600"
    session_token = tab.evaluate("() => localStorage.getItem('dd-session')")
    assert session_token
    with api_client(session_token) as session:
        assert session.post("/auth/logout").status_code in (200, 204)
    open_route(tab, "/account", wait=3.0)
    assert tab.get_by_role("dialog", name="sign in").is_visible(), "a revoked session was not offered sign-in again"
    assert tab.url.endswith("/account")
    assert tab.evaluate("() => localStorage.getItem('dd-session')") in (None, "")
    assert tab.evaluate("() => localStorage.getItem('dd-progress-1-2')") == "0.600", "signing out dropped browser progress"
    context.close()


def test_reading_progress_is_kept_in_local_storage_keys_dd_last_chapter_and_dd_progress(chromium):
    """Reading writes dd-last-chapter and dd-progress-<volume>-<chapter> at most once per second with three decimals.

    cov: C-RL-04, C-CF-145, C-CF-146, C-CF-147, C-CF-148
    """
    context = new_context(chromium)
    context.add_init_script("window.__ddWrites = 0; const set = Storage.prototype.setItem; Storage.prototype.setItem = "
                            "function (k, v) { if (String(k).startsWith('dd-progress-')) window.__ddWrites += 1; "
                            "return set.call(this, k, v); };")
    tab = context.new_page()
    open_route(tab, "/chapter/1", wait=3.0)
    tab.evaluate("() => { window.__ddWrites = 0; }")
    for _ in range(8):
        tab.keyboard.press("ArrowRight")
        settle(0.25)
    settle(1.5)
    writes = tab.evaluate("() => window.__ddWrites")
    assert writes <= 5, f"progress was written {writes} times in about three seconds"
    assert tab.evaluate("() => localStorage.getItem('dd-last-chapter')") == "1/1"
    value = tab.evaluate("() => localStorage.getItem('dd-progress-1-1')")
    assert value and re.fullmatch(r"(0(\.\d{1,3})?|1(\.0{1,3})?)", value) and float(value) > 0, value
    context.close()


def test_language_switch_changes_address_strings_lang_and_images_without_reload(chromium):
    """Switching language keeps the document, changes the address, strings, lang and lettered images, and remembers the choice.

    cov: C-CF-325, C-CF-326, C-CF-327, C-CF-328, C-CF-329, C-CF-330
    """
    context = new_context(chromium)
    tab = context.new_page()
    seen = []
    tab.on("request", lambda request: seen.append(urlparse(request.url).path))
    open_route(tab, "/chapter/1", wait=3.0)
    mark_document(tab)
    tab.get_by_role("button", name="FR").click()
    tab.wait_for_url("**/fr/chapter/1")
    settle(2.0)
    assert document_kept(tab)
    assert tab.evaluate("() => document.documentElement.lang") == "fr"
    assert tab.get_by_role("link", name="chapitres").count() >= 1
    assert tab.evaluate("() => localStorage.getItem('dd-language')") == "fr"
    assert any("c1b1p1-sign" in p and "fr" in p for p in seen), "the lettered layer image did not switch language"
    tab.get_by_role("button", name="EN").click()
    tab.wait_for_url(re.compile(r".*/chapter/1$"))
    settle(1.0)
    assert not urlparse(tab.url).path.startswith("/fr") and tab.evaluate("() => document.documentElement.lang") == "en"
    context.close()


def test_public_pages_never_show_a_raw_error_stack_trace_or_catalogue_key_path(chromium):
    """No public page shows a catalogue key path, a raw error or a stack trace, even when the API fails.

    cov: C-CF-334, C-UF-55
    """
    context = new_context(chromium)
    tab = context.new_page()
    for route in ("/", "/chapters", "/chapter/1", "/chapter/4", "/about", "/legal", "/account", "/support/return",
                  "/fr", "/fr/chapters", "/fr/about", "/nowhere"):
        open_route(tab, route, wait=2.0)
        text = visible_text(tab)
        assert not KEY_PATH_RE.search(text), f"{route} shows a key path: {KEY_PATH_RE.search(text).group(0)}"
        assert "Traceback" not in text and "Internal Server Error" not in text
    tab.route(re.compile(r".*/api/volumes(\?.*)?$"), lambda route: route.fulfill(status=500, body="Traceback: boom"))
    open_route(tab, "/chapters", wait=2.5)
    text = visible_text(tab)
    assert "Traceback" not in text and "boom" not in text and not KEY_PATH_RE.search(text)
    context.close()


def test_public_loading_states_show_first_load_screen_then_a_thin_bottom_bar_and_an_empty_or_failed_volume_list_offers_a_retry(chromium):
    """A first visit shows the first-load screen, later loads a thin bottom bar, and an empty or failed rack offers a retry.

    cov: C-UF-47, C-UF-48, C-UF-49, C-UF-50, C-UF-51, C-FE-23
    """
    context = new_context(chromium)
    tab = context.new_page()

    def slow(route):
        settle(1.5)
        route.continue_()

    tab.route(re.compile(r".*/api/textures/.*"), slow)
    tab.goto(appclient.app_url() + "/", wait_until="domcontentloaded")
    settle(0.8)
    loader = tab.get_by_role("progressbar").first
    assert loader.count() == 1 and loader.is_visible(), "no first-load screen on the first visit"
    settle(4.0)
    tab.get_by_role("link", name="chapters").first.click()
    tab.wait_for_url("**/chapters")
    tab.get_by_role("listbox").focus()
    tab.keyboard.press("Enter")
    settle(0.5)
    bar = tab.get_by_role("progressbar").first
    box = bar.bounding_box()
    assert box and box["height"] <= 12 and box["y"] + box["height"] >= tab.viewport_size["height"] - 16, box
    tab.unroute(re.compile(r".*/api/textures/.*"))
    state = {"mode": "empty"}

    def rack(route):
        if state["mode"] == "empty":
            route.fulfill(status=200, content_type="application/json", body="[]")
        elif state["mode"] == "fail":
            route.fulfill(status=500, content_type="application/json", body="{}")
        else:
            route.continue_()

    tab.route(re.compile(r".*/api/volumes(\?.*)?$"), rack)
    for mode in ("empty", "fail"):
        state["mode"] = mode
        open_route(tab, "/chapters", wait=2.5)
        retry = tab.get_by_role("button", name=re.compile("try again|retry", re.I))
        assert retry.count() >= 1, f"a {mode} volume list shows no recoverable retry"
    state["mode"] = "live"
    tab.get_by_role("button", name=re.compile("try again|retry", re.I)).first.click()
    settle(2.5)
    assert tab.get_by_role("option").count() >= 5
    context.close()


def record_click_opens_surprise(tab) -> bool:
    size = tab.viewport_size
    dialog = tab.get_by_role("dialog", name="surprise")
    for row in range(10):
        for column in range(13):
            tab.mouse.click(size["width"] * (0.3 + 0.4 * column / 12), size["height"] * (0.12 + 0.43 * row / 9))
            settle(0.25)
            if dialog.count() and dialog.first.is_visible():
                tab.keyboard.press("Escape")
                return True
            if urlparse(tab.url).path not in ("", "/"):
                open_route(tab, "/", wait=1.5)
    return False


def test_responsive_width_steps_hide_arrow_pairs_move_header_links_language_selector_tip_control_and_scale_rack_timeline_record_without_sideways_overflow_in_portrait(chromium):
    """Each width step rearranges the chrome, the record hides on narrow screens, nothing overflows sideways, portrait grows the about headings.

    cov: C-UX-82, C-UX-83, C-UX-84, C-UX-85, C-UX-86, C-UX-87, C-UX-88, C-UX-89, C-UX-90, C-UX-93, C-FE-06, C-FE-25
    """
    def fresh(viewport):
        context = new_context(chromium, viewport=viewport)
        return context, context.new_page()

    for viewport in (WIDE_VIEWPORT, TABLET_VIEWPORT, NARROW_TABLET_VIEWPORT, PHONE_VIEWPORT, SMALLEST_VIEWPORT):
        context, tab = fresh(viewport)
        for route in ("/", "/chapters", "/chapter/1", "/about", "/legal"):
            open_route(tab, route, wait=1.5)
            assert tab.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 1"), (
                f"{route} overflows sideways at {viewport['width']}px")
        context.close()
    context, tab = fresh(WIDE_VIEWPORT)
    open_route(tab, "/chapter/1", wait=2.5)
    assert tab.get_by_role("button", name="next panel").is_visible()
    wide_capsule = tab.get_by_role("slider", name="chapter progress").bounding_box()["width"]
    context.close()
    context, tab = fresh(TABLET_VIEWPORT)
    open_route(tab, "/chapter/1", wait=2.5)
    assert not tab.get_by_role("button", name="next panel").is_visible(), "arrow pairs still show at tablet width"
    context.close()
    context, tab = fresh(NARROW_TABLET_VIEWPORT)
    open_route(tab, "/chapters", wait=2.0)
    language = tab.get_by_role("button", name="EN").bounding_box()
    assert language["x"] < 200 and language["y"] > NARROW_TABLET_VIEWPORT["height"] - 160, language
    open_route(tab, "/about", wait=2.0)
    assert tab.get_by_role("navigation").filter(has=tab.get_by_role("link", name="the team")).count() == 0 or \
        not tab.get_by_role("link", name="the team").first.is_visible(), "the about rail still shows"
    context.close()
    context, tab = fresh(PHONE_VIEWPORT)
    open_route(tab, "/chapters", wait=2.0)
    chapters_link = tab.get_by_role("link", name="chapters").first.bounding_box()
    about_link = tab.get_by_role("link", name="about").first.bounding_box()
    assert chapters_link["x"] < 60 and about_link["x"] + about_link["width"] > PHONE_VIEWPORT["width"] - 60
    tip = tab.get_by_role("link", name="support us").first.bounding_box()
    assert tip["y"] < 160 and abs(tip["x"] + tip["width"] / 2 - PHONE_VIEWPORT["width"] / 2) < 60, tip
    open_route(tab, "/chapter/1", wait=2.5)
    assert tab.get_by_role("slider", name="chapter progress").bounding_box()["width"] < wide_capsule
    context.close()
    context, tab = fresh(PORTRAIT_VIEWPORT)
    open_route(tab, "/about", wait=2.0)
    portrait = tab.get_by_role("heading").first.evaluate("el => parseFloat(getComputedStyle(el).fontSize) / window.innerWidth")
    context.close()
    context, tab = fresh(WIDE_VIEWPORT)
    open_route(tab, "/about", wait=2.0)
    landscape = tab.get_by_role("heading").first.evaluate("el => parseFloat(getComputedStyle(el).fontSize) / window.innerWidth")
    context.close()
    assert portrait > landscape, (portrait, landscape)
    context, tab = fresh(WIDE_VIEWPORT)
    open_route(tab, "/", wait=2.5)
    assert record_click_opens_surprise(tab), "no click above the centre of the wide title screen opened the surprise"
    context.close()
    context, tab = fresh(PHONE_VIEWPORT)
    open_route(tab, "/", wait=2.5)
    assert not record_click_opens_surprise(tab), "the title-screen record still shows on a narrow screen"
    context.close()


def test_touch_devices_get_no_hover_animation_or_tip_label_roll(chromium):
    """On a touch device hovering animates nothing and the tip label never rolls.

    cov: C-UX-53, C-FE-34
    """
    context = new_context(chromium, viewport=PHONE_VIEWPORT, has_touch=True, is_mobile=True)
    tab = context.new_page()
    open_route(tab, "/chapters", wait=2.5)
    for name in ("chapters", "support us"):
        link = tab.get_by_role("link", name=name).first
        before_hover = style_of(link, "transform")
        link.hover()
        settle(0.6)
        assert style_of(link, "transform") == before_hover, f"{name} animated on hover on a touch device"
        assert running_long_animations(tab) == 0
    context.close()


def test_reduced_motion_jumps_the_camera_and_stills_record_reveals_pile_cards_marquee_consent(chromium):
    """Under reduced motion no page runs looping or long animations: record, reveals, pile, cards, marquee and consent stay still.

    cov: C-UX-54, C-UX-55, C-UX-56, C-UX-57, C-UX-58, C-UX-59, C-UX-60
    """
    context = new_context(chromium, consent=None, reduced_motion="reduce")
    tab = context.new_page()
    open_route(tab, "/", wait=2.0)
    strip = tab.get_by_role("button", name="Accept")
    assert strip.is_visible() and running_long_animations(tab) == 0, "the consent strip or record animates"
    strip.click()
    for route in ("/", "/chapters", "/about", "/about#team"):
        open_route(tab, route, wait=2.0)
        assert running_long_animations(tab) == 0, f"{route} animates under reduced motion"
    open_route(tab, "/chapter/1", wait=3.0)
    tab.keyboard.press("ArrowRight")
    settle(0.15)
    assert wait_timecode(tab, "01:02", 1.0), "the camera did not jump between panels"
    tab.get_by_role("slider", name="chapter progress").focus()
    tab.keyboard.press("End")
    settle(1.5)
    assert running_long_animations(tab) == 0, "the next-track marquee moves under reduced motion"
    context.close()


def test_accessibility_keyboard_navigation_focus_ring_inline_icon_labels_touch_targets_assistive_text_headings_per_route_contrast_live_regions_and_200_percent_text(chromium):
    """Keyboard reach, focus rings, labels, targets, clipped assistive text, headings, contrast, live regions, icons and 200 percent text.

    cov: C-UX-70, C-UX-72, C-UX-73, C-UX-74, C-UX-75, C-UX-76, C-UX-77, C-UX-78, C-UX-79, C-UX-81, C-FE-17
    """
    context = new_context(chromium)
    tab = context.new_page()
    for route, status_path in (("/", "/"), ("/chapters", "/chapters"), ("/chapter/1", "/chapter/1"), ("/about", "/about"),
                               ("/legal", "/legal"), ("/account", "/account"), ("/support/return", "/support/return"),
                               ("/missing-page", "/missing-page")):
        open_route(tab, route, wait=2.0)
        assert tab.locator("h1").count() == 1, f"{route} has {tab.locator('h1').count()} level-one headings"
    open_route(tab, "/chapters", wait=2.5)
    reached = set()
    for _ in range(25):
        tab.keyboard.press("Tab")
        info = tab.evaluate("() => { const el = document.activeElement; const s = getComputedStyle(el); return "
                            "{tag: el.tagName, name: el.getAttribute('aria-label') || el.innerText || '', "
                            "outline: s.outlineStyle, width: parseFloat(s.outlineWidth), shadow: s.boxShadow}; }")
        reached.add(info["name"].strip().lower())
        assert info["outline"] != "none" and info["width"] >= 2 or info["shadow"] != "none", f"no focus ring on {info}"
    for name in ("chapters", "about", "support us"):
        assert any(name in r for r in reached), f"keyboard never reached {name}"
    unnamed = tab.evaluate("() => [...document.querySelectorAll('button, a[href]')].filter(el => el.offsetParent && "
                           "!(el.getAttribute('aria-label') || el.innerText.trim() || el.getAttribute('title'))).length")
    assert unnamed == 0, "an icon-only control has no label"
    small = tab.evaluate("() => [...document.querySelectorAll('button, a[href], [role=slider]')].filter(el => el.offsetParent)"
                         ".map(el => el.getBoundingClientRect()).filter(r => r.width > 0 && (r.width < 44 || r.height < 44)).length")
    assert small == 0, f"{small} touch targets are under 44 by 44 pixels"
    icons = tab.evaluate("() => [...document.querySelectorAll('svg')].map(s => getComputedStyle(s).fill + getComputedStyle(s).stroke)")
    assert icons, "no inline icons"
    sleeve = tab.get_by_role("option").first
    assert contrast(style_of(sleeve, "color"), ground_of(sleeve)) >= 4.5
    open_route(tab, "/", wait=2.0)
    credit = tab.get_by_text("By Damien Lorca & Camille Rouyer").first
    hidden = credit.evaluate("el => { const s = getComputedStyle(el); return {opacity: s.opacity, display: s.display, "
                             "clip: s.clip + ' ' + s.clipPath, w: el.getBoundingClientRect().width}; }")
    assert hidden["opacity"] != "0" and hidden["display"] != "none", hidden
    assert "rect" in hidden["clip"] or "inset" in hidden["clip"] or hidden["w"] <= 2, hidden
    open_route(tab, "/chapter/1", wait=3.0)
    assert tab.locator("[aria-live=polite]").count() >= 1 and tab.locator("[aria-live=assertive]").count() >= 1
    tab.keyboard.press("ArrowRight")
    assert wait_for(lambda: PANEL_DESCRIPTIONS[(1, 1, 2)][0] in tab.locator("[aria-live=polite]").all_inner_texts().__str__(), 5, 0.3)
    tab.evaluate("() => { document.documentElement.style.fontSize = '200%'; }")
    open_route(tab, "/chapters", wait=2.0)
    tab.evaluate("() => { document.documentElement.style.fontSize = '200%'; }")
    settle(1.0)
    option = tab.get_by_role("option").first
    assert CHAPTER_TITLES[1][0] in (option.get_attribute("aria-label") or option.inner_text())
    context.close()


def test_inter_variable_font_family_is_served_from_the_app_origin_with_the_fallback_stack_and_the_pinned_type_sizes_on_a_flat_scale(chromium):
    """Inter is bundled on the app origin with the pinned fallback stack, and the pinned elements use the pinned sizes.

    cov: C-UX-20, C-UX-21, C-UX-22, C-UX-23, C-UX-24, C-UX-25, C-UX-26, C-UX-27, C-UX-28, C-UX-29, C-UX-30, C-UX-31, C-UX-32, C-UX-33, C-UX-34, C-TR-46, C-TR-47
    """
    context = new_context(chromium)
    tab = context.new_page()
    fonts = []
    tab.on("request", lambda request: fonts.append(request.url) if request.resource_type == "font" else None)
    open_route(tab, "/chapters", wait=3.0)
    family = tab.evaluate("() => getComputedStyle(document.body).fontFamily")
    assert family.startswith("Inter") and "Liberation Sans" in family and "system-ui" in family, family
    origin = urlparse(appclient.app_url()).netloc
    assert fonts and all(urlparse(u).netloc == origin for u in fonts), fonts

    def size(locator):
        return float(style_of(locator, "font-size").replace("px", "")), int(style_of(locator, "font-weight"))

    checks = [
        (tab.get_by_text("01.welcome to Varny", exact=True).first, 17, 800),
        (tab.get_by_text("Doudou FeverVol. I", exact=True).first, 14, None),
        (tab.get_by_text("01:06", exact=True).first, 12, 700),
        (tab.get_by_role("link", name="about").first, 15, None),
        (tab.get_by_text("support us", exact=True).first, 15, 700),
        (tab.get_by_role("button", name="EN"), 10, 600),
    ]
    open_route(tab, "/chapters", wait=2.0)
    for locator, px, weight in checks:
        got_px, got_weight = size(locator)
        assert abs(got_px - px) < 0.6, (px, got_px)
        if weight:
            assert got_weight == weight, (weight, got_weight)
    open_route(tab, "/chapter/1", wait=3.0)
    got = size(tab.get_by_text("01:01", exact=True).first)
    assert abs(got[0] - 9.5) < 0.6 and got[1] == 700, got
    open_route(tab, "/", wait=2.0)
    got = size(tab.get_by_text("read now", exact=True).first)
    assert abs(got[0] - 35) < 0.6 and got[1] == 600, got
    open_route(tab, "/legal", wait=2.0)
    assert abs(size(tab.get_by_role("heading", name="Legal Notice & Terms of Use"))[0] - 60) < 0.6
    assert abs(size(tab.get_by_role("heading", name="Hosting"))[0] - 30) < 0.6
    assert abs(size(tab.get_by_text(CATALOGUE_EN["legal.publisher_body"]).first)[0] - 20) < 0.6
    open_route(tab, "/about", wait=2.0)
    assert abs(size(tab.get_by_text(CATALOGUE_EN["about.team_dam_body"]).first)[0] - 18) < 0.6
    heading = tab.get_by_role("heading").first
    ratio = heading.evaluate("el => parseFloat(getComputedStyle(el).fontSize) / window.innerWidth")
    assert abs(ratio - 0.05) < 0.006 and int(style_of(heading, "font-weight")) == 900, ratio
    context.close()


def test_reader_panel_selection_escape_input_guard_and_edge_strips_swallow_drags_keeping_browser_history(ui_page):
    """Panel clicks frame and Escape returns; a second quick input is swallowed; edge strips swallow edge drags.

    cov: C-FE-15, C-FE-16, C-FE-40, C-FE-41, C-FE-42
    """
    open_route(ui_page, "/chapter/1", wait=3.0)
    ui_page.keyboard.press("ArrowRight")
    assert wait_timecode(ui_page, "01:02")
    settle(0.8)
    ui_page.keyboard.press("ArrowRight")
    ui_page.keyboard.press("ArrowRight")
    settle(1.5)
    assert timecode(ui_page, 1) == "01:03", "a second input right after a selection was not swallowed"
    size = ui_page.viewport_size
    canvas = ui_page.locator("canvas")
    before_click = canvas.screenshot()
    ui_page.mouse.click(size["width"] / 2, size["height"] / 2)
    settle(1.2)
    framed = canvas.screenshot()
    assert framed != before_click, "clicking a panel did not move the camera"
    ui_page.keyboard.press("Escape")
    settle(1.2)
    assert canvas.screenshot() != framed, "Escape did not fly back out"
    history = ui_page.evaluate("() => history.length")
    edge = ui_page.evaluate(f"() => {{ const el = document.elementFromPoint(3, {size['height'] / 2}); "
                            "const r = el.getBoundingClientRect(); return {tag: el.tagName, w: r.width, h: r.height}; }")
    assert edge["tag"] != "CANVAS" and edge["w"] <= 40 and edge["h"] >= size["height"] - 2, edge
    position = timecode(ui_page, 1)
    ui_page.mouse.move(3, size["height"] / 2)
    ui_page.mouse.down()
    ui_page.mouse.move(400, size["height"] / 2, steps=15)
    ui_page.mouse.up()
    settle(1.5)
    assert ui_page.evaluate("() => history.length") == history and ui_page.url.endswith("/chapter/1")
    assert timecode(ui_page, 1) == position, "a drag from the edge moved the reader"


def test_consent_strip_keeps_focus_until_answered_writing_dd_consent_and_releasing_corner_controls(chromium):
    """The consent strip takes and keeps focus, writes dd-consent on answer, releases the corner controls, and stays answered.

    cov: C-CF-533, C-CF-534, C-CF-536, C-CF-537, C-CF-538
    """
    for answer, stored in (("Accept", "accepted"), ("Decline", "declined")):
        context = new_context(chromium, consent=None)
        tab = context.new_page()
        open_route(tab, "/", wait=2.5)
        assert CATALOGUE_EN["consent.message"] in visible_text(tab)
        inside = "() => !!document.activeElement.closest('[role=dialog], [role=region], section, aside, div') && " \
                 "[...document.querySelectorAll('button')].some(b => b.innerText.trim() === 'Accept' && " \
                 "b.parentElement.contains(document.activeElement) || b === document.activeElement)"
        assert tab.evaluate(inside), "the consent strip did not take focus"
        for _ in range(6):
            tab.keyboard.press("Tab")
            assert tab.evaluate(inside), "focus left the consent strip before it was answered"
        tab.get_by_role("button", name=answer).click()
        settle(1.0)
        assert tab.evaluate("() => localStorage.getItem('dd-consent')") == stored
        assert in_viewport(tab, tab.get_by_role("button", name="EN"))
        tab.reload()
        settle(2.0)
        assert tab.get_by_role("button", name="Accept").count() == 0, "the strip returned after an answer"
        context.close()


def test_declined_visitor_keeps_only_functional_storage_keys_and_sends_no_event_or_request_to_another_origin_analytics_font_or_video(chromium):
    """A declined visitor keeps only functional keys, sends no measured event, and no page calls another origin.

    cov: C-OV-19, C-OV-20, C-CF-541, C-CF-542, C-CF-543, C-TR-48, C-CN-15
    """
    context = new_context(chromium, consent=None)
    tab = context.new_page()
    requests = []
    tab.on("request", lambda request: requests.append(request.url))
    open_route(tab, "/", wait=2.5)
    assert not any("/api/events" in u for u in requests), "an event was sent before any consent answer"
    tab.get_by_role("button", name="Decline").click()
    for route in ("/chapters", "/chapter/1", "/about", "/legal", "/fr", "/fr/chapter/2"):
        open_route(tab, route, wait=2.0)
        for _ in range(3):
            tab.keyboard.press("ArrowRight")
            settle(0.6)
    keys = storage_keys(tab) + cookie_names(tab)
    extra = [k for k in keys if k not in ALLOWED_STORAGE and not k.startswith(PROGRESS_KEY_PREFIX)]
    assert not extra, f"a declined visitor holds {extra}"
    assert not any("/api/events" in u for u in requests), "a declined visitor sent measured events"
    origin = urlparse(appclient.app_url()).netloc
    foreign = [u for u in requests if urlparse(u).scheme.startswith("http") and urlparse(u).netloc != origin]
    assert not foreign, f"pages called other origins: {foreign[:5]}"
    context.close()


def test_accepted_visitor_records_chapter_opened_and_panel_reached_events(chromium):
    """After accept, reading sends chapter_opened and panel_reached through /api/events, each panel once per visit.

    cov: C-CF-544, C-CF-545
    """
    context = new_context(chromium, consent=None)
    tab = context.new_page()
    events = []
    tab.on("request", lambda request: events.append(json.loads(request.post_data or "{}"))
           if urlparse(request.url).path == "/api/events" else None)
    open_route(tab, "/", wait=2.0)
    tab.get_by_role("button", name="Accept").click()
    open_route(tab, "/chapter/1", wait=3.0)
    for key in ("ArrowRight", "ArrowLeft", "ArrowRight"):
        tab.keyboard.press(key)
        settle(1.0)
    settle(2.0)
    opened = [e for e in events if e.get("name") == "chapter_opened"]
    assert opened and set(opened[0]["params"]) == {"volume", "chapter", "locale"}, events
    reached_two = [e for e in events if e.get("name") == "panel_reached" and int(e["params"]["panel"]) == 2]
    assert len(reached_two) == 1, f"panel_reached for panel 2 was sent {len(reached_two)} times"
    context.close()


def test_page_views_are_recorded_by_route_name_whatever_the_consent_decision(chromium, author):
    """Every public page view, in-app ones included, posts its route name whatever the consent decision.

    cov: C-CF-556, C-CF-557, C-CF-558, C-CF-559
    """
    built = build_chapter(author)
    assert publish(author, built["chapter"]["id"]).status_code == 200
    for consent in ("declined", "accepted"):
        context = new_context(chromium, consent=consent)
        tab = context.new_page()
        routes = []
        tab.on("request", lambda request: routes.append(json.loads(request.post_data or "{}").get("route"))
               if urlparse(request.url).path == "/api/page-views" else None)
        open_route(tab, "/", wait=2.0)
        tab.get_by_role("link", name="chapters").first.click()
        settle(2.0)
        open_route(tab, "/chapter/1", wait=2.0)
        open_route(tab, f"/volumes/{built['order']}/chapter/1", wait=2.0)
        for route in ("/about", "/legal", "/support/return", "/account", "/no-such-page"):
            open_route(tab, route, wait=1.5)
        assert routes[:2] == ["index", "chapters"], routes
        assert routes.count("chapter-id") >= 2 and {"about", "legal", "support-return", "account", "not-found"} <= set(routes), routes
        context.close()


def test_legal_page_is_selectable_prose_with_eight_sections_stating_publisher_contact_hosting_domains_property_terms_data_cookies_law_facts(ui_page):
    """The legal page is selectable prose under its heading with eight sections carrying the pinned facts.

    cov: C-CF-539, C-CF-540, C-CF-603, C-CF-604, C-CF-605, C-CF-606, C-CF-607, C-CF-608, C-CF-609, C-CF-610, C-CF-611, C-CF-612, C-CF-613, C-CF-614, C-CF-615, C-CF-616, C-CF-617, C-CF-618
    """
    open_route(ui_page, "/legal", wait=2.5)
    assert ui_page.get_by_role("heading", level=1, name="Legal Notice & Terms of Use").count() == 1
    headings = [ui_page.get_by_role("heading", name=h, exact=True).count() for h in LEGAL_HEADINGS]
    assert headings == [1] * 8, dict(zip(LEGAL_HEADINGS, headings))
    assert ui_page.evaluate("() => getComputedStyle(document.querySelector('main') || document.body).userSelect") != "none"
    text = visible_text(ui_page)
    for key in ("legal.publisher_body", "legal.hosting_body", "legal.domains_body", "legal.property_body",
                "legal.terms_body", "legal.data_body", "legal.cookies_body", "legal.law_body", "legal.contact_label"):
        assert CATALOGUE_EN[key] in text, key
    for fact in (CONTACT_EMAIL, HOSTING, REGISTRAR, *DOMAINS, "dd-consent", "dd-session", "dd-studio-session",
                 "French law", "courts of Paris", "Accept"):
        assert fact in text, fact


def test_about_page_scrolls_four_named_sections_with_a_dot_rail_opening_fragments_and_hiding_the_rail_when_the_language_selector_moves(chromium):
    """About alone scrolls through four named sections with a dot rail, opens fragments, and hides the rail at the pinned step.

    cov: C-CF-571, C-CF-572, C-CF-573, C-CF-574, C-CF-575, C-CF-599, C-CF-600, C-CF-601, C-CF-602
    """
    context = new_context(chromium)
    tab = context.new_page()
    open_route(tab, "/chapters", wait=2.0)
    assert tab.evaluate("() => document.scrollingElement.scrollHeight <= window.innerHeight + 1")
    open_route(tab, "/about", wait=2.5)
    assert tab.evaluate("() => document.scrollingElement.scrollHeight > window.innerHeight * 2")
    for name in ("intro", "the legend", "the team", "support us"):
        assert tab.get_by_role("region", name=name).count() == 1, f"no section named {name}"
    rail = tab.get_by_role("navigation").filter(has=tab.get_by_role("link", name="the team")).first
    assert rail.get_by_role("link").count() == 4
    box = rail.bounding_box()
    assert box["x"] > tab.viewport_size["width"] * 0.8
    rail.get_by_role("link", name="the team").hover()
    settle(0.5)
    assert "the team" in visible_text(tab)
    rail.get_by_role("link", name="the team").click()
    settle(1.5)
    assert in_viewport(tab, tab.get_by_role("region", name="the team").get_by_role("heading").first)
    for route, section in (("/about#doudou", "the legend"), ("/about#team", "the team"), ("/fr/about#equipe", "l'equipe"),
                           ("/about#support", "support us"), ("/fr/about#doudou", "la legende"), ("/about#nothing", "intro")):
        open_route(tab, route, wait=2.5)
        region = tab.get_by_role("region", name=section)
        top = region.evaluate("el => el.getBoundingClientRect().top")
        assert abs(top) < tab.viewport_size["height"] / 2, f"{route} did not open at {section} (top {top})"
    context.close()
    narrow = new_context(chromium, viewport=NARROW_TABLET_VIEWPORT)
    tab = narrow.new_page()
    open_route(tab, "/about", wait=2.0)
    assert not tab.get_by_role("link", name="the team").first.is_visible()
    narrow.close()


def test_about_sections_show_the_pinned_legend_team_support_texts(ui_page):
    """The about sections show the pinned legend, team and support texts, dark and cream cards, and the tip chip link.

    cov: C-CF-582, C-CF-583, C-CF-584, C-CF-585, C-CF-586, C-CF-587
    """
    open_route(ui_page, "/about", wait=2.5)
    ui_page.evaluate("() => window.scrollTo(0, document.scrollingElement.scrollHeight)")
    settle(3.0)
    text = visible_text(ui_page)
    for key in ("about.legend_body", "about.team_dam_body", "about.team_ca_body", "about.support_body"):
        assert CATALOGUE_EN[key] in ui_page.content() or CATALOGUE_EN[key] in text, key
    hidden = ui_page.get_by_text(CATALOGUE_EN["about.support_hidden"], exact=True)
    assert hidden.count() == 1 and not hidden.is_visible()
    dam = ui_page.get_by_text(CATALOGUE_EN["about.team_dam_body"]).first
    ca = ui_page.get_by_text(CATALOGUE_EN["about.team_ca_body"]).first
    assert luminance(ground_of(dam)) < 0.1 and luminance(ground_of(ca)) > 0.7
    chip = ui_page.get_by_role("link", name=re.compile("give a tip"))
    assert chip.count() == 1 and chip.get_attribute("href").startswith(TIPBOX_PAGE)


def test_about_tip_line_writes_the_seeded_threshold_as_english_or_french_money_formatted_with_days_for_the_page_language(ui_page):
    """The about tip line fills the threshold amount and days in each page language's pinned money form.

    cov: C-CF-530, C-CF-593, C-CF-594, C-CF-595, C-CF-596, C-CF-597, C-CF-598
    """
    for route, line in (("/about", "Tips of $5.00 or more read new chapters up to 7 days early."),
                        ("/fr/about", "Les pourboires de 5,00 $ ou plus lisent les nouveaux chapitres jusqu'a 7 jours plus tot.")):
        open_route(ui_page, route, wait=2.5)
        ui_page.evaluate("() => window.scrollTo(0, document.scrollingElement.scrollHeight)")
        settle(2.0)
        found = ui_page.evaluate("() => document.body.textContent.replace(/\\u00a0|\\u202f/g, ' ')")
        assert line in found, route


KONAMI = ("ArrowUp", "ArrowUp", "ArrowDown", "ArrowDown", "ArrowLeft", "ArrowRight", "ArrowLeft", "ArrowRight", "b", "a")


def test_surprise_opens_on_the_key_sequence_without_sound_closing_on_escape_overlay_or_navigation_and_stays_off_under_reduced_motion(chromium):
    """The key sequence opens a soundless surprise that traps focus and closes on Escape, overlay or navigation, never under reduced motion.

    cov: C-CF-619, C-CF-620, C-CF-624, C-CF-625, C-CF-626, C-CF-627, C-CF-628, C-CF-629, C-CF-630, C-UX-61
    """
    context = new_context(chromium)
    context.add_init_script("window.__ddAudio = 0; const A = window.AudioContext; if (A) { window.AudioContext = function () "
                            "{ window.__ddAudio += 1; return new A(); }; } HTMLMediaElement.prototype.play = function () "
                            "{ window.__ddAudio += 1; return Promise.resolve(); };")
    tab = context.new_page()
    open_route(tab, "/about", wait=2.0)
    tab.get_by_role("link", name="about").first.focus()
    for key in KONAMI[:5] + ("c",) + KONAMI[5:]:
        tab.keyboard.press(key)
    settle(1.0)
    assert tab.get_by_role("dialog", name="surprise").count() == 0, "a wrong key did not reset the sequence"
    for key in KONAMI:
        tab.keyboard.press(key)
    dialog = tab.get_by_role("dialog", name="surprise")
    assert wait_for(lambda: dialog.count() == 1 and dialog.is_visible(), 5, 0.3)
    for _ in range(4):
        tab.keyboard.press("Tab")
        assert tab.evaluate("() => !!document.activeElement.closest('[role=dialog]')"), "focus left the surprise"
    tab.keyboard.press("Escape")
    settle(1.0)
    assert dialog.count() == 0 or not dialog.is_visible()
    assert tab.evaluate("() => document.activeElement.innerText.trim().toLowerCase()") == "about"
    for key in KONAMI:
        tab.keyboard.press(key)
    assert wait_for(lambda: dialog.count() == 1, 5, 0.3)
    tab.mouse.click(5, tab.viewport_size["height"] - 5)
    settle(1.0)
    assert dialog.count() == 0 or not dialog.is_visible(), "pressing the overlay did not close the surprise"
    open_route(tab, "/", wait=1.5)
    tab.get_by_role("link", name="about").first.click() if tab.get_by_role("link", name="about").count() else None
    settle(1.5)
    for key in KONAMI:
        tab.keyboard.press(key)
    assert wait_for(lambda: dialog.count() == 1, 5, 0.3)
    tab.go_back()
    settle(1.5)
    assert dialog.count() == 0 or not dialog.is_visible(), "navigating away did not close the surprise"
    assert tab.evaluate("() => window.__ddAudio") == 0 and tab.locator("audio, video").count() == 0
    context.close()
    still = new_context(chromium, reduced_motion="reduce")
    tab = still.new_page()
    open_route(tab, "/", wait=2.0)
    for key in KONAMI:
        tab.keyboard.press(key)
    size = tab.viewport_size
    tab.mouse.click(size["width"] / 2, size["height"] * 0.3)
    settle(1.5)
    assert tab.get_by_role("dialog", name="surprise").count() == 0, "the surprise opened under reduced motion"
    still.close()


def test_support_return_page_reads_the_token_and_shows_the_thank_you_line_for_each_status(chromium):
    """The return page shows the sign-in, pending, granted, below-threshold and expired lines for each status.

    cov: C-CF-237, C-CF-239, C-UF-35
    """
    signed_out = new_context(chromium)
    tab = signed_out.new_page()
    open_route(tab, f"/support/return?token={return_token()}", wait=3.0)
    assert CATALOGUE_EN["support.sign_in"] in visible_text(tab) and tab.get_by_role("dialog", name="sign in").is_visible()
    signed_out.close()
    probe = register_reader()
    pending_token, granted_token, small_token = return_token(), return_token(), return_token()
    assert deliver(event_body("tip.received", tip_data(600, token=granted_token))).status_code == 200
    assert deliver(event_body("tip.received", tip_data(200, token=small_token))).status_code == 200
    settle(3.0)
    context = new_context(chromium)
    context.add_init_script(f"try {{ window.localStorage.setItem('dd-session', '{probe['token']}'); }} catch (e) {{}}")
    tab = context.new_page()
    for token_value, key in ((pending_token, "support.pending"), (granted_token, "support.granted"),
                             (small_token, "support.below_threshold"), ("unknown-" + token_hex(), "support.expired")):
        open_route(tab, f"/support/return?token={token_value}", wait=3.0)
        assert CATALOGUE_EN[key] in visible_text(tab), key
    context.close()


def texture_version_of(url: str) -> int:
    return int(urlparse(url).path.split("/")[3].lstrip("v"))


def studio_page(chromium, **options):
    context, tab, token = signed_in_author_page(chromium, **options)
    return context, tab


def test_studio_console_keeps_dd_studio_session_and_shows_skeleton_rows_empty_states_and_the_guided_path(chromium, author):
    """Studio sign-in keeps dd-studio-session; loading shows skeleton rows; empty lists and an empty studio say so.

    cov: C-UF-52, C-UF-53, C-UF-54, C-UF-56, C-UF-57, C-TR-11
    """
    context = new_context(chromium)
    tab = context.new_page()
    open_route(tab, "/studio/sign-in", wait=2.0)
    tab.get_by_label("email").fill(AUTHOR_EMAIL)
    tab.get_by_label("password").fill(SEED_PASSWORD)
    tab.get_by_role("button", name="sign in").click()
    settle(2.5)
    assert tab.evaluate(f"() => localStorage.getItem('{AUTHOR_SESSION_KEY}')"), "the author token is not kept under dd-studio-session"

    def slow_volumes(route):
        settle(3.0)
        route.continue_()

    tab.route(re.compile(r".*/api/studio/volumes(\?.*)?$"), slow_volumes)
    tab.goto(appclient.app_url() + "/studio/volumes", wait_until="domcontentloaded")
    settle(1.0)
    skeletons = tab.evaluate("() => document.querySelectorAll('[aria-busy=true], [class*=skeleton], [data-skeleton]').length")
    assert skeletons > 0, "no skeleton rows while the studio loads"
    assert tab.get_by_role("progressbar").count() == 0 or tab.locator("[class*=spinner]").count() == 0
    tab.unroute(re.compile(r".*/api/studio/volumes(\?.*)?$"))
    tab.route(re.compile(r".*/api/studio/tips(\?.*)?$"),
              lambda route: route.fulfill(status=200, content_type="application/json", body='{"items": [], "next_cursor": null}'))
    open_route(tab, "/studio/supporters", wait=2.5)
    assert re.search(r"\bno\b.*\btips?\b", visible_text(tab), re.I | re.S), "the empty supporter list says nothing"
    tab.route(re.compile(r".*/api/studio/page-views(\?.*)?$"),
              lambda route: route.fulfill(status=200, content_type="application/json", body='{"items": [], "next_cursor": null}'))
    open_route(tab, "/studio/insights", wait=2.5)
    assert re.search(r"\bno\b.*\b(page )?views?\b", visible_text(tab), re.I | re.S), "the empty page-view list says nothing"
    volume = new_volume(author)
    open_route(tab, f"/studio/volumes/{volume['id']}", wait=2.5)
    assert re.search(r"\bno\b.*\bchapters?\b", visible_text(tab), re.I | re.S), "an empty volume says nothing"
    tab.route(re.compile(r".*/api/studio/volumes(\?.*)?$"),
              lambda route: route.fulfill(status=200, content_type="application/json", body="[]"))
    open_route(tab, "/studio", wait=2.5)
    guide = visible_text(tab).lower()
    positions = [guide.find(word) for word in ("volume", "chapter", "board", "import")]
    assert all(p >= 0 for p in positions) and positions == sorted(positions), f"no guided path: {guide[:300]}"
    context.close()


def test_studio_forms_open_modal_dialogs_label_fields_above_errors_beneath_and_title_editor_shows_previous_chapter_titles(chromium, author):
    """Studio create actions open modal dialogs whose labels sit above fields and errors beneath; title editing shows earlier titles.

    cov: C-CF-786, C-UX-64, C-FE-63
    """
    context, tab = studio_page(chromium)
    open_route(tab, "/studio/volumes", wait=2.5)
    tab.get_by_role("button", name="New volume").click()
    dialog = tab.get_by_role("dialog")
    assert dialog.is_visible() and dialog.get_attribute("aria-modal") == "true"
    field = dialog.get_by_role("textbox").first
    label_box = dialog.locator("label").first.bounding_box()
    field_box = field.bounding_box()
    assert label_box["y"] + label_box["height"] <= field_box["y"] + 2, "the label does not sit above its field"
    field.fill("")
    dialog.get_by_role("button", name=re.compile("create|save|add", re.I)).first.click()
    settle(1.0)
    error = dialog.get_by_role("alert").first if dialog.get_by_role("alert").count() else dialog.locator("[id*=error], [class*=error]").first
    assert error.is_visible() and error.bounding_box()["y"] >= field_box["y"] + field_box["height"] - 2
    tab.keyboard.press("Escape")
    settle(0.8)
    assert tab.get_by_role("dialog").count() == 0 or not tab.get_by_role("dialog").is_visible()
    volume = studio_volume(author, 1)
    open_route(tab, f"/studio/volumes/{volume['id']}", wait=2.5)
    tab.get_by_role("button", name="New chapter").click()
    assert tab.get_by_role("dialog").is_visible()
    tab.keyboard.press("Escape")
    chapter = studio_chapter_row(author, 1, 5)
    open_route(tab, f"/studio/chapters/{chapter['id']}", wait=2.5)
    text = visible_text(tab)
    for number in (3, 4):
        assert CHAPTER_TITLES[number][0] in text and CHAPTER_TITLES[number][1] in text, "earlier titles are not shown beside the editor"
    tab.get_by_role("button", name="New board").click()
    assert tab.get_by_role("dialog").is_visible()
    tab.keyboard.press("Escape")
    context.close()


def test_panel_composer_console_edit_saves_at_once_puts_back_rejected_values_with_the_reason_announcing_the_rejected_save_and_shows_both_values_on_a_version_conflict(chromium, author):
    """Composer edits show at once and save; rejected values return with a reason; a version conflict shows both values.

    cov: C-CF-703, C-CF-709, C-CF-710, C-UX-80
    """
    built = build_chapter(author, ready=False)
    board = board_detail(author, built["board"]["id"])
    panel = board["panels"][0]
    context, tab = studio_page(chromium)
    open_route(tab, f"/studio/chapters/{built['chapter']['id']}/panels/{panel['id']}", wait=3.0)
    tab.get_by_text("stage", exact=True).first.click()
    depth = tab.get_by_label(re.compile("^depth$", re.I)).first
    depth.fill("3")
    depth.press("Tab")
    assert depth.input_value() == "3"
    assert wait_for(lambda: float(layers_by_role(author, built["board"]["id"])["stage"]["depth"]) == 3.0, 10)
    depth.fill("11")
    depth.press("Tab")
    settle(2.0)
    assert depth.input_value() in ("3", "3.0"), "a rejected value was not put back"
    assert tab.get_by_text(re.compile("depth", re.I)).count() >= 2, "no reason is stated beneath the field"
    assert "depth" in " ".join(tab.locator("[aria-live=assertive]").all_inner_texts()).lower() or \
        tab.locator("[aria-live=assertive]").count() >= 1
    current = layers_by_role(author, built["board"]["id"])["stage"]
    assert author.patch(f"/studio/layers/{current['id']}", json={"version": current["version"], "depth": 5}).status_code == 200
    depth.fill("-1")
    depth.press("Tab")
    settle(2.5)
    text = visible_text(tab)
    assert "-1" in text and "5" in text, "a version conflict does not show both values"
    assert tab.get_by_role("button", name=re.compile("keep", re.I)).count() >= 1
    context.close()


def test_journey_drawing_to_panel_creates_volume_chapter_board_imports_sets_depth_and_marks_failing_preflight_thumbnails(chromium, author):
    """Journey 8 in the console: create Vol. II, its chapter and board, drop two files, see a two-layer panel, set depth 3.

    cov: C-UF-38, C-UF-39, C-UF-40, C-UF-41, C-FE-55
    """
    context, tab = studio_page(chromium)
    open_route(tab, "/studio/volumes", wait=2.5)
    tab.get_by_role("button", name="New volume").click()
    tab.get_by_role("dialog").get_by_role("textbox").first.fill("Vol. II")
    tab.get_by_role("dialog").get_by_role("button", name=re.compile("create|save|add", re.I)).first.click()
    settle(2.0)
    created = [v for v in author.get("/studio/volumes").json() if v["label"] == "Vol. II"]
    assert created, "the modal did not create Vol. II"
    volume = max(created, key=lambda v: int(v["order"]))
    open_route(tab, f"/studio/volumes/{volume['id']}", wait=2.5)
    tab.get_by_role("button", name="New chapter").click()
    boxes = tab.get_by_role("dialog").get_by_role("textbox")
    boxes.nth(0).fill("the night shift")
    boxes.nth(1).fill("le service de nuit")
    tab.get_by_role("dialog").get_by_role("button", name=re.compile("create|save|add", re.I)).first.click()
    settle(2.0)
    chapter = studio_chapters(author, volume["id"])[0]
    assert chapter["titles"] == {"en": "the night shift", "fr": "le service de nuit"}, chapter
    open_route(tab, f"/studio/chapters/{chapter['id']}", wait=2.5)
    tab.get_by_role("button", name="New board").click()
    if tab.get_by_role("dialog").count():
        tab.get_by_role("dialog").get_by_role("button", name=re.compile("create|save|add", re.I)).first.click()
    settle(2.0)
    board = studio_chapter(author, chapter["id"])["boards"][0]
    open_route(tab, f"/studio/chapters/{chapter['id']}/boards/{board['id']}", wait=2.5)
    tab.locator("input[type=file]").first.set_input_files([
        {"name": "c1b1p1-back.png", "mimeType": "image/png", "buffer": make_png()},
        {"name": "c1b1p1-stage.png", "mimeType": "image/png", "buffer": make_png(rgb=(80, 20, 20))},
    ])
    settle(4.0)
    detail = board_detail(author, board["id"])
    assert len(detail["panels"]) == 1 and len(detail["panels"][0]["layers"]) == 2, detail
    strip = visible_text(tab)
    assert re.search(r"\b2\b", strip), "the filmstrip does not show the layer count"
    warning = tab.locator("[aria-label*=rule i], [title*=rule i], [aria-label*=warning i]")
    assert warning.count() >= 1, "no warning mark for the failing preflight rule"
    panel = detail["panels"][0]
    open_route(tab, f"/studio/chapters/{chapter['id']}/panels/{panel['id']}", wait=3.0)
    tab.get_by_text("stage", exact=True).first.click()
    mark = tab.locator("[aria-label*=stage i][role=slider], [data-role=stage]").first
    before_mark = mark.bounding_box()
    depth = tab.get_by_label(re.compile("^depth$", re.I)).first
    depth.fill("3")
    depth.press("Tab")
    settle(2.0)
    assert mark.bounding_box() != before_mark, "the depth ruler mark did not move"
    assert float(layers_by_role(author, board["id"])["stage"]["depth"]) == 3.0
    context.close()


def test_translation_grid_cell_below_100_percent_opens_the_missing_keys(chromium, author):
    """A coverage grid cell under 100 percent opens its missing keys.

    cov: C-CF-785
    """
    entry = next(e for e in author.get("/studio/translations/fr", params={"namespace": "chrome"}).json()
                 if e["key"] == "chrome.about")
    assert author.put("/studio/translations/fr/chrome.about",
                      json={"value": entry["value"], "state": "untranslated", "note": ""}).status_code == 200
    context, tab = studio_page(chromium)
    try:
        open_route(tab, "/studio/translations", wait=3.0)
        cell = tab.get_by_role("cell", name=re.compile(r"^\d{1,2}(\.\d+)? ?%$")).first
        assert cell.count() == 1, "no cell shows coverage under 100 percent"
        cell.click()
        settle(2.0)
        assert "chrome.about" in visible_text(tab), "the cell did not open its missing keys"
    finally:
        restored = author.put("/studio/translations/fr/chrome.about",
                              json={"value": entry["value"], "state": "reviewed", "note": entry.get("note") or ""})
        context.close()
    assert restored.status_code == 200


def test_rotated_tipbox_secret_refuses_notifications_signed_with_the_previous_secret(author):
    """After rotation a notification signed with the previous secret answers 401; a short secret is rejected by field.

    cov: C-CF-819, C-CF-820, C-CF-821
    """
    field_starts(author.put("/studio/integrations/tipbox/secret", json={"secret": "short-secret"}), "secret")
    fresh_secret = "tbx_whsec_rotated_" + token_hex()
    rotated = author.put("/studio/integrations/tipbox/secret", json={"secret": fresh_secret})
    try:
        assert rotated.status_code == 200 and fresh_secret not in rotated.text, describe(rotated)
        assert rotated.json()["secret_last_four"] == fresh_secret[-4:]
        body = event_body("tip.received", tip_data(300))
        assert deliver(body, signature=sign(body, TIPBOX_SECRET)).status_code == 401
        other = event_body("tip.received", tip_data(300))
        assert deliver(other, signature=sign(other, fresh_secret)).status_code == 200
    finally:
        restored = author.put("/studio/integrations/tipbox/secret", json={"secret": TIPBOX_SECRET})
        assert restored.status_code == 200 and restored.json()["secret_last_four"] == TIPBOX_SECRET_LAST_FOUR


def failed_login(path: str, email: str, password: str) -> httpx.Response:
    return httpx.post(f"{appclient.api_base()}{path}", json={"email": email, "password": password}, timeout=appclient.TIMEOUT)


def test_reader_and_author_login_lock_out_after_ten_failed_sign_ins_matching_wrong_password_and_logout_ends_the_token():
    """Sign-in returns a token, fails identically for unknown addresses, locks out after ten failures, and logout ends the token.

    cov: C-CF-14, C-CF-15, C-CF-16, C-CF-17, C-CF-18, C-CF-19, C-CF-20
    """
    probe = register_reader()
    good = failed_login("/auth/login", probe["email"], probe["password"])
    assert good.status_code == 200 and good.json()["access_token"], describe(good)
    wrong = failed_login("/auth/login", probe["email"], "wrong-password-value")
    unknown = failed_login("/auth/login", probe_email(), "wrong-password-value")
    assert wrong.status_code == unknown.status_code and 400 <= wrong.status_code < 500
    assert error_of(wrong)["code"] == error_of(unknown)["code"] and error_of(wrong)["message"] == error_of(unknown)["message"]
    token_value = good.json()["access_token"]
    with api_client(token_value) as session:
        assert session.post("/auth/logout").status_code in (200, 204)
        for path in ("/me", "/me/progress", "/me/entitlements"):
            assert session.get(path).status_code == 401, path
    for path, email, password in (("/auth/login", probe["email"], probe["password"]),
                                  ("/studio/auth/login", AUTHOR2_EMAIL, SEED_PASSWORD)):
        for _ in range(10):
            assert 400 <= failed_login(path, email, "wrong-password-value").status_code < 500
        locked = failed_login(path, email, password)
        assert locked.status_code == wrong.status_code, f"{email} signed in during a lockout. {describe(locked)}"
        assert error_of(locked)["code"] == error_of(wrong)["code"] and error_of(locked)["message"] == error_of(wrong)["message"]


def test_unpublished_chapter_image_requested_after_expires_answers_404(author, early_signed_image):
    """A signed image address of a scheduled chapter answers 404 once its expires moment has passed.

    cov: C-CF-216
    """
    path, query = image_parts(early_signed_image["url"])
    expires = int(query["expires"])
    version = texture_version_of(early_signed_image["url"])
    assert version == int(settings_of(author)["asset_version"]), "the asset version moved before the expiry check"
    limit = deadline_after(max(0, expires - now_unix()) + 30)
    while now_unix() <= expires + 2 and before(limit):
        settle(5.0)
    assert now_unix() > expires, "the signed address never reached its expires moment"
    assert fetch_absolute(early_signed_image["url"]).status_code == 404, "an expired signed address still opened the image"


def test_console_release_actions_mark_ready_run_preflight_publish_schedule_unpublish_confirming_first_and_raise_the_asset_version_ending_on_full_page_confirmations(chromium, author):
    """Journey 9 and the release actions in the console confirm destructive steps and end on full-page confirmations.

    cov: C-CF-769, C-CF-770, C-CF-771, C-CF-772, C-UF-42, C-UF-43, C-UX-66
    """
    built = build_chapter(author, ready=False)
    chapter_id = built["chapter"]["id"]
    title = built["chapter"]["titles"]["en"]
    context, tab = studio_page(chromium)
    open_route(tab, f"/studio/chapters/{chapter_id}", wait=3.0)
    tab.get_by_role("button", name="Mark ready").click()
    assert wait_for(lambda: chapter_state(author, chapter_id) == "ready", 10)
    tab.get_by_role("button", name="Run preflight").click()
    settle(2.0)
    assert len(re.findall(r"\b(pass|passed|passes)\b", visible_text(tab), re.I)) >= 1
    tab.get_by_role("button", name="Publish now").click()
    settle(2.5)
    assert title in visible_text(tab) and re.search(r"published", visible_text(tab), re.I)
    assert chapter_state(author, chapter_id) == "published"
    open_route(tab, f"/studio/chapters/{chapter_id}", wait=2.5)
    tab.get_by_role("button", name=re.compile("^unpublish", re.I)).click()
    confirm = tab.get_by_role("dialog")
    assert confirm.is_visible() and re.search(r"unpublish", confirm.inner_text(), re.I), "unpublishing did not confirm first"
    confirm.get_by_role("button", name=re.compile("unpublish|confirm", re.I)).first.click()
    settle(2.5)
    assert chapter_state(author, chapter_id) == "unpublished" and re.search(r"unpublished", visible_text(tab), re.I)
    second = build_chapter(author)
    open_route(tab, f"/studio/chapters/{second['chapter']['id']}", wait=2.5)
    tab.get_by_role("button", name=re.compile("^schedule", re.I)).first.click()
    moment = tab.locator("input[type=datetime-local], input[type=date], input[type=text]").first
    moment.fill((utc_now() + datetime.timedelta(days=3)).strftime("%Y-%m-%dT18:00"))
    tab.get_by_role("button", name=re.compile("^schedule|confirm", re.I)).last.click()
    settle(2.5)
    assert chapter_state(author, second["chapter"]["id"]) == "scheduled" and re.search(r"scheduled", visible_text(tab), re.I)
    before = int(settings_of(author)["asset_version"])
    open_route(tab, "/studio/settings", wait=2.5)
    tab.get_by_role("button", name=re.compile("asset version", re.I)).first.click()
    confirm = tab.get_by_role("dialog")
    assert confirm.is_visible(), "raising the asset version did not confirm first"
    confirm.get_by_role("button", name=re.compile("raise|confirm", re.I)).first.click()
    settle(2.5)
    assert int(settings_of(author)["asset_version"]) == before + 1
    assert str(before + 1) in visible_text(tab)
    context.close()


def test_raising_the_asset_version_moves_manifest_addresses_and_retires_old_ones(author):
    """Raising the asset version moves every manifest to the new version's addresses and retires the old ones.

    cov: C-CF-822, C-CF-823, C-CF-824
    """
    old_urls = layer_urls(manifest(1, 1).json())
    before = int(settings_of(author)["asset_version"])
    assert all(texture_version_of(u) == before for u in old_urls)
    assert fetch_absolute(old_urls[0]).status_code == 200
    raised = author.post("/studio/asset-version")
    assert raised.status_code == 200 and int(raised.json()["asset_version"]) == before + 1, describe(raised)
    new_urls = layer_urls(manifest(1, 1).json())
    assert all(texture_version_of(u) == before + 1 for u in new_urls)
    assert fetch_absolute(new_urls[0]).status_code == 200
    assert fetch_absolute(old_urls[0]).status_code == 404, "an old version's address still answers"


def test_audit_records_are_only_added_never_changed_or_removed(backend, audit_snapshot):
    """Every audit record present at the start of the run is still present and unchanged at the end, and more were added.

    cov: C-CF-768
    """
    rows = {str(r["id"]): r for r in backend.query("SELECT * FROM audit_records")}
    for record in audit_snapshot["rows"]:
        kept = rows.get(str(record["id"]))
        assert kept is not None, f"audit record {record['id']} was removed"
        assert kept == record, f"audit record {record['id']} was changed"
    assert len(rows) > len(audit_snapshot["rows"]), "the run's studio mutations added no audit record"
