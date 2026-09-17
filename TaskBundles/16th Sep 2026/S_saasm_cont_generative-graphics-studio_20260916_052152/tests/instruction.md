# vvvivid

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, pick a tool from the tile
grid, drag a control and watch the preview redraw, and leave with the graphic, without hitting an
error page and without signing in. A different stranger must NOT be able to read a preset its
owner has kept private: not from the gallery, not from its own address, and not by asking for its
rendered export. This cannot be faked in the interface. Hiding a card from a grid while the
address behind it still answers is not protection, and a rendered export must live in the object
store at a key derived from its own bytes, where a copy on the app's own disk does not count.

## Overview

vvvivid is a free suite of browser-side graphic generators for web designers and developers. The
front door is a grid of tiles, one per tool. Opening a tile gives a live preview above a panel of
controls. Dragging a control redraws the preview immediately, in the browser, with no round trip.
When the graphic looks right the visitor copies its markup or downloads a raster export. Nothing
has to be established before the tool works: no account, no onboarding, no modal, and no state to
set up. Most people who use this product never sign in, and every generator is complete for them.

Signing in adds the one feature that touches stored state. An author saves the current settings
as a named preset. A preset's address is derived from the settings themselves rather than
assigned, which means saving is idempotent: two people who independently arrive at the same
settings produce the same address and one stored row. A preset is private when saved. Its owner
may publish it to a public gallery, where other people browse it, open it and fork it, and a fork
records what it came from.

There are no comments, no likes, no follows, no messaging, no payment and no email. The
genuinely hard part is that a preset's identity is a function of its own content, and three
things have to stay true at once because of it: saving the same settings twice must not make two
rows, a private preset must be unreachable three separate ways, and a rendered export must be
addressed by its bytes so that two identical renders share one stored object.

## User roles

| Role | Can do |
|---|---|
| `reader` | Use every generator in full, signed in or not: change controls, copy the markup, download an export. Browse the public gallery, open a published entry, read its lineage. Open an unlisted preset when holding its address. Report a gallery entry. **Cannot save a preset. Cannot render into the object store. Cannot publish. Cannot fork. Cannot read a private preset owned by anybody, in a listing or at its own address, and cannot fetch its export.** |
| `author` | Everything a reader can do, plus: save the current settings as a named preset, render an export, change the visibility of a preset they own, publish one they own, fork any preset they can read, and read their own preset list. **Cannot edit, publish, delete or change the visibility of a preset another account owns. Cannot change a preset's derived address. Cannot republish an entry another account published.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI
is not authorization: a direct API call from a `reader` session to any `author`-only endpoint
must be rejected by the server (an unauthorized request is denied, not served), leaving the
protected state unchanged.

There is no public signup. Accounts exist only because they are seeded. There is no password
reset and no invitation flow.

Seeded accounts, all sharing the password `deku-studio-2026`:

| Email | Handle | Display name | Role |
|---|---|---|---|
| `mara@vvvivid.tools` | `mara` | Mara Okonkwo | `author` |
| `tomas@vvvivid.tools` | `tomas` | Tomas Reinholt | `author` |
| `visitor@vvvivid.tools` | `visitor` | Ines Haddad | `reader` |

## Core features

### The derived address

This is the idea the rest of the product rests on, and it is the first thing to get right.

A preset's identifier is computed from its own settings, never assigned. Canonicalise the
settings into one string, digest it, encode the digest, and take the leading nineteen characters.

The canonical string is: the generator key, the generator version, then every parameter as
`key=value` in the generator's own schema order with no parameter omitted even when it equals its
default, then the seed, then the width, then the height. Fields are joined with a single vertical
bar. There is no whitespace anywhere in it. Numbers are written in plain decimal with no trailing
zeros and no exponent.

The digest is SHA-256 over the UTF-8 bytes of that string. The encoding is base32 using the
lower-case alphabet `a` to `z` followed by `2` to `7`, with any padding removed. The identifier
is the first nineteen characters of that encoding.

A worked example, which must reproduce exactly:

```
canonical: bbblob|1|complexity=5|contrast=40|edges=smooth|fill=solid|seed=7|w=1200|h=1200
id:        iiancd7svxmz3dbmqqk
```

1. Saving a set of settings returns the identifier that derivation produces.
2. Saving the same settings a second time, by the same account or a different one, returns the
   same identifier and leaves exactly one preset row.
3. Two authors saving identical settings at the same instant must not both create a row: exactly
   one row exists afterwards and both callers receive the same identifier. **This must hold at
   the database level, not only in application logic.**
4. A canonical string longer than `8192` bytes is rejected as too large and stores nothing.
5. No request can set or change a preset's identifier. An attempt to supply one is ignored.

### Visibility, and what private means

A preset carries one of three visibilities: `private`, `unlisted`, `public`. A preset is
`private` when first saved unless the author says otherwise.

1. A `private` preset is absent from the gallery and absent from every public listing, for
   everybody.
2. Reading a `private` preset at its own address, as a signed-out visitor, as a `reader`, or as
   an `author` who does not own it, is refused as not found. The refusal is indistinguishable
   from the refusal for an identifier that was never created, so a caller cannot learn that the
   preset exists.
3. Fetching a `private` preset's rendered export is refused the same way, by the same three
   callers.
4. The owner of a `private` preset reads it at its own address and sees it in their own list.
5. An `unlisted` preset resolves at its own address for any caller holding that address, and
   stays absent from the gallery and from search. The interface must describe an unlisted
   address as shareable rather than as secret, because the address is derived from the settings
   and anyone who arrives at the same settings arrives at the same address. Describing it as a
   secret is a defect.
6. A `public` preset resolves for anyone and appears in the gallery once published.
7. Only the owner changes a visibility. Any other account attempting it is denied, and the row
   does not change.

### Rendered exports and the object store

A render turns a preset into a stored file. Exports live in the object store, never in the
database.

1. An author renders a preset they can read. The bytes are written to the bucket at
   `renders/{sha256_of_bytes}.{ext}`, where the digest is the SHA-256 of the object's own bytes,
   in lower-case hexadecimal, and `{ext}` is `svg` or `png`. A worked example: an SVG document
   whose bytes hash to `900fbe93...b601` is written to
   `renders/900fbe934249ad120004bd24adf66aad8817d89586273c0cc50e187bddebb601.svg`.
2. The key is derived from the bytes and nothing else: not the preset, not the account, not the
   time.
3. Two presets that render to identical bytes produce one stored object, and both presets
   reference that one key.
4. A render row records the key, the format, the dimensions and the byte size. No column
   anywhere holds the bytes themselves.
5. A render larger than `4194304` bytes is refused as too large. It writes no object and leaves
   the preset's existing renders untouched.
6. A format other than `svg` or `png` is refused as an unsupported format, with the same two
   consequences.
7. A published preset's export is fetched by anybody. A private preset's export follows the
   visibility rule above.
8. Rendering a preset another account owns is denied, and no object is written.

### Forking and lineage

1. An author forks any preset they can read. The fork opens the generator with the parent's
   settings loaded.
2. Changing at least one parameter and saving produces a new preset whose parent is the original.
   Saving with nothing changed derives the parent's own identifier, so it returns the parent
   rather than creating a self-parented row.
3. A fork records exactly one parent. The parent's fork count rises by exactly one at the moment
   the fork is created, and is stored rather than counted on read.
4. Lineage is walked in both directions: toward ancestors for attribution, toward descendants for
   the fork count. An ancestor walk stops at a depth of `64` and reports that it stopped rather
   than truncating silently.
5. Deleting a preset that has forks does not orphan them. Its row is tombstoned: its parameters
   are retained, its title and owner are cleared, its state becomes `tombstoned`, and a child
   still resolves its ancestry through it.
6. A tombstoned preset is absent from the gallery and from every listing, and its own address
   reports that it was withdrawn rather than reporting not found, because its children still
   name it.

### Publication and the gallery

1. Publishing sets a preset's visibility to `public` and creates one gallery entry.
2. Publication requires an account, requires a title of `1` to `80` characters, and accepts up
   to `8` tags. A public gallery with unattributable authorship has no lever against abuse, which
   is why anonymous publication is refused.
3. Publishing a preset that is already published returns the entry that already exists and
   creates no second entry. At most one gallery entry exists per preset.
4. Publishing a preset another account owns is denied, and no entry is created.
5. The gallery lists entries whose state is `live`, newest published moment first. An entry whose
   state is `limited` is reachable at its own address and absent from the gallery listing. An
   entry whose state is `removed` is absent from both.
6. Filtering the gallery to one tool lists only that tool's entries, in the same order.
7. An entry displays its title, its publisher's handle, its immediate parent when it has one, and
   its fork count.
8. Tags are read back in their stored order, which is the order the author gave them.

### Reporting

1. Anybody, signed in or not, reports a gallery entry with a reason drawn from `spam`,
   `infringement`, `offensive` and an optional note.
2. A reason outside that set is rejected as invalid and stores nothing.
3. A report increments the entry's report count. Reporting does not by itself change the entry's
   state.
4. Report rows are readable by nobody through the public interface.

### The tools

Twenty-four tiles are seeded, listed under `## Data model`. Three kinds sit behind them:
generators with a live preview and controls, colour tools, and long-form documents with neither.

The naming convention is the product's identity and is normative. A tool's name is an ordinary
lower-case English word whose first letter is repeated three times, so a tool that makes ripples
is named by tripling the first letter of "ripple". Names are set in lower case everywhere,
including at the start of a sentence and in the page title. Names run between five and thirteen
characters. The two documents deliberately break the convention and are set in sentence case with
a space, because they are documents and not tools. No tile carries a category label; its one-line
description is the only explanation.

1. The tile grid is one component rendered from one stored list, and it appears on every route.
   A grid hand-authored per route is a defect.
2. A tool's route slug is its name. No separate slug field exists.
3. A generator whose status is `retired` keeps its route, its schema and its presets, and leaves
   the tile grid. `vvvanish` is seeded as the retired one: its route resolves and it is absent
   from the grid.
4. A generator route carries a live preview, the control panel, and the full tile grid beneath
   its own content.
5. Changing a control redraws the preview without a round trip to the server. With scripting
   unavailable the route still renders, the controls still submit, and the preview still arrives
   drawn by the server.
6. The same settings produce the same graphic whether drawn in the browser or on the server.
7. Six generators carry a real parameter schema: `bbblob`, `wwwave`, `gggrid`, `ffflow`,
   `rrripple` and `gggrit`. Each schema is an ordered list of parameter descriptors, and each
   descriptor names its key, its label, its kind, and the group it belongs to. A continuous
   parameter also declares its own range and step. The schema order is what the canonical string
   above walks.

### The public surface

These hold on every route a signed-out visitor can reach.

1. A terms page states what may be done with a generated graphic and what the product asks of a
   publisher. It is reachable from the footer of every route, and it is linked from the publish
   surface, because publication is the one place in this product where a person commits to
   something.
2. Every internal link on every public route resolves. A link in the tile grid, in the rail, in
   an about block or in a footer that leads nowhere is a defect, and the grid is rendered from
   the stored tool list precisely so that a retired tool cannot leave one behind.
3. A first-time visitor is asked once whether non-essential cookies are wanted. The answer is
   remembered, survives a reload, and the visitor is not asked again. Declining leaves every
   generator fully working, because nothing in the product needs a non-essential cookie.
4. Every form rejects invalid input inline, names the field that is wrong in words beside it,
   and writes nothing. This holds for the sign-in form, the save form, the publish form and the
   report form. A form that reports a failure only after writing a partial row is a defect.

### Auth

Email and password. A successful sign-in returns a bearer token in a field named `access_token`,
and the client sends it on every authenticated request. Passwords are stored hashed, never in
plain text, and no endpoint returns a password or its hash. A token is valid for twenty-four
hours from issue; an expired or malformed token is denied exactly as a missing one.

1. Signing in with a seeded email and `deku-studio-2026` succeeds and returns `access_token`.
2. Signing in with a seeded email and any other password is denied, and the response does not
   reveal whether the email exists.
3. Signing in with an unknown email is denied identically.
4. Reading the session with a valid token returns that account's email, handle, display name and
   role. Reading it without a token is denied.

## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/` | The tile grid, which is the product's only navigation | none |
| `/{tool}` | One generator: preview, controls, about block, then the grid | none |
| `/{tool}/save` | Name the current settings and save them as a preset | `author` |
| `/p/{id}` | One preset at its derived address | none |
| `/gallery` | Published entries, newest first, filterable by tool | none |
| `/gallery/{id}` | One entry with its lineage and its fork count | none |
| `/studio` | The signed-in author's own presets, with their visibilities | `author` |
| `/studio/presets/{id}/publish` | Give a title and tags, then publish | `author` |
| `/studio/presets/{id}/published` | The confirmation that publication succeeded | `author` |
| `/sign-in` | Sign in | none |
| `/license` | What may be done with the output | none |

### Entry and redirects

A signed-out visitor who opens `/studio`, any `/studio` address or a `/{tool}/save` address is
sent to `/sign-in`, and after a successful sign-in lands on the address originally asked for
rather than a generic home. A signed-in `reader` who opens one of those is shown a refusal saying
the action belongs to accounts that can save, and is not sent to sign in again. An author who
opens the publish address for a preset another account owns is shown the same refusal. Signing
out returns the visitor to `/` and discards the token. A token that expires mid-action leaves the
visitor on the same surface with a message saying the session ended and a control to sign in
again, and the settings they were working on are still on screen when they return.

### Journeys

1. **Leave with a graphic, signed out.** Open `/`. The grid shows the seeded tiles in their
   stored order, `vvvivid` names set in lower case. Open `bbblob`. The preview is already drawn.
   Drag the complexity control; the preview redraws as it moves. Copy the markup, and the copy
   control confirms in place. Scroll past the about block and meet the full grid again. Open
   `wwwave` from it.
2. **Save a preset.** Sign in as `mara@vvvivid.tools`. Work `gggrid` until it looks right. Take
   the save action, landing on `/gggrid/save`. The route shows the address the current settings
   derive to, before saving. Give the title `Tight rule grid` and leave the visibility private.
   Save. Open `/studio`: the preset is listed, marked private.
3. **Private stays private.** With the identifier from journey 2, open `/p/{id}` signed out: not
   found. Open it as `visitor@vvvivid.tools`: not found. Open it as `tomas@vvvivid.tools`: not
   found. Ask for its export as any of the three: refused the same way. Open it as
   `mara@vvvivid.tools`: it resolves.
4. **Publish.** Signed in as `mara@vvvivid.tools`, open the publish address for that preset, give
   a title and two tags, and publish. The surface is replaced by a full-page confirmation naming
   the entry's address. Open `/gallery` signed out: the entry is first, newest first.
5. **Fork.** Signed in as `tomas@vvvivid.tools`, open that gallery entry and fork it. The
   generator opens with the parent's settings. Change one control and save. The new preset names
   the original as its parent, and the original's fork count has risen by one.
6. **Saving is idempotent.** Signed in as `tomas@vvvivid.tools`, reproduce exactly the settings
   of a preset `mara@vvvivid.tools` already saved and save them. The same identifier comes back
   and no second row is created.

### States

Every list has an empty state written for that list: an author with nothing saved is told no
preset has been saved yet; a gallery filtered to a tool with no entries is told that tool has
nothing published yet; an entry with no forks shows a fork count of zero rather than hiding the
figure. The gallery itself is never empty, because seeded presets are published into it. Every
route has a loading state holding the final layout's shape so nothing jumps when content arrives.
A tool name that does not resolve, and a preset identifier that does not resolve, both show a
not-found page inside the same shell carrying a link home and a link to the gallery. A withdrawn
preset shows a withdrawn page rather than a not-found page. A failed request says what failed and
offers the action again. No route may leave the visitor on a blank page or an unstyled error.

## UI/UX notes

The design direction is `clinical-precision`. The mood is calibrated, neutral and medical-grade.
The type personality is one neutral sans with a monospace reserved for identifiers. The motion
character is `eased`. The density is comfortable. The layout archetype is a persistent rail
beside a content column, because the navigation is a rail.

**North star.** In the first moment a stranger should understand that everything on the screen
except the graphic is deliberately holding still, so the graphic is the only thing being judged.

**Register.** Operational. This is an instrument, not an editorial page: quiet, organised, built
for repeated adjustment. The graphic supplies all of the colour in the product.

**Precision over personality. The output over the interface. Reversibility over commitment,
everywhere except publication, which is deliberately one-way.**

### Ground, surface and the four meanings

The page ground is a very light neutral. Panels sit on a slightly raised neutral that separates
from the ground without a border and without a shadow, so the separation is carried by the
difference between the two grounds alone. The preview sits on a third surface, distinct from both
and deliberately the most neutral thing on the page, because it is the backdrop the visitor
judges colour against. A checkered indication shows where the graphic is transparent, and it is
the one place a repeating pattern is allowed in the chrome.

One accent carries the primary action and appears nowhere else in the interface. Three further
colours carry meaning and nothing decorative: one for something that failed, one for something in
progress, one for something private. A surface that is none of those four borrows none of them.
The exact shades are yours, so long as they hold those rules and clear the contrast floors below.

`medical-grade` governs the chrome and never the output. A tool for choosing colour must not tint
its own panels, or the visitor cannot judge what they are making. Every saturated pixel in a
correct build belongs to the graphic, the primary action, or one of the three meanings.

Text carries three levels of presence and no more: the value a person is reading, the label
naming it, and the quiet metadata beneath.

**Mode.** The product ships one fully designed light appearance and no second one. There is no
dark mode and no theme switch. A colour tool is judged against the ground it sits on, so a
single known ground is a requirement rather than a limitation: a graphic that looks right here
looks right for everyone who opens it. Every contrast floor below is stated against that one
appearance.

The colour of this product lives entirely in what the generators draw. The palettes the tools
ship with run wide and bright: mid vivid blues and a deep muted blue, a light soft blue, mid
vivid cyan and teal alongside a mid soft teal, violet in both a mid vivid and a deep soft form,
indigo in a mid soft form, magenta in a light vivid and a light soft form, mid vivid green with
a mid soft lime, and orange in a mid vivid, a light vivid and a light amber form. A generator's
defaults draw from that range, so a visitor who touches nothing still sees a graphic worth
keeping. None of those colours appears in the chrome: the interface stays neutral so that the
range above is judged on its own, which is the whole point of the ground rule stated above.

### Type

One neutral sans carries the whole interface. A monospace is reserved for identifiers and for
values that must be compared or copied: a preset's derived address, an object key, a parameter's
current reading. Nothing else is monospace, and that restriction is what makes the monospace mean
"this is an exact value" rather than "this is styled". Figures align in a column wherever values
stack, which in this product means the control panel and the gallery's fork counts. A heading and
body copy differ enough in weight and size to read as two kinds of information at a glance.

### Calibration, which is what the controls are for

`calibrated` governs every control. Each one reports its own current value, in the monospace
face, positioned so the reading does not move as the value changes. A control whose value cannot
be read back is a defect. The panel groups controls under quiet headings, and each group can be
collapsed so a long panel stays navigable.

The save surface shows the address the current settings derive to before anything is saved, and
labels it as derived from the settings, because that is the product's central promise made
visible. The same settings always produce the same graphic, and the interface states this rather
than implying it.

### Motion

`eased` governs everything that moves. One speed and one easing across the whole product, quick
enough not to be waited for and slow enough to be seen, settling at the end rather than starting
sharply. Nothing uses a different speed to feel special.

The one deliberate exception is the preview: it redraws on the frame after a control moves,
undrawn and unanimated. A redraw that eases lies about what the control did, because it shows a
state being approached rather than the state the settings are actually in. A tile lifts slightly
toward the pointer and returns on the shared speed. A panel that opens or closes eases its height
rather than jumping, so the page never appears to reflow at random. The copy action confirms by
changing its own label, holding it long enough to read, then returning; nothing else moves to
announce it.

### Accessibility

Body text and every control label clear the WCAG AA contrast floor against whichever ground sits
behind them, and large text clears the large-text floor. Every control is reachable by keyboard
navigation in the order it reads on the page, and a slider is adjustable by arrow key and reports
its value as text rather than as position alone. The focus indicator is visible against all three
grounds named above, not only the lightest. A reader who has asked their system to reduce motion
gets the whole product with every transition removed and every element arriving in its final
state. Unavailable is never signalled by colour alone. The graphic itself carries a text
description naming the tool that made it.

### The surfaces

**The rail.** Persistent on every route, it carries the wordmark, the tool groups, the gallery,
and, when signed in, the author's own presets and their handle. It does not scroll with the page.
On a narrow viewport it collapses to a single control that opens it as a full-height panel.

**The tile grid.** The product's front door and its only navigation, repeated at the foot of
every route. Its ordering is the stored position of each tool, so the grid reads the same on
every route and a retired tool leaves no gap. Cards carry the tool name and its one-line
description and nothing else. One column
on a phone, two on a tablet and four on a wide screen, with a gap that never collapses and a
layout that holds at every width between. The whole card is the link target.

**The generator route.** The preview sits above the controls at every width. The action to copy
and the action to export stay reachable at any scroll position, because getting the graphic out
is the only job most visitors have. Below the tool sit its about block and then the grid.

**The save route.** A single column: the derived address, a title field, a visibility choice with
its three options each explained in one line, and the primary action. The unlisted option's
explanation says plainly that the address is shareable rather than secret.

**The gallery.** A grid of entries, each showing its rendered thumbnail, its title, its
publisher's handle and its fork count. An entry that has a parent names it. The filter by tool is
a row of the tool names, not a dropdown, because the set is small and visible beats hidden.

**The publish confirmation.** A full page, not a notice. It fills the viewport, names the entry's
address, states that publication is attributable and one-way, and offers the entry and the
gallery as the two ways onward. It does not disappear on its own.

### Components and their states

One primary action style and one quieter alternative. The primary carries the accent and the
strongest contrast in the interface; the quieter one carries neither. Both have resting,
pointed-at, pressed, focused and unavailable states. Every field has resting, focused, filled,
invalid and disabled states, and an invalid field says what is wrong beneath it in words rather
than only changing colour.

### Responsive

The layout holds from a narrow phone viewport to a wide desktop, and must survive every width
between rather than only at the breakpoints you pick. Where those fall is yours. The narrow
layout carries every control the wide layout carries; nothing is hidden to make it fit, because a
control that disappears at a width makes the tool unusable there rather than merely smaller.

At a narrow viewport nothing overflows sideways: no surface in the product scrolls horizontally,
and the preview scales to the column rather than pushing it. Every navigation target stays
reachable there, which includes the rail behind its single control and every tile in the grid.

### What it must not look like

Not a marketing page. Not a page whose chrome competes with its own output. Not decoration
standing in for content. Not a layout borrowed from a subject unrelated to this one.

## Technical requirements

The application is server-rendered with progressive enhancement. Every route arrives as a
complete document. The generator route is then enhanced on the client so a control change redraws
the preview locally. With scripting unavailable the route still works through ordinary form
submission and the server draws the preview.

- Frontend: vanilla progressive enhancement, no framework.
- Backend: Express with Nunjucks templates, serving the documents and one JSON API under the
  `/api` prefix on the same origin.
- Datastore: PostgreSQL, reached through `DATABASE_URL`.
- Object store: MinIO, reached through `STORAGE_ENDPOINT`, `STORAGE_BUCKET`,
  `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The bucket is private.
- Further environment: `AUTH_SECRET`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`.

Both PostgreSQL and MinIO are already running and reachable at those variables.

The drawing core is one module loaded by both the browser and the server, because the same
settings must produce the same bytes in both places.

The API surface:

| Method and path | Purpose | Auth |
|---|---|---|
| `POST /api/auth/login` | Sign in, returns `access_token` | none |
| `GET /api/session` | The current account | token |
| `GET /api/health` | Readiness | none |
| `GET /api/generators` | The seeded tiles in stored order | none |
| `GET /api/generators/{key}` | One generator and its schema | none |
| `GET /api/gallery` | Published entries, newest first | none |
| `GET /api/gallery/{presetId}` | One entry with its lineage | none |
| `GET /api/presets/{id}` | One preset, subject to visibility | none |
| `GET /api/presets/{id}/render` | The rendered export bytes | none for public |
| `POST /api/reports` | Report an entry | none |
| `GET /api/studio/presets` | The caller's own presets | `author` |
| `POST /api/presets` | Save settings as a preset | `author` |
| `PATCH /api/presets/{id}` | Change title or visibility | `author` |
| `DELETE /api/presets/{id}` | Tombstone a preset | `author` |
| `POST /api/presets/{id}/render` | Render into the object store | `author` |
| `POST /api/presets/{id}/fork` | Fork a readable preset | `author` |
| `POST /api/presets/{id}/publish` | Publish an owned preset | `author` |

Outcomes are reported as: `200` for a read, `201` for a creation, `400` for a malformed or
invalid body, `401` for a missing, expired or bad token, `403` for a caller who is authenticated
but not entitled, `404` for an identifier that is unknown or not visible to this caller, `409`
for a conflict, `413` for a payload above its cap, and `415` for an unsupported format. A preset
the caller may not see returns `404` and nothing else, so it is indistinguishable from an
identifier that was never created.

The application serves a production build on the container-internal port `4173`, bound to
`0.0.0.0`. Every dependency installs at image build time; there is no network at run time.

## Data model

Seven tables. All timestamps are UTC. **Every table carries its own `id`, the child table
included**, with no exceptions.

`accounts`: `id`, `email` unique, `handle` unique, `display_name`, `role` one of `author` or
`reader`, `password_hash`, `created_at`. Three seeded rows as listed under User roles.

`generators`: `id`, `key` unique, `title`, `blurb`, `kind` one of `generator`, `colour` or
`document`, `status` one of `live` or `retired`, `position`, `param_schema` nullable,
`created_at`. Twenty-four seeded rows, read-only, in this order:

| Position | Key | Blurb | Kind | Status |
|---|---|---|---|---|
| 1 | `pppick` | color picker | `colour` | `live` |
| 2 | `mmmingle` | color palette generator | `colour` | `live` |
| 3 | `bbblob` | SVG blobs | `generator` | `live` |
| 4 | `wwwave` | SVG wave generator | `generator` | `live` |
| 5 | `gggrid` | SVG grid patterns | `generator` | `live` |
| 6 | `ffflow` | fluid SVG gradients | `generator` | `live` |
| 7 | `rrripple` | make some SVG ripples | `generator` | `live` |
| 8 | `gggrit` | noise texture generator | `generator` | `live` |
| 9 | `Style Selectors` | A Visual Guide | `document` | `live` |
| 10 | `Vector Spinners` | How to make them | `document` | `live` |
| 11 | `tttile` | repeating SVG shapes | `generator` | `live` |
| 12 | `aaambient` | abstract backgrounds | `generator` | `live` |
| 13 | `iiisogrid` | isometric SVG patterns | `generator` | `live` |
| 14 | `ggglow` | glowing SVG shapes | `generator` | `live` |
| 15 | `qqquilt` | generative patterns | `generator` | `live` |
| 16 | `mmmesh` | mesh-like gradients | `generator` | `live` |
| 17 | `cccurve` | curvy line patterns | `generator` | `live` |
| 18 | `hhhelix` | SVG spiral patterns | `generator` | `live` |
| 19 | `ooorbit` | SVG gradient circle patterns | `generator` | `live` |
| 20 | `bbbeam` | bursting line patterns | `generator` | `live` |
| 21 | `mmmaze` | grid pattern generator | `generator` | `live` |
| 22 | `ssspark` | star SVGs | `generator` | `live` |
| 23 | `cccheer` | confetti generator | `generator` | `live` |
| 24 | `vvvanish` | shapes that vanish | `generator` | `retired` |

The six carrying a real `param_schema` are `bbblob`, `wwwave`, `gggrid`, `ffflow`, `rrripple` and
`gggrit`. Their parameter keys, in schema order, are:

| Key | Parameters in schema order |
|---|---|
| `bbblob` | `complexity`, `contrast`, `edges`, `fill` |
| `wwwave` | `amplitude`, `frequency`, `layers`, `fill` |
| `gggrid` | `columns`, `rows`, `thickness`, `stroke` |
| `ffflow` | `stops`, `angle`, `blur`, `palette` |
| `rrripple` | `rings`, `spacing`, `falloff`, `stroke` |
| `gggrit` | `density`, `scale`, `opacity`, `tint` |

`presets`: `id` nineteen characters and derived, `generator_key` referencing `generators.key`,
`generator_version`, `params`, `seed`, `ratio`, `width`, `height`, `title` nullable, `owner_id`
referencing `accounts`, `parent_id` nullable referencing `presets`, `visibility` one of `private`,
`unlisted` or `public`, `state` one of `live` or `tombstoned`, `fork_count`, `created_at`.

Four seeded rows, every one owned by a seeded author: two `public` and published, titled
`Soft four-lobe` on `bbblob` and `Three-layer crest` on `wwwave`; one `unlisted` titled
`Tight rule grid` on `gggrid`; one `private` titled `Dawn wash` on `ffflow`. Each seeded
identifier is the derivation of that row's own settings.

`renders`: `id`, `preset_id` referencing `presets`, `object_key`, `format` one of `svg` or `png`,
`width`, `height`, `byte_size`, `created_at`.

`gallery_entries`: `id`, `preset_id` unique referencing `presets`, `published_by` referencing
`accounts`, `published_at`, `title`, `thumbnail_object_key` nullable, `state` one of `live`,
`limited` or `removed`, `report_count`. Two seeded rows, both `live`.

`gallery_entry_tags`: `id`, `gallery_entry_id` referencing `gallery_entries`, `tag`, `position`.
Read back in `position` order, at most eight rows per entry.

`reports`: `id`, `gallery_entry_id` referencing `gallery_entries`, `reporter_id` nullable
referencing `accounts`, `reason` one of `spam`, `infringement` or `offensive`, `note` nullable,
`created_at`. Not seeded.

Invariants that must hold in the stored data rather than only in the code that writes it:

- A preset's identifier equals the derivation of its own settings, so two identical saves are one
  row whatever order they arrive in.
- A generator key is unique, and a retired generator keeps its route, its schema and its presets.
- At most one gallery entry exists for a preset.
- An object key is the digest of that object's own bytes, so two identical renders are one
  object, and a key that names no object in the bucket is a defect.
- A preset with forks is never removed from the lineage: its row is tombstoned, its parameters
  retained, its parent link retained, its title and owner cleared.
- A preset's `fork_count` equals the number of live presets naming it as parent.
- No column in any table holds image bytes.

## Constraints

- Single tenancy. One catalogue of tools and one gallery.
- No public signup, no password reset, no invitation, no account deletion.
- No comments, no likes, no follows, no messaging and no social graph of any kind.
- No payment. No email. Nothing is ever sent anywhere.
- No near-duplicate clustering, no ranking score and no account standing.
- No real-time collaboration and no shared editing session.
- No public generation API, no keys, no quotas and no metering.
- No workspaces and no team membership. A preset is owned by one account.
- No collections and no curated feeds beyond newest first and filter by tool.
- No moderation queue and no review decisions. A report is stored and counted, nothing more.
- No print-resolution rendering, no colour vision simulation and no print gamut work.
- No upload of any kind. Every graphic in the product is generated from parameters.
- No format other than the two named above may be rendered or stored.
- No stateless permalink. A preset is shared by its stored address, never by packing the whole
  parameter set into the address itself.
- No history of earlier parameter sets. A generator holds the settings it has now, and a
  visitor who wants an earlier result reaches it through a saved preset.
- No randomize control. Every value a generator holds was put there by the visitor or came from
  the seeded defaults.
- No conversion tracking, no analytics and no measurement of how long a page is.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses.
  Read both from the environment; never hardcode either.
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
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

## Definition of done

- A signed-out visitor opens `/`, sees the twenty-three live tiles in stored order with
  `vvvanish` absent, opens `bbblob`, drags a control, watches the preview redraw without a page
  load, and copies the markup.
- The canonical string in the worked example derives to `iiancd7svxmz3dbmqqk`, and saving those
  settings twice leaves one preset row carrying that identifier.
- Two simultaneous saves of identical settings leave exactly one row, and both callers receive
  the same identifier.
- A `private` preset is absent from the gallery, returns not found at its own address to a
  signed-out visitor, to `visitor@vvvivid.tools` and to a second author, and refuses its export
  identically to all three, while its owner reads both.
- An `unlisted` preset resolves at its address for any caller holding it and is absent from the
  gallery, and the interface describes that address as shareable rather than secret.
- A render writes an object into the bucket at `renders/{sha256_of_bytes}.{ext}`; two presets
  rendering identical bytes share one object; a render above `4194304` bytes and a format outside
  `svg` and `png` each write no object.
- Publishing requires an account and a title, produces one entry, and publishing twice returns
  the entry that already exists.
- A fork records exactly one parent and raises the parent's stored fork count by exactly one.
- Deleting a forked preset tombstones it, and its child still resolves its ancestry through it.
- `visitor@vvvivid.tools` is denied by the server at every author-only endpoint called directly,
  and no row changes.
- An author is denied when publishing, editing, deleting or rendering a preset another account
  owns, and the row does not change.
- Every route renders inside the same shell, and no route reaches a blank page or an unstyled
  error.
- The interface reads as `clinical-precision`: a neutral chrome carrying no saturated colour
  except the primary action and the three meanings, one neutral sans with monospace reserved for
  identifiers and readings, and one `eased` speed everywhere except the preview redraw, which is
  not animated.
- Reduced-motion visitors get the whole product with every transition removed.
- Contrast clears WCAG AA on body text and labels against every ground, every control is
  reachable and visibly focused under keyboard navigation, and a slider reports its value as
  text.
- The layout holds at every viewport width from a narrow phone to a wide desktop, and the narrow
  layout carries every control the wide layout carries.
