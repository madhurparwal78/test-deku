# Voxelith

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, upload a photograph without an account and get a downloadable
three-dimensional model back, and a signed-in creator must be able to spend a
credit, watch the job through to completion across a page reload, and save the
finished mesh into a private library that nobody else can read. The stored mesh
of one creator may never be readable by another creator or by an anonymous
request, and a balance with room for one job may never pay for two. Both hold at
the API and in the object store, not only in the interface: a control that is
merely hidden from view has refused nothing.

---

## Overview

Voxelith converts a photograph, or a written prompt, into a downloadable
three-dimensional mesh. The conversion is the product and everything else is
plumbing around it. A game artist, a product designer or a 3D-printing hobbyist
arrives with a picture and leaves with a GLB, an OBJ or an STL.

Four facts make this a system rather than a demo, and each of them is graded.

**The work is long-running.** A conversion takes minutes, not milliseconds, so
it is a queue with a visible state rather than a spinner. A job that is still
running when the page is refreshed is still running when the page comes back.

**The work is metered.** Credits, granted monthly by plan. A job reserves credit
when it starts and settles when it ends, a failed job costs nothing, and two
jobs submitted against a balance with room for one resolve to one accepted job
and one refusal.

**The output carries a licence**, and which licence depends on what the creator
was paying at the moment the asset was made. A model made on the free plan is
openly licensed forever, including after the creator upgrades. Payment changes
what the artefact legally is, which is unlike volume or speed, and it fails
differently: it is stamped on the asset at creation, never derived afterwards
from the plan the creator holds today.

**The output expires** on a schedule that also depends on the plan, from a week
to never, and archiving an asset does not pause that clock.

**Anyone can use the generator without an account.** The hero promises a first
model free and four sample images are offered to visitors who have not signed
in. That is the most consequential architectural fact in this brief: an
anonymous visitor consumes real compute, so every obligation an account would
normally carry, the allowance, the abuse control and the cost ceiling, has to be
met some other way. The allowance is bounded, it is enforced on the server
against a stored subject, and the work a visitor did before signing up follows
them into the account they create.

Alongside the paid cloud generator sits a second, separate product: three tools
that run entirely inside the browser and upload nothing at all. They are free
against paid, local against cloud, instant against queued, and no account
against an account. They exist to bring people to the site and they make a
privacy promise the main product cannot make, so that promise is kept
absolutely.

A build that renders a beautiful gallery and lets one creator download another
creator's mesh has not built this product. Neither has one that charges twice
for a job that ran once.

---

## User roles

Two, and only one of them holds an account.

| Role | Holds | Cannot |
|---|---|---|
| `creator` | an account, a plan, a credit balance, a private asset library, and the right to generate at every tier their plan allows | read, download, rename, tag, favourite, archive or delete any asset belonging to another creator; generate at a tier their plan does not carry; spend credit they do not have |
| `visitor` | no account. One bounded anonymous generation, the four pre-computed samples, the gallery, the pricing page, the three local tools and the legal pages | a second anonymous generation; any access to any creator's library or stored objects; any tier above the free plan's allowance |

Signup is open. A visitor becomes a creator by registering with an email and a
password, and the anonymous asset they made before registering is carried into
their new library if it is still inside its claim window, with the licence it was
already stamped with.

Ownership is enforced **server-side on every read of an asset and on every read
of a stored object**. Hiding a download control in the interface is not
ownership: a direct API call from `creator2@example.com`'s session for
`creator@example.com`'s asset, or for the object behind it, is rejected with
`404`, so the existence of another creator's asset is not disclosed. The same
request carrying no session at all is rejected with `401`. The object store is
not publicly readable and no path serves an object without first deciding who is
asking.

A creator is deactivated, never deleted, because the credit ledger and the
download history reference them and a removed account turns an audit trail into
unattributable rows. Account deletion states plainly what it cannot recall: a
model made under the free plan carries an open licence, and others who already
hold it keep that grant.

---
## Core features

Every rule below has a negative case and an exact rejection status.

1. **Sign up, sign in and session.** A visitor registers at `/sign-up` with an
   email and a password and lands on `/my-assets`. A seeded creator signs in at
   `/sign-in` with an email and a password. A wrong password is rejected with
   `401` and a message that does not say which half was wrong. A request to any
   library endpoint without a session is rejected with `401`.

2. **One stored tier table.** Quality is four named tiers and each is a preset
   over two stored parameters, an octree resolution and an inference step count.

   | Tier | Octree resolution | Inference steps | Polygon ceiling | Credits |
   |---|---|---|---|---|
   | `fast` | `196` | `20` | `15000` | `2` |
   | `standard` | `256` | `30` | `30000` | `5` |
   | `pro` | `384` | `40` | `60000` | `10` |
   | `ultra` | `512` | `50` | `300000` | `20` |

   The generator control, the feature copy, the frequently-asked questions and
   the pricing page all read this one table. A tier named in one place and
   missing from another, or a polygon ceiling printed as one number on the
   pricing page and a different number in the headline, is a defect: the maximum
   polygon count on this site is `300000` and it appears as that number
   everywhere it appears at all. A write that sets a tier outside these four
   names is rejected with `422`.

   The tier a job ran at is a preset, and a preset's definition will change. So
   the resolution and the step count that actually produced a result are
   recorded on the job, and the asset remains reproducible from those two
   numbers after the table has moved on.

3. **The generator control surface.** On `/` the generator carries a source mode
   of `image-to-3d` or `text-to-3d`, an input mode of `single-image` or
   `multiple-images`, the four tiers as a labelled radio group, a texture toggle,
   and a generate control with the credit cost printed beside it. The four
   controls do not vary independently: `multiple-images` is available only at the
   `ultra` tier and only to a paid plan, and the cost follows all four.

   Cost is `tier credits`, plus `5` when textures are on, plus `10` when the
   input mode is `multiple-images`. The default state is `image-to-3d`,
   `single-image`, `pro`, textures off, which is `10` credits.

   **The cost shown is the cost charged.** It updates as the controls change, it
   holds from display through submission, and it holds even if the tier table is
   edited in between. A job that settles at a different figure from the one its
   creator was shown is wrong however defensible the new figure is.

4. **The licence is stated before generation, not after.** The confirmation step
   names the licence the result will carry before the job is submitted:
   `CC-BY-4.0` under the free plan and for an anonymous visitor, and
   `customer-owned` under a paid plan. A creator who discovers after the fact
   that their model must be attributed has been misled by omission.

5. **Upload is three affordances for one action.** A file input, a drop target
   and a paste handler all reach the same validation. Accepted input formats are
   `JPG`, `PNG` and `WEBP`; anything else is rejected inline with the format
   named, and nothing is stored. The file input is the keyboard path and it is
   always present.

6. **The job.** Submission returns a job in `queued`. It moves to `processing`,
   then to `completed` or `failed`. Its state is visible with a queue position
   or a named state and never a bare spinner with no information, it survives a
   page reload, it remains correct after the tab has been hidden, and a single
   poller serves the whole document rather than one per open tab.

   - Credit is **reserved** when the job starts and **settled** when it ends.
   - A job that ends `failed` **returns the reservation in full** and the creator
     is told, and the balance afterwards equals the balance before.
   - A job is **idempotent on its idempotency key**. A second submission of the
     same key, whether the creator's retry or the system's, produces one asset
     and spends one reservation, and answers with the job that already exists.
   - A submission whose cost exceeds the available balance is rejected with
     `402` and nothing is reserved.
   - **Two submissions arriving together against a balance with room for one
     leave one accepted and one rejected with `402`.** The ledger afterwards
     shows one reservation and a balance that never went below zero.

7. **Queue priority is fixed at submission.** It is written onto the job from the
   plan the creator held when they submitted: `limited` on free, `standard` on
   pro, `higher` on max. A creator who upgrades while a job is queued does not
   jump, and one who downgrades does not fall.

8. **One generation is one asset.** A completed job produces a single asset
   carrying several representations: a `glb` for web and games, an `obj` for 3D
   software, an `stl` for 3D printing, its texture maps and a preview image.
   Downloading the OBJ and then the STL of one model spends no further credit
   and creates no second library entry. Each download is recorded against the
   asset with its representation and its time, and that history is visible to
   the asset's owner and to nobody else.

9. **The download carries its licence.** An exported archive contains the mesh
   and, beside it, a file stating the asset's licence and, under `CC-BY-4.0`,
   its attribution requirement. The licence travels with the file, because a
   licence that exists only in a database row is a licence the person holding the
   mesh cannot read.

10. **Licence attaches at creation and never moves.** The asset stores the plan
    it was made under and the licence that plan grants. Upgrading from free to
    pro does not relicense past work: an asset made on free stays `CC-BY-4.0`
    permanently, because retroactively privatising it would withdraw a grant
    already made. A request to change a stored licence is rejected with `409`.

11. **Retention.** Each asset carries a deletion date set from the plan at
    creation: seven days on free, one hundred and eighty days on pro, and none at
    all on max, which keeps assets permanently. Each asset shows its deletion
    date. Something warns before an asset is deleted, because seven days is short
    enough that silent deletion loses somebody's work.

    **Downgrading does not shorten an existing date.** A creator moving from pro
    to free keeps the dates their existing assets already carry, and the
    interface states that before the downgrade completes rather than after.
    Assets made after the downgrade carry the free plan's seven days.

12. **The asset library at `/my-assets`.** Behind a session, and it is the
    creator's own and nobody else's.

    | Capability | Behaviour |
    |---|---|
    | Filter by status | `completed`, `processing`, `failed` |
    | Filter by tag | any stored tag |
    | Filter by favourite | a per-asset flag |
    | Favourite | set and unset |
    | Archive | a per-asset state, distinct from delete |
    | Title | editable, overriding the generated default |
    | Description | free text |
    | Tags | many per asset |
    | Download history | per asset, owner-visible |

    **Filters compose.** Status and tag and favourite apply together, not one at
    a time.

    **Archive is not delete.** An archived asset leaves the default view and
    still exists, is still reachable by an explicit filter, and its deletion date
    keeps counting down exactly as before. A build where archiving stops the
    clock has quietly given free-plan creators permanent storage.

13. **Anonymous generation.** A visitor with no session generates once. The
    allowance is `1`, it is enforced on the server against a stored subject
    rather than against a cookie, and the four samples `sneaker`, `mug`, `chair`
    and `plant` are offered as free starting points.

    - The four samples are **pre-computed**. Choosing one serves an existing
      stored asset and never re-runs a conversion.
    - A second anonymous attempt is rejected with `429` and a message that names
      the reason, that the one free model has been used, and offers signing up.
      A generic failure is not acceptable here.
    - An anonymous result is **claimable**. The response carries a claim token
      valid for `24` hours, and a visitor who signs up inside that window finds
      the model in their new library with the licence it was stamped with. After
      the window the token is refused with `410`.

14. **Free credits are a pool that can run out.** The free plan grants `10`
    credits monthly and a `5` credit welcome gift on a first-come, first-served
    basis, which means the welcome pool empties. A creator who cannot be granted
    welcome credit because the pool is exhausted is told exactly that, with
    `409` and a message naming the exhausted pool, rather than being shown a
    generic failure. The exhaustion of the free-credit pool is surfaced as
    itself, because a first-come, first-served allowance implies a pool that
    empties and a visitor who meets an empty one deserves to be told so.

15. **The monthly grant.** It is anchored to the creator's subscription
    anniversary, not to the calendar month, and granting the same period twice
    grants once. **Unspent monthly credits do not roll over**; the welcome grant
    does not expire. The pricing page states both, because a plan that says
    `1,000 credits monthly` and never says what happens to the unspent ones has
    not finished describing itself.

16. **Pricing at `/pricing`.** Three plans, and what they gate.

    | | `free` | `pro` | `max` |
    |---|---|---|---|
    | Price | `$0` | `$15.00` struck to `$9.90` per month | `$39.00` struck to `$19.90` per month |
    | Badge | | `-34% OFF` | `-50% OFF`, `Most Popular` |
    | Monthly credits | `10` | `1000` | `4000` |
    | Welcome credits | `5` | | |
    | Tiers | `fast` and `standard`, single image and text only | all four, and multiple images at `ultra` | all four, and multiple images at `ultra` |
    | Polygon ceiling | `60000` | `300000` | `300000` |
    | Textures | none | 4K PBR textures | 4K PBR textures |
    | Queue priority | `limited` | `standard` | `higher` |
    | Retention | `7` days | `180` days | permanent |
    | Licence | `CC-BY-4.0` | `customer-owned` | `customer-owned` |
    | Support | | email within 24h | priority support and an uptime commitment |
    | Downloads | unlimited, of completed models | unlimited, with no upgrade prompt | unlimited, with no upgrade prompt |

    Payment buys five separable things and they fail differently: volume in
    credits, capability in tiers and textures, speed in queue priority,
    durability in retention, and rights in the licence. The last is the one that
    is unlike the others.

17. **The promotional price has an end.** A promotion is stored with a start
    date and an end date, and the struck prices above are in effect from
    `2026-09-01` to `2026-12-31`. After the end date the list price is charged
    and shown. Copy that reads `limited time` with no date anywhere is either
    false or unmaintained.

18. **The gallery at `/gallery`.** Before-and-after pairs, a source image beside
    its finished render. **Every gallery item names its source and the quality
    tier that produced it**, because a gallery of results with no settings
    attached teaches nothing and reads as advertising. The four published items
    are `Brass Compass` at `pro`, `Woven Basket` at `standard`, `Carved Owl` at
    `ultra` and `Tin Robot` at `fast`.

19. **Published figures are stored, not typed.** Every number the site publishes
    about itself is one stored row with one value, a basis and a measurement
    date, and it is rendered from that row everywhere it appears.

    | Key | Value | Basis | Measured |
    |---|---|---|---|
    | `models_created` | `25000` | jobs that reached `completed` | `2026-09-01` |
    | `average_rating` | `4.9` of `5` | ratings left on completed downloads | `2026-09-01` |
    | `success_rate` | `99.0` percent | jobs reaching `completed` over the preceding thirty days | `2026-09-01` |
    | `countries_served` | `80` | distinct billing countries | `2026-09-01` |
    | `average_cost_usd` | `$0.50` | one `pro` tier generation at the `max` plan credit rate | `2026-09-01` |
    | `conversion_minutes` | `2` to `3` | median wall time of a `pro` generation | `2026-09-01` |

    `success_rate` appears once and as one value. A site printing the same
    metric as two different numbers on one page is the direct consequence of
    that metric being typed into two templates instead of read from one row.

20. **The comparison table** on `/` compares a commissioned model with this
    service: conversion time `2-3 Days` against `2-3 Minutes`, success rate
    `Variable` against `99.0%`, average cost `$200+` against `$0.50`, and
    training required `Months` against `None`. Each figure on the service's side
    is rendered from the stored claim above, with its measurement date shown.

21. **The three local tools.** `/3d-tools` and three children, and they are a
    second, separate product.

    | Tool | Route | What it does |
    |---|---|---|
    | Online 3D Viewer | `/3d-tools/online-viewer` | previews `GLB`, `OBJ`, `STL`, `FBX`, `STEP` and ten more formats, `15` in all |
    | 3D File Converter | `/3d-tools/file-converter` | converts between `128` declared mesh, CAD, voxel and image format pairs |
    | 3D Text Generator | `/3d-tools/3d-text-generator` | turns typed text into geometry and exports `GLB`, `OBJ` or `STL` |

    - **Nothing leaves the browser.** Once one of these three routes has loaded,
      it issues no network request of any kind for as long as it is used, and
      that includes anything that measures behaviour. Sending the name of
      somebody's file to a measurement endpoint breaks the promise exactly as
      sending the file would.
    - **`128` pairs is a claim, so it is a data structure.** The converter holds
      a conversion matrix, the route prints the number of supported pairs, and
      that printed number equals the number of supported entries in the matrix.
      A list of special cases that happens to add up is not this.
    - **A file the tool cannot handle is refused by name.** The refusal states
      the format it found and that the tool does not support it. A silent
      failure on an unsupported file is indistinguishable from a broken tool.
    - `STEP` in the viewer's list is a CAD format built from mathematical
      surfaces rather than triangles, and it reaches the screen only as
      tessellated geometry. It is on the list because the list says so, and it
      is the hardest thing on it.

22. **A privacy page at `/privacy`**, reachable from the footer of every page,
    states what Voxelith stores about a creator, how long each asset is kept
    under each plan, and that the three local tools store and transmit nothing
    at all. `/terms` and `/cookie` are reachable from the same footer and
    `/terms` is linked from the signup form.

23. **An unknown address renders Voxelith's own not-found page**, which carries
    the product's chrome, a way back to `/` and to `/my-assets`, and answers
    `404`. A framework's default error screen is not this.

24. **Forms refuse automated submission.** The contact form at `/contact` and
    the anonymous generator both carry an unattended decoy field that a person
    never fills, and both refuse a submission that fills it. Both also refuse a
    form submitted repeatedly in quick succession: a third submission of the same
    form from one subject inside `60` seconds is refused. A refusal on either
    ground answers `429` and writes nothing.

25. **Every form rejects invalid input inline**, names the field that failed,
    summarises the failures at the top of the form as well as beside each field,
    and writes nothing at all when it refuses.

---
## User flow

Navigation is a left rail: the generator, the gallery, the tools, the library
and pricing, each a destination of its own. The work surface is a split detail
pane, so selecting an asset in the library opens it beside the list rather than
replacing it. Generating opens a modal over the current route, which is where
the cost and the licence are confirmed before anything is spent. Ordinary
confirmations are a toast; a job changing state also writes into a live region,
because a toast that has already faded is not an announcement.

**Routes.**

| Route | Who reaches it |
|---|---|
| `/` | anybody. The generator, the comparison table and the statistics band |
| `/gallery` | anybody |
| `/pricing` | anybody |
| `/3d-tools` | anybody |
| `/3d-tools/online-viewer` | anybody |
| `/3d-tools/file-converter` | anybody |
| `/3d-tools/3d-text-generator` | anybody |
| `/contact` | anybody |
| `/privacy` | anybody |
| `/terms` | anybody |
| `/cookie` | anybody |
| `/sign-in` | anybody without a session |
| `/sign-up` | anybody without a session |
| `/my-assets` | a `creator`, and only their own assets |
| `/my-assets/:asset` | the asset's owner, and nobody else |
| any unknown address | the not-found page |

**The graded journey.** A visitor with no session opens `/`, picks the `mug`
sample, and reads the cost beside the generate control and the licence the
result will carry. They generate. The job appears in `queued`, moves through
`processing`, and reaches `completed`, and the mesh downloads. They try a second
generation and are refused by name with `429`. They sign up at `/sign-up`, and
the model they just made is waiting in `/my-assets`, still carrying
`CC-BY-4.0`.

`creator@example.com` signs in and lands on `/my-assets`, which shows `Harbour
Crane`, `Rope Coil` and `Broken Statue` and does not show the archived `Ceramic
Teapot` until the archived filter is applied. They open the generator, upload a
photograph through the file input, and change the tier from `standard` to `pro`.
The cost beside the control changes from `5` to `10`. The confirmation modal
names both the cost and `customer-owned`, and they generate. The new job appears
in the library as `processing`; they reload the page and it is still processing
with its state intact; it reaches `completed`. They open it in the detail pane,
rename it, write a description, add the tags `prop` and `metal`, favourite it,
and download the GLB and then the STL. The balance has moved by `10` in total,
not by `20`, and the download history shows two entries.

They filter by status `completed` and tag `prop` and favourite together and get
exactly the assets that satisfy all three. They archive `Harbour Crane`; it
leaves the default list, remains reachable behind the archived filter, and its
deletion date is the date it always was.

**The refusals, in the same journey.** `creator2@example.com` signs in and
requests `creator@example.com`'s asset directly and is refused with `404`, and
the same for the stored object behind it, and the asset is exactly as it was. An
unauthenticated request for either is refused with `401`. `creator3@example.com`
holds `5` credits, which is one `standard` generation and no more, and submits
two at once: one is accepted, one is refused with `402`, and the balance never
goes below zero.

**States.** A creator whose balance cannot cover the selected combination sees
the generate control explain which of the balance, the plan's tiers or the
plan's texture allowance is the blocker, and sees the one action that would
change it. An empty library states what would be here and offers the generator
rather than an empty grid. The shell renders immediately and each region
skeletons independently; the rail never skeletons. A permission denial names
what was missing and never names another creator. Navigating away from a dirty
title or description warns. Every error surface shows its request identifier
with a copy control. A job that completes while the creator is on another route,
or has navigated away and come back, is in its correct state when they return.
Switching locale while a job is running and a cost is displayed reformats the
figure and changes neither the cost nor the job.

---

## UI/UX notes

There is one theme here and it is dark; no light variant is built. Voxelith's
ground is a near-black neutral, and every border on it is a mid grey. Those two values, with the height of the
announcement banner above the header, are the whole of the product's own
palette; the rest of the surface colours come from the component library
underneath, and only the ones actually used are shipped. A theme that carries
hundreds of values for colours that never appear is how a stylesheet gets heavy.

One accent, a bright lime, and it is the brand. It is a token, not a value typed
in wherever it is needed, and it is spent only on the primary action, on the
live indicator of a running job, and on a credit balance that has fallen too low
to generate. Verify it against the near-black ground at the interface text size,
which is the size on the overwhelming majority of elements: a saturated
yellow-green is bright without always being high-contrast, and it is used for
both text and buttons.

Status is never colour alone. `completed`, `processing` and `failed` each carry
an icon and a word as well as a hue, and de-emphasis fades toward the mid grey
border value rather than toward a second accent.

Type is one sans family at weights `500`, `600` and `700`. Body copy is set at
`16` over `24`, interface text at `14` over `20`, and headings at `36` over `40`
and `30` over `36`. Numbers in the library table, in the credit ledger and in
the pricing table are tabular, so figures align in a column. Stacking uses seven
values and no more, so the announcement banner, the header, the detail sheet,
the generator modal and a toast each have one home and cannot fight over the
same one.

Motion is a slow colour wash behind the hero, gently floating cards, a pulsing
glow on a running job, and a slight tilt on a gallery item as it is approached,
as though it were an object on a table rather than a picture on a page. That
last one is the only motion that says anything about what this product does.
Under reduced motion the four continuous animations stop at a resting frame and
every entrance resolves immediately, with one exception: **the generator's own
progress indication keeps moving**, because an indicator showing that a
several-minute job is alive is information rather than decoration, and removing
it leaves somebody unable to tell a working queue from a broken one.

Hover is gated on a device that actually has a pointer, so no hover treatment
sticks on a touch surface, and nothing is reachable by hover alone. The
high-contrast mode people turn on at the operating-system level is handled
rather than ignored, across the chrome, the library table, the status pills and
the generator controls.

Accessibility here is a contract rather than a preference. Body text clears the
WCAG AA contrast bar against whatever ground it sits on. Touch targets are sized
comfortably for a thumb. Every interactive element can be driven from the
keyboard alone, and shows a visible focus ring while it holds focus. Icon-only
controls carry a label. Nothing signals meaning by colour alone. The four quality tiers are
a labelled radio group and each one carries its credit cost in its accessible
name, because the cost differs per tier and a control that announces only its
name hides the thing that is being chosen. **A job reaching `completed` or
`failed` announces itself**, since a job that takes minutes and finishes
silently is invisible to somebody who looked away. The 3D preview is a canvas
and is therefore opaque: it carries a text alternative describing the model, and
orbit and zoom are operable from the keyboard, and the download formats are a
route to the same thing that does not require seeing it.

Every content image carries alternative text and decorative images declare
themselves decorative. Every page declares its language, and that declaration
changes with the locale. Prices, dates and numbers are formatted per locale.
Text direction is handled rather than assumed, so that adding a right-to-left
language later does not mean rewriting the layout. Headings are given line-break
guidance, because a heading that fits in English overflows in German, and
because Chinese, Japanese and Korean line-break differently from Latin scripts
and break in the wrong place unless they are told how. Structurally, each page is one
landmark tree: a banner, a navigation region, a main region and a footer. Its
headings step down a level at a time and skip none. A skip control at the top
jumps straight past the chrome into the main region. The generator modal traps focus while it is open
and returns focus to the control that opened it.

The narrow arrangement is the same tree rearranged, never a second tree built
beside the first. Five widths are used symmetrically as both minimum and
maximum. Narrow the window and the rail becomes icons carrying tooltips, the asset detail
pane turns into a full-height sheet laid over the library list, and a table
takes its own scroll container rather than pushing the page wider. Nothing
overflows sideways at any width. Portrait or landscape, every navigation target
is still reachable, and a short viewport holds as well as a narrow one.

Each page leads with one clear primary action, visually distinct from every
secondary one: generate on `/`, the plan choice on `/pricing`, the generator on
an empty `/my-assets`, and the file chooser on each of the three tools.

---
## Technical requirements

The stack is a single-page client over a JSON API. Preact with Vite builds the
client, which consumes the API and renders every route in the browser. Fastify
serves the HTTP API on the same origin under the `/api` prefix. PostgreSQL is
the datastore and MinIO is the object store; both are already running and are
reached through their environment variables. The datastore is at `DATABASE_URL`,
which carries the same value as `DB_URL`. The object store is at
`STORAGE_ENDPOINT`, with `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` and the
bucket named by `STORAGE_BUCKET`. Nothing else is installed and no other backing
service exists.

Every stored file lives in MinIO: the uploaded source image, the `glb`, the
`obj`, the `stl`, the texture maps, the preview image and the exported archive.
The bucket is not publicly readable. Every object is served through an
application path that establishes who is asking before it answers, so that a URL
which leaks is a URL that still refuses a stranger. An object belonging to one
creator is never returned to another, and that holds for the anonymous case as
well as the signed-in one.

The conversion itself is performed by the application. A submitted job reaches a
terminal state on its own without any external service being contacted, and it
takes long enough to be observably asynchronous: the interface must show a
running job rather than a completed one the instant it is submitted. The number
of seconds a conversion occupies is read from `GENERATION_SECONDS`, never
hardcoded, so the same build is both a product that takes minutes and a build
that can be exercised quickly.

Session is email and password with bearer tokens. `POST /api/auth/login` takes
an email and a password and answers with an access token, which every
session-bearing request carries. Passwords are stored so that the stored form
cannot be reversed, and no response body, no error message and
no page the browser downloads ever contains a password, a token belonging to
another session, a bucket credential or a database credential.

Credit accounting is serialisable with respect to a balance. Two submissions
arriving at the same instant against one account resolve to the same outcome
they would have reached one after the other, and the balance is never negative
at any point that any observer can read. A job's reservation and its settlement
are recorded, never overwritten, so that the balance is always the sum of what
came before it.

Every response carries a request identifier and every error surface can show it.
Every public route carries its own title and its own description, and no two
public routes share either. Every public route declares a social preview title
and a preview image, and that image resolves. Times are stored and compared in
UTC. Money is stored in integer minor units in `usd`. Font faces are subsetted
per locale, so a visitor reading one language downloads only that language's
character sets and not the character sets of the other eleven; that is the
largest mechanical saving available here. No route ships a rotating model as a
sequence of still images, and no page requests a stock portrait of a person.

The three routes under `/3d-tools` make no request after their initial load.
That is a property of the shipped client, not an intention.

`GET /api/health` returns `200` once the app is ready.

**The API surface.**

| Endpoint | Purpose |
|---|---|
| `POST /api/auth/sign-up` | register, open to anybody |
| `POST /api/auth/login` | exchange email and password for an access token |
| `GET /api/session` | the current account, its plan and its balance |
| `GET /api/tiers` | the one stored tier table |
| `GET /api/plans` | the three plans and the active promotion |
| `POST /api/jobs` | submit a generation, carrying an idempotency key |
| `GET /api/jobs/{id}` | one job and its state |
| `GET /api/assets` | the caller's library, filtered by status, tag, favourite and archived |
| `GET /api/assets/{id}` | one asset owned by the caller |
| `PATCH /api/assets/{id}` | title, description, favourite, archived |
| `POST /api/assets/{id}/tags` | add a tag |
| `GET /api/assets/{id}/download/{kind}` | one representation, owner only, recorded |
| `GET /api/credits` | the caller's ledger |
| `POST /api/claims` | exchange an anonymous claim token for ownership |
| `GET /api/samples` | the four pre-computed samples |
| `GET /api/gallery` | the published gallery items with their sources and tiers |
| `GET /api/claims/published` | the stored published figures |
| `POST /api/contact` | the contact form |

---

## Data model

Rows, their ownership and the invariants that hold over them.

| Entity | Fields |
|---|---|
| `account` | email, display name, plan, status: `active` or `deactivated`, subscription anniversary, created at |
| `plan` | key: `free`, `pro` or `max`, list price, promotional price, promotion start, promotion end, monthly credits, welcome credits, polygon ceiling, allowed tiers, textures allowed, multiple images allowed, queue priority, retention days, licence, rollover |
| `quality_tier` | key: `fast`, `standard`, `pro` or `ultra`, octree resolution, inference steps, polygon ceiling, credit cost |
| `credit_ledger` | account, kind: `welcome`, `monthly`, `reservation`, `settlement` or `refund`, amount, balance after, job, period start, occurred at |
| `job` | owner account or claim token, source mode, input mode, tier, textures, source object key, octree resolution recorded, inference steps recorded, cost shown, cost charged, queue priority, state: `queued`, `processing`, `completed` or `failed`, idempotency key, attempt count, error reason, created at, started at, ended at, row version |
| `asset` | job, owner account or claim token, title, description, licence, plan at creation, tier at creation, polygon count, favourite, archived, deletion date, created at |
| `asset_representation` | asset, kind: `glb`, `obj`, `stl`, `texture-map` or `preview`, object key, byte size |
| `asset_tag` | asset, tag |
| `download_event` | asset, account, representation kind, occurred at |
| `anonymous_allowance` | subject hash, attempts used, first seen at, claim token, claim expires at |
| `sample` | key, title, source object key, pre-computed asset, tier |
| `gallery_item` | title, source object key, asset, tier, published |
| `published_claim` | key, value, unit, basis, measured on |
| `conversion_pair` | source format, target format, supported |
| `contact_message` | name, email, body, occurred at |

**Ownership.** Every `job`, `asset`, `asset_representation`, `asset_tag`,
`download_event` and `credit_ledger` row carries its owner, which is exactly one
of an account or an anonymous claim token and never neither and never both. A
read answering for one account never returns a row belonging to another, and
that holds for background work and for object reads as well as for interactive
reads.

**Invariants.**

- One completed `job` produces exactly one `asset`, and that asset carries
  several `asset_representation` rows.
- A `job` carries an idempotency key that is unique per owner, so a resubmission
  yields the existing job rather than a second one.
- A `job` carries a row version that changes on every transition, so two state
  changes arriving together produce one transition and the second is told the
  row has moved.
- `credit_ledger` and `download_event` rows are inserted and never updated or
  deleted, and an account's balance equals the sum of its ledger amounts.
- A `job` that reaches `failed` has a `refund` equal to its `reservation`, and
  the account's balance after equals its balance before the reservation.
- `cost_charged` equals `cost_shown` on every settled job.
- No `credit_ledger` row leaves a `balance after` below zero.
- `asset.licence` and `asset.plan_at_creation` are written once, at creation,
  and never updated.
- `asset.deletion_date` is written once, at creation, from the plan's retention
  at that moment, and a later plan change does not move it.
- `asset.archived` does not affect `asset.deletion_date`.
- `job.queue_priority` is written at submission from the plan at that moment.
- A `monthly` ledger row is unique per account per period start.
- `anonymous_allowance.attempts_used` never exceeds `1`.
- A `sample` always resolves to a stored pre-computed asset and never to a new
  job.
- `published_claim.key` is unique, so one metric has one value.
- The tier on a `job` and on an `asset` is one of the four stored tier keys.

**Roles.** The stored role set is `creator` and `visitor`, and only `creator` is
an account.

**Seed data.** Seeding is idempotent: running it twice leaves the same rows.

| Account | Plan | Balance | Holds |
|---|---|---|---|
| `creator@example.com` | `pro` | `1000` | `Harbour Crane` (completed, `pro`, favourited, tags `vehicle` and `industrial`), `Ceramic Teapot` (completed, `standard`, archived, tags `prop` and `kitchen`), `Rope Coil` (processing, `pro`, tag `prop`), `Broken Statue` (failed, `ultra`, tag `figure`) |
| `creator2@example.com` | `free` | `15` | `Paper Lantern` (completed, `standard`, `CC-BY-4.0`, tag `prop`) |
| `creator3@example.com` | `free` | `5` | nothing |

Every seeded account signs in with the password `deku-demo-pw-2026`. That exact
string is the seeded password: it is not an example and not a placeholder, and an
account seeded with any other password cannot be signed into. The three seeded
addresses and that password are written to `/app/USER_README.md`.

`creator3@example.com` holds exactly one `standard` generation's worth of credit
and no more.

The four samples `sneaker`, `mug`, `chair` and `plant` are seeded with their
pre-computed assets. The four gallery items `Brass Compass`, `Woven Basket`,
`Carved Owl` and `Tin Robot` are seeded published, each naming its source and its
tier. The six published figures are seeded with their values, their bases and the
measurement date `2026-09-01`.

---
## Front-end specification

The client is a single page over the JSON API. The shell is a left rail, a
header carrying the announcement banner above it, and a main region. The rail
carries the generator, the gallery, the tools, the library and pricing, and it
collapses to icons at a narrow width.

**The generator**, on `/`, is the landing surface. Its controls sit together:
the source mode, the input mode, the four tiers as a radio group each carrying
its own credit cost, the texture toggle, and the generate control with the
current cost beside it. Above them sits the upload target, which accepts a file
through its input, through a drop and through a paste, and which shows the four
samples to a visitor with no session. Selecting generate opens a modal naming
the cost, the tier, the licence and the polygon ceiling, and the job is
submitted only from there.

**A running job** is a card carrying its state, its position or its named stage,
its tier and the cost it reserved. It is rendered from the server's copy of the
state, so a reload redraws the same job in the same state. One poller serves the
document, it slows while the document is hidden, and it stops when no job is
running.

**The library**, on `/my-assets`, is a list on the left and a detail pane on the
right. The list carries the filter controls for status, tag, favourite and
archived, which apply together. A row shows the asset's preview, its title, its
tier, its licence, its status and its deletion date. The detail pane carries the
title and description as editable fields, the tag editor, the favourite and
archive controls, the three download formats, and the download history. At a
narrow width the detail pane becomes a full-height sheet over the list.

**The viewer** appears in the detail pane and on the gallery. It renders a mesh
up to the ceiling the plans advertise, on hardware the visitor did not choose,
so it degrades to the preview image rather than failing when a mesh at the
maximum cannot be held. It carries a text alternative and keyboard orbit and
zoom.

**The three tools** each occupy their own route and share a shape: a drop target
and a file input, a result area, and a statement of what the tool supports. The
converter additionally renders its pair matrix and the count of supported pairs.
None of the three renders anything that requires a request.

**Feedback.** A toast confirms an ordinary action and then fades. A job changing
state additionally updates a live region, so the change is announced and not
only shown. A refusal is rendered where the action was taken, names the field or
the reason, and leaves the form filled in.

---

## Build plan

1. Schema, seed, the MinIO buckets and `GET /api/health`.
2. Sign-up, sign-in, bearer sessions, and the seeded accounts.
3. The stored tier table and the plan table, and the endpoints that read them.
4. The generator controls and the cost calculation, including the confirmation
   modal that states the cost and the licence.
5. Job submission, the reservation, the worker that advances a job to a terminal
   state, and the object writes.
6. The credit ledger, its append-only history, and the contended path where two
   submissions meet one balance.
7. Failure, refund, and idempotency on the submission key.
8. The library: filters that compose, favourite, archive, title, description,
   tags, downloads and download history.
9. The ownership check on every asset read and every object read.
10. Licence and retention stamping, the downgrade rule, and the licence file
    inside the exported archive.
11. Anonymous generation, the bounded allowance, the pre-computed samples and
    the claim path.
12. The three local tools, the conversion matrix and its count.
13. The gallery, the stored published figures, the comparison table and the
    statistics band.
14. The public pages: privacy, terms, cookie, contact, the not-found page, the
    per-route title, description and social preview, and the refusal of
    automated submission.

---

## Constraints

Build the generator, the gallery, the pricing page, the signed-in asset library,
the three local browser tools and the legal pages. The following are
deliberately out of scope: translated route trees for the twelve languages, the
editorial routes for a blog, a changelog and documentation, the four unlaunched
surfaces for text, image, audio and video generation, the waiting list, the
hosted payment provider and its checkout, and any component-library scaffolding
route. Plans are changed directly against the account; no payment is taken.

The formatting half of the locale obligation stays and is built: every page
declares its language, and prices, dates and numbers are formatted per locale.

Two things the reference product does are deliberately not reproduced. There are
no testimonials illustrated with portraits drawn from a placeholder-avatar
service; where genuine attributable testimonials do not exist, the comparison
table and the stored figures carry the argument alone and are stronger for it.
And no gallery item uses a recognisable character from a published work as its
source image; the four published items use generated subjects.

Use only the backing services named in this brief. No number in this brief is a
suggestion: the closed vocabularies are closed, and a value outside one is
refused rather than stored. There is no light theme.

---

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
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

---

## Definition of done

A stranger converts one photograph into a downloadable three-dimensional model
without an account, and a signed-in creator spends a credit, watches the job
survive a page reload on its way to completion, and finds the finished mesh in a
private library with its licence and its deletion date already stamped on it.
The hardest guarantee is that the meter and the boundary both hold outside the
interface: a balance with room for one job never pays for two, and one creator's
stored mesh is never readable by another.
