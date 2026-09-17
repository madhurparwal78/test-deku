# Meridian Cloud

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser, write `amber` into `us-central` on the
consistency console, read `amber` back from `eu-west`, and send a contact-sales enquiry that an
administrator then finds on the desk, without hitting an error page. A different stranger must not be
able to read a draft product's page, its art or its datasheet by any means: the bucket holds those
bytes, the app decides who may read them, and a link that reaches the bytes without asking the app
does not count as protection.

## Overview

The app serves a public site for the cloud platform `Meridian Cloud` and a private desk with its own
sign-in for the staff who publish it. The site's job is to make one technical claim credible to an
engineering buyer: that the flagship relational database, `Tessera`, stays strongly consistent across
regions because its clocks are synchronized.

A visitor reads the published product pages with no account. A visitor browses the products as a flat
index, through the three seeded product families, and through the six seeded industry solutions. A
visitor opens a product to read its claims with its highlights rail and its generated card art. A
visitor downloads a datasheet from its card. A visitor looks through the card art of every published
product in one grid. A visitor exercises the consistency console: writing a value in one named region
and reading it back from another, reading the synchronized-clock uncertainty band, and severing and
restoring a link between regions. A visitor ends by submitting the contact-sales form.

The site serves four audiences, and every public surface is built for one of them: data architects,
who arrive asking whether one database can stay strongly consistent across regions and are answered
by the flagship product route with the console; engineering leaders, who ask whether it scales and
stays up and are answered by the highlights rail with the service level; platform teams, who are
answered by the industry solutions; and executives with analysts, who are answered by the customer
proof wall. No audience is served by a surface the brief does not describe.

Staff work at the desk in three roles. An editor drafts a product page and attaches its art and its
datasheet; a publisher publishes it and returns it to draft; an administrator reads the stored
contact-sales submissions and the page-view log. An unpublished product is absent from every public
surface and its address answers not found.

It is not a store, a signup funnel or a chatbot: nothing is bought, no visitor account exists, and the
assistant calls no language model. The genuinely hard part is the console's ordering rule, that a read
from any region never returns a value older than a write already acknowledged anywhere.

## User roles

| Role | Account | Read | Write |
|---|---|---|---|
| `visitor` | none | every published product, family, industry, datasheet and art piece; the console | a console write, read or partition; a contact-sales submission. **Cannot** read a draft, its art or its datasheet, an enquiry or the page-view log, and **cannot** reach the desk. |
| `editor` | seeded | everything a visitor reads, plus every product in both states at the desk | draft a product, edit it, attach art and a datasheet, save. **Cannot** publish, **cannot** return a product to draft, and **cannot** read an enquiry or the page-view log. |
| `publisher` | seeded | everything an editor reads | everything an editor writes, plus publish and return to draft. **Cannot** read an enquiry or the page-view log. |
| `administrator` | seeded | everything a publisher reads, plus the stored enquiries and the page-view log | everything a publisher writes. |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not
authorization: a direct API call from an `editor` session to any `publisher`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged. The same holds for a `publisher` session calling an `administrator`-only endpoint, and for
any caller with no session calling a desk endpoint.

Signup is closed. A `visitor` holds no account and nothing on the public side creates one, so the app
carries no registration form, no registration endpoint and no password reset. The three desk roles are
seeded:

| Role | Address | Password |
|---|---|---|
| `editor` | `editor@example.com` | `deku-demo-pw-2026` |
| `publisher` | `publisher@example.com` | `deku-demo-pw-2026` |
| `administrator` | `administrator@example.com` | `deku-demo-pw-2026` |

Write each address with its password into `/app/USER_README.md`.

## Core features

### Draft products stay unreadable

1. A `draft` product is absent from every public surface: the product index, every family, the
   industry proof cards, the datasheet library, the art gallery, the home product rail, the header
   search overlay, the mega-menu, and the related row of any other product. Returning a published
   product to draft removes it from every one of those at once.
2. A `draft` product's address, `/product/{slug}`, answers not found, exactly as an address naming no
   product at all does. It never answers forbidden, so the existence of an unpublished page is not
   disclosed.
3. The bytes of an art piece or a datasheet belonging to a `draft` product answer not found to a
   request carrying no valid desk bearer token, exactly as the product address does, and are served to
   a request carrying one, so the composer can show a draft's own art. The bucket is not readable
   without credentials, so no link to it reaches the bytes either. Returning a product to draft stops
   both at once for every caller without a desk session.
4. No query parameter on a public endpoint makes it answer with a `draft` product.

### Launch obligations

5. Every content image carries alternative text describing what it depicts. A decorative image, the
   brand gradient bar, the grain over the card art, the product marks and the customer wordmark
   tiles, declares itself decorative with empty alternative text. Publishing is refused where a
   product's art piece carries an empty description.
6. The app offers a cookie choice on a visitor's first public surface: an `Accept` control, a
   `Decline` control and a link to the privacy page. Until the visitor chooses, the app sets no
   analytics cookie and no preference cookie; the only cookie a choice sets is the one recording it.
7. The app remembers the choice, so the band does not return on the next public surface or after a
   reload. A dismissed promo banner is remembered for the session without a cookie.
8. Every public route carries its own page title and its own description meta tag, and no two public
   routes share either. A product page's title carries the product name and its description carries
   the product summary.
9. Every public route carries a canonical link to its own address.
10. The app records a page view for every public route it serves, with the route as requested (for
    example `/product/tessera`) and the time. The log carries no cookie and no visitor identifier, so it
    records every view whatever the cookie choice. Only an administrator reads it.

### The consistency console

11. The app serves the consistency console at `/console`, and embeds the same console on the home
    route and on `/product/tessera`.
12. The console names five regions: `us-central`, `eu-west`, `asia-south`, `sa-east` and
    `au-southeast`. A request naming any other region is refused as invalid.
13. A console write takes a region, a key and a value, and answers with a commit timestamp and
    `uncertainty_ms`, the clock uncertainty it waited out. `uncertainty_ms` is always greater than
    zero, and the write does not answer before that many milliseconds have passed. Every console
    timestamp is an ISO 8601 UTC string with milliseconds, for example `2026-09-16T09:06:10.123Z`. A
    write missing its key or its value is refused as invalid and names the missing field.
14. A console read takes a region, a key and a mode of `strong`, `bounded` or `exact`, and answers
    with the value, its timestamp, its staleness and a latency figure. The staleness is a whole number
    of milliseconds by which the returned value trails the latest acknowledged write for that key, `0`
    for a `strong` read, and the latency figure is a whole number of milliseconds. Any other mode is
    refused as invalid.
15. A read in mode `strong` never returns a value older than any acknowledged write, whichever region
    serves it. Writing in one region and reading from any other returns the value just written.
16. A read in mode `bounded` takes a staleness bound, a whole number of milliseconds above zero, and
    never returns a value staler than that bound. A read in mode `exact` takes a timestamp and returns
    the value committed at or before it. A `bounded` read with no bound, or a bound that is not a whole
    number above zero, and an `exact` read with no timestamp, are refused as invalid and name the
    missing or malformed field.
17. The partition control severs one named region from the rest and restores it. Severing a region
    already severed, or restoring one already joined, changes nothing and answers the same five
    regions.
18. A write against a severed region is refused, and the refusal says the region will not accept a
    write it cannot safely agree on. A write on the majority side still commits, and reads there stay
    correct.
19. Restoring a severed region re-syncs it to the majority value, and no console state is ever readable
    as corrupted or forked.
20. The console exposes its state as text as well as by colour: the current value per region, the
    clock uncertainty and the partition status.
21. The console resets to its seeded state on request, with every region unsevered. A reset while no
    region is severed answers the same seeded state and changes nothing.

### Products and families

22. The app serves the flat product index at `/product` with a heading, a count line reading the
    number of published products, a filter bar and a card grid.
23. The app serves one published product at `/product/{slug}` with its eyebrow, its heading, its lead,
    its summary, its highlights rail, one claim band per highlight line, its card art, its datasheet
    where it has one, and a related row.
24. The related row carries up to three other published products sharing a family, ordered by sort
    index ascending. A product sharing no family with another shows no related row.
25. The app narrows the product index by name on a partial, case-insensitive match, and by family to
    the products carrying it. The family filter takes the family slug, for example `?family=databases`,
    and a slug naming no family answers a top-level empty array.
26. The app orders the product index by name ascending where the sort is `name`, and by most recently
    added first where the sort is `recent`. A sort other than `name` or `recent` is refused as invalid.
27. The app carries the active name filter, family filter and sort in the address, so reloading that
    address applies the same three again.
28. A product-index filter matching nothing answers with a top-level empty array, and the index shows
    its empty message with a way to clear the filter.
29. The app serves the three seeded families at `/family`, one card each carrying the family name, its
    standfirst and its published count.
30. The app serves one family at `/family/{slug}` with its head, its standfirst, its editorial intro and
    the published products carrying it. A family holding no published product answers with an ordinary
    empty surface, never not found, because the family exists.

### Industry solutions

31. The app serves the six seeded industries at `/solution` as a grid filtered by chips reading `All`
    and each industry name, each card carrying its name, its proof stat line and its named customer.
32. The home route's industry explorer swaps its right panel to the selected industry's proof card
    without loading another address.

### Datasheets and the art gallery

33. The app serves the datasheet library at `/datasheet`, listing the datasheets of published products
    plus the three platform datasheets that belong to no product.
34. A datasheet card carries a cover generated from the document's own first page, its page count and
    its file size in megabytes to one decimal place. The cover is never a separately uploaded picture,
    and a datasheet registered with no picture of any kind still shows one.
35. A datasheet download carries a `Content-Disposition` of `attachment` and a filename derived from the
    title, so `Meridian Platform Overview` downloads as `meridian-platform-overview.pdf`.
36. The app serves the art gallery at `/gallery` as one grid over the card art of every published
    product, paging at 24 pieces from page `1` and narrowable to one family by its slug. A page past the
    last, or a slug naming no family, answers a top-level empty array; a page below `1` is refused as
    invalid.
37. The app streams every art piece and every datasheet from the bucket itself, resolving the owning
    product's state as it reads, rather than handing the browser a link to the bucket.

### Contact sales and the assistant

38. The app takes a contact-sales submission of a full name, a work email, a company, a region of
    `Americas`, `Europe` or `Asia Pacific`, and an interest of `Evaluation`, `Migration` or `Pricing`,
    with an optional message, and answers with an enquiry identifier.
39. The app refuses as invalid a submission whose work email is not an address, whose name is shorter
    than 2 characters, whose region or interest is not one listed above, or whose message runs past 1000
    characters, and the refusal names the field it is about.
40. The app stores every submission. Only an administrator reads the stored submissions, newest first;
    no visitor surface and no editor or publisher session reads one back.
41. The app serves the assistant surface at `/ask` with its greeting, four suggestions and a field
    holding at most 500 characters, and the counter reads how many of those 500 are entered. Typing or
    pasting past 500 keeps the first 500. The assistant sends a query nowhere and answers nothing.

### The desk

42. The app serves the desk sign-in at `/desk/login`, and a signed-out `/desk` shows that card rather
    than the entry list.
43. Every `/api/desk/` endpoint denies a request carrying no bearer token or a malformed one as
    unauthorized, serving nothing.
44. A sign-in failure reveals nothing about whether the address exists: a wrong password and an unknown
    address are refused identically.
45. The desk lists products in both states at `/desk`, with the name, families, state, art count and
    last-edited columns, a badge on each row reading `Live` or `Draft`, and three filter controls whose
    counts come from `GET /api/desk/products/counts` as the keys `all`, `published` and `draft`. Each row
    of `GET /api/desk/products` carries `art_count`. Selecting a row opens that product's detail pane
    beside the list without leaving `/desk`, and the pane's `Open in composer` control opens
    `/desk/product/{id}`.
46. Entering the composer creates no row. A product row comes into existence on the first
    `Save draft`, and an upload target is issued only for a product that already has an id. An uploaded
    datasheet is registered with its title, and the app reads its page count from the stored document
    at registration; a registered object key the bucket does not hold is refused as invalid.
47. A created product always lands in state `draft`, whatever the request body says.
48. Only a publisher or an administrator may publish or return a product to draft. An editor's publish
    or return-to-draft is denied as unauthorized and leaves the product's state unchanged.
49. A publish is refused as invalid when a required field is empty, when the web address is already
    held, when the web address is a reserved segment, when the product carries no art piece, or when an
    art piece carries an empty description. The required fields are the product name, the web address,
    the eyebrow, the summary and the claim body. A draft may be saved incomplete, and may be saved with
    a web address another product already holds; the refusal comes at publish.
50. The reserved web addresses are `desk`, `api`, `media`, `product`, `family`, `solution`, `datasheet`,
    `gallery`, `console`, `ask`, `contact`, `privacy`, `terms` and `404`.
51. One published product holds a given web address at any time, so two publishes naming the same
    address never both succeed.
52. The composer fills the web address in from the product name, and stops once the editor has edited
    the address by hand.
53. The app refuses as invalid a product name of one or two characters and a summary longer than 240
    characters, at save and at publish. An empty name is an incomplete draft rather than a short one,
    so it saves and is refused only at publish.
54. Returning a product to draft asks for confirmation before it takes effect.
55. Only an administrator reads the page-view log at `/desk/views`, which shows a count per public route
    and a list of recent views with their route and time. An editor or a publisher is denied it.
56. Signing out of the desk returns the sign-in card, and the ended session's token is refused
    afterwards.

### Standing pages

57. The app serves the privacy page at `/privacy` and the site terms at `/terms`, and the footer of
    every surface reaches both.
58. The app renders the platform's own not-found surface for any unmatched path, inside the global
    header and footer.

## User flow

| Route | What it shows | Auth |
|---|---|---|
| `/` | Home: hero, product rail, consistency console, industry explorer, customer proof, closing band | none |
| `/product` | Product index: heading, count line, filter bar, card grid | none |
| `/product/{slug}` | One product: hero, highlights rail, claim bands, art strip, datasheet, related row | none |
| `/family` | Family index: three cards with name, standfirst, published count | none |
| `/family/{slug}` | One family: head, standfirst, intro, its published products | none |
| `/solution` | Industry index: six industries filtered by chips | none |
| `/datasheet` | Datasheet library: cover cards, page count, file size, download control | none |
| `/gallery` | Art gallery: one grid over every published product's card art | none |
| `/console` | The consistency console on its own route | none |
| `/ask` | Assistant surface: greeting, four suggestions, a capped field | none |
| `/contact` | Contact-sales form | none |
| `/privacy` | What the platform records, with the cookie choice explained | none |
| `/terms` | Site terms | none |
| `/desk/login` | Sign-in card | none |
| `/desk` | Products in both states, with three filter counts | editor, publisher, administrator |
| `/desk/product/new` | Composer, empty | editor, publisher, administrator |
| `/desk/product/{id}` | Composer, loaded | editor, publisher, administrator |
| `/desk/enquiries` | The stored contact-sales submissions, newest first | administrator |
| `/desk/views` | A count per public route and a list of recent views | administrator |

Eighteen journeys, each of which must work end to end:

1. A visitor arriving for the first time reads the cookie choice band, presses `Decline`, and finds the
   band gone on the next public surface and after a reload, with no analytics cookie set.
2. A visitor opens `/`, `/product` and `/product/tessera` in turn and finds a different page title and a
   different description on each, the product page's title carrying `Tessera`.
3. A visitor opens `/console`, writes the value `amber` into `us-central`, reads the key back from
   `eu-west` in mode `strong`, and receives `amber` with a latency figure and a staleness of `0`.
4. A visitor severs `asia-south`, attempts a write against it and reads the refusal, writes into
   `eu-west` instead and sees it commit, then restores `asia-south` and sees it rejoin.
5. Signed out, a visitor opens `/product/halyard` and receives the not-found surface with the heading
   `We cannot find that page`, and finds `Halyard` in neither the product index, the `Networking`
   family, the art gallery nor the header search.
6. A visitor opens `/product/tessera`, reads the eyebrow `Tessera database`, the heading
   `One database, every region, one truth`, the highlights rail and the claim bands, then follows a card
   in the related row to another published product sharing a family.
7. A visitor opens `/product`, reads the count line `8 products`, types `slip` into the name field and
   sees `Slipstream` as the only card left.
8. A visitor chooses the family `Databases` in the filter bar, copies the address, reloads it, and finds
   the same family filter still applied.
9. A visitor chooses the sort `Name, A to Z` and sees the cards ordered alphabetically, then chooses
   `Recently added` and sees the newest first.
10. A visitor types `zzzz` into the name field, reads the empty message, and presses `Clear filter`.
11. A visitor opens `/family/databases`, reads the family name `Databases`, its standfirst and its
    editorial intro, then follows `Families` in the header to `/family` and reads the three cards with
    their published counts.
12. A visitor selects `Telecommunications` in the home route's industry explorer and sees the right
    panel swap to its proof card with its stat line and its named customer.
13. A visitor opens `/datasheet`, reads the card for `Meridian Platform Overview` with its cover, its
    page count and its file size, and downloads it.
14. A visitor opens `/gallery`, narrows it to `Databases`, opens one piece and reads its alternative text
    and the name of the product it belongs to.
15. A visitor submits the contact-sales form with a full name, a work email, a company, the region
    `Europe` and the interest `Evaluation`, and reads the success banner with its enquiry identifier.
16. An editor opens `/desk/login`, submits `editor@example.com` with the password `deku-demo-pw-2026`,
    lands on `/desk`, presses `New product`, types the name `Kestrel`, sees the web address fill in as
    `kestrel`, fills the eyebrow, the summary and the claim body, saves the draft, attaches one art
    piece with a description, saves again, and finds no `Publish` control available to the editor.
17. A publisher signs in as `publisher@example.com`, selects `Kestrel` in the list, reads its detail
    pane, presses `Open in composer`, presses `Publish` and reads the
    message `Published. It is live now.`, then presses `Return to draft`, confirms, and reads
    `Returned to draft. It is no longer public.`
18. An administrator signs in as `administrator@example.com`, opens `/desk/enquiries` and reads the submission
    of journey 15, then opens `/desk/views` and reads a count for `/product` with the time of a recent
    view.

## UI/UX notes

Accessibility is a requirement, not an aspiration: the site is fully operable by keyboard and screen
reader. Body text and supporting copy meet WCAG AA
contrast against their grounds, and the light cool neutral is never used for copy a visitor must read.
Every interactive element is reachable in document order and the focus ring is never removed, only
restyled. Every navigation target is comfortably sized for a finger. One `banner`, one `main` per route
and one `contentinfo`, with navigation landmarks for the primary nav and the product sub-nav; one `h1`
per route, and headings descend without skipping a level. Every content image carries alternative
text and every decorative one declares itself decorative; every icon-only control carries an accessible
name. Dialogs and overlays close on Escape and return focus to what opened them, and a destructive
action asks for confirmation before it takes effect. Nothing is carried by
colour or motion alone: every console state and every badge pairs its colour with a word. Under a
request for reduced motion, sliding, rotation and auto-advance stop, opacity fades stay and shorten,
and every control still works.

North star: a visitor should understand, in the first moment, that this is a calm and serious platform
making one precise technical claim, and should be able to test that claim on the page rather than take
it on faith.

Palette by role. The page ground of every surface is a near-white neutral, and section bands sit on a
near-white neutral one step below it. Inset wells sit one step below that, and hairlines and skeletons
one step below again. Card and control borders are a near-white neutral. Body text and headings take a
deep neutral; supporting copy, captions and every metadata line a visitor reads take a mid cool
neutral; disabled text alone takes the same mid cool neutral one step lighter; placeholders take a light
cool neutral. The footer sits on the
page ground like every other surface.

A single mid, vivid blue marks everything a visitor can act on and everything currently selected, and
nothing inert wears it except the console's commit-wait bar; pressed and emphasised states take the
same blue darker, and so does the text of a link or button pointed at. The button hover fill and the chip fill are a near-white cool neutral, and selected
navigation takes that one step deeper. The four brand hues, a light, vivid blue, a mid, soft green, a
light, vivid red and a mid, vivid orange, appear in the wordmark, the gradient bar, the product marks
and the thin underline under the active header label, and none of them fills a button or colours a
link's text. Success takes the mid, soft green and marks only a completed action or a good state: a
confirmed console write, the fill of a `Live` badge, a success message's border, and the throughput
meter's consistency tick. A success banner sits on a near-white neutral fill with a mid, soft green left
border, and a failure banner on a near-white warm neutral fill with its text in the mid, vivid red. Failure takes a mid, vivid red and marks only a refusal: a validation failure, a
refused console write, or a failure message or banner. The mid, vivid orange is the warning accent and
marks the `Draft` badge, an unfinished state rather than a wrong one. Every badge sets its word in a
deep neutral on its fill. The product commits to the light scheme.

Type is a humanist geometric sans set calmly, in two families and no more: `Manrope` for display headings, product titles and card titles, and
`Inter` for body, navigation, badges, filter controls and metadata. Both are named with a fallback
stack already showing, and no font file ships with the build.

Shape reads as one soft product radius on cards and on the largest control group, tighter inside
buttons and text fields, softer on feature tiles, a full pill on chips, filter toggles and the rounded
primary button, and a circle on icon buttons. One decorative asymmetric radius appears on the active
side-rail item of a product route and nowhere else.

Density reads as spacious, on an eight-step rhythm, with a generous reading measure. The default gutter
and card padding are one step of that rhythm and the band separation is double it. The fixed header
holds a constant height across every route. Bands are separated by air rather than by lines: the
change of ground between two neighbouring bands is the only separation drawn between them, and nothing
is drawn in the seam.

Motion character is eased and brief. Five easing characters carry the whole product: a default for
colour and transform, a decelerating entrance, an accelerating exit as an element leaves, an expressive
expand and collapse for panels, and the skeleton's own slow loading pulse. The named moments are a
fade in from below as a band enters the viewport, the product rail advancing one card, the mega-menu
panel dropping open with its chevron turning, a desk message entering on a short decelerating travel,
the skeleton shimmer sweeping a waiting surface, the brand gradient turning a half-turn once on load
behind the flagship product mark and then holding, and the console's three: its uncertainty band
narrowing, its commit-wait bar filling, and a severed region's links going dashed. Nothing is
scroll-scrubbed, and the skeleton shimmer is the one animation that loops for as long as its surface
waits.

Components carry their states rather than only their resting look: a control shows resting,
pointed-at, pressed, focused and unavailable, and a field carries its label above with any failure
message directly beneath. Unavailable is signalled by more than colour. The craft holds up close: a card, a control and a console
state each read as finished at rest, pointed-at and pressed, with nothing left in a placeholder look.

The product is responsive across five breakpoints. At a narrow viewport nothing overflows sideways,
every navigation target stays reachable, and rows of cards fold to a single column.

Design against these failures: a surface dominated by one hue family with no second signal; a band
rendered empty rather than omitted; a spinner standing in for content that is already drawn; a console
whose proof is a colour with no word; and a marketing composition standing where the working desk
belongs.

## Technical requirements

Build the public surfaces as server-rendered pages: every public route arrives as HTML carrying its
content on first paint, and only the consistency console, the product rail and the industry explorer
hydrate as islands. Build the server as `Fastify` and the client as `SolidStart` in TypeScript. The
signed-in desk may hydrate freely.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database,
cache, queue, object store, identity provider or mail vendor - the only backing services available in
this environment are `PostgreSQL` and `MinIO`, and reaching for anything else is a contract violation.
No search service and no edge functions. No third-party runtime call except the font service the two
named families are declared against.

Read every connection value from the environment and never hardcode a host or a port:

| Variable | What it carries |
|---|---|
| `DATABASE_URL` | the `PostgreSQL` connection |
| `STORAGE_ENDPOINT` | the `MinIO` endpoint |
| `STORAGE_BUCKET` | the bucket every object is written into |
| `STORAGE_ACCESS_KEY` | the `MinIO` access key |
| `STORAGE_SECRET_KEY` | the `MinIO` secret key |
| `APP_PUBLIC_URL` | the origin the app is reachable at |
| `APP_PUBLIC_PORT` | the port the outside world uses |

`PostgreSQL` and `MinIO` are already running and reachable at those variables. Do not download,
install, compile or start a copy of either.

**Sessions.** `POST /api/auth/login` takes an email and a password and answers with a bearer token
that expires after 12 hours. Every `/api/desk/` endpoint requires it. Passwords are stored hashed.
`POST /api/auth/logout` ends the session, and its token is refused afterwards.

**Object WRITES go straight to the store.** `POST /api/desk/uploads` answers with a target inside the
bucket that expires after 15 minutes and is scoped to one object key, carrying `url`, `method`,
`headers` and `object_key`. The browser puts the bytes at that target and the desk then registers the
object key, an art piece through `POST /api/desk/art` and a datasheet through `POST /api/desk/datasheets`.
A target is issued only for a product that already has an id.

**Object READS are mediated by the app, and that choice is part of the contract.** The bucket is not
publicly readable. Art and datasheet bytes are served at `GET /api/media/art/{art_id}` and
`GET /api/media/datasheets/{datasheet_id}`, each of which resolves the owning product's state, and
for a `draft` product the caller's desk bearer token, before streaming a byte. A link handed to the browser that reaches the bucket directly would leave a draft
product's bytes readable by anyone holding it, so reads are not served that way.

**What must hold when two staff work at once.** Two simultaneous publishes naming the same web address
must not both succeed. One published product holds a given web address at any time. A publish whose web
address is already held is refused and changes nothing, and this holds when two attempts arrive at
once: exactly one wins. Saving one product twice creates no second product.

**What must hold in the console.** No read in mode `strong` returns a value older than any acknowledged
write, whichever region serves it. A commit is acknowledged only after the clock uncertainty it reports
has passed, so timestamp order is real-time order. A write against a severed region is refused rather
than accepted and reconciled later. No console state is ever readable as corrupted or forked.

**Performance the product owes.** These are budgets, not aspirations. The largest piece of content on
the home surface paints in under 2.5 seconds on a fourth-generation mobile connection. An interaction
paints its next frame in under 200 milliseconds. No surface shifts its layout by more than a tenth of
a viewport as content arrives. The compressed JavaScript the home surface delivers stays under 180KB.
No more than three requests block first paint on the home surface.

**Media weight is the product's largest risk, and three rules contain it.** The console, the product
rail and any below-fold generated art are deferred until after first paint. Only the hero mark with the
first row of cards loads eagerly, and every image below the fold loads lazily. Every generated image
declares its intrinsic width and height and is delivered with a candidate set and a sizes hint, so no
layout shift occurs as it arrives.

`GET /api/health` answers with the body `{"status": "ready"}` once the app has its database and its
bucket. Log one structured line per request on stdout carrying the method, the path, the status and the
duration. Never log a credential, a bearer token or the body of a contact-sales submission. The page-view
log is application data, not the request log.

Derive rather than store: the per-family published count, the `art_count` on the desk list, the file
size on a datasheet card, the console read's staleness and latency, and the per-route view count.
Seeding must be idempotent: restarting the app must not duplicate rows.

## Data model

Thirteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

`accounts` carries `id`, `email` (unique), `password_hash`, `role` (`editor`, `publisher` or
`administrator`) and `created_at`.

`sessions` carries `id`, `account_id`, `token_hash`, `created_at`, `expires_at` and `ended_at`, so a
signed-out or expired token is refused.

`products` carries `id`, `slug`, `name`, `eyebrow`, `heading`, `lead`, `summary`, `claim_body`, `state`
(`draft` or `published`, lowercase), `families` (zero to three), `featured` (boolean), `sort_index`
(integer), `service_level`, `regions_available` (integer), `created_at` and `updated_at`. `slug` is
unique among published products.

`families` carries `id`, `slug`, `name`, `standfirst` and `intro`. Three rows, seeded, never written
from the desk:

| slug | name | standfirst | intro |
|---|---|---|---|
| `databases` | `Databases` | `Relational and analytical stores that keep one answer everywhere.` | `Every database here is managed, replicated across regions and read through the same consistency guarantees.` |
| `networking` | `Networking` | `The paths your data travels, kept short and private.` | `Traffic stays on the platform's own network from the edge to the region that serves it.` |
| `analytics` | `Analytics` | `Questions asked of data where it already lives.` | `Analysis runs beside the data, so a report reads the same rows the application just wrote.` |

`highlights` carries `id`, `product_id`, `line` and `sort_index`: the lines of a product's highlights
rail, one claim band per line.

`art_pieces` carries `id`, `product_id`, `object_key`, `alt_text`, `seed`, `width`, `height` and
`sort_index`.

`datasheets` carries `id`, `product_id` (null for a platform datasheet), `object_key`, `title` and
`page_count`, the page count read from the stored document when it is registered or seeded; its byte
size is never stored.

`industries` carries `id`, `slug`, `name`, `stat_line`, `customer_name` and `sort_index`. Six rows,
seeded.

`customers` carries `id`, `name` and `sort_index`. Eight rows, seeded.

`console_writes` carries `id`, `region`, `key`, `value`, `commit_timestamp` and `uncertainty_ms`.

`partitions` carries `id`, `region` and `severed` (boolean).

`sales_enquiries` carries `id`, `name`, `work_email`, `company`, `region`, `interest`, `message` and
`received_at`.

`page_views` carries `id`, `route` and `viewed_at`.

Object keys follow these schemes exactly:

| What | Key |
|---|---|
| an art piece | `products/<product_id>/art/<sha256_of_bytes>.<ext>` |
| a product's datasheet | `products/<product_id>/datasheet/<sha256_of_bytes>.pdf` |
| a platform datasheet | `platform/<datasheet_id>/<sha256_of_bytes>.pdf` |

The seed holds nine products, eight `published` and one `draft`, created in `sort_index` order so the
most recently added seeded product is `Halyard`, then `Foundry`:

| name | slug | state | families | featured | sort_index | art | datasheet |
|---|---|---|---|---|---|---|---|
| `Tessera` | `tessera` | `published` | Databases | yes | 1 | 3 | `Tessera Technical Overview` |
| `Slipstream` | `slipstream` | `published` | Networking | yes | 2 | 2 | none |
| `Beacon Enterprise` | `beacon-enterprise` | `published` | Analytics | yes | 3 | 2 | none |
| `Quarry` | `quarry` | `published` | Databases, Analytics | yes | 4 | 2 | none |
| `Bastion` | `bastion` | `published` | Networking | yes | 5 | 2 | none |
| `Anvil` | `anvil` | `published` | Networking, Databases | yes | 6 | 2 | none |
| `Lattice` | `lattice` | `published` | Analytics | no | 7 | 2 | none |
| `Foundry` | `foundry` | `published` | Databases | no | 8 | 2 | none |
| `Halyard` | `halyard` | `draft` | Networking | no | 9 | 3 | `Halyard Technical Overview` |

That gives `Databases` 4 published products, `Networking` 3 and `Analytics` 3.

Each seeded art piece takes as its `seed` the product slug followed by its sort index (`tessera-1`), is
drawn at 1200 by 900, and carries the alternative text
`<product name> card art, generated field <sort index> of <art count>`, for example
`Tessera card art, generated field 1 of 3`.

`Tessera` carries the eyebrow `Tessera database`, the heading `One database, every region, one truth`,
the lead `A fully managed relational database with strong consistency across regions, backed by synchronized clocks.`,
the service level `99.999%` and 5 regions available. Every other seeded product carries its own name as
its heading.

`Tessera` carries eight highlight lines, one claim band each, at these sort indexes:

| sort_index | line |
|---|---|
| 1 | `Reads always reflect the latest write` |
| 2 | `Synchronized clocks with atomic and satellite time` |
| 3 | `Correct through network partitions, never corrupted` |
| 4 | `Massive transaction scale with no consistency trade` |
| 5 | `Synchronous multi-region replication` |
| 6 | `Tunable read staleness when you want it` |
| 7 | `Automatic failover with zero data loss` |
| 8 | `Five-nines availability, multi-region` |

Three platform datasheets, owning no product: `Meridian Platform Overview`, `The Global Network` and
`Consistency Explained`.

Five console regions, seeded unsevered: `us-central`, `eu-west`, `asia-south`, `sa-east` and
`au-southeast`.

Six industries, in this order:

| name | slug | stat line | customer |
|---|---|---|---|
| `Retail` | `retail` | `9 of the top 10 retail companies build on Meridian Cloud` | `Vessel Foods` |
| `Financial services` | `financial-services` | `Nearly 90% of the largest global banks run regulated workloads here` | `Cobalt Bank` |
| `Healthcare` | `healthcare` | `Clinical records stay in region, with one consistent read` | `Truenorth` |
| `Telecommunications` | `telecommunications` | `Issue resolution cut from hours to minutes across a national network` | `Harrowgate` |
| `Government` | `government` | `Residency guarantees met in 5 regions at once` | `Marea Global` |
| `Manufacturing` | `manufacturing` | `Plant telemetry at 1 million writes a second, ordered globally` | `Stonecraft` |

Eight customers on the proof wall, in this order: `Harrowgate`, `Vessel Foods`, `Cobalt Bank`,
`Truenorth`, `Stonecraft`, `Threadly`, `Marea Global`, `The Gazette`.

The testimonial card carries the quote
`We put agents to work across our network and cut issue resolution from hours to minutes.` attributed
to `Anjali Rao`, `SVP of Engineering for Network Automation`, `Harrowgate`.

## Front-end specification

### Type scale

Eleven steps, each as size / line-height / weight:

| Step | Size / line-height | Weight | Role |
|---|---|---|---|
| body | `16px` / `24px` | 400 | paragraphs, list items |
| body-medium | `16px` / `24px` | 500 | emphasised body, navigation |
| body-tall | `16px` / `26px` | 500 | button labels in body context |
| small | `14px` / `24px` | 400 | captions, sub-navigation |
| dense | `13px` / `24px` | 400 | metadata, footnotes |
| lead | `18px` / `28px` | 400 | hero sub-copy |
| title | `20px` / `28px` | 500 | card and section titles |
| heading | `24px` / `32px` | 500 | route sub-heads, the assistant greeting |
| display | `28px` / `36px` | 400 | hero and product headings |
| micro | `12px` / `16px` | 400 | eyebrows, chip labels |
| button | `14px` / `36px` | 500 | the control label, with no text transform |

`Manrope` carries the display, heading and title steps. `Inter` carries every other step. Both are
declared against the fallback stack `system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif`,
which is already showing before either family arrives, so text is never invisible.

### Information architecture

The information architecture is four shells, and every route declares which one it uses as its
page-type attribute, a `data-page-type` attribute on the page's outer element. `landing` is full-width bands with no side rail, and the home route alone uses it.
`product` is a left sticky sub-nav with a right highlights rail, used by every product route. `tool` is
a centred single-purpose surface with minimal chrome, used by the console and the assistant. `index` is
a filterable card grid, used by the product index, the family index, the industry index, the datasheet
library and the art gallery. A route's page-type attribute selects its shell, so no route invents a
layout of its own.

### Scaling, typography and the effects vocabulary

Scaling is in fixed steps rather than viewport-derived units: the body root is a fixed size and the
eleven type steps above are the whole typography of the product, with no step invented outside them.

The effects vocabulary is seven entries, and nothing outside it is drawn: the resting card's hairline
with no shadow; the hover raise on a card or a button; the deeper dropdown shadow; the brand gradient
bar and its half-turn on load; the edge-fade mask that softens the product rail and the customer wall
at both ends; the skeleton shimmer over a waiting surface; and the focus ring.

### Accessibility values

Body text and supporting copy meet a contrast of at least 4.5 to 1 against their grounds. A navigation
target is at least 44 by 44 on its shorter side. The first focusable element on every route is a
`Skip to content` link into the `main` landmark.

### Layout and breakpoints

Five breakpoints, named `sm`, `md`, `lg`, `xl` and `xxl` in ascending order. The content column is
centred with a gutter that steps at each breakpoint. The grid is twelve columns, capping at a maximum
content width and centring beyond the widest tier.

Column counts: the product grid is three cards across at `xl`, two at `md`, one below; the family index
is three in a row at `lg`, stacked below `md`; the datasheet library is four across at `xl`, three at
`lg`, two at `md`, one below; the gallery masonry runs one column below `md`, two at `md`, three at
`lg`, four at `xl`; the industry grid is three at `lg`, two at `md`, one below; the product rail shows
one card with part of the next below `md`, and three at `lg` and above.

Three structural changes across the tiers: the primary navigation collapses into a drawer below `md`;
a product route's left sub-nav becomes a dropdown above the content and its right highlights rail moves
inline below the hero below `lg`; and the console stacks its four parts vertically with shortened
region labels below `md`. The ask bar docks full-width above the footer below `md` rather than floating
over content.

### Elevation

The layers, from the back: page flow and cards; the sticky sub-nav and hover cards; in-page rails and
the back-to-top control; the ask bar; dropdown panels; the fixed header with its mega-menu; the cookie
choice band; and the dialog layer holding the search overlay, the return-to-draft confirmation and the
desk message stack, which sits in front of everything.

A resting card draws no shadow, only its hairline border. A hovered card and a hovered button raise on
a soft two-part shadow. A dropdown panel carries a deeper two-part shadow. The focus ring is a solid ring
in the mid, vivid blue, never removed and only ever restyled.

### Chrome

**Header.** A fixed bar at a constant height on the page ground with a hairline bottom border, spanning
the full width. Left to right: the wordmark `Meridian` plus `Cloud`, linking to `/`; the primary
navigation labels `Products`, `Families`, `Solutions`, `Datasheets`, `Console` and `Contact us` at the
body-medium step, opening `/product`, `/family`, `/solution`, `/datasheet`, `/console` and `/contact`;
then a right cluster with a search control and a filled `Start free` button opening `/contact`. A
navigation label warms to the mid, vivid blue on hover, and the active label carries a thin underline
in the light, vivid blue.

**Mega-menu.** `Products` opens a full-width panel under the header at the dropdown layer, grouping the
published products by their three families. Group headings sit at the micro step in a mid cool neutral;
links sit at the small step in a deep neutral and warm to the mid, vivid blue. The panel fades open and
the chevron beside its trigger turns through a half turn. Only one panel is open at a time, and Escape
closes it.

**Drawer.** Below `md` the primary navigation collapses behind a menu mark. Pressing it slides a
full-height panel in from the left over a dimmed backdrop at half opacity. Each primary item is a row
with a trailing arrow. A close control and Escape dismiss it, and the `Start free` button pins to the
panel foot.

**Search overlay.** The header search control opens an overlay at the dialog layer over a soft scrim. It
is a single field with the search glyph at the body step and a results list that fades in, filtering the
published products by name. Escape or a press on the scrim closes it, and focus is trapped until it does.

**Ask bar.** A rounded-pill bar fixed near the foot of the viewport on the home and product routes, on
the section ground with a hairline border, its placeholder `Ask anything about Meridian Cloud` in a light
cool neutral and a trailing send glyph in the mid, vivid blue. Submitting it opens `/ask` with the query
prefilled.

**Footer.** A five-column link matrix on the page ground above a hairline top rule, the columns headed
`Why Meridian Cloud`, `Products and pricing`, `Solutions`, `Resources` and `Engage`, opening `/`,
`/product`, `/solution`, `/datasheet` and `/contact`. Column headings sit at the body-medium step;
links sit at the small step in a mid cool neutral and warm to a deep neutral on hover. Below the matrix a
baseline row carries `Privacy` and `Site terms`, opening `/privacy` and `/terms`, and the fine print line
reads `Meridian Cloud. All rights reserved.`

**Cookie choice.** A band docked to the foot of the viewport on the page ground with a hairline top
border: the sentence `We use cookies to measure how the site is used.`, a `Privacy` link into the privacy
page, a filled `Accept` control and an outline `Decline` control. It stands only until the visitor
chooses and never covers the primary action of the surface behind it.

**Page metadata.** Every public route carries its own title, the surface name followed by
`- Meridian Cloud`, its own description, and a canonical link to its own address.

### Home

Bands in order: the hero, the product rail, the consistency console, the industry explorer, the customer
proof, the closing band, then the footer. The rail, the explorer and the closing band sit on the section
ground; the hero, the console and the customer proof sit on the page ground. The alternation is the only
separation drawn between them.

**Hero.** Centred with generous top space. The gradient product mark above the display heading
`The new way to cloud with Meridian`, the lead sub-line
`Build on one database that spans every region and never disagrees with itself. Start with an evaluation.`,
then two controls, a filled `Get started for free` and an outline `Contact sales`, both opening
`/contact`. Below them, a pill link reading
`Try Beacon Enterprise, the front door to AI for every employee` opens `/ask`.

**Product rail.** Under the heading `Products that hold their promises`, a horizontally scrolling rail
of dark product cards, each a deep neutral fill with near-white text over its art, the band itself on
the section ground, edge-faded at both ends, advancing one card on a timer and paged by a
previous and a next control. Each card carries an eyebrow at the micro step, a title line and generated
art. The first card is `Tessera` and selecting a card opens its product route. The rail shows only
published products carrying the `featured` flag, ordered by sort index, pads nothing where fewer are
flagged, and is omitted as a whole where none are.

**Industry explorer.** Under the heading `Solutions for your industry`, a two-pane band: a left list of
the six industries and a right panel showing the selected industry's proof card, its stat line and its
customer. `Retail` is selected on arrival, and selecting another fades the right panel to it without
loading another address.

**Customer proof.** Under the heading `Teams that build here`, an edge-faded wall of the eight customer
wordmark tiles, each set as type in a mid cool neutral and centred in a fixed tile, beside the testimonial
card carrying the quote with its attribution.

**Closing band.** On the section ground: the heading `Start your evaluation`, one line, and the filled
`Get started for free` with the outline `Contact sales`, both opening `/contact`.

### Product route

A left sticky sub-nav, a centre column and a right highlights rail. The sub-nav items are `Overview` and
one item per claim band; for `Tessera` those are `Overview`, `Consistency`, `Synchronized clock`,
`Partitions`, `Scale`, `Replication`, `Read modes`, `Failover` and `Service levels`. Selecting one scrolls to that band, and the active item carries the one decorative
asymmetric radius. A dismissible promo banner on the section ground sits above the hero, with an inline
link to `/console` and a trailing circular chip.

**Product hero.** The eyebrow at the micro step, the display heading, the lead, a filled
`Get started for free` opening `/contact`, and a `Try it in the console` link opening `/console`.

**Highlights rail.** A sticky card on the section ground in the right column, listing the product's
highlight lines as jump links, each with a trailing down-chevron.

**Claim bands.** One band per highlight line, in sort order, each stating that line's capability as a
claim a buyer could challenge, with a heading, a paragraph of body and, where the console can test it, a
`Try it in the console` link opening the console with a region pair prefilled. For `Tessera` the eight
bands are strong global consistency; synchronized-clock ordering of every commit; correctness during
network partitions, never corrupted; massive-scale transactions with no consistency trade, the data
sharded and rebalanced automatically as load grows; synchronous multi-region replication; tunable read
staleness; zero-data-loss automatic failover; and five-nines availability across regions.

**Art strip.** The product's art pieces in a row at the media radius, the first eagerly loaded and the
rest lazily. Selecting one opens it with its alternative text and the product name.

**Datasheet.** Where the product carries one, a card with its generated cover at the media radius in a
three-by-four aspect ratio, its title at the title step, a metadata line at the micro step in a mid cool
neutral reading the page count and the file size in megabytes to one decimal place, and a pill download
control.

**Related row.** Under the heading `Related products`, up to three cards from other published products
sharing a family, ordered by sort index ascending.

### Family, solution, datasheet and gallery surfaces

**Family index.** A breadcrumb, the heading `Three ways into the platform`, one sentence of standfirst,
then three cards in a row at `lg`, each carrying the family name at the title step, its standfirst at the
small step and its published count.

**Family page.** A full-width head still at two fifths of the viewport height under the family name at
the display step, its standfirst at the lead step, one paragraph of editorial intro in the reading
column, then the published products carrying it in the product grid. A family holding no published
product shows the sentence `Nothing is in this family yet. It will fill up.`

**Product index.** A breadcrumb, the heading `Every product on the platform`, a count line reading
`8 products`, then a sticky filter bar holding the name field labelled `Filter by name`, the family
selector and the sort selector with `Name, A to Z` and `Recently added`, then the card grid. The empty
state reads `Nothing matches that. Try a different family, or clear the filter.` beside a `Clear filter`
control.

**Solution index.** A breadcrumb, the heading `Solutions by industry`, a row of filter chips reading
`All` and each industry name, and the six industries as a grid, each card carrying the industry name at
the title step, its stat line at the body step and its customer at the dense step.

**Datasheet library.** A breadcrumb, the heading `Datasheets to download`, two sentences of standfirst in
an eight-twelfths reading column, then the grid of datasheet cards drawn as on the product route. The
composer offers no field for a cover.

**Art gallery.** A breadcrumb, the heading `Every product, drawn`, the family selector, then a masonry
grid keeping each piece's own aspect ratio at four columns on a wide viewport. A `Show more` control at
the foot of the grid adds further pieces below without moving the pieces already drawn or the footer.
Selecting a tile opens a lightbox carrying the product name, the alternative text and a
`Read about this product` link.

### The consistency console

A panel on the section ground at the product radius with a hairline border, in four parts with a
throughput meter along the foot.

**Region globe.** A flat drawn world map with the five region nodes as discs in a near-white cool
neutral, ringed in a near-white soft blue when active, joined by thin links in a light soft blue. Region
labels sit at the small step in a mid cool neutral. A selected region lifts to the mid, vivid blue fill.

**Write-then-read strip.** Two control groups below the map. The write group binds a source region, a key
and a small value; the read group binds any other region and a mode of `strong`, `bounded` or `exact`.
Writing commits the value, the committed state flashes the mid, soft green with a checkmark, and reading
from any other region then returns the same value with its latency figure. Both groups work from the
keyboard with the same outcomes as a pointer.

**Synchronized-clock readout.** A strip showing each region's clock as an uncertainty band rather than a
single instant, drawn as a narrowing bar in the near-white soft blue. When a write commits, the console
shows a commit-wait equal to that band, drawn as a filling bar in the mid, vivid blue, then acknowledges
with the checkmark and declares the write safely ordered before any later read anywhere.

**Partition toggle.** A control that cuts the link between a chosen region and the rest. On cut, the
severed region's node greys to a light cool neutral and its links draw dashed. A write attempted against
the isolated side is refused with the status circle in the mid, vivid red and the caption
`That region will not accept a write it cannot safely agree on.` A write on the majority side still
commits. Restoring the link re-syncs the isolated region, which shows the skeleton shimmer briefly and
then rejoins.

**Throughput meter.** A slim bar along the foot showing transactions a second rising as regions and load
are added, with the consistency tick in the mid, soft green holding throughout.

Under a request for reduced motion, or with no scripting, the console becomes a still labelled diagram of
its four parts with a one-line caption under each, and every write, read and partition control still
works from the keyboard: a request for reduced motion disables movement everywhere, yet the console
stays usable. Every control carries an accessible name, and the console's state reads as text:
the current value per region, the clock uncertainty and the partition status.

### Assistant, contact and standing surfaces

**Assistant.** A centred single-purpose surface with minimal chrome: the greeting
`Hello, how can I help?` at the heading step, four suggestion pills reading
`How can I try Meridian Cloud products for free?`, `How do I evaluate Tessera?`,
`Discover solutions for my industry` and `Summarize what is new`, then the field capped at 500 characters
with the counter `0 of 500 characters entered` beneath it and the caption `Built with Beacon Enterprise`.

**Contact sales.** A form in the reading column carrying the fields `Full name`, `Work email`, `Company`,
`Region`, `Interest` and `Message`, each labelled above with any failure message directly beneath, and a
filled `Contact sales` submit control. On success a banner on the near-white neutral success fill with a checkmark reads
`Thank you. Your evaluation request is with us.` and shows the enquiry identifier. On failure a banner on
the near-white warm neutral failure fill with the status circle names the field it is about.

**Privacy.** The heading `What we record` over one reading column stating that the platform records a
page view per public route with its time, and the contents of a contact-sales submission, and nothing
else; that the page-view log sets no cookie; and that the cookie choice governs cookies alone.

**Site terms.** The heading `Using the platform` over one reading column.

**Not found.** The heading `We cannot find that page` with the body
`It may have moved, or it may never have been here. The platform is still where you left it.` and a
control back to `/`, inside the global header and footer.

### The desk

**Sign-in card.** Centred on the page ground at the product radius: the heading `Sign in to the desk`, the
fields `Email` and `Password` each labelled above, and a filled `Sign in` control. A failed sign-in nudges
the card once, turns its border the failure red, and shows `That address and password do not match.`

**Desk navigation.** Every signed-in desk page carries a left sidebar holding `Products`, then
`Evaluation requests` and `Page views` for an administrator only, then a `Sign out` control at its foot.

**Product list.** The heading `Products`, three filter controls reading `All`, `Live` and `Draft` each
carrying a count, a `New product` control, then a split surface: the table with the columns `Name`,
`Families`, `State`, `Art` and `Last edited` on the left, figures aligned wherever counts stack, and a
detail pane on the right. Each row carries a badge reading `Live` on the mid, soft green or `Draft` on the
mid, vivid orange, each word set in a deep neutral on its fill. Selecting a row marks it and fills the
pane with that product's name, badge, summary, art pieces with their descriptions and an
`Open in composer` control, while the table stays in view. Below `lg` the pane stacks under the table.

**Composer.** One column on the page ground, drawn from the public design system: the same near-white
grounds, the same two families, the same radii and the same mid, vivid blue for every control. Fields in
order: `Product name`, `Web address`, `Eyebrow`, `Summary`, `Claim body`, `Families, up to three`,
`Show on the front page`, `Service level`, `Regions available`, `Highlight lines`, `Art`, `Datasheet`. The
art field takes a description per piece, labelled `Describe this image`, and shows how far each upload
has got while it runs. The controls are `Save draft` for every role, and `Publish` and `Return to draft`
for a publisher or an administrator only. `Return to draft` opens a confirmation dialog reading
`Return this product to draft?` with `Return to draft` and `Cancel`.

**Enquiries.** The heading `Evaluation requests` over the stored submissions newest first, each row
carrying the name, the company, the region, the interest and when it arrived.

**Views.** The heading `Page views` over a count per public route, ordered by count descending, and a list
of recent views each carrying its route and its time.

**Messages.** An editor action is answered by a brief toast message standing in a corner of the desk over the
page the editor acted on, pinned bottom right and entering on a short decelerating travel. A success
message carries a left border in the mid, soft green, a failure message in the mid, vivid red. A message
dismisses after five seconds or on press, the stack holds at most three, and a fourth displaces the
oldest. Nothing on the public side raises one.

### Iconography, motion mechanisms and the zero-asset substitution guide

The iconography is eleven marks drawn from coordinates in the build: the wordmark, a navigation chevron,
an arrow-forward mark for every onward link, a play triangle for the console's run control, a status
circle for error and close, a checkmark, a search glyph, a diamond mark, the gradient product mark, a
send glyph, and a globe for the privacy page. Each utility mark takes the colour of the text around
it; the wordmark carries the four brand hues letter by letter, the gradient product mark carries the
brand gradient, and the diamond mark takes the mid, vivid orange.

Five further colour roles complete the palette: secondary emphasis takes the mid, vivid blue one step
darker than the primary; the console's confirmed-write state takes the mid, soft green darker; a rare
category chip takes a near-white cool neutral with a violet cast; the testimonial attribution, a high-contrast
caption, takes a deep neutral one step lighter than headings; and secondary dividers take a light cool neutral one step deeper
than a hairline.

Motion comes in three kinds of moment and no fourth: a quick change when something is pointed at,
focused or opened; an entrance, or a loop while a surface waits; and the fade in from below, the reveal-on-enter
moment as a band first enters view. The named keyframes are the fade in from below, the carousel slide of the
product rail advancing or retreating one card, the half-turn of the gradient behind the flagship mark,
the skeleton shimmer sweeping a transparent highlight across a waiting surface, a notification badge growing in and out on its
appearance, and the focus animation that grows the focus outline outward to its offset. Scroll position
drives nothing but that fade in from below, and no captured scroll depth is re-enacted.

The zero-asset substitution guide replaces every asset class with a recipe, and no category of asset is
exempt: product-card art is a seeded generated field; the customer logos and the category logos are
wordmark tiles set in type; a portrait, where the testimonial carries one, is a generated monogram disc
rather than a photograph; diagrams are drawn in the build; and fonts are named rather than shipped. The
guide has limits: nothing it generates stands in for a claim, so a diagram shows how the console works
and never a figure the console did not produce.

### Components

A card carries its hairline border at rest and raises on hover, and every card, chip, field and badge
keeps one look on every surface where it appears.

### Media system

Every image is generated, and no photograph, film, icon file, font file or compressed texture ships with
the build. A product's card art is a two-point radial gradient keyed by a seed derived from the product
slug, so the same product always produces the same art and nothing reshuffles between reads, with a fine
desaturated grain over it at low opacity. The brand gradient bar runs between the light vivid blue and
the mid soft green.

Every generated image declares its intrinsic width and height, is delivered with a candidate set matching
the five breakpoints and a sizes hint, and loads behind a placeholder ground generated from its own
average colour. Datasheets are generated at seed time from the product's own text: a cover carrying the
product name in the display family, a contents page, and one page per highlight line. Page count and byte
size are read from the generated document, so the metadata line is truthful about the file the visitor
receives.

### Copy

Every string the product ships. These are exact.

| Where | String |
|---|---|
| header navigation | `Products`, `Families`, `Solutions`, `Datasheets`, `Console`, `Contact us` |
| header primary control | `Start free` |
| skip link | `Skip to content` |
| home heading | `The new way to cloud with Meridian` |
| home lead | `Build on one database that spans every region and never disagrees with itself. Start with an evaluation.` |
| home primary control | `Get started for free` |
| home outline control | `Contact sales` |
| home assistant pill | `Try Beacon Enterprise, the front door to AI for every employee` |
| rail heading | `Products that hold their promises` |
| explorer heading | `Solutions for your industry` |
| proof heading | `Teams that build here` |
| closing heading | `Start your evaluation` |
| ask bar placeholder | `Ask anything about Meridian Cloud` |
| cookie band body | `We use cookies to measure how the site is used.` |
| cookie accept control | `Accept` |
| cookie decline control | `Decline` |
| product index heading | `Every product on the platform` |
| product index count | `8 products` |
| product index name field | `Filter by name` |
| product index sorts | `Name, A to Z`, `Recently added` |
| product index empty | `Nothing matches that. Try a different family, or clear the filter.` |
| product index empty control | `Clear filter` |
| product console link | `Try it in the console` |
| related row heading | `Related products` |
| family index heading | `Three ways into the platform` |
| family empty | `Nothing is in this family yet. It will fill up.` |
| solution index heading | `Solutions by industry` |
| solution filter chip | `All` |
| datasheet library heading | `Datasheets to download` |
| gallery heading | `Every product, drawn` |
| gallery lightbox link | `Read about this product` |
| gallery more control | `Show more` |
| console refusal | `That region will not accept a write it cannot safely agree on.` |
| assistant greeting | `Hello, how can I help?` |
| assistant counter | `0 of 500 characters entered` |
| assistant caption | `Built with Beacon Enterprise` |
| contact submit | `Contact sales` |
| contact success | `Thank you. Your evaluation request is with us.` |
| privacy heading | `What we record` |
| terms heading | `Using the platform` |
| not-found heading | `We cannot find that page` |
| not-found body | `It may have moved, or it may never have been here. The platform is still where you left it.` |
| footer columns | `Why Meridian Cloud`, `Products and pricing`, `Solutions`, `Resources`, `Engage` |
| footer baseline | `Privacy`, `Site terms` |
| footer fine print | `Meridian Cloud. All rights reserved.` |
| page title suffix | `- Meridian Cloud` |
| desk sign-in heading | `Sign in to the desk` |
| desk sign-in submit | `Sign in` |
| desk sign-in failure | `That address and password do not match.` |
| desk list heading | `Products` |
| desk detail pane control | `Open in composer` |
| desk sidebar sign-out control | `Sign out` |
| desk filter controls | `All`, `Live`, `Draft` |
| desk new control | `New product` |
| desk badges | `Live`, `Draft` |
| desk art field label | `Describe this image` |
| desk composer controls | `Save draft`, `Publish`, `Return to draft` |
| desk return confirmation | `Return this product to draft?` |
| desk confirmation cancel | `Cancel` |
| desk enquiries heading | `Evaluation requests` |
| desk views heading | `Page views` |
| message, published | `Published. It is live now.` |
| message, returned | `Returned to draft. It is no longer public.` |
| message, upload failed | `That upload did not finish. Try it again.` |

## Constraints

- No payments, no pricing calculator and no billing of any kind.
- No visitor accounts. The public side holds no account, so there is no registration endpoint, no
  password reset flow and no visitor profile.
- No language model. The assistant surface carries its greeting, its suggestions, its field and its
  counter, and answers nothing.
- No search service. The search overlay filters the published products inside the app.
- No email is sent. The contact-sales form stores its submission and delivers nothing.
- No localisation and no language selector: one locale.
- No newsletter signup and no third-party newsletter embed.
- Three product families, not six. The platform's wider catalogue is out of scope.
- No video anywhere, including video thumbnails.
- No multi-tenancy and no single sign-on.
- No third-party analytics vendor. The page-view log is the app's own table.
- No free-account signup flow. `Start free` and `Get started for free` open the contact-sales form.
- No separate templates for the networking and assistant products; both are ordinary product pages.
- Nothing is scroll-scrubbed, and the skeleton shimmer is the only animation that loops.
- The app ships no binary asset.
- The app stays responsive with the seeded 9 products, 20 art pieces, 5 datasheets, 6 industries, 8
  customers and 3 desk accounts.

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

A successful call returns the named resource or shape. List endpoints return a top-level JSON array. An
invalid or unauthorized call is rejected as a client error, never a server error and never a silent
success, and leaves the stored state unchanged. Every `/api/desk/` endpoint takes a bearer token;
`/api/auth/login`, `/api/health` and the public endpoints take none, except that the two media
endpoints also accept one.

| Endpoint | Request | Response |
|---|---|---|
| `GET /api/health` | none | `{"status": "ready"}` |
| `GET /api/products` | `?family=&sort=name\|recent&name=`, `family` being a family slug | an array of the published products the filters select, each carrying `id`, `slug`, `name`, `eyebrow`, `summary`, `families`, `featured` and `sort_index` |
| `GET /api/products/{slug}` | none | one published product with `heading`, `lead`, `highlights`, `art`, `datasheet` and `related`, or not found where the product is `draft` or absent |
| `GET /api/families` | none | the three families, each carrying `id`, `slug`, `name`, `standfirst` and `published_count` |
| `GET /api/families/{slug}` | none | one family with `intro` and `products`, the published products carrying it |
| `GET /api/industries` | none | the six industries in `sort_index` order, each carrying `slug`, `name`, `stat_line` and `customer_name` |
| `GET /api/customers` | none | the eight customers in `sort_index` order, each carrying `id` and `name` |
| `GET /api/datasheets` | none | an array of the datasheets of published products plus the platform ones, each carrying `id`, `title`, `page_count`, `byte_size` and `product_name` where there is one |
| `GET /api/art` | `?family=&page=`, `family` being a family slug and `page` counting from `1` | the art of published products, paged at 24, each carrying `id`, `product_slug`, `product_name` and `alt_text` |
| `GET /api/media/art/{art_id}` | none | the bytes, or not found where the owning product is `draft` and the request carries no valid desk bearer token |
| `GET /api/media/datasheets/{datasheet_id}` | none | the bytes with a `Content-Disposition` of `attachment`, or not found where the owning product is `draft` and the request carries no valid desk bearer token |
| `POST /api/console/write` | `{"region", "key", "value"}` | `{"commit_timestamp", "uncertainty_ms"}`, or a refusal where the region is severed |
| `POST /api/console/read` | `{"region", "key", "mode", "bound", "timestamp"}`, `bound` for `bounded` and `timestamp` for `exact` | `{"value", "timestamp", "staleness", "latency_ms"}`, `staleness` and `latency_ms` in whole milliseconds |
| `POST /api/console/partition` | `{"region", "severed"}` | `{"regions"}`, the five regions each carrying `region` and `severed` |
| `POST /api/console/reset` | none | `{"regions"}`, every region unsevered |
| `POST /api/contact` | `{"name", "work_email", "company", "region", "interest", "message"}` | `{"ok", "enquiry_id"}` |
| `POST /api/auth/login` | `{"email", "password"}` | `{"access_token", "role"}` |
| `POST /api/auth/logout` | none | the session ended |
| `GET /api/desk/products` | `?state=all\|published\|draft` | an array of the products that state selects, each carrying `id`, `slug`, `name`, `state`, `families`, `featured`, `art_count` and `updated_at` |
| `GET /api/desk/products/counts` | none | `{"all", "published", "draft"}` |
| `GET /api/desk/products/{id}` | none | one product in either state with `art` and `datasheet` |
| `POST /api/desk/products` | the product fields | the created product, always `draft` |
| `PATCH /api/desk/products/{id}` | the changed fields | the updated product |
| `POST /api/desk/products/{id}/publish` | none | the published product, or a refusal naming the condition; publisher or administrator only |
| `POST /api/desk/products/{id}/unpublish` | none | the product back in `draft`; publisher or administrator only |
| `POST /api/desk/uploads` | `{"product_id", "kind", "filename", "content_type"}`, `kind` being `art` or `datasheet` | `{"url", "method", "headers", "object_key"}` |
| `POST /api/desk/art` | `{"product_id", "object_key", "alt_text", "width", "height", "sort_index"}` | the registered art piece |
| `POST /api/desk/datasheets` | `{"product_id", "object_key", "title"}` | the registered datasheet carrying `id`, `title` and `page_count` |
| `GET /api/desk/enquiries` | none | an array of the stored submissions, newest first; administrator only |
| `GET /api/desk/views` | none | `{"counts", "recent"}`: `counts` is an array, each entry carrying `route` and `count`, ordered by `count` descending, and `recent` is an array of views each carrying `route` and `viewed_at`; administrator only |

### No mocks

Every response above is served from `PostgreSQL` and `MinIO`. No fixture file, no in-memory stub, no
hardcoded array and no response the app returns to itself stands in for a query. The console's regions
and writes are rows, not a client-side simulation, and art and datasheet bytes live in the bucket, not on
the app container's own disk.

## Definition of done

A visitor can read the eight published products, prove on the console that a value written in one
region reads back from any other, and send a sales enquiry that an administrator then finds on the desk.
A draft product, its art and its datasheet stay unreadable to anyone outside the desk until it is
published.
