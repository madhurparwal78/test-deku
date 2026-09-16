# Junction

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, five haulage companies must be able to ask for the
same half hour at the Dallas crossdock at the same instant and find that exactly
as many of them are confirmed as there are dock doors free for that trailer
type, never one more and never two on one door, and a gate operator who holds a
lorry at the fence must be unable to release it except through an approval that
a site manager at that site, and never the person who asked, gives.

That sentence is the product. A confirmation the app shows to itself does not
count: a booking is confirmed only when it holds its door for its window against
every other writer, and a release is real only when the approval behind it was
decided by someone eligible at the moment they decided.

## Overview

Junction is an operating system for the logistics yard, where trailers are
parked, moved, loaded, sealed and released. Its Yard Control System, YCS,
observes, decides and proves: cameras supply positions, moves are assigned
without asking, and every decision is kept as evidence.

You are building three estates behind one brand: the public content site, the
operator console, organised site first, and the haulier portal where outside
companies book their own arrival slots. The console is an exception queue with
a map beside it.

The hard part is allocation under contention: doors, windows, spots and moves
are finite, and two writers arriving together must never both win. Junction is
not a marketplace and has no self-service checkout.

## User roles

Ten roles, each held through a grant scoped to an organisation, a site set or
one site.

| Role | Holds | Never |
|---|---|---|
| organisation administrator | every action in the organisation | identity media, break glass, audit export, unbounded footage |
| security administrator | watchlists, footage, cases, audit read | operational writes |
| network manager | reads across a site set, reports, exceptions | operational writes |
| site manager | every operational action at one site, approvals | any other site |
| dispatcher | moves, the map, exceptions, shifts, dock read | approving |
| gate operator | visits, holds, release requests | approving |
| dock operator | dock activity, seals, custody events | approving |
| spotter | their own assigned moves and issue reports | any other move |
| analyst | reports and exports | operational reads of identity or footage |
| content publisher | the content site and its page view log | customer records |

A role counts only in the scope of the resource it touches. Authorization is enforced **server-side on every
mutating endpoint**. Hiding a button in the UI is not authorization: a direct
API call from a gate operator session to any site manager-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving
the protected state unchanged.

Haulier and customer users sign in to the portal, a separate identity space.
Signup is closed.

## Core features

1. **Dock windows never oversell.** A door holds at most one confirmed
   appointment for any overlapping moment. Bookings for one window arriving
   together confirm as many as there are capable free doors, and every other
   one is refused with alternatives; a window that merely touches another's end
   is not an overlap.
2. **One open move per trailer, one claim per spot.** Two moves for one asset,
   or two moves into one free spot, arriving together leave exactly one; a
   cancelled or completed move frees its destination.
3. **A stale position cannot be moved.** A move for an asset not confirmed
   within the site's staleness threshold is refused and a confirmation task is
   raised instead.
4. **Placed is not verified.** A spotter's placement and an observation of the
   asset at its destination are separate states, and only the observation
   verifies.
5. **Release goes through approval.** A held visit is released only by an
   approval decided by an eligible site manager at that site; the requester
   never approves their own request, and eligibility is read when the decision
   is made.
6. **Grants are read on every request.** A revoked grant stops working on the
   same session at once.
7. **The portal reveals nothing about anyone else.** Another company's booking
   and a site the haulier is not authorised at answer exactly as something that
   does not exist; availability states only whether a window can be had.
8. **Federated reports suppress small aggregates.** A customer with fewer than
   five loads in a period sees suppression, not a number.
9. **Custody is evidence.** Custody events form a verifiable chain; a correction
   is a new event, and no connection can rewrite one.
10. **Messages carry no freight.** A booking confirmation is sent once per
    booking and names no load or customer; a visit link dies on cancellation.
11. **Time belongs to the site.** A shift crossing a daylight saving change
    lasts the time that really elapsed, not its wall clock gap.
12. **The public site.** A terms page in every footer, the product's own
    not-found page, a page view log a publisher reads, security headers on every
    response, and a contact form that refuses a bot.

## User flow

| Route | Purpose |
|---|---|
| `/`, the pillar, module, market and problem routes, `/resources`, `/yard-efficiency-calculator`, `/yard-security-grader`, `/contact`, `/terms`, `/privacy` | the public estate |
| `/console/login` | member sign in |
| `/console/s/{siteId}` | site home |
| `/console/s/{siteId}/map` | the live yard map |
| `/console/s/{siteId}/gate` | the lane board |
| `/console/s/{siteId}/appointments` | the door calendar |
| `/console/s/{siteId}/appointments/new` | booking, on its own route |
| `/console/s/{siteId}/dispatch` | the move board |
| `/console/s/{siteId}/workflows/{instanceId}` | one approval |
| `/console/s/{siteId}/exceptions` | the exception inbox |
| `/console/admin/members` | grants |
| `/carrier`, `/carrier/book`, `/carrier/visits/{visitId}` | the haulier portal |
| `/v/{token}` | a driver's single visit view |
| any unmatched path | the not-found page, answered not-found |

**Entry.** Every console and portal route needs a session; an unauthenticated
visit renders a sign in panel in place and never serves data.

**Journeys.**
1. `bookings@redline.example.com` opens `/carrier/book`, picks Dallas
   Crossdock, an inbound dry van and a date, sees only open windows, and books
   one; a toast confirms it.
2. `gate.dal@tidewater.example.com` opens the Dallas lane board and finds the
   held Oakridge lorry with its release request pending.
3. `manager.dal@tidewater.example.com` opens that approval and approves it; the
   visit reads admitted.
4. `dispatch.dal@tidewater.example.com` opens the map, sees stale trailers drawn
   faded with a dashed edge, and proposes a move.

**States.** Every surface has loading shaped like its content, empty with the
action that ends it, error with the request identifier, and stale, which dims
and disables writes.

## UI/UX notes

Industrial and engineered: a technical drawing of a yard, not decoration. The
spacious public estate alternates whole sections of near-white neutral,
near-black cool neutral and near-black neutral grounds, draws structure with
hairlines that fade at their ends, and spends one mid, vivid lime on emphasis
only: the primary action, the active item, a hover, a live dot. The lime is
never a section ground and never body text on a light ground. Panels are raised
deep neutral, secondary text is muted neutral and borders are faint hairlines; a
light, vivid red warns, an amber cautions and a muted green marks success.

Type is `Junction Grotesk` for sentences, set large and tight, from `82.4976px`
display down to a `16px` interface default, and `Junction Mono` for small upper
case labels at `14px` and `11px`, widely tracked; aligned figures use tabular
digits. Controls are slightly rounded, panels more. The public motion is eased:
headings arrive a character at a time through a band of lime, sections rise
once, and transitions share one small vocabulary of curves. The console is
designed dark, dense, built for scanning, with instant motion; its required light
theme follows the operating system until a member chooses. The public layout is
a floating top header pill; the console is a rail on the left.

Inputs take the lime rule on focus, labels sit above fields with errors beneath,
a toast confirms a completed write, overlays close on Escape and return focus,
and a destructive action asks first.

Every text pairing meets WCAG AA contrast, every surface has full keyboard
navigation with a visible focus ring, icon-only controls carry labels, touch
targets are generous, no state is signalled by colour or motion alone, and a
reduced motion preference turns every entrance into a short fade while keeping
hover and focus feedback. The
layout scales fluidly to a capped column, and each responsive breakpoint changes
structure, never size.

## Technical requirements

### The stack, and what is already running

Build Junction as a **single page application over a JSON API**. The server is
**Litestar** on Python 3.12. The browser half is **Vue 3** built with **Vite**:
the server returns one application shell for every console, portal and content
route, the browser renders the route, and every piece of data arrives from the
JSON API. One process serves the production build of the browser application,
the documents the server must answer itself (the not-found answer, the terms
page, the security headers), and the HTTP API on the same origin under the
`/api` prefix.

Three backing services are **already running** and reachable at their
environment variables. Do not download, install, compile or start a copy of any
of them.

| Service | Read from | What it is for |
|---|---|---|
| PostgreSQL | `DATABASE_URL` (the same value is also in `DB_URL`) | every durable row in this brief |
| Keycloak | `AUTH_URL` and `AUTH_ISSUER_URL`, which carry the same issuer, with `AUTH_CLIENT_ID` and `AUTH_CLIENT_SECRET` | the identity provider that holds member credentials, realm `junction` |
| Mailpit | `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS`, the last two empty because the server takes no authentication | real SMTP; every message Junction sends goes here |

`APP_PUBLIC_URL` and `APP_PUBLIC_PORT` are read from the environment and never
hardcoded. Use only the libraries named here plus their direct dependencies. Do
not introduce a second database, cache, queue, object store, identity provider
or mail vendor: the only backing services available in this environment are
PostgreSQL, Keycloak and Mailpit, and reaching for anything else is a contract
violation. Anything this brief calls a queue, an outbox, a cache, an event log,
a time series store, an object store, an analytical store or a search index is
a table in PostgreSQL, and anything it calls a camera, a site node, a vehicle
unit, a warehouse system, a transport system, a content back end or a model
service is represented by its records and its HTTP surface, not by a process
you start.

### Placeholder identity

The product this brief describes was measured from a real company. Every name
below replaces one, and the replacement is the name you use everywhere. The
reference marked each name with a placeholder token, such as BRAND for the
wordmark, OSNAME for the category and OSABBR for its short form, and no token
ever reaches a page.

| Stands for | Use |
|---|---|
| the product and company wordmark | `Junction`, eight characters |
| the operating company | `Junction Systems, Inc.` |
| the category the product coined | `Yard Control System`, short form `YCS`, carried with a trademark mark |
| the named yard management product | `ClearYard`, nine characters |
| the named structured workflow product | `Routines`, eight characters |
| the named gate throughput product | `Rapid Gate` |
| the public conversational agent | `Ada` |
| the design studio credited in the footer | `kinetika`, eight characters |
| the published sales line | `+1 (555) 010-4477` |
| the published support, press and vulnerability addresses | `support@junction.example.com`, `press@junction.example.com`, `security@junction.example.com` |
| the text family | `Junction Grotesk` |
| the monospace family | `Junction Mono` |
| the investor in the investor wall | `Northmoor` |
| the chief executive named in a press release | `Rowan Vasquez` |
| the customer wordmarks, in logo wall order | `Rydell`, `Handa`, `Tidewater`, `DSX`, `Northfield`, `Everwear`, `Cadence Cold`, `Praxis`, and in case studies `Vantage Retail` and `Meridian Foods` |

Every identifier derived from the original brand is scrubbed before it reaches a
class name, a module name, a custom event name or copy. The self-guided product
tour, the conversational widget vendor, the customer relationship vendor, the
analyst house, the perimeter security partner and the ten rival products have no
names in Junction: each is a configured destination or a stated source, never a
typed brand, and the analytics measurement identifier and the search console
verification token are injected from configuration and never committed.

### The three estates and the three applications

| Estate | Who reaches it | How it renders | Caching |
|---|---|---|---|
| content site | the anonymous public and search engines | the application shell, then the route, with each route's title, description and canonical address in the document | public, per route, invalidated on publish |
| operator console, under `/console` | members of a customer organisation | behind a member session, never indexed | never stored by a shared cache |
| haulier portal, under `/carrier` and `/api/portal` | haulier users, customer users, and drivers holding a visit link | behind a portal session or a visit link, never indexed | never stored by a shared cache |

The three are separate products that share three things only: the design tokens
of the front-end specification, the primitive component set, and the typed HTTP
contract. They do not share a router, a store, a session or a data access path,
and each can be released without the others. The console and the frontline
surfaces release continuously; the content site releases on publish.

### Identity, sessions and the two spaces

Six kinds of principal, and they never share an identity space.

| Principal | Authenticates by | Space |
|---|---|---|
| member | Keycloak, realm `junction`, through the app | organisation |
| haulier user | a local credential held by Junction | portal |
| customer user | a local credential held by Junction | portal |
| driver | nothing; a single visit link | none |
| machine credential | a client secret shown once and stored as a hash | organisation |
| workflow instance | an internal principal minted per instance | organisation |

**Members.** Member credentials live in Keycloak. The app never stores a member
password and never mints a Keycloak administrative token.
`POST /api/auth/login` takes `{"email", "password"}`, exchanges them with
Keycloak, and on success writes a **session row** of its own and returns
`{"access_token", "expires_at"}`, a bearer token that names that row. Every
console call presents it. A member session idles out after 60 minutes, expires
absolutely after 12 hours, and is revocable individually; a revoked session is
refused on its next call.

**Portal principals.** `POST /api/portal/auth/login` takes `{"email",
"password"}` for a haulier user or a customer user, checks a password hash
Junction holds, and returns `{"access_token", "expires_at",
"principal_kind"}` with `principal_kind` `haulier_user` or `customer_user`. A
portal session idles out after 30 minutes and expires absolutely after 8 hours.
A haulier user registers only by invitation from a haulier administrator or from
a member holding haulier management; self registration from a mail domain is not
offered, because a domain does not establish which haulier a person works for.

**The spaces never cross.** A member token presented to any `/api/portal/` route,
and a portal token presented to any other `/api/` route, is refused with `401`
and code `principal_kind_mismatch`. A principal in one space can never be granted
a role in the other, and the refusal is structural rather than a rule in a
handler. A person who is both a haulier user and a member holds two principals
and neither sees the other's context.

**What a session never carries.** Permissions are not carried in a token as a
claim the server trusts. The session names the principal; the grants are read
when the request is served. A token holding a role is a role that survives its
own revocation until the token expires, and that is exactly what must not happen.

**Federation and lifecycle, as capabilities.** An organisation may federate
through an assertion based protocol and a token based one. Assertions are
checked for signature, audience, recipient, replay window and bounded clock skew,
and the assertion identifier is kept so one assertion is never accepted twice.
Two signing certificates may be valid at once, and expiry raises a task at
ninety, thirty and seven days. Discovery is by mail domain, which an organisation
claims through a verification step. Just in time provisioning creates a member
on a first valid assertion where the organisation enables it, with roles from
group claims; a member is matched on the provider's immutable subject, never on
a mail address, because addresses are reassigned. An organisation may require
federation, after which local credentials stop working except for break glass
accounts, which carry a second factor and are recorded on every use. Group
claims are read on every sign in and directory derived grants are replaced, not
merged; a grant made in the console is marked as direct, survives a sign in and
still carries its expiry. A leaver is deprovisioned by directory removal or
push: sessions revoked within 30 seconds, derived and direct grants removed, open
approvals, owned watchlist entries and connectors reassigned, shifts closed. A
reconciliation compares the directory to the member table at least every 4 hours
so a leaver never waits for a sign in that will not come, a dormant member's
elevated grants are suspended, and an orphaned record goes to the owner's
manager. A member in two organisations holds two memberships and chooses at sign
in; a directory outage leaves existing sessions running to their absolute
lifetime; a group mapped to a deleted role makes no grant and is flagged.

**Local credentials** where there is no federation: a memory hard password hash
whose parameters are recorded per credential; a length minimum with no
composition rules, checked against a breached credential corpus, with no forced
rotation; a second factor required for any administrative or security role and
offered to everyone, hardware keys and time based codes, with recovery codes
issued once; a single use, short lived signed reset link that never says whether
an address is registered and revokes every session on success; progressive delay
rather than a hard lock, so nobody can lock a gate operator out; and sign in,
reset and invitation answering identically for known and unknown addresses.

**Sessions in detail.** A session travels in a signed, encrypted, secure,
host-only, same-site cookie that script cannot read, or as the bearer token the
login returns. Refresh tokens rotate and a reused refresh token invalidates the
whole family, revokes every session for that principal and raises a security
event. A session records the device, address range and assertion; a change of
address range beyond a threshold demands re-authentication for a sensitive
action. A second factor is presented again for a grant change, a watchlist
change, a break glass invocation, an identity media read, an export and a
credential rotation. Every session is visible to its member and revocable one by
one, a revocation takes effect everywhere within 30 seconds including the live
channel, and logout clears the session, revokes the refresh family and, where
configured, starts a federated single logout.

**Machine credentials** are created by a permitted member with a purpose, a
scope of operations and sites, an owner and a maximum age; the secret is shown
once and stored as a hash; rotation overlaps validity and reminds at seventy five
per cent of the maximum age; expiry stops the credential; revocation is effective
within 30 seconds; every use, creation, rotation and revocation is recorded with
the actor and reason; and a leak is handled by revoking, rotating, reviewing the
credential's whole recorded life and notifying the organisation's security
contacts. A site node holds a hardware backed, non-exportable credential rotated
automatically.

### One authorisation decision

Every check answers one question: may this **principal** perform this **action**
on this **resource**, in this **context**, where the context is the organisation,
the site, the module entitlement, the site's policy, the time, the shift, the
residency and whether the session is elevated. It is one decision reached from
one place, returning allow or deny, the rule that decided, and any obligations
the handler must meet: a redaction, a required reason, a required second
approver, a rate ceiling. The default is deny, an explicit deny beats every
allow, policy is versioned data that can be changed and reverted without a
release, a decision is reached within `5ms` at the ninety ninth percentile from a
warm local cache, and every decision records the policy version it used.

The same decision is enforced where the call is accepted, where the rows are
read, and at the point of execution for anything whose preconditions can change
between the call and the effect: a gate release, a move assignment, an approval
decision, a booking commit. A handler that forgets to filter must receive
nothing rather than everything, and the organisation and site in scope come from
the authenticated principal, never from a request parameter. Background jobs,
exports, report builders and cache warmers act under a scoped principal, never a
privileged one.

**The permission vocabulary.** An action not in this table does not exist.

| Resource | Actions |
|---|---|
| organisation | read, update, set-residency, set-retention, transfer, delete |
| site | read, create, update, deactivate, set-policy |
| site plan | read, propose, approve, publish |
| entitlement | read, request, grant |
| member | read, invite, update, deactivate, assign-role |
| role and grant | read, create, revoke, explain |
| asset | read, update, flag |
| position | read, correct |
| visit | read, hold, release, refuse, amend |
| capture | read, correct |
| identity capture | read-metadata, read-media |
| appointment | read, create, amend, cancel, approve, override-constraint |
| haulier | read, propose, verify, authorise, suspend |
| haulier user | read, invite, deactivate |
| move | read, create, assign, reassign, cancel, complete-manually |
| dock activity | read, record, skip-verification |
| seal | read, record, override |
| custody | read, generate-pack, share-federated |
| security event | read, acknowledge, dismiss, escalate |
| watchlist | read, propose, approve, override-match, remove |
| footage | read-bounded, read-unbounded, export |
| case | read, create, update, close |
| claim | read, create, update, resolve |
| workflow definition | read, propose, approve, publish, suspend |
| workflow instance | read, cancel, retry |
| approval | read, decide, delegate |
| exception | read, resolve, defer, reassign, escalate |
| report | read, create, schedule, export |
| connector | read, configure, test, enable, disable |
| webhook | read, create, rotate-secret, replay, disable |
| machine credential | read, create, rotate, revoke |
| audit | read, export |
| break glass | invoke, review |

`identity capture.read-media` is the most restricted action in the product: it is
in no composite role, is granted individually with an expiry, needs a second
factor and a reason on every use, and every use is recorded with that reason.
`custody.share-federated` is separate from `custody.read`, because sharing
evidence outside the tenant is a different power from reading it inside. No
action anywhere reads back a webhook secret, a machine credential secret or a
connector credential.

**Roles, grants and scope.** The nine roles of the user roles table ship, and an
organisation may define its own from this vocabulary through an approval. No
shipped role includes identity media read, unbounded footage, audit export or
break glass invocation; those four are granted one at a time, with an expiry and
a reason. A grant is a principal, a role, a scope of organisation, region, site
set, site, or a lane or dock within a site, a granter, a reason, an effective
start and an expiry. Scopes add up for allows and never for denies: a member who
is a site manager at one site and a gate operator at another holds each role only
in its own site, and every action is evaluated against the scope the resource is
in. The four base operational roles, dispatcher, gate operator, dock operator and
spotter, may be granted without an expiry; every other role requires one, and a
grant of an elevated role without an expiry is refused with `422` and code
`expiry_required`. The granter receives a renewal task at seventy five per cent
of a grant's life.

**Entitlement comes before permission.** A module an organisation has not bought
for a site is a different state from an action a member may not take. The
entitlement is evaluated first: a call into an unentitled module at a site is
refused with `403` and code `module_not_entitled`, and the console shows the
module's offer; a call a member's grants do not permit is refused with `403` and
code `forbidden`. A custom role naming an action its organisation is not entitled
to is definable and the action stays unreachable.

**Access requests and explainability.** A member may request a grant from the
surface that denied them, carrying the attempted action and a reason, routed as
an approval to that grant's approver set, which for an elevated grant is two
approvers. A denial always states what would let the member proceed. For any
principal, action and resource the console answers whether they may, which rule
decided, which grant supplied it, from which source, when it expires, and if not,
what would let them. The admin surface lists every role with its actions, every
member with each grant and its source, every grant expiring within thirty days,
every grant never exercised, and every action no member has ever used.

**Edge cases.** A grant expiring mid session denies the next request and names
the expired grant. An approver who lost the role before deciding cannot decide.
A workflow instance acting for a member acts as its own principal and records the
member as origin. A network report job reads exactly the site set the requesting
member holds, computed at generation. A policy rolled back mid flight lets
in-flight decisions finish on their own version. A site node credential trying a
member action is refused structurally.

### Sites, time and the site in scope

`site` is the join point of the model: nine of the fifteen operational tables
carry it, every grant is scoped by it, every entitlement is evaluated against it,
and every report aggregates from it. An organisation holds residency, retention
policy, an encryption key reference, a plan and its federation configuration; a
region optionally groups sites for regional roles; a site holds its time zone,
unit preference, operating hours, plan version, policy configuration and module
entitlements.

**The site in scope is a request, never an authorisation.** Every console call
names its site, and the server checks it against the member's grants on every
call. A site belonging to another organisation answers exactly as a site that
does not exist: `404` with code `not_found`.

**Time.** A site has a time zone and it is a property of the site, not of the
member. Every operational time renders in the site's zone with the zone
abbreviated beside it, and a member in another zone never sees their own. Every
write that takes a local wall clock time takes it as `YYYY-MM-DDTHH:MM` in the
site's own zone, and every response returns instants as ISO 8601 with the site's
offset at that instant, for example `2026-09-20T10:00:00-05:00`. A duration is
the time that really elapsed, including across a daylight saving change inside
it, renders as a duration such as `14h 20m`, and travels in responses as whole
seconds. Every instant is stored with its originating zone. Dwell, detention and
service level breaches are durations and are never shown as clock times.

### The console: shell, surfaces and honesty

The console is where a human resolves what the system could not decide by
itself. It is not a data entry surface: if an operator is typing something a
camera saw, the product has failed. It is an exception queue with a map beside
it.

| Region | Contents | Behaviour |
|---|---|---|
| rail, left | the mark, the surface entries, the member's avatar at the foot | fixed and narrow; expands with labels on hover or focus after a short intent delay |
| site bar, top | the site switcher, the live clock in the site's own zone, the exception count, search, notifications | fixed |
| work area | the surface | scrolls on its own; the shell never scrolls |
| inspector, right | the selected object | docks beside a wide work area, covers it below a laptop width |

The console never uses the content site's smoothed scroll, and its motion is
instant. It is designed on the brand's near-black cool neutral ground with deep
neutral panels and deep cool neutral hairlines; a required light theme swaps to
near-white neutral surfaces, is chosen per member, and until a member chooses
follows the operating system's preference, because gate control rooms run dark
and offices run light.

**The rail.** The four surfaces the product is sold on, in the yard's own order,
then the cross-cutting entries. A surface whose module is not entitled at the
site in scope renders the module's offer rather than disappearing.

| Rail entry | Surface | Module |
|---|---|---|
| Map | the live yard map | yard visibility |
| Gate | the lane board | gate management |
| Appointments | the door calendar | haulier appointments |
| Dispatch | the move board | dispatch and spotter orchestration |
| Dock | the dock board | load verification |
| Security | security events and watchlists | haulier risk assessment, or yard security |
| Workflows | definitions and instances | always present |
| Reports | analytics | always present |
| Admin | organisation, sites, members, roles, hauliers, integrations, tokens, audit, identity | permission gated, not module gated |

An unentitled module renders its own name, its solution paragraph, a still
illustration and two actions: request the module from the organisation's own
administrator, which opens an approval, and open the public module page. An
unpermitted surface is absent from the rail and its address renders the not
permitted document. Telling a member a feature exists that they may not use is
correct; telling a customer about a module they have not bought is a sale;
confusing the two leaks the permission model or wastes the sale.

**Organisation home.** A member with access to one site is sent to that site's
home by a client side replacement, so the back control never loops. A member with
more sees the network summary: every granted site with its live exception count,
gate queue depth, spot occupancy and service level state.

**Site home.** One screen with no scrolling at a laptop viewport, answering in
order: what is wrong now (open exceptions by severity and the three oldest),
what is arriving (the next two hours of appointments, the gate queue depth, any
held visit), what is moving (open moves by state, spotters on shift, the oldest
unassigned move), and how the day is going (check-ins completed, average gate
time, moves completed, average dwell). Every panel states its own data age.

**The site switcher** lists only sites the member holds a grant on, grouped by
region, filtered by name, code and city; switching keeps the current surface
where the target site has that module and falls back to its home where it does
not; unsaved work in the inspector prompts and names what would be lost; it
opens on a keyboard chord and commits on Enter; the last site is remembered per
member per device. On a switch every cached value scoped to the previous site is
dropped before the new surface renders, because another site's row appearing for
one frame is a cross-tenant disclosure.

**Freshness.** The console is live and honest about when it is not.

| State | Presentation |
|---|---|
| live | data under ten seconds old, no indicator |
| lagging | ten to thirty seconds, the age beside the panel heading |
| stale | over thirty seconds; the panel dims, the age shows in the caution colour, and every control that writes is disabled |
| disconnected | a persistent bar states the live channel is down, the age keeps counting, and every write control is disabled with the reason |
| reconnecting | the bar states the attempt; on reconnection the surface reconciles the affected records rather than reloading |
| read-only | the member has read grants only; write controls are absent, not disabled |

A stale console never accepts a write: assigning a move from a thirty second old
picture sends a spotter to a place the trailer has already left.

**Keyboard and command.** The console works entirely from the keyboard, because
it is used in gloves in control rooms. A command chord opens a surface to go to a
site or surface, find an asset by identifier or plate, start a workflow or open
an exception; a digit selects a rail surface; a search chord focuses the current
surface's search; escape closes the inspector, then the command surface, then
clears a selection; an accept chord accepts the focused queue item; a defer chord
defers it and opens the reason. Every destructive or state changing chord asks
for a confirmation that names the object and the action. Every chord has a
pointer equivalent and never collides with an assistive technology's own chords,
and a keyboard help surface lists them.

### The live yard map

The product's central object: a drawn plan of the site with every asset where it
is and what state it is in.

**Rendering.** The map draws the yard's own geometry: fence line, gates, lanes,
spot rows, dock face and buildings, in a local plane anchored to the site's
origin and rotation so it is oriented to the yard rather than to north, in metres
internally and the site's own unit preference on screen. It holds sixty frames a
second while panning with two thousand assets; the static plan, the assets and
the interaction are separate layers and the asset layer redraws only on a change
or a pan; hit testing uses a spatial index; labels draw above a zoom threshold,
decluttered so none overlap, and the selected object's label always draws; zoom
is continuous from the whole site to one spot. Above two thousand assets the
assets cluster by spot row and expand on zoom.

**The site plan is data**, authored in the admin surface, versioned, never an
image, and editing it is an approval workflow with two approvers, because a moved
spot polygon moves where the system believes trailers are.

| Object | Fields |
|---|---|
| site | origin, rotation, bounds, time zone, unit preference |
| zone | a named polygon: a spot block, a staging area, a fuel point, a maintenance bay, a restricted area |
| spot | identifier, polygon, row, ordinal, type, permitted asset types, out of service flag |
| dock door | identifier, polygon, door number, permitted asset types, equipment, out of service flag |
| gate | identifier, polygon, direction, lanes |
| lane | identifier, polygon, gate, direction, kiosk, cameras |
| path | a centreline with a direction and a travel cost, used by assignment |
| camera | identifier, position, bearing, field of view, coverage polygon |

A spot identifier is unique within a site and is the label operators say over a
radio; it is a string such as `A-03`, never a number.

**Asset presentation.** An asset is an oriented rectangle at its true footprint,
filled by state and outlined by condition: empty and available in the raised
deep neutral; loaded and ready in the lime; loaded and not ready in the caution
amber; in a move in the mid vivid blue with its path drawn; held or refused in
the mid vivid red; dwelling past its threshold with a hatch over its fill; a
last known position faded with a dashed outline; selected with a brighter blue
outline at double weight. The last known state is required and is the one most
builds omit: a trailer not confirmed within the site's staleness threshold looks
different from one that was.

**Interaction.** Hovering an asset shows its identifier, type, state, spot, dwell
and last confirmation; clicking selects it and opens the inspector; a double click
zooms to it; dragging it onto a spot **proposes a move** and never writes a
position; dragging the canvas pans; wheel or pinch zooms about the pointer; a box
selects many for a bulk proposal; a context menu proposes a move, holds, releases,
opens history or reports a problem; arrows pan, plus and minus zoom, Tab walks
assets in spot order and Enter selects.

**The inspector** shows identity, state, position with confidence and age, dwell
against its threshold, the appointment and haulier, the load and seal state, the
open moves, the last ten events and the custody chain link. Every field states its
provenance: observed by a named camera at a time with a confidence, reported by a
named integration, or entered by a named member. A field without provenance does
not render.

**The inventory** is the same data as a table of identifier, type, haulier, state,
spot, dwell, last confirmed, appointment and load state, filterable and sortable on
every column and exportable. The table and the map share one selection and one
filter, and a filter dims excluded assets on the map instead of removing them.

**Reconciliation is continuous.** An observation of an asset on a spot the system
believed empty updates the position, and if the system believed another asset was
there both are flagged and an exception raised. An asset unseen past the staleness
threshold becomes last known and joins the stale list. An unknown asset raises a
discovery exception with the observation. An asset unseen for a full sweep raises a
disappearance exception. A manual count produces a per-asset difference report
with each asset's observation history. Two contradicting observations always raise
an exception carrying both; the system never quietly picks a winner.

**Map states.** No plan yet shows the plan editor's entry point with a message. A
plan with no known assets draws every spot empty and says no observations have
arrived. A down position feed draws every asset as last known, shows the
disconnected bar and disables proposals. An asset outside the site bounds draws at
the boundary with a marker and raises an exception. Two assets on one spot both
draw, offset, with a conflict marker. Below a tablet width the map becomes a list
of spots grouped by row.

**Positions over HTTP.** `POST /api/sites/{site_id}/positions` records an
observation of an asset on a spot from a permitted member, at the instant it is
received, and updates the asset's position. A dispatcher, a site manager or an organisation
administrator is permitted to record a position and to create an asset at the site. An asset's reading carries
`staleness` of `fresh` or `stale` against the site's threshold, computed when it
is read. Seeded positions were observed long ago and read as stale.

### The gate and the visit

The gate's promise: cameras capture identity, lane cards refill without a person,
one board carries every inbound and outbound movement, plates, identity documents
and container numbers are read in seconds, drivers check themselves in through a
simple flow, and gate processing is up to eighty five per cent faster with
seventy five per cent fewer errors.

**The visit** is one vehicle's arrival, time inside and departure, and its state
lives in its own field with a history, never derived from other rows and never in
a single mutable blob.

| State | Entered when | Left when |
|---|---|---|
| `approaching` | a vehicle is observed in an approach lane | captures are complete or it leaves |
| `identifying` | captures are complete and matching runs | a match resolves or fails |
| `matched` | bound to an appointment, or an unbooked arrival is permitted | instructions are issued |
| `held` | a check failed and a person must decide | released or refused |
| `refused` | a refusal is decided | the vehicle is observed leaving |
| `admitted` | instructions issued and the barrier released | the asset is observed on a spot or at a door |
| `on site` | inside | an exit begins |
| `exiting` | outbound checks run | the exit observation |
| `closed` | the exit observation | final |
| `abandoned` | no observation for the abandon threshold in a non-final state | final, raising an exception |

A transition the machine does not allow is refused with `409` and code
`illegal_transition`, and the state is unchanged.

**Capture.** Each lane's cameras produce observations with a confidence: the plate
and the trailer or container number always, the tractor unit number optionally,
the seal presence and number on an outbound loaded visit, the driver identity
document per site policy, the visual condition always, and the axle and dimension
class optionally. No capture is a decision. A capture below the site's confidence
threshold does not fail the visit: it goes to the lane operator with the image and
ranked candidate readings, the operator confirms or corrects in one action, and
the correction is kept as a labelled example.

**The decision.** `POST /api/sites/{site_id}/visits` records an arrival at a lane
from a gate operator or site manager and runs the ordered checks, recording every
result:

| Check | Passes when | On failure |
|---|---|---|
| appointment | a booking exists for this haulier or asset within the arrival window and its grace | the site's unbooked arrival policy: permit, permit with an exception, or hold |
| haulier authorisation | the haulier is authorised for this site and direction and not suspended | hold |
| driver identity | the identity matches the booking's driver within tolerance | hold |
| watchlist | no active entry matches the plate, driver, haulier or asset in the site's or organisation's lists | refuse, and raise a security event |
| asset expectation | the asset matches the booking, or policy permits it | hold |
| document | required documents are present and readable | hold |
| capacity | a spot or door is free for this asset type | queue, with a stated wait |
| dimension or hazard | the vehicle class is permitted at this site and door | refuse or reroute |

A hold opens an exception with the failing check, the captures and the actions
available. A refusal needs a reason from a controlled list and a member, and it is
never automatic except on an active watchlist match, which is itself reviewable.
An active watchlist match leaves the visit `refused` whatever else would hold it; otherwise any
failed check that holds leaves it `held`, and a visit nothing holds or refuses is `admitted`.
An entry past its expiry matches nothing, from the instant it expires. The whole
path from final capture to decision completes within `4s` at the ninety fifth
percentile.

**Release.** A held visit is released only through an approval. A gate operator or
site manager asks with `POST /api/visits/{visit_id}/release-requests`; the request
enters `pending`, every eligible approver except the requester is told, and when an
eligible site manager at that site approves, the visit becomes `admitted`. A request
against a visit that is not held is refused with `409` and code
`illegal_transition`.

**Driver identity** is the most sensitive processing in the product. A document
image, and where policy and jurisdiction allow a live face image compared one to
one against that document and never against a database of faces, is captured only
for admission to a private site, with the purpose stated to the driver in their
own language. Both images are kept for the site's configured period, `30` days by
default, then deleted on schedule; a non-reversible token per organisation is kept
beyond that for repeat recognition, so one driver at two customers is two tokens.
They are encrypted with a per-organisation key, readable only under a distinct
permission granted to few with a reason recorded on every read, and a driver may
refuse, in which case the site's policy applies and a manual identity path exists.
A site in a jurisdiction requiring consent for biometric processing never enables
the face comparison. No face image, document image or token ever appears in a
webhook, export, log line, analytics event or report.

**The lane board** has one column per lane and one card per visit by arrival: plate
and asset number with a confidence marker where low, haulier and appointment with
lateness, state in its colour, a live dwell in state, a row of check results with
failing ones in red and a word beside each, and the one action the state permits. A
held visit rises to the top of its lane and is announced. The board updates live
and degrades like every console surface: a gate operator on a stale board cannot
release a barrier.

**The visit detail** is the evidence pack for one visit: every capture with its image
and confidence, every check with the rule version that produced it, every
transition with its actor and time, the instructions issued and the custody link,
exportable as one signed document.

**Instructions to the driver** on admission: the assigned spot or door, the route,
the site rules and the exit procedure, by message to the booking's number, then a
printed slip, then a lane display; in the driver's own language from a fixed
translated set, never machine translated at issue time; with a short link to the
driver's visit view.

**Exit** runs the same path with outbound checks: the asset leaving is the one
expected, the seal is present and matches, load verification is complete where
required, and no hold is open. A failed outbound check holds the vehicle at the
exit lane.

**Gate edge cases.** An unbooked arrival where a booking is required follows policy,
and a hold names the reason and invites the haulier to book retrospectively. An
early driver gets the window's grace, then queues with a stated wait rather than a
refusal. A right plate with the wrong trailer fails asset expectation and a
permitted member can amend the booking in place. Two vehicles in one lane together
are never composed into one visit; an exception carries the frames. A vehicle
reversing out abandons after the threshold. A barrier that fails to open after a
release records the release, raises an equipment exception, and leaves the visit
`matched` rather than `admitted`, because the state describes the world, not the
intent. A site whose network is down runs the lane in degraded mode and reconciles
later. A refused driver returning within the hour has the refusal shown before any
decision. A booking cancelled while the lorry is in the lane keeps its binding and
raises an exception.

### Haulier appointments

Hauliers book their own slots so they stop arriving whenever, bookings stop
bunching, doors stop sitting empty before four lorries arrive at once, and no-shows
stop wrecking the plan; real time appointment changes let doors and labour be
reallocated.

**The calendar** is a resource calendar of dock doors grouped by dock and gate
capacity, with time running across, at the site's slot length, `30` minutes by
default: a day by default, a week for planning, an hour view for the shift. It has
an unassigned band for bookings without a door, the gate queue depth as a band
above it so collisions are visible before they happen, a live now marker in the
site's zone, and drag between doors and times subject to the constraints below.
Closed periods render as unavailable, not empty, because an empty Sunday and a
closed Sunday mean opposite things.

**An appointment** holds its haulier, a direction of `inbound`, `outbound` or
`live_load`, a window in the site's zone with grace either side, a door that may be
assigned later, the asset type and an asset number that may be unknown, the load
with its reference and the customer of the tenant it belongs to, the driver's name,
telephone, language and credential reference, equipment needs such as a tail lift,
reefer power or hazardous handling, its state, its source of `portal`, `console`,
`integration` or `gate`, and the constraint evaluation made when it was booked.

**A booking is accepted only if every constraint holds, evaluated on the server when
it is written, regardless of what the booking surface showed:**

| Constraint | Rule | Refusal code |
|---|---|---|
| door capability | the door permits the asset type and has the equipment | `door_incapable` |
| door availability | the door is in service and holds no confirmed booking overlapping any moment of the window | `door_unavailable`, or `door_out_of_service` |
| site capacity | concurrent visits in the window stay under the site's ceiling | `no_capacity` |
| gate capacity | arrivals in the window stay under the gate's throughput ceiling | `no_capacity` |
| labour | the shift pattern staffs the window for the load type | `no_capacity` |
| haulier authorisation | the haulier is authorised for the site and direction and stays so through the window | `haulier_not_authorised` |
| lead time | the window starts at least the site's minimum lead time from now, unless the booker may override | `inside_lead_time` |
| horizon | the window starts within the site's booking horizon | `beyond_horizon` |
| operating hours and curfew | the window sits inside operating hours and outside any restricted period for the asset class | `outside_operating_hours` |

Windows are half open: a window ending at `09:30` and a window starting at `09:30`
on one door do not overlap, and both are confirmed. A booking that fails a door
availability or capacity constraint is refused with `409` and offered alternatives:
`{"code", "message", "request_id", "alternatives": [{"starts_at", "ends_at"}]}`,
listing nearby windows that would be accepted for the same request. The booking
surface renders a refusal as an alternative offer, not a failure. **A booking is a
reservation against a finite resource: bookings for the same resource arriving at
the same moment never confirm more than the resource can hold.**

**The appointment machine.**

| State | Meaning |
|---|---|
| `requested` | submitted by a haulier at a site requiring approval |
| `confirmed` | holds its slot |
| `amended` | changed after confirmation, the prior version kept |
| `arrived` | bound to a visit at the gate |
| `in_progress` | the asset is at the door |
| `completed` | work finished and the asset released |
| `departed` | the visit closed |
| `no_show` | the window and grace passed with no arrival |
| `cancelled` | withdrawn by the haulier or the site, with a reason |
| `expired` | never confirmed within the approval window |

An appointment whose window and grace have passed with no arrival reads `no_show`
from that moment, releases its slot, notifies the haulier and counts against the
haulier's reliability, without a person noticing it. Every amendment is an entry
with actor, reason and the constraint evaluation, never an overwrite, and an update
names the version it was based on: an update based on an older version is refused
with `409`, code `version_conflict` and `{"current_version"}`, and a surface offers
to reload that one appointment, never the calendar.

**Messages** are scheduled per appointment and kind, each sent once for its
triggering transition however often that transition is retried: a confirmation on
confirm by mail to the haulier and message to the driver where a number exists; a
change on amendment naming what changed; a reminder at the site's lead, `24h` and
again `2h` by default; arrival instructions on the `2h` reminder carrying the visit
link; a no-show mail; a cancellation to both; and a delay message when the gate
queue passes a threshold inside the window. A message never carries load detail, a
customer name or identity data, because a telephone is not a confidential channel.

**Haulier reliability** per haulier per site: on-time arrivals, late arrivals by
band, no-shows, cancellations inside the lead time and average time on site,
visible to the site and to the haulier. It never changes a booking decision by
itself; it informs the human authorisation review, which can show its reasoning and
be overridden.

**Appointment edge cases.** An empty view renders its resources and hours with a
message. A door taken out of service flags every affected booking, proposes a
reallocation and silently moves none. An authorisation lapsing between booking and
arrival flags the booking, notifies the haulier and holds the visit at the gate. An
integration proposing a booking that breaks a constraint is refused with the
constraint named and told so. A changed slot length leaves existing windows alone. A
window containing a daylight saving change has the duration its instants give it.
Two planners dragging one booking at once: the second meets the version conflict.

### Dispatch and moves

Dispatch replaces radio chatter with a digital command centre and a browser
application for the driver: the dispatcher manages assets visually, assigns work
digitally and measures what happened, so spotters stop driving empty to the wrong
end of the lot and the urgent move stops waiting behind three routine ones.

**A move** is one asset from one location to another by one spotter at a priority:
the asset; a from and a to that may be a spot, a door, a gate lane, a staging area,
or `unspecified` until execution; a reason of `inbound_placement`,
`outbound_staging`, `door_feed`, `door_clear`, `repositioning`, `maintenance`,
`fuel`, `inspection` or `customer_request`; a computed priority with a manual
override; a due time from the driving appointment or service level; an assignee; a
state; an origin naming the workflow, integration, member or agent that created it;
and constraints of equipment, hazard class, licence class and door access. Free text
is only ever an additional note.

**Creating a move.** Four origins converge on one validation path: automatic when a
workflow fires, proposed when a dispatcher drags on the map, requested by a dock or
gate operator, and from an integration. Every creation checks that the asset exists
and its position is not stale, that the destination is compatible with the asset
type, that the destination is free or reserved for this move, that no other open
move holds this asset, and that the requester may. Each failure names its own
constraint:

| Failure | Refusal |
|---|---|
| the asset already has an open move | `409`, code `asset_has_open_move`, with `{"move_id"}` naming the open move |
| the destination is reserved by another open move | `409`, code `destination_reserved` |
| the asset's position is stale | `409`, code `position_stale`, and a position confirmation task is raised for that asset |
| the destination does not accept this asset type | `422`, code `destination_incompatible` |

A destination is **reserved** from the moment a move targeting it is created until
that move completes, is cancelled or expires. At creation a destination is free when no
open move holds it; an asset already standing on it is discovered when the move executes,
where the move fails with that reason, and does not refuse the creation. **Two moves arriving together for one
asset leave exactly one open move, and two moves arriving together for one free
destination leave exactly one holding it.**

**Assignment** is automatic by default and manual by exception: automatic assignment is a site
setting, on for a new site, and while it is off a created move stays `open` until a transition
assigns it. The cost of a
candidate spotter for a move is the travel time from the spotter to the origin plus
the travel time from origin to destination, both over the site's path graph rather
than a straight line, plus a queue penalty for the spotter's existing work, plus a
skill penalty for licence class, hazard endorsement, door access and instruction
language, minus an urgency credit that rises as the due time nears and is unbounded
once it passes, capped per cycle so one impossible move cannot starve the shift.
Assignment reruns on every relevant event and is idempotent: unchanged state gives
the same assignment. An accepted move is never reassigned automatically. A
dispatcher may override any assignment, recording the actor and, where the site
requires, a reason; the pattern of overrides is how the cost model is found wrong.
Empty travel is reported per shift and per spotter: travel with an asset, without,
and the ratio.

**The move machine.**

| State | Entered when |
|---|---|
| `open` | created and validated |
| `assigned` | a spotter is chosen |
| `accepted` | the spotter accepts |
| `travelling` | the spotter heads to the origin |
| `hooked` | the asset is coupled |
| `moving` | in transit |
| `placed` | the spotter confirms the asset is at the destination |
| `verified` | an observation shows the asset at the destination |
| `completed` | verified, or completed manually with a reason where no observation is possible |
| `rejected` | the spotter cannot do it, with a controlled reason |
| `cancelled` | withdrawn, with a reason |
| `failed` | blocked at execution: not there, spot occupied, would not couple |

`placed` and `verified` are distinct states. A person saying they put it there and a
camera seeing it there are different facts. **A move becomes `verified` only when an
observation places its asset at its destination while it is `placed`; no request
moves it to `verified` directly.** A move `placed` and not verified within the
site's verification window raises an exception carrying the spotter's claim and the
last observation. `POST /api/moves/{move_id}/transitions` takes `{"to", "version"}`
and moves the machine one legal step; an illegal step is refused with `409`, code
`illegal_transition`, and a stale version with `409`, code `version_conflict`.
`POST /api/moves/{move_id}/cancel` cancels with a reason and frees the destination.

**The dispatch board** has three columns and a map in one screen: unassigned moves
by priority with asset, route, due time and the computed best spotter with its cost;
in flight moves grouped by spotter with elapsed time against estimate; and attention,
holding rejected, failed, overdue and unverified moves, which is the dispatcher's
real job and reads first below a laptop width. The map shows every spotter's live
position and every in-flight route, and selection is shared both ways.

**The move detail** shows the fields, the full state history with actor, time and
position, the assignment decision with every candidate's cost by term, acceptance or
rejection, the verifying observations and the creating workflow instance.

**Spotters and shifts.** A spotter is a member with a frontline role, a shift, a
vehicle and endorsements. A shift has a start, an end, breaks and a site. No move is
assigned outside a shift, inside a break, or in the wind-down before a shift ends
when the estimate exceeds the time left. Handover is explicit: each open move is
carried to the next shift or returned to unassigned, and the handover is recorded.
`POST /api/sites/{site_id}/shifts` records a shift from the site's local wall clock
start and end and returns its instants and its `duration_seconds`. Shifts of one member may
overlap, because cover and handover overlap on the floor; each is recorded.

**Dispatch edge cases.** A spotter offline mid-move leaves the move in its state,
queues actions on the handheld and marks the spotter unreachable with the age of last
contact. An asset missing at the origin fails the move with that reason and raises a
discovery exception, never starting a search silently. An occupied destination fails
the move, releases the reservation and reruns assignment. A move against a stale
position is refused and a confirmation task created. Three rejections in a shift
trigger nothing automatic and surface in the assignment quality report. A site that
loses connectivity keeps handhelds on their last assignment set, marks the board
degraded and disables new assignment.

### The dock, load verification and the custody chain

This module is an evidence feature, not an efficiency feature. Its promise: capture
dock door data and verify seals at the point of action, defend against chargebacks
and damage claims, and give a third party logistics operator's own customers
federated reporting on their own freight. When a customer files a chargeback or a
shortage claim the burden of proof is on the yard, and Junction must meet it.

**The custody chain** is an ordered sequence of custody events for one asset, and it
only ever grows.

| Event | Records |
|---|---|
| `arrived` | the gate observation, plate, asset number, seal state, condition images |
| `admitted` | the decision, the actor or rule, the assigned destination |
| `moved` | each move's origin, destination, spotter and verifying observation |
| `docked` | the door, the time, the observation |
| `opened` | the seal broken, by whom, witnessed by which camera |
| `loaded` or `unloaded` | the manifest reference, the count where counted, the operator |
| `sealed` | the new seal number, its image, the operator |
| `released` | the release decision and its actor |
| `departed` | the exit observation, the seal state, the condition images |
| `corrected` | a correction to an earlier event, naming it, with a reason and an actor |

Every event carries its identifier, its `sequence` within the asset's chain starting
at `1`, the previous event's hash as `prior_hash` (sixty four zeros for the first),
its own `hash` over its content and that previous hash, the actor, the source as an
observation, an integration or a member, and the instant. Recomputing the hashes in
order reproduces the head; a changed event breaks every hash after it.

**A chain is never edited.** A correction is a new event of kind `corrected` that names
the event it corrects in `corrects`, with a reason and an actor; the original stays
exactly as it was, and both appear everywhere the chain appears. There is no request
that changes or removes a custody event, and no connection the application holds,
including one made with its own database credentials, can change or remove a row of
the `custody_event` table or the `audit_event` table.

- `POST /api/sites/{site_id}/custody-events` records an event from a dock operator or
  site manager, next in sequence in the order it is received; a late camera or integration report
  means kinds are not refused for arriving out of their usual lifecycle order.
- `POST /api/custody-events/{event_id}/corrections` records a correction.
- `GET /api/sites/{site_id}/assets/{asset_number}/custody` returns the chain in order
  with its head hash.
- `POST /api/sites/{site_id}/assets/{asset_number}/custody/verify` recomputes the chain
  from the stored events and answers `{"valid": true, "broken_at": null}`, or
  `{"valid": false, "broken_at": <sequence>}` naming the first event whose stored hash
  no longer matches.

**The dock board** has one column per door and one card per activity: the door's
number, equipment and state; the asset, haulier and load reference; the activity of
loading, unloading, live load, idle or blocked; elapsed time against the expected
duration for the load type; the seal as present, broken or resealed with its number;
verification steps done of those required; and blockers of missing labour, equipment,
paperwork or an open exception. A door with no activity renders as idle with the time
since it was last used, because idle door time is what the module exists to reduce.

**Verification happens at the point of action.** Before opening, the seal number is
captured and compared to the record, and a mismatch stops work and raises an exception
before the doors open. On opening, a dock camera records it as a custody event. During
work, counts and damage are recorded. On completion, the load is compared to the
manifest and a discrepancy is recorded, not resolved. On sealing, the new seal is
captured and read, with manual entry only where the read fails and marked as manual.
After sealing, nothing more is recorded against that visit at that door except a
correction. A step may be skipped only with a controlled reason and a permitted
member, and the skip is carried on the evidence pack as a stated gap.

**Media retention.** Gate condition images, seal images and dock opening and sealing
frames `180` days; continuous dock footage `7` days, rolling; media referenced by an
open claim indefinitely under a legal hold; identity media `30` days and never under a
claim hold. A legal hold is itself recorded with an owner and a review date, because a
hold nobody reviews becomes a retention policy by accident.

**The asset history** is every chain across every visit, filterable by visit, date and
event kind, with media inline and every actor named, so an operations manager can
answer a call about a load from three weeks ago without an export.

**The evidence pack** is one generated document for a visit or a load: the chain in
order, every image with capture time and camera, the seal record, the manifest
comparison, every discrepancy, every skipped step with its reason, the actors, and a
verification statement carrying the chain head hash. It is generated in the
background with the requester told when it is ready; generating one is a permission
and is recorded with a reason; identity data is never included and a driver is named
only as the name on the booking; it is shared with a customer of the tenant only
through the federated view; and packs are retained and recorded like any object.

**Federated customer reporting.** A third party logistics operator shows its own
customer the evidence for that customer's own freight and nothing else. The view is
scoped to the load's customer of the tenant, the customer's users are portal
principals, and the surface is read only: their loads, each load's custody chain, the
evidence packs, and service level performance on their own freight. It never shows
another customer's asset or volume or any site-wide figure that could be differenced
to reveal one, and **every aggregate over fewer than five loads is suppressed**:
`GET /api/portal/customer/report` with query `site_id` and `period` (`YYYY-MM`)
answers `{"period", "loads", "median_dwell_seconds", "suppressed"}`, where a customer
with fewer than five loads in the period receives `loads` and `median_dwell_seconds`
as `null` and `suppressed` as `true`. `GET /api/portal/customer/loads` with the same
query lists only the caller's own loads. Every access is recorded and visible to the
tenant.

**Discrepancies and claims.** A discrepancy is its own record of what was expected,
what was found, the evidence and the raiser, moving through `raised`,
`investigating`, `resolved` and `disputed`. A claim references discrepancies and
evidence packs, carries a counterparty, a value and a deadline, drives a legal hold,
and is handled as an approval workflow.

**Dock edge cases.** An unreadable seal is entered manually, marked so, with the image
kept, and the pack names the weakness. A trailer with no seal where one was expected is
held at the gate before it enters, with condition images captured anyway. A door camera
failing mid-load records an observation gap with its duration and the pack states it.
A manifest arriving after completion is compared then, and any discrepancy is a new
event on the closed chain. A load for two customers of the tenant carries both
references and each customer sees only their own lines. A claim raised after the
retention period gets a pack from the retained chain that states which media expired
and when. When media storage is exhausted, custody events keep recording and media
capture drops to key frames with an alarm; custody is never lost for want of a picture.

### Security, fraud and the break glass path

Yard security, cargo fraud prevention and chain of custody become native to the
platform, and this is where the five layers the public grader scores are operated.

**A security event** is an observation or rule result that warrants a human look, a
separate record from an operational exception with its own handling, retention,
permissions and escalation: a watchlist match, an identity mismatch, an unauthorised
haulier, tailgating of two vehicles on one release, a perimeter breach outside a gate,
after hours movement, an unexpected departure with no release, a seal number changed
with no sealing event, a dwell anomaly in a restricted zone, repeated refusal of one
driver or haulier in a window, and a camera tamper. Each carries the observation, the
media, the rule version, a severity and a confidence; one with no retrievable media is
still an event and states the gap.

**Watchlists** are controlled lists of drivers, hauliers, plates or asset numbers with
a reason, an owner, a scope of a site or the organisation, never shared across
organisations in any direction under any configuration, and an expiry within the
organisation's maximum. Adding an entry is an approval needing two approvers, so no
one person can bar a haulier alone, and an integration can never propose one. An
entry approaching expiry raises a task to its owner, and **an expired entry stops
matching the instant it expires**. A match refuses admission and raises a security
event and never notifies a third party by itself; a permitted member may override a
match at the lane with a reason, and the override is itself a security event; the
driver is told they are refused and given a contact route but not told why at the
fence. Every add, amendment, match, override and removal is recorded with actor and
reason. A watchlist is the single most abusable feature in the product, and a free
text table with a delete button is a liability.

**Haulier risk** per haulier per site is a band with its reasons, never a bare score,
computed from authorisation state, credential expiry, reliability, security event
history, identity mismatch history and insurance and certification currency where
required. It advises the human decision and the unbooked arrival policy and never
refuses a visit by itself.

**The security surface** is an event queue ordered by severity then age, filterable by
kind, severity, state, camera, gate and time; a map overlay of event locations; a media
viewer showing the event and a configurable window either side; actions to
acknowledge, escalate, dismiss with a reason, attach to a case or raise a claim; cases
grouping events with a narrative, an owner and a state; and an incident pack built like
the evidence pack. Dismissing needs a reason and is recorded, because a one click
dismiss is a dismiss without reading.

**Footage.** No member browses continuous footage by default: it is reached only
through an event, visit, move or custody chain and bounded to that record's window.
Unbounded access is a distinct permission granted rarely, needing a reason every
session, time boxed and self-expiring. Every footage access records actor, reason,
camera, time range and the record it came through. Where a jurisdiction or agreement
requires, footage of a named individual needs a second approver. Exporting footage is a
separate permission from viewing it.

**Break glass** grants a time boxed elevation to a defined emergency role, never to
unrestricted access; only a small named set of principals may invoke it; it needs a
reason, a controlled category and an acknowledgement that the session is recorded; it
lasts at most `60` minutes and cannot be extended, a second invocation being a second
record; it notifies the organisation's security contacts and the tenant's audit stream
at invocation, not at the end; it never crosses an organisation; every action under it
carries the elevation identifier; it raises a mandatory review with a deadline that
escalates when missed; and it can never read identity media.

**Detection quality.** Every detection rule has a version, a confidence threshold and a
measured false positive rate on the site's own history; a rule whose rate passes its
ceiling is demoted from refusing to raising and its owner is told.

**Security edge cases.** A watchlist entry whose owner leaves is reassigned by the
lifecycle process, and one with no owner stops matching at its next review. An event
whose media has expired states the gap and names the retention policy. An offline
camera states its own outage. A lane override later found wrong is reviewable and
cannot be deleted. A disputed refusal creates a case with the driver's account and
requires the entry's owner to review. Two events of one incident are grouped, and
neither is deleted.

### The workflow engine, autonomy and approvals

Everything the product does by itself exists as a workflow definition with a
confidence threshold, an approval path and a record; a public claim about autonomous
action with no definition behind it is a defect. This is the named product
`Routines`, and it is a first class subsystem.

**A definition** is versioned data authored in the console and published through
approval: a trigger (an event kind with a predicate over its payload, a schedule or a
threshold crossing), guards re-evaluated at execution, steps as an ordered graph with
parallel and conditional branches, actions from the closed catalogue, autonomy per step
of `automatic`, `automatic_above_confidence`, `propose_only` or `human_only`, approvals
per step of none, one approver, a chain or a quorum of `n` of `m`, per-step timeouts
with an escalation target, per-step compensation that undoes it if a later step fails,
a scope of organisation, site set or site, and a rate ceiling on instances per period.
A published definition is immutable: an edit is a new version, and a running instance
finishes on the version it started with, recorded on it.

**An instance** is a durable record with its identifier, definition version, trigger
event, actor chain and step history, stored as one row per step transition rather than a
document rewritten in place, and every action it takes names the instance as its origin.

**The action catalogue** is closed: `createMove`, `cancelMove`, `assignDoor`,
`amendAppointment`, `holdVisit`, `releaseVisit` (always with an approval step),
`raiseException`, `raiseSecurityEvent`, `notify`, `emitWebhook`, `callIntegration`,
`setAssetFlag` (a controlled flag only), `startWorkflow` (to a depth of three),
`requestApproval`, `waitFor` and `generateEvidencePack`. Four things are never
automatic at any confidence and can only be proposed to a person: refusing a visit other
than on a watchlist match, adding a watchlist entry, deleting any record, and changing an
authorisation or a permission.

**Approvals** are records with a subject, a requester, a required approver set, a
decision, a reason and a deadline.

| Property | Requirement |
|---|---|
| shapes | a single approver, a sequential chain, or a parallel quorum |
| eligibility | read from the policy at the moment of decision, never at request; a member who lost the role may not decide |
| separation of duties | the requester never approves their own request, and a chain never contains the requester |
| delegation | a member may delegate approval authority for a bounded period to a named member; the delegation is recorded and the decision names both |
| escalation | on timeout to a configured target, then to the site's operations owner; never approved silently |
| auto-deny | a configured shape where a timeout denies, for time critical requests such as a gate release |
| reason | required on a denial, and on an approval where the definition asks |
| record | every state change, delegation and escalation |
| notification | to the approver set on request, escalation and decision, once per transition |

`POST /api/approvals/{approval_id}/decisions` takes `{"decision", "reason"}` with a
decision of `approved` or `rejected`. The requester deciding their own request is
refused with `403` and code `self_approval_forbidden`; a member not eligible for that
request at that request's site is refused with `403` and code `forbidden`; a decision on
a request that is no longer pending is refused with `409` and code `already_decided`. A
refusal leaves the request and its subject exactly as they were. Approvals in flight
survive a definition change, a member's departure and a restart.

**The instance detail** shows the definition and version, the trigger and payload, each
step's state, timing, actor and result, each guard evaluation with its inputs, every
approval with its chain and reasons, every action with the record it produced, and any
compensation that ran, so a member can say why the system did what it did without help.

**The shipped definitions**, enabled per site:

| Definition | Trigger | Autonomy | Approval |
|---|---|---|---|
| inbound placement | a visit is admitted | automatic | none |
| door feed | a door's next booking is inside the lead time and its asset is not staged | automatic | none |
| door clear | a load completes | automatic | none |
| dwell escalation | an asset passes its dwell threshold | automatic to raise, propose only to move | none to raise |
| detention warning | an asset nears a detention boundary | automatic notify | none |
| appointment reallocation | a door goes out of service | propose only | site planner |
| no-show release | window and grace pass | automatic | none |
| unbooked arrival | a visit matches no booking | per site policy, propose only by default | gate supervisor |
| identity mismatch | the identity check fails | human only | gate supervisor |
| capture correction | a capture falls below threshold | human only | none, recorded |
| stale position sweep | an asset passes the staleness threshold | automatic to flag, propose only to task | none |
| reconciliation difference | observations disagree | automatic to raise | none |
| seal anomaly | a seal changes with no sealing event | automatic to raise | none |
| claim hold | a claim is raised | automatic to hold media | operations owner to release |
| plan edit | a site plan change | human only | two approvers |
| watchlist entry | an entry is proposed | human only | two approvers |
| module request | a member requests a module | human only | organisation administrator |
| access request | a member requests a grant | human only | the grant's approver set |
| gate release override | a held visit is asked to be released | human only | a site manager at that site, other than the requester |

**The exception inbox** is the console's front door: every open exception across every
surface for the site, ordered by severity then age and never by choice, grouped by kind
with a count, each item showing what happened, the evidence, the affected record, the
workflow that raised it and its actions. Actions are resolve with a controlled outcome,
defer with a reason and a time, reassign, escalate and attach to a case. An exception
past its kind's threshold escalates by itself; bulk actions are allowed only for one
kind with one outcome and record each item separately; an exception is never deleted,
only resolved, and `resolved as no action` is a deliberate choice. The inbox states its
own open count, count breaching age thresholds, and median time to resolve.

**Agent proposals.** Where a model rather than a rule proposes an action, the proposal
records the model version, inputs and confidence; a per-definition confidence floor hides
anything below it; every proposal states its reasoning in the operator's language,
referencing the records it used; a per-organisation ceiling on model invocations falls
back to the rule path when reached, never stalling; and a model never evaluates an
authorisation decision, a watchlist match, an identity comparison or an approval. A model
may propose moving a trailer. It may not decide who is allowed on site.

**Workflow edge cases.** A misfiring definition is stopped by its rate ceiling, suspended,
and its owner told with a sample of instances. A failed step compensates in reverse order,
and a failed compensation raises a severity one exception and stops rather than retrying
blindly. A requester who became an approver through a role change is refused at decision
and the request escalates. A chain whose approvers have all left escalates to the site's
operations owner, then the organisation administrator, and never expires unactioned. A
workflow cycle is refused at depth three and logged as a definition defect. An instance
at a disconnected site holds and retries its site actions idempotently on reconnection.
Two instances proposing contradictory moves for one asset: the second fails validation
naming the first and both definitions. Resolving an already resolved exception meets the
version conflict and shows the existing outcome and its actor.

### Analytics and the network control tower

**The network control tower** is one organisation scoped screen of every site the member
holds a grant on: a tile per site with name, region, live exceptions by severity, gate
queue depth, spot occupancy, service level state and a sparkline of the day's throughput;
the day's network totals; each service level objective with attainment and budget
consumed; the three sites furthest from their own baseline with the metric named; open
severity one exceptions and security cases; and sites by rollout state. A tile shows state,
never detail, and entering a tile enters that site. Every figure is scoped by the member's
own grants: an organisation administrator sees every site, a regional manager their
region, a site manager one tile.

**The counter** is one component for every live figure: a value, a label, a comparison
that names its baseline (yesterday, the same weekday last week, the site's own thirty day
median, or the target), and a freshness state.

**Site reports** print each metric's versioned definition on demand: gate processing time
from final capture to barrier release at the median and ninety fifth percentile; gate
queue time from first approach to final capture; total gate time from first approach to
release; check-ins per hour per lane; capture accuracy as captures accepted without
correction per kind; dwell from admission to departure by load state; detention exposure
beyond the free period per haulier and per customer of the tenant; spot occupancy sampled
every five minutes; move cycle time from creation to verification by reason and priority;
empty travel ratio; moves per spotter hour; door utilisation; door turn time from docked
to released by load type; appointment adherence per haulier; no-show rate per haulier;
exception rate per hundred visits by kind; exception resolution time by kind; autonomy
rate; and override rate per decision kind. A definition change creates a new version and
each period states which version computed it.

**Network reports** add variance between sites on one metric, module adoption per site,
cost per move by site, and savings realised against the baseline captured at deployment in
the calculator's own three categories: labour at the gate, spotter time and vehicles, and
detention.

**Service level objectives**, per site and organisation, each with a target, window, error
budget and owner: gate decision latency ninety five per cent within `4s`; total gate time
ninety per cent within the site's target; move assignment ninety five per cent within
`10s` of opening; position freshness ninety nine per cent of assets confirmed within the
staleness threshold; appointment availability answered within `2s` at the ninety fifth
percentile; severity two exceptions ninety per cent resolved within threshold; and live
channel ninety nine point nine per cent of sessions connected. A breach notifies the owner
and appears on the tower.

**The claims the product must prove** are reported per site against the customer's own
baseline captured in the two weeks before go-live: up to eighty five per cent faster gate
processing as total gate time, seventy five per cent fewer errors as capture corrections
plus downstream data corrections, and the calculator's savings categories. A site with no
captured baseline reports its improvement as unmeasurable rather than inventing one.

**Operational quality reports** visible to the customer: capture quality per camera and
kind with the cameras trending worst; detection quality per rule with fire rate, false
positive rate against dismissals and demotions; assignment quality with override rate by
term, estimate error and the worst estimated moves; and autonomy quality per definition
with instances, automatic completions, proposals accepted and rejected and the reasons.

**Queries and exports.** Reports never run against the live transactional tables the
console writes to: they read a separate analytical copy at most `5` minutes behind that
states its lag on every report. Custom reports are a saved query builder over the metric
catalogue, not a free query language. A report may be scheduled for delivery by mail or to
a destination. Exports are comma separated or columnar, generated in the background and
delivered by a signed single use link; exporting is a separate permission from viewing and
every export is recorded with its filter and row count; any aggregate crossing a customer
of the tenant boundary suppresses cells below five; and a cross-region network report is
computed per region and combined as aggregates with no row level data.

**Analytics edge cases.** A site live for two days says the period is too short rather than
drawing a line through two points. A metric definition changing mid-period shows a break
labelled with both versions. Network aggregates across zones are computed on instants and
labelled with the aggregation zone. A lagging analytical copy states its lag and refuses a
real time claim, and the tower falls back to live counts. A scheduled report whose owner's
grants narrowed is generated against the grants at delivery or cancelled. A customer with
three loads has every aggregate suppressed and the report says so. An export longer than
retention covers the retained period and states what is missing.

### Frontline surfaces: spotter, gate operator and driver

The frontline promises are explicit: an intuitive browser based application that works on
any mobile device in the operator's language, a visual first map showing where every asset
is and its status, assignments in a clear prioritised list so a spotter knows the next job
without a radio, and instant communication with managers to report an issue or ask for
help. Browser based is a requirement: nothing to install, provision, update or enrol.

**Conditions.** A five year old mid-range handset, one hand, gloves, daylight and dark, a
network that fails at the far corner of the lot. Touch targets are larger than on the
public site, type never drops below the interface default, the high contrast token set
applies, portrait first with landscape supported, no action needs precision, a long press
or a drag as its only path, the task survives a call, lock or app switch, a daylight mode
raises contrast by hand or by ambient sensing, and the language is the member's own.

**The spotter surface** shows one task at a time, full screen: the asset identifier very
large, origin and destination spot identifiers large, the reason, and the due time as a
countdown; the route on the frontline map; one large accept; a reject needing a controlled
reason; large controls for hooked, moving and placed in order; the next task only once the
current one is placed; the queue depth shown but not browsable by default, viewable but not
reorderable by a permitted operator; and help always present. Confirming placed captures the
operator's position and, where the site has coverage, triggers the verifying observation.
The operator is never asked to confirm what a camera can see.

**The frontline map** is the yard map at reduced fidelity: the operator's own position, the
route, the target spot highlighted, and assets within a radius, with no inspector, bulk
selection or move proposal. With no position fix it draws the plan, the target and the
route from the last known position, and says there is no fix.

**The gate operator surface** is the lane board for one lane on a fixed screen or handheld:
the visit's captures with large images and low confidence marked, one confirm per capture
with a correction keyboard suited to the kind (alphanumeric for a plate, numeric for a
seal), release, hold or refuse each with the checks behind the recommendation, a refusal
needing a reason and, where configured, a supervisor, and the vehicles waiting behind with
their waits. Refuse is never next to release and never in the same place across states.

**Offline.** The shell, site plan and translated strings are cached; the current task and
the next two are cached; accept, hooked, moving, placed, reject and issue report are recorded
locally with time and position and queued; the queue delivers in order on reconnection, each
action idempotent on a locally generated identifier; an action against a move reassigned
while offline is refused on delivery, the operator told, and the action kept for the record;
local timestamps carry the device's clock skew against the last server contact; the local
queue is bounded and says it cannot take more work offline rather than dropping the oldest;
and the offline state is persistent and unambiguous, so a spotter never believes a completion
was recorded when it was not.

**Communication.** An issue report takes a controlled category, an optional photograph, an
optional note and the position, and creates a routed exception. A safety report has its own
severity, goes straight to the site's safety owner, is never closable by the reporter's own
manager alone, and is the first item delivered on reconnection. A help request goes to the
dispatcher with the current task attached. A dispatcher broadcast to operators on shift is
acknowledged, with unacknowledged broadcasts visible. Direct messages run between an operator
and the dispatcher within a shift. There is no free messaging between operators.

**Language.** Every frontline string, including errors, reasons and controlled options, comes
from a translated set chosen by the member, falling back to the site's language, then the
organisation's, then the default, never to a raw key. Spot, door and asset identifiers are never
translated; numbers, dates and durations follow the locale; right to left layouts are supported
with the yard plan never mirrored; and an untranslated string blocks that locale's release.

**Frontline edge cases.** A shift ending mid-task warns before and at the end and the handover
lists the task. A critical battery drops to text only without the map and says why. A missing
asset is rejected with that reason. Two operators accepting one move by a race: the second is
refused naming the first. A member deprovisioned mid-shift has the session ended at the next
contact, queued actions still accepted on delivery, and the open move returned to unassigned. A
plan updated mid-shift invalidates the cached plan, warns the operator and recomputes the route.

### The haulier portal

An organisation outside the tenant writing into the tenant's schedule is the single most
dangerous surface in the build. The portal is its own estate with its own identity space,
session policy, rate limits and permission model. It shares the database and shares no code path
that resolves a tenant member's permissions.

**Three objects, never confused.**

| Object | What it is |
|---|---|
| haulier | a company, existing once in Junction, keyed on a verified identifier such as a motor carrier registration |
| haulier site authorisation | one haulier and one site of one organisation: authorised or not, for which directions and asset classes, from when to when, with an owner and a review date |
| haulier user | a person at a haulier who sees that haulier's own bookings and nothing else |

A haulier delivering to two customers of Junction is one haulier with two authorisations. A
haulier user sees only the sites their company is authorised at and only their own company's
bookings there. **A haulier must never learn, from any response, error, timing or enumeration,
which other organisations use Junction or what another company has booked.** A booking belonging
to another company, and a site the haulier is not authorised at, answer exactly as a booking or a
site that does not exist: `404` with code `not_found`, with the same message.

**The register and authorisation** live in the console's admin surface and every change is an
approval, never a direct write: a member proposes a haulier by verified identifier and the company
is matched or created; insurance, operating authority and required certification are verified with
expiries; authorisation names sites, directions, asset classes and dates; at least one approver
other than the proposer approves; an authorisation nearing expiry raises a task and an expired one
stops permitting bookings and holds arriving visits; a suspension takes effect at once with a
reason, notifies the haulier, cancels future bookings with a stated reason, and never silently voids
a booking a driver is already driving to, whose arrival is held for a person to decide.

**The haulier home** shows upcoming visits across every authorised site with window, site, door
where assigned, driver and state, and the haulier's own reliability figures beside the site's
threshold, never ranked against other hauliers.

**Booking** separates availability from reservation.

- `GET /api/portal/sites` lists the sites the caller's company is authorised at as
  `[{"id", "name", "time_zone"}]`; for a customer user it lists the sites where that
  customer's loads were handled, in the same shape.
- `GET /api/portal/sites/{site_id}/availability` with query `date` (`YYYY-MM-DD` in the site's
  zone), `direction` and `asset_type` returns a JSON array of `{"starts_at", "ends_at"}` windows the
  caller's own request could be booked into, and nothing else: never the site's occupancy, never who
  else is booked, never a door, and never how many doors exist.
- Selecting a window may place a soft hold of `10` minutes so a haulier completing the form does not
  lose it, warned before expiry with an offer to extend, re-evaluated if it lapses.
- `POST /api/portal/sites/{site_id}/bookings` books, re-evaluating every constraint on the server
  and assigning a capable free door itself; a failure names its constraint with alternatives.
- At a site requiring approval a booking enters `requested`.
- A booking may be amended or cancelled inside the site's lead time rules, and otherwise requested
  from the site, with `POST /api/portal/bookings/{booking_id}/cancel`.
- The haulier attaches the load documents the site requires for that direction and names the driver,
  telephone and language from its own roster.

Availability search and booking are rate limited per haulier user, per haulier and per site, because
an unlimited availability search maps a competitor's yard over time. Each of those limits admits at least one hundred and
twenty requests a minute, and a request past one is refused with `429` and code `rate_limited`.

**The visit view** shows, for a booked visit, the window, the site's address and arrival instructions,
the door where known, documents, driver and state once the visit begins; once on site only the state
changes and nothing about the yard; and after departure the time on site, the detention position and,
where the tenant enables it, the evidence pack for the haulier's own load.

**Drivers and credentials.** The haulier keeps its own roster of name, telephone, language, licence
class, endorsements and expiries. The tenant sees only the driver named on a booking and the haulier
never sees the tenant's identity captures. A credential expiring before a booked window warns at
booking and again at the reminder. Removing a driver leaves past visits intact. The roster holds no
document images and no identity numbers.

**Settings** hold contacts for confirmations, changes, no-shows and authorisation reviews, the
haulier's notification preferences, and the company profile with verified identifiers and
certification documents.

**The driver's visit link.** A driver may have no account and still needs instructions.
`GET /api/visit-views/{token}` needs no session and returns the window, the site address, arrival
instructions, the assigned door or spot once known and a contact number, and never the load detail,
the customer name, any other visit, any map beyond the arrival route, or identity data. The token is
short and unguessable, returned as `visit_link` the moment the booking is made and delivered again in
the reminder, valid from the booking until `4h` after the visit closes, rate limited per token and reissued if enumerated, and it grants a view only, never an action
beyond acknowledging arrival. **A token for a cancelled booking is refused from the instant of
cancellation with `410` and code `visit_link_revoked`.** A token opened after its visit closed shows a
stated message and the site's contact number, never an error page.

**Portal security.** A haulier user can never hold a tenant role; the portal idles out sooner than the
console and a haulier administrator needs a second factor; authorisation is evaluated on the haulier's
identity wherever rows are read; site, booking and driver identifiers are opaque and non-sequential;
search, booking, amendment and uploads are rate limited per user, haulier and address; uploads are
scanned, type restricted, size limited and never served from a path a tenant surface trusts; and the
tenant sees haulier user activity at its own sites in its own record.

**Portal edge cases.** A haulier suspended at one of two sites of one organisation has only that site's
bookings cancelled and the portal says which. Two users of one company booking one slot: the second
meets the constraint re-evaluation with alternatives. An expired soft hold re-evaluates, offering the
nearest alternatives without losing the form. A disputed no-show is raised against the tenant with the
visit attached and only its resolution changes the reliability figures. A company merger keeps both
prior identifiers and past attribution. An uploaded document with personal data is stored under the
tenant's retention and residency, and the upload notice says so.

### Module and component architecture

**What the reference used is information, not instruction.** The measured product was
a component framework with a file based router and a central store, rendered on the
server then hydrated, with a utility class styling layer, a smooth scroll controller, a
carousel, an unstyled accessible primitive set for navigation and dropdowns, and a
timeline library carrying scroll linked timelines, path drawing, custom easing and text
splitting. None of it is required. What is required are the capabilities it implied: a
content route rendered without a layout shift; an animation linked to a scroll position
rather than a clock; a vector path drawn progressively; a heading split into characters
without breaking its accessible name; interpolation on an authored curve; ownership of
document scrolling that can be taken and given back; accessible navigation and
disclosure primitives; and a carousel with keyboard, pointer and disabled end semantics.

**Four component layers, depending only downward.** Tokens hold the design values and no
logic. Primitives are button, field, select, checkbox, radio, disclosure, dialogue,
popover, tabs, table, toast, tooltip, badge, counter and digit stack, with no product
vocabulary, no data fetching, full keyboard operation and a documented accessible pattern
each. Patterns are card, panel, boundary, connector figure, ruled grid, logo wall,
carousel, calendar, board, map, queue, inspector, form panel and evidence viewer, with
product vocabulary and state through properties but no fetching. Features compose a route
or surface and alone fetch data, check permissions and call workflows. A permission check
never lives below the feature layer.

**State has four homes.** Server state lives in a query cache keyed by resource and scope,
with the site in scope in every key. Live state from the live channel patches that same
cache and never a second store. Interface state stays inside its component. Session state is
one small module holding identity, grants, entitlements, preferences and the site in scope.
Grants and entitlements cached in the browser are for presentation only and are decided again
on the server for every request.

**Data access, and changes that appear at once.** Each application has one generated client from the
HTTP contract, and no feature writes a request by hand. Every call carries the site in scope,
a request identifier and, where it writes, an idempotency key. Exactly three operations may
show their change at once and undo it with a message if the save fails, because their latency is felt and rolling back is safe: accepting a
move, resolving an exception and toggling a filter. Every other write shows a pending state
and waits: a gate release shown before it is saved is a barrier that opened on screen and not in the world.

**Errors.** A panel boundary states its failure and offers a retry while the rest of the
surface works; a surface boundary keeps the shell and states the failure with a request
identifier; an application boundary shows the static failure document. Every error a member
sees carries a request identifier matching the server's trace, and every message states what
failed, what the member can do and whether work was lost, never that something went wrong.

**Suites that exist, and what they protect.** The computation of the calculator and the
assignment cost; the contract between client and server; the policy, per role, action and
resource; tenancy, attempting every read and write across a tenant and a site boundary; every
state machine, exhaustively; idempotency, replaying every write and webhook; recorded
integration exchanges; accessibility on every route and surface with a manual keyboard and
screen reader pass on the console and frontline; visual at nine scroll positions and three
widths; performance against the budgets; offline on the frontline; and chaos on the site
connectivity path. The policy and tenancy properties block a release; the rest report.

### Backend architecture

The source of truth is physical, so every record is a lagging, probabilistic model of a yard
and every read can say how stale and how confident it is. Ingestion is continuous and site
local. Decisions at the gate are bound to four seconds. The record is evidence, so custody and
audit only ever grow and nothing that matters is edited in place.

**Seven boundaries**, which a smaller build may merge but must keep visible in its code:
identity and policy (principals, sessions, roles, grants, entitlements, decisions); yard state
(sites, plans, assets, positions, spots, doors, moves, visits); scheduling (appointments,
availability, capacity, hauliers, authorisations); evidence (custody, observations, media
references, audit, evidence packs); workflow (definitions, instances, approvals, exceptions);
integration (connectors, mappings, exchanges, webhooks); and analytics (the analytical copy,
metrics, reports, exports). The gate decision crosses identity, yard state and scheduling and
keeps its four second budget including every hop.

**Communication, as guarantees.** The browser reaches the services through one gateway that
ends the session and supplies the principal. A site's edge delivers batched observations over a
mutually authenticated channel with a per-site credential, at least once, with idempotency
keys. Synchronous calls between boundaries exist only where a caller cannot proceed without an
answer: the gate decision, a policy decision, a booking constraint check. Everything else
flows as events with per-subject ordering. **A state change and the event that announces it are
never separated: stopping the process between them neither loses the event nor invents one.**
Every consumer ignores an event it has already handled, and every call to a partner carries an
idempotency key derived from the record rather than from the attempt.

**Consistency, per operation, named in the contract.** Booking a slot, assigning a move,
releasing a gate, deciding an approval, writing a custody event and changing a grant are
strongly consistent: a conflicting concurrent write is refused, never merged. Every console read
after a write by the same principal sees that write. Analytics, rollups, search and reports are
eventually consistent with a stated lag. Three operations span boundaries and must never half
complete, each undoing what it did if a later part fails: booking a slot that reserves a door and
creates an expected visit; admitting a visit that binds a booking, creates a move and reserves a
spot; and completing a load that writes custody events, frees a door and creates an outbound move.

**Deployment.** At least two regions, an organisation pinned to one for its operational data; a
site's identity, yard state and scheduling served in its own region across three failure domains;
the gate path surviving the loss of one failure domain within its objective; the site edge
surviving the loss of the region in degraded mode; the content site served globally from the edge;
and region failover deliberate, documented and rehearsed, never automatic, because moving a
residency pinned tenant automatically is a compliance incident.

**Stores, all in PostgreSQL here.** The relational tables are the source of truth for anything a
decision depends on, and their integrity rules are the enforcement mechanism for tenancy; custody
and audit are append only and verifiable; positions and observations are a high volume projection
partitioned by time and dropped by partition on retention; media is referenced with lifecycle and
per-organisation encryption and no public address; and search, cache, analytical copy and event log
serve their sections. A position a decision relies on is also written to the relational record.

**Multi-tenancy.** One logical database per region with every tenant table carrying its organisation and
every site table its site, both enforced where rows are read. The application's database role
cannot read around those rules and migrations use another role. Organisation and site are set from
the authenticated principal at the start of every transaction, never from a request parameter.
Background jobs run under the same scoped rules. A very large tenant may move to its own database by
routing alone. The single most likely catastrophic defect is a handler that forgets a tenant filter,
and the tenancy rules make that return nothing rather than everything.

**Failure containment, in priority order.** Analytics down: reports say so and operations continue.
Integration down: exchanges queue and partners are told while the gate, map and dispatch continue.
Workflow down: automation stops, manual work continues, and the console says automation is suspended.
Evidence down: operations continue, custody events queue durably at the site edge, and a gate release
needing a custody write is held. Identity down: existing sessions continue on cached grants for a
bounded window with writes disabled and no new sessions. A lost region follows the recovery plan. A
disconnected site runs in degraded mode. When it must choose, Junction keeps the gate open, the map
current and the moves flowing, in that order, and tells the operator what it gave up.

### Integrations, webhooks and the live channel

Interoperation with a warehouse system and a transport system is a public commitment and the largest
ongoing failure surface.

**The HTTP contract as a product.** One machine readable schema is the source of truth and both
server and clients are generated from it; resources read as a verb on a noun; a major version lives
in the path, minor changes only add, and a deprecated field announces its sunset date in a response
header before removal; every operation is scoped to an organisation and names its site explicitly;
identifiers are opaque; every operational collection pages with a cursor and never an offset; each
collection has a defined filter grammar rather than a free query; a field selection parameter lets a
board skip media references; errors carry a stable machine code, a message, the field where
applicable, a request identifier and a retry indication; instants carry an offset and durations are
seconds; **every write accepts an `Idempotency-Key` header and returns the original response for a
replay of the same key and the same body within twenty four hours, while the same key with a
different body is refused with `409` and code `idempotency_key_reused`**; and every mutable resource
carries a `version` that an update must name.

**Machine access.** Credentials hold only the operations their exchanges use, are bound to an
organisation and optionally a site set, rotate with overlapping validity, and are rate limited per
credential, operation class and organisation with the remaining quota and reset instant on every
response, a token bucket burst allowance so a nightly reconciliation is not refused into failure, and
limits enforced per organisation before any global limit.

**The eight exchanges**, each bidirectional where the partner supports it:

| Exchange | Direction | Trigger | Carries | On failure |
|---|---|---|---|---|
| inbound asset notification | out | a visit is admitted | asset, load reference, haulier, booking, arrival instant, destination | queued, retried, surfaced after the retry budget |
| spotting task management | both | a move changes state; a partner requests a move | move, asset, origin, destination, reason, priority, state, timing | an inbound request breaking move validation is refused with the constraint named |
| intelligent dock scheduling | both | a booking changes; a partner proposes one | booking, door, window, constraints | an inbound proposal breaking a booking constraint is refused with alternatives |
| inventory reconciliation | out | on schedule and on demand | the inventory with positions, states and confidences at an instant | the instant is always stated |
| dynamic receiving prioritisation | out | a high priority inbound load is admitted or imminent | load, priority basis, expected availability | queued and retried |
| agentic exception handling | out | an exception is raised and resolved | exception, subject, diagnosis, action taken or proposed, instance | never retried into a duplicate action, idempotent on the exception |
| automated trailer status update | out | a state or position change crosses a partner relevant threshold | asset, state, position summary, dwell, confidence, instant | coalesced to the latest, never a storm |
| detention and demurrage alert | out | a dwell threshold is crossed | asset, load, haulier, customer of the tenant, free period, elapsed, projected charge | once per asset per threshold per visit |

Every outbound exchange states the instant its content was true, so a partner never treats a five
minute old inventory as current. A trailer moving across a yard produces continuous position
changes, and a status feed that sends each one is how an integration gets switched off.

**Connectors are configuration**: partner kind, endpoint, credential reference and environment;
field mappings both ways with code list translation for asset types, load states and reason codes;
enablement per exchange per site; a sandbox binding with a replayable fixture set; health as last
success, last failure, error rate, queue depth and state; and a named owner who receives failures.
Enabling an exchange is what widens a connector's credential scope, never more.

**Webhooks** per organisation, optionally per site, each subscribed to event kinds: every delivery is
signed over the raw body and a timestamp with a per-endpoint secret, two secrets valid during a
rotation; the timestamp sits inside the signature and receivers reject deliveries older than five
minutes; a delivery identifier and an event identifier stay stable across retries; ordering is
guaranteed per subject, not globally; retries back off exponentially with jitter for twenty four hours
and then mark the endpoint failing; after a stated run of failures the endpoint is disabled, its owner
told, and undelivered events kept seven days for manual replay; an operator may replay one delivery or a
time range, marked as a replay; a payload carries the event and a reference to the resource, never a
media object or identity data; and the customer sees a delivery log of request, response status and
timing with the body redacted. The receiver guidance is part of the product: verify the signature, check
the timestamp, be idempotent on the event identifier, answer within five seconds and process
asynchronously.

**The live channel** delivers console and frontline updates by server push, upgradeable to a two way
socket where a surface sends; it is authorised at connection and again on grant change, disconnecting a
revoked member within `30s`; subscriptions are per site and surface; each subject carries a sequence
number so a client detects a gap and refetches those subjects rather than reloading; it falls back to
polling at a stated interval with the freshness indicator telling the truth; the server coalesces per
subject so a slow client receives the latest state, never a backlog; and connections are limited per
member and per organisation.

**The public streaming path** for the conversational agent streams from the content site,
unauthenticated, rate limited per address and session, with a hard token ceiling per response and per
session and a stated behaviour when exhausted.

**The content back end interface** validates every publish: required fields present, references
resolving, the cross linking graph rules holding, every case study metric carrying a basis, every rival
claim carrying a source and a date, and every locale complete. A failing publish does not publish and
names every failure.

**Reconciliation** runs for every integration and reports, never resolves: exchanges with no confirmed
delivery re-enqueued hourly with their original key; the partner's asset list compared daily and on
demand; bookings present in one system and not the other reported hourly to both owners; undelivered
webhook events per endpoint daily with a replay action; and credentials past their maximum age or wider
than their enabled exchanges weekly. Every connector ships a recorded exchange fixture set including the
partner's known error and malformed responses.

### The vision pipeline and the edge estate

The commitments: plates, identity documents and container numbers read in seconds; flexible technology
that works with cameras a customer may already own; plug and play commissioning without a construction
project; live in five days with low information technology lift and no third party devices to support; a
vehicle mounted location service updating positions continuously; automated damage detection at the point
of action; and the eighty five and seventy five per cent claims.

**The estate** is cameras at each gate lane, on existing yard poles and buildings and at each dock door,
using the customer's own where they meet the specification; one or more site nodes running inference,
buffering and the lane decision cache; and vehicle units on spotter tractors for position and a screen
mount. The vehicle unit is managed entirely by the vendor and never enrols in the customer's device
management, which is why it does not break the no third party devices promise.

**The observation** is the only thing that leaves a site by default: a kind of plate, container number,
trailer number, seal, document, presence, position, condition, movement or tamper; a normalised value;
ranked alternatives with their own confidences; a calibrated confidence rather than a raw score; the source
camera or vehicle unit; the instant from the site's own time source with its skew recorded; the region in
frame and, where calibrated, the position on the plan; a media reference resolved only when a person opens
it; and the model version. An observation is never overwritten; a correction is a new observation referencing
the original. Raw video never leaves the site by default.

**At a lane** everything but the policy decision runs locally within the four second budget: detection
within `200ms` of the frame, continuous tracking with best frame selection per kind, reading at `600ms` per
kind in parallel, calibration and assembly in `100ms`, delivery in `300ms`, the checks in `1.5s`, and the
decision back in `300ms`. The pipeline never reads the first frame a plate appears in: it tracks the vehicle,
scores frames per kind on sharpness, angle and occlusion, reads the best two and agrees them. Camera tamper
detection runs continuously for a changed field of view, an obscured lens, persistent exposure failure or a
stopped stream, raises a security event and marks the camera degraded.

**Commissioning.** A published camera minimum per capture kind for resolution, frame rate, shutter, dynamic
range, mounting height, angle and illumination; a survey that ingests a sample stream and names the failing
parameter per kind; a guided calibration placing four or more ground points to produce the camera to plan
transform; coverage computed from calibration and shown on the map; enrolment with identifier, location, role
and retention class before any observation; per-camera health of stream, frame rate, latency, tamper and
accuracy; and the five day claim measured by the commissioning flow itself. Before go-live the survey runs
remotely; day one installs and connects the node and enrols and verifies cameras; day two calibrates and has the
plan authored and approved; day three runs shadow mode, deciding without acting and measuring accuracy against
the manual record; day four sets thresholds from that, configures policy and provisions members; day five goes
live at one lane with an operator confirming every decision and the baseline already captured; then lane by
lane and module by module. Shadow mode is never skipped: it produces the thresholds and the baseline.

**Model quality.** Confidences are calibrated per site and kind against observed correction rates; thresholds
come from the site's own accuracy; every operator correction is kept as a labelled example with its frame; a
customer's frames improve only that customer's calibration unless an explicit, revocable organisation agreement
permits general training, and its state is visible in the console; a model version is promoted at a site only
when it beats the incumbent on that site's own held out set, rolled out in stages with automatic rollback on an
accuracy regression; and accuracy per camera per week raises a maintenance task before a camera starts failing
decisions.

**Disconnected operation.** Capture and reading continue locally. The gate decides against the lane cache of the
next twelve hours of bookings, the haulier authorisations and the watchlist, refreshed while connected. A
decision the cache cannot make holds the visit, says the site is offline and offers a supervisor override with a
recorded reason reviewed on reconnection. A watchlist match still refuses, and a cache past its maximum age fails
closed on refusals and open on ordinary admissions and says which. Positions continue locally. Assignment runs
locally with handhelds offline. Custody events are written and chained locally and merged in order on
reconnection. The buffer delivers in order with idempotency, every offline override is surfaced for review, and
on approaching its capacity the node sheds continuous footage first and never observations or custody events.

**Edge security.** Each node holds a hardware backed credential, opens outbound connections only with no inbound
port, keeps video on site, takes signed staged updates with automatic rollback and never during operating hours
without approval, reports its own tamper state and stops producing observations when it cannot attest its
integrity, and sits on its own network segment with a documented firewall requirement.

### Background work and notifications

**Four primitives, chosen per job and named in it.** A queue for event triggered, retryable work such as a lead
dispatch, a webhook delivery or an evidence pack; a scheduled job for work at a time, idempotent per period, such as
retention, reconciliation or the no-show sweep; a durable workflow for multi-step work with waits, timeouts,
approvals and compensation; and a stream consumer for continuous ordered volume such as position ingestion. A
process that waits on a person is never a queue job that sleeps and never a scan of a state column.

**Every job** runs under a scoped principal, never spans two organisations in one execution, is idempotent on the
domain record and period, retries with exponential backoff, jitter and a ceiling into a visible, replayable dead
letter, dead letters a deterministic failure rather than retrying it forever, has a timeout, is traced with tenant,
subject and outcome, respects a per-organisation concurrency ceiling, and computes its window from its last
successful run rather than assuming it ran on time. Two instances never both run: a lease lets one proceed and the
other exits cleanly.

**The queue catalogue:** lead dispatch, consent withdrawal propagation, gated document delivery, grader report
generation, evidence pack generation, export generation, webhook delivery, exchange delivery, media transcode and
rendition, observation enrichment, notification fan-out, search index update and model example collection.

**The scheduled catalogue:** the no-show sweep and the appointment reminder every minute; the dwell and detention
threshold sweep every minute; the stale position sweep every five minutes; exception ageing and approval timeout;
directory reconciliation every four hours; exchange reconciliation hourly; integration and lead delivery
reconciliation daily; the retention sweep daily; credential and grant expiry tasks daily; authorisation and watchlist
review tasks daily; content publish invalidation on publish, computed from the reference graph for exactly the
affected routes and never a global purge; the index rebuild nightly; the analytical rollup every five minutes and
nightly; model drift weekly; and backup verification daily. Where a state is a pure function of time, such as a
booking becoming `no_show`, a hold lapsing or a watchlist entry expiring, it reads correctly from the moment it
becomes true whether or not a sweep has run.

**Notifications.** One service, one preference model and one idempotency rule for every channel (in product, mail,
message to a mobile number, integration destination) and every audience (a member, a role at a scope, a haulier
contact, a driver, a machine destination). Preferences per member, kind and channel with organisation defaults and
site overrides. A kind may arrive immediately or in a digest, except an operational alert, which is never digested.
Quiet hours are honoured except for a severity one exception or a safety report, which are delivered anyway with the
override stated. **One notification per subject, kind and triggering transition: a retry never sends a second
message, because the message's identity comes from the transition and not from the attempt.** A burst of one kind for
one subject collapses to one with a count. An unacknowledged severity one notification escalates on a stated ladder.
Every attempt records channel, provider response and final state on the subject. Content never carries identity data,
load detail, a customer name or a media object. Non operational mail carries an unsubscribe; an operational alert to a
member does not.

**The retention sweep**, the most consequential job: every retention class per organisation; legal holds suspend
deletion for their subject; identity media deleted on its own schedule and never held; time partitioned tables dropped
by partition and media by lifecycle; every store a value reached covered, including the analytical copy, the search
index, the cache, backups within their window and any retained export; a report of what was deleted by class and
organisation, alerting when a class deleted nothing it should have; a failure raised as severity one; and a dry run mode
used before any class's period changes. An object referenced by a pending evidence pack request defers one cycle.

**The change stream.** Every committed change is published once to a durable log partitioned per organisation and
ordered per subject, feeding the analytical copy, the search index, webhook fan-out, notifications and workflow
triggers from one path, so a report and a webhook never disagree.

### Mail

Every message goes over real SMTP to `SMTP_HOST` at `SMTP_PORT`, one message per recipient, no cc and no bcc.

| When | To | Subject | Body |
|---|---|---|---|
| a booking is confirmed | the haulier's booking contact | `Junction booking confirmed: ` followed by the booking reference | the first line is the booking reference on its own; then the window and the site; never the load reference, the customer, the goods or identity data |
| a booking is cancelled | the haulier's booking contact | `Junction booking cancelled: ` followed by the booking reference | the first line is the booking reference; then the reason |
| a no-show is recorded | the haulier's booking contact | `Junction no-show recorded: ` followed by the booking reference | the first line is the booking reference |
| an approval request enters `pending` | every member eligible to decide it except the requester | `Junction approval requested: ` followed by the approval identifier | the first line is the approval identifier on its own; then the action and the requester |
| an approval is decided | the requester | `Junction approval granted: ` or `Junction approval rejected: ` followed by the approval identifier | the first line is the approval identifier; then the decision and its reason |

Replaying the request that confirmed a booking never produces a second confirmation message.

### Caching, validation and concurrency

**Two caching rules decide everything.** A response that depends on a principal is never stored where another
principal's request could reach it, and a cached operational value carries its age wherever it is shown.

- The content site caches every route that does not depend on a request, tagged per content item, purged by tag on
  publish, with immutable assets named by content hash, and never calls its content back end from a visitor's browser,
  because the token stays on the server.
- **Every console and portal API response carries `Cache-Control: no-store`**, the browser's own cache holds nothing
  that depends on a principal, and the query cache is keyed by resource, organisation and site and cleared on sign out
  and on a site switch.
- The server may cache the site plan, the role and policy set, the entitlement set and the haulier authorisation set,
  each keyed by organisation and site, short lived and invalidated by the change stream.
- Nothing that decides a permission is cached for longer than five seconds, and a revocation invalidates it explicitly.
- A cache key is built by one function that cannot be called without its scope; a cache warmer runs scoped; the vary set
  is declared per route; and sign out clears the client cache.

**Four layers of validation, each catching what the others cannot.** The browser checks shape, type, range and format
for immediate feedback only. The server checks the same schema, generated from the one contract, and never trusts the
browser. The domain checks what a schema cannot know: a window inside operating hours, a spot compatible with an asset
type, a transition legal from the current state. And the rules that must hold whatever code path runs hold whatever
code path runs. A failed validation answers `422` with a per-field map in `fields`.

**Rate limits and quotas**, enforced per organisation before any global limit, each limited response stating the limit,
the remaining quota and the reset instant: public forms per address and origin; the conversational agent per session and
origin with a token ceiling; site search generously per origin; the console per member and organisation at an order of
magnitude above human speed, so a person at a gate is never refused for speed; portal availability per haulier user, haulier and
site, deliberately tight; portal booking per haulier with a stated retry after; the machine interface per credential,
operation class and organisation; the live channel by connection counts; and inbound integration calls per endpoint.

**Concurrency.** Every mutable record carries a version and every update names the version it read; a mismatch is a
conflict surfaced to the person with what changed and who changed it, never resolved by the last write winning and never
silently retried. Two dispatchers assigning the same move both find out. Reservations of finite resources, a door for a
window and an open move for an asset and its destination, never over-allocate under simultaneous writes. Every write
accepts an idempotency key.

**Input handling.** Queries are parameterised everywhere; rendered documents escape by default with raw insertion only
through one audited helper used by the rich text renderer over a sanitised block set; state changing requests need a
same-site cookie or a bearer token, pass an origin check, and are never registered on a safe method; the console and
portal refuse to be framed; a strict nonce based content policy forbids inline script and reports violations; uploads
follow the portal rules; redirect parameters come from an allow list; mail headers cannot be injected through a name
field; and payload size, nesting depth and slow clients are bounded before parsing.

**Edge cases.** A stale policy cache at revocation is invalidated explicitly and the thirty second bound holds anyway. An
unavailable cache makes every read fall through: slower and correct, never faster and wrong. An idempotent write replayed
with a different body is a conflict. A schema relaxed on the client and not the server is a contract failure. A legitimate
nightly reconciliation hitting a limit is covered by the burst allowance and a sustained breach alerts the connector's
owner.

### Compliance, audit and data governance

**What Junction holds**, each class with a stated retention, residency, access permission, deletion path and owner:
identity data (driver document images, face images, recognition tokens), the most sensitive; workforce data (member
identities, shifts, individual performance, footage of people working), subject to employment law and works council
agreements; commercial data (volumes, dwell, detention exposure, customers of the tenant, haulier reliability), where a
leak between tenants is a competitive harm; freight data (load references, goods, temperature regimes, hazard classes),
the tenant's customers' data; evidence (custody chains, seal records, media), legally significant; and visitor data (form
submissions, agent transcripts, consent records).

**The audit record** is append only, tamper evident, queryable and its own subsystem. It records every state changing
action, every access to a restricted class, **every authorisation denial**, every policy and grant change, every
configuration change, every export and every break glass action, each with the actor and actor type, the grants in effect,
the action, the resource type and identifier, the organisation and site, the instant, the source address range, the request
and session identifiers, before and after values where applicable, the reason where required, the policy version and any
elevation identifier. It is chained per organisation with each entry carrying the previous entry's hash, the head anchored
externally at a stated interval; it has no path that changes or removes an entry; it is kept at least seven years; it
answers queries by actor, resource, action, time range and site within `2s` for ninety days; it is read with `audit.read`
by an organisation administrator and a security administrator and exported only with an individually granted
`audit.export`; and a gap in its sequence is itself an alert. `GET /api/audit` with optional query `action` and `outcome`
returns entries newest first as `[{"sequence", "action", "outcome", "actor_email", "resource_id", "occurred_at"}]` with
`outcome` of `allowed` or `denied`.

**Restricted access.** Reading identity media, reading unbounded footage, generating an evidence pack, sharing federated
evidence and exporting anything each take a required reason at the point of access and record what was accessed. A member
sees their own restricted access history, and an organisation administrator receives a weekly summary of restricted access.

**Retention defaults and bounds**, configurable per organisation within them: identity media `30` days, `7` to `90`, never
extended by a hold; recognition tokens `24` months, `0` to `36`, revocable; gate condition and seal media `180` days, `30`
days to `7` years; continuous footage `7` days, `1` to `90`; observations `13` months, `3` months to `7` years; position
history `13` months, `3` months to `7` years; visits, moves and appointments `7` years, `2` to `10`; custody chains `7`
years, `7` to `10`, never below the claim window; the audit record `7` years upward; individual workforce performance `13`
months, `3` to `24`, then aggregated; visitor submissions and consent `36` months from last contact, `12` to `60`; and agent
transcripts `30` days, `7` to `90`.

**Encryption.** Encryption in transit everywhere including inside the deployment, with the site node channel mutually
authenticated; every store encrypted at rest and media per object; identity media, custody media and continuous footage under
a per-organisation key, so destroying the key destroys that organisation's media; customer managed keys offered with the
consequence stated plainly, that a revoked key makes the media unreadable to the customer's own operators too; field level
encryption for identity capture fields, credential hashes, webhook secrets and connector credentials; scheduled rotation by
re-wrapping; and keys never reachable from a role that can read the ciphertext in bulk.

**Governance surfaces** in the admin area: the data inventory with each class's retention and residency, the current policy
and its version, the grant register, the restricted access summary, the audit query, legal holds, the consent to train state
and deletion requests.

**Residency.** An organisation is pinned to a region at creation, and every operational record, media object and backup stays
there; video never leaves the site; a member in another region reads through the pinned region without replication; network
reports combine per-region aggregates; every processor is listed per region with its agreement and data classes; per site
configuration covers biometric comparison, a second approver for workforce footage and the retention floor; and changing
residency is a governed migration.

**Export and portability.** Export permissions are distinct from reads; every export records actor, reason, filter, row count
and destination; delivery is a signed single use link, never an attachment; content never includes identity media or another
tenant's data and applies suppression; every document carries the organisation, requester, instant and filter so a leaked
export is traceable; a full organisation export is an approval, generated in the background, excluding only identity media and
other tenants' data; and export volume per organisation per period is limited, because bulk export is what exfiltration looks
like.

**Minimisation in outputs.** Identity media, recognition tokens, raw footage and full media objects never appear in a webhook,
an exchange, an export, a notification, a log line, a trace attribute, an analytics event, an error message, a support bundle or
an evidence pack. Output paths refuse those field types, a scrubber runs on the way out, and a release fails if a prohibited
field is reachable from a prohibited path.

**Deletion.** A visitor's submission, consent record and transcript are deleted within thirty days of a request and the deletion
is recorded. A driver's identity media is already on a thirty day schedule and the recognition token is deleted on request, while
the visit record persists as the tenant's business record and the response says so plainly. A departing member is deprovisioned
while their identity in the audit record remains, because a record with its actors removed is not a record. An organisation at
contract end gets a notice period and a full export, then deletion from every store, the search index, the analytical copy, the
caches and finally the backups, with key destruction making media unreadable immediately. A deletion that misses a denormalised
copy has deleted nothing.

**For a buyer's reviewers** Junction produces a system description, a data flow diagram per class, a processor register, the
retention schedule, the permission matrix, the access review procedure, the incident procedure and the accessibility statement.

### Observability, reliability and failure handling

**What must be answerable.** Why a gate is slow now, and why one lorry waited eleven minutes, from a trace joined to the visit;
why a move went to a spotter, from the move detail; why a member was denied, from the explanation surface; who read a driver's
document and why, from restricted access records; whether automation is improving, from the quality reports; which sites are
degrading, from the tower; and whether observations were lost in an outage, from the gap records. Four of those are product
surfaces rather than telemetry, because a question only the vendor can answer is a support ticket.

**Tracing** propagates a standard trace context through the API, the event log, queues and the site node channel; carries
organisation, site, principal type, surface, operation and domain subject, never a restricted value; samples ordinary traffic
lightly and keeps every gate decision, every write, every error and every request from a member who reported a problem; spans each
gate check so a latency breach names its cause; and joins browser navigation and live update spans by request identifier.

**Logs** are structured events, never formatted strings, each with instant, level, service, trace and span, organisation, site,
principal type, request identifier and event name; restricted classes are refused and scrubbed; logs are queryable per organisation
with support access scoped and recorded; they are kept ninety days hot and thirteen months cold; and **every error response returns
its `request_id`**, the join between a customer's screenshot and an engineer's query.

**Alerting is on symptoms and error budget burn**, never a raw resource figure, each alert naming an owner, a runbook and a customer
impact: gate decision latency burning its budget over fourteen times the sustainable rate over an hour; any lane failing to reach a
decision, immediately; the live channel objective breaching for fifteen minutes; a site producing no observations for two minutes in
operating hours; a queue above threshold for ten minutes; a dead letter rate above threshold; a failing webhook endpoint; a retention
sweep failure and an audit chain gap, immediately at severity one; the policy decision latency objective breaching; backup
verification failure daily at severity one; and a per-organisation metric cardinality explosion before it affects other tenants.

**Query and load protection.** Statement timeouts per query class; slow query alerts with statement and plan per organisation;
detection of a request issuing more than a stated number of statements, because no board, queue or listing queries once per row;
connection pools per service with per-organisation ceilings; read replicas only for reporting and large reads, never a decision; and
under sustained overload shedding exports, then reports, then network rollups, then non critical notifications, never the gate path
and never custody writes, in the same order the failure containment keeps things alive.

**Data loss detection.** Each camera's observation stream is sequenced so gaps are detectable and reported per site per day; the node
reports what it buffered, delivered and shed; on reconnection the server states its range and the node replays the difference; and an
unrecoverable gap becomes a visible observation gap record stated on any evidence pack covering it.

**Product analytics**, separate from operational telemetry, consent gated on the content site and free of personal identifiers:
route views, navigation panel opens, conversion block interactions, tool starts and completions, gated form submissions and agent
sessions on the content site; surface views, exception outcomes, overrides, chord usage and unentitled offer views in the console,
visible to the customer and never used by the vendor to score an individual member.

**Backup and recovery.** Continuous relational backup with point in time recovery over thirty five days and daily object snapshots,
kept in the organisation's region under its keys; a daily automated restore of a sample into isolation with a custody and audit chain
integrity check; a recovery point of `5` minutes for operational records and zero for custody and audit events, written durably at the
site before acknowledgement; a recovery time of `4` hours for a region and `30` minutes for a failure domain; region failover rehearsed
twice a year; sites in degraded mode during failover; and every restore recorded, with any chain divergence it causes reported.

**Incidents.** Severity one for a gate down, a suspected data exposure, an audit integrity failure or a retention failure; two for a
degraded surface; three for a contained defect. A status surface updated within thirty minutes of a severity one and at a stated cadence
after, with per-organisation notification where affected. A suspected cross tenant exposure has its own procedure: contain, scope from the
audit record and never from logs alone, and notify affected organisations within the stated period. Every severity one and two gets a
written review with timeline, cause and owned actions, readable by any affected organisation.

**Rehearsal** in a production shaped environment: a site offline for four hours in operating hours monthly; a failure domain lost on the
gate path, the identity provider unavailable, a partner integration returning malformed responses for an hour and the live channel
unavailable, quarterly; a regional failover twice a year; and the daily restore. The site disconnection matters most, because it is the
failure that will actually happen.

### Build order, as dependencies

The foundations come first, and each later phase depends on the one before it.

| Chain | Runs alongside the others because |
|---|---|
| the content estate | it depends on nothing else in the product |
| the platform floor of identity, policy, tenancy and audit | every console surface depends on it |
| the observation path of site node and pipeline | it has the longest lead time and involves hardware |

| Deliverable | Depends on | What you can look at once it exists |
|---|---|---|
| tokens, primitives, the two families, the motion language and scroll control, content schemas and publish validation, the route shell, header, panels, footer and error routes, tenancy, principals, sessions, the policy decision and the audit chain, the site plan model and editor | nothing | the public chrome over empty routes in the finished visual language; a console shell that signs a member in, switches a site and refuses everything correctly |
| the home route with its sequence, the pillar, module, market and problem templates, resources and search, the forms and consent, the calculator and grader, the site node, enrolment, calibration and observation model, yard state and the map | the floor | the whole public site with both tools; a live map of a real yard |
| the visit machine, capture, matching and lane board, driver identity, instructions and the visit link, the workflow engine and exception inbox, shadow mode, baseline and commissioning | the map and the floor | one automated gate lane with a measured before and after |
| moves, assignment and the dispatch board, the frontline surface with offline, shifts and handover, reconciliation and stale positions | the gate | spotters taking jobs on a handheld with empty travel measured |
| appointments, constraints and the calendar, the haulier portal and its isolation, the dock board, verification, custody and evidence packs, federated reporting, the integration service and the eight exchanges | dispatch | the schedule, the outside world and the evidence trail |
| security events, watchlists, cases, footage governance and break glass, analytics, reports and claims, the network control tower, residency, retention, governance and deletion, webhooks and the customer machine interface, observability, backup and rehearsal | everything above | scale and governance |

The gate ships with the workflow engine, because every hold, escalation and approval at the gate is a workflow instance. The haulier
portal ships only once the tenancy properties hold against it. The network control tower, webhooks and customer defined roles come last,
because each is valuable only once several sites are live. The audit chain, the policy decision, retention and deletion, accessibility and
frontline offline behaviour come early, against instinct: a chain started late has a permanent gap, permissions added to a working system
ship a hole, identity media collected before a deletion path exists is held unlawfully, and accessibility and offline are architecture.

**Release and rollout.** Every operational change ships behind a flag per organisation and site; a decision path change rolls out site by
site with accuracy and latency watched; every release reverts without a data migration, splitting any irreversible migration into an
additive release and a cleanup release; migrations expand, migrate, then contract; the site node updates in stages with automatic rollback
and never during operating hours without approval; and the policy and tenancy properties block a release.

### The public surface and what the server owes it

**Documents the server answers itself.** The browser application renders the content
routes, but the server answers some requests completely on its own, readable without any
script:

- **The not-found answer.** Every path that is not a route in the content, console or
  portal route tables answers with status `404` and the product's own not-found document,
  carrying the mark, the heading `Page not found`, the line `The page you're looking for
  doesn't exist or has been moved.`, and links back to `/` and to `/resources`. A soft
  `200` for an unknown address, and a redirect to the home route, are both wrong. An
  unknown path under `/api/` answers `404` with code `not_found` in the error shape.
- **The not permitted, removed and failure documents** share that template: `403` titled
  `Not permitted`, saying the address exists but is not available to the visitor and that
  signing in may help; `410` titled `Page removed`, saying the address was deliberately
  removed and suggesting the nearest surviving route by slug similarity; and `500` titled
  `Something failed on our side`, saying the failure is Junction's and not the visitor's,
  carrying a request identifier, and offering retry, home and contact. The `500` document
  depends on nothing: no content back end, search index, font file or script.
- **The legal routes.** `/terms`, `/privacy`, `/security` and `/accessibility` are answered
  as complete documents whose first heading is `Terms of use`, `Privacy`, `Security and
  trust` and `Accessibility statement` respectively. Terms exist because the calculator and
  grader produce estimates that need a disclaimer; privacy because the site captures
  addresses, retains assistant transcripts and processes driver identity in the product;
  security and trust because the buying roles include information technology professionals
  who look for it before a demo; and the accessibility statement because the conformance
  target, assessment date, known exceptions with their alternatives, tested assistive
  technologies and a barrier reporting contact with a response time must be published.
- **The footer link.** Every document the server answers carries, in its own markup, a
  footer link to `/terms`, and the portal's invitation acceptance form links to it too.

**Headers on every response.** Every response, whether a document, an asset or an API
answer, carries `X-Content-Type-Options: nosniff` and a `Strict-Transport-Security` policy
with a positive `max-age`. Console and portal documents also carry a content security policy
that forbids framing. Every console and portal API response carries `Cache-Control:
no-store`.

**The page view log.** Every document request the server answers for a public content route
is recorded with its `route`, its response `status` and the instant it was served, and
`GET /api/page-views` returns them newest first as `[{"route", "status", "viewed_at"}]` to a
member holding the content publisher role and to nobody else; any other principal is refused
with `403` and code `forbidden`. Page views carry no personal identifier.

**Nothing secret in the browser.** No credential, client secret, database address or content
back end token appears in anything the browser downloads.

### Forms, the submission pipeline and consent

Every public form is one of five and they share one validation engine, one submission
pipeline and one consent record: contact with six fields on the contact and home routes; demo
request with five fields on the demo landing route; a gated document with one field and consent
for field guides, the survey and datasheets; a newsletter with one field and consent in the
connection block and listing footers; and result capture with one field and consent in the
calculator and the grader.

**Submission, in order.** Every capture posts to Junction's own origin, never to a third party
from the browser, because vendor field identifiers leak the vendor, a third origin may fall
outside consent, and a vendor outage would become a visitor's failure. The server validates
against the same schema the browser used; applies rate limits per address and per network
origin; screens with an invisible decoy field and a timing score, showing a challenge only on a
bad score; **writes the submission with its consent record before any outbound call**;
acknowledges the visitor without depending on delivery; queues delivery to the customer
relationship system with idempotency on the submission identifier and retries with backoff;
queues the visitor's acknowledgement mail; and reconciles daily, re-queueing any submission with
no confirmed delivery. A lead that reached Junction and not the vendor is recoverable; a lead that
only ever existed as a timed out call is gone.

**The contact endpoint.** `POST /api/forms/contact` takes `{"full_name", "role", "phone",
"email", "company", "help", "company_website", "submission_id"}` where `help` is a non empty list
of the five help options, `phone` is optional, and `company_website` is the decoy field no person
sees. A valid submission answers `201` with `{"id"}` and is stored in the `form_submission` table
with its `email`. A submission whose decoy field is filled is refused with `422` and code
`rejected_submission`. A fourth submission carrying the same `email` inside sixty seconds is refused
with `429` and code `rate_limited`. Neither refusal writes anything. A replay of the same
`submission_id` inside twenty four hours answers `201` with the original `{"id"}` and produces one record
and one outbound delivery.
Across every form, an address at `example.com` or at any of its subdomains is reserved and accepted
without a mail exchanger lookup, and the limit per network origin admits at least sixty submissions a
minute, so a burst from one address meets the per address limit first.

**Consent.** Every capture writes the exact consent text shown, its version, the instant, the route
address, the categories accepted and the mechanism. Withdrawal is available from every mail and by a
request to `support@junction.example.com`, propagates to the customer relationship system in the
background, and is reconciled daily.

**Anti-abuse.** Automated submission meets the decoy field, the timing score, per address and per
origin limits and a challenge only on a bad score. Address enumeration through the newsletter meets an
identical response for a new and an existing address. Shared gated document links meet single use
signed links with a short life. Mail injection through a name field meets strict validation and a mail
path that refuses header content in a body field. Replay meets idempotency on a client generated
submission identifier held for twenty four hours.

**The gated document** opens in place as a panel over the block that offered it, never a route change
or a browser dialogue; focus moves into it and is held there until Escape closes it and returns focus;
delivery is a single use signed link valid for twenty four hours, mailed and also opened in place; once
an address is given, later gates in the session deliver at once; and the consent checkbox is unticked by
default with the full consent sentence as its label. A gated document is never the only way to reach the
information: the offering route carries an ungated summary of at least three substantive points.

**The conversational agent `Ada`** is a first party surface opened from the connection block and a
persistent corner affordance on every content route. Its corpus is the published content estate only,
indexed at publish. Every answer cites the routes it drew on as links, and an answer without a citation is
not shown. Outside its corpus it says so and offers the contact route, and it never speculates about
pricing, availability, a customer's configuration or a rival product. It is labelled automated in its
first message and its affordance. An address is never required; it may be offered once after the third
exchange and refused permanently. Transcripts are kept thirty days for quality, never used to identify a
visitor, and covered by consent. It streams from Junction's origin, loads nothing until the affordance is
used, never shifts layout, and when the model service is down it says so and offers the contact route and
the telephone line rather than an empty conversation. It reads published content and nothing else: it can
never reach the console, operational data or any tenant record.

**Consent and analytics.** A consent surface on first visit offers accept, reject and a per category
choice; no analytics, agent or third party embed loads before a decision; a rejection holds for the session
and is stored for a year.

### The savings calculator

The calculator is the highest intent surface on the site and the only place a visitor supplies their own
operational figures, so a badly specified computation becomes a commercial claim. It lives on its own route,
embedded in full on the home route, and is offered from the connection block.

**Inputs, defaults, ranges and steps:**

| Label | Control | Default | Range | Step |
|---|---|---|---|---|
| `Number of gates` | integer field | `2` | `1` to `40` | `1` |
| `Shifts per day` | integer field | `3` | `1` to `3` | `1` |
| `Operating days per week` | integer field | `6` | `1` to `7` | `1` |
| `Spotters per shift` | integer field | `3` | `0` to `40` | `1` |
| `Check-ins per day` | integer field | `45` | `1` to `2000` | `1` |
| `Blended hourly wage` | currency field, prefixed | `28` | `1` to `200` | `0.5` |
| `How significant are your annual detention and demurrage costs?` | slider | `5` | `1` to `10` | `1` |

The slider carries `1 - LOW` at its start, `10 - HIGH` at its end and a middle label that moves with the handle
and states the current value, such as `5 - MEDIUM`, which is also its accessible value text.

**The computation** runs entirely in the browser on every input with no network call, in integer minor units
with no binary floating point value for money, rounded once at presentation to whole major units.

- `labourSaving` is check-ins per day, times operating days per week, times `52`, times the minutes saved per
  check-in, divided by `60`, times the blended wage. **Minutes saved per check-in is `39`**, measured exactly and
  consistent with the published claim of up to eighty five per cent faster gate processing against a manual
  check-in of about three quarters of an hour.
- `spotterSaving` is spotters per shift, times shifts per day, times operating days per week, times `52`, times
  the hours saved per spotter shift, times the blended wage, plus the spotter units released times the annual unit
  cost, where units released is spotters per shift divided by three, rounded down.
- `demurrageSaving` is the demurrage exposure, proportional to the significance and to the number of gates, times
  a recovery rate.
- The total is the sum of the three, and the estimated savings rate is the total over the visitor's baseline annual
  yard cost, the sum of gate, spotter and demurrage cost before any saving, shown as a whole percentage.

**The measured acceptance vector.** With every input at its default the calculator shows exactly: `Labor Savings`
`255,528`, `Spotter Savings` `193,248`, `Detention & Demurrage Savings` `192,850`, a total of `641,626`, and
`Est. Savings` of `23%`. The hours saved per spotter shift, the annual unit cost, the demurrage exposure per point
of significance per gate, the recovery rate and the baseline cost are yours to set within the shapes above, held in
one configuration object editable without a code change, so long as the defaults reproduce that vector exactly.
Every coefficient you use is stated in the disclosure.

**The result panel** is a near-black cool neutral panel with the notch cut into its top edge on both sides and the
lime results glow behind it: the headline `With Junction your yard saves` with its second half muted; the total set
large as a digit stack with the currency mark separated by a space; `Est. Savings:` with a muted label and bright
value; `Estimated annual savings by category:`; and three rows, `Labor Savings (Gate, Traffic, Dispatch, Yard
Check):`, `Spotter Savings (Drivers and Unit Leases):` and `Detention & Demurrage Savings:`, each value right aligned
as a digit stack. The parentheticals are the model's scope: labour covers gate, traffic, dispatch and yard check
roles; spotter covers drivers and unit leases; the third covers detention and demurrage. Every value animates through
its digit stack on change, and a new change interrupts rather than queues.

**The capture** sits inside the result panel as a nested translucent panel headed `Want to know more?` with the body
`Enter your work email below if you would like to run a custom ROI analysis with one of our team of yard experts.`, the
label `Work Email` and the action `SUBMIT`. It appears only once a result exists, which with the defaults is at once;
it is slightly faded until an input changes and fully opaque after, because the visitor who typed their own figures is
the one worth asking. Its submission carries the whole input vector, the computed result and the coefficient version.

**The disclosure** beneath the panel is collapsed by default, reachable by keyboard, never hidden from assistive
technology, in the document rather than fetched, and states every coefficient in plain sentences, that the figures are
an estimate, and that they are not a quotation or a contractual commitment.

**Calculator states.** A cleared field is invalid, the panel holds its last valid figures visibly dimmed and names the
invalid field beneath it. An out of range value is clamped on blur, not on input, and the clamp is announced. A non
numeric character is refused at input. Zero spotters show the spotter category as zero rather than hiding it. Every
input at its minimum gives a small total that is never negative. A total past nine figures widens the digit stack with
no truncation, exponent or abbreviation. Presentation follows the visitor's locale and the model does not. The home route
instance and the route instance share no state, so moving between them starts from the defaults.

### The security grader

`Yard Security Grader | Junction`, headed `How secure is your yard, layer by layer?`, introduced with `This grader is
fifteen quick questions that will assess your operation across five layers of yard security. The result is a single
security score and a layer-by-layer breakdown.`, a legend `What we grade`, and the action `Grade my yard`. It is the
security pillar's conversion path.

**The instrument.** Fifteen questions, three per layer, each a single choice of four ordered options scoring `0`, `1`,
`2` and `3`, ordered within a layer from the weakest practice to the strongest and worded so the honest answer is easy.

| Identifier | Layer | Asks about |
|---|---|---|
| `L00` | Digital Check-in | whether arrival is recorded by a system or a person, contemporaneously, searchably |
| `L01` | Carrier Risk Assessment | whether the haulier is checked against an authorisation, before arrival, enforceably at the fence |
| `L02` | ID Verification | whether the driver's identity is captured, verified against the booking, and a mismatch stops the visit |
| `L03` | Load Verification | whether the load is recorded at the dock, the seal verified, and custody unbroken to the gate |
| `L04` | Perimeter Cameras | whether the fence line is covered, continuously, with footage retrievable by time and place |

**Scoring.** A layer's percentage is its three answers over nine, rounded to the nearest whole number. The overall score
is all fifteen over forty five, out of one hundred, rounded to the nearest whole number. The score maps to a band that sets
the ring's fill, the band name and the verdict: `0` to `39` is `Open yard` in the critical red; `40` to `59` is `Partially
covered` in the caution amber; `60` to `79` is `Verified yard` in the ok green; `80` to `100` is `Sealed yard` in the lime. A
layer's status uses the same thresholds with three words: `Exposed` below forty, `Partial` from forty to seventy nine,
`Covered` at eighty and above. Status is never carried by colour alone.

**After the result**, three actions in order: get the full report, which is the result capture offering a written report
per layer with the recommended remediation and the module that delivers it; see how this is fixed, which navigates to the
route addressing the visitor's weakest layer, chosen by the lowest layer percentage with ties broken by layer order, where
`L00` leads to `/modules/gate-management`, `L01` and `L02` to `/modules/haulier-risk-assessment-and-driver-id`, `L03` to
`/modules/load-verification` and `L04` to `/modules/yard-visibility`, and a full score leads to `/yard-security`; and retake.

**Scoring integrity.** The scoring is not secret and runs in the browser for instant feedback, but the server never trusts
a score it did not compute. `POST /api/grader/reports` takes `{"answers", "score", "email", "consent"}` where `answers` is
fifteen integers in layer order, and answers `202` with `{"score", "band", "layers": [{"id", "percent", "status"}],
"fix_route"}` computed from the answers alone, ignoring any `score` supplied. The report is generated server side from the
answer vector from a versioned template whose version is recorded, contains the score, band, the five layer breakdowns, the
chosen options restated as current practice and one remediation per layer, and is delivered by a single use signed link. A
shared result address encodes only the answer vector and carries no company name unless one was given to the report.

**The interaction.** One question at a time, full panel, with a progress indicator naming the layer identifier and the
question's place in the instrument. Choosing an option records it and advances after a short pause with no confirm; back
returns to the previous question with its answer still chosen; number keys one to four choose, arrows move, Enter confirms
and Backspace goes back; the fifteenth answer replaces the panel with the result in place; retake resets to question one and
clears stored answers; each question is a history entry so the browser's back control works; and answers, never the result,
persist in the browser for seven days so an interrupted visitor resumes. No address is needed to finish.

**The result** is a neutral dark panel with the notch cut into its top: `Your result` muted; the score ring with the numeral
large and `/ 100` beneath; the band name in its colour; a one sentence verdict; two muted sentences of explanation; and five
layer rows, each a small badge carrying the layer identifier in the layer's own hue (a neutral grey, an amber, a blue, a violet
and a green, identifying the layer, never its status), the layer name, the status word and percentage right aligned, and a
progress track. The reference's own result screen at a score of thirty read `Open yard`, `The gate is verifying almost
nothing.` and `Right now the yard runs on trust. Nothing reliably confirms who or what enters or leaves, and no record would
hold up in a claim or an audit.`, with layer rows `L00` `Exposed 17%`, `L01` `Exposed 33%`, `L02` `Exposed 33%`, `L03`
`Partial 50%` and `L04` `Exposed 17%`; that screen is carried as copy for its band, and the scoring rule above governs every
number.

**The survey instrument** for the 2026 State of the Yard Survey shares the segmented result, layer rows and banded score, with
respondent categories as segments, two marks on each track for the visitor and the published median, and no verdict sentence.
The published distribution is versioned content and a comparison never renders against a missing one.

**Grader states.** Answers older than seven days have expired and the instrument restarts with a message. A failed report
keeps the result on screen, states the failure and re-offers. A full score leads to the security pillar. Questions edited
between visit and return discard stored answers. Under assistive technology each question is a labelled radio group, progress
is announced, and the result receives focus and is announced in full.

### The content back end, resources and search

**The content back end** is a table backed store with versioned schemas for the pillar, module, market, problem, case study
and resource models; a draft state reachable only by a signed preview token, never an unlisted public address; a publish that
is an event invalidating exactly the affected routes; references validated at publish so the cross linking rules hold; a locale
dimension on every field with a fallback chain; a media library with derived renditions; and author, editor and publisher roles.
It is never called from a visitor's browser on a content route.

**Resources** are six categories with their own listings and one hub: blogs, case studies, videos, webinars, press releases, and
podcasts and articles, plus `announcement`, an alias of press releases in the hub's Latest News band. Category is a controlled
vocabulary and renders on cards in lower case monospace. **The hub** at `/resources` is titled `Resources` with the heading
`Viewpoints for a smarter yard`: one carousel per category of its six most recent items, each headed with a link to its listing,
the first band `Latest News` drawing from announcements, and the site search at its head. **A listing** is titled `All <Category>
| Junction` with a heading, a filter row and a grid of cards: category chips on the hub only; a multiple select topic filter from
a controlled vocabulary reflected in the address so a filtered listing is linkable; newest first by default and relevance when a
search term is present; and cursor paging that appends on an explicit action, never on scroll, so the footer stays reachable. The
first page of cards is in the document. **A detail** lives at `/all-resources/{slug}` across all categories, so an item keeps its
address if re-categorised: a breadcrumb whose separator and current item are muted, the current item not a link; an eyebrow with the
category; a character split title; a byline and date; a hero media well; the body; and three related items from the same topic. The
body supports exactly paragraphs, headings of levels two and three, ordered and unordered lists, block quotes, captioned images,
video embeds, tables, callouts and references to a case study, a module route or a gated document; an unknown block is dropped with
a build warning. Every embed waits for consent behind a first party placeholder carrying the embed's title.

**Search** is one input with an attached action forming one pill, scoped to resources and the pillar, module, market and problem
routes; a static index for the first two characters and a server query beyond; results after a quarter of a second of quiet,
grouped by route family with the matched term marked; the six most recent resources for an empty query; for no results, a message
naming the query, the three most read resources and a contact link, never a bare empty state; up and down through results, Enter to
open, Escape to close and return focus; and a submitted search navigating to a results route carrying the query so it can be shared.

**Resource states.** An empty listing renders its heading, a message and the three most recent items from the hub. An article
referencing a deleted case study omits the reference block and raises a build error. A missing hero renders the generated cover. A
failed search index turns the input into a submit to the results route with type-ahead disabled. A failed append keeps loaded cards
and re-offers with a message.

**Canonical, sitemap and robots.** Every route declares a canonical address and duplicate addresses declare the preferred one; the
sitemap is generated from the route manifest split by family with last modified dates and excludes the console and portal entirely;
robots disallows the console and portal and their documents also carry a no-index directive, because a disallow does not stop a linked
address being indexed; content routes declare `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1`; and every
content route emits a social title, description, type and image, generated where the content back end has none.

**The technical index** at `/technical-index`, titled `Junction` with the eyebrow and heading `Technical Index`, lists every content route
grouped by family with its title, last modified date and canonical address, generated from the route manifest at build, never authored; a
route missing from it is a build failure.

**Redirects** are content, editable without a release, applied before the route resolver: a trailing slash redirects permanently to the
unslashed form; an upper case segment to lower case; a retired route with a successor to the successor; a retired route with no successor
answers the removed document, never a redirect to home; a campaign address redirects to its canonical route keeping query parameters; and a
redirect loop is detected at publish and blocks it.

### The HTTP contract

Every route below lives under `/api` on the app's own origin and speaks JSON. Errors use
one shape everywhere: `{"code", "message", "request_id", "fields"}`, where `code` is a
stable machine readable value, `message` is for a person, `request_id` identifies the
request, and `fields` is a per-field map present only for a validation failure. No raw
exception text or provider message ever reaches a person.

- A console call presents `Authorization: Bearer <access_token>` from
  `POST /api/auth/login`; a portal call presents the token from
  `POST /api/portal/auth/login`.
- A call that needs a principal and has none answers `401` with code `unauthenticated`.
- A resource that does not exist, that belongs to another organisation, or that sits at a
  site the caller holds no grant on, answers `404` with code `not_found`, with the same
  message in every case.
- A principal whose grants at the resource's site do not permit the call answers `403`
  with code `forbidden`, naming the missing permission in the message.
- A call into a module the site is not entitled to answers `403` with code
  `module_not_entitled`.
- A validation failure answers `422` with code `validation_failed` and `fields`, unless a
  more specific code is named below.
- Site scoped instants carry the site's offset; other instants carry `Z`. Durations are
  whole seconds.
- A collection answers a top level JSON array. An operational collection accepts `limit`
  from `1` to `100` and `cursor`, and returns the next cursor in the `X-Next-Cursor`
  response header, absent on the last page.
- Every write accepts an `Idempotency-Key` header as described under the HTTP contract as a
  product.
- Asset types are `dry_van`, `reefer`, `flatbed`, `container`, `chassis` and `tractor`.
  Directions are `inbound`, `outbound` and `live_load`. Module identifiers are
  `gate_management`, `haulier_risk`, `dispatch`, `yard_visibility`, `load_verification` and
  `haulier_appointments`. Role identifiers are `organisation_administrator`,
  `security_administrator`, `network_manager`, `site_manager`, `dispatcher`,
  `gate_operator`, `dock_operator`, `spotter`, `analyst` and `content_publisher`.

**Sessions**

| Call | Body | Success |
|---|---|---|
| `POST /api/auth/login` | `{"email", "password"}` | `200` `{"access_token", "expires_at"}`; a wrong pair is `401` `invalid_credentials` |
| `POST /api/auth/logout` | none | `204` |
| `GET /api/auth/me` | none | `200` `{"member_id", "email", "name", "organisation", "grants": [{"id", "role", "site_id", "expires_at"}]}` |
| `POST /api/portal/auth/login` | `{"email", "password"}` | `200` `{"access_token", "expires_at", "principal_kind"}`; a wrong pair is `401` `invalid_credentials` |

Signup is closed in both spaces: `POST /api/auth/signup` and `POST /api/portal/auth/signup` answer `404` with
code `not_found`, and no call creates an account for its caller.

**Sites, members and grants**

| Call | Body or query | Success |
|---|---|---|
| `GET /api/sites` | none | an array of `{"id", "code", "name", "time_zone", "modules"}` for every site the member holds a grant on; an organisation administrator sees every site of the organisation |
| `GET /api/sites/{site_id}` | none | `200` `{"id", "code", "name", "time_zone", "modules", "slot_minutes", "position_staleness_seconds"}` |
| `GET /api/members` | none | an organisation administrator receives an array of `{"member_id", "email", "name", "grants"}` |
| `POST /api/members/{member_id}/grants` | `{"role", "site_id", "reason", "expires_at"}`, `site_id` absent for an organisation scope, `expires_at` optional only for a base operational role | `201` `{"id", "role", "site_id", "expires_at"}`; an elevated role without `expires_at` is `422` `expiry_required` |
| `DELETE /api/grants/{grant_id}` | none | `204`, effective on the grantee's very next request |

**Assets, positions, moves, tasks and shifts**

| Call | Body or query | Success |
|---|---|---|
| `POST /api/sites/{site_id}/assets` | `{"asset_number", "asset_type", "haulier_registration"}`, the last optional | `201` `{"id", "asset_number", "asset_type"}`; an asset number already held in the organisation is `409` `asset_exists` |
| `GET /api/sites/{site_id}/assets/{asset_number}` | none | `200` `{"asset_number", "asset_type", "spot", "observed_at", "staleness", "open_move_id"}` |
| `POST /api/sites/{site_id}/positions` | `{"asset_number", "spot"}` | `201` `{"asset_number", "spot", "observed_at", "staleness"}`; the observation also verifies a `placed` move whose destination is that spot |
| `POST /api/sites/{site_id}/moves` | `{"asset_number", "to_spot", "reason"}` | `201` `{"id", "state", "asset_number", "from_spot", "to_spot", "reason", "assignee_email", "version"}` with state `open`; refusals as in the move validation table |
| `GET /api/moves/{move_id}` | none | `200`, the move in the shape above |
| `POST /api/moves/{move_id}/transitions` | `{"to", "version", "assignee_email", "reason"}`, `assignee_email` required to reach `assigned`, `reason` required for `rejected`, `failed` and a manual `completed` | `200`, the move; `409` `illegal_transition` or `409` `version_conflict` with `{"current_version"}` |
| `POST /api/moves/{move_id}/cancel` | `{"reason"}` | `200`, the move with state `cancelled` and its destination freed |
| `GET /api/sites/{site_id}/tasks` | query `kind` | an array of `{"id", "kind", "asset_number", "state"}`; a stale move attempt raises kind `position_confirmation` |
| `POST /api/sites/{site_id}/shifts` | `{"member_email", "starts_local", "ends_local"}` | `201` `{"id", "member_email", "starts_at", "ends_at", "duration_seconds"}` |

A move reaches `assigned` only with a spotter who holds a shift at the move's site covering the
moment of assignment; otherwise the transition is refused with `409` and code
`spotter_not_on_shift`. A dispatcher, site manager or organisation administrator for the move's site
creates and cancels moves and may record any transition on a move, a manual `completed` included; a spotter may record a
transition only on a move assigned to that spotter. Every other principal at the site, another
spotter included, is refused with `403` and code `forbidden`.

**Visits and approvals**

| Call | Body | Success |
|---|---|---|
| `POST /api/sites/{site_id}/visits` | `{"lane", "direction", "plate", "asset_number", "haulier_registration"}` | `201` `{"id", "state", "plate", "haulier_registration", "checks": [{"kind", "result"}]}` where `kind` is one of `appointment`, `haulier_authorisation`, `driver_identity`, `watchlist`, `asset_expectation`, `document`, `capacity` and `dimension_hazard`, and `result` is `pass`, `fail` or `not_applicable` |
| `GET /api/visits/{visit_id}` | none | `200`, the visit in the shape above |
| `POST /api/visits/{visit_id}/release-requests` | `{"reason"}` | `201` `{"id", "state", "action", "subject_id", "requested_by"}` with state `pending`, action `gate.release_override` and `subject_id` the visit |
| `GET /api/approvals/{approval_id}` | none | `200` `{"id", "state", "action", "subject_id", "requested_by", "decisions": [{"decided_by", "decision", "reason"}]}` |
| `POST /api/approvals/{approval_id}/decisions` | `{"decision", "reason"}` | `200`, the approval; an approved `gate.release_override` leaves its visit `admitted` |

**Appointments**

| Call | Body | Success |
|---|---|---|
| `POST /api/sites/{site_id}/appointments` | `{"haulier_registration", "direction", "door", "asset_type", "starts_local", "ends_local", "load_reference", "customer_of_tenant"}`, the last two optional | `201` `{"id", "reference", "state", "door", "starts_at", "ends_at", "duration_seconds", "version"}` with state `confirmed`; refusals as in the booking constraint table |
| `GET /api/appointments/{appointment_id}` | none | `200`, the appointment in the shape above, for a portal booking as much as a console one |
| `PATCH /api/appointments/{appointment_id}` | `{"version", "reason"}` with any of `"door"`, `"starts_local"`, `"ends_local"` | `200`, the appointment with its version advanced; `409` `version_conflict` with `{"current_version"}` |
| `POST /api/appointments/{appointment_id}/cancel` | `{"reason"}` | `200`, state `cancelled` |

**Custody**

| Call | Body | Success |
|---|---|---|
| `POST /api/sites/{site_id}/custody-events` | `{"asset_number", "kind", "seal_number", "note"}`, the last two optional | `201` `{"id", "asset_number", "sequence", "kind", "seal_number", "prior_hash", "hash", "corrects"}` |
| `POST /api/custody-events/{event_id}/corrections` | `{"reason", "seal_number"}` | `201`, a new event of kind `corrected` with `corrects` naming the original |
| `GET /api/sites/{site_id}/assets/{asset_number}/custody` | none | `200` `{"events": [event, in sequence order], "head_hash"}` |
| `POST /api/sites/{site_id}/assets/{asset_number}/custody/verify` | none | `200` `{"valid", "broken_at"}` |

**Audit and page views**

| Call | Query | Success |
|---|---|---|
| `GET /api/audit` | `action`, `outcome`, both optional | an array of `{"sequence", "action", "outcome", "actor_email", "resource_id", "occurred_at"}`, newest first; a refused approval decision is recorded with action `approval.decide` and outcome `denied` |
| `GET /api/page-views` | none | an array of `{"route", "status", "viewed_at"}`, newest first, for a content publisher |

**The portal**

| Call | Body or query | Success |
|---|---|---|
| `GET /api/portal/sites` | none | an array of `{"id", "name", "time_zone"}` |
| `GET /api/portal/sites/{site_id}/availability` | query `date`, `direction`, `asset_type` | an array of `{"starts_at", "ends_at"}` and nothing else |
| `POST /api/portal/sites/{site_id}/bookings` | `{"direction", "asset_type", "starts_local", "ends_local", "load_reference", "driver": {"name", "telephone", "language"}}`, `load_reference` optional | `201` `{"id", "reference", "state", "direction", "asset_type", "starts_at", "ends_at", "visit_link"}` where `visit_link` is `/v/{token}`; `409` `no_capacity` with alternatives |
| `GET /api/portal/bookings/{booking_id}` | none | `200`, the booking in the shape above |
| `POST /api/portal/bookings/{booking_id}/cancel` | `{"reason"}` | `200`, state `cancelled` |
| `GET /api/visit-views/{token}` | none, no session | `200` `{"window": {"starts_at", "ends_at"}, "site_address", "arrival_instructions", "door", "contact_number"}`; `410` `visit_link_revoked` once its booking is cancelled |
| `GET /api/portal/customer/report` | query `site_id`, `period` | `200` `{"period", "loads", "median_dwell_seconds", "suppressed"}` |
| `GET /api/portal/customer/loads` | query `site_id`, `period` | an array of `{"reference", "arrived_at", "departed_at"}`, the caller's own loads only |

**The public surface**

| Call | Body | Success |
|---|---|---|
| `POST /api/forms/contact` | `{"full_name", "role", "phone", "email", "company", "help", "company_website", "submission_id"}` | `201` `{"id"}`; `422` `rejected_submission`; `429` `rate_limited` |
| `POST /api/grader/reports` | `{"answers", "score", "email", "consent"}` | `202` `{"score", "band", "layers": [{"id", "percent", "status"}], "fix_route"}` |
| `GET /api/health` | none | `200` |

### Seeded fixtures

Seeding runs on first start and is idempotent: restarting must not create a second copy of
any seeded row. Every seeded account uses the password `deku-demo-pw-2026`. Every member below
also exists in the Keycloak realm `junction` with the same address and password; portal
principals exist only in Junction. Seeded accounts hold no second factor enrolment: for them the
password sign in completes the session, administrative and security roles included, and every call
in the HTTP contract, grant changes among them, proceeds on that session with no second factor step.

**Organisations.** **Tidewater Logistics**, slug `tidewater`, a third party logistics operator
pinned to region `us-central`, running two sites. **Northfield Distribution**, slug `northfield`,
pinned to `us-east`, running one site. **Junction Systems**, slug `junction`, the vendor's own
organisation, which holds the content publisher. No row of one organisation is ever visible to
another, and a member of one who names a resource of another receives exactly the response a
resource that does not exist produces.

**Sites.**

| Code | Name | Organisation | Time zone | Modules |
|---|---|---|---|---|
| `DAL1` | Dallas Crossdock | Tidewater | `America/Chicago` | all six |
| `RNO2` | Reno Distribution | Tidewater | `America/Los_Angeles` | `gate_management`, `yard_visibility`, `dispatch` |
| `ATL1` | Atlanta Yard | Northfield | `America/New_York` | all six |

Dallas Crossdock runs a slot length of `30` minutes, operating hours `06:00` to `22:00` every
day, a minimum lead time of `120` minutes, a booking horizon of `60` days, a position staleness
threshold of `1800` seconds, an arrival grace of `15` minutes, a gate throughput ceiling of `8`
arrivals per slot, a concurrent visit ceiling of `40`, labour staffed across all operating hours
for every load type, no approval required for portal bookings, and an unbooked arrival policy of
permit with an exception. Automatic move assignment is off at every seeded site. Its address is `4100 Crossdock Parkway, Dallas, TX 75212` and its
contact number `+1 (555) 010-2210`.

**Dallas doors.** `D01`, `D02`, `D03` and `D04` accept `dry_van`; `D05` accepts `reefer` only;
`D06` accepts `dry_van` and is out of service. Atlanta Yard has doors `D01` and `D02`, both
accepting `dry_van`, with the same hours and rules as Dallas. Reno Distribution has no doors.

**Dallas lanes and spots.** Lanes `G1-IN`, `G1-OUT` and `G2-IN`. Spots `A-01` to `A-12` accept
`dry_van`; spots `R-01` to `R-04` accept `reefer`; spots `S-01` to `S-06` accept every asset type.

**Members**, all in Keycloak:

| Address | Organisation | Grants | Name |
|---|---|---|---|
| `orgadmin@tidewater.example.com` | Tidewater | `organisation_administrator` for the organisation | Maya Okafor |
| `manager.dal@tidewater.example.com` | Tidewater | `site_manager` at `DAL1` | Luis Ferreira |
| `manager2.dal@tidewater.example.com` | Tidewater | `site_manager` at `DAL1` | Priya Raman |
| `dispatch.dal@tidewater.example.com` | Tidewater | `dispatcher` at `DAL1` | Tomas Lindqvist |
| `gate.dal@tidewater.example.com` | Tidewater | `gate_operator` at `DAL1` | Grace Achterberg |
| `dock.dal@tidewater.example.com` | Tidewater | `dock_operator` at `DAL1` | Samir Haddad |
| `spotter.dal@tidewater.example.com` | Tidewater | `spotter` at `DAL1` | Kofi Mensah |
| `spotter2.dal@tidewater.example.com` | Tidewater | `spotter` at `DAL1` | Efua Boateng |
| `dual@tidewater.example.com` | Tidewater | `site_manager` at `RNO2` and `gate_operator` at `DAL1` | Jonah Whitcombe |
| `security@tidewater.example.com` | Tidewater | `security_administrator` for the organisation | Ines Castell |
| `analyst@tidewater.example.com` | Tidewater | `analyst` for the organisation | Wren Adeyemi |
| `manager.atl@northfield.example.com` | Northfield | `site_manager` at `ATL1` | Hana Moreau |
| `publisher@junction.example.com` | Junction Systems | `content_publisher` for the organisation | Arlo Benedetti |

Every elevated seeded grant expires at `2027-12-31T23:59:59Z`.

**Hauliers and their users.**

| Haulier | Registration | Authorisation | Booking contact | Portal users |
|---|---|---|---|---|
| Redline Haulage | `MC-100245` | `DAL1`, inbound and outbound, until `2027-12-31` | `bookings@redline.example.com` | `bookings@redline.example.com`, `ops@redline.example.com` |
| Bluecrest Freight | `MC-200318` | `DAL1`, inbound and outbound, until `2027-12-31` | `desk@bluecrest.example.com` | `desk@bluecrest.example.com` |
| Oakridge Carriers | `MC-300771` | `ATL1` only | `team@oakridge.example.com` | `team@oakridge.example.com` |
| Halvard Transport | `MC-400932` | `DAL1`, suspended | `dispatch@halvard.example.com` | `dispatch@halvard.example.com` |

**Customers of Tidewater.** **Everwear** has the customer user `reports@everwear.example.com` and six
loads at `DAL1` in September 2026, references `EW-0901` to `EW-0906`. **Praxis** has the customer user
`reports@praxis.example.com` and three loads at `DAL1` in September 2026, references `PX-0901` to
`PX-0903`. Each load arrived and departed within September 2026.

**Assets at Dallas**, each with a last known position observed at `2026-09-01T08:00:00-05:00`:

| Asset | Type | Haulier | Spot |
|---|---|---|---|
| `TRL-4471` | `dry_van` | Redline Haulage | `A-03` |
| `TRL-5820` | `dry_van` | Bluecrest Freight | `A-07` |
| `TRL-6093` | `dry_van` | Redline Haulage | `S-02` |
| `RFR-2201` | `reefer` | Bluecrest Freight | `R-01` |

**Watchlist at Dallas.** An active entry for the plate `TX-9KR-221`, reason `cargo_theft_report`, owned
by `security@tidewater.example.com`, expiring `2099-12-31`; and an entry for the plate `TX-4LM-870`,
reason `cargo_theft_report`, that expired at `2026-01-31T23:59:59Z`.

**A held visit awaiting approval.** At `DAL1`, lane `G1-IN`, an inbound visit of the plate `OK-77-TRK`
for Oakridge Carriers is `held` on its haulier authorisation, and a `gate.release_override` request for it
is `pending`, raised by `gate.dal@tidewater.example.com` with the reason `Driver holds paperwork for a
retrospective booking`.

## Data model

Sixty eight tables are named below, all in PostgreSQL at `DATABASE_URL`. All timestamps are UTC instants stored
with the zone they originated in; site local times are derived for presentation. **Every seeded
account uses the password `deku-demo-pw-2026`.** It is fixture data, not a secret. Hash it as
normal; the exact literal must work at login, and it must be written into `/app/USER_README.md`
beside each seeded account so anyone opening the app can sign in.

### Conventions

| Convention | Rule |
|---|---|
| identifiers | opaque, non-sequential, prefixed by type (`org_`, `site_`, `mbr_`, `grt_`, `hau_`, `ast_`, `mov_`, `apt_`, `vis_`, `apr_`, `cus_`, `evt_`) and safe in an address; a sequential identifier in the portal is an enumeration surface |
| tenancy | every tenant table carries `organisation_id` and every site scoped table also carries `site_id`, and rows are only ever readable within the principal's own organisation and granted sites |
| time | every instant stored with its originating zone; every duration derived, never stored, unless it is a measured fact |
| money | integer minor units with an explicit currency, never a floating point value |
| soft delete | only where a record can legitimately be withdrawn; never on a custody, audit, observation or decision record |
| versioning | every mutable record carries a monotonic `version`, which every update names |
| provenance | every value that came from an observation carries the observation reference and its confidence |
| history | every record a person can change has a history of actor, instant, before and after values and reason where required |

### Tenancy

- **organisation** - identifier, name, slug unique across the table, residency region, retention
  policy, encryption key reference, plan, federation configuration.
- **region** - an optional grouping of an organisation's sites for regional roles.
- **site** - organisation, optional region, code unique within the organisation, name, time zone,
  unit preference, operating hours, slot minutes, lead time, horizon, staleness threshold, arrival
  grace, capacity ceilings, unbooked arrival policy, whether portal bookings need approval, address,
  contact number, plan version, policy configuration.
- **entitlement** - organisation or site, module, state, effective dates.
- **customer_of_tenant** - a customer of an organisation, used for attribution and for federated
  reporting, with its portal users.

### Yard geometry

- **site_plan** - site, version, state; versioned, so every operational record referencing a spot,
  door or lane stores the plan version current at the time, and a changed polygon never rewrites where
  a trailer was three months ago in an evidence pack.
- **zone**, **spot**, **dock_door**, **gate**, **lane**, **path** and **camera** - the fields of the
  site plan table in Technical requirements. A spot identifier is unique per site plan version.

### Assets and freight

- **asset** - organisation, identifier, asset number unique per organisation and not globally,
  because two customers may hold the same trailer number, type, owning haulier, dimensions,
  equipment, hazard class, condition state.
- **asset_position** - the current position: asset, spot or zone, coordinates, bearing, source
  observation, confidence, observed instant. Staleness is computed against the site threshold when
  read, never stored.
- **asset_position_history** - a time series partitioned by time and retained by age.
- **load** - reference, direction, `customer_of_tenant_id`, goods description, temperature regime,
  hazard class, expected count, arrival and departure instants. `customer_of_tenant_id` is nullable for
  an organisation that owns its own freight and required per site configuration for one that does not.
- **seal** - number, applied instant and member, image reference, verified instant and member, state.
- **manifest** - the declared contents, its source and its comparison result.

### People and organisations outside the tenant

- **haulier** - a global company record keyed on its verified registration.
- **haulier_site_authorisation** - haulier, site, directions, asset classes, from, until, state of
  `authorised` or `suspended`, owner, review date, booking contact.
- **portal_principal** - kind of `haulier_user` or `customer_user`, the haulier or customer of the tenant
  it belongs to, email unique without regard to case, password hash, invitation, second factor state.
- **driver** - name, telephone, language, credential classes and expiries, owned by a haulier.
- **driver_identity_capture** - the sensitive record: its own table, its own encryption key, its own
  permission, its own retention, referenced by a visit and never embedded in it, and never joined by any
  exportable read, because reaching it needs a permission no export holds.

### Operations

- **visit** - site, lane, direction, plate, asset, haulier, state with a history table, never derived.
- **visit_capture** - one row per capture: kind, value, confidence, media reference, corrected value,
  corrector.
- **visit_check** - one row per check: kind, result, rule version, inputs digest.
- **appointment** - site, haulier, direction, door, asset type, asset number, window start and end,
  load, driver, equipment, state, source, reference, constraint evaluation, version, with an amendment
  history. **At most one confirmed appointment holds a door for any overlapping moment, however many
  writers arrive together.** A visit binds at most one appointment and an appointment binds at most
  one visit.
- **move** - site, asset, from, to, reason, priority, due, assignee, state with a state history,
  origin, constraints, version. **At most one open move exists per asset, and at most one open move
  holds a destination, however many writers arrive together.**
- **assignment_decision** - the move, every candidate considered with its cost by term, the chosen
  assignee and whether it was overridden, kept as long as the move.
- **shift** - member, site, start, end, breaks, vehicle.
- **task** - site, kind, subject, state; a `position_confirmation` task names its asset.
- **exception** - kind, severity, subject, raising workflow instance, state, outcome, actor, deferrals.
- **security_event** - kind, observation, media, rule version, severity, confidence, state.
- **incident_case** - a grouping of security events with a narrative and an owner.
- **watchlist_entry** - scope, subject kind and value, reason, justification, owner, expiry, approval
  reference, review record.
- **discrepancy** and **claim** - as the dock and custody section describes.

### Evidence

- **observation** - the atomic fact: kind, value, alternatives, confidence, source, instant with skew,
  spatial reference, media reference, model version. Never overwritten.
- **custody_event** - `id`, holding the identifier the HTTP contract returns for the event, `organisation_id`, `site_id`, `asset_number`, `sequence`, `kind`,
  `seal_number`, `note`, `corrects`, `actor`, `source`, `occurred_at`, `prior_hash`, `hash`. The prior
  event reference is unique within a chain, so a chain cannot fork.
- **media_object** - reference, class, retention class, encryption key reference, holds, deletion state.
- **evidence_pack** - requester, reason, filter, chain head hash, delivery record.
- **audit_event** - `id`, `organisation_id`, `sequence`, `action`, `outcome`, `actor_id`, `actor_email`,
  `resource_type`, `resource_id`, `occurred_at`, `request_id`, `reason`, `policy_version`, `prior_hash`,
  `hash`, chained per organisation.
- **legal_hold** - subject, owner, reason, review date, released by.

`custody_event` and `audit_event` share one construction and one verification routine, and neither can be
changed or have a row removed by any connection the application holds.

### Identity and policy

- **member** - organisation, email, name, the provider's immutable subject, directory reference, status.
- **directory_group** - a directory group mapped to roles at a scope.
- **role** - a named set of permissions from the vocabulary.
- **access_grant** - principal, role, scope kind, site, granted by, reason, effective from, expires at. Expires at
  is required for every role above the four base operational roles. A directory derived grant is marked so.
- **delegation** - approval authority delegated for a bounded period.
- **session** - principal, principal kind, issued at, last seen at, absolute expiry, revoked at, revoked
  reason, device, address range. A session never stores a grant.
- **machine_credential** - purpose, scope, owner, secret hash, created, rotated, expires, revoked.
- **policy_version** - the policy set as versioned data.

### Workflow, integration and the public estate

- **workflow_definition** and **workflow_definition_version**, the entities `workflowDefinition` and
  `workflowDefinitionVersion`.
- **workflow_instance** and **workflow_step_event**, one row per step transition.
- **approval_request** (`approvalRequest`) - organisation, site, action, subject, requester, required approver set, state,
  deadline, created at.
- **approval_decision** (`approvalDecision`) - request, approver, decision, reason, decided at, delegation.
- **connector**, **exchange** with its idempotency key, attempts, state and last error,
  **webhook_endpoint** (`webhookEndpoint`), **webhook_delivery** (`webhookDelivery`) and **reconciliation_run**.
- **notification_delivery** - subject, kind, triggering transition, channel, recipient, provider response,
  state; one row per subject, kind, transition and recipient.
- **idempotency_record** - principal, key, request fingerprint, stored response, created at, kept twenty
  four hours.
- **form_submission** - form kind, `email`, fields, consent record, submission identifier, delivery state.
- **page_view** - route, status, viewed at.
- **content_item** - model, locale, version, state, references.

### Integrity rules

- No cascading delete anywhere in the operational model: a parent referenced by a child cannot be deleted,
  and an organisation's removal is the governed process of the compliance section.
- Every foreign key is indexed and every tenancy column leads its table's primary access path.
- The two time series tables are partitioned by time and dropped by partition on retention, never deleted
  row by row, because a retention policy that deletes a hundred million rows never runs.
- No console list issues a query per row: every board, queue and listing is one query with its joins.

### Volumes at a hundred site organisation

| Table | Rows per site per year | Read by |
|---|---|---|
| visit | 50 thousand to 300 thousand | site and state; site and time range; asset |
| visit_capture | four to eight per visit | visit |
| observation | 5 million to 50 million | site and time range; camera and time range; asset and time range |
| asset_position_history | 10 million to 100 million | asset and time range, retained by age |
| move | 100 thousand to 500 thousand | site and state; assignee and shift; asset |
| appointment | 50 thousand to 300 thousand | site, door and time range |
| custody_event | ten to thirty per visit | asset and visit, ordered |
| audit_event | 1 million to 10 million | organisation and time; actor; resource |
| exception | 5 thousand to 50 thousand | site, state and severity |

### Seed data

The seeded rows are exactly those of the seeded fixtures in Technical requirements. Seeding must be
idempotent: restarting the app must not duplicate rows.

## Front-end specification

Every visual value below was measured from the reference product, except where a statement says
it is proposed. Throughout this brief the register is normative versus informational: a capability
requirement is normative and must be met, while an observed implementation of the reference is
informational evidence the build is free to satisfy another way. Colours are carried as their family, tone and shade and never as a code; the
exact shade is yours so long as it reads as that description in that role. Motion is carried as
its moment and character. Type is carried exactly.

### The content route estate

Forty seven addresses were measured. Every one is a real route; every other address answers the
not-found document with status `404`.

| Path | Family |
|---|---|
| `/` | home |
| `/home` | home, the same document at a second address, declaring `/` canonical and absent from the sitemap |
| `/why-junction` | pillar |
| `/what-is-ycs` | pillar |
| `/clearyard-yms` | pillar |
| `/the-agentic-ai-yard` | pillar |
| `/junction-ai-computer-vision` | pillar |
| `/ycs-vs-yms` | pillar, comparison |
| `/junction-at-the-gate`, `/junction-in-the-yard`, `/junction-at-the-dock`, `/junction-across-your-operation` | the four surface routes |
| `/yard-security` | pillar |
| `/get-more-out-of-your-wms-and-tms` | pillar, integration |
| `/modules/gate-management`, `/modules/haulier-risk-assessment-and-driver-id`, `/modules/dispatch-and-spotter-orchestration`, `/modules/yard-visibility`, `/modules/load-verification`, `/modules/haulier-appointments` | the six module routes |
| `/markets/junction-for-executive-leadership`, `/markets/junction-for-financial-decision-makers`, `/markets/junction-for-digital-transformation-innovation-teams`, `/markets/junction-for-it-technology-professionals`, `/markets/junction-for-operations-management`, `/markets/junction-for-logistics-specialists`, `/markets/junction-for-frontline-users` | market routes by role |
| `/markets/junction-for-3pls`, `/markets/junction-for-retail-grocery`, `/markets/junction-for-consumer-packaged-goods-cpg-`, `/markets/junction-for-refrigerated-warehousing`, `/markets/junction-for-contract-carriers` | market routes by industry |
| `/markets/junction-for-warehouse-yards`, `/markets/junction-for-manufacturing-facilities`, `/markets/junction-for-drop-lots`, `/markets/junction-for-maintenance-fueling-depots` | market routes by facility |
| `/markets/junction-for-medium-sized-operations` | market route by size |
| `/top-yard-problems/real-time-visibility`, `/top-yard-problems/inefficient-operations`, `/top-yard-problems/high-operational-costs`, `/top-yard-problems/poor-customer-experience`, `/top-yard-problems/security-safety-and-fraud`, `/top-yard-problems/lack-of-supply-chain-resilience`, `/top-yard-problems/slow-technology-adoption`, `/top-yard-problems/meeting-sustainability-targets`, `/top-yard-problems/labor-shortages-and-workforce-issues`, `/top-yard-problems/lack-of-integration-and-data` | the ten problem routes |
| `/resources`, `/resources/blogs`, `/resources/case-studies`, `/resources/videos`, `/resources/webinars`, `/resources/press-releases`, `/resources/podcasts-articles` | the resource hub and six listings |
| `/all-resources/{slug}` | resource detail |
| `/about`, `/events` | company |
| `/contact`, `/demo-landing-page` | conversion |
| `/yard-efficiency-calculator`, `/yard-security-grader`, `/interactive-highlights-2026-state-of-the-yard-survey` | tools |
| `/technical-index` | utility |
| `/terms`, `/privacy`, `/security`, `/accessibility` | legal |

Six further literals found only in shipped bundle strings were probed and all answered not-found:
two two letter fragments, two nested two segment fragments, a content delivery prefix and a
versioned interface prefix. They are artefacts, not hidden routes, and are not built.

**The console route table**, all under `/console`, site first because every operational record
belongs to one site and grants are per site: `/` the organisation home and site chooser; `/s/{siteId}`
site home; `/s/{siteId}/map`; `/s/{siteId}/gate`; `/s/{siteId}/gate/{visitId}`;
`/s/{siteId}/appointments`; `/s/{siteId}/appointments/new`; `/s/{siteId}/appointments/{appointmentId}`;
`/s/{siteId}/dispatch`; `/s/{siteId}/dispatch/{moveId}`; `/s/{siteId}/docks`; `/s/{siteId}/assets`;
`/s/{siteId}/assets/{assetId}`; `/s/{siteId}/security`; `/s/{siteId}/workflows`;
`/s/{siteId}/workflows/{instanceId}`; `/s/{siteId}/exceptions`; `/s/{siteId}/reports`; `/network` the
control tower; `/network/reports`; `/admin/organisation`; `/admin/sites`; `/admin/members`;
`/admin/roles`; `/admin/hauliers`; `/admin/integrations`; `/admin/tokens`; `/admin/audit`;
`/admin/identity`; and `/s/{siteId}/field`, the frontline surface chosen by role. `/console/login`
signs a member in. Creating a booking in the console opens its own route rather than a dialogue, and
the outcome of a write is confirmed with a toast.

**The portal route table**: `/carrier` the haulier home; `/carrier/book` availability and booking;
`/carrier/visits/{visitId}` one visit; `/carrier/drivers` the roster; `/carrier/settings` profile and
notifications; `/carrier/login`; and `/v/{token}`, a driver's single visit view with no account.

**Cross-linking rules.** Every module route links to its surface route, to at least two problem routes,
and to the two adjacent modules in the yard's physical order: gate, visibility, dispatch, dock, load
verification, with appointments upstream of the gate and risk assessment inside it. Every problem route
names at least two modules, and every module is named by at least three problem routes; the content back
end refuses a publish that breaks this. Every market route ends on the same platform tab strip and
conversion block. Every content route offers three conversion paths and no more, in this order: the
self-guided product tour, the demo request, and the contact route.

### The navigation taxonomy

The header exposes five items: four open a panel and one is a direct link. These are the single source
for the header, the mobile drawer and the footer.

**System.** A direct link `Why Junction?`. The group `The Yard Control System`: `What is YCS`,
`ClearYard YMS`, `The Agentic AI Yard`, `Junction at the Gate`, `Junction In the Yard`, `Junction at the
Dock`, `Junction Across Your Operations`. Direct links `The Agentic AI Yard`, `Junction Computer Vision`,
`Yard Security`, `YCS vs. YMS`. The group `Top 10 Yard Problems`: `Real-Time Visibility`, `Inefficient
Operations`, `High Operational Costs`, `Poor Customer Experience`, `Security, Safety, and Fraud`, `Supply
Chain Resilience`, `Slow Tech Adoption`, `Meeting Sustainability Targets`, `Labor Shortages and Workforce
Issues`, `Lack of Integration and Data`. A direct link `Get More out of TMS/WMS`.

**Markets.** `By Size`: `Enterprise Operations`, `Medium-Sized Operations`. `By Need`: `Gate Management`,
`Haulier Risk Assessment & Driver ID`, `Dispatch & Spotter Orchestration`, `Yard Visibility`, `Load
Verification`, `Haulier Appointments`, `End to End Yard Security`. `By Role`: `Executive Leadership`,
`Financial Decision Makers`, `Digital Transformation & Innovation`, `IT & Technology Professionals`,
`Operations Management`, `Logistics Specialists`, `Frontline Users`. `By Industry`: `Third Party
Logistics`, `Retail & Grocery`, `Consumer Packaged Goods`, `Refrigerated Warehousing`, `Contract
Carriers`. `By Facility`: `Warehouse Yards`, `Manufacturing Facilities`, `Drop Lots`, `Maintenance &
Fueling Depots`.

**Featured.** `2026 State of the Yard Survey`, `2026 Events`, `Yard Security Grader`, `Yard Efficiency
Calculator`, `Lights-Out Yard Webinar`.

**Resources.** `Resources`, `Press Releases`, `Podcasts & Articles`, `Videos`, `Blogs`, `Case Studies`,
`Webinars`, `Yard Efficiency Calculator`, `2026 State of the Yard Survey`, `Yard Security Grader`.

**About** is a direct link with no panel.

### Design system

**Character.** Three grounds used as whole section decisions rather than accents: a near-white neutral, the
brand's near-black cool neutral, and a true near-black neutral. Type is a neutral grotesque set tight and
large, with labels and numerals in a small, wide tracked, upper case monospace. One mid, vivid lime carries
every emphasis and is the only saturated colour on the public surface. Structure is drawn with hairlines and
rounded orthogonal connector paths that read as a technical diagram of a yard.

**Scaling.** The layout scales from one root unit rather than a breakpoint ladder: a spacing unit
proportional to the viewport width, capped so that the layout stops growing at the widest desktop width and
centres in the wider field. A second unit of one hundredth of the small viewport width tracks the viewport
without the cap. Three viewport height units, dynamic, large and small, are published because mobile browser
chrome moves, and full bleed sections use the small one so a section never jumps when the address bar
retracts. Every gutter, section rhythm and card inset is a multiple or fraction of the spacing unit.

**The public palette, by role.**

| Token | Described | Role |
|---|---|---|
| `--c-white` | near-white neutral, the lightest | primary light ground, type on dark |
| `--c-dirty-white` | near-white neutral, a step down | secondary light ground, card fill on white |
| `--c-black` | near-black neutral, true black | the ground of the technical grid section |
| `--c-dark-green` | near-black cool neutral with a green cast | the brand ground, footer, dark cards, and body type on light |
| `--c-lime` | mid, vivid lime | the single emphasis colour |
| `--c-orange` | light, vivid red leaning orange | the one warning colour, reserved for exposure and risk |
| `--c-gray` | deep neutral | muted type on light |
| `--c-dark-gray` | mid neutral | tertiary type, placeholder text |
| `--c-light-gray` | light neutral | disabled type, section eyebrow labels |
| `--c-light-light-gray` | near-white neutral, a hairline step | hairlines, dividers, unfilled track |
| `--c-black-10` | black at a tenth | shadow base |
| `--c-dark-green-05`, `--c-dark-green-15`, `--c-dark-green-20` | the brand ground at a twentieth, a little over a seventh and a fifth | tint fill, tint border, emphasised tint border |
| `--c-dark-gray-008` | a deep neutral at a whisper | subtle fill on white |
| `--c-white-0`, `--c-white-15`, `--c-white-20`, `--c-white-30`, `--c-white-40` | white fully transparent, then at rising translucency | gradient terminus, hairline on dark, border on dark, muted type on dark, secondary type on dark |

**The ratio is the design.** The three most used computed colours in the whole product are the brand's
near-black cool neutral, near-white neutral and the hairline near-white neutral, in that order, and they
outnumber everything else combined; a built home route whose colour census does not look like that has
drifted. The lime appears once for roughly every sixty uses of the two grounds. It is permitted only on the
primary action, the active navigation item, a hover state, a live status dot, a numeral in a proof point and
the connector path origin blob, and it is forbidden as a section ground on the public surface.

**The console palette**, measured and reserved for the console where the public palette has no member for a
required meaning.

| Token | Described | Role |
|---|---|---|
| `--c-status-critical` | mid, vivid red | a breached service level, a refused visit, an exposed security layer |
| `--c-status-critical-soft` | light, soft red | the same at reduced weight on a dark ground |
| `--c-status-caution` | a translucent vivid amber | a partial state, a threshold approached |
| `--c-status-ok` | a translucent muted green | a satisfied state where the lime would read as an action |
| `--c-info` | mid, vivid blue, deeper | an informational link in dense operational text |
| `--c-accent-blue` | mid, vivid blue | a selected map object |
| `--c-accent-blue-bright` | mid, vivid cyan leaning blue | a hovered map object |
| `--c-deep-green` | deep neutral with a green cast, one step lighter than the brand ground | the console ground |
| `--c-panel` | deep neutral | a neutral panel on the black ground |
| `--c-panel-raised` | deep neutral, a step lighter | a raised neutral panel |
| `--c-hairline-dark` | deep cool neutral | a hairline on the console ground |
| `--c-muted-dark` | light neutral, darker | secondary type on the console ground |
| `--c-muted-mid` | light neutral, lighter | tertiary type on the console ground |
| `--c-surface-1`, `--c-surface-2`, `--c-surface-3` | near-white neutrals, middle, recessed and raised | the console's light surfaces |
| `--c-tint-lime` | near-white, muted lime | the lime at ground weight, for a success wash |

**Alpha overlays** are published as their own tokens rather than composed at the point of use, because the
reference used a fixed ladder and composed values drift: nine white overlays from faint to three quarters on
dark, and seven overlays of the brand ground from a whisper to half on light.

**Contrast pairings.** On near-white grounds, primary type is the brand's near-black cool neutral, secondary
type the deep neutral and hairlines the hairline near-white; on the brand ground and on true black, primary type
is near-white, secondary type near-white at four tenths, and hairlines near-white at a sixth or a tenth. Anything
outside these pairings needs a contrast measurement before it ships. The lime on white fails normal text contrast
and is never body copy on a light ground; it is legal as type on the brand ground, as a fill behind brand ground
type, which is the one action treatment, as a hairline, and as a graphic element with no text. The warning colour
on white is legal only for a label at the smallest semibold label size or above, and always carries a word beside
the colour.

**Typography.**

```css
:root {
  --font-primary: "Junction Grotesk", "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-mono: "Junction Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}
```

The reference loaded a licensed neutral grotesque in Book, Regular, Medium and Semibold and a monospace in Regular
and SemiBold as self hosted web fonts, plus a third family pulled in by its chat widget vendor. The rendered scale,
in measured use order, is the type scale: no step is added and none is rounded.

| Step | Size | Weight | Line height | Measured on |
|---|---|---|---|---|
| display-1 | `82.4976px` | `400` | `78.3727px` | the home hero statement |
| display-2 | `70px` | `400` | `70px` | route titles, the most used large step |
| display-2-tight | `70px` | `400` | `66.5px` | the title variant setting two lines |
| display-3 | `58px` | `400` | `55.1px` | section titles |
| display-4 | `50px` | `400` | `50px` | card titles at the widest width |
| title-1 | `47.9952px` | `500` | `50.395px` | numeric proof points |
| title-2 | `46px` | `400` | `55.2px` | section subtitles |
| title-2-alt | `46px` | `450` | `55.2px` | the same at the text weight |
| title-3 | `39.9984px` | `400` | `39.9984px` | card titles |
| title-4 | `34.5024px` | `400` | `48.3034px` | long form subheads |
| title-4-tight | `34.5024px` | `400` | `41.4029px` | the same in a card |
| title-5 | `32px` | `400` | `38.4px` | list headings |
| body-1 | `22.9983px` | `450` | `28.9779px` | standfirst paragraphs |
| body-2 | `22.5072px` | `400` | `32.8605px` | long form body |
| body-3 | `18px` | `400` | `25.2px` | dense body |
| body-4 | `17.2512px` | `450` | `21.7365px` | card body, the most used body step |
| body-5 | `16px` | `400` | `24px` | the interface default and the most used step overall |
| body-5-tight | `16px` | `500` | `19.2px` | emphasised interface text |
| label-1 | `14px` | `450` | `14px` | monospace labels |
| label-2 | `11px` | `600` | `13.2px` | eyebrow labels |
| label-3 | `11px` | `600` | `8.91px` | the same set tight in a badge |
| label-4 | `11px` | `400` | `11px` | the lightest label |

Every step at `11px` and `14px` is set in `--font-mono`, upper case, with widened letter spacing. Every step at
`16px` and above is set in `--font-primary`. Nothing mixes the two families in one line except the calculator's
numeral treatment. Every face uses swap display: a layout that reflows when a font arrives is acceptable, one that
shows nothing while waiting is not.

**Radius, by role**, published as `--r-control`, `--r-card`, `--r-card-lg`, `--r-media`, `--r-media-left`, `--r-media-right`,
`--r-form-panel`, `--r-panel-lg`, `--r-badge` and `--r-hair` in this order. A small softness for buttons, inputs, pills and dropdown triggers, the most used by far; a larger
softness for cards, panels and drawers; a slightly larger one for the product grid card and the promotional banner; a
medium one for media wells inside a card; asymmetric pairs that round only the outer corners of a figure joined to a
panel on its right or left; a form panel softness between card and control for the three large form panels; the
largest softness for the promotional banner's inner panel; a tight softness for the grader's layer badges; and a
hairline softness for the scroll indicator and thin state markers.

**Elevation, four shadows and no others.** `--sh-drawer`, cast leftwards and soft, for the header drawer and mobile
menu; `--sh-form`, a faint inset top highlight with a long, soft drop, for the three dark form panels; `--sh-slot`, soft
and even, for the pinned slot stack; and `--sh-gated`, a two-layer, green-tinted shadow for the gated-content card.

**Blur is a material with six strengths, each with one job**: the strongest for the header drawer and mobile menu panel,
the most used; a near-strongest for the header pill buttons and the form submit control; an even softer, wider one for a
feature card icon well and the contact card arrow; a light one for the drawer trigger; a faint one for the calculator
action and the tab buttons; and a faintest one for the clipped slot. Two element blurs are states rather than looks: a
card's rollover wrapper blurs while revealing the layer beneath, and a loading media element starts heavily blurred and
releases to sharp on decode.

**Gradients**, each a design system decision used more than once and each a linear-gradient or radial gradient over
translucent colours: a vertical rule fade and horizontal rule fades, rightwards and leftwards, from transparent to a
light hairline grey; a tight and a wide lime proximity glow fading to nothing; the numeric
proof point fill running from a deeper to the full lime; the technical grid on black as two one pixel line fields at a faint
white; a media base scrim as a linear-gradient from a near-black neutral to transparent; a subtle lime form ground running from white through
the dirty white to the lime tint; a two-state track fill in the brand ground, solid for its first third and a fifth
strength after; a soft lime results glow; and a skeleton shimmer in faint brand ground tints.

**Two edge masks** make tall or wide ruled figures fade rather than being cut: a vertical linear-gradient ramp from transparent
to opaque across the first and last sixth, and the same ramp composed on both axes.

**One blend mode** in the whole product: difference, on the scroll indicator only, so one element stays legible over both
grounds. It is forbidden elsewhere: reaching for a blend mode to solve contrast means there is a contrast problem.

**Layer order**, nine values and no tenth: in-flow content; a raised sibling in a card; a card's own overlay or media scrim;
a sticky sub-header or tab strip; the sequential stack of a pinned section's slots, one layer per slot; a dropdown surface;
the site header; the header drawer and mobile menu panel; a modal and its scrim; and the conversational widget and consent
banner above everything.

**Spacing rhythm.** A section's vertical padding is one, one and a half or two spacing units; the gap between an eyebrow and
its title is half a unit; the gap inside a card is a quarter unit. Horizontal gutters are one unit on desktop and half a unit
below a tablet width, and the content column is capped and centred above the widest desktop width.

### Iconography

Every figure is inline vector geometry drawn in the current colour. Nothing is an icon font and nothing is a raster. The
geometry below is coordinates, so the build produces the same shapes rather than similar ones.

**The mark and the wordmark.** The lockup occupies a `0 0 215 49` view box, rendered smaller in the header and at its full
footer size. It is a square mark on the left and the wordmark to its right. The mark is a rounded square with one corner cut
back, one closed path in the region from `x` `0` to `44` and `y` `0` to `49`: it begins at `9.16512, 0` where the top edge
meets the corner; a cubic to `6.75488, 1.02245` then a straight run to `1.00056, 6.92436`, a chamfer rather than an arc; a
vertical run down the left edge to `y = 48.0871` closing with a small radius to `y = 49`; a horizontal run along the bottom to
`x = 34.3481`; and a chamfer rising from there toward `36.75`, the clipped corner that is the mark's only asymmetry. It fills
lime on a dark ground and white on the light header pill, and its counter is the ground colour, not a second fill. The wordmark
is not copied from the reference: it is set in `--font-primary` at the Medium weight, tracked to share the mark's baseline and
cap height, and converted to outlines only for the favicon. A second lockup at `0 0 203 45` for the footer, lime mark and white
wordmark, is the same construction at another optical size with a proportionally larger chamfer, not a scaled copy.

**The chevrons**, one construction at three sizes: an open two segment polyline stroked at one and a half units with round
joins and no fill. `chevron-down` in a `0 0 12 12` box is `M3 4.5L6 7.5L9 4.5`, beside the four panel triggers, turning over
when its panel opens. `chevron-right` in `0 0 16 16` is `M6 12L10 8L6 4`, on the mobile drawer's group disclosures, turning a
quarter when a group opens. `chevron-left` is `chevron-right` mirrored about `x = 8`, on the carousel's previous control. A
rotation is a transform on the figure, never a second path, and the two carousel controls are one component rotated so a
disabled state styles identically on both.

**The contact figure** is a handset in `0 0 24 24`, drawn inside the header pill stroked at two units with round caps and
joins, as one continuous stroke: `M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79
0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91`.

**The arrow** ending a text link is not a figure: it is the glyph `->` in `--font-mono`, inheriting the link colour with a
small left margin, sliding a short way to the right on hover. Because it is text it inherits the character reveal without
special handling.

**Section boundary shapes.** Section edges are full width paths whose top edge carries a symmetrical notch, two shallow arcs
stepping the edge down by a fixed depth over a fixed span centred on the column, generated from four parameters rather than
stored: `w`, the path width, matching the viewport, with `1441`, `991` and `391` wide view boxes measured; `depth`, from `20` to
`30`; `span`, from `26.78` at the narrowest to `49.28` at the widest; and `r`, the corner radius, from `2.32` to `61.91`, scaling
with the span. For width `w`, depth `d`, span `s` and radius `r`:

```
M -0.5,-0.5
L (w/2 - s/2 - r),-0.5
A r,r 0 0 1 (w/2 - s/2 + r*0.6),(d*0.2)
L (w/2 - s/2 + s*0.4),(d*0.85)
A r,r 0 0 0 (w/2 - s/2 + s*0.55),d
L (w/2 + s/2 - s*0.55),d
A r,r 0 0 0 (w/2 + s/2 - s*0.4),(d*0.85)
L (w/2 + s/2 - r*0.6),(d*0.2)
A r,r 0 0 1 (w/2 + s/2 + r),-0.5
L (w+0.5),-0.5
L (w+0.5),(h+0.5)
L -0.5,(h+0.5)
Z
```

Four home route boundaries carry no notch and are plain rectangles. The notch is a signal: it marks the top of a section that
introduces a new subject, and a plain edge marks a section that continues the last one.

**The connector path system**, the product's signature figure: orthogonal polylines with rounded corners stroked at one unit
with no fill on a full width view box, four per figure entering from the four edges, each beginning at a blob and ending at a
viewport edge. The blob, repeated per connector and translated to its origin rather than redrawn, is `M55.1257 34C40.6277 34 34
36.52 34 44.5C34 54.16 38.9708 55 55.1257 55 C78.4606 55 121.817 45.34 120.988 44.5C119.817 43.312 78.4606 34 55.1257 34Z`,
filled lime in the emphasised figure and light neutral in the muted one. Corner radii follow the run leaving the corner: `21`
under `100`, `30` under `250`, and `50` from `250`. The desktop set on the home route in a `0 0 1440 679` box:

| Connector | Path |
|---|---|
| left descending | `M 609.75,0 L 609.04,119.75 A 50.3,50.3 0 0 1 558.75,169.75 L 194,169.75 A 50,50 0 0 0 144,219.75 L 144,237.65 A 46.96,46.96 0 0 1 80.47,281.58 L 0,251.23` |
| right ascending | `M 1053.75,0 L 1053.75,153.7 A 50,50 0 0 0 1103.75,203.7 L 1246,203.7 A 50,50 0 0 1 1296,253.7 L 1296,289.5 A 50,50 0 0 0 1346,339.5 L 1440,339.5` |
| right lower | `M 1440,543.2 L 914,543.2 A 50,50 0 0 0 864,593.2 L 864,679` |
| left lower | `M 0,475.3 L 213,475.3 A 25.94,25.94 0 0 1 229.03,521.64 L 28.8,679` |

The mobile set in a `0 0 390 482` box:

| Connector | Path |
|---|---|
| upper | `M 195,0 L 195,56.4 A 40,40 0 0 1 155,96.4 L 0,96.4` |
| right | `M 390,385.6 L 303,385.6 A 30,30 0 0 0 273,415.6 L 273,482` |
| left | `M 0,361.5 L 58.5,361.5 A 21,21 0 0 1 71.85,398.7 L 0,457.9` |

Each connector is drawn twice, once stroked to hold the static state for a reduced motion visitor and once as the target of
the draw animation, and the figure carries the two axis edge mask so a path leaving the box fades. The muted figure's grey was
carried inline on the reference's geometry rather than in a stylesheet, so light neutral is the nearest measured member and
stands in for it.

**The technical grid.** The black home route section is ruled with a two axis single pixel grid at a faint white on a spacing
unit module, a background on one element rather than divider elements, fixed in the section's own coordinates while content
passes over it.

**State figures.** A live dot is a small lime circle inside a slightly larger box with a second circle at the same centre
repeatedly pinging outwards and fading, marking a live camera feed, a moving asset or an active lane, always with the word
`live` beside it. A score ring is a dash drawn circle at radius `60` in a `0 0 140 140` box with a thick round capped stroke,
its track at near-white a sixth strength and its fill in the band's colour. A layer badge is a tightly rounded rectangle with the
tight label step in one of five layer hues. A progress track is a thin bar in the hairline grey, filled from the left in its
row's own hue.

### Global chrome

**The header pill.** Not a bar: a floating rounded pill, horizontally centred and offset from the top of the viewport, sitting
above the content on a translucent white at a sixth strength with the strongest blur behind it, so what is beneath shows through
in colour but not detail, on the site header layer. It holds the mark and wordmark, four panel triggers, one direct link, the
contact figure button and three action buttons. It never changes height, never collapses and never hides on scroll, on every
content route: over grounds alternating between white, black and the brand green, a moving header would read as a defect. Its
labels invert with the ground beneath, white over dark and brand green over light, transitioning their colour with the in-out
curve, driven by testing the header's own rectangle against the ground each section declares, never by scroll position, so a
section added later inverts it without a code change.

**The action cluster**, right aligned in the pill in this order and no other: the contact figure as a small softly rounded
square on a faint white, linking by telephone to `+1 (555) 010-4477`; `Explore Product` in lime with brand green type, opening
the configured product tour with campaign parameters in the same tab; `Request Demo` in white with brand green type, to
`/demo-landing-page`; and `Contact Us` in white at about two thirds strength with brand green type, to `/contact`. Every action
label is two words on two lines, upper case, in `--font-mono` at label-2, each word in its own element so the two lines animate
independently on hover. The buttons carry the near-strongest blur so they stay distinct from the pill over a busy image.

**Outbound destinations.** The product tour, the three social profiles and the telephone link leave the origin, each with a
no-opener relation. Only the product tour carries campaign parameters, appended by the build rather than typed into content, so
renaming a campaign needs no content edit.

**The panel triggers**, `System`, `Markets`, `Featured` and `Resources`, are buttons each followed by `chevron-down`; `About` is a
plain link. The pointer entering a trigger opens its panel after a short intent delay and leaving both trigger and panel closes
it after a slightly longer grace delay; keyboard focus alone does not open it, while Enter, Space or ArrowDown do; Escape closes it
and returns focus to the trigger; Tab walks the panel's links in document order and closes it on leaving; activating the open
panel's trigger closes it; and activating another trigger swaps panels without a close animation in between. On hover the label
and border move from white to lime, an underline drawn as a pseudo element scales from nothing to full width and full opacity,
and a second pseudo element nudges by under one per cent. The underline scales from the left without affecting layout. `System`
differs by measurement: its underline is already present at rest and grows a little on hover, marking the default section.
Preserve it.

**The panel** is a right anchored drawer, never a full width mega menu: an aside rendered in a portal on the drawer layer, narrow,
the full viewport tall, sliding in from its own width to rest, on the brand green at half strength with the strongest blur and the
drawer shadow cast left, with no scrim, the page behind staying visible but inert to the pointer. Inside, a group is a native
disclosure whose summary is the group title and whose body is its links; groups collapse independently and their open state lasts
the session; direct links sit level with group titles without chevrons. The whole taxonomy is the panel content and no link in a
panel resolves to not-found. A panel closes on route change, removed on the new route's first frame rather than animating out.

**The mobile menu.** Below a laptop width the triggers and direct link become one three rule trigger at the right of the pill with
a light blur. The mobile panel is the same aside at the same width, ground, blur and shadow, holding the whole taxonomy at once with
every group collapsed on open, and appending the telephone link and the three actions as full width stacked controls. While it is
open, document scrolling is stopped through the smooth scroll controller, published as a stopped state class on the document root,
never by setting overflow on the document, which fights the controller and jumps on close.

**The scroll indicator** is a hairline element at the foot of a route's first viewport with the difference blend, reading `SCROLL TO
EXPLORE` in `--font-mono` at label-4, removed for good once the visitor scrolls past one viewport.

**The footer** sits on the brand green with white type, four columns on desktop collapsing to one below a tablet width. Identity: the
footer lockup, and below it the analyst badge as three lines of label-4 reading `2025 Market Guide`, `Yard Management` and
`Featured Vendor`. `TECHNOLOGY`: `Homepage`, `Yard Control System`, `The Agentic AI Yard`, `Yard Efficiency Calculator`. `COMPANY`:
`About`, `Resources`, `Contact`. `REACH US`: a title-5 line `Ready for your yard of the future?`, the telephone number as a title-5
link, a muted `Give us a call today.`, and three social marks. The base carries at label-4 the copyright line `Copyright Junction
Systems, Inc. © 2025 All Rights Reserved` with the year rendered from the build clock rather than typed, a link to `Technical
Index`, the links to `/terms`, `/privacy`, `/security` and `/accessibility`, and opposite, right aligned, a muted `Made by` followed by
the `kinetika` mark. The footer is not sticky or pinned, and carries a transform hint because it takes part in the section reveal and
is the last element the scroll system touches.

**The conversational widget.** The reference embedded a third party agent as a frame on the top layer that injected its own family
and root properties. Junction exposes `Ada` as a first party surface instead and keeps the requirement the embed met: a visitor on any
content route can ask a question in natural language and get an answer drawn from the published content without a form. It is inert
until used, loads nothing on first paint, never shifts layout, and can be dismissed for the session.

**Consent and analytics.** The consent surface on the top layer is presented on first visit with accept, reject and a per category
choice, nothing loads before a decision, a rejection holds for the session and is stored for a year, and analytics events carry no
personally identifying value, with the measurement identifier injected from configuration and never committed.

### Motion language

**Six curves carry the product**, from nineteen measured; the rest were third party or one-off and
are not adopted, and a motion that needs a curve outside these is the wrong motion.

| Token | Character | Job |
|---|---|---|
| `--e-standard` | a gentle, even deceleration | colour, background and small transforms, the default |
| `--e-expo` | a very fast start settling into a long, soft landing | the long reveal of an element arriving from below |
| `--e-ui` | a crisp material ease in and out | interface affordances: a menu, a focus ring, a control |
| `--e-inout` | a symmetric ease in and out | the header's colour inversion |
| `--e-notch` | a slow start and slow stop with a fast middle, the one authored curve | the section boundary notch |
| `--e-out` | a plain deceleration published on the document root and referenced by name | the most used curve in the whole product |

Three more serve specific jobs: a springless, very fast settling curve for the card slide; an
accelerating curve for a scale that must move away; and a no-overshoot curve for a transform that
must arrive exactly, used by the digit stack.

**Durations cluster into five bands**, and the bands are the vocabulary: instant, for opacity toggles,
a focus ring and a control's own press; quick, for colour, background, border and a disabled state;
standard, for anything the pointer caused; slow, for a panel or a disclosure; and reveal, for an element
entering the viewport for the first time, just under a second to a little over. Nothing runs longer than
the reveal band except the character reveal, whose length follows its character count, and the scroll
linked connector draw.

**The keyframe catalogue**, after removing the chat widget's own sets:

| Name | Shape | Job |
|---|---|---|
| `char-colour` | from the hairline grey, through the lime at thirty per cent, landing on the brand green | the character reveal, measured six times, once per instance, which is how the per-character delay varied |
| `spin` | one full turn | a pending indicator |
| `pulse` | dipping to half opacity at the midpoint | a skeleton row |
| `ping` | scaling up to double while fading to nothing over its last quarter | the live dot |
| `fade-in` | opacity from none to full | the plain arrival for a reduced motion visitor |
| `shimmer` | the background sliding from left to right | a loading placeholder |
| `slide-in-bottom` | rising from fully below into place | a toast or a sheet |
| `slide-in-left` | entering from fully left, resting at sixty per cent, overshooting a little back at eighty, then settling | a panel arriving with one settle; the out of order stops are measured and are the settle |
| `slide-in-right` | the mirror of the above | a panel from the right |
| `slide-out-top` | rising fully out of view plus a little more, clearing its own shadow | a dismissed banner |
| `marquee` | sliding one full width to the right | the logo wall |
| `nudge` | a small lift and return | an idle hint on a control not yet pressed |

Every keyframe is paused until its element enters the viewport, and every infinite one stops when its
element leaves; a marquee running off screen burns battery for nothing.

**The character reveal**, the signature motion, on every route title, the home hero statement and every
large section title, never on body copy. A heading is split into one element per character; each carries a
will-change hint for opacity and transform while a positional reveal runs and for colour while a colour reveal
runs, both removed on completion, measured at eight hundred ninety four and four hundred forty one hints. Two
reveals compose on the split: an arrival, where each character fades up from nothing while rising a short way
into place on the expo curve, and a colour reveal running `char-colour` linearly, because the keyframe's own
thirty per cent stop is the shaping; both stagger by a tiny per-character delay in document order. Across a
heading that reads as a band of lime washing left to right through the words and leaving them set in brand green.
The split never breaks the accessible name: the heading keeps its full text for assistive technology and the
character elements are hidden from it, so a heading is never read one letter at a time. Under a reduced motion
preference the split is not performed and the heading renders as text in brand green at full opacity on first
paint.

**The section reveal.** Every section's contents arrive once, when the section first crosses seventy per cent of
the way down the viewport, and never again. A block rises from well below while fading in on the expo curve; a card
in a row does the same with a small stagger by index; a field or control rises a little with a short delay while
fading quickly; a figure rotates into place while fading; and a media element starts a tenth oversized and settles to
its size while fading in. These resting start states are exact and differ from one another: a short rise for a
heading character, a small rise for a field, a much longer rise for a content wrapper, and a tenth oversized for media.

**Hover states**, half the perceived craft, each a measured before and after:

| Element | Change |
|---|---|
| navigation trigger | colour and border from white to lime, the before pseudo element matching, the underline scaling from nothing to nearly full with its opacity rising to full |
| the default navigation trigger | the same colour change, with its underline already nearly full at rest and growing just past full |
| a card with a media well | the media scaling up by a fifth inside its fixed frame on the card slide curve |
| a rollover wrapper | blurring and fading to three tenths, revealing the layer beneath |
| a text link | its colour on the root deceleration, and the arrow sliding right |
| an action button | its color and background-color on the standard curve |
| a carousel control | its background on hover, and on reaching its end a disabled state transition held backwards, measured live on seven distinct controls |
| a grayscale logo | from fully grey to full colour |

Every hover rule sits inside a media query for a device that hovers with a fine pointer, which the reference
declared twenty seven times: a touch device never enters a hover state it cannot leave.

**The connector draw.** Connectors draw themselves: each path's dash pattern and dash offset equal its own measured
length, and the offset runs to zero as the figure crosses the viewport, while the origin blob scales from nothing to
full on the expo curve just before its path begins. The draw is scroll linked, a function of the section's progress
through the viewport, so scrolling back un-draws it. The reference drove it with a scroll linked timeline library and a
path drawing plugin at one pinned version; the capability is required and the library is not.

**Reduced motion.** Under a reduced motion preference, which the reference declared, there is no character split and no
character reveal; every entry becomes a quick `fade-in`; the marquee, the ping, the nudge and the connector draw stop and
render at their end state; the scroll linked hero sequence stops and renders its first frame; and every hover and focus
transition stays, because those are feedback, held to the instant band. Reduced motion never removes information: a state
only ever shown by movement gets a static equivalent.

### The scroll system

Eight selectors on the home route change a transform, opacity, clip or background as a continuous function of scroll
position at every width, so the page's layout is partly a function of one input, specified before any route.

**The controller.** One controller owns the document's vertical position. It takes wheel, trackpad, touch and keyboard
scrolling, integrates them into a smoothed target and writes the result, and everything else reads position from it, never
from the raw scroll offset. Its smoothing is a critically damped approach reaching the target within a device pixel about half
a second after a single wheel notch; touch keeps native momentum and only wheel and keyboard are smoothed; anchor links
animate with the controller rather than jumping; it can be stopped and started and publishes that on the document root, with a
base class while installed, a second while a scroll is in progress and a third while stopped; and scroll restoration is manual,
restoring position after the route's first meaningful paint. The base class appears on every route and the in progress class on
the home route at every width. The controller is removed under a reduced motion preference and native scrolling is used, because
smoothed scrolling is a common trigger for motion discomfort. The reference used a dedicated smooth scroll library, identified from
a runtime version global and its own root classes.

**Progress sources**, published as custom properties on the elements that consume them, so nothing reads a scroll offset:
`--section-progress`, from an element's top entering the viewport bottom to its bottom leaving the viewport top, from `0` to `1`,
feeding the connector draw and block reveals; `--pin-progress`, across a pinned section's own scroll length, feeding the hero
sequence and the slot stack; and `--text-highlight-progress`, a heading's own crossing of the viewport centre, feeding the character
colour reveal, measured on the document root resting at `0`, the signature of a highlight driven by scroll rather than a timeline.

**The scrubbed selector inventory** at every width, each a scroll linked animation and none time based, with how many distinct
values each took across nine sampled positions: a vertical rule's transform, 286 on desktop and 294 on mobile, the grid's vertical
hairlines drifting against the content; a horizontal rule's transform, the same counts on the other axis; the glow holder's
transform and background image, 192 and 2, the lime proximity glow tracking down the section; the background gradient's transform,
192, the wide glow moving at a different rate; a picture's transform and opacity, seven to ten each, media scaling and fading
through its section; a clipped slot's clip path, 10, the slot stack; a section divider's transform and background image, 3 and 2,
the fading rules extending as a section is entered; a digit stack's transform, four to five, the counting numerals; and the
sequence wrapper's transform, two to three, the hero container. The two rule selectors take nearly three hundred values across nine
samples, which is a per frame value: the grid drift is continuous, driven from the controller's own frame, composited on transform
and never animated through layout.

**The slot stack.** One home route section pins and steps through six panels over three viewport heights of scroll, each slot on its
own layer in the slot band. Each slot's clip opens from a zero area rectangle at its own notch to the full panel over its own fifth of
the pin progress, casts the slot shadow, and carries the faintest blur while below the active slot. A slot never exits; the next clips
over it. The clip is a referenced clip path per slot, six measured plus nested variants, never a rectangle inset, because slot edges
carry the notch. The pin releases cleanly: a visitor who scrolls past fast and back finds the correct slot, because the stack is a pure
function of `--pin-progress` with no internal counter.

**The document length budget.** The home route measures about seventeen and a half viewport heights at a desktop viewport, is longest
at tablet at about twenty four and a half viewport heights plus one, and about nineteen and a half plus one at mobile. That is what twelve
sections and a three viewport pin cost; a home route half again as long has added a section nobody measured. Nine scroll positions at
`0`, `12`, `25`, `37`, `50`, `62`, `75`, `87` and `100` per cent of scrollable height are the sample for every route.

**Scroll edge cases.** Arriving at a fragment deep in a pinned section resolves the pin's length first and then jumps, correct on the first
frame. A document that grows after first paint recalculates every pin, because a pin that does not is the commonest cause of a section ending
early. A resize across a breakpoint mid-pin recalculates and holds the same fractional progress, not the same pixel offset. A scroll linked
element never intersected because it is inside a collapsed disclosure renders at its end state. A controller that fails to install leaves the
page scrolling natively with every scroll linked element at its end state. Printing releases every pin, renders every reveal at its end and makes
the fixed header static, honouring the print query the reference declared three times.

### The dimensional layer: the pinned frame sequence

The home route opens on one full viewport canvas carrying no three dimensional scene: a pre-rendered image sequence played by scroll position,
of a lorry and trailer at a yard fence under a low sun, holding for the first viewport and handing off to the content beneath. It is the most
expensive thing in the product and the likeliest to be built wrongly.

**The evidence.** One canvas on the in-flow layer, the full viewport; frames requested at the desktop width at indices `0`, `1`, `9`, `17`, `25`,
`33`, `41`, `49`, `57`, `65`, `73`, `81`, `89`, `97`, `105`, `113`, `121`, `129`, `137`, `145`, `153`, `161`, `169`, `177`, `185`, `193` and `201`,
a fetch stride of eight from index one rather than a frame stride, implying at least `202` frames at desktop; a modern lossy still format, one file
per frame; a separate sequence per breakpoint named by breakpoint in the reference's own paths; `5046` still files totalling `239` megabytes across the
capture; and a scrubbed container taking two to three transform values across the pin. A quarter of a gigabyte of frames is not a choice to copy, and
the zero asset guide replaces it entirely.

**The playback contract**, whatever produces the frames: the pin lasts one viewport height and the sequence completes as the first viewport of content
leaves; the frame is `round(clamp(--pin-progress, 0, 1) * (frameCount - 1))`, a pure function with no easing, because easing belongs in the frames; one
draw per animation frame and only when the index changed; cover fit, centred, holding the subject's own anchor at forty per cent of the viewport height
so the composition does not drift with aspect; frame `0` on screen before the route is interactive, never an empty canvas; frames decoded off the main
thread and held as decoded bitmaps, not elements; a bounded ring of decoded frames around the current index, released when the section is more than one
viewport away; and the backing store sized to the device pixel ratio capped at two, with the current frame redrawn synchronously on resize.

**The loading ladder**, interactive after the first stage: first, frame `0` alone at full quality, blocking only the canvas's first paint; second, every
eighth frame in order, blocking nothing, with scrubbing snapping to the nearest loaded frame; third, the frames between, bisecting the largest gap first;
fourth, the next breakpoint's sequence, only when the viewport is near a breakpoint boundary. The stride of eight is what the reference requested and gives
a visitor who scrolls at once a sequence that moves. On a constrained connection or a data saving preference the third and fourth stages are skipped and a
twenty five frame sequence plays, which is still a moving image.

**The handoff.** The sequence does not fade. Past `0.85` pin progress the canvas moves up with the pinned container and the black technical grid beneath is
revealed by that movement rather than a cross fade, because the change from a photographic ground to a drawn one is the route's first argument. Once
released, the canvas unmounts and its frames are freed.

**What it shows.** A slow lateral move along a tractor unit and trailer standing side on against a graded sky, the vehicle in near silhouette, the ground in
deep shadow, the sky from a pale lilac at the top through amber to a hot white at the horizon behind the cab. The camera tracks rather than orbits; the subject
does not move, the light does. The substitute must keep four things: the side on silhouette, the vertical sky gradient, the hard horizon with the ground near
black, and the single specular hot spot behind the cab.

**Three further clips**, served as video inside content sections, are wire frame renders of a yard: numbered parking spots in outline, a trailer descending into
a spot, and a label reading an assignment instruction. They are replaced by a procedural drawing, because a wire frame yard is a figure the build can draw.

**Sequence edge cases.** A frame source that fails entirely draws the procedural sky gradient and the pin still runs. Scrolling faster than frames decode draws
the nearest loaded frame and never queues, catches up or plays frames already passed. A low memory device shrinks the ring to five frames and abandons the third
stage. Reduced motion removes the pin, renders frame `0` as a still and makes the section one viewport tall. Arriving mid-page resolves the index from progress
before the first draw, so frame `0` never flashes. Printing renders frame `0` as a still.

### The home route

The document title is `Junction Yard Control System | The New Industry Standard in Yard Operations` and the description `Max throughput. Easy-to-use. Rapid
ROI. Junction Yard Control System is the only AI-native, fully-integrated platform for the yard of the future.` Two addresses serve it, `/` and `/home`, with
identical measured heights at every width; `/home` declares `/` canonical and only `/` is in the sitemap. There is one document, not two.

**Twelve sections, in order**, each with its ground and top boundary: the pinned sequence on its photographic ground with no boundary; the technical grid
statement on true black, notched; the customer logo wall on white, plain; the three step entry ladder on the dirty white, notched; the embedded savings
calculator on white with a brand green panel, plain; the platform argument on white, notched; the modular platform tab strip on white, plain; the connector
figure and proof points on white, notched; the investor and customer wall on white, plain; the resource carousels on the dirty white, notched; the contact block
on white with a brand green panel, plain; and the closing statement and footer on the brand green, notched.

**The hero statement** over the sequence is one display-1 statement split per character and revealed as the pin begins: `We have reinvented the future of
logistics through the yard. AI-native technology that turns the space between your gate and your dock into the most productive part of your operation.` The
scroll indicator sits at its foot.

**The technical grid statement** is true black ruled with the grid, notched at its top, deliberately close to empty: the grid occupies it and one statement
crosses it. The argument that the yard is an engineered space is made by the change of ground rather than by copy.

**The logo wall** is a five column ruled grid, hairlines in the hairline grey fading at their ends, one wordmark centred in each cell of the middle row, shown in
grayscale and released to full colour on hover, under the heading `Powering the yards behind the brands you know`. Wordmarks are content; the grid reflows to three
columns below a laptop width and two below a tablet width; rows follow the wordmark count and the grid is never padded with empty ruled cells.

**The entry ladder.** Under the heading `Fix one yard problem today. Expand on your timetable.`, three white cards on the dirty white, each with an index label in
`--font-mono` at label-2, a title at title-3, a paragraph at body-4, a media well and an action:

| Index label | Title | Body | Action |
|---|---|---|---|
| `01 FAST START` | `Fix One Problem in the Yard` | `Gate, security, dock: start with the single problem slowing your yard down today. Go live in days with no disruption and at low cost.` | `FIX NOW` |
| `02 SINGLE SITE & GROWING` | `I Have a Few Yards to Optimize` | `Begin with one site, prove the value, and roll out to the rest on your own timeline. No big platform commitment to get started.` | `LEARN MORE` |
| `03 ENTERPRISE NETWORK` | `I Run a Network of Yards` | `One control tower across every site, with the analytics and orchestration to manage your whole operation from a single view.` | `ONE SYSTEM FOR ALL` |

The three steps are three shapes of deployment from one codebase: a single module independently deployable at one site with no dependency on the others and useful
with no integration; site as the unit of configuration, entitlement and rollout, where adding a site never reconfigures the first; and organisation level aggregation,
cross-site policy, roles and reporting with per-site boundaries intact. The reference also promises, twice, live in five days, low information technology lift and no
third party devices to support. The media wells held aerial yard photographs, replaced by generated plan views at three densities, a congested lot, an ordered dock
face and a large ordered lot, because the cards argue about scale. A card's media scales up inside its fixed well on hover.

**The embedded calculator** is the full calculator, not a teaser, headed `Yard Efficiency Calculator` with the eyebrow `Calculator` and the panel heading `Tell us about
your yard:`, its result panel carrying the digit stack and the results glow.

**The digit stack.** A changing numeral is not re-rendered: each digit position is a vertical stack of the ten glyphs translated so the current glyph sits in the window,
on the no-overshoot curve, measured animating four or five times as its section is entered. It is used for the calculator's three category figures and total, the proof
points, and the console's counters, never for a value the visitor typed. The accessible value is the whole formatted number on the containing element and the stack is
hidden from assistive technology.

**The connector figure and proof points.** The connector figure is this section's ground, drawing itself as the section is entered, with proof points over it: a value at
title-1 filled with the numeric lime gradient and a label at label-2 beneath at seven tenths opacity, measured as `Labor Savings from Asset Searches` and `Throughput
Improvement`. The investor and customer wall repeats the ruled grid with different wordmarks and no hover release, because these are investors and the grayscale is the
point.

**The platform argument and tab strip.** The heading `One Modular Platform Infinite Possibilities` carries the lime on the second half of the word `Platform`, set as two
elements, the split point being content. The standfirst: `Build your Yard Control System on application at a time. From gate to dock, start with the application you need
most and then expands as your needs grow. Junction is designed to automate workflows, optimize worker productivity, and deliver maximum visibility of every asset and movement
in the yard.` Beneath, a four tab strip with label-2 upper case tabs and a previous and next pair at the right, the tabs being the four surfaces in order:

| Tab | Card title |
|---|---|
| `AT THE GATE` | `Automate and Expedite Gate Operations` |
| `IN THE YARD` | `Real-Time Visibility and Workflow Automation` |
| `AT THE DOCK` | `Optimize Loading and Improve Dock Efficiency` |
| `ACROSS OPERATIONS` | `A Unified, Connected Data-Driven System` |

Activating a tab scrolls its card to the leading edge and gives the tab the active treatment, unmounting nothing; previous and next advance by one card, not one viewport; a
drag or swipe scrolls freely with momentum and snaps to the nearest card's leading edge; at either end the matching control takes its disabled treatment; and by keyboard the
strip is a tab list where left and right move the active tab, Home and End jump to the ends, and the card row is a labelled region. The strip and the row are one component with
one source of truth and can never disagree. The surfaces themselves cover: at the gate, arrival, identity, appointment match, document capture, lane assignment and release; in
the yard, trailer position, spot inventory, move orders, spotter dispatch and safety; at the dock, door scheduling, loading and unloading, seals and chain of custody; across
operations, multi-site rollup, analytics, integration and exception handling.

**The resource carousels** are six, one per resource category, each with its own previous and next pair, the seven live disabled transitions being these controls at their ends.
Each loads its first four cards with the document and fetches the rest on first interaction; a carousel with no items is not rendered and leaves no heading.

**The contact block** has two columns. The left carries the heading `Contact us and we will be in touch same day, your way` with the lime on two words; `Fill out the form, and
we'll be happy to discuss how Junction can help you with your yard of the future:` followed by `30-minute demo`, `Needs discovery call` and `Yard ROI assessment` beside a lime
rule; and a customer wordmark row under `Trusted by those in the know.` The right carries the contact form in a brand green panel with the form panel softness and shadow.

**The closing statement** on the brand green is `The yard of the future starts today.` at display-2 split per character with one action, `TAKE CHARGE OF YOUR YARD`, and the
footer follows with no boundary: closing section and footer are one dark field.

**Home states.** An unreachable content back end still renders sections one, two, four, five, six, seven, eleven and twelve from build time content, completing the route with no
network call, while the live fetched logo walls and carousels render nothing rather than a placeholder. A carousel category with no items omits the whole carousel with its heading.
A logo wall with fewer wordmarks than columns renders one row of the available cells without ruling empty ones. A calculator that fails to start renders its panel with the default
inputs and a static result and hides the capture. A failed media well renders the procedural placeholder keyed by the item's own identifier, stable between visits.

### The platform pillar routes

Ten routes share one template, measured on six of them with identical structure: an eyebrow, a title, a
standfirst, a problem block, a solution block, a proof block, the platform tab strip, the analyst badge and the
shared conversion block. Its content model is also the content back end schema for this type:

| Field | Type | Required | Rendered as |
|---|---|---|---|
| `eyebrow` | short text | yes | label-2, `--font-mono`, upper case, light neutral |
| `title` | short text | yes | display-2, character split |
| `standfirst` | rich text, two paragraphs at most | no | body-1 |
| `problemLabel` | short text, `The Problem` by default | yes | label-2 |
| `problems` | two to four `{ heading, body }` | yes | a card row at title-4 and body-4 |
| `solutionLabel` | short text, `The Solution` by default | yes | label-2 |
| `solutionBody` | rich text | yes | body-2 |
| `solutionPoints` | three to six `{ heading, body }` | no | the ruled solution grid |
| `proof` | two to four `{ value, label }` | no | proof points |
| `figure` | one of `connector`, `grid`, `sequence`, `none` | yes | the ground treatment |
| `relatedModules` | at least one reference | yes | cross links |
| `relatedProblems` | at least two references | yes | cross links |

The problem block always precedes the solution block and both labels render even with one problem: every pillar
route says what is wrong, then what Junction does.

**Why Junction**, titled `Why Junction?`, names three classes of competing product rather than operational problems:

| Problem | Body |
|---|---|
| `Point Solutions` | `Point tech like camera solutions can be too narrow in scope to meet the full breadth of needs of the modern yard.` |
| `Visibility and Supply Chain Management Solutions` | `Broadly-suited solutions are often robust in other areas, but their YMS modules are frequently an afterthought with little innovation.` |
| `Specialized YMS Vendors` | `Existing YMS vendors may have decent technology for automating individual processes, but their systems often have to be cobbled together with other technology to achieve an end-to-end solution.` |

It then names five buying roles and what each suffers, each row linking to its market route, the densest cross link on the
site and what makes the role routes reachable:

| Role | What it suffers |
|---|---|
| `Executive Leadership` | `The yard causes financial blind spots and strategic risks that impact the entire business.` |
| `Corporate Innovation` | `Legacy systems and data silos in the yard hinder their ability to integrate technology and drive automation across the supply chain.` |
| `Operational Management` | `Lack the real-time visibility and inefficient communication, which are daily challenges that slow down logistics operations.` |
| `Logistics Specialists` | `They care about yard problems because manual processes and a lack of accurate data prevent them from efficiently tracking trailers and managing demurrage and detention fees.` |
| `Frontline Users` | `Problems in the yard cause wasted time, confusing instructions, and unsafe conditions.` |

**What is YCS**, titled `What is YCS`, is the category definition, and its solution copy, which also appears on the home route, is the
product's one sentence definition: `The Junction Yard Control System (YCS) uses computer vision and autonomous decision intelligence to
turn chaotic, manually run yards into self-aware logistics environments. Its key benefits include:` followed by the four surfaces, each
linking to its surface route.

**ClearYard YMS**, titled `Junction ClearYard YMS`, positions the product inside the category the buyer already budgets for, with six
solution points: `AI Computer Vision-Powered Workflows`, `Full Automation and Orchestration`, `Modular and Configurable Platform`,
`Automated Gate Operations`, `Efficient Dock Scheduling`, `Real-Time Asset Visibility`.

**The Agentic AI Yard**, titled `The Agentic AI Yard` with the eyebrow `Why Agentic AI in the Yard`, is the public statement of the
console's autonomy, and the two must agree: anything it claims the system does on its own exists as a workflow definition with a
confidence threshold, an approval path and a record.

**Junction AI Computer Vision**, titled `Junction AI Computer Vision`, carries the product's technical claims. Solution points:
`Flexible Technology`, the estate works with cameras the customer may already own; `Plug & Play`, commissioning without a construction
project; and `Enterprise Ready`, the security and integration posture. Capabilities: `Automated Gate Check-In & Check-Out`, `Leave behind
those manual logs, kiosks, transcription errors, and long queues. With Junction, AI computer vision auto-captures plates, IDs, and containers
in seconds, drivers self-check via a simple flow.` followed by `The results: up to 85% faster gate processing and 75% fewer errors.`;
`Asset Inventory & Location Management`, continuous position rather than a periodic walk; `Automated Damage Detection`, condition captured at
the point of action; and `Security & Fraud Detection`, identity and behaviour feeding the security surface. A market research block presents
the pull quote `Warehouse and yard operations are beginning to use AI-enabled vision systems to automate activities and visually monitor
processes to identify ergonomic, safety and procedural issues.` with two figures labelled `yard deployments will employ vision-AI enabled
autonomous data collection instead of RFID` and `of WMS systems are supporting some AI enabled vision deployments`. An analyst quotation or
figure carries a source attribution field and does not render without it, because an uncredited market figure is a legal exposure.

**YCS vs. YMS**, titled `YCS vs. YMS`, with six differentiators: `AI Computer Vision at its Core`, `AI-Driven Autonomous Workflows`, `Single
Pane of Glass Visibility`, `Configurable to All Yards`, `Unlocks Value of WMS/TMS`, `Low Disruption, High Value`. Beneath them a case study
headed `Rydell reduces time to productivity`, with the body `Inefficient manual gate processes led to significant delays, operational
bottlenecks, and inaccurate data. Junction Rapid Gate uses computer vision to automate lorry check-ins, reducing dwell.` and the pull quote `We
have not seen this kind of accuracy with computer-vision technology, this is a significant milestone in the race to modernize the yard.`; and a
value block with the eyebrow `Our Value`, the standfirst `we offer the most flexible, cost effective solution on the market.`, and three points
`Maximum, automated throughput`, `Scalable, easy operation` and `Affordable, rapid ROI`. The reference's origin statement, reused on the about
route: `Junction was founded by industry leaders to set a new, AI-driven standard for yard automation and execution. Unlike fragmented point
solutions, the Junction Yard Control System unifies critical yard operations.`

**The four surface routes** use the template with the sequence figure and four problems each:

| Route | Problems |
|---|---|
| at the gate | `Truck Congestion & Queuing`, `Inefficient Check-In / Paperwork`, `Lack of Visibility & Scheduling`, `Security & Compliance Gaps` |
| in the yard | `Trailer Misplacement`, `Idle Equipment & Inefficient Moves`, `Poor Visibility into Capacity`, `Safety Risks` |
| at the dock | `Dock Door Bottlenecks`, `Uncoordinated Labor & Equipment`, `Load/Unload Delays`, `Cross-Team Communication Gaps` |
| across operations | `Fragmented Systems & Data Silos`, `Poor Real-Time Visibility`, `High Detention & Demurrage Costs`, `Lack of Predictive Planning` |

The gate route's solution heading is `Junction Solves Problems At The Gate, Differently`.

**Yard Security**, titled `Junction Yard Security`, is sold as a cross cutting capability: yard security, cargo fraud prevention and chain of
custody have been a patchwork and Junction makes them native. Its primary action is the security grader rather than a demo request, because a
security buyer answers fifteen questions before talking to a salesperson.

**Get More Out of WMS/TMS**, titled `Get More Out of WMS/TMS`, with the standfirst `You've invested in a WMS to optimize your warehouse and a TMS to
streamline transportation, but bottlenecks, yard delays, and frustrated carriers persist.` Its solution block is the eight exchanges, a public
commitment honoured exchange for exchange: `Inbound Asset Notifications`, the yard telling the warehouse what arrived before it is unloaded; `Spotting
Task Management`, `Optimized yard jockey movements ensure trailers are in the right place at the right time, eliminating idle dock time.`;
`Intelligent Dock Scheduling`, `Real-time updates on appointments allow dynamic adjustments to doors and labor, preventing costly backlogs.`;
`Inventory Reconciliation`, `By providing real-time visibility into trailers, a YCS enables the WMS to conduct more accurate cycle counts and
inventory reconciliations.`; `Dynamic Receiving Prioritization`, the yard telling the warehouse about high priority inbound loads so receiving plans
and labour can move; `Agentic Exception Handling`, `Our AI-enabled system will detect issues, diagnose root causes, and take intelligent corrective
actions in real-time across all prescribed yard workflows.`; `Automated Trailer Status Updates`, `Real-time trailer status feeds directly to your TMS,
creating a single source of truth.`; and `Detention & Demurrage Alerts`, `Automatic alerts when dwell times exceed thresholds, preventing unnecessary
costs.`

**The ruled solution grid** separates cells with fading hairlines rather than borders over a masked vector figure: each cell is a heading at title-4-tight
and a body at body-4 and nothing else, no icon, action or image. The one exception, measured, is a soft lime glow on the cell under the pointer.

### The module routes

Six routes, one per module, and the highest converting on the site. They differ from the pillar template in three ways: the problem is one long, specific,
unflattering paragraph in the second person about the reader's own yard; the solution is one paragraph naming the mechanism; and a field guide block offers a
gated practical playbook with a one line promise. The model adds `fieldGuideTitle`, `fieldGuidePromise` and `fieldGuideAsset`, the last a reference to a gated
document. Every capability a solution paragraph names exists in the console section behind that module: gate management in the gate, haulier risk and driver
identity in security, dispatch in dispatch, yard visibility in the map, load verification in the dock, appointments in appointments.

**Gate management**, `Yard Gate Management & Automated Truck Check-In`. Problem: `A guard with a clipboard, a radio, and a printed appointment list can only
process one truck at a time, and every truck behind it idles. Drivers burn hours of service in the queue, license plates and paperwork are transcribed by hand,
and nothing that happens at the fence reaches the yard until somebody walks it over.` Solution: `Junction Gate Management enables seamless gate operations by
using computer vision-enabled cameras to automate key ID capture, refilling lane cards, and providing a single dashboard for all in-and-out movements.` Field
guide: `A practical playbook for cutting truck check-in from minutes to seconds.` Its capability: unattended arrival capture, identity and plate reading,
appointment match, lane and dock assignment, and a printed or messaged instruction to the driver.

**Haulier risk assessment and driver identity**, `Driver Identity Verification & Carrier Fraud Prevention`, the one place on the public site naming cargo theft
directly. Its capability: identity capture and verification, haulier authorisation check, watchlist evaluation, a risk band and a refusal path, because anyone can
claim to be anyone at an unmanned fence.

**Dispatch and spotter orchestration**, `Yard Spotter Management & Trailer Move Automation`. Problem: `In most yards, spotter moves are assigned over the radio by a
supervisor working from memory and instinct. Spotters drive empty across the lot to the wrong end, the genuinely urgent move waits behind three routine ones, and nobody
can say afterwards how long anything took.` Solution: `By replacing chaotic radio chatter with a digital command center and an intuitive, browser-based spotter app,
Junction empowers dispatchers to visually manage yard assets, digitally assign tasks, and measure what actually happened.` Field guide: `A practical playbook for spotter
management.` Its capability: a prioritised move queue, automatic assignment against position and travel cost, a browser handheld for the driver, and digital acceptance and
completion.

**Yard visibility**, `Real-Time Yard Visibility & Trailer Tracking`. Problem: `Trailers go missing inside your own fence, spotters spend half their shift hunting for assets,
and the inventory in your system stopped matching reality hours ago. Someone walks the lot with a clipboard to find out.` Solution: `By utilizing a vehicle-mounted Real-Time
Location Service to continuously update asset locations, operations can eliminate manual audits, optimize spotter routing, and better align asset readiness with the dock.`
Field guide: `A practical playbook for real-time yard visibility.` Its capability: continuous position for every asset, a live map, a self reconciling spot inventory, and an
audit that is a query rather than a walk.

**Load verification**, `Load Verification, Chargeback Prevention & Chain of Custody`. Problem: `When a customer files a chargeback or an OS&D claim, the burden of proof is on
you, and most yards can't meet it. There's no record of what was actually loaded, no chain of custody from the dock to the gate, and no way to show the seal was intact when it
left.` Solution: `Junction enables seamless load verification by capturing dock-door data and verifying seals at the point of action, defending against chargebacks and damage
claims, and providing federated customer reporting.` Field guide: `A practical playbook for proving what left your yard.` Its capability: dock door capture at the point of
action, seal verification, an unbroken custody record from dock to gate, and a shareable evidence pack.

**Haulier appointments**, `Yard and Dock Appointment Scheduling & Carrier Self-Service`. Problem: `Carriers can't book their own slots, so they show up whenever, and
appointments bunch, doors sit empty for an hour and then four trucks arrive at once, and no-shows blow up the plan.` Solution: `Carrier Appointments is a centralized system that
simplifies facility management by automating truck arrival booking, document scanning, and ID capture via computer vision and mobile devices.` Field guide: `A practical playbook
for managing yard schedules.` Its capability: a published availability calendar, self service booking from outside the tenant, capacity and door constraints, reminders, and
no-show handling with rebooking.

A seventh capability, end to end yard security, sits in the navigation as a cross cutting offer rather than a module.

**The field guide block** carries the eyebrow `FIELD GUIDE`, a promise line at title-4 and one action, which opens the gated form in place rather than navigating, because a visitor
at the foot of a module route who is moved to a new address is lost. Once a visitor gives an address for any field guide in a session, later field guides on other routes deliver at
once.

### The market routes

Seventeen routes address the one product to seventeen audiences across size, need, role, industry and facility, because a warehouse operations manager and a finance director
search for different words and will not read each other's page. The template is the pillar template with the problem block as pain points, labelled `Core Pain Points` on role
routes and `The Problem` on industry and facility routes; the solution block as outcomes written in the audience's vocabulary naming the roles served; and, on role routes only, a
motivation block labelled `Why Solve the Yard Now`. The same tab strip instance closes every market route, which is what stops seventeen routes becoming seventeen products.

**Frontline users.** Pain points `Wasted Time`, `Confusing Instructions` and `Unsafe Conditions`, with the bodies `Task assignments are vague or delivered via a static list, leaving
you to guess what to do next.` and `You're often walking into unsafe or unfamiliar areas, and you lack a clear way to report hazards or problems.` Motivation `Reduce Physical
Strain`, `Improve Safety` and `Empowerment`. Outcomes:

| Outcome | Body |
|---|---|
| `Intuitive Browser-Based App` | `A super-intuitive easy to use browser-based application works with any mobile device and operator language.` |
| `Visual-First Design` | `The interactive yard map shows you exactly where every asset is and what its status is, eliminating the need to search for a trailer in a sea of boxes.` |
| `Clear, Simple Task Lists` | `Your assignments are delivered directly to the application in a clear, prioritized list. A Spotter knows exactly what to do next without relying on radio communication.` |
| `Instant Communication` | `Allows users to communicate instantly with managers and other drivers to report an issue or request help, improving efficiency and safety.` |

Those four outcomes are what the frontline surface must be: browser based, map first, a prioritised list, and able to raise an issue.

**Executive leadership** addresses the buyer who never opens the console: its outcomes are the network control tower and its proof points are financial.

**Third party logistics**, `Junction for 3PLs`, with the standfirst `Stop losing revenue to congestion, wasted driver time, and manual errors. Junction YCS transforms your yard
into a strategic asset, enabling seamless scalability and a new level of customer service.`, problems `Multi-Client Complexity`, `High Variability`, `Diverse Yard Types` and
`Strict SLA Pressures`, and outcomes:

| Outcome | Body |
|---|---|
| `Boost Profitability` | `Reduce dwell times, eliminate detention fees, and hit performance goals by optimizing trailer movement and increasing yard throughput.` |
| `Enhance Client Satisfaction` | `Deliver real-time visibility and precise ETAs, giving account managers and client service teams the tools to communicate confidently with customers.` |
| `Scalable Operations` | `Handle fluctuating volumes and complex yard operations without adding headcount or expanding physical space, supporting COOs and network managers in managing growth efficiently.` |
| `Operational Excellence` | `Streamline communication across gate, dispatch, and dock teams, reducing manual errors and helping frontline Yard Jockeys and Dispatchers work faster and smarter.` |
| `Data-Driven Decisions` | `Gain actionable insights on dwell times, turn times, and asset utilization, giving executives, analysts, and operations leaders the data to make strategic improvements.` |

Its multi-client problem forces a data model decision: a third party logistics operator runs one yard for several of its own customers, so every asset, movement and cost is
attributable to a customer of the tenant, which is the field federated reporting filters on.

**Search and metadata.** Every market route has its own title, description and canonical address, none generated by concatenation, with titles following the pattern of subject then
two claims joined by an ampersand as content. Every market and pillar route emits structured data for the organisation, a product referencing the module set, and a breadcrumb list,
from the content model rather than authored markup. The seventeen routes never compete in search: each has its own canonical address and is linked from exactly one navigation group.

**Market states.** No proof points omit the proof block. No motivation block omits it, since only role routes have one. Tab strip cards that fail to resolve leave the four labels as
links to the surface routes and omit the card row. A route with fewer than two related problems does not publish.

### Yard problems, comparisons and case studies

**The ten problem routes**, in the navigation's order, which is preserved, with the navigation label and the slug differing on three of them because one is written for a scanning
reader and one for a search engine, both stored and neither derived: Real-Time Visibility at `real-time-visibility`; Inefficient Operations at `inefficient-operations`; High
Operational Costs at `high-operational-costs`; Poor Customer Experience at `poor-customer-experience`; Security, Safety, and Fraud at `security-safety-and-fraud`; Supply Chain
Resilience at `lack-of-supply-chain-resilience`; Slow Tech Adoption at `slow-technology-adoption`; Meeting Sustainability Targets at `meeting-sustainability-targets`; Labor Shortages
and Workforce Issues at `labor-shortages-and-workforce-issues`; and Lack of Integration and Data at `lack-of-integration-and-data`. Each is titled `Top Yard Challenges | <problem>
Solutions for Logistics`, uses the pillar template with the grid figure, and adds a block naming the modules that address it with one line each on how.

**The problem to module matrix**, shipped as content:

| Problem | Modules |
|---|---|
| Real-time visibility | yard visibility, dispatch and spotter orchestration |
| Inefficient operations | dispatch and spotter orchestration, haulier appointments, gate management |
| High operational costs | dispatch and spotter orchestration, gate management, yard visibility |
| Poor customer experience | haulier appointments, load verification |
| Security, safety and fraud | haulier risk assessment and driver identity, load verification, gate management |
| Supply chain resilience | yard visibility, haulier appointments |
| Slow technology adoption | gate management, yard visibility |
| Meeting sustainability targets | dispatch and spotter orchestration, haulier appointments |
| Labour shortages and workforce issues | gate management, dispatch and spotter orchestration |
| Lack of integration and data | yard visibility, load verification |

**The case study** is a first class content type embedded on the comparison route, the resource listings, the home carousels, a market route and its own detail address: a customer
reference carrying the wordmark; a headline at title-3; a situation and an intervention at body-4; a pull quote at title-4 with its quote mark faded to four tenths and an attribution;
and two to four metrics shown as proof points. Every metric requires a `basis` rendered at label-4 beneath its label, and a metric without one does not render, because a percentage with
no denominator is how a case study becomes a liability.

**The comparison routes.** Ten articles compare Junction with ten rival products, with a near identical standfirst describing Junction as a purpose built, category native platform
providing end to end orchestration and automation across the yard against a rival described by what it does not cover. They are one template with a structured comparison table whose rows
are the six differentiators. Every claim about a rival carries `sourceUrl` and `asOfDate` and prints the date; a rival's name is text and never its mark; and an unsourced claim does not
render and its row collapses rather than showing an empty cell. They carry the same robots directives as every route but are excluded from the primary navigation, reachable from the resource
listings and search only.

**The survey** route presents the 2026 State of the Yard Survey interactively and freely, gated only at download, drawing on insights from over two thousand operations leaders on what is
working, what is breaking and where teams are investing, using the grader's segmented result.

### The company routes

**About**, titled `A Different Kind of Logistics Technology Company | The Yard Reinvented` with the eyebrow `About Junction`, is the third longest route at about fourteen and a half
viewport heights on desktop, a long form argument rather than boilerplate, in order: a display-1 character split statement over the technical grid; the origin statement; the four surface tab
strip; a leadership card grid of portrait, name, role and one line; the investor wall; a list of office cities with an address each and no map; and the connection block. The leadership grid is
the only place a person's photograph appears, and every card renders correctly with no portrait, decided for the whole grid rather than per card.

**Press releases** are a resource category, not a company route, each with a dateline of place and date, a headline, a standfirst that is a complete sentence, and an optional quotation with a
named attribution, covering a product launch, a workflow product, a market guide recognition, a partnership and a chief executive appointment.

**Events**, titled `Meet Junction at an Event in 2026` with the eyebrow `Upcoming Events` and the standfirst `Our Go To Market and Leadership teams will be traveling a ton this year to
contribute new ideas, meet with customers, and connect with new prospects at the industry's most important gatherings.` A grid of event cards, three across on desktop, two at tablet and one
below a tablet width, measured with seventeen events, each with dates and city on one label-2 monospace upper case line such as `9/13-15, Long Beach`, a name at title-4-tight such as `IANA
Intermodal Expo`, a one sentence summary at body-4 such as `North America's leading intermodal freight trade show, where rail, trucking, port and logistics leaders shape what moves next.`,
and an optional `Register Today` booking link. The date is a structured range, not a string, so an event whose end has passed moves to a past band beneath the grid or is removed if that band is
empty, the grid sorts by start date and groups by month under label-2 month headings, and each card emits event structured data. With every event past, the grid is replaced by a message and the
connection block.

**The connection block** closes the events, contact and about routes, headed `We are here to help` with the eyebrow `Other ways to connect`, as four cards: `Download 2026 State of the Yard
Survey`, opening the gated form, on the brand green; `Chat with Ada, our AI`, `Get instant answers about integrations, edge cases, and more, no forms required.`, opening the agent, on white;
`Calculate your ROI`, `Enter your yard size, throughput, and dwell time to estimate your ROI.`, navigating to the calculator, on the brand green; and `Subscribe to our newsletter`, an inline
`Work Email *` field and action, on white. Light and dark themes alternate; each card's arrow carries a soft blur behind it. The newsletter card submits without leaving the route and replaces its
own form with a confirmation in place, never navigating or opening a modal.

**Company states.** No upcoming events render the past band alone with a message and the connection block. An event without a booking address omits its action. A missing leadership portrait
removes portraits from every card. A failed newsletter submission keeps the value, states the error inline beneath the field and re-offers. An already subscribed address receives the same
confirmation as a new one, because confirming or denying a subscription discloses whether an address is on a list.

### The conversion routes and forms

**The contact route**, titled `Contact - Junction`, carries the contact form in a dark panel, a gated datasheet offer headed `Not ready for a call? Download a brief overview of Junction.` with
the field `Work Email *` and the action `Download Now`, the connection block, and a resource carousel.

**The contact form**, six fields in this order, two columns on desktop collapsing to one below a tablet width, the last two spanning both columns:

| Field | Type | Required | Placeholder | Validation |
|---|---|---|---|---|
| Full Name | text | yes | `John Doe` | two to eighty characters with at least one non-space |
| Role or position | text | yes | `Project manager` | two to eighty characters |
| Phone number | telephone | no | `(323) 555-0147` | if present, a parseable international number stored canonically and shown in the visitor's format |
| Email | email | yes | `name@email.com` | a syntactically valid address whose domain has a mail exchanger; free mail domains accepted |
| Company name | text | yes | `Acme` | two to one hundred and twenty characters |
| How Can We Help? | multiple select | yes | `Select options` | at least one of `Schedule a 30-minute meeting with a yard expert`, `Schedule a YCS Demo`, `Arrange ROI consultation`, `Set Up a 2-Day Proof of Value on site`, `Something else` |

The panel is the brand green with the form panel softness and shadow. Fields are underlined rather than boxed, a single hairline in near-white at a fifth strength moving to lime on focus, with
labels above each field at body-4 that never float into it, because a floating label that becomes the only label disappears from a screen reader's description. The submit control is disabled until
the form is valid, shown at half opacity with the near-strongest blur, and stays focusable and announces why it is disabled. A field blurred while invalid shows its error beneath, turns its rule to the
warning colour and takes an invalid state; a corrected field clears its error on input, not on blur; submitting an invalid form moves focus to the first invalid field and announces the error summary;
submitting while in flight is impossible and shows pending; success replaces the panel in place with a confirmation naming what happens next and when, without a route change; a network failure keeps
every value, states the error above the control and re-offers; and server field errors are applied to their fields by name.

**The demo landing route**, titled `Demo Landing Page`, with two separately split heading lines `Schedule a demo of` and `built to replace yard labor,`, five fields `Full Name`, `Company`, `Title`,
`Phone Number` and `Email` with no help topic and no free text, reached from campaigns where every extra field costs conversions. It has no navigation panels, no footer link list and no resource
carousel: only the mark, the form, a customer wall and the analyst badge, the one route where the chrome is stripped. Campaign parameters on its address are captured into the submission and never
rendered into the document.

**The gated form** is a white panel with the media softness and the gated shadow, one `Work Email *` field, one consent checkbox and one action.

**The shared conversion block** closes every pillar, module, market and problem route with the same three actions in order, the analyst badge and the telephone line, one component instance carrying
no route specific copy.

### Error route dress

**The not-found document**, titled `404 - Junction`, is the brand green ruled with a technical grid of faint white lines: the lockup centred with a lime mark and white wordmark, whose mark moves from
white to lime on hover; the code `404` at display-1 in lime with its zero set as a slashed glyph; the title `Page not found` at display-3 in white; the description `The page you're looking for doesn't
exist or has been moved.` at body-4 in `--font-mono`, muted, on two lines, the one place body copy is monospaced so the route reads as a system message; a primary lime action `BACK TO HOME` with brand
green type at label-2; and a secondary text link `EXPLORE RESOURCES ->`. It carries the header and footer at reduced weight, the mark and the two actions only, and runs no scroll system, character split
or sequence. The not permitted, removed and failure documents share this dress with their own code, title, description and actions.

### Responsive behaviour

**The measured media queries**, with their use counts saying which are structural: a minimum at laptop
width, the primary structural breakpoint where navigation, grids and panels change, sixty one uses; a
minimum at tablet width, the secondary one where one column becomes two, thirty one uses; a hovering fine
pointer, every hover rule, twenty seven; a maximum just under laptop width, the mobile navigation and drawer,
fourteen; a minimum at the widest desktop width, where the content column caps, nine; a minimum at a wide
laptop width, where the console inspector docks beside the work area, seven; a minimum at a very wide desktop
width, where the calculator and form panels widen, four; a minimum at a large handset width, two up card grids,
three; reduced motion, four; and print, three. The layout scales continuously from the spacing unit: these
queries change structure, never size, and a build that copies the breakpoints without the fluid unit is wrong at
every width between them.

**The three captured viewports** are desktop at `1440` by `900`, tablet at `1024` by `768` and mobile at `390`
by `844` CSS pixels. The tablet document is the longest, the signature of two columns collapsing to one before the
type reduces; preserve it.

**The content site across the three widths.** The header is the full pill on desktop, the pill with the mobile
trigger at tablet, and the mark with the trigger alone on mobile. The navigation panel is a narrow right drawer on
desktop and tablet and full width on mobile. Pillar problem cards run four, two and one across; module solution
grids three, two and one; market outcome grids three, two and one; the logo wall five, three and two columns; the
events grid three, two and one. The resource carousel shows four cards, then two and a half, then one and a quarter,
so the next card is visibly cut, which is the affordance that tells a touch visitor the row scrolls. The contact block
is two columns with the form on the right, then one column with the form below. The calculator has inputs left and
result right, then inputs above and result below, and on mobile the result stays at the foot until scrolled past. The
tab strip keeps four tabs on a row, then scrolls horizontally, then keeps the active tab scrolled into view. The footer
runs four, two and one columns.

**Pinned sections** keep their pin at every width with pin lengths in viewport heights, sourcing a separate frame
sequence per breakpoint. Below a tablet width the slot stack reduces from six slots to four, merging the two closest
pairs, because six slots on a tall narrow screen is four screens of scrolling for one argument.

**The console across widths.** At the widest desktop widths the rail is collapsed and expands on intent, the site bar is
full, the inspector docks, the map and board sit side by side, the calendar shows a full day and the dispatch board three
columns. At a wide laptop width the inspector narrows the work area and the calendar scrolls. At laptop width the site bar
keeps only the switcher and exception count, the inspector becomes a sheet over the work area, the map and board stack board
first, the calendar shows a half day, and the dispatch board shows two columns with attention first. Below laptop width the
rail becomes a bottom bar of five entries and an overflow, the inspector is full screen, the board shows alone with a map
action, the calendar becomes a list of appointments by hour, and the dispatch board is one column with attention first.

**The narrow console.** Laptop width is the minimum for full capability; below it the console becomes a triage surface of
the exception inbox, the lane board, the move attention column and the site's counters, every other surface states the width
it needs and offers the frontline surface where the member's role permits, and the map becomes a spot list grouped by row with
each spot's asset, state and dwell and a filter, which is the right instrument, not a degradation.

**The frontline surface** is designed at mobile width and scaled up, the inverse of every other surface; above tablet width it
centres at a narrow maximum rather than filling the width, because a tablet is still used one handed.

**Orientation, zoom and text.** Every surface works in both orientations and none locks, the frontline surface designed portrait;
browser zoom to `200%` loses no function and never scrolls the document horizontally; a `200%` text only increase clips no control
and truncates no label, every text bearing element sized logically rather than at a fixed height; the frontline surface follows the
operating system's text size; everything is usable at `320` CSS pixels wide; and at very wide screens the content column caps and the
console's work area distributes rather than stretching a table.

**Responsive edge cases.** A resize across a breakpoint mid-pin follows the scroll edge cases. Resizing below laptop width with the
inspector open makes it full screen with its state kept. Rotating a handset during a frontline task keeps the task and every
confirmation. A foldable changing posture is a resize and loses nothing. A console surface printed repeats table headers, releases pins,
drops the rail and site bar, and stamps every page with the site, the member and the instant. A very large operating system font on the
frontline reflows the single task layout into a vertical stack with nothing truncated.

### Accessibility

**The standard.** The whole product meets WCAG AA, and the console and frontline surfaces meet it with the additions below. Buyers
include information technology professionals and public sector adjacent operators who procure against a conformance statement, and the
frontline surface is a condition of someone's job, so a yard worker with low vision or limited dexterity must be able to do it.

**Colour and contrast.** The contrast pairings of the design system are the legal set. Body text reaches a ratio of at least `4.5` to
`1`; large text and interface graphics at least `3` to `1`; the lime on white is never text; a focus indicator reaches `3` to `1`
against both its component and its ground; disabled controls are exempt from the ratio but are never the only signal of a state; and each
map asset state is distinguishable from its neighbours by shape or hatch as well as fill.

**Reflow.** Every surface reflows to a `320` CSS pixel equivalent at `400%` zoom with no two dimensional scrolling, except the yard map, the
appointment calendar and the dispatch board, which are inherently two dimensional and each offer a single column view carrying the same
information.

**Structure and naming.** One top level heading per document, landmark regions on every surface, and a skip link as the first focusable
element. The character split keeps the heading's accessible name and hides the characters. The digit stack exposes its formatted value and
hides the glyphs. Every icon-only control has a name, and decorative chevrons are hidden. Every table has a caption and header associations,
while the dispatch board and lane board are lists of articles, because their cards are not rows. Spot, door and asset identifiers are read as
written, so `A-14` is never announced as a date or a subtraction.

**Keyboard.** Every surface is fully operable by keyboard with a visible focus indicator at every step and no trap anywhere: navigation triggers
and panels as specified; the tab strip as a tab list with arrows, Home and End; carousels as a group with previous and next controls, arrows
scrolling the row and every card in the tab order; the calendar as a grid where arrows move by slot and resource and Enter opens a booking; the
map as specified; dialogues and drawers moving focus in, holding it, restoring it on close and closing on Escape; toasts never stealing focus,
announced politely, with their actions reachable from a defined chord; the command surface; and the console's chords listed on a keyboard help
surface reachable by a documented chord. No chord collides with an assistive technology's own, and every chord has a pointer equivalent.

**Nothing by colour or motion alone.** The grader's layer statuses carry `Exposed`, `Partial` and `Covered`; the map's states carry a hatch for
dwelling, a dashed outline for stale and a label on selection; gate check results carry a word beside each mark; freshness carries the age in
words; a service level breach names its objective and attainment; a live indicator carries the word `live`; and the connector draw's end state
carries what its animation carried.

**Forms and errors.** Every field has a persistent visible label above it and never a placeholder as its only label. Errors are tied to their
field, announced when they appear and repeated in a summary at the top of a long form with a link to each. A disabled submit states why in an
associated description. Required fields say so in the label, not only by an asterisk's colour. A field's expected format is stated before it is
entered. The only time limits in the product are the soft booking hold and the break glass session, and each warns before it expires and offers to
extend where it can.

**Frontline additions.** Touch targets of at least `56` CSS pixels separated by at least `8`, against `44` on the public surface; text contrast of at
least `7` to `1` in daylight mode; no status by colour, motion or sound alone; every action possible with one finger and no path gesture; no control
that needs a response within a time window; every state changing action either reversible within `30` seconds or confirmed by naming the action; and
text resizable to `200%` with the single task layout reflowing.

**The accessibility statement** at `/accessibility` states the conformance target, the assessment date, the known exceptions with the three two
dimensional surfaces and their alternatives, the assistive technologies tested, and a contact for reporting a barrier with a stated response time. A
known exception with no alternative and no remediation date does not belong in the statement; it belongs in the backlog.

**How conformance is held.** An automated rule scan runs on every route and console surface every release, blocking on a level A violation; a person
traverses every surface by keyboard every release; a screen reader pass on the console and frontline surfaces uses at least two reader and browser
combinations every release; zoom and reflow at `400%` is checked every release; and a frontline user reviews the frontline surface every quarter. The
automated scan catches about a third of what matters; the keyboard and screen reader passes catch the heading read letter by letter, the map with no
keyboard path and the disabled control that never says why.

### Frontend performance

**What the reference cost.** `5046` still images totalling `238955766` bytes, `4` moving images at `10261085`, `12` other raster stills at `5500541`,
`154` scripts at `312277`, `6` font files at `199268` and `26` vector files at `835`. The frame sequences were ninety eight per cent of the payload; a build
that copies the look and the payload copies the wrong half.

**Budgets per content route** at the desktop viewport on a connection shaped like a fast mobile network: largest contentful paint `2.0s`; interaction to next paint `200ms`;
cumulative layout shift `0.05`; first party script before hydration `120KB` compressed and total script `220KB` compressed; fonts two families, four faces,
`140KB` in total; first viewport images `250KB` including the sequence's first frame; total payload at first paint `600KB`; and `25` requests before
interactive. **Per console surface** on a stable connection: shell interactive in `1.5s`; a surface's first useful render within `1.0s` of navigation; map
frame time `16ms` while panning two thousand assets; a live update painted within `250ms` at the ninety fifth percentile; and application script `450KB`
compressed, split per surface. A budget regression fails the build rather than raising a warning.

**The critical path.** A content route's first paint depends on the document, one stylesheet, one font face and the sequence's first frame, and nothing else:
no script, content back end call or third party blocks it. The character split runs after the route renders without shifting layout, because a heading's box
is identical split and unsplit.

**Fonts.** Two families and four faces, the text family at two weights and the monospace at two, swap display, the two first viewport faces preloaded, subset
to the characters the content uses plus a Latin extended range, served from Junction's own origin, with the fallback stacks metric adjusted so the swap moves
no line.

**Images.** Every content image in at least three widths and two formats chosen by the browser; intrinsic dimensions on every image so none shifts layout;
first viewport images eager at high fetch priority and everything else lazy; asynchronous decoding except the sequence's first frame; the generated cover shown
at once and replaced on decode, never a grey box or a costly blurred thumbnail; logo walls in vector where the source is vector, with grayscale as a filter
rather than a second asset; and custody images at a thumbnail in lists and full size only in a viewer.

**The sequence budget.** The first frame within the first viewport budget; the twenty five stride frames under `1.2MB` together; the intermediate frames at low
priority never competing with a navigation; the decoded ring bounded and released on exit; and the procedural generator removing the class from the budget, so a
content route's first paint fits `600KB` with the sequence included.

**The main thread.** No task over `50ms` during load or scroll; the scroll controller reads and writes once per frame and never reads layout inside a scroll
handler; the scrubbed selectors animate transform and opacity only; the character split runs in chunks yielding between headings; the map has its own render loop
decoupled from the framework's; hydration is progressive by section with lower sections hydrated on approach; and the agent, consent surface and analytics load after
the load event and after consent.

**Caching and delivery.** Documents revalidate at the edge and serve stale while revalidating, invalidated by publish; hashed immutable assets, sequence frames and
fonts are cached for a year; content back end responses are cached at the edge tagged per item and purged by tag; console responses are never cached at the edge and
are cached per principal in the browser's query cache only; and no console or portal response is ever cacheable by a shared cache, because a tenant scoped response in
an edge cache is a cross tenant disclosure waiting for a key collision.

**Measurement.** Field measurement of the three core metrics on the content site, segmented by route family, device class and connection; synthetic measurement in
the pipeline against the budgets; and real user measurement of console surface render times and map frame times segmented by site, so a site with a slow local network
arrives as a metric rather than a support case.

**Performance edge cases.** A font that fails renders the metric adjusted fallback with no reflow. A bot with no script receives the full document with every section's
copy and reveals at their end state. A console member on a high latency satellite link falls back to polling with honest freshness. A very high pixel ratio caps the
canvas at two. A data saving visitor skips the later sequence stages, gets the smallest adequate images, and the agent does not preload.

### Copy deck

Every string below was rendered by the reference and read from the capture, with names replaced by Junction's own. It is transcribed, not written.

**Global chrome.** Navigation `System`, `Markets`, `Featured`, `Resources`, `About`; actions `EXPLORE PRODUCT`, `REQUEST DEMO`, `CONTACT US`; scroll indicator
`SCROLL TO EXPLORE`; footer column heads `TECHNOLOGY`, `COMPANY`, `REACH US`; footer technology `Homepage`, `Yard Control System`, `The Agentic AI Yard`, `Yard
Efficiency Calculator`; footer company `About`, `Resources`, `Contact`; footer reach `Ready for your yard of the future?`, `+1 (555) 010-4477`, `Give us a call today.`;
footer base `Copyright Junction Systems, Inc. © 2025 All Rights Reserved`, `Technical Index`, `Made by kinetika`; analyst badge `2025 Market Guide`, `Yard Management`,
`Featured Vendor`.

**The System panel.** `Why Junction?`, `The Yard Control System`, `What is YCS`, `ClearYard YMS`, `The Agentic AI Yard`, `Junction at the Gate`, `Junction In the Yard`,
`Junction at the Dock`, `Junction Across Your Operations`, `The Agentic AI Yard`, `Junction Computer Vision`, `Yard Security`, `YCS vs. YMS`, `Top 10 Yard Problems`,
`Real-Time Visibility`, `Inefficient Operations`, `High Operational Costs`, `Poor Customer Experience`, `Security, Safety, and Fraud`, `Supply Chain Resilience`, `Slow
Tech Adoption`, `Meeting Sustainability Targets`, `Labor Shortages and Workforce Issues`, `Lack of Integration and Data`, `Get More out of TMS/WMS`.

**The Markets, Featured and Resources panels** are exactly the navigation taxonomy's members.

**The home route.**

| Section | Copy |
|---|---|
| hero | `We have reinvented the future of logistics through the yard. AI-native technology that turns the space between your gate and your dock into the most productive part of your operation.` |
| logo wall | `Powering the yards behind the brands you know` |
| ladder heading | `Fix one yard problem today. Expand on your timetable.` |
| why eyebrow and heading | `Why Junction`, `Introducing the Junction Yard Control System` |
| why body | `The Junction Yard Control System (YCS) uses computer vision and autonomous decision intelligence to turn chaotic, manually run yards into self-aware logistics environments. Its key benefits include:` |
| platform eyebrow and heading | `Platform`, `One Modular Platform Infinite Possibilities` |
| tabs and tab cards | `AT THE GATE`, `IN THE YARD`, `AT THE DOCK`, `ACROSS OPERATIONS`; `Automate and Expedite Gate Operations`, `Real-Time Visibility and Workflow Automation`, `Optimize Loading and Improve Dock Efficiency`, `A Unified, Connected Data-Driven System` |
| benefit | `Start with the applications you need most and then expand as you need or as your operations become more complex. Live in 5 days, low IT lift, no third-party devices to support.` |
| benefit | `Eliminates Unnecessary Labor`, `Automated workflows eliminate the need for labor at the gate, dispatch, yard.` |
| contact | `Contact us and we will be in touch same day, your way`; `Fill out the form, and we'll be happy to discuss how Junction can help you with your yard of the future:`; `30-minute demo`; `Needs discovery call`; `Yard ROI assessment`; `Trusted by those in the know.` |
| closing | `The yard of the future starts today.`, `TAKE CHARGE OF YOUR YARD` |
| other actions | `Explore the Survey`, `Junction on the Road`, `Grade your yard security now.`, `Go to Calculator`, `Register Today`, `All Resources`, `Read More`, `Learn More`, `Watch Now`, `Check them out!` |

**The calculator.** `Yard Efficiency Calculator`, `Calculator`, `Tell us about your yard:`, `Number of gates`, `Shifts per day`, `Operating days per week`, `Spotters per
shift`, `Check-ins per day`, `Blended hourly wage`, `How significant are your annual detention and demurrage costs?`, `1 - LOW`, `5 - MEDIUM`, `10 - HIGH`, `With
Junction your yard saves`, `Est. Savings:`, `Estimated annual savings by category:`, `Labor Savings (Gate, Traffic, Dispatch, Yard Check):`, `Spotter Savings (Drivers
and Unit Leases):`, `Detention & Demurrage Savings:`, `Want to know more?`, `Enter your work email below if you would like to run a custom ROI analysis with one of our
team of yard experts.`, `Work Email`, `SUBMIT`, `Massive impact, minimal disruption, insane confidence`.

**The grader.** `Yard Security Grader`, `Junction · Yard Security Grader`, `How secure is your yard, layer by layer?`, `Grade your yard`, the introduction sentence, `What
we grade`, `Grade my yard`, `Your result`, `/ 100`, `Open yard`, `The gate is verifying almost nothing.`, the two sentence explanation, `L00 Digital Check-in`, `L01 Carrier
Risk Assessment`, `L02 ID Verification`, `L03 Load Verification`, `L04 Perimeter Cameras`, `Exposed`, `Partial`.

**The contact and demo routes.** Contact fields `Full Name`, `Role or position`, `Phone number`, `Email`, `Company name`, `How Can We Help?`; placeholders `John Doe`,
`Project manager`, `(323) 555-0147`, `name@email.com`, `Acme`, `Select options`; the five help options; the datasheet offer `Download datasheet`, `Not ready for a call?
Download a brief overview of Junction.`, `Work Email *`, `Download Now`; the demo route `Schedule a demo of`, `built to replace yard labor,`, `Full Name`, `Company`,
`Title`, `Phone Number`, `Email`; and the connection block `Other ways to connect`, `We are here to help`, `Download 2026 State of the Yard Survey`, `Chat with Ada, our AI`,
`Get instant answers about integrations, edge cases, and more, no forms required.`, `Calculate your ROI`, `Enter your yard size, throughput, and dwell time to estimate your
ROI.`, `Subscribe to our newsletter`, `Work Email *`, `Submit`.

**The module routes.** The six titles, problems, solutions, `FIELD GUIDE` and promises of the module routes section.

**The pillar routes' titles.** `Why Junction | AI-Powered Yard Management & Logistics Solutions`; `Junction YCS | Yard Control System for AI-Driven Logistics Automation`;
`Junction ClearYard YMS | Real-Time Yard Visibility & Autonomous Operations`; `Junction Agentic AI Yard | Autonomous AI-Driven Yard Management`; `Junction AI Computer
Vision | Real-Time Yard Intelligence & Logistics Automation`; `Junction YCS vs YMS | Yard Control System vs Yard Management System`; `Junction at the Gate | AI-Powered Gate
Automation & Logistics Flow`; `Junction in the Yard | AI-Powered Yard Operations & Real-Time Visibility`; `Junction at the Dock | AI-Driven Dock Efficiency & Logistics
Optimization`; `Junction Across Your Operation | Integrated Supply Chain Solutions`; `Junction Yard Security | AI-Driven Perimeter Security & Cargo Fraud Protection`; `Get More
Out of Your WMS & TMS | Boost Warehouse & Transportation Efficiency`. Labels `The Problem`, `The Solution`, `Market Research`, `Case Study`, `Our Value`, `Featured Content`,
`Core Pain Points`, `Why Solve the Yard Now`. Vision claims `Automated Gate Check-In & Check-Out`, `Asset Inventory & Location Management`, `Automated Damage Detection`,
`Security & Fraud Detection`, `Flexible Technology`, `Plug & Play`, `Enterprise Ready`, `The results: up to 85% faster gate processing and 75% fewer errors.`

**The company routes.** About's title, eyebrow and origin statement; events' title, eyebrow and standfirst; resources `Resources`, `Viewpoints for a smarter yard`, `Latest
News`, and the card categories `blog`, `video`, `case-study`, `webinar`, `announcement`.

**The error route.** `404`, `Page not found`, `The page you're looking for doesn't exist or has been moved.`, `BACK TO HOME`, `EXPLORE RESOURCES ->`.

**Metadata.** The home description and the robots directives as stated for the home route and canonical rules.

**Rules for copy.** The trademark mark on `YCS`, `Yard Control System` and `ClearYard` is part of the string, not appended by the renderer. The platform heading's mid-word
colour break is authored as two elements. Every measured string is set exactly as transcribed, including the reference's own inconsistencies listed below. Headings are
sentence case and actions and labels upper case, measured and consistent. No long dash appears anywhere in the copy; where the reference used one, a colon or a comma replaces
it.

### The zero asset guide

The build receives no binary: every asset class the reference used is replaced by a recipe. Values here are proposed rather than measured, except named colours.

**What is replaced.** The hero frame sequence, files named `hero_anim_desktop_60_0.webp` through at least `_201.webp` per breakpoint; the wire frame yard clips,
`vid_3-1_prerender_1.mp4`, `vid_3-3_prerender_1.mp4` and `vid_3-5_prerender_1.mp4`; the four licensed grotesque faces and two openly licensed monospace faces; `26` vector and
`11` raster customer and investor wordmarks; yard photography in the ladder cards and article covers; leadership portraits; and a social preview image per route.

**The hero sequence** is a generator, not a file set, producing frames at build time or drawing at runtime, runtime preferred because it removes the class from the payload.
Four layers from back to front: a sky gradient over the whole canvas from a cool pale lilac at the top through amber in the middle third to a hot near-white band at the horizon,
interpolated in a perceptual space so the amber does not muddy; a sun as a radial falloff just behind the cab at the horizon with a bright core and long soft skirt, its intensity
the animated parameter; the ground as a flat near black below the horizon with one soft edged light pool spreading from the sun's base across about a third of the width; and the
vehicle as a near black side on silhouette with a rim light on its sun facing edge only. The silhouette is built from primitives: a trailer body about two thirds of the frame wide
and a quarter tall with a lighter top edge; a thin chassis rail with two wheel groups of two circles at the rear third; two thin landing legs at the front third; a cab of a tall front
face, a sloped upper and a shorter rear face joined by two arcs, with one lighter rounded window, a thin exhaust stack and a mirror arm; three groups of two wheels for steer and drive;
and a rim light stroking the same paths finely in a warm near-white on the sun facing side, fading away from the sun. Over the pin the camera tracks laterally by about a fifth of the
frame width, the sun's intensity rises then settles, and the rim light's falloff follows the sun; nothing else moves. This keyframe contract is inferred from scroll screenshots rather
than a recovered timeline. The generator is deterministic from a seed and a progress value so a frame is reproducible.

**The wire frame clips** are drawn: a true black ground with the technical grid; outlined spot rectangles in a cool pale blue at low opacity in a row, each numbered above in
`--font-mono` at label-1; the silhouette drawn as an outline in the same blue with circular wheels; the trailer descending from above the frame into its spot, decelerating over the
clip's progress; an instruction label as a rounded rectangle of the brand ground at high opacity with lime monospace type at label-2 appearing as the trailer settles, its copy being
content such as `ASSIGN TO SPOT 11`; and sparse single pixel white points at low opacity drifting slowly for depth.

**The typefaces.** `Junction Grotesk` is a neutral grotesque with a large x-height and closed apertures in Book, Regular, Medium and Semibold, licensed or an openly licensed
grotesque of similar proportion named in the build, with true italics not required. `Junction Mono` is a monospace with a slashed zero, a clearly distinct `1`, `l` and `I`, and wide
default tracking, in Regular and SemiBold. Whichever is chosen, the fallback stacks are metric adjusted to it and the type scale rechecked at the display steps, because another
x-height moves line breaks. The slashed zero is required: the not-found route sets `404` large, the grader sets a score, and the console sets spot identifiers, where an ambiguous zero
is an operational error.

**Photography and covers** become a deterministic generated cover keyed by the item's identifier: a seed from the identifier; two palette members chosen by seed from the brand ground,
the lime, the warning colour, the dirty white and the light neutral, always a legal contrast pair; a ground in the first with three to six seeded connector paths in the second; the
technical grid over it at low opacity; a fine tonal grain from an inline turbulence filter at a base frequency of about `0.9` with four octaves, desaturated, at about four per cent
opacity; and the category label in the corner in `--font-mono` at label-2. The three ladder cards take a density parameter and draw a plan view of a yard as small filled rectangles at
three densities, a diagram consistent with the rest of the surface.

**Wordmarks and portraits.** A customer wordmark is the customer's property and is not generated: the placeholder name is set in `Junction Grotesk` Semibold, sized to its cell, in the
brand green, and since grayscale does nothing to a text mark its hover becomes an opacity change from faint to full. A leadership portrait becomes the person's initials in `Junction
Grotesk` Medium in the dirty white on a ground generated from the name, decided per grid.

**Social previews** are generated per route at build time from the cover generator at the social aspect ratio with the route's title set over it on up to two lines and the mark in the
corner, deterministic from the route's address.

**Audio.** The content site has none. The console has two synthesised cues, both off by default, opt-in per member and never the only signal: for a severity one exception, two short
enveloped triangle wave tones a fifth apart with a short gap, a fast attack and a gentle release; and for a gate decision needing an operator, one short sine tone pitched clearly above a
gate house's ambient noise.

**What the substitutions cost**, stated honestly: the hero loses photographic realism and reads as a rendered illustration while keeping composition, light and motion; the wire frame clips
lose almost nothing; the typefaces lose the exact line breaks the headlines were art directed around; the photography loses realism deliberately in favour of diagrams; and the wordmarks lose
recognisability, so real marks must be supplied before a real audience sees them.

### What is measured and what is proposed

**Measured** from forty seven routes at three widths and nine scroll positions each with a hover diff per route: the content routes and their templates; eighty colour values, the complete
root token set, two families and the rendered scale; seventy inline vector figures; one hundred and forty four keyframes, nineteen curves, the transition table, seven live runtime animations
and the scrubbed selector inventory; the canvas, frame request pattern, stride and asset census; the calculator's seven inputs, defaults, three categories and worked example; the grader's
length, five layers, result structure and one result; and the rendered copy. The route estate captured eleven of twelve pillar routes, all six module routes, four of seventeen market routes,
two of ten problem routes, four of six resource listings and one resource detail; uncaptured routes follow their measured templates, and the uncaptured resource categories deserve a check.

**Reconstructed**: the console, frontline surfaces, haulier portal and every platform section, which sat behind authentication, derived from what the public surface commits the product to.
Read them as a specification to satisfy, not a description of the reference: where the reference's own console differs, these requirements govern.

**Motion that could not be recovered**: the hero sequence's internal timing, baked into its frames; the slot stack's per-slot clip geometry, whose element scoped definitions were not exposed; the
connector draw's timing, which is scroll linked with the blob's lead proposed; and the character reveal's per-character stagger, inferred from total length and character count.

**Values standing in**: the muted connector blob's grey, carried inline on the reference's geometry, stood in for by light neutral; the published deceleration curve, referenced by its token name;
and the console's status and surface colours, measured on third party surfaces embedded in the reference rather than on its own components.

**The calculator's coefficients.** Minutes saved per check-in at `39` was recovered exactly. The hours saved per spotter shift, spotter units released, annual unit cost, demurrage exposure model,
recovery rate and baseline were reconstructed. The reconstructed values first proposed for them, two hours saved per shift, a unit cost of twenty four thousand, an exposure of eight thousand per point
per gate and a recovery rate of fifty five hundredths, do not reproduce the measured worked example, so the measured example governs and the coefficients are fitted to it, as the calculator section
states. Anyone with a second worked example re-fits the coefficients and the acceptance vector together.

**The grader's example.** The measured result screen at a score of thirty carried layer percentages that three answers scored zero to three over nine cannot produce; its band and copy are carried, and
the scoring rule governs every number.

**Inconsistencies in the reference that are preserved**, because silently fixing copy is how a copy deck and a page diverge, and each should be raised with the content owner: the platform standfirst
reads `on application at a time` where `one` appears intended; the same sentence mixes person in `then expands as your needs grow`; the home route's calculator eyebrow is misspelled `Calcultor` in one
instance and correct elsewhere; the comparison route's pull quote read `roce`, corrected here to `race`; three of the ten problem routes' navigation labels differ from their slugs, deliberately; and three
body paragraphs used long dashes, replaced by colons or commas.

**Considered and deliberately not built**: self service subscription checkout and proration, because every measured conversion is a form or a demo request in an enterprise contract sale; usage based
metering and overage billing, for the same reason; a public developer platform with self service credentials, because machine credentials are issued inside a customer organisation; a consumer
marketplace or plugin ecosystem; an event sourced activity timeline as the primary model, because the append only custody and audit chains are what the domain needs; bitemporal tables across the model,
because the versioned site plan and versioned workflow definitions are the two places where knowing what was known when matters; and a third party policy engine component, since whether the one policy
decision is a library or a service is a build choice. Three things go beyond any tier framework because the domain demands them: disconnected operation at the site edge, confidence and provenance on every
observed field, and the separation of a spotter's claim from a camera's confirmation. A build without those three has built the yard management system the reference argues against.

### Properties that hold everywhere

**Structure and content.** Every address in the content route table resolves and every other answers not-found with `404`; the technical index lists every route; every navigation member reaches a real
route; every problem route names two or more modules and every module is named by three or more problem routes; a publish breaking the content rules is refused naming every failure; every case study metric
carries a basis and every rival claim a source and date; and every route's copy matches the copy deck, including the preserved inconsistencies.

**Visual system.** A home route's colour census is dominated by the brand ground, white and the hairline grey in about the measured ratio; the lime appears only in its permitted places and never as a public
section ground; every type step belongs to the scale; the radius, shadow and blur sets gain no member; the layer order gains no value; boundaries are notched exactly where the home route's section order says;
and the connector figures reproduce the measured path data.

**Motion and scroll.** At the nine scroll positions and three widths every route matches its reference composition; the home route's height stays within five per cent of the measured budget at each width; the
character reveal runs left to right through the lime with the heading's accessible name intact; scrolling back un-draws every scroll linked element; reduced motion runs no split, pin, marquee or draw and loses no
information; a disabled controller still scrolls with every reveal at its end state; and no curve outside the curve set appears.

**Interaction.** The tab strip and its row never disagree; every carousel's controls disable at both ends; the navigation panels honour their intent and grace delays and every keyboard path; the header inverts against
the ground beneath it rather than a scroll position; and no touch device sticks in a hover state.

**The tools.** The calculator's defaults produce the measured vector; no currency value is computed in floating point; clearing a field holds the last valid result and names the field; the disclosure states every
coefficient; the grader's second action goes to the route for the weakest layer; a tampered score is recomputed on the server; and every grader status shows a word as well as a colour.

**Forms and capture.** A submission is recorded before any outbound call and survives a failed call; a replayed submission produces one record and one delivery; a newsletter submission for an existing address is
indistinguishable from a new one; a gated document link is single use and expires; and the agent cites its sources, refuses outside its corpus and cannot reach an operational record.

**Autonomy and workflow.** Every public claim of autonomous action maps to a shipped definition; the four permanently human actions never happen automatically at any confidence; a requester never approves their own
request; an approval survives a definition change, a member leaving and a restart; a misfiring definition is stopped and suspended; an instance explains itself without help; and workflow state is stored as rows and
survives concurrent updates without loss.

**Operations.** A gate decision completes within `4s` at the ninety fifth percentile under load; a capture below threshold goes to an operator with ranked candidates and never decides; a stale console refuses every write; a
move placed but not verified raises an exception; dragging an asset proposes a move and never writes a position; contradicting observations raise an exception rather than one winning; a shift crossing a daylight saving
change lasts its true elapsed time; every operational time renders in the site's zone; and a stale position looks different from a confirmed one.

**Concurrency and integrity.** Simultaneous bookings for one door and window produce one confirmation and a constraint refusal for the rest; simultaneous moves for one asset produce one; a version conflict is surfaced and
never resolved by the last write; replaying a write with its idempotency key produces one effect; replaying a webhook delivery produces one downstream effect; custody and audit chains verify by recomputation; and nothing
can change or remove a custody or audit event.

**Tenancy and authorisation.** Every role, action and scope decides as the policy says; every read and write attempted across an organisation or site boundary returns nothing rather than a refusal that reveals existence; a
haulier user reading another company's booking gets the same answer as for a booking that does not exist; the application's database role cannot read around the tenancy rules; background jobs, exports and cache warmers
act under scoped principals; no console or portal response is storable by a shared cache; a grant revocation takes effect within `30s` everywhere including the live channel; no shipped role includes identity media, unbounded
footage, audit export or break glass; the explanation surface answers correctly for a member with grants from two sources at two scopes; and a federated aggregate over fewer than five loads is suppressed.

**Identity and lifecycle.** A member removed from the directory loses access within the reconciliation interval without signing in; permissions are never trusted claims in a session; a reused refresh token invalidates its
family and raises a security event; sign in, reset and invitation never disclose whether an address is registered; a second factor is required again for every sensitive action; and a leaver's approvals, watchlist entries and
connectors are reassigned.

**Sensitive data.** No identity media, recognition token, raw footage or media object appears in any webhook, exchange, export, notification, log line, trace attribute, analytics event or evidence pack; identity media is
deleted on its own schedule and never held; reading it needs a second factor and a reason and names what was read; footage is never browsed without the unbounded permission; break glass notifies at invocation, expires at
`60` minutes, tags every action and forces a review, and cannot read identity media; the retention sweep deletes from every store a value reached and alarms at severity one when it fails; and no watchlist entry is created
by one person alone or by an integration.

**Resilience.** A site disconnected for four hours in operating hours keeps its gate running on the local cache; an expired watchlist cache fails closed on refusals and open on ordinary admissions; offline frontline actions
arrive in order, idempotently, with a conflicting one reported rather than dropped; a safety report arrives first on reconnection; an observation gap becomes a visible record on any evidence pack covering it; load shedding
sheds in the order failure containment keeps things alive; the daily restore passes with a chain integrity check; and the failure document renders with every other system down.

**Accessibility and performance.** The automated scan passes on every route and console surface; every surface is operable by keyboard with visible focus and no trap; the three two dimensional surfaces offer single column
views; no state is signalled by colour, motion or sound alone; every surface works at `200%` text and `400%` zoom without clipping; the frontline additions hold; every performance budget holds; the map holds its frame budget
at two thousand assets; and no state changing route is registered on a safe method.

**The claims.** A site's baseline is captured in shadow mode before go-live; a site without one reports its improvement as unmeasurable; realised savings use the calculator's three categories; the operational quality reports
are visible to the customer; and every metric prints its versioned definition.

## Constraints

- Tenancy is organisation over site: no row of one organisation, and no row of a site a principal holds
  no grant on, is ever readable, and a haulier or customer user reads only their own company's records.
- Signup is closed; members arrive through the directory or an invitation.
- No self service checkout, no metered billing, no marketplace, no plugin ecosystem, no anonymous
  developer credentials, and no free messaging between operators.
- No native application.
- No backing service beyond PostgreSQL, Keycloak and Mailpit, and no call to any other host.
- Money is integer minor units, instants carry their zone, and identifiers handed out are opaque.
- Custody and audit records only ever grow.
- The console stays responsive with two thousand assets on the map and a year of visits at a site.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is
  the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to `/app/USER_README.md`.
  Junction has thirteen seeded members and seven seeded portal principals, and they all share one password;
  list every address, whether it signs in to the console or the portal, and that password there.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary
  background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the
  container.
- The backing services named in this brief are already running and reachable at their environment variables.
  Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

## Definition of done

Junction is done when it is deployed and healthy, a haulier can book an arrival slot at a Dallas dock door
and receive one confirmation that names no freight, and a held lorry is admitted only once an eligible site
manager, never the person who asked, approves its release. However many bookings or moves arrive for the same
door, window, trailer or spot at once, none is ever allocated twice.
