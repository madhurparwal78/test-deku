# Sable

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser and complete a
staged project brief on a phone, in one hand, leaving with a discovery call booked at a
named time in their own time zone, without hitting an error page and without losing a word
they typed.

A different stranger, signed in to the client portal for one engagement, must NOT be able
to read another engagement's deliverables, comments or approvals by any means. That cannot
be arranged in the interface: the record must not be returned at all. In the same way, a
file attached to a brief must exist as a real object in the MinIO bucket at its pinned key
scheme; bytes on the app container's own filesystem, or a row holding the file's contents,
do not count. And a case that has not been published must not be readable at its own
address by anyone who is not the studio.

## Overview

Sable is the public site and new-business surface of Sable Digital, a full-cycle digital
agency. It is a marketing site that sells on craft, and a small set of working surfaces
behind it: a case archive that can be asked a question, a staged project brief that ends in
a booked call, a capabilities deck composed on the spot, and a private engagement portal for
clients already in flight.

Three readers use it, in descending order of how much they will see. A prospective client
arrives from a referral or an award index and wants to know within two screens whether this
studio makes things at their level; the entire scroll design is aimed at that person. A
procurement or marketing lead needs something to circulate internally, and gets a composed
capabilities deck rather than a document mailed a day later. A designer or developer
considering applying reads the service index and the case archive as a description of the
work. A fourth reader, an existing client mid-engagement, reaches the portal and nothing
else.

Part of this product is measured against the site the studio already runs, and part of it is
commissioned. The marketing spine, the contact route and the privacy document reproduce what
exists; the case study route, the queryable archive, the staged brief, the tone board, the
deck composer and the client portal are new. Every capability stated here is normative and is
not optional. Where a line notes what the existing site happens to do, that note is
informational and the build may satisfy the capability another way. Acceptance is judged on
the normative statements alone.

The site has one action that touches state and matters more than the rest: submitting a
project brief. It runs over six stages, it survives a closed tab, and it ends with a
specific conversation at a specific time rather than a message sent into a void.

What it deliberately is not: there is no project management tool, no chat, no folder-based
file store, no downloadable deck file, no live calendar integration, no payments, no
invoicing, no subscriptions, no comments, likes, follows or messaging on the public routes,
and no third-party analytics endpoint. The portal answers three questions and does nothing
else, and that scope discipline is the difference between a feature and a second product.

The genuinely hard part is the brief's booking step. Two visitors will select the same slot
inside the hold window, and exactly one of them must end up with it, refused at submission
rather than at selection, with every other answer in their brief intact.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `studio` | Publish and unpublish a case; create and edit case chapters; read every submitted brief and its attachment once scanned; create engagements, milestones, deliverables and versions; read deck read-telemetry; extend or revoke a deck link | **Cannot approve a deliverable on a client's behalf**, and **cannot read a client's portal session** |
| `client` | Sign in to the portal for the engagements their account is attached to; read that engagement's current phase, milestones, deliverables, versions, people and documents; comment on a version, including pinning a comment to a point on a still; approve or request changes **only when their account carries the approval right on that engagement** | **Cannot read any engagement their account is not attached to**, **cannot read an unpublished case**, **cannot read another visitor's brief or composed deck**, **cannot publish anything**, and **cannot approve without the approval right** |

The portal's three registers, `viewer`, `approver` and `owner`, are an approval right held
by a `client` account on one engagement, not extra roles. A `viewer` is a `client` account
without the right; an `approver` and an `owner` are `client` accounts with it.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the
UI is not authorization: a direct API call from a `client` session to any `studio`-only
endpoint must be rejected by the server (an unauthorized request is denied, not served),
leaving the protected state unchanged. The same holds inside the `client` role: a direct API
call from an account without the approval right to the approve endpoint is denied and the
version's state does not change.

Signup is open: anyone may create an account. A new account is attached to no engagement and
therefore sees nothing in the portal until the studio attaches it. Portal accounts may also
enter by a single-use sign-in link that is valid for fifteen minutes; the link exchanges for
the same session a password sign-in produces.

Seeded accounts, all using the password `deku-demo-pw-2026`:

| Email | Role | Notes |
|---|---|---|
| `studio@example.com` | `studio` | the agency account |
| `client@example.com` | `client` | attached to the `Northwind Aero` engagement, **with** the approval right |
| `client2@example.com` | `client` | attached to the `Bridgeline Health` engagement, **without** the approval right |

## Core features

### Auth

Accounts are email and password, held by the app itself. There is no external identity
provider. A successful sign in returns a bearer token the client sends on every subsequent
request; the token expires after thirty days and an expired token leaves whatever was in
flight untouched. Passwords are stored hashed. Signup is open and asks for email, password
and a display name. A portal sign-in link is single use, expires fifteen minutes after it is
issued, and a used or expired link offers a control to request a fresh one rather than
failing silently.

1. A request carrying no bearer token to any portal endpoint is denied, and no engagement
   data appears in the response body.
2. Signing out clears the session on that device and offers to clear every session on every
   device.

### Uploads and the object store

1. Uploaded bytes live in the MinIO bucket and nowhere else. **No copy on the app
   container's filesystem and no bytes in a table.** The key scheme is fixed:
   `briefs/{brief_token}/{sha256_of_bytes}.{ext}`, for example
   `briefs/8f41c2d7e9b04a16/3b1f9c0d5a72e84b6f1d20c93ae57482fd6b0913c4e75a28d0f61b39e2470c85.pdf`,
   and `deliverables/{engagement_id}/{version_id}/{sha256_of_bytes}.{ext}`, for example
   `deliverables/7/2/9a4c1e07b3d85f62a018c74be95d203f6187ca45e0b2d9376f4a81c05e6d3b29.png`.
2. A protected object is reached only through an authenticated streaming endpoint on the
   app's own origin, and never issued to an account that is not entitled to it.
3. **An upload is not readable by anyone, including the studio, until it has been scanned.**
   A request for an unscanned object is denied.
4. A brief attachment belongs to one brief token. A request for it carrying a different
   token, or no token, is denied.

### The marketing spine

The home route tells one story in nine bands, in this order, and it runs to roughly sixteen
screens: the loader and the hero video on the dark ground; the studio strip and the
positioning line, where the ground cuts from dark to light; the What We Do service index;
the tone words over the dot field; Fresh Drop, the latest case; four numbered capability
features, pinned, back on the dark ground; Selected Cases, the archive grid; the
capabilities deck band on its brushed metal texture; and the clients index followed by the
footer.

1. The three in-page anchors `Projects`, `Services` and `Agency` are anchors on the home
   route, not routes. Following `Projects` from `/contact/` must navigate to `/` and then
   settle at the projects band. The landing position must not be offset by the difference
   between the header's layout token and the band the header actually draws.
2. `Contact` is the only real route in the navigation, and it renders struck through while
   the contact route is active.
3. Moving between routes does not reload the document: the next document is fetched, the
   main region is swapped, every scroll-linked binding is destroyed, and the new route
   initialises. **After twenty navigations the home route must scroll exactly as it did on
   the first load.** A build that leaves bindings attached leaks one timeline per
   navigation and degrades the longer the site is used.
4. Back and forward restore the scroll position on a route already visited, and do not
   replay the loader.

### The loader and first load

A dark field covers the viewport with a single light bar across its vertical midpoint,
carrying the word `LOADING...` in the monospace, upper case, ranged left inside the bar. The
bar is a real progress meter: it grows from nothing to the full width of the frame and the
label rides its left edge. The label rises at a constant rate, not eased, because it is
reporting progress.

1. The loader runs on a first document load and never again: not on a route change within
   the session, not on a return to a visited route through history, and not at all when
   reduced motion is requested.
2. When it finishes, the dark field splits at the bar and the two halves sweep outward like
   curtains, and the wordmark drops in from above. The curtains meet at the bar, not at the
   centre of the screen.
3. Two separate moments exist: content reveals may begin when the sequence completes, and
   the loader element itself is removed from the document at the second. It must be removed
   rather than hidden, because it sits above everything including the pointer for the rest
   of the session otherwise.
4. The loader must never block input: the capabilities deck control is reachable while it
   runs.
5. The slow-load simulation switch is a development affordance and must not be enabled in
   the built output.

### The service index and the tone words

Twenty services in four columns of five, ruled between every row, the rules running full
width past the last column so the band reads as a schedule rather than a list. The twenty,
in order:

`Logo Design`, `Brand Identity Systems`, `Corporate Identity`, `User Experience Design`,
`UX Strategy`, `User Interface Design`, `UI Kits & Design Systems`, `Product Design`,
`Custom Product Solutions`, `Prototyping`, `Graphic Design`, `Marketing Graphics`,
`Illustrations`, `Motion Design`, `3D Modeling`, `Frontend Development`,
`Backend Development`, `DevOps & Architecture`, `Product Analytics`, `Creative Direction`.

The band's heading pairs `WE DO` with `What`, and its lead reads
`We build standout digital products and experiences that move our clients' brands forward.`
A hover affordance labelled `SABLE APPROACH` sits beside the index; it is labelled `hover`
where the pointer is fine and `Tap To` where it is not.

Four tone words fade in sequence over the dot field: `Vision.`, `Clarity.`, `Flow.`,
`Execution.` Beside them sits the studio paragraph, which names Sable Digital's
headquarters and its distributed team of designers, developers and strategists working
across North America and Europe.

1. Each dot in the field has a home position that is never drawn, and a current position.
   Scroll displaces the dot and it returns towards its home. The displacement is per dot,
   not one movement applied to the whole group.
2. Reversing the scroll anywhere on the route runs every driven property backwards with the
   input, with no re-entry animation.

### The four capability features

A pinned band on the dark ground holding four numbered capabilities. The section holds
still while its four items advance past the reader.

| Number | Title | Keywords |
|---|---|---|
| `(01)` | `Branding` | `meaning`, `identity` |
| `(02)` | `UX/UI Design` | `logic`, `layout` |
| `(03)` | `Web & Development` | `reliability`, `deployment` |
| `(04)` | `3D / Motion` | `dynamics`, `energy` |

The keyword pool the cycler draws from, thirty words: `aesthetic`, `architecture`,
`branding`, `clarity`, `consistency`, `deployment`, `depth`, `dynamics`, `emotion`,
`energy`, `feedback`, `flow`, `hierarchy`, `identity`, `interaction`, `layout`, `logic`,
`meaning`, `movement`, `performance`, `realism`, `reliability`, `rhythm`, `scalability`,
`story`, `structure`, `texture`, `timing`, `tone`, `voice`.

Each feature carries a video. Below the four sits a full-width call to action with two arc
decorations, the right one a half-turn rotation of the left so that one drawing serves both,
each inverted so a single dark drawing works on either ground.

1. On a phone the capability band does not pin. That is a separate arrangement, not the
   same arrangement with different numbers, because a pinned band on a phone fights the
   browser's own address-bar behaviour.

### Selected cases and the archive

Thirteen cases in a staggered three-column arrangement with uneven vertical offsets, so no
two adjacent cases share a baseline. Each case is a media panel with its name beneath in the
monospace, upper case. The heading reads `Selected Cases` and carries three counts beside
it: `BRANDING (7)`, `WEB (13)`, `PRODUCT (5)`.

The thirteen, with their sectors:

| Case | Sector |
|---|---|
| `Northwind Aero` | `TECHNOLOGY` |
| `Bridgeline Health` | `HEALTHCARE` |
| `Northwind Ops` | `TECHNOLOGY` |
| `Meridian Commodities` | `FINANCE` |
| `Cobalt Commerce` | `ECOMMERCE` |
| `Halden Group` | `AGENCY` |
| `Summit Interlink` | `TECHNOLOGY` |
| `Vantage Cards` | `FINANCE` |
| `Baseplate` | `TECHNOLOGY` |
| `Sturgeon` | `AGENCY` |
| `The Balance Clinic` | `HEALTHCARE` |
| `Future Tense` | `AGENCY` |
| `Grove App` | `ECOMMERCE` |
| `Token Market` | `FINANCE` |

1. Case media is wiped in from a corner rather than faded. **The corner alternates through
   the four corners in a fixed cycle as the reader descends, and two adjacent cases never
   use the same corner.** The corner is derived from the case's position in the grid and is
   never stored on the case record, because an editor given the choice picks a favourite and
   the alternation is the point.
2. The case name rises into place under its panel as the panel wipes in. On a phone the name
   fades instead of rising, and the case panel fades instead of wiping.

### The case overlay and the case study route

Selecting a case in the home archive opens an overlay rather than navigating. The overlay
carries the case name, a row of discipline tags, two paragraphs of body, a gallery of
stills and video, a circled close control that rotates a half turn when pointed at, and a
`Let's talk` call to action.

The twenty-four discipline tags, normalised to upper case: `BRANDING`, `GRAPHIC DESIGN`,
`UX & UI DESIGN`, `WEB DEVELOPMENT`, `ILLUSTRATIONS`, `MOTION DESIGN`,
`CREATIVE DIRECTION`, `STRATEGY`, `CORPORATE IDENTITY`, `SOCIAL`, `PRODUCT`, `DEVELOPMENT`,
`CONSULTANCY`, `FRONT-END`, `API INTEGRATION`, `WEB DESIGN`, `ANIMATION`, `ARCHITECTURE`,
`DEVOPS`, `SOLUTION`, `SECURITY`, `UX DESIGN`, `UI DESIGN`, `WORDPRESS`.

1. The overlay traps focus inside itself while open, returns focus to the case that opened
   it on close, and closes on the escape key. The document does not scroll behind it.
2. Every case is **also** a full route at `/work/<case-slug>/`, so a single project can be
   sent as a link into a procurement thread and read by somebody who will never load the
   home route. The overlay is kept as the quick look.
3. The slug is derived from the case name, lower case and hyphenated, and is stable for the
   life of the case. A renamed case keeps its slug and gains a redirect. **A slug is never
   reused.**
4. A case is a sequence of typed chapters rather than a body of prose, and the renderer
   chooses the layout from the type. The ten types: `cover` (name, sector, year and one
   positioning line, full bleed on the dark ground), `context` (two to four paragraphs and a
   tag row), `figures` (up to four measures with labels, as large display numerals),
   `still` (one image with an optional caption), `compare` (two images and a draggable
   divider), `sequence` (three to eight images on a horizontal track), `motion` (one video
   with a poster and a caption), `quote` (a quotation and its attribution), `stack` (the
   delivered disciplines as tag pills) and `outcome` (a closing paragraph and the call to
   action).
5. **A case must open with `cover` and close with `outcome`.** Every other type is optional
   and repeatable. **A case carrying fewer than four chapters must not publish**, and an
   attempt to publish one is rejected as invalid with the reason stated.
6. A chapter rail lists the chapter titles in the monospace, marks the current chapter with
   an accent dot **paired with its title in text**, and allows a jump to any of them.
7. The comparison chapter must be readable without dragging: both labels are always visible
   and at rest each image shows half of itself. The divider is operable by keyboard, where
   the left and right arrows move it a small step and home and end jump to the extremes, and
   dragging it on a touch screen does not capture the page's vertical scroll.
8. The sequence chapter advances its horizontal track from vertical scroll while pinned.
   When motion is reduced the pin is released and the track becomes an ordinary
   horizontally scrollable region reachable by tab, which is a better experience with a
   keyboard than the pinned arrangement rather than a degraded one.
9. Three related cases sit at the foot of every case route, chosen by the similarity rule
   and each rendered as an archive card.
10. **An unpublished case is not readable at `/work/<case-slug>/` by anyone but `studio`.**
    A request from a signed-out visitor, or from a `client` session, is answered as not
    found, and the response body carries no part of the case.

### Case intelligence: the archive, comparison and search

`/work/` carries every case, not only the thirteen selected for the home route, and the home
route's Selected Cases band links to it. Its heading reads `The Archive`.

1. Three facets narrow it: **Sector** (`FINANCE`, `TECHNOLOGY`, `HEALTHCARE`, `AGENCY`,
   `ECOMMERCE`), **Discipline** (the twenty-four tags above) and **Kind** (`BRANDING`,
   `WEB`, `PRODUCT`). Values combine as an intersection across facets and as a union within
   a facet.
2. **Every facet value shows its live count**, and a value whose count is zero is disabled
   rather than hidden, so a visitor cannot filter their way into an empty page.
3. The active filter is carried in the address, so a filtered archive is a link that opens
   the same filter somewhere else.
4. An empty result names the nearest non-empty filter and offers it, reading
   `Nothing matches all of those. The nearest is:`. A single `Clear filters` control is
   visible whenever any facet is active.
5. Up to three cases are held side by side in a comparison tray. A `Compare` control sits on
   each archive card and on each case route, and the tray is pinned to the foot and
   collapsed to a bar showing `Comparing <N>`. Expanded it is three columns with aligned
   rows comparing sector, kind, disciplines delivered, engagement shape and the `figures`
   chapter measures. **A measure a case does not publish reads `not published` rather than
   being omitted, so the columns stay aligned.** The tray survives navigation within the
   session and is itself addressable.
6. Similarity is the overlap of each case's discipline tags, sector and kind, ordered by
   discipline overlap first, then sector, then recency. **A similarity suggestion must state
   in one line what the two cases share**, in the form `Also <DISCIPLINE_LIST>`. A
   recommendation the reader cannot account for reads as an advertisement.
7. One search field matches case names, sector, discipline tags and the text of `context`
   chapters. It filters the archive in place rather than navigating to a results route, it
   is reachable by tab from the archive heading, and the escape key clears it. Results
   update once the field settles after the last keystroke rather than firing on every one,
   and the latency on a local dataset is short enough that the archive feels immediate.
8. **Changing a filter must not replay the corner wipe on cases already on screen.** A case
   entering the filtered set fades in, a case leaving fades out and the grid then reflows,
   and a case that stays moves to its new position. Only the archive's first paint runs the
   full corner wipe. Replaying it on every change makes the page strobe.

### The contact route and the capabilities deck modal

`/contact/` is one screen tall and does not scroll. The contact rail runs down the left with
the address, phone, email, the deck control and five social marks, bracketed top and bottom
by two wireframe hemispheres, the lower one mirrored. The heading pairs `Let's` with `Talk`.

The form is six softly rounded panels in an asymmetric arrangement with the project
description panel spanning two rows, and one full-bleed submit bar across the foot:

| Field | Label | Required |
|---|---|---|
| name | `*Hello Sable, my name is...` | yes |
| company | `*My company name is...` | yes |
| current site | `Current site https://` | no |
| project | `Now, a little about my project...` | no |
| contact intro | `*you can contact me...` | a label, not a field |
| email | `My Email:` | yes |
| phone | `My Phone:`, placeholder `(000) 000 0000` | no |
| brief | `here's my brief`, control `UPLOAD BRIEF (max 2mb)` | no |
| consent | `I have read and agree with privacy policy` | yes |
| submit | `Submit` | - |

1. The form validates itself rather than leaving validation to the browser. Every form on
   the site rejects invalid input inline, names the field it is complaining about, and
   **writes nothing** when it does.
2. Submission is guarded against automated abuse, and the guard **degrades to a usable state
   if the verification service cannot be reached rather than blocking a genuine sender.**
   Spam protection refuses a form submitted by a bot: an unattended decoy field that a
   person never fills, or the same form submitted repeatedly in quick succession. A human
   verification challenge may be presented, and a visitor who passes it is not asked again
   in the same session.
3. Five failures are distinguished, each with its own message: verification unavailable,
   verification failed, input rejected, upload too large, and network failure. One vague
   message for five different problems is not acceptable.
4. The attachment limit is two megabytes. An oversized attachment is rejected as invalid on
   its own, the limit is stated, and the rest of the form is kept.
5. On success the form is replaced in place by a success block titled `thank you`. **The
   replacement is announced to assistive technology and focus moves into it**, because a
   silent in-place swap leaves anyone not looking at the screen with no idea the message
   was sent.
6. The same markup serves the contact form and the deck request: the target is an attribute
   on the form, not a hard-coded path.
7. The capabilities deck control appears in the header, in the contact rail, on the hero
   card and in the textured band. It opens a modal titled `Capabilities` and `Deck` asking
   for name, company and email, whose success block reads `Great!` and
   `We've received your request, our Capabilities Deck will be in your inbox within a day.`
8. The published email address must not appear as plain text in the served document, and
   must be present and selectable after load. If the decoding fails the link must still
   resolve, so a working fallback is rendered rather than an empty anchor.
9. Below the submit bar the contact route offers the longer path, reading
   `Rather tell us properly? Start a brief.` **The short form is never removed in favour of
   the long one.** A five-field form and a staged brief serve different people.

### Brief Studio

`/brief/` is the primary path, six stages, each one screen and each independently
addressable so the browser's back button moves between stages rather than leaving the brief.

| Stage | Question | Asks for | Required |
|---|---|---|---|
| 1 | `First, who are you?` | name, company, email, phone, current site | name, company, email |
| 2 | `What do you need from us?` | the twenty services as selectable pills | at least one |
| 3 | `This looks like...` | one of four engagement shapes, derived and confirmed | yes |
| 4 | `When, and roughly what size?` | a timing band and a budget band | timing |
| 5 | `Now, a little about my project...` | the free text field and the attachment | no |
| 6 | `Let us talk. Times shown in <TIME_ZONE>.` | the slot picker | no |

Stage two reuses the same twenty service names as the home route index, and stage five the
same upload control and the same two megabyte limit as the contact form. A visitor who read
the service index recognises the list, and a new vocabulary at the point of enquiry costs
enquiries.

1. **Stage three does not ask an open question.** It proposes an engagement shape derived
   from the stage two selection, states the reason it derived it, and lets the visitor
   correct it under `Not quite. It is more like...`. A derivation the visitor cannot see or
   change is a guess wearing a suit. The four shapes: `identity` when branding, corporate
   identity or logo design were selected with no development, shown as a brand programme;
   `product` when product design, UX or UI were selected, with or without development, shown
   as a product engagement; `build` when frontend, backend, DevOps or analytics were
   selected with little or no design, shown as a build engagement; and `full-cycle` when the
   selection spans design and development, shown as an end to end programme.
2. Budget and timing are bands, never a free number. A free number field on an agency brief
   produces either a refusal to answer or an anchor nobody meant. The timing bands:
   exploring with no date, within three months, within six months, already started. The
   budget bands: `Still working it out`, under the first threshold, the middle band, the
   upper band, above the upper band. The thresholds are content rather than code and live in
   the brief record so they can change without a deploy. **`Still working it out` is a
   first-class answer and must not be styled as a lesser option.**
3. **Saving and resuming.** The record is saved after every completed stage and on a two second pause in any text
   field. The first save issues an opaque, unguessable token, the resume path is
   `/brief/<brief-token>/`, and the link is shown on screen and sent to the address once one
   is present, reading `Saved. Your link is in your inbox.` Returning reads
   `Picking up where you left off.`
4. **The resume link is a bearer credential.** It must not be indexable, must not appear in
   a referrer, must expire thirty days after the last edit, and **must not carry the
   visitor's email address in the path**, which is the usual shortcut and which leaks that
   address into every log it touches. The current stage is also held in the browser so a
   lost connection loses nothing.
5. **No failure at any stage may return the visitor to stage one.** Verification
   unavailable: the brief is accepted, the visitor is told it is received, and verification
   happens server side. Slot taken: everything is kept and the two nearest free slots are
   offered. Attachment too large: only the attachment is rejected and the limit is stated.
   Network lost mid-submit: the brief is retained locally, the submission is retried, and
   the visitor is never shown an empty form.
6. On success the visitor lands on a full-page confirmation reading
   `Booked. We will see you then.`, naming the booked time in the visitor's own zone and in
   the studio's zone.
7. What the studio receives is one record and one notification carrying the derived shape,
   the discipline selection, the budget and timing bands, the booked slot in both zones, the
   free text and a link to the attachment, sorted so the studio can triage without opening
   anything.

### The slot picker

1. Slots come from the studio's **published availability document, never from a live
   calendar.** This is a privacy requirement as much as an architectural one: the studio's
   real calendar must never be exposed to an unauthenticated visitor, and a published
   availability window leaks nothing about what fills the rest of the week.
2. Slots are thirty minutes and the horizon is fourteen days forward, no more.
3. **The visitor's time zone is detected, displayed by name, and made overridable before any
   slot is drawn.** `Not your time zone? Change it.` sits beside it. A visitor who reads a
   grid of times, chooses one, and only then discovers the times were in the studio's zone
   has been actively misled, and it is the single most common defect in booking interfaces.
4. Selecting a slot places a soft hold, reversible until submission, released after fifteen
   minutes of inactivity.
5. **Two visitors selecting the same slot within the hold window is normal, not
   exceptional.** The second is refused **at submission, not at selection**, because
   refusing at selection requires a live connection the visitor may not have. Exactly one of
   two simultaneous submissions for the same slot is booked; the other is rejected and told
   which slot went, in the words
   `That time went while you were writing. The two nearest are below, and nothing else was
   lost.`, with the two nearest free slots offered by name. **The refusal must not lose any
   other answer in the brief**, including the free text and the attachment.
6. The picker is fully operable by keyboard: the day columns form a grid, the arrow keys
   move between slots, and the selected slot is announced together with its time zone.
7. The picker never animates between weeks; it changes its content in place.

### The tone board

An optional board, offered inside the brief under `Optional: show us how it should feel.`

1. A square field ruled with the faint grid rule carries two labelled axes: `restrained` to
   `expressive` across, and `classical` to `contemporary` up. Thirty word tiles sit in a
   tray beneath it, drawn from the capability keyword pool and rendered as tag pills.
2. A tile is picked up by pointer or by the space key on a focused tile, follows the pointer
   with a ghost left in the tray, and on release carries a little inertia, continuing and settling
   just past where it was let go before returning. Position is continuous and meaningful; there is no
   grid to snap to. A tile on the board takes a solid fill. Dragging a tile off the board
   returns it to the tray.
3. **Eight tiles is the limit, and the ninth prompts a swap rather than being refused
   silently**, reading `Eight is plenty. Swap one out?`
4. Arrow keys move a picked tile a small step, holding shift moves it a larger one, and
   enter drops it. Dragging on a touch screen does not capture the page's scroll outside a
   tile drag.
5. The board produces a tone signature: two axis values and the chosen words, shown back as
   a sentence and carried into the brief record, and rendered alongside the brief at
   `/brief/<brief-token>/`.
6. **The board is skippable under `Skip this`, and skipping it must not present the brief as
   incomplete.** It is an invitation, not a gate.
7. **A list view is available at all times and is not a lesser path**, offered as
   `Use the list instead`. It carries the same thirty words with two sliders each and
   produces an identical output. The board and the list are two presentations of one state,
   and switching between them mid-arrangement loses nothing.
8. Every tile is a focusable control with an accessible name, and its position is announced
   as two named regions rather than as coordinates, for example `expressive, contemporary`.

### The capabilities deck composer

The reference path stays: name, company and email, and a deck promised by email. The modal
gains a second option reading `Build one now`, which opens `/deck/`.

1. Three questions on one screen, no stages: `What are you working on?` (the four engagement
   shapes, which select the case set and order the discipline pages),
   `What is your sector?` (the five sectors plus `something else`, which promotes cases from
   that sector), and `How much detail?` (`Overview`, `Standard`, `Deep`, which sets the page
   count at roughly six, twelve or twenty).
2. Assembly is from typed blocks, never from a template per permutation. Always
   present: a `Cover` carrying the visitor's company name when one was given, a
   `What we do` block of the twenty services ordered by the chosen shape, an `Approach`
   block of the four capabilities in the shape's order, and a `Next step`. Three to eight
   `Case` blocks are selected by sector match first, then shape match, then recency.
   `Figures` blocks appear at `Standard` and `Deep`; `Team` blocks (disciplines and
   distribution, no named individuals) and `Ways of working` blocks appear at `Deep` only.
3. **The `Next step` block links into the brief with the composer's answers carried across**,
   reading `Start a brief from this`. A deck that ends in a dead end wastes the one moment
   when the reader is certain to be interested.
4. The composed deck is a read-only paginated route at `/deck/<deck-token>/`, rendered in
   the same design system as the rest of the site. **There is no downloadable file. The link
   is the artefact.** The token is opaque, unguessable and not indexable, the deck lives
   ninety days and the studio may extend it, the whole deck is one document so no page waits
   on a later fetch, and printing it produces one deck page per sheet with no cropped media.
5. What the studio learns from a deck: the first open timestamp, the furthest page reached
   and the set of pages viewed, aggregate seconds on each case page, whether the token was
   opened from a new context, and whether a brief was started from it.
6. **The limits on that are requirements, not courtesies**: no identification of a forwarded
   reader, no location beyond time zone, no fingerprinting, and a plainly worded line on the
   **first page of every deck** reading
   `Whoever sent you this deck can see which pages were read.` Telemetry the reader is not
   told about is surveillance.
7. If the composer is unreachable the site falls back to the modal and the emailed deck.
8. **An expired deck token and a revoked deck token produce an identical response**, reading
   `This deck has expired. Ask for a fresh link.` with a control to request one.
   Distinguishing them tells a stranger that the token was real.

### The engagement portal

`/portal/`, the only authenticated surface and the only one holding another company's
confidential material. It is not linked from the header; it is reached from a link in the
engagement's welcome email and bookmarked thereafter.

It is read-mostly with exactly one write action that matters. Six panels:

| Panel | Shows | Register |
|---|---|---|
| `Right now` | the current phase and what the studio is doing this week, one line | read only |
| Milestones | the engagement's phases with dates, the current one marked | read only |
| `Waiting on you` | deliverables awaiting approval and questions awaiting an answer | actionable |
| Deliverables | every delivered item, newest first, with version history | read, comment, approve |
| People | who is on the engagement, by discipline, no personal contact details | read only |
| Documents | the submitted brief, the tone board and the agreed scope | read only |

The `Right now` panel is one line and it is first, because it is the question every client
actually opens the portal to ask.

1. **Every record is scoped to one engagement, and no query may be satisfiable without an
   engagement identifier the signed-in account is attached to.** Access control is enforced
   where the data lives, not in the interface: an interface that fetches a deliverable and
   then decides whether to show it has already fetched it, and the first defect in a
   rendering path leaks another company's unreleased brand. A request from
   `client2@example.com` for a `Northwind Aero` deliverable, comment, version or approval is
   denied and **no part of that record appears in the response**.
2. A deliverable is a named item with numbered versions, each carrying a date and a preview
   **rendered in the browser, never a download-only item.**
3. Comments are threaded per version, resolvable, and record the resolver and the time. A
   comment may be pinned to a point on a still.
4. The two decisions are `Approve` and `Request changes`, the second under
   `What needs to change?`. **A request for changes without a note is rejected as invalid
   and records nothing.**
5. **Only an account carrying the approval right on that engagement may approve**, enforced
   where the data lives. A direct approve request from `client2@example.com` is denied and
   the version's state is unchanged.
6. **An approved version is frozen.** A change creates a new version rather than altering
   the approved one, and the frozen version reads
   `Approved <DATE> by <ACTOR>. Changes create a new version.`
7. **Approval is a record, not a state flag.** Every approval, rejection and comment is
   recorded with its actor and its time, and is never deleted, only superseded. Months later
   both sides must be able to answer who approved what and when, and a state flag cannot
   answer that.
8. Notification is a digest rather than an alert per event, defaulting to `Daily` and
   settable to `Weekly` or `Off`.
9. **Nothing in the portal is pinned and nothing is driven by scroll.** The public site is a
   performance; the portal is a tool, and a client checking a deliverable late at night
   should not have to scroll through choreography to reach it.
10. A second factor is required for any account carrying approval rights.

### The published surface

1. A privacy page at `/privacy-policy/`, reachable from the footer of every page, states
   what Sable stores about a visitor and how long it is kept. It carries an effective date
   and eight numbered sections: `1. Introduction`, `2. What We Collect`,
   `3. How We Use Your Information`, `4. File Uploads`, `5. Cookies`, `6. Data Storage`,
   `7. Your Rights`, `8. Contact`. What it says is collected: first name and last name,
   email address, phone number, company name, message content, and uploaded files such as
   briefs and project documents. What it says those are used for: to respond to inquiries or
   proposals, to communicate about potential collaborations, to review submitted project
   materials, and to analyze site traffic to improve user experience.
2. **The policy must also name every collection point the newer surfaces introduce**: brief
   drafts held against a resumable token, booked call slots and time zone, deck composition
   choices and read telemetry, tone board arrangements, and portal accounts, comments and
   approval records. A collection the policy does not name is a defect, and the policy
   amendment that names them ships before the features it describes rather than after.
3. A terms page at `/terms/`, reachable from the footer of every page, and linked from the
   signup form.
4. A first-time visitor is asked once about non-essential cookies, and the answer survives a
   reload.
5. An unknown address renders Sable's own not-found page, carrying a way back to the home
   route, and answers not-found rather than answering as though the address existed.
6. Each page view is recorded with its route and a timestamp, readable by `studio` and by
   nobody else.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the nine-band home route | public |
| `/contact/` | the one-screen enquiry form | public |
| `/privacy-policy/` | the privacy document | public |
| `/terms/` | the terms document | public |
| `/work/` | the filterable case archive | public |
| `/work/<case-slug>/` | one case study | public when published, `studio` otherwise |
| `/brief/` | stage one of the staged brief | public |
| `/brief/<brief-token>/` | resume or read back a saved brief | the token |
| `/deck/` | the deck composer | public |
| `/deck/<deck-token>/` | a composed deck, read only | the token |
| `/portal/` | the engagement portal | `client` or `studio` |
| `/login` | sign in | public |
| `/signup` | create an account | public |
| any unknown address | the not-found page | public |

Trailing slashes are significant on the sub-routes: `/contact` is a permanent redirect to
`/contact/`.

**Entry and redirects.** An unauthenticated request for `/portal/` lands on `/login` and,
after a successful sign in, continues to `/portal/` rather than to the home route. A
`client` session requesting a `studio`-only endpoint is denied. A bearer token that expires
mid-action leaves the record untouched, returns the visitor to `/login`, and carries them
back to what they were doing once they sign in again. A used or expired sign-in link lands
on `/login` with a control to request a fresh one. Signing out clears the session on that
device and offers to clear every session. An expired or revoked brief token gives the same
page with a control to start again; an expired or revoked deck token gives the same page
with a control to request a fresh link. A renamed case's old slug permanently redirects to
its current one.

**Journeys.**

1. *A stranger reads a case and sends it on.* Open `/work/`, narrow to `HEALTHCARE`, read
   the live count beside every remaining facet value, open `Bridgeline Health`, read it from
   `cover` to `outcome` using the chapter rail, drag the comparison divider, copy the
   address. The address opens on the case for somebody who has never seen the home route,
   with no home route load.
2. *A prospective client books a call.* Open `/brief/`. Stage one: a name, a company and an
   email. Stage two: select `Brand Identity Systems` and `Motion Design`. Stage three: the
   site proposes `identity`, states why, and the visitor overrides it to `full-cycle`. Stage
   four: `within three months` and `Still working it out`. Stage five: the free text and an
   attachment under the limit. Stage six: the zone is named, the slots are drawn, one is
   selected and held. Submit. The full-page confirmation names the booked time in both
   zones, and the attachment exists in the bucket at its key.
3. *The brief survives an interruption.* Reach stage four, close the tab, open the resume
   link. Every answer is where it was, at stage four.
4. *Two visitors want the same slot.* Both select the last free slot on the first day inside
   the hold window and both submit. One is booked. The other is refused at submission, keeps
   every answer including the free text and the attachment, and is offered the two nearest
   free slots by name.
5. *A marketing lead composes a deck.* Open the deck modal, choose `Build one now`, answer
   the three questions at `Standard`, open the composed deck. The telemetry line is on the
   first page. Printing gives one deck page per sheet. The closing link opens `/brief/` with
   the shape and sector already filled in.
6. *A client approves a deliverable.* Sign in as `client@example.com`. `Right now` is one
   line and first. Open the version in `Waiting on you`, pin a comment to a point on the
   still, approve it. The approval names actor and time, the earlier version is still
   present, and the approved one is frozen.
7. *A client without the right is refused.* Sign in as `client2@example.com` and attempt to
   approve a version on the `Bridgeline Health` engagement. Denied, and the version's state
   is unchanged. Request changes with no note: also denied.
8. *A client cannot reach another engagement.* Signed in as `client2@example.com`, request
   the `Northwind Aero` engagement directly. The record is not returned.

**States.** Every list has an empty state that says what would fill it: an archive filtered
to nothing names the nearest non-empty filter and offers it; a portal panel with nothing
awaiting a decision says so rather than sitting empty; a brief with no attachment says the
attachment is optional. Every route has a loading state, and the first is the loader itself.
No error crashes the app or leaves a blank page: every revealing element releases its
content regardless after a short deadline, so a page of invisible text is not reachable.

## UI/UX notes

The direction comes from the studio the site is for: considered, performative and exact,
with the craft itself as the evidence. The north star is that in the first moment a visitor
should understand this studio decided every edge, and the register is editorial on the
public routes and operational inside the portal. Those two are not in tension. The public
site is a performance and may carry atmosphere with the work seen first; the portal is a
tool that keeps the same kit of parts and drops the choreography entirely.

There are exactly two grounds and the page cuts between them at a full-bleed edge rather
than blending: pure black, a near-black neutral, and pure white, a near-white neutral, with one marginally lighter
near-black neutral reserved for a single inset panel. Text is pure on both: the light ground
carries pure near-black neutral text, the dark ground pure near-white neutral text, with no
softened near-black and no off-white, because that purity is what makes the hard cut work.
There is one accent, a mid, vivid teal, and it appears almost nowhere: behind selected text,
on the pointer dot, and as the marker showing which chapter or which deliverable you are on.
It is never a fill, never a button and never a heading colour. A near-white warm neutral, bone,
serves as a second, sparing accent. Rules are a mid neutral at full and half strength, with
a deep neutral at low alpha for the faint grid rule. Form errors are the only light, muted
red on the site. The generated stills draw their grounds from deep and near-black neutrals
and their lights from a mid neutral, a light neutral and a near-white neutral. No colour
interpolates into another; the only two gradients fade one colour to transparent.

Type is four voices with four jobs, and the families are exact: `Kamerik205`, a geometric
grotesque, for display and the wordmark; `PPNeueMontreal`, a neutral grotesque, for reading;
`FreigBigProLigIta`, a high-contrast didone at a light weight, as the counter-voice, which
must look fragile beside the display face rather than merely different; and
`AkkuratMonoLLWeb`, a monospace, for every label, caption, address and piece of metadata.
The monospace is the interface voice, and it is what makes the site read as a technical
document wrapped around an art book. The sizes are exact too: display at `176.4px`,
`121.275px` and `80px` across the three tiers, section titles at `60px`, `41.25px` and
`40px`, the counter-voice at `33.75px` and `23.2031px` and at `217.5px` in the What We Do
pairing, subsection titles at `30px`, case names at `22px`, lead paragraphs at `20px`, body
at `18px` and `16px`, monospace labels at `16px` and `14px`. Three ratios are the whole
system: display line boxes sit at `0.84` of the font size, titles at `0.88`, reading text at
`1.5`, and monospace labels at `1.00` where the line box is the cap height by design. Line
boxes shorter than the font size on every display step is the detail a rebuild loses first.
Display faces are tracked a little tighter than normal, the body face tighter still, and the
monospace is never tracked; the rule follows the role, not the family, so the body face used
at display size takes the display tracking.

Every major heading is a pair: a roman span in the display face and an italic span in the
counter-voice set larger, on the same baseline, offset so the two interlock rather than
sitting side by side. They arrive from opposite sides and land together, the italic
travelling more than twice as far. The What We Do pairing is the one exception and the one
piece of outlined type on the site: its italic word is stroked with no fill, sitting behind
the filled roman words at roughly twice their cap height and bleeding off the frame's left
edge.

Roundness carries meaning and the tiers are far apart on purpose: anything you press is a
full stadium with round ends, panels are softly rounded rectangles, and the discipline tags
are barely rounded at all, which is how a reader knows at a glance that a tag is information
rather than something to press. Nothing floats: there is no drop shadow anywhere, and the
two inset strokes that do exist are drawn so they cannot affect layout. Hairlines read as
one device pixel rather than one reference pixel, which is the difference between a rule
that sits behind the type and one that argues with it. The public routes are spacious, with
a tight frame gutter and a generous vertical rhythm; the gutter grows and the header shrinks
on the phone, which is the opposite of the usual move and is deliberate. The portal is
comfortable rather than spacious, because a client is scanning for one thing.

The motion character is eased throughout, and specifically everything arrives late and
settles: movement is slow at both ends with a fast middle, and nothing on this site snaps.
The perceived quality comes almost entirely from the length of that deceleration. Named
moments, in words: a title arrives a little too wide and squeezes to its proper width, which
is a squash rather than a fade and is most of why the headings read as typeset; case media
is wiped in from a corner that alternates as the reader descends; a left-edge curtain opens
across the latest-case panel, its open width expressed as the remainder of its container so
it keeps its proportion at any width; each dot in the field drifts away from an unseen home
and returns; one element changes in no time at all but a fraction of a second late, so that
whatever was moving has finished first, and dropping that wait shows a flash of the hidden
element; another moves first and only then moves its own anchor point; a divider and a
dropped tile overshoot their target and return, which is the only motion on the site that
passes where it is going and is used in exactly two places; one marquee runs a single continuous loop, the only
looping motion on the site; and the loader's label rises at a constant rate rather than easing, because
it is reporting progress. The fixed chrome does not switch between a light and a dark
variant: the header and the pointer ring render as the inverse of whatever passes beneath
them, continuously and per pixel, so one wordmark serves both grounds and the textured band
between them. A build that swaps colours at the boundary will visibly step as the reader
scrolls past the join.

Reduced motion is honoured everywhere and it must not produce a grey, motionless version of
the site. Every reveal resolves to its end state with no timeline created, every scrubbed
property sits at its end value with the scroll smoothing removed and native scrolling
restored, the marquee shows its first frame, the rotating mark is still, the pointer
replacement is not rendered and the system cursor returns, the loader is skipped entirely
including on a first visit, and no video is autoplayed: the generated poster stands with a
play control. What is lost is travel, not character, and the site must still be recognisably
itself, with the same layout, the same hard cut between grounds, the same type pairings and
the same corner-clipped images resolved to open. Nothing on the site may animate against a
reader who has asked it not to.

The site commits to one scheme and designs it fully: the two grounds ARE the design, the
dark ground and the light ground alternating band by band on one page, and there is no
separate dark theme layered over them. A reader's own colour-scheme preference changes
nothing here, and neither scheme is graded against the other.

The layout archetype is a fixed top navigation, and it is deliberately not a single even
row: two links stack in one column, a third takes its own column, and the fourth is pushed
to the right edge, an asymmetry visible at every scroll position. Every control carries a
resting, pointed-at, pressed, focused and unavailable state; the escape key closes every
overlay; a destructive action confirms first; and unavailable is never signalled by colour
alone. Overlays trap focus inside themselves and return it to whatever opened them.

The accessibility floors are contract rather than taste, and they are stated as values
because plain language genuinely underspecifies them. Text and its background meet WCAG AA
contrast on both grounds and in the generated imagery. Every control has a comfortably sized
touch target, including the discipline tags and the slot controls, which are the two most
likely to fall under it. Keyboard navigation reaches everything with a visible focus ring
that survives the inverting chrome, because a blended focus ring is not a focus ring, and
focus order follows reading order at every width including the staggered case grid where
visual order and source order diverge. Icon-only controls carry labels, meaning is never
carried by the accent alone, and the split positioning line keeps the whole sentence as its
accessible name so it reads as a sentence rather than as loose characters. The type scale
grows from the reader's own root size preference rather than being pinned, keeping every
ratio: the ratios are what make it look like itself, not the absolute values.

The design holds at three widths, phone, tablet and desktop, with a correction at the very
small and the very large end, and it must hold at every width between those tiers rather
than only at them. At a narrow viewport nothing overflows sideways and every navigation
target stays reachable. The service index runs four columns, then two, then one; the client
index five, then three, then two; the case grid three staggered columns, then two, then one;
the navigation becomes a menu button. Above the largest tier the frame stops growing and the
gutter absorbs the excess rather than the columns widening. Two responsive rules are
substitutions rather than degradations: the case reveal is a corner wipe on desktop and a
fade on the phone, and the pinned capability band does not pin on a phone at all. The phone
home route comes out taller than the desktop one; a phone build that is shorter has dropped
a band.

Each page leads with one clear primary action, visually distinct from every secondary one,
and every content image carries alternative text while a decorative one declares itself
decorative.

What it must not look like: a page dominated by one hue family with no second signal;
decoration standing in for content; or a marketing composition where the working interface
belongs, which is the trap the portal sits one decision away from. The stances, each of
which a competing studio could rationally invert: space over dividers, character over
decoration, two grounds over a tonal ramp, alternation over randomness, and restraint with
the accent over reaching for it. The exact values behind these words are yours, so long as
they hold the relationships and the exclusivity rules above.

## Technical requirements

The rendering model is server-rendered HTML with hydrated islands. The marketing routes, the
archive and the case study routes are produced as HTML on the server, so the first thing the
browser receives carries the words rather than an empty shell waiting on script; only the
parts that need behaviour are hydrated. Build the front end with **SvelteKit**, which serves
those documents and their islands, and the HTTP API with **Express**, on the same origin
under the `/api` prefix. Persist to **PostgreSQL**, reached at `DATABASE_URL`. Store every
uploaded byte in **MinIO**, reached at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`,
`STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The app's own address and port come from
`APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a host or a port; read every one of
them from the environment. Both backing services are **already running** and reachable at
those variables and must not be downloaded, installed, compiled or started.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing
services available in this environment are PostgreSQL and MinIO, and reaching for anything
else is a contract violation.

Authentication is app-implemented email and password with bearer tokens, plus the
single-use portal sign-in link described above, which exchanges for the same session.
Passwords are hashed. `GET /api/health` returns `200` once the app is ready. Request logs go
to standard output, one line per request, carrying the method, the path and the outcome.

**No credential, API key, bucket secret or admin token appears in anything the browser
downloads.** That includes the served HTML, every script and stylesheet it fetches, every
JSON response to an unauthenticated request, and any inline configuration object. The
storage credentials are read on the server and never reach the client.

**Every public route carries its own title and description, and no two public routes share
them.** A case route's title is the case name followed by the studio name, its description
is the positioning line from its `cover` chapter, and it declares a social preview image and
an article record naming the case, the client sector and the date.

Every module that binds to scroll, pointer or resize exposes a way to start and a way to
stop, and a route change stops every one of them before the next route starts. The
observable consequence is the one that matters: after twenty navigations the home route
scrolls as it did on the first load, and memory does not climb with the count. The portal,
the brief, the deck composer and the archive must not pull the marketing routes' motion
code, and the portal loads nothing that binds to scroll at all.

Video is the whole performance budget on a site like this: on the reference it was the large
majority of everything transferred and code, type and styles together were a rounding error
beside it. So the discipline is staged: a video's source begins loading two viewport heights
before the element arrives and playback begins one viewport height before, never both at
once, because a single trigger that does both stalls on a slow connection and the reader
meets a black panel. A video resets when it leaves the frame in either direction. Every
video has a generated poster present before it, every autoplayed video is muted and plays
inline, and one modern codec with one broadly compatible fallback is enough. At most three
renditions are selected by frame width rather than by guessing at the connection. Under
reduced motion or a data-saving preference no video loads at all and the poster stands with
a play control. Only the hero video may load before interaction.

The human-verification guard loads when a form is first focused rather than in the document
head, and the page-view record is written after the opening sequence finishes. The type
families are subset to Latin, the display face and the monospace are preloaded because they
carry the first screen, and font loading swaps rather than blocking.

Everything driven by scroll is a transform, an opacity or a clip. The dot field is driven as
one movement per dot rather than as attribute writes, and the whole scroll path holds the
device's refresh rate on a three-year-old laptop. Only one region is pinned at a time; two
overlapping pinned regions is the usual cause of a jump.

## Data model

Twenty-one tables. All timestamps are UTC, and calendar-day logic uses server-side UTC
today.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture
data, not a secret. Hash it as normal; the exact literal must work at login, and it must be
written into `/app/USER_README.md` alongside each account so a grader can sign in.

**`account`** - `id`, `email` (unique), `password_hash`, `display_name`, `role` (`studio` or
`client`), `created_at`.

**`session`** - `id`, `account_id`, `token`, `expires_at` (thirty days from issue).

**`signin_link`** - `id`, `account_id`, `token`, `expires_at` (fifteen minutes from issue),
`used_at`. A used link cannot be used again.

**`case`** - `id`, `slug` (unique, never reused), `name`, `sector` (one of `FINANCE`,
`TECHNOLOGY`, `HEALTHCARE`, `AGENCY`, `ECOMMERCE`), `kind` (one of `BRANDING`, `WEB`,
`PRODUCT`), `year`, `positioning_line`, `selected` (whether it appears in the home route
band), `published`, `shape`. `tags` is a list drawn from the twenty-four discipline tags.
The wipe corner is **derived from the case's position in the archive and is not a stored
field**: storing it per case invites an editor to pick a favourite, which destroys the
alternation.

**`case_chapter`** - `id`, `case_id`, `ordinal`, `type` (one of `cover`, `context`,
`figures`, `still`, `compare`, `sequence`, `motion`, `quote`, `stack`, `outcome`), `body`,
`media_key`, `caption`. The first chapter of a case is `cover` and the last is `outcome`,
and a case with fewer than four chapters cannot be published.

**`case_figure`** - `id`, `case_id`, `label`, `value`. Used by the comparison tray; a case
that publishes none leaves the row reading `not published`.

**`case_redirect`** - `old_slug` (unique), `case_id`.

**`service`** - `id`, `name`, `column_index`, `row_index`. The twenty service names in the
measured order.

**`capability`** - `id`, `number`, `title`, `keyword_one`, `keyword_two`. Four rows.

**`keyword`** - `id`, `word`. The thirty-word pool.

**`discipline_tag`** - `id`, `label`. The twenty-four tags, stored upper case, because the
reference carries them in mixed case and that is an inconsistency rather than a system.

**`studio_detail`** - the single row holding the published studio identity: the street line
`Suite 200-000 0 Ave SW`, the city and province line `Riverbend, AB`, the postal line
`A0A 0A0`, the country `Canada`, the phone `+1 (000) 000 0000`, the published address
`hi@example.com`, and the founding mark `EST. 2023`.

**`social_profile`** - `id`, `kind`, `url`, `ordinal`. Five rows in this order: the
professional network profile, the photo social profile, the design community profile, the
general social profile and the short-post social profile. A row with no url renders no mark
rather than an empty one.

**`client_record`** - `id`, `name`, `sector`, `listed`. The client index is deliberately
longer than the case archive: the studio lists more clients than it shows work for.

**`brief`** - `id`, `token` (unique, opaque, unguessable, **never derived from an email
address**), `stage`, `name`, `company`, `email`, `phone`, `current_site`, `shape`,
`shape_overridden` (whether the visitor corrected the derivation), `timing`, `budget`,
`narrative`, `tone_axis_x`, `tone_axis_y`, `created_at`, `updated_at`, `expires_at` (thirty
days from the last edit). `shape_overridden` is stored because a studio reading a hundred
briefs learns more from where its derivation was wrong than from where it was right.

**`brief_discipline`** - `brief_id`, `service_id`. The stage two selection.

**`brief_tone_word`** - `brief_id`, `keyword_id`, `x`, `y`. At most eight rows per brief.

**`attachment`** - `id`, `brief_id` or `version_id`, `object_key`, `byte_size` (at most two
megabytes), `content_type`, `scanned`. Bytes live in the bucket at `object_key` and nowhere
else. An unscanned attachment is readable by nobody.

**`availability_slot`** - `id`, `starts_at` (thirty-minute granularity, at most fourteen
days forward), `state` (`free`, `held` or `booked`), `hold_token`, `hold_expires_at`
(fifteen minutes from the hold).

**`booking`** - `id`, `slot_id`, `brief_id`, `studio_zone_rendering`,
`visitor_zone_rendering`. **A slot reaches `booked` at most once: two simultaneous
submissions for the same slot produce exactly one booking, the other is rejected, and the
slot never ends up with two bookings.** A rejected submission leaves the rest of that brief
untouched.

**`deck`** - `id`, `token` (unique, opaque, unguessable, not indexable), `company`, `shape`,
`sector`, `detail` (`overview`, `standard` or `deep`), `created_at`, `expires_at` (ninety
days), `revoked`. **An expired deck and a revoked deck are indistinguishable in the
response.**

**`deck_block`** - `id`, `deck_id`, `ordinal`, `type` (`cover`, `what_we_do`, `approach`,
`case`, `figures`, `team`, `ways_of_working`, `next_step`), `case_id`.

**`deck_read`** - `id`, `deck_id`, `context_id`, `first_opened_at`, `furthest_page`,
`pages_viewed`, `brief_started`. Carries no reader identity and no location beyond a time
zone name.

**`engagement`** - `id`, `name`, `client_record_id`, `phase_name`, `right_now_line`.

**`engagement_account`** - `engagement_id`, `account_id`, `can_approve`. **Every portal read
resolves through this table: a record is returned only when the signed-in account has a row
here for that engagement.**

**`milestone`** - `id`, `engagement_id`, `name`, `date`, `state`.

**`deliverable`** - `id`, `engagement_id`, `name`.

**`version`** - `id`, `deliverable_id`, `number`, `created_at`, `preview_key`, `frozen`.
**An approved version is frozen and never changes; a change produces a new version.**

**`comment`** - `id`, `version_id`, `account_id`, `body`, `position_x`, `position_y`,
`resolved`, `resolved_by`, `resolved_at`. Appended, never edited in place.

**`approval`** - `id`, `version_id`, `account_id`, `decision` (`approve` or
`request_changes`), `note`, `created_at`. `note` is required when the decision is
`request_changes`. **Rows are appended and never deleted, only superseded**, because both
sides must be able to answer months later who approved what and when.

**`page_view`** - `id`, `route`, `created_at`. Readable by `studio` only.

Derived rather than stored: the wipe corner, every facet count in the archive, the
similarity ordering, the deck page count, and the rendering of a booked slot in each zone.

**Seed data.** Three accounts as listed in `## User roles`. The twenty services, four
capabilities, thirty keywords, twenty-four discipline tags and five sectors with their
counts (`FINANCE` 9, `TECHNOLOGY` 5, `HEALTHCARE` 2, `AGENCY` 6, `ECOMMERCE` 2, twenty-four
in all against thirteen named cases). The client index carries the thirteen case names plus
eleven additional listed clients: `Payless Legal`, `Ironvault Holdings`, `Northwind Ops`,
`Ellis Hartwell`, `Milepost`, `Osric Ratings`, `Delta Interactive`, `Tilford Fibre`,
`Basis`, `Portway App` and `The Quite Funny Agency`. The thirteen cases with their sectors as listed above:
`Northwind Aero` and `Bridgeline Health` are published and each carries a full chapter set
including one `compare` and one `sequence`; `Token Market` is seeded **unpublished** so the
not-publicly-readable rule has a boundary; `Bridgeline Health` publishes no `figures`
chapter, so the comparison tray has a `not published` row to render. One availability
document with exactly **one free slot remaining on the first day**. Two engagements,
`Northwind Aero` and `Bridgeline Health`, each with milestones, one deliverable at two
versions, and one version awaiting approval. `client@example.com` is attached to
`Northwind Aero` with `can_approve` true; `client2@example.com` is attached to
`Bridgeline Health` with `can_approve` false.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual specification in full. Nothing here overrides a rule stated
above; it makes the look exact.

### Typography and elevation

The typography is the four voices and the three ratios stated above, and two further steps
belong with them: a subtitle step in the monospace that sits beneath a section title, and a
small monospace step for captions and metadata. Where the body face is used at display size
it takes the display tracking rather than its own, so the rule follows the role.

Elevation is twelve stacking levels and only a few of them matter. Full-bleed background
media sits behind the content. In-flow content sits at the base. Pinned section layers sit
above it. The fixed header and its parts sit above those. The capabilities modal and the case
overlay sit above the header. The loader and the pointer replacement sit at the top, with the
pointer above the loader, so the pointer is never occluded by anything, including an open
modal. There is no other elevation in the system and nothing may invent one.

The scrollbar track takes a near-white neutral of its own, which is the only chrome the
browser draws that this system styles.

### The frame and the grounds

The frame is gutter, content column, gutter, with the gutter unusually tight on desktop and
tablet and wider on the phone, which is what lets the client index run five columns to the
very edge. The header is a fixed band across the full width of the viewport. Its layout
token and the band it actually draws are **not the same measurement**, and both are in use:
the token is what anchored navigation offsets against, the band is what is drawn. Resolve
that deliberately, or every in-page anchor lands slightly out.

Three things are fixed to the viewport and survive every route change: the header, the
pointer replacement, and the award badge on the right edge. The award badge is third-party
furniture: build it as a slot that renders nothing when its token is empty, not as a
hard-coded element. It sits outside the header's subtree, because it must not invert.

The header carries, left to right: the wordmark linked to `/`, a small rotating mark beside
it, the `GET CAPABILITIES DECK` control, a spacer, `Projects` and `Services` stacked in one
column, `Agency` in its own column, and `Contact` ranged right. On the contact route the
wordmark shortens to a two-letter monogram.

**The inverting chrome is the whole trick and nothing inside the header may break it.**
Nothing in the header sets its own blend or its own background, the header takes no backdrop
treatment, and any element that must not invert lives outside it. Over the light ground the
wordmark renders dark, over the dark ground it renders light, and over the brushed metal
band it renders as a negative of the texture. There is no scroll listener changing a class
and there must not be one: the effect is continuous, and a class swap steps visibly at the
boundary.

### The pointer replacement

Two layers follow the pointer where the pointer is fine and hovering is possible, and
neither is rendered anywhere else, where the system cursor returns. A small dot in the accent
tracks the pointer with no perceptible lag. A ring, in the dark neutral, trails it, carries
the same inversion as the header so that it stays visible over the dark ground, and arrives
late with a slight overshoot on a fast movement. The ring is above everything, including an
open overlay, so it is never occluded.

### Stacking

Full-bleed background media sits behind the content. In-flow content, then pinned section
layers, then the fixed header and its parts, then the capabilities modal and the case
overlay, then the loader and the pointer, with the pointer above the loader.

### Rules, radius and strokes

Three rule strengths, used structurally: a solid hairline in a mid neutral for panel edges,
the same at half strength for the row rules in the service index, and a faint grid rule in a
deep neutral at low alpha for the horizontal rules that continue past content. Roundness
runs in tiers from a full stadium for the scroll hint and every pressable control, through a
circle for every close control, to softly rounded panels for the contact form and the portal,
a smaller rounding for the modal and the deck card, and barely any for the tag pills. There
is no drop shadow. Two inset strokes exist: one on the deck modal panel, one on the contact
submit control. Only two gradients exist, both fading one colour to transparent, and one of
them has both its stops at the same position so it draws as a hard band under the modal
header rather than as a gradient at all.

### Declared transitions and the declared keyframe set

The stylesheet holds the vocabulary and the code holds the choreography, and that split is
the architectural statement of this system. Almost everything that moves is driven from a
timeline; exactly one element, the loader's label, has its movement declared in the
stylesheet instead, and what the visitor actually saw there was a constant rate rather than
the eased one the declaration asks for, because a timeline took the element over. Build the
one that was seen and treat the declaration as the initial state it is overridden from.

Two of the declared transitions carry real design intent and are easy to lose. One is not a
transition at all but a delayed instant: the change happens in no time, a fraction of a
second late, so that whatever was moving has finished first, and a build that drops the wait
shows a flash of the element it was hiding. The other is a relay: the element moves first,
and only when it has finished does its own anchor point move, which is a piece of
choreography written into a single declaration.

The declared keyframe set is the site's own named animations plus a few that belong to
embedded third parties and are not the studio's to reproduce. The studio's own are: the
loader curtains sweeping open, the loader bar rising away, the loader label sliding up into
view, a text block leaving upward, the title settling from slightly too wide to its proper
width, the marquee running its single loop, the wordmark dropping in from above, and a hint
fading in and out again.

### Iconography

Every mark is drawn geometry inheriting the current colour, with no binary anywhere and no
mark setting its own blend inside the chrome. The set: a document with an upload tray beside
the deck control; an attachment mark in two states, a document with a plus in its empty state
and the same document with a check when a file has attached, swapped rather than animated
between; a cross inside a circle for closing the case overlay and the deck modal, which
rotates a half turn when pointed at; a pair of wireframe hemispheres bracketing the contact
rail, the same dome ruled with latitude arcs and the lower one mirrored, whose rules must be
drawn as arcs or the mark reads as a fan; five social marks at a small square size, of which
one was recovered whole and four are redrawn to match it; the dot field; a four-pointed
sparkle with strongly concave sides that rotates and fades with scroll; the award badge as a
vertical tab; and a single horizontal rule mark drawn in a much wider coordinate space than
it renders into, which is what lets it be redrawn as a hand-wobbled line without changing
its layout box. The wordmark is type, not geometry: set it, do not trace it. Only the
sparkle and the dot field carry their own fill; everything else inherits.

### The dot field

The largest drawing on the site: forty-two small dark dots paired with twenty-one large
unfilled circles. **Each unfilled circle is a dot's home position and is never visible.** The
dot is displaced out of its home by scroll and travels back towards it. That pairing is the
whole mechanism, and it is why the invisible circles are in the drawing at all. The
displacement is per dot and is defined in the drawing's own coordinate space, so it is
identical at every width.

### The scroll system

Scroll position is smoothed: an input impulse produces continued travel that decays rather
than stopping with the input. **Every scroll-linked animation reads from the smoothed
position rather than the native one**, or the two disagree by a frame and the whole page
shimmers. The smoothing must be removable at run time, because reduced motion turns it off
and a route change tears it down.

What is driven by scroll, and what it does: the dot field's circles, by far the most finely
driven thing on the page; the clip on case media, wiping from a corner; the media inside a
case panel; a case name, rising and fading into place under its panel; a capability number,
rising and fading in from nothing; the rules under the service index; the sparkle, rotating
and fading; the navigation items; both spans of a title pair, converging from opposite
directions; the rotating mark beside the wordmark, tracking a horizontal range; the hero
video and its cover, which begins fully collapsed and scales open; the tone words, fading in
sequence; and the loader's curtains and its line. Where a property is unchanged across a
stretch of the page it is genuinely parked, not merely unobserved, and a build that starts
moving it early reads as busy against a reference that waits.

Two pinned regions exist: the capability band, which holds while its four items advance, and
one trigger per case in the archive, whose bounds are clamped so that a case near the start
or the end of the document cannot resolve to a position that reveals it immediately on load
or never reveals it at all. The capability band's video container carries a shallow
perspective so the panels advance in depth rather than sliding flat, and its background is
built at the full content width and then compressed horizontally, so a build that makes it
at the size it appears will get it wrong.

Media loads two viewport heights before it arrives and plays one viewport height before, and
resets when it leaves the frame in either direction.

### Exit and teardown

The loader's exit is two separate moments and they are separate on purpose: content reveals
may begin at the first, and the loader element itself is removed from the document at the
second. Teardown is the same idea applied to every route change: every binding that listens
to scroll, pointer or resize is destroyed before the next route initialises, and a module
that cannot be destroyed does not belong in the build. A class that disables `pointer-events`
across a region is part of that teardown vocabulary: while an overlay is open the region
behind it does not respond to the pointer, and the disable is lifted when the overlay closes.

### The reveal contract

Every revealing element behaves identically, from one contract rather than twenty
implementations: a default duration and a short default delay, the site's workhorse
movement, triggered when the element's top crosses the foot of the viewport, resolving to
its end state under reduced motion, and a no-op when the element has already revealed.
**A reveal fires regardless after a safety deadline**, so a trigger that never fires cannot
leave a block invisible. A page of invisible text is the worst failure this design has
available, and that deadline is what makes it unreachable.

### The home route, band by band

**Hero.** A full-bleed video on the dark ground with no overlaid text. Its cover element
begins fully collapsed on both axes and scales open under scroll rather than being hidden
and shown, because a collapsed element can be scrubbed and a hidden one cannot. The hero
poster is generated.

**The studio strip.** Three monospace items in a row on the dark ground, upper case and
letter-spaced: `FULL-CYCLE DIGITAL AGENCY`, `EST. 2023`, `Canada`. It is the only place the
studio says what it is in plain terms and it is set at the smallest size on the page. That
contrast is the joke and it is preserved.

**The positioning line.** Breaking a string into per-character, per-word and per-line pieces
is done all at once and separately, because the reveal drives characters while the layout
must still break by line. The split is re-run on resize and **must be reversible**, because a split that cannot be undone
leaves the text unreadable to anything that is not looking at it. The line reads:
`We create premium digital experiences that express brand stories through design craft,
functional tech, and steady, unhurried craft.`

**What we do.** The twenty services in four ruled columns of five, set in the body face upper
case, under the outlined title pair, with the `SABLE APPROACH` affordance beside it.

**Tone words and the dot field.** `Vision.`, `Clarity.`, `Flow.`, `Execution.` fading in
sequence over the drifting dots, with the studio paragraph beside them and a hint element
that scales open from nothing when the field becomes interactive.

**Fresh Drop.** The latest case, its title pair setting `Fresh` in italic above and `Drop` in
the display face below and right, with a full-bleed still occupying the right half of the
frame behind a left-edge curtain, and the case name in the monospace beneath.

**The four capability features.** Pinned, on the dark ground, four numbered panels each with
a title and two cycling keywords, a video, and a compressed background sliding across as the
panel advances. A full-width call to action sits below with two mirrored arc decorations.

**Selected cases.** The staggered archive grid, its heading carrying the three kind counts.

**The capabilities band.** A full-bleed brushed metal texture carrying
`DISCOVER HOW WE CAN HELP - REQUEST OUR CAPABILITIES DECK` in centred upper-case monospace
with the stadium deck control beneath it. **This band is where the inverting header is
checked**, because it must render as a negative of the texture as it crosses.

**The hero deck card.** A small card near the top of the page carrying the same invitation in
miniature: a ruled sphere mark in a rounded tile at the left, the two lines
`Discover How We Can Help` and `- Request Our Capabilities Deck` in monospace, and a
`GET YOUR COPY` control. It fades in on scroll rather than on load.

**Clients.** A title pair setting `Clients` above `BRANDS` in the italic at a larger size,
then a two-part index: a sector column at the left with counts, and a five-column index of
client names at the right in upper-case monospace ranged left. **Each count is circled by an
irregular ellipse that crosses itself and does not close.** It is the one hand-drawn element
on the site and it must look drawn, not generated: a clean ellipse looks like a computer drew
it, which is the one thing this element must not look like.

**The footer.** The year mark `23-26` at the display face, very large, reading as an
operating span rather than a single year; the copyright line and `PRIVACY POLICY` in
monospace; the contact rail; and a full-bleed video panel at the lower left.

### The contact rail

The same order every time it appears: hemisphere dome up, the `address:` label and the four
address lines, a bullet, the `Phone:` label and the number, a bullet, the `email:` label and
the address, the deck control, a bullet, the `Social:` label and five marks, then hemisphere
dome down. Every label and every value is monospace, upper case, at the same size, and the
bullets are small filled circles used as separators rather than as list markers.

### The privacy and terms routes

Plain documents, the only routes on the site that are. The privacy route opens out of a
circular clip that grows from nothing, which is the only circular reveal on the site, and
carries a distinct footer treatment with the wordmark beside a three-letter monospace mark.

### Keyboard and forced colours

Keyboard handling inside an overlay is explicit: `Escape` closes it, `ArrowUp` and
`ArrowDown` move between its items, and `PageUp` and `PageDown` move a screen at a time.
Those five keys are handled in every overlay, the case quick look, the capabilities modal,
the slot picker and the tone board alike, and the handling is the same in each so a reader
learns it once.

A forced-colours branch is required: where the operating system overrides colour entirely,
the site must stay usable rather than disappearing. Under forced colours the inverting chrome
falls back to a solid ground with a visible border, the accent marker keeps its paired text,
and every focus ring stays visible. Honour a dark colour-scheme preference within that branch
rather than fighting it.

### The generated imagery: the zero-asset substitution guide

No binary ships. This is the substitution guide, one recipe per asset class the reference
served, and every one of them is drawn rather than fetched:

- **Case stills and poster frames**, which is the most-used recipe by far. Each still is
  generated from a seed derived from the case slug, so the same case always produces the
  same image: a ground tone and a light tone chosen from the neutral palette by the seed, a
  soft off-centre radial light, three to five large overlapping rounded rectangles, capsules
  and ellipses at low alpha and seeded rotations, a single directional blur along the
  dominant angle so the result reads as a defocused object rather than as flat shapes, and a
  grain overlay. Poster frames use the same recipe with a heavier blur, so the poster reads
  as a still of something and the video replacing it is not a visual jump. Aspect ratios are
  fixed so the grid does not reflow when real imagery arrives: three by two for archive
  stills, sixteen by nine for video posters, and four by five for the two portrait slots in
  the staggered grid.
- **The brushed metal band**: a neutral fill, two thousand faint horizontal one-pixel lines
  at random vertical positions and random lightness at low alpha, a horizontal blur with no
  vertical blur, which is what gives it its direction, a vertical gradient from light to dark
  to give the band its roll, and **one soft specular streak across the upper third, which is
  the detail that makes it read as metal rather than as noise.** Its position matters more
  than its intensity.
- **The feature panel background**: a dark fill, an off-centre radial highlight, and grain.
- **The loader mark**: a ruled sphere, twenty-four latitude ellipses inside a circle, stroked
  with no fill, drawn at a large intrinsic size and scaled down so its stroke weight stays
  constant. Animate it by scaling each ellipse's vertical radius through a sine over the
  loop, which reads as the sphere turning, not by rotating the whole drawing.
- **The rotating wordmark mark**: three concentric partial arcs at three radii, each turning
  at a different rate and the middle one counter to the others. **The counter-rotation is
  what stops it reading as a spinner.**
- **The circled counts**: an ellipse drawn as two overlapping arcs whose stroke crosses
  itself twice and does not close, with every control point perturbed by a value derived from
  the numeral, so each count is circled differently and the same count is always circled
  identically.
- **Share images**, generated per route from the still recipe with the route title set in the
  display face over it and the wordmark at the lower left.
- **Grain**, a tiling noise tile used by three of the recipes above, generated from
  turbulence at a low base frequency over four octaves, which gives a fine grain that does
  not visibly repeat across the tile, with its saturation reduced to nothing so it is tonal
  and does not tint what it sits on, applied at a low alpha and never a heavy one.
- **The four unrecovered social marks**, each a single solid path with no stroke, matched to
  the recovered mark's optical weight. Five marks of different weights in one row is the most
  visible failure available here.

Two things are not recoverable by any recipe and no substitution is attempted: the case
narratives and the real project photography are the studio's own work. The generated stills are placeholders that hold the layout at the correct
aspect ratios, and they are deliberately abstract so nobody mistakes one for a case.

## Constraints

- One studio. There is no multi-tenancy on the marketing routes, and the portal's tenancy
  unit is the engagement.
- Nothing on a marketing route waits on a query. Everything a visitor reads without
  identifying themselves is published and cacheable; everything else is a record behind a
  token or a session. There is no third category.
- No project management tooling, no chat, no folder-based file store, no downloadable deck
  file, no live calendar integration.
- No payments, no invoicing, no subscriptions, no pricing page. Budget is a band, never a
  number.
- No comments, likes, follows or messaging on the public routes.
- No external network calls at run time. No third-party analytics endpoint, no fingerprinting,
  no identification of a forwarded deck reader, and no location beyond a time zone name.
- No native application. The site is not expected to work with the network off, with one
  exception: a composed deck is one document, so no page of it waits on a later fetch.
- The build is zero-asset. **No binary asset of any kind ships**: no photograph, no video file, no font file, no icon
  file, no texture. Every mark, still, poster, texture and share image is generated, and the
  build must succeed with an empty asset directory.
- The four licensed typefaces are commercial licences, are not redistributable, and are
  **not** shipped. Name them,
  and fall back: the display voice through `Arial Black`, `Helvetica`, `Arial`,
  `sans-serif`; the body voice through `Helvetica Neue`, `Helvetica`, `Arial`,
  `sans-serif`; the counter-voice through `Didot`, `Bodoni MT`, `Georgia`, `serif`, always
  italic; and the monospace through `ui-monospace`, `SFMono-Regular`, `Menlo`, `Consolas`,
  `monospace`. Choose a substitute for cap height and character width rather than for
  character, because the line-height ratios were measured against the original metrics and a
  shorter cap height makes every heading look loose. Naming a widely available or openly
  licensed family is not an asset dependency; serving a licensed retail face is.
- Four behaviours are deliberately **not** reproduced from the reference and must be
  corrected: reduced motion is honoured rather than ignored; the desktop class is keyed to
  pointer capability rather than to a parsed device identifier; the width boundaries are
  standardised so there is no width at which no layout rule applies; and the root type size
  derives from the reader's preference rather than being pinned.
- The reference's own brand and its clients' names appear nowhere in the built output.
- The data volume the app must stay responsive at: a few hundred cases, a few thousand
  briefs, a few hundred composed decks, and a few dozen engagements each with tens of
  deliverable versions and hundreds of comments.

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
| `POST /api/auth/signup` | `{ email, password, display_name }` | `{ token, account }` |
| `POST /api/auth/login` | `{ email, password }` | `{ token, account }` |
| `POST /api/auth/signin-link` | `{ email }` | `{ sent }` |
| `POST /api/auth/signin-link/exchange` | `{ token }` | `{ token, account }` |
| `POST /api/auth/logout` | `{ all_devices }` | `{ ok }` |
| `GET /api/cases` | `?sector=&discipline=&kind=&q=` | a top-level JSON array of case summaries |
| `GET /api/cases/{slug}` | - | `{ case, chapters, figures, related }` |
| `GET /api/cases/{slug}/still` | - | the generated still for that case, byte-identical on every read |
| `GET /api/cases/facets` | `?sector=&discipline=&kind=` | `{ sector, discipline, kind }`, each value with its live count |
| `POST /api/cases/{slug}/publish` | - | `{ case }`, `studio` only |
| `GET /api/services` | - | a top-level JSON array |
| `GET /api/capabilities` | - | a top-level JSON array |
| `GET /api/availability` | `?zone=` | `{ generated, zone, slots }` |
| `POST /api/briefs` | `{ stage, contact, disciplines, shape, shape_overridden, timing, budget, narrative, tone }` | `{ token, stage, expires_at }` |
| `GET /api/briefs/{token}` | - | the brief record |
| `PATCH /api/briefs/{token}` | any subset of the create body | the brief record |
| `POST /api/briefs/{token}/attachment` | multipart file, at most two megabytes | `{ object_key, byte_size }` |
| `POST /api/briefs/{token}/hold` | `{ slot_id }` | `{ hold_token, hold_expires_at }` |
| `POST /api/briefs/{token}/submit` | `{ slot_id, hold_token }` | `{ booking }`, or a rejection naming the two nearest free slots |
| `POST /api/decks` | `{ company, shape, sector, detail }` | `{ token, expires_at }` |
| `GET /api/decks/{token}` | - | `{ blocks, cases, telemetry_notice }` |
| `POST /api/decks/{token}/read` | `{ page }` | `{ ok }` |
| `GET /api/decks/{token}/telemetry` | - | the read record, `studio` only |
| `GET /api/portal/engagements` | - | a top-level JSON array, scoped to the signed-in account |
| `GET /api/portal/engagements/{id}` | - | `{ phase, right_now, milestones, deliverables, people, documents }` |
| `GET /api/portal/versions/{id}` | - | `{ version, comments, approvals }` |
| `POST /api/portal/versions/{id}/comments` | `{ body, position_x, position_y }` | the comment |
| `POST /api/portal/versions/{id}/approve` | `{ decision, note }` | the approval record |
| `GET /api/objects/{key}` | - | the object bytes, authenticated and entitled only |
| `GET /api/health` | - | `200` |

Field names are exact. A list endpoint returns a top-level JSON array. A successful call
returns the named resource or shape; an invalid or unauthorized call is rejected as a client
error, never as a server error and never as a silent success. Bearer auth is required on
everything except signup, login, the sign-in-link endpoints, the public case, service,
capability and availability reads, the token-addressed brief and deck reads, and health.

### No mocks

PostgreSQL and MinIO are the facts. An in-memory array of briefs, a bookings list held in a
module variable, a hardcoded availability response the app answers to itself, attachment
bytes written to the app container's own filesystem or held in a database column, a
`scanned` flag set without anything having scanned, or a portal query that reads every
engagement and filters the result in the view: each of these is a contract violation however
good the interface looks. **The named provider is the fact - the app's UI and its own tables
can only reflect what lives in the provider, never substitute for it.**

## Definition of done

A visitor can read a case at its own address, compose a capabilities deck, and finish a
six-stage brief on a phone that ends with a discovery call booked at a named time in their
own zone, the attached file living in the object store. When two people submit for one slot,
exactly one is booked and the other keeps every answer. A client signed in to one engagement
sees that engagement alone, and an approval names who gave it and when.
