# Slate - App Builder Marketing Site

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, read the pitch, check the answers, describe the app they want in the
prompt box and attach a spreadsheet, and have that request filed, without
hitting an error page. A different stranger, and every signed-in reader, and
even the site's other author, must NOT be able to read an unpublished article or
its cover image by any means. The cover bytes must live in the MinIO bucket at
their scheme's key; a copy on the app's own disk does not count, and neither
does a row that says an upload happened.

---

## Overview
Slate turns a spreadsheet a business already keeps into a running application.
This build is the shop window and the editorial machine behind it: seven public
reading surfaces, one not-found surface, and a studio where the site's own
authors publish the four collections those surfaces read.

Every route carries the same primary action, and it is not a form. It is a
prompt composer that files a build request, inline in the home hero and pinned
to the bottom of the viewport after it.

It is deliberately not the product it sells: no visual editor, no sync, no
workflow runner, no billing, no comments, no search. The hard part is one rule:
an unpublished article is unreachable by anyone but its author, the object store
included.

---

## User roles
| Role | Can do |
|---|---|
| `author` | The studio: create, edit, publish and unpublish their own records in all four collections, upload an article cover, feature one published article. **Cannot touch another author's records, and cannot read their drafts or draft covers.** |
| `reader` | A signed-up account: reads published surfaces, files a build request, subscribes. **Cannot reach the studio, call any authoring endpoint, or read any draft or draft cover.** |

An anonymous visitor reads every published surface and may file a build request
and a subscription. Everything else requires a bearer token.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `reader` session
to any `author`-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged.

Signup is open and creates a `reader`. `author` accounts are seeded only.

---

## Core features
### Auth
Email and password, hashed, with bearer tokens on every authenticated call.
Tokens expire; an expired token on a mutating call is rejected and the record is
unchanged.

### The four collections
Articles, press items, jobs and question entries. Every record is `draft` or
`published`.

1. A public collection route lists `published` records only, newest first.
2. A `draft` is readable only by the account in its author field; anyone else is
   denied, identically whether the slug exists or not.
3. At most one article is `featured` at any time, and featuring a second clears
   the first. Two simultaneous requests featuring different articles must not
   both succeed: exactly one wins, the other is rejected, and exactly one row
   stays featured.
4. An author acts only on their own records: a request from
   `author2@example.com` against a record owned by `author@example.com` is
   denied and the row is unchanged.
5. A job with `open` false is absent from the careers list while its own route
   still resolves; the department grouping is computed on read.

### Covers
6. A cover is written into the MinIO bucket under the key scheme pinned in
   Technical requirements. The row carries the key; the bytes exist nowhere
   else, not on the filesystem and not in a column.
7. Cover bytes are read only through `GET /api/covers/{slug}` on the app's own
   origin. A published cover answers anyone; a draft's answers only its author
   and is denied to everyone else. No presigned read URL is issued for a cover.

### The composer and the build request
8. The composer is on every route. It sits inline in the home hero, pins to the
   bottom of the viewport for the rest of the scroll, and keeps its typed value
   across that transition without a layout jump.
9. An attachment goes from the browser straight into the bucket under a
   presigned PUT grant expiring 300 seconds after it is issued. The site never
   proxies those bytes, and the build request carries the attachment identifier
   rather than the file.

### The subscription
10. Submitting an email records a pending subscription and returns the same
    response whether or not that address was already on the list.

---

## User flow
| Route | Purpose | Auth |
|---|---|---|
| `/`, `/byoa` | Home; bring your own agent | none |
| `/docs`, `/docs/:page` | Documentation portal | none |
| `/faqs` | Questions and answers | none |
| `/blog`, `/blog/:slug` | Editorial index and article | none |
| `/news` | Press digest, paginated | none |
| `/jobs`, `/jobs/:slug` | Careers and one opening | none |
| `/login`, `/signup` | Sign in; open signup | none |
| `/studio/*` | Studio: one grid per collection | `author` |
| `/e/:id`, `/i/:id`, `/s/:id`, `/va/:id` | Parametric prefixes | none |

**Entry and redirects.** An anonymous request to `/studio` or below lands on
`/login` and returns there after signing in. A signed-in `reader` asking for
`/studio` is refused. Signing in sends an `author` to `/studio` and a `reader`
to `/`. Signing out invalidates the token. An unknown path renders the
not-found surface.

**Journeys.**
1. Open `/`, type into the composer, scroll past the hero, watch it pin with the
   typed text intact, attach a spreadsheet, and submit.
2. Sign in as `author@example.com`, open `/studio/articles`, see three cards of
   which `Agents Reading Your Schema` is a draft. Write a new article in the
   slide-over and save it as a draft: it appears at once and is absent from
   `/blog`. Publish it and it appears on `/blog`, newest first.
3. Sign out and ask for `/blog/agents-reading-your-schema` and its cover: both
   refused. As `author2@example.com`: still refused. As `author@example.com`:
   both answer.
4. Feature `What Your Warehouse Sheet Already Knows`; the previously featured
   article is no longer featured and `/blog` shows one featured card.
5. On `/blog` submit `subscriber@example.com`, already on the list, then a fresh
   address. The two responses are identical.

**States.** Every collection surface has an empty state naming what would appear
there, every route has a loading state, and a failed request shows a message
without breaking the page. On any route shorter than the viewport the footer
sits at its bottom.

---

## UI/UX notes
A command-line product, high-contrast and unapologetically technical. Someone
should see in the first moment that this company's own tool is an operator's
console rather than a brochure: the public routes sell, the studio works.

Type is monospace everywhere across the studio, the agent terminal and every
figure that stacks; the editorial reading measure keeps a proportional face,
because long prose is the only thing here read at length.

Motion character is instant, and it governs the studio: a save, a publish and
the create panel land the moment they happen rather than easing in. The seven
public routes keep the measured house easing set out in the front-end
specification, which is what keeps the selling surfaces and the working surface
distinguishable. One character governs each side, with no per-component
exception, and reduced motion is honoured on both.

Density is compact, so a full collection fits one screen. The layout archetype
is sidebar-nav: a fixed rail of the four collections, a card grid beside it,
creation in a slide-over, and a saved row that appears before the server answers
and corrects itself if it disagrees.

Palette by role, never by notation. One warm charcoal carries body text; two
lighter steps carry secondary and tertiary text and stay distinguishable. One
value draws every hairline and outlined pill. One saturated teal is the accent,
reserved for progress, documentation links and one large mark. Failure, success
and in-progress each own a colour that means only that. The careers route
carries a pale acid ground found nowhere else. The exact shades are yours, so
long as those rules hold.

Fully rounded pills for buttons, tags and switches, a gentle corner elsewhere.
Space over dividers, comprehension over atmosphere. Commit to light and design
it through; a dark mode is optional and is not asked for.

Every control has resting, pointed-at, pressed, focused and unavailable states;
Escape closes what opened over the page and unpublishing confirms first. Text
and controls meet WCAG AA contrast, every control is reachable by keyboard with
a visible focus ring, icon-only controls carry labels, and meaning is never
carried by colour alone. Responsive behaviour must hold at every viewport width
between the named tiers, not only at them.

Not a page dominated by one hue family, and not a marketing composition where a
working interface belongs.

---

## Constraints

In scope: the site and its four collections. The non-goals are firm. Single
tenant. No comments, no likes, no messaging, no search over customer
data, no notifications. No visual editor, no spreadsheet sync, no computed
columns, no workflow runner, no agent runtime, no metering, no billing. No payments and no price
surface. No email is sent; a subscription records a pending confirmation and
stops there. No real-time collaboration, no offline mode, no native app. No
third-party analytics tags, no consent vendor, and no outbound network call at
run time. No edge functions. The only backing services are PostgreSQL and MinIO.
The app must stay responsive with 200 articles, 400 press items, 60 job
openings and 300 question entries.

---

## Technical requirements

The frontend is Svelte with Vite, built to static assets. The backend is NestJS
on Node 20, serving the HTTP API under the `/api` prefix on the same origin as
those assets. The rendering model is a single-page application over a JSON API:
the browser receives one application shell on first paint, the same shell for
`/blog` as for `/jobs`, and each route's content arrives as JSON from the same
origin afterwards.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing services available in this environment are
PostgreSQL and MinIO, and reaching for anything else is a contract violation.

PostgreSQL is reached at `DATABASE_URL`. MinIO is reached at
`STORAGE_ENDPOINT` with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and
`STORAGE_SECRET_KEY`. The app's own origin and port are `APP_PUBLIC_URL` and
`APP_PUBLIC_PORT`. Read every one of them from the environment and never
hardcode a host or a port. Both backing services are already running and
reachable at those variables; do not download, install, compile or start a copy
of either.

Authentication is email and password implemented by the app, with bearer tokens
and hashed passwords. `GET /api/health` returns `200` once the app is ready.
Logs go to stdout.

Two independently tokenised design systems live in one application and are
selected per route segment. The documentation route uses its own ramp, its own
type and its own component namespace; every other route uses the marketing one.
The observable property: a component built for one layer does not pick up the
other layer's values when it is rendered, and no token from one layer resolves
on a surface belonging to the other.

### Object keys, uploads and machine-readable paths

A cover object key is `covers/{article_slug}/{sha256_of_bytes}.{ext}`, for
example
`covers/spreadsheet-to-app-in-an-afternoon/9f2a7c41b0e35d82f6a9c4d17e0b3a58c92d4f61e8a70b3c5d9e2f14a86b07d3.png`.
An attachment object key is `build-requests/{request_id}/{sha256_of_bytes}.{ext}`.

The accepted attachment types are the two common spreadsheet formats and
delimited text, at most 26214400 bytes. The type is decided by reading the
content and never by trusting the extension: a `.csv` name over executable bytes
is rejected as invalid. A build request carries a `prompt` of 1 to 4000
characters, an optional attachment identifier, the `route` it came from, a
`variant` of `inline` or `pinned`, a `locale` and a `client_id`; it is durable
before the response is sent, and the response carries the request identifier and
the next step.

The whole question-and-answer set is retrievable as structured data at
`/api/questions`, ordered by group then position, in addition to being rendered
on `/faqs`. Every documentation page is retrievable as plain structured text at
a deterministic path derived from its own path, and a machine-readable index of
every documentation page exists at the documentation root.

The press digest is paginated by the server. A page request returns that page,
the first page, the last page and the neighbouring pages without the client
having loaded any intermediate page, and the range expander widens the visible
range rather than jumping to a page.

---

## Data model

Seven tables. All timestamps are UTC.

> **Every seeded account uses the password `deku-demo-pw-2026`.** It is
> benchmark fixture data, not a secret. Hash it as normal; the exact literal
> must work at login, and it must be written into `/app/USER_README.md`
> alongside each account so a grader can sign in.

**users** - `id`, `email` unique and case-insensitive, `password_hash`, `role`
one of `author` or `reader`, `created_at`.

**articles** - `id`, `slug` unique, `title`, `standfirst`, `body`, `cover_key`
nullable, `status` one of `draft` or `published`, `featured` boolean,
`published_at` nullable, `author_id` referencing `users`, `tags`, `created_at`,
`updated_at`. `published_at` is non-null exactly when `status` is `published`.
At most one row in the whole table has `featured` true at any time; this must
hold under concurrent requests, not merely in application-level checks, so two
simultaneous requests featuring two different articles must not both succeed.
Exactly one wins, the other is rejected, and a failed attempt leaves no partial
state: never two featured rows and never zero.

**press_items** - `id`, `slug` unique, `title`, `category`, `published_on`
date, `summary_points` holding 3 to 5 entries, `outlet`, `hero_key` nullable,
`status`, `author_id`.

**jobs** - `id`, `slug` unique, `title`, `department`, `location`,
`employment_type`, `description`, `open` boolean, `author_id`. The department
grouping the careers route renders is derived on read, never stored.

**qa_entries** - `id`, `group`, `group_order`, `position`, `question`,
`answer`, `status`, `author_id`. Ordered by `group_order` then `position`.

**build_requests** - `id`, `request_id` unique, `prompt`, `attachment_key`
nullable, `route`, `variant` one of `inline` or `pinned`, `locale`,
`client_id`, `created_at`.

**subscriptions** - `id`, `email` unique, `source`, `locale`, `confirmed`
defaulting to false, `created_at`. Submitting an address that is already
present leaves one row and produces the same response as a new address.

Derived rather than stored: the careers department grouping, the press page
count, every ordering, and every count rendered anywhere on the site.

**Seed data.** Three accounts, all with the password above:
`author@example.com` and `author2@example.com` as `author`,
`reader@example.com` as `reader`.

Three articles, newest first: `agents-reading-your-schema`
(`Agents Reading Your Schema`, `draft`, owned by `author@example.com`, carrying
a cover object); `what-your-warehouse-sheet-already-knows`
(`What Your Warehouse Sheet Already Knows`, `published`, owned by
`author2@example.com`); `spreadsheet-to-app-in-an-afternoon`
(`Spreadsheet To An App In An Afternoon`, `published`, `featured` true, owned by
`author@example.com`).

Three press items, all published, each with exactly three `summary_points`:
`slate-raises-a-series-b` (`Slate Raises A Series B`, category `Funding`,
`2026-03-04`, outlet `The Ledger`); `warehouses-run-on-slate`
(`Warehouses Run On Slate`, `Customers`, `2026-02-18`, `Field Report`);
`slate-opens-the-agent-gateway` (`Slate Opens The Agent Gateway`, `Product`,
`2026-01-27`, `Terminal Weekly`).

Three job openings: `staff-frontend-engineer` (`Staff Frontend Engineer`,
`Engineering`, `Remote, EU`, `Full-time`, open); `technical-writer`
(`Technical Writer`, `Documentation`, `Lisbon`, `Full-time`, open);
`field-marketing-lead` (`Field Marketing Lead`, `Marketing`, `New York`,
`Full-time`, closed).

Three question entries: in group `Getting started` at `group_order` 1,
`What does Slate build from a spreadsheet?` at position 1 and
`Do I need to know how to code?` at position 2; in group `Agents and data` at
`group_order` 2, `Which coding agents can drive Slate?` at position 1.

One subscription: `subscriber@example.com`, `confirmed` false.

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
| `GET /api/articles` | none | a top-level JSON array of published articles, newest first |
| `GET /api/articles/{slug}` | none | one article; a draft answers its author only |
| `POST /api/articles` | `{ title, standfirst, body, tags, status }` | the created article |
| `PATCH /api/articles/{slug}` | any of `{ title, standfirst, body, tags, status, featured }` | the updated article |
| `POST /api/articles/{slug}/cover` | the image bytes | `{ cover_key }` |
| `GET /api/covers/{slug}` | none | the cover bytes; a draft's cover answers its author only |
| `GET /api/studio/articles` | none | the signed-in author's own articles, drafts included |
| `GET /api/docs` | none | the machine-readable index of every documentation page |
| `GET /api/docs/{page}.txt` | none | that documentation page as plain text |
| `GET /api/press` | `page` | `{ items, page, pages }` |
| `GET /api/jobs` | none | a top-level JSON array of open jobs grouped by department |
| `GET /api/jobs/{slug}` | none | one job, open or closed |
| `GET /api/questions` | none | a top-level JSON array ordered by group then position |
| `POST /api/site/attachments` | `{ filename, content_type, size }` | `{ attachment_id, upload_url, expires_in }` |
| `POST /api/site/build-requests` | `{ prompt, attachment_id, route, variant, locale, client_id }` | `{ request_id, next }` |
| `POST /api/site/subscriptions` | `{ email, source, locale }` | `{ pending: true }` |
| `GET /api/health` | none | `200` |

Field names are exact. A successful call returns the named resource or shape. An
invalid or unauthorized call is rejected as a client error, never a `5xx` and
never a silent success. Bearer auth is required on everything except login,
signup, health, the public collection reads, the attachment grant, the build
request and the subscription.

### No mocks

An in-memory list of articles, image bytes written to the app container's
filesystem, a `cover_key` recorded for an object that was never written, an
attachment the app proxied and stored itself, a hardcoded upload response the
app returns to itself: each of these is a contract violation however good the
interface looks. PostgreSQL and MinIO are the fact. The app's UI and its own
tables can only reflect what lives in the provider, never substitute for it.

---

## Front-end specification

This section carries the measured visual specification. Every value here is a
contract value: it was measured, not chosen, and the numbers belong in the
build.

### Information architecture

Twelve paths. Seven are full routes: `/` (document title
`AI App Builder: Turn Spreadsheets into Business Apps`), `/byoa`
(`Bring your own agent`), `/docs` (`Slate Documentation`), `/faqs`
(`Slate FAQ: Building Custom Apps and AI Agents`), `/blog` (`The Column`),
`/news` (`Slate News`), `/jobs` (`Join us`). Five resolve to the shared
not-found surface, document title `Page Not Found`: `/e/`, `/i/`, `/s/`, `/va`
and `/va/`. Those four short paths are parametric prefixes, most likely an
embed, an invitation, a share and a verification link; build them as segment
prefixes taking a required trailing identifier and render the not-found surface
when it is absent.

The primary navigation carries five items: `Product` (a menu), `Enterprise`,
`Customers`, `Resources` (a menu) and `Pricing`. Two open overlay panels. The
right cluster differs by route family: on home and agent it is `Log in`,
`Contact sales`, `Get started`; on editorial, answers, careers and press it is a
search affordance, `Log in`, `Contact sales`, `Start for free`. The
documentation portal replaces the whole bar.

The footer is the sitemap and names destinations the capture did not reach.
Build them as routes with a skeleton, never as dead links. Product: Platform,
Bring your own agent. Apps: Inventory, Logistics, Procurement, Vendor
Management, Warehouse Management, Project Management, Portals, Dashboards, CRM,
Work Orders, Field Sales, All Apps. Solutions: Business, Enterprise, Supply
Chain, Manufacturing, Retail, Real Estate, Hospitality, Professional Services.
Resources: Templates, Customer Stories, Docs, Help Center, Community, Events,
News, AI in Operations Report. Company: Pricing, Careers, Blog, Research, Trust
Center, Compare, FAQs, Integrations, Changelog, Classic. Legal and meta: Status,
Terms, Privacy, OSS, Sitemap, LLMS, Contact Us.

### The two-layer reality

Two complete design systems ship in one application, and neither is a
variation of the other. Layer A, the marketing layer, serves home, agent, editorial, press, answers and
careers. It is driven from a root custom-property set with `--color-*`,
`--text-*`, `--radius-*`, `--spacing`, `--breakpoint-*` and `--ease-*` families,
and its root class carries a font-module marker plus `antialiased`. Layer B, the
documentation layer, serves `/docs` only, carries its own root class `light`,
its own accent ramp `--accent-1` to `--accent-12`, a twelve-step perceptual grey
ramp `--gray-1` to `--gray-12`, and its own component prefix `dsp-`. They share
no token namespace, no type scale and no colour model.

### Colour, Layer A: the warm neutral ramp

| Token | Value | Role |
|---|---|---|
| `--color-neutral-warm-50` | near-white neutral | page tint on light sections |
| `--color-neutral-warm-100` | near-white neutral | hover fill on menu rows |
| `--color-neutral-warm-200` | near-white neutral | card fill, divider ground |
| `--color-neutral-warm-300` | near-white neutral | hairline on light |
| `--color-neutral-warm-400` | light warm neutral | secondary text on dark |
| `--color-neutral-warm-500` | light warm neutral | disabled text, bound to `--color-disabled` |
| `--color-neutral-warm-600` | mid neutral | tertiary text |
| `--color-neutral-warm-700` | deep neutral | body text, the single most used colour on the site |
| `--color-neutral-warm-800` | deep neutral | raised dark surface |
| `--color-neutral-warm-900` | near-black neutral | dark section ground |
| `--color-neutral-warm-950` | near-black neutral | deepest ground, bound to `--color-primary` |

Semantic aliases, which components reference: `--color-primary` near-black neutral light
and `#fff` dark; `--color-secondary` mid neutral light and near-white neutral dark;
`--color-tertiary` mid neutral light and light neutral dark; `--color-disabled`
light warm neutral, not declared dark; `--color-accent` mid, vivid teal light and light, soft teal
dark.

The dark surface ramp is declared separately and is not the light ramp inverted:
`--color-neutrals-opaque-dark-50` near-black neutral, `-100` near-black neutral, `-200` deep neutral,
`-300` deep neutral, `-400` deep neutral, `-500` mid neutral, `-600` mid neutral, `-700`
light neutral, `-800` near-white neutral, `-900` `#fff`.

### Colour, Layer A: accent and the chromatic set

| Token | Value | Where |
|---|---|---|
| `--color-aqua-50` | near-white cool neutral | declared, unused |
| `--color-aqua-100` | near-white cool neutral | tag fill |
| `--color-aqua-200` | near-white, muted teal | the `Hiring` badge in the footer |
| `--color-aqua-300` | near-white, soft teal | declared, unused |
| `--color-aqua-400` | light, soft teal | declared, unused |
| `--color-aqua-500` | mid, vivid teal | the accent proper |
| `--color-aqua-600` | mid, vivid teal | accent pressed |
| `--color-aqua-700` | deep, soft teal | accent on light, text-safe |
| `--color-aqua-900` | near-black cool neutral | accent ground |

The remaining chromatic ramps are declared and appear only as fills in the app
tile grid. Carry them. Green: near-white neutral, mid, vivid teal, mid, vivid teal, near-black, muted green. Red:
near-white warm neutral, near-white warm neutral, light, vivid red, mid, vivid red, mid, vivid red, deep, soft red, near-black, muted red.
Yellow: near-white warm neutral, near-white warm neutral, mid, vivid amber, mid, vivid orange, near-black, muted orange, near-black warm neutral.
Orange: light, vivid orange, mid, vivid orange. Blue: near-white neutral, near-white cool neutral, near-white, soft blue, deep, muted blue,
deep cool neutral. Amethyst: near-white cool neutral, deep cool neutral. Pear: near-white warm neutral, light, vivid amber. Pine:
near-white neutral. Beige: near-white neutral, near-white warm neutral, near-white warm neutral.

`--color-pear-100` near-white warm neutral is the full-bleed ground of the careers hero and is
the only coloured page background on the site.

### Colour, Layer A: the alpha ladders

Two nine-step ladders in constant use for hairlines, hover fills and scrims. On
light, `--color-neutrals-alpha-light-*`: 50 `#00000005`, 100 `#0000000f`, 200
`#0000001a`, 300 `#00000029`, 400 `#0000003d`, 500 `#0006`, 600 `#000000a3`,
700 `#000000b8`, 800 `#000000e0`, 900 `#000000f5`. On dark,
`--color-neutrals-alpha-dark-*`: 50 `#ffffff0d`, 100 `#ffffff1a`, 200
`#ffffff29`, 300 `#ffffff3d`, 400 `#ffffff5c`, 500 `#ffffff80`, 600 `#ffffffa8`,
700 `#ffffffbf`, 800 `#ffffffe0`, 900 `#fffffff5`.

`#0000001a` is the outlined-pill border and the default hairline. `#0000000f` is
the resting fill of the two ghost buttons in the hero showcase.

### Colour, Layer B: the documentation ramps

Twelve-step grey: near-white neutral, near-white neutral, near-white neutral, near-white neutral, near-white neutral,
near-white neutral, near-white neutral, `#bbb`, light neutral, mid neutral, mid neutral, deep neutral.
Twelve-step accent: near-white neutral, near-white cool neutral, near-white cool neutral, near-white, muted teal, light, muted teal,
light, soft teal, light, soft teal, mid, vivid teal, mid, vivid teal, mid, vivid teal, deep, soft teal, deep, muted teal.
Step 9 of the accent ramp is mid, vivid teal, the same value as `--color-accent` in
Layer A, and it is the only token the two systems share. Layer B also declares
`--color-background` `rgba(247, 247, 248, 1)`, `--color-border-default`
`rgba(229, 231, 235, 1)` and `--color-body` deep neutral.

### Type families

| Role | Family | Weights | Licence |
|---|---|---|---|
| Display, headings, interface | Booton VF | variable 300 to 800 | commercial |
| Editorial pull quotes | Affairs | 400 | commercial |
| Metadata, terminal theatre | Maxeville Mono | 800 | commercial |
| Documentation body | Inter | 400, 500, 600 | open |
| Documentation code | DM Mono | 500 | open |

All five are served with `font-display: swap`. Fallback stacks, normative:
display `"Booton VF", ui-sans-serif, system-ui, sans-serif`; editorial
`"Affairs", Georgia, "Times New Roman", serif`; mono `"Maxeville Mono",
ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace`.

The display family is used at non-standard weights: `--font-weight-normal` is
`450` rather than 400, and `575` carries emphasis where a static family would
use 600. A variable family is a requirement, not a preference. A substituted
family with four fixed weights will read subtly wrong on every surface at once.

### Type scale, Layer A

`--text-xs` `0.75rem`/`1.3`/`-0.12px`; `--text-sm` `0.875rem`/`1.3`/`-0.14px`;
`--text-base` `1rem`/`calc(1.5/1)`; `--text-md` `1rem`/`1.4`/`-0.16px`;
`--text-lg` `1.25rem`/`1.3`/`-0.2px`; `--text-xl` `1.375rem`/`1.3`/`-0.22px`;
`--text-2xl` `1.875rem`/`1.2`/`-0.3px`; `--text-3xl`
`1.875rem`/`calc(2.25/1.875)`; `--text-4xl` `2.25rem`/`calc(2.5/2.25)`;
`--text-5xl` `3rem`/`1`; `--text-6xl` `3.75rem`/`1`; `--text-7xl` `4.5rem`/`1`;
`--text-9xl` `8rem`/`1`.

The pullout scale, every step carrying a letter-spacing of exactly one percent
of the size, negative: `--text-pullout-sm` `18px`/`1.4`/`-0.18px`;
`--text-pullout-md` `24px`/`1.3`/`-0.24px`; `--text-pullout-lg`
`28px`/`1.3`/`-0.28px`; `--text-pullout-xl` `36px`/`1.2`/`-0.36px`;
`--text-pullout-2xl` `44px`/`1.2`/`-0.44px`. Any new display size follows the
one-percent rule.

### The rendered scale

The ten most common size, weight and line-height triples, which a rebuild should
reproduce in roughly this order: `16px`/450/`24px` (8097), `14px`/450/`18.2px`
(7392), `16px`/400/`24px` (1847), `16px`/450/`28px` (979), `16px`/400/`20px`
(532), `14px`/600/`18.2px` (489), `16px`/600/`28px` (414), `14px`/400/`17.5px`
(272), `16px`/575/`24px` (261), `48px`/575/`48px` (71), `36px`/575/`40px` (75),
`30px`/575/`36px` (76). The largest headline rendered anywhere is `48px`; the
enormous declared steps are unused.

### Spacing, radius and containers

`--spacing` is `0.25rem` and every spacing utility is a multiple of it. Radius
tokens: `--radius-sm` `0.25rem`, `--radius-md` `0.375rem`, `--radius-lg`
`0.5rem`, `--radius-xl` `0.75rem`, `--radius-2xl` `1rem`, `--radius-3xl`
`1.5rem`, `--radius-4xl` `2rem`.

Build to the measured radii, which differ from the tokens: `3.35544e+07px`, a
fully rounded pill, is the most common radius on the site at 582 occurrences and
is the house shape; then `6px` at 435, `8px` at 304, `16px` at 47, `12px` at 46,
`50%` at 42 for circular avatars and dots, `14px` at 24, `10px` at 21, `24px` at
12, `9px` at 9, `26px` at 3 for the terminal input, `32px` at 3 for the
pre-footer frame, `7px` at 3, `4px` at 3.

Containers `--container-xs` `20rem` through `--container-7xl` `80rem`, in the
steps 20, 24, 28, 32, 36, 42, 48, 56, 64, 72, 80. The documentation layer
declares its own `--content-width` of `640px`. `--site-nav-height` is `68px` and
every sticky element is positioned against it.

### Duration and easing tokens

Eight easing tokens are declared and each carries a character rather than a
curve. `--default-transition-timing-function` and `--ease-in-out` both start and
finish gently and hurry through the middle, and that pairing is the site's
baseline. `--ease-in` leaves slowly and arrives abruptly. `--ease-out` leaves at
once and arrives slowly. `--ease-slide` is the most emphatic of the set, almost
still at both ends and very fast between them, and it carries the full-height
slides. `--ease-shift` puts almost all of its movement at the start and decays
into its resting place, and it carries menu panel arrivals and dropdown
expansions. `--ease-collapse` is gentler than the baseline at both ends and
carries collapsing regions. `--default-transition-duration` is short enough that
the interface reads as answering rather than arranging itself; the exact values
are the builder's, so long as one family governs the whole site.

### Iconography

The wordmark is a text mark in the display family. Interface icons are drawn on
a `0 0 24 24` box at stroke `1.5`; illustrative icons at stroke `1.75`. The
answers route carries one large mark filled with the accent. Footer social icons
sit in a row at the foot of every route. The app tile grid uses a set of glyphs,
one per tile, filled from the chromatic ramps above. Rules: one stroke weight per
family, never mix, and never scale a stroke with the box.

### Global chrome

The header is `68px` tall and sticky. The action pills are a filled
`Get started` and an outlined `Contact sales`, with `Log in` as a bare text
button; on the reading routes the filled pill reads `Start for free`. At `390px`
the centre navigation collapses and the row becomes wordmark, a filled `Sign up`
pill, a bare `Log in`, and a three-line menu glyph; note that the mobile primary
action is `Sign up`, a different word from the desktop cluster on the same route.

The persistent prompt composer is the most important component on the site: a
rounded card at radius `14px` carrying a single-line text input with the
placeholder `Describe what you want to build...` at `--text-lg`, an attachment
row beneath it with a paperclip glyph and the label `Upload spreadsheet` at
`--text-md`, and a circular submit button on the right at `40px` on ground
near-black neutral with an upward arrow glyph in `#fff`. Card treatment, measured:
`backdrop-filter: blur(12px)`, a five-slot shadow stack whose visible layers are
`rgba(0, 0, 0, 0.06) 0px 0px 0px 1px` and `rgba(0, 0, 0, 0.01) 0px 106px 43px
0px`, and a semi-transparent white fill so that whatever passes behind it is
visible and blurred. `blur(12px)` is the house glass value, measured 54 times.

The navigation overlay panels are children of their trigger, positioned
`absolute top-full left-0` inside a container carrying `perspective: 2000px`.
Panel motion is four named keyframes at `0.25s ease`: `enterFromLeft`,
`enterFromRight`, `exitToLeft`, `exitToRight`, each translating `200px`
horizontally while crossing opacity, which is what makes moving between two open
menu items slide the outgoing panel one way and the incoming panel the other.
Two further keyframes handle the panel itself: `scaleIn` at `0.2s ease` from
`rotateX(-10deg) scale(.9)` to rest, and `scaleOut` at `0.2s ease` to
`rotateX(-10deg) scale(.95)`. Menu row hover is transparent to
`rgb(245, 245, 242)` for a panel row and transparent to `rgba(0, 0, 0, 0.06)`
for a header-level trigger; on the agent and press routes the same triggers
hover to `oklab(0.999994 0.0000455678 0.0000200868 / 0.3)`, white at thirty
percent, because those routes run dark.

The route progress bar is `3px` tall in `rgba(12, 189, 195, 1)` with a glow of
`0 0 10px rgba(12, 189, 195, 1), 0 0 5px rgba(12, 189, 195, 1)` at stack order
`99999`, with an `18px` spinner at border `2px` positioned `top: 15px, right:
15px` on a `400ms` period. This is the only place the accent appears at full
strength on a light ground.

The pre-footer is a full-bleed photographic band at radius `32px` on its outer
frame. The footer carries the sitemap of Section 2.3 above. The consent bar
gates analytics collection and never blocks rendering.

### Motion language

The house curves are the eight `--ease-*` tokens above, and the default
transition is the site's baseline everywhere. Named keyframe animations cover the panel set, the marquee, the
scene switcher, the typing caret and the entrance observer. Runtime animations
measured on the site sit at the same duration. Reduced motion: under
`prefers-reduced-motion` every scroll-driven value, every parallax offset and
every keyframe resolves to its end state immediately, and nothing animates.

### Scroll system

Scroll-driven values are computed from scroll position, not from time. Measured
page lengths at desktop: the answers route is the longest surface in the capture
at 22404 device pixels, and the not-found surface is the shortest at 172 device
pixels desktop, 380 tablet, 687 mobile. The home route, the careers route and
the agent route each carry scroll-driven values; the documentation, answers,
editorial and press routes carry none. The documentation route clips its sidebar
with a soft fade at top and bottom so entries dissolve as they scroll past
rather than being sliced off.

### The hero showcase

Composed in layers: a ground, a device composite, an interface card, and two
ghost buttons resting at `#0000000f`. Five scenes cycle. The interface card
treatment carries the house glass value. Scene switching is driven by an index
and each scene is labelled. One tile is scrubbed against scroll position. Inside
the composite a pointer-driven parallax offsets the layers. On mobile the hero
substitutes a single static composition. What cannot be recovered from the
capture is the source artwork; Section 36 of the supplied specification gives
the substitution recipe and generated geometry stands in.

### The agent terminal theatre

A frame at radius `26px` on a dark ground with the component prefix `at-`. The
line grammar is a prompt sigil, a command, then output. A typing animation
reveals each line with a blinking caret. Three windows sit side by side. A
status row runs beneath them naming the connected agents `Aria`, `Nomad`,
`Quill` and `Forge` and the two models `Ember` and `Onyx`. An ambient ground
sits behind the frame. An integration panel lists the endpoints the gateway
exposes.

### Route compositions

**Home**, in order: hero, trust marquee of twelve customer wordmarks running as
two tracks in opposite directions at different speeds with both edges softly
faded, the
connected-apps section, the card carousel, the three-step disclosure, the device
composition, the integration chip field, the dark security band, the app tile
grid, the testimonial carousel, and the founder quote from `Ilse Varga`.

**Bring your own agent**: a dark ground and an inverted chrome, the headline
treatment, the composite mark, the six-item platform grid, and the endpoint
block.

**Documentation portal**: its own header, a sidebar on frosted glass with a
tree, a landing grid, the machine-readable index, and file-type glyphs on
`0 0 24 24` at stroke `1.5` for an arrow in a circle, a three-panel layout, a
table and a four-square grid. Hovering a sidebar row turns its text, its rule
and its arrow to the accent at once, and a row whose name overflows slides
sideways on hover so the end can be read. A visually hidden instruction
announces the index and the plain-text path.

**Questions and answers**: a pair layout of question and answer, grouped under
headings, with the large accent cube. It is the longest route because it is
written for the technical buyer.

**Editorial index**: the title `The Column` at `48px`, a one-line standfirst,
the inline subscribe form (a single rounded field at radius `3.35544e+07px`,
border `#0000001a`, placeholder `Enter email address`, a filled `Subscribe`
button inset on the right, total width `362px` at desktop), the featured article
as a large media card at `9px` radius across roughly half the measure, then
article rows each with a `9px` thumbnail at `176px`, a title at `--text-lg`
weight 600 and a standfirst in `--color-secondary`, hairline between rows, row
hover from `rgba(0, 0, 0, 0.06)` to `rgba(0, 0, 0, 0.1)`.

**Press digest**: a dark hero carrying the lead story over a photograph, a
horizontal strip of five further headlines, a vertical list of items each with a
title at `--text-lg`, a category pill on a dark ground, a date written out in
full including the weekday, and three to five one-line summary bullets, then
pagination reading `Previous`, `1`, `2`, `3`, an ellipsis button, `29`, `30`,
`31`, `Next`. The ellipsis is a button that expands the range, not a label.

**Careers**: the near-white warm neutral ground full bleed behind the header, a centred
two-line headline at `48px`, a ghost pill `See open roles` with a downward
arrow, the parallax field of eight photographs sized `602px`, `527px`, `433px`,
`428px`, `371px`, `171px`, `158px` and `152px` (the spread is what produces the
depth, do not normalise it), a mission statement at `--text-3xl`, three columns
`Global Impact`, `Design Culture` and `Great Backers`, a large retreat
photograph with a caption under `Make every day count for something`, the
`Our values` tabs `Collaboration`, `Ownership` and `Velocity` swapping a
paragraph beside them on the house `0.15s`, three serif testimonials, a
`Slate in a snapshot` row of four statistics each a label at `--text-lg` over a
value, the dark `Open Roles` block on near-black neutral with white text and a `48px`
heading, and a closing invitation.

**Not found**: header, a short message block, footer. The measured heights are
scroll distances, not content heights, which is why the footer must sit at the
bottom of the viewport on any route shorter than it. It uses the reading-route
header cluster.

### Module and component architecture

Four layers: tokens, primitives, composites, routes. The component inventory
covers the header, the action pills, the composer, the overlay panels, the
progress bar, the pre-footer, the footer, the consent bar, the marquee, the
carousel, the disclosure, the tile grid, the terminal frame, the sidebar tree,
the pair layout, the article row, the press item, the parallax field, the values
tabs and the statistics row. Naming is consistent within a layer. An entrance
observer reveals sections as they enter the viewport and is the only shared
scroll listener. State is local to a route except the composer's value and the
consent state.

### Responsive behaviour

The captured widths are `390px`, `768px` and `1440px`. Declared breakpoints
follow the `--breakpoint-*` family. Layout changes by route: the home hero
substitutes on mobile, the editorial index collapses the featured card above the
rows, the careers parallax reduces its count, the documentation sidebar becomes
a drawer, and the press strip becomes a scroller. The page-length inversion is
real and expected: the not-found surface is longest at mobile and shortest at
desktop, because the footer anchors to the viewport. Touch targets are
comfortably sized and every hover affordance has a touch equivalent.

### Accessibility

The reference is already right on landmark structure, heading order and the
hidden documentation instruction. The build must do better on focus visibility,
on labels for icon-only controls, and on colour never being the only carrier of
meaning. Keyboard order follows the visual order on every route. Motion is
gated on `prefers-reduced-motion` everywhere.

### Performance

The reference shipped more than the budget allows. Normative budgets: the
application shell is small enough to paint quickly on a mid-range device, the
scroll budget keeps every scroll-driven value on one shared listener, and
loading order puts the shell and the composer ahead of imagery. Under pressure,
drop in this order: the ambient ground, the parallax field, the marquee, the
scene switcher, and only then any content.

### Zero-asset substitution

No photographic or vector asset from the reference ships. The asset manifest is
replaced as follows: the hero scenes are generated geometry; product screenshots
and abstract covers are generated; photographs are solid or gradient fills at
the measured sizes with the measured radii; generated geometry uses the
chromatic ramps; the twelve wordmarks are set in the display family; the
typefaces are substituted per the recipe above; grain and texture are generated;
video is replaced by a static frame.

### Named animations

Every keyframe the site declares, by name and by what it does. Durations and
easing curves are the builder's to choose; the character and the uniformity are
not. Under `prefers-reduced-motion` every one of these resolves to its end state
at once.

| Name | What it does |
|---|---|
| `accordionDown` | an accordion panel grows from nothing to its content height |
| `accordionUp` | the same panel collapses back to nothing |
| `collapsible-open` | a collapsible region fades in as it grows to its content height |
| `collapsible-closed` | the region fades out as it collapses |
| `slide-up-and-fade` | the element rises a hair as it fades in |
| `slide-down-and-fade` | the element settles a hair downward as it fades in |
| `slide-left-and-fade` | the element drifts left as it fades in |
| `slide-right-and-fade` | the element drifts right as it fades in |
| `slide-up` | the element travels its own full height upward and leaves |
| `slide-down` | the element arrives from above its own height |
| `spin` | one full rotation, repeating without pause, for the loading spinner |
| `buildShimmer` | a highlight sweeps left to right across a building surface, repeating |
| `shine` | a skewed highlight crosses a surface and fades at both ends |
| `thumb-rock` | the scrubbed tile rocks about its own centre |
| `dropdown-expand` | a dropdown opens with almost all of its movement at the start. Not defined beyond its binding |
| `overlay-show` | a scrim fades up under an opened panel. Not defined beyond its binding |
| `pulse` | a surface drops to half opacity at the midpoint and returns, repeating |
| `dsp-sidebar-marquee` | an overlong documentation sidebar row slides sideways on hover, on a `transform` driven by a `--marquee-translate` custom property, so its end can be read |
| `enterFromLeft`, `enterFromRight` | a navigation panel arrives horizontally while crossing opacity |
| `exitToLeft`, `exitToRight` | the outgoing panel leaves the other way, which is why four exist |
| `scaleIn` | the panel tips forward out of its perspective space and settles |
| `scaleOut` | the panel tips back and shrinks slightly as it goes |
| `at-in` | one terminal line appears, rising a hair as it fades in |
| `at-blink` | the terminal caret holds, then blanks, repeating without pause |

### Transitioned properties

The house transition applies to `color`, `background-color`, `border-color`,
`fill`, `stroke`, `opacity`, `box-shadow` and `filter`. A second and faster
transition, whose timing function is not declared, applies to `border-color` and
`background-color` alone on hover. `transform`, `translate`, `scale` and
`rotate` share the house duration, and so do `grid-template-columns` and
`opacity` on the disclosure, which is the most frequently transitioned pair on
the site. Every transition uses one character and one duration family, with no
per-component exception.

### Runtime animation bindings

The agent terminal theatre animates each transcript line in turn. `at-in` is
bound to `div.at-welcome`, `div.at-user`, `div.at-tool`, `div.at-out`,
`div.at-ok` and `div.at-say`, each playing once at a linear rate and holding its
end state. `at-blink` is bound to `span.at-caret` alone and repeats at a linear
rate without pause. The
home route's scrubbed tile binds `thumb-rock` to a transform driven by scroll
position. On the narrow width the hero substitutes a three-state step loader
whose only animated property is a transform.

The pointer-driven parallax inside the hero composite offsets three elements:
`div.at-welcome` moves on `transform` and `background-image`, `div.at-user` on
`transform` alone, and `div.at-say` on `transform` and only at the narrow
width.

### Iconography geometry

Interface icons are drawn on a 24-unit canvas at stroke `1.5`; illustrative icons
on the same canvas at stroke `1.75`. Two rendered sizes dominate, `16px` and
`20px`, both from the 24-unit canvas. The captured set includes a compact chevron
pointing down, a paired chevron pointing up and down for a sort control, a
four-square grid, a three-panel layout, a table, an arrow in a circle, and a
database cylinder drawn as an ellipse cap over a body. Each icon carries
alternative text, or is marked decorative where a neighbouring label already
names it.

### The documentation sidebar tree

The captured tree, in order: Getting Started, Building Apps, Data Sources
expanded to show the built-in tables, the guide to large tables, the warehouse
connector and getting started with each, Layouts, Components, Actions,
Workflows, AI, Users and Permissions, Publishing, Administration, and the API
reference. Each row carries a leading glyph naming the kind of page.

### Captured widths

| Width | Height | What it stands for |
|---|---|---|
| `1440px` | `900px` | desktop |
| `990px` | `800px` | the awkward middle, a tablet |
| `390px` | `844px` | a current phone |

The layout holds at every width between these, not only at them.

### Performance budget

Normative. The home route ships at most `180` kilobytes of compressed JavaScript.
At most two font families load on first render, each subsetted, compressed and
preloaded. Streamed component payloads are the largest single cost in the
reference and must come down. No analytics call blocks rendering, and the consent
state gates collection. Under pressure, drop in this order: the ambient ground,
the parallax field, the marquee, the scene switcher, and only then any content.

### Launch surface

These ship with the site, not after it.

- A **privacy** page and a **terms** page, both reachable from the footer strip
  and both rendering real content rather than a placeholder.
- A **sitemap** at a stable path, listing every public route, alongside a robots
  file that points at it.
- **Alternative text** on every content image, and an explicit decorative marking
  on images a neighbouring label already describes.
- A **page view** record for every public route, written to the site's own first
  party collection point, gated on the consent state, with a rotating first party
  identifier and no third party tag.

### Copy deck

Pinned strings. Where the supplied specification used a bracketed token, the
value below is the one this product uses, and it is used consistently everywhere.

**Identity.** The product is `Slate`; its platform name is `SlateOS`; published
apps are served under `slate.app`. The four coding agents named on the agent
route are `Aria`, `Nomad`, `Quill` and `Forge`. The two models named inside the
terminal are `Ember` and `Onyx`. The three model vendors named on the answers
route are `Northwind`, `Cascade` and `Meridian`. The chief executive quoted at
the close of the home route is `Ilse Varga`.

**Six customer companies**, used in the testimonial carousel: `Halden Materials`,
`Wrenfield Group`, `Alder Bay Realty`, `Northgate Media`, `Pike & Rowe`,
`Fenwick Pay`. **Six named people**, one per testimonial: `Rae Alderton`,
`Nils Brandt`, `Imani Sole`, `Piet Coenen`, `Sara Vance`, `Tom Ashby`. **Three
staff quoted on the careers route**: `Mira Okafor`, `Jonas Vella`,
`Nia Truscott`. **Three investors** named on the careers route: `Ridgeline`,
`Foundry Lane`, `Beacon Hill`.

**Chrome.** The consent bar reads `We use cookies to improve our service.` with
`Learn More`, `No thanks` and `Continue`. The footer strip reads `Status`,
`Terms`, `Privacy`, `OSS`, `Sitemap`, `LLMS`, `Contact Us`, and the careers link
carries a `Hiring` badge.

**Home.** The headline is `Turn your spreadsheets into` over
`apps that run your business`. The subhead is `Slate understands how you work,
then builds connected apps for your team, your customers, and every part of your
operation. No code required.` The integration chip field names `Google Sheets`,
`Excel`, `Airtable`, `QuickBooks`, `Salesforce`, `PostgreSQL`, `Snowflake` and
`Slack`. The dark security band carries the badges `CCPA`, `SOC 2`, `GDPR` and
`AES 256`. The device composition lists data rows for `Employees`,
`Expense Reports`, `IT Assets`, `Meeting Rooms` and `Policies`, and workflow rows
for `Quarterly Policy Acknowledgment`, `Expense Approval Reminder` and
`New Hire Onboarding`.

**Agent route.** The headline is `Build in your agent.` in a muted tone over
`Deploy, manage, and collaborate on Slate.` in white. The subhead reads
`Build in Aria, Nomad, Quill, etc.` over
`Slate adds hosting, data, workflows, auth and more.` The two buttons read
`Upgrade to Team` and `How to connect`.

The first terminal transcript runs, in order: a welcome line
`Welcome to Aria Code` with `cwd: ~/acme/inventory` and
`via Slate, you, org Acme`; a user line
`Look at this spreadsheet and create an app for my team to update it in the
field. Send me a nightly report.`; a tool line `Read local file`
`(inventory.data)`; an output line `1,248 rows, SKU, on hand, location, notes`; a
tool line `Build and deploy app` `(Inventory)`; an output line
`inventory.slate.app`; a tool line `Build and start workflow`
`(Nightly inventory report)`; an `at-out` line `inventory.slate.app`; an output
line `Scheduled 8:00pm, running`; an
acknowledgement `App, workflow, and data - done in one go`; outputs
`App, inventory.slate.app`, `Workflow, nightly report is on` and
`Live data is in context - ask about it anytime`; and a spoken line
`Built the app, started the workflow, and I have full context of this inventory
now.` The frame's composer reads `Ask Aria to work on a task...` and its status
row reads `Aria Max, Ember` beside `~/acme/inventory`.

The second heading is `Build anywhere.` over `Own it together.`, with the body
`Your agent is replaceable. Your software is not. Slate keeps every app, table,
permission, and workflow in one shared system.` The frame labels read
`Alex builds in Nomad` and `Sam continues in Quill`.

The six-item platform grid is headed `Batteries included platform`:
`Hosting and storage`, `The app is not on someone's machine.`; `Database`,
`Shared, live business data.`; `Code storage`, `No repository required.`;
`Team permissions`, `Keep apps private to the company.`; `Workflows`,
`Automations live next to the apps.`; `Edit in Slate`,
`Lose the agent, keep the software.`

The three-part block `Keep what makes your agent yours.` carries `Subscription`,
`Tokens run on the Aria, Nomad, or Quill plan you already pay for. That is the
most immediate reason to bring your own agent.`; `Context`, `Your agent already
knows your files and chat. Slate joins that conversation.`; and `Capability`,
`Keep search, files, and other connectors. Add Slate's apps, data, and
workflows.`

The endpoint block is headed `One endpoint. More ways to work.` and lists
`Ship an app on Aria`, `Bring your Nomad tools and context to Slate`,
`Ask Quill about your business`, and `Use Forge to schedule a workflow`.

**Answers route.** The group headings, in order, are `Slate Overview`,
`Data & Scalability`, `Slate AI`, `AI Agents`, `AI Agent for Invoice
Processing`, and `AI Agent for Resume Screening`. Representative questions the
set must answer: `What's the difference between using a Slate built-in data
source vs. external data sources?`; `How many rows of data can Slate handle?`,
answered with the ten million row ceiling large tables carry;
`What are Slate Workflows?`, answered in terms of triggers and actions;
`What models does Slate AI leverage?`, answered with `Northwind`, `Cascade` and
`Meridian`; and `How secure are Slate AI agents?`, answered by inheriting the
same security framework as the rest of the product.

**Careers route.** The eyebrow reads `Unleash your genius`. The three columns are
`Global Impact`, `Design Culture` and `Great Backers`, the last reading
`We're funded by Ridgeline, Foundry Lane, and Beacon Hill, and our angels include
the people who built the tools you use every day.` The values tabs are
`Collaboration`, `Ownership` and `Velocity`. The location line reads
`We are flexibly remote, with Americas and Western European time zones
preferred.` The staff testimonials include
`There is nothing better than working on a revolutionary product driven by an
incredibly relevant mission.` and `The drive to push boundaries, experiment, and
fail-forward is something I've never experienced to this degree anywhere else.`

**Testimonials.** Representative quotes:
`I didn't expect to be the one building an app - but Slate's new AI capabilities
made it that simple.`; `When we found Slate, we discovered it was so easy to just
take a spreadsheet and create a really workable app.`; `We have a tool that we
use for quarterly planning. It's great visually, not so much from a data
perspective. Slate fixed that.`; and `SlateOS is incredible. The speed and
accuracy with which it turns ideas into functional apps is remarkable.`

### Asset substitution

No photograph, video or vector from the reference ships. Each is replaced:

- The three from-spreadsheet motion pieces, `upload`, `understands` and
  `put-to-work`, and the responsive-devices piece, are each replaced by a static
  poster image built from generated geometry. No video element ships.
- The hero building scene is generated: a five-storey cutaway drawn as flat
  geometry with floor slabs and party walls; small two-tone occupants at desks
  and in aisles; and three parallax planes for exterior, interior and props, so
  the composite has real depth.
- Product screenshots and abstract covers are generated at the measured sizes and
  radii.
- The twelve marquee wordmarks are set in the display family.
- Grain and texture are generated rather than sampled.

### Evidence gaps

Inferred rather than measured: the purpose of the four parametric prefixes, and
the product behind the site. Measured but incomplete: the chromatic ramps that
appear on no captured surface, and the type steps above `48px`. Substitutions
made at authoring time: the brand name, the two renamed class prefixes `dsp-`
and `at-`, and every asset. Three classes of real named third party were replaced
with invented ones and are recorded as such: three model vendors, six customer
companies with six named people, and three investors. What is measured and can be trusted: the palette,
the type scale, the radii, the easing tokens, the page lengths, the breakpoints
and the copy strings pinned above.

---

## Definition of done

A visitor can read the pitch, check the answers, describe the app they want and
attach a spreadsheet, and have that request filed with a request identifier
returned. An author can publish an article with a cover image and see it appear
on the editorial index, and exactly one article is featured at a time. An
unpublished article and its cover image stay unreachable to everyone but their
own author. The app is deployed and healthy.
