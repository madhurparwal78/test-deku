# Qualitative Fieldwork Agency

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser, read a published case study, scope a
multi-market study through the staged brief form and land on a confirmation carrying a quotable
reference, and an editor must be able to sign in and find that request already routed, already
staged and already carrying the right sensitivity, without hitting an error page. A different
stranger must NOT be able to read an unpublished article, the image behind it, or another client's
request by any means, including a direct request for it by its own path. The uploaded image bytes
must live in the object store at their scheme's key; a copy on the app's own disk does not count.

## Overview

Meridian Field is a global qualitative market research agency. It sells consumer fieldwork as a
project: a brand describes a business question, the agency designs the study, recruits people in the
relevant countries, moderates the sessions in local languages and reports back. There is nothing to
buy here, no plan ladder and no cart. The public site exists to explain thirteen research methods
and twelve industry sectors, prove reach across a country network, publish case studies, and move a
qualified stranger into a scoped request for quote.

The product is two things in one codebase. The public site is editorial: spacious, illustrated,
built to be found by a stranger typing a question into a search engine and to be read end to end.
The console behind it is operational: quiet, dense, built for staff who work a queue and publish the
estate the stranger arrived through. One action on the public site changes stored state, the brief
form, and everything else a visitor does is a read of published content.

It deliberately is not a research platform. There is no questionnaire builder, no fielding engine,
no transcript or video tool, no participant records, no consent capture, no incentive payment, no
partner portal and no site search. It sends no email, takes no payment and carries no second
language.

The genuinely hard part is that draft and published are the same records seen through different
eyes, and the boundary has to hold in three places at once: the public route, the list that feeds
it, and the bytes behind the image. An app that hides a draft in the interface while still serving
its path or its cover object to anybody who asks has painted the boundary rather than built it.

## User roles

Two roles.

| Role | Can do | Cannot do |
|---|---|---|
| `editor` | Sign in to the console; read every article in any status; create, edit and upload; publish and unpublish; work every opportunity, add notes and advance stages | **Cannot** be created by signing up, and **cannot** be granted by any request the app serves |
| `client` | Sign up; sign in; submit a brief; read the status and reference of their own requests | **Cannot** open any console route, **cannot** read an unpublished article or its image, **cannot** read or change another client's request, and **cannot** publish anything |

Anyone at all, signed in or not, may read every published route and may submit a brief. A visitor
who is signed in as a `client` has their request recorded against their account; a visitor who is
not gets the same reference and the same confirmation.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `client` session to any `editor`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged.

Signup is open and every self-served account is a `client`. There is no route, form or field by
which an account can choose or change its own role. Editor accounts are seeded.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Role | Seeded state |
|---|---|---|
| `editor@example.com` | editor | holds the `technology`, `gaming`, `beauty-cosmetics` and `pharmaceutical` sectors |
| `editor2@example.com` | editor | holds the `automotive`, `financial-services` and `hospitality` sectors |
| `client@example.com` | client | has one submitted request, against `pharmaceutical` |
| `client2@example.com` | client | has one submitted request, against `crypto` |

## Core features

### Accounts and sessions

The app implements its own accounts: email and password, with a bearer token the client sends on
every authenticated request. Passwords are stored hashed, never in plain text, and never returned
by any endpoint.

1. `POST /api/auth/signup` with an email and a password creates a `client` and returns a token. A
   second signup with an address already in use is rejected as invalid and creates nothing.
2. `POST /api/auth/login` with a seeded email and `deku-demo-pw-2026` returns a token. A wrong
   password is denied and returns no token.
3. A request that carries no token, or a token the app did not issue, is denied on every guarded
   endpoint, and the stored state is unchanged.
4. A signup body that names a role is accepted only as a `client`; the role in the body is ignored
   and the created account is a `client`.

### The editorial estate

Every public route renders from stored content records, not from hard-coded markup.

1. `/methodology` lists all thirteen methods and `/sectors` lists all twelve sectors, with no
   pagination, no truncation and no view-all control that hides members. Both header dropdown
   panels render the same full child sets.
2. `/methodology/<slug>` and `/sectors/<slug>` render one record each. A slug that matches no
   published record renders the not-found page and answers not-found.
3. `/services` lists the nine services with the two primary ones above the seven supporting ones:
   `Qualitative Research` and `Behavioural Analysis` are primary;
   `International Respondent Recruitment`, `Screener Design`, `Study Design`,
   `Discussion Guide Development`, `Desk Research`, `Analysis and Reporting` and
   `Translation and Transcripts` are supporting. Those nine names are also the choices the
   brief form offers at its second stage, read from the same records, so the site and the brief
   form can never advertise different work.
4. `/network` renders the country set as pins on the map and as a rail of country names beneath it.
   The rail is a real list in document order, reachable by keyboard, and every country on the rail
   links where its pin links. Below the primary threshold the map is decorative and the rail is the
   interface.
5. `/about-us` publishes the six process steps in order: `Brief`, `Select`, `Validate`, `Confirm`,
   `Execute`, `Report`. The console's opportunity stages use exactly these six names and no others.
6. The home route publishes the three figures `60+`, `400` and `50+` from stored records and never
   from a live count of anything.
7. Every internal link on every public route resolves to a route the app serves. A published
   record's body may not link to a path that does not exist, and publishing one is refused.

### The article library

1. `GET /api/articles` returns only articles whose status is `published`, newest first. A `draft`,
   `in_review` or `archived` article is absent from it for everyone, editor or not.
2. `/articles` filters on category and region. Each control is multi-select within itself and the
   two intersect across each other. The selection lives in the query string, so a filtered view
   survives a reload and can be shared.
3. Each filter option shows how many articles would remain if it were added to the current
   selection, and an option that would leave nothing is shown unavailable rather than hidden.
   Clearing every filter is one action, present whenever any filter is active.
4. With no results the index names the active filters, offers to clear them, and keeps a count
   visible reading zero, so a reader can see that the filter caused it.
5. `/articles/<slug>` renders a published article: its title, its one region and its one to three
   categories, its published date, its author and its body. The body is constrained to the reading
   measure and never runs the full grid width.
6. A request for an unpublished article's public path, `/articles/field-notes-from-lagos` among
   them, renders the not-found page and answers not-found for everyone who is not an editor. The
   response says nothing that distinguishes an unpublished record from a path that never existed.
7. An article card is one link. Its category and region chips are not links of their own, and
   filtering happens on the index rather than by activating a chip on a card. A card's accessible
   label reads `Read more about` followed by the article's own title.
8. A method route and a sector route each carry related articles chosen by shared tag, most
   recently published first, and a block with nothing to show is omitted rather than rendered
   empty.

### The staged brief and the request for quote

The brief form is the one public action that changes stored state. It runs across three stages,
each at its own address, so a half-finished brief can be returned to and the reader can see how
many stages remain.

1. `/contact` takes who is asking: full name, work email and company. `/contact/study` takes the
   shape of the study: one sector, one or more markets, one or more methods, one or more services,
   a sample size per market and a budget band. `/contact/question` takes the challenge in the
   client's own words and how they heard about the agency.
2. `POST /api/briefs` accepts the whole brief. Every field is validated again on the server: the
   sector must be one the site publishes, every market must be a seeded country, every method must
   be one of the thirteen, every service must be one of the nine, the challenge must run to at least
   twenty characters, and the work email must look like an address. An invalid brief is rejected, names the field that failed, and writes
   nothing at all.
3. A brief that names `Other` as how they heard about the agency must also carry the free-text
   companion field, and is rejected as invalid without it.
4. An accepted brief is acknowledged immediately with a reference beginning `MF-`, and
   `/contact/sent` shows that reference and states what happens next. The same reference is stored
   on the request and on the opportunity it opens.
5. **Submitting the same brief twice must not open a second opportunity.** The same work email with
   the same challenge text on the same UTC day resolves to the first request: the second submission
   is accepted, returns the first reference, and leaves exactly one stored request and exactly one
   stored opportunity. It is never a second row and never a second reference.
6. A brief submitted by a signed-in `client` is recorded against that account and appears at
   `/account/requests`. A brief submitted by a visitor who is not signed in is stored with no
   account and is not readable at `/account/requests` by anybody.
7. `GET /api/requests` returns only the requests belonging to the calling account. A `client`
   asking for another client's reference is answered as though it does not exist, and the other
   client's request is unchanged.

### Automated submission defence

1. The brief form carries one unattended decoy field, named `company_website`, which a person never
   sees and never fills. A submission that arrives with it filled is refused neutrally, stores no
   request and opens no opportunity.
2. A submitter posting the same form repeatedly in quick succession is refused after the third
   attempt within one minute and told when to try again. The refusal never accuses anybody and
   never discloses which check refused it.

### The opportunity board

1. An accepted brief opens exactly one opportunity, at stage `Brief`, carrying the brief's own
   reference.
2. Routing is deterministic and is recorded on the opportunity. When the brief's sector record
   names an owner, the opportunity is routed to that owner and its routing reason is stored as
   `sector_owner`. When the sector record names no owner, the opportunity is left unowned, its
   routing reason is stored as `no_sector_owner`, and it stays visible to every editor rather than
   disappearing into one person's list.
3. Sensitivity is copied from the sector record at the moment the opportunity is created. A brief
   naming `pharmaceutical` or `beauty-cosmetics` opens an opportunity whose sensitivity class is
   `elevated`; every other sector opens one at `standard`. It is never inferred from the wording of
   the challenge and is never left to be set by hand afterwards.
4. Stages advance forward only, one step at a time, through `Brief`, `Select`, `Validate`,
   `Confirm`, `Execute`, `Report`. A request to skip a stage, to move backwards, or to name a stage
   outside those six is rejected as invalid and the stored stage is unchanged.
5. An editor adds a note to an opportunity in the row itself, without leaving the board. The note
   records who wrote it and when, and notes are never edited or deleted once written.
6. The board is ordered by how long ago the brief arrived, oldest first, because the clock is the
   promise. Every card shows the reference, the company, the sector, the markets, the stage, the
   owner or that it is unowned, the sensitivity class and the elapsed time.
7. A `client` session is refused at every console endpoint, and the refusal leaves every
   opportunity exactly as it was.

### The editorial console and publishing

1. An editor creates an article as a `draft` from `/console/articles/new`, and a draft is readable
   in the console and nowhere else.
2. Publishing is refused, with the reason stated, when the article has no search description, when
   it has no body, or when its categories include `Case Studies` and it carries no client approval
   reference. The record stays a `draft` and no public route begins serving it.
3. A published article with a client approval reference on it, `CA-2026-014` on the seeded case
   study, is what a case study looks like when it is legal to publish.
4. Publishing sets the first-published moment once; a later edit updates the edited moment and
   never rewrites the first.
5. Unpublishing returns an article to `draft`, and its public path answers not-found again from
   that moment.
6. A slug is unique across articles, lowercase, hyphenated, and refused when it is already taken.

### Images and the object store

1. An editor uploads an article's cover through `POST /api/articles/{slug}/cover`. **The bytes are
   written to the object store at `STORAGE_ENDPOINT` in the bucket named by `STORAGE_BUCKET`, and
   nowhere else.** Bytes on the app's own filesystem, a blob inside a database column, or a
   placeholder shipped with the app are all failures of this rule however correct the page looks.
2. The object key is `articles/{article_id}/{sha256_of_bytes}.{ext}`, for example
   `articles/12/9f2ad0c7b3e54118a1c6d0b9f47e2a5c8d31be6079ff4a2c5e8b1d0473a69cf2.jpg`. The digest
   is of the bytes as uploaded, so uploading the same image to the same article twice leaves one
   object and one stored asset row, not two.
3. Cover bytes are served by the app at `GET /api/articles/{slug}/cover`, never from a public
   bucket address. A published article's cover is readable by anyone. **An unpublished article's
   cover is readable by an editor only: the same request from a client session, or with no session
   at all, is answered as though the object does not exist.**
4. Every uploaded image carries alternative text, or is explicitly marked decorative. An upload
   carrying neither is rejected as invalid and writes no object.
5. An upload from a `client` session is denied and writes no object.

### The cookie choice

1. A first-time visitor is asked once about non-essential cookies, in a panel carrying three
   categories: an essential one that is locked on, and two the visitor sets for themselves.
2. The decision is stored with a version and survives a reload: a visitor who has answered is not
   asked again on any later route in the same browser.
3. Every route's footer carries a `Cookie Preferences` control that reopens the panel, because
   withdrawing a decision has to be as easy as making it.

### When a page does not exist

1. An unknown address renders the agency's own not-found page and answers with a true not-found
   status, never a page claiming everything is fine.
2. That page carries a heading saying plainly that the page does not exist and a way back to each
   of `/`, `/methodology`, `/sectors` and `/articles`, plus the quote action.
3. There is no site search on it, because there is none anywhere else on the site.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | home: hero, four promise tiles, value strip, three figures, featured articles, client marks | public |
| `/services` | the nine services, two primary above seven supporting | public |
| `/methodology` | the thirteen methods as a two-column list of large rows | public |
| `/methodology/focus-groups` | one method, composed from content blocks, ending in an accordion | public |
| `/sectors` | the twelve sectors as a two-column list of large rows | public |
| `/sectors/pharmaceutical` | one sector, same composition, sector content | public |
| `/network` | the map, the country rail and the six regional bands | public |
| `/about-us` | mission, the six process steps, the comparison, the team | public |
| `/articles` | the filtered index of published articles | public |
| `/articles/five-markets-one-brief` | one published case study | public |
| `/contact` | brief stage one: who is asking | public |
| `/contact/study` | brief stage two: the shape of the study | public |
| `/contact/question` | brief stage three: the question itself | public |
| `/contact/sent` | the acknowledgement carrying the reference | public |
| `/privacy` | the privacy notice | public |
| `/signup` | open signup, mints a client | public |
| `/login` | sign in | public |
| `/account/requests` | the signed-in client's own requests, and nobody else's | client |
| `/console` | the opportunity board | editor |
| `/console/opportunities/MF-2026-00001` | one opportunity, its brief, its routing and its notes | editor |
| `/console/articles` | the editorial list, every record in every status | editor |
| `/console/articles/new` | create a draft | editor |

**Entry and redirects.** An unauthenticated request for `/console` or `/account/requests` lands on
`/login`, and signing in returns to the route that was asked for. A `client` session asking for any
`/console` route is refused rather than redirected into it. An editor signing in lands on
`/console`; a client signing in lands on `/account/requests`. Signing out returns to `/`, and the
same session then opens neither guarded surface. A token that has expired mid-action returns the
visitor to `/login` with what they typed still in the form. A request for an unpublished article's
public path answers exactly as a request for a path that never existed.

**Journeys.**

1. **Scope a study.** Open `/`, follow the `Speak their language.` tile to `/sectors`, open
   `/sectors/pharmaceutical`, follow its closing action to `/contact`, enter `Dana Whitfield`,
   `dana@example.com` and `Halcyon Labs`, continue to `/contact/study`, choose the
   `Pharmaceutical` sector, the markets `Germany` and `Japan`, the method `In-depth Interviews`,
   the services `Qualitative Research` and `Translation and Transcripts`, a sample size and a
   budget band, continue to `/contact/question`, write the challenge and choose
   `Perplexity` as how they heard, submit, and land on `/contact/sent` reading a reference
   beginning `MF-`.
2. **Work the queue.** Sign in as `editor@example.com`, land on `/console`, find the card carrying
   that reference with sensitivity `elevated` and owner `editor@example.com`, open it, add a note
   in the row, advance the stage from `Brief` to `Select`, and see the card carry the new stage.
3. **Publish a case study.** Sign in as `editor@example.com`, open `/console/articles`, create a
   draft, upload its cover, attempt to publish it as a `Case Studies` article with no client
   approval reference and read the stated refusal, add the reference, publish, then open its public
   path and find it live and listed in `/articles`.
4. **Filter the library.** Open `/articles`, select the `Case Studies` category, watch the count
   fall and the address carry the selection, reload and keep it, then clear it in one action.
5. **Stay in your own lane.** Sign in as `client2@example.com`, read one request at
   `/account/requests`, ask for the other client's reference directly and be answered as though it
   does not exist, then ask for `/articles/field-notes-from-lagos` and its cover and be answered
   the same way.

**States.** Every list has an empty state, every route has a loading state, and no failure takes a
route down with it. The filtered index with no results names the active filters and offers to clear
them. A related block with nothing to show is omitted rather than rendered as an empty heading.
In-place content settles as a skeleton at the destination's own shape rather than a spinner, so a
grid does not collapse and expand under a reader about to click. The board with nothing open says
so plainly and points at the editorial list. A stage change the store refuses returns the row to
its previous stage and states beside it what failed. Every form keeps what was typed when a
submission fails.

## UI/UX notes

**North star.** Somebody arriving should understand within one screen that this agency talks to
real people in their own countries, and should feel that the work is done by hand rather than
harvested. **Register.** The public site is editorial and carries atmosphere, with the subject seen
first; the console is operational and carries none, built for scanning and repeated action. Two
stances hold the whole product together and a competing agency could rationally invert either:
**space over dividers** on the public site, and **information over atmosphere** in the console.

**Mode.** Committed to light and designed fully in light. There is no dark mode to grade.

**Palette by role.** The page ground is a near-white warm neutral, nearer paper than white, and a
second ground one step darker than it carries alternating bands, separators and secondary controls;
a third, a light warm neutral, is the ground a secondary control moves to when it is pointed at.
Every glyph on the site is a deep warm neutral, never a true black, and the two grounds must stay
visibly separate from each other without a rule between them. Cards, the header bar and form
controls sit on a near-white neutral. The primary accent is a light, soft green: it grounds the
home hero edge to edge, it carries the logo mark, and it is the only accent allowed to own a whole
surface. Three further accents each own one thing and appear nowhere else: a light, vivid cyan on
the quote action and one promise tile, a mid, vivid amber on the carousel and dropdown affordances
and one promise tile, and a light, vivid red on one promise tile, on the required-field marker and
on the border of a field that has been filled in wrongly. A near-white, muted violet belongs to the
illustrations and to one promise tile and is never a control anywhere else. Each accent moves one
step darker when it is pressed. A surface wearing the green is not also wearing the cyan: accents
are used one at a time. Button labels are a near-black neutral while body copy is the deep warm
neutral, and that difference is a deliberate weight lift on anything a reader can act on, not an
inconsistency to tidy away. The exact shades are yours, so long as each meaning keeps its colour
exclusively and the contrast floors below hold.

**Type.** `Space Grotesk` carries every character on the site, in two real weights: the normal
weight the product treats as its body weight, and a heavier one used only for emphasis inside
running copy. A system sans stands behind it so a failed font load never blocks text. Nothing is
sized to a fixed step: every size interpolates between a narrow-screen value and a wide-screen
value, so body copy settles at `1rem` on a handset and `1.0625rem` on a wide screen, and the hero
display runs from `3.625rem` up to `10.875rem`. Line height is a multiplier rather than a length:
body copy at `1.5`, the hero display at `1`. Long-form copy is capped at a reading measure of
`48rem` and never runs the full grid width. Figures line up on tabular numerals wherever amounts or
counts stack, which here means the three published figures and every column in the console. The
full scale is in the front-end specification below.

**Motion.** Two characters and nothing else. Reveals and large moves are `eased`: a strong start
and a long settle, so movement reads as designed rather than mechanical. Anything a pointer can
touch overshoots its end value and springs back, which is what makes this site read as made by
people rather than assembled. Entrances are one of five patterns: `fade-rise` for body copy and
card text, `scale-settle` for illustrations, `ground-grow` where a coloured panel grows out from
nothing behind the text, `stagger-three` where three items arrive a beat apart, and `split-line`
where a heading assembles word by word. `ground-grow` is the home route's dominant entrance and a
fade does not read as it. Looping movement exists in three places only, the drifting image lanes,
the country rail and the wobbling underline beneath an emphasised phrase, and each one pauses when
it leaves the screen, pauses when the document is hidden, and pauses under a pointer so a mark can
be read. The lanes run at deliberately different speeds; matched speeds make five columns read as
one sliding block. Under `prefers-reduced-motion` every entrance resolves at once to its end state,
all looping movement stops on its first frame, the rail becomes a plain scrollable list and the
first-load sequence becomes a plain fade; content is never hidden behind an animation that does not
run, and the small hover response stays, because it is how a reader knows a control is a control.
The console does not borrow the public site's character: nothing there bounces, and a transition
that draws attention to itself while somebody is reading a queue has failed.

**Density and layout.** The public site is spacious: one thing dominant per view, sections separated
by space rather than by rules, and a hairline only where two sections share a ground. Its chrome is
a floating capsule inset from both edges and sitting a little below the top of the window, holding
the logo, four navigation items and a detached quote action; two of those items open a panel
listing their full child set. The capsule never shrinks, fades or changes height as the page moves
under it, and that stillness is the design. The console inverts all of it: its layout archetype is
a persistent sidebar, its working surface is a card grid of open opportunities, and rows sit tight
enough that a full queue is read without scrolling. Creating anything in the console happens in the
row itself, so the queue never disappears while it is being worked, and a change lands in the list
immediately and is reconciled against what the store accepted; when the store refuses, the row
returns to its previous state and says beside itself what failed.

**Components.** Every control carries resting, pointed-at, pressed, focused and unavailable states,
and unavailable is never signalled by colour alone. The button's signature is a circular icon disc
at one end: at rest the disc sits in place, and on hover it drops away while a second disc rises
into place and settles. The navigation item grows a soft capsule behind its label from undersized
and invisible; the current route wears that capsule permanently and without animation, so the site
never shows two. Escape closes any open panel and returns focus to whatever opened it. Every form
control carries a persistent visible label, never a placeholder standing in for one, and a field in
error carries an icon and a message beside it rather than a colour alone.

**Accessibility floors, which are contract rather than taste.** The product meets WCAG 2.1 level AA
and the console is held to the same bar, because that is where this gets skipped and where staff
spend the day. Body text reaches at least `4.5:1` against its ground, and large display text,
interface components and the focus ring reach at least `3:1`. Every route carries a skip link as
its first focusable element, the four landmarks, exactly one level-one heading and no skipped
level. Keyboard navigation reaches every control, including the dropdown panels, the filter panel,
the accordion and the card grid, and the visible focus ring is never removed anywhere. Any heading
split into words for its entrance also exists once as a single string for assistive technology, or
a quarter of this site's headings become a stream of disconnected words. Every content image
carries alternative text and decorative images declare themselves decorative. Nothing flashes more
than three times a second.

**Responsive.** The site reflows rather than hides: nothing on a handset is missing that a wide
screen has. Above the primary breakpoint the header carries its navigation list and its panels, the
article grid runs three across, the paired brief fields sit side by side, the comparison stays two
columns and the map is the interface. Below it the navigation collapses into a slide-in panel whose
two dropdowns become accordions, the grid steps down, the paired row unstacks, the comparison
becomes two sequential lists with their own headings, and the country rail becomes the interface.
At the narrowest the grid is one column and the section navigation becomes a labelled scrollable
row. The middle width between handset and wide screen is where this design is tallest and it is the
one to check first. No route scrolls sideways at the narrowest supported viewport at four times
zoom, and the only horizontal scroll regions anywhere are the marquee track, the carousel and that
section navigation row.

**What it must not look like.** Not a page dominated by one hue family with no second signal. Not
decoration standing in for content. Not a marketing composition where the console belongs, and not
the console's density where the editorial routes belong. Not a product whose state has to be
inferred from a colour swatch with no word beside it.

## Technical requirements

Front end: HTMX over server-rendered templates, so every route is a complete document that works
with scripting switched off, and enhanced interactions swap a fragment in place rather than
replacing the page. Back end: Express on Node 20, rendering documents through Nunjucks templates
and serving the HTTP API on the same origin under the `/api` prefix. The browser receives rendered
markup on first paint, not an application shell, and only the article filter, the carousel controls
and the map pins degrade to a plain form or a plain list when scripting is unavailable. Store:
PostgreSQL, reached at `DATABASE_URL`, which the environment also exports as `DB_URL` with the same
value. Objects: MinIO, reached at `STORAGE_ENDPOINT` with the bucket named by `STORAGE_BUCKET` and
the credentials `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Auth: app-implemented email and
password with bearer tokens, passwords stored hashed. Health: `GET /api/health` returns `200` once
the app is ready.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing services
available in this environment are PostgreSQL and MinIO, and reaching for anything else is a
contract violation.

PostgreSQL and MinIO are already running and reachable at those variables. Do not download,
install, compile or start a copy of either, and never hardcode a host, a port or a credential that
the environment supplies.

Machine-readable surfaces: every public route serves its own title and its own meta description and
no two routes share either; a route title reads as the route's own name, then a separator, then
`Meridian Field`. Nothing the browser downloads carries a credential, a bucket key or a token.

All timestamps are UTC and are sent as ISO 8601 strings ending in `Z`.

## Data model

Thirteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**`account`** - `id`, `email` unique, `password_hash`, `display_name`, `role` which is `editor` or
`client`, `created_at`. Two addresses can never share an account: the second insert of an address
already stored is refused rather than accepted.

**`method`** - `id`, `title`, `slug` unique, `short_name`, `summary`, `menu_order`, `status`.
Thirteen rows.

**`sector`** - `id`, `title`, `slug` unique, `short_name`, `summary`, `menu_order`,
`sensitivity_class` which is `standard` or `elevated`, `owner_email` which may be empty, `status`.
Twelve rows.

**`service`** - `id`, `name`, `kind` which is `primary` or `supporting`, `rank`, `body`. Nine rows,
ranked so the two primary ones sort above the seven supporting ones.

**`region`** - `id`, `name`, `slug` unique, `has_band`, `band_order`. Seven rows.

**`country`** - `id`, `name`, `iso_code` unique, `region_id`, `map_x`, `map_y`, `is_featured`,
`timezone`. The two coordinates are decimals between zero and one, resolved against the map
artwork's own box, so a new market is added as a record rather than as code.

**`category`** - `id`, `name`, `slug` unique. Five rows.

**`article`** - `id`, `title`, `slug` unique, `summary`, `body`, `region_id`, `author_name`,
`status` which is one of `draft`, `in_review`, `published` or `archived`, `seo_description`,
`client_approval_reference` which may be empty, `cover_key` which may be empty, `is_featured`,
`published_at` set once at first publish and never rewritten, `updated_at` maintained on every
edit. An article carries exactly one region.

**`article_category`** - `article_id`, `category_id`. An article carries one to three categories and
the same category never appears twice on one article.

**`brief`** - `id`, `reference` unique, `full_name`, `work_email`, `company`, `sector_slug`,
`markets`, `methods`, `services`, `sample_size`, `budget_band`, `challenge`, `attribution_key`,
`attribution_detail`, `account_id` which may be empty, `dedupe_key` unique, `submitted_at`. The
dedupe key is derived from the lowercased work email, the challenge text and the UTC date of
submission, and the store holds one row per key: a same-day resubmission of the same brief by the
same address resolves to the row already there rather than adding a second.

**`opportunity`** - `id`, `brief_id` unique, `reference` unique and equal to its brief's reference,
`stage` which is one of `Brief`, `Select`, `Validate`, `Confirm`, `Execute` or `Report`,
`owner_email` which may be empty, `routing_reason` which is `sector_owner` or `no_sector_owner`,
`sensitivity_class` which is `standard` or `elevated`, `created_at`, `updated_at`. Exactly one
opportunity exists per brief and a second can never be created for the same one.

**`opportunity_note`** - `id`, `opportunity_id`, `author_email`, `body`, `created_at`. Append only:
no route updates or deletes a note once written.

**`content_asset`** - `id`, `object_key` unique, `article_id`, `content_type`, `byte_size`,
`alt_text`, `is_decorative`, `uploaded_at`. One row per object key, so the same bytes uploaded to
the same article twice leave one object and one row.

**`site_setting`** - `key` unique, `value`. Carries the three published figures, the availability
line and its expiry date, and the site name `Meridian Field`.

Derived rather than stored: the filter counts on the article index, the elapsed time on an
opportunity card, whether an office is currently open, and the related-article selections. None of
them is a column.

**Seed data.** The thirteen methods are `Online Bulletin Boards`, `Focus Groups`, `Taste Testing`,
`Central Location Testing`, `Customer Intercept`, `Online Diary`, `Mystery Shopping`, `Shop-Along`,
`UX Research`, `In-depth Interviews`, `Ethnographic Research`, `Dyads and Triads` and
`Co-Creation Workshops`, each with its own lowercase hyphenated slug. The twelve sectors are `Automotive`,
`Technology`, `Sports`, `Gaming`, `FMCG`, `Food and Beverage`, `Financial Services`,
`Beauty and Cosmetics`, `Crypto`, `Hospitality`, `Consulting` and `Pharmaceutical`, of which
`Beauty and Cosmetics` and `Pharmaceutical` carry `elevated` sensitivity and the rest carry
`standard`. The
seven regions are `The Americas`, `APAC`, `The Middle East`, `Europe`, `East Asia` and `Africa`,
each with a band in that order, plus `Worldwide`, which has none. The five categories are `Case
Studies`, `Educational`, `Industry Insights`, `Customer Insights` and `Methodology`. Twenty-four
countries are seeded, twenty-two of them featured on the rail, including `Germany`, `Japan`,
`Nigeria` and `Brazil`. The eleven attribution options are seeded with stable keys, ending in
`Other`, which requires its companion field.

Seven articles are seeded, six `published` and one `draft`:

| Title | Slug | Region | Categories | Status |
|---|---|---|---|---|
| `Five Markets, One Brief` | `five-markets-one-brief` | `Worldwide` | `Case Studies` | published, approval `CA-2026-014`, featured, has a cover object |
| `What Shoppers Say Versus What They Do` | `what-shoppers-say-versus-what-they-do` | `Europe` | `Educational`, `Methodology` | published, featured |
| `Recruiting Clinicians Without Losing Them` | `recruiting-clinicians-without-losing-them` | `APAC` | `Industry Insights` | published, featured |
| `Shade Ranges and Skin Tones` | `shade-ranges-and-skin-tones` | `The Middle East` | `Customer Insights` | published, featured |
| `Running Focus Groups Across Time Zones` | `running-focus-groups-across-time-zones` | `The Americas` | `Methodology`, `Educational` | published |
| `Why Gamers Answer Differently at Midnight` | `why-gamers-answer-differently-at-midnight` | `East Asia` | `Industry Insights`, `Customer Insights` | published |
| `Field Notes From Lagos` | `field-notes-from-lagos` | `Africa` | `Educational` | draft, has a cover object |

Two briefs are seeded with their opportunities: `client@example.com` against `pharmaceutical`,
which is `elevated`, owned by `editor@example.com` and stored with routing reason `sector_owner`;
and `client2@example.com` against `crypto`, which is `standard`, unowned and stored with routing
reason `no_sector_owner`. The first carries the reference `MF-2026-00001` and the second
`MF-2026-00002`; references issued afterwards continue that sequence.

Six client marks, three team members and two offices, `London` and `Singapore`, are seeded with
their time zones.

Seeding must be idempotent - restarting the app must not duplicate rows, and must not write a
second copy of a seeded object into the bucket.

## Front-end specification

The visual detail the six sections above state as intent, written out surface by surface. Nothing
here is decoration: every paragraph describes something a reader can see and a reviewer can reject.

**The type scale, carried exactly.** Each step interpolates between its narrow-screen value and its
wide-screen value, and the root size interpolates with them, so every length on the site scales
from one number rather than jumping at fixed steps.

| Step | Narrow screen | Wide screen |
|---|---|---|
| Small print, chips, captions | `0.75rem` | `0.875rem` |
| Body copy and button labels | `1rem` | `1.0625rem` |
| Lead paragraph | `1.1563rem` | `1.1875rem` |
| Smallest heading | `1.5rem` | `1.5rem` |
| Card and section heading | `1.5rem` | `1.75rem` |
| Block heading | `1.625rem` | `2.375rem` |
| Route section heading | `2.125rem` | `3.125rem` |
| Route heading | `2.75rem` | `4.75rem` |
| Display heading | `3.4375rem` | `7.5rem` |
| Hero display | `3.625rem` | `10.875rem` |

Body copy sits at a line height of `1.5` and the hero display at `1`. Long-form copy holds a
reading measure of `48rem`.

**Shape and grid.** The layout is a sixteen-column grid, not twelve, because the asymmetric splits
on the promise tiles and the regional bands do not resolve on twelve. One base unit governs every
gap, gutter and margin, and every spacing value is a multiple of it. Four shapes exist and stay
distinct from one another: a small softening on controls and small cards, a larger one on card
images and feature panels, a full capsule on navigation pills and the header bar, and a circle on
client marks and icon discs. The exact radii are yours as long as those four stay unmistakably
different.

**The header.** A white capsule floating clear of all four edges, carrying three separated groups:
the logo lockup, the four navigation items, and the quote action in a detached capsule of its own.
That separation is the only hierarchy in the header and it must survive. The logo is two marks in
one link: a glyph that keeps the green accent on every ground, and a wordmark that takes the
current foreground. The bar sits over the green on the home route and over the page ground
everywhere else, and it does not shrink, fade, change height or change ground as the page moves
under it.

**The two panels.** `Methodology` and `Industry Sectors` each open a panel listing their full child
set beside a dark promotional panel whose image sits slightly beyond its frame and settles back as
the panel opens. The list items enter staggered from just below their rest position. A panel opens
on pointer enter and on keyboard activation, closes on pointer leave of both the item and the
panel, on Escape, on focus leaving forwards and on a route change, and holds open briefly on leave
so the diagonal path from the label to the panel does not dismiss it. Only one panel is open at a
time and a closed panel is inert to assistive technology. On a touch pointer the first tap opens
the panel rather than navigating, and the panel's own all-items link keeps the index route
reachable.

**The button.** One component. A label, and a circular icon disc at one end. At rest the default
disc sits in place and a second disc waits above it at no size at all; on hover the first drops
away as it shrinks while the second rises into place and overshoots slightly before settling, and
the label shifts to clear the disc without a second layout pass. Five variants exist and which
colour goes where is fixed: the green carries the quote action, and the cyan, the amber, the red
and the violet each carry exactly one promise tile. A pressed button takes its own darker step.

**The home route.** Nine stacked sections in this order: the hero on green running full bleed
behind the floating header; the illustrated timeline carrying the four promise tiles; a closing
invitation inside the timeline; the three-value strip; the figures block; the featured articles;
the client mark wall; the closing panel; the footer. The hero carries a two-line display heading, a
subheading, one paragraph and an illustration entering from below the fold, and it scales down
slightly as it leaves before holding. Because the display heading is split into words for its
entrance, the same heading exists once more as a single string for assistive technology; both are
required. The four tiles are one component wearing four accents and pointing at four routes:
`No more chaos.` to `/services`, `One brief. One team.` to `/methodology`, `Speak their language.`
to `/sectors` and `Global, for real.` to `/network`. Each tile reveals with two ground layers, the
coloured one and the white one, growing together from nothing behind the text, with the description
and the action fading up a beat later. The three figures arrive one after another a beat apart. The
client mark wall is a marquee of circular discs which show a mark's name as text where it has no
image.

**The method and sector routes.** Long documents, ten to fourteen screens, composed from an ordered
list of content blocks rather than a fixed template, so two of them need not carry the same
sections in the same order. The block kinds are rich text with emphasis and links, a heading with
two to six points, a ticked variant of that, prose carrying the published figures, a related
article, a question-and-answer accordion, a call to action in one accent, a full-width image, and
the link list the two index routes use. An emphasised phrase inside running copy carries a
hand-drawn wobbling underline, chosen phrase by phrase by whoever writes it; that emphasis is
presentational and is never announced as stress, or a screen reader shouts nine times a paragraph.
Each accordion question is a control carrying its own expanded state and naming the region it
controls, more than one may be open at once, opening one never closes another, its height animates
except under reduced motion, and a direct link to a question opens it and scrolls it clear of the
floating header.

**The network route.** A hero of four short lines, then a positioning sentence that assembles word
by word as it passes and also exists once as a single string. The map is a filled world silhouette
in the second ground on the page ground, no borders, no labels, no graticule, shown through a
circular window so the artwork is wider than its frame. A pin rests undersized and grows to full
size on hover or on focus, its label sliding in from the left and its small panel dropping in from
above. Beneath it the rail of country names slides endlessly past and is a real keyboard-reachable
list in document order. The five value cards sit in a horizontally scrollable track with snap
points that works with no script, with previous and next controls that move by one card and become
unavailable at each end, arrow-key support on the track, no autoplay, and the set announced as a
list with its length. The six regional bands alternate grounds, each carrying prose, a photograph
tilted about ten degrees alternating direction band by band, and one related article.

**The about route.** Its hero is five lanes of drifting images, each image fading out toward the top
and bottom of its lane rather than being cut at a hard edge. A section navigation sticks below the
header once its origin is passed, marks the section being read, is a labelled navigation landmark
holding in-page links, carries its current marker as something other than colour alone, offsets its
anchors clear of the header, and becomes a labelled scrollable row at the narrowest widths. The
comparison block stays a genuine two-column comparison on a wide screen and becomes two sequential
lists with their own headings below the primary threshold, because the pairing is the meaning.

**The article index.** A card grid three across on a wide screen, and a filter bar floating as a
white capsule near the foot of the viewport carrying the two controls, each showing its live count
beside its label. Below the primary threshold that bar becomes a trigger opening a full-height
panel which traps focus, applies on close, and shows the resulting count on its apply control
before the reader commits. A card is one link: chips over the image, title beneath it, and an image
that sits slightly oversized inside its clipped frame and settles toward true size on hover, so the
crop breathes without the card moving. Building that the other way round, scaling up from true
size, tears the crop at the frame.

**The article detail.** Title, region and category chips, published date and author, the lead
image, the body at the reading measure, and a link to the next article. An edited date is shown
separately only when it differs from the published date by more than a day. An author whose team
record is unpublished renders as plain text rather than as a link.

**The brief form.** Three stages, each its own document with its own heading and its own place in
the address, and each stating which stage it is and how many remain. Stage one is who is asking,
stage two is the shape of the study, stage three is the question itself. The paired fields sit side
by side above the primary threshold and unstack below it. Every control carries a persistent
visible label, and the required marker is the red accent. Validation runs when a field is left
rather than on the first keystroke, and once a field has failed it is rechecked on every change. A
free-mail work email raises a note at the field and is never refused. The submit control is never
disabled, because a disabled control that will not explain itself is worse than a refusal;
activating it with errors present moves focus to the first field in error and announces how many
there are. A slow submission says so politely rather than sitting silent, a refused one keeps every
value the visitor typed, and a failed one states the failure plainly with a reference and offers
the direct mail address as the way round. The decoy field is present in the markup, reachable by
nothing a person uses, and labelled for assistive technology as one to leave empty.

**First load and route change.** The first document of a session paints behind a cover: the agency
mark draws itself on as a line, a dot arrives, and the cover wipes upward to reveal the page with a
softening curve at the wiping edge rather than a straight shutter line. Only then do the page's
reveals run. The cover never blocks: if loading runs long it lifts anyway against whatever has
painted. After that first document a same-origin navigation replaces the main region while the
header, the panels and the consent layer stay exactly where they are; the document's title and
description are replaced with the new route's own, reveal observers are rebound against the new
content, looping movement is restarted, scroll goes to the top or is restored on a backward
navigation, focus moves to the new document's first heading, and a polite announcement names the
new page. A navigation that fails, a cross-origin target or a modified click falls back to an
ordinary navigation. A progress indicator appears only when a transition runs long, because below
that it flashes and reads as a fault.

**Scroll.** Wheel and trackpad scrolling is smoothed with inertia while keyboard, scrollbar and
anchor navigation stay exact; smoothing is off under reduced motion, never runs inside a nested
scroll region, and never runs while the navigation panel or the consent layer is open. Elements
reveal on arrival, once, and hold: nothing reverses on scroll up, elements in a group fire together
with their stagger, and if the observation mechanism is unavailable everything resolves to its end
state rather than staying invisible. The home route's illustrated scene is the one position-linked
surface: its decorative layers tilt and drift at different rates through their own passage, and it
sheds parallax layers rather than content at the narrowest widths. In-page anchors land clear of
the floating header and move focus to the target as well as scrolling to it.

**Focus.** A focused control carries a visible ring offset from its own edge, in the foreground
colour on light grounds and in white on the green and on the dark promotional panel. The ring is
shown for keyboard focus and suppressed for pointer focus, and it is never removed anywhere,
including inside the navigation panel and the consent layer. A focused navigation item shows its
capsule at full size plus the ring. A focused button shows the ring and does not fire the icon
swap, because that swap is a pointer affordance and firing it on focus produces movement the
keyboard user did not ask for.

**The console.** A persistent sidebar naming its two surfaces, the board and the editorial list,
with the current one marked by more than colour. The board is a card grid, oldest brief first, each
card carrying the reference in the first line, then the company, the sector, the markets, the
stage, the owner or `unassigned`, the sensitivity class as a word beside its colour, and the
elapsed time since the brief arrived. A stage advances from the card itself and the card updates at
once, reverting with a message beside it if the store refuses. A note is written in the card and
appears above the previous note without the board reloading. The editorial list is a real table
with row and column headers, its sortable columns announce their sort state, its bulk selection
announces its count, and a refused publish states which rule refused it. Nothing in the console
animates beyond the plainest change of state.

**Empty, loading and error states.** In-place content settles as a skeleton at the destination's
own shape, never a spinner, because a spinner in a card grid collapses the layout and then expands
it under a reader about to click. A listing beneath a filter keeps its count visible at zero. A
collection that fails to load says so, offers a retry, and leaves the rest of the route standing. A
server failure renders the same layout as the rest of the site with a distinct message and a
quotable reference, carries no technical detail, and renders without a data dependency, because it
is what shows when the data dependency is what failed.

**The footer.** Identical on every route: a closing invitation carrying the quote action, the link
list, two office blocks each carrying its city, address, working hours and the office's current
local time with whether it is open now, and a baseline with the copyright line. The `Cookie
Preferences` control sits in that link list on every route and is a button rather than a link.

## Constraints

- One agency, one site, one console. No second tenant, no client workspaces, no per-client login
  beyond the request list described above.
- No research delivery: no questionnaire builder, no fielding engine, no transcripts, no session
  recordings, no media of any kind beyond the images an editor uploads, no participant records, no
  consent capture for participants, no incentive payments and no partner portal.
- No payments, no invoicing, no plans, no subscriptions and no cart.
- No email, no SMS and no push. A submitted brief is acknowledged on the screen, never in an inbox.
- No third-party analytics, tag manager, bot-defence service, booking page or external content
  platform. The content records live in this app's own store and nothing on any route calls out to
  another service at runtime.
- No site search, no comments, no likes, no follows, no messaging and no public profiles.
- One language, English, and one currency-free commercial surface: a brief carries a budget band,
  never a price.
- No native app and no offline mode.
- The app stays responsive with the seeded estate plus a few hundred articles, a few thousand
  stored requests and their opportunities.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses.
  Read both from the environment; never hardcode either.
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

**API shapes.** Field names are exact. A list endpoint returns a top-level JSON array. A successful
call returns the named resource or shape; an invalid or unauthorized call is rejected as a client
error, never as a server error and never as a silent success, and carries a message naming the
reason.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | - | `status` |
| `POST /api/auth/signup` | `email`, `password`, `display_name` | `access_token`, `email`, `role` |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `email`, `role` |
| `GET /api/methods` | - | `title`, `slug`, `short_name`, `summary`, `menu_order` for all thirteen |
| `GET /api/sectors` | - | `title`, `slug`, `short_name`, `sensitivity_class`, `menu_order` for all twelve |
| `GET /api/services` | - | `name`, `kind`, `rank` for all nine |
| `GET /api/countries` | - | `name`, `iso_code`, `region`, `map_x`, `map_y`, `is_featured` |
| `GET /api/articles` | `category`, `region` | published articles only: `title`, `slug`, `summary`, `region`, `categories`, `published_at`, `cover_url` |
| `GET /api/articles/{slug}` | - | one published article in full, or not found when it is not published |
| `POST /api/articles` | `title`, `slug`, `summary`, `body`, `region`, `categories`, `seo_description`, `client_approval_reference` | the created `draft` |
| `PATCH /api/articles/{slug}` | any of the above | the updated article |
| `POST /api/articles/{slug}/cover` | the image bytes, `alt_text` or `is_decorative` | `object_key`, `content_type`, `byte_size` |
| `GET /api/articles/{slug}/cover` | - | the stored bytes, or not found when the article is not published and the caller is not an editor |
| `POST /api/articles/{slug}/publish` | - | the published article, or a refusal naming the rule that refused it |
| `POST /api/articles/{slug}/unpublish` | - | the article, back at `draft` |
| `POST /api/briefs` | `full_name`, `work_email`, `company`, `sector_slug`, `markets`, `methods`, `services`, `sample_size`, `budget_band`, `challenge`, `attribution_key`, `attribution_detail`, `company_website` | `reference`, `submitted_at`, and per-field errors when it is invalid |
| `GET /api/requests` | - | the calling account's own requests: `reference`, `company`, `sector_slug`, `stage`, `submitted_at` |
| `GET /api/opportunities` | `stage`, `owner` | every opportunity, oldest brief first: `reference`, `company`, `sector_slug`, `markets`, `stage`, `owner_email`, `routing_reason`, `sensitivity_class`, `submitted_at` |
| `GET /api/opportunities/{reference}` | - | one opportunity with its brief and its notes |
| `PATCH /api/opportunities/{reference}` | `stage` | the opportunity at its new stage, or a refusal leaving the stored stage unchanged |
| `POST /api/opportunities/{reference}/notes` | `body` | the created note with `author_email` and `created_at` |
| `POST /api/consent` | `essential`, `analytics`, `preferences`, `version` | the stored choice |

Bearer auth is required on everything except `GET /api/health`, the public read endpoints, both
auth endpoints, `POST /api/briefs` and `POST /api/consent`.

**No mocks.** MinIO is the only place an uploaded image exists. An in-memory list of uploads, a
base64 string in a database column, a file written under the app's own directory, a placeholder
image shipped with the app, or a cover route that answers with bytes it generated itself are all
the same failure wearing different clothes. The named provider is the fact - the app's UI and its
own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A stranger can read any published method, sector or case study, scope a multi-market study through
the three brief stages, and leave with a reference they can quote. An editor signs in and finds
that request already in the console, routed by its sector, staged at `Brief`, and elevated when the
sector is one of the two that carry it. An unpublished article and the image behind it stay
unreadable to everyone but an editor, at their own paths, and every image an editor uploads lives
in the object store.
