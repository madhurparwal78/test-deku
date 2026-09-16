# Foldline

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, sign in as the publisher, write a post, set a paywall by moving a gate
line across the real audience, publish the post so its audio edition is stored,
and confirm that a paying subscriber can play that edition while a free reader
cannot, without hitting an error page. The audio edition must live as a real
object in the object store, and a gated edition must never be readable by a
reader who has not paid for it, because a separate check reads the store and the
database directly and content that only exists on screen does not count.

---

## Overview

Foldline is where one independent writer runs a paid publication end to end:
writing posts, gating some of them behind a paid tier, collecting recurring
subscription revenue from readers, and seeing whether a gating decision earned
more than it cost. The audience and the money are the same object as the writing,
so the paywall can be set against real readers rather than guessed.

The genuinely hard parts are two. The paywall must hold: a gated post's audio
edition must stay readable only by a subscriber whose paid tier reaches the gate,
even against a direct request for the stored object. And the money must stay
honest: subscribing once must charge once and book one balanced ledger
transaction, even when the same request arrives twice at the same moment.

---

## User roles

| Role | Can do |
|---|---|
| `author` | Sign up and sign in; write, gate and publish posts; move the gate line to set a post's paywall and read the live projection; see the audience as records; read the double-entry ledger; create discount offers; release a post as a newsletter. **Cannot** be charged, and the author is the only role that may write a post or read the audience and the ledger. |
| `reader` | Sign up and sign in; read the free portion of any published post; subscribe to a paid tier and read gated posts and play their audio editions while the subscription is active; read and manage their own subscription. **Cannot** write, gate or publish a post, cannot read the audience or the ledger, and cannot play a gated audio edition without an active paid subscription that reaches the gate. |

Authorization is enforced server side on every mutating endpoint and on every
request for a stored object. Hiding a control in the UI is not authorization: a
direct API call from a `reader` session to any `author` only endpoint, or a
direct request from a free reader for a gated audio edition, must be rejected by
the server, leaving the protected state unchanged.

Signup is open: anyone may create an account with an email address and a
password, choosing the `author` or `reader` role at signup. Accounts are seeded
for demonstration: `author@example.com` as the publisher, `reader@example.com` as
a paying premium subscriber, and `reader2@example.com` as a free reader.

---

## Core features

### Accounts and sessions

Email and password accounts. Passwords are hashed at rest and never stored or
logged in plaintext. Login returns a bearer token the client sends as
`Authorization: Bearer <token>`; tokens expire after 8 hours. Signup rejects an
already registered email and a password shorter than 8 characters, each with a
client error that names the field. There is no password reset and no third party
login.

### Posts and the composer

A signed in `author` writes a post with a title, a body of plain text, and a
free word count that marks how much of the body any visitor may read. A post is a
draft until it is published. The free portion of a published post is public and
readable by anyone; the gated remainder is readable only by an entitled reader.
Rules, each individually checkable:

1. An author creates a post as a draft with a title, a body and a free word count.
2. Publishing a post stores exactly one audio edition object and marks the post
   published, after which it appears on the public site.
3. A post created by one author is never writable by a reader or by another
   account through any route.

### The audience field and the gate

The paywall is set spatially: the author moves a gate line across the real
audience and the consequence is shown before it is committed. The gate names the
tier at or above which a subscriber may read the post. As the gate moves, a
projection recomputes against the publication's own cohort: the projected reach,
the projected recurring revenue, and a confidence. Rules, each individually
checkable:

1. The projected reach for a gate is the count of subscribers whose active tier
   is at or above the gated tier, computed on read from the real audience.
2. Below the minimum cohort of `3` subscribers at or above the gated tier, the
   projection refuses to project a revenue figure and shows the raw counts
   instead of a confident number.
3. Committing the gate writes the post's paywall directly; the projection is a
   reading of the same gate, never a separate control that can drift from it.
4. A gate that names an unknown or deactivated tier is refused, naming the tier,
   and the post's existing gate is unchanged.

### The gated audio edition

Every published post has exactly one audio edition saved as a single object in
the store. The edition of a gated post is protected: it is readable only by a
reader whose active paid tier reaches the post's gate.

1. A published post names a stored audio edition object that exists in the store.
2. A gated edition streams to an entitled subscriber and is refused to a free
   reader and to an unauthenticated caller, and the object is unchanged.
3. A public post's edition plays for any signed in account.

### Tiers, offers and subscribing

The publication seeds a free tier and a paid `premium` tier priced at `800` minor
units. A reader subscribes to a paid tier and gains entitlement to gated posts at
or below that tier. An author may publish a discount offer, a code that takes a
percentage off the tier price at checkout. Rules, each individually checkable:

1. A reader subscribes to `premium`, the subscription becomes active, and the
   reader can then read a `premium` gated post.
2. Applying the seeded offer `WELCOME25` takes `25` percent off, so a `premium`
   subscription resolves to `600` minor units.
3. A subscribe request from an already subscribed reader for the same active tier
   creates no second active subscription.

### The double-entry ledger

Every subscription charge is booked into a double-entry ledger the author can
read. Each ledger transaction posts a balanced pair of entries: the sum of its
debit amounts equals the sum of its credit amounts. Entries are append-only, so a
correction is a new opposing transaction rather than an edit. Across the whole
publication the ledger reconciles: total debits equal total credits.

### The audience and newsletter release

The author sees subscribers as records carrying their tier, their last seen
engagement, and a lifetime value read from the ledger. Releasing a published post
as a newsletter resolves the recipients for a segment and creates one delivery
record per resolved recipient. Re-releasing the same post to the same segment
creates no further delivery for a recipient already served. The resolved
recipient count is the exact number of subscribers who will receive it.

### Static pages, links and error handling

The app serves a `/privacy` page with real, readable content, reachable from the
footer of every page, stating what the publication stores about a subscriber.
Every internal link on every public route resolves to a real page. Every form,
including signup and the composer, validates its inputs in the browser and shows
the specific reason for invalid input inline before any request is sent.

---

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/signup` | Create an account and pick a role | No |
| `/login` | Email and password login | No |
| `/` | The public site: published posts with their free portion | No |
| `/posts/{slug}` | A public post; the gated remainder needs an entitled tier | No |
| `/composer` | Write and edit a post | `author` |
| `/field/{id}` | The audience field: move the gate and read the projection | `author` |
| `/audience` | Subscribers as records, paginated | `author` |
| `/ledger` | The double-entry ledger, paginated | `author` |
| `/subscribe` | Pick a tier, apply an offer, subscribe | `reader` |
| `/privacy` | Privacy page | No |

**Entry and redirects.** An unauthenticated visit to any protected route
redirects to `/login`. Successful login lands the author on the composer and the
reader on the public site. Logout returns to `/login`. An expired token acting
mid page redirects to `/login` without crashing the view. A `reader` who reaches
an `author` only route is sent back to the public site rather than shown a broken
page.

**Journeys.**

1. **Gate and publish.** Sign in as `author@example.com`, open the composer,
   write a short post, open its audience field, move the gate to `premium`, read
   the projected reach and revenue, commit the gate, then publish. The post
   appears on the public site with only its free portion open, and its audio
   edition is stored.
2. **Pay to read.** Sign in as `reader@example.com`, open the gated post, and
   play its audio edition. The edition plays because the subscription reaches the
   gate.
3. **The paywall holds.** Sign in as `reader2@example.com`, open the same gated
   post, and request its audio edition directly. The request is refused and the
   stored object is unchanged.
4. **Subscribe once.** Sign up a new reader and subscribe to `premium` with a
   discount code. The balance charged and the ledger transaction match the
   discounted price, and repeating the subscribe does not charge again.

**States.** Every list and the audience field have a loading state and an empty
state ("No subscribers yet, import or invite your readers"). Rule rejections
surface the specific reason inline. A network failure shows an inline retry,
never a blank screen. When the cohort is too small the field shows the raw counts
with a plain explanation rather than a confident projection.

---

## UI/UX notes

The console reads as an editorial desk rather than a dashboard: a warm near white
ground, pure white raised surfaces, near black primary text with a lighter
neutral for secondary lines, and hairline borders in a light neutral. The
audience field sits on its own dark plane in either theme so the gate and the
cohort read clearly. Colour is held back: a deep blue is the one interactive
accent for links and focus, positive figures such as revenue rising read as a
muted teal green, negative figures read as a red, and anything at risk reads as a
muted orange amber. State is never carried by colour alone; every status also carries a
text label.

**Type.** A reading serif carries post bodies, post titles and the public
surface, and a grotesque interface face carries the console. Every ledger figure,
projection figure and table count uses tabular numerals so columns align.

**Motion.** Motion is understated: panels ease to a stop and nothing bounces
except the gate as it settles into place. Use a short eased transition on hover,
focus and panel changes, and animate the projection figures so they settle rather
than snapping when the gate moves. Respect `prefers-reduced-motion` by disabling
every non essential animation. Zero motion is a defect and so is a bouncy
overshoot on anything but the gate.

**Accessibility and responsiveness.** Meet WCAG AA contrast for body text, give
every interactive control a visible focus ring, and support full keyboard
navigation including moving the gate line by the arrow keys. Icon only controls
carry text labels. Every content image carries alternative text and a purely
decorative image declares itself decorative. The layout is responsive: it holds
from a narrow phone viewport up to a wide desktop, and on a narrow viewport the
audience field is replaced by a cohort table rather than a spatial control so no
view scrolls sideways.

---

## Technical requirements

- **Frontend:** React 18 with Vite and TypeScript.
- **Backend:** Node.js 20 with Express.
- **Database:** PostgreSQL, read the connection string from `DATABASE_URL`. The
  service is already running; do not install or start your own.
- **Object store:** MinIO, reached with `STORAGE_ENDPOINT`, `STORAGE_BUCKET`,
  `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Every published post's audio
  edition is written to this store under a stable key and is served back through
  the app, never from the local filesystem and never as a blob inside the
  database.
- **Auth:** in app email and password, hashed at rest, stateless bearer tokens
  with an 8 hour expiry.
- **Health:** `GET /api/health` returns `200` when the app and its backing
  services are ready.
- **Logging:** requests and errors to stdout.

**Subscribing under concurrency.** Subscribing must stay correct when two
requests for one reader arrive at the same moment. Two simultaneous subscribe
requests carrying the same `Idempotency-Key` must create exactly one
subscription; the second must return the first subscription's id and must not
create a second row. A replay of that request with the same key and the same body
must produce no second charge and no second ledger transaction. The same key sent
with a different body is rejected with `409 Conflict`. Application level checks
alone are not sufficient under this contention; state the observable outcome and
choose any approach that delivers it.

**Paginated reads.** The audience, the posts list and the ledger are all read as
pages. Each list endpoint accepts a `limit=` query parameter, named `page_size`,
with a default of 20 and a maximum of 100. The client fetches the following page
by passing an opaque cursor back unchanged. The opaque cursor stays stable as the
audience grows, so paging never repeats or skips a subscriber across thousands of
rows. Every list response carries `next_cursor`, which is null on the final page,
and a `has_more` boolean. A request for a page
beyond the end returns an empty page with `has_more` false rather than an error.

**Discoverability.** A `sitemap` lists every public route and a robots file
points at the sitemap. Every public route declares its own social preview title
and a preview image, and the preview image resolves.

- **No secrets in the browser bundle.** Storage credentials and database
  credentials are used only on the server and must never be compiled into or
  served with the frontend bundle.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, a cache, a message queue, a second object store, an
identity provider, a payment processor or a mail vendor: the only backing
services in this environment are PostgreSQL at `DATABASE_URL` and MinIO at
`STORAGE_ENDPOINT`, and reaching for anything else is a contract violation.

---

## Data model

All timestamps are UTC. Money is whole minor units of `usd`.

> **Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
> fixture data, not a secret. Hash it as normal; the exact literal must work at
> login, and it must be written into `/app/USER_README.md` alongside each account
> so a reviewer can sign in.

**`accounts`** id; email (unique, lowercased); password_hash; role (`author` or
`reader`); created_at.

**`posts`** id; author_id (the owner); title; slug; body; free_words (the count
of leading words any visitor may read); gate_tier (null for a public post, else
the tier name at or above which a subscriber may read); status (`draft` or
`published`); audio_key (the object key of the stored audio edition, null until
published); created_at; published_at.

**`tiers`** id; name (`free` or `premium`); type (`free` or `paid`); price_minor
(whole minor units, `0` for free); active; created_at. Seeded and read only to
the app.

**`offers`** id; code (unique, lowercased); percent_off (1 to 100); active;
created_at.

**`subscriptions`** id; subscriber_id; tier_id; status (`active` or `cancelled`);
amount_minor (the charged amount after any offer); offer_code (null when none);
idempotency_key (the client supplied key, null when none was sent); started_at;
cancelled_at.

**`ledger_transactions`** id; subscription_id; idempotency_key; kind (`charge`);
occurred_at. Each transaction owns a balanced set of entries.

**`ledger_entries`** id; transaction_id; direction (`debit` or `credit`);
account (for example `assets:receivable` or `income:subscriptions`); amount_minor
(greater than zero); created_at.

**`deliveries`** id; post_id; subscriber_id; segment; status (`queued` or
`sent`); created_at. No two deliveries for one post reach the same subscriber.

**`engagement`** each subscriber row carries a last_seen timestamp and a computed
lifetime value read from the ledger, never a stored money column that can drift.

**Rules the data must keep.** A post's audio edition lives in the object store
under `audio_key`, a key that begins `editions/` (for example
`editions/{post_id}/{sha256}.mp3`), and nowhere else; two posts never share one
stored object key;
publishing changes the post status and writes the edition, it never inlines the
audio on the row. For every ledger transaction the debits equal the credits, and
the balance is computed on read from the entries. A subscribe that was refused
leaves neither a subscription row nor a ledger transaction behind.

**Derived, never stored:** the projected reach and revenue for a gate, the
spendable segment of the audience, a subscriber's lifetime value, and each page's
cursor are all computed on read. There is no reach column and no cached balance
that can drift.

**Seed data, exact and idempotent, relative to first start:**

- Tiers: `free` at `0` and `premium` at `800` minor units in `usd`.
- Offers: `WELCOME25` at `25` percent off, active.
- Accounts, all with the seeded password: `author@example.com` (`author`),
  `reader@example.com` (`reader`), `reader2@example.com` (`reader`), and three
  further readers `reader3@example.com`, `reader4@example.com` and
  `reader5@example.com`.
- Subscriptions: `reader@example.com` and `reader3@example.com` are active on
  `premium`, so the `premium` cohort is `2`, below the minimum of `3` and a
  projection at `premium` refuses. `reader2@example.com`, `reader4@example.com`
  and `reader5@example.com` are on `free`, so the whole-audience cohort of `6`
  supports a projection at `free`.
- Posts: `author@example.com` owns one `published` post gated at `premium` with a
  stored audio edition, which is the target of the paywall journey, and one
  `published` public post whose edition plays for anyone.

Seeding must be idempotent: restarting the app must not duplicate rows or objects.

---

## Build plan

1. **Setup** scaffold the frontend and backend; `GET /api/health` returns `200`.
   Exit: health green through the public URL.
2. **Database and store** create the tables above and confirm the app can read
   and write the object store; idempotent seed of tiers, the offer, accounts,
   subscriptions and the two seeded posts. Exit: seed rows in Postgres and seed
   objects in the bucket; a re run adds nothing.
3. **Auth** signup, login and bearer middleware with roles. Exit: seeded accounts
   log in with the pinned password; a protected endpoint rejects an anonymous call.
4. **Posts** the composer and the public reading surface with the free portion.
   Exit: an author writes a draft and a visitor reads its free portion.
5. **Gate and projection** the audience field, the projected reach and revenue,
   the minimum-cohort refusal, and the gate commit. Exit: moving the gate
   recomputes the projection and committing writes the paywall.
6. **Publish and protect** publishing stores one audio edition object and the
   gated edition is denied to a free reader. Exit: an entitled subscriber plays
   the edition and a free reader is refused.
7. **Tiers and subscribe** the tiers, the discount offer, and idempotent
   subscribe. Exit: a duplicated key creates one subscription and a replay does
   not charge twice.
8. **Ledger and audience** the double-entry ledger, the subscriber records, and
   newsletter release. Exit: a subscribe books a balanced transaction, the ledger
   reconciles, and a release creates no duplicate delivery.
9. **UI, static pages and hardening** palette, type, states, motion, responsive
   layout, the privacy page, alternative text, the sitemap and social previews,
   form validation. Exit: every viewport holds with no sideways scroll and every
   negative case returns its named reason.
10. **Deploy and self test** production build, detached start, then walk every
    journey in a real browser. Exit: all four journeys pass against the deployed
    app, cold.

---

## Constraints

- One publication run by one writer; no multi-tenant hosting and no team seats.
- No WebGL particle compositor: the audience field is a data-driven gating surface
  with a live projection, not a 250,000-point GPU scene.
- No collaborative multi-writer editing, no presence and no suggestion flow.
- No real payment processor: subscription charges are booked into the local
  ledger, not collected from a card vendor.
- No deliverability reputation, no domain warmup and no dunning.
- No custom domains, no TLS provisioning and no email or SMS sending; a newsletter
  release records deliveries in the database.
- No second datastore, cache, queue or object store beyond the PostgreSQL and
  MinIO named here.
- No external network calls at runtime beyond the named backing services.
- Responsive web only; no native app.
- The audience and the ledger must stay responsive with tens of thousands of rows.

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

Write `/app/USER_README.md` with the seeded accounts and their password.

### API shapes

| Endpoint | Request body or query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{email, password, role}` | `{token}` |
| `POST /api/auth/login` | `{email, password}` | `{token}` |
| `GET /api/posts` | `?status=&page_size=&cursor=` | `{items, next_cursor, has_more}` |
| `POST /api/posts` | `{title, body, free_words}` | the post `{id, slug, status, gate_tier}` |
| `GET /api/posts/{id}` | the post for the caller | the post with its free portion, and the gated body only for an entitled caller |
| `POST /api/posts/{id}/gate` | `{tier}` | the post with its new `gate_tier` |
| `GET /api/posts/{id}/projection` | `?tier=` | `{reach, projected_revenue, confidence, sufficient}` |
| `POST /api/posts/{id}/publish` | publish and store the edition | the post `{id, status, audio_key}` |
| `GET /api/posts/{id}/audio` | the stored audio edition stream | audio bytes for an entitled caller |
| `GET /api/tiers` | the seeded tiers | `{items}` |
| `POST /api/subscriptions` | `{tier, offer_code}`, optional `Idempotency-Key` header | the subscription `{id, tier, status, amount_minor}` |
| `GET /api/subscriptions` | the caller's own subscription | `{items}` |
| `GET /api/subscribers` | `?page_size=&cursor=` | `{items, next_cursor, has_more}` of the audience |
| `GET /api/ledger` | `?page_size=&cursor=` | `{items, next_cursor, has_more}` of ledger entries |
| `POST /api/posts/{id}/release` | `{segment}` | `{resolved_recipients}` and the deliveries created |
| `GET /api/deliveries` | `?post_id=&page_size=&cursor=` | `{items, next_cursor, has_more}` |
| `GET /api/health` | readiness | `{ok: true}` |

Field names are exact. List endpoints return their rows under `items` with
`next_cursor` and `has_more`. Every business rule violation returns a client
error naming the reason, never a server error and never a silent success. Every
endpoint except signup, login, health and the public reads requires a valid
bearer token; an anonymous caller to a protected endpoint is rejected.

### No mocks

Posts, tiers, subscriptions, ledger entries and deliveries live in the real
PostgreSQL at `DATABASE_URL`, and every audio edition lives in the real MinIO
bucket at `STORAGE_ENDPOINT`, and nowhere else. An in memory list, a local file
store, a browser stored copy, or a grid rendered from client state that was never
persisted is a contract violation. A post that shows on screen but is absent from
Postgres, or whose edition is absent from the bucket, does not count. The named
provider is the fact: the app's UI and its own tables can only reflect what lives
in the provider, never substitute for it.

---

## Definition of done

The app is deployed and healthy. A stranger can sign in as the publisher, write a
post, set its paywall by moving the gate across the real audience with the
projected reach and revenue shown, publish it so its audio edition is stored, and
confirm that a paying subscriber can play the edition while a free reader and an
anonymous caller cannot. Subscribing once with one key creates exactly one
subscription and books one balanced ledger transaction, a discount resolves the
charged amount, and the ledger reconciles debits against credits. Every count and
figure shown matches the database.
