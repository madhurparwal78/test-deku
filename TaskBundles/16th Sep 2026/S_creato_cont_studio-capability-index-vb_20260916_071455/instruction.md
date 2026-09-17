# Halvard Studio Capability Index

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, read a published client case study filtered by its industry, browse the
services and articles, and submit a project enquiry that lands on an
acknowledgement page, without hitting an error page. A separate check reads the
database and the object store directly, so a case study that only exists on
screen, or a draft whose media is reachable by a guessed address, does not count.

---

## Overview

Halvard Studio is the public site of a two person digital studio that sells
brand identity and production websites. It is aimed at a marketing lead scouting
a partner, who needs to answer three questions in order: have these people done
work at my scale, do they do the thing I need, and are two people enough. The
site answers them with client case studies cut by industry, a services index, a
wall of side experiments, insight articles and a small product shelf. A visitor
ends by submitting a project enquiry that requests a thirty minute introduction
call.

An editor signs in to publish and manage the content and to read the enquiries
that arrive. Everything a visitor sees is public and needs no account. The
genuinely hard parts are two: a draft case study, and its media, must never be
readable by the public until it is published, and a project enquiry submitted
twice from one attempt must create exactly one record.

This is the whole product. It is deliberately not a store with prices or a cart,
not a booking calendar with live availability, and not a comment or account
system for visitors. There are no likes, no view counters shown to visitors, and
no site-wide search.

---

## User roles

| Role | Can do |
|---|---|
| `editor` | Sign up and sign in; create, edit, publish and unpublish case studies, services, articles, experiments and products; preview their own drafts before publishing; read submitted enquiries. **Cannot** be impersonated by an anonymous caller: every managing endpoint refuses a request that carries no editor session. |
| `visitor` | Read every published case study, service, article, experiment and product with no account; filter case studies by industry; submit one project enquiry. **Cannot** read a draft record or its media, and **cannot** reach any editor managing endpoint. |

Authorization is enforced server side on every mutating endpoint and on every
request for a draft record or a draft media object. Hiding a control in the UI is
not authorization: a direct API call from a `visitor` session, or from an
anonymous caller, to any `editor` only endpoint must be refused by the server,
leaving the content unchanged.

Signup is open for editors: a studio member may create an account with an email
address and a password. Two editor accounts and one visitor account are seeded
for demonstration: `editor@example.com`, `editor2@example.com` and
`visitor@example.com`.

---

## Core features

### Accounts and sessions

Email and password accounts for editors. Passwords are hashed at rest and never
stored or logged in plaintext. Login returns a bearer token the client sends as
`Authorization: Bearer <token>`; tokens expire after 8 hours. Signup rejects an
already registered email and a password shorter than 8 characters, each with a
client error naming the field. There is no password reset and no third party
login.

### Case studies filtered by industry

A case study carries a client name, one industry, a short summary, a serif deck
sentence, a credits list and an ordered body of typed blocks, plus media stored
as objects. The public case study index lists only published case studies and
can be filtered by one of the seven industries: Fintech, Maritime, Pharma,
Networks, Recruitment, Sports Tech and Real Estate. Each detail page shows the
deck, the credits, the block body and an optional client quote. Rules, each
individually checkable:

1. The index lists a case study only once it is published, newest first, and the
   industry filter narrows the list to matching case studies.
2. A published case study detail renders its deck, credits and blocks, and its
   media loads from the object store.
3. A case study whose industry is unknown, or whose summary is empty, is refused
   at the managing endpoint with a client error naming the field.

### Draft protection

Every case study and article is a draft when created and public only once an
editor publishes it. This is the load bearing rule:

1. A draft record is not-found to the public: the public detail route returns a
   not found status, never a redirect, and never the draft body.
2. A draft record's media object is not publicly readable: a direct request for
   it from a visitor or an anonymous caller is refused, and the object is
   unchanged. Publishing the record makes both the record and its media public.
3. An editor previews their own draft through an authenticated route before
   publishing.

### Services index and detail

Services are grouped into three practice areas. The services index shows the
full catalogue and marks the services that carry their own page. A service
detail page shows a deck and a body, and a proof row of the published case
studies that credited that service, drawn from the case study credits. Expanding
a group in the index is navigation only and does not filter the catalogue.

### Articles, the wall and the shelf

Insight articles are read from a masonry index that shows every published
article, each opening to a detail page with a body and a closing questions block.
Exactly one article is pinned to the head of the index. The side experiments wall
shows the studio's experiments with a "Load more" control that appends the next
page in place. A small product shelf shows three products, each an outbound link
to its own site.

### Project enquiry

A visitor submits one project enquiry from the enquiry desk: a name, an email, an
optional company, an optional budget band, an optional set of services, a
message and a consent checkbox. A valid submission is persisted as one enquiry
and the visitor lands on an acknowledgement page. Validation is checkable: the
name is required, the email must be syntactically valid, the message is between
20 and 4000 characters, and consent is required; each failure is named on the
field. A submitted enquiry is readable only by an editor.

### Static pages and error handling

The app serves a `/privacy` page and a `sitemap` that lists every published
route, both reachable without an account. An unknown route renders a custom
not-found page that keeps the header and footer and returns the correct
not-found status rather than redirecting. The enquiry form validates its inputs
in the browser and names the reason for any invalid input inline. A page view is
recorded for each public route so the studio can see traffic, and no visitor
facing counter is shown.

---

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/signup` | Create an editor account | No |
| `/login` | Email and password login | No |
| `/` | Home: featured work, services, latest articles | No |
| `/work` | Case study index with the industry filter | No |
| `/work/{slug}` | One published case study | No |
| `/services` | Services index | No |
| `/services/{slug}` | One service with its proof row | No |
| `/posts` | Article masonry index | No |
| `/posts/{slug}` | One article with its questions block | No |
| `/experiments` | The experiments wall with Load more | No |
| `/products` | The product shelf | No |
| `/enquiry` | The project enquiry desk | No |
| `/enquiry/sent` | Acknowledgement after a submission | No |
| `/privacy` | Privacy page | No |
| `/studio` | Editor console: manage records and read enquiries | `editor` |

**Entry and redirects.** The public routes need no account. An unauthenticated
visit to `/studio` redirects to `/login`. Successful login lands on `/studio`. A
`visitor` session that reaches `/studio` is sent back to the home page rather
than shown a broken view. An expired token acting mid page redirects to `/login`.

**Journeys.**

1. **Scout the work.** Open `/work`, filter by Fintech, open a published case
   study, and read its deck, credits and body with the media loaded from the
   store.
2. **Draft stays private.** A visitor requests a draft case study by its address
   and receives a not-found page; a direct request for that draft's media object
   is refused. An editor signs in, previews the same draft, then publishes it,
   and now both the page and its media are public.
3. **Submit an enquiry.** From the enquiry desk, fill a valid name, email,
   message and consent, submit, and land on the acknowledgement page. Submitting
   the same attempt twice creates exactly one enquiry.
4. **Read the studio.** Open `/posts`, open a published article, read its body
   and its closing questions block.

**States.** Every list and grid has a loading state and an empty state ("No case
studies yet"). Rule rejections surface the specific reason inline. A network
failure shows an inline retry, never a blank screen.

---

## UI/UX notes

Restrained, senior and calm, closer to an editorial workbench than a consumer
catalogue. Confidence comes through dense, warm-grey monochrome and generous
whitespace, not through colour or size. Reference in spirit: a printed capability
document, quiet and self-assured.

**Palette, by role.** The page ground is a light, warm neutral, and cards and
panels sit as pure white above it. Text is a near black neutral, with a deep,
warm grey neutral for secondary lines and hairline borders in a light neutral.
The one accent is a single vivid green dot on the leading edge of the book a call
button, used two or three times a page and nowhere else. Meaning never rides on
colour alone: there is no red error state, and every status carries a text label.

**Type.** A grotesque sans throughout, named `Aeonik`, with a display serif named
`Feature Deck` reserved for a handful of italic emphasis words and the case study
deck. No weight is ever bold: headings are light and body text stays comfortably
sized. Headings are tracked tight and get lighter as they grow.

**Motion.** Motion is held to a minimum: colour changes are quick and position
changes are slow, and nothing bounces. Use a short transition on hover and focus,
and animate a headline that resolves out of a character scramble on first view.
Respect `prefers-reduced-motion` by disabling every non essential animation. Zero
motion is a defect and so is a bouncy overshoot.

**Shape and depth.** Surfaces are nearly flat, separated by hairlines rather than
shadow, with at most one soft shadow on the cookie consent strip. A persistent
left rail on the work, services and article routes keeps its scroll position when
a visitor opens a detail page.

**Accessibility and responsiveness.** Meet WCAG AA contrast for body text, give
every interactive control a visible focus ring, and support full keyboard
navigation. Icon only controls carry text labels. The layout is responsive: it
holds from a narrow viewport on a phone up to a wide desktop, the case study and
article grids reflow to a single column at the small breakpoint, and no view
scrolls sideways.

---

## Technical requirements

- **Frontend:** React 18 with Vite and TypeScript.
- **Backend:** Node.js 20 with Express.
- **Database:** PostgreSQL, read the connection string from `DATABASE_URL`. The
  service is already running; do not install or start your own.
- **Object store:** MinIO, reached with `STORAGE_ENDPOINT`, `STORAGE_BUCKET`,
  `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Every case study and article
  media file is written to this store under a stable key and served back through
  the app, never from the local filesystem and never as a blob inside the
  database.
- **Auth:** in app email and password for editors, hashed at rest, stateless
  bearer tokens with an 8 hour expiry.
- **Health:** `GET /api/health` returns `200` when the app and its backing
  services are ready.
- **Logging:** requests and errors to stdout.

**Enquiry write under contention.** The enquiry desk mints an idempotency key
when the form first renders and sends it on every submit attempt. Two submissions
carrying the same `Idempotency-Key` must create exactly one enquiry. The second
must return the first enquiry's id and must not create a second row. A replay of
that submission with the same key and the same body must produce no second write.
The same key sent with a different body is rejected with `409 Conflict`. A
managing check alone is not sufficient under this contention; state the
observable outcome and choose any approach that delivers it.

**Paginated reads.** The case study index, the article index and the experiments
wall are all read as pages. Each list endpoint accepts a `limit=` query
parameter, named `page_size`, with a default of 20 and a maximum of 100. The
client fetches the following page by passing an opaque cursor back unchanged. The
opaque cursor stays stable as records are added, so paging never repeats or skips
an item across a long list. Every list response carries `next_cursor`, which is
null on the final page, and a `has_more` boolean. A request for a page beyond the
end returns an empty page with `has_more` false rather than an error.

- **No secrets in the browser bundle.** Storage credentials, database
  credentials and the editor session secret are used only on the server and must
  never be compiled into or served with the frontend bundle.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, a cache, a message queue, a second object store, an
identity provider or a mail vendor: the only backing services in this environment
are PostgreSQL at `DATABASE_URL` and MinIO at `STORAGE_ENDPOINT`, and reaching for
anything else is a contract violation.

---

## Data model

All timestamps are UTC.

> **Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
> fixture data, not a secret. Hash it as normal; the exact literal must work at
> login, and it must be written into `/app/USER_README.md` alongside each account
> so a reviewer can sign in.

**`accounts`** id; email (unique, lowercased); password_hash; role (`editor` or
`visitor`); created_at.

**`case_studies`** id; slug (unique); client_name; industry (one of the seven);
summary; deck; visit_url (optional); status (`draft` or `published`);
published_at; created_at.

**`case_study_media`** id; case_study_id (the owner); storage_key; ordinal. Media
lives under `storage_key` in the object store, keyed as
`casestudies/{id}/{sha256}.{ext}`, and nowhere else.

**`case_study_credits`** id; case_study_id; service_id; grouping. The proof row
of a service is drawn from these rows.

**`services`** id; slug (unique); name; group; benefit; has_page (boolean);
ordinal.

**`articles`** id; slug (unique); title; kind (`insight` or `vault`); standfirst;
status (`draft` or `published`); pinned (boolean); published_at; created_at.

**`experiments`** id; name; kind; media_key; ordinal.

**`products`** id; name; description; url (absolute, off site); ordinal.

**`enquiries`** id; name; email; company (optional); budget_band (optional);
message; consent (boolean); idempotency_key (the client supplied key, unique per
enquiry); received_at.

**Rules the data must keep.** An index query returns only records whose status is
published; a draft record is not-found to the public. A case study's media lives
under `storage_key` in the object store, never as a database blob, and a draft's
media is not publicly readable. Two submissions carrying one idempotency key
result in exactly one enquiry row. At most one article is pinned.

**Derived, never stored:** the filtered case study list, each page's cursor and a
service's proof row are all computed on read.

**Seed data, exact and idempotent, relative to first start:**

- Accounts, all with the seeded password: `editor@example.com` (`editor`),
  `editor2@example.com` (`editor`), `visitor@example.com` (`visitor`).
- Case studies: at least one published case study per seeded industry so the
  filter can be observed, plus one `draft` case study owned by the studio with
  its own media object, which is the target of the draft protection journey.
- Services across the three groups, some carrying their own page; articles with
  exactly one pinned; a handful of experiments and three products.

Seeding must be idempotent: restarting the app must not duplicate a row or an
object.

---

## Build plan

1. **Setup** scaffold the frontend and backend; `GET /api/health` returns `200`.
2. **Database and store** create the tables and confirm the app reads and writes
   the object store; idempotent seed of accounts, case studies, services,
   articles, experiments and products.
3. **Auth** editor signup, login and bearer middleware with roles.
4. **Case studies** the industry filter and the detail page with media from the
   store, paginated reads.
5. **Draft protection** drafts not-found to the public, draft media refused,
   editor preview, publish makes both public.
6. **Services, articles, wall, shelf** the indexes and details, the proof row,
   the pinned article, the Load more wall and the product shelf.
7. **Enquiry** the desk, validation, the idempotent one-record write, the
   acknowledgement page.
8. **UI, static pages and hardening** palette, type, motion, responsive layout,
   privacy page, sitemap, custom not-found, page view logging.
9. **Deploy and self test** production build, detached start, then walk every
   journey in a real browser.

---

## Constraints

- One studio site, one shared catalogue of content; no visitor accounts.
- No prices, no cart, no payment; the product shelf links off site.
- No live booking calendar or slot availability; the thirty minute call is
  requested through the enquiry, not reserved in the app.
- No email, SMS or push; the acknowledgement is shown on screen only.
- No second datastore, cache, queue or object store beyond the PostgreSQL and
  MinIO named here.
- No external network calls at runtime beyond the named backing services.
- Responsive web only; no native app.
- The case study and article reads must stay responsive with hundreds of records.

---

## Deployment contract

Your application is served over HTTP and opened in a browser after your session
has ended.

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`: `4173` is the container internal port and
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
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

Write `/app/USER_README.md` with the three seeded accounts and their password.

### API shapes

| Endpoint | Request body or query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{email, password, role}` | `{token}` |
| `POST /api/auth/login` | `{email, password}` | `{token}` |
| `GET /api/case-studies` | `?industry=&page_size=&cursor=` | `{items, next_cursor, has_more}` of published case studies |
| `GET /api/case-studies/{slug}` | a published case study | the case study, or not-found for a draft |
| `GET /api/case-studies/{slug}/media/{id}` | a media object | the bytes for a published case study, refused for a draft |
| `GET /api/services` | the catalogue | array of services |
| `GET /api/services/{slug}` | one service | the service with its proof row |
| `GET /api/posts` | `?page_size=&cursor=` | `{items, next_cursor, has_more}` of published articles |
| `GET /api/experiments` | `?page_size=&cursor=` | `{items, next_cursor, has_more}` |
| `POST /api/enquiries` | `{name, email, company, budget_band, services, message, consent}`, optional `Idempotency-Key` header | the enquiry `{id}` |
| `GET /api/enquiries` | the studio inbox | array of enquiries, editor only |
| `GET /api/health` | readiness | `{ok: true}` |

Field names are exact. List endpoints return their rows under `items` with
`next_cursor` and `has_more`. Every business rule violation returns a client
error naming the reason, never a server error and never a silent success. The
managing endpoints require a valid editor bearer token; an anonymous caller is
refused.

### No mocks

Content and enquiries live in the real PostgreSQL at `DATABASE_URL`, and case
study and article media live in the real MinIO bucket at `STORAGE_ENDPOINT`, and
nowhere else. An in memory list, a local file store, a browser stored copy, or a
page rendered from client state that was never persisted is a contract
violation. A case study that shows on screen but is absent from Postgres, or
whose media is absent from the bucket, does not count. The named provider is the
fact: the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

---

## Definition of done

The app is deployed and healthy. A stranger can read a published case study
filtered by its industry with its media loaded from the store, browse the
services and articles, and submit a project enquiry that lands on the
acknowledgement page. A draft case study is not-found to the public and its media
cannot be read until it is published. Submitting one enquiry attempt twice
creates exactly one record. Every record shown matches the database.
