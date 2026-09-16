# Quarto Structured Content Platform

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, sign in as the
engineering editor, open the article `article-aurora-pipeline`, embolden the middle of a
word in its second paragraph, watch a colleague's marker appear beside the same field,
publish the document, land on a confirmation naming the revision it produced, and then see
that same article on the public blog index and inside the listing that names its author,
without hitting an error page. A different stranger signed in as the marketing editor must
NOT be able to read `article-aurora-pipeline` by any means, and a stranger with no
credentials at all must NOT be able to read `article-keys-and-arrays`, which has never been
published. Neither guarantee can be arranged in the interface: the article's image must
exist as a real object in the MinIO bucket at its content-addressed key, the published
revision must exist as a real row in PostgreSQL with its own place in the document's
revision chain, and a word that was emboldened halfway through must still be findable in
search as one word.

## Overview

Quarto is a content platform for engineering and editorial teams who publish one body of
content to many surfaces at once. It has two halves and a hard line between them.

The **Content Store** holds documents, answers queries about them, streams changes and
serves assets. **Quarto Studio** is an editing application, configured in code, that
produces a working editing interface from a schema. The line between them is the product's
whole argument: the store has no idea the Studio exists, so anything an editor can do by
clicking, a script can do without it. That is what makes migration possible at all, and it
is what makes the product usable by teams who never open the Studio.

What is stored is a document: a bundle of named fields with a type. An article is a
document, so is an author. What it is not is a page. The same document feeds a website, an
application, a shop screen and an email, so it stores what the thing **is** rather than how
it looks. Rich text is stored as structure rather than as markup, which is what lets the
same article render four ways, be queried inside, be edited by two people at once, and carry
nothing that has to be sanitized on the way out.

Four audiences arrive at the public half. A developer evaluating wants to know how fast they
can have it running, and is answered by a command they can copy. A developer integrating
wants to know what the query language does, and is answered by the documentation. An
editorial lead wants to know whether their team can use it. A buyer wants to know whether it
is safe.

The genuinely hard part is that every collaborative property in this product is a
consequence of one rule that looks like a technicality: every object inside an array carries
a small permanent name of its own, assigned when it is created, never reused and never
derived from its position. Get that wrong and the product demonstrates beautifully and falls
apart the first day two colleagues open the same article.

What this deliberately is not: there is no video and no player, no binary asset of any kind,
no third-party script, no outbound network call at runtime, no background worker, no
replica, no region, no backup or restore, no billing, no federated identity, no signup and
no password reset.

## User roles

Four roles. Signup is closed: people and their departments are seeded and there is no
self-registration anywhere in the product.

| Role | Can read | Can write |
|---|---|---|
| `viewer` | Published documents in any dataset they are granted, and nothing else | Nothing. **Cannot create, edit, publish or delete any document. Cannot read a draft, at any address, under any perspective.** |
| `contributor` | Published documents and drafts whose `department` equals their own | Create a document, patch a draft, upload an asset, and discard their own draft, all within their own department. **Cannot publish or unpublish anything. Cannot read or write a document in another department. Cannot delete a published document. Cannot reach any project route.** |
| `editor` | Everything `contributor` reads, in their own department | Everything `contributor` writes, plus publish, unpublish, schedule, create a release, and run a query in the playground. **Cannot read or write a document in another department. Cannot deploy a schema, run a migration, create a token, change a grant, copy a dataset or change a dataset's visibility. Cannot read the audit log.** |
| `administrator` | Every dataset, every document in every department, the schema, tokens, grants, webhooks, migration runs and the audit log | Deploy a schema, create and delete a dataset, change a dataset's visibility, copy a dataset, create and revoke a token, create and remove a grant, configure a webhook, and run a migration. **Cannot create, patch, publish or unpublish a document.** The person who decides who may change the content does not change it. |
| anonymous visitor | Every public route, and published documents in a public dataset | Submit the demo request form and record a cookie decision, and nothing else. **Cannot read a draft. Cannot reach any Studio or project address.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the
UI is not authorization: a direct API call from a `contributor` session to any
`editor`-only endpoint must be rejected by the server (an unauthorized request is denied,
not served), leaving the protected state unchanged.

Two rules sit on top of the role, and both are about the particular document in front of the
caller rather than the kind of person they are.

A grant carries a filter, and the filter is evaluated on the service on every read and every
write. `editor` and `contributor` hold a grant restricting them to documents whose
`department` equals their own. A document outside the grant is answered as not found rather
than as forbidden, because telling somebody a record exists is itself a disclosure, and it is
absent from every list, every query result and every search result rather than filtered out
of the page after it arrives.

A write that would move a document **out of** the writer's own grant is refused with the code
`grant_escape_refused`. Changing `department` from `engineering` to `marketing` while holding
the engineering grant is exactly that write, and permitting it makes every grant escapable by
editing your way out of it. A grant filter that fails to evaluate denies rather than permits.

Where a permit rule and a deny rule both match, the deny wins, every time.

Seeded people, all with the password `deku-demo-pw-2026`:

| Email | Name | Role | Department |
|---|---|---|---|
| `admin@example.com` | Ines Haugen | `administrator` | none |
| `editor@example.com` | Marit Solberg | `editor` | `engineering` |
| `editor2@example.com` | Tomas Lindqvist | `editor` | `marketing` |
| `contributor@example.com` | Priya Raman | `contributor` | `engineering` |
| `viewer@example.com` | Georg Almeida | `viewer` | none |

## Core features

### Auth and the dataset boundary

1. `POST /api/auth/login` takes `email` and `password`, checks them against the stored hash
   in PostgreSQL, and hands back an opaque `access_token`. Every later call presents it as
   `Authorization: Bearer <token>`. A password that is not the seeded one is turned away.
   So is an address no seeded person holds, answered identically, so the response never
   says which addresses exist.
2. That token identifies a person; it decides nothing. Role, department and grant are
   fetched from PostgreSQL while each request is being served, so a grant taken away this
   minute is gone from the next call rather than from whenever a token would have run out.
3. `GET /api/me` returns the signed-in person with their `role`, their `department` and the
   datasets they may reach. A caller with no token is denied.
4. `GET /api/datasets` returns the datasets the caller may reach, each carrying `id`,
   `visibility`, `document_count` and `asset_count`. Two datasets are seeded, `production`
   and `staging`, and both begin `private`.
5. Every store address carries its dataset as a path segment, and the dataset is resolved
   from that segment and re-authorised on every request. It is never taken from the session,
   from ambient configuration or from a value the client sends in a body. There are no
   cross-dataset queries, no cross-dataset transactions, and a reference that points into
   another dataset is always weak.
6. There is no signup endpoint, no password reset and no second identity provider anywhere
   in this application.

### What a document is

7. A document carries five reserved fields: `_id`, `_type`, `_rev`, `_createdAt` and
   `_updatedAt`. `_rev`, `_createdAt` and `_updatedAt` are assigned by the service and are
   refused when a client supplies them on a write. `_id` and `_type` are supplied by the
   client and are required.
8. The field kinds are closed: `string`, `text`, `number`, `boolean`, `date`, `datetime`,
   `url` and `slug` are primitives; `object` is a nested structure with its own fields and
   is **not** a separate document; `array` is ordered; `reference` points at another
   document; `image` and `file` are a reference to an asset plus per-use metadata; and
   `block` is one paragraph-level unit of rich text.
9. **Every object inside an array carries a `_key`**, a string unique within that array,
   assigned at creation and never reused, never reassigned and never derived from the item's
   position or its content. Every write path assigns it: a document created through the API
   with a five-item array comes back with five keys, not with keys that appear the first
   time somebody edits it. Editing an item and saving it ten times leaves every key
   unchanged. An array of objects without keys is not a content model, it is a list that
   corrupts the moment two people touch it.
10. The schema describes the editing interface and validates in the Studio. The store
    accepts any valid document shape. A document written by a script that does not match the
    current schema is stored, is queryable, and shows in the Studio as an unknown field
    rather than being rejected or silently dropped. Validation is advisory when a draft is
    saved and enforced when a document is published.

### Rich text, stored as structure

11. Rich text is an array of blocks. A block carries `_type` of `block`, a `_key`, a
    `style` of `normal` or `h1` through `h6` or `blockquote`, an optional `listItem` of
    `bullet` or `number`, an optional `level` of one or more, an array of `markDefs`, and an
    array of `children`. A child span carries `_type` of `span`, a `_key`, `text` and an
    array of `marks`. An array of rich text may also hold blocks that are not text at all:
    an image, a code sample, a callout, each an ordinary object with its own `_type` sitting
    between the text blocks.
12. **A decorator and an annotation are different things, and this is the commonest source
    of defects in the product.** A decorator is a label with no data: `strong`, `em`, `code`,
    stored as a literal string in `marks`. An annotation carries data: a link, a reference to
    another document, stored as an entry in `markDefs` with its own `_key`, and referenced by
    that key from `marks`.
13. A `marks` entry is a decorator when it names a decorator declared in the schema, and
    otherwise it is a key into `markDefs`. That resolution order is fixed. A build that looks
    for a matching `markDefs` entry first misbehaves the moment somebody names a decorator
    the same as a key, and declaring a decorator named the same as an existing key must
    leave the decorator winning.
14. A `markDefs` entry that no span references any longer is removed on the same write that
    orphaned it. Applying a link and removing it fifty times must leave `markDefs` empty.
    Orphaned annotations are invisible in the editor and inflate documents without bound.
15. A `marks` entry naming a `markDefs` key that is absent renders as unmarked text and is
    reported. It never throws and never stops the page. Documents in the wild will have this.
16. **Emboldening the middle of an unmarked span splits it into three.** The first resulting
    span keeps the original `_key`; the two new spans get new keys. Reassigning all three
    breaks every outstanding reference to that span, including another person's cursor.
17. Adjacent spans whose `marks` are equal **as sets** are merged, and the merge keeps the
    earlier key. `["strong","em"]` and `["em","strong"]` are the same set and must merge; a
    build comparing arrays grows a new span on every keystroke. An empty span is removed
    unless it is the only span in its block, in which case it is kept so the block still
    exists and still renders. Merging never crosses a block boundary.
18. Lists are not nested structures. A list is a run of adjacent blocks carrying the same
    `listItem`, and nesting is expressed by `level`. A `normal` block between two bulleted
    blocks ends the first list and starts a second. A level jump of more than one between
    consecutive items is normalized to one deeper.
19. **Whatever renders rich text groups the runs itself.** Five consecutive bulleted blocks
    render as one list of five items. A renderer that emits one list per item produces a page
    of single-item lists that looks almost right on screen and is announced as "list, one
    item" five times over.
20. Rendering is a per-surface concern, so serialization belongs to each surface and the
    product ships a serializer contract rather than a renderer: a component per block `style` with a fallback that renders as a
    paragraph and reports, a component per `marks` entry applied in a **stable order** so
    that bold-inside-link and link-inside-bold produce the same tree, a component per
    non-text block `_type` with a fallback that renders nothing visible and reports, and for
    anything unknown: never throw, never render raw, always report. A serializer that throws
    on an unknown block takes down a page because somebody added a content type; one that
    renders unknown content raw is an injection vector.
21. A renderer never infers structure that is not in the data. A paragraph beginning with a
    dash is not a list item, a line of dashes is not a rule, and markup characters inside
    `text` are literal characters. Text stored with markup characters in it comes back
    byte-identical.

### Drafts, publishing and the revision chain

22. A document being edited and a document being served are **two documents**, not two
    states of one. The draft's identity is the published identity with the reserved prefix
    `drafts.`, so the draft of `article-aurora-pipeline` is `drafts.article-aurora-pipeline`.
    A draft is an ordinary document, so every mutation, query, grant and listener mechanism
    applies to it unchanged, and a published document with no draft has no draft document at
    all rather than a null column.
23. Four states exist and the interface distinguishes all four, labelled exactly
    `Not published` when only a draft has ever existed, `Published` when the published
    document exists and no draft does, `Published with unpublished edits` when both exist,
    and `Draft` when the document was published once, was taken down, and its draft is kept.
    Collapsing "never published" and "published with edits" into "has a draft" is the defect
    that leaves an editor unable to answer the only question they care about, which is what
    is live right now.
24. **Publishing is one transaction.** It writes the draft's content over the published id
    and deletes the draft, and either both land or neither does. Done as two calls, a failure
    in the gap either leaves a draft that is live but still reads as unpublished, or deletes
    a draft whose content never reached the published document, and the second is data loss.
    Unpublishing is the mirror: create the draft from the published document and delete the
    published one, in one transaction.
25. Every mutation produces a new `_rev`, and every revision is addressable through
    `GET /api/data/history/{dataset}/{id}`. History is append-only: nothing is ever removed
    from it by an ordinary edit, restoring a revision is itself a new revision rather than a
    rewind, and the history of the draft and of the published document is one chain, because
    publishing is a write to the published document like any other. A document's history
    survives the document being deleted, and the document is restorable from it.
26. A query names which of the two it wants. `published` returns published documents only.
    `drafts` returns drafts overlaid on published, so a document with a draft returns the
    draft, and the returned document carries the **published id**, not the prefixed one, so a
    preview renders identically to production. `raw` returns both as they are stored, with
    the prefixed ids visible.
27. **The default perspective for a read with no credentials is `published`.** A build
    defaulting to `drafts` publishes unfinished work to the world and it will not be noticed
    until it is. A perspective is not a filter consumers apply: a consumer that fetches `raw`
    and filters in the browser has fetched unpublished content to a browser, which is the
    same leak by another route.
28. Preview is a signed, expiring grant to read `drafts` for one document, never a permanent
    token embedded in a front end. It expires after the number of seconds in
    `PREVIEW_GRANT_TTL_SEC`, is bound to one document in one dataset, and is revocable. An
    expired or revoked grant is refused with `preview_grant_expired`.

### Mutations, patches and transactions

29. `POST /api/data/mutate/{dataset}` takes a client-supplied `transactionId` and an ordered
    array of `mutations`. The mutation types are `create`, which fails when the id exists;
    `createOrReplace`, which writes wholesale; `createIfNotExists`, which is a no-op when the
    id exists; `patch`, which applies operations to specific paths; and `delete`.
30. **An editing interface uses `patch`.** `createOrReplace` from an editor is the defect
    that makes collaboration impossible: it writes the whole document from one client's view
    of it, so anything anybody else changed in the meantime is silently reverted.
31. The patch operations are `set`, which writes and creates the path when absent;
    `setIfMissing`; `unset`, which removes; `inc` and `dec`, which are server-side arithmetic
    so a counter is never read, added to and written back by a client; `insert`, carrying
    `before`, `after` or `replace` and an `items` array; `diffMatchPatch`, which sends a
    textual difference; and `ifRevisionID`, which states the revision the patch was based on.
    One hundred concurrent `inc` operations of one against a counter at zero leave it at
    exactly `100`.
32. A path addresses a place in a document, and takes forms such as `title`, `author.name`,
    `body[2].children[0].text`, `tags[_key == "x9f"]` and `categories[0:3]`. **Paths into
    arrays of objects use the key predicate form.** Index addressing is permitted only for
    reads and for arrays of primitives.
33. **Patching an array item by its index rather than its key is the failure this product is
    built to prevent.** Editing item `k3` while another client inserts an item at position
    zero must land on `k3`. Removing an item is by key. Inserting is relative to a key.
    Appending is the one index form that is correct, `insert: {after: "items[-1]"}`, because
    `-1` means the end regardless of length. Reordering is an unset by key and an insert by
    key in one transaction; rewriting the array is `createOrReplace` in miniature and reverts
    any concurrent edit to any item in it.
34. Long plain-text fields are edited with `diffMatchPatch`, which the service applies
    against the current value, because a `set` on the whole string is a save that quietly
    overwrites the other person. Rich text does **not** use it: it uses keyed patches into
    the block array, because a textual difference of a structure is meaningless. A
    `diffMatchPatch` that fails to apply is an error, never a silent overwrite.
35. Atomicity is absolute here. A single mutation is atomic and a transaction is atomic
    across every document it names.
    A patch with ten operations applies all ten or none, in the order given, so an `insert`
    after an `unset` in the same patch sees the array without the unset item. Sending a patch
    whose fourth operation is invalid leaves none of the four applied. A transaction produces
    one revision per affected document and one entry in the event stream, so a listener sees
    a consistent world.
36. **Every patch the Studio derives from a form the person was looking at carries
    `ifRevisionID`.** A machine writer that genuinely intends the later save to replace the
    earlier one omits it deliberately and says so in its own code, rather than omitting it
    because a library made that the easy path. A revision mismatch is refused with `revision_mismatch` and is never a
    silent overwrite. The client resolves it by replaying its outstanding local operations on
    top of the new revision, not by refetching and discarding what the person was typing.
37. Idempotency is carried by the client's own transaction id. Replaying a `transactionId` within the number of seconds in
    `TRANSACTION_REPLAY_WINDOW_SEC` returns the original result and applies nothing. Network
    retries are ordinary traffic on this API: without this, a retried publish creates a
    second revision, a retried `inc` counts twice, and a retried `create` fails confusingly
    instead of succeeding.
38. **Changing or deleting content by query is the most dangerous surface in the product,
    and it is guarded four ways.** It requires an explicit `confirm` flag that no client sets
    by default, and is refused with `mutation_by_query_unconfirmed` without it. It is refused
    with `unfiltered_mutation_refused` when the query carries no filter, always, with no
    override. A dry run returning the affected ids and count is the default in every
    interface that offers it. The affected count is bounded and the operation is refused
    above the bound with a pointer to the migration runner. Every use is written to the audit
    log with its query text, its count and its actor, whatever the outcome.

### References and what happens at the other end

39. A reference is `{_type: "reference", _ref: "author-marit", _weak: true|false}`, and
    strong is the default. Referential integrity is the store's job rather than a convention
    the callers agree to keep.
40. **Deleting a document with an incoming strong reference is refused** with
    `delete_blocked_by_references`, and the refusal **names the referring documents** up to a
    bound with a count beyond it. A refusal saying only that the document is referenced
    leaves the operator with no way to proceed. The refusal is evaluated at commit time, so a
    reference created at the same moment as the delete cannot slip through.
41. A weak reference that points at nothing is **not** an error. Dereferencing it yields
    `null` and every consumer handles it. Cycles are permitted, because content genuinely has
    them; what is bounded is the dereference depth of a query.
42. **Publishing a document whose strong references point at documents that exist only as
    drafts is refused** with `publish_dependencies_unpublished`, listing the unpublished
    dependencies and offering to publish them together as one transaction.
    `article-keys-and-arrays` references `author-tomas`, which is draft-only, and is the
    seeded case. A build that publishes anyway produces a live page pointing at nothing, and
    the error surfaces on the public site rather than in the Studio.

### The query language

43. `POST /api/data/query/{dataset}` takes `query`, an object of `params`, and an optional
    `perspective`, and returns `result` beside `cost`. The language is projection-oriented:
    `*` is every document, `[...]` filters, `| order(...)` orders, `[0...10]` slices,
    `{...}` projects the shape the caller wants back, `->` dereferences a reference,
    `"name": expr` renames or computes, `...` spreads the source object, and
    `cond => {...}` projects conditionally per item.
44. The caller declares the response shape, which is what removes the usual round-trip
    problem: an article, its author, the author's photograph and a count of related pieces
    are one query and one response. The consequence is stated rather than hidden: the caller
    owns the response's cost.
45. **Values reach a query as parameters and are never interpolated into query text.** A
    parameter whose value contains query syntax is a string containing query syntax and
    nothing else, and must come back as a literal rather than changing what the query
    selects. The service refuses a query whose text is longer than `16KB`. Where a query
    shape genuinely must vary, the variation is a choice from a fixed set of server-known
    queries, never a query assembled from what somebody typed. This is the injection surface
    of this product, and it looks less dangerous than the equivalent in a relational database
    only because the language is unfamiliar.
46. Dereferencing respects the perspective: under `drafts`, following a reference returns the
    draft of the target where one exists, so a preview is internally consistent.
47. The function set is closed: `count`, `defined`, `coalesce`, `select`, `references`,
    `length`, `now`, `round`, `string::split`, `array::unique`, `pt::text` for extracting
    plain text from rich text, and `score` with `boost` for relevance ordering. `now()` is
    evaluated once per query, on the service, never per document and never on the client, and
    a query using it is reported uncacheable.
48. The language performs no writes, no arbitrary computation, no cross-dataset join and no
    user-defined function. Each absence is deliberate, and together they are what keeps the
    cost of a query predictable.

### What a query costs, and saying so

49. **Every response carries its cost**, and the cost is visible in the playground where
    queries are written: documents examined before filtering, documents returned after it,
    dereferences performed with their count and depth, the time at the service, and whether
    an index was used and which. A query language whose cost is invisible produces incidents
    written by people who had no way to know.
50. `_type` and `_id` are always indexed. Equality on a declared field, ordering by a
    declared field, and the reverse lookup behind `references()` are backed by indexes
    declared in the schema and maintained on write. Anything else is a scan.
51. A query that would exceed a bound is refused with `query_bound_exceeded` and an
    explanation **naming the specific predicate** that made it expensive and the index that
    would fix it. A generic timeout teaches the caller nothing. The bounds are a dereference
    depth of `5`, a response size of `10MB`, an execution time of `10s` and the query text
    length above. Refusing loudly is better than serving slowly, because a slow query on a
    content platform is discovered by the customer's visitors rather than by the customer.

### Live updates

52. `GET /api/data/listen/{dataset}` holds a connection open and delivers events for
    documents matching a query, so another person's change appears without reloading the
    page. The first event is a `welcome`; each later event carries `documentId`,
    `transactionId`, `result`, `previousRev`, `resultRev` and `transition`.
53. **A gap is never silently bridged.** When an event's `previousRev` is not the revision
    the client holds, the client has missed something and refetches the document. Applying an
    event whose previous revision the client does not hold produces a document that is
    neither the client's state nor the service's.
54. An event carries the `transactionId` so a client recognises the echo of its own write and
    does not apply it twice. It does reconcile: the returned revision becomes the base for
    its next patch. A client that ignores its own echoes sends its next patch against a stale
    revision and is refused, which then looks like a conflict where there was none.
55. `transition` names whether the document appeared in, was updated within, or disappeared
    **from the query's result set**, which is not the same as being created or deleted: an
    edit that makes a document stop matching the filter is a disappearance, not a delete.
    Ordering is guaranteed per document, not globally.
56. Reconnection resumes from the last event id the client stored. The service holds a
    replay buffer, and a resume beyond it is refused rather than partially served, so the
    client resynchronizes by refetching. Reconnect delay grows with full jitter and is capped
    at `30s`, and the attempt counter resets on a successful `welcome` rather than on the
    connection opening, because resetting on the open produces a hot loop against a service
    that accepts and immediately closes.
57. A live query keeps a **result set** current rather than streaming document events, and it
    must handle four cases: a matching document changed, so replace it in place and preserve
    order unless the order key changed; a document started matching, so insert it at its
    ordered position; a document stopped matching, so remove it; and **a referenced document
    changed, so the result changes even though no document in the set changed**, because the
    projection dereferenced it. The fourth is the one that is missed: a listing projecting an
    author's name does not update when the author is renamed unless dereferenced documents
    are tracked as dependencies of the result.
58. A consumer that cannot keep up has a bounded outbound queue. On overflow the connection
    is closed with a resumable code and never silently trimmed of events: a slow consumer
    loses its connection, never its data.

### Two people in one document

59. Editing produces patches against paths, not document snapshots. Two clients editing
    different fields both land. Two clients editing different items in one array both land,
    because addressing is by key. Two clients emboldening different words in one paragraph
    both land, because spans are keyed. Two clients writing the same primitive field resolve
    to the later save, and the earlier writer is told rather than left to discover it. Two
    clients editing the same long text field, or the same span's text, are merged by textual
    difference. Structural operations on one array are serialized by the service, which
    assigns an order and refuses operations whose preconditions no longer hold, while text
    edits inside those items stay concurrent and unaffected.
60. Presence carries which document a person has open, which field they are focused on, their
    cursor and selection inside a text field at no more than `20` updates a second, and their
    name and avatar. It carries nothing else, never a stable address. It is never persisted,
    never replayed to somebody joining, and never the source of a lock.
61. **Nothing is locked, and that is a product decision rather than an omission.** Locking is
    easier to build and worse to use: locks are left behind by people who went to lunch, so
    an override is needed, and the override becomes the normal path. Presence plus per-path
    merging handles the real cases, and the residual case of two people typing in the same
    sentence in the same second is resolved by merging.
62. **A person's typing is never discarded to resolve a conflict.** Rebasing is what happens
    instead. When a patch is refused for a revision mismatch, the client fetches the current document and its revision,
    computes the difference from the base it held, transforms its outstanding local
    operations against that difference, reapplies them and resends with the new revision. If
    a local operation targeted something that no longer exists, it is dropped **and the
    person is told exactly what was dropped**, naming the field or the item. Silently
    dropping somebody's edit because the thing it targeted was deleted is data loss with a
    friendly face.
63. A cursor keeps its position relative to the text rather than its numeric offset. A cursor
    at the fortieth character when a colleague inserts ten characters above it belongs at the
    fiftieth. A build that stores cursors as numbers alone moves everybody's cursor backwards
    every time a colleague types above them.
64. What a person sees: another person in the document is a marker in the header; another
    person in the field being edited is a marker beside the field and their cursor inside a
    text field; a remote change to the field being edited applies and the local cursor keeps
    its place in the text; a remote change to a field not being edited applies with a brief
    highlight; and a local edit dropped in a replay is a named, dismissible notice.

### The Studio: schema, forms and validation

65. A schema declares document types and their fields, and generates the editing interface.
    A type carries `name`, `title`, `type`, `fields` for objects and documents, `of` for
    arrays, `to` for references naming the permitted target types, `options`, `validation`,
    `preview`, `initialValue`, and `readOnly` and `hidden` which may be static or a function
    of the document and the person. Schema is code and is deployed, which is what makes a
    schema change a reviewable difference with a history and makes a migration writable
    against the difference between two known versions.
66. **`readOnly` and `hidden` are interface affordances, not security.** A hidden field is
    still in the document, still returned by a query and still writable through the mutation
    API by anybody with write access. This is the single most likely misunderstanding of the
    Studio's capabilities, and a build that hides a field and believes it has protected it
    has not.
67. Any field may declare a custom editing component. A custom input receives the value, a
    change callback that emits **patches**, the presence data and the validation state. A
    custom input that emits whole values instead of patches breaks collaboration for that one
    field, which is the hardest kind of defect to notice.
68. Every type declares how it appears in a list: a title, a subtitle, a thumbnail. **A
    preview must not require a query.** It is computed from fields on the document with at
    most one dereference, because a list of one hundred documents whose previews each run a
    query is one hundred queries.
69. Validation has three levels. An `error` blocks publishing and does not block saving a
    draft. A `warning` is advisory and never blocks. An `info` is guidance. **Drafts always
    save**, however incomplete or wrong, because somebody interrupted mid-sentence must never
    lose what they had. Custom validation may query, runs asynchronously, waits for typing to
    settle rather than running on every keystroke, and the interface distinguishes "not yet
    validated" from "valid". Validation runs again at publish time, on the service. Errors are
    attached to paths, so an error on the fourth item of an array stays on that item when the
    array is reordered.
70. The document table is a query walked with a cursor, and it renders only the rows that fit
    and stays responsive as the person scrolls. Editors work in datasets with hundreds of
    thousands of documents, and a list that fetches everything is unusable for the largest
    customers, who are also the most valuable ones.

### Assets and the image pipeline

71. **An uploaded file produces an asset document, and each place that uses it holds a
    reference plus per-use metadata.** The asset owns the bytes, the dimensions, the palette,
    the blur placeholder and the extracted metadata. The use owns the crop, the hotspot, the
    alternative text and the caption. The same photograph used in three places is one asset
    with three different crops and three different alternative texts, and a build that stores
    the crop on the asset makes one editor's crop change every other use of that image.
72. `POST /api/assets/{dataset}` takes the file and returns the asset document. Its `_id` has
    the form `image-<sha256 of the bytes>-<width>x<height>-<ext>`, so the id embeds the
    content hash and the dimensions. **Uploading identical bytes twice yields one asset,
    referenced twice**: deduplication is a property of the id rather than a lookup. It is
    never surfaced to the uploader, because telling somebody their upload already existed
    reveals another person's content. Deleting an asset that is referenced is refused, the
    same way a document is.
73. **Every uploaded byte lives in the MinIO bucket named by `STORAGE_BUCKET` at
    `STORAGE_ENDPOINT`, and nowhere else.** The object key scheme is
    `assets/{dataset}/{sha256_of_bytes}.{ext}`, for example
    `assets/production/9f2ae1c4d0b7.png`. Bytes on the application container's filesystem, a
    blob column in PostgreSQL, or a base64 string inside a document are each a contract
    violation however good the interface looks.
74. Derived renderings are cached in the same bucket under
    `derived/{dataset}/{sha256_of_bytes}/{parameter_digest}.{ext}`, where the parameter
    digest is taken over the exact parameter set in a canonical order, so the cache key
    cannot collide and a purge is precise.
75. Assets in a private dataset are readable only through the authenticated streaming
    endpoint `GET /api/assets/{dataset}/{asset_id}`, which re-authorises on every request.
    In a public dataset an asset referenced by a published document is readable without
    credentials, and **an asset referenced only by a draft still requires credentials**.
76. Crop and hotspot are fractions of the original, never pixels, because pixels break the
    moment a larger original replaces the file. `crop` carries `top`, `bottom`, `left` and
    `right`; `hotspot` carries `x`, `y`, `width` and `height` and marks the region that must
    survive.
77. **The order is fixed: apply the crop, then fit the requested aspect around the hotspot,
    then scale.** Any other order produces a different image, and the difference is a face
    with the top of its head missing. Rotation recorded in the file's own orientation
    metadata is applied **before** the crop is interpreted, because the crop was authored
    against the visually upright image. When the requested aspect fits inside the crop
    without losing any of the hotspot, the hotspot has no effect: it is a region to preserve,
    not a centre point, and treating it as a centre produces off-centre crops whenever it
    sits near an edge.
78. The transformation parameters are closed and every one is bounded: `w` and `h`, which
    clamp rather than upscale beyond the original; `fit`, one of `crop`, `clip`, `fill`,
    `max`, `min` or `scale`; `fm` for the format, with negotiation and a defined fallback;
    `q` for quality; `blur`, `sharp` and `sat`; `rect`, an explicit crop that **overrides**
    the field's crop rather than composing with it; and `auto`. An unbounded transformation
    parameter is a way to spend a rendering budget from a browser. A transformation that
    fails serves the original at a bounded size rather than an error, because a missing image
    on somebody's home page is worse than a slightly wrong one.
79. Dimensions, aspect, palette and a blur placeholder are extracted on upload, and so is the
    location recorded in the file's own metadata where it is present. **The location is
    stored where the project can see it and stripped from the served file**, and it is not
    returned by default in a query. A photograph uploaded by a journalist must not publish
    the coordinates of where it was taken because a content platform passed the bytes through
    unchanged.
80. Upload safety: the type is determined from the leading bytes and never from the filename;
    the dimensions are read from the header and checked before any decode allocates memory;
    decoding runs with memory and time caps; everything is re-encoded from decoded pixels so
    nothing uploaded is ever served back byte for byte; and files are served from a path
    holding no session credentials, with inline rendering disabled outside a small allow list.
    A file whose declared type does not match its bytes is refused with `asset_type_refused`,
    and a header claiming enormous dimensions is refused before anything is allocated.

### Schema evolution and migration

81. A migration is code, it is versioned, and it is executed by a runner at
    `POST /api/project/migrations`. **The dry run is the default**: invoked without `mode`
    set to `apply`, it writes nothing and reports the count of documents affected and a
    sample of before-and-after pairs, under the line
    `Dry run: {n} documents would change. Nothing has been written.`
82. A migration is idempotent: running it twice does what running it once did, because
    migrations are interrupted and the operator's only safe response to an interruption is to
    run it again. It is resumable from a cursor, so a run over a million documents is not
    all-or-nothing. It is batched into transactions of a bounded size, so each batch is atomic
    even though the run is not. It is rate-limited so it does not starve live traffic. It
    records what ran, against which dataset, by whom, when and with what result. It is written
    with a reversal, or with an explicit statement that the change is irreversible and why.
83. **Every breaking change is three deployments, never fewer.** `expand`, in which the schema
    accepts both shapes and the application reads both and writes the new; `migrate`, in which
    the runner converts existing content resumably in batches; and `contract`, in which the
    schema drops the old shape. A rename done in one step loses every document written
    between the deployment and the conversion. The `contract` phase is refused until a
    verification query returns zero documents in the old shape, and that query is part of the
    migration's own definition rather than something an operator remembers to run.
84. **A migration that touches rich text preserves `_key` on every block and every span it
    does not explicitly remove.** Rebuilding a block array with fresh keys invalidates every
    outstanding editing session on those documents, detaches every annotation anchored to a
    block, and makes the document's difference against its own previous revision read as a
    complete rewrite. The rebuild looks correct in the result and has destroyed the
    document's identity.
85. The runner requires the dataset as an explicit argument with no default, ever, and it
    cannot read the dataset from ambient configuration. When the target is `production` it
    requires the dataset name to be typed again as confirmation and is refused with
    `production_confirmation_required` without it. The dry run's report states the dataset
    name in its first line.
86. The deployed schema is registered with its version, and the service reports, per dataset,
    how many documents do not validate against the current version and against which rules.
    Schema drift is invisible until somebody tries to publish and cannot.

### Datasets

87. A dataset is a named, isolated collection of documents and assets. Its visibility is
    `private` or `public`, new datasets default to `private`, and the visibility is shown
    wherever the dataset is named rather than only in its settings.
88. **Switching a dataset from `private` to `public` requires typing the dataset name** and
    shows a count of the documents that would become world-readable. The confirmation states
    `This dataset is public. Anyone can read its published content.` and says plainly that a
    public dataset still requires credentials for drafts, because "public" is otherwise
    reasonably read as "everything in it is public".
89. Copying one dataset into another states whether it includes drafts, assets and history,
    and each defaults to a deliberate answer rather than to everything. **A copy into a
    non-empty dataset is refused** unless the operator chooses between merge and replace
    explicitly, with a count for each. A copy into `production` requires the same typed
    confirmation a migration does. A copy into a dataset used for development runs the
    redaction rules the project declares for fields marked personal in the schema, or is
    refused with `personal_fields_undeclared` when none are declared and the source contains
    such a field. Copying live content into a test environment is the single most common way
    personal data ends up somewhere nobody is guarding.
90. Deleting a dataset requires typing its name, states the document and asset counts, and
    the dataset stays recoverable for `168h` before the data is removed.

### Tokens and grants

91. A token carries a scope of `read` or `write`, one dataset or all, never implicitly. Its
    value is shown once at creation and never again. Two tokens may be valid at once so one
    can be rotated without downtime. An expiry is optional and the interface pushes toward
    setting one. Every token records its last-used time and the prefix of the calling address.
    Revocation is immediate and propagates to open listeners within `5s`.
92. **A write token in a browser bundle is a published token.** The interface warns at
    creation when a token is scoped for write, and a write scoped token presented from a
    browser context is refused with `browser_write_token_refused` unless an explicit override
    is set, because the accident is not knowing it happened.
93. A grant is a role plus a query filter, for example
    `_type == "article" && department == $user.department`. The filter is evaluated on the
    service on every read and every write and never applied by a client. A restricted caller's
    raw response contains no restricted document at all, rather than containing them and
    hiding them. Grant filters are checked for cost like any query, because they run on every
    operation.
94. **There is no field-level security, and that is recorded so it is not added carelessly.**
    Genuine field-level security would require every projection, every listener event, every
    export and every history revision to be filtered per person per field, and a partial
    implementation is worse than none because it looks like protection. Where a field must be
    protected it belongs in a separate document with its own grant, and the interface says so
    at the exact point where somebody would otherwise reach for the hide switch.
95. A perspective and a grant are independent and both apply. A caller with read access to
    published content who asks for the `drafts` perspective receives published content only,
    with a response header stating that the perspective was downgraded, rather than an error.
    An error would itself leak that drafts exist.

### Webhooks

96. A webhook carries `id`, `name`, `url`, `dataset`, a `trigger` of `create`, `update` or
    `delete`, a `filter`, a `projection`, `headers`, a `secret`, an `enabled` flag and an
    `api_version`. The filter and the projection are what let a consumer receive exactly the
    documents it cares about in exactly the shape it wants, rather than every change in the
    dataset. Without a projection, a rebuild hook receives a whole document to decide whether
    one field changed.
97. A delivery is **recorded rather than sent**: this application makes no outbound network
    call at runtime, so each delivery is written to the delivery record with its webhook, its
    transaction id, the affected ids and a truncation flag, and nothing is ever fetched. A
    webhook address is validated at configuration time and is never called.
98. **The rebuild storm is the failure specific to this product.** A migration touching fifty
    thousand documents would, done naively, record fifty thousand deliveries, each one a
    request for somebody's site to rebuild itself. Deliveries are coalesced per webhook per
    window: a burst above a threshold collapses into one record carrying the affected ids up
    to a cap and a flag saying the list was truncated. A migration run declares itself, and a
    webhook may be configured to suppress during a declared migration and record once at the
    end. The interface warns, at the moment a mutation by query or a migration is confirmed,
    how many deliveries it will cause.

### Scheduling and releases

99. A document may be scheduled to publish at an instant, and the instant is stored with the
    scheduler's zone name rather than a fixed offset, so a schedule set for nine in the
    morning stays at nine in the morning across a daylight transition. A local time that does
    not exist resolves forward to the first valid instant; one that occurs twice takes the
    first.
100. Executing a schedule runs the publish transaction, including its reference checks. **A
     schedule whose dependencies are unpublished fails loudly and is recorded as `failed`
     with its reason**, rather than publishing a broken document at three in the morning. A
     scheduled document edited after scheduling publishes its current draft, and the
     interface says so at the moment of editing. Cancelling is available until execution, and
     execution is idempotent for one document at one instant. There is no background worker
     here: a schedule whose instant has passed executes the next time that schedule, its
     document or the release list is read or acted upon, and nothing an observer can see
     distinguishes that from a sweeper.
101. A release is a named set of documents published together, atomically, at one instant. It
     publishes in one transaction, because a release that publishes half of a product launch
     is worse than one that publishes none. A set exceeding the transaction bound is refused
     with `release_too_large` **at creation time**, with the size stated, rather than
     partially executed at release time. A release has a preview of its own, so the site can
     be seen as it will look afterwards. Validation for the whole set runs at schedule time
     and again immediately before execution, and a document that became invalid in between
     blocks the release and is named, rather than being dropped from it silently. Releases are
     archivable and their contents inspectable afterwards, because "what went out in the March
     launch" is a question people ask months later.

### Search

102. Two different things are called search and they are kept apart, because conflating them
     produces a product that is bad at both. Editor search runs over every document including
     drafts, needs recency and exact id and slug matching and filtering by type and author,
     tolerates some latency, and returns a document to open. Consumer search runs over
     published documents only by default, needs relevance, tolerates none, and returns a page
     to visit.
103. **Indexing rich text is the specific difficulty here**, because the searchable text of a
     document is not in a field: it is spread across an array of blocks and their spans.
     Plain text is extracted by concatenating spans **with block boundaries preserved**, so a
     phrase search cannot match across a paragraph break. **A span boundary inside a word must
     not break the indexed token**: a word whose middle is emboldened is stored as three
     spans and must index as one word. A build that indexes spans independently fails to find
     any word somebody happened to embolden halfway through, and the defect is invisible until
     a customer reports it about one specific word.
104. A non-text block contributes its own declared searchable fields, an image's alternative
     text for instance, and nothing else. An annotation contributes its target's title where
     the reference resolves, so a search for an author's name finds articles linking to them.
105. Ranking takes a field boost declared in the schema as its primary signal, an exact match
     on a title or slug as a high one, term frequency within the document as a moderate one,
     and recency as a tie-break only. Boosts are declared in the schema, so relevance is
     content modelling rather than a hidden tuning parameter.
106. **Results are filtered against the caller's grants at query time**, never from
     permissions recorded in the index. Somebody who lost access five seconds ago must not see
     the document in their results. The consequence is stated in the response: the total is
     approximate, because the page is fetched over-wide and trimmed.
107. An index that cannot answer says so. Search reports itself as `rebuilding` under the line
     `Search is catching up. Your document is not lost.` rather than returning zero results,
     because "no results" reads as "my document is gone" to somebody who just wrote it. A
     write becomes searchable within `10s`; a deletion or a permission change is processed
     within `2s` and **ahead of** insertions.

### Internationalization: content in several languages

108. Two patterns are supported and the tradeoff is named rather than chosen for the
     customer, because the right answer depends on their editorial process. Field-level keeps
     one document with each translatable field an object keyed by locale, which suits a small
     number of locales edited together and publishes them together, and makes per-locale
     grants impossible. Document-level keeps one document per locale linked by a shared
     identifier, which suits many locales with independent workflows and per-locale
     publishing, and multiplies the document count. The choice is recorded in the schema and
     cannot be mixed within one document type.
109. A fallback chain is declared per locale and ends at a required base locale. Fallback is
     applied at query time **by the caller's request**, never by silently substituting during
     editing: an editor must be able to see that a translation is missing, and a consumer must
     be able to receive something. A field that fell back is flagged in the response so a
     consumer can label it, which several markets require.
110. **An empty translation and a missing translation are different.** A translation
     deliberately set to an empty string does not fall back; a missing one does. A translator
     who means "there is no subtitle in this language" must not have the base language's
     subtitle appear instead.
111. Lengths and validation limits are counted in extended grapheme clusters rather than code
     units. Slugs are generated with locale-aware transliteration and the result is editable,
     because automatic transliteration is wrong often enough to matter. Document lists are
     sorted by the **reader's** locale rather than the content's. Text direction comes from
     the field's locale rather than from the interface. The interface language, the content's
     locale and the person's own locale are three independent things: somebody may work in one
     interface language on content in another while their dates render in a third, and a build
     assuming any two are the same is wrong for exactly the customers who buy this feature.

### The public site

112. The home route's spine carries, in order: an announcement bar with one sentence and a trailing
     arrow; a dark hero with a headline, a body line and three actions; a customer marquee; a
     numbered section index; five feature sections; a developer band; two very large closing
     actions; and the footer.
113. The hero's three actions are the primary `Start building`, the secondary `Watch demo`,
     and a third that is not a button at all: a monospace pill carrying the install command
     `npm create quarto@latest` with a copy control beside it. The audience is developers, and
     the shortest path from the home page to a running project is a line pasted into a
     terminal rather than a sign-up form. **The copy control copies the command text only**,
     without the prompt character and without any of the surrounding markup, which is the
     single most common defect in copy controls on developer sites.
114. The section index is a rail of five numbered entries set in the monospace face, reading
     `01 CONTENT-AS-DATA`, `02 EDITORIAL FREEDOM`, `03 CONTENT AGENT`,
     `04 AUTOMATION AT SCALE` and `05 POWER ANY APPLICATION`. **It is a navigation control,
     not a decoration**: each entry scrolls to its section, the active entry follows the
     scroll position, and the whole rail is reachable by keyboard. A numbered rail that only
     reflects position and cannot be used to move is a common and frustrating
     half-implementation.
115. The top bar carries seven entries: `Products`, `Solutions`, `Resources`, `Docs`,
     `Enterprise` and `Pricing`, with `Log in`, `Contact Sales` and `Get started` set apart on
     the right. The first three open a mega-menu of six groups, each with a promoted item:
     content operations, holding Quarto Studio, Quarto Agent, the Quarto SDK, the Media
     Library, Releases and an agent interface; content backend, holding the Content Store, a
     context service, a tool-connection server, functions and a delivery network; solutions by
     industry, holding commerce, media and publishing, and software; solutions by team,
     holding developers, editors, product owners and business leaders; resources, holding
     learning, community, frameworks, templates, tools and plugins, and schemas and snippets;
     and insight, holding the blog, engineering, events, customer stories, guides and use
     cases.
116. Code samples are tokenized when the site is built, never coloured in the browser. Each
     block declares its language, is reachable and scrollable by keyboard, and carries a copy
     control that copies the **source text** reassembled from its pieces rather than the
     highlighted markup. Where a sample exists in more than one language it is tabbed, and the
     choice is remembered for that visitor across blocks and across routes.
117. Diagrams are inline vector drawn from a small vocabulary of labelled nodes, orthogonal
     edges with a single arrowhead, dashed groups and small badges, laid out left to right.
     They are never images. Each carries a text alternative stating the flow in words rather
     than describing shapes, in the manner of "content is written to the store, which notifies
     the cache and the search index".
118. Customer logos are generated typographic tiles carrying the customer's name, deliberately
     typographic so they read as placeholders rather than as poorly reproduced marks. They
     are generated already monochrome, so no colour-removing filter treatment is applied to
     them anywhere. Author
     portraits are generated geometric avatars, deterministic from the person's name. **No
     binary asset ships**: no image file, no font file, no icon font, no sprite, no video.
     Product screenshots are replaced by live miniature renderings of the product's own
     components at reduced scale with generated content, so the marketing page cannot drift
     out of date with the product.
119. The documentation route is its own information architecture with its own chrome, sharing
     one design system and one component library. Search is its primary navigation: focusable
     from anywhere with a keyboard shortcut, searching headings and body, and showing the
     section path of each result so a reader knows where they would land. The version is in
     the address rather than in a cookie, so a link to documentation is a link to a specific
     version, and a reader on an older version sees a banner and a link to the current one.
     Every heading has a stable anchor that survives an edit. The feedback control asks one
     question and does not open a form. Every article declares its last-reviewed date, and one
     past a staleness threshold is flagged to its owner rather than to the reader. The query
     language reference, the mutation reference and the schema-type reference are **generated
     from the same definitions the product uses**, never written by hand, because hand-written
     reference material drifts within one release and the drift is invisible until somebody
     follows it and it does not work.
120. **The blog is a consumer of the product this site sells.** Its articles are documents in
     the `production` dataset of type `article`, its bodies are rich text rendered through the
     serializer contract, and it reads under the `published` perspective. A draft-only article
     such as `article-keys-and-arrays` never appears on it. The category filter lives in the
     address as `?category=`, so a filtered index is linkable and can be returned to, the back
     button restores both the filter and the scroll position, and changing the filter resets
     the paging. Paging is by cursor, never by offset. A build whose own blog does not use its
     own content model has no forcing function on the quality of that model.
121. **One not-found page, served with a `404` status and the document title
     `Page not found`.** Every unmatched path renders it and **no path renders the home page**.
     A path that does not exist rendering the home page with a success status is worse than an
     honest error: search engines index duplicates of the front page, a visitor who mistyped
     is told nothing, and genuinely broken links become undetectable because nothing ever
     reports a failure. The page carries the address that failed, a search control scoped to
     the documentation, and links to the three most likely destinations, and where the address
     differs from a real route by a small edit distance it suggests that route explicitly,
     because most wrong addresses on a documentation-heavy site are near-misses.
122. **Every internal link on every public route resolves.** No link on a public route points
     at an address that answers not-found, including every link in the footer, in the
     mega-menu and in the body of a documentation article.
123. The consent control is first-party. It sits at the modal tier rather than above
     everything, records a decision per category, never blocks first paint, and is reachable
     again afterwards from the footer, whose legal line carries `Terms`, `Privacy` and
     `Cookie settings`. **Refusing is exactly as easy as accepting**: one control each, the
     same size, the same prominence, and the decision survives a reload. No third-party script
     is used for it or for anything else.
124. `GET /sitemap.xml` lists every public route from the same manifest the footer renders,
     and `GET /robots.txt` names that sitemap with an absolute address built from
     `APP_PUBLIC_URL`.
125. `POST /api/leads` takes `work_email`, `name`, `company`, `team_size` and `message` from
     the demo request form at `/contact`. Every field is validated inline, the message names
     the field that is wrong, and nothing is written when anything is invalid. The form is
     refused for a submitter that behaves like a bot: an unattended decoy field that a person
     never sees is filled in, or the same form is submitted repeatedly in quick succession
     from one origin. A refused submission writes no lead and says plainly that it was
     refused.
126. Every public route carries its own title and description and no two public routes share
     either.

### What the product says when it has to tell the truth

127. These strings are requirements and may not be softened into generic error text. The
     editor's own actions read `Publish`, `Unpublish`, `Discard changes`, `Duplicate` and
     `Delete`. A required field reads `This field is required` and a blocked publish reads
     `Fix errors before publishing`. Presence beside a field reads `{name} is editing this
     field`. A resolved conflict reads
     `Someone else saved while you were editing. Your changes were kept.` A dropped local
     operation reads `We could not keep one change: {field} was deleted while you edited it.`
     A blocked publish for dependencies reads
     `This references {n} unpublished documents. Publish them together?` A blocked delete
     reads `{n} documents reference this. Remove those references first.` A read-only Studio
     reads `Editing is paused. Your work so far is saved.` Each is a moment where the product
     has to tell somebody the truth about their own content, and "something went wrong" is a
     failure to meet the requirement rather than a neutral alternative.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | The marketing home | none |
| `/products/{slug}` | One product surface from the mega-menu | none |
| `/solutions/{slug}` | One solution entry | none |
| `/resources/{slug}` | One resource entry | none |
| `/pricing` | Plans, with no purchase path | none |
| `/enterprise` | The buyer's route, carrying `BOOK A DEMO` | none |
| `/docs` | Documentation home | none |
| `/docs/{version}/{section}/{slug}` | One documentation article | none |
| `/blog` | The editorial index, filtered by `?category=` | none |
| `/blog/{slug}` | One article, rendered from rich text | none |
| `/contact` | The demo request form | none |
| `/privacy` | What the product stores and for how long | none |
| `/terms` | Terms | none |
| `/cookie-settings` | The cookie decision, revisitable | none |
| `/sitemap.xml` | Every public route | none |
| `/robots.txt` | Points at the sitemap | none |
| `/signin` | Email and password | none |
| `/studio` | The dataset chooser | any signed-in person |
| `/d/{dataset}/desk` | The document table | any signed-in person |
| `/d/{dataset}/desk/{type}` | The table filtered to one type | any signed-in person |
| `/d/{dataset}/doc/{id}` | The document editor | any signed-in person |
| `/d/{dataset}/doc/{id}/history` | The revision chain | any signed-in person |
| `/d/{dataset}/doc/{id}/published` | The publish confirmation | `editor` |
| `/d/{dataset}/vision` | The query playground and its cost report | `editor` or `administrator` |
| `/d/{dataset}/media` | The Media Library | any signed-in person |
| `/d/{dataset}/search` | Editor search | any signed-in person |
| `/d/{dataset}/releases` | Releases and schedules | `editor` |
| `/preview/{grant}` | A draft rendered under a preview grant | the grant only |
| `/project/schema` | The deployed schema and its drift count | `administrator` |
| `/project/datasets` | Datasets, visibility, copy and delete | `administrator` |
| `/project/tokens` | Tokens | `administrator` |
| `/project/grants` | Document-level grants | `administrator` |
| `/project/migrations` | The migration runner | `administrator` |
| `/project/webhooks` | Webhook configuration and the delivery record | `administrator` |
| `/project/audit` | The audit log | `administrator` |

**Entry and redirects.** An anonymous request for any `/d/...` or `/project/...` address
lands on `/signin` carrying where it was going, and returns there once signed in. Signing in
lands on `/studio`; choosing a dataset lands on `/d/{dataset}/desk`. Signing out returns to
`/signin`. A token that expires mid-action returns the person to `/signin` with the
destination preserved and whatever they had typed in the open editor still there. A
signed-in person opening a route their role cannot read is told plainly and offered the
routes they can reach, and the navigation never shows a group they hold nothing in. A person
opening a document outside their own department is told it was not found. Every unmatched
path renders the not-found page with a `404`.

**Journeys.**

1. *A developer evaluates.* Open `/`. Read the hero. Move to the install command pill with
   the keyboard and copy it: the command text flashes, returns, and a confirmation mark
   appears, overshoots and settles. Open the products menu from the top bar using the
   keyboard alone, move through its six groups, press Escape and find focus back on the
   trigger. Follow the rail entry `04 AUTOMATION AT SCALE` to its section.
2. *An editor publishes.* Sign in as `editor@example.com`. Choose `production`. Open
   `article-aurora-pipeline` from the document table. Embolden the middle of the word
   `pipeline` in the second paragraph and watch the paragraph become three spans with the
   first keeping its key. Press `Publish` and land on `/d/production/doc/article-aurora-pipeline/published`,
   which names the document, the revision it produced and the surfaces it now reaches. Open
   `/blog` in another tab and read the article there.
3. *A publish is refused.* Open `article-keys-and-arrays`, whose author exists only as a
   draft. Press `Publish`. Read `This references 1 unpublished documents. Publish them
   together?`, accept, and watch both documents publish in one transaction.
4. *Two people in one document.* `editor@example.com` and `contributor@example.com` both
   open `article-aurora-pipeline`. Each sees the other's marker in the header and beside the
   field. Each emboldens a different word in the same paragraph, and both marks survive. One
   saves while the other is mid-word: the typing survives and the person reads
   `Someone else saved while you were editing. Your changes were kept.`
5. *A contributor cannot publish.* Sign in as `contributor@example.com` and open the same
   article. The `Publish` control is absent, not present and refusing. Calling the publish
   endpoint directly with this session is denied by the server and the document is unchanged.
6. *A department boundary.* Sign in as `editor@example.com` and ask for
   `article-quarterly-letter`, which belongs to `marketing`. It is answered as not found, it
   is absent from the document table, it is absent from every query result, and it is absent
   from editor search.
7. *An image in two places.* Open `/d/production/media`. Change the crop on the use inside
   `article-aurora-pipeline`. Open `article-quarterly-letter` as `editor2@example.com` and
   find its own crop and its own alternative text unchanged. Request a square rendering of
   the same wide image whose hotspot sits near the left edge, and find the hotspot region
   fully in frame.
8. *A migration.* Sign in as `admin@example.com`. Open `/project/migrations`. Run a field
   rename against `production` and read `Dry run: 3 documents would change. Nothing has been
   written.` Type the dataset name again, apply it, then run it a second time and read that
   nothing changed. Open a migrated article and find every block and span key unchanged.
9. *A dangerous delete.* As `admin@example.com`, attempt to delete `author-marit` while
   `article-aurora-pipeline` references it, and read
   `1 documents reference this. Remove those references first.` with the article named.
   Attempt a delete by query with no filter and read the flat refusal. Open `/project/audit`
   and find the attempt recorded with its actor and its query text.
10. *A dataset goes public.* Open `/project/datasets`. Switch `staging` to public, type
    `staging` to confirm, and read the count of documents about to become world-readable
    beside `This dataset is public. Anyone can read its published content.` Then read, with
    no credentials at all, a published document in `staging`, and be refused a draft in the
    same dataset.

**States.** An empty document table says what would be listed there and names the action that
puts the first document in it. A filtered table that comes back with nothing lists each filter
still in force, each with its own control to lift it. A route that is still fetching holds the
space its rows will take, so the page does not jump when they land. A second fetch of a table
already on screen dims the rows in place and replaces them where they sit, keeping the scroll
position. Where part of a page fails, the rows that arrived stay and the range that did not
carries its own retry, rather than the whole route becoming an error. Search that cannot
answer says it is catching up rather than returning nothing. A control the viewer may not use is absent rather than present and refusing, since
a disabled control tells them something exists. Errors never crash a route: every one is an
inline message in the region that produced it, and the page keeps what was typed. When the
store cannot be written to, the Studio goes explicitly read-only with a banner naming the
reason and accepts no edit, rather than accepting edits and losing them.

## UI/UX notes

The north star is comprehension. Somebody arriving on the home route should understand
within one screen that this is a place to keep the words and pictures a company publishes,
stored as structured information rather than as web pages, so one body of content can feed a
website, an application, a shop screen and an email without being written four times. There
is no mood to invent beyond that, and inventing one would be the same defect as inventing a
colour.

Two registers share one system. The public half argues a case and may carry atmosphere, and
its subject is code, terminals and diagrams rather than photography. The Studio is
operational. It is read at speed by somebody who will open forty documents today, so it is
quiet, it is dense without being crowded, it repeats one arrangement rather than composing
each route, and it spends no space on anything that is not content or a control. The Studio
adds density, never a second visual language. Comprehension over atmosphere in the
Studio; space over dividers on the public half.

**Colour by role, never by palette entry.** Components ask for a role and never for a
numbered swatch: the page ground, the recessed surface, the primary text, the secondary
text, the tertiary text, the hairline, and a mirrored set for dark surfaces. There are three
levels of each and one inverse triad, and a dark section is served by the inverse set rather
than by a switch inside a component. Change what the secondary text means and it changes
everywhere at once.

The weight of the design sits on two colours: a near-black neutral and a near-white neutral.
This is a two-colour design with accents, not a colourful one, and the accents appear on a
handful of surfaces. The page ground is a near-white neutral and a recessed surface is a
near-white neutral one step deeper; the two must stay visibly separate without a dividing
rule. The dark surface is a near-black neutral and its own recessed step is a deep neutral.
Body text on light is a near-black neutral, secondary text is a deep neutral, and tertiary
text is a mid neutral; on dark they become a near-white neutral and a light neutral.
Hairlines are a near-white neutral on light and a deep neutral on dark.

The brand colour is a light, vivid red, and it is the only thing on a light page wearing it.
**On a dark surface the brand colour is not a lighter red, it is white**, and reproducing
that is what stops the dark sections reading as the light ones with the lamps turned down.
The second brand entry is a light, vivid blue and it is the focus colour and nothing else.
Four accents exist and each is declared in the wide gamut with an ordinary-range companion
alongside, so a display that can show the saturated colour gets it and every other display
gets a defined one rather than nothing: a soft cyan, a vivid green, a muted violet, and a
warm neutral that reads as a pale yellow. The failure colour is a vivid red that appears
nowhere except on something that has gone wrong. The copy confirmation flashes a mid, vivid
orange and returns to white, and that orange appears nowhere else in the product. The exact
shades are yours, so long as each role holds the relationship and the exclusivity above.

**Mode.** The product is designed light. The dark surfaces are sections inside that light
design, served by the inverse triad rather than by a second theme, so there is one designed
mode and no separate dark variant to build or to judge.

**Type.** No font binary ships. The two stacks are the platform user-interface sans and the
platform monospace, each named with its generic fallbacks, and the specification is complete
and correct in those alone. Seven sizes carry the whole product and no eighth is introduced.
Body is the size every other size is measured against, and it dominates the page by a wide
margin. Above it sit three: emphasised body, a single step up and no more; a subheading, half
again above body; and a section heading, roughly twice body, which is the widest jump in the
set. Below it sit three: the monospace interface size, which is the third most common text in
the product because navigation labels, detail labels and every code sample are set in it; a
label a step under that; and the smallest label, smaller again, which earns its target area
from padding rather than by growing. Where the seven land is yours, so long as each reads as a
distinct step at a glance and nothing but a section heading out-jumps body.

Two properties are the character, and a submission can be rejected on either. The weight that
carries a section heading and emphasised body is an intermediate one, between the regular and
the medium cut of the same face; rounding it to either is visible across every heading on the
page. And a heading's line height sits only just above its own size, closer than body's, so
large type is set tight and light rather than loose and heavy. That is what keeps a page full
of technical detail calm. Figures line up in a column wherever counts stack.

**Shape and depth.** Every button is a full capsule, and that single decision does more for
the product's character than any colour in it. Three other softenings exist and no more:
none at all, a small one for inline code and small controls, and a larger one for cards. The
product is almost flat: depth is carried by the ground pair and by hairlines rather than by
shadows, and the one hairline drawn as an inset shadow neither affects layout nor doubles
where two surfaces meet. Gradients are masks rather than decoration: a fade at each end of
the marquee so logos enter and leave through a soft edge rather than being clipped, a scrim
over the dark hero, and a notch cut out of each avatar so the next overlaps cleanly.

**Iconography.** Every symbol is geometry drawn in the page on one grid, stroked finely with
round joins and no fill, and the fineness of that stroke is why the interface reads as
precise and technical rather than soft and friendly. There is no icon font, no sprite and no
file. The wordmark is the product name set in the display face inside the lockup box the
layouts reserve, and it inherits its colour so it needs no dark variant. A label hidden from
view is clipped to nothing and left in the accessibility tree, never removed from the page
and never pushed off-screen where it can create a scroll.

**Chrome.** Three bars: a thin announcement strip whose height is a single stored value
every offset below it reads, so removing the strip does not break every anchor on the site;
the main bar; and the mega-menu panel that drops out of it. On the home route the main bar
sits over the dark hero with no ground of its own and its contents are white, and on every
light route it has a white ground and near-black contents. That is one component reading the
surface beneath it rather than two bars, which is why it never flickers between routes.
Hover does one of exactly three things and nothing else: a dark solid control steps one shade
along the neutral scale, a ghost control acquires the recessed ground, and the inverting
control swaps its foreground and background completely with its decorative pseudo-elements
following, because styling those separately leaves an underline or a ring the wrong colour
on hover. Every hover state is gated to devices with a pointer, so a touch never latches one
after a tap, and every hover affordance has an equivalent that does not need a pointer.

**Motion.** Two curves do the work and no others: the standard both-ends ease for anything
that moves both ways, and a decelerating one for anything that only arrives. Colour changes
take one short beat and movement takes a slightly longer one, and that is the whole system.
Nothing uses a different speed to feel special, and nothing declares a transition against
every property at once. The catalogue of named moments: a plain fade in, the most
used; the standard entrance, a fade with a short rise; a panel arriving with a slight tilt
away from the viewer, which is the only three-dimensional gesture in the product; its exit,
authored shallower than its entrance so leaving reads as quicker than arriving; a disclosure
whose height animates against its own measured height rather than a guess; a pulse and a
quieter pulse; a marquee whose doubled track slides by exactly half its own width, which is
what makes it seamless, at a speed derived from the content width rather than fixed, so
adding a logo does not speed it up; a text caret drawn as a blinking border; a loader that spins, and it rotates a full turn each cycle; and an
asymmetric blink, lit longer than it is dark, for anything live. The copy confirmation
overshoots, **holds at its largest for a moment**, and then settles: the hold is what makes
it read as a confirmation rather than a wobble, and an overshoot that returns immediately is
the wrong thing. Panels animate in and out including their appearance and disappearance, so
a closed panel is out of the layout and out of the tab order rather than sitting there at
zero opacity. Reduced motion is declared in **both** directions: movement is switched on for
people who have not asked for less rather than switched off for people who have, so anything
added later is quiet by default. Under a reduced preference the marquee holds, the pulse
holds, entrances resolve to their end state, and the copy confirmation appears without its
overshoot.

**Layout, scroll and density.** Five width boundaries in one notation, and going up: below
the smallest the actions stack full width and the announcement wraps; then the base layout;
then feature sections go two-column and begin alternating while the section rail turns from a
horizontal strip into a vertical one; then the mega-menu replaces the menu button and the
install command pill appears; then the container reaches its maximum and the scene
compositions gain their outer elements; then the outer padding widens and nothing else
changes. Scroll drives opacity and transform only and nothing scroll-driven touches layout:
a progress bar growing from its left edge, the marquee, a still scene crossfading against its
placeholder so the section looks finished before anything has loaded, and a diagram drawing
itself. On a narrow screen the decorative section fades are the effects that drop, because
the expensive ones belong on the capable device and doing it the other way round is the
common mistake. Stacking uses a named scale of six and no other value: behind, base, raised,
chrome, menu and modal, with nothing above the modal tier. In the Studio one table serves
every list route, with rows sitting tight enough that a full screen of documents is readable
at once, a sticky header, sortable columns that announce their sort state, the whole row as
the target, and explicit controls in a trailing overflow menu. Creating a document opens a
modal over the table rather than navigating away; publishing navigates to a confirmation
route of its own. State is never carried by colour alone: every badge carries a label and a
shape.

**Accessibility floors, which are contract rather than taste.** Body text meets a contrast
ratio of at least `4.5:1` against its ground and large text at least `3:1`; where the
tertiary text colour would carry meaning at the smallest label sizes it is raised to the
secondary one instead. Interactive targets are never smaller than `44px` in either
dimension, including the smallest label controls, which gain padding rather than a larger
type size. Full keyboard navigation reaches every control in visual order with a focus
indicator that is always visible, and on a capsule the indicator follows the capsule rather
than a rectangle. The mega-menu is the largest piece of work here: six groups of links that
open on pointer are almost always unusable without one, so it opens on focus, its entries are
in the tab order only while it is open, Escape closes it and returns focus to the trigger,
and each group is a labelled region. A skip link reading `Skip to content` is the first
focusable element on every route. A link that opens elsewhere announces it, using
`Opens in a new window`, `Opens an external website` or
`Opens an external website in a new window`. Every code block carries an accessible name
stating its language and its copy control announces success. Every content image carries
alternative text and a decorative one declares itself decorative. Every diagram carries a
text alternative stating the flow in words. The marquee is hidden from assistive technology
and the customer names appear as text elsewhere. Every icon-only control carries a name
describing the action rather than the shape, and meaning is never carried by colour alone
anywhere. The rich-text editor is operable and announceable, because a structured editor that
cannot be used with a screen reader excludes people from the job of editing rather than from
a feature.

**Responsive behaviour.** Nothing is hidden at any width. The narrow page is taller than the
wide one because it carries the same content in one column rather than a reduced set, and at
a narrow viewport nothing overflows sideways and every navigation target stays reachable.
The single exception is the install command pill, which is removed on a mobile screen
because there is no terminal on the device to paste it into, and it is replaced by nothing rather than by
a disabled control. The layout holds at every width between the named boundaries, including
below the smallest.

**What this must not look like.** A page tinted end to end in one hue family, with nothing
but that tint to tell one state from another, is the first failure. An ornament standing where
a diagram, a code sample or a document row should be is the second. A hero, a testimonial band
or a pricing composition inside the Studio is the third, and the mirror of it is the fourth:
the public half may breathe, the Studio may not. Nothing here is borrowed from a subject that
has nothing to do with publishing, code or the people who do both.

## Technical requirements

**Stack.** NestJS on Node 20, compiled to a production build at image build time, serving
both the rendered HTML and the JSON API from one process on one origin, with the API under
the `/api` prefix. Handlebars server templates produce every route: the server sends a
rendered document, so the browser receives the content of a route on first paint rather than
an empty shell it fills in afterwards, and a crawler and a link preview both see a route's
title, description and body without running script. Alpine.js runs over that server-rendered
markup and upgrades it in place; every interactive surface still works from a form submission
or a link when script has not run. PostgreSQL is the record for every document, revision,
grant, token, release, schedule, webhook, migration run and audit entry, reached with the
connection string in `DATABASE_URL`. MinIO is the record for every uploaded byte and every
derived rendering, reached at `STORAGE_ENDPOINT` with the bucket in `STORAGE_BUCKET` and the
credentials in `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Plain CSS with custom
properties, and no utility-class framework. Live updates and presence travel over a
long-lived HTTP stream on this same origin under `/api`.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
services available in this environment are PostgreSQL and MinIO, and reaching for anything
else is a contract violation. Both are **already running** and reachable at the environment
variables above; do not download, install, compile or start a copy of either.

**Configuration.** `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`,
`STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`,
`PREVIEW_GRANT_TTL_SEC` and `TRANSACTION_REPLAY_WINDOW_SEC` are read from the environment.
Never hardcode a host, a port or a duration. `PREVIEW_GRANT_TTL_SEC` is the lifetime of a
preview grant in seconds and its production value is `3600`.
`TRANSACTION_REPLAY_WINDOW_SEC` is how long a transaction id is remembered in seconds and its
production value is `300`. The application must read both; a duration compiled into the
application is a contract violation.

**The core never depends on the editor.** The layering is tokens, then primitives, then
compositions, then site routes, with the Studio shell depending on tokens and primitives
only and the platform core depending on nothing above it. Every capability the Studio offers
is reachable over the same public API a script uses, with no private path and no endpoint
that exists only for the editor. A core that reaches upward into the editor makes the
migration runner impossible, and the migration runner is the reason the product survives its
third year.

**Authorization is a layer, not a scatter of checks.** One decision is made per request from
the caller, the action, the resource and the dataset, and it is made before the request body
is validated, so an unauthorised caller cannot probe validation behaviour. The same decision
governs a route, a query result, a field in a response and a mutation. A document the caller
may not read is absent from the response rather than present and hidden. The client is never
an enforcement point: the Studio hides what a person cannot use because that is kinder, not
because it is a control. An authorization outcome is never cached, because a cached permit
outlives the revocation that should have ended it.

**The dataset boundary is a property of the query.** No read reaches storage without a
dataset predicate and a grant predicate, both derived from the route and the session rather
than from anything the client sends. A dataset identifier accepted from a request body is the
mechanism of every cross-dataset read defect in products of this shape.

**Concurrency, stated as what must be true.** Two clients patching different fields of one
document must both succeed. Two clients patching different items of one array, addressed by
key, must both succeed, and inserting an item at the head of the array while another patch is
in flight against a key must leave that patch on the item it named. One hundred simultaneous
increments of one counter leave it at exactly one hundred, with no lost update. Two
simultaneous publishes of one document produce exactly one published revision and the second
caller is told the document had already moved on. Two clients sending the same transaction id
produce exactly one effect. Two clients issuing structural operations against one array
converge on one order, and both clients end holding that same order. A refused mutation
leaves no partial state: no orphaned revision, no audit entry for work that did not happen,
and no event on the stream.

**One write, one announcement.** The new revision, its history entry and the record that
tells the rest of the system about it are written in one transaction. Announcing from
application code after the commit loses the notification on a crash, which here means a
document that changed while the search index never updated and the delivery record never
grew, and nothing detects that.

**Derived stores are rebuildable.** The documents, their revisions and the uploaded bytes are
the permanent record. The query indexes, the reverse reference index, the search index and
the derived-image cache are worked out from those and can be rebuilt at any time, which is
what makes an index change or a relevance change safe. Deleting the search index and
rebuilding it must return identical query results.

**Caching and invalidation.** A response is cacheable when its perspective needs no
credentials and its query contains no `now()`, and both conditions are checked and reported
so a caller can see why a query is uncacheable rather than guessing. The key is the query
text, its parameters, the dataset, the perspective and the schema version. **Invalidation is
by tag: a query records every document type and id it touched, including the ones it reached
by dereference, and a mutation purges the tags it affects.** Publishing one article
invalidates every listing that included it and every page that dereferenced it; a build
tracking only the document itself leaves every listing stale, which presents to the customer
as pressing publish and not seeing the article on the front page. A staleness ceiling of
`60s` applies even without a purge, so a missed purge self-heals within a minute.

**The consistency model, stated rather than hidden.** A writer reading their own write gets
read-your-writes, always. The live query interface is strongly consistent. A cached read is
eventually consistent, bounded by the staleness ceiling below. Grant evaluation is
read-after-write and never reads anything but the authoritative copy, because a stale query
result is an inconvenience and a stale grant serves a document to somebody who lost access.
Reads spanning two documents are not taken against one instant, and that is stated rather
than hidden: a query joining two documents through a dereference may observe the referenced
document at a newer revision than the referring one. Where a consumer needs a consistent
pair it fetches both in one query, which is evaluated at a single point in time.

**Backpressure.** Every queue in this application has a stated bound and a stated behaviour
at that bound. The permitted behaviours are to shed a cache refresh, to refuse with a
retryable error, or to close a listener and let it resume. Never to grow without limit, and
never to drop a mutation or an event.

**Degradation, in order.** Query cost reporting is sampled first, then search reports itself
as rebuilding, then delivery records queue and are written late but never dropped, then new
listener connections are refused while existing ones continue, then cached reads are served
stale beyond the ceiling and labelled, then the Studio goes read-only with a banner naming
the reason, then mutations are refused with a retryable error, and published reads are the
last thing to go, because the reader's site is somebody else's business. At the read-only
rung the Studio accepts no edit and says so; it does not silently fail to save while somebody
keeps typing.

**The audit log.** Append-only and hash-chained per project, each entry carrying `id`,
`actor`, `action`, `target`, `dataset`, `params_digest`, `result`, `prev_hash` and `hash`,
written through a single writer so the predecessor is unambiguous and the chain verifies end
to end after a hundred concurrent audited actions. Recorded without exception: token creation
and revocation, grant changes, dataset visibility changes, dataset copies and deletions,
schema deployments, migration runs, and every mutation by query.

**What is measured, and who sees it.** Query latency and cost per query shape, the count of
queries refused for exceeding a bound, mutation latency and the revision-conflict rate,
listener connection and reconnect counts, cache hit rate and purge latency, delivery record
depth, search index lag, schema drift per dataset, migration progress, and asset
transformation failures. The query cost, the refusal count, the search lag, the schema drift
and the migration progress are surfaced **to the customer** rather than kept internal,
because customers write their own queries and a platform whose customers cannot see why
their queries are slow will be blamed for it, correctly. The revision-conflict rate is a maintained conflict-rate metric and an
alert rather than a chart, because a rising rate on one document type means an automated
writer is fighting a person and the person is quietly losing work every time.

**Logging discipline.** Log lines are built from a named list of fields and go to standard
output. One line per request carries a request identifier, the route, the status, the
latency, the dataset, the principal and the decision outcome, and the identifier is returned
on every response including every error. **Never logged: document content, asset bytes, token
values, or the values of query parameters.** Query text is logged with parameters replaced by
their names, which is what makes parameterization an operational benefit as well as a
security one.

**Transport and response hygiene.** No state-changing request is reachable by a safe method,
anywhere. A request whose content type does not match its body is rejected rather than
sniffed. A parameter an endpoint does not recognise is rejected rather than ignored, because
ignoring it is friendlier for one afternoon and then somebody ships an integration believing
it turned a setting on. No credential, token or secret value appears in anything the browser
downloads.

**Outbound safety.** This application makes no outbound network call at runtime. A webhook
address is validated at configuration time and is never fetched.

**Performance budgets.** The first-view inventory of scripts, styles and rendered images
stays inside these figures. First contentful paint under `1.5s`, the largest contentful element
under `2.5s`, interaction latency at the 75th percentile under `200ms`, cumulative layout
shift under `0.05`, no single main-thread task over `50ms`, home-page script on first view
under `250KB` compressed, total transfer on first view under `1MB`, zero third-party
requests, zero font bytes, and zero bytes of syntax highlighting shipped to the browser. A
documentation article paints under `1s` because it is static, and its search index ships with
the page and answers under `100ms`. The hero's still scene loads behind its placeholder. The
marquee animates one property and declares that it will. Panels in the mega-menu are not
rendered until the menu is first opened.

## Data model

Eighteen tables. All timestamps are UTC. Every identifier a client supplies is a string.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture
data, not a secret. Hash it as normal; the exact literal must work at login, and it must be
written into `/app/USER_README.md` alongside each account so a grader can sign in.

### person
`id`, `email` unique, `display_name`, `password_hash`, `role`, `department` nullable,
`locale`, `created_at`. `role` is `administrator`, `editor`, `contributor` or `viewer`.
`department` is `engineering` or `marketing`, and is null for an `administrator` and a
`viewer`.

### dataset
`id` which is the name, `visibility`, `document_count`, `asset_count`, `deleted_at`
nullable, `purge_after` nullable, `created_at`. `visibility` is `private` or `public` and a
new dataset is `private`. `purge_after` is `deleted_at` plus `168h`, and the dataset is
recoverable until then. `document_count` and `asset_count` are **derived on read** from the
document and asset rows, never stored running totals a second code path could forget.

### document
`dataset`, `_id`, `_type`, `_rev`, `_createdAt`, `_updatedAt`, `department`, and `body`
carrying the schema-shaped fields. Unique on the dataset and the identifier together. A
draft is an ordinary row whose `_id` is the published `_id` prefixed with `drafts.`, so the
whole draft space is addressable by one grant rule and a published document with no draft has
no row rather than a null column. Every object inside any array in `body` carries a `_key`
that is unique within that array.

### revision
`id`, `dataset`, `document_id`, `_rev`, `previous_rev` nullable, `transaction_id`,
`actor_id`, `action`, `body`, `created_at`. Append-only. `previous_rev` chains to the row
before it, and the chain of a document and of its draft is one chain. A revision row survives
its document row being deleted, which is what makes a deletion recoverable.

### transaction
`id` supplied by the client, `dataset`, `actor_id`, `results`, `created_at`. Unique on the
identifier, which is the property that makes a replay within `TRANSACTION_REPLAY_WINDOW_SEC`
return the original `results` and apply nothing.

### reference_edge
`dataset`, `from_id`, `to_id`, `path`, `strength`. `strength` is `strong` or `weak`.
Maintained on every write, and it is what both the `references()` function and the delete
refusal read. Derived and rebuildable from `document`.

### asset
`_id` in the form `image-<sha256>-<width>x<height>-<ext>`, `dataset`, `object_key`,
`original_filename`, `size_bytes`, `mime_type`, `width`, `height`, `palette`,
`blur_placeholder`, `orientation`, `location` nullable, `created_at`. Unique on the dataset
and the identifier together, which is what makes deduplication a property of the identifier.
The crop, the hotspot and the alternative text are **not** here: they belong to each use and
live inside the document that holds the reference.

### grant
`id`, `role`, `dataset`, `filter`, `created_at`. `filter` is a query filter evaluated on the
service on every read and every write.

### token
`id`, `label`, `scope`, `dataset` nullable, `secret_hash`, `prefix`, `last_used_at`
nullable, `last_used_address_prefix` nullable, `expires_at` nullable, `revoked_at` nullable,
`created_at`. `scope` is `read` or `write`. The secret value itself is never stored and never
returned after creation.

### preview_grant
`id`, `dataset`, `document_id`, `issued_to`, `expires_at`, `revoked_at` nullable.
`expires_at` is the issue time plus `PREVIEW_GRANT_TTL_SEC`.

### release
`id`, `dataset`, `title`, `state`, `document_ids`, `scheduled_at` nullable, `zone` nullable,
`published_at` nullable, `archived_at` nullable. `state` is `open`, `scheduled`, `published`,
`blocked` or `archived`.

### schedule
`id`, `dataset`, `document_id`, `instant`, `zone`, `state`, `failure_reason` nullable.
`state` is `pending`, `executed`, `failed` or `cancelled`. `zone` holds a zone name, never a
fixed offset. Unique on the dataset, the document and the instant together, which is what
makes execution idempotent.

### webhook
`id`, `name`, `url`, `dataset`, `trigger`, `filter`, `projection`, `headers`, `secret`,
`enabled`, `api_version`, `created_at`. `trigger` is `create`, `update` or `delete`.

### webhook_delivery
`id`, `webhook_id`, `transaction_id`, `document_ids`, `truncated`, `coalesced_from`,
`created_at`. A record of what would be sent. Nothing is ever fetched.

### migration_run
`id`, `name`, `dataset`, `mode`, `phase`, `cursor`, `affected`, `sample`, `actor_id`,
`started_at`, `finished_at` nullable, `result`. `mode` is `dry_run` or `apply` and the
default is `dry_run`. `phase` is `expand`, `migrate` or `contract`. `cursor` is what makes a
run resumable.

### search_document
`dataset`, `document_id`, `tokens`, `boosts`, `state`, `indexed_at`. `state` is `current`,
`stale` or `rebuilding`. Derived and rebuildable from `document`.

### audit_entry
`id`, `actor`, `action`, `target`, `dataset`, `params_digest`, `result`, `prev_hash`,
`hash`, `created_at`. Append-only and hash-chained, written through a single writer.

### lead
`id`, `work_email`, `name`, `company`, `team_size`, `message`, `created_at`.

### consent_decision
`id`, `visitor_token`, `analytics`, `preferences`, `decided_at`.

### Invariants

A document's `_rev` changes on every mutation, and no two revisions of one document share
one. Publishing writes the published row and removes the draft row together, so no observer
ever sees a state where neither exists. A delete of a document that any `reference_edge`
points at with `strength` of `strong` is refused at commit time. `audit_entry.prev_hash`
equals the previous entry's `hash`, and the chain verifies end to end. The search index, the
reference edges and the derived image cache are reconstructible from the documents, the
revisions and the assets alone.

### Seed data

Two datasets, `production` and `staging`, both `private`.

Five people, exactly as named in `## User roles`, each with the corpus password.

Eight documents in `production`:

| `_id` | `_type` | `department` | State |
|---|---|---|---|
| `article-aurora-pipeline` | `article` | `engineering` | `Published with unpublished edits` |
| `article-keys-and-arrays` | `article` | `engineering` | `Not published` |
| `article-migrating-schemas` | `article` | `engineering` | `Published` |
| `article-retired-notes` | `article` | `engineering` | `Draft`, taken down and kept |
| `article-editorial-standards` | `article` | `engineering` | `Published with unpublished edits` |
| `article-quarterly-letter` | `article` | `marketing` | `Published` |
| `author-marit` | `author` | `engineering` | `Published` |
| `author-tomas` | `author` | `marketing` | `Not published` |

`article-aurora-pipeline` carries a body of five blocks: two `normal` paragraphs, a run of
three consecutive `bullet` blocks, and an image block. Its second paragraph contains the word
`pipeline` whose middle is already emboldened, so it is stored as three spans and is the
seeded case for a search token that crosses a span boundary. It holds a `strong` reference to
`author-marit` and a `weak` reference to `article-retired-notes`.

`article-keys-and-arrays` holds a `strong` reference to `author-tomas`, which exists only as
a draft, so the refused publish is seeded rather than constructed.

`article-editorial-standards` is the working copy the walk-through journeys edit, save and
publish. It carries a title, a summary, a tag list of three keyed items and a body of two
paragraphs, and nothing else in the seed depends on its state.

One asset is seeded, `image-9f2ae1c4d0b7-1600x900-png`, stored at the object key
`assets/production/9f2ae1c4d0b7.png`, and it is used twice: inside
`article-aurora-pipeline` with one crop and the alternative text
`A layered diagram of a content pipeline`, and inside `article-quarterly-letter` with a
different crop and the alternative text `The quarterly figures, drawn as a bar chart`. Its
hotspot sits near the left edge, so a square rendering of it is the seeded case for the
region that must survive.

Grants: `editor` and `contributor` each hold a grant whose filter restricts them to documents
whose `department` equals their own. `viewer` holds a grant restricting them to published
documents.

Three blog categories exist: `guide`, `engineering` and `product`. Documentation is seeded
under two versions, `v1` which is current and `v0` which shows an older-version banner.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

Everything here is appearance. Where a sentence also carries behaviour, the behaviour is
stated precisely and the appearance is stated as intent.

### The token layer

Two layers exist and components consume only the second. Underneath is a palette of ramps
nobody names outside the token sheet; above it is a semantic layer naming roles, and the
whole system is a `base`, `dim` and `faint` triad for grounds and for text, mirrored by an
`inverse` triad for dark surfaces. A component never names a palette entry. It names a role,
and a dark section is served by the inverse set rather than by a theme switch inside the
component. That is what lets the meaning of the secondary text change in one place and change
everywhere.

Both light and dark values are declared for every ground role, and the brand entry is the
one deliberate asymmetry: light gets the vivid red, dark gets white.

### Colour, continued

Beyond the roles named in `## UI/UX notes` the product introduces no new colour. The Studio
adds semantic aliases over the same roles and nothing else: a published badge takes the
vivid green, a draft badge the mid neutral, a blocked or failed state the failure red, an
in-progress state the warm neutral that reads as pale yellow, a selected row the recessed
ground, and a row separator the faintest hairline. The soft cyan and the muted violet appear
only inside diagrams and code tokens, at most three token roles to a diagram. A component
that hard-codes a value cannot be re-themed, so colour is always applied through its role.

### Typography, in full

Two families and no font file. The interface family is the platform user-interface sans with
its generic fallbacks, and code, tabular figures and every navigation label are set in the
platform monospace with its generic fallbacks. Naming a family is not an asset dependency;
shipping one is.

The rendered scale, described rather than pinned: body is the dominant size in the product by
a wide margin; a subheading sits half again above it at a line height barely above its own
size; the monospace interface size sits below body and carries two variants of its own, a
denser one inside a code block and a tighter one for a small monospace label; a label sits a
step under the monospace size; the smallest label is smaller again and reaches its target area
through padding; a section heading is roughly twice body and takes the intermediate weight;
and emphasised body is one step above body at that same weight. Inline code is set a step
below the body around it, with its letter spacing tightened just enough that a run of
identifiers does not read looser than the sentence holding it. The seven steps are the
builder's to place, so long as they stay distinct and hold those relations.

### Radius, depth and masks

Four softenings and no others: none, the small one carried by inline code and small controls,
the card one, and the full capsule that every button wears. The capsule is the single most
characteristic decision in the system and it is used everywhere a button appears, including
the two very large closing actions, which are the same component at a larger size rather than
a bespoke element, which is what keeps their hover, focus and unavailable behaviour identical
to every other button.

Depth is carried by the ground pair and by hairlines. One shadow exists as a device rather
than as depth: an inset hairline drawn as a shadow rather than as a border, which does not
affect layout and does not double where two surfaces meet. Gradients are masks: a bottom
fade, a horizontal fade at each end of the marquee, a scrim over the dark hero, and a radial
notch cut out of each avatar so the next one overlaps cleanly, which works on any background
because it is a mask rather than a border.

### Iconography, in full

Every icon is inline geometry on one grid, stroked finely with round joins and no fill, and
it inherits its colour rather than carrying one. The set the product authors: chevrons in
four directions, close, check, copy, external link, search, menu, dot, plus, minus, filter,
calendar, clock, user, lock, warning, info, code, terminal, document, folder, image, link,
arrow-right, and one tile per product entry in the mega-menu. Two are worth drawing
carefully: the external-link mark is a box left open at its upper right so the arrow can pass
through the gap without a mask, and the close mark is two crossed lines rather than a filled
path so it stays a hairline at every size. There is no icon font, and none is introduced.

The wordmark is the product name set in the display face inside the lockup box every layout
reserves, so a layout that allowed for a mark still balances, and it inherits colour so it
needs no dark variant.

### The chrome, in full

The announcement strip carries one sentence in the monospace face with a trailing arrow, and
its height is a single stored value that the sticky chrome and every in-page anchor offset
read, so removing the strip does not break every anchor on the site the day it is removed.

The main bar carries the wordmark, the seven entries and the account cluster set apart on the
right. The mega-menu's six groups carry entry titles in the sans at body size and group
labels in the monospace at the interface size, one promoted item per group with its own image
and its own action, and a `New` badge on any entry that has just arrived. It opens on hover
and on focus, and on a tap for a device with no pointer. It closes on Escape, on a click
outside, and when focus leaves. The bar acquires a ground the moment a menu opens, so the
panel and the bar read as one surface rather than two.

The footer repeats the group structure of the mega-menu as a link grid, with a theme control,
the social row, and a legal line carrying `Terms`, `Privacy` and `Cookie settings`.

### The code and diagram surface

This product's illustration layer is code, terminal output and architecture diagrams rather
than photography. A code block sits on the recessed ground on light and on the inverse pair
on dark, at the monospace interface size, with a tab strip above it when one sample exists in
more than one language and the choice remembered for that visitor. A block fades in once it
has been tokenized, and it is tokenized when the site is built rather than in the browser.
The tab strip above such a block is a segmented control whose indicator width animates
linearly from the old tab to the new one, and that width animation is the one linear
movement in the product.

A diagram is drawn from four shapes: a labelled node with the card softening, an orthogonal
edge with a single arrowhead, a dashed group with a label, and a small badge on a node. Its
layout is layered left to right on a grid with edges routed orthogonally, its type is the
body face and never smaller than the smallest label size, and it uses at most three colour
roles. Every diagram is selectable, translatable and searchable because it is drawn in the
page, and every one carries a text alternative stating the flow in words.

### The home route, in full

The hero's headline sits at the page-heading scale, two lines wide on a large screen and
three on a phone, white on the near-black ground, with a body line beneath at the largest
body size and the three actions all wearing the capsule. Its ground is a generated still
scene and its placeholder, which are a poster crossfade rather than a parallax: the
placeholder holds until the scene is ready and the two cross-fade. Both ignore the pointer,
so neither intercepts a click, and nothing on any route pins, parallaxes or moves sideways
as the page scrolls. The chrome sits over it with no ground of its own.

The customer marquee runs on the accent ground with its track doubled and masked at both
edges, pausing on hover and under a reduced-motion preference, hidden from assistive
technology, with the customer names present as text elsewhere on the route.

Each feature section carries a heading at the section-heading size and intermediate weight, a
body paragraph, a four-item list, and an outline action naming the product surface set in
monospace uppercase at the interface size. That outline monospace action is the product's
third button variant and its "go deeper" affordance, distinct from both the solid primary and
the ghost.

The developer band is a centred heading reading `Less talk, more code` above three columns,
each with a title, a sentence and a row of tool marks, and the first column repeats the
copyable install command.

The closing actions are two of the same button component at an unusually large size, side by
side, one in the brand and one in the near-black, together spanning most of the page width.

On a phone the announcement wraps to two lines, the chrome reduces to the wordmark, one
action and a menu control, the hero headline runs to three lines with its actions stacked
full width, the marquee continues at the same derived speed, and the section rail becomes a
horizontal strip above its sections.

### Stacking

A named scale of six values and no other: behind, base, raised, chrome, menu and modal. The
consent control sits at the modal tier and not above everything, because a control that
outranks every other layer in the document is a control nothing else can ever sit in front of.

### The Studio shell

A fixed top bar carrying the wordmark, the dataset switcher, editor search and the profile.
The dataset switcher never collapses and is never behind a menu at any width, and it states
the dataset's visibility wherever the dataset is named. A public dataset carries a band across
the full width of the top bar reading that anyone can read its published content; a private
dataset carries no band, and the absence of the band is the signal. Switching dataset is a
full navigation rather than a state swap, because a residual response from one dataset
rendered under another dataset's name is the worst thing this product can do.

The document editor is a single column of fields at a capped measure with the document's state
badge, its actions and its presence markers in a header that stays in place while the fields
scroll. A field being edited by somebody else carries their marker beside it; a field changed
remotely while it is not being edited applies with a brief highlight.

## Constraints

- No document in one department is ever visible to a person in another department, at any
  address, under any perspective, in either dataset.
- This is a zero-asset build: every asset class the product would otherwise load is a
  generated substitution instead. No binary asset ships or is fetched: no image file, no font
  file, no icon font, no sprite and no video. There is no hero video, no adaptive video player and no poster image file;
  the hero's ground is a generated inline vector scene. No external address and no asset file
  is referenced anywhere in the build.
- No third-party script of any kind: no consent vendor, no analytics vendor, no tag manager,
  no syntax highlighter shipped to the browser, and no font service. Third-party requests are
  zero.
- No outbound network call at runtime. Webhook endpoints are configured, validated and their
  deliveries recorded and coalesced; nothing is ever sent to one, so there is no delivery
  attempt, no signature verification against a raw body, no retry schedule, no dead letter
  retained for re-driving by hand with its payload, and no replay.
- No background job, no cron, no scheduler, no worker, no message queue and no outbox relay
  process. A schedule or a release whose instant has passed executes the next time it is read
  or acted upon.
- No read replica, no region selection, no data residency, no edge cache and no delivery
  network. No backup, no point-in-time restore, no restore drill and no scheduled restore
  job.
- No federated identity, no second factor, no recovery codes, no password reset, no signup
  and no self-service account creation.
- No billing, no plans, no quotas, no usage metering and no per-plan limits. The bounds in
  this brief are fixed, not purchased.
- No page-view analytics and no visitor-level tracking beyond the cookie decision itself.
- No right-to-left rendering, no locale switching in the public chrome, and no translation
  workflow beyond the field-level and document-level patterns described above.
- No compliance attestation badge and no availability claim appears anywhere on the public
  half. Those are claims about audits an operator has or has not had, and reproducing one
  would be a false statement rather than a borrowing. Every marketing claim on the site is
  either one this build can support or is absent.
- No native application, no edge function, and no second application framework beyond the one
  named in `## Technical requirements`.
- No field-level security, and no interface that implies it.
- The product must stay responsive with roughly two hundred thousand documents and two
  million revisions in one dataset.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `200` |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `person` |
| `GET /api/me` | none | the person with `role`, `department` and reachable datasets |
| `GET /api/datasets` | none | a top-level JSON array of datasets |
| `POST /api/data/query/{dataset}` | `query`, `params`, `perspective` | `result` beside `cost` |
| `POST /api/data/mutate/{dataset}` | `transactionId`, `mutations`, `dryRun`, `confirm` | `transactionId` and one result per mutation |
| `GET /api/data/doc/{dataset}/{id}` | `perspective` | one document |
| `GET /api/data/history/{dataset}/{id}` | `cursor` | a top-level JSON array of revisions |
| `POST /api/data/publish/{dataset}/{id}` | `alsoPublish` optional | the published document and its `_rev` |
| `POST /api/data/unpublish/{dataset}/{id}` | none | the draft the unpublish created |
| `GET /api/data/listen/{dataset}` | `query`, `lastEventId` | a stream of `welcome` then `mutation` events |
| `POST /api/data/preview-grants/{dataset}/{id}` | none | the grant and its `expires_at` |
| `POST /api/assets/{dataset}` | the file | the created asset document |
| `GET /api/assets/{dataset}/{asset_id}` | `w`, `h`, `fit`, `fm`, `q`, `rect`, `blur`, `sharp`, `sat`, `auto` | the rendered image |
| `GET /api/search/{dataset}` | `q`, `type`, `perspective`, `cursor` | matches, their `total` marked approximate, and the index `state` |
| `GET /api/presence/{dataset}/{id}` | none | a stream of presence events |
| `POST /api/presence/{dataset}/{id}` | `field`, `cursor` | accepted |
| `GET /api/project/schema` | none | the deployed schema and its drift count per dataset |
| `POST /api/project/schema` | the schema | the deployed version |
| `POST /api/project/datasets` | `id`, `visibility` | the created dataset |
| `POST /api/project/datasets/{dataset}/visibility` | `visibility`, `confirm_name` | the dataset and the count made readable |
| `POST /api/project/datasets/{dataset}/copy` | `target`, `include_drafts`, `include_assets`, `include_history`, `mode`, `confirm_name` | the copy result and its counts |
| `DELETE /api/project/datasets/{dataset}` | `confirm_name` | the dataset with its `purge_after` |
| `GET /api/project/tokens` | none | a top-level JSON array, never carrying a secret |
| `POST /api/project/tokens` | `label`, `scope`, `dataset`, `expires_at` | the token, carrying its secret exactly once |
| `POST /api/project/tokens/{id}/revoke` | none | the revoked token |
| `GET /api/project/grants` | none | a top-level JSON array of grants |
| `POST /api/project/grants` | `role`, `dataset`, `filter` | the created grant |
| `GET /api/project/webhooks` | `dataset` | a top-level JSON array of webhooks |
| `POST /api/project/webhooks` | `name`, `url`, `dataset`, `trigger`, `filter`, `projection` | the created webhook |
| `GET /api/project/webhook-deliveries` | `webhook_id`, `cursor` | a top-level JSON array of delivery records |
| `POST /api/project/migrations` | `name`, `dataset`, `mode`, `phase`, `cursor`, `confirm_name` | the run with its `affected` count and its `sample` |
| `GET /api/project/migrations` | `cursor` | a top-level JSON array of runs |
| `GET /api/project/audit` | `actor`, `action`, `cursor` | a top-level JSON array of entries with their hashes |
| `POST /api/releases/{dataset}` | `title`, `document_ids`, `scheduled_at`, `zone` | the created release |
| `POST /api/releases/{dataset}/{id}/publish` | none | the release, now `published` |
| `POST /api/schedules/{dataset}` | `document_id`, `instant`, `zone` | the created schedule |
| `GET /api/schedules/{dataset}` | `state` | a top-level JSON array of schedules |
| `POST /api/leads` | `work_email`, `name`, `company`, `team_size`, `message` | the created lead |

Field names are exact. A list endpoint returns a top-level JSON array. A successful call
returns the named resource or shape. An invalid, unauthenticated or unauthorized call is
rejected as a client error, never as a server error and never as a silent success, and
carries a body of the shape `{"error": {"code", "message", "path", "request_id"}}` where
`code` is the stable machine-readable string this brief pins and `message` is for a person to
read. Bearer auth is required on everything under `/api/data`, `/api/assets`,
`/api/presence`, `/api/search`, `/api/project`, `/api/releases`, `/api/schedules` and on
`/api/me`, with the single exception of a read under the `published` perspective in a dataset
whose visibility is `public`.

**No mocks.** PostgreSQL is the fact for every document, revision, grant, token and audit
entry, and MinIO is the fact for every uploaded byte. An in-memory array of documents, a
revision chain recomputed on read rather than stored, image bytes on the app container's
filesystem or base64 inside a document, a search index that is a scan of an in-process
object, a seed that lives in a JavaScript file rather than in the database, or an audit hash
chain computed at display time are each a contract violation however good the interface
looks. The named provider is the fact - the app's UI and its own tables can only reflect what
lives in the provider, never substitute for it.

## Definition of done

An editor opens an article, emboldens the middle of a word, publishes it in one action, and
sees it on the public blog moments later while a colleague editing the same paragraph keeps
every character they typed. An article whose author has never been published cannot be
published until both go out together, and an author that articles point at cannot be deleted
until they do not. A visitor with no credentials reads published articles and never a draft,
and an editor in one department never sees another department's work at any address. The
uploaded picture lives in the object store, is cropped differently in each place it appears,
and keeps the face in frame when it is asked for as a square.
