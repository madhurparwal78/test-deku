# Fieldline

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, read the whole portfolio on one continuous scroll while each system's diagram plays as it passes, and send a note through the contact channel that comes back with a private thread link, without hitting an error page. The hard part is the boundary around unpublished work: a piece of writing that is still a draft, and the still drawing exported for it, must be readable by its own author and by nobody else, and the exported bytes must live in the MinIO bucket at the key scheme pinned below. A copy of those bytes on the app container's own filesystem, or a column in PostgreSQL holding the drawing itself, is not the object store and does not count.

## Overview

Fieldline is the personal site of `Nils Adeyemi Karlsen`, an engineer who builds machine-learning systems, and it is built to be read rather than navigated. It makes three claims that a conventional portfolio does not. The opening is a rendered field rather than a photograph: a turning wireframe volume of several thousand triangulated points fills the first screen with the headline set inside it. Work is shown as its architecture: each shipped system is drawn as a labelled diagram of boxes, connectors, gates and a run log, and the diagram plays as the reader scrolls past it, so the claim being made is not that this person made a thing but that this is how the thing works. And the whole index is one scrubbed timeline: nine bands in a fixed order, played by the reader's own finger.

Three readers settle every tension, in this order of priority. A hiring engineer arrives from a link in a message, wants evidence of judgement rather than a list of tools, and leaves having actually read the systems band. A prospective client arrives from a search or a referral, wants proof this person ships and can explain it, and leaves having sent a note. A peer arrives from the writing, wants one specific idea, and leaves with a subscription or a link shared onward.

The only other route of substance is the writing archive and the pieces in it. The author writes a piece and its diagram in a studio, exports a still drawing of that diagram into the object store, and publishes. Notes arriving through the contact channel are scored as they land and sorted into three lanes on the author's desk, where nothing is ever deleted and no reply is ever sent without the author pressing send.

What it deliberately is not: not a case-study site with a route per project, because everything of substance lives on one scroll; not a content management system with a public author surface; not an application. The complete list of state a visitor can create is three things: a note, a subscription, and an anonymous tally that a reader scrolled this far. Keeping that list short is a design position, not an omission. There are no comments, no likes, no follower graph, no direct messaging, no payment of any kind, and no outbound email, because this environment has no mail service.

The genuinely hard part is that an unpublished piece is private property. The row, the page and the exported object in the store are all closed until the author publishes, and publishing is the single act that opens all three.

## User roles

| Role | Can do |
|---|---|
| Visitor (signed out) | Read the index, the archive, any published piece, the privacy page and every diagram; answer the cookie question; send a note through the contact channel and open the resulting thread by its token; add a message to that thread; subscribe to the writing and confirm the subscription. **Cannot reach the studio, the desk or any draft piece, draft diagram or exported still of either; cannot read any other sender's thread; cannot see any note listing.** |
| `reader` | Everything a visitor can do, plus see their own notes collected on the account route and manage their subscription there. **Cannot compose, publish, validate or export anything; cannot reach the studio or the desk; cannot read another account's draft or another sender's thread.** |
| `author` | Everything a reader can do, plus compose a piece and its diagram in the studio, save drafts, validate a structure, export a still into the object store, publish, and work the desk: read every arriving note with its score breakdown, change its lane or state, snooze it, and send a reply they have edited themselves. **Cannot read, edit, publish, export or delete a piece or diagram owned by another account.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a `reader` session to any `author`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is open. Anyone may create an account from `/signup` and choose whether it is a `reader` or an `author` account; there is no invitation and no approval step. Sending a note and subscribing need no account at all, which is the point of the token thread. The seeded accounts below already exist and every one of them uses the password `deku-demo-pw-2026`:

| Email | Role | Display name |
|---|---|---|
| `author@example.com` | `author` | `Nils Adeyemi Karlsen` |
| `author2@example.com` | `author` | `Wren Adeyemi Karlsen` |
| `reader@example.com` | `reader` | `Juno Castellane` |

## Core features

### Auth

This app owns its own accounts: an email, a password, nothing borrowed from outside. Signing in hands back a bearer token that rides on every request afterwards, good for twelve hours and refused once that runs out. A stored password is a hash of the password, never the password. Signing up takes an email, a password and a role, folds the email to lower case, and turns away a second account on an address already in use with the offending field named. Nothing resets a password, because nothing here can send a reader anything.

1. A fresh address yields an account plus a token that works straight away. The same address offered twice is turned away as invalid, the email field is named in the refusal, and the second account row never exists.
2. A form that refuses says so in place, names the field at fault, and writes nothing at all. A sign-up carrying an empty password, a note carrying a two-word message and a sign-in carrying an address nobody registered each leave the datastore byte for byte as they found it.

### The index as a sequence

The index is nine bands in one fixed order, and the order is the argument: hero, manifesto, experience, philosophy, systems, open source, stack, signal, footer. A reader never navigates between them; they scroll.

3. `GET /api/bands` returns a top-level JSON array of the nine bands in that order, each carrying `slug`, `name`, `start_fraction` and `end_fraction`, where the fractions are the band's share of the whole document and the nine ranges tile from zero to one with no gap and no overlap. The band slugs are `hero`, `manifesto`, `experience`, `philosophy`, `systems`, `open-source`, `stack`, `signal` and `footer`.
4. The left rail names the band the reader is currently in and shows how far through the document they are. The name changes as the marker crosses a band boundary, and the rail carries `aria-current` on the entry for the current band. The top-bar entries `systems`, `open source` and `signal` scroll to their band rather than navigating, and `blog` navigates.
5. The experience band carries six roles across four employers in reverse chronological order, and an employer's header stays pinned to the top of the screen while that employer's roles are being read. The philosophy band carries four numbered principles, each on its own screen with its own diagram. The systems band carries five entries, each with a diagram, a run log, a contribution line and a tool list.

### The wireframe field

The first screen is a triangulated wireframe volume, roughly ellipsoidal and several thousand vertices wide, drawn as lines rather than faces and turning slowly, with the headline sitting inside it and in front of it. Most edges are grey at low alpha; a small minority are drawn in the field's accent hues as connected paths so they read as threads running through the mass rather than as speckle. It is drawn live, it never repeats, and it leans slightly toward the pointer where there is a real pointer to lean toward.

6. The field renders as a single drawing call over a transparent ground, and it holds a steady frame rate on ordinary laptop hardware. It dissolves into the page ground at the foot of the first screen rather than ending at a hard edge.
7. The field's render loop stops entirely once the field is fully covered by the content scrolled over it, and once the document is hidden, and restarts when it is neither. A loop that keeps running through the rest of the document is a defect, not a detail: the index is several times the height of the viewport and the field is behind all of it.
8. When the device reports no hardware acceleration, or the reader has asked for reduced motion, the field renders a still frame generated from the same geometry and the same seed, drawn as vector line geometry at three widths rather than as a raster, so it stays sharp and ships no image file.

### The diagram language

Every principle and every shipped system carries a diagram. A diagram is **data, not hand-written markup**: it is declared as a structure of nodes, edges, an optional sampled series, annotations, a timeline and a layout, and one renderer turns that structure into drawn geometry. That is what makes the tall layout and the wide layout two arrangements of one description rather than two drawings to maintain.

9. A diagram's structure uses a closed vocabulary and the validator refuses anything outside it. A node's `kind` is one of `box`, `gate`, `store` or `terminal`. An edge's `kind` is one of `plain`, `active` or `drift`. A timeline stop carries an `at` between zero and one, a `target` and an `effect`, and `effect` is one of `travel`, `sweep`, `gate`, `promote`, `drift`, `enter` or `pulse`. `POST /api/diagrams/<slug>/validate` reports every illegal kind, every edge naming a node that does not exist, and every stop outside zero to one, each with the offending item named.
10. Layout is deterministic: nodes are placed in flow order at a fixed pitch, edges are routed orthogonally with a single corner, and the coordinate box is computed from the result. The same structure renders the same drawing on two consecutive builds, which is what makes a diagram reviewable in version control. Two timeline stops targeting the same mark at the same instant resolve to the later one in list order, and validation warns about it rather than failing.
11. One structure renders both the tall layout and the wide layout with no second input. The two are different arrangements, not one scaled: the tall one runs its stages down a column and is considerably taller, and the wide one runs them across a row.
12. Beneath each system diagram sits a run log of exactly four rows, each a marker, a label and a right-aligned value. The rows complete in order as the diagram is scrolled through. A completed row shows a check; the row waiting next shows a ring and is the only thing in the whole diagram wearing the accent colour. Under the log sits a status row carrying a left label and a right label.
13. Every diagram carries a text alternative that describes its nodes in order, the connections between them, and what its run log concludes. The alternative is a description, not a caption: it must give somebody who cannot see the drawing the argument the drawing makes, and the string `system diagram` alone does not qualify. The animated marks are decorative and are hidden from assistive technology; the run-log rows are not, and are announced in order as they complete.

### Writing, drafts and the studio

Hand-drawing a diagram twice, once tall and once wide, and then timing it by eye against scrolling, is the problem the studio removes: a diagram becomes a short structure the renderer draws both ways. An `author` composes a piece in a three-step wizard, each step at its own address, because the diagram half of a piece needs its own screen. Step one at `/studio/new/piece` takes the series, the title, the summary and the body. Step two at `/studio/new/diagram` takes the diagram structure, renders it at both widths side by side, and offers a scrub bar under each that drives the progress value from zero to one directly. Step three at `/studio/new/review` validates, exports and publishes.

14. `POST /api/posts` creates a piece with status `draft`, derives a unique kebab-case slug from the title, assigns the next unused number within the chosen series, and returns it. The code is the series and the number joined by a hyphen, and the two series number independently: `ENG-001` and `THT-001` both exist, and creating a third `ENG` piece gives `ENG-002` while the `THT` series stays where it is.
15. `POST /api/diagrams/<slug>/export` renders the diagram to a still drawing and writes those bytes into the MinIO bucket at `diagrams/{diagram_id}/{sha256_of_bytes}.{ext}`, for example `diagrams/5/3c81f0a94e27b6d5c08f1a3e72b9d46c5f8071e2a3b4c6d9e0f1a2b3c4d5e6f7.svg`. Attaching a still to a piece writes it at `posts/{post_id}/{sha256_of_bytes}.{ext}`, for example `posts/12/9f2a1c7e0b4d8a63f5e2904c7b1d6a8e3f0c95b27d4e81a6c3f97b0d25e4a1d0.svg`. The row stores the key; it never stores the bytes. Exporting into a diagram owned by another account is denied and no object is written.
16. An export is refused while validation is failing, and a refused export writes no object and leaves no key on the row. A failed export leaves no partial state: no orphaned object in the bucket, no half-written key.
17. **Draft protection, the rule this product is built around.** While a piece is a draft, `GET /api/posts/<slug>` and `GET /api/posts/<slug>/still` answer only the owning author's session. An anonymous request, a `reader` request and a request from the second author account are all denied and return no bytes and no body. The draft appears in no listing: `GET /api/posts` returns published pieces only, newest first. The same rule holds for a draft diagram and its exported still through `GET /api/diagrams/<slug>` and `GET /api/diagrams/<slug>/still`. Once published, all four endpoints answer anyone.
18. `POST /api/posts/<slug>/publish` moves the piece to status `published`, stamps `published_at`, and opens the piece page and its still together. Publishing a piece whose diagram has never exported a still is rejected as invalid with a message naming the still. Publishing a piece owned by another account is denied and the piece stays a draft.
19. Pressing publish twice on one draft yields one piece, one slug and one stored drawing: the second attempt changes neither the row count nor the key already on the row. Two publish requests for that draft landing together are not both accepted either; one wins, the other comes back naming the conflict.

### The contact channel

The fixed contact button and the signal band both open the same panel over the page, so a reader never loses their place in the scroll. The panel is also addressable at `/signal` for a direct link.

20. The panel takes a name of `2` to `80` characters, an email checked for syntax with disposable domains refused, an intent that is one of `Hiring`, `Consulting`, `Collaboration` or `Something else`, a message of `20` to `4000` characters, and, only when the intent is `Consulting`, a budget band chosen from four bands plus `Not sure yet`. Validation is deferred to submit. All five fields are required except the budget band, and a note that fails any of them is rejected as invalid, keeps everything the sender typed, and shows one line naming what is wrong.
21. `POST /api/notes` stores the note with its intent, a coarse referrer and the band the reader was in when they opened the panel, and returns a `thread_token`. On success the panel replaces its body with a confirmation carrying the thread link. `GET /api/notes/<thread_token>` returns that one note and its messages and nothing else: the token reaches exactly one note, grants nothing further, and appears in no listing anywhere in the product. A request for a token that does not exist answers not found, and so does a request for a real note without its token.
22. `POST /api/notes/<thread_token>/messages` adds a message to the thread with `author_kind` of `sender`. A note is never deleted by the sender; closing it is the author's action. The sender sees the note as sent, its state, and any reply from the author, in order.
23. `POST /api/subscribers` records the address in state `pending` and returns the confirmation link. Nothing reaches a subscriber in `pending` but that confirmation, and the address is on no list until `GET /api/subscribers/confirm/<token>` is followed, which moves it to `confirmed` and redirects to the archive. The confirmation token expires after `7` days and an expired one is refused as gone rather than silently accepted. `POST /api/subscribers/unsubscribe/<token>` moves the address to `unsubscribed` in one action with no page load and no sign-in, and every recorded outbound message carries that token.
24. Rate limits, all enforced server-side and all answered with `That is a few too many in an hour. Try again later.`: `3` notes per hour and `10` per day from one email address, `10` notes per hour from one network address, `20` messages per day on one thread, `3` subscriptions per day from one address, and `120` view beacons per minute. A fourth note from one address inside an hour is refused and no fourth note row exists.

### The signal desk

A portfolio that works produces a stream of notes that is mostly noise: two recruiters, one student, one genuine consulting enquiry, one automated solicitation. Read in one undifferentiated list with no context, the good ones get buried and the wrong ones get answered first. That is the problem the desk solves, and it solves it by sorting notes as they arrive without ever discarding one.

25. A score is computed once per note, at creation, from six signals, and the weights live in one configuration file the desk prints on screen so the author can see why a note landed where it did. A message length between `120` and `1500` characters scores `+2`. Naming a system or a piece from the site, matched as a substring against the seeded system titles and piece titles, scores `+3`. An intent of `Consulting` with a budget band above the first scores `+2`. Arriving from the systems band or the signal band scores `+2`. A message containing a link and fewer than `40` words scores `-4`. An address domain matching the organisation the message claims scores `+1`.
26. The total maps to three lanes: `signal` at `4` and above, `unsorted` from `0` to `3`, and `likely noise` below `0`. Nothing is deleted and `likely noise` is a lane rather than a bin: it is presented collapsed, reopening it is one action, and the reopen is recorded. A note naming a seeded system and asking about consulting lands in `signal`. A forty-word note carrying a link lands in `likely noise` and is still readable.
27. If scoring cannot run, the note is delivered anyway with no lane and appears in `unsorted`. Delivery is the priority and scoring is an enrichment: a scoring pass that is down must never swallow a note.
28. The desk at `/desk` shows three lanes, as columns on a wide screen and stacked on a narrow one. Each note is a card carrying the sender's name, the intent, the first two lines of the message, the score with its contributing signals revealed on the card, and the age. The card actions are `Reply`, `Snooze`, `Close` and `Mark noise`. Replying opens a composer with a draft assembled from the intent and any matched system, which the author edits before sending. No reply is ever sent without the author pressing send.
29. A note in the `signal` lane is offered three concrete slots from the next two weeks, drawn from the author's weekly availability rule. `POST /api/bookings` holds a slot for `10` minutes while the chooser decides, and an abandoned hold expires and returns the slot. Two senders choosing the same slot must not both succeed: exactly one booking becomes `confirmed` and the other is refused with a message naming the taken slot and the remaining slots are re-offered. A refused booking leaves no partial state and no slot stuck in `held`.

### The ordinary surface

30. Somebody arriving for the first time meets one dismissible band above the footer asking whether non-essential cookies are allowed. Whichever way they answer, the answer holds across a reload and across every later route, and the band stays gone for them afterwards. The refusal sits beside the acceptance at the same size and the same reach; neither is tucked behind the other.
31. Each page view is recorded with its route, the day, and how far down the index that reader reached, as the slug of the deepest band they entered. `POST /api/views` takes a route and a band and records nothing that could identify one reader: no third-party identifier, no address, no fingerprint, and the record is an aggregate per route per day rather than a row per visitor. `GET /api/views` answers the `author` account only and returns the aggregate. This is the one number worth collecting on a site like this, because the whole page is an argument that builds to the systems band and it is worth knowing whether anyone arrives.
32. Every internal link on every public route resolves. The top bar, the rail, the footer, the archive list, every piece's previous and next entries, the repository rows and the privacy page are all reachable by following links from the index, and none of them leads to a page that answers not found.
33. An unknown address renders the product's own not-found page and answers not found: the code `404`, the line `This page could not be found.` and an action reading `Return home` that returns to `/`. The top bar wraps it unchanged and the rail is absent, so a lost visitor is never stranded on a bare framework error screen.
34. A privacy page at `/privacy`, linked from the footer of every route, states in plain words what the site records, which is a note, a subscription and an anonymous per-route tally, and that the tally is kept for `13` months and holds no value that could identify one reader.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | The whole portfolio on one scroll, nine bands in order | public |
| `/blog` | The writing archive, newest first | public |
| `/blog/<slug>` | One piece, at reading measure | public when published, owner only while draft |
| `/signal` | The contact channel as its own address | public |
| `/signal/<token>` | The sender's own thread | token |
| `/privacy` | What the site records and for how long | public |
| `/signup` | Create a `reader` or `author` account | public |
| `/login` | Sign in | public |
| `/studio` | The author's grid of pieces and diagrams | `author` |
| `/studio/new/piece` | Wizard step one: the piece | `author` |
| `/studio/new/diagram` | Wizard step two: the diagram, both widths, with a scrub bar | `author` |
| `/studio/new/review` | Wizard step three: validate, export, publish | `author` |
| `/studio/diagram/<slug>` | Edit one diagram | `author` |
| `/desk` | Three lanes of arriving notes | `author` |
| `/account` | The signed-in account: own threads, subscription, cookie answer | `reader` or `author` |
| any other path | The product's own not-found page | public |

**Entry and redirects.** Asking for `/studio`, for any `/studio/` step, for `/desk` or for `/account` while signed out puts the reader on `/login` first, and signing in from there carries them on to whichever of those they wanted. Somebody who signs in with nothing pending arrives on `/studio` if the account is an `author` and on `/account` if it is a `reader`. Signing out puts them back on `/`. If the token runs out halfway through a piece, `/login` comes back with everything still typed into the form, and nothing has been written. A `reader` who reaches `/studio` or `/desk` is refused with a message saying those surfaces belong to the author account, not redirected quietly into them. A signed-out request for a draft piece renders the not-found page rather than revealing that the piece exists. A thread link for a token that has no note renders the not-found page too.

**Journeys.**

1. A visitor opens `/`, reads `I build machines that read the world.` inside the turning field, scrolls past the manifesto line, watches the rail name `EXPERIENCE` while the employer headers pin and release, reaches the philosophy band and reads principle `01`, then reaches the systems band and watches the pipeline diagram play its marks along its connectors while the run log ticks its four rows off in order.
2. The same visitor presses the fixed `LET'S TALK` button, fills the panel with a name, an address, the intent `Consulting`, a budget band and a message naming a system from the page, presses `Send`, and lands on a confirmation carrying the thread link. Opening that link shows the note as sent with its state; adding a message puts it under the original.
3. `author@example.com` signs in with `deku-demo-pw-2026`, opens `/studio`, starts the wizard, writes an `ENG` piece at step one, declares its diagram at step two and drags the scrub bar to the halfway point to watch the gate close, validates and exports at step three, and sees the piece appear in the grid as a draft with its code.
4. The same author publishes that draft from the grid. An inline banner in the page confirms it, the piece appears at the top of `/blog` with its code and date, and the still exported for it now answers anyone.
5. A signed-out visitor requests the still of the draft piece `Everything I got wrong about retrieval` and is refused; no bytes come back, and the draft is in neither `/blog` nor `GET /api/posts`.
6. `author@example.com` opens `/desk`, finds the seeded notes in `signal`, `unsorted` and `likely noise`, opens the score breakdown on the top card to see which of the six signals fired, edits the drafted reply, and sends it. The sender sees the reply on their thread.
7. A reader subscribes from the foot of `/blog`, follows the confirmation link, and the subscription moves from `pending` to `confirmed`; following the unsubscribe link once moves it to `unsubscribed` without a sign-in.

**States.** Every list has an empty state that names the absence in one sentence and offers the action that fills it: an author with nothing written sees an empty studio grid inviting a first piece, the desk with nothing waiting reads `Nothing waiting` over `Notes appear here as they arrive.` with no action, and the diagram editor with nothing open reads `No diagram open` over `Create one or open an existing diagram to begin.` with a `New diagram` action. Every surface that fetches has a loading state built from shimmering blocks in the shape of the final layout rather than a spinner over a blank page. Errors render inside the page chrome as one line with a retry that repeats the same request, and a refusal renders the product's own not-found page. Nothing ever renders a blank screen or a raw error dump.

## UI/UX notes

**North star.** Somebody arriving should understand within the first screen that this person builds systems and can explain how they work, and should feel they are reading something rather than being sold something.

**Register.** Editorial and personal: the subject is seen first and the page is allowed atmosphere, while every figure, label, timestamp and diagram annotation stays quiet and exact. Reading over navigating. Space over dividers. Drawing over decoration. A competing portfolio could rationally hold the opposite of each of those and be right for its own context, which is why they are stated.

**Colour, by role and by exclusivity.** The page is an evenly stepped neutral ramp and nothing else. It runs from a near-white ground through a sunk panel tone that fills every diagram box, a hairline tone that strokes them, a rule tone for dividers, a disabled tone, a tertiary tone, a secondary tone that carries all body copy, a meta tone for labels, a strong secondary, a heading tone, a near-black for the counter's figure, and a near-black for primary text. The steps must read as evenly spaced to the eye rather than evenly spaced by number, which is the difference between a page that reads calm and one that reads muddy, and it is worth the effort even though it looks like a technicality.

There is exactly one saturated colour in the whole interface, a mid, vivid orange, and that restraint is the design. It carries the rail marker, the name of the current band, the contact button and the one run-log row that is waiting, and it appears nowhere else. A deep, soft blue is the second signal and is confined to the principle number, the stepper's active node and the threads running through the field. A light, soft blue carries inline links in long-form writing and moves a step lighter when pointed at. A light, soft cyan and a light, soft orange exist only as field thread hues and as the diagram's promotion state, and they never carry meaning outside a drawing. Everything else on the page is neutral. The exact values are yours, so long as the ramp reads evenly and the exclusivity rules above hold.

**Against the default.** A grey page is not a licence to reach for a second hue when the first one runs out of jobs: one saturated colour, and the rest of the meaning carried by position, weight and the mono split. This page's only ornament is its drawings, so anything decorative that describes no real system has no place on it. The studio grid and the desk lanes are work surfaces, not landing pages, and an editorial hero dropped onto either one is the failure to avoid.

**Type.** Two families and the split between them is normative rather than decorative: one for prose and one monospaced, called the mono family throughout this brief, for every label, figure, timestamp, code fragment and diagram annotation, so instruments always look like instruments and prose always looks like prose. Headings carry real contrast in weight and size against body copy, so a heading reads as a title and body reads comfortably at arm's length. Long-form measure is capped so a line of prose never runs much past sixty characters, which is why the writing is easy to read at any window width. Figures line up in a column wherever values stack, so a run log scans down its right edge. Uppercase mono carries band labels, section markers and status words, with tracking opened enough to keep them readable at label size. Both fallback stacks must be metric matched, because the monospaced face carries the diagram annotations and a fallback of a different width would move the drawings as the fonts settle. The families and the sizes are yours; the split, the measure cap, the alignment and the metric match are not.

**Shape and density.** Corners are barely softened everywhere, and the only fully rounded shapes in the product are the scroll cue's capsule and the dots. Space, not rules, separates the bands: two bands read as separate at a glance with no line between them, and the single hairline rule that does exist is drawn as geometry in a pale sand at low alpha rather than as a border. Density is spacious through the reading bands, where one idea gets one screen, and compact in the studio grid and the desk lanes, where a full set of cards should fit one screen. The base unit is yours; the contrast between the two densities is not.

**Depth.** A small fixed ladder, in this order from back to front: the field behind everything, the overlay gradients over it, content, the diagram overlay, the left rail, the top bar, and the opening curtain in front of all of it. Nothing invents a new layer to win a fight. Shadows barely exist; where one appears it is shallow and close rather than a soft cloud.

**Motion.** One house ease governs almost everything and is the single most identifying property of this site's movement: it arrives quickly and settles late, which is what makes a page of grey rectangles feel machined rather than plain. It is the easing on every hover, every entrance and every scrubbed reveal. Movements share one short duration, quick enough not to be waited for and slow enough to be seen, and only the opening curtain runs longer. Nothing uses a different duration or a different curve to feel special. These moments animate and no others: the headline arrives word by word, each word sliding up and sharpening from a blur as though it were being focused; the name line and the role line follow it; the opening curtain fades away across the whole screen; the scroll cue's dot travels down its capsule and its chevron pulses, both on a loop; the band label breathes on a loop; a mark travels along a connector, sideways in the wide layout and downward in the tall one; a longer sweep traverses a whole diagram for a pipeline run; a gate closes, collapsing to a sliver of its height and dimming, and stays there; a path draws itself in and then retracts, which is a candidate promoted and then released; an idle connector carries a slow dash drift; an element enters by rising a little and fading in; and a node under load scales up and dims at the midpoint of its pulse. Each of those is a meaning, not an effect: a reader who watches a diagram play should be able to say what happened in that run. The exact timings and curves are yours so long as everything shares one character.

**Reduced motion.** Where the reader has asked their device to reduce movement, the field holds its first frame, every diagram renders in its final state with no scrubbed choreography, and the cue and the band label stop pulsing. The headline words appear without blur or travel. The hover transition is preserved rather than removed, and the counter keeps counting, because it is information rather than animation.

**Accessibility.** One first-level heading per route, and the index's is the opening line. Bands are sections with accessible names taken from the band list. The rail is navigation with a name and marks its current entry. Every diagram carries a text alternative describing its nodes in order, its connections and what its run log concluded, so a reader using a screen reader gets the argument the drawing makes rather than the word diagram; the animated marks are decorative and hidden, and the run-log rows are announced in order. The field is decorative, carries no text and is hidden entirely. Body text meets WCAG AA contrast against the page ground. The accent does not clear that bar at body size, so it is used only as tracked uppercase label text and as white on an orange fill, which does clear it. Every control is reachable and operable by keyboard navigation with a visible focus ring drawn as an outline in the accent; the panel traps focus while it is open, returns focus to the control that opened it, and closes on escape; scrolling to a band from the top bar moves focus to that band, so a keyboard reader and a pointer reader end in the same place. Icon-only controls carry a text label. Colour is never the sole carrier of meaning: a completed run-log row pairs its tone with a check and the waiting row pairs the accent with a ring.

**Responsive.** Breakpoints are expressed against the reader's own text size rather than against the device, so somebody who has enlarged their text gets the simpler layout rather than a broken one. The responsive matrix is three tiers of behaviour and the layout holds at every width between them. On a narrow viewport the rail is hidden, the contact button becomes a full-width bar across the foot, the diagrams take their tall layout, nothing overflows sideways, and every navigation target stays reachable. At a small tablet width the diagrams switch to their wide layout while system entries stay one column. On a wide screen the rail appears and system entries run two columns. The document is taller on a phone than on a desktop because the diagrams stack rather than shrink. That is correct and must not be tidied away: a diagram squeezed to phone width is a smudge, and a longer page somebody can read beats a shorter one they cannot. Hover effects sit behind a real pointer and carry no information of their own, so the cursor glow simply does not exist on touch. Tap targets reach a comfortable size through padding rather than by inflating the type. Choose the widths; the behaviour at each of them is already chosen.

**One leading action per view.** Every route puts one action ahead of the rest and makes it look that way: the fixed contact control on the index, `Send` inside the panel, publish in the studio, `Return home` when an address leads nowhere. Nothing secondary borrows the accent to compete with it.

**Mode.** The product commits to light and builds it out: a near-white ground, near-black text, and the whole ramp tuned for that direction. The theme control may offer a dark scheme, but the dark scheme is a bonus rather than an obligation, and a half-finished second theme is worse than one finished theme.

**Component states.** Each control carries five appearances, at rest, under the pointer, pressed, focused and unavailable, and the last of those is told apart from the first by more than tone. Escape shuts the contact panel and the cookie band. Anything destructive asks once before it acts.

## Technical requirements

Frontend: Alpine.js over server-rendered templates, with two standalone browser modules for the field renderer and the diagram renderer, and one scroll provider that both read. Backend: Flask with Jinja templates, building each route into a complete document on the server and answering the HTTP API on that same origin under the `/api` prefix. The pieces, the diagrams, the notes and the tallies are held in PostgreSQL, whose address arrives as `DATABASE_URL`. Every exported drawing is held in MinIO, reached through `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The author signs in with an email and a password this app owns, and carries a bearer token afterwards. `GET /api/health` answers `200` once both services are reachable, and each request leaves one structured line on standard output.

The rendering model is observable, not an implementation note: the first response for any route carries the whole document, including the nine bands and every diagram's final geometry, as markup. The browser adds movement to content that is already there, which is why the archive and the piece routes can ship none of the field or diagram code at all and still be complete.

Every host, every port and every credential arrives from the environment and is read from there; writing one into the source is a defect even when the value happens to be right. PostgreSQL and MinIO are already up and already reachable at the variables above, so nothing in this build downloads, installs, compiles or starts a copy of either.

The libraries named here, plus what they depend on, are the whole toolbox. A second database, a cache, a queue, a second object store, an outside identity provider or a mail vendor are each a contract violation - PostgreSQL and MinIO are the only backing services this environment carries, and reaching past them is reaching for something that is not there.

**Content and state are two different things.** The career roles, the principles, the systems, the repositories, the stack list, the diagrams and the published pieces are authored content: the author writes them, they are read at render time, and a visitor cannot create one. The only state a visitor creates is a note, a subscription and an anonymous page-view tally. Content still lives in PostgreSQL so the studio can write it, but nothing on a content band is a form.

**No message leaves this app.** The environment carries no mail service, no messaging service and no notification service, and none may be introduced. Everywhere the product would send something, it records an `outbound_messages` row carrying the recipient, the kind, the single-use link token and the delivery state, and shows the link once on the surface that created it. The rule this protects is unchanged and is enforced exactly: an address in `pending` is on no list, and only following the confirmation link moves it to `confirmed`.

**Nothing secret is downloadable.** The served document, every script it pulls, every JSON answer and every inline attribute are all things a reader can open, so none of them may carry a credential, a store key, an admin token or a database address. Only the server talks to the object store. A still reaches a reader through this application's own endpoint, which decides first whether that reader may have it; the browser never learns where the bucket is or how to open it.

**Site icon.** The site serves its own favicon and declares it in the document head on every route, so a reader who keeps the tab open can find it again. The favicon is generated vector geometry like everything else here, not a shipped binary, and it resolves at the address the head declares.

**Performance, as observable outcomes.** The field draws in a single call, holds a steady frame rate on ordinary laptop hardware, and stops rendering the moment it is covered or the document is hidden. The index scrolls smoothly with several diagrams playing at once, because one passive listener reads the scroll position once per frame and writes custom properties that everything visual consumes, and nothing in that path writes a layout property: only transform, opacity, filter, clip and stroke offset change as the reader scrolls. No single piece of work during a scroll blocks the page long enough to be felt as a stutter. The index paints its headline before the field has started. The archive and the piece routes create no drawing context at all. The counter writes text at most twice a second. Nothing on any route reflows when the fonts finish loading.

**The live counter.** The top bar carries a figure that starts at zero on page load and climbs continuously from the elapsed time on the page, formatted to one decimal place with the word `trillion`, followed by `synapses fired while you're here`. It never resets on scroll, it never animates its digits individually, and it re-renders at most twice a second so it reads as a meter rather than a slot machine. The rate is the commonly cited figure for synaptic firings across a human brain, which is why it reaches the low hundreds of trillions after a few minutes of reading; the joke only works because the number is real, so keep the rate.

## Data model

Sixteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

`accounts` - `id` integer, `email` text unique and stored lowercase, `password_hash` text, `display_name` text, `role` text and one of `reader` or `author`, `created_at` timestamp.

`career_roles` - `id` integer, `employer` text, `city` text, `title` text, `start_date` date, `end_date` date and null meaning present, `summary` text, `sort_order` integer. Reverse chronological order is derived on read from the dates, not stored as a rank.

`principles` - `id` integer, `position` integer from `1` to `4` and unique, `label` text, `headline` text, `body` text, `caption` text, `diagram_id` referencing `diagrams`.

`systems` - `id` integer, `position` integer from `1` to `5` and unique, `year` text, `title` text, `subtitle` text, `status` text and an open string, `description` text, `contribution` text, `tools` a list of text, `confidential` boolean, `diagram_id` referencing `diagrams`, `run_log` four ordered pairs of `label` and `value`.

`repositories` - `id` integer, `name` text, `description` text, `language` text, `stars` integer, `url_token` text, `sort_order` integer. The outbound address is a token resolved from configuration at render time and is never a literal in the markup.

`stack_items` - `id` integer, `group_name` text, `name` text, `sort_order` integer.

`diagrams` - `id` integer, `slug` text unique and kebab-case, `title` text, `structure` holding `nodes`, `edges`, `series`, `annotations`, `timeline` and `layout`, `alt_text` text, `owner_id` referencing `accounts`, `status` text and one of `draft` or `published`, `still_key` text holding the object key and never the bytes, `created_at` timestamp, `updated_at` timestamp. `series` is a fixed table of `70` sampled values shipped with the diagram and identical on every render; it is a measured signal and generating it randomly makes the drawing look like decoration.

`posts` - `id` integer, `slug` text unique and kebab-case, `series` text and one of `ENG` or `THT`, `number` integer, `title` text, `summary` text and nullable, `body` text, `status` text and one of `draft` or `published`, `author_id` referencing `accounts`, `diagram_id` referencing `diagrams` and nullable, `still_key` text, `published_at` timestamp and null while the piece is a draft, `created_at` timestamp. `number` is unique within its `series` and the two series number independently. `code` is derived on read as the series and the number joined by a hyphen, never stored twice.

`notes` - `id` integer, `name` text, `email` text, `intent` text and a closed enum of `Hiring`, `Consulting`, `Collaboration` or `Something else`, `budget_band` text and null unless the intent is `Consulting`, `message` text, `state` text and one of `new`, `read`, `replied`, `closed` or `spam`, `score` integer and nullable, `lane` text and nullable and one of `signal`, `unsorted` or `likely noise`, `score_breakdown` holding the six signals and which of them fired, `snoozed_until` timestamp and nullable, `referrer` text and nullable, `band` text and nullable, `thread_token` text unique, `created_at` timestamp and indexed.

`note_messages` - `id` integer, `note_id` referencing `notes` and indexed, `author_kind` text and one of `sender` or `owner`, `body` text, `created_at` timestamp.

`subscribers` - `id` integer, `email` text unique and stored lowercase, `state` text and one of `pending`, `confirmed` or `unsubscribed`, `confirm_token` text, `unsubscribe_token` text, `confirmed_at` timestamp, `unsubscribed_at` timestamp, `created_at` timestamp.

`page_views` - `id` integer, `route` text, `day` date, `count` integer, `max_band` text holding the slug of the deepest band reached. One row per route per day, aggregated, never per visitor, and carrying no value that could identify one reader.

`availability_rules` - `id` integer, `weekday` integer, `start_time` time, `end_time` time, `timezone` text, `slot_minutes` integer.

`bookings` - `id` integer, `note_id` referencing `notes`, `starts_at` timestamp, `state` text and one of `held`, `confirmed` or `cancelled`, `hold_expires_at` timestamp.

`desk_sessions` - `id` integer, `account_id` referencing `accounts`, `token` text unique, `expires_at` timestamp, `used_at` timestamp. A desk session expires `24` hours after it is issued.

`outbound_messages` - `id` integer, `recipient` text, `kind` text and one of `note_confirmation`, `owner_notification`, `subscription_confirmation`, `reply` or `booking_confirmation`, `link_token` text and nullable, `state` text and one of `queued`, `delivered` or `failed`, `attempts` integer, `created_at` timestamp, `delivered_at` timestamp. An owner notification is recorded after scoring, or after `30` seconds regardless of whether scoring has finished, and a failed one is retried five times with a widening gap before it is left `failed`.

`cookie_choices` - `id` integer, `visitor_token` text unique, `accepted` boolean, `decided_at` timestamp.

**Invariants, stated as properties of the running system.** A draft piece, the diagram it carries, and the objects at their `still_key` values are readable by the owning author and by nobody else; publishing is the only act that opens them, and it opens the row, the page and the object together. Publishing the same draft twice leaves exactly one published piece and one stored object, and two publishes of the same draft arriving together are not both accepted. A `thread_token` reaches exactly one note and appears in no listing. A subscriber in `pending` is on no list and nothing but the confirmation is recorded for them. A `number` is unique within its `series`, and the `ENG` and `THT` series advance independently. Two bookings for the same slot are not both confirmed: exactly one wins and the other is refused, and no slot is left `held` by a chooser who walked away. A failed export, a failed publish or a failed booking leaves no partial state: no orphaned object in the bucket, no key on a row with no object behind it, no piece half-moved to `published`. `page_views` holds no value that could identify one reader.

**Seed data.** Three accounts as listed in `## User roles`.

Six career roles across four employers, reverse chronological: `AI & Machine Learning Engineer` at `Brightwater Capital` in `Halifax`, `Jul 2025 - Present`, described as `I architect the agentic systems the investment teams run on. A multi-agent extraction pipeline that turns unstructured documents into structured metrics, and an orchestration layer over 30+ institutional research providers where a single agent run picks its own tools, resolves the question, and answers with citations. Versioned agents, eval gates before release, trace telemetry on every run.`; `Founder` at `Saltmarsh AI` in `Halifax`, `Apr 2025 - Present`, described as `AI consulting for Canadian businesses. I find the two or three workflows where automation pays for itself, then build and deploy them on infrastructure the client owns and can audit.`; `Business Intelligence Developer` at `Brightwater Capital`, `May 2024 - Jul 2025`, described as `Built the warehouse-backed reporting the investment and operations teams work from, and automated the catalog sync, lineage and ownership behind it, so a metric meant the same thing in two different reports.`; `IT Technical Support` at `Brightwater Capital`, `Mar 2022 - May 2024`, described as `Two years of escalations, security policy, and the process fixes that stopped the same ticket from coming back a third time. Most of what I know about how production fails, I learned here rather than from a design doc.`; `IT Specialist Level II` at `Eastfell Health` in `Dartmouth`, `Mar 2021 - Mar 2022`, described as `Infrastructure deployment and level-2 support across a regional health network, where an outage reaches clinical staff in minutes and the rollback plan matters more than the change itself.`; and `IT Technician Level I` at `Colvin College` in `Halifax`, `Aug 2020 - Jan 2022`, described as `My first job in tech: SLA-bound ticket work, hands-on troubleshooting, and a lot of practice explaining a complicated failure to someone who just wants their machine back.`

Four principles. `01` `Context`, headline `Most of my agent bugs were never model bugs.`, body `Every time an extraction came out wrong and I went looking, the model had done something reasonable with something it should never have been handed. So I spend most of my time on what goes into the window, and very little on the prompt.`, caption `Retrieval over 30+ research providers`. `02` `Evals`, headline `I stopped trusting changes I could not measure.`, body `A demo tells you the happy path works. It tells you nothing about the next forty documents. I build the eval set first now, even when it feels like a detour, because the alternative is editing prompts and hoping.`, caption `Eval gate on a versioned extraction agent`. `03` `Quiet failures`, headline `The expensive failures are the ones nobody sees.`, body `A tool returns something useless, the model works around it, the run finishes clean, and nobody gets paged. That whole class of failure is why I trace every tool call going in and coming out, instead of logging only the ones that throw.`, caption `Trace-level observability on every agent run`. `04` `Handover`, headline `A system nobody else can run is a system I have not finished.`, body `The last stretch of an agent is the part that lets somebody who did not build it see what it did and change it. Traces they can read, a configuration they can edit, and a way to turn it off. I build that part before I call the thing shipped.`, caption `Owner cockpit over a nightly extraction run`.

Five systems, under the overline `Systems` and the heading `Things people depend on at work.` System `01`, `2026`, `Ferrite`, `Structured extraction for video`, `Private beta`, described as `A video and a schema in, typed JSON out. Transcription, scene detection, frame dedup, vision, and a temporal knowledge graph, with every value pointing back to the second and the modality it came from. Exposed as an API, an MCP server for agents, and apps.` System `02`, `2026`, `Northlight`, `Eval gates for versioned agents`, `SHIPPED`, described as `A versioned agent, a frozen case set, and a gate that refuses a release when a case regresses. Every run writes its cases, its diffs and its verdict beside the traces, so a regression is a row somebody can open rather than a feeling somebody has.` System `03`, `2026`, `Macro Economics Research Agents`, `Multi-agent system with security-level access and parallelization`, `SHIPPED`, described as `Fixed income and currencies research, searchable in one place. A named agent object owns routing and search strategy, the backend executes its tools, and a citation composer links every claim back to the report and the page it came from. One agent run resolves a conversation turn. Runs as a container service beside the warehouse, with a desktop client and trace-level observability over every run.` System `04`, `2025`, `Document Intake for a Private Credit Desk`, `Multi-agent extraction from mixed-format reporting packs`, `SHIPPED`, `confidential` true, described as `Quarterly reporting packs arrive as scans, spreadsheets and slide decks. A parser splits them by modality, an agent per metric extracts a value with its evidence, and nothing reaches the gold table until an owner confirms it. Built on infrastructure the client owns and handed over with its traces.` System `05`, `2024`, `Catalog Lineage Service`, `Warehouse metric ownership and lineage sync`, `SHIPPED`, described as `A metric meant two things in two reports, so the definitions, their owners and their upstream tables became one record the reports read from. A nightly sync reconciles the warehouse against it and files the differences.`

Every system carries the contribution label `MY PART:` followed by its own contribution line, and system `04` additionally carries the line `Client system. The names, the internals, and the data stay with the client.` That line is not a detail: it is how the site shows work it may not name, and it must survive into the build.

Five repositories: `fieldline`, `The scroll-driven diagram renderer this site is built on`, `TypeScript`; `sd-format`, `A declarative format for system diagrams, with a validator`, `TypeScript`; `evalgate`, `A release gate that refuses a regression on a frozen case set`, `Python`; `tracewire`, `Trace-level logging for tool calls going in and coming out`, `Python`; `icosonoise`, `A displaced icosphere and its edge list, from one seed`, `TypeScript`.

Five stack groups of authored content, which describe the subject's own working tools and not how this app is built: `Languages` holding `Python`, `TypeScript` and `SQL`; `Models` holding `PyTorch`, `Transformers` and `ONNX Runtime`; `Data` holding `PostgreSQL`, `DuckDB` and `Parquet`; `Observability` holding `OpenTelemetry`, `Grafana` and `Loki`; `Infrastructure` holding `Docker`, `Terraform` and `Nginx`.

Six diagrams, five published and one draft, each with its structure, its text alternative and its exported still in the bucket. The pipeline diagram carries the annotations `PIPELINE`, `EVAL`, `01 PARSE` over `text, tables, charts, audio, video`, `02 EXTRACT` over `agent per metric`, `03 REVIEW` over `owner cockpit`, and `04 CONFIRM` over `human`. Its run log, headed `RUN LOG`, is `parsed` against `4 pages, 2 charts, 1 scan, 1 recording`; `extracted` against `net_asset_value - conf 0.91`; `eval gate passed` against `12 / 12 cases`; and `awaiting owner confirm` against `nothing promotes on its own`. Its status row reads `PENDING` on the left and `PROMOTED TO GOLD` on the right. The signal diagram carries `SOURCE`, the timestamps `01:12`, `04:31` and `11:07`, `SAMPLED FRAMES` with the frame range `210` through `220`, and `TYPED RESULT` over a JSON fragment carrying `schema`, `decisions`, `decision`, `owner`, `confidence`, `evidence` and a timestamp key. The routing diagram carries `ONE TURN, ONE AGENT RUN` and `ROUTES`.

Three pieces under the archive title `Blog` and the subtitle `Frequency log - tuning into thoughts on AI, taste, and craft`. Published: `[ENG-001]`, `May 12, 2026`, `Most video AI gives you bullet points. I built one that gives you a map.`, summarised as `Flat summaries strip video of the one thing that makes it video: time. Ferrite keeps it. Here is how I turned meetings, interviews, and podcasts into temporal knowledge graphs where every insight links back to the exact second it happened.` Published: `[THT-001]`, `Jan 15, 2026`, `A developer's guide to taste in the age of AI`, summarised as `When AI can write any code, the bottleneck shifts from execution to judgement. Taste becomes the differentiator, the ability to know what should exist, not just how to build it.` Draft, owned by `author@example.com`: `[ENG-002]`, `Everything I got wrong about retrieval`, with no summary. The draft and the still exported for it are the boundary case: they answer their author and nobody else.

Four notes, one in each of `signal`, `unsorted` and `likely noise` plus one unscored in `unsorted`, so every lane on the desk has something in it on a first run. One availability rule with exactly one slot remaining on its first day, which is the contention boundary. One confirmed subscriber and one still `pending`.

The index carries the headline `I build machines that read the world.`, the name line `Nils Adeyemi Karlsen`, the role line `AI Engineer / Founder of Ferrite / Halifax`, whose spaced solidus is what stops the three facts reading as one phrase, the scroll cue `scroll down`, the manifesto line `I learned engineering from broken things.` alone on its own screen, the philosophy divider `HOW I BUILD`, and the footer `Designed by Studio Halvard` beside the year `2026`.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the full visual and structural specification. Nothing here changes a rule stated above.

### Global chrome

**The top bar.** Fixed across the full width on every route, sitting over the page ground with no border and no shadow, in the layer band above content and below the opening curtain. Left: the wordmark, the subject's name set in uppercase monospace and tracked open. Right, in order: the live counter, the four entries `blog`, `systems`, `open source` and `signal` resting in the secondary tone and warming to primary text when pointed at, and a theme control. `blog` navigates; the other three scroll to their band with a smooth behaviour that respects the reduced-motion preference and that also moves keyboard focus to the band. The theme control is the only control in the chrome: a plain circle outline, hairline weight, in the primary text tone, carrying a name and a pressed state, and switching between the light scheme and an optional dark one.

**The live counter.** The figure in the counter's own near-black tone and the phrase `synapses fired while you're here` in the secondary tone, both in monospace at the size the navigation uses. Behaviour is specified in `## Technical requirements`; what matters visually is that it reads as a meter and never as a slot machine.

**The left rail.** Fixed at the left edge from the first scroll, hidden on narrow viewports, entering by sliding in from off the left edge. It is a vertical ruler of hairline ticks in the rule tone, one per percent of document height with every fifth drawn longer, a longer mark again in the meta tone at each of the nine band boundaries, a solid right-pointing triangle marker in the accent at the current scroll fraction, and the current band's name beside the marker in uppercase monospace, tracked open, in the accent. The label changes as the marker crosses a boundary and moves with the scroll, so the rail is a progress meter and a table of contents at once.

**The contact button.** Fixed against the right edge, vertically centred, entering after the first band and staying for the rest of the document. An accent ground with the label `LET'S TALK` in white uppercase monospace, tracked open, on a barely softened rectangle. It opens the contact panel rather than navigating. On a narrow viewport it becomes a full-width bar across the foot.

**Cursor glow.** A radial layer following the pointer at very low opacity, present only where there is a real pointer. It is barely visible by design: it warms the area under the pointer rather than announcing itself, and it does not exist on touch.

**The footer.** One row in the tertiary tone: the design credit `Designed by Studio Halvard` as a link carrying a trailing north-east arrow glyph, and the year `2026`. The privacy link sits beside it on every route.

### Iconography

The site carries almost no icons, which is deliberate: the drawings do that work instead. Four glyphs exist, each drawn as vector geometry rather than as a font or a bitmap, each recolouring from the surrounding text colour.

The play marker is a solid right-pointing triangle in the accent, and it is the rail's current-band marker. The scroll cue is a rounded capsule outline in the meta tone with a small fully rounded dot travelling down the inside of it on a loop, and a chevron below it drawn as a square with only two adjacent borders and rotated a quarter turn, pulsing on its own loop. The rule is a single horizontal line drawn as geometry rather than as a border, stroked in a pale sand at low alpha, and it is the only divider on the site. The theme control is a plain circle outline at hairline weight.

### Surfaces, scale, spacing and depth

Spacing is a single base unit and every gap on the page is a multiple of it; the unit is yours, the multiples are not. Three container measures exist, a narrow one for the panel, a middle one for the archive column at tablet width, and a maximum one for the hero column and the wide archive. The radius vocabulary has two steps and no more: barely softened for everything, and fully rounded for the two shapes named below. The page is the ground tone. A diagram box is the sunk tone filled and the hairline tone stroked; an active box keeps the fill and takes the sand accent at a heavier stroke. A spotlight card is a barely-there dark wash with a slightly stronger border of the same. The cursor glow is a fainter wash again. Two overlay lift steps exist as translucent whites. Depth runs, from back to front: the field, the overlay gradients, content, the diagram overlay, the rail, the top bar, the opening curtain.

### The wireframe field

**Construction.** Geometry is a subdivided icosphere of several thousand vertices, displaced along its normals by several octaves of gradient noise at falling amplitudes so the silhouette is lumpy rather than spherical. It is drawn as edges only, from an edge list built once from the geometry, as a single line-segment buffer. Base edges are a mid neutral at low alpha for the near side, falling further toward the far side by depth, so the volume reads as a volume. A small share of edges take the thread hues, the deep soft blue, the light soft cyan, the light soft orange, a second light soft blue and a light soft periwinkle blue, and those edges are chosen as connected paths rather than at random, which is what makes them read as threads and not as speckle. The volume turns continuously about its vertical axis with a slower roll about the depth axis, its displacement amplitude breathes slightly over a slow cycle, and it yaws a little toward the pointer, eased, where there is a real pointer.

Three layers sit over it and all three are load-bearing. A radial vignette darkens the container from its centre outward. A fade to the page ground at the foot of the first screen overlaps the band below it, which is what makes the field dissolve into the page rather than end at an edge. And a soft radial scrim sits directly behind the headline, which is why the type stays readable over the densest part of the mesh.

The field is fixed behind the document and does not scrub. It keeps turning at its own rate and is progressively covered as content scrolls over it, and its container's opacity reaches zero by the end of the first band, at which point it stops rendering entirely. The still fallback is the same drawing, generated from the same geometry and the same seed as vector line geometry at three widths, so it stays sharp and ships no image file.

### The diagram language

Every diagram is built from seven kinds of mark and no diagram introduces an eighth: a box, an active box, a connector, an active connector, a travelling packet, a bar in a sampled series, and an annotation set in monospace. A box is the sunk fill with the hairline stroke and barely softened corners; an active box takes the sand accent at a heavier stroke. A connector is a straight line in the hairline tone, running horizontally in the wide layout and vertically in the tall one; an active connector takes the accent. A travelling packet is a small elongated rectangle, lying along the connector it rides. A bar is a thin vertical rectangle whose height carries its value, drawn around a centre line, and the whole series is the fixed table of `70` values measured from a real signal. An annotation is monospace text in the secondary tone, and in a diagram the annotation text is part of the drawing and scales with it rather than with the page's type scale.

The seven effects a timeline stop may carry, and what each one means: `travel`, a mark moving along a connector, which is data in transit; `sweep`, a longer traverse across the whole drawing, which is a pipeline run; `gate`, a mark collapsing to a sliver of its height and dimming and staying there, which is a gate closing; `promote`, a path drawing itself in and then retracting, which is a candidate promoted and then released; `drift`, a slow dash offset on an idle connector, which is traffic on a quiet path; `enter`, an element rising a little and fading in; and `pulse`, a node scaling up and dimming at the midpoint, which is a node under load.

Every diagram exists as two separate drawings with different coordinate boxes, one below the middle breakpoint and one above, produced by the one renderer from the one structure. The tall variant is considerably taller than the wide one is wide is deep, and its stages sit in a column where the wide variant's sit in a row.

The run log beneath a system diagram is four rows of a marker, a label and a right-aligned value in monospace. Rows complete in order, evenly spaced across the diagram's own progress. Completed rows sit in the secondary tone with a check in the meta tone; the row waiting next sits in the accent with a ring. The status row below it carries a left label in the tertiary tone and a right label in the secondary tone.

### Scroll system

The index is one timeline the reader plays with a finger. One passive listener owns the scroll position for the whole application, reads it once per frame, and writes it to custom properties; every band, rail and diagram is a consumer of those properties and no mark listens to scroll on its own. Each diagram owns a scroll range equal to its own height plus one viewport and maps its progress through that range to one normalised value between zero and one, and every mark inside it reads that one value, which is what keeps the cost flat however many marks a drawing has.

The rail marker maps linearly over the whole document. The band label steps at the nine boundaries and cross-fades over a small share of a band rather than switching hard. A run log's rows complete at four evenly spaced points through their diagram's progress. Experience rows rise a little and fade in over the first fifth of their own visibility. A section marker sharpens from a blur while sliding in from the left. Two fixed layers, one at the top and one at the bottom, carry a gradient mask that softens content entering and leaving the viewport, and their own opacity is driven by scroll so they are absent at the very top and the very bottom of the document.

### Route: index

**Hero.** Full viewport, the field behind, the legibility scrim over it, and a centred column at the widest of the three container measures. The headline `I build machines that read the world.` sits in it at display size in the primary text tone, arriving word by word. Beneath it the name line `Nils Adeyemi Karlsen` in monospace in the secondary tone, then the role line `AI Engineer / Founder of Ferrite / Halifax`, whose spaced solidus is what stops the three facts reading as one phrase. At the foot, the cue `scroll down` in tracked uppercase monospace above the capsule glyph, breathing on its loop.

**Manifesto.** One line alone on the screen, `I learned engineering from broken things.`, a step larger than body copy. No heading, no rule, no decoration. It gets its own band because it is the site's thesis.

**Experience.** Reverse chronological, six roles across four employers. An employer header is the employer name in the heading tone, then a solidus in the secondary tone, then the city; it is sticky within its own group, sits on the page ground, and carries a hairline rule beneath it. A role row is a small dot in the rule tone on a hairline vertical thread, the title at body size in a heavier weight, the dates in monospace in the secondary tone with a spaced rule between them, and the description at body size in the secondary tone at the capped measure. Each row rises a little and fades in over the first fifth of its own visibility.

**Philosophy.** Introduced by a centred divider reading `HOW I BUILD` in tracked uppercase monospace with a hairline either side. Beneath it a stepper: four nodes on a faint horizontal thread, each a ring with its number below, the active one filled in the deep soft blue and the rest in the rule tone, the thread itself carrying the slow dash drift. Then one screen per principle: the number `01` to `04` at display size in the deep soft blue, a short uppercase monospace label, a fluid headline that grows with the viewport, a body paragraph in the secondary tone at the capped measure, an italic-free monospace caption naming the artefact, and the principle's own diagram.

**Systems.** Introduced by the overline `Systems` in monospace and the heading `Things people depend on at work.` Five entries. On a wide screen an entry runs two columns: the left carries the index, the year, the title, the subtitle and the status; the right carries the description, the diagram, the run log, the contribution line and the tools. The index and year are monospace separated by a rule with the index dot in the deep soft blue. The status is tracked uppercase monospace. The contribution is the label `MY PART:` in uppercase monospace in the tertiary tone followed by the contribution in the primary text tone. The tools are a middot-separated list in the secondary tone. Where the work is a client system, one monospace line in the tertiary tone carries the confidentiality sentence.

**Open source, stack and signal.** Open source is a list of repository rows, each a name, a one-line description and a language chip. Stack is a grouped list of tool names in the secondary tone, each group carrying a tracked uppercase monospace group label. Signal is the contact band, which opens the same panel the fixed button does.

**Footer.** One row: the design credit as a link with a trailing north-east arrow, and the year, in the tertiary tone.

### Route: the archive

A quiet route with no field, no rail and no diagrams. The title `Blog` at a fluid display size in the primary text tone, and the subtitle `Frequency log - tuning into thoughts on AI, taste, and craft` in monospace in the secondary tone. Each entry carries its code in brackets and its date, both monospace with the code in the tertiary tone and the date in the secondary tone, then a fluid entry title, then a summary at body size at the capped measure, present on some entries and absent on others. A hairline rule separates entries with generous space above and below. The column sits at the widest container measure, left aligned and offset from the left edge rather than centred. Entries sharpen from a blur while rising and fading in as they enter.

The entry code is a taxonomy, not decoration: `ENG` is the engineering series and `THT` is the essays series, each numbered independently, so a reader can tell at a glance which kind of piece they are about to open.

### Route: one piece

The archive's typography at reading size. The code and the date at the top in monospace, then the title at the archive's display size, then the summary as a deck a step above body, then the body in the primary text tone at the capped measure. Headings inside the body sit at card-title size with generous space above and little below. Inline links are the light soft blue, moving a step lighter when pointed at, underlined at hairline weight with a small offset. Code is monospace on the sunk tone with softened corners and no syntax colouring, because the writing is about ideas rather than about syntax. Any diagram may be embedded at the full measure width. The foot carries the previous and next entries by publication order and the subscribe control, labelled `New writing, when there is some.`, which reports back `Follow the confirmation link, and you are on the list.` The reading column is offset left, matching the archive, rather than centred.

### Route: not found

The code `404` at display size in the primary text tone, the line `This page could not be found.` at body size in the secondary tone, and the action `Return home` in tracked uppercase monospace in the accent. The page ground, the top bar present, the rail absent.

### The contact panel and the thread

The panel is a centred sheet at the narrowest container measure on wider screens and a full-screen sheet on a narrow viewport. Title `Send a signal`, subtitle `A sentence about what you are working on is plenty.`, then the name, the address, the intent as a single choice of four, the message, and the budget band revealed only when the intent is `Consulting`. Submit is the accent button reading `Send`. On success the panel replaces its body with `Sent. Your thread link is below, and it is the only way back to this note.` and the link itself. On failure the panel stays filled and shows one line in the accent: `A name, so I know who I am replying to.`, `That address does not look right.`, `A little more detail would help.`, `That is a few too many in an hour. Try again later.` or `That did not send. Try again.` with a retry. An expired thread link reads `That link has expired.`

The thread route shows the note as sent, its state, any reply, and one action: add a message. Nothing else is on that page, because the token grants nothing else.

### The studio and the desk

The studio index is a grid of cards, one per piece and one per diagram, each card carrying the drawing it represents, its code or slug, its state, and its last edit. Cards are compact so a full set fits one screen.

The wizard is three steps, each at its own address, each showing which step it is and allowing a step back without losing what was typed. Step one is the piece. Step two is the diagram: the structure on one side and the rendered drawing on the other, shown at both widths, with a scrub bar under each that drives the progress value directly from zero to one, so the author can drag the timeline and watch it play. A width toggle shows the two stacked or one at a time, and dragging a timeline stop rewrites the structure. Step three validates, reporting every illegal kind and every dangling edge with the offending item named, then exports, then publishes. Validation failing holds the preview on the last valid render and refuses the export. Saving, validating, exporting and publishing each report in an inline banner inside the page rather than in a message that disappears. The empty state reads `No diagram open` over `Create one or open an existing diagram to begin.` with a `New diagram` action.

There is exactly one author, so permissions stay simple: the studio and the desk answer an `author` session and nothing else, and they write only content that is already meant to become public, which is the containment that makes an authoring surface safe to have on a site with no other accounts. The desk is three lanes, as columns on a wide screen and stacked on a narrow one, `likely noise` presented collapsed. A card carries the name, the intent, the first two lines, the age, and the score with the six signals that produced it laid out on the card so the author can see why it landed where it did. A scoring rule the author cannot inspect is one they will stop trusting. The empty state reads `Nothing waiting` over `Notes appear here as they arrive.` with no action.

### Module and component architecture

**Layering.** Five layers, each knowing only about the one below it. Tokens know nothing. Primitives, the rule, the chip, the dot, the capsule cue, the rail, the panel, the field container, the button and the spotlight card, know only tokens. Renderers, the wireframe field, the diagram renderer and the counter, know tokens and their own inputs; they are the only stateful modules in the product and everything else takes content in and produces markup. Bands know primitives and renderers. Routes know bands and content.

One module owns the scroll listener, exposes the document progress and the per-band progress as custom properties, and is the only consumer of the scroll position anywhere in the application. This is an architectural constraint rather than a preference: it is the difference between this page holding a steady frame rate and stuttering.

### Zero-asset substitution

No binary asset ships: no image file, no video file, no font file and no vector-animation file. The wireframe still is generated from the same geometry and seed as vector line geometry at three widths and committed as text, so it stays sharp on any display. No portrait is required, because no captured surface displays one; where an author image is wanted the site draws a monogram, a softened square on the sunk tone with the initials in monospace and a hairline border. No project still is required either, because every system is represented by its diagram, which is the whole point of the design; where a link preview needs one, the same renderer flattens the system's diagram to a still with the title set in the corner. Both type families are named rather than bundled, with metric-matched fallback stacks. Every outbound address in the content, the repositories, the design credit and any social link, is a token in the content record and never a literal in the markup.

## Constraints

Single subject: there is one portfolio, one author of record, and no tenancy of any kind. Ownership applies to pieces and diagrams and to nothing else.

Absent by design: no route per project and no case-study pages; no comments, no likes, no reactions, no follower graph and no direct messaging; no public author surface beyond the studio; no search; no password reset; no payment, no pricing and no money movement anywhere in the product; no outbound email, SMS or push of any kind, because this environment carries no such service and none may be introduced; no third-party analytics, no advertising network and no external reputation service, including in the note scoring, which uses only the six signals stated above; no native mobile or desktop application; no external network call at runtime beyond the two named backing services.

The stack band is authored content describing the subject's own working tools. It says nothing about how this application is built, and nothing on it may be read as a requirement on this build.

No binary file ships with the build, and every drawing on the site is generated.

The app must stay responsive with `2000` pieces, `500` diagrams, `20000` notes, `60000` note messages, `20000` subscribers and `200000` page-view rows in the database.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password`, `role` | the account and a bearer `token` |
| `POST /api/auth/login` | `email`, `password` | the account and a bearer `token` |
| `GET /api/auth/me` | none | the signed-in account |
| `GET /api/health` | none | `200` |
| `GET /api/bands` | none | a top-level JSON array of `slug`, `name`, `start_fraction`, `end_fraction` |
| `GET /api/posts` | optional `series` | a top-level JSON array of published pieces, newest first |
| `POST /api/posts` | `series`, `title`, `summary`, `body` | the created draft with its `slug`, `number` and `code` |
| `GET /api/posts/<slug>` | none | the piece; a draft answers the owning author only |
| `POST /api/posts/<slug>/publish` | none | the published piece with `published_at` |
| `POST /api/posts/<slug>/still` | none | the piece with its `still_key`, copied from its diagram's exported still |
| `GET /api/posts/<slug>/still` | none | the still bytes; a draft answers the owning author only |
| `GET /api/diagrams` | none | a top-level JSON array of published diagrams |
| `POST /api/diagrams` | `title`, `structure`, `alt_text` | the created draft diagram with its `slug` |
| `GET /api/diagrams/<slug>` | none | the diagram and its structure; a draft answers its owner only |
| `POST /api/diagrams/<slug>/validate` | none | the findings, each naming its offending item |
| `POST /api/diagrams/<slug>/export` | none | the diagram with its `still_key` |
| `GET /api/diagrams/<slug>/render` | `progress` from `0` to `1` | the drawing at that progress, identical on every call |
| `GET /api/diagrams/<slug>/still` | none | the still bytes; a draft answers its owner only |
| `POST /api/notes` | `name`, `email`, `intent`, `budget_band?`, `message`, `referrer?`, `band?` | the created note and its `thread_token` |
| `GET /api/notes/<thread_token>` | none | that one note and its messages |
| `POST /api/notes/<thread_token>/messages` | `body` | the created message |
| `GET /api/desk` | optional `lane`, `cursor` | the lanes, their items and the next cursor |
| `PATCH /api/notes/<id>` | `state?`, `lane?`, `snoozed_until?` | the updated note |
| `POST /api/notes/<id>/reply` | `body` | the created message |
| `GET /api/availability` | `note_token` | the offered slots |
| `POST /api/bookings` | `starts_at` | the created booking |
| `POST /api/subscribers` | `email` | the recorded address and its confirmation link |
| `GET /api/subscribers/confirm/<token>` | none | a redirect to the archive |
| `POST /api/subscribers/unsubscribe/<token>` | none | the unsubscribed address |
| `GET /api/account` | none | the signed-in account's own threads plus its subscription state |
| `GET /api/views` | optional `route` | the aggregate, to the `author` account only |
| `POST /api/views` | `route`, `band` | acknowledgement |
| `GET /api/cookie-choice` | none | the recorded answer, or that none was given |
| `POST /api/cookie-choice` | `accepted` | the recorded answer |

A successful call returns the named resource or shape. An invalid or unauthorized call is rejected as a client error, never a `5xx` and never a silent success, with a message naming the reason. Every endpoint that touches an account's own data requires a bearer token; login, signup, health, the public read endpoints and the token-scoped thread endpoints answer without one.

**No mocks.** The exported still bytes live in the MinIO bucket at the pinned key and nowhere else. An in-memory map of drawings, a text column in PostgreSQL holding the drawing, a file written under the app container's own directory, a hardcoded response the app returns to itself, or a drawing inlined into the served HTML in place of the stored object are each a contract violation however convincing the page looks. The named provider is the fact - the app's UI and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A stranger can open Fieldline, read the whole portfolio on one scroll while each system's diagram plays and its run log completes, and send a note that comes back with a private thread link that opens their own note and nothing else. An author can write a piece, declare its diagram, export a still into the object store and publish, and until that publish the draft and its still answer nobody but their author. Publishing the same draft twice still leaves exactly one published piece and one stored drawing, and two people choosing the same slot to talk produce one confirmation and one refusal.
