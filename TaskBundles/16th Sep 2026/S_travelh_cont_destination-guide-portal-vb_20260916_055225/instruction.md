# Destination Guide Portal

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser and read the published guide
entry for a place, see its photographs, and download a regional guide document, without hitting an
error page. A different stranger must NOT be able to reach the one entry an editor is still
working on, by any means: not from the index, not from a themed collection, not from the photo
gallery, not from the brochure library, not at the entry's own address, and not by asking the app
for the bytes of a picture attached to it. The uploaded pictures and documents must live in the
object store at their scheme's key; a copy on the app's own disk does not count, and a database
column holding the bytes does not count either.

## Overview

`Marnavel Coast Board` promotes the region `Marnavel` and publishes its guide to the places worth
visiting there. This product is that guide, and the private desk its editors write it from.

A visitor arrives with no account and never needs one. They browse places as a flat index or
through three themed collections, open a place and read its guide entry with a gallery attached,
scan a calendar of what is on, download a regional guide document, and look through every
photograph in one gallery surface. An editor signs in at a separate address, writes an entry,
uploads its pictures and its guide document, and either publishes it into the guide or holds it as
a draft.

The product deliberately is not a booking business. There is no reservation, no ticket, no
payment, no price and no availability. There are no visitor accounts, so no comments, no ratings,
no favourites and no saved trips. There is no email of any kind, no search service, no
translation and no second board.

The genuinely hard part is that an unfinished entry has to be invisible to the public along every
route that exists, including a direct request for the bytes of a picture attached to it, and it
has to become invisible again the moment a live entry is returned to draft.

## User roles

| Role | Can do |
|---|---|
| `visitor` | Read every published entry, every themed collection, the events calendar, the brochure library and the photo gallery. Holds no account and signs in nowhere. **Cannot see an entry in state `draft` on any public surface, at its own address, or through the bytes of its pictures or its guide document. Cannot reach any desk address. Cannot make any public response return a draft, with any query string.** |
| `editor` | Sign in at the desk. Read every entry in both states. Create an entry, edit it, attach pictures with a description each, attach a guide document, publish it and return it to draft. **Cannot create an entry that is already published in one call. Cannot publish an entry that fails any of the five publish conditions. Cannot create, rename or delete a themed collection. Cannot create or edit an event. Cannot reach any desk address without a valid token.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `visitor` session to any `editor`-only endpoint must
be rejected by the server (an unauthorized request is denied, not served), leaving the protected
state unchanged.

Signup is closed. A `visitor` holds no account, so there is nothing for one to sign up for, and
the desk has no registration form or endpoint. One editor account is seeded:

| Account | Password |
|---|---|
| `editor@example.com` | `deku-demo-pw-2026` |

## Core features

### Draft invisibility, and the bytes behind it

An entry is either `published` or `draft`, lowercase, and the public side reads published data
only. That filter is applied once, in the data layer, rather than separately on each surface that
displays an entry.

1. A `draft` entry is absent from the place index response, from every themed collection response,
   from the photo gallery response and from the brochure library response. No query string on any
   public endpoint makes a public response carry a draft; there is no state parameter.
2. Requesting the address of a `draft` entry answers `404` and renders the not-found surface. It
   does not answer `403`, because the existence of a draft is itself not public.
3. Every picture and every guide document is fetched through the app, at
   `GET /api/media/images/{image_id}` and `GET /api/media/brochures/{brochure_id}`, and the app
   resolves the owning entry's state at the moment of the request. An object owned by a
   `published` entry resolves and returns its bytes. An object owned by a `draft` entry answers
   `404`. A regional guide document has no owning entry and always resolves.
4. The object store is not publicly readable, and an unguessable key is not access control: the
   key of a draft picture is visible to an editor on the desk, so the guard is the state check at
   request time, not the obscurity of the key.
5. Returning a `published` entry to `draft` reverses rules 1, 2 and 3 at once and from that
   moment, with no window in which the old answers are still served.

### Objects in the store

6. A picture uploaded through the desk exists as a real object in the store under
   `entries/<entry_id>/gallery/<sha256_of_bytes>.<ext>`, for example
   `entries/4/gallery/9f2a...d0.jpg`. A guide document attached to an entry is stored under
   `entries/<entry_id>/brochure/<sha256_of_bytes>.pdf` and a regional one under
   `regional/<brochure_id>/<sha256_of_bytes>.pdf`.
7. The bytes live in the store and nowhere else. Bytes on the app's own filesystem, bytes in a
   database column, and a picture the app serves from its own bundle are each a contract
   violation, however correct the page looks.
8. The picture count shown against an entry on the desk list equals the number of objects the
   store actually holds for that entry.
9. The file size on a guide document's card is read from the stored object's own metadata at the
   moment the card is rendered. It is never a figure an editor typed, because a typed figure
   drifts from the file the moment the file is replaced.

### The events calendar

10. The public events response carries an event only when its effective end date is today or
    later in UTC. Expiry is the server's own job: an event whose end date has passed is excluded
    from the response, and is not present in it at all.
11. Where an event carries no end date, its start date is its end date.
12. The boundary is the end of the day, not the instant of the start: an event whose end date is
    today is present for the whole of today.
13. Nobody edits an event to make this happen. There is no desk endpoint that creates, edits or
    deletes an event; the calendar's contents change because the day changed.

### The place index and a place entry

14. The index lists published entries only, paged at 24, and its count line reads the number of
    published entries.
15. The index filters on place name and on theme, and sorts by name ascending or by recently
    added. Every filter and sort choice is held in the query string, so a filtered view is a
    shareable address that survives a reload.
16. Where a filter matches nothing, the grid is replaced by one sentence and a control that clears
    the filter. It is never a blank region.
17. A place entry carries its guide text, its theme badges, a fact panel holding the nearest
    station, the best months to visit and a distance figure, a strip of every picture attached to
    it, and a related row of up to three other published entries sharing at least one theme,
    excluding itself, ordered by sort index ascending. Where fewer than three qualify, the row
    renders what exists.
18. A place slug is lowercase kebab, unique across both states, and may not be any of the
    eleven reserved top-level segments `desk`, `api`, `media`, `event`, `brochures`,
    `photo-gallery`, `collection`, `destination`, `privacy`, `terms` or `404`.

### Themed collections

19. There are exactly three themed collections, `Coastline`, `Highlands` and `Backwater`, seeded
    and fixed. No request creates, renames or deletes one. `/collection` is the index of the three:
    it carries one card per collection with its name, its standfirst and its published count, and
    it is where the `Themes` label in the header goes.
20. An entry carries zero to three collections. An entry carrying none appears in the index and in
    no collection.
21. A collection with no published entries renders its head and its editorial introduction and
    then one sentence in place of the grid. It answers `200`, not `404`, because a collection is a
    permanent part of the site while a place may never have existed.

### The brochure library and the photo gallery

22. The brochure library carries the guide documents of published entries plus the regional ones.
    A document attached to a `draft` entry is absent from it.
23. A guide document's card carries a cover generated from the document's own first page at upload
    time, its page count, and its file size in megabytes to one decimal place. The cover is not a
    separately uploaded picture, and the composer offers no field for one: the observable
    consequence is that a document registered with no picture of any kind still shows a cover,
    whose intrinsic ratio is the three by four the card declares.
24. Downloading a guide document delivers the stored object with a `Content-Disposition` of
    `attachment` and a filename derived from the document's title by lowercasing it, replacing each
    run of characters that are neither a letter nor a digit with one hyphen, and appending `.pdf`.
    So `Marnavel in Three Days` downloads as `marnavel-in-three-days.pdf`, and `The Coast Road` as
    `the-coast-road.pdf`.
25. The photo gallery carries every picture of every published entry in one surface, filterable by
    theme with the choice held in the query string, paged at 24 and extended by an explicit control
    at the foot of the grid rather than by scroll position.
26. Selecting a tile opens a lightbox carrying the picture, the place name and a link to that
    place's entry, with previous and next controls stepping through the filtered set and wrapping
    at both ends.

### The editor desk

27. `/desk/login` takes an email and a password. A failed sign-in states that the credentials did
    not match and does not distinguish an unknown address from a wrong password.
28. `/desk` lists every entry in both states, ordered by last edited descending, with columns for
    name, themes, state, picture count and last edited, a badge naming the state, and a filter
    across all, published and draft that carries the count for each. The picture count is carried
    as `picture_count` on each row of the response behind it, and the three filter counts come
    from `GET /api/desk/entries/counts` as the keys `all`, `published` and `draft`.
29. The composer is one form at two addresses, `/desk/entry/new` and `/desk/entry/<id>`. Its
    fields are name (required, 3 to 80 characters), slug (required), summary (required, up to 240
    characters), guide (required, up to 20000 characters), themes (zero to three), featured, sort
    index, nearest station (required, up to 80 characters), best months (required, up to 80
    characters), distance in kilometres (required, a positive integer), the picture set (zero to
    twenty) and one optional guide document.
30. The slug derives from the name while the editor has not touched it, and stops deriving the
    moment they edit it by hand, so renaming a published place does not silently move its address.
31. Validation runs on the server and is repeated on the client. A field failing validation is
    named in the refusal, and nothing is written. A draft may be saved incomplete: a create or an
    update accepts an empty `summary`, an empty `guide` and no picture at all, because those are
    refusals only at publish. A `name` outside 3 to 80 characters, a `summary` over 240 characters,
    and a slug that is malformed, already held by another entry or a reserved segment are refused
    at once. The slug rules are enforced on every write and again at publish: refusing the write
    or refusing the publish are both correct, so long as no second entry ever comes to hold a live
    address.
32. Every picture carries a required description. A picture with an empty description cannot be
    attached to a published entry.
33. The row comes into existence on the first `Save draft`, not on entering the composer: pressing
    `New entry` writes nothing, so `/desk` lists no entry until the editor saves one, and an upload
    target is issued only for an entry that already has an id. After that first save, further
    pictures may still be uploading when the editor saves again, and an entry may be saved as a
    draft with uploads still in flight. An upload that fails is
    retryable without re-selecting the file and without losing the rest of the form: the observable
    consequence is that the retry reuses the `object_key` the first attempt was issued, and the
    other fields still hold what the editor typed.

### Publish and return to draft

34. Every entry is created in state `draft`. There is no request that creates a `published` entry
    in one call.
35. Publishing is refused by the API, not merely by a disabled control, when any required field is
    empty, when the slug is already held by another entry in either state, when the slug is a
    reserved segment, when any upload is still in flight, or when any attached picture has an empty
    description. The refusal names which of the five conditions failed.
36. Publishing makes the entry appear on the index, in each of its collections, at its own
    address, in the photo gallery, and its guide document in the brochure library. Returning it to
    draft removes it from every one of those.

### The standing pages

37. A privacy page, reachable from the footer of every surface, states what the board records about
    a visitor and how long it is kept.
38. A terms page, reachable from the footer of every surface and from the desk sign-in card, states
    the conditions on using the guide and reusing its photographs.
39. Any unmatched path renders the board's own not-found surface, carrying the header, the footer,
    a heading, one sentence and a single control back to the home surface, and answers `404`.
40. Every internal link on every public surface resolves. No internal link answers `404`.

### Auth

41. `POST /api/auth/login` takes `{"email","password"}` and answers `{"access_token": "<token>"}`.
    The client sends that token on every desk request as an `Authorization: Bearer <token>`
    header, and every endpoint under `/api/desk/` requires it. `POST /api/auth/logout` ends the
    session and the token stops working.
42. A request with no token, a malformed token or an expired token is denied, and the entry it
    named is unchanged. A token expires 12 hours after it is issued.
43. Passwords are stored hashed, never in plain text. There is no password reset flow and no
    registration endpoint.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home: motion header, themed triptych, featured places, the next events, the guide promotion, the gallery teaser | none |
| `/destination` | Place index: sticky filter bar, card grid, count line | none |
| `/destination/<slug>` | Place entry: head still, guide text, fact panel, picture strip, related row | none |
| `/collection` | Themed collection index: one card per collection with its name, standfirst and published count | none |
| `/collection/<slug>` | Themed collection: head still, editorial introduction, filtered card grid | none |
| `/event` | Events calendar: month headings, event rows | none |
| `/brochures` | Brochure library: cover cards, page count, file size, download control | none |
| `/photo-gallery` | Photo gallery: masonry grid, theme filter, lightbox, show-more control | none |
| `/privacy` | Privacy page | none |
| `/terms` | Terms page | none |
| `/404` | Not-found surface, also rendered for any unmatched path | none |
| `/desk/login` | Editor sign-in card | none |
| `/desk` | Entry list, both states, with a count per state | editor |
| `/desk/entry/new` | Composer, empty | editor |
| `/desk/entry/<id>` | Composer, loaded | editor |

**Entry and redirects.** A signed-out request for `/desk`, `/desk/entry/new` or
`/desk/entry/<id>` lands on `/desk/login`. A successful sign-in lands on `/desk`. Signing out
returns to `/desk/login` and the desk address that was open is no longer reachable. A token that
expires part-way through an edit: the save is denied, the entry is unchanged, and the editor is
returned to `/desk/login` with the reason stated. A `visitor` has no entitled route to be wrong
about, because every public surface is open and the desk is the only closed one. Any unmatched
path renders the not-found surface. The address of a `draft` entry renders the not-found surface
too, and never a forbidden page.

**Journeys.** Each journey starts from the seeded state `## Data model` describes, so the counts
below are the seed's counts rather than the counts left by the journey before.

1. Open `/destination`. The count line reads `8 places`. Type `salt` into the name filter; the
   cards already on screen hold at half opacity rather than unmounting, and `Saltmere` is the
   result. Copy the address, reload it, and the same filter is still applied.
2. Open `/destination/alder-cove`. Read the guide text, read the fact panel's nearest station,
   best months and distance, drag the picture strip sideways, and follow one of the three related
   places.
3. Open `/event`. The month headings come from the data, so a month with nothing in it is not
   shown. `Highfen Harvest Fair` is present on its final day. `Penmara Kite Days` is absent.
4. Open `/brochures`. Read the page count and the file size on `Marnavel in Three Days`, press
   `Download`, and receive a file named after the guide rather than an identifier.
5. Open `/photo-gallery`. Narrow to `Coastline`, open a tile, step through the set with the arrow
   keys, close with the escape key, and find the keyboard focus back on the tile that was opened.
6. Open `/desk/login`. Submit `editor@example.com` with a wrong password: the card shivers once,
   both fields take the failure colour, and the message reads `Those details did not match. Try
   again.` without saying which half was wrong. Submit it again with `deku-demo-pw-2026` and land
   on `/desk`.
7. From `/desk` press `New entry`. Type `Ferrow Sands`; the web address fills itself in as
   `ferrow-sands`, which no entry holds. Edit the address by hand to `ferrow-sands-walks`, retype
   the name, and the address stays as edited. Fill the fact panel fields, then press `Save draft`,
   which creates the entry and puts it on `/desk`. Attach three pictures, giving each a
   description, attach the guide document, and press `Save draft` again.
8. With the summary field emptied, press `Publish`: the refusal reads `Fill in every required
   field before publishing.` Refill it, set the web address to `event`, and press `Publish`: the
   refusal reads `That web address is reserved. Choose another.`
9. Set the address back to `ferrow-sands-walks` and press `Publish`. The toast reads `Published. It
   is live now.` Signed out, `/destination/ferrow-sands-walks` now renders the entry and its three
   pictures load through the app.
10. From `/desk` press `Return to draft` on `Alder Cove`. Signed out, it is absent from
    `/destination`, absent from `/collection/coastline`, its pictures are absent from
    `/photo-gallery`, its own address answers not-found, and `Alder Cove on Foot` is gone from
    `/brochures`.

**States.** Every list has an empty state that says something: the index's cleared-filter
sentence, a collection's `Nothing is in this theme yet. It will fill up.`, the calendar's
`Nothing is scheduled just now. The places are still there.`, and the desk list's own line. Every
filtered request has an in-flight state, in which the existing cards hold at half opacity under
the sticky bar rather than unmounting and reflowing. Every upload shows determinate progress and
offers a retry that keeps the chosen file and the rest of the form. An error never takes a surface
down: the failed region is replaced by `Something went wrong at our end. Try again in a moment.`
and the rest of the page stays usable.

## UI/UX notes

North star: a visitor should understand, in the first moment, that somebody who knows this region
chose these places and can tell them when to go. The register is consumer editorial: the subject
is seen before the interface, photography leads, and the chrome is a pale frame around it. The
stance is **atmosphere over ornament** - the warmth comes from the imagery and from one accent
colour, never from decoration standing in for content. A working console would rationally hold the
opposite.

Palette by role. The page ground is a near-white neutral and section bands sit on a near-white
neutral one step down from it; the alternation between the two is the only separation between
bands, and no rules are drawn. Body text is a deep cool neutral, secondary body a deep neutral,
and metadata a mid cool neutral. Headings on a light ground take a near-black neutral. The footer
is the one dark region in the product, a deep neutral carrying white text. The primary accent is a
mid, vivid orange and it is the only thing wearing that colour: everything a visitor can act on
and everything currently selected takes it, and nothing else does. A secondary mid, vivid amber
carries the home eyebrow line and a badge fill. Inline links inside prose take a mid, vivid blue
and controls never do. Card and divider borders take a near-white neutral a shade below the
section ground; inputs and table rules take a near-white cool neutral. Failure is a mid, vivid red
and appears nowhere but a validation failure. Success is a deep, soft teal and appears nowhere but
the live badge and the publish confirmation. A draft badge is a mid, vivid amber fill with deep
cool neutral text on it. Two exclusivity rules hold: the orange accent is never body text on a
near-white ground, carrying borders, fills and text on the deep cool neutral only; and the light
cool neutral is placeholder and disabled text only, never something a visitor must read. The exact
shades are yours, so long as those two rules hold and every pairing carrying body text meets WCAG
AA contrast in the scheme you ship.

Type is two families and no more: `Playfair Display` for display headings, place titles, month
headings and guide subheadings, and `IBM Plex Sans Condensed` for body, navigation, metadata and
controls. Both come from a font service and no font file ships. Both carry a real fallback stack
and load so that the swap does not reflow a heading. Figures align wherever counts stack, on the
desk list and on the calendar.

Shape reads as one soft product radius on cards and inputs, tighter inside nested controls,
slightly softer on media tiles, a full pill on outline buttons, and a circle on close controls.
Density is spacious: the reading measure is generous and bands are separated by air rather than by
lines. The layout archetype is a top navigation bar, fixed and pale, present on every surface,
collapsing into a drawer that enters from the right over a dimmed page on the narrow tiers.

Motion character is eased: entrances are decelerating, exits accelerating, position changes
symmetric, and one long reveal on the home surface waits a beat and then glides in. Every state
change not otherwise named takes the product default. The named moments are the long reveal on the
home header text, a lift on a themed-collection card, a border warm on an event row, an inner zoom
on a media tile that scales the image and not its frame, a single sideways nudge on a field that
fails validation, a fade out on a leaving toast, a slide on the navigation drawer, and a ring that
fills with scroll progress. Under a reduced-motion preference every transition collapses to
effectively nothing, the header holds its poster frame instead of playing, and the nudge becomes a
static border change to the failure colour; nothing becomes unreachable, because nothing here is
carried by motion alone.

Components carry their states rather than only their resting look: a control shows resting,
pointed-at, pressed, focused and unavailable; a field carries its label above it with any failure
message directly beneath; anything that opens over the page closes on the escape key; and
unavailable is never signalled by colour alone. The amber is the product's warning colour as well
as its secondary accent, marking a state that is unfinished rather than wrong, which is why a draft
badge wears it where a validation failure wears the red.

Accessibility is graded, not aspirational. Every interactive element is reachable in document
order and the focus ring is never removed, only restyled. Document structure carries the meaning as
well: one first-level heading per surface, headings descending without skipping a level, and
landmarks for the banner, the navigation, the main region and the content information. Keyboard navigation works throughout the
lightbox, the drawer and the composer, each of which traps focus and hands it back on close. Every
content image carries alternative text taken from a required field on its upload, and the
decorative header motion layer carries an empty one. Touch targets are comfortably sized, icon-only
controls carry labels, and meaning is never carried by colour alone: a state badge carries its word
as well as its fill.

The product is responsive across five breakpoints. At a narrow viewport nothing overflows sideways,
every navigation target stays reachable behind the drawer, and rows of cards fold to a single
column. Commit to the light scheme and design it fully; a dark scheme is optional and is not part
of what is asked.

Design against these failures: a surface dominated by one hue family with no second signal; a band
rendered empty rather than omitted; a marketing composition where the working desk belongs; the
accent used for small text on a near-white ground; and a grid that grows on scroll, which puts the
footer out of reach for good.

## Technical requirements

Build the public surfaces as server-rendered pages: every public route arrives as HTML carrying
its content on first paint, and only the interactive parts hydrate over it as islands, so a
visitor on a slow connection reads the guide before any script has run. The frontend is `Nuxt 3`.
The HTTP API is `Fastify`, served on the same origin under the `/api` prefix. The datastore is
`PostgreSQL`. Object storage is `MinIO`. Authentication is implemented in the app: email and
password exchanged for a bearer token, passwords stored hashed. `GET /api/health` returns `200`
once the app is ready. Requests are logged as one structured line each to standard output,
carrying method, path and status; there is no log file and no log service.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing services
available in this environment are `PostgreSQL` and `MinIO`, and reaching for anything else is a
contract violation.

Read every connection value from the environment and never hardcode a host or a port:

| Variable | What it carries |
|---|---|
| `DATABASE_URL` | the `PostgreSQL` connection |
| `STORAGE_ENDPOINT` | the `MinIO` endpoint |
| `STORAGE_BUCKET` | the bucket every object is written into |
| `STORAGE_ACCESS_KEY` | the access key for that bucket |
| `STORAGE_SECRET_KEY` | the matching key value for that bucket |
| `APP_PUBLIC_URL` | the origin the app is reachable at |
| `APP_PUBLIC_PORT` | the port the outside world uses |

`PostgreSQL` and `MinIO` are already running and reachable at those variables. Do not download,
install, compile or start a copy of either.

**Object WRITES go straight to the store.** `POST /api/desk/uploads` answers with a scoped,
expiring target inside the compose network, the desk sends the bytes to that target, and the app is
told the resulting `object_key` afterwards. The app never carries the bytes of an upload through
itself.

**Object READS are mediated by the app, and that choice is part of the contract.** The bucket is
not publicly readable, and the app serves every picture and every guide document itself, resolving
the owning entry's state as it answers. The alternative shape - handing the browser a
time-limited link straight to the bucket - is not acceptable for a READ, because a link already issued
keeps working after an editor returns an entry to draft, and rule 5 of `## Core features` says
there is no such window.

**What must hold when two editors work at once.** Two simultaneous publish attempts naming the
same web address must not both succeed: exactly one entry ends up holding that address, the other
attempt is refused and names the collision, and no entry is left half-published. Saving the same
entry twice in a row leaves one entry, not two, and the second save is the state that stands.
Publishing an entry and then returning it to draft leaves that one entry row, in state `draft`,
rather than a second row beside it.

**Performance the product owes.** These are budgets, not aspirations. The home surface's largest
piece of content paints in under two and a half seconds on a fourth-generation mobile connection. No surface shifts its layout by more
than a tenth of a viewport as content arrives. An interaction paints its next frame in under two
hundred milliseconds. The compressed JavaScript the home surface delivers stays under 180KB, and
no more than three requests block first paint. The place index and the photo gallery each page at
24 records and neither loads its full set.

**Media weight is the product's largest risk, and three rules contain it.** The header motion
layer never blocks first paint: its poster frame is part of the initial response and the motion
begins after. Every still is responsive and lazy below the fold; only the header still and the
first row of cards load eagerly. No lossless still ships for a photographic image: photographic
content is delivered compressed, and a lossless format is used only for marks and diagrams.

## Data model

Seven tables, one per entity. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not
a secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

### editors

`id`, `email` (unique), `password_hash`. One seeded row: `editor@example.com`.

### collections

`id`, `slug` (unique), `name`, `standfirst`. Exactly three rows, seeded, and no request creates a
fourth: `coastline` / `Coastline`, `highlands` / `Highlands`, `backwater` / `Backwater`. The
`standfirst` is the one-sentence line the collection surface renders under its name.

### entries

`id`, `slug` (unique across both states, lowercase kebab, never a reserved segment), `name` (3 to
80 characters), `summary` (up to 240 characters), `guide` (up to 20000 characters), `state`
(`draft` or `published`, lowercase), `featured` (boolean), `sort_index` (integer),
`transport_point`, `best_months`, `distance_km` (integer), `created_at`, `updated_at`.

There is no owner column. The product has one editor role and every editor may edit every entry.

Derived on read rather than stored: the published count on the index head, the picture count on the
desk list, the file size on a guide document's card (read from the stored object itself, never a
column), the calendar's month headings, and a place's related row.

Invariants, each a property of the running app:

1. One entry holds a given `slug` at any time, across both states. A publish attempt whose slug is
   already held is refused and changes nothing, and this holds when two attempts arrive at once:
   exactly one wins.
2. An entry comes into existence in state `draft`. No request produces a `published` entry
   directly.
3. No public response carries an entry in state `draft`, under any query string.
4. A collection's public membership is exactly the published entries joined to it.

### entry_collections

`entry_id`, `collection_id`. Many to many, the pair unique, zero to three rows per entry.

### images

`id`, `entry_id`, `object_key`, `alt_text` (required, non-empty), `width` (intrinsic), `height`
(intrinsic), `position` (order within the entry's gallery). `width` and `height` are stored so a
still can reserve its space before it arrives.

### brochures

`id`, `entry_id` (null for a regional guide), `object_key`, `title`, `page_count` (read from the
document at upload). There is no `byte_size` column: the size is read from the stored object every
time a card is rendered, which is why it is listed as derived rather than stored.

### events

`id`, `entry_id` (the place it happens at), `name`, `description`, `starts_on` (date), `ends_on`
(date, nullable and then the start date is its end date).

### Seed data

Nine entries, eight `published` and one `draft`:

| name | slug | state | collections | featured | sort_index | pictures | guide document |
|---|---|---|---|---|---|---|---|
| `Alder Cove` | `alder-cove` | `published` | Coastline | yes | 1 | 3 | `Alder Cove on Foot` |
| `Thistle Bay` | `thistle-bay` | `published` | Coastline, Backwater | yes | 2 | 2 | none |
| `Rook Hollow` | `rook-hollow` | `published` | Highlands | yes | 3 | 2 | none |
| `Penmara` | `penmara` | `published` | Coastline | yes | 4 | 2 | none |
| `Glasswater` | `glasswater` | `published` | Backwater | yes | 5 | 2 | none |
| `Highfen` | `highfen` | `published` | Highlands | yes | 6 | 2 | none |
| `Saltmere` | `saltmere` | `published` | Coastline, Backwater | no | 7 | 2 | none |
| `Brindle Tor` | `brindle-tor` | `published` | Highlands | no | 8 | 2 | none |
| `Ossary Fen` | `ossary-fen` | `draft` | Backwater | no | 9 | 3 | `Ossary Fen in Winter` |

The fact panel of each seeded entry:

| name | transport_point | best_months | distance_km |
|---|---|---|---|
| `Alder Cove` | `Alder Halt` | `May to September` | 12 |
| `Thistle Bay` | `Thistle Bay Pier` | `June to August` | 28 |
| `Rook Hollow` | `Hollow Bridge` | `April to October` | 41 |
| `Penmara` | `Penmara Road` | `March to June` | 57 |
| `Glasswater` | `Glasswater Quay` | `May to October` | 33 |
| `Highfen` | `Highfen Cross` | `July to September` | 64 |
| `Saltmere` | `Saltmere Halt` | `April to September` | 19 |
| `Brindle Tor` | `Brindle Foot` | `May to August` | 72 |
| `Ossary Fen` | `Ossary Lane` | `September to November` | 46 |

`distance_km` is stored as the integer and rendered as that integer followed by a space and `km`,
so `Alder Cove` reads `12 km` in its fact panel.

That is 20 pictures in total, 17 on published entries and 3 on the draft, and every one carries a
non-empty description. Three regional guide documents carry no owning entry:
`Marnavel in Three Days`, `The Coast Road` and `Backwater Passages`.

Four events, dated relative to the app's first start in UTC:

| name | place | starts_on | ends_on | on the calendar |
|---|---|---|---|---|
| `Penmara Kite Days` | `Penmara` | today minus 12 | today minus 5 | no, it has ended |
| `Highfen Harvest Fair` | `Highfen` | today minus 1 | today | yes, for all of today |
| `Thistle Bay Regatta` | `Thistle Bay` | today plus 2 | none | yes |
| `Alder Lantern Nights` | `Alder Cove` | today plus 9 | today plus 11 | yes |

The already-ended event exists so the calendar has something to leave out. The event ending today
exists so the boundary is the end of the day. The event with no end date exists so the fallback
has a subject. The draft entry exists so every clause of draft invisibility has something to
refuse.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual specification in full. Nothing here overrides a rule stated above;
where a behaviour and a visual meet, the behaviour above governs.

### Colour tokens, by role

The palette is a small warm layer over a neutral base. Carried by role, family, tone and shade;
the exact values are yours, so long as the exclusivity rules in `## UI/UX notes` hold.

| Role | Colour |
|---|---|
| primary accent: hover target, active navigation label, warmed border | mid, vivid orange |
| secondary accent: home eyebrow, badge fill | mid, vivid amber |
| page ground | near-white neutral |
| section ground, card ground | near-white neutral, one step below the page |
| alternating band ground | near-white neutral, a hair off the section ground |
| card and divider border | near-white neutral, below the card ground |
| input border, table rule | near-white cool neutral |
| body text | deep cool neutral |
| secondary body text | deep neutral |
| captions, metadata | mid cool neutral |
| disabled text, placeholder text | light cool neutral |
| headings on a light ground | near-black neutral |
| footer ground | deep neutral |
| inline link | mid, vivid blue |
| validation failure | mid, vivid red |
| publish confirmation | deep, soft teal |
| draft badge | mid, vivid amber |

Two further values are normative where named: cards carry one soft drop shadow, offset downward
and blurred, dark at roughly a third opacity; and the divider rule is a hairline in a near-white
neutral.

### Type

Two families, both served from a font service, both loading so that the swap does not reflow.

| Family | Weights | Role | Fallback stack |
|---|---|---|---|
| `Playfair Display` | 500, 600 | display headings, place titles | `Georgia, "Times New Roman", serif` |
| `IBM Plex Sans Condensed` | 400, 500, 600 | body, navigation, metadata, controls | `system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif` |

Naming a hosted family is not an asset dependency. No font file ships.

The rendered scale, in descending order of use:

| Size | Weight | Line height | Role |
|---|---|---|---|
| 16px | 400 | 24px | body default |
| 18px | 400 | 27px | lead paragraph |
| 14px | 400 | 21px | metadata, captions |
| 14px | 700 | 14px | navigation label |
| 13px | 700 | 11.7px | eyebrow, badge |
| 16px | 400 | 32px | long form body |
| 20px | 600 | 24px | card title |
| 28px | 500 | 33.6px | section heading, top step |
| 26.74px | 500 | 32.088px | section heading, middle step |
| 23.14px | 500 | 27.768px | section heading, bottom step |
| 12px | 400 | 18px | footer fine print |

The three heading steps are one clamped rule, not three declarations.

### Radius

One product radius carries almost every corner: cards, inputs, buttons and the event row. A
tighter inner radius is used for nested controls sitting inside a card. A slightly softer media
radius is used on gallery tiles and the picture strip. Outline buttons and the floating scroll
control are full pills. Close buttons and social marks are circles.

### Layout and breakpoints

Five breakpoints, named `sm`, `md`, `lg`, `xl` and `xxl` in ascending order. The content column is
centred with a gutter that steps at each breakpoint. The grid is twelve columns.

### Elevation

Stacking order, back to front: in-flow content at the base; sticky section headers raised just
above it; the floating scroll-to-top control above those; the global header above that; then the
modal and drawer backdrop; the navigation drawer over the backdrop; the modal dialog over the
drawer; and the toast stack in front of everything.

### Iconography

Eleven inline vector marks, every one drawn from coordinates in the build. No icon font ships and
no icon is referenced as a file.

Interface marks: a **search** mark, one circle with a line for its handle. A **menu** mark, three
lines evenly spaced on the vertical. An **arrow** mark, one path plus one heavier line in the
accent orange, its rotation of two hundred and twenty-five degrees about the mark's own centre
baked into the drawn geometry rather than applied at run time. A **progress ring**, one unfilled
circular path whose circumference is driven by its dash offset, coupled so directly to scroll
position that it reads as tracking rather than as an animation.

Social marks: seven marks in the footer, rendered at the same square box and evenly spaced on the
horizontal, drawn at that one box size whatever each mark's own viewBox family is, so the two
families align optically on one baseline. They are decorative link targets, and each carries an
accessible name naming its destination network.

### Global chrome

**Header.** Fixed to the top of the viewport, spanning the full width, above everything but a
modal, the drawer and a toast. Its ground is a very shallow vertical lift between two near-white
neutrals, which reads as a flat near-white with a soft edge. Contents left to right: the wordmark,
the primary navigation, the search control; below the `lg` tier the menu mark takes the
navigation's place. The search control opens `/destination` with the name filter focused and empty;
it reaches no search service, because the name filter is the only search the product has. The primary navigation carries five labels at the navigation size and weight
in `IBM Plex Sans Condensed`. The active label takes the accent orange, and a label transitions
its colour gently rather than snapping.

**Navigation drawer.** Below the `lg` tier the navigation collapses into a drawer that enters from
the right, over a backdrop that fades to half opacity. It rests offscreen and travels on the
horizontal alone; nothing else about it moves.

**Footer.** The footer ground is the deep neutral with body text in white at the metadata size.
It carries four link columns, every link in them resolving to a route in the `## User flow` table:
**Places** holds `Places`, `Themes` and `Gallery`; **Plan** holds `What is on` and `Guides`;
**Board** holds `Privacy`; **Legal** holds `Terms`. The `Enquiries` string is the Board column's
heading over the enquiry address rather than a link of its own. It also carries the seven social
marks, the enquiry address at `visit@example.com`,
and a fine print line at the smallest size. A footer link moves from white to the accent orange on
hover, gently. The privacy page and the terms page are linked from one of those columns on every
surface.

**Not-found surface.** Carries the global header and footer, a heading at the top type step, one
sentence of explanation and a single pill button back to the home surface. It answers `404`. It is
reachable at `/404` and is rendered for any unmatched path.

**Accessibility control.** A persistent floating control, pinned to the viewport edge, opens a
panel offering at minimum a text size increase, a contrast inversion and a reset. Its state
survives navigation within a session. It is reachable by keyboard and is the first focusable
element in the document after the skip link. Its panel rows are pill-cornered and its content
blocks tighter; both carry a small offset shadow. On hover its label and border move from white to
a near-black neutral, including on the marks drawn before and after its label.

### Motion language

Four easing characters and no others: entrances are decelerating, exits accelerating, position
changes symmetric, and the long reveal decelerates over a longer travel after a held pause. A
gentle symmetric ease and a plain linear ramp are also permitted where named below.

The product default applies to any state change not otherwise specified: a short, gently
symmetric ease. Wherever a control changes state, three properties move together on that one ease
rather than one at a time: `color`, `background-color` and `border-color`. Named exceptions, as moments rather than durations:

- the **long reveal**: a held pause, then just under a second of decelerating travel. It is the
  entrance of the home surface's header content, and it is the only entrance in the product that
  waits.
- the **drawer slide** and the **toast entrance**: a short decelerating travel.
- the **backdrop fade** and the **still fade**: a short linear opacity ramp.
- the **ring fill**: a stroke-offset change so short it reads as direct coupling to scroll.
- the **nudge**: a field that fails validation moves on the horizontal - out one way, further
  back the other, a smaller correction, and home - firing once. It is the shape of a head shaking
  no.
- the **fade out**: a toast leaves by running its opacity to nothing.

No spinner, progress stripe or placeholder glow is required anywhere in the product. Where a
loading affordance is needed, one of the named moments above carries it: the index holds its cards
at half opacity, and an upload shows determinate progress.

Under a reduced-motion preference every transition duration collapses to effectively nothing, the
header motion layer does not autoplay and shows its poster frame, and the nudge is replaced by a
static border colour change to the failure red. Nothing becomes unreachable and no information is
lost.

**Scroll indicator.** A ring pinned bottom right, above the in-flow content and below the header,
carrying the progress-ring geometry. It rests slightly below its final position and lifts into
place on first scroll. Its stroke fills in proportion to document scroll progress, it carries a
soft two-part drop shadow, and pressing it returns to the top of the document.

### Media system

**Header media.** The home surface's header is a full-bleed motion panel occupying the viewport
below the header bar. Back to front: the motion layer, muted, looping, playing inline, with no
controls; a scrim running corner to corner from near-black to a softer dark, which is what lets
white lettering sit on it and stay readable; then the header content. The motion layer must not
block first paint. Its poster frame renders immediately and the motion begins only once it can
play through; on a connection where it cannot, the poster frame is the final state and nothing
appears broken.

**Progressive stills.** Every still loads behind a generated blur placeholder produced at build
time from the still's own average colour, never shipped. Each still is delivered at a minimum of
three widths with a size declaration matching the five breakpoints, and declares its intrinsic
width and height so that no layout shift occurs as it arrives.

**Media radius and framing.** Gallery tiles take the media radius; cards take the product radius.
A tile that zooms on hover scales its inner image only, never its frame, and its frame keeps its
clipping so the image cannot escape it.

**Detail strip.** A horizontal strip of stills beneath a place heading carries a soft inset shadow
along its top, which reads as an inner edge. It scrolls horizontally on touch and by drag on
pointer. Its scrollbar is hidden and its keyboard scrolling is not.

### Surface: home

`/`. Bands top to bottom: the header media panel; the header content; the themed collection
triptych; the featured places row; the upcoming events strip; the guide promotion; the gallery
teaser; the footer. The triptych, the events strip and the gallery teaser sit on the section
ground; the featured row and the guide promotion sit on the page ground. The alternation is the
only separation between them and no rules are drawn.

**Header content.** Set over the motion panel, left aligned, vertically centred, constrained to
seven twelfths of the grid at the `lg` tier and above and to the full column below it: an eyebrow
at the eyebrow size, weight and letter spacing in the secondary amber; the display heading at the
top type step in `Playfair Display` weight 500 in white; one lead sentence at the lead size in
white; and one pill button with a transparent ground, a hairline white border and a white label.
The three text elements enter on the long reveal, staggered in band order. The button does not
animate in: it is present from first paint so the surface is actionable before the entrance
completes. On hover the button inverts, taking a white ground and a deep cool neutral label.

**Themed collection triptych.** Three cards in a row at the `lg` tier and above, stacked below
`md`. Each carries a still, a title at the card-title size and a one-line description at the
metadata size in the mid cool neutral. Card ground is the page ground, at the product radius with
the card shadow. The three link to the three collection addresses. The set is fixed; a fourth
theme does not appear here. On hover a card lifts slightly on the vertical and its title takes the
accent orange.

**Featured places row.** Up to six place cards drawn from published entries flagged `featured`,
ordered by sort index ascending, four across at `xl`, three at `lg`, two at `md`, one below. Each
carries a still at the media radius, the place name at the card-title size, and its collection
name at the eyebrow size in the mid cool neutral. Where fewer than six entries carry the flag the
row renders what exists and does not pad. Where none do, the entire band is omitted rather than
rendered empty.

**Upcoming events strip.** The next four events by start date ascending, filtered to those whose
end date has not passed. Each carries a date block, the event name at the card-title size and a
place name at the metadata size in the mid cool neutral. A link at the strip foot leads to the
calendar. The filter is applied on the server: an event that has ended is not present in the
response at all, not merely hidden by the client.

**Guide promotion.** A two column band: a still on one side, and on the other a heading at the
middle type step, two sentences at the long-form body size and a pill button to the brochure
library.

**Gallery teaser.** Eight tiles in a masonry arrangement at the media radius, linking to the photo
gallery. Each tile applies the inner zoom.

### Surface: place index

`/destination`. **Head:** a breadcrumb at the metadata size, a heading at the top type step, and a
count line at the metadata size in the mid cool neutral reading the number of published entries.
Breadcrumb links take the secondary deep neutral and move to the accent orange on hover, gently.

**Filter bar:** sticky beneath the global header, above in-flow content. It carries a text field
filtering on place name, which settles before it runs rather than firing on every keystroke; a
theme selector offering `Coastline`, `Highlands`, `Backwater` and an all option; and a sort
selector offering name ascending and recently added. Ground is the page ground with a hairline
bottom border in the card border neutral. Fields take the product radius with a hairline input
border, and a focus ring as a soft wide halo in the inline-link blue.

**Grid:** place cards, three across at `xl`, two at `md`, one below. Each carries a still at the
media radius, the name at the card-title size, its themes as badges at the eyebrow size, and a
summary truncated to two lines at the metadata size.

**Empty and in-flight states:** where a filter matches nothing the grid is replaced by one
sentence and a control clearing the filter, never a blank region. While a filtered request is in
flight the existing cards hold at half opacity rather than unmounting, so the grid does not
collapse and reflow under the sticky bar.

No scroll-scrubbed animation exists anywhere in this product. The only scroll-coupled property is
the progress ring.

### Surface: place entry

`/destination/<slug>`. **Head:** a full width still at the top of the document, three fifths of
the viewport height, carrying the same scrim as the home header. Over it the place name at the top
type step in `Playfair Display` weight 600 in white, and its theme badges.

**Body:** two columns at the `lg` tier and above, a single column below. The main column takes
eight twelfths and carries the guide text at the long-form body size with subheadings at the
bottom type step in `Playfair Display` weight 500; paragraph spacing is one line height. The side
column takes four twelfths and is sticky at `lg` and above: a fact panel on the section ground at
the product radius carrying the nearest transport point, the best months to visit and a distance
figure, each as a label at the eyebrow size in the mid cool neutral above a value at the body size.

**Picture strip:** the horizontal still strip sits between the body and the related row and
carries every picture attached to the entry.

**Related row:** three cards drawn from other published entries sharing at least one theme,
excluding the current entry, ordered by sort index ascending. Where fewer than three qualify the row renders
what exists.

### Surface: themed collection index

`/collection`. The index of the three collections, and the destination of the `Themes` label in the
header. Head: breadcrumb, a heading at the top type step, one sentence of standfirst. Body: three
cards in a row at the `lg` tier and above, stacked below `md`, each carrying a still at the media
radius, the collection name at the card-title size, its standfirst at the metadata size in the mid
cool neutral, and its published count at the eyebrow size. A card lifts slightly on the vertical on
hover and its title takes the accent orange, exactly as the home triptych does. The set is fixed at
three, so this surface never renders an empty state.

### Surface: themed collection

`/collection/<slug>`. **Head:** a full width still at two fifths of the viewport height under the
same scrim, carrying the collection name at the top type step in white and a one-sentence
standfirst at the lead size. Breadcrumb links over the still take white and move to the accent
orange on hover.

**Body:** an editorial introduction of two to four paragraphs at the long-form body size in a
single centred column of six twelfths, followed by the place grid filtered to entries carrying
this collection. Cards here carry a border that moves from a near-white neutral to the accent
orange on hover, alongside the title colour change.

The three collections are fixed and seeded, not editor creatable. An entry may carry any number of
them, including none; an entry carrying none appears in the index and in no collection. A
collection with no published entries renders its head and its introduction and then one sentence
in place of the grid. It does not answer `404`, because the collection itself is a permanent part
of the site.

### Surface: events calendar

`/event`. **Head:** breadcrumb, heading at the top type step, and a count line reading the number
of upcoming events. The breadcrumb here sits over a dark ground: links take white and move to the
accent orange on hover.

**Month grouping:** events are grouped under month headings at the bottom type step in
`Playfair Display` weight 500. A month with no events is omitted; the sequence of headings is
derived from the data, not from the calendar. The month groups are real headings, so a screen
reader can jump between months.

**Event row:** a horizontal card at the product radius on the page ground with a hairline border.
Left, a fixed square date block on the section ground carrying the day numeral at the middle type
step in weight 600 and the month abbreviation at the eyebrow size in the mid cool neutral; where
an event spans days the block carries the start day and a range indicator. Centre, the event name
at the card-title size, the place name at the metadata size in the mid cool neutral, and a
description truncated to two lines at the metadata size. Right, a still at the product radius,
sized to about a sixth of the row at `lg` and above and omitted below `md`. On hover the row's
border and its name both take the accent orange.

**Empty state:** where no upcoming events exist the month grouping is replaced by one sentence and
a link to the place index. The head and its count line, reading zero, remain.

### Surface: brochure library

`/brochures`. **Head:** breadcrumb, heading at the top type step, and two sentences of standfirst
at the lead size in a column of eight twelfths.

**Grid:** brochure cards, four across at `xl`, three at `lg`, two at `md`, one below. Each card
carries a cover still at the product radius in a three-by-four aspect ratio, the title at the
card-title size, a metadata line at the eyebrow size in the mid cool neutral reading the page count
and the file size in megabytes to one decimal place, and a pill download control. The cover is
generated from the document's first page at upload time and is not a separately uploaded still.

### Surface: photo gallery

`/photo-gallery`. **Layout:** a masonry arrangement preserving each still's own aspect ratio, four
columns at `xl`, three at `lg`, two at `md`, one below, at one grid gutter at every breakpoint,
tiles at the media radius. Each tile applies the inner zoom on hover: the image scales, the frame
does not.

**Filter:** a theme selector matching the index's, offering the three collections and an all
option, with the choice held in the query string.

**Lightbox:** selecting a tile opens a modal over the backdrop. The still is fitted to the
viewport with a margin of one grid gutter. A caption bar carries the place name at the body size in
weight 700 and a link to that place's entry. Previous and next controls step through the filtered
set, wrapping at both ends. The close control is a circle at half opacity, rising to full on
hover. The modal traps focus, returns focus to the originating tile on close, closes on the escape
key and closes on a backdrop press; arrow keys step the set. The backdrop fades and the still
itself fades, both on the short linear ramp.

**Paging:** the grid loads 24 tiles and extends by 24 on demand through an explicit control at the
grid foot. It does not extend on scroll position, because an infinite grid makes the footer
unreachable.

### Surface: editor desk

Its chrome inherits the design system above and introduces no token of its own.

**Sign in.** `/desk/login`. A single centred card at the product radius on the page ground with the
card shadow, holding an email field, a password field and a submit control. A failed sign-in
applies the nudge to the card and sets both field borders to the failure red. The message states
that the credentials did not match and does not distinguish an unknown address from a wrong
password. Under reduced motion the nudge is replaced by the border change alone. The terms page is
linked from the foot of this card.

**Entry list.** `/desk`. A table of every entry in both states, ordered by last edited descending.
Columns: name, themes, state, picture count, last edited. The state cell carries a badge: live
takes the success teal with white text, draft takes the amber with deep cool neutral text. A
filter above the table switches between all, live and draft, and each control carries its count.

**Composer.** `/desk/entry/new` and `/desk/entry/<id>`: one form at two addresses.

| Field | Type | Rule |
|---|---|---|
| name | text | required, 3 to 80 characters |
| web address | text | required, lowercase kebab, unique, not a reserved segment |
| summary | text | required, up to 240 characters |
| guide | long text | required, up to 20000 characters |
| themes | multi select | zero to three, from the fixed set |
| featured | boolean | governs inclusion in the featured row |
| sort index | integer | governs ordering in the featured row and the related row |
| nearest station | text | required, up to 80 characters, rendered in the fact panel |
| best months | text | required, up to 80 characters, rendered in the fact panel |
| distance in kilometres | integer | required, positive, rendered in the fact panel as the integer followed by `km` |
| pictures | file set | zero to twenty images, each with a required description |
| guide document | file | optional, one document |

The web address field derives from the name on first entry and stops deriving once edited by hand,
so renaming a published place does not silently move its address. Validation runs on the server
and is repeated on the client; a field failing validation takes the nudge treatment.

**Upload.** Pictures and the guide document go to the object store, and the app holds the resulting
object identifiers. Each upload shows determinate progress. A failed upload is retryable without
re-selecting the file and without losing the rest of the form. An entry may be saved as a draft
with uploads still in flight; it may not be published until every upload has completed.

**Publish and unpublish.** Publishing makes the entry appear on the index, at its own address, in
its collections and in the gallery, its guide document in the brochure library, and on the home
surface only where the entry is flagged `featured`.
Unpublishing reverses every one of those, including the reachability of its stored bytes. Both are
confirmed by a toast.

### Shared components

The component architecture is nine shared modules and no more. Nine components carry the whole
surface set, each specified once above and referenced by the surfaces: the global header, the navigation drawer, the global footer, the place card, the media
tile, the filter bar, the pill button, the modal and the toast. The place card is the most reused
component on the public side: it takes one entry and a variant, and the variant governs only which
fields render, never its ground, radius, shadow or hover behaviour.

**Toast.** A stack pinned bottom right in front of everything, entering on a short decelerating
travel and leaving on the fade out. Success carries a left border in the success teal, failure in
the failure red. A toast dismisses after five seconds or on press. The stack holds at most three; a
fourth displaces the oldest. Toasts report the outcome of an editor action only, and nothing on the
public side raises one.

**Data boundaries.** The public surfaces read published data only, and that filter is applied in
the data layer rather than in any view. A view that receives an entry may assume it is publishable
and carries no state check of its own. This is deliberate: a check spread across seven views is a
check that will eventually be missed in one of them. The editor surfaces read both states through
a separate, authenticated path.

### Responsive behaviour

Column counts by surface:

| Surface | Below `md` | `md` | `lg` | `xl` |
|---|---|---|---|---|
| themed triptych | 1 | 3 | 3 | 3 |
| featured row | 1 | 2 | 3 | 4 |
| place grid and collection grid | 1 | 2 | 3 | 3 |
| brochure grid | 1 | 2 | 3 | 4 |
| gallery masonry | 1 | 2 | 3 | 4 |
| event row | stacked | stacked | horizontal | horizontal |

Three changes are structural rather than a reflow. The primary navigation becomes the drawer below
`lg`. The place entry's side column moves from sticky beside the body to inline beneath it below
`lg`. The event row's still is omitted below `md` - omitted, not hidden: it is absent from the
response, so no bytes are fetched for a still nobody will draw.

A reduced-motion preference carries more declarations than any width in this product, and that is
worth stating plainly: motion preference matters more here than any single breakpoint.

**Print.** A print stylesheet is supplied for the place entry surface alone: chrome removed, side
column inline, picture strip reduced to its first still, and link destinations printed after their
labels.

### Zero-asset substitution

No binary asset ships with the build. No photograph, no film, no icon file, no font file, no
compressed texture. Each class gets a procedural replacement.

**Motion header.** A generated loop, produced at build time and encoded once, or drawn live where
the runtime allows it: three horizontal bands of colour drifting at different rates behind a fourth
band of slow vertical gradient, with the grain overlay below. The farthest band is a light neutral,
the middle a light cool neutral, the nearest a near-white neutral, over a deep neutral ground.
Drift rates are chosen as coprime values so the composition does not visibly repeat. The scrim
sits over it unchanged, which is what makes this read as atmosphere rather than as a pattern. This
is honestly a stand-in for footage of a real place: it produces a moving, tonally correct backdrop
at the right weight and rhythm, and a board shipping to the public would replace it with real
footage without changing anything else here.

**Stills.** A generated gradient keyed by a seed derived from the entry slug, so the same entry
always produces the same still and the grid does not reshuffle its colours between builds: a
two-point radial gradient, the first point high and left in a palette colour, the second low and
right in a second palette colour, composited over a near-white neutral, with the grain overlay at
low opacity. Palette pairs cycle through light neutral with near-white neutral, light cool neutral
with near-white neutral, the secondary amber with the section ground, and light neutral with the
card border neutral. Intrinsic dimensions are declared and match the aspect ratio the surface
expects: three by two for cards, three by four for brochure covers, and the tile's own recorded
ratio for the gallery masonry.

**Grain.** An inline vector turbulence filter as a data URI, desaturated to remove its colour
speckle, composited at low opacity. At a few hundred pixels square it tiles without a visible seam
and adds the tonal variation that keeps a generated gradient from reading as a flat background.
The grain is the important part: without it these read as flat blocks of colour, and with it they
read as something photographic.

**Fonts.** No substitute is needed. Both families are served from a font service, which is not an
asset dependency; the build names the families and the fallback stacks and ships no font file.

**Guide documents.** Generated at seed time from the entry's own text: a cover carrying the place
name set in the display family, a contents page, and one page per picture description. Page count
and byte size are read from the generated document, so the metadata line is truthful about the
file the visitor actually receives.

### Copy

Every string the product ships. These are exact.

**Global chrome.**

| Key | String |
|---|---|
| navigation, places | `Places` |
| navigation, themes | `Themes` |
| navigation, events | `What is on` |
| navigation, brochures | `Guides` |
| navigation, gallery | `Gallery` |
| search label | `Search the guide` |
| menu label | `Open menu` |
| footer enquiries heading | `Enquiries` |
| footer address | `visit@example.com` |
| footer legal line | `Marnavel Coast Board. All rights reserved.` |
| footer social label | `Follow Marnavel Coast Board` |
| skip link | `Skip to content` |
| footer privacy link | `Privacy` |
| footer terms link | `Terms` |

**Home.**

| Key | String |
|---|---|
| eyebrow | `PLAN YOUR VISIT` |
| heading | `Take the long way through Marnavel` |
| lead | `Eight places worth the detour, and the best month to see each one.` |
| call to action | `Start exploring` |
| themes heading | `Three ways in` |
| featured heading | `Worth the detour` |
| events heading | `Coming up` |
| events call to action | `See the full calendar` |
| guide promotion heading | `Take the guide with you` |
| guide promotion body | `A printed companion to every place in this guide, with maps, seasons and the roads between them. Free to download, made to be folded.` |
| guide promotion call to action | `Download the guide` |
| gallery heading | `In pictures` |

**Place index and place entry.**

| Key | String |
|---|---|
| index heading | `Every place in the guide` |
| index count | `{n} places` |
| filter by name | `Filter by name` |
| filter by theme | `All themes` |
| sort by name | `Name, A to Z` |
| sort by recency | `Recently added` |
| index empty | `Nothing matches that. Try a different theme, or clear the filter.` |
| index empty control | `Clear filter` |
| fact label, transport | `Nearest station` |
| fact label, months | `Best months` |
| fact label, distance | `Distance` |
| related heading | `Nearby and alike` |

**Collections, events, brochures, gallery.**

| Key | String |
|---|---|
| collection index heading | `Three ways into Marnavel` |
| collection index standfirst | `Every place in the guide sits in one of these three, or in none of them.` |
| collection index count | `{n} places` |
| collection empty | `Nothing is in this theme yet. It will fill up.` |
| events heading | `What is on in Marnavel` |
| events count | `{n} coming up` |
| events empty | `Nothing is scheduled just now. The places are still there.` |
| events empty control | `Browse places` |
| events date range joiner | `to` |
| brochures heading | `Guides to download` |
| brochures lead | `Printed companions to the places in this guide. Each one folds to pocket size and needs no signal to read.` |
| brochures metadata | `{n} pages, {size} MB` |
| brochures control | `Download` |
| gallery heading | `Marnavel in pictures` |
| gallery show more | `Show more` |
| lightbox close | `Close` |
| lightbox previous | `Previous picture` |
| lightbox next | `Next picture` |
| lightbox link | `Read about this place` |

**Editor desk.**

| Key | String |
|---|---|
| sign-in heading | `Sign in to the desk` |
| sign-in submit | `Sign in` |
| sign-in failed | `Those details did not match. Try again.` |
| list heading | `Entries` |
| filter, all | `All` |
| filter, published | `Live` |
| filter, draft | `Draft` |
| badge, published | `Live` |
| badge, draft | `Draft` |
| new entry | `New entry` |
| field, name | `Place name` |
| field, slug | `Web address` |
| field, summary | `Summary` |
| field, guide | `The guide` |
| field, themes | `Themes, up to three` |
| field, featured | `Show on the front page` |
| field, gallery | `Pictures` |
| field, alternative text | `Describe this picture` |
| field, brochure | `Guide document` |
| save | `Save draft` |
| publish | `Publish` |
| unpublish | `Return to draft` |
| refusal, fields | `Fill in every required field before publishing.` |
| refusal, slug taken | `That web address is already taken.` |
| refusal, slug reserved | `That web address is reserved. Choose another.` |
| refusal, uploads | `Wait for the uploads to finish.` |
| refusal, description | `Describe every picture before publishing.` |
| toast, published | `Published. It is live now.` |
| toast, unpublished | `Returned to draft. It is no longer public.` |
| toast, saved | `Saved.` |

**Errors and standing pages.**

| Key | String |
|---|---|
| not-found heading | `We cannot find that page` |
| not-found body | `It may have moved, or it may never have been here. The guide is still where you left it.` |
| not-found control | `Back to the guide` |
| upload failed | `That upload did not finish. Try it again.` |
| generic failure | `Something went wrong at our end. Try again in a moment.` |
| privacy heading | `What we record` |
| terms heading | `Using the guide` |

## Constraints

- One board, one region, one language, one currency-free product. No tenancy, no second board, no
  translation.
- No booking, ticketing, payment, price, availability or reservation of any kind.
- No visitor accounts. No comments, ratings, favourites, itineraries or saved trips. No public
  signup, and no password reset.
- No editor-created collections: the three are seeded and fixed. No editor-created events: the
  calendar is seeded and the desk has no event endpoint.
- No second editor role, no approval step, no per-entry ownership.
- No email of any kind: no confirmation, no digest, no notification. No mail service is available.
- No search service, no full-text index, and no search beyond the index's name filter.
- No analytics collection, no consent banner, no cookie choice. The one third-party request the
  product makes at run time is the font service the two families are served from, named in
  `## Front-end specification`; nothing else leaves the origin.
- No native application, no offline mode, no background worker.
- No binary asset ships: every still, the header loop, every mark and both type families are
  procedural or hosted, per `## Front-end specification`.
- No scroll-scrubbed animation anywhere. The progress ring is the only scroll-coupled property.
- The app stays responsive with 9 entries, 20 pictures, 5 guide documents and 4 events, and must
  not degrade at ten times that: 90 entries, 200 pictures and 40 events.

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
| `GET /api/health` | none | `200` once ready |
| `GET /api/entries` | `?theme=<slug>&name=<text>&sort=name\|recent&page=<n>` | a top-level JSON array of published entries, paged at 24, each carrying `id`, `slug`, `name`, `summary`, `featured`, `sort_index`, `themes` and `images` |
| `GET /api/entries/{slug}` | none | one published entry with its `images`, `transport_point`, `best_months`, `distance_km`, `guide` and `related`; `404` when the entry is `draft` or absent |
| `GET /api/collections` | none | a top-level JSON array of the three collections, each carrying `slug`, `name`, `standfirst` and `published_count` |
| `GET /api/collections/{slug}` | none | one collection with its published entries; `200` with an empty entry list when it has none |
| `GET /api/events` | none | a top-level JSON array of events whose effective end date is today or later, ordered by `starts_on` ascending, each carrying `id`, `name`, `description`, `starts_on`, `ends_on` and the place name |
| `GET /api/brochures` | none | a top-level JSON array of the guide documents of published entries plus the regional ones, each carrying `id`, `title`, `page_count`, `byte_size` and the place name where there is one |
| `GET /api/images` | `?theme=<slug>&page=<n>` | a top-level JSON array of the pictures of published entries, paged at 24, each carrying `id`, `alt_text`, `width`, `height` and the owning place's `slug` and `name` |
| `GET /api/media/images/{image_id}` | none | the object's bytes; `404` when the owning entry is `draft` |
| `GET /api/media/brochures/{brochure_id}` | none | the document's bytes with `Content-Disposition: attachment` and a filename from the title; `404` when the owning entry is `draft` |
| `POST /api/auth/login` | `{"email","password"}` | `{"access_token": "<token>"}`; an unusable pair is rejected as a client error |
| `POST /api/auth/logout` | none | the token stops working |
| `GET /api/desk/entries` | `?state=all\|published\|draft` | a top-level JSON array of the entries the state filter selects, each carrying `id`, `slug`, `name`, `state`, `themes`, `picture_count` and `updated_at` |
| `GET /api/desk/entries/counts` | none | `{"all": <n>, "published": <n>, "draft": <n>}`, the three figures the desk list's filter controls render |
| `GET /api/desk/entries/{id}` | none | one entry in either state with its `images` and its `brochure` |
| `POST /api/desk/entries` | `{"name","slug","summary","guide","themes","featured","sort_index","transport_point","best_months","distance_km"}` | the created entry, always in state `draft` |
| `PATCH /api/desk/entries/{id}` | any subset of the create body | the updated entry |
| `POST /api/desk/entries/{id}/publish` | none | the entry in state `published`, or a refusal naming which of the five conditions failed |
| `POST /api/desk/entries/{id}/unpublish` | none | the entry in state `draft` |
| `POST /api/desk/uploads` | `{"entry_id","kind","filename","content_type"}` | `{"url","method","headers","object_key"}`: the scoped, expiring target the bytes are sent to, the method to send them with, any headers to send, and the `object_key` they will land at |
| `POST /api/desk/images` | `{"entry_id","object_key","alt_text","width","height","position"}` | the registered picture |
| `POST /api/desk/brochures` | `{"entry_id","object_key","title"}` | the registered document, with its `page_count` and `byte_size` read from the stored object |

None of the public endpoints accepts a state parameter. There is no query string that makes a
public endpoint return a draft. Every endpoint under `/api/desk/` requires the bearer token; a request without one is denied. An invalid or unauthorized call is
rejected as a client error, never with a server error and never as a silent success.

### No mocks

`MinIO` is the only place the uploaded bytes live. Each of the following is a contract violation,
however good the page looks: an in-memory pictures array; bytes written to the app container's
filesystem, whether under a public directory or a private one; bytes stored in a database column;
a picture the app serves from its own bundle rather than from the bucket; a file size an editor typed, or one
the app stored in a column instead of reading from the object as the card renders; and a
publicly-readable bucket with an unguessable key standing in for an access check.

The named provider is the fact - the app's UI and its own tables can only reflect what lives in
the provider, never substitute for it.

## Definition of done

A traveller can open the guide, narrow it to a theme, read a place's entry with its photographs,
see what is on this month, and download a regional guide document named after itself. The one
entry an editor has not finished is unreachable to a visitor everywhere, including the bytes of its
pictures, and becomes unreachable again the moment a live entry is returned to draft.
