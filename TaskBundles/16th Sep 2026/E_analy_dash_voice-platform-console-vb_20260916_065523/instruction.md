# Vocalis Console

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser
and sign in as an engineer, submit a clip through the playground, read the
accuracy and latency it reports, and issue the first scoped credential for a
project without hitting an error page.

A different stranger, holding a membership that carries an explicit deny on one
project, must NOT be able to read that project by any means: not through the
project index, not through the project switcher, not by typing its address, and
not through the organisation usage figure. The usage totals this console shows
must be the sum of the metering rows stored underneath them; a figure the app
computes for itself and never checks against its own rows does not count.

## Overview

Vocalis sells speech recognition and speech synthesis to other companies as
metered infrastructure, billed by the second. The model line is `Volt`: `Volt STT`
listens and `Volt TTS` speaks. This is the console behind it: the
governed surface where a customer organisation holds projects, a project holds
scoped credentials, every request is metered and attributed to exactly one
project, and members hold roles that can differ per project.

An organisation is the tenant. A project is the unit of isolation, of metering
and of configuration. A credential belongs to exactly one project and is a
principal in its own right rather than a stand-in for the person who created it.
Usage accumulates against the project, rolls up by day, and lands on an invoice
the organisation can be shown and can argue with.

The people who use it are not one audience. An engineer wants a working
credential and a way to see that a request arrived. An owner wants to know what
is authorised to spend money and what it spent. An auditor wants to read the
record of who changed either, including changes the administrator made, and to
change nothing.

This is deliberately **not** the whole platform. There is no marketing site, no
audio socket, no microphone capture, no stored audio, no federated sign-in and no
real payment provider. The console records usage and governs access; it does not
carry audio.

The genuinely hard part is arithmetic that has to survive redelivery and late
arrival: the figure on the usage screen, the rows it summarises and the invoice
that bills for them must agree, while the intake accepts the same event twice
without counting it twice, and while an event that arrives late for a period
already invoiced restates that period without touching the invoice.

## User roles

Four roles, assigned at organisation level. A per-project override may deny a
permission the organisation role grants, and deny always wins.

| Role | Can read | Can write | Cannot |
|---|---|---|---|
| Owner | the organisation, every project, all usage, invoices, the balance ledger, the audit record | organisation settings, projects, member roles, credentials including elevated ones, approval decisions | **approve their own request** |
| Administrator | the organisation, every project, all usage | projects, ordinary credentials, member roles up to their own level | **read invoices**, **read the audit record**, **issue an elevated credential**, **change organisation settings** |
| Member | projects they are not denied, usage for those projects | nothing except playground requests and revoking a credential they issued themselves | **create a project**, **issue any credential**, **revoke another person's credential**, **read invoices**, **read the audit record** |
| Auditor | the organisation, every project, all usage, invoices, and the audit record | nothing at all | **write anything**, **use the playground** |

The auditor reads the audit record and the administrator does not. That
separation is the point of the role: an auditor who needs an administrator's help
to see the administrator's own activity is not auditing anything.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a member session to
any owner-only endpoint must be rejected by the server (an unauthorized request is
denied, not served), leaving the protected state unchanged.

**Signup is closed.** There is no registration form and no self-service account
creation. Accounts exist only because they are seeded.

Seeded accounts, every one using the password `deku-demo-pw-2026`:

| Email | Name | Northwind Audio | Halyard Labs |
|---|---|---|---|
| `owner@example.com` | Dana Reyes | owner | owner |
| `owner2@example.com` | Priya Nandakumar | owner | not a member |
| `admin@example.com` | Marcus Hale | administrator | not a member |
| `member@example.com` | Ines Duarte | member | not a member |
| `member2@example.com` | Tobias Frey | member | not a member |
| `auditor@example.com` | Ruth Okafor | auditor | not a member |

## Core features

### Auth

Email and password, exchanged for a bearer token the console sends on every
subsequent call. Passwords are stored hashed, never in clear.

1. A correct email and password returns a token and the signed-in principal.
2. A wrong password, an unknown email, and a disabled account are refused
   identically, so the response never confirms that an address exists.
3. Signing out invalidates the token; a call carrying it afterwards is refused.
4. An expired or unknown token is refused and no state changes.
5. No password, no token and no credential secret appears in any response body,
   log line or error message.

### The console shell

The shell is the global chrome: everything that persists across console routes.
It carries the wordmark, the organisation switcher, the project switcher, a
global search, notifications and the account menu, and it renders nothing until
the session and the principal's permissions are resolved. Notifications group by
resource, newest first, and carry an unread mark.

1. The organisation switcher lists only organisations the principal belongs to.
   Where they belong to exactly one, it renders as a label rather than a control.
2. The project switcher lists only projects the principal can read within the
   selected organisation.
3. **Changing organisation clears the project selection and lands on the
   organisation overview.** The previous organisation's project identifier is
   never carried into the new one, and no screen in the new organisation may be
   reached by reusing it.
4. The selected organisation and project appear in the address, so every screen
   is linkable and a shared link resolves to the same screen or to a clean
   refusal.
5. Search returns projects, credentials by label and members, and never returns a
   resource the principal cannot read. It never searches transcripts. The
   restriction is applied when the results are gathered, not by hiding rows
   afterwards, so the number of results, the paging and the response time never
   confirm that something exists.
6. Each screen leads with one **primary action**, visually distinct from every
   secondary control on the same screen.

### Projects

Creating a project opens a modal on the project index.

1. A project carries a name, a slug, a region, a retention period in days and a
   state.
2. The name is mutable and unique within the organisation.
3. The slug is derived from the name once at creation and never changes
   afterwards, even when the name does.
4. Only an owner or an administrator may create a project. A member's attempt is
   denied and no project is created.
5. A project is never deleted. Archiving it is the terminal action: an archived
   project refuses new usage, revokes its credentials, and keeps every metering
   row and every invoice line it already had.
6. **The billing record outlives the project.** Archiving `Meeting Capture` must
   leave its `300` audio seconds in the August figures and on invoice
   `NW-2026-0001`, because an invoice has to remain explicable after the project
   it bills for stops being used.
7. A project the principal may not read is reported as not found rather than as
   forbidden, so the console never confirms that a named customer's project
   exists.

### Scoped credentials

The most security-sensitive surface here. Issuing opens a modal on the credential
index; the result is a full-page confirmation.

Seven scopes exist, and no others:

| Scope | Grants |
|---|---|
| `recognize:batch` | submit pre-recorded recognition |
| `recognize:stream` | open a recognition stream |
| `synthesize` | request synthesis |
| `agent` | open an agent session |
| `usage:read` | read this project's usage |
| `manage:keys` | issue and revoke credentials in this project |
| `admin:project` | change project settings |

1. A credential carries a label, a scope set drawn from the seven above, exactly
   one project which is fixed at creation, an optional expiry, the principal who
   created it, a last-used time and a revocation time.
2. The secret is forty characters beginning `vclk`. Its first eight characters
   are the prefix, which is stored in clear, is unique across every credential,
   and is what the index displays. A secret of the shape
   `vclk9d41c7e206b8fa53d9174e0cb62f8a3d570e9b1` therefore has the prefix
   `vclk9d41`.
3. **The secret is shown exactly once, at creation, and is never recoverable.**
   It appears on a full-page confirmation that cannot be dismissed until it is
   acknowledged. After that there is no control anywhere that reveals it, no
   endpoint that returns it, and no log, error or response that contains it.
   Losing it means issuing a new one.
4. The stored form is a hash of the full secret and cannot be reversed.
   Verification finds the row by prefix and then compares the hash, so an unknown
   prefix and a wrong secret are refused identically.
5. Rotating a credential issues a successor and leaves both valid through an
   overlap window, after which the original expires. A rotation that stops the
   original working immediately is an outage the product caused, and is wrong.
6. Revoking is immediate: from the instant it is revoked, the credential is
   refused everywhere.
7. `manage:keys` and `admin:project` are **elevated**. A request for a credential
   carrying either one issues nothing straight away. It records an approval
   request naming the requester, the reason, the label and the requested scopes,
   and the credential is created only when a **different owner** approves it. The
   issued credential then carries a mandatory expiry.
8. **Self-approval is impossible and is refused by the server**, not hidden in the
   interface. A request approved by the principal who raised it must not issue a
   credential.
9. Where an organisation holds exactly one owner, an elevated request is refused
   with an explanation to appoint a second owner, rather than quietly permitting
   self-approval.
10. A member may revoke a credential they issued themselves and no other. An
    administrator or owner may revoke any credential in the organisation.
11. The credential index shows label, prefix in a monospaced face with a copy
    control, scopes as chips with the overflow collapsed past three, created,
    last used, expiry and status. The created and last-used cells read as a
    relative age, with the absolute time available on hover. A credential
    that has never been used renders the word `never` explicitly and reads as a
    warning, because an unused credential is attack surface with no benefit.
12. Status is one of `active`, `expiring`, `expired` or `revoked`.

### The playground

An authenticated surface where a member sends a real request to the service and
watches the result arrive. It is the shortest path from an account to a project's
first successful request.

The environment holds no object store and this console carries no audio bytes,
so recognition works from a seeded clip inventory. Three clips exist, each with a
known duration and a known result:

Recognition runs on `Volt STT` and synthesis on `Volt TTS`; a project's default
model names one of the two.

| Clip | Duration | Accuracy |
|---|---|---|
| `Quarterly Review Call` | `180` audio seconds | `97.4%` |
| `Support Voicemail` | `45` audio seconds | `92.1%` |
| `Product Demo` | `120` audio seconds | `95.8%` |

1. Submitting a clip for recognition returns its transcript, its accuracy as a
   percentage to one decimal place, and the latency the request took in
   milliseconds, measured by the app.
2. Submitting text for synthesis returns the number of characters accepted and
   the latency, and the character count is the count of the text submitted.
3. **Every playground request is metered and attributed exactly as a production
   request is.** Submitting `Quarterly Review Call` against `Contact Centre`
   writes exactly one metering row of `180` audio seconds on the line
   `recognize.batch`, attributed to that project, and raises that project's total
   for the open period by exactly `180`.
4. The playground is not a path around the limits. A request against an archived
   project is refused, and a principal who cannot use the playground is refused.
5. An auditor cannot use the playground at all; the attempt is denied and nothing
   is metered.
6. Every playground request is recorded and inspectable afterwards, showing the
   parameters the service received including the defaults the client did not
   send, the latency, and the billed quantity.
7. A request that fails meters nothing.

### The metering intake

This is where a project's credential is actually used, and it is the reason a
credential exists. A caller presents a credential secret as a bearer token and
submits a usage event.

1. The submission carries an idempotency key, a line, a quantity, a unit and the
   time the usage occurred. That time is written in the ISO 8601 form
   `2026-08-01T09:00:00Z`, always in UTC with the trailing `Z`.
2. The credential is verified by prefix then hash. An unknown, expired or revoked
   credential is refused and nothing is written.
3. A credential lacking the scope for the submitted line is refused and nothing
   is written.
4. **A submission whose idempotency key has been seen before writes no second row
   and changes no total.** Idempotency is keyed by that external identifier, so a
   delivery can be replayed safely: it is accepted rather than treated as an
   error, because a retried delivery is normal and must be a no-op.
5. The event is attributed to the credential's own project. A caller cannot
   attribute usage to a project their credential does not belong to.
6. An archived project accepts no new events.
7. The event records both when the usage occurred and when the record was
   written, because a customer running the software on their own machines reports
   late.

### Usage and reconciliation

The organisation overview and every project usage screen are a grid of charts
over a table of the same figures.

1. A usage screen takes a date range and groups by project, by line or by model.
   It shows a stacked area chart over time and a table of exact figures.
2. **The chart and the table are the same figures.** A screen whose graph and
   table disagree destroys confidence in every number in the product, and it
   happens whenever they are computed separately.
3. **A total equals the sum of the rows underneath it, exactly.** For the range
   `2026-08-01` to `2026-08-31`, `Contact Centre` totals `5400` audio seconds and
   `6500` characters over five rows; `Voice Notes` totals `1500` audio seconds
   over two rows; `Meeting Capture` totals `300` audio seconds over one row; and
   `Northwind Audio` totals `7200` audio seconds and `6500` characters.
4. **An organisation total excludes every project the reader may not read.** The
   same range read by `member2@example.com`, who is denied `Voice Notes`, totals
   `5700` audio seconds rather than `7200`.
5. An event arriving with an occurrence time inside a period whose invoice is
   already finalised is accepted and restates that period's own figures. The
   finalised invoice's total does not change.
6. Every figure states how current it is rather than implying it is live.
7. A range holding no usage shows an empty state on the chart and the table
   together, never a blank panel.
8. Aggregation is by daily rollup rather than by scanning every metering row, and
   a rollup is recomputable from its rows at any time. A rollup that has drifted
   from its source is undetectable without that recomputation, and it is what a
   customer discovers first.
9. **Anomaly surfacing.** A project whose usage in the open period exceeds its own
   trailing average by a configured multiple is surfaced as a notification in the
   console, because the common catastrophe in a metered product is a runaway loop
   discovered on the invoice.
10. Usage may also be reported late by a customer running the software
    **self-hosted**. Such reporting arrives through the same intake, carries the
    same idempotency key, and is attributed by its occurrence time rather than by
    its arrival time.

### Billing, the balance and invoices

1. A balance is an append-only ledger and never a mutable number. Every movement
   is an entry: a grant, a purchase, a drawdown, an expiry, an adjustment or a
   refund.
2. The balance is the sum of its entries. `Northwind Audio` holds a grant of
   `20000` and a drawdown of `-19100`, so its balance reads `900` minor units.
3. No ledger entry is ever updated or removed. A correction is a further entry.
4. Invoicing runs on a period that closes at the organisation's billing anchor
   day. A draft invoice is generated from the daily rollups.
5. To finalise a draft is to make it immutable and to give it its number.
   **A number is allocated at finalisation, never at draft**, and numbers run
   sequentially and gaplessly per legal entity. `Northwind Audio Ltd` holds
   `NW-2026-0001`, so the next number it allocates is `NW-2026-0002`.
6. A finalised invoice is immutable. A correction references it as a credit entry
   and never edits it.
7. An invoice's total equals the sum of its lines, and its lines are the daily
   rollups for its period. `NW-2026-0001` totals `19100` minor units in `usd`.
8. Only an owner or an auditor may read an invoice. An administrator's attempt is
   denied.
9. Money is held as an integer count of minor units with a currency code, and
   never as a fractional number.
10. The balance raises a notification when it falls low and again when it is
    exhausted. At zero with grace enabled the organisation continues to be served
    into a bounded overdraft and is notified; at zero without grace, new requests
    are refused while anything already in flight completes.
11. A usage table is exportable as comma-separated values. Past a threshold the
    export is generated asynchronously and offered when it is ready, rather than
    holding the request open.

### Roles, overrides and the audit record

1. A role is assigned at organisation level and is one of `owner`,
   `administrator`, `member` or `auditor`.
2. A per-project override names a principal, a permission and an effect of either
   `grant` or `deny`.
3. **Deny always wins.** The decision order is the explicit project deny, then the
   explicit project grant, then the organisation role, then a default of denied.
   `member2@example.com` carries a deny on reading `Voice Notes`, and holds a
   member role that would otherwise read it.
4. An administrator may assign a role up to their own level and no higher. An
   attempt to make someone an owner is denied.
5. The last owner of an organisation cannot be removed or demoted; the action is
   refused with an explanation.
6. Removing a member ends their sessions and leaves the credentials they issued
   active and flagged for review. Cascading revocation would take down the
   customer's production systems when somebody leaves, so the product makes the
   choice visible rather than making it silently.
7. Every credential issue, rotation and revocation, every approval decision,
   every role change, every override change and **every refusal** appends one row
   to the audit record, naming the actor, the action, the resource, the outcome,
   a correlation identifier for the request, and the inputs the decision was made
   on.
8. The audit record is append-only and **tamper evident**: rows carry a sequence
   that makes a removed or rewritten row visible as evidence rather than
   invisible. No endpoint updates or removes a row. Data governance beyond this
   record is limited to the retention period each project carries.
9. The actor on an event caused by a credential is the credential, not the person
   who created it.

### The public surface and its edges

1. A **terms** page is reachable from the footer of every page and is linked from
   the sign-in form, and it states what the product records about an
   organisation and how long it is kept.
2. An address matching no route renders the console's own **not-found** page,
   carrying the product's chrome and a way back, and answers with a not-found
   result rather than a success.
3. Every **internal link** on every reachable page resolves. No navigation item,
   footer link or in-page link points at an address that does not exist.
4. Every response carries the standard **security headers**, including a strict
   transport policy and a content-type policy that refuses sniffing.
5. A form rejects invalid input in place, naming the field, and writes nothing.
   Validation happens on the server as well as in the browser, and the server's
   answer is the one that decides.

## User flow

The information architecture is one authenticated console behind a public
sign-in, with the selected organisation and project carried in the address.

| Route | Purpose | Auth |
|---|---|---|
| `/` | sends a signed-in principal to `/overview` and everyone else to `/sign-in` | public |
| `/sign-in` | email and password | public |
| `/terms` | terms of service | public |
| `/overview` | organisation overview, a grid of usage tiles per readable project | authenticated |
| `/projects` | project index; the create modal opens here | authenticated |
| `/projects/<slug>` | project detail | authenticated |
| `/projects/<slug>/keys` | credential index; the issue modal opens here | authenticated |
| `/projects/<slug>/keys/issued` | the one-time secret confirmation | authenticated |
| `/projects/<slug>/playground` | submit a clip or text, read the result | authenticated |
| `/projects/<slug>/usage` | project usage, chart over table | authenticated |
| `/usage` | organisation usage across readable projects | authenticated |
| `/billing` | plan, balance, ledger and invoice list | authenticated |
| `/billing/invoices/<number>` | one invoice and its lines | authenticated |
| `/members` | members, roles and per-project overrides | authenticated |
| `/approvals` | elevated credential requests awaiting a decision | authenticated |
| `/audit` | the append-only activity record | authenticated |
| `/account` | the signed-in principal, and sign out | authenticated |

**Entry and redirects**

An unauthenticated request for a protected route goes to `/sign-in`, and after a
successful sign-in the originally requested route opens. A sign-in with no held
destination lands on `/overview`. Signing out invalidates the token and returns to
`/sign-in`, and going back in the browser does not restore a signed-in screen. An
expired token mid-action refuses the action, writes nothing, and returns to
`/sign-in`. Switching organisation clears the project selection and lands on
`/overview` for the newly selected organisation. The account menu opens
`/account`, which names the signed-in principal and carries the sign-out control. A route the principal is not
entitled to read renders the not-found page and answers not found.

**Journeys**

1. Sign in as `member@example.com`, open `Contact Centre`, open its playground,
   submit `Quarterly Review Call`. The result shows the transcript, `97.4%` and a
   latency in milliseconds; the project's open-period total rises by exactly
   `180` audio seconds and the request appears in the request list.
2. Sign in as `admin@example.com`, open `Voice Notes`, open its credentials. The
   index is empty and says so. Issue a credential labelled `Notes Ingest` with
   the scopes `recognize:batch` and `usage:read`. The confirmation shows the
   secret once and will not dismiss until it is acknowledged. The index then
   lists `Notes Ingest` by its prefix with last used reading `never`.
3. Submit a usage event to the intake using that secret, carrying an idempotency
   key, `recognize.batch` and a quantity. `Voice Notes` rises by that quantity.
   Submit it again with the same key: the total does not move.
4. Sign in as `owner@example.com`, open `/usage`, set the range `2026-08-01` to
   `2026-08-31`. The organisation total reads `7200` audio seconds and `6500`
   characters, and the table rows sum to exactly that.
5. Sign in as `member2@example.com` and open `Voice Notes`. It is not found, it
   is absent from the project index and the project switcher, and the same
   organisation range now totals `5700` audio seconds.
6. Sign in as `owner@example.com`, request a credential on `Contact Centre`
   carrying `manage:keys` with a reason. Nothing is issued and a request appears
   on `/approvals`. The same owner cannot approve it. Sign in as
   `owner2@example.com` and approve it; the credential issues with an expiry and
   both principals appear in the audit record.
7. Sign in as `auditor@example.com`, open `/audit`, and read every entry the
   previous journeys wrote. Open `/billing` and read `NW-2026-0001`. Open
   `/members` and read the four roles held in the organisation. Attempt to issue
   a credential: it is denied.

**States**

Every list has an empty state naming what is missing and offering the action that
fills it: the project index, the credential index, the invoice list, the
approvals list, the audit record and both usage surfaces. Every page has a
loading state; tables show skeleton rows and charts a skeleton frame. A failed
request shows a banner in place and leaves the shell standing, and never replaces
the console with an error page. The playground result panel is absent until a
request is made, the submit control shows it is working, and a second submit is
refused while the first is in flight.

## UI/UX notes

The console is visibly the same product as the platform it belongs to, and the
character is taken from that product rather than invented here. The register is
operational: this is a place where people work, not a place they are being sold
to. The north star is comprehension, and there is no feeling to manufacture.

**Ground and palette by role.** The page ground is a near-black neutral that
almost nothing brightens, so the saturated accents read as light sources rather
than as decoration. Surfaces step upward from it in four further near-black
neutrals, and that stepping is how depth is made rather than by drawing borders.
The interior of a primary control is a near-black neutral one point darker than
the ground, so a control reads as a cut-out rather than as a panel sitting on it.

Headings and primary control labels take a near-white neutral, the only true
white, and white is reserved for them. High-emphasis body takes a second
near-white neutral. Running text is deliberately not white: the default body
colour is a light neutral, with two further light neutrals for secondary and
tertiary text and a mid neutral for muted labels and captions. Disabled text,
borders, dividers and inset borders come from three deep neutrals, never from a
lightened ground.

**Three accent families, each with a job, and mixing them is an error rather than
a preference.** The brand green is a mid, vivid teal and carries flat fills and
the open state; a light, vivid teal is the interactive and open-state green. The
blue family runs alongside it: a mid, vivid cyan is the origin of the heading
ramp and of the glows, a mid, soft cyan is its desaturated flat treatment, a
light, soft blue is the focus ring, and a near-white, soft cyan is the palest
tint. The violet and magenta family is reserved for a second control treatment
and for the widest gradient fields and appears nowhere else: a mid, vivid indigo
terminal, a near-white, muted indigo origin, a mid, vivid violet and a mid, vivid
magenta in the alternate control border, a light, vivid violet and a mid, vivid
red as field stops, a light, vivid blue as the terminal of the two-colour heading
ramp, and a deep, muted blue as the base of the dark radial field.

The exact shades are yours so long as they hold those relationships. Meaning is
never carried by colour alone: failure, success and in-progress each carry a word
or a mark as well as a hue.

**Depth is coloured light, not shadow.** A primary action carries a horizontal
glow pair, teal bleeding off one edge and cyan off the other with nothing above
or below, so it reads as lit from both sides rather than raised. Cards carry one
soft lift. Backdrop blur appears in three places and no more.

**Type.** Two families: a display face at weight 700 for headings and controls,
and a text face at 400, 500 and 600 for everything else. The display face is a
geometric grotesque with a single-storey lowercase `a` at weight 700; use
`Space Grotesk`. The text face is an open-licensed grotesque carrying tabular
figures, because usage quantities and currency stack in columns that must align;
use `Inter`. Both fall back to the system sans stack. Console body type is `14px`
on a `20px` line, and the card radius is smaller than the marketing surface's.
Every figure that stacks in a column is set in tabular figures, and the
credential prefix is monospaced.

**Shape and density.** Primary controls, avatars and badges are fully rounded.
Inline controls and chips take the default softness, cards a gentle one, keyboard
hint glyphs barely any. Density is compact: rows sit tight so a full credential
list or a full usage table reads in one screen.

**Motion is eased.** Considered entrance and exit easing, so motion reads as a
designed interface; nothing overshoots and nothing springs. Everything that
changes shares one shape of acceleration, with a few exceptions that each have a
job: overlays and dialogs land firmly and quickly, and folding sections take a
steeper shape which makes a wrong measured height immediately obvious, which is
why it was chosen. Anything a person caused finishes fast enough to read as a
response rather than a performance; anything that runs on its own is almost
imperceptible, and a reader notices the animated control border drifting only by
watching for it. The named moments are a fade in on first appearance,
a show and hide pair for dialogs and popovers, a modal that scales up slightly
as it fades in, an accordion whose height animates from a measured content
height and never on first paint, a chevron that turns a half turn as a section
opens, a continuous spin for the loading indicator,
a slow opacity pulse for anything live, and a
heading that **settles downward into place** rather than rising into it, which is
unusual and is deliberate.

Under a reduced-motion preference every self-running animation stops and renders
at its first frame, the accordion height change becomes instant, and the animated
border freezes. Dialogs may keep their opacity change. Nothing translates.

**Components.** Every control has a resting, pointed-at, pressed, focused and
unavailable state. Escape closes any overlay. Revoking a credential and archiving
a project both confirm first. Unavailable is never signalled by colour alone.
Hover treatments apply only to a real pointer, because on a touch pointer a hover
effect has no way to end and latches after a tap.

**Mode.** Committed to dark and designed fully for it. There is no light mode and
none is implied.

**One primary action per screen**, wearing the glow, with every other control on
that screen visually secondary: create on the project index, issue on the
credential index, submit in the playground, the decision on the oldest request in
the approvals list.

**Responsive.** The layout holds at every width between the named tiers rather
than only at them. The primary reflow is at the tablet width, the section
navigation appears at the desktop width, and a wide tier sits above it. Below the
phone tier console tables become stacked cards, each row one card carrying the
same fields with their labels, because a table that scrolls sideways on a phone
hides the column that matters. Nothing overflows sideways at any viewport width
and every navigation target stays reachable.

**Accessibility floors**, which do not vary with the character: body text meets
the WCAG AA contrast ratio of `4.5:1` against its background in the committed dark
mode, every touch target is at least `44x44` pixels, keyboard navigation reaches
every control with a visible focus ring drawn in the focus blue, every icon-only
control carries a label, and meaning is never carried by colour alone. A skip link is the
first focusable element on every page and moves to the main landmark. A result
panel uses a live region for announcing final text only and never announces
provisional text, so a screen reader is not read the same sentence twice.

**What this must not look like.** Not a marketing composition where a working
interface belongs: no oversized hero, no editorial column, no decoration standing
in for content. Not a page dominated by one hue family with no second signal. Not
a surface where the only way to tell an unavailable control from an available one
is its colour.

## Technical requirements

Server-rendered multi-page application. The backend is `Express` with `Nunjucks`
templates; the browser layer is `HTMX` over those server templates. Storage is
PostgreSQL, reached at `DATABASE_URL`. Auth is app-implemented email and password
with bearer tokens. `GET /api/health` returns `200` once the app is ready.
Request lines go to stdout.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing service available in this environment is
PostgreSQL, and reaching for anything else is a contract violation.

PostgreSQL is **already running** and reachable at `DATABASE_URL`. Do not
download, install, compile or start a copy of it.

The observable consequence of the rendering model: every console route arrives as
complete HTML on first paint, so the browser receives a finished page rather than
an empty shell that fetches its own content. An interaction that changes part of
a screen replaces that fragment in place rather than reloading the document, and
every such screen is also reachable as a full page load at its own address.

Two authentication surfaces exist and stay distinct. The console presents a
bearer session token identifying a user. The usage intake presents a credential
secret as a bearer token, identifying a credential. A credential is a principal
in its own right: the audit record names it as the actor, and removing the user
who issued it does not revoke it.

Passwords and credential secrets are stored hashed. The first eight characters of
a credential secret are stored separately as its lookup prefix, which is unique.
An unknown prefix and a wrong secret must be refused identically, so that neither
the response nor the time it takes distinguishes them.

Every response carries a strict transport policy header, a content-type policy
that refuses sniffing, a frame policy and a referrer policy.

Nothing in the browser bundle contains a credential, a session token or a
password.

There is no outbound network at run time.

## Data model

Fifteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account so
a grader can sign in.

Conventions that hold for every table: a tenant column on everything carrying
tenant data; a created and an updated timestamp, both with a timezone and both
stored in coordinated universal time; soft deletion through a nullable archived
time rather than removal; money as an integer count of minor units plus a
currency code; quantities as integers in the smallest billable unit; and fixed
value sets rather than free text for every enumerated field.

**organisations** - `id`, `name`, `slug` unique, `legal_entity`,
`billing_anchor_day`, `currency`, `plan`, `created_at`, `updated_at`.

**users** - `id`, `email` unique and lowercase, `display_name`, `password_hash`,
`created_at`.

**memberships** - `id`, `org_id`, `user_id`, `role`, `joined_at`, `removed_at`
nullable. One live membership per user per organisation. `role` is `owner`,
`administrator`, `member` or `auditor`.

**projects** - `id`, `org_id`, `name`, `slug`, `region`, `retention_days`,
`archived_at` nullable, `created_at`, `updated_at`. The slug is unique within the
organisation and is derived once at creation; it is not recomputed when the name
changes.

**project_role_overrides** - `id`, `org_id`, `project_id`, `user_id`,
`permission`, `effect`. One override per project, principal and permission.
`effect` is `grant` or `deny`.

**api_keys** - `id`, `org_id`, `project_id`, `label`, `prefix` unique,
`secret_hash`, `scopes`, `created_by`, `expires_at` nullable, `last_used_at`
nullable, `revoked_at` nullable, `rotated_from` nullable, `created_at`. The full
secret is not a column: it is not stored in any form that can be read back.

**key_issue_approvals** - `id`, `org_id`, `project_id`, `requested_by`, `reason`,
`requested_scopes`, `label`, `approver_id` nullable, `decision`, `decided_at`
nullable, `expires_at`, `created_at`. `decision` is `pending`, `approved`,
`rejected` or `expired`. The approver is never the requester.

**usage_events** - `id`, `idempotency_key` unique, `org_id`, `project_id`,
`key_id` nullable, `line`, `model`, `mode`, `quantity`, `unit`, `region`,
`rate_version`, `source`, `occurred_at`, `recorded_at`. `line` is
`recognize.batch`, `recognize.stream`, `synthesize` or `agent`. `unit` is
`audio_second`, `character` or `session_second`. `source` is `cloud`, `dedicated`
or `self_hosted`.

**usage_rollup_daily** - `org_id`, `project_id`, `line`, `day`, `quantity`,
`cost_minor`. **Derived, never authored**: recomputable from `usage_events` at any
time, and it must equal that recomputation.

**rate_cards** - `id`, `version` unique, `line`, `unit`, `price_minor_per_unit`,
`currency`, `effective_from`.

**invoices** - `id`, `org_id`, `number`, `period_start`, `period_end`, `status`,
`subtotal_minor`, `tax_minor`, `total_minor`, `currency`, `finalised_at`
nullable. `status` is `draft`, `finalised`, `paid` or `uncollectible`. The number
is unique per legal entity.

**invoice_lines** - `id`, `invoice_id`, `project_id`, `line`, `quantity`, `unit`,
`rate_version`, `amount_minor`.

**ledger_entries** - `id`, `org_id`, `type`, `amount_minor` signed, `currency`,
`source_ref`, `effective_at`, `created_by`, `created_at`. `type` is `grant`,
`purchase`, `drawdown`, `expiry`, `adjustment` or `refund`.

**audit_events** - `id`, `org_id`, `actor_type`, `actor_id`, `action`,
`resource_type`, `resource_id`, `outcome`, `policy_inputs`, `occurred_at`.
`actor_type` is `user`, `credential` or `system`. `outcome` is `allowed` or
`denied`.

**clips** - `id`, `name`, `duration_seconds`, `accuracy`, `transcript`. The
seeded playground inventory, shared across projects and not tenant data.

**playground_requests** - `id`, `org_id`, `project_id`, `user_id`, `mode`,
`clip_id` nullable, `input_characters` nullable, `accuracy` nullable,
`latency_ms`, `usage_event_id`, `created_at`.

### Invariants, stated as properties of the running system

- A project's usage total for a date range equals the sum of the quantities of
  its metering rows whose occurrence time falls inside that range, per line. The
  chart and the table read that one figure.
- An idempotency key appears on at most one metering row. A second submission
  carrying a key already present writes no row and moves no total, under
  concurrent submission as well as sequential.
- A metering row whose occurrence time falls inside a period already invoiced is
  accepted and restates that period's daily figures, and the finalised invoice's
  total does not change.
- An organisation usage figure shown to a principal excludes every project that
  principal may not read.
- A credential prefix appears on at most one credential and is the only lookup
  path used to verify one.
- No response, log line or error contains a credential secret, a password or a
  session token.
- A revoked credential is refused from the instant it is revoked.
- A credential carrying an elevated scope exists only where an approved request
  names it, and that request's approver is not its requester.
- The balance equals the sum of the ledger entries, and no entry is ever updated
  or removed.
- An invoice number is gapless per legal entity and is allocated only at
  finalisation.
- A finalised invoice is never updated.
- An archived project accepts no new metering rows and keeps every existing one.
- Every authorisation decision, allowed or denied, appends one audit row.

### Seed data

Two organisations. `Northwind Audio`, slug `northwind-audio`, legal entity
`Northwind Audio Ltd`, billing anchor day `1`, currency `usd`, plan `Growth`.
`Halyard Labs`, slug `halyard-labs`, legal entity `Halyard Labs Inc`, billing
anchor day `1`, currency `usd`, plan `Pay as you go`.

Six users as listed under `## User roles`. `owner@example.com` belongs to both
organisations; every other account belongs to `Northwind Audio` only.

Four projects:

| Organisation | Name | Slug | Region | Retention | State |
|---|---|---|---|---|---|
| Northwind Audio | `Contact Centre` | `contact-centre` | `eu-west` | `90` | active |
| Northwind Audio | `Voice Notes` | `voice-notes` | `us-east` | `30` | active |
| Northwind Audio | `Meeting Capture` | `meeting-capture` | `eu-west` | `90` | archived |
| Halyard Labs | `Field Recorder` | `field-recorder` | `us-east` | `90` | active |

One override: `member2@example.com` is denied reading `Voice Notes`.
`member@example.com` carries no override and reads it.

Two credentials. `Contact Centre` holds `Ingest Staging`, prefix `vclk2f8a`,
scopes `recognize:batch` and `recognize:stream`, never used. `Meeting Capture`
holds `Capture Legacy`, prefix `vclk6b1d`, scope `recognize:batch`, revoked.
`Voice Notes` holds none.

Rate card `2026-01`: `recognize.batch` at `1` minor unit per audio second,
`recognize.stream` at `2`, `synthesize` at `1` per character, `agent` at `4` per
session second, all in `usd`.

Metering rows for the period `2026-08-01` to `2026-08-31`:

| Project | Line | Quantity |
|---|---|---|
| `Contact Centre` | `recognize.stream` | `1800` |
| `Contact Centre` | `recognize.stream` | `2400` |
| `Contact Centre` | `recognize.stream` | `1200` |
| `Contact Centre` | `synthesize` | `4000` |
| `Contact Centre` | `synthesize` | `2500` |
| `Voice Notes` | `recognize.batch` | `900` |
| `Voice Notes` | `recognize.batch` | `600` |
| `Meeting Capture` | `recognize.batch` | `300` |
| `Field Recorder` | `recognize.batch` | `500` |

Two invoices, both finalised for that period: `NW-2026-0001` for
`Northwind Audio` totalling `19100` minor units, and `HL-2026-0001` for
`Halyard Labs` totalling `500`.

Two ledger entries for `Northwind Audio`: a `grant` of `20000` with source
`welcome-credit`, and a `drawdown` of `-19100` with source `NW-2026-0001`.

Three clips: `Quarterly Review Call` at `180` audio seconds and `97.4%`,
transcript `Revenue for the quarter came in ahead of plan and churn held flat.`;
`Support Voicemail` at `45` audio seconds and `92.1%`, transcript
`Hello, my card was declined twice this morning. Please call me back.`; and
`Product Demo` at `120` audio seconds and `95.8%`, transcript
`This is the streaming endpoint returning partial results as you speak.`

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

The visual specification the console inherits from the product it belongs to.
Everything here reaches the builder in full.

**The surface stops.** Five near-black neutrals in a measured ladder: the page
ground, a raised band sitting on it, a panel and menu sheet above that, the card
interior which is the most-used non-ground surface, and a quoted-card base. The
interior of a primary control and two gradient bases take a sixth, one point
darker than the ground. The one-point difference between the ground and true
black is load-bearing and is why a control reads as a cut-out.

**The neutral ramp** runs nine steps from the only true white through two
near-white neutrals for high-emphasis body, three light neutrals covering the
default body colour and its secondary and tertiary partners, a mid neutral for
muted labels and captions, and three deep neutrals for disabled text, borders and
dividers, and inset borders. The default body colour and the muted label carry
almost all of the rendered text between them, which is the whole typographic
strategy: running text is deliberately not white.

**Gradients.** The heading fill paints one phrase per heading with a ramp running
left to right from the mid, vivid cyan to the brand teal while the rest of the
sentence stays white; an alternate heading ramp starts instead at the light,
vivid blue. The animated control border cycles between the mid, vivid cyan and
the brand teal and back, drifting slowly enough that it reads as a sheen rather
than as an animation. A second, alternate control border uses the violet family:
the mid, vivid violet and the mid, vivid magenta. The control interior is masked
with a flat near-black. Two rule gradients fade a hairline divider into the brand
teal, one running from the light, vivid blue and one from the mid, vivid cyan
through a midpoint. Those two are interpolated in a perceptual colour space,
which is not decorative: a ramp between those colours muddies through grey in the
default space and stays even in a perceptual one.

**The wide fields.** Behind the sign-in surface a chromatic field of broad blue
and violet beams converges on a horizontal seam, with the heading sitting on the
seam under a soft dark text shadow. Its stops are drawn from the violet and
magenta family and include the light, vivid violet, the mid, vivid magenta and
the single warm stop, a mid, vivid red. A dark radial field built on the deep,
muted blue sits behind the secondary surfaces. A slow starfield drifts upward
behind them over a minute and a half or more, and stops entirely under a
reduced-motion preference.

**Typography.** The type scale, carried exactly:

| Size | Weight | Line-height | Role |
|---|---|---|---|
| `30px` | 700 | `38px` | route heading |
| `20px` | 700 | `30px` | card heading, emphatic |
| `18px` | 600 | `28px` | control labels and card headings |
| `18px` | 500 | `28px` | navigation and menu items |
| `16px` | 600 | `24px` | small control labels |
| `14px` | 500 | `20px` | badge and tag labels |
| `14px` | 400 | `20px` | console body, captions and footnotes |
| `13px` | 400 | `20px` | dense metadata |
| `12px` | 400 | `18px` | legal and attribution |
| `11px` | 400 | `28px` | over-line labels, tracked |

The `11px` over-line label against a `28px` line is not an error: it is set on
the same rhythm as body text so it sits in a stacked block without disturbing the
baseline.

**Depth values.** A primary control carries a horizontal glow pair only: a
positive offset carrying the brand teal and a negative one carrying the cyan,
both blurred, with zero vertical offset. Cards carry one soft downward lift,
which is the dominant shadow in the product. A field hairline, a floating panel
pair, a raised-card pair and an inset hairline complete the set. A live dot
carries a teal ring and a teal halo, and a badge carries a teal inner glow.

**Iconography.** Eight inline marks, each an icon drawn as geometry rather than
loaded as a file. The wordmark is a geometric lockup drawn
around the display face's single-storey lowercase `a`. A waveform mark draws a
row of vertical bars of varying height on a square canvas, standing for
recognition. A speaker mark draws a cone with two arcs, standing for synthesis. A
key mark draws a circle with a toothed shaft. A chevron draws a single angle and
rotates a half turn when a section opens. A copy mark draws two offset rounded
rectangles. A check draws a single stroke. A warning draws a triangle with a
centred bar. Each is drawn rather than loaded, and each carries an accessible
label because none of them is decorative.

**Typefaces ship as names, never as files.** `Space Grotesk` for display and
`Inter` for text, both with a swap behaviour while loading and both falling back
to the system sans stack. No font file, image, texture or audio sample is
required to build this: every icon is drawn, every field is a gradient, and the
clip inventory is text.

**Breakpoints** are the phone tier, the tablet width where the primary reflow
happens, the desktop width where the section navigation appears, and a wide tier
above it. Hover treatments are gated to a real pointer. Stacking uses a small
fixed set of levels: content, raised, sticky header, overlay and dialog.

## Constraints

- One product surface: the authenticated console plus its sign-in and terms
  pages. No marketing site, no pricing pages, no editorial collections, no
  customer stories and no lead-capture forms.
- No request-serving plane. No audio socket, no binary frames, no partial
  transcripts, no reconnection or resumption, and no concurrency limiting across
  instances.
- No microphone capture, no device selection, no input meter and no resampling.
- No object storage. No upload, no pre-signed grant, and no stored audio bytes.
- No federated sign-in, no directory provisioning, no group claims and no domain
  verification.
- No real payment provider. No card is charged, no webhook is received, and no
  external billing service exists.
- No mail of any kind. Invitations, notifications and digests are in-console only.
- No territory management, no record-sharing rules, no infrastructure
  configuration graph and no per-organisation custom fields.
- No data movement between regions. A project shows its region; nothing migrates.
- No outbound network calls at run time. No native or mobile app.
- Tenancy is by organisation. Nothing a principal reads may include a row from an
  organisation they do not belong to.
- The app stays responsive with four projects, ten metering rows per project per
  day for a year, and a thousand audit rows.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of
  the shell. An ordinary background job dies with its shell, and the app will not
  be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Field names are exact. A list endpoint returns a top-level JSON
array. A successful call returns the named resource; an invalid or unauthorized
call is rejected as a client error, never as a server error and never as a silent
success. Bearer auth is required on everything except sign-in, health and the
terms page.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/sessions` | `email`, `password` | `token`, `user` |
| `DELETE /api/sessions/current` | none | the session is invalidated |
| `GET /api/organisations` | none | array of `slug`, `name`, `role` |
| `GET /api/organisations/<slug>/projects` | none | array of `slug`, `name`, `region`, `state` |
| `POST /api/organisations/<slug>/projects` | `name`, `region`, `retention_days` | the created project including its derived `slug` |
| `GET /api/projects/<slug>` | none | `slug`, `name`, `region`, `retention_days`, `state`, `key_count` |
| `POST /api/projects/<slug>/archive` | none | the project with `state` `archived` |
| `GET /api/projects/<slug>/keys` | none | array of `label`, `prefix`, `scopes`, `created_at`, `last_used_at`, `expires_at`, `status` |
| `POST /api/projects/<slug>/keys` | `label`, `scopes`, `expires_at` | `secret`, `prefix`, `label`, `scopes` on issue, or the created approval request when a scope is elevated |
| `POST /api/projects/<slug>/keys/<prefix>/revoke` | none | the credential with `status` `revoked` |
| `POST /api/projects/<slug>/keys/<prefix>/rotate` | none | `secret`, `prefix` of the successor, and the original's `expires_at` |
| `GET /api/projects/<slug>/clips` | none | array of `name`, `duration_seconds` |
| `POST /api/projects/<slug>/playground/recognize` | `clip` | `transcript`, `accuracy`, `latency_ms`, `quantity`, `unit` |
| `POST /api/projects/<slug>/playground/synthesize` | `text`, `voice` | `characters`, `latency_ms`, `quantity`, `unit` |
| `GET /api/projects/<slug>/requests` | none | array of `mode`, `clip`, `accuracy`, `latency_ms`, `quantity`, `created_at` |
| `GET /api/projects/<slug>/usage` | `from`, `to`, `group_by` | `total_quantity` per unit, `series`, `rows` |
| `GET /api/organisations/<slug>/usage` | `from`, `to`, `group_by` | `total_quantity` per unit, `series`, `rows` |
| `POST /api/usage/events` | `idempotency_key`, `line`, `quantity`, `unit`, `occurred_at` | the accepted event, and the same response for a repeat |
| `GET /api/organisations/<slug>/invoices` | none | array of `number`, `period_start`, `period_end`, `status`, `total_minor`, `currency` |
| `GET /api/invoices/<number>` | none | the invoice and its `lines` |
| `GET /api/organisations/<slug>/ledger` | none | array of `type`, `amount_minor`, `source_ref`, `effective_at`, and the materialised `balance_minor` |
| `GET /api/organisations/<slug>/members` | none | array of `email`, `display_name`, `role` |
| `POST /api/organisations/<slug>/members/<email>/role` | `role` | the updated membership |
| `POST /api/projects/<slug>/overrides` | `email`, `permission`, `effect` | the created override |
| `GET /api/approvals` | none | array of `id`, `project`, `label`, `requested_scopes`, `requested_by`, `reason`, `decision` |
| `POST /api/approvals/<id>/approve` | none | the issued credential's `secret` and `prefix`, or a refusal when the approver is the requester |
| `POST /api/approvals/<id>/reject` | none | the request with `decision` `rejected` |
| `GET /api/organisations/<slug>/audit` | `from`, `to` | array of `actor_type`, `actor_id`, `action`, `resource_type`, `resource_id`, `outcome`, `occurred_at` |
| `GET /api/health` | none | `200` once ready |

**No mocks.** The usage figures, the invoice totals and the balance must come
from rows that exist in PostgreSQL. An in-memory totals object, a hardcoded
figure the app returns to itself, a rollup written by hand rather than computed
from its rows, and a balance stored as a column that is edited in place are each
a violation of this brief. PostgreSQL is the fact: the console's screens and its
own summaries can only reflect what lives in those rows, never substitute for it.

## Definition of done

An engineer can sign in, submit a clip through the playground, read the accuracy
and latency it reports, and see that request counted against the project a moment
later. An administrator can issue a project's first scoped credential, see its
secret exactly once, and never see it again. The usage a console shows for any
range is the sum of the rows stored underneath it, and stays so after the same
event is delivered twice or arrives late for a period already invoiced. A member
denied one project cannot reach it, and it is absent from the figures they are
shown.
