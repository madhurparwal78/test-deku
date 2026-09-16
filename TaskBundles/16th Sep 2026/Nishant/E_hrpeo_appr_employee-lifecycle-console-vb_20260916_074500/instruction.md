# Cadrix Employee Lifecycle Console

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, sign in as a
manager, open the approval queue, approve a leave request from one of their own direct
reports, and see the booked day arrive in the open payroll run as an input nobody typed,
without hitting an error page. A different stranger, signed in as a peer manager, must NOT
be able to decide that same request by any means, and the payroll account that moved a run
into review must NOT be able to sign that run off. The seeded people, policies and runs
must live in PostgreSQL and the seeded identities in Keycloak; a row the app keeps to
itself in memory does not count.

## Overview

Cadrix holds one record per employee from hire to exit. Leave, attendance, claims and
statutory payroll all read from that one record, which is the whole point: change somebody's
department once and the payroll run, the leave calendar and the approval chain all know.

Three kinds of person use it. An employee reads their own record, applies for leave, submits
a claim and reads their own payslips. A manager decides the requests their own direct reports
raise, and reads the attendance month grid for their line. A payroll account opens, locks,
computes and reviews a monthly run, reads the register, and signs off a run somebody else
prepared.

The genuinely hard part is that authority here is a relationship, not a role. Holding
`manager` does not let you decide a request; managing that requester does. Holding `payroll`
does not let you sign off a run; having not prepared it does. Both boundaries are enforced
on the server and both leave the underlying row untouched when they refuse.

Deliberately not built: no onboarding or exit workflow, no final settlement, no typed
assistant, no report builder, no letters or generated documents, no outbound email or
notification of any kind, and no marketing website. The approval queue is the notification.

## User roles

Three roles. Every seeded account uses the password `deku-demo-pw-2026`.

| Role | Can read | Can write |
|---|---|---|
| `employee` | their own record, their own leave balances and ledger, their own attendance days, their own claims, their own payslips | apply for leave, request a regularisation, submit a claim, withdraw their own pending request. **Cannot read another employee's record, another employee's balance, any salary figure, or any payroll run**, and **cannot decide any request, including their own** |
| `manager` | everything an `employee` can, plus the record, leave balance and attendance days of their own direct reports, and the approval queue filtered to their own direct reports | approve or reject a request raised by one of their own direct reports. **Cannot decide a request raised by anybody who does not report directly to them**, **cannot decide their own request**, **cannot read any salary figure**, and **cannot open, lock, compute, review or sign off a payroll run** |
| `payroll` | every employee in a payroll group they own, including salary structures, payslips and the register | open, lock, compute and review a payroll run; sign off a run reviewed by a different account. **Cannot decide a leave request, a regularisation or a claim**, and **cannot sign off a run they themselves moved into review** |

That table is the capability matrix and it is the whole of the permission model: each
role is one persona with one job, and a capability the matrix does not grant is a deny.
There is no sixth role, no support persona and no impersonation of any kind.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the
UI is not authorization: a direct API call from an `employee` session to a `manager`-only or
`payroll`-only endpoint must be rejected by the server (an unauthorized request is denied,
not served), leaving the protected state unchanged.

Signup is closed. Accounts exist only as seeded identities in Keycloak; the app creates no
account of its own and offers no registration route.

The seeded accounts, each holding one realm role:

| Email | Employee number | Name | Role | Reports to |
|---|---|---|---|---|
| `employee@example.com` | `E-1001` | `Nadia Fernandes` | `employee` | `E-2001` |
| `employee2@example.com` | `E-1002` | `Arjun Mehta` | `employee` | `E-2001` |
| `employee3@example.com` | `E-1003` | `Sofia Ruiz` | `employee` | `E-2002` |
| `manager@example.com` | `E-2001` | `Priya Raman` | `manager` | `E-3001` |
| `manager2@example.com` | `E-2002` | `Tomas Lindqvist` | `manager` | `E-3001` |
| `payroll@example.com` | `E-4001` | `Daniel Okafor` | `payroll` | `E-3001` |
| `payroll2@example.com` | `E-4002` | `Helen Zhao` | `payroll` | `E-3001` |

`E-1004` `Marcus Bell` is a fourth employee in the payroll group with no sign-in of their
own, seeded so the run covers four people rather than three.

## Core features

**The employee record.** One record per employee, addressed by an `employee_number` that is
unique and never reused.

1. The record opens as tabs, each reading from the same row: Profile, holding personal
   contact details and an emergency contact; Employment, holding designation, department,
   location, manager, employment type and the joining and confirmation dates; Compensation,
   holding the salary structure and its history; Statutory, holding national identifiers,
   provident fund and insurance numbers; Bank, write-only and never displayed in full after
   saving; Leave; Attendance; and Claims. Every other surface reads from that one record
   rather than holding a copy of it.
2. Fields fall in three classes. Self-editable fields (contact, address, emergency contact)
   the employee changes directly. Requested fields (name, bank, statutory identifiers) the
   employee proposes and `payroll` confirms, and both versions are kept. Restricted fields
   (designation, salary, manager, employment type) are never edited in place.
3. A restricted field changes only as a dated change record carrying an effective date, an
   approver and a reason, so the employee's state on any past date is reconstructable from
   the change history. Editing a restricted field directly is refused and names the field.
4. Bank details are the sharpest case: an employee changing their own bank account without a
   second confirmation is refused, and the proposal is held until `payroll` confirms it.

**The leave policy engine.** A policy is data, never code. Each policy carries its accrual
kind and rate, its cap, its carry forward and when the carried days expire, whether it is
encashable, who it applies to, its minimum notice, its maximum consecutive days, the days
after which a document is required, whether half days are permitted, how far the balance may
go below zero, its holiday calendar and its number of approval levels.

1. Three policies are seeded: `ANNUAL`, `SICK` and `UNPAID`. `ANNUAL` accrues monthly,
   `SICK` yearly, `UNPAID` not at all.
2. Holidays belong to a calendar and a calendar belongs to a location, because a company
   operating in two states does not share a holiday list. Weekends belong to the calendar
   too.
3. A day is stored as an integer count of half days. A response reports `halves` as that
   integer and `days` as that integer divided by two, so a half day is exact and a balance
   is never a floating-point value.

**Applying for leave.** Applying happens in a new row at the top of the employee's own
request list, never on a separate page.

1. Picking the dates computes the half days deducted before submission, excluding the
   holidays and weekends of the employee's own calendar. `2026-08-17` to `2026-08-21` under
   the `KA-2026` calendar is `8` halves, because `2026-08-19` is a holiday on that calendar.
2. The balance, the notice rule and the consecutive-day rule are checked and shown before
   submission, not after. A request breaching `min_notice_days` is refused as invalid at
   submission and writes no row.
3. Who else on the requester's team is already away on those dates is shown with the form,
   by name, before submission.
4. Submitting books the half days provisionally: a `pending` ledger entry is written and the
   request enters `pending`. Approval converts it to `availed`; rejection removes the pending
   entry and returns the balance to what it was.
5. A request whose dates overlap a date already `approved` or `availed` for the same
   employee is refused as invalid and writes no row.
6. Request states are `draft`, `pending`, `approved`, `rejected`, `cancelled`, `withdrawn`,
   `availed` and `expired`. `availed` is set by the date passing, and that is what moves the
   day into payroll's input.
7. Cancelling after the dates have passed is refused for an employee and permitted for
   `payroll`, and it writes a `correction` ledger entry carrying a reason rather than
   adjusting anything silently.

**The balance is the ledger.** A leave balance is never a stored number anybody edits.

1. The balance in half days is `opening` plus `accrual` plus `correction`, minus `availed`,
   minus `pending`, minus `encashment`, minus `lapse`, over that employee and that policy.
2. Every balance shown can be expanded into exactly the ledger entries that produce it, and
   the expansion sums to the figure shown.
3. `E-1001` on `ANNUAL` is seeded with `20` opening halves, seven monthly accruals of `4`
   halves each, `8` halves availed and `4` halves pending, so the balance reads `36` halves,
   which is `18.0` days.

**Attendance.** Punches arrive from a device and are evidence, not editable data.

1. A punch carries the employee, the instant, its direction (`in` or `out`), its source
   (`device`, `web`, `mobile`, `geo`, `face` or `manual`), its device, its location, a
   confidence for the recognition sources, and `raw_ref`, the source's own identifier. A
   biometric reader, a location-verified punch from a phone, a geofenced marker and a
   face-recognition terminal all arrive on this one stream and are told apart only by
   `source`.
2. Punches are append-only. No punch is ever updated and no punch is ever deleted.
3. Posting a punch whose `raw_ref` already exists writes no second row and leaves the
   computed day exactly as it was. The response reports the punch already held rather than
   inventing a new one.
4. A day is computed from the punches, the shift and the leave, and carries `worked_minutes`
   capped at the shift maximum, a `status` of `present`, `half_day`, `absent`, `weekly_off`,
   `holiday`, `on_leave` or `unpaired`, minutes late, minutes early and overtime where the
   policy permits it.
5. An `in` punch with no matching `out` punch produces the status `unpaired` and is surfaced
   as a defect on the month grid. It is never silently dropped and never paired with a
   neighbouring day's punch.
6. A correction is a regularisation: the employee requests it with a reason and their manager
   decides it. The original punches remain, the regularisation sits on top, and the computed
   day reports both the punched times and the regularised times.
7. The month grid shows employees down and days across, one cell per day carrying its state
   as a letter and a colour, with the counts on the right.

**Claims.** A claim carries a category from `TRAVEL`, `MEALS` and `EQUIPMENT`, an amount in
minor units, a currency, the date it was spent on, and a receipt reference above the
threshold.

1. A receipt reference is required above `200000` minor units and a claim above that
   threshold without one is refused as invalid.
2. A manager approves a claim up to `1000000` minor units. Above that the claim escalates to
   `payroll`, and the claimant is told which of the two will decide it at the moment they
   submit, not afterwards.
3. Claim states are `draft`, `submitted`, `approved`, `rejected`, `paid` and
   `reimbursed_via_payroll`.
4. An approved claim is paid either through the payroll run as a non-taxable reimbursement
   line or through a separate payment batch, decided by the organisation's
   `claim_payment_route` setting, which is seeded as `payroll`. A claim is never in both: a
   claim already carrying `reimbursed_via_payroll` cannot be added to a batch, and the
   attempt is refused.

**One approval queue.** Leave requests, regularisations and claims all arrive in one queue,
with a filter by kind. A manager never visits three screens to clear their morning.

1. Each row carries the requester, the kind, a one-line summary, its age in days and the two
   actions. Opening a row shows the context that decides it: for leave, the balance and who
   else is away; for a claim, the receipt reference and the category limit; for a
   regularisation, the original punches.
2. **A decision is scoped by the reporting line. A `manager` may decide only a request whose
   requester's `manager_employee_number` is that manager's own `employee_number`. A request
   from a peer manager's direct report is denied at the server, and the request row keeps its
   state, its decider and its reason exactly as they were.**
3. **Nobody decides their own request. A `manager` deciding a request they themselves raised
   is denied at the server even though the requester reports to them in every other sense,
   and the row is unchanged.**
4. **A request is decided once. A second decision on a request that already carries a
   decision is refused, naming the account that decided it and when. Two decisions submitted
   at the same moment produce exactly one decision: one is accepted, the other is refused as
   already decided, and the leave ledger moves exactly once.**
5. An approval chain is per policy and names a role relative to the requester rather than a
   person, so the chain survives a reorganisation. `ANNUAL` and `SICK` are one level.
6. Escalation is by timeout and never by approval: a request unanswered for `3` days
   escalates to the next level and both parties are told in the queue. The timeout moves
   the request up the chain and never decides it.
7. Bulk approval and bulk rejection act across the filtered selection with a `10` second
   window in which the action can be undone. A bulk rejection requires a reason and a bulk
   approval does not, which is deliberate.

**The payroll run.** A run is an object with a lifecycle, not a button. There is exactly one
run per period per payroll group, and a second attempt to open one for a period a run already
covers is refused.

1. Run states are `open`, `locked`, `computed`, `in_review`, `signed_off`, `paid`, `closed`
   and `reopened`, and they advance only in that order. `closed` means filed and archived,
   and `reopened` is what a signed-off run becomes when it is pulled back.
2. Locking is the moment the run stops tracking its sources. It freezes attendance days and
   absences, leave without pay, overtime, claims marked for payroll, salary revisions
   effective in the period, joiners and leavers, and any ad-hoc earning or deduction. Anything
   arriving afterwards belongs to the next period, and the run says so plainly at the moment
   of locking.
3. Computing runs per employee in component order and produces one payslip each. The run
   reports progress per employee and completes for the whole group or not at all: a partial
   computation is never a state.
4. A per-employee failure is a blocking finding rather than a wrong number: a missing bank
   account, a missing statutory identifier, a negative net pay, or a component formula that
   cannot be resolved. Moving to review with a blocking finding outstanding is refused.
5. Statutory deductions come from a rule set that is data, versioned by an effective date,
   carrying a jurisdiction, a state, a basis, a rate, its thresholds, its caps and its
   rounding. The seeded rule set is `IN-2026-04`, effective from `2026-04-01`, version `1`,
   and it carries the heads `PF`, `ESI`, `PT`, `LWF` and `TDS` across the states `KA` and
   `MH`. No rate is written into the application: a rate change is a data change.
6. Every computed statutory line records the rule version that produced it, so a
   recomputation years later reproduces the original figure.
7. The register is one row per employee, one column per component, with totals per column,
   subtotals per department and a grand total. Filtering the register to one department shows
   that department's totals, labelled as filtered rather than presented as the whole.

**Sign-off, the control that matters most.**

1. **The account that moved a run to `in_review` may not be the account that moves it to
   `signed_off`. The second attempt by the same account is denied at the server, the run
   keeps the state `in_review`, and `signed_off_by` stays empty.**
2. Sign-off presents the total gross, the total deductions, the total net and the headcount
   paid, and requires the exact total net in minor units to be typed back. A mismatch is
   refused as invalid and the run keeps its state.
3. A signed-off run's payslip figures never change. Reopening a signed-off run is refused
   once payment has been initiated; before that it requires a reason and writes an audit
   entry.
4. Payslips are published to the employee surface on close, and an employee reads only their
   own.

**The employee surface.** At `/me`, an employee reads their balances per policy, their own
requests and their own payslips without asking anybody. A payslip request for a period
belonging to somebody else is denied.

**The launch surface.**

1. An address that matches no route renders the product's own not-found page, carrying a way
   back into the console, and answers as not found rather than as success.
2. The app serves a favicon and declares it in the document head of every page.
3. Every internal link on every route resolves. No link on any route reachable by a signed-in
   `manager` leads anywhere that answers as not found.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/login` | sign in | none |
| `/me` | own balances, own requests, own payslips | any role |
| `/me/leave` | apply for leave in a new row | any role |
| `/me/claims` | submit a claim in a new row | any role |
| `/people` | the employee directory | `manager`, `payroll` |
| `/people/E-1001` | one employee record, tabbed | `manager`, `payroll` |
| `/approvals` | the one queue, filtered by kind | `manager` |
| `/approvals/1` | one request with its deciding context | `manager` |
| `/attendance` | the month grid for the caller's own line | `manager` |
| `/payroll` | the runs list | `payroll` |
| `/payroll/2026-07` | one run and its lifecycle | `payroll` |
| `/payroll/2026-07/register` | the register | `payroll` |

**Entry and redirects.** A signed-out request for any route other than `/login` goes to
`/login` and returns to the route that was asked for once the sign-in succeeds. With no
stored destination, sign-in lands on `/me`. Signing out returns to `/login`. A token
expiring mid-action keeps the typed values on the page and offers a fresh sign-in rather
than discarding the work. A role reaching a route it does not hold is refused with the
reason and nothing changes.

**Journeys.**

1. Sign in as `manager@example.com`, open `/approvals`, open the pending `ANNUAL` request
   from `Nadia Fernandes`, read her balance and the one teammate already away that week,
   approve it, and watch the row leave the queue before the response lands.
2. Sign in as `employee@example.com`, open `/me/leave`, open a new row at the top of the
   list, pick `2026-08-17` to `2026-08-21`, read `8` halves and the remaining balance before
   submitting, submit, and see the balance move into pending.
3. Sign in as `manager2@example.com`, open the same request by its address, and attempt both
   actions: refused, and the request is still `pending` with no decider.
4. Sign in as `payroll@example.com`, lock `/payroll/2026-07`, compute it, move it to review,
   then attempt to sign it off: refused as the same actor, and the run is still `in_review`.
5. Sign in as `payroll2@example.com`, open `/payroll/2026-07/register`, read the grand total
   net `13075000`, type it back, and sign the run off.
6. Open `/payroll/2026-99` and land on the product's own not-found page with a way back.

**States.** Every list carries an empty state naming the next action, and every route carries
a loading state while it resolves. A refusal raises an inline banner above the surface that
raised it, naming what was refused and why; no route becomes an error page. Every request
row, attendance cell and run state carries its state as a word beside its colour.

## UI/UX notes

The north star is comprehension. This is a console and a payroll tool, so the honest thing
somebody should understand in the first moment is that they can read it, and saying so
plainly is the whole of the ambition. The register is operational: quiet, dense but
organised, built for scanning and for repeated action, with no oversized hero and no
editorial composition. Space over decoration, and stillness over expressiveness.

Colour is carried by role, not by value, and the exact shade is yours so long as it holds
the relationships below. The ground is a near-white neutral. Headings take a near-black
neutral and body copy takes a deep neutral, which is the wrong way round from most products
and is the measured character of this one: only headings take the near-black. Captions take a
mid neutral. The brand is a mid, vivid violet and it appears on the wordmark, on emphasis
words and on in-content links and nowhere else. The one primary action per screen sits on a
deep, soft indigo ground and takes a light, vivid violet on hover, and no secondary control
wears either. Each screen leads with exactly one primary action, visually distinct from every
secondary one, and a screen carrying two things that look primary has failed this rule.

Status carries meaning and each meaning owns one colour that nothing else uses: a mid, vivid
green for approved, present and paid; a mid, vivid orange for pending and awaiting approval;
a mid, vivid red for rejected, absent and failed; a mid, vivid blue for informational; and a
mid cool neutral for draft and not applicable. **Meaning is never carried by colour alone.**
Every state pill carries its state as a word as well, which matters more here than in most
products: somebody signing off a payroll run may not see colour.

The product commits to light and is designed fully for it. A dark mode is optional and is
never the default; a build that ships only light has met this brief.

Type is one variable sans family for the interface and one tabular-figure family for every
number in a payroll or attendance context. Every amount, balance, count and duration renders
with tabular figures, and this is the one typographic rule that is not negotiable: a register
whose columns do not align is unreadable.

Density is compact on the directory, the register, the approval queue and the attendance
grid, so a full queue fits one screen, with a control to switch to comfortable. The
employee's own surface is comfortable by default. Shape is soft rather than sharp: fully
rounded pills and buttons, gently rounded cards, less on panels and inputs, least on chips.
Elevation belongs only to floating surfaces.

Motion is confined to four moments and nothing else animates. A panel or sheet opens on a
long decelerate. A row changes state on the house ease. A skeleton holds while a list loads.
A progress indicator runs during a payroll computation. Somebody working a register for two
hours wants the rows to stay still. With a reduced-motion preference set, panels appear
without travel, skeletons hold their first frame, and the payroll progress indicator keeps
running, because it is the only signal that a long operation is proceeding.

Components are specified by their states rather than their measurements: resting,
pointed-at, pressed, focused and unavailable. Escape closes a layer and returns focus to
whatever opened it, with the sign-off dialog the deliberate exception. A destructive action
confirms first. Unavailable is never signalled by colour alone.

Accessibility is contract. One `h1` per screen. Contrast meets WCAG AA. Every command has a
keyboard navigation route with a visible focus ring. Tables are real tables with header
associations rather than grids of divisions. Icon-only controls carry labels. The month grid
declares its dimensions and announces the state of its focused cell as text. Dialogs trap
focus and return it. Every amount is announced with its currency and every date is announced
in full rather than in the abbreviated form the table shows.

Responsive behaviour holds at every width between the named tiers, and the layout floors on
the smallest viewport. The employee surface and the approval queue are designed for the
narrowest width first, because that is where they are used. What the product must not look
like: a page dominated by one hue family with no second signal, decoration standing in for
content, or a marketing composition where a working interface belongs.

## Technical requirements

Every route's HTML is produced on the server and arrives complete on first paint;
interactive behaviour is added on top of HTML that already rendered. The approval queue, the
attendance month grid and the register are the islands that take that behaviour, and each
still lists its rows with scripting disabled.

Stack: TypeScript on Node 20. Nuxt 3 renders the routes on the server and ships islands over
the delivered HTML. The JSON API is a Hono application mounted on the same origin under
`/api`, served by the same process that renders the pages, so there is one listener and one
production build. Storage is PostgreSQL. Identity is Keycloak. `GET /api/health` returns
`200`, with no credential, once the app has connected to PostgreSQL, has read Keycloak's
discovery document and has finished seeding.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
services available in this environment are PostgreSQL and Keycloak, and reaching for
anything else is a contract violation.

Read every connection detail from the environment and never hardcode a host or a port.
PostgreSQL is at `DATABASE_URL`. Keycloak is at `AUTH_ISSUER_URL`, with the app's own client
credentials at `AUTH_CLIENT_ID` and `AUTH_CLIENT_SECRET`. The app's own address is
`APP_PUBLIC_URL` and its outside port is `APP_PUBLIC_PORT`. Both backing services are already
running and must not be downloaded, installed, compiled or started.

Identity is Keycloak's and authorization is the app's. The app exchanges an email and the
seeded password for a token at Keycloak, validates that token's signature and its realm role
on every request, and then resolves the caller's own employee record from the token subject.
The realm carries the three roles `employee`, `manager` and `payroll` and it is already
imported; the app creates no realm, no role and no user, and holds no administrative
credential for Keycloak. A role read from a request body rather than from the validated token
is never authority.

A role is a floor and never a scope. Every read and every write is additionally narrowed by
the relationship the record carries: a manager's reach is the set of employees whose
`manager_employee_number` is that manager's own number, and a payroll account's reach is the
payroll groups it owns. A request that passes the role check and fails the relationship check
is refused exactly as one that failed both.

Leave balances, attendance days, payroll components and statutory lines are computed on the
server, once, and are never recomputed in the browser for display. A figure a client can
derive is a figure two clients can derive differently.

Nothing the browser downloads carries a credential, an API key, a client secret or an
administrative token. `AUTH_CLIENT_SECRET` and `DATABASE_URL` stay on the server, and no
response body, no served script and no rendered HTML contains either.

Every collection endpoint pages by opaque cursor, never an offset: `50` rows a page by
default and `500` at most, with the cursor returned in the `X-Next-Cursor` response header
and absent on the last page. A paging session over the directory and over the register never
repeats a row and never skips one.

Application logs go to standard output, one line per request carrying the method, the path,
the outcome and the elapsed milliseconds, and never a password, a token, an email address, a
salary figure or a national identifier. That log is the whole of the observability surface:
there is no trace pipeline and no metrics exporter.

Every page declares a favicon in its document head and the app serves it.

## Data model

Twenty-three tables. The entities are listed first, then the conventions that govern every
one of them, then the invariants the product may never violate. All timestamps are UTC, and
a calendar day is decided by server-side UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
not a secret. Hash it as normal; the exact literal must work at login, and it must be written
into `/app/USER_README.md` alongside each account so a grader can sign in.

Money is an integer in the currency's minor unit with the currency code beside it, never a
floating-point number. The currency is `inr` throughout. Leave days are an integer count of
half days for the same reason.

`employee`: `id`, `employee_number`, `full_name`, `email`, `state`, `joining_date`,
`confirmation_date`, `last_working_day`, `manager_employee_number`, `department_code`,
`location_code`, `grade_code`, `cost_centre_code`, `payroll_group_code`, `created_at`,
`updated_at`. `employee_number` is unique and never reused. `state` is `pre_joining`,
`active`, `on_notice`, `exited` or `alumni`. `manager_employee_number` refers to another
employee, and a reporting line that would close a cycle is refused and the cycle is named.

`employment_change`: `id`, `employee_number`, `field`, `from_value`, `to_value`,
`effective_from`, `reason`, `approved_by`, `approved_at`. A restricted field changes only
here. The employee's value for any field on any past date is the latest change whose
`effective_from` is on or before that date.

`salary_structure`: `id`, `employee_number`, `effective_from`, `gross_minor`, `currency`.
`salary_component`: `id`, `structure_id`, `code`, `kind`, `formula_kind`, `formula_value`,
`of_code`, `taxability`, `prorated`, `compute_order`. `kind` is `earning`, `deduction`,
`employer_contribution` or `reimbursement`; `formula_kind` is `fixed`, `percent_of` or
`slab`. Components compute in `compute_order`, and a structure whose component order refers
back on itself is refused at save with the cycle named.

`holiday_calendar`: `id`, `code`, `location_code`, `weekend_days`. `holiday`: `id`,
`calendar_id`, `on_date`, `name`.

`leave_policy`: `id`, `code`, `name`, `accrual`, `accrual_halves`, `accrual_cap_halves`,
`carry_forward_halves`, `carry_forward_expires_on`, `encashable`, `min_notice_days`,
`max_consecutive_halves`, `requires_document_after_halves`, `half_day`,
`negative_balance_halves`, `holiday_calendar_id`, `approval_levels`.

`leave_ledger_entry`: `id`, `employee_number`, `policy_code`, `kind`, `halves`,
`effective_on`, `source_id`. `kind` is `opening`, `accrual`, `availed`, `pending`,
`correction`, `encashment` or `lapse`. **The balance is the sum of these entries and is
never stored as a column**: `opening` plus `accrual` plus `correction`, minus `availed`,
minus `pending`, minus `encashment`, minus `lapse`.

`leave_request`: `id`, `employee_number`, `policy_code`, `from_date`, `to_date`, `half_day`,
`halves`, `reason`, `state`, `document_ref`, `created_at`. Two approved or availed requests
for one employee never cover the same date.

`attendance_punch`: `id`, `employee_number`, `at`, `direction`, `source`, `device_id`,
`location_code`, `confidence`, `raw_ref`, `created_at`. `raw_ref` is unique. **A row in this
table is never updated and never deleted once written.** Posting a `raw_ref` already present
writes no second row.

`attendance_day`: `id`, `employee_number`, `on_date`, `worked_minutes`, `status`,
`late_minutes`, `early_minutes`, `overtime_minutes`, `regularisation_id`. Derived from the punches, the
shift and the leave, and recomputed rather than edited.

`shift`: `id`, `code`, `starts_at`, `ends_at`, `grace_minutes`, `break_minutes`, `night`.
`roster_entry`: `id`, `employee_number`, `on_date`, `shift_code`, `reason`.

`regularisation`: `id`, `employee_number`, `on_date`, `reason`, `in_at`, `out_at`, `state`,
`created_at`.

`claim`: `id`, `employee_number`, `category`, `amount_minor`, `currency`, `spent_on`,
`receipt_ref`, `project_code`, `cost_centre_code`, `state`, `created_at`. A claim carries
`reimbursed_via_payroll` or `paid`, never both across its lifetime.

`approval`: `id`, `kind`, `subject_id`, `requested_by`, `level`, `approver_role`, `state`,
`decided_by`, `decided_at`, `reason`, `escalated_at`, `created_at`. `kind` is `leave`,
`regularisation` or `claim`. **A row that already carries a `decided_by` accepts no second
decision: of two decisions submitted at the same moment exactly one is accepted, the other is
refused as already decided, and the leave ledger moves once.**

`payroll_group`: `id`, `code`, `name`. `payroll_run`: `id`, `group_code`, `period`, `state`,
`reviewed_by`, `reviewed_at`, `signed_off_by`, `signed_off_at`, `total_gross_minor`,
`total_deductions_minor`, `total_net_minor`, `headcount_paid`, `locked_at`, `created_at`.
`period` is `YYYY-MM` and one run exists per group per period. **`signed_off_by` is never
equal to `reviewed_by`.**

`payslip`: `id`, `run_id`, `employee_number`, `gross_minor`, `deductions_minor`, `net_minor`,
`lop_days`, `published`. `payslip_line`: `id`, `payslip_id`, `code`, `kind`, `amount_minor`,
`rule_version`, `compute_order`. Once its run reaches `signed_off`, no figure on a payslip or
a payslip line changes.

`statutory_rule_set`: `id`, `code`, `jurisdiction`, `effective_from`, `effective_to`,
`version`. `statutory_rule`: `id`, `rule_set_id`, `code`, `state_code`, `basis`, `rate_bp`,
`threshold_minor`, `cap_minor`, `flat_minor`, `rounding`. **Every `payslip_line` whose
`kind` is a statutory deduction records the `version` of the rule set that produced it.**

`audit_entry`: `id`, `actor`, `action`, `subject_kind`, `subject_id`, `at`, `detail`. A
privileged action and its audit entry are both present or both absent.

**Derived, not stored.** The leave balance, every attendance day, the payslip totals and the
run totals are all derived from the rows above at read time or at computation time, and none
of them is a mutable column somebody edits.

**Proration.** A component marked prorated is scaled for a part-month, and the proration
applies to the gross before any statutory line is computed. A component not marked prorated
is paid whole.

**The computation, pinned with worked examples.** For a period, the gross is prorated by the
paid calendar days: `gross_minor` multiplied by (days in the period minus leave-without-pay
days) divided by days in the period, rounded half up. `BASIC` is `40` percent of the prorated
gross, `HRA` is `20` percent, and `SPECIAL` is the remainder. Then, from rule set `IN-2026-04`
version `1`:

| Head | Basis | Rule |
|---|---|---|
| `PF` | `BASIC` | `12` percent of `BASIC`, with the base capped at `1500000` minor units |
| `ESI` | prorated gross | `0.75` percent, and `0` when the prorated gross exceeds `2100000` minor units |
| `PT` | prorated gross, per state | `KA`: `20000` minor units when the prorated gross exceeds `1500000`, else `0`. `MH`: `20000` when it exceeds `1000000`, else `0` |
| `LWF` | flat, per state | `KA`: `2000` minor units, in June and December only, else `0` |
| `TDS` | annualised taxable gross | `0` up to `30000000`, then `5` percent of the excess up to `60000000`, then `20` percent of the excess above it; the annual figure divided by `12`, rounded half up |

Two worked rows, both for period `2026-07` in state `KA`, which has `31` days:

`E-1002` `Arjun Mehta`, `gross_minor` `5000000`, no leave without pay. Prorated gross
`5000000`. `BASIC` `2000000`. `PF` `180000`, because `12` percent of the capped base
`1500000` is `180000`. `ESI` `0`. `PT` `20000`. `LWF` `0`. Annualised taxable gross
`60000000`, so annual `TDS` is `1500000` and the monthly line is `125000`. Deductions
`325000`. Net `4675000`.

`E-1001` `Nadia Fernandes`, `gross_minor` `3100000`, one leave-without-pay day. Prorated
gross `3000000`, because `3100000` times `30` divided by `31` is `3000000`. `BASIC`
`1200000`. `PF` `144000`. `ESI` `0`. `PT` `20000`. `LWF` `0`. Annualised taxable gross
`37200000`, so annual `TDS` is `360000` and the monthly line is `30000`. Deductions `194000`.
Net `2806000`.

The employer's `PF` contribution is an `employer_contribution` component and never reduces
net pay.

**Conventions.** Money is an integer in the currency's minor unit with the currency code
beside it, and rounding is per statutory rule and recorded per line. Every dimension on an
employee is effective-dated, so a query for a past date reconstructs the state at that date;
a punch stores an absolute instant and its location's zone. People authenticate with a token
and a device authenticates with a scoped key that can post punches and nothing else.
Pagination is by cursor, `50` by default and `500` at most. Idempotency is required on
punches by `raw_ref` and on every run transition. An error body is
`{ "error": { "code", "message", "field" } }`.

**Invariants.** Ten properties the product may never violate, each observable from outside:

- The account that prepares a payroll run is never the account that signs it off.
- A leave balance always equals the sum of its ledger.
- An attendance punch is never updated or deleted; a correction is a regularisation.
- A closed payroll run's figures never change.
- An employee's state at any past date is reconstructable from `employment_change`.
- A claim is paid through payroll or through a batch, never both.
- A request carrying a decision accepts no second decision.
- A salary figure is readable only by a `payroll` account, including through the register.
- No privileged action commits without its audit entry, in the same transaction.
- Every statutory line records the rule version that produced it.

**Retention.** An employee record is retained for the statutory period of its jurisdiction
after exit, which is longer than any product-level preference and is therefore not
configurable downward. Punches are retained `3` years and audit entries `7` years. Nothing
in this build deletes any of them.

**Seed data.** One organisation named `Cadrix` across the states `KA` and `MH`, with the
holiday calendars `KA-2026` and `MH-2026`. `KA-2026` carries `2026-08-19` as the holiday
`Independence Observance` and its weekend is Saturday and Sunday.

`120` employees across the departments `ENG`, `OPS`, `FIN` and `PEOPLE`, including two
joiners this month, one employee `on_notice` and one `alumni`. The named seven of the
`## User roles` table are seeded with those exact numbers, names and reporting lines, plus
`E-1004` `Marcus Bell` in `ENG` reporting to `E-2001`.

Two payroll groups: `MONTHLY-CORE` holding `E-1001`, `E-1002`, `E-1003` and `E-1004`, and
`MONTHLY-OPS` holding everybody else. Both seeded payroll accounts own both groups, so either
reads the whole directory and either works either group's run. Salary structures: `E-1001` `3100000`, `E-1002`
`5000000`, `E-1003` `2000000`, `E-1004` `4000000`, each in `inr`.

Three leave policies. `ANNUAL` accrues `4` halves monthly to a cap of `60` halves, carries
`10` halves forward expiring `2026-12-31`, is encashable, needs `2` days notice, allows at
most `30` consecutive halves, permits half days, allows no negative balance, uses the
calendar of the employee's location and has one approval level. `SICK` accrues `24` halves
yearly, carries nothing forward, requires a document above `4` halves and has one approval
level. `UNPAID` accrues nothing and allows a negative balance of `20` halves.

`E-1001` on `ANNUAL` holds `20` opening halves, seven monthly accruals of `4`, `8` availed
and `4` pending, for a balance of `36` halves.

`31` days of July 2026 attendance for the `MONTHLY-CORE` group, including four `unpaired`
days and two `pending` regularisations. Twelve claims spread across every claim state, of
which one is `submitted` at `2500000` minor units, which is above the manager's limit and is
therefore waiting on `payroll`.

Pending work waiting in the queue on a first start: one `pending` `ANNUAL` leave request
from `E-1001` covering `2026-09-21` to `2026-09-22`, which is the `4` pending halves above
and which waits on `E-2001`; one `pending` `ANNUAL` leave request from `E-1003` covering
`2026-09-28` to `2026-09-29`, which waits on `E-2002`; and the `submitted` claim of
`2500000` minor units, whose approval waits on a `payroll` account rather than on a
`manager`. Every one of the three carries an approval row in the queue with no decider.

Payroll runs: `2026-05` and `2026-06` for `MONTHLY-CORE`, both `closed` with their registers
and published payslips; `2026-07` for `MONTHLY-CORE` at `locked`; and `2026-08` for
`MONTHLY-CORE` at `open`, which is the period a preparer takes through the whole lifecycle from
the beginning. When `2026-07` is
computed its totals are `total_gross_minor` `14000000`, `total_deductions_minor` `925000`,
`total_net_minor` `13075000` and `headcount_paid` `4`.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the supplied visual and behavioural specification. Every value in it is
contract. Where it leaves a value open it says so, and where it describes a colour rather
than naming one, the exact shade is the builder's to choose so long as the stated
relationship holds.

### How the design was measured, and what was not

The reference generates its styles as the page runs, so no stylesheet was available to
parse: the declared-colour channel and the typography channel both came back empty. Every
colour below was read from the computed styles of the rendered page, which is strong
evidence for colour and for effects. The type family and the rendered scale were recovered
not at all, so the family is a normative substitute and the scale is derived from the
screenshots rather than measured. The capture reached twelve public routes at three widths
and could not pass the sign-in control, so the console itself is specified rather than
observed. That is the evidence gap, and the substitution for it is stated wherever it bites:
the type scale, the illustration and the wordmark are reconstructions, everything else is
measured. Treat the colour roles as exact and the type scale as the reconstruction it is.

### Information architecture

Twelve routes, listed in `## User flow`. The console is one product behind one sign-in: the
public surface is the sign-in route and the not-found page and nothing else. Navigation is a
left rail carrying the modules in a fixed order: the employee's own surface, the directory,
the approval queue, attendance, and payroll, with the account control at the foot. The work
surface is a queue list: rows down the page, the deciding context opening in place, and the
filter above it. Creating a request opens a new row at the top of the list rather than a
separate page or a layer. Feedback is the row itself, which updates the moment the action is
taken rather than waiting for the response.

### The ground and the text ladder

The page ground and every card ground are a near-white neutral, and it is the single most
used value in the product. Primary text is a near-black neutral and is reserved for
headings. Body copy is a deep neutral, and that inversion is measured rather than preferred:
the softer grey carries the reading and only the headings take the near-black. Captions and
meta are a mid neutral.

Hairlines are a near-white neutral one step down from the ground. Table rules are a
near-white neutral one step darker again. A table header and any sunk panel take a
near-white neutral, and the same panel on a cool surface takes a near-white neutral with a
cooler cast. Four steps, and no border anywhere a luminance step will do.

### The brand and the accents

| Role | Colour |
|---|---|
| the wordmark, emphasis words and in-content links | a mid, vivid violet |
| the primary button ground and the footer ground | a deep, soft indigo |
| the primary button hover | a light, vivid violet |
| the brand on a dark ground | a light, soft violet |
| the announcement bar ground | a near-white neutral with a violet cast |
| the eyebrow pill | a light, soft orange |

### The four summary tiles

Four pastel grounds, one per headline statistic, in a fixed order across the top of the home
screen: a near-white neutral with a mint cast for the countries figure, a near-white cool
neutral for the companies figure, a near-white warm neutral for the employees figure, and a
near-white neutral with a violet cast for the products figure. Those four plus the eyebrow
pill and the brand violet are the whole of the home screen's colour.

### Semantic colour, for the console

| Meaning | Colour | Its ground |
|---|---|---|
| approved, present, paid | a mid, vivid green | a near-white neutral |
| pending, awaiting approval | a mid, vivid orange | a near-white warm neutral |
| rejected, absent, failed | a mid, vivid red | a near-white warm neutral |
| informational | a mid, vivid blue | a near-white cool neutral |
| draft, not applicable | a mid cool neutral | the page ground |

Normative: a leave state, an attendance state and a payroll state are never communicated by
colour alone. Every state pill carries its state as text.

### Type, exactly

One variable sans family for the interface and one tabular-figure family for every number in
a payroll or attendance context.

| Role | Size | Line height | Weight |
|---|---|---|---|
| Display | `56px` | `64px` | `700` |
| Page title | `32px` | `40px` | `700` |
| Section heading | `24px` | `32px` | `600` |
| Card title | `18px` | `26px` | `600` |
| Body | `16px` | `24px` | `400` |
| Secondary | `14px` | `20px` | `400` |
| Label | `13px` | `18px` | `600` |
| Micro | `11px` | `16px` | `600` |
| Figure, tabular | `24px` | `32px` | `700` |

### Radius, border, elevation and density

Pills, buttons and the announcement bar are fully rounded. Cards are the next step down,
panels and inputs a step below that, chips and small controls below that again, and swatches
barely rounded at all. Borders are a single hairline. Elevation is limited to floating
surfaces: a menu, a sticky bar, a dialog and a transient message.

Two densities. Comfortable rows on the home screen and the employee surface. Compact rows on
the directory, the register, the approval queue and the attendance grid, and compact is the
default on every one of those with a control to switch. Somebody working a thousand-row
register needs rows, not whitespace.

### Iconography and illustration

The wordmark is a lowercase word set in the brand violet with a raised dot over one letter
and a small two-letter suffix below the baseline at the end. Interface glyphs are a single
consistent stroke weight and every icon-only control carries a label. Illustration is
generated rather than sourced: flat, built from the palette above, carrying no photograph of
a person and no third-party mark, and every content image carries alternative text while a
decorative one declares itself decorative.

Zero-asset substitution is the rule for everything the product ships. No photograph, no
third-party logo, no certification badge and no downloaded illustration: each is replaced by
a mark drawn from the palette and the geometry above. Fonts are self-hosted and no font
service is called at run time, so the product renders identically with the network away.

### Global chrome

An announcement bar sits above the header on its violet-cast ground and can be dismissed for
the session. The header carries the wordmark, the primary navigation and the account control.
Buttons come in a primary, a secondary and a quiet variant, and only the primary wears the
indigo ground. The product shell is a left rail carrying the modules, which collapses to
icons and then to a sheet as the window narrows.

### The five states, everywhere

Every surface in the console defines five states and they are the same five everywhere:
loading, which holds a skeleton; empty, which names the next action; populated; error, which
names what failed and offers the retry; and refused, which names what was refused and why.
Search is one field over people, requests and runs, reflected in the address so a result can
be linked and restored on back.

### Motion, as moments

The reference declares ten curves and four of them carry the site: a house ease on hovers and
colour, a long decelerate on panels and menus opening, an overshoot on anything that pops,
and a stronger overshoot on the announcement pill. One runtime animation was captured across
the whole reference, which is a site that barely moves, and the console behind it moves less.
The durations are not carried here: motion is specified as moments and characters, never as a
curve or a number, and the exact easing is yours so long as one house ease carries everything
that is not one of the four moments below.

Four moments move and nothing else does. A panel or a sheet opens on the long decelerate. A
row changes state on the house ease. A skeleton holds while a list is loading. A progress
indicator runs through a payroll computation. The two things that pop, the announcement pill
and a transient message, overshoot very slightly and settle.

A mega-menu opens on a pointer and on a click without one, translating up as it fades in, and
it waits a beat before closing so that a diagonal pointer path to a distant item does not
dismiss it, which is the detail every mega-menu gets wrong.

Under a reduced-motion preference panels appear without travel, skeletons hold their first
frame, and the payroll progress indicator continues.

### Responsive, by surface

| Surface | Narrowest | Middle | Widest |
|---|---|---|---|
| Product shell | the rail becomes a sheet | the rail collapses to icons | the full rail |
| Directory | cards carrying name, designation and status | a table with fewer columns | the full table |
| Month grid | one employee at a time, days down | seven days across with paging | the full grid |
| Register | not offered: the screen states that it needs a wider window and offers the export | horizontally scrolled with a frozen first column | full |
| Employee surface | full, and built narrowest first | full | full |
| Approvals | full, built narrowest first | full | full |

Two of those are deliberate. The register is not made to work on a phone: it is refused with
an explanation and an export, because a forty-column financial table on a small screen is a
way to make an expensive mistake. The employee surface and the approval queue are built for
the narrow width first, because that is where they are actually used.

### Copy that ships as written

| Where | Copy |
|---|---|
| the directory, empty | `No people yet` above `Add your first employee or import a list.` |
| the approval queue, empty | `Nothing waiting` above `Requests from your team will appear here.` |
| a peer manager refused a decision | `Not your report` |
| a manager deciding their own request | `You cannot decide your own request` |
| a second decision on a decided request | `Already decided` |
| a run signed off by its reviewer | `Sign-off needs a second pair of eyes` |
| a total net typed back wrongly | `That total does not match the run` |
| the register on a narrow window | `The register needs a wider window` above `Export the register instead.` |
| the not-found page | `That page does not exist` above `Back to your console.` |

## Constraints

One organisation. Every read and every write is scoped to it, and there is no second tenant
to isolate from. No money leaves the product: there is no payment initiation, no bank file
and no external financial call at run time.

Not built and not to be added: onboarding, exit, clearance or the final settlement; a typed
assistant of any kind; a report builder, report scheduling or export delivery; payroll
pre-flight variance, the statutory calendar or workforce cost planning; delegation of
approval to a colleague; support staff impersonation or a time-boxed staff access grant;
billing, plans, invoices or metering; integrations, webhooks or a public API key; document
generation, letters or certificates; outbound email, SMS or push of any kind, including
notifications, because the queue is the notification; a second factor, a password reset flow,
federated identity beyond the provider named here, or any self-service signup; a native or
mobile application; and any marketing route, pricing page or public website.

Performance is a capability requirement rather than a preference. The app stays responsive
at `10000` employees in the directory, `1000` employees by `31` days
in the attendance month grid, `10000` employees by `40` components in the payroll register,
and `12` months of history for reporting reads.

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
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable
  from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `{ "email", "password" }` | `{ "access_token", "employee_number", "role" }` |
| `GET /api/me` | - | `{ "employee_number", "full_name", "email", "role", "manager_employee_number", "department_code" }` |
| `GET /api/health` | - | `{ "status" }` |
| `GET /api/employees` | `?department_code=&cursor=` | a top-level array of `{ "employee_number", "full_name", "designation", "department_code", "location_code", "manager_employee_number", "state", "joining_date" }`, with `X-Next-Cursor` |
| `GET /api/employees/{employee_number}` | - | `{ "employee_number", "full_name", "email", "state", "manager_employee_number", "department_code", "location_code", "payroll_group_code" }` |
| `POST /api/employees/{employee_number}/changes` | `{ "field", "to_value", "effective_from", "reason" }` | `{ "id", "field", "from_value", "to_value", "effective_from", "approved_by" }` |
| `GET /api/leave-balances` | `?employee_number=&policy_code=` | a top-level array of `{ "policy_code", "opening", "accrual", "availed", "pending", "correction", "halves", "days" }` |
| `GET /api/leave-ledger` | `?employee_number=&policy_code=` | a top-level array of `{ "id", "kind", "halves", "effective_on", "source_id" }` |
| `POST /api/leave-requests` | `{ "policy_code", "from_date", "to_date", "half_day", "reason" }` | `{ "id", "state", "halves", "days", "approval_id" }` |
| `GET /api/leave-requests` | `?employee_number=&state=&cursor=` | a top-level array of `{ "id", "employee_number", "policy_code", "from_date", "to_date", "halves", "state" }` |
| `GET /api/approvals` | `?kind=&state=&cursor=` | a top-level array of `{ "id", "kind", "subject_id", "requested_by", "summary", "age_days", "state", "decided_by" }`, with `X-Next-Cursor` |
| `GET /api/approvals/{id}` | - | `{ "id", "kind", "subject_id", "requested_by", "state", "decided_by", "decided_at", "reason", "context" }` |
| `POST /api/approvals/{id}/decide` | `{ "decision", "reason" }` | `{ "id", "state", "decided_by", "decided_at" }` |
| `POST /api/attendance/punches` | `{ "employee_number", "at", "direction", "source", "device_id", "raw_ref" }` | `{ "id", "raw_ref", "accepted" }` |
| `GET /api/attendance/days` | `?employee_number=&month=` | a top-level array of `{ "on_date", "status", "worked_minutes", "late_minutes", "early_minutes", "overtime_minutes", "regularisation_id" }` |
| `POST /api/regularisations` | `{ "on_date", "in_at", "out_at", "reason" }` | `{ "id", "state", "approval_id" }` |
| `POST /api/claims` | `{ "category", "amount_minor", "currency", "spent_on", "receipt_ref" }` | `{ "id", "state", "approval_id", "decided_by_role" }` |
| `GET /api/claims` | `?employee_number=&state=&cursor=` | a top-level array of `{ "id", "employee_number", "category", "amount_minor", "currency", "spent_on", "state" }` |
| `POST /api/payroll-runs` | `{ "group_code", "period" }` | `{ "id", "group_code", "period", "state" }` |
| `GET /api/payroll-runs/{period}` | `?group_code=` | `{ "id", "group_code", "period", "state", "reviewed_by", "signed_off_by", "total_gross_minor", "total_deductions_minor", "total_net_minor", "headcount_paid" }` |
| `POST /api/payroll-runs/{period}/lock` | `{ "group_code" }` | `{ "state", "inputs_summary" }` |
| `POST /api/payroll-runs/{period}/compute` | `{ "group_code" }` | `{ "state", "computed", "blocking_findings" }` |
| `POST /api/payroll-runs/{period}/review` | `{ "group_code" }` | `{ "state", "reviewed_by" }` |
| `POST /api/payroll-runs/{period}/signoff` | `{ "group_code", "confirm_total_net_minor" }` | `{ "state", "signed_off_by", "signed_off_at" }` |
| `GET /api/payroll-runs/{period}/register` | `?group_code=&department_code=&cursor=` | `{ "rows", "totals", "filtered" }`, with `X-Next-Cursor` |
| `GET /api/me/payslips/{period}` | - | `{ "period", "gross_minor", "deductions_minor", "net_minor", "lop_days", "lines" }` |

Every list endpoint returns a top-level JSON array. Field names are exact. The token a
successful sign-in returns is carried on every later call as a bearer credential, and the
field holding it is named `access_token`. Bearer auth is
required on everything except `GET /api/health` and `POST /api/auth/login`. A successful call
returns the named shape; an invalid or unauthorized call is rejected as a client error, never
a `5xx` and never a silent success, and carries a reason. The agent chooses conventional
codes. `POST /api/attendance/punches` accepts a scoped device key or any signed-in caller's
bearer credential: a punch is evidence of a moment rather than an assertion of authority, and
the row records which credential posted it.

### No mocks

PostgreSQL and Keycloak are the facts. An in-memory employees dictionary, a users table the
app keeps beside Keycloak's realm and signs its own tokens against, a hardcoded
`{"status":"approved"}` response the app returns to itself, a balance column the app
increments instead of a ledger it sums, or a seeded register served from a fixture file are
all contract violations however good the interface looks. The named provider is the fact: the
app's UI and its own tables can only reflect what lives in the provider, never substitute for
it.

## Definition of done

A manager signs in, opens one queue holding every request their own team has raised, reads
the balance and the roster beside a leave request, and approves it, and the booked day
reaches the open payroll run without anybody retyping it. A manager from another team cannot
decide that request and the request stays pending. An employee reads their own balance and
can expand it into the entries that produce it. A payroll run locks its inputs, computes
every employee or none, and is signed off only by an account that did not prepare it, against
a total net typed back exactly.
