# Ravel Financial Data Network

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, sign in as a
compliance approver, and sign off a production access request that somebody else filed,
without hitting an error page. A different stranger, signed in as a developer, must NOT be
able to sign off any request by any means, including a direct API call, and the person who
filed a request must not be able to approve their own. Those refusals happen in the server,
and the stored request must be unchanged afterwards: a screen that merely hides the approve
button has not refused anything.

---

## Overview

Ravel is a financial data network. Consumers hold accounts at banks, companies build
applications that need data from those accounts, and Ravel holds the consumer's permission in
between. Build the operator console its customers use: the governed surface where an
organisation manages its applications, API keys, environments, connected end-user accounts,
webhook endpoints, team roles and consumer data requests.

Engineering, risk and compliance staff open it with two questions: what is happening right now,
and why did this connection fail. They leave having acted, by filing a request to go live or by
signing one off.

It is deliberately not a bank, not a consumer product and not a reporting warehouse. No
marketing site, no documentation site, no bank-connection widget, no consumer portal, no billing.

The hard part: permission here is a policy, not a tenant filter. It depends on role, environment,
owning team, and whether the entitlement behind the action was ever approved.

---

## User roles

Four roles, seeded in the identity provider from first boot. Signup is closed: no route creates
an account. Every seeded account uses the password `deku-demo-pw-2026`.

| Role | Account | Write |
|---|---|---|
| `developer` | `developer@example.com`, `developer2@example.com` | Create applications; create and revoke `sandbox` and `development` credentials; file production access requests; manage webhook endpoints. **Never a `production` credential, never any decision on a request** |
| `administrator` | `administrator@example.com`, `administrator2@example.com` | All of the above, plus `production` credentials, member roles and data requests. **Never any decision on a request** |
| `compliance_approver` | `compliance@example.com` | Claim, approve, deny and return production access requests. **Never an application, a credential or a webhook endpoint** |
| `analyst` | `analyst@example.com` | **Nothing. Every mutating endpoint is denied** |

Every role reads every route in its own organisation; only writes differ. The
`compliance_approver` additionally reads the full audit log.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI
is not authorization: a direct API call from a `developer` session to any
`compliance_approver`-only endpoint must be rejected by the server (an unauthorized request is
denied, not served), leaving the protected state unchanged.

A `developer` writes only against applications owned by their own team:
`developer@example.com` is on `Payments Integration`, `developer2@example.com` on
`Risk Platform`. `administrator2@example.com` belongs to a different organisation and is denied
every read and every write on every Vantor record.

---

## Core features

### Production access requests
A request is per application, per environment, per product, in one of the nine states named in Data model.

1. **A `developer`, an `administrator` or an `analyst` calling claim, approve, deny or return is denied by the server, and the request's `state`, `claimed_by` and `decided_by` are unchanged on a fresh read.** Only a `compliance_approver` decides.
2. **The filer can never decide their own request, even holding `compliance_approver`.** `AR-1004` was filed by `compliance@example.com`, the only Vantor approver, so no session may approve it: the attempt is denied and `AR-1004` stays `submitted`.
3. All seven answers named in Data model are required before a submit; a submit missing any is rejected as invalid and the request stays `draft`.
4. Claiming moves `submitted` to `in_review`; a decision moves it to `returned`, `approved` or `denied`; `returned` returns to `submitted`. A decide against any other state is a conflict.
5. Approving stamps `decided_by` and `decided_at` and moves that one entitlement to `live` in that environment alone. Denying needs a reason of 1 to 280 characters.

### Connections
6. Status is derived from the eight values in Data model. `requires_reauthentication` and `institution_unavailable` are told apart at a glance.
7. **No console response carries a balance, a transaction, an account number or an identity record.** A connection exposes institution, status, consent scope and expiry, refresh history and a masked reference such as `cst_****7Q2A`.

### Applications and credentials
8. An application fixes its region at creation and exists in `sandbox`, `development` and `production` at once, each with its own credentials and entitlements.
9. A created credential returns its secret once, `sec_` plus 32 lowercase hex, for example `sec_2b9f41c7d0a84e6395fd1c8b7a02e5d4`. No later read returns it; only the last four, `e5d4` there, the date and the creator remain.
10. At most two unrevoked credentials per environment; a third is rejected as invalid. A `production` credential expires after 365 days.
11. A secret never reaches a list response, an error message, a log line or an audit entry.

### Audit
12. Every mutation appends one entry to a gapless per-organisation sequence from `1`. No route updates or deletes one, and the chain a caller reads back verifies against the hash rule in Data model.

### The console's public edges
13. A terms page is reachable from the footer of every route and from the sign-in route.
14. A first-time visitor is asked once about non-essential cookies, and the answer survives a reload.
15. Every internal link on every route resolves.
16. A sign-in submitted repeatedly in quick succession is refused, as is any form whose unattended decoy field carries a value.

---

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/login` | sign in through the identity provider | none |
| `/` | overview: waiting tasks, health, top failures, quota | any role |
| `/applications` | application list, newest activity first | any role |
| `/applications/{slug}` | one application, one tab per environment | any role |
| `/applications/{slug}/{environment}` | credentials and entitlements | any role |
| `/access-requests` | the request board, columns by state | any role |
| `/access-requests/{id}` | one request, its answers and history | any role |
| `/connections` | the connection board, columns by status | any role |
| `/connections/{id}` | one connection, its consent scope | any role |
| `/webhooks` | endpoints and their verification state | any role |
| `/team` | members, roles and teams | any role |
| `/data-requests` | consumer export and erasure requests | any role |
| `/audit` | the appended log | any role |
| `/usage` | requests used against committed volume | any role |

**Entry and redirects.** Any route but `/login` redirects there when unauthenticated; sign-in lands on `/`; logout revokes the token and returns to `/login`. A token expiring mid-action fails that action cleanly, keeps what was typed, and offers re-authentication in place. A member who may read a route but not write it sees the write control replaced by a line naming the role that holds the action, never an error page and never a blank column.

**Journeys.**
1. As `developer@example.com`, open `/applications`, select `Vantor Payouts`, open `development`, then `/connections`. `con_9km4` sits in the `requires_reauthentication` column and `con_3wp8` in `institution_unavailable`. Opening `con_9km4` names the institution, the consent scope and `cst_****9K4B`.
2. Open `/applications/vantor-payouts/production`, where the `identity` row reads `off`. Request production access: a modal collects the seven answers and submitting lands on a confirmation page naming what was filed.
3. As `compliance@example.com`, claim `AR-1001` in `/access-requests`: the card moves to the `in_review` column. Approve it: only `transactions` becomes `live` in `production` on `Vantor Payouts`, and `/audit` gains a chained entry.
4. Open `AR-1004`, filed by this same account. The approve control is absent with a line saying why, and a direct approve call is denied with `AR-1004` still `submitted`.

**States.** Every board carries an empty state saying what would fill it, a loading state shaped like its own columns, and a filtered-empty state with the filter summary, a clear control and the unfiltered count. Lists are cursor-paginated and report a total. A denial names the missing permission and the role that holds it, never a person. An error re-renders the route with the failure named and the request identifier quoted.

---

## UI/UX notes

The north star: a member arriving at a board should see, before reading, which requests are waiting on them and which are waiting on somebody else. The register is operational, a console opened many times a day to act, so it reads quiet and organised for scanning and repeated action, never as a marketing composition.

The direction is layered and translucent: depth-driven hierarchy, expressed by surfaces sitting at readable depths over one another rather than by rules and boxes. A panel floating over a board is frosted enough that the column beneath stays legible as context, never so frosted that text on it loses contrast. One refined sans carries the surface, with monospace for tabular numerals so counts and identifiers align. Density is comfortable: rows breathe and a full working set still fits one screen.

Motion character is eased: considered entrance and exit easing, so movement reads as a designed interface rather than a machine. Anything arriving carries a slight overshoot that settles, anything leaving is pulled away and ends flat, and every transition shares that character rather than inventing its own. One switch sets every duration to nothing, and the reduced-motion rule is wired through that switch alone.

The layout archetype is a persistent left sidebar carrying the primary navigation, collapsible and remembering its state. The two queues are boards: columns by state on the requests board, columns by status on the connections board, one card per record. Creating anything opens a modal over the board; committing a decision lands on a full confirmation page naming what changed, rather than a transient message.

Colour is used by role, never by ramp: background, surface, primary text, muted text, border, one primary action with its own pressed state, and a distinct meaning-carrying colour each for failure, success and in-progress. A status chip is filled from the lightest step of its family and bordered from the darkest, which is why a board reads as pastel rather than as traffic lights. The colour meaning something has gone wrong appears nowhere else.

Buttons carry three variants across five states, with hovered, pressed and loading deliberately identical so pressing flows into waiting. Inputs carry six states, and only the invalid one changes the field's background, always with its message text, because meaning is never carried by colour alone. Escape closes any overlay; the secret-reveal overlay closes only by an explicit control.

Contrast meets WCAG AA on the pairs used, including text over any translucent surface. Every control is reachable by keyboard navigation with a visible focus ring on every ground, icon-only controls carry labels, and touch targets are comfortably sized. The layout holds at every viewport width with no horizontal page overflow, and boards become one stacked column below the desktop breakpoint. Commit to light; dark is optional and is not judged.

Depth over dividers, calm over expressive. The exact shades are yours, so long as they hold the rules above.

---

## Front-end specification

This section carries the measured design system. It names every colour by family, tone and
shade rather than by value: a value is something to copy, a described colour is something to
choose, and the choice is what this section is asking for.

### Scaling

Every spacing value, padding and control height is authored as a multiple of one root unit,
`--unit`, which is `0.8rem`. A value that cannot be written as `calc(var(--unit) * n)` is a
defect. Type sizes and control heights are in `rem`, never `px`, so a visitor who has raised
their browser text size gets a larger console rather than a broken one:
`--height-large-form-controls` is `5.6rem`, seven units; `--font-size-large-form-controls` is
`2rem`; `--font-size-med` is `1.4rem`. `--border-radius` is `0.2rem` on the legacy surface, while
the console surface uses the pixel radii below, which is a deliberate difference: a pill that
scales with text stops being a pill.

### The palette, by family

Six hue families, each running a 100 to 1000 lightness scale from near-white to near-black. Two
generations ship: the legacy ramps carry the status system and the form controls, and the console
ramps carry the shell, its buttons and its inputs.

- **Neutral** is the structural family and does most of the work. The legacy ramp runs ten steps
  from a near-white neutral through mid neutrals to a near-black neutral. The console ramp is
  warmer and shorter: pure white at the top, then a near-white neutral, two light neutrals, a mid
  neutral, two deep neutrals and a near-black neutral at the bottom. The two ramps are not
  interchangeable and both ship.
- **Cyan** is the interactive family: the colour a control moves to when it is pointed at,
  focused or pressed. It runs from a near-white cyan through a light cyan and a mid, vivid cyan
  down to a deep cyan. The pressed step is one shade below the hover step, and no other family
  signals interaction.
- **Teal** is the success family, from a near-white teal through a light teal to a mid, vivid teal
  and a deep teal.
- **Red** is the failure family. The legacy ramp runs from a near-white red through a light red to
  a mid, vivid red and a deep, muted red. The console red ramp is separate and warmer, six steps
  from a near-white warm red down to a deep, muted red, and it is the one the form controls use.
- **Amber** is the warning family, from a near-white amber through a light amber to a mid, vivid
  amber and a deep amber. One amber sits outside the ramps entirely and is the warning border.
- **Indigo** is the informational family, from a near-white indigo through a light indigo to a
  mid, vivid indigo and a deep indigo.
- **Blue** and **orange** appear only twice each and only outside the console: a near-black,
  muted blue is the ground the sign-in route and the secret-reveal overlay stand on, and a mid,
  vivid orange is the tile colour a mobile browser reads from the document head.

The accent gradient runs from a light, vivid teal into a mid, vivid cyan at a shallow angle, with
a stretched variant where a wider run is needed. It appears on exactly one surface per route and
never behind text that must meet contrast.

No colour is authored outside these families. A component asks for a semantic role, never for a
ramp step.

### The semantic layer

No component reaches into a ramp. Every step is re-exported under a role name, and the roles are
grouped by what they paint.

**Fill.** A page background, a secondary background one step darker, a tertiary background one
step darker again, an inverse background at the near-black neutral, a default fill, an inverse
fill, and the interactive set: default, hover, pressed, a low-contrast pressed wash, disabled,
and error.

**Text.** High, default and low contrast over a light ground; the same three inverted for a dark
ground; and the interactive set: default, hover, pressed, disabled, plus a destructive pair.

**Border.** High, default and low contrast; the interactive set of default, filled, hover,
focused, pressed, disabled and error; the status set; and a destructive trio at low, default and
high contrast.

Reproduce two asymmetries exactly, because they are what the system reads like:

1. **The status family borders with the darkest step of its family and fills with the lightest.**
   A success chip is a near-white teal fill inside a mid, vivid teal border; attention is a
   near-white cyan fill inside a deep cyan border; warning is a near-white amber fill inside the
   amber border colour; error is a light red fill inside a deep red border; default is a light
   neutral fill inside a mid neutral border. That single decision is why the chips read as pastel
   rather than as traffic lights.
2. **Text hover and text pressed are the same step, while fill and border move one step darker on
   press.** Text does not darken on press; its container does.

### The unresolved tokens

Seven tokens resolve to `transparent` on `:root`: `--border-color`, `--button-bg-color`,
`--button-border-color`, `--button-text-color`, `--label-color`, `--placeholder-color` and
`--text-color`. They are per-component slots. Keep them inert at the root so a component that
forgets to set one renders invisibly. Do not give them a fallback colour: the loud failure is the
point.

### Radius, elevation and depth

Radius scale, by frequency of use: `2px` is the default control radius and
`--button-border-radius`; `8px` for card icons and navigation panel bodies; `4px` for post cards
and image wrappers; `100px` for tag filters; `1px` for inline spans; `999px` for navigation links
and full-width rounded buttons; `12px` for menu panels; `16px` for the mobile menu dialog and
navigation panel inners; `6px` for tab buttons; `40px` for the floating navigation bar;
`20px 20px 0 0` for a banner's top corners only. Both pill radii, `100px` and `999px`, are in use
on different component generations; reproduce both.

Elevation is four shadows, authored twice, once in `rem` and once in `px`:
`0 1.6rem 2.4rem`, `0 0.8rem 1.6rem`, `0 0.8rem 0.8rem` and `0 0.2rem 0.4rem`, mirrored as
`0px 16px 24px`, `0px 8px 16px`, `0px 8px 8px` and `0px 2px 4px`. All eight carry the same
colour: one near-black neutral at eight per cent. The scale is built from distance alone, never
from opacity, which is why the surfaces read as crisp rather than smudged.

The floating navigation bar carries a three-part shadow: an outer contact shadow at six per cent
black, an inset one-pixel white rim at twelve per cent, and a wider soft drop in a mid neutral at
twelve per cent. The rim is what makes the bar read as glass rather than as a grey rectangle. A
dropdown panel uses the same recipe one step tighter.

### The component state matrix

Buttons are a full cross product of three variants and five states, with four properties each.

| Variant | State | Background | Border | Text and icon |
|---|---|---|---|---|
| solid | resting | near-black neutral | transparent | white |
| solid | hovered | near-black neutral at 84 per cent | transparent | white |
| solid | pressed | near-black neutral at 84 per cent | transparent | white |
| solid | loading | near-black neutral at 84 per cent | transparent | white |
| solid | disabled | mid neutral | transparent | white |
| outlined | resting | transparent | light neutral | near-black neutral, icon one step lighter |
| outlined | hovered | mid neutral at 8 per cent | near-black neutral at 84 per cent | near-black neutral, icon one step lighter |
| outlined | pressed | mid neutral at 8 per cent | near-black neutral at 84 per cent | near-black neutral, icon one step lighter |
| outlined | loading | mid neutral at 8 per cent | near-black neutral at 84 per cent | near-black neutral, icon one step lighter |
| outlined | disabled | transparent | mid neutral | mid neutral |
| ghost | resting | transparent | transparent | near-black neutral, icon one step lighter |
| ghost | hovered | mid neutral at 8 per cent | transparent | near-black neutral, icon one step lighter |
| ghost | pressed | mid neutral at 8 per cent | transparent | near-black neutral, icon one step lighter |
| ghost | loading | mid neutral at 8 per cent | transparent | near-black neutral, icon one step lighter |
| ghost | disabled | transparent | transparent | mid neutral |

Three consequences, all deliberate. Hovered, pressed and loading are identical in every variant,
so a loading button feels like a continuation of the press rather than a new screen state. A solid
button lightens on contact by going translucent over whatever is behind it rather than by moving
down the ramp, so its hover colour on a dark ground differs from its hover colour on white, and
that is correct. Icon and text differ by one ramp step in the non-solid variants, because an icon
is optically heavier than a letter at the same value.

Text inputs carry six states:

| State | Background | Border | Label | Message | Text |
|---|---|---|---|---|---|
| resting | white | light neutral | mid neutral | mid neutral | deep neutral |
| hovered | white | mid neutral | mid neutral | mid neutral | deep neutral |
| focused | white | deep neutral | mid neutral | mid neutral | deep neutral |
| pressed | white | near-black neutral at 84 per cent | mid neutral | mid neutral | deep neutral |
| disabled | light neutral | mid neutral | mid neutral | mid neutral | mid neutral |
| invalid | near-white warm red | mid red | deep red | deep red | deep red |

The invalid state is the only one that changes the background; every other state moves the border
alone. It is always accompanied by its message text.

The legacy surface keeps its own input set, including a full dark-field variant, because the
sign-in route puts inputs on a dark ground. Radio controls, tabs and tooltips each carry their own
role set on the same principle: the interactive states move to the cyan family, and the tooltip is
dark only. A badge never inverts its text; it changes its fill.

### Typography

No font file ships. Three faces are proprietary and are replaced by stacks that may be named: the
brand text face and the interface face fall back to
`"Inter var","Inter",-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif`; the display
face, a high-contrast display serif, falls back to
`"Playfair Display",Georgia,"Times New Roman",serif`; `Inconsolata` and `Monaspace Neon` are open
licence and may be named directly. `--font-stack-sans` is `Cern,Helvetica,Arial,sans-serif` and
`--font-stack-monospace` is `Inconsolata,Consolas,Courier,monospace`. All faces load with
`font-display: swap`: the copy is the product here, and a blocked render costs more than a reflow.

The scale actually rendered, in descending order of use: `16px` at `24px` for body copy; `18px`
semibold at `24px` for card titles and menu labels; `14px` at `21px` for secondary and caption
copy; `16px` semibold at `24px` for emphasised body; `16px` at `16px` for single-line list rows;
`16px` medium at `24px`; `18px` semibold at `28px` and at `23.4px`; `16px` semibold at `32px`;
`14px` at `20px` for dense secondary copy; `24px` for sub-headings, with and without a `32px`
leading; `12px` for legal and meta; `14.4px` bold at `14.4px` for the wordmark lockup; `10px` at
`11.5px` for the smallest legal type; `12px` semibold at `18px` for chips and tags; `12.992px` at
`19.488px`, which is a `0.812rem` token at a 1.5 ratio; `16px` bold at `21.3333px`, which is
`1.3333rem`; and `8.5px` for the smallest print. Author the token, never the fraction. The body
ratio is 1.5 and holds from `10px` to `18px`; display sizes above `24px` set their own leading
between 1.0 and 1.15, which is what makes a two-line headline lock up as a block.

### Motion

Motion is tokenised as tightly as colour, which is why the product feels coherent across every
surface. Six families, and everything belongs to one:

| Family | Character | Duration | What uses it |
|---|---|---|---|
| arrive | overshoots slightly and settles | `350ms` | panels, cards, anything entering |
| adjust | even, no character | `100ms` | colour, cross-fades, small corrections |
| leave | pulled away, ending flat | `0.2s` | modals and panels closing |
| settle | a damped bounce | per component | held in the token set, used by no console surface |
| sweep | even and continuous | `2500ms` to `10000ms` | spin, marquee, sheen |
| scrub | position-driven | none | tied to scroll position |

Arrive and leave are asymmetric on purpose: things spring in and get pulled out. The primary
duration is `350ms` and the secondary is `100ms`; a modal opens over `0.2s` and closes over
`0.5s`; the general transition duration is `35ms` with a `225ms` delay on the one panel that
waits before closing.

`--debug-animation` at `0ms` is a live kill switch. Wire the reduced-motion rule through that one
token rather than through a second mechanism. `transition: all` appears nowhere. `will-change` is
applied and removed around an animation and never left on. Every infinite loop pauses off screen
and under reduced motion.

### Layer order

Four tokens name the intentional layers: `--z-index-dropdown` `10`, `--z-index-tooltip` `100`,
`--z-index-modal` `1000`, `--z-index-date-input` `10000`. Use those four and nothing else in
application code. The maximum-integer band belongs to third-party embeds and is a reserved band
the build does not enter.

### Skeletons and loading

The skeleton ground is a light neutral and the indeterminate spinner is a mid, vivid cyan. The
sheen is a horizontal gradient from fully transparent white, to white at half opacity in the
middle, to two fully transparent stops at the end, swept left to right by a keyframe whose whole
body is a translation to `100%`. The two trailing stops are both fully transparent and one is
redundant; reproduce the gradient as given anyway.

Every list, card grid and table renders a skeleton of the correct shape and row count while
loading, never a spinner in an empty rectangle. The spinner is for indeterminate inline actions
only, such as a button in its loading state.

### Module and component architecture

The front end is organised as modules with one owner each, not as a flat folder of views: a shell
module for the sidebar, header and account menu; a board module shared by the two column routes; a
form module carrying the seven-question modal; a table module carrying the loading skeleton and
the empty, filtered-empty and denied states; and a token module that is the single home of every
value in this section. The information architecture above is the contract between them: a module
never reaches into another module's tokens or markup.

### Performance budgets

Each route ships only what that route needs. The console's first screen must be usable on a
mid-range laptop over a slow connection, and no route downloads another route's code. No scroll
listener performs layout work, no font file is fetched from a third party, and the zero-asset
substitution rule holds: no image, font, video or texture file ships with the build, and every
mark is drawn from geometry authored in the markup.

### Motion safety and assistive technology

Reduced motion is a safety requirement, not a preference: a visitor who has asked their device for
less movement must get a console with no parallax, no continuous loop and no settle, and the
vestibular risk is the reason. The board routes, the request form and the secret-reveal overlay
are operable and announced correctly with assistive technology, including the focus move into an
overlay and back out of it on close.

### Responsive and accessibility floors

Four breakpoints only; component-specific rules are container queries. No horizontal page overflow
at any breakpoint on any route. Every surface is usable at 400 per cent zoom. Boards become one
stacked column below `1024px`. Hover effects sit inside a hover-capable query and do not stick on
touch. Every hidden element is `inert` as well as transparent. One `h1` per route, no skipped
heading levels, landmarks on every route, no positive `tabindex`, and a skip link first in the
order reaching `#main-content`. Contrast is checked against the role pairs above as a failing
build step, and every interactive element is reachable and operable by keyboard with a visible
focus indicator on every ground.

### Copy

No typographic dash appears anywhere in the product's copy. Consumer-facing wording is written in
plain sentences. The same sentence describing a data class is rendered identically wherever it
appears, so nobody reads two different descriptions of one thing.

### The three identity spaces

Three separate spaces exist across the wider network and they never meet: the operator space
holding members of customer organisations, the consumer space holding the end users who linked an
account, and the machine space holding an application's own credentials. This console serves the
operator space alone. It shares no table, no cookie, no signing key and no session store with
either of the other two, because a design in which a consumer row and a member row can be confused
is the privilege escalation this product cannot survive. A machine credential authenticates every
call it makes and holds no session at all.

---

## Technical requirements

The app is an **Express** service rendering **Nunjucks** templates on the server, with **Alpine.js** attached to that rendered markup for progressive behaviour. The rendering model is a progressively enhanced multi-page application: every route is produced as complete HTML on the server and arrives fully formed on first paint, so the browser receives rendered markup rather than a bundle that then fetches its own content. There is no client-side router, no hydration step and no second rendering tree. Alpine.js carries exactly three enhancements: the create-application and request modals, the collapsible sidebar, and the board column filters. The same Express process serves the JSON API under `/api` on the same origin.

Storage is **PostgreSQL**, reached at `DATABASE_URL`. Identity is **Keycloak**, reached at
`AUTH_ISSUER_URL`, with `AUTH_CLIENT_ID` and `AUTH_CLIENT_SECRET` for the confidential client.
The app's public origin and port come from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Read every
one of them from the environment; never hardcode a host or a port.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
services available in this environment are PostgreSQL and Keycloak, and reaching for anything
else is a contract violation. Both are already running and reachable at those variables; do not
download, install, compile or start a copy of either.

`GET /api/health` returns `200` with a JSON body once seeding has completed and both backing
services are reachable.

No credential, API key or admin token appears in anything the browser downloads: no secret
value reaches rendered markup, a script the console serves, or any response body a browser can
read.

Every request is logged as one structured JSON line carrying the request identifier, the
organisation, the environment, the acting principal's email and the route. A request body is
never logged. A secret value is never logged, never returned in an error message and never
written to an audit entry.

One request identifier is generated when a request arrives and is carried into the log line,
the audit entry, the error response body and the `X-Request-Id` response header. It is the
value a support conversation starts with.

Authorization is decided in one place that every route consults, taking the principal, the
action, the resource, the resource's environment, the owning team and the approval state of
the entitlement behind it. The default answer is deny, and an explicit denial recorded against
a member defeats every allow that member otherwise holds. The same answer is applied again when
rows are selected, so a route that forgets to scope returns nothing rather than everything.

Sessions are opaque bearer tokens, expire 8 hours after issue, and are revoked at logout. They
are required on every endpoint except `POST /api/auth/login` and `GET /api/health`.

### Backend architecture and data conventions

The service is one process with three layers: routes, a decision point and a data layer. The
conventions below hold across every table. Identifiers exposed outside the service are opaque
and type-prefixed, never sequential, because a sequential connection identifier leaks volume
and invites enumeration. Every table carrying organisation data holds a non-nullable
organisation column and is isolated on it at the data layer, so row-level isolation is a
property of the store rather than a convention every query has to remember: a read issued
with a valid session for another organisation returns nothing. Every foreign key states what
happens to its children explicitly. Soft deletion is for configuration only.

### Idempotency, versioning and growth

Seeding is idempotent, and so is every job the service runs: running one twice produces one
effect. A request form carries a version, and a decision is recorded against the exact
version it was made on, so re-opening a form after a decision starts a new version rather
than rewriting history. The API is versioned by header, never by path, and an additive change
ships without a version bump while a removal requires one; deprecation is announced on the
response before a route is withdrawn.

Indexing follows growth: the audit table is the one that grows without bound and is never
deleted from, connections are read by organisation and by status, and every list route is
cursor-paginated on an indexed key. No route can reach an unbounded scan.

### Rate limiting and quota

Every response carries the limit, the remaining count and the reset time for the bucket it was
counted against. A caller over its limit is refused with a `Retry-After` in seconds rather
than served slowly. Buckets are per organisation and per session; a single session cannot
consume the organisation's whole allowance. Usage is derived from the recorded request stream
rather than counted in the request path, and the derivation is reconciled against the raw
count before it is shown.

### Caching and validation

A response that may be cached carries its own validation token so a repeat read can be
answered without re-computing it, and every cache key includes the organisation, the
environment and the region. An authenticated route is never stored in a shared cache. Any
change to a member's role or to an entitlement is effective on the next decision, so nothing
is served from a cached authorisation answer after the grant behind it moved.

### Regionality, residency and deletion

An application's region is chosen once and is then immutable, because changing it later would
mean moving consumer records across a border. Residency follows from it: a record created
under an application is read only in that application's region, and a cross-region read is
refused with the resource's region named. Erasure is a propagation problem rather than a
delete: completing an `erasure` data request must remove the derived rows everywhere they
were written, and the request cannot report `completed` before every one of them is gone. The
audit entry recording an erasure survives the erasure.

### Governance and the regimes that apply

Which obligations attach to an application is computed from its region and the products
entitled to it, never configured by hand, and the seven-question form asks what those
obligations require. The audit chain is the evidence: it is appended to in the same
transaction as the change it records, so a mutation that cannot be recorded fails rather than
succeeding silently.

### Observability, telemetry and degradation

One structured line per request is the telemetry: request identifier, organisation,
environment, principal and route, and never a body and never a secret. When PostgreSQL is
unreachable the health route reports it and every write is refused with an explanation rather
than queued, because a queued write against financial access configuration applied later, when
nobody is watching, is worse than a write that plainly failed. When Keycloak is unreachable,
sessions already issued continue until they expire and new sign-ins fail with a message naming
the provider. No degraded mode changes behaviour silently: every one of them says on screen
what is reduced.

### Workspace, switching, settings and the three views

A session is scoped to exactly one organisation and one workspace, and that organisation is in
the route rather than only in the session, so a link pasted into a chat resolves to the right
organisation or to a clear permission error, never silently to a different one. Switching
organisation, the settings groups behind it and bulk operations over a filtered set are all
governed by the same decision point. The companion's three operational views (connections,
activity and logs) have three different grains, three different retentions and three different
permission requirements; this build ships the connections view alone and does not merge the
other two into it.
---

### Operational limits carried here rather than in the feature rules

A re-authentication prompt addressed to more than 100 connections at once is rejected unless a
second approver has signed it, and the rejection names the count and the threshold. A dry run
reporting the count, a sample and the estimated completion is offered before the action is armed.

Another organisation's records are denied on every read and every write, and never appear in a
list a member of a different organisation reads. That holds at the route layer and again when
rows are selected.

Every route is readable by every signed-in member of the organisation that owns the record; only
the write set differs by role.

---

## Data model

Thirteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
not a secret. Hash it as normal; the exact literal must work at login, and it must be written
into `/app/USER_README.md` alongside each account so a grader can sign in.

**organisation** - `name` (unique), `region` (`us` or `eu`), `committed_requests`, `status`.

**team** - `organisation_id`, `name`, unique together.

**member** - `organisation_id`, `email` (unique), `display_name`, `role` (one of `developer`,
`administrator`, `compliance_approver`, `analyst`), `team_id` (null means organisation-wide),
`status` (`active` or `deactivated`). A member is never deleted.

**application** - `organisation_id`, `team_id`, `name`, `slug` (unique within the
organisation), `region`, `status`, `created_by_member_id`, `last_activity_at`. `region` is
fixed at creation: no later write changes it, and the attempt is rejected as invalid.

**app_environment** - `application_id`, `kind` (`sandbox`, `development`, `production`),
`connection_cap`. Exactly three rows exist per application from the moment it is created, and
`development.connection_cap` is `25`: a connection created past that cap is rejected as
invalid, reporting the current count and the cap rather than failing silently.

**api_credential** - `application_id`, `environment`, `public_identifier`, `secret_hash`,
`last_four`, `created_by_member_id`, `created_at`, `last_used_at`, `expires_at`, `revoked_at`.
`secret_hash` is one way: no column anywhere can return a secret, which is what makes the
show-once rule true rather than a policy. At most two rows per application per environment have
a null `revoked_at` at any time, and that must hold under concurrent creation attempts, not
merely in application-level checks: two simultaneous creations against an environment already
holding one live credential must not both succeed. Exactly one wins, the other is rejected, and
a failed creation leaves no row behind.

**product** - `key` (one of `auth`, `balance`, `identity`, `transactions`, `signal`,
`transfer`), `name`, `summary`, `regulatory_class`.

**entitlement** - `application_id`, `environment`, `product_key` (unique together), `state`
(`off`, `pending`, `live`, `revoked`), `approved_request_id`, `review_due_at`.

**access_request** - `id` in the form `AR-` followed by four digits, `application_id`,
`environment`, `product_key`, `state` (one of `draft`, `submitted`, `in_review`, `returned`,
`approved`, `denied`, `live`, `revoked`, `suspended`), `form_version`
starting at `1`, `requested_by_member_id`, `claimed_by_member_id`, `decided_by_member_id`,
`decided_at`, `reason`, `submitted_at`. Two invariants hold at all times:
`decided_by_member_id` is never equal to `requested_by_member_id`, and `claimed_by_member_id`
and `decided_by_member_id` only ever hold a member whose role is `compliance_approver`. Both
must hold under concurrent decisions, not merely in application-level checks: two simultaneous
approvals of one `submitted` request must not both succeed, exactly one wins, the other is
rejected, and the losing attempt leaves no audit entry.

**access_request_answer** - `access_request_id`, `question_key`, `value`, `form_version`,
`answered_at`. The seven question keys are `intended_use`, `consumer_disclosure`,
`retention_period_days`, `sub_processors`, `security_contact`, `expected_monthly_volume` and
`regulatory_basis`. All seven must carry a value before a request may leave `draft`; a submit
missing any one of them is rejected as invalid and the request stays `draft`.

**connection** - `id` in the form `con_` followed by four lowercase alphanumerics,
`organisation_id`, `application_id`, `environment`, `institution_name`, `consumer_reference`,
`status` (one of `healthy`, `degraded`, `requires_reauthentication`,
`institution_unavailable`, `revoked_by_consumer`, `revoked_by_customer`, `expired`,
`suspended`), `status_reason`, `consent_expires_at`, `last_refreshed_at`, `last_error_code`.
`status` is derived on read from the refresh history and the consent record, not stored as free
text. There is no balance column, no transaction column, no account-number column and no
identity column in this build.

**webhook_endpoint** - `application_id`, `environment`, `target_url`, `status` (`unverified`,
`verified`, `disabled`), `subscribed_event_types`, `verification_token`, `verified_at`. At most
five rows per application per environment, and `target_url` must begin `https://`. A row is
created `unverified` and receives nothing until it answers the challenge carried in
`verification_token`. `subscribed_event_types` defaults to empty and holds values drawn from
`connection.created`, `connection.updated`, `connection.requires_reauthentication`,
`connection.revoked_by_consumer`, `connection.revoked_by_customer`, `connection.expired`,
`connection.error`, `entitlement.approved`, `entitlement.revoked`, `key.expiring` and
`key.revoked`. A delivery payload carries references only, never consumer data.

**data_request** - `id` in the form `dsr_` followed by four digits, `organisation_id`, `kind`
(`export` or `erasure`), `consumer_reference`, `state` (`received`, `in_progress`, `completed`,
`rejected`), `received_at`, `due_at` which is `received_at` plus 30 days, `completed_at`.

**audit_entry** - `sequence`, `organisation_id`, `actor_email`, `action`, `resource_type`,
`resource_id`, `occurred_at`, `previous_hash`, `entry_hash`. The sequence is gapless per
organisation and starts at `1`. Entries are only ever appended; no route updates or deletes
one, and an attempt to do so is rejected. `entry_hash` is the lowercase hex SHA-256 of
`previous_hash`, `sequence`, `actor_email`, `action`, `resource_type`, `resource_id` and
`occurred_at` joined by a single `|` in that order, with a `previous_hash` of sixty-four `0`
characters on the first entry of an organisation. Worked example: the first Vantor entry, with
`sequence` `1`, `actor_email` `developer@example.com`, `action` `application.created`,
`resource_type` `application`, `resource_id` `vantor-payouts` and `occurred_at`
`2026-01-05T09:00:00Z`, hashes the exact string
`0000000000000000000000000000000000000000000000000000000000000000|1|developer@example.com|application.created|application|vantor-payouts|2026-01-05T09:00:00Z`.

### Seed data

Two organisations: `Vantor`, region `us`, `committed_requests` `50000`; `Wrenwood`, region
`eu`, `committed_requests` `50000`.

Two Vantor teams: `Payments Integration`, `Risk Platform`.

Six members, all with the password above:

| Email | Name | Organisation | Role | Team |
|---|---|---|---|---|
| `developer@example.com` | Nadia Brandt | Vantor | `developer` | Payments Integration |
| `developer2@example.com` | Owen Keeler | Vantor | `developer` | Risk Platform |
| `administrator@example.com` | Priya Raman | Vantor | `administrator` | organisation-wide |
| `compliance@example.com` | Hugo Lindqvist | Vantor | `compliance_approver` | organisation-wide |
| `analyst@example.com` | Mei Sandoval | Vantor | `analyst` | organisation-wide |
| `administrator2@example.com` | Tomas Beck | Wrenwood | `administrator` | organisation-wide |

Four applications: `Vantor Payouts` (`vantor-payouts`, Payments Integration, `us`),
`Vantor Risk Signals` (`vantor-risk-signals`, Risk Platform, `us`), `Vantor Ledger Sync`
(`vantor-ledger-sync`, Payments Integration, `us`), and `Wrenwood Onboarding`
(`wrenwood-onboarding`, Wrenwood, `eu`).

Six products: `auth`, `balance`, `identity`, `transactions`, `signal`, `transfer`.

Entitlements: every application holds one row per environment per product. `sandbox` and
`development` rows are `live` from creation and need no approval. `production` rows are `off`,
except `Vantor Ledger Sync` / `production` / `balance`, which is `live` and points at
`AR-1003`.

Five access requests:

| Id | Application | Environment | Product | State | Requested by | Claimed by |
|---|---|---|---|---|---|---|
| `AR-1001` | Vantor Payouts | `production` | `transactions` | `submitted` | `developer@example.com` | none |
| `AR-1002` | Vantor Risk Signals | `production` | `signal` | `in_review` | `developer2@example.com` | `compliance@example.com` |
| `AR-1003` | Vantor Ledger Sync | `production` | `balance` | `approved` | `developer@example.com` | `compliance@example.com` |
| `AR-1004` | Vantor Payouts | `production` | `transfer` | `submitted` | `compliance@example.com` | none |
| `AR-2001` | Wrenwood Onboarding | `production` | `identity` | `submitted` | `administrator2@example.com` | none |

All five carry a complete set of seven answers.

Four connections, all on `Vantor Payouts` / `development`:

| Id | Institution | Status | Consumer reference |
|---|---|---|---|
| `con_7hq2` | Gantry Bank | `healthy` | `cst_****7Q2A` |
| `con_9km4` | Anchor National | `requires_reauthentication` | `cst_****9K4B` |
| `con_3wp8` | Gantry Bank | `institution_unavailable` | `cst_****3W8C` |
| `con_5tz1` | Metro Credit Union | `revoked_by_consumer` | `cst_****5T1D` |

One webhook endpoint: `https://hooks.vantor.example/ravel` on `Vantor Payouts` /
`development`, `verified`, subscribed to `connection.created`,
`connection.revoked_by_consumer` and `entitlement.approved`.

Two data requests: `dsr_4410`, `erasure`, `received`, `cst_****9K4B`; and `dsr_4411`,
`export`, `completed`, `cst_****7Q2A`.

Seeding must be idempotent: restarting the app must not duplicate rows.

---

## Constraints

- One console per organisation. No marketing site, no documentation site, no embedded
  bank-connection widget, no consumer portal.
- No billing, invoices, price books or payment collection. No money movement, identity
  verification sessions or watchlist screening.
- No single sign-on configuration screen, directory provisioning or break-glass principal: the
  identity provider is already configured in this environment.
- No external network calls at runtime beyond PostgreSQL and Keycloak. No email, no SMS, no
  object store, no third-party analytics. A webhook endpoint is recorded and verified, never
  actually delivered to.
- No native app, no offline mode, no data export file generation.
- Stay responsive with 4 applications, 12 environments, 5 access requests, 4 connections and
  10,000 audit entries.

---

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses.
  Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
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
| `POST /api/auth/login` | `{"email","password"}` | `{"access_token","role","organisation"}` |
| `POST /api/auth/logout` | none | `{"revoked": true}` |
| `GET /api/me` | none | `{"email","display_name","role","organisation","team"}` |
| `GET /api/health` | none | `{"status":"ok"}` |
| `GET /api/applications` | `?environment=&cursor=` | a top-level JSON array of applications |
| `POST /api/applications` | `{"name","team","region"}` | the created application |
| `GET /api/applications/{slug}` | none | the application with its three environments |
| `GET /api/applications/{slug}/{environment}` | none | `{"credentials":[],"entitlements":[]}` |
| `POST /api/applications/{slug}/{environment}/credentials` | none | `{"public_identifier","secret","last_four","expires_at"}`, the only response ever carrying `secret` |
| `GET /api/applications/{slug}/{environment}/credentials` | none | a top-level JSON array, each item carrying `public_identifier`, `last_four`, `created_at`, `created_by`, `last_used_at`, `expires_at`, and never `secret` |
| `POST /api/credentials/{id}/revoke` | none | the revoked credential |
| `GET /api/products` | none | a top-level JSON array of products |
| `GET /api/access-requests` | `?state=&application=&cursor=` | a top-level JSON array of requests |
| `POST /api/access-requests` | `{"application","environment","product_key","answers"}` | the created request in `draft` |
| `GET /api/access-requests/{id}` | none | the request with its answers and its history |
| `POST /api/access-requests/{id}/submit` | none | the request in `submitted` |
| `POST /api/access-requests/{id}/claim` | none | the request in `in_review` |
| `POST /api/access-requests/{id}/approve` | none | the request in `approved` |
| `POST /api/access-requests/{id}/deny` | `{"reason"}` | the request in `denied` |
| `POST /api/access-requests/{id}/return` | `{"reason"}` | the request in `returned` |
| `GET /api/connections` | `?application=&environment=&status=&cursor=` | a top-level JSON array of connections |
| `GET /api/connections/{id}` | none | the connection, its consent scope and its history |
| `POST /api/connections/reauthentication-prompts` | `{"connection_ids":[]}` | `{"queued": n}` |
| `GET /api/webhook-endpoints` | `?application=&environment=` | a top-level JSON array |
| `POST /api/webhook-endpoints` | `{"application","environment","target_url","event_types"}` | the created endpoint in `unverified` |
| `GET /api/team` | none | a top-level JSON array of members |
| `POST /api/team/{email}/role` | `{"role"}` | the updated member |
| `GET /api/data-requests` | `?state=` | a top-level JSON array |
| `POST /api/data-requests/{id}/complete` | none | the completed request |
| `GET /api/audit` | `?cursor=` | a top-level JSON array of entries, oldest first |
| `GET /api/usage` | none | `{"requests_used","committed_requests","period_start","period_end"}` |

Every list endpoint returns a top-level JSON array. A successful call returns the named
resource or shape. An invalid or unauthorized call is rejected as a client error, never a
`5xx` and never a silent success; pick conventional codes and be consistent. Bearer auth is
required on everything except `POST /api/auth/login` and `GET /api/health`.

### No mocks

PostgreSQL and Keycloak are the facts. A member table the app invented in memory, a
hardcoded `{"valid": true}` the app returns to its own login route instead of exchanging with
Keycloak, an audit array held in process memory that a restart clears, a role read from a
cookie the browser sent rather than from the member row: each is a contract violation however
good the screen looks. The named provider is the fact - the app's UI and its own tables can
only reflect what lives in the provider, never substitute for it.

---

## Definition of done

A compliance approver can sign in, claim a production access request somebody else filed, and
approve it, and only that one product becomes usable in production on that one application. A
developer who tries the same call is refused by the server and the request is unchanged. The
member who filed a request cannot approve it, whatever role they hold. Every one of those acts
is readable afterwards as a chained entry in the organisation's log, and no balance,
transaction or account number is reachable from any console route.
