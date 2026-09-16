# Vellum - Audio Gated Portfolio

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, choose a door at the audio gate, walk the filterable wall of work, read
a case study end to end, drag the world scene and send a new-business enquiry,
without hitting an error page. A different stranger, and every signed-in reader,
and even the studio's other author, must NOT be able to reach an unpublished
project or its poster image by any means. The poster bytes must live in the
MinIO bucket at their scheme's key; a copy on the app's own disk does not count,
and neither does a row that says an upload happened.

---

## Overview
Vellum is the shop window for an independent brand, digital and motion studio,
and the editorial machine behind it. The public site is an entered space rather
than a page: an audio gate, a lit room scene, a filterable wall of work, long
case studies in ordered blocks, and a scene the visitor drags.

It collects one action that matters, the new-business enquiry, and the studio
publishes its own work from a signed-in console.

It deliberately does not transact: no comments, no likes, no messaging, no
search, no payments. The hard part is one rule. A draft project and its poster
object stay unreachable to everyone but their own author, the object store
included.

---

## User roles
| Role | Can do |
|---|---|
| `author` | The studio: create, edit, publish and unpublish their own projects, blocks and awards, upload a poster, promote one published project to `lead`, read the enquiry queue. **Cannot touch another author's projects, and cannot read their drafts or draft posters.** |
| `reader` | A signed-up account: reads every published surface and sends an enquiry. **Cannot reach the studio console, call any authoring endpoint, or read any draft or draft poster.** |

An anonymous visitor reads every published surface and may send an enquiry.
Everything else requires a bearer token.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `reader` session
to any `author`-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged.

Signup is open and creates a `reader`. `author` accounts are seeded only.

---

## Core features
### Auth
Email and password, hashed, with bearer tokens. An expired token on a mutating
call is rejected and the record is unchanged.

### The work
Every project is `draft` or `published`.

1. `/projects` and `GET /api/projects` list `published` projects only, ordered by
   `position` ascending. A `draft` appears on neither.
2. A draft project, its blocks, its awards and its poster answer its own author
   alone. An anonymous caller, a signed-in `reader` and the other author are
   refused on the route and on the poster endpoint.
3. Poster bytes live in the MinIO bucket under
   `projects/{project_slug}/{sha256_of_bytes}.{ext}`. A `poster_key` recorded for
   an object that was never written is invalid.
4. At most one project carries `lead` true at any moment. Two simultaneous
   promotions of different projects must not both succeed: exactly one wins, the
   other is rejected, and a failure leaves neither two leads nor zero.
5. Filtering `/projects` by a facet re-lays the wall out with no page load,
   reflects the facet in the location, and back restores the previous set.
6. A project `slug` is exactly two lowercase letters, unique, and may not equal
   `projects`, `world`, `contact`, `login`, `signup`, `studio` or `api`. A
   creation claiming one is rejected and stores nothing.

### The gate
7. `/` renders the intro overlay before any other content, carrying `Enter` and
   `Enter without audio`. No audio plays until one is pressed. Either dismisses
   the overlay with no reload, and the choice holds for the session.

### The enquiry
8. `POST /api/enquiries` takes `{ name, email, message, projectType, budget }`,
   the last two optional. A missing or malformed `name`, `email` or `message` is
   rejected with a reason per offending field and stores nothing.
9. A valid enquiry is durable before the response is sent, and the response
   carries its `reference`. Re-sending the same `email` with the same `message`
   stores one row and returns that same `reference`, never a second.
10. The form carries a `company_website` honeypot field no person fills. A
    submission carrying any value in it stores nothing and answers exactly as a
    stored one.

### The rest of the site
11. Every public route's footer links to `/terms`, as does `/signup`. The terms
    page states what the studio records about an enquirer.
12. Every internal link on every public route resolves; a link to a route the app
    does not serve is a defect.

---

## User flow
| Route | Purpose | Auth |
|---|---|---|
| `/` | Intro gate, then the room scene | none |
| `/projects` | Filterable wall of work | none |
| `/world` | Drag-to-explore scene | none |
| `/contact` | Studio details, enquiry form | none |
| `/:slug` | A case study, sample `/ma` | none |
| `/login`, `/signup` | Sign in; open signup | none |
| `/studio/projects` | Project table | `author` |
| `/studio/enquiries` | Enquiry queue | `author` |

**Entry and redirects.** An anonymous request to `/studio` lands on `/login`,
returning there after sign-in. A signed-in `reader` asking for `/studio` is
refused. Sign-in sends an `author` to `/studio/projects`, a `reader` to `/`.
Signing out invalidates the token. An unknown path, and a draft's route asked
for by anyone but its owner, both show not-found.

**Journeys.**
1. Open `/`, press `Enter without audio`: the overlay fades with no reload, the
   room is on screen, nothing has sounded.
2. Open `/projects`, press the `Motion` pill: the wall re-lays out to `Marlow`
   plus `Halcyon Field`, the location carries the facet, back restores the three.
   `Meridian Reel` never appears.
3. Open `/ma`: the filmstrip translates sideways as the page scrolls down, the
   awards strip scrolls in its own frame, next-project links to `/ls`.
4. Open `/contact`, send an empty form: each field carries its own error, with
   nothing stored. Fill it, send: the success line shows a reference, no reload.
5. As `author@example.com`, open `/studio/projects`, add a project in the inline
   row atop the table, upload a poster, publish: it is on `/projects`.
6. Sign out, ask for `/mr` plus its poster: both not-found. As
   `author2@example.com`: still refused. As `author@example.com`: both answer.

**States.** Every list has an empty state naming what would appear there, every
route a loading state, a failed request a message, never a broken page.

---

## UI/UX notes
Two registers in one product. The public routes are editorial and atmospheric,
the work seen first; the console is operational, quiet, dense. Someone should
understand in the first moment that this studio builds experiences rather than
pages, because they are standing inside one.

The console is command-line in character, high-contrast, unapologetically
technical. Type there is monospace everywhere, across the project table, the
enquiry queue and every figure that stacks. Motion there is instant: state
changes land the moment they happen, nothing eases in. Density is compact, so a
full project table fits one screen. The layout archetype is sidebar-nav: a fixed
rail, a table beside it, creation in a row atop that table, a saved row that
appears before the server answers and corrects itself if it disagrees.

Palette by role from the measured treatment pinned below: one blush ground, one
warm-white surface, near-black body text, one muted step for metadata, one
hairline border, one primary action with a darker pointed-at state, and a coral
accent belonging to the intro gate alone. Failure, success and in-progress each
own a colour meaning only that. Light is the committed mode, designed in full;
dark is optional. Type is a wide grotesque for interface, a display serif italic
for the oversized statements, tabular numerals where figures align. One curve
carries every public transition.

Round controls and large soft radii outside, tight rows inside. Space over
dividers outside, comprehension over atmosphere inside. Every control has
resting, pointed-at, pressed, focused and unavailable states; inputs carry a
label above with error text beneath, Escape closes what opened over the page,
unpublishing confirms first. Text and controls meet WCAG AA contrast, every
control is reachable by keyboard with a visible focus ring, icon-only controls
carry labels, meaning is never colour alone, reduced motion is honoured.
Behaviour holds at every viewport width between the named tiers.

Not a page dominated by one hue family with no second signal, and not a
marketing composition where a working interface belongs.

---

## Constraints

In scope: the public site, its projects, and the studio console behind it. The
non-goals are firm. Single tenant. No comments, no likes, no messaging, no
search, no notifications. No payments and no price surface. **No
email is sent**: an enquiry is persisted, worked in the studio queue. No second content source. No real-time collaboration, no
offline mode, no native app. No third-party analytics tag, no consent vendor and
no outbound network call at run time. No edge functions. The build ships no
binary asset of any kind. The only backing services are PostgreSQL and MinIO.
The app must stay responsive with 200 projects, 2000 blocks, 400 awards and 5000
enquiries.

---

## Technical requirements

The frontend is Astro with islands. The backend is Fastify on Node 20, serving
the HTTP API under the `/api` prefix on the same origin as the built assets. The
rendering model is server-rendered routes with islands: the browser receives the
route's real markup on first paint, and only the interactive pieces hydrate
afterwards, so `/projects` arrives readable before any script runs.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing services available in this environment are
PostgreSQL and MinIO, and reaching for anything else is a contract violation.

PostgreSQL is reached at `DATABASE_URL`. MinIO is reached at `STORAGE_ENDPOINT`
with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The app's
own origin and port are `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Read every one
of them from the environment and never hardcode a host or a port. Both backing
services are already running and reachable at those variables; do not download,
install, compile or start a copy of either.

Authentication is email and password implemented by the app, with bearer tokens
and hashed passwords. `GET /api/health` returns `200` once the app is ready.
Logs go to stdout.

### What every response carries

Every response carries the standard security headers, a strict transport policy
and a nosniff content-type policy among them. No credential, API key or admin
token appears in anything the browser downloads: not in a script, not in a
stylesheet, not in an inlined payload. The site serves a favicon and declares
that favicon in the document head of every route.

The enquiry endpoint is rate-limited and spam-guarded on two signals: the
honeypot field named in the core rules, and timing, so a form returned faster
than a person could have filled it is refused. Neither guard needs a third-party
script.

### Object keys and protected media

A poster object key is `projects/{project_slug}/{sha256_of_bytes}.{ext}`, for
example
`projects/ma/3f7c1d0b9a2e845f6c31d9b7e04a2c58f19d63b7c0a4e28d5f316b9c7a0d42e1.png`.
A block media object key is `blocks/{project_slug}/{block_position}/{sha256_of_bytes}.{ext}`.
The accepted poster types are PNG and JPEG, at most 8388608 bytes, and the type
is decided by reading the content rather than by trusting the extension: a
`.png` name over other bytes is rejected as invalid.

Protected media is reachable by exactly one of two mechanisms, and the build
picks one and stays consistent: an authenticated streaming endpoint on the app's
own origin, or presigned URLs valid for at most five minutes. Neither is ever
issued for a draft's object to a caller who is not that draft's author.

### The entered experience

The whole page is smooth-scrolled: wheel and touch input drive a transformed
scroll surface, and the reported scroll position is synthetic rather than the
document's own. One normalised progress value is published from that surface,
and the scene camera, the split-character reveals, the button fills and the
horizontal filmstrip all read it. Nothing reads the native scroll offset and
nothing runs a second frame timer, so scroll, scene and reveals never tear at
any scroll speed.

The three-dimensional layer is a real-time renderer with a perspective camera
whose position and target are driven by that same progress value. Materials are
lit by captured-sphere lighting textures rather than by scene lights, which is
why the look holds steady as the camera moves. It runs behind the layout with no
visible seam. Under load it sheds particles first, then the post-processing
pass, and only as a last resort freezes to a still composition; it must never
stutter.

The ambient sound bed is created and shaped in the browser's audio graph through
a filter node rather than merely played back. It is gated by the explicit choice
at the intro, is toggleable at any time from the corner control, and defaults to
the last choice for the session.

### Zero assets

The build ships no image, video, font file, mesh, texture or audio file. Every
asset class is procedural: meshes composed from primitives, lighting and surface
textures drawn on a canvas at load, project posters generated as seeded gradients
keyed per project slug so each project keeps a stable and distinct still, and the
sound bed synthesised from detuned oscillators through the same filter node. Only
the alphabet, the geometry and the numbers in this brief are required to produce
them. Typefaces are named from freely self-hostable equivalents with a fallback
stack and are never shipped as files.

---

## Data model

Seven tables. All timestamps are UTC.

> **Every seeded account uses the password `deku-demo-pw-2026`.** It is
> benchmark fixture data, not a secret. Hash it as normal; the exact literal
> must work at login, and it must be written into `/app/USER_README.md`
> alongside each account so a grader can sign in.

**users** - `id`, `email` unique and case-insensitive, `password_hash`, `role`
one of `author` or `reader`, `created_at`.

**projects** - `id`, `slug` unique, `title`, `client`, `facets` holding one to
three of `Brand`, `Digital` and `Motion`, `position` integer, `status` one of
`draft` or `published`, `lead` boolean, `published_at` nullable, `poster_key`
nullable, `summary`, `credits`, `author_id` referencing `users`, `created_at`,
`updated_at`. `published_at` is non-null exactly when `status` is `published`,
and `lead` is true only on a `published` row. At most one row in the whole table
has `lead` true at any time; this must hold under concurrent requests, not merely
in application-level checks, so two simultaneous promotions of two different
projects must not both succeed. Exactly one wins, the other is rejected, and a
failed attempt leaves no partial state: never two leads and never zero.

**project_blocks** - `id`, `project_id` referencing `projects`, `position`,
`kind` one of `full_bleed_media`, `paired_detail`, `pull_quote` or
`filmstrip_row`, `copy`, `media_key` nullable, `aspect_ratio` one of `16/9`,
`9/16`, `4/3`, `3/4`, `3/2`, `2/3` or `1`. Ordered by `position`.

**project_awards** - `id`, `project_id`, `name`, `year`, `position`. Ordered by
`position`.

**enquiries** - `id`, `reference` unique, `name`, `email`, `message`,
`project_type` nullable, `budget` nullable, `created_at`. Two submissions
carrying the same `email` and the same `message` leave one row and return the
same `reference`.

**pages** - `id`, `slug` unique, `title`, `blocks`.

**site_globals** - a single row: `contact_email`, `studio_phone`, `address_a`,
`address_b`, `social_twitter`, `social_instagram`, `social_linkedin`,
`social_dribbble`, `social_behance`.

Derived rather than stored: the count on each facet pill, the next-project
reference, every ordering, and every count rendered anywhere on the site.

**Seed data.** Three accounts, all with the password above:
`author@example.com` and `author2@example.com` as `author`,
`reader@example.com` as `reader`.

Four projects, by `position`: `ma` (`Marlow`, client `Alder`, facets `Brand` and
`Motion`, `published`, `lead` true, owned by `author@example.com`, carrying a
poster object); `ls` (`Loam Season`, client `Loam`, facet `Digital`,
`published`, owned by `author2@example.com`); `hf` (`Halcyon Field`, client
`Halcyon`, facet `Motion`, `published`, owned by `author@example.com`); `mr`
(`Meridian Reel`, client `Meridian`, facets `Brand` and `Digital`, `draft`,
owned by `author@example.com`, carrying a poster object).

`ma` carries five blocks in order: `full_bleed_media` at `16/9`, `paired_detail`
at `4/3`, `filmstrip_row` at `3/2`, `pull_quote`, and `full_bleed_media` at
`16/9`. It carries two awards: `Kestrel Award` of 2026 at position 1 and
`Fenwick Prize` of 2025 at position 2.

One page: slug `contact`, title `Contact`.

One `site_globals` row: `projects@vellum.co`, `(+44) 0117 900 0000`,
`35a Prospect Avenue, BS1 0AA`, `90 Print Street, EC2A 0BB`, and the five social
labels `Twitter`, `Instagram`, `LinkedIn`, `Dribbble` and `Behance`.

One enquiry: reference `ENQ-1001`, from `Rowan Hale` at `rowan@example.com`.

Seeding must be idempotent - restarting the app must not duplicate rows.

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
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running
  when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{ email, password }` | the created user and a bearer token |
| `POST /api/auth/login` | `{ email, password }` | a bearer token |
| `GET /api/projects` | `facet`, as in `GET /api/projects?facet=Motion` | a top-level JSON array of published projects, by `position`, narrowed to the facet when one is given |
| `GET /api/projects/{slug}` | none | one project with its blocks and awards; a draft answers its author only |
| `POST /api/projects` | `{ slug, title, client, facets, summary, credits, status }` | the created project |
| `PATCH /api/projects/{slug}` | any of `{ title, client, facets, position, summary, credits, status, lead }` | the updated project |
| `POST /api/projects/{slug}/poster` | the image bytes | `{ poster_key }` |
| `GET /api/posters/{slug}` | none | the poster bytes; a draft's poster answers its author only |
| `POST /api/projects/{slug}/blocks` | `{ position, kind, copy, aspect_ratio }` | the created block |
| `GET /api/pages/{slug}` | none | one page and its blocks |
| `GET /api/globals` | none | the studio contact and social block |
| `POST /api/enquiries` | `{ name, email, message, projectType, budget, company_website }` | `{ reference }` |
| `GET /api/enquiries` | none | a top-level JSON array, newest first, `author` only |
| `GET /api/health` | none | `200` |

Field names are exact. A successful call returns the named resource or shape. An
invalid or unauthorized call is rejected as a client error, never a `5xx` and
never a silent success. Bearer auth is required on everything except login,
signup, health, the published reads, the page and globals reads, and the enquiry
submission.

### No mocks

An in-memory list of projects, poster bytes written to the app container's
filesystem, a `poster_key` recorded for an object that was never written, a
hardcoded upload response the app returns to itself, an enquiry held only in a
process variable: each of these is a contract violation however good the
interface looks. PostgreSQL and MinIO are the fact. The app's UI and its own
tables can only reflect what lives in the provider, never substitute for it.

---

## Front-end specification

This section carries the measured visual specification supplied with this brief.
Every value here is a contract value: it was measured against a captured
reference, not chosen, and the numbers belong in the build. Values marked
inferred are reconstructions and may be tuned against the running product.

**Normative versus informational.** Every statement in this section is normative
unless it is labelled otherwise: it states a capability the build must have,
without naming a library. Where a sentence reports what the captured reference
happened to use, that is informational evidence and never an instruction, and the
build may satisfy the same capability by any means it likes. A measured number is
normative; the tool that produced it is not.

**Audiences.** Four audiences arrive and each is served somewhere different. A
prospective client asks whether the studio is good and whether it is for them,
and is answered by the index room and the wall of work. Press and awards want
notable work and credits, and are answered by the project routes, the awards
strip and the contact route. A collaborator or a hire wants tone and a way in,
and is answered by the world route, the contact route and the social links. A
returning visitor wants one specific piece of work and is answered by the
projects index narrowed by its facets. Every audience must reach its surface in
at most two moves from the entered home scene.

### Information architecture and navigation model

Five public places: the index room, the wall of work, one project's case study,
the world scene, and contact. There is no persistent visible menu bar. Global
chrome is three circular controls pinned to the corners of every route at
`z-index: 50`: a menu toggle, an audio mute toggle and a world shortcut. The
menu toggle raises a full-screen overlay carrying four numbered destinations and
the studio footer. Menu order is fixed: `01 Index`, `02 Projects`, `03 Contact`,
`04 World`. Two-letter path segments are project slugs, and a single-letter
trailing segment is an in-page anchor within a case study; neither is ever
top-level navigation.

### Colour

| Role | The colour, described |
|---|---|
| Primary ground | a near-white, muted warm red: the blush the whole public site sits on |
| Ink | a deep neutral, never a pure near-black neutral, for body text |
| Hard black | a near-black neutral, reserved for icon geometry |
| Panel | a near-white neutral, and a second warmer near-white neutral beside it |
| Loader accent box | a near-white, muted red, warmer than the ground; the coral, used here alone |
| Hairline | a near-white neutral one step below the panels |
| Mid grey ramp | three light neutrals, each distinguishable from the next |
| Deep grey | a deep neutral, for the progress stroke and secondary marks |
| Scene shadow | a near-black cool neutral with a blue cast |
| Overlay scrim | the hard black at half opacity |
| Hairline on dark | a near-white neutral at low opacity |

A saturated preset set is available to editorial blocks only and is not core
brand colour: a mid, vivid cyan and a light, soft cyan; a mid, vivid teal and a
light, soft teal; a mid, vivid orange and a second, hotter mid, vivid orange; a
mid, vivid red and a light, soft red; a light, vivid indigo; and a light cool
neutral. The scene palette additionally carries a deep, soft green and a
near-black neutral. Ten presets plus two scene colours, thirteen in all, and the
exact values are the builder's so long as each stays distinguishable from its
neighbour at body size.

### Type scale and typefaces

Root sizing is viewport-derived, which is why the rendered scale is fractional.
Reproduce the rule, not the fractions.

| Tier | Rendered size and line-height | Weight | Role |
|---|---|---|---|
| Display XL | `90px / 90px` and `87.5px / 87.5px` | 400 | oversized serif statements |
| Display L | `57.6px / 86.4px`, `56px / 84px` | 400 | section headings |
| Heading | `42px / 42px` | 400 | route titles |
| Subhead | `28.8px / 28.8px` | 300 | lightweight intros |
| Body | `18.72px`, `18.2px`, `17.28px` | 400 | paragraph copy |
| Body small | `16.8px`, `15.12px`, `14.4px`, `14px / 21px` | 400 | metadata, captions |
| Micro | `11.52px`, `11.2px`, `10.08px`, `9.8px`, `8.75px` | 400 | eyebrows, numerals |
| Body emphasis | `14px / 21px` | 700 | inline emphasis |

Two families carry the public routes. A wide geometric grotesque with a large
x-height carries interface and body and every tier except Display XL; a
high-contrast display serif with a true italic carries Display XL. Both are
self-hosted and subset, and neither blocks first paint. Name a freely
self-hostable grotesque with the fallback stack `system-ui`, `Arial`,
`sans-serif`, and a freely self-hostable display serif with the fallback stack
`Georgia`, `Times New Roman`, `serif`. Naming a freely hostable font is not an
asset dependency; shipping a font file is.

### Spacing scale, radii, shadows and layout tokens

Spacing custom properties, in rem: step 20 `0.44rem`, 30 `0.67rem`, 40 `1rem`,
50 `1.5rem`, 60 `2.25rem`, 70 `3.38rem`, 80 `5.06rem`.

Radii in use: fully round controls at `50%` and `100%`; pill filter buttons at
`175px` to `180px` with a fill layer at `26.25px` to `27px`; button inners at
`21px`, `21.6px`, `23.1px` and `23.76px`; the cursor circle at `16.8px` to
`17.28px`; panels at `10px`.

Named shadow tokens: crisp `6px 6px 0px rgb(0, 0, 0)`; sharp
`6px 6px 0px rgba(0, 0, 0, 0.2)`; natural `6px 6px 9px rgba(0, 0, 0, 0.2)`; deep
`12px 12px 50px rgba(0, 0, 0, 0.4)`; outlined
`6px 6px 0px -3px rgb(255, 255, 255), 6px 6px rgb(0, 0, 0)`.

Aspect-ratio presets: `16/9`, `9/16`, `4/3`, `3/4`, `3/2`, `2/3`, `1`. Editorial
preset font sizes: `13px`, `20px`, `36px`, `42px`. Root custom properties
`--screen-height: 900px` and `--vh` drive the viewport-derived sizing.

### Iconography

Every icon is inline vector geometry. The build ships no icon file.

**Eyes mark, the studio logo.** `viewBox="0 0 311.3 233.3"`, 14 primitives: a
left and a right eye outline as `path`s beginning
`M139.5,101.5c2.5-7.8,6-14.8,10.3-21...` and
`M206,58.9c-3.8-1.2-7.6-1.8-11.4-1.8...`; two left pupil ring `ellipse`s with
transforms `matrix(0.3023 -0.9532 0.9532 0.3023 -22.508 182.8248)` at cx `113.6`
cy `106.8` and `matrix(0.2938 -0.9559 0.9559 0.2938 -24.3184 186.5732)` at cx
`114.1` cy `109.7`; a left pupil dot `circle` cx `132.6` cy `120.7` r `11`; two
right pupil ring `ellipse`s with transforms
`matrix(0.3023 -0.9532 0.9532 0.3023 19.5634 260.2873)` at cx `187.6` cy `116.8`
and `matrix(0.2938 -0.9559 0.9559 0.2938 23.4151 259.1791)` at cx `187.1` cy
`113.7`; a right pupil dot `circle` cx `208.6` cy `121.7` r `11`; an upper blink
mask `rect` x `62.9` y `22.3` width `103.2` height `78.5` transform
`matrix(1,0,0,1,0,-46.315)`; a lower blink mask `rect` x `65.1` y `125.7` width
`89.3` height `78.5` transform `matrix(1,0,0,1,0,33.755)`; a left brow accent
`path` `M131.8,98.8c-0.9-2.8-3-5.3-5.8-6.2...`; a right brow accent `path`
`M158.8,104.8c0.1-7,5.7-13.4,13.1-12.3...`; and a heart `path.js-eyes-heart`
`M139.5,101.5...` that the pupils morph to on hover. Eye outlines and pupil dots
filled the hard black on a near-white neutral sclera. The two mask rects slide on scroll-scrubbed
transforms to make the eyes blink.

**Menu toggle.** `viewBox="0 0 14 5"`, two circles, both r `2.4`, filled the ink,
centres at cx `2.4` cy `2.4` and cx `11.6` cy `2.4`. The dots animate apart into
a close glyph when the overlay opens.

**Audio mute.** `viewBox="0 0 18 16"`, five vertical `line` bars at
`stroke-width` `2`, scaled by transforms `matrix(1,0,0,1,0,0)`,
`matrix(1,0,0,0.8,0,3.2)`, `matrix(1,0,0,0.6,0,6.4)`, `matrix(1,0,0,0.4,0,9.6)`
and `matrix(1,0,0,0.3,0,11.2)`. The heights animate continuously while audio
plays and settle flat when muted.

**World and play button.** `viewBox="0 0 100 100"`: a backing `circle` cx `50` cy
`50` r `49`; a play triangle `path`
`M58,49.1c0.7,0.4,0.7,1.3,0,1.7l-14.2,8.2c-0.7,0.4-1.5-0.1-1.5-0.9V41.8c0-0.8,0.8-1.3,1.5-0.9L58,49.1z`
filled the hard black; and two pause bars at x roughly `42` and `52`, width about `5`,
height about `18`. Play and pause cross-fade.

**Cursor drag arrows.** `viewBox="0 0 46 10"`, two arrow `path`s filled the
hard black: left
`M14.1667 5.625H2.15333L5.32667 9.125L4.53333 10L0 5L4.53333 0L5.32667 0.875L2.15333 4.375H14.1667V5.625Z`
and right
`M31.0001 4.375L43.0134 4.375L39.8401 0.875L40.6334 0L45.1667 5L40.6334 10L39.8401 9.125L43.0134 5.625L31.0001 5.625L31.0001 4.375Z`.

**Progress ring.** `viewBox="0 0 100 100"`, two concentric `circle`s r `39`: a
track stroke at the hairline and a progress stroke at the deep grey carrying
`transform=rotate(-90)` so it fills from twelve o'clock. It drives the loader and
the media scrubbers.

**Close and add control.** `viewBox="0 0 48 48"`, a ring `circle` cx `24` cy `24`
r `23.5` and three `line`s at `stroke-width` `2` forming a plus that rotates to a
cross on toggle.

**Wordmark logotype.** The reference wordmark is one inline
`svg#Layer_1`, `viewBox="0 0 1263.3 159.6"`, 13 `path` primitives plus a
registered-mark ring. Set the wordmark from the display grotesque instead of
reproducing the outline.

**Footer arrow glyph.** Each footer contact and social line is prefixed by an
inline turn-down-right arrow glyph.

### Global chrome and button mechanics

Each corner control is `border-radius: 50%`, built from stacked layers: a
filling background circle at `border-radius: 100%`, an inner at `23.1px` radius,
and an inner background that scales from `matrix(1e-05,0,0,1e-05,0,0)` to full on
hover, a radial wipe from the centre. `will-change: transform` is set on those
backgrounds and nowhere else by default.

Rectangular buttons, the filter pills and the Enter button are not CSS-bordered.
Each carries an inline `svg` of stacked `rect`s driven by mask references: a
background rect, a fill rect, a border rect and a hover border rect, each masked
by its own generated mask. On hover the fill rect's mask animates so the fill
wipes in directionally and the border draws on, independently of the label. A
background colour transition is not an acceptable substitute.

The overlay menu carries the four numbered nav items, each label split into
per-character elements with a duplicate hover-character layer for the hover swap,
a serif italic hover caption per item, and the footer block. Each nav character
enters from `matrix(0,0,0,1,...)`, scaled to zero width, to full, staggered
across the label.

The footer carries the new-business email `projects@vellum.co`, the phone
`(+44) 0117 900 0000` and five social links, each prefixed by the arrow glyph
and each pointing at one profile: a short-form social profile labelled
`Twitter`, an image social profile labelled `Instagram`, a professional network
profile labelled `LinkedIn`, a design-community profile labelled `Dribbble` and
a portfolio-community profile labelled `Behance`. The two
studio addresses `35a Prospect Avenue, BS1 0AA` and `90 Print Street, EC2A 0BB`
sit on the contact route.

### Motion language

Three movement characters carry almost all motion. The dominant one, on every
transform reveal and used in over a hundred places, leaves quickly and arrives
slowly, coasting to rest over about a second with no bounce at the end. The
second, on opacity reveals over about seven tenths of a second, does the same
more gently. The third is symmetric, an ease-in-out in character: it starts and stops at the
same rate, it appears in exactly two declarations, and it is reserved for the two
places a thing has to feel reversible. One further
movement is its own, named for the hand it makes from the project menu into a
project route: it overshoots slightly at the midpoint, then settles, so the menu
appears to pass the reader through rather than cut away.

Everything else is shorter and plainer: about four tenths of a second, even in
and out, for the small state changes; about half a second, leaving quickly, for
a colour or a fill change; about two tenths for a snap; and about half a second,
leaving quickly, for an overlay's opacity and visibility together. Nothing on
the public routes is instant, and nothing takes longer than the second the
dominant character uses.

Headings and nav labels are split into per-character elements. Characters begin
scaled to zero width at `matrix(0,0,0,1,x,0)` with per-character x offsets
measured at `0.9`, `3.6`, `8.1` and `14.4`, and reveal to `matrix(1,0,0,1,0,0)`
on the house curve, staggered along the word so it unfurls rather than fading as
a block. Nav hover characters translate vertically at
`matrix(1,0,0,1,0,25.2656)` and `matrix(1,0,0,1,0,24.5625)`, so a duplicate line
slides up as the original slides away. Scrolling backwards un-reveals split text.

The loader boxes run an infinite `4000ms linear` animation. The loader progress
bar transitions `transform` over `1000ms ease-out` with `fill: backwards`.
Circular controls scale their inner background from near-zero on hover, and
colour and fill changes ride `color 0.5s ease-out` and `fill 0.5s ease-out`.

### Scroll system

The page does not scroll natively. The document root carries a scroll-disabled
state class while the loader or an overlay is up, the native scroll offset stays
at `0`, and content moves by transform on a scroll proxy. Wheel and touch input
are captured and eased into that transform, and the engine exposes a normalised
progress value per scrubbed element.

Measured scroll geometry on the sample project route: desktop total
`13836px`, with frames at `0, 1660, 3459, 5119, 6918, 8578, 10377, 12037,
13836`; tablet total `10776px`, with frames at
`0, 1293, 2694, 3987, 5388, 6681, 8082, 9375, 10776`. A case study is therefore
roughly seven to nine viewports tall, in even beats of about `1700px`.

Scroll-scrubbed surfaces, with the number of distinct sampled values: the button
fill mask (7), a third-width horizontal filmstrip track (10), the two loader
boxes (9), the menu characters (8), the equaliser bars on the home route (9), the
nav items (4), the internally scrolling awards list (4 to 6), the serif italic
hover caption (3), the eyes and the heart path (2 to 4), and a masked group's
clip path (2).

### The three-dimensional layer

Two scenes. The home room composes an interior from separate meshes: two room
shells, a table, a chair, pillows, rocks, a land group, a grass field, a
particles layer and a bundled objects container. Lighting is baked as captured
sphere textures: a pearl one, a black one, a white one, an ambient-occlusion
texture and a sky map tile. No light objects exist, which is why the look is
stable as the camera moves.

The second scene backs the project menu and the world route: a butterfly with a
diffuse and a normal atlas, an arch and a floor, lit by a dedicated project-model
capture in a light and a dark variant. The camera is a perspective camera whose
position and target ride the smooth-scroll progress. The loader wrap carries CSS
`perspective: 448px` rising to `460.8px`, and a card container carries `1000px`;
these frame the three-dimensional loader boxes before the scene takes over.
Surface treatments in use: a noise texture, a gradient-noise texture, an
iridescent lookup and a grass blade texture. The loader eyes sit on a
`preserve-3d` stage with the loader boxes and share the scrubbed transform
channel.

### Audio system

An ambient bed is created or shaped in the browser's audio graph through a
biquad filter, so it can be softened and opened rather than only made louder.
Nothing sounds before the visitor opts in at the intro. The mute control shapes
or cuts it, its five bars animate continuously while unmuted and settle flat on
mute, and `fill 0.5s ease-out` carries the colour change. Short interface cues
sit over the bed: a soft rising sine over a fraction of a second on hover and a
shorter one at the door hand-off. Both the bed and the cues are inferred
reconstructions, synthesised rather than recorded.

### Loader and intro gate

Centred on the blush ground: the eyes mark, resolving out of a single large
glyph; the six brand letter tiles `V E L L U M`, which arrive scrambled and
settle to the word; the title `Vellum`; the tagline in three lines,
`A brand, digital and motion studio creating`,
`refreshingly unexpected ideas and striking visuals`, and
`that help bold brands cut through the noise.`; the `Enter` button carrying a
down-right arrow and the button fill mechanics above; and a text link at the
foot reading `Enter without audio`.

Two stacked boxes, the second in the loader coral, sit on a `preserve-3d`
wrap and tumble in three dimensions on the infinite `4000ms linear` loop. The
progress element fills from empty to full as the scene streams behind it. Either
door fades the overlay on
`opacity 0.5s ease-out, visibility 0.5s ease-out` with no reload, the root gains
its loaded state class, and the eyes blink once on hand-off. A second, minimal
loader wrap covers in-session route transitions so navigation never shows the
full front door twice.

### Route: Index

The home route is the entered room with layout copy composited over and after
it. Inferred structure, top to bottom: hand-off from the loader into the lit room
with the camera settled; an oversized serif italic statement at Display XL as the
opening line, revealed by split characters; a scroll passage through the room as
the camera moves, with copy pinned and released against scene beats; a transition
into the project-menu scene; then the footer. The camera keyframe contract is
inferred: settle, dolly through the room, rise to reveal the land group, then
push toward the project-menu scene. The eyes mark persists as a small fixed
element and blinks on scroll beats.

Type-in-scene: the Display XL serif statements sit in front of the rendered
scene rather than inside it, on their own layer, and reveal per character as the
camera passes their beat. They stay selectable text in the reading order, never
geometry, so the type-in-scene composition costs the scene nothing and is
readable with the scene frozen.

### Route: Projects

Filtering is a pill-button facet row with an active state per facet, an animated
fill layer and a disclosure chevron. Filtering is client-side and instant over an
already-loaded set, the active facet is reflected in the location so a
back-navigation restores it, and the filtered set re-lays out without a full
reload.

The gallery is a mixed-ratio masonry built from the aspect-ratio tokens, never a
grid of identical boxes. Each card is one project showing a generated poster
still and its title. Hover animates the card fill and lifts the title. Cards
route to the case study on the house curve, or on the `projectMenuToProject`
curve when they are opened from the menu scene. On enter, a card may swap its
still for a slow generated gradient drift in place of a video preview.

### Route: Project detail

Opened from the project menu the route transitions on the `projectMenuToProject`
curve; opened from the projects grid it uses the house curve. The vertical
rhythm runs in even beats of about `1700px`, each beat a composition unit: title,
full-bleed media, paired detail, pull quote, credits. The signature device is the
third-width horizontal track that translates sideways as the reader scrolls
down, ten sampled positions. Full-bleed media sections use the progress ring as a
scrubber or loop indicator. An awards list scrolls within its own frame near the
foot, followed by credits and a next-project link back into the menu scene.

### Route: World

A drag-to-explore scene reusing the project-menu composition. The cursor shows
the drag arrows over it. Pointer drag orbits or pans the camera and releasing
eases back on the house curve, so the view coasts to a stop. The corner world
shortcut routes here. The butterfly is the animated focal point; its wing
animation is an inferred keyframe contract, wings rotating about the body axis
between roughly plus and minus forty degrees on a slow loop eased on the house
curve.

### Route: Contact

Studio details and the one workflow that touches server state. It carries
`projects@vellum.co`, `(+44) 0117 900 0000`, the two addresses and the five
social links. The form fields are labelled `Name`, `Email`, `Message` and
`What do you have in mind?`, and the submit control reads `Send`. On success the
line `Thanks. We will be in touch.` appears with the enquiry reference. Inline
validation, the submitting state on the button fill, and the success and error
states all happen without a page reload. The layout is two columns on desktop,
details left and form right, and stacks on mobile.

### Custom cursor system

A bespoke cursor replaces the pointer: a circle at `border-radius: 16.8px` to
`17.28px`, plus a hold inner and hold outer pair that scale up from
`matrix(0,0,0,0,0,0)` on press and hold, plus the drag-arrows glyph. The circle
trails the pointer with eased interpolation so it arrives a beat late, and it
must never introduce latency on the actual click target. States: a small circle
by default; grown with a changed fill over a link or button; the drag arrows over
a draggable surface; the hold rings while pressed. On touch and coarse pointers
the custom cursor is disabled and native hit targets are used.

### Module and component architecture

Layering: four cooperating layers sit over one render loop, in this order from
the back. The scroll proxy captures input and produces eased progress. The scene
layer draws the room and binds its camera to that progress. The DOM layout layer
carries the copy, the cards and the forms, positioned over and between scene
beats. The chrome and cursor layer sits above everything. The layering is fixed;
no layer reaches into another's state. A single animation frame drives all four, which is
the central architectural constraint. The named responsibilities are the loader,
the naked loader, the smooth-scroll proxy and progress bus, the scene root, the
home and menu scenes, the split-text reveal, the masked-fill button, the circle
button, the overlay menu, the cursor, the audio bed, the project filters, the
project grid, the case study as a long-scroll story with its horizontal
filmstrip, the world scene controller, the contact form and the footer. The progress bus publishes one normalised value plus per-element
scrub values, and no component reads the native scroll offset. Client-side route
transitions swap the DOM and re-target the camera without a full reload.

### State machine and root classes

Global state lives as classes on the document root and every part of the
interface reads it. The observed states are: smooth scroll suspended, during the
loader or an overlay; loaded, meaning the intro is dismissed and the experience
entered; menu open, meaning the overlay is raised; and scrolling, meaning smooth
scroll is in motion, which drives the cursor and the chrome. The loader sets
scroll-suspended; the door hand-off clears it and sets loaded; opening the menu
re-suspends scroll and sets menu-open; closing reverses it; a route change raises
the naked loader and briefly re-suspends scroll.

The z-index ladder, low to high: `-1` for scene backdrops, then `1`, `2`, `5`,
`10`, `12`, `39`, `40`, `50` for the corner chrome, `60`, `70`, `80`, `900`,
`11000`, and `12000` for the loader and the overlay.

### Responsive behaviour

Measured breakpoints, by frequency: `min-width: 768px`, `min-width: 1366px`,
`min-width: 1024px`, `min-width: 414px` and `min-width: 1921px`. Read as base
mobile, `414` large phone, `768` tablet, `1024` and `1366` desktop tiers, and
`1921` wide desktop. Root font size derives from the viewport through
`--screen-height` and `--vh`, so the scale flexes with window height and not only
width.

Across breakpoints: the scene remains but simplifies, with fewer meshes, lower
particle counts and reduced post-processing; the horizontal filmstrip reduces its
card width and travel, so the tablet case study totals `10776px` against the
desktop `13836px`, which is compression rather than a wholesale reflow; the
custom cursor is disabled on coarse pointers; and two-column layouts stack.
Orientation is a real axis and not a side effect of width: portrait orientation
selects the card ratios `9/16`, `2/3` and `3/4`, and landscape orientation
selects `16/9`, `3/2` and `4/3`. A narrow window in landscape orientation takes
the landscape ratios, not the portrait ones.

### Accessibility

The intro is dismissible by keyboard: both `Enter` and `Enter without audio` are
focusable controls with visible focus, reachable without a pointer. A reduced
motion preference suspends the split-character waves, freezes the scene to a
still composition and cuts the loader loop to a short fade. Audio never
autoplays.

The oversized serif statements are real headings in the reading order, not
decorative text, and the eyes mark carries an accessible name for the studio. The
overlay menu is a labelled navigation region, its items are links, and the
numbered prefixes `01` to `04` are decorative. Screen-reader-only labels use the
`clip-path: inset(50%)` visually-hidden pattern; the menu toggle's is
`Toggle Menu`, and the mute and world controls carry equivalents. The filter
pills are real buttons whose pressed state reflects the active facet. The contact
form has associated labels, inline error text, and a submit state announced to
assistive technology.

The ink on the blush ground, and the ink on a near-white neutral panel, both meet
the body contrast bar. The micro tiers between `8.75px` and `11.2px` must be
checked against their own grounds and darkened toward the hard black where they
fall short.

### Performance

Hold a smooth frame rate on a three-year-old laptop with the scene running. The
loader is first meaningful paint and must appear before anything heavy loads, with
the scene streaming in behind the progress element. Degrade in a fixed order: drop
particles, then the post-processing pass, then fall back to a still scene
composition, rather than stuttering. Project and case-study media load lazily
below the fold. One render loop only, no component with its own frame timer.
`will-change: transform` goes only on the elements that need it, never blanketed
across the page. Off-screen scenes pause their loop.

### Delivery

Delivery is static-first. Every route prerenders its copy and its structure at
the server, so the wall of work, a case study's blocks and the contact details
are all present in the first response. The scene, the custom cursor and the
smooth-scroll surface hydrate on the client afterwards and never gate the text.
Project content is read from the app's own store at request time rather than
compiled into the bundle, so publishing a project from the studio console changes
the public wall without a rebuild. Nothing in the delivery path may block first
paint.

### Document titles and route copy

The home document title is `Vellum - Brand, Digital & Motion`. A project document
title is the project title, then a spaced hyphen, then `Vellum`, so `/ma` reads
`Marlow - Vellum`.

### Zero-asset substitutions

Compose each mesh from primitives and keep the original object names so the scene
graph runs unmodified. Room shells: two open boxes, one face removed, nested for
wall and floor. Table: a rounded box top on four cylinder legs. Chair: a rounded
box seat, a back panel, four legs. Pillows: rounded boxes with a high corner
radius, slightly squashed. Rocks and the land group: low-frequency displaced
spheres and a subdivided plane displaced by noise. Grass: instanced thin blades
on the land plane, count reduced on small screens. Particles: an instanced point
cloud. Butterfly: two thin wings mirrored on a capsule body. Arch: a half-torus
on two cylinders. Floor: a subdivided plane. Keep the original object names from
the menu-scene meshes, `butterfly`, `arch-dc` and `floor-dc`, so the scene-graph
code runs unmodified.

Generate each captured-lighting texture on a canvas: a radial gradient with the
bright highlight offset up and left, dark toward the lower right, and one small
hot specular dot. The five the scene asks for, by their original matcap names,
are `pearl-matcap`, `matcap-black`, `matcap-white`, `project-model-matcap` and
its dark variant. The pearl variant adds a faint iridescent sweep. The black and
white variants are the same generator at two brightness settings. Compressed
scene textures become canvas-generated equivalents at load, so no
compressed-texture pipeline is needed at all. Spend the most effort here: this is
what most decides the look of a scene lit this way.

Surface maps: fine multi-octave turbulence, desaturated so it adds tone and not
colour, for grain and noise; a small horizontal gradient ramp cycling through
the cyan, the indigo, the teal and the orange from the preset set for the
iridescent lookup; and a vertical gradient from a darker to a lighter green, based
on the scene's deep, soft green, for the grass blade.

Project and card media: seeded gradient posters keyed per project slug so each
project has a stable, distinct still, drawn from the palette above. Where a card
would play a preview, loop a slow generated gradient drift instead. Full-bleed
case-study video becomes the same generated drift at full size.

### Evidence gaps

The captured reference gated every route behind the audio intro and the capture
never went through it, so the entered home composition, the projects grid layout,
the world interaction and the contact page are reconstructed from the copy deck,
the scene manifest and the one project route that reported real scroll. Hover
states came back empty and are reconstructed from the duplicate-character layers,
the masked button fills and the declared transitions. Mesh-baked animation, the
butterfly flap and the home camera path could not be recovered and are inferred
keyframe contracts here. Three icon colours were mapped to the nearest palette
token: the play fill to the hard black, the ring track to the hairline and the
ring progress to the deep grey. The reference typefaces are commercial faces and are
replaced by self-hostable equivalents with the fallback stacks named above. The
new-business form and its endpoint are specified rather than observed. What is
measured and can be trusted: the palette, the type scale, the spacing, the radii,
the shadows, the easing curves, the scroll geometry, the breakpoints, the icon
geometry and the copy strings pinned above.

---

## Definition of done

A visitor chooses a door at the audio gate, walks a wall of work that filters
instantly and survives a back-navigation, reads a case study whose filmstrip
moves sideways as they scroll down, drags the world scene, and sends an enquiry
that comes back with a reference. An author publishes a project with a poster
image and sees it appear on the wall, and exactly one project is the lead at a
time. An unpublished project and its poster stay unreachable to everyone but
their own author. The app is deployed and healthy.
