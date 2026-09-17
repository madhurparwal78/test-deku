# Checklist: Verwick Xpo

Items: 779
Unpinned values flagged: 6
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The product serves a trilingual public site plus an operations console behind one sign-in. `src: Overview`
- [ ] `C-OV-02` `capability` The campus is modelled as a graph of spaces that fit inside one another. `src: Overview`
- [ ] `C-OV-03` `constraint` No two events may hold the same square metre in the same window. `src: Overview`
- [ ] `C-OV-04` `constraint` Exactly one part of the product answers whether a space is free. `src: Overview`
- [ ] `C-OV-05` `constraint` Capacity is a licensed figure held against a space, never derived from floor area. `src: Overview`
- [ ] `C-OV-06` `constraint` A combination capacity is never the sum of the parts of that combination. `src: Overview`
- [ ] `C-OV-07` `capability` The console carries thirteen desks, from the campus calendar through reporting. `src: Overview`
- [ ] `C-OV-08` `constraint` The product carries no ticket selling, no box office, no payroll, no procurement. `src: Overview`
- [ ] `C-OV-09` `constraint` The product carries no chat, no comments, no likes, no second factor. `src: Overview`
- [ ] `C-OV-10` `constraint` No surface makes a model call of any kind. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A `coordinator` places options, sets ranks, opens challenges, confirms bookings. `src: User roles`
- [ ] `C-RL-02` `role` A `coordinator` writes contracts, amendments, phase windows, maintenance windows. `src: User roles`
- [ ] `C-RL-03` `role` A `coordinator` sets publication state, forks annual-plan scenarios, sends invitations. `src: User roles`
- [ ] `C-RL-04` `role` A `coordinator` cannot approve an amendment that same account requested. `src: User roles`
- [ ] `C-RL-05` `role` A `coordinator` cannot alter an audit record. `src: User roles`
- [ ] `C-RL-06` `role` A `coordinator` cannot declare evacuation. `src: User roles`
- [ ] `C-RL-07` `role` A `coordinator` cannot change a licensed capacity figure. `src: User roles`
- [ ] `C-RL-08` `role` An `operations` account sets entrance modes per event, per phase. `src: User roles`
- [ ] `C-RL-09` `role` An `operations` account issues badges, suspends badges, records scan decisions. `src: User roles`
- [ ] `C-RL-10` `role` An `operations` account raises incidents, closes incidents, declares evacuation. `src: User roles`
- [ ] `C-RL-11` `role` An `operations` account revises licensed capacity figures, schedules work orders. `src: User roles`
- [ ] `C-RL-12` `role` An `operations` account cannot confirm a booking. `src: User roles`
- [ ] `C-RL-13` `role` An `operations` account cannot price anything, cannot raise an invoice. `src: User roles`
- [ ] `C-RL-14` `role` An `operations` account cannot publish to the public site. `src: User roles`
- [ ] `C-RL-15` `role` An `operations` account cannot read the commercial terms of a contract. `src: User roles`
- [ ] `C-RL-16` `role` A `planner` reads the events of the party of that planner, never another party's. `src: User roles`
- [ ] `C-RL-17` `role` A `planner` writes plan revisions, approval requests, service orders inside cut-offs. `src: User roles`
- [ ] `C-RL-18` `role` A `planner` accredits exhibitors, sets the rules capping exhibitor ordering. `src: User roles`
- [ ] `C-RL-19` `role` A `planner` writes the public fields of the event of that planner, plus translations. `src: User roles`
- [ ] `C-RL-20` `role` A `planner` cannot reach another party's event through search, export, public preview. `src: User roles`
- [ ] `C-RL-21` `role` A `planner` cannot confirm a booking. `src: User roles`
- [ ] `C-RL-22` `role` A `planner` cannot grant a right the accreditation of that planner does not hold. `src: User roles`
- [ ] `C-RL-23` `role` A `planner` cannot approve a plan revision that same planner submitted. `src: User roles`
- [ ] `C-RL-24` `role` An `exhibitor` reads only the own stand of that exhibitor, plus the position on the approved plan. `src: User roles`
- [ ] `C-RL-25` `role` An `exhibitor` reads the own accreditation, badges, service orders, dock slot, invoices. `src: User roles`
- [ ] `C-RL-26` `role` An `exhibitor` writes service orders inside the rules of the organiser. `src: User roles`
- [ ] `C-RL-27` `role` An `exhibitor` requests accreditation for the own stand contractor of that exhibitor. `src: User roles`
- [ ] `C-RL-28` `role` An `exhibitor` cannot read another exhibitor's stand, position, orders, badges, invoices. `src: User roles`
- [ ] `C-RL-29` `capability` A forged request for another exhibitor's record is answered as not found, never as forbidden. `src: User roles`
- [ ] `C-RL-30` `role` A `finance` account writes invoices, credit notes, deposit schedules, payment records. `src: User roles`
- [ ] `C-RL-31` `role` A `finance` account raises damage charges, cleaning charges, dispute outcomes. `src: User roles`
- [ ] `C-RL-32` `role` A `finance` account cannot confirm a booking, cannot change a plan, cannot issue a badge. `src: User roles`
- [ ] `C-RL-33` `role` An `auditor` reads the audit trail plus every report, nothing else anywhere. `src: User roles`
- [ ] `C-RL-34` `role` An `auditor` writes nothing anywhere. `src: User roles`
- [ ] `C-RL-35` `capability` Authorization is enforced server-side on every mutating endpoint. `src: User roles`
- [ ] `C-RL-36` `capability` A direct API call from a lower role to a higher-role endpoint is refused by the server. `src: User roles`
- [ ] `C-RL-37` `capability` A refused call leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-38` `constraint` Signup is closed on the console path: an account exists by seeding, by invitation. `src: User roles`
- [ ] `C-RL-39` `capability` Permission is scoped by relationship, so a planner reaches an event through the party of that planner. `src: User roles`
- [ ] `C-RL-40` `literal` The seeded principals are `coordinator@example.com`, `operations@example.com`, `planner@example.com`, `planner2@example.com`, `exhibitor@example.com`, `finance@example.com`, `auditor@example.com`. `src: User roles`
- [ ] `C-RL-41` `literal` Every seeded principal signs in with the password `deku-demo-pw-2026`. `src: User roles`
- [ ] `C-RL-42` `literal` The seeded exhibitor party is `Ironwood Interiors`, holding stand `S-118`. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` Sign-in accepts an email plus a password, returning a bearer token carrying the principal email, the principal role. `src: Core features, auth`
- [ ] `C-CF-02` `capability` An unknown address produces the same refusal as a wrong password. `src: Core features, auth`
- [ ] `C-CF-03` `constraint` Neither response nor page reveals which of an unknown address, a wrong password occurred. `src: Core features, auth`
- [ ] `C-CF-04` `capability` Repeated sign-in failures for one address are refused after a stated number of attempts. `src: Core features, auth`
- [ ] `C-CF-05` `capability` A sign-in lockout appends an authentication event to the audit trail. `src: Core features, auth`
- [ ] `C-CF-06` `capability` A signed-out token is refused on the next request, never served from a cache. `src: Core features, auth`
- [ ] `C-CF-07` `capability` A session expiring mid-action leaves the typed work on screen, offering sign-in in place. `src: Core features, auth`
- [ ] `C-CF-08` `capability` An anonymous caller reaching a console route is served the sign-in route with the requested address remembered. `src: Core features, auth`
- [ ] `C-CF-09` `constraint` Passwords are stored hashed. `src: Core features, auth`
- [ ] `C-CF-10` `data` Every space carries a kind, a floor area in square metres, an entrance set, an availability calendar. `src: Core features, space model`
- [ ] `C-CF-11` `literal` A space kind is one of `hall`, `event_hall`, `meeting_room`, `boulevard`, `passage`, `combination`. `src: Core features, space model`
- [ ] `C-CF-12` `capability` Adjacent halls combine into one hireable space. `src: Core features, space model`
- [ ] `C-CF-13` `capability` The passage between two halls is itself hireable, making the combination of those halls possible. `src: Core features, space model`
- [ ] `C-CF-14` `capability` The covered boulevard may be hired as exhibition space, as catering space. `src: Core features, space model`
- [ ] `C-CF-15` `constraint` The covered boulevard remains the public route between halls throughout any hire of that boulevard. `src: Core features, space model`
- [ ] `C-CF-16` `capability` The meeting rooms combine with one another, plus with the event hall. `src: Core features, space model`
- [ ] `C-CF-17` `data` A combination is a node whose children are the spaces that combination consumes. `src: Core features, space model`
- [ ] `C-CF-18` `capability` Holding a combination holds every descendant space of that combination. `src: Core features, space model`
- [ ] `C-CF-19` `capability` Holding any descendant blocks every ancestor combination of that descendant. `src: Core features, space model`
- [ ] `C-CF-20` `constraint` Checking availability only at the leaf level is refused as a violation. `src: Core features, space model`
- [ ] `C-CF-21` `constraint` Checking availability only at the level booked is refused as a violation. `src: Core features, space model`
- [ ] `C-CF-22` `literal` Availability answers exactly one of `free`, `held`, `booked`, `blocked_by_ancestor`, `blocked_by_descendant`, `maintenance`. `src: Core features, space model`
- [ ] `C-CF-23` `capability` A blocked availability answer names the blocking space. `src: Core features, space model`
- [ ] `C-CF-24` `capability` Hiring the boulevard is refused when the remaining public route would breach the occupancy rules. `src: Core features, space model`
- [ ] `C-CF-25` `capability` A refused boulevard hire names the failing route. `src: Core features, space model`
- [ ] `C-CF-26` `capability` A space added in operations appears on the public floor plan without anyone redrawing a picture. `src: Core features, space model`
- [ ] `C-CF-27` `literal` The campus carries exactly one campus-wide state at a time, `normal` or `evacuation`. `src: Core features, space model`
- [ ] `C-CF-28` `literal` A layout name is one of `theatre`, `cabaret`, `banquet`, `stand_grid`, `standing`. `src: Core features, layouts`
- [ ] `C-CF-29` `data` Each layout carries an own licensed capacity, an own build-hours figure. `src: Core features, layouts`
- [ ] `C-CF-30` `constraint` Licensed capacity is never derived from floor area. `src: Core features, layouts`
- [ ] `C-CF-31` `capability` The seeded inventory licenses more people in `Hall 5` than in `Hall 4` on less floor area. `src: Core features, layouts`
- [ ] `C-CF-32` `constraint` A combination carries an own licensed figure rather than the sum of the children of that combination. `src: Core features, layouts`
- [ ] `C-CF-33` `capability` The layout chosen for a booking sets the figure the safety board enforces. `src: Core features, layouts`
- [ ] `C-CF-34` `capability` The layout chosen for a booking sets the build hours the works schedule reserves. `src: Core features, layouts`
- [ ] `C-CF-35` `data` A licensed figure is versioned, carrying the date from which that figure is effective. `src: Core features, layouts`
- [ ] `C-CF-36` `capability` A revised licence figure applies only to bookings confirmed after the revision. `src: Core features, layouts`
- [ ] `C-CF-37` `constraint` Rewriting historical capacity to a revised figure is refused as a violation. `src: Core features, layouts`
- [ ] `C-CF-38` `data` An enquiry carries a contact, a date range, an expected visitor count, an event type, spaces of interest. `src: Core features, enquiries`
- [ ] `C-CF-39` `capability` A public contact submission creates an enquiry record in the product. `src: Core features, enquiries`
- [ ] `C-CF-40` `constraint` Sending an email in place of creating an enquiry record is refused as a violation. `src: Core features, enquiries`
- [ ] `C-CF-41` `data` An option is a soft hold on a named space set across a named window, carrying an expiry, a rank. `src: Core features, options`
- [ ] `C-CF-42` `literal` Option state is exactly one of `held`, `challenged`, `released`, `confirmed`, `lapsed`. `src: Core features, options`
- [ ] `C-CF-43` `capability` Several options coexist on the same space set, the same window, ranked first, second, third. `src: Core features, options`
- [ ] `C-CF-44` `constraint` A rank is unique per space per window. `src: Core features, options`
- [ ] `C-CF-45` `constraint` Taking a lower-ranked option never blocks a higher-ranked one. `src: Core features, options`
- [ ] `C-CF-46` `capability` A lower-ranked option may challenge the holder of a higher rank. `src: Core features, options`
- [ ] `C-CF-47` `capability` A challenged holder is notified, receiving a stated window to confirm, to release. `src: Core features, options`
- [ ] `C-CF-48` `capability` An unanswered challenge releases the option of the holder, promoting the challenger, without anybody pressing a button. `src: Core features, options`
- [ ] `C-CF-49` `constraint` Leaving a challenge outcome to a nightly job is refused as a violation. `src: Core features, options`
- [ ] `C-CF-50` `capability` Confirming an option releases the other options on that space, that window. `src: Core features, options`
- [ ] `C-CF-51` `capability` Each released holder receives a notification record naming the space set, the window, the reason. `src: Core features, options`
- [ ] `C-CF-52` `capability` An option reaching expiry with no confirmation becomes `lapsed`. `src: Core features, options`
- [ ] `C-CF-53` `capability` A lapsed option returns the space to `free` for every rank below that option. `src: Core features, options`
- [ ] `C-CF-54` `capability` Confirmation creates the space set, the phase records, the contract record in one transaction. `src: Core features, confirmation`
- [ ] `C-CF-55` `constraint` A partial confirmation is refused: either every record is created, none is. `src: Core features, confirmation`
- [ ] `C-CF-56` `capability` Two coordinators confirming competing options in the same instant leave exactly one booking. `src: Core features, confirmation`
- [ ] `C-CF-57` `capability` The losing confirmation is refused with the space, the window already taken named. `src: Core features, confirmation`
- [ ] `C-CF-58` `capability` The losing option stays readable after a contended confirmation. `src: Core features, confirmation`
- [ ] `C-CF-59` `constraint` The single-booking guarantee holds where the data lives, never only in application code. `src: Core features, confirmation`
- [ ] `C-CF-60` `data` A contract file holds the agreed terms, the priced services, the deposit schedule, the signatures. `src: Core features, confirmation`
- [ ] `C-CF-61` `capability` A signed contract locks the space set of the booking of that contract. `src: Core features, confirmation`
- [ ] `C-CF-62` `data` An amendment names who requested the change, who approved the change, what moved, when. `src: Core features, confirmation`
- [ ] `C-CF-63` `capability` Cancelling a booking releases every space that booking held, in one transaction. `src: Core features, confirmation`
- [ ] `C-CF-64` `capability` A released window reads `free` to the desk, the planner, the public calendar, reporting alike. `src: Core features, confirmation`
- [ ] `C-CF-65` `literal` A booking phase kind is exactly one of `access`, `build_up`, `run`, `tear_down`, `clearance`. `src: Core features, timeline`
- [ ] `C-CF-66` `data` Each phase carries an own start, an own end, an own occupancy rule, an own accreditation profile. `src: Core features, timeline`
- [ ] `C-CF-67` `capability` Every phase occupies the space exactly as the run phase does. `src: Core features, timeline`
- [ ] `C-CF-68` `constraint` Treating build-up as a calendar annotation beside the booking is refused as a violation. `src: Core features, timeline`
- [ ] `C-CF-69` `constraint` Treating tear-down as a calendar annotation beside the booking is refused as a violation. `src: Core features, timeline`
- [ ] `C-CF-70` `ui` The campus timeline draws every phase of every event on one axis, one row per space. `src: Core features, timeline`
- [ ] `C-CF-71` `ui` A combination is drawn across every row that combination consumes. `src: Core features, timeline`
- [ ] `C-CF-72` `capability` Two events sharing a hall on consecutive days are refused unless the tear-down window, the build-up window genuinely fit. `src: Core features, timeline`
- [ ] `C-CF-73` `capability` A refused turnaround names the shortfall in hours. `src: Core features, timeline`
- [ ] `C-CF-74` `capability` Extending a run pushes the tear-down window of the same booking. `src: Core features, timeline`
- [ ] `C-CF-75` `capability` A phase collision raises a conflict record naming both bookings, plus the overlapping window. `src: Core features, timeline`
- [ ] `C-CF-76` `constraint` A phase collision never silently overwrites either booking. `src: Core features, timeline`
- [ ] `C-CF-77` `capability` Layout build hours seed the default phase lengths of a booking. `src: Core features, timeline`
- [ ] `C-CF-78` `data` Loading docks, freight lifts, forklifts, rigging crews, power drops are finite scheduled resources. `src: Core features, resources`
- [ ] `C-CF-79` `capability` A shared resource is scheduled against the same timeline as the spaces. `src: Core features, resources`
- [ ] `C-CF-80` `capability` Resource contention is shown naming both events, plus the contended window. `src: Core features, resources`
- [ ] `C-CF-81` `capability` An assignment that would double-book a resource is refused. `src: Core features, resources`
- [ ] `C-CF-82` `capability` A resource assignment carries a competence requirement where one applies. `src: Core features, resources`
- [ ] `C-CF-83` `capability` An assignment breaching the stated working-hours rule of a crew is refused with the rule named. `src: Core features, resources`
- [ ] `C-CF-84` `ui` The planner canvas renders the true space geometry at scale from the space model. `src: Core features, planner`
- [ ] `C-CF-85` `data` Structural constraints are first-class objects: columns, trusses with heights, doors with widths. `src: Core features, planner`
- [ ] `C-CF-86` `data` Structural constraints carry fire exits with required clearances, rigging anchors with load limits. `src: Core features, planner`
- [ ] `C-CF-87` `data` Structural constraints carry power positions, water positions, the ceiling height envelope. `src: Core features, planner`
- [ ] `C-CF-88` `literal` A placed plan object kind is one of `stand`, `catering_point`, `stage`, `seating_block`, `entrance_point`. `src: Core features, planner`
- [ ] `C-CF-89` `capability` A placed object snaps to the plan grid, carrying own dimensions in metres, plus the owning party. `src: Core features, planner`
- [ ] `C-CF-90` `capability` A stand blocking a fire exit is flagged at the moment of placement. `src: Core features, planner`
- [ ] `C-CF-91` `capability` A stand encroaching on a required aisle width is flagged at the moment of placement. `src: Core features, planner`
- [ ] `C-CF-92` `capability` A stand sitting on a column is flagged at the moment of placement. `src: Core features, planner`
- [ ] `C-CF-93` `capability` An object exceeding the load limit of a rigging anchor is flagged at the moment of placement. `src: Core features, planner`
- [ ] `C-CF-94` `ui` A validation flag names the rule in words, showing the offending measurement. `src: Core features, planner`
- [ ] `C-CF-95` `constraint` A plan validating only on save is refused as a violation. `src: Core features, planner`
- [ ] `C-CF-96` `capability` Validation runs on the objects a change affects rather than on the whole plan. `src: Core features, planner`
- [ ] `C-CF-97` `capability` The canvas keeps panning smoothly, keeps zooming smoothly, at eight hundred objects. `src: Core features, planner`
- [ ] `C-CF-98` `capability` Two planners in one plan each see the presence of the other within a second, with no reload. `src: Core features, planner`
- [ ] `C-CF-99` `capability` Two planners in one plan each see the changes of the other within a second, with no reload. `src: Core features, planner`
- [ ] `C-CF-100` `capability` Edits from two planners merge per object. `src: Core features, planner`
- [ ] `C-CF-101` `constraint` An object one planner is dragging cannot be moved out from under that planner. `src: Core features, planner`
- [ ] `C-CF-102` `capability` Two simultaneous moves of one object resolve to one position on both screens. `src: Core features, planner`
- [ ] `C-CF-103` `constraint` A contended move never loses the other work of either planner. `src: Core features, planner`
- [ ] `C-CF-104` `data` A plan revision carries a compare view against the revision before that one. `src: Core features, planner`
- [ ] `C-CF-105` `literal` A plan revision state is exactly one of `draft`, `submitted`, `approved`, `withdrawn`. `src: Core features, planner`
- [ ] `C-CF-106` `capability` The approved revision flows to the works schedule, the exit calculation, the exhibitor pack. `src: Core features, planner`
- [ ] `C-CF-107` `capability` Withdrawing an approval suspends every work order scheduled against the withdrawn revision. `src: Core features, planner`
- [ ] `C-CF-108` `literal` A party kind is one of `organiser`, `exhibitor`, `contractor`, `venue_staff`, `caterer`, `security`, `cleaner`, `visitor`. `src: Core features, accreditation`
- [ ] `C-CF-109` `capability` Every person on site is accredited per event, per phase, per space set. `src: Core features, accreditation`
- [ ] `C-CF-110` `literal` An evidence kind is one of `insurance`, `risk_assessment`, `competence`, `identity`. `src: Core features, accreditation`
- [ ] `C-CF-111` `literal` Accreditation state is exactly one of `pending_evidence`, `valid`, `expired`, `revoked`. `src: Core features, accreditation`
- [ ] `C-CF-112` `capability` An expiring certificate withdraws the accreditation of that certificate at the moment of expiry. `src: Core features, accreditation`
- [ ] `C-CF-113` `capability` Every badge derived from a withdrawn accreditation stops working at the same moment. `src: Core features, accreditation`
- [ ] `C-CF-114` `constraint` Leaving expiry to a nightly sweep is refused as a violation. `src: Core features, accreditation`
- [ ] `C-CF-115` `capability` An organiser accredits the exhibitors of that organiser. `src: Core features, accreditation`
- [ ] `C-CF-116` `capability` An exhibitor accredits the own stand contractor of that exhibitor. `src: Core features, accreditation`
- [ ] `C-CF-117` `constraint` A right granted downstream never exceeds the right of the granter of that right. `src: Core features, accreditation`
- [ ] `C-CF-118` `capability` A delegated right is resolved at read time rather than only at assignment time. `src: Core features, accreditation`
- [ ] `C-CF-119` `capability` Revoking an organiser accreditation withdraws every accreditation granted beneath that one, within a second. `src: Core features, accreditation`
- [ ] `C-CF-120` `capability` Every badge derived from a cascaded revocation stops working within a second. `src: Core features, accreditation`
- [ ] `C-CF-121` `constraint` A cascade running on a schedule rather than on the revocation is refused as a violation. `src: Core features, accreditation`
- [ ] `C-CF-122` `capability` A person holding accreditations for several concurrent events holds the union of what is currently valid. `src: Core features, accreditation`
- [ ] `C-CF-123` `constraint` The rights of a person are scoped to the space, the phase that person stands in. `src: Core features, accreditation`
- [ ] `C-CF-124` `literal` An entrance mode is one of `staff`, `contractor`, `exhibitor`, `trade`, `public`, `closed`. `src: Core features, access`
- [ ] `C-CF-125` `capability` Entrance mode is set per event, per phase, never as a site-wide setting. `src: Core features, access`
- [ ] `C-CF-126` `capability` One event runs access control through a single entrance with the others `closed`. `src: Core features, access`
- [ ] `C-CF-127` `data` A badge is issued from an accreditation, is signed, is time-bound, names exactly one person. `src: Core features, access`
- [ ] `C-CF-128` `constraint` A badge cannot be transferred between people. `src: Core features, access`
- [ ] `C-CF-129` `capability` A scan is evaluated against the current accreditation, phase, space rights, occupancy. `src: Core features, access`
- [ ] `C-CF-130` `literal` A scan decision is `admitted` or `refused`. `src: Core features, access`
- [ ] `C-CF-131` `capability` A scan decision returns within a bounded time. `src: Core features, access`
- [ ] `C-CF-132` `literal` A refusal reason is one of `no_accreditation`, `wrong_phase`, `wrong_space`, `expired_evidence`, `revoked`, `at_capacity`, `anti_passback`. `src: Core features, access`
- [ ] `C-CF-133` `ui` A refusal reason is shown to the steward at the door in words. `src: Core features, access`
- [ ] `C-CF-134` `capability` A badge having entered without leaving cannot be used again at another entrance. `src: Core features, access`
- [ ] `C-CF-135` `capability` A stated grace window allows legitimate re-entry after an anti-passback refusal. `src: Core features, access`
- [ ] `C-CF-136` `capability` The anti-passback rule may be relaxed per event by an operations account. `src: Core features, access`
- [ ] `C-CF-137` `data` Every scan is appended carrying the entrance, the badge, the decision, the reason, the time. `src: Core features, access`
- [ ] `C-CF-138` `constraint` An update against a scan row is refused where the data lives. `src: Core features, access`
- [ ] `C-CF-139` `constraint` A delete against a scan row is refused where the data lives. `src: Core features, access`
- [ ] `C-CF-140` `capability` An entrance losing the connection of that entrance keeps deciding on the rule set last held. `src: Core features, degraded entrance`
- [ ] `C-CF-141` `capability` A degraded entrance keeps deciding for a stated staleness bound, queueing every scan taken. `src: Core features, degraded entrance`
- [ ] `C-CF-142` `constraint` Admitting nobody during a disconnection is refused as unsafe. `src: Core features, degraded entrance`
- [ ] `C-CF-143` `constraint` Admitting everybody during a disconnection is refused as a breach. `src: Core features, degraded entrance`
- [ ] `C-CF-144` `capability` Queued scans reconcile in order on reconnect. `src: Core features, degraded entrance`
- [ ] `C-CF-145` `capability` A revocation issued during a disconnection takes effect at reconnect. `src: Core features, degraded entrance`
- [ ] `C-CF-146` `capability` A scan admitting somebody after revocation is surfaced to operations as a named exception. `src: Core features, degraded entrance`
- [ ] `C-CF-147` `ui` The staleness bound is shown at the entrance throughout a degraded period. `src: Core features, degraded entrance`
- [ ] `C-CF-148` `capability` Live occupancy per space is derived from entrance scans, internal scans. `src: Core features, occupancy`
- [ ] `C-CF-149` `capability` Live occupancy is compared continuously against the licensed capacity of the current layout. `src: Core features, occupancy`
- [ ] `C-CF-150` `capability` A person admitted to a combination is present in every constituent hall of that combination. `src: Core features, occupancy`
- [ ] `C-CF-151` `capability` Somebody moving between joined halls through the boulevard is never counted twice. `src: Core features, occupancy`
- [ ] `C-CF-152` `constraint` Counting occupancy per door is refused as a violation. `src: Core features, occupancy`
- [ ] `C-CF-153` `literal` Occupancy state is exactly one of `clear`, `approaching`, `at_limit`. `src: Core features, occupancy`
- [ ] `C-CF-154` `capability` An `approaching` occupancy state raises an alert on the safety board. `src: Core features, occupancy`
- [ ] `C-CF-155` `capability` An `at_limit` occupancy state closes admission to that space. `src: Core features, occupancy`
- [ ] `C-CF-156` `constraint` An `at_limit` occupancy state leaves every exit free. `src: Core features, occupancy`
- [ ] `C-CF-157` `capability` Occupancy recomputes per scan rather than by recounting the whole campus. `src: Core features, occupancy`
- [ ] `C-CF-158` `capability` The safety board shows a new occupancy figure within a second of a scan. `src: Core features, occupancy`
- [ ] `C-CF-159` `constraint` An occupancy figure is an integer, never fractional, never negative. `src: Core features, occupancy`
- [ ] `C-CF-160` `capability` The licensed figure of a space is bound to the exits available in the current approved plan. `src: Core features, safety`
- [ ] `C-CF-161` `capability` An approved plan blocking an exit reduces the licensed figure of that space automatically. `src: Core features, safety`
- [ ] `C-CF-162` `ui` The safety board shows a reduced figure together with the reason, plus the causing plan revision. `src: Core features, safety`
- [ ] `C-CF-163` `data` An incident carries a type, a plan position, an urgency level, an owner, an action timeline. `src: Core features, safety`
- [ ] `C-CF-164` `capability` An incident cannot be closed without a close-out note. `src: Core features, safety`
- [ ] `C-CF-165` `capability` Declaring evacuation opens every entrance as an exit. `src: Core features, safety`
- [ ] `C-CF-166` `capability` Declaring evacuation suspends admission across the campus. `src: Core features, safety`
- [ ] `C-CF-167` `capability` Declaring evacuation publishes muster information to staff surfaces. `src: Core features, safety`
- [ ] `C-CF-168` `capability` Declaring evacuation freezes the access log for the investigation. `src: Core features, safety`
- [ ] `C-CF-169` `constraint` Nothing in the product may prevent an exit throughout a declared evacuation. `src: Core features, safety`
- [ ] `C-CF-170` `capability` Declaring evacuation is written to the audit trail with the account, the time. `src: Core features, safety`
- [ ] `C-CF-171` `capability` Standing down evacuation is written to the audit trail with the account, the time. `src: Core features, safety`
- [ ] `C-CF-172` `capability` A frozen access log stays readable throughout the freeze. `src: Core features, safety`
- [ ] `C-CF-173` `capability` Every capacity change, plan approval, incident, evacuation, drill is appended to the trail. `src: Core features, safety`
- [ ] `C-CF-174` `data` The venue sells catering, technical services, furniture, cleaning, waste, signage, parking allocations. `src: Core features, services`
- [ ] `C-CF-175` `data` Each service carries a unit, a price in integer minor units, a lead time, an order cut-off. `src: Core features, services`
- [ ] `C-CF-176` `capability` A service cut-off is expressed relative to a named event phase. `src: Core features, services`
- [ ] `C-CF-177` `capability` A rigging order requires an approved plan revision. `src: Core features, services`
- [ ] `C-CF-178` `capability` A power drop order requires a position on the approved plan. `src: Core features, services`
- [ ] `C-CF-179` `capability` An order whose dependency is unmet is refused with the missing dependency named. `src: Core features, services`
- [ ] `C-CF-180` `capability` Ordering after the cut-off requires a surcharge plus an approval, both recorded on the order. `src: Core features, services`
- [ ] `C-CF-181` `literal` A service order state is exactly one of `draft`, `ordered`, `late_ordered`, `cancelled`, `delivered`. `src: Core features, services`
- [ ] `C-CF-182` `data` A catering order carries a headcount with an own confirmation deadline, dietary requirements. `src: Core features, services`
- [ ] `C-CF-183` `capability` A catering service time is tied to the run phase of the booking. `src: Core features, services`
- [ ] `C-CF-184` `capability` A catering delivery position is a position on the approved floor plan. `src: Core features, services`
- [ ] `C-CF-185` `capability` An exhibitor orders for the own stand of that exhibitor inside the rules of the organiser. `src: Core features, services`
- [ ] `C-CF-186` `capability` The rules of an organiser may cap spend, restrict suppliers, require approval. `src: Core features, services`
- [ ] `C-CF-187` `capability` An organiser sees the aggregate across every stand; an exhibitor sees only the own orders. `src: Core features, services`
- [ ] `C-CF-188` `capability` A booking accrues charges from space hire, phase durations, services ordered. `src: Core features, invoicing`
- [ ] `C-CF-189` `capability` A booking accrues charges from metered power, water, waste, cleaning hours. `src: Core features, invoicing`
- [ ] `C-CF-190` `capability` A booking accrues any late-order surcharge raised against that booking. `src: Core features, invoicing`
- [ ] `C-CF-191` `constraint` Money is held in integer minor units of `usd`, never as a decimal fraction. `src: Core features, invoicing`
- [ ] `C-CF-192` `capability` Value-added tax is applied per line by rule, with the rounding decision recorded on the line. `src: Core features, invoicing`
- [ ] `C-CF-193` `constraint` Invoice lines sum exactly to the invoice total, leaving no residue. `src: Core features, invoicing`
- [ ] `C-CF-194` `capability` Deposits follow the schedule of the contract of that booking. `src: Core features, invoicing`
- [ ] `C-CF-195` `capability` The final invoice reconciles the estimate to the actual with every variance attributed to a named cause. `src: Core features, invoicing`
- [ ] `C-CF-196` `capability` Charges of an exhibitor are billed to that exhibitor. `src: Core features, invoicing`
- [ ] `C-CF-197` `constraint` An organiser never sees the payment records of an exhibitor. `src: Core features, invoicing`
- [ ] `C-CF-198` `capability` A damage charge is raised with the inspection evidence attached. `src: Core features, invoicing`
- [ ] `C-CF-199` `capability` A damage charge carries a dispute path with a recorded outcome. `src: Core features, invoicing`
- [ ] `C-CF-200` `capability` A retried invoice export never produces a second invoice for the same booking. `src: Core features, invoicing`
- [ ] `C-CF-201` `literal` A publication state is exactly one of `private`, `announced`, `published`. `src: Core features, publishing`
- [ ] `C-CF-202` `capability` Nothing reaches the public site before the publication date of that record. `src: Core features, publishing`
- [ ] `C-CF-203` `capability` An unannounced booking occupies the diary, staying invisible to every public surface. `src: Core features, publishing`
- [ ] `C-CF-204` `data` The public field set is title, description, dates, public times, status, sector, halls, organiser links. `src: Core features, publishing`
- [ ] `C-CF-205` `constraint` Rates, contacts, contract terms, occupancy, incidents are structurally incapable of publication. `src: Core features, publishing`
- [ ] `C-CF-206` `constraint` Filtering internal fields when a page renders is refused as a violation. `src: Core features, publishing`
- [ ] `C-CF-207` `data` Each public field carries per-language values plus a translation state. `src: Core features, publishing`
- [ ] `C-CF-208` `capability` A missing translation falls back with a visible label naming the language shown. `src: Core features, publishing`
- [ ] `C-CF-209` `constraint` A missing translation never renders an empty field, never silently renders another language. `src: Core features, publishing`
- [ ] `C-CF-210` `capability` Publishing is atomic per event, taking effect on the public site within a minute. `src: Core features, publishing`
- [ ] `C-CF-211` `capability` Unpublishing removes an event from the public site within a minute. `src: Core features, publishing`
- [ ] `C-CF-212` `capability` A publication state change is written to the audit trail with the actor, the time. `src: Core features, publishing`
- [ ] `C-CF-213` `ui` The exhibitor surface shows the stand, the position on the approved plan, the accreditation, the badges. `src: Core features, exhibitor portal`
- [ ] `C-CF-214` `ui` The exhibitor surface shows the service orders, the dock slot, the documents, the invoices. `src: Core features, exhibitor portal`
- [ ] `C-CF-215` `capability` An exhibitor requests a dock slot from the slots the organiser released. `src: Core features, exhibitor portal`
- [ ] `C-CF-216` `capability` A dock slot request for a taken slot is refused, naming the next free slot. `src: Core features, exhibitor portal`
- [ ] `C-CF-217` `capability` The document set of an exhibitor is generated from the records of the event of that exhibitor. `src: Core features, exhibitor portal`
- [ ] `C-CF-218` `data` Work orders are scheduled against riggers, electricians, cleaners, forklifts, drivers, lifts, docks. `src: Core features, works`
- [ ] `C-CF-219` `capability` A work order names the competence required by that order. `src: Core features, works`
- [ ] `C-CF-220` `capability` Scheduling a rigging order to somebody without rigging competence is refused with the competence named. `src: Core features, works`
- [ ] `C-CF-221` `ui` A clash view shows every double-booking of a person, of a machine, across concurrent events. `src: Core features, works`
- [ ] `C-CF-222` `capability` A work order whose plan approval is withdrawn moves to suspended rather than being carried out. `src: Core features, works`
- [ ] `C-CF-223` `capability` A suspension names the revision that was withdrawn. `src: Core features, works`
- [ ] `C-CF-224` `capability` Reports answer campus occupancy over time by space, by combination. `src: Core features, reporting`
- [ ] `C-CF-225` `capability` Reports answer revenue per event, revenue per square metre per day. `src: Core features, reporting`
- [ ] `C-CF-226` `capability` Reports answer service attachment rates, turnaround performance against the phase model. `src: Core features, reporting`
- [ ] `C-CF-227` `capability` Reports answer incident rates, close-out times, accreditation compliance, expired-certificate events. `src: Core features, reporting`
- [ ] `C-CF-228` `capability` Reports answer waste streams, energy per event, reusable stand material for the charter. `src: Core features, reporting`
- [ ] `C-CF-229` `constraint` Every reporting figure derives from the ledgers rather than from a stored summary. `src: Core features, reporting`
- [ ] `C-CF-230` `constraint` One period totalled along different axes agrees exactly. `src: Core features, reporting`
- [ ] `C-CF-231` `capability` A report is scoped by the rights of the reader of that report. `src: Core features, reporting`
- [ ] `C-CF-232` `capability` External ticketing volumes are imported for occupancy forecasting. `src: Core features, interfaces`
- [ ] `C-CF-233` `capability` Gate scan events are deduplicated against the own scans of the product. `src: Core features, interfaces`
- [ ] `C-CF-234` `capability` Parking is allocated per event with pre-booked allocations for exhibitors, staff. `src: Core features, interfaces`
- [ ] `C-CF-235` `capability` The live parking count feeds the public visitor-information pages. `src: Core features, interfaces`
- [ ] `C-CF-236` `capability` Invoices synchronise to the accounting interface behind one boundary, idempotently. `src: Core features, interfaces`
- [ ] `C-CF-237` `constraint` The public site consumes the published projection through one authority, never an operations record directly. `src: Core features, interfaces`
- [ ] `C-CF-238` `ui` The visitor plan renders the entrance, the halls in use, the catering positions, the toilets, the exits. `src: Core features, wayfinding`
- [ ] `C-CF-239` `ui` The visitor plan renders the route between the halls in use for that event. `src: Core features, wayfinding`
- [ ] `C-CF-240` `capability` The plan is cached on the device of the visitor on first load. `src: Core features, wayfinding`
- [ ] `C-CF-241` `capability` The wayfinding page renders fully with the network off. `src: Core features, wayfinding`
- [ ] `C-CF-242` `capability` A cache older than the stated freshness announces the own age of that cache. `src: Core features, wayfinding`
- [ ] `C-CF-243` `constraint` A build requiring the network to draw the map is refused as a violation. `src: Core features, wayfinding`
- [ ] `C-CF-244` `capability` A hall closed for turnaround redraws the map within a minute of the operations change. `src: Core features, wayfinding`
- [ ] `C-CF-245` `capability` An entrance switched from `public` to `staff` redraws the map within a minute. `src: Core features, wayfinding`
- [ ] `C-CF-246` `capability` A catering position marked sold out redraws the map within a minute. `src: Core features, wayfinding`
- [ ] `C-CF-247` `constraint` A closed route is never offered as a path. `src: Core features, wayfinding`
- [ ] `C-CF-248` `ui` The visitor plan carries a step-free route layer. `src: Core features, wayfinding`
- [ ] `C-CF-249` `ui` Every route drawn is also available as an ordered list of written directions. `src: Core features, wayfinding`
- [ ] `C-CF-250` `capability` A visitor arriving on the French site receives French directions. `src: Core features, wayfinding`
- [ ] `C-CF-251` `ui` The annual view shows every hall across a year on one row each. `src: Core features, annual plan`
- [ ] `C-CF-252` `ui` The annual view carries confirmed bookings, ranked options, recurring anchor events. `src: Core features, annual plan`
- [ ] `C-CF-253` `ui` The annual view carries maintenance windows, venue fair concepts, closed periods. `src: Core features, annual plan`
- [ ] `C-CF-254` `capability` A recurring event carries a provisional hold on the same week of the next year. `src: Core features, annual plan`
- [ ] `C-CF-255` `capability` A provisional hold ages into an option, then into a booking. `src: Core features, annual plan`
- [ ] `C-CF-256` `capability` Losing a recurring hold is surfaced naming the event, the week. `src: Core features, annual plan`
- [ ] `C-CF-257` `ui` The yield view shows revenue per square metre per day for any window. `src: Core features, annual plan`
- [ ] `C-CF-258` `capability` A maintenance hold occupies space exactly as an event does. `src: Core features, annual plan`
- [ ] `C-CF-259` `constraint` A maintenance hold cannot be booked over. `src: Core features, annual plan`
- [ ] `C-CF-260` `capability` A coordinator forks the annual plan, moving bookings inside the fork. `src: Core features, annual plan`
- [ ] `C-CF-261` `capability` A fork shows the conflicts, the yield difference, before any commit. `src: Core features, annual plan`
- [ ] `C-CF-262` `capability` Committing a fork applies the whole fork atomically, failing whole otherwise. `src: Core features, annual plan`
- [ ] `C-CF-263` `constraint` A partially applied scenario is refused as a violation. `src: Core features, annual plan`
- [ ] `C-CF-264` `ui` The home hero carries the display line over a full-bleed generated image behind a dark scrim. `src: Core features, public home`
- [ ] `C-CF-265` `ui` The home hero carries two actions plus a bouncing cue inviting the first scroll. `src: Core features, public home`
- [ ] `C-CF-266` `ui` The coming-soon band carries three event cards over an all-events link. `src: Core features, public home`
- [ ] `C-CF-267` `ui` The visitor band carries the practical-information paragraph plus a plan-your-visit action. `src: Core features, public home`
- [ ] `C-CF-268` `ui` The organiser band carries the versatile-venue paragraph, the fifty-years line, a nine-image gallery. `src: Core features, public home`
- [ ] `C-CF-269` `ui` The setting band carries the blank-canvas paragraph, two actions, four summary blocks. `src: Core features, public home`
- [ ] `C-CF-270` `ui` The inspiration band carries case cards each naming the halls used, over a more-events link. `src: Core features, public home`
- [ ] `C-CF-271` `ui` The stay-up-to-date band carries the newsletter invitation plus three social profiles. `src: Core features, public home`
- [ ] `C-CF-272` `ui` The newsflash band carries news cards with a category chip, a date, a read link. `src: Core features, public home`
- [ ] `C-CF-273` `ui` An event card carries a generated image, a status chip, a title, a date range, a daily time range. `src: Core features, public calendar`
- [ ] `C-CF-274` `ui` An event card carries hall chips, a sector chip, a description, outbound actions. `src: Core features, public calendar`
- [ ] `C-CF-275` `literal` The two status chips read `Open to the public`, `Trade fair - registration required`. `src: Core features, public calendar`
- [ ] `C-CF-276` `capability` Calendar filters cover month, date range, status, sector, hall. `src: Core features, public calendar`
- [ ] `C-CF-277` `capability` Filter state is carried in the address so a filtered view is shareable as a link. `src: Core features, public calendar`
- [ ] `C-CF-278` `capability` Filter state is reflected in the page title. `src: Core features, public calendar`
- [ ] `C-CF-279` `capability` A multi-day event renders once with the range of that event, never once per day. `src: Core features, public calendar`
- [ ] `C-CF-280` `capability` An event running past midnight belongs to the day that event started. `src: Core features, public calendar`
- [ ] `C-CF-281` `capability` The calendar publishes only events marked published, only after the publication date. `src: Core features, public calendar`
- [ ] `C-CF-282` `ui` A filter matching nothing shows an empty state naming the filter, offering to clear that filter. `src: Core features, public calendar`
- [ ] `C-CF-283` `ui` The spaces route carries the interactive floor plan over one specification block per space. `src: Core features, public spaces`
- [ ] `C-CF-284` `ui` A specification block names the capacity, the floor area, the unique features, the event types suited. `src: Core features, public spaces`
- [ ] `C-CF-285` `constraint` The floor plan is drawn geometry, never an image. `src: Core features, public spaces`
- [ ] `C-CF-286` `ui` Each hall is a closed region carrying the number of that hall as a text label. `src: Core features, public spaces`
- [ ] `C-CF-287` `literal` The plan regions run `1` through `6` plus `XXL` for the event hall. `src: Core features, public spaces`
- [ ] `C-CF-288` `ui` The plan carries the meeting centre, the covered boulevard, the passages between adjacent halls. `src: Core features, public spaces`
- [ ] `C-CF-289` `ui` Pointing at a region lifts that region plus the number of that region. `src: Core features, public spaces`
- [ ] `C-CF-290` `capability` Choosing a region scrolls to the specification block of that hall. `src: Core features, public spaces`
- [ ] `C-CF-291` `ui` The plan is operable region by region from the keyboard in a stated order. `src: Core features, public spaces`
- [ ] `C-CF-292` `ui` Each region announces the name, the capacity, the floor area of that hall. `src: Core features, public spaces`
- [ ] `C-CF-293` `ui` The spaces route closes with the flexible-combinations paragraph, the venue-team introduction. `src: Core features, public spaces`
- [ ] `C-CF-294` `ui` The spaces route carries six reasons organisers choose the venue, a case strip, an enquiry form. `src: Core features, public spaces`
- [ ] `C-CF-295` `ui` The meetings route carries the meeting rooms, the combinations, the audiovisual provision, a contact block. `src: Core features, public organiser`
- [ ] `C-CF-296` `ui` The catering route carries receptions, walking dinners, the self-service exhibition restaurant. `src: Core features, public organiser`
- [ ] `C-CF-297` `ui` The restaurant route carries the fast-gourmet concept plus the role of that restaurant on fair days. `src: Core features, public organiser`
- [ ] `C-CF-298` `ui` The organiser accessibility route carries road, rail, air access plus what the region offers delegates. `src: Core features, public organiser`
- [ ] `C-CF-299` `ui` The unique-events route carries the case studies, one page per case naming the spaces used. `src: Core features, public organiser`
- [ ] `C-CF-300` `ui` The visit hub carries accessibility, parking, food, drink, the city, the questions accordion. `src: Core features, public visit`
- [ ] `C-CF-301` `ui` Visitor pages carry large touch targets, nothing depending on hover, practical facts above the fold. `src: Core features, public visit`
- [ ] `C-CF-302` `ui` The about hub carries who we are, the fifty-year history, sustainability, safety, the media kit. `src: Core features, public about`
- [ ] `C-CF-303` `capability` The media kit carries downloadable logos, floor plans, the safety manual behind a resolving anchor. `src: Core features, public about`
- [ ] `C-CF-304` `ui` The news index carries cards with category chips, dates, plus an article page per item. `src: Core features, public news`
- [ ] `C-CF-305` `capability` An article published in one language stays visible in the others, labelled as another language. `src: Core features, public news`
- [ ] `C-CF-306` `constraint` An untranslated article is never silently omitted from a language. `src: Core features, public news`
- [ ] `C-CF-307` `ui` The contact route carries a first name, a last name, an email, an event kind, a date range. `src: Core features, public contact`
- [ ] `C-CF-308` `ui` The contact route carries an expected visitor count plus the spaces of interest. `src: Core features, public contact`
- [ ] `C-CF-309` `ui` The contact form states what happens next after submission. `src: Core features, public contact`
- [ ] `C-CF-310` `ui` The legal routes carry the general conditions, the privacy policy, the cookie policy, each dated. `src: Core features, public legal`
- [ ] `C-CF-311` `capability` The cookie policy is generated from the consent declaration rather than hand-written. `src: Core features, public legal`
- [ ] `C-CF-312` `capability` A consent banner gates a statistics category, a marketing category, over a necessary category. `src: Core features, consent`
- [ ] `C-CF-313` `constraint` The necessary consent category cannot be refused. `src: Core features, consent`
- [ ] `C-CF-314` `capability` Nothing in the statistics category loads until statistics consent is given. `src: Core features, consent`
- [ ] `C-CF-315` `capability` Nothing in the marketing category loads until marketing consent is given. `src: Core features, consent`
- [ ] `C-CF-316` `capability` Withdrawing consent stops the withdrawn category from then on. `src: Core features, consent`
- [ ] `C-CF-317` `data` A consent record carries an identity plus a date. `src: Core features, consent`
- [ ] `C-CF-318` `ui` The cookie policy lists every cookie by provider, purpose, retention, kind. `src: Core features, consent`
- [ ] `C-CF-319` `data` A page view record carries the route, the language, the time. `src: Core features, consent`
- [ ] `C-CF-320` `constraint` A page view record never carries an identifier for the person. `src: Core features, consent`
- [ ] `C-CF-321` `capability` No page view is recorded at all for as long as statistics consent is absent. `src: Core features, consent`
- [ ] `C-CF-322` `capability` The reporting surface shows page views per route, per language, over a window. `src: Core features, consent`
- [ ] `C-CF-323` `constraint` The reported page view figure agrees with the page view records exactly. `src: Core features, consent`
- [ ] `C-CF-324` `literal` The search overlay carries one field labelled `Search entire website`. `src: Core features, search`
- [ ] `C-CF-325` `capability` Search covers page content, event titles, news, in the language the visitor reads. `src: Core features, search`
- [ ] `C-CF-326` `ui` A search matching nothing offers the calendar, the spaces route, rather than a dead end. `src: Core features, search`
- [ ] `C-CF-327` `literal` A newsletter capture answers exactly one of `sent`, `invalid`, `already`. `src: Core features, newsletter`
- [ ] `C-CF-328` `capability` The same address twice answers `already` rather than creating a second subscription. `src: Core features, newsletter`
- [ ] `C-CF-329` `capability` The language switcher preserves the current page plus the parameters of that page. `src: Core features, language`
- [ ] `C-CF-330` `capability` Switching language on a hall page lands on the same hall in the new language. `src: Core features, language`
- [ ] `C-CF-331` `capability` Switching language on a filtered calendar keeps the filter. `src: Core features, language`
- [ ] `C-CF-332` `constraint` Returning the reader to the home page on a language switch is refused as a violation. `src: Core features, language`
- [ ] `C-CF-333` `literal` Every public route exists under the prefixes `nl`, `fr`, `en`. `src: Core features, language`
- [ ] `C-CF-334` `capability` Each page declares the language that page is written in. `src: Core features, language`
- [ ] `C-CF-335` `capability` An unknown address under any language prefix is answered as not found. `src: Core features, not-found`
- [ ] `C-CF-336` `ui` The not-found screen renders in the language of the prefix requested. `src: Core features, not-found`
- [ ] `C-CF-337` `ui` The not-found screen carries a route home plus a search field. `src: Core features, not-found`
- [ ] `C-CF-338` `capability` Every internal link on the not-found screen resolves. `src: Core features, not-found`

## C-UF User flow

- [ ] `C-UF-01` `literal` The public routes exist under the three language prefixes `nl`, `fr`, `en`. `src: User flow, routes`
- [ ] `C-UF-02` `literal` The public route set carries `/LANG`, `/LANG/calendar`, `/LANG/visit`, `/LANG/organize`, `/LANG/about`, `/LANG/news`, `/LANG/contact`. `src: User flow, routes`
- [ ] `C-UF-03` `literal` The visit routes carry `/LANG/visit/accessibility-parking`, `/LANG/visit/food-drinks`, `/LANG/visit/what-to-do-city`, `/LANG/visit/frequently-asked-questions`. `src: User flow, routes`
- [ ] `C-UF-04` `literal` The organiser routes carry `/LANG/organize/spaces`, `/LANG/organize/meetings`, `/LANG/organize/catering`, `/LANG/organize/orangery-kitchen`, `/LANG/organize/accessibility-region`, `/LANG/organize/unique-events`. `src: User flow, routes`
- [ ] `C-UF-05` `literal` The about routes carry `/LANG/about/who-are-we`, `/LANG/about/history`, `/LANG/about/sustainability-safety`, `/LANG/about/media-kit-documents`. `src: User flow, routes`
- [ ] `C-UF-06` `literal` The legal routes carry `/LANG/general-conditions`, `/LANG/privacy-policy`, `/LANG/cookies`. `src: User flow, routes`
- [ ] `C-UF-07` `literal` The remaining public routes carry `/LANG/news/newsletter`, `/LANG/search`, `/LANG/wayfinding/:event`, `/robots.txt`, `/sitemap.xml`. `src: User flow, routes`
- [ ] `C-UF-08` `literal` The console routes carry `/signin`, `/console`, `/console/enquiries`, `/console/options`, `/console/bookings/:id`, `/console/plans/:id`. `src: User flow, routes`
- [ ] `C-UF-09` `literal` The console routes carry `/console/accreditation`, `/console/access`, `/console/safety`, `/console/works`, `/console/services`. `src: User flow, routes`
- [ ] `C-UF-10` `literal` The console routes carry `/console/invoices`, `/console/publish`, `/console/annual`, `/console/reports`, `/console/audit`, `/portal`. `src: User flow, routes`
- [ ] `C-UF-11` `capability` An anonymous caller opening a console route is served `/signin` with the requested address remembered. `src: User flow, entry`
- [ ] `C-UF-12` `capability` A coordinator with no remembered address lands on `/console` after signing in. `src: User flow, entry`
- [ ] `C-UF-13` `capability` An operations account with no remembered address lands on `/console/safety` after signing in. `src: User flow, entry`
- [ ] `C-UF-14` `capability` An exhibitor with no remembered address lands on `/portal` after signing in. `src: User flow, entry`
- [ ] `C-UF-15` `capability` Signing out returns to the language home last used, stopping the token at once. `src: User flow, entry`
- [ ] `C-UF-16` `capability` A principal opening a route the role of that principal lacks is told plainly the surface is not theirs. `src: User flow, entry`
- [ ] `C-UF-17` `ui` A principal refused a route is offered a route back to one the role of that principal holds. `src: User flow, entry`
- [ ] `C-UF-18` `constraint` A principal refused a route is never shown an empty version of that route. `src: User flow, entry`
- [ ] `C-UF-19` `ui` Every list surface carries an empty state naming the one next action of that surface. `src: User flow, states`
- [ ] `C-UF-20` `constraint` An empty state rendering nothing is an unfinished screen. `src: User flow, states`
- [ ] `C-UF-21` `ui` Every page carries a loading state; every list carries a skeleton reserving the row space. `src: User flow, states`
- [ ] `C-UF-22` `ui` Refused, empty, loading, degraded, error are five states that look different from one another. `src: User flow, states`
- [ ] `C-UF-23` `constraint` A space nobody may see never renders the same way as a space holding nothing. `src: User flow, states`
- [ ] `C-UF-24` `capability` An error anywhere is caught, stated in words, recoverable. `src: User flow, states`
- [ ] `C-UF-25` `constraint` An error never replaces the page with a stack trace. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The public north star is a large working building with a team behind that building. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The console north star is comprehension: which square metres are held, by whom, until when. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The public register may carry atmosphere, putting the subject first. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` The console register is quiet, utilitarian, dense but organised, built for repeated action. `src: UI/UX notes`
- [ ] `C-UX-05` `constraint` The console carries no oversized hero, no editorial composition, no decoration standing in for content. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` The public page ground is a near-white neutral. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` A mid, vivid red carries primary actions, links, accents, exclusively. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` A deep, muted red carries every line of body text. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` A light, vivid red carries hover, secondary accent, with a deeper sibling for the pressed state. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` A tertiary wash of the light red carries selection, soft fills, appearing in no other role. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Three neutrals below the ground carry secondary text, tertiary text, hairlines, dividers. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` A mid, soft red carries validation failure over a near-white warm neutral wash. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Two support washes carry meaning in the calendar, in notices: a near-white soft orange, a near-white muted red. `src: UI/UX notes`
- [ ] `C-UX-14` `constraint` A state meaning none of the three signalled meanings borrows none of the colours of those meanings. `src: UI/UX notes`
- [ ] `C-UX-15` `ui` A console panel sits a shade above the page; a recessed well a shade below. `src: UI/UX notes`
- [ ] `C-UX-16` `constraint` No occupancy state is signalled by colour alone. `src: UI/UX notes`
- [ ] `C-UX-17` `ui` One variable geometric sans carries everything, with a metrically matched system fallback. `src: UI/UX notes`
- [ ] `C-UX-18` `ui` Figures line up in a column wherever capacities, areas, amounts stack. `src: UI/UX notes`
- [ ] `C-UX-19` `ui` Hairline borders do most of the depth work, with one soft shadow lifting a raised card. `src: UI/UX notes`
- [ ] `C-UX-20` `ui` The status chip is the only fully rounded shape in the product. `src: UI/UX notes`
- [ ] `C-UX-21` `ui` Motion moves on a single decelerating settle at one speed everywhere. `src: UI/UX notes`
- [ ] `C-UX-22` `ui` Section content rises, fading in, as a band enters the viewport, once per band. `src: UI/UX notes`
- [ ] `C-UX-23` `constraint` Nothing uses a different transition speed to feel special. `src: UI/UX notes`
- [ ] `C-UX-24` `capability` Motion is enabled only where the device of the reader asks for movement. `src: UI/UX notes`
- [ ] `C-UX-25` `capability` Under the reduced state no reveal, bounce, settle, slide animation runs at all. `src: UI/UX notes`
- [ ] `C-UX-26` `ui` The public surface is spacious, with band gaps several times the gap beneath a heading. `src: UI/UX notes`
- [ ] `C-UX-27` `ui` The console is compact, so a full week of a hall fits one screen. `src: UI/UX notes`
- [ ] `C-UX-28` `contract` Text, interface components, the focus indicator meet WCAG AA contrast in both surfaces. `src: UI/UX notes`
- [ ] `C-UX-29` `contract` Touch targets are at least 44 by 44 device-independent pixels. `src: UI/UX notes`
- [ ] `C-UX-30` `contract` Public body text never falls below 16 pixels. `src: UI/UX notes`
- [ ] `C-UX-31` `capability` Every interaction is reachable by keyboard navigation with a visible focus ring. `src: UI/UX notes`
- [ ] `C-UX-32` `constraint` Meaning is never carried by colour alone. `src: UI/UX notes`
- [ ] `C-UX-33` `capability` Every icon-only control carries an accessible name. `src: UI/UX notes`
- [ ] `C-UX-34` `ui` The floor plan regions are focusable in a stated order, announcing name, capacity, area. `src: UI/UX notes`
- [ ] `C-UX-35` `ui` The campus timeline announces the space, the window a row represents. `src: UI/UX notes`
- [ ] `C-UX-36` `ui` Safety board alerts are announced as words, not only coloured. `src: UI/UX notes`
- [ ] `C-UX-37` `ui` Overlays move focus in, hold focus, return focus where that focus came from. `src: UI/UX notes`
- [ ] `C-UX-38` `capability` The public site reflows to a narrow viewport in all three languages. `src: UI/UX notes`
- [ ] `C-UX-39` `constraint` Navigation labels, chips, buttons must not wrap in the wordiest of the three languages. `src: UI/UX notes`
- [ ] `C-UX-40` `capability` The floor plan on a phone becomes a pannable, pinch-zoomable region list. `src: UI/UX notes`
- [ ] `C-UX-41` `capability` Every hall specification stays reachable without the plan. `src: UI/UX notes`
- [ ] `C-UX-42` `ui` Calendar filters collapse into a sheet; cards stack keeping the status chip, dates, hall chips visible. `src: UI/UX notes`
- [ ] `C-UX-43` `ui` Access control, the safety board, incident raising are laid out for gloved one-handed use. `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The layout is checked at a wide desktop width, a small tablet width, a phone width. `src: Front-end specification`
- [ ] `C-FE-02` `ui` Four rhythm steps interpolate smoothly with the viewport between a lower bound, an upper bound. `src: Front-end specification`
- [ ] `C-FE-03` `ui` Section padding uses the same rhythm ladder as the gaps. `src: Front-end specification`
- [ ] `C-FE-04` `constraint` Flattening the rhythm ladder to fixed values is refused as a violation. `src: Front-end specification`
- [ ] `C-FE-05` `ui` The breakpoint ladder carries phone, large phone, small tablet, tablet, small desktop, desktop, wide, very wide tiers. `src: Front-end specification`
- [ ] `C-FE-06` `ui` The tablet tier is where the navigation collapses. `src: Front-end specification`
- [ ] `C-FE-07` `ui` A stated maximum width caps the reading column on the legal routes. `src: Front-end specification`
- [ ] `C-FE-08` `capability` Motion is gated positively on a preference for movement rather than negatively. `src: Front-end specification`
- [ ] `C-FE-09` `capability` Hover styling sits behind a pointer-capability branch rather than a width branch. `src: Front-end specification`
- [ ] `C-FE-10` `ui` The stacking order is a closed named ladder from ambient backdrop to skip link. `src: Front-end specification`
- [ ] `C-FE-11` `constraint` No element may compete with the overlay range by choosing an arbitrarily large number. `src: Front-end specification`
- [ ] `C-FE-12` `ui` Layer one holds one neutral ladder plus one brand ladder, with the support washes, the validation pair. `src: Front-end specification`
- [ ] `C-FE-13` `ui` Layer two holds semantic roles named for the job of each rather than for the colour. `src: Front-end specification`
- [ ] `C-FE-14` `ui` The console redefines layer two, leaving layer one untouched, leaving layer three untouched. `src: Front-end specification`
- [ ] `C-FE-15` `ui` Layer three holds a full state set per interactive component rather than an opacity drop. `src: Front-end specification`
- [ ] `C-FE-16` `ui` The state set covers the solid button, the outline button, the text button, the navigation item. `src: Front-end specification`
- [ ] `C-FE-17` `ui` The state set covers the status chip, the form field, the floor-plan region. `src: Front-end specification`
- [ ] `C-FE-18` `constraint` Unavailable is never signalled by colour alone. `src: Front-end specification`
- [ ] `C-FE-19` `literal` The typeface family is `Inter`, loaded from a hosted service with a stated swap behaviour. `src: Front-end specification`
- [ ] `C-FE-20` `constraint` No licensed typeface file ships. `src: Front-end specification`
- [ ] `C-FE-21` `literal` Body copy is set at `16px` on a `24px` line. `src: Front-end specification`
- [ ] `C-FE-22` `literal` The dense interface band is set at `15px` on a `24px` line. `src: Front-end specification`
- [ ] `C-FE-23` `literal` Fine print is set at `14px` on a `21px` line. `src: Front-end specification`
- [ ] `C-FE-24` `literal` Micro-labels are set at `12px` on a `14.4px` line. `src: Front-end specification`
- [ ] `C-FE-25` `literal` Card titles are set at `20px` on a `30px` line. `src: Front-end specification`
- [ ] `C-FE-26` `literal` Compact heads are set at `18px` on an `18px` line. `src: Front-end specification`
- [ ] `C-FE-27` `ui` The display ladder interpolates with the viewport rather than stepping. `src: Front-end specification`
- [ ] `C-FE-28` `ui` Tracking tightens as size grows, opening as size shrinks. `src: Front-end specification`
- [ ] `C-FE-29` `ui` Figures are tabular wherever capacities, areas, occupancy counts, money stack. `src: Front-end specification`
- [ ] `C-FE-30` `ui` The wordmark is drawn geometry carrying an accessible name. `src: Front-end specification`
- [ ] `C-FE-31` `constraint` Interface glyphs are a drawn stroke set, never an icon font. `src: Front-end specification`
- [ ] `C-FE-32` `literal` The glyph set is chevron, arrow, close, search, menu, calendar, location pin, clock, download, external link, three social marks. `src: Front-end specification`
- [ ] `C-FE-33` `ui` A glyph carries a title where meaningful, hidden from assistive technology where decorative. `src: Front-end specification`
- [ ] `C-FE-34` `ui` The floor plan is one piece of inline geometry with the campus outline plus sibling regions. `src: Front-end specification`
- [ ] `C-FE-35` `ui` A decorative second piece of drawn geometry carries the angled background form of the spaces route. `src: Front-end specification`
- [ ] `C-FE-36` `capability` Plan regions are generated from the space records rather than hand-drawn. `src: Front-end specification`
- [ ] `C-FE-37` `ui` Status chips, sector chips are pill labels carrying words. `src: Front-end specification`
- [ ] `C-FE-38` `ui` The header carries a slim utility strip above the main bar. `src: Front-end specification`
- [ ] `C-FE-39` `literal` The utility strip holds `Jobs`, `Northtide Venues Group`, `nl`, `fr`, `en`. `src: Front-end specification`
- [ ] `C-FE-40` `literal` The main bar holds `Calendar`, `Visit`, `Organize`, `About Verwick Xpo`, `News`, `Contact`. `src: Front-end specification`
- [ ] `C-FE-41` `ui` Three main-bar items open a panel of child links. `src: Front-end specification`
- [ ] `C-FE-42` `ui` Below the tablet tier the navigation collapses into a sheet keeping the same order. `src: Front-end specification`
- [ ] `C-FE-43` `ui` A submenu inside the sheet is a push with a back control rather than an expand. `src: Front-end specification`
- [ ] `C-FE-44` `ui` The footer carries the wordmark, the charter mark, the copyright line, four legal links. `src: Front-end specification`
- [ ] `C-FE-45` `literal` The four footer legal links read `General terms & conditions`, `Safety manual`, `Privacy policy`, `Cookie Policy`. `src: Front-end specification`
- [ ] `C-FE-46` `capability` The safety manual link is directed at the media kit document anchor, which resolves. `src: Front-end specification`
- [ ] `C-FE-47` `ui` Breadcrumbs appear on every inner page, naming the path the reader took. `src: Front-end specification`
- [ ] `C-FE-48` `ui` Buttons come in solid, outline, text-with-arrow treatments sharing one geometry. `src: Front-end specification`
- [ ] `C-FE-49` `ui` Every button treatment carries resting, pointed-at, pressed, focused, unavailable states. `src: Front-end specification`
- [ ] `C-FE-50` `ui` Carousels carry keyboard controls plus honest pagination reporting the real count. `src: Front-end specification`
- [ ] `C-FE-51` `ui` The lightbox traps focus, returning focus where that focus came from. `src: Front-end specification`
- [ ] `C-FE-52` `capability` The consent dialog cannot be dismissed into acceptance. `src: Front-end specification`
- [ ] `C-FE-53` `capability` Closing the consent dialog without choosing leaves the optional categories refused. `src: Front-end specification`
- [ ] `C-FE-54` `ui` The calendar route is a filter rail over a card grid, becoming a sheet over a stack when narrow. `src: Front-end specification`
- [ ] `C-FE-55` `literal` A specification block carries the labelled fields `Capacity`, `Surface area`, `Unique features`, `Suitable for`. `src: Front-end specification`
- [ ] `C-FE-56` `ui` The console routes are a persistent desk rail, a working surface, a contextual panel. `src: Front-end specification`
- [ ] `C-FE-57` `ui` One easing carries the whole product: a strong decelerating settle. `src: Front-end specification`
- [ ] `C-FE-58` `constraint` There is no second easing anywhere in the product. `src: Front-end specification`
- [ ] `C-FE-59` `ui` The scroll reveal rises a short distance, fading in, once per band, then stays arrived. `src: Front-end specification`
- [ ] `C-FE-60` `ui` The hero cue translates a short distance downward, then back, continuously. `src: Front-end specification`
- [ ] `C-FE-61` `ui` The attention settle rotates one element a few degrees, then settles back. `src: Front-end specification`
- [ ] `C-FE-62` `ui` Carousel slides are horizontal, vertical slide-in, slide-out pairs offset by the carousel gap. `src: Front-end specification`
- [ ] `C-FE-63` `ui` The lightbox zoom enters scaling up from slightly undersized, rising a short distance. `src: Front-end specification`
- [ ] `C-FE-64` `ui` A progress bar scales from nothing to full for carousel, gallery progress. `src: Front-end specification`
- [ ] `C-FE-65` `ui` A rotation loop carries every loading state at one speed everywhere. `src: Front-end specification`
- [ ] `C-FE-66` `ui` A row changing under the reader is marked briefly rather than silently replaced. `src: Front-end specification`
- [ ] `C-FE-67` `capability` Under the reduced state the progress bar jumps to the value of that bar. `src: Front-end specification`
- [ ] `C-FE-68` `capability` Under the reduced state the live-change marker is static rather than fading. `src: Front-end specification`
- [ ] `C-FE-69` `ui` The campus timeline scrolls horizontally when narrow with the space column pinned. `src: Front-end specification`
- [ ] `C-FE-70` `ui` The three floor surfaces carry targets well above the minimum, within thumb reach. `src: Front-end specification`
- [ ] `C-FE-71` `contract` The three floor surfaces carry contrast surviving direct sunlight. `src: Front-end specification`
- [ ] `C-FE-72` `ui` Each view declares one main landmark, a banner landmark, a contentinfo landmark. `src: Front-end specification`
- [ ] `C-FE-73` `ui` Navigation landmarks are labelled individually where more than one exists. `src: Front-end specification`
- [ ] `C-FE-74` `ui` Each view carries exactly one first-level heading, skipping no level below that heading. `src: Front-end specification`
- [ ] `C-FE-75` `constraint` Where a control carries a visible label the accessible name matches that label. `src: Front-end specification`
- [ ] `C-FE-76` `capability` Each document declares the own language of that document. `src: Front-end specification`
- [ ] `C-FE-77` `capability` An element written in a different language declares the own language of that element. `src: Front-end specification`
- [ ] `C-FE-78` `capability` Every route carries a unique title leading with the page, ending with the product name. `src: Front-end specification`
- [ ] `C-FE-79` `capability` Every route carries a meta `description`. `src: Front-end specification`
- [ ] `C-FE-80` `literal` A visible skip link reading `Skip to main content` is the first focusable element on every page. `src: Front-end specification`
- [ ] `C-FE-81` `ui` Live regions announce a scan decision, an occupancy state change, a plan validation failure, a save outcome. `src: Front-end specification`
- [ ] `C-FE-82` `literal` The hero display line reads `when ideas need space`. `src: Front-end specification, copy deck`
- [ ] `C-FE-83` `literal` The hero actions read `View our calendar`, `Organize your event`. `src: Front-end specification, copy deck`
- [ ] `C-FE-84` `literal` The upcoming band reads `Coming soon to Verwick Xpo` over `All events`. `src: Front-end specification, copy deck`
- [ ] `C-FE-85` `literal` The visitor band heading reads `Are you visiting Verwick Xpo soon?` with the action `Plan your visit`. `src: Front-end specification, copy deck`
- [ ] `C-FE-86` `literal` The organiser band heading reads `Your next event at Verwick Xpo?`. `src: Front-end specification, copy deck`
- [ ] `C-FE-87` `literal` The setting band reads `The right setting for every concept` with the actions `Organize in Verwick Xpo`, `Discover the halls`. `src: Front-end specification, copy deck`
- [ ] `C-FE-88` `literal` The four building blocks read `6 halls: versatility at its best`, `Meeting center: 5 rooms, endless possibilities`, `The Concourse: covered boulevard`, `The Orangery: Fast Gourmet Kitchen`. `src: Front-end specification, copy deck`
- [ ] `C-FE-89` `literal` The inspiration band reads `Get inspired` with `More unique events`. `src: Front-end specification, copy deck`
- [ ] `C-FE-90` `literal` The newsletter band reads `Stay up to date` with `Subscribe to the newsletter`, `Follow us`. `src: Front-end specification, copy deck`
- [ ] `C-FE-91` `literal` The news band reads `Xpo Newsflash` with `All newsflashes`. `src: Front-end specification, copy deck`
- [ ] `C-FE-92` `ui` The spaces route opens with the flexible-halls heading over three actions, pinned below. `src: Front-end specification, copy deck`
- [ ] `C-FE-93` `literal` The spaces route carries `Flexible combinations tailored to you`, `Say hi to the Venue team`, `Contact us`. `src: Front-end specification, copy deck`
- [ ] `C-FE-94` `ui` The reasons band heading names the venue, carrying the flexible-spaces line, the parking line, pinned below. `src: Front-end specification, copy deck`
- [ ] `C-FE-95` `literal` The case strip heading reads `The spaces in use`. `src: Front-end specification, copy deck`
- [ ] `C-FE-96` `literal` The footer copyright line reads `(C) 2026 Verwick Xpo`. `src: Front-end specification, copy deck`
- [ ] `C-FE-97` `literal` The not-found screen carries `Page not found` plus the action `Go to homepage`. `src: Front-end specification, copy deck`
- [ ] `C-FE-98` `literal` The three case studies name `Palmarosa`, `Bookmark Fair`, plus the passage `The Transit`. `src: Front-end specification, copy deck`
- [ ] `C-FE-99` `literal` The corporate news item reads `Calderhook Group completes acquisition of Northtide Venues Group`, dated `03.08.2026`. `src: Front-end specification, copy deck`
- [ ] `C-FE-100` `literal` The sustainability news item reads `Verwick Xpo achieves the Westmark sustainability charter for the 10th consecutive year`, dated `07.07.2026`. `src: Front-end specification, copy deck`
- [ ] `C-FE-101` `capability` The sustainability news item ships with an original-language body under an English heading. `src: Front-end specification, copy deck`
- [ ] `C-FE-102` `literal` The seeded sector chips read `Architecture & Design`, `Lifestyle & Sports`, `Sustainability`. `src: Front-end specification, copy deck`
- [ ] `C-FE-103` `literal` The `Hall 4` suitability field reads `not captured` rather than an invented line. `src: Front-end specification, copy deck`
- [ ] `C-FE-104` `constraint` No binary asset ships: no typeface file, no photograph, no icon file, no texture, no video, no logo file. `src: Front-end specification, assets`
- [ ] `C-FE-105` `capability` Photography is a seeded procedural composition per subject, keyed by the slug of that subject. `src: Front-end specification, assets`
- [ ] `C-FE-106` `capability` The gallery lightbox shows the same generated composition at a larger size. `src: Front-end specification, assets`
- [ ] `C-FE-107` `capability` The media-kit documents are generated at build time from the space model, from the specification. `src: Front-end specification, assets`
- [ ] `C-FE-108` `constraint` Every image element declares the dimensions of that element in the markup. `src: Front-end specification, assets`
- [ ] `C-FE-109` `constraint` Every image carries alternative text describing the subject rather than naming a file. `src: Front-end specification, assets`
- [ ] `C-FE-110` `capability` A `favicon` is served. `src: Front-end specification, assets`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The browser receives a static production bundle on first paint. `src: Technical requirements`
- [ ] `C-TR-02` `contract` Every subsequent fact arrives as JSON from the same origin under `/api`. `src: Technical requirements`
- [ ] `C-TR-03` `contract` The backend is `NestJS` on Node 20. `src: Technical requirements`
- [ ] `C-TR-04` `contract` The frontend is `Vue 3` built by `Vite` into the production bundle. `src: Technical requirements`
- [ ] `C-TR-05` `contract` The datastore is `PostgreSQL`, reached at `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-06` `contract` Authentication is implemented by the app: email, password, hashed, bearer tokens. `src: Technical requirements`
- [ ] `C-TR-07` `contract` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements`
- [ ] `C-TR-08` `constraint` Only the libraries named in the brief plus the direct dependencies of those may be used. `src: Technical requirements`
- [ ] `C-TR-09` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced. `src: Technical requirements`
- [ ] `C-TR-10` `constraint` The backing service is already running; nothing downloads, installs, compiles, starts a copy. `src: Technical requirements`
- [ ] `C-TR-11` `constraint` No host, no port is hardcoded; every one is read from the environment. `src: Technical requirements`
- [ ] `C-TR-12` `constraint` Exactly one part of the product answers whether a space is free in a window. `src: Technical requirements`
- [ ] `C-TR-13` `constraint` Exactly one part of the product answers how many people are inside a space. `src: Technical requirements`
- [ ] `C-TR-14` `capability` Two surfaces disagreeing about one hall in one second is the observable symptom of a second authority. `src: Technical requirements`
- [ ] `C-TR-15` `capability` The plan geometry, the overlap resolver, the accreditation evaluator are separable units. `src: Technical requirements`
- [ ] `C-TR-16` `capability` The tax calculator, the phase-fit calculator are separable units taking inputs, returning answers. `src: Technical requirements`
- [ ] `C-TR-17` `constraint` Overlap, licensed capacity, accreditation validity, publication scope are enforced where the data lives. `src: Technical requirements`
- [ ] `C-TR-18` `constraint` The append-only property of the trail is enforced where the data lives. `src: Technical requirements`
- [ ] `C-TR-19` `capability` A request crafted to bypass the application layer still fails. `src: Technical requirements`
- [ ] `C-TR-20` `capability` Holds, phase changes, plan revisions, scans, occupancy, incidents reach every open surface within a second. `src: Technical requirements`
- [ ] `C-TR-21` `constraint` A live change reaches an open surface without the reader reloading the page. `src: Technical requirements`
- [ ] `C-TR-22` `capability` A burst of scans is batched so the console does not degrade. `src: Technical requirements`
- [ ] `C-TR-23` `capability` One thousand scans arriving in a minute leave the safety board responsive. `src: Technical requirements`
- [ ] `C-TR-24` `data` The space model, the layout capacities, the licence figures, the accreditation rules carry versions. `src: Technical requirements`
- [ ] `C-TR-25` `data` Every booking, plan revision, badge, invoice records the version that record was written under. `src: Technical requirements`
- [ ] `C-TR-26` `constraint` Migrations are forward-only, running once. `src: Technical requirements`
- [ ] `C-TR-27` `capability` The public calendar renders a year of events with filters applied in under a second. `src: Technical requirements`
- [ ] `C-TR-28` `constraint` The calendar reads indexed, paginated queries rather than loading the year into the browser. `src: Technical requirements`
- [ ] `C-TR-29` `capability` The planner holds a smooth frame rate at eight hundred objects. `src: Technical requirements`
- [ ] `C-TR-30` `capability` An access decision returns within a bounded time at the door, even on the degraded path. `src: Technical requirements`
- [ ] `C-TR-31` `capability` Occupancy recomputes per scan without a full recount. `src: Technical requirements`
- [ ] `C-TR-32` `constraint` Every list endpoint pages by cursor; none is unbounded. `src: Technical requirements`
- [ ] `C-TR-33` `capability` Images are served in modern formats at the sizes actually displayed. `src: Technical requirements`
- [ ] `C-TR-34` `capability` Media below the fold is deferred with the dimensions of that media declared. `src: Technical requirements`
- [ ] `C-TR-35` `capability` An error is mapped before leaving the server. `src: Technical requirements`
- [ ] `C-TR-36` `constraint` A refusal by the product stays distinct from a failure inside a backing service. `src: Technical requirements`
- [ ] `C-TR-37` `constraint` No response body, log line, error body, audit record carries a credential, a token, a stack trace. `src: Technical requirements`
- [ ] `C-TR-38` `capability` A request identifier is generated at the edge, attached to every log line, returned on every error. `src: Technical requirements`
- [ ] `C-TR-39` `constraint` A parameter is logged by name, by type, never by value. `src: Technical requirements`
- [ ] `C-TR-40` `contract` Every response carries a security header set with a content policy forbidding inline script. `src: Technical requirements`
- [ ] `C-TR-41` `contract` The security header set carries a strict transport policy, a frame-ancestors refusal. `src: Technical requirements`
- [ ] `C-TR-42` `contract` The security header set carries a referrer policy, a nosniff declaration, a permissions policy. `src: Technical requirements`
- [ ] `C-TR-43` `capability` State-changing requests are protected against cross-site forgery. `src: Technical requirements`
- [ ] `C-TR-44` `constraint` No state change happens on a GET. `src: Technical requirements`
- [ ] `C-TR-45` `contract` Session cookies are http-only, same-site. `src: Technical requirements`
- [ ] `C-TR-46` `constraint` Free text reaching a page is rendered as text. `src: Technical requirements`
- [ ] `C-TR-47` `capability` Uploads are validated server-side, served through short-lived signed links. `src: Technical requirements`
- [ ] `C-TR-48` `constraint` No secret value is returned by a read path, embedded in a bundled asset. `src: Technical requirements`
- [ ] `C-TR-49` `constraint` Personal data is collected only where the safety regime, the law requires. `src: Technical requirements`
- [ ] `C-TR-50` `capability` Personal data is minimised, encrypted at rest, cleared on the stated retention schedule. `src: Technical requirements`
- [ ] `C-TR-51` `constraint` The audit trail is append-only where the data lives rather than by convention. `src: Technical requirements`
- [ ] `C-TR-52` `data` The trail covers accreditation grants, revocations, capacity changes, plan approvals, publication changes. `src: Technical requirements`
- [ ] `C-TR-53` `data` The trail covers access-rule changes, invoice adjustments, evacuation declarations. `src: Technical requirements`
- [ ] `C-TR-54` `data` Every trail row carries the actor, the time, the before value, the after value. `src: Technical requirements`
- [ ] `C-TR-55` `capability` `sitemap.xml` is generated from the published public routes across all three languages. `src: Technical requirements`
- [ ] `C-TR-56` `capability` `robots.txt` names the sitemap. `src: Technical requirements`
- [ ] `C-TR-57` `capability` Every public route carries a canonical address. `src: Technical requirements`
- [ ] `C-TR-58` `constraint` A mutating call crossing a boundary carries a key derived from the logical operation. `src: Technical requirements`
- [ ] `C-TR-59` `constraint` An idempotency key is never derived from the clock, never from a value generated at send time. `src: Technical requirements`
- [ ] `C-TR-60` `capability` A repeated idempotency key returns the first result rather than acting again. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `constraint` All timestamps are UTC, rendered in the venue zone. `src: Data model`
- [ ] `C-DM-02` `capability` The twice-yearly clock change is handled for a build-up window running overnight. `src: Data model`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model`
- [ ] `C-DM-04` `literal` The seeded accounts are written into `/app/USER_README.md` so a person can sign in. `src: Data model`
- [ ] `C-DM-05` `constraint` Money is held in integer minor units of `usd`, so fourteen thousand five hundred dollars is `1450000`. `src: Data model`
- [ ] `C-DM-06` `data` A principal carries an id, a unique email, a role, a password hash, a party link, a status. `src: Data model`
- [ ] `C-DM-07` `literal` A principal role is one of `coordinator`, `operations`, `planner`, `exhibitor`, `finance`, `auditor`. `src: Data model`
- [ ] `C-DM-08` `data` A party carries a unique name, a kind, a self-referential parent link for delegation. `src: Data model`
- [ ] `C-DM-09` `capability` The party parent link is checked for cycles when written. `src: Data model`
- [ ] `C-DM-10` `data` A space carries a unique name, a kind, a floor area, an entrance set, geometry, a version. `src: Data model`
- [ ] `C-DM-11` `data` Combination membership lives in a members table joining a combination to a member space. `src: Data model`
- [ ] `C-DM-12` `constraint` Floor area is a stored fact, never the source of a capacity. `src: Data model`
- [ ] `C-DM-13` `data` A layout row carries a space, a name, a licensed capacity, build hours, a version, an effective date. `src: Data model`
- [ ] `C-DM-14` `constraint` A combination carries own layout rows rather than inheriting the rows of the members. `src: Data model`
- [ ] `C-DM-15` `data` A hold carries a space, a window, a kind, a rank, a state, an expiry, a creator. `src: Data model`
- [ ] `C-DM-16` `literal` A hold kind is one of `option`, `booking`, `maintenance`. `src: Data model`
- [ ] `C-DM-17` `capability` A hold on any node blocks every ancestor, every descendant of that node in the same window. `src: Data model`
- [ ] `C-DM-18` `data` An enquiry carries a contact name, a contact email, a window, an expected count, an event type, a source. `src: Data model`
- [ ] `C-DM-19` `literal` An enquiry source is `public_form` or `sales`. `src: Data model`
- [ ] `C-DM-20` `data` An option carries an enquiry link, a space set, a window, a rank, a state, an expiry. `src: Data model`
- [ ] `C-DM-21` `data` A challenge carries a challenger option, a holder option, an opening time, a window end, an outcome. `src: Data model`
- [ ] `C-DM-22` `data` A booking carries an option link, a party, a contract, a layout, a state. `src: Data model`
- [ ] `C-DM-23` `data` A phase carries a booking, a kind, a window start, a window end. `src: Data model`
- [ ] `C-DM-24` `constraint` A phase row is a hold on the space of that phase exactly as a run row is. `src: Data model`
- [ ] `C-DM-25` `data` A contract carries a booking, terms, a signature time, a deposit schedule. `src: Data model`
- [ ] `C-DM-26` `data` An amendment carries a contract, a requester, an approver, what moved, a decision time. `src: Data model`
- [ ] `C-DM-27` `data` A resource carries a name, a kind, a capacity, a competence set. `src: Data model`
- [ ] `C-DM-28` `literal` A resource kind is one of `dock`, `lift`, `forklift`, `crew`, `power_drop`. `src: Data model`
- [ ] `C-DM-29` `data` A work order carries a booking, a plan revision, a resource, a required competence, a window, a state. `src: Data model`
- [ ] `C-DM-30` `data` A plan revision carries a plan, a sequence, a state, an approver, an approval time. `src: Data model`
- [ ] `C-DM-31` `data` A plan object carries a revision, a kind, a party, a position, dimensions, an optional stand reference. `src: Data model`
- [ ] `C-DM-32` `data` A plan constraint carries a space, a kind, geometry, a limit value. `src: Data model`
- [ ] `C-DM-33` `literal` A plan constraint kind is one of `column`, `truss`, `door`, `fire_exit`, `rigging_point`, `power_point`, `water_point`. `src: Data model`
- [ ] `C-DM-34` `data` An accreditation carries a party, a person reference, a booking, phase kinds, a space set, a granter link. `src: Data model`
- [ ] `C-DM-35` `data` An accreditation carries a state, a valid-from time, a valid-until time. `src: Data model`
- [ ] `C-DM-36` `capability` The granter link is what the cascade walks, bounding a delegated right. `src: Data model`
- [ ] `C-DM-37` `data` An evidence row carries an accreditation, a kind, an expiry. `src: Data model`
- [ ] `C-DM-38` `data` A badge carries an accreditation, a person reference, an issue time, a validity end, a state. `src: Data model`
- [ ] `C-DM-39` `data` A scan carries a badge, an entrance, a decision, a reason, a time, an offline marker, a reconciliation time. `src: Data model`
- [ ] `C-DM-40` `constraint` The scan table is append-only where the data lives. `src: Data model`
- [ ] `C-DM-41` `data` An entrance carries a unique name, a space set, an exit marker. `src: Data model`
- [ ] `C-DM-42` `data` An entrance mode row carries an entrance, a booking, a phase kind, a mode. `src: Data model`
- [ ] `C-DM-43` `data` An occupancy sample carries a space, a count, a state, a time. `src: Data model`
- [ ] `C-DM-44` `constraint` An occupancy count is derived from the scan graph rather than from a per-door tally. `src: Data model`
- [ ] `C-DM-45` `data` An incident carries a booking, a type, a plan position, an urgency level, an owner, an open time. `src: Data model`
- [ ] `C-DM-46` `data` An incident carries a close time, a close-out note, plus an action timeline beside that incident. `src: Data model`
- [ ] `C-DM-47` `data` An evacuation carries a declaring account, a declaration time, a stand-down time, a log freeze point. `src: Data model`
- [ ] `C-DM-48` `data` A service carries a name, a category, a unit, a unit price, a lead time, a cut-off phase, a cut-off offset. `src: Data model`
- [ ] `C-DM-49` `literal` A service category is one of `catering`, `technical`, `furniture`, `cleaning`, `waste`, `signage`, `parking`. `src: Data model`
- [ ] `C-DM-50` `data` A service row carries an approved-plan requirement flag, a plan-position requirement flag. `src: Data model`
- [ ] `C-DM-51` `data` A service order carries a booking, a party, a service, a quantity, a state, a surcharge, an approver. `src: Data model`
- [ ] `C-DM-52` `data` A service order carries a plan object link, a headcount, dietary requirements, a service window. `src: Data model`
- [ ] `C-DM-53` `data` An invoice carries a booking, a party, a state, an issue time, a total in minor units. `src: Data model`
- [ ] `C-DM-54` `data` An invoice line carries a description, a quantity, a unit price, a tax rule, a tax amount, a rounding amount. `src: Data model`
- [ ] `C-DM-55` `data` An invoice line carries a line amount plus an optional variance cause. `src: Data model`
- [ ] `C-DM-56` `data` A payment carries an invoice, a kind, an amount, a receipt time, a unique external reference. `src: Data model`
- [ ] `C-DM-57` `literal` A payment kind is one of `deposit`, `stage`, `final`, `credit`. `src: Data model`
- [ ] `C-DM-58` `data` A publication carries a booking, a state, a publish time, the public field set. `src: Data model`
- [ ] `C-DM-59` `data` A translation carries a publication, a language, a field, a value, a state. `src: Data model`
- [ ] `C-DM-60` `literal` A translation state is one of `missing`, `draft`, `published`. `src: Data model`
- [ ] `C-DM-61` `constraint` The public projection reads the publication table, the translation table, nothing else. `src: Data model`
- [ ] `C-DM-62` `data` A page view carries a route, a language, a time. `src: Data model`
- [ ] `C-DM-63` `data` A consent row carries a reference, a statistics decision, a marketing decision, a decision time. `src: Data model`
- [ ] `C-DM-64` `data` An audit event carries a sequence, an actor, an action, a target, a before value, an after value, a time. `src: Data model`
- [ ] `C-DM-65` `constraint` An update against the audit table is refused where the data lives. `src: Data model`
- [ ] `C-DM-66` `constraint` Availability state, live occupancy, invoice totals, reporting figures are derived on read. `src: Data model`
- [ ] `C-DM-67` `constraint` No derived figure is a stored summary that can drift. `src: Data model`
- [ ] `C-DM-68` `literal` The seeded spaces are `Hall 1`, `Hall 2`, `Hall 3`, `Hall 4`, `Hall 5`, `Hall 6`, `The Event Hall`, `MC 1`, `MC 2`, `MC 3`, `MC 4`, `The Concourse`, `The Transit`. `src: Data model, seed`
- [ ] `C-DM-69` `literal` `Hall 1` carries `6090` square metres licensing `1620`. `src: Data model, seed`
- [ ] `C-DM-70` `literal` `Hall 2` carries `4058` square metres licensing `1740`. `src: Data model, seed`
- [ ] `C-DM-71` `literal` `Hall 3` carries `3601` square metres licensing `1680`. `src: Data model, seed`
- [ ] `C-DM-72` `literal` `Hall 4` carries `7685` square metres licensing `3660`. `src: Data model, seed`
- [ ] `C-DM-73` `literal` `Hall 5` carries `4723` square metres licensing `5160`. `src: Data model, seed`
- [ ] `C-DM-74` `literal` `Hall 6` carries `5055` square metres licensing `1860`. `src: Data model, seed`
- [ ] `C-DM-75` `literal` `The Event Hall` carries `2000` square metres licensing `2000`, with a tribune seating `550`. `src: Data model, seed`
- [ ] `C-DM-76` `literal` The four meeting rooms total `1679` square metres. `src: Data model, seed`
- [ ] `C-DM-77` `capability` `Hall 5` licenses more people than `Hall 4` on less floor area. `src: Data model, seed`
- [ ] `C-DM-78` `capability` The combination of the two largest halls plus the passage licenses a stored figure below the sum, pinned below. `src: Data model, seed`
- [ ] `C-DM-79` `literal` The combination `The Meeting Centre with the Event Hall` licenses `2600`. `src: Data model, seed`
- [ ] `C-DM-80` `literal` The seeded entrances are `North Entrance`, `South Entrance`, `Concourse East`, `Concourse West`, `Dock Gate`. `src: Data model, seed`
- [ ] `C-DM-81` `literal` Parking carries `2500` spaces. `src: Data model, seed`
- [ ] `C-DM-82` `literal` The seeded parties beyond the venue are `Palmarosa`, `Bookmark Fair`, `Ironwood Interiors`. `src: Data model, seed`
- [ ] `C-DM-83` `capability` The parent party of `Ironwood Interiors` is `Bookmark Fair`. `src: Data model, seed`
- [ ] `C-DM-84` `literal` The seeded bookings are `Verwick Design Days`, `Bookmark Fair`, `Ironwood Night`. `src: Data model, seed`
- [ ] `C-DM-85` `capability` `Verwick Design Days` holds the combination of two halls plus the passage between those halls. `src: Data model, seed`
- [ ] `C-DM-86` `capability` `Bookmark Fair` holds four halls, the four meeting rooms, the event hall. `src: Data model, seed`
- [ ] `C-DM-87` `capability` `Ironwood Night` carries the publication state `private`, so no public surface shows that booking. `src: Data model, seed`
- [ ] `C-DM-88` `capability` Each seeded booking carries five phases. `src: Data model, seed`
- [ ] `C-DM-89` `capability` A maintenance hold on `Hall 3` blocks any booking over that window. `src: Data model, seed`
- [ ] `C-DM-90` `capability` Two seeded options sit on `Hall 6` across one week at ranks `1`, `2`. `src: Data model, seed`
- [ ] `C-DM-91` `capability` The seeded plan carries an `approved` revision with at least four objects. `src: Data model, seed`
- [ ] `C-DM-92` `capability` The seeded plan carries two fire exit constraints with required clearances. `src: Data model, seed`
- [ ] `C-DM-93` `capability` One seeded contractor accreditation carries insurance evidence expiring inside the seeded window. `src: Data model, seed`
- [ ] `C-DM-94` `capability` The seeded services carry a rigging service requiring an approved plan. `src: Data model, seed`
- [ ] `C-DM-95` `capability` The seeded services carry a power drop requiring a plan position. `src: Data model, seed`
- [ ] `C-DM-96` `literal` `Hall 4` hire is priced at `1450000` minor units per run day. `src: Data model, seed`
- [ ] `C-DM-97` `capability` One seeded article carries a published English heading over a body untranslated elsewhere. `src: Data model, seed`
- [ ] `C-DM-98` `constraint` Seeding is idempotent, so restarting the app duplicates no row. `src: Data model, seed`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One campus, one tenant, with no second venue, no cross-campus surface. `src: Constraints`
- [ ] `C-CN-02` `constraint` No ticket selling, no box office, no seat-level allocation exists. `src: Constraints`
- [ ] `C-CN-03` `constraint` No payroll, no procurement, no supplier marketplace exists. `src: Constraints`
- [ ] `C-CN-04` `constraint` No sales pipeline beyond the enquiry exists. `src: Constraints`
- [ ] `C-CN-05` `constraint` No second factor, no federated identity provider, no directory provisioning exists. `src: Constraints`
- [ ] `C-CN-06` `constraint` No native mobile application, no chat, no comment, no like, no direct message exists. `src: Constraints`
- [ ] `C-CN-07` `constraint` No surface makes a model call. `src: Constraints`
- [ ] `C-CN-08` `constraint` `PostgreSQL` is the only backing service. `src: Constraints`
- [ ] `C-CN-09` `constraint` The ticketing, parking, accounting interfaces are internal boundaries within the product. `src: Constraints`
- [ ] `C-CN-10` `constraint` No external network call is made at runtime; no analytics destination is contacted. `src: Constraints`
- [ ] `C-CN-11` `constraint` No mark reproduces a real trademark. `src: Constraints`
- [ ] `C-CN-12` `constraint` No name in the seed data refers to a real company. `src: Constraints`
- [ ] `C-CN-13` `constraint` No route reflects an unescaped request value into a page. `src: Constraints`
- [ ] `C-CN-14` `constraint` No credential value reaches any surface. `src: Constraints`
- [ ] `C-CN-15` `constraint` No internal field reaches any public surface. `src: Constraints`
- [ ] `C-CN-16` `capability` The product stays responsive with five hundred bookings in a campus year. `src: Constraints`
- [ ] `C-CN-17` `capability` The product stays responsive with eight hundred objects on one floor plan. `src: Constraints`
- [ ] `C-CN-18` `capability` The product stays responsive with one hundred thousand scans in the access log. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-03` `contract` Both the public port, the public URL are read from the environment, never hardcoded. `src: Deployment contract`
- [ ] `C-DC-04` `contract` The HTTP API is served on that same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-05` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-07` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-08` `contract` Reserved `.browser_screenshots/`, `.downloads/` directories exist at the app root, empty. `src: Deployment contract`
- [ ] `C-DC-09` `contract` A production build is served behind a static or preview server, never a dev server. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends, never as a child of the shell. `src: Deployment contract`
- [ ] `C-DC-11` `contract` The server binds `0.0.0.0`, never `127.0.0.1`, never `localhost`. `src: Deployment contract`
- [ ] `C-DC-12` `contract` The named backing service is already running at the environment variable of that service. `src: Deployment contract`
- [ ] `C-DC-13` `contract` Only the providers named in the brief are used; no edge functions exist. `src: Deployment contract`
- [ ] `C-DC-14` `contract` No persistent volume, no fixed container name, no custom network is declared. `src: Deployment contract`
- [ ] `C-DC-15` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API`
- [ ] `C-DC-16` `contract` An invalid call is rejected as a client error, never as a server error, never as a silent success. `src: Deployment contract, API`
- [ ] `C-DC-17` `contract` Bearer auth is carried on everything except the sign-in, health, public, search, page-view endpoints. `src: Deployment contract, API`
- [ ] `C-DC-18` `contract` `POST /api/auth/login` takes `email`, `password`, returning `access_token` plus `principal`. `src: Deployment contract, API`
- [ ] `C-DC-19` `contract` `GET /api/availability` takes `space`, `from`, `to`, returning `state` plus `blocking_space` on a block. `src: Deployment contract, API`
- [ ] `C-DC-20` `contract` `POST /api/options` takes `enquiry_id`, `spaces`, `window_start`, `window_end`, `rank`, `expires_at`. `src: Deployment contract, API`
- [ ] `C-DC-21` `contract` `POST /api/options/{id}/confirm` takes `layout`, `idempotency_key`, returning the booking or a refusal. `src: Deployment contract, API`
- [ ] `C-DC-22` `contract` `POST /api/bookings/{id}/phases` returns the phase or a refusal naming `shortfall_hours`. `src: Deployment contract, API`
- [ ] `C-DC-23` `contract` `POST /api/plans/{id}/objects` returns the object or a refusal carrying `rule` plus `measurement`. `src: Deployment contract, API`
- [ ] `C-DC-24` `contract` `POST /api/accreditations/{id}/revoke` returns the revoked accreditation plus a `cascaded` count. `src: Deployment contract, API`
- [ ] `C-DC-25` `contract` `POST /api/scans` returns `decision`, adding `reason` on a refusal. `src: Deployment contract, API`
- [ ] `C-DC-26` `contract` `GET /api/occupancy` takes `space`, returning `count`, `state`, `licensed_capacity`. `src: Deployment contract, API`
- [ ] `C-DC-27` `contract` `GET /api/public/events` returns published events carrying the public fields only. `src: Deployment contract, API`
- [ ] `C-DC-28` `contract` `POST /api/subscriptions` takes `email`, returning `state`. `src: Deployment contract, API`
- [ ] `C-DC-29` `contract` `POST /api/page-views` takes `route`, `language`, refused for as long as statistics consent is absent. `src: Deployment contract, API`
- [ ] `C-DC-30` `contract` `GET /api/audit` returns an event array plus a `next_cursor`. `src: Deployment contract, API`
- [ ] `C-DC-31` `constraint` An in-memory array of holds, bookings, scans, audit events rebuilt at start is refused as a violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-32` `constraint` An availability answer composed without consulting the stored holds is refused as a violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-33` `constraint` An occupancy figure kept as a process counter rather than derived from stored scans is refused. `src: Deployment contract, no mocks`
- [ ] `C-DC-34` `constraint` An audit chain recomputed on read so as to be intact by construction is refused as a violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-35` `constraint` A publication filtered when a page renders rather than stored as a projection is refused. `src: Deployment contract, no mocks`

## Pinned literals

| Value | Class | Item |
|---|---|---|
| `coordinator@example.com` | a value the brief pins verbatim | `C-RL-40` |
| `operations@example.com` | a value the brief pins verbatim | `C-RL-40` |
| `planner@example.com` | a value the brief pins verbatim | `C-RL-40` |
| `planner2@example.com` | a value the brief pins verbatim | `C-RL-40` |
| `exhibitor@example.com` | a value the brief pins verbatim | `C-RL-40` |
| `finance@example.com` | a value the brief pins verbatim | `C-RL-40` |
| `auditor@example.com` | a value the brief pins verbatim | `C-RL-40` |
| `deku-demo-pw-2026` | a value the brief pins verbatim | `C-RL-41` |
| `Ironwood Interiors` | a value the brief pins verbatim | `C-RL-42` |
| `S-118` | a value the brief pins verbatim | `C-RL-42` |
| `hall` | a value the brief pins verbatim | `C-CF-11` |
| `event_hall` | a value the brief pins verbatim | `C-CF-11` |
| `meeting_room` | a value the brief pins verbatim | `C-CF-11` |
| `boulevard` | a value the brief pins verbatim | `C-CF-11` |
| `passage` | a value the brief pins verbatim | `C-CF-11` |
| `combination` | a value the brief pins verbatim | `C-CF-11` |
| `free` | a value the brief pins verbatim | `C-CF-22` |
| `held` | a value the brief pins verbatim | `C-CF-22` |
| `booked` | a value the brief pins verbatim | `C-CF-22` |
| `blocked_by_ancestor` | a value the brief pins verbatim | `C-CF-22` |
| `blocked_by_descendant` | a value the brief pins verbatim | `C-CF-22` |
| `maintenance` | a value the brief pins verbatim | `C-CF-22` |
| `normal` | a value the brief pins verbatim | `C-CF-27` |
| `evacuation` | a value the brief pins verbatim | `C-CF-27` |
| `theatre` | a value the brief pins verbatim | `C-CF-28` |
| `cabaret` | a value the brief pins verbatim | `C-CF-28` |
| `banquet` | a value the brief pins verbatim | `C-CF-28` |
| `stand_grid` | a value the brief pins verbatim | `C-CF-28` |
| `standing` | a value the brief pins verbatim | `C-CF-28` |
| `challenged` | a value the brief pins verbatim | `C-CF-42` |
| `released` | a value the brief pins verbatim | `C-CF-42` |
| `confirmed` | a value the brief pins verbatim | `C-CF-42` |
| `lapsed` | a value the brief pins verbatim | `C-CF-42` |
| `access` | a value the brief pins verbatim | `C-CF-65` |
| `build_up` | a value the brief pins verbatim | `C-CF-65` |
| `run` | a value the brief pins verbatim | `C-CF-65` |
| `tear_down` | a value the brief pins verbatim | `C-CF-65` |
| `clearance` | a value the brief pins verbatim | `C-CF-65` |
| `stand` | a value the brief pins verbatim | `C-CF-88` |
| `catering_point` | a value the brief pins verbatim | `C-CF-88` |
| `stage` | a value the brief pins verbatim | `C-CF-88` |
| `seating_block` | a value the brief pins verbatim | `C-CF-88` |
| `entrance_point` | a value the brief pins verbatim | `C-CF-88` |
| `draft` | a value the brief pins verbatim | `C-CF-105` |
| `submitted` | a value the brief pins verbatim | `C-CF-105` |
| `approved` | a value the brief pins verbatim | `C-CF-105` |
| `withdrawn` | a value the brief pins verbatim | `C-CF-105` |
| `organiser` | a value the brief pins verbatim | `C-CF-108` |
| `exhibitor` | a value the brief pins verbatim | `C-CF-108` |
| `contractor` | a value the brief pins verbatim | `C-CF-108` |
| `venue_staff` | a value the brief pins verbatim | `C-CF-108` |
| `caterer` | a value the brief pins verbatim | `C-CF-108` |
| `security` | a value the brief pins verbatim | `C-CF-108` |
| `cleaner` | a value the brief pins verbatim | `C-CF-108` |
| `visitor` | a value the brief pins verbatim | `C-CF-108` |
| `insurance` | a value the brief pins verbatim | `C-CF-110` |
| `risk_assessment` | a value the brief pins verbatim | `C-CF-110` |
| `competence` | a value the brief pins verbatim | `C-CF-110` |
| `identity` | a value the brief pins verbatim | `C-CF-110` |
| `pending_evidence` | a value the brief pins verbatim | `C-CF-111` |
| `valid` | a value the brief pins verbatim | `C-CF-111` |
| `expired` | a value the brief pins verbatim | `C-CF-111` |
| `revoked` | a value the brief pins verbatim | `C-CF-111` |
| `staff` | a value the brief pins verbatim | `C-CF-124` |
| `trade` | a value the brief pins verbatim | `C-CF-124` |
| `public` | a value the brief pins verbatim | `C-CF-124` |
| `closed` | a value the brief pins verbatim | `C-CF-124` |
| `admitted` | a value the brief pins verbatim | `C-CF-130` |
| `refused` | a value the brief pins verbatim | `C-CF-130` |
| `no_accreditation` | a value the brief pins verbatim | `C-CF-132` |
| `wrong_phase` | a value the brief pins verbatim | `C-CF-132` |
| `wrong_space` | a value the brief pins verbatim | `C-CF-132` |
| `expired_evidence` | a value the brief pins verbatim | `C-CF-132` |
| `at_capacity` | a value the brief pins verbatim | `C-CF-132` |
| `anti_passback` | a value the brief pins verbatim | `C-CF-132` |
| `clear` | a value the brief pins verbatim | `C-CF-153` |
| `approaching` | a value the brief pins verbatim | `C-CF-153` |
| `at_limit` | a value the brief pins verbatim | `C-CF-153` |
| `ordered` | a value the brief pins verbatim | `C-CF-181` |
| `late_ordered` | a value the brief pins verbatim | `C-CF-181` |
| `cancelled` | a value the brief pins verbatim | `C-CF-181` |
| `delivered` | a value the brief pins verbatim | `C-CF-181` |
| `private` | a value the brief pins verbatim | `C-CF-201` |
| `announced` | a value the brief pins verbatim | `C-CF-201` |
| `published` | a value the brief pins verbatim | `C-CF-201` |
| `Open to the public` | a value the brief pins verbatim | `C-CF-275` |
| `Trade fair - registration required` | a value the brief pins verbatim | `C-CF-275` |
| `1` | a value the brief pins verbatim | `C-CF-287` |
| `6` | a value the brief pins verbatim | `C-CF-287` |
| `XXL` | a value the brief pins verbatim | `C-CF-287` |
| `Search entire website` | a value the brief pins verbatim | `C-CF-324` |
| `sent` | a value the brief pins verbatim | `C-CF-327` |
| `invalid` | a value the brief pins verbatim | `C-CF-327` |
| `already` | a value the brief pins verbatim | `C-CF-327` |
| `nl` | a value the brief pins verbatim | `C-CF-333` |
| `fr` | a value the brief pins verbatim | `C-CF-333` |
| `en` | a value the brief pins verbatim | `C-CF-333` |
| `/LANG` | a value the brief pins verbatim | `C-UF-02` |
| `/LANG/calendar` | a value the brief pins verbatim | `C-UF-02` |
| `/LANG/visit` | a value the brief pins verbatim | `C-UF-02` |
| `/LANG/organize` | a value the brief pins verbatim | `C-UF-02` |
| `/LANG/about` | a value the brief pins verbatim | `C-UF-02` |
| `/LANG/news` | a value the brief pins verbatim | `C-UF-02` |
| `/LANG/contact` | a value the brief pins verbatim | `C-UF-02` |
| `/LANG/visit/accessibility-parking` | a value the brief pins verbatim | `C-UF-03` |
| `/LANG/visit/food-drinks` | a value the brief pins verbatim | `C-UF-03` |
| `/LANG/visit/what-to-do-city` | a value the brief pins verbatim | `C-UF-03` |
| `/LANG/visit/frequently-asked-questions` | a value the brief pins verbatim | `C-UF-03` |
| `/LANG/organize/spaces` | a value the brief pins verbatim | `C-UF-04` |
| `/LANG/organize/meetings` | a value the brief pins verbatim | `C-UF-04` |
| `/LANG/organize/catering` | a value the brief pins verbatim | `C-UF-04` |
| `/LANG/organize/orangery-kitchen` | a value the brief pins verbatim | `C-UF-04` |
| `/LANG/organize/accessibility-region` | a value the brief pins verbatim | `C-UF-04` |
| `/LANG/organize/unique-events` | a value the brief pins verbatim | `C-UF-04` |
| `/LANG/about/who-are-we` | a value the brief pins verbatim | `C-UF-05` |
| `/LANG/about/history` | a value the brief pins verbatim | `C-UF-05` |
| `/LANG/about/sustainability-safety` | a value the brief pins verbatim | `C-UF-05` |
| `/LANG/about/media-kit-documents` | a value the brief pins verbatim | `C-UF-05` |
| `/LANG/general-conditions` | a value the brief pins verbatim | `C-UF-06` |
| `/LANG/privacy-policy` | a value the brief pins verbatim | `C-UF-06` |
| `/LANG/cookies` | a value the brief pins verbatim | `C-UF-06` |
| `/LANG/news/newsletter` | a value the brief pins verbatim | `C-UF-07` |
| `/LANG/search` | a value the brief pins verbatim | `C-UF-07` |
| `/LANG/wayfinding/:event` | a value the brief pins verbatim | `C-UF-07` |
| `/robots.txt` | a value the brief pins verbatim | `C-UF-07` |
| `/sitemap.xml` | a value the brief pins verbatim | `C-UF-07` |
| `/signin` | a value the brief pins verbatim | `C-UF-08` |
| `/console` | a value the brief pins verbatim | `C-UF-08` |
| `/console/enquiries` | a value the brief pins verbatim | `C-UF-08` |
| `/console/options` | a value the brief pins verbatim | `C-UF-08` |
| `/console/bookings/:id` | a value the brief pins verbatim | `C-UF-08` |
| `/console/plans/:id` | a value the brief pins verbatim | `C-UF-08` |
| `/console/accreditation` | a value the brief pins verbatim | `C-UF-09` |
| `/console/access` | a value the brief pins verbatim | `C-UF-09` |
| `/console/safety` | a value the brief pins verbatim | `C-UF-09` |
| `/console/works` | a value the brief pins verbatim | `C-UF-09` |
| `/console/services` | a value the brief pins verbatim | `C-UF-09` |
| `/console/invoices` | a value the brief pins verbatim | `C-UF-10` |
| `/console/publish` | a value the brief pins verbatim | `C-UF-10` |
| `/console/annual` | a value the brief pins verbatim | `C-UF-10` |
| `/console/reports` | a value the brief pins verbatim | `C-UF-10` |
| `/console/audit` | a value the brief pins verbatim | `C-UF-10` |
| `/portal` | a value the brief pins verbatim | `C-UF-10` |
| `Inter` | a value the brief pins verbatim | `C-FE-19` |
| `16px` | a value the brief pins verbatim | `C-FE-21` |
| `24px` | a value the brief pins verbatim | `C-FE-21` |
| `15px` | a value the brief pins verbatim | `C-FE-22` |
| `14px` | a value the brief pins verbatim | `C-FE-23` |
| `21px` | a value the brief pins verbatim | `C-FE-23` |
| `12px` | a value the brief pins verbatim | `C-FE-24` |
| `14.4px` | a value the brief pins verbatim | `C-FE-24` |
| `20px` | a value the brief pins verbatim | `C-FE-25` |
| `30px` | a value the brief pins verbatim | `C-FE-25` |
| `18px` | a value the brief pins verbatim | `C-FE-26` |
| `Jobs` | a value the brief pins verbatim | `C-FE-39` |
| `Northtide Venues Group` | a value the brief pins verbatim | `C-FE-39` |
| `Calendar` | a value the brief pins verbatim | `C-FE-40` |
| `Visit` | a value the brief pins verbatim | `C-FE-40` |
| `Organize` | a value the brief pins verbatim | `C-FE-40` |
| `About Verwick Xpo` | a value the brief pins verbatim | `C-FE-40` |
| `News` | a value the brief pins verbatim | `C-FE-40` |
| `Contact` | a value the brief pins verbatim | `C-FE-40` |
| `General terms & conditions` | a value the brief pins verbatim | `C-FE-45` |
| `Safety manual` | a value the brief pins verbatim | `C-FE-45` |
| `Privacy policy` | a value the brief pins verbatim | `C-FE-45` |
| `Cookie Policy` | a value the brief pins verbatim | `C-FE-45` |
| `Capacity` | a value the brief pins verbatim | `C-FE-55` |
| `Surface area` | a value the brief pins verbatim | `C-FE-55` |
| `Unique features` | a value the brief pins verbatim | `C-FE-55` |
| `Suitable for` | a value the brief pins verbatim | `C-FE-55` |
| `Skip to main content` | a value the brief pins verbatim | `C-FE-80` |
| `when ideas need space` | a value the brief pins verbatim | `C-FE-82` |
| `View our calendar` | a value the brief pins verbatim | `C-FE-83` |
| `Organize your event` | a value the brief pins verbatim | `C-FE-83` |
| `Coming soon to Verwick Xpo` | a value the brief pins verbatim | `C-FE-84` |
| `All events` | a value the brief pins verbatim | `C-FE-84` |
| `Are you visiting Verwick Xpo soon?` | a value the brief pins verbatim | `C-FE-85` |
| `Plan your visit` | a value the brief pins verbatim | `C-FE-85` |
| `Your next event at Verwick Xpo?` | a value the brief pins verbatim | `C-FE-86` |
| `The right setting for every concept` | a value the brief pins verbatim | `C-FE-87` |
| `Organize in Verwick Xpo` | a value the brief pins verbatim | `C-FE-87` |
| `Discover the halls` | a value the brief pins verbatim | `C-FE-87` |
| `6 halls: versatility at its best` | a value the brief pins verbatim | `C-FE-88` |
| `Meeting center: 5 rooms, endless possibilities` | a value the brief pins verbatim | `C-FE-88` |
| `The Concourse: covered boulevard` | a value the brief pins verbatim | `C-FE-88` |
| `The Orangery: Fast Gourmet Kitchen` | a value the brief pins verbatim | `C-FE-88` |
| `Get inspired` | a value the brief pins verbatim | `C-FE-89` |
| `More unique events` | a value the brief pins verbatim | `C-FE-89` |
| `Stay up to date` | a value the brief pins verbatim | `C-FE-90` |
| `Subscribe to the newsletter` | a value the brief pins verbatim | `C-FE-90` |
| `Follow us` | a value the brief pins verbatim | `C-FE-90` |
| `Xpo Newsflash` | a value the brief pins verbatim | `C-FE-91` |
| `All newsflashes` | a value the brief pins verbatim | `C-FE-91` |
| `Flexible combinations tailored to you` | a value the brief pins verbatim | `C-FE-93` |
| `Say hi to the Venue team` | a value the brief pins verbatim | `C-FE-93` |
| `Contact us` | a value the brief pins verbatim | `C-FE-93` |
| `The spaces in use` | a value the brief pins verbatim | `C-FE-95` |
| `(C) 2026 Verwick Xpo` | a value the brief pins verbatim | `C-FE-96` |
| `Page not found` | a value the brief pins verbatim | `C-FE-97` |
| `Go to homepage` | a value the brief pins verbatim | `C-FE-97` |
| `Palmarosa` | a value the brief pins verbatim | `C-FE-98` |
| `Bookmark Fair` | a value the brief pins verbatim | `C-FE-98` |
| `The Transit` | a value the brief pins verbatim | `C-FE-98` |
| `Calderhook Group completes acquisition of Northtide Venues Group` | a value the brief pins verbatim | `C-FE-99` |
| `03.08.2026` | a value the brief pins verbatim | `C-FE-99` |
| `Verwick Xpo achieves the Westmark sustainability charter for the 10th consecutive year` | a value the brief pins verbatim | `C-FE-100` |
| `07.07.2026` | a value the brief pins verbatim | `C-FE-100` |
| `Architecture & Design` | a value the brief pins verbatim | `C-FE-102` |
| `Lifestyle & Sports` | a value the brief pins verbatim | `C-FE-102` |
| `Sustainability` | a value the brief pins verbatim | `C-FE-102` |
| `Hall 4` | a value the brief pins verbatim | `C-FE-103` |
| `not captured` | a value the brief pins verbatim | `C-FE-103` |
| `/app/USER_README.md` | a value the brief pins verbatim | `C-DM-04` |
| `coordinator` | a value the brief pins verbatim | `C-DM-07` |
| `operations` | a value the brief pins verbatim | `C-DM-07` |
| `planner` | a value the brief pins verbatim | `C-DM-07` |
| `finance` | a value the brief pins verbatim | `C-DM-07` |
| `auditor` | a value the brief pins verbatim | `C-DM-07` |
| `option` | a value the brief pins verbatim | `C-DM-16` |
| `booking` | a value the brief pins verbatim | `C-DM-16` |
| `public_form` | a value the brief pins verbatim | `C-DM-19` |
| `sales` | a value the brief pins verbatim | `C-DM-19` |
| `dock` | a value the brief pins verbatim | `C-DM-28` |
| `lift` | a value the brief pins verbatim | `C-DM-28` |
| `forklift` | a value the brief pins verbatim | `C-DM-28` |
| `crew` | a value the brief pins verbatim | `C-DM-28` |
| `power_drop` | a value the brief pins verbatim | `C-DM-28` |
| `column` | a value the brief pins verbatim | `C-DM-33` |
| `truss` | a value the brief pins verbatim | `C-DM-33` |
| `door` | a value the brief pins verbatim | `C-DM-33` |
| `fire_exit` | a value the brief pins verbatim | `C-DM-33` |
| `rigging_point` | a value the brief pins verbatim | `C-DM-33` |
| `power_point` | a value the brief pins verbatim | `C-DM-33` |
| `water_point` | a value the brief pins verbatim | `C-DM-33` |
| `catering` | a value the brief pins verbatim | `C-DM-49` |
| `technical` | a value the brief pins verbatim | `C-DM-49` |
| `furniture` | a value the brief pins verbatim | `C-DM-49` |
| `cleaning` | a value the brief pins verbatim | `C-DM-49` |
| `waste` | a value the brief pins verbatim | `C-DM-49` |
| `signage` | a value the brief pins verbatim | `C-DM-49` |
| `parking` | a value the brief pins verbatim | `C-DM-49` |
| `deposit` | a value the brief pins verbatim | `C-DM-57` |
| `final` | a value the brief pins verbatim | `C-DM-57` |
| `credit` | a value the brief pins verbatim | `C-DM-57` |
| `missing` | a value the brief pins verbatim | `C-DM-60` |
| `Hall 1` | a value the brief pins verbatim | `C-DM-68` |
| `Hall 2` | a value the brief pins verbatim | `C-DM-68` |
| `Hall 3` | a value the brief pins verbatim | `C-DM-68` |
| `Hall 5` | a value the brief pins verbatim | `C-DM-68` |
| `Hall 6` | a value the brief pins verbatim | `C-DM-68` |
| `The Event Hall` | a value the brief pins verbatim | `C-DM-68` |
| `MC 1` | a value the brief pins verbatim | `C-DM-68` |
| `MC 2` | a value the brief pins verbatim | `C-DM-68` |
| `MC 3` | a value the brief pins verbatim | `C-DM-68` |
| `MC 4` | a value the brief pins verbatim | `C-DM-68` |
| `The Concourse` | a value the brief pins verbatim | `C-DM-68` |
| `6090` | a value the brief pins verbatim | `C-DM-69` |
| `1620` | a value the brief pins verbatim | `C-DM-69` |
| `4058` | a value the brief pins verbatim | `C-DM-70` |
| `1740` | a value the brief pins verbatim | `C-DM-70` |
| `3601` | a value the brief pins verbatim | `C-DM-71` |
| `1680` | a value the brief pins verbatim | `C-DM-71` |
| `7685` | a value the brief pins verbatim | `C-DM-72` |
| `3660` | a value the brief pins verbatim | `C-DM-72` |
| `4723` | a value the brief pins verbatim | `C-DM-73` |
| `5160` | a value the brief pins verbatim | `C-DM-73` |
| `5055` | a value the brief pins verbatim | `C-DM-74` |
| `1860` | a value the brief pins verbatim | `C-DM-74` |
| `2000` | a value the brief pins verbatim | `C-DM-75` |
| `550` | a value the brief pins verbatim | `C-DM-75` |
| `1679` | a value the brief pins verbatim | `C-DM-76` |
| `The Meeting Centre with the Event Hall` | a value the brief pins verbatim | `C-DM-79` |
| `2600` | a value the brief pins verbatim | `C-DM-79` |
| `North Entrance` | a value the brief pins verbatim | `C-DM-80` |
| `South Entrance` | a value the brief pins verbatim | `C-DM-80` |
| `Concourse East` | a value the brief pins verbatim | `C-DM-80` |
| `Concourse West` | a value the brief pins verbatim | `C-DM-80` |
| `Dock Gate` | a value the brief pins verbatim | `C-DM-80` |
| `2500` | a value the brief pins verbatim | `C-DM-81` |
| `Verwick Design Days` | a value the brief pins verbatim | `C-DM-84` |
| `Ironwood Night` | a value the brief pins verbatim | `C-DM-84` |
| `1450000` | a value the brief pins verbatim | `C-DM-96` |
| `Flexible halls and rooms` | a value the brief pins verbatim | `C-FE-92` |
| `View the floor plan` | a value the brief pins verbatim | `C-FE-92` |
| `Start your request` | a value the brief pins verbatim | `C-FE-92` |
| `Why do organizers choose Verwick Xpo?` | a value the brief pins verbatim | `C-FE-94` |
| `6 flexible halls and 5 modular meeting rooms` | a value the brief pins verbatim | `C-FE-94` |
| `2,500 parking spaces` | a value the brief pins verbatim | `C-FE-94` |
| `Halls 4 and 5 with the Transit` | a value the brief pins verbatim | `C-DM-78` |
| `7400` | a value the brief pins verbatim | `C-DM-78` |
| `8820` | a value the brief pins verbatim | `C-DM-78` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the stated number of sign-in attempts before a lockout | `C-CF-04` |
| the stated staleness bound a degraded entrance decides within | `C-CF-152` |
| the stated grace window allowing legitimate re-entry | `C-CF-148` |
| the stated working-hours rule bounding a crew assignment | `C-CF-084` |
| the stated freshness after which a cached visitor map announces its age | `C-CF-236` |
| the stated maximum width capping the reading column on the legal routes | `C-FE-07` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 1 | 10 |
| User roles | 2 | 42 |
| Core features | 33 | 338 |
| User flow | 4 | 25 |
| UI and UX notes | 4 | 43 |
| Front-end specification | 7 | 110 |
| Technical requirements | 12 | 60 |
| Data model | 6 | 98 |
| Constraints | 2 | 18 |
| Deployment contract | 9 | 35 |
