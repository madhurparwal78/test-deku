# Verwick Xpo

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser and, signed in as a coordinator, hold Hall 4, Hall 5 and the passage between them for a client across a week, confirm that hold into a booking with its build-up and tear-down windows, and watch the same week become unavailable to every other desk in the product, without hitting an error page. A different stranger, signed in as an exhibitor, must NOT be able to read another exhibitor's stand position, service orders or invoice, by any means, including calling the API directly with a valid token. A refusal is a refusal: the record must be unchanged afterwards, and the refusal must be a distinct answer from an empty result. Two coordinators confirming competing holds on the same square metre in the same instant must leave exactly one booking and one clear refusal behind in the store; a green tick the app returns to itself does not count.

## Overview

Verwick Xpo is the software a large exhibition and convention campus runs on. The campus is nearly 40,000 square metres: six halls, an event hall, a modular meeting centre, a covered boulevard that links them and the passages between adjacent halls. The venue does not rent bare space. It sells the hall together with the catering, the ticketing, the parking, the technical services and the safety cover, and the product exists to keep all of that straight while several clients are on site at once.

The product has two surfaces and both are the product. A public site in three languages carries an events calendar, everything a visitor needs on the day, everything an organiser needs including an interactive plan of the whole campus, the company pages, the newsroom and the legal set. Behind one sign-in sits the operations console: the campus calendar, the enquiry and option desk, booking files, the floor-plan planner, services and catering, accreditation and badges, entrance and access control, the occupancy and safety board, the works schedule, invoicing, the publishing desk and reporting.

One sentence generates most of the rules below. The campus is a graph of spaces that fit inside one another, so no two events may ever hold the same square metre at the same time, and exactly one part of the product is allowed to answer the question of whether a space is free. Everything else asks it. The second hard sentence is that capacity is a licensed figure held against a space and a layout, never a number derived from floor area and never the sum of a combination's parts: the venue's highest-capacity hall is not its largest, because capacity comes from exits and licences.

Verwick Xpo deliberately is not a great many things. There is no ticket selling, no seat-level box office, no payroll, no procurement, no supplier marketplace, no customer relationship pipeline beyond the enquiry, no second campus, no native mobile application, no chat, no comments, no likes, no second factor, no federated identity provider and no model call of any kind from any surface. The genuinely hard part is that the building has to be right on the worst day: a hall joined to its neighbour must never be double-sold, a badge withdrawn at midnight must stop working at midnight, an approved plan that blocks a fire exit must reduce the number of people allowed in the room, and a door that loses its network must keep deciding correctly rather than locking everybody out or letting everybody in.

## User roles

Six roles. Signup is closed on the console path: an account exists because it was seeded or because a coordinator invited it. The public site's enquiry form and newsletter capture create an enquiry and a subscription, never a console account.

A role is scoped to a function rather than to a person, and permission is scoped by relationship as well as by role. A `planner` reaches an event because that event's organiser record names the planner's party, not because the role is `planner`. An `exhibitor` reaches a stand because that stand is its own. Two planners on two different events opening the same campus calendar must see different detail on the same week.

| Role | Can read | Can write |
|---|---|---|
| `coordinator` | every enquiry, option, booking, contract, phase, plan revision, service order, accreditation, publication record and report on the campus | enquiries, options and their ranks, challenges, confirmations, contracts and amendments, phase windows, maintenance windows, publication state, annual-plan scenarios, and invitations. **Cannot approve an amendment the same account requested, cannot alter or delete an audit record, cannot declare evacuation, and cannot change a licensed capacity figure.** |
| `operations` | the campus timeline, every entrance and its mode, every badge and scan, live occupancy per space, incidents, the works schedule and the resource calendar | entrance modes per event and per phase, badge issue and suspension, scan decisions, incident records and their close-out, evacuation declaration, licensed capacity revisions, work orders and resource assignments. **Cannot confirm a booking, cannot price or invoice, cannot publish to the public site, and cannot read a contract's commercial terms.** |
| `planner` | the events of the planner's own party: the booking file's operational half, the floor plan and its revisions, service and catering orders, the exhibitor list, accreditation under that party, and the event's own public page | plan revisions and approval requests, service and catering orders within the cut-offs, exhibitor accreditation and the rules that cap it, the event's public fields and translations. **Cannot see another party's event, plan, orders, exhibitors or rates through any surface including search, export and the public preview; cannot confirm a booking; cannot grant a right the planner's own accreditation does not hold; and cannot approve the planner's own plan revision.** |
| `exhibitor` | that exhibitor's own stand and its position on the approved plan, its own accreditation and badges, its own service orders, its own loading-dock slot, its own invoices, plus the event documents the organiser publishes to exhibitors | its own service orders within the organiser's rules, its own stand contractor's accreditation request, and its own loading-dock slot request. **Cannot read or write another exhibitor's stand, position, orders, badges or invoices; a forged request for one is answered as not found rather than as forbidden, so the existence of another stand is never disclosed.** |
| `finance` | contracts, deposit schedules, invoices, lines, payments, metered consumption, variance and every report | invoices, credit notes, deposit schedules, payment records, damage and cleaning charges, and dispute outcomes. **Cannot confirm a booking, cannot change a plan, cannot issue a badge, and cannot alter an audit record.** |
| `auditor` | the append-only audit trail and every report, and nothing else anywhere | nothing, anywhere. **Cannot read an enquiry, a plan, an order, a badge, a contract or a member record, and cannot alter the trail it reads.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a `exhibitor` session to any `coordinator`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

The console's desks are named for the venue's real functions and the six roles above work at them: sales and event coordination at the enquiry and booking desks, operations, technical and security at the timeline, access-control and safety boards, catering at the service desk, finance at invoicing, publishing at the public-content desk, and read-only management at reporting.

Seeded accounts, every one of them using the corpus password `deku-demo-pw-2026`:

| Email | Role | Party |
|---|---|---|
| `coordinator@example.com` | `coordinator` | the venue |
| `operations@example.com` | `operations` | the venue |
| `planner@example.com` | `planner` | `Palmarosa` |
| `planner2@example.com` | `planner` | `Bookmark Fair` |
| `exhibitor@example.com` | `exhibitor` | `Ironwood Interiors`, stand `S-118` |
| `finance@example.com` | `finance` | the venue |
| `auditor@example.com` | `auditor` | the venue |

## Core features

### Auth and sessions

Sign-in takes an email and a password and returns an `access_token` the client sends as a bearer token on every request except sign-in itself, the health route and the unauthenticated public endpoints. Passwords are stored hashed. There is no public registration on the console path.

1. A correct email with a correct password signs in and returns a token that carries the principal's email and role.
2. An unknown address and a wrong password produce the **same** refusal message, the same outcome, and neither response nor any part of the page reveals which of the two happened.
3. Repeated failures for one address are refused after a stated number of attempts, and the lockout is itself written to the audit trail as an authentication event.
4. Signing out stops the token working immediately. A request carrying a signed-out token is refused, not served from a cache.
5. A token that expires mid-action leaves the typed work on screen, says the session has ended, and offers sign-in in place rather than discarding the work.
6. An anonymous caller reaching any console route is served the sign-in route with the address it asked for remembered, and is returned there after signing in.

### The campus and its space model

The campus is a graph, not a list. This is the heart of the product and every other feature reads it.

1. Every space is a node carrying a kind, a floor area in square metres, a licensed capacity per layout, an entrance set and an availability calendar. The kinds are `hall`, `event_hall`, `meeting_room`, `boulevard`, `passage` and `combination`.
2. Spaces compose. Adjacent halls combine into one hireable space; the passage between two halls is itself hireable and is also what makes that combination possible; the covered boulevard connects every hall, may be hired as exhibition or catering space, and remains the public route between halls while it is hired; the meeting rooms combine with one another and with the event hall. A combination is a node whose children are the spaces it consumes.
3. **The overlap rule.** Holding a combination holds every descendant space. Holding any descendant blocks every ancestor combination. No two holds may ever cover the same square metre in the same window, and the answer must come from one authority used by the enquiry desk, the planner, the public calendar, reporting and every interface alike. Checking availability only at the leaf level, or only at the level booked, is a contract violation: it passes every casual test and double-books the boulevard.
4. Availability answers with exactly one state from this closed set, spelled exactly: `free`, `held`, `booked`, `blocked_by_ancestor`, `blocked_by_descendant`, `maintenance`. `blocked_by_ancestor` and `blocked_by_descendant` name the blocking space, because a coordinator told only that a hall is busy cannot tell a client why.
5. **The circulation constraint.** The boulevard may be hired as exhibition or catering space only while a compliant public route between the halls in use remains. Hiring it is refused, with the failing route named, when the resulting route would breach the occupancy rules below. This is the constraint that makes the model more than a calendar.
6. A space added or divided in operations appears on the public floor plan without anyone redrawing a picture, because the public plan is rendered from the same space records the planner works in.
7. The campus carries exactly one campus-wide state at a time, `normal` or `evacuation`, and the safety rules below say what the second one overrides.

### Layouts and licensed capacity

1. A space carries named layouts, from the closed set `theatre`, `cabaret`, `banquet`, `stand_grid` and `standing`. Each layout carries its own licensed capacity and its own build hours.
2. Capacity is a stored, licensed figure per space and per layout. It is never derived from floor area. The seeded inventory proves why: `Hall 5` licenses more people than `Hall 4` in less than two thirds of the floor area, because capacity is a function of layout, exits and licensing.
3. A combination carries its own licensed figure, because exits and circulation change when a wall opens. Adding a combination's children together is a contract violation, and the seeded combination is set so that the sum and the licensed figure differ.
4. The layout chosen for a booking changes two things at once: the number the safety board enforces, and the build hours the works schedule reserves.
5. A licensed figure is versioned. Revising one after a safety inspection applies to bookings confirmed afterwards; last year's approved plans and the occupancy records taken under them still read at the version they were written under. Rewriting historical capacity to today's figure is a contract violation.

### Enquiries, options and the challenge

1. An enquiry arrives from the public contact form or from a coordinator, and carries a contact, a date range, an expected visitor count, an event type and the spaces of interest. A public submission creates an enquiry record in the product; sending an email instead is a contract violation.
2. An option is a soft hold on a named space set across a named window, carrying an expiry and a rank. Option state is exactly one of `held`, `challenged`, `released`, `confirmed` or `lapsed`.
3. Several options may exist on the same space set and window, ranked first, second and third. Ranks are unique per space and window. Taking a lower-ranked option does not block a higher one, and it does not make the space unavailable to the higher rank.
4. **The challenge.** A lower-ranked option may challenge the holder. The holder is notified and has a stated window to confirm or release. On expiry of that window the outcome is applied by the product itself, without anybody pressing a button: an unanswered challenge releases the holder's option and promotes the challenger. Leaving that outcome to a nightly job or to a person is a contract violation.
5. Confirming any option releases the others on that space and window, and each released holder receives a notification record naming the space set, the window and the reason.
6. An option that reaches its expiry with no confirmation becomes `lapsed` and the space returns to `free` for every rank below it.

### Confirmation, the contract file and amendments

1. Confirmation converts an option into a booking **atomically**: the space set, the build-up and tear-down windows, the phase records and the contract record are created in one transaction, or none of them is.
2. **Two coordinators confirming competing options on the same space and window in the same instant resolve to exactly one booking and one clear refusal.** The refusal names the space and the window that were taken, the losing option stays readable, and the store holds one booking afterwards. The guarantee must hold in the store, not only in the interface: enforcing it in application code alone is a contract violation.
3. The contract file holds the agreed terms, the priced services, the deposit schedule and the signatures. A signed contract locks the space set.
4. Any later change to a signed contract goes through an amendment record naming who requested it, who approved it, what it moved and when. A coordinator cannot approve an amendment that same account requested.
5. Cancelling a booking releases every space it held, in one transaction, and the released window is immediately `free` to the desk, the planner, the public calendar and reporting alike.

### The event timeline and its phases

1. A booking is a span with phases, not a day. The phases are exactly `access`, `build_up`, `run`, `tear_down` and `clearance`, each with its own start, its own end, its own occupancy rule and its own accreditation profile.
2. **Every phase occupies the space exactly as the run does.** The next event cannot begin building while the previous one is still dismantling in the same hall. Treating build-up and tear-down as calendar annotations beside the booking rather than as occupancy is a contract violation: the diary looks correct and two events collide in the hall.
3. The campus timeline shows every phase of every event on one axis, one row per space, with combinations drawn across the rows they consume.
4. **The tight turnaround.** Two events sharing a hall on consecutive days are refused unless the tear-down and build-up windows genuinely fit, and the refusal names the shortfall in hours.
5. Phase changes cascade. Extending a run pushes tear-down, which may collide with the next booking's build-up; the collision is raised to a coordinator as a conflict record naming both bookings and the overlapping window, and neither booking is silently overwritten.
6. Layout build hours seed the default phase lengths, so choosing `stand_grid` over `theatre` lengthens build-up without anybody typing a number.

### Shared infrastructure on the campus timeline

1. Loading docks, freight lifts, forklifts, rigging crews and power drops are finite resources scheduled against the same timeline as the spaces.
2. Two events building at once contend for a dock. The schedule shows the contention, names both events and the window, and a coordinator resolves it by moving one; the product refuses an assignment that would double-book a resource.
3. A resource assignment carries a competence requirement where one applies, and only a person or crew holding that competence may be assigned to it.
4. Shift limits are enforced: an assignment that would breach a crew's stated working-hours rule is refused with the rule named.

### The floor-plan planner

The planner is where an event's floor plan is drawn on the venue's own geometry.

1. The canvas renders the true space geometry at scale from the space model, with structural constraints drawn as first-class objects rather than as decoration: columns, the wooden trusses and their heights, doors and their widths, fire exits and their required clearances, rigging points and their load limits, power and water positions, and the ceiling height envelope.
2. Objects placed on the canvas come from the closed set `stand`, `catering_point`, `stage`, `seating_block` and `entrance_point`. Each snaps to the plan grid, carries its own dimensions in metres, and carries the party that owns it.
3. **Live validation.** A stand that blocks a fire exit, encroaches on a required aisle width, sits on a column, or exceeds a rigging point's load limit is flagged at the moment it is placed, with the rule named in words and the offending measurement shown. A plan that validates only on save is a contract violation, because the builder has already moved on.
4. Validation runs on the objects a change actually affects rather than on the whole plan, so dragging one stand on a plan of eight hundred never stalls the canvas, and the canvas keeps panning and zooming smoothly at that size.
5. **Two planners in one plan is an expected state.** Each sees the other's presence and the other's changes within a second without reloading. Edits merge per object. An object one planner is dragging cannot be moved out from under them. Two simultaneous moves of the same object resolve to one position on both screens, and neither planner's other work is lost.
6. A plan has revisions. A revision carries a compare view against the one before it, an approval state from the closed set `draft`, `submitted`, `approved` and `withdrawn`, and the account that decided it. A planner cannot approve the planner's own revision.
7. The approved revision is the one that flows onward: to the works schedule, to the safety board's exit calculation and to the exhibitor pack. Withdrawing an approval suspends every work order that was scheduled against it rather than letting the work go ahead.

### Accreditation and its evidence

1. Every person on site belongs to a party, and the parties are exactly `organiser`, `exhibitor`, `contractor`, `venue_staff`, `caterer`, `security`, `cleaner` and `visitor`. Each is accredited per event, per phase and per space set.
2. Accreditation carries evidence where the law requires it: an insurance certificate with an expiry date, a risk assessment for the works being done, a competence record for rigging or electrical work, and an identity record for security. Accreditation state is exactly one of `pending_evidence`, `valid`, `expired` or `revoked`.
3. **An expired certificate withdraws its accreditation at the moment it expires, not at the next manual review, and every badge derived from it stops working at the same moment.** Leaving expiry to a nightly sweep is a contract violation: it passes every demonstration and leaves a withdrawn contractor holding a working badge.
4. **Delegation.** An organiser accredits its exhibitors; an exhibitor accredits its own stand contractor. A right granted downstream can never exceed the granter's own right, checked when the right is resolved rather than only when it is assigned, because the granter's rights can shrink afterwards.
5. **The cascade.** Revoking an organiser's accreditation withdraws every accreditation granted beneath it, and every badge derived from those, within a second. A cascade that runs on a schedule rather than on the revocation is a contract violation, and this is exactly where a permission model leaks.
6. A person may hold accreditations for several concurrent events from different parties. That person's rights at any instant are the union of what is currently valid, scoped to the space and the phase they are standing in, never the union of everything they have ever held.

### Badges, entrances and access control

1. Every entrance is a controlled point carrying a mode per event and per phase, from the closed set `staff`, `contractor`, `exhibitor`, `trade`, `public` and `closed`. Entrance mode is per event and per phase, never a site-wide setting: one event runs access control through a single entrance while the others stay `closed`, and another opens every entrance on its public day.
2. A badge is issued from an accreditation, is signed and time-bound, names exactly one person, and cannot be transferred.
3. A scan is evaluated against the current accreditation, the current phase, the current space rights and the current occupancy, and answers with a decision of `admitted` or `refused` within a bounded time.
4. A refusal carries exactly one reason from the closed set `no_accreditation`, `wrong_phase`, `wrong_space`, `expired_evidence`, `revoked`, `at_capacity` and `anti_passback`, and the reason is shown to the steward at the door in words.
5. **Anti-passback.** A badge that has entered and not left cannot be used again at another entrance. A stated grace window allows legitimate re-entry, and the rule may be relaxed per event by operations.
6. Every scan, admitted or refused, is appended to a log carrying the entrance, the badge, the decision, the reason and the time. The log is append-only in the store: an update or a delete against a scan row is refused there, not merely omitted from the interface.

### The degraded entrance

1. An entrance whose connection to the central system drops keeps deciding on the rule set it last held, for a stated staleness bound, and queues every scan it takes.
2. Admitting nobody while offline is unsafe in a crowd and admitting everybody is a breach. The specification requires the middle path, and the stated bound is what makes it defensible.
3. Offline tolerance ends at reconnect, and reconciliation is the price of it: the queued scans reconcile in order. A revocation issued while the entrance was offline takes effect at reconnect, and every scan that admitted somebody after their accreditation had been revoked is surfaced to operations as a named exception rather than swallowed.
4. The staleness bound is shown at the entrance while it is degraded, so the steward knows how old the rules they are working from are.

### Occupancy on the space graph

1. Live occupancy per space is derived from entrance and internal scans and compared continuously against the licensed capacity of that space or combination in its current layout.
2. **Occupancy is a graph problem, not a counter.** A person admitted to a combination is present in every constituent hall. Somebody walking from one joined hall into the next through the boulevard has not arrived twice. Counting per door is a contract violation: it overstates occupancy and closes a hall that is not full, and it fails only once a joined hall is busy, which is the day it matters.
3. Occupancy state is exactly one of `clear`, `approaching` or `at_limit`. `approaching` raises an alert on the safety board. `at_limit` closes admission to that space while leaving every exit free.
4. Occupancy recomputes per scan rather than by recounting the whole campus, and the safety board shows the new figure within a second of a scan.
5. Occupancy figures are integers. A space is never reported at a fractional occupancy and never at a negative one.

### Exits, incidents and evacuation

1. Each space's licensed figure is bound to the exits available in the current approved plan. An approved plan that blocks an exit reduces the licensed figure automatically, and the safety board shows the new number together with the reason and the plan revision that caused it.
2. An incident is a first-class record carrying a type, a location as a position on the floor plan, a severity, an owner, a timeline of actions and a required close-out. An incident cannot be closed without a close-out note.
3. **Evacuation overrides everything.** Declaring it opens every entrance as an exit, suspends admission across the campus, publishes muster information to staff surfaces and freezes the access log for the investigation. Nothing anywhere in the product may prevent an exit while evacuation is declared, including a badge refusal, an occupancy limit or an expired accreditation.
4. Declaring and standing down evacuation are both written to the audit trail with the account and the time, and the frozen log stays readable while frozen.
5. The regime is auditable end to end. Every capacity change, plan approval, incident, evacuation declaration and drill is appended to the trail with the actor, the time and the before and after values, because the venue holds a sustainability and safety charter awarded ten consecutive years and publishes a safety manual against it.

### Services, catering and technical orders

1. The venue sells services alongside the space: catering from receptions through walking dinners to the self-service exhibition restaurant, technical services covering power drops, rigging, lighting, sound and internet, plus furniture, cleaning, waste, signage and parking allocations.
2. Each service carries a unit, a price in integer minor units, a lead time and an order cut-off expressed relative to a named event phase.
3. Some services carry dependencies. A rigging order requires an approved plan revision. A power drop requires a position on that plan. An order whose dependency is not met is refused, with the missing dependency named.
4. Ordering after the cut-off is possible only with a surcharge and an approval. Both are recorded on the order, and the order state moves to `late_ordered`. Service order state is exactly one of `draft`, `ordered`, `late_ordered`, `cancelled` and `delivered`.
5. Catering orders carry a headcount with its own confirmation deadline, dietary requirements, service times tied to the run phase, and delivery points that are positions on the approved floor plan.
6. An exhibitor orders for that exhibitor's own stand, within the organiser's rules, which may cap spend, restrict suppliers or require the organiser's approval. The organiser sees the aggregate across every stand; the exhibitor sees only its own.

### Invoicing and settlement

1. A booking accrues charges from the space hire, the phase durations, the services ordered, the consumption metered during the event covering power, water, waste and cleaning hours, and any late-order surcharges.
2. Money is held and computed in **integer minor units** of `usd` throughout. Value-added tax is applied per line by rule, and the rounding decision is recorded on the line, so lines sum exactly to the invoice total with no residue.
3. Deposits and stage payments follow the contract schedule. The final invoice reconciles the estimate to the actual with every variance attributable to a named cause.
4. An exhibitor's own charges are billed to the exhibitor. The organiser sees the summary of them and never the exhibitor's own payment records.
5. Damage and cleaning charges arising from the tear-down inspection are raised with the inspection evidence attached and carry a dispute path with a recorded outcome.
6. An invoice export to the accounting interface is idempotent: a retried export never produces a second invoice for the same booking.

### Publishing to the public site

1. An event carries a publication state, exactly one of `private`, `announced` or `published`, together with a publication date. Nothing reaches the public site before that date, so a client's unannounced booking occupies the diary and is invisible to every public surface.
2. The public fields are an explicit subset: title, description, dates, public times, status, sector, the halls named for wayfinding, and the organiser's own links. Internal fields covering rates, contacts, contract terms, occupancy and incidents are structurally incapable of publication rather than filtered when a page renders. Filtering internal fields at render time is a contract violation: one forgotten template exposes a rate card.
3. Each public field carries per-language values with a translation state. A missing translation falls back with a visible label naming the language it is being shown in, rather than showing an empty field or silently showing another language.
4. Publishing is atomic per event and takes effect on the public site within a minute. Unpublishing removes it just as fast, because an event pulled at a client's request must actually disappear.
5. The public calendar reads the same records the operations desks book. It publishes only what is published, and a change of publication state is written to the audit trail with the actor and the time.

### The exhibitor portal

1. Exhibitors are the largest population of users and get their own surface, scoped entirely to one stand: the stand and its position on the approved plan, the exhibitor's own accreditation and badges, its service orders within the organiser's rules, its build-up slot for the loading dock, its documents covering the safety manual, the technical specification and the deadlines, and its invoices.
2. **Everything an exhibitor sees stops at that exhibitor's own stand.** A forged request naming another exhibitor's orders, position, badges or invoice is answered as not found, so the existence of the other stand is never disclosed.
3. An exhibitor requests a loading-dock slot from the slots the organiser has released, and the request is refused when the slot is already taken, naming the next free slot.
4. The exhibitor's document set is generated from the event's own records, so the technical specification an exhibitor downloads and the plan the planner works in cannot disagree.

### Works and technical scheduling

1. Work orders are scheduled against people and equipment: riggers, electricians, cleaners, forklifts and their drivers, lifts, and the loading docks.
2. A work order names the competence it requires, and only a qualified person may be scheduled to it. Scheduling a rigging order to somebody with no rigging competence is refused with the competence named.
3. A clash view shows every double-booking of a person or a machine across concurrent events, and the product refuses the assignment that would create one.
4. A work order whose plan approval is withdrawn moves to suspended rather than being carried out, and the suspension names the revision that was withdrawn.

### Reporting

1. The reports answer campus occupancy over time by space and by combination, revenue per event and per square metre per day, service attachment rates, turnaround performance against the phase model, incident rates and close-out times, accreditation compliance including expired-certificate events, and the sustainability metrics the charter requires covering waste streams, energy per event and reusable stand material.
2. Every figure derives from the ledgers rather than from a stored summary, and the same period totalled along different axes must agree exactly.
3. A report is scoped by the reader's own rights: a planner's report covers that planner's own events and nobody else's.

### Ticketing, parking and finance interfaces

1. External ticketing owns sales for public events. The product imports sold volumes for occupancy forecasting and accepts gate scan events, deduplicated against its own scans so one visitor is never counted twice.
2. Parking is allocated per event across the campus's `2500` spaces, with pre-booked allocations for exhibitors and staff, and the live count feeds the public visitor-information pages.
3. Invoices and payments synchronise to the accounting interface behind one boundary, idempotently.
4. The public site consumes the published projection through one authority and never reads an operations record directly.

### Wayfinding and the visitor day

1. The visitor plan is the same geometry as the public floor plan, rendered for a phone held in a corridor: the visitor's entrance, the halls in use for the event they came for, the catering points taken from the approved floor plan, the toilets, the exits and the route between them.
2. **It must work on the venue's worst network.** The plan and the current event's data are cached on the visitor's device on first load, the page renders fully with the network off, and a cache older than its stated freshness announces its own age rather than presenting yesterday's layout as today's. A build that needs the network to draw the map is a contract violation, because the halls are steel boxes and the signal dies inside them.
3. Live state changes what it shows. A hall closed for turnaround, an entrance switched from `public` to `staff`, a catering point marked sold out, or an incident closing a route all redraw the map within a minute of the operations change, and a closed route is never offered as a path.
4. **Accessibility is not a mode.** The plan carries a step-free route layer, and every route it draws is also available as an ordered list of written directions, because a map is unusable to a portion of visitors and the venue's own accessibility page promises otherwise.
5. Language follows the visitor rather than the venue: a visitor who arrived on the French site gets French directions.

### The annual campus plan

1. The annual view shows every hall across a year on one row each, carrying confirmed bookings, options at their ranks, the recurring anchor events that return every edition, the maintenance windows, the venue's own fair concepts and the closed periods.
2. A recurring event holds its slot across editions. A fair in its fifth edition carries a provisional hold on the same week of the next year, which ages into an option and then into a booking. Losing that hold is surfaced as a commercial event naming the fair and the week, rather than leaving a silent gap.
3. The yield view shows revenue per square metre per day for any window, so a coordinator can see what a low-value booking costs in displaced capacity before accepting it.
4. **Maintenance occupies space exactly as an event does.** A floor resurfacing in `Hall 3` holds `Hall 3` against every other hold, and cannot be booked over.
5. **Scenario planning.** A coordinator forks the annual plan, moves bookings inside the fork to test a rearrangement, and sees the conflicts and the yield difference before committing. Committing applies the whole fork atomically or fails whole. A partially applied scenario is a contract violation, because half a rearrangement is worse than none.

### The public site: home

Band order is normative and the copy is pinned in the copy deck below.

1. Hero: the display line over a full-bleed generated image with a dark scrim, two actions, and a bouncing cue inviting the first scroll.
2. Coming soon: three event cards taken from the calendar, each with its status chip, its dates, its times, its hall chips, its sector and its outbound actions, over an all-events link.
3. Visitor invitation: a banner asking whether the reader is visiting soon, the practical-information paragraph, and a plan-your-visit action.
4. Organiser invitation: the versatile-venue paragraph, the promise that the venue does not merely rent halls, the fifty-years-of-experience line, and a nine-image gallery with a lightbox.
5. The right setting: the blank-canvas paragraph with two actions, then four summary blocks covering the six halls, the meeting centre of five rooms usable separately or combined, the covered boulevard that connects all the halls and has two entrances and doubles as exhibition or catering space, and the in-house restaurant that combines self-service speed with bistro quality.
6. Inspiration: case cards, each naming the halls it used, over a more-events link.
7. Stay up to date: the newsletter invitation and the three social profiles.
8. Newsflash: news cards with a category chip, a date and a read link.
9. Footer.

### The public site: the calendar

1. Every entry is an event card carrying a generated image, a status chip reading either `Open to the public` or `Trade fair - registration required`, a title, a date or date range, a daily time range, one or more space chips naming the halls used, a sector chip, a description and its outbound actions, which are the event's own website and a ticket link where selling is external.
2. Filters cover month and date range, status, sector and hall. The filter state is carried in the address so a filtered view can be shared as a link, and the same state is reflected in the page title.
3. A multi-day event renders once with its range rather than once per day, and an event running past midnight belongs to the day it started.
4. The calendar publishes only events whose organiser has marked them published and only after the publication date. An event held in the diary for a client who has not announced it is invisible here.
5. A filter that matches nothing shows a designed empty state naming the filter that emptied it and offering to clear it, rather than an empty page.

### The public site: spaces and the floor plan

1. The page carries the interactive floor plan and, beneath it, one specification block per space naming its capacity, its floor area, its unique features and the event types it suits.
2. **The plan is drawn geometry, never an image.** It is an outline of the campus with each hall as a closed region carrying its number as a text label, the numbers running one through six plus the event hall marked `XXL`, the meeting centre, the covered boulevard connecting the halls, and the passages between adjacent halls.
3. Regions are interactive. Pointing at a region lifts it and its number. Choosing one scrolls to that hall's specification block. The plan is operable region by region from the keyboard in a stated order with a visible focus outline, and each region announces its hall's name, capacity and floor area.
4. The plan renders from the space model, so a space added in operations appears without anyone redrawing it.
5. The page closes with the flexible-combinations paragraph, the venue-team introduction, six reasons organisers choose the venue covering in-house experience, flexible spaces, bespoke catering, easy access, ample parking and end-to-end care, a case-study strip and an enquiry form.

### The public site: the rest of the organiser section

1. Meetings: the modular meeting centre, its rooms, their combinations, the audiovisual provision, the catering that accompanies a meeting, and its own contact team block.
2. Catering: the offer from receptions through walking dinners to the self-service exhibition restaurant, with the note that catering is in-house.
3. The in-house restaurant: the fast-gourmet kitchen brand, its concept and its role on busy fair days.
4. Accessibility and the region: reaching the venue by road, rail and air as an organiser, and what the surrounding region offers delegates.
5. Unique events: the case studies, each naming the spaces used and what was done with them, one page per case.

### The public site: visit

1. The visitor hub, then accessibility and parking covering routes, the parking spaces, public transport and drop-off; food and drink on site; what to do in the city; and the frequently asked questions as an accordion.
2. Visitor pages are the most-read pages during an event and must be legible on a phone in a car park: large touch targets, nothing that depends on hover, and the practical facts above the fold.

### The public site: about and news

1. About: the hub, who we are, the history of fifty years on the site, sustainability and safety, and the media kit with downloadable logos, floor plans and the safety manual behind an anchor that resolves.
2. News: an index of cards carrying category chips and dates, plus an article page per item.
3. An article published in one language and not yet translated stays visible in the other languages, labelled as available in another language, rather than being silently omitted.

### The public site: contact, legal and not-found

1. Contact: the enquiry form carrying a first name, a last name, an email, the kind of event being organised, the date range, the expected visitor count and the spaces of interest. Submitting it creates an enquiry in the product and the form states what happens next.
2. Legal: the general conditions, the privacy policy and the cookie policy, each dated and set in the reading column, with the cookie policy generated from the consent declaration rather than hand-written.
3. The not-found route is a designed screen offering a route home and a search field, not a bare error.

### Consent, cookies and the page-view record

1. A consent banner gates a statistics category and a marketing category, over a necessary category that cannot be refused. Refusal is honoured: nothing in the statistics or marketing categories loads until consent is given, and withdrawing consent stops it from then on.
2. The consent record carries an identity and a date, and the cookie policy page lists every cookie by provider, purpose, retention and type, generated from the same declaration the banner enforces.
3. A page view is recorded for each public route request, carrying the route, the language and the time, and never carrying an identifier for the person. The page-view record is what the statistics category governs: with statistics refused, no page view is recorded at all.
4. The reporting surface shows page views per route and per language over a window, and the figure agrees with the page-view records exactly.

### Search, the newsletter and the language switcher

1. A search control opens a full-width overlay with one field labelled `Search entire website`, and searches page content, event titles and news across the language the visitor is reading in.
2. A search that matches nothing offers the calendar and the spaces page rather than a dead end.
3. The newsletter capture takes an email address and answers with exactly one state from the closed set `sent`, `invalid` and `already`. The same address twice answers `already` rather than creating a second subscription.
4. **The language switcher preserves the current page and its parameters.** Switching language on a hall page lands on the same hall in the new language, and switching language on a filtered calendar keeps the filter. Returning the reader to the home page is a contract violation.
5. Every route exists under all three language prefixes, and each page declares the language it is written in.

### The not-found route

1. An unknown address under any language prefix is answered as not found with the designed screen, in the language of the prefix it was asked for.
2. The screen carries a route home and a search field, and the internal links on it resolve.

## User flow

### Routes

`LANG` is one of `nl`, `fr` or `en`, and every public route exists under all three.

| Route | Purpose | Auth |
|---|---|---|
| `/LANG` | home: hero, upcoming events, visit and organise invitations, hall summary, inspiration, newsletter, news | none |
| `/LANG/calendar` | the events calendar with its filters | none |
| `/LANG/visit` | visitor hub | none |
| `/LANG/visit/accessibility-parking` | how to reach the venue and park | none |
| `/LANG/visit/food-drinks` | eating and drinking on site | none |
| `/LANG/visit/what-to-do-city` | the surrounding city | none |
| `/LANG/visit/frequently-asked-questions` | visitor questions as an accordion | none |
| `/LANG/organize` | organiser hub | none |
| `/LANG/organize/spaces` | the floor plan and every space's specification | none |
| `/LANG/organize/meetings` | the modular meeting centre | none |
| `/LANG/organize/catering` | the catering offer | none |
| `/LANG/organize/orangery-kitchen` | the in-house restaurant brand | none |
| `/LANG/organize/accessibility-region` | reaching the venue as an organiser | none |
| `/LANG/organize/unique-events` | the case studies | none |
| `/LANG/organize/unique-events/:case` | one case study | none |
| `/LANG/about` | about hub | none |
| `/LANG/about/who-are-we` | the team and the venue | none |
| `/LANG/about/history` | fifty years of the site | none |
| `/LANG/about/sustainability-safety` | the charter and the safety regime | none |
| `/LANG/about/media-kit-documents` | logos, plans and the safety manual | none |
| `/LANG/news` | news index | none |
| `/LANG/news/:article` | one article | none |
| `/LANG/news/newsletter` | newsletter subscription | none |
| `/LANG/contact` | contact and enquiry | none |
| `/LANG/general-conditions` | the general terms and conditions | none |
| `/LANG/privacy-policy` | the privacy policy | none |
| `/LANG/cookies` | the cookie policy, generated from the consent declaration | none |
| `/LANG/search` | search results for a query string | none |
| `/LANG/wayfinding/:event` | the visitor plan for one event, usable with the network off | none |
| `/robots.txt` and `/sitemap.xml` | the crawler contract | none |
| `/signin` | sign in | none |
| `/console` | the campus calendar, the console home | any signed-in principal |
| `/console/enquiries` | the enquiry desk | `coordinator` |
| `/console/options` | the option and challenge desk | `coordinator` |
| `/console/bookings/:id` | one booking file: phases, contract, services, exhibitors | `coordinator`, `finance`, and the owning `planner` |
| `/console/plans/:id` | the floor-plan planner | `coordinator`, the owning `planner` |
| `/console/accreditation` | parties, evidence, delegation and revocation | `coordinator`, `operations`, the owning `planner` |
| `/console/access` | entrance modes, badge issue and the scan log | `operations` |
| `/console/safety` | occupancy, alerts, incidents and evacuation | `operations` |
| `/console/works` | the works and resource schedule | `operations` |
| `/console/services` | the service and catering order desk | `coordinator`, the owning `planner` |
| `/console/invoices` | invoicing and settlement | `finance`, `coordinator` reads |
| `/console/publish` | the public-content desk | `coordinator` |
| `/console/annual` | the annual campus plan and its scenarios | `coordinator` |
| `/console/reports` | reporting | any signed-in principal, scoped to their own rights |
| `/console/audit` | the append-only audit trail | `auditor` |
| `/portal` | the exhibitor's own stand, orders, badges, dock slot and invoices | `exhibitor` |
| `*` | the designed not-found screen | none |

### Entry and redirects

An anonymous caller opening any `/console` or `/portal` route is served `/signin` with the requested address remembered, and lands on it after signing in. Signing in with no remembered address lands a `coordinator`, `finance` and `auditor` on `/console`, an `operations` account on `/console/safety`, a `planner` on `/console` and an `exhibitor` on `/portal`. Signing out returns to the language home the reader last used and stops the token working at once. A token that expires mid-action leaves the work on screen and offers sign-in in place. A signed-in principal opening a route their role does not hold is told plainly that the surface is not theirs, with a route back to one that is; they are never shown an empty version of it.

### Journeys

1. **Hold, challenge, confirm.** Sign in as `coordinator@example.com`. Open the enquiry desk, open the seeded enquiry from `Palmarosa`, and place an option on `Hall 4`, `Hall 5` and `The Transit` for the seeded window at rank one. Place a second option on the same set and window at rank two for `Bookmark Fair`. Challenge from rank two; the rank-one holder is notified and the challenge window starts. Confirm the rank-one option. The rank-two option is released with a notification naming the space set and the window, the booking exists with its five phases, and the campus timeline shows the hall rows occupied across build-up, run and tear-down.
2. **The combination blocks its parts.** Still as `coordinator@example.com`, open the campus calendar and ask for `Hall 4` alone in the window just booked. The answer is `blocked_by_ancestor` naming the combination, not `free`.
3. **Draw the plan and break a rule.** Sign in as `planner@example.com`, open the plan for the confirmed booking, place a stand across a fire exit, and see it flagged the moment it lands with the rule named in words and the clearance measurement shown. Move it clear, submit the revision, and watch approval move it to `approved`.
4. **The badge dies with the certificate.** Sign in as `operations@example.com`, open accreditation, and see the seeded contractor whose insurance certificate expires inside the seeded window. Advance past that expiry; the accreditation reads `expired` and a scan of its badge at `North Entrance` is refused with the reason `expired_evidence`.
5. **The cascade.** As `coordinator@example.com`, revoke the organiser accreditation of `Bookmark Fair`. Every exhibitor and contractor accredited beneath it reads `revoked` within a second, and their badges stop working.
6. **The exhibitor's wall.** Sign in as `exhibitor@example.com`, open `/portal`, see stand `S-118` and its position, its orders and its invoice. Ask the API for another exhibitor's stand and receive not found.
7. **The public half.** With no session, open `/en/calendar`, filter to `Hall 5`, copy the address and open it in a fresh window: the same filter is applied. Switch the language to `fr` and stay on the filtered calendar. Open `/en/organize/spaces`, tab to `Hall 5` on the floor plan, hear its name, capacity and area announced, and press it to reach its specification block. Confirm the privately held event is nowhere on the calendar.

### States

Every list surface carries a designed empty state naming its one next action: a hall with no holds in the window, an event with no exhibitors yet, a plan with no objects, an accreditation list awaiting evidence, an entrance with no scans, a safety board with no incidents, a works schedule with no orders, an invoice with no lines, a report with no rows and a calendar filtered to nothing. An empty state that renders nothing is an unfinished screen. Every page has a loading state and every list a skeleton that reserves the space its rows will take, so nothing jumps when they arrive. Refused, empty, loading, degraded and error are five different states and they look and read differently: a space nobody may see and a space with nothing in it must never render the same way. An error anywhere is caught, stated in words and recoverable, and never replaces the page with a stack trace.

## UI/UX notes

The north star for the public site: somebody arriving should understand within one screen that this is a large, working building with a team behind it, and should feel invited rather than sold to. The north star for the console is plainer and it is comprehension: which square metres are held, by whom, until when, and whether the building is safe right now.

Two registers in one product, held apart on purpose. The public site is a consumer and editorial surface that may carry atmosphere, and the subject, the building and what happens inside it, is the first thing seen. The console is an operational tool: quiet, utilitarian, dense but organised, restrained and predictable, built for scanning and for the same action forty times a day, with no oversized heroes, no editorial composition and no decoration standing in for content. Comprehension over atmosphere inside the console; warmth over neutrality outside it.

The public field is a plain near-white neutral ground. One mid, vivid red is the brand: it carries primary actions, links and accents and it is the only thing on a page wearing it. A deep, muted red carries every line of body text, which is what stops the page reading as black ink on white and is the single most recognisable thing about the palette. A light, vivid red is the hover and secondary accent, the tone the venue's own team calls its coral, with a slightly deeper sibling for the pressed state; the same light red held at a low single-figure tenth of full opacity, roughly nineteen percent, is the tertiary wash that carries selection and soft fills and appears in no other role. Three neutrals below the ground carry secondary text, tertiary text, and the hairlines and dividers, each a step lighter than the one before, and a mid, soft red carries validation failure over a near-white warm neutral wash that appears in no other role. Two support washes carry meaning in the calendar and in notices and appear nowhere else: a near-white, soft orange and a near-white, muted red. The exact shades are yours, so long as the brand red is exclusive to action, the deep red is exclusive to reading, and a state that is none of the three meanings borrows none of their colours.

The console redefines those roles for a working surface and leaves their meanings alone: a panel sits a shade above the page, a recessed well a shade below, and a hovered panel a shade above again, so a panel reads as separate without needing a border. Occupancy has three states and each carries its own tone, and none of the three is ever signalled by colour alone: every one carries a word.

One family does everything, a variable geometric sans across a wide weight range with roman and italic and a metrically matched system fallback, plus a drawn stroke icon set. Headings read as titles through size and weight rather than through a second family, figures line up in a column wherever capacities, areas and amounts stack, and the dense interface band sits a step below body copy so a full campus row fits one screen. Type is the one place this brief gives you values rather than intent, and the scale is in the front-end specification.

Depth is restrained. Hairline borders and dividers in the lightest neutral do most of the work, one soft shadow lifts a raised card, a slightly stronger one lifts an overlay, and imagery runs full bleed behind a dark scrim. Corners are barely softened on a short ladder, and the only fully rounded shape in the product is the small status marker, so a chip never reads as a button.

Motion is one gesture rather than nine. Everything that moves moves on a single decelerating settle, quick to leave and slow to arrive, at one speed that is quick enough not to be waited for and slow enough to be seen. Section content rises and fades as its band enters the viewport, once per band, and then stays arrived. A downward cue bounces gently under the hero, inviting the first scroll. A single element that needs attention settles with a small rotation rather than flashing. Carousels slide horizontally and vertically in matched pairs, the lightbox crossfades and its images arrive very slightly undersized before settling to true size, a scaling bar carries carousel and gallery progress, and loading states rotate. Nothing uses a different speed to feel special. **Stillness is the default, not an option:** motion is enabled only where the reader's device asks for it, so the reduced state is what the product does unless told otherwise, and in that state no reveal, bounce, settle or slide animation runs at all, content renders in place, and carousels change slides instantly while every state change stays instantaneous rather than merely faster.

Density is the register's tell. The public site is spacious, with the gap between bands several times the gap beneath a heading and roughly halving on a narrow screen, every gap a multiple of one base unit that is yours to choose, and the rhythm scaling smoothly with the window rather than jumping at fixed sizes. The console is compact: rows sit tight so a full week of a hall fits one screen, hit areas stay large, positions stay stable between loads, and chrome stays minimal.

Accessibility is a floor, not a preference. Text, interface components and the focus indicator meet WCAG AA contrast, in both the public and the console surfaces. Touch targets are at least 44 by 44 device-independent pixels, and body text never falls below 16 pixels on the public site. Every interaction is reachable by keyboard navigation with a visible focus ring that survives a high-contrast setting, every icon-only control carries an accessible name, and meaning is never carried by colour alone. Four surfaces need their own answer and get one: the floor plan, whose regions are focusable in a stated order and each announce their hall's name, capacity and area; the campus timeline, which announces the space and the window a row represents rather than only drawing it; the safety board, whose alerts are announced as well as coloured; and overlays, which move focus in, hold it and return it where it came from.

Responsive behaviour is two problems rather than one. The public site reflows to a narrow viewport in all three languages, and **the longest language decides the layout**: navigation labels, chips and buttons must not wrap or truncate in the wordiest language, and the arrangement is checked in that language rather than in the shortest one. The floor plan on a phone becomes a pannable, pinch-zoomable region list carrying the same keyboard and announced semantics, and every hall's specification stays reachable without the plan. Calendar filters collapse into a sheet and event cards stack while keeping the status chip, the dates and the hall chips visible. The console is desktop-first and says so, but three surfaces must work on a phone because they are used on the floor: access control, the safety board and incident raising, each specified for gloved, one-handed use with large targets and high contrast under bright light.

## Front-end specification

This section carries the visual specification in full. Nothing here restates a rule stated above; where a rule appears above it is not repeated here.

### Ground, spacing and the grid

The layout is checked at three widths: a wide desktop, a small tablet and a phone. Spacing is fluid by design rather than stepped. Four rhythm steps exist, a tiny one, a small one, a default one and a large one, each interpolating smoothly with the viewport width between a lower and an upper bound, each bound roughly half as far again as the step below it. Section padding uses the same ladder, so vertical rhythm is one system rather than a set of magic numbers, and flattening the ladder to fixed values produces a page that is correct at one width and wrong everywhere between.

The breakpoint ladder is unusually tall and it is deliberate: a phone tier, a large-phone tier, a small-tablet tier, a tablet tier which carries by far the most rules and is where the navigation collapses, a small-desktop tier, a desktop tier, a wide tier and a very wide tier, with a small number of narrow overrides below the phone tier and a stated maximum width for the reading column on the legal pages. The exact widths are yours; carrying the whole ladder is not, because a two-breakpoint build holds at two widths and breaks between them.

Motion is gated **positively** on a preference for movement rather than negatively on a preference against it, so stillness is what the product does by default. Hover styling sits behind a pointer-capability branch rather than a width branch, so a touch device never inherits a hover treatment it cannot leave.

The stacking order is a closed, named ladder and nothing may sit outside it: an ambient backdrop behind the page, then base content, then raised content, then a sticky bar, then the overlay range carrying modals, the consent dialog and the lightbox, then the skip link above everything. The overlay range is a named token at the top of the product's own ladder, and no element may compete with it by choosing an arbitrarily large number, so nothing can ever silently cover the safety board or the evacuation banner.

### Colour, in three layers

Layer one is the raw ladders: one neutral ladder running from the near-white page ground down through three greys to the hairline tone, and one brand ladder running from the deep, muted red of body text through the mid, vivid red of action to the light, vivid red of hover, plus the two support washes and the validation pair. Every value in the product comes from those ladders.

Layer two is the semantic roles, each named for its job rather than for its colour: the page ground, a raised panel, a recessed well, a hovered panel, body text, secondary text, tertiary text, inverted text on a dark scrim, the link colour, the link hover colour, the hairline, the selection wash, the scrim over full-bleed imagery, and the four state roles covering failure, success, in-progress and neutral information. The console redefines layer two and leaves layers one and three untouched, which is the whole reason the layers are separated.

Layer three is the per-component state set, and it is the layer that makes the interface read as considered rather than assembled. Every interactive component declares its full set rather than deriving hover by dropping opacity. At minimum: the solid primary button, the outline button, the text button, the navigation item with default, hover, active and inactive states, the status chip in each of its meanings, the form field with default, hover, focused, invalid and unavailable states, and the floor-plan region with default, hover, focused and selected states. Unavailable is never signalled by colour alone.

### Typography

One variable geometric sans carries everything, with a full weight axis from the very lightest to black, roman and italic, and a metrically matched system fallback declared after it so the swap does not move the layout. `Inter` is the family this build ships, loaded from a hosted service with a stated swap behaviour and subset to the characters the three languages need. No licensed typeface file ships.

The rendered scale, each step with a job: body copy at 16px on a 24px line, the dense interface and card band at 15px on a 24px line at regular, semibold and bold, fine print at 14px on a 21px line, micro-labels at 12px on a 14.4px line, card titles at 20px on a 30px line, compact heads at 18px on an 18px line, and a fluid display ladder that interpolates with the viewport rather than stepping. Line height is generous at body sizes, tight at caption sizes and equal to the type size itself at display sizes. Tracking tightens as size grows and opens as size shrinks. Figures are tabular wherever capacities, areas, occupancy counts or money stack in a column.

### Iconography, marks and the floor plan

The wordmark is drawn geometry set on a wide, short box, reproduced as drawn letterforms rather than as a font glyph, and it always carries an accessible name.

Interface glyphs are a drawn stroke set on a square box inheriting the current text colour, never an icon font. An icon font is a graded defect here rather than a style choice: it fails when the font fails, it is announced as a letter by assistive technology, and it cannot inherit two colours. The set is small and closed: chevron, arrow, close, search, menu, calendar, location pin, clock, download, external link, plus the three social marks. Each glyph carries a title where it is meaningful and is hidden from assistive technology where it is decorative.

The floor plan is a single piece of inline geometry on one wide, tall box, drawn as closed regions rather than as an image, with the campus outline, each hall, the event hall, the meeting rooms, the covered boulevard and the passages as sibling regions, and each hall's number as a text label positioned inside its own region. A second, decorative piece of drawn geometry carries the page's angled background form. The plan's regions are the space model made visible, so they are generated from the space records rather than hand-drawn, and a hall's region cannot show a hall the building does not have.

Event status chips and sector chips are pill labels carrying words. Colour never carries the status alone.

### Global chrome

**The header** carries a slim utility strip above the main bar. The strip holds the jobs link, the parent group link and the three language codes. The main bar holds the wordmark at the leading edge and six primary items: `Calendar`, `Visit`, `Organize`, `About Verwick Xpo`, `News` and `Contact`. Three of those, `Visit`, `Organize` and `About Verwick Xpo`, open a panel of child links. A search control opens a full-width overlay with one field. Below the tablet tier the whole navigation collapses into a single sheet that keeps the same order and the same language codes, and a submenu inside it is a push with a back control rather than an expand.

**The footer** carries the wordmark, the sustainability charter mark, the copyright line and four legal links: `General terms & conditions`, `Safety manual`, `Privacy policy` and `Cookie Policy`. The safety manual link points at the media kit page's document anchor, which is a real anchor and must resolve. Beneath them sit the newsletter invitation and the three social profiles.

**Breadcrumbs** appear on every inner page and name the path the reader took.

**Buttons** come in three treatments sharing one geometry: solid in the brand red for the one loud action per view, outline for its quieter companion, and text with a trailing arrow inline in copy. Every treatment carries resting, pointed-at, pressed, focused and unavailable states.

**Shared furniture** beyond the buttons: carousels for galleries and case studies with keyboard controls and honest pagination that reports the real count; accordions for the questions page; a lightbox for gallery images that traps focus and returns it; and a newsletter capture band.

**The consent dialog** sits in the overlay range, traps focus while it is open, and cannot be dismissed into acceptance: closing it without choosing leaves the optional categories refused.

### Route compositions

The home route is the band order given above. The calendar is a filter rail over a card grid that becomes a sheet and a stack on a narrow viewport. The spaces route is the plan over the specification blocks, one block per space, each carrying `Capacity`, `Surface area`, `Unique features` and `Suitable for` as labelled fields. The visit and about routes are a reading column with a lead image and a contents rail. The news index is a card grid with category chips; an article is a reading column with a dated header. The legal routes are a reading column with a visible date and no decoration. The contact route is the form beside the practical details. The not-found route is the designed screen with a route home and a search field. The console routes are a persistent desk rail, a working surface and a contextual panel, with the campus timeline as the console home.

### Motion, in detail

One easing carries the whole product, a strong decelerating settle, and one default duration carries almost every transition. There is no second easing anywhere: a component that eases differently from its neighbour is the defect this rule exists to prevent. The named moments, each of which must exist and none of which needs a number:

- **Scroll reveal.** Section content rises a short distance while fading in as its band enters the viewport, once per band, then stays arrived.
- **Hero cue.** A downward marker translates a short distance and back, continuously and gently, inviting the first scroll.
- **Attention settle.** A single element rotates a few degrees and settles back, used to draw the eye to one thing and never to more than one at a time.
- **Carousel slides.** Horizontal and vertical slide-in and slide-out pairs, offset by the carousel's own gap so a slide never appears to jump its track.
- **Lightbox zoom.** An image enters scaling up from very slightly undersized while rising a short distance, and leaves the same way, with a throw-out variant on dismissal.
- **Progress.** A bar that scales from nothing to full carries carousel and gallery progress.
- **Loading.** A rotation loop carries every loading state, at one speed everywhere.
- **Live change.** A row on the campus timeline or the safety board that changes under the reader is marked briefly rather than silently replaced, so a figure that moved is visible as having moved.

Under the reduced state, which is the default, none of the reveals, cues, settles, slides or zooms run. Content renders in place, carousels change slides instantly, the progress bar jumps to its value, and the live-change marker becomes a static marker rather than a fading one, because the requirement is to see that something changed, not to watch it change.

### Responsive and the longest language

Every string in the chrome, the chips and the buttons is checked in the wordiest of the three languages, and the layout holds there. The campus timeline scrolls horizontally on a narrow viewport while its space column stays pinned, so a reader always knows which row they are on. The three floor surfaces, access control, the safety board and incident raising, are laid out for one hand and a glove: targets well above the minimum, controls within reach of a thumb, and contrast that survives direct sunlight.

### Assistive technology and document structure

Each view declares one main landmark, a banner landmark, a contentinfo landmark and navigation landmarks labelled individually where there is more than one. Each view carries exactly one first-level heading and skips no level below it. Every control carries an accessible name, and where a control has a visible label the accessible name matches it. Each document declares its own language, and any element written in a different language declares its own. Every route carries a unique title leading with the specific page and ending with the product name, plus a meta `description`. A visible skip link is the first focusable thing on every page.

Live regions announce the four things that change without the reader acting: a scan decision at an entrance, an occupancy state change, a plan validation failure and a save outcome.

### The copy deck

Every string below appears verbatim, in the English rendering. All three languages carry the same strings translated, and the English set is the one pinned here.

**Chrome.** Utility strip: `Jobs`, `Northtide Venues Group`, `nl`, `fr`, `en`. Main navigation: `Calendar`, `Visit`, `Organize`, `About Verwick Xpo`, `News`, `Contact`. The `Visit` panel: `Accessibility & parking`, `Food & drinks`, `What to do in Verwick`, `Frequently Asked Questions`. The `Organize` panel: `Spaces`, `Meetings`, `Catering`, `The Orangery`, `Accessibility & region`, `Unique events`. The `About Verwick Xpo` panel: `Who are we?`, `History`, `Sustainability & safety`, `Media kit & documents`. Search field label: `Search entire website`. Footer: `(C) 2026 Verwick Xpo`, `General terms & conditions`, `Safety manual`, `Privacy policy`, `Cookie Policy`, `Subscribe to the newsletter`, `Follow us`, and the three social profiles `Instagram`, `LinkedIn`, `Facebook`. Skip link: `Skip to main content`.

**Home.** Hero: `when ideas need space`, with the actions `View our calendar` and `Organize your event`. Upcoming: `Coming soon to Verwick Xpo` over `All events`. Visitor band: `Are you visiting Verwick Xpo soon?` and `Great, we look forward to welcoming you! Click through for all practical information on parking, accessibility, accommodation and answers to frequently asked questions. That way, you don't have to worry about anything and can make the most of your visit.` with the action `Plan your visit`. Organiser band: `Your next event at Verwick Xpo?` and `Verwick Xpo is a versatile event venue in the western province to host conferences, corporate events, trade shows, meetings and other events.` followed by `A unique idea deserves the right location. We don't just rent out our event halls. We are happy to think along with you and explore the possibilities together. This way, we create the ideal setting for your trade fair, conference, event or meeting. Thanks to our modern facilities and 50 years of experience, we bring your big or small plans to life down to the finest details. Our team takes care of everything from A to Z, whether it's catering, ticketing, parking, technical support or safety.` Setting band: `when ideas need space` over `The right setting for every concept` and `From an intimate reception to a large-scale corporate event. From a niche trade fair to a well-attended public event. From a strategic meeting to an inspiring conference... Our venue is a blank canvas of nearly 40,000 m2 where (almost) anything is possible, as long as you dare to dream.` with the actions `Organize in Verwick Xpo` and `Discover the halls`.

The four building blocks, each a heading over its paragraph: `6 halls: versatility at its best`; `Meeting center: 5 rooms, endless possibilities`; `The Concourse: covered boulevard`, whose paragraph states that it connects all the halls, is the beating heart of the venue, has two entrances and doubles as additional exhibition space or catering area; and `The Orangery: Fast Gourmet Kitchen`, whose paragraph states that it combines the speed of self-service with the quality of a bistro.

Inspiration: `Get inspired` over `Get inspired by a selection of events recently held at Verwick Xpo.` with `More unique events`. Newsletter: `Stay up to date` with `Subscribe to the newsletter` and `Follow us`. News: `Xpo Newsflash` over `Curious about our latest news? We take you behind the scenes at Verwick Xpo.` with `All newsflashes`.

**Spaces.** `Flexible halls and rooms` over the paragraph about a versatile offer of halls, party rooms and meeting rooms that can be arranged entirely to the client's wishes. The actions `View the floor plan`, `Start your request` and `Get inspired`. The plan carries the regions `1` through `6` plus `XXL`. Then one specification block per space, each with the labelled fields `Capacity`, `Surface area`, `Unique features` and `Suitable for`:

| Space | Capacity | Surface area | Unique features | Suitable for |
|---|---|---|---|---|
| `Hall 1` | `up to 1,620 visitors` | `6,090 m2` | the oldest hall, characteristic wooden trusses giving a vintage look, wooden columns | trade fairs and conferences |
| `Hall 2` | `up to 1,740 visitors` | `4,058 m2` | elongated, in the same style as Hall 1, wooden trusses worked into the ceiling | trade fairs, conferences, performances |
| `Hall 3` | `up to 1,680 visitors` | `3,601 m2` | the smallest hall, characteristic yellow grid ceiling, yellow tube structure, riggable | trade fairs and events |
| `Hall 4` | `up to 3,660 visitors` | `7,685 m2` | the largest and most recent hall, a black box | not captured |
| `Hall 5` | `up to 5,160 visitors` | `4,723 m2` | a square black box, excellent for events and parties, acoustic panels | parties, club nights, trade fairs |
| `Hall 6` | `up to 1,860 visitors` | `5,055 m2` | the same style as Hall 3 but considerably larger | trade fairs, conferences, events |
| `The Event Hall` | `up to 2,000 people` | `2,000 m2` | the newest event hall, suitable for any reception or conference, a tribune seating 550 | parties, receptions, conferences, seminars |
| `Meeting Centre` | `four combinable MC rooms beside the event hall` | `1,679 m2 total` | modular, its own entrance, a terrace with garden | meetings and receptions |

`Hall 4` carries no suitability line, and the field reads `not captured` rather than inventing one.

Then `Flexible combinations tailored to you` with its paragraph; `Say hi to the Venue team` with the proactive-support paragraph and `Contact us`; `Why do organizers choose Verwick Xpo?` with its six reasons, `In-house experience`, `Flexible spaces` carrying `6 flexible halls and 5 modular meeting rooms`, `Bespoke catering`, `Easily accessible` as a congestion-free location, `Ample parking` carrying `2,500 parking spaces`, and `End-to-end care`; then `The spaces in use` with the case strip.

**The case studies, verbatim.** The architecture trade event: `an exclusive, high-end trade event aimed at (interior) architects, engineers and specifiers, with a strong focus on product innovations. They make use of Hall 4, Hall 5, and the convenient passage between them, the Transit.` The interior-sector corporate event: `Hall 3 was transformed by event agency Palmarosa into a stunning and unique corporate event. More than 900 guests enjoyed live performances and acts while savoring a walking dinner provided by our in-house catering. Mobile catering points were installed throughout the hall. The spacious South entrance was used for access control.` The book fair: `Bookmark Fair has now been held in Verwick Xpo for 5 editions! They use Halls 1, 2, 3 and 6 for the fair and the children's play area. The MC rooms and the XXL serve as the setting for book signings, presentations and interviews. Visitors can easily find their way thanks to the direct connection between all the spaces used.`

**News fixtures.** The corporate item `Calderhook Group completes acquisition of Northtide Venues Group`, dated `03.08.2026`, whose body states that the deal creates opportunities for expansion and continued growth among specialist event communities by leveraging complementary capabilities. The sustainability item `Verwick Xpo achieves the Westmark sustainability charter for the 10th consecutive year`, dated `07.07.2026`, whose body describes recognition for companies integrating sustainable enterprise into daily operations through concrete actions and objectives. That second item ships with its body in its original language under an English heading, because that is how it was published, and it is the fixture the translation-state rule exists to handle.

**Status and sector chips.** The two status chips read `Open to the public` and `Trade fair - registration required`. The seeded sector chips read `Architecture & Design`, `Lifestyle & Sports` and `Sustainability`.

**Not-found.** The screen carries `Page not found`, the action `Go to homepage` and a search field carrying the same label as the header's.

### Generated assets

No binary asset ships: no typeface file, no photograph, no icon file, no texture, no video and no logo file. Everything is generated, drawn inline or rendered procedurally.

- **The floor plan** is inline geometry generated from the space model, never an exported image.
- **Photography** for the hero, the galleries, the hall images, the case studies, the news and the team is a seeded procedural composition per subject: layered gradient fields in the brand palette under a soft scrim and the standard card treatment, each carrying its caption and its alternative text, seeded from the subject's own slug so the same subject always renders the same composition and a grid of cards reads as one family. The gallery lightbox shows the same generated composition at a larger size.
- **The wordmark, the charter mark and the social marks** are drawn geometry. The icon font is replaced by the drawn stroke set.
- **The media-kit documents**, the logo pack, the floor plans, the safety manual and the technical specification, are generated at build time from the space model and from this specification, so the plan a contractor downloads is the plan the planner uses and cannot be an out-of-date copy.
- Every image element declares its dimensions in the markup so nothing shifts when it renders, and every one carries alternative text describing its subject rather than naming its file.
- A `favicon` is served, and every route carries a title and a meta `description`.

## Technical requirements

The browser receives a static production bundle on first paint and every subsequent fact arrives as JSON from the same origin under `/api`. The backend is **NestJS** on Node 20, serving that JSON API. The frontend is **Vue 3** built by **Vite** into the production bundle. The datastore is **PostgreSQL**, reached at `DATABASE_URL`. Authentication is implemented by the app itself: email and password, hashed passwords, bearer tokens on every request except sign-in, `GET /api/health` and the unauthenticated public endpoints. `GET /api/health` returns `200` once the app is ready.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor: the only backing service available in this environment is PostgreSQL, and reaching for anything else is a contract violation.

The backing service above is **already running** at that environment variable. It must not be downloaded, installed, compiled or started. Never hardcode a host or a port; read every one of them from the environment, including `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`.

**One authority per question.** Exactly one part of the product answers whether a space is free in a window, and the enquiry desk, the planner, the public calendar, reporting and every interface ask it. Exactly one part answers how many people are inside a space, and the safety board, the access decision and the public capacity display ask that one. A second implementation of either is a contract violation, and it is observable: two surfaces that disagree about the same hall in the same second are the symptom.

**Pure, fixture-testable modules.** The floor-plan geometry, the overlap resolver, the accreditation evaluator, the tax calculator and the phase-fit calculator are separable units that take inputs and return answers with no reach into request state, so each can be exercised against fixed inputs and produce a fixed answer.

**Enforcement lives in the store.** Overlap, licensed capacity, accreditation validity, publication scope and the append-only property of the trail are enforced where the data lives, not only in application code. A request crafted to bypass the application layer must still fail. This is the difference between a rule and a habit.

**Liveness.** Holds, phase changes, plan revisions, scans, occupancy figures and incidents reach every open surface within a second of the change, without the reader reloading the page, and entrances additionally hold their own cached rule set for the degraded case. A burst of scans when a hall opens its doors is batched so the console does not degrade, and the arrival of one thousand scans in a minute must not make the safety board unresponsive.

**Schema and rule evolution.** The space model, the layout capacities, the licence figures and the accreditation rules all carry versions, and every booking, plan revision, badge and invoice records the version it was written under. History reads at its own version; only bookings made afterwards inherit a revised figure. Migrations are forward-only and run once.

**Performance bounds and their reference conditions.** Every bound is stated against a four-year-old mid-range laptop, a deliberately slowed connection, a campus year carrying five hundred bookings, a floor plan of eight hundred objects and an access log of one hundred thousand scans. A bound without its conditions is a wish.

- The public calendar renders a year of events with filters applied in under a second, from indexed, paginated queries rather than by loading the year into the browser.
- The planner holds a smooth frame rate at eight hundred objects, with validation running incrementally on what a change affects.
- An access decision returns within a bounded time at the door, including the degraded path, because a queue at an entrance is a safety problem rather than a latency problem.
- Occupancy recomputes per scan without a full recount, and the safety board updates within a second of a scan.
- Every list endpoint pages by cursor and none is unbounded.
- Images are served in modern formats at the sizes actually displayed, and media below the fold is deferred with its dimensions declared.

**Error mapping.** An error is mapped before it leaves the server. A refusal by the product and a failure inside a backing service are different facts and stay distinct, because merging them makes both undebuggable. No response body, log line, error body or audit record carries a credential, a connection string, a token or a stack trace.

**Observability, which is not the audit trail.** A request identifier is generated at the edge, attached to every log line and returned to the caller on every error so a person can quote it. Logs are structured, and personal data never appears in one: a parameter is logged by name and type, never by value. The trail answers who did this and is kept for years; this answers why this is slow and is kept for weeks, and merging them produces a record too noisy to audit and too expensive to keep.

**Security and privacy.** Every response carries a **security header** set: a content security policy that forbids inline script, a strict transport policy, a frame-ancestors refusal, a referrer policy, a nosniff declaration and a permissions policy. State-changing requests are protected against cross-site forgery, no state change happens on a GET, session cookies are http-only and same-site, free text that reaches a page is rendered as text, and uploads are validated server-side and served through short-lived signed links. No secret value is ever returned by any read path or embedded in any bundled asset.

Personal data of visitors and contractors is collected only where the safety regime or the law requires it, is minimised, is encrypted at rest, and is cleared automatically on the retention schedule the privacy policy states, rather than when somebody remembers. The audit trail is append-only in the store rather than by convention, and it covers accreditation grants and revocations, capacity changes, plan approvals, publication changes, access-rule changes, invoice adjustments and evacuation declarations, with the actor, the time and the before and after values.

**The crawler contract.** `sitemap.xml` is generated from the published public routes across all three languages, `robots.txt` names it, and every public route carries a canonical address.

**Idempotency.** Every mutating call that crosses a boundary carries an idempotency key derived from the logical operation, never from the clock and never from a value generated at send time, because both defeat the retry they exist to protect. A repeated key returns the first result rather than acting again.

## Data model

Roughly two dozen tables. All timestamps are UTC, rendered in the venue's own zone, with the twice-yearly clock change handled explicitly for a build-up window that runs overnight. Occupancy counts and money are integers.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a person can sign in.

Money is held and computed in **integer minor units** of `usd`, never as a decimal fraction. `amount_minor` is a count of cents: `$14,500.00` is `1450000`, not `14500.00` and not `14500`.

### principals

`id`, `email` unique, `role` one of `coordinator`, `operations`, `planner`, `exhibitor`, `finance`, `auditor`, `password_hash`, `party_id` nullable, `status` one of `active` or `removed`, `created_at`.

### parties

`id`, `name` unique, `kind` one of `organiser`, `exhibitor`, `contractor`, `venue_staff`, `caterer`, `security`, `cleaner`, `visitor`, `parent_party_id` nullable and self-referential for delegation, `created_at`. The parent link is what the delegation rule walks, and it is checked for cycles when it is written.

### spaces

`id`, `name` unique, `kind` one of `hall`, `event_hall`, `meeting_room`, `boulevard`, `passage`, `combination`, `area_sqm`, `entrance_ids`, `geometry`, `version`, `created_at`. A combination's membership lives in `space_members` carrying `combination_id` and `member_space_id`. Area is a stored fact about the floor and is never the source of a capacity.

### layouts

`id`, `space_id`, `name` one of `theatre`, `cabaret`, `banquet`, `stand_grid`, `standing`, `licensed_capacity`, `build_hours`, `version`, `effective_from`. Licensed capacity is licensed data per space per layout, and a combination carries its own rows here rather than inheriting its members'.

### holds

`id`, `space_id`, `window_start`, `window_end`, `kind` one of `option`, `booking`, `maintenance`, `rank` nullable, `state`, `expires_at` nullable, `created_by`, `created_at`. This is the one table the overlap rule lives in: a hold on any node blocks every ancestor and every descendant of that node in the same window, enforced where the rows live.

### enquiries, options, challenges

`enquiries`: `id`, `contact_name`, `contact_email`, `window_start`, `window_end`, `expected_visitors`, `event_type`, `spaces_of_interest`, `source` one of `public_form` or `sales`, `created_at`. `options`: `id`, `enquiry_id`, `space_set`, `window`, `rank`, `state`, `expires_at`. Rank is unique per space and window. `challenges`: `id`, `challenger_option_id`, `holder_option_id`, `opened_at`, `window_ends_at`, `outcome`.

### bookings, phases, contracts, amendments

`bookings`: `id`, `option_id`, `party_id`, `contract_id`, `layout_id`, `state`, `created_at`. `phases`: `id`, `booking_id`, `kind` one of `access`, `build_up`, `run`, `tear_down`, `clearance`, `window_start`, `window_end`. A phase row is a hold on its space exactly as a run is. `contracts`: `id`, `booking_id`, `terms`, `signed_at` nullable, `deposit_schedule`. `amendments`: `id`, `contract_id`, `requested_by`, `approved_by`, `moved_what`, `decided_at`.

### resources, work_orders

`resources`: `id`, `name`, `kind` one of `dock`, `lift`, `forklift`, `crew`, `power_drop`, `capacity`, `competences`. `work_orders`: `id`, `booking_id`, `plan_revision_id`, `resource_id`, `required_competence`, `window`, `state`. A work order whose plan revision is withdrawn moves to suspended.

### plans, plan_revisions, plan_objects

`plans`: `id`, `booking_id`, `space_id`. `plan_revisions`: `id`, `plan_id`, `sequence`, `state` one of `draft`, `submitted`, `approved`, `withdrawn`, `approved_by` nullable, `approved_at` nullable. `plan_objects`: `id`, `plan_revision_id`, `kind` one of `stand`, `catering_point`, `stage`, `seating_block`, `entrance_point`, `party_id`, `position`, `dimensions`, `stand_ref` nullable. `plan_constraints` carries the structural objects: `id`, `space_id`, `kind` one of `column`, `truss`, `door`, `fire_exit`, `rigging_point`, `power_point`, `water_point`, `geometry`, `limit_value`.

### accreditations, evidence, badges, scans

`accreditations`: `id`, `party_id`, `person_ref`, `booking_id`, `phase_kinds`, `space_set`, `granted_by_accreditation_id` nullable, `state` one of `pending_evidence`, `valid`, `expired`, `revoked`, `valid_from`, `valid_until`. The granter link is what the cascade walks and what bounds a delegated right. `evidence`: `id`, `accreditation_id`, `kind` one of `insurance`, `risk_assessment`, `competence`, `identity`, `expires_at`. `badges`: `id`, `accreditation_id`, `person_ref`, `issued_at`, `valid_until`, `state`. `scans`: `id`, `badge_id`, `entrance_id`, `decision` one of `admitted`, `refused`, `reason`, `at`, `queued_offline`, `reconciled_at` nullable. The scan table is append-only in the store.

### entrances, entrance_modes

`entrances`: `id`, `name` unique, `space_ids`, `is_exit`. `entrance_modes`: `id`, `entrance_id`, `booking_id`, `phase_kind`, `mode` one of `staff`, `contractor`, `exhibitor`, `trade`, `public`, `closed`. Mode is per event and per phase, which is why the table carries both.

### occupancy_samples, incidents, evacuations

`occupancy_samples`: `id`, `space_id`, `count`, `state` one of `clear`, `approaching`, `at_limit`, `at`. The count is derived from the scan graph rather than from a per-door tally. `incidents`: `id`, `booking_id`, `type`, `plan_position`, `severity`, `owner`, `opened_at`, `closed_at` nullable, `close_out_note` nullable, with an `incident_actions` timeline beside it. `evacuations`: `id`, `declared_by`, `declared_at`, `stood_down_at` nullable, `log_frozen_from`.

### services, service_orders

`services`: `id`, `name`, `category` one of `catering`, `technical`, `furniture`, `cleaning`, `waste`, `signage`, `parking`, `unit`, `unit_price_minor`, `lead_time_hours`, `cutoff_phase`, `cutoff_offset_hours`, `requires_approved_plan`, `requires_plan_position`. `service_orders`: `id`, `booking_id`, `party_id`, `service_id`, `quantity`, `state` one of `draft`, `ordered`, `late_ordered`, `cancelled`, `delivered`, `surcharge_minor`, `approved_by` nullable, `plan_object_id` nullable, `headcount` nullable, `dietary`, `service_window`.

### invoices, invoice_lines, payments

`invoices`: `id`, `booking_id`, `party_id`, `state`, `issued_at`, `total_minor`. `invoice_lines`: `id`, `invoice_id`, `description`, `quantity`, `unit_price_minor`, `tax_rule`, `tax_minor`, `rounding_minor`, `amount_minor`, `variance_cause` nullable. Lines sum exactly to the invoice total, and the rounding decision is recorded rather than absorbed. `payments`: `id`, `invoice_id`, `kind` one of `deposit`, `stage`, `final`, `credit`, `amount_minor`, `received_at`, `external_ref` unique for the idempotent export.

### publications, translations

`publications`: `id`, `booking_id`, `state` one of `private`, `announced`, `published`, `publish_at`, `public_fields`. `translations`: `id`, `publication_id`, `language` one of `nl`, `fr`, `en`, `field`, `value`, `state` one of `missing`, `draft`, `published`. The public projection reads only these two tables, which is what makes an internal field structurally incapable of publication.

### page_views, consents

`page_views`: `id`, `route`, `language`, `at`. Carries no identifier for the person. `consents`: `id`, `consent_ref`, `statistics`, `marketing`, `decided_at`. A page view is written only while the statistics category is granted.

### audit_events

`id`, `sequence`, `actor`, `action`, `target`, `before`, `after`, `at`. Append-only in the store: an update or a delete against this table is refused there.

### Derived rather than stored

Availability state, live occupancy per space, invoice totals, every reporting figure and the public projection are all derived from the tables above on read. None of them is a stored summary that can drift.

### Seed data

One campus. Twelve spaces: `Hall 1` through `Hall 6`, `The Event Hall`, the meeting rooms `MC 1` through `MC 4`, `The Concourse` as the covered boulevard and `The Transit` as the passage between `Hall 4` and `Hall 5`.

Floor areas and licensed capacities in the `stand_grid` layout, exactly as the specification blocks state them: `Hall 1` at `6090` square metres licensing `1620`; `Hall 2` at `4058` licensing `1740`; `Hall 3` at `3601` licensing `1680`; `Hall 4` at `7685` licensing `3660`; `Hall 5` at `4723` licensing `5160`; `Hall 6` at `5055` licensing `1860`; `The Event Hall` at `2000` licensing `2000` with a tribune seating `550`; the four `MC` rooms totalling `1679`. `Hall 5` licenses more people than `Hall 4` on less floor, which is the inversion the model must respect.

Two combinations, each carrying its own licensed figure. `Halls 4 and 5 with the Transit` combines `Hall 4`, `Hall 5` and `The Transit` and licenses `7400`, which is deliberately not the `8820` its two halls would sum to. `The Meeting Centre with the Event Hall` combines `MC 1` through `MC 4` and `The Event Hall` and licenses `2600`.

Five entrances: `North Entrance`, `South Entrance`, `Concourse East`, `Concourse West` and `Dock Gate`. Parking carries `2500` spaces.

Three parties beyond the venue: `Palmarosa` as an organiser, `Bookmark Fair` as an organiser, and `Ironwood Interiors` as an exhibitor whose parent party is `Bookmark Fair`, holding stand `S-118`.

Three bookings. `Verwick Design Days`, organised by `Palmarosa`, holding the combination `Halls 4 and 5 with the Transit`, status chip `Trade fair - registration required`, sector `Architecture & Design`, publication state `published`. `Bookmark Fair`, organised by `Bookmark Fair`, holding `Hall 1`, `Hall 2`, `Hall 3`, `Hall 6`, the four `MC` rooms and `The Event Hall`, status chip `Open to the public`, sector `Lifestyle & Sports`, publication state `published`. `Ironwood Night`, organised by `Palmarosa`, holding `Hall 3` in a later window, publication state `private`, so it occupies the diary and appears on no public surface.

Each booking carries five phases. `Verwick Design Days` carries a `build_up` window immediately before its `run` and a `tear_down` window immediately after, sized from the `stand_grid` build hours.

One maintenance hold: a floor resurfacing on `Hall 3`, which no booking may be placed over.

Two options on one space set, both on `Hall 6` across one seeded week: rank `1` held by `Palmarosa` and rank `2` held by `Bookmark Fair`, so the challenge path has something to run on.

One plan on `Verwick Design Days` with an `approved` revision carrying at least four objects, including one `catering_point`, plus the structural constraints of `Hall 4` and `Hall 5`: columns, trusses, doors, two `fire_exit` constraints with their required clearances, and rigging points with their load limits.

Accreditations: `Palmarosa` accredited as organiser on `Verwick Design Days` across every phase; `Ironwood Interiors` accredited by `Bookmark Fair`; and one contractor accredited by `Ironwood Interiors` whose `insurance` evidence expires inside the seeded window, so the expiry path has something to expire. Badges are issued from each.

Services: at least one from each category, including a rigging service carrying `requires_approved_plan`, a power drop carrying `requires_plan_position`, and a catering service carrying a headcount deadline. `Hall 4` hire is priced at `1450000` minor units per run day.

Two news articles and three case studies exactly as the copy deck names them, one of the two articles carrying a `published` English heading over a body whose translation state is `missing` in the other two languages, so the fallback label has something to label.

Seeding must be idempotent: restarting the app must not duplicate a row.

## Constraints

One campus, one tenant. No second venue and no cross-campus surface.

Absent features: no ticket selling and no box office, no seat-level allocation, no payroll, no procurement, no supplier marketplace, no sales pipeline beyond the enquiry, no second factor, no federated identity provider, no directory provisioning, no native mobile application, no chat, no comments, no likes, no direct messaging, and no model call of any kind from any surface.

Absent integrations: PostgreSQL is the only backing service. The ticketing, parking and accounting interfaces are internal boundaries within this product, taking and returning records in this product's own store; no external network call is made at runtime and no analytics destination is contacted.

Zero-asset build. No binary asset ships: no typeface file, no photograph, no icon file, no texture, no video, no logo file. Everything is generated, drawn inline or rendered procedurally by the zero-asset substitution recipes the front-end specification gives, and that guide is the only source for what replaces a binary. No mark reproduces a real trademark, and no name in the seed data refers to a real company.

No route reflects an unescaped request value into a page. No credential value reaches any surface. No internal field reaches any public surface.

The product must stay responsive with a campus year of five hundred bookings, a floor plan of eight hundred objects and an access log of one hundred thousand scans.

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
- The backing service named in this brief is already running and reachable at its environment variable. Do not download, install, compile or start a copy of it.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

Field names are exact. A list endpoint returns a top-level JSON array. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never as a server error and never as a silent success. Bearer auth is carried on everything except `POST /api/auth/login`, `GET /api/health`, `POST /api/enquiries`, `POST /api/subscriptions`, `GET /api/public/events`, `GET /api/public/spaces`, `GET /api/public/news`, `GET /api/search` and `POST /api/page-views`.

| Endpoint | Request body or query | Returns |
|---|---|---|
| `POST /api/auth/login` | `email`, `password` | `access_token`, `principal` with `email` and `role` |
| `POST /api/auth/logout` | none | empty on success |
| `GET /api/me` | none | `email`, `role`, `party` |
| `GET /api/spaces` | none | array of `id`, `name`, `kind`, `area_sqm`, `members`, `entrances` |
| `GET /api/spaces/{id}/layouts` | none | array of `name`, `licensed_capacity`, `build_hours`, `version` |
| `GET /api/availability` | `space`, `from`, `to` | `state` from the closed set, and on a block also `blocking_space` |
| `POST /api/enquiries` | `contact_name`, `contact_email`, `window_start`, `window_end`, `expected_visitors`, `event_type`, `spaces_of_interest` | the created enquiry with its `id` |
| `GET /api/enquiries` | optional `state` | array of enquiries |
| `POST /api/options` | `enquiry_id`, `spaces`, `window_start`, `window_end`, `rank`, `expires_at` | the created option with its `rank` and `state` |
| `POST /api/options/{id}/challenge` | none | the challenge with its `window_ends_at` |
| `POST /api/options/{id}/confirm` | `layout`, `idempotency_key` | the booking with its `phases` and `contract`, or a refusal naming the space and window already taken |
| `GET /api/bookings/{id}` | none | the booking, its phases, its contract, its services and its exhibitors |
| `POST /api/bookings/{id}/phases` | `kind`, `window_start`, `window_end` | the phase, or a refusal naming the `shortfall_hours` |
| `POST /api/bookings/{id}/cancel` | none | empty on success |
| `GET /api/plans/{id}/revisions` | none | array of `sequence`, `state`, `approved_by` |
| `POST /api/plans/{id}/objects` | `kind`, `position`, `dimensions` | the object, or a refusal carrying `rule` and `measurement` |
| `POST /api/plan-revisions/{id}/decision` | `decision` of `approved` or `withdrawn` | the decided revision |
| `GET /api/accreditations` | optional `booking`, `party` | array of accreditations with their `state` and `granted_by` |
| `POST /api/accreditations` | `party`, `person_ref`, `booking`, `phase_kinds`, `space_set` | the created accreditation |
| `POST /api/accreditations/{id}/revoke` | none | the revoked accreditation and the `cascaded` count |
| `GET /api/entrances` | optional `booking` | array of `name`, `mode` per `phase_kind` |
| `PUT /api/entrances/{id}/mode` | `booking`, `phase_kind`, `mode` | the updated mode |
| `POST /api/scans` | `badge`, `entrance`, `at`, optional `queued_offline` | `decision`, and on a refusal also `reason` |
| `GET /api/occupancy` | `space` | `count`, `state`, `licensed_capacity` |
| `POST /api/incidents` | `booking`, `type`, `plan_position`, `severity`, `owner` | the created incident |
| `POST /api/evacuations` | none | the declaration with its `declared_at` |
| `POST /api/service-orders` | `booking`, `service`, `quantity`, optional `plan_object`, optional `headcount` | the order with its `state` and `surcharge_minor`, or a refusal naming the missing dependency |
| `GET /api/invoices/{id}` | none | the invoice, its `lines` and its `total_minor` |
| `POST /api/invoices/{id}/export` | `idempotency_key` | the export result with its `external_ref` |
| `PUT /api/publications/{booking}` | `state`, `publish_at`, `public_fields` | the publication record |
| `GET /api/public/events` | optional `month`, `status`, `sector`, `hall` | array of published events with their public fields only |
| `GET /api/public/spaces` | none | array of `name`, `capacity`, `area_sqm`, `features`, `suitable_for` |
| `GET /api/public/news` | optional `language` | array of articles with their `translation_state` |
| `POST /api/subscriptions` | `email` | `state` of `sent`, `invalid` or `already` |
| `POST /api/page-views` | `route`, `language` | empty on success, refused while statistics consent is absent |
| `GET /api/search` | `q`, `language` | `state` of `ok`, `invalid` or `failed`, and on `ok` the grouped `results` |
| `GET /api/reports/{name}` | `from`, `to` | the report rows, scoped to the caller's rights |
| `GET /api/audit` | optional `actor`, `action`, `from`, `to`, `cursor` | array of events and a `next_cursor` |
| `GET /api/health` | none | `200` once ready |

### No mocks

PostgreSQL is the fact. Any of the following is a contract violation however good the interface looks: an in-memory array of holds, bookings, scans or audit events that the process rebuilds at start; an availability answer composed without consulting the stored holds; an occupancy figure kept as a counter in the process rather than derived from the stored scans; an audit chain recomputed on read so that it is intact by construction; and a publication filtered when a page renders rather than stored as a separate projection. The named provider is the fact: the app's interface and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A coordinator holds two halls and the passage between them for a week, confirms that hold into a booking whose build-up and tear-down windows occupy the halls exactly as the run does, and every other desk then finds that week taken at the combination and at each hall inside it. A planner's stand across a fire exit is refused as it lands, with the rule named and the clearance measured. A visitor reads the calendar in any of the three languages and never sees the privately held event.
