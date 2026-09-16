# Roomstack

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, an administrator signed in as `admin2@example.com`
must be able to open the approval queue, read a pending request to revoke a
directory sourced group's access, approve it, execute it, and watch every live
room connection held by that group's members end at once, while the developer
who raised the request is refused when they try to approve it themselves.

That sentence is the product. Everything else in this brief exists to make it
true under pressure: the request must be executable only with the arguments that
were approved, the impact must be recomputed at the moment of execution, and a
group whose membership grew between approval and execution must send the request
back for approval rather than run against the larger set.

## Overview

Roomstack sells the infrastructure that lets several people, and several
machines, change the same data at once without the application breaking. You
are building the **governance console** its customers sign in to, the public
site that sells and prices it, and the admission surface their end users reach
rooms through.

An organisation owns projects, a project owns environments, and an environment
owns rooms, credentials and outbound endpoints. Around that sit one
authorisation decision, a change approval workflow, a metered bill, an append
only record, and a directory connection where leaving means leaving. Roomstack
is not a document editor.

## User roles

Three roles sign in, and end users never do.

| Role | May | May never |
|---|---|---|
| `admin` | raise, approve or reject requests, manage members, groups, credentials and the directory connection | approve a request they raised |
| `developer` | raise requests, write project resources, issue development credentials, open connections | approve anything, or read a production credential |
| `analyst` | read usage, audit and room metadata | write anything, or reach a credential |

Ownership is not a fourth role: one `admin` per organisation holds it, adding
legal hold release, break glass, entitlement and plan changes, and the page view
log. Below, `owner` means that admin.

An **end user** lives in the customer's own product, holds a short lived identity
token, reaches rooms only, and sits in a store with no foreign key to members, so
that identity fails closed on a console route. Signup is closed, and a refusal
never says whether a resource exists.

## Core features

1. **Lower roles are refused at the API.** An `analyst` who tries to approve,
   execute or change anything, or a `developer` who tries to approve, gets `403`
   and the row they aimed at reads exactly as before.
2. **The approval queue.** A request carries its action, arguments, a reason and
   an impact summary counting the rooms, connections, end users, members and
   credentials it affects. It moves through draft, pending, approved, executing,
   then executed, failed, expired or rejected, and is raised through a three step
   wizard, one address per step, that keeps every value when moving back.
3. **Two guards and expiry.** Self approval is refused wherever it is attempted.
   Executing other arguments than those approved is refused, an impact that grew
   after approval returns the request to pending with the difference shown, and
   an expired request says so and its requester is told.
4. **Revoking a directory group.** Groups arrive from the customer's directory and
   are read only here. On execution every grant the group carried is withdrawn,
   every console session its members hold is revoked, every credential they
   issued is retired, and every open room connection naming them is terminated.
5. **Environments and credentials.** Kind and region are fixed at creation. A
   development credential is revealable again and every reveal is recorded; a
   production credential is shown once and refused ever after.
6. **Rooms.** The room browser pages through rooms written to while they are read,
   and the inspector is a read of another company's content, recorded as such.
7. **One entitlement table.** The pricing page, the comparison matrix, the
   admission check deciding whether one more connection is allowed, the warning
   threshold and the invoice all read it, and the connection past a ceiling is
   refused.
8. **Meters and the record.** Collaboration minutes accrue per room only while two
   or more connections are held. Every configuration change, content read and
   refusal is written to an append only record sealed against the one before it.
9. **The site around it.** A pricing page, a not-found page in the product's own
   dress, a favicon, a page view an owner can read, and a form refusing a
   submission that arrives repeatedly.

## User flow

A **sidebar** carries the organisation switcher, the project list, the
environment badge and the surface links. It survives every route change; the
work surface is replaced. Console addresses read
`/{org}/{project}/{env}/{surface}`, so a link lands a colleague on the same
organisation, project and environment.

| Route | Purpose |
|---|---|
| `/`, `/pricing`, `/privacy`, `/terms`, `/contact` | the public surface |
| `/auth/login` | hands off to Keycloak |
| `/{org}/approvals` | the queue, filtered by state |
| `/{org}/approvals/new/{step}` | the three step wizard |
| `/{org}/approvals/{id}` | one request, its impact, its decisions |
| `/{org}/groups`, `/{org}/members`, `/{org}/audit` | groups, members, record |
| `/{org}/{project}/{env}/rooms` | the browser and one room's inspector |
| `/{org}/{project}/{env}/keys` | credentials |
| `/{org}/{project}/{env}/usage` | meters, credits, forecast |
| `/{org}/{project}/{env}/webhooks` | endpoints and deliveries |
| any unmatched path | the product's own not-found page |

**Entry.** Every console route requires a session; an unauthenticated request is
refused, never redirected.

**Journeys.**
1. `developer@example.com` raises a request to revoke `Northlake Contractors`,
   reads an impact naming the rooms and the live connections, and submits.
2. The same developer opens that request and tries to approve it. The control is
   absent and the call underneath it is refused.
3. `admin2@example.com` approves and executes it, and a toast confirms the
   outcome. The affected members' sessions and connections are gone.
4. `analyst@example.com` reads the queue and is refused at every write.
5. The owner changes one entitlement value and sees the pricing page, the
   comparison matrix and the admission ceiling move together.

**States.** Every surface has four: loading shaped like what replaces it, empty
with the one control that ends it, error carrying the request identifier, and
partial, where loaded rows render and a strip names what did not.

## UI/UX notes

Roomstack is designed **fully in dark**; only the documentation subsite sits on a
light ground, and there is no light mode to toggle. It reads as expensive through
a true black ground with one raised step, a one pixel hairline where a border or
shadow would be, a soft pink bloom behind the hero, working miniatures, and
handwritten annotations. Cards share edges; corners are gently rounded; the public
site breathes while console rows sit tight so a full queue fits one screen.

Colour is carried by role, never as a value: background **near-black neutral**,
text **near-white neutral** for headings and a grey **light neutral** for body,
muted **mid neutral** for placeholders, borders a **deep neutral** hairline, brand
a **light, soft indigo**. The primary action is a white button that darkens on
hover. Danger, success and warning each own a hue and always carry a word beside
it, and text keeps clear contrast against its ground.

Type: a geometric grotesque for headlines and labels, Inter for long reading,
JetBrains Mono for code and eyebrows, tabular figures where numbers align. An
input's label sits above and its error below; a toast confirms and leaves; an
overlay closes on Escape; anything irreversible asks first.

Motion is **eased**: a gentle decelerate for small things, a long expressive out
for large ones, one slight overshoot used once, and a state change
**transitions** only what it names. Under reduced **motion** arrivals stop while
colour changes, disclosures and the spinner stay.

**WCAG** AA contrast; **keyboard navigation** with a focus ring never removed;
labels on icon only controls; meaning never by colour alone; comfortable touch
targets; alternative text on every content image; and six named **breakpoints**
across phone, tablet and desktop, nothing overflowing at the narrowest
**viewport**.

## Technical requirements

### The stack, and what is already running

Build Roomstack as a **server rendered site with interactive islands**. The
server is **Fastify** on Node 20. The browser half is **Astro** with islands:
every route renders as a document on the server, and only the parts that need
behaviour, the queue filters, the wizard, the inspector and the usage charts,
hydrate. One process serves both the rendered document and the HTTP API on the
same origin under the `/api` prefix.

Three backing services are **already running** and reachable at their
environment variables. Do not download, install, compile or start a copy of any
of them.

| Service | Read from | What it is for |
|---|---|---|
| PostgreSQL | `DATABASE_URL` | every durable row in this brief |
| Keycloak | `AUTH_URL` and `AUTH_ISSUER_URL`, which carry the same issuer, with `AUTH_CLIENT_ID` and `AUTH_CLIENT_SECRET` | the identity provider that holds member credentials |
| Mailpit | `SMTP_HOST`, `SMTP_PORT` | real SMTP; every message this product sends goes here |

`APP_PUBLIC_URL` and `APP_PUBLIC_PORT` are read from the environment and never
hardcoded. There is no other backing service, no queue broker, no cache server
and no object store: anything this brief calls a queue, a cache or an outbox is
a table in PostgreSQL.

### Identity, and the two stores that must not become one

Member credentials live in **Keycloak**, realm `roomstack`. The app never stores
a member password and never mints a Keycloak administrative token.
`POST /api/auth/login` takes `{"email", "password"}`, exchanges them with
Keycloak, and on success writes a **session row** of its own and returns
`{"access_token", "expires_at"}`, a bearer token that names that row. Every console call presents that bearer token.

The session row is what makes revocation possible, and revocation is the point.
A session is idle-expired after 12 hours and absolutely expired after 30 days,
is rotated on any change of role, and is revocable by identifier. Signing in
creates a new session and leaves the member's other sessions valid. A revoked session's bearer token is refused on the next call with
`401` and code `session_revoked`.

**End users are a different store.** An end user has an external identifier such
as `eu-alicia`, belongs to zero or more groups, and holds only a short lived
**identity token** minted by a service credential at `POST /api/identity-tokens`
with body `{"user_id"}`. The token lives 600 seconds, is never stored, and names
the end user and nothing else: the groups that decide what it may reach are
resolved from the directory record at admission and **resolved again on every
operation**, so a group change binds without a new token. An identity token
presented to any `/api/` route outside the `/api/rt/` prefix is refused with
`401` and code `principal_kind_mismatch`. There is no foreign key between
members and end users and there may never be one.

### One authorisation decision

**Capability requirement.** Authorisation is one evaluated decision reached from
one place, returning allow, deny, or deny with a reason. It is not a set of
conditionals spread through route handlers. A build that answers "may this
principal do this" in more than one file will answer it differently in at least
one of them.

The decision reads a subject, an action, a resource and a context. The context
carries at least the resource's region, its legal hold, its classification, the
age of the subject's second factor, and the expiry on the subject's grant.

Four rules, and all four are observable from outside:

1. An organisation role's permission set is the starting point.
2. Every project role assignment matching the resource whose expiry is null or
   in the future is added to it. **An expired assignment evaluates as absent,
   not as a lower role, and it evaluates as absent the moment it expires** and
   not when some later sweep notices.
3. Every explicit deny is subtracted. An explicit deny defeats any union of
   allows and there is no permission that overrides it.
4. Classification, legal hold and residency are inputs to this same decision,
   never a separate mechanism bolted beside it.

### Room grants, and the precedence that decides them

A room carries three layers of grant, and they resolve by **replacement, not
union**. The more specific layer replaces the less specific one entirely:

1. `default_accesses` on the room, applying to everyone who reaches it. An empty
   list means private.
2. `room_group_access`, keyed by a group's external identifier.
3. `room_user_access`, keyed by an end user's external identifier.

So a user grant of `["room:read"]` sitting over a group grant of
`["room:write"]` **narrows the end user to read**. A build that unions the
layers gives that person write, which is the single most common way this class
of product leaks. The same resolution is used by the console, by the service
credential surface and by the admission surface, and the same function computes
all three.

The access vocabulary is closed: `room:read`, `room:write`, `comment:read`,
`comment:write`. **`room:write` does not imply `comment:write` and
`comment:write` does not imply `room:write`**, because a reviewer who may
comment on a document they may not edit is the case this separation exists for.

### The admission and operation surface

This is the realtime plane, expressed over HTTP. It is not a document engine.

| Call | Auth | Behaviour |
|---|---|---|
| `POST /api/rt/connections` | identity token | body `{"room_id"}`; `201` with `{"connection_id", "accesses"}` |
| `POST /api/rt/connections/{id}/operations` | identity token | body `{"kind"}`, one of `storage.read`, `storage.write`, `comment.read`, `comment.write`; `202` on allow |
| `DELETE /api/rt/connections/{id}` | identity token | closes the connection and stamps its close time |
| `GET /api/rt/connections` | session | open connections, filtered by `room_id` |

Admission refusals are typed and each names what was hit: `403`
`room_access_denied`; `409` `room_full`, naming the entitlement key and the
ceiling it read; `403` `quota_exhausted`, naming the meter. A refused admission
leaves every existing connection on that room undisturbed. **The connection past
the ceiling is refused; the oldest connection is never dropped to make room.**
The ceiling holds when connections arrive together: if more arrive at the same
moment than the room has space for, exactly as many are admitted as fit and every
other is refused with `room_full`.

**Permission is re-evaluated on every operation, not at admission.** Remove a
grant from a principal holding an open connection and the very next operation
that needed it is refused with `403` and code `operation_not_permitted`, naming
the access it required, while the connection stays open. Remove read and the
connection is **closed** instead, and the next operation on it returns `410`
with code `connection_closed`. A build that resolves permission once at
admission lets a person removed from a project keep writing until they close the
tab.

### Change approval

A change request carries `action`, `arguments`, `reason`, the computed `impact`,
`argument_hash`, `status` and `expires_at`. The policy is a per organisation
table mapping an action to a requirement (none, one approver, two approvers, or
a named group), to a set of eligible approvers, to a timeout, and to an
escalation group.

**The argument hash is defined exactly, because everything downstream compares
it.** It is the lowercase hexadecimal SHA-256 of the UTF-8 bytes of the
arguments object serialised as JSON with keys sorted, no whitespace, and no
trailing newline. `POST /api/approvals` returns it, `POST
/api/approvals/{id}/decisions` records the hash the approver saw, and execution
recomputes it from the request's current arguments.

Four guards, each refused at the API and not merely hidden in the interface:

- **Self approval.** The requester may not approve their own request. Calling
  the decision route directly returns `403` with code `self_approval_refused`.
- **Argument drift.** Execution presents the arguments it intends to run. If
  their hash differs from the hash recorded on the approval, execution returns
  `409` with code `arguments_not_approved`, nothing is changed, and the request
  stays `approved`.
- **Impact growth.** The impact summary is recomputed at the moment of
  execution. If **any counted field is strictly greater** than the value the
  approver saw, the request returns to `pending`, the response is `409` with
  code `impact_changed` carrying both summaries as `approved_impact` and
  `current_impact`, nothing is changed, and every eligible approver is notified
  again. Approving a change to two rooms and executing it against
  two thousand is the accident this prevents.
- **Expiry.** A request in `draft`, `pending` or `approved` whose `expires_at`
  has passed reads as `expired` wherever it is read, in a list or singly. Its
  requester is told by mail within one minute of expiry, exactly once. Executing
  it returns `409` with code `request_expired`.

**Contention.** Two executions of one approved request arriving at the same moment
run the change once: exactly one answers `200`, the other answers `409` with code
`request_not_approved` because the request is no longer `approved`, and the record
holds exactly one allowed `approval.executed` event for the request. Two eligible
approvers deciding at the same moment are both recorded in `decisions`, and neither
decision overwrites the other.

The impact summary counts `rooms`, `connections`, `end_users`, `members` and
`credentials`, computed from the state at the time it is computed.

**Break glass.** In a declared incident an `owner` may execute a change
controlled action without approval. Doing so requires a second factor asserted
within the last 300 seconds, writes an audit event of its own distinct action,
notifies every owner and every eligible approver immediately, and opens a review
item that `GET /api/review-items` reports as outstanding until it is closed with
a written justification of at least 40 characters. A second factor code serves only
the member it was mailed to, and serves every break glass that member performs
within its 300 seconds: a code mailed to any other member, in this organisation or
another, is refused exactly as a missing code is. An emergency path that is not
conspicuous afterwards becomes the normal path.

**Just in time access to content.** A room classified `regulated` refuses the
inspector outright with `403` and code `access_not_granted`. A member requests
access with a reason, an eligible approver grants it for a bounded window of at
most four hours, the grant is an attribute on the principal consumed by the one
authorisation decision rather than a role change, every read inside the window
is recorded and attributed to the grant, and it expires rather than renewing.

### The directory connection, and what revocation must actually do

Groups carry a `source` of `manual` or `directory`. A directory group's
membership is read only in the console, because a group whose membership can be
edited in two systems will disagree with itself. A group holds both members and
end users, which is what a real staff directory provisions.

Executing `group.revoke_access` against a directory group is one operation, and
all five of the following are true afterwards:

- no `room_group_access` row keyed by that group survives;
- every membership it carries reads `deprovisioned`;
- every console session held by those members is revoked;
- every credential those members created is retired, with a retirement reason;
- **every open room connection whose end user belongs to that group is
  terminated**, carrying a close time and a close reason.

The last of those is the one builds omit. A build that only flips a column
leaves the person editing a document until their token expires, and the whole
point of the control is that leaving means leaving.

### Entitlements are data, consumed in five places

Every plan limit is a row in one entitlement table keyed by plan and key. There
is no limit written as a literal anywhere else in the product. Five consumers
read that table and must move together when one row changes: the pricing page's
plan cards and its comparison matrix; the admission check that decides whether
one more connection is allowed; the console's warning threshold, which fires at
eighty per cent of a ceiling; the seat line on the invoice; and
`GET /api/entitlements`, which returns the table itself.

The table as seeded, where `unlimited` means no ceiling and a `custom` value applies
the team plan's value until a negotiated figure replaces it:

| Key | Type | Free | Pro | Team | Enterprise |
|---|---|---|---|---|---|
| `connections_per_room` | integer | `10` | `10` | `50` | `100` |
| `projects` | integer | `10` | `10` | `10` | `500` |
| `seats_included` | integer | `3` | `3` | `10` | `unlimited` |
| `seat_overage_minor` | integer | `0` | `0` | `2500` | `2500` |
| `storage_per_room_mb` | integer | `10` | `10` | `50` | `custom` |
| `file_upload_max_bytes` | integer | `52428800` | `1073741824` | `1073741824` | `536870912000` |
| `version_retention_hours` | integer | `24` | `720` | `2160` | `custom` |
| `event_retention_hours` | integer | `24` | `168` | `720` | `custom` |
| `webhook_min_interval_seconds` | integer | `60` | `60` | `30` | `custom` |
| `branding_removable` | boolean | `false` | `true` | `true` | `true` |
| `sso` | boolean | `false` | `false` | `true` | `true` |
| `directory_sync` | boolean | `false` | `false` | `false` | `true` |
| `rbac_scope` | enum | `team` | `team` | `team` | `team_and_project` |
| `soc2_report` | boolean | `false` | `false` | `true` | `true` |
| `hipaa_baa` | enum | `none` | `none` | `paid_add_on` | `included` |
| `multi_region` | boolean | `false` | `false` | `false` | `true` |
| `management_api` | boolean | `false` | `false` | `false` | `true` |
| `uptime_sla` | boolean | `false` | `false` | `false` | `true` |
| `meter_cap_collaboration_minutes` | integer | `10000` | `unlimited` | `unlimited` | `unlimited` |
| `meter_cap_storage_updates` | integer | `3000000` | `unlimited` | `unlimited` | `unlimited` |

An entitlement change is visible on the pricing page on the very next request,
because the table is pushed rather than waited out. A downgrade's `exceeding` list,
whose `resource_type` is `group`, `project` or `organisation`, names every resource
the target plan cannot hold:
each directory group when the target plan lacks `directory_sync`, each project
beyond the target's `projects`, and the organisation itself when its seats exceed
the target's `seats_included`. Rate budgets never bind below 1200 requests a minute
per credential and per organisation, 120 room creations a minute per environment,
and ten times the plan's connection ceiling in identity tokens a minute per
project.

`PATCH /api/entitlements/{plan}/{key}` changes one value. If the pricing page
says fifty connections and the admission surface admits fifty one, one of them
is lying to a paying customer and which one is lying is not knowable from
outside.

### Money, meters and the invoice

**Every figure is an integer in minor units of `usd`.** No total is computed in
floating point, and the annual plan figure is a published figure rather than the
monthly one with a percentage applied, because the two arithmetic routes
disagree by a penny and the penny is visible.

A meter rate is stated as **integer minor units per one million units**, so no
rate is ever a fraction and the arithmetic is pure logic, deterministic for a given
input, with incremental meters accumulated and level meters sampled. A line's gross charge is
`quantity * rate_minor_per_million / 1000000`, rounded half up to the nearest
minor unit. The quantity in that formula is the line's period quantity, so the
rounding happens once per line and never per interval, and half up means a half
goes to the larger neighbour, never to the even one.

| Meter | Kind | Rate, minor units per million |
|---|---|---|
| `collaboration_minutes` | flow | `200000` |
| `comments_created` | flow | `1000000` |
| `storage_updates` | flow | `100` |
| `data_stored_gb` | level | `15000000` |
| `custom_notifications` | flow | `500000` |
| `file_storage_gb` | level | `15000000` |

**The difference between the two kinds is the one a build gets wrong.** A flow
meter's period quantity is the **sum** of its interval quantities. A level
meter's period quantity is the **highest sample** recorded in the period, never
the sum, because a customer storing a steady ten gigabytes for a week is storing
ten gigabytes and not seventy. A build that accumulates a level double bills
every customer every day and passes every unit test written by the person who
made the mistake.

**Collaboration minutes accrue per room, not per participant.** A room accrues
while it holds two or more open connections and accrues nothing while it holds
one. Six people in a room for one minute is one minute, not six. Accrual is
measured in whole seconds from the stored open and close stamps of the room's
own connection records.

The invoice for a period carries, as visible lines: the plan fee, one line per
meter with its quantity, its rate and its gross charge, a seat line, and one
credit line. **The invoice total equals the sum of its own visible lines
exactly**, with no tolerance. The seat line is
`max(0, active_and_invited_seats - seats_included) * seat_overage_minor`. The
credit line is the negative of the smaller of the subscription's credit
allowance and the gross metered total; credits reset each cycle and do not carry
over.

A downgrade that would leave the organisation over an entitlement is **accepted
and scheduled for period end**, and the response names every resource that will
exceed the new plan. It is not refused, because refusing to let a customer spend
less is a dark pattern, and it is not enforced by deleting their data.

### Writing under contention, and replaying a write

`POST /api/usage/intervals`, called with a secret key, takes `{"room_id",
"meter", "interval_start", "interval_end", "quantity"}` and its natural key is
the key's environment, the room, the meter and the interval start, so the same room
identifier, meter and start in another environment is a different interval. When two identical
requests for the same natural key arrive at the same moment **exactly one**
interval row exists afterwards and both callers receive the same interval
identifier. A request for a key that already exists carrying a **different**
quantity is refused with `409` and code `usage_interval_conflict`, because that
is a client bug and hiding it makes it permanent.

Every state changing call accepts an `Idempotency-Key` header. The response is
stored against that key for 24 hours. A repeat with the same key and the same
body returns the stored response and **must not create a second** row, a second
audit event or a second outbound event. A repeat with the same key and a
different body returns `409 Conflict` with code `idempotency_key_reused`. A key is
scoped to the credential presenting it, so the same key sent by another member or
another organisation is a different key and its first use is an ordinary write. Two
simultaneous room creations under one key leave a **single winner**: one room,
one creation event, and no second write. Application level checks alone are
insufficient under concurrency. Choose any mechanism.

### Reading a collection that is being written to

Every collection read is walked with an **opaque cursor** rather than a page
number, so a list that is being inserted into while it is read returns every row
exactly once and never repeats one. A caller sets the page size with `limit=`,
between 1 and 100, and the default is 20 when the caller says nothing; the
response echoes the size it used as `page_size`. The **opaque cursor** encodes
the sort key and a tiebreak identifier, and a change of sort or filter
invalidates it rather than silently returning a different window: a cursor
presented with a different filter or order answers `422` with code
`cursor_invalid`. A response
carries `next_cursor` and `has_more` and **no `total_count` on any collection
that can be large**, because a count over a table being written at
collaboration speed runs on every keystroke of a filter field. The rooms
collection sorts by last connection descending with the identifier as tiebreak.

### Structured logs, and the identifier that makes support possible

Every request, every outbound delivery and every background run carries a
correlation identifier. The app writes **structured logs**, one JSON object per
line, to `stdout`, and writes the same lines to `/tmp/app.log`. Each line
carries the correlation identifier under the key `request_id`, together with the
route, the status and the elapsed milliseconds.

Those **structured logs** are half of the obligation and the response is the
other half. Every response, successful or not, carries the identifier in an
`X-Request-Id` header, and a caller that supplies that header has its value
echoed rather than replaced. Every error body carries the same value under
`request_id`, and every audit event records it.

A build whose error states say something went wrong with no identifier has made
every support conversation start with an unanswerable question. Writing
**structured logs** to `stdout` alone is not enough, and neither is a file
nobody can correlate to a response.

### The record

Every mutation of an organisation's configuration, **every read of a customer's
content**, and **every refusal**, are written to the audit record. Denials carry
the rule that refused them. Reads of content through the inspector are recorded
as reads, because opening a room inspector is a person reading somebody else's
document.

An event carries the organisation, a gapless `sequence` within it, the server
time it occurred, the actor and the actor's kind, the action from a closed
vocabulary, the resource type, the resource identifier, the resource's name **at
the time**, the outcome of `allowed`, `denied` or `error`, a reason, the
`request_id`, and the two hashes.

**The chain is defined exactly so it can be verified from outside.** For each
event, `hash` is the lowercase hexadecimal SHA-256 of the UTF-8 bytes of
`prev_hash + "|" + payload`, where `payload` is the JSON object of exactly these
keys serialised with keys sorted and no whitespace: `sequence`, `occurred_at`,
`actor_id`, `actor_kind`, `action`, `resource_type`, `resource_id`,
`resource_name_at_time`, `outcome`, `reason`, `request_id`. `occurred_at` is an
ISO 8601 instant in UTC with second precision and a trailing `Z`. The first
event in an organisation's chain uses a `prev_hash` of sixty four zeroes.
`GET /api/audit/verify` walks the chain and returns `{"ok": true}` or
`{"ok": false, "first_break": <sequence>}`.

The sequence is **gapless per organisation under concurrent writes from several
processes**, so a missing event is detectable. The record is append only: no
route in this product issues an update or a delete against it, and **the
credential the application itself holds at `DATABASE_URL` is unable to update or
delete a row of `audit_event`**, so the tamper evidence is not decorative.

A refusal's event carries outcome `denied` and the refusal's error code as its
reason. Opening the inspector writes action `room.inspected` with `resource_id`
set to the room identifier, and an inspector read allowed by a just in time grant
carries that access request's identifier as its reason. Creating a key writes
action `key.created` and revealing one writes `key.revealed`, each with
`resource_id` set to the key identifier. Executing a
request writes `approval.executed`, and break glass writes
`approval.break_glass`.

### Outbound events

An endpoint carries a destination, a signing secret shown once, a subscribed
event set, an enabled flag and a delivery history. A destination that is not an
encrypted transport, or that resolves to a loopback or private network range, is
refused at creation with `422` and a per field map, because a destination the
platform calls on the customer's behalf is otherwise a request forgery
primitive.

Delivery is at least once and unordered, and the platform's obligation is to
make the consumer's deduplication possible. Every delivery carries an event
identifier that is **stable across retries and across a replay**. The payload is
signed with the endpoint's secret over the string `<timestamp>.<body>`, and the
signature header reads `X-Roomstack-Signature: t=<unix seconds>,v1=<lowercase
hex HMAC-SHA256>`. **The timestamp is inside the signed material**, so a
delivery captured today and replayed next week is rejectable by the consumer; a
signature over the body alone can be replayed forever. The delivery log exposes
the event identifier, the attempt number, the status, the response code, the
signed timestamp, the signature and the exact body that was signed.

The retry ladder is immediately, then `5s`, `5m`, `30m`, `2h`, `5h`, `10h`,
`10h`, and it stops after the eighth attempt. Five consecutive days of failure
disable the endpoint and notify the organisation. A failed delivery can be
replayed singly or in bulk from the console, and a replay reuses the original
event identifier.

The event catalogue is `room.created`, `room.deleted`, `user.entered` and
`user.left` for admission; `storage.updated` and `ydoc.updated` for document
changes, where every accepted `storage.write` operation is a document change;
the thread and comment events named under comments; `notification` when a digest
window closes; `version.created` and `version.restored`; and the `key.*`,
`member.*` and `project.*` organisation events. Every room event carries `room_id`
in its `data`.

Document change events are **collapsed to at most one per room per the plan's
`webhook_min_interval_seconds`**, and that ceiling is per room and never global,
so a busy room cannot silence a quiet one. The consequence is documented rather
than hidden: a consumer cannot rebuild the document from the event stream and
must read the current state.

An event is written **in the same transaction as the state change that caused
it**, into an outbox table, and a separate pass publishes from it. Publishing
after the commit drops events whenever the process dies between the two and
invents them whenever the transaction rolls back, and both failures are silent,
rare enough to go unnoticed for months, and permanent divergence in the customer's
mirror.

### Mail

Every message goes over real SMTP to `SMTP_HOST` at `SMTP_PORT`. One message per
recipient, no cc and no bcc.

| When | To | Subject begins with | Body must name |
|---|---|---|---|
| a request enters `pending`, including a return to pending | every eligible approver except the requester | `Roomstack approval requested: ` | the action, the requester and the request identifier |
| a request is approved | the requester | `Roomstack approval granted: ` | the action, the approver and the request identifier |
| a request is rejected | the requester | `Roomstack approval rejected: ` | the action, the reason and the request identifier |
| a request expires | the requester, within one minute of expiry and exactly once | `Roomstack approval expired: ` | the action and the request identifier |
| break glass is used | every owner and every eligible approver | `Roomstack break glass used: ` | the action, the owner and the request identifier |
| a second factor is challenged | the challenged member | `Roomstack second factor code` | the six digit code |

The subject continues with a space and then the action, so a revocation request
produces the subject `Roomstack approval requested: group.revoke_access`. The
first line of every approval and break glass message is the request identifier
on its own, and the first line of a second factor message is the six digit code
on its own, so a reader scanning a busy inbox finds what the message is about
before anything else.

**The non-transition rule.** Moving a request from `approved` to `executing`,
and from `executing` to `executed` or `failed`, sends nothing at all. Those are
the transitions a build over-notifies on, and a customer who gets five messages
about one decision turns the channel off.

### Background work

Anything that cannot reliably complete inside ten seconds is a job with an
identifier, a progress surface and a completion message, not a request that
spins. Every job is idempotent on a stated natural key, takes a lease keyed on
its scope and period so two runs do not both happen, processes a collection in
pages with a cursor and a wall clock budget rather than running long, records
its start, end, items processed and items failed, and quarantines an item that
exhausts its retry budget into a dead letter with its error so the rest keeps
moving. Work is partitioned per organisation and scheduled round robin between
partitions, so one organisation's backlog cannot starve another's.

### Validation, caching and errors

Every input has one schema and both the client check and the server check are
generated from it, not kept in step by hand. The server refuses a request that
fails it with a per field map rather than a sentence. Domain invariants that a
schema cannot express, whether this room exists, whether this principal may
write it, whether this identifier is free, are checked in the domain, and the
constraints that must hold whatever the code path are held by the database.

Signed in list responses are not cached at a shared layer at all. Any cached
value derived from organisation scoped data carries the organisation identifier
in its key, through one derivation that cannot be called without one. Permission
changes, plan changes and revocations are pushed to whatever holds derived state
rather than waited out, because within five seconds and within five minutes are
very different promises when the change is that somebody was just removed.

One error shape everywhere: a stable machine readable `code` from a closed
vocabulary, a human readable `message`, the `request_id`, and an optional per
field map. No raw exception text and no raw provider message ever reaches a
person.

### The public surface and its obligations

- Every unmatched path renders the product's own **not-found** page, carrying
  the wordmark, a sentence and a link back to the home route, and answers with
  status `404`. It is never a redirect to the home route, which is the internet
  equivalent of hanging up.
- A **favicon** is served at `/favicon.ico` with an image content type and is
  declared in the head of every document.
- Every **page view** of a public route is recorded with its route, its status
  and the instant it happened, and `GET /api/page-views` returns them to an
  `owner` and to nobody else.
- `POST /api/enquiries`, behind the contact route, refuses a submission that
  fills the decoy field `role_title`, which no person can see, with `422`; and
  refuses a fourth submission from one caller inside sixty seconds with `429`.
  Neither refusal writes anything.
- No credential, secret key, client secret or database address appears in
  anything the browser downloads.
- Every response carries a nosniff content type policy and a strict transport
  policy.

### Residency, holds and erasure

An environment's region is fixed at creation and content for that environment is
stored and processed only there. What may leave a region is configuration
carrying no room content, aggregate counts for billing, and audit events. While a
legal hold is in force, deletion is refused everywhere including for an `owner`
and including through the service credential surface, and the refusal names the
hold. A request may be raised and approved against a held resource, and the hold is
decided when the change executes: executing an approved deletion of a held room
answers `409` with code `legal_hold` naming the hold under `hold`, changes nothing,
and leaves the request `approved`. Break glass is no way around a hold either; it
answers the same `409` `legal_hold` and deletes nothing. Erasure of an end user removes or anonymises them across rooms, threads,
comments, reactions, mentions, notification entries, presence records and audit
actor fields, and it must also reach the search projections, the notification
projections and **the bodies of outbound deliveries still inside their retention
window**, which is the copy every build forgets.

### The HTTP contract

Every route below lives under `/api` on the app's own origin, speaks JSON, and
answers errors in the one error shape: `{"code", "message", "request_id",
"fields"}`, with `fields` present only for validation failures. Organisations are
addressed by slug, everything else by its opaque identifier, and rooms by their
customer chosen identifier inside an environment. A console session is presented
as `Authorization: Bearer <access_token>`. Every route under
`/api/environments/{environment_id}/` also accepts a secret key of that same
environment in the same header, which is the service credential surface. An
unauthenticated call to a route that needs a principal answers `401` with code
`unauthenticated`. Wherever a call below names `owner`, it means the `admin` who
holds the organisation's ownership. Every instant in a response is ISO 8601 in UTC
with a trailing `Z`, and a `limit=` outside 1 to 100 answers `422`; an unauthenticated browser request for a console page answers
`401` and renders a sign in panel in place carrying the intended destination. A
resource that does not exist, or that the caller's organisation does not own,
answers `404` with code `not_found`. A principal whose role does not carry the
permission a call needs answers `403` with code `forbidden`, naming the permission
in the message. Every collection answers newest first unless a call below says
otherwise.

**Sessions and second factors**

| Call | Body | Success |
|---|---|---|
| `POST /api/auth/login` | `{"email", "password"}` | `200` `{"access_token", "expires_at"}`; a wrong pair is `401` `invalid_credentials` |
| `GET /api/auth/me` | none | `200` `{"member_id", "email", "role", "organisation"}` |
| `POST /api/auth/second-factor/challenge` | none | `202`, and a six digit code is mailed to the member, valid for 300 seconds |

**Organisations, projects, environments and credentials**

| Call | Body | Success |
|---|---|---|
| `GET /api/organisations/{org}` | none | `200` `{"slug", "name", "plan"}` |
| `GET /api/organisations/{org}/members` | none | a page of `{"member_id", "email", "name", "role", "status"}` |
| `GET /api/organisations/{org}/projects` | none | a page of `{"id", "name", "slug", "environments": [{"id", "kind", "region"}]}` |
| `POST /api/organisations/{org}/projects` | `{"name", "slug"}` | `201` `{"id", "name", "slug"}` |
| `POST /api/projects/{project_id}/environments` | `{"kind", "region"}` | `201` `{"id", "kind", "region"}`; a second environment of one kind is `409` `environment_exists` |
| `PATCH /api/environments/{environment_id}` | any of `{"kind", "region"}` | always refused, `409` `environment_immutable` |
| `POST /api/environments/{environment_id}/keys` | `{"kind", "label"}` with kind `secret` or `public` | `201` `{"id", "kind", "prefix", "status", "secret"}` |
| `GET /api/environments/{environment_id}/keys` | none | a page of keys, each as `GET /api/keys/{key_id}` reads it |
| `GET /api/keys/{key_id}` | none | `200` `{"id", "kind", "prefix", "label", "status", "created_by", "last_used_at"}`, never the secret |
| `POST /api/keys/{key_id}/reveal` | none | `200` `{"secret"}` for a development key; `409` `secret_not_revealable` for a production key |
| `POST /api/keys/{key_id}/retire` | none | `200` `{"id", "status": "retired"}` |

A development key's secret is readable again and every reveal writes a
`key.revealed` audit event; a production key's secret appears in the creation
response and nowhere else, ever. Status is `active`, `retired` or `suspended`.
Developers issue keys in development environments; production keys are issued by
an `admin` or `owner`.

**The directory**

| Call | Auth | Body | Success |
|---|---|---|---|
| `POST /api/organisations/{org}/directory-tokens` | session, `admin` or `owner` | none | `201` `{"token"}`, shown once |
| `PUT /api/directory/groups/{external_id}` | directory token | `{"name", "members": [email], "end_users": [{"environment_id", "user_id"}]}` | `200` or `201` `{"id", "external_id", "source": "directory"}` |
| `GET /api/organisations/{org}/groups/{external_id}` | session | none | `200` `{"external_id", "name", "source", "members": [{"email", "status"}], "end_users": [{"environment_id", "user_id"}]}` |

A directory put replaces the group's whole membership with the lists given,
creates the group on first sight, creates an end user it has not seen, and
re-activates a listed member whose membership was deprovisioned. A listed address
that is not a member of the organisation is refused with `422`. Changing a
directory group's membership through a session is refused with `409`
`group_directory_managed`.

**Rooms and grants**, every path under `/api/environments/{environment_id}`

| Call | Body | Success |
|---|---|---|
| `POST /rooms` | `{"room_id", "classification", "default_accesses"}`, the last two optional | `201` `{"id", "room_id", "classification", "default_accesses", "state"}` |
| `GET /rooms` | query `limit=`, `cursor` | a page of rooms |
| `DELETE /rooms/{room_id}` | none | `204`; under a hold `409` `legal_hold` with `{"hold"}` |
| `PUT /rooms/{room_id}/default-accesses` | `{"accesses"}` | `200` |
| `PUT` or `DELETE /rooms/{room_id}/group-accesses/{group_external_id}` | `{"accesses"}` on put | `200` or `204` |
| `GET /rooms/{room_id}/group-accesses` | none | `200` `{"items": [{"group_external_id", "accesses"}]}` |
| `PUT` or `DELETE /rooms/{room_id}/user-accesses/{user_id}` | `{"accesses"}` on put | `200` or `204` |
| `GET /rooms/{room_id}/inspector` | none | `200` `{"room", "storage", "presence", "threads", "versions"}` |
| `GET /rooms/{room_id}/capacity` | none | `200` `{"open_connections", "ceiling", "warning_at"}` |
| `GET /rooms/{room_id}/accrual` | none | `200` `{"collaboration_seconds"}` |
| `GET /events` | query `type`, `limit=`, `cursor` | a page of outbox events `{"id", "type", "created_at", "data"}` |

A room reads as `{"id", "room_id", "classification", "default_accesses",
"state", "last_connection_at", "version"}` wherever one is returned, including each item of
`GET /rooms` and the `room` of the inspector. `version` is an opaque marker that
changes on every update of the room. `PUT /rooms/{room_id}/default-accesses` honours
an `If-Match` header carrying it: a stale marker answers `409` with code
`version_conflict` and the room as it now stands under `current`, and a put without
`If-Match` is a blind update and is applied. A room identifier is unique per
environment and is not reused within 24 hours of its room's deletion: creating it
again in that environment answers `409` with code `room_id_unavailable`, while the
same identifier in another environment is free. `warning_at` is the ceiling multiplied
by eight tenths and rounded up.
`collaboration_seconds` is the whole seconds for which the room has held two or more
open connections, computed from its connection records. `PUT` on an access path
creates or replaces that layer's grant; `DELETE` removes the layer so the less
specific one applies. A room event's `data` carries `room_id`.

**End users and the admission surface**

| Call | Auth | Body | Success |
|---|---|---|---|
| `POST /api/identity-tokens` | secret key | `{"user_id"}` | `201` `{"token", "expires_in": 600}`; a retired key is `401` `key_retired` |
| `POST /api/rt/connections` | identity token | `{"room_id"}` | `201` `{"connection_id", "room_id", "accesses"}` |
| `POST /api/rt/connections/{connection_id}/operations` | identity token | `{"kind"}` | `202` `{"accepted": true}` |
| `DELETE /api/rt/connections/{connection_id}` | identity token | none | `204` |
| `GET /api/rt/connections/{connection_id}` | session or secret key | none | `200` `{"connection_id", "room_id", "user_id", "opened_at", "closed_at", "close_reason"}` |

The room named at admission is looked up in the secret key's environment. Any
operation on a closed connection answers `410` with code `connection_closed`. A
`room_full` refusal carries `entitlement` and `ceiling` beside the error keys, and
a `quota_exhausted` refusal carries `meter`. Minting a
token for an end user the environment has not seen creates that end user. A
connection closed by revocation, by retirement of the key its token was minted with,
or by loss of read access carries a non null `close_reason`.

**Change approval**

| Call | Body | Success |
|---|---|---|
| `POST /api/organisations/{org}/approvals` | `{"action", "arguments", "reason"}` | `201`, the request in `pending` |
| `GET /api/organisations/{org}/approvals` | query `status`, `limit=`, `cursor` | a page of requests |
| `GET /api/approvals/{approval_id}` | none | `200`, the request |
| `POST /api/approvals/{approval_id}/decisions` | `{"decision", "reason"}` with decision `approved` or `rejected` | `201`, the request |
| `POST /api/approvals/{approval_id}/execute` | `{"arguments"}` | `200`, the request in `executed` |
| `PUT /api/organisations/{org}/approval-policies/{action}` | `{"requirement", "eligible_roles", "timeout_seconds"}` | `200`, the policy |
| `POST /api/organisations/{org}/break-glass` | `{"action", "arguments", "reason", "second_factor_code"}` | `200` `{"approval", "review_item_id"}` |
| `GET /api/organisations/{org}/review-items` | none | a page of `{"id", "status", "cause", "approval_id"}` with status `outstanding` or `closed` |
| `POST /api/review-items/{review_item_id}/close` | `{"justification"}` | `200`; under 40 characters `422` |
| `POST /api/access-requests` | `{"environment_id", "room_id", "reason"}` | `201` `{"id", "status": "pending"}` |
| `POST /api/access-requests/{access_request_id}/grant` | `{"duration_seconds"}` | `200` `{"id", "status": "granted", "expires_at"}`; above 14400 is `422` |

A request reads as `{"id", "action", "arguments", "reason", "argument_hash",
"impact", "status", "requested_by", "expires_at", "decisions": [{"approver",
"decision", "decided_at", "argument_hash"}]}`, where `requested_by` and `approver`
are member addresses. Execution is performed by the requester or by an eligible
approver once the request is `approved`, and executing a request in any other
state is `409` `request_not_approved`. A second decision by the same approver is
`409` `already_decided`. A principal who is neither eligible nor the requester is
`403` `approver_not_eligible`. Break glass without a second factor code issued to
that owner within the last 300 seconds is `403` `second_factor_required`, and by
anyone but an `owner` is `403` `approver_not_eligible`. A request returned to
`pending` by impact growth keeps its old decisions visible but they no longer
count, so it needs approving again.

The actions and their arguments are exact: `group.revoke_access` takes
`{"group_external_id"}`; `room.default_access_public` takes `{"environment_id",
"room_id"}` and sets that room's default accesses to `["room:read"]`;
`room.delete_production` takes `{"environment_id", "room_id"}`; `project.delete`
takes `{"project_id"}` and begins staged deletion; `credential.rotate_production`
takes `{"key_id"}`. For `group.revoke_access`, `rooms` counts rooms carrying a grant
keyed by the group, `connections` counts every open connection held by the group's
end users, `end_users` and `members` count the group's end users and members, and
`credentials` counts active keys created by those members. For the room actions
`rooms` is one and `connections` and `end_users` count what is open and connected
in that room. For `project.delete`, the same counts are taken across the project.

**Entitlements, plans, usage and invoices**

| Call | Auth | Body | Success |
|---|---|---|---|
| `GET /api/entitlements` | none | none | `200` `{"items": [{"plan", "key", "value_type", "value"}]}`, the whole table |
| `PATCH /api/entitlements/{plan}/{key}` | session, `owner` | `{"value"}` | `200`, the row |
| `POST /api/organisations/{org}/plan-changes` | session, `owner` | `{"plan"}` | an upgrade `200` applied; a downgrade `202` `{"id", "status": "scheduled", "effective_at", "exceeding": [{"entitlement", "resource_type", "resource_id"}]}` |
| `DELETE /api/organisations/{org}/plan-changes/{plan_change_id}` | session, `owner` | none | `204`, the scheduled change cancelled |
| `POST /api/usage/intervals` | secret key | `{"room_id", "meter", "interval_start", "interval_end", "quantity"}` | `201` `{"id"}`, or `200` with the same `{"id"}` for an identical repeat |
| `GET /api/environments/{environment_id}/usage/intervals` | session or secret key | query `room_id`, `meter`, `limit=`, `cursor` | a page of intervals |
| `GET /api/environments/{environment_id}/usage` | session or secret key | query `period` as `YYYY-MM` | `200` `{"period", "meters": [{"meter", "kind", "quantity", "rate_minor_per_million", "amount_minor"}]}` |
| `GET /api/organisations/{org}/invoices/{period}` | session | none | `200` `{"period", "currency": "usd", "lines": [{"kind", "meter", "quantity", "rate_minor_per_million", "amount_minor"}], "total_minor"}` |

Invoice line kinds are `plan_fee`, `meter`, `seats` and `credit`, with `meter`,
`quantity` and `rate_minor_per_million` present on meter lines only. Every amount in
every response is an integer. The entitlement table and the meter list are returned
whole rather than paged.

**The record, outbound events, the site**

| Call | Auth | Body | Success |
|---|---|---|---|
| `GET /api/organisations/{org}/audit` | session | query `order` of `asc` or `desc`, `limit=`, `cursor` | a page of audit events carrying every chain key plus `id`, `prev_hash` and `hash` |
| `GET /api/organisations/{org}/audit/verify` | session | none | `200` `{"ok"}`, with `first_break` when not ok |
| `POST /api/environments/{environment_id}/webhook-endpoints` | session | `{"url", "events"}` | `201` `{"id", "url", "events", "secret", "verified"}` |
| `GET /api/webhook-endpoints/{endpoint_id}/deliveries` | session | query `limit=`, `cursor` | a page of `{"id", "event_id", "event_type", "attempt", "status", "response_code", "attempted_at", "next_attempt_at", "signed_timestamp", "signature", "body"}` |
| `POST /api/webhook-deliveries/{delivery_id}/replay` | session | none | `201`, the new delivery |
| `GET /api/page-views` | session, `owner` | query `limit=`, `cursor` | a page of `{"route", "status", "occurred_at"}` |
| `GET /api/enquiries/form` | none | none | `200` `{"form_token"}` |
| `POST /api/enquiries` | none | `{"form_token", "first_name", "last_name", "work_email", "company_size", "role", "interest", "website", "role_title"}` | `201` `{"id"}` |
| `GET /api/enquiries` | session, `owner` | query `limit=`, `cursor` | a page of enquiries |
| `GET /api/health` | none | none | `200` |

Each attempt at a delivery is its own row. A delivery body is the exact JSON string
that was signed, of the shape `{"id", "type", "created_at", "data"}` where `id` is
the event identifier, and `signature` is the full header value. A destination whose
host is a literal loopback or private address, or that resolves to one, or that is
not `https`, is refused with `422` naming `url` in `fields`; a destination whose host
does not resolve at all is accepted, marked unverified, and its deliveries fail and
walk the retry ladder. **The first document change in a room within an interval
produces its event at once; later changes in that room within the same interval are
collapsed into one event emitted when the interval ends.** An enquiry carrying a
non empty `role_title` is refused with `422` `spam_refused`; one arriving less than
two seconds after its `form_token` was issued is refused with `422`
`submitted_too_fast`; a fourth accepted enquiry from one address inside sixty
seconds is refused with `429` `rate_limited`; and none of those refusals is recorded
or counts toward the limit. Page views are recorded for every document route outside
`/api`.

### How to read the rest of this section

Every requirement from here to the fixtures is normative: it states what the
running product must do without naming a library. The technology the reference
product was observed to use is informational only, and a build that satisfies these
requirements with a different stack is correct.

### The realtime plane, in full

**The handshake has three parties.** The end user's browser asks the customer's
own server for a token; the customer's server, holding a secret key, asks
Roomstack to mint one; the browser presents it when opening a connection. The
platform never sees the customer's own session cookie. A token is bound to one
connection attempt and valid for `600s`. The secret key never leaves the
customer's server, and a client that presents a secret key where an identity token
belongs is refused and the event is recorded, because that pattern means a secret
has been shipped to browsers.

Two token shapes exist. An **identity token** carries the end user and has its
permission resolved late, at admission and on every operation, against the room's
stored grants; this build implements it. An **access token** carries an explicit
list of room patterns and permissions resolved at mint time, supporting a trailing
wildcard only, because a leading wildcard grants a project.

**The stale grant hazard, stated plainly.** With the access shape the permission
list lives inside the token for its lifetime, so revoking a grant does not affect a
token already minted. The obligations are that the lifetime is capped at `600s` so
the window is bounded, that the console's permission editor says at the point of
editing that changes take effect at the next mint for projects using that shape,
and that a revocation list for identities and connections exists so immediate
revocation is always available as terminate sessions for this identity.

**The connection lifecycle** has five states, and a client behaves differently in
each: `initial`, nothing attempted, the room shell without content; `connecting`, a
skeleton with no error copy; `connected`, the full interface; `reconnecting`, the
last known content retained and marked stale while edits queue locally; and
`disconnected`, read only with a banner and a manual retry. A separate signal fires
when a connection has been lost beyond about `5s`, and only that signal decides
whether to tell the person anything, because a warning on every reconnection is a
warning shown constantly on a phone. Reconnection backs off exponentially with
jitter from `250ms` to a `10s` cap and resets the delay only after a connection has
been held for `10s`; resetting on open produces a tight loop against a server that
accepts and immediately closes.

**Presence** is per connection rather than per user, ephemeral, never written to
durable storage, and gone on disconnect. Cursor movement is sampled at the client
and coalesced at the edge rather than streamed at input rate. The stream of other
participants carries typed changes, enter, leave, update, and a reset after
reconnection, rather than snapshots, because snapshots make a fifty person room
quadratic. A server may set presence without a connection, which is how a
background agent appears in a room.

**Storage** supports two engines, a native document of nested objects, ordered
lists and maps, where the later write to a field replaces the earlier one and list
order is kept by position and operation ordering, and a binary document in the
editor community's shared format resolved by its own algebra. Any set of concurrent
operations applied in any order at any replica **converges to the same document**,
including under duplication and after a healed partition, with concurrent deletion
of a parent and insertion into its child resolving identically everywhere and
concurrent list insertions at one position ordering identically everywhere. A
client may group operations into one message and one history entry, synchronously
only. Undo reverses the local participant's last operation and never a colleague's;
history can pause and resume to merge a burst; and a suppressed mode keeps a
background agent's writes out of every undo stack. Operations made while
disconnected queue locally in order, replay against the current state on
reconnection, and a full queue surfaces a specific state naming what will be lost
before it is lost. Per room document size is the plan's `storage_per_room_mb`, a
warning is raised as it approaches, and a write past it is refused with a typed
error rather than truncated. A server side mutation produces the same events and
the same convergence guarantees as a client one.

**Permission latency** is a requirement, not a hope:

| Input change | Reaches every open connection |
|---|---|
| room grants edited | within `5s` |
| group membership changed | within `5s` |
| identity deprovisioned by the directory | immediately, connection closed |
| key revoked | within `30s`, connections closed |
| plan downgrade reducing connection limits | at the next connection, never mid session |

**Broadcast** is fire and forget: not persisted, not ordered against storage
operations, not delivered to someone who joins later, and suitable only for
transient signals such as a reaction, a nudge or someone typing. A server may send
it, which is how a workflow outside a room signals the people inside.

**Connection limits and fair share.** A room's ceiling is the plan's
`connections_per_room`, and a separate per organisation ceiling protects the
platform from one customer's traffic. Both are token buckets, both report their
remaining budget on refusal so a client can back off, and a refusal names which of
the two was hit. Refusals are metered and appear on the overview.

**Regional routing.** Every connection for a room terminates in its environment's
region and the document's durable state never leaves it. A client elsewhere
connects across the network to the pinned region rather than a nearer replica,
because a nearer replica would be a copy in another jurisdiction. If the region is
unavailable, connections are refused rather than routed elsewhere.

### Rooms, keys and projects

A room is created explicitly through the service credential surface, or implicitly
the first time an identity connects to an identifier that does not exist and the
credential permits creation. Both paths emit the same `room.created` event, and the
implicit path has its own rate bucket because a misconfigured client can create
millions of billable rooms in an hour. A room identifier is customer chosen,
renaming is an explicit atomic operation that preserves storage, threads, versions
and grants, fails if the target exists, and emits an event carrying both names.

| State | Connections | Storage | Billing |
|---|---|---|---|
| `active` | accepted | hot | metered |
| `idle` | accepted with a cold start | moved to slower storage after `72h` without a connection | data storage only |
| `archived` | refused with a specific code | retained, read only through the service credential surface | data storage only |
| `suspended` | refused with a reason, for quota, abuse or hold | retained | data storage only |
| `deleted` | refused | erased | none |

A cold start from `idle` completes within `800ms` at the ninety fifth percentile
while the client shows connecting, because treating a cold room as an error
produces a product that fails every Monday morning.

**The room browser** shows identifier, last connection, active connections, storage
size, thread count, version count and created at; filters by identifier prefix,
metadata key and value, activity window and lifecycle state; sorts by last
connection descending; and has three empty states: a project that has never had a
room, explaining how a room is created with the one line of client code that does
it; a filter matching nothing, restating the filter with a control that clears it;
and a new production environment, noting that development traffic does not appear
there with the environment selector highlighted. **The room inspector** has four
tabs over one room: Storage, the document tree with each node's type, key and value,
live as it is edited, with a value over `4096` characters truncated behind an
explicit expand; Presence, the connected principals with connection identifier,
identity, attached information, connected at and last presence payload; Threads;
and Versions, with restore. It is a read surface with three writes, delete the room,
delete storage and restore a version, each confirmed at its tier and audited, and
every open of it writes an audit event naming the room.

**Key kinds.** Public keys carry the prefix `pk_` and may open a connection from a
browser for prototyping without reading another user's data. Secret keys carry
`sk_` and hold full project authority on the customer's server. Management keys
carry `mk_`, are organisation wide and scoped, and exist on the top plan only.
Every key carries an environment, a label, a creator, a creation time, a last used
time and address, and an optional expiry. The keys surface sorts by last used
descending by default, because the operationally interesting key is the one nobody
is using, and filters by environment and status.

**Leaked key handling.** When a key's prefix is found in public code hosting, the key
is suspended immediately rather than queued for review; every owner and admin is
notified; an audit event of type `key.leak_suspended` records the source; and the
console shows the affected key with the reason and a one step reissue. Suspension
comes before notification because a public key is in someone else's hands within
minutes.

**Project deletion** is staged: requested, with the typed name confirmed, marking
the project `pending_deletion`, suspending every key and refusing every connection;
a grace period of `168h` during which an owner may restore it, usage is still billed
and rooms are readable by nobody; and executed after grace, erasing content and
retaining the audit record. Deletion is refused outright while any room in the
project is under a legal hold, and the refusal names the holds.

**Seats and invitations.** An invitation writes an `invited` membership, sends one
message, and carries a single use token valid for `168h`. Inviting an address that
is already a member is idempotent and returns the existing membership. Inviting an
address in a domain claimed by an identity provider is refused with an explanation,
because that person arrives through single sign on or the directory. Revoking an
invitation invalidates its token, and a later acceptance returns a specific expired
state. Seats count `active` and `invited` memberships together, and crossing the
included count is shown before the invitation is sent, not after. The last owner
cannot leave; a directory deprovisioning of an owner suspends rather than deletes
that membership and notifies every other owner; a role downgraded during an open
session fails the next authorisation call closed and reissues the session at the
lower role within `60s`; and an invitation accepted after its inviter left is valid
and keeps the original inviter in the record.

**Single sign on and the directory, beyond revocation.** Assertion based federation
and token based federation are both supported. An assertion is validated for its
signature against the provider's published keys, its audience, its recipient, an
issue time within `120s` of skew, and its identifier against a replay cache holding
`24h`, so the same assertion presented twice is refused. Domain claiming is two
steps: assert the domain, prove it by publishing a record, and only then require
federated sign in for that domain. Just in time provisioning creates a membership on
first federated sign in with the mapped role, **defaulting to the lowest role and
never the highest**. Directory deprovisioning is the requirement that fails most
often, so reconciliation runs on a schedule as well as on each directory event,
because a missed directory event is ordinary and an ex-employee holding access is
not. At least one break glass credential path survives a misconfigured provider,
held by an owner, usable only with a second factor, and every use notifies every
other owner.

### Comments and threads

A thread carries its room, customer defined metadata, a resolved flag with resolver
and time, its creator and a deletion stamp; a comment carries its thread, a body,
attachments, mentions derived from the body, its author, creation and edit times and
a deletion stamp; a reaction is unique on comment, emoji and actor. **The body is a
structured document, not a string**: mentions, links and formatting are nodes, so no
consumer re-parses text and no path renders customer text as markup. **Deletion is a
tombstone**, and a thread whose every comment is deleted is itself deleted and emits
`thread.deleted`.

Thread metadata is a flat map of string, number or boolean values, filterable by
equality, numeric comparison and presence, so a canvas can ask for the four threads
in the region on screen rather than every thread in the room. A mention is a node
carrying a stable identifier and never a display name. A group mention expands at
notification time, not write time, so a person added later is not notified
retroactively and a person removed is skipped. **Mentioning a principal who cannot
read the room is refused at write time with a per mention error and the comment is
not written.** Reading threads requires `comment:read`; writing requires
`comment:write`, separable from document write; editing and deleting require
authorship or a moderation capability; resolving requires `comment:write`; and public
and private comments are a thread level visibility attribute resolved with the same
precedence as room grants.

Client behaviour: a posted comment appears at once with a pending marker, settles on
acknowledgement, and on refusal reverts with an inline error and the text preserved;
an unsent composer body survives a reload; comments order by creation time with the
identifier as tiebreak so two written in the same millisecond order identically for
everyone; threads page by cursor and comments within a thread do not page below
`100`; and toggling a reaction is idempotent. The composed components, a thread, a
composer and an inbox entry, carry their own accessible structure and are themed by
variables, and the primitives beneath them assume nothing about the composed
structure. Every mutation emits `thread.created`, `thread.deleted`,
`thread.metadata_updated`, `thread.marked_as_resolved`,
`thread.marked_as_unresolved`, `comment.created`, `comment.edited`,
`comment.deleted`, `comment.metadata_updated`, `comment.reaction_added` or
`comment.reaction_removed`, none of them collapsed, because they are human rate
actions the email path depends on seeing.

### Notifications and feeds

End user notifications come in three kinds: thread, raised by a mention or a reply in
a thread the recipient participates in and grouped per thread; text mention, raised
by a mention inside a document body and grouped per document; and custom, raised by
the customer's own server with a customer defined type, grouped per type and subject,
and metered. **The inbox groups by subject, not by event**, so ten replies are one
entry carrying ten activities; read state is per entry per user and marking read is
idempotent; entries page newest first; the unread count is a maintained counter
rather than a count query; and deleting a subject marks its entries unavailable rather
than leaving holes.

Channels: the in product inbox is delivered by the platform; email and chat
integrations are delivered by the customer's own server from an outbound event, so
the platform never sends an end user email and sending domains stay the customer's;
web push is delivered by the customer's service. Settings are a matrix of channel by
kind per user per project with values `enabled`, `disabled` and `inherit`, inheriting
user, then project default, then platform default; a channel with no configured
endpoint reports as unavailable rather than enabled; and settings are read at
delivery time. **The digest is the delay that makes email work**: activity opens a
window of about thirty minutes per recipient, per subject, per channel; further
activity joins it; on expiry one `notification` event carries every activity in it;
a recipient who reads the entry in product before the window closes has the email
suppressed; a recipient whose room permission is revoked during the window receives
nothing; and the window survives a restart of the process holding it. A build that
emits on each activity has built a spam generator.

Console notifications are a different path: usage thresholds, key leaks, endpoints
auto disabled, approval requests, directory sync failures and invoice events,
addressed to members at their own address over SMTP, and not metered.

**Feeds**, marked beta, are an append only ordered log in a room, distinct from
threads: each entry carries a gapless per feed sequence and each participant holds a
cursor, so an offline consumer asks for everything after its last number and knows
it has missed nothing.

### AI copilots

A copilot is **a participant in a room, not a side channel**: it appears in presence,
its writes go through the same document path as a person's in its own identity, its
messages are persisted, and its actions pass the same authorisation decision. A
copilot carries a name, provider, model, a required fallback model, a system
instruction that is versioned and audited when changed without altering existing
chats, a temperature, an output ceiling, a tool policy, knowledge sources and an
enabled flag. A chat belongs to one copilot and optionally a room. **Messages form a
tree, not a list**: each carries a parent, a role of user, assistant or tool, its
content, tool calls and results, a status of `pending`, `streaming`, `complete`,
`failed` or `cancelled`, and what it branches from, so editing an earlier message
and asking again creates a branch rather than destroying history.

**Streaming and cancellation.** A response streams to every participant of the chat
over the same connection as everything else, so two people watching one chat see the
same stream. A stream cancelled by the requester stops within `500ms` and persists the
partial message as `cancelled`. A stream interrupted by a disconnection resumes from
the persisted offset on reconnection, or completes on the server and is delivered
whole, and never restarts, because restarting bills twice.

**Knowledge and retrieval.** Sources, pages, documents, images and inline text, are
fetched, chunked, embedded and indexed on a schedule, **per project and never shared
across projects** even for identical content. A source that fails to fetch is marked
failed with the reason and retried on a decaying schedule; retrieved passages are
attributed in the response; and removing a source removes its vectors within one
index cycle, because orphaned vectors keep answering from deleted material.

**Tools** run in one of three modes: `auto`, called without asking; `confirm`, where
the interface renders the proposed call and its arguments for a person to approve or
reject; and `disabled`, never offered. Every call and result is persisted on the tree
and auditable; a mutating call writes through the document path in the assistant's
identity with history suppressed; a call is refused, visibly, when the assistant's
identity lacks the permission; confirmations expire after `300s` as rejections; and
every mutating call carries an idempotency key derived from the message identifier.

**Cost, metering and abuse.** Every request records input tokens, output tokens,
model, latency and principal. A per organisation monthly budget is enforced at request
time with a typed refusal, and the console shows the ceiling and who set it. Rate
limits bind per end user as well as per project, so one abusive end user cannot
exhaust a customer's budget. The copilot's own writes count toward storage metering.
**No model provider is reachable from this environment**, so a request that would
reach one records a `failed` status with the reason `provider_unavailable` and no
charge, which is the same behaviour this product owes when both a provider and its
fallback are down.

### Versions and files

A version carries its room, a sequence, a creator that is a person, an automatic
policy or a restore, a kind of `automatic`, `manual` or `pre_restore`, a size, a
checksum and an optional label. Automatic versions are taken on a schedule and on
quiescence, when a burst of editing has been still for `300s`; manual versions carry a
label; and **a restore takes a version first**. Retention prunes automatic versions
first, oldest first, never pruning manual or pre restore versions inside the plan's
window.

**A restore under concurrent writers** takes the room's write lease, captures a pre
restore version of the current state, computes the operation set that turns current
into target, applies it as one batch in the identity of the restoring principal, and
releases the lease. It never replaces the document wholesale, which would discard
operations arriving during the computation from people still looking at the screen.
Two simultaneous restores serialise, the second computed against the first's result.
A restore under a legal hold is refused, and a restore of a pruned version is refused
with a specific reason.

Files: uploads below `8 MB` are a single request and above it multi part with each
part retryable; files are addressed by an opaque identifier; a read requires room
read on every request and not only when a signed link is issued; signed links expire
in `600s` and are bound to the requesting identity; the declared type is never
trusted and anything renderable as active content is served with a disposition that
stops it executing on the customer's origin; deduplication is by checksum within a
project only, never across projects, because shared blobs make one organisation's
erasure impossible to honour; and removing a referencing node schedules the blob for
collection after `168h`, so an undo does not break an image.

### The service credential surface

A server to server interface covers every resource in this brief: rooms, storage,
documents, threads, comments, notifications, notification settings, groups, versions
and files within a project, and on the top plan organisation resources such as
members, projects and keys. A project secret authenticates project scoped calls in
its environment; a management credential authenticates organisation calls and
carries an explicit scope list, so an automation that reads usage cannot delete a
project.

Shape: resources are plural nouns and actions beyond create, read, update and delete
are sub resources rather than verbs in a path; identifiers are opaque and prefixed by
type; errors carry a code, a message and a request identifier, always all three;
validation failures return a per field map; time has one format and one zone; money
is integer minor units with an explicit currency; and absent and null are distinct
on update so a field can be cleared. **Pagination** is the cursor contract above, with
no offsets anywhere. Mutable resources carry a version marker; an update presenting a
stale marker is refused with `409` carrying the current state, and a blind update is
permitted and documented as blind. Server side storage changes are a document patch,
so two servers editing different parts of one document do not overwrite each other,
and a whole document write is available and documented as destructive.

Rate limits run in three tiers, per credential, per organisation, and per endpoint
class with a smaller bucket for expensive reads and uploads, and every response
reports the remaining budget, the ceiling and the reset time. A refusal carries a
retry hint, because a refusal without one makes every client retry at once.

**Versioning and deprecation.** The interface is dated. Removing a field, narrowing a
type, changing a default or adding a required parameter is breaking and needs a new
date; adding an optional field or a new value to an open set is not, and clients
tolerate both. A deprecated version carries a sunset header and a documented end date
at least `180d` out, the console shows which versions an organisation's traffic still
uses, and the organisation is notified while that traffic persists.

### Usage, billing and plan changes

**The usage surface**, per project and per organisation with a period selector,
draws one chart per meter with the credit allowance as a horizontal reference and
the projection to period end as a distinct continuation; beneath it a table of
quantity, unit rate, credit applied and net charge per meter with the arithmetic
visible; attribution of usage by project; and export of the period as a delimited
file produced as a background job.

| Transition | Effect |
|---|---|
| upgrade | immediate; entitlements raised at once; the charge prorated for the rest of the period |
| downgrade | scheduled for period end; entitlements unchanged until then; every resource that will exceed the new plan named |
| cancel | scheduled for period end; data retained for the grace window |
| reactivate within grace | restores without data loss |

No payment provider runs in this environment, and the subscription row is the mirror
a provider would reconcile. The mirror still owes its rules: provider state is the
source of truth and is never inferred from a checkout completing; an inbound provider
message is signature verified before it is parsed; it is deduplicated on the
provider's event identifier held for `72h`; out of order messages are decided by the
provider's own version rather than arrival time, so an update after a deletion never
resurrects a subscription; checkout completed twice creates one subscription, keyed
on the organisation and the target plan; and a failed payment moves the organisation
into a visible dunning state with the amount and retry date, warns before it
suspends, and **suspends writes before reads**, so a customer in arrears can still
get their data out. On the free plan the meters are hard caps: at eighty per cent an
administrator is notified, at one hundred per cent the metered capability is refused
with a typed error naming the meter, and every refusal is recorded and shown on the
usage surface.

### Console analytics and observability

Two audiences, two systems. Customer facing analytics are what an organisation sees
about its own usage and health, partitioned by the organisation identifier in every
query and retained per plan. Operator telemetry is aggregate, retained on its own
schedule, built from a separate store the customer facing code holds no credential
for, and never rendered to a customer.

**The overview** tiles: active connections now with a `24h` sparkline; active rooms
now with a `24h` sparkline; monthly active users for the period against the period
before; collaboration minutes for the period against the credit allowance; storage
against the room ceiling; errors as a rate over `1h` by class; and refusals as a count
over `24h` by reason, room full, quota or permission. Every tile has an empty state
saying why it is empty and how to change that, because a new project's overview is a
row of zeroes that teaches nobody anything.

Time series follow a resolution ladder: a `1h` window at `10s` resolution retained
`48h`; `24h` at `1m` retained `30d`; `30d` at `1h` retained `13 months`; and `13
months` at `1d`. Rollups are scheduled jobs and a query picks the coarsest series
that satisfies its window. Billed quantities are never read from rollups: the charts
are for looking at, the meter is for charging, and the console says which is which.

**The error and refusal explorer** groups by class, authentication failure,
permission refusal, quota refusal, room full, payload too large, storage limit,
provider error and internal error, with recent samples carrying time, room, principal
shape and request identifier, and never an end user's content or any part of a token
or key, because a redaction that shows a prefix leaks a prefix. The request
identifier is propagated across the connection boundary, the outbox publisher and the
outbound delivery, so one request that ends in a delivery can be followed end to end.

| Objective | Target | Window |
|---|---|---|
| connection establishment success | `99.9%` | `30d` |
| connection establishment latency, ninety fifth percentile | `< 500ms` | `30d` |
| operation broadcast latency within region, ninety fifth percentile | `< 150ms` | `30d` |
| service credential surface availability | `99.9%` | `30d` |
| outbound delivery first attempt within `10s` | `99%` | `30d` |
| console availability | `99.9%` | `30d` |

The top plan's `99.99%` uptime commitment is measured against connection
establishment and operation delivery rather than the marketing site. Alerting is on
error budget burn rate rather than an instantaneous threshold. Server side budgets:
an authorisation decision under `1ms` at the ninety fifth percentile from a resolved
set held on the connection; a default page of a service collection under `200ms`; and
metering writes off the request path entirely.

### Governance beyond the chain

**What is audited**, by domain: identity, sign in, sign out, failed sign in, second
factor enrolled, session reuse detected, break glass used; membership, invited,
joined, role changed, suspended, deprovisioned, invitation revoked; federation,
provider configured, domain claimed, mapping changed, sync run, sync failure;
project, created, renamed, deleted, restored, region set; key, created, revealed,
retired, leak suspended; room, inspected, storage read, storage deleted, room
deleted, identifier changed; version, created, restored, pruned by policy; outbound
endpoint, created, secret rotated, disabled, delivery replayed; copilot, configured,
system instruction changed, knowledge source added or removed; billing, plan changed,
payment method changed, credits granted; governance, export requested, erasure
requested, legal hold placed or released; approval, requested, approved, rejected,
expired, escalated. The two unusual fields are deliberate: the resource name at the
time, so a renamed project still reads correctly, and the outcome including denials,
because what someone tried and was refused is the most useful thing in an
investigation. A refresh token presented twice revokes its whole family and writes
`session.reuse_detected`.

**Tamper evidence** makes modification detectable rather than impossible: the chain
head is published to an append only store on a schedule, the console exposes the
verification that reports the first break, and retention deletion is a separately
credentialed pass deleting whole sealed segments. **The audit surface** filters by
actor, action, resource, outcome, time window and address, searches the resource
name, pages by cursor, and exports a signed file as a background job; on the top plan
events stream continuously to the customer's collector through the outbox carrying
the sequence, so a collector down for an hour loses nothing and can detect a gap.
Retention is `90d` on plans that have the log and custom on the top plan, with a floor
that cannot be set below the organisation's declared regulatory minimum.

**Classification.** A room is `standard`, ordinary handling; `confidential`, where
the inspector requires just in time approval; or `regulated`, where the inspector
requires approval and a stated reason, content is excluded from support access
entirely, and encryption uses the organisation's own key where configured.
Classification is an input to the one authorisation decision rather than a separate
mechanism.

**Export and erasure.** A full export of an organisation's rooms, threads,
notifications and configuration is a background job delivered as an expiring, audited
link. Erasure of one end user completes within `30d`. Erasure of an organisation
happens after cancellation and the grace window, retaining only what tax and audit
require. **Erasure requests are recorded and replayed against any backup restored
after the request**, because a backup restored a month later otherwise resurrects
erased data, and erasure reaches the search index, notification projections, the
copilot vector store, cached room summaries and outbound payloads still in retention.

**Legal hold.** While held, deletion is refused everywhere, retention pruning and
version pruning skip the held resources, erasure requests targeting held content are
recorded as pending and executed when the hold lifts, and placing and releasing a
hold are themselves audited, with release requiring the governance capability, which
is separable from ownership.

### Security, privacy and compliance controls

The public security route makes commitments this build must stand behind: an audited
security programme, an independent audit under the common controls standard, support
for the health information regime, annual independent penetration testing,
encryption at rest and in transit, vulnerability scanning, logging and monitoring,
continuity and incident response, least privilege internally, quarterly access
review, and a data processing agreement.

| Control | Requirement |
|---|---|
| transport | encrypted transport only on every surface, no downgrade path, a strict transport policy with a long window and preloading |
| storage | every store encrypted at rest, with keys held in a managed service, rotated on a schedule, and per organisation keys available on the top plan for regulated rooms |
| field level | end user identifiers, display information and comment bodies encrypted per field in regulated rooms |
| backups | encrypted, with restores tested on a schedule and the test recorded |
| session cookie | the browser console holds its session in an http only, secure, same site lax, host prefixed cookie naming the same session row a bearer token names |
| request forgery | a double submit token on every cookie authenticated state changing call, and the connection handshake is not a form target |
| content security | a strict policy with nonces, no inline handlers, and a report endpoint |
| frame protection | the console refuses framing entirely |
| file serving | from an origin with no session cookie, with a download disposition for anything not explicitly renderable |
| outbound requests | outbound destinations and knowledge fetches resolve through an allowlisting resolver refusing private ranges, and redirects are followed only after re-checking the target |
| secrets in logs | a redaction filter at the logging boundary, so a known secret pattern never appears in output |
| timing | credential comparison in constant time, and sign in returns the same shape in a similar duration whether or not the address exists |
| enumeration | sign in, password reset and invitation acceptance return the same response for existing and non existing addresses |

Security rate limits are separate from quota and tighter: failed sign ins, `5` per
`15m` per address then a widening delay; sign in per address range, `50` per `15m`; password
reset, `3` per hour per address with an identical response whether or not a message
was sent; token minting per project, proportional to the plan's connection ceiling;
invitations, `50` per hour per organisation; management credential creation, `10` per
day per organisation.

Where the health regime is in force, on the top plan or as a `$350/month` add on on
the team plan, every room is treated as at least `confidential`, the inspector always
requires just in time access, support access to content is disabled entirely, audit
retention floors at the regime's requirement, and erasure that conflicts with
retention is held and surfaced rather than resolved silently.

Incident response detects on burn rate, audit anomalies and leaked key matches;
declares with one action that opens an incident record and starts the clock; contains
with **one action each** to revoke every session for an identity, suspend every key in
a project, and terminate every connection to a room, tested quarterly; notifies
affected organisations within the contractual window; and reviews in writing within
`5` working days.

### Background work, by name

| Job | Kind | Cadence |
|---|---|---|
| outbox publisher | queue | continuous |
| outbound delivery | queue | continuous, on the retry ladder |
| notification digest | durable workflow | per recipient per subject |
| usage rollup | scheduled | every `5m`, `1h` and `1d` |
| meter close | scheduled | hourly and at period end |
| invoice preparation | durable workflow | at period end |
| directory reconciliation | scheduled | every `15m` |
| room tiering | scheduled | hourly |
| automatic versioning | queue | on quiescence |
| version pruning | scheduled | daily, respecting holds |
| knowledge re-indexing | scheduled | per plan interval |
| leaked key scan | queue | on external signal |
| export generation | durable workflow | on request |
| erasure execution | durable workflow | on request, within `30d` |
| audit segment sealing | scheduled | hourly |
| blob collection | scheduled | daily, after `168h` |
| retention enforcement | scheduled | daily |
| approval expiry | scheduled | every `30s` |
| dunning | durable workflow | on payment failure |

A queue is for work triggered by an event where order does not matter, at least once
with a dead letter; a scheduled job is for work triggered by time, at least once per
period under a lock; and a durable workflow is for multi step work with waits, human
input or a compensating undo, whose state survives a restart. Approval requests, plan
changes, exports and digests are durable workflows rather than sleeping consumers,
and a deploy must not lose an open window. Every task meets the rules above:
idempotent on a stated natural key, leased per scope, bounded, observable,
quarantining poison work, and partitioned for tenant fairness so one organisation's
million room backfill never delays another's digest.

### Caching and invalidation

| Data | Where cached | Lifetime | Invalidated by |
|---|---|---|---|
| public marketing pages | edge | `300s`, stale while revalidating `86400s` | publish |
| build generated public assets | edge | immutable for a year, content hashed | never |
| documentation pages | edge | `300s` | publish |
| entitlement table | process memory | `60s` | a plan change event, pushed |
| resolved permission for a connection | connection memory | until an input changes | the invalidation channel |
| room summary for the browser list | shared cache | `10s` | a write to the room |
| session and identity | shared cache | the session lifetime | sign out, role change, deprovision |
| usage rollups | shared cache | `60s` | a new rollup |
| console list responses | none | none | none |

**Invalidation is pushed, not polled.** Permission changes, plan changes, key
revocations and deprovisioning are pushed to every process holding derived state over
the same channel the realtime plane uses; a time to live is the backstop and never
the mechanism, because the latency table above cannot be met by expiry.

| Field | Rule |
|---|---|
| room identifier | `1` to `128` characters, no control characters, unique per environment, not reused within `24h` of deletion |
| metadata | at most `50` keys, keys `1` to `64` characters, values string, number or boolean, serialised value at most `1024` characters |
| comment body | a structured document; nesting deeper than `100` nodes is refused; mentions resolved and permission checked |
| outbound destination | encrypted transport, resolving to a public address, at most `2048` characters |
| email address | validated by shape only and then by delivery, never by a pattern claiming to implement the standard |
| money | integer minor units and a currency, refused if the currency does not match the subscription |
| time window | start before end, at most the plan's retention, refused with the maximum stated |
| idempotency key | `1` to `255` characters, scoped to the credential |
| file upload | declared size checked against the plan before transfer starts, and the transfer aborted when the actual size exceeds it |

### Failure handling and degradation of the platform

**The principle**: every dependency has a stated behaviour when it is unavailable,
and that behaviour is always narrower than the surface failing.

| Failure | Behaviour |
|---|---|
| token mint fails at the customer's server | a typed authentication state and a backed off retry, never a loop |
| connection refused as not authorised | a typed refusal; the interface renders read only with an explanation |
| connection refused as room full | a typed refusal naming the limit |
| connection refused on quota | a typed refusal naming the meter |
| connection lost briefly | reconnecting; last known content retained and marked stale; edits queue locally |
| connection lost beyond the threshold | the lost connection signal fires and the interface may tell the person |
| retry budget exhausted | disconnected, read only, explicit manual retry |
| storage write rejected for size | a typed error naming the limit, the operation not partially applied |
| offline queue overflow | a specific state naming what will be lost, before it is lost |
| identity provider down | existing sessions continue; new federated sign ins fail with a specific message; break glass remains |
| directory down | reconciliation retries; deprovisioning already observed still executes; the console shows sync failing |
| model provider down | fall back to the fallback model recording which answered; if both fail, a failed status, the person told, no charge |
| object store down | file reads fail individually, the rest of the room is unaffected, uploads refused as retryable |
| search index down | the room browser falls back to prefix filtering on the primary store, marked as reduced |
| metering store down | writes buffer; if the buffer fills, service continues and the gap is recorded explicitly and shown on the usage surface |
| queue down | the outbox holds and publication resumes with nothing lost |
| **audit store down** | **the action is refused**, because an action that cannot be recorded is not permitted |

**Backpressure and overload.** One organisation flooding the service credential
surface is refused by its own bucket first and other organisations are unaffected; a
room past its operation rate has operations coalesced and then refused with a typed
error without the connection being dropped; a backed up outbound queue slows delivery
while the outbox stays durable and the console shows the lag; a backed up job
partition leaves other partitions proceeding; and a platform shedding load preserves
reads over writes and says so.

### Seeded fixtures

Seeding runs on first start, is idempotent, and every seeded account uses the
password `deku-demo-pw-2026`. Every member below also exists in the Keycloak
realm `roomstack` with the same address and password.

| Address | Organisation | Role | Name |
|---|---|---|---|
| `owner@example.com` | Northlake | `admin`, holding ownership | Dana Whitlock |
| `admin@example.com` | Northlake | `admin` | Idris Bekele |
| `admin2@example.com` | Northlake | `admin` | Stacy Loamwork |
| `developer@example.com` | Northlake | `developer` | Alicia Cadence |
| `developer2@example.com` | Northlake | `developer` | Olivier Bramble |
| `contractor@example.com` | Northlake | `developer` | Nimesh Sundial |
| `analyst@example.com` | Northlake | `analyst` | Jonathan Foundry |
| `owner2@example.com` | Pagewise | `admin`, holding ownership | Marc Kestrel |

Two organisations: **Northlake**, slug `northlake`, plan `enterprise`, default
region `eu-west`, subscription plan fee `50000` minor units with a credit
allowance of `60000`; and **Pagewise**, slug `pagewise`, plan `free`, default
region `us-east`, plan fee `0` and allowance `0`. No row of one is ever visible
to the other, and a member of one who names a resource of the other receives
exactly the response a non existent resource would produce.

Projects: **Atlas Editor** (`atlas-editor`) and **Fieldnote Boards**
(`fieldnote-boards`) in Northlake, **Tetrad Canvas** (`tetrad-canvas`) in
Pagewise. Each has a `development` and a `production` environment; Atlas Editor
is pinned to `eu-west` and the other two to `us-east`.

Six rooms in the Atlas Editor production environment:

| Room | Classification | Grants |
|---|---|---|
| `doc-almanac-brief` | `standard` | default `["room:read","room:write"]` |
| `doc-cadence-roadmap` | `standard` | default `[]`; group `grp-northlake-reviewers` `["room:read","room:write"]`; user `eu-olivier` `["room:read"]` |
| `doc-bramble-notes` | `standard` | default `["room:read"]`; user `eu-alicia` `["room:read","comment:write"]` |
| `doc-sundial-intake` | `regulated` | default `[]` |
| `doc-hollow-dispute` | `standard` | default `["room:read"]`, under the legal hold `hold-hollow-2026` |
| `doc-foundry-handoff` | `standard` | default `[]`; group `grp-northlake-contractors` `["room:read","room:write"]` |

Six end users in that environment: `eu-alicia`, `eu-olivier`, `eu-marc`,
`eu-stacy`, `eu-nimesh` and `eu-jonathan`.

Three groups in Northlake. **Northlake Contractors**, source `directory`,
external identifier `grp-northlake-contractors`, carries the member
`developer2@example.com` and the end users `eu-marc` and `eu-stacy`.
**Northlake Reviewers**, source `directory`, external identifier
`grp-northlake-reviewers`, carries the end users `eu-alicia` and `eu-olivier`.
**Platform Admins**, source `manual`, external identifier
`grp-platform-admins`, carries `admin@example.com` and `admin2@example.com`.
`eu-nimesh` and `eu-jonathan` belong to no group.

One credential: a development secret key labelled `Contractor sandbox` in the
Atlas Editor development environment, created by `developer2@example.com`.

Change controlled actions for Northlake, each with a timeout of 86400 seconds:
`credential.rotate_production`, `room.delete_production`,
`room.default_access_public`, `group.revoke_access` and
`project_role.grant_long` need **one approver** holding `admin`;
`project.delete` and `identity_provider.configure` need **two approvers**
holding `admin`; `audit.retention_change` needs two approvers holding `admin`;
and `legal_hold.release` needs the named group **Platform Admins**. In a policy
body, `requirement` is one of `none`, `one_approver`, `two_approvers` or
`named_group`, and `eligible_roles` lists roles.

One request is seeded in `pending`: `group.revoke_access` with the arguments
`{"group_external_id": "grp-northlake-contractors"}`, raised by
`developer@example.com` with the reason `Contract ended 2026-09-15`.

Seeded usage intervals for the Atlas Editor production environment, for the
period beginning `2026-09-01T00:00:00Z`:

| Room | Meter | Quantity |
|---|---|---|
| `doc-almanac-brief` | `collaboration_minutes` | `120000` |
| `doc-cadence-roadmap` | `collaboration_minutes` | `180000` |
| `doc-bramble-notes` | `collaboration_minutes` | `60000` |
| `doc-almanac-brief` | `comments_created` | `15000` |
| `doc-almanac-brief` | `storage_updates` | `4200000` |
| `doc-almanac-brief` | `custom_notifications` | `240000` |
| `doc-almanac-brief` | `data_stored_gb` | three samples of `10` |
| `doc-almanac-brief` | `file_storage_gb` | two samples of `4` |

The invoice for period `2026-09` for Northlake is therefore a plan fee of
`50000`, collaboration minutes `72000`, comments `15000`, storage updates `420`,
data stored `150`, custom notifications `120000`, file storage `60`, a seat line
of `0` while `seats_included` is `unlimited`, and a credit line of `-60000`,
totalling `197630` minor units.

## Data model

Everything durable lives in PostgreSQL at `DATABASE_URL`. Identifiers handed to
a client are opaque and prefixed by their type (`org_`, `prj_`, `env_`, `key_`,
`room_`, `conn_`, `req_`, `evt_`, `grp_`), never sequential. Every table
carrying organisation scoped data holds the organisation identifier and is
filtered by it in the database itself, not only by the query builder, because
one missing filter in one handler is the whole breach.

### The control plane

- **organisation** - identifier, name, slug unique across the table, plan,
  status, default region, created at, deleted at.
- **member** - identifier, organisation, identity, role, status of `invited`,
  `active`, `suspended` or `deprovisioned`, who invited them, granted at,
  expires at. **Unique on the pair of organisation and identity**: without that
  pair two invitations create two memberships and role resolution becomes order
  dependent. Membership is an edge carrying attributes, never a column on a
  person, because a person may belong to two organisations and a grant may end.
- **identity** - identifier, email address unique without regard to case,
  display name, whether a second factor is enrolled, the provider subject that
  Keycloak knows them by, created at. Federated identities are matched on the
  stable provider subject and never on the address, because addresses change.
- **grp** - identifier, organisation, name, source of `manual` or `directory`,
  external identifier. Unique on the pair of organisation and name.
- **grp_member** - group, principal kind of `member` or `end_user`, principal
  identifier. A directory group's rows are written only by reconciliation.
- **project** - identifier, organisation, name, slug unique within the
  organisation, status, deleted at.
- **environment** - identifier, project, kind of `development` or `production`,
  region, created at. **Unique on the pair of project and kind**, so a project
  has exactly one production environment and a build that allows two has two
  sources of truth for a region. Kind and region are refused on update by a
  database constraint, not by a disabled form field.
- **api_key** - identifier, environment, kind of `public`, `secret` or
  `management`, prefix, secret hash, label, created by, created at, last used
  at, last used address, revoked at, revoked reason, expires at. The secret hash
  may be absent only for a development key, and that is held by a check
  constraint so a production secret cannot be stored in the clear by an
  accidental code path. Last used is written at most once per sixty seconds per
  key, because writing it on every request turns authentication into a write
  path.
- **project_role_assignment** - identifier, project, principal kind, principal
  identifier, role, granted by, granted at, expires at. Expiry is read on every
  authorisation call, so it is indexed.
- **entitlement** - plan and key together identify the row; value type and
  value. This table is the only place a plan limit exists.
- **subscription** - identifier, organisation, provider identifier, plan,
  status, period start, period end, plan fee in minor units, credits in minor
  units, whether it cancels at period end, and the provider's own version, which
  is what decides ordering when two provider messages arrive out of order.
- **session** - identifier, identity, member, issued at, last seen at, absolute
  expiry, revoked at, revoked reason. A session is the unit of revocation.
- **webhook_endpoint** - identifier, environment, destination, secret hash,
  subscribed events, enabled, consecutive failure days, created at, verified at.
- **approval_request** - identifier, organisation, action, arguments, argument
  hash, requested by, reason, impact, status, expires at, created at, executed
  at, failure reason.
- **approval_decision** - identifier, request, approver, decision of `approved`
  or `rejected`, decided at, and the argument hash the approver saw.
- **access_grant** - identifier, organisation, room, member, reason, granted by,
  granted at, expires at. The just in time window, consumed by the one
  authorisation decision.
- **review_item** - identifier, organisation, cause, opened at, due at, closed
  at, justification.
- **idempotency_record** - key, credential, request fingerprint, response
  status, response body, created at. Held for 24 hours.

### The collaboration plane

- **room** - identifier, environment, room identifier of one to 128 characters
  unique within the environment and not reusable within 24 hours of deletion,
  state of `active`, `idle`, `archived`, `suspended` or `deleted`,
  classification of `standard`, `confidential` or `regulated`, default accesses,
  stored bytes, last connection at, created at, deleted at, legal hold.
- **room_group_access** - room and group external identifier together identify
  the row; accesses.
- **room_user_access** - room and end user external identifier together identify
  the row; accesses.
- **end_user** - identifier, environment, external identifier unique within the
  environment, display information the customer attached, erased at. Separate
  from `identity` and `member`, with no foreign key reaching either.
- **connection** - identifier, room, end user, opened at, closed at, close
  reason. An open connection is one whose closed at is absent. Presence is per
  connection, so two tabs from one person are two rows carrying one identity.
- **thread** - identifier, room, metadata as a queryable map of at most fifty
  keys, resolved, resolved by, resolved at, created by, created at, deleted at.
- **comment** - identifier, thread, body as a structured document rather than a
  string, created by, created at, edited at, deleted at, sequence. Deletion is a
  tombstone: the row, its identifier and its position survive and it renders as
  removed, because hard deleting one from the middle of a thread breaks every
  notification and every outbound payload that referenced it. A thread whose
  comments are all deleted is itself deleted and emits its own deletion event.
- **reaction** - comment, emoji and actor together identify the row; added at.
  Adding one that exists is no operation rather than a duplicate.
- **version** - identifier, room, sequence unique within the room, kind of
  `automatic`, `manual` or `pre_restore`, label, size, checksum, created by,
  created at.
- **feed** and **feed_entry** - a feed is named within a room; an entry carries
  a **gapless sequence within its feed**, so a consumer that was offline asks
  for everything after the last number it saw and knows it has missed nothing.
- **inbox_entry** - identifier, environment, end user, kind, subject type,
  subject identifier, last activity at, read at, with the four of environment,
  end user, subject type and subject identifier together unique, so ten replies
  to one thread are one entry carrying ten activities rather than ten entries.
- **inbox_activity** - identifier, entry, event, occurred at.
- **notification_setting** - environment, end user, channel and kind together
  identify the row; value of `enabled`, `disabled` or `inherit`. Read at
  delivery time, never at enqueue time, so switching a channel off suppresses a
  message already waiting.

### The append only planes

- **usage_interval** - environment, room, meter and interval start together
  identify the row; interval end, quantity, sample or flow. That key is what
  makes a retried write store once.
- **audit_event** - organisation and sequence together identify the row. Its
  columns are named exactly as the chain keys, `sequence`, `occurred_at`,
  `actor_id`, `actor_kind`, `action`, `resource_type`, `resource_id`,
  `resource_name_at_time`, `outcome`, `reason` and `request_id`, together with
  `organisation_id`, `id`, `prev_hash` and `hash`, plus the actor address and the
  redacted before and after. That key is what makes the sequence gapless and
  therefore what makes a missing event detectable.
- **outbox** - identifier, organisation, event identifier, event type, payload,
  created at, published at, claim holder, claim expires at. A row is written in
  the same transaction as the change it describes and the claim on it is atomic,
  so two publishers running at once deliver each event once.
- **webhook_delivery** - identifier, endpoint, event identifier stable across
  every attempt, event type, attempt number, status, response code, signed
  timestamp, signature, body, next attempt at, created at.
- **page_view** - identifier, route, status, occurred at.
- **enquiry** - identifier, name, organisation name, work address, message,
  created at.

Both append only tables are partitioned by time, and neither is ever updated or
deleted by the application. Retention deletion is a separately credentialed
pass that removes whole sealed segments rather than individual rows, so a
deletion cannot be used to remove one inconvenient event.

### Seed data

Seeding runs on first start and is idempotent. The accounts, organisations,
groups, rooms, end users, credential, policies, pending request and usage
intervals are exactly those listed under seeded fixtures in the technical
requirements, and every seeded account signs in with the password
`deku-demo-pw-2026`, which is written with the addresses to
`/app/USER_README.md`.

### The indexes that exist because a screen would otherwise be unusable

Threads by room, resolution and creation time for the thread list with its
default filter; the thread metadata map for the filtering the canvas case needs;
comments by thread and sequence for ordered reading and the tiebreak; inbox
entries by environment, end user and last activity for the inbox, with a partial
one over unread entries for the counter; rooms by environment and last
connection descending with the identifier as tiebreak for the cursor; and live
credentials by environment for authentication.

## Front-end specification

This section carries the exact visual and structural values. Colour is carried
as family, tone and shade rather than as a value; type is carried exactly; motion
is carried in words.

### The ground, and the one raised step

The whole product sits on true black. There is exactly one step above it, a
**near-black neutral** barely lighter than the page, for panels that must read
as a distinct plane, and a **near-white neutral** inverse surface for inverted
panels and the primary button. Almost all separation is a hairline rather than
elevation, and the hairline exists in two forms that are not redundant: a
translucent one that composites correctly over the bloom and over a moving
surface, and an opaque **deep neutral** one that is what a one pixel ring
resolves to over the page ground. Every card and panel edge is that one pixel
ring. A slightly stronger translucent fill marks a control at rest.

**Cards share edges.** Card grids butt against one another with a single
hairline between them rather than a gap, so a two by two grid of statements
reads as one object cut into four. That is why the home route's benefit grid and
the enterprise route's capability grid both look like one panel. Implement the
shared edge as a grid level concern that sets a panel's edges from its position,
so a two by two grid renders three lines rather than eight, never as a per
instance override.

The page ground fades up behind the fixed header over twice the header height,
and combined with the header's backdrop blur this is what makes content dissolve
rather than slide under a bar. A graph paper pattern, a repeating one pixel grid
built from two linear gradients rather than an image, sits behind the code block
on the comments route and behind the architecture diagram on the home route,
masked at its edges so it fades out rather than ending at a hard line.

### Foreground steps

| Step | Colour | Use |
|---|---|---|
| primary | **near-white neutral** | headings, body at emphasis |
| subtle | **light neutral** | body copy, the default reading colour |
| subtler | a dimmer **light neutral** | secondary body, captions at `14px` and above |
| subtlest | **mid neutral** | labels, disabled text, placeholders, decorative line numbers |

White dominates the computed colours, the subtler grey is the second most used
at about a fifth of the volume, and the subtle grey follows. **Body copy is grey
and headings are white**, and a build that sets body copy white loses the entire
tonal structure in one line. The subtlest step does not meet an ordinary contrast
threshold against black and appears in no running prose: it is permitted only on
placeholders, disabled controls, decorative line numbers and large display type
used as ornament. The reference product uses it on the closing display headline
of the home route, where it carries meaning; this build uses the subtle step
there instead, and that divergence is deliberate.

### Brand, accents and product hues

The brand is a **light, soft indigo**, used for documentation accents, links and
primitive marks, with a translucent wash of the same hue behind a chip.

Four accents form one family, built the same way by a single hue rotation around
a fixed lightness and saturation: a **light, soft cyan** called blue, a **light,
soft teal** called green, a **light, soft violet** called pink, and a **light,
soft amber** called yellow. Each has a bold partner, a paler step of the same
hue, used for a filled surface rather than a mark. Reproduce them as that one
family rather than as a generated ramp; a generated ramp lands elsewhere and the
difference shows when two accents sit adjacent in the primitive list.

Each of the four collaboration features owns a hue, and that hue re-themes the
whole of its route: the eyebrow mark, the highlight behind the headline, the
demonstration furniture and the section rules all shift together from one
declaration scoped at the route root. One declaration, four routes.

| Feature | Hue | Character |
|---|---|---|
| Multiplayer | **light, soft blue** | built like the accent family |
| Comments | **light, soft orange** | built like the accent family |
| Notifications | a second **light, soft teal**, a mint | built like the accent family |
| AI Copilots | **mid, vivid red**, a hot pink | markedly more saturated and darker, the only accent outside the family |

The fourth is the site's cleverest decision: it is the value that produces the
pink bloom on the home hero, and the AI surface is the one the site wants to feel
different from the others.

**No value is written at a use site.** Every colour, radius, shadow and duration
resolves through a named token, and a scan of the built interface finds no
literal colour anywhere a component uses one.

### Type

Three families, all measured from the face declarations.

| Family | Weights | Role |
|---|---|---|
| Suisse Intl | `400`, `500`, `600 700` | display and interface; the product voice |
| Inter | variable `100 900`, with an italic face | long form body, documentation, anywhere a wider weight range is needed |
| JetBrains Mono | `400`, `500` | code, eyebrows, the letterspaced uppercase label |

**Suisse Intl is a licensed commercial face and this build may not ship it.**
Substitute a geometric grotesque carrying `400`, `500` and `600`, matched on cap
height and on the ratio of x-height to cap height, and rule out faces with wide
default sidebearings, because the display tracking below is negative and the
letterforms must not collide. Inter and JetBrains Mono are openly licensed and
are kept by name. Every face declares a swap display strategy and a metric
matched fallback with adjusted size, ascent, descent and line gap, so the
fallback occupies the same space as the real face and nothing reflows when it
arrives. That is the reason the reference headlines do not jump.

The scale actually rendered, by volume:

| Size | Weight | Line height | Where |
|---|---|---|---|
| `16px` | `400` | `24px` | the dominant body size, by a factor of five over everything else |
| `14px` | `500` | `20px` | interface labels, menu items, buttons |
| `14px` | `400` | `20px` | secondary body |
| `12px` | `400` | `16px` | captions, table cells, the eyebrow |
| `12px` | `500` | `16px` | badges |
| `18px` | `400` | `29.25px` | the lead paragraph under a headline |
| `20px` | `500` | `28px` | small section headings |
| `24px` | `500` | `33.6px` | card headings |
| `16px` | `400` | `26px` | a looser body variant used in long form |
| `14px` | `400` | `17.5px` | a tight variant used inside demonstrations |

Display sizes are absent from that table on purpose: headlines are set in
viewport relative units and interpolate continuously between a minimum and a
maximum, clamped at both ends, rather than stepping at a breakpoint.

| Role | Minimum | Maximum | Line height | Tracking |
|---|---|---|---|---|
| hero headline | `40px` at the narrow width | `84px` at the wide width | `1.02` | `-0.03em` |
| section headline | `28px` | `56px` | `1.06` | `-0.025em` |
| card headline | `20px` | `24px` | `1.4` | `-0.01em` |
| lead paragraph | `16px` | `18px` | `1.625` | `0` |

These four rows are inferred from three captured widths rather than parsed, so
the shape of the rule is certain and the exact endpoints are a reconstruction.
Negative tracking on display sizes and zero tracking on body is what makes the
headlines read as tightly set rather than as large body copy.

**The letterspaced label.** A monospace, uppercase, widely letterspaced eyebrow
above a headline, in JetBrains Mono at `12px`, weight `400`, tracking `0.1em`,
in the subtlest step on a dark ground or in the route's own product hue. On the
home route it comes into focus as it arrives, its opacity and its blur resolving
together.

**Emphasis by colour, not by weight.** The site's most characteristic
typographic move is a grey paragraph in which the load bearing clauses are set in
white at the same size and weight.

### Radius, depth, blur and containers

| Radius | Where |
|---|---|
| `2px` | inline chips, the smallest badges |
| `4px` | the default: links with a background, small controls |
| `5px` | menu panels |
| `6px` | the most used value overall: cards, buttons, inputs in the interface |
| `8px` | form fields on the enquiry route |
| `12px` | large cards, the demonstration frames |
| `100px` | the pill toggle on the pricing route |
| full round | avatars and circular controls, which the capture reports as an extremely large value |

Depth is mostly not shadow. Five treatments, in order of frequency: the hairline
ring on every card and panel edge; an inset hairline on inline code; a field ring
on inputs and selects; a focus ring, a black halo four pixels wide separating an
avatar or control from what is behind it; and the popover shadow, soft and offset
downward, which is the only real drop shadow and is reserved for floating
panels. **A build that reaches for a soft shadow on a card has misread the
system.**

Blur tokens run `4px`, `8px`, `12px`, `16px`, `24px` and `64px`. The `12px` step
is the fixed header's backdrop; the `4px` step is the entrance blur on popovers;
the `64px` step is the bloom.

Containers run `20rem`, `24rem`, `28rem`, `32rem`, `36rem`, `42rem`, `48rem`,
`56rem`, `64rem` and `72rem`. Two custom properties carry the page rhythm by
name, an outer gutter used for the page margin and by the toast slide distance,
and an inner gutter used inside panels.

### Iconography

Icons are inline geometry, never files, and seventy were recovered. They fall
into three grids and the grid says which set an icon belongs to.

| Grid | Model | Use |
|---|---|---|
| `0 0 16 16` | filled paths, no stroke | interface icons: arrows, chevrons, external link, plus, close |
| `0 0 20 20` | filled paths | brand and social marks, and the larger interface set |
| `0 0 32 32` | filled paths, two path composites | feature and capability marks above card headings |

Every icon fills with the current colour and inherits it from its context, with
exactly two exceptions: the four point sparkle in the AI context, pinned to the
copilot hue, and the same sparkle on an inverted chip, pinned to the inverse
surface. Both are the same geometry with a different declared fill.

**The wordmark** is a single compound path of letterforms beside a mark of two
triangles, rendered at the height of the header row with automatic width. The
two triangles are rotationally symmetric about the mark's centre, the second
being the first turned half a turn, and a build that draws them independently
with one vertex wrong produces a mark that looks correct until it is scaled up.
The mark is used without the letterforms on the account routes. The wordmark
carries the flare sweep on hover.

**The interface set** carries a menu of four rules, a long right arrow, a short
right arrow, a left chevron, a plus, an external link, and a tooltip arrow whose
outline path is drawn twice on purpose so the fill and the ring can be coloured
independently while sharing one geometry.

**The two icons the product is about** are the filled cursor, the presence mark
used in the menu, on cards and as the moving badge, and the sparkle, the AI mark,
in a four point form and in a richer two star composite used at display size
inside headlines with a small optical nudge that makes an icon in a line of
display type look centred. The send mark is a paper plane on the composer's
submit control.

**The capability marks** above card headings include conflict resolution as a
node graph, community as a speech shape with dots, and an application window.

Icon behaviour: colour inherited; sizing by a size utility, never by intrinsic
dimensions; decorative icons hidden from assistive technology; meaningful icons
named, and an icon only control always named. The arrow inside a link slides in
from slightly left and fades in on hover **and on focus**, and the external link
mark fades in on hover **and on focus**. A build that implements the hover half
and drops the focus half removes the affordance for every keyboard user in a two
word omission.

### Motion

Every easing in the reference was parsed from its stylesheets. Motion is eased,
and three curves carry the whole feel: a decelerating curve with no overshoot for
everything small, colour, opacity and small transforms; an expressive out, fast
and then easing over a long tail so it feels weighted, for everything large,
reveals, sheets and big movement; and **the overshoot, which passes its target
and returns, used for exactly one thing**, which is why it reads as deliberate
rather than bouncy. The rest are supporting and are named here so none is
invented:

| Curve | Role |
|---|---|
| the default decelerate | colour, opacity and small transforms |
| the in and out | anything that both leaves and arrives |
| the expressive out, in three spellings | reveals, sheets, large movement |
| a slightly softer expressive out, combined across two spellings | softer large movement |
| a gentler decelerate | long moves, and the cursor badge paths |
| the carousel curve | carousel transforms and the testimonial cross fade |
| a symmetric in and out | balanced movement |
| an expressive out, tighter | short expressive movement |
| a very late decelerate | things that arrive suddenly and settle |
| the overshoot | the one thing that overshoots |
| a stronger overshoot | used once |
| a fast in, slow out | an attention move |
| the exponential in | held as `--ease-in-expo` |
| a mild out, combined across spellings | mild settling |
| a mild overshoot | used once |
| the pulse curve | the pulse utility |
| a symmetric in and out, slower | slow balanced movement |
| a sharp symmetric in and out | abrupt balanced movement |
| near linear with soft ends | steady travel |
| a symmetric pair, two spellings | balanced movement |

Durations are carried by character. The menu item ground is the fastest thing in
the product, deliberately, because a menu being scanned must not lag the
pointer. Colour, ground, border and outline changes are quick and share one
default duration. Icon slides and small transforms are a little slower; card
edges, sheets and most transforms slower again; the shadow half of a paired
background and shadow change slower still; large transforms and carousel
movement slower again. The spinner has a short steady period, slow colour washes
and the flare sweep take about a second, the largest reveal takes a little more,
and the pulse is the slowest loop.

**The colour transition is enumerated, never all.** Colour, background colour,
border colour and outline colour change together on the default decelerate at
one of four short durations. The reference transitions `all` on tens of
thousands of declarations, and that is the one thing in its motion layer not to
copy: `all` transitions properties nobody intended, including layout properties,
and it is a reliable source of dropped frames.

Entrances and exits, each named:

| Moment | What it does | Where |
|---|---|---|
| slide down | fades in while travelling a few pixels down into place | menus opening downward |
| slide up | fades in while travelling a few pixels up into place | tooltips and popovers opening upward |
| appear, disappear | a plain fade in, a plain fade out | the general fade |
| popover in | resolves from a slight blur while fading in and growing very slightly | floating panels, the only entrance that blurs, so a panel reads as coming into focus rather than being scaled up |
| dropdown in | fades in while growing very slightly | menu panels |
| tooltip in | identical to dropdown in | tooltips |
| toast in | enters from past the right page edge by exactly the outer gutter | toasts |
| toast hide | fades while shrinking very slightly | toast dismissal |
| toast swipe out | continues from where the swipe ended back out past the gutter | touch dismissal |
| sheet, four directions | travels fully in from the top, bottom, left or right, named slideInFromTop and its siblings, and back out | drawers |

**The reveal.** Sections enter as they scroll into view as a paired change: the
transform starts at once, travelling up from a small upward translation on the
expressive out, and the opacity only begins after a short delay of a few tenths
of a second, which is what makes a reveal read as arriving from somewhere rather
than fading in place. Siblings stagger slightly. The trigger is intersection with
the viewport, once, and **the observer disconnects after firing**, because a
reveal that re-runs on scroll back is a different design and reads as unstable.
A reveal masks per line rather than per word, so descenders are not clipped.

**The flare** is a diagonal band of transparency sweeping across a masked
element, running on the wordmark on hover and on a looping element in the footer
region. **The shimmer** is a soft four stop mask four times the width of its
element swept from one side to the other; it is the loading treatment for a
skeleton and it is reused for every loading state in the console.

**Masks used as design, not as effects.** An illustration fade dissolves the
bottom of a demonstration rather than cutting it; a top entry fade lets content
emerge from behind the header; a radial vignette fades a centred block at its
corners; a section base fade dissolves a panel into the page below it; and a
horizontal edge fade is the treatment for every horizontally scrolling row,
including the logo wall and the category rail, because a row ending at a hard
edge tells the reader nothing about whether there is more.

**The spinner** is twelve bars, each rotated, each fading from full to a faint
opacity on a linear loop with the same animation offset in time, so it reads as
mechanical rather than as spinning. **The noise drift** translates a static
grain tile through a small cycle of offsets, the standard trick for making a
grain look like film grain, and **the light streaks** fade up to a faint glow and
back on the industry route heroes.

**Reduced motion** branches both ways rather than only disabling:

| Category | Behaviour under reduced motion |
|---|---|
| section reveals | absent; content is present at rest |
| loops: flare, shimmer, noise, light streaks | stopped at a composed frame |
| the cursor field | static, cursors at their rest positions |
| carousels | do not advance on their own; controls still work |
| colour, ground, border and outline transitions | retained |
| disclosure transitions on menus and drawers | retained, at the default duration |
| the spinner | retained, because a loading indicator that does not move is not a loading indicator |

Disabling every transition makes the interface feel broken rather than calm, and
it is the most common overcorrection. Nothing in the product flashes more than
three times a second, and everything that moves on its own can be stopped and
stops permanently on interaction.

### Scroll

**The document is the scroller.** There is no scroll hijacking, no momentum
smoothing and no scrubbed timeline; a build that introduces smoothing has changed
the product, because every behaviour here assumes the scroll position is the
browser's. What is genuinely scroll driven on the home route is short: two
horizontal marquees that move continuously and were only caught at different
points; the bloom element's transform and its backgroundImage; the full bleed
noise layer's backgroundImage; the eyebrow label's opacity and filter; a
comment reaction button's boxShadow; and a handful of clip path and transform
changes inside the demonstration.

All scroll driven work on a route reads the scroll position **once per frame from
one subscription** and distributes it; reveals use intersection observation and
unobserve after firing. Five independent listeners on one page is five layout
reads a frame.

Sticky elements: the header, fixed always; the pricing plan header row, sticky
within the comparison table; the documentation sidebar, with its own independent
scroll; the documentation contents rail, with the current heading marked; and
the examples category rail above the large width. Every sticky offset is
expressed against the header height custom property and never as a literal,
because a hard coded offset breaks when the announcement pill is present.

### The demonstration surface

The single most important object on the public site and the one most likely to
be under-built. Every major route carries a framed miniature of an application
with people and machines visibly working inside it: the hero of the home route,
the proof on each feature route, and three variants in a card grid on the
enterprise route. **It is not a screenshot and it is not a video with a play
button.** It is a live composition of real interface furniture, real type,
moving cursors, avatar stacks, comment popovers and assistant panels inside a
frame.

**The frame** has a `12px` radius, or `12px 12px 0px 0px` where it is cut off at
the page edge; the hairline ring; a chrome bar of about `44px` holding three
small `8px` decorative dots spaced `6px` apart at the left and a tab set; an
interior on the raised surface; and a bottom that dissolves through the
illustration fade rather than ending.

**The tab set** reads Document, Workflow, Sheet and Dashboard, each with a small
leading icon, one active. The active tab carries the slightly stronger fill with
white text at weight `500`; inactive tabs carry no ground with the subtler grey
at `400`; all are `14px` on a `20px` line at a `6px` radius. It is a real tab
widget: a tablist, a selected tab, arrow keys between tabs, the panel associated
with its tab. It cycles on its own on a timer, and **the timer stops permanently
on any interaction**, which is what separates a demonstration from an
advertisement.

**The cursor badges** are the product's central metaphor: a filled cursor of
`16px` with a label at a `4px` radius in `12px` type at weight `500`, offset
`4px` right and `8px` down from the pointer tip. Each participant gets one
accent and keeps it; measured instances are in the green family, in a blue and
in a neutral grey. A badge travels a continuous curve between rest points rather
than a straight line, taking about two seconds a leg and pausing a little over a
second at each rest, on the gentler decelerate. Those timings are inferred.
Cursors are decorative and hidden from assistive technology, the frame carries a
text alternative describing what the demonstration shows, and the animation
stops when the document is hidden and under reduced motion.

**The annotation lettering** is handwritten labels with a curved hand drawn arrow
pointing at part of the demonstration, reading `Your app with Roomstack` and
`Collaborate in realtime`, at about `14px` in white, outside the frame at the
wide width and suppressed below the medium width. It is the one informal element
and it carries a disproportionate share of the personality.

**The avatar stack** holds full round `28px` avatars whose overlap is set by a
custom property named for it, with a radial gradient mask cutting the previous
avatar so the next sits cleanly against it, a black four pixel ring as a
separator, and a count chip for overflow. The radial mask works over the bloom,
which a ring of background colour would not.

| Variant | Where | Contents |
|---|---|---|
| Workflow | home hero | a node graph with connected boxes, a cursor, an assistant chip in the product pink |
| Sheet | home hero, and the narrow default | a spreadsheet grid with a selected cell, a second person's selection, a formula |
| Document | home hero | a text document with a selection, a comment popover, a mention |
| Dashboard | home hero | charts and tiles with a cursor |
| Comment thread | comments route | a thread with avatars, timestamps, reactions, a composer with an at-mention control, an emoji control, an attachment control and a send control in the brand purple |
| Assistant chat | AI copilots route | a chat with a question, a streaming answer, and a tool call with confirm and cancel controls |
| Inbox | notifications route | notification cards with avatars, bodies, relative times and action controls |
| Editor | multiplayer route | a text editor with two cursors, a floating toolbar and an assistant control |

Every variant renders without any binary asset; holds at the narrow width by
dropping content rather than scaling, because a scaled demonstration is
illegible; contains no real form control, because a real input inside a picture
of an application is a keyboard trap with no purpose; is one region with one text
alternative rather than forty decorative labels read aloud; and suspends its
animation off screen.

### Global chrome

The header, its three menus, the announcement pill, the mobile drawer, the skip
link and the footer appear on every marketing route. They do not appear on the
documentation subsite, which carries its own chrome, nor on the account routes,
which carry none.

**The header** is fixed to the top at full width with no ground of its own, a
`12px` backdrop blur, a height held in a custom property named for the header
height, and a layer above page content and below overlays. Left to right: the
wordmark linking home; three menu triggers reading Product, Solutions and
Resources; two links reading Docs and Pricing; then, pushed right, a text link
reading Sign in and a filled button reading Get started. Above the medium width
the whole set is visible; below it everything between the wordmark and the
actions collapses into one control named Open menu, drawn as the four rules.

**The menu panels** have a `5px` radius and the hairline ring, open with the
dropdown entrance, carry the tooltip arrow above the large width, and hold a
small directory with a sentence under every entry. Each trigger is a **button
with an expanded state, not a link**. A panel opens on activation including
keyboard activation, not on hover alone; hover may open it additionally above the
large width where the pointer is fine. Escape closes it and returns focus to the
trigger; an outside click closes it; moving to another trigger swaps the panel as
a cross fade without closing and reopening; focus moves into the panel on
keyboard activation and the arrow keys move between items; and the panel is
**not** a focus trap, so tabbing past its last item closes it and continues into
the header.

| Menu | Group | Items and their sentences |
|---|---|---|
| Product | Realtime Infrastructure | Presence: Online users, cursors, selections. Broadcast: Temporary event signals. Storage: Synced data and file storage. Feeds, marked Beta: Messages and activity logs. Threads: Contextual conversations. |
| Product | Collaboration features | Multiplayer: Realtime collaboration. Comments: Contextual commenting. Notifications: Smart alerts for your app. AI Copilots: Individual AI assistants. |
| Solutions | Industries | Human resources: Collaboration for HR & talent tools. Security & compliance: Collaborative reviews for audits & evidence. Sales & marketing tools: Engaging features that help sellers sell. Healthcare: HIPAA-ready collaboration for care teams. Creative tools: Multiplayer canvases for people & AI. Legal: Secure drafting for firms & clients. AEC: Collaboration for design & construction. Education: Interactive realtime learning experiences. |
| Solutions | Users | Enterprise: Realtime collaboration without a rewrite. Innovation: Validate and ship multiplayer bets fast. Startups: Build multiplayer products from day one. Individual builders: Prototype multiplayer apps in minutes. |
| Resources | Tools | Examples: Gallery of open source examples. Showcase: Gallery of collaborative experiences. Next.js Starter Kit: Kickstart your Next.js collaborative app. DevTools: Browser extension. Tutorial: Step-by-step interactive tutorial. Guides: How-to guides and tutorial. Figma UI Kit: Roomstack Collaboration Kit. |
| Resources | Company | Blog: The latest from Roomstack. Customers: The teams Roomstack empowers. Changelog, and the rest of the company set. |

**The announcement pill** sits centred above the home hero, not as a full width
bar: a small monospace uppercase tag reading `RECAP` on the brand wash, a
sentence reading `The Age of Agent-Ready Software` at `14px` weight `500`, and a
square arrow control on a slightly stronger fill. It is one link in its entirety,
with the arrow as decoration rather than a second target.

**Buttons.** Primary: a white ground, black text, `6px` radius, `36px` tall,
darkening by a measured two per cent on hover and staying neutral. Secondary: the
translucent fill with white text, the same radius and height, its ground alpha
rising slightly on hover. Ghost: no ground, white text, a `4px` radius, a faint
fill appearing on hover. Link with arrow: inline, the arrow sliding in on hover
and focus. All carry the enumerated colour transition.

**The skip link** is the first focusable element, visually hidden until focused,
then positioned at the top left over the header, and activating it moves focus,
not only the scroll position, to the main landmark.

**The mobile drawer** covers the viewport below the medium width, entering with
slideInFromTop over a fading overlay on the expressive out. Background scroll is
prevented while it is open and the scroll position is restored on close; focus is
trapped inside; escape closes it; and its groups are collapsible disclosures
rather than one long list.

**The footer** carries four link columns and a brand column. Realtime
Infrastructure: Presence, Broadcast, Storage, Feeds with a Beta chip, Threads.
Collaborative features, then Solutions, then Use cases. Resources, then
Technologies: Documentation, Examples, Showcase, DevTools, React components,
Next.js Starter Kit, Tutorial, Guides, Release notes, then the fourteen
technology routes. Company: Pricing, Blog, Customers, Changelog, About, Contact
us, Careers, Terms of service, Privacy policy, DPA, Security, Trust center,
Subprocessors. The brand column carries the wordmark; a status line reading
`All systems operational` at `14px` weight `500` beside an `8px` filled dot in
the green accent family; five social marks; two circular `48px` compliance badges
drawn as outlined circles with a hairline ring containing set type at `8px`; and
the copyright `(c) 2026 Roomstack Inc.` at `12px` in the subtlest step, right
aligned. **The status line is live**: it reflects a real availability signal and
links to the status surface, because a hard coded green dot will still be green
during an outage.

**Hover states** outside the account and documentation routes are reconstructed
from declared transitions rather than observed: the primary button's two per cent
darkening, the secondary button and chip's alpha rise, a text link's underline
appearing at one pixel in the current colour at reduced alpha, a link arrow
sliding and fading in, a card's edge ring brightening while its interior does not
move, a menu item's low alpha ground appearing fastest of all, the wordmark's
flare sweep running once, and a documentation link darkening on its light
ground with both pseudo elements following. **Every hover rule is gated on a fine
pointer**, because a hover state that latches on after a tap is the single most
common touch defect in a rebuild of a site like this.

### The public routes

| Route | Kind |
|---|---|
| `/` | marketing, home |
| `/realtime-infrastructure` | marketing, platform |
| `/multiplayer`, `/comments`, `/notifications`, `/ai-copilots` | marketing, the four feature pages |
| `/examples`, `/showcase` | galleries |
| `/devtools` | marketing, tool |
| `/pricing` | commercial |
| `/enterprise`, `/startups`, `/innovation-teams`, `/individual-builders` | buyer segments |
| `/solutions/{industry}` | eight industry routes |
| `/use-cases/{case}` | seven use case routes |
| `/technology/{integration}` | fourteen technology routes |
| `/customers`, `/about`, `/careers` | proof and company |
| `/docs`, `/blog`, `/changelog` | documentation subsite and editorial indexes |
| `/security`, `/trust`, `/status` | trust |
| `/privacy`, `/terms`, `/dpa`, `/subprocessors` | legal |
| `/contact`, `/contact/sales` | enquiry |
| `/auth/login`, `/auth/signup` | account |
| any unmatched path | the not-found route |

The eight industries are human resources, security and compliance, sales and
marketing tools, healthcare, creative tools, legal, architecture engineering and
construction, and education. The seven use cases are collaborative text editor,
collaborative whiteboard, collaborative creative tool, collaborative form,
comments, document browsing, and sharing and permissions. The fourteen
technology routes each pair the word collaborative with a named editor, framework
or state library, plus one route for hosting a shared document format, exist for
search, and are linked only from the footer.

**Address conventions.** No trailing slash: a request with one redirects
permanently to the form without. Lowercase: a mixed case path redirects
permanently. Filter state lives in the query rather than the fragment, so it
survives a share and a reload. The primitive selector on the platform route is
one query key with five legal values. Documentation anchors live in the fragment
and derive from a stable identifier rather than the heading text. Unknown paths
render the not-found route with a `404` status, never a redirect.

**The content model behind the routes.** A feature has a slug, a name, a one line
description, an accent token, hero copy, sections and related features. A
primitive has a slug, name, description, icon and demonstration. A segment has a
slug, a kind of industry, user, use case or technology, a name, a description and
a proof set. An example has a slug, title, preview, feature tags, technology tags
and source location. A showcase entry has a slug, company, title, preview and
link. A customer has a slug, name, logo geometry and a tier of wall, case study or
quote. A case study has a slug, customer, headline, body and metrics. A post has a
slug, title, excerpt, author, date, tags and body. A changelog entry has a slug,
date, title, body and tags. A plan has a key, name, description, monthly price,
annual price, credit allowance, feature bullets and call to action. A doc page
has a slug, section, title, body, anchors, and next and previous. The entitlement
and the meter are shared with the console rather than being site content.

**The conversions.** Get started, from the header, the hero and most section
ends, begins account provisioning; Get started for free does the same from the
free plan; Contact sales opens the stepped enquiry; Get a demo opens the same
enquiry pre-marked as enterprise; Browse examples opens the gallery; Sign in opens
the account route.

### Home

In order: the announcement pill; a centred hero with a headline, a lead, two
actions and an annotation; the demonstration frame over the bloom; the trust line
and logo wall; the concurrency statement; the primitive list panel; the benefit
grid; the collaboration headline with cursor badges; the architecture diagram and
its capability grid; the platform statement; the testimonial carousel; the
platform capability grid; the closing action block; the footer.

**The hero** is centred on the vertical axis. The headline
`Realtime infrastructure for multiplayer apps and agents` sets two lines wide and
four narrow in white on the display rule. The lead is the product summary at
`18px` on a `29.25px` line in the subtle grey. The primary action is a filled
white button reading Get started for free; the secondary is a ghost disclosure
reading Install with AI with a downward chevron, opening a small menu of the
assistant tools the product installs into. The annotation `Your app with
Roomstack` sits right of the actions with a curved arrow pointing down and left
at the frame.

**The bloom** is the single largest visual element and the only saturated colour
above the fold: an absolutely positioned `2000px` square soft cloud in the
product pink family with lighter passages toward white, blurred at `64px`, its
transform and background image changing with scroll, the noise drift over it,
extending past the frame on both sides at the wide width and reducing to a band
behind the frame below the medium width. It is generated rather than a large
decoded image, because it is above the fold and it is the largest paint on the
page.

**The primitive list** is one split panel: the headline
`Realtime sync is the foundation of collaborative AI.` at the left and five rows
at the right: Presence, Online users, cursors, selections; Broadcast, Temporary
event signals; Storage, Synced data and file storage; Notifications, Smart alerts
for your app; AI Copilots, Individual AI assistants. The marks in this one list
are shaded lit objects while every other icon in the product is flat, and that
contrast is what makes the list read as the product's core rather than as a
feature list.

**The trust line** reads `Trusted by leading engineering, product, and design
teams` at `16px` in the subtle grey, centred, above two rows of five customer
wordmarks drawn as inline geometry in a single foreground at reduced opacity, so
every mark reads at the same weight whatever its own brand colour. That treatment
is what makes a logo wall look considered rather than like a sponsor list. It
wraps below the wide width, and on the pricing route the same wall scrolls
horizontally and continuously.

**The concurrency statement** is a left aligned paragraph alone on the page,
headed `Realtime infrastructure for collaborative AI.`, reading `When people and
AI agents work on the same data, concurrency becomes the problem. Roomstack keeps
everything in sync so updates stay consistent.`, with `concurrency becomes the
problem` and `updates stay consistent` in white.

**The benefit grid** is two by two, sharing hairline edges, each cell a capability
mark above a heading and two lines: Keep your users engaged, Collaborative
products keep your users active, invested, and coming back; Onboard users
faster, drive adoption, AI copilots help your users succeed from day one,
shortening time to value; Unlock new revenue opportunities, Monetize
collaboration and AI with premium or usage-based plans; Ship faster, stay
focused, Skip months of engineering work, Roomstack handles it all for you.
Beneath it in the same panel, the display line `Magic happens when humans and AI
collaborate.` carries two cursor badges over its second line, one labelled AI in
the product pink and one labelled Human in a neutral grey. The badges are the
brightest elements in the block, so the eye reads them first and the headline
second, and that inversion is deliberate.

**The architecture diagram** shows a client node, a dotted connection path
animated as a marching dash, a labelled Storage node carrying a small lit mark, a
server rack mark, and a chip reading Ping that appears, holds and fades on a loop,
over the graph paper ground, with nodes at a `6px` radius in the hairline ring and
labels in the letterspaced label. Beneath it, a two by two capability grid:
Conflict resolution, concurrent edits are merged automatically; Realtime
collaboration, see changes instantly with synced data, presence, and events;
Offline support, keep working offline and changes sync automatically when
reconnected; Multiplayer undo/redo, each user maintains their own history, even
in shared environments. Then the platform statement `Behind every Roomstack
feature is a battle-tested platform built for scale, reliability, and security,
trusted by teams shipping to millions of users.` with `battle-tested platform`
in white, and a second grid: Effortless scaling, Built to handle any traffic on
your collaborative experiences; Minimal configuration, Scale to millions of
users, no complex configuration required; No maintenance required; and
Enterprise-ready security. Those four capability statements are the public form
of the guarantees the platform half of this brief specifies.

**The closing block** `Turn your product into the space where people and AI
collaborate` repeats at the foot of the home route and every feature route with
the two primary actions, and on feature routes a panel headed `More than just`
followed by the feature name lists the other three features as cards.

**The not-found route** keeps the full header and footer and fills one viewport
without scrolling: a display status number, the heading `That address does not
exist`, and two actions reading Return home and Search the documentation.

### Realtime infrastructure

The platform route sells the machinery to the engineer who has to justify the
choice. It opens on a full bleed **dotted world map**: a regular dot lattice masked
to a coarse landmass, the dots a low alpha white, a handful of `2px` lit points in
full white marking the hosting regions, and a bottom dissolving through the
section base fade. The lit points are the visual argument for multi region
hosting.

Its central interaction is **the primitive switcher**: five primitives, Presence,
Broadcast, Storage, Feeds marked Beta, and Threads, one selected, in a keyboard
operable tab list whose current primitive is a query key. Selecting one cross
fades a panel labelled Realtime room showing a connection count and a participant
list that mixes people with named roles and machine agents with named runtimes,
each with a decorative disconnect control, animating the panel height rather than
jumping. Arriving with the key selects that primitive without animating; an
unknown value falls back to the first primitive and rewrites the address; the
panel is announced on change; and the switcher works from the address alone,
because the five primitive links in the header menu point here with a query key.
Both kinds of participant appear in one list with the same treatment, differing
only by a small runtime label, which is the product's central claim drawn as a
list. The statement reads `Realtime sync is the foundation to collaborative AI.`
and `AI multiplies the number of entities working in your product. Roomstack
keeps everything in sync, so concurrent edits and conflicts are handled
automatically.`, followed by Get started for free and Contact sales.

### The four feature pages

One template, four hues. The eyebrow is a shaded mark plus the feature name; then
the headline and any lead; two actions, a filled Get started for free and a text
link to sales or a demo; a row of three attribute chips on two of the four; the
demonstration; three to five capability sections, each a headline plus a
demonstration; a code surface; a platform trust grid; the `More than just` cross
links, generated from the feature model and never listing the current feature;
and the closing block. Each hero carries a glow in its own hue: across the middle
of the hero for multiplayer, deepest at the horizon where the cards begin; a warm
wash from the top for comments; a mint glow rising from the bottom for
notifications; and a saturated field filling the demonstration panel itself for
AI copilots.

**Multiplayer**, centred, headed `Add realtime collaboration to your product
experience`, with Get started for free and Contact sales. Its demonstration is a
horizontally scrolling row of four framed panels moving continuously right to
left at about one panel width every few seconds, faded at both edges, pausing on
hover and on focus within, and static on its first two panels under reduced
motion: Flowcharts, a node graph with two cursors and a selected node; Forms,
three labelled fields reading Project name, Team and Access level, two of them
with a two pixel focus ring in a participant's colour and a small name tab
attached to the ring's top right corner, which is the clearest single
illustration of what the product does; Whiteboards, a drawn shape, an avatar and a
comment bubble reading `Try a darker color?`; and Sheets, a grid with two coloured
cell selections. Later blocks cover text editors, a fully managed backend for sync
engines, and the developer experience.

**Comments**, centred, headed `Enable feedback in your text editor effortlessly`,
with the words text editor carrying an amber selection highlight and a caret bar
at its left edge. Three chips beneath the actions read Realtime, Customizable and
Accessible, and floating skeleton comment cards at low opacity scattered outside
the reading column give the page depth. **The theming demonstration** carries a
theme control of light and dark, a corner radius control of three corner glyphs,
and an accent control of six swatches, a purple, a red, an amber, a green, a blue
and a grey. Any control re-themes a live comment thread beneath it, with avatars,
names, relative timestamps, bodies, a mention chip, reaction chips, a resolve
control, and a composer with at-mention, emoji, attachment and a filled send
control. Changing a control changes variables at one scope root and rewrites no
component rule; the chosen combination survives a reload; the controls are grouped
radio sets whose options have accessible names beyond their colour; and **every
one of the eighteen combinations holds the text contrast threshold**, verified
across the full product rather than a sample, since the pale accent on the light
theme is the combination that fails. The theming section reads `Default
components`, `Make it your own`, `Default components allow you to customize
colors, spacing, and more, via CSS variables and classes.` and `Learn more`, and
its code surface on graph paper carries three file tabs, Comment, Composer and
User. Then `OPEN-SOURCE EXAMPLES` and `Explore our examples`. Narrow, the
demonstration contexts become a horizontal pill row, each pill in its own context
colour.

**Notifications**, centred, headed `Embed an inbox in your app and keep users
coming back`, with Get started for free and Book a demo. Its demonstration shows
the same event twice, split in two panels: at the left an in product inbox headed
`Notifications (4)` with entries by Alicia reading `We should show this to the
rest of the team!`, by Nimesh reading `@Alicia I've updated the copy on the
homepage. Please review and let me know if there are any changes you'd like to
make.`, and by Jonathan; at the right the email it becomes, from `Alicia via
Northlake` to a recipient with the design team copied, opening `Hello Olivier,`
and `Alicia left a comment in "Comments - Design explorations".` Later blocks cover
intelligent notifications, pre-built components and custom notifications.

**AI Copilots** is the only split hero, copy at the left and a saturated pink
panel at the right holding a chat with a Chats header, a back control, a New chat
control, a message region and a composer with a send control, with a named
cursor badge at its top right and a badge labelled AI at its lower left. It is
headed `AI assistants that can take actions on behalf of the user` with the lead
`Add AI assistants with domain-specific knowledge that can take actions on behalf
of the user.` A four column row beneath reads: Bring your LLM, connect any model
provider; Context-aware AI actions, your AI understands your app's state; No AI
expertise required, no AI plumbing, just add a chat component; and Collaborative
by design, we've spent years perfecting realtime collaboration. Later blocks cover
managed knowledge infrastructure, custom interface in chat, plugging in your own
model, custom tool calls, and a two column comparison of what a customer would
have to build from scratch against what the product provides.

Every horizontally scrolling row on these pages pauses on hover and focus and is
reachable by keyboard, because a moving row that cannot be stopped is unreadable
for many people.

### Examples, showcase and devtools

**Examples**, headed `Open-source examples built with Roomstack`, is a sticky rail
at the left and a card grid at the right. The rail carries a technology select
with a leading code icon defaulting to `All technologies`, then the categories All
examples, AI, Avatar stack, Code editor, Comments, Creative tool, Cursors, Forms,
Notifications, Productivity, Text editor and Whiteboard, each a link with a
`16px` leading icon, the current one on the slightly stronger fill at a `6px`
radius and marked as current rather than only styled. Category and technology are
both query keys, compose, and survive a reload and a back navigation, and choosing
a category does not clear the technology. The grid is two columns above the large
width and one below; each card is a light preview panel, the only light surface on
the marketing site, then a title, then a framework mark and a row of feature marks
at the bottom right, the cursor for multiplayer, a speech shape for comments, a
bell for notifications and the sparkle for AI, each named. Cards share hairline
edges, so the grid reads as one ruled sheet, and **every card reserves its preview
area before the preview renders**, so the card under the pointer never moves. Three
empty states cover no results for the category, for the technology, and for the
pair, each restating the filters and offering to clear each independently.

**Showcase** is a three column grid of larger cards sharing edges in both axes,
with titles including Multiplayer canvas with a whiteboard library, Collaborative
document editing, Private comment threads, AI slideshow editor, Conflict-free
multiplayer editing, Realtime spreadsheet editing, AI presence highlighting
changes, Inline AI comments, and Workflow automation nodes. Its previews are
composed animated miniatures rather than recordings.

**DevTools**, headed `Inspect collaborative experiences` with `Visualize your
collaborative experiences as you build them, in realtime. See how your data
structures are resolved and how they change over time.`, presents the browser
extension with a storage panel showing an expandable document tree, a presence
panel showing connected participants and their attached data, a note that
everything updates as it happens, and a note that it works in light and dark.
Those two panels are the public form of the room inspector and are composed from
the same components.

### Pricing

In order: the headline `Pricing` and the lead; the billing period toggle; four
plan cards; the scrolling logo wall; the comparison matrix in grouped sections;
the metered rate table; the questions; the closing block.

**The period toggle** is a full round pill with two options, Monthly and Annual,
the second carrying a badge reading `2 months free` in the green accent family at
`12px` weight `500`. The selected option sits on the slightly stronger fill with
white text and the unselected on no ground in the subtlest step. It is a grouped
radio control rather than two buttons, and the chosen period is a query key that
survives a reload and a back navigation.

**The plan cards** share hairline edges in one row above the large width and
stack below it.

| Plan | Description | Annual | Monthly | Under the price |
|---|---|---|---|---|
| Free | For personal development, prototyping, and testing. | Free | Free | No credit card required |
| Pro | For developers shipping collaborative features. | `$25` | `$30` | per month billed annually |
| Team | For teams shipping collaborative features at scale. | From `$500` | From `$600` | per month billed annually |
| Enterprise | For organizations with premium security and partnership needs. | Custom | Custom | |

The Pro and Team cards carry a badge reading `Save 17%` at the top right when
annual is selected. Each card carries a feature list with a leading icon per row.
Free: Free monthly credits; Realtime infrastructure; Collaboration features;
Pre-built components. Pro: Everything in Free, plus `$30` monthly credits; Remove
Roomstack branding; AI Copilots re-index interval. Team: Everything in Pro, plus
`$600` monthly credits; Extended version history; Higher webhook event frequency;
More simultaneous connections; Public/private comments. Enterprise: Everything in
Team, plus Volume discounts; Multi-region hosting; Management API; SCIM &
directory sync; Advanced permissions; Advanced support. The Team card also carries
a credit selector reading `$600 credits` with a badge reading `Save $100` and a
chevron, opening a list of credit tiers between the published floor and ceiling,
and choosing a tier changes the card's price. **Every figure on this route is an
integer in minor units, and the annual figure is read from a published annual
rate, never derived from the monthly one.**

**The metered rates** read: Realtime collaboration minutes, `$0.002` per minute;
Comments created, `$0.01` per comment; Realtime data storage updates, `$1` per
`1M` updates; Realtime data stored, `$0.15` per gigabyte; Monthly custom
notifications, `$0.005` per event; File storage, `$0.15` per gigabyte. Beneath
them: `Credits reset at the start of each billing cycle and do not roll over`.

**The comparison matrix** is the largest component on the public site and every
cell is read from the entitlement table. Each cell that renders an entitlement
carries `data-entitlement` set to `<plan>.<key>`, such as
`enterprise.connections_per_room`, and its visible text is the value itself for an
integer, Unlimited or Custom for those words, and a check mark or a dash for a
boolean. Its header carries the four plan columns
with calls to action reading Get started for free, Upgrade to Pro, Upgrade to
Team and Contact sales, each with a trailing arrow, sticky within the table and
offset by the header height property. Row groups each carry a heading spanning the
label column: Collaboration features; Realtime data storage; Sync engines; Version
history; Agents; Roomstack AI Copilots; Platform; Authentication; Access
security; Compliance. A hairline separates every row and every column; a cell
holds a check mark, a dash, a number, a duration or a short phrase; hovering a row
highlights it across all four columns behind a fine pointer; and a defined term
carries a dotted underline whose explanation is reachable on hover, on focus and
on tap and is associated with the term rather than held in a title attribute.

Notable rows: Pre-built components on every plan; Remove Roomstack branding,
absent on Free; Monthly active users and Monthly active rooms, Unlimited on all
four; Simultaneous connections per room, `10`, `10`, `50`, `100`; Multiplayer
undo/redo and Offline support on every plan; Webhook events frequency, `60
seconds`, `60 seconds`, `30 seconds`, Custom; Realtime data storage updates, `3M`
included then `$1 per 1M updates` on the middle two, Custom; Realtime data stored,
`1 GB` included then `$0.15 per GB`, Custom; Realtime data stored per room, `10
MB`, `10 MB`, `50 MB`, Custom; both sync engines on every plan; Version history,
`24 hours`, `30 days`, `90 days`, Custom; Agent frontend actions and Agent activity
feeds on every plan; LLM, three named providers on every plan; Model
configuration on every plan; Knowledge RAG, Websites, PDF and Images on every
plan; AI Copilots re-index interval, absent on Free; Developer dashboard, the edge
network, the connection engine and Webhooks on every plan; sign in providers on
every plan; Multi-factor authentication on every plan; SAML SSO, absent, absent,
present, present; Directory sync (SCIM), present on Enterprise only; Role-based
access control, Team level, Team level, Team level, Team and project levels; SOC
2 Report, absent, absent, present, present; HIPAA BAA, absent, absent,
`$350/month`, present; Custom security reviews and the `99.99%` uptime SLA on
Enterprise only. The platform section lead reads `Realtime infrastructure,
monitoring dashboard, tools, and more.` At the narrow width the table becomes one
panel per plan with the group headings repeated inside each, dropping no content
and scrolling nothing sideways.

**The questions**, the frequently asked questions block, are an accordion, all closed by default, more than one open at
a time, each a disclosure with an expanded state and addressable by fragment so a
deep link opens it on arrival, its height animating on the expressive out and not
under reduced motion: `How does pricing work in Roomstack?`, `What counts as a
realtime collaboration minute?`, `Which Roomstack plan should I choose?` and `Can
I try Roomstack before paying for it?`. The second answer is the same sentence the
meter implements: a room accrues collaboration minutes while it holds two or more
concurrent connections, and a room with one participant accrues none.

### Enterprise, segments, industries and technologies

**The enterprise route** carries, in order: the eyebrow `ROOMSTACK FOR
ENTERPRISE`; the headline `Modernize with realtime collaboration` with two named
cursor badges beside it, one grey and one blue, as its only ornament; the lead
`Your users expect Figma and Notion-level collaboration. Modernize in stages,
from ready-made features to a full sync engine, without a rewrite.`; one action,
Get a demo; three trust chips; the staged adoption grid; the notification feed;
the self hosting and enterprise controls pair; the architecture diagram; the
compliance badges; a testimonial; the sales enquiry inline; the footer.

The trust chips are one row, each a `16px` check mark and a `12px` phrase in the
subtle grey: `SOC 2 Type II & HIPAA`, `99.99% uptime SLA` and `Dedicated solutions
engineer`.

The staged adoption grid opens with the statement `The collaboration layer for
enterprises modernizing products customers rely on every day.` and five panels,
each with a live demonstration inside:

| Panel | Body | Demonstration |
|---|---|---|
| Start with ready-made features | Ship Comments, Notifications, and Multiplayer in weeks with drop-in components. | a checklist animating through Comments live in the product, Notifications in the rolling out, and Multiplayer editing next, under two cursor badges |
| Graduate to the full sync engine | Move core surfaces onto Storage and Yjs one at a time. No big-bang migration. | a document with a text selection and two comments with a reaction |
| Partner with the Roomstack team | Dedicated engineer, private Slack, and custom SLA for confident rollouts. | a feed of console notifications |
| Run Roomstack in your cloud, badged Soon | Own your data while Roomstack keeps you updated, secure, and supported. | the architecture diagram |
| Enterprise controls & compliance | Multi-region hosting, SSO, SCIM, and RBAC, plus SOC 2, HIPAA, and a GDPR DPA. | two compliance badges captioned SOC 2 and HIPAA |

The notification feed is a stack of cards, each with a leading mark, a body and a
relative time: a meeting mark, `Quarterly architecture review, with a solutions
engineer`, `15m ago`; a bell, `Alicia created a new API key for Production`, `30m
ago`; an envelope, `Roomstack: Your monthly usage report is ready. Connections,
monthly active users, and storage across...`, `45m ago`; a bell, `Marc invited you
to Production readiness review`, `1h ago`. It is the only public view of the
console's own notification surface, and its second entry is a key creation
surfaced to the organisation as it happens.

**The architecture diagram** on this route shows three nodes on a dotted field
labelled `Your app`, `Your database` and `Roomstack Sync`, the last in a blue ring
with a cursor badge attached, joined by right angled paths: the customer keeps
their application and their database, and the sync layer is run for them.

**The buyer segment routes**, enterprise, innovation teams, startups and
individual builders, share one template: a segment headline, a three panel
statement of the segment's problem, a proof set from the customer model, and a
closing action that routes enterprise and innovation to sales and startups and
individual builders to account provisioning. **The eight industry routes** add an
industry proof set and, where the industry has one, a compliance statement; the
healthcare route states the health regime position accurately rather than
generically; and the industry heroes carry the light streaks and the noise drift.
**The seven use case routes** each pair one use case with the feature that serves
it and one worked example. **The fourteen technology routes** carry a hero naming
the technology, a code surface showing the integration, a link to the matching
example and the closing block. All of these are **generated from the segment model
rather than hand authored**, because thirty near-identical hand written routes
diverge and the divergence is invisible until a customer notices one is two
versions out of date.

### Customers, about and careers

**Customers** carries a headline and lead, a logo wall larger than the home
route's, featured case studies as cards, a quote, a long tail list, and the
closing block. The case study headings read `How Northlake transformed email
collaboration with realtime multiplayer editing`, `How Pagewise built a one to one
meeting tool that rivals a mainstream document editor`, `How Tetrad used live
reactions to improve engagement on a livestream`, and `How Almanac powers
collaboration with Roomstack`. The long tail is a plain list of around forty
company names at `14px` in the subtle grey across three or four columns, and it is
not a logo wall, because at that count wordmarks are noise and names are
information.

**The testimonial carousel**, used on the home route, the enterprise route and the
sales enquiry, is a bordered panel sharing edges with its grid: a customer
wordmark at the top left, a quote whose load bearing first sentence is white and
remainder subtle grey with typographic quote marks outside the measure, and an
avatar with a name and a role, such as Dana Whitlock or Idris Bekele. Two square
buttons at the top right carry the chevrons. It advances manually only on the
enterprise route and automatically on the home route, pausing on hover and focus,
cross fading on the carousel curve. The region is a labelled group with a live
region politeness of off and an explicit slide count, and automatic advance stops
permanently on interaction.

**A case study** carries a hero with the customer name, headline and a metric
strip; a long form body with pull quotes and inline demonstration frames; a
sidebar with the customer's industry, size, the features they use and a link to
their product; and two more case studies at the foot. **About** carries the
company narrative, the team, investors and a values block on the segment
template. **Careers** groups open roles by function, each linking to a role page
with title, location, team, description, requirements and an application action,
and when no roles are open it says so in a sentence and offers a general enquiry
rather than rendering an empty list.

### Documentation, blog and changelog

**The documentation subsite is a different product.** It runs on a light ground
with its own chrome, its links darkening on hover and its link grounds shifting
through a light purple wash, which nothing else on the site does. Its chrome
carries the same wordmark dark on light; a primary navigation of Documentation,
Guides, Tutorial and Examples with the current one on a light purple ground in
brand purple text; a repository mark with a star count; a search field reading
`Search or ask AI...` with a keyboard chord chip; a Feedback control and a dark
Sign in button; a scrollable left rail of expandable groups whose top level is
Overview, Get started, Concepts, Authentication, Collaboration features,
Integrations, Platform, Pricing, Tools and Upgrading; and a right rail of on page
contents with the current heading marked by a filled bar. The landing page carries
the product sentence, Get started and Browse examples over a large dotted outline
of the cursor mark, and four card groups: Collaboration features, API Reference,
Examples and Community. Its pages document Roomstack's own admission surface, the
approval calls and the outbound event catalogue.

Documentation behaviour: anchors derive from a stable identifier so a reworded
title breaks no inbound link; a deep link scrolls with the sticky header offset
accounted for rather than landing under it; the left rail marks the current page
and preserves its own scroll across navigation; the right rail tracks the current
heading by reading position rather than the scroll midpoint; search opens on the
chord shown in its chip, traps focus, restores it on close, and its results are
keyboard navigable; code blocks scroll horizontally within themselves and the page
never scrolls sideways; the copy control announces success and is never a bare
unnamed icon; and next and previous links at the foot of every page follow the
tree order.

**Code surfaces** have a `12px` radius, the hairline ring, and a tab strip when
more than one file is shown, each tab a file mark and a name in JetBrains Mono at
`12px`. Line numbers sit in the subtlest step and are not selectable. The body is
JetBrains Mono at `14px` on a `20px` line. On marketing routes the ground is graph
paper behind a transparent panel; in documentation it is a light neutral panel.
Inline code carries the inset hairline, highlight colours come from the accent
family, and marketing code that appears to be typed is complete in the markup and
does not animate under reduced motion.

**The blog** lists posts with title, excerpt, author, date and tags, filters by tag
in the address, and pages by cursor rather than page number. **The changelog** is a
dated, reverse chronological list of entries, each with a date, a title, a body
and tags naming the affected product area, and **every entry is individually
addressable by fragment**, because linking to one specific change is what a
changelog is for.

### Security, legal, trust and status

These routes exist to be sent to somebody in a procurement conversation who is
looking for a reason to say no. They are long form prose with no decoration.

**Security** sits on the dark ground with the site chrome, its section headings at
`24px` weight `500` and its body at `16px` on a `24px` line in the subtle grey,
with two compliance badge marks inline where they are discussed. Its headings run:
Organisational security, covering compliance documents, the information security
program, independent audit certification, health information compliance,
third-party audits, third-party penetration testing, roles and responsibilities,
security awareness training, confidentiality and background checks; Cloud
security, covering cloud infrastructure security, data hosting security,
encryption at rest, encryption in transit, vulnerability scanning, logging and
monitoring, business continuity and disaster recovery, and incident response;
Access security, covering permissions and authentication, least privilege access
control, quarterly access reviews, password requirements and password managers;
and Vendor and risk management, covering annual risk assessments and vendor risk
management. Its statements read: `We have an information security program in
place that is communicated throughout the organization.`; `Roomstack is
independently audited to the common security controls standard. Access to the
report requires the third plan.`; `Roomstack supports the health information
regime for enterprise customers. Access to that documentation requires the third
plan with the health add on.`; `Our organization undergoes independent
third-party assessments to test our security and compliance controls.`; `We
conduct independent third-party penetration testing at least annually.`; `All
databases are encrypted at rest.`; and `Our applications use encrypted transport
only.` The two access statements link to a documents surface inside the console.

**Trust** presents the same compliance posture, the sub-processor list and the
current status as a route in this build rather than an externally hosted service.
**Status** shows current availability by component, the realtime plane, the
management interface, the console and the documentation, with an incident history
and the service level objectives. **Privacy** states what the product stores about
a customer's members and end users and how long it is kept; **Terms** carries the
terms of service; **DPA** carries the data processing addendum, one of the longest
documents on the site; and **Subprocessors** is a table of processors with the
purpose and the location of each, and the location column is the public form of
the residency rule rather than decoration. Every legal route carries a last
updated date, an anchored table of contents and individually addressable sections.

### Contact sales

A stepped enquiry rendered as its own route and inline at the foot of the
enterprise route, with the eyebrow `SCHEDULE A CALL` and the headline `Let's talk
about your use case` inline, or `Talk to our sales team` standalone with the lead
`Contact sales to discover the value of Roomstack for your company and explore our
custom plans and pricing. If you have technical questions, feel free to contact
support.` Two panels share a hairline, the form at the left and the testimonial
carousel at the right, which moves below the form at the narrow width.

| Field | Type | Required | Placeholder or options |
|---|---|---|---|
| First name | text | yes | none |
| Last name | text | yes | none |
| Work email | email | yes | none |
| Company size | select | yes | Select size, then `1-10`, `11-50`, `51-200`, `201-1000`, `1000+` |
| Role | select | yes | Select role, then `Engineering`, `Product`, `Design`, `Executive`, `Other` |
| What are you interested in? | multi line text | yes | Share more about your use case, product, tech stack, and what you want to accomplish |
| Website | text | no | none |

Required labels carry an asterisk appended, and are also marked in the accessible
name. Fields have an `8px` radius, the field ring and a placeholder in the
subtlest step. Selects are real selects with the chevron at their right. The form
is staged with Previous, Next and Continue: the step is in the address so a
partially completed form can be returned to; values are preserved backward and
forward including the free text; validation runs on blur and on step advance and
never on every keystroke of a field not yet blurred; an invalid advance moves focus
to the first invalid field and announces the count of problems; the draft is kept
on the device and restored on reload and cleared on success; progress shows how
many steps remain; and the whole form, both selects included, completes without a
pointer.

The submission is validated on the server against the same schema the client
uses and answers with a per field map. **The enquiry is recorded before any
delivery is attempted**, so a mail failure does not lose the lead; a duplicate
submission within ten minutes returns the original identifier and creates one
record; a submission arriving within two seconds of the form being issued is
refused; the submission records the consent text version shown; and if delivery
fails the person sees a fallback contact route with their values intact.

### Sign in and sign up

The account routes carry no site header and no footer: a centred column on the
black ground with the mark alone, without its letterforms, at `24px` above a
heading of Sign in or Sign up at `24px` weight `500`, a card of about `440px` at a
`12px` radius on the raised surface in the hairline ring, and a `14px` legal line
at the foot in the subtle grey reading `By creating an account, you agree to the
Terms of Service and Privacy Policy`.

**Sign in** carries email and password fields, a Continue action, a hairline
divider with the word OR centred over it in `12px` uppercase, and federated
provider buttons, full width on the secondary ground with the provider mark at the
left and a label reading Continue with the provider's name. The focused field
carries a brighter ring. Sign in hands the credentials to Keycloak.

**Signup is closed in this build.** `/auth/signup` renders the account layout and
the measured card, with First name, Last name and Email fields whose placeholders
read `Your first name`, `Your last name` and `Your email address`, a Continue
action, the OR divider and the footer line `Already have an account? Sign in`,
and submitting it records an enquiry and creates no account.

Sign in, password reset and invitation acceptance return the same response and
take a similar time whether or not the address exists. A federated identity is
created or linked by the provider's stable subject and never by address. An
address in a domain claimed by an organisation's identity provider is sent into
that flow. Arriving from an invitation pre-fills and locks the address and binds
the membership on completion. A second factor is offered after the first sign in
and required for organisation owners. **The destination a person is returned to
after signing in is carried through the whole flow and validated against an
allowlist**, so a genuine link to this sign in page cannot bounce a newly signed
in person to another origin.

### The console shell

The console inverts every property of the public site: it is authenticated, per
organisation, almost every screen writes, and no two organisations ever see the
same bytes. Its visual design is a proposal consistent with the design system
above rather than a reproduction.

Three regions are fixed for the life of a session: an **organisation rail**,
`56px` collapsed and `240px` expanded, carrying the organisation switcher, the
project list, the environment badge and settings; a **context bar**, full width
and `48px` tall, carrying the breadcrumb, the environment selector, search, the
notification bell and the account menu; and the **work surface**, which scrolls
independently of the rail and is the only region replaced on a route change, so a
room inspector keeps its live view while the operator moves around.

The **organisation switcher** lists every organisation the principal belongs to
and a create affordance, and switching is a hard navigation that closes every open
connection, clears every cached query and re-authenticates, because anything less
leaks one organisation's room list into another's screen through a warm cache.
The **environment selector** lists the project's development and production
environments; production carries a persistent tinted band across the top of the
context bar, and every destructive control inside it requires a typed
confirmation. Both selectors are combo boxes with type ahead, keyboard reachable,
and round trip through the address.

In a console address `{org}` is the organisation slug, `{project}` the project slug
and `{env}` the environment kind, so the Atlas Editor production rooms live at
`/northlake/atlas-editor/production/rooms`. The approvals surface offers owners a
break glass action beside the queue.

The surfaces are `overview`, `rooms`, `keys`, `webhooks`, `copilots`, `usage`,
`audit` and `settings`, scoped to a project and environment, and `approvals`,
`groups`, `members`, `billing` and `security`, scoped to the organisation and
dropping the project and environment segments. A console link naming a project the
principal cannot read renders the not-authorised state and never a redirect to the
overview, because a redirect tells the reader the project exists.

**Destructive confirmations** come in three tiers decided by blast radius rather
than by how a control looks: reversible actions, such as archiving an endpoint or
disabling a copilot, offer an inline undo for ten seconds with no dialog;
irreversible actions on one resource, such as deleting a room or a version, open a
dialog naming the resource with a single confirm; and irreversible actions on many
resources, such as deleting a project, rolling a production secret or deleting an
organisation, require the resource name typed exactly, compared case sensitively
after trimming surrounding whitespace and nothing else, plus a second factor where
one is enrolled. A confirm control that enables on any non empty string is a speed
bump, not a confirmation.

**The not-authorised state** names the permission required and the role that
carries it and offers one action, request access, which opens the approval
workflow with the target resource filled in. It never names other members, never
says whether the resource exists, and never renders a partial surface behind a
blur, because a blurred surface is a rendered surface and the data reached the
client.

**The keyboard model**: `Cmd/Ctrl K` opens the command palette over rooms,
projects, surfaces and members; `g` then `o` opens the overview, `g` then `r` the
rooms, `g` then `u` the usage, and `g` then `a` the audit; `/` focuses the
surface's own filter; and `Esc` closes the topmost overlay, then clears the filter,
then blurs. A sequence chord is cancelled by any key outside it and by a `1000ms`
timeout, and every chord is also a visible control, because a keyboard only route
to a feature with no pointer route is an accessibility defect.

The **approval queue** is a queue list: each row carries the action, the requester,
the state as a word and a badge, the impact counts, and the time remaining before
expiry, newest first, filterable by state in the address. The **wizard** is three
routes, `/{org}/approvals/new/action`, `/{org}/approvals/new/arguments` and
`/{org}/approvals/new/review`, and every value survives at every stage including a
reload. Outcomes are confirmed with a **toast** that enters past the outer gutter
and carries the request identifier.

### Module and component architecture

Four layers, and dependencies point one way only.

| Layer | Contains | May depend on |
|---|---|---|
| Tokens | every value in this section, as declarations only | nothing |
| Primitives | button, link, input, select, textarea, chip, badge, card, panel, disclosure, tabs, menu, tooltip, popover, sheet, toast, avatar, avatar stack, skeleton, code block, table | tokens |
| Compositions | header, menu panel, drawer, footer, hero, demonstration frame, cursor badge, plan card, comparison matrix, gallery card, thread, composer, inbox entry, chat, notification card, carousel, accordion | tokens, primitives |
| Routes | every public route and every console surface | everything above |

A primitive that imports a composition is the defect that turns a component
library back into a pile of markup. The primitives that carry the most weight are
the panel, which holds the hairline ring, the shared edge behaviour and the radius
set; the disclosure, which is the menus, the drawer groups, the pricing questions
and the documentation rail with different presentation; the tabs, which are the
demonstration tab strip, the primitive switcher, the code file tabs and the room
inspector; the skeleton, which is the shimmer reused for every console loading
state; and the cursor badge, the product's central metaphor.

**State ownership follows one rule: if two people would want to see the same
thing, it belongs in the address.** A demonstration's tab selection belongs to the
composition, with its timer cancelled permanently on interaction. The primitive
selection, gallery filters, pricing period, documentation anchor, and the
console's organisation, project, environment and surface belong to the address.
The theming demonstration selection and the enquiry draft are kept on the device,
with the enquiry step also in the address. Console data lives in a query cache
keyed with the organisation identifier; room state lives on the server; the
session lives in its bearer token and its server side row.

Inside the console three further layers sit beneath the surfaces: one data access
client with one error shape, one retry policy and one cache key derivation; one
policy client asking the single authorisation question once per surface; and one
connection manager shared across surfaces that survives route changes within an
environment.

**What is deliberately not a component:** a page layout wrapper taking a variant,
because four routes with a variant flag become four routes with eleven flags; a
generic icon component taking a name string, because icons are geometry imported
individually so unused ones are not shipped; a theme provider that swaps palettes,
because the accent is one scoped declaration; and a modal manager, because the
public site has two overlays, the drawer and the popover, and both are locally
owned. The four collaboration features share the room but not each other, so a
failure in one never stops the other three, so their work is parallelised rather
than chained; and the governance half and the commercial half of the console share
the record and nothing else.

### No asset file is fetched anywhere

The reference ships hundreds of font responses, hundreds of megabytes of video,
several megabytes of raster imagery in webp, png and jpeg, two dozen vector files,
animated gifs and a few audio files. **This build ships none of them** beyond the
two openly licensed type families, and nothing in the build depends on an external
service for content this brief specifies.

- **Icons** are inline geometry, and the full set of seventy is transcribed as view
  box and path data.
- **The bloom** is a stack of three radial gradients on one `2000px` square
  element, blurred by `64px`: a near white core with a pink cast from the centre to
  about a fifth of the radius, the hot product pink through the body to about half,
  and fully transparent falloff to the edge. Two further gradients offset from the
  centre at low opacity break the symmetry, because a single centred radial reads
  as a lamp and this must read as a cloud; their offsets are proposed rather than
  measured. The per feature glows are the same construction with the route's hue
  substituted and the placement changed.
- **The grain** over it is an inline turbulence filter rendered once into a tiling
  data image: a base frequency around `0.9` for a fine grain at a `300px` tile, `4`
  octaves for tonal variation, zero saturation so it does not tint the bloom, about
  `0.08` opacity over the bloom, translated by the noise drift. Generate once and
  translate forever; never regenerate the tile per frame.
- **The handwriting** is two measured strings that never change, so they are drawn
  once as two paths, exactly like the icons, with the curved arrows already
  geometry. A different handwriting face would change the page's personality more
  than any other substitution.
- **Every video** becomes a composed miniature built from the demonstration
  primitives and animated on a loop: showcase previews become a miniature of the
  interface type with two cursors moving; feature route demonstrations become the
  variants above; documentation demonstrations become a still composition with one
  animated element. This substitution has honest limits: recordings of real
  products by real customers become schematics of the same idea, and it is the
  largest fidelity loss in the build.
- **The shaded primitive marks** are drawn per mark as a small lit sphere, torus or
  rounded cube: a radial ground from a mid grey at the upper left to near black at
  the lower right, one small bright specular spot at the upper left at about
  eighteen per cent of the radius, a thin brighter rim arc at the lower right at
  about four per cent of the diameter, and a soft dark contact shadow beneath at
  thirty per cent opacity. **The rim light does most of the work and is the detail
  usually omitted.** Without hardware acceleration the marks fall back to the flat
  icon set.
- **Customer wordmarks** are generated per company name: the display family at
  weight `600` at a fixed cap height, beside a glyph derived from a hash of the name,
  one of a circle, a triangle, a square, a chevron or a pair of bars, in a single
  foreground at the wall's reduced opacity, with letter spacing varying slightly by
  hash so the wall does not read as one repeated element. The long tail list needs
  no substitute because it is plain text.
- **Avatars** are generated: a two stop linear ground whose hue derives from a hash
  of the participant identifier at a fixed lightness, a simple abstract head and
  shoulders silhouette in a lighter tint of the same hue, the participant's initials
  centred in the display family at weight `500` as a fallback, and a full round
  shape. Hue derived from the identifier means the same participant is the same
  colour everywhere, and presence colour is how people recognise each other.
- **The dotted world map** is a hexagonal or square dot lattice at about a `6px`
  pitch, masked by a coarse inline landmass path of a few hundred proposed points,
  with `1.5px` dots in white at about four per cent alpha, `2px` lit points at full
  alpha over the hosting regions, and edges dissolving through the section base
  fade.
- **Audio.** No interface sound ships. If one is ever added it is generated, a
  short enveloped tone through a filter with its waveform, sweep and duration
  stated, off by default and behind a preference.

What the substitutions cost: fonts, small; the bloom and glows, small; the grain,
none; the handwriting, small; the shaded marks, moderate; video, large; wordmarks,
moderate, because a wall of invented marks demonstrates the layout and proves
nothing; avatars and the world map, small.

### Breakpoints and gutters

Six named widths, and each change is a reorganisation rather than a shrink. The
pixel ladder is the site's own and the only one used.

| Name | Width | What changes |
|---|---|---|
| narrow | below `520px` | single column throughout; the demonstration drops content; annotations suppressed |
| small | `520px` | two column card grids appear; plan cards remain stacked |
| medium | `768px` | the header's link set is still collapsed; feature grids go two wide; the comparison matrix is still per plan panels |
| large | `1024px` | the full link set appears and the drawer retires; the comparison matrix becomes a table; the examples rail becomes sticky |
| wide | `1280px` | four column plan cards; the demonstration reaches its full composition; annotations appear |
| widest | `1640px` | the page stops growing and centres; the bloom extends past the content column |

| Width band | Outer gutter | Inner gutter |
|---|---|---|
| narrow | `16px` | `16px` |
| small and medium | `24px` | `20px` |
| large | `32px` | `24px` |
| wide and above | `40px` | `32px` |

The gutter steps are inferred from measured margins. Per route: the header shows
the wordmark and menu control narrow and medium and the full link set with both
actions wide; the hero headline sets four lines narrow, three medium and two wide;
the demonstration frame shows one column of content with scrolling tabs and no
annotations narrow, most content without annotations medium, and the full
composition with annotations outside the frame wide; the logo wall runs two
columns wrapping narrow, three medium and two rows of five wide; benefit grids run
one column with horizontal hairlines only narrow and two columns above; plan cards
stack full width narrow, run two columns medium and four columns wide; the
comparison matrix is one panel per plan with group headings repeated narrow and
medium and a table with a sticky header wide; the examples rail is a horizontal
pill row narrow and medium and a sticky vertical rail wide; the examples grid is
one column narrow and two above; the showcase grid is one, two and three columns;
feature demonstration rows are a horizontal pill row of contexts narrow, reduced
medium and the full sliding row wide; the documentation hides both rails behind
two controls narrow, hides both medium and shows both wide; the enquiry form is
full width with the carousel below narrow and two panels side by side wide; and the
footer stacks its columns as disclosures narrow, runs two columns medium and four
columns plus the brand column wide.

Rules that hold at every width: no horizontal page scroll anywhere, though wide
content scrolls inside its own region; touch targets of at least `44px` in both
axes below the large width, including the tab strip and the category pills; every
hover rule behind a fine pointer query; the demonstration drops content rather than
scaling; the display rule interpolates continuously while body sizes do not change;
sticky offsets expressed against the header height property; and safe areas
respected at the bottom of the drawer and any fixed control. What must not change
with width: long form reading measure stays bounded at the widest width; the tonal
system stays the same, with body copy grey at every width and no mobile palette;
and **nothing available at a wide width is missing at a narrow one**. Content is
reorganised, never removed, with the single exception of decorative annotations,
because hiding a navigation item, a plan feature or a table row on a phone is a
content decision disguised as a layout decision.

### Accessibility

**The commitment.** One of the three chips on the comments route reads Accessible,
which makes accessibility a public claim about the components this product sells.
The target is the recognised success criteria at the AA level, plus the specific
requirements below.

**Structure.** One banner, one main and one content information landmark per
document, with the documentation rails complementary and each labelled. A skip link
is the first focusable element, visible on focus, and **moves focus rather than
only scrolling** to the main landmark. One level one heading per route with no
skipped levels, and the comparison matrix's group headings are real headings. A
unique page title per route, front loading the distinguishing words. The document
declares its language. On a console route change the new surface's heading receives
focus and the change is announced.

**Keyboard.** Header menus behave as described under global chrome. The drawer
traps focus while open, closes on escape, restores focus to its trigger, and
prevents background scroll. Tabs everywhere move with the arrow keys, jump with home
and end, associate their panel, and stop any automatic advance permanently on
interaction. Accordion headings are buttons toggled by space and enter. Carousel
previous and next are real named buttons, and automatic advance pauses on hover and
on focus within and stops permanently on interaction. Selects are native controls
whose chevron is decorative. The command palette opens on its documented chord,
traps and restores focus, and navigates results by arrow keys. Every feature is
reachable without a pointer and no feature exists only behind hover. **Focus is
never removed**, and its ring meets the non-text contrast threshold against every
ground it appears on, including the white primary button and the light
documentation ground.

**Contrast.** Of the four foreground steps only three are safe for prose. White
passes at every size against black; the subtle grey passes for body; the subtler
grey passes for body at the sizes it is used, captions at `14px` and above; and the
subtlest step does not pass for body and is used only on placeholders, disabled
controls, decorative line numbers and ornamental display type. Every combination of
the theming demonstration's eighteen states holds the threshold, verified across the
full product of the options.

**Names, roles and values.** Icon only controls carry an accessible name: the copy
control, the carousel arrows, the theme switches, the drawer trigger. Each feature
mark on a gallery card carries a name. The status dot's state is in text and not
only colour. A plan card's saving is in text. Required fields are marked in the
accessible name and not only by an asterisk glyph. Error messages are associated with
their field and announced. The comparison matrix is a real table with header cells
in both axes and a caption. Live regions are assertive for the enquiry error
summary, polite for console job progress, and off for the carousel.

**Motion, media and pointers.** Reduced motion is honoured as described above.
Nothing flashes more than three times a second. Everything that moves on its own can
be stopped. The demonstration frames, cursor badges, bloom, grain and dot map are
hidden from assistive technology, each with a text alternative adjacent where it
carries meaning. Every content image carries alternative text, and a decorative one
declares itself decorative. No functionality requires a drag, a multipoint gesture
or a path, and every hover only affordance has a tap or focus equivalent.

**Forms.** Real labels rather than placeholders; validation on blur rather than per
keystroke; focus moved to the first error; the error count announced; values
preserved across steps.

**The components the product sells.** The composed comment, composer, inbox and chat
components become part of customers' products, so their accessibility is a supply
chain property. Each is operable by keyboard alone in isolation, because a customer
may render one on an otherwise inaccessible page. Each carries its own accessible
structure rather than depending on the host page's landmarks or headings. The
composer's rich text region announces its formatting state and presents its mention
suggestions as a listbox. Every string is externalised and none is composed by
concatenating fragments, which breaks in most languages. And the theming variables
cannot be set to a combination that fails contrast without the component reporting
it in development, so a customer who picks a pale accent is told they have made
their own product unreadable.

### Performance

Measured on a mid range laptop on a slowed connection and on a mid range phone,
for the home route:

| Metric | Budget |
|---|---|
| first contentful paint | `< 1.2s` |
| largest contentful paint | `< 2.0s` |
| cumulative layout shift | `< 0.05` |
| interaction to next paint | `< 200ms` |
| total blocking time | `< 200ms` |
| compressed script on first load | `< 180kb` |
| compressed style on first load | `< 40kb` |
| frames during scroll | `60` per second sustained, no frame over `16ms` in a `5s` scroll |
| console surface first meaningful render | `< 1.0s` on a warm session |
| room connection established, ninety fifth percentile | `< 500ms` |

The largest contentful paint on the home route is the demonstration frame on the
bloom, and both are generated rather than fetched, which is what makes the budget
achievable. The reference is font heavy and video heavy; this build is neither,
because it ships neither: two families subset and preloaded with a metric matched
fallback, no video, no raster imagery, and script bounded by the budget.

Loading: the header, the hero copy and the frame outline render from the initial
document without waiting for script; the bloom paints from style alone; the
demonstration's animation starts after the page is interactive; below the fold
compositions load on approach; the two faces above the fold are preloaded; nothing
third party sits on the critical path and analytics loads after interactivity; the
documentation search index loads on first open. During a five second continuous
scroll of the home route there is no layout read inside a write phase and no more
than two style recalculations per frame, and every scroll driven property is a
transform, an opacity, or a custom property feeding one; the one measured exception,
the bloom's changing background, is a custom property driving a gradient stop rather
than a replaced image.

Animation discipline: every loop, marquee, cursor path and carousel suspends when its
container is out of view; all animation stops when the document is hidden; the
layer promotion hint is applied only while an element animates and then removed,
because the reference declares it permanently on nearly eight hundred elements and
that promotes eight hundred layers on exactly the devices with least memory; and
anything running per frame animates only transform and opacity.

In the console the room list pages by cursor with no count query; the inspector's
document tree renders only its visible part so the list stays smooth when it is
long; live updates are collapsed to at most one render per animation frame rather
than one per operation; charts read the rollup resolution appropriate to their
window; and the query cache is keyed with the organisation identifier and cleared
entirely on an organisation switch.

### Degradation on the public site and in the console

Nothing here is allowed to fail as a blank page.

| Failure | Behaviour |
|---|---|
| script fails to load or execute | every route still reads: content is in the document, links work, and the enquiry form submits as a plain form to the same endpoint |
| a font fails | the metric matched fallback renders and nothing reflows |
| the bloom cannot be painted | the ground stays black and nothing else changes |
| hardware acceleration is unavailable | the shaded marks fall back to flat icons and the dot map renders as a static field |
| the status source is unavailable | the status line reads as unknown in neutral text and links through, and never reads operational by default |
| a gallery preview fails | the reserved area shows the card's title on a neutral panel and the grid does not reflow |
| the enquiry endpoint fails | the fallback contact route with the entered values intact |

In the console every surface implements its partial state. The overview renders the
tiles whose source is available and marks the rest unavailable individually. The
room list renders rows from the control plane while its live connection column reads
unavailable. The inspector may render its storage tab while its presence tab reports
unavailable. Usage renders its historical series while omitting the projection with a
note. **Audit is never partial**: if it cannot be read completely it says so, because
a partial audit view is a misleading one. Every error a person sees carries what
happened in one sentence, whether it is theirs to fix, what to do next, and the
request identifier, and never a stack trace, a raw provider message or an
untranslated code alone.

### Copy that is pinned

| Where | Exact words |
|---|---|
| product summary and home lead | `Roomstack provides the infrastructure to handle concurrent edits on shared data, so people and AI agents can collaborate without breaking your app.` |
| home section headline and subhead | `Unlock the secret sauce behind world-class products.` and `In just a few lines of code.` |
| demonstration app label | `Your app` |
| pricing lead | `Roomstack provides the realtime infrastructure to power human-AI collaboration at any scale.` |
| annual badge, saving badge | `2 months free`, `Save 17%` |
| status line | `All systems operational` |
| not-found heading and actions | `That address does not exist`, Return home, Search the documentation |
| documentation search | `Search or ask AI...` |
| self approval refusal | `You cannot approve a request you raised.` |
| impact growth refusal | `The impact of this change has grown since it was approved.` |

The twelve customer names are Northlake, Pagewise, Tetrad, Almanac, Fieldnote,
Cadence, Bramble, Foundry, Sundial, Loamwork, Kestrel and Hollow; the two quoted
people are Dana Whitlock and Idris Bekele; the six demonstration names are Alicia,
Jonathan, Stacy, Olivier, Marc and Nimesh; and the three model providers are named
neutrally. Editor and framework names on the technology routes are third party
marks used nominatively and are kept. Line lengths matter: headlines were chosen to
break at the same words at the same widths.

### What is measured and what is proposed

Everything above is either measured or reconstructed, and the builder should know
which. Measured: the colours, the easing set, the icons, the type, the spacing and
nearly all of the wording, across nineteen product routes at three widths. Inferred
or proposed, and therefore adjustable: the display type endpoints, the gutter steps,
the cursor badge path and timings, the bloom's secondary gradient offsets, the world
map landmass, the marquee speeds, the demonstration tab dwell time, and breakpoint
behaviour between the captured widths. Hover states on the marketing routes are
reconstructed from declared transitions, and the only observed hover results are on
the sign up and documentation routes. Everything behind sign in, the whole console,
is a reconstruction from what the public site promises, principally the pricing
matrix and the enterprise controls sentence: its requirements are sound because they
are what those promises cost to keep, and its screens are a proposal. The deliberate
divergences from the reference are the closing headline's colour, enumerated
transition properties, layer promotion only while animating, composed miniatures
instead of video, a trust route in this build instead of an external service, and a
status line that is live with an unknown state. Known limits of the capture method:
body copy was transcribed from screenshots where a node cap was reached, accelerated
content is known by appearance only, continuous motion is bounded rather than fixed
by nine scroll samples, and there was no authenticated capture.

## Constraints

- The realtime plane here is an admission and operation surface, not a document
  engine: it decides on every operation whether that operation is allowed.
- Signup is closed: no route creates an account.
- Money is integer minor units in `usd`, times are UTC, and an identifier handed
  to a client is opaque; a sequential one is a contract violation.
- The record of who did what is append only.
- Seeding is idempotent: restarting must not create a second seeded row.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written
  to `/app/USER_README.md`. Roomstack has seven seeded accounts and they all
  share one password; list every address and that password there.
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

## Definition of done

Roomstack is done when it is deployed and healthy, an administrator can approve
and execute the revocation of a directory sourced group through the console, and
every live room connection, session and credential belonging to that group ends
at once, while a requester can never approve their own request and a request can
never run against arguments or an impact larger than the ones approved.
