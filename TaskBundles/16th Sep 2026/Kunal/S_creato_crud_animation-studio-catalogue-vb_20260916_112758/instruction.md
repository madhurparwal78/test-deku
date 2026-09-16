# The Line Studio

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, filter the film catalogue to
one category and open a case study from it, without hitting an error page. A different stranger,
by any means, must NOT be able to reach a film that is under embargo or past its rights window:
not at its own address, not in the catalogue, not in any count, not in the search results, not in
the machine-readable site index, and not through the onward link on the film beside it. That
cannot be arranged by hiding a tile. The record must be absent from the response the server
builds, and an address that answers differently for a hidden film than for a film that never
existed is itself the leak.

## Overview

The Line Studio is an animation studio in Leeds, England. This is the studio's public face and
the system that keeps it true. The catalogue is the spine: every film the studio has directed,
one case study each, reachable in two interactions from anywhere in the product. Around it sit a
slate of original properties the studio is developing for itself, an editorial feed, a podcast
archive, a shop selling digital packs and limited physical editions, and a contact surface that
routes an enquiry to a named person by subject rather than into a shared inbox.

Behind all of it is an editorial back office where a small staff drafts, reviews, schedules,
embargoes and publishes every public record, and where a shopkeeper manages products, drops and
orders. Visitors need no account. Customers have one so they can return and re-download something
they bought. Staff sign in somewhere the public never sees.

Three things decide whether this product is correct, and none of them is visible in a screenshot.
Counts must be honest: the facet buttons print their own counts and the header prints the
catalogue total, and a count derived separately from the list it describes will drift, which
makes every other number in the product untrustworthy. Work under embargo must be genuinely
unreachable rather than merely hidden, because a case study for an unannounced client campaign is
under contract. And a purchase must never be lost: a digital pack is bought once and
re-downloaded for years, including after the pack has been updated.

What this is deliberately not. Not a client portal: there is no logged-in area where a client
reviews work in progress. Not a booking system: an enquiry is a message routed to a person, not a
calendar slot. Not a print shop: physical fulfilment is tracked as a state, never performed. No
comments, no likes, no follower graph, no messaging between visitors. No card details anywhere,
at any depth, by any route.

The genuinely hard part is one sentence. Four conditions - the record's state, its embargo
instant, its rights window and its client's naming permission - must be applied inside the query
that selects records, and the same conditions must produce the list, the total and every
per-facet count. Everything else here is ordinary product work.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor, no account | browse the catalogue, filter it, open a case study, read the feed, play a podcast preview, search, subscribe to the newsletter, send an enquiry, ask to be told when a drop opens | **see any draft, scheduled, embargoed, expired, archived or confidential record, by any address**; **reach the back office** |
| Customer | everything a visitor can, plus buy a digital pack or a physical edition, see their own orders, download what they own including every later version of it, track a shipment | **read, download or reference any other customer's order, entitlement, download or shipment, by any identifier in any request**; **change anything editorial** |
| Editor | create, update and read drafts of case studies, articles, slate entries, episodes and jobs; create and update people; read and assign enquiries; read the editorial log for records they touched | **publish, unpublish, schedule, reorder, embargo, delete**; **read the editorial log for a record they never touched**; **touch products, drops or orders** |
| Publisher | everything an editor can, plus reorder, publish, unpublish, schedule, and set an embargo | **lift an embargo early**; **change a rights window**; **change a client naming permission**; **merge people**; **delete a record**; **publish a record they authored themselves** |
| Producer | everything a publisher can except lifting an embargo early, plus change rights windows, change a client naming permission, merge two people, delete a record | **lift an embargo early**; **touch products, drops or orders**; **manage staff accounts** |
| Shopkeeper | manage products, versions, drops, stock and fulfilment; refund an order; grant or revoke an entitlement; read and assign enquiries | **create, edit or publish any editorial record**; **manage staff accounts** |
| Owner | everything, plus lift an embargo early, manage staff accounts and export the subscriber list | nothing |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from an Editor session to any Publisher-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected
state unchanged.

Three asymmetries in that table are deliberate and each must hold. A Publisher may set an embargo
and only an Owner may lift one early, because lifting early is the irreversible action. Only a
Producer may change whether a client may be named publicly, because that is a contractual fact
and not an editorial one. And an Editor may read the editorial log only for records they touched,
which is enough to check their own work and not enough to audit a colleague.

**Enforcement lives in one place**: a single decision consulted by every command handler and by
every public read condition. It is not enforced in the interface, and the interface's decision to
hide a control grants nothing. Every denial is recorded with the principal, the command, the
record and the request identifier. A command with no permission entry is denied, and the app
refuses to start rather than denying it at request time. A record a requester may not see answers exactly as an address that never
existed, including its headers: a different answer for a hidden film is how somebody goes fishing
for unannounced work.

**Signup is open for customers.** A visitor may create a customer account with an email address
and a password. Staff accounts are never self-served: only the Owner creates one.

Seeded accounts, all with the password `deku-demo-pw-2026`:

| Email | Role |
|---|---|
| `editor@example.com` | Editor |
| `publisher@example.com` | Publisher |
| `producer@example.com` | Producer |
| `shopkeeper@example.com` | Shopkeeper |
| `owner@example.com` | Owner |
| `customer@example.com` | Customer, owns one digital product |
| `customer2@example.com` | Customer, owns nothing |

## Core features

### Auth

Email and password with bearer tokens. The client sends the token on every request that is not
the health check, a public read, or a sign-in. Passwords are hashed; the literal
`deku-demo-pw-2026` must work at login for every seeded account.

1. A bearer token expires. An expired token is refused and nothing is written.
2. Staff sign-in is reachable only under `/studio`. No public route carries a staff sign-in
   control, and a staff credential presented to a public route handler is refused.
3. A customer signs in on the public origin, for their own orders and downloads only.
4. A sign-in with a wrong password is rejected without saying which half was wrong, and repeated
   failures for one address slow down rather than locking the account permanently.
5. The response to a request for a sign-in link is identical whether or not the address is known.
   A differentiated response turns the form into a tool for testing whether somebody has an
   account.

### The catalogue

The spine of the product, at `/work`. Every published film on one page, no pagination.

1. The catalogue header prints the live total as `[ 6 ]` on seeded data, and the facet control
   prints `All [ 6 ]`, `Branded [ 3 ]` and `Entertainment [ 3 ]`.
2. **The total, every facet count and the list itself come from one derivation.** A count computed
   separately from the list it describes drifts. Publishing a film raises the total and its own
   facet count in the same breath; embargoing one lowers both. A count that disagrees with the
   number of tiles rendered is a defect however correct each looks alone.
3. The facet options are derived from the types actually present on readable case studies, never
   hard-coded. `All` is always first and always carries the total.
4. Choosing a facet rewrites the address to `/work?type=branded` and does not reload the route.
   The header, the facet panel and the floating controls persist through the change.
5. **A filtered catalogue survives a reload and a back navigation.** Opening
   `/work?type=branded` directly renders the three Branded films with the facet already chosen.
   This is the rule the whole product rests on: **what the list displayed must be what is stored,
   and re-reading it must show the same thing.** A grid that only looks right until the page is
   reloaded has failed.
6. `/work?type=nonsense` falls back to all films with a message, never an error page.
7. Facets are exclusive by design. An address requesting two takes the first.
8. Two view modes, `Grid` and `List`, toggled by a floating control at the foot of the page and
   **persisted for that visitor across route changes and reloads without a server round trip**.
   `Grid` is three columns at desktop, two at tablet, one at handset, media above metadata. `List`
   is one row per film, full width, metadata left and a small preview beside it. The current mode
   is carried in a stable machine-readable attribute on the grid container.
9. Default ordering is publication date, newest first, with an editor-set manual position
   overriding it for records that carry one. Ordering is stable: two films sharing a date break
   the tie on identity, so the catalogue never reshuffles between requests.
10. A tile prints, in this vocabulary: the literal word `Type` then a slash then the type; the
    literal word `Director` then a slash then the director names; the title; the synopsis; and an
    identity of the film's position in the current ordering, then a slash, then its two-digit
    year. **The position counts from `01` within the current ordering, so a filtered catalogue
    renumbers.** It is not the record's identifier.
11. A film with several directors lists all of them, comma separated, each linking to that
    director's filtered catalogue. A film with no director recorded shows no director row at all
    rather than a blank one, and cannot be published.
12. A facet that yields nothing renders `No films under <TYPE> yet.` with a control returning to
    all films.
13. While a filter is in flight the counts hold their previous values and the grid dims. Nothing
    changes size.

### Media, and the budget it lives under

The catalogue is a wall of film. Almost all of the engineering here is about not requesting it.

1. **Every media box is laid out at its final size and filled with the signal red before anything
   arrives.** Nothing reflows when media lands. A half-loaded catalogue reads as a deliberate red
   grid rather than as a broken page, and the feed's reserved cards alternate the red with its
   pale tint so a loading feed reads as a designed checkerboard.
2. A picture resolves outward from its centre through a mask rather than fading flat.
3. Five video roles, and they do not share rules: a tile preview is silent, looping, without
   controls, and requested only at the desktop composition; a hero background is silent and
   looping; a feature player has sound and full controls and never autoplays; a secondary
   behind-the-scenes player is the same; a carousel item is silent and looping.
4. **A silent looping preview is an enhancement and is never merely paused.** On a coarse
   pointer, under a saved-data preference, on a connection the platform reports as slow, or under
   reduced motion, the poster is shown and **no video is requested at all**. The cost being
   avoided is bandwidth, not frames.
5. **At most twelve tiles may hold a video element at one time**, those within the window plus one
   screen either way. A tile leaving that window releases its video element and its source; it
   does not merely pause. Every film is still fully written into the page with its title and its
   synopsis, because the markup must be findable and readable with scripting unavailable. It is
   only the media that is held back.
6. No route requests a single video byte before its own critical content has painted.
7. **Performance on this product is almost entirely a question of film.** Film is the
   overwhelming majority of what a visit would transfer, and every budget here follows from that:
   markup, styles and code together are a small fraction of it. Virtualisation applies to the media and
   to nothing else: the markup is never virtualised, because the cost of every title and synopsis is a few tens of kilobytes
   and the cost of every film is an order of magnitude more. The most expensive visual effects,
   the duplicated multiplying layer and the blur behind the floating controls, are capped by
   count rather than trusted.
8. A rendition is chosen from the rendered box width: the smallest below a narrow box, the middle
   one between, the largest above. Tile previews always take the smallest whatever their box,
   because they are silent, looping and many to a page.
9. Every video surface prints a duration and shows a poster, and both are derived on ingest
   rather than typed: a job reads the source duration and generates a poster frame at a
   producer-chosen timecode defaulting to one tenth of the way in. Duration is stored in seconds
   and formatted at render, `M:SS` under an hour and `H:MM:SS` above it. A duration under a
   minute renders `0:MM`, never as seconds alone.
10. A record whose poster job has not completed keeps its reserved state and **cannot be
    published**.
11. **Only one media source plays at a time, across video and audio together.** Starting a podcast
    preview stops any playing film, and starting a film stops any playing preview. Nothing ever
    begins with sound.

### The case study

At `/work/<slug>`. Not a fixed template: an ordered, mixed sequence of modules chosen per film.

1. The hero is a full-bleed still or film under a red panel carrying, in order, the frame rate
   with `FPS` after it, the type, the running time, the month and two-digit year, and the studio
   copyright line in Roman numerals. A link reading `The Crew` jumps to the credits block at the
   foot of the same route rather than opening anything.
2. The intro prints a definition list: `Director`, whose values are links to that director's
   filtered catalogue, and `Client`, whose values are plain text. **Directors link and clients do
   not**, because a director has a body of work in the catalogue and a client is a name.
3. The module kinds are a closed set: feature player, section heading with its split word, rich
   text, secondary player marked `BTS`, captioned slider, navigable carousel with a thumbnail
   strip, crew block, director note, full-bleed image, and pull quote.
4. Each module kind has its own field set and its own validation. **A module payload that fails
   its validation is refused at the write**, never tolerated and skipped at render, and a record
   whose modules do not all validate cannot be published.
5. Crew is a relationship, not text. A person exists once in the people directory, is attached to
   a film with a role and a position, and their name is rendered from that directory so a
   correction propagates everywhere. **Credits always print in the industry order** - Director,
   Producer, Production Manager, Art Director, Animation Lead, Clean-up Lead, Compositing Lead -
   regardless of the order anybody typed them in.
6. A person who leaves the studio disappears from the squad list on `/about` and **remains
   credited on every film they worked on**, because a credit is a historical fact and staff
   membership is not. `Halle Brandt` is seeded in exactly that state.
7. The director note is a toggle revealing commentary attributed to the director.
8. The onward link at the foot goes to **the next film in the ordering the visitor is actually
   walking**: if they arrived from a filtered catalogue, the next film inside that filter. When
   the current film is the last, it wraps to the first. When it is the only readable film, the
   link is suppressed rather than pointing at itself.
9. A case study whose media is still processing renders with its reserved boxes and no player
   control.

### Publication, embargo and rights windows

One state machine serves case studies, articles, slate entries, episodes and jobs: `draft`,
`in_review`, `scheduled`, `published`, `embargoed`, `expired`, `archived`.

1. **The publication gate returns every failure at once, not the first.** A record may enter
   `published` or `scheduled` only when: every required field is present; every module payload
   validates; every referenced asset is ready; every non-decorative image carries alternative
   text; at least one director credit exists on a case study; the type is set and is an existing
   facet; a duration exists and is greater than zero; the rights start is not in the future; the
   slug is unique among records that are not archived; an outbound article has either a
   resolvable target or a body; the client naming permission has been reviewed since the client
   last changed; and a poster exists for anything carrying media.
2. **Two-stage publish.** An Editor moves a record to `in_review`. A Publisher, Producer or Owner
   then publishes it, schedules it, or returns it to draft with a required note that is attached
   to the record and shown to its author. **A Publisher may not publish a record they authored
   themselves**, unless they are the Owner. That is the only separation-of-duty rule here and it
   is not optional.
3. A scheduled record is published by the app's own scheduled work, which claims each due record
   so the same record is never published twice. Publishing a record that is already published is
   a no-op, recorded as one. The scheduled instant is stored with its zone, entered in the
   studio's zone, and shown in both the studio zone and the viewer's zone, because a film timed
   to a client's press announcement in another country is the normal case and an hour's error is
   a broken contract.
4. **An embargoed record is treated as not existing by every public path, without exception.** Its
   own address answers as a slug that never existed. It is excluded from the catalogue list and
   every count by the same condition that selects them, never by a filter applied afterwards. The
   onward link of its neighbour resolves past it. It is absent from the home route, the feed, the
   slate, the search results, the machine-readable site index and every syndication document. It
   remains visible in the back office, marked, with its lift instant. A preview link may still
   open it, and every such view is recorded.
5. Lifting an embargo early is an Owner-only command, recorded, and requires typing the record's
   name to confirm. At the stated instant the app's scheduled work lifts it and everything
   returns.
6. A rights window is a start instant, an end instant and an optional territory list. Before the
   start the record is unpublishable; after the end it is `expired` and publicly unreadable
   without being deleted, and it disappears from the catalogue, the counts, the machine surfaces
   and the onward links. It stays visible in the back office marked as expired, because a
   Producer will renew it. When a region cannot be inferred, a record with a territory list is
   treated as not visible: that is the safe direction.
7. **A client whose naming permission is withheld appears in no response field anywhere** for that
   film. The film publishes; only the naming is withheld. A name that is absent from the page and
   present in the payload has leaked. `Kessel` is seeded in exactly that state.
8. **Every mutation and its editorial log row commit together or not at all.** The log is
   append-only: no update, no delete, no exception. One row per changed field, naming the actor,
   the record, the field, the value before, the value after and the request identifier. A
   mutation that commits without its log row is a defect and a log row without its mutation is
   worse.
9. **Invalidation is part of the mutation, not a later tidy-up.** Publishing, unpublishing,
   embargoing, lifting an embargo or expiring a record refreshes everything derived from it in
   the same breath: its own address, the catalogue list, the total, its facet count, the home
   route, the machine index, the syndication documents and the onward links of its neighbours.
   Nothing derived from a record may outlive a change to it, and a response that still shows the
   old answer after the change has committed is the defect this rule exists to prevent.
10. Two editors saving the same record: every update carries the version it read, and a stale
   version is refused as a conflict with the current record returned, rather than overwriting.
   **A conflict is presented as a field-level comparison, never as a whole-record overwrite
   prompt**, because a prompt that offers to discard somebody's work is not a resolution.
   Reordering modules is its own command carrying the whole ordered list of identities, so two
   concurrent reorders conflict rather than interleaving into nonsense. A draft saves itself as
   it is typed, and an automatic save writes no log row: only an explicit save does.
11. An unpublished record may be opened with a preview link, whose **scope is one record in one
    representation**: seven days, not extendable, granting a read and never a write and never a
    list, revoked immediately on publication, excluded from every machine surface, recorded on
    every view, and the rendered page carries a persistent banner reading `Not published. This
    preview link expires <DATE>.`

### The slate

At `/entertainment`. The studio's own properties, and the most commercially sensitive records in
the product.

1. Visibility has three values, not two: `confidential`, which is the default for a new entry and
   is **not served at any address**; `announced`, which serves the title, the logline, the format
   and the stage and nothing else, no partner names and no dates; and `in_production`, which
   serves all of that plus a link to the catalogue record once one exists.
2. Confidential entries are excluded by the condition that selects entries, never filtered out in
   the renderer.
3. The status line is rendered from a controlled vocabulary of a format and a stage, printed as
   the format then the word `in` then the stage. The seeded statuses are `Series in development`,
   `Feature film in development`, `Web series in development`, `Game in development`, `In
   development`, `Pre-school series in development` and `Web series in production`. Free text is
   not accepted: the same status written two ways is the defect this replaces.
4. Each entry prints its position in the list, then a slash, then the literal characters `XX`.
   **`XX` is a constant, not a total**, because a slate has no fixed end. It is deliberate and
   must be preserved.
5. A slate with nothing announced does not render its heading at all. That block is structurally
   empty, not temporarily empty.
6. The route carries the studio's position on unsolicited material, and that position is
   enforced by the enquiry form rather than merely printed beside it.

### The feed

At `/blog`, labelled `Feed` everywhere in the interface. **The path and the label are decoupled**
and the path stays stable for inbound links.

1. Exactly one article may be featured at a time. **Featuring a second unfeatures the first**, so
   the flag is a single reference held on the studio record rather than a boolean on each article.
2. With no featured article the featured block is absent and the index moves up. The route never
   renders an empty hero.
3. A card prints its category, then the date as three separate parts - day, month, year -
   separated by slashes, then the title, then the standfirst. The three parts are styled
   separately and the wrapping element carries one machine-readable date, so the date is
   parseable while the parts are set as a production stamp.
4. Categories are a controlled vocabulary derived from the categories present on published
   articles, in an editor-set order. Two are seeded, `Studio News` and `Entertainment`, and the
   set is not hard-coded at two.
5. **Two article shapes, and the second is the common case.** An original article holds its own
   body. A link-out article holds a standfirst and one or two pull quotations only, and ends in a
   link reading `Read The Article` pointing at the publication that carries the full piece. A
   build that assumes every article has a body renders empty pages for most of a studio archive.
6. An outbound link opens in the same tab, carries a relationship annotation preventing the
   target from reaching back into this window, and **names its target host beside the link so a
   visitor knows where they are being sent before they go.** The outbound event is recorded with
   the article identity and the target host.
7. A link-out target is checked on a schedule. A target that fails three consecutive checks marks
   its article for editorial attention and is **never unpublished automatically**, because a dead
   link on a published article is an editorial decision.
8. An article with an empty body and no outbound target fails the publication gate and cannot
   reach a published state at all.
9. A category with no articles renders `Nothing filed under <CATEGORY> yet.` with a control
   returning to all.

### The podcast

At `/podcast`. Short route, dense with episodes.

1. Episodes are grouped by season, newest season first, and newest episode first inside a season.
   **Seasons are derived from the episodes, never declared**: a season with no episodes has no
   heading at all.
2. A row prints its identity as the letter `S`, the season, a dot, the letter `E`, the episode -
   **both zero-padded to two digits**, which corrects the source's own inconsistency - then the
   guest, then the duration formatted `H:MM:SS`.
3. The preview control is invisible at rest and resolves on row hover or focus. **It must be
   reachable in tab order while it is still transparent**, or the whole archive becomes unplayable
   from a keyboard.
4. A preview plays a bounded clip that is **a separate short file, not a range request against the
   full episode**. A range request against a two-hour file still opens a two-hour file, and a
   visitor pressing preview on six rows has opened six of them.
5. The amplitude bars beside a playing row are driven from the playing audio itself, from a
   precomputed amplitude series stored once on ingest rather than by decoding the whole file in
   the browser. When the audio graph is unavailable the bars render at a fixed height and playback
   still works.
6. Playback continues while the visitor scrolls and while they move to another route inside the
   app, and stops on a full page navigation. The playing row is marked and its control becomes a
   stop control. **Only one row may play.** Position is not remembered between visits.
7. Audio never autoplays. The analyser is torn down when playback stops.
8. The `Listen` links point at the show's distribution addresses. **There is deliberately no full
   player in the product**: the product previews and the directories deliver.
9. An episode whose audio is still processing renders without a preview control and is excluded
   from the syndication document.
10. Ingest derives everything a person would otherwise type: it reads duration, channels and
    loudness, produces a normalised rendition and keeps the original, cuts the preview clip
    between its stored start and end seconds defaulting to forty-five seconds from one tenth in,
    computes the amplitude series once, and uses the show artwork unless an episode overrides it.

### The shop

At `/shop`. Two panels: digital products on the left on the sheet, physical editions on the right
on the red. At the handset composition they stack.

1. Digital products are seeded as `Rostrum Brush Pack` at `1200`, `Beatboard Templates` at `1000`
   and `Lightbox Starter Kit` at `2500`, all in `usd`, all integer minor units. `1200` is `$12.00`, not
   `12.00` and not `12`. The panel prints its own count as `[ 3 ]` and the subtitle
   `One-time purchase, lifetime updates. Go go go!`.
2. Each product card carries a stable scatter seed derived from its identity, so the pile looks
   scattered and **looks the same on every visit**, and a card does not jump when the list is
   re-fetched. Under reduced motion the scatter is suppressed entirely and the cards render as a
   plain grid. The pile is keyboard traversable in the list's real order whatever its visual
   scatter.
3. **What is bought is the product, never a version.** What is delivered is the current version at
   the moment of download. A new version is immediately downloadable by everyone who ever bought
   the product, with no per-customer work. That is the lifetime-updates promise and it is the
   reason the entitlement points at the product. `Rostrum Brush Pack` is seeded with versions
   `1.0` and `1.1` to prove it.
4. Price, format, size and a licence summary are all rendered before a visitor commits, and the
   full terms are linked.
5. An entitlement is one row per customer and product, unique, permanent unless revoked by a
   refund. **Buying the same product twice creates no second entitlement**: the second purchase is
   refused as already owned, and the customer is told they already own it and shown their
   download.
6. A download is a short-lived single-use address minted per request and bound to the entitlement.
   **The entitlement is resolved from the authenticated customer and the requested product, never
   from an identifier carried in the request.** A request from `customer2@example.com` for
   anything owned by `customer@example.com` is refused whatever identifier it carries, and the
   underlying row does not change. An expired link renders `That link has expired. Here is a new
   one.`
7. Physical editions are sold in timed drops. A drop moves through `closed`, `announced`, `open`
   and back to `closed`. Closed is the normal state and not an error: the panel prints
   `The shop is closed!` with a control to be told when the next drop opens.
8. The countdown on an announced drop is computed against a server-supplied instant and refetched
   when the tab becomes visible again, **never from the device clock**, because a clock an hour
   fast would otherwise open the shop early. The change from announced to open happens in place
   without a reload, and the visitor's scroll position is not touched.
9. An item is purchasable while its total stock exceeds what is sold plus what is reserved.
   Adding to a basket reserves stock for a bounded window and the reservation expires on its own.
10. **Two visitors buying the last item must not both succeed. Exactly one is accepted, the other
    is refused with the sold-out message, and stock never goes below zero.** This must hold under
    real concurrency. A failed purchase leaves no partial state: no order row, no reserved unit
    stranded, no entitlement. `Studio Tee` is seeded with exactly one remaining for this reason,
    and `Crop Mark Print` is seeded sold out and prints `Gone`.
11. **A purchase submitted twice with the same idempotency key produces exactly one order, one
    set of lines and one entitlement**, and the second submission returns the first result rather
    than acting again.
12. A refund revokes the entitlement and invalidates every outstanding download link for it, and
    the customer is told which product and why. A chargeback does the same and additionally
    flags that customer's address for review before any future entitlement is granted. The
    product never marks an order refunded on optimism: the refund is recorded when it is real.
13. **The division of responsibility is deliberate.** This product owns the catalogue, the
    presentation, the price display, the order, the entitlement and the delivery. It does not own
    and never sees the card details, and the price, the format, the size and the licence summary
    are all rendered here rather than left to be discovered later. An oversell is impossible by
    construction rather than by care.
14. A product with entitlements against it is **delisted, never deleted**. Every existing
    entitlement keeps working.
15. Shipment state is displayed, never proxied. An order does not become delivered because time
    passed: after a long wait with no word it becomes `unknown`, because `unknown` is honest and
    `delivered` is a claim.

### The contact surface

At `/contact`. The studio's revenue funnel, and the reason contact is not one form.

1. The route lists a named person and an address for each kind of enquiry, so commercial work,
   original properties and games each reach the right desk. The seeded routes are
   `Commercials and Branded Content` to `newbusiness@example.com`,
   `Head of Development / IP` to `entertainment@example.com`, `Games` to
   `games@example.com`, `Careers` to `jobs@example.com`, and `General` to
   `info@example.com`.
2. **The enquiry is stored before any delivery is attempted.** The studio's new business must not
   depend on a mail service being reachable at the moment somebody decides to get in touch. The
   stored enquiry carries the subject it was classified under and the address it was routed to.
3. When the person a subject routes to has left the studio, that subject routes to the general
   address, the person is not named, and the enquiry is flagged.
4. **The addresses remain visible whether or not the form works.** If the form is unavailable the
   page names the outage and the addresses are still there. The form is never the only route.
5. The form's fields are: name, required, two to a hundred and twenty characters after trimming;
   organisation, optional; email, required; subject, required, from the routed vocabulary plus a
   general option; budget band and timing, optional and **present in the markup only once a
   commercial subject is chosen** rather than rendered and concealed, so a keyboard visitor never
   tabs through fields that do not apply; message, required, twenty to four thousand characters
   after trimming with a live remaining count once it runs long; and an attachment, optional and
   refused on two subjects.
6. **The submissions policy is enforced, not printed.** On the development and games subjects no
   file control is rendered at all, and a submission carrying an attachment is refused with
   `We cannot accept attachments on this subject. For legal reasons we are unable to look at
   unsolicited creative material. Portfolios go to jobs@example.com.` It is never
   silently dropped. The same stored policy text renders in all three places it appears, so it
   cannot diverge.
7. Where an attachment is accepted: one file, at most ten megabytes, one document format,
   determined by inspecting the content rather than trusting the name or the extension, stored
   under a generated name outside anything the app serves, and never served from this origin.
8. Opportunities lists open roles with a title, a contract type, a location and an application
   address. **With no open roles it prints `We're currently not hiring, check back another time.`,
   which is a first-class state and not a fallback.**
9. Six questions and answers, numbered `[ 01 ]` to `[ 06 ]`. Each opens and closes independently,
   several may be open at once, the open set is written to the address as a fragment so one answer
   is linkable, and **every answer is present in the served markup whatever its open state**, so
   it is findable by the browser's own find-in-page.
10. The four address lines are one link with the whole address as its accessible name, not four
    adjacent links.

### Forms, validation and spam

Three visitor-facing forms: the newsletter field in the footer, the enquiry form, and the drop
notification field.

1. **Never validate a field the visitor has not finished with.** Validation runs on blur for a
   field that has been changed, and on submit for everything.
2. **Once a field has failed, validate it on input**, so the error clears as it is fixed rather
   than on the next blur.
3. **Never move focus on validation.** On a failed submit focus moves once to the first invalid
   field and never again.
4. Email validation checks for one at-sign with something either side and a dot in the domain, and
   **nothing more**. It does not check the domain against a list, does not reject plus-addressing,
   does not reject long domains, does not lowercase what was typed for display, and does not
   silently correct a domain it thinks is a typo.
5. Every form rejects invalid input inline, names the field it belongs to, and writes nothing. The
   message sits directly below its field, states what to do rather than blaming, is
   programmatically the field's description, is announced when it appears without moving focus,
   and is **never carried by colour alone**: it is text. A failed submit also renders a summary
   above the form linking to each invalid field.
6. **Nothing a visitor typed is ever discarded.** A failed submission leaves the form populated, a
   recoverable failure offers a retry with the values intact, and navigating away from a dirty
   form asks first.
7. Spam control is layered and none of the layers is a visible puzzle: a decoy field hidden from
   sight and from assistive technology, whose completion accepts and silently discards; a
   submission arriving faster than a person could type it, refused; a single-use token minted on
   render, bound to the session and expiring; and a limit per address and per source, so a form
   submitted **repeatedly** in quick succession is refused rather than served. A refused
   submission that is not clearly automated is quarantined for a human to read rather than
   deleted, because losing one real commission enquiry costs more than reading a hundred junk
   ones.
8. A form has four visible conditions and no more: **idle, with submit enabled**; sending, with
   submit disabled and relabelled, the form still populated and no spinner standing in for it;
   succeeded, with the form replaced by a confirmation; and failed, with everything still there.
9. **Rate limiting exists to stop abuse and not to stop people.** Limits are keyed by address and
   by source, generous enough that an office or a mobile carrier sharing one address is not
   blocked, and a burst of requests for addresses that do not exist is slowed and recorded,
   because somebody trying two hundred slugs in a row is not browsing.
10. Rate-limited submission renders `You have sent a few already. Try again in <MINUTES>
   minutes, or email info@example.com.` and names the addresses as the alternative.
11. A successful enquiry replaces the form with `Thanks <NAME>. This went to the right desk and you
   will hear back within two working days. We sent a copy to <EMAIL>.`
12. Newsletter subscription is double opt-in: the row is created pending, a single-use
    confirmation link moves it to confirmed, an unconfirmed row is removed after a month, and a
    previously unsubscribed address must confirm again. **The response is identical whether the
    address is new, pending or already confirmed.**
13. **The three audience lists never merge.** Somebody who asked to be told when a drop opens has
    not asked for a newsletter, and an enquirer has asked for neither. Each row records which
    surface captured it and on what basis.
14. Unsubscribing takes one click, is honoured without a confirmation step and without a session,
    and is recorded before the visitor is sent anywhere.

### Search

1. Search covers everything published and nothing that is not: case studies by title, synopsis,
   type, director names, nameable client names and module text; articles by title, standfirst,
   body and category; announced slate entries; episodes by guest and identity; products by title
   and subtitle; people by name and roles.
2. **Nothing unpublished, embargoed, expired, confidential or carrying a withheld client name is
   ever indexed.**
3. **Removal is synchronous and addition may be asynchronous.** An embargo, an expiry or an
   unpublish removes the document in the same transaction as the mutation; a newly published
   record may appear a moment later. A film appearing in search a minute late costs nothing; a
   film under embargo remaining searchable for a minute is the failure this product is most
   careful about.
4. **The scope above is the whole scope**: nothing outside it is searchable, and nothing inside
   it is skipped. Matching is by prefix and tolerates a single character's difference on longer
   terms. Ranking is field-weighted, title above synopsis above module text, with recency as the
   tiebreak. **Stemming is English only**, matching the site language, because a second language
   would need a second analyser nobody would maintain.
5. The index is derived, disposable and rebuildable from the database in one command. It is
   **rebuilt nightly into a new index and swapped atomically**, and updated incrementally in
   between. It is never
   It is never a source of truth, and a disagreement between the index and the database is always
   resolved in the database's favour.
6. The control sits in the header at the desktop composition and in the navigation overlay below
   it. Before anything is typed it offers the three most recent publications. Results are grouped
   by kind with a count per group, keyboard navigable, with the current result announced, and
   pressing enter with nothing selected opens the full results at `/search`.
7. Empty results render `Nothing matches <TERM>.` with the nearest indexed terms where there are
   any.
8. A search term is hashed where it is recorded. Term frequency is answerable and the terms
   themselves are not stored, because a search box on a studio site fills with half-remembered
   client names.

### The machine surfaces and the launch surface

1. A machine-readable site index lists every publicly readable record and is regenerated on
   publication and on an embargo lift. A syndication document per feed category and one combined
   carry the most recent published articles. A podcast syndication document carries every
   published episode with its audio address, duration, season and number, and it is generated
   rather than authored and validated before it is served, because an invalid one silently
   removes the show from the directories. An episode's identifier and its audio address never
   change once set.
2. **Anything unpublished, embargoed, confidential or out of its rights window appears in none of
   the three.**
3. A **terms** of sale page covers the digital licence and the physical drop, and a storage
   statement covers the measurement posture. Both are reachable from the footer of every page,
   and the terms page is linked from the purchase surface before a visitor commits.
4. **Every content image carries alternative text**, and decorative images declare themselves
   decorative: the crop-mark overlay, the duplicate wordmarks and the separator glyphs are
   decorative and say so.
5. **Every internal link on every public route resolves.** A link that leads nowhere is a defect,
   and the not-found page exists for addresses nobody published, not for the product's own links.
6. Every public route declares its own social **preview image** and preview title, and the image
   resolves.
7. Every page view is recorded first-party with its route, its referrer host, its composition band
   and its instant, readable by the Owner. **No identifier is written to the visitor's device for
   measurement**, no third-party analytics script is loaded, and there is no advertising pixel and
   no tag manager. That is why there is no cookie banner: there is nothing to consent to.
8. An unknown address renders the product's own not-found page with the full chrome, a message,
   and three ways back into the catalogue: the newest film, a random film, and the catalogue
   itself. It never redirects to the home route, because a visitor who followed a dead link needs
   to know the link was dead. A slug that once existed resolves through the redirect table with a
   permanent redirect and never reaches the not-found page.

### Privacy, retention and subject rights

1. The privacy page is content that commits the build: the newsletter collects an address and
   nothing else; every marketing message carries a one-click unsubscribe; a person may withdraw
   consent and have their data erased; a person may have their data exported in a machine-readable
   form; third parties are named; and data found to have come from a child is deleted on
   discovery.
2. A processing register records, per data category, what it is, why it is held, the lawful basis,
   the retention period, where it is stored and who receives it. **A privacy page change adding a
   data category is refused until the matching register entry exists.**
3. An access or portability request produces an export of every row keyed to that address in a
   machine-readable form. An erasure request deletes the subscriber, drop-watcher and enquiry
   rows, and **anonymises rather than deletes a customer**, because the order record is retained
   for accounting. The editorial log keeps actor identities and loses the personal payload.
4. A credited person asking for removal comes off the staff list and their portrait is deleted,
   and **their credits are retained**, because a credit is a joint professional record.
5. Each kind of processing records the basis it rests on: consent for the newsletter, captured
   by the double opt-in, and consent again for a drop notification, scoped to that drop;
   **legitimate interest in responding to an approach** for handling an enquiry; the contract for
   fulfilling an order and granting an entitlement; a legal obligation for the accounting
   retention; and legitimate interest again for the measurement posture, which is supported by
   its having no cross-site identifier to justify.
6. Retention is enforced by scheduled work per category, and each run records its counts so a
   category that stops being pruned is visible.

### The studio's live state

1. The header prints whether the studio is open and fills a dot when it is, as
   `Open (10-6pm)` on seeded data. **The open state is computed on the server** from the studio's
   own opening hours, its own time zone and its holiday list, never from the visitor's device
   clock, because a visitor in another zone with a wrong clock must still see the truth.
2. The response carries the open flag, the displayed hours and the instant of the next change, so
   the client schedules one update at the right moment rather than asking again and again.

### Scheduled work

The app performs its own scheduled work, in-process. Each run **claims its work so two runs cannot
process the same record**, is safe to run twice, and records a run row with its start, its end,
its outcome and its counts.

| Work | What it does |
|---|---|
| publish due records | moves scheduled records to published at their instant |
| lift embargoes | lifts an embargo at its stated instant |
| expire rights windows | moves a record past its rights end to expired |
| open and close drops | moves a drop through its states at its instants |
| expire stock reservations | releases a reservation that was never completed |
| check outbound links | marks an article whose target has failed three consecutive checks |
| regenerate the machine surfaces | on change, and on a schedule |
| prune by retention category | per the retention table, reporting counts |

**Scheduling is stored with its zone and evaluated on the server**, never against a visitor's
clock, and a record due in the past at startup is published on the next run rather than skipped.

**A run that does not happen is as much a failure as a run that errors.** The run record must make
a scheduled job that has stopped running visible without anybody noticing an error, because the
embargo lift silently failing is a broken client contract and produces no error at all.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | home: hero film, intro with the live catalogue count, three featured films, studio panel, clients, reel, three news cards | none |
| `/work` | the catalogue: facet control with counts, tiles or rows, floating view and top controls | none |
| `/work/<slug>` | a case study: hero slate, intro, ordered modules, crew, onward link | none |
| `/entertainment` | the slate: proposition, routed contacts, the development list | none |
| `/about` | the studio: narrative, three process cards, reel, four disciplines, the squad | none |
| `/blog` | the feed: one featured article above a card grid | none |
| `/blog/<slug>` | a feed article, original or link-out | none |
| `/podcast` | the archive, grouped by season | none |
| `/shop` | two panels: digital products and editions | none |
| `/contact` | routed enquiry directory, opportunities, questions and answers, the form | none |
| `/privacy` | the privacy document | none |
| `/terms` | terms of sale | none |
| `/storage` | the storage statement | none |
| `/search` | full results, grouped by kind | none |
| `/account` | a customer's own orders, entitlements and downloads | customer |
| `/studio` | the back office | staff |

Site credits are **not a route**: they open as an overlay with no address and no history entry, so
the browser back control does not close them. The close control is the first focusable element and
the escape key and a click on the ground both close it.

**Entry and redirects**

| Case | Result |
|---|---|
| unauthenticated visitor requests `/account` | the customer sign-in, returning to `/account` afterwards |
| unauthenticated visitor requests `/studio` | the staff sign-in, giving nothing away about what is behind it |
| staff sign-in succeeds | the back-office record list |
| customer signs out | back to `/`, the session revoked, protected routes refused again |
| a token expires mid-action | the action is refused as unauthenticated, nothing is written, the form keeps what was typed |
| a staff user issues a command their role does not carry | refused by the server, **and the underlying database row must not change** |
| a slug in the redirect table | a permanent redirect; the not-found page never renders |
| an unknown address | the product's own not-found page with three ways back into the catalogue |

**Journeys**

1. **Filter the catalogue and open a case study.** Open `/work`. The header prints `[ 6 ]`. Open
   the facet control: `All [ 6 ]`, `Branded [ 3 ]`, `Entertainment [ 3 ]`. Choose `Branded`. The
   address becomes `/work?type=branded`, the grid re-renders without a route reload, and the
   toggle reads `Branded` with `[ 3 ]`. Reload the page: the same three films, the same facet,
   the same counts. Open `Constellations`. Its type, its director `Elin Marsh`, its client
   `Verano`, its running time and its month are all printed. The onward link goes to the next
   `Branded` film, not the next film overall.
2. **Switch view mode and keep it.** On `/work` press the floating control to move from `Grid` to
   `List`. Navigate to `/about` and back: still `List`. Reload: still `List`.
3. **Publish, and watch the counts move.** Sign in at `/studio` as `editor@example.com`. Open the
   draft `Low Tide` and send it for review with no director credit: it is refused and every
   missing thing is named at once. Add the credit and the poster and send it for review. Sign out,
   sign in as `publisher@example.com`, publish it. `/work` now prints `[ 7 ]` and `Branded` prints
   `[ 4 ]`.
4. **Embargo holds.** As `publisher@example.com`, set an embargo on `Constellations`. It leaves
   the catalogue, both counts, the home route, the search results and the machine index together.
   Its address answers exactly as an address that never existed. The onward link on the film
   before it skips past it. Sign in as `owner@example.com` and lift the embargo early, typing the
   record's name to confirm: everything returns.
5. **Buy, and buy again.** As `customer2@example.com`, open `/shop` and buy `Beatboard
   Templates`. An order and an entitlement appear at `/account` and the download works. Submit the
   same purchase again with the same idempotency key: still one order, one entitlement, and the
   second response is the first result. Try to buy `Beatboard Templates` a second time as a fresh
   purchase: refused as already owned, with the existing download shown.
6. **The last item.** Two customers buy `Studio Tee`, which has exactly one left. One order is
   created and the other is refused with the sold-out message. Stock never goes below zero and no
   half-written order survives.
7. **Send an enquiry.** On `/contact` choose the `Games` subject: no file control is rendered, and
   a submission carrying an attachment is refused with the policy message and the address
   portfolios actually go to. Choose `Commercials and Branded Content`, complete the form, submit.
   The enquiry is stored and routed before anything else happens, and the confirmation names the
   subject and prints back the address that was typed.
8. **Listen.** On `/podcast` the archive is grouped `SEASON 2` then `SEASON 1`. Start a preview on
   one row: its bars move and the row is marked. Start a preview on another row: the first stops.
   Nothing plays with the page.

**States**

- Every asynchronous surface resolves to exactly one of six states and there is no seventh:
  reserved, where the box is laid out at its final size and filled before content exists;
  skeleton, where structure is rendered without content; partial, where some records have
  resolved; settled; empty, resolved with nothing to show; and failed.
- Every list has an empty state that names what is missing and offers a way on: `No films under
  <TYPE> yet.`, `Nothing filed under <CATEGORY> yet.`, `Nothing matches <TERM>.`,
  `We're currently not hiring, check back another time.`, `The shop is closed!`.
- A container whose emptiness is temporary renders with a message. **A container whose emptiness
  is structural does not render at all**: no heading for a season with no episodes, no block for a
  slate with nothing announced.
- Every page has a loading state, and the first load shows a counter bound to real readiness with
  a hard ceiling after which it gets out of the way. **A counter that sits one short of the end is
  worse than no counter**, so the count continues toward its end and the dismissal is the
  completion. The loading screen never reappears on a route change inside the app.
- A route change that fails leaves the visitor on the route they were reading with an inline
  message. The page they were reading is more useful than an apology screen.
- **Errors never crash the app.** A module that fails renders its own failed state and the rest of
  the route survives. A route that fails keeps its chrome and its onward links.
- A failed list renders the last good list with a staleness notice and a retry, or the failed
  state with a retry if there is nothing to fall back to, never a blank page.
- **A count that cannot be computed renders an empty bracket pair, `[ ]`, and never `0`.** Zero is
  a claim and an empty bracket is an admission.
- The film platform being unreachable produces **one** page-level notice and posters everywhere,
  never one error per tile.
- Every result, every staleness notice and every outage is an inline banner in place. Nothing
  floats over the page to announce itself.

## UI/UX notes

The product should read as a film studio's own paperwork: a near-white neutral sheet, near-black
neutral type set very large and very tight, one signal colour, and a vocabulary of production
marks borrowed from an animation lightbox and a broadcast monitor. The register is editorial and
consumer rather than operational: the subject is seen first, and the interface is the sheet the
subject sits on. No data-grid chrome, no toolbar, no marketing composition standing in for the
working interface.

**Chrome is monochrome and content is colour.** Everything saturated on the page came out of a
film; nothing the interface itself draws is saturated except the one signal.

**Palette by role.** The sheet is a near-white neutral and is the default ground on every route.
The signal is a light, vivid red and is a state rather than a decoration: it marks the current
route, the live open dot, the active facet, the two full-bleed panels and the reserved media box,
and it appears nowhere else. Ink is a near-black neutral and carries all body and display text on
the sheet, and is also the inverted ground. A raised panel and a recessed panel are each a
near-white neutral a step either side of the sheet; the recessed one also draws the table rule and
the disabled control. White is a near-white neutral and is the only text colour on the red and on
the inverted ground. The hairline under a form field is a light neutral. The feed's alternating
reserved card uses a light, soft red, and that pale tint is used nowhere else. Placeholder text is
a mid neutral and is permitted for placeholder text only, never for a value a visitor must read.
The exact values are yours, so long as those relationships and those exclusivity rules hold.

Two text pairings are permitted at body size: ink on the sheet, and white on the signal. Ink on
the signal is permitted at display size only. Body text and its background meet WCAG AA contrast
on every route, and the placeholder grey is the one exception and is never a value.

**Type is one variable family and no second family.** Use `Inter`, with a continuous weight axis
covering at least 300 to 500, one style, installed at image build time and served from the app's
own origin. The fallback stack is `Inter`, then the platform neo-grotesque, then the generic
sans-serif, and metric closeness matters because a mismatched fallback reflows the hero. The
display steps are `175px` over `140px`, `72px` over `57.6px` and `46px` over `36.8px`: **every
display line height is `0.8` of its size**, held exactly, which is what makes a stacked headline
read as one solid mass rather than three lines of text. Body copy is `16.6667px` over `20px` and
the lead paragraph is `24px` over `22.8px`, set tighter than one. **The scale is flat in the
middle and violent at the ends**, with no step between `26.6666px` and `46px` and none between
`72px` and `175px`; filling those gaps produces a conventional article page instead of a title
card. Weight `300` is the light register for the slash separator and de-emphasised labels, `440`
is the text weight, `470` is the emphasis weight for headings and active labels, and `500` is
reserved for display sizes. Numerals are lining with tabular figures available, because indices
and durations stack in columns. Uppercase is applied by style and never by content, so a stored
string is always sentence case.

**Motion is eased, and it is a response rather than an ambient state.** Movement covers most of
its distance almost at once and then settles, which is what makes the product feel immediate at
every scale while nothing appears to snap. **There is not one looping decorative animation
anywhere**: everything that moves does so because the visitor did something or scrolled somewhere,
and then it stops. A drifting background or a pulsing button is a category this design does not
contain. Duration scales with the size of the thing moving - a small label sliding into place is
short, a full-height panel is long - and a colour change always takes the same time whatever is
changing. Only colour, opacity and transform are ever transitioned, plus one reveal clip and one
panel ground; a transition is never declared on every property at once.

The named moments, each of which must exist and none of which may be invented: the leading dot
**scales up from nothing** when its item becomes current or hovered, popping rather than fading,
and building it as a fade loses the whole character of the interaction; a text link keeps **a
second copy of its label just off to the left** behind a clip, and on hover the visible one leaves
while the hidden one arrives, so the word is replaced rather than recoloured; an arrow link's
resting glyph **exits right while its duplicate arrives from the left**; a headline enters **one
word at a time**, punctuation travelling with its word; the footer call to action enters **one
character at a time**; a section **enters once** when its top crosses a fixed fraction of the
window height and never leaves, so scrolling back up replays nothing; children of an entering
section follow one another on a short, deliberately **uneven step** that is transcribed rather
than generated; a picture **resolves outward from its centre** through a mask rather than fading
flat; the footer is **uncovered from behind the page** as the last section scrolls off it; and a
route change **accelerates away** rather than settling, which is the opposite character to
everything else here.

**Reduced motion is honoured by removal, never by shortening.** Smooth scrolling is off and native
scrolling restored; the custom scrollbar is hidden and the native one restored; the custom cursor
is suppressed and the system cursor is never hidden; scroll-driven transforms are not applied and
their elements sit at their end state; text reveals are not applied and the text is fully visible
from first paint; the shop scatter is suppressed and the cards render as a plain grid; nothing
autoplays and every preview shows its poster with an explicit control. Hover transitions remain,
because a deliberate pointer entry is not vestibular motion, and the first-load counter remains
because it is a progress indicator, though its circular reveal becomes a fade.

**Density is comfortable and editorial.** The sheet breathes and a catalogue tile gives its
synopsis room to run to several lines; rows never sit tight enough to read as a spreadsheet.
Everything that is content is square-cornered and flat, and everything that is a control floating
over content is fully rounded and softly blurred behind it. **The two floating catalogue controls
are the only rounded, blurred elements in the whole product**, and that separation is a rule
rather than an accident. Horizontal rhythm is a fraction of the window width rather than a fixed
measure, so the ratio between gutter, navigation stagger and type size is preserved at every
width, and one gutter hook applies the page margin everywhere.

**Layout is a fixed top navigation**: one primary navigation, eight items, one order - Home, Work,
Entertainment, About, Feed, Podcast, Contact, Shop - and the footer repeats the same eight in the
same order, because the two must never diverge. Above the wide threshold the eight sit inline in
the header separated by a lighter-weight slash, with the current route marked by a filled red dot
before its label; below it they collapse behind a wide two-bar toggle and open as a full-window
overlay. Matching is exact: the catalogue must not read as current while a visitor is on a case
study. The search control is the one command-palette-shaped surface, reachable from the header at
the desktop composition and from the overlay below it, opening onto a field that offers the three
most recent publications before anything is typed. **Each page leads with one clear primary
action**, visually distinct from every secondary one.

**Three responsive compositions**, authored at desktop and corrected downward, because desktop is
the composition carrying the eight inline items, the three-column grid and the split shop. The
catalogue grid is three columns, then two, then one. The feed grid is two columns, then two, then
one, and **the handset card loses its excerpt** so the feed does not end up longer on a phone than
on a desktop. The footer's four columns become two and then disclosures. The contact lists go
from three columns to one at tablet. The shop is a fixed two-panel split at desktop and tablet,
each panel scrolling within itself, and stacks at handset. Tile previews and the custom cursor are
desktop only. Display sizes reduce proportionally. **Spacing and type scale continuously between
the thresholds and only composition steps at a breakpoint**, because a gutter that jumps produces
a lurch this design does not have. At a narrow viewport nothing overflows sideways, the layout
holds at any width, nothing is hidden, and every navigation target stays reachable. In a short
landscape window a full-window hero caps at a film ratio rather than consuming the height.
Resizing across a threshold switches composition without a reload: text splits re-run and scroll
ranges recompute.

**Accessibility floors, which are contract rather than taste.** WCAG AA contrast on every text
pairing. Full keyboard navigation with a visible focus ring that is never removed, in ink or in
white on the red. Comfortably sized touch targets, larger again on a coarse pointer for the
controls that are transparent at rest. Labels on every icon-only control. **Meaning is never
carried by colour alone**: the current route carries a dot as well as a colour, the active facet
carries a dot as well as a colour, an invalid field carries text as well as a colour. One
first-level heading per route, no heading level skipped, banner, navigation, main and contentinfo
landmarks, and a skip link as the first focusable element. The two modal regions take focus to
their close control, trap it, return it to the opener, make the background inert and pause the
scroll layer. **Four controls are invisible at rest** - the header address, the client row, the
podcast preview and the client link - and every one resolves on focus as well as on hover,
resolves unconditionally on a coarse pointer and under reduced motion, and is never the only route
to something available nowhere else. The pointer-driven carousel carries real previous and next
controls, arrow key support and an announced position. Every label the custom pointer prints also
exists as an accessible name or a visible label on the control it describes. Slash separators are
hidden from assistive technology, so the navigation does not read as one long list of slashes.
Split text keeps the complete original string as its container's accessible name, hides its
fragments individually, re-splits on resize, and copies as the original string with its spaces.

**What it must not look like.** Not a page dominated by one hue family with no second signal: the
red is a state, and a page washed in it says nothing. Not decoration standing in for content:
every mark in this system is a production mark that means something. Not a marketing composition
where the working interface belongs. Space over dividers, and calm over expressive, everywhere
except the one signal.

## Front-end specification

Unbudgeted detail the visual system depends on. Everything here is appearance and behaviour a
visitor can see; nothing here overrides a rule stated elsewhere.

### The mark vocabulary

Every icon is inline geometry drawn from coordinates in the page. **No icon font and no icon
file.** There are far fewer shapes than it looks, and the same shape is reused rather than
redrawn:

| Shape | Used as |
|---|---|
| the studio wordmark | the header lockup, the first-load screen, and the footer at display size with a descender band |
| the registered mark | beside the header lockup and over the home hero, and as the final shape of the footer wordmark |
| a two-bar toggle | the navigation toggle below the wide threshold, wide and thin so it reads as a typographic mark rather than a button; its close state is the same two bars drawn crossed rather than rotated, so the bar ends stay square |
| one right arrow | every text link with an arrow, its hover duplicate, the footer call to action, the newsletter submit, and the shop product link |
| one play triangle | the player, the carousel navigation, the podcast preview, the podcast row highlight, the legal navigation marker, and, quarter-turned, the facet disclosure. It is never drawn inside a circle |
| one down chevron with a stem | the footer column disclosure, the credits opener, the question and answer disclosure, and the next-case link. Half-turned when open |
| a corner bracket with a diagonal, and a centre cross-hair | the crop-mark overlay |
| a lozenge stamp | the bottom right of the slate hero and the case study hero |
| two boxed meta marks | the record identity mark, which is the studio abbreviation, a rule and an outlined box carrying the position and the year; and the originals mark, an outlined box with a leading filled dot |
| equaliser bars | the podcast row, collapsed to nothing at rest and driven from the playing amplitude |
| one drawn swirl | a single hand-drawn sweep used once as a graphic gesture, stroked in the signal red |

The wordmark is **optically spaced, not evenly spaced**: the gaps between its letters are judged
by eye and are not equal, and a version with even gaps reads subtly wrong at display size. It is
built as solid rectangles with square corners so it can be inverted, masked, scaled and clipped
without a raster asset, and it carries a text alternative on the header instance while the footer
and first-load duplicates are decorative.

The crop-mark overlay prints three concentric labelled rectangles - `Overscan`, `Crop` and
`Action Safe` - plus an aspect-ratio bracket and a zoom label. The three rectangles hold a real
broadcast safe-area relationship, and the inner two are expressed as percentages of the outer so
the relationship survives at any size. The tick marks extending from the rectangle are drawn to
sit exactly outside it whatever its measured size. The whole overlay is decorative and hidden from
assistive technology.

### The dot and the slash

A dot carries state across the entire interface, in two sizes: a small one in the header status
and a standard one before a navigation item, a heading kicker or a meta label. It is filled or a
ring, and it takes the signal red or white. It is **scaled to nothing at rest on both axes** and
scales to full when its parent becomes current or hovered; the ring variant is optically lifted
against its label baseline.

A forward slash does more structural work than any other element: it separates navigation items,
heading kickers from headings, credit roles from names, date parts, and list items. It is set at
the light weight, and it is **a real character in a real element, never a border and never a
pseudo-element**, so it is selectable and copyable. It is marked so assistive technology does not
announce it between every pair of items.

### The compositing device

The most distinctive device in the system is a duplicated content layer that multiplies against
what sits behind it. A block of content is rendered twice, once normally and once inside the
multiplying layer, so that **where a text block crosses the boundary between the sheet and a
full-bleed red panel the text darkens through the overlap instead of switching colour at the
boundary.** The boundary moves with scroll and a colour switch would step. If text visibly snaps
colour as a panel edge passes, this has been built the wrong way.

It appears on the home hero layer, the case study hero, the contact hero foreground, the podcast
banner label, the case footer, the about process cards and the player wrapper. It is capped by
count per route, because multiply blending forces its own layer and it is one of the two most
expensive effects in the product; the other is the blur behind the floating controls, capped at
those two controls.

### Global chrome

**The header** is fixed to the top at every width, full width, transparent over a light route and
veiled where it sits over media. It never hides on scroll and never shrinks. Four regions, left to
right: the lockup linked to the home route; a live status reading `Open (10-6pm)` with a filled
red dot when the studio is open; the location reading `Leeds, England`, which **fades out to
reveal the contact address on hover** and, because that is a hover-only affordance carrying
information, also on focus and unconditionally on a coarse pointer; and the eight navigation items
with slash separators. Below the wide threshold the status, the location and the items are
replaced by the two-bar toggle. On a route whose hero is dark or red every header element inverts
to white and returns to ink on hover, and that inversion is driven by the route rather than by
scroll position.

**The desktop navigation** applies a stagger: each item is offset by a unit multiplied by its
position from the end, so the items are progressively pushed right as the list grows. It is built
as a generated series rather than as one rule per item, works for any item count from one to ten
without adding a rule, and recomputes on resize and on route change.

**The overlay navigation** opens full-window above the header over a veiled ground with a faded
figure behind the list. Items enter staggered. The scroll layer is paused while it is open. It is
dismissed by the close mark, the escape key, a route change and a tap on the ground, and focus
moves to the close control on open, is trapped while open and returns to the toggle on close.

**The footer** is uncovered rather than scrolled to: it sits behind the page and is progressively
revealed as the last section scrolls off it. It carries, in order: the call to action `Let's Talk`
with the contact address as an arrow link, set one character to an element for its reveal; four
columns, `Reach out` with the address and telephone, `Find us` with the four address lines,
`Social` with the network links, and `Nav` with the same eight items in the same order; the
wordmark at display size; a faded, desaturated figure; a newsletter field with an arrow control
lifted to sit on the field baseline; and a legal line carrying the copyright glyph, the legal
name, the year, and three controls separated by slashes: `Site Credits`, `Privacy` and `Up`. Below
the wide threshold the four columns collapse to disclosures.

**The credits overlay** carries a display letter, then role and name pairs in the pattern of a
filled dot, the role, a slash, and the name. The roles are `Site Design`, `Site Development`,
`Creative Director`, `Project Manager`, `Concepts` and `Content Team`.

**The custom pointer** is an enhancement over the system pointer and never a replacement for it.
It carries a label set by whatever it is over: `Scroll to explore` on the home hero, `View
project` on a featured tile, `View case study` on a catalogue or slate tile, `Play (<DURATION>)`
on any video surface carrying that video's running time, `Read more` on a feed card, `View crew`
on the case study hero, and `previous`, `[<INDEX>/<TOTAL>]` and `Next asset` across the thirds of
a carousel. It is suppressed entirely where the pointer is coarse, where there is no pointer, and
under reduced motion, and the system pointer is never hidden in those cases.

**The scrollbar** replaces the native one and is a real control: draggable, clickable in its track
to page, keyboard reachable, and carrying the smoothed scroll position rather than the raw
document position, because the two differ during an eased scroll. It is hidden and the native
scrollbar restored under reduced motion.

**The first-load screen, the preloader,** shows the wordmark and a frame counter counting up to twenty-four, which
is one second of film, with the registered mark revealed through a circular clip that opens from
the centre. The count is bound to real readiness - the typeface, the route's critical data and the
first above-the-fold image - not to a timer, and there is a hard ceiling after which it dismisses
regardless. It never appears on a route change inside the app.

### Scroll behaviour

Scrolling is smoothed: a wheel or a finger sets the page moving and it glides to a stop rather
than halting dead. The layer exposes a paused state, is paused whenever a modal region is open,
restores the exact prior position on resume, and is absent entirely under reduced motion. Anchor
navigation, the browser's find-in-page and focus-driven scrolling all keep working, which means
the layer listens for programmatic scrolling rather than fighting it.

Two mechanisms, built differently and never confused:

- **Threshold reveals.** The great majority. An element sits offset and invisible, crosses a
  trigger point once, transitions to its resting state, and stays there. It never returns, so
  scrolling back up replays nothing.
- **Scrubbed timelines.** A handful, where position is a continuous function of scroll within a
  range **with no transition declared at all**, because a transition on a value that changes every
  frame reads as lag. These are the scrollbar handle; the home featured media, whose two nested
  layers move at different rates so the picture drifts inside its own frame as the frame moves up
  the window; the podcast banner label travelling horizontally over a fixed photograph; the two
  floating catalogue controls, which arrive once the grid begins and retreat at the footer; and
  the shop card pile, which is by a wide margin the most continuously driven thing in the product.

Positions measured for a scrubbed range are cached and recomputed on resize and on route change
only; nothing reads layout inside a frame callback, because doing so with a full catalogue on the
page forces a layout every frame. Only elements currently being driven are promoted, and they are
demoted when they finish. A scroll-driven element whose section is shorter than the window sits at
its end state rather than dividing by zero.

### Route compositions

**Home** is a stack of full-window blocks rather than a reflowing document, which is why its
height barely changes with width: hero, intro, three featured films, the studio panel, clients and
partners, the reel, three news cards, footer. The hero is a full-window silent looping film under
a red multiplying layer, so the darkest parts of the picture stay black and only the lit parts
take the colour, with the wordmark across the foot of the window. The intro carries a kicker
slash, the heading `About The Line`, the split word `Highlights`, and two arrow links, `The Work`
carrying the live catalogue count in brackets and `The Studio`. Each featured film carries the
crop-mark overlay. The studio panel is inverted and carries the split word `The Studio`, the
heading `The lowdown` with the studio description, the heading `Awards & Mentions` with the award
bodies and the publication list, and a pull quote with its attribution. The client row is
invisible at rest and resolves name by name on hover, on focus, unconditionally on a coarse
pointer and unconditionally under reduced motion. The reel is the feature player with the title
word `Reel`. The news block carries the kicker `FROM THE STUDIO`, the split word `News`, and the
three most recently published articles.

**The catalogue** is a header block carrying the facet control at display size and the live total,
then the grid, then two floating controls: the view toggle at the bottom right and a top control
at the bottom left. Opening the facet control reveals the facet list, each option printing its
count between separate bracket elements so the brackets are styled independently and the count
animates inside them, with a slash between options and a `Close` control. The current facet is
marked with a filled dot. A tile's synopsis is **split into one element per rendered line** and
re-split on resize, because a stale split overlaps text at another width.

**A case study** opens on the hero slate, then the intro with `Behind The Line` as its section
title and the definition list, then the editor's chosen modules, then the crew, then the onward
link. Section headings come in pairs of a heading and a split word: `OVERVIEW`, `BEHIND THE
SCENES` with `Making Of`, `PRE-PRODUCTION` with `Beatboards`, `EXPLORATION` with `Concept`, and
`Behind the curtain` with `The Crew`. The hero title is split one element per word, and the
separating slash is its own word element. The carousel is steered by pointer position - the left
third goes back, the right third goes forward, and the centre reports the index over the total -
with the thumbnail strip living in the pointer rather than on the page; it is clipped at rest and
opens on interaction, and it is open upward by a full height so an item can overflow above the
carousel without being cut. Because that navigation is expressed through pointer position, the
carousel also carries real previous and next controls, arrow key support when focus is inside, and
a live region announcing the position.

**The slate** opens on a split title over a darkening figure with the lozenge stamp, a four-item
category line reading `Video Games`, `TV Series`, `Films` and `Interactive Experiences`, then the
proposition block with its routed contacts and the submissions footnote, then the development list
with its heading `DEVELOPMENT SLATE`, the split word `Upcoming`, and a live entry count.

**About** opens on a ten-word headline split one word to an element over a two-layer figure whose
background sits at a low opacity so it reads as a ghost behind the type. Then the studio narrative
under `Behind The Line`, then the process module: three numbered cards, each with a hover title, a
numeral, a card heading, a card title and a paragraph, and a layer that slides over each card as
the block passes up the window. **That layer is scroll-driven, not hover-driven**, so it works on
a touch device with no pointer at all. Then the brandmark block and the showreel, then four
discipline blocks each with a kicker, a heading, copy and an arrow link back into the catalogue
carrying the live count, with a four-item carousel navigation beneath printing a two-digit
identity, a type and a machine-styled path label derived from the type by uppercasing it and
substituting underscores for spaces, so the two can never diverge. The discipline set and the
catalogue facet set are **different vocabularies and must not be unified**. Then the squad, from
the one people directory filtered to current staff.

**The feed** opens on the featured article as a full-bleed image tinted with the signal and the
title set in white at the largest display step, then the index grid under the heading `What's
going on` and the split word `Feed`.

**The podcast** opens on the show title split across two lines, its premise naming both hosts, a
`Listen` link, the circular show badge, and a banner label travelling over a full-bleed
photograph, then the archive under `Archives` with the split word `Episodes`.

**The shop** does not scroll as a page at desktop or tablet: it is a fixed two-panel composition
with each panel scrolling within itself. The left panel carries the display heading `Digital` and
`Products`, the count in brackets, the subtitle and the scattered card pile. The right panel is
the editions wordmark in a script face at display size in white on the red, overflowing the panel
to the right, with two lines of copy and the drop state beneath.

**Contact** opens on the kicker `Contact us` and the display line `Let's talk` over a layered
parallax hero built from several independently driven planes, then the general address and the
telephone number, the four address lines as one link to a map, then the routed enquiry directory
grouped as `People`, `Agency` and `Follow us`, then `Opportunities`, then `Ask Us` with the six
questions and answers. The display line is the heading and the kicker sits under it in the
heading order, correcting the source's inverted levels.

**Privacy, terms and storage** are document routes with a section navigation, long-form headings
and body copy, no media and no motion beyond the scrollbar and the footer.

### Depth

Eleven stacking values resolve to six bands and the build must not invent a seventh: content that
is **explicitly grounded**; content raised, which is the default for anything overlapping; the
second content layer, where the duplicated multiplying layer sits; a third and a top content
layer; sticky within a section; the crop-mark overlay; the scrollbar; the header; the navigation
overlay; and the first-load screen with the pointer above everything.

### The governing idea, typography and iconography

**The governing idea.** The product is designed as a film studio's own paperwork. Every ornament
in the system is a piece of studio furniture rather than a flourish, and the build treats that
vocabulary as load-bearing.

**Typography** is one variable family and nothing else, at the scale given in `## UI/UX notes`.
The shape of that type scale is the design: the display steps hold their ratio exactly, the
middle of the scale is flat, and the ends are violent.

The display letter is one element for a whole string, keyed by its first letter, which is why
the route display letter carries `.letter-C`, `.letter-L`, `.letter-T`, `.letter-H` or
`.letter-M` according to the word it sets.

**Iconography** is the shape list above, and the whole set is inline geometry. The play triangle
seen as a play control, as the facet disclosure and as the accordion marker is **one triangle
turned different ways**, never three shapes. The same is true of the arrow and of the chevron.

### Component architecture and the rendering strategy

Three layers, and the direction of knowledge between them is a rule rather than a style.
**Primitives** - the dot, the slash, the link, the arrow link, the pill control, the picture, the
player, the crop-mark overlay, the meta mark, the accordion and the display letter - know about
nothing above them. **Modules** - the hero, the catalogue tile, the feed card, the episode row,
the process card, the slate row, the carousel, the slider, the crew list and the contact list -
know only about primitives. **Routes** know about modules, primitives and their own data.

**A module never fetches.** A route fetches and passes down. That is what lets the same tile
appear on the home route, in the catalogue and on the slate without three variants of it drifting
apart.

**The rendering strategy** is server-first: every public route renders its critical content on the
server and the media, the previews and the scroll behaviour attach afterwards.

**Two things are global and exactly one of each exists.** One store holds the identity of whatever
is currently playing, because the exclusive-playback rule cannot be enforced by components that do
not know about each other. One scroll driver owns the smoothed layer, publishes a normalised
position, and offers exactly two subscription kinds matching the two mechanisms above: a threshold
subscription that fires once, and a range subscription that receives a progress value each frame.
Range subscribers are batched into one frame callback and write only composited properties.

Ownership of the rest: route data belongs to the route until the route changes; the catalogue
facet and the view mode belong to the address, mirrored to storage, permanently for the mode and
per address for the facet; scroll position per route is keyed by history entry for the session;
the audio mute preference is stored permanently; the two overlays are open until closed; a
customer session belongs to the origin; and a dirty form's contents belong to the form, mirrored
so that nothing typed is lost.

**Every module is individually fallible.** A module that throws renders its own failed state and
the rest of the route survives; a route that throws keeps its chrome. A failure is reported with
the module name, the route and the record identity.

### The class contract and the machine-readable hooks

The class names are structural and carry no brand, so the build keeps them: a block, a
double-underscore element, a double-hyphen modifier. These hooks are contract and must appear
exactly as written, because behaviour elsewhere in this brief is described by them:

`.acetate`, `.gutters`, `.bg-loading`, `.base-image--loaded`, `.router-link-active`,
`.router-link-exact-active`, `.nav-item--translated`, `.button-pill`, `.button-pill--list`,
`.button-pill--no-dot`, `.dot--8`, `.dot--15`, `.dot--red`, `.dot--white`, `.dot--filled`,
`.dot--border`, `.director-note-toggle--visible`, `.work-filter__btn`, `.work-filter__count`,
`.filter-status`, `.letter-C`, `.letter-L`, `.letter-T`, `.letter-H`, `.letter-M`,
`.scroll-layer`, `.scroll-layer--scrolling`, `.scroll-layer--stopped` and
`.font-active`.

The last four replace the reference's own scroll-layer and typeface-ready class names, which
carried a library's name; the states they mark are unchanged, and the name is the build's to keep
stable rather than a vendor's to dictate.

### The named surfaces and what drives them

| Surface | Block | Driven by |
|---|---|---|
| the scrollbar handle | `scrollbar__handle` | scrubbed, every route, every width |
| the navigation stagger | `nav-item`, `nav-item--translated` | scrubbed, desktop only |
| the footer uncover | `footer__sticky-inner` | scrubbed, every route |
| the picture fade | `base-image__img` | threshold, wherever pictures are |
| the film fade | the player and the tile preview | threshold |
| a hero's layers | the route's own hero inner elements | threshold, on home, about, contact and slate |
| the home featured media | `home-featured-work-asset__wrapper` and `home-featured-work-asset__fig-wrapper`, two nested wrappers moving at different rates so the picture drifts inside its own frame | scrubbed, home only |
| the leading dot | `dot--15` | threshold, every route |
| the floating controls | `button-pill`, `button-pill--list`, `button-pill--no-dot` | scrubbed, the catalogue only |
| the process cards | `module-process__item-hover` and its acetate duplicate | scrubbed, about only. **It is scroll-driven and not hover-driven** whatever its name suggests, so it moves on a touch device with no pointer at all |
| the podcast banner | `podcast-episodes__fig-inner` and its acetate span | scrubbed, podcast only |
| the shop card pile | `shop-gumroad__fig` | scrubbed, shop only, and the most continuously driven element anywhere in the product |
| the case footer | `case-footer__content--main` and its acetate span | threshold, a case study only |
| the director note | `director-note-toggle`, `director-note-toggle--visible` | threshold, a case study only |
| the about hero background wash | `about-hero__bg`, at a low opacity so it reads as a ghost behind the type | threshold |
| the home hero colour layer | `home-hero__layer` with its acetate duplicate | threshold |

An element crossing its threshold once is a state change. An element with many distinct positions
across a scroll is genuinely scrubbed. Anything between the two is a threshold reveal that
happened to be sampled mid-transition, and it is built as a threshold reveal.

### Fluid rather than stepped, and unusual widths

Horizontal rhythm is a fraction of the window width and does not step at a threshold. Only
composition changes at a threshold; spacing and the type scale are **fluid** between them rather
than **stepped**, because a gutter that steps produces a visible jump.

Unusual widths and **orientation** are first-class rather than an afterthought. In a short
landscape window a full-window hero caps at a film ratio rather than consuming the height. Above
the wide threshold content caps and centres, with a maximum measure on text blocks. Below the
narrowest ordinary width the layout holds, nothing is hidden, and horizontal overflow is
prohibited.

### The copy deck

Strings are stored in sentence case and cased by style. Everything below is pinned copy.

| Element | String |
|---|---|
| route title pattern | the page, then the qualifier where there is one, then `The Line Studio` |
| the podcast route title | `Animation Podcast The Rostrum and Grill / Ear Candy / The Line Studio` |
| the header status | `Open (10-6pm)` |
| the header location label | the city and the region, `Leeds, England` |
| the copyright line on a hero or a player | `The Line`, then the copyright glyph, then the year in Roman numerals, `MMXXVI` |
| the footer legal line | the copyright glyph, `The Line Studio Ltd`, `2026` |
| the header and footer call to action | `Let's Talk` |
| footer columns | `Reach out`, `Find us`, `Social`, `Nav` |
| networks in the footer | `YouTube`, `Instagram`, `TikTok`, `X`, `Facebook`, `LinkedIn` |
| networks on the contact route | the same six plus `Vimeo`, which the footer omits. The difference is a per-surface flag on one record, never two lists |
| legal controls | `Site Credits`, `Privacy`, `Up` |
| credits roles | `Site Design`, `Site Development`, `Creative Director`, `Project Manager`, `Concepts`, `Content Team` |
| the home intro | the heading `About The Line`, the split word `Highlights`, the arrow links `The Work` and `The Studio` |
| the home studio panel | `The Studio`, `The lowdown`, `Awards & Mentions`, `Clients + Partners`, and a pull quote with its attribution prefixed by a hyphen |
| the home news block | the kicker `FROM THE STUDIO` and the split word `News` |
| crop-mark labels | `Overscan`, `Crop`, `Action Safe`, `100%`, `[ 16:9 ]` |
| catalogue controls | `All`, `Branded`, `Entertainment`, `Close`, `Grid`, `List`, `Reset`, `Top` |
| catalogue tile labels | `Type` and `Director`, set in the signal red with the value after a slash |
| case study headings and their split words | `OVERVIEW`; `BEHIND THE SCENES` with `Making Of`; `PRE-PRODUCTION` with `Beatboards`; `EXPLORATION` with `Concept`; `Behind the curtain` with `The Crew` |
| case study player titles | `Play`, and `BTS` on the secondary player |
| the slate | the split title `The Line / Entertainment`, the categories `Video Games`, `TV Series`, `Films` and `Interactive Experiences`, the heading `DEVELOPMENT SLATE`, the split word `Upcoming`, the label `Status` |
| the slate routing line | `For enquiries about The Line Entertainment please contact:` |
| the slate footnote | `*we're unfortunately unable to accept unsolicited submissions for IP development` |
| about disciplines | `Commercial`, `The Hype Video`, `Music`, `Entertainment`, each linking back into the catalogue with the live count |
| about carousel navigation | identities `01`, `02`, `03`, `04`, types `Branded`, `Cinematics`, `Music Videos`, `Entertainment`, and a machine-styled path label derived from the type by uppercasing it and substituting underscores for spaces, so the two can never diverge |
| about hero meta | the city and the country, `Leeds, UK`, with the label `The Studio` |
| about squad label | a filled dot then `Director & Art Director` |
| feed | the kicker `Featured`, the link `Read On`, the heading `What's going on`, the split word `Feed`, the categories `Studio News` and `Entertainment`, and the outbound link `Read The Article` |
| podcast | the link `Listen`, the meta `5 Episodes`, the headings `Archives` and `SEASON 2`, the split word `Episodes`, the control `Preview` |
| shop | `Digital`, `Products`, `One-time purchase, lifetime updates. Go go go!`, the editions wordmark `editions`, `LIMITED RELEASE ITEMS FROM The Line CREW.`, `GET YOURS BEFORE IT'S GONE - LITERALLY!`, and `The shop is closed!` |
| contact headings | `Contact us`, `Let's talk`, `General enquiries`, `Address`, `Reach Out`, `People`, `Agency`, `Follow us`, `Opportunities`, `Ask Us` |
| contact list titles | `Contact`, `REPS`, `SOCIALS`, and the subtitles `Commercials/Branded Content`, `Head of Development / IP`, `Games`, `USA / Northpoint`, `Contact Northpoint`, `Networks` |
| the overseas representation agency | `Northpoint`, listed with three names and their addresses, and a telephone number |
| contact jobs | the display `Join`, `The Line`, and the empty line `We're currently not hiring, check back another time.` |
| the questions | `Who is The Line?`, `What does your process look like?`, `How much for an animation?`, `How can I work at The Line?`, `Do you offer work experience or internships?`, `Can I send you my script or film idea?` |
| the answer carrying the legal position | `Thanks so much for thinking of us for your creative project, but we do not accept any kind of creative submissions. All of our ideas and stories are developed internally and for legal reasons we cannot consider any unsolicited creative material (scripts, synopses, sketches, etc).` |
| credit roles, in industry order | `Director`, `Producer`, `Production Manager`, `Art Director`, `Animation Lead`, `Clean-up Lead`, `Compositing Lead` |

Two spellings in the source material are corrected here rather than reproduced: the routing line
reads `enquiries`, and the slate statuses use `Web series` in both of the places the source wrote
it two ways.

## Technical requirements

Server-rendered HTML with hydrated islands, using **Astro** for the frontend with **Fastify**
serving the HTTP API on the same origin under `/api`, and **PostgreSQL** as the datastore. Every
public route renders its critical content on the server: the header, the headings, the copy, the
metadata and the media boxes at their final sizes. Media, previews and scroll behaviour attach
afterwards, so a visitor with scripting unavailable gets a readable, navigable product with
posters instead of previews, and the catalogue, the feed and the podcast archive all stay usable.
The corollary binds the text reveals: the text is present and visible in the served markup and the
reveal is applied afterwards, never the reverse.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing service
available in this environment is PostgreSQL, and reaching for anything else is a contract
violation.

- PostgreSQL is reached at `DATABASE_URL`. The app reads it from the environment and never
  hardcodes a host or a port.
- The app's own public address and port are read from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`.
- Authentication is email and password with bearer tokens, implemented in the app. There is no
  external identity provider. Passwords are hashed.
- `GET /api/health` returns `200` once the app is ready, and not before.
- Configuration comes from the environment. **Startup fails loudly on a missing or malformed
  configuration value rather than defaulting**, because a default that quietly disables the
  embargo condition is unthinkable.
- One structured log line per event, carrying a request identifier generated per request, the
  route, the principal kind where there is one, the outcome and the duration. **The request
  identifier is returned to the client** in a response header and in every error body, so a report
  can be traced rather than guessed at. Addresses are logged hashed; message bodies, tokens and
  attachment contents are never logged at all.
- No credential, API key or administrative token appears in anything the browser downloads.
- Every response carries the standard security headers, including a strict transport policy and a
  content-type policy that forbids sniffing, a referrer policy of same-origin, and a permissions
  policy denying camera, microphone, geolocation and payment.
- Responses are compressed, with the modern encoding negotiated with the client and a fallback
  where it is not accepted.
- **No debug surface is reachable in the running product**, and dependencies are patched rather
  than pinned and forgotten, because the commonest attacker here is an opportunistic scanner
  looking for a known vulnerability rather than anybody interested in this studio.
- No response header or error body names the framework, the platform, a version, a table, a query
  or an internal address, and no error body ever carries a stack trace.
- Authentication and enumeration paths take the same time whatever the outcome.
- **No route accepts a field named for a card, at any depth**, and no request body reaching the app
  may match a card pattern. The product never receives, stores, transmits or logs a card number by
  any path.
- Uploads are typed by inspecting their content rather than by their declared type or their
  extension, are size-limited per path, are stored under a generated name outside anything the app
  serves, and are not readable until they have been checked. Image metadata, including location
  data, is stripped on ingest.
- **Observability is a requirement rather than a nicety.** What is instrumented: every request,
  every scheduled run, every authorization denial and every business event - a publication, an
  enquiry, a subscription, an order, a download. Alongside the logs the app keeps a run record per
  scheduled job and a record of each denial, and **alerting is on absence as well as on error**:
  a scheduled job that has missed several of its intervals must be visible from its own records,
  because a job that quietly stops produces no error at all.
- Every state-changing request carries a token bound to the session and verified on the server,
  so a **cross-site forged request** cannot act on somebody's behalf. No state-changing operation
  is reachable by a safe method: the public read surface accepts no other method at all, which
  makes the classic mistake structurally impossible rather than merely avoided.
- No third-party script is loaded on any public route. No tag manager, no chat widget, no
  advertising, no analytics vendor.
- Dependencies install at image build time. There is no network at runtime.

**The zero-asset substitution guide.** Every asset is generated rather than shipped: **no image,
video, audio or typeface binary is part of this task**. The principle is that a substitution is a
recipe rather than a placeholder: each one below produces something shippable, and each is honest
about falling short of a real frame, which is why every box is at its true size and every colour
relationship is intact so that dropping real artwork in later changes how the product looks and
nothing else. A deterministic generator seeded from a record's identity produces a placeholder
for any asset reference with no file, so the same record always yields the same picture. A
placeholder fills with the signal red, or the pale tint on the feed, overlays two or three large
soft radial fields at low alpha positioned from the seed, applies a neutral generated grain, draws
the crop-mark overlay where the surface calls for it, and adds a centred elliptical silhouette at
low alpha for a portrait rather than attempting a face. A tile preview is a generated silent loop
built from that picture with two of its fields drifting on a short cycle, rendered at three sizes
so the rendition ladder is exercised. A feature player's source is a generated slate carrying the
title, the duration and a counting timecode, which is enough for playback, seeking and duration
formatting to be real. An episode is a generated tone at the recorded duration with a varying
amplitude envelope, so the loudness pass and the amplitude bars have something to work on. A
caption track is generated carrying the timecode, so caption presence and caption absence are both
real states. The grain is drawn by the app rather than loaded as a texture.

## Data model

Thirty-eight tables, and five principles decide the shape of all of them. **All timestamps are
UTC.** Every amount is an integer in minor units with an
explicit lowercase currency code, and no floating point value goes anywhere near a price. Every
media column is a reference to the asset table; no table stores bytes. A fact is stored once: a
person, a client and a type each exist in one table and are referenced everywhere else.
Publication is a state on a record, never a second published copy of it.

> **Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
> not a secret. Hash it as normal; the exact literal must work at login, and it must be written
> into `/app/USER_README.md` alongside each account so a grader can sign in.

### Editorial

- `studio`: one row. `name`, `legal_name`, `description`, `address_lines`, `postcode`, `phone`,
  `general_email`, `founding_year`, `timezone`, `opens_at`, `closes_at`, `reel_duration_s`,
  `reel_year`, `featured_article_id`. The featured article is a reference held here rather than a
  flag on each article, which is what makes featuring a second article unfeature the first.
- `case_study`: `slug` unique, `title`, `display_title`, `synopsis`, `type_id`, `frame_rate`,
  `released_on`, `duration_s`, `poster_asset_id`, `preview_asset_id`, `film_asset_id`, `state`,
  `published_at`, `scheduled_for`, `embargo_until`, `rights_start`, `rights_end`, `territories`,
  `manual_position`, `featured_position`, `is_hero`, `version`. `display_title` exists because a
  published slug is immutable and a title can still change afterwards.
- `case_module`: `case_study_id`, `position`, `kind`, `payload`. The body of a case study is an
  ordered mixed sequence, so it is rows rather than columns; one nullable column per module field
  would produce a table of mostly-empty columns with no way to order or repeat anything.
- `work_type`: `label` unique, `slug` unique, `position`. The catalogue facets.
- `article`: `slug` unique, `title`, `standfirst`, `body`, `category_id`, `state`, `published_at`,
  `scheduled_for`, `poster_asset_id`, `outbound_url`, `outbound_host`, `outbound_checked_at`,
  `outbound_ok`, `related_case_study_id`.
- `article_category`: `label` unique, `slug`, `position`.
- `slate_entry`: `slug` unique, `title`, `logline`, `format_id`, `stage_id`, `position`,
  `visibility`, `case_study_id` nullable.
- `slate_format` and `slate_stage`: `label` unique, `position`. Together they render the status
  line, which is why it cannot be free text.
- `discipline`: `label`, `body`, `position`, `carousel_type_label`.
- `process_card`: `position`, `numeral`, `hover_title`, `heading`, `title`, `body`.
- `faq`: `position`, `question`, `answer`, `surface`.
- `award` and `publication`: `label`, `url`, `position`.
- `network`: `label`, `url`, `position`, `show_in_footer`, `show_in_contact`. The footer and the
  contact route show different sets, and the difference is these two flags rather than two lists.
- `job`: `title`, `contract_type`, `location`, `apply_email`, `state`, `closes_at`.
- `redirect`: `from_path` unique, `to_path`, `kind`. Resolved before the not-found path. Chains
  resolve to a bounded depth and a cycle stops the app at startup rather than looping at runtime.

### People and organisations

- `person`: `full_name`, `slug`, `is_staff`, `staff_from`, `staff_until`, `bio`,
  `portrait_asset_id`.
- `credit_role`: `label` unique, `industry_position`. The industry order credits print in.
- `case_credit`: `case_study_id`, `person_id`, `credit_role_id`, `position`, unique on the first
  three.
- `staff_role`: `person_id`, `credit_role_id`, `position`.
- `client`: `name`, `slug`, `may_be_named`, `position`.
- `case_client`: `case_study_id`, `client_id`, `position`.
- `contact_route`: `subject`, `person_id` nullable, `email`, `group`, `position`,
  `accepts_attachments`.

Two people may not be merged carelessly: a merge repoints every credit and removes the loser
inside one transaction, and a normalised name is checked on write so a duplicate is warned about
before it exists.

### Podcast

- `show`: one row. `name`, `premise`, `artwork_asset_id`, `banner_asset_id`, `directory_urls`.
- `episode`: `season`, `number`, `guest`, `duration_s`, `audio_asset_id`, `preview_asset_id`,
  `preview_start_s`, `preview_end_s`, `waveform`, `published_at`, `state`, unique on `season` and
  `number` together. Season and episode are stored as integers and formatted zero-padded at
  render. The archive's season grouping is computed from this flat list rather than stored nested,
  because a flat list with two integers sorts correctly and survives an episode moving season.
- `show_host`: `person_id`, `position`.

### Commerce

- `product`: `slug` unique, `kind` which is `digital` or `physical`, `title`, `subtitle`,
  `price_minor`, `currency`, `format_label`, `size_bytes`, `licence_summary`, `scatter_seed`,
  `state`.
- `product_version`: `product_id`, `version`, `released_at`, `changelog`, `file_asset_id`.
- `drop`: `name`, `opens_at`, `closes_at`, `state`.
- `drop_item`: `drop_id`, `product_id`, `stock_total`, `stock_reserved`, `stock_sold`.
- `customer`: `email` unique and case-folded, `password_hash`, `created_at`, `last_seen_at`.
- `customer_order`: `customer_id`, `reference` unique, `state`, `total_minor`, `currency`, `placed_at`,
  `refunded_at`, `idempotency_key` unique.
- `order_line`: `order_id`, `product_id`, `product_version_id`, `quantity`, `unit_price_minor`.
- `entitlement`: `customer_id`, `product_id`, `order_line_id`, `granted_at`, `revoked_at`, unique
  on `customer_id` and `product_id` together.
- `download_token`: `entitlement_id`, `token_hash`, `issued_at`, `expires_at`, `used_at`.
- `shipment`: `order_id`, `carrier`, `tracking_ref`, `state`, `shipped_at`, `delivered_at`.
- `drop_notification`: `email`, `drop_id`, `created_at`, `confirmed_at`, `notified_at`.

### Audience and operations

- `subscriber`: `email` unique and case-folded, `state` which is `pending`, `confirmed`,
  `unsubscribed` or `bounced`, `confirmed_at`, `unsubscribed_at`, `source`, `consent_basis`. A
  subscriber captured from a drop notification has not consented to the newsletter, which is what
  `source` is for.
- `enquiry`: `name`, `organisation`, `email`, `subject`, `budget_band`, `timing`, `message`,
  `attachment_asset_id`, `routed_to`, `state`, `spam_score`, `received_at`.
- `asset`: `kind`, `provider_ref`, `width`, `height`, `duration_s`, `byte_size`,
  `poster_asset_id`, `alt_text`, `processing_state`, `checksum`, `seed`. A signed address is never
  stored, only the reference it is minted from, because a stored expired address is the commonest
  cause of a broken media page.
- `editorial_event`: `actor_kind`, `actor_id`, `action`, `entity_type`, `entity_id`, `field`,
  `before`, `after`, `request_id`, `occurred_at`. One row per changed field.
- `staff_user`: `person_id`, `email` unique, `role`, `state`, `password_hash`, `last_login_at`.
- `session`: `subject_kind`, `subject_id`, `token_hash`, `issued_at`, `expires_at`,
  `rotated_from`, `revoked_at`.
- `page_view`: `route`, `referrer_host`, `composition`, `occurred_at`.
- `job_run`: `job`, `started_at`, `finished_at`, `outcome`, `counts`.

### Migrations and integrity

Every schema change ships as a reversible migration. Anything a running release reads is changed
by adding the new column, backfilling it, writing both, moving the reads, and only then removing
the old one, so a release can be rolled back without the database being rolled back with it.
Integrity is the database's job rather than the application's: foreign keys are declared and
enforced there, and every enumerated column is either a reference to a lookup table or a
constraint, never a bare string trusted by convention.

### Derived rather than stored

The catalogue total and every facet count; a film's position in the current ordering; the season
grouping; a duration's rendered form; the open state and the instant of its next change; the facet
vocabulary; the article category vocabulary; and the crew module, which is rendered from the
credits rather than stored as a module payload.

### Invariants, as properties of the running system

- **The public read condition.** A case study is publicly readable only when its state is
   published, its embargo instant is absent or past, its rights start is absent or past, and its
   rights end is absent or future. The same condition produces the list, the total and every
   per-facet count, and it is part of the query that selects records rather than a step applied to
   the results.
- **A withheld client name is absent from the response**, not hidden in the page.
- **One entitlement per customer and product.** A second purchase of the same product by the same
   customer creates no second entitlement and no second order.
- **Availability is total stock minus sold minus reserved, and it never goes below zero.** Two
   simultaneous purchases of the last item: exactly one is accepted and the other is rejected.
- **An order submitted twice with the same idempotency key produces exactly one order**, one set
   of lines and one entitlement, and returns the original result the second time.
- **A mutation and its log row commit together or not at all**, and the log is append-only.
- `season` and `number` together identify an episode uniquely.
- A slug is immutable once a record has been published; a changed slug leaves a redirect behind
   and is never reused for a different record.
- Deleting a person who holds credits is refused. Deleting a product that has entitlements is
   refused. Deleting a work type that a case study references is refused.
- Every customer-owned row carries its customer's identity and is filtered by the authenticated
  customer inside the query that selects it.
- Foreign keys are declared and enforced in the database rather than in application code, and
  every enumerated column is either a reference to a lookup table or a database-level
  constraint, never a bare string trusted by convention.

### Seed data

Nine case studies, six of them publicly readable:

| Title | Type | Director | Client | State |
|---|---|---|---|---|
| `Constellations` | `Branded` | `Elin Marsh` | `Verano` | published |
| `The Summit` | `Branded` | `Cato Bellweather` | `Kessel`, who may not be named | published |
| `Jungle All Stars` | `Entertainment` | `Priya Sandoval` | `Halberd` | published |
| `A Hundred Years of Sweet` | `Branded` | `Jonas Vik` | `Tessellate` | published |
| `Mistfall` | `Entertainment` | `Ruth Okonjo` | `Norwind` | published |
| `Kerb Kings` | `Entertainment` | `Milo Ferreira` | `Bright Anchor` | published |
| `Nightjar` | `Branded` | `Elin Marsh` | `Moraine` | published, embargoed until a future instant |
| `Paper Lantern` | `Entertainment` | `Jonas Vik` | `Fenwick` | published, rights ended in the past |
| `Low Tide` | `Branded` | `Priya Sandoval` | `Verano` | draft |

The counts that follow are `6` in total, `3` under `Branded` and `3` under `Entertainment`.

`Constellations` carries `Elin Marsh` as Director, `Halle Brandt` as Producer and `Tomas Vey` as
Art Director. `Halle Brandt` is no longer staff: she is absent from the squad and still credited.

The feed carries `Inside the Ink Room` in `Studio News`, featured, with its own body; `Nine
Questions on Hand Drawn Animation` in `Entertainment`, a link-out to the host `spool.example`; and
`The Rostrum Turns Three` in `Studio News`. `Season Four in the Room` is scheduled ahead and is
not found.

The slate carries `Amber & Wilder`, `The Great Piton`, `NEW WRLD`, `Freight` and `Housemates` as
announced, `Kerb Kings` in production and linked to its case study, and `The Ends of Peck` as
confidential and served nowhere.

The podcast is `The Rostrum and Grill`, hosted by `Rae Alvarsson` and `Nils Croft`, with five
published episodes across two seasons and one whose audio is still processing.

The shop carries `Rostrum Brush Pack` at `1200`, `Beatboard Templates` at `1000` and `Lightbox Starter Kit` at
`2500`, all in `usd`. `Rostrum Brush Pack` has versions `1.0` and `1.1`. The drop
`Editions 01` is open, with `Studio Tee` at a total stock of `3` and `2` sold, leaving exactly one,
and `Crop Mark Print` at a total of `5` with `5` sold. The drop `Editions 02` is announced with a
future opening instant.

`customer@example.com` holds an entitlement to `Rostrum Brush Pack`. `customer2@example.com` holds
nothing.

The studio record carries the name `The Line Studio`, the legal name `The Line Studio Ltd`,
`Leeds`, `England`, the founding year `2013`, and opening hours that render `Open (10-6pm)`.

**Seeding must be idempotent - restarting the app must not duplicate rows.**

## Constraints

- One studio. There is no second tenant, no organisation switcher and no per-tenant configuration.
- No card details, no payment provider, no checkout hosted anywhere else, and no framed payment
  surface of any kind.
- No mail delivery. Enquiries, subscriptions and drop notifications are stored and shown in the
  back office; nothing is actually sent.
- No object store, no content delivery network, no cache tier, no queue broker, no search service,
  no secret store and no error-reporting service. PostgreSQL and the app's own process are all
  there is.
- No third-party analytics, no advertising pixel, no tag manager, no chat widget, no cookie
  banner.
- No external network calls at runtime, of any kind, to anything.
- No native application, no installable app shell, no push notifications.
- No comments, no likes, no follower graph, no direct messages.
- No federated sign-on, no directory provisioning, no policy engine, no multi-stage approval
  graph, no delegation, no multi-region residency, no per-tenant key management and no
  tamper-evident chained audit. Each of those would add machinery a studio of this size would
  never operate, and unoperated machinery is worse than none.
- No client portal and no work-in-progress review area.
- The product must stay responsive with a few hundred case studies, a few hundred articles, a few
  hundred episodes and a few thousand orders. It is not a system of record for millions of rows.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`:
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
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
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

Field names are exact. A list endpoint returns a top-level JSON array. A successful call returns
the named resource or shape; an invalid or unauthorized call is rejected as a client error, never
a server error and never a silent success. Bearer authentication is required on everything except
the health check, the public reads and the sign-in endpoints.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `{"status"}` |
| `POST /api/auth/login` | `{"email","password"}` | `{"access_token","role","expires_at"}` |
| `POST /api/auth/signup` | `{"email","password"}` | `{"access_token","role","expires_at"}` for a customer |
| `GET /api/catalogue` | `?type=&view=&order=` | array of `{"slug","title","type","directors","clients","synopsis","duration_s","released_on","year","position","poster_url","preview_url"}` |
| `GET /api/catalogue/counts` | `?` none | `{"total","facets":[{"slug","label","count"}]}` |
| `GET /api/case-studies/<slug>` | none | `{"slug","title","type","frame_rate","duration_s","released_on","synopsis","directors","clients","modules","credits","next_slug"}` |
| `GET /api/slate` | none | array of `{"slug","title","logline","format","stage","position","case_study_slug"}` |
| `GET /api/feed` | `?category=` | array of `{"slug","title","standfirst","category","published_at","outbound_host"}` |
| `GET /api/feed/<slug>` | none | `{"slug","title","standfirst","body","category","published_at","outbound_url","outbound_host","related_case_study_slug"}` |
| `GET /api/podcast` | none | `{"show":{"name","premise","hosts","episode_count"},"episodes":[{"season","number","identity","guest","duration_s","preview_url"}]}` |
| `GET /api/shop` | none | `{"products":[{"slug","title","price_minor","currency","format_label","size_bytes","licence_summary","scatter_seed","version"}],"drop":{"name","state","opens_at","closes_at","items":[{"product_slug","stock_available"}]}}` |
| `GET /api/contact` | none | `{"general_email","phone","address_lines","routes":[{"subject","person","email","accepts_attachments"}],"jobs","faqs"}` |
| `GET /api/studio-state` | none | `{"open","hours_label","next_change_at"}` |
| `GET /api/search` | `?q=` | `{"groups":[{"kind","count","results":[{"kind","slug","title"}]}]}` |
| `POST /api/enquiries` | `{"name","organisation","email","subject","budget_band","timing","message"}` | `{"id","subject","routed_to","email"}` |
| `POST /api/subscribers` | `{"email","source"}` | `{"state"}` |
| `POST /api/orders` | `{"product_slug","idempotency_key"}` | `{"reference","state","total_minor","currency","lines","entitlement_ids"}` |
| `GET /api/orders` | none | array of the authenticated customer's orders |
| `POST /api/downloads` | `{"product_slug"}` | `{"url","expires_at","version"}` |
| `GET /api/studio/records` | `?kind=&state=` | array of back-office rows for the authenticated staff user |
| `POST /api/studio/records/<id>/transition` | `{"command","note","confirm_title"}` | `{"id","state","failures"}` |
| `PATCH /api/studio/records/<id>` | the changed fields and `{"version"}` | `{"id","version"}` |

**Versioning and compatibility.** The API carries its version in the path. Within a version only
additive change is permitted: a new field may appear, and an existing field may never change type
or disappear. A breaking change mints a new version, and the previous one keeps working alongside
it.

The publication gate returns every failure at once in `failures`, never only the first. A stale
`version` on a patch is rejected as a conflict with the current record returned. A record a
requester may not see and a record that never existed produce the same response, including the
same headers.

### No mocks

The named backing service is the fact. Any of the following is a contract violation however good
the interface looks: an in-memory array of case studies, an on-disk file used as the store, a
hardcoded list of counts, a count computed from a literal instead of from the rows, a seed script
that writes to something other than PostgreSQL, an entitlement asserted in the interface without a
row behind it, or a stock figure held anywhere except the row it belongs to. The app's UI and its
own responses can only ever reflect what lives in PostgreSQL, never substitute for it.

## Definition of done

A visitor can open the catalogue, filter it to one category and open a case study, and every count
on the page agrees with the films they can actually see. A film under embargo or past its rights
window is unreachable at every address and absent from every count, list, search result and
machine-readable index, and its neighbour's onward link skips it. A customer can buy a digital
pack, download it, and download it again after a new version lands; nobody can reach anybody
else's download; and the last item in a drop sells exactly once.
