# Meridian Instrument Portfolio Console

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser, steer
a single-canvas console between its five destinations, open a work dossier and send a
message, while the owner signs in, writes a new work entry, publishes it, reorders the
shelf and sees the public console rebuild around it, without hitting an error page. The
hard part is the publish boundary: an entry that is not published must appear in no
public read, its detail must answer as gone, and its generated preview image must not be
readable by a stranger even at its exact object key. The preview bytes must live as a
real object in the `minio` bucket at the key scheme this brief pins; a copy on the app
container's own disk does not count.

## Overview

Meridian is a portfolio console for one person. It presents a body of work as an
instrument reading rather than as a page: a black field, a single drawing surface at the
full window size, and five destinations arranged as a small diagram of labelled plates
joined by lines in the upper right corner. Choosing a plate replaces the contents of the
field with a different scene, and the diagram redraws itself into a new arrangement as it
goes. The document never reloads while a visitor steers it.

The public content is written by the owner. The owner signs in, writes each work entry
and its dossier, chooses the order the entries sit in on the shelf, publishes, and the
scene rebuilds from what they wrote. Visitors get the console and a message form whose
submissions land in an inbox only the owner can read. An editor can be invited to help
with the writing and can do everything except publish, reorder, delete and read a
message.

The genuinely hard part is that publishing is a boundary rather than a flag on a row.
An unpublished entry has to be absent from the single public read, absent from the card
row, absent from the paging indicator, answer as gone at its own detail path, and have
its generated preview object refused to a stranger, while keeping its shelf position so
that publishing it later puts it back where the owner left it rather than at the end.

What this product deliberately is not: there is no public sign-up, no search anywhere on
the public console, no comments, no likes, no follows, no notifications beyond one
count, no payment of any kind, and no recognition editor. The recognition rows and the
cities they are pinned to are seeded and read only in this release.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor, never signed in | Steer the console between all five destinations, open a published work dossier, read the recognition rows, send one message from the contact form | **Cannot see a draft entry, its dossier or its preview image. Cannot reach any `/studio` route. Cannot read any message.** |
| `editor` | Everything a visitor can, plus sign in, read every work entry including drafts, create an entry, edit an entry, edit the profile, change their own password | **Cannot publish or unpublish an entry. Cannot delete an entry. Cannot reorder the shelf. Cannot read, archive or delete a message. Cannot see the unread count at all, not even as a zero. Cannot read the page-view log. Cannot invite or remove an editor.** |
| `owner` | Everything an editor can, plus publish, unpublish, delete, reorder the shelf, read and archive and delete messages, read the page-view log, invite and remove an editor | **Cannot be deleted and cannot be demoted. Cannot remove themselves.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in
the UI is not authorization: a direct API call from an `editor` session to any
`owner`-only endpoint must be rejected by the server (an unauthorized request is denied,
not served), leaving the protected state unchanged.

The permission matrix above is the whole of it: there is no administrator above the
owner and no viewer below the editor, because a product with one real user does not need
five roles and every role that exists is a row in every table that follows. Every
permission in it is checked at the server on the request that performs the act, against
the role the session resolves to. The rail hiding an item and a tile being absent are
conveniences, not controls.

Exactly one account holds the `owner` role. There is no public sign-up form: an account
exists because the owner made it. Account creation is open to an invited address only,
and the invitee completes it themselves: the owner submits an address, a single-use
invitation is created, and following it lets the invitee choose their own password at
`/invite/<token>`, after which the account exists with the `editor` role. An invitation
is valid for seven days and can be used once. Removing an editor revokes every session
that account holds and leaves their entries in place with their authorship intact.

Seeded accounts, both with the password `deku-demo-pw-2026`:

| Address | Role | Display name |
|---|---|---|
| `owner@example.com` | `owner` | `Marlow Hendriks` |
| `editor@example.com` | `editor` | `Rowan Vale` |

## Core features

### The public console

The five destinations are `/` for home, `/product` for work, `/sketch` for studies,
`/award` for recognition and `/contact` for contact, plus one failure surface at
`/error`. Every one of them renders one drawing surface at the full window size.

1. `GET /api/console` returns the whole public payload in one read: the profile, the
   published work entries with their links, the published studies, the published
   recognitions and the cities. It requires no session. Every list in it is in shelf
   order. The console loads it once and a destination change makes no further request
   and does not reload the document.
2. The drawing surface survives every destination change without being rebuilt. Moving
   from `/` to `/product` and back leaves the same surface in place.
3. Each destination fills the field with its own scene. Home carries a portrait built
   from points, a drifting field of letters behind it, a biography panel at the upper
   left and three callout annotations pinned to points on the portrait. Work carries the
   work cards floating over a wireframe landscape with moving markers, their trails and
   a pulse ring travelling across the ground. Studies carries a contour field filling the
   whole frame with a selector at the bottom centre whose items are labelled `01`, `02`
   and `03`, zero-padded to two digits. Recognition carries a globe built from points
   with city markers, a target reticle and the dated rows at the right, each drawing an
   arc to the city it belongs to. Contact carries three oversized wire letters with a
   panel over them holding the message form.
4. Nothing on the public console scrolls, at any window size. A short window makes the
   interface larger rather than cropping it, up to a clamp.
5. The navigation diagram is the only navigation the public console has. It sits in the
   upper right, `Home` is the parent plate and `Product`, `Sketch`, `Award` and
   `Contact` hang off it, and the plates settle to different positions on every
   destination with the connector lines redrawing between them. The four child plates
   arrive twice as fast as the parent.
6. Alongside the drawing surface the app maintains a complete parallel structure that
   does not draw: every string the scene shows, in reading order, with correct heading
   levels, and every interactive thing in the scene as a real control with a real label.
   It sits immediately before the drawing surface, it is fully in the tab order, it is
   not hidden from assistive technology, and it is replaced entirely on a destination
   change. On `/` it carries the intro paragraphs, the heading `Biography`, the history
   rows and the three annotations. On `/product` it carries the heading `Work` and the
   entries as a list, each with its title, kind, year and summary. On `/sketch` it
   carries the heading `Studies` and the selector as a radio group with the current item
   marked. On `/award` it carries the heading `Recognition`, the rows with their year,
   body, rank and city, and a separate list of the cities. On `/contact` it carries the
   heading `Contact` and the form.
7. The wordmark reads `MARLOW HENDRIKS` at the upper left of every destination and the
   footer reads `COPYRIGHT 2026 MARLOW HENDRIKS. ALL RIGHTS RESERVED.` Both are present
   at every width.

### Accounts and sessions

8. `POST /api/auth/login` with a correct address in `email` and a correct password in
   `password` answers `200` with an `access_token` the caller sends afterwards as a
   bearer credential, and sets the browser's own opaque session cookie in the same
   response. Both carriers name one session, valid thirty days from issue, extended by
   any request inside that lifetime, and ended by fourteen days without one. The cookie
   cannot be read by scripts. Neither carrier holds a claim: every request resolves the
   session to an account and a role at the server, and nothing about who the caller is
   is read from the request body.
9. A wrong password, an unknown address and a disabled account are all answered
   identically, with the line `That did not match. Check both fields and try again.`
   Neither field is ever named as the wrong one.
10. Five consecutive failed sign-ins on one account lock it for fifteen minutes. A
    locked account is told so, with the time it unlocks, in the line
    `Too many attempts. Try again after <time>.` A sixth attempt during the lock is
    refused and does not extend the count.
11. A signed-out request for any `/studio` route is sent to `/sign-in` carrying the
    intended path, and a successful sign-in sends the visitor onward to it. The intended
    path is validated before it is followed: it must begin with exactly one solidus, must
    not begin with two, and must match a route this brief names. Anything else is
    discarded and the visitor lands on `/studio`.

### The work entry dossier

12. An entry carries a title of 1 to 120 characters after trimming, a kind of 0 to 60, a
    year of four digits from 1970 to 2026, a summary of 0 to 280, a body of 0 to 8000, a
    grid seed that is a whole number from 0 to 999999, a grid palette that is one of
    `neutral`, `blue` or `coral`, and zero to four links each with a label of 1 to 40 and
    an address that parses and begins with a secure scheme.
13. Every constraint above is refused inline on its own field, with nothing written, and
    with exactly these sentences: `Give the entry a title.` for a missing title,
    `Keep this under 60 characters.` for an over-long kind,
    `Use a four digit year up to 2026.` for a year outside the band,
    `Keep the summary under 280 characters.` for an over-long summary,
    `This is longer than the editor will keep.` for an over-long body,
    `Use a whole number up to 999999.` for a seed outside its band, and
    `Give this link a label and a secure address.` for a link missing either half or
    carrying an address that is not a secure scheme.
14. No submit control anywhere in this product is ever disabled. Pressing one with an
    invalid form shows every error at once rather than refusing to respond.
15. No form anywhere in this product is ever cleared by a failure. A rejection, a
    rate limit, an expired session and a server failure all leave every field exactly as
    the person left it.
16. Every write to an entry carries the version it was working from. A write from a
    version that is no longer current is refused rather than merged, and the person is
    told with the line `This changed somewhere else while you were working.` and offered
    the two controls `KEEP MINE` and `TAKE THEIRS`. An accepted write raises the version
    by one.

### Publish, unpublish and the preview object

17. Saving an entry does not make it public. `SAVE` writes the record with `published`
    false at the position at the end of the shelf. Publishing is a separate act and only
    an `owner` may perform it. The status banner after a save reads `Saved just now.`
18. Publishing an entry makes it appear in `GET /api/console` and in the card row at its
    shelf position, and the banner reads `Published. It is on the site now.`
    Unpublishing removes it from both, and the banner reads
    `Unpublished. It is off the site.`
19. A work entry that is not published must be absent from `GET /api/console`, absent
    from the card row, absent from the paging indicator, and its own detail path
    `GET /api/work/<id>` must answer as gone rather than as present or as a server
    failure. This holds for an entry that was never published and for one that was
    published and then unpublished while somebody was looking at it.
20. Each entry carries a preview image generated from its grid seed and its grid
    palette. The bytes are written to the object store as a real object under the key
    `previews/{entry_id}/{sha256_of_bytes}.png`, for example
    `previews/7/9f2a4c1de0b37a5c8e6f1042bb93d7150ac6e2418d9f30b7c5a2e64019d3f8ab.png`.
    The bytes live in the bucket and nowhere else: not on the app container's
    filesystem, not in a database column, not inlined into a response.
21. A published entry's preview image is readable by a stranger with no session. A draft
    entry's preview image is not readable by a stranger, at its exact key, by any means.
    An unauthenticated request for a draft entry's preview is denied, not served.
    Regenerating a preview from the same seed and the same palette produces the same
    bytes and therefore the same key.
22. Changing the grid seed or the grid palette regenerates the preview and the entry's
    key moves with it. The old object is no longer referenced by any entry.

### The shelf

23. `/studio/shelf` holds two ordered lists on one page: the work entries in the order
    they appear across the card row on `/product`, and the study set in the order the
    selector pages through on `/sketch`. Only an `owner` may reach it and only an `owner`
    may write an order.
24. A row moves with the pointer, dragged by a six-dot handle at its left, and it moves
    with the keyboard: focus the handle, press space to lift the row, move it with the
    up and down arrow keys, and press space again to commit or escape to cancel. Both
    paths are required and both write the same order. The keyboard path is normative
    rather than a fallback.
25. Committing an order writes every affected position in one transaction, and the
    banner reads `Order saved.` A partial order is never written: if any position in the
    payload names an entry that does not exist, or names one twice, the whole reorder is
    refused and the order that was already stored is what remains.
26. Positions are dense from zero and unique across every entry, published or not. An
    unpublished entry keeps its position and is skipped when the public list is built, so
    publishing it later puts it back exactly where the owner left it rather than at the
    end. Getting this wrong is the single most annoying defect this page can have.
27. Every visible two-digit position label re-settles into its new value when an order is
    committed, and the selector labels on `/sketch` follow the study order.

### The contact form and the inbox

28. The public form at `/contact` takes a name of 1 to 80 characters after trimming, an
    address of 1 to 254 characters containing exactly one at sign with something either
    side and no whitespace, and a message of 10 to 4000 characters after trimming.
    Their inline errors are exactly `Tell me what to call you.`,
    `That address will not reach you.` and `A few more words, please.`
29. A successful send answers with the created identifier, the banner settles in reading
    `Sent. I will read it.`, all three fields clear, and the control returns. A rejection
    leaves the fields as they are and the banner reads
    `That did not send. Your text is still here.`
30. The form carries a decoy field that must stay empty and a timestamp of when the form
    was built. A submission with the decoy field filled is refused, and a submission made
    less than two seconds after the form was built is refused. A body containing more
    than two addresses is refused. The same form submitted repeatedly in quick succession
    from one address is refused after the third message inside one hour. Every refusal
    writes no message and answers with the same shape a success would, differing only in
    the banner. There is no puzzle, no image challenge and no third-party gate.
31. A message is stored with the sender's name, the sender's address, the body, its state
    which is one of `unread`, `read` or `archived`, the route it was submitted from, and
    the moment it arrived. It lands in the inbox at `/studio/inbox`, newest first, and
    only an `owner` may read it.
32. A message is rendered as text, everywhere it appears, and nothing in it is ever made
    live. No markup is interpreted, no address becomes a link, no image loads, and
    nothing a stranger types can make a page do anything. Markup typed into a message
    body appears as the characters that were typed.
33. Opening a message marks it read after one second on screen, not on navigation, so
    opening the wrong row and leaving inside a second does not mark it. The controls on
    one message are `ARCHIVE`, `MARK UNREAD` and `DELETE`.

### The failure surface

34. There is one failure surface, at `/error`, and it takes a code and a message from the
    address. An unknown address anywhere in the product renders it showing
    `404 NOT FOUND` with the control `RETURN HOME`, and answers as not found rather than
    as success.
35. The code and the message are matched against a closed table before anything is
    rendered, and the address is never echoed back:

    | Code | Message | Action |
    |---|---|---|
    | `404` | `NOT FOUND` | `RETURN HOME` |
    | `403` | `NOT PERMITTED` | `BACK TO WORK` |
    | `410` | `NO LONGER HERE` | `RETURN HOME` |
    | `429` | `TOO MANY REQUESTS` | `RETURN HOME` |
    | `500` | `SOMETHING BROKE` | `RETURN HOME` |
    | `OOPS!` | `APP CRASHED!!` | `RELOAD` |

    Anything outside the table renders as `500 SOMETHING BROKE`. A visitor asking for
    `/error?code=999&message=NONSENSE` sees `500 SOMETHING BROKE` and does not see
    `NONSENSE` anywhere.
36. An `editor` reaching an `owner`-only surface gets this surface at `403 NOT PERMITTED`
    on the owner shell, with the explanation `Messages are visible to the owner only.`
    where the refusal is the inbox, the control `BACK TO WORK` going to `/studio/work`,
    and the rail still present with the refused item absent from it. A refusal is a
    screen somebody designed, not a bare status with nothing behind it. An `editor`
    never sees the unread count at any value, including zero: the tile is absent rather
    than empty, because a zero is still an answer to a question they are not allowed to
    ask.

### Loading and first entry

38. A first arrival at any public destination shows the loading surface before the scene:
    a progress counter reading three digits and a percent sign, two concentric rings, and
    a label. The counter's digits are set on a fixed pitch so the readout does not shift
    as the number climbs, and it is drawn in two layers offset from one another in depth.
39. The handover from the loading surface to the scene is a fade rather than a swap: the
    counter reaches its maximum, the loading surface fades out and the scene fades in, and
    the navigation diagram and the footer are the last things to appear.
40. The minimum display rule holds for the loading surface and for every placeholder in
    the product: three tenths of a second to fade in, at least half a second on screen,
    three tenths to fade out. A surface that resolves faster than that still shows, so a
    fast connection does not produce a flash.

### The page-view log

37. Every view of a public destination is recorded with the route it was and the moment
    it happened. The owner reads the log at `/studio/log` and at
    `GET /api/studio/page-views`, newest first. No page view record carries a full
    network address and nothing in the log follows one person between two views. An
    `editor` requesting the log is denied.

### The voice of every string

41. Every sentence the product says is one of the sentences this brief pins, and no
    surface invents its own. Five rules govern them: second person for an instruction and
    first person where the owner is speaking, which is why the send confirmation reads
    `Sent. I will read it.`; no exclamation mark anywhere except on the crash surface,
    whose copy keeps both of them; never apologise for something that is not the
    product's fault and always apologise plainly for something that is; say what happened
    and then what is still true, which is the shape of
    `That did not send. Your text is still here.`; and no typographic dash in any string,
    anywhere, in any locale, because these strings get grepped as plain text and a
    typographic dash that survives into a label causes real trouble later.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home destination: the point portrait, the letter field, the biography panel, three annotations | Public |
| `/product` | Work destination: the card row over the wireframe terrain | Public |
| `/sketch` | Studies destination: the contour field and the three-item selector | Public |
| `/sketch/<id>` | One study selected | Public |
| `/award` | Recognition destination: the point globe, the city markers, the reticle, the dated rows | Public |
| `/contact` | Contact destination: the wire letters and the message form | Public |
| `/error` | The one failure surface | Public |
| `/sign-in` | Sign in | Signed out only |
| `/invite/<token>` | An invited editor sets a password | Signed out only |
| `/studio` | Dashboard: the tiles and the recent list | `owner` or `editor` |
| `/studio/work` | Entry list | `owner` or `editor` |
| `/studio/work/new` | Entry editor, empty | `owner` or `editor` |
| `/studio/work/<id>` | Entry editor | `owner` or `editor` |
| `/studio/shelf` | The two ordered lists | `owner` only |
| `/studio/inbox` | Messages | `owner` only |
| `/studio/inbox/<id>` | One message | `owner` only |
| `/studio/account` | Password, sessions, editors | `owner` or `editor` |
| `/studio/log` | The page-view log | `owner` only |

**Entry and redirects.** A signed-out request for any `/studio` route lands on
`/sign-in` carrying the intended path, and signing in sends the visitor onward to it. A
signed-in request for `/sign-in` or for `/invite/<token>` lands on `/studio`. An
`editor` reaching `/studio/shelf`, `/studio/inbox`, `/studio/inbox/<id>` or `/studio/log`
gets the rendered refusal at `403 NOT PERMITTED`, not a redirect and not a bare status.
Signing out ends the current session and lands on `/`. A session that expires part way
through an edit does not clear the form: the next write answers as unauthenticated and a
banner offers a fresh sign-in.

**Journeys.** The first is the primary workflow this product exists for, end to end, and
it touches stored state four separate times: the session, the entry record, the published
flag and the shelf order. A journey that saves one thing proves very little.

1. *The owner publishes and reorders.* Open `/studio` signed out and land on `/sign-in`
   carrying `/studio`. Sign in as `owner@example.com` with `deku-demo-pw-2026` and land
   on `/studio`. Read the published count off the dashboard. Press `NEW ENTRY` and land
   on `/studio/work/new`. Type a title, a kind, a year and a summary, press `SAVE`, and
   read `Saved just now.` with the address now at `/studio/work/` followed by an
   identifier. Press `PUBLISH` and read `Published. It is on the site now.`, with
   `UNPUBLISH` now in the place `PUBLISH` was. Open `/product` and find the entry last in
   the card row. Open `/studio/shelf`, move the row to the first position with the
   keyboard, and read `Order saved.` Reload `/product` and find the entry first.
2. *A visitor sends a message.* Open `/contact`, press `SEND` with every field empty and
   read all three inline errors at once with the control still live. Fill the three
   fields and press `SEND`. Read `Sent. I will read it.` and find all three fields
   cleared.
3. *The owner reads it.* Open `/studio/inbox` and find the row unread and newest first.
   Open it, wait a second, and find it read. The body is the characters that were typed.
4. *An editor is refused.* Sign in as `editor@example.com`, land on `/studio`, and find
   no `INBOX` in the rail and no unread tile. Open `/studio/inbox` and read
   `403 NOT PERMITTED` and `Messages are visible to the owner only.` with `BACK TO WORK`
   beneath. Open `/studio/work/new`, fill it and press `SAVE`, read `Saved just now.`,
   and find no `PUBLISH` and no `DELETE` control anywhere on the page.
5. *A visitor steers the console.* Open `/` and move through `Home`, `Product`, `Sketch`,
   `Award` and `Contact` on the diagram in the corner. The document never reloads, the
   drawing surface is never rebuilt, and no second console read is made.
6. *A stranger tries a draft.* Ask for a draft entry at `GET /api/work/<id>` and be told
   it is gone. Ask for that entry's preview at its exact key and be denied.

**States.** Every list carries a loading state, an empty state, an error state and a
refused state. None is a blank region, none is a spinner without words, none leaves the
reader with no way forward, and none changes the size of the region it fills. The entry
list empty state reads `Nothing here yet.` with `NEW ENTRY`. The shelf reads
`Nothing on the shelf yet.` with `NEW ENTRY`, and with exactly one entry it reads
`One entry. Nothing to order yet.` The inbox reads `No messages.` with
`The contact form on the public site sends here.` beneath it. The page-view log reads
`Nothing recorded yet.` The work destination with nothing published renders the terrain,
the markers and the dust, and one label in the card row's place reads
`Work coming soon.` The recognition destination with nothing published renders the globe
and its cage and one line reads `Recognition coming soon.` A list that failed to load
reads `That did not load.` with a `Try again` control. An error never crashes the app.

## UI/UX notes

The direction is measured off the product this brief was written from, and it is one
idea taken all the way: the console is a readout, not a page. A visitor should understand
in the first moment that they are looking at an instrument. The register is operational
taken to its expressive end, which means the public console is quiet, dense and built
for looking rather than scanning, while the owner's side is an ordinary back office and
reads like one. Space over decoration. Stillness over incident.

**Palette, by role.** The whole console is one near-black neutral ground with one
near-white neutral for every string the scene draws. Everything that is not text is that
same base at a strength, so what the product has is a strength ramp rather than a set of
colours, and the strength is the token. Full strength carries brackets, corner dots, city
markers, the globe cage and the selector's active state; nine tenths the terrain points;
eight tenths the terrain segments and the error text; a half the trajectory caps and
label outlines; three tenths the connector lines and plate fills; a fifth the settled
hairline under a field, the wipe behind a control label and the dust. Everything that
animates in starts at nothing.

Four neutrals sit within twenty points of each other and each holds exactly one job,
which is the rule that stops the palette collapsing: a string drawn into the scene takes
the scene neutral and never the page-furniture one, a line that connects or brackets or
points takes the light neutral and never the terrain's, a point or cage belonging to the
globe takes its own, and a coordinate readout takes the dimmest and nothing else. The
moving markers over the terrain are a light, soft red, they are the only warm colour in
the product, and they appear nowhere else. The letter field behind the portrait is a
five-step ramp running from a near-black cool neutral through a near-black, muted blue, a
deep, muted blue and a deep, soft blue to a deep, vivid blue, and it is the only hue
anywhere on the home destination. The published marker on the shelf is a deep, muted
green and it is the only green in the product. Anything that has gone wrong is a single
soft warm red at eight tenths strength, used for every inline error and for the delete
control's label, and for nothing else. A mid, vivid red, a mid, vivid violet and a mid,
vivid amber are channel-test values that reach no surface: none of the three appears in
the product, and a build in which one is visible has picked up a debugging pass.

**Type.** One technical sans with flat terminals, squared bowls, low contrast and
tabular figures, at four weights. The declared family stack is exactly
`IBM Plex Sans, "Helvetica Neue", Arial, system-ui, sans-serif`, and the interface must
read correctly on the fallback alone. The one property that cannot be substituted away is
that the family has to survive being turned into geometry at ten scene units, because the
navigation plates are set there and a face with fine hairlines smears at that size. The
exact ramp, in pixels and in scene units, is in `## Front-end specification`.

**Shape and density.** No rounded corner anywhere, with one exception: the state dot in
the inbox is a circle. Everything else is a rectangle, a hairline or a bracket of four
corner arms rather than a border. The console is dense by construction, because nothing
scrolls and everything has to fit one frame. The owner's side is comfortable: a single
centred column, a constant field pitch, and an error line that occupies its space whether
or not it has content, so a form never reflows when an error appears.

**Motion.** The motion character is `eased`: a considered entrance and exit on everything
that arrives, and nothing that loops. There is no looping animation anywhere and a
shimmering placeholder would be the only one, so placeholders do not shimmer, pulse or
animate. Four named moments exist and no others. The text settle is the signature: a
string arrives as substitute characters and resolves into its own glyphs, and it is what
every banner, every position label and every changing count does. The destination change
dismisses the outgoing scene, presents the incoming geometry at once and schedules its
annotations last, while the diagram in the corner redraws into a new arrangement with the
four child plates arriving twice as fast as the parent, which is what makes it read as
being pulled into shape rather than replayed. The nearest-edge wipe means a control's
fill enters from the edge the pointer actually crossed and leaves by the edge it leaves
through. The lift means a shelf row under a drag takes a fill while the rows around it
part to show where it will land. Nothing parallaxes and nothing on the public console
scrolls at any width. Under a reduced-motion preference each of the four has a substitute
that lands the same end state without the transit, and the parallel structure's five
destinations are present as soon as the scene is ready rather than after the annotation
delay. Every transition in the product respects that preference.

**Accessibility.** The interface is drawn, which makes it invisible to everything except
eyes unless something is done about it, and the parallel structure is that something: it
carries every string the scene draws, in reading order, with correct heading levels and
real controls, and it is what somebody using a screen reader or a keyboard actually
operates. Body text meets the WCAG AA contrast bar against its ground, and so does every
half-strength secondary line, which is the constraint that decides how far the strength
ramp may be taken. Meaning is never carried by colour alone: the shelf's published marker
carries the word `PUBLISHED` or `DRAFT` beside its dot. Full keyboard navigation with a
visible focus ring on every focusable thing, including the parallel structure's links and
the selector's radio group; the ring is never removed and no state exists in which a
focused thing has none, and a field keeps its underline change while focused so that the
ring and the underline are both present rather than one replacing the other. Icon-only
controls carry a label: the sound control reads as on or off and the six-dot handle reads
as the reorder handle for its row. Touch targets are comfortably sized. The focus order on
every destination is the skip link reading `Skip to content`, then the destination region,
then the five destinations in the order `Home`, `Product`, `Sketch`, `Award`, `Contact`,
then the destination's own controls, then the information control, the source link and
the sound control. The five destinations come before the destination's own controls,
which is the opposite of the visual order and is right: somebody arriving by keyboard
needs to be able to leave before they need to be able to act.

**Responsive.** One real breakpoint. Above it the arrangement never changes between two
wide sizes, only its size, and a short viewport makes the interface larger rather than
cropping it up to a clamp. Below it the contact surface renders in ordinary page
furniture and the console does not attempt the scene. At a narrow viewport nothing
overflows sideways and every destination stays reachable. The owner's side is a single
centred column at every width, and the entry editor's preview panel moves from beside the
fields to above them at the narrow one. Orientation is not a second breakpoint: a narrow
window held the long way and a wide one held the short way are decided by width alone, so
rotating a device changes the size of the arrangement and never which arrangement it is.
No scrollbar appears on the public console at any width or orientation.

**What it must not look like.** Not a marketing page: no hero, no editorial composition,
no decoration standing in for content. Not a dashboard template: no card with a drop
shadow, no gradient, no accent colour applied for warmth. And not a page dominated by one
hue with no second signal, which is the failure the strength ramp exists to prevent.
Wherever this section declines to give a value, the exact value is yours so long as it
holds the rules above.

## Technical requirements

The app is a single-page application served against a JSON API on the same origin. The
browser receives an application shell on first paint and the console's content arrives in
one read; there is no per-destination fetch and no document reload while a visitor
steers. Frontend: React with Vite, built to static assets. Backend: FastAPI. Datastore:
PostgreSQL, reached at `DATABASE_URL`. Object store: `minio`, reached at
`STORAGE_ENDPOINT` with the bucket at `STORAGE_BUCKET` and the credentials at
`STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Authentication is email and password
implemented by the app, with an opaque session cookie that scripts cannot read and that
carries no claims. Passwords are stored only as a memory-hard hash and are never
returned by any endpoint. `GET /api/health` returns `200` once the app is ready and
reads nothing behind a session. One structured log line per request goes to standard
output carrying the method, the route template, the status and the elapsed milliseconds,
and no log line carries a full network address, a session token, a password or a message
body.

Use only the libraries named here plus their direct dependencies. Do not introduce a
second database, cache, queue, object store, identity provider or mail vendor: the only
backing services available in this environment are `postgres` and `minio`, and reaching
for anything else is a contract violation. Both are already running and reachable at
their environment variables. Do not download, install, compile or start a copy of either.
Never hardcode a host or a port; read every one from the environment.

The rendering capability this product needs, stated as capability rather than as a
library: the build must hold one drawing surface at the full window size across every
destination change without rebuilding it, draw its text as geometry rather than as page
text, and hold its frame budget while the interface above it changes. Whatever draws that
surface is yours to choose.

The rendering capability extends to five more things, each stated as a capability the
build must have rather than as a library it must use. It must hold at least seven
independently presentable scenes and composite them into one frame. It must run a
simulation pass on the drawing hardware whose output feeds the next frame. It must
composite a post-processing chain of at least three passes over the result, including a
bloom and a colour-split whose strength is driven by how fast the camera is moving. It
must generate a signed distance field for text at run time, so that a title the owner
types appears drawn into the scene, crisp, without a reload. And it must resize without
reallocating the scene, updating every camera's aspect on the way.

Module separation, stated as observable behaviour. The console never reads the address
bar and the interface above it never reaches into the scene, so the two can be reasoned
about apart; the owner's studio is a separate surface whose components and modules are
never loaded alongside the console, so a visitor downloads none of the editor. Three trees, and the
architecture of one never leaks into another.

Performance. The first destination reaches an interactive frame on a mid-range laptop
within a stated budget and holds a steady frame rate afterwards; the scene, its audio
graph and its glyph cache are built once and are not rebuilt on a destination change.
The shell, the console read and the glyph atlas for the interface weights are preloaded;
every scene's own geometry is deferred until its destination is first reached. When the
frame rate falls the build degrades one tier at a time rather than all at once, dropping
the post-processing chain first, then the point counts, then the simulation pass, and it
never degrades the parallel structure. Degradation moves one tier at a time and never
jumps two, and it recovers a tier when the frame rate does. Frame-rate independence is
the rule behind it: every smoothing factor is corrected for elapsed time, so the
same motion reads the same at any frame rate on any machine. The glyph cache is bounded and
evicts least-recently-used entries rather than growing without limit.

The zero-asset rule, and the substitution that replaces every binary. The product ships no binary asset of
its own. It downloads no image, no
audio file, no scene binary and no font file from its own origin: every point set, every
texture, every card image and every contour field is generated from an integer seed at
build time or at run time, and the one type family is declared as a stack rather than
served as a file.

Every response carries a security header set: a strict transport policy, a nosniff
content-type policy, a frame-denial policy, a same-origin referrer policy, and a content
policy permitting scripts and styles from the origin only with no inline script. The
session cookie is not readable by scripts, is marked secure, is same-site strict, and is
not sent on cross-site requests.

Every public destination declares its own title and its own social preview title and
preview image, and no two destinations share them. The preview image each one declares
resolves to bytes that are actually served. The titles are `MARLOW HENDRIKS | Product
Engineer and Design Engineer` on `/` and on `/error`, and `MARLOW HENDRIKS | Product`,
`MARLOW HENDRIKS | Sketch`, `MARLOW HENDRIKS | Award` and `MARLOW HENDRIKS | Contact`
on the other four. The description used on every public destination is `Marlow Hendriks,
product engineer and design engineer, building digital products end to end. Beauty and
function as a single problem.`

No credential, access key or session token appears in anything the browser downloads.
The object store's credentials are read at the server and never reach the client.

## Data model

Eight tables holding nine entities. All timestamps are UTC.

The relationships between them: an account has many sessions; an account authors many
work entries, and deleting the account leaves them; a work entry has up to four links; a
city has many recognitions and a recognition names exactly one city; a message and a
study each stand alone; and there is exactly one profile beside the one owner. Every one
of these is persistence that survives a reload and follows the owner to a new device:
everything on the server does, and the only things that live in the browser are the
sound control's state and a half-written contact message.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture
data, not a secret. Hash it as normal; the exact literal must work at login, and it must
be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**`accounts`** carries `id`, `email` which is unique and lowercased and 1 to 254 long,
`password_hash` which is never returned, `display_name` 1 to 80, `role` which is `owner`
or `editor`, `failed_attempts` which resets to zero on a successful sign-in,
`locked_until` which is a timestamp or empty, and `created_at` and `updated_at`. Exactly
one row holds `owner`.

**`sessions`** carries `id`, `account_id`, `token_hash` because the cookie value is never
stored, `user_agent_summary` which is a short description and never the full string, and
`created_at`, `last_seen_at` and `expires_at`.

**`profile`** is exactly one row: `full_name` 1 to 40, `role_line` 1 to 80, `intro` 0 to
1200, `history` which is a list of period and role pairs 0 to 12 long, `annotations`
which is a list of two-line pairs exactly 3 long, `portrait_seed` 0 to 999999, `version`
and `updated_at`.

**`work_entries`** carries `id`, `title` 1 to 120, `kind` 0 to 60, `year` 1970 to 2026,
`summary` 0 to 280, `body` 0 to 8000, `grid_seed` 0 to 999999, `grid_palette` which is
`neutral` or `blue` or `coral`, `position`, `published`, `published_at`, `preview_key`
which holds the object key in the bucket, `author_id` which names the account that
created it and survives that account's removal, `version`, `created_at` and `updated_at`.
`position` is dense from zero and unique across every row, published or not.

**`entry_links`** carries `entry_id`, `label` 1 to 40, `href` which must parse and begin
with a secure scheme, and `ordinal` 0 to 3. At most four rows belong to one entry.

**`studies`** carries `id`, `title` 1 to 120, `field_seed` 0 to 999999, `position` dense
from zero, `published`, `version`, `created_at` and `updated_at`.

**`recognitions`** carries `id`, `year` 1970 to 2026, `body` 1 to 120, `rank` which is one
of `Gold`, `Silver`, `Bronze`, `Winner`, `Merit`, `Nominee`, `Finalist`, `Honoree` or
`Selection`, `city_id`, and `published`. **`cities`** carries `id`, `name`, `latitude`,
`longitude` and `bearing_label`. A recognition names exactly one city; a city may carry
many recognitions.

**`messages`** carries `id`, `sender_name` 1 to 80, `sender_email` 1 to 254, `body` 10 to
4000, `state` which is `unread` or `read` or `archived`, `source_path` which is the route
the form was submitted from, and `received_at`.

**`page_views`** carries `id`, `route` and `viewed_at`, and nothing else. No row holds a
full network address and nothing in the table follows one person between two views.

Derived rather than stored: the dashboard's published count, draft count and unread
count; the paging indicator's length on `/product`; and every relative time the interface
shows.

Two invariants the running system must hold, both observable from outside it. Two writes
to one work entry from the same version: exactly one is accepted and the other is
refused, and the accepted one raises the version by one. Two reorders submitted at once:
exactly one order is stored whole, and no state exists in which some positions came from
one payload and the rest from the other.

**Seed data.** Two accounts: `owner@example.com` with display name `Marlow Hendriks` and
role `owner`, and `editor@example.com` with display name `Rowan Vale` and role `editor`.
One profile row with `full_name` `MARLOW HENDRIKS`, `role_line`
`Product Engineer and Design Engineer`, `portrait_seed` `41207`, four history rows and
three annotation pairs. No work entries. Three published studies at positions 0 to 2:
`Ridge Survey` with `field_seed` `10240`, `Tide Table` with `field_seed` `20480`, and
`Lantern Field` with `field_seed` `30720`. Three published recognitions: `2013`
`Northlight Prize` `Bronze` in `Oslo`, `2012` `Meridian Review` `Winner` in `Lisbon`, and
`2009` `Halden Biennale` `Gold` in `Kyoto`. Three cities: `Oslo`, `Lisbon` and `Kyoto`,
each with its coordinate pair and its bearing label. No messages and no page views. The
seeded studies are what make a first run whole rather than empty: the studies destination
renders its full contour field with a working selector before the owner has written
anything.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

**Type.** One technical sans with flat terminals, squared bowls, low contrast and
tabular figures, at four weights. The declared family stack is exactly
`IBM Plex Sans, "Helvetica Neue", Arial, system-ui, sans-serif`, and the interface must
read correctly on the fallback alone. The one property that cannot be substituted away is
that the family has to survive being turned into geometry at ten scene units, because the
navigation plates are set there and a face with fine hairlines smears at that size. The
page-furniture ramp is carried exactly: annotation bodies and coordinate readouts at
`11px` weight `300` on `13.2px`; inline errors and every half-strength secondary line at
`11px` weight `400` on `13.2px`; footer copy at `12px` weight `300` on `14.4px` with
`1px` tracking; field labels and rail items at `12px` weight `400` on `12px` with `1px`
tracking; the status banner at `12px` weight `400` on `15.6px`; input text, message
bodies and empty-state copy at `16px` weight `300` on `22.4px`; the wordmark at `18px`
weight `400` on `21.6px` with `1px` tracking; bracketed controls at `20px` weight `400`
on `20px` with `2px` tracking; the failure action label at `24px` weight `400` with
`3px` tracking; panel titles and the failure code at `28px` weight `300` on `28px`.
Where a line box equals its type size the element is a chrome row whose box must not
grow, and that is deliberate. The scene ramp is unrelated and is in scene units: the
wordmark and the loading counter at `96`, a recognition row at `32`, a navigation plate
at `10`, a terrain annotation at `16`, on a base leading of `48`.

**Shape and density.** No rounded corner anywhere, with one exception: the state dot in
the inbox is a circle. Everything else is a rectangle, a hairline or a bracket of four
corner arms rather than a border. The console is dense by construction, because nothing
scrolls and everything has to fit one frame. The owner's side is comfortable: a single
centred column, a constant field pitch, and an error line that occupies its space whether
or not it has content, so a form never reflows when an error appears. That last property
is worth more than it looks and it is the reason two of the gaps in the layout are the
odd sizes they are.

**Iconography.** Seven symbols exist in the product and no eighth is drawn: the sound
control on, the sound control off, the information control, the six-dot reorder handle,
the paging indicator's mark, the selector's bracket arm, and the compass tick. Every one
is drawn on a whole-unit grid with no arbitrary angle, at a stroke that matches the
hairlines around it, and a new symbol that has to be added is built on the same grid or
it does not belong.

**Spacing scale.** Space is a scale rather than a set of margins: one base step, doubled
and halved, with the field pitch and the label-to-input gap fixed so the form never
reflows. Sections read as separate at a glance without needing a dividing line, which is
what the scale buys and why there are almost no rules in this interface.

**Radii, borders and blur.** The radius scale has one value, which is none, and one
exception, which is the circular state dot. A border is a hairline at a strength or it is
four bracket corner arms; there is no second border weight. Blur exists in exactly one
place, behind the message panel over the wire letters, where it separates the form from
the scene without hiding it.

**Depth.** Depth is carried by overlap and by strength, never by a drop shadow and never
by a gradient. The loading counter's two layers are offset in depth and that offset is the
only place in the product where two copies of one string are drawn at once.

**The compass and the arrival sequence.** The compass over the terrain is drawn when the
work destination has anything published, with its four cardinal points set larger than
its four intercardinal ones and its ticks and labels in the terrain's own neutral. The
arrival sequence on every destination is fixed: the base geometry presents at once, the
destination's own marker follows, the annotations arrive last and arrive faster on a
second visit than on a first, and the navigation diagram and the footer return together
at the end.

**The failure surface treatment.** The code and the message are set at the panel title
size in the scene's own near-white neutral on the near-black ground, with the action
label above a bordered plate at the largest tracking in the product, and the plate's
border at the lightest strength. Where the failure surface renders inside the drawing
surface rather than as page furniture it is drawn at the scene's own scale, and both
paths must exist: the scene path while the console is alive, the page-furniture path when
it is not.

**The interaction on the shelf, stated as feel.** A row under the pointer takes a fill, a
row being dragged takes the darker fill and a hairline border, and the rows around it
part rather than sliding under it. The drop position snaps to a row boundary. Escape
returns the row to where it started and writes nothing.

## Constraints

Single owner, single portfolio. No multi-tenancy and no second profile.

Absent by decision, and not to be added: a recognition editor, since the recognition rows
and their cities are seeded and read only in this release; any search on the public
console, where the owner's lists are the only filterable ones and carry their filter and
sort state in the address; an audio layer, so no bed, cue, gain node or oscillator exists
anywhere in this product and the sound control is a label with nothing behind it; a
real-time channel and every behaviour that would depend on one, so the unread count
refreshes on a read rather than on a push and no reconciliation between two open sessions
is ever attempted, though a reorder is still applied optimistically in the interface and
animates back if the write is refused; data export; internationalisation, locale
resolution and translated copy, so every string is the English this brief pins and the
formatting of every date, time and number is fixed rather than resolved; schema migration
tooling; an analytics vendor or any third-party instrumentation, so the page view is the
only event recorded anywhere and the log is the whole of it; an offline hold for an unsent
message; comments, likes, follows and any social surface; any notification beyond the
single unread count; any payment, price or currency anywhere.

Security and abuse. The only two things a stranger can reach are the public read and the
contact form, and that surface stays small: there is no public sign-up to abuse, no
markup path into any rendered string, and no address in the failure surface that is not
matched against its closed table first.

No external service is called to satisfy a request at run time. No native application.
No edge functions.

The app stays responsive with 200 work entries, 200 studies, 500 recognitions, 5,000
messages and 50,000 page views in the database.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never
  hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root,
  empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the
  shell. An ordinary background job dies with its shell, and the app will not be running
  when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Every endpoint below accepts the bearer token from
`POST /api/auth/login` in an `Authorization` header, and the browser's session cookie
carries the same session. Both are absent from health, the console read, the
published-entry read, the published preview read, the message post and the page-view
post, which need no credential at all.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | A readiness body |
| `GET /api/console` | none | `{ profile, work, studies, recognitions, cities }`, published only, in shelf order |
| `GET /api/work/{id}` | none | One published entry with its links. A draft or a deleted one answers as gone |
| `GET /api/previews/{entry_id}/{object}` | none | The preview bytes for a published entry. A draft entry's preview is denied |
| `POST /api/messages` | `{ name, email, body, decoy, built_at }` | `{ id }` |
| `POST /api/page-views` | `{ route }` | The recorded view |
| `POST /api/auth/login` | `{ email, password }` | `{ access_token, account }` and the session cookie |
| `POST /api/auth/logout` | none | Empty |
| `GET /api/studio/work` | `q`, `state`, `sort`, `page` | `{ items, total, page }`, every entry including drafts |
| `POST /api/studio/work` | An entry without server fields | `{ item }` |
| `GET /api/studio/work/{id}` | none | `{ item }` |
| `PATCH /api/studio/work/{id}` | Changed fields and `version` | `{ item }` |
| `DELETE /api/studio/work/{id}` | `{ version }` | Empty. `owner` only |
| `POST /api/studio/work/{id}/publish` | `{ version }` | `{ item }`. `owner` only |
| `DELETE /api/studio/work/{id}/publish` | `{ version }` | `{ item }`. `owner` only |
| `PUT /api/studio/shelf` | `{ kind, order, versions }` | `{ items }`. `owner` only |
| `GET /api/studio/messages` | `q`, `state`, `sort`, `page` | `{ items, total, page, unread }`. `owner` only |
| `GET /api/studio/messages/{id}` | none | `{ item }`. `owner` only |
| `PATCH /api/studio/messages/{id}` | `{ state }` | `{ item }`. `owner` only |
| `DELETE /api/studio/messages/{id}` | none | Empty. `owner` only |
| `GET /api/studio/page-views` | `page` | `{ items, total, page }`. `owner` only |
| `GET /api/studio/editors` | none | `{ items }`. `owner` only |
| `POST /api/studio/editors` | `{ email }` | `{ invitation }`. `owner` only |

A list endpoint returns a top-level JSON array or an object whose `items` key holds one.
A successful call returns the named resource or shape. An invalid or unauthorized call is
rejected as a client error, never as a server failure and never as a silent success.
Every non-success response carries the same body shape and nothing else: an `error`
object holding a `code` from the closed set `bad_request`, `unauthenticated`,
`forbidden`, `not_found`, `gone`, `conflict`, `unprocessable`, `rate_limited`, `locked`,
`server_error`; a `message` which is exactly the sentence this brief pins for that
condition; and, for an unprocessable one only, a `fields` map from field name to the
inline sentence.

**No mocks.** The preview bytes for every entry live as a real object in the `minio`
bucket under the pinned key scheme. An in-memory dictionary of preview bytes, a file
written to the app container's own filesystem, a data URI inlined into a response, and a
column in `postgres` holding the bytes are each the wrong thing and each leaves the
bucket empty. The named provider is the fact: the app's UI and its own tables can only
reflect what lives in the provider, never substitute for it.

## Definition of done

A stranger can open the console, steer it between all five destinations without the
document reloading, open a published dossier and send a message that the owner then
reads in their inbox. The owner can sign in, write an entry, publish it, and find it in
the public card row, then move it to the front of the shelf with the keyboard alone and
find it first. An entry that is not published is absent from the public read, answers as
gone at its own path, and its preview image is refused to a stranger at its exact key.
