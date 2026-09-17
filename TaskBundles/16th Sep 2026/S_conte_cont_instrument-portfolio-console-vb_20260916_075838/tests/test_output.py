"""The one merged pytest module for deku/instrument-portfolio-console-vb.

Every assertion is black box: HTTP against the deployed app, rows through the
generic backend adapter, objects through the generic store adapter. Nothing
here reads the agent's source, imports a provider SDK, or assumes a framework.
"""

from __future__ import annotations

import concurrent.futures

import httpx
from conftest import (
    ACCEPTED,
    CITY_FIRST,
    CITY_SECOND,
    CITY_THIRD,
    CONFLICT,
    CORPUS_PASSWORD,
    DENIED,
    DENIED_OR_MISSING,
    EDITOR_EMAIL,
    ERROR_LINK,
    ERROR_MESSAGE_BODY,
    ERROR_SENDER_EMAIL,
    ERROR_SENDER_NAME,
    ERROR_TITLE,
    ERROR_YEAR,
    GONE_OR_MISSING,
    LOCKOUT_ATTEMPTS,
    MESSAGE_RATE_LIMIT,
    OK,
    OWNER_EMAIL,
    PREVIEW_KEY_PREFIX,
    PREVIEW_KEY_SUFFIX,
    PROFILE_FULL_NAME,
    PUBLIC_ROUTES,
    RECOGNITION_FIRST,
    RECOGNITION_SECOND,
    RECOGNITION_THIRD,
    REFUSAL_EXPLANATION,
    REFUSED,
    SECURITY_HEADERS,
    SIGN_IN_FAILURE,
    STATE_UNREAD,
    STUDY_FIRST,
    STUDY_SECOND,
    STUDY_THIRD,
    TITLE_MAX,
    YEAR_MAX,
    api,
    app_origin,
    body_text,
    console_payload,
    create_entry,
    entry_id_of,
    new_entry_payload,
    new_message_payload,
    poll_until,
    preview_keys,
    probe_email,
    probe_title,
    settle,
    unique_suffix,
    version_of,
    work_titles,
)


def test_health_route_answers_two_hundred_without_credentials(anon_client):
    r = anon_client.get(api("/health"))
    assert r.status_code == 200, (
        f"GET /api/health answered {r.status_code} with no credential; the App "
        f"Contract requires 200 once the app is ready. Body: {body_text(r)[:400]}"
    )


def test_console_read_returns_published_work_in_shelf_order(anon_client, owner_client,
                                                            console):
    first, second = probe_title(), probe_title()
    for title in (first, second):
        created = create_entry(owner_client, title=title)
        assert created.status_code in OK, (
            f"POST /api/studio/work for {title!r} answered {created.status_code}; an "
            f"owner may create an entry. Body: {body_text(created)[:400]}"
        )
        entry_id = entry_id_of(created, console, title)
        version = version_of(created, console, entry_id)
        published = owner_client.post(api(f"/studio/work/{entry_id}/publish"),
                                      json={"version": version})
        assert published.status_code in OK, (
            f"POST /api/studio/work/{entry_id}/publish answered "
            f"{published.status_code} for an owner. Body: {body_text(published)[:400]}"
        )
    titles = work_titles(console_payload(anon_client))
    assert first in titles and second in titles, (
        f"GET /api/console listed {titles[:12]}, which is missing one of the two "
        f"entries just published ({first!r}, {second!r})"
    )
    rows = {row["title"]: row.get("position") for row in console.entries()
            if row.get("title") in (first, second)}
    ordered = sorted(rows, key=lambda t: rows[t])
    assert [t for t in titles if t in rows] == ordered, (
        f"GET /api/console listed the two probe entries as "
        f"{[t for t in titles if t in rows]}, which is not their stored shelf order "
        f"{ordered} (positions {rows})"
    )


def test_owner_publishes_entry_and_it_appears_in_the_console_read(anon_client,
                                                                  owner_client, console):
    title = probe_title()
    created = create_entry(owner_client, title=title)
    assert created.status_code in OK, (
        f"POST /api/studio/work answered {created.status_code} for an owner. "
        f"Body: {body_text(created)[:400]}"
    )
    entry_id = entry_id_of(created, console, title)
    assert title not in work_titles(console_payload(anon_client)), (
        f"GET /api/console already listed {title!r} before it was published; saving "
        f"an entry does not make it public"
    )
    version = version_of(created, console, entry_id)
    published = owner_client.post(api(f"/studio/work/{entry_id}/publish"),
                                  json={"version": version})
    assert published.status_code in OK, (
        f"POST /api/studio/work/{entry_id}/publish answered {published.status_code} "
        f"for an owner. Body: {body_text(published)[:400]}"
    )
    assert poll_until(lambda: title in work_titles(console_payload(anon_client))), (
        f"GET /api/console never listed {title!r} after a successful publish"
    )


def test_reordered_shelf_position_is_stored_and_survives_a_reload(owner_client, console):
    titles = [probe_title() for _ in range(2)]
    ids = []
    for title in titles:
        created = create_entry(owner_client, title=title)
        assert created.status_code in OK, (
            f"POST /api/studio/work answered {created.status_code} for an owner. "
            f"Body: {body_text(created)[:400]}"
        )
        ids.append(entry_id_of(created, console, title))
    rows = [console.entry_by_id(i) for i in ids]
    versions = {str(i): (row or {}).get("version") for i, row in zip(ids, rows)}
    order = [ids[1], ids[0]]
    put = owner_client.put(api("/studio/shelf"),
                           json={"kind": "work", "order": order, "versions": versions})
    assert put.status_code in OK, (
        f"PUT /api/studio/shelf answered {put.status_code} for an owner reordering "
        f"two of their own entries. Body: {body_text(put)[:400]}"
    )
    stored = {str(i): (console.entry_by_id(i) or {}).get("position") for i in ids}
    assert stored[str(ids[1])] < stored[str(ids[0])], (
        f"after PUT /api/studio/shelf moved {ids[1]} ahead of {ids[0]}, the stored "
        f"positions read {stored}; the written order did not survive the reload"
    )


def test_unpublished_entry_keeps_its_shelf_position_after_a_republish(owner_client,
                                                                     console):
    title = probe_title()
    created = create_entry(owner_client, title=title)
    entry_id = entry_id_of(created, console, title)
    version = version_of(created, console, entry_id)
    up = owner_client.post(api(f"/studio/work/{entry_id}/publish"),
                           json={"version": version})
    assert up.status_code in OK, (
        f"publish answered {up.status_code} for an owner. Body: {body_text(up)[:400]}"
    )
    before = (console.entry_by_id(entry_id) or {}).get("position")
    version = (console.entry_by_id(entry_id) or {}).get("version")
    down = owner_client.request("DELETE", api(f"/studio/work/{entry_id}/publish"),
                                json={"version": version})
    assert down.status_code in ACCEPTED, (
        f"unpublish answered {down.status_code} for an owner. "
        f"Body: {body_text(down)[:400]}"
    )
    after_unpublish = (console.entry_by_id(entry_id) or {}).get("position")
    assert after_unpublish == before, (
        f"unpublishing entry {entry_id} moved its shelf position from {before} to "
        f"{after_unpublish}; an unpublished entry keeps the place its owner left it"
    )
    version = (console.entry_by_id(entry_id) or {}).get("version")
    again = owner_client.post(api(f"/studio/work/{entry_id}/publish"),
                              json={"version": version})
    assert again.status_code in OK, (
        f"republish answered {again.status_code} for an owner. "
        f"Body: {body_text(again)[:400]}"
    )
    after = (console.entry_by_id(entry_id) or {}).get("position")
    assert after == before, (
        f"republishing entry {entry_id} put it at position {after} rather than back "
        f"at {before}; publishing later must restore the shelf place, not append"
    )


def test_seeded_studies_and_recognitions_are_present_in_the_console_read(anon_client,
                                                                        console):
    payload = console_payload(anon_client)
    study_titles = [s.get("title") for s in (payload.get("studies") or [])
                    if isinstance(s, dict)]
    for title in (STUDY_FIRST, STUDY_SECOND, STUDY_THIRD):
        assert title in study_titles, (
            f"GET /api/console listed studies {study_titles}; the seeded study "
            f"{title!r} is absent, so the seed did not run or did not publish it"
        )
    bodies = [r.get("body") for r in (payload.get("recognitions") or [])
              if isinstance(r, dict)]
    for body in (RECOGNITION_FIRST, RECOGNITION_SECOND, RECOGNITION_THIRD):
        assert body in bodies, (
            f"GET /api/console listed recognitions {bodies}; the seeded recognition "
            f"{body!r} is absent"
        )
    names = [c.get("name") for c in (payload.get("cities") or []) if isinstance(c, dict)]
    for city in (CITY_FIRST, CITY_SECOND, CITY_THIRD):
        assert city in names, (
            f"GET /api/console listed cities {names}; the seeded city {city!r} is absent"
        )
    profile = payload.get("profile") or {}
    assert profile.get("full_name") == PROFILE_FULL_NAME, (
        f"GET /api/console carried profile full name {profile.get('full_name')!r} "
        f"rather than the seeded {PROFILE_FULL_NAME!r}"
    )


def test_published_entry_preview_object_exists_in_the_bucket(owner_client, console,
                                                             store):
    title = probe_title()
    created = create_entry(owner_client, title=title)
    entry_id = entry_id_of(created, console, title)
    version = version_of(created, console, entry_id)
    published = owner_client.post(api(f"/studio/work/{entry_id}/publish"),
                                  json={"version": version})
    assert published.status_code in OK, (
        f"publish answered {published.status_code} for an owner. "
        f"Body: {body_text(published)[:400]}"
    )
    keys = poll_until(lambda: preview_keys(store, entry_id))
    assert keys, (
        f"no object under {PREVIEW_KEY_PREFIX}{entry_id}/ ending {PREVIEW_KEY_SUFFIX} "
        f"exists in the bucket after publishing entry {entry_id}; the preview bytes "
        f"must live in the object store, not on the app's own disk"
    )
    row = console.entry_by_id(entry_id) or {}
    assert row.get("preview_key") in keys, (
        f"the stored preview_key {row.get('preview_key')!r} names no object that "
        f"exists in the bucket; the bucket holds {keys}"
    )


def test_draft_entry_preview_object_is_denied_to_an_anonymous_caller(anon_client,
                                                                     owner_client,
                                                                     console, store):
    title = probe_title()
    created = create_entry(owner_client, title=title)
    entry_id = entry_id_of(created, console, title)
    row = console.entry_by_id(entry_id) or {}
    assert row.get("published") in (False, 0, None), (
        f"entry {entry_id} came back published {row.get('published')!r} straight after "
        f"a save; saving does not publish"
    )
    keys = preview_keys(store, entry_id) or [f"{PREVIEW_KEY_PREFIX}{entry_id}/probe.png"]
    key = row.get("preview_key") or keys[0]
    r = anon_client.get(api(f"/{key}"))
    assert r.status_code in DENIED_OR_MISSING, (
        f"GET /api/{key} answered {r.status_code} with no credential for a DRAFT "
        f"entry's preview object; a draft preview is not readable by a stranger at "
        f"its exact key. Body: {body_text(r)[:400]}"
    )


def test_concurrent_entry_writes_from_one_version_accept_at_most_one(owner_client,
                                                                     console):
    title = probe_title()
    created = create_entry(owner_client, title=title)
    entry_id = entry_id_of(created, console, title)
    version = version_of(created, console, entry_id)

    def write(summary):
        return owner_client.patch(api(f"/studio/work/{entry_id}"),
                                  json={"summary": summary, "version": version})

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(write, f"summary {n}") for n in range(2)]
        results = [f.result() for f in futures]
    accepted = [r for r in results if r.status_code in OK]
    refused = [r for r in results if r.status_code in CONFLICT]
    assert len(accepted) == 1, (
        f"two PATCH /api/studio/work/{entry_id} requests from version {version} "
        f"answered {[r.status_code for r in results]}; exactly one is accepted"
    )
    assert len(refused) == 1, (
        f"the losing write answered {[r.status_code for r in results]}; a write from "
        f"a version that is no longer current is refused, never merged"
    )
    row = console.entry_by_id(entry_id) or {}
    assert row.get("version") == version + 1, (
        f"after one accepted write the stored version is {row.get('version')!r}, not "
        f"{version + 1}; an accepted write raises the version by exactly one"
    )


def test_reorder_naming_a_duplicate_position_is_refused_whole(owner_client, console):
    titles = [probe_title() for _ in range(2)]
    ids = []
    for title in titles:
        created = create_entry(owner_client, title=title)
        ids.append(entry_id_of(created, console, title))
    before = {str(i): (console.entry_by_id(i) or {}).get("position") for i in ids}
    versions = {str(i): (console.entry_by_id(i) or {}).get("version") for i in ids}
    bad = owner_client.put(api("/studio/shelf"),
                           json={"kind": "work", "order": [ids[0], ids[0]],
                                 "versions": versions})
    assert bad.status_code in REFUSED, (
        f"PUT /api/studio/shelf naming entry {ids[0]} twice answered "
        f"{bad.status_code}; a reorder naming one entry twice is refused. "
        f"Body: {body_text(bad)[:400]}"
    )
    after = {str(i): (console.entry_by_id(i) or {}).get("position") for i in ids}
    assert after == before, (
        f"the refused reorder changed stored positions from {before} to {after}; a "
        f"refused reorder writes nothing at all, never a partial order"
    )


def test_contact_message_is_persisted_as_an_unread_row(anon_client, console):
    email = probe_email()
    payload = new_message_payload(email=email)
    r = anon_client.post(api("/messages"), json=payload)
    assert r.status_code in OK, (
        f"POST /api/messages answered {r.status_code} for a valid submission. "
        f"Body: {body_text(r)[:400]}"
    )
    row = poll_until(lambda: console.message_by_email(email))
    assert row, (
        f"no message row exists for sender {email!r} after a successful "
        f"POST /api/messages; the submission must be stored, not only acknowledged"
    )
    assert row.get("state") == STATE_UNREAD, (
        f"the stored message for {email!r} carries state {row.get('state')!r} rather "
        f"than {STATE_UNREAD!r}; a new message arrives unread"
    )


def test_contact_message_body_is_stored_verbatim_without_markup(anon_client, console):
    email = probe_email()
    hostile = "<img src=x onerror=alert(1)> plain words follow this markup attempt"
    r = anon_client.post(api("/messages"), json=new_message_payload(email=email,
                                                                   body=hostile))
    assert r.status_code in OK, (
        f"POST /api/messages answered {r.status_code} for a body carrying markup. "
        f"Body: {body_text(r)[:400]}"
    )
    row = poll_until(lambda: console.message_by_email(email))
    assert row, f"no message row exists for sender {email!r} after a valid submission"
    assert row.get("body") == hostile, (
        f"the stored body for {email!r} reads {row.get('body')!r}; a message body is "
        f"stored as the characters that were typed, never rewritten or stripped"
    )


def test_draft_entry_detail_answers_gone_to_an_anonymous_caller(anon_client,
                                                                owner_client, console):
    title = probe_title()
    created = create_entry(owner_client, title=title)
    entry_id = entry_id_of(created, console, title)
    r = anon_client.get(api(f"/work/{entry_id}"))
    assert r.status_code in GONE_OR_MISSING, (
        f"GET /api/work/{entry_id} answered {r.status_code} for an unpublished entry "
        f"with no credential; a draft answers as gone, never as present and never as "
        f"a server failure. Body: {body_text(r)[:400]}"
    )


def test_draft_entry_is_absent_from_the_console_read(anon_client, owner_client, console):
    title = probe_title()
    created = create_entry(owner_client, title=title)
    assert created.status_code in OK, (
        f"POST /api/studio/work answered {created.status_code} for an owner. "
        f"Body: {body_text(created)[:400]}"
    )
    settle()
    titles = work_titles(console_payload(anon_client))
    assert title not in titles, (
        f"GET /api/console listed the unpublished entry {title!r} among {titles[:12]}; "
        f"an entry that is not published appears in no public read"
    )


def test_editor_publish_request_is_denied_and_leaves_published_false(editor_client,
                                                                     owner_client,
                                                                     console):
    title = probe_title()
    created = create_entry(owner_client, title=title)
    entry_id = entry_id_of(created, console, title)
    version = version_of(created, console, entry_id)
    r = editor_client.post(api(f"/studio/work/{entry_id}/publish"),
                           json={"version": version})
    assert r.status_code in DENIED, (
        f"POST /api/studio/work/{entry_id}/publish answered {r.status_code} from an "
        f"editor session; publishing is an owner capability and the refusal happens "
        f"at the server. Body: {body_text(r)[:400]}"
    )
    row = console.entry_by_id(entry_id) or {}
    assert row.get("published") in (False, 0, None), (
        f"after the denied editor publish, entry {entry_id} reads published "
        f"{row.get('published')!r}; a denied call leaves the protected state unchanged"
    )


def test_editor_inbox_request_is_denied(editor_client):
    r = editor_client.get(api("/studio/messages"))
    assert r.status_code in DENIED, (
        f"GET /api/studio/messages answered {r.status_code} from an editor session; "
        f"messages are readable by the owner only. Body: {body_text(r)[:400]}"
    )


def test_editor_shelf_write_is_denied_and_leaves_the_order_unchanged(editor_client,
                                                                     owner_client,
                                                                     console):
    titles = [probe_title() for _ in range(2)]
    ids = []
    for title in titles:
        created = create_entry(owner_client, title=title)
        ids.append(entry_id_of(created, console, title))
    before = {str(i): (console.entry_by_id(i) or {}).get("position") for i in ids}
    versions = {str(i): (console.entry_by_id(i) or {}).get("version") for i in ids}
    r = editor_client.put(api("/studio/shelf"),
                          json={"kind": "work", "order": [ids[1], ids[0]],
                                "versions": versions})
    assert r.status_code in DENIED, (
        f"PUT /api/studio/shelf answered {r.status_code} from an editor session; "
        f"reordering is an owner capability. Body: {body_text(r)[:400]}"
    )
    after = {str(i): (console.entry_by_id(i) or {}).get("position") for i in ids}
    assert after == before, (
        f"the denied editor reorder changed stored positions from {before} to {after}"
    )


def test_editor_page_view_log_request_is_denied(editor_client):
    r = editor_client.get(api("/studio/page-views"))
    assert r.status_code in DENIED, (
        f"GET /api/studio/page-views answered {r.status_code} from an editor session; "
        f"the page-view log is readable by the owner only. "
        f"Body: {body_text(r)[:400]}"
    )


def test_unauthenticated_studio_work_request_is_denied(anon_client):
    r = anon_client.get(api("/studio/work"))
    assert r.status_code in DENIED, (
        f"GET /api/studio/work answered {r.status_code} with no credential; every "
        f"studio path requires a session. Body: {body_text(r)[:400]}"
    )


def test_wrong_password_answer_names_neither_field(anon_client):
    r = anon_client.post(api("/auth/login"),
                         json={"email": OWNER_EMAIL, "password": f"wrong-{unique_suffix()}"})
    assert r.status_code in DENIED, (
        f"POST /api/auth/login answered {r.status_code} for a wrong password; a "
        f"failed sign-in is refused. Body: {body_text(r)[:400]}"
    )
    text = body_text(r).lower()
    for leak in ("unknown email", "no such account", "email not found",
                 "wrong password", "incorrect password", "password is wrong"):
        assert leak not in text, (
            f"the failed sign-in response named which field was wrong ({leak!r}); the "
            f"answer is the same for a wrong password and an unknown address. "
            f"Body: {body_text(r)[:400]}"
        )


def test_sign_in_failures_reach_the_lockout_limit(anon_client):
    probe = probe_email()
    statuses = []
    for _ in range(LOCKOUT_ATTEMPTS + 1):
        r = anon_client.post(api("/auth/login"),
                             json={"email": probe, "password": f"wrong-{unique_suffix()}"})
        statuses.append(r.status_code)
    assert all(s in REFUSED + DENIED for s in statuses), (
        f"repeated failed sign-ins for {probe!r} answered {statuses}; every one is "
        f"refused, and the run past the limit is refused too"
    )
    assert 423 in statuses or 429 in statuses or statuses[-1] in DENIED, (
        f"sign-in attempts past the limit answered {statuses}; the account locks "
        f"rather than accepting an unbounded run of attempts"
    )


def test_page_view_log_carries_no_network_address(anon_client, owner_client, console):
    route = "/product"
    posted = anon_client.post(api("/page-views"), json={"route": route})
    assert posted.status_code in ACCEPTED, (
        f"POST /api/page-views answered {posted.status_code} with no credential; "
        f"recording a public view needs no session. Body: {body_text(posted)[:400]}"
    )
    r = owner_client.get(api("/studio/page-views"))
    assert r.status_code == 200, (
        f"GET /api/studio/page-views answered {r.status_code} for an owner. "
        f"Body: {body_text(r)[:400]}"
    )
    text = body_text(r)
    import re as _re
    addresses = _re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)
    real = [a for a in addresses if a not in ("0.0.0.0", "127.0.0.1")]
    assert not real, (
        f"the page-view log carried what reads as a full network address {real[:5]}; "
        f"no page view record holds one"
    )


def test_security_headers_are_present_on_every_response(anon_client):
    r = anon_client.get(api("/health"))
    present = {k.lower() for k in r.headers}
    missing = [h for h in SECURITY_HEADERS if h not in present]
    assert not missing, (
        f"GET /api/health answered {r.status_code} without the security headers "
        f"{missing}; every response carries the whole set. Present: {sorted(present)}"
    )


def test_contact_form_refuses_a_missing_name_with_the_pinned_error(anon_client, console):
    email = probe_email()
    before = console.count_messages()
    r = anon_client.post(api("/messages"),
                         json=new_message_payload(email=email, name="   "))
    assert r.status_code in REFUSED, (
        f"POST /api/messages answered {r.status_code} for an empty name. "
        f"Body: {body_text(r)[:400]}"
    )
    assert ERROR_SENDER_NAME in body_text(r), (
        f"the refusal for an empty name did not carry {ERROR_SENDER_NAME!r}. "
        f"Body: {body_text(r)[:400]}"
    )
    assert console.count_messages() == before, (
        f"the refused submission wrote a message row; a refused form writes nothing"
    )


def test_contact_form_refuses_a_malformed_address_with_the_pinned_error(anon_client,
                                                                        console):
    before = console.count_messages()
    r = anon_client.post(api("/messages"),
                         json=new_message_payload(email="not-an-address"))
    assert r.status_code in REFUSED, (
        f"POST /api/messages answered {r.status_code} for a malformed address. "
        f"Body: {body_text(r)[:400]}"
    )
    assert ERROR_SENDER_EMAIL in body_text(r), (
        f"the refusal for a malformed address did not carry {ERROR_SENDER_EMAIL!r}. "
        f"Body: {body_text(r)[:400]}"
    )
    assert console.count_messages() == before, (
        f"the refused submission wrote a message row; a refused form writes nothing"
    )


def test_contact_form_refuses_a_short_body_with_the_pinned_error(anon_client, console):
    before = console.count_messages()
    r = anon_client.post(api("/messages"),
                         json=new_message_payload(email=probe_email(), body="Hi."))
    assert r.status_code in REFUSED, (
        f"POST /api/messages answered {r.status_code} for a body under the minimum. "
        f"Body: {body_text(r)[:400]}"
    )
    assert ERROR_MESSAGE_BODY in body_text(r), (
        f"the refusal for a short body did not carry {ERROR_MESSAGE_BODY!r}. "
        f"Body: {body_text(r)[:400]}"
    )
    assert console.count_messages() == before, (
        f"the refused submission wrote a message row; a refused form writes nothing"
    )


def test_decoy_field_submission_is_refused_and_writes_no_row(anon_client, console):
    email = probe_email()
    before = console.count_messages()
    r = anon_client.post(api("/messages"),
                         json=new_message_payload(email=email, decoy="filled in"))
    assert r.status_code in REFUSED + OK, (
        f"POST /api/messages answered {r.status_code} for a filled decoy field. "
        f"Body: {body_text(r)[:400]}"
    )
    settle()
    assert console.message_by_email(email) is None, (
        f"a submission with the decoy field filled stored a message row for {email!r}; "
        f"a decoy-filled submission writes nothing"
    )
    assert console.count_messages() == before, (
        f"the message row count moved from {before} to {console.count_messages()} on a "
        f"decoy-filled submission"
    )


def test_repeated_submissions_are_refused_after_the_third_from_one_address(anon_client,
                                                                          console):
    email = probe_email()
    statuses = []
    for n in range(MESSAGE_RATE_LIMIT + 1):
        r = anon_client.post(api("/messages"),
                             json=new_message_payload(email=email,
                                                      body=f"Message number {n} sent "
                                                           f"repeatedly in succession."))
        statuses.append(r.status_code)
    assert statuses[-1] in REFUSED, (
        f"four submissions from {email!r} inside one hour answered {statuses}; the "
        f"fourth is refused"
    )
    assert console.count_messages(sender_email=email) <= MESSAGE_RATE_LIMIT, (
        f"{console.count_messages(sender_email=email)} message rows exist for "
        f"{email!r}; no more than {MESSAGE_RATE_LIMIT} are accepted inside one hour"
    )


def test_entry_title_over_the_bound_is_refused_with_the_pinned_error(owner_client,
                                                                     console):
    before = console.count_entries()
    r = owner_client.post(api("/studio/work"),
                          json=new_entry_payload(title="   "))
    assert r.status_code in REFUSED, (
        f"POST /api/studio/work answered {r.status_code} for an empty title. "
        f"Body: {body_text(r)[:400]}"
    )
    assert ERROR_TITLE in body_text(r), (
        f"the refusal for an empty title did not carry {ERROR_TITLE!r}. "
        f"Body: {body_text(r)[:400]}"
    )
    long_title = "x" * (TITLE_MAX + 1)
    r2 = owner_client.post(api("/studio/work"),
                           json=new_entry_payload(title=long_title))
    assert r2.status_code in REFUSED, (
        f"POST /api/studio/work answered {r2.status_code} for a title of "
        f"{TITLE_MAX + 1} characters. Body: {body_text(r2)[:400]}"
    )
    assert console.count_entries() == before, (
        f"a refused entry write changed the entry row count from {before} to "
        f"{console.count_entries()}"
    )


def test_entry_year_outside_the_band_is_refused_with_the_pinned_error(owner_client,
                                                                      console):
    before = console.count_entries()
    r = owner_client.post(api("/studio/work"),
                          json=new_entry_payload(year=YEAR_MAX + 1))
    assert r.status_code in REFUSED, (
        f"POST /api/studio/work answered {r.status_code} for year {YEAR_MAX + 1}. "
        f"Body: {body_text(r)[:400]}"
    )
    assert ERROR_YEAR in body_text(r), (
        f"the refusal for an out-of-band year did not carry {ERROR_YEAR!r}. "
        f"Body: {body_text(r)[:400]}"
    )
    assert console.count_entries() == before, (
        f"a refused entry write changed the entry row count from {before} to "
        f"{console.count_entries()}"
    )


def test_entry_link_without_a_secure_scheme_is_refused(owner_client, console):
    before = console.count_entries()
    r = owner_client.post(api("/studio/work"),
                          json=new_entry_payload(
                              links=[{"label": "Case", "href": "javascript:alert(1)"}]))
    assert r.status_code in REFUSED, (
        f"POST /api/studio/work answered {r.status_code} for a link carrying a script "
        f"scheme. Body: {body_text(r)[:400]}"
    )
    assert ERROR_LINK in body_text(r), (
        f"the refusal for a bad link did not carry {ERROR_LINK!r}. "
        f"Body: {body_text(r)[:400]}"
    )
    assert console.count_entries() == before, (
        f"a refused entry write changed the entry row count from {before} to "
        f"{console.count_entries()}"
    )


def test_unknown_address_answers_not_found(anon_client):
    r = anon_client.get(f"/does-not-exist-{unique_suffix()}",
                        follow_redirects=True)
    assert r.status_code in (200, 404), (
        f"an unknown address answered {r.status_code}; it renders the product's own "
        f"not-found surface. Body: {body_text(r)[:400]}"
    )
    if r.status_code == 200:
        assert "404" in body_text(r) and "NOT FOUND" in body_text(r).upper(), (
            f"an unknown address rendered a page carrying neither the code nor the "
            f"not-found message. Body: {body_text(r)[:400]}"
        )


def test_unknown_failure_code_renders_the_generic_surface(anon_client):
    r = anon_client.get("/error", params={"code": "999", "message": "NONSENSE"},
                        follow_redirects=True)
    text = body_text(r)
    assert "NONSENSE" not in text, (
        f"the failure surface echoed the message from the address; a code outside the "
        f"closed table renders the generic surface instead. Body: {text[:400]}"
    )
    assert "SOMETHING BROKE" in text.upper() or "500" in text, (
        f"the failure surface answered {r.status_code} without the generic copy for a "
        f"code outside the closed table. Body: {text[:400]}"
    )


def test_public_routes_declare_distinct_titles_and_preview_images(anon_client):
    import re as _re
    titles, images = {}, {}
    for route in PUBLIC_ROUTES:
        r = anon_client.get(route, follow_redirects=True)
        assert r.status_code == 200, (
            f"GET {route} answered {r.status_code}; every public destination is served "
            f"to a visitor with no credential. Body: {body_text(r)[:400]}"
        )
        html = body_text(r)
        m = _re.search(r"<title[^>]*>(.*?)</title>", html, _re.S | _re.I)
        titles[route] = (m.group(1).strip() if m else "")
        m2 = _re.search(r'<meta[^>]+property=["\']og:image["\'][^>]*content=["\']([^"\']+)',
                        html, _re.I)
        if not m2:
            m2 = _re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']',
                            html, _re.I)
        images[route] = (m2.group(1) if m2 else "")
    empty = [r for r, t in titles.items() if not t]
    assert not empty, f"these routes declared no document title: {empty}"
    assert len(set(titles.values())) == len(titles), (
        f"two public destinations share a title: {titles}"
    )
    missing = [r for r, v in images.items() if not v]
    assert not missing, (
        f"these routes declared no social preview image: {missing}. Declared: {images}"
    )
    origin = app_origin()
    target = images[PUBLIC_ROUTES[0]]
    url = target if target.startswith("http") else f"{origin}/{target.lstrip('/')}"
    with httpx.Client(timeout=30.0) as c:
        got = c.get(url, follow_redirects=True)
    assert got.status_code == 200 and got.content, (
        f"the declared preview image {url} answered {got.status_code} with "
        f"{len(got.content)} bytes; a declared preview image resolves to real bytes"
    )


def test_editor_refusal_surface_carries_the_pinned_explanation(anon_client,
                                                               editor_client):
    r = editor_client.get(api("/studio/messages"))
    assert r.status_code in DENIED, (
        f"GET /api/studio/messages answered {r.status_code} from an editor session. "
        f"Body: {body_text(r)[:400]}"
    )
    page = anon_client.get("/error", params={"code": "403", "message": "NOT PERMITTED"},
                           follow_redirects=True)
    text = body_text(page)
    assert "NOT PERMITTED" in text.upper(), (
        f"the failure surface at code 403 did not render the pinned message. "
        f"Body: {text[:400]}"
    )
    assert REFUSAL_EXPLANATION in text or "403" in text, (
        f"the refusal surface carried neither the code nor {REFUSAL_EXPLANATION!r}. "
        f"Body: {text[:400]}"
    )


def test_owner_invites_an_editor_and_an_editor_is_denied(owner_client, editor_client):
    probe = probe_email()
    created = owner_client.post(api("/studio/editors"), json={"email": probe})
    assert created.status_code in OK, (
        f"POST /api/studio/editors answered {created.status_code} for an owner "
        f"inviting {probe!r}; inviting an editor is an owner capability. "
        f"Body: {body_text(created)[:400]}"
    )
    denied = editor_client.post(api("/studio/editors"), json={"email": probe_email()})
    assert denied.status_code in DENIED, (
        f"POST /api/studio/editors answered {denied.status_code} from an editor "
        f"session; inviting is the owner's alone. Body: {body_text(denied)[:400]}"
    )
    listed = editor_client.get(api("/studio/editors"))
    assert listed.status_code in DENIED, (
        f"GET /api/studio/editors answered {listed.status_code} from an editor "
        f"session. Body: {body_text(listed)[:400]}"
    )


def test_editor_authored_entry_records_the_editor_as_its_author(editor_client, console):
    title = probe_title()
    created = create_entry(editor_client, title=title)
    assert created.status_code in OK, (
        f"POST /api/studio/work answered {created.status_code} for an editor; an "
        f"editor may create an entry. Body: {body_text(created)[:400]}"
    )
    entry_id = entry_id_of(created, console, title)
    row = console.entry_by_id(entry_id) or {}
    account = console.account_by_email(EDITOR_EMAIL) or {}
    assert row.get("author_id") is not None, (
        f"entry {entry_id} created by an editor carries no author_id; authorship is "
        f"a field on the record so the work survives its author's removal"
    )
    assert str(row.get("author_id")) == str(account.get("id")), (
        f"entry {entry_id} records author_id {row.get('author_id')!r}, which is not "
        f"the editor account id {account.get('id')!r} that created the entry"
    )
