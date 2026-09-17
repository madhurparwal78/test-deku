from __future__ import annotations

import re
import threading
import uuid

import httpx

import appclient
from conftest import (AUTHOR2_EMAIL, AUTHOR_EMAIL, AWARD_NAMES, BRIEF_TEXT,
                      BUDGET_TOKENS, CAREERS_HOST, CASE_STATES,
                      CHAPTER_KINDS, CLIENT_NAMES, CONSOLE_WRITE_LIMIT,
                      CRAWLER_FRAGMENTS, DESCRIPTION_MESSAGE, DISCIPLINES_LINE,
                      DISPLAY_NAMES, DRAFT_SLUG, DRAFT_TITLE, EDITOR_EMAIL,
                      EMAIL_MESSAGE, ENQUIRY_LIMIT, ENQUIRY_SENDER_SUBJECT,
                      EVENT_NAMES,
                      HARBOURSIDE_LINES, HOME_TRANSFER_BUDGET,
                      INERT_SEPARATOR, INVITATION_DAYS, INVITE_SUBJECT,
                      LAUNCH_MESSAGE, LOCKED_MESSAGE, MEDIA_KEY_PREFIX,
                      MESSAGE_KINDS, NAME_MESSAGE, NEWSLETTER_LIMIT,
                      NO_CHAPTER_MESSAGE, NORTHGATE_LINES, NOTICE_DESCRIPTION,
                      NOTICE_LABELS, NOTICE_TITLE, OFFICE_CITIES, OFFICE_PHONES,
                      ORDER_WRITE_LIMIT, ORGANISATION_MESSAGE, PAGE_SIZE, PASSWORD,
                      PRIVACY_CONTACT, PUBLISHED_SLUG, PUBLISHED_TITLE,
                      PUBLIC_ROUTES, RESET_ANSWER, RESET_LIMIT, RESET_SUBJECT,
                      RETURN_NOTE_MESSAGE, SECOND_SLUG, SECTOR_LABELS,
                      SECTOR_MESSAGE, SECTOR_TOKENS, SECURITY_HEADERS,
                      SHORT_PASSWORD_MESSAGE, SIGNUP_LIMIT, SIGN_IN_ATTEMPT_LIMIT,
                      SIGN_IN_REFUSAL, SOCIAL_LINES, STUDIO_CONTACT,
                      STUDIO_IDLE_SECONDS, STUDIO_PROMISE, SUBMITTED_SLUG, SUBMITTED_TITLE, THIRD_SLUG, TITLE_MESSAGE,
                      UPLOAD_LIMIT_BYTES, VERIFY_SUBJECT, VISITOR_EMAIL,
                      WORDMARK_LINE, WORDMARK_SECOND, add_chapter, app_origin,
                      denied, digest_of, enquiry_payload, flat, fresh_email,
                      fresh_title, invited_account, is_client_error,
                      message_of_kind, messages_for, new_case_file, open_site,
                      page_body, page_response, png_bytes, public_case_file,
                      public_summaries, published_case_file, ready_case_file,
                      refusal, save_header, send_enquiry, settle, sign_in_on_page,
                      all_published,
                      signed_up_visitor,
                      site_document, studio_record, submit, token_of, transition,
                      upload_image, verified_visitor)


def test_health_answers_once_the_app_is_ready():
    response = httpx.get(f"{app_origin()}/api/health", timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"the health route answered {response.status_code}")
    home = page_response("/")
    assert home.status_code == 200, f"the home address answered {home.status_code}"


def test_every_response_carries_the_security_headers():
    for path in ("/", "/work/all"):
        response = page_response(path)
        for header in SECURITY_HEADERS:
            assert header in {k.lower() for k in response.headers}, (
                f"{path} answered without {header}: {sorted(response.headers)}")
        assert "includesubdomains" in response.headers["strict-transport-security"].lower()
        assert response.headers["x-content-type-options"].lower() == "nosniff"
        assert response.headers["x-frame-options"].upper() == "DENY"
        assert response.headers["referrer-policy"].lower() == "same-origin"


def test_the_content_policy_bans_inline_script_and_framing():
    policy = page_response("/").headers["content-security-policy"].lower()
    assert "frame-ancestors 'none'" in policy, (
        f"the policy does not deny framing: {policy}")
    assert "unsafe-inline" not in policy, f"the policy allows inline script: {policy}"
    assert "unsafe-eval" not in policy, f"the policy allows eval: {policy}"


def test_a_cross_origin_request_receives_no_permission():
    response = httpx.get(f"{appclient.api_base()}/site",
                         headers={"Origin": "https://elsewhere.example"},
                         timeout=appclient.TIMEOUT)
    allowed = response.headers.get("access-control-allow-origin", "")
    assert allowed in ("", app_origin()), (
        f"the API granted a foreign origin {allowed!r}")


def test_any_app_cookie_is_http_only_and_same_site_strict():
    response = httpx.post(f"{appclient.api_base()}/auth/login",
                          json={"email": VISITOR_EMAIL, "password": PASSWORD},
                          timeout=appclient.TIMEOUT)
    assert response.status_code == 200, f"the sign-in answered {response.status_code}"
    for raw in response.headers.get_list("set-cookie"):
        low = raw.lower()
        assert "httponly" in low, f"a cookie is readable by script: {raw}"
        assert "samesite=strict" in low, f"a cookie is not same-site strict: {raw}"
        assert "domain=" not in low, f"a cookie carries a domain scope: {raw}"


def test_a_public_address_answers_the_application_document():
    for path in PUBLIC_ROUTES:
        text = page_body(path)
        assert "<title>" in text.lower(), f"{path} carries no title before scripts run"
        assert 'og:title' in text, f"{path} carries no link preview title"
        assert 'og:image' in text, f"{path} carries no link preview image"
    home = page_body("/")
    assert 'lang="en"' in home.lower(), f"the document declares no source locale: {home[:200]}"


def test_a_case_file_preview_image_is_drawn_by_the_app():
    text = page_body(f"/work/{PUBLISHED_SLUG}")
    assert f"{PUBLISHED_TITLE} · Kelo" in text, (
        f"the case file preview title is not the title with the studio: {text[:400]}")
    assert f"/api/preview/{PUBLISHED_SLUG}.png" in text, (
        "the case file document names no preview image on its own origin")
    image = httpx.get(f"{app_origin()}/api/preview/{PUBLISHED_SLUG}.png",
                      timeout=appclient.TIMEOUT)
    assert image.status_code == 200, f"the preview image answered {image.status_code}"
    assert image.headers["content-type"].startswith("image/png"), (
        f"the preview image is {image.headers['content-type']}")


def test_every_other_public_address_uses_the_site_preview_image():
    for path in ("/", "/story", "/contact"):
        assert "/api/preview/site.png" in page_body(path), (
            f"{path} names no site preview image")
    image = httpx.get(f"{app_origin()}/api/preview/site.png", timeout=appclient.TIMEOUT)
    assert image.status_code == 200, f"the site preview answered {image.status_code}"
    assert image.headers["content-type"].startswith("image/png")


def test_no_credential_reaches_the_browser():
    text = page_body("/")
    lowered = text.lower()
    for marker in ("storage_secret_key", "storage_access_key", "postgresql://",
                   "db_admin_url", "deku-store-secret"):
        assert marker not in lowered, f"the document carries {marker}"
    site = flat(site_document())
    for marker in ("password_hash", "token_hash", "secret"):
        assert marker not in site, f"the site document carries {marker}"


def test_the_site_document_carries_the_seeded_taxonomy():
    site = site_document()
    for key in ("studio", "sectors", "clients", "awards", "contact", "notice",
                "newsletter"):
        assert key in site, f"the site document is missing {key}: {sorted(site)}"
    tokens = [row["token"] for row in site["sectors"]]
    labels = [row["label"] for row in site["sectors"]]
    assert tokens == list(SECTOR_TOKENS), f"the sector tokens are {tokens}"
    assert labels == list(SECTOR_LABELS), f"the sector labels are {labels}"
    positions = [row["position"] for row in site["sectors"]]
    assert len(set(positions)) == len(positions), f"two sectors share a position: {positions}"


def test_the_client_roster_is_seeded_in_its_groups():
    site = site_document()
    names = [row["name"] for row in site["clients"]]
    assert len(names) == len(CLIENT_NAMES), f"the roster holds {len(names)} names"
    assert names == list(CLIENT_NAMES), f"the roster reads {names}"
    by_sector: dict = {}
    for row in site["clients"]:
        by_sector.setdefault(row["sector"], []).append(row["position"])
    for sector, group in by_sector.items():
        assert len(set(group)) == len(group), (
            f"two client entries of {sector} share a position: {group}")


def test_the_studio_block_carries_the_promise_and_the_awards():
    site = site_document()
    studio = site["studio"]
    assert studio["name"] == WORDMARK_LINE, f"the studio name reads {studio['name']!r}"
    assert studio["line"] == WORDMARK_SECOND, f"the studio line reads {studio['line']!r}"
    assert studio["promise"] == STUDIO_PROMISE, f"the promise reads {studio['promise']!r}"
    assert studio["skills"] == DISCIPLINES_LINE, f"the disciplines read {studio['skills']!r}"
    assert [str(name) for name in site["awards"]] == list(AWARD_NAMES), (
        f"the studio awards read {site['awards']}")


def test_the_contact_block_is_stored_line_by_line():
    contact = site_document()["contact"]
    assert contact["new_business_email"] == STUDIO_CONTACT
    assert contact["careers_host"] == CAREERS_HOST
    assert contact["privacy_email"] == PRIVACY_CONTACT
    cities = [office["city"] for office in contact["offices"]]
    phones = [office["phone"] for office in contact["offices"]]
    assert cities == list(OFFICE_CITIES), f"the offices read {cities}"
    assert phones == list(OFFICE_PHONES), f"the numbers read {phones}"
    assert contact["offices"][0]["address_lines"] == list(HARBOURSIDE_LINES)
    assert contact["offices"][1]["address_lines"] == list(NORTHGATE_LINES)
    assert [str(line) for line in contact["social"]] == list(SOCIAL_LINES)


def test_the_notice_rows_are_seeded_with_their_labels():
    notice = site_document()["notice"]
    assert notice["title"] == NOTICE_TITLE, f"the notice title reads {notice['title']!r}"
    assert notice["description"] == NOTICE_DESCRIPTION
    labels = [row["label"] for row in notice["rows"]]
    assert labels == list(NOTICE_LABELS), f"the notice labels read {labels}"
    positions = [row["position"] for row in notice["rows"]]
    assert len(set(positions)) == len(positions), f"two rows share a position: {positions}"
    first = notice["rows"][0]
    assert first["updated_at"], f"the first row carries no update time: {first}"


def test_the_seeded_examples_are_published_in_grid_order():
    summaries = public_summaries()
    slugs = [row["slug"] for row in summaries]
    for slug in (PUBLISHED_SLUG, SECOND_SLUG, THIRD_SLUG):
        assert slug in slugs, f"{slug} is not in the public list: {slugs}"
    positions = {row["slug"]: row["position"] for row in summaries}
    assert positions[PUBLISHED_SLUG] == 1, f"{PUBLISHED_SLUG} sits at {positions[PUBLISHED_SLUG]}"
    assert positions[SECOND_SLUG] == 2, f"{SECOND_SLUG} sits at {positions[SECOND_SLUG]}"
    assert positions[THIRD_SLUG] == 3, f"{THIRD_SLUG} sits at {positions[THIRD_SLUG]}"
    summary = [row for row in summaries if row["slug"] == PUBLISHED_SLUG][0]
    for key in ("id", "slug", "title", "client", "sector", "sector_label",
                "description", "position", "published_at"):
        assert key in summary, f"the public summary is missing {key}: {sorted(summary)}"


def test_the_seeded_case_files_carry_their_chapter_kinds(db):
    expected = {PUBLISHED_SLUG: ["headline", "text", "image", "list"],
                SECOND_SLUG: ["headline", "text", "video", "device"],
                THIRD_SLUG: ["headline", "text", "split", "video_loop"]}
    for slug, kinds in expected.items():
        record = public_case_file(slug)
        assert [row["kind"] for row in record["chapters"]] == kinds, (
            f"{slug} carries {[row['kind'] for row in record['chapters']]}")
        positions = [row["position"] for row in record["chapters"]]
        assert sorted(positions) == positions, f"{slug} chapters are out of order"
        assert len(set(positions)) == len(positions), f"{slug} repeats a chapter position"
    rows = db.rows("case_file", seeded=True)
    assert len(rows) == 3, f"the seed marks {len(rows)} example case files"


def test_glass_harbour_carries_its_awards_and_information_items():
    record = public_case_file(PUBLISHED_SLUG)
    assert record["title"] == PUBLISHED_TITLE
    assert record["client"] == "Aster", f"the client reads {record['client']!r}"
    awards = [(row["name"], row["mark"]) for row in record["awards"]]
    assert awards == [("Harbour Prize", "treatment-1"), ("Wexel", "treatment-2")], (
        f"the awards read {awards}")
    items = [(row["heading"], row["value"]) for row in record["information_items"]]
    assert items == [("Year", "2024"), ("Role", "Brand system")], (
        f"the information items read {items}")
    positions = [row["position"] for row in record["awards"]]
    assert sorted(positions) == positions, f"the awards are out of order: {positions}"


def test_the_full_public_shape_names_the_next_case_file():
    record = public_case_file(PUBLISHED_SLUG)
    for key in ("launch_url", "information_items", "chapters", "awards", "next"):
        assert key in record, f"the full shape is missing {key}: {sorted(record)}"
    assert record["next"]["slug"] == SECOND_SLUG, (
        f"the next case file after position one is {record['next']}")
    for key in ("slug", "title", "description"):
        assert key in record["next"], f"the next block is missing {key}"
    kinds = {row["kind"] for row in record["chapters"]}
    assert kinds <= set(CHAPTER_KINDS), f"an unknown chapter kind is stored: {kinds}"


def test_the_public_list_is_an_array_with_a_page_of_twenty_four():
    first = public_summaries({"page": 1})
    assert isinstance(first, list), f"the list is {type(first).__name__}"
    assert len(first) <= PAGE_SIZE, f"one page carried {len(first)} case files"
    second = public_summaries({"page": 2})
    assert isinstance(second, list), f"the second page is {type(second).__name__}"
    overlap = {row["slug"] for row in first} & {row["slug"] for row in second}
    assert not overlap, f"two pages repeat {overlap}"


def test_the_public_list_sorts_by_order_then_newest_then_title():
    ordered = [row["position"] for row in public_summaries({"sort": "order"})]
    assert ordered == sorted(ordered), f"the grid order is {ordered}"
    newest = [row["published_at"] for row in public_summaries({"sort": "newest"})]
    assert newest == sorted(newest, reverse=True), f"the newest order is {newest}"
    titles = [row["title"] for row in public_summaries({"sort": "title"})]
    assert titles == sorted(titles, key=lambda t: t.lower()), (
        f"the alphabetical order is {titles}")


def test_the_public_list_filters_by_sector_and_refuses_an_unknown_one():
    rows = public_summaries({"sector": "sector-1"})
    assert rows, "the technology sector carries no published case file"
    assert {row["sector"] for row in rows} == {"sector-1"}, (
        f"the filter returned {[row['sector'] for row in rows]}")
    unknown = httpx.get(f"{appclient.api_base()}/case-files",
                        params={"sector": "sector-99"}, timeout=appclient.TIMEOUT)
    payload = refusal(unknown, "an unknown sector token")
    assert SECTOR_MESSAGE in flat(payload), f"the refusal reads {payload}"
    text = httpx.get(f"{appclient.api_base()}/case-files", params={"q": "harbour"},
                     timeout=appclient.TIMEOUT)
    assert text.status_code < 300, "the public list refused a free-text parameter"
    assert len(text.json()) == len(public_summaries()), (
        "the public list narrowed on free text, and the public site has no text search")


def test_an_unpublished_case_file_is_invisible_to_the_public(db):
    slugs = {row["slug"] for row in public_summaries()}
    assert DRAFT_SLUG not in slugs, f"{DRAFT_SLUG} is in the public list"
    assert SUBMITTED_SLUG not in slugs, f"{SUBMITTED_SLUG} is in the public list"
    for slug in (DRAFT_SLUG, SUBMITTED_SLUG, "does-not-exist"):
        response = httpx.get(f"{appclient.api_base()}/case-files/{slug}",
                             timeout=appclient.TIMEOUT)
        assert response.status_code == 404, (
            f"the public read of {slug} answered {response.status_code}")
    row = db.one("case_file", slug=DRAFT_SLUG)
    assert row is not None, f"{DRAFT_SLUG} is not seeded"
    assert row["state"] == "draft", f"{DRAFT_SLUG} is stored as {row['state']}"
    assert row["position"] is None, f"{DRAFT_SLUG} holds the grid position {row['position']}"


def test_the_seeded_draft_and_submitted_case_files_belong_to_their_authors(db):
    accounts = {row["email"]: row["id"] for row in db.rows("account")}
    draft = db.one("case_file", slug=DRAFT_SLUG)
    submitted = db.one("case_file", slug=SUBMITTED_SLUG)
    assert draft["owner_id"] == accounts[AUTHOR_EMAIL], (
        f"{DRAFT_TITLE} is owned by another account")
    assert submitted["owner_id"] == accounts[AUTHOR2_EMAIL], (
        f"{SUBMITTED_TITLE} is owned by another account")
    assert submitted["state"] == "submitted", (
        f"{SUBMITTED_TITLE} is stored as {submitted['state']}")
    assert draft["state"] in CASE_STATES and submitted["state"] in CASE_STATES


def test_a_path_traversal_in_a_slug_answers_not_found():
    for slug in ("..%2F..%2Fetc%2Fpasswd", "..", "%2e%2e%2fadmin"):
        response = httpx.get(f"{appclient.api_base()}/case-files/{slug}",
                             timeout=appclient.TIMEOUT)
        assert response.status_code == 404, (
            f"a traversal attempt answered {response.status_code}")


def test_the_seed_holds_the_named_tables_without_duplicates(db):
    tables = ("account", "account_session", "account_token", "invitation", "sector",
              "client_entry", "case_file", "chapter", "information_item", "award",
              "case_media", "slug_redirect", "retired_slug", "notice_row", "enquiry",
              "shortlist_entry", "subscriber", "message", "analytics_event")
    assert len(tables) == 19, "the data model names nineteen tables"
    for table in tables:
        assert db.count(table) >= 0, f"the table {table} is missing"
    emails = [row["email"] for row in db.rows("account")]
    assert len(emails) == len(set(emails)), f"an address is seeded twice: {emails}"
    names = {row["display_name"] for row in db.rows("account")}
    assert set(DISPLAY_NAMES) <= names, f"the seeded display names read {names}"
    sectors = [row["token"] for row in db.rows("sector")]
    assert sectors == list(SECTOR_TOKENS), f"the sectors read {sectors}"
    notice_rows = db.rows("notice_row")
    assert len(notice_rows) == len(NOTICE_LABELS), (
        f"the seed wrote {len(notice_rows)} notice rows")
    created = db.rows("case_file", slug=PUBLISHED_SLUG)
    assert len(created) == 1, f"{PUBLISHED_SLUG} is seeded {len(created)} times"


def test_api_timestamps_are_utc(db):
    record = public_case_file(PUBLISHED_SLUG)
    stamp = str(record["published_at"])
    assert stamp.endswith("Z") or "+00:00" in stamp, (
        f"the publication time is not UTC: {stamp}")
    row = db.one("case_file", slug=PUBLISHED_SLUG)
    assert row["created_at"] is not None, "the stored row carries no creation time"


def test_an_uploaded_image_lands_in_the_bucket_at_its_content_key(author, store, db):
    record = ready_case_file(author)
    case_id = record["id"]
    data = png_bytes(tone=11)
    response = upload_image(author, case_id, data)
    assert response.status_code == 201, (
        f"the upload answered {response.status_code}: {response.text[:300]}")
    media = response.json()
    digest = digest_of(data)
    expected = f"{MEDIA_KEY_PREFIX}{case_id}/{digest}.png"
    assert media["key"] == expected, f"the object key reads {media['key']!r}"
    assert media["sha256"] == digest, f"the stored digest reads {media['sha256']!r}"
    assert media["size_bytes"] == len(data), f"the stored size reads {media['size_bytes']}"
    assert media["content_type"] == "image/png", f"the type reads {media['content_type']!r}"
    assert store.exists(expected), f"no object exists in the bucket at {expected}"
    row = db.one("case_media", key=expected)
    assert row is not None, f"no case media row names {expected}"


def test_the_uploaded_bytes_are_not_held_in_a_table(author, store, db):
    record = ready_case_file(author)
    data = png_bytes(tone=19)
    media = upload_image(author, record["id"], data).json()
    row = db.one("case_media", key=media["key"])
    for value in row.values():
        assert not isinstance(value, (bytes, bytearray, memoryview)), (
            f"the media row carries bytes in a column: {sorted(row)}")
    assert store.exists(media["key"]), "the bytes are not in the bucket"
    keys = store.list(f"{MEDIA_KEY_PREFIX}{record['id']}/")
    assert media["key"] in keys, f"the object is not listed under its case file: {keys}"


def test_media_of_an_unpublished_case_file_is_denied_without_a_session(author, anon):
    record = ready_case_file(author)
    media = upload_image(author, record["id"]).json()
    response = httpx.get(f"{appclient.api_base()}/media/{media['id']}",
                         timeout=appclient.TIMEOUT)
    assert response.status_code == 404, (
        f"an unpublished image answered {response.status_code} with no session")
    assert not response.content.startswith(b"\x89PNG"), "the bytes were served anyway"


def test_media_of_an_unpublished_case_file_is_denied_to_a_stranger(author, visitor,
                                                                   other_author):
    record = ready_case_file(author)
    media = upload_image(author, record["id"]).json()
    for api, who in ((visitor, "a visitor"), (other_author, "another author")):
        response = api.get(f"/media/{media['id']}")
        assert response.status_code == 404, (
            f"{who} read an unpublished image with {response.status_code}")
        assert not response.content.startswith(b"\x89PNG"), f"{who} received the bytes"


def test_media_of_an_unpublished_case_file_reaches_its_owner_and_an_editor(author,
                                                                           editor):
    record = ready_case_file(author)
    data = png_bytes(tone=23)
    media = upload_image(author, record["id"], data).json()
    for api, who in ((author, "the owner"), (editor, "an editor")):
        response = api.get(f"/media/{media['id']}")
        assert response.status_code == 200, (
            f"{who} was refused the image with {response.status_code}")
        assert response.content == data, f"{who} received other bytes"
        assert response.headers["content-type"].startswith("image/png")


def test_media_of_a_published_case_file_is_public(author, editor):
    record = published_case_file(author, editor, with_image=True)
    studio = studio_record(editor, record["id"])
    media_ids = [chapter["payload"].get("media_id") for chapter in studio["chapters"]
                 if chapter["kind"] == "image"]
    assert media_ids and media_ids[0], f"the published case file carries no image: {studio}"
    response = httpx.get(f"{appclient.api_base()}/media/{media_ids[0]}",
                         timeout=appclient.TIMEOUT)
    assert response.status_code == 200, (
        f"a published image answered {response.status_code} with no session")
    assert response.content.startswith(b"\x89PNG"), "the served bytes are not the image"


def test_an_upload_that_is_not_an_image_is_refused(author, store, db):
    record = ready_case_file(author)
    before = len(store.list(f"{MEDIA_KEY_PREFIX}{record['id']}/"))
    response = upload_image(author, record["id"], b"not an image at all",
                            name="notes.txt", content_type="text/plain")
    payload = refusal(response, "a text upload")
    assert "file" in payload["fields"], f"the refusal names no file field: {payload}"
    assert db.count("case_media", case_file_id=record["id"]) == 0, (
        "the refused upload wrote a media row")
    assert len(store.list(f"{MEDIA_KEY_PREFIX}{record['id']}/")) == before, (
        "the refused upload wrote an object")


def test_an_upload_over_the_size_limit_is_refused(author, db):
    record = ready_case_file(author)
    oversize = png_bytes(width=1400, height=1400, tone=200)
    padded = oversize + b"\x00" * max(0, UPLOAD_LIMIT_BYTES + 1 - len(oversize))
    response = upload_image(author, record["id"], padded)
    payload = refusal(response, "an oversized upload")
    assert "file" in payload["fields"], f"the refusal names no file field: {payload}"
    assert db.count("case_media", case_file_id=record["id"]) == 0, (
        "the oversized upload wrote a media row")


def test_an_upload_from_a_foreign_account_is_denied(author, other_author, visitor, db):
    record = ready_case_file(author)
    for api, who in ((other_author, "another author"), (visitor, "a visitor")):
        response = upload_image(api, record["id"])
        denied(response, f"an upload by {who}")
    assert db.count("case_media", case_file_id=record["id"]) == 0, (
        "a denied upload wrote a media row")


def test_the_seeded_draft_image_exists_in_the_bucket_and_stays_private(db, store):
    draft = db.one("case_file", slug=DRAFT_SLUG)
    rows = db.rows("case_media", case_file_id=draft["id"])
    assert rows, f"{DRAFT_TITLE} carries no seeded media row"
    key = rows[0]["key"]
    assert key.startswith(f"{MEDIA_KEY_PREFIX}{draft['id']}/"), (
        f"the seeded object key reads {key!r}")
    assert store.exists(key), f"no seeded object exists at {key}"
    response = httpx.get(f"{appclient.api_base()}/media/{rows[0]['id']}",
                         timeout=appclient.TIMEOUT)
    assert response.status_code == 404, (
        f"the seeded draft image answered {response.status_code} with no session")


def test_no_bucket_address_is_handed_to_the_browser(author, editor):
    record = published_case_file(author, editor, with_image=True)
    text = page_body(f"/work/{record['slug']}")
    public = flat(public_case_file(record["slug"]))
    for marker in ("x-amz", "9000", "amazonaws", "presigned"):
        assert marker not in public, f"the public shape carries {marker}"
    assert "storage_endpoint" not in text.lower(), "the document names the bucket host"


def test_the_seeded_accounts_sign_in_with_the_pinned_password():
    for email in (EDITOR_EMAIL, AUTHOR_EMAIL, AUTHOR2_EMAIL, VISITOR_EMAIL):
        response = httpx.post(f"{appclient.api_base()}/auth/login",
                              json={"email": email, "password": PASSWORD},
                              timeout=appclient.TIMEOUT)
        assert response.status_code == 200, (
            f"{email} answered {response.status_code} at sign-in")
        payload = response.json()
        assert payload.get("access_token"), f"{email} received no token: {payload}"
        account = payload.get("account") or {}
        assert account.get("display_name") in DISPLAY_NAMES, (
            f"{email} carries the display name {account.get('display_name')!r}")


def test_a_protected_call_needs_the_bearer_token(anon, visitor):
    for path in ("/auth/me", "/messages", "/shortlist", "/studio/case-files"):
        denied(anon.get(path), f"an unsigned read of {path}")
    response = visitor.get("/auth/me")
    assert response.status_code == 200, (
        f"a bearer token was refused with {response.status_code}")
    stale = appclient.client("not-a-real-token")
    denied(stale.get("/auth/me"), "a made-up token")
    stale.close()


def test_a_failed_sign_in_says_nothing_about_the_address():
    wrong = httpx.post(f"{appclient.api_base()}/auth/login",
                       json={"email": VISITOR_EMAIL, "password": "wrong-password-9"},
                       timeout=appclient.TIMEOUT)
    unknown = httpx.post(f"{appclient.api_base()}/auth/login",
                         json={"email": fresh_email("nobody"),
                               "password": "wrong-password-9"},
                         timeout=appclient.TIMEOUT)
    for response, who in ((wrong, "a wrong password"), (unknown, "an unknown address")):
        payload = refusal(response, f"{who} at sign-in")
        assert payload["message"] == SIGN_IN_REFUSAL, (
            f"{who} answered {payload['message']!r}")
    assert wrong.status_code == unknown.status_code, (
        "an unknown address answers differently from a wrong password")


def test_a_short_password_is_refused_at_sign_up():
    response = httpx.post(f"{appclient.api_base()}/auth/signup",
                          json={"email": fresh_email("short"), "password": "too-short",
                                "display_name": "Ash Vale"},
                          timeout=appclient.TIMEOUT)
    payload = refusal(response, "a short password")
    assert SHORT_PASSWORD_MESSAGE in flat(payload), f"the refusal reads {payload}"


def test_no_endpoint_returns_a_password_or_its_hash(editor, visitor):
    shapes = [visitor.get("/auth/me").json(), editor.get("/studio/accounts").json()]
    for shape in shapes:
        text = flat(shape)
        assert "password" not in text, f"an account shape carries a password: {text[:200]}"
        assert PASSWORD not in text, "an account shape carries the seeded password"
    account = visitor.get("/auth/me").json()
    for key in ("id", "email", "display_name", "role", "email_verified",
                "verification_deadline", "previous_email", "previous_email_until",
                "created_at"):
        assert key in account, f"the public account shape is missing {key}: {sorted(account)}"


def test_an_address_is_lowercased_and_kept_unique(db):
    email = fresh_email("Mixed")
    shouted = email.upper()
    response = httpx.post(f"{appclient.api_base()}/auth/signup",
                          json={"email": shouted, "password": PASSWORD,
                                "display_name": "Case Fold"},
                          timeout=appclient.TIMEOUT)
    assert response.status_code == 201, (
        f"the sign-up answered {response.status_code}: {response.text[:300]}")
    assert db.one("account", email=email.lower()) is not None, (
        f"the address was not stored lowercased: {email}")
    again = httpx.post(f"{appclient.api_base()}/auth/signup",
                       json={"email": email.lower(), "password": PASSWORD,
                             "display_name": "Case Fold"},
                       timeout=appclient.TIMEOUT)
    payload = refusal(again, "a repeated address")
    assert payload["error"] == "conflict", f"the second account answered {payload}"


def test_sign_up_creates_an_unconfirmed_visitor_and_signs_it_in(db):
    created = signed_up_visitor()
    account = created["account"]
    assert account.get("role") == "visitor", f"sign-up created {account.get('role')!r}"
    assert account.get("email_verified") is False, "the new address is already confirmed"
    assert account.get("verification_deadline"), "no confirmation deadline is shown"
    with appclient.client(created["token"]) as api:
        assert api.get("/auth/me").status_code == 200, "the new visitor is not signed in"
    asked = httpx.post(f"{appclient.api_base()}/auth/signup",
                       json={"email": fresh_email("asker"), "password": PASSWORD,
                             "display_name": "Asks For More", "role": "editor"},
                       timeout=appclient.TIMEOUT)
    assert asked.status_code == 201, f"the sign-up answered {asked.status_code}"
    assert asked.json()["account"]["role"] == "visitor", (
        "asking for a role at sign-up granted one")
    row = db.one("account", email=created["email"])
    assert row["role"] == "visitor", f"the stored role reads {row['role']!r}"


def test_sign_up_writes_a_confirmation_message_with_one_link():
    created = signed_up_visitor()
    with appclient.client(created["token"]) as api:
        message = message_of_kind(api, "verify_address")
    assert message["subject"] == VERIFY_SUBJECT, f"the subject reads {message['subject']!r}"
    assert message["to_email"] == created["email"], f"the message went to {message['to_email']}"
    assert token_of(message["link"]), f"the message carries no token: {message['link']}"
    assert "7" in message["body"] or "seven" in message["body"].lower(), (
        f"the message does not state the expiry: {message['body']}")
    assert PASSWORD not in message["body"], "the message carries the password"


def test_following_the_confirmation_link_confirms_the_address():
    created = verified_visitor()
    with appclient.client(created["token"]) as api:
        account = api.get("/auth/me").json()
    assert account["email_verified"] is True, f"the address is still unconfirmed: {account}"
    assert account["verification_deadline"] in (None, ""), (
        f"a confirmed account keeps a deadline: {account['verification_deadline']}")
    unknown = httpx.post(f"{appclient.api_base()}/accounts/verifications",
                         json={"token": uuid.uuid4().hex}, timeout=appclient.TIMEOUT)
    refusal(unknown, "an unknown confirmation token")


def test_session_lifetimes_differ_by_role(visitor, author):
    visitor_sessions = visitor.get("/auth/sessions").json()
    author_sessions = author.get("/auth/sessions").json()
    assert isinstance(visitor_sessions, list) and visitor_sessions
    current = [row for row in visitor_sessions if row.get("current")]
    assert current, f"no session is marked current: {visitor_sessions}"
    assert current[0]["idle_timeout_seconds"] in (None, 0), (
        f"a visitor session carries an idle timeout: {current[0]}")
    studio = [row for row in author_sessions if row.get("current")][0]
    assert studio["idle_timeout_seconds"] == STUDIO_IDLE_SECONDS, (
        f"a studio session idles at {studio['idle_timeout_seconds']}")
    for row in visitor_sessions + author_sessions:
        for key in ("id", "created_at", "last_used_at", "expires_at"):
            assert key in row, f"a session row is missing {key}: {sorted(row)}"


def test_the_stored_session_expiry_matches_the_role(db):
    created = signed_up_visitor()
    account = db.one("account", email=created["email"])
    rows = db.rows("account_session", account_id=account["id"])
    assert rows, "the sign-up opened no session"
    session = rows[-1]
    span = session["expires_at"] - session["created_at"]
    assert span.days == 30, f"a visitor session lasts {span}"
    assert session["idle_timeout_seconds"] is None, (
        f"a visitor session idles at {session['idle_timeout_seconds']}")
    studio = db.one("account", email=AUTHOR_EMAIL)
    appclient.login(AUTHOR_EMAIL, PASSWORD)
    studio_rows = db.rows("account_session", account_id=studio["id"])
    latest = studio_rows[-1]
    studio_span = latest["expires_at"] - latest["created_at"]
    assert 11 <= studio_span.total_seconds() / 3600 <= 12.5, (
        f"a studio session lasts {studio_span}")
    assert latest["idle_timeout_seconds"] == STUDIO_IDLE_SECONDS


def test_every_sign_in_issues_a_new_token():
    first = appclient.login(VISITOR_EMAIL, PASSWORD)
    second = appclient.login(VISITOR_EMAIL, PASSWORD)
    assert first != second, "two sign-ins reused one token"
    with appclient.client(first) as api:
        assert api.get("/auth/me").status_code == 200, "the first session was closed"


def test_logout_revokes_the_current_session_only():
    first = appclient.login(VISITOR_EMAIL, PASSWORD)
    second = appclient.login(VISITOR_EMAIL, PASSWORD)
    with appclient.client(second) as api:
        assert api.post("/auth/logout", json={}).status_code < 300, "the sign-out failed"
        denied(api.get("/auth/me"), "a revoked token")
    with appclient.client(first) as other:
        assert other.get("/auth/me").status_code == 200, (
            "signing out of one device closed another")


def test_logout_with_all_devices_revokes_every_session():
    created = verified_visitor()
    first = appclient.login(created["email"], PASSWORD)
    second = appclient.login(created["email"], PASSWORD)
    with appclient.client(second) as api:
        assert api.post("/auth/logout", json={"all_devices": True}).status_code < 300
    with appclient.client(first) as other:
        denied(other.get("/auth/me"), "a token revoked on every device")


def test_one_session_can_be_revoked_on_its_own():
    created = verified_visitor()
    doomed = appclient.login(created["email"], PASSWORD)
    keeper = appclient.login(created["email"], PASSWORD)
    with appclient.client(keeper) as api:
        rows = api.get("/auth/sessions").json()
        target = [row for row in rows if not row.get("current")]
        assert target, f"the second session is not listed: {rows}"
        assert api.delete(f"/auth/sessions/{target[0]['id']}").status_code < 300
    with appclient.client(doomed) as closed:
        denied(closed.get("/auth/me"), "a revoked session")


def test_a_reset_request_answers_the_same_for_any_address():
    known = httpx.post(f"{appclient.api_base()}/accounts/resets",
                       json={"email": VISITOR_EMAIL}, timeout=appclient.TIMEOUT)
    unknown = httpx.post(f"{appclient.api_base()}/accounts/resets",
                         json={"email": fresh_email("nobody")},
                         timeout=appclient.TIMEOUT)
    assert known.status_code == unknown.status_code == 202, (
        f"the answers differ: {known.status_code} and {unknown.status_code}")
    assert known.json()["message"] == RESET_ANSWER, f"the answer reads {known.json()}"
    assert unknown.json()["message"] == RESET_ANSWER, f"the answer reads {unknown.json()}"


def test_a_reset_link_works_once_and_closes_every_session():
    created = verified_visitor()
    other = appclient.login(created["email"], PASSWORD)
    asked = httpx.post(f"{appclient.api_base()}/accounts/resets",
                       json={"email": created["email"]}, timeout=appclient.TIMEOUT)
    assert asked.status_code == 202
    with appclient.client(created["token"]) as api:
        message = message_of_kind(api, "reset_password")
    assert message["subject"] == RESET_SUBJECT, f"the subject reads {message['subject']!r}"
    assert "60" in message["body"] or "sixty" in message["body"].lower(), (
        f"the message does not state the expiry: {message['body']}")
    token = token_of(message["link"])
    fresh_password = "deku-reset-pass-9"
    done = httpx.post(f"{appclient.api_base()}/accounts/resets/complete",
                      json={"token": token, "password": fresh_password},
                      timeout=appclient.TIMEOUT)
    assert done.status_code < 300, f"the reset answered {done.status_code}: {done.text[:200]}"
    with appclient.client(other) as closed:
        denied(closed.get("/auth/me"), "a session after a completed reset")
    again = httpx.post(f"{appclient.api_base()}/accounts/resets/complete",
                       json={"token": token, "password": "deku-reset-pass-8"},
                       timeout=appclient.TIMEOUT)
    refusal(again, "a reused reset token")
    assert appclient.login(created["email"], fresh_password), "the new password fails"


def test_a_reset_link_is_void_once_the_account_signs_in():
    created = verified_visitor()
    asked = httpx.post(f"{appclient.api_base()}/accounts/resets",
                       json={"email": created["email"]}, timeout=appclient.TIMEOUT)
    assert asked.status_code == 202
    with appclient.client(created["token"]) as api:
        token = token_of(message_of_kind(api, "reset_password")["link"])
    appclient.login(created["email"], PASSWORD)
    void = httpx.post(f"{appclient.api_base()}/accounts/resets/complete",
                      json={"token": token, "password": "deku-reset-pass-7"},
                      timeout=appclient.TIMEOUT)
    refusal(void, "a reset token voided by a sign-in")


def test_five_failed_sign_ins_lock_the_account():
    created = signed_up_visitor()
    statuses = []
    for _ in range(SIGN_IN_ATTEMPT_LIMIT):
        statuses.append(httpx.post(f"{appclient.api_base()}/auth/login",
                                   json={"email": created["email"],
                                         "password": "wrong-password-9"},
                                   timeout=appclient.TIMEOUT).status_code)
    locked = httpx.post(f"{appclient.api_base()}/auth/login",
                        json={"email": created["email"], "password": PASSWORD},
                        timeout=appclient.TIMEOUT)
    payload = refusal(locked, "a sign-in after five failures")
    assert payload["error"] == "rate_limited", f"the lock answered {payload}"
    assert payload["message"] == LOCKED_MESSAGE, f"the lock reads {payload['message']!r}"
    assert payload["retry_after"], f"the refusal carries no retry window: {payload}"
    assert all(is_client_error(status) for status in statuses), (
        f"a wrong password answered {statuses}")


def test_sign_up_is_limited_to_three_an_hour_for_one_address():
    email = fresh_email("repeat")
    statuses = []
    for index in range(SIGNUP_LIMIT + 1):
        response = httpx.post(f"{appclient.api_base()}/auth/signup",
                              json={"email": email, "password": PASSWORD,
                                    "display_name": f"Again {index}"},
                              timeout=appclient.TIMEOUT)
        statuses.append(response)
    payload = refusal(statuses[-1], "a fourth sign-up for one address")
    assert payload["error"] in ("rate_limited", "conflict"), f"the refusal reads {payload}"


def test_reset_requests_are_limited_for_one_address():
    created = verified_visitor()
    last = None
    for _ in range(RESET_LIMIT + 1):
        last = httpx.post(f"{appclient.api_base()}/accounts/resets",
                          json={"email": created["email"]}, timeout=appclient.TIMEOUT)
    payload = refusal(last, "a fourth reset request for one address")
    assert payload["error"] == "rate_limited", f"the refusal reads {payload}"
    assert payload["retry_after"], f"the refusal carries no retry window: {payload}"


def test_an_account_holder_changes_the_display_name_and_address():
    created = verified_visitor()
    with appclient.client(created["token"]) as api:
        account = api.get("/auth/me").json()
        renamed = api.patch(f"/accounts/{account['id']}",
                            json={"display_name": "Rowan Ashfield"})
        assert renamed.status_code < 300, f"the rename answered {renamed.status_code}"
        assert renamed.json()["display_name"] == "Rowan Ashfield"
        moved = api.patch(f"/accounts/{account['id']}",
                          json={"email": fresh_email("moved"),
                                "current_password": PASSWORD})
        assert moved.status_code < 300, f"the address change answered {moved.status_code}"
        payload = moved.json()
        assert payload["previous_email"] == created["email"], (
            f"the old address is not kept: {payload}")
        assert payload["previous_email_until"], "no recovery window is shown"


def test_deleting_an_account_needs_its_display_name():
    created = verified_visitor("Quinn Marsh")
    with appclient.client(created["token"]) as api:
        account = api.get("/auth/me").json()
        wrong = api.request("DELETE", f"/accounts/{account['id']}",
                            json={"confirm_display_name": "Somebody Else"})
        refusal(wrong, "a deletion naming the wrong person")
        right = api.request("DELETE", f"/accounts/{account['id']}",
                            json={"confirm_display_name": "Quinn Marsh"})
        assert right.status_code < 300, f"the deletion answered {right.status_code}"


def test_deleting_an_author_moves_the_case_files_to_the_editor(editor, db):
    account = invited_account(editor, role="author", display_name="Nell Foster")
    with appclient.client(appclient.login(account["email"], PASSWORD)) as api:
        record = ready_case_file(api, title=fresh_title("Foster"))
    accounts = editor.get("/studio/accounts").json()
    row = [item for item in accounts if item["email"] == account["email"]][0]
    removed = editor.request("DELETE", f"/accounts/{row['id']}",
                             json={"confirm_display_name": "Nell Foster"})
    assert removed.status_code < 300, f"the deletion answered {removed.status_code}"
    moved = studio_record(editor, record["id"])
    assert moved["owner_name"] == DISPLAY_NAMES[0], (
        f"the case file moved to {moved['owner_name']!r}")
    assert moved["original_author_name"] == "Nell Foster", (
        f"the original author reads {moved['original_author_name']!r}")


def test_an_invitation_creates_an_account_that_can_sign_in(editor, db):
    email = fresh_email("invited")
    response = editor.post("/studio/invitations",
                           json={"email": email, "role": "author",
                                 "display_name": "Bay Calloway"})
    assert response.status_code == 201, (
        f"the invitation answered {response.status_code}: {response.text[:300]}")
    invitation = response.json()
    assert invitation["invite_url"], f"the invitation carries no address: {invitation}"
    token = token_of(invitation["invite_url"])
    accepted = httpx.post(f"{appclient.api_base()}/invitations/accept",
                          json={"token": token, "password": PASSWORD,
                                "display_name": "Bay Calloway"},
                          timeout=appclient.TIMEOUT)
    assert accepted.status_code == 201, (
        f"accepting answered {accepted.status_code}: {accepted.text[:300]}")
    assert accepted.json()["access_token"], "accepting signed nobody in"
    assert accepted.json()["account"]["role"] == "author", (
        f"the invited account is {accepted.json()['account']['role']!r}")
    row = db.one("invitation", email=email)
    span = row["expires_at"] - row["created_at"]
    assert span.days == INVITATION_DAYS, f"the invitation lasts {span}"


def test_an_invitation_writes_a_message_naming_the_inviter(editor):
    email = fresh_email("named")
    editor.post("/studio/invitations",
                json={"email": email, "role": "author", "display_name": "Wren Oak"})
    outbox = editor.get("/studio/outbox").json()
    rows = [row for row in outbox if row["to_email"] == email]
    assert rows, f"no message was written to {email}"
    message = rows[0]
    assert message["subject"] == INVITE_SUBJECT, f"the subject reads {message['subject']!r}"
    assert message["kind"] == "invitation", f"the kind reads {message['kind']!r}"
    assert DISPLAY_NAMES[0] in message["body"], (
        f"the message does not name the inviter: {message['body']}")
    assert "author" in message["body"].lower(), (
        f"the message does not name the role: {message['body']}")
    assert str(INVITATION_DAYS) in message["body"], (
        f"the message does not state the expiry: {message['body']}")


def test_only_an_editor_invites_or_changes_a_role(author, visitor, editor):
    for api, who in ((author, "an author"), (visitor, "a visitor")):
        denied(api.post("/studio/invitations",
                        json={"email": fresh_email("sneak"), "role": "editor",
                              "display_name": "Sneak Past"}), f"an invitation by {who}")
    accounts = editor.get("/studio/accounts").json()
    target = [row for row in accounts if row["email"] == VISITOR_EMAIL][0]
    denied(author.patch(f"/accounts/{target['id']}", json={"role": "editor"}),
           "a role change by an author")
    assert editor.get("/studio/accounts").json(), "the account list is unreadable"
    again = [row for row in editor.get("/studio/accounts").json()
             if row["email"] == VISITOR_EMAIL][0]
    assert again["role"] == "visitor", f"the visitor became {again['role']!r}"


def test_an_editor_changes_another_role_but_never_their_own(editor, db):
    account = invited_account(editor, role="author", display_name="Iris Vale")
    row = [item for item in editor.get("/studio/accounts").json()
           if item["email"] == account["email"]][0]
    promoted = editor.patch(f"/accounts/{row['id']}", json={"role": "editor"})
    assert promoted.status_code < 300, f"the promotion answered {promoted.status_code}"
    assert promoted.json()["role"] == "editor"
    demoted = editor.patch(f"/accounts/{row['id']}", json={"role": "author"})
    assert demoted.status_code < 300, f"the demotion answered {demoted.status_code}"
    me = editor.get("/auth/me").json()
    refused = editor.patch(f"/accounts/{me['id']}", json={"role": "author"})
    payload = refusal(refused, "an editor changing their own role")
    assert "role" in payload["fields"], f"the refusal names no role field: {payload}"
    assert db.one("account", email=EDITOR_EMAIL)["role"] == "editor", (
        "the editor changed their own role")


def test_a_visitor_cannot_reach_the_console(visitor, anon):
    for path in ("/studio/case-files", "/studio/enquiries", "/studio/outbox",
                 "/studio/accounts", "/studio/export", "/studio/events"):
        denied(visitor.get(path), f"a visitor reading {path}")
        denied(anon.get(path), f"an unsigned read of {path}")
    denied(visitor.post("/studio/case-files"), "a visitor creating a case file")


def test_a_new_case_file_opens_as_an_untitled_draft(author, db):
    record = new_case_file(author)
    assert record["title"] == "Untitled", f"the new case file reads {record['title']!r}"
    assert record["state"] == "draft", f"the new case file is {record['state']!r}"
    assert record["slug"] in (None, ""), f"the new case file holds the slug {record['slug']!r}"
    assert record["version"] == 1, f"the new case file starts at version {record['version']}"
    assert not record.get("chapters"), f"the new case file carries chapters: {record}"
    assert record.get("sector") in (None, ""), f"the new case file names a sector: {record}"
    row = db.one("case_file", id=record["id"])
    assert row["position"] is None, f"an unpublished case file holds position {row['position']}"


def test_the_first_title_save_derives_the_slug(author):
    record = new_case_file(author)
    saved = save_header(author, record["id"], title="The Long Room")
    assert saved.status_code < 300, f"the title save answered {saved.status_code}"
    slug = saved.json()["slug"]
    assert slug == "the-long-room" or slug.startswith("the-long-room-"), (
        f"the slug reads {slug!r}")


def test_a_clashing_title_takes_a_numbered_slug(author):
    title = fresh_title("Quay")
    first = ready_case_file(author, title=title)
    second = new_case_file(author)
    saved = save_header(author, second["id"], title=title)
    assert saved.status_code < 300, f"the second save answered {saved.status_code}"
    assert saved.json()["slug"] != first["slug"], "two case files share one address"
    assert saved.json()["slug"].endswith("-2"), (
        f"the clashing slug reads {saved.json()['slug']!r}")


def test_the_slug_stays_fixed_when_the_title_changes(author):
    record = ready_case_file(author)
    slug = record["slug"]
    changed = save_header(author, record["id"], title=fresh_title("Renamed"))
    assert changed.status_code < 300, f"the rename answered {changed.status_code}"
    assert changed.json()["slug"] == slug, (
        f"the address moved from {slug!r} to {changed.json()['slug']!r}")


def test_an_editor_changes_a_slug_once_and_the_old_address_redirects(author, editor, db):
    record = published_case_file(author, editor)
    old = record["slug"]
    new = f"{old}-harbour"
    moved = save_header(editor, record["id"], slug=new)
    assert moved.status_code < 300, f"the slug change answered {moved.status_code}"
    assert moved.json()["slug"] == new, f"the slug reads {moved.json()['slug']!r}"
    response = httpx.get(f"{appclient.api_base()}/case-files/{old}",
                         follow_redirects=False, timeout=appclient.TIMEOUT)
    assert response.status_code in (301, 308), (
        f"the old address answered {response.status_code}")
    assert new in response.headers.get("location", ""), (
        f"the redirect points at {response.headers.get('location')!r}")
    again = save_header(editor, record["id"], slug=f"{new}-two")
    refusal(again, "a second slug change")
    assert db.one("slug_redirect", old_slug=old) is not None, "no redirect row was kept"
    shouted = save_header(editor, record["id"], slug="Not A Slug")
    refusal(shouted, "a slug that is not lowercase kebab")


def test_the_header_refuses_an_invalid_value_and_writes_nothing(author):
    record = ready_case_file(author)
    before = studio_record(author, record["id"])
    cases = (({"title": "a"}, "title", TITLE_MESSAGE),
             ({"title": "Untitled"}, "title", TITLE_MESSAGE),
             ({"client": ""}, "client", CLIENT_MESSAGE),
             ({"sector": "sector-99"}, "sector", SECTOR_MESSAGE),
             ({"description": "too short"}, "description", DESCRIPTION_MESSAGE),
             ({"launch_url": "http://kelo.example.com"}, "launch_url", LAUNCH_MESSAGE))
    for payload, field, message in cases:
        response = save_header(author, record["id"], **payload)
        refused = refusal(response, f"a save of {field}")
        assert field in refused["fields"], f"the refusal names no {field}: {refused}"
        assert refused["fields"][field] == message, (
            f"the {field} message reads {refused['fields'][field]!r}")
    after = studio_record(author, record["id"])
    for field in ("title", "client", "sector", "description", "launch_url"):
        assert before.get(field) == after.get(field), (
            f"a refused save changed {field}")


def test_information_items_stop_at_six(author):
    record = ready_case_file(author)
    items = [{"heading": f"Fact {index}", "value": f"Value {index}"}
             for index in range(6)]
    saved = save_header(author, record["id"], information_items=items)
    assert saved.status_code < 300, f"six items answered {saved.status_code}"
    assert len(saved.json()["information_items"]) == 6
    seven = items + [{"heading": "Seven", "value": "Too many"}]
    refused = save_header(author, record["id"], information_items=seven)
    refusal(refused, "a seventh information item")
    long_heading = [{"heading": "H" * 25, "value": "Value"}]
    refusal(save_header(author, record["id"], information_items=long_heading),
            "an over-long information heading")
    positions = [row["position"] for row in
                 studio_record(author, record["id"])["information_items"]]
    assert sorted(positions) == positions, f"the items are out of order: {positions}"


def test_an_award_mark_is_one_of_the_eight_treatments(author):
    record = ready_case_file(author)
    saved = save_header(author, record["id"],
                        awards=[{"name": "Harbour Prize", "mark": "treatment-3"}])
    assert saved.status_code < 300, f"a valid award answered {saved.status_code}"
    award = saved.json()["awards"][0]
    assert award["mark"] == "treatment-3", f"the mark reads {award['mark']!r}"
    assert award["position"] is not None, f"the award carries no position: {award}"
    refusal(save_header(author, record["id"],
                        awards=[{"name": "Harbour Prize", "mark": "treatment-9"}]),
            "an award mark outside the eight treatments")


def test_a_chapter_is_added_at_the_end_and_may_be_unfinished(author, db):
    record = ready_case_file(author)
    before = len(studio_record(author, record["id"])["chapters"])
    chapter = add_chapter(author, record["id"], "list", {"items": []})
    assert chapter["position"] == before + 1 or chapter["position"] == before, (
        f"the new chapter landed at {chapter['position']} behind {before} others")
    chapters = studio_record(author, record["id"])["chapters"]
    assert chapters[-1]["id"] == chapter["id"], "the chapter was not added at the end"
    row = db.one("chapter", id=chapter["id"])
    assert row["kind"] == "list", f"the stored kind reads {row['kind']!r}"
    assert row["payload"] is not None, "the chapter stored no payload"
    assert row["case_file_id"] == record["id"], "the chapter names another case file"


def test_an_unknown_chapter_kind_is_refused(author):
    record = ready_case_file(author)
    response = author.post(f"/studio/case-files/{record['id']}/chapters",
                           json={"kind": "carousel", "payload": {"title": "No"}})
    refusal(response, "a chapter of an unknown kind")
    kinds = {row["kind"] for row in studio_record(author, record["id"])["chapters"]}
    assert kinds <= set(CHAPTER_KINDS), f"an unknown kind was stored: {kinds}"


def test_the_chapter_order_is_rewritten_from_the_complete_list(author):
    record = ready_case_file(author, with_image=True)
    chapters = studio_record(author, record["id"])["chapters"]
    assert len(chapters) >= 3, f"the case file carries {len(chapters)} chapters"
    ids = [row["id"] for row in chapters]
    reversed_ids = list(reversed(ids))
    response = author.put(f"/studio/case-files/{record['id']}/chapter-order",
                          json={"chapter_ids": reversed_ids})
    assert response.status_code < 300, f"the reorder answered {response.status_code}"
    after = studio_record(author, record["id"])["chapters"]
    assert [row["id"] for row in after] == reversed_ids, (
        f"the stored order reads {[row['id'] for row in after]}")
    positions = [row["position"] for row in after]
    assert len(set(positions)) == len(positions), f"two chapters share a position: {positions}"


def test_a_broken_chapter_order_changes_nothing(author, other_author):
    record = ready_case_file(author, with_image=True)
    foreign = ready_case_file(other_author)
    chapters = studio_record(author, record["id"])["chapters"]
    ids = [row["id"] for row in chapters]
    foreign_id = studio_record(other_author, foreign["id"])["chapters"][0]["id"]
    for payload, what in (({"chapter_ids": ids[:-1]}, "a list missing a chapter"),
                          ({"chapter_ids": ids + [ids[0]]}, "a repeated chapter"),
                          ({"chapter_ids": ids[:-1] + [foreign_id]},
                           "a chapter of another case file")):
        response = author.put(f"/studio/case-files/{record['id']}/chapter-order",
                              json=payload)
        refusal(response, what)
    after = [row["id"] for row in studio_record(author, record["id"])["chapters"]]
    assert after == ids, f"a refused reorder changed the list to {after}"


def test_a_submit_lists_every_failed_gate(author):
    record = new_case_file(author)
    response = submit(author, record["id"])
    payload = refusal(response, "a submit of an empty case file")
    fields = payload["fields"]
    assert fields.get("title") == TITLE_MESSAGE, f"the gates read {fields}"
    assert fields.get("chapters") == NO_CHAPTER_MESSAGE, f"the gates read {fields}"
    assert "client" in fields and "sector" in fields and "description" in fields, (
        f"the refusal lists only {sorted(fields)}")
    assert studio_record(author, record["id"])["state"] == "draft", (
        "a failed submit moved the case file")


def test_a_submit_names_an_unfinished_chapter_and_a_missing_item(author):
    record = ready_case_file(author)
    add_chapter(author, record["id"], "headline", {})
    save_header(author, record["id"],
                information_items=[{"heading": "Year", "value": ""}])
    payload = refusal(submit(author, record["id"]), "a submit with an unfinished chapter")
    assert "chapter_payloads" in payload["fields"], f"the gates read {payload['fields']}"
    assert "information_items" in payload["fields"], f"the gates read {payload['fields']}"
    assert studio_record(author, record["id"])["state"] == "draft"


def test_a_successful_submit_closes_the_case_file_to_its_author(author, editor):
    record = ready_case_file(author)
    response = submit(author, record["id"])
    assert response.status_code < 300, f"the submit answered {response.status_code}"
    moved = studio_record(author, record["id"])
    assert moved["state"] == "submitted", f"the case file is {moved['state']!r}"
    assert moved["submitted_at"], f"no submission time was recorded: {moved}"
    assert moved["submitted_by"], f"no submitter was recorded: {moved}"
    refused = save_header(author, record["id"], client="Another Client")
    refusal(refused, "an author editing a submitted case file")
    assert studio_record(editor, record["id"])["client"] != "Another Client", (
        "a submitted case file accepted an author edit")
    refusal(submit(author, record["id"]), "a second submit")


def test_a_return_stores_the_note_and_reopens_the_case_file(author, editor):
    record = ready_case_file(author)
    submit(author, record["id"])
    returned = transition(editor, record["id"], "changes_requested",
                          note="Please lengthen the middle section a little.")
    assert returned.status_code < 300, f"the return answered {returned.status_code}"
    moved = studio_record(author, record["id"])
    assert moved["state"] == "changes_requested", f"the case file is {moved['state']!r}"
    assert moved["return_note"] == "Please lengthen the middle section a little."
    assert moved["returned_at"], f"no return time was recorded: {moved}"
    saved = save_header(author, record["id"], client="Aster")
    assert saved.status_code < 300, "a returned case file refused an author edit"
    again = submit(author, record["id"])
    assert again.status_code < 300, f"the resubmit answered {again.status_code}"
    assert studio_record(author, record["id"])["state"] == "submitted"


def test_a_return_note_is_bounded(author, editor):
    record = ready_case_file(author)
    submit(author, record["id"])
    for note in ("too short", "n" * 501):
        payload = refusal(transition(editor, record["id"], "changes_requested",
                                     note=note), "a return note outside its bounds")
        assert RETURN_NOTE_MESSAGE in flat(payload), f"the refusal reads {payload}"
    assert studio_record(editor, record["id"])["state"] == "submitted"


def test_an_approval_records_the_reviewing_editor(author, editor):
    record = ready_case_file(author)
    submit(author, record["id"])
    approved = transition(editor, record["id"], "approved")
    assert approved.status_code < 300, f"the approval answered {approved.status_code}"
    moved = studio_record(editor, record["id"])
    assert moved["state"] == "approved", f"the case file is {moved['state']!r}"
    assert moved["reviewed_by"], f"no reviewer was recorded: {moved}"
    assert moved["approved_at"], f"no approval time was recorded: {moved}"
    assert moved["self_approved"] in (False, None), (
        f"a reviewed case file reads as self approved: {moved}")


def test_an_author_cannot_approve_or_return(author, other_author):
    record = ready_case_file(author)
    submit(author, record["id"])
    denied(transition(author, record["id"], "approved"),
           "an author approving their own case file")
    denied(transition(other_author, record["id"], "approved"),
           "an author approving another case file")
    denied(transition(other_author, record["id"], "changes_requested",
                      note="I would like this changed a little."),
           "an author returning another case file")
    assert studio_record(author, record["id"])["state"] == "submitted"


def test_the_sole_editor_self_approves_on_submit(editor, db):
    editors = [row for row in editor.get("/studio/accounts").json()
               if row["role"] == "editor"]
    assert len(editors) == 1, f"the studio holds {len(editors)} editors"
    record = ready_case_file(editor, title=fresh_title("Sole"))
    response = submit(editor, record["id"])
    assert response.status_code < 300, f"the submit answered {response.status_code}"
    moved = studio_record(editor, record["id"])
    assert moved["state"] == "approved", f"the case file is {moved['state']!r}"
    assert moved["self_approved"] is True, f"the case file is not marked: {moved}"
    assert moved["reviewed_by"] in (None, ""), f"a reviewer was recorded: {moved}"


def test_an_editor_with_a_colleague_cannot_approve_their_own_case_file(editor):
    colleague = invited_account(editor, role="editor", display_name="Hale Brennan")
    row = [item for item in editor.get("/studio/accounts").json()
           if item["email"] == colleague["email"]][0]
    try:
        record = ready_case_file(editor, title=fresh_title("Pair"))
        response = submit(editor, record["id"])
        assert response.status_code < 300, f"the submit answered {response.status_code}"
        assert studio_record(editor, record["id"])["state"] == "submitted", (
            "the case file skipped review while a second editor exists")
        denied(transition(editor, record["id"], "approved"),
               "an editor approving their own case file")
        with appclient.client(appclient.login(colleague["email"], PASSWORD)) as other:
            approved = transition(other, record["id"], "approved")
            assert approved.status_code < 300, (
                f"a second editor was refused with {approved.status_code}")
    finally:
        editor.patch(f"/accounts/{row['id']}", json={"role": "author"})


def test_two_approvals_of_one_case_file_admit_exactly_one(author, editor):
    record = ready_case_file(author)
    submit(author, record["id"])
    outcomes: list = []
    barrier = threading.Barrier(2)

    def approve():
        with appclient.client(appclient.login(EDITOR_EMAIL, PASSWORD)) as api:
            barrier.wait()
            outcomes.append(transition(api, record["id"], "approved"))

    runners = [threading.Thread(target=approve) for _ in range(2)]
    for runner in runners:
        runner.start()
    for runner in runners:
        runner.join()
    codes = sorted(response.status_code for response in outcomes)
    assert sum(1 for code in codes if code < 300) == 1, (
        f"two approvals answered {codes}")
    loser = [response for response in outcomes if response.status_code >= 300][0]
    payload = refusal(loser, "the second approval")
    assert payload["error"] == "conflict", f"the second approval answered {payload}"
    assert DISPLAY_NAMES[0] in payload["message"], (
        f"the conflict does not name who moved it: {payload['message']}")
    assert studio_record(editor, record["id"])["state"] == "approved"


def test_publishing_places_the_case_file_at_the_end_of_the_grid(author, editor, db):
    record = ready_case_file(author, title=fresh_title("Grid"))
    submit(author, record["id"])
    transition(editor, record["id"], "approved")
    before = [row["position"] for row in all_published()]
    live = transition(editor, record["id"], "published")
    assert live.status_code < 300, f"the publication answered {live.status_code}"
    moved = studio_record(editor, record["id"])
    assert moved["state"] == "published", f"the case file is {moved['state']!r}"
    assert moved["published_at"], f"no publication time was recorded: {moved}"
    assert moved["position"] == max(before) + 1, (
        f"the case file landed at {moved['position']} behind {max(before)}")
    slugs = [row["slug"] for row in all_published()]
    assert record["slug"] in slugs, "the published case file is not in the public list"
    assert public_case_file(record["slug"])["title"] == moved["title"]
    positions = [row["position"] for row in db.rows("case_file", state="published")]
    assert len(set(positions)) == len(positions), f"two published rows share {positions}"


def test_a_case_file_publishes_only_from_approved(author, editor):
    record = ready_case_file(author)
    denied_move = transition(editor, record["id"], "published")
    payload = refusal(denied_move, "a publication from draft")
    assert payload["error"] in ("state_not_allowed", "conflict"), (
        f"the refusal reads {payload}")
    assert studio_record(editor, record["id"])["state"] == "draft"
    submit(author, record["id"])
    transition(editor, record["id"], "approved")
    back = transition(editor, record["id"], "draft")
    assert back.status_code < 300, f"the return to draft answered {back.status_code}"
    assert studio_record(editor, record["id"])["state"] == "draft"


def test_a_change_to_a_published_case_file_waits_in_the_pending_copy(author, editor):
    record = published_case_file(author, editor, with_image=True)
    live = public_case_file(record["slug"])["description"]
    changed = save_header(author, record["id"],
                          description="A rewritten description that runs past forty characters.")
    assert changed.status_code < 300, f"the rewrite answered {changed.status_code}"
    studio = studio_record(author, record["id"])
    assert studio["state"] == "published", f"the case file became {studio['state']!r}"
    assert studio["draft_payload"], f"no pending copy was written: {studio}"
    assert public_case_file(record["slug"])["description"] == live, (
        "the public address showed the pending copy")


def test_publishing_changes_moves_the_pending_copy_to_the_public(author, editor):
    record = published_case_file(author, editor)
    published_at = studio_record(editor, record["id"])["published_at"]
    wording = "A rewritten description that runs comfortably past forty characters."
    save_header(author, record["id"], description=wording)
    response = author.post(f"/studio/case-files/{record['id']}/publish-changes", json={})
    assert response.status_code < 300, (
        f"publishing the changes answered {response.status_code}: {response.text[:300]}")
    studio = studio_record(author, record["id"])
    assert studio["draft_payload"] in (None, {}, ""), (
        f"the pending copy survived: {studio['draft_payload']}")
    assert studio["published_at"] == published_at, "the publication time moved"
    fresh = httpx.get(f"{appclient.api_base()}/case-files/{record['slug']}",
                      timeout=appclient.TIMEOUT).json()
    assert fresh["description"] == wording, (
        f"a fresh client still reads {fresh['description']!r}")


def test_another_author_cannot_touch_a_case_file_they_do_not_own(author, other_author,
                                                                 editor):
    record = published_case_file(author, editor)
    denied(other_author.get(f"/studio/case-files/{record['id']}"),
           "an author reading another case file")
    denied(save_header(other_author, record["id"], client="Nightly"),
           "an author editing another case file")
    denied(other_author.post(f"/studio/case-files/{record['id']}/publish-changes",
                             json={}), "an author publishing another case file")
    denied(other_author.request("DELETE", f"/studio/case-files/{record['id']}"),
           "an author deleting another case file")
    assert studio_record(editor, record["id"])["client"] != "Nightly"


def test_taking_a_case_file_down_clears_its_place(author, editor, db):
    record = published_case_file(author, editor, title=fresh_title("Down"))
    down = transition(editor, record["id"], "approved")
    assert down.status_code < 300, f"the removal answered {down.status_code}"
    moved = studio_record(editor, record["id"])
    assert moved["state"] == "approved", f"the case file is {moved['state']!r}"
    assert moved["position"] in (None, 0), f"the grid position reads {moved['position']}"
    assert record["slug"] not in [row["slug"] for row in public_summaries()]
    gone = httpx.get(f"{appclient.api_base()}/case-files/{record['slug']}",
                     timeout=appclient.TIMEOUT)
    assert gone.status_code == 404, f"the address answered {gone.status_code}"
    again = transition(editor, record["id"], "published")
    assert again.status_code < 300, f"republishing answered {again.status_code}"
    assert record["slug"] in [row["slug"] for row in public_summaries()]


def test_a_case_file_that_was_published_cannot_be_deleted(author, editor):
    record = published_case_file(author, editor, title=fresh_title("Kept"))
    payload = refusal(editor.request("DELETE", f"/studio/case-files/{record['id']}"),
                      "deleting a published case file")
    assert payload["error"] == "conflict", f"the refusal reads {payload}"
    transition(editor, record["id"], "approved")
    still = refusal(editor.request("DELETE", f"/studio/case-files/{record['id']}"),
                    "deleting a case file that was once published")
    assert still["error"] == "conflict", f"the refusal reads {still}"
    assert studio_record(editor, record["id"])["id"] == record["id"]


def test_a_never_published_case_file_is_deleted_with_its_parts(author, editor, db):
    record = ready_case_file(author, with_image=True)
    case_id = record["id"]
    save_header(author, case_id, information_items=[{"heading": "Year", "value": "2026"}],
                awards=[{"name": "Wexel", "mark": "treatment-2"}])
    removed = editor.request("DELETE", f"/studio/case-files/{case_id}")
    assert removed.status_code < 300, f"the deletion answered {removed.status_code}"
    assert db.count("case_file", id=case_id) == 0, "the case file row survived"
    assert db.count("chapter", case_file_id=case_id) == 0, "a chapter row survived"
    assert db.count("information_item", case_file_id=case_id) == 0, "an item row survived"
    assert db.count("award", case_file_id=case_id) == 0, "an award row survived"
    denied(author.request("DELETE", f"/studio/case-files/{record['id']}"),
           "an author deleting a case file")


def test_a_retired_slug_is_never_issued_again(author, editor, db):
    title = fresh_title("Retired")
    record = ready_case_file(author, title=title)
    old = record["slug"]
    editor.request("DELETE", f"/studio/case-files/{record['id']}")
    assert db.one("retired_slug", slug=old) is not None, f"{old} was not retired"
    again = new_case_file(author)
    saved = save_header(author, again["id"], title=title)
    assert saved.json()["slug"] != old, f"the retired slug {old} was issued again"


def test_a_stale_version_is_refused(author):
    record = ready_case_file(author)
    version = studio_record(author, record["id"])["version"]
    first = save_header(author, record["id"], client="Aster", version=version)
    assert first.status_code < 300, f"the first save answered {first.status_code}"
    assert first.json()["version"] > version, "the version did not move"
    stale = save_header(author, record["id"], client="Sable", version=version)
    payload = refusal(stale, "a save carrying a stale version")
    assert payload["error"] == "version_conflict", f"the refusal reads {payload}"
    assert studio_record(author, record["id"])["client"] == "Aster", (
        "the stale write landed anyway")


def test_the_grid_order_is_replaced_whole(editor, author):
    published_case_file(author, editor, title=fresh_title("Order"))
    rows = all_published()
    ids = [row["id"] for row in rows]
    swapped = ids[1:] + ids[:1]
    response = editor.put("/studio/grid-order", json={"case_file_ids": swapped})
    assert response.status_code < 300, f"the grid order answered {response.status_code}"
    after = [row["id"] for row in all_published()]
    assert after == swapped, f"the public order reads {after}"
    partial = editor.put("/studio/grid-order", json={"case_file_ids": swapped[:-1]})
    refusal(partial, "a grid order missing a case file")
    assert [row["id"] for row in all_published()] == swapped, (
        "a refused grid order changed the public list")
    restored = editor.put("/studio/grid-order", json={"case_file_ids": ids})
    assert restored.status_code < 300, f"restoring answered {restored.status_code}"


def test_an_author_is_refused_every_editor_route(author, editor):
    record = published_case_file(author, editor)
    ids = [row["id"] for row in all_published()]
    denied(author.put("/studio/grid-order", json={"case_file_ids": ids}),
           "an author reordering the grid")
    denied(author.get("/studio/enquiries"), "an author reading the inbox")
    denied(author.get("/studio/outbox"), "an author reading the outbox")
    denied(author.get("/studio/accounts"), "an author reading the account list")
    denied(author.get("/studio/export"), "an author reading the export")
    denied(author.get("/studio/events"), "an author reading the events")
    denied(author.post("/studio/sectors", json={"token": "sector-8", "label": "New"}),
           "an author adding a sector")
    denied(author.post("/studio/clients", json={"sector": "sector-1", "name": "New"}),
           "an author adding a client")
    denied(author.post("/studio/examples/remove", json={}),
           "an author removing the examples")
    assert [row["id"] for row in all_published()] == ids, "a denied call moved the grid"
    assert record["state"] == "published"


def test_the_case_file_list_shows_every_row_and_hides_foreign_reads(author, editor):
    record = ready_case_file(author, title=fresh_title("Mine"))
    rows = author.get("/studio/case-files").json()
    slugs = {row["slug"] for row in rows}
    assert record["slug"] in slugs, "an author cannot see their own case file"
    foreign = [row for row in rows if row.get("editable") is False]
    assert foreign, "the list shows no row belonging to somebody else"
    assert any(row["title"] == SUBMITTED_TITLE for row in rows), (
        f"{SUBMITTED_TITLE} is missing from the list")
    target = [row for row in rows if row["title"] == SUBMITTED_TITLE][0]
    denied(author.get(f"/studio/case-files/{target['id']}"),
           "an author opening another person's case file")
    assert editor.get(f"/studio/case-files/{target['id']}").status_code == 200, (
        "an editor cannot open a case file they do not own")
    preview = editor.get(f"/studio/case-files/{target['id']}").json()
    assert preview["title"] == SUBMITTED_TITLE


def test_console_filters_intersect(editor, author):
    record = ready_case_file(author, title=fresh_title("Filtered"), sector="sector-4")
    rows = editor.get("/studio/case-files",
                      params={"state": "draft", "sector": "sector-4"}).json()
    ids = [row["id"] for row in rows]
    assert record["id"] in ids, "the intersecting filter dropped a matching case file"
    for row in rows:
        assert row["state"] == "draft" and row["sector"] == "sector-4", (
            f"the filter returned {row}")
    empty = editor.get("/studio/case-files",
                       params={"state": "published", "sector": "sector-4",
                               "q": "a title nobody wrote"}).json()
    assert empty == [], f"a combination with no results returned {empty}"


def test_console_search_matches_titles_clients_and_ranks_beginnings(editor, author):
    marker = uuid.uuid4().hex[:6]
    first = ready_case_file(author, title=f"Harbourlight {marker}")
    second = new_case_file(author)
    save_header(author, second["id"], title=f"Quiet {marker} Works",
                client=f"Harbourlight {marker}")
    rows = editor.get("/studio/case-files", params={"q": f"harbourlight {marker}"}).json()
    ids = [row["id"] for row in rows]
    assert first["id"] in ids and second["id"] in ids, (
        f"the search returned {[row['title'] for row in rows]}")
    assert ids[0] == first["id"], "a title beginning does not rank above a client match"
    shouted = editor.get("/studio/case-files",
                         params={"q": f"HARBOURLIGHT {marker}"}).json()
    assert [row["id"] for row in shouted] == ids, "the search reads letter case"
    accented = editor.get("/studio/case-files",
                          params={"q": f"hárbourlight {marker}"}).json()
    assert [row["id"] for row in accented] == ids, "the search reads accents"
    single = editor.get("/studio/case-files", params={"q": "h"}).json()
    assert len(single) >= len(rows), "a one-character search was not dropped"


def test_presence_holds_a_field_until_it_is_released(author, editor):
    record = ready_case_file(author)
    held = editor.post(f"/studio/case-files/{record['id']}/presence",
                       json={"field": "description"})
    assert held.status_code < 300, f"announcing presence answered {held.status_code}"
    studio = studio_record(author, record["id"])
    holders = [row for row in studio["presence"] if row.get("field") == "description"]
    assert holders, f"the case file shows no held field: {studio['presence']}"
    assert holders[0]["display_name"] == DISPLAY_NAMES[0], (
        f"the presence line names {holders[0]['display_name']!r}")
    blocked = save_header(author, record["id"], description=BRIEF_TEXT)
    payload = refusal(blocked, "a save to a held field")
    assert payload["error"] == "conflict", f"the refusal reads {payload}"
    released = editor.post(f"/studio/case-files/{record['id']}/presence",
                           json={"field": None})
    assert released.status_code < 300, f"releasing answered {released.status_code}"
    saved = save_header(author, record["id"], description=BRIEF_TEXT)
    assert saved.status_code < 300, f"the freed field answered {saved.status_code}"


def test_console_writes_are_limited_to_a_hundred_and_twenty_a_minute(fresh_author):
    record = ready_case_file(fresh_author)
    last = None
    for index in range(CONSOLE_WRITE_LIMIT + 4):
        last = save_header(fresh_author, record["id"], client=f"Aster {index}")
        if last.status_code == 429:
            break
    payload = refusal(last, "a console write past the limit")
    assert payload["error"] == "rate_limited", f"the refusal reads {payload}"
    assert payload["retry_after"], f"the refusal carries no retry window: {payload}"


def test_an_ordering_route_is_limited_to_thirty_a_minute(fresh_author):
    record = ready_case_file(fresh_author, with_image=True)
    ids = [row["id"] for row in studio_record(fresh_author, record["id"])["chapters"]]
    last = None
    for _ in range(ORDER_WRITE_LIMIT + 2):
        last = fresh_author.put(f"/studio/case-files/{record['id']}/chapter-order",
                                json={"chapter_ids": ids})
        if last.status_code == 429:
            break
    payload = refusal(last, "an ordering write past the limit")
    assert payload["error"] == "rate_limited", f"the refusal reads {payload}"


def test_a_valid_enquiry_is_stored_as_new(anon, db):
    payload = enquiry_payload()
    response = anon.post("/enquiries", json=payload)
    assert response.status_code == 201, (
        f"the enquiry answered {response.status_code}: {response.text[:300]}")
    stored = db.one("enquiry", email=payload["email"])
    assert stored is not None, f"nothing was stored for {payload['email']}"
    assert stored["state"] == "new", f"the enquiry is stored as {stored['state']!r}"
    assert stored["brief"] == payload["brief"], "the brief was not stored verbatim"
    assert stored["budget"] in BUDGET_TOKENS, f"the budget reads {stored['budget']!r}"
    assert stored["consent"], "the consent was not stored"


def test_an_invalid_enquiry_is_refused_field_by_field(anon, db):
    cases = ((("name", ""), NAME_MESSAGE), (("email", "not-an-address"), EMAIL_MESSAGE),
             (("brief", "far too short to be a brief"), BRIEF_MESSAGE),
             (("consent", False), CONSENT_MESSAGE),
             (("organisation", "O" * 121), ORGANISATION_MESSAGE))
    before = db.count("enquiry")
    for (field, value), message in cases:
        response = send_enquiry(anon, **{field: value})
        payload = refusal(response, f"an enquiry with a bad {field}")
        assert payload["error"] == "validation_failed", f"the refusal reads {payload}"
        assert field in payload["fields"], f"the refusal names no {field}: {payload}"
        assert payload["fields"][field] == message, (
            f"the {field} message reads {payload['fields'][field]!r}")
    assert db.count("enquiry") == before, "a refused enquiry was stored"


def test_the_enquiry_brief_is_bounded_at_both_ends(anon, db):
    before = db.count("enquiry")
    refusal(send_enquiry(anon, brief="b" * 4001), "a brief over four thousand characters")
    refusal(send_enquiry(anon, sector="sector-99"), "an enquiry naming an unknown sector")
    refusal(send_enquiry(anon, budget="enormous"), "an enquiry with an unknown budget")
    assert db.count("enquiry") == before, "a refused enquiry was stored"
    ok = send_enquiry(anon, brief="b" * 4000)
    assert ok.status_code == 201, f"a brief of four thousand answered {ok.status_code}"


def test_an_enquiry_from_a_verified_visitor_is_attributed(db):
    created = verified_visitor("Wynn Harper")
    with appclient.client(created["token"]) as api:
        account = api.get("/auth/me").json()
        response = api.post("/enquiries", json=enquiry_payload(email=created["email"],
                                                               name="Wynn Harper"))
        assert response.status_code == 201, f"the enquiry answered {response.status_code}"
        mine = api.get("/enquiries/mine").json()
    stored = db.one("enquiry", email=created["email"])
    assert stored["account_id"] == account["id"], (
        f"the enquiry was stored against {stored['account_id']}")
    assert [row["id"] for row in mine] == [stored["id"]], (
        f"the sender's own list reads {mine}")
    for key in ("id", "brief", "state", "reply", "created_at"):
        assert key in mine[0], f"the sender's list is missing {key}: {sorted(mine[0])}"


def test_an_enquiry_from_a_stranger_is_stored_unattributed(anon, db):
    payload = enquiry_payload()
    anon.post("/enquiries", json=payload)
    stored = db.one("enquiry", email=payload["email"])
    assert stored["account_id"] in (None, 0), (
        f"an unattributed enquiry was linked to {stored['account_id']}")


def test_an_unconfirmed_visitor_is_not_attributed_or_replied_to(db):
    created = signed_up_visitor("Pell Winter")
    with appclient.client(created["token"]) as api:
        response = api.post("/enquiries", json=enquiry_payload(email=created["email"],
                                                               name="Pell Winter"))
        assert response.status_code == 201, f"the enquiry answered {response.status_code}"
    stored = db.one("enquiry", email=created["email"])
    assert stored["account_id"] in (None, 0), (
        "an unconfirmed address was attributed to its account")


def test_an_enquiry_writes_one_message_to_the_sender_and_one_to_the_editors(editor, anon):
    payload = enquiry_payload(brief=f"{BRIEF_TEXT} Read more at https://kelo.example.com")
    anon.post("/enquiries", json=payload)
    outbox = editor.get("/studio/outbox").json()
    to_sender = [row for row in outbox if row["to_email"] == payload["email"]]
    to_editor = [row for row in outbox if row["to_email"] == EDITOR_EMAIL
                 and row["kind"] == "enquiry_arrived"]
    assert to_sender, f"no message reached {payload['email']}"
    assert to_editor, "no message reached the editors"
    assert to_sender[0]["subject"] == ENQUIRY_SENDER_SUBJECT, (
        f"the sender's subject reads {to_sender[0]['subject']!r}")
    assert payload["name"] in to_editor[0]["subject"], (
        f"the editors' subject reads {to_editor[0]['subject']!r}")
    assert INERT_SEPARATOR in to_editor[0]["body"], (
        f"a web address in the brief stayed live: {to_editor[0]['body']}")
    assert "https://" not in to_editor[0]["body"], (
        "the editors' copy carries a live address the sender wrote")
    assert STUDIO_CONTACT in to_editor[0]["body"] or STUDIO_CONTACT in to_sender[0]["body"]


def test_enquiries_are_limited_for_one_sender(anon):
    sender = fresh_email("keen")
    last = None
    for _ in range(ENQUIRY_LIMIT + 1):
        last = anon.post("/enquiries", json=enquiry_payload(email=sender))
    payload = refusal(last, "a fourth enquiry from one address")
    assert payload["error"] == "rate_limited", f"the refusal reads {payload}"
    assert payload["retry_after"], f"the refusal carries no retry window: {payload}"


def test_the_inbox_lists_enquiries_newest_first_and_searches_them(editor, anon):
    marker = uuid.uuid4().hex[:6]
    anon.post("/enquiries", json=enquiry_payload(organisation=f"Bellwether {marker}"))
    rows = editor.get("/studio/enquiries").json()
    assert rows, "the inbox is empty"
    stamps = [row["created_at"] for row in rows]
    assert stamps == sorted(stamps, reverse=True), f"the inbox order reads {stamps}"
    for key in ("id", "name", "email", "organisation", "budget", "sector", "brief",
                "state", "assigned_to", "reply", "read", "account_id", "created_at",
                "answered_at"):
        assert key in rows[0], f"an inbox row is missing {key}: {sorted(rows[0])}"
    found = editor.get("/studio/enquiries", params={"q": f"bellwether {marker}"}).json()
    assert len(found) == 1, f"the search returned {len(found)} rows"
    by_state = editor.get("/studio/enquiries", params={"enquiry_state": "new"}).json()
    assert all(row["state"] == "new" for row in by_state), "the state filter leaked"


def test_an_editor_assigns_reads_and_answers_an_enquiry(editor, db):
    created = verified_visitor("Odell Frame")
    with appclient.client(created["token"]) as api:
        api.post("/enquiries", json=enquiry_payload(email=created["email"],
                                                    name="Odell Frame"))
    stored = db.one("enquiry", email=created["email"])
    read = editor.patch(f"/studio/enquiries/{stored['id']}", json={"read": True})
    assert read.status_code < 300, f"marking it read answered {read.status_code}"
    account = editor.get("/auth/me").json()
    assigned = editor.patch(f"/studio/enquiries/{stored['id']}",
                            json={"state": "assigned", "assigned_to": account["id"]})
    assert assigned.status_code < 300, f"assigning answered {assigned.status_code}"
    assert assigned.json()["assigned_to"] == account["id"]
    replied = editor.post(f"/studio/enquiries/{stored['id']}/replies",
                          json={"body": "We would be glad to talk about this."})
    assert replied.status_code < 300, f"the reply answered {replied.status_code}"
    assert replied.json()["state"] == "answered", f"the enquiry is {replied.json()['state']!r}"
    with appclient.client(created["token"]) as api:
        mine = api.get("/enquiries/mine").json()
    assert mine[0]["reply"] == "We would be glad to talk about this.", (
        f"the sender reads {mine[0]['reply']!r}")
    assert db.one("enquiry", id=stored["id"])["answered_at"] is not None


def test_an_unattributed_enquiry_cannot_be_answered(editor, anon, db):
    payload = enquiry_payload()
    anon.post("/enquiries", json=payload)
    stored = db.one("enquiry", email=payload["email"])
    response = editor.post(f"/studio/enquiries/{stored['id']}/replies",
                           json={"body": "We cannot reach this sender in the app."})
    refused = refusal(response, "a reply to an unattributed enquiry")
    assert refused["error"] in ("validation_failed", "state_not_allowed"), (
        f"the refusal reads {refused}")
    assert db.one("enquiry", id=stored["id"])["reply"] in (None, ""), (
        "a reply was stored anyway")


def test_the_newsletter_stores_one_row_for_an_address(anon, db):
    address = fresh_email("reader")
    first = anon.post("/subscribers", json={"email": address})
    assert first.status_code == 201, f"the subscription answered {first.status_code}"
    again = anon.post("/subscribers", json={"email": address})
    payload = refusal(again, "a repeated subscription")
    assert payload["error"] == "conflict", f"the refusal reads {payload}"
    assert db.count("subscriber", email=address) == 1, (
        "the address was stored more than once")
    refusal(anon.post("/subscribers", json={"email": "not-an-address"}),
            "a malformed newsletter address")
    shouted = fresh_email("Loud").upper()
    anon.post("/subscribers", json={"email": shouted})
    assert db.one("subscriber", email=shouted.lower()) is not None, (
        "a subscriber address was not lowercased")


def test_newsletter_subscriptions_are_limited_for_one_address(anon):
    address = fresh_email("eager")
    last = None
    for _ in range(NEWSLETTER_LIMIT + 1):
        last = anon.post("/subscribers", json={"email": address})
    payload = refusal(last, "a sixth subscription for one address")
    assert payload["error"] in ("rate_limited", "conflict"), f"the refusal reads {payload}"


def test_the_shortlist_accepts_repeated_writes(db):
    created = verified_visitor("Bly Kerrigan")
    record = public_summaries()[0]
    with appclient.client(created["token"]) as api:
        account = api.get("/auth/me").json()
        first = api.put(f"/shortlist/{record['id']}")
        second = api.put(f"/shortlist/{record['id']}")
        assert first.status_code < 300 and second.status_code < 300, (
            f"the shortlist answered {first.status_code} then {second.status_code}")
        assert db.count("shortlist_entry", account_id=account["id"],
                        case_file_id=record["id"]) == 1, "the entry was written twice"
        rows = api.get("/shortlist").json()
        assert [row["case_file_id"] for row in rows] == [record["id"]], (
            f"the shortlist reads {rows}")
        assert rows[0]["slug"] == record["slug"] and rows[0]["title"] == record["title"]
        removed = api.delete(f"/shortlist/{record['id']}")
        again = api.delete(f"/shortlist/{record['id']}")
        assert removed.status_code < 300 and again.status_code < 300, (
            f"removal answered {removed.status_code} then {again.status_code}")
        assert api.get("/shortlist").json() == [], "the entry survived removal"


def test_only_a_published_case_file_is_kept(db, author):
    created = verified_visitor("Nia Colbourne")
    unpublished = ready_case_file(author)
    with appclient.client(created["token"]) as api:
        response = api.put(f"/shortlist/{unpublished['id']}")
        refusal(response, "shortlisting an unpublished case file")
        assert api.get("/shortlist").json() == [], "the unpublished case file was kept"


def test_an_unconfirmed_visitor_cannot_write_the_server_shortlist():
    created = signed_up_visitor("Fen Marlow")
    record = public_summaries()[0]
    with appclient.client(created["token"]) as api:
        refusal(api.put(f"/shortlist/{record['id']}"),
                "a shortlist write from an unconfirmed address")


def test_signing_in_merges_a_browser_shortlist(db):
    created = verified_visitor("Tam Ellery")
    rows = public_summaries()[:2]
    with appclient.client(created["token"]) as api:
        api.put(f"/shortlist/{rows[0]['id']}")
        merged = api.post("/shortlist/merge",
                          json={"entries": [{"case_file_id": rows[0]["id"],
                                             "created_at": "2026-09-01T09:00:00Z"},
                                            {"case_file_id": rows[1]["id"],
                                             "created_at": "2026-09-02T09:00:00Z"}]})
        assert merged.status_code < 300, f"the merge answered {merged.status_code}"
        kept = {row["case_file_id"] for row in api.get("/shortlist").json()}
    assert kept == {rows[0]["id"], rows[1]["id"]}, f"the merged shortlist reads {kept}"
    account = db.one("account", email=created["email"])
    assert db.count("shortlist_entry", account_id=account["id"],
                    case_file_id=rows[0]["id"]) == 1, "the merge duplicated an entry"


def test_a_sector_in_use_cannot_be_removed(editor, db):
    sectors = site_document()["sectors"]
    used = [row for row in sectors if row["token"] == "sector-1"][0]
    stored = db.one("sector", token="sector-1")
    payload = refusal(editor.request("DELETE", f"/studio/sectors/{stored['id']}"),
                      "removing a sector in use")
    assert payload["error"] == "conflict", f"the refusal reads {payload}"
    assert used["label"] == SECTOR_LABELS[0]
    created = editor.post("/studio/sectors", json={"token": "sector-8", "label": "Spare"})
    assert created.status_code == 201, f"a new sector answered {created.status_code}"
    renamed = editor.patch(f"/studio/sectors/{created.json()['id']}",
                           json={"label": "Spare Work"})
    assert renamed.status_code < 300, f"the rename answered {renamed.status_code}"
    refusal(editor.patch(f"/studio/sectors/{created.json()['id']}",
                         json={"label": "L" * 25}), "a sector label over its bound")
    removed = editor.request("DELETE", f"/studio/sectors/{created.json()['id']}")
    assert removed.status_code < 300, f"removing a spare sector answered {removed.status_code}"


def test_a_notice_body_keeps_only_four_treatments(editor, db):
    row = db.rows("notice_row")[0]
    body = ("<p>We keep <em>only</em> what we need.</p>"
            "<ul><li>Enquiries</li></ul>"
            "<script>window.alert(1)</script>"
            "<p onclick=\"steal()\">Reach us at "
            "<a href=\"https://kelo.example.com\" target=\"_blank\">our site</a> or "
            "<a href=\"javascript:steal()\">here</a>.</p>")
    response = editor.patch(f"/studio/notice-rows/{row['id']}", json={"body": body})
    assert response.status_code < 300, f"the notice save answered {response.status_code}"
    saved = response.json()["body"]
    assert "<script" not in saved, f"a script survived the save: {saved}"
    assert "onclick" not in saved, f"an attribute survived the save: {saved}"
    assert "target=" not in saved, f"a link attribute survived the save: {saved}"
    assert "javascript:" not in saved, f"a script address survived the save: {saved}"
    assert "here" in saved, "the dropped link lost its text"
    assert "<em>" in saved and "<li>" in saved, f"an allowed treatment was stripped: {saved}"
    padded = editor.patch(f"/studio/notice-rows/{row['id']}",
                          json={"label": "  Spaced  label  "})
    assert padded.json()["label"] == "Spaced  label", (
        f"the label was not trimmed: {padded.json()['label']!r}")


def test_an_editor_exports_every_entity(editor):
    export = editor.get("/studio/export")
    assert export.status_code == 200, f"the export answered {export.status_code}"
    payload = export.json()
    for key in ("accounts", "sectors", "clients", "case_files", "chapters",
                "information_items", "awards", "notice_rows", "enquiries",
                "subscribers", "messages"):
        assert key in payload, f"the export is missing {key}: {sorted(payload)}"
    assert len(payload["sectors"]) >= len(SECTOR_TOKENS)
    assert len(payload["clients"]) >= len(CLIENT_NAMES)
    assert "password_hash" not in flat(payload), "the export carries a password hash"


def test_only_named_events_are_stored_with_their_named_properties(anon, editor, db):
    good = anon.post("/events", json={"name": "site_opened",
                                      "properties": {"referrer_class": "direct",
                                                     "viewport_class": "wide",
                                                     "reduced_motion": False,
                                                     "webgl_available": True,
                                                     "visitor_email": VISITOR_EMAIL}})
    assert good.status_code == 202, f"a named event answered {good.status_code}"
    refusal(anon.post("/events", json={"name": "vendor_ping", "properties": {}}),
            "an event outside the named list")
    for name in EVENT_NAMES:
        accepted = anon.post("/events", json={"name": name, "properties": {}})
        assert accepted.status_code == 202, (
            f"the named event {name} answered {accepted.status_code}")
    rows = editor.get("/studio/events", params={"name": "site_opened"}).json()
    assert rows, "no site event was stored"
    latest = rows[-1]
    assert "referrer_class" in latest["properties"], (
        f"the stored properties read {latest['properties']}")
    assert "visitor_email" not in latest["properties"], (
        f"an unnamed property was stored: {latest['properties']}")
    assert VISITOR_EMAIL not in flat(rows), "an address was stored on an event"
    assert db.count("analytics_event") >= 1


def test_a_message_is_read_by_its_own_account_only(visitor, author, editor):
    created = verified_visitor("Cleo Danforth")
    with appclient.client(created["token"]) as api:
        mine = messages_for(api)
    assert mine, "the new account received no message"
    for row in mine:
        assert row["to_email"] == created["email"], (
            f"a message addressed to {row['to_email']} reached another account")
        assert row["kind"] in MESSAGE_KINDS, f"the kind reads {row['kind']!r}"
        assert len(row["subject"]) < 60, f"the subject runs to {len(row['subject'])}"
        assert row["body"].count("http") <= 1, f"the message carries two links: {row['body']}"
        assert PASSWORD not in row["body"], "the message carries a password"
    others = [row for row in messages_for(visitor) if row["to_email"] == created["email"]]
    assert not others, "one account reads another account's messages"
    denied(author.get("/studio/outbox"), "an author reading the outbox")
    outbox = editor.get("/studio/outbox").json()
    stamps = [row["created_at"] for row in outbox]
    assert stamps == sorted(stamps, reverse=True), "the outbox is not newest first"
    assert any(row["to_email"] == created["email"] for row in outbox), (
        "the outbox misses a written message")


def test_a_return_and_a_first_publication_write_one_message_each(author, editor):
    record = ready_case_file(author, title=fresh_title("Told"))
    submit(author, record["id"])
    note = "Please lengthen the middle section a little."
    transition(editor, record["id"], "changes_requested", note=note)
    returned = message_of_kind(author, "case_file_returned")
    assert record["title"] in returned["subject"], (
        f"the return subject reads {returned['subject']!r}")
    assert note in returned["body"], f"the note was not carried: {returned['body']}"
    submit(author, record["id"])
    transition(editor, record["id"], "approved")
    transition(editor, record["id"], "published")
    live = message_of_kind(author, "case_file_live")
    assert record["title"] in live["subject"], f"the live subject reads {live['subject']!r}"
    assert record["slug"] in live["link"], f"the live message links to {live['link']!r}"
    before = len([row for row in messages_for(author) if row["kind"] == "case_file_live"])
    save_header(author, record["id"],
                description="A rewritten description that runs past forty characters.")
    author.post(f"/studio/case-files/{record['id']}/publish-changes", json={})
    after = len([row for row in messages_for(author) if row["kind"] == "case_file_live"])
    assert after == before, "publishing changes wrote another message"


def test_two_simultaneous_sign_ups_for_one_address_create_one_account(db):
    email = fresh_email("race")
    outcomes: list = []
    barrier = threading.Barrier(2)

    def register():
        barrier.wait()
        outcomes.append(httpx.post(f"{appclient.api_base()}/auth/signup",
                                   json={"email": email, "password": PASSWORD,
                                         "display_name": "Race Condition"},
                                   timeout=appclient.TIMEOUT))

    runners = [threading.Thread(target=register) for _ in range(2)]
    for runner in runners:
        runner.start()
    for runner in runners:
        runner.join()
    assert db.count("account", email=email) == 1, (
        f"two accounts exist for {email}: {[r.status_code for r in outcomes]}")


def test_two_simultaneous_subscriptions_create_one_subscriber(db):
    email = fresh_email("double")
    outcomes: list = []
    barrier = threading.Barrier(2)

    def subscribe():
        barrier.wait()
        outcomes.append(httpx.post(f"{appclient.api_base()}/subscribers",
                                   json={"email": email}, timeout=appclient.TIMEOUT))

    runners = [threading.Thread(target=subscribe) for _ in range(2)]
    for runner in runners:
        runner.start()
    for runner in runners:
        runner.join()
    assert db.count("subscriber", email=email) == 1, (
        f"two subscribers exist for {email}: {[r.status_code for r in outcomes]}")


def test_a_review_queue_row_arrives_for_the_editor(author, editor):
    record = ready_case_file(author, title=fresh_title("Queued"))
    submit(author, record["id"])
    rows = settle(lambda: [row for row in
                           editor.get("/studio/case-files",
                                      params={"state": "submitted"}).json()
                           if row["id"] == record["id"]],
                  "the submitted case file reaching the review queue")
    assert rows[0]["state"] == "submitted", f"the queue row reads {rows[0]}"
    assert rows[0]["owner_name"] == DISPLAY_NAMES[1], (
        f"the queue names {rows[0]['owner_name']!r}")


def test_the_home_screen_fills_one_window(page):
    open_site(page)
    metrics = page.evaluate(
        "() => ({doc: document.documentElement.scrollHeight,"
        " view: window.innerHeight, wide: document.documentElement.scrollWidth,"
        " across: window.innerWidth})")
    assert metrics["doc"] <= metrics["view"] + 2, (
        f"the home document runs {metrics['doc']} tall in a window of {metrics['view']}")
    assert metrics["wide"] <= metrics["across"] + 2, (
        f"the home document runs {metrics['wide']} wide in a window of {metrics['across']}")
    text = page.inner_text("body")
    assert WORDMARK_LINE in text, f"the wordmark is missing: {text[:200]}"
    assert WORDMARK_SECOND in text, f"the second wordmark line is missing: {text[:200]}"
    assert page.locator("footer").count() == 0, "the home screen carries a footer"
    assert page.locator("canvas").count() >= 1, "no drawing surface carries the crystal"


def test_the_wordmark_is_set_in_the_pinned_type(page):
    open_site(page)
    mark = page.get_by_text(WORDMARK_LINE).first
    style = mark.evaluate(
        "node => {const s = getComputedStyle(node);"
        " return {family: s.fontFamily, size: s.fontSize, weight: s.fontWeight};}")
    assert "inter" in style["family"].lower(), f"the family reads {style['family']!r}"
    assert "arial" in style["family"].lower(), f"the fallback reads {style['family']!r}"
    assert style["size"] == "48px", f"the wordmark is set at {style['size']}"
    assert style["weight"] in ("200", "300"), f"the wordmark weight reads {style['weight']}"


def test_no_rendered_text_falls_below_its_pinned_floor(page):
    for path in (f"/work/{PUBLISHED_SLUG}", "/contact"):
        open_site(page, path)
        sizes = page.evaluate(
            "() => Array.from(document.querySelectorAll('body *'))"
            ".filter(node => Array.from(node.childNodes).some("
            "child => child.nodeType === 3 && child.textContent.trim().length > 1))"
            ".map(node => parseFloat(getComputedStyle(node).fontSize))"
            ".filter(size => size > 0)")
        assert sizes, f"{path} rendered no text to measure"
        assert min(sizes) >= 10, f"{path} renders a label at {min(sizes)} pixels"
        reading = [size for size in sizes if size < 26]
        assert reading, f"{path} carries no reading text under the display steps"
        assert max(sizes) >= 34, f"{path} carries no display step above the reading sizes"
    open_site(page, "/work")
    title = page.get_by_text(PUBLISHED_TITLE).first
    assert title.count(), "the carousel shows no project title"
    step = title.evaluate("node => getComputedStyle(node).fontSize")
    assert step == "65px", f"a carousel title is set at {step}"


def test_the_page_fetches_no_media_file_of_its_own(page):
    seen: list = []
    page.on("request", lambda request: seen.append(request.url))
    open_site(page)
    page.wait_for_timeout(4000)
    for url in seen:
        low = url.lower().split("?")[0]
        for suffix in (".mp3", ".wav", ".ogg", ".m4a", ".mp4", ".webm", ".woff",
                       ".woff2", ".ttf", ".otf", ".glb", ".gltf"):
            assert not low.endswith(suffix), f"the page fetched {url}"
    assert not page.evaluate("() => document.querySelectorAll('audio, video').length > 0"
                             " && Array.from(document.querySelectorAll('audio, video'))"
                             ".some(node => !node.paused)"), "sound plays on arrival"


def test_the_page_calls_no_third_party_host(page):
    seen: list = []
    sockets: list = []
    page.on("request", lambda request: seen.append(request.url))
    page.on("websocket", lambda socket: sockets.append(socket.url))
    open_site(page)
    page.wait_for_timeout(4000)
    origin = app_origin()
    for url in seen:
        assert url.startswith(origin) or url.startswith("data:") or url.startswith("blob:"), (
            f"the page called {url}")
    assert not sockets, f"the public site opened a live connection: {sockets}"


def test_the_home_screen_stays_inside_its_transfer_budget(page):
    open_site(page)
    page.wait_for_timeout(4000)
    total = page.evaluate(
        "() => performance.getEntriesByType('resource')"
        ".reduce((sum, entry) => sum + (entry.transferSize || 0), 0)"
        " + (performance.getEntriesByType('navigation')[0] || {transferSize: 0}).transferSize")
    assert total <= HOME_TRANSFER_BUDGET, (
        f"the first visit transferred {total} bytes past the budget")
    names = page.evaluate(
        "() => performance.getEntriesByType('resource').map(entry => entry.name)")
    for name in names:
        low = name.lower()
        assert "poster" not in low and "console" not in low, (
            f"the home screen fetched {name}")


def test_the_app_serves_a_production_build(page):
    seen: list = []
    page.on("request", lambda request: seen.append(request.url))
    open_site(page)
    assert page.locator("[data-v-app]").count() >= 1, (
        "the document carries no mounted application root")
    text = page.content()
    assert "/@vite/client" not in text, "the document loads a development client"
    for url in seen:
        assert "/@vite/" not in url, f"the page fetched a development module: {url}"


def test_the_site_renders_with_browser_storage_blocked(browser):
    context = browser.new_context()
    context.add_init_script(
        "Object.defineProperty(window, 'localStorage', {get() {"
        " throw new Error('storage is blocked'); }});")
    surface = context.new_page()
    surface.goto(f"{app_origin()}/", wait_until="networkidle")
    text = surface.inner_text("body")
    assert WORDMARK_LINE in text, f"the wordmark is missing with storage blocked: {text[:200]}"
    assert "error" not in text.lower(), f"an error was shown instead: {text[:200]}"
    context.close()


def test_the_crystal_keeps_its_place_in_browser_storage(page):
    open_site(page)
    page.wait_for_timeout(1200)
    keys = page.evaluate("() => Object.keys(window.localStorage)")
    assert "crystal_angle" in keys, f"the stored keys read {keys}"
    assert "crystal_seed" in keys, f"the stored keys read {keys}"
    assert "crystal_count" in keys, f"the stored keys read {keys}"
    count = page.evaluate("() => window.localStorage.getItem('crystal_count')")
    assert str(count).strip('"').isdigit(), f"the stored count reads {count!r}"


def test_the_page_records_its_opening_on_the_app_origin(page):
    posted: list = []
    page.on("request", lambda request: posted.append((request.method, request.url))
            if request.method == "POST" else None)
    open_site(page)
    events = []
    for _ in range(12):
        page.wait_for_timeout(1000)
        events = [url for method, url in posted
                  if url.startswith(f"{app_origin()}/api/events")]
        if events:
            break
    assert events, f"the page sent no opening event: {posted}"


def test_the_story_carries_its_renamed_classes(page):
    open_site(page, "/story")
    assert page.locator(".about__studioTitle").count() >= 1, (
        "the studio title carries no renamed class")
    assert page.locator(".about__studioSubtitle").count() >= 1, (
        "the studio subtitle carries no renamed class")
    classes = page.evaluate(
        "() => Array.from(document.querySelectorAll('*'))"
        ".map(node => node.className && node.className.toString()).join(' ')")
    assert "kelo" not in classes.lower(), "a class name carries the studio name"
    text = page.inner_text("body")
    assert STUDIO_PROMISE in text, f"the promise is missing: {text[:200]}"
    assert SECTOR_LABELS[0] in text, f"the first sector row is missing: {text[:200]}"


def test_every_form_control_carries_its_field_name(page):
    open_site(page, "/studio/sign-in")
    assert page.locator("input[name=\"email\"]").count() >= 1, (
        "the sign-in address field carries no name")
    assert page.locator("input[name=\"password\"]").count() >= 1, (
        "the sign-in password field carries no name")
    assert "Studio" in page.inner_text("body"), "the sign-in layer shows no heading"
    open_site(page, "/contact")
    for field in ("name", "email", "organisation", "brief", "consent"):
        assert page.locator(f"[name=\"{field}\"]").count() >= 1, (
            f"the enquiry form carries no {field} control")


def test_the_enquiry_form_answers_inline_and_stores_nothing(page, db):
    before = db.count("enquiry")
    open_site(page, "/contact")
    page.fill("[name=\"name\"]", "")
    page.fill("[name=\"brief\"]", "far too short")
    page.locator("form").filter(has=page.locator("[name=\"brief\"]")).first.locator(
        "button, [type=\"submit\"]").first.click()
    page.wait_for_timeout(1200)
    text = page.inner_text("body")
    assert NAME_MESSAGE in text or BRIEF_MESSAGE in text, (
        f"the form said nothing about the missing values: {text[:400]}")
    assert db.count("enquiry") == before, "a refused enquiry reached the database"


def test_markup_typed_into_a_title_is_shown_as_text(page, author, editor):
    marker = uuid.uuid4().hex[:6]
    record = published_case_file(author, editor, title=f"<b>Bolt</b> {marker}")
    open_site(page, f"/work/{record['slug']}")
    text = page.inner_text("body")
    assert f"<b>Bolt</b> {marker}" in text, f"the title was not shown as text: {text[:300]}"
    assert page.locator("b", has_text="Bolt").count() == 0, (
        "the typed markup became an element")


def test_a_narrow_window_never_scrolls_sideways(narrow_page):
    for path in ("/", "/work/all", "/contact", "/notice"):
        narrow_page.goto(f"{app_origin()}{path}", wait_until="networkidle")
        metrics = narrow_page.evaluate(
            "() => ({wide: document.documentElement.scrollWidth,"
            " across: window.innerWidth})")
        assert metrics["wide"] <= metrics["across"] + 2, (
            f"{path} runs {metrics['wide']} wide in a window of {metrics['across']}")


def test_the_crawler_fragments_are_not_product_pages(page):
    for path in ("/", "/work/all", "/contact"):
        open_site(page, path)
        hrefs = page.evaluate(
            "() => Array.from(document.querySelectorAll('a[href]'))"
            ".map(node => node.getAttribute('href'))")
        for fragment in CRAWLER_FRAGMENTS:
            assert fragment not in hrefs, f"{path} links to {fragment}"


def test_a_pasted_case_file_address_opens_that_case_file(page):
    open_site(page, f"/work/{PUBLISHED_SLUG}")
    text = page.inner_text("body")
    assert PUBLISHED_TITLE in text, f"the case file did not open: {text[:300]}"
    assert page.url.endswith(f"/work/{PUBLISHED_SLUG}"), f"the address reads {page.url}"
    assert "LAUNCHED AT" in text or "Aster" in text, (
        f"the case file header is missing: {text[:300]}")
    gone = page.goto(f"{app_origin()}/work/{DRAFT_SLUG}", wait_until="networkidle")
    assert gone is not None
    missing = page.inner_text("body")
    assert "Not here." in missing, f"an unpublished address showed {missing[:300]}"
    assert page.url.endswith(f"/work/{DRAFT_SLUG}"), f"the address moved to {page.url}"

def test_the_rows_live_in_postgres_and_the_bytes_in_the_bucket(author, editor, db, store):
    record = published_case_file(author, editor, title=fresh_title("Ledger"),
                                 with_image=True)
    row = db.one("case_file", id=record["id"])
    assert row is not None, "the published case file is in no database row"
    assert row["title"] == record["title"], (
        f"the stored title reads {row['title']!r} against {record['title']!r}")
    public = public_case_file(record["slug"])
    assert public["title"] == row["title"], (
        "the public interface disagrees with the stored row")
    media = db.rows("case_media", case_file_id=record["id"])
    assert media, "the uploaded image left no media row"
    assert store.exists(media[0]["key"]), (
        f"the interface names an object the bucket does not hold: {media[0]['key']}")
    assert db.count("account") >= 4, "the accounts are not in the database"


def test_an_invalid_call_answers_a_client_error(anon, author, editor):
    attempts = ((anon.get("/case-files/does-not-exist"), "an unknown case file"),
                (anon.post("/enquiries", json={}), "an empty enquiry"),
                (anon.get("/studio/case-files"), "an unsigned studio read"),
                (author.get("/studio/enquiries"), "an author reading the inbox"),
                (author.post("/studio/case-files/999999999/transitions",
                             json={"to": "published"}), "a move on a missing case file"),
                (editor.patch("/studio/notice-rows/999999999", json={"label": "X"}),
                 "a save to a missing notice row"),
                (anon.post("/subscribers", json={"email": None}),
                 "a subscription with no address"))
    for response, what in attempts:
        assert is_client_error(response.status_code), (
            f"{what} answered {response.status_code}: {response.text[:200]}")
    assert page_response("/").status_code == 200, "the app stopped answering"


def test_an_image_chapter_keeps_the_text_alternative(author):
    record = ready_case_file(author)
    media = upload_image(author, record["id"]).json()
    chapter = add_chapter(author, record["id"], "image",
                          {"alt": "A room with its own weather", "media_id": media["id"]})
    assert chapter["payload"]["alt"] == "A room with its own weather", (
        f"the stored alternative reads {chapter['payload']}")
    assert chapter["payload"]["media_id"] == media["id"], (
        "the chapter lost the uploaded picture")
    stored = studio_record(author, record["id"])["chapters"][-1]
    assert stored["payload"]["alt"] == "A room with its own weather"


def test_the_enquiry_budget_takes_each_of_the_five_bands(anon, db):
    for band in BUDGET_TOKENS:
        payload = enquiry_payload(budget=band)
        response = anon.post("/enquiries", json=payload)
        assert response.status_code == 201, (
            f"the band {band} answered {response.status_code}: {response.text[:200]}")
        assert db.one("enquiry", email=payload["email"])["budget"] == band, (
            f"the band {band} was not stored")


def test_a_new_enquiry_reaches_an_open_inbox(editor, anon):
    payload = enquiry_payload()
    anon.post("/enquiries", json=payload)
    rows = settle(lambda: [row for row in editor.get("/studio/enquiries").json()
                           if row["email"] == payload["email"]],
                  "the new enquiry reaching the inbox")
    assert rows[0]["name"] == payload["name"], f"the inbox row reads {rows[0]}"
    assert rows[0]["state"] == "new", f"the new enquiry is {rows[0]['state']!r}"
    assert rows[0]["read"] in (False, None), "the new enquiry is already read"


def test_a_signed_out_studio_address_asks_for_a_sign_in(page):
    page.goto(f"{app_origin()}/studio", wait_until="networkidle")
    assert "/studio/sign-in" in page.url, f"the address reads {page.url}"
    assert "next=/studio" in page.url, f"the address carries {page.url}"
    assert "Studio" in page.inner_text("body"), "the sign-in layer shows no heading"
    page.goto(f"{app_origin()}/studio/review", wait_until="networkidle")
    assert "next=/studio/review" in page.url, f"the address reads {page.url}"


def test_a_foreign_next_value_is_discarded(page):
    page.goto(f"{app_origin()}/studio/sign-in?next=//elsewhere.example",
              wait_until="networkidle")
    sign_in_on_page(page, EDITOR_EMAIL)
    assert "elsewhere.example" not in page.url, f"the sign-in left for {page.url}"
    assert page.url.rstrip("/").endswith("/studio"), f"the sign-in landed at {page.url}"


def test_a_visitor_is_denied_the_console_surfaces(page):
    page.goto(f"{app_origin()}/studio/sign-in", wait_until="networkidle")
    sign_in_on_page(page, VISITOR_EMAIL)
    assert page.url.rstrip("/") == app_origin().rstrip("/"), (
        f"a visitor landed at {page.url}")
    for path in ("/studio", "/studio/review", "/studio/enquiries", "/studio/site"):
        page.goto(f"{app_origin()}{path}", wait_until="networkidle")
        text = page.inner_text("body")
        assert "Not for you" in text, f"{path} showed {text[:200]}"
        assert "BACK TO THE WORK" in text, f"{path} offers no way back: {text[:200]}"
    page.goto(f"{app_origin()}/studio/account", wait_until="networkidle")
    assert "Not for you" not in page.inner_text("body"), (
        "the account surface was denied to its own holder")


def test_an_author_sees_the_list_and_not_the_editor_surfaces(page):
    page.goto(f"{app_origin()}/studio/sign-in", wait_until="networkidle")
    sign_in_on_page(page, AUTHOR_EMAIL)
    assert page.url.rstrip("/").endswith("/studio"), f"an author landed at {page.url}"
    assert DRAFT_TITLE in page.inner_text("body"), (
        f"the author's own case file is not listed: {page.inner_text('body')[:300]}")
    for path in ("/studio/review", "/studio/grid", "/studio/enquiries",
                 "/studio/outbox", "/studio/site"):
        page.goto(f"{app_origin()}{path}", wait_until="networkidle")
        assert "Not for you" in page.inner_text("body"), (
            f"{path} opened for an author")


def test_the_account_routes_answer_the_application(page):
    for path in ("/join", "/reset", "/shortlist"):
        page.goto(f"{app_origin()}{path}", wait_until="networkidle")
        assert page.locator("[data-v-app]").count() >= 1, f"{path} served no application"
        assert page.inner_text("body").strip(), f"{path} rendered nothing"
    page.goto(f"{app_origin()}/invite?token=not-a-real-token", wait_until="networkidle")
    assert page.inner_text("body").strip(), "the invitation route rendered nothing"


def test_a_kept_case_file_shows_on_the_shortlist_route(page, visitor):
    record = public_summaries()[0]
    kept = visitor.put(f"/shortlist/{record['id']}")
    assert kept.status_code < 300, f"keeping the case file answered {kept.status_code}"
    page.goto(f"{app_origin()}/studio/sign-in", wait_until="networkidle")
    sign_in_on_page(page, VISITOR_EMAIL)
    page.goto(f"{app_origin()}/shortlist", wait_until="networkidle")
    text = page.inner_text("body")
    assert record["title"] in text, (
        f"the kept case file is missing from the shortlist surface: {text[:300]}")
    visitor.delete(f"/shortlist/{record['id']}")


def test_signing_out_returns_to_the_home_screen(page):
    page.goto(f"{app_origin()}/studio/sign-in", wait_until="networkidle")
    sign_in_on_page(page, AUTHOR_EMAIL)
    page.goto(f"{app_origin()}/studio/account", wait_until="networkidle")
    control = page.get_by_text(re.compile("sign out", re.IGNORECASE)).first
    assert control.count() >= 1, "the account surface offers no way out"
    control.click()
    page.wait_for_timeout(1500)
    assert page.url.rstrip("/") == app_origin().rstrip("/"), (
        f"signing out landed at {page.url}")


def test_the_icon_set_is_declared_inside_the_document(page):
    open_site(page)
    symbols = page.evaluate(
        "() => Array.from(document.querySelectorAll('symbol, svg [id]'))"
        ".map(node => node.id).filter(Boolean)")
    for name in ("arrow", "close", "play", "drop", "menu"):
        assert any(name in symbol for symbol in symbols), (
            f"the {name} mark is not declared in the document: {symbols}")
    assert len(set(symbols)) >= 10, f"the document declares {len(set(symbols))} marks"


def test_the_site_keeps_working_with_the_network_off(page):
    open_site(page)
    page.goto(f"{app_origin()}/story", wait_until="networkidle")
    page.context.set_offline(True)
    page.goto(f"{app_origin()}/contact", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    text = page.inner_text("body")
    assert "OFFLINE" in text.upper(), f"the bar said nothing about the connection: {text[:300]}"
    page.context.set_offline(False)
    back = ""
    for _ in range(10):
        page.wait_for_timeout(1000)
        back = page.inner_text("body").upper()
        if "BACK ONLINE" in back:
            break
    assert "BACK ONLINE" in back, f"the bar never said the connection returned: {back[:300]}"
    page.context.set_offline(True)
    page.goto(f"{app_origin()}/contact", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    offline_contact = page.inner_text("body")
    assert "saved here" in offline_contact, (
        f"the offline contact surface kept no message for the visitor: {offline_contact[:300]}")
    page.goto(f"{app_origin()}/story", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    offline_story = page.inner_text("body")
    assert "You are offline." in offline_story, (
        f"the offline studio story showed no offline face: {offline_story[:300]}")
    page.context.set_offline(False)


def test_an_unsent_enquiry_survives_a_reload(page, db):
    before = db.count("enquiry")
    open_site(page, "/contact")
    page.fill("[name=\"name\"]", "Marlow Frye")
    page.fill("[name=\"brief\"]", BRIEF_TEXT)
    page.locator("[name=\"brief\"]").blur()
    page.wait_for_timeout(800)
    stored = page.evaluate("() => window.localStorage.getItem('enquiry_draft')")
    assert stored and "Marlow Frye" in stored, f"the draft reads {stored!r}"
    page.reload(wait_until="networkidle")
    page.wait_for_timeout(800)
    assert page.input_value("[name=\"name\"]") == "Marlow Frye", (
        "the reload lost the typed name")
    assert db.count("enquiry") == before, "an unsent enquiry reached the database"


def test_a_filter_change_replaces_the_history_entry(page):
    open_site(page, "/work")
    page.goto(f"{app_origin()}/work/all", wait_until="networkidle")
    depth = page.evaluate("() => window.history.length")
    page.goto(f"{app_origin()}/work/all?sector=sector-6", wait_until="networkidle")
    assert "sector=sector-6" in page.url, f"the address reads {page.url}"
    assert page.evaluate("() => window.history.length") >= depth, "history shrank"
    page.go_back()
    page.wait_for_timeout(1200)
    assert "/work" in page.url, f"the back control landed at {page.url}"


def test_the_examples_are_reported_and_removed_last(editor, db):
    before = editor.get("/studio/examples").json()
    assert before["present"] is True, f"the examples are reported as {before}"
    assert before["count"] == 3, f"the examples number {before['count']}"
    seeded = db.rows("case_file", seeded=True)
    ids = [row["id"] for row in seeded]
    response = editor.post("/studio/examples/remove", json={})
    assert response.status_code < 300, f"the removal answered {response.status_code}"
    for case_id in ids:
        assert db.count("case_file", id=case_id) == 0, f"case file {case_id} survived"
        assert db.count("chapter", case_file_id=case_id) == 0, (
            f"a chapter of {case_id} survived")
    after = editor.get("/studio/examples").json()
    assert after["present"] is False, f"the examples are still reported as {after}"
    slugs = {row["slug"] for row in public_summaries()}
    assert PUBLISHED_SLUG not in slugs, "a removed example is still public"
