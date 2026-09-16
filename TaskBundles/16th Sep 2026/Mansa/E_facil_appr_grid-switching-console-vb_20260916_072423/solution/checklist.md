# Checklist: grid-switching-console-vb

Items: 328
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC
Unpinned values flagged: 8

## C-OV Overview

- [ ] `C-OV-01` `capability` The console holds the electrical network as a versioned model `src: Overview`
- [ ] `C-OV-02` `capability` The console holds live measurements arriving from every monitored point `src: Overview`
- [ ] `C-OV-03` `capability` The console holds alarms raised from those measurements `src: Overview`
- [ ] `C-OV-04` `capability` The console holds incidents, switching orders, isolation permits `src: Overview`
- [ ] `C-OV-05` `capability` One continuous operations canvas holds the whole network, with every other panel docking over the canvas `src: Overview`
- [ ] `C-OV-06` `capability` Every operational artefact binds to an immutable model version `src: Overview`
- [ ] `C-OV-07` `constraint` No unauthenticated route returns anything beyond the sign-in entry, the terms page, static assets `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` An `operator` acknowledges alarms inside an assigned operating area `src: User roles`
- [ ] `C-RL-02` `role` An `operator` creates, edits, submits switching orders inside an assigned operating area `src: User roles`
- [ ] `C-RL-03` `role` An `operator` executes steps of an approved order inside an assigned operating area `src: User roles`
- [ ] `C-RL-04` `role` An `operator` cannot approve any switching order `src: User roles`
- [ ] `C-RL-05` `role` An `operator` cannot publish a model version `src: User roles`
- [ ] `C-RL-06` `role` An `operator` cannot issue an isolation permit, cannot release one `src: User roles`
- [ ] `C-RL-07` `role` An `operator` cannot read the append-only record `src: User roles`
- [ ] `C-RL-08` `role` A `coordinator` approves switching orders of risk class 1 to 3 `src: User roles`
- [ ] `C-RL-09` `role` A `coordinator` cannot publish a model version `src: User roles`
- [ ] `C-RL-10` `role` A `controller` gives the second distinct signature a risk class 4 order needs `src: User roles`
- [ ] `C-RL-11` `role` A `controller` publishes a model version a `coordinator` has approved `src: User roles`
- [ ] `C-RL-12` `role` An `auditor` reads the whole append-only record `src: User roles`
- [ ] `C-RL-13` `role` An `auditor` cannot acknowledge an alarm `src: User roles`
- [ ] `C-RL-14` `role` An `auditor` cannot touch an order, a permit, a crew assignment `src: User roles`
- [ ] `C-RL-15` `contract` Authorization runs server-side on every mutating endpoint, so a direct call from a lower role to a higher-role endpoint is denied with the protected state unchanged `src: User roles`
- [ ] `C-RL-16` `role` An `operator` acts only on elements whose operating area is one of the assigned areas `src: User roles`
- [ ] `C-RL-17` `role` No identity approves a switching order that identity created once the order reaches risk class 2 `src: User roles`
- [ ] `C-RL-18` `constraint` No role holds a capability to delete a record entry `src: User roles`
- [ ] `C-RL-19` `literal` The seeded accounts are `operator@example.com`, `operator2@example.com`, `coordinator@example.com`, `controller@example.com`, `auditor@example.com` `src: User roles`
- [ ] `C-RL-20` `literal` Every seeded account uses the password `deku-demo-pw-2026` `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` The sign-in surface takes an email address, relays the credential to the identity provider `src: Core features rule 1`
- [ ] `C-CF-02` `capability` A credential the identity provider rejects produces a refusal naming neither which half was wrong nor whether the email exists `src: Core features rule 1`
- [ ] `C-CF-03` `capability` A rejected sign-in takes the same time whether or not the address is known `src: Core features rule 1`
- [ ] `C-CF-04` `capability` A successful sign-in stores the subject identifier, the email, the display name, the realm roles on the session `src: Core features rule 2`
- [ ] `C-CF-05` `literal` Signing in at `POST /api/auth/login` returns `access_token`, sent as a bearer token on every other call `src: Core features rule 2`
- [ ] `C-CF-06` `capability` Every request resolves role plus assigned areas from the token on the server `src: Core features rule 3`
- [ ] `C-CF-07` `capability` A request carrying no token, an expired token, a malformed token is denied `src: Core features rule 3`
- [ ] `C-CF-08` `capability` A denial names the capability required `src: Core features rule 3`
- [ ] `C-CF-09` `capability` Signing out ends the session `src: Core features rule 4`
- [ ] `C-CF-10` `capability` A token presented after sign-out is denied `src: Core features rule 4`
- [ ] `C-CF-11` `literal` A session expires `12` hours after creation `src: Core features rule 5`
- [ ] `C-CF-12` `constraint` The app stores no password, offers no signup, no reset, no invitation `src: Core features Auth`
- [ ] `C-CF-13` `capability` Elements, connectivity, operating areas belong to a model version identified by an increasing integer train `src: Core features rule 6`
- [ ] `C-CF-14` `capability` Exactly one model version sits in state `published` at a time `src: Core features rule 6`
- [ ] `C-CF-15` `literal` The seeded published version is train `418` `src: Core features rule 6`
- [ ] `C-CF-16` `literal` Train `419` exists in state `ready`, unpublished `src: Core features rule 6`
- [ ] `C-CF-17` `constraint` A published version is immutable, with no edit path `src: Core features rule 7`
- [ ] `C-CF-18` `capability` Publishing a new version moves the previous one to `superseded`, recording the successor `src: Core features rule 7`
- [ ] `C-CF-19` `capability` A `coordinator` moves a `ready` version to `pending_approval` by approving `src: Core features rule 8`
- [ ] `C-CF-20` `capability` A `controller` publishes a version a different identity approved `src: Core features rule 8`
- [ ] `C-CF-21` `capability` A `controller` publishing a version nobody approved is refused, leaving the version `ready` `src: Core features rule 8`
- [ ] `C-CF-22` `capability` Publishing is refused whenever any switching order sits in `executing` or in `suspended`, naming every blocking order `src: Core features rule 9`
- [ ] `C-CF-23` `capability` Publishing leaves orders, permits, study runs pinned to the version each was created against `src: Core features rule 10`
- [ ] `C-CF-24` `capability` Every measurement sample carries a value, an observed instant, a received instant, a quality flag, a source `src: Core features rule 11`
- [ ] `C-CF-25` `capability` A sample submitted without a quality flag is rejected, named in the rejected list, with the rest of the batch accepted `src: Core features rule 11`
- [ ] `C-CF-26` `capability` A sample whose unit differs from the declared unit of the point is rejected, never converted `src: Core features rule 11`
- [ ] `C-CF-27` `capability` A point whose newest sample is older than the expected period is marked stale, with the reading age shown `src: Core features rule 12`
- [ ] `C-CF-28` `capability` A measurement history request over a wide window returns a minimum plus a maximum per bucket, saying so `src: Core features rule 13`
- [ ] `C-CF-29` `constraint` A mean-only reduction of a wide window is not acceptable `src: Core features rule 13`
- [ ] `C-CF-30` `capability` Only a machine identity holding the ingest scope writes a measurement `src: Core features rule 14`
- [ ] `C-CF-31` `capability` A signed-in human session attempting a measurement write is denied whatever the role `src: Core features rule 14`
- [ ] `C-CF-32` `capability` Alarm rules are evaluated continuously against arriving measurements `src: Core features rule 15`
- [ ] `C-CF-33` `capability` Alarms are listed in descending order of the server-computed ranking value `src: Core features rule 15`
- [ ] `C-CF-34` `capability` The client never calculates the ranking value of an alarm `src: Core features rule 15`
- [ ] `C-CF-35` `literal` The seeded alarm on `4B-RCL-118` has a ranking value of `34412` `src: Core features rule 15`
- [ ] `C-CF-36` `capability` Two operators acknowledging one alarm together produce exactly one acknowledgement `src: Core features rule 16`
- [ ] `C-CF-37` `literal` The losing acknowledgement is refused with the code `ALARM_ALREADY_ACKNOWLEDGED`, naming the winning identity plus the instant `src: Core features rule 16`
- [ ] `C-CF-38` `capability` The record carries exactly one acknowledgement entry per alarm `src: Core features rule 16`
- [ ] `C-CF-39` `literal` Suppressing needs a reason of `8` to `500` characters `src: Core features rule 17`
- [ ] `C-CF-40` `literal` Suppressing needs a duration between `60` seconds, `86400` seconds `src: Core features rule 17`
- [ ] `C-CF-41` `capability` A suppression value outside a stated range is rejected, the field is named, nothing is written `src: Core features rule 17`
- [ ] `C-CF-42` `literal` Suppressing an alarm inside a live permit's isolated set is refused with the code `SUPPRESSION_BLOCKED_BY_PERMIT`, leaving the alarm `active` `src: Core features rule 17`
- [ ] `C-CF-43` `literal` An operator acting on an alarm outside the assigned areas is denied with the code `OUT_OF_AREA`, leaving the alarm row unchanged `src: Core features rule 18`
- [ ] `C-CF-44` `literal` The seeded incident is `INC-4471` at urgency 2 in state `open` with no commander `src: Core features rule 19`
- [ ] `C-CF-45` `capability` A `coordinator` assumes command by sending the command version believed current, becoming commander when that version still holds `src: Core features rule 20`
- [ ] `C-CF-46` `literal` A stale assume is refused with the code `COMMAND_VERSION_CONFLICT`, naming the identity currently holding command, changing nothing `src: Core features rule 20`
- [ ] `C-CF-47` `capability` Exactly one identity holds command of an incident at a time `src: Core features rule 20`
- [ ] `C-CF-48` `capability` The incident timeline is append-only, ordered by a server-assigned sequence gapless within the incident `src: Core features rule 21`
- [ ] `C-CF-49` `constraint` Client timestamps are recorded, never used for timeline ordering `src: Core features rule 21`
- [ ] `C-CF-50` `literal` A timeline note runs `1` to `4000` characters `src: Core features rule 21`
- [ ] `C-CF-51` `capability` Closing an incident is refused whenever an attached order sits in `executing` or in `suspended` `src: Core features rule 22`
- [ ] `C-CF-52` `capability` Closing an incident is refused whenever a permit scoped to the incident sits in `live` `src: Core features rule 22`
- [ ] `C-CF-53` `capability` Closing an incident is refused whenever a manual position override made during the incident stays unreconciled `src: Core features rule 22`
- [ ] `C-CF-54` `capability` The close refusal lists every blocker with a kind plus a reference `src: Core features rule 22`
- [ ] `C-CF-55` `capability` An outage impact snapshot still resolving renders a minimum plus a maximum, never a midpoint `src: Core features rule 23`
- [ ] `C-CF-56` `literal` The seeded snapshot reads `4100` as the minimum affected count, `4700` as the maximum, `61` on the sensitive register `src: Core features rule 23`
- [ ] `C-CF-57` `literal` The seeded snapshot carries `182400` integer minor units in `usd` as the estimated interruption cost `src: Core features rule 23`
- [ ] `C-CF-58` `capability` Reading the sensitive customer register writes a record entry carrying the count returned, never the identities `src: Core features rule 24`
- [ ] `C-CF-59` `capability` An order pins the currently published model version at the moment of creation `src: Core features rule 25`
- [ ] `C-CF-60` `literal` The seeded order is `SWO-2026-014` in state `draft`, pinned to train `418`, area `Northgate`, owned by `operator@example.com` `src: Core features rule 25`
- [ ] `C-CF-61` `capability` A step names an element by stable key plus an action drawn from the eight permitted actions `src: Core features rule 26`
- [ ] `C-CF-62` `ui` A step is added inline to the step list by picking the device on the operations canvas, never through a separate page `src: Core features rule 26`
- [ ] `C-CF-63` `capability` Step ordinals stay dense, contiguous, renumbering the rest on insert, delete, reorder `src: Core features rule 26`
- [ ] `C-CF-64` `capability` The order carries a digest over the ordered step list, recomputed whenever a step changes `src: Core features rule 27`
- [ ] `C-CF-65` `capability` A study returns for each step the predicted post-step state, the customers de-energized, the per-conductor loading against rating, any violation `src: Core features rule 28`
- [ ] `C-CF-66` `capability` The same order with the same pinned version plus the same base-state instant produces identical study results every run `src: Core features rule 28`
- [ ] `C-CF-67` `literal` A conductor loading above `1.000` is a `thermal` violation of the severe class `src: Core features rule 28`
- [ ] `C-CF-68` `literal` A conductor loading from `0.800` to `1.000` inclusive is a `thermal` violation of the lesser class `src: Core features rule 28`
- [ ] `C-CF-69` `literal` Closing `NG-TIE-330` with `NG-SEC-142` closed gives `HS-OHL-3301` a loading of `1.070` `src: Core features rule 28`
- [ ] `C-CF-70` `literal` Opening `NG-SEC-142` before closing the tie gives `HS-OHL-3301` a loading of `0.780` `src: Core features rule 28`
- [ ] `C-CF-71` `capability` Submitting moves the order to `pending_approval`, recording the digest submitted `src: Core features rule 29`
- [ ] `C-CF-72` `capability` An approval records the exact step-sequence digest approved `src: Core features rule 30`
- [ ] `C-CF-73` `capability` An order sits in `approved`, `executing`, `completed` only when the approved digest equals the current digest `src: Core features rule 30`
- [ ] `C-CF-74` `capability` Editing any step of an approved order returns the order to `draft`, clearing the approved digest `src: Core features rule 30`
- [ ] `C-CF-75` `capability` An `operator` session calling approve on any order is denied `src: Core features rule 31`
- [ ] `C-CF-76` `capability` A denied approve leaves the order state, the approved digest, the approval history unchanged `src: Core features rule 31`
- [ ] `C-CF-77` `literal` An identity approving an order that identity created at risk class 2 or above is refused with the code `SELF_APPROVAL_DENIED` `src: Core features rule 32`
- [ ] `C-CF-78` `capability` A refused self-approval names the separation-of-duty rule, leaving the order `pending_approval` `src: Core features rule 32`
- [ ] `C-CF-79` `capability` Risk class is computed on the server, never calculated nor overridden by the client `src: Core features rule 33`
- [ ] `C-CF-80` `literal` Risk class is the lowest band below `500` customers at risk, the middle band from `500` to `1999`, the third band at `2000` or more `src: Core features rule 33`
- [ ] `C-CF-81` `capability` Risk class reaches the third band whenever the order closes a normally-open tie against a still-connected alternate source `src: Core features rule 33`
- [ ] `C-CF-82` `literal` Risk class reaches the top band when the order reaches `2000` customers plus creates a parallel path `src: Core features rule 33`
- [ ] `C-CF-83` `capability` A risk class 1 to 3 order needs one approval from a `coordinator` or a `controller` `src: Core features rule 33`
- [ ] `C-CF-84` `capability` A risk class 4 order needs two approvals from two distinct identities, at least one a `controller` `src: Core features rule 33`
- [ ] `C-CF-85` `capability` A single approval on a risk class 4 order leaves the order `pending_approval` `src: Core features rule 33`
- [ ] `C-CF-86` `literal` The seeded order `SWO-2026-014` puts `4412` customers at risk, landing at risk class 3 `src: Core features rule 33`
- [ ] `C-CF-87` `capability` Two identities approving one order together produce exactly one approval record `src: Core features rule 34`
- [ ] `C-CF-88` `literal` The losing approval is refused with the code `VERSION_CONFLICT`, naming the approval that won `src: Core features rule 34`
- [ ] `C-CF-89` `literal` Executing a step needs a confirmation token minted for that step plus that identity, valid `120` seconds, usable once `src: Core features rule 35`
- [ ] `C-CF-90` `literal` An execute without a usable confirmation token is refused with the code `CONFIRMATION_REQUIRED`, emitting no instruction `src: Core features rule 35`
- [ ] `C-CF-91` `literal` An execute whose approved digest differs from the current digest is refused with the code `APPROVAL_HASH_MISMATCH` `src: Core features rule 36`
- [ ] `C-CF-92` `literal` An execute whose step ordinal is not the next one is refused with the code `STEP_OUT_OF_ORDER` `src: Core features rule 36`
- [ ] `C-CF-93` `literal` An execute whose element is absent from the pinned version is refused with the code `MODEL_VERSION_ELEMENT_MISSING` `src: Core features rule 36`
- [ ] `C-CF-94` `literal` An execute forbidden by a live permit is refused with the code `SAFETY_DOCUMENT_CONFLICT`, naming the permit `src: Core features rule 36`
- [ ] `C-CF-95` `literal` An execute whose order area is outside the caller's assigned areas is refused with the code `OUT_OF_AREA` `src: Core features rule 36`
- [ ] `C-CF-96` `capability` A refused execute writes nothing, emitting no instruction `src: Core features rule 36`
- [ ] `C-CF-97` `capability` A step is given an idempotency key when the step is created, never when the step is executed `src: Core features rule 37`
- [ ] `C-CF-98` `capability` Two simultaneous executions of one step produce exactly one execution attempt, one emitted instruction, one record entry `src: Core features rule 37`
- [ ] `C-CF-99` `capability` Both callers of a doubled execute receive the same body `src: Core features rule 37`
- [ ] `C-CF-100` `capability` A repeat of a completed execution returns the original outcome, emitting nothing `src: Core features rule 37`
- [ ] `C-CF-101` `capability` A step execution in flight when the process restarts resumes rather than starting again `src: Core features rule 38`
- [ ] `C-CF-102` `capability` A resumed execution emits no second instruction `src: Core features rule 38`
- [ ] `C-CF-103` `capability` Execution emits a signed instruction, moving the step to `instructed` `src: Core features rule 39`
- [ ] `C-CF-104` `capability` A step reaches `confirmed` only when a measurement reports the device in the commanded position with quality `good` `src: Core features rule 39`
- [ ] `C-CF-105` `literal` A step with no confirming measurement within `30` seconds moves to `failed`, offering a manual confirmation path `src: Core features rule 39`
- [ ] `C-CF-106` `constraint` The product never retries a control instruction on its own `src: Core features rule 39`
- [ ] `C-CF-107` `capability` Publishing a newer model version during an execution leaves the order pinned, showing a non-blocking drift notice naming both trains `src: Core features rule 40`
- [ ] `C-CF-108` `literal` An order may be aborted with a reason of `12` to `1000` characters `src: Core features rule 41`
- [ ] `C-CF-109` `capability` An aborted order keeps every completed step plus the execution history, rolling nothing back `src: Core features rule 41`
- [ ] `C-CF-110` `capability` Issuing a permit validates first against live measurements rather than against the order's intent `src: Core features rule 42`
- [ ] `C-CF-111` `capability` Validation needs every isolating device reporting the required position with quality `good` `src: Core features rule 42`
- [ ] `C-CF-112` `capability` A device reporting `indeterminate` or `stale` fails validation, with the response naming that device, the quality, the instant of the reading `src: Core features rule 42`
- [ ] `C-CF-113` `literal` Validating over `NG-OHL-2202` with isolating devices `4B-RCL-118`, `NG-SEC-142` fails because `NG-SEC-142` reports position quality `indeterminate` `src: Core features rule 42`
- [ ] `C-CF-114` `literal` Issuing without a passing validation is refused with the code `SAFETY_VALIDATION_FAILED`, creating no permit `src: Core features rule 43`
- [ ] `C-CF-115` `capability` An issued permit stores the value, the quality, the observed instant of every isolating device as of validation `src: Core features rule 44`
- [ ] `C-CF-116` `literal` Adding a step that would energize an element inside a live permit's isolated set is refused at authoring time with the code `SAFETY_DOCUMENT_CONFLICT` `src: Core features rule 45`
- [ ] `C-CF-117` `capability` A step refused by a live permit is not added `src: Core features rule 45`
- [ ] `C-CF-118` `capability` Releasing a permit needs an explicit all-clear confirmation naming the crew, asserting every crew member is clear `src: Core features rule 46`
- [ ] `C-CF-119` `capability` A release without the all-clear assertion is refused, leaving the permit `live` `src: Core features rule 46`
- [ ] `C-CF-120` `literal` The release confirm control stays non-interactive for `800` milliseconds after the confirmation opens `src: Core features rule 46`
- [ ] `C-CF-121` `literal` A manual position override records a reason of `12` to `500` characters plus a field reference `src: Core features rule 47`
- [ ] `C-CF-122` `capability` An override sets the element's effective position with quality `manual` `src: Core features rule 47`
- [ ] `C-CF-123` `capability` An unreconciled override blocks incident closure, appearing in shift handover `src: Core features rule 47`
- [ ] `C-CF-124` `literal` Assigning a leased crew a second time is refused with the code `LEASE_HELD` naming the holder, leaving the first assignment untouched `src: Core features rule 48`
- [ ] `C-CF-125` `capability` An assignment whose crew skills miss the required skills is refused unless an override reason is supplied `src: Core features rule 49`
- [ ] `C-CF-126` `capability` A crew estimate derived from straight-line distance is labelled straight-line everywhere the estimate appears `src: Core features rule 50`
- [ ] `C-CF-127` `capability` Every state-changing action writes one record entry carrying a gapless sequence number, the acting identity, the capability exercised, the outcome `src: Core features rule 51`
- [ ] `C-CF-128` `capability` A record entry hash covers the previous entry's hash followed by the canonical form of the entry `src: Core features rule 51`
- [ ] `C-CF-129` `literal` The first record entry carries `64` zeroes as the previous hash `src: Core features rule 51`
- [ ] `C-CF-130` `constraint` The record accepts insertions only, with no role, no endpoint updating nor deleting an entry `src: Core features rule 52`
- [ ] `C-CF-131` `ui` The interface renders no edit control, no delete control on the record in any state `src: Core features rule 52`
- [ ] `C-CF-132` `capability` A chain recomputation over a window returns the bounds, the entry count, the computed root, the expected root, whether both match `src: Core features rule 53`
- [ ] `C-CF-133` `capability` A chain recomputation returns the first divergent sequence number when the roots differ `src: Core features rule 53`
- [ ] `C-CF-134` `literal` A recomputation window covers at most `366` days `src: Core features rule 53`
- [ ] `C-CF-135` `literal` A state-changing request that cannot be recorded is refused with the code `AUDIT_UNAVAILABLE`, with the state change not occurring `src: Core features rule 54`
- [ ] `C-CF-136` `capability` Opening a handover pre-assembles open incidents, unclosed orders, live permits, unreconciled overrides, suppressed alarms, stale study results `src: Core features rule 55`
- [ ] `C-CF-137` `literal` A pre-assembled study result is one older than `30` minutes `src: Core features rule 55`
- [ ] `C-CF-138` `literal` Every handover item needs a disposition of `carry_forward` or `resolved` with a note of `4` to `2000` characters `src: Core features rule 56`
- [ ] `C-CF-139` `literal` Submitting a handover with an undispositioned item is refused with the code `UNDISPOSITIONED_ITEMS`, listing every one, leaving the handover in `composing` `src: Core features rule 56`
- [ ] `C-CF-140` `capability` Accepting a handover transfers ownership of every carried order to the incoming identity in one act `src: Core features rule 57`
- [ ] `C-CF-141` `capability` A partial handover transfer is not possible `src: Core features rule 57`
- [ ] `C-CF-142` `literal` A terms page lives at `/terms`, linked from the footer of every page `src: Core features rule 58`
- [ ] `C-CF-143` `capability` A first-time visitor is asked once about non-essential cookies, with the answer surviving a reload `src: Core features rule 59`
- [ ] `C-CF-144` `capability` Every form rejects invalid input inline, naming the wrong field plus the reason, keeping what was typed, writing nothing `src: Core features rule 60`
- [ ] `C-CF-145` `literal` The public sign-in form carries a decoy field `company_website` that a person never fills `src: Core features rule 61`
- [ ] `C-CF-146` `capability` A submission arriving with the decoy field filled is refused without creating a session `src: Core features rule 61`
- [ ] `C-CF-147` `literal` More than `5` submissions from one client within `60` seconds are refused, saying when the next attempt is allowed `src: Core features rule 61`
- [ ] `C-CF-148` `capability` An unknown address renders the product's own not-found surface with a way back, answering as not found `src: Core features rule 62`

## C-UF User flow

- [ ] `C-UF-01` `literal` The sign-in entry lives at `/`, the operations surface at `/console` `src: User flow route table`
- [ ] `C-UF-02` `literal` The order builder lives at `/console/orders/:reference`, the record explorer at `/record` `src: User flow route table`
- [ ] `C-UF-03` `capability` The operations canvas encodes camera, time cursor, active layers, selection, pinned version, dock occupancy in the query string `src: User flow`
- [ ] `C-UF-04` `capability` Opening a shared address restores camera, time, layers, selection, dock state `src: User flow`
- [ ] `C-UF-05` `capability` A shared address grants nothing, applying the recipient's own role plus areas `src: User flow`
- [ ] `C-UF-06` `capability` Elements a recipient may not read are omitted, with the omitted number shown `src: User flow`
- [ ] `C-UF-07` `literal` Every alarm, incident, order, order step, study case, record entry has a permalink of the form `/go/{objectType}/{objectId}` `src: User flow`
- [ ] `C-UF-08` `capability` A permalink to an unreadable object renders the permission surface naming the object type plus the capability required, revealing nothing further `src: User flow`
- [ ] `C-UF-09` `capability` A permalink whose element is absent from the current published version opens pinned to the version holding the element, labelling that state `src: User flow`
- [ ] `C-UF-10` `capability` An unauthenticated request for a signed-in route goes to `/`, returning to the originally requested address after sign-in `src: User flow`
- [ ] `C-UF-11` `capability` A session expiring part-way through an action leaves the action unapplied `src: User flow`
- [ ] `C-UF-12` `capability` A signed-in user requesting a route the role forbids gets the permission surface naming the capability required `src: User flow`
- [ ] `C-UF-13` `capability` The permission surface does not reveal whether the object behind the address exists `src: User flow`
- [ ] `C-UF-14` `ui` Every list carries an empty state saying what would fill the list, visually distinct from the loading state `src: User flow states`
- [ ] `C-UF-15` `ui` A surface the viewer may not see is distinct from an empty one, never saying no results where the truth is no permission `src: User flow states`
- [ ] `C-UF-16` `ui` A partial list says how many rows were withheld by permission `src: User flow states`
- [ ] `C-UF-17` `ui` A stale surface says how old the data is, becoming more insistent with age `src: User flow states`
- [ ] `C-UF-18` `ui` An error names what failed, why, the single next action, never taking the application down `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The first moment communicates the present electrical state of the network plus which part is under somebody's hand `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The register is operational: dense, organised, restrained, with controls that stay in one place `src: UI/UX notes`
- [ ] `C-UX-03` `ui` No hero composition, no editorial furniture, no decoration standing in for content appears `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Two modes exist, light plus dark, each designed rather than one inverted from the other `src: UI/UX notes`
- [ ] `C-UX-05` `ui` A neutral page ground sits beside a slightly separated panel ground, readable as separate without a drawn divider `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Eight colours carry electrical meaning, appearing nowhere else in the product `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Every electrical state carries a mandatory pattern as the primary channel at every zoom, in every tier `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Four separate colours carry interface status, carrying nothing electrical `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Typography carries three roles: an interface face, a monospaced face with tabular figures, a display face used only on index tiles `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Every value changing over time uses tabular figures, so a ticking value never reflows neighbours `src: UI/UX notes`
- [ ] `C-UX-11` `ui` One base spacing unit generates every gap in the product `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Elevation is a border plus a shadow, never a shadow alone `src: UI/UX notes`
- [ ] `C-UX-13` `ui` The motion character is mechanical: short, close to linear, reading as a machine responding `src: UI/UX notes`
- [ ] `C-UX-14` `ui` Overshoot, anticipation are prohibited outright, with spring behaviour allowed only for position `src: UI/UX notes`
- [ ] `C-UX-15` `ui` Every animation is interruptible, reaching the interrupting state from the current interpolated value `src: UI/UX notes`
- [ ] `C-UX-16` `ui` A readout may animate presentation, never the quantity, showing the true current value at every frame `src: UI/UX notes`
- [ ] `C-UX-17` `ui` The reduced-motion track is a designed alternative, never a blanket zero-duration override `src: UI/UX notes`
- [ ] `C-UX-18` `literal` Body text holds at least `4.5:1` against the ground, large text at least `3:1` `src: UI/UX notes`
- [ ] `C-UX-19` `literal` Every control target measures at least `24` by `24` CSS pixels `src: UI/UX notes`
- [ ] `C-UX-20` `literal` Text resizes to `200%` with no loss of content, no loss of function `src: UI/UX notes`
- [ ] `C-UX-21` `ui` Full keyboard navigation reaches every interaction, with a visible focus ring holding at least `3:1` `src: UI/UX notes`
- [ ] `C-UX-22` `ui` Meaning is never carried by colour alone `src: UI/UX notes`
- [ ] `C-UX-23` `ui` Every content image carries alternative text saying what the image shows, with decorative images declaring themselves decorative `src: UI/UX notes`
- [ ] `C-UX-24` `ui` Nothing overflows sideways at the smallest supported viewport, with every navigation target reachable `src: UI/UX notes`
- [ ] `C-UX-25` `ui` Each surface leads with one clear primary action, visually distinct from every secondary one `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The client is built with SolidJS compiled by Vite into a production bundle `src: Technical requirements`
- [ ] `C-TR-02` `contract` The server is Express on Node 20 in TypeScript, serving the built client plus the API from one process `src: Technical requirements`
- [ ] `C-TR-03` `literal` The datastore is PostgreSQL, reached at `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-04` `literal` The identity provider is Keycloak, reached at `AUTH_URL` `src: Technical requirements`
- [ ] `C-TR-05` `literal` The realm is named by `AUTH_REALM`, the client by `AUTH_CLIENT_ID`, the secret by `AUTH_CLIENT_SECRET` `src: Technical requirements`
- [ ] `C-TR-06` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced `src: Technical requirements`
- [ ] `C-TR-07` `capability` An email with no account in the realm cannot sign in, cannot be created from inside the product `src: Technical requirements`
- [ ] `C-TR-08` `literal` `GET /api/health` returns `200` once the app holds a database connection, reaching the identity provider's discovery document `src: Technical requirements`
- [ ] `C-TR-09` `contract` Logs are one structured JSON object per line carrying a timestamp, a level, a stable event name, a correlation identifier `src: Technical requirements`
- [ ] `C-TR-10` `constraint` Log lines carry no measurement value, no incident body, no override reason, no secret `src: Technical requirements`
- [ ] `C-TR-11` `capability` One stream per signed-in session carries alarm, incident, order, permit, dispatch events plus a measurement frame `src: Technical requirements`
- [ ] `C-TR-12` `capability` Stream frames are coalesced so only the latest value per point is delivered `src: Technical requirements`
- [ ] `C-TR-13` `capability` A study result carries the model version plus the base-state instant beside the result itself `src: Technical requirements`
- [ ] `C-TR-14` `capability` A losing concurrent request changes nothing, leaving no orphaned row, no step stuck without an attempt, no crew leased to nobody `src: Technical requirements`
- [ ] `C-TR-15` `literal` Every list endpoint pages by an opaque cursor defaulting to `50` items, capped at `200` `src: Technical requirements`
- [ ] `C-TR-16` `capability` A response omitting rows the caller may not read says how many were omitted `src: Technical requirements`
- [ ] `C-TR-17` `constraint` Every interface string is externalized, with no string literal living in a component `src: Technical requirements`
- [ ] `C-TR-18` `constraint` Units of measurement are not localized, so a voltage stays kV in every locale `src: Technical requirements`
- [ ] `C-TR-19` `constraint` No credential, client secret, admin token, connection string appears in anything the browser downloads `src: Technical requirements`
- [ ] `C-TR-20` `contract` Every response carries the standard security headers, a strict transport policy, a content-type policy refusing sniffing `src: Technical requirements`
- [ ] `C-TR-21` `constraint` Personal data lives in the staff account records, the crew member records, the sensitive customer register, nowhere else `src: Technical requirements`
- [ ] `C-TR-22` `constraint` Presence is ephemeral, never persisted `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Twenty-eight tables hold the product's state, with every timestamp in UTC `src: Data model`
- [ ] `C-DM-02` `literal` Every seeded account uses `deku-demo-pw-2026`, written into `/app/USER_README.md` beside each account `src: Data model`
- [ ] `C-DM-03` `data` A model version carries a unique increasing train plus a state drawn from the five permitted values `src: Data model`
- [ ] `C-DM-04` `data` A network element's stable key is unique within a model version, surviving across versions `src: Data model`
- [ ] `C-DM-05` `data` A conductor class element carries a rating, absent on every other class `src: Data model`
- [ ] `C-DM-06` `data` Connectivity edges form the graph deciding what is energized from where `src: Data model`
- [ ] `C-DM-07` `data` A measurement sample without a quality flag does not exist in the store `src: Data model`
- [ ] `C-DM-08` `data` An incident timeline sequence is server-assigned, gapless within the incident `src: Data model`
- [ ] `C-DM-09` `data` A step idempotency key is written at step creation `src: Data model`
- [ ] `C-DM-10` `data` One execution attempt exists per successful execution of a step `src: Data model`
- [ ] `C-DM-11` `data` One approval record exists per approver per digest `src: Data model`
- [ ] `C-DM-12` `data` A permit stores validation evidence covering every isolating device as of validation `src: Data model`
- [ ] `C-DM-13` `data` A record entry sequence is gapless across the deployment `src: Data model`
- [ ] `C-DM-14` `literal` The seeded operating areas are `Northgate`, `Harbourside` `src: Data model seed data`
- [ ] `C-DM-15` `literal` Twelve elements belong to train `418`, from `NG-SUB-01` through `HS-OHL-3301` `src: Data model seed data`
- [ ] `C-DM-16` `literal` `NG-OHL-2202` carries a rating of `180` A, a section load of `58.0` A, `2840` customers `src: Data model seed data`
- [ ] `C-DM-17` `literal` `NG-OHL-2203` carries a rating of `160` A, a section load of `38.0` A, `1572` customers `src: Data model seed data`
- [ ] `C-DM-18` `literal` `HS-OHL-3301` carries a rating of `200` A, a section load of `118.0` A `src: Data model seed data`
- [ ] `C-DM-19` `literal` `NG-SEC-142` reports switch position `closed` with quality `indeterminate` `src: Data model seed data`
- [ ] `C-DM-20` `literal` The seeded crews are `C-07` in `Northgate`, `C-12` in `Harbourside` `src: Data model seed data`
- [ ] `C-DM-21` `literal` The permit reference the seeded scenario issues is `SD-2291` `src: Data model seed data`
- [ ] `C-DM-22` `constraint` Seeding is idempotent, so restarting the app duplicates no rows `src: Data model seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` One loop at the root drives camera integration, the canvas redraw, overlay reconciliation, chart drawing, every interface animation `src: Front-end specification`
- [ ] `C-FE-02` `ui` The operations canvas mounts once for the session, never unmounting `src: Front-end specification`
- [ ] `C-FE-03` `ui` A route change, a dock opening, a selection changing, a measurement arriving rebuilds nothing on the canvas `src: Front-end specification`
- [ ] `C-FE-04` `ui` Live electrical state lives in a state buffer rewritten as measurements arrive `src: Front-end specification`
- [ ] `C-FE-05` `ui` Zoom bands cross-fade rather than popping, continuing from the mix currently on screen when interrupted `src: Front-end specification`
- [ ] `C-FE-06` `ui` The pointer acquires the nearest element within a small radius rather than needing a direct hit `src: Front-end specification`
- [ ] `C-FE-07` `ui` The cursor over the canvas says what the current position will do before the operator commits `src: Front-end specification`
- [ ] `C-FE-08` `ui` Elements changing state together change in one frame, never staggered `src: Front-end specification`
- [ ] `C-FE-09` `ui` A fault pulse travels outward along the electrical graph at a rate set by connection distance rather than screen distance `src: Front-end specification`
- [ ] `C-FE-10` `ui` Study mode draws live state beside studied state, mixing both with the live layer dimmed `src: Front-end specification`
- [ ] `C-FE-11` `ui` Any pan, zoom, drag by the operator cancels a camera animation instantly with no decay ramp `src: Front-end specification`
- [ ] `C-FE-12` `ui` A confirmation stamp runs only on server confirmation, never optimistically, remaining the one uninterruptible animation `src: Front-end specification`
- [ ] `C-FE-13` `ui` A step execution timeline grows live through the phases, hatching a frozen segment on suspension `src: Front-end specification`
- [ ] `C-FE-14` `ui` Progress never animates backward, holding position as the text revises `src: Front-end specification`
- [ ] `C-FE-15` `ui` Uncomputed study cells carry a stipple, so an incomplete run never reads as a clean one `src: Front-end specification`
- [ ] `C-FE-16` `ui` The staleness indicator is never suppressed by a tier, by reduced motion, by a user preference `src: Front-end specification`
- [ ] `C-FE-17` `ui` An insertion never moves content under the pointer, never moves content containing focus `src: Front-end specification`
- [ ] `C-FE-18` `ui` A re-sort caps how many rows animate, applying the rest instantly `src: Front-end specification`
- [ ] `C-FE-19` `ui` Three tiers compute at session start from named signals, with the tier being the minimum any signal permits `src: Front-end specification`
- [ ] `C-FE-20` `ui` Every functional capability stays available at the lowest tier `src: Front-end specification`
- [ ] `C-FE-21` `ui` The canvas mirrors content to a screen-reader-visible tree updated at a bounded rate `src: Front-end specification`
- [ ] `C-FE-22` `ui` Arrow keys traverse the network by electrical connectivity in a deterministic order derived from the model `src: Front-end specification`
- [ ] `C-FE-23` `ui` Assertive announcement is reserved for an authority change, a chain failure, a blocking refusal `src: Front-end specification`
- [ ] `C-FE-24` `ui` Every listed component implements every listed state `src: Front-end specification`
- [ ] `C-FE-25` `ui` The confirm control is the only permitted control for an action changing the electrical network `src: Front-end specification`
- [ ] `C-FE-26` `ui` An empty state distinguishes five kinds: no data, no results, not permitted, error, first run `src: Front-end specification`
- [ ] `C-FE-27` `ui` Icons are one stroked set drawn inline, inheriting the current text colour, with no icon fonts `src: Front-end specification`
- [ ] `C-FE-28` `ui` Electrical device symbols follow the recognised international convention, never restyled for visual consistency `src: Front-end specification`
- [ ] `C-FE-29` `ui` No icon is the sole carrier of state `src: Front-end specification`
- [ ] `C-FE-30` `ui` Every message names what failed, why, the single next action `src: Front-end specification`
- [ ] `C-FE-31` `ui` Quantities carry the unit in standard form, never abbreviated below the unit `src: Front-end specification`
- [ ] `C-FE-32` `ui` Exactly four movements exist for aesthetic reasons, each one named `src: Front-end specification`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` Four roles exist, with the planning engineer, the platform administrator, the executive sponsor out of scope `src: Constraints`
- [ ] `C-CN-02` `constraint` One organization is seeded, with no tenant creation, no organization switcher, no residency configuration `src: Constraints`
- [ ] `C-CN-03` `constraint` No account creation of any kind exists `src: Constraints`
- [ ] `C-CN-04` `constraint` No policy authoring surface exists, no policy simulator `src: Constraints`
- [ ] `C-CN-05` `constraint` No evidence bundle export exists, no legal hold, no signed download links `src: Constraints`
- [ ] `C-CN-06` `constraint` No email, no messaging, no notification channels exist, so every notice is in-product `src: Constraints`
- [ ] `C-CN-07` `constraint` No media uploads exist, no photographs, no attachments `src: Constraints`
- [ ] `C-CN-08` `constraint` No external network calls happen at run time `src: Constraints`
- [ ] `C-CN-09` `literal` The app stays responsive with at least `5,000` elements, `50,000` stored measurement samples, `200` alarms, `500` record entries `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173` `src: Deployment contract`
- [ ] `C-DC-03` `literal` The HTTP API is served on the same origin under the `/api` prefix `src: Deployment contract`
- [ ] `C-DC-04` `literal` `GET /api/health` returns `200` once the app is ready `src: Deployment contract`
- [ ] `C-DC-05` `capability` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-06` `literal` Login credentials are written to `/app/USER_README.md` `src: Deployment contract`
- [ ] `C-DC-07` `literal` Reserved `.browser_screenshots/`, `.downloads/` directories exist at the app root, empty `src: Deployment contract`
- [ ] `C-DC-08` `constraint` A production build is served behind a static or preview server, never a dev server `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends, never a child of the shell `src: Deployment contract`
- [ ] `C-DC-10` `literal` The server binds `0.0.0.0`, never `127.0.0.1`, never `localhost` `src: Deployment contract`
- [ ] `C-DC-11` `constraint` The backing services are already running, so nothing downloads, installs, compiles, starts a copy `src: Deployment contract`
- [ ] `C-DC-12` `constraint` No persistent volumes, no fixed container names, no custom networks are used `src: Deployment contract`
- [ ] `C-DC-13` `literal` The app reads `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `DATABASE_URL`, `AUTH_URL`, `AUTH_REALM`, `AUTH_CLIENT_ID`, `AUTH_CLIENT_SECRET`, nothing else `src: Deployment contract`
- [ ] `C-DC-14` `contract` Every path is prefixed `/api/v1` apart from the health endpoint `src: Deployment contract`
- [ ] `C-DC-15` `contract` A list endpoint returns a top-level JSON array or a `data` array beside a `page` object `src: Deployment contract`
- [ ] `C-DC-16` `contract` A page object carries `next_cursor`, `has_more`, `limit` `src: Deployment contract`
- [ ] `C-DC-17` `contract` A rejected call returns an `error` object carrying `code`, `message`, `detail` `src: Deployment contract`
- [ ] `C-DC-18` `capability` A rejected call is a client error, never a server error, never a silent success `src: Deployment contract`
- [ ] `C-DC-19` `capability` A `detail` object never contains anything the caller may not read `src: Deployment contract`
- [ ] `C-DC-20` `capability` Every call apart from the health endpoint, the discovery endpoint, the sign-in endpoint carries the bearer token `src: Deployment contract`
- [ ] `C-DC-21` `literal` Signing in posts to `POST /api/auth/login`, returning `access_token` plus the acting identity `src: Deployment contract`
- [ ] `C-DC-22` `literal` A step is executed through `POST /api/v1/switching-orders/{reference}/steps/{stepId}/execute` `src: Deployment contract`
- [ ] `C-DC-23` `literal` An order is approved through `POST /api/v1/switching-orders/{reference}/approve` `src: Deployment contract`
- [ ] `C-DC-24` `literal` A permit is validated through `POST /api/v1/safety-documents/validate` `src: Deployment contract`
- [ ] `C-DC-25` `constraint` PostgreSQL holds the product's data, Keycloak holds the accounts, with no in-memory stand-in for either `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `operator@example.com` | the seeded operator account | `C-RL-19` |
| `operator2@example.com` | the second seeded operator account | `C-RL-19` |
| `coordinator@example.com` | the seeded coordinator account | `C-RL-19` |
| `controller@example.com` | the seeded controller account | `C-RL-19` |
| `auditor@example.com` | the seeded auditor account | `C-RL-19` |
| `deku-demo-pw-2026` | the corpus password | `C-RL-20` |
| `operator` | the lowest operational role | `C-RL-01` |
| `coordinator` | the approving role | `C-RL-08` |
| `controller` | the countersigning role | `C-RL-10` |
| `auditor` | the read-only record role | `C-RL-12` |
| `12` | the session lifetime in hours | `C-CF-11` |
| `418` | the seeded published model train | `C-CF-15` |
| `419` | the seeded unpublished model train | `C-CF-16` |
| `published` | the live model version state | `C-CF-14` |
| `ready` | the reviewed model version state | `C-CF-16` |
| `pending_approval` | the awaiting-approval state | `C-CF-19` |
| `superseded` | the retired model version state | `C-CF-18` |
| `executing` | the running order state | `C-CF-22` |
| `suspended` | the paused order state | `C-CF-22` |
| `draft` | the editable order state | `C-CF-60` |
| `approved` | the signed-off order state | `C-CF-73` |
| `completed` | the finished order state | `C-CF-73` |
| `good` | the acceptable measurement quality | `C-CF-104` |
| `indeterminate` | the unusable measurement quality | `C-CF-112` |
| `stale` | the aged measurement quality | `C-CF-112` |
| `manual` | the overridden measurement quality | `C-CF-122` |
| `34412` | the seeded alarm ranking value | `C-CF-35` |
| `4B-RCL-118` | the tripped recloser | `C-CF-35` |
| `ALARM_ALREADY_ACKNOWLEDGED` | the doubled acknowledgement code | `C-CF-37` |
| `8` | the shortest suppression reason | `C-CF-39` |
| `500` | the longest suppression reason | `C-CF-39` |
| `60` | the shortest suppression duration in seconds | `C-CF-40` |
| `86400` | the longest suppression duration in seconds | `C-CF-40` |
| `SUPPRESSION_BLOCKED_BY_PERMIT` | the permit-blocked suppression code | `C-CF-42` |
| `active` | the unacknowledged alarm state | `C-CF-42` |
| `OUT_OF_AREA` | the area-scope denial code | `C-CF-43` |
| `INC-4471` | the seeded incident reference | `C-CF-44` |
| `open` | the uncommanded incident state | `C-CF-44` |
| `COMMAND_VERSION_CONFLICT` | the stale command-assume code | `C-CF-46` |
| `1` | the shortest timeline note | `C-CF-50` |
| `4000` | the longest timeline note | `C-CF-50` |
| `4100` | the seeded minimum affected count | `C-CF-56` |
| `4700` | the seeded maximum affected count | `C-CF-56` |
| `61` | the seeded sensitive register count | `C-CF-56` |
| `182400` | the seeded estimated interruption cost in minor units | `C-CF-57` |
| `usd` | the currency code | `C-CF-57` |
| `SWO-2026-014` | the seeded switching order reference | `C-CF-60` |
| `Northgate` | the first seeded operating area | `C-CF-60` |
| `Harbourside` | the second seeded operating area | `C-DM-14` |
| `thermal` | the loading violation kind | `C-CF-67` |
| `1.000` | the loading above which a violation is severe | `C-CF-67` |
| `0.800` | the loading at which a violation begins | `C-CF-68` |
| `NG-TIE-330` | the normally-open tie switch | `C-CF-69` |
| `NG-SEC-142` | the sectionalizer with unusable position quality | `C-CF-69` |
| `HS-OHL-3301` | the Harbourside conductor that receives the transferred load | `C-CF-69` |
| `1.070` | the loading of the overloaded transfer | `C-CF-69` |
| `0.780` | the loading of the clean transfer | `C-CF-70` |
| `SELF_APPROVAL_DENIED` | the self-approval refusal code | `C-CF-77` |
| `2000` | the customer count at which risk class reaches three | `C-CF-80` |
| `1999` | the top of the middle risk band | `C-CF-80` |
| `4412` | the customers at risk on the seeded order | `C-CF-86` |
| `VERSION_CONFLICT` | the doubled approval code | `C-CF-88` |
| `120` | the confirmation token lifetime in seconds | `C-CF-89` |
| `CONFIRMATION_REQUIRED` | the missing confirmation code | `C-CF-90` |
| `APPROVAL_HASH_MISMATCH` | the voided approval code | `C-CF-91` |
| `STEP_OUT_OF_ORDER` | the wrong-ordinal code | `C-CF-92` |
| `MODEL_VERSION_ELEMENT_MISSING` | the absent element code | `C-CF-93` |
| `SAFETY_DOCUMENT_CONFLICT` | the permit conflict code | `C-CF-94` |
| `instructed` | the emitted step state | `C-CF-103` |
| `confirmed` | the settled step state | `C-CF-104` |
| `failed` | the unconfirmed step state | `C-CF-105` |
| `30` | the confirmation window in seconds | `C-CF-105` |
| `1000` | the longest abort reason | `C-CF-108` |
| `NG-OHL-2202` | the isolated conductor | `C-CF-113` |
| `SAFETY_VALIDATION_FAILED` | the failed permit validation code | `C-CF-114` |
| `800` | the release dwell in milliseconds | `C-CF-120` |
| `LEASE_HELD` | the crew lease conflict code | `C-CF-124` |
| `64` | the zero count in the first previous hash | `C-CF-129` |
| `366` | the longest recomputation window in days | `C-CF-134` |
| `AUDIT_UNAVAILABLE` | the unrecordable action code | `C-CF-135` |
| `carry_forward` | the first handover disposition | `C-CF-138` |
| `resolved` | the second handover disposition | `C-CF-138` |
| `2000` | the longest disposition note | `C-CF-138` |
| `4` | the shortest disposition note | `C-CF-138` |
| `UNDISPOSITIONED_ITEMS` | the blocked handover code | `C-CF-139` |
| `composing` | the unsubmitted handover state | `C-CF-139` |
| `/terms` | the terms page address | `C-CF-142` |
| `company_website` | the decoy field name | `C-CF-145` |
| `5` | the submission count before refusal | `C-CF-147` |
| `/` | the sign-in entry address | `C-UF-01` |
| `/console` | the operations surface address | `C-UF-01` |
| `/console/orders/:reference` | the order builder address | `C-UF-02` |
| `/record` | the record explorer address | `C-UF-02` |
| `/go/{objectType}/{objectId}` | the permalink form | `C-UF-07` |
| `4.5:1` | the body text contrast floor | `C-UX-18` |
| `3:1` | the large text contrast floor | `C-UX-18` |
| `24` | the smallest control target in CSS pixels | `C-UX-19` |
| `200%` | the text resize floor | `C-UX-20` |
| `DATABASE_URL` | the database environment variable | `C-TR-03` |
| `AUTH_URL` | the identity provider environment variable | `C-TR-04` |
| `AUTH_REALM` | the realm environment variable | `C-TR-05` |
| `AUTH_CLIENT_ID` | the client identifier variable | `C-TR-05` |
| `AUTH_CLIENT_SECRET` | the client secret variable | `C-TR-05` |
| `GET /api/health` | the health endpoint | `C-TR-08` |
| `200` | the health response status | `C-TR-08` |
| `50` | the default page size | `C-TR-15` |
| `/app/USER_README.md` | the credentials file | `C-DM-02` |
| `NG-SUB-01` | the first seeded element | `C-DM-15` |
| `180` | the rating of the isolated conductor in amperes | `C-DM-16` |
| `58.0` | the section load of the isolated conductor in amperes | `C-DM-16` |
| `2840` | the customers on the isolated conductor | `C-DM-16` |
| `NG-OHL-2203` | the conductor beyond the sectionalizer | `C-DM-17` |
| `160` | the rating of the far conductor in amperes | `C-DM-17` |
| `38.0` | the section load of the far conductor in amperes | `C-DM-17` |
| `1572` | the customers on the far conductor | `C-DM-17` |
| `118.0` | the section load of the Harbourside conductor in amperes | `C-DM-18` |
| `closed` | the seeded sectionalizer position | `C-DM-19` |
| `C-07` | the Northgate crew | `C-DM-20` |
| `C-12` | the Harbourside crew | `C-DM-20` |
| `SD-2291` | the permit reference the scenario issues | `C-DM-21` |
| `5,000` | the element count the app stays responsive at | `C-CN-09` |
| `50,000` | the stored sample count the app stays responsive at | `C-CN-09` |
| `APP_PUBLIC_URL` | the public address variable | `C-DC-01` |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | `C-DC-02` |
| `/api` | the API prefix | `C-DC-03` |
| `.browser_screenshots/` | the first reserved directory | `C-DC-07` |
| `.downloads/` | the second reserved directory | `C-DC-07` |
| `0.0.0.0` | the bind address | `C-DC-10` |
| `127.0.0.1` | the first forbidden bind address | `C-DC-10` |
| `localhost` | the forbidden bind hostname | `C-DC-10` |
| `APP_PUBLIC_PORT` | the public port variable | `C-DC-13` |
| `data` | the list envelope key | `C-DC-15` |
| `page` | the paging envelope key | `C-DC-15` |
| `next_cursor` | the cursor field | `C-DC-16` |
| `has_more` | the more-pages field | `C-DC-16` |
| `limit` | the page size field | `C-DC-16` |
| `error` | the refusal envelope key | `C-DC-17` |
| `code` | the stable refusal code field | `C-DC-17` |
| `message` | the displayable refusal field | `C-DC-17` |
| `detail` | the structured refusal field | `C-DC-17` |
| `POST /api/auth/login` | the sign-in endpoint | `C-DC-21` |
| `access_token` | the bearer token field | `C-DC-21` |
| `POST /api/v1/switching-orders/{reference}/steps/{stepId}/execute` | the step execution endpoint | `C-DC-22` |
| `POST /api/v1/switching-orders/{reference}/approve` | the approval endpoint | `C-DC-23` |
| `POST /api/v1/safety-documents/validate` | the permit validation endpoint | `C-DC-24` |
| `/api/v1` | the versioned API prefix | `C-DC-14` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact shades behind each named colour role | `C-UX-06` |
| the exact type families, the exact sizes | `C-UX-09` |
| the base spacing unit the whole scale derives from | `C-UX-11` |
| the exact durations behind the named motion tiers | `C-UX-13` |
| the widths at which each responsive arrangement takes over | `C-UX-24` |
| the exact signal thresholds that demote a tier | `C-FE-19` |
| the acquisition radius around a network element | `C-FE-06` |
| the cap on how many rows animate through a re-sort | `C-FE-18` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 5 | 7 |
| User roles | 3 | 20 |
| Core features | 20 | 148 |
| User flow | 10 | 18 |
| UI and UX notes | 13 | 25 |
| Technical requirements | 5 | 22 |
| Data model | 5 | 22 |
| Front-end specification | 14 | 32 |
| Constraints | 2 | 9 |
| Deployment contract | 12 | 25 |
