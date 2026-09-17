# Milo Rennick Brand Platform

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, see which race is next,
read a published story with its gallery, and subscribe for updates and confirm that
subscription, without hitting an error page. A different stranger must NOT be able to reach a
story the team has not published yet, or the photograph bytes behind one, by any means,
including a direct request to the route that serves those bytes. That boundary cannot be faked
in the app itself: the uploaded bytes must live in the `minio` bucket at their scheme's key, and
a copy kept on the app container's own disk does not count.

## Overview

Milo Rennick Brand Platform is the public brand property of a professional racing driver and the
editorial workspace the small management team runs behind it. Fans come for the next race, the
last result and the new photographs; the team writes stories, curates galleries, reconciles the
season feed and sends nothing without a person pressing send.

The public half is half magazine and half scoreboard. It carries the season calendar with its
session times, the career record, editorial stories with their galleries, a curated merchandise
strip and a link out to the storefront. It is deliberately not a fan community: there is no fan
account, no comment, no upload from the public and no messaging. The only fan identity is a
confirmed email address.

The hard part is the seam between the two halves. Unpublished editorial and its photograph bytes
must be unreadable to everyone but the signed-in team, on direct request and not only by
omission from a list; and the season data arriving from the timing feed must reconcile rather
than overwrite, so a retried delivery carrying an older classification can never move a final
result backwards on the public site.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `visitor` | Read published stories and their photographs, the season, the results, the profile, the partners and the merchandise strip. Subscribe. Send a business enquiry. | **Cannot read a story that is `draft`, `in_review`, `scheduled`, `unpublished` or `archived`, or the photograph bytes behind one. Cannot create, upload, publish, ingest or read either inbox.** |
| `contributor` | All of that, plus create a story, upload a gallery photograph, set alternative text, and submit a story for review. | **Cannot publish, cannot unpublish, cannot run an ingestion, cannot read the subscriber list or the enquiry inbox, cannot manage editors.** |
| `editor` | All of that, plus publish and unpublish, read every story in every state, read the enquiry inbox and the subscriber list, run an ingestion and record a manual override. | **Cannot manage editors, cannot read or write workspace settings.** |
| `owner` | Everything, including the editor list and the workspace settings. | **Cannot be created by signup.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a control in the UI
is not authorization: a direct API call from a lower role to any endpoint above its rung must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected
state unchanged.

Signup is open and always creates a `visitor`. The four seeded accounts all use the password
`deku-demo-pw-2026`: `owner@example.com`, `editor@example.com`, `contributor@example.com` and
`visitor@example.com`.

## Core features

### Editorial state and public visibility

1. A story's `state` is exactly one of `draft`, `in_review`, `scheduled`, `published`,
   `unpublished` or `archived`. Creating one always produces `draft`.
2. Public visibility is derived, never a column an editor sets: a story is public when its state
   is `published` and its `publishedAt` is not in the future. A `scheduled` story whose time has
   not arrived is absent from every public read and refused on direct request.
3. The public story list holds public stories only. A direct request for a non-public story by
   its public id is refused, not partially served.
4. Public order is `publishedAt` newest first. Against the shipped seed the public list holds
   `3 stories`; publishing a fourth makes it read `4 stories`.
5. Unpublishing is immediate: the story leaves the public list and its public id answers as not
   found rather than redirecting, because a redirect discloses that the record existed.

### Publishing a story

1. A contributor creates a story at its own address, `/studio/stories/new`, attaches gallery
   photographs, and submits it for review, which moves it to `in_review`.
2. Pre-publication validation runs before every publish. Publication is **blocked**, with a
   message naming the reason, when any of these is true. These are blocks, not warnings, because
   a warning that can be dismissed is a warning that will be dismissed.
   - a gallery photograph on the story carries no alternative text
   - a `quotation` on the story carries no attribution
   - the story references a round that is not in the current season
3. Publishing sets `state` to `published` and stamps `publishedAt` once. Publishing again changes
   nothing and is not an error.
4. A `slug` is unique. A create carrying a slug already taken is rejected as invalid and leaves no
   row and no object.
5. A public id is opaque and is never a sequential number. Two stories created one after the
   other carry public ids that cannot be reached from each other by counting. That is enumeration
   resistance: a visitor must not be able to walk the catalogue by incrementing an identifier, and
   must not be able to learn how much unpublished editorial exists by observing gaps. Internal
   identifiers may stay sequential; the two are distinct fields.
6. Concurrent editing is detected rather than lost, and concurrent-edit detection is at the record
   rather than at the field. An edit carries the `version` the editor
   loaded; an edit carrying a stale version is refused and says so, so a colleague's work is never
   silently overwritten.
7. Publication ordering is fixed and is the hazard this product is most likely to get wrong: the
   photographs are complete, then the record is published, then the public route is verified. A
   story is never announced anywhere before it is visible.

### The photograph boundary

1. One authenticated route on the app's own origin serves photograph bytes: for a photograph on a
   public story it answers anyone, for a photograph on any other story only a signed-in
   `contributor`, `editor` or `owner`.
2. An anonymous request for a `scheduled` story's photograph is denied, a signed-in `visitor`
   request for the same photograph is denied, and an `editor` request returns the bytes.
3. A denial returns no part of the object: no low-quality placeholder, no redirect to the store,
   no presigned link, and the object is untouched.

### Subscribing, and the confirmation that is not optional

1. The footer of every route carries a subscribe form of one email field with a visible label, a
   consent statement and a link to the privacy route.
2. A submission creates a subscriber at status `pending` and returns a single-purpose
   confirmation token. A pending subscriber is not a subscriber and is never counted as one.
3. Confirming with that token moves the subscriber to `confirmed` and stamps `confirmedAt`. The
   confirmation token confirms only: presenting it to the unsubscribe route does nothing.
4. Unsubscribing takes its own token, never expires, and changes state only on an explicit
   positive action, so a mail client that merely fetches the link cannot unsubscribe anyone.
5. A repeat submission for an address already known answers exactly as the first one did, with no
   statement about whether the address was already on the list.
6. Retention of the unconfirmed is bounded: a pending record that is not confirmed within the
   workspace's window is deleted rather than retained, because an unconfirmed address is not a
   subscriber and holding it is neither useful nor defensible.
7. An address in a `suppressed` state creates no pending record and receives no token, and answers
   with the same pending message as any other submission.

### The public pages every visitor can reach

1. A privacy page at `/legal/privacy-policy` is reachable from the footer of every route and
   states what the platform stores about a subscriber and an enquiry: the email address, the
   chosen topics, the consent record, and the name, organisation and message on an enquiry.
2. A terms page at `/legal/terms-conditions` is reachable from the footer of every route.
3. An unknown address renders the platform's own not-found route, with a `Back to the season`
   action, and answers as not found rather than as a page that exists.
4. Every internal link on every public route resolves. A link in the chrome, in the footer or in
   the body of a public story never lands on the not-found route.
5. Every public route carries its own title and description and no two public routes share them.
   Addresses are lowercase and hyphen-separated with no trailing slash except the site root, and a
   request carrying a trailing slash or mixed case redirects permanently to the canonical form.
   Every route emits a canonical link and a social preview set, and a structured-data block
   describes the athlete on the home route and the sporting events on the calendar, generated from
   the same records that render the page.
6. A maintenance state exists and reads `Back shortly. We are making a change.` rather than a
   server error page.

### Abuse control on the public write surfaces

The subscribe form and the enquiry form are the only two places an unauthenticated visitor changes
server state, so they are the whole of the public attack surface. Both are protected by a layered
scheme in which no single layer is a visible burden on a legitimate visitor: a decoy field hidden
from people but present to naive automation, whose completion silently discards the submission; a
minimum elapsed time between the form being rendered and submitted, below which the submission is
discarded; a signed, expiring token issued with the form and required at submit, which is also the
cross-site request forgery protection; and a rate limit per address and per calling origin. A
challenge is presented only on the enquiry form and only when the preceding layers have scored a
submission as suspicious, because a challenge in front of every subscribe box costs more
legitimate subscribers than it saves in spam.

Every field is validated at the server against one declared schema which is also the source of the
client's rules, so the two cannot drift. The server normalises before validating: it trims, it
collapses internal whitespace, it lowercases the address domain, and it rejects rather than
silently strips a control character. It rejects any field absent from the schema rather than
ignoring it, and bounds every string and the whole request body. On the enquiry form the name must
be non-empty after trimming and length-bounded, and the message is length-bounded at both ends,
since a two-character enquiry is not one. The organisation is optional and length-bounded. The
consent box is never pre-checked and must be explicitly ticked.

## Season data and the feed

1. The public site never waits on the timing provider. Every ingested value is persisted locally
   and served from local storage on a visitor request.
2. The feed is treated as an untrusted, occasionally wrong external system. Every payload is
   validated against a declared schema and a malformed response is rejected rather than persisted,
   and the raw payload of every run is retained for a bounded window so a wrong figure on the
   public site can be traced to what arrived.
3. Idempotency and ordering are the two properties this seam lives or dies on. An ingestion run is
   submitted by an `editor` or an `owner` and carries a `runId` and a list of entities. Applying
   the same `runId` twice produces the same result: the second run applies nothing and reports
   itself as a duplicate.
3. Every ingested entity carries the provider's own `providerUpdatedAt`. An entity is applied only
   when that instant is newer than what is stored. An out-of-order delivery is counted as
   superseded and changes nothing, so a provisional classification arriving after the final one
   can never move a result backwards.
5. Ingestion is a reconciliation, never an overwrite. Every incoming record is classified as
   unchanged, changed, new or missing. A round present locally and absent from the payload moves to
   `missing_review` for a person to look at, because a truncated payload is far likelier than a
   genuinely deleted season.
6. A field carrying an active manual override is never overwritten. The run records the clash as a
   conflict and leaves the override value standing, because the provider is sometimes wrong and the
   team sometimes knows better.
7. Concurrent runs are prevented by a lease. A manual refresh submitted while a run is in flight is
   refused rather than interleaved with it.
8. The next round is the earliest round whose `endsAt` is still ahead and whose state is neither
   `complete` nor `cancelled`. A completed round is never presented as upcoming, at any layer.
   These are the correctness rules the whole property is judged on, and they are computed on read.
9. A session time is stored as an absolute instant and is rendered with the name of the zone it is
   being shown in. The calendar offers the circuit's own zone as the alternative.
10. Inside a round's weekend window the next-race card carries a countdown to the next session
   start. The countdown is announced politely at meaningful thresholds rather than on every tick,
   and it disappears rather than counting past zero.
11. Where a figure is older than its freshness budget the surface states when it was last
   confirmed. A freshness budget is a workspace setting, not a constant in the code.
12. An ingestion entity carries a `type` of `round`, `session`, `classification` or `standing`,
   the `roundNumber` the entity belongs to, a `providerUpdatedAt` instant, plus the fields of its
   own type. A `classification` entity also carries `sessionKind`, `position`, `status` and
   `provisional`. A `round` entity also carries `state`. An entity of an unknown type is rejected
   as invalid rather than ignored.
13. The ingestion response reports `applied`, `superseded`, `conflicted` and `missing` as counts,
   and `duplicate` as a boolean that is true only for a replayed `runId`. A run whose payload
   omits a `type` on any entity is rejected as invalid, applies nothing, and records no run.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the brand entry point, the next-race card and the story teasers | public |
| `/on-track` | the record: statistics, career results, standings | public |
| `/off-track` | the person: topics, galleries, quotations | public |
| `/calendar` | the season, upcoming and past, with session times | public |
| `/stories/:public_id` | one published story with its gallery | public |
| `/legal/privacy-policy`, `/legal/terms-conditions` | the legal texts | public |
| `/subscribe/confirm`, `/subscribe/unsubscribe` | the two token landings | public |
| `/login`, `/signup` | sign in, registration | public |
| `/studio` | the workspace dashboard | contributor |
| `/studio/stories`, `/studio/stories/new` | the story list and the create address | contributor |
| `/studio/media` | the gallery library and alternative text | contributor |
| `/studio/calendar` | ingestion runs and overrides | editor |
| `/studio/enquiries`, `/studio/audience` | the two inboxes | editor |
| `/studio/settings` | editors, roles and workspace settings | owner |

**Entry and redirects.** An unauthenticated `/studio` request goes to `/login`, and sign in lands
on the route asked for. A signed-in `visitor` there is refused with a message, not looped back.
After login a `contributor`, an `editor` or an `owner` lands on `/studio`, a `visitor` on `/`.
Logout discards the token. An expiry mid-action refuses the action and returns to `/login`. An
unknown or non-public story id at `/stories/:public_id` shows the not-found route.

**Journeys.**

1. Open `/`: the next-race card reads `Sundown`, round `04`, with the constructor `Halcyon` and
   the debut year `2019` on its standing line. The teaser strip carries `3 stories`. Follow one
   into `/stories/:public_id` and the gallery renders with captions in the place-comma-year form.
2. Open `/calendar`: six rounds for the `2026` `Prime One` season, three of them complete. The
   featured panel carries `Sundown` with its date range, circuit length, lap count and first year
   competed, and a schedule table of that round's sessions with the zone they are shown in named.
   Toggle to the visualiser and back; the mode is in the address, so the view can be shared.
3. Subscribe from the footer with a new address. The form is replaced in place by a message
   telling the visitor to check their email, and the response carries a confirmation token.
   Confirm at `/subscribe/confirm`; the subscriber becomes `confirmed`. Submit the same address
   again and the identical pending message appears.
4. Sign in as `editor@example.com` with `deku-demo-pw-2026`. `/studio/stories` lists six stories
   across every state. Publish `What Sundown Asks For`; signed out, `/` now reads `4 stories`.
5. Sign in as `contributor@example.com`, create `The Long Way Round` at `/studio/stories/new`,
   attach a photograph, submit for review, then try to publish and be refused as a contributor.
6. Signed out, `/stories/2a9b7f31c8` is not found and its photograph route denied. As
   `visitor@example.com` the photograph is still denied; as `editor@example.com` it is served.
7. Open the menu overlay, send a business enquiry with name, email, enquiry type, message and the
   consent box ticked, and read back the reference `ENQ-00001` from the confirmation. Leave the
   organisation blank and it still sends; leave the message blank and the submission is refused
   with an error summary naming the field.

**States.** Every list has an empty state naming what is missing, every route a loading state. A
rejected submission keeps what was typed and names the field at fault. Where a figure is older
than its freshness budget the surface says when it was last confirmed rather than showing a
stale number as if it were current. No error leaves a blank page.

## UI/UX notes

An editorial property wrapped around a live scoreboard: slow, hand-made, art-directed pages that
must carry race information which has to be right within seconds of a chequered flag. The voice
is plain and confident, never breathless, and the one place the design raises its voice is the
next-race card, which is the most load-bearing thing on the site.

Type is two voices. A variable grotesque carries everything structural: navigation, statistics,
tables and body copy, tight and industrial with wide apertures. A high-contrast display serif
carries pull-quotes, single accent words inside sans headings, and the second line of every split
heading. That split heading, its first line in the grotesque at high weight and its second in the
serif at the same optical size, is the signature typographic device and appears on the calendar
hero, the off-track hero and the impact statements. It is required, not decorative.

Ground alternates by route and that alternation is the primary structural signal a reader gets.
The light routes sit on a near-white neutral with a warmer near-white neutral for editorial
sections; the on-track and calendar routes sit on a near-black neutral; the menu overlay and the
footer sit on a deep neutral. The accent is one mid, vivid lime and it is never diluted: there is
no tint ramp, and where it must recede it changes to its resting form, a second mid, vivid lime,
or drops to nothing. A mid, vivid orange is the secondary accent and appears only on alert and
warning states; a light, vivid red belongs to the error surface and appears nowhere else. Light
neutrals and a light warm neutral carry captions, dividers and secondary text, and the deep and
mid neutrals carry raised surfaces and rules on the dark routes.

Nothing steps and everything scales: on the wide layouts every typographic and spatial value
derives from one clamped viewport ratio rather than from a breakpoint ladder, so a layout drawn
once holds its proportions across the whole desktop range. Rendered sizes are therefore not round
numbers, and that is correct.

Motion is one long, hard, late-settling ease carrying almost everything, with a small set of
named exceptions rather than a curve invented per component. Headings reveal line by line on a
wipe from the left with a per-line stagger; photographs enter on a mask that opens; the pinned
photograph track and the oval composition scrub against scroll rather than firing at a single
trigger; the accent stroke draws itself across the hero. Under a reduced-motion preference every
travel collapses to a cross fade in place, the scrubbed compositions settle at their resting
frame, and nothing that carries information is lost.

Accessibility is contract, not taste: contrast meets WCAG AA against the ground in every state
including mid-transition frames, keyboard navigation reaches every calendar row and every gallery
item with a visible focus ring, every photograph carries alternative text, the failed enquiry
raises an error summary at the top of the form that moves focus to itself and links to each
field, and the submit control is never disabled for being invalid. Meaning is never by colour
alone.

The layout is top-nav with a centre monogram and a persistent store button top right; the work
surfaces are card grids, and the reading routes sit in a centred column with generous gutters.
Each route leads with one clear primary action, visually distinct from every secondary one. At a
phone width the navigation collapses into the menu overlay, the calendar list becomes the default
mode, nothing overflows sideways and every navigation target stays reachable.

## Technical requirements

The frontend is **Angular**. The backend is **Fastify**. The rendering model is a single-page
application over a JSON API: the browser receives an application shell on first paint and every
route's content arrives as JSON from the same origin. The server renders no page HTML.

Both halves install from the public npm registry at image build time and run on the Node 20
runtime the environment image already carries.

Storage is **PostgreSQL**, reached at `DATABASE_URL`. Object storage is **MinIO**, S3 compatible,
reached at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and
`STORAGE_SECRET_KEY`. Both are already running in this environment. Read every host and
credential from the environment; never hardcode one.

Auth is app-implemented email and password, stored hashed, with bearer tokens. Login returns
`access_token`, which the client sends as `Authorization: Bearer <access_token>` on every request except login, signup
and health. A token expires after 24 hours and an expired token is refused. Signup is open and
always produces a `visitor`; the three team roles are seeded. There is no password reset and no
external identity provider.

`GET /api/health` returns `200` with a JSON body once the app is ready. Request logging is
structured to stdout, one line per request carrying method, path, status and duration, and never
a password, a token or object bytes.

Every photograph and every derivative lives in `minio` and nowhere else. Protected bytes are
served through an authenticated streaming route on the app's own origin rather than by handing
out presigned URLs, so one route owns the visibility decision for every object. Apply that one
mechanism consistently.

Every response is shaped by an explicit field allowlist per resource and per audience. No public
response carries a provider identifier, an author identifier, a revision, a scheduling time, a
subscriber field or an enquiry field. No serialiser returns a record by spreading its stored row,
and no relation is included unless the allowlist for that audience names it.

Scoping is structural, not remembered. Every read and every write carries the visibility scope it
is entitled to, so a query that forgets returns nothing rather than everything. Four leaks this
closes, each of them a realistic failure of this product: draft editorial served publicly because
a public read did not filter on state and publication time; a subscriber address reaching a public
response because a serialiser included a related record without an allowlist; an enquiry body
reaching a public surface for the same reason; and draft editorial reaching a warmed public
response because the job that warmed it did not carry the scope. The fourth is the dangerous one,
because the request never reaches the authorization decision at all.

Sign-out destroys the server-side session rather than only clearing the cookie, and revocation is
immediate: an owner can revoke every session belonging to any team account, and a password change
revokes every other session for that account while keeping the current one. A session identifier
is regenerated on sign-in and on any change of role.

Cross-site request forgery is closed by the signed, expiring form token above, and content safety
by rejecting a document tree carrying any node type outside the declared schema rather than by
escaping on the way out. Rate limits apply per address and per calling origin on the two public
write surfaces, on login and on the ingestion endpoint; a read of public season data is not rate
limited, because rate limiting a race-weekend crowd is the failure rather than the defence.

An audit trail records every publish, unpublish, override, ingestion run, role change and audience
export, with the account, the instant and the record. Logs carry a request identifier so one
request can be followed end to end, errors are aggregated rather than only printed, and an
ingestion run that exceeds its freshness budget raises an alarm on the workspace dashboard.

Nothing the browser downloads carries a credential: no database password, no object-store access
key or secret, and no bearer token belonging to a seeded account appears in any served script,
stylesheet, document or JSON payload.

Every response carries the standard security headers, including a strict transport policy and a
nosniff content-type policy.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing
services available in this environment are `postgres` and `minio`, and reaching for anything else
is a contract violation.

## Data model

Nine tables. All timestamps are UTC and carry a zone.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not
a secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

### `users`

`id` integer primary key, `email` text unique, `password_hash` text, `role` text restricted to
`owner`, `editor`, `contributor` or `visitor`, `created_at` timestamptz.

### `rounds`

`id` integer primary key, `number` integer unique within the season, `name` text, `circuit` text,
`country` text, `starts_at` timestamptz, `ends_at` timestamptz, `state` text restricted to
`scheduled`, `in_progress`, `complete`, `cancelled`, `postponed` or `missing_review`, `laps`
integer, `distance_km` numeric, `length_km` numeric, `first_competed_year` integer,
`provider_id` text, `provider_updated_at` timestamptz.

`ends_at` is always after `starts_at`. `distance_km` and `length_km` are fixed precision, never
floating point.

### `sessions_slots`

`id` integer primary key, `round_id` integer, `kind` text restricted to `practice`, `qualifying`,
`sprint` or `race`, `label` text, `position` integer, `starts_at` timestamptz, `time_confirmed`
boolean, `state` text restricted to `scheduled`, `in_progress`, `complete` or `cancelled`,
`provider_updated_at` timestamptz.

### `classifications`

`id` integer primary key, `round_id` integer, `session_slot_id` integer unique, `position`
integer nullable, `status` text restricted to `classified`, `retired`, `disqualified`,
`did_not_start` or `did_not_qualify`, `time_ms` bigint nullable, `gap_text` text nullable,
`points` numeric, `constructor` text, `provisional` boolean, `source` text restricted to
`provider` or `manual`, `provider_updated_at` timestamptz.

Observable invariant: a classification carrying a numeric `position` has status `classified`. A
retirement, a disqualification and a non-start are distinct states and are never collapsed into
one another or into an empty position. An update whose `provider_updated_at` is not newer than the
stored one is not applied.

### `standings`

`id` integer primary key, `after_round_id` integer, `position` integer, `points` numeric,
`provider_updated_at` timestamptz.

### `field_overrides`

`id` integer primary key, `entity_type` text, `entity_id` integer, `field` text,
`original_value` text, `override_value` text, `editor_id` integer, `created_at` timestamptz,
`released_at` timestamptz nullable. At most one active override per `entity_type`, `entity_id`
and `field`.

### `stories`

`id` integer primary key, `public_id` text unique, `slug` text unique, `type` text restricted to
`story`, `topic`, `quotation` or `legal`, `title` text, `body` text, `attribution` text nullable,
`state` text restricted to `draft`, `in_review`, `scheduled`, `published`, `unpublished` or
`archived`, `published_at` timestamptz nullable, `scheduled_for` timestamptz nullable,
`author_id` integer, `round_id` integer nullable, `version` integer, `created_at` timestamptz.

`public_id` is opaque: it is not derived from `id` and cannot be reached from another public id
by counting. `published_at` is stamped the first time the story becomes `published` and is never
rewritten. `version` rises on every edit, and an edit carrying a stale version is refused.

Observable invariant: a story's `slug` is unique across the whole table, and that holds under
concurrent creates rather than only in application-level checks. Two simultaneous creates of the
same slug must not both succeed: exactly one wins, the other is rejected, leaving no orphaned row
and no orphaned object. The same holds for an ingestion `run_id` and for an active override on a
given entity, type and field: a second arrival is refused rather than racing the first.

### `assets`

`id` integer primary key, `story_id` integer nullable, `storage_key` text, `content_hash` text,
`width` integer, `height` integer, `alt_text` text nullable, `caption_place` text,
`caption_year` integer, `position` integer, `derivative_state` text restricted to `pending`,
`complete` or `failed`, `created_at` timestamptz. `storage_key` holds the object key, never the
bytes.

### `subscribers`

`id` integer primary key, `email` text unique, `status` text restricted to `pending`,
`confirmed`, `unsubscribed` or `suppressed`, `topics` text array, `confirm_token` text unique,
`unsubscribe_token` text unique, `consent_source` text, `consent_at` timestamptz, `confirmed_at`
timestamptz nullable, `unsubscribed_at` timestamptz nullable.

### `enquiries`

`id` integer primary key, `reference` text unique, `name` text, `email` text, `organisation` text
nullable, `enquiry_type` text restricted to `partnership`, `media`, `appearance` or `other`,
`message` text, `consent` boolean, `created_at` timestamptz.

`reference` is derived from the id at insert and then stored so it can be quoted back: `ENQ-`
followed by the id zero padded to five digits.

### `ingest_runs`

`id` integer primary key, `run_id` text unique, `applied` integer, `superseded` integer,
`conflicted` integer, `missing` integer, `created_at` timestamptz.

**Derived rather than stored:** the public story count, the next round, the driver's age from the
date of birth on the profile, the championship position ordinal suffix, and the career aggregates
on the on-track route.

### Seed data

Accounts: `owner@example.com` as `owner`, `editor@example.com` as `editor`,
`contributor@example.com` as `contributor`, `visitor@example.com` as `visitor`. All four use
`deku-demo-pw-2026`.

Six rounds of the `2026` `Prime One` season. The first three are seeded to instants already past
at seed time and the last three to instants still ahead of it, computed when the seed runs, so
the season is always half run:

| number | name | circuit | country | state |
|---|---|---|---|---|
| `01` | Verano Grand Prix | Verano | Costa Verde | complete |
| `02` | Kestrel Bay Grand Prix | Kestrel Bay | Marisol | complete |
| `03` | Aldenne Grand Prix | Aldenne | Valmont | complete |
| `04` | Sundown Grand Prix | Sundown | Ardenia | scheduled |
| `05` | Port Mira Grand Prix | Port Mira | Lucaya | scheduled |
| `06` | Caldera Grand Prix | Caldera | Ferrante | scheduled |

Each round carries four session slots, `practice`, `qualifying`, `sprint` and `race`, in that
order. Each of the three complete rounds carries one `race` classification with status
`classified` and a numeric position, `provisional` false and `source` `provider`.

Six stories, three of them public:

| public_id | slug | title | type | state |
|---|---|---|---|---|
| `9f3c1a7d42` | `recovery-drive-at-verano` | Recovery Drive at Verano | story | published |
| `4b82e05c17` | `two-tenths-at-kestrel-bay` | Two Tenths at Kestrel Bay | story | published |
| `d15a6f9b30` | `the-aldenne-long-run` | The Aldenne Long Run | story | published |
| `7e0d4c82a6` | `what-sundown-asks-for` | What Sundown Asks For | story | scheduled |
| `2a9b7f31c8` | `the-winter-programme` | The Winter Programme | story | draft |
| `b63e18a70f` | `off-season-in-the-workshop` | Off Season in the Workshop | story | in_review |

Every seeded story, including the three that are not public, carries at least one real photograph
object in `minio` under `assets/{asset_id}/{sha256_of_bytes}.{ext}`, generated procedurally at
seed time. A non-public story's photograph therefore exists and is refused, rather than merely
being absent. The photograph on `the-winter-programme` carries no `alt_text`, so publishing that
story is blocked until one is set. One seeded `quotation` carries no `attribution`, so publishing
it is blocked for that reason.

One `profile` record behind the statistic strips: nickname `Milo`, monogram `MR`, constructor
`Halcyon`, series `Prime One`, debut year `2019`, home town `Bracken Hill`, home country
`Ardenia`.

Four merchandise items in the curated strip, one of them explicitly sold out and one carrying a
price older than its freshness budget, which is shown without a price rather than with the stale
one. Three partner marks, named by category only: `title`, `technical` and `official`.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Constraints

One brand, one workspace, one production environment. There is no fan account, no profile, no
saved item, no comment and no user-generated content of any kind, therefore no moderation queue.
No storefront reimplementation: no cart, no inventory, no tax, no fulfilment and no card capture.
No live telemetry and no lap-by-lap timing screen. No federated sign-on, no permission scheme
beyond the four roles above, and no approval chain crossing more than the single review step. No
email is sent by this app; subscription confirmation and unsubscription travel as tokens the API
returns and two public routes consume, and enquiries are read in the workspace. No external
network calls at run time, and a visitor request never fans out to the timing provider. No
analytics vendor and no third-party tag. No binary asset ships with the build: every photograph,
icon, circuit outline and three-dimensional form is generated in code. The app must stay
responsive with a season of 500 rounds and 5,000 stored subscribers.

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
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{ email, password }` | `{ access_token, role }`, role always `visitor` |
| `POST /api/auth/login` | `{ email, password }` | `{ access_token, role }` |
| `GET /api/health` | none | `{ status }` |
| `GET /api/stories` | none | top-level JSON array of public stories, each `{ publicId, slug, title, type, body, publishedAt, assets }` |
| `GET /api/stories/count` | none | `{ count }`, public only |
| `GET /api/stories/:public_id` | none | one story object |
| `GET /api/assets/:asset_id/file` | none | the photograph bytes |
| `GET /api/season` | none | `{ year, series, rounds }` |
| `GET /api/season/next-round` | none | `{ number, name, circuit, country, startsAt, endsAt, state, laps, distanceKm, lengthKm, firstCompetedYear, sessions }` |
| `GET /api/results` | none | top-level JSON array of classifications, each `{ roundNumber, roundName, position, status, timeMs, gapText, points, constructor, provisional }` |
| `GET /api/standings` | none | `{ position, points, afterRoundNumber }` |
| `GET /api/profile` | none | `{ nickname, monogram, constructor, series, debutYear, homeTown, homeCountry }` |
| `GET /api/merch` | none | top-level JSON array, each `{ title, price, currency, availability, url }`, the price displayed in the currency the platform reports with no local conversion, since a converted price the checkout will not honour is worse than a foreign one |
| `GET /api/partners` | none | top-level JSON array, each `{ category, tier, order }` |
| `POST /api/subscribers` | `{ email, topics }` | `{ status, confirmToken, unsubscribeToken }` |
| `POST /api/subscribers/confirm` | `{ token }` | `{ status }` |
| `POST /api/subscribers/unsubscribe` | `{ token }` | `{ status }` |
| `POST /api/enquiries` | `{ name, email, organisation, enquiryType, message, consent }` | `{ id, reference }` |
| `GET /api/studio/stories` | none | top-level JSON array of every story in every state |
| `POST /api/studio/stories` | `{ slug, title, type, body, attribution }` | the created story, `state` `draft` |
| `POST /api/studio/stories/:public_id/assets` | multipart, field `file` | `{ assetId, storageKey }` |
| `PATCH /api/studio/assets/:asset_id` | `{ altText }` | the asset |
| `POST /api/studio/stories/:public_id/submit` | none | the story, `state` `in_review` |
| `POST /api/studio/stories/:public_id/publish` | none | the story, `state` `published` |
| `POST /api/studio/stories/:public_id/unpublish` | none | the story, `state` `unpublished` |
| `POST /api/studio/ingest` | `{ runId, entities }` | `{ runId, applied, superseded, conflicted, missing, duplicate }` |
| `GET /api/studio/ingest/runs` | none | top-level JSON array of runs |
| `POST /api/studio/overrides` | `{ entityType, entityId, field, overrideValue }` | the override |
| `GET /api/studio/enquiries` | none | top-level JSON array of stored enquiries |
| `GET /api/studio/subscribers` | none | top-level JSON array of subscribers |
| `GET /api/studio/editors` | none | top-level JSON array of team accounts |

Field names are exact. Bearer auth is required on everything except `POST /api/auth/login`,
`POST /api/auth/signup` and `GET /api/health`; every `GET` outside `/api/studio`, plus
`POST /api/subscribers`, `POST /api/subscribers/confirm`, `POST /api/subscribers/unsubscribe` and
`POST /api/enquiries`, also accept an anonymous caller. A successful call returns the named shape;
an invalid or unauthorized call is rejected as a client error, never a `5xx` and never a silent
success.

### No mocks

An in-memory `objects` map holding uploaded bytes, photograph bytes written to the app
container's filesystem, a database column carrying base64 image data, a hardcoded
`{"uploaded": true}` response the app returns to itself, or a season served from a JSON file
checked into the repository are all contract violations however good the interface looks. `minio`
is the fact and `postgres` is the fact: the app's UI and its own tables can only reflect what
lives in the provider, never substitute for it.

## Front-end specification

This section carries the measured visual, motion and interaction detail the product is built to.
Values here are contract.

Two registers run through it. A statement of what the product must do is **normative** and is a
requirement. A statement of what was observed in the reference property is **informational**,
offered as evidence of intent rather than as an instruction, and the build is free to satisfy the
requirement by any means that holds the stated character. Where a paragraph carries no marker,
read it as normative.

Six audiences read the finished property and the design answers to all of them: fans arriving
from a social post on a handset with one question, subscribed fans who also want the email,
buyers heading for the store, commercial enquirers looking for the management team, the editors
working in the workspace, and the ingestion run itself.

### The scaling model

One drawing, made at a fixed design width on a fixed base unit, multiplied by a ratio derived
from the viewport and clamped at both ends, below which the ratio stops shrinking and above which
it stops growing. Every typographic and spatial value on the wide layouts derives from that one
clamped ratio, so a layout drawn once holds its exact proportions across the whole desktop range
without a single redraw. A global multiplier is exposed so the whole drawing can be scaled at
once. Three consequences the build must not fight: rendered sizes are irrational and are outputs
rather than inputs, so they are never rounded into a step scale; the root size is not the same at
every width, so a rem inside the scaled container means a multiple of the fluid unit; and a
design change is a change to the drawing, never to a breakpoint. Below the narrow threshold the
model is abandoned and the responsive section takes over.

### Colour tokens

The brief names each colour by family, tone and shade; the exact value is the builder's to
choose, so long as it lands in the band named and holds the exclusivity rules below.

| Token | Colour | Role |
|---|---|---|
| `--ground-light` | a near-white neutral | the dominant light ground, and not white |
| `--ground-cream` | a near-white warm neutral | a warmer light ground for editorial sections |
| `--panel-light` | a near-white neutral, a step below the ground | light panel fill |
| `--tone-mid-light` | a near-white neutral, the workhorse | the mid-light tone and the navigation text shadow |
| `--divider-light` | a light neutral | divider and disabled tone |
| `--caption-light` | a light neutral, the darkest of the light family | captions on light grounds |
| `--secondary-dark` | a light warm neutral | secondary text on the dark routes |
| `--ground-dark` | a deep neutral | the dominant dark ground, and not black |
| `--raised-dark` | a deep neutral, one step above the ground | raised surface on dark |
| `--divider-dark` | a mid neutral | divider on dark |
| `--ground-black` | a near-black neutral | the reserved true black, the deepest grounds and the calendar |

Accent palette, state only. Each appears in its named role and nowhere else.

| Token | Colour | Role |
|---|---|---|
| `--accent` | a mid, vivid lime | the single accent: signature, store button, statistics, highlighter |
| `--accent-rest` | a mid, vivid lime, one step muted | the accent at rest, or over a photograph |
| `--accent-zero` | the accent at zero alpha | the start stop of the footer gradient |
| `--warning` | a mid, vivid orange | the secondary accent, used sparingly for alert and warning states |
| `--error` | a light, vivid red | the error surface family, and it appears nowhere else |

Two further values carry meaning and are not tokens: the dark ground at low alpha, used for the
contour pattern drawn over light grounds, and the accent at zero alpha above.

**The rule that governs the palette.** The accent is a single colour and it is never diluted.
There is no accent-light, no accent-dark and no tint ramp. Where the accent must recede it
changes to its resting form or drops to nothing, and that is the whole vocabulary. A build that
introduces a five-step accent ramp will look immediately wrong.

### Ground assignment per route

| Surface | Ground | Body text | Secondary text | Accent |
|---|---|---|---|---|
| Home, upper | `--ground-light` | `--ground-dark` | `--caption-light` | `--accent` |
| Home, editorial | `--ground-cream` | `--ground-dark` | `--caption-light` | `--accent` |
| On Track | `--ground-black` | `--ground-light` | `--secondary-dark` | `--accent` |
| Off Track | `--ground-cream` | `--ground-dark` | `--caption-light` | `--accent` |
| Calendar | `--ground-black` | `--ground-light` | `--secondary-dark` | `--accent` |
| Menu overlay | `--ground-dark` | `--ground-light` | `--secondary-dark` | `--accent` |
| Footer | `--ground-black` | `--ground-light` | `--secondary-dark` | `--accent` |
| Legal | `--ground-light` | `--ground-dark` | `--divider-dark` | `--accent` |

The navigation chrome inverts against whatever it sits over, by one blend treatment plus a class
swap at measured thresholds, never two copies of the bar.

### Contrast obligations

Three pairings are known to be tight and are handled deliberately rather than adjusted. The
accent is a high-luminance yellow-green, so the store button's label is set in the dark ground
colour and never in the light one. The darkest light-family tone on the warmer light ground is
permitted only at the caption role, which is uppercase and letterspaced, and never for body copy.
The light warm neutral on the true black passes at body size and its size is never reduced below
the caption role. Text meets the normal-size contrast threshold against its own ground in every
state, including the transient frames of a reveal, where a mid-transition frame must never be the
only frame in which text is legible.

### Type

Two families. Everything structural is set in a variable grotesque across a wide weight axis,
tight and industrial with wide apertures, carrying navigation, statistics, tables and body copy.
The display accent is a high-contrast display serif at a heavy weight, used for pull-quotes, the
second line of a split heading, and single accent words inside a sans heading. Both are declared
with a swap display strategy and both carry a normative fallback stack so the art-directed line
lengths hold before a licence is in place.

The ramp, by role: an impact display and a secondary impact display for the route heroes; a menu
overlay link at three widths; a section heading; a heading; a serif pull-quote; a footer button
label at two widths; body large; a navigation button label at two widths; body regular; the base
rendered size, which is by a wide margin the most common; a primary button label at three widths;
and a caption. Figures align wherever numbers stack, which on this property is most places.

### The eyebrow and the caption

The eyebrow is the smallest structural role on the site: uppercase, letterspaced, set in the
grotesque, and it labels every card slot, every statistic and every gallery photograph. A gallery
caption is an eyebrow in the place-comma-year form, set above the photograph and flush left with
its edge.

### Global chrome

The chrome is fixed on every route: a bar pinned to the top carrying the wordmark left, the
monogram centre, and the store button top right; a menu overlay that opens over any route; and a
footer at the end of scrolling content.

**The store button.** Persistent, top right, on every route. It is a plain cross-origin link to
the storefront carrying the correct rel attributes, opening in the same tab, propagating a
referral parameter so the storefront can attribute the visit. It never depends on a live call to
the commerce platform: it must still work when that platform is down, because the platform's own
error page is a better outcome than a button that does nothing.

**The menu overlay.** Four destinations and the business-enquiries surface, set as oversized
links in the grotesque on the deep neutral ground. It does not create a history entry, so the
browser back button leaves the site rather than closing the overlay, which is the correct
behaviour for a transient layer. It traps focus while open and returns focus to the control that
opened it.

**Nav inversion.** The bar reads over both the light and the dark grounds, so its marks invert
against whatever sits under them. The inversion is one blend treatment plus a class swap at
measured scroll thresholds, never two copies of the bar.

**Buttons and the duplicate-glyph roll.** A primary button carries its label twice, one copy
stacked above the other inside a clipped frame; on hover and on focus the pair rolls so the second
copy takes the first one's place. It is the same device at every button size and it is the only
label transition on the site.

**The chevron.** One chevron glyph, drawn as inline geometry, serves every direction: down on the
scroll hint, right on a tertiary control, and rotated in place rather than redrawn per direction.

**The rotate-device prompt.** In a short landscape viewport the calendar visualiser shows a prompt
asking the reader to rotate the device, because the drawing cannot hold its proportions there. The
prompt is dismissible and the list mode stays reachable behind it.

**The footer.** The subscribe form, the social row, the legal links, the partner line and the
accent gradient that begins at the accent's zero-alpha stop. Footer links carry an animated
underline built from two layers that swap on hover.

### The next-race card

A small portrait card pinned to the lower left of the home hero, and the single most load-bearing
piece of live data on the site. Five rows: an eyebrow reading as the next-race label; a circuit
outline drawn in stroke, per round; the circuit or round name with the round designation; a rule;
and a laurel mark above a two-line standing statement naming the constructor and the debut year.
It is populated from the next-round query and never from a stored flag. Where the figures behind
it are older than their freshness budget it states when they were last confirmed rather than
presenting a stale figure as current.

### Route detail

**Home.** A sequence of compositions rather than a page of sections, in this order: the hero with
the three-dimensional helmet and the next-race card on the light ground; a split-family statement
revealed line by line; a pinned horizontal photograph track on the warmer ground; a portrait
composition rendered with real depth; a scattered gallery collage with eyebrow captions; a signed
pull-quote; the oval, a full-bleed line composition on a clip scrub; the on-track and off-track
split gateway; the livery grid on true black; a partner marquee; a social callout card; and the
footer. There is no headline in the visible layer: the heading exists in the document as a
visually hidden pair, the driver's name at first level and the season and role at second.

**On Track.** Dark ground throughout and the densest data surface on the site. The hero is an
oversized split-family title with a handwritten accent stroke breaking out of the viewport on the
left, and a reserved spacer beneath the fixed bar so the cap height cannot collide with it. Then a
statistic strip of three items on one baseline, a nickname, an age and a home town with a flag
chip, each an eyebrow revealed on a wipe with a per-item stagger, the age derived from the date of
birth so it cannot go stale. Then a statement paragraph with a serif accent line. Then the race
context cluster of four cards: previous round, next round, circuit and standing, the previous card
visually recessed relative to the next, complete in the first viewport after the hero at every
width. Then the career statistics, the results table of every classified finish in reverse
chronological order, a podium gallery with a signed pull-quote, and the footer.

**Off Track.** The warmer light ground, and the route for the person away from the car: lifestyle,
personal projects and interests. Topic sections alternate side by side, each a name, a description
and a gallery collage, ordered and sided from the record rather than from the template. The seeded
topics are `Padel tennis`, a court kept sharp away from the circuit, and `Music`, a long-running
playlist added to on every flight. A signed pull-quote carries the highlighter treatment in the
accent, and the home quotation reads `I started in a kart at seven years old, and I have been
chasing the same feeling ever since.`

**Calendar.** True black, the most data-dense route, and the one with two view modes. The hero is
a two-line split-family title, the second line carrying the season year rendered from the current
season record and never from a template literal, with a large handwritten accent stroke scrawled
across both lines. Then a header bar: a two-line summary of the season state revealed per line;
the standing as an eyebrow above a large numeral with a superscript ordinal; the round as an
eyebrow above a large numeral; and two controls, the visualiser and the list. Then the featured
round panel, bordered in the accent, carrying the next round in full: the circuit name set
vertically at impact scale on the left edge with the country flag chip beneath it; a when-label
above the date range and month; the circuit length and the first year competed; the race distance
and the lap count; and on the right an eyebrow naming the driver and circuit, a short editorial
note, and the schedule table. Large numerals in the panel are set in the accent and the month in
the light ground colour.

**The schedule table and the timezone rule.** Each row is a session name in uppercase, a day and
abbreviated month, and a local start time on a 24-hour clock. Session times are stored as absolute
instants, rendered in the visitor's own zone by default, and the surface always displays which
zone it is showing. A control offers the circuit's own zone as the alternative. Two cases must
behave correctly: a session that crosses midnight in the visitor's zone, and a session that falls
inside a daylight-saving transition in either zone.

**The two view modes.** The list is the season as rows; the visualiser is the circuit outline
drawn at scale with its annotations. The two modes create history entries and are reflected in the
address, so a reader can share a link to the visualiser rather than the list.

**The track visualiser.** A single circuit outline drawn from a stored two-dimensional path,
scaled to its frame, with annotations placed at a normalised distance along the lap and a
collision rule that drops the lower-priority label when two would overlap. The start marker is
always drawn. Where the path is absent the panel shows the round without the drawing rather than
an empty frame.

**Story detail.** The photograph as hero, the title in the split-family device, the eyebrow
carrying the round association where there is one, the body as an ordered sequence of blocks drawn
from a text block, a full-bleed photograph band, a two-up photograph pair and a pull-quote, and
the gallery with its place-comma-year captions.

**Legal and not found.** The legal routes carry a single rich field each with the last-updated
time taken from the publication time. The not-found route carries the wordmark large on the true
black ground, the heading, and a `Back to the season` action, and it answers as not found.

### The three-dimensional layer

**Capability requirement, normative.** A full-viewport real-time layer composited behind the flat
content, rendering the helmet as the home hero, the portrait composition as a displaced masked
plane, and the livery collection. One persistent rendering context for the whole session,
transparent-backed so the page ground shows through, sized to the viewport and capped at a device
pixel ratio of two. The loop pauses when nothing is animating and when the tab is hidden, and
resumes on interaction.

**Fallback, and it is a contract.** The layer must survive a weak graphics chip and degrade to a
still frame. A portrait responds to pointer position with a small parallax derived from real
depth so the face separates from its background, and falls back to a flat masked image with a
soft drop shadow where the layer is unavailable. The page remains fully usable and no content
depends on the layer.

**Materials.** The helmet reads as a lacquered shell: a clear coat over a base, a fine flake in
the base so it breaks up under a moving light, and a separate matte material for the visor seal.
The portrait plane carries a depth, an alpha and a soft shadow map so the face separates from its
background. Every material is generated in code and none loads a texture file.

**Lighting.** One key light, one fill at low intensity and one rim light picked from the accent, so
the accent appears on the helmet as a lit edge rather than as a painted stripe. The rig is fixed to
the camera rather than to the scene, so a rotation does not walk the highlight off the form.

**Audio.** There is no audio layer. The reference carried an ambient bed and interface cues; the
brand platform carries neither, and nothing on the site plays a sound.

**Observed implementation, informational.** The captured reference drove the hero title through a
state-machine vector embed and baked the helmet's idle animation into a model file. Neither is
carried: the geometry is generated in code.

### Motion language

One long, hard, late-settling ease carries almost everything and is the site's default. The named
exceptions are few and each is described by what it does rather than by a curve: a heading reveals
line by line on a wipe from the left with a per-line stagger; a photograph enters on a mask that
opens from its own edge; the accent stroke draws itself across the hero from left to right; the
partner marquee travels continuously and never pauses on hover; the highlighter sweeps behind a
pull-quote line as it enters.

Scrubbed compositions change transform and opacity continuously across scroll frames rather than
at a single trigger: the pinned photograph track, the portrait composition, the gallery collage
parallax, the oval's clip, the split gateway's counter-scrub and the social callout's sticky
travel. Ordinary scrolling on the reading routes is eased rather than native, so a reveal can be
tied to a virtual scroll position.

**Reduced motion.** Under a reduced-motion preference every travel collapses to a cross fade in
place, the scrubbed compositions settle at their resting frame, the marquee holds, the stroke is
drawn complete rather than animating, and nothing that conveys information is removed.

### First load

The preloader is the hold that covers the first paint while the shell resolves, carrying the
wordmark and a progress indication on the dark ground, and hands off cleanly: once the shell is
ready the hold tears down, the chrome performs its entrance and the hero becomes interactive. If
assets are still arriving the hold waits at a near-complete state rather than snapping. It must
not block interaction past its exit.

### Iconography

Every icon is inline vector geometry, transcribed rather than shipped as a file, inheriting the
current text colour unless a fill is stated: the monogram mark, the laurel, the flag chip, the
arrow-out on a tertiary control, the social marks, the card frame, the handwritten signature form
and the circuit outlines. The signature form is the same geometry at three scales: the hero
stroke, the standing signature and the highlighter.

### Responsive behaviour

Three widths. At the desktop range the full chrome, the fluid scaling model, the four-card race
context cluster and the two calendar modes. At the tablet range the bar compresses to the
wordmark, the monogram and the store button, the reading layout becomes one column, and the race
context cluster stacks two by two. Below the narrow threshold the fluid model is abandoned for a
fixed root, the menu overlay becomes the primary route switch, the calendar list is the default
mode, the schedule table becomes a stack of rows rather than a scrolling table, nothing overflows
sideways, and every navigation target stays reachable.

### Print, and reading direction

A print stylesheet drops the chrome, the three-dimensional layer and every scrubbed composition,
sets the body in the grotesque on white, and prints the calendar and the results table as plain
tables with their headers repeated. Right-to-left readiness is structural rather than delivered:
the layout is expressed in logical start and end rather than left and right, and the accent stroke
and the chevron mirror with the writing direction, so a right-to-left locale is a translation job
rather than a rebuild.

### Accessibility

Structure and landmarks: one `main` per route, a labelled navigation, a labelled `contentinfo`
footer, and the visually hidden heading pair naming the home route for assistive technology.
Keyboard: every calendar row, every gallery item and every results row is reachable and
activatable, the two view-mode controls and the timezone control are real buttons, the menu
overlay traps focus while open and returns it to the control that opened it on Escape. Forms: the
error summary on a failed enquiry submit lists every error, links each to its field and moves
focus to itself; the submit control is never disabled for being invalid; a message beneath a field
is associated with that field programmatically. Every photograph carries alternative text and a
decorative one declares itself decorative. Contrast and state: text meets WCAG AA against its
ground, state is never signalled by colour alone, and the focus ring is visible on every surface
including the inverted ones.

### Performance

The critical styles covering the first viewport are inlined and every script is deferred, so
nothing script-shaped blocks the render. Development tooling is stripped from the production
build, and shipping it is a failure rather than a convention. Numbers carry locale-aware
separators and the workspace sorts with locale-aware collation. Budgets: the home route holds a
smooth frame rate on a mid-range handset with the three-dimensional layer running; the render loop pauses when nothing is animating and when the
tab is hidden; photographs load lazily in view order behind a placeholder derived from the stored
dominant colour; nothing blocks first paint except the opening hold. The load shape is flat for
twelve days and then multiplies for ninety minutes at the moment the data underneath is changing
fastest, which is the defining non-functional problem of this build and the reason the next-race
figures are computed rather than cached as a flag.

### Module and component architecture

The build is one shell holding the persistent chrome, the persistent three-dimensional layer and a
routed content region, so the rendering context survives a route change. Layering is explicit and
one way: a data layer that owns every read and write and is the only place a scope is applied; a
domain layer that owns the derived values, the next-round query, the career aggregates and the
publication rules; a presentation layer of routes and components that reads from the domain layer
and writes to nothing else. The reveal primitive is one wrapper taking an offset and a stagger that
drives every entrance in the product, so the motion vocabulary cannot fragment per component.

### Principals, integrations and resilience

The only principals are the four roles above plus the anonymous visitor and the ingestion run
itself. A confirmed subscriber is an address, never an account.

Each integration the platform holds is a record naming its kind, its state, a reference to where
its credentials live rather than the credentials themselves, and the instants of its last success
and last failure. That record is what drives the third-party list on the privacy route, so the list
cannot drift from what is actually connected.

Resilience is stated as behaviour, not as uptime: the public site stays fully functional with the
feed unreachable for longer than a whole race weekend, serving its last good data and saying when
it was confirmed rather than degrading to empty; the store button keeps working with the commerce
platform down; and the three-dimensional layer degrades to a still frame rather than taking the
page with it.

Schema migrations run as an explicit deployment step rather than on application start, and a
migration that changes a column in use ships as an expand, then a migrate, then a contract, so a
deployment is never simultaneously incompatible with the running version.

### Editorial workflow in the workspace

A story moves `draft`, `in_review` where a contributor wrote it, `scheduled` or `published`, and
`unpublished` or `archived` after. The review step is the only approval in the product: a
contributor submits, an editor or an owner publishes, and an editor may return a record to `draft`
with a note. There is no multi-stage chain, no delegation and no escalation on timeout. An edit
carries the version the editor loaded, and an edit carrying a stale version is refused rather than
silently overwriting a colleague's work. Publication order is fixed: the photographs are complete,
then the record is published, then the public route is verified, and only then is the story
announced anywhere. A correction to a published record raises a revision and republishes in place.

### The ingestion surface in the workspace

The workspace shows every ingestion run with its counts of applied, superseded, conflicted and
missing entities, and the raw payload of each run is retained for a bounded window so a wrong
figure on the public site can be traced to what arrived. A round in `missing_review` is listed for
a person to decide on rather than removed. A conflict lists the field, the stored override and the
incoming value, and the override stands until a person releases it. A manual refresh while a run
is in flight is refused rather than interleaved. A run that times out or finds the feed
unavailable retries on a jittered exponential backoff to a bounded ceiling and then raises an
alarm, and it never retries a rejected credential in a loop. Historical seasons carry a relaxed
budget and raise a dashboard notice only.

### Analytics, consent and privacy

The only measurement is recorded in this app's own tables: route views, the subscribe funnel, the
enquiry funnel and the store-button departure. There is no third-party tag and no external beacon.
Everything held about a subscriber can be exported and deleted for that address, leaving only a
suppression record that retains no address in clear.

### Copy deck

Global chrome carries the wordmark `Milo Rennick`, the monogram `MR`, the store button label
`Store`, and the menu destinations `Home`, `On Track`, `Off Track` and `Calendar` beside
`Business enquiries`.

Home carries the next-race eyebrow `Next race`, the standing statement naming `Halcyon` and
`2019`, and the teaser strip label `Latest`.

On Track carries the statistic strip labels `Nickname`, `Age` and `Home`, the career heading
`The record`, and the results table columns `Round`, `Date`, `Position`, `Time` and `Points`.

Calendar carries the season year `2026`, the series name `Prime One`, the header labels
`Standing` and `Round`, the featured panel labels `When`, `Circuit length`, `Race distance`,
`Laps` and `First competed`, and the two mode controls `Visualiser` and `List`.

The footer subscribe form carries the label `Email address`, the consent line naming what
subscribing means, and the pending message `Check your inbox to confirm.`

The enquiry form carries the field labels `Name`, `Email address`, `Organisation`,
`Enquiry type` and `Message`, the consent checkbox, and the confirmation carrying the reference.

Not found carries `Page not found` and `Back to the season`.

### Zero-asset substitution

Nothing in the build depends on a binary file. The helmet, the portrait plane and the livery forms
are generated as geometry at start-up. Photography and generated imagery are the same thing here: every photograph is
generated procedurally at seed time, one deterministic image per asset derived from its content
hash, so every seeded story has real bytes in the bucket and no photographic imagery ships as a
file. Circuit outlines, the laurel, the flag chips and the signature strokes are inline
vector geometry. The typefaces come from the platform stack or from a webfont fetched at build
time, never a font binary shipped in the repository. Grain is generated as a noise pass rather
than a tiled image.

### Evidence gaps

Two areas of the reference were not directly measurable and are reconstructed here: the story
detail template, because every capture of an internal editorial route resolved to the not-found
page, and the three-dimensional scene graph, because the helmet's animation is baked in a model
file. Both are specified above from the surrounding metadata and the measured not-found frame,
and both should be expected to need adjustment.

### Acceptance

Structure and content: every route above exists and carries its copy; the public story count is
live; non-public stories and their photographs are absent from and refused to the public.
Season: the next round is computed, a completed round is never upcoming, session times render with
their zone named, and an out-of-order classification never moves a result backwards. Design and
motion: the palette, the two type families, the split heading, the ground alternation and the
single undiluted accent are as tabulated; the reveal, the scrub and the reduced-motion behaviour
are as described. Quality: the three-dimensional layer degrades safely, the store button works with
the platform down, and nothing in the build depends on a binary file.

## Definition of done

A visitor can open the app, see which race is next, read a published story with its gallery, and
subscribe and confirm that subscription. A story the team has not published is absent from every
public read and its photograph bytes are refused to anyone outside the workspace, on direct
request. An ingestion run replayed twice changes nothing the second time, and an older
classification never overwrites a newer one. The app is deployed and healthy.
