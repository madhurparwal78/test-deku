# Mote Interactive Animation Studio

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, find a published
interactive graphic in the marketplace, sign up for a seat, and open a document in the
workspace without hitting an error page. A different stranger, signed out, must NOT be able to
reach the bytes of a document that has never been published, by any means. The document bytes
must live in the object store under the key scheme this brief pins; a copy on the app's own
disk or a row in the app's own tables does not count.

## Overview

Mote is a browser workspace where a team builds interactive graphics and ships them into live
applications. A workspace holds folders, a folder holds documents, a document carries
artboards, one named animation and a state machine. Every edit is an operation on an
append-only log, and a revision is materialised from it as a content addressed binary.

Publishing is not saving: a publish freezes a revision into an immutable build and points a
named channel at it, so a rollback is one action. A marketplace shows published work to anybody
and unpublished work to nobody, which is the hard part: it reads the same database as the
workspace. Not a marketing site, a desktop app or a billing product.

## User roles

Two roles. Every seeded account uses the password `deku-demo-pw-2026`.

| Role | Can do |
|---|---|
| `editor` | read every folder and document here; create folders and documents; append operations; materialise and restore revisions; publish, roll back and unpublish; invite and change a role. Holds a seat. |
| `viewer` | read only documents granted to them, and only folders on the path to one. **Cannot create, edit, materialise, restore, publish, roll back, unpublish, invite or change a role**, and **cannot learn any folder name off that path.** No seat. |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI
is not authorization: a direct API call from a `viewer` session to an `editor`-only endpoint
must be rejected by the server (an unauthorized request is denied, not served), leaving the
protected state unchanged.

Signup is open and a new account gets its own empty workspace. In `Northlight Studio`,
`editor@example.com`, `editor2@example.com` and `editor3@example.com` are `editor`, and
`viewer@example.com` is a `viewer` on `Broadcast` alone.

## Core features

**The operation log.** Each edit is one operation carrying a client-minted `op_id`.

1. The service assigns `seq`, strictly increasing per document; two clients appending at once
   get two different values and neither is lost.
2. Two operations on different properties of one node both apply, outcome `applied`; two on
   one property resolve to the higher `seq`, the earlier recorded `superseded`.
3. An operation against a node an earlier one deleted is recorded `discarded`, the response
   naming who deleted it rather than dropping it silently.
4. Re-posting a held `op_id` returns the original `seq` and writes no second row.

**Publish and rollback.**

1. A publish freezes one revision into an immutable build, renders a poster, points the named
   channel at it and creates a listing. No build column changes after.
2. A channel points at one current build, or none. **Two simultaneous publishes of one document
   to one channel must not both become current: exactly one wins, the other is rejected, and
   the channel keeps one build with no orphan. This must hold at the database level, not only
   in application logic.**
3. A rollback repoints the channel at an earlier build and reaches every reader within ten
   seconds. Unpublishing removes delivery and the listing, never the build.

**The runtime address and the draft.**

1. `GET /api/runtime/{slug}` needs no credential and serves the exact bytes of its channel's
   current build. A channel with no current build is not served.
2. `Menu Transition` has never been published. Its revision bytes are in the object store and
   no unauthenticated route reaches them.
3. `GET /api/listings` never returns an unpublished document, in any ordering, for any search
   term, signed in or out.

**Seats.** An `editor` holds a seat; a `viewer` and a pending invitation do not, and the count
is derived from the grants on read. `Northlight Studio` caps seats at `3` and holds three.
**Accepting an invitation over the cap is refused: it is held at `seat_blocked`, no member row
is written, and the derived count does not move.** A `viewer` invitation still succeeds.

**Launch surface.**

1. A privacy page is reachable from every footer and says what the product stores.
2. A first-time visitor is asked once about non-essential cookies; the answer survives a reload.
3. Every form rejects invalid input inline, names the field, and writes nothing.
4. Each page view is recorded with its route and timestamp, readable by an `editor`.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/m` | the marketplace grid and search | none |
| `/m/<handle>/<slug>` | one listing, playing | none |
| `/signup` | open signup | none |
| `/login` | sign in | none |
| `/w` | redirects to a readable folder | both |
| `/w/files/<folder_id>` | folders, documents, detail | both |
| `/w/documents/new` | create a document | editor |
| `/w/d/<document_id>` | artboards, timeline, states | both |
| `/w/d/<document_id>/history` | revisions, restore | both |
| `/w/d/<document_id>/publish` | publish, rollback, unpublish | editor |
| `/w/members` | members, roles, seats, invites | editor |

**Entry and redirects.** A signed-out request for a `/w` route goes to `/login`, then to the
route asked for; with no destination it lands on `/w`, which redirects to the first readable
folder. Sign-out returns to `/m`. A token expiring mid-action keeps the typed values, and a
`viewer` reaching an `editor` route is refused, nothing changed.

**Journeys.**

1. Open `/m`, search `menu`, get nothing, open `/m/rae/loader-ring`, sign up, land on an empty
   workspace.
2. Sign in as `editor@example.com`, open `/w/files/1`, follow the create control to
   `/w/documents/new` and name a document `Hover Chip` in `Product UI`.
3. Two editors change one property of one node on `/w/d/1`; both end on the higher `seq` value
   and the loser is told who won.
4. On `/w/d/1/publish` publish the head revision to `loader-ring`, read the bytes from
   `/api/runtime/loader-ring` signed out, roll back, see the old bytes in ten seconds.
5. On `/w/members` invite `editor4@example.com` as an `editor` and accept: refused, held at
   `seat_blocked`, seats still `3`.

**States.** Every list has an empty state naming what to do next and every route has a loading
state. A refusal raises an inline banner naming what was refused and why; no page becomes an
error page. A document shows `draft`, `published` or `unshared changes`, and a listing tile
shows its poster frame before the document loads.

## UI/UX notes

The direction is command-line: high contrast, unapologetically technical, an instrument rather
than a website. The register is operational, so the workspace reads quiet and built for
scanning, with no hero and no editorial composition. The product commits to dark; a light mode
is optional and never the default.

Type is monospace everywhere, no proportional face. A display voice in capitals tracked open
and a body voice at ordinary weight carry the hierarchy, distinguishable at the smallest label
size.

Motion character is instant: state changes land immediately and nothing but the focus ring
carries a duration, because a product whose content is animated work must not have an interface
competing with it. Every transition names the properties it animates; hover is a colour change,
never a transform.

Density is compact, so a full folder fits one screen and panels separate by luminance steps
rather than by a border. Colour is rationed: the only saturated things on screen are the
graphics the product made, one primary action, and a distinct colour each for failure, success
and in progress.

Components are specified by behaviour: a control carries resting, pointed-at, pressed, focused
and unavailable states; an input shows its label and its error in a fixed place; Escape closes
a layer and returns focus to its trigger; a destructive action confirms.

Accessibility is contract: contrast meets WCAG AA, every command has a keyboard route with a
visible focus ring, icon-only controls carry labels, and meaning is never carried by colour
alone. A playing graphic is opaque, so each carries alternative text that travels with it; a
decorative one declares itself decorative.

Responsive behaviour holds at every width between the named tiers, the layout floors on the
smallest viewport and caps its container on the largest, and no route is twice as tall on a
phone as on a desktop.

## Constraints

One workspace per account; a member never reads another workspace's rows. No money appears
anywhere, and no external network call is made at run time beyond the two backing services.

Not built and not to be added: any marketing route; a desktop app, installer or download; plans, prices, invoices, proration, metering or dunning; federated identity or a
second factor; a video render pipeline or batch export; a background job queue;
customer-owned buckets or data residency; an assistant or any execution of member-supplied
code; a newsletter, a contact form or outbound email; comments, direct messages, notifications
or shared libraries; staged erasure, an audit ledger, tracing or metrics; a native mobile
app.

The app stays responsive at `2000` documents across `50` folders, `200` revisions on one
document, and `500` public listings.

## Technical requirements

Every page's HTML is produced on the server and arrives complete on first paint. A member with
scripting disabled still sees the folder tree, the document list, the revision history, the
member list and the marketplace grid, and can still follow every link. Scripting enhances a
page that already rendered: the canvas, the timeline scrubber, the state-machine graph and the
inline banners are added on top.

Stack: Python 3.12 with Django serving HTML templates, and a JSON API on the same origin under
`/api`. The front end is vanilla progressive enhancement: no bundler-produced single-page
application, no client-side router, enhancement scripts served as plain ES modules. Storage is
PostgreSQL. Objects are stored in MinIO. Authentication is app implemented email and password
with bearer tokens. `GET /api/health` returns `200`, with no credential, once the app has
connected to PostgreSQL and to the object store and has finished seeding. Application logs go
to standard output, one line per request carrying the method, path, outcome and elapsed
milliseconds, and never a password, a token, an email address or a document name. That log is
the whole of the observability surface: there is no trace pipeline and no metrics exporter.

Three trust zones scope every request. A public edge anybody reaches, which is `/m`,
`GET /api/listings` and `GET /api/runtime/{slug}`; a member surface behind a bearer token,
which is everything under `/w` and every other endpoint; and a machine surface behind a scoped
token, which is NOT built here. The boundary that matters is the first one, because the public
edge reads the same document store the member surface writes to.

Collaboration here is not realtime push. Another member's change reaches a second editor when
that editor reads `GET /api/documents/{id}/operations?since=<seq>`, so every convergence rule below is a property
of the log and of the ordering the service assigns rather than of how the bytes travel. A
client that drops its connection resumes from the last sequence it saw acknowledged rather than
from zero, and spaces its attempts with an increasing, jittered gap so a restarted service is
not met by every client at once.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
services available in this environment are PostgreSQL and MinIO, and reaching for anything
else is a contract violation.

Read every connection detail from the environment and never hardcode a host or a port.
PostgreSQL is at `DATABASE_URL`. MinIO is at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`,
`STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`; the bucket already exists and is private. The
app's own address is `APP_PUBLIC_URL` and its outside port is `APP_PUBLIC_PORT`. Both backing
services are already running and must not be downloaded, installed or started.

Paging on `GET /api/listings` and `GET /api/documents` is by opaque cursor, never an offset, at
most `24` items a page, with the cursor returned in the `X-Next-Cursor` response header and
absent on the last page. The featured ordering is snapshotted at the first page of a paging
session, so a reader never sees one listing on two pages and never skips one even when a
listing is published or unpublished between pages.

`GET /api/listings?order=` takes `featured`, `latest` or `for-hire`. `latest` is `published_at`
descending. `for-hire` restricts to authors whose `for_hire` is true, then applies the featured
ordering within that set. `featured` is an editorial ordering led by `featured_rank`, with
recency decaying, likes contributing only log-scaled and secondary, a cap of one consecutive
listing per `handle`, and a listing carrying a poster, a title and tags ranking above one that
does not. Search covers title, handle and tags, runs server side, and is reflected in the
address so a search result can be linked and restored on back.

A like is one per member per listing: posting it twice leaves `like_count` where the first post
put it, and the count moves in the same transaction as the like row rather than being counted
live.

`GET /api/runtime/{slug}` answers with `Cache-Control: max-age=10`, so a rollback reaches every
reader within ten seconds. Anything addressed by content hash is immutable and may be cached
indefinitely.

A failed publish leaves no partial state: no orphaned build row, no listing without a build,
and no channel pointing at a build that does not exist.

## Data model

Thirteen tables plus the grant, revision-parent and like join tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
not a secret. Hash it as normal; the exact literal must work at login, and it must be written
into `/app/USER_README.md` alongside each account so a grader can sign in.

`workspace`: `id`, `name`, `slug`, `seat_cap`, `created_at`. `slug` is unique.

`member`: `id`, `workspace_id`, `email`, `display_name`, `handle`, `password_hash`, `status`,
`for_hire`, `created_at`. `email` and `handle` are unique. `status` is `active`, `invited` or
`deactivated`. A handle never changes once a listing carries it.

`grant`: `id`, `member_id`, `resource_type`, `resource_id`, `role`, `deny`, `expires_at`,
`granted_by`, `created_at`. `role` is `editor` or `viewer`. Effective permission resolves in
this order: an explicit `deny` at any level defeats an allow at every level; otherwise the most
specific grant wins, so a grant on a document beats a grant on its folder; where two are
equally specific the more permissive wins; an expired grant is not a grant, evaluated against
the request's own timestamp. Resolution depends on nothing but the grant set and the resource
path.

`invitation`: `id`, `workspace_id`, `email`, `role`, `token_hash`, `state`, `expires_at`,
`created_at`. `state` is `invited`, `accepted`, `seat_blocked`, `expired` or `revoked`.

`folder`: `id`, `workspace_id`, `parent_folder_id`, `name`, `created_at`. Self referential; a
move that would create a cycle is refused and the cycle is named.

`document`: `id`, `folder_id`, `name`, `head_revision_id`, `poster_asset_id`, `deleted_at`,
`size_bytes`, `created_at`.

`artboard`: `id`, `document_id`, `name`, `width`, `height`, `index`.

`animation`: `id`, `artboard_id`, `name`, `frame_count`, `frame_rate`. `frame_count` is an
integer count of frames and is never a duration in seconds.

`state_node`: `id`, `document_id`, `name`, `kind`, `index`. `transition`: `id`, `from_state_id`,
`to_state_id`, `duration_frames`, `exit_fraction`, `condition_input`, `condition_op`,
`condition_value`, `index`. `index` is the declaration order and decides which transition wins.

`operation`: `id`, `document_id`, `seq`, `op_id`, `member_id`, `session_id`, `lamport`,
`target`, `property`, `value`, `outcome`, `discarded_by_member_id`, `created_at`. `session_id`
is one connected editing context, so one member with two tabs holds two; `lamport` is that
session's own logical clock, carried on every operation as the causal order beside the
service's total order. `seq` is unique per document and strictly
increasing; `op_id` is unique per document. `outcome` is `applied`, `superseded` or
`discarded`. Two clients appending at the same moment must receive two different `seq` values
and no operation may be lost. This must hold under real concurrency, not only in application
level checks.

`revision`: `id`, `document_id`, `author_member_id`, `content_hash`, `object_key`, `label`,
`size_bytes`, `created_at`, with `revision_parent` (`revision_id`, `parent_revision_id`)
carrying its parents. A member may name a revision through `label`, and naming one creates
none; a labelled revision is never pruned, and this build prunes no revision at all. `content_hash` is the lowercase SHA-256 hex of the exact bytes at `object_key`, and
materialising a revision whose hash equals the head's creates no revision. The graph is append
only: no parent row is ever deleted or rewritten. A restore is never destructive: it inserts a
NEW revision whose content is the restored one and whose two parent rows are the current head
and the restored revision, so every revision made after the restored one stays reachable.

`build`: `id`, `document_id`, `revision_id`, `format_version`, `content_hash`, `object_key`,
`poster_key`, `bytes`, `created_at`. Immutable after insert. `format_version` is the document
format the build was authored against, and `bytes` its stored size.

`channel`: `id`, `document_id`, `slug`, `current_build_id`, `state`, `created_at`. `slug` is
unique and `state` is `live` or `unpublished`. A channel holds at most one current build at any
time, and two simultaneous publishes to one channel never both become current.

`listing`: `id`, `build_id`, `handle`, `slug`, `title`, `tags`, `visibility`, `featured_rank`,
`like_count`, `published_at`. `visibility` is `public` or `private`, and is `public` only while
its build's channel state is `live`. `listing_like` (`listing_id`, `member_id`, `created_at`) is unique on the listing plus member
pair, and `like_count` moves in the same transaction as the like row.

**Cascade, retention and recovery.** A document is soft deleted: `deleted_at` is set, the row
stays, and the document is recoverable from a trash view that restores it to its original
folder when that folder still exists and to the workspace root otherwise. A revision is never
deleted, because the graph is append only. A build is never deleted while a channel points at
it. A member who has authored a revision is deactivated rather than deleted, so their past work
keeps its author; their grants are revoked and their tokens stop working at once.

**Derived, not stored.** The seat count is the number of distinct `active` members holding an
`editor` grant on the workspace, computed on read. The seat contradiction in the source is
resolved here rather than reproduced: members who can edit are counted and capped, members who
can only look are free and unlimited. The `unshared changes` state is computed by
comparing a document's head revision with its channel's current build. Neither is a column.

**Object keys.** A revision's bytes live in the bucket at
`documents/{document_id}/{sha256_of_bytes}.mot`, for example
`documents/1/9f2a4c0b7d6e1385a0c4fb92e7d5136a8b40cf21e9d37a5c6081bf4e2a97d350.mot`. A poster
frame lives at `posters/{build_id}/{sha256_of_bytes}.svg`, for example
`posters/1/4d81c7e05a3b92f6018de4c73b5a2096f18e0c4d7b3a95e621f08dc4a7b3e520.svg`. A document's
bytes exist nowhere else: not on the app's filesystem, not in a table column. No object exceeds
`10485760` bytes.

**Seed data.** Workspace `Northlight Studio`, slug `northlight`, `seat_cap` `3`. Members
`editor@example.com` (`Rae Okonkwo`, `rae`, `editor`), `editor2@example.com`
(`Tomas Lindqvist`, `tomas`, `editor`, `for_hire` true), `editor3@example.com`
(`Priya Raman`, `priya`, `editor`), `viewer@example.com` (`Sam Brennan`, `sam`, `viewer`,
granted read on `Broadcast` only). Folders `Product UI`, `Game UI`, `Broadcast` at the root.
Documents `Loader Ring` in `Product UI` owned by `rae` and published on channel `loader-ring`;
`Menu Transition` in `Game UI` owned by `rae` and never published; `Match Ticker` in
`Broadcast` owned by `tomas` and published on channel `match-ticker`. Artboards `Ring`
(`1920` by `1080`) and `Ring Compact` (`640` by `640`) on `Loader Ring`, `Menu` (`1280` by
`720`) on `Menu Transition`, `Ticker` (`1920` by `320`) on `Match Ticker`. Animations `Spin`
`120` frames at `60`, `Slide` `45` frames at `60`, `Crawl` `600` frames at `60`. The state
machine on `Loader Ring` has states `Idle`, `Loading`, `Done` plus `entry`, inputs `progress`
(number), `complete` (boolean) and `tap` (trigger), and transitions in this declaration order:
`Idle` to `Loading` when `progress` is greater than `0`; `Loading` to `Done` when `complete` is
true; `Done` to `Idle` when `tap` fires. Listings: `Loader Ring` by `rae` at slug
`loader-ring`, tags `ui` and `loader`, `featured_rank` `1`, `like_count` `23`; `Match Ticker`
by `tomas` at slug `match-ticker`, tags `broadcast` and `ticker`, `featured_rank` `2`,
`like_count` `623`.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the supplied visual and behavioural specification. Every value in it is
contract. Where it leaves a value open it says so.

### Information architecture

Eleven routes, listed in `## User flow`. The public surface is `/m` and `/api/runtime/{slug}`;
everything under `/w` needs a session. Navigation is `top-nav`, four items on every signed-in
route: Files, Marketplace, Members, and the account control. There is no sidebar and no menu. A
searchable command palette opens on a keyboard shortcut and reaches every command; it is the
guaranteed keyboard route, not the navigation. The work surface is a split detail pane: the
folder tree and document list on the left, the selected document's detail on the right, both
resizable and both persisted per member. Creating a document is a dedicated route rather than a
layer. Feedback is an inline banner above the surface that raised it, never a toast.

### Colour: the ground

The whole surface is built from **nine ordered neutral steps** running from the darkest
near-black neutral up to a deep neutral, and almost nothing is separated by a border. The
relationship is the requirement, not any one value: each step sits two or three points of
luminance above the one below, so a panel reads as raised without an outline. A build that
spreads them into a tidier ramp, or adds a hairline because a step looks subtle in isolation,
has produced a different product. Choose the exact values; hold the order and the interval.

| Step | Colour | Role |
|---|---|---|
| 1 `--mote-void` | the darkest near-black neutral | gradient stops, one card hover state |
| 2 `--mote-ground` | near-black neutral, a shade above the void | the page behind everything |
| 3 `--mote-ground-alt` | near-black neutral | the alternating band on long lists |
| 4 `--mote-surface` | near-black neutral | raised panel |
| 5 `--mote-card` | near-black neutral | document tiles, revision rows |
| 6 `--mote-field` | near-black neutral, the lightest of the near-blacks | inputs, ghost buttons |
| 7 `--mote-field-hover` | deep neutral | the ghost button under a fine pointer |
| 8 `--mote-raise` | deep neutral | pressed and selected rows |
| 9 `--mote-checker` | deep neutral | the transparency checkerboard behind published work |
| 10 `--mote-edge` | deep neutral | the outline that exists only on focus |
| 11 `--mote-divider` | deep neutral, the lightest step | every rule and hairline |

### Colour: text

**Nine text values, and they are not collapsible to four.** The tonal argument is that text
recedes in small steps, so a page carrying six levels of hierarchy needs no rules, no boxes and
no colour to express them. Again the ladder is the contract and the values are yours.

| Step | Colour | Role |
|---|---|---|
| 1 `--mote-text` | near-white neutral, the brightest | headings, and body on the darkest ground |
| 2 `--mote-text-light` | near-white neutral | long-form body |
| 3 `--mote-text-strong` | near-white neutral | emphasised runs inside body copy |
| 4 `--mote-text-value` | near-white neutral, the dimmest of them | numeric values in the inspector |
| 5 `--mote-text-muted` | light neutral | body copy under a heading |
| 6 `--mote-text-dim` | mid neutral | eyebrow labels and captions |
| 7 `--mote-text-default` | mid neutral | default text and the chevron stroke |
| 8 `--mote-text-faint` | mid neutral, the darkest still legible at a large size | column headings |
| 9 `--mote-text-disabled` | deep neutral | disabled controls |

### Colour: accent and semantic

Colour is rationed. Outside the work itself, seven values carry it, and each is named by family
and tone rather than by a value so the builder chooses the exact shade.

| Token | Colour | Where |
|---|---|---|
| `--mote-cta` | a light, vivid orange | the fill on the one primary control |
| `--mote-amber` | a light, vivid orange, softer than the call to action | the eyebrow mark above a section heading |
| `--mote-link` | a light, soft cyan | in-content links |
| `--mote-primary` | a light, vivid cyan | the primary control inside the workspace |
| `--mote-primary-hover` | a light, soft cyan | that control under a fine pointer |
| `--mote-ok` | a mid, soft teal | affirmative state |
| `--mote-no` | a light, vivid red | negative state, and the filled like control |

The affirmative mark inside a filled disc reads as a lighter teal and the negative mark as a
lighter red, because both sit on a fill rather than on the ground. The primary control is the
only saturated fill on a viewport, one per viewport, never two; every other control is a
near-black neutral ghost.

### Contrast

On this palette the near-white neutrals and the light neutral clear the contrast bar against
the ground at body size. A mid neutral clears it at large sizes only, which is why eyebrow
labels and column headings are the only things set in one. The darkest mid neutral does NOT
clear it at body size, so it is never a body-text colour here: secondary and legal copy steps
up one rung. The deep neutral used for disabled controls clears nothing and is correct for
disabled and for nothing else.

### The spectrum sweep

One effect uses full spectrum and it is the product's signature: a single line of text filled
with a horizontal gradient interpolated in a perceptual colour space, with the gradient
translated across the text rather than the text being recoloured. The perceptual space is
normative: a linear interpolation between the blue stop and the orange stop passes through
grey and a perceptual one does not, and a muddy midpoint is the defect. The ramp runs from a
near-white neutral through a vivid blue, a vivid cyan, a vivid orange and a vivid magenta, in
that order, over roughly the middle third of the line; the source's own capture truncates the
tail and the build completes it. The gradient is clipped to the text and animated by
translating its background position.

### The checkerboard and depth

Published work is shown against a checkerboard of two deep neutral squares, because much of it
has a transparent background and a flat dark panel would hide that. Two layers at an offset,
at the tile radius below.

There is almost no shadow. An input carries a resting inset ring that is fully transparent
until focus. A tile and its badge carry the faintest possible drop, a single pixel of offset
and two of blur at low opacity. A selected tab carries a slightly deeper one. Two gradient
overlays do the rest: a downward black-to-transparent wash under an open layer, and a radial
near-black-to-black ground at the top of a route.

### Typefaces and the type scale

One monospace superfamily, in two voices: **Roboto Mono**, the open-licensed family the source
already uses for this product's own application chrome. The display voice is capitals at weight
500, tracked open; the body voice is the same face at 400, tracked normal. The two must be distinguishable
at a glance at `12px`, because the eyebrow sits at `12px` directly above body copy at `14px`.
Naming an open-licensed family is not an asset dependency, and a normative fallback stack ships
so the first paint is never blank. Numeric values align in columns wherever amounts stack.

| Token | Size | Weight | Line-height | Voice |
|---|---|---|---|---|
| `micro` | `10px` | 400 | `12px` | body |
| `caption` | `11px` | 400 | `17.6px` | body |
| `eyebrow` | `12px` | 500 | `14.4px` | display |
| `label-bold` | `12px` | 700 | normal | body |
| `body-s` | `13px` | 500 | `22.1px` | body |
| `body-tight` | `14px` | 500 | `14px` | body |
| `body-dense` | `14px` | 400 | `16.8px` | body |
| `body` | `14px` | 400 | `19.6px` | body |
| `body-loose` | `14px` | 400 | `21px` | body |
| `body-relaxed` | `14px` | 400 | `22.4px` | body |
| `body-m` | `15px` | 500 | `21px` | body |
| `body-m-loose` | `15px` | 500 | `22.5px` | body |
| `lead` | `16px` | 400 | `25.6px` | body |
| `lead-tight` | `16px` | 500 | `19.2px` | body |
| `title-s` | `20px` | 500 | `24px` | display |
| `title` | `20px` | 500 | `28px` | display |
| `title-m` | `21px` | 500 | `29.4px` | display |
| `title-l` | `24px` | 500 | `33.6px` | display |
| `heading` | `40px` | 500 | `48px` | display |

### Letter-spacing

Two tracking values carry as much of the register as the faces do. The wordmark and the eyebrow
are tracked open: four capitals across `275` units of a `50`-unit-tall box, roughly four times
the natural advance, and it is the single most identifying typographic decision here.
Everything else is tracked normal or slightly tight, and body copy is never tracked.

### Radius, spacing and density

Radius is small and five values cover the product: `8px` on buttons and cards, `10px` on media
panels, `5px` on small controls and tags, `4px` on inputs and table cells, `3px` on text
placeholders, `12px` on the marketplace tile, `16px` on the pill control and on tile avatars,
`2px` on a badge, and `50%` on an avatar. Density is compact: rows sit tight so a full folder
fits one screen, and the list and the detail stay readable side by side.

### Iconography

Nothing ships as a file. The chevron is a three-point path `M5.5 6.5L7.5 8.5L9.5 6.5` in a
`0 0 15 15` box, stroked in the default mid neutral, round caps and joins, no fill; the apex sits `2` units below
the arms and a `3`-unit drop reads as a different, chunkier mark at that size. The corner mark
is `M 6 0 L 6 6 L 0 6 L 6 6 Z` in a `0 0 12 12` box under
`translate(3 1) rotate(45 3 3)`, stroke width `1.75`, fill `transparent`, stroked in the brightest near-white neutral: it
walks out along one arm and back along the other, so it is two strokes and not a triangle.
The like control is a `0 0 16 14` path with `evenodd` fill and clip rules, stroked in the
default mid neutral when unset and filled in the light, vivid red when set. The play badge is a `0 0 256 256` enclosure rendered
`20 x 20` with `polygon points="160 128 112 96 112 160 160 128"`, stroke `rgb(255, 255, 255)`
at width `16`, round caps and joins, no fill. The layers mark is the same box rendered `17 x 17`
as a solid fill with four rounded quadrants at `8` unit radii, unequal in size so it reads as
panes rather than a grid. The wordmark is the product name drawn in the display voice as
capitals, tracked to fill a `5.5:1` aspect ratio, converted to outlines, filled in the
brightest near-white neutral, never coloured, at `220 x 40`, `143 x 26` and `110 x 20`; the monogram is its first letter
under the same rule, a single glyph with a diagonal cut.

### Chrome and controls

Three control styles and no others. Primary: the light, vivid orange fill, no border, a
near-white neutral label at `eyebrow`, one per viewport. Ghost: the lightest near-black neutral
fill with a `1px` inset ring drawn on `::after` in the first deep neutral, a near-white neutral
label at `eyebrow`, every other control. Pill: the light, vivid cyan, no border, a near-white
neutral label, `16px` radius, the marketplace surface only.

Measured hover transitions: the ghost's fill moves up one neutral step while its `::after`
ring jumps several, landing at a light neutral; the pill's fill moves from the vivid cyan to
the soft one. Reproduce the split: the ring brightens much further than the fill, and a
single border property animating both at once produces a control that looks like it is lighting
up rather than being outlined. Controls carry an optional leading icon at `17px` at the label's
colour.

The in-content link is the most repeated interaction: `color` and `border-color` on the text
and on both pseudo-elements move together from `rgb(153, 153, 153)` to `rgb(255, 255, 255)`.
The underline is a bottom border on `::after` and a clipped duplicate on `::before`, so it is
drawn across rather than switched on. On a surface that sits on artwork the same construction
runs from `rgba(255, 255, 255, 0.75)` instead.

Every component carries resting, pointed-at, pressed, focused and unavailable states.
Unavailable is never signalled by colour alone. `Escape` closes any layer and returns focus to
its trigger, and arrow keys move within a layer. A destructive action confirms first.

The header is not fixed: it scrolls away with the page and does not return on scroll up. Below
`800px` its items collapse behind one control, and the panel that opens is full height over the
page rather than a dropdown; opening it traps focus, holds its own scroll position, and
restores the page's on close.

### Motion

Four curves cover the whole product and a fifth is never invented: `cubic-bezier(0,0,.2,1)` for
anything entering or growing, `cubic-bezier(.4,0,1,1)` for anything leaving or shrinking,
`cubic-bezier(.05,0,0,1)` for a layer opening, and `cubic-bezier(.4,0,.2,1)` for anything moving
between two resting states.

Everything a person triggers resolves in `1s` or less, and only a whole panel takes as long as
`1.5s`. Anything ambient is slow and was never triggered by anybody. Two keyframe animations
belong to the product's own shell: a banner fade from `opacity: 0` to `opacity: 1`, and an
empty-state float alternating between `translateY(-40px)` and `translateY(-20px)`, a `20px`
travel that reads as breathing rather than bobbing.

`transition: all` is never declared: it animates properties nobody intended, including ones a
script sets at load, and it is a leading cause of the first-interaction hitch. Every hover state
sits inside `(hover:hover) and (pointer:fine)` and every continuous animation sits inside
`(prefers-reduced-motion: no-preference)`; a hover state that fires on touch leaves an element
stuck in its hover appearance until the next tap elsewhere and repaints on every tap.

Under a reduced-motion preference continuous motion STOPS rather than slowing, because a
slowed marquee is still motion; a playing document renders its first frame and waits for an
activation control that is present; and the colour and opacity transitions REMAIN. Removing
those as well makes the interface feel broken rather than calm, and every route stays complete
and readable with nothing content-bearing that exists only while something moves.

Nothing plays an entrance on scroll. Nothing is scrubbed against scroll position. The things
that move, move continuously, and all of them are the product's own output rather than the
page's decoration.

### The playback surface

Every playing document on every surface goes through one player component, and nothing else in
the build touches a renderer.

1. Determinism: the same document, the same starting state and the same ordered inputs with the
   same timestamps produce byte-identical frames, in the workspace preview and at the runtime
   address alike.
2. Time is supplied, not sampled: the player advances by an elapsed time passed into it and
   never reads a clock itself.
3. Resolution independence: artwork is vector, rasterised at the device's actual pixel ratio,
   re-rasterised on a ratio change, never scaled from a cached bitmap.
4. Bounded cost: a document declares its own artboard size and the player draws into a surface
   of exactly that aspect. Where the container disagrees, the fit rule belongs to the embedding
   and takes one of `contain`, `cover`, `fill`, `fit-width`, `fit-height`.
5. Graceful degradation: where the accelerated path is unavailable the player falls back to a
   software path at a reduced rate rather than failing. A blank rectangle where artwork should
   be is the worst available outcome.
6. Bounded memory: one graphics context draws every visible document on a page; instances are
   pooled and reused.
7. Only what is visible advances. A document outside the viewport is suspended, keeps its
   state, and resumes at the state it held. Suspension is by intersection, not by scroll offset.
8. A frame budget is declared per page and enforced. When it is exceeded, documents drop to a
   lower advance rate in a stable order, furthest from the centre of the viewport first, and
   recover in the same order. Dropping is visible as slowness, never as stopping.
9. Every embedding has a poster: the document's own first frame, rendered at publish time and
   delivered with the listing. Nothing is ever a blank rectangle while a binary loads.

The runtime interface is versioned independently of the document format. A document authored
against format version `N` plays in every runtime built for `N` or later; forward compatibility
is not claimed. A runtime meeting a newer format version says so through its interface and
shows the poster frame rather than drawing a partial document.

### The state machine at runtime

A document's behaviour is a graph, not a sequence. A state is a named animation or a
pseudo-state; a transition is a directed edge with a duration, an exit time and an ordered
condition list; an input is a named boolean, number or trigger; a listener is a named pointer
region with an event and input assignments; a layer is an independently evaluated set of states
composited in declaration order.

1. Conditions are evaluated in declaration order and the first satisfied transition wins.
2. A trigger is consumed by exactly one evaluation and then cleared, whether or not it caused a
   transition.
3. Exit time is a fraction of the source state's duration and a transition cannot be taken
   before it.
4. A later layer overrides an earlier one for any property both animate, and nothing else about
   layer interaction may be relied on.
5. Setting an input is queued and applied at the next advance, never immediately, so a host
   that sets three inputs in a row sees all three applied to the same frame.

Data binding: a document declares typed properties and the host supplies values. Types are
string, number, boolean, colour, enumeration, image and list. Binding is one way from host to
document by default, with an explicit two-way mode for a property a listener writes. A missing
property falls back to the authored value and never stops the document playing. A type mismatch
is a load-time error reported on the interface rather than a silent coercion.

### The document surface

Five regions, all resizable, all persisted per member per document: a hierarchy tree, the
artboard canvas, an inspector, an animations list, and the timeline or the state-machine graph.

A Design and Animate switch decides what every other region does: in Design an edit changes an
object's resting value, in Animate it writes a keyframe at the playhead. The mode is a hard
modal boundary and the canvas carries a persistent visual treatment while in Animate, and it is
not subtle.

The hierarchy is virtualised and scrolls ten thousand nodes at the display's rate; it supports
multi-select, drag to reparent with before, after and inside as three distinct drop targets,
full keyboard operation including reparenting, inline rename that keeps the selection, and a
search that keeps the ancestors of matches visible.

The canvas hit-tests against rendered geometry rather than bounding boxes, zooms continuously
and cursor-anchored from `1x` to `64x` with fit-to-artboard and 100 percent commands, pans by
space-drag, middle-drag and two-finger scroll, snaps to artboard edges and object edges and
centres with a suppressing modifier, and draws its scale, rotate and skew handles at a constant
screen size regardless of zoom. Handles drawn in document space make the canvas unusable above
about `4x`.

The inspector groups Transform (position `X` and `Y`, scale `X` and `Y` as percentages,
rotation in degrees, style), Layer (a blend mode and an opacity percentage), Clipping and
Constraints. Values render at `body-tight` in the dimmest near-white neutral on near-black
neutral fields; labels render at `caption` in the default mid neutral. Every numeric field is also a scrubber: dragging the label changes the
value continuously, the scrubber is `8px` wide by `16px` tall in a row `24px` tall, and a whole
scrub gesture produces one undo entry rather than one per frame.

The timeline carries one track per animated property, grouped by object and collapsible;
selectable, multi-selectable, draggable keys with a marquee; a playhead that is draggable and
settable from the ruler and that renders every frame it passes while scrubbing; per-key-pair
interpolation edited on a curve graph with the four curves above as presets; snapping to
frames, keys and markers with a suppressing modifier; and a loop range independent of the
animation's own length.

The state-machine graph carries states plus entry, any and exit pseudo-states as draggable
nodes with persisted positions; transitions as selectable curves with a visible direction; a
transition's duration, exit time and ordered conditions in the inspector; explicit reorderable
condition order; one graph per layer as tabs; and live operation, so inputs are settable while
the graph runs and the active state and the traversing transition are highlighted.

Undo is a command stack, not a sequence of document snapshots, and each command carries its
inverse. One gesture is one command, so a drag through two hundred positions undoes once. The
stack survives a document reload within a session. **Undo is per member**: in a document with
three people editing, undo reverses the member's own most recent un-undone operation and never
somebody else's, even when somebody else's was more recent. A member's undo emits a new
operation that inverts their own, transformed against everything applied since; it does not
remove anything from the log, the document does not travel backwards, and an undo whose target
no longer exists is refused with a reason rather than applied approximately. A command that
cannot be inverted is refused rather than pushed as an unwindable entry.

### The workspace surface

The chrome carries the monogram, a workspace switcher with the chevron, and a breadcrumb at the
top left; search across the workspace's documents at the top centre; the account control at the
top right; and a notice strip for quota and incident notices.

The document list shows a tile per document: a `12px` radius on the checkerboard carrying the
document's poster frame, a title at `body-tight` weight 500 in the brightest near-white neutral
that is inline editable, meta at `caption` in the default mid neutral giving the edited-at time and who edited it, and a
`caption` chip where a document is `published`, has `unshared changes`, or is a `draft`. The
list sorts by edited-at descending by default and also by name, created-at and size; the sort
is per member and persists.

Four situations the file browser must survive: a folder of ten thousand documents scrolls
smoothly because the list is virtualised, the sort runs in the service and paging is cursor
based; a move of four hundred documents between folders is one operation with one undo, applied
atomically or not at all; a folder shared with a member who cannot see its parent shows the
breadcrumb they can see and elides the rest, never leaking the names of folders above their
grant; and one document open in two tabs by one member is two sessions and not a duplicate, so
presence shows that member once and edits from both converge.

The breadcrumb elision is a hard requirement, not a courtesy: `viewer@example.com` is granted
`Broadcast` and must not be able to obtain the names `Product UI` or `Game UI` through any
route or any endpoint.

### The marketplace surface

The marketplace drops the workspace chrome and carries its own: the monogram, the word
`Marketplace` with the chevron, a full-width search field between the title and the tabs at
a near-black neutral with `8px` radius and the placeholder `Search the marketplace`, three tabs
`Featured`, `Latest` and `For hire` at `eyebrow` with the selected tab on a deep neutral at `8px`
radius carrying `rgba(0, 0, 0, 0.4) 0px 4px 8px 0px`, and one pill control reading
`Get started`. Its footer carries a copyright line and nothing else. The copyright year is
computed, never typed.

The tile is three columns at desktop, `12px` radius, on the checkerboard: the document playing
and contained; an avatar at `24px` with `16px` radius or a lettered placeholder on a near-black
neutral; the author at `body-tight` weight 500 in a near-white neutral; a `For hire` badge at
`caption` with `2px` radius on the light, vivid cyan where the author offers commissions; a
middle dot separator in a mid neutral, because a separator in a heading is typographic and never pictographic and the
source's pictographic glyph is deliberately not reproduced; the title at `body` in a light neutral
truncated to one line with an ellipsis; and the
like control with its count right-aligned at `caption` in the default mid neutral. Counts render as integers
to `999`, then one decimal and a thousands suffix.

The grid renders at every width: one column below `600px`, two to `1024px`, three above. It is
virtualised and holds a bounded number of live documents, the rest showing their poster frame.
A tile is a link with a real address covering the whole tile rather than the title alone, so it
can be opened in a new tab.

### Module boundaries

Five modules, and the boundaries are the load-bearing part. `document` owns the document model,
the commands and the undo stack, and knows nothing of the network or the canvas. `render` owns
the renderer, the canvas, hit testing and handles, and mutates the document only through
commands. `sync` owns the operation log, presence and transport, and does not know what a
command means. `shell` owns panels, layout, routing and the persistence of panel state, and
holds no document logic. `service` owns the service interface, tokens and retry, and is never
called from `render`.

`document` has no dependency on `render`, `sync` or `service` and is testable headlessly with
no network, no canvas and no clock. That is what makes the determinism requirement testable at
all.

The public surface and the workspace surface do not share a bundle: a visitor reading the
marketplace must not download the document editor.

### Responsive behaviour

Three widths: `1440 x 900`, `990 x 800`, `390 x 844`. Three switches carry the layout: at
`min-width: 800px` the top-nav shows its items in full and the split detail pane splits; at
`min-width: 1024px` the list and the detail sit side by side at full width and the marketplace
grid goes to three columns; at `min-width: 600px` the marketplace grid goes from one column to
two. Below `375px` the layout sets a floor and stops adapting; above `2200px` the container
caps and centres while the ground continues to the edges.

Type does not scale with the viewport; it steps at the two primary switches. At `390px` a
headline fits two lines without hyphenation and without a horizontal scroll. No route's mobile
scroll extent exceeds twice its desktop extent. Any track wider than the viewport sits inside a
clipping container exactly the viewport's width, so nothing drags the page sideways.

### Accessibility

Every interactive element carries a visible focus indicator meeting contrast against both
the page ground and a field; on this palette a `2px` outline in the brightest near-white neutral at `2px` offset is the only
value that works on both. Focus order follows reading order on every route. A layer traps focus
and restores it to its trigger. In the document surface, focus moves between the five regions
with a documented key and the current region is announced.

Contrast meets WCAG AA throughout. Every command is reachable from the keyboard with a
searchable command palette as the guaranteed route, and every value is editable without a
pointer, including the inspector's scrubbers, which accept typed values and arrow-key stepping.
Colour is never the only signal: the Design and Animate modes, the state of a graph node and
the document state chip each carry a second signal. No essential information is conveyed only
by a hover.

A playing document is a canvas and a canvas is opaque. Every embedding carries a text
alternative describing what the document depicts and, where it is interactive, what it does;
that alternative is authored on the document and travels with it rather than being written at
the embed site. An interactive document is a control: focusable, its inputs reachable from the
keyboard, its state changes announced. A decorative document is marked as such and skipped
entirely.

Duplicated markup is never used to produce a visual effect: a track that repeats its contents
is repeated for the eye and once for the accessibility tree.

### Performance

Budgets per route, uncompressed, excluding documents: the marketplace at `260KB` of script,
`90KB` of fonts and `30KB` of markup; the workspace shell at `700KB` of script, `90KB` of fonts
and `20KB` of markup; the renderer module at `400KB`, loaded on demand by the first player that
mounts and never on a route that has none.

Targets: first contentful paint under `1.5s` on a mid-tier phone on a `4G` profile; largest
contentful paint under `2.5s` on the same; cumulative layout shift under `0.05`; interaction to
next paint under `200ms` on the busiest grid; and a sustained display frame rate with the
marketplace grid playing, over a `10s` window, with no dropped frames. The workspace holds the
display's rate while scrolling a hierarchy of ten thousand nodes.

Three families need three files, not thirty-two: one variable file each where available, subset
to the ranges the interface actually uses, preloaded, with a normative fallback stack.

No video ships. Every moving thing on every surface is a playing document, which averages about
`21KB`, rather than a recording of one.

The renderer module is never on the critical path to first paint: a route paints its text and
layout before any document loads. A document that fails to load leaves its poster frame in
place permanently, never a blank rectangle. On a device without the accelerated path the
software fallback targets half the display's rate rather than dropping documents.

### Zero assets

No photograph, typeface file, icon file, video or animation document ships with this build.
There is no asset manifest and no reference to an asset file anywhere; this substitution guide
is the whole of it. Icons are drawn from the coordinates above. Wordmarks are constructed from the display voice
rather than copied. Where the specification names a third-party mark, the build ships a
lettered placeholder on a near-black neutral at the same rect until a real one is supplied. Artwork is the
product's own output: a playing document stands in for every image, and its poster frame stands
in for a document that has not loaded.

### Naming conventions

Component classes are `mote-<component>`; element classes are `mote-<component>__<element>`;
state classes are `is-<state>` on the component root; custom properties are `--mote-<token>`;
custom events are `mote:<noun>-<verb>`, for example `mote:document-published`; data attributes
are `data-mote-<name>`, for example `data-mote-channel`.

### Evidence gaps

Two classes of value in the specification above are reconstructed rather than measured, and a
reader deciding how much to trust one should know which. The document surface and the
marketplace tile were reconstructed from published product screenshots rather than captured
directly. The whole service contract is derived from what the interface promises, which is the
only honest source available: an interface that advertises seats and workspace-wide permissions
has committed to a permission model whether or not anybody outside can see it. The hero type
size, the truncated tail of the spectrum sweep and the clipped reveal are reconstructions.
Five captured duration values were extraction artifacts of shorthand parsing and are not
durations. Expect the reconstructed numbers to need adjustment; treat the measured ones as
exact.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world
  uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable
  from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{ "email", "password", "display_name", "handle" }` | `{ "token", "member_id", "workspace_id" }` |
| `POST /api/auth/login` | `{ "email", "password" }` | `{ "token", "member_id" }` |
| `GET /api/me` | - | `{ "id", "email", "display_name", "handle", "role", "workspace_id" }` |
| `GET /api/health` | - | `{ "status" }` |
| `GET /api/folders` | - | a top-level array of `{ "id", "name", "parent_folder_id" }` |
| `POST /api/documents` | `{ "folder_id", "name" }` | `{ "id", "folder_id", "name", "head_revision_id" }` |
| `GET /api/documents` | `?folder_id=&cursor=` | a top-level array of `{ "id", "name", "folder_id", "state", "updated_at" }`, with `X-Next-Cursor` |
| `GET /api/documents/{id}` | - | `{ "id", "name", "folder_id", "head_revision_id", "artboards", "state_machine" }` |
| `POST /api/documents/{id}/operations` | `{ "op_id", "target", "property", "value" }` | `{ "seq", "outcome", "discarded_by" }` |
| `GET /api/documents/{id}/operations` | `?since=` | a top-level array of `{ "seq", "op_id", "member_id", "target", "property", "value", "outcome" }` |
| `POST /api/documents/{id}/revisions` | `{ "label" }` | `{ "id", "content_hash", "object_key", "parent_revision_ids", "created" }` |
| `GET /api/documents/{id}/revisions` | - | a top-level array of `{ "id", "content_hash", "object_key", "parent_revision_ids", "label", "created_at" }` |
| `POST /api/documents/{id}/revisions/{revision_id}/restore` | - | `{ "id", "content_hash", "parent_revision_ids" }` |
| `GET /api/documents/{id}/revisions/{revision_id}/content` | - | the revision's exact bytes |
| `POST /api/documents/{id}/publish` | `{ "revision_id", "channel_slug", "title", "tags" }` | `{ "build_id", "channel_slug", "content_hash", "object_key", "poster_key", "listing_id" }` |
| `POST /api/channels/{slug}/rollback` | `{ "build_id" }` | `{ "channel_slug", "current_build_id" }` |
| `POST /api/channels/{slug}/unpublish` | - | `{ "channel_slug", "state" }` |
| `GET /api/runtime/{slug}` | - | the current build's exact bytes, `Cache-Control: max-age=10` |
| `GET /api/listings` | `?order=&q=&cursor=` | a top-level array of `{ "id", "title", "handle", "slug", "poster_key", "like_count", "featured_rank", "published_at" }`, with `X-Next-Cursor` |
| `POST /api/listings/{id}/likes` | - | `{ "listing_id", "like_count", "liked" }` |
| `GET /api/members` | - | a top-level array of `{ "id", "email", "display_name", "handle", "role", "status", "for_hire" }`, plus `{ "seat_cap", "seats_used" }` on `GET /api/members/seats` |
| `POST /api/invitations` | `{ "email", "role" }` | `{ "id", "state", "token" }` |
| `POST /api/invitations/{token}/accept` | `{ "password", "display_name", "handle" }` | `{ "state", "member_id" }` |

Every list endpoint returns a top-level JSON array. Field names are exact. Bearer auth is
required on everything except `GET /api/health`, `POST /api/auth/signup`,
`POST /api/auth/login`, `GET /api/listings` and `GET /api/runtime/{slug}`. A successful call
returns the named shape; an invalid or unauthorized call is rejected as a client error, never
a `5xx` and never a silent success, and carries a reason. The agent chooses conventional codes.

### No mocks

PostgreSQL and MinIO are the facts. An in-memory documents dictionary, a hardcoded
`{"status":"stored"}` response the app returns to itself, document bytes written to the app
container's filesystem, a base64 column standing in for an object, or a listing feed served
from a fixture file are all contract violations however good the interface looks. The named
provider is the fact: the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Definition of done

A stranger can browse the marketplace, find a published graphic, sign up and open a document in
their own workspace. An editor can edit a document alongside a teammate and both end on the
same value, with the loser told who won. Publishing a revision makes its exact bytes available
at the channel's runtime address, and rolling back puts the previous bytes there within ten
seconds. A document that has never been published is reachable from no public address and
appears in no marketplace result.
