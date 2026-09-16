# Veyra Fault Triage

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, sign in as the seeded engineer, open the fault queue, claim the most severe open fault, confirm it, and see it leave the queue while the owner of that site receives exactly one email about it, without hitting an error page. The hard part is that two engineers claiming the same fault at the same moment: exactly one claim stands, the other is refused and told who holds the fault, and the fault never ends up with two claimants or two claim entries in its history. The email must be a real message delivered through Mailpit to the site owner's address; a notice the app shows to itself does not count.

## Overview

Veyra Fault Triage is the work console of an infrastructure inspection operator. The operator flies LiDAR survey drones over wind turbines, solar farms, power lines and substations. Every survey flight finds fault zones: a crack, a surface deformation, corrosion, or vegetation growing into a clearance. A pilot logs the completed flight and its fault zones, the faults land in one triage queue ordered by severity, an engineer claims a fault and either confirms it or dismisses it, and a confirmed fault emails the owner of the site and leaves the queue.

The scope is the ten feature areas below. The product also carries a public landing page in the operator's visual language, a site register with the owner contact for every site, and an operations overview that counts faults by asset class and status.

It is deliberately not a flight planner, a point cloud viewer, a repair work-order system or a customer portal. Site owners never sign in; the confirmation email is where the product's responsibility ends.

The genuinely hard part is that a fault has exactly one owner of its decision at a time, even when two engineers press claim in the same instant.

## User roles

Three roles, all staff. Site owners are contacts on a site record, never accounts.

| Role | Read | Write |
|---|---|---|
| `administrator` | everything | creates and deactivates staff accounts; creates and edits sites; everything a pilot and an engineer can do |
| `pilot` | sites, surveys, the queue, the overview | logs a survey flight with its fault zones. **Cannot claim, release, confirm or dismiss a fault. Cannot create or edit a site.** |
| `engineer` | sites, surveys, the queue, the overview | claims an open fault; releases, confirms or dismisses a fault it holds. **Cannot decide a fault claimed by another engineer. Cannot create or edit a site or a staff account.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a `pilot` session to any `engineer`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. The same holds for an `engineer` session calling an `administrator`-only endpoint, and for an engineer deciding a fault another engineer holds.

There is no sign up. Accounts are created by the administrator, and the seeded accounts are `administrator@example.com`, `pilot@example.com`, `engineer@example.com` and `engineer2@example.com`.

## Core features

### 1. Staff sign in

1. Staff sign in with email and password at `/login`. A wrong password or an unknown email is refused with the message `That email and password do not match.` and issues no token.
2. A deactivated account is refused with the same message.
3. There is no sign up, no password reset and no remember-me control. The sign in card says `Accounts are created by your administrator.`

### 2. Site register

1. A site has a name, an asset class, a region, an owner name and an owner email. The four asset classes are `wind_turbines`, `solar_farms`, `power_lines` and `substations`, shown as `Wind Turbines`, `Solar Farms`, `Power Lines` and `Substations`.
2. Only the administrator creates or edits a site. A site name is unique.
3. A site can be marked inactive. An inactive site accepts no new survey, and its existing faults stay where they are.

### 3. Logging a survey flight

1. A pilot or the administrator logs a survey against an active site with a flown-at time in UTC, a coverage in square kilometres and optional notes, plus between 1 and 20 fault zones.
2. Every fault zone carries a kind (`crack`, `deformation`, `corrosion` or `vegetation_encroachment`), a location of 3 to 120 characters, a measured deformation in whole millimetres from 0 to 2000, and a severity from 1 to 4, where 4 is the most severe.
3. A flown-at time in the future is rejected as invalid. A coverage of 0 or less, or above 100, is rejected as invalid. A survey with no fault zone, or with more than 20, is rejected as invalid.
4. A survey and its fault zones are stored together or not at all: a rejected survey leaves no survey row and no fault row behind.
5. Every fault created by a survey starts `open`. After logging, the pilot sees the survey page with a message such as `Survey logged. 3 faults added to the queue.` carrying the real count.

### 4. The triage queue

1. The queue lists every `open` and `claimed` fault, ordered by severity from 4 down to 1, then by measured deformation from largest to smallest, then by the survey's flown-at time from oldest to newest. Every viewer sees the same order.
2. Each queue line shows the severity numeral, the kind and location, the site and its asset class, the deformation, how long ago it was flown, and the status: `Open` or `Claimed by` followed by the engineer's name.
3. The queue can be narrowed by asset class and to the faults the viewer holds. The narrowing is carried in the address, so a shared link opens the same view.
4. With nothing waiting, the queue says `The queue is clear.`

### 5. Claiming a fault, and the rule that matters

1. An engineer or the administrator claims an `open` fault. The fault becomes `claimed`, records who holds it, and writes one `claimed` entry to its history.
2. **Two claims on the same open fault arriving at the same moment must not both succeed: exactly one claim is accepted, every other claim is refused as a conflict and names the engineer who holds the fault, and the fault ends with one claimant and exactly one `claimed` history entry.**
3. Claiming a fault that is already `claimed`, `confirmed` or `dismissed` is refused as a conflict and changes nothing.
4. The claimant can release the fault. It returns to `open`, holds no claimant, keeps its place in the queue order, and writes a `released` entry.

### 6. Deciding a fault

1. Only the engineer holding a claimed fault can confirm or dismiss it. Anyone else attempting either is denied and the fault stays `claimed` by its holder.
2. Confirming asks the engineer to check the recipient first, in the form `Confirm and email Dana Whitlock at harrow.owner@example.com?`, and then sets the fault to `confirmed`.
3. Dismissing requires a written reason of 10 to 500 characters; a shorter or missing reason is rejected as invalid and the fault stays `claimed`. A dismissed fault stores the reason.
4. A decided fault, `confirmed` or `dismissed`, leaves the queue for every viewer and never returns to it. Every decision writes its entry to the fault's history with the actor and the time.

### 7. Owner notification by email

1. Confirming a fault sends exactly one email, after the decision is stored, addressed only to the site's owner email, with no cc and no bcc.
2. The subject begins with `Confirmed fault at` followed by a space, the site name, a colon and the severity and kind, for example `Confirmed fault at Harrow Ridge Wind Farm: severity 4 crack`.
3. The body names the site, the kind, the location, the deformation in millimetres, the severity out of 4, the survey's flown-at time in UTC, the confirming engineer and the fault reference.
4. Dismissing a fault sends no email. Releasing a fault sends no email. Logging a survey sends no email.
5. If delivery fails, the decision still stands, the history records `email_failed`, and the fault page says `The email to the site owner could not be sent.`

### 8. Operations overview

1. The console home shows, for each asset class and for all sites together, the number of faults `open`, `claimed`, `confirmed` and `dismissed`.
2. The counts are computed from the stored faults, so logging a survey of three faults on a wind turbine site raises that class's open count by three, and the all-sites figure equals the sum of the four classes.
3. Each count links to the matching filtered queue or decision list.

### 9. The public landing page

1. `/` is a public landing page in the operator's visual language: the product name as large outlined lettering over a pale wash, the lines `Autonomous LIDAR inspection systems.` and `Precision that secures critical infrastructure.`, the sentence `Detecting cracks, deformations and structural risks before they become failures.`, the payload figures `5 returns`, `±2 cm` and `450 m`, the four asset classes, and a capabilities selector.
2. The capabilities selector switches between `Scan`, `Connection` and `Compactness`, showing `360°`, `7 km` and `42 cm` with their paragraphs.
3. The page ends in one primary action, `Sign in to the console`, which opens `/login`.

### 10. Page view record

1. Each console page view is recorded with its route and the time it was served.
2. The administrator can read the count of page views per route.

## User flow

The information architecture is a public landing page, a sign in page, and a console that drills down from the overview to the queue to one fault.

| Route | Purpose | Auth |
|---|---|---|
| `/` | public landing page | none |
| `/login` | sign in | none |
| `/console` | operations overview | any role |
| `/console/queue` | the triage queue | any role |
| `/console/faults/:id` | one fault, its gauge, its history and its decision panel | any role |
| `/console/surveys/new` | log a survey | `pilot`, `administrator` |
| `/console/surveys/:id` | one survey and the faults it produced | any role |
| `/console/sites` | the site register | any role; editing `administrator` |
| `/console/staff` | staff accounts | `administrator` |

**Entry and redirects.** A signed-out visit to any `/console` route redirects to `/login`, and a successful sign in returns to the route first requested, or to `/console`. Signing out from the menu ends the session and returns to `/`. A token that expires mid-action returns the member to `/login` with the unsaved form discarded. A role opening a route it may not use sees the heading `Not permitted`, one line of explanation and a link back to `/console`. Navigation drills down: every console page carries a breadcrumb trail such as `Overview > Queue > F-12`, and each crumb is a link.

**Journey 1, triage to confirmation.** The engineer signs in at `/login` as `engineer@example.com`, lands on `/console`, opens the queue, and sees the seeded crack on `Blade B, 14 m from root` at `Harrow Ridge Wind Farm` at the top with severity 4. They open it, claim it, read the measurement and the gauge, choose confirm, check the recipient `harrow.owner@example.com`, and send. A toast confirms the email; the fault shows `confirmed`, it is gone from the queue, and the overview's confirmed count for wind turbines has risen by one.

**Journey 2, contention.** Two engineers have the same open fault on screen. Both press claim together. One sees the decision buttons; the other sees `Mira Okafor claimed this fault a moment ago.` with the holder's real name, and the panel shows the fault as claimed by the winner.

**Journey 3, logging a survey.** The pilot signs in as `pilot@example.com`, opens `/console/surveys/new`, picks `Saltmarsh Solar Array`, enters a flown-at time, a coverage and two fault zones, and saves. The survey page opens with `Survey logged. 2 faults added to the queue.`, and both faults appear in the queue in severity order.

**Journey 4, denial.** The pilot opens a fault and finds no claim control; a direct claim request from the pilot session is denied and the fault stays `open`. The second engineer opens a fault the first engineer holds and finds no decision controls; a direct confirm request from that session is denied and the fault stays `claimed`.

**States.** Every list has an empty state that says why it is empty. Every page shows a loading state while it waits. A failed request shows a message in place and never crashes the app. A form error sits under the field it belongs to, names the field, and moves focus to the first invalid field.

## UI/UX notes

**North star.** An engineer should understand at a glance which fault is worst and who holds it. **Register.** This is an operational console: quiet, calm, built for scanning and repeated decisions; only the public landing page carries atmosphere.

**Colour, by role.** The page ground is a near-white neutral and cards sit on a lighter near-white neutral. All primary text, hairline rules and the primary button fill are one deep cool neutral ink, and secondary text is a mid cool neutral at reduced strength. Links and the focus ring are a mid, muted cyan. Status dots carry meaning: a light, muted teal for confirmed, a mid, soft cyan for claimed, a near-white neutral for dismissed, and the ink for open. The pale wash behind the landing hero and the sign in card runs from a near-white cool neutral at the top to the page ground. There is no red, orange or green warning colour anywhere: severity is carried by a numeral and by weight, never by hue alone. The exact shades are yours within those roles. The console is designed in light mode only, fully committed; there is no dark theme to build.

**Type.** One family, `Switzer`, a variable grotesque, carries everything, with `Proto Mono` at a light weight for bracketed labels such as `[ OPEN ]` and for numerals that line up in tables. Sizes: page titles 48px light, overview numerals 64px light, the fault headline 28px light, card titles 24px light, body and table cells 16px regular, buttons 14px medium, bracketed labels 12px. The landing page wordmarks run at 120px light and the hero wordmark at 240px light.

**Shape and density.** Comfortable rather than cramped: every section is separated by a single thin rule, inputs and buttons have small soft corners, filter chips are fully rounded pills, and status dots are circles. Space over dividers inside a card.

**Iconography.** Icons are drawn in the page from lines and circles, in the ink, never loaded as image files: a turbine, a solar panel, a pylon, a substation, a tick for confirm, a cross for dismiss, a hand for claim, and a nine-dot grid for the menu. The fault page carries a half-dome gauge, a half circle with radial ticks and a small pointer notch, whose notch points to one of four positions for severity 1 to 4.

**Global chrome.** Every console page has the same slim top bar: the product mark and name with the current page title on the left, the signed-in member's name and role in the middle, a UTC clock whose colon blinks, and a `menu` button on a pale panel fill at the right. The menu opens a full-height panel from the right edge, revealed by a horizontal wipe, listing `Overview`, `Queue`, `Log a survey`, `Sites`, `Staff` for the administrator, and `Sign out`; Escape closes it and returns focus to the button.

**Motion.** Motion is calm and eased: things glide in and slow gently at the end, colour transitions are brief, and nothing overshoots or bounces. Page titles resolve word by word out of a soft blur. Queue lines rise into place one after another on first load. A decided fault's line collapses out of the queue. A status dot that changed since the last refresh pulses once so the change is noticed. Under `prefers-reduced-motion` the blurs, wipes, rises and pulses are removed and only colour transitions remain.

**Components.** Every button, field, chip, queue line and panel has a defined look when resting, pointed at, pressed, focused, unavailable, loading, empty and in error. Unavailable is never signalled by colour alone. Each page leads with one clear primary action in the ink fill, visually distinct from every secondary action, which sits on the pale panel fill.

**Accessibility.** Every journey works with keyboard navigation alone, in visual order, with a visible focus ring on the focused element. Body text and its background meet WCAG AA contrast. The queue is a real table with a caption and column headers. Severity is announced as `severity 4 of 4`. A status change found on refresh is announced once. Icon-only controls carry labels, and every drawn icon that carries meaning has alternative text.

**Responsive.** The layout is responsive across phone, tablet and desktop widths. At a narrow viewport the top bar keeps the mark, the name and `menu`; the queue becomes a stack of cards showing severity, fault, site and status; the overview becomes one card per asset class; form rows stack into one column; and nothing overflows sideways. At a middle breakpoint the queue keeps severity, fault, site, status and action and folds deformation and flown-at under the fault text. On a wide screen the fault page places the measurement and gauge beside the decision panel.

## Technical requirements

The app is a single-page application over a JSON API. The frontend is Svelte built with Vite; the backend is Fastify on Node, in TypeScript. The browser receives a small HTML shell on first paint and the Svelte app renders the console from JSON fetched under `/api`. Data is stored in the PostgreSQL database at `DATABASE_URL`. Email is sent over SMTP through Mailpit at `SMTP_HOST` and `SMTP_PORT`, reading `SMTP_USER` and `SMTP_PASS` from the environment.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing services available in this environment are PostgreSQL and Mailpit, and reaching for anything else is a contract violation.

Authentication is app-implemented email and password with bearer tokens. `POST /api/auth/login` takes `email` and `password` and returns `access_token`; every other endpoint except `GET /api/health` requires `Authorization: Bearer <token>`. Passwords are stored hashed.

The site serves a favicon and declares it in the document head with a `rel="icon"` link that resolves.

Every response carries the standard security headers, including a strict transport policy (`Strict-Transport-Security`) and `X-Content-Type-Options: nosniff`.

No credential appears in anything the browser downloads: the seeded password, the database connection string and the SMTP credentials never reach the HTML shell or any script or stylesheet the app serves.

Performance: the queue answers promptly and stays usable with one thousand open faults.

`GET /api/health` returns `200` once the app is ready.

## Data model

Six tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**`staff`.** `email` (unique, stored lowercase), `name`, `role` in (`administrator`, `pilot`, `engineer`), `active` (boolean, default true), `password_hash`, `created_at`.

**`sites`.** `name` (unique), `asset_class` in (`wind_turbines`, `solar_farms`, `power_lines`, `substations`), `region`, `owner_name`, `owner_email`, `active` (boolean, default true).

**`surveys`.** `site_id`, `pilot_id`, `flown_at`, `coverage_km2` (greater than 0, at most 100), `notes` (at most 500 characters), `created_at`.

**`faults`.** `survey_id`, `kind` in (`crack`, `deformation`, `corrosion`, `vegetation_encroachment`), `location`, `deformation_mm` (integer, 0 to 2000), `severity` (integer, 1 to 4), `status` in (`open`, `claimed`, `confirmed`, `dismissed`), `claimed_by` (nullable), `decided_by` (nullable), `dismiss_reason` (nullable), `created_at`. The fault reference shown to people is `F-` followed by the fault's number, such as `F-12`.

**`fault_events`.** `fault_id`, `actor_id` (nullable), `kind` in (`claimed`, `released`, `confirmed`, `dismissed`, `email_sent`, `email_failed`), `created_at`. Append only: an entry is never edited or removed.

**`page_views`.** `route`, `viewed_at`.

Invariants that must hold of the running system:

- A fault has at most one claimant at any time. Two simultaneous claims on the same open fault must not both succeed; exactly one wins, the others are refused, and exactly one `claimed` row exists in `fault_events` for that claim.
- A fault's `status` is the single source of whether it is in the queue; the queue is that status read back, never a separate copy that could disagree.
- `claimed_by` is set exactly when `status` is `claimed`. `decided_by` is set exactly when `status` is `confirmed` or `dismissed`. `dismiss_reason` is set exactly when `status` is `dismissed`.
- A survey and its faults are written together or not at all.
- The overview counts are computed from `faults` on read, never stored.

**Seed data.** Four staff: `administrator@example.com` (administrator, Priya Raman), `pilot@example.com` (pilot, Tomas Reyes), `engineer@example.com` (engineer, Mira Okafor) and `engineer2@example.com` (engineer, Jonah Ellery). Four sites, one per class: `Harrow Ridge Wind Farm` (`wind_turbines`, owner Dana Whitlock, `harrow.owner@example.com`), `Saltmarsh Solar Array` (`solar_farms`, owner Ines Calder, `saltmarsh.owner@example.com`), `Brackenfold Line` (`power_lines`, owner Omar Haddad, `brackenfold.owner@example.com`) and `Tollgate Substation` (`substations`, owner Ruth Adeyemi, `tollgate.owner@example.com`). One survey on `Harrow Ridge Wind Farm` flown by the pilot, carrying three `open` faults: a `crack` at `Blade B, 14 m from root` with deformation 38 and severity 4; a `deformation` at `Tower T2 flange` with deformation 22 and severity 3; and `vegetation_encroachment` at `Access track, north gate` with deformation 0 and severity 2. Write the accounts and the password to `/app/USER_README.md`.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Constraints

- One operator, one organisation. There is no tenancy and no customer portal.
- Site owners never sign in and have no account.
- There is no sign up, no password reset and no single sign-on.
- There is no point cloud viewer, no 3D model, no video and no flight control or telemetry anywhere in the product.
- There is no integration with any drone vendor or processing software, and no outbound call to any third party at runtime.
- There is no live push: another engineer's claim appears when the queue next refreshes or the page next loads, never as a live stream.
- No background job, scheduler, cron or queue worker. Anything that looks timed is computed when it is next read.
- No repair work orders, no attachments and no comments on a fault.
- The app stays responsive with one thousand open faults and fifty sites.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them. PostgreSQL is reachable at `DATABASE_URL` and Mailpit at `SMTP_HOST` and `SMTP_PORT`.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** List endpoints return a top-level JSON array. A successful call returns the named resource; an invalid, unauthorized or conflicting call is rejected as a client error, never a server error and never a silent success.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `email`, `password` | `access_token`, `staff` with `id`, `name`, `role` |
| `GET /api/health` | none | `200` |
| `GET /api/sites` | none | array of sites with `id`, `name`, `asset_class`, `region`, `owner_name`, `owner_email`, `active` |
| `POST /api/sites` | `name`, `asset_class`, `region`, `owner_name`, `owner_email` | the created site; `administrator` only |
| `PATCH /api/sites/:id` | any of `name`, `region`, `owner_name`, `owner_email`, `active` | the updated site; `administrator` only |
| `POST /api/surveys` | `site_id`, `flown_at`, `coverage_km2`, `notes`, `faults` as an array of `kind`, `location`, `deformation_mm`, `severity` | the created survey with `id` and `faults`, each fault carrying `id` and `status` |
| `GET /api/surveys/:id` | none | the survey with its `faults` |
| `GET /api/faults` | optional `asset_class`, optional `mine=true` | array of `open` and `claimed` faults in queue order, each with `id`, `kind`, `location`, `deformation_mm`, `severity`, `status`, `claimed_by`, `site_id` |
| `GET /api/faults/:id` | none | the fault with its `events` |
| `POST /api/faults/:id/claim` | none | the claimed fault; a conflict carries `claimed_by` |
| `POST /api/faults/:id/release` | none | the released fault; claimant only |
| `POST /api/faults/:id/confirm` | none | the confirmed fault; claimant only |
| `POST /api/faults/:id/dismiss` | `reason` | the dismissed fault; claimant only |
| `GET /api/overview` | none | an object keyed by `wind_turbines`, `solar_farms`, `power_lines`, `substations` and `all`, each carrying `open`, `claimed`, `confirmed`, `dismissed` |
| `POST /api/page-views` | `route` | the recorded view |
| `GET /api/page-views` | none | array of `route` and `count`; `administrator` only |
| `POST /api/staff` | `email`, `name`, `role`, `password` | the created staff member with `id`; `administrator` only |
| `PATCH /api/staff/:id` | `active` | the updated staff member; `administrator` only |

**No mocks.** An email the app records in its own table and never sends, a success toast with no message behind it, a message sent to a fixed test address instead of the site owner, or a claim tracked only in browser memory are all contract violations however good the interface looks. The named provider is the fact - the app's UI and its own tables can only reflect what lives in the provider, never substitute for it. A confirmed fault's email must exist as a real message in Mailpit addressed to that site's owner, and a fault's claim must exist as its stored row in PostgreSQL.

## Definition of done

For acceptance, an engineer can sign in, claim the most severe open fault, confirm it, and the site owner receives one email while the fault leaves the queue for everyone. Two engineers claiming the same fault at once produce one claimant, one refusal naming the holder, and one claim entry in the fault's history. A pilot cannot decide a fault and an engineer cannot decide a fault another engineer holds. A dismissed fault sends no email.
