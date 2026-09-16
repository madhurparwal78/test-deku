# Checklist: Clinical Records Platform

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 494
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public project site for an open-source health record. `src: Overview, para 2`
- [ ] `C-OV-02` `capability` The app serves a clinical record behind a sign-in boundary. `src: Overview, para 3`
- [ ] `C-OV-03` `constraint` The app keeps every clinical fact as a stored version rather than an overwritten row. `src: Overview, para 3`
- [ ] `C-OV-04` `capability` A clinician ends a visit by signing the encounter. `src: Overview, para 3`
- [ ] `C-OV-05` `constraint` The app refuses to show a reader a count over rows the same reader was refused. `src: Overview, para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` A clinician reads the chart of a patient the same clinician holds a relationship with. `src: User roles, table row 1`
- [ ] `C-RL-02` `role` A clinician writes a note on an encounter of their own. `src: User roles, table row 1`
- [ ] `C-RL-03` `role` A clinician signs an encounter. `src: User roles, table row 1`
- [ ] `C-RL-04` `role` A front desk account registers a patient. `src: User roles, table row 2`
- [ ] `C-RL-05` `role` A front desk account books an appointment. `src: User roles, table row 2`
- [ ] `C-RL-06` `role` A biller submits a claim. `src: User roles, table row 3`
- [ ] `C-RL-07` `role` A biller posts a remittance. `src: User roles, table row 3`
- [ ] `C-RL-08` `role` A patient reads their own record. `src: User roles, table row 4`
- [ ] `C-RL-09` `role` A patient reads the log of who has read their own record. `src: User roles, table row 4`
- [ ] `C-RL-10` `role` A clinician cannot open the chart of a patient the same clinician holds no relationship with. `src: User roles, cannot list bullet 1`
- [ ] `C-RL-11` `role` A clinician cannot edit a note once the note is signed. `src: User roles, cannot list bullet 1`
- [ ] `C-RL-12` `role` A clinician cannot sign an encounter carrying no coded diagnosis. `src: User roles, cannot list bullet 1`
- [ ] `C-RL-13` `role` A front desk account cannot read a clinical note. `src: User roles, cannot list bullet 2`
- [ ] `C-RL-14` `role` A front desk account cannot read a stored result. `src: User roles, cannot list bullet 2`
- [ ] `C-RL-15` `role` A biller cannot read a stored prescription. `src: User roles, cannot list bullet 3`
- [ ] `C-RL-16` `role` A biller cannot read a condition labelled `restricted`. `src: User roles, cannot list bullet 3`
- [ ] `C-RL-17` `role` A patient cannot read another patient's record by any path. `src: User roles, cannot list bullet 4`
- [ ] `C-RL-18` `role` A patient cannot open a workspace route. `src: User roles, cannot list bullet 4`
- [ ] `C-RL-19` `role` A patient cannot edit a stored clinical fact. `src: User roles, cannot list bullet 4`
- [ ] `C-RL-20` `constraint` The server rejects a patient call to a clinician-only endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-21` `constraint` A denied request leaves the protected state unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-22` `constraint` Holding a clinical role alone opens no chart. `src: User roles, relationship paragraph`
- [ ] `C-RL-23` `capability` Care team membership opens a chart for a clinician. `src: User roles, relationship paragraph`
- [ ] `C-RL-24` `capability` An emergency declaration named for one patient opens that patient's chart. `src: User roles, relationship paragraph`
- [ ] `C-RL-25` `constraint` A refused chart read answers with the same status as a read of an unissued medical record number. `src: User roles, relationship paragraph`
- [ ] `C-RL-26` `constraint` A refused chart read answers with the same body as a read of an unissued medical record number. `src: User roles, relationship paragraph`
- [ ] `C-RL-27` `constraint` No route creates an account. `src: User roles, signup paragraph`
- [ ] `C-RL-28` `constraint` No field lets an account choose its own role. `src: User roles, signup paragraph`
- [ ] `C-RL-29` `literal` The app seeds the clinician account `clinician@example.com`. `src: User roles, seeded accounts table row 1`
- [ ] `C-RL-30` `literal` The app seeds the clinician account `clinician2@example.com`. `src: User roles, seeded accounts table row 2`
- [ ] `C-RL-31` `literal` The app seeds the front desk account `frontdesk@example.com`. `src: User roles, seeded accounts table row 3`
- [ ] `C-RL-32` `literal` The app seeds the biller account `biller@example.com`. `src: User roles, seeded accounts table row 4`
- [ ] `C-RL-33` `literal` The app seeds the patient account `patient@example.com`. `src: User roles, seeded accounts table row 5`
- [ ] `C-RL-34` `literal` The app seeds the patient account `patient2@example.com`. `src: User roles, seeded accounts table row 6`
- [ ] `C-RL-35` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-36` `data` The account `clinician2@example.com` holds no relationship to a seeded patient. `src: User roles, seeded accounts table row 2`
- [ ] `C-RL-37` `data` The account `patient@example.com` is bound to `KH-100234`. `src: User roles, seeded accounts table row 5`

## C-CF Core features

- [ ] `C-CF-01` `capability` The endpoint `POST /api/auth/login` returns a bearer token for a seeded address. `src: Core features, Accounts and sessions rule 1`
- [ ] `C-CF-02` `constraint` A login carrying a wrong password returns no token. `src: Core features, Accounts and sessions rule 1`
- [ ] `C-CF-03` `constraint` A guarded endpoint denies a call carrying no token. `src: Core features, Accounts and sessions rule 2`
- [ ] `C-CF-04` `constraint` A guarded endpoint denies a call carrying a token the app never issued. `src: Core features, Accounts and sessions rule 2`
- [ ] `C-CF-05` `constraint` The app reads the acting role from the stored account row. `src: Core features, Accounts and sessions rule 3`
- [ ] `C-CF-06` `constraint` The app ignores a role named in a request body. `src: Core features, Accounts and sessions rule 3`
- [ ] `C-CF-07` `constraint` No endpoint creates an account. `src: Core features, Accounts and sessions rule 4`
- [ ] `C-CF-08` `data` The app stores every password hashed. `src: Core features, Accounts and sessions para 1`
- [ ] `C-CF-09` `constraint` No endpoint returns a stored password hash. `src: Core features, Accounts and sessions para 1`
- [ ] `C-CF-10` `data` Every clinical fact carries a `version_id`. `src: Core features, The record refuses to forget rule 1`
- [ ] `C-CF-11` `data` A corrected fact carries a `supersedes` naming the version replaced. `src: Core features, The record refuses to forget rule 1`
- [ ] `C-CF-12` `data` A corrected fact carries a stored `reason`. `src: Core features, The record refuses to forget rule 1`
- [ ] `C-CF-13` `capability` Reading a clinical fact returns the highest stored version. `src: Core features, The record refuses to forget rule 2`
- [ ] `C-CF-14` `capability` The endpoint `GET /api/observations/{id}/history` returns every stored version. `src: Core features, The record refuses to forget rule 2`
- [ ] `C-CF-15` `data` The seeded potassium observation carries two stored versions. `src: Core features, The record refuses to forget rule 2`
- [ ] `C-CF-16` `data` The first potassium version carries the value `6.2`. `src: Core features, The record refuses to forget rule 2`
- [ ] `C-CF-17` `data` The second potassium version carries the value `4.1`. `src: Core features, The record refuses to forget rule 2`
- [ ] `C-CF-18` `constraint` A retraction sets `entered_in_error` rather than removing a row. `src: Core features, The record refuses to forget rule 3`
- [ ] `C-CF-19` `capability` A retracted fact stays in the history read. `src: Core features, The record refuses to forget rule 3`
- [ ] `C-CF-20` `constraint` A retracted fact leaves the chart read. `src: Core features, The record refuses to forget rule 3`
- [ ] `C-CF-21` `constraint` The app keeps `completed` apart from `entered_in_error`. `src: Core features, The record refuses to forget rule 4`
- [ ] `C-CF-22` `data` Every clinical fact carries an `effective_time`. `src: Core features, The record refuses to forget rule 5`
- [ ] `C-CF-23` `data` Every clinical fact carries a `recorded_time`. `src: Core features, The record refuses to forget rule 5`
- [ ] `C-CF-24` `capability` The query `as_known_at` returns the chart as the chart stood at a stated instant. `src: Core features, The record refuses to forget rule 6`
- [ ] `C-CF-25` `data` The patient `KH-100236` carries a birth date of `1988`. `src: Core features, The record refuses to forget rule 7`
- [ ] `C-CF-26` `data` The patient `KH-100236` carries a `birth_date_precision` reading `year`. `src: Core features, The record refuses to forget rule 7`
- [ ] `C-CF-27` `constraint` No surface renders a year-precision birth date as a full calendar day. `src: Core features, The record refuses to forget rule 7`
- [ ] `C-CF-28` `data` The seeded troponin observation carries a `comparator` reading `<`. `src: Core features, The record refuses to forget rule 8`
- [ ] `C-CF-29` `data` The seeded troponin observation carries a `unit_code` reading `ng/mL`. `src: Core features, The record refuses to forget rule 8`
- [ ] `C-CF-30` `constraint` A bounded observation read keeps the stored comparator. `src: Core features, The record refuses to forget rule 8`
- [ ] `C-CF-31` `data` A coded value carries a `code_system`. `src: Core features, Coded values rule 1`
- [ ] `C-CF-32` `data` A coded value carries a `code_display` captured at recording time. `src: Core features, Coded values rule 1`
- [ ] `C-CF-33` `data` A coded value carries a `code_version`. `src: Core features, Coded values rule 1`
- [ ] `C-CF-34` `constraint` A condition missing a code field is refused as invalid. `src: Core features, The encounter and its note rule 4`
- [ ] `C-CF-35` `literal` The seeded diabetes diagnosis carries the code `E11.9`. `src: Core features, Coded values rule 4`
- [ ] `C-CF-36` `literal` The seeded restricted diagnosis carries the code `F11.20`. `src: Core features, Coded values rule 4`
- [ ] `C-CF-37` `literal` The seeded billed procedure carries the code `99213`. `src: Core features, Coded values rule 4`
- [ ] `C-CF-38` `literal` The seeded potassium observation carries the code `2823-3`. `src: Core features, Coded values rule 4`
- [ ] `C-CF-39` `literal` The seeded prescription carries the code `860975`. `src: Core features, Coded values rule 4`
- [ ] `C-CF-40` `capability` The endpoint `GET /api/patients` returns only patients the caller may open. `src: Core features, The patient register rule 1`
- [ ] `C-CF-41` `constraint` A search matching nothing answers as a search whose matches were all filtered away. `src: Core features, The patient register rule 1`
- [ ] `C-CF-42` `data` A patient identifier is unique over `system`, `value`, `period_start` together. `src: Core features, The patient register rule 2`
- [ ] `C-CF-43` `capability` A registration reusing a member number from an ended policy succeeds. `src: Core features, The patient register rule 2`
- [ ] `C-CF-44` `capability` The endpoint `POST /api/patients` returns the assigned `mrn`. `src: Core features, The patient register rule 3`
- [ ] `C-CF-45` `capability` A registration matching a stored patient on family name, birth date, address, telephone opens an `identity_review` row. `src: Core features, The patient register rule 3`
- [ ] `C-CF-46` `data` An identity review row opened for a same-birth-date near match carries `twin_warning`. `src: Core features, The patient register rule 3`
- [ ] `C-CF-47` `constraint` A possible-match warning names no matched record. `src: Core features, The patient register rule 3`
- [ ] `C-CF-48` `constraint` A candidate in the middle matching band is resolved automatically in neither direction. `src: Core features, The patient register rule 4`
- [ ] `C-CF-49` `capability` Reading the subsumed number `KH-100239` returns the survivor `KH-100240`. `src: Core features, The patient register rule 5`
- [ ] `C-CF-50` `data` A merged read carries a field stating that the identity moved. `src: Core features, The patient register rule 5`
- [ ] `C-CF-51` `constraint` A merge leaves the subsumed row stored. `src: Core features, The patient register rule 5`
- [ ] `C-CF-52` `capability` The endpoint `GET /api/appointments/availability` computes free time from a stored weekly template. `src: Core features, The appointment book rule 1`
- [ ] `C-CF-53` `constraint` The app stores no table of empty slots. `src: Core features, The appointment book rule 1`
- [ ] `C-CF-54` `data` A room is held from five minutes before an appointment start. `src: Core features, The appointment book rule 2`
- [ ] `C-CF-55` `data` A clinician is held until ten minutes after an appointment end. `src: Core features, The appointment book rule 2`
- [ ] `C-CF-56` `capability` The endpoint `POST /api/appointments` writes one occupancy row per resource held. `src: Core features, The appointment book rule 3`
- [ ] `C-CF-57` `constraint` Two simultaneous bookings of the last remaining slot leave exactly one appointment. `src: Core features, The appointment book rule 3`
- [ ] `C-CF-58` `constraint` The losing simultaneous booking is rejected as a conflict naming the clash. `src: Core features, The appointment book rule 3`
- [ ] `C-CF-59` `constraint` A booking whose room is already held fails whole. `src: Core features, The appointment book rule 4`
- [ ] `C-CF-60` `constraint` A failed booking leaves no occupancy row stored. `src: Core features, The appointment book rule 4`
- [ ] `C-CF-61` `capability` The endpoint `POST /api/appointments/{number}/cancel` releases every occupancy row. `src: Core features, The appointment book rule 5`
- [ ] `C-CF-62` `capability` A cancelled slot becomes bookable again. `src: Core features, The appointment book rule 5`
- [ ] `C-CF-63` `capability` The endpoint `POST /api/appointments/{number}/reschedule` claims the new time before releasing the old one. `src: Core features, The appointment book rule 6`
- [ ] `C-CF-64` `constraint` A reschedule onto a taken time leaves the original appointment `booked`. `src: Core features, The appointment book rule 6`
- [ ] `C-CF-65` `constraint` A `no_show` appointment frees no slot afterwards. `src: Core features, The appointment book rule 7`
- [ ] `C-CF-66` `capability` The endpoint `POST /api/encounters` returns the encounter `number`. `src: Core features, The encounter and its note rule 1`
- [ ] `C-CF-67` `constraint` A note in `draft` is readable only by the note's author. `src: Core features, The encounter and its note rule 2`
- [ ] `C-CF-68` `capability` An encounter carrying a draft note stays visible to another clinician. `src: Core features, The encounter and its note rule 2`
- [ ] `C-CF-69` `capability` The endpoint `PATCH /api/encounters/{number}/note` accepts a save carrying the loaded `version_id`. `src: Core features, The encounter and its note rule 3`
- [ ] `C-CF-70` `constraint` A note save carrying a stale `version_id` is refused. `src: Core features, The encounter and its note rule 3`
- [ ] `C-CF-71` `capability` A refused note save returns the current stored version. `src: Core features, The encounter and its note rule 3`
- [ ] `C-CF-72` `constraint` A refused note save merges nothing. `src: Core features, The encounter and its note rule 3`
- [ ] `C-CF-73` `capability` The endpoint `POST /api/encounters/{number}/orders` creates an order in `draft`. `src: Core features, The encounter and its note rule 5`
- [ ] `C-CF-74` `constraint` A `draft` order is absent from the active order list. `src: Core features, The encounter and its note rule 5`
- [ ] `C-CF-75` `capability` The endpoint `POST /api/encounters/{number}/sign` stores a `note_signature`. `src: Core features, Signing rule 1`
- [ ] `C-CF-76` `data` A stored signature carries a `rendering_hash`. `src: Core features, Signing rule 1`
- [ ] `C-CF-77` `data` A stored signature carries `included_refs` naming every fact the note pulled in. `src: Core features, Signing rule 1`
- [ ] `C-CF-78` `data` A stored signature carries the `terminology_versions` in force. `src: Core features, Signing rule 1`
- [ ] `C-CF-79` `capability` Signing moves every order on the encounter from `draft` to `active`. `src: Core features, Signing rule 2`
- [ ] `C-CF-80` `capability` Signing queues one claim at status `queued`. `src: Core features, Signing rule 3`
- [ ] `C-CF-81` `data` A queued claim carries an ordered `diagnoses` list copied from the encounter. `src: Core features, Signing rule 3`
- [ ] `C-CF-82` `capability` The sign response carries `orders_released` as a count. `src: Core features, Signing rule 4`
- [ ] `C-CF-83` `capability` The sign response carries the queued `claim_number`. `src: Core features, Signing rule 4`
- [ ] `C-CF-84` `constraint` Signing an encounter carrying no coded diagnosis is refused. `src: Core features, Signing rule 5`
- [ ] `C-CF-85` `constraint` A refused signing releases no order. `src: Core features, Signing rule 5`
- [ ] `C-CF-86` `constraint` A refused signing queues no claim. `src: Core features, Signing rule 5`
- [ ] `C-CF-87` `constraint` Signing an already signed encounter is refused. `src: Core features, Signing rule 6`
- [ ] `C-CF-88` `constraint` A repeated signing queues no second claim. `src: Core features, Signing rule 6`
- [ ] `C-CF-89` `capability` The endpoint `GET /api/encounters/{number}/rendering` returns the note as rendered at signing. `src: Core features, Signing rule 7`
- [ ] `C-CF-90` `constraint` Adding a medication after signing changes no stored `rendering_hash`. `src: Core features, Signing rule 7`
- [ ] `C-CF-91` `constraint` Adding a medication after signing changes no rendered note text. `src: Core features, Signing rule 7`
- [ ] `C-CF-92` `capability` The endpoint `POST /api/encounters/{number}/addendum` appends new information after a signed note. `src: Core features, Signing rule 8`
- [ ] `C-CF-93` `capability` The endpoint `POST /api/encounters/{number}/amendment` writes a new note version. `src: Core features, Signing rule 8`
- [ ] `C-CF-94` `constraint` An addendum carrying no reason is refused. `src: Core features, Signing rule 8`
- [ ] `C-CF-95` `capability` An amended note keeps the original version readable in history. `src: Core features, Signing rule 8`
- [ ] `C-CF-96` `capability` The endpoint `POST /api/portal/amendment-requests` attaches a patient statement. `src: Core features, Signing rule 9`
- [ ] `C-CF-97` `constraint` A patient amendment request changes no stored clinical entry. `src: Core features, Signing rule 9`
- [ ] `C-CF-98` `capability` The endpoint `POST /api/results` records a result against a named `placer_number`. `src: Core features, Results rule 1`
- [ ] `C-CF-99` `constraint` A result carrying a stored `control_id` creates no second observation. `src: Core features, Results rule 1`
- [ ] `C-CF-100` `capability` A repeated result is answered with the first stored outcome. `src: Core features, Results rule 1`
- [ ] `C-CF-101` `data` A stored observation keeps the `reference_low` the sender supplied. `src: Core features, Results rule 2`
- [ ] `C-CF-102` `data` A stored observation keeps the `reference_high` the sender supplied. `src: Core features, Results rule 2`
- [ ] `C-CF-103` `data` A stored observation keeps the `abnormal_flag` the sender supplied. `src: Core features, Results rule 2`
- [ ] `C-CF-104` `constraint` The app consults no reference range table of the app's own. `src: Core features, Results rule 2`
- [ ] `C-CF-105` `capability` A corrected result writes a new observation version. `src: Core features, Results rule 3`
- [ ] `C-CF-106` `constraint` A result whose `effective_time` predates the current one does not become current. `src: Core features, Results rule 4`
- [ ] `C-CF-107` `capability` The endpoint `GET /api/results/unmatched` returns the reconciliation queue. `src: Core features, Results rule 5`
- [ ] `C-CF-108` `constraint` A result whose patient cannot be identified is filed against no patient. `src: Core features, Results rule 5`
- [ ] `C-CF-109` `data` The seeded reconciliation queue holds exactly one entry. `src: Core features, Results rule 5`
- [ ] `C-CF-110` `capability` The endpoint `POST /api/prescriptions` renders `patient_instruction` from the structured fields. `src: Core features, Prescribing and allergies rule 1`
- [ ] `C-CF-111` `data` The prescription `RX-2026-0001` carries a `dose_quantity` of `500`. `src: Core features, Prescribing and allergies rule 2`
- [ ] `C-CF-112` `data` The prescription `RX-2026-0001` carries a `dispense_quantity` of `60`. `src: Core features, Prescribing and allergies rule 2`
- [ ] `C-CF-113` `data` The prescription `RX-2026-0001` carries `refills_authorised` of `0`. `src: Core features, Prescribing and allergies rule 2`
- [ ] `C-CF-114` `capability` The safety check runs over the patient's complete stored record. `src: Core features, Prescribing and allergies rule 3`
- [ ] `C-CF-115` `capability` A conflict response states how serious the conflict is. `src: Core features, Prescribing and allergies rule 3`
- [ ] `C-CF-116` `constraint` A conflict with a withheld fact names nothing about the conflicting entry. `src: Core features, Prescribing and allergies rule 3`
- [ ] `C-CF-117` `capability` A conflict response offers the consent route. `src: Core features, Prescribing and allergies rule 3`
- [ ] `C-CF-118` `data` The patient `KH-100234` carries a recorded allergy to `penicillin`. `src: Core features, Prescribing and allergies rule 4`
- [ ] `C-CF-119` `data` The patient `KH-100235` carries a `no_known_allergies` assertion. `src: Core features, Prescribing and allergies rule 4`
- [ ] `C-CF-120` `capability` The allergy read for `KH-100236` returns an `assertion` reading `not_asked`. `src: Core features, Prescribing and allergies rule 4`
- [ ] `C-CF-121` `constraint` An empty allergy list renders as no assertion of safety. `src: Core features, Prescribing and allergies rule 4`
- [ ] `C-CF-122` `capability` The endpoint `POST /api/eligibility` stores a dated snapshot. `src: Core features, Coverage rule 1`
- [ ] `C-CF-123` `data` An eligibility read returns `checked_at` beside the answer. `src: Core features, Coverage rule 1`
- [ ] `C-CF-124` `data` A claim line names a diagnosis by position through `diagnosis_pointers`. `src: Core features, Coverage rule 2`
- [ ] `C-CF-125` `constraint` A pointer at a position outside the claim's own list is refused as invalid. `src: Core features, Coverage rule 2`
- [ ] `C-CF-126` `data` A claim line carries a `unit_qualifier` reading `unit` or `minute`. `src: Core features, Coverage rule 3`
- [ ] `C-CF-127` `capability` The endpoint `POST /api/claims/{number}/submit` moves a queued claim to `submitted`. `src: Core features, Coverage rule 4`
- [ ] `C-CF-128` `constraint` A submit on a claim outside `queued` leaves the stored status unchanged. `src: Core features, Coverage rule 4`
- [ ] `C-CF-129` `capability` The endpoint `POST /api/remittances` posts a balancing remittance. `src: Core features, Coverage rule 5`
- [ ] `C-CF-130` `data` The remittance `REM-2026-0001` pays `12000` against a charge of `18500`. `src: Core features, Coverage rule 5`
- [ ] `C-CF-131` `data` The remittance `REM-2026-0001` carries a `contractual` adjustment of `4500`. `src: Core features, Coverage rule 5`
- [ ] `C-CF-132` `data` The remittance `REM-2026-0001` carries a `patient_responsibility` adjustment of `2000`. `src: Core features, Coverage rule 5`
- [ ] `C-CF-133` `constraint` A remittance whose lines do not balance is stored `quarantined`. `src: Core features, Coverage rule 6`
- [ ] `C-CF-134` `constraint` A quarantined remittance changes no claim status. `src: Core features, Coverage rule 6`
- [ ] `C-CF-135` `data` A quarantined remittance carries a stored `quarantine_reason`. `src: Core features, Coverage rule 6`
- [ ] `C-CF-136` `constraint` The app tolerates no difference of one minor unit. `src: Core features, Coverage rule 6`
- [ ] `C-CF-137` `capability` The patient balance after `REM-2026-0001` reads `2000`. `src: Core features, Coverage rule 7`
- [ ] `C-CF-138` `constraint` A `contractual` adjustment creates no patient balance. `src: Core features, Coverage rule 7`
- [ ] `C-CF-139` `data` The ledger entries of one `transaction_id` sum to zero. `src: Core features, Coverage rule 8`
- [ ] `C-CF-140` `capability` The endpoint `GET /api/claims/{number}/ledger` returns the entries beside their sum. `src: Core features, Coverage rule 8`
- [ ] `C-CF-141` `data` Splitting `10000` across three equal lines yields `3334` on the first line. `src: Core features, Coverage rule 9`
- [ ] `C-CF-142` `constraint` A count is computed over the rows the reader received. `src: Core features, Filtering rule 1`
- [ ] `C-CF-143` `data` A biller reading the conditions of `KH-100234` receives two of the three. `src: Core features, Filtering rule 1`
- [ ] `C-CF-144` `constraint` No response states that a fact was hidden. `src: Core features, Filtering rule 2`
- [ ] `C-CF-145` `capability` The endpoint `POST /api/patients/{mrn}/break-glass` opens access to one named patient. `src: Core features, Filtering rule 3`
- [ ] `C-CF-146` `constraint` A break-glass declaration carrying a reason under twenty characters is refused. `src: Core features, Filtering rule 3`
- [ ] `C-CF-147` `constraint` A break-glass declaration opens no second patient. `src: Core features, Filtering rule 4`
- [ ] `C-CF-148` `constraint` Emergency access returns no fact labelled `restricted`. `src: Core features, Filtering rule 5`
- [ ] `C-CF-149` `data` Every access to identifiable patient data writes an `audit_event`. `src: Core features, The audit record rule 1`
- [ ] `C-CF-150` `data` A denied read writes an `audit_event`. `src: Core features, The audit record rule 1`
- [ ] `C-CF-151` `constraint` The audit entry commits before the rows are released. `src: Core features, The audit record rule 2`
- [ ] `C-CF-152` `data` An audit entry carries the acting account. `src: Core features, The audit record rule 3`
- [ ] `C-CF-153` `data` An audit entry carries the selector that was searched for. `src: Core features, The audit record rule 3`
- [ ] `C-CF-154` `data` An audit entry carries the hash of the preceding entry. `src: Core features, The audit record rule 3`
- [ ] `C-CF-155` `constraint` The app removes no audit entry. `src: Core features, The audit record rule 4`
- [ ] `C-CF-156` `capability` The endpoint `GET /api/portal/access-log` returns every access to the calling patient's record. `src: Core features, The audit record rule 5`
- [ ] `C-CF-157` `capability` A chart read by a clinician becomes the newest row in the patient's access log. `src: Core features, The audit record rule 5`
- [ ] `C-CF-158` `capability` The endpoint `GET /api/portal/record` returns the calling patient's own record. `src: Core features, The patient portal rule 1`
- [ ] `C-CF-159` `constraint` A patient asking for another patient's number is answered as for an unissued number. `src: Core features, The patient portal rule 1`
- [ ] `C-CF-160` `capability` A result is available to the patient as soon as the result is available to the clinician. `src: Core features, The patient portal rule 2`
- [ ] `C-CF-161` `constraint` No surface offers a blanket delay on releasing a result. `src: Core features, The patient portal rule 2`
- [ ] `C-CF-162` `capability` The endpoint `POST /api/portal/appointment-requests` records a request. `src: Core features, The patient portal rule 3`
- [ ] `C-CF-163` `constraint` A patient appointment request holds no slot. `src: Core features, The patient portal rule 3`
- [ ] `C-CF-164` `capability` The endpoint `POST /api/portal/demographic-proposals` records a proposed change. `src: Core features, The patient portal rule 4`
- [ ] `C-CF-165` `constraint` A demographic proposal applies no stored change. `src: Core features, The patient portal rule 4`
- [ ] `C-CF-166` `capability` The endpoint `GET /api/worklists` returns every list with a `depth`. `src: Core features, Worklists rule 1`
- [ ] `C-CF-167` `data` Every worklist carries an `oldest_age_hours`. `src: Core features, Worklists rule 1`
- [ ] `C-CF-168` `data` Every worklist carries an `owner_role`. `src: Core features, Worklists rule 2`
- [ ] `C-CF-169` `constraint` Closing a worklist item without an `outcome` is refused. `src: Core features, Worklists rule 3`
- [ ] `C-CF-170` `data` A closed worklist item stores the closing account. `src: Core features, Worklists rule 3`
- [ ] `C-CF-171` `capability` The home route stacks the announcement bar above the hero billboard. `src: Core features, The project site rule 1`
- [ ] `C-CF-172` `capability` The home route carries four action cards below the hero billboard. `src: Core features, The project site rule 1`
- [ ] `C-CF-173` `constraint` The announcement bar appears on no route other than the home route. `src: Core features, The project site rule 1`
- [ ] `C-CF-174` `literal` The first action card reads `Contribute Now`. `src: Core features, The project site rule 2`
- [ ] `C-CF-175` `literal` The second action card reads `Try Now`. `src: Core features, The project site rule 2`
- [ ] `C-CF-176` `literal` The third action card reads `Find Support`. `src: Core features, The project site rule 2`
- [ ] `C-CF-177` `literal` The fourth action card reads `Download for Free`. `src: Core features, The project site rule 2`
- [ ] `C-CF-178` `constraint` Each action card is one link covering its own icon. `src: Core features, The project site rule 2`
- [ ] `C-CF-179` `capability` The open-source statement carries the pinned free-software heading. `src: Core features, The project site rule 2`
- [ ] `C-CF-180` `literal` The feature grid is headed `A Feature-Rich Solution`. `src: Core features, The project site rule 2`
- [ ] `C-CF-181` `literal` The adopter row is headed `Who uses Kestrel`. `src: Core features, The project site rule 2`
- [ ] `C-CF-182` `literal` The contribution appeal is headed `Help Needed!`. `src: Core features, The project site rule 2`
- [ ] `C-CF-183` `literal` The contribution appeal control reads `Donate Now`. `src: Core features, The project site rule 2`
- [ ] `C-CF-184` `literal` The first feature card is titled `Scheduling`. `src: Core features, The project site rule 3`
- [ ] `C-CF-185` `literal` The second feature card is titled `e-Prescribing`. `src: Core features, The project site rule 3`
- [ ] `C-CF-186` `literal` The eighth feature card is titled `Multilingual Support`. `src: Core features, The project site rule 3`
- [ ] `C-CF-187` `capability` The route `/downloads` renders one stored release record. `src: Core features, The project site rule 4`
- [ ] `C-CF-188` `constraint` The release version comes from the same record as the artifact list. `src: Core features, The project site rule 4`
- [ ] `C-CF-189` `literal` The seeded release carries the version `8.3.0`. `src: Core features, The project site rule 4`
- [ ] `C-CF-190` `literal` The release date renders as `18 March 2026`. `src: Core features, The project site rule 4`
- [ ] `C-CF-191` `data` Every artifact carries at least two stored digests. `src: Core features, The project site rule 5`
- [ ] `C-CF-192` `constraint` A digest sits beside its artifact rather than behind a link. `src: Core features, The project site rule 5`
- [ ] `C-CF-193` `literal` The copy control reads `Copy address`. `src: Core features, The project site rule 5`
- [ ] `C-CF-194` `literal` A used copy control reads `Copied`. `src: Core features, The project site rule 5`
- [ ] `C-CF-195` `literal` The route `/demo` states `These demonstrations contain no real patient information. Everything in them is invented.`. `src: Core features, The project site rule 6`
- [ ] `C-CF-196` `constraint` The demonstration notice sits above the credentials table. `src: Core features, The project site rule 6`
- [ ] `C-CF-197` `capability` The route `/demo` renders its credentials from stored configuration. `src: Core features, The project site rule 6`
- [ ] `C-CF-198` `capability` The route `/demo` shows each instance as reachable or not. `src: Core features, The project site rule 6`
- [ ] `C-CF-199` `capability` The route `/modules` lists every module with a `licence`. `src: Core features, The project site rule 7`
- [ ] `C-CF-200` `capability` The route `/modules` lists every module with a `last_verified_on` date. `src: Core features, The project site rule 7`
- [ ] `C-CF-201` `data` Every module states whether the module sends patient information outside the practice. `src: Core features, The project site rule 7`
- [ ] `C-CF-202` `constraint` The module route states that listing is not endorsement. `src: Core features, The project site rule 7`
- [ ] `C-CF-203` `capability` A module category badge filters the list at `/modules?category=<slug>`. `src: Core features, The project site rule 8`
- [ ] `C-CF-204` `constraint` A filtered module view carries its own address. `src: Core features, The project site rule 8`
- [ ] `C-CF-205` `data` The module `skyline-telehealth` needs the core version `7.0.10`. `src: Core features, The project site rule 9`
- [ ] `C-CF-206` `data` The module `ward-reports` needs the core version `7.0.2`. `src: Core features, The project site rule 9`
- [ ] `C-CF-207` `constraint` A core version requirement is compared as an ordered version. `src: Core features, The project site rule 9`
- [ ] `C-CF-208` `capability` The route `/support` answers what the software costs to acquire. `src: Core features, The project site rule 10`
- [ ] `C-CF-209` `capability` The route `/support` states the neutral rule its vendor list is ordered by. `src: Core features, The project site rule 10`
- [ ] `C-CF-210` `ui` The route `/support` compares free support against paid support as prose rather than as a grid. `src: Core features, The project site rule 10`
- [ ] `C-CF-211` `capability` The route `/contribute` renders three platform cards of equal height. `src: Core features, The project site rule 11`
- [ ] `C-CF-212` `constraint` No platform card is marked as recommended. `src: Core features, The project site rule 11`
- [ ] `C-CF-213` `constraint` An address on the contribution route renders in full. `src: Core features, The project site rule 11`
- [ ] `C-CF-214` `constraint` The route `/contribute` carries no payment form. `src: Core features, The project site rule 11`
- [ ] `C-CF-215` `literal` The charitable-status badge reads `Registered nonprofit: donations are tax-deductible in the stated jurisdiction`. `src: Core features, The project site rule 11`
- [ ] `C-CF-216` `literal` The news index is headed `Kestrel News`. `src: Core features, The project site rule 12`
- [ ] `C-CF-217` `literal` A news card read-more link is named `Read more about` followed by its own title. `src: Core features, The project site rule 12`
- [ ] `C-CF-218` `constraint` An unmatched address answers not found rather than success. `src: Core features, When a page does not exist rule 1`
- [ ] `C-CF-219` `capability` An unmatched address renders the app's own not-found route. `src: Core features, When a page does not exist rule 1`
- [ ] `C-CF-220` `literal` The not-found route is headed `4-oh-4!`. `src: Core features, When a page does not exist rule 2`
- [ ] `C-CF-221` `literal` The not-found route reads `Looks like you were looking for a page that can't be found right now.`. `src: Core features, When a page does not exist rule 2`
- [ ] `C-CF-222` `capability` The not-found route carries the pinned second sentence about a logged mishap. `src: Core features, When a page does not exist rule 2`
- [ ] `C-CF-223` `constraint` The not-found route redirects to no home route. `src: Core features, When a page does not exist rule 2`
- [ ] `C-CF-224` `data` A not-found response is recorded as a page view carrying its own path. `src: Core features, When a page does not exist rule 3`
- [ ] `C-CF-225` `constraint` A stored page view carries nothing identifying a visitor. `src: Core features, When a page does not exist rule 3`
- [ ] `C-CF-226` `capability` The endpoint `GET /api/site/page-views` returns a page view per row. `src: Core features, When a page does not exist rule 3`
- [ ] `C-CF-227` `constraint` Every internal link on a public route resolves to a served route. `src: Core features, When a page does not exist rule 4`

## C-UF User flow

- [ ] `C-UF-01` `capability` The route `/` serves the home surface to a visitor holding no session. `src: User flow, route table row 1`
- [ ] `C-UF-02` `capability` The route `/downloads` serves the release surface to a visitor holding no session. `src: User flow, route table row 2`
- [ ] `C-UF-03` `capability` The route `/blog` serves the news index to a visitor holding no session. `src: User flow, route table row 5`
- [ ] `C-UF-04` `capability` The route `/privacy` serves a privacy notice to a visitor holding no session. `src: User flow, route table row 9`
- [ ] `C-UF-05` `capability` The route `/workspace` serves the worklist board to a staff session. `src: User flow, route table row 11`
- [ ] `C-UF-06` `capability` The route `/portal` serves a patient's own record to a patient session. `src: User flow, route table row 19`
- [ ] `C-UF-07` `constraint` An unauthenticated request for a workspace route lands on `/login`. `src: User flow, entry and redirects`
- [ ] `C-UF-08` `capability` Signing in returns the actor to the route asked for. `src: User flow, entry and redirects`
- [ ] `C-UF-09` `constraint` A patient session asking for a workspace route is refused rather than redirected. `src: User flow, entry and redirects`
- [ ] `C-UF-10` `constraint` A staff session asking for `/portal` is refused. `src: User flow, entry and redirects`
- [ ] `C-UF-11` `capability` A biller signing in lands on `/workspace`. `src: User flow, entry and redirects`
- [ ] `C-UF-12` `capability` A patient signing in lands on `/portal`. `src: User flow, entry and redirects`
- [ ] `C-UF-13` `capability` Signing out returns the actor to `/`. `src: User flow, entry and redirects`
- [ ] `C-UF-14` `constraint` A signed-out session opens neither guarded surface. `src: User flow, entry and redirects`
- [ ] `C-UF-15` `capability` An expired token returns the actor to `/login` keeping what was typed. `src: User flow, entry and redirects`
- [ ] `C-UF-16` `capability` A visitor copies a release digest from `/downloads`. `src: User flow, journey 1`
- [ ] `C-UF-17` `capability` A front desk clerk takes the last remaining slot on `2026-09-21`. `src: User flow, journey 2`
- [ ] `C-UF-18` `capability` A clinician lands on the signing confirmation after signing. `src: User flow, journey 3`
- [ ] `C-UF-19` `capability` A biller reads a patient balance after posting a balancing remittance. `src: User flow, journey 4`
- [ ] `C-UF-20` `capability` A clinician holding no relationship declares an emergency reason before reading a chart. `src: User flow, journey 5`
- [ ] `C-UF-21` `capability` Every list carries an empty state naming what would fill the list. `src: User flow, states`
- [ ] `C-UF-22` `ui` Every route carries a loading state at the destination's own shape. `src: User flow, states`
- [ ] `C-UF-23` `capability` A refused write returns the row to the previous state. `src: User flow, states`
- [ ] `C-UF-24` `capability` A refused write keeps what was typed. `src: User flow, states`
- [ ] `C-UF-25` `constraint` A chart section with nothing visible reads as a section with nothing stored. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The public routes read as institutional rather than as a product launch. `src: UI/UX notes, north star`
- [ ] `C-UX-02` `ui` The workspace reads as operational rather than editorial. `src: UI/UX notes, register`
- [ ] `C-UX-03` `ui` The product commits to one light mode throughout. `src: UI/UX notes, mode`
- [ ] `C-UX-04` `ui` One deep, soft blue grounds the header, the sidebar, the section title band. `src: UI/UX notes, palette`
- [ ] `C-UX-05` `ui` A deep, vivid cyan carries the announcement bar beside the support panel. `src: UI/UX notes, palette`
- [ ] `C-UX-06` `ui` A mid, vivid red carries every route heading. `src: UI/UX notes, palette`
- [ ] `C-UX-07` `ui` A second mid, vivid red carries the single contribute control. `src: UI/UX notes, palette`
- [ ] `C-UX-08` `ui` The default page ground is a near-white neutral. `src: UI/UX notes, palette`
- [ ] `C-UX-09` `ui` Body copy takes a deep cool neutral rather than a true black. `src: UI/UX notes, palette`
- [ ] `C-UX-10` `ui` A near-white cool neutral draws every rule beneath a section. `src: UI/UX notes, palette`
- [ ] `C-UX-11` `ui` A near-white, muted cyan is what a header link becomes under the pointer. `src: UI/UX notes, palette`
- [ ] `C-UX-12` `ui` A mid, vivid blue belongs to the module category badge alone. `src: UI/UX notes, palette`
- [ ] `C-UX-13` `ui` A deep, soft teal belongs to the zero-fee platform card alone. `src: UI/UX notes, palette`
- [ ] `C-UX-14` `ui` A light, vivid amber belongs to the not-found sticky note alone. `src: UI/UX notes, palette`
- [ ] `C-UX-15` `constraint` No surface the product styles carries a gradient. `src: UI/UX notes, palette`
- [ ] `C-UX-16` `ui` Three status meanings carry the only saturated colour on a working screen. `src: UI/UX notes, workspace palette`
- [ ] `C-UX-17` `constraint` No state is signalled by colour alone. `src: UI/UX notes, workspace palette`
- [ ] `C-UX-18` `literal` Headings use the family `Source Sans 3`. `src: UI/UX notes, type`
- [ ] `C-UX-19` `constraint` Body copy loads no font file. `src: UI/UX notes, type`
- [ ] `C-UX-20` `constraint` A monospace face carries digests, medical record numbers, coded values. `src: UI/UX notes, type`
- [ ] `C-UX-21` `ui` Figures line up on tabular numerals wherever amounts stack. `src: UI/UX notes, type`
- [ ] `C-UX-22` `ui` One entrance animates a line of text rising into place once. `src: UI/UX notes, motion`
- [ ] `C-UX-23` `ui` Every pointer transition runs at one duration on one curve. `src: UI/UX notes, motion`
- [ ] `C-UX-24` `ui` A photographic band offsets against scroll more slowly than the document. `src: UI/UX notes, motion`
- [ ] `C-UX-25` `capability` The announcement carousel pauses under a pointer. `src: UI/UX notes, motion`
- [ ] `C-UX-26` `constraint` The announcement carousel stops for good once a chevron is used. `src: UI/UX notes, motion`
- [ ] `C-UX-27` `capability` A reduced-motion preference renders the entrance at its end state. `src: UI/UX notes, motion`
- [ ] `C-UX-28` `constraint` A reduced-motion preference stops the background offset. `src: UI/UX notes, motion`
- [ ] `C-UX-29` `capability` The workspace holds a persistent sidebar as its layout archetype. `src: UI/UX notes, density`
- [ ] `C-UX-30` `capability` The workspace working surface is a grid of worklist cards. `src: UI/UX notes, density`
- [ ] `C-UX-31` `capability` Anything created in the workspace is written in the row itself. `src: UI/UX notes, density`
- [ ] `C-UX-32` `ui` Every control carries its own resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes, components`
- [ ] `C-UX-33` `constraint` An unavailable control is signalled by more than colour. `src: UI/UX notes, components`
- [ ] `C-UX-34` `capability` The support control opens on Enter rather than on a click alone. `src: UI/UX notes, components`
- [ ] `C-UX-35` `capability` The support control closes on Escape returning focus to the opener. `src: UI/UX notes, components`
- [ ] `C-UX-36` `ui` A support panel item gains contrast under the pointer. `src: UI/UX notes, components`
- [ ] `C-UX-37` `constraint` Every form control carries a persistent visible label. `src: UI/UX notes, components`
- [ ] `C-UX-38` `contract` Body text reaches a contrast ratio of at least `4.5:1` against its ground. `src: UI/UX notes, accessibility`
- [ ] `C-UX-39` `contract` Interface components reach a contrast ratio of at least `3:1`. `src: UI/UX notes, accessibility`
- [ ] `C-UX-40` `contract` Every route carries a skip link as its first focusable element. `src: UI/UX notes, accessibility`
- [ ] `C-UX-41` `contract` Every route carries exactly one level-one heading. `src: UI/UX notes, accessibility`
- [ ] `C-UX-42` `capability` Keyboard navigation reaches the worklist board. `src: UI/UX notes, accessibility`
- [ ] `C-UX-43` `constraint` The visible focus ring is removed nowhere. `src: UI/UX notes, accessibility`
- [ ] `C-UX-44` `constraint` Every content image carries alternative text. `src: UI/UX notes, accessibility`
- [ ] `C-UX-45` `constraint` A decorative image declares itself decorative. `src: UI/UX notes, accessibility`
- [ ] `C-UX-46` `capability` The navigation collapses behind a toggle below the third breakpoint. `src: UI/UX notes, responsive`
- [ ] `C-UX-47` `capability` The collapsed navigation expands in flow rather than overlaying the route. `src: UI/UX notes, responsive`
- [ ] `C-UX-48` `constraint` The contribute control stays visible beside the collapsed toggle. `src: UI/UX notes, responsive`
- [ ] `C-UX-49` `capability` The feature grid runs one column, then two, then four. `src: UI/UX notes, responsive`
- [ ] `C-UX-50` `capability` The worklist board runs one column, then two, then three. `src: UI/UX notes, responsive`
- [ ] `C-UX-51` `constraint` No route scrolls sideways at the narrowest supported viewport at twice the size. `src: UI/UX notes, responsive`
- [ ] `C-UX-52` `ui` No oversized hero stands in for content anywhere. `src: UI/UX notes, what it must not look like`
- [ ] `C-UX-53` `ui` No marketing composition appears where the workspace belongs. `src: UI/UX notes, what it must not look like`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The browser receives complete markup on first paint. `src: Technical requirements, para 1`
- [ ] `C-TR-02` `contract` The HTTP API is served under the `/api` prefix on the app origin. `src: Technical requirements, para 1`
- [ ] `C-TR-03` `contract` The store is reached at `DATABASE_URL`. `src: Technical requirements, para 1`
- [ ] `C-TR-04` `contract` Every row the app stores is readable in the PostgreSQL the environment names. `src: Technical requirements, para 1`
- [ ] `C-TR-05` `contract` The endpoint `GET /api/health` returns `200` once the app is ready. `src: Technical requirements, para 1`
- [ ] `C-TR-06` `constraint` The app introduces no second database. `src: Technical requirements, para 2`
- [ ] `C-TR-07` `constraint` The app starts no copy of PostgreSQL. `src: Technical requirements, para 3`
- [ ] `C-TR-08` `contract` Every public route carries its own meta description. `src: Technical requirements, para 4`
- [ ] `C-TR-09` `constraint` No two public routes share a title. `src: Technical requirements, para 4`
- [ ] `C-TR-10` `contract` A route title ends with the product name `Kestrel`. `src: Technical requirements, para 4`
- [ ] `C-TR-11` `contract` Every public route declares a social preview image. `src: Technical requirements, para 4`
- [ ] `C-TR-12` `constraint` A declared preview image resolves rather than answering not found. `src: Technical requirements, para 4`
- [ ] `C-TR-13` `contract` Every response carries the security header `Strict-Transport-Security`. `src: Technical requirements, para 5`
- [ ] `C-TR-14` `contract` Every response carries `X-Content-Type-Options` reading `nosniff`. `src: Technical requirements, para 5`
- [ ] `C-TR-15` `contract` Every response carries `X-Frame-Options` reading `DENY`. `src: Technical requirements, para 5`
- [ ] `C-TR-16` `contract` Every response carries `Referrer-Policy` reading `no-referrer`. `src: Technical requirements, para 5`
- [ ] `C-TR-17` `contract` Every response carries a `Content-Security-Policy`. `src: Technical requirements, para 5`
- [ ] `C-TR-18` `constraint` Nothing the browser downloads carries a credential. `src: Technical requirements, para 5`
- [ ] `C-TR-19` `constraint` No route contacts a third-party origin at runtime. `src: Technical requirements, para 6`
- [ ] `C-TR-20` `constraint` Application logs carry no medical record number. `src: Technical requirements, para 7`
- [ ] `C-TR-21` `contract` Every emitted timestamp ends in `Z`. `src: Technical requirements, para 8`
- [ ] `C-TR-22` `contract` Money is an integer count of minor units in `usd`. `src: Technical requirements, para 8`
- [ ] `C-TR-23` `constraint` No money field carries a floating point value. `src: Technical requirements, para 8`

## C-DM Data model

- [ ] `C-DM-01` `contract` The seeded password is written into `/app/USER_README.md` beside each account. `src: Data model, password paragraph`
- [ ] `C-DM-02` `data` The table `account` stores `email` as unique. `src: Data model, account`
- [ ] `C-DM-03` `data` The table `account` stores a `role` chosen from `clinician`, `front_desk`, `biller`, `patient`. `src: Data model, account`
- [ ] `C-DM-04` `data` The table `emergency_access` stores a `reason` of at least twenty characters. `src: Data model, emergency_access`
- [ ] `C-DM-05` `data` The table `audit_event` stores a `prev_hash` linking each row to the preceding row. `src: Data model, audit_event`
- [ ] `C-DM-06` `data` The table `patient` stores `mrn` as unique. `src: Data model, patient`
- [ ] `C-DM-07` `data` The table `patient` stores a `birth_date_precision` of `year`, `month` or `day`. `src: Data model, patient`
- [ ] `C-DM-08` `data` The table `patient_identifier` is unique over `system`, `value`, `period_start`. `src: Data model, patient_identifier`
- [ ] `C-DM-09` `data` The table `availability_template` stores `start_local` as a wall-clock time. `src: Data model, availability_template`
- [ ] `C-DM-10` `data` The table `appointment` stores a `status` of `booked`, `cancelled`, `completed` or `no_show`. `src: Data model, appointment`
- [ ] `C-DM-11` `data` The table `resource_occupancy` holds one row per resource an appointment claims. `src: Data model, resource_occupancy`
- [ ] `C-DM-12` `constraint` Two overlapping occupancy rows for one resource never both exist. `src: Data model, resource_occupancy`
- [ ] `C-DM-13` `data` The table `encounter` stores a `status` of `open` or `signed`. `src: Data model, encounter`
- [ ] `C-DM-14` `data` The table `clinical_note` stores a `status` of `draft`, `signed`, `amended`, `addended` or `entered_in_error`. `src: Data model, clinical_note`
- [ ] `C-DM-15` `data` The table `note_signature` stores `included_refs`. `src: Data model, note_signature`
- [ ] `C-DM-16` `data` The table `condition` stores a `sensitivity` of `normal` or `restricted`. `src: Data model, condition`
- [ ] `C-DM-17` `data` The table `service_request` stores a `status` of `draft`, `active`, `completed`, `revoked` or `entered_in_error`. `src: Data model, service_request`
- [ ] `C-DM-18` `data` The table `service_request` stores a `filler_number` apart from its own `number`. `src: Data model, service_request`
- [ ] `C-DM-19` `data` The table `observation` stores `control_id` as unique. `src: Data model, observation`
- [ ] `C-DM-20` `data` The table `allergy` stores an `assertion` of `allergy` or `no_known_allergies`. `src: Data model, allergy`
- [ ] `C-DM-21` `data` The table `medication_request` derives `patient_instruction` from the structured fields. `src: Data model, medication_request`
- [ ] `C-DM-22` `data` The table `coverage` is unique over `payer_name`, `member_number`, `period_start`. `src: Data model, coverage`
- [ ] `C-DM-23` `data` The table `claim` stores a `status` of `queued`, `submitted`, `paid` or `denied`. `src: Data model, claim`
- [ ] `C-DM-24` `data` The table `claim_line` stores `diagnosis_pointers` as ordered positions. `src: Data model, claim_line`
- [ ] `C-DM-25` `data` The table `remittance` stores a `state` of `posted` or `quarantined`. `src: Data model, remittance`
- [ ] `C-DM-26` `data` The table `remittance_line` stores an adjustment `group` of `contractual`, `patient_responsibility`, `payer_initiated` or `other`. `src: Data model, remittance_line`
- [ ] `C-DM-27` `data` The table `ledger_entry` carries rows that are only ever added. `src: Data model, ledger_entry`
- [ ] `C-DM-28` `data` The table `site_article` stores `reading_minutes` at publish time. `src: Data model, site_article`
- [ ] `C-DM-29` `data` The table `page_view` carries no visitor identifier. `src: Data model, page_view`
- [ ] `C-DM-30` `literal` The app seeds the patient `KH-100234`. `src: Data model, seed data paragraph 1`
- [ ] `C-DM-31` `literal` The app seeds the patient `KH-100235`. `src: Data model, seed data paragraph 1`
- [ ] `C-DM-32` `literal` The app seeds the patient `KH-100236`. `src: Data model, seed data paragraph 1`
- [ ] `C-DM-33` `literal` The app seeds the twin patient `KH-100237`. `src: Data model, seed data paragraph 1`
- [ ] `C-DM-34` `literal` The app seeds the twin patient `KH-100238`. `src: Data model, seed data paragraph 1`
- [ ] `C-DM-35` `literal` The app seeds the subsumed patient `KH-100239`. `src: Data model, seed data paragraph 1`
- [ ] `C-DM-36` `literal` The app seeds the surviving patient `KH-100240`. `src: Data model, seed data paragraph 1`
- [ ] `C-DM-37` `data` The patient `KH-100234` carries three stored conditions. `src: Data model, seed data paragraph 1`
- [ ] `C-DM-38` `literal` The app seeds the signed encounter `ENC-2026-0001`. `src: Data model, seed data paragraph 2`
- [ ] `C-DM-39` `literal` The app seeds the open encounter `ENC-2026-0002`. `src: Data model, seed data paragraph 2`
- [ ] `C-DM-40` `literal` The app seeds the released order `ORD-2026-0001`. `src: Data model, seed data paragraph 2`
- [ ] `C-DM-41` `literal` The app seeds the queued claim `CLM-2026-0001`. `src: Data model, seed data paragraph 2`
- [ ] `C-DM-42` `literal` The app seeds the submitted claim `CLM-2026-0002`. `src: Data model, seed data paragraph 3`
- [ ] `C-DM-43` `literal` The app seeds the paid claim `CLM-2026-0003`. `src: Data model, seed data paragraph 3`
- [ ] `C-DM-44` `literal` The app seeds the denied claim `CLM-2026-0004`. `src: Data model, seed data paragraph 3`
- [ ] `C-DM-45` `literal` The app seeds the prescription `RX-2026-0001`. `src: Data model, seed data paragraph 2`
- [ ] `C-DM-46` `literal` The app seeds the eligibility snapshot `ELG-2026-0001`. `src: Data model, seed data paragraph 3`
- [ ] `C-DM-47` `literal` The app seeds the balancing remittance `REM-2026-0001`. `src: Data model, seed data paragraph 3`
- [ ] `C-DM-48` `literal` The app seeds the unbalanced remittance `REM-2026-0002`. `src: Data model, seed data paragraph 3`
- [ ] `C-DM-49` `literal` The app seeds the cancelled appointment `APT-2026-0002`. `src: Data model, seed data paragraph 3`
- [ ] `C-DM-50` `literal` The app seeds the missed appointment `APT-2026-0003`. `src: Data model, seed data paragraph 3`
- [ ] `C-DM-51` `data` The app seeds three site articles. `src: Data model, seed data paragraph 4`
- [ ] `C-DM-52` `data` The app seeds four site modules. `src: Data model, seed data paragraph 4`
- [ ] `C-DM-53` `data` The app seeds two site announcements. `src: Data model, seed data paragraph 4`
- [ ] `C-DM-54` `constraint` Restarting the app duplicates no seeded row. `src: Data model, closing paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `literal` Fine print renders at `11.9px`. `src: Front-end specification, type scale table`
- [ ] `C-FE-02` `literal` Secondary copy renders at `13.6px`. `src: Front-end specification, type scale table`
- [ ] `C-FE-03` `literal` Body copy renders at `16px` on a line height of `23.2px`. `src: Front-end specification, type scale table`
- [ ] `C-FE-04` `literal` A card title renders at `22.4px`. `src: Front-end specification, type scale table`
- [ ] `C-FE-05` `literal` A section heading renders at `32px`. `src: Front-end specification, type scale table`
- [ ] `C-FE-06` `literal` An article first-level heading renders at `2.2rem`. `src: Front-end specification, article headings`
- [ ] `C-FE-07` `literal` The hero display line renders at `3rem` on a wide screen. `src: Front-end specification, article headings`
- [ ] `C-FE-08` `ui` The hero display line carries a hard offset shadow over the billboard ground. `src: Front-end specification, article headings`
- [ ] `C-FE-09` `ui` Six corner shapes stay distinguishable from one another. `src: Front-end specification, shape`
- [ ] `C-FE-10` `ui` One shadow exists, an even halo with no vertical offset. `src: Front-end specification, shape`
- [ ] `C-FE-11` `ui` Every horizontal rule renders at a quarter opacity. `src: Front-end specification, shape`
- [ ] `C-FE-12` `constraint` Three stacking levels exist, no more. `src: Front-end specification, shape`
- [ ] `C-FE-13` `literal` The announcement bar label reads `New:`. `src: Front-end specification, the chrome`
- [ ] `C-FE-14` `ui` The announcement dot for the current item is distinguished by more than its fill. `src: Front-end specification, the chrome`
- [ ] `C-FE-15` `capability` The header stays in place as the page moves beneath the header. `src: Front-end specification, the chrome`
- [ ] `C-FE-16` `capability` The announcement bar scrolls out of view as the header stays put. `src: Front-end specification, the chrome`
- [ ] `C-FE-17` `constraint` The wordmark is one link whose accessible name is the product name. `src: Front-end specification, the chrome`
- [ ] `C-FE-18` `ui` The footer carries four columns above four centred lines of fine print. `src: Front-end specification, the chrome`
- [ ] `C-FE-19` `ui` The footer attribution line credits the sources the drawn geometry derives from. `src: Front-end specification, the chrome`
- [ ] `C-FE-20` `constraint` Every symbol is drawn as inline vector geometry. `src: Front-end specification, icons`
- [ ] `C-FE-21` `capability` Eight icons sit above the eight feature cards. `src: Front-end specification, icons`
- [ ] `C-FE-22` `ui` The monitor icon above the second action card carries no surrounding circle. `src: Front-end specification, icons`
- [ ] `C-FE-23` `constraint` An organisation mark in the adopter row renders as the organisation's name in type. `src: Front-end specification, icons`
- [ ] `C-FE-24` `constraint` A certification mark renders as a bordered plate carrying text. `src: Front-end specification, icons`
- [ ] `C-FE-25` `constraint` A card lead image is generated from a seed derived from its own slug. `src: Front-end specification, icons`
- [ ] `C-FE-26` `constraint` The not-found illustration is a tilted sticky note with a strip of tape. `src: Front-end specification, icons`
- [ ] `C-FE-27` `constraint` No third-party video player loads before a visitor asks for one. `src: Front-end specification, icons`
- [ ] `C-FE-28` `ui` The home route stacks nine bands in a fixed order. `src: Front-end specification, the home route`
- [ ] `C-FE-29` `ui` A photographic band carries a colour overlay rather than an image treatment. `src: Front-end specification, the home route`
- [ ] `C-FE-30` `constraint` A photographic band carries no text. `src: Front-end specification, the home route`
- [ ] `C-FE-31` `constraint` A photographic band is exposed as decorative. `src: Front-end specification, the home route`
- [ ] `C-FE-32` `capability` The workspace sidebar carries the six worklists above the register. `src: Front-end specification, the workspace`
- [ ] `C-FE-33` `capability` A chart reads top to bottom from demographics down to encounters. `src: Front-end specification, the workspace`
- [ ] `C-FE-34` `capability` A worklist card carries its own depth beside the age of its oldest item. `src: Front-end specification, the workspace`
- [ ] `C-FE-35` `capability` A worklist holding nothing says so rather than rendering an empty card. `src: Front-end specification, the workspace`
- [ ] `C-FE-36` `capability` The signing confirmation states the locked note version on its own line. `src: Front-end specification, the signing confirmation`
- [ ] `C-FE-37` `capability` The signing confirmation offers exactly two onward actions. `src: Front-end specification, the signing confirmation`
- [ ] `C-FE-38` `constraint` A form error is stated in text beside its own field. `src: Front-end specification, the forms`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app serves one clinic rather than a second tenant. `src: Constraints, bullet 1`
- [ ] `C-CN-02` `constraint` The app carries no inpatient surface. `src: Constraints, bullet 2`
- [ ] `C-CN-03` `constraint` The app parses no positional clinical message format. `src: Constraints, bullet 3`
- [ ] `C-CN-04` `constraint` The app runs no population export. `src: Constraints, bullet 4`
- [ ] `C-CN-05` `constraint` The app performs no payment transaction. `src: Constraints, bullet 5`
- [ ] `C-CN-06` `constraint` The app sends no email. `src: Constraints, bullet 6`
- [ ] `C-CN-07` `constraint` The app stores no uploaded file. `src: Constraints, bullet 7`
- [ ] `C-CN-08` `constraint` The app loads no third-party analytics. `src: Constraints, bullet 8`
- [ ] `C-CN-09` `constraint` The app carries no site search. `src: Constraints, bullet 9`
- [ ] `C-CN-10` `constraint` The app carries one language. `src: Constraints, bullet 10`
- [ ] `C-CN-11` `constraint` The app ships no native application. `src: Constraints, bullet 11`
- [ ] `C-CN-12` `constraint` The app stays responsive with a few thousand stored encounters. `src: Constraints, bullet 12`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-02` `contract` The container-internal port is `4173`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-03` `contract` The outside port comes from `APP_PUBLIC_PORT`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-04` `contract` The HTTP API is served under the `/api` prefix. `src: Deployment contract, bullet 2`
- [ ] `C-DC-05` `contract` The route `GET /api/health` answers `200` once the app is ready. `src: Deployment contract, bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract, bullet 4`
- [ ] `C-DC-07` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract, bullet 5`
- [ ] `C-DC-08` `contract` The directory `.browser_screenshots/` exists empty at the app root. `src: Deployment contract, bullet 6`
- [ ] `C-DC-09` `contract` The directory `.downloads/` exists empty at the app root. `src: Deployment contract, bullet 6`
- [ ] `C-DC-10` `contract` The app serves a production build rather than a dev server. `src: Deployment contract, bullet 7`
- [ ] `C-DC-11` `contract` The server keeps running after the session ends. `src: Deployment contract, bullet 8`
- [ ] `C-DC-12` `contract` The server binds `0.0.0.0`. `src: Deployment contract, bullet 9`
- [ ] `C-DC-13` `constraint` The app downloads no copy of a backing service. `src: Deployment contract, bullet 10`
- [ ] `C-DC-14` `constraint` The app uses no edge function. `src: Deployment contract, bullet 11`
- [ ] `C-DC-15` `constraint` The app declares no persistent volume. `src: Deployment contract, bullet 12`
- [ ] `C-DC-16` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-17` `contract` An invalid call is rejected as a client error rather than a server error. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-18` `contract` A rejection carries a message naming the reason. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-19` `contract` Bearer auth is required on every endpoint outside health, login, the public site reads. `src: Deployment contract, API shapes closing paragraph`
- [ ] `C-DC-20` `constraint` No stored record is substituted by a value the app returns to itself. `src: Deployment contract, no mocks paragraph`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `E11.9` | code of the seeded diabetes diagnosis | C-CF-35 | Core features, Coded values rule 4 |
| `F11.20` | code of the seeded restricted diagnosis | C-CF-36 | Core features, Coded values rule 4 |
| `99213` | code of the seeded billed procedure | C-CF-37 | Core features, Coded values rule 4 |
| `2823-3` | code of the seeded potassium observation | C-CF-38 | Core features, Coded values rule 4 |
| `860975` | code of the seeded prescribed medication | C-CF-39 | Core features, Coded values rule 4 |
| `Contribute Now` | first action card label on the home route | C-CF-174 | Core features, The project site rule 2 |
| `Try Now` | second action card label on the home route | C-CF-175 | Core features, The project site rule 2 |
| `Find Support` | third action card label on the home route | C-CF-176 | Core features, The project site rule 2 |
| `Download for Free` | fourth action card label on the home route | C-CF-177 | Core features, The project site rule 2 |
| `A Feature-Rich Solution` | heading of the feature grid | C-CF-180 | Core features, The project site rule 2 |
| `Who uses Kestrel` | heading of the adopter row | C-CF-181 | Core features, The project site rule 2 |
| `Help Needed!` | heading of the contribution appeal | C-CF-182 | Core features, The project site rule 2 |
| `Donate Now` | label of the contribution appeal control | C-CF-183 | Core features, The project site rule 2 |
| `Scheduling` | title of the first feature card | C-CF-184 | Core features, The project site rule 3 |
| `e-Prescribing` | title of the second feature card | C-CF-185 | Core features, The project site rule 3 |
| `Multilingual Support` | title of the eighth feature card | C-CF-186 | Core features, The project site rule 3 |
| `8.3.0` | version of the seeded release | C-CF-189 | Core features, The project site rule 4 |
| `18 March 2026` | rendered release date on the download route | C-CF-190 | Core features, The project site rule 4 |
| `Copy address` | resting label of the copy control | C-CF-193 | Core features, The project site rule 5 |
| `Copied` | label of the copy control once used | C-CF-194 | Core features, The project site rule 5 |
| `/demo` | route carrying the demonstration notice | C-CF-195 | Core features, The project site rule 6 |
| `These demonstrations contain no real patient information. Everything in them is invented.` | notice above the demonstration credentials | C-CF-195 | Core features, The project site rule 6 |
| `Registered nonprofit: donations are tax-deductible in the stated jurisdiction` | charitable-status badge on the contribution route | C-CF-215 | Core features, The project site rule 11 |
| `Kestrel News` | heading of the news index | C-CF-216 | Core features, The project site rule 12 |
| `Read more about` | accessible-name prefix of a news card read-more link | C-CF-217 | Core features, The project site rule 12 |
| `4-oh-4!` | heading of the not-found route | C-CF-220 | Core features, When a page does not exist rule 2 |
| `Looks like you were looking for a page that can't be found right now.` | first sentence of the not-found route | C-CF-221 | Core features, When a page does not exist rule 2 |
| `KH-100234` | medical record number of the first seeded patient | C-DM-30 | Data model, seed data paragraph 1 |
| `KH-100235` | medical record number of the second seeded patient | C-DM-31 | Data model, seed data paragraph 1 |
| `KH-100236` | medical record number of the year-precision patient | C-DM-32 | Data model, seed data paragraph 1 |
| `KH-100237` | medical record number of the first seeded twin | C-DM-33 | Data model, seed data paragraph 1 |
| `KH-100238` | medical record number of the second seeded twin | C-DM-34 | Data model, seed data paragraph 1 |
| `KH-100239` | medical record number subsumed by a merge | C-DM-35 | Data model, seed data paragraph 1 |
| `KH-100240` | medical record number surviving a merge | C-DM-36 | Data model, seed data paragraph 1 |
| `ENC-2026-0001` | number of the seeded signed encounter | C-DM-38 | Data model, seed data paragraph 2 |
| `ENC-2026-0002` | number of the seeded open encounter | C-DM-39 | Data model, seed data paragraph 2 |
| `ORD-2026-0001` | number of the seeded released order | C-DM-40 | Data model, seed data paragraph 2 |
| `CLM-2026-0001` | number of the seeded queued claim | C-DM-41 | Data model, seed data paragraph 2 |
| `CLM-2026-0002` | number of the seeded submitted claim | C-DM-42 | Data model, seed data paragraph 3 |
| `CLM-2026-0003` | number of the seeded paid claim | C-DM-43 | Data model, seed data paragraph 3 |
| `CLM-2026-0004` | number of the seeded denied claim | C-DM-44 | Data model, seed data paragraph 3 |
| `RX-2026-0001` | number of the seeded prescription | C-DM-45 | Data model, seed data paragraph 2 |
| `ELG-2026-0001` | number of the seeded eligibility snapshot | C-DM-46 | Data model, seed data paragraph 3 |
| `REM-2026-0001` | number of the balancing remittance | C-DM-47 | Data model, seed data paragraph 3 |
| `REM-2026-0002` | number of the remittance one minor unit out | C-DM-48 | Data model, seed data paragraph 3 |
| `APT-2026-0002` | number of the seeded cancelled appointment | C-DM-49 | Data model, seed data paragraph 3 |
| `APT-2026-0003` | number of the seeded missed appointment | C-DM-50 | Data model, seed data paragraph 3 |
| `11.9px` | rendered size of the footer fine print | C-FE-01 | Front-end specification, type scale table |
| `13.6px` | rendered size of secondary copy | C-FE-02 | Front-end specification, type scale table |
| `16px` | rendered size of body copy | C-FE-03 | Front-end specification, type scale table |
| `23.2px` | line height inherited across four rendered sizes | C-FE-03 | Front-end specification, type scale table |
| `22.4px` | rendered size of a card title | C-FE-04 | Front-end specification, type scale table |
| `32px` | rendered size of a section heading | C-FE-05 | Front-end specification, type scale table |
| `2.2rem` | rendered size of an article first-level heading | C-FE-06 | Front-end specification, article headings |
| `3rem` | rendered size of the hero display line on a wide screen | C-FE-07 | Front-end specification, article headings |
| `New:` | label leading the announcement bar | C-FE-13 | Front-end specification, the chrome |
| `clinician@example.com` | seeded clinician account holding a care-team relationship | C-RL-29 | User roles, seeded accounts table row 1 |
| `clinician2@example.com` | seeded clinician account holding no relationship | C-RL-30 | User roles, seeded accounts table row 2 |
| `frontdesk@example.com` | seeded front desk account | C-RL-31 | User roles, seeded accounts table row 3 |
| `biller@example.com` | seeded biller account | C-RL-32 | User roles, seeded accounts table row 4 |
| `patient@example.com` | seeded portal account bound to the first patient | C-RL-33 | User roles, seeded accounts table row 5 |
| `patient2@example.com` | seeded portal account bound to the second patient | C-RL-34 | User roles, seeded accounts table row 6 |
| `deku-demo-pw-2026` | password every seeded account signs in with | C-RL-35 | User roles, seeded accounts paragraph |
| `Source Sans 3` | the one display family the product self-hosts | C-UX-18 | UI/UX notes, type |
| `Fully Open-Source. Free Software, Always and Forever.` | heading of the open-source statement | C-CF-179 | Core features, The project site rule 2 |
| `Sorry about that, the mishap has been logged and we'll look into it.` | second sentence of the not-found route | C-CF-222 | Core features, When a page does not exist rule 2 |
| `APP_PUBLIC_URL` | environment variable naming the public origin | C-DC-01 | Deployment contract, bullet 1 |
| `4173` | container-internal port | C-DC-02 | Deployment contract, bullet 1 |
| `APP_PUBLIC_PORT` | environment variable naming the public port | C-DC-03 | Deployment contract, bullet 1 |
| `/api` | prefix the HTTP API is served under | C-DC-04 | Deployment contract, bullet 2 |
| `/app/USER_README.md` | file carrying the seeded logins | C-DC-07 | Deployment contract, bullet 5 |
| `.browser_screenshots/` | reserved empty directory at the app root | C-DC-08 | Deployment contract, bullet 6 |
| `.downloads/` | reserved empty directory at the app root | C-DC-09 | Deployment contract, bullet 6 |
| `0.0.0.0` | address the server binds | C-DC-12 | Deployment contract, bullet 9 |
| `DATABASE_URL` | environment variable naming the store | C-TR-03 | Technical requirements, para 1 |
| `DB_URL` | second environment variable carrying the store address | C-TR-04 | Technical requirements, para 1 |
| `GET /api/health` | health route | C-TR-05 | Technical requirements, para 1 |
| `200` | status the health route returns | C-TR-05 | Technical requirements, para 1 |
| `Kestrel` | product name every route title ends with | C-TR-10 | Technical requirements, para 4 |
| `Z` | suffix on every emitted timestamp | C-TR-21 | Technical requirements, para 8 |
| `usd` | currency every stored amount carries | C-TR-22 | Technical requirements, para 8 |
| `4.5:1` | minimum contrast ratio for body text | C-UX-30 | UI/UX notes, accessibility |
| `3:1` | minimum contrast ratio for interface components | C-UX-31 | UI/UX notes, accessibility |
| `6.2` | value of the first potassium version | C-CF-15 | Core features, The record refuses to forget rule 2 |
| `4.1` | value of the second potassium version | C-CF-16 | Core features, The record refuses to forget rule 2 |
| `1988` | birth date of the year-precision patient | C-CF-24 | Core features, The record refuses to forget rule 7 |
| `ng/mL` | unit of the seeded troponin observation | C-CF-28 | Core features, The record refuses to forget rule 8 |
| `18500` | charge on the seeded claim line, in minor units | C-CF-140 | Core features, Coverage rule 5 |
| `12000` | amount the balancing remittance paid, in minor units | C-CF-140 | Core features, Coverage rule 5 |
| `4500` | contractual adjustment on the balancing remittance | C-CF-141 | Core features, Coverage rule 5 |
| `2000` | patient responsibility on the balancing remittance | C-CF-142 | Core features, Coverage rule 5 |
| `3334` | first share when 10000 splits across three equal lines | C-CF-149 | Core features, Coverage rule 9 |
| `10000` | amount split across three equal lines in the worked example | C-CF-149 | Core features, Coverage rule 9 |
| `500` | dose quantity on the seeded prescription | C-CF-121 | Core features, Prescribing and allergies rule 2 |
| `60` | dispense quantity on the seeded prescription | C-CF-122 | Core features, Prescribing and allergies rule 2 |
| `penicillin` | substance of the seeded recorded allergy | C-CF-128 | Core features, Prescribing and allergies rule 4 |
| `7.0.10` | core version the telehealth module needs | C-CF-205 | Core features, The project site rule 9 |
| `7.0.2` | core version the reporting module needs | C-CF-206 | Core features, The project site rule 9 |
| `2026-09-21` | seeded day whose last remaining slot is contended | C-UF-17 | User flow, journey 2 |
| `nosniff` | value of the content-type policy header | C-TR-14 | Technical requirements, para 5 |
| `DENY` | value of the frame policy header | C-TR-15 | Technical requirements, para 5 |
| `no-referrer` | value of the referrer policy header | C-TR-16 | Technical requirements, para 5 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the lookback window an encounter relationship stays open for | C-RL-22 | named as bounded with no stated length |
| the bounded period an emergency declaration stays open for | C-CF-155 | named as bounded with no stated length |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 5 |
| User roles | 2 | 37 |
| Core features | 40 | 227 |
| User flow | 5 | 25 |
| UI and UX notes | 5 | 53 |
| Technical requirements | 5 | 23 |
| Data model | 4 | 54 |
| Front-end specification | 1 | 38 |
| Constraints | 1 | 12 |
| Deployment contract | 10 | 20 |
