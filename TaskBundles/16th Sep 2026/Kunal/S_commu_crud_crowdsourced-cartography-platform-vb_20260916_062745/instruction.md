# Openhaven

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, pan and zoom a map drawn from the stored geographic data, sign in as a
mapper, correct a feature, and see that correction still there after a reload,
without hitting an error page. The hard part is that the dataset is shared: two
mappers who start from the same version of the same feature and save at the same
moment must not both succeed, and the one who loses must be told which feature
and which version put them out of date. That guarantee has to hold in the stored
data itself, not in a message the interface shows to one of them.

## Overview

Openhaven is a single, shared, editable map of the world. It is one dataset with
several faces: a rendered map you can pan and zoom, an editor that writes into
it, a history that records every change ever made to it, and a small set of
reading pages around it. The dataset is the product; the pages are the lobby.

Three audiences use it at once. Visitors open the map, move around it, search
for a place and read the community diary, with no account at all. Mappers sign
up, open the editor, and add or correct real-world features: a road, a building
outline, a point of interest. Their save merges into the live dataset and
becomes visible to everyone. Downstream consumers read the same data through the
HTTP API and draw it somewhere else, which is why the API is a first-class
surface and not an implementation detail of the pages.

The genuinely hard part is that the whole dataset is world-writable and nobody
may lock a region while they work, so two people editing the same corner of the
world at the same moment is ordinary rather than exceptional, and neither
person's work may be silently dropped.

Openhaven deliberately is not a general social network. There are no likes, no
follows, no private messages between users, and no comment threads on diary
entries. There is no GPS trace upload, no route planning or directions, no
language selector, no donation flow, and no desktop editor handoff. There is no
moderator tier: reverting a bad change is an ordinary edit that any signed-in
mapper can make, and it is recorded like any other.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor (signed out) | Read everything: the map, any element and any of its past versions, the changeset history, the diary, about and help. Search the dataset. Download an area. | **Cannot create, modify, delete or revert anything. Cannot open a changeset. Cannot post a diary entry.** |
| Mapper (signed in) | Everything a visitor can do, plus: open a changeset, upload creates, modifies and deletes in it, close it, comment on any changeset, and revert any changeset including one they did not write. | **Cannot edit another mapper's diary entry. Cannot delete history: a removal is recorded as a new version, never as an erasure.** |

There is one authenticated role. Mappers are peers: the dataset is shared, so
any mapper may correct or revert any element regardless of who touched it last.
The boundary that matters is signed in versus signed out.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a signed-out
visitor session to any mapper-only endpoint must be rejected by the server (an
unauthorized request is denied, not served), leaving the protected state
unchanged.

Signup is open: anyone may create an account from `/signup` with an email and a
password, and is signed in immediately afterwards.

Three accounts are seeded so the dataset has history from the first start:

| Email | Display name |
|---|---|
| `mapper@example.com` | Ada Fenwick |
| `mapper2@example.com` | Bo Larsen |
| `mapper3@example.com` | Cleo Nkemdirim |

## Core features

### Auth

Accounts are email and password, implemented by this app. There is no external
identity provider.

1. `POST /api/auth/signup` takes an email and a password and creates a mapper.
   An email already in use is rejected as invalid and creates no second account.
2. `POST /api/auth/login` takes an email and a password and returns a bearer
   token. The client sends that token on every mutating request.
3. Passwords are stored hashed, never in plain text, and never returned by any
   endpoint.
4. A token expires after eight hours. A request carrying an expired or absent
   token to any mutating endpoint is denied and changes nothing.

### The shared dataset

Everything on the map is built from three element types, and every other feature
here rests on them.

1. A **node** is a single point at a latitude and longitude. It may stand alone
   as a point of interest, or serve as a vertex of a way.
2. A **way** is an ordered list of node references. Open, it is a road or a
   path; closed, where the last reference repeats the first, it is a building or
   a lake.
3. A **relation** is an ordered list of members, each a node, a way or another
   relation, each carrying a role.
4. Every element carries an integer id, a `version`, the id of the changeset
   that wrote it, a timestamp, the mapper who wrote it, and a `visible` flag.
5. Tags are free-form `key=value` strings on any element: `highway=residential`,
   `building=yes`, `amenity=cafe`.
6. Relations reference their members by id and never by copy. **One way must be
   able to belong to several relations at once**, and correcting that way once
   must correct it everywhere it participates. A build that duplicates the way
   into each relation fails this rule: editing it in one place would leave the
   others stale.
7. A way may only reference nodes that exist and are `visible`. A relation may
   only reference members that exist.
8. Deleting a node that is still a member of a visible way or relation is
   refused, and the refusal names the referencing elements and says the node is
   `still in use`. The node stays visible and unchanged.

### Editing: the changeset cycle

Edits are never loose. A mapper batches them into a changeset.

1. `PUT /api/changeset/create` opens a changeset for the signed-in mapper and
   returns its id. A changeset carries a free-text comment describing the edit.
2. `POST /api/changeset/{id}/upload` applies a batch of creates, modifies and
   deletes. Each element in the batch states the `version` the editor loaded.
3. The upload is atomic. If any element in the batch is refused, **none** of the
   batch is applied and the stored dataset is exactly as it was before the call.
   A half-merged changeset must never exist.
4. `PUT /api/changeset/{id}/close` closes it. A closed changeset accepts no
   further uploads.
5. On a successful upload every touched element gets a new `version`, exactly
   one higher than the version it had, attributed to that changeset and that
   mapper.
6. A changeset carries a bounding box computed from the elements it touched, and
   a count of the elements it wrote.
7. A changeset may not write more than `500` elements. A larger batch is
   rejected as invalid and writes nothing.
8. **The persisted element must match what the editor displayed, and must
   survive a reload.** After a mapper saves a corrected name or tag on a
   feature, reopening that feature in a new browser session, and reading it back
   from `GET /api/node/{id}`, must both show the corrected value and the raised
   `version`. A value that is shown in the interface but is not in the stored
   dataset fails this rule, and so does one that reverts to its old value when
   the page is loaded again.

### History and blame

Nothing is ever overwritten.

1. Every version of every element is retained and addressable. Reading an
   element at a past version returns exactly what it was at that point, not a
   reconstruction.
2. `GET /api/node/{id}/history` returns every version of that node, oldest
   first. The same holds for ways and relations.
3. A delete does not erase. It writes a new version with `visible` false, so the
   element can still be inspected and can be brought back.
4. `GET /api/changesets` returns the changeset stream, `newest first`, each with
   its author, its comment, its bounding box and its counts of creates,
   modifies and deletes.
5. Opening one changeset lists the exact elements and versions it wrote.
6. Every element resolves to who last touched it, in which changeset, and when.
7. History is append-only. Writing a new version must never alter an older one,
   so the record of what an element used to be is stable forever.

### Reverting a bad change

1. `POST /api/changeset/{id}/revert` creates a **new** changeset that restores
   every element the named changeset touched to the version it held immediately
   before that changeset ran.
2. A revert is an ordinary, attributed edit: it is authored by the mapper who
   asked for it, it appears in the changeset stream like any other, and it can
   itself be reverted.
3. A revert never deletes history. The reverted versions remain readable.
4. Reverting a changeset whose elements have since moved on to newer versions is
   refused rather than forced, and the refusal names the elements that moved.

### Validation that warns without blocking

The dataset is open to everyone, so a good-faith mapper must not be stopped by a
wall of gates, while a structurally broken edit must still be refused.

1. The editor warns, before upload, about likely mistakes: a way that crosses
   itself, a building outline that overlaps another, a tag key it does not
   recognise, and a value outside a sensible range. Each warning names the
   element it is about.
2. These warnings are **dismissible and do not block the upload**. The mapper
   may upload over any of them, because the editor cannot know local ground
   truth and the person standing in the street can.
3. The server refuses only structural violations: a reference to an element that
   does not exist, a delete of something `still in use`, a stale `version`, and a
   batch over the element ceiling. It never refuses an edit for being
   subjectively wrong.

### The map surface

The structure of this surface is a stack: tiles at the bottom, the vector layers
over them, and the floating chrome above both.

1. `/` opens a full-viewport map of the dataset with the site chrome floating
   over it. Pan by dragging, zoom by wheel, by double-click and by the plus and
   minus controls on the right-hand rail.
2. The map is a grid of square tiles positioned by their `{z}/{x}/{y}` address,
   with markers, the search result pin and the location dot drawn in layers
   above them.
3. A first-time visitor sees a welcome card over the map, headed "Welcome to
   Openhaven!", with a short line explaining that the map is made by people like
   you and free to use under an open license, and two actions: one that reads
   more about the project and one that starts mapping. Closing it dismisses it,
   and the choice survives a reload of the page.
4. A layer switcher offers named base styles and overlay toggles for notes, raw
   data and traces. The chosen style survives a reload.
5. Searching a place name finds matching features in the dataset and drops a
   result pin on the map at the matched feature. Dismissing the pin removes it.
6. The locate control drops a distinct marker for the viewer's own position.
7. A scale bar sits at the bottom left and an attribution line naming Openhaven
   contributors sits at the bottom right, on every view of the map.

### Tiles drawn on demand

1. `GET /api/tile/{z}/{x}/{y}.png` returns one map tile, `256` pixels square,
   drawn from the stored elements whose geography falls inside that tile's
   bounds plus a small buffer so features crossing the edge draw correctly.
2. Zoom `0` is the whole world in one tile, and each zoom step splits every tile
   into four, so zoom `z` holds two-to-the-z tiles across and the same down. The
   deepest zoom the app serves is `19`.
3. Which tags draw as what, and at which zooms, is one style definition shared by
   every zoom level. Zoom decides how much detail is drawn, never which dataset
   is read.
4. Tiles are drawn **on demand, per tile**. The app must never pre-draw the
   whole world.
5. A tile is cached after it is drawn and served from that caching layer while
   it is still current. Freshness decides that: a tile stays current until an
   edit touches its bounds.
6. When an edit changes data inside a tile's bounds, that tile and its parents
   and children in the pyramid are marked stale and are drawn again on their
   next request, so an edit becomes visible without redrawing the planet. The
   trigger is the changed element's own bounds, never a clock.

### Spatial querying: finding what is inside an area

This is the busiest read in the product and it has to stay fast as the dataset
grows.

1. `GET /api/map?bbox=min-lon,min-lat,max-lon,max-lat` returns every node inside
   the box, every way any of whose nodes is inside it, and every relation
   referencing those, as a single JSON payload.
2. This is the read the map itself makes as you pan, and the read the editor
   makes before you edit.
3. The request is capped by area: a `bbox` larger than `0.25` square degrees is
   rejected as too large, with a message naming the limit, so one request can
   never ask for the whole world.
4. It is capped by count as well: a request that would return more than `5000`
   elements is rejected the same way.
5. An element created seconds ago is returned by a `bbox` covering it on the
   very next request. There is no delay before a new feature becomes findable by
   location.
6. `/export` shows the map with a panel that downloads the raw elements for the
   area currently in view, through the same bounded read.

### The reading pages

1. `/about` explains the project: that Openhaven provides map data for thousands
   of websites, mobile apps and hardware devices, and that it is built by a
   community of mappers who contribute and maintain data about roads, trails,
   cafes, railway stations and much more, all over the world. It carries five
   short sections headed Local Knowledge, Community Driven, Open Data, Legal and
   Partners.
2. `/diary` lists community diary entries, `newest first`, each showing its
   title as a link, a byline reading "Posted by" the author's display name and
   the date, the body, and a comment count. Ten entries are shown per page, with
   newer and older pagers.
3. `/help` is a grid of help resources. Each is a bordered tile with a heading
   and a one-line description, and `the whole card is clickable`, not just the
   heading.
4. Every form in the app rejects invalid input inline, naming the field that is
   wrong and leaving the other fields as the person typed them, and writes
   nothing when it does. Signing up with a malformed email, opening a changeset
   with an empty comment, or posting a diary entry with no title are each
   refused this way.
5. An address that matches nothing renders Openhaven's own not-found page,
   headed "File not found", with a way back to the map, and answers as not
   found rather than as success.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the map home: full-viewport map, welcome card, search | public |
| `/edit` | the editor over the same map | mapper |
| `/about` | what the project is and how it is licensed | public |
| `/diary` | community diary entries, newest first | public |
| `/help` | grid of help and community resources | public |
| `/history` | the changeset stream for the current view | public |
| `/export` | download the raw elements for the current view | public |
| `/changeset/:id` | one changeset and the exact elements it wrote | public |
| `/login` | sign in | public |
| `/signup` | create an account | public |

**Entry and redirects.** A signed-out request for `/edit` goes to `/login` and,
after a successful sign-in, continues to `/edit` rather than to the map home.
Signing in from `/login` directly lands on `/`. Signing out returns to `/` and
the map is still fully readable. A token that expires mid-edit returns the
mapper to `/login` with the open changeset still open, so no queued work is
lost. Every read route is reachable signed out; a signed-out request to a
mapper-only endpoint is denied by the server, not merely hidden in the interface.

**Journeys.**

1. *A visitor reads the map.* Open `/`, close the welcome card, drag the map
   west, zoom in twice, type "Riverside Cafe" into the search field, press the
   search control. A result pin drops on the cafe and a panel names it. Reload
   the page: the welcome card does not come back.
2. *A mapper corrects a feature.* Sign in as `mapper@example.com` with
   `deku-demo-pw-2026`, open `/edit`, click the node named `Old Mill`, change
   its name in the form that opens over the map, give the changeset the comment
   "Corrected the mill name", and upload. The browser lands on that changeset's
   own page, which lists the one element it wrote and its new `version`. Open
   `/api/node/2` in a new session: the new name and the raised `version` are
   both there.
3. *Two mappers collide.* `mapper@example.com` and `mapper2@example.com` both
   load node `1` at `version` `1`. Both upload a different name for it. One
   upload is accepted and takes the node to `version` `2`. The other is rejected,
   naming node `1`, the `version` it sent and the `version` now stored, and
   writes nothing at all: the node still holds exactly one new name, not two.
4. *A delete is refused.* Sign in as `mapper3@example.com`, open `/edit`, select
   node `3`, which is a vertex of the way `Kingsway`, and try to delete it. The
   upload is refused, the message says the node is `still in use` and names
   `Kingsway`, and node `3` is still `visible`.
5. *History is walked.* Open `/history`, pick the changeset commented
   "Initial survey of the town centre", and read the elements it wrote. Follow
   `Riverside Cafe` to its history and read its first version. Then revert a
   later changeset from its own page and watch a new changeset appear in the
   stream, authored by the mapper who asked for it.
6. *A newcomer joins.* Open `/signup`, submit a malformed email, and read the
   inline message naming the email field with the rest of the form still filled
   in. Correct it, submit, and land signed in on `/` ready to open `/edit`.

**States.** The map shows a loading state while tiles are being drawn and never
a blank rectangle. The changeset stream, the diary list, the search results and
a changeset's element list each have an empty state that says what would appear
there. A failed request shows a message in place and leaves the rest of the page
usable; nothing in this app crashes to a blank screen.

## UI/UX notes

The north star is that the map is understood instantly as the real subject and
everything else reads as quiet furniture around it. The register is operational:
this is a tool people work in, not a poster, so it is dense but organised, built
for scanning and for repeated action, with no oversized hero and no editorial
composition. Calm over expressive, and legibility over atmosphere, because a
mapper is reading fine geographic detail for long stretches.

**Palette, by role.** The surface is a near-white neutral, with a second
near-white neutral for header bands and subtle fills that reads as a shade
quieter than the page. Body text is a deep cool neutral, and a mid cool neutral
carries timestamps, bylines and captions so they recede without becoming
unreadable. Borders are a near-white cool neutral hairline, one weight
everywhere, used instead of shadow to separate things. The primary accent is a
light, vivid blue: it carries links, focus and the primary action, and nothing
decorative wears it. A light, soft green belongs to the edit control and the
brand mark and signals a valid state, with a mid, soft green available as its
secondary accent; green means "you may change the world here" and appears
nowhere else. A mid, vivid red means something has gone wrong or will be
destroyed, and it appears nowhere else. A mid, vivid amber carries caution and a
mid, vivid cyan carries informational badges. A mid, vivid magenta is reserved
for inline code. A deep cool neutral band, distinct in role from the
body text that shares its description, backs the one dark chrome strip on the
about page. The map itself is `the brightest thing on the screen`: the chrome
around it stays desaturated so that the rendered tiles carry the colour.
A light cool neutral draws the zoom-target marker. The exact shades are yours,
so long as each role above keeps its exclusivity.

What this must not look like: a page dominated by one hue family with no second
signal, decoration standing in for content, or a marketing composition where a
working interface belongs.

**Type and typography.** The body family is the `system UI stack`: `system-ui, -apple-system,
"Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", "Liberation Sans", Arial,
sans-serif`. Monospace is `SFMono-Regular, Menlo, Monaco, Consolas, "Liberation
Mono", "Courier New", monospace` and is reserved for identifiers, tags and
coordinates. Body copy is `14px`, which is the dominant size, at a line height
of `21px`. Lead paragraphs and form controls are `16px` at `24px`. Fine print
and attribution are `12px` at `18px`. Page titles are `32px` at weight `500`.
Section subheads are `20px` at `30px`. Card headings are `18px` at weight `600`.
Figures align wherever versions, counts or coordinates stack in a column.

**Shape, spacing and density.** The corner radius is softly rounded rather than
sharp or pill-like, with one step softer for cards and panels and one step
tighter for small controls. Shadow is spare, used only to lift a menu or a map
control off the surface beneath it, and spacing carries the rest. Density is comfortable rather than airy: rows in the changeset stream
and the element list sit close enough that a full page of history is read
without scrolling, while the reading pages breathe. Space does the separating,
with a hairline only where space alone would be ambiguous.

**Components.** Every interactive thing has a resting, pointed-at, pressed,
focused and unavailable state. The outlined green edit control `fills in
solidly` when it is pointed at, inverting its text against it. Escape closes the
editor form and the layer panel. A destructive action, including a revert, asks
for confirmation first and names what it will undo. Something unavailable is
never signalled by colour alone.

**Motion.** The character is eased: entrances and exits are considered, so
movement reads as a designed interface rather than a machine. It is restrained
and always has a job, because this is a tool. A spinner `turns while something
loads`. The location marker sends out a `soft expanding ripple` like a raindrop
landing, and it is the one lively moment in the product. Content that has not
arrived yet shows a skeleton state, a `placeholder shimmer`, rather than jumping
when it lands, and deferred content `fades in after a beat` rather than
flashing. The search result
pin `fades out as it is dismissed`. A panel `slides in from the edge` and back
out. Colour transitions on controls settle quickly rather than lingering, and
every transition in the product shares one character so the whole interface
reads as one thing. Those are the only animations here; nothing is driven by
scrolling. Where a person has asked their system for reduced motion, all of this
movement simply stops; nothing is substituted for it and nothing is left
animating. Where a person has forced-colors turned on, the interface honours
their colours instead of overriding them.

**Accessibility.** Body text meets the WCAG AA contrast bar against its
background, and the green and blue accents carry controls, large text and
non-text marks rather than small body copy. Every interactive control shows a
clearly visible focus ring in the blue accent, and the whole app, the map
controls included, is operable by keyboard navigation alone. Icon-only controls
carry text alternatives, loading regions announce themselves, and meaning is
never carried by colour alone. Every content image carries alternative text
describing what it shows, and an image that is purely decorative declares itself
decorative so it is skipped rather than announced.

**Responsive.** The layout holds at every viewport between the named tiers, not
only at them. On a narrow viewport the navigation collapses behind a single
toggle that opens a stacked menu, the search field and the welcome card become
full-width sheets over the map, the help grid reflows to one column, and diary
entries run full width. The control rail stays pinned to the right edge and its
targets stay comfortably sized for a fingertip. Nothing overflows sideways at a
narrow viewport, and every navigation target stays reachable.

**Mode.** Commit to light and design it fully. A dark mode is optional and is
not part of what this brief asks for.

## Front-end specification

**Module architecture and the rendering split.** The map client is one module
and the editor is another, and neither reaches into the reading pages. Those
reading pages arrive as HTML from the server, so they
are readable and indexable without the map ever running. The map is one
self-contained rich client mounted into that HTML, and the editor is a separate
part of it that is only fetched when a mapper actually goes to `/edit`.
Navigation between pages swaps the content without a full reload.

**Iconography, and zero-asset substitution.** Nothing in this build fetches an image file, an
icon font or a web font. Every icon is drawn as inline vector geometry in the
page, at one flat line-drawn weight throughout: a teardrop pin with an inner dot for a place, a magnifying glass with a
handle for search, a circled pin for the zoom target, chevrons for the pagers,
a stack for the layers control, a crosshair for locate, and a cross for close.
Each is a single-weight line drawing that inherits the current text colour, so
it stays crisp at any size. The about page banner and the small locale marks
beside diary entries are drawn procedurally from the palette rather than loaded.
The type is the system stack, which needs no file.

**Copy identity.** These strings are content facts, not suggestions:

| Where | Copy |
|---|---|
| Brand | the wordmark `Openhaven`, beside a compass mark |
| Navigation | `History`, `Export`, `User Diaries`, `Help`, `About` |
| Actions | `Edit`, `Log In`, `Sign Up` |
| Search | `Search`, `Where is this?` |
| Attribution | `Openhaven contributors` |
| Welcome card | `Welcome to Openhaven!`, `Learn More`, `Start Mapping` |
| Layers panel | `Map Layers`, `Standard`, `Cycle Map`, `Transport Map`, `Topographic`, `Humanitarian`, `Map Notes`, `Map Data`, `Public GPS Traces`, `Legend`, `Share` |
| About | `Local Knowledge`, `Community Driven`, `Open Data`, `Legal`, `Partners` |
| Diary | `Users' Diaries`, `Recent diary entries`, `Newer Entries`, `Older Entries`, `Posted by`, `See full entry`, `No comments`, `Location:` |
| Help | `Getting Help`, `Beginners' Guide`, `Help & Community Forum`, `Mailing Lists`, `For Organizations`, `Openhaven Wiki` |
| Loading | `Loading...` |
| Not found | `File not found` |

## Technical requirements

The frontend is Remix, which is React Router 7, running on Node 20. The backend
is FastAPI on Python 3.12. Storage is PostgreSQL, reached at `DATABASE_URL`.
Auth is app-implemented email and password with bearer tokens. `GET /api/health`
returns `200` once the app is ready. Because the rendering model is
server-rendered pages with one embedded rich client, the browser receives the
content of `/about`, `/diary` and `/help` as HTML on first paint, and the map
becomes interactive after that.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor. The only backing service available in this environment is
PostgreSQL, already running and reachable at `DATABASE_URL`, and reaching for
anything else is a contract violation.

**Under simultaneous requests.** When two uploads that both claim the same
`version` of the same element arrive at the same moment, exactly one of them is
applied and the element ends at exactly one new `version`. The other upload
must leave the stored dataset untouched, and the losing mapper receives a
`409 Conflict` response naming the element, the `version` they sent and the
`version` now stored, so they can reload and decide what to do. Replaying an
upload that has already been applied must not create a second version of any
element in it and must not create a second changeset: the dataset after the
replay is byte-for-byte the dataset after the first call. These outcomes are
properties of the stored data under real concurrency, and they hold however many
requests arrive together.

**Every public route carries its own title and description**, and no two routes
share either: the map home, the editor, about, diary, help, history, export and
each changeset page are each described distinctly in the document head.

**A sitemap lists every public route**, served at `/sitemap.xml`, and a robots
file at `/robots.txt` points at that sitemap. Both are served by the app itself
and stay correct as routes are added.

Seeding runs at startup and is idempotent.

## Data model

Ten tables. All timestamps are UTC. Three of them hold the primitive element
types and the rest hang off those.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account
so a grader can sign in.

**mappers** - `id`, `email` (unique), `display_name`, `password_hash`,
`created_at`.

**changesets** - `id`, `mapper_id`, `comment`, `opened_at`, `closed_at`,
`min_lon`, `min_lat`, `max_lon`, `max_lat`, `element_count`. A changeset is open
until `closed_at` is set.

**nodes** - `id`, `version`, `changeset_id`, `mapper_id`, `lat`, `lon`,
`visible`, `created_at`. An element is identified by its `id` together with its
`version`, and both are stored; neither is derived.

**ways** - `id`, `version`, `changeset_id`, `mapper_id`, `visible`,
`created_at`.

**way_nodes** - `way_id`, `way_version`, `sequence`, `node_id`. The order of a
way's nodes is the `sequence`, and it is stored, not inferred.

**relations** - `id`, `version`, `changeset_id`, `mapper_id`, `visible`,
`created_at`.

**relation_members** - `relation_id`, `relation_version`, `sequence`,
`member_type`, `member_id`, `role`. `member_type` is node, way or relation.

**tags** - `element_type`, `element_id`, `element_version`, `key`, `value`.

**diary_entries** - `id`, `mapper_id`, `title`, `body`, `posted_at`.

**tile_cache** - `z`, `x`, `y`, `image`, `drawn_at`, `stale`.

A changeset's bounding box and its `element_count` are derived from the elements
it wrote rather than supplied by the client.

**Invariants, stated as properties of the stored data.** Referential integrity
and versioning are both properties of this stored data, never of a single
request. An element's `version`
is `1` when it is created and rises by exactly one on every later write to it. A
write never alters an existing row, so every past version remains exactly as it
was. A way's node references and a relation's member references always resolve
to elements that exist, and a node that any visible way or relation still
references cannot be made not `visible`. Two writes that both start from the
same `version` of one element leave that element at exactly one new `version`,
never two, and never at a version that skips a number.

**Seed data.** Three mappers, as listed under User roles. Three closed
changesets: changeset `1` by Ada Fenwick commented
"Initial survey of the town centre", changeset `2` by Bo Larsen commented
"Added Market Hall outline", and changeset `3` by Cleo Nkemdirim commented
"Tagged the cycle route".

Nine nodes at `version` `1`. Node `1` is `Riverside Cafe`, tagged
`amenity=cafe`. Node `2` is `Old Mill`, tagged `historic=mill`. Nodes `3`, `4`
and `5` are the vertices of a road, and nodes `6` through `9` are the corners of
a building.

Two ways at `version` `1`. Way `1` is `Kingsway`, tagged `highway=residential`,
running through nodes `3`, `4` and `5`. Way `2` is `Market Hall`, tagged
`building=yes`, a closed outline around nodes `6` through `9`.

Two relations at `version` `1`. Relation `1` is `Route 12`, tagged `route=bus`.
Relation `2` is `Thames Cycle Way`, tagged `route=bicycle`. **Both reference way
`1`**, which is the seeded proof that one road belongs to several relations at
once.

Three diary entries, newest first: "Mapping the towpath after the flood" by Bo
Larsen, "Three weeks of building outlines" by Ada Fenwick, and
"Why I started mapping" by Cleo Nkemdirim.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- One shared global dataset. There is no tenancy, no per-user dataset and no
  private area of the map.
- No GPS trace upload, no route planning, no directions and no routing engine.
- No desktop editor handoff and no remote control.
- No chrome-free embed route.
- No language selector, no translation and no locale switching.
- No donations, no payments and no billing of any kind.
- No moderator tier, no user blocking and no account suspension.
- No private messaging, no follows, no likes and no comment threads on diary
  entries beyond the count.
- No replication feed and no external mirrors.
- No content delivery network and no second host for tiles: tiles are served by
  this app, on this origin.
- No external network calls at runtime. No third-party map data, no hosted tile
  provider and no geocoding service.
- No native mobile app.
- No downloaded binary asset of any kind: no image file, no icon font, no web
  font.
- Performance: the app must stay responsive with fifty thousand elements in the
  dataset and five thousand changesets of history.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written
  to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the
  app root, empty.
- Serve a production build behind a static or preview server, never a dev
  server.
- The server must keep running after this session ends and must not be a child
  of the shell. An ordinary background job dies with its shell, and the app will
  not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing service named in this brief is already running and reachable at
  its environment variable. Do not download, install, compile or start a copy of
  it.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password`, `display_name` | the created mapper and a bearer token |
| `POST /api/auth/login` | `email`, `password` | a bearer token |
| `GET /api/health` | none | `200` once ready |
| `GET /api/map` | `bbox=min-lon,min-lat,max-lon,max-lat` | an object holding arrays of `nodes`, `ways` and `relations` |
| `GET /api/node/{id}` | none | the current node: `id`, `version`, `lat`, `lon`, `visible`, `tags`, `changeset` |
| `GET /api/node/{id}/{version}` | none | that node exactly as it was at that `version` |
| `GET /api/node/{id}/history` | none | a top-level JSON array of every version, oldest first |
| `GET /api/way/{id}` | none | the current way: `id`, `version`, `nodes`, `visible`, `tags` |
| `GET /api/relation/{id}` | none | the current relation: `id`, `version`, `members`, `visible`, `tags` |
| `PUT /api/changeset/create` | `comment` | the opened changeset with its `id` |
| `POST /api/changeset/{id}/upload` | `create`, `modify`, `delete`, each element carrying its `version` | the written elements with their new versions |
| `PUT /api/changeset/{id}/close` | none | the closed changeset |
| `POST /api/changeset/{id}/comment` | `text` | the stored comment |
| `POST /api/changeset/{id}/revert` | none | the new changeset that undid it |
| `GET /api/changesets` | optional `bbox` | a top-level JSON array, newest first |
| `GET /api/tile/{z}/{x}/{y}.png` | none | one `256` pixel square tile image |
| `GET /api/diary` | optional `page` | a top-level JSON array of entries, newest first |

Every mutating endpoint requires the bearer token. `GET /api/health`, the login
and signup endpoints, and every read above are reachable without one. A
successful call returns the named resource or shape. An invalid or unauthorized
call is rejected as a client error, never as a server error and never as a
silent success.

**No mocks.** The dataset is the fact. An in-memory array of elements that the
process rebuilds on restart, a hard-coded tile image returned regardless of
what the data says, a history assembled at read time from the current row rather
than from stored versions, or a conflict decided by a variable held in the web
process are each a violation of this contract. PostgreSQL holds the elements,
their versions, the changesets and the tags, and the app's own interface can
only reflect what lives there, never substitute for it.

## Definition of done

A visitor can open the map, move around it, search a place and read the diary
without an account, and a signed-in mapper can correct a feature and find that
correction still there after a reload, with every past version still readable.
When two mappers save a change to the same feature from the same starting
version at the same moment, the feature ends up holding exactly one of those
changes, and the mapper whose change did not land is told which feature and
which version put them out of date. Any changeset can be undone by a new one
that is itself recorded, so nothing in the map's record is ever lost.
