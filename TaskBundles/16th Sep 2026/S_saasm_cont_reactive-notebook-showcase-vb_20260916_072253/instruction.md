# Reactive Notebook Showcase

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser, read
the home route, browse the community listing sorted by stars, follow the closing call to
action, and create a free account, without hitting an error page.

An author must be able to sign in to the studio, compose a page from ordered blocks,
upload an image, and publish. While that page is a draft, the image must not be readable
by a signed-out visitor, and the moment the page publishes the same image must be
readable. The bytes must live as a real object in the `minio` bucket at the key scheme
below: a row in a database column, or a file on the app's own disk, is not the object,
and a page hidden from a listing whose image still answers at its own address is not a
draft.

## Overview

Datalume is a platform for reactive data notebooks that run in a web browser. This
application is its public marketing surface together with the studio that composes it: a
small set of high-craft pages that explain the notebook, tell an AI-for-data story, show
off community work, and route a visitor to a free account.

The people who use it are two. A visitor is a data scientist, an analyst or a developer,
and the site's whole job is to make the reactive notebook legible in seconds and then get
them to sign up. An author is a marketer who owns the pages: they compose each route from
ordered section blocks, upload its media and publish it, without a deploy and without a
developer.

The tone is confident and technical. Two registers of surface alternate: bright editorial
pages on white with near-black text, and full-bleed feature panels in a saturated blue, a
warm pink-to-orange gradient, or a signature mint teal. Display headlines are set in a
monospaced face, a deliberate nod to code.

What it deliberately is not: this is the storefront, not the notebook. The reactive
engine, the renderer, real-time multiplayer, the execution sandbox, the data connectors,
version history and the AI canvas all live in the application the site advertises, and
none of them is built here. There is no pricing engine, no payment, no search index, and
no comment thread.

The genuinely hard part is that a draft is one visibility decision expressed in two
places, the page row and the object in the bucket, and the two have to agree.

## User roles

| Role | Can do |
|---|---|
| Reader (signed out, or signed in with a free account) | Read every published page, browse and sort the community listing, page through it, create a free account, subscribe to the mailing list, and read the terms page. **Cannot reach the studio, cannot read a draft page, and cannot read the media of a draft page.** |
| Author (signed in) | Everything a reader can do, plus compose, edit, reorder and publish the pages they own, and upload media to them. **Cannot edit, publish or read another author's draft page, cannot read another author's draft media, and cannot delete a published page's slug.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in
the UI is not authorization: a direct API call from a Reader session to any Author-only
endpoint must be rejected by the server (an unauthorized request is denied, not served),
leaving the protected state unchanged. The same holds between two Authors: a request from
one author's session for another author's draft page, its blocks or its media is denied,
and the target row is unchanged.

Reader signup is open. Anybody can create a free account from `/new`. Author accounts are
seeded and there is no author signup.

These accounts are seeded so the product can be exercised immediately. Every seeded
account uses the password `deku-demo-pw-2026`.

| Email | Role | Owns |
|---|---|---|
| `author@example.com` | Author | the three published pages |
| `author2@example.com` | Author | the one draft page |
| `reader@example.com` | Reader | nothing |

## Core features

### Auth

Email and password, implemented by the app. Passwords are stored hashed, never in plain
text. The JSON API authenticates with a bearer token issued at login and sent on every
request except login, signup and `GET /api/health`. Tokens expire; an expired token on a
studio route returns the author to the sign-in page with their destination preserved, and
the block text they had not yet saved is not lost.

### The composed page

1. A page is an ordered list of section blocks held in the product's own store rather
   than hard-coded into a page file. Changing copy or reordering bands is a data change
   and needs no deploy.
2. A block carries a `kind`, and the kinds are `hero`, `value_line`, `feature_card`,
   `color_panel`, `community`, `testimonial`, `use_cases` and `cta`. A block of any other
   kind is refused.
3. Block positions are contiguous from `1` within a page. Removing a block closes the gap;
   no page ever has a position twice or a hole in the sequence.
4. A page renders its blocks in position order, and the rendered route is the page.

### Draft and publish, which is the rule that matters

1. A page is `draft` when it is created and becomes `published` when its author publishes
   it. Those are the only two states.
2. A draft page is invisible to a reader: its route answers not-found, exactly as an
   address that was never created does, and it appears in no sitemap and no listing.
3. **The media of a draft page is not publicly readable.** An image uploaded to a draft
   page exists as a real object in the bucket at its key, and a request for it from a
   signed-out visitor is refused.
4. The moment a page publishes, every media object its blocks reference becomes publicly
   readable at that same key. Nothing is re-uploaded and no key changes.
5. Publishing is idempotent. Publishing an already-published page changes no timestamp,
   creates no second row, and moves no object.
6. An author publishes only a page they own. A publish request for another author's page
   is denied and that page stays a draft.

### Media in the object store

1. Every uploaded byte lives in `minio`, reached at `STORAGE_ENDPOINT` in the bucket named
   by `STORAGE_BUCKET`, with `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY` read from the
   environment.
2. The object key is fixed and derived from the bytes:
   `media/{page_slug}/{sha256_of_bytes}.{ext}` - for example
   `media/home/9f2a4c1d8b7e6051a3c2d4e6f8091a2b3c4d5e6f7081920a1b2c3d4e5f60718.png`.
3. Bytes live nowhere else. Not on the app's filesystem, not in a database column, not in
   a data URI in the page. The object in the bucket is the image.
4. Uploading identical bytes to one page twice yields one object and one row, because the
   key is the digest of the bytes.
5. Protected media is served by one of exactly two mechanisms, and the app picks one and
   holds to it everywhere: an authenticated streaming endpoint that checks the caller
   before reading the object, or a presigned URL valid for no more than five minutes,
   issued only to a caller entitled to it. A presigned URL is never issued to a signed-out
   visitor for a draft page's object.

### The authoring studio

1. `/studio` lists the pages the signed-in author owns, drafts and published together,
   each showing its state.
2. `/studio/pages/<slug>` composes one page: the block list on one side and the selected
   block's fields on the other, both visible at once.
3. Adding a block opens its own address at `/studio/pages/<slug>/blocks/new` rather than a
   panel over the list.
4. A save, a publish, a refused action and a completed upload each report in a transient
   message that does not move the page under the author's hands.
5. A reader who reaches any studio address is denied, whether by clicking or by calling
   the endpoint directly.

### The home route

1. A full-width mint teal announcement band sits above the header, reading
   `Notebooks 2.0 is now live on the web.` with a near-black pill button `Try it now`. It
   is dismissible, it does not take focus when the page loads, and it scrolls away with
   the page rather than sticking.
2. A dark hero carries the display headline `Not your typical notebook` over the lead
   `Datalume's reactive JavaScript notebooks are uniquely suited for interactive data
   visualization, animation, learning, and experimentation.`, then a solid teal
   `Try it for free` and an outlined `Explore the docs`.
3. A white band centres `The shortest path from idea to live code` over
   `Datalume Notebooks run in your browser, so you can immediately start building instead
   of setting up a local dev environment. Our notebooks were designed from the ground up
   to encourage collaboration and code reuse.`
4. Three bordered cards follow, each with a line icon, a monospaced heading and body copy:
   `Literate programming` with `Weave together Markdown, JavaScript, HTML, and SQL for
   expressive dynamic documents, charts, and apps.`; `Connect to any data` with
   `Connect to any data source with ease - whether it's a file, a database, or an API.`;
   and `Built-in reactivity` with `Cells re-run automatically as you make changes and
   interact with inputs, making code easier to understand.`
5. A full-bleed blue panel carries the eyebrow `MULTIPLAYER EDITING`, the headline
   `Collaborate and share`, the body `Accelerate your feedback loop with real-time
   multiplayer, comments, automatic version history, and git-style forking & merging to
   freely explore new ideas.`, and a `Read the documentation` link, beside a notebook
   preview in which a second cursor edits a cell while its chart keeps up.
6. A second blue panel carries the eyebrow `EMBEDDING`, the headline
   `Ready for production`, the body `Conveniently embed notebooks as iframes, or for
   seamless integration, import notebooks into your app as reactive JavaScript modules.`,
   and a `Read the documentation` link, beside a preview framed with a small attribution
   badge in its corner.
7. A white community band centres `Join the community` over `Over 1,000,000 notebooks
   have been created on Datalume. Discover new ways to present data, connect with other
   data visualization enthusiasts, and fork public notebooks to get started more quickly.
   For even more examples check out trending and recent.`, where `trending` and `recent`
   are links to the listing. Below it a rail of community cards advances continuously.
8. A full-bleed teal panel closes with `Get started today` and a solid near-black
   `Sign up for notebooks` leading to `/new`, then the footer.

### The AI route

1. A dark hero centres `Supercharge your data workflow with AI` over `Discover more
   insights while maintaining confidence in the results. AI is interpretable and
   transparent in Datalume Canvases.`, above a canvas preview showing a grouping panel, a
   typed result table and a ranked answer, with a near-black `Watch the demo` button over
   it.
2. Four feature panels follow, several on the pink-to-orange gradient ground:
   `An AI-powered frontend for your database` with `From query-building to chart creation,
   AI equips you to pursue interesting paths, breeze past blockers, and iterate more
   quickly.`; `Answers you can verify` with `No more black box responses. AI works
   directly on the canvas so you can inspect, understand, and evaluate the results.`;
   `Better inputs for more predictable outputs` with `By "seeing" your canvas, including
   column summaries and sample rows, AI outputs better, more contextual answers.`; and
   `Pair with AI` with `Flex beyond your skills by partnering with AI. Use AI to create a
   useful starting point, then use code to modify results and fine-tune charts.`
3. A band titled `Use cases` lists exactly eight short headings, in this order:
   `Find and join relevant tables`, `Avoid a blank page`, `Flex beyond your skill`,
   `Make a histogram`, `Define a metric with natural language`,
   `Outsource data wrangling tasks`, `Make a quick prototype`, `Test an idea`.
4. Two testimonials follow, each with a quote, a person, a role and a `See their work`
   link: `AI is critical during all aspects of the discovery process from designing the
   right graph to tweaking the graph that you need, to getting the right insights for what
   the user needs.` from `Alex Rivera`, `Founder`; and `The AI is extremely impressive. I
   gave it a table of maintenance notes with hundreds of rows of station visits and simply
   asked it the reasons why the stations were disabled or otherwise removed. Boom, it gave
   me the top 6 reasons and a summary chart.` from `Sam Okafor`,
   `Software Engineer III`.
5. The route closes on `Get started today` over a `Get started` button.

### The community listing

1. `/top` lists published notebooks under four sort tabs: `Trending`, `Recent`,
   `Most stars last month` and `Most stars all time`. `Most stars all time` is the default
   and is shown selected.
2. Under the default sort the listing is ordered by star count, highest first. The first
   card is `D3 Gallery` at `1000` stars and the ninth is `Collapsible Tree` at `399`.
3. The listing pages at `30` per page. A count line reads the range and the total, and
   `Prev` is unavailable on the first page while `Next` advances to the second.
4. A grid and list toggle switches the presentation without changing the order, the page
   or the set of notebooks shown.
5. A card carries a thumbnail, a title link, an author with a circular avatar, a date, a
   star count with a star glyph, a comment count where there is one, and a fork glyph
   where the notebook was forked from another. `Zoomable Sunburst` is the seeded forked
   notebook.
6. Star and comment counts are never negative, and a notebook is never its own fork.

### Sign up, which every call to action leads to

1. `/new` is a centred card headed `Sign up` offering five account-creation methods, each
   with its provider glyph: `GitHub`, `Google`, `Microsoft`, `SSO` and `Email`.
2. Below them `Already have an account?` with a `Sign in` link, and the fine print
   `By continuing you agree to our Terms of Service.` with `Terms of Service` linked to
   `/terms-of-service`.
3. The email method takes an address and a password and creates a free reader account.
4. A second signup with an address that already has an account is refused and creates no
   second account.
5. Every `Get started`, `Try it for free`, `Try it now` and `Sign up for notebooks` action
   anywhere on the site leads here.
6. The form is protected against a bot: a submission that fills the unattended decoy field
   is refused, and so is the same form submitted repeatedly in quick succession. A refused
   submission creates no account.

### The not-found chrome

The information architecture is four public pages and one fallback, and that fallback is
where a lost visitor keeps every path back.

1. Every address that names no published page renders one screen saying the page was not
   found, inside the full header and footer, and answers not-found rather than
   redirecting.
2. It centres `Sorry, but we can't find that page right now.` over the body
   `You can search the site if you're looking for something in particular, or browse
   through popular notebooks from our community.`, where `browse through popular
   notebooks` links to `/top`.
3. A draft page's route renders exactly this screen, so a draft is indistinguishable from
   an address that was never created.

### The footer, on every route

1. The footer opens with the Datalume wordmark and a social row reading `GitHub`,
   `LinkedIn`, `Bluesky`, `YouTube` and `X`, then four link columns.
2. The columns are `Platform` with `Datalume Notebooks` and `Pricing`; `Docs` with
   `Datalume`, `Datalume Framework`, `Datalume Plot`, `D3` and `Release notes`;
   `Resources` with `Blog`, `Webinars`, `Videos`, `Customer stories` and `Forum`; and
   `Company` with `About`, `Careers`, `Contact us`, `Newsletter signup` and `GitHub`.
3. A legal strip closes it: `© 2026 Datalume, Inc.`, `Privacy`, `Security`,
   `Terms of Service` and `Vulnerability Disclosure`.
4. `Newsletter signup` takes an email address and records a subscriber. A second
   subscription with the same address records no second subscriber.

### What the site claims about the product

These six capabilities are what the pages assert and evidence. They describe the
application the site advertises; this build states them, and does not implement them.

1. **Reactive computation.** A notebook is a graph of cells rather than an ordered script:
   changing an input recomputes exactly the cells that depended on it and re-renders their
   outputs, and each recomputed cell signals itself with a brief amber flash. The
   `Built-in reactivity` card is where the home route says so.
2. **Live rendering.** A cell's output is anything a browser can draw, including
   hand-written `D3` compositions and `Datalume Plot` charts, redrawn as its inputs change
   rather than reloaded.
3. **Real-time multiplayer.** Several people edit one live notebook at once, seeing each
   other's cursors, and the computation is shared too, so a teammate's edit re-runs the
   cells on everyone's screen together. The `MULTIPLAYER EDITING` panel is where the home
   route says so.
4. **Sandboxed execution.** Anyone may run a stranger's notebook, so every notebook runs
   isolated from the host page, from other tenants and from the platform's own origin,
   under fixed limits. The footer's `Security` and `Vulnerability Disclosure` links are
   where the site puts its posture.
5. **Data connectivity and versioning.** A notebook ingests a file, an endpoint or a
   database as reactive values; tabular data arrives typed with per-column summaries;
   history is automatic and a notebook forks in one action.
6. **Publishing and community.** A finished notebook publishes with a chosen visibility
   and renders identically when embedded elsewhere, and public ones join the listing where
   they are starred, commented on and forked.

### The launch surface

1. A terms page at `/terms-of-service` is reachable from the footer of every page and from
   the sign-up card's fine print.
2. `/sitemap.xml` lists every published public route and no draft page. `/robots.txt`
   points at it.
3. Every response carries the standard security headers, including a strict transport
   policy and a nosniff content-type policy.
4. No credential, access key or token appears in anything the browser downloads. The
   storage keys and the database URL are read from the environment on the server and never
   reach a template, a script bundle or a response body.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | The home page: the banner, the dark hero, the value line, the three feature cards, the two blue panels, the community band, the closing call to action, the footer | Public |
| `/ai` | AI for data analysis | Public |
| `/top` | Popular notebooks, sorted and paged | Public |
| `/new` | Sign up | Public |
| `/terms-of-service` | The terms of use | Public |
| `/sitemap.xml` | Every published public route | Public |
| `/robots.txt` | Points at the sitemap | Public |
| `/studio/login` | Author sign-in | Public |
| `/studio` | The pages this author owns | Author |
| `/studio/pages/<slug>` | Compose a page: its blocks beside the selected block | Author |
| `/studio/pages/<slug>/blocks/new` | Add a block | Author |

**Entry and redirects.** An unauthenticated visitor who opens a studio address is sent to
`/studio/login` with their destination preserved and arrives on it after signing in.
Signing in with no destination lands on `/studio`. Signing out returns to `/`. A token
that expires mid-edit returns the author to `/studio/login` with the destination
preserved, and the block text they had not saved is still there when they return. A reader
who opens a studio address is denied rather than redirected into it. Any address that
names no published page renders the not-found screen.

**Journeys.**

1. **Read the pitch and sign up.** Open `/` as a signed-out visitor. Read the headline
   `Not your typical notebook`, scroll past the three feature cards and the two blue
   panels to the community band, follow `Sign up for notebooks` to `/new`, choose the
   email method, submit `reader2@example.com` with `deku-demo-pw-2026`, and land with a
   free account.
2. **Browse the community.** Open `/top`. The selected tab is `Most stars all time` and
   the first card is `D3 Gallery` showing `1000` stars. `Zoomable Sunburst` carries the
   fork glyph. Switch to `Recent` and the order changes. Follow `Next` and the count line
   advances to the second page while `Prev` becomes available.
3. **Compose and publish.** Sign in at `/studio/login` as `author2@example.com` with
   `deku-demo-pw-2026`. Open `/studio/pages/field-guide`, which is a draft. Add a block at
   its own address, upload an image, and save. A signed-out visitor asking for that image
   is refused, and `/field-guide` answers not-found. Publish the page. The same image is
   now readable at the same key and `/field-guide` renders.
4. **Stay out of another author's draft.** Signed in as `author@example.com`, request
   `author2@example.com`'s draft page, its blocks and its media. Each is denied and
   nothing about that page changes.

**States.** Every list has an empty state: `/top` under a tab with no notebooks names the
tab, `/studio` with no pages says so, and a page with no blocks renders its chrome rather
than a blank body. Every route has a loading state and never renders as a bare white page.
A rejected action leaves the page standing and reports its reason in a transient message;
nothing crashes the app.

## UI/UX notes

The north star: a visitor should understand what a reactive notebook is before they have
read a sentence, because a working one is running on the page. The register is confident
and technical, written for people who write code, and it alternates deliberately between
bright editorial bands and full-bleed colour panels that stop the scroll.

**Palette by role.** The page ground is a near-white neutral and body text is a
near-black neutral. Panels and hover grounds are a near-white neutral; borders are a
near-white neutral stepping to a light neutral; muted text is a light neutral, and a mid
neutral where it must still be read. The hero, the navigation and the footer sit on a
near-black neutral, and faint text on that dark ground is a light neutral. The brand
carries a vivid mint teal, which is the banner and the primary accent, and its hover on a
light ground is a deep mint teal. Feature panels are a mid, soft blue stepping to a mid,
vivid blue. Links are a mid, vivid cyan and a light, vivid cyan. The selection handles
that ornament the feature cards are a mid, soft indigo with a light, vivid indigo. A
near-white cool neutral is the faint wash behind pale panels, and a deep neutral is the
chrome's own darker step. One gradient exists: a vivid magenta falling to a vivid orange,
and it belongs to the AI route's panels and nowhere else. The exact shades are yours, so
long as each role above is filled by one colour and no two roles share one.

A terminal palette renders code output inside the previews: a near-black neutral ground
with a light, vivid red, a mid, soft teal, a mid, vivid amber, a mid, soft blue, a light,
vivid magenta and a mid, vivid teal. The provider marks on the sign-up card are the only
other multi-colour things on the site, and they carry a mid, vivid orange, a light, vivid
red, a light, vivid blue, a mid, vivid red, a mid, vivid cyan and a mid, vivid lime.

**Typography.** Three families, three jobs. `Inter` carries the UI, the body and the
navigation. `Spline Sans Mono` carries the display headlines, the code cells and the
console output. `Source Serif Pro`, at weights 400, 600 and 700 in roman and italic,
carries the notebook titles inside previews and the footer wordmark. The signature move is
that the largest headlines are set in the monospaced face rather than a sans, because the
audience writes code. The scale is wide and it steps clearly: a display headline that
dominates its band at a light weight, a sub-headline a clear step below it, a lead
paragraph larger than the body it introduces, then body, then interface text and labels.
Every size carries a line height chosen for its job, generous for reading and tight for
display. Captions, metadata and code are set at `12px`, which is the dominant size on the
page, and the fine print inside dense previews and the axis labels inside chart previews
step below it. All three families declare a swap behaviour with a real fallback stack, so
text paints immediately.

**Grid and shape.** A centred single column at a capped measure, with colour panels
breaking out to the viewport edge and carrying a faint square grid texture behind them.
Radii step through one fixed scale: cards, buttons and inputs take the small step, large
media panels a generous one, the ornamented card borders the smallest, pills are fully
round and avatars are circles. Elevation is soft and low, so a card reads as floating a
few millimetres off the page rather than stamped onto it; the floating hero cards, the
pills and the large media panels each carry their own lift, the largest a layered one.

**Iconography.** Every glyph is a line drawing in the current text colour on a small
square, reproduced from its geometry rather than shipped as a file, so it stays sharp at
any size and inherits the contrast around it: a chevron that rotates when its menu opens,
a link chevron, a three-bar hamburger, a play triangle, a magnifier, a gear, and one glyph
each for the three feature cards and the AI sparkle. The brand mark is a target,
concentric rings around a filled centre dot. The footer wordmark is live type in
`Source Serif Pro`, never traced into a path.

**Chrome.** A sticky header spans the full width above everything else: the target logo on
the left, then `Notebooks`, `Resources` and `Pricing`, then `Sign in` as a plain link and
`Get started` as a solid pill. Its trick is colour: while it floats over the dark hero it
renders light on dark, and it flips to dark on light once the page scrolls onto white
underneath it, interpolating its own colour tokens as the hero passes rather than swapping
at a threshold. `Resources` opens a menu. The dark footer and the centred sign-up card are
shared chrome and read identically wherever they appear.

**Density is comfortable.** The measure is capped so prose stays readable, and the colour
panels are generous, but the community grid and the studio's block list are efficient
rather than airy.

**Motion character: eased.** Movement is quiet and functional, with considered entrance
and exit easing, and one signature exception. When a cell recomputes, its background
pulses a near-white, soft amber and settles back to the page ground: that flash is the
whole product in one gesture, because it shows at a glance which parts of the page just
recalculated. The other named moments are a continuous horizontal marquee, a button press
that dips and returns, a scripted cursor that dips as it clicks, a stroke that draws
itself on, a terminal cursor that blinks, and an accordion that opens and closes by its
own height. One easing is the workhorse and the others are exceptions. Transitions are
declared per property, never as one blanket rule animating everything; a blanket rule is a
defect, not a shortcut.

**Scroll.** Three things move on the two long routes and none on the not-found screen. The
header recolours as described. A flowing strip of community examples, a carousel, translates
horizontally and advances continuously on a fixed one-minute loop, independent of how fast
the visitor scrolls. It is the one runtime animation on the site. And the hero carries a
live running visualization that animates its own marks and reveals its labels through
circular masks, holding sixty frames a second: it is a running graphic, not a recorded
clip.

**The notebook preview.** A rounded white card at the generous radius, holding a stack of
cells. An output cell renders a result: a scatter, a Sankey diagram, a typed table with
per-column headers and inline mini-histograms, a heatmap, a line chart or a force-directed
graph, its title set in `Source Serif Pro` italic. A code cell is a monospaced editor with
syntax highlighting, a left gutter carrying a pin and a code-toggle glyph, and a right
gutter carrying a run affordance. Three variants exist: the plain preview, a multiplayer
variant in which a second cursor edits a cell while its chart keeps up, and an embed
variant framed with a small attribution badge in its corner.

**Responsive behaviour** holds at four width tiers and at every width between them. Multi
column reflows to single column: the three feature cards stack, the colour panels move
their preview below their copy, and the community grid drops to one column. The
`Resources` menu collapses to a hamburger driving an accordion. Hover affordances are
gated so a touch device does not inherit hover-only behaviour, and one boundary is written
once in one unit rather than as two parallel sets.

**Accessibility floors**, which are contract rather than taste: contrast meeting WCAG AA
in both header states, which is the reason the header recolours at all; comfortably sized
touch targets; full keyboard navigation with visible focus rings; labels on icon-only
controls; and meaning never carried by colour alone. Menus and the mobile accordion are
operable from the keyboard and trap focus only while open. The live previews neither trap
keyboard focus nor autoplay motion for a visitor who has asked for less of it: under a
reduced-motion preference the marquee stills and the scripted cursor stops. The
announcement banner is dismissible and does not take focus when the page loads. The
monospaced face is decorative at display sizes, so body copy stays in `Inter` at `16px`
and up, and the whole site stays usable zoomed to twice its size.

What this must not look like: a page dominated by one hue family with no second signal, a
marketing composition where the working studio belongs, or decoration standing in for the
live previews that are the entire argument.

## Technical requirements

The app is server-rendered. Flask renders a complete page from its Jinja templates for
every route, so the browser receives finished HTML on first paint rather than an empty
shell it must fill; Alpine.js layers the interactive behaviour onto that markup - the
resources menu, the mobile accordion, the sort tabs, the grid and list toggle, the
dismissible banner and the studio's block editor - rather than replacing it. The datastore
is PostgreSQL at `DATABASE_URL`. Object storage is `minio` at `STORAGE_ENDPOINT` in the
bucket named by `STORAGE_BUCKET`, with `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`.
Authentication is email and password implemented by the app, with bearer tokens on the
JSON API. `GET /api/health` returns `200` once the app is ready. Request lines go to
standard output.

Use only the libraries named here plus their direct dependencies. Do not introduce a
second database, cache, queue, object store, identity provider or mail vendor - the only
backing services available in this environment are `postgres` and `minio`, and reaching
for anything else is a contract violation.

Read every host, port and credential from the environment. Never hardcode one, and never
let one reach the browser.

Visibility is settled by the server. Whatever a listing shows, a page and its media are
served or refused by the application, and a request that bypasses the interface entirely
gets the same answer.

Marketing content is served from the product's own store as ordered section blocks, so
copy and order change without a deploy. The community listing is a paginated, sortable
read over the notebook records. Account creation completes on this origin.

## Data model

Twelve tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture
data, not a secret. Hash it as normal; the exact literal must work at login, and it must
be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**`authors`** - `id`, `email` unique, `password_hash`, `display_name`, `created_at`.

**`readers`** - `id`, `email` unique, `password_hash`, `provider`, `created_at`. A reader
email is unique, and `provider` records which of the five methods created the account.

**`pages`** - `id`, `slug` unique, `title`, `meta_title`, `state` which is `draft` or
`published`, `owner_id`, `published_at`, `created_at`. A page is `draft` at creation. Its
slug never changes once it has been published. `published_at` is empty while it is a
draft.

**`blocks`** - `id`, `page_id`, `position`, `kind`, `eyebrow`, `heading`, `lead`, `body`,
`link_label`, `link_href`, `media_id`. `kind` is one of `hero`, `value_line`,
`feature_card`, `color_panel`, `community`, `testimonial`, `use_cases` and `cta`. Position
is unique within a page and contiguous from `1`, so a page never carries a gap or a
duplicate position.

**`media`** - `id`, `object_key` unique, `content_type`, `byte_size`, `sha256` unique,
`visibility`, `uploaded_by`, `created_at`. `visibility` is derived from the state of the
pages whose blocks reference the object rather than set on its own: an object referenced
only by draft pages is not publicly readable, and one referenced by any published page is.

**`notebooks`** - `id`, `slug` unique, `title`, `author_name`, `published_on`,
`star_count`, `comment_count`, `forked_from_id`, `thumbnail_media_id`. `star_count` and
`comment_count` are non-negative. `forked_from_id` references another notebook or is
empty, and never references its own row.

**`testimonials`** - `id`, `page_id`, `quote`, `person`, `role`, `link_href`, `position`.

**`use_cases`** - `id`, `page_id`, `label`, `position`.

**`footer_links`** - `id`, `column_name`, `label`, `href`, `position`.

**`signups`** - `id`, `reader_id`, `provider`, `created_at`.

**`newsletter_subscribers`** - `id`, `email` unique, `created_at`.

Derived rather than stored: a page's rendered markup, the listing's count line, and
whether a media object is publicly readable.

**Concurrency invariants**, stated as properties of the running system. Two simultaneous
publishes of one page must leave exactly one published page with one `published_at`, and
must not move an object twice. Two simultaneous signups with one email address must leave
exactly one reader row: one wins and the other is rejected. Two simultaneous uploads of
identical bytes to one page must leave exactly one media row and one object in the bucket.
Two simultaneous block insertions at one position must not leave a page carrying that
position twice.

**Seed data.** Seeding is idempotent: restarting the app must not duplicate rows.

Two authors, both with the password `deku-demo-pw-2026`: `author@example.com`, display
name `Mara Delgado`, owning the three published pages; and `author2@example.com`, display
name `Ines Bardot`, owning the one draft page. One reader, `reader@example.com`, with the
same password and provider `email`.

Four pages:

| Slug | Title | State | Owner |
|---|---|---|---|
| `home` | Datalume Notebooks: Fast data exploration and prototyping | `published` | `author@example.com` |
| `ai` | AI for data analysis | `published` | `author@example.com` |
| `top` | Discover our most popular data visualizations | `published` | `author@example.com` |
| `field-guide` | Datalume field guide | `draft` | `author2@example.com` |

Each page is seeded with its blocks in position order, and each carries one media object
at the key scheme above. The `field-guide` object is the boundary this task needs: it
exists in the bucket and is not publicly readable while the page is a draft.

Thirty-three notebooks. Nine are seeded by value, and under the default sort they are the
first nine of page one in this order:

| Slug | Title | Author | Published on | Stars | Comments | Forked |
|---|---|---|---|---|---|---|
| `d3-gallery` | D3 Gallery | D3 | 2026-06-12 | `1000` | `2` | no |
| `inputs` | Inputs | Ada Kovacs | 2018-01-25 | `991` | `18` | no |
| `learn-d3-introduction` | Learn D3: Introduction | D3 | 2020-03-24 | `755` | `3` | no |
| `datalume-and-creative-coding` | Datalume and Creative Coding | Noor Haddad | 2022-12-15 | `603` | `0` | no |
| `zoomable-sunburst` | Zoomable Sunburst | D3 | 2023-07-18 | `511` | `3` | yes |
| `datalume-plot` | Datalume Plot | Datalume | 2022-12-13 | `450` | `9` | no |
| `force-directed-graph-component` | Force-Directed Graph Component | D3 | 2023-09-27 | `418` | `12` | no |
| `enigma-machine` | Enigma Machine | Wren Alvarez | 2019-08-31 | `417` | `0` | no |
| `collapsible-tree` | Collapsible Tree | D3 | 2023-06-15 | `399` | `0` | no |

The remaining twenty-four carry distinct slugs, titles, authors and dates, and every one
of them has a star count below `399`, so the nine above are the top nine under the default
sort and the listing runs to a second page at `30` per page.

The four footer columns, the eight use cases and the two testimonials of the AI route are
seeded as rows rather than written into a template.

## Constraints

- The notebook application is out of scope. The reactive engine, the renderer, real-time
  multiplayer, the execution sandbox, data connectors, version history, forking and the AI
  canvas are described by the pages and built by nobody here.
- No payment, no pricing tiers, no billing. The footer links a pricing page; the site
  sells nothing.
- No search index. The not-found copy offers a search; the link points at the listing.
- No comment threads, no starring by a visitor, no following, no user profiles. Star and
  comment counts are seeded values the listing reads.
- Two roles only. No organisation, no team, no invitation and no role beyond author and
  reader.
- No real customer, testimonial or notebook-author identity. Every name in this brief is
  invented and must stay invented.
- No third-party analytics and no external network calls at run time beyond the two named
  backing services.
- No map renderer, no vector-animation runtime and no WebGL shader work. Where the
  reference used one of those elements decoratively, a static illustration replaces it;
  none is needed for this rebuild.
- No video. The multiplayer story is told by the scripted preview, never by a recorded
  clip.
- No native application and no application-store build.
- The app must stay responsive with a few thousand notebooks, a few hundred pages and tens
  of thousands of media objects.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT`
  is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root,
  empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the
  shell. An ordinary background job dies with its shell, and the app will not be running
  when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password` | the reader and a bearer token |
| `POST /api/auth/login` | `email`, `password` | the account and a bearer token |
| `GET /api/health` | none | a health object |
| `GET /api/pages/<slug>` | none | one published page with its blocks in position order |
| `GET /api/pages` | none | a top-level JSON array of the signed-in author's own pages |
| `POST /api/pages` | `slug`, `title`, `meta_title` | the created draft page |
| `PATCH /api/pages/<slug>` | any of `title`, `meta_title` | the updated page |
| `POST /api/pages/<slug>/publish` | none | the published page with its `published_at` |
| `POST /api/blocks` | `page_id`, `position`, `kind`, and the block's own fields | the created block |
| `PATCH /api/blocks/<id>` | any block field | the updated block |
| `DELETE /api/blocks/<id>` | none | the page's remaining blocks, repositioned |
| `POST /api/media` | the bytes, and `page_slug` | the media record with its `object_key` |
| `GET /api/media/<id>` | none | the object, or a refusal |
| `GET /api/notebooks` | optional `sort`, optional `page` | a top-level JSON array of notebooks with the range and total |
| `POST /api/signups` | `email`, `password`, `provider` | the reader |
| `POST /api/newsletter` | `email` | the subscriber |

Field names are exact. A successful call returns the named resource or shape. An invalid
or unauthorized call is rejected as a client error, never a `5xx` and never a silent
success, and carries a reason. Bearer auth is required on everything except
`POST /api/auth/signup`, `POST /api/auth/login`, `GET /api/health`,
`GET /api/pages/<slug>` for a published page, and `GET /api/notebooks`.

**No mocks.** An image written to the app's filesystem, a base64 string in a database
column, a data URI inlined into the page, a `media` row whose `object_key` names nothing in
the bucket, or a stubbed storage client that answers its own calls: each is a contract
violation however good the interface looks. The named provider is the fact - the app's UI
and its own tables can only reflect what lives in `minio`, never substitute for it.

## Definition of done

A visitor can read the home route, browse the community listing sorted by stars, page
through it, and create a free account from the card every call to action leads to. An
author can sign in to the studio, compose a page from ordered blocks, upload an image and
publish, and the image lives as a real object in the bucket at a key derived from its own
bytes. While the page is a draft neither it nor its image is readable by a signed-out
visitor, and publishing makes both readable without moving a byte.
