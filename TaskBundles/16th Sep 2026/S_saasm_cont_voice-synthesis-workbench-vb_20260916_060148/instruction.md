# Ethara Voice Studio

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, sign in as a creator, write a short script, pick a voice, generate a
narrated take, and see that take saved in their own asset library with the audio
playing back, without hitting an error page. The generated audio must live as a
real object in the object store, and a private take must never be readable by
anyone else, because a separate check reads the store and the database directly
and a take that only exists on screen does not count.

---

## Overview

Ethara Voice Studio is a text to speech workbench for creators, developers and
buyers who evaluate voice AI. A signed in creator browses a voice catalogue,
writes a script, picks a voice and a language, and generates a narrated take.
Each take is rendered to an audio object saved in the object store and added to
the creator's asset library. Generating a take draws down a credit balance, so
the workbench meters usage the way a real voice platform does.

Takes are private by default. A creator may publish a take to a public gallery
where any visitor can play it, while an unpublished take stays readable only by
its owner. The genuinely hard parts are two: the credit balance must stay honest
when many generations are requested at once, and a private take must stay
private even against a direct request for its stored audio.

This is the whole product. It is deliberately not a live conversational agents
console, not a voice cloning pipeline, and not a billing and invoicing system.
There are no phone calls, no real time streaming sockets, no payment collection,
and no team seat management.

---

## User roles

| Role | Can do |
|---|---|
| `author` | Sign up and sign in; browse and filter the voice catalogue; write a script and generate a narrated take; view, play and download their own takes; publish a take to the public gallery or return it to private; create and revoke their own metered API keys; read their own credit balance and usage. **Cannot** read, play, publish or delete another author's take, and **cannot** generate once their credit balance cannot cover the cost. |
| `reader` | Sign up and sign in; browse and filter the voice catalogue; play takes that have been published to the public gallery. **Cannot** generate a take, cannot create an API key, and cannot read any take that has not been published. |

Authorization is enforced server side on every mutating endpoint and on every
request for a stored object. Hiding a control in the UI is not authorization: a
direct API call from a `reader` session to any `author` only endpoint, or a
direct request from one author for another author's private take, must be
rejected by the server, leaving the protected state unchanged.

Signup is open: anyone may create an account with an email address and a
password, choosing the `author` or `reader` role at signup. Three accounts are
seeded for demonstration: `author@example.com` and `author2@example.com` as
authors, and `reader@example.com` as a reader.

---

## Core features

### Accounts and sessions

Email and password accounts. Passwords are hashed at rest and never stored or
logged in plaintext. Login returns a bearer token the client sends as
`Authorization: Bearer <token>`; tokens expire after 8 hours. Signup rejects an
already registered email and a password shorter than 8 characters, each with a
client error that names the field. There is no password reset and no third party
login.

### Voice catalogue

A shared catalogue of platform voices, seeded and read only to every account.
Each voice carries a display name, a short descriptor, one use case, one
language and a pre rendered preview clip that plays with no credit cost. The
catalogue can be filtered by use case and by language, and the current filter is
reflected in the page address so a filtered view can be shared. The seven use
cases are Advertisement, Characters, Conversational, Educational, Entertainment,
Narration and Social Media. The catalogue covers 8 languages.

### Generate a take

A signed in `author` writes a script of plain text, optionally marked with
bracketed direction tags such as `[whispers]` or `[laughs]` that are preserved
into the request, then picks one voice and one language and generates a take.
Generating charges a fixed 100 credits and produces one audio object saved in
the object store, after which the take appears in the author's asset library
with status `ready`. Rules, each individually checkable:

1. A generate request with a script, a known voice and a supported language
   succeeds, stores exactly one audio object, charges exactly 100 credits, and
   the take shows as `ready` and owned by the caller.
2. A generate request whose voice is unknown, whose language is unsupported, or
   whose script is empty is rejected with a client error that names the field,
   and no object is stored and no credit is charged.
3. A generate request from a `reader`, or from an account whose remaining
   balance is below 100 credits, is rejected and no object is stored.
4. A failed generate leaves no partial state: no orphan take row and no stored
   object with no matching take.

### Asset library

An `author` sees their own takes, newest first, each showing a script excerpt,
the voice name, the language, the status, the credits charged and the created
date. The library is paginated. Each take can be played from and downloaded
through an audio endpoint that streams the stored object to its owner. No author
can see or play another author's takes by any route.

### Visibility and the public gallery

Every take is `private` when created. An `author` may publish one of their own
takes, which sets its visibility to `public` and lists it in the gallery, and
may return a take to `private`, which removes it from the gallery immediately.

1. A published take appears in the public gallery and can be played by any
   signed in account, including a `reader`.
2. A take that is `private` is readable only by its owner. A request for its
   stored audio from another author, from a `reader`, or from an unauthenticated
   caller is denied by the server, and the take and its object are unchanged.
3. Returning a take to `private` removes it from the gallery on the next read
   and again denies its audio to everyone but the owner.

### Metered API keys

An `author` can create a named API key to generate takes from outside the
browser. The secret value is shown once at creation and is stored only as a
hash; it can never be retrieved again. The key list shows each key's prefix and
its last used time, never the secret. A generate request authenticated with a
valid key charges the owning author's credits and records a usage event; a
revoked or unknown key is rejected.

### Static pages and error handling

The app serves a `/privacy` page and a `/terms` page with real, readable
content, reachable from the footer. An unknown route renders a custom not-found
page that keeps the header and footer and returns the correct not-found status
rather than redirecting. Every form, including signup and the generate form,
validates its inputs in the browser and shows the specific reason for invalid
input inline before any request is sent.

---

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/signup` | Create an account and pick a role | No |
| `/login` | Email and password login | No |
| `/` | Voice catalogue with use case and language filters | Yes |
| `/studio` | Write a script, pick a voice, generate a take | `author` |
| `/library` | The author's own takes, paginated, with play and publish | `author` |
| `/gallery` | Public published takes, paginated, playable by anyone signed in | Yes |
| `/keys` | Create and revoke metered API keys | `author` |
| `/privacy` | Privacy page | No |
| `/terms` | Terms page | No |

**Entry and redirects.** An unauthenticated visit to any protected route
redirects to `/login`. Successful login lands on `/`. Logout returns to
`/login`. An expired token acting mid page redirects to `/login` without
crashing the view. A `reader` who reaches an `author` only route is sent back to
the catalogue rather than shown a broken page.

**Journeys.**

1. **Generate and save.** Sign in as `author@example.com`, open `/studio`, type
   a short script, pick the voice Aurora and the language English, and generate.
   The take appears in `/library` as `ready`, the credit balance drops by 100,
   and playing the take streams the stored audio.
2. **Publish to the gallery.** From `/library`, publish the new take. Open
   `/gallery` and confirm it appears and plays. Sign in as `reader@example.com`
   and confirm the same gallery take plays for a reader.
3. **Private stays private.** Sign in as `reader@example.com` and request the
   stored audio for `author2@example.com`'s private take directly. The request
   is denied and the take is unchanged. Sign in as `author@example.com` and make
   the same direct request for that other author's private take; it is denied
   too.
4. **Out of credits.** Sign in as an author whose balance is below 100 credits
   and attempt to generate. The attempt is rejected, no object is stored, and
   the balance is unchanged.

**States.** Every list and grid has a loading state and an empty state ("No
takes yet, write a script to get started"). Rule rejections surface the specific
reason inline. A network failure shows an inline retry, never a blank screen.

---

## UI/UX notes

Calm, precise and printed rather than screen like, closer to an architect's
drafting sheet than a consumer landing page. Confidence comes through generous
whitespace and quiet motion, not through size or colour. Hearing a voice is the
point, so the audio player is the primitive the whole product composes around.
Reference in spirit: the restraint of a well made research tool.

**Palette, by role.** The page ground is a warm, near white neutral, and cards
and popovers sit on pure white above it. Text is a near black neutral, with a
lighter neutral for secondary lines and hairline borders in a light neutral. The
one interactive accent is a soft blue for links and focus. A soft orange marks
the creation surfaces, a calm teal marks anything to do with metered usage, and
a bright violet is used only for the bracketed direction tags inside a script.
Success reads as a green and errors as a red. State is never carried by colour
alone: every status also carries a text label.

**Type.** `Inter` throughout, with a monospace face reserved for identifiers and
counts. Headings are set large and light and get lighter as they grow; body text
stays comfortably sized and never lightens below the secondary neutral. Times,
durations and credit counts use tabular numerals so columns align.

**Motion.** Motion is understated: things glide to a stop and nothing bounces.
Use a short, eased transition on hover, focus and panel changes, and animate the
generation progress indicator while a take renders. Respect
`prefers-reduced-motion` by disabling every non essential animation. Zero motion
is a defect and so is a bouncy overshoot.

**Depth and texture.** Surfaces are nearly flat, separated by hairlines and a
single soft shadow at most on a dialog. A fine monochrome grain sits over the
gradient hero and voice artwork so the surfaces read as printed rather than
plastic.

**Accessibility and responsiveness.** Meet WCAG AA contrast for body text, give
every interactive control a visible focus ring, and support full keyboard
navigation including the audio player transport. Icon only controls carry text
labels. The layout is responsive: it holds from a narrow phone viewport up to a
wide desktop, the catalogue reflows from a multi column grid to a single column
at the small breakpoint, and no view scrolls sideways.

---

## Technical requirements

- **Frontend:** React 18 with Vite and TypeScript.
- **Backend:** Node.js 20 with Express.
- **Database:** PostgreSQL, read the connection string from `DATABASE_URL`. The
  service is already running; do not install or start your own.
- **Object store:** MinIO, reached with `STORAGE_ENDPOINT`, `STORAGE_BUCKET`,
  `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Every generated take's audio is
  written to this store under a stable key and is served back through the app,
  never from the local filesystem and never as a blob inside the database.
- **Auth:** in app email and password, hashed at rest, stateless bearer tokens
  with an 8 hour expiry.
- **Health:** `GET /api/health` returns `200` when the app and its backing
  services are ready.
- **Logging:** requests and errors to stdout.

**Metering under concurrency.** The credit balance is the honest record of what
an account may still spend, and it must stay correct when generations arrive at
the same moment. Two simultaneous generate requests carrying the same
`Idempotency-Key` must create exactly one take and one stored object. The second
request must return the first take's id and must not create a second row. A
replay of that request with the same key and the same body must produce no
duplicate charge and no second write. The same key sent with a different body is
rejected with `409 Conflict`. When the remaining balance can pay for fewer
generations than are requested at once, only the generations the balance can
cover succeed and every other is rejected with `402`, and the balance is never
driven below zero. Application level checks alone are not sufficient under this
contention; state the observable outcome and choose any approach that delivers
it.

**Paginated reads.** The catalogue, the asset library, the public gallery and
the usage log are all read as pages. Each list endpoint accepts a `limit=` query
parameter, named `page_size`, with a default of 20 and a maximum of 100. The
client fetches the following page by passing an opaque cursor back unchanged.
The opaque cursor stays stable as the catalogue grows, so paging never repeats
or skips a voice across thousands of rows. Every list response carries
`next_cursor`, which is null on the final page, and a `has_more` boolean. A
request for a page beyond the end returns an empty page with `has_more` false
rather than an error.

- **No secrets in the browser bundle.** Storage credentials, database
  credentials and API key secrets are used only on the server and must never be
  compiled into or served with the frontend bundle.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, a cache, a message queue, a second object store, an
identity provider or a mail vendor: the only backing services in this
environment are PostgreSQL at `DATABASE_URL` and MinIO at `STORAGE_ENDPOINT`,
and reaching for anything else is a contract violation.

---

## Data model

All timestamps are UTC. Credits are whole integers.

> **Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
> fixture data, not a secret. Hash it as normal; the exact literal must work at
> login, and it must be written into `/app/USER_README.md` alongside each account
> so a reviewer can sign in.

**`accounts`** id; email (unique, lowercased); password_hash; role (`author` or
`reader`); created_at.

**`voices`** id; name; descriptor; use_case (one of the seven); language;
preview_key (the object key of the pre rendered preview); created_at. The
catalogue is seeded and read only to the app.

**`credit_grants`** id; account_id; amount (whole credits); granted_at;
expires_at (null for a grant that does not expire). The spendable balance of an
account is the sum of its unexpired grant amounts less the credits already
committed to takes, computed on read.

**`takes`** id; account_id (the owner); voice_id; language; script; status
(`ready`); visibility (`private` or `public`); storage_key; credits_charged;
idempotency_key (the client supplied key for the request that created it, null
when none was sent); created_at.

**`api_keys`** id; account_id; name; prefix (the shown part of the secret);
key_hash; last_used_at; revoked_at (null until revoked); created_at.

**`usage_events`** id; account_id; api_key_id (null for a browser generation);
take_id; credits; request_id (the correlation id of the generating request);
occurred_at.

**Rules the data must keep.** A take's audio lives in the object store under
`storage_key` and nowhere else. Two takes never share one stored object key.
Publishing changes only `visibility`; it never copies or moves the object. The
balance is never negative, and a take that was rejected leaves neither a row nor
a stored object behind.

**Derived, never stored:** the spendable balance, the filtered catalogue view
and each page's cursor are all computed on read. There is no balance column that
can drift and no cached page count.

**Seed data, exact and idempotent, relative to first start:**

- Voices: Aurora (Narration, English), Ember (Conversational, English), Sable
  (Characters, English), Cato (Educational, English), Lyric (Social Media,
  Spanish), Marlowe (Narration, French), Wren (Advertisement, German) and Juno
  (Entertainment, Japanese), each with a seeded preview object.
- Accounts, all with the seeded password: `author@example.com` (`author`),
  `author2@example.com` (`author`), `reader@example.com` (`reader`).
- Grants: `author@example.com` receives 300 credits, enough for exactly three
  generations, so the metering contract can be observed. `author2@example.com`
  receives 50 credits, below the cost of one generation.
- Takes: `author@example.com` owns one `public` take titled from a short welcome
  script; `author2@example.com` owns one `private` take, which is the target of
  the protected content journey. Each seeded take has its own stored audio
  object.

Seeding must be idempotent: restarting the app must not duplicate rows or
objects.

---

## Build plan

1. **Setup** scaffold the frontend and backend; `GET /api/health` returns `200`.
   Exit: health green through the public URL.
2. **Database and store** create the tables above and confirm the app can read
   and write the object store; idempotent seed of voices, accounts, grants and
   the two seeded takes. Exit: seed rows in Postgres and seed objects in the
   bucket; a re run adds nothing.
3. **Auth** signup, login and bearer middleware with roles. Exit: seeded
   accounts log in with the pinned password; a protected endpoint rejects an
   anonymous call.
4. **Catalogue** the seeded voices with use case and language filters and paged
   reads. Exit: filtering by a use case and by a language narrows the list and a
   second page fetch uses the returned cursor.
5. **Generate** the studio flow: charge credits, render an audio object into the
   store, save the take. Exit: a generate stores one object, charges 100 credits
   and shows the take `ready`.
6. **Metering** the concurrency and replay outcomes and the out of credits
   rejection. Exit: a duplicated key creates one take, a replay does not charge
   twice, and an unaffordable generate returns `402`.
7. **Library, gallery and visibility** own takes, publish and unpublish, and the
   protected audio endpoint. Exit: a private take's audio is denied to a
   non owner and a published take plays for a reader.
8. **Keys and usage** create once shown keys, meter key generations, record
   usage events. Exit: a key generation records a usage event with its request
   id and the key list never shows the secret.
9. **UI, static pages and hardening** palette, type, states, motion, responsive
   layout, privacy and terms pages, custom not found, form validation. Exit:
   every viewport holds with no sideways scroll and every negative case returns
   its named reason.
10. **Deploy and self test** production build, detached start, then walk every
    journey in a real browser. Exit: all four journeys pass against the deployed
    app, cold.

---

## Constraints

- One workbench, one shared voice catalogue; no per account custom voices and no
  voice cloning.
- No live conversational agents, no phone or chat channels, no real time audio
  sockets.
- No payment collection, no invoices, no plans or seats; credits are seeded, not
  purchased.
- No email, SMS or push of any kind.
- No second datastore, cache, queue or object store beyond the PostgreSQL and
  MinIO named here.
- No external network calls at runtime beyond the named backing services.
- Responsive web only; no native app.
- The catalogue read must stay responsive with thousands of voices.

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
| `GET /api/voices` | `?use_case=&language=&page_size=&cursor=` | `{items, next_cursor, has_more}` |
| `POST /api/takes` | `{voice_id, language, script}`, optional `Idempotency-Key` header | the take `{id, voice_id, language, status, visibility, credits_charged}` |
| `GET /api/takes` | `?page_size=&cursor=` | `{items, next_cursor, has_more}` of the caller's takes |
| `GET /api/takes/{id}/audio` | the stored audio stream | audio bytes for an entitled caller |
| `POST /api/takes/{id}/publish` | `{visibility}` | the take with its new `visibility` |
| `GET /api/gallery` | `?page_size=&cursor=` | `{items, next_cursor, has_more}` of public takes |
| `GET /api/credits` | the caller's balance | `{balance}` |
| `POST /api/keys` | `{name}` | `{id, name, prefix, key}` with `key` shown once |
| `GET /api/keys` | the caller's keys | array of `{id, name, prefix, last_used_at}` |
| `GET /api/usage` | `?page_size=&cursor=` | `{items, next_cursor, has_more}` of usage events |
| `GET /api/health` | readiness | `{ok: true}` |

Field names are exact. List endpoints return their rows under `items` with
`next_cursor` and `has_more`. Every business rule violation returns a client
error naming the reason, never a server error and never a silent success. Every
endpoint except signup, login and health requires a valid bearer token or a
valid API key; an anonymous caller is rejected.

### No mocks

Takes, credits and usage live in the real PostgreSQL at `DATABASE_URL`, and take
audio lives in the real MinIO bucket at `STORAGE_ENDPOINT`, and nowhere else. An
in memory list, a local file store, a browser stored copy, or a grid rendered
from client state that was never persisted is a contract violation. A take that
shows on screen but is absent from Postgres or whose audio is absent from the
bucket does not count. The named provider is the fact: the app's UI and its own
tables can only reflect what lives in the provider, never substitute for it.

---

## Definition of done

The app is deployed and healthy. A stranger can sign in as a creator, write a
script, generate a take, and play it back from their asset library with the
credit balance reduced by its cost. The generated audio exists as an object in
the store, a published take plays for anyone in the gallery, and a private take
cannot be read by any other account. Generating the same request twice with one
key creates exactly one take and charges once, and an account that cannot afford
a generation is refused. Every credit and count shown matches the database.
