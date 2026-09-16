# Switchyard Grid Switching Console

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, sign in as the seeded control
room operator, acknowledge the live alarm on recloser `4B-RCL-118`, draft a switching order
against the published network model, run the study that predicts each step's electrical
consequence, send the order for approval, and watch a coordinator approve it and the operator
execute step one, without hitting an error page. The hard part is that authority is the product:
an operator must never be able to approve an order, nobody may approve an order they created once
its risk class reaches 2, and a live isolation permit must block a re-energizing step while the
order is still being written rather than when the step is run. Those refusals are enforced by the
server on every request and the stored row is left exactly as it was, so a hidden button is not a
refusal.

## Overview

Switchyard is the console a distribution control room works from. It holds the electrical network
as a versioned model, the live measurements arriving from every monitored point, the alarms those
measurements raise, the incidents operators open when protection operates, the switching orders
that restore supply, the isolation permits that keep crews safe while they work on de-energized
plant, and the append-only record of everything that was decided and done.

The distinctive central interaction is the **operations canvas**: one continuous surface holding
the whole network, which every other panel docks over and links back to. It is not a map view
inside the product; the canvas is the product, and the panels are lenses onto it.

It exists because that work is currently spread across a diagram on one screen, a measurement
system on another, a spreadsheet holding the switching order, an email thread holding the
approval and a radio holding the crew. The operator joins them in their head at three in the
morning, and join errors under load are the dominant cause of switching incidents. Three failures
follow: the switching order is not bound to the network model it operates on, so an order written
against last week's topology can be executed against this week's; the electrical consequence of a
step is not available at the moment the operator needs it; and the regulatory record is
reconstructed from logs and recollection weeks later. Switchyard binds every artefact to an
immutable model version, answers "what happens if I open this" before the device is opened, and
writes the record as the work happens.

The people who use it are control room operators on a rotating roster, the coordinator who takes
command when an event outgrows one desk, the controller who countersigns the most consequential
acts, and the auditor who has to reconstruct what happened and prove the record was not altered.
The buyer is a committee, the data is a regulated asset, and every network-affecting action needs
a human decision recorded against a named identity.

What it deliberately is not. It is not a control system: it does not poll field devices and does
not own the path to them. It emits a signed instruction and waits for a measurement to confirm the
device actually moved. It does not bill anybody's electricity customers. There is no self-serve
signup, no public product surface and no unauthenticated route that returns anything but the
sign-in entry, the terms page and static assets. There is no offline replica, no white-label mode
and no report builder. Nothing in it switches autonomously.

The genuinely hard part is that approval is bound to a specific sequence of steps rather than to
an order, and that the binding has to survive editing, concurrency and a model version being
republished underneath it.

## User roles

Four roles. Signup is closed: accounts exist only because they are seeded into the identity
provider's realm, and the app offers no way to create one.

| Role | Can read | Can write |
|---|---|---|
| `operator` | The full published model, live and historical measurements in full inside an assigned operating area and as aggregates outside it, alarms, incidents touching their area, orders, permits, crews | Acknowledge and suppress alarms in their area; open incidents; create, edit and submit switching orders in their area; execute steps of an approved order in their area; record an attributed manual position override. **Cannot approve any switching order, including one they did not create. Cannot publish a model version. Cannot issue or release an isolation permit. Cannot read the append-only record.** |
| `coordinator` | Everything an operator reads, across every operating area, plus their own actions in the record | Everything an operator writes, plus: assume command of an incident, set its severity, close it; approve or reject switching orders of risk class 1 to 3; issue, release and revoke isolation permits; assign and recall crews; reconcile a position override; approve a model version. **Cannot give the second signature on a risk class 4 order. Cannot publish a model version. Cannot read another identity's actions in the record.** |
| `controller` | Everything a coordinator reads, plus the whole record | Everything a coordinator writes, plus: give the second, distinct signature that a risk class 4 order requires; publish a model version that a coordinator has approved. **Cannot delete a record entry, which no role can do.** |
| `auditor` | The whole append-only record, the grant history, and every incident, order and permit as read-only | Nothing operational at all. May run a verification over a window of the record. **Cannot acknowledge an alarm, open or close an incident, touch an order or a permit, assign a crew, or change any configuration. Cannot delete a record entry.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from an `operator` session to any `coordinator`-only or
`controller`-only endpoint must be rejected by the server (an unauthorized request is denied, not
served), leaving the protected state unchanged.

Two rules cut across the table and are not role checks:

- **Scope by relationship, not only by role.** An `operator` may act only on elements and orders
  whose operating area is one of their assigned areas. The identical action against the identical
  element in a different area is denied, from both read-write endpoints and from execution.
- **No self-approval.** No identity may approve a switching order they created once the order's
  risk class is 2 or higher, whatever role they hold. This rule is never weakened.

No role holds a capability to delete a record entry. The capability does not exist in the product.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Role | Assigned areas |
|---|---|---|
| `operator@example.com` | `operator` | `Northgate` |
| `operator2@example.com` | `operator` | `Harbourside` |
| `coordinator@example.com` | `coordinator` | `Northgate`, `Harbourside` |
| `controller@example.com` | `controller` | `Northgate`, `Harbourside` |
| `auditor@example.com` | `auditor` | none |

## Core features

### Auth

Accounts live in the identity provider, not in this application. The app stores no password and
offers no signup, no password reset and no invitation.

1. The sign-in surface takes an email address. The app resolves it against the identity provider's
   realm, relays the credential to the provider for validation, and on success mints its own
   session. A credential the provider rejects produces a refusal that says the credential was not
   accepted and names neither which half was wrong nor whether the email exists, and the response
   takes the same time whether or not the address is known.
2. Signing in is `POST /api/auth/login` carrying `{"email", "password", "company_website"}`. A
   successful sign-in returns `{"access_token": "..."}` plus the acting identity, and records the
   provider's subject identifier, the email, the display name and the realm roles on the session,
   resolving the assigned operating areas from the account. The client sends that token as a
   bearer token on every other call, and sends nothing else. Signing out is `POST /api/auth/logout`.
3. Every request resolves role and assigned areas from the token on the server. A request carrying
   no token, an expired token, a malformed token or a token the server does not know is denied; a
   request whose role does not hold the endpoint's capability is denied and the response names the
   capability required.
4. Signing out ends the session and returns to the sign-in surface. A token presented after
   sign-out is denied.
5. Sessions expire 12 hours after they are created, matched to the longest shift, so that a
   session cannot outlive the shift that authorized it.

### The network model, versioned

6. Elements, connectivity and operating areas belong to a model version identified by an
   increasing integer called its train. Exactly one version is in state `published` at a time.
   The seeded published version is train `418`; train `419` exists in state `ready` and is not
   published.
7. A published version is immutable. There is no edit path. A correction is a new version, and
   publishing a new one moves the previous one to `superseded` and records the successor on it.
8. Publishing runs in two acts by two distinct identities: a `coordinator` moves a `ready` version
   to `pending_approval` by approving it, and a `controller` publishes it. The same identity
   cannot do both. A `controller` attempting to publish a version nobody has approved is refused,
   and the version stays `ready`.
9. Publishing is refused while any switching order anywhere is in state `executing` or
   `suspended`. The refusal names every blocking order by its reference and the version stays
   `pending_approval`.
10. Publishing never invalidates work in flight. Orders, permits and study runs stay pinned to the
    version they were created against.

### Live measurements

11. Every measurement point declares a quantity and a unit. Every sample carries a value, an
    `observed_at` instant, a `received_at` instant, a `quality` of `good`, `suspect`, `stale`,
    `indeterminate`, `manual` or `estimated`, and a `source`. A sample submitted without a quality
    is rejected, named in the response's `rejected` list, and the rest of the batch is accepted. A
    sample whose unit differs from its point's declared unit is rejected and never converted.
12. The console shows the latest value per point with its age. A point whose newest sample is
    older than its declared expected period is marked stale, and the surface says how old the
    reading is. The product never presents a stale value as current.
13. A measurement history request returns a series over a window, served from a rollup rather
    than from raw samples wherever the window is wide. Where the window is long enough
    that more than one stored sample falls per rendered point, the response returns the minimum and
    the maximum per bucket and says so, rather than a mean, so that a transient inside a bucket
    survives. A mean-only reduction hides exactly the events an operator is looking for and is not
    acceptable.
14. Only a machine identity holding the ingest scope may write a measurement. A signed-in human
    session attempting to write one is denied, whatever its role, because an operator able to
    manufacture a measurement can manufacture the evidence their own actions are judged against.

### Alarms

15. Alarm rules are evaluated continuously against arriving measurements, and a rule that matches
    raises an alarm. An alarm carries a severity of 1 to 4, a state of
    `active`, `acknowledged`, `cleared` or `suppressed`, and a server-computed integer
    `computed_priority` that the client never calculates. Alarms are listed in descending
    `computed_priority`. The priority is `(5 - severity) * 10000`, plus the number of customers at
    risk on the alarm's element capped at `9000`, plus `500` when that element sits inside a live
    isolation permit's isolated set, plus `250` when the alarm is bound to an incident. Worked
    example: the seeded severity 2 alarm on `4B-RCL-118`, with 4412 customers at risk, no permit
    and no incident binding, has `computed_priority` `34412`.
16. Acknowledging has exactly one winner. Two operators acknowledging the same alarm at the same
    moment produce one acknowledgement: the first is accepted, the second is refused with the code
    `ALARM_ALREADY_ACKNOWLEDGED` naming the acknowledging identity and the instant, the losing
    client's optimistic state is reverted in view, and the record carries exactly one
    acknowledgement entry for that alarm.
17. Suppressing needs a reason of 8 to 500 characters and a duration between 60 and 86400 seconds.
    Either outside its range is rejected, the field is named, and nothing is written. Suppressing
    an alarm whose element sits inside a live isolation permit's isolated set is refused with the
    code `SUPPRESSION_BLOCKED_BY_PERMIT` naming the permit's reference, and the alarm stays
    `active`.
18. An operator may acknowledge or suppress only an alarm whose element is inside one of their
    assigned areas. The same call against an element in another area is denied with the code
    `OUT_OF_AREA` and the alarm row is unchanged.

### Incidents

19. An `operator` or a `coordinator` opens an incident with a severity of 1 to 4 and an optional
    set of seed alarms, which become bound to it. The seeded incident is `INC-4471` at severity 2
    in state `open` with no commander.
20. A `coordinator` assumes command by sending the command version they believe is current. If it
    still is, they become commander, the version increments and the incident moves to `commanded`.
    If it is not, the call is refused with the code `COMMAND_VERSION_CONFLICT` naming the identity
    that currently holds command, and nothing changes. Exactly one identity holds command at a
    time.
21. The incident timeline is append-only and ordered by a server-assigned sequence that is gapless
    within the incident. Client timestamps are recorded and never used for ordering, so two notes
    posted at the same instant cannot interleave incorrectly. A note is 1 to 4000 characters.
22. Closing an incident is refused while any of the following is true, and the refusal lists every
    blocker with its kind and its reference: an order attached to the incident is `executing` or
    `suspended`; an isolation permit scoped to the incident is `live`; a manual position override
    made during the incident has not been reconciled; customers remain unrestored with no recorded
    reason. The incident stays `open` or `commanded`.
23. The outage attached to an incident carries a customer impact snapshot. While its
    `resolution_state` is `estimating` the affected count is a minimum and a maximum and is
    rendered as a range in words; it is never collapsed to a midpoint and never animated as though
    converging on one. The seeded snapshot reads `customers_affected_min` `4100`,
    `customers_affected_max` `4700`, `sensitive_customers_count` `61` and an estimated
    interruption cost of `182400` integer minor units in `usd`, which is `$1,824.00`.
24. Reading the sensitive customer register is capability-gated and writes a record entry on every
    read carrying the count returned and not the identities. It is the most restricted data in the
    product.

### Switching orders

This is the feature the product exists for, and its rules are the ones that must hold under
pressure.

25. An order is created against an operating area and pins the currently published model version at
    the moment of creation. The seeded order is `SWO-2026-014`, state `draft`, pinned to train
    `418`, area `Northgate`, owned by `operator@example.com`, with no steps.
26. A step names an element by its stable key and an action from `open`, `close`, `isolate`,
    `earth`, `remove_earth`, `tag`, `untag` and `verify`. Steps are added inline to the step list by
    picking the device on the network view, never through a separate page. Ordinals are dense and
    contiguous, and reordering, inserting or deleting renumbers the rest.
27. The order carries a `step_sequence_hash`, which is a digest over its ordered step list. A step
    added, edited, reordered or deleted recomputes it.
28. A study, which is a simulation of the order against the pinned model, returns for each step in
    order the predicted post-step state: the elements that end
    de-energized, the customers de-energized, the per-conductor loading against its rating, and any
    violation. The study is deterministic: the same order, the same pinned version and the same
    base-state instant produce identical results every time. Loading on a conductor is the sum of
    the seeded section load of every conductor that would be fed through it after the step, divided
    by its rating and rounded to three decimal places. A loading above `1.000` is a `thermal`
    violation at severity `critical`; a loading from `0.800` to `1.000` inclusive is a `thermal`
    violation at severity `warning`. Worked example on the seeded network: with `4B-RCL-118` open,
    closing tie `NG-TIE-330` while sectionalizer `NG-SEC-142` is closed back-feeds both
    `NG-OHL-2202` (section load `58.0` A) and `NG-OHL-2203` (section load `38.0` A) onto
    `HS-OHL-3301`, which already carries `118.0` A against a rating of `200` A, giving `214.0` A
    and a loading of `1.070`, a `critical` thermal violation. Opening `NG-SEC-142` first
    back-feeds only `NG-OHL-2203`, giving `156.0` A and a loading of `0.780`, which is clean.
29. Submitting moves the order to `pending_approval` and records the hash being submitted.
30. **Approval is of a step sequence, not of an order.** An approval records the exact
    `step_sequence_hash` it approved. An order may be `approved`, `executing` or `completed` only
    while its `approved_hash` equals its current `step_sequence_hash`. Editing any step of an
    `approved` order returns it to `draft`, clears `approved_hash`, and the approval is void. There
    is no path that leaves an order approved against a sequence nobody approved.
31. **An `operator` cannot approve.** An `operator` session calling approve on any order, their own
    or anyone else's, is denied. The order's state, its `approved_hash` and its approval history are
    unchanged, and nothing is written.
32. **Nobody approves their own order at risk class 2 or above.** A `coordinator` who created an
    order of risk class 2 or higher and calls approve on it is refused with the code
    `SELF_APPROVAL_DENIED`, the refusal names the separation-of-duty rule, and the order stays
    `pending_approval`.
33. Risk class is computed on the server and the client never calculates or overrides it. It is 1
    when fewer than 500 customers are at risk, 2 from 500 to 1999, and 3 at 2000 or more or
    whenever the order closes a normally-open tie while the alternate source is still connected. It
    is 4 when the order both reaches 2000 customers and creates that parallel path. A risk class 1
    to 3 order needs one approval from a `coordinator` or a `controller`. A risk class 4 order needs
    two approvals from two distinct identities, at least one of them a `controller`; a single
    approval leaves it in `pending_approval`. Worked example: `SWO-2026-014` puts 4412 customers at
    risk and is risk class 3.
34. Two identities approving the same order at the same moment produce exactly one approval record.
    The second is refused with the code `VERSION_CONFLICT` naming the approval that won, and the
    order has a single approval for that hash.
35. Executing a step requires a confirmation token minted for that step and that identity, valid
    for 120 seconds and usable once. A call without one, with an expired one, with one minted for a
    different step, or with one already spent is refused with the code `CONFIRMATION_REQUIRED` and
    no instruction is emitted. This makes one-click execution impossible even from a client that
    is not this product's own.
36. Executing is refused, with nothing written and no instruction emitted, when any of these holds:
    the order is not `approved` or `executing`; `approved_hash` does not equal
    `step_sequence_hash`, which is the code `APPROVAL_HASH_MISMATCH`; the step's ordinal is not the
    next one, which is `STEP_OUT_OF_ORDER`; the step's element is absent from the pinned model
    version, which is `MODEL_VERSION_ELEMENT_MISSING`; a live isolation permit forbids the action,
    which is `SAFETY_DOCUMENT_CONFLICT` naming the permit; the order's operating area is not one of
    the caller's assigned areas, which is `OUT_OF_AREA`; or the record cannot be written, which is
    `AUDIT_UNAVAILABLE`.
37. **A step is executed exactly once.** Each step is given an idempotency key when the step is
    created, not when it is executed. Two simultaneous executions of the same step produce exactly
    one execution attempt, exactly one emitted instruction, exactly one record entry, and both
    callers receive the same body. A repeat of a completed execution returns the original outcome
    and emits nothing.
38. Execution is durable. A step execution that is in flight when the process restarts resumes
    from where it was rather than starting again, and because the step's idempotency key was
    written when the step was created, the resumed execution emits no second instruction. The
    execution workflow survives a restart; the instruction is emitted once.
39. A step is not confirmed by the operator asserting it. Execution emits a signed instruction and
    moves the step to `instructed`; the step reaches `confirmed` only when a measurement reports
    the device in its commanded position with quality `good`. If no confirming measurement arrives
    within 30 seconds the step moves to `failed`, a manual confirmation path is offered, and the
    product never retries a control instruction on its own.
40. Publishing a newer model version while an order is executing does not stop it. The order stays
    pinned to the version it was approved against, a non-blocking drift notice appears naming both
    trains, and execution continues. Only a pending step whose element is absent from the pinned
    version blocks, and it blocks with the element named.
41. An order may be suspended with a reason and resumed from where it stopped, or aborted with a
    reason of 12 to 1000 characters. An aborted order keeps every completed step and its execution
    history; nothing is rolled back and nothing is deleted.

### Isolation permits

42. A permit binds a crew, an isolated set of elements and the isolating devices that isolate them.
    Issuing it always validates first, and the validation asserts against live measurements rather
    than against the order's intent: every isolating device must report its required position with
    quality `good`. A device reporting `indeterminate` or `stale` fails validation and the response
    names that device, its quality and the instant the reading was taken. Worked example on the
    seeded network: validating the permit over `NG-OHL-2202` with isolating devices `4B-RCL-118`
    and `NG-SEC-142` fails, because `NG-SEC-142` reports switch position quality `indeterminate`.
43. Issuing without a passing validation is refused with the code `SAFETY_VALIDATION_FAILED` and no
    permit is created. A client-side check is not a validation.
44. When a permit issues it stores the value, the quality and the `observed_at` instant of every
    isolating device as of the validation, so the issue is provable afterwards.
45. A live permit blocks re-energization **at authoring time**. Adding a step whose action would
    energize any element inside a live permit's isolated set is refused while the order is being
    written, with the code `SAFETY_DOCUMENT_CONFLICT` naming the permit, and no step is added. It
    is not left to fail at execution.
46. Releasing a permit requires an explicit all-clear confirmation that names the crew and asserts
    that every crew member is clear. A release without that assertion is refused and the permit
    stays `live`. In the interface the confirm control is non-interactive for 800 milliseconds
    after the confirmation opens, which is the one place in this product where a deliberate delay
    is a requirement rather than a defect.
47. A manual position override records the asserted position, a reason of 12 to 500 characters and
    a field reference identifying who verified the device in the field. It sets the element's
    effective position with quality `manual`, and until it is reconciled by a `coordinator` it
    blocks incident closure and appears in shift handover.

### Crew dispatch

48. Assigning a crew claims it. An assignment takes a lease on the crew, and a second assignment of
    the same crew while the lease holds is refused with the code `LEASE_HELD` naming the holder,
    leaving the first assignment untouched. An assignment moves through `pending_ack`,
    `acknowledged`, `en_route`, `on_site` and `cleared`, or is `recalled` or `declined`.
49. An assignment whose crew's skills do not intersect the work's required skills is refused unless
    an override reason is supplied, and the reason is recorded on the assignment.
50. A crew's estimated arrival is presented with its uncertainty. Where the routing service cannot
    answer, the distance shown is straight-line and is labelled as straight-line everywhere it
    appears, announced to assistive technology as well as shown, and never silently substituted.

### The append-only record

51. Every state-changing action writes one record entry carrying a gapless sequence number, the
    instant, the acting identity, the capability exercised, the resource kind and identifier, the
    outcome, the source address, a digest of the payload, the previous entry's hash and this
    entry's hash. An entry's hash is the digest of the previous entry's hash followed by the
    canonical form of the entry; the first entry's previous hash is sixty-four zeroes.
52. The record accepts insertions only. No role and no endpoint can edit or delete an entry, and
    the interface renders no edit or delete control in any state, including for the highest role.
53. Verification recomputes the chain over a requested window and returns the window bounds, the
    entry count, the computed root, the expected root, whether they match, and the first divergent
    sequence number when they do not. A verification window covers at most 366 days.
54. **An action that cannot be recorded does not happen.** When the record cannot be written, the
    state-changing request is refused with the code `AUDIT_UNAVAILABLE` and the state change does
    not occur. This is the strictest refusal in the product and it is deliberate.

### Shift handover

55. Opening a handover names the incoming identity and the shift end, and the server pre-assembles
    every unfinished thing: open incidents, orders that are not closed, live permits, unreconciled
    position overrides, suppressed alarms with the reason they were suppressed, and study results
    older than 30 minutes. Each pre-assembled item has a kind and a reference.
56. Every item needs an explicit disposition of `carry_forward` or `resolved` with a note of 4 to
    2000 characters. Nothing is silently dropped. Submitting while any item is undispositioned is
    refused with the code `UNDISPOSITIONED_ITEMS` listing every one of them and the handover stays
    in `composing`.
57. Accepting transfers ownership of every carried order to the incoming identity in a single act.
    A partial transfer is not possible: either every carried order moves or none does.

### The rest of the product

58. A terms page lives at `/terms` and is linked from the footer of every page, signed in or not,
    and states the conditions under which the console may be used.
59. A first-time visitor is asked once about non-essential cookies. The answer is recorded against
    that visitor and survives a reload: the choice is not offered again on the next page view or
    after refreshing.
60. Every form in the product rejects invalid input inline, names the field that is wrong and the
    reason, keeps what the user already typed, and writes nothing. A rejected submission leaves no
    row behind.
61. The public sign-in form refuses automated submission. It carries a field that a person never
    fills and that is not presented to a person; a submission arriving with that field filled is
    refused without creating a session. More than 5 submissions from the same client within 60
    seconds are also refused, and the refusal says when the next attempt is allowed.
62. An unknown address renders the product's own not-found surface, with a way back to the console,
    and answers as not found rather than as success.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Sign-in entry. Takes the email, relays the credential to the identity provider, establishes the session | public |
| `/terms` | Terms page, linked from every footer | public |
| `/console` | The operations surface: the network view plus its dock regions | signed in |
| `/console/alarms` | Alarm board, docked right | signed in |
| `/console/incidents/:reference` | Incident room, docked left | signed in |
| `/console/orders/:reference` | Switching order builder and execution, docked left | `operator`, `coordinator`, `controller` |
| `/console/dispatch` | Dispatch board, docked left | `operator`, `coordinator`, `controller` |
| `/console/telemetry` | Measurement explorer, docked bottom | signed in |
| `/study/:reference` | Study bench: the simulation parameters, its results and its violations | `operator`, `coordinator`, `controller` |
| `/console/inspect/:stableKey` | Asset inspector, floating | signed in |
| `/model` | Model manager: versions, differences, approve, publish | `coordinator`, `controller` |
| `/handover/:handoverId` | Shift handover | `operator`, `coordinator` |
| `/record` | Audit explorer: the append-only record and its verification | `controller`, `auditor` |
| `/settings` | Per-user preferences | signed in |

The view state of the network surface travels in the query string on `/console`: the camera, the
time cursor, the active layers, the current selection, the pinned model version, which panel
occupies each dock region and which elements are being inspected. Opening someone else's address
restores all of it. A shared address grants nothing: the recipient's own role and areas are
applied, elements they may not read are omitted, and the number omitted is shown.

**Permalinks.** Every alarm, incident, order, order step, study case and record entry has a
permalink of the form `/go/{objectType}/{objectId}` that resolves to the surface that shows it with
the canvas in the right state. A deep link to an object the viewer may not read renders the
permission surface naming the object type and the capability required, and reveals nothing further:
not the object's parent, not its area and not its timestamp, so the link cannot be used to confirm
that the object exists. A permalink stays stable across a model version being republished; where
the referenced element is absent from the current published version, the surface opens pinned to
the version in which it did exist and labels that state.

**Entry and redirects.** An unauthenticated request for any signed-in route goes to `/` and
returns to the originally requested address once the session exists. Sign-in lands on `/console`.
Signing out ends the session and returns to `/`. A session that expires part-way through an action
leaves the action unapplied, returns the user to `/`, and restores the surface they were on once
they sign in again. A signed-in user requesting a route their role does not permit gets the
product's own permission surface, naming the capability required, rather than a redirect or a
blank page, and it does not reveal whether the object behind the address exists.

**Journeys.**

1. *Acknowledge and open.* `operator@example.com` signs in with `deku-demo-pw-2026` and lands on
   `/console`. The alarm board shows the severity 2 protection alarm on `4B-RCL-118` at the top of
   the list. They acknowledge it, the row morphs into its acknowledged state, and the count in the
   header falls by one. They marquee-select the de-energized section on the network view and the
   outage panel reads the impact as a range between 4100 and 4700 customers with 61 on the
   sensitive register. They open `INC-4471` to severity 2.
2. *Author, study, approve, execute.* The operator opens `SWO-2026-014`. They add step 1, opening
   `NG-SEC-142`, then step 2, closing `NG-TIE-330`, by picking each device on the network view. They
   run the study. It comes back clean at a loading of `0.780` on `HS-OHL-3301`. They add a third
   step that closes `NG-SEC-142` again, re-run, and step 3 returns a `critical` thermal violation at
   `1.070`; the offending conductor is framed on the network view in its above-rating treatment.
   They delete step 3 and submit. `coordinator@example.com` opens the order, reviews each step with
   its predicted result attached, and approves; the order becomes `approved` at risk class 3 and the
   confirmation stamp marks the moment. The operator arms the execute control, reads the restatement
   of the device, the action and the predicted result, confirms, and step 1 moves to `instructed`
   and then to `confirmed` when the measurement reports `NG-SEC-142` open with quality `good`.
3. *The wrong role.* The operator calls approve on the order they just submitted. The server denies
   it. Reopening the order shows it still in `pending_approval`, with no approval recorded.
4. *Self-approval.* `coordinator@example.com` creates a new order in `Northgate` that puts 4412
   customers at risk, submits it, and calls approve. The refusal names the separation-of-duty rule
   and the order stays `pending_approval`. `controller@example.com` approves it instead.
5. *Out of area.* `operator2@example.com`, assigned to `Harbourside`, opens `SWO-2026-014` by its
   address. They can read it. Every write against it is denied with `OUT_OF_AREA` and the order is
   unchanged.
6. *Permit.* `coordinator@example.com` validates a permit over `NG-OHL-2202` with isolating devices
   `4B-RCL-118` and `NG-SEC-142`. Validation fails and names `NG-SEC-142` and its `indeterminate`
   position quality; the device is framed on the network view. The operator records a manual
   position override with a reason and a field reference. Validation re-runs and passes. `SD-2291`
   issues against crew `C-07`, the isolated section takes the permit hatch on the network view, and
   an attempt to add a step closing `4B-RCL-118` to any order is refused at that moment, naming
   `SD-2291`.
7. *The record.* `auditor@example.com` signs in, filters the record to `INC-4471` and the window,
   opens the entry that carried the manual override and reads the acting identity, the reason and
   the field reference, then runs a verification over the window and sees the computed root match
   the expected one. No edit or delete control exists anywhere on these surfaces.
8. *Handover.* The outgoing operator opens a handover to the incoming operator. Every unfinished
   item is pre-assembled. They try to submit with one item undispositioned; the refusal lists it and
   moves focus to it. They disposition it, submit, and the incoming operator accepts. The open
   order's owner is now the incoming identity.

**States.** Every list has an empty state that says what would fill it and how, and is visually
distinct from its loading state. Every loading state is laid out at the geometry of the content it
stands in for. A surface the viewer may not see is distinct from an empty one and never says "no
results" where the truth is "you may not see this". A partial list says how many rows were withheld
by permission. A stale surface says how old its data is and becomes more insistent as it ages. An
error names what failed, why, and the single next action, and never takes the application down.

## UI/UX notes

The north star: somebody arriving at this console should understand, in the first moment, the
present electrical state of the network and which part of it is under somebody's hand right now.
The honest aim here is comprehension, not atmosphere, and saying so plainly is the whole of it.

The register is operational. This is a control desk that runs around the clock in a room held at
low light, read at a glance and worked repeatedly for a twelve-hour shift. Dense but organised,
restrained, predictable, with controls that stay in the same place. No hero composition, no
editorial furniture, no decoration standing in for content.

Three stances, each of which a competing product could rationally invert. **Pattern over colour**:
every electrical state carries a distinct stroke or fill treatment and colour only reinforces it,
which costs legibility for most readers to buy it for all of them. **Density over breathing room**:
a full alarm queue and a full step list belong on one screen, and space is spent separating groups
rather than padding rows. **Stated staleness over apparent freshness**: where data is old the
surface says so, even when saying so makes the screen busier.

Because the console must support speed and repetition it needs density, large hit areas, positions
that do not move under the pointer and minimal chrome. Because it must guide at the moment of
commitment it needs one obvious next action per surface, with the restatement of what is about to
happen placed where the eye already is and everything else quieter. Because it must reassure while
a consequence is being decided, nothing moves on the surface the operator is reading while they
decide.

**Colour, by role.** Two modes, light and dark, both designed rather than one inverted from the
other, because the control room runs dark and the daytime office does not. A neutral page ground
and a slightly separated panel ground, with a third raised step for anything floating; the two
grounds must read as separate at desk distance without a drawn divider. Two border weights from the
same neutral family, low and high. Four foreground steps from the strongest for headings down
through body and secondary to disabled, and disabled is never signalled by colour alone.

Eight colours carry electrical meaning and appear nowhere else in the product: energized and within
limits, de-energized, loaded between eighty and one hundred per cent of rating, above rating, a
detected fault, under an isolation permit, a reading whose quality is not good, and a studied rather
than observed state. Energized reads as a deep, soft teal in light mode and a mid, vivid teal in
dark; de-energized as a mid cool neutral in both; loaded as a deep, vivid orange becoming a light,
vivid orange; above rating as a mid, vivid red becoming a light, vivid red; faulted as a mid, soft
violet becoming a light, soft violet; under permit as a mid, vivid blue becoming a light, vivid
blue; quality-not-good as a mid neutral in both; and studied state as the energized teal held back
in opacity. Re-using the above-rating red for a form error is prohibited. Four separate colours
carry interface status and nothing electrical: informational, taken from the accent family;
completed, a deep, soft teal becoming a mid, soft teal; attention, a deep, soft orange becoming a
light, vivid orange; and destructive or invalid, a mid, soft red becoming a light, soft red. The
focus ring is a mid, vivid blue becoming a light, vivid blue. The accent family runs four steps from
a near-white, muted blue tint through a light, soft blue and a mid, vivid blue to a deep, vivid blue
shade, mirrored in dark mode from a deep, muted blue through a mid, soft blue and a light, vivid
blue to a light, soft blue, and carries the primary action and informational emphasis and nothing
else on a surface. The exact shades are yours, so long as the three families stay mutually
distinguishable under the three common forms of colour vision deficiency and no electrical colour
leaks into an interface meaning.

**Every electrical state carries a mandatory pattern as its primary channel**, at every zoom and in
every capability tier: energized solid; de-energized a medium dash; loaded solid but visibly
heavier; above rating a tight dash, heavier again; faulted a dash-dot; under permit a diagonal
cross-hatch; quality-not-good a fine dot; and studied state a long dash. The pitch and weights are
yours; the distinctness at a glance is not.

Against defaults: no surface dominated by a single hue family with no second signal, no page that
reads as a marketing composition where a working console belongs, and nothing borrowed from a
template whose subject is not an operations surface.

**Type.** Typography here carries three roles and three personalities. An interface face with a weight axis carries every
label, heading and body line. A monospaced face with a weight axis and tabular figures carries
every numeric readout, identifier, timestamp and rule text, and every value that changes over time
uses those tabular figures, because a ticking value that reflows its neighbours is a defect. A
single-weight display face is used only for the headline index tiles on the reporting surface and
nowhere else. Each face ships a fallback tuned so that swapping fallback for real face shifts no
layout at all. The scale runs from that display size through four heading steps, a body size, a
smaller body size, a caption and a micro size, plus three monospace numeric steps, and it is fluid
between a tablet width and a wide-desktop width and clamps outside them. There is a floor below
which no size exists, and the smallest size never carries anything a user must read in order to
act. Proportions carry more than values: a heading must read as a title at a glance and body must
read comfortably at desk distance, and figures must line up in a column wherever amounts stack. The
families and the exact sizes are yours, so long as those two relationships hold.

**Space, shape and elevation.** One base spacing unit, and every gap in the product is a multiple
of it. The gap between panel sections is roughly three times the gap under a heading and about
halves on a narrow screen. Corners are barely softened, panels a shade rounder than controls, and
the only fully rounded shape in the product is the small state chip. Four elevation steps, and each
one is a border plus a shadow rather than a shadow alone, because a shadow is close to invisible on
the dark ground this console runs on. A named layer order governs stacking, from the network view
beneath, through its overlay, the dock regions, floating panels, the rails, sheets, dialogs,
transient notices and the focus trap.

**Motion.** The motion system is where most of this product's character lives, and every named
movement below composes from it. The motion character is mechanical: short, close to linear, reading as a machine
responding rather than as an interface performing. Everything animates at one speed on one curve
unless a rule below says otherwise, and nothing uses a different speed to feel special. The set of
curves is closed: a default for any property change, an accelerating one for anything leaving so it
is gone before the eye follows, a decelerating one for anything arriving so it settles where the
eye can read it, an emphasis curve with a longer tail for state changes that carry operational
consequence, a strictly linear rate for progress and anything representing a constant rate, and a
stepped, quantized curve reserved for the confirmation stamp. A non-linear progress bar
misrepresents rate and is prohibited. Overshoot and anticipation are prohibited outright, because
an operator reading a value that overshoots its target has briefly read a wrong number; spring
behaviour is therefore allowed, in a small set of named presets, for camera position, panel position, drag follow and layout
translation only, never for opacity, colour, the scale of anything bearing text, or any value the
user reads. Durations form a scale from an instant tier for hover, focus and press, through fast,
base, slow and deliberate tiers, to a camera tier, with one longer tier used only by the
confirmation stamp; nothing else in the product runs longer than the camera tier, because an
operator waiting on an animation is an operator not working. Stagger has three bands and a hard
envelope: short lists stagger noticeably, medium lists about half as much, and past roughly thirty
items the stagger becomes zero and the list arrives at once. If count times interval would exceed
the envelope the interval shrinks rather than the envelope growing. Stagger runs in reading order,
never in document order where they differ, and never radially from the pointer.

Five choreography principles govern every movement. **One thing moves**: at most one group animates position at a
time in any dock region. **Interruption always wins**: every animation is interruptible and the
interrupting state is reached from the current interpolated value, never from the original start
value, so nothing ever restarts from its beginning. **Reversal retraces the path and shortens the
time**, following the same property path on the exit curve at about three quarters of the forward
duration. **Motion never blocks input**: no control is unusable because something is animating, and
the only exception in the entire product is the deliberate delay on permit release. **Data never
animates its value**: a readout may animate its presentation, its position, its opacity or a digit
roll, but it shows the true current value at every frame, and interpolating between the old and the
new number so that intermediate frames display quantities that were never measured is prohibited.

**The reduced-motion track is a designed alternative, not a kill switch.** A blanket zero-duration override
is prohibited and an in-application preference overrides the system setting in both directions when
it is set explicitly. Translation is removed while state change is preserved, so anything that
moves through space either applies at once or is replaced by a non-spatial signal such as an
outline, a trail marker or a pulse. Short colour and opacity transitions are kept, because they are
not vestibular triggers and removing them makes state changes harder to notice, which is the
opposite of the accommodation's purpose; longer ones are removed. Continuous motion stops and the
information it carried is re-encoded statically. Safety-critical timing is never removed:
confirmation dwell periods, staleness indication and degradation indication are constraints and
indicators rather than motion, and they are unchanged. Every alternative must still carry the
information the original carried.

**Accessibility floors, which are contract rather than taste.** Body text holds at least 4.5:1
against its ground and large or heavy text at least 3:1; non-text state indicators hold at least
3:1 against every adjacent colour. Because the network view's ground varies, every overlay drawn
over it either sits on a scrim of at least 0.72 alpha or carries a hairline outline in the extreme
neutral sized to hold 3:1 against any ground. A high-contrast preference raises every foreground a
step and forces every state pattern to its heaviest weight. Every control target is at least 24 by
24 CSS pixels, and the network view's element acquisition radius does the equivalent job for
elements one to three pixels wide. Text resizes to 200% with no loss of content or function and no
text sits in a fixed-height box. Full keyboard navigation reaches every interaction including every
gesture on the network view, with a visible focus ring that holds at least 3:1 against every
adjacent colour, drawn in the overlay rather than into the rendered surface because a ring drawn
into arbitrary underlying colour cannot be guaranteed. No icon-only control ships without a label.
Meaning is never carried by colour alone. Nothing flashes more than three times a second in any
fifth of the viewport. Alternative text is present on every content image and says what the image
shows, and images that are purely decorative declare themselves decorative so they are skipped
rather than described.

**Layout and responsive behaviour.** The root surface is the network view. It stays mounted for the
whole session; changing what is shown never rebuilds it. Everything else is either a panel docked
into one of four regions over it, one at a time on the left, one on the right, one at the bottom
and up to three floating, or a full-surface workspace that covers it while leaving it mounted and
redrawing more slowly behind. Opening a second panel for an occupied region replaces the incumbent
with a cross-slide along that dock's own edge, so the direction reads as replacement rather than as
stacking. Opening a fourth floating panel closes the least recently focused. The workspace surfaces
carry a breadcrumb path back to the network view, because they are the only places a user is more
than one step from it. Responsive behaviour is a ladder of arrangements rather than a set of
breakpoints: at the widest wall and desk widths every dock may be open at once and label density is
highest; one step narrower label density drops and the left and right docks become mutually
exclusive once the rendered element count is high; at laptop width the docks become mutually
exclusive outright and the post-processing chain reduces; at tablet width docks become full-width
sheets over the network view; and at phone width the network view still renders but redraws on
demand rather than continuously, which is a battery and thermal requirement rather than a
capability one, marquee and lasso give way to tap-to-select, labels reduce to a handful, presence
is hidden, split views become sequential sections and drag-to-assign becomes an explicit assign
action. The layout holds at every width in between, nothing overflows sideways at the smallest
supported viewport, and every navigation target stays reachable there. Charts that cannot compress
without becoming illegible degrade to a summary line plus a text summary rather than squeezing
their axes into nonsense, and every chart and every grid has a real table alternative reachable
from the keyboard. Where the choice is yours, it is yours, so long as the ladder holds at every
width and nothing above loses a state.

**One primary action per surface.** Each surface leads with a single clear primary action, visually
distinct from every secondary one, wearing the strongest contrast in the interface; everything else
is quieter.

## Technical requirements

Frontend: **SolidJS** compiled by **Vite** into a production bundle, a single-page client that
renders every surface in the browser and talks to a JSON API on the same origin. Backend:
**Express** on **Node 20** in TypeScript, serving both the built client and the API from one
process. Datastore: **PostgreSQL**, reached at `DATABASE_URL`. Identity provider: **Keycloak**,
reached at `AUTH_URL`. The browser receives a static shell and the client paints every surface,
which is the right trade here because the network view's content is a binary geometry payload and
a live stream rather than markup, and every route sits behind a sign-in where there is no crawler
and no cold-start indexing to serve.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing services
available in this environment are **PostgreSQL** and **Keycloak**, and reaching for anything else
is a contract violation.

**Identity.** Sign-in is single sign-on against the identity provider over OIDC: the provider
holds the account and validates the credential, and this product holds neither.
The realm is named by `AUTH_REALM` and the confidential client the app authenticates
as is named by `AUTH_CLIENT_ID` with its secret in `AUTH_CLIENT_SECRET`. The app relays the
submitted credential to the identity provider at `AUTH_URL`, receives tokens on success, reads the
subject, the email, the display name and the realm roles from them, and issues its own session
cookie. The app stores no password and creates no account: an email with no account in the realm
cannot sign in and cannot be created from inside the product. The realm's roles are `operator`,
`coordinator`, `controller` and `auditor`, and the assigned operating areas are carried as an
account attribute. Read every one of those values from the environment; never hardcode a host, a
realm name or a client identifier.

**Health.** `GET /api/health` returns `200` once the app holds a database connection and can reach
the identity provider's discovery document. It answers before any session exists.

**Logging.** One structured JSON object per line, carrying a timestamp, a level, a stable event
name, a correlation identifier for the request and the acting subject where one exists. A log line
without an event name is not acceptable. Log lines carry no measurement value, no incident body, no
override reason, no policy text, no personal identifier beyond an opaque one, and no secret.

**Real-time updates and collaboration.** Several operators work one event together, so the console
is collaborative by default rather than by a shared-editing feature bolted on: one real-time
transport, one stream per signed-in session, carries alarm, incident, order, permit and dispatch
events plus a measurement frame, so a change one signed-in user makes appears on another user's
open surface without a reload. Frames are coalesced so that only the latest value per point
is delivered; a backlog of superseded values is never replayed, because the operator needs the
present rather than a history. One stream per session, not one per panel.

**Determinism of the study.** The study engine is deterministic. The same order, the same pinned model version and the same
base-state instant must produce identical study results on every run, including the per-conductor
loading to three decimal places and the set of violations. A result always carries the model
version and the base-state instant it was computed against, rendered next to the result rather than
only in a details panel, because a result read without knowing what it was computed against is
worse than no result.

**Idempotency and concurrency, stated as properties of the running system.** Two simultaneous
executions of one switching step leave exactly one execution attempt, one emitted instruction and
one record entry, and both callers receive the same body. Two simultaneous approvals of one order
leave exactly one approval record and the loser is told who won. Two simultaneous acknowledgements
of one alarm leave exactly one acknowledgement and the loser is told who won. Two simultaneous
assignments of one crew leave exactly one assignment and the loser is told who holds it. In every
case the losing request changes nothing and leaves no partial state behind: no orphaned row, no
step left `instructed` with no attempt, no crew left leased to nobody.

**Reads and paging.** Every list endpoint pages by an opaque cursor, defaulting to 50 items and
capped at 200. A response that omits rows the caller may not read says how many were omitted rather
than silently under-reporting.

**Internationalization.** Every interface string is externalized and no string literal lives in a
component. Dates, times and numbers format per the viewer's locale, with the operational time zone
always shown and coordinated universal time shown on any surface that becomes evidence. Units of
measurement are not localized: a voltage is kV in every locale, because localizing an electrical
unit would create exactly the class of error this product exists to prevent. Device designations,
element identifiers, order references and record content are never translated. Sentences are never
assembled by concatenation, plural forms follow the locale's own rules, and the layout tolerates a
string growing by two-fifths without truncating or overflowing. Text direction is left to right at
launch, and the layout uses direction-agnostic properties throughout so that adding the other
direction later is a translation task rather than a re-layout.

**Privacy and governance.** Personal data lives in exactly three places and no others: the account
records of the utility's own staff, the crew member records, and the sensitive-customer register.
The register is the most restricted data in the product: it is stored apart from the impact
snapshot that counts it, read only through a capability-gated endpoint, audited on every read by
count rather than by identity, and never joined into any other response. Presence is ephemeral and
is never persisted, so the platform builds no record of where an operator looked or when they were
at their desk, and that absence is a designed property rather than an oversight. Nothing in this
product is a compliance control in itself; what it provides is the record from which a customer's
own compliance evidence is drawn.

**No secrets reach the browser.** No credential, client secret, admin token or connection string
appears in any file the browser downloads, in any response body, or in any client-side bundle.

**Security headers.** Every response carries the standard set, including a strict transport policy
and a content-type policy that refuses sniffing.

## Data model

Twenty-eight tables. All timestamps are UTC, and calendar-day logic uses the server's UTC day.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

`operating_area`: `id`, `name`, `slug`. `name` is unique.

`model_version`: `id`, `train` (integer, unique, increasing), `state` (`importing`, `ready`,
`pending_approval`, `published`, `superseded`), `element_count`, `approved_by`, `approved_at`,
`published_by`, `published_at`, `superseded_by_id`. At most one row is `published` at any instant.

`network_element`: `id`, `model_version_id`, `stable_key`, `element_class`, `name`,
`operating_area_id`, `feeder`, `phases`, `nominal_voltage_v`, `rating_a`, `section_load_a`,
`stratum`, `normally_open`, `instance_index`. `stable_key` is unique within a model version and is
what survives across versions, so an address to an element still resolves after a republish.
`element_class` is one of `substation`, `busbar`, `transformer`, `conductor_overhead`,
`conductor_underground`, `switch_disconnector`, `switch_load_break`, `circuit_breaker`, `recloser`,
`sectionalizer`, `fuse`, `service_point`. `stratum` is one of `underground`, `surface`,
`overhead_lv`, `overhead_hv`. `rating_a` is required on every conductor class and absent elsewhere.

`connectivity_edge`: `id`, `model_version_id`, `from_element_id`, `to_element_id`, `normally_open`.
The edges of a version form the graph that decides what is energized from where, which supply path
a conductor sits on, and how many connections away one element is from another. Tracing that graph
outward from a source, and tracing it downward from a device to the service points it feeds, is
what every energization answer in the product is derived from.

`measurement_point`: `id`, `element_id`, `stable_key`, `quantity` (`voltage`, `current`,
`active_power`, `switch_position`, `frequency`, `temperature`), `unit`, `expected_period_s`.

`measurement_sample`: `id`, `point_id`, `observed_at`, `received_at`, `value`, `quality` (`good`,
`suspect`, `stale`, `indeterminate`, `manual`, `estimated`), `source`. Quality is required. The
latest sample per point is what the console reads as current, and its age against
`expected_period_s` is what decides whether the point is marked stale.

`alarm_rule`: `id`, `name`, `point_stable_key`, `condition`, `threshold`, `severity`, `enabled`.

`alarm`: `id`, `rule_id`, `point_id`, `element_id`, `raised_at`, `cleared_at`, `acknowledged_at`,
`acknowledged_by`, `state` (`active`, `acknowledged`, `cleared`, `suppressed`), `severity`,
`computed_priority`, `classification`, `incident_id`, `suppression_reason`, `suppressed_until`.
`computed_priority` is derived on read-through from severity, customers at risk, permit coverage
and incident binding, never stored from a client value.

`incident`: `id`, `reference`, `severity`, `state` (`open`, `commanded`, `closing`, `closed`),
`commander_id`, `command_version`, `opened_at`, `opened_by`, `closed_at`, `closed_by`,
`closure_summary`, `model_version_id`. `reference` is unique.

`incident_timeline_entry`: `id`, `incident_id`, `sequence`, `occurred_at`, `kind` (`note`,
`system`, `artefact`, `command_change`, `severity_change`), `author_id`, `body`. `sequence` is
assigned by the server and is gapless within an incident.

`incident_member`: `incident_id`, `user_id`, `role_in_incident`, `joined_at`, `left_at`.

`outage_event`: `id`, `incident_id`, `began_at`, `restored_at`, `cause_code`,
`de_energized_element_ids`, `estimated_restoration_at`, `etr_revision_count`.

`customer_impact_snapshot`: `id`, `outage_event_id`, `captured_at`, `customers_affected_min`,
`customers_affected_max`, `sensitive_customers_count`, `customer_minutes`, `estimated_cost_minor`,
`currency`, `resolution_state` (`estimating`, `resolved`). The affected count stays a minimum and a
maximum while `resolution_state` is `estimating`. `customer_minutes` is derived on read from the
de-energized set and the elapsed time, not stored.

`switching_order`: `id`, `reference`, `incident_id`, `model_version_id`, `operating_area_id`,
`state` (`draft`, `validating`, `validated`, `pending_approval`, `approved`, `executing`,
`suspended`, `completed`, `aborted`), `risk_class` (1 to 4), `step_sequence_hash`, `approved_hash`,
`created_by`, `owner_id`, `current_step_index`, `suspended_reason`, `abort_reason`. `reference` is
unique. An order in `approved`, `executing` or `completed` always has `approved_hash` equal to
`step_sequence_hash`; there is no state of the system in which it does not. `risk_class` is derived
on the server from the customers at risk and whether the sequence creates a parallel path.

`switching_step`: `id`, `order_id`, `ordinal`, `element_id`, `element_stable_key`, `action`,
`state` (`pending`, `instructed`, `acknowledged`, `confirming`, `confirmed`, `failed`, `skipped`),
`predicted_result`, `study_case_id`, `idempotency_key`. Ordinals are dense and contiguous within an
order. `idempotency_key` is written when the step is created and is what makes a second execution
of the same step a no-op that returns the first one's outcome.

`step_execution_attempt`: `id`, `step_id`, `attempt_no`, `instructed_at`, `acknowledged_at`,
`confirmed_at`, `failed_at`, `failure_reason`, `instruction_signature`. One attempt per successful
execution of a step and no more.

`approval_record`: `id`, `order_id`, `approver_id`, `approved_hash`, `decision` (`approve`,
`reject`), `decided_at`, `comment`, `risk_class_at_decision`. One approval per approver per hash.

`study_run`: `id`, `order_id`, `model_version_id`, `base_state_at`, `state`, `case_count`,
`cases_completed`, `started_at`, `completed_at`.

`study_case`: `id`, `study_run_id`, `case_index`, `step_ordinal`, `converged`, `max_loading_pu`,
`min_voltage_pu`, `customers_de_energized`. A case that does not converge is a result and not a
failure, and the run is not marked failed because of it.

`violation`: `id`, `study_case_id`, `element_id`, `kind` (`thermal`, `overvoltage`,
`undervoltage`, `reverse_power`), `severity` (`warning`, `critical`), `value`, `limit_value`.

`safety_document`: `id`, `reference`, `order_id`, `crew_id`, `isolated_element_ids`,
`isolating_device_ids`, `state` (`validating`, `live`, `released`, `revoked`), `issued_at`,
`issued_by`, `released_at`, `released_by`, `release_confirmation`, `validation_evidence`.
`reference` is unique. `validation_evidence` holds the value, the quality and the `observed_at`
instant of every isolating device as of the validation that permitted the issue, which is what
makes an issue provable afterwards.

`position_override`: `id`, `element_id`, `asserted_position`, `reason`, `field_reference`,
`asserted_by`, `asserted_at`, `reconciled_at`, `reconciled_by`, `incident_id`. An override whose
`reconciled_at` is null blocks its incident from closing and appears in handover pre-assembly.

`crew`: `id`, `call_sign`, `skills`, `availability` (`available`, `assigned`, `en_route`,
`on_site`, `unavailable`, `off_shift`), `base_area_id`, `lease_holder_id`, `lease_expires_at`.
`call_sign` is unique. A crew with a live lease cannot be claimed by a second assignment.

`dispatch_assignment`: `id`, `crew_id`, `incident_id`, `target_element_id`, `state`
(`pending_ack`, `acknowledged`, `en_route`, `on_site`, `cleared`, `recalled`, `declined`),
`assigned_at`, `assigned_by`, `acknowledged_at`, `safety_document_id`, `skill_override_reason`,
`routed_eta_at`, `routed_eta_uncertainty_s`, `eta_is_straight_line`.

`handover`: `id`, `outgoing_user_id`, `incoming_user_id`, `shift_ends_at`, `state` (`assembling`,
`composing`, `submitted`, `accepted`, `expired`), `submitted_at`, `accepted_at`. Exactly one
outgoing and one incoming identity, and they differ.

`handover_item`: `id`, `handover_id`, `kind` (`incident`, `order`, `safety_document`, `override`,
`suppressed_alarm`, `stale_study`), `ref_id`, `disposition` (`carry_forward`, `resolved`, or null),
`note`, `view_state`. A handover cannot leave `composing` while any of its items has a null
`disposition`.

`audit_event`: `id`, `sequence`, `occurred_at`, `actor_id`, `capability`, `resource_kind`,
`resource_id`, `outcome`, `source_ip`, `payload_digest`, `prev_hash`, `entry_hash`. `sequence` is
gapless across the deployment. The only operation this table ever undergoes is an insertion; no
endpoint, no role and no path updates or deletes a row, and a gap in the sequence is a detectable
tamper indication rather than a tidying opportunity.

`app_user`: `id`, `subject_id`, `email`, `display_name`, `role`, `assigned_area_ids`, `status`,
`last_seen_at`. `email` is unique. `subject_id` is the identity provider's subject and is what a
session is resolved through.

`page_view`: `id`, `route`, `viewed_at`, `user_id`.

`cookie_choice`: `id`, `visitor_token`, `non_essential_accepted`, `decided_at`. `visitor_token` is
unique, and the recorded choice is what stops the question being asked a second time.

**Seed data.**

Two operating areas, `Northgate` and `Harbourside`.

Two model versions: train `418` in state `published`, which owns every seeded element, and train
`419` in state `ready`.

Twelve elements in train `418`:

| `stable_key` | `element_class` | Area | Detail |
|---|---|---|---|
| `NG-SUB-01` | `substation` | `Northgate` | Northgate Primary |
| `NG-BUS-11` | `busbar` | `Northgate` | nominal 11000 V |
| `NG-CB-101` | `circuit_breaker` | `Northgate` | feeder head, closed |
| `NG-OHL-2201` | `conductor_overhead` | `Northgate` | rating `220` A, section load `92.0` A |
| `4B-RCL-118` | `recloser` | `Northgate` | mid-feeder, tripped open |
| `NG-OHL-2202` | `conductor_overhead` | `Northgate` | rating `180` A, section load `58.0` A, 2840 customers |
| `NG-SEC-142` | `sectionalizer` | `Northgate` | closed, position quality `indeterminate` |
| `NG-OHL-2203` | `conductor_overhead` | `Northgate` | rating `160` A, section load `38.0` A, 1572 customers |
| `NG-TIE-330` | `switch_load_break` | `Northgate` | tie to Harbourside, normally open |
| `HS-SUB-02` | `substation` | `Harbourside` | Harbourside Primary |
| `HS-CB-201` | `circuit_breaker` | `Harbourside` | closed |
| `HS-OHL-3301` | `conductor_overhead` | `Harbourside` | rating `200` A, section load `118.0` A |

Connectivity runs `NG-SUB-01` to `NG-BUS-11` to `NG-CB-101` to `NG-OHL-2201` to `4B-RCL-118` to
`NG-OHL-2202` to `NG-SEC-142` to `NG-OHL-2203` to `NG-TIE-330`, and `HS-SUB-02` to `HS-CB-201` to
`HS-OHL-3301` to `NG-TIE-330`. `NG-TIE-330` is normally open, so the two feeders are separate
until it closes.

Latest measurements: `NG-OHL-2201` at `92.0` A quality `good`; `NG-OHL-2202` and `NG-OHL-2203` at
`0.0` A quality `good`, because `4B-RCL-118` is open; `HS-OHL-3301` at `118.0` A quality `good`;
`NG-BUS-11` at `11200` V quality `good`; `4B-RCL-118` switch position `open` quality `good`;
`NG-CB-101`, `HS-CB-201` and `NG-TIE-330` at their seeded positions with quality `good`; and
`NG-SEC-142` switch position `closed` with quality `indeterminate`, which is the reading that makes
the first permit validation fail and name that device.

One alarm, active and unacknowledged: severity 2, named `Protection operation on 4B-RCL-118`,
raised against the recloser's own point, with 4412 customers at risk, giving `computed_priority`
`34412`.

One incident, `INC-4471`, severity 2, state `open`, opened by `operator@example.com`, with the
alarm bound to it and no commander. Its outage carries the impact snapshot in rule 23.

One switching order, `SWO-2026-014`, state `draft`, pinned to train `418`, area `Northgate`, owner
`operator@example.com`, no steps.

Two crews: `C-07`, available, based in `Northgate`, with skills `switching` and `lv-jointing`; and
`C-12`, available, based in `Harbourside`, with skill `switching`. The permit reference the seeded
scenario issues is `SD-2291`.

Five accounts, exactly the table in `## User roles`, each present both in the identity provider's
realm with the corpus password and as an `app_user` row carrying its role and assigned areas.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual and interaction detail that will not fit in `## UI/UX notes`. It
adds nothing that contradicts it.

**Render-loop orchestration.** One loop at the root of the application drives everything: camera
integration, the canvas redraw, the overlay reconciliation, chart drawing and every interface
animation. There is no second loop anywhere. Its order within a frame is fixed, and layout is read
in one batch before anything is written, never interleaved with writes.

**The network view is one persistent surface.** It mounts once for the session and is never
unmounted. A change of route, a dock opening, a workspace covering it, a selection changing, a
measurement arriving: none of these rebuilds it and none of them re-uploads its geometry. Static
topology is uploaded once per model version. Live electrical state lives in a state buffer that is
rewritten as measurements arrive, and changing what the operator sees means changing the contents
of that buffer, not the structure of the scene. A frame that changes six thousand elements costs
the same structural work as a frame that changes one. A workspace covering the surface reduces how
often it redraws but never releases its resources.

**Level of detail.** At the widest zoom conductors collapse to one line per feeder and only
protective devices draw. Zooming in brings full conductors at hairline width with devices as small
glyphs, then width-scaled conductors with full device symbols, then phase separation, drawing one
conductor per phase where the model has more than one. A band change cross-fades between the two
bands rather than popping, and a band change during a cross-fade continues from the mix currently
on screen. Camera motion never waits for a band change.

**Depth strata.** Underground cable, surface plant, overhead low voltage and overhead high voltage
separate in depth as the operator zooms in, so co-located plant at different levels is
distinguishable without a legend, and they collapse to one plane when zoomed out far enough that
the separation would exceed the positional error of the geometry. The threshold carries a
hysteresis band so that jitter around it cannot cause repeated transitions.

**Pointer work on a surface of one-pixel objects.** The pointer acquires the nearest element within
a small radius rather than requiring a hit, and the acquired element's hit target visibly leans
toward the pointer so the attraction is legible. A tooltip waits for a brief hover intent and is
cancelled by any further movement. The cursor over the surface says what the current position will
do before the operator commits: select, pan, marquee, add to order, inspect, or not permitted. It
never replaces the native cursor over a control, a text field or a scrollable region, and it does
not exist at all for touch input. Dragging on empty space draws a selection region with a live
count; dragging past the viewport edge pans at a rate proportional to how far past the edge the
pointer has gone; Escape cancels the drag and restores the previous selection.

**Named movements the product must have.** Each is described by what happens rather than by how it
is built.

- *State write.* When measurements change the electrical state of many elements at once they all
  change together in one frame, because they changed together in the world. Staggering a physical
  simultaneity misrepresents it. The previous state cross-fades briefly into the new one, and a
  second change arriving mid-fade continues from the colour currently on screen rather than
  queueing or restarting.
- *Fault propagation.* When a protective device operates, a pulse travels outward from that device
  along the electrical graph at a rate set by how many connections away each element is rather than
  by how far away it is on screen, so the operator reads the electrical extent of the outage rather
  than a geographic ripple. It rises quickly, holds while the front travels, and falls away. At
  most three run at once, and a fourth replaces the oldest by overlapping it rather than queueing.
- *Selection halo and permit hatch.* A selection is outlined as one continuous shape around a set
  of thin, disconnected geometry. The isolation-permit cross-hatch drifts slowly and continuously
  along its own diagonal; this is the only continuously moving decoration permitted on the network
  view, and it is permitted only because a static hatch at low zoom breaks into an unreadable
  shimmer and motion resolves it.
- *Live against studied.* Entering study mode does not swap what is drawn. Live and studied state
  are drawn together and mixed with the live layer dimmed, so the difference is directly visible
  rather than remembered from the previous screen. Unchanged elements desaturate while changed
  elements keep full chroma and gain a hairline outline.
- *Camera.* Every camera move in the product is one interpolation over position, zoom, bearing and
  pitch, and a long move arcs outward in zoom, travels, and comes back in rather than sliding at
  constant zoom. Exactly one camera animation runs at a time; a new target replaces the current one
  and keeps its velocity, so a retarget in flight is continuous rather than a restart. Any pan,
  zoom or drag by the operator cancels it instantly with no decay ramp, because a camera that
  fights the operator is a defect.
- *Pan inertia and edge resistance.* Pan momentum decays to a stop. Panning past the network's
  boundary is resisted with increasing firmness and released with a snap. A new grab during
  momentum arrests the surface immediately with no residual drift.
- *Crew marker.* A crew's position arrives at long intervals. The marker advances along the route
  the crew is actually following rather than along a straight line, and carries a visibly distinct
  trail for the inferred portion of its path, so a dispatcher can always tell a reported position
  from an inferred one. A report landing far from the inferred position jumps the marker rather
  than travelling to it, because travelling would draw a path the crew did not take, and the jump
  is marked with a brief attention ring.
- *Route travel.* A crew's route is a dashed line whose dashes travel in the direction of travel at
  a rate proportional to the crew's estimated ground speed, which gives direction without
  arrowheads, illegible at these widths, and speed without a label.
- *Shared-element promotion.* Opening an element's inspector lifts the element's own symbol from
  the network view into the inspector header along a direct path, so the operator's eye keeps hold
  of the object instead of re-acquiring it. The panel begins arriving before the symbol starts
  moving, so the destination exists before the traveller gets there.
- *Address restoration.* Arriving at an address carrying view state does not cut to it. Layers
  cross-fade while the camera flies, the selection outline lands as the camera settles, and the
  docks open last. Any input from the operator cancels the remainder at once and applies every
  uncompleted stage immediately, so the address is still honoured.
- *Value ticker.* In a changing readout only the digits that changed slide within their own
  fixed-width cells; unchanged digits do not move; direction follows the change; and a carry that
  changes several digits moves them together.
- *Priority roll.* When an alarm's rank changes the rank numeral rolls through the intervening
  whole numbers rather than jumping, capped so the roll never outlasts the row's own travel, and
  always landing on the true value.
- *Ordinal set.* Switching-order step numbers are revealed glyph by glyph behind a wipe when a step
  is added, and renumber together when steps are inserted, deleted or reordered, so a renumber
  reads as "these steps changed number" rather than as a silent mutation.
- *Confirmation stamp.* Four moments are irreversible commitments: approving an order, issuing a
  permit, publishing a model version and reconciling a position override. Each is marked by a stamp
  revealed in discrete steps rather than smoothly, which reads as mechanical and consequential
  rather than as polish. It is the only quantized motion in the product, it runs only on server
  confirmation and never optimistically, and it is the one animation that may not be interrupted.
- *Step execution timeline.* Each executing step shows its phases in sequence, instruction emitted,
  acknowledged, awaiting confirmation, confirmed, with the elapsed time in each growing live, so a
  slow step reveals where it is slow. Past one threshold the running segment takes the attention
  tone and past a second the destructive tone, and the manual confirmation path appears.
  Suspension freezes the segment and hatches it; resuming continues from the frozen value with the
  elapsed time accounted rather than reset.
- *Progress rings.* Long operations show determinate progress against real units, cases or objects
  or chunks, with an estimated completion derived from observed throughput. An indeterminate state
  is visually distinct rather than a spinning determinate ring and is never used where a
  determinate count is obtainable. Progress never animates backward: a revised-down estimate holds
  position and revises the text instead. Cancellation stops the ring where it stands and marks it
  rather than resetting it to zero.
- *Progressive matrix fill.* Study result grids fill cell by cell as cases complete.
  Not-yet-computed cells carry a stipple and computed-clean cells a flat fill, so an incomplete run
  can never be read as a clean one. The fill follows completion order, not row order, and the grid
  is not reordered to look tidy.
- *Streaming strip chart.* A live series scrolls at a constant rate driven by the wall clock rather
  than by frame count, so its rate is the same on every machine. Brushing freezes it instantly;
  returning to live catches up at a bounded rate and, where catching up would take longer than that
  bound, jumps and says that it jumped.
- *Loading heat.* Conductor loading renders as a continuous field along the conductor with hard
  edges exactly at the two thresholds that matter, so the thresholds read as edges rather than as
  gradients.
- *Brushing and linking.* A brush on any time-based surface re-times every other surface. There is
  exactly one time cursor in the application, and subscribers apply the new window on the frame
  they receive it rather than each animating their own re-time.
- *Plot crosshair.* Moving over the measurement plot places a crosshair, reads out every visible
  series at that instant, and projects a ghost time cursor onto the network view, so hovering a
  chart previews a network state without committing to it. The readout snaps to the nearest real
  sample and never interpolates between samples.
- *Alarm ingress.* A single strip above the alarm list shows arrivals per short bucket, so an
  operator can tell one alarm from the beginning of a storm without reading the list. A bucket that
  rolls over mid-growth finishes growing at double rate rather than being truncated.
- *Routed estimate.* A crew's estimated arrival renders as a bar with a visibly distinct hatched
  extension for routing uncertainty, so a point estimate is never read as a promise.
- *Impact counters.* Large counts change by a coordinated digit roll plus a magnitude bar, never by
  numeric interpolation. Where the figure is a range the counter renders the range in words, never
  a midpoint, and never animates as though converging on one.
- *Chain integrity strip.* A strip above the record stream shows one mark per block of entries in
  the queried window, coloured by verification status, so a break is visible as a position rather
  than reported as a sentence. A failing mark outlines itself and the outline never fades.
- *Reconnect progress.* Losing and regaining the live stream is shown as a determinate sequence,
  detecting, waiting with the remaining delay counting down, connecting, authenticating, catching
  up with a frame count, rather than as an indeterminate spinner, because the operator needs to
  know whether to wait or to act.
- *Staleness and backfill.* Any surface whose data is older than its freshness contract shows an
  age indicator that becomes more prominent as the data ages, stepping through the informational,
  attention and destructive tones. This indicator is never suppressed by any capability tier, by
  reduced motion, or by any user preference: it is how an operator knows the screen is lying to
  them.
- *Row state morph.* A row changing state morphs in place. Its state chip cross-fades, its
  background transitions, its available actions swap, and its height changes only when the new
  state needs more room. An optimistic state the server later refuses plays the reverse and then
  plays forward into the true state, so the operator sees the revert happen rather than a silent
  correction.
- *Reflow on sort.* When a list re-orders, rows travel to their new positions rather than
  teleporting, so a specific row can be tracked through the re-sort. A hard cap limits how many
  rows animate; rows beyond the cap, chosen by distance travelled, take their new position
  instantly. That cap is a requirement, not a heuristic.
- *Insert without displacement.* Append-only streams insert without displacing what the operator is
  reading. At the live edge new items push and the scroll follows; away from the edge they
  accumulate behind a count badge instead. An insertion never moves content that is under the
  pointer or that contains focus.
- *Hierarchy expansion.* Approval trails, grant chains and the organisation tree expand with their
  children arriving and their connector lines drawing themselves, so the structure is legible as it
  appears.
- *Confirm-step expansion.* The confirming control expands in place to reveal its restatement rather
  than opening a dialog, so the pointer does not travel and the eye does not leave the object being
  acted on. Collapsing it never commits the action.
- *Degradation band.* A band in the status rail names exactly which capabilities are unavailable and
  why. Several concurrent degradations render as one band with a list, never as stacked bands. It
  occupies reserved space so its appearance never reflows the network view.
- *Degraded palette.* While the product is degraded the surrounding chrome desaturates slightly so
  peripheral vision registers the condition before the band is read, and the desaturation never
  takes any text or indicator below its contrast floor.
- *Theme and severity transition.* Changing theme, or an incident changing severity, transitions the
  palette rather than swapping it, and the network view and the interface transition together on one
  timeline so nothing disagrees mid-change.
- *Alarm contrast lift.* While an unacknowledged alarm of the top two severities is active the
  interface raises foreground contrast one step and thickens every state pattern, so the console
  becomes measurably more legible under load rather than merely showing something red. It releases
  more slowly than it engages so that rapid acknowledgement cycles do not make the console flicker.
- *Determinate load.* The first load names its phases in order rather than showing a percentage:
  attribute table, geometry, shaders, first state frame. Each phase completes before the next
  appears, and a failure in one phase halts and offers a retry of that phase alone rather than a
  full restart. The network view becomes pannable as soon as any geometry has arrived; a blocking
  full-screen loader over it is prohibited.
- *Skeleton morph.* Placeholders are laid out at the exact geometry of the content they stand in for
  and turn into that content in place rather than cross-fading between two differently shaped
  things. They do not appear at all for operations expected to finish almost immediately; below that
  threshold the region holds its previous content.
- *Presence.* Other signed-in users appear as cursors on the network view, interpolated between
  their reports and briefly extrapolated, with an explicit decay so a stopped cursor visibly stops
  rather than drifting. Their selections render beneath the local selection so the local one always
  reads as primary. Members joining and leaving a room animate in and out of the presence strip
  without displacing the header around them. Authority transfer moves a badge from the previous
  holder's avatar to the new holder's along a direct path, so every observer sees where authority
  went rather than reading that it changed; the badge always arrives, and the capability change
  never waits for the animation.

**Scroll is a value input here, not a storytelling device.** This product has no narrative to
scroll through. Three surfaces are scroll-driven and each one treats the scroll position as a
value: the model version timeline pins above the change list and its marker tracks the scroll
position through the version's change density; the time cursor scrubs the whole application, so
dragging it re-times the canvas, every chart, every panel and the presence layer together; and the
record replay transport plays reconstructed network state forward while the record stream scrolls
in lockstep, where the scroll position and the playhead are one value in two representations and
either may drive the other. A scroll-linked value tracks the input exactly and is never eased,
because easing a scroll is lag. A programmatic scroll is cancelled by any user scroll inside it.

**The eight state patterns are generative rather than tiled.** Each is a procedural function of the
element's state and its position on screen, so every pattern keeps exactly its intended pitch at
every zoom level and every pixel density instead of breaking up into a moire as a repeated image
would. The edges are resolved analytically rather than by drawing the pattern larger and shrinking
it.

**Theming and ambient response.** The palette transitions rather than swapping, so every consumer
of a colour moves together and no component needs to know a transition is happening. Three things
drive it: the light and dark preference, an incident changing severity, and the product entering or
leaving a degraded state. The canvas reads the same colour values the interface does, from one
source, so the two can never disagree about what energized looks like.

**How reduced motion re-encodes each of those.** The travelling dash becomes a taper from short
dashes at the origin to long ones at the destination. The drifting permit hatch becomes a wider
static pitch that does not shimmer. Interpolated presence cursors become discrete positions plus a
short trail marking the previous one. The fault pulse becomes a single static outline over the whole
affected section, which preserves the extent and removes only the travel. A re-sort applies
positions instantly and the previously focused row takes a temporary focus outline at its new place
so it can still be tracked. The camera still moves rather than cutting, because a cut loses the
spatial relationship between where the view was and where it was sent, but the zoom arc is removed
because the arc is the part that induces the sensation. Authority transfer sets the badge at the
destination and pulses an outline on both avatars. The confirmation stamp renders fully formed and
still holds its moment.

**Capability tiers.** Three tiers, computed once at session start and re-evaluated on defined
signals: whether an accelerated drawing surface exists at all, the device's reported memory and
core count, the effective connection class, a data-saver preference, battery level while
discharging, viewport width, and the session's own sustained frame time. The tier is the minimum
any single signal permits, so one failing signal demotes. Demotion is prompt; promotion requires
the qualifying signal to hold continuously for far longer, so the tier cannot oscillate. Every tier
change appears in the status rail with the specific signal named. What changes between tiers: the
element cap, the number of detail bands, the number of post-processing passes, how often
measurements are applied, whether the render loop is continuous or on demand, how many presence
cursors and remote selections render, how many rows animate on a re-sort, how many chart series
stream and how fast, whether the pointer carries a custom cursor, whether lasso as well as marquee
is offered, the frame cache size and the texture memory ceiling. What never changes at any tier:
state pattern rendering, staleness indication, degradation indication, confirmation dwell periods,
focus visibility, and the screen-reader mirror of the network view's content. **Every functional
capability is available at the lowest tier.** Tiers change performance and richness, never what the
operator can accomplish: an operator on the plainest tier can still execute a switching order.

**The screen-reader treatment of the network view.** The surface mirrors its content to an
off-screen but screen-reader-visible tree describing the current viewport: element counts by class,
an energization summary, active alarms by severity, and the focused element's full state. It
updates at a bounded rate so it cannot flood, and it announces politely. Arrow keys traverse the
network by electrical connectivity rather than by screen position, and the traversal order is
deterministic and derived from the model, so two operators traversing the same network reach
elements in the same order. Bracket keys move between siblings on a bus, Enter selects, Escape
exits. Every gesture has a keyboard equivalent: marquee selection becomes extend-along-connectivity,
and follow mode has its own shortcut. Predicted results are available as text and not only as a
drawing. Announcements are rate-limited and coalesced, and assertive announcement is reserved for
three things only: a change in who holds authority, a verification failure, and a blocking refusal.
Typing indicators never announce.

**Components, by their states.** Every one of these has every state implemented; a component
missing a state is incomplete. A button in primary, secondary, quiet and destructive variants, each
with resting, pointed-at, focused, pressed, loading, unavailable and just-succeeded states. A
confirm control, which is the only permitted control for any action that changes the electrical
network, issues or releases a permit, or publishes a model version, with resting, armed, dwelling,
confirming, confirmed and cancelled states, restating the object and the consequence in its second
stage. An icon button that always carries a label. A chip, and a state chip with one appearance per
electrical state plus transitioning and quality-unknown. A field in text, number, select,
multi-line, duration, timestamp and coordinate variants with resting, focused, filled, invalid,
disabled, read-only and validating states. A table and a virtual list in dense and comfortable
densities with loading, populated, empty, filtered-empty, partial and error states, where partial
means rows were withheld by permission and says how many. A panel and a sheet with opening, open,
resizing, closing and replaced states. A dialog in default, destructive and blocking variants with
focus trapped while open. A toast and a banner, the banner adding a degraded variant. Tabs, an
accordion, a tooltip and a popover. A counter in single, range and delta variants with idle,
updating, provisional and unavailable states, and a ticker in elapsed, countdown and age variants.
A progress ring and a progress bar, determinate and indeterminate, with idle, running, complete,
failed and cancelled states. A strip chart, a sparkline and a matrix. A presence avatar and a
cursor label. An empty state in five distinct kinds, no data, no results, not permitted, error and
first run, each visually and textually distinct, because rendering "no results" where the truth is
"you may not see this" is a security defect rather than a copy defect. A skeleton block in text,
row, chart and panel shapes. Escape closes the topmost transient surface, destructive actions
confirm first, and every control reachable by pointer is reachable by keyboard in a sensible order
with a visible ring.

**Iconography.** One stroked set at a single stroke weight on one grid, drawn inline so it inherits
the current text colour. Icon fonts are not used. Every icon has a text label or an accessible name,
and an icon-only control's tooltip carries the same string as its accessible name. Electrical device
symbols follow the recognised international convention for electrical diagrams and are not restyled
for visual consistency with the interface icon set: they are the operator's professional vocabulary,
not decoration. No icon is the sole carrier of state; state is carried by pattern and text, and the
icon identifies the object rather than its condition.

**Voice and copy.** Second person for instructions to the current user, third person for
descriptions of system state, never first person: the product does not have a personality and must
not claim one. Every error names what failed, why, and the single next action, in that order. The
worked pattern is: "Cannot issue safety document SD-2291. Device NG-SEC-142 reports position
quality `indeterminate`. Verify the device position in the field and record a manual override." A
message that says an operation failed without naming the object and the reason is a defect. The
words "error", "problem", "issue" and "something went wrong" are never the whole of a message, and
the product never apologises, because the operator is working and sympathy costs them reading time.
Quantities always carry their unit in its standard form and are never abbreviated below it: write
"4.2 kV", not "4.2k". Counts above four digits use a thin group separator and never a magnitude
letter on any operational surface. Times carry their zone, always, and carry coordinated universal
time in parentheses on any surface that becomes evidence. Destructive confirmations state the count
and the reversibility. Empty states state what would fill them and how; a blank panel with a single
word is not acceptable. These words are banned in interface copy because each is a claim about
quality that is worth measuring if it is worth making: smooth, fast, seamless, rich, intuitive,
simply, just, easy.

**The decorative budget.** Exactly four movements in this product exist for reasons that are
aesthetic rather than informational, and they are named here so the budget is auditable: the drift
of the permit hatch, the stepped quality of the confirmation stamp, the flight of the authority
badge, and the deliberately slower release of the alarm contrast lift. Every other movement must be
traceable to a decision an operator makes faster or more reliably because of it. Adding a fifth
means removing one of these.

## Constraints

These are the product's explicit non-goals. Each one names a capability the source product has and
this build does not, so that nothing here is left to be guessed at. The scalability targets of a
fleet deployment are not a goal either: the volumes below are what this build must stay responsive
at.

- Four roles only, as set out above. The network planning engineer who runs contingency studies
  away from a live event, the platform administrator who configures identity and policy, the
  executive sponsor who reads reliability performance, and the field dispatch supervisor are all
  out of scope as separate personas; the capabilities of the dispatch supervisor sit with the
  coordinator, and the others have no surface in this build.
- One organization, seeded. No tenant creation, no organization switcher, no cross-organization
  sharing, no residency configuration and no tenant termination.
- No account creation of any kind: no signup, no invitation, no password reset, no self-service
  profile creation. Accounts exist only because they are seeded into the realm.
- No provisioning protocol, no assertion-based federation metadata exchange, no break-glass path
  and no hardware authenticator enrolment. The identity provider named in this brief is the only
  identity surface.
- No policy authoring surface and no policy simulator. Authorization is the fixed role and area
  model in `## User roles`, not a document a user writes.
- No bulk operations surface, no feature flags, no quota administration and no webhook
  subscriptions.
- No evidence bundle export, no legal hold, no data-loss-prevention scanning and no signed download
  links. The record is readable and verifiable in the product and is not exported.
- No email, no messaging, no notification channels and no paging. Every notice is in-product.
- No media uploads, no photographs and no attachments.
- No reliability index reporting, no major-event-day classification and no report builder.
- No road-graph routing service and no live traffic. A crew's estimated arrival is derived from
  straight-line distance and is labelled as such everywhere it appears.
- No contingency sweep over thousands of cases: the study runs over the order's own steps, in
  order, and nothing larger.
- No native application and no offline mode. The app does not keep working with the network off and
  does not queue work to catch up later; when the connection drops it says so and refuses the
  actions whose correctness depends on current state.
- No external network calls at run time. Everything the product needs is in this environment.
- No third-party analytics, no advertising and no tracking beyond the recorded page view and the
  cookie choice this brief asks for.
- The app must stay responsive with a published model of at least 5,000 elements, 50,000 stored
  measurement samples, 200 alarms and 500 record entries.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses.
  Read both from the environment; never hardcode either.
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

**Environment variables the app reads.** `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`; `DATABASE_URL`
for PostgreSQL; and `AUTH_URL`, `AUTH_REALM`, `AUTH_CLIENT_ID` and `AUTH_CLIENT_SECRET` for
Keycloak. There are no others.

**API shapes.** Every path below is prefixed `/api/v1` except `/api/health`. Field names are exact.
A list endpoint returns a top-level JSON array or a `data` array with a `page` object carrying
`next_cursor`, `has_more` and `limit`. A successful call returns the named resource or shape. An
invalid, unauthenticated or unauthorized call is rejected as a client error, never as a server
error and never as a silent success, and its body is `{"error": {"code": "...", "message": "...",
"detail": {...}}}` where `code` is one of the stable strings this brief names, `message` follows the
copy rule above and is safe to display, and `detail` never contains anything the caller may not
read. Every path is prefixed `/api/v1` except `GET /api/health` and the two session endpoints,
`POST /api/auth/login` and `POST /api/auth/logout`, which are unversioned because a session is not
part of the operational API's own contract. Every call except the health endpoint, the discovery
endpoint and the sign-in endpoint carries the bearer token.

| Endpoint | Request body or query | Returns |
|---|---|---|
| `GET /api/health` | none | `{status, checks}` |
| `GET /api/v1/auth/discover` | `?email=` | `{realm, sign_in_required}` |
| `POST /api/auth/login` | `{email, password, company_website}` | `{access_token}` plus `{id, email, display_name, role, assigned_areas}` |
| `POST /api/auth/logout` | none | no content |
| `GET /api/v1/me` | none | `{id, email, display_name, role, assigned_areas, capabilities}` |
| `GET /api/v1/model-versions` | `?state=` cursor | model versions |
| `POST /api/v1/model-versions/{train}/approve` | `{comment}` | model version |
| `POST /api/v1/model-versions/{train}/publish` | `{acknowledged_warnings}` | model version |
| `GET /api/v1/elements` | `?model_version=&area=&class=` cursor | elements |
| `GET /api/v1/elements/{stableKey}` | `?model_version=` | element with its latest state |
| `GET /api/v1/elements/{stableKey}/connectivity` | `?depth=` | neighbours |
| `POST /api/v1/elements/{stableKey}/position-override` | `{asserted_position, reason, field_reference}` | position override |
| `POST /api/v1/position-overrides/{overrideId}/reconcile` | `{note}` | position override |
| `POST /api/v1/measurements/ingest` | `{samples}` | `{accepted, rejected}` |
| `GET /api/v1/measurements/latest` | `?point_ids=` | latest values with quality and age |
| `POST /api/v1/measurements/series` | `{point_ids, from, to, target_samples}` | series with `envelope`, `min`, `max`, `avg` |
| `GET /api/v1/alarms` | `?state=&sort=` cursor | alarms in `computed_priority` order |
| `POST /api/v1/alarms/{alarmId}/acknowledge` | `{classification}` | alarm |
| `POST /api/v1/alarms/{alarmId}/suppress` | `{reason, duration_s}` | alarm |
| `GET /api/v1/incidents` | `?state=` cursor | incidents |
| `POST /api/v1/incidents` | `{severity, seed_alarm_ids, area_names}` | incident |
| `GET /api/v1/incidents/{reference}` | none | incident with members and outage |
| `POST /api/v1/incidents/{reference}/command` | `{expected_command_version}` | incident |
| `POST /api/v1/incidents/{reference}/timeline` | `{kind, body}` | timeline entry |
| `POST /api/v1/incidents/{reference}/close` | `{closure_summary}` | incident, or a refusal listing `blockers` |
| `GET /api/v1/outages/{outageId}/impact` | none | impact snapshot |
| `PUT /api/v1/outages/{outageId}/etr` | `{estimated_restoration_at, reason}` | outage |
| `GET /api/v1/switching-orders` | `?state=&area=` cursor | orders |
| `POST /api/v1/switching-orders` | `{incident_reference, area_name}` | order |
| `GET /api/v1/switching-orders/{reference}` | none | order with its steps and approvals |
| `POST /api/v1/switching-orders/{reference}/steps` | `{element_stable_key, action, after_ordinal}` | step |
| `PATCH /api/v1/switching-orders/{reference}/steps/{stepId}` | `{action, ordinal}` | step |
| `DELETE /api/v1/switching-orders/{reference}/steps/{stepId}` | none | no content |
| `POST /api/v1/switching-orders/{reference}/study` | `{base_state_at}` | study run with per-step cases and violations |
| `POST /api/v1/switching-orders/{reference}/submit` | none | order |
| `POST /api/v1/switching-orders/{reference}/approve` | `{approved_hash, comment}` | order |
| `POST /api/v1/switching-orders/{reference}/reject` | `{comment}` | order |
| `POST /api/v1/switching-orders/{reference}/steps/{stepId}/confirm-token` | none | `{confirm_token, expires_at}` |
| `POST /api/v1/switching-orders/{reference}/steps/{stepId}/execute` | `{confirm_token}` | step with its attempt and predicted result |
| `POST /api/v1/switching-orders/{reference}/suspend` | `{reason}` | order |
| `POST /api/v1/switching-orders/{reference}/resume` | none | order |
| `POST /api/v1/switching-orders/{reference}/abort` | `{reason}` | order |
| `POST /api/v1/safety-documents/validate` | `{order_reference, isolated_element_keys, isolating_device_keys}` | `{valid, findings}` |
| `POST /api/v1/safety-documents` | `{order_reference, crew_call_sign, isolated_element_keys, isolating_device_keys}` | safety document |
| `POST /api/v1/safety-documents/{reference}/release` | `{all_clear_confirmed, confirmed_by}` | safety document |
| `GET /api/v1/crews` | `?availability=&area=` | crews with availability and lease holder |
| `POST /api/v1/dispatch/assignments` | `{crew_call_sign, incident_reference, target_element_key, skill_override_reason}` | assignment |
| `POST /api/v1/dispatch/assignments/{assignmentId}/recall` | `{reason}` | assignment |
| `POST /api/v1/handovers` | `{incoming_email, shift_ends_at}` | handover with pre-assembled items |
| `GET /api/v1/handovers/{handoverId}` | none | handover |
| `PATCH /api/v1/handovers/{handoverId}/items/{itemId}` | `{disposition, note, view_state}` | handover item |
| `POST /api/v1/handovers/{handoverId}/submit` | none | handover, or a refusal listing undispositioned items |
| `POST /api/v1/handovers/{handoverId}/accept` | none | handover |
| `GET /api/v1/audit/events` | `?incident_reference=&actor=&from=&to=` cursor | record entries |
| `POST /api/v1/audit/verify` | `{from, to}` | `{from_sequence, to_sequence, entry_count, computed_root, expected_root, verified, first_divergent_sequence}` |
| `POST /api/v1/cookie-choice` | `{non_essential_accepted}` | `{visitor_token, non_essential_accepted}` |
| `GET /api/v1/events` | none | the live stream for the session |

The stable error codes this brief names are `ALARM_ALREADY_ACKNOWLEDGED`,
`SUPPRESSION_BLOCKED_BY_PERMIT`, `OUT_OF_AREA`, `COMMAND_VERSION_CONFLICT`,
`SELF_APPROVAL_DENIED`, `VERSION_CONFLICT`, `CONFIRMATION_REQUIRED`, `APPROVAL_HASH_MISMATCH`,
`STEP_OUT_OF_ORDER`, `MODEL_VERSION_ELEMENT_MISSING`, `SAFETY_DOCUMENT_CONFLICT`,
`SAFETY_VALIDATION_FAILED`, `LEASE_HELD`, `UNDISPOSITIONED_ITEMS` and `AUDIT_UNAVAILABLE`.

**No stand-ins.** PostgreSQL is where this product's data lives and Keycloak is where its accounts
live. An in-memory array of users, a hardcoded token the app hands back to itself, a table of
accounts in the application's own schema carrying passwords, an account created by the app rather
than seeded into the realm, or a study result computed in the browser and posted back as though the
server produced it: each of those is a contract violation however good the interface looks. The
named provider is the fact, and the app's own tables and its own screens can only reflect what
lives in the provider, never substitute for it.

## Definition of done

A control room operator signs in with the credential their identity provider holds, acknowledges
the live alarm, drafts a switching order against the published network model, sees the study
return a thermal violation on the conductor that would be overloaded, fixes the order, and hands
it to a coordinator who approves it. The operator then executes the first step behind a two-stage
confirmation, and the step completes only when a measurement says the device moved. An operator who
tries to approve is refused and the order is untouched, a live isolation permit stops a
re-energizing step being written at all, and every one of those acts is in the chained record.
