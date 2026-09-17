# Spectre Studio Showcase

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, drag the wall of
published work, open a project, and send a routed enquiry that comes back with a reference,
without hitting an error page. A different stranger must NOT be able to reach a project the
studio has not published yet, or the image bytes behind it, by any means, including a direct
request to the route that serves those bytes. That boundary cannot be faked in the app itself:
the uploaded bytes must live in the `minio` bucket at their scheme's key, and a copy kept on
the app container's own disk does not count.

## Overview

Spectre Studio Showcase is the public site of a technology-led creative studio and the small
publishing console behind it. Clients, candidates and press come to see the work; the studio's
curator adds a project, puts its image in the object store, and decides when it becomes visible.

The public half is a portfolio that behaves like a piece of work rather than a page about one:
the home route is a draggable, throwable wall of published projects, with an about narrative, a
careers route and a three-step enquiry. It is deliberately not a client portal, not a blog and
not a content-management system, and it has no comments, no likes and no payment.

The hard part is the seam: an unpublished project and its stored image must be unreadable to
everyone but a signed-in curator, on direct request and not only by omission from a list.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `visitor` | Read published projects and their images, open roles, the configuration. Submit an enquiry. Submit a wildcard application with one file. | **Cannot read a draft project or the image bytes behind one. Cannot read a closed role. Cannot create, upload to, or publish a project. Cannot read either inbox.** |
| `curator` | All of that, plus create a project, upload its thumbnail, publish it, read every project including drafts, read closed roles, read both inboxes. | **Cannot be created by signup.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI
is not authorization: a direct API call from a `visitor` session to any `curator`-only endpoint
must be rejected by the server (an unauthorized request is denied, not served), leaving the
protected state unchanged.

Signup is open and always creates a `visitor`. Both seeded accounts use the password
`deku-demo-pw-2026`: `curator@example.com` and `visitor@example.com`.

## Core features

### The project catalogue

1. A project's `status` is exactly `draft` or `published`. Creating one always produces `draft`;
   publishing is a separate, explicit act.
2. The public catalogue holds published projects only. A draft is absent from it, and a direct
   request for a draft by slug from an anonymous or `visitor` session is refused, not partially
   served.
3. The canvas header shows the live count of published projects, computed on read. Against the
   shipped seed it reads `6 projects`; publishing a seventh makes it read `7 projects`.
4. Public order is `display_order` ascending, then `published_at` newest first. Filtering by
   discipline or tag never exposes a draft.

### Publishing a project

1. The wizard has three steps, each at its own address: `/studio/projects/new/details`,
   `/studio/projects/new/media` and `/studio/projects/new/review`. Stepping back never discards
   what was entered.
2. Step two uploads exactly one image into `minio` under
   `projects/{project_id}/{sha256_of_bytes}.{ext}`, for example `projects/7/9f2a1c4e.png`. The
   bytes live in the bucket and nowhere else: not on the app's filesystem, not in a column.
3. A `slug` is unique. A create carrying a slug already taken is rejected as invalid and leaves
   no row and no object.
4. Publishing sets `status` to `published` and stamps `published_at` once. Publishing again
   changes nothing and is not an error.

### The public pages every visitor can reach

1. A privacy page at `/privacy` is reachable from the footer of every route and states what the
   studio stores about an enquiry and an application: the name, the email address, the company,
   the note and the uploaded file.
2. A terms page at `/terms` is reachable from the footer of every route, and the signup form
   links to it beside its submit control.
3. An unknown address renders the studio's own not-found route, with a `Return home` action, and
   answers as not found rather than as a page that exists.

### The visibility boundary

1. One authenticated route on the app's own origin serves image bytes: for a published project
   it answers anyone, for a draft only a signed-in `curator`.
2. An anonymous request for a draft's image is denied, a signed-in `visitor` request for the same
   image is denied, and a `curator` request returns the bytes.
3. A denial returns no part of the object: no thumbnail, no redirect to the store, no presigned
   link, and the object is untouched.

## Enquiry and careers

1. The public roles list holds open roles only. A closed role is absent from it and refused on
   direct request from a non-curator session.
2. The wildcard application accepts one file into `minio` under
   `applications/{application_id}/{sha256_of_bytes}.{ext}` and returns `WLD-` plus the id zero
   padded to five digits, for example `WLD-00001`.
3. Enquiry step one records `intent`, one of `collaboration`, `hiring` or `anything-else`;
   `anything-else` shows the direct contact details and stores no form.
4. Step two takes `readiness`, an integer `0`, `1` or `2` from a three-stop slider, then full
   name, email and company, all required, then an optional note. A submission missing a required
   field is rejected as invalid, keeps every value entered, and names the field at fault.
5. A stored enquiry returns `ENQ-` plus the id zero padded to five digits, for example
   `ENQ-00001`, and the curator's inbox shows that same reference.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the throwable wall of work | public |
| `/projects/:slug` | one project | public |
| `/about` | narrative, offices | public |
| `/careers` | roles and the wildcard | public |
| `/contact`, `/contact/enquiry`, `/contact/complete` | the three enquiry steps | public |
| `/privacy`, `/terms` | the legal texts | public |
| `/login`, `/signup` | sign in, registration | public |
| `/studio` | console, with drafts | curator |
| the three wizard step routes | details, media, review | curator |
| `/studio/enquiries` | enquiry inbox | curator |

**Entry and redirects.** An unauthenticated `/studio` request goes to `/login`, and sign in lands
on the route asked for. A signed-in `visitor` there is refused with a message, not looped back.
After login a `curator` lands on `/studio`, a `visitor` on `/`. Logout discards the token. An
expiry mid-action refuses the action and returns to `/login`. A draft or unknown slug at
`/projects/:slug` shows the not-found route.

**Journeys.**

1. Open `/`: the header reads `All projects` and `6 projects`. Drag and the field tracks the
   pointer one to one; release and it coasts to a stop, with cards arriving without end. Point at
   `Beacon World Cup 2026` for client `Beacon`, year `2026`, pills `Experience`, `3d`, `motion`.
   Toggle the list view. Open the project, go back: the wall is where it was left.
2. Sign in as `curator@example.com` with `deku-demo-pw-2026`. `/studio` lists eight projects,
   six published and two draft. Run the wizard for `Discovery Quests`, client `Loomis`, upload an
   image, confirm. Signed out, `/` still reads `6 projects`; publish it for `7 projects`.
3. Signed out, `/projects/brand-standards` is not found and its image route denied. As
   `visitor@example.com` the image is still denied; as `curator@example.com` it is served.
4. Open `/contact`, choose `Collaboration`, pick the middle slider stop, fill name, email and
   company, submit. `/contact/complete` shows `Nice one!` and `ENQ-00001`, which the curator
   sees at `/studio/enquiries`.
5. Open `/careers`: four open roles, `Motion Designer (AKL)` absent. Expand
   `Frontend Engineer (LDN)`. Submit the wildcard with a file for `WLD-00001`.

**States.** Every list has an empty state naming what is missing, every route a loading state,
the canvas included. A rejected submission keeps what was typed and names the field at fault. No
error leaves a blank page.

## UI/UX notes

A welcoming studio front of house that happens to be dark. The work is seen first and the
interface gets out of its way. The voice is warm and plainly spoken, and the one place that
warmth becomes visible is the enquiry flow, which should feel like being met at a door rather
than filling in a form.

Type is two voices. A display face carries body copy through to the wall-sized headline; a
monospace is reserved for small technical labels, which gives the site its instrument-panel
character. Set body copy in a rounded humanist sans so the reading voice stays human against that
hard mono. Figures align wherever numbers stack.

Ground is the deepest value in the system and the site commits to dark fully. One warm accent
carries highlight and focus and appears nowhere decorative, so that when it appears it reads as
an event. A separate colour means failure and appears nowhere else. Space over dividers: let
sections read as separate without a rule between them. The exact shades are yours, so long as
they hold those two exclusivity rules.

Motion is springy where it counts: the wall under a throw, and the cards as they land, overshoot
a touch and settle rather than gliding to a halt, and that spring is the site's signature. It is
not the whole vocabulary. The workhorse everywhere else is a firm ease with a hair of
anticipation, reveals take a longer soft settle, and the loader bar is sharp at the start and
slow at the end. The set is small and deliberate rather than one curve invented per component.
Elements enter by rising a short way and fading, and headlines assemble a word at a time. Under a
reduced-motion preference travel collapses to a cross fade in place: the fade stays, and nothing
that carries information is lost.

Accessibility is contract, not taste: contrast meets WCAG AA, touch targets are comfortably
sized, keyboard navigation reaches every card on the wall with a visible focus ring, and every
icon-only control carries a label. Meaning is never by colour alone, and the custom pointer never
stands in for a real focus ring.

The layout is top-nav with a floating route pill; the wall fills the viewport and the reading
routes sit in a centred column with generous gutters. The wall stays draggable at every width and
the reading column never runs edge to edge. It must not read as a page dominated by one hue
family with no second signal, and the console must not read as a marketing page: it is the one
surface where the working interface belongs.

## Technical requirements

The frontend is **React with Vite**. The backend is **NestJS**. The rendering model is a
single-page application over a JSON API: the browser receives an application shell on first
paint and every route's content arrives as JSON from the same origin. The server renders no
page HTML.

Both halves install from the public npm registry at image build time and run on the Node 20
runtime the environment image already carries.

Storage is **PostgreSQL**, reached at `DATABASE_URL`. Object storage is **MinIO**, S3
compatible, reached at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and
`STORAGE_SECRET_KEY`. Both are already running in this environment. Read every host and
credential from the environment; never hardcode one.

Auth is app-implemented email and password, stored hashed, with bearer tokens. Login returns
`access_token`, which the client sends as `Authorization: Bearer <access_token>` on every request except login, signup
and health. A token expires after 24 hours and an expired token is refused. Signup is open and
always produces a `visitor`; the `curator` role is seeded. There is no password reset and no
external identity provider.

`GET /api/health` returns `200` with a JSON body once the app is ready. Request logging is
structured to stdout, one line per request carrying method, path, status and duration, and
never a password, a token or object bytes.

Every image and every uploaded file lives in `minio` and nowhere else. Protected bytes are
served through an authenticated streaming route on the app's own origin rather than by handing
out presigned URLs, so one route owns the visibility decision for every object. Apply that one
mechanism consistently.

Nothing the browser downloads carries a credential: no database password, no object-store access
key or secret, and no bearer token belonging to a seeded account appears in any served script,
stylesheet, document or JSON payload.

Every response carries the standard security headers, including a strict transport policy and a
nosniff content-type policy.

A sitemap at `/sitemap.xml` lists every public route, and a robots file at `/robots.txt` points
at that sitemap.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing
services available in this environment are `postgres` and `minio`, and reaching for anything
else is a contract violation.

## Data model

Seven tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
not a secret. Hash it as normal; the exact literal must work at login, and it must be written
into `/app/USER_README.md` alongside each account so a grader can sign in.

### `users`

`id` integer primary key, `email` text unique, `password_hash` text, `role` text restricted to
`curator` or `visitor`, `created_at` timestamptz.

### `projects`

`id` integer primary key, `slug` text unique, `title` text, `client` text, `year` text,
`discipline` text restricted to `Experience`, `Communication` or `Product`, `tags` text array,
`summary` text, `status` text restricted to `draft` or `published`, `thumbnail_key` text
nullable, `display_order` integer, `created_at` timestamptz, `published_at` timestamptz
nullable.

`status` is `draft` on create. `published_at` is stamped the first time the project becomes
`published` and is never rewritten afterwards. `thumbnail_key` holds the object key, never the
bytes.

Observable invariant: a project's `slug` is unique across the whole table, and that holds under
concurrent creates rather than only in application-level checks. Two simultaneous creates of
the same slug must not both succeed: exactly one wins and the other is rejected, leaving no
orphaned row and no orphaned object.

### `roles_open`

`id` integer primary key, `slug` text unique, `discipline` text restricted to `technology`,
`partnership` or `creative`, `title` text, `office` text restricted to `London` or `Auckland`,
`detail` text, `apply_url` text, `open` boolean.

### `enquiries`

`id` integer primary key, `reference` text unique, `intent` text restricted to `collaboration`,
`hiring` or `anything-else`, `readiness` integer restricted to `0`, `1` or `2`, `name` text,
`email` text, `company` text, `message` text, `created_at` timestamptz.

`reference` is derived from the id at insert and then stored so it can be quoted back: `ENQ-`
followed by the id zero padded to five digits.

### `applications`

`id` integer primary key, `reference` text unique, `name` text, `email` text, `portfolio_url`
text, `message` text, `file_key` text, `created_at` timestamptz. `reference` is `WLD-` followed
by the id zero padded to five digits.

### `consent_events`

`id` integer primary key, `choice` text restricted to `accept` or `decline`, `created_at`
timestamptz.

### `site_config`

`id` integer primary key, `payload` jsonb. Exactly one row, holding offices, social links,
legal links and team counts.

**Derived rather than stored:** the published-project count shown on the canvas, the
per-discipline counts on the about route, and the two office clock times, which are computed
from each office timezone in the browser.

### Seed data

Accounts: `curator@example.com` with role `curator`, and `visitor@example.com` with role
`visitor`. Both use `deku-demo-pw-2026`.

Eight projects, six published and two draft:

| slug | title | client | year | discipline | tags | status |
|---|---|---|---|---|---|---|
| `beacon-world-cup-2026` | Beacon World Cup 2026 | Beacon | 2026 | Experience | `3d`, `motion` | published |
| `free-signals-center` | Free Signals Center | Vireo Music | 2026 | Product | `website`, `tool` | published |
| `powering-progress` | Powering Progress | Northwind | 2025 | Communication | `film`, `campaign` | published |
| `transforming-ventures` | Transforming Ventures | Meridian | 2025 | Communication | `brand`, `content` | published |
| `campus-visitor-guide` | Campus Visitor Guide | Larkspur | 2025 | Product | `website`, `cms` | published |
| `midnight-woods-tour` | Midnight Woods Tour | Umbra | 2024 | Experience | `3d`, `game` | published |
| `brand-standards` | Brand Standards | Sundial | 2026 | Communication | `brand` | draft |
| `handset-for-travel` | Handset for Travel | Cascade | 2026 | Product | `physical`, `illustration` | draft |

Every seeded project, including both drafts, carries a real thumbnail object in `minio` at its
key scheme, generated procedurally at seed time. A draft's image therefore exists and is
refused, rather than merely being absent.

Five open-role rows, four open and one closed:

| slug | discipline | title | office | open |
|---|---|---|---|---|
| `frontend-engineer-ldn` | technology | Frontend Engineer (LDN) | London | true |
| `senior-partnerships-manager-ldn` | partnership | Senior Partnerships Manager (LDN) | London | true |
| `design-lead-ldn` | creative | Design Lead (LDN) | London | true |
| `designer-ldn` | creative | Designer (LDN) | London | true |
| `motion-designer-akl` | creative | Motion Designer (AKL) | Auckland | false |

One `site_config` row: offices `London` (`Europe/London`, handle `@SPCTRLDN`, email
`hello@spectre.agency`) and `Auckland` (`Pacific/Auckland`, handle `@SPQAKL`, email
`kia@spectre.nz`); the messaging number `+440000000000`; team counts `Experience` 18,
`Communication` 12, `Product` 9; legal links `Privacy Policy`, `Modern Slavery Statement` and
`AI Policy`; the certification line `ISO 27001`, certificate number `12439`.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Constraints

One studio, one tenant, two offices. No client portal and no per-client login. No comments, no
likes, no messaging between visitors. No blog, no newsletter, no search. No rich-text authoring
beyond the project summary and the role detail. No payment of any kind, and no billing surface.
No email is sent by this app; enquiries and applications are read in the console. No native
application and no app-store packaging. No analytics vendor and no third-party tag: the consent
choice is recorded in this app's own table. No external network calls at run time. No binary
asset ships with the build: every image, icon, sound and three-dimensional form is generated in
code. The app must stay responsive with a catalogue of 500 projects on the wall and 5,000
stored enquiries.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world
  uses. Read both from the environment; never hardcode either.
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
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable
  from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{ email, password }` | `{ access_token, role }`, role always `visitor` |
| `POST /api/auth/login` | `{ email, password }` | `{ access_token, role }` |
| `GET /api/health` | none | `{ status }` |
| `GET /api/projects` | optional `discipline`, `tag` | top-level JSON array of published projects; each `{ id, slug, title, client, year, discipline, tags, summary, thumbnailUrl, status, displayOrder, publishedAt }` |
| `GET /api/projects/count` | none | `{ count }`, published only |
| `GET /api/projects/:slug` | none | one project object |
| `POST /api/projects` | `{ title, client, year, discipline, tags, summary, slug }` | the created project, `status` `draft` |
| `POST /api/projects/:slug/thumbnail` | multipart, field `file` | `{ slug, thumbnailKey }` |
| `POST /api/projects/:slug/publish` | none | the project, `status` `published` |
| `GET /api/projects/:slug/thumbnail` | none | the image bytes |
| `GET /api/studio/projects` | none | top-level JSON array of every project, draft and published |
| `GET /api/roles` | none | top-level JSON array of open roles, each `{ id, slug, discipline, title, office, detail, applyUrl, open }` |
| `GET /api/studio/roles` | none | top-level JSON array of every role |
| `POST /api/enquiries` | `{ intent, readiness, name, email, company, message }` | `{ id, reference }` |
| `GET /api/enquiries` | none | top-level JSON array of stored enquiries |
| `POST /api/applications` | multipart `{ name, email, portfolioUrl, message, file }` | `{ id, reference }` |
| `GET /api/config` | none | `{ offices, social, legal, counts }` |
| `POST /api/consent` | `{ choice }` | `{ ok }` |

Field names are exact. Bearer auth is required on everything except `POST /api/auth/login`,
`POST /api/auth/signup` and `GET /api/health`; `GET /api/projects`, `GET /api/projects/count`,
`GET /api/projects/:slug`, `GET /api/roles`, `GET /api/config`, `POST /api/enquiries`,
`POST /api/applications` and `POST /api/consent` also accept an anonymous caller. A successful
call returns the named shape; an invalid or unauthorized call is rejected as a client error,
never a `5xx` and never a silent success.

### No mocks

An in-memory `objects` map holding uploaded bytes, image bytes written to the app container's
filesystem, a database column carrying base64 image data, a hardcoded `{"uploaded": true}`
response the app returns to itself, or a project list served from a JSON file checked into the
repository are all contract violations however good the interface looks. `minio` is the fact
and `postgres` is the fact: the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Front-end specification

This section carries the measured visual, motion and interaction detail the product is built
to. Values here are contract.

Two registers run through it. A statement of what the product must do is **normative** and is a
requirement. A statement of what was observed in the studio's earlier work is **informational**,
offered as evidence of intent rather than as an instruction, and the build is free to satisfy
the requirement by any means that holds the stated values. Where a paragraph carries no marker,
read it as normative.

Four audiences read the finished site and the design answers to all of them: prospective
clients asking whether this studio can make something world class for them, talent asking what
it is like to work here and whether there are roles open, press and peers asking what has
shipped and who made it, and returning contacts looking for the right person to reach.

### Scaling and breakpoints

A token set on a fixed root with hard breakpoints rather than fluid interpolation. The
reference edges, in descending frequency of use: `(min-width: 1024px)` is the primary desktop
branch, `(min-width: 1440px)` large desktop, `(min-width: 1920px)` extra-large desktop,
`(max-width: 1024px)` the mobile and tablet branch, `(min-width: 599px)` above large phone, the
bands `(min-width: 1024px) and (max-width: 1440px)` and
`(min-width: 1440px) and (max-width: 1920px)`, and `screen and (max-height: 400px)` as a
short-viewport guard for the canvas. Three widths anchor the matrix: desktop at `1440px`,
tablet between `599px` and `1024px`, mobile below `599px`.

### Colour tokens

Near-monochrome. Two custom properties are defined on the root and everything else is built from
black, white and their alphas. The brief names each colour by family, tone and shade; the exact
value is the builder's to choose, so long as it lands in the band named and holds the
exclusivity rules below.

| Token | Colour | Role |
|---|---|---|
| `--color-primary` | a near-white neutral | primary text and marks, defined on `:root` |
| `--color-secondary` | a deep neutral | secondary ground and panels, defined on `:root` |
| `--ink` | a near-black neutral | the dominant page ground |
| `--ground-2` | a deep neutral, one step above the ink | raised panels, cards, the cookie banner |
| `--ground-3` | a deep neutral, one step above that | nested surfaces |
| `--line` | a deep neutral, light enough to read as a line | hairlines and separators at full strength |
| `--muted` | a light neutral | muted labels and inactive text |
| `--soft` | a near-white neutral, one step below the primary | off-white on light inversions |

Accent palette, state only. Each of these appears in its named role and nowhere else.

| Token | Colour | Role |
|---|---|---|
| `--accent-warm` | a mid, vivid orange | the single warm accent, highlights and focus |
| `--confirm` | a mid, soft teal | positive hover on the cookie controls |
| `--confirm-2` | a mid, soft green | the messaging-action confirm hover |
| `--signal-green` | a light, vivid green | reserved for signal moments |
| `--signal-teal` | a mid, vivid teal | the companion to the signal green |
| `--wash-teal` | a light, soft teal | the pale wash on a tinted surface |
| `--fail` | a mid, soft red | the colour that means something has gone wrong, and appears nowhere else |
| `--focus-alt` | a mid, vivid violet | the high-visibility focus outline on inverted surfaces |
| `--sand` | a light, soft orange | the warm neutral on the wildcard upload affordance |

Alpha system, expressed as `hsla` stops against white and black: hairline fills over dark at one tenth, raised-panel
fills at fifteen hundredths, control borders at one fifth, active borders at three tenths,
secondary text at two fifths, placeholder text at one half, the mono-detail label a shade above
that, strong secondary text at three fifths, and the faintest divider at one twentieth. Scrims
over media sit at two fifths black and the mask stop on the header blur at three fifths. The
resting fill of the contact tiles and buttons is a mid neutral at roughly half opacity. Two theme
functions are preserved: a blend of the primary and a relative colour derived from it, both
deriving tints without adding tokens.

### Type scale

Two licensed families, named exactly, each with a normative fallback stack to use until the
licence is in place. The display and body face is `Helvetica Now Display`, falling back to
`"Helvetica Now Display", "Helvetica Neue", Helvetica, Arial, system-ui, sans-serif`. The mono
detail face is `ballinger-mono`, falling back to `"ballinger-mono", "IBM Plex Mono",
"Roboto Mono", ui-monospace, "SFMono-Regular", Menlo, monospace`. Both fallbacks are close enough
in metrics that the art-directed line lengths hold. Naming a family is not an asset dependency.

The ramp: a display and body grotesque at weights `400`, `500`, `700`, `800` and `900`, and
a mono detail face at `300` and `500`. The ramp, by frequency: `16px/500` base UI, `10.88px/400`
line-height `11.968px` mono micro label, `29.7px/700` line-height `29.7px` section and card
titles, `16px/400` line-height `15.2px` body, `48px/700` line-height `48px` route headings,
`57.42px/800` line-height `51.678px` the wall-sized about headline, `50px/800` line-height
`46.5px` large display, `33.12px/500` line-height `30.816px` sub-display, `17.92px/500`
line-height `25.088px` lead paragraph, `12px/500` small UI labels, `14px/400` line-height
`13.3px` captions, `20px/400` line-height `24px` intro paragraph, `18px/700` emphasised list
titles, `11px/400` line-height `12.1px` smallest mono label, and `6.4px/400` line-height
`6.4px` the canvas-distance micro label.

### Radius, elevation and layering

Radii: `14px` the mono-detail pill, `48px` primary buttons and CTA links, `40px` the bottom
pill navigation and the view toggle, `32px` the cookie banner, `5px` the contact intent tiles,
`3px` form fields and numbered boxes, `1600px` the slider thumb, `50%` avatars, dots and icon
buttons.

Elevation is layering, not shadow. The `z-index` ladder is fixed: `-1` the three-dimensional
canvas composited behind content, `1` in-flow content, `2` raised content within a section,
`100` the bottom pill navigation, `1000` the fixed header, `9999` the cookie banner, `10000`
the contact overlay, `10001` the custom cursor.

### Spacing and layout grid

A centred column with generous side gutters at desktop. The about and careers routes use a
two-column split: a left rail of mono labels, a right column of body. The canvas route ignores
the column and fills the viewport. Spacing is expressed in `rem` off the fixed root; the
recurring rhythm is a `2rem` resting offset with `4rem` and `6rem` entrance travel.

### Iconography

Every icon is inline vector geometry, transcribed rather than shipped as a file, inheriting the
current text colour unless a fill is stated.

- **Sound dot-grid:** `viewBox="0 0 23 8"`, twenty-four circles of `r="1"` on a three-row by
  eight-column lattice, columns at `cx` of `1, 4, 7, 10, 13, 16, 19, 22` and rows at `cy` of
  `1, 4, 7`. These pulse when sound is enabled.
- **Dual-clock dots:** the day dot is one `circle` at `cx="4" cy="4" r="4"`; the night moon is
  `viewBox="0 0 8 8"` with one crescent `path`. The day office shows the dot, the night office
  the moon, chosen from the office local hour.
- **Social icons:** professional network at `viewBox="0 0 16 16"`, one `path`,
  `fill="currentColor"`, a rounded square with an inset mark; short-form social at
  `viewBox="0 0 31 32"`, one `path`, crossing strokes; image social at `viewBox="0 0 12 13"`,
  two `path`s, a rounded-square outline plus an inner ring and lens dot.
- **Interface icons:** a diagonal arrow at `viewBox="0 0 22 22"`, one `path` filled with the primary near-white,
  on `Let's talk` and `Return home`; a close mark at `viewBox="0 0 56 56"`, a
  `circle cx="28" cy="28" r="28"` filled with the primary near-white, plus a cross `path` at `stroke-width="1.5"`;
  an arrow-in-circle in the same `56` frame on the intent tiles; a small `circle cx="5" cy="5"
  r="5"` as the tile bullet; a copy mark at `viewBox="0 0 25 25"`, two `path`s; a messaging mark
  at `viewBox="0 0 24 25"`, one `path` filled with the primary near-white; an upload cloud at
  `viewBox="0 0 27 18"` on the wildcard file field.
- **Slider tick track:** the range control draws its track as unit rectangles rather than a
  line: `viewBox="0 0 648 16"`, seventy `rect`s of `width="1" height="1"` at `y="7.5"`, stepped
  by `6.0467px`. Narrower variants exist at `viewBox="0 0 214 16"` with 38 ticks and
  `viewBox="0 0 359 16"` with 62 ticks. Render the tick count from the track width so the ticks
  stay evenly spaced.

### Global chrome

The chrome is fixed on every real route: a header pinned to the top, a pill navigation pinned
to the bottom, a footer at the end of scrolling content, and two floating overlays, the cookie
banner and the contact panel.

**Header,** `z-index: 1000`, five slots across one row: the wordmark top-left, drawn as the
mascot silhouette with a registered mark and linking home; the sound toggle centre-left, the
dot-grid icon plus the label `Sound [OFF]` in mono detail; the tagline centre, `Spectre is a
technology-led creative agency crafting experiences for global brands.` set in mono detail at
`10.88px`; the dual clock centre-right, two rows each carrying an office label, a live time and
a day or night dot; and the `Let's talk` pill button top-right at radius `48px`, opening the
contact panel. Behind it sits a gradient blur bar: `backdrop-filter: blur(26px)` masked by
`linear-gradient(rgb(0, 0, 0), rgba(0, 0, 0, 0.6) 75%, rgba(0, 0, 0, 0))`, strongest at the top
and fading to nothing, so content stays legible under the header without a hard edge.

**Header entrance and hide.** Top-anchored elements enter on `ease-down` (`top: -6rem` to
`top: 0`), bottom-anchored ones on `ease-up` (`bottom: -4rem` to `bottom: 2rem`), and centred
ones on `ease-down-medium` (`translate(-50%, -100%)` to `translate(-50%, -50%)`). The CTA
carries a `matrix(1, 0, 0, 1, 0, -13.9766)` resting lift.

**Bottom pill navigation,** pinned bottom-centre at `z-index: 100`, radius `40px`, a
`blur(10px)` backdrop. Three items, `Work`, `About` and `Careers`, the active route a filled
white pill and the inactive items muted. The highlight slides between items on a `transform`
transition, and the wrapper carries a horizontal offset transform so the pill re-centres as the
active label width changes.

**The dual clock.** Two offices, each a label, a live `HH:MM` time and a marker: the day dot in
daytime, the moon at night, chosen from the office local hour. `London, UK` and `Auckland, NZ`.
Times update once per minute from the client clock offset to each zone, never from a request.
The active office dot blinks.

**Footer.** Both offices as full postal blocks, the studio registered marks `Spectre` and
`SPQ`, the certification line `ISO 27001` with certificate number `12439`, the social row, and
three legal links, `Privacy Policy`, `Modern Slavery Statement` and `AI Policy`. Footer links
carry an animated underline built from two pseudo-elements that swap on hover.

**Cookie banner,** bottom-anchored, `z-index: 9999`, radius `32px`, `blur(10px)` backdrop,
entering on `translateY(150%)` to `translateX(0)`. Copy: `WE USE COOKIES TO ANALYSE OUR
TRAFFIC. FOR MORE INFO, READ OUR PRIVACY POLICY`, with `Accept` and `Decline`. The buttons
carry a three-layer hover shifting colour and border from `rgb(0, 0, 0)` to the confirm green
`rgb(80, 186, 163)`. The choice is persisted and gates analytics.

### Motion language

**The principle.** Motion is the product. Two behaviours dominate: elements travel a short
distance as they enter, a rise from below and occasionally a scale-in, and interactive surfaces
move under the pointer with weight through drag inertia, cursor lag and hover lifts. Ordinary
scrolling is eased rather than native.

Named entrances, each described by what it does rather than by a curve: top-anchored chrome
drops in from above its resting place; bottom-anchored chrome rises from below it; centred chrome
slides down into the middle; the cookie banner travels up from fully below the fold; the client
logo grid pops in from nothing, overshoots slightly larger than its resting size and settles
back; an image reveal grows from half size to full and fades back out; a loading mark spins
continuously about its centre; and the active clock dot fades between two thirds and full
opacity and back.

Easing, by character rather than by curve. The default is a firm ease with a hair of anticipation
at the start and a glide to a soft stop. Reveals settle on a longer, softer curve. The canvas and
the card translate overshoot their target and spring back, which is the site's signature. The
loader bar is sharp at the start and slow at the end. The studio's own declared ease is a smooth
acceleration into a long settle, and the remainder of the set covers a soft launch, a symmetric
ease, a slow-out settle, and a bounce that overshoots past its target.

Declared transitions, by what they govern: background colour on buttons and controls, transform
on hover lifts and pill slides, colour on links, the spring-plus-fade on the card and canvas
entrance, the loader bar, the accordion opening and closing on its row height, background and
border together on the intent tiles, a longer progress move, and a two-stage hover whose colour
change is delayed behind its first stage. Every duration is the builder's to choose; what is
fixed is that they share one vocabulary and that the card entrance is the springy one.

Runtime behaviour: the clock dot blinks about once a second, without end; the contact panel and
its intent grid fade in once and stay; the loader bar fills once, holding at empty before it
starts; the loader headline and mark play a single exit move; and the loader wrapper itself runs
a short ease-out.

**Reduced motion.** Under a reduced-motion preference drag inertia collapses to an immediate
settle, the mascot holds a static pose, the canvas entrance and card reveals cross-fade in place
without travel, the clock dot stops blinking, and the loader shows the fill without the skew,
stretch and split. Nothing that conveys information is removed, only its travel.

### Scroll and reveal system

**Smooth scroll.** Scrolling on the about, careers and project-detail routes is eased rather
than native: wheel and touch input drive a virtual scroll position the page interpolates toward
each frame, so reveal animations can be tied to that position. The home canvas does not scroll;
it drags.

**Reveal on entry.** The dominant reveal is a rise-and-fade: elements begin offset below their
resting place at zero opacity, then travel up and fade in as they enter. Containers and list
items lift from a `20px` offset, assets and cards from a `10px` one. The entrance uses the
spring-plus-fade character above.

**Scroll-scrubbed elements.** On about and careers a set of elements change transform and
opacity continuously across scroll frames rather than at a single trigger: on about the
split-word spans, the carousel track and the section containers; on careers the left and right
rich-text columns, the asset blocks, the separators, the card container and the open-roles
section. Separators scrub their horizontal scale from `matrix(0, 0, 0, 1, 0, 0)` outward, so
each rule draws itself across as it enters.

**Split text.** Display headlines reveal per word or per letter on a short stagger tied to
scroll entry, each unit rising into place, never the whole line at once. The about headline
splits to individual letters.

### The three-dimensional layer

A full-viewport real-time three-dimensional layer composited behind the content at
`z-index: -1`, rendering one hero object, a ghost mascot, in three recurring roles: the loader
mark, the floating hero of the not-found route, and a per-section character on careers.

**Renderer contract.** One persistent rendering context for the whole session,
transparent-backed so the page ground shows through, sized to the viewport and capped at a
device pixel ratio of `2`. A post-processing chain is present: a render pass plus at least one
full-screen effect pass, supporting a bloom or fresnel-glow pass and a subtle grain pass so the
mascot reads as self-lit and filmic. The loop pauses when no animated element is on screen and
when the tab is hidden, and resumes on interaction.

**The mascot material.** A self-lit translucent form with visible internal structure: a soft
fresnel rim toward the primary near-white, a dark interior toward the page ground, and a fine internal noise
giving a wispy filament texture inside a smooth outer silhouette. It must read as a lit,
semi-transparent object floating in a void rather than a flat cut-out, and must carry a slow
idle motion, a gentle bob and rotation, even at rest. On careers the same mascot appears twice
per value section, once bright and once dark.

**Pointer and scroll binding.** The mascot tracks the pointer with a lagged follow so it
appears to look toward the cursor, and on careers it is bound to scroll so each section's
character settles as that section enters.

**Fallback.** Where the three-dimensional context is unavailable the mascot degrades to a
static generated silhouette in the same position and the page remains fully usable. No content
depends on the layer.

### The loader sequence

The site opens on a loader that holds the first paint while assets stream, then performs a short
choreography on the way out: the mascot, a headline and a progress bar on the black ground. The wrapper
animates over `500ms` ease-out, filling both. Within it the progress bar scales from empty to
full on the sharp-in slow-out character, backwards-filled so it holds at empty before it starts. The headline plays one of a set of `1000ms` linear exits: `move-out-left`
(`translateX(0)` to `translateX(-10vw)`), `move-out-right` (to `translateX(10vw)`), `move-up`
(`translateY(0)` to `translateY(-30vh)`) or `move-down` (to `translateY(30vh)`). The mark plays
a `1000ms` linear deformation as it leaves: `skew-left` (`skew(0deg)` to `skew(-20deg)` and
back), `skew-right`, or `stretch` (`scaleY(1)` to `scaleY(1.3)` and back), each carrying
`will-change: transform`. The exit variant is chosen per load, so the loader does not leave the
same way twice.

That choreography is the loader's whole purpose after the bar fills.

**Handoff.** The loader must not block interaction past its exit: once the bar completes and the
exit move plays, the loader tears down, the chrome performs its entrance, and the wall becomes
throwable. If assets are still streaming the loader holds at a near-full bar rather than
snapping, and the mascot idles.

### Audio system

An ambient sound layer plus short interface cues, both off until the visitor opts in. The header
carries a `Sound [OFF]` toggle and the home canvas shows a one-time prompt, `CLICK TO ENABLE
SOUND`.

Sound is strictly opt-in and there is no autoplay of any kind: no audio plays before a user
gesture. The first click or tap that enables sound both starts the
ambient bed and unlocks the cue bus. The choice persists across routes and reloads, and the
label reflects state. While sound is on, the control's dot grid and its surrounding circle,
resting at `opacity: 0.2`, pulse, so the header carries a living indicator of audio state; when
off the dots hold at rest.

Cues fire on canvas grab and release, on view toggle, on tile hover and on contact-panel open
and close. Each is a short enveloped tone generated in code, never a file, mixed low under the
ambient bed and ducked while a cue plays.

### The project canvas

The home route is not a scrolling page. It is an infinite, draggable canvas holding every
published project as a thumbnail, that the visitor grabs and throws to explore. The header reads
`All projects` and the live count.

**Grab, drag and throw.** Pointer-down anywhere on the field grabs it; pointer-move drags the
whole field of thumbnails under the pointer one to one; pointer-up releases it with inertia, so
the field keeps travelling and eases to a stop. The field wraps: dragging far in any direction
brings further projects into view without an end, so the wall feels boundless, while the count
stays finite. Momentum decays on a weighted curve, so a hard flick travels far and a gentle
nudge barely moves. Under reduced motion, inertia collapses to an immediate settle.

**Depth and entrance.** At rest the thumbnails sit on a subtle perspective: distant items
smaller and dimmer, near items larger, and the field carries a faint three-dimensional curve
before settling flat. Cards enter with the spring-plus-fade above.

**The thumbnail.** Each carries, on hover or focus, the project title at `29.7px/700`, the
client name, a set of discipline and tag pills at radius `14px`, and the year. Pills carry a
discipline, one of `Experience`, `Communication` or `Product`, and free tags from `ai`, `3d`,
`motion`, `website`, `game`, `film`, `campaign`, `social`, `illustration`, `event`, `brand`,
`content`, `cms`, `tool`, `physical`, `experiential` and `ooh`. The resting thumbnail is quiet
and the metadata resolves in on approach.

**Hover and the image trail.** Moving the pointer on the canvas drags a trail of images behind
it at `mix-blend-mode: difference`, and the custom cursor inverts whatever it crosses. Hovering
a thumbnail lifts and sharpens it and brings its metadata forward.

**Grid and list views.** A control pinned bottom-left toggles two arrangements of the same set:
the throwable field, thumbnails in a loose lattice; and a tidy vertical list, one row each
carrying title, client, year and pills, scrolling conventionally, its item wrapper carrying the
`20px` reveal offset. The toggle is two icons, a grid of squares and a stack of rows, in a
rounded control; switching plays a cue and cross-animates the layout.

**Entering a project.** Activating a thumbnail by click, or by keyboard enter on the focused
item, transitions to the project-detail route with the thumbnail expanding into the detail hero
rather than a hard navigation. Back returns to the canvas at the same drag position.

### Cursor and pointer system

The custom cursor is a small mark that inverts its background, always on top at
`z-index: 10001`, and follows the pointer on a lag so it trails slightly behind rather than
locking to it. It takes contextual states: a resting dot, a grab state over the canvas, a drag
state while the field is held, a label state over an activatable thumbnail, and a hidden state
over text inputs. The hover catalogue covers thumbnail lift, footer link underline swap,
intent-tile background and border shift, cookie-button three-layer hover, and the transparent to
white fill on the previous-step button. The custom cursor never replaces the real focus ring,
and it is suppressed entirely for touch and for reduced motion.

### Route detail

The project collection source and the open-roles collection source are the two read collections
behind the site; the professional-network profile and the image-social profile are two of the
three social links in the footer row. All four are configuration rather than routes.

**Home,** titled for the studio and the work. Hidden landmark copy names the page for assistive
technology; an on-canvas wordmark sits behind the field; the count and index header reads
`All projects` with the live count.

**Project detail,** at `/projects/:slug`, reconstructed from the canvas metadata and the studio's
own copy: the thumbnail as hero, the title, the client, the year, the discipline and tag pills,
the summary, and ordered detail media bands.

**About.** A wall headline set at `57.42px/800`, split to individual letters and revealed on a
stagger; a scrolling carousel; the studio statement; the three focuses, each a
column with a body paragraph and a `View our ... work` link into the canvas filtered by that
discipline: `Experience`, whose focus is immersion, intrigue and impact, carrying purpose-led
activation and inspiring engagement; `Communication`, whose focus is meaning, connection and
performance; and `Product`, whose focus is utility, scale and function, long term, evolving and
business goal driven. Then the two studios as postal blocks with their handles, the team
breakdown by function with the counts from the configuration document, the named operations lead
`Mara`, `Chief Operations Officer`, and the client logo grid, which enters on the overshoot
pop.

**Careers.** A `Careers` mono label over the spirit hero and a `View open roles` button that
jumps to the list. Three value sections, each a mono `Spectres are` label, a one-word title and a
body paragraph whose theme is fixed: `Respected` is moulding roles to people and complementary
skill sets, `Trusted` is the team controlling its own destiny and delivering exceptional work,
and `Unrivalled` is staying ahead of the curve and thriving outside traditional agency models.
The mascot stands to the side, settling
per section as it enters, with columns, separators and card scrubbed on scroll. Then
`Roles we are on the lookout for:` over the open roles, each a discipline label and a title,
expanding on an accordion at `grid-template-rows 0.3s ease-in-out` to reveal its detail and an
apply action. Then the wildcard block and its `Open submissions` row, which opens the
application and accepts a file upload.

**Contact.** A full-screen panel at `z-index: 10000` that opens over any route, fading in over
`600ms` and closing on the `56` close mark. Opening it records history state rather than a hard
navigation. Step one is a heading, `Welcome! It is great to meet you.`, under a `Let's talk`
label, then three tiles each a bullet, a subtitle and a title: `Collaboration` /
`I'm interested in working together.`, `Hiring` / `I'd like to join the team.`, and
`Anything else` / `Just saying hi.` The first two carry the arrow-in-circle mark and route to
the form; the third reveals two direct contacts, `EMAIL hello@spectre.agency` and
`WHATSAPP +440000000000`, each copyable. Step two is the five-field stepped form, each field
numbered in mono `01` to `05`: `01` `How shall we kick things off?` on the three-stop slider,
`02` `Full name*`, `03` `Email address*`, `04` `Company*`, and `05`
`Drop us a note, we would love to chat!` The slider is a labelled range with three stops drawn
on the tick track, its labels `We would like to get to know each other.`,
`We have some ideas floating around.` and `We have something more specific in mind.`; the thumb
at radius `1600px` slides on `transform` and snaps to the nearest stop. Step three is the
completion: a `Complete` label, `Nice one!`, `Thank you for sharing.`, three numbered boxes
explaining what happens next, the enquiry reference, and a `Finish` button that closes the
panel. The form carries idle, submitting, success and failure states; validation is inline and
per field; failure keeps the entered values and offers a retry.

**Not found and legal.** The not-found route is the mascot floating large on the black ground
under the title `Page not found`, with a `Return home` action carrying the diagonal arrow. Seven
captured addresses, `/as`, `/gs`, `/g/d`, `/as/d`, `/projects`, `/g/collect` and `/mc/collect`,
resolve here and must not become public routes. The legal route at `/privacy` carries the
privacy policy, the modern slavery statement and the AI policy as three sections.

### Frontend module and component architecture

The application is one shell holding the persistent chrome, the persistent three-dimensional
layer and a routed content region, so the canvas context and the audio bus survive route
changes. The module tree groups by surface: chrome, canvas, routes, overlays and engines.
Cross-cutting engines are the render loop, the smooth-scroll driver, the audio bus, the pointer
and cursor tracker, and the reveal observer. The reveal primitive is one wrapper that takes an
offset and a stagger and drives every entrance in the product, so the motion vocabulary cannot
fragment per component.

### State, data flow and routing

State ownership is explicit: the catalogue is fetched once and held for the session; the canvas
holds its own drag position and view mode; the enquiry wizard holds its draft across its three
addresses; the audio and consent choices are persisted. Data flows one way, from the API into
the shell and down into the routes; no component writes to another's state. Routing and history
follow the rule that the enquiry panel and the wizard push real history entries, so back moves
one step rather than dismissing the whole flow, and returning to the canvas restores its drag
position.

### Responsive behaviour

Three widths. At desktop the full chrome, the two-column reading layout and the throwable wall.
Between `599px` and `1024px` the header compresses to the wordmark, the sound toggle and the
CTA, the reading layout becomes one column, and the wall keeps its drag. Below `599px` the
bottom pill navigation becomes the primary route switch, the dual clock collapses to the active
office, the list view is the default arrangement of the work, and the enquiry steps stack one
field at a time. Touch: drag and throw are the same gesture as pointer drag, hover metadata
resolves on tap-and-hold instead of hover, and the custom cursor is suppressed.

### Accessibility

Structure and landmarks: one `main` per route, a labelled navigation, a labelled
`contentinfo` footer, and hidden landmark copy naming the canvas for assistive technology.
Keyboard: every card on the wall is reachable and activatable, the view toggle and the sound
toggle are real buttons, the accordion rows are expandable from the keyboard, the contact panel
traps focus while open and returns it to the control that opened it on Escape, and the slider is
operable by arrow keys with its stop announced. The custom cursor is decorative and hidden from
assistive technology; the reduced-motion preference is honoured everywhere. Contrast and state:
text meets WCAG AA against its ground, state is never signalled by colour alone, and the focus
ring is visible on every surface including the inverted ones.

### Performance

Budgets: the wall holds a smooth frame rate on a three-year-old laptop with the canvas and the
mascot both running; the canvas cost is bounded by drawing only the thumbnails within and just
beyond the viewport and by reusing card nodes as the field wraps; the render loop pauses when
nothing is animating and when the tab is hidden. Asset streaming: the catalogue arrives once and
thumbnails load lazily in view order, the mascot's geometry is generated rather than fetched, and
nothing blocks first paint except the loader itself.

### Analytics, consent and privacy

The consent gate is client-side: no measurement of any kind runs before a choice is recorded, and
the choice is posted to this app's own consent endpoint so the decision has a record. What is
measured, once consent is given, is limited to route views, the enquiry funnel steps and the
wildcard submission, all recorded in this app. There is no third-party tag and no external
beacon; the measurement identifiers in the reference are stubs and are not carried.

### Content model and editorial workflow

Authoring happens in the studio console. A project is authored as structured fields plus an
ordered list of detail blocks; the block types are a text block, a full-bleed media band, a
two-up media pair and a pull quote. Media handling is uniform: one upload path, one key scheme,
one authenticated read path, and no bytes anywhere but the bucket.

### Build order

The build order is the author's to choose. What the product must satisfy at the end is
everything above.

### Copy deck

Global chrome carries the tagline `Spectre is a technology-led creative agency crafting
experiences for global brands.`, the navigation labels `Work`, `About` and `Careers`, the CTA
`Let's talk`, the sound label `Sound [OFF]`, the cookie copy `WE USE COOKIES TO ANALYSE OUR
TRAFFIC. FOR MORE INFO, READ OUR PRIVACY POLICY` with `Accept` and `Decline`, and the footer
certification `ISO 27001`.

Home carries `All projects` and the count. The project set is the eight seeded titles above.

About carries the wall headline and the statement, and names the three focuses `Experience`,
`Communication` and `Product`.

Careers carries the spirit statement: `Spectre spirit represents the energy our team is built
on. It is a mindset, a way of working and a set of values that inspire us to challenge the
boundaries of what is possible. From the studio up, we created Spectre to be the company we
always wanted to work at but could never find, bringing together the world's most unique and
talented forward thinkers.`, the button `View open roles`, the three values `Respected`,
`Trusted` and `Unrivalled`, the heading `Roles we are on the lookout for:`, and the wildcard
copy: `Or are we really looking for you? If the roles we are hiring are not a perfect fit but
you feel like you would be a great Spectre, we would still love to hear from you. Send us a
wildcard application below.` under the label `Open submissions`.

Contact carries `Welcome! It is great to meet you.`, the three tile titles, the five field
labels, the three slider labels, and the completion copy `Nice one!` and
`Thank you for sharing.` with the `Finish` button.

Not found carries `Page not found` and `Return home`.

### Zero-asset substitution

Nothing in the build depends on a binary file. The mascot model is generated in code as a
ghost-like form: a rounded capsule body with a wavy skirt, built as geometry at start-up rather
than loaded. Its material and particle detail are procedural, per the fresnel and noise
description above. Audio is synthesised: an ambient bed built from layered low oscillators with
a slow filter sweep, and five cues, a click, a swipe, a whoosh, a riser and a load cue, each a
short enveloped tone. The dot grid and tick marks are drawn as inline vector geometry. The reference shipped the font binaries `HelveticaNowDisplay-Regular.woff` and
`HelveticaNowDisplay-Medium.woff`; neither is carried. Fonts come from the platform stack or from
a webfont fetched at build time, never a `woff` binary shipped in the repository. Project, tile and not-found imagery is generated procedurally at seed time, one
deterministic image per project derived from its slug, so every seeded project has real bytes in
the bucket. Grain is generated as a noise pass rather than a tiled image.

### Evidence gaps

Two areas of the reference were not directly measurable and are reconstructed here: the
project-detail template, since every capture of an internal detail route resolved to the
not-found page and the capture is therefore not-found-dominated, and
the three-dimensional scene graph, since the mascot's animation is baked in a model file. Both
are specified above from the canvas metadata, the studio's own copy and the measured not-found
frame, and both should be expected to need adjustment. Enum substitutions, colour provenance,
hover evidence, routes and views are all as measured and carried above.

### Acceptance

Structure and content: every route above exists and carries its copy; the catalogue count is
live; drafts and closed roles are absent from public reads. Design and motion: the palette, type
ramp, radii and `z-index` ladder are as tabulated; the reveal, the spring and the reduced-motion
behaviour are as described. The set pieces: the loader hands off cleanly, the wall drags and
throws and wraps, the mascot renders translucent and self-lit and degrades safely, the custom
cursor inverts and trails, and the sound layer stays silent until it is invited. Quality: the
app holds a smooth frame rate with the canvas and the mascot running, and nothing in the build
depends on a binary file.

## Definition of done

A visitor can open the app, drag the wall of published work, open a project, and send an enquiry
that comes back with a quotable reference. A project the studio has not published is absent from
the wall and its image bytes are refused to anyone who is not the signed-in curator, on direct
request. A curator can create a project through the wizard, put its thumbnail in the bucket, and
publish it, and the count on the wall changes to match. The app is deployed and healthy.
