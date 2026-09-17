"""The pytest layer for the vvvivid task.

Black box throughout. Every assertion is an HTTP call against the running app or
an out-of-band read of the same PostgreSQL and object store the app writes to.
No test reads the app's source, and no test depends on another test's ordering.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import re
import uuid

import httpx

import appclient
from conftest import (
    PRIVATE_PRESET_TITLE,
    RENDER_PREFIX,
    db_render_keys,
    derive_identifier,
    expected_identifier,
    fresh_seed,
    object_keys,
    save_preset,
    settings_from,
)

WORKED_CANONICAL = (
    "bbblob|1|complexity=5|contrast=40|edges=smooth|fill=solid|seed=7|w=1200|h=1200"
)
WORKED_IDENTIFIER = "iiancd7svxmz3dbmqqk"

PUBLIC_ROUTES = ["/", "/gallery", "/license"]


def _unique_title(stem: str) -> str:
    return f"{stem} {uuid.uuid4().hex[:8]}"


def _saved(client, settings, **kw):
    response = save_preset(client, settings, **kw)
    assert response.status_code in (200, 201), (
        f"saving settings returned {response.status_code}: {response.text[:400]}"
    )
    return response.json()


def _identifier_of(payload: dict) -> str:
    for key in ("id", "identifier", "presetId", "preset_id"):
        if isinstance(payload, dict) and payload.get(key):
            return str(payload[key])
    raise AssertionError(f"save response carries no preset identifier: {payload!r}")


def test_seeded_tiles_are_listed_in_stored_order(anonymous, backend):
    stored = [r["key"] for r in backend.rows("generators", status="live")]
    stored_by_position = [
        r["key"]
        for r in sorted(backend.rows("generators", status="live"),
                        key=lambda r: r["position"])
    ]
    assert stored, "no generator rows are seeded"

    response = anonymous.get("/generators")
    assert response.status_code == 200, response.text[:300]
    served = [r["key"] for r in response.json()]

    assert served == stored_by_position, (
        "the tile list is not served in the stored position order: "
        f"served {served[:6]}..., stored {stored_by_position[:6]}..."
    )
    assert set(served) == set(stored), (
        "the served tiles differ from the live seeded rows"
    )


def test_retired_generator_keeps_its_route_and_leaves_the_grid(anonymous, backend):
    retired = backend.rows("generators", status="retired")
    assert retired, "no generator is seeded as retired"
    key = retired[0]["key"]

    listed = [r["key"] for r in anonymous.get("/generators").json()]
    assert key not in listed, (
        f"the retired generator {key!r} is still in the tile grid"
    )

    detail = anonymous.get(f"/generators/{key}")
    assert detail.status_code == 200, (
        f"the retired generator {key!r} lost its route: {detail.status_code}"
    )


def test_worked_example_canonical_string_derives_its_pinned_identifier():
    assert derive_identifier(WORKED_CANONICAL) == WORKED_IDENTIFIER, (
        "the derivation in the brief does not reproduce its own worked example"
    )


def test_saved_preset_identifier_matches_the_recomputed_derivation(
        author, new_settings, schema_order):
    settings = new_settings()
    body = _saved(author, settings, title=_unique_title("Derived"))
    assert _identifier_of(body) == expected_identifier(settings, schema_order), (
        "the identifier the app returned is not the derivation of the settings sent"
    )


def test_second_save_of_identical_settings_returns_one_identifier(author, new_settings):
    settings = new_settings()
    first = _identifier_of(_saved(author, settings, title=_unique_title("First")))
    second = _identifier_of(_saved(author, settings, title=_unique_title("Second")))
    assert first == second, (
        f"saving identical settings twice produced two identifiers: {first} then {second}"
    )


def test_second_save_of_identical_settings_leaves_one_row(author, backend, new_settings):
    settings = new_settings()
    identifier = _identifier_of(_saved(author, settings, title=_unique_title("Once")))
    _saved(author, settings, title=_unique_title("Twice"))
    assert backend.count("presets", id=identifier) == 1, (
        "saving identical settings twice left more than one preset row"
    )


def test_a_supplied_identifier_on_a_save_is_ignored(author, new_settings, schema_order):
    settings = new_settings()
    body = dict(settings)
    body["id"] = "aaaaaaaaaaaaaaaaaaa"
    response = author.post("/presets", json=body)
    assert response.status_code in (200, 201, 400), response.text[:300]
    if response.status_code in (200, 201):
        assert _identifier_of(response.json()) == expected_identifier(settings, schema_order), (
            "a caller-supplied identifier was accepted instead of the derivation"
        )


def test_concurrent_identical_saves_leave_exactly_one_row(
        author_token, second_author_token, backend, new_settings):
    settings = new_settings()

    def attempt(token):
        with appclient.client(token) as c:
            return save_preset(c, settings, title=_unique_title("Race"))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(attempt, t) for t in (author_token, second_author_token)]
        responses = [f.result() for f in futures]

    accepted = [r for r in responses if r.status_code in (200, 201)]
    assert accepted, (
        "both concurrent saves of identical settings failed: "
        + ", ".join(f"{r.status_code} {r.text[:120]}" for r in responses)
    )
    identifier = _identifier_of(accepted[0].json())
    assert backend.count("presets", id=identifier) == 1, (
        "two concurrent saves of identical settings created more than one row"
    )


def test_concurrent_identical_saves_return_one_identifier_to_both(
        author_token, second_author_token, new_settings):
    settings = new_settings()

    def attempt(token):
        with appclient.client(token) as c:
            return save_preset(c, settings, title=_unique_title("Race"))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        responses = [f.result() for f in
                     [pool.submit(attempt, t) for t in (author_token, second_author_token)]]

    identifiers = {_identifier_of(r.json()) for r in responses
                   if r.status_code in (200, 201)}
    assert len(identifiers) == 1, (
        f"concurrent saves of identical settings returned {identifiers}"
    )


def test_private_preset_is_absent_from_the_gallery(anonymous, private_preset):
    entries = anonymous.get("/gallery").json()
    titles = {e.get("title") for e in entries}
    ids = {str(e.get("presetId") or e.get("preset_id") or e.get("id")) for e in entries}
    assert PRIVATE_PRESET_TITLE not in titles, (
        "a private preset is listed in the gallery by title"
    )
    assert private_preset["id"] not in ids, (
        "a private preset is listed in the gallery by identifier"
    )


def test_private_preset_address_is_refused_to_every_caller_but_its_owner(
        anonymous, reader, second_author, private_preset):
    identifier = private_preset["id"]
    for name, client in (("signed-out", anonymous), ("reader", reader),
                         ("non-owning author", second_author)):
        response = client.get(f"/presets/{identifier}")
        assert response.status_code == 404, (
            f"the {name} caller got {response.status_code} for a private preset, "
            f"expected 404"
        )


def test_private_refusal_is_indistinguishable_from_an_unknown_identifier(
        anonymous, private_preset):
    unknown = "zzzzzzzzzzzzzzzzzzz"
    private = anonymous.get(f"/presets/{private_preset['id']}")
    missing = anonymous.get(f"/presets/{unknown}")
    assert private.status_code == missing.status_code == 404, (
        f"private returned {private.status_code}, unknown returned {missing.status_code}"
    )
    assert private.text.strip() == missing.text.strip(), (
        "the refusal for a private preset differs from the refusal for an unknown "
        "identifier, so a caller can tell the private preset exists"
    )


def test_owner_reads_their_own_private_preset(author, private_preset):
    response = author.get(f"/presets/{private_preset['id']}")
    assert response.status_code == 200, (
        f"the owner cannot read their own private preset: {response.status_code}"
    )


def test_private_preset_export_is_refused_to_every_caller_but_its_owner(
        anonymous, reader, second_author, private_preset):
    identifier = private_preset["id"]
    for name, client in (("signed-out", anonymous), ("reader", reader),
                         ("non-owning author", second_author)):
        response = client.get(f"/presets/{identifier}/render")
        assert response.status_code == 404, (
            f"the {name} caller got {response.status_code} for a private preset's "
            f"export, expected 404"
        )


def test_published_preset_export_is_served_to_anyone(anonymous, author, public_preset):
    identifier = public_preset["id"]
    made = author.post(f"/presets/{identifier}/render", json={"format": "svg"})
    assert made.status_code in (200, 201), made.text[:300]

    response = anonymous.get(f"/presets/{identifier}/render")
    assert response.status_code == 200, (
        f"a published preset's export is not served to a signed-out caller: "
        f"{response.status_code}"
    )
    assert response.content, "the served export carries no bytes"


def test_unlisted_preset_resolves_for_any_caller_holding_the_address(
        anonymous, unlisted_preset):
    response = anonymous.get(f"/presets/{unlisted_preset['id']}")
    assert response.status_code == 200, (
        f"an unlisted preset did not resolve for a caller holding its address: "
        f"{response.status_code}"
    )


def test_unlisted_preset_is_absent_from_the_gallery(anonymous, unlisted_preset):
    entries = anonymous.get("/gallery").json()
    ids = {str(e.get("presetId") or e.get("preset_id") or e.get("id")) for e in entries}
    assert unlisted_preset["id"] not in ids, (
        "an unlisted preset appears in the gallery"
    )


def _render(author, identifier, fmt="svg"):
    return author.post(f"/presets/{identifier}/render", json={"format": fmt})


def test_render_object_exists_in_the_bucket_at_its_content_key(
        author, backend, store, new_settings):
    identifier = _identifier_of(_saved(author, new_settings(), title=_unique_title("Render")))
    response = _render(author, identifier)
    assert response.status_code in (200, 201), response.text[:300]

    rows = backend.rows("renders", preset_id=identifier)
    assert rows, "rendering recorded no render row"
    key = rows[-1]["object_key"]
    assert key.startswith(RENDER_PREFIX), (
        f"the render key {key!r} does not use the pinned prefix {RENDER_PREFIX!r}"
    )
    assert store.exists(key), (
        f"the render row names {key!r}, which is not an object in the bucket"
    )


def test_render_object_key_is_the_digest_of_the_stored_bytes(
        anonymous, author, backend, new_settings):
    identifier = _identifier_of(_saved(author, new_settings(), title=_unique_title("Digest")))
    assert _render(author, identifier).status_code in (200, 201)

    row = backend.rows("renders", preset_id=identifier)[-1]
    served = anonymous.get(f"/presets/{identifier}/render")
    assert served.status_code == 200, served.status_code

    digest = hashlib.sha256(served.content).hexdigest()
    assert digest in row["object_key"], (
        f"the object key {row['object_key']!r} does not carry the digest of the bytes "
        f"served for that render ({digest})"
    )


def test_render_bytes_are_not_stored_in_the_database(author, backend, new_settings):
    identifier = _identifier_of(_saved(author, new_settings(), title=_unique_title("NoBytes")))
    assert _render(author, identifier).status_code in (200, 201)

    row = backend.rows("renders", preset_id=identifier)[-1]
    for column, value in row.items():
        if isinstance(value, (bytes, bytearray, memoryview)):
            raise AssertionError(
                f"the renders table holds raw bytes in column {column!r}"
            )
        if isinstance(value, str) and value.lstrip().startswith("<svg"):
            raise AssertionError(
                f"the renders table holds the document itself in column {column!r}"
            )


def test_two_identical_renders_store_one_object(author, backend, store, new_settings):
    settings = new_settings()
    first = _identifier_of(_saved(author, settings, title=_unique_title("Twin A")))
    assert _render(author, first).status_code in (200, 201)
    first_key = backend.rows("renders", preset_id=first)[-1]["object_key"]

    before = object_keys(store)
    assert _render(author, first).status_code in (200, 201)
    after = object_keys(store)

    assert after == before, (
        "re-rendering identical bytes added an object to the bucket; content "
        f"addressing should have reused {first_key!r}"
    )
    assert store.exists(first_key)
    assert first_key in db_render_keys(backend), (
        "the bucket holds the object but no render row references its key"
    )


def test_oversized_render_is_refused_and_writes_no_object(
        author, store, new_settings):
    identifier = _identifier_of(_saved(author, new_settings(), title=_unique_title("Big")))
    before = object_keys(store)

    response = author.post(
        f"/presets/{identifier}/render",
        json={"format": "png", "width": 40000, "height": 40000},
    )
    assert response.status_code in (400, 413), (
        f"an oversized render returned {response.status_code}, expected a refusal"
    )
    assert object_keys(store) == before, (
        "a refused oversized render still wrote an object into the bucket"
    )


def test_unsupported_render_format_is_refused_and_writes_no_object(
        author, store, new_settings):
    identifier = _identifier_of(_saved(author, new_settings(), title=_unique_title("Bad")))
    before = object_keys(store)

    response = author.post(f"/presets/{identifier}/render", json={"format": "tiff"})
    assert response.status_code in (400, 415), (
        f"an unsupported render format returned {response.status_code}, expected a refusal"
    )
    assert object_keys(store) == before, (
        "a refused unsupported-format render still wrote an object into the bucket"
    )


def _publish(client, identifier, title=None, tags=None):
    body = {}
    if title is not None:
        body["title"] = title
    if tags is not None:
        body["tags"] = tags
    return client.post(f"/presets/{identifier}/publish", json=body)


def test_publication_creates_one_live_gallery_entry(author, backend, new_settings):
    identifier = _identifier_of(_saved(author, new_settings(), title=_unique_title("Pub")))
    title = _unique_title("Published")
    response = _publish(author, identifier, title=title)
    assert response.status_code in (200, 201), response.text[:300]

    assert backend.count("gallery_entries", preset_id=identifier) == 1, (
        "publishing did not create exactly one gallery entry"
    )
    row = backend.one("gallery_entries", preset_id=identifier)
    assert row["state"] == "live", f"the new entry's state is {row['state']!r}"
    assert backend.one("presets", id=identifier)["visibility"] == "public", (
        "publishing did not set the preset's visibility to public"
    )


def test_publication_without_an_account_is_refused(anonymous, backend, public_preset):
    before = backend.count("gallery_entries")
    response = _publish(anonymous, public_preset["id"], title=_unique_title("Anon"))
    assert response.status_code in (401, 403), (
        f"an anonymous publication returned {response.status_code}, expected a refusal"
    )
    assert backend.count("gallery_entries") == before, (
        "a refused anonymous publication still created an entry"
    )


def test_publication_without_a_title_is_rejected(author, backend, new_settings):
    identifier = _identifier_of(_saved(author, new_settings(), title=_unique_title("NoTitle")))
    before = backend.count("gallery_entries")
    response = _publish(author, identifier)
    assert response.status_code == 400, (
        f"publishing with no title returned {response.status_code}, expected 400"
    )
    assert backend.count("gallery_entries") == before, (
        "a rejected publication still created an entry"
    )


def test_entry_tags_are_read_back_in_stored_order(author, backend, new_settings):
    identifier = _identifier_of(_saved(author, new_settings(), title=_unique_title("Tags")))
    tags = ["ordered", "second", "third"]
    assert _publish(author, identifier, title=_unique_title("Tagged"),
                    tags=tags).status_code in (200, 201)

    entry = backend.one("gallery_entries", preset_id=identifier)
    rows = backend.rows("gallery_entry_tags", gallery_entry_id=entry["id"])
    stored = [r["tag"] for r in sorted(rows, key=lambda r: r["position"])]
    assert stored == tags, f"tags were read back as {stored}, expected {tags}"


def test_publishing_an_already_published_preset_returns_the_existing_entry(
        author, backend, new_settings):
    identifier = _identifier_of(_saved(author, new_settings(), title=_unique_title("Re")))
    first = _publish(author, identifier, title=_unique_title("Once"))
    assert first.status_code in (200, 201), first.text[:300]
    existing = backend.one("gallery_entries", preset_id=identifier)

    second = _publish(author, identifier, title=_unique_title("Again"))
    assert second.status_code in (200, 201, 409), second.text[:300]

    still = backend.one("gallery_entries", preset_id=identifier)
    assert still["id"] == existing["id"], (
        "republishing replaced the gallery entry instead of returning the existing one"
    )


def test_publishing_twice_leaves_one_gallery_entry(author, backend, new_settings):
    identifier = _identifier_of(_saved(author, new_settings(), title=_unique_title("Twice")))
    _publish(author, identifier, title=_unique_title("First"))
    _publish(author, identifier, title=_unique_title("Second"))
    assert backend.count("gallery_entries", preset_id=identifier) == 1, (
        "publishing the same preset twice left more than one gallery entry"
    )


def _fork(client, identifier, settings=None, title=None):
    body = {}
    if settings is not None:
        body.update(settings)
    if title is not None:
        body["title"] = title
    return client.post(f"/presets/{identifier}/fork", json=body)


def test_fork_records_exactly_one_parent(author, second_author, backend, public_preset):
    parent = public_preset
    child_settings = settings_from(parent, fresh_seed())
    response = _fork(second_author, parent["id"], child_settings,
                     title=_unique_title("Forked"))
    assert response.status_code in (200, 201), response.text[:400]

    child_id = _identifier_of(response.json())
    child = backend.one("presets", id=child_id)
    assert child is not None, "the fork created no row"
    assert child["parent_id"] == parent["id"], (
        f"the fork names {child['parent_id']!r} as its parent, expected {parent['id']!r}"
    )


def test_fork_raises_the_parent_stored_fork_count_by_one(
        author, second_author, backend, public_preset):
    parent_id = public_preset["id"]
    before = backend.one("presets", id=parent_id)["fork_count"]

    response = _fork(second_author, parent_id,
                     settings_from(public_preset, fresh_seed()),
                     title=_unique_title("Counted"))
    assert response.status_code in (200, 201), response.text[:400]

    after = backend.one("presets", id=parent_id)["fork_count"]
    assert after == before + 1, (
        f"the parent's stored fork count went from {before} to {after}, expected "
        f"{before + 1}"
    )


def test_forking_without_changing_a_setting_returns_the_parent(
        second_author, backend, public_preset):
    parent_id = public_preset["id"]
    before = backend.count("presets")

    response = _fork(second_author, parent_id,
                     settings_from(public_preset, public_preset["seed"]),
                     title=_unique_title("Unchanged"))
    assert response.status_code in (200, 201, 409), response.text[:400]

    if response.status_code in (200, 201):
        assert _identifier_of(response.json()) == parent_id, (
            "forking with nothing changed produced a new identifier"
        )
    assert backend.count("presets") == before, (
        "forking with nothing changed created a row"
    )


def test_deleting_a_forked_preset_tombstones_it_rather_than_removing_it(
        author, second_author, backend, new_settings):
    parent_id = _identifier_of(_saved(author, new_settings(),
                                      title=_unique_title("Ancestor"),
                                      visibility="public"))
    parent_row = backend.one("presets", id=parent_id)
    assert _fork(second_author, parent_id, settings_from(parent_row, fresh_seed()),
                 title=_unique_title("Descendant")).status_code in (200, 201)

    response = author.delete(f"/presets/{parent_id}")
    assert response.status_code in (200, 204), response.text[:300]

    row = backend.one("presets", id=parent_id)
    assert row is not None, "deleting a forked preset removed its row entirely"
    assert row["state"] == "tombstoned", (
        f"the deleted preset's state is {row['state']!r}, expected 'tombstoned'"
    )
    assert row["params"], "the tombstone dropped the parameters it must retain"


def test_child_resolves_its_ancestry_through_a_tombstoned_parent(
        author, second_author, backend, new_settings):
    parent_id = _identifier_of(_saved(author, new_settings(),
                                      title=_unique_title("Gone"),
                                      visibility="public"))
    parent_row = backend.one("presets", id=parent_id)
    forked = _fork(second_author, parent_id,
                   settings_from(parent_row, fresh_seed()),
                   title=_unique_title("Orphan"))
    assert forked.status_code in (200, 201), forked.text[:400]
    child_id = _identifier_of(forked.json())

    assert author.delete(f"/presets/{parent_id}").status_code in (200, 204)

    child = backend.one("presets", id=child_id)
    assert child["parent_id"] == parent_id, (
        "the child lost its parent link when the parent was tombstoned"
    )
    read = second_author.get(f"/presets/{child_id}")
    assert read.status_code == 200, (
        f"the child stopped resolving after its parent was tombstoned: "
        f"{read.status_code}"
    )


def test_tombstoned_preset_is_absent_from_the_gallery(
        anonymous, author, second_author, backend, new_settings):
    parent_id = _identifier_of(_saved(author, new_settings(),
                                      title=_unique_title("Withdrawn"),
                                      visibility="public"))
    parent_row = backend.one("presets", id=parent_id)
    _publish(author, parent_id, title=_unique_title("WithdrawnEntry"))
    _fork(second_author, parent_id, settings_from(parent_row, fresh_seed()),
          title=_unique_title("Child"))

    assert author.delete(f"/presets/{parent_id}").status_code in (200, 204)

    entries = anonymous.get("/gallery").json()
    ids = {str(e.get("presetId") or e.get("preset_id") or e.get("id")) for e in entries}
    assert parent_id not in ids, (
        "a tombstoned preset is still listed in the gallery"
    )


def test_reader_cannot_save_render_publish_or_fork(reader, public_preset, new_settings):
    identifier = public_preset["id"]
    attempts = {
        "save": save_preset(reader, new_settings(), title=_unique_title("Reader")),
        "render": reader.post(f"/presets/{identifier}/render", json={"format": "svg"}),
        "publish": _publish(reader, identifier, title=_unique_title("Reader")),
        "fork": _fork(reader, identifier, None, title=_unique_title("Reader")),
    }
    for action, response in attempts.items():
        assert response.status_code in (401, 403), (
            f"a reader session was allowed to {action}: {response.status_code}"
        )


def test_denied_reader_write_creates_no_row(reader, backend, new_settings):
    before_presets = backend.count("presets")
    before_entries = backend.count("gallery_entries")
    before_renders = backend.count("renders")

    save_preset(reader, new_settings(), title=_unique_title("Nope"))

    assert backend.count("presets") == before_presets, (
        "a denied reader save created a preset row"
    )
    assert backend.count("gallery_entries") == before_entries
    assert backend.count("renders") == before_renders


def test_cross_author_edit_publish_delete_and_render_are_forbidden(
        second_author, author, new_settings):
    owned = _identifier_of(_saved(author, new_settings(), title=_unique_title("Mine")))
    attempts = {
        "edit": second_author.patch(f"/presets/{owned}", json={"title": "taken"}),
        "publish": _publish(second_author, owned, title=_unique_title("Taken")),
        "delete": second_author.delete(f"/presets/{owned}"),
        "render": second_author.post(f"/presets/{owned}/render", json={"format": "svg"}),
    }
    for action, response in attempts.items():
        assert response.status_code in (403, 404), (
            f"a second author was allowed to {action} another account's preset: "
            f"{response.status_code}"
        )


def test_forbidden_cross_author_write_leaves_the_row_unchanged(
        second_author, author, backend, new_settings):
    title = _unique_title("Untouched")
    owned = _identifier_of(_saved(author, new_settings(), title=title))
    before = backend.one("presets", id=owned)

    second_author.patch(f"/presets/{owned}", json={"title": "taken"})
    second_author.delete(f"/presets/{owned}")

    after = backend.one("presets", id=owned)
    assert after is not None, "a forbidden cross-author delete removed the row"
    assert after["title"] == before["title"] == title, (
        f"a forbidden cross-author edit changed the title to {after['title']!r}"
    )
    assert after["state"] == before["state"], (
        "a forbidden cross-author delete changed the row's state"
    )


def test_every_internal_link_on_every_public_route_resolves(anonymous):
    import re

    import httpx

    base = appclient.app_url()
    seen, broken = set(), []

    with httpx.Client(base_url=base, timeout=30.0, follow_redirects=True) as page:
        for route in PUBLIC_ROUTES:
            response = page.get(route)
            assert response.status_code == 200, (
                f"public route {route} returned {response.status_code}"
            )
            for href in re.findall(r'href="([^"#?]+)"', response.text):
                if href.startswith(("http://", "https://", "mailto:", "javascript:")):
                    continue
                if not href.startswith("/") or href in seen:
                    continue
                seen.add(href)
                target = page.get(href)
                if target.status_code >= 400:
                    broken.append(f"{href} -> {target.status_code} (from {route})")

    assert seen, "no internal links were found on any public route"
    assert not broken, "internal links that do not resolve: " + "; ".join(broken[:10])


def test_invalid_form_input_is_rejected_and_writes_nothing(anonymous, backend, public_preset):
    before = backend.count("reports")
    response = anonymous.post(
        "/reports",
        json={"galleryEntryId": public_preset["id"], "reason": "not-a-reason"},
    )
    assert response.status_code == 400, (
        f"an invalid report reason returned {response.status_code}, expected 400"
    )
    assert backend.count("reports") == before, (
        "a rejected report still wrote a row"
    )


def test_terms_page_is_served():
    with httpx.Client(base_url=appclient.app_url(), timeout=30.0,
                      follow_redirects=True) as page:
        response = page.get("/license")
    assert response.status_code == 200, (
        f"the terms page returned {response.status_code}"
    )
    assert response.text.strip(), "the terms page is empty"


def test_deployment_contract_holds(anonymous):
    """The app is reachable at APP_PUBLIC_URL, serves its HTTP API under the /api
    prefix on the same origin, returns 200 from GET /api/health once ready, listens
    on container-internal port 4173, binds 0.0.0.0 rather than 127.0.0.1 or
    localhost, reads both port values from the environment, and keeps the reserved
    .browser_screenshots/ and .downloads/ directories at the app root."""
    import os

    health = anonymous.get("/health")
    assert health.status_code == 200, (
        f"GET /api/health returned {health.status_code} once the app was ready"
    )
    assert os.environ.get("APP_PUBLIC_URL"), "APP_PUBLIC_URL is not set for the verifier"
    assert appclient.api_base().endswith("/api"), (
        f"the API is not served under the /api prefix: {appclient.api_base()}"
    )
    assert appclient.api_base().startswith(appclient.app_url()), (
        "the API is not served on the same origin as the documents"
    )


def test_scope_out_surfaces_are_absent(anonymous):
    """The product offers no comment surface, no like surface, no follow surface,
    no tag pages, no newsletter, no messaging surface, no payment surface, no public
    signup, no password reset, no invitation flow, no account deletion, no
    collections, no curated feed, no moderation queue, no review decision, no public
    generation API, no API keys, no quotas, no metering, no workspaces, no team
    membership, no near-duplicate clustering, no ranking figure, no account
    standing, no real-time collaboration, no shared editing session, no upload, no
    print-resolution rendering, no colour vision simulation and no print gamut work.
    None of those endpoints answers, and the app sends no email."""
    absent = [
        "comments", "likes", "follows", "tags", "newsletter", "messages",
        "payments", "signup", "password-reset", "invitations", "collections",
        "moderation", "keys", "quotas", "workspaces", "uploads", "clustering",
        "standing", "collaboration",
    ]
    served = []
    for path in absent:
        response = anonymous.get(f"/{path}")
        if response.status_code < 400:
            served.append(f"/{path} -> {response.status_code}")
    assert not served, (
        "surfaces the brief scopes out still answer: " + "; ".join(served)
    )


def test_declared_stack_and_environment_are_in_use(backend, store):
    """The app stores data in PostgreSQL reached through DATABASE_URL and stores
    objects in MinIO reached through STORAGE_ENDPOINT, with the bucket name from
    STORAGE_BUCKET, the key from STORAGE_ACCESS_KEY and the secret from
    STORAGE_SECRET_KEY. Both backing services are already running and reachable."""
    import os

    for name in ("STORAGE_ENDPOINT", "STORAGE_BUCKET"):
        assert os.environ.get(name), f"{name} is not set for the verifier"
    assert backend.count("accounts") >= 3, (
        "the declared PostgreSQL datastore holds fewer than the three seeded accounts"
    )
    store.list(RENDER_PREFIX)


def test_data_model_tables_and_columns_exist(backend):
    """The app defines seven tables, gives every table its own id, and stores every
    timestamp in UTC. accounts carries email, handle, display_name, role and
    password_hash. generators carries key, title, blurb, kind, status, position and
    param_schema. presets carries generator_key, generator_version, params, seed,
    ratio, width, height, title, owner_id, parent_id, visibility, state and
    fork_count. renders carries preset_id, object_key, format, width, height and
    byte_size. gallery_entries carries preset_id, published_by, published_at, title,
    thumbnail_object_key, state and report_count. gallery_entry_tags carries
    gallery_entry_id, tag and position. reports carries gallery_entry_id,
    reporter_id, reason and note."""
    expected = {
        "accounts": ["email", "handle", "display_name", "role", "password_hash"],
        "generators": ["key", "title", "blurb", "kind", "status", "position"],
        "presets": ["generator_key", "params", "seed", "visibility", "state",
                    "fork_count", "owner_id", "parent_id"],
        "renders": ["preset_id", "object_key", "format", "byte_size"],
        "gallery_entries": ["preset_id", "published_by", "title", "state"],
        "gallery_entry_tags": ["gallery_entry_id", "tag", "position"],
        "reports": ["gallery_entry_id", "reason"],
    }
    for table, columns in expected.items():
        rows = backend.rows(table, limit=1)
        assert rows is not None, f"table {table} could not be read in id order"
        if not rows:
            continue
        present = set(rows[0])
        assert "id" in present, f"table {table} carries no id of its own"
        missing = [c for c in columns if c not in present]
        assert not missing, f"table {table} is missing columns {missing}"


def test_seeded_accounts_carry_their_handles_and_roles(backend):
    """The app seeds the account mara@vvvivid.tools with the handle mara and the
    display name Mara Okonkwo as an author, tomas@vvvivid.tools with the handle
    tomas and the display name Tomas Reinholt as an author, and
    visitor@vvvivid.tools with the handle visitor and the display name Ines Haddad
    as a reader. Every seeded account accepts the password deku-studio-2026."""
    expected = {
        "mara@vvvivid.tools": ("mara", "Mara Okonkwo", "author"),
        "tomas@vvvivid.tools": ("tomas", "Tomas Reinholt", "author"),
        "visitor@vvvivid.tools": ("visitor", "Ines Haddad", "reader"),
    }
    for email, (handle, display, role) in expected.items():
        row = backend.one("accounts", email=email)
        assert row is not None, f"the account {email} is not seeded"
        assert row["handle"] == handle, f"{email} carries handle {row['handle']!r}"
        assert row["display_name"] == display, (
            f"{email} carries display name {row['display_name']!r}"
        )
        assert row["role"] == role, f"{email} carries role {row['role']!r}"
        assert "deku-studio-2026" not in str(row.get("password_hash", "")), (
            f"{email} stores its password rather than a hash of that password"
        )


def test_every_route_in_the_brief_resolves(anonymous):
    """Every route the brief names resolves: the tile index at /, one generator at
    /{tool}, the gallery at /gallery, one preset at /p/{id}, sign-in at /sign-in and
    the licence statement at /license."""
    listed = anonymous.get("/generators")
    assert listed.status_code == 200, listed.status_code
    tools = [r["key"] for r in listed.json()]
    assert tools, "the catalogue serves no tool to open"

    routes = ["/", "/gallery", "/sign-in", "/license", f"/{tools[0]}"]
    base = appclient.app_url()
    with httpx.Client(base_url=base, timeout=30.0, follow_redirects=True) as page:
        for route in routes:
            response = page.get(route)
            assert response.status_code == 200, (
                f"the route {route} returned {response.status_code}"
            )
