# Vesper

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, scroll the home route from its opening curtain to its red foot, filter the project archive down to one practice field and share that filtered address as a link, create an account from a project they pressed `Add` on, find that project already waiting in their reel, add two more, drag the third to the top, reload the page and still see their own order, write a note and a brief, send the reel to the studio, and then sign in as the studio and read that reel in the client's order with the client's note intact, all without hitting an error page. Two things in that sentence cannot be arranged inside the app's own screens. The order the client left the reel in is the order the studio must read, so a reorder that is applied on screen and lost on reload is a broken product however good the drag felt, and the order must come back from storage rather than from anything the page remembered. And a reel that is still a draft must be invisible to the studio: a curator asking for a draft reel's address by hand must be told there is no such thing, because a refusal would confirm that it exists.

## Overview

Vesper is a creative studio's public site and the private client area attached to it. Both live on one origin and they are deliberately two different products wearing one identity.

The public half has one job: to make a visitor believe the studio can make something they could not make themselves. It does that by refusing to describe the work and showing it instead. The home route is close to wordless. A full-bleed pinned opening, one manifesto sentence held for two screens over a drifting particle field, four projects that each fill the screen with a floating navigator that always names the one you are looking at, four practice fields, a wall of client marks, a wall of awards, the three latest journal entries, and the red foot of the page. There is no paragraph about the studio's values anywhere on it. Four audiences read it and each is served by a different block: brand and marketing leads by the project run and the archive, procurement and producers by the practice fields and a project's credit list, peers and press and award juries by the journal and the awards wall, and an existing client mid-pitch by the reel. The archive holds fifteen projects, filterable to one of four practice fields; the journal holds ten entries, filterable to one of three kinds.

The private half closes the loop the public half opens. A visitor who has watched four projects and wants three of them has nowhere to put that. So they sign in, collect projects into a named **reel**, drag it into the order they care about, write a line of brief against each pick and a paragraph about what they are actually trying to make, and send it. The studio opens the reel with the client's own ordering and the client's own notes intact, before the first call. The studio answers by email, which is what the reel was for.

The genuinely hard part is that the client's own ordering has to survive everything: an optimistic drag, a failed write that has to put the row back at exactly the speed it left, a reload, a send that freezes the reel into a snapshot, and a read by somebody else. Every one of those is a place where an order can quietly become the order the database happened to return.

Vesper deliberately is not several things. There is no free-text search, no visitor-facing sort, no second filter that intersects with the first, no reel index or create-a-reel control, no reply field on the studio side, no notification centre or unread count, no messaging between accounts, no comments, no likes, no payments and no currency of any kind, no rich text, no dialog or modal layer, no spinner, no toast queue, no second theme, and no native application. Nothing in the build fetches an image, a film, a typeface file, a three-dimensional model or an environment map from anywhere: every picture is drawn by the browser from a seed.

## User roles

An account is one kind of thing. Authority is a property of the account's role, and the role is set where the accounts are, not in the product: there is no route that grants it, no invitation flow and no administration console. A studio of this size promotes somebody where the accounts live, and every product that grows a permissions console eventually grows a permissions bug.

The capability matrix, which is the whole permission system:

| Role | Can do | Cannot do |
|---|---|---|
| Visitor (signed out) | Read every public route, read the archive and the journal and their detail routes, read the imprint and privacy page and the terms page, filter either collection, subscribe to the journal, open `/reel` and see what a reel is, sign up, sign in, ask for a password reset | **Never create a reel, never add or remove a reel item, never reorder, never write a note or a brief, never send, never read any reel, never reach the studio queue** |
| Client | Everything a visitor can, plus: create the account's one reel by adding to it, add and remove items, reorder them, write a note against each item, write the reel's brief, rename the reel, send it once per send cycle, reopen it while it is `sent`, and delete it | **Never read another account's reel, never read the studio queue, never mark any reel answered, never grant themselves the curator role, never see any reel in state `draft` other than their own** |
| Curator | Everything a client can with their own reel, plus: read the queue of sent reels, read any reel in state `sent` or `answered` with its client's display name and address, and mark one answered | **Never read a reel in state `draft`, which must read as not found rather than as a refusal, never delete any reel including their own clients', never edit a client's title, note, brief or ordering, never send on a client's behalf** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a Client session to any Curator-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Two asymmetries in that table are deliberate and must survive. A curator reads a `sent` reel and never a `draft` one, because a draft is somebody thinking out loud and reading it over their shoulder is not on. And a curator cannot delete a reel, because the person who wrote it owns it.

The reel a request acts on is resolved from the session's own account, never from anything the caller supplied. There is no client-facing address that carries a reel identifier, so there is no identifier for a client to change. The studio's read paths do carry one, and they are the only paths that do.

Signup is open. Four accounts are seeded, all on the password `deku-demo-pw-2026`:

| Address | Display name | Role | Their reel on a first run |
|---|---|---|---|
| `client@example.com` | `Nadia Fell` | `client` | `Autumn shortlist`, state `draft`, three items |
| `client2@example.com` | `Tomas Renn` | `client` | `Rebrand longlist`, state `sent`, five items, already in the queue |
| `client3@example.com` | `Priya Sandoval` | `client` | `Everything reel`, state `draft`, eleven items |
| `curator@example.com` | `Imogen Shaw` | `curator` | empty |

## Core features

### Auth and identity

Email and password are exchanged for a session token. Sign-in returns that token in the response body and also sets it as an HTTP-only, secure, same-site cookie on the app's own origin, so a browser carries the session without any page script having to hold it; a request carrying either the bearer token or the cookie is authenticated. Passwords are stored under a memory-hard hash with a per-account salt and are never stored, logged or returned in any form that can be read back.

1. A session lasts `30` days and slides: any authenticated request older than `24` hours renews it. Signing out revokes **every** session for that account, not only the one acting, so signing out on one device signs the account out everywhere. An absent, expired or revoked session is rejected and mutates nothing.
2. Sign-up takes a display name of `1` to `60` characters after trimming, an email address, and a password of `8` to `200` characters. The address is trimmed, lowercased and capped at `254` characters. There is no email verification step and the account is usable immediately: a verification wall in front of a shortlist tool loses more clients than it protects.
3. A sign-up against an address that already has an account is refused with `That email is already registered`. This one refusal has to leak, because the visitor must be told to sign in instead, and it is rate limited hard enough to be useless for enumeration, which is the only reason the two refusals below are written the way they are.
4. Sign-in refuses a wrong password and an unknown address identically, with `That email and password do not match`. Never `no such account`. The refusal must also take the same time in both cases, so that a stopwatch does not answer the question the words refuse to.
5. A password reset asks for an address and always shows the same success surface, whether or not that address has an account, and always answers the same way. A message carrying a single-use link valid for `60` minutes is sent only when the address really has an account; nothing at all is sent when it does not. Using the link writes the new password, invalidates every previously issued reset link for that address, destroys every session for the account, and signs the client in fresh.
6. Every account has exactly one reel, created with the account in state `empty`. There is no reel list, no create control and no default reel to choose. A visitor cannot start a reel at all, and that cost is paid openly: a reel that exists in one browser and not another is worse than no reel, because the client believes they have it.

### The project archive

7. `/work` lists all `15` published projects in their authored order as a mosaic of full-width and half-width tiles. The order is fixed art direction, not a preference: nothing anywhere on the site lets a visitor re-sort a collection.
8. A row of filter controls reads `All`, `Brand Identity`, `Website`, `Visuals`, `Extended Reality`. Activating one narrows the mosaic to the projects that belong to that practice field and writes `?category=<slug>` into the address; activating `All` writes the bare path. The slugs are `brand-identity`, `website`, `visuals` and `extended-reality`.
9. A project belongs to any number of practice fields, so a filter is a membership test and not an equality test. `Second Skin` belongs to both `Extended Reality` and `Visuals`, `Tessellate` to both `Brand Identity` and `Visuals`, and `Oxbow` to both `Brand Identity` and `Website`; each must appear under both of its filters. A single-value comparison that drops one of them is the defect this rule exists to catch.
10. The filter set is single-select. Activating a second filter replaces the first and never intersects with it. With five practice fields over fifteen projects most pairs would produce nothing, and a row of controls that mostly produces nothing teaches people to stop pressing them.
11. Filtering pushes a history entry and must not scroll the page. Filtering from half way down the archive and being thrown back to the top makes the bar unusable. Going back restores the previous filter, also without scrolling. On first paint the address is read once and the filter set to match, so `/work?category=visuals` opens showing exactly `Drylands`, `Quiet Mile`, `Second Skin`, `Tessellate` and `Cold Open`.
12. A filter control is rendered only for a practice field that actually has published members, so the archive's no-results surface is reachable only when a field is genuinely empty.
13. `/work/{slug}` is a project's own case study: its work at full screen with the title across the bottom, an introduction with its practice fields listed beside it as controls, a run of media at four widths, a ruled credit list of role and name pairs, and the next project already sitting underneath the page rather than behind a button. Reaching the bottom of a project leaves the visitor already inside the next one. An unknown slug renders the studio's own not-found screen and answers with a not-found status.

### The journal

14. `/blog` lists all `10` published entries newest first in a square grid, each carrying its date in the top corner and its title in a control at the bottom left. Filter controls read `All`, `Editorial`, `Events`, `News` and narrow by the entry's kind, which is one of `editorial`, `events` or `news`. The same address rules as the archive apply.
15. Dates are written `DD/MM/YY`, zero-padded and slash-separated, everywhere they appear: on a journal tile, on a journal entry, on a reel's sent date and in the studio queue. This format is the studio's own convention and is not localised, because the date sits in a fixed-width corner of a square tile and a spelled-out month runs off it. No date anywhere on the site is relative: nothing reads `2 days ago`, because a page that says that is wrong the moment it is cached.
16. `/blog/{slug}` is the entry: a title, its date, one wide lead image, then a measured reading column, then three related entries in a band whose proportion is fixed by the design rather than by whatever the pictures happen to be. An unknown slug renders the not-found screen.

### The reel

The reel is the product. Everything above it exists so that there is something worth putting in one.

17. An `Add` control sits on every project tile in the archive mosaic, on the project detail hero, and in the home route's project navigator. It never appears on a journal tile. Its label is `Add` before the project is in the reel and `Added` after, and the change is applied the instant it is pressed rather than after the write returns, because a control that waits gets pressed twice.
18. Pressing `Add` while signed out opens the sign-in surface with `next` carrying the address that was being read, and **holds the pending add**. When the account is created or signed into, the held add is applied and the visitor is returned to what they asked for with that project already in their reel. They must not have to go back and find it again.
19. The first add moves the reel from `empty` to `draft` and writes one item at position `0`. Positions are zero-based, contiguous and unique within a reel.
20. A reel holds at most `12` items. The thirteenth add is refused: the tile control does not change, and the message `A reel holds twelve projects at most` appears in the notification strip. `client3@example.com` opens with `11` items, so one add reaches the ceiling and the next one is refused. Twelve is the client wall's cell count, which is the largest grid this design already lays out cleanly.
21. A reel has a title, `1` to `80` characters after trimming, defaulting to `Untitled reel` and edited in place on the route. Each item carries an optional note of at most `280` characters. The reel carries an optional brief of at most `2000` characters. All three write on blur, or after `800` milliseconds of idle, whichever comes first, so there is no save control anywhere in the client area and nothing to forget to press.
22. A character counter appears against a field only once `80%` of its limit has been reached, and it changes to the failure ink once the limit is passed. A counter that is always visible turns writing a sentence into sitting an exam.
23. **A row is reorderable by pointer drag, by touch drag and by keyboard, and all three produce the same write.** Pointer: press the handle and drag. Touch: long-press the handle for `300` milliseconds first, so a drag does not steal a scroll. Keyboard: focus the handle and press the up or down arrow, moving one position per press, with each move announced as `<project title> moved to position <n> of <total>`.
24. **The order write is one whole ordered list of item identifiers, never a set of index updates, and the stored order is the order that comes back.** The service rewrites every position from that list's own indices. Two consequences are both wanted: a partial reorder cannot leave a gap or a duplicate, and two sessions racing resolve as one whole list winning outright rather than interleaving into an order neither client asked for. Reordering, then reloading the page, must give back the client's order and not the order the items were added in; this is the single assertion the whole product turns on, and it is not satisfied by a page that remembers the order it just drew.
25. Removing an item rewrites the remaining positions to stay contiguous and asks for no confirmation, because it is one press to put back and confirmation on a cheap action trains people to dismiss the expensive one without reading. The strip reads `Removed.` with a `Retry` for `5` seconds.
26. Emptying the whole reel takes a second press of the same control within `3` seconds, its label changing to `Press again` in between. Deleting the account requires typing the account's own address into a field, not the word delete: typing your own address is a fact you have to know and typing a word is a reflex. Deleting an account deletes its reel, its items and its snapshots, and retains its subscriber row, because subscribing is a separate consent.

### Sending, and the studio side

27. Send validates in this exact order and stops at the first failure, showing that rule's own words: at least one item, or `Add at least one project`; at most twelve, or `A reel holds twelve projects at most`; a title present after trimming, or `Give the reel a name`; a brief within its limit, or `The brief is too long`; every note within its limit, or `A note is too long`; every item still pointing at a published project, or `One of your projects is no longer available`; and the reel still in state `draft`, or `This reel has already been sent`. A failing send changes nothing and leaves the reel in `draft`.
28. A passing send moves the reel to `sent`, writes its sent date, **freezes the reel into a snapshot** at its current version, makes the whole surface read-only, and replaces the send control with a block reading `Sent` beside the sent date and a bare control reading `Reopen`. The studio reads the snapshot and never the live reel, so a client who carries on tinkering after sending does not change what somebody is reading mid-read.
29. Send is never applied optimistically. It is irreversible from the client's side and it changes what somebody else sees, so it waits for the service. The same is true of marking a reel answered, and of signing in and out: identity is never guessed.
30. A `sent` reel can be reopened by its owner, which returns it to `draft`, clears its sent date, discards the snapshot and removes it from the queue. The strip reads `Reopened. The studio no longer sees it.` A reel that has been `answered` can never be reopened; editing it instead starts a new send cycle at the next version, and the previous snapshot is retained.
31. `/studio/reels` is the curator's queue: every reel in state `sent`, newest sent first, one row per reel carrying the client's display name, the reel's title, its item count, its sent date and a control reading `Open`. It is the one collection in the product that pages, because it is the only one that grows without bound, and it pages by handing out a cursor rather than a page number: new reels arrive at the top, and an offset page two silently repeats rows. Its empty surface reads `No reels waiting`.
32. `/studio/reels/{id}` renders one reel read-only, in the client's order, with every note and the brief, plus the client's display name and address and the sent date, and a control reading `Mark answered`. There is no reply field.
33. Marking a reel answered moves it to `answered`, writes the answered date, and makes the owner's `/reel` route carry a persistent block reading `The studio has your reel` above the item list. That block is a state and not an alert: it does not dismiss, and it stays until the client starts a new send cycle.
34. A client requesting any studio address stays where they are and is shown the denied screen with the address unchanged, because bouncing somebody who is already signed in makes them think they typed it wrong. A curator requesting a reel that is still `draft` is shown the not-found screen instead: a refusal would confirm that the draft exists.

### Optimistic writes, rollback and reconciliation

35. Applied on screen first and confirmed afterwards: adding an item, removing an item, reordering, renaming the reel, and writing a note or the brief. Waiting for the service: sending, marking answered, signing in and signing out. The line is that anything a client can undo themselves is applied first, and anything that changes what somebody else sees waits.
36. A rollback is visible and is never a dialog. A failed reorder animates the row from where the client put it back to the order the service holds, at the same speed the drag used, and the strip reads `Could not reorder. Put back.` A failed add returns the tile control from `Added` to `Add` and removes the row with the same movement the other rows used to make space for it, with `Could not add that.` A failed remove returns the row and pushes the rows below it back down.
37. **A failed text write never replaces what the client typed.** The field keeps its value, the strip reads `Not saved.` and offers `Retry`. Reverting a field to the service's older value throws away typing the client can see in front of them, and no amount of correctness justifies it.
38. Reconciliation has one rule: the service's ordering wins and the client's text wins. Two sessions that reorder the same reel resolve as one whole list winning. Two sessions that edit different fields do not clobber each other, because fields are written independently. A send that arrives for a reel already `sent` is refused as already sent and the surface reconciles to read-only rather than retrying.
39. The studio queue is the only surface that updates without a reload, and it polls rather than holding a connection open, because it changes a few times a day and one person is watching it. **No surface polls while the document is hidden.** Nothing on the public routes updates by itself.

### Filtering, forms and their one grammar

40. There is one form grammar in the product and every form is built to it: a field, a submit control beside or beneath it, a pending state in which the submit's word becomes `...` and every field is disabled, a success state, and a failure message placed outside the form's own flow so that the form does not jump when a message appears. There is no spinner anywhere in this product.
41. **A submit control is disabled when, and only when, a request is in flight.** It is never disabled because a field is empty or invalid. An empty required field produces a message on submit, not a dead control: a disabled control with no explanation is the most common way a form becomes unusable for somebody who cannot see which field is at fault. The send control is the one exception, and even there the disabled state is reachable only through a rule the client can see, which is a reel with no items, and the surface says so where the items would be.
42. A rejected submit keeps every field's value and moves focus to the field the response names, or to the form's first field when it names none. A failed request leaves the submit at rest so the client can retry without retyping.
43. The newsletter field sits in the footer of every long public route under the label `Newsletter`, takes an address, displays whatever is typed in lower case, and on success replaces the whole form with a block reading `Thanks for subscribing`. Its default failure reads `Something went wrong`. Addresses are case-insensitive, and a client typing in capitals should not see their own address shouted back at them in a line of small type.
44. Every string a visitor supplies is trimmed, length-checked and stored as text, and rendered back as text and never as markup. There is no rich text anywhere in the client area and none should be added. Pasting a booby-trapped fragment into a note, saving it, reloading and opening the reel as a curator must show the literal characters that were typed, in both places: nothing executes, and just as importantly nothing is silently stripped or rewritten, because a field that quietly edits what you paste is not trustworthy for pasting a real reference into.
45. The `next` parameter is validated as a path and never as a location: it must begin with a single `/` and must not begin with `//`, and anything else is replaced by `/`. A `category` value that is not a known slug is treated as absent.
46. Requests are rate limited, and two of the limits deliberately answer with success rather than a refusal, because refusing would reveal whether an address is known: a repeat newsletter submission for the same address inside an hour is accepted and silently discarded, and a repeat reset request for the same address inside `15` minutes answers exactly as the first one did. Sign-in, sign-up and send are limited too, and those refusals are visible.

### The messages the product sends

47. Four messages exist and no more. A welcome message when an account is created, subject `Vesper: your reel`, carrying one paragraph about what a reel is and a link to `/work`, sent once and never repeated. A reset message, subject `Vesper: reset your password`, carrying the single-use link and one line saying to ignore it if it was not requested. A confirmation to the client when a reel is sent, subject `Vesper: we have your reel`. And a notice to the studio at `contact@vesper.works` when a reel is sent, subject `New reel from <display name>`, which carries the client's display name escaped and does not include any note text at all.
48. There is no notification centre, no unread count, no bell and no digest. A shortlist tool that grows an inbox has quietly become a different product. Inside the page there is exactly one transient surface, the notification strip: one message at a time, at the foot of the window, wiping up from the bottom edge, leaving after `5` seconds, optionally carrying a bare `Retry` control, and replacing its own text rather than re-animating when a second message arrives. It shares its shape with the offline bar and the two never appear together: while the connection is gone, the offline bar owns that strip.

### Analytics, instrumentation, and what is never measured

49. The product records its own page views and a named set of events with their route and the moment they happened, readable by a curator and by nobody else. The events are `route_view`, `hero_scrolled`, `mission_seen`, `project_opened`, `navigator_used`, `filter_applied`, `filter_cleared`, `signal_opened`, `contact_opened`, `newsletter_submitted`, `newsletter_result`, `sign_in_started`, `account_created`, `reel_item_added`, `reel_item_removed`, `reel_reordered`, `reel_note_written`, `reel_sent`, `reel_reopened` and `reel_answered`. The single most useful property on that list is `surface`, carried by `project_opened` and `signal_opened`, which is one of `home_run`, `home_navigator`, `archive`, `project_detail`, `journal`, `footer`, `mobile_panel` or `reel`, because it is what tells the studio whether the home route's four projects or the archive's fifteen are doing the work.
50. Nothing anybody typed is ever recorded. No email address in any event, no reel title, no note text, no brief text, no display name, no address with its query string attached, and no pointer coordinate. A note event records a `length_bucket` of `short`, `medium` or `long` rather than a character count.
51. A first-time visitor is asked once about measurement, in the notification strip rather than in a dialog, and the answer survives a reload. Nothing is recorded before that answer. **Refusing must leave the entire product, including signing in and building and sending a reel, working identically**, and the question must not return.
52. Four counts are kept regardless of that answer, because none of them identifies anybody: reels sent per week, the median item count of a sent reel, the median hours from sent to answered, and newsletter submissions and failures.

### The pages that are not the work

53. An imprint and privacy page lives at `/legal/imprint-privacy-policy`, is linked from the footer's own bottom rule on every route that carries a footer, and states in plain words what the product stores about a client, what it never records, and how long a session and a reset link last. A terms page lives at `/legal/terms`, is reachable from the same footer rule, and is linked from the sign-up form beside the submit control.
54. Every internal link on every public route resolves. A footer link, a navigation control, a tile link, a filter control, a related-entry link, a next-project link and the not-found screen's way home all lead somewhere that answers.
55. An address that matches nothing renders the studio's own not-found screen and answers with a not-found status. It must not be a redirect to an address that answers as though it were found. Wrong addresses arrive in quantity, many of them looking like third-party tracking paths, and a site that answers those as real pages gets a few hundred of them indexed.
56. Every public route carries its own title and its own description, and no two routes share either. `/` reads `Vesper - Creative Innovation and Digital Futures`, `/work` reads `Our Portfolio - Vesper`, `/blog` reads `Signals`, `/contact` reads `Contact - Vesper`, `/legal/imprint-privacy-policy` reads `Imprint & Privacy - Vesper`, `/legal/terms` reads `Terms - Vesper`, `/sign-in` reads `Sign in - Vesper`, `/reel` reads `Your reel - Vesper` and `/studio/reels` reads `Reels - Vesper`.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | The argument, end to end: hero, manifesto, four projects, practice fields, clients, awards, latest entries, footer | public |
| `/work` | The filterable project archive, fifteen tiles | public |
| `/work/{slug}` | One project's case study, with the next project underneath it | public |
| `/blog` | The journal index, ten entries in a square grid | public |
| `/blog/{slug}` | One journal entry and its related entries | public |
| `/contact` | One screen: a headline, a control, the studio's address block | public |
| `/legal/imprint-privacy-policy` | Imprint and privacy, one measured column | public |
| `/legal/terms` | Terms of use, the same column | public |
| `/sign-in` | Identity, in four modes carried by the query: sign in, `?mode=create`, `?mode=reset`, `?mode=set` | public |
| `/reel` | The account's one reel. Renders for a signed-out visitor, showing what a reel is | public to read, owner to act |
| `/studio/reels` | The queue of sent reels, newest first | curator |
| `/studio/reels/{id}` | One sent reel, read only, in the client's order | curator |
| anything else | The studio's own not-found screen | public |

The words and the addresses disagree on purpose. The navigation reads `PROJECTS`, `SIGNALS` and `CONTACT` while the addresses underneath are `/work`, `/blog` and `/contact`. Keep both: the addresses are what has already been linked to, and the words are what the studio calls the things.

**Entry and redirects.**

- A signed-out request for `/studio/reels` or `/studio/reels/{id}` redirects to `/sign-in?next=<the path that was asked for>` and returns there once the session exists.
- A signed-in Client requesting any `/studio` address is **not** redirected. The denied screen renders at that address, with the address bar unchanged, reading `Not your reel` above a control reading `back to yours` that points at `/reel`. A gated route redirects, a forbidden route renders: if signing in might legitimately make the visitor allowed, send them to sign in and bring them back; if they are signed in and still not allowed, do not send them anywhere.
- `/reel` renders for a signed-out visitor, showing the route's own heading and the signed-out empty surface reading `Sign in to start a reel` above a control reading `Sign in`. It is the one gated surface that never bounces, because the point of a reel is understood by seeing an empty one.
- `/sign-in` requested by a signed-in Client redirects to `/reel`; requested by a Curator, to `/studio/reels`.
- A session that expires mid-edit sends the writer to `/sign-in?next=/reel` with the pending write held, and replays that write once the session is fresh. Nothing the client typed is discarded on the way.
- Signing out revokes every session for the account and returns to `/`.
- `next` must begin with a single `/` and must not begin with `//`; anything else becomes `/`.

**Journey 1, the reel, end to end.** Open `/work`. The mosaic shows fifteen tiles, `Nightshift` first. Press `Add` on `Nightshift` while signed out: the sign-in surface opens with `next=/work` and the add is held. Switch to create mode, enter `Nadia Fell`, an address and a password, and submit. You are returned to `/work`, `Nightshift` is already in the reel, and its tile control reads `Added`. Press `Add` on `Ferrous` and on `Kiln House`. Open `/reel`: three rows in add order, under the title `Untitled reel`. Press the title, type `Pitch shortlist`, click away; the title is written. Focus the third row's handle and press the up arrow twice, or drag it to the top; `Kiln House` becomes the first row and each move is announced. Reload the page: `Kiln House` is still first. Write `This is the one` in the first row's note. Write `A launch film for a new product` in the brief. Press `Send to the studio`. The curtain sweeps across without a navigation, the surface turns read-only, and a block reads `Sent` beside a `Reopen` control.

**Journey 2, the studio.** Sign out, sign in as `curator@example.com`, open `/studio/reels`. `Pitch shortlist` sits at the top of the queue beside `Nadia Fell`, its item count and its sent date, with a control reading `Open`. Open it: `Kiln House`, `Nightshift`, `Ferrous` in that order, with `This is the one` against the first and the brief below them. Press `Mark answered`. Sign back in as the client and open `/reel`: the block above the list reads `The studio has your reel`.

**Journey 3, browsing and filtering.** Open `/`. A curtain covers the first load with a count filling in from the left. Scroll: the opening swells and fades through into the manifesto sentence, which holds for two screens while the particle field fades up behind it; then four projects each fill the screen, and the floating navigator's thumbnail, label and destination always agree with the project you are looking at. Follow the run's control to `/work`. Press `Visuals`: the address gains `?category=visuals`, five projects remain, the page does not jump, and the active control reads as a solid block. Copy that address, open it in a fresh window, and the archive opens filtered. Press `All` and all fifteen return with the bare path in the address.

**Journey 4, the refusals.** Signed in as `client@example.com`, open `/studio/reels`: the denied screen renders where you are. Signed in as `curator@example.com`, open the address of a reel that is still `draft`: the not-found screen renders instead, because a refusal would say it exists. Signed in as `client3@example.com`, whose reel already holds eleven items, press `Add` twice more: the first succeeds and the second leaves the tile control unchanged while the strip reads `A reel holds twelve projects at most`.

**States.**

- Every collection has an empty surface built from the same three parts: the section mark, one line of small capitals naming what is empty, and, where there is something to offer, one control. `No projects in this field` with `Show all projects`. `No entries of this kind` with `Show all entries`. `Your reel is empty` with `Browse projects`. `Sign in to start a reel` with `Sign in`. `No reels waiting`, with nothing to offer.
- Three surfaces are simply not rendered when they are empty rather than announcing it: related entries, the client wall and the awards wall. A studio with no awards should not carry a box saying it has no awards.
- Every loading surface is a placeholder block at exactly the size of the thing it stands in for, with a soft band sweeping across it, so that nothing on the page moves when the content arrives. A placeholder at the wrong size is worse than none.
- Every failed load shows the empty surface's layout with the line `Could not load this` and a control reading `Try again` that re-fires the request. A single row that has lost its project instead keeps its layout, fills its thumbnail well with the panel ink, replaces its title with `No longer available`, outlines itself in the failure ink, and keeps only its remove control live.
- Losing the connection raises a strip at the foot of the window reading `You are offline`, or `You are offline. Changes will be saved.` while a reel edit is being held. Held writes replay in order when the connection returns. A send while offline is blocked before the request and reads `Could not send. Your reel is safe.` Nothing a client typed is discarded by any of this.
- The states are checked in one order and a surface never shows two at once: offline, then loading, then failure, then empty.
- An error anywhere renders a surface. Nothing crashes the app into a blank page.

## UI/UX notes

**The north star.** Somebody arriving should believe, within one screen and without reading a word, that this studio can make something they could not make themselves, and should learn it by being shown rather than told.

**The register.** This is consumer and editorial work, not an operational tool. The subject itself is the first thing seen, the interface is as quiet as it can be while still being findable, and the page is allowed to carry atmosphere. It is not a dashboard and must never read as one: no panel chrome around content, no dense tabular arrangement of the work, and no marketing composition standing in for the work itself.

Four stances, each of which a competing studio could rationally invert. **Showing over explaining**: a studio that led with its process and its values would be making a different argument, and this one does not. **Continuity over sections**: the home route reads as one unbroken take, and the seams between its blocks are things to hide rather than to mark. **Restraint over range**: three colours, one interactive shape, one gap, one typeface. **One gesture repeated over a vocabulary of gestures**: the same rising fill answers every press on every route, so the interface never has to be learned twice.

**The palette, by role.** Three inks do all the work and there is no fourth. The ground is a near-black neutral, and every route except the foot of the page sits on it. The ink is a near-white neutral: body text, every hairline outline, every icon fill, and the default accent. One mid, vivid red is the signal, and it is the only accent on the ground; it is also the whole field of the footer, the whole field of the mobile panel, both curtains, the scroll marker, the wordmark in the opening, and the only light in the particle scene. A second red, one visible step hotter than the signal and used nowhere else, picks out emphasis runs inside project introduction copy; it never appears on a control and never on the ground. Beyond those there are exactly three translucent tints of the same two neutrals: a panel weight of the ink used as a fill behind content, a rule weight of the ink used only as a line, and a divider weight of the red used once. The rule for choosing between the two ink tints is the one that decides it every time: if the thing being coloured has height, it is the fill; if it has only length, it is the rule. The exact values are yours, so long as the ground is near-black, the ink is near-white, the two reds differ by one visible step of heat, and no other colour family appears anywhere in the product.

**What the palette must not become.** Not a page dominated by one hue with no second signal. Not a red used often enough that it stops reading as the brand and starts reading as decoration. Not a fourth colour introduced to distinguish a state that the three already distinguish.

**Type.** One grotesque, three weights, no italic and no second family. Give it a tall x-height, terminals cut square rather than angled, a double-storey lowercase letter shape rather than a single-storey one, and tight default spacing, because the whole display ramp is set slightly tighter than its natural fit. The three weights must stay distinguishable at label size, because the lightest and the heaviest sit beside each other in the opening counter.

Two type regimes, and unifying them is the mistake somebody will eventually try to make in the name of consistency. Display type is set tight, because it is there to be looked at. Journal body copy is set visibly looser than everything else on the site, because somebody is reading it. Do not make them match.

Display sizes grow smoothly between a phone width and a large-laptop width rather than stepping at thresholds, and hold still above and below those two anchors. The small uppercase labels never grow at all, at any width, because a signpost that scales stops reading as a signpost. Every heading honours the line breaks its copy was written with rather than reflowing them: the break is part of the composition.

**Shape and density.** Nothing anywhere has a rounded corner. Nothing casts a shadow. That is load-bearing rather than austere: the square corner is what makes a hairline outline read as a technical drawing rather than as a soft chip, and it is the difference between this reading as expensive and as generic. The only soft effect in the whole system is a frosting behind every control, and it is not decoration either: this product constantly puts near-white hairlines over bright moving pictures, and the frosting is the only reason they stay legible.

One gap separates every two pieces of media, everywhere, and it is the same gap at every width. Every fractional tile subtracts its own share of that gap from its own width. Get the subtraction wrong and a thin dark seam blinks in and out every time somebody resizes their window. The public routes read spacious, with sections separated by space rather than by dividing rules, and the client area's rows read compact, tight enough that a full reel is one stack rather than a scroll. **Space over dividers** is the rule: a section that needs a line drawn under it to read as a section has not been given enough room.

**Layering.** The layers form one strict stack and nothing new should be inserted between two of them without moving a whole tier: the opening curtain above the route-change curtain, above the wordmark, above the scroll marker, above the navigation, above promoted content, above the scene, above local layers, above the ground the particle canvas sits on. The wordmark sitting under the navigation and over the scroll marker is deliberate: a navigation bar passes cleanly over the wordmark during a page change, and the scroll marker can never cover either.

**The one interactive shape.** Almost every clickable thing in this product is the same object: a short bar with a hairline outline, a frosted backdrop, and a block of ink that rises from below when it is pointed at or when it is the active one. As the fill rises, the word inside swaps for a second copy of itself in the opposite ink while the resting copy leaves upward, and the arrow in its well slides out to the right while a fresh one arrives from the left. It has resting, pointed-at, pressed, focused and unavailable states; unavailable is never signalled by colour alone. There are four variants of it and no more: default on the ground, accent-bound so that it takes whatever ink its section declares, solid, and solid on red. A bare variant drops the frosting, the fill, the outline and the minimum width and narrows its icon well, and the footer and contact links are the only things that use it.

Two rules about that object are worth protecting. The fill arrives faster than the ink changes, so the block lands first and the word settles into it; equalising the two makes the control feel mushy. And its outline changes colour only, never width, because a hairline that animates its width shimmers.

**The accent declaration.** Every stretch of page declares once which of the two inks the interactive elements inside it should carry, and every control, label, rule and icon inside reads that one declaration rather than deciding for itself. The wordmark reads a separate declaration of its own, so it can stay near-white while a whole section turns red. The practical effect is that a new section dropped onto the red ground comes out the right colour without anything inside it being told.

**Motion.** Movement here is continuous rather than incidental, and it is the thing that most decides whether this reads as one studio or as a template. Everything that changes state and will change back, such as a control lighting up or a panel opening, moves on one curve; everything that arrives once, such as a reveal or a regroup, moves on a second, faster-starting curve with a longer tail; the two curtains have a third curve reserved to them alone, and using it anywhere else removes the one thing that makes changing page feel unlike an interaction. There is a fourth curve used exactly once, for the travel of a revealing paragraph. Those four are the entire vocabulary.

The signature moment is the headline reveal, and it is neither a fade nor a slide. Every headline is present and laid out before it is seen, hidden under a soft-edged window sitting below the words. As the headline comes into view that window travels up through the letters, uncovering them, while the whole line rises a fraction of its own height; each line waits a beat longer than the line above it, so a three-line headline unrolls rather than appearing. It is tied to where the page has been scrolled and not to a timer, so scrolling back up visibly un-reveals it rather than replaying it. If the reverse animates instead of snapping back, the whole page starts to feel like a slideshow, and that one detail is the difference between the motion feeling attached to a finger and feeling played at somebody.

Everything else that moves is named, because a moment that is named gets built and a moment that is summarised does not. The control fill rises and its label swaps. The menu bars fold into a cross, turning about the bar that was already centred. The mobile panel wipes down from its top edge and its contents settle into place a beat behind the wipe rather than arriving with it. The opening curtain flashes to the signal colour while it initialises, its counter fades in, the wordmark behind the counter fills in from the left in step with the count, and the two halves then leave sideways along the diagonal. The route-change curtain sweeps the same diagonal slightly faster. The scroll marker fades in when a gesture begins and out again when it ends. The scroll indicator appears once, at the top of the home route, and never returns. A journal tile grows inside its own row on a wide screen and grows its picture behind a fixed frame on a narrow one, never both. An archive tile expands to take the full row over the longest movement anywhere in the product, and its own label fades out as it does, because a small control stretched across a doubled picture reads as a mistake. The navigator's labels and its arrow well change ink together. The wordmark changes ink when a section changes accent. The foot of the page carries the studio's name drifting sideways forever on a narrow screen. The particle field drifts and tumbles continuously while it is in view. The contact object turns slowly on the spot. The word inside an active control crawls upward as the page scrolls, two copies chasing each other exactly one line apart so the loop has no seam. And the filter row pans under a finger, with a rubber band at its start that springs back rather than stopping dead.

**Reduced motion, and vestibular safety.** Movement makes some people ill, so this is a safety requirement and not a preference. When a visitor has asked their system for less movement, everything that plays without being asked for stops and holds its first frame: the drifting name in the foot, the particle field, the rotating object, the crawling label. Every reveal becomes a state, applied at once, with the text present and readable, because it always was; only the window over it is removed. Everything that answers a direct action is kept and still animates, because a control that does not respond reads as broken rather than as calm. The curtains are the judgement call: they are not asked for, and removing them entirely makes a route change a hard cut, so they fade in place instead of travelling.

**The diagonal.** The letterforms lean. The two curtains are split by a diagonal. The band of repeated wordmarks across the contact route lies at an angle. All three are the same angle, and that is the strongest single piece of art direction in the product: everything here leans the same way. The diagonal is defined against the height of the window rather than its width, so it holds its angle on a wide screen instead of flattening, and it degrades to a straight vertical split on a very tall one rather than to nothing. If the wordmark is redrawn, redraw the diagonal to match it, or the product quietly stops holding together.

**Accessibility, which is a floor and not a preference.** All text meets the WCAG AA contrast bar against the ground it is set on. That has one consequence this design must accept rather than inherit: small text is never set in the red on the near-black ground, because at label size that pair is too dim for a large number of people to read. Red stays for the display steps, which are large enough, and for the diagonal, the marks and the giant numerals; small labels on the ground are near-white. The palette does not change and the page looks almost identical.

Every focusable element carries a visible focus treatment that is distinguishable from its hover treatment: pointing at a control raises its fill, focusing it thickens its outline, and the two must never be told apart only by guessing. Nothing removes focus visibility without replacing it. Full keyboard navigation reaches every control in reading order on every route, the first focusable thing on every route is a skip control that jumps into the main content, the mobile panel is the only keyboard trap in the product and it releases on Escape and returns focus to the button that opened it, and the reel reorders by keyboard alone with every move announced. Touch targets are comfortably sized. Icon-only controls carry a name. Meaning is never carried by colour alone: the active filter is a solid block as well as a different ink, and a row that has lost its project says so in words as well as in its outline.

One polite live region per route carries exactly four kinds of message and nothing else: a filter applied, a filter cleared, a reel row moved, and whatever the notification strip is currently saying. A live region that announces scroll progress, reveal states or hover changes is worse than none, because none of those is a change the visitor asked for.

Two things this design honestly cannot fix, and they are stated rather than pretended away. It is dark only; there is no light theme and adding one would make it a different product, so it must instead survive a forced-colours mode, which means every hairline is drawn as a real border or outline rather than as a background so that forced colours can see it. And the opening sets words over a moving picture, whose brightness is not knowable in advance, so the region the words sit in carries a darkening layer whenever the picture behind it is bright there.

**Responsive.** Three widths, and the layout holds at every width between them rather than only at the three. On a phone the three navigation words collapse into one square button that pulls a full red panel down over the page; grids step down in column count; the foot of the page carries the drifting name; the archive's tiles all take the full width at a taller proportion; the filter row becomes pannable; the reel's rows stack into three lines and lose their drag handle, because a handle on a three-line row has no obvious grab point and reordering falls back to the arrow controls that are the keyboard path anyway. At a narrow viewport nothing overflows sideways, no content is clipped, and every navigation target stays reachable.

A few things deliberately never change with the width: the gap between two pieces of media, the height of a control, the size of a label, the size of an icon, the angle of the diagonal, the theme, and the beat between one revealing line and the next. If those grew with the screen the product would stop feeling precise.

Every hover effect is gated on a device that actually has a pointer, and there are only a handful of them: the control fill, the label swap, the icon swap, the menu bars and the journal tile. On a touch device none of them run, which is why a control whose readable state is its filled state is held permanently filled there.

Full-height surfaces are measured against a height the page computes for itself and rewrites on every resize, rather than against the browser's own idea of the screen, so a phone's collapsing address bar does not resize the opening mid-scroll. That is the single most common way a product like this feels broken on a phone. On a short landscape phone the opening's headline drops a step rather than the wordmark shrinking: the wordmark is the opening, the headline is not.

The product does not print, and it says so rather than producing sixty pages of black. A print treatment drops every fixed layer, inverts to dark ink on a light ground, and prints the legal routes and the journal body only.

## Technical requirements

The application is a server-rendered multi-page product. **Express** serves every route and **Nunjucks** renders the markup on the server, so the first response already carries the archive, the journal and the reel's rows as real markup rather than as an empty shell. **Alpine.js** progressively enhances the parts that need behaviour in the browser: the filter row, the tile expand, the reel's in-place editing and its reorder, the notification strip and the offline bar. The scroll subscriber, the reveal machinery and the two real-time canvas layers are authored directly against the platform rather than through a component framework, because they write values to the style layer rather than into a component tree. The observable consequence of this rendering model is that a route's content is in the first response: a visitor with script disabled can still read every public route, follow every internal link, and use the filter controls as ordinary links.

The datastore is **PostgreSQL**, reached at `DATABASE_URL`. The public address and port are `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Read all three from the environment; never hardcode a host or a port. These backing services are already running and reachable at those variables and must not be downloaded, installed, compiled or started.

> Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing service available in this environment is PostgreSQL, and reaching for anything else is a contract violation.

`GET /api/health` returns `200` once the application holds a database connection and the seed has completed. Request logs are structured lines on standard output carrying the method, the path, the status and the duration. A log line never carries a session token, a password, a password hash, a reel title, a note or a brief.

**Every public route carries its own title and its own meta description, and no two routes share either.** The titles are pinned in `## Core features`; each description is one sentence about that route in particular, not a repeat of the studio's own summary.

**No credential reaches the browser.** Nothing the browser downloads contains a database address, a session secret, a password hash or any administrative token, in markup, in script, in a style sheet or in a comment.

**Security and abuse are handled at the service, on every request, resolved from the session and never from anything the caller controls in a body or a header.** The per-path rules and the rate limits are in the core features above; the transport rules close this section.

**The zero-asset rule, and the substitution that makes it work.** Nothing is fetched from outside the application's own origin. No image, no film, no typeface file, no three-dimensional model, no environment map, no measurement tag and no third-party script. Every picture in the product is generated in the browser at the size of the slot it fills, from a seed derived from the slug of the thing it stands for, so the same project always produces the same picture and a reload does not reshuffle the page. A generated picture is two soft pools of colour on the ground, angled by a value derived from that same seed, with a fine grain laid over it. The grain is inline vector turbulence at a fine base frequency, drawn over a few octaves so that it carries tonal variation without structure, flattened to grey so that it does not tint the field, and kept faint enough to read as grain rather than as noise; a project thumbnail additionally carries its own index set very faintly through the middle, so a placeholder grid is legible during a build without reading as a missing-image icon. Only ledger colours are used, at stated transparencies. When real media arrives it replaces the generated output at the same proportion and nothing else changes.

The particle form is an irregular faceted solid: a subdivided icosahedron whose vertices are displaced along their own normals by a deterministic amount and whose normals are then recomputed flat rather than smooth. Flat is the load-bearing word, because the lighting reads face normals and a smooth form catches no glint. The contact object is composed from primitives and its parts keep five name prefixes, `Shell`, `WindShield`, `Vent`, `Sticker` and `Trim`, because materials are selected by name prefix rather than by index, so any replacement object that keeps those prefixes works unmodified. The environment that object reflects is drawn into an equirectangular canvas: a sky filling the upper half as a vertical gradient from a strong near-white at the zenith to a weaker one at the horizon, a soft blurred horizon band, a dark lower half lifting towards that horizon, one bright key light, one weaker fill light, and one red bounce along the lower flank; that bounce is the only thing tying the object to the palette, and the object at its stated roughness is almost entirely made of its reflections, so it is worth building carefully.

**There is exactly one scroll subscriber in the whole product.** It reads all geometry first, then writes every derived value to the style layer as custom properties; every element that moves reads those properties and never subscribes for itself. Each participating element's own box is cached and invalidated on resize only. The scroll position used is the interpolated one the subscriber already holds, never re-read from the document inside a frame. The archive is the stress case, with well over a hundred elements consuming a scroll-written value at once on a narrow screen, and it must still be one computation with many readers. The observable property: resizing the window or scrolling fast must not make the page stutter, and no element may animate a property nobody asked it to, which means every transition names the properties it applies to rather than applying to everything.

Media loads only once it is within one viewport height of the visible area, plays only while it is intersecting, is paused rather than merely hidden when it is scrolled past, and at most two pieces of moving media play at once. Every moving picture carries a still first frame so that something is painted before it decodes. All moving media is muted and plays inline.

Both real-time surfaces render at the device's own refresh rate while visible, **stop rendering entirely when the document is hidden**, and reduce resolution rather than drop frames when they miss their budget. The ladder, in order: raise resolution while comfortably inside budget; fall back to the default; reduce resolution once; halve the instance count; turn off edge smoothing; and finally stop the frame loop and hold a single static frame. A single frame of the particle field is a still picture of a rock field, which is a perfectly good background, so the surface is never removed entirely: the layout above it assumes a dark ground and a suddenly empty layer reads as a fault. A visitor who has asked for reduced motion, or a device with no hardware acceleration, goes straight to the last rung from the first frame.

The five values that shape the particle lighting, which are its shininess, its light intensity, its specular strength, its light radius and its light colour, are read once at start from a single configuration source so they can be changed without editing program source. No control surface for them is reachable in the running product, and no styling for such a surface ships.

Every response carries a strict transport policy, a nosniff content-type policy and a policy that refuses framing by another origin, and the session cookie is HTTP-only, secure and same-site. The application accepts no cross-origin request.

## Data model

Sixteen tables. All timestamps are UTC, and calendar-day logic uses server-side UTC today. The entities, their relationships and cardinality, and the rules about persistence and migration between one send cycle and the next are all below.

> **Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**`category`** - `id`, `slug`, `name`, `scope`, `position`. `scope` is `project` or `signal`. `slug` is lowercase kebab and unique. Four project-scope rows: `brand-identity`, `website`, `visuals`, `extended-reality`. Three signal-scope rows: `editorial`, `events`, `news`.

**`project`** - `id`, `slug`, `title`, `subtitle`, `intro`, `credits`, `published`, `position`, `tile_width`. `tile_width` is `full` or `half` and is the authored mosaic rhythm. `position` is the authored archive order and is not derived from anything. `credits` is an ordered list of role and name pairs.

**`project_category`** - `project_id`, `category_id`. A project belongs to any number of practice fields, so this is a set and the filter is a membership test over it.

**`signal`** - `id`, `slug`, `title`, `kind`, `published_on`, `body`, `published`. `kind` is `editorial`, `events` or `news`. The index is ordered by `published_on` descending and that order is not configurable.

**`signal_related`** - `signal_id`, `related_signal_id`. Up to three per entry.

**`client_mark`** - `id`, `name`, `position`. Twelve rows. **`award`** - `id`, `name`, `caption_line_1`, `caption_line_2`, `position`. Four rows, and the two caption lines are a pair that must not be reflowed into one.

**`account`** - `id`, `email`, `display_name`, `password_hash`, `role`, `created_at`, `last_seen_at`. `email` is unique, trimmed and lowercased. `role` is `client` or `curator`. `id` is an opaque string, never a sequential integer: a sequential identifier makes the studio's workload countable from outside, and that applies to every table here.

**`session`** - `id`, `account_id`, `token_hash`, `created_at`, `last_used_at`, `expires_at`, `revoked_at`. Only the hash of a session token is stored.

**`reset_token`** - `id`, `account_id`, `token_hash`, `expires_at`, `used_at`. Single use, compared in constant time, and deleted on use.

**`reel`** - `id`, `account_id`, `title`, `brief`, `state`, `version`, `sent_at`, `answered_at`, `updated_at`. `account_id` is unique: an account has exactly one reel, created with the account in state `empty`. `state` is one of `empty`, `draft`, `sent`, `answered`. `version` starts at `1` and increments per send cycle. `title` is `1` to `80` characters after trimming and `brief` is at most `2000` characters. `sent_at` is written on send and cleared on reopen; `answered_at` is written when a curator marks it.

**`reel_item`** - `id`, `reel_id`, `project_id`, `position`, `note`, `added_at`. `note` is at most `280` characters. **A reel holds at most twelve items, and within one reel the set of positions is always exactly the integers from zero to one less than the item count, each appearing once.** That property must hold after every add, every remove and every reorder, and after two reorders that arrive at the same moment: one of them wins whole, the other does not interleave with it, and the reel is never left with a gap, a duplicate or a thirteenth row. The same project must not appear twice in one reel.

**`reel_snapshot`** - `id`, `reel_id`, `version`, `title`, `brief`, `items`, `sent_at`. Written when a reel is sent and holding the ordered items with their notes as they stood at that moment. The studio reads the snapshot; a reopen discards it.

**`subscriber`** - `id`, `email`, `created_at`. The address is unique across the table. A subscriber row outlives the account that created it.

**`outbox_message`** - `id`, `to_address`, `subject`, `body`, `created_at`. The four transactional messages are written here, readable by a curator. A message body never carries a note or a brief.

**`event_log`** - `id`, `name`, `route`, `properties`, `created_at`. `name` is one of the named events. `properties` never carries an address, a display name, a title, a note, a brief or a pointer coordinate.

Derived rather than stored: the item count of a reel, the median item count of a sent reel, the hours between sent and answered, the number of projects matching a filter, and the ordinal the navigator shows. None of those is a column.

The reference from a reel item to a project crosses a boundary and is deliberately not treated as guaranteed. It is checked when the reel is read and again when it is sent, and never assumed: a project can be withdrawn between an add and a send, and the row renders as no longer available rather than disappearing.

Deleting an account deletes its reel, its items and its snapshots, and leaves its subscriber row. Deleting a project never deletes a reel item. Deleting a category removes it from its projects and never deletes a project.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

`## UI/UX notes` states the direction. This section states the product's surfaces one by one, so that nothing has to be inferred. It carries no colour value, no pixel, no duration and no curve: every one of those is yours, and the properties below are what they have to satisfy.

### The token layer, typography and scaling

Three inks, three transparent tints of them, one interactive shape, one gap, one type family, one set of layers. Everything in the product resolves to that list, and a component that declares a colour, a curve, a spacing step or a type size of its own has become a second design system. Two exceptions exist and both are named here: the hotter red used only for emphasis inside project introduction copy, and the divider tint used only between practice fields on a narrow screen.

Typography is one family at three weights, and its personality is described above; what belongs here is how it scales. Scaling works in three regimes and the build reproduces all three rather than picking one. Display type is fixed below a narrow anchor width, interpolates linearly between that anchor and a wide one, and is fixed again above the wide anchor. The page gutter steps at the tablet breakpoint and then becomes proportional to the viewport at the desktop breakpoint. Each of those two breakpoints carries a paired ceiling, so a rule that applies above one has a matching rule that applies below it. The two anchors that bound the type interpolation are not breakpoints at all: nothing about the layout differs across either of them. Full-height surfaces use a height the page computes for itself and rewrites on load and on every resize, rather than the browser's own viewport-height unit, so that a mobile browser's collapsing chrome does not resize a full-screen block mid-scroll.

### Iconography

Six glyphs, all drawn as inline vector geometry. None is a font glyph and none is a separate file, which is what lets the product ship with no assets at all.

1. **The arrow.** A horizontal shaft with a chevron head, drawn as one closed filled outline rather than as a line plus a caret, so nothing thins when it is scaled. It means "go here". It sits in the navigation bars, the mobile panel's rows, the project navigator and every control's icon well.
2. **The outbound arrow.** The same construction rotated to point up and to the right, drawn on a canvas one unit smaller so that it optically matches the horizontal arrow beside it. It means "this leaves the site", and it marks the contact address, the two social destinations and the legal link.
3. **The section asterisk.** A six-pointed mark: one vertical bar through the centre and two bars of the same width crossed over it at sixty degrees. It sits centred inside a small square box carrying its own hairline outline, and every section on every route opens with it.
4. **The menu bars.** Not a path but three short blocks, each centred about the same point inside a square that carries the same rising fill and hairline outline as every other control. Closed, one bar sits centred and two are held above and below it. Open, the centred bar and one other rotate into a cross while the third leaves sideways and fades. The bar that is already centred when closed is the one the cross turns about; drawing them in the obvious order rotates the cross about the wrong bar.
5. **The scroll indicator.** A mouse body outlined at a constant weight with a wheel dot inside it and a dashed ring around the whole thing, with the capsule drawn twice so the second copy can pulse by scaling. It is drawn in the signal red.
6. **The not-found numerals.** Three enormous numerals as a single path, filled in the signal red, sized against the width of the window with a ceiling against its height.

Rules for a seventh glyph, because the set is small enough that one will be needed and small enough that an inconsistent one will show. Use the same square canvas the other four share. Keep one constant stroke weight, expressed as a fraction of the canvas rather than as a size, so nothing has a light or a heavy variant and nothing scales its weight with its rendered size. Draw closed filled outlines, never strokes. Use only right angles and half-right angles for arrows, and only thirds of a half turn for radial marks; no other angle appears anywhere in the set. Give any glyph that is clickable in its own right a full-canvas transparent hit area as its first path, so the target is the box rather than the strokes. A diagonal glyph drops to the smaller canvas and keeps the same absolute weight, which reads correctly beside an orthogonal one; do not instead scale the larger glyph down.

### The wordmark

The wordmark is the loudest thing in the product. It is set edge to edge across the full width of the window twice on the home route: once across the middle of the opening, and once as a drifting band in the foot of the page. Its construction rule, rather than its outline, is what is specified, because a replacement drawn to the rule sits on the same grid as the original:

1. Every stroke is a parallelogram sheared about the vertical, leaning left, at the same angle as the page's diagonal.
2. The cap height fills the canvas, with a little clearance at the top and none at the bottom.
3. Counters are cut as parallel slots at that same shear, never as curves.
4. Stroke weight is uniform, with no thick-to-thin modulation anywhere.
5. The lockup is set to the full canvas width with no side bearing, so it can be drawn edge to edge at any width.

A six-character lockup drawn to those five rules fits every layout in this specification without adjustment. A separate mark exists for the route-change curtain: two sheared blades stacked with a diagonal gap between them, the lower offset right. It is the wordmark's leading glyph pair on its own, and where the wordmark is redrawn the mark is cut from it the same way rather than designed separately. A tiling variant of the lockup exists for the foot band and the contact band, and it closes the seam between repeats rather than leaving a gap once per cycle.

### Global chrome

Six things persist across routes.

**The wordmark layer.** A fixed block at the top left, padded by the gutter of its width, and above the desktop width given an explicit height so that the navigation beside it cannot be pushed. Inside it, a link, and inside that a compensation wrapper that nudges the glyph up and slightly left, because the canvas has clearance at its top and none at its bottom so the glyph reads optically low and right in its own box. The glyph fills whichever ink the accent declaration for the wordmark names, and it changes that ink on the state curve when a route or a section changes accent, with no script touching it.

**The navigation bar.** A fixed row justified to the right, running the full width of the page with the gutter around it. Above the desktop width the row is constrained to exactly the right-hand half of the screen no matter how wide it gets, and its three controls share that half equally with their minimum widths released. Three accent-bound controls: `PROJECTS` to `/work`, `SIGNALS` to `/blog`, `CONTACT` to `/contact`. There is no home link in the bar; the wordmark is the way home, and there are no dropdowns. Below the desktop width all three are removed from the document entirely rather than hidden, rearranged or shrunk, and one square menu button replaces them wholesale.

**The mobile panel.** A fixed full-screen layer in the signal red, revealed by clipping rather than by moving, so the page behind it never shifts. Closed it is clipped to nothing and is not hittable; open it fills the window. It wipes down from its top edge, and its contents carry their own shorter travel so they settle into place a fraction behind the wipe rather than arriving with it. On closing, the panel stays hittable until the wipe finishes. Its rows run `PROJECTS`, `SIGNALS`, `CONTACT` and the two social destinations, each a flex line carrying the arrow glyph and a full-width hairline rule along its bottom edge. Below the rows sit the closing headline at a modest measure and the contact and social links as bare controls.

**The scroll marker.** The native scrollbar is suppressed and replaced by a fixed rail pinned to the right edge, running the full height, taking no pointer events, slightly wider from the tablet width up. Its slider is the signal red and its height is the ratio of the window to the document. The rail rests invisible and fades in while a scroll gesture is in progress, then fades out again; it is a fade around each gesture rather than a step.

**The footer.** Present on the home, archive and journal routes only. Its whole field is the signal red, it is promoted above the main content, and it takes a large fraction of the window's height with a fixed proportion above the desktop width. Three regions, top to bottom. A content row that is a column on a phone and a justified row above it: a main column carrying the closing headline at the largest heading step and then the newsletter field; a links column carrying the contact address and the two social destinations as bare controls; and an address column carrying the street and the postcode line in small uppercase. Then a wordmark band: below the desktop width the tiling lockup drifts sideways forever on a slow linear loop, and above it that animation is swapped for an initial keyframe that does nothing, the element returns to the normal flow, its doubled copy is hidden, and the wordmark simply spans the page. Then a legal rule: a full-width line justified to the right carrying the link reading `Imprint & Privacy`, and beside it the link reading `Terms`.

**The opening loader.** A fixed layer above everything, covering the window, made of two diagonal half-curtains, a counter and a compressed cut of the wordmark. The curtains rest on the ground colour and flash to the signal red while the page initialises. They are clipped to the two halves of the site's diagonal, and the two halves overlap by a hair: that overlap is not a mistake and must be kept, because without it a sub-pixel line of page shows through the join at fractional device pixel ratios. The counter block is centred, held slightly low, and is a justified row carrying the live percentage on the left and a fixed full-percentage figure on the right, so the two numbers converge as loading completes. Behind the counter sit two copies of the compressed wordmark, the lower held faint and the upper clipped from the left so that it fills in as progress runs. The progress value eases towards its target each frame, and the frame loop is torn down once it is nearly complete, so the last stretch is not animated: the end of any loading bar is a lie and animating it only makes people wait longer. When it completes the two halves leave sideways along the diagonal and the layer stops taking pointer events.

**The route-change curtain.** The same diagonal geometry on its own layer, in the signal red, on a tighter curve than the loader's. It rests off screen to either side and closes over the window on a route change, carrying the mark in its centre. A second, simpler panel exists in the same family for full-bleed transitions: it clips open from its bottom edge and releases a half-turn rotation instantly at the moment the wipe finishes, so the media inside flips at the seam rather than visibly rotating.

**The section label.** Every section on every route opens with the same three-part line: the asterisk in its outlined box, a gap, and one short uppercase word. The box outline, the glyph fill and the word all follow the section's accent declaration. The labels in use are `Projects`, `Services`, `Clients`, `Awards`, `Latest Signals`, `Newsletter`, `Work`, `Blog`, `Your reel`, `Sign in` and `Reels`.

### The control primitive, in full

Every part of it, because almost every interaction in the product is this one object.

- **Geometry.** A short bar the height of a line of small type, with a minimum width, laid out inline with its contents centred vertically, clipping its own overflow, and never wrapping its label: white space inside a label never becomes a line break.
- **The fill.** A layer at full size, resting below the bar and rising to cover it when the control is pointed at or is marked active, moving faster than the ink changes above it.
- **The outline.** A hairline drawn as its own layer above the fill rather than as a border, so that it survives the fill rising underneath it. It transitions its colour only.
- **The backdrop.** A frosting behind the bar. It is the only reason a near-white hairline stays legible over a bright moving picture, and the bare variant is the only thing that drops it.
- **The label.** A short uppercase run with generous letter spacing and equal padding either side, drawn twice. The second copy sits below, starts invisible, and is coloured for the filled state. On hover the resting copy travels up and fades out while the second travels up and fades in.
- **The icon well.** A square at the bar's own height, also doubled: the resting arrow travels out to the right and fades while a second arrives from the left. Its fill follows the same accent logic as the label.
- **The variants.** Default, transparent, filling with the ink, its label inverting to the ground. Accent-bound, filling with whatever ink its section declares and inverting to that declaration's opposite. Solid, which starts filled with the ink and inverts on hover. Solid on red, the same on the signal field. And bare, which drops the frosting, the fill, the outline and the minimum width and narrows its icon well; the footer and contact links are the only bare ones.
- **Where there is no pointer**, a control whose readable state is its filled state is held filled permanently, because there is no hover to reveal it.
- **Focus** thickens the outline and, on the ground, switches an accent-bound control's outline to the near-white ink. The fill does not rise on focus: rising is hover, thickening is focus, and the two must be tellable apart.

### The motion vocabulary, moment by moment

Four curve roles. **State**, symmetric and slow at both ends, for anything that goes to a state it will come back from: a hover, an open, an active, an ink change. **Arrive**, fast at the start with a long tail, for anything that arrives once: a reveal, a resize, a filter regroup, a tile expanding. **Swipe**, symmetric and tighter, reserved for the two curtains and used nowhere else, because it is what makes a route change feel unlike an interaction. **Settle**, immediate start and gentle stop, used exactly once, for the travel of a revealing paragraph. Choosing between the first two is the thing to get right: if it will come back, it is state; if it arrives once, it is arrive.

**The word reveal**, in full, because it is the signature. Every headline is split into lines, then words, then characters, on the laid-out text, without changing where it wraps. Each word carries a soft-edged window several times its own height, positioned at rest so that the word sits inside a fully transparent stretch of it: present, laid out, and invisible. When the headline becomes visible three things happen at once and all three matter. The window travels from its bottom to its top, so the soft band sweeps up through the word. The word rises half its own height. And the whole thing is delayed per line, so line one starts immediately, line two a beat later and line three a beat after that. The resting state's travel is instantaneous with a delay rather than animated, which is what makes the reverse snap once the window has faded the word out. Reversing it correctly is the difference between the reveal feeling attached to scroll and feeling like a played clip. A character layer sits underneath the same mechanism for headlines that resolve to characters, rising and fading in, with a small negative left margin compensating for the wrapper's inter-element whitespace; drop that compensation and every split headline sets one hair wider than the same copy unsplit.

**The paragraph reveal** is the same mechanism with three differences: a shorter resting transition, the travel on the settle curve while the window stays on arrive, and emphasis runs inside it carried by hue at the surrounding weight rather than by a bolder weight.

Every other moment, with what happens to it under reduced motion:

| Moment | What it is | Under reduced motion |
|---|---|---|
| Word reveal | The window sweeps up through a headline, staggered per line | The window jumps to its end, the travel to zero, no transition |
| Paragraph reveal | The same, shorter, on the settle curve | As above |
| Character reveal | Characters rise and fade in | Applied at once |
| Control fill | The block rises from below | Kept. It is a state change, not decoration |
| Control label swap | Two copies cross | Kept |
| Control ink | Colour and outline colour change on an accent change | Kept |
| Menu bars | Three bars fold into a cross | Kept |
| Mobile panel wipe | The panel clips down, contents settle behind it | The panel appears with no wipe, the inner travel dropped |
| Loader curtain | The two halves leave along the diagonal | Fades instead of travelling |
| Loader ground | Flashes to the signal red while initialising | Kept |
| Loader counter | Fades in | Kept |
| Route curtain | The two halves close and open along the diagonal | Fades |
| Transition panel | Clips open, then flips instantly at the seam | Fades, the delayed flip dropped |
| Scroll marker | Fades in on gesture start, out on gesture end | Kept |
| Scroll indicator | Fades in while the opening is in view, once | Kept |
| Journal tile grow | A flexible tile widens inside its own row | Dropped, the tile keeps its resting width |
| Journal image push | A fixed tile's picture scales behind its frame | Dropped |
| Archive tile expand | A half tile takes the full row, the longest movement here | Applied instantly |
| Archive tile label | The tile's own label fades out as it expands | Kept |
| Navigator ink | The active label and the arrow well change together | Kept |
| Wordmark ink | The lockup changes ink on an accent change | Kept |
| Footer marquee | The lockup drifts sideways forever on a phone | Stopped at its start position |
| Particle drift | The field tumbles and drifts continuously while in view | Time frozen, one static frame |
| Object rotation | The contact object turns about the vertical | Frozen at its start angle |
| Rolling label | The word inside an active control crawls with scroll | Dropped, the label sits still |
| Category bar pan | The filter row follows a finger, interpolating each frame | Kept. It follows a finger |

Only two named keyframe sets exist in the whole product: the travelling window that is the standalone form of the word reveal, and the foot band's drift. Everything else is a declared transition or a value written from scroll.

**The diagonal.** One geometry, shared by the loader, the route curtain, the not-found screen and the denied screen, authored once and reused. It runs from one side at the top of the window to the other at the bottom, with its horizontal run set as a fraction of the window's height rather than its width, which is why it keeps the same angle on a phone as on a laptop instead of going flat. Clamping stops it running off the sides on a window taller than it is wide, so on a tall phone it degrades to a straight vertical split rather than to nothing. A rule variant draws the same line as a thin band by insetting the polygon either side of it. The not-found screen uses the geometry without the clamping, because there the diagonal is meant to run off the sides.

### The scroll system

Scroll is the only real input this product has, and five values are computed from it, all in one pass, all written to the style layer.

**Interpolated position.** Wheel and trackpad input is interpolated rather than applied directly, so the document position approaches its target instead of jumping to it, and every scroll-derived value below is computed against that interpolated position rather than against the raw one. Native scroll stays the source of truth for anchors, keyboard paging and assistive technology. Three states are exposed on the document root: the interpolation layer is mounted; a gesture is in progress; interpolation is actively running. The scroll marker is bound to the middle one, which is what fades it in on gesture start and out on gesture end. If the interpolation layer has not mounted shortly after first paint, native overflow is released, a marker is set on the root, and every scroll-derived value falls back to reading native scroll position: the page then works without interpolation and nothing is frozen. A page that scrolls while everything attached to scrolling is stuck is broken in a confusing way; this is the friendlier failure.

**The depth value, which is the parallax.** Every media surface moves against the page at one factor of scroll speed, and it is the same factor for every media surface in the product. It is computed from the element's own distance from the centre of the window as a proportion of half the window, written as a percentage, and consumed in two ways: as a vertical travel on a parallax wrapper inset to zero inside the clipping box and the same size as it, and as a shift of the visible crop on a thumbnail, which moves what is seen rather than moving the box. Because the wrapper is always the same size as its clipping parent and the parent clips, the media is always over-scanned and the fraction never reveals an edge. Much more than this fraction and the page starts to feel like it is sliding apart.

**The project-run ratio.** The home route's four-project run and its navigator are driven by one ratio and not by a set of thresholds: the run wrapper's own position relative to its own height. From that one number come the navigator's vertical travel, each thumbnail's reveal, and the active index. The navigator's label column and its thumbnail column both take the same single travel, so a single percentage scrolls both in lockstep and the label always agrees with the thumbnail. **The label, the thumbnail and the destination must be driven from one computed index.** Three separate listeners drift by one item at speed, and the panel starts sending people to the wrong project.

**The rolling label.** The active control's label crawls continuously as the page scrolls, so a filled control does not look frozen on a long route. Two copies of the same word chase each other exactly one line apart, and the offset wraps, so the loop has no seam. It completes one cycle for a small fraction of the document scrolled.

**The loading progress value.** Not scroll-driven but written the same way: a value that eases towards its target every frame, consumed by the clipped wordmark copy as a clip inset from the left and printed by the counter as an integer.

Which surfaces are scrubbed, meaning a continuous function of position that reverses on scroll-up, and which are triggered, meaning a state set once when a threshold is crossed:

| Route | Surface | Mechanism |
|---|---|---|
| Home | Project item wrapper | Scrubbed depth |
| Home | Navigator label stack and thumbnail stack | Scrubbed from the run ratio |
| Home | Headline words | Triggered, then transitioned |
| Home | Opening media wrapper | Triggered |
| Home | Scroll indicator | Triggered, once |
| Home, archive, journal | Scroll marker slider | Scrubbed |
| Home, archive, journal | Scroll marker rail | Triggered on gesture |
| Archive | Tile media wrapper | Scrubbed depth, the heaviest surface in the product |
| Journal | Headline words | Triggered |
| Contact | Wordmark band | Time-driven, not scroll-driven |
| Every route | Loader wordmark | Progress-driven |
| Not found | Numeral columns | Time-driven, not scroll-driven |

### The real-time layers

Two independent surfaces on two routes, sharing one set of rules. Neither carries information. Both exist to make a flat page feel as though it has a room behind it.

**The particle field**, on the home route. A fixed canvas pinned to the window at the very bottom of the stack, with the document scrolling over it. It reads the pointer and never captures it. It draws one small irregular faceted form many times over, fewer instances on a narrow screen, placed evenly over a sphere by a spiral distribution rather than by naive random spherical coordinates, which clump at the poles. Each instance carries its own starting orientation, its own angular velocity per axis, its own size variation and its own drift speed. The whole field drifts sideways and wraps back round, and each instance is pushed forward along that wrap by its own starting rotation, so the field is already fully populated on the first frame instead of marching in from one edge. The slowest instance crosses in a couple of minutes and the fastest in a few seconds, and that spread is what stops the field reading as a single sheet moving sideways.

Its lighting is hand-written rather than physical, and three properties carry the whole look. The forms are matte and colourless, a neutral grey. **The only light in the scene is a single pointer-driven lamp in the signal red** and falls off completely over a short radius, so forms near the cursor catch a red edge and everything further away stays nearly black; a cold overhead fill at a quarter strength exists only so that the unlit side is not pure black, and it makes faces pointing up read very slightly warm and faces pointing down very slightly cold. Every silhouette edge is darkened rather than rim-lit, which is what stops a field of small bright objects turning into noise. **Each form carries two separate speculars: a wide soft sheen and a small hard hot spot inside it.** Collapsing them into one produces a plastic highlight.

Two behaviours make the difference between expensive and cheap. **The lamp lags the pointer**, interpolating a small fraction of the remaining distance each frame, so it is always visibly a beat behind and reads as a heavy light being carried rather than a dot glued to the cursor; making it arrive instantly collapses the effect. And **the field is bound to the manifesto block alone**: its opacity eases towards one while that block is meaningfully in view and towards zero when it is not, and below a very small opacity the draw is skipped entirely rather than merely made transparent. Off the manifesto, the field is not drawn at all.

The five settled values that shape this lighting are softer than the constructed defaults a first draft reaches for: a lower shininess, a lower light intensity, a modest specular strength, a short light radius, and the signal red as the light colour. A small wireframe marker sits at the lamp's position for development and must not be visible in the shipped product.

**The object layer**, on the contact route. A fixed canvas above the layout taking no pointer events, so the copy underneath stays selectable. One dark, glossy, fully metallic object at low roughness turns slowly about the vertical only, at a constant rotation against elapsed time in the negated direction, and the environment it reflects counter-rotates at the same rate, which makes the highlights slide across the surface at twice the object's rate and reads as polished rather than as a rotating model. The object is recentred on load, so it turns about its own middle rather than about its origin. Its parts are identified by name prefix rather than by index. It has its own single width threshold, separate from the layout's: above it the object sits in the right-hand third of the visible frame, clear of both the headline and the contact block, at a larger scale; below it the object centres, drops slightly, and the copy sits over it.

Both surfaces are transparent-backed, antialiased, ask for the high-performance device, and **set their frame loop to never render while the document is hidden**. Both attach a performance monitor that raises resolution when frame timings improve and reduces it when they decline, with a single allowed oscillation before it settles so a device sitting exactly at the boundary does not flap between two resolutions.

### The home route, block by block

Nine blocks in one continuous take, and the whole route is laid out against the computed viewport height so the proportions survive a collapsing phone chrome.

1. **The opening.** Four superimposed fixed layers inside one full-height block. Nothing here scrolls; the document scrolls past it. A media layer fills the window and carries a still first frame behind it. Over it, the wordmark laid edge to edge across the full page width less its gutters, vertically centred, filled in the signal red. Over that, at the bottom left, the headline in two authored lines, taking no pointer events. And at the bottom right, the scroll indicator. The media layer is the only element in the product that scales: as the route scrolls past, it swells slightly and fades out, both as a state set once rather than as a continuous function, and it holds that end state. That swell is what makes the opening read as pushed through rather than faded out, and it is what hides the seam where the manifesto begins. A secondary opening style exists for a route carrying a line rather than a headline: a smaller uppercase centred run.
2. **The scroll indicator.** Fixed at the bottom right, taking no pointer events, resting invisible and fading to full while the opening is in view. It appears once, at the top, and never returns.
3. **The manifesto.** A block two screens tall on the signal red, taking no pointer events, holding one centred sentence at the largest display step with a generous measure, pinned inside a fixed centred wrapper so that the sentence holds still for the whole two screens while the document travels under it. Two screens of dwell is deliberate: it is long enough that a visitor stops to read, and the field behind it drifts slowly enough that stopping is when it looks best. This block is the particle field's only trigger. The sentence is split to words and revealed.
4. **The project run.** Four full-screen project items in a wrapping row separated by the media gap, inside a clipping block. Each item is full width and a full screen tall, holding a depth wrapper the same size as the item, a muted looping media element cropped to fill inside that, and a link covering the whole item.
5. **The navigator.** A fixed overlay across the window taking no pointer events, holding one panel that takes them back. The panel is frosted, hairline-outlined, and takes the rising fill on hover. It has three cells: a square thumbnail well holding a column of square crops, a label column holding a column of rows, and a square arrow well. The thumbnail column and the label column carry the same single travel so they move in lockstep. The label column is masked so that rows entering and leaving the window fade rather than clip. Each label row carries the project title above its practice field. On hover the label ink, the arrow well's ground and the arrow's fill all change together. When the run is in its red state the panel's ground is the signal red, the labels stay near-white, and both the hover label and the arrow become red against a near-white fill. **Only the active row's link takes pointer events**; the other three take none. On a phone the overlay aligns to the bottom of the screen rather than to its centre.
6. **The practice fields.** Four numbered fields in the signal red on the page ground, in a wrapping row with a generous block rhythm above and below. Each carries a two-digit numeral, a two-line title at a mid heading step, and a short body at the smallest paragraph step held to a narrow measure. On a phone they stack one per row with a translucent red divider under each; on a tablet, two per row with the divider; above the desktop width, four across with no divider at all. The divider disappearing at the widest width is the tell that this row is designed as four columns and degrades to a stacked list rather than the other way round. A small square icon well exists in each field, filled in the accent with a glyph in the opposite ink, and it is left unpopulated unless a field needs a mark. The numerals are set in the near-white ink on the ground, not in red, because at label size red on the ground is too dim.
7. **The client wall.** A grid of twelve client wordmarks in the signal red, taking no pointer events anywhere in the block, three columns on a phone, four on a tablet, six above the desktop width, each cell centring its mark. Taking no pointer events is correct and deliberate: these are proof, not navigation. Each mark carries its owner's name as its accessible name, because they are content rather than decoration.
8. **The awards wall.** The same construction with three differences: two columns on a phone rather than three, a larger grid margin, and a caption under every cell. A caption is two authored lines, a count and a category, and it must not be allowed to reflow, because the two lines are a pair. It is positioned just below its cell and is centred.
9. **The latest entries.** A header row carrying the section label on the left and a control on the right, then the three most recent journal tiles three across. Above the desktop width the container takes a fixed proportion of its own width with the grid pinned to its bottom, so that three square tiles do not set the band's height. Between the tablet and desktop widths the third grid position is hidden outright, because two columns of three tiles leaves an orphan.

The footer sits directly under the last tile with no gap and no separator: the media gap rhythm does not apply between a section and the footer.

### The archive route

A short heading block rather than a full-screen one: the section label reading `Work`, the headline `Our Portfolio` at a large heading step, and the filter row directly under it, overlapping upward into the heading block's bottom padding.

**The filter row.** A flex line of controls at the control height, each taking an equal share of the width. Below the tablet width the minimum width is released and the row is absolutely positioned at its container's top left so it can overflow the screen horizontally, where it becomes draggable: the row follows a horizontal pan gesture, interpolating towards its clamped target each frame, and it can be dragged a little past its start and springs back, because the interpolation always chases the clamped target. The active control carries the active modifier, holding its fill permanently, so the current filter reads as a solid block rather than as an outline.

**The mosaic.** A wrapping row separated by the media gap. Above the desktop width a tile is either full width or half width and a full screen tall; below it every tile is full width at a taller-than-wide proportion, and the media inside takes a portrait crop centred inside that tile rather than being letterboxed. The mixed widths are doing real work: a grid of identical squares makes fifteen projects look like a catalogue, and a mixed rhythm makes them look like a body of work.

**The tile.** An outer box holding an inner absolutely positioned layer padded by the gutter, aligned to the bottom left, clipping its overflow; inside that a depth wrapper, a muted looping media element cropped to fill, a control carrying the project title at the bottom left, an `Add` control at the top right, and a link covering the whole tile. Project titles honour their authored line breaks.

**The expand.** A half tile can take the full row, and it is the one place in the product where a box changes size. The tile is promoted above its neighbours, **its inner layer** takes double width, its partner in the pair slides aside, and its own label control fades out because a control stretched across a doubled picture reads as a mistake. Both the width and the slide run on the longest movement anywhere in the product. **The thing that grows must be a layer inside the tile, never the tile itself**: the outer keeps its layout width so the tiles beside and below it do not reflow. Growing the outer jumps the whole mosaic. The expanded state is reachable and reversible by keyboard as well as by pointer.

**The closing block.** Below the mosaic, one full screen: a headline held to a wide measure, a control, a media layer cropped to fill, a feature graphic pinned to the bottom right and deliberately over-scanned so it bleeds off the corner rather than sitting inside the block, and a wash rising from the bottom edge in the signal red, blended so that the red lifts out of the picture's shadows rather than being laid on top of it. That wash is the only blend in the whole product, and it is why the block reads as lit from below rather than tinted. Then the footer.

### The project detail route

The main block sits promoted on the page ground and the route carries a full screen of trailing margin, which is not padding: it is the gap through which the fixed next-project layer shows.

**The opening.** A full-height clipped block aligned to its bottom, with the media filling it, and the title at the largest heading step inside a padded inner. A half-opacity copy of the same string sits at the bottom left as a layout instrument, so the title's reveal can be sized against laid-out text without the split wrapper affecting the measurement. It is hidden entirely from assistive technology.

**The introduction.** A justified column that becomes a row above the desktop width with the text taking half the width. The title is held to a wide measure. The practice fields sit beside it as a row of controls that release their minimum width and share the row on a phone. The body is revealed as a paragraph. Emphasis runs inside it take the hotter red at the surrounding weight, never at a bolder one: emphasis carried by hue alone lifts a phrase, and hue plus weight shouts. This is the only place the hotter red appears.

**The body.** A wrapping row separated by the media gap holding media blocks at four widths: full, half, third and quarter, each subtracting its own share of the gap. Every media block is set to a wide cinematic proportion and cropped to fill. A wider text block is available for long passages between media, with an inner that takes half the width above the desktop width and a minimum measure floor, because a half-width measure on a narrow laptop otherwise drops below readable. A horizontal slider is available for a run of items wider than the screen, the first and last flush with the gutter. A video player exists at the same proportion, with a portrait variant that takes the full height and auto width, a click area covering it entirely, and a thin progress rail along its bottom edge whose inner is filled in the accent and grows from its left edge; **progress is expressed as a transform on that inner, never as a width recomputed per frame**.

**The credits.** A column that becomes a row above the desktop width, in two halves: a label and the table. Each row is a justified line carrying the role on the left at the lighter weight and the name on the right, both uppercase, with a rule under it drawn thinner than a hairline in the translucent ink. That sub-hairline rule is the product's only sub-pixel measurement and it is intentional: at a full hairline it reads as a boxed table and at half it reads as a ruled sheet, which is the difference between a spreadsheet and a title card.

**The handover.** A fixed full-height layer pinned to the top left holding the next project's media at full size, with its title and a control at the bottom. It is fixed, and the route above it carries a full screen of trailing margin, so it is not a section that scrolls up into view: it is a layer that has been there all along, revealed as the main block scrolls off it. Reaching the bottom of a project therefore lands the visitor already inside the next one, with no button anywhere.

### The journal index and entry

The index is the archive's heading block and filter row with the label reading `Blog`, the headline `Signals and Field Notes` split across two authored lines, and four filter controls. The grid is a wrapping row separated by the media gap holding one tile shape at three densities: one column on a phone, two on a tablet, three above the desktop width. Note that the two-column basis subtracts a little more of the gap than the arithmetic suggests, because these tiles carry an automatic top margin and a basis rather than a computed width, and the extra absorbs the rounding that the automatic margin introduces.

**The tile** is square, aligned to its bottom, clipping its overflow, padded by the gutter, with the media filling it, the date absolutely positioned at its top right in small uppercase, a control carrying the title at the bottom left, and a link covering the whole tile.

**Two hover behaviours, and which applies depends on whether the tile is allowed to change size.** Above the desktop width a tile grows by a small fraction inside its own row and its row-mates give up exactly that space, so the row breathes without anything moving to another line. In every other case the media inside scales by the same small fraction behind a frame that stays put. They are the same fraction expressed in two different places, and the choice is not cosmetic: a wide row can afford to redistribute and a narrow one cannot, so the growth is pushed into the picture instead. Applying both at once makes the tile jump. **Nothing a tile does on hover may reflow the rows below it.**

**The entry** is a heading block carrying the section label, the title at the largest heading step and the date; then a lead image at the wide cinematic proportion; then the body. The body is the only measured reading column in the product: headings and paragraphs held to a comfortable measure, centred with automatic side margins, **set visibly looser than the same steps anywhere else on the site**. Everywhere else the type is packed tight because it is display; here it is set loose because somebody is reading it, and somebody will eventually try to unify them for consistency. They should not. Links inside the body are near-white with a hairline rule under them rather than an underline, and they fade slightly on hover. Media inside the body uses the project detail's four widths and the same gap, so a full-width image inside an entry and inside a case study are the same component; a media block nested inside another takes no vertical rhythm of its own.

**Related entries** sit in a band whose container takes a fixed proportion of its own width above the desktop width with the grid pinned to its bottom, so the band's height is decided by the design rather than by whatever the pictures happen to be. Between the tablet and desktop widths its third position is hidden.

### The contact route

One screen. No form, no scroll, no footer. A column justified between its top and its bottom, on the page ground, with the accent declared red so every control on the route is red. The headline sits at the top at the largest heading step with a control directly beneath it. The contact block sits at the bottom: a narrow column in small uppercase holding the address `contact@vesper.works` as a bare control with the outbound arrow, then the two address lines set upright rather than italic, then the two social destinations as bare controls. Setting the address block upright is deliberate: an address element italicises by default in most engines, and italic does not exist in this type system.

**Nothing on this route is vertically centred.** Everything is pushed to the top or the bottom and the gap between takes up the slack, which is why the layout holds on a short laptop and a tall phone without a single adjustment on the vertical axis.

**The band.** A fixed band taking no pointer events, carrying the tiling wordmark, laid across the screen on the site's diagonal. It is shorter and unrotated and centred on a phone, and taller and rotated to the site's angle and pushed right above the desktop width. Inside it, a strip of repeated wordmarks at full band height, each overlapping its neighbour by a hair so the joins close, translating continuously and linearly on the horizontal axis and wrapping by one repeat width, at the same rate as the foot band. It is time-driven and not scroll-driven. **Each wordmark in the strip is drawn as a red block with the letterforms knocked out of it rather than as red letters**, so the page ground shows through the counters and the band reads as a strip of tape rather than as lettering.

Over the top right of it, the rotating object, above the layout and taking no pointer events.

### The legal and terms routes

A short heading block carrying the title, then one measured column, then a generous bottom rhythm. The column is held to a comfortable measure, **left-aligned against the gutter rather than centred**, which is the same position every other route's copy starts from. Its whole content honours the source text's own line breaks, because legal copy arrives pasted out of a document with authored breaks and this is what stops those breaks collapsing into one wall. Headings step down in size with a clear rhythm above them. Links are near-white. Paragraphs are set with both edges flush, which is the only justified text in the product; justified text without word-breaking produces rivers, so if word-breaking is not available for the content language, set it ragged on the right instead.

Both routes use the same construction. The imprint and privacy route states what the product stores about a client, what it never records, and how long a session and a reset link last. The terms route states the terms of use and is linked from the sign-up form as well as from the footer.

### The not-found screen and the denied screen

The not-found screen is not an error page. It is a designed screen, and it is where the diagonal is stated most plainly.

The numerals fill most of the screen in the signal red on the page ground. Two absolutely positioned wrappers each cover the window and each is clipped to one side of the diagonal, without the clamping the curtains use, because here the diagonal is meant to run off the sides on a tall window. Each wrapper holds its own copy of a column of two stacked numeral sets, and each column translates vertically, linearly, wrapping, from its start to half its own height. The two columns run at the same rate in opposite directions. Because the two copies are clipped to opposite sides of the diagonal, **the numerals shear apart along that line**: the upper-left half slides against the lower-right half and the numerals are continuously being cut and re-registered. Over both sits the diagonal drawn as a thin band in the signal red, taking no pointer events, and it pulses faintly rather than holding still. At the bottom centre sits a block with the line `Page not found` above a control reading `back home` pointing at `/`, and that line is set in the near-white ink rather than in red, because it is small text on the ground. The wordmark and the navigation are present and unchanged; the footer is not. The drift is time-driven: the page is not scrolling while it happens.

The denied screen is the same screen with the numerals dropped and the diagonal kept, which is the whole design decision: the visitor should recognise the shape instantly and read immediately that this is a different refusal. In place of the numerals, one line at the largest display step in the signal red, centred, held to a generous measure. The rule stops pulsing and sits static, because a pulse reads as playful and a permission refusal should not. The way back reads `Not your reel` above a control reading `back to yours` pointing at `/reel`.

### The client area

Every surface here is built from parts that already exist. It adds no colour, no curve, no spacing step, no type step and no icon. That constraint is the reason it is worth trusting: a client area that introduced its own greys and its own easing would be a second product wearing the first one's clothes.

**The sign-in surface.** Built to the contact route's shape, because it is the only single-screen layout the system already has: a full-height column justified between its top and its bottom, with the accent declared red so every control on the route is red. The top block carries the section label reading `Sign in` and a two-line headline; the bottom block carries the form in a column the width of the footer's main column. The form is the newsletter field's construction stacked, rows separated by the media gap, with a final row for the submit. Its four modes are carried in the query and switch without a navigation: sign in; create, with a third field for a display name, a submit reading `Create account`, and the terms link beside it; reset, with one field and a submit reading `Send reset link`; and set, with two password fields and a submit reading `Set password`. A bare control below the form toggles between sign in and create, and another reads `Forgot password`. A password field carries a bare control at its right reading `Show` that toggles the field's type; it is not an icon, because this type system has no eye glyph and inventing one would break the icon set.

**The reel route.** The archive's short heading block with the section label reading `Your reel` and the reel's own title as the headline, edited in place: the field's panel ground appears only while it is focused and there is no visible box at rest. Then the item list, then the brief, then the send control.

**An item row** is built as the project navigator's label row: a justified flex line at the navigator's own row height, in small uppercase, held inside a fixed-height window, with a square thumbnail well on the left and a square control well on the right, and the media gap between rows. The thumbnail is the project's square crop cropped to fill. The title block carries the project title above its practice field. The note sits on its own line below the title block at the smallest paragraph step. The handle is a small box carrying the asterisk glyph and is the drag affordance; the remove control is a small box carrying the arrow glyph rotated a half turn. The row's ground is transparent with the standard hairline outline drawn as its own layer, and it takes the standard rising fill on hover.

**Reordering.** Dragging by the handle lifts the dragged row above its neighbours and the rows it passes translate by one row height. On touch the handle needs a short press before the drag begins, so a drag does not steal a scroll. From the keyboard, focusing the handle and pressing an arrow moves the row one position per press and announces it. **Per row, the controls come before the content in the document**, so a keyboard user reordering a list never has to tab through text fields to reach the next handle.

**The fields.** The title is the second heading step, edited in place. The note is one line at the smallest paragraph step on the panel ground with the standard side padding, taking the full row width. The brief is the same step on the panel ground, several rows tall, resizable on the vertical axis only. All three write on blur or after a short idle, whichever is first, and their counters stay hidden until the limit is close.

**The send control** is a solid accent-bound control the full width of the brief column at the bottom of the route. Ready it reads `Send to the studio`; pending, its word becomes `...` and it is disabled; sent, it is replaced by the sent surface. The sent surface is the newsletter field's success block scaled up: a block on the panel ground at the control height in small uppercase reading `Sent`, with the send date beside it and a bare control reading `Reopen`. **Sending fires the route-change curtain without a navigation.** That is the one place the curtain is used for something other than a route change, and it is deliberate: sending a reel is the only moment in the product that deserves to feel like a scene change.

**The studio queue.** One row per reel, built as the latest-entries header row repeated: a section label carrying the client's display name, the reel's title at the smallest paragraph step, the item count, the sent date, and a control reading `Open`. Rows are separated by the media gap rather than by rules. Above the desktop width a row is a justified line at the navigator's row height; below it the row stacks and the date moves under the title.

**The answered notice** is the newsletter success block at the full column width on the panel ground, in small uppercase, reading `The studio has your reel`, sitting above the item list. It is a state and not an alert, so it does not dismiss.

**The notification strip.** Fixed, full width, at the control height, at the bottom of the window, above everything except the curtains. Its ground is the signal red for a failure and the panel ink for an acknowledgement, and its text is small uppercase in the near-white ink. It enters and leaves by the mobile panel's wipe, inverted, from the bottom edge. It dwells briefly and then leaves. One at a time: a second message replaces the first without re-animating the strip. It may carry one optional bare control at its right, for `Retry`. **It never becomes a corner card at any width**, because it shares its geometry with the offline bar and the two must be indistinguishable in shape. The offline bar is the same strip with its own copy, and it is the one surface in the product that appears without being asked for, which is exactly why it is a strip and not a dialog.

**The skeleton** is a block at exactly the size of the element it stands in for, on the panel ground, square-cornered like everything else, with a single sweep of the word reveal's own soft window travelling across its width, linearly, repeating. Under reduced motion the sweep is dropped and the block sits flat.

**The empty surface** is a centred column: the asterisk in its outlined box in the accent, one line of small uppercase below it, and, where there is one to offer, a control below that.

### Responsive behaviour, width by width

| Surface | Phone | Tablet | Desktop and wider |
|---|---|---|---|
| Gutter | Smallest fixed step | Larger fixed step | Proportional to the viewport |
| Navigation | Menu button only | Menu button only | Three bars filling the right half |
| Wordmark | Larger | Larger | Smaller, with the block's height fixed |
| Footer content | Column | Row | Justified row |
| Footer wordmark | Drifting | Drifting | Static, spanning the page |
| Archive tile | Full width, taller than wide | Same | Full or half, a full screen tall |
| Archive tile media | Portrait crop, centred | Portrait crop | Fills the tile |
| Journal tile | One column | Two | Three |
| Journal tile hover | Media scales | Media scales | Tile grows within its row |
| Client wall | Three columns | Four | Six |
| Awards wall | Two columns | Four | Four |
| Award caption | Smaller | Smaller | Larger |
| Practice fields | One per row, divider | Two per row, divider | Four across, no divider |
| Project navigator | Bottom of the screen | Centred | Centred, one step taller |
| Navigator label | Smaller | Smaller | Larger |
| Category bar | Absolute, pannable, overflowing | In flow | In flow |
| Contact band | Shorter, unrotated, centred | Shorter | Taller, rotated, pushed right |
| Contact object | Centred, smaller | Centred | Right third, larger |
| Project introduction | Column | Column | Row, text at half width |
| Credit table | Column, first row ruled above | Column | Row, halves at half width |
| Journal body | Full width less gutters | Same | Held to its measure, centred |
| Related entries | Rows stack | Third position hidden | Three across in a fixed-proportion band |
| Sign-in block | Full width less gutters | Same | The footer main column's width, left-aligned |
| Sign-in rows | Stacked | Stacked | Stacked. They never become a row: an address beside a password reads as a search bar |
| Sign-in headline | Second heading step | Second | Largest heading step |
| Reel row | Stacked into three lines | Stacked | Justified on one line at the navigator's row height |
| Reel row thumbnail | Square at the navigator's smaller size | Same | Square at the navigator's larger size |
| Reel row handle | Absent; reordering is by the arrow controls | Absent | Present, drag enabled |
| Reel row note | Full row width below the title | Full width | Inline, after the title block |
| Brief field | Full width, fewer rows | More rows | More rows, capped at the main column |
| Send control | Full width | Full width | The main column's width |
| Studio queue row | Stacked, date under the title | Stacked | Justified on one line |
| Notification strip | Full width strip | Same | Same |
| Offline bar | As the strip | Same | Same |
| Empty surface | Centred in what it replaces | Same | Same |
| Skeleton | The exact size of its target | Same | Same |
| Denied screen | The split, diagonal running off the sides | Same | Same |
| Add control on a tile | Permanently filled | Filled | Outlined, filling on hover |

Two of those rows are the ones a build gets wrong. The reel row's handle is absent below the desktop width, because a drag handle on a touch device competes with the page scroll, and on a stacked three-line row it has no obvious grab point; reordering there falls back to the arrow controls, which are the keyboard path anyway. And the notification strip never becomes a corner card, for the reason above.

The product has no orientation queries and needs none, because every full-height surface is measured against the computed height, which is rewritten on every resize including an orientation change. The one real risk is a landscape phone, which is very short: there the opening's wordmark at full width and the two-line headline below it can collide, so below a short viewport height the headline drops a step and the wordmark keeps its width.

### Focus order, per route

Focus order is document order everywhere, and that sentence is only useful if the document order is stated, because four routes carry fixed overlays whose position in the markup is not where they appear on screen.

| Route | Order |
|---|---|
| `/` | Skip control, wordmark, three navigation bars, opening headline, the four project links in run order, **then** the navigator's active link, practice field bodies, client marks, award marks, latest entry tiles, footer headline, newsletter field, newsletter submit, footer links, legal link, terms link |
| `/work` | Skip control, wordmark, navigation, headline, five filter controls in order, then per tile the `Add` control and the tile link in mosaic order, closing control, footer as above |
| `/work/{slug}` | Skip control, wordmark, navigation, opening title, `Add` control, practice field controls, body media links, next-project link, footer as above |
| `/blog` | Skip control, wordmark, navigation, headline, four filter controls, ten tile links in grid order, footer as above |
| `/blog/{slug}` | Skip control, wordmark, navigation, title, body links in reading order, related entry links, footer as above |
| `/contact` | Skip control, wordmark, navigation, headline control, address, two social links. The object layer is not in the order at all |
| `/legal/...` | Skip control, wordmark, navigation, body links in reading order |
| Not found | Skip control, wordmark, navigation, return control |
| `/sign-in` | Skip control, wordmark, navigation, each field in visual order, the reveal control after its password field, submit, terms link, mode toggle, forgot control |
| `/reel` | Skip control, wordmark, navigation, sign out, title field, then per row: handle, remove, note; then brief, then send |
| `/studio/reels` | Skip control, wordmark, navigation, sign out, each row's open control in queue order |
| Denied | Skip control, wordmark, navigation, return control |

Three rules that table encodes. The home route's navigator comes **after** the project run in the document, because it is a fixed overlay drawn over the run, and if it preceded the run in markup then tabbing from the second project would jump into the overlay and back out again. A fixed overlay that carries no action is not in the order at all: the contact object, the particle field, both curtains, the loader and the scroll marker are all removed from it. And per row, controls come before content.

The keyboard path through the whole workflow, as one sequence: tab to a tile's `Add` control and activate it; land on the sign-in surface with focus in its first field; tab through the fields and submit; land back on `/work` with focus restored to the tile that was pressed; tab to two more `Add` controls; navigate to `/reel`; tab to the first row's handle; arrow up or down to reorder, with each move announced; tab to the note field and type; tab to the brief and type; tab to send and activate. No step in that sequence requires a pointer, and no step requires leaving and re-entering a region.

### Module and component architecture: build these once

A module owns a layout. It does not own a colour, a curve, a duration or a type size: those come from the token layer, and any module that declares one of its own has become a second design system. Six components carry the product, and building them before any route is the difference between one scroll listener and nine.

| Component | Used by |
|---|---|
| The control | Navigation, filter row, every tile label, every `Add`, every form submit, mobile panel rows, every reel control |
| The section label | Every section on every route |
| The split text | Every headline and every revealing paragraph |
| The media frame | Home run, archive tile, journal tile, project body, related entries, reel thumbnails |
| The diagonal | Loader, route curtain, not-found, denied |
| The grid | Home run, archive mosaic, journal grid, project body, related entries |

The media frame is the least obvious and the most valuable: a clipping box, an over-sized child carrying the scroll-written depth value, and a media element cropped to fill. Every moving picture in the product is that one component at a different proportion.

**And do not build these.** No second grid system: one wrapping row with one gap covers every grid here. No modal or dialog layer: nothing in this product opens a dialog, the mobile panel is a route-level surface, the notification strip is not modal, and no confirmation is a dialog. No queue of notifications: the strip is single-slot on purpose. No rich text editor. No spinner component. No icon component library: six glyphs, all inline. No theme switcher: there is one theme and its inversion is the accent declaration. Every one of those is a thing a team adds by reflex, and every one of them would make this a different product.

### Copy

Every string a visitor reads. A break inside a quoted string is authored and must be reproduced, because headings honour their own breaks rather than reflowing.

**Section labels.** `Projects` above the project run. `Services` above the practice fields. `Clients`. `Awards`. `Latest Signals`. `Newsletter` above the footer field. `Work` on the archive. `Blog` on the journal, which reads `Blog` while the navigation reads `SIGNALS`; keep both. `Your reel`. `Sign in`. `Reels`.

**Home.** Opening headline, two authored lines: `Creative Innovation` then `and Digital Futures`. Manifesto, one sentence: `The future of digital belongs to brands that are felt, explored and remembered.` Project run headline `Our Portfolio`, with a control reading `all projects`. Practice headline `Fields of Practice`. The four fields, each a two-line title and a body:

| Numeral | Title, two authored lines | Body |
|---|---|---|
| `01` | `Strategy` / `Brand Identity` | `We define your foundation through positioning, narrative, and visual identity built to scale.` |
| `02` | `Website` / `Digital Experience` | `We translate that foundation into digital experiences that bring your brand to life online.` |
| `03` | `Visuals` / `CGI Animation` | `We craft visual worlds through cinematic CGI and motion systems, giving your brand dimension.` |
| `04` | `Spatial` / `Extended Reality` | `We extend your identity into physical spaces through AR/VR, and real-time environments.` |

The four awards and their two-line captions: `Tessera Prize` reading `1x Nominee` then `2x Honoree`; `Fold Awards` reading `4x Winner` then `2x Shortlisted`; `The Grid` reading `6x Site of the Day` then `2x Studio of the Year Nominee`; and `Nocturne` reading `11x Site of the Day`. The latest-entries control reads `All Signals`.

The four home-run projects and their subtitles: `Nightshift` / `Digital Experience`, `Ferrous` / `Digital Identity`, `Kiln House` / `Digital Twin AR/VR`, `Second Skin` / `Augmented Fashion`. The twelve client marks, in wall order: `Aldermere`, `Brightwork`, `Corvid`, `Dunlin Mills`, `Everline`, `Fathom`, `Grayforge`, `Hollow Bay`, `Ironvale`, `Juniper Rail`, `Keelson`, `Lowfield`.

**Archive.** Headline `Our Portfolio`. Filters in order: `All`, `Brand Identity`, `Website`, `Visuals`, `Extended Reality`. The fifteen projects in mosaic order, each with its subtitle and its practice fields:

| Title | Slug | Subtitle | Practice fields |
|---|---|---|---|
| `Nightshift` | `nightshift` | `Digital Experience` | Website |
| `Ferrous` | `ferrous` | `Digital Identity` | Brand Identity |
| `Kiln House` | `kiln-house` | `Digital Twin AR/VR` | Extended Reality |
| `Second Skin` | `second-skin` | `Augmented Fashion` | Extended Reality, Visuals |
| `Cold Open` | `cold-open` | `Title Sequence` | Visuals |
| `Marrow` | `marrow` | `Brand System` | Brand Identity |
| `Halyard` | `halyard` | `Product Site` | Website |
| `Tessellate` | `tessellate` | `Motion Identity` | Brand Identity, Visuals |
| `Drylands` | `drylands` | `Campaign Film` | Visuals |
| `Pale Horse` | `pale-horse` | `Launch Site` | Website |
| `Foundry Row` | `foundry-row` | `Spatial Showroom` | Extended Reality |
| `Oxbow` | `oxbow` | `Identity and Site` | Brand Identity, Website |
| `Signal Box` | `signal-box` | `Interactive Install` | Extended Reality |
| `Quiet Mile` | `quiet-mile` | `Brand Film` | Visuals |
| `Lantern` | `lantern` | `Digital Flagship` | Website |

The first four of the fifteen are the same four the home route runs: the home route is a selection from the archive, not a separate set.

**Journal.** Headline, two authored lines: `Signals` then `and Field Notes`. Filters in order: `All`, `Editorial`, `Events`, `News`. The ten entries, newest first, with their kinds and dates:

| Title | Slug | Kind | Date |
|---|---|---|---|
| `The Long Take` | `the-long-take` | `editorial` | `13/05/26` |
| `Notes From The Floor` | `notes-from-the-floor` | `events` | `28/04/26` |
| `Against The Grid` | `against-the-grid` | `editorial` | `22/01/26` |
| `A Room With No Corners` | `a-room-with-no-corners` | `editorial` | `11/09/25` |
| `Studio Of The Year` | `studio-of-the-year` | `news` | `05/09/25` |
| `Six Weeks In Ceramic` | `six-weeks-in-ceramic` | `editorial` | `15/05/25` |
| `Open House` | `open-house` | `events` | `11/10/24` |
| `Ferrous Goes Live` | `ferrous-goes-live` | `news` | `02/07/24` |
| `Light As Material` | `light-as-material` | `editorial` | `23/11/23` |
| `The First Reel` | `the-first-reel` | `news` | `17/10/23` |

**The shared closing block**, on the home footer, the archive's closing block, the journal footer and the contact route. The same two strings in all four places, and that repetition is the product's only refrain: the headline `The best projects start with a good conversation.` above a control reading `Let's talk`. Do not vary it per page. The archive's closing block carries its own headline instead: `Let's shape what's next in digital together.` above the same control.

**Contact.** The address `contact@vesper.works`, the street line `14 Kiln Street`, the postcode line `E2 8HD London`, and the two social destinations `Instagram` and `Behance`.

**Footer.** Newsletter label `Newsletter`. Placeholder `your@email.com`. Control `Subscribe`, becoming `...` while pending. Success `Thanks for subscribing`. Default failure `Something went wrong`. Legal links `Imprint & Privacy` and `Terms`.

**Not found.** The line `Page not found` above a control reading `back home`, quoted exactly including the lower-case control, which renders uppercase through the label's own transform.

**Client area.** Sign in: headline `Sign in` then `to your reel`, control `Sign in`, mode toggle `Create an account`, and `Forgot password`. Create: headline `Start` then `your reel`, control `Create account`. Reset: headline `Reset` then `your password`, control `Send reset link`, success `Check your email`. Set password: control `Set password`. Password reveal control `Show`. Reel: default title `Untitled reel`, brief label `Brief`, brief placeholder `What are you trying to make?`, note placeholder `Why this one?`, send control `Send to the studio` becoming `...` while pending, sent block `Sent`, reopen control `Reopen`, answered notice `The studio has your reel`, empty line `Your reel is empty` with control `Browse projects`, signed-out line `Sign in to start a reel` with control `Sign in`. Tile add control, two states: `Add` and `Added`. Studio queue: empty line `No reels waiting`, row control `Open`. Studio reel: control `Mark answered`. Denied: line `Not your reel`, control `back to yours`. Header: `Sign out`.

**Messages.** Validation, in the order they are checked: `Add at least one project`, `A reel holds twelve projects at most`, `Give the reel a name`, `The brief is too long`, `A note is too long`, `One of your projects is no longer available`, `This reel has already been sent`. Identity: `That email and password do not match`, `That email is already registered`. The strip: `Could not reorder. Put back.`, `Could not add that.`, `Not saved.`, `Retry`, `Some changes were not saved.`, `Removed.`, `Reopened. The studio no longer sees it.`, `Check your email`. States: `No projects in this field`, `Show all projects`, `No entries of this kind`, `Show all entries`, `Could not load this`, `Try again`, `No longer available`, `You are offline`, `You are offline. Changes will be saved.`, `Could not send. Your reel is safe.` Announcements: `Showing <n> projects in <category>`, `Showing all <n> projects`, `<project title> moved to position <n> of <total>`. Destructive: `Press again`.

**The register of every message above.** A short declarative sentence in the studio's own voice. No exclamation marks, no apology, no emoji, and never the word sorry. `Could not reorder. Put back.` is four words and tells the visitor both what failed and what the page did about it. Keep that shape: a product this severe cannot suddenly become chatty at the exact moment something goes wrong.

### Forms, in detail

One form was ever designed here and every other form is built to it, so the product has one grammar rather than five.

**The newsletter field**, in the footer under the label `Newsletter`. A translucent near-white strip at the control height with no border and no radius, the standard side padding, near-white text and a near-white placeholder reading `your@email.com`, set at the small label step and transformed to lower case. Beside it, a solid-on-red control reading `Subscribe` carrying the outbound arrow. The form is a row from the tablet width up and a column below it, separated by the media gap, and it submits with the browser's own validation switched off so that every message is the product's own.

Its four states. **Idle**: the field and the control. **Loading**: both disabled, the control's word replaced by `...`. **Success**: the whole form replaced by a block on the panel ground at the control height in small uppercase reading `Thanks for subscribing`. **Failure**: the form stays and a message appears below it. The message sits **outside the form's own flow**, so that the form does not jump when a message appears.

Every other form is this one stacked, rows separated by the media gap, with the field type changed. On the sign-in routes the submit is the accent-bound solid variant rather than solid-on-red, because those routes sit on the page ground rather than on red. The forms are: sign in, taking an address and a password; create account, taking a display name, an address and a password; reset request, taking an address; and set password, taking a password twice. Sign-in rows never become a row even at the widest width: an address field beside a password field reads as a search bar.

The field inventory, with its constraints:

| Field | Route | Type | Constraint |
|---|---|---|---|
| Newsletter address | footer of every long route | address | required, trimmed |
| Sign-in address | `/sign-in` | address | required, trimmed, lowercased |
| Sign-in password | `/sign-in` | password | required, `8` to `200` characters |
| Display name | `/sign-in?mode=create` | text | required, `1` to `60` characters after trimming |
| Reset address | `/sign-in?mode=reset` | address | required, trimmed |
| New password | `/sign-in?mode=set` | password | required, `8` to `200`, entered twice, must match |
| Reel title | `/reel` | text | required on send, `1` to `80` after trimming |
| Item note | `/reel` | text | optional, at most `280` |
| Brief | `/reel` | multi-line text | optional, at most `2000` |
| Category filter | `/work`, `/blog` | control set | one known slug, or absent |

There is no phone field, no company field and no free-text message field anywhere in the product.

**Pending, success and recovery.** Pending: the submit's word becomes `...` and every field is disabled, and there is no spinner anywhere. Success: a form that ends a task is replaced by the success block, and a form that continues one keeps its shape while a success message appears where a failure message would, in the near-white ink rather than the failure red. A rejection shows the message the response carries, in that same position, with every field keeping its value and focus moving to the field the response names or to the form's first field. A failed request shows `Something went wrong` in the same place, keeps every value, and returns the submit to rest so the client can retry without retyping.

## Constraints

- Internationalisation and formatting: one studio, one locale, declared on the document. There is no translation layer and no locale negotiated from a request header. If a second locale is ever added it takes its own path prefix, because a link shared in one language must open in that language.
- Dates are the studio's own format everywhere and are never localised and never relative.
- No free-text search, no visitor-facing sort, and no filter that intersects with another.
- No pagination on the public collections. Fifteen projects and ten entries are returned whole.
- No reel index, no create-a-reel control, no default reel to choose. One account, one reel.
- No reply field, no messaging, no comments, no likes, no follows, no notification centre.
- No payments, no pricing, no currency, no money value anywhere in the product.
- No rich text, no markup parsing of anything a visitor supplied, and no dialog or modal layer.
- No spinner and no queue of notifications.
- No second theme, and no theme switcher.
- No native application and no installable offline mode.
- No audio anywhere. Nothing plays a sound, and if audio is ever added it must stay muted until it is asked for and must carry a visible control.
- No third-party measurement tag, no measurement host, and no visitor-identification pixel.
- No external network call at run time, in either direction. Nothing is fetched from another origin: not an image, not a film, not a typeface file, not a three-dimensional model, not an environment map and not a script.
- No administrative console, no role-granting route, no invitation flow.
- The product must stay responsive with fifteen projects, ten journal entries, four practice fields, twelve client marks, four awards, and a studio queue holding a few hundred sent reels, each holding up to twelve items.

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

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/projects` | optional `category` | a top-level JSON array of published projects in their authored order, each with `id`, `slug`, `title`, `subtitle`, `categories`, `tile_width` |
| `GET /api/projects/{slug}` | | the project with `intro`, `credits` and its practice fields |
| `GET /api/signals` | optional `kind` | a top-level JSON array of published entries, newest first, each with `id`, `slug`, `title`, `kind`, `published_on` |
| `GET /api/signals/{slug}` | | the entry with `body` and `related` |
| `POST /api/newsletter` | `email` | accepted, and accepted again for a repeat inside the hour without saying so |
| `POST /api/auth/sign-up` | `display_name`, `email`, `password` | the account plus a bearer session token in `access_token`, the same token also set as a session cookie |
| `POST /api/auth/sign-in` | `email`, `password` | the account plus a bearer session token in `access_token`, or one refusal that does not distinguish a wrong password from an unknown address |
| `POST /api/auth/sign-out` | | every session for the account revoked |
| `GET /api/auth/me` | | the account, carrying `id`, `email`, `display_name` and `role`, and never a password hash |
| `POST /api/auth/reset` | `email` | accepted, identically, whether or not the address has an account |
| `POST /api/auth/reset/confirm` | `token`, `password` | the password written, every session for that account revoked |
| `GET /api/reel` | | the session's own reel and a top-level JSON array of its items in `position` order, each with `id`, `project_id`, `position`, `note` |
| `PATCH /api/reel` | `title` and/or `brief` | the reel |
| `POST /api/reel/items` | `project_id` | the created item at the next position |
| `PATCH /api/reel/items/{item_id}` | `note` | the item |
| `DELETE /api/reel/items/{item_id}` | | the item removed and the remaining positions rewritten contiguous |
| `PUT /api/reel/order` | `order`, the complete array of item identifiers in their new order | the items in their new `position` order |
| `POST /api/reel/send` | | the reel in state `sent` with its `sent_at`, and a snapshot frozen at its current `version` |
| `POST /api/reel/reopen` | | the reel back in state `draft`, its `sent_at` cleared and its snapshot discarded |
| `GET /api/studio/reels` | `state`, `cursor` | a top-level JSON array of sent reels newest first, each with its client's `display_name`, the reel `title`, its item count and its `sent_at`, plus the next `cursor` |
| `GET /api/studio/reels/{reel_id}` | | the snapshot, its items in the client's order with their notes, and the client's `display_name` and `email` |
| `POST /api/studio/reels/{reel_id}/answer` | | the reel in state `answered` with its `answered_at` |
| `GET /api/health` | | readiness |

A session is required on everything except the public reads, the newsletter, sign-up, sign-in, reset and health. The curator role is required on every `/api/studio` path. The reel a request acts on is always resolved from the session, never from a path or a body, on every client-facing reel path. A successful call returns the named resource or shape; an invalid, unauthenticated or unauthorized call is rejected as a client error, never a `5xx` and never a silent success. A write against a reel that is not in state `draft` is refused as a conflict rather than applied, and the client reconciles to read-only rather than retrying. A curator's read of a reel in state `draft` answers as not found, never as a refusal.

Every response carries a strict transport policy, a nosniff content-type policy and a policy refusing framing by another origin. The session cookie is HTTP-only, secure and same-site.

### No mocks

The datastore is not simulated. Rows held in a process rather than in PostgreSQL disappear when the app restarts, and a reel assembled from a module-level object is not a reel. An ordering the page remembers between renders is not an ordering: it has to come back from PostgreSQL after a restart, in the order the client left it. A snapshot that is recomputed from the live reel at read time is not a snapshot, because the whole point of it is that it does not change when the live reel does. And a message the app logs to itself, an in-memory list of what it would have sent, or a `{"sent": true}` returned to its own caller is not a message: the four transactional messages exist as rows a curator can read. **PostgreSQL is the fact: this app's own screens can only reflect what lives in it, never substitute for it.**

## Definition of done

A visitor can read the whole public site, filter the archive to one practice field and share that filtered address as a link that opens filtered. A client can press `Add` on a project while signed out, create an account, and find that project already in their reel; can add two more, reorder them, reload the page, and still see their own order; and can write a note and a brief and send the reel, after which it is read-only. The studio reads that reel in the client's order with the client's note, marks it answered, and the client sees that it was picked up. A reel that is still a draft is invisible to the studio, and a reel that is not yours is never readable, whichever address is asked for.
