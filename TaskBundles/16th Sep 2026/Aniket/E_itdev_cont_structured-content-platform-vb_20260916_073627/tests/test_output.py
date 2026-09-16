"""The one pytest module for deku/structured-content-platform-vb.

Black box throughout: every assertion is made over the JSON API, over the served
markup of the public routes, over the rows the `backend` slot exposes and over
the objects the `storage` slot exposes. Nothing here reads the agent's source,
imports a provider SDK, or decides at run time whether a feature exists.
"""

from __future__ import annotations

import conftest as C


def test_login_returns_bearer_token(api):
    health = api.get(C.API_HEALTH)
    assert health.status_code in C.OK_READ, (
        "GET %s%s returned %s; the app answers at APP_PUBLIC_URL with its API "
        "under the /api prefix, bound so the port mapping reaches it"
        % (C.API_HEALTH, "", health.status_code))
    response = C.login(api, C.EDITOR_EMAIL)
    assert response.status_code in C.OK_WRITE, (
        "POST %s with the seeded editor and the pinned password returned %s: %r"
        % (C.API_LOGIN, response.status_code, response.text[:300]))
    assert C.token_of(response.json()), (
        "POST %s returned no bearer token for %r: %r"
        % (C.API_LOGIN, C.EDITOR_EMAIL, response.text[:300]))


def test_me_reports_role_and_department(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    response = api.get(C.API_ME, headers=headers)
    assert response.status_code in C.OK_READ, (
        "GET %s as the seeded editor returned %s: %r"
        % (C.API_ME, response.status_code, response.text[:300]))
    payload = C.json_body(response)
    assert C.field(payload, "role") == C.ROLE_EDITOR, (
        "GET %s reported role %r for %r, expected %r: %r"
        % (C.API_ME, C.field(payload, "role"), C.EDITOR_EMAIL, C.ROLE_EDITOR,
           response.text[:300]))
    assert C.field(payload, "department") == C.DEPARTMENT_ENGINEERING, (
        "GET %s reported department %r for %r, expected %r: %r"
        % (C.API_ME, C.field(payload, "department"), C.EDITOR_EMAIL,
           C.DEPARTMENT_ENGINEERING, response.text[:300]))
    anonymous = api.get(C.API_ME)
    assert anonymous.status_code in C.DENIED, (
        "GET %s with no bearer token returned %s rather than a denial: %r"
        % (C.API_ME, anonymous.status_code, anonymous.text[:300]))


def test_publish_stores_one_published_row_and_removes_the_draft(api, store):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.probe_id("article-probe")
    created = C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(C.DRAFT_PREFIX + document_id,
                                          C.probe_title())}])
    assert created.status_code in C.OK_WRITE, (
        "creating a draft through %s returned %s: %r"
        % (C.API_MUTATE, created.status_code, created.text[:300]))
    response = C.publish_doc(api, headers, C.DATASET_PRODUCTION, document_id)
    assert response.status_code in C.OK_WRITE, (
        "publishing %r as the seeded editor returned %s: %r"
        % (document_id, response.status_code, response.text[:300]))
    C.settle()
    published = store.document(C.DATASET_PRODUCTION, document_id)
    assert published, (
        "publishing %r left no published row in the document store"
        % document_id)
    draft = store.document(C.DATASET_PRODUCTION, C.DRAFT_PREFIX + document_id)
    assert draft is None, (
        "publishing %r left the draft row %r behind: publishing is one "
        "transaction that writes the published document and removes the draft"
        % (document_id, C.DRAFT_PREFIX + document_id))


def test_publish_confirmation_names_the_new_revision(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.probe_id("article-probe")
    C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(C.DRAFT_PREFIX + document_id,
                                          C.probe_title())}])
    response = C.publish_doc(api, headers, C.DATASET_PRODUCTION, document_id)
    assert response.status_code in C.OK_WRITE, (
        "publishing %r returned %s: %r"
        % (document_id, response.status_code, response.text[:300]))
    payload = C.doc_body(response)
    revision = C.field(payload, C.FIELD_REV, "rev", "revision")
    assert revision, (
        "publishing %r returned no %s for the revision it produced: %r"
        % (document_id, C.FIELD_REV, response.text[:300]))


def test_datasets_list_carries_visibility_and_counts(api):
    headers = C.bearer(api, C.ADMIN_EMAIL)
    response = api.get(C.API_DATASETS, headers=headers)
    assert response.status_code in C.OK_READ, (
        "GET %s as the administrator returned %s: %r"
        % (C.API_DATASETS, response.status_code, response.text[:300]))
    rows = C.as_list(response.json())
    names = [str(C.field(row, "id", "name")) for row in rows]
    for dataset in C.DATASETS:
        assert dataset in names, (
            "GET %s did not list the seeded dataset %r, it listed %r"
            % (C.API_DATASETS, dataset, names))
    for row in rows:
        assert C.field(row, "visibility") in (C.VISIBILITY_PRIVATE,
                                              C.VISIBILITY_PUBLIC), (
            "dataset %r reported visibility %r, expected %r or %r"
            % (C.field(row, "id", "name"), C.field(row, "visibility"),
               C.VISIBILITY_PRIVATE, C.VISIBILITY_PUBLIC))
        assert C.field(row, "document_count", "documentCount") is not None, (
            "dataset %r carried no document count: %r"
            % (C.field(row, "id", "name"), row))


def test_wrong_password_is_refused(api):
    response = C.login(api, C.EDITOR_EMAIL, "not-" + C.PASSWORD)
    assert response.status_code not in C.OK_WRITE, (
        "POST %s accepted a password that is not the seeded one for %r: %s %r"
        % (C.API_LOGIN, C.EDITOR_EMAIL, response.status_code,
           response.text[:300]))
    assert not C.token_of(C.json_body(response)), (
        "POST %s returned a bearer token for a wrong password: %r"
        % (C.API_LOGIN, response.text[:300]))


def test_unknown_email_is_refused_without_a_hint(api):
    unknown = C.probe_email()
    missing = C.login(api, unknown)
    wrong = C.login(api, C.EDITOR_EMAIL, "not-" + C.PASSWORD)
    assert missing.status_code not in C.OK_WRITE, (
        "POST %s accepted an address that is not seeded (%r): %s %r"
        % (C.API_LOGIN, unknown, missing.status_code, missing.text[:300]))
    assert missing.status_code == wrong.status_code, (
        "POST %s answered an unknown address with %s and a wrong password with "
        "%s: the two must be answered the same way so the response does not "
        "say which addresses exist"
        % (C.API_LOGIN, missing.status_code, wrong.status_code))
    body = C.body_text(missing).lower()
    for hint in ("not found", "no such", "unknown user", "does not exist"):
        assert hint not in body, (
            "POST %s told the caller %r about an address that is not seeded: %r"
            % (C.API_LOGIN, hint, C.body_text(missing)[:300]))


def test_document_carries_reserved_service_fields(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    response = C.read_doc(api, headers, C.DATASET_PRODUCTION, C.DOC_MIGRATING)
    assert response.status_code in C.OK_READ, (
        "reading the seeded document %r returned %s: %r"
        % (C.DOC_MIGRATING, response.status_code, response.text[:300]))
    document = C.doc_body(response)
    for name in C.RESERVED_FIELDS:
        assert name in document, (
            "the seeded document %r came back without the reserved field %r: "
            "the keys it carried were %r"
            % (C.DOC_MIGRATING, name, sorted(document)))
    assert document[C.FIELD_TYPE] == C.TYPE_ARTICLE, (
        "the seeded document %r reported %s %r rather than %r"
        % (C.DOC_MIGRATING, C.FIELD_TYPE, document[C.FIELD_TYPE],
           C.TYPE_ARTICLE))


def test_client_supplied_revision_is_refused(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document = C.article_doc(C.DRAFT_PREFIX + C.probe_id("article-probe"),
                             C.probe_title())
    document[C.FIELD_REV] = "rev-supplied-by-the-client"
    response = C.mutate(api, headers, C.DATASET_PRODUCTION,
                        [{C.MUTATION_CREATE: document}])
    assert response.status_code in C.REFUSED, (
        "creating a document that supplies %s returned %s rather than a "
        "refusal: the service assigns %r, %r and %r and refuses them from a "
        "client: %r"
        % (C.FIELD_REV, response.status_code, C.FIELD_REV, C.FIELD_CREATED,
           C.FIELD_UPDATED, response.text[:300]))


def test_created_array_objects_all_carry_keys(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.DRAFT_PREFIX + C.probe_id("article-probe")
    response = C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(document_id, C.probe_title(),
                                          items=5)}])
    assert response.status_code in C.OK_WRITE, (
        "creating a document with a five-item array returned %s: %r"
        % (response.status_code, response.text[:300]))
    read = C.read_doc(api, headers, C.DATASET_PRODUCTION, document_id,
                      C.PERSPECTIVE_RAW)
    keys = C.keys_of(C.doc_body(read).get("tags"))
    assert len(keys) == 5, (
        "the five items written into the array came back as %d: %r"
        % (len(keys), C.doc_body(read).get("tags")))
    assert all(keys), (
        "an array item came back with no _key: %r. Every object inside an array "
        "carries a key assigned at creation, through every write path" % (keys,))
    assert len(set(keys)) == 5, (
        "the five array items share keys rather than carrying five distinct "
        "ones: %r" % (keys,))


def test_repeated_saves_leave_array_keys_unchanged(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.DRAFT_PREFIX + C.probe_id("article-probe")
    C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(document_id, C.probe_title(),
                                          items=3)}])
    first = C.keys_of(C.doc_body(C.read_doc(api, headers, C.DATASET_PRODUCTION,
                                            document_id,
                                            C.PERSPECTIVE_RAW)).get("tags"))
    for round_number in range(10):
        saved = C.mutate(api, headers, C.DATASET_PRODUCTION, [
            {C.MUTATION_PATCH: {"id": document_id,
                                "set": {"title": C.probe_title("Save %d"
                                                               % round_number)}}}])
        assert saved.status_code in C.OK_WRITE, (
            "save %d of %r returned %s: %r"
            % (round_number, document_id, saved.status_code, saved.text[:300]))
    after = C.keys_of(C.doc_body(C.read_doc(api, headers, C.DATASET_PRODUCTION,
                                            document_id,
                                            C.PERSPECTIVE_RAW)).get("tags"))
    assert after == first, (
        "ten saves of %r changed the array keys from %r to %r: a key is "
        "assigned once and never reassigned" % (document_id, first, after))


def test_array_patch_by_key_survives_a_concurrent_head_insert(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.DRAFT_PREFIX + C.probe_id("article-probe")
    C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(document_id, C.probe_title(),
                                          items=3)}])
    keys = C.keys_of(C.doc_body(C.read_doc(api, headers, C.DATASET_PRODUCTION,
                                           document_id,
                                           C.PERSPECTIVE_RAW)).get("tags"))
    assert len(keys) == 3 and all(keys), (
        "the probe document %r did not come back with three keyed array items: "
        "%r" % (document_id, keys))
    target = keys[2]
    marker = "renamed-%s" % C.probe_token()
    inserted = {"_type": "tag", "label": "inserted-%s" % C.probe_token()}

    def patch_by_key():
        return C.mutate(api, headers, C.DATASET_PRODUCTION, [
            {C.MUTATION_PATCH: {
                "id": document_id,
                "set": {'tags[_key == "%s"].label' % target: marker}}}])

    def insert_at_head():
        return C.mutate(api, headers, C.DATASET_PRODUCTION, [
            {C.MUTATION_PATCH: {
                "id": document_id,
                "insert": {"before": "tags[0]", "items": [inserted]}}}])

    results = C.in_parallel(lambda: (patch_by_key(), insert_at_head()), 1)[0]
    for response in results:
        assert response.status_code in C.OK_WRITE, (
            "a patch against %r returned %s: %r"
            % (document_id, response.status_code, response.text[:300]))
    C.settle()
    tags = C.doc_body(C.read_doc(api, headers, C.DATASET_PRODUCTION,
                                 document_id, C.PERSPECTIVE_RAW)).get("tags")
    landed = [t for t in (tags or []) if isinstance(t, dict)
              and t.get("_key") == target]
    assert landed, (
        "the item keyed %r is gone from %r after a concurrent head insert: %r"
        % (target, document_id, tags))
    assert landed[0].get("label") == marker, (
        "the patch addressed to the item keyed %r landed on %r instead: a "
        "patch addressed by key must land on the item it named, whatever was "
        "inserted above it. The array came back as %r"
        % (target, landed[0].get("label"), tags))


def test_concurrent_increments_are_all_stored(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.DRAFT_PREFIX + C.probe_id("article-probe")
    document = C.article_doc(document_id, C.probe_title())
    document["views"] = 0
    C.mutate(api, headers, C.DATASET_PRODUCTION,
             [{C.MUTATION_CREATE: document}])

    def bump():
        return C.mutate(api, headers, C.DATASET_PRODUCTION, [
            {C.MUTATION_PATCH: {"id": document_id, "inc": {"views": 1}}}])

    responses = C.in_parallel(bump, C.CONCURRENT_INCREMENTS)
    accepted = [r for r in responses if r.status_code in C.OK_WRITE]
    assert len(accepted) == C.CONCURRENT_INCREMENTS, (
        "%d of %d concurrent increments were accepted; the rest returned %r"
        % (len(accepted), C.CONCURRENT_INCREMENTS,
           sorted({r.status_code for r in responses})))
    C.settle()
    views = C.doc_body(C.read_doc(api, headers, C.DATASET_PRODUCTION,
                                  document_id,
                                  C.PERSPECTIVE_RAW)).get("views")
    assert views == C.CONCURRENT_INCREMENTS, (
        "%d concurrent increments of one counter left it at %r rather than at "
        "%d: an increment is server-side arithmetic, never a read followed by "
        "a write" % (C.CONCURRENT_INCREMENTS, views, C.CONCURRENT_INCREMENTS))


def test_replayed_transaction_id_applies_once(api, store):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.DRAFT_PREFIX + C.probe_id("article-probe")
    document = C.article_doc(document_id, C.probe_title())
    document["views"] = 0
    C.mutate(api, headers, C.DATASET_PRODUCTION,
             [{C.MUTATION_CREATE: document}])
    transaction_id = C.probe_transaction()
    mutations = [{C.MUTATION_PATCH: {"id": document_id, "inc": {"views": 1}}}]
    first = C.mutate(api, headers, C.DATASET_PRODUCTION, mutations,
                     transaction_id)
    assert first.status_code in C.OK_WRITE, (
        "the first send of transaction %r returned %s: %r"
        % (transaction_id, first.status_code, first.text[:300]))
    for _ in range(4):
        replay = C.mutate(api, headers, C.DATASET_PRODUCTION, mutations,
                          transaction_id)
        assert replay.status_code in C.OK_WRITE, (
            "replaying transaction %r returned %s rather than the original "
            "result: %r" % (transaction_id, replay.status_code,
                            replay.text[:300]))
    C.settle()
    views = C.doc_body(C.read_doc(api, headers, C.DATASET_PRODUCTION,
                                  document_id,
                                  C.PERSPECTIVE_RAW)).get("views")
    assert views == 1, (
        "one transaction sent five times left the counter at %r rather than at "
        "1: a replayed transaction id returns the original result and applies "
        "nothing" % (views,))
    revisions = store.revisions_of(C.DATASET_PRODUCTION, document_id)
    assert len([r for r in revisions
                if str(C.field(r, "transaction_id", "transactionId") or "")
                == transaction_id]) <= 1, (
        "transaction %r produced more than one revision of %r"
        % (transaction_id, document_id))


def test_revision_mismatch_is_refused(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.DRAFT_PREFIX + C.probe_id("article-probe")
    C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(document_id, C.probe_title())}])
    first = C.doc_body(C.read_doc(api, headers, C.DATASET_PRODUCTION,
                                  document_id, C.PERSPECTIVE_RAW))
    stale = first.get(C.FIELD_REV)
    assert stale, (
        "the probe document %r came back with no %s to base a patch on"
        % (document_id, C.FIELD_REV))
    moved = C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_PATCH: {"id": document_id,
                            "set": {"title": C.probe_title("Moved on")}}}])
    assert moved.status_code in C.OK_WRITE, (
        "moving %r on returned %s: %r"
        % (document_id, moved.status_code, moved.text[:300]))
    response = C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_PATCH: {"id": document_id, "ifRevisionID": stale,
                            "set": {"title": C.probe_title("Stale write")}}}])
    assert response.status_code in C.REFUSED, (
        "a patch based on the superseded revision %r returned %s rather than a "
        "refusal: %r" % (stale, response.status_code, response.text[:300]))
    assert C.error_code(response) == C.CODE_REVISION_MISMATCH, (
        "a patch based on a superseded revision was refused with the code %r "
        "rather than %r: %r"
        % (C.error_code(response), C.CODE_REVISION_MISMATCH,
           response.text[:300]))


def test_partial_patch_applies_nothing(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.DRAFT_PREFIX + C.probe_id("article-probe")
    original = C.probe_title("Original")
    C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(document_id, original, items=2)}])
    response = C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_PATCH: {
            "id": document_id,
            "set": {"title": C.probe_title("Changed")},
            "inc": {"title": 1},
        }}])
    assert response.status_code in C.REFUSED, (
        "a patch whose arithmetic operation targets a text field returned %s "
        "rather than a refusal: %r"
        % (response.status_code, response.text[:300]))
    C.settle()
    title = C.doc_body(C.read_doc(api, headers, C.DATASET_PRODUCTION,
                                  document_id,
                                  C.PERSPECTIVE_RAW)).get("title")
    assert title == original, (
        "a refused patch left the title at %r rather than at %r: the "
        "operations of one patch apply together or not at all"
        % (title, original))


def test_split_span_keeps_the_first_key(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    response = C.read_doc(api, headers, C.DATASET_PRODUCTION, C.DOC_AURORA,
                          C.PERSPECTIVE_DRAFTS)
    assert response.status_code in C.OK_READ, (
        "reading %r under the %r perspective returned %s: %r"
        % (C.DOC_AURORA, C.PERSPECTIVE_DRAFTS, response.status_code,
           response.text[:300]))
    body = C.doc_body(response).get("body")
    block = C.find_block_with(body, C.SPLIT_WORD)
    assert block is not None, (
        "the seeded article %r carries no block containing the word %r: its "
        "body came back as %r" % (C.DOC_AURORA, C.SPLIT_WORD, body))
    spans = C.spans_of(block)
    assert len(spans) >= 3, (
        "the seeded paragraph whose middle word is part-emboldened came back "
        "as %d span(s): emboldening the middle of a span splits it into three"
        % len(spans))
    emboldened = [s for s in spans if C.MARK_STRONG in (s.get("marks") or [])]
    assert emboldened, (
        "no span of the seeded paragraph carries the %r decorator: %r"
        % (C.MARK_STRONG, spans))
    assert all(s.get("_key") for s in spans), (
        "a span of the seeded paragraph came back with no _key: %r" % (spans,))
    assert spans[0].get("_key") != emboldened[0].get("_key"), (
        "the emboldened fragment reuses the first span's key: the first "
        "fragment of a split keeps the original key and the new fragments get "
        "new ones. The spans came back as %r" % (spans,))


def test_adjacent_spans_with_equal_mark_sets_merge(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.DRAFT_PREFIX + C.probe_id("article-probe")
    block = {"_type": "block", "style": "normal", "children": [
        {"_type": "span", "text": "first ", "marks": [C.MARK_STRONG, C.MARK_EM]},
        {"_type": "span", "text": "second", "marks": [C.MARK_EM, C.MARK_STRONG]},
    ]}
    created = C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(document_id, C.probe_title(),
                                          body=[block])}])
    assert created.status_code in C.OK_WRITE, (
        "creating a document with two adjacent equally marked spans returned "
        "%s: %r" % (created.status_code, created.text[:300]))
    C.settle()
    stored = C.doc_body(C.read_doc(api, headers, C.DATASET_PRODUCTION,
                                   document_id, C.PERSPECTIVE_RAW)).get("body")
    spans = C.spans_of((stored or [{}])[0])
    assert len(spans) == 1, (
        "two adjacent spans carrying the same two decorators in a different "
        "order came back as %d spans rather than one: mark sets are compared "
        "as sets. The block came back as %r" % (len(spans), stored))
    assert spans[0].get("text") == "first second", (
        "the merged span reads %r rather than %r"
        % (spans[0].get("text"), "first second"))


def test_orphaned_annotation_is_removed(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.DRAFT_PREFIX + C.probe_id("article-probe")
    mark_key = "link-%s" % C.probe_token()
    block = {"_type": "block", "style": "normal",
             "markDefs": [{"_key": mark_key, "_type": "link",
                           "href": "/docs"}],
             "children": [{"_type": "span", "text": "read the documentation",
                           "marks": [mark_key]}]}
    C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(document_id, C.probe_title(),
                                          body=[block])}])
    stripped = dict(block)
    stripped["children"] = [{"_type": "span", "text": "read the documentation",
                             "marks": []}]
    response = C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_PATCH: {"id": document_id, "set": {"body": [stripped]}}}])
    assert response.status_code in C.OK_WRITE, (
        "removing the only reference to an annotation returned %s: %r"
        % (response.status_code, response.text[:300]))
    C.settle()
    stored = C.doc_body(C.read_doc(api, headers, C.DATASET_PRODUCTION,
                                   document_id, C.PERSPECTIVE_RAW)).get("body")
    definitions = (stored or [{}])[0].get("markDefs") or []
    assert not definitions, (
        "the annotation %r survived the removal of the only span referencing "
        "it: an orphaned annotation is removed on the write that orphaned it. "
        "markDefs came back as %r" % (mark_key, definitions))


def test_consecutive_bullets_render_as_one_list(site):
    response = site.get("%s/%s" % (C.ROUTE_BLOG, C.DOC_AURORA))
    assert response.status_code in C.OK_READ, (
        "reading the published article at %s/%s returned %s"
        % (C.ROUTE_BLOG, C.DOC_AURORA, response.status_code))
    markup = C.body_text(response)
    lists = len(C.LIST_OPEN_RE.findall(markup))
    items = len(C.LIST_ITEM_RE.findall(markup))
    assert items >= 3, (
        "the seeded article renders %d list item(s); its body carries a run of "
        "three consecutive bulleted blocks" % items)
    assert lists == 1, (
        "the run of three consecutive bulleted blocks rendered as %d lists "
        "rather than as one list of three items: a serializer groups a run "
        "itself" % lists)


def test_markup_characters_survive_byte_identical(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.DRAFT_PREFIX + C.probe_id("article-probe")
    literal = "- not a bullet <b>not bold</b> *not italic* %s" % C.probe_token()
    C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(document_id, C.probe_title(),
                                          body=[C.text_block(literal)])}])
    C.settle()
    stored = C.doc_body(C.read_doc(api, headers, C.DATASET_PRODUCTION,
                                   document_id, C.PERSPECTIVE_RAW)).get("body")
    spans = C.spans_of((stored or [{}])[0])
    assert spans, (
        "the probe block came back with no spans: %r" % (stored,))
    assert spans[0].get("text") == literal, (
        "text stored with markup characters came back as %r rather than %r: "
        "span text is literal and is never re-interpreted"
        % (spans[0].get("text"), literal))


def test_drafts_perspective_returns_published_ids(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    response = C.read_doc(api, headers, C.DATASET_PRODUCTION, C.DOC_AURORA,
                          C.PERSPECTIVE_DRAFTS)
    assert response.status_code in C.OK_READ, (
        "reading %r under the %r perspective returned %s: %r"
        % (C.DOC_AURORA, C.PERSPECTIVE_DRAFTS, response.status_code,
           response.text[:300]))
    document = C.doc_body(response)
    assert document.get(C.FIELD_ID) == C.DOC_AURORA, (
        "the %r perspective returned the identifier %r rather than the "
        "published identifier %r: a preview must render identically to "
        "production" % (C.PERSPECTIVE_DRAFTS, document.get(C.FIELD_ID),
                        C.DOC_AURORA))
    raw = C.read_doc(api, headers, C.DATASET_PRODUCTION,
                     C.DRAFT_PREFIX + C.DOC_AURORA, C.PERSPECTIVE_RAW)
    assert raw.status_code in C.OK_READ, (
        "the %r perspective did not expose the stored draft %r: %s %r"
        % (C.PERSPECTIVE_RAW, C.DRAFT_PREFIX + C.DOC_AURORA, raw.status_code,
           raw.text[:300]))


def test_history_is_append_only_across_publish(api, store):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.probe_id("article-probe")
    C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(C.DRAFT_PREFIX + document_id,
                                          C.probe_title())}])
    C.publish_doc(api, headers, C.DATASET_PRODUCTION, document_id)
    C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE_OR_REPLACE: C.article_doc(
            C.DRAFT_PREFIX + document_id, C.probe_title("Second draft"))}])
    C.publish_doc(api, headers, C.DATASET_PRODUCTION, document_id)
    C.settle()
    response = C.read_history(api, headers, C.DATASET_PRODUCTION, document_id)
    assert response.status_code in C.OK_READ, (
        "reading the history of %r returned %s: %r"
        % (document_id, response.status_code, response.text[:300]))
    revisions = C.as_list(response.json())
    assert len(revisions) >= 2, (
        "two publishes of %r left %d revision(s) in its history: history is "
        "append-only and a publish is a write like any other"
        % (document_id, len(revisions)))
    stored = store.revisions_of(C.DATASET_PRODUCTION, document_id)
    assert len(stored) >= 2, (
        "the revision store holds %d row(s) for %r after two publishes"
        % (len(stored), document_id))


def test_four_publication_states_are_distinguishable(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    expected = {
        C.DOC_AURORA: C.STATE_PUBLISHED_WITH_EDITS,
        C.DOC_KEYS: C.STATE_NOT_PUBLISHED,
        C.DOC_MIGRATING: C.STATE_PUBLISHED,
        C.DOC_RETIRED: C.STATE_DRAFT,
    }
    seen = {}
    for document_id, want in expected.items():
        response = C.read_doc(api, headers, C.DATASET_PRODUCTION, document_id,
                              C.PERSPECTIVE_DRAFTS)
        assert response.status_code in C.OK_READ, (
            "reading the seeded document %r returned %s: %r"
            % (document_id, response.status_code, response.text[:300]))
        state = C.field(C.doc_body(response), "state", "publication_state",
                        "publicationState")
        assert state is not None, (
            "the seeded document %r reported no publication state; the "
            "interface distinguishes %r" % (document_id, C.PUBLICATION_STATES))
        seen[document_id] = str(state)
        assert str(state) == want, (
            "the seeded document %r reported the state %r rather than %r"
            % (document_id, state, want))
    assert len(set(seen.values())) == 4, (
        "the four seeded documents reported %d distinct states rather than "
        "four: %r" % (len(set(seen.values())), seen))


def test_unpublish_recreates_the_draft(api, store):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.probe_id("article-probe")
    C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(C.DRAFT_PREFIX + document_id,
                                          C.probe_title())}])
    C.publish_doc(api, headers, C.DATASET_PRODUCTION, document_id)
    response = C.unpublish_doc(api, headers, C.DATASET_PRODUCTION, document_id)
    assert response.status_code in C.OK_WRITE, (
        "unpublishing %r returned %s: %r"
        % (document_id, response.status_code, response.text[:300]))
    C.settle()
    assert store.document(C.DATASET_PRODUCTION, document_id) is None, (
        "unpublishing %r left the published row in place" % document_id)
    assert store.document(C.DATASET_PRODUCTION,
                          C.DRAFT_PREFIX + document_id) is not None, (
        "unpublishing %r created no draft row: unpublishing is the mirror of "
        "publishing and both halves land together" % document_id)


def test_listen_stream_opens_with_welcome_and_carries_revisions(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    path = C.dataset_path(C.API_LISTEN, C.DATASET_PRODUCTION)
    with api.stream("GET", path, params={"query": '*[_type == "article"]'},
                    headers=headers) as response:
        assert response.status_code in C.OK_READ, (
            "opening the event stream returned %s" % response.status_code)
        collected = []
        for line in response.iter_lines():
            collected.append(line)
            if len(collected) >= 12:
                break
    joined = "\n".join(collected)
    assert "welcome" in joined, (
        "the event stream did not open with a welcome event; it began %r"
        % joined[:300])
    for name in ("previousRev", "resultRev", "transactionId", "transition"):
        assert name in joined or not joined.count("mutation"), (
            "a change event on the stream carried no %r: a client cannot tell "
            "a gap from a delivery without it. The stream read %r"
            % (name, joined[:400]))


def test_query_returns_result_with_cost(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    response = C.run_query(api, headers, C.DATASET_PRODUCTION,
                           '*[_type == $type]{_id, title}',
                           {"type": C.TYPE_ARTICLE})
    assert response.status_code in C.OK_READ, (
        "running a projection over articles returned %s: %r"
        % (response.status_code, response.text[:300]))
    result = C.query_result(response)
    assert result, (
        "a projection over the seeded articles came back empty: %r"
        % response.text[:300])
    cost = C.query_cost(response)
    assert cost, (
        "the query answer carried no cost record: every response carries its "
        "own cost. The body was %r" % response.text[:300])
    for name in ("documents_examined", "documentsExamined", "examined"):
        if name in cost:
            break
    else:
        raise AssertionError(
            "the cost record named no count of documents examined: %r" % (cost,))


def test_query_parameter_containing_syntax_is_a_literal(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    injected = '" || _type == "author'
    response = C.run_query(api, headers, C.DATASET_PRODUCTION,
                           '*[_type == "article" && title == $needle]{_id}',
                           {"needle": injected})
    assert response.status_code in C.OK_READ, (
        "a query whose parameter carries query syntax returned %s rather than "
        "an ordinary answer: %r" % (response.status_code, response.text[:300]))
    result = C.query_result(response)
    assert result == [], (
        "a parameter carrying query syntax changed what the query selected: it "
        "returned %r. A parameter value is a literal string, never spliced into "
        "the query text" % (result,))
    ids = [str(C.field(row, C.FIELD_ID)) for row in result]
    assert C.DOC_AUTHOR_MARIT not in ids, (
        "a parameter carrying query syntax reached an author document: %r"
        % (ids,))


def test_query_over_bound_is_refused_naming_the_predicate(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    deep = "author->" * (C.DEREFERENCE_DEPTH_BOUND + 3)
    response = C.run_query(api, headers, C.DATASET_PRODUCTION,
                           '*[_type == "article"]{"deep": %s name}' % deep)
    assert response.status_code in C.REFUSED, (
        "a query dereferencing %d levels deep returned %s rather than a "
        "refusal: the dereference depth bound is %d"
        % (C.DEREFERENCE_DEPTH_BOUND + 3, response.status_code,
           C.DEREFERENCE_DEPTH_BOUND))
    assert C.error_code(response) == C.CODE_QUERY_BOUND, (
        "the refusal carried the code %r rather than %r: %r"
        % (C.error_code(response), C.CODE_QUERY_BOUND, response.text[:300]))
    assert C.mentions(response, "deref"), (
        "the refusal named no specific predicate: a bound refusal names what "
        "made the query expensive. The body was %r" % response.text[:400])


def test_migration_dry_run_writes_nothing(api, store):
    headers = C.bearer(api, C.ADMIN_EMAIL)
    before = store.count(C.TABLE_REVISION, dataset=C.DATASET_PRODUCTION)
    response = C.run_migration(api, headers, "rename-standfirst",
                               C.DATASET_PRODUCTION)
    assert response.status_code in C.OK_WRITE, (
        "a migration invoked in its default mode returned %s: %r"
        % (response.status_code, response.text[:300]))
    payload = C.json_body(response)
    assert str(C.field(payload, "mode")) == C.MODE_DRY_RUN, (
        "a migration invoked without a mode ran as %r rather than %r: the dry "
        "run is the default" % (C.field(payload, "mode"), C.MODE_DRY_RUN))
    assert C.field(payload, "affected") is not None, (
        "the dry run reported no affected count: %r" % response.text[:300])
    assert C.field(payload, "sample") is not None, (
        "the dry run reported no sample of before-and-after pairs: %r"
        % response.text[:300])
    C.settle()
    after = store.count(C.TABLE_REVISION, dataset=C.DATASET_PRODUCTION)
    assert after == before, (
        "a dry run added %d revision(s) to the store: it reports what it would "
        "change and writes nothing" % (after - before))


def test_migration_rerun_changes_nothing(api):
    headers = C.bearer(api, C.ADMIN_EMAIL)
    name = "rename-standfirst"
    first = C.run_migration(api, headers, name, C.DATASET_PRODUCTION,
                            C.MODE_APPLY,
                            confirm_name=C.DATASET_PRODUCTION)
    assert first.status_code in C.OK_WRITE, (
        "applying the migration %r returned %s: %r"
        % (name, first.status_code, first.text[:300]))
    C.settle()
    second = C.run_migration(api, headers, name, C.DATASET_PRODUCTION,
                             C.MODE_APPLY,
                             confirm_name=C.DATASET_PRODUCTION)
    assert second.status_code in C.OK_WRITE, (
        "running the migration %r a second time returned %s: %r"
        % (name, second.status_code, second.text[:300]))
    affected = C.field(C.json_body(second), "affected")
    assert affected in (0, "0"), (
        "the second run of %r reported %r documents changed rather than none: "
        "a migration is idempotent because an interrupted run is re-run"
        % (name, affected))


def test_migration_preserves_rich_text_keys(api):
    headers = C.bearer(api, C.ADMIN_EMAIL)
    editor = C.bearer(api, C.EDITOR_EMAIL)
    before = C.block_and_span_keys(
        C.doc_body(C.read_doc(api, editor, C.DATASET_PRODUCTION, C.DOC_AURORA,
                              C.PERSPECTIVE_DRAFTS)).get("body"))
    assert before and all(before), (
        "the seeded article %r came back with an unkeyed block or span: %r"
        % (C.DOC_AURORA, before))
    response = C.run_migration(api, headers, "rename-standfirst",
                               C.DATASET_PRODUCTION, C.MODE_APPLY,
                               confirm_name=C.DATASET_PRODUCTION)
    assert response.status_code in C.OK_WRITE, (
        "applying the migration returned %s: %r"
        % (response.status_code, response.text[:300]))
    C.settle()
    after = C.block_and_span_keys(
        C.doc_body(C.read_doc(api, editor, C.DATASET_PRODUCTION, C.DOC_AURORA,
                              C.PERSPECTIVE_DRAFTS)).get("body"))
    assert after == before, (
        "a migration changed the block and span keys of %r from %r to %r: a "
        "migration touching rich text keeps every key it does not explicitly "
        "remove, or it destroys the document's identity"
        % (C.DOC_AURORA, before, after))


def test_migration_against_production_requires_retyped_name(api):
    headers = C.bearer(api, C.ADMIN_EMAIL)
    response = C.run_migration(api, headers, "rename-standfirst",
                               C.DATASET_PRODUCTION, C.MODE_APPLY)
    assert response.status_code in C.REFUSED, (
        "applying a migration against %r without the dataset name typed again "
        "returned %s rather than a refusal: %r"
        % (C.DATASET_PRODUCTION, response.status_code, response.text[:300]))
    assert C.error_code(response) == C.CODE_PRODUCTION_CONFIRMATION, (
        "the refusal carried the code %r rather than %r: %r"
        % (C.error_code(response), C.CODE_PRODUCTION_CONFIRMATION,
           response.text[:300]))
    nameless = api.post(C.API_MIGRATIONS,
                        json={"name": "rename-standfirst",
                              "mode": C.MODE_DRY_RUN},
                        headers=headers)
    assert nameless.status_code in C.REFUSED, (
        "a migration invoked with no dataset named returned %s rather than a "
        "refusal: the runner has no default dataset"
        % nameless.status_code)


def test_dataset_visibility_change_requires_typed_name(api, store):
    headers = C.bearer(api, C.ADMIN_EMAIL)
    path = "%s/%s/visibility" % (C.API_PROJECT_DATASETS, C.DATASET_STAGING)
    unconfirmed = api.post(path, json={"visibility": C.VISIBILITY_PUBLIC},
                           headers=headers)
    assert unconfirmed.status_code in C.REFUSED, (
        "switching %r to %r without the dataset name typed again returned %s "
        "rather than a refusal: %r"
        % (C.DATASET_STAGING, C.VISIBILITY_PUBLIC, unconfirmed.status_code,
           unconfirmed.text[:300]))
    row = store.one(C.TABLE_DATASET, id=C.DATASET_STAGING)
    assert row is None or str(C.field(row, "visibility")) != C.VISIBILITY_PUBLIC, (
        "the unconfirmed request made %r public anyway: %r"
        % (C.DATASET_STAGING, row))
    confirmed = api.post(path, json={"visibility": C.VISIBILITY_PUBLIC,
                                     "confirm_name": C.DATASET_STAGING},
                         headers=headers)
    assert confirmed.status_code in C.OK_WRITE, (
        "switching %r to %r with the name typed again returned %s: %r"
        % (C.DATASET_STAGING, C.VISIBILITY_PUBLIC, confirmed.status_code,
           confirmed.text[:300]))
    assert C.field(C.json_body(confirmed), "count", "documents",
                   "document_count") is not None, (
        "the confirmation stated no count of documents becoming world-readable:"
        " %r" % confirmed.text[:300])


def test_release_publishes_atomically(api, store):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    members = [C.probe_id("article-probe"), C.probe_id("article-probe")]
    for member in members:
        C.mutate(api, headers, C.DATASET_PRODUCTION, [
            {C.MUTATION_CREATE: C.article_doc(C.DRAFT_PREFIX + member,
                                              C.probe_title())}])
    created = api.post(C.dataset_path(C.API_RELEASES, C.DATASET_PRODUCTION),
                       json={"title": C.probe_title("Release"),
                             "document_ids": members}, headers=headers)
    assert created.status_code in C.OK_WRITE, (
        "creating a release of two documents returned %s: %r"
        % (created.status_code, created.text[:300]))
    release_id = str(C.field(C.json_body(created), "id", "release_id") or "")
    assert release_id, (
        "the created release carried no identifier: %r" % created.text[:300])
    published = api.post(
        C.dataset_path(C.API_RELEASES, C.DATASET_PRODUCTION, release_id,
                       "publish"), json={}, headers=headers)
    assert published.status_code in C.OK_WRITE, (
        "publishing release %r returned %s: %r"
        % (release_id, published.status_code, published.text[:300]))
    C.settle()
    for member in members:
        assert store.document(C.DATASET_PRODUCTION, member), (
            "release %r published without %r reaching the published state: a "
            "release publishes its whole set in one transaction or none of it"
            % (release_id, member))


def test_oversized_release_is_refused_at_creation(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    members = ["%s-%d" % (C.probe_id("article-probe"), n) for n in range(5000)]
    response = api.post(C.dataset_path(C.API_RELEASES, C.DATASET_PRODUCTION),
                        json={"title": C.probe_title("Oversized"),
                              "document_ids": members}, headers=headers)
    assert response.status_code in C.REFUSED, (
        "creating a release of %d documents returned %s rather than a refusal "
        "at creation time: %r"
        % (len(members), response.status_code, response.text[:300]))
    assert C.error_code(response) == C.CODE_RELEASE_TOO_LARGE, (
        "the refusal carried the code %r rather than %r: %r"
        % (C.error_code(response), C.CODE_RELEASE_TOO_LARGE,
           response.text[:300]))


def test_search_finds_a_word_split_across_spans(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    response = C.search(api, headers, C.DATASET_PRODUCTION, C.SPLIT_WORD)
    assert response.status_code in C.OK_READ, (
        "searching %r returned %s: %r"
        % (C.SPLIT_WORD, response.status_code, response.text[:300]))
    matches = C.search_matches(response)
    ids = [str(C.field(m, "_id", "documentId", "id")) for m in matches]
    assert C.DOC_AURORA in ids, (
        "searching for %r did not find %r, whose second paragraph carries that "
        "word with its middle emboldened. A span boundary inside a word must "
        "not break the indexed token. The matches were %r"
        % (C.SPLIT_WORD, C.DOC_AURORA, ids))


def test_unmatched_path_returns_the_not_found_page(raw_site):
    response = raw_site.get(C.ROUTE_UNMATCHED)
    assert response.status_code in C.NOT_FOUND, (
        "an address matching no route returned %s rather than 404: an address "
        "that does not exist must not answer as though it did"
        % response.status_code)
    markup = C.body_text(response)
    assert C.COPY_NOT_FOUND_TITLE in C.page_title(markup), (
        "the not-found page carried the document title %r rather than %r"
        % (C.page_title(markup), C.COPY_NOT_FOUND_TITLE))
    assert C.COPY_RAIL_FIRST not in markup, (
        "an address matching no route rendered the home page: no path renders "
        "the home page")


def test_no_internal_link_on_a_public_route_is_broken(site):
    broken = []
    for route in C.PUBLIC_ROUTES:
        page = site.get(route)
        assert page.status_code in C.OK_READ, (
            "the public route %r returned %s" % (route, page.status_code))
        for target in C.internal_links(C.body_text(page))[:40]:
            linked = site.get(target)
            if linked.status_code not in C.OK_READ:
                broken.append((route, target, linked.status_code))
    assert not broken, (
        "internal links on public routes do not resolve: %r. Every internal "
        "link on every public route resolves" % broken[:8])


def test_sitemap_lists_every_public_route(site):
    response = site.get(C.ROUTE_SITEMAP)
    assert response.status_code in C.OK_READ, (
        "GET %s returned %s" % (C.ROUTE_SITEMAP, response.status_code))
    listed = C.SITEMAP_LOC_RE.findall(C.body_text(response))
    assert listed, (
        "%s listed no addresses: %r"
        % (C.ROUTE_SITEMAP, C.body_text(response)[:300]))
    for route in C.PUBLIC_ROUTES:
        assert any(entry.rstrip("/").endswith(route.rstrip("/")) or
                   (route == C.ROUTE_HOME and entry.rstrip("/"))
                   for entry in listed), (
            "%s does not list the public route %r; it listed %r"
            % (C.ROUTE_SITEMAP, route, listed))


def test_robots_names_the_sitemap(site):
    response = site.get(C.ROUTE_ROBOTS)
    assert response.status_code in C.OK_READ, (
        "GET %s returned %s" % (C.ROUTE_ROBOTS, response.status_code))
    found = C.ROBOTS_SITEMAP_RE.search(C.body_text(response))
    assert found, (
        "%s names no sitemap: %r"
        % (C.ROUTE_ROBOTS, C.body_text(response)[:300]))
    named = found.group(1)
    assert named.startswith("http"), (
        "%s named the sitemap as %r rather than as an absolute address"
        % (C.ROUTE_ROBOTS, named))
    assert named.rstrip("/").endswith(C.ROUTE_SITEMAP), (
        "%s pointed at %r rather than at %r"
        % (C.ROUTE_ROBOTS, named, C.ROUTE_SITEMAP))


def test_cookie_decision_survives_a_reload(site):
    first = site.get(C.ROUTE_HOME)
    assert first.status_code in C.OK_READ, (
        "GET %s returned %s" % (C.ROUTE_HOME, first.status_code))
    markup = C.body_text(first).lower()
    assert "cookie" in markup, (
        "the home route offered no cookie decision: a first-time visitor is "
        "asked once about non-essential cookies")
    recorded = site.post(C.ROUTE_COOKIES,
                         data={"analytics": "no", "preferences": "yes"})
    assert recorded.status_code in (200, 201, 204, 302, 303), (
        "recording a cookie decision at %s returned %s: %r"
        % (C.ROUTE_COOKIES, recorded.status_code, recorded.text[:200]))
    again = site.get(C.ROUTE_HOME)
    assert "cookie" not in C.body_text(again).lower() or \
        C.ROUTE_COOKIES in C.body_text(again), (
        "the cookie choice was asked again after a decision was recorded: the "
        "answer survives a reload and is reachable afterwards from the footer")


def test_repeated_lead_submissions_are_refused(api, store):
    company = "Probe Co %s" % C.probe_token()
    address = C.probe_email()
    first = C.submit_lead(api, address, company)
    assert first.status_code in C.OK_WRITE, (
        "the first demo request returned %s: %r"
        % (first.status_code, first.text[:300]))
    repeats = [C.submit_lead(api, C.probe_email(), company) for _ in range(6)]
    refused = [r for r in repeats if r.status_code in C.REFUSED]
    assert refused, (
        "six demo requests sent one after another from one origin were all "
        "accepted: a form submitted repeatedly in quick succession is refused. "
        "The statuses were %r" % [r.status_code for r in repeats])
    C.settle()
    stored = store.count(C.TABLE_LEAD, company=company)
    assert stored < 1 + len(repeats), (
        "%d leads were written for the company %r although %d submissions were "
        "refused" % (stored, company, len(refused)))


def test_contributor_cannot_publish(api, store):
    contributor = C.bearer(api, C.CONTRIBUTOR_EMAIL)
    editor = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.probe_id("article-probe")
    created = C.mutate(api, contributor, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(C.DRAFT_PREFIX + document_id,
                                          C.probe_title())}])
    assert created.status_code in C.OK_WRITE, (
        "a contributor could not create a draft inside their own department: "
        "%s %r" % (created.status_code, created.text[:300]))
    response = C.publish_doc(api, contributor, C.DATASET_PRODUCTION,
                             document_id)
    assert response.status_code in C.DENIED, (
        "a contributor publishing %r was answered %s rather than denied: "
        "publishing is an editor's action and the server is the enforcement "
        "point" % (document_id, response.status_code))
    C.settle()
    assert store.document(C.DATASET_PRODUCTION, document_id) is None, (
        "a denied publish of %r wrote a published row anyway" % document_id)
    allowed = C.publish_doc(api, editor, C.DATASET_PRODUCTION, document_id)
    assert allowed.status_code in C.OK_WRITE, (
        "an editor publishing the same document was answered %s: %r"
        % (allowed.status_code, allowed.text[:300]))


def test_editor_cannot_reach_project_routes(api):
    editor = C.bearer(api, C.EDITOR_EMAIL)
    admin = C.bearer(api, C.ADMIN_EMAIL)
    for path in (C.API_AUDIT, C.API_TOKENS, C.API_GRANTS, C.API_MIGRATIONS):
        refused = api.get(path, headers=editor)
        assert refused.status_code in C.DENIED_OR_MISSING, (
            "an editor reading %s was answered %s rather than denied: project "
            "administration belongs to the administrator alone"
            % (path, refused.status_code))
        allowed = api.get(path, headers=admin)
        assert allowed.status_code in C.OK_READ, (
            "the administrator reading %s was answered %s: %r"
            % (path, allowed.status_code, allowed.text[:200]))


def test_administrator_cannot_patch_a_document(api):
    admin = C.bearer(api, C.ADMIN_EMAIL)
    response = C.mutate(api, admin, C.DATASET_PRODUCTION, [
        {C.MUTATION_PATCH: {"id": C.DRAFT_PREFIX + C.DOC_AURORA,
                            "set": {"title": C.probe_title("Admin write")}}}])
    assert response.status_code in C.DENIED, (
        "the administrator patching %r was answered %s rather than denied: the "
        "person who decides who may change the content does not change it"
        % (C.DOC_AURORA, response.status_code))


def test_editor_cannot_read_another_department(api):
    editor = C.bearer(api, C.EDITOR_EMAIL)
    other = C.bearer(api, C.EDITOR2_EMAIL)
    refused = C.read_doc(api, editor, C.DATASET_PRODUCTION, C.DOC_QUARTERLY)
    assert refused.status_code in C.NOT_FOUND, (
        "the engineering editor reading %r, which belongs to %r, was answered "
        "%s rather than not found: naming the refusal is itself a disclosure"
        % (C.DOC_QUARTERLY, C.DEPARTMENT_MARKETING, refused.status_code))
    listed = C.run_query(api, editor, C.DATASET_PRODUCTION,
                         '*[_type == "article"]{_id}')
    ids = [str(C.field(row, C.FIELD_ID)) for row in C.query_result(listed)]
    assert C.DOC_QUARTERLY not in ids, (
        "a query run by the engineering editor returned %r among %r: a grant "
        "filter runs on the service, so the restricted document is absent from "
        "the raw answer rather than hidden afterwards" % (C.DOC_QUARTERLY, ids))
    allowed = C.read_doc(api, other, C.DATASET_PRODUCTION, C.DOC_QUARTERLY)
    assert allowed.status_code in C.OK_READ, (
        "the marketing editor reading their own department's %r was answered "
        "%s: %r" % (C.DOC_QUARTERLY, allowed.status_code, allowed.text[:300]))


def test_cross_department_document_is_absent_from_search(api):
    editor = C.bearer(api, C.EDITOR_EMAIL)
    other = C.bearer(api, C.EDITOR2_EMAIL)
    mine = C.search(api, editor, C.DATASET_PRODUCTION, "quarterly")
    assert mine.status_code in C.OK_READ, (
        "editor search returned %s: %r" % (mine.status_code, mine.text[:300]))
    ids = [str(C.field(m, "_id", "documentId", "id"))
           for m in C.search_matches(mine)]
    assert C.DOC_QUARTERLY not in ids, (
        "%r appeared in the engineering editor's search results: results are "
        "filtered against the caller's grants at query time. The matches were "
        "%r" % (C.DOC_QUARTERLY, ids))
    theirs = C.search(api, other, C.DATASET_PRODUCTION, "quarterly")
    their_ids = [str(C.field(m, "_id", "documentId", "id"))
                 for m in C.search_matches(theirs)]
    assert C.DOC_QUARTERLY in their_ids, (
        "the marketing editor's own document %r was missing from their search "
        "results: %r" % (C.DOC_QUARTERLY, their_ids))


def test_grant_escape_write_is_refused(api, store):
    editor = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.DRAFT_PREFIX + C.probe_id("article-probe")
    C.mutate(api, editor, C.DATASET_PRODUCTION, [
        {C.MUTATION_CREATE: C.article_doc(document_id, C.probe_title())}])
    response = C.mutate(api, editor, C.DATASET_PRODUCTION, [
        {C.MUTATION_PATCH: {"id": document_id,
                            "set": {"department": C.DEPARTMENT_MARKETING}}}])
    assert response.status_code in C.REFUSED + C.DENIED, (
        "moving a document out of the writer's own grant was answered %s "
        "rather than refused: a grant a writer can edit their way out of is no "
        "grant" % response.status_code)
    assert C.error_code(response) == C.CODE_GRANT_ESCAPE, (
        "the refusal carried the code %r rather than %r: %r"
        % (C.error_code(response), C.CODE_GRANT_ESCAPE, response.text[:300]))
    C.settle()
    row = store.document(C.DATASET_PRODUCTION, document_id)
    assert row is None or str(C.field(row, "department",
                                      "dept")) != C.DEPARTMENT_MARKETING, (
        "the refused write changed the stored department anyway: %r" % (row,))


def test_anonymous_read_defaults_to_published(api, site):
    response = C.run_query(api, {}, C.DATASET_PRODUCTION,
                           '*[_type == "article"]{_id}')
    ids = [str(C.field(row, C.FIELD_ID)) for row in C.query_result(response)]
    assert C.DOC_KEYS not in ids, (
        "a read carrying no credentials returned the never-published document "
        "%r: the default perspective for an anonymous read is %r. The answer "
        "held %r" % (C.DOC_KEYS, C.PERSPECTIVE_PUBLISHED, ids))
    for identifier in ids:
        assert not identifier.startswith(C.DRAFT_PREFIX), (
            "a read carrying no credentials returned the draft %r" % identifier)
    blog = site.get(C.ROUTE_BLOG)
    assert blog.status_code in C.OK_READ, (
        "GET %s returned %s" % (C.ROUTE_BLOG, blog.status_code))
    assert C.DOC_KEYS not in C.body_text(blog), (
        "the public blog index named the never-published article %r"
        % C.DOC_KEYS)


def test_viewer_cannot_read_a_draft(api):
    viewer = C.bearer(api, C.VIEWER_EMAIL)
    response = C.read_doc(api, viewer, C.DATASET_PRODUCTION, C.DOC_KEYS,
                          C.PERSPECTIVE_DRAFTS)
    assert response.status_code in C.DENIED_OR_MISSING, (
        "a viewer reading the never-published document %r under the %r "
        "perspective was answered %s rather than refused"
        % (C.DOC_KEYS, C.PERSPECTIVE_DRAFTS, response.status_code))
    raw = C.read_doc(api, viewer, C.DATASET_PRODUCTION,
                     C.DRAFT_PREFIX + C.DOC_AURORA, C.PERSPECTIVE_RAW)
    assert raw.status_code in C.DENIED_OR_MISSING, (
        "a viewer reading the stored draft %r was answered %s rather than "
        "refused" % (C.DRAFT_PREFIX + C.DOC_AURORA, raw.status_code))


def test_perspective_downgrade_is_stated_not_an_error(api):
    viewer = C.bearer(api, C.VIEWER_EMAIL)
    response = C.run_query(api, viewer, C.DATASET_PRODUCTION,
                           '*[_type == "article"]{_id}',
                           perspective=C.PERSPECTIVE_DRAFTS)
    assert response.status_code in C.OK_READ, (
        "a published-only caller asking for the %r perspective was answered %s "
        "rather than published content plus a stated downgrade: an error would "
        "itself say that drafts exist"
        % (C.PERSPECTIVE_DRAFTS, response.status_code))
    headers = {str(k).lower(): str(v) for k, v in response.headers.items()}
    stated = any("perspective" in k for k in headers) or \
        "perspective" in C.body_text(response).lower()
    assert stated, (
        "the answer did not state that the perspective was downgraded: the "
        "headers were %r" % sorted(headers))
    ids = [str(C.field(row, C.FIELD_ID)) for row in C.query_result(response)]
    assert C.DOC_KEYS not in ids, (
        "the downgraded answer still carried the never-published document %r"
        % C.DOC_KEYS)


def test_unfiltered_mutation_by_query_is_refused(api, store):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    before = store.count(C.TABLE_DOCUMENT, dataset=C.DATASET_PRODUCTION)
    response = C.mutate(api, headers, C.DATASET_PRODUCTION,
                        [{C.MUTATION_DELETE: {"query": "*"}}],
                        extra={"confirm": True})
    assert response.status_code in C.REFUSED, (
        "a delete addressed by an unfiltered query was answered %s rather than "
        "refused: it is refused always, with no override"
        % response.status_code)
    assert C.error_code(response) == C.CODE_UNFILTERED, (
        "the refusal carried the code %r rather than %r: %r"
        % (C.error_code(response), C.CODE_UNFILTERED, response.text[:300]))
    C.settle()
    after = store.count(C.TABLE_DOCUMENT, dataset=C.DATASET_PRODUCTION)
    assert after == before, (
        "the refused unfiltered delete removed %d document(s)" % (before - after))


def test_unconfirmed_mutation_by_query_is_refused(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    response = C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_DELETE: {"query": '*[_type == "article" && department == "%s"]'
                             % C.DEPARTMENT_ENGINEERING}}])
    assert response.status_code in C.REFUSED, (
        "a mutation addressed by query without the confirmation flag was "
        "answered %s rather than refused" % response.status_code)
    assert C.error_code(response) == C.CODE_UNCONFIRMED, (
        "the refusal carried the code %r rather than %r: %r"
        % (C.error_code(response), C.CODE_UNCONFIRMED, response.text[:300]))


def test_mutation_by_query_is_audited(api):
    editor = C.bearer(api, C.EDITOR_EMAIL)
    admin = C.bearer(api, C.ADMIN_EMAIL)
    marker = C.probe_token()
    query = ('*[_type == "article" && department == "%s" && title == "%s"]'
             % (C.DEPARTMENT_ENGINEERING, marker))
    C.mutate(api, editor, C.DATASET_PRODUCTION,
             [{C.MUTATION_DELETE: {"query": query}}], extra={"confirm": True})
    C.settle()
    response = C.read_audit(api, admin)
    assert response.status_code in C.OK_READ, (
        "reading the audit log as the administrator returned %s: %r"
        % (response.status_code, response.text[:300]))
    text = C.body_text(response)
    assert marker in text, (
        "a mutation addressed by query left no audit entry naming its query "
        "text: every use is recorded with its query text, its count and its "
        "actor, whatever the outcome")


def test_audit_chain_verifies_end_to_end(api, store):
    admin = C.bearer(api, C.ADMIN_EMAIL)
    editor = C.bearer(api, C.EDITOR_EMAIL)

    def audited_action():
        return C.mutate(api, editor, C.DATASET_PRODUCTION, [
            {C.MUTATION_DELETE: {
                "query": '*[_type == "article" && title == "%s"]'
                         % C.probe_token()}}], extra={"confirm": True})

    C.in_parallel(audited_action, 20)
    C.settle()
    rows = store.rows(C.TABLE_AUDIT)
    assert rows, (
        "the audit log holds no entries after twenty audited actions")
    by_hash = {}
    for row in rows:
        value = C.field(row, "hash")
        if value is not None:
            by_hash[str(value)] = row
    assert len(by_hash) == len(rows), (
        "%d audit entries produced %d distinct hashes: the chain is written "
        "through one writer so the predecessor of each entry is unambiguous"
        % (len(rows), len(by_hash)))
    predecessors = [str(C.field(row, "prev_hash") or "") for row in rows]
    dangling = [p for p in predecessors if p and p not in by_hash]
    assert not dangling, (
        "%d audit entries name a predecessor hash that is not in the log: the "
        "chain must verify end to end. The dangling values were %r"
        % (len(dangling), dangling[:4]))


def test_publish_with_draft_dependency_is_refused(api, store):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    response = C.publish_doc(api, headers, C.DATASET_PRODUCTION, C.DOC_KEYS)
    assert response.status_code in C.REFUSED, (
        "publishing %r, whose strong reference names the draft-only %r, was "
        "answered %s rather than refused"
        % (C.DOC_KEYS, C.DOC_AUTHOR_TOMAS, response.status_code))
    assert C.error_code(response) == C.CODE_PUBLISH_DEPENDENCIES, (
        "the refusal carried the code %r rather than %r: %r"
        % (C.error_code(response), C.CODE_PUBLISH_DEPENDENCIES,
           response.text[:300]))
    assert C.mentions(response, C.DOC_AUTHOR_TOMAS), (
        "the refusal did not name the unpublished dependency %r: %r"
        % (C.DOC_AUTHOR_TOMAS, response.text[:400]))
    C.settle()
    assert store.document(C.DATASET_PRODUCTION, C.DOC_KEYS) is None, (
        "the refused publish of %r wrote a published row anyway" % C.DOC_KEYS)
    together = C.publish_doc(api, headers, C.DATASET_PRODUCTION, C.DOC_KEYS,
                             also=[C.DOC_AUTHOR_TOMAS])
    assert together.status_code in C.OK_WRITE, (
        "publishing %r together with its dependency %r was answered %s: the "
        "refusal offers to publish them together in one transaction"
        % (C.DOC_KEYS, C.DOC_AUTHOR_TOMAS, together.status_code))


def test_strong_reference_blocks_delete_and_names_referrers(api, store):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    response = C.mutate(api, headers, C.DATASET_PRODUCTION, [
        {C.MUTATION_DELETE: {"id": C.DOC_AUTHOR_MARIT}}])
    assert response.status_code in C.REFUSED, (
        "deleting %r, which %r names with a strong reference, was answered %s "
        "rather than refused"
        % (C.DOC_AUTHOR_MARIT, C.DOC_AURORA, response.status_code))
    assert C.error_code(response) == C.CODE_DELETE_BLOCKED, (
        "the refusal carried the code %r rather than %r: %r"
        % (C.error_code(response), C.CODE_DELETE_BLOCKED, response.text[:300]))
    assert C.mentions(response, C.DOC_AURORA), (
        "the refusal did not name the referring document %r: a refusal saying "
        "only that the document is referenced leaves the operator with nowhere "
        "to go. The body was %r" % (C.DOC_AURORA, response.text[:400]))
    C.settle()
    assert store.document(C.DATASET_PRODUCTION, C.DOC_AUTHOR_MARIT), (
        "the refused delete removed %r anyway" % C.DOC_AUTHOR_MARIT)


def test_weak_dangling_reference_dereferences_to_null(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    document_id = C.DRAFT_PREFIX + C.probe_id("article-probe")
    document = C.article_doc(document_id, C.probe_title())
    document["related"] = {"_type": "reference",
                           "_ref": C.probe_id("article-absent"),
                           "_weak": True}
    created = C.mutate(api, headers, C.DATASET_PRODUCTION,
                       [{C.MUTATION_CREATE: document}])
    assert created.status_code in C.OK_WRITE, (
        "creating a document holding a weak reference to a document that does "
        "not exist was answered %s: a weak reference that dangles is not an "
        "error" % created.status_code)
    response = C.run_query(api, headers, C.DATASET_PRODUCTION,
                           '*[_id == $id]{"target": related->title}',
                           {"id": document_id}, C.PERSPECTIVE_RAW)
    assert response.status_code in C.OK_READ, (
        "dereferencing a dangling weak reference was answered %s rather than "
        "with a result: %r" % (response.status_code, response.text[:300]))
    rows = C.query_result(response)
    assert rows, (
        "the query over %r came back empty: %r"
        % (document_id, response.text[:300]))
    assert rows[0].get("target") is None, (
        "dereferencing a dangling weak reference produced %r rather than null"
        % (rows[0].get("target"),))


def test_uploaded_bytes_live_in_the_bucket_at_the_pinned_key(api, bucket):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    payload = C.png_bytes(8, 6, tone=17)
    response = C.upload_asset(api, headers, C.DATASET_PRODUCTION, payload)
    assert response.status_code in C.OK_WRITE, (
        "uploading a file to %s returned %s: %r"
        % (C.API_ASSETS, response.status_code, response.text[:300]))
    asset_id = C.asset_id_of(response)
    assert asset_id.startswith("image-"), (
        "the created asset carried the identifier %r; the identifier embeds "
        "the content hash and the dimensions" % asset_id)
    assert "8x6" in asset_id, (
        "the asset identifier %r does not embed the measured dimensions of the "
        "uploaded file" % asset_id)
    C.settle()
    prefix = "%s%s/" % (C.ASSET_PREFIX, C.DATASET_PRODUCTION)
    keys = bucket.list(prefix)
    assert keys, (
        "the bucket holds no object under %r after an upload: every uploaded "
        "byte lives in the object store at its content-addressed key, and "
        "nowhere else" % prefix)
    fresh = [k for k in keys if k != C.ASSET_OBJECT_KEY]
    assert fresh, (
        "the upload added no new object under %r; the bucket held %r"
        % (prefix, keys[:8]))
    assert bucket.exists(C.ASSET_OBJECT_KEY), (
        "the seeded asset is not in the bucket at %r" % C.ASSET_OBJECT_KEY)


def test_identical_uploads_deduplicate_to_one_asset(api, store):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    payload = C.png_bytes(9, 7, tone=41)
    first = C.upload_asset(api, headers, C.DATASET_PRODUCTION, payload,
                           filename="first.png")
    second = C.upload_asset(api, headers, C.DATASET_PRODUCTION, payload,
                            filename="second.png")
    assert first.status_code in C.OK_WRITE and second.status_code in C.OK_WRITE, (
        "uploading the same bytes twice returned %s then %s: %r"
        % (first.status_code, second.status_code, second.text[:300]))
    assert C.asset_id_of(first) == C.asset_id_of(second), (
        "uploading identical bytes produced two asset identifiers, %r and %r: "
        "deduplication is a property of the identifier"
        % (C.asset_id_of(first), C.asset_id_of(second)))
    C.settle()
    stored = store.count(C.TABLE_ASSET, dataset=C.DATASET_PRODUCTION,
                         _id=C.asset_id_of(first))
    assert stored == 1, (
        "the asset store holds %d rows for the identifier %r after two uploads "
        "of the same bytes" % (stored, C.asset_id_of(first)))


def test_derived_rendering_is_cached_under_its_own_prefix(api, bucket):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    response = C.read_asset(api, headers, C.DATASET_PRODUCTION, C.ASSET_SEEDED,
                            {"w": 400, "h": 400, "fit": "crop"})
    assert response.status_code in C.OK_READ, (
        "requesting a derived rendering of %r returned %s: %r"
        % (C.ASSET_SEEDED, response.status_code, response.text[:200]))
    C.settle()
    keys = bucket.list(C.DERIVED_PREFIX)
    assert keys, (
        "no derived rendering was cached under %r: a derived result is content "
        "addressed by the source asset together with its exact parameter set"
        % C.DERIVED_PREFIX)
    assert any(C.DATASET_PRODUCTION in key for key in keys), (
        "the cached derived renderings name no dataset: %r" % keys[:8])


def test_crop_on_one_use_leaves_other_uses_unchanged(api):
    editor = C.bearer(api, C.EDITOR_EMAIL)
    other = C.bearer(api, C.EDITOR2_EMAIL)
    before = C.doc_body(C.read_doc(api, other, C.DATASET_PRODUCTION,
                                   C.DOC_QUARTERLY, C.PERSPECTIVE_DRAFTS))
    response = C.mutate(api, editor, C.DATASET_PRODUCTION, [
        {C.MUTATION_PATCH: {
            "id": C.DRAFT_PREFIX + C.DOC_AURORA,
            "set": {"cover.crop": {"top": 0.1, "bottom": 0.05,
                                   "left": 0.2, "right": 0.0}}}}])
    assert response.status_code in C.OK_WRITE, (
        "changing the crop on one use of %r returned %s: %r"
        % (C.ASSET_SEEDED, response.status_code, response.text[:300]))
    C.settle()
    after = C.doc_body(C.read_doc(api, other, C.DATASET_PRODUCTION,
                                  C.DOC_QUARTERLY, C.PERSPECTIVE_DRAFTS))
    assert after.get("cover") == before.get("cover"), (
        "cropping the image inside %r changed the use inside %r as well: the "
        "crop, the hotspot and the alternative text belong to the use rather "
        "than to the asset. Before %r, after %r"
        % (C.DOC_AURORA, C.DOC_QUARTERLY, before.get("cover"),
           after.get("cover")))
    alt = (after.get("cover") or {}).get("alt")
    assert alt == C.ALT_QUARTERLY, (
        "the alternative text of the marketing use reads %r rather than %r"
        % (alt, C.ALT_QUARTERLY))


def test_square_rendering_keeps_the_hotspot_visible(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    square = C.read_asset(api, headers, C.DATASET_PRODUCTION, C.ASSET_SEEDED,
                          {"w": 400, "h": 400, "fit": "crop"})
    assert square.status_code in C.OK_READ, (
        "requesting a square rendering of the wide seeded asset returned %s"
        % square.status_code)
    assert square.content, (
        "the square rendering came back empty")
    huge = C.read_asset(api, headers, C.DATASET_PRODUCTION, C.ASSET_SEEDED,
                        {"w": 99999, "h": 99999, "fit": "crop"})
    assert huge.status_code in C.OK_READ, (
        "a request far beyond the original's dimensions returned %s rather "
        "than a clamped rendering: a width beyond the original clamps rather "
        "than upscaling" % huge.status_code)
    assert len(huge.content) < 40 * 1024 * 1024, (
        "a request beyond the original's dimensions produced %d bytes: every "
        "transformation parameter is bounded" % len(huge.content))


def test_private_dataset_asset_requires_credentials(api):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    anonymous = C.read_asset(api, None, C.DATASET_PRODUCTION, C.ASSET_SEEDED)
    assert anonymous.status_code in C.DENIED_OR_MISSING, (
        "an asset in the private dataset %r was served to a caller with no "
        "credentials: %s. An asset in a private dataset is served only through "
        "the authenticated streaming path"
        % (C.DATASET_PRODUCTION, anonymous.status_code))
    allowed = C.read_asset(api, headers, C.DATASET_PRODUCTION, C.ASSET_SEEDED)
    assert allowed.status_code in C.OK_READ, (
        "the same asset was refused to the signed-in editor: %s"
        % allowed.status_code)


def test_mislabelled_upload_is_refused(api, store):
    headers = C.bearer(api, C.EDITOR_EMAIL)
    before = store.count(C.TABLE_ASSET, dataset=C.DATASET_PRODUCTION)
    response = C.upload_asset(api, headers, C.DATASET_PRODUCTION,
                              b"this is not an image at all",
                              filename="pretend.png")
    assert response.status_code in C.REFUSED, (
        "a file whose declared type disagrees with its leading bytes was "
        "answered %s rather than refused: the type is read from the bytes and "
        "never from the filename" % response.status_code)
    assert C.error_code(response) == C.CODE_ASSET_TYPE, (
        "the refusal carried the code %r rather than %r: %r"
        % (C.error_code(response), C.CODE_ASSET_TYPE, response.text[:300]))
    C.settle()
    after = store.count(C.TABLE_ASSET, dataset=C.DATASET_PRODUCTION)
    assert after == before, (
        "the refused upload created %d asset row(s)" % (after - before))
