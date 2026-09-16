# Tessera Brand Guidelines

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the hub, read any of the
eight illustrated guideline chapters end to end, sign in with a provisioned account,
browse the released asset library, open one asset and read the licence terms attached
to it, and raise a usage request against an asset their standing permissions do not
already cover, without hitting an error page. The hard part is the approval stage: a
single stage of a usage request must be decided exactly once, and that must hold when
two reviewers approve the same stage at the same instant. The decision a reviewer holds
must be a real row in the database that a second decision cannot overwrite; a message
the app returns to itself does not count. Exactly one grant is minted per approved
request, and exactly one audit record is written per transition.

## Overview

Tessera Brand Guidelines is where a global technology company keeps, teaches and
polices its visual and verbal identity. The product has two surfaces that share one
identity system and one content spine, and they are one product rather than two.

The **public reading surface** is a hub and eight chapter routes: framework, voice and
tone, logo, typography, iconography, colour, imagery and motion. Each chapter is a long
scroll driven document that teaches by demonstration rather than by screenshot. The
typography chapter runs a live variable weight ruler, the motion chapter runs a working
timeline editor with keyframe markers, the colour chapter runs a rotating palette wheel,
and the iconography chapter runs three counter scrolling icon marquees. Nothing that
explains a rule is a flat image.

The **governed asset and approval surface** sits behind a sign in, and the public
surface links to it at the foot of every chapter under `Brand Partner Toolkit` and
`Legal Branding Resources`. It holds the released asset library, the licence terms
attached to each asset, the usage request desk, the approval queue and the audit
record.

The coupling between the halves is the whole point. The chapter that tells you the mark
has two expressions is the same record that decides which of those two expressions an
agency is entitled to download. A chapter states rules with normative force, and those
rules are addressable: every published statement carries a stable identifier that a
request, a grant and an audit record can cite.

The state changing heart of the product is the usage request. A visitor reads; an
employee downloads what is generally released; a partner asks for what their engagement
does not already cover; a reviewer decides. An approval mints a time bounded grant whose
expiry is the earliest of the campaign end the requester asked for, the licence default
duration, any shorter window a reviewer imposed, and the end date of the requester's own
engagement. The engagement end always wins when it is the smallest, even when that makes
the grant expire the same afternoon, and the reviewer is shown that cap before deciding.

Three governance properties are load bearing and none of them can be faked with static
content. Availability is computed for one principal against one asset at the moment it
is asked for, and is never reused across principals. No path reaches a released binary
without passing the policy decision and writing the record. An audit record, once
written, cannot be altered or removed by anybody, including an owner.

This task builds the reading surface and the governed surface. It deliberately is not
the rest of the estate: no directory synchronisation from a corporate identity provider,
no upstream digital asset store, no content management vendor, no edge cache
invalidation, no design tool plugin, no webhook delivery to an agency's own systems, no
trademark register, no analytics property and no security log forwarding. It has no
comments, no likes, no messaging and no leaderboard.


### The information architecture, in one place

Two templates carry the whole public surface: the hub at `/`, and the chapter template at
each of the eight slugs. The governed surface adds the library, the asset detail, the
request desk, the approval queue and the admin console with its audit query. Chapters are
addressed by slug, and the slug is the join key between the reading surface and every
governed record. Ordering is content rather than code: the eight tiles render in a fixed
order held as a published field on the chapter record.

### The populations this product serves

The product has populations rather than users, and each sees a different subset of one
object graph. The personas this build implements are the anonymous visitor who reads the
nine public routes, the employee who downloads what is generally released, the agency
contributor whose downloads are bounded by the asset classes their engagement grants and
whose engagement has an end date, and the brand reviewer who decides requests and reads
the record. A press contact reads the press kit collection, and that collection exists in
the library; press is an application class rather than a fifth role in this build. The
wider estate also names a chapter author, a brand owner, a legal reviewer, a directory
principal and an integration principal, and none of those is built here: chapter authoring,
policy editing, asset release, directory synchronisation and token minting for a design
tool plugin are all out of scope, and this brief says so under the constraints below.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `visitor` | Open the hub and all eight chapter routes, read every chapter and work every demonstration, open the menu overlay, follow the outro and footer links, answer the cookie choice, land on the not found page | **Cannot sign in without a provisioned account, cannot open the library, an asset, a request, the queue or the audit record, cannot download any asset binary** |
| `employee` | Everything a visitor can do, plus browse the whole library, open any asset detail, download any asset whose availability is `Available`, raise a usage request against an asset that is `Request required` or `Restricted`, read and withdraw their own requests | **Cannot download a `Restricted` asset without a grant, cannot open the approval queue, cannot decide any request, cannot read another principal's request, cannot read the audit record** |
| `partner` | Everything an employee can do, except that downloads are limited to the asset classes their engagement grants, plus upload a proof where a condition requires one | **Cannot download outside their engagement's asset classes, cannot download after their engagement end date, cannot read another partner's request, cannot open the approval queue or the audit record** |
| `reviewer` | Everything an employee can do, plus open the approval queue, approve, reject or request changes on a stage assigned to them, attach a condition to an approval, and read the audit record | **Cannot decide a stage on a request they raised themselves, cannot decide a stage assigned to a different reviewer, cannot alter or delete an audit record, cannot edit chapter content** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a control
in the UI is not authorization: a direct API call from an `employee` session to any
`reviewer` only endpoint must be rejected by the server (an unauthorized request is
denied, not served), leaving the protected state unchanged.

Signup is closed. There is no self registration and no public signup endpoint; every
principal is provisioned ahead of time. The nine public routes, every demonstration on
them and the cookie choice all answer without an account. Signing in gates the library,
asset detail, downloads, requests, the queue and the audit record, and nothing else.

Five accounts are seeded, every one of them with the password `deku-demo-pw-2026`:

| Account | Role | Engagement |
|---|---|---|
| `employee@example.com` | `employee` | none, permanent |
| `partner@example.com` | `partner` | asset classes `spot_icon` and `pictogram`, ends `2026-11-30` |
| `partner2@example.com` | `partner` | asset class `photograph`, ends `2027-03-31` |
| `reviewer@example.com` | `reviewer` | none, permanent |
| `reviewer2@example.com` | `reviewer` | none, permanent |

A `partner` whose engagement end date has passed is refused a download and refused a
new request, with the engagement end date named in the refusal.

## Core features

### The routes

Nine public routes answer content, three reserved addresses answer not found, and six
addresses sit behind the sign in.

| Address | What it is | Who reaches it |
|---|---|---|
| `/` | the hub | anybody |
| `/framework` | the Framework chapter | anybody |
| `/voice-and-tone` | the Voice & Tone chapter | anybody |
| `/logo` | the Logo chapter | anybody |
| `/typography` | the Typography chapter | anybody |
| `/iconography` | the Iconography chapter | anybody |
| `/color` | the Colour chapter | anybody |
| `/imagery` | the Imagery chapter | anybody |
| `/motion` | the Motion chapter | anybody |
| `/2/`, `/as`, `/gs` | reserved, answer the not-found page at `404` | anybody |
| `/library` | the asset library | a signed in principal |
| `/asset/<asset-id>` | asset detail | a signed in principal |
| `/requests` | the caller's own usage requests | a signed in principal |
| `/requests/<request-id>` | one usage request | its requester, or a reviewer holding a stage of it |
| `/queue` | the approval queue | a `reviewer` only |
| `/admin/audit` | the audit query surface | a `reviewer` only |

Every page title is the route's own, and no two routes share one.

### The hub

`/` is a full viewport assembling tile grid with no chapter body. Eight tiles, one per
chapter, reach their final geometry only at full scroll of the hub route; before that
they are mid assembly, and the hub reads as a thing being built rather than a thing
that has appeared. The eight render in one fixed order that the hub, the menu overlay
and the outro all repeat identically: Framework, Voice & Tone, Logo, Typography,
Iconography, Colour, Imagery, Motion. That order is a stored field on the chapter
record rather than a fixed array in the page, because it is an editorial decision that
changes when the identity changes.

Each tile carries its chapter name, its own ground colour from the chapter palette and
its own legal type colour. A tile is a link to `/<chapter-slug>`.

### The eight chapters

Every chapter route is served from the chapter record addressed by slug. A chapter is a
vertical scroll document with four fixed parts: a vertical rail carrying the chapter
title and the scroll progress, an opening act, three to six teaching sections, and the
shared outro. There is no breadcrumb, no next chapter link and no in page table of
contents. Every lateral move goes through the menu overlay, and that constraint is
deliberate: a chapter is a document to be read through, and the only way out is the
same door you came in by.

| Slug | Chapter | Its demonstration |
|---|---|---|
| `framework` | Framework | the four published principles as a stepped diagram, each expandable to its normative statement |
| `voice-and-tone` | Voice & Tone | a tab control showing the same message written for the marketing, web and product surfaces |
| `logo` | Logo | the mark in both permitted expressions, pill labelled `Version A` and `Version B`, each with its own permitted applications and an anatomy drawing carrying the clear space multiple |
| `typography` | Typography | a live variable weight ruler that thickens the display face as it is dragged |
| `iconography` | Iconography | three counter scrolling marquees, one per icon class, each stating its drawn size |
| `color` | Colour | a rotating palette wheel carrying every published palette member name |
| `imagery` | Imagery | a stage that switches one subject between the declared image types |
| `motion` | Motion | a working timeline editor with keyframe markers that plays one reveal back frame by frame |

The four published framework principles are `Prioritize Simplicity`, `Deepen
Understanding`, `Instant Feedback` and `Subtle Playfulness`. They are published
constraints on other teams' work, not claims about a product, and each one is an
addressable statement.

The three icon classes carry published drawn sizes, stated as a rule rather than as a
suggestion: spot icons are square at one hundred and twenty units, pictograms are square
at sixty four units, and user interface icons are square at twenty four units. The
iconography chapter states all three, and the library refuses a released icon whose
declared dimensions do not match its class.

Every published statement in every chapter carries a stable statement identifier of the
form `<chapter-slug>.<section>.<n>`, for example `logo.expressions.2`. A usage request
cites the identifiers the requester relied on, and an audit record can name them years
later.

### The outro and the footer

Every one of the nine public routes ends with the same outro, splitting its onward links
three ways for three populations: `Brand Partner Toolkit`, `Legal Branding Resources`
and `Tessera Design`. The first two reach the governed surface; the third is an external
destination. A legal desk sitting beside the partner desk on every content route is a
governance fact, and the two must not be collapsed into one link.

The footer carries six destinations on every route: `Modern Slavery Statement`,
`Impressum`, `Cancel Contract`, `Cookies & CCPA preferences`, `Privacy` and `Terms`.
Every **internal link** on every public route resolves; none of them answers a client or
a server error.

### The cookie choice

A first time visitor is asked once about non essential **cookie** use, in a frame
carrying a `Do not sell or share my personal data to third parties` control alongside
accept and reject. The answer is recorded and survives a reload: a visitor who has
answered is never asked a second time. The `Cookies & CCPA preferences` footer link
reopens the choice so that an answer can be changed later. That frame is the only
element in the whole product permitted a drop shadow.

### The not found route

`/2/`, `/as` and `/gs` are reserved and answer with the product's own designed
**not-found** page at status `404`, carrying the chapter menu as the way back. So does
any other unknown address. A retired chapter address answers not found rather than
redirecting quietly to the hub: somebody has that link in a contract, and a guideline
address that silently becomes a different guideline is a governance failure. These slugs
are reserved against the chapter namespace and are refused at chapter creation time:
`library`, `asset`, `requests`, `queue`, `admin`, `studio`, `api`, `auth`, `health`,
`2`, `as`, `gs`.

### Sign in

There is no signup and no public registration form. A provisioned principal signs in
with an email address and a password and receives a bearer token. A session that expires
in the middle of filling in a request does not discard the draft: the principal signs in
again and everything already typed is still there.

### The asset library

`/library` is the asset browse surface and it is never empty. A principal holding no
permission on any asset still sees every asset, each one badged `Request required`,
because an empty library teaches nothing about what exists and makes it impossible to
tell whether you are asking for the right thing.

| Region | Contents |
|---|---|
| Filter rail | chapter, asset class, image type, delivery surface, licence class, and availability to the signed in principal |
| Result grid | asset cards carrying preview, name, class, format list, licence badge and availability badge |
| Availability badge | exactly one of `Available`, `Request required`, `Restricted` or `Retired` |
| Collections | curated sets, including the press kit and the partner toolkit |

Availability is computed for the signed in principal against each asset at the moment
the library is asked for, and an availability answer computed for one principal is never
served to another. A filter that excludes every result says which filter did it and
offers to clear that one filter rather than all of them.

The seven asset classes are `mark`, `spot_icon`, `pictogram`, `ui_icon`, `photograph`,
`typeface` and `motion_clip`.

### Asset detail

`/asset/<asset-id>` carries the preview rendered from the asset's own derivative and
never from the master, every released format with its dimensions and colour space, the
governing usage text from the chapter that owns it linked to its statement identifier,
the licence record, any condition a reviewer has attached, the chapter version this asset
was released alongside, the assets it supersedes, and a history of its releases,
retirements and licence changes drawn from the audit record and filtered to this asset.

The action is `Download`, or `Request use`, or a disabled control. **The reason a control
is disabled is always shown**, naming the asset class, the engagement or the retirement
that caused it. A governance tool that greys out a button without saying why generates a
support ticket and teaches people to route around it.

A download of a `Restricted` asset is refused unless the signed in principal holds an
active grant covering that asset, and the refusal names what is missing. A `Retired`
asset is never downloadable, and its detail page names its successor.

### The usage request desk

`/requests` lists the signed in principal's own requests, filterable by state, and
`/requests/<request-id>` is one request. A request carries the asset, the intended
application class, the territory, the campaign start and end dates, the requester's
grant, the decision chain, every comment and every condition.

A request records at submission time which chapter version was current, which statement
identifiers the requester cited, which policy version will evaluate it and which grants
the requester already held, so that the request stays self describing years later without
being joined against current state.

The nine request states are `draft`, `routed`, `under_review`, `changes_requested`,
`approved`, `granted`, `rejected`, `withdrawn` and `expired`. **A request always has
exactly one named holder, and every surface that shows a request shows it.** "With the
brand team" is not a holder, and the app never lets a request be in that condition.

| State | Holder | Exit |
|---|---|---|
| `draft` | the requester | submit |
| `routed` | the system | assignment, immediately |
| `under_review` | one named reviewer per open stage | a decision |
| `changes_requested` | the requester | resubmit, which returns the request to `routed` and re-evaluates policy, because the request has changed |
| `approved` | the system | grant minting |
| `granted` | terminal | the grant, with its conditions |
| `rejected` | terminal | a reason, always shown |
| `withdrawn` | terminal | the requester's own act |
| `expired` | terminal | an escalation record |

The six application classes are `internal`, `advertising`, `co_brand`, `merchandise`,
`partnership` and `press`.

### Routing and the approval queue

How many approval stages a request needs is decided from what is being asked for rather
than from a fixed chart:

| Rule | Effect |
|---|---|
| Application class is `co_brand`, `merchandise` or `partnership` | a legal stage is added, and it is always required |
| Asset class is `mark` | a second stage is added, and it must be held by a reviewer distinct from the first |
| Requested campaign window ends after the requester's engagement | the request is still accepted and the resulting grant will be capped; the reviewer is shown the cap before deciding |
| The requester is themselves a reviewer | they are never assigned their own request |
| No eligible reviewer exists | the request escalates to an owner immediately, and never sits unassigned |

`/queue` is the reviewers' side of the same workflow, open to `reviewer` only, ordered by
the deadline stored on the request. The decision panel offers approve, reject, request
changes and attach condition, and it explains why this request reached this reviewer.

A deadline is set at submission from the application class and stored on the request, so
that a later policy change does not silently move a live deadline.

### Conditions, proofs and grants

A condition is a first class record attached to an approval rather than a note in a
comment box, because it has to be checkable later. The six condition kinds are
`clear_space`, `no_recolour`, `attribution`, `proof_required`, `territory` and
`expiry_override`.

A `proof_required` condition holds the grant in a pending state: the grant is created
with its start date in the future and activates only when a named reviewer marks the
proof accepted. A proof upload is size capped, is type checked by inspecting the file's
own content rather than by trusting its name, and is never rendered while its scan state
is pending.

On the last approval the app mints exactly one grant. Its end date is the earliest of the
requested campaign end, the licence default duration, any `expiry_override` condition and
the requester's engagement end. Every grant carries the identifier of the request that
justified it, so that no permission exists without a recorded reason. Minting is keyed on
the request identifier: a retried approval yields the same grant, never a second one.

### Decisions are made once

A single stage of a request is decided exactly once, and this is the property the whole
product is built around.

- When two reviewers approve the same stage at the same instant, exactly one decision is
  recorded and the other is refused as a conflict that reports the winner's outcome. The
  two are never merged, and the refusal is a client error rather than a server error.
- An approved request mints exactly one grant and writes exactly one audit record per
  transition, however many times an approval is retried.
- When a request is withdrawn while a reviewer is deciding, withdrawal wins: the decision
  is refused and the reviewer is told why.
- When an asset is retired while a request against it is under review, that request is
  rejected automatically, the successor asset identifier is named, and the requester is
  invited to resubmit against it.
- The same request submitted twice in quick succession by a double click produces one
  submission, not two.

### The audit record

`/admin/audit` is open to `reviewer` only and answers a query over the audit record.
Every transition writes one record carrying the acting principal, the principal type, the
address the action came from, the request identifier, and the state before and the state
after.

A record, once written, is altered or removed by nobody. There is no endpoint, no control
and no role that edits or deletes one, and an attempt to do either is refused. Proving
years later who was permitted to use what and when is the obligation this surface exists
to discharge.

### Forms refuse a robot

Every form on the public surface and on the request desk refuses an automated
submission. A submission that fills the unattended decoy field is refused, and so is the
same form submitted **repeatedly** in quick succession from one origin. A refused
submission writes nothing. Every form also rejects invalid input inline, naming the field
at fault, and writes nothing when it does.

## User flow

**A visitor reads a chapter.** A visitor opens `/` and the eight tiles assemble as the
hub is scrolled, reaching their final geometry at full scroll. The cookie frame asks
once about non essential cookie use and the answer is remembered. The visitor opens the
menu overlay, picks Typography, and lands on `/typography`. The vertical rail carries
the chapter title and fills as the page advances. The variable weight ruler thickens the
display face as it is dragged. At the foot of the chapter the outro offers the partner
toolkit, the legal resources and the design publication. The visitor follows the partner
toolkit link, is not signed in, and is asked to sign in rather than shown an empty
library.

**An employee downloads a released asset.** The employee signs in with
`employee@example.com` and opens `/library`. Every asset is visible and each carries
its availability badge. The employee filters by chapter to Logo, opens the mark, reads
the licence record and the governing statement, and downloads the format they need
because the asset is badged `Available`. The download is recorded against them.

**A partner is refused, then asks.** The partner signs in with
`partner@example.com`, whose engagement grants `spot_icon` and `pictogram` and ends
on `2026-11-30`. They open the mark, which is badged `Restricted`, and the download
control is disabled with the reason stated: the mark is outside the asset classes their
engagement grants. They choose `Request use` instead and fill in the application class
`co_brand`, the territory, and a campaign running to `2027-01-31`. The desk warns them
before submission that the campaign end falls after their engagement ends, so any grant
will be capped at the engagement end date. They submit.

**The request is routed.** Because the application class is `co_brand` a legal stage is
added, and because the asset class is `mark` a second brand stage is added that must be
held by a distinct reviewer. The request leaves `draft`, passes through `routed`, and
arrives at `under_review` with one named reviewer holding each open stage. The requester
sees both names on `/requests/<request-id>`.

**A reviewer decides.** The reviewer signs in with `reviewer@example.com` and opens
`/queue`, which is ordered by the deadline stored on each request. The decision panel
explains that this request reached them because the asset class is `mark`, and shows the
cap that will be applied to the grant. They approve and attach a `clear_space` condition
and a `no_recolour` condition. The second reviewer signs in with
`reviewer2@example.com` and approves the legal stage. On that last approval the app
mints exactly one grant, ends it at the engagement end date rather than the campaign end
date, attaches both conditions, moves the request to `granted` and writes an audit
record. The partner can now download the mark, and only the mark, and only until the
engagement ends.

**Two reviewers collide.** Two reviewers approve the same open stage at the same instant.
Exactly one decision is recorded. The other is refused as a conflict and is shown the
outcome that won. No second grant is minted, no second audit record is written, and the
request advances once.

**A reviewer may not decide their own request.** A reviewer raises a request of their
own, and that request is never assigned to them. If they call the decision endpoint for
it directly, the server refuses and the request is unchanged.

**An employee is refused the queue.** The employee calls the queue endpoint and the
decision endpoint directly with their own bearer token. Both are refused, and the
request they tried to decide is unchanged.

**A record cannot be unwritten.** A reviewer opens `/admin/audit`, queries by request
identifier, and reads the whole decision history: who acted, from where, and what the
state was before and after. They attempt to remove one and are refused. The record still
answers the same query afterwards.

**An unknown address.** Anybody opens `/gs`, or any other address that is not a route,
and lands on the product's own designed not-found page at status `404`, with the chapter
menu offering the way back.

## UI/UX notes

The product is loud in structure and quiet in decoration. There is no photography in the
chrome, no gradient anywhere except a single conic sweep on one button, and exactly one
drop shadow in the whole product, which belongs to the consent frame. A builder arriving
from a marketing reference will want to add photography, cards, shadows and rounded
containers; do not.

**What carries the design instead.** Hairline construction lines in a light, vivid blue,
drawn as real elements rather than as background decoration, sitting over and under
content and moving with it. Full bleed planes of unmodulated brand colour that occupy
whole grid cells, with the chapter's own colour as the page ground. Type at two extremes,
a small annotation face used relentlessly and display type used sparingly, with almost
nothing in between. Demonstrations rather than screenshots: every explanatory figure is a
working component.

**The palette, described rather than specified.** The core is three colours: a mid, vivid
blue that carries the brand and every active state, a warm near-white ground named
`Coconut`, and a warm near-black ground named `Graphite` used for inverted sections. Two
further blues exist and are not interchangeable with the core: a lighter one that is the
only hover destination in the product, and a slightly deeper one for the pressed and
focus-visible states. The accent set is eighteen members and every one has a published
name that the colour chapter must show: `Azalea`, `Pink`, `Crimson`, `Sunset`, `Rust`,
`Tangerine`, `Gold`, `Vivid Amber`, `Canopy`, `Lime`, `Ocean`, `Zen`, `Navy`, `Cloud`,
`Plum`, `Orchid` and `Coconut`, plus a construction hairline member. Across those accents
the families run from a deep, vivid red and a mid, vivid magenta through a deep, vivid
orange and a light, vivid amber to a mid, vivid lime, a deep, muted teal, a deep, vivid
cyan and a deep, soft violet. Greys are an eight step ramp with numeric names, and four
further neutral surfaces sit alongside them as rules and grounds rather than as text. The
whole system contains exactly four transparency values plus three lighter ones for dark
grounds and two for the consent scrim.

**The pairing table is declared, not calculated.** Eight identity grounds each have
exactly one legal type colour, and a builder must look the pairing up rather than derive
a foreground from a background by luminance. The eight pairs run: a light, vivid blue
ground carrying a deep, muted indigo type; a light, vivid cyan ground carrying a deep,
soft cyan; a mid, vivid lime ground carrying a deep, muted teal; a light, vivid orange
ground carrying a deep, soft orange; a light, soft red ground carrying a mid, soft
magenta; a light, soft violet ground carrying a deep, muted violet; a mid, vivid orange
ground carrying a deep, soft red; and a light, vivid amber ground carrying a deep, soft
orange. Never recolour one half of a pair without the other.

**Type.** Two families carry everything: a commissioned display face, `Ridge Grotesk`,
whose variable cut `TS Ridge Grotesk` drives the typography chapter's weight ruler, and a
licensed text face, `Basis Grotesk`, drawn by the foundry `Ridge Type`. The rendered
scale is dominated by one small annotation size, which accounts for more rendered text
than every other size combined, because the product annotates itself constantly and
reserves large display type for a handful of scroll driven headlines. Set the page grid
as a fixed outer margin with a wide cap, so that on a large display the columns keep
growing rather than centring inside a narrow measure.

**Motion.** Motion is considered rather than decorative: entrances and exits are eased
over short durations, the named heading reveal fills a headline word by word as it enters
the viewport, and three global elements are scrubbed by scroll position rather than
played on a timer. Nothing in the governed surface is scroll scrubbed, because a working
tool must not make a reviewer wait for an animation. Never declare a blanket transition
on every property; name the properties that move. Honour the reduced motion preference
everywhere: when it is set, the scrubbed elements take their final state immediately, the
heading reveal shows the whole headline at once, and only the focus ring still animates.

**Accessibility.** Body text meets the contrast bar against its ground in every one of
the eight identity pairings, which is one reason the pairing table is declared rather
than computed. Every control is reachable and operable by keyboard alone, in a visible
order, and the focus ring is always drawn and never suppressed. Every icon only control
carries a text label for assistive technology, every content image carries alternative
text, and every decorative image declares itself decorative. Meaning is never carried by
colour alone: an availability badge states its word as well as its colour, and a request
state is named rather than merely tinted. Touch targets are comfortably sized on a touch
surface.

**Responsive behaviour.** The layout answers at a narrow phone width, at tablet width and
at desktop width, and at the narrow width nothing overflows sideways and every navigation
target stays reachable. The hub tiles restack into a single column and still assemble on
scroll. A chapter drops its vertical rail to a slim progress indicator. The library's
filter rail collapses into a disclosure above the result grid, and the queue's decision
panel becomes a full width sheet. Tables that cannot compress, such as the audit query
result, scroll horizontally inside their own container rather than widening the page.

**The reader owns the scroll.** There is no scroll hijacking and no smooth-scroll
interception anywhere in the product: the page advances at whatever rate the reader
drives it, and the scrubbed elements follow that position rather than animating on their
own schedule. Never intercept a wheel, a key or a touch drag to run a scripted journey.

**Density.** The reading surface is spacious and unhurried; the governed surface is
dense, so that a full approval queue fits one screen without scrolling. Those are two
different reading experiences sharing one design system, and the difference is
deliberate.

## Technical requirements

- The app is a server rendered or single page web application backed by the PostgreSQL
  database reachable at `DATABASE_URL`, and by the MinIO object store reachable at
  `STORAGE_ENDPOINT` with the bucket named in `STORAGE_BUCKET`. Both are already running.
- Asset masters, asset derivatives and uploaded proofs are objects in the MinIO store.
  **A protected object is never publicly readable.** An anonymous request for the object
  address of a `Restricted` or `Retired` asset is refused, and a download reaches the
  caller only after the app has decided that this principal may have this asset now.
- Every response carries the standard **security header** set, including a strict
  transport policy, a nosniff content type policy, a frame ancestry policy and a
  referrer policy.
- Authentication is an email address and a password, and a successful sign in returns a
  bearer token that authorises every later call. There is no signup endpoint.
- Authorization is decided on the server for every request that changes state, and for
  every read of a request, a queue or an audit record. A decision is made against the
  signed in principal, never against a value the client supplies.
- Availability of an asset to a principal is decided at the moment it is asked for. An
  availability answer computed for one principal is never returned to another, and no
  cached copy of a per principal answer is served across principals.
- A stage of a usage request accepts exactly one decision. Two decisions arriving for one
  open stage at the same instant produce exactly one recorded decision and exactly one
  advance of the request; the loser is answered as a conflict that names the outcome that
  won, and no state is left half written.
- Grant minting is idempotent against the request identifier. Approving an already
  approved request answers with the grant that already exists, and never creates a second
  grant, a second condition set or a second audit record.
- An audit record is append only. The app exposes no way to update or delete one, and an
  attempt is refused rather than silently ignored.
- Deadlines are stored on the request when it is submitted, so a later change to policy
  does not move a deadline that is already running.
- A proof upload is accepted only up to a size cap, and its type is decided by inspecting
  the content of the file rather than by trusting the name it arrives under. A proof whose
  scan state is still pending is never rendered.
- Every form refuses an automated submission, both by the unattended decoy field and by
  the same form arriving repeatedly in quick succession from one origin.
- The HTTP API answers with JSON. A successful call returns the named resource; an invalid
  or unauthorized call is answered as a client error, never as a server error and never as
  a silent success.
- Times are stored and returned in UTC. Money does not appear in this product.
- The reading surface keeps working when the governed surface cannot answer: all nine
  public routes still render, and the outro links state that the toolkit is temporarily
  unavailable rather than failing the page.


### API conventions and validation

- Every collection endpoint answers a top-level JSON array, and every single resource
  answers a JSON object. Field names are lower snake case and are stable once published.
- Every list that can grow without bound is paginated, and a page is requested by a cursor
  rather than by an offset, so that a record inserted while a reader is paging does not
  make them skip or repeat a row.
- Validation is decided on the server for every field. A rejected body names the field at
  fault and the reason, writes nothing, and answers as a client error. Validation of a
  date range checks that the campaign start is not after the campaign end, that a
  territory is one of the published set, and that every cited statement identifier exists
  in the chapter version being cited.
- A rate limit applies per principal and per address to sign in, to request submission and
  to proof upload. A caller over the limit is refused with a stated retry moment and
  nothing is written. This is the same protection that refuses an automated submission.
- An identifier that appears in a response is opaque to the client: a client never
  constructs one, and never relies on it being sequential.

### Concurrency, idempotency and time

- Two callers acting on one open stage produce exactly one recorded decision. The winner
  advances the request; the loser is answered as a conflict naming the outcome that won.
  Nothing is left half written, and no partial state is visible to a third reader.
- Every state changing endpoint is safe to retry. A retried request submission, a retried
  decision, a retried proof acceptance and a retried grant minting each yield the outcome
  that already exists rather than a second record. Idempotency holds across the boundary
  between the app and its store, so a caller who never sees the answer and tries again is
  not punished for it.
- The app reads one clock. Every stored moment is UTC, every returned moment is UTC, and
  no deadline, expiry or audit ordering depends on a client supplied time.
- A grant's expiry is decided at the moment a download is asked for, not by a scheduled
  sweep, so an expired grant is refused the instant it expires rather than at the next
  run of a job.

### Directory, groups and attributes

- A principal reaches the app already provisioned. This build seeds the principals
  directly; there is no directory synchronisation to run and no external source to
  reconcile against.
- A principal belongs to zero or more groups, and a group is the unit an entitlement is
  attached to. The partner engagement in the roles table is exactly this: a group carrying
  the asset classes it grants and the date it ends.
- A principal also carries attributes, and an attribute participates in the decision
  alongside the role and the group. The attributes this build needs are the engagement end
  date and the granted asset classes.
- A decision is therefore made from the role, the groups, the attributes and the asset,
  together, and the surfaces explain which of them caused the answer.

### Data governance, retention and deletion

- An audit record is never deleted and never redacted. It is the one record with no
  retention limit.
- A proof is purged after its retention period, and its checksum and its scan state are
  retained after the file itself has gone, so that the record of what was reviewed
  survives the thing that was reviewed.
- A page view and a consent choice carry no principal identity beyond what the reader
  supplied, and a consent choice is private to the reader who made it.
- A download record is retained for the life of the audit record it belongs to.
- Deletion of a principal is not a function of this app. Where a record must stop being
  reachable, it is marked rather than removed, and the audit record that names it is
  unaffected.

### Performance and resilience

- The nine public routes answer quickly enough to read without waiting, and a chapter's
  demonstrations do not block its text from appearing.
- The library answers a filtered query and the queue answers a reviewer's own stages
  without the reader noticing a delay, at the seeded data scale and an order of magnitude
  above it.
- Bulk selection in the library is decided per asset, so a bulk download of ten assets
  makes ten decisions and may release some and refuse others, naming each refusal.
- When the object store cannot be reached, the library and the asset detail still render
  from the database, previews fall back to a placeholder, and a download states that the
  store is temporarily unavailable. The chapters are unaffected.
- When the database cannot be reached, the app answers a server error on the governed
  surface only; the reading surface continues to serve all nine public routes.
- A failure in one dependency never cascades into a failure of an unrelated surface, and
  the dependency failure matrix above is the whole of it: database, object store, neither.

### Observability

- The app writes a structured event for every sign in, every decision, every grant minted,
  every download released and every refusal, each carrying the acting principal and the
  address it came from.
- A health endpoint reports readiness, and reports the database and the object store
  separately, so that a degraded surface can be told from a dead one.
- An operational alert is raised in the app's own records when a request escalates for
  want of an eligible reviewer, when a rate limit is breached repeatedly from one origin,
  and when a proof is quarantined. An alert is a record a reviewer can read, not a message
  that leaves the app.
- A request that breaches its deadline is recorded as a breach, and the breach is itself
  an audit event.

### Security posture

- No secret appears in any response, in any page source, or in any client bundle. The app
  reads every credential from its environment.
- Every upload is checked by content rather than by name, is size capped, is stored under a
  name the app generates rather than the name it arrived under, and is never served from
  the origin that accepted it.
- Every query against the store is parameterised, and no user supplied string is ever
  interpreted as code, as markup or as a serialised object.
- Every protected object address is unguessable and is released only after a decision.
  An anonymous caller holding an object address for a restricted asset is refused.
- Authorization is decided from the session, never from a role, a principal identifier or
  an entitlement the client supplies in a body, a query or a header.

### Module architecture

The app is built in layers, and the layering is what keeps the two halves from leaking
into one another: a reading layer that serves the nine public routes from published
content only, a policy layer that owns every decision about who may have what, a workflow
layer that owns request state and stage decisions, a distribution layer that releases
binaries, and a record layer that writes the audit. The reading layer holds no per
principal state and reaches nothing in the distribution layer. Each layer is one module
with a named boundary, and a decision is made in exactly one of them.


### Anti-abuse, injection and detection

- Anti-abuse protection covers sign in, request submission, proof upload and every public
  form. Rate limiting is per principal and per origin address, and a caller over the limit
  is refused without anything being written.
- No user supplied string is ever interpreted as code or as markup, and no user supplied
  payload is ever deserialised into an object the app then trusts. An upload is treated as
  bytes, never as an instruction. Injection through a query, a body, a header, a filename
  or a field name is refused by treating every one of them as data.
- Detection is part of the product rather than an operations afterthought: a refused sign
  in, a rate limit breach, a quarantined proof, a download refusal and an attempt to reach
  a protected object address without a decision are each recorded as events a reviewer can
  query. A pattern of them from one origin raises the operational alert described above.
- A best effort is not enough on the refusal path: a refusal is a recorded outcome, not a
  silent no-op, and every refusal names its reason.

### Step-up authentication for sensitive acts

Three acts require the principal to re-enter their password even though their session is
still valid: deciding a stage, accepting a proof, and querying the audit record. A
step-up is bounded in time, and once it lapses the next sensitive act asks again. There is
no break-glass path that bypasses a decision or writes without a record: an emergency
override is not a feature of this product, because a governance tool with an unrecorded
escape hatch cannot answer the question it exists to answer.

### Row level enforcement

Every read of a request, a grant, a proof, a download or an audit record is narrowed to
what the calling principal is entitled to see, and the narrowing happens where the data is
read rather than in the surface that displays it. A partner asking for the whole request
collection receives their own requests only, and an employee asking for the audit
collection receives a refusal. The entities listed in the data model each state whose rows
a principal may see, and no surface is trusted to filter on the layer's behalf.

### Search and discovery

The library is searchable by asset name, by asset class, by the chapter that governs an
asset and by licence class, and the chapters are searchable by statement text. What is
searched is published content and asset metadata only: a request, a grant, a proof and an
audit record are never reachable through search, only through their own surfaces. A search
answer is narrowed to the calling principal exactly as a list is, so a search never
reveals the existence of something a list would have hidden.

### Propagation and consistency

A change made on the governed surface is visible to its own reader immediately. Propagation
to another reader's view is bounded and small, and no surface ever shows a decision that
has not been recorded. Where a reader could observe two related facts mid change, the app
shows the pair as it was before the change or as it is after it, never a mixture: a request
never appears granted while its grant is absent, and a grant never appears without the
request that justified it.


### The decision rules that admit no exception

- **Default is deny.** A principal who matches no entitlement is refused. An explicit deny
  beats any allow, so a revoked grant or a prohibited application class cannot be
  overridden by a broader group membership that would otherwise permit it.
- **Decision correctness is absolute.** There is no tolerance for a wrong allow: releasing
  a binary to a principal who should not have had it is the one failure this product exists
  to prevent, and it is worse than refusing somebody who should have been allowed.
- **Audit completeness is absolute.** A change that cannot be recorded does not happen: if
  the record cannot be written, the change is refused and nothing is left behind.
- **A licence change is never retroactive.** Changing a licence's terms neither voids nor
  extends a grant that already exists. Existing grants keep the terms they were minted
  under, and the change applies to grants minted after it.
- **An unpublished chapter is confidential.** A draft chapter version is readable only by a
  reviewer, and never reachable on the public surface, because an early disclosure leaks a
  rebrand or a launch.
- **The principal list is not enumerable.** Sign in answers a failed attempt in the same
  shape and the same time whether or not the address exists, and no surface lists the
  principals or the partner organisations, because that list is competitive intelligence.

## Data model

The database holds the following records. Field names are the app's own to choose unless
this brief names one; the relationships and the rules below are not.

| Record | Holds | Rules |
|---|---|---|
| `principal` | email address, password, role, display name, and for a partner the engagement asset classes and engagement end date | role is one of `employee`, `partner` or `reviewer`; the email address is unique; there is no self registration |
| `chapter` | slug, title, display order, ground colour name, type colour name, published state and current version | slug is unique and is the join key between the reading surface and every governed record; a slug from the reserved list is refused |
| `chapter_version` | the chapter it belongs to, its statements and the time it was published | a request names the version that was current when it was submitted |
| `statement` | its chapter version, its stable statement identifier and its normative text | the identifier is stable across versions and is what a request, a grant and an audit record cite |
| `asset` | name, asset class, the chapter that governs it, licence, availability class, declared dimensions, format list, master object address, derivative object address and successor | asset class is one of the seven named classes; availability class is one of `Available`, `Request required`, `Restricted` or `Retired`; a `Retired` asset names its successor; an icon whose declared dimensions do not match its class is refused |
| `licence` | licence class, permitted application classes, prohibited application classes, territory, default duration and whether modification is permitted | a licence is attached to an asset and is what a reviewer reads before deciding |
| `usage_request` | requester, asset, application class, territory, campaign start, campaign end, state, current holder, deadline, the chapter version, the cited statement identifiers, the policy version and the grants the requester already held | state is one of the nine named states; the requester is never the holder of a review stage of their own request; a request in any state has exactly one named holder |
| `request_stage` | its request, the stage kind, the reviewer holding it, its outcome and the time it was decided | a stage accepts exactly one decision; the two stages of a `mark` request are held by two distinct reviewers; a reviewer never holds a stage of their own request |
| `condition` | its request stage, its kind and its text | kind is one of the six named kinds; a condition survives as a record and is not a comment |
| `grant` | its principal, its asset, the request that justified it, its start date, its end date and its conditions | exactly one grant exists per approved request; the end date is the earliest of campaign end, licence default duration, any `expiry_override` condition and the principal's engagement end |
| `proof` | its condition, its object address, its checksum and its scan state | scan state is one of `pending`, `clean` or `quarantined`; a pending proof is never rendered; accepting a proof activates the grant that was waiting on it |
| `audit_record` | acting principal, principal type, the address the action came from, the request identifier, the state before, the state after and the time | append only; no path updates or deletes one; exactly one record is written per transition |
| `download` | the principal, the asset, the grant relied on and the time | written whenever a binary is released, so that every use of the identity is recorded |
| `consent_choice` | the visitor it belongs to, the answer and the time | an answer survives a reload and is asked for only once |
| `page_view` | the route and the time | recorded for a public route view |

**Seed data.** The eight chapters are seeded with their slugs, titles and display order
in the fixed order Framework, Voice & Tone, Logo, Typography, Iconography, Colour,
Imagery and Motion. At least one asset exists per asset class. The mark is seeded in both
expressions, `Version A` and `Version B`, as `Restricted` assets of class `mark` governed
by the `logo` chapter. At least one `spot_icon` and one `pictogram` are seeded
`Available`. At least one `photograph` is seeded `Request required`. One asset is seeded
`Retired` and names its successor. Every asset carries a licence. The five accounts of
the roles table are seeded with the stated engagements.


**The asset lifecycle.** An asset moves through a fixed lifecycle and its availability
class is the visible face of where it has reached: drafted, released, superseded and
retired. Releasing an asset is what makes it reachable at all; superseding it points a
successor at it; retiring it stops every download and leaves the record intact. A chapter
version cannot be published until the assets it references have been released, which is
the coupling between the two halves of the product.

**Variants.** One asset holds many variants, and a variant is a released derivative rather
than a separate asset: the same mark in several formats, colour spaces and declared
dimensions, each listed on the asset detail. A variant is never licensed separately from
its asset, and a grant covers an asset and therefore all of its released variants.

**Tamper evidence.** The audit record carries tamper evidence: each record is written with
a digest that covers its own fields and the digest of the record before it, so that a
removed or edited record is detectable by reading the chain rather than by trusting that
nobody touched it. The app exposes the verification as a read, and a broken chain is
reported rather than hidden.

**Temporal data.** A request names the chapter version and the policy version that applied
when it was submitted, and a grant names the request that justified it, so that a reader
years later can reconstruct what the rules were without any of them still being current.

## Front-end specification

This section carries the visual and interaction material in full. Everything here is
described rather than valued: no exact pixel, position, size, colour code, easing name or
parameter value is given, because the builder is expected to design against these
descriptions rather than transcribe numbers. Named typefaces and named technologies are
the exception and are given exactly.

### Global chrome

The chrome is the same on all nine public routes and is built from seven parts.

| Part | Behaviour |
|---|---|
| The menu button | fixed in a corner, always reachable, carrying the brand colour; it is the only way to move laterally between chapters, and it is the single element in the product allowed a conic gradient sweep |
| The vertical rail | a slim column carrying the chapter title set sideways, non interactive, filling as a scroll progress indicator; absent on the hub |
| The menu overlay | opens over the current route carrying the same eight chapters in the same fixed order plus the hub, and closes back to where it was opened from |
| The scroll affordance | a small persistent hint at the first viewport of a chapter that there is more below, which retires once the reader has scrolled |
| The partner drawer | the panel the outro's partner and legal links open, which is the doorway from the reading surface to the governed surface |
| The outro | the shared closing block on every route, splitting three ways to the partner toolkit, the legal resources and the design publication |
| The footer | six legal and preference destinations on every route |
| The consent frame | the cookie and personal data choice, asked once, the only element carrying a drop shadow |

### The demonstration canvas

The single largest risk in this build, and the thing that makes the product what it is:
**every explanatory figure is a working component and none of them is an image.** A
screenshot of a slider is a failure even when it looks identical.

Each demonstration shares one anatomy: a stage with its own subtle overlay ground inside
the section, the live component on that stage, an annotation label set in the small
annotation face, and construction hairlines drawn as real elements. Several carry a
cursor tag: a small floating label naming a person and their role, following the pointer
across the stage, used to show who is speaking or acting. The tag names and roles are
content, not decoration, and include a type designer, a type director, a foundry chief
and a race driver.

A demonstration has four stage states: idle before it is reached, active while it is in
the viewport, engaged while the reader is manipulating it, and settled once released.
Every one of them is keyboard operable, and every one of them has a still, correct
appearance when the reduced motion preference is set.

### The hub route

The hub has three acts as it is scrolled. In the first the eight tiles are scattered and
incomplete. In the second they travel toward their places while the rail transforms
alongside them. In the third they reach their final geometry, which they hold at full
scroll. The tile palette is drawn from the accent set, one ground and one legal type
colour per tile, looked up from the pairing table and never computed. The hub's states
are the three acts plus a reduced motion state in which the tiles are simply in their
final geometry from the first frame.

### The chapter template

A chapter runs in a fixed vertical order: the opening act, a ground sequence that changes
the page ground as the reader descends, three to six teaching sections, and the shared
outro. A teaching section has a contract: a headline, a normative statement, one live
demonstration and an annotation. The shared states across every chapter are the first
viewport, mid scroll, fully read, and reduced motion.

### Chapter: Framework

Shape: an opening messy work headline, a file grid, a sketch curve diagram, a pillar
carousel, a strategy carousel and a closing. The messy work headline is a display line
that arrives word by word. The file grid shows work in progress artefacts as labelled
tiles. The sketch curve diagram draws a rough curve as a real element rather than as a
picture. The pillar carousel steps through the four published principles, `Prioritize
Simplicity`, `Deepen Understanding`, `Instant Feedback` and `Subtle Playfulness`, each
expandable to its normative statement. The strategy carousel closes the chapter.

### Chapter: Voice & Tone

Shape: a quotation opening, a consistency headline, a pillar carousel, a surface tab
switcher and an annotated example canvas. The quotation opening carries an epigraph with
its attribution. The surface tab switcher is the important one: it shows the same message
written three ways under the labels `Marketing`, `Web` and `Product`, because three
delivery surfaces with divergent rules is an organisational fact rather than a
presentation choice. The annotated example canvas marks up a real piece of copy with
construction hairlines and annotation labels.

### Chapter: Logo

Shape: a vertex assembly, the mark built as four clipped squares, the two expressions,
the lock anatomy diagram, an aspect ratio switcher and a plane composition. The vertex
assembly draws the mark from its corner points as the section is entered. The two
expressions are pill labelled `Version A` and `Version B`, each stating its own permitted
applications, and they are the two records the governed surface decides between. The lock
anatomy diagram carries the clear space multiple as a drawn measurement with annotation
labels rather than as a number in prose. The aspect ratio switcher shows the mark holding
its construction across shapes. The plane composition places the mark white inside a full
bleed plane of brand colour.

### Chapter: Typography

Shape: a specimen opening, a ruler, a typewriter, the weight ruler and specimen clips.
The two families are named exactly: the commissioned display face is `Ridge Grotesk`,
its variable cut is `TS Ridge Grotesk`, the licensed text face is `Basis Grotesk`, and the
foundry that drew the display face is `Ridge Type`. The ruler measures the specimen as a
drawn element. The typewriter sets a line character by character. The weight ruler is the
chapter's defining demonstration: dragging it drives the variable axis of the display
face and the specimen thickens live under the reader's hand. The specimen clips show the
face at its extremes, a small annotation size and a large display size, with almost
nothing between them.

### Chapter: Iconography

Shape: a folder stack, an interleaved headline, the triple marquee, the user interface
icon row and the system statements. The folder stack opens to reveal the icon classes.
The interleaved headline sets two lines that pass through one another. The triple marquee
is three counter scrolling rows, one per icon class, each row stating the size its class
is drawn at: spot icons square at one hundred and twenty units, pictograms square at
sixty four units, user interface icons square at twenty four units. The icon row shows
the interface set at its own size. The system statements close with the drawing rules:
consistent stroke, consistent corner treatment, no gradient, no shadow, and one optical
weight across a class.

### Chapter: Colour

Shape: a word fill headline, the three categories, the swatch table, the palette wheel
and a surface three up. The word fill headline is the product's named reveal: a display
headline whose words fill with colour one at a time as the line enters the viewport. The
three categories are named on the chapter as `Core`, `Accents` and `Greys`. The swatch
table lists every published palette member by name. The palette wheel rotates through the
accent set as a live component. The surface three up repeats the same guidance three ways
under `Marketing`, `Web` and `Product`.

### Chapter: Imagery

Shape: a card stack, four type panels, a customer file panel and a closing statement. The
card stack shuffles subjects. The four type panels each demonstrate one declared image
type with one subject, so the reader sees the same thing treated four ways. The customer
file panel is the governance panel: it states that a customer's own file is an asset class
with consent attached, and that a withdrawn consent is an immediate refusal rather than a
queued review.

### Chapter: Motion

Shape: a word fill headline, a selection apparatus, the timeline editor, the curve editor,
the principles and a three line closing statement. The timeline editor is the chapter's
defining demonstration: a working editor with keyframe markers that plays one reveal back
frame by frame under the reader's control, scrubbable both ways. The curve editor lets the
reader shape an easing curve by dragging its handles and see the result applied
immediately. The principles state the motion language in words: short and considered,
entrances and exits eased, nothing gratuitous, and the reduced motion preference always
honoured.

### The not found route

Shape: the product's own designed page, not a framework default. Contents: a short
statement that the address is not a guideline, the chapter menu as the way back, and the
same footer as every other route. It carries the one measured hover in the product, the
lighter blue hover destination on its link back. It answers at status `404` on every
reserved and unknown address.

### The governed surface, visually

The governed surface shares the design system and the component library and takes none of
the scroll machinery. It is dense, it is fast, and nothing in it is scroll scrubbed. Its
four rooms are the library, the asset detail, the request desk with the approval queue,
and the admin console with its audit query. Region layouts are given in `## Core
features`; visually, the rules are: the filter rail is a quiet column of grouped
controls, the result grid is a plain card grid with the badge as the loudest element on
each card, the decision panel is the densest surface in the product and fits a whole
decision without scrolling, and the audit query result is a table that scrolls inside its
own container rather than widening the page.

### States every surface owes

| State | Requirement |
|---|---|
| Empty | the library is never empty; every other list states what would fill it and what to do next |
| No results after filtering | names the filter that excluded everything and offers to clear that one filter |
| Loading | a quiet placeholder that holds the layout, never a spinner that shifts the page |
| Error | states what failed and what the reader can do, and never blames the reader |
| Unauthorized | asks the reader to sign in rather than showing an empty surface |
| Session expired mid action | preserves what was typed, re-authenticates, and resumes; nothing is silently discarded |
| Reduced motion | every scrubbed element takes its final state at once, and only the focus ring animates |
| Governed surface unavailable | the nine public routes still render and the outro says the toolkit is temporarily unavailable |

### Internationalisation and copy

All copy is English. Text expansion must not break a layout: every label, badge and
button holds its shape when its text grows. Dates are shown unambiguously and stored in
UTC. The copy deck is the product's own: chapter headlines, normative statements,
annotation labels, cursor tag names and roles, palette member names, the four framework
principles, the six footer destinations and the three outro destinations are all content
the build must carry.

### Stacking and layering on screen

The product has a strict front to back order and nothing may jump it: the page ground sits
behind everything, then full bleed colour planes, then content, then construction
hairlines which deliberately sit both over and under content, then the vertical rail, then
the menu button, then the menu overlay, and finally the consent frame in front of all of
it. A demonstration's own stage layers inside the content band and never above the rail.
No element is lifted above the overlay, and no element is given a shadow to imply depth;
depth is carried by order and by the planes.

### Small chrome pieces, named

| Piece | What it is |
|---|---|
| Annotation label | the small label in the annotation face that names a part of a demonstration; the most repeated piece of type in the product |
| Construction hairline | a faint rule in a light, vivid blue drawn as a real element, used to show alignment and measurement |
| Cursor tag | a floating chip that follows the pointer across a demonstration stage, naming a person and their role |
| Coordinate readout | a small live readout on a demonstration that reports the value the reader is currently setting, such as the weight the ruler is at |
| Pill label | the small capsule that marks the mark's two expressions as `Version A` and `Version B` |
| Availability badge | the chip on an asset card stating one of the four availability words |
| Chevron | the small directional glyph used on a disclosure and on a carousel step; the only directional glyph in the product |
| Progress fill | the fill that advances inside the vertical rail as a chapter is read |
| Scroll hint | the small persistent affordance at the first viewport of a chapter that retires once the reader scrolls |

### Glyphs and media

The icon system is three classes and a chrome set. A glyph is drawn rather than
photographed, carries one optical weight across its class, keeps one stroke treatment and
one corner treatment, and takes no gradient and no shadow. The chrome glyphs are the menu
mark, the close mark, the chevron and the external link mark. Demonstration glyphs are the
ones a chapter animates, and they are the same drawings at the same sizes.

Media in this product is limited and deliberate. There is no photography in the chrome. A
photograph appears only inside the imagery chapter's type panels and inside an asset
preview. A motion clip asset carries a still poster frame and plays only when a reader asks
it to. No audio exists anywhere in the product, and no video autoplays.

Where a real brand binary would sit, this build substitutes a generated placeholder that
holds the right shape, the right dimensions and the right format list, so that every
dimensional contract and every format list is exercised without shipping a real asset. A
placeholder is visibly a placeholder and is never presented as final artwork. Grain,
texture and any compiled animation scene are out of scope: a texture is a flat plane here,
and the wordmark is set from the named display face rather than supplied as a drawn file.

### The credit line

The product credits its makers on the hub outro: the owning in house function is
`Tessera Brand Studio`, the external collaborator is `Meridian Studio`, and ten named
internal contributors are listed alongside them. An external party credited inside the
identity is the normal case here rather than the exception, and the credit line is content
the build carries rather than decoration.

### Launch readiness

Before the product is considered launched, every public route carries its own title, the
not-found page answers on every reserved address, every internal link resolves, the
consent choice is asked once and remembered, every form refuses an automated submission,
and every response carries its security header set. These are not extras; a governance
product that leaks a broken link teaches its readers that its rules are optional too.


### The copy the product carries

Ten internal contributors are credited by name on the hub outro alongside the external
collaborator: `Rafi Osmani`, `Nikhil Barretto`, `Sam Delaney`, `Dana Ruiz`, `Marisa Kade`,
`Ellis Trembath`, `Hanna Bertolucci`, `Devan Mistry`, `Marcus Ade` and `Adaeze Oni`. Two
epigraphs open two chapters, attributed to `Vera Lindqvist` and to `Ada Renwick`. The
cursor-tag labels name `Nadia` and `Rose` with the roles type designer, type director,
foundry chief and race driver. Every one of those strings is content the build carries.

### Motion vocabulary, in words

The movements the product uses, described rather than valued:

| Movement | Character |
|---|---|
| Fade | opacity alone, used only where nothing should move, such as a stage settling |
| Forward travel | an element advancing toward the reader as it enters, used on the hub tiles |
| Chase | a highlight running along a construction hairline, forward only, never reversing |
| Circle sweep | the rotation of the palette wheel and of the aspect ratio switcher, linear and unhurried |
| Word fill | the named reveal: a headline filling word by word as the line enters the viewport |
| Negative travel | an element leaving upward as the next ground arrives beneath it |
| Scrub | position driven by scroll rather than by a timer, on three global elements only |

Motion is eased on entrance and exit, and only the circle sweep runs at a constant rate.
Nothing overshoots. No movement is ever the only signal that something happened: a state
change is always also visible in text.

### Type detail

The annotation face carries generous leading relative to its small size, which is why it
stays readable at the density the product uses it. Display type is set tight, close to its
own height, because it exists as a graphic element rather than as a paragraph. There is no
intermediate size doing general purpose work, and that absence is deliberate. Set numbers
in the governed surface so that columns of them align.

### Clarity over complexity

Where a surface could be complex, it is made plain instead: the decision panel states in
one sentence why a request reached this reviewer, the refusal states in one sentence what
is missing, and the availability badge states one word. A governance product earns
compliance through clarity, and anything that reads as a puzzle will be worked around.

## Constraints

- Only the providers named in this brief exist: PostgreSQL for the database and MinIO for
  the object store. Do not add a cache, a queue, a search engine, a mail sender or a
  second database, and do not call out to the public internet at request time.
- There is no corporate identity provider to integrate with in this build. Sign in is the
  app's own email address and password against the seeded principals, and the brief's
  references to a provisioned directory describe where principals come from, not a service
  to call.
- No signup. Creating a principal is not a function of this app.
- No payments, no money, no currency anywhere in the product.
- No email is sent. Where this brief says a holder is notified, the notification is a
  record the holder can read in the app, not a message that leaves it.
- No file is served from the upload origin, and no protected object is publicly readable.
- No audit record is ever updated or deleted, by any role, through any path.
- No persistent volume, no fixed container name and no custom network.
- The eight chapter slugs, the reserved slug list, the seven asset classes, the six
  application classes, the nine request states, the six condition kinds and the four
  availability badges are closed sets. Do not add a member to any of them.
- All times are UTC. All text is English.
- The reading surface contains no photography in its chrome, one gradient, and one drop
  shadow which belongs to the consent frame.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment;
  never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root,
  empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the
  shell. An ordinary background job dies with its shell, and the app will not be running
  when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of
  them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `email`, `password` | the principal plus an `access_token` |
| `GET /api/health` | none | readiness |
| `GET /api/chapters` | none | a top-level JSON array of chapters, each with `slug`, `title`, `display_order`, `ground_colour`, `type_colour` |
| `GET /api/chapters/{slug}` | none | one chapter with its current version and its statements, each with `statement_id` and `text` |
| `GET /api/assets` | optional `chapter`, `asset_class`, `licence_class`, `availability` | a top-level JSON array of assets, each with `id`, `name`, `asset_class`, `chapter`, `availability`, `formats`, `licence_class` |
| `GET /api/assets/{id}` | none | one asset with its `licence`, its `conditions`, its `successor`, its `dimensions` and the `availability` computed for the caller |
| `GET /api/assets/{id}/download` | none | the released binary when the caller may have it, otherwise a refusal naming what is missing |
| `POST /api/requests` | `asset_id`, `application_class`, `territory`, `campaign_start`, `campaign_end`, `cited_statement_ids` | the created request with its `state`, its `holder`, its `deadline` and its stages |
| `GET /api/requests` | optional `state` | a top-level JSON array of the caller's own requests |
| `GET /api/requests/{id}` | none | one of the caller's own requests, with its decision chain, comments and conditions |
| `POST /api/requests/{id}/withdraw` | none | the withdrawn request |
| `GET /api/queue` | none | a top-level JSON array of the stages awaiting the calling reviewer, ordered by deadline |
| `POST /api/stages/{id}/decision` | `decision`, optional `conditions`, optional `reason` | the decided stage and the request as it now stands |
| `POST /api/conditions/{id}/proof` | the proof file | the stored proof with its `scan_state` |
| `POST /api/proofs/{id}/accept` | none | the accepted proof and the activated grant |
| `GET /api/grants` | none | a top-level JSON array of the caller's own grants, each with `asset_id`, `request_id`, `starts_at`, `ends_at`, `conditions` |
| `GET /api/audit` | optional `request_id`, `principal`, `from`, `to` | a top-level JSON array of audit records, each with `actor`, `principal_type`, `address`, `request_id`, `state_before`, `state_after`, `recorded_at` |
| `POST /api/consent` | `answer` | the recorded consent choice |
| `GET /api/consent` | none | the caller's recorded consent choice, or none |
| `POST /api/page-views` | `route` | the recorded view |

A successful call returns the named resource or shape. An invalid or unauthorized call is
rejected as a client error, never as a server error and never as a silent success. Bearer
auth is required on everything except login, health, the chapter list, a single chapter,
the consent choice and recording a page view.

## Definition of done

A stranger can open the hub, watch the eight tiles assemble, read any of the eight
chapters and work every demonstration on them, and answer the cookie choice once. A
signed in employee can browse a library that is never empty, read an asset's licence and
download what is released to them. A partner is refused the mark with the reason stated,
raises a usage request instead, and is warned that their engagement caps the grant. Two
reviewers decide the two stages and exactly one grant is minted, ending at the engagement
end date. Two reviewers approving one stage at the same instant produce exactly one
decision, one grant and one audit record. An employee calling a reviewer endpoint is
refused and nothing changes. An audit record cannot be altered or removed. An unknown
address lands on the product's own not-found page.
