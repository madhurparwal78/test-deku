# Clinical Records Platform

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser, read the project site, copy a
release digest, and sign in as a clinician to open an encounter, write its note, code its diagnosis,
place its order and sign it, landing on a confirmation that names the locked note version, the
orders that were released and the claim that was queued, without hitting an error page. A different
clinician, one with no relationship to that patient, must NOT be able to tell a real medical record
number from one that was never issued, by any means, including a direct request for the chart by its
own path. A signed note must re-render a day later to the same stored hash even after the patient's
medication list has moved on; a note that re-reads the list at display time is a different document
wearing the same signature.

## Overview

Kestrel is an open-source health record for a small clinic, and the public project site that
distributes it. Two products sit under one codebase and the seam between them is a sign-in screen.

The public half is a volunteer community explaining a serious piece of infrastructure. There is
nothing to buy, no trial, no sales contact and no signup. It publishes the current release with the
digests an administrator needs to verify it, a demonstration that holds no real patient data, a
directory of modules that plug into the record, a news index, an honest page about what free
software costs to run, and a way to contribute. It is institutional rather than commercial, and the
design carries that.

The record half is used by four kinds of staff and by the patients they treat. It holds a patient
register, an appointment book, encounters with their notes, coded diagnoses, orders, results,
prescriptions, insurance coverage and claims. It is evidentiary: nothing in it is overwritten and
nothing is removed. A correction writes a new version that names what it supersedes and why, and
every earlier version stays readable forever. A clinician's visit ends at one action, signing the
encounter, and that action does three things at once: it locks the note against a stored rendering,
it releases the encounter's orders, and it queues its claim.

It deliberately is not a hospital system. There are no beds, no theatre lists and no ward rounds. It
speaks no wire message format to a laboratory or a clearing house, runs no population export, hosts
no third-party application, computes no quality measure and carries no decision-support rule engine.
It takes no payment on any surface, sends no email, uploads no file and carries no second language.

The genuinely hard part is that four readers look at one record and each is owed a different subset
of it, and the boundary has to hold in three places at once: the row, the column, and the arithmetic
over both. An app that filters the list and then reports the unfiltered count has told the reader
exactly how many facts were hidden and roughly when they were added.

## User roles

Five roles. Every account is seeded; nothing anywhere creates one.

| Role | Can read | Can write |
|---|---|---|
| `clinician` | the chart of a patient they hold a relationship with, including facts labelled `restricted` | notes, coded diagnoses, orders, prescriptions, allergies; signs an encounter |
| `front_desk` | patient demographics, coverage and the appointment book | registers a patient, books, cancels and reschedules appointments, records coverage |
| `biller` | the claims worklist, and the coded diagnoses of an encounter that justify a charge | eligibility checks, claim submissions, remittance postings |
| `patient` | their own record and the log of who has read it | an amendment request, an appointment request, a proposed demographic change |
| `clinician2` is an ordinary `clinician` account and is named here only because it holds no relationship to the seeded patients | | |

What each role **cannot** do is the part that is graded:

- A `clinician` **cannot** open the chart of a patient they hold no relationship with, **cannot**
  edit a note once it is signed, and **cannot** sign an encounter that carries no coded diagnosis.
- A `front_desk` account **cannot** read a note, a coded diagnosis, an order, a result or a
  prescription, and **cannot** sign anything.
- A `biller` **cannot** read a note, a result or a prescription, and **cannot** read any fact
  labelled `restricted`, including in a count.
- A `patient` **cannot** read another patient's record by any path, **cannot** open any `/workspace`
  route, and **cannot** edit a stored fact: an amendment request attaches their statement beside the
  record and leaves the original standing.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `patient` session to any `clinician`-only endpoint must
be rejected by the server (an unauthorized request is denied, not served), leaving the protected
state unchanged.

Holding a clinical role does not open a chart. What opens a chart is a relationship with that
particular patient: being on their care team, being the clinician on an encounter of theirs, holding
a scheduled appointment with them, or holding an emergency declaration named for them. A read of a
chart the reader may not open and a read of a medical record number that was never issued answer
with the same status and the same body, and they must be indistinguishable to the caller. A distinct
refusal on a record that exists is a confirmation that a named person is a patient here, and that
confirmation is the disclosure that matters before any clinical detail is read at all.

There is no signup. There is no route, form or field by which an account is created or by which an
account chooses or changes its own role, and a request to any address that looks like one answers
exactly as any unrouted path does.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Role | Seeded state |
|---|---|---|
| `clinician@example.com` | clinician | on the care team of `KH-100234` and `KH-100235`; author of the draft note on `ENC-2026-0002` |
| `clinician2@example.com` | clinician | holds no relationship to any seeded patient |
| `frontdesk@example.com` | front_desk | no patient relationship is needed or held |
| `biller@example.com` | biller | works the four seeded claims |
| `patient@example.com` | patient | bound to `KH-100234` |
| `patient2@example.com` | patient | bound to `KH-100235` |

## Core features

### Accounts and sessions

The app implements its own accounts: email and password, with a bearer token the client sends on
every authenticated request. Passwords are stored hashed, never in plain text, and never returned by
any endpoint.

1. `POST /api/auth/login` with a seeded email and `deku-demo-pw-2026` returns a token, the email and
   the role. A wrong password is denied and returns no token.
2. A request that carries no token, or a token the app did not issue, is denied on every guarded
   endpoint, and the stored state is unchanged.
3. The acting role is read from the stored account row. A role named in a request body, a query
   string or a header is ignored, and the account keeps the role it was seeded with.
4. There is no account-creation endpoint. `POST /api/auth/signup`, `POST /api/auth/register` and
   `POST /api/accounts` are addresses this product does not serve: each answers as an unrouted
   path answers, and no account exists afterwards that did not exist before.

### The record refuses to forget

This is the rule every other clinical rule stands on.

1. Every clinical fact is stored as an immutable version. A correction writes a new version carrying
   a `version_id` one higher, a `supersedes` naming the version it replaces, and a `reason`. The
   earlier version stays readable at `GET /api/observations/{id}/history` and the equivalents for a
   patient, a condition and a note.
2. Reading a fact returns its highest version. Nothing in the clinical record is updated in place
   and nothing is removed, so a history read of the seeded potassium on `ENC-2026-0001` returns two
   entries: `6.2` recorded first, then `4.1` which supersedes it and carries its reason.
3. `entered_in_error` is a status and not a deletion. `POST /api/conditions/{id}/retract` sets it
   with a stored reason: the fact leaves the chart, stays in the history read, and is still
   counted by the history read. A retraction that removes the row is a failure however correct
   the screen looks.
4. Three statements that look alike are kept apart and are never collapsed into one action: a course
   that `completed`, a course the patient `stopped` early, and a record that was `entered_in_error`
   and was never real.
5. Every clinical fact carries two clocks rather than one: `effective_time`, when it was true of
   the patient, and `recorded_time`, when this app came to know it. The two clocks are routinely
   far apart, a patient reports on a Tuesday a seizure that happened on the Sunday, and both are
   returned on every clinical read.
6. `GET /api/patients/{mrn}/conditions?as_known_at=<timestamp>` returns the chart as it stood at
   that instant rather than as it stands now. Asked with the `recorded_time` of the first potassium
   version, the observation read returns `6.2`; asked with no `as_known_at`, it returns `4.1`.
7. A date carries its own precision. `KH-100236` has a birth date known only to the year and is
   returned as `1988` with `birth_date_precision` reading `year`. No surface anywhere renders
   `1988-01-01`, because inventing a day fabricates a fact that then matches this patient to the
   wrong person somewhere else.
8. A quantity carries a coded unit and, where the value is bounded rather than exact, a comparator.
   The seeded troponin is returned as a value of `0.01` with `comparator` reading `<` and
   `unit_code` reading `ng/mL`. A read that drops the comparator has turned an undetectable quantity
   into a detected one, which reverses the clinical meaning.

### Coded values

1. A coded value is four fields and never one: `code_system`, `code`, `code_display` as captured at
   the time of recording, and `code_version`. All four are stored and all four are returned.
2. Comparison is on `code_system` and `code` together. `E11.9` in `icd10cm` and a same-spelled code
   in another system are different values, and `code_display` is never a key.
3. The display text stored with a fact is the text rendered for that fact forever. Re-rendering a
   historical code against today's display text silently rewrites a signed note.
4. The code systems in use are `icd10cm` for diagnoses, `cpt` for billed procedures, `loinc` for
   laboratory observations and `rxnorm` for medications, with `ucum` carrying units. The seeded
   values are `icd10cm` `E11.9` `Type 2 diabetes mellitus without complications` at version `2026`,
   `icd10cm` `F11.20` `Opioid dependence, uncomplicated` at version `2026`, `cpt` `99213`
   `Office or other outpatient visit, established patient, low level` at version `2026`, `loinc`
   `2823-3` `Potassium [Moles/volume] in Serum or Plasma` at version `2.76`, and `rxnorm` `860975`
   `metformin hydrochloride 500 MG Oral Tablet` at version `2026-03`.

### The patient register

1. `GET /api/patients?family=<name>&birth_date=<date>` searches the register and returns only
   patients the caller may open. A query that matches nothing and a query whose every match was
   filtered away return the same body and the same count of zero.
2. A patient has one internal identity and many external identifiers. Uniqueness is over
   `system`, `value` and `period_start` together and never over `value` alone, so registering
   `KH-100236` with the insurance member number `M-4471` succeeds even though `KH-100235` held that
   member number on a policy that has ended.
3. `POST /api/patients` registers a patient and returns the assigned `mrn`. A registration whose
   family name, birth date, address and telephone all match a stored patient and whose given name
   does not opens an `identity_review` row carrying `twin_warning` reading `true`, and the response
   states that a possible match exists and must be checked without naming the matched record or its
   medical record number.
4. Matching has three outcomes and never two. Above the automatic band the records are linked; below
   the review band they are treated as distinct; between them the candidate is queued for a person
   and is resolved automatically in neither direction.
5. A merge is a link and never a rewrite. `GET /api/patients/KH-100239` returns the survivor
   `KH-100240` together with a field stating that the identity moved and naming the survivor. The
   subsumed row is not deleted, no clinical fact is repointed, and the merge carries the fields a
   reversal needs.

### The appointment book

1. `GET /api/appointments/availability?provider=<email>&date=<date>` computes free time at read time
   from the provider's weekly template, minus leave and closures, minus what is already booked. The
   app stores no table of empty slots.
2. An appointment holds more than its face duration, and each resource is held for its own interval:
   the room is held from five minutes before the start until five minutes after the end, and the
   clinician is held until ten minutes after the end.
3. `POST /api/appointments` books one appointment and writes one occupancy row per resource it
   holds, in one action. Two simultaneous requests for the last remaining slot on `2026-09-21` must
   not both succeed: exactly one is accepted, the other is rejected as a conflict naming the clash,
   and exactly one appointment exists afterwards. This must hold under real concurrency.
4. A booking whose clinician is free and whose room is taken fails whole. No occupancy row and no
   appointment survives a failed booking.
5. `POST /api/appointments/{number}/cancel` releases every occupancy row in the same action that
   sets the status to `cancelled`, and the slot is immediately bookable again.
6. `POST /api/appointments/{number}/reschedule` claims the new time before releasing the old one. If
   the new time is taken the patient keeps the original appointment, which stays `booked` at its
   original time, and nothing is released.
7. `no_show` is a status on a period that happened. It does not free the slot afterwards, it is not
   a cancellation, and it survives into the worklists rather than being cleaned up.

### The encounter and its note

1. `POST /api/encounters` opens an encounter for a patient the calling clinician may open, and
   returns its `number`. The encounter is visible to the care team from the moment it is opened.
2. A note in `draft` is readable only by its author. `ENC-2026-0002` carries a draft note by
   `clinician@example.com`, and `clinician2@example.com` reading that encounter sees the encounter
   itself and no note body. The encounter being visible while its note is not is the point: nobody
   should think the visit did not happen.
3. `PATCH /api/encounters/{number}/note` carries the `version_id` the editor loaded. A save against
   a stale version is refused, the response carries the current version and the current body, and
   nothing is merged. Two clinical narratives merged automatically produce a sentence neither author
   wrote.
4. `POST /api/encounters/{number}/conditions` adds a coded diagnosis to the encounter. Its four code
   fields are all required and a condition missing any of them is refused as invalid.
5. `POST /api/encounters/{number}/orders` adds an order. A new order is created in `draft`, and a
   `draft` order is not an instruction: it is not released, it does not appear in
   `GET /api/orders?status=active`, and nothing may transmit it.

### Signing, and everything it releases

This is the one action the whole workspace exists to reach. `POST /api/encounters/{number}/sign`
does three things at once and either all of them happen or none does.

1. It locks the note. A `note_signature` is stored carrying the signing account, the instant, a
   `rendering_hash` over the note as rendered, the `template_version`, the `terminology_versions` in
   force, and `included_refs` naming the identity and version of every fact the note pulled in.
2. It releases every order the encounter holds from `draft` to `active`.
3. It queues the claim: one `claim` row at status `queued`, carrying an ordered `diagnoses` list
   copied from the encounter's coded conditions and one `claim_line` per billed procedure.
4. The response carries `encounter_number`, `note_version_id`, `rendering_hash`, `orders_released`
   as a count and `claim_number`, and the client is taken to
   `/workspace/encounters/{number}/signed`, which states the same four facts in words.
5. Signing an encounter that carries no coded diagnosis is refused, and nothing changes: no order
   moves to `active`, no claim exists, and the note stays `draft`.
6. Signing an encounter that is already `signed` is refused. No second claim is queued, no order is
   released a second time, and the stored `rendering_hash` is unchanged.
7. `GET /api/encounters/{number}/rendering` returns the note exactly as it was rendered at signing,
   together with the stored `rendering_hash`. Adding a medication to that patient afterwards changes
   neither the returned text nor the hash. A note that renders a live query at display time is a
   note whose content moves after signature, which means the signature attests to something that no
   longer exists.
8. A signed note is never edited. `POST /api/encounters/{number}/addendum` appends new information
   with its own author, instant and reason, rendered after the note. `POST
   /api/encounters/{number}/amendment` writes a new note version with its own reason while the
   original stays readable in the history. Both require a reason and both refuse without one.
9. A patient who disagrees uses `POST /api/portal/amendment-requests`. Their statement is attached
   to the record, the clinician's entry stands unchanged, and the app does not resolve the
   disagreement in either direction.

### Results

1. `POST /api/results` records a result against the order named by its `placer_number`, storing the
   `control_id` the sender supplied. A result carrying a `control_id` already stored is recorded
   once: the repeat is answered with the first outcome and creates no second observation.
2. The reference range and the abnormal flag arrive with the result and are stored with the
   observation. The app consults no range table of its own, because the same analyte has different
   normal ranges by method, by age, by sex and in pregnancy. The seeded potassium carries
   `reference_low` `3.5`, `reference_high` `5.1` and `unit_code` `mmol/L`.
3. A correction is a new version and never an overwrite, and it raises a re-review item for whoever
   saw the original.
4. State is sequenced by the times inside the result rather than by the order of arrival. A result
   whose `effective_time` is older than the one already current is stored and does not become
   current, so a stale message cannot undo a correction.
5. A result whose patient cannot be identified is never filed against a guess and never discarded.
   It is held in the reconciliation queue at `GET /api/results/unmatched`, which has an owner and an
   age, and the seeded queue holds exactly one.

### Prescribing and allergies

1. `POST /api/prescriptions` captures dosage as structured fields and renders `patient_instruction`
   from them. Free text is never the source of truth.
2. `dose_quantity` and `dispense_quantity` are different numbers in different units and are never
   conflated: the seeded `RX-2026-0001` is `500` `mg` per administration and `60` `tablet`
   dispensed. `refills_authorised` is `0`, and zero is a value rather than an absent one.
3. The safety check runs on the server over the patient's complete record, including facts the
   prescriber may not see. Where the conflict is with a fact the prescriber may not see, the
   response states that a conflict exists and how severe it is and names nothing about the
   conflicting entry, and it offers the route to ask the patient for consent. Where the prescriber
   may see the fact, the response names it.
4. Three allergy states are distinct and are never collapsed. `KH-100234` carries a recorded allergy
   to `penicillin` with reaction `anaphylaxis` and criticality `high`. `KH-100235` carries a
   `no_known_allergies` assertion with its author and its date. `KH-100236` carries nothing at all,
   and the allergy read for that patient returns `assertion` reading `not_asked`. An empty list
   rendered as an assertion of safety is a clinical claim nobody made.

### Coverage, eligibility and the claim

1. `POST /api/eligibility` stores a dated snapshot carrying its own number, the instant it was
   checked, whether the policy was active and the coverage level the payer stated. No surface
   renders a stored snapshot as today's answer: every eligibility read returns `checked_at` beside
   it.
2. A claim is built from the encounter's own facts and references them. `claim_line` rows point at
   diagnoses by position in the claim's own ordered `diagnoses` list through
   `diagnosis_pointers`, and never by repeating the code. A pointer at a position that does not
   exist is refused as invalid.
3. A line's quantity is not always a count. `unit_qualifier` reads `unit` or `minute` and says
   which, so a line billed in minutes is never sent as a bare count.
4. `POST /api/claims/{number}/submit` moves a `queued` claim to `submitted`. A claim that is not
   `queued` is refused and its status is unchanged.
5. `POST /api/remittances` posts a remittance, and the arithmetic must hold exactly, in minor units,
   per line and for the claim as a whole: a line's charge equals what was paid on it plus every
   adjustment against it, and the claim's charge equals the sum of its lines. `REM-2026-0001`
   balances: the single line's charge of `18500` equals `12000` paid plus a `contractual` adjustment
   of `4500` plus a `patient_responsibility` adjustment of `2000`.
6. A remittance that does not balance is not posted at all. `REM-2026-0002` is one minor unit out
   and is stored `quarantined` with its reason, raises a worklist item, and changes no claim status
   and no balance. There is no tolerance of a single minor unit: a minor unit that appears from
   nowhere has to be put somewhere, and wherever it is put it is wrong.
7. Only the `patient_responsibility` group creates patient balance. After `REM-2026-0001` posts, the
   patient balance on that claim is `2000` and never `6500`. Billing a patient for the contractual
   discount the practice agreed to give is a compliance failure rather than a small error.
8. Every financial event writes ledger entries that sum to zero across one `transaction_id`, nothing
   is ever edited afterwards, and a balance is the sum over entries rather than a stored running
   total. `GET /api/claims/{number}/ledger` returns the entries and their sum.
9. Splitting an amount across lines has one right answer and always the same one: compute each share
   exactly, take the floor of each in minor units, then distribute the remaining minor units one at
   a time in descending order of the fraction that was dropped, breaking ties by line number
   ascending. `POST /api/allocations` performs that split, and `10000` across three equal lines is
   `3334`, `3333`, `3333`, in that order, on every call.

### Filtering, counts and emergency access

1. A reader who may not see a fact is not told it exists. Every count, every total, every page
   total and every latest-updated instant is computed from the rows the reader actually received.
   `biller@example.com` reading the conditions of `KH-100234` receives two of its three, and the
   `total` field reads two.
2. No response states that anything was hidden, and a chart section with nothing visible reads
   exactly as a chart section with nothing in it.
3. `POST /api/patients/{mrn}/break-glass` opens emergency access to one named patient. It requires a
   typed `reason` of at least twenty characters; a shorter reason is refused as invalid and opens
   nothing. A menu alone would produce the word emergency every time.
4. Emergency access is bounded, expires without renewal, and names one patient. It is never a mode
   the actor enters: after declaring for `KH-100234`, the same account asking for `KH-100235` is
   still answered as though that record does not exist.
5. Access opened by an emergency declaration carries facts labelled `normal` and never facts
   labelled `restricted`, and the counts it returns exclude them without saying so.

### The audit record and the access log

1. Every access to identifiable patient data is recorded, including a read that returned nothing and
   including a read that was denied. The most common real breach in a record system is somebody
   reading a chart they had no business reading and changing nothing at all, so a log of writes
   cannot see it.
2. The entry is written and committed before the rows are released. If the entry cannot be written
   the operation fails and the caller is shown an error rather than the data.
3. Each entry names the acting account, the patient, the action, the outcome, what was reached and
   the selector that was searched for, and carries the hash of the entry before it so a later edit
   no longer joins up.
4. Entries are only ever added. Nothing in the app updates or removes one.
5. `GET /api/portal/access-log` returns, to the patient, every access to their own record in
   reverse-chronological order. After `clinician@example.com` opens the chart of `KH-100234`, that
   read is the newest row in the log of `patient@example.com`.

### The patient portal

1. `GET /api/portal/record` returns the calling patient's own record and nobody else's. A patient
   asking for another patient's medical record number is answered exactly as for a number that was
   never issued.
2. Release is the default. A result is available to the patient at the same moment it is available
   to the clinician. A blanket delay while a clinician reviews it is not offered anywhere, and the
   record instead states honestly that a result has not yet been reviewed, which is a different
   thing from hiding it.
3. `POST /api/portal/appointment-requests` records a request rather than a booking. It occupies
   nothing and holds nothing, and it reaches the appointment-request worklist.
4. `POST /api/portal/demographic-proposals` records a proposed change to the patient's own
   demographics and applies nothing. Demographics are matching keys, and a self-service change to a
   birth date silently changes who this record matches.

### Worklists

1. `GET /api/worklists` returns every list with its `key`, its `owner_role`, its `depth` and the age
   in hours of its oldest item. The keys are `unsigned_notes`, `unmatched_results`,
   `identity_review`, `quarantined_remittances`, `denied_claims` and `appointment_requests`.
2. Every list is owned by a role rather than by a person, so nothing is invisible while somebody is
   on leave, and every item carries its age without being asked for it.
3. Nothing is cleared without an outcome. `POST /api/worklists/{key}/items/{id}/close` requires an
   `outcome` and records its author, and `no_action_needed` is an outcome with an author rather than
   an absence.

### The project site

1. The home route carries, in this order: the announcement bar, the hero billboard, four action
   cards, the open-source statement, the latest news, the eight-card feature grid, the adopter row,
   the contribution appeal and the deployment pair. The announcement bar appears on the home route
   and on no other, because lifting it everywhere pushes nine routes down by the height of a bar
   that should not be there.
2. The four action cards read `Contribute Now`, `Try Now`, `Find Support` and `Download for Free`,
   in that order, and each card is one link including its icon. The open-source statement is headed
   `Fully Open-Source. Free Software, Always and Forever.`, the feature grid is headed
   `A Feature-Rich Solution`, the adopter row is headed `Who uses Kestrel`, and the contribution
   appeal is headed `Help Needed!` above a control reading `Donate Now`.
3. The eight feature cards are titled `Scheduling`, `e-Prescribing`, `Medical Billing`, `Reporting`,
   `Lab Integration`, `Clinical Decision Rules`, `Advanced Security` and `Multilingual Support`.
4. `/downloads` renders one release record. The version, the release date and the artifact list come
   from a single stored record rather than three independently edited strings, so the route can
   never announce one version in its heading while linking the artifacts of another. The seeded
   release is `8.3.0`, released on a date rendered with its month named rather than numbered, as
   `18 March 2026`.
5. Every artifact carries at least two digests, shown beside the artifact rather than behind a link,
   in a monospace face, selectable as a plain string, with a control beside each reading
   `Copy address` and reading `Copied` once used. An administrator who has to transcribe a digest by
   hand will not verify it, and an unverified download of a record system is the supply-chain
   problem this route exists to prevent.
6. `/demo` states, before the credentials and not after, that
   `These demonstrations contain no real patient information. Everything in them is invented.` It
   names when the demonstration resets and in which time standard, renders its credentials from the
   demonstration's own configuration rather than from typed-in copy, and shows each instance as
   reachable or not with the age of that check when the check is older than its interval.
7. `/modules` lists every module with its name, its vendor, its categories, the core version it
   needs, its licence, where its source can be read, when it was last verified, and whether it sends
   patient information outside the practice. The route states that listing is not endorsement and
   that entries are ordered by name.
8. A module's category badge is a link that filters the list, and the filtered view is a route with
   its own address at `/modules?category=<slug>` rather than a control that only changes the screen.
   A directory whose categories are decoration is a directory nobody can navigate, and a filter with
   no address is a filter nobody can share.
9. Version requirements are compared as ordered versions and never as strings. The seeded
   `skyline-telehealth` needs `7.0.10` and `ward-reports` needs `7.0.2`, and `7.0.10` is the higher
   of the two.
10. `/support` answers three questions plainly: what the software costs to acquire, which is
    nothing; what it costs to run; and what happens if a vendor disappears, which is that the
    software and the records stay with the practice. It ranks no vendor, it states the neutral rule
    its vendor list is ordered by, and it compares free and paid support as prose rather than as a
    grid of ticks.
11. `/contribute` renders three platform cards of equal height with their controls aligned on one
    baseline, nothing marked as recommended, defaulted or preselected, and two address rows whose
    addresses are rendered in full and never truncated. Its charitable-status badge reads
    `Registered nonprofit: donations are tax-deductible in the stated jurisdiction`, because a
    deductibility claim is true only somewhere and a donor who gives on the strength of an
    unqualified badge has been misled. The control beside each address copies
    exactly the string on the screen, read once from one value. The route takes no payment: no form,
    no amount picker, no card field, no suggested amount and no list of past donors.
12. `/blog` is the news index and is headed `Kestrel News`. Each card carries its article's title as
    a link, its date, its excerpt and a read-more link whose accessible name reads
    `Read more about` followed by the article's own title.

### When a page does not exist

1. Any unmatched address renders the app's own not-found route and answers not found rather than
   success. A not-found route served as a success is invisible to every link checker and every
   monitoring tool.
2. The route is headed `4-oh-4!` and reads
   `Looks like you were looking for a page that can't be found right now.` then
   `Sorry about that, the mishap has been logged and we'll look into it.` It is never a redirect to
   the home route: a redirect discards the address the visitor asked for, which is the one piece of
   evidence needed to fix the link that sent them.
3. That second sentence is a promise and it is binding. Every not-found response is recorded as a
   page view carrying its path, the referring page where one was sent, and the status, and carrying
   nothing that identifies the visitor. The log is readable by a signed-in staff account at
   `GET /api/site/page-views`, which returns a page view per row with its path and its instant.
4. Every internal link on every public route resolves to a route the app serves. An internal link
   that answers not found is a broken product rather than a broken page.
5. Six addresses are deliberately absent, because the product carries none of the things they would
   name: `/signup`, `/register`, `/search`, `/checkout`, `/beds` and `/export`. Each answers exactly
   as any address the product never served answers.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | home: announcement, billboard, four action cards, the statement, the news, the feature grid, the adopters, the appeal, the deployment pair | public |
| `/downloads` | the current release, its date, its artifacts and their digests | public |
| `/demo` | the no-real-data notice, the reset schedule, the credentials table, instance health | public |
| `/support` | what the software costs to acquire and to run, and who offers paid help | public |
| `/blog` | the news index | public |
| `/blog/kestrel-8-3-0-is-released` | one article | public |
| `/modules` | the module directory, filtered by `?category=` | public |
| `/contribute` | three platform cards and two address rows | public |
| `/privacy` | the privacy notice | public |
| `/login` | sign in | public |
| `/workspace` | the worklist board | staff |
| `/workspace/patients` | the patient register | staff |
| `/workspace/patients/KH-100234` | one chart | scoped |
| `/workspace/schedule` | the appointment book | clinician, front_desk |
| `/workspace/encounters/ENC-2026-0001` | one encounter and its note | clinician |
| `/workspace/encounters/ENC-2026-0001/signed` | the confirmation after signing | clinician |
| `/workspace/claims` | the claims worklist | biller |
| `/workspace/claims/CLM-2026-0001` | one claim and its remittance | biller |
| `/portal` | a patient's own record, its access log and the two requests | patient |

**Entry and redirects.** An unauthenticated request for any `/workspace` or `/portal` route lands on
`/login`, and signing in returns to the route that was asked for. A `patient` session asking for a
`/workspace` route is refused rather than redirected into it, and a staff session asking for
`/portal` is refused the same way. A clinician, a front desk clerk and a biller all land on
`/workspace`; a patient lands on `/portal`. Signing out returns to `/` and the same session then
opens neither guarded surface. A token that has expired mid-action returns the actor to `/login`
with what they typed still in the form. A request for a chart the reader may not open answers
exactly as a request for a medical record number that was never issued.

**Journeys.**

1. **Evaluate the project.** Open `/`, read the announcement, follow `Download for Free` to
   `/downloads`, copy the container artifact's digest with the control beside it and watch the
   control read `Copied`, then follow `Try Now` to `/demo` and read the no-real-data notice above
   the credentials table.
2. **Register and book.** Sign in as `frontdesk@example.com`, open `/workspace/patients`, register a
   patient whose family name, birth date, address and telephone match the seeded twin `KH-100237`
   and whose given name does not, read the possible-match warning that names nobody, then open
   `/workspace/schedule` and take the last remaining slot on `2026-09-21`.
3. **See the patient and sign.** Sign in as `clinician@example.com`, open `/workspace`, open the
   unsigned-note card, open `ENC-2026-0002`, write the note in the row, add the coded diagnosis
   `E11.9`, add an order, sign, and land on the confirmation reading the locked note version, the
   number of orders released and the queued claim number.
4. **Work the money.** Sign in as `biller@example.com`, open `/workspace/claims`, open
   `CLM-2026-0001`, submit it, post `REM-2026-0001`, read a patient balance of `2000`, then post
   `REM-2026-0002` and read it quarantined with its reason on the worklist board while the claim
   status is unchanged.
5. **Stay in your own lane.** Sign in as `clinician2@example.com`, ask for `KH-100234` and be
   answered as though it does not exist, declare an emergency reason of at least twenty characters,
   read the chart with two of its three conditions and a count reading two, then sign in as
   `patient@example.com` and find both reads in the access log.

**States.** Every list has an empty state naming what would fill it, every route has a loading state
at the destination's own shape rather than a spinner, and no failure takes a route down with it. A
refused write returns the row to what it was and states beside it what failed, keeping what was
typed. The worklist board with nothing open says so plainly rather than rendering empty cards. A
chart section with nothing visible reads exactly as a chart section with nothing in it.

## UI/UX notes

**North star.** Somebody arriving at the public routes should understand within one screen that this
is serious infrastructure maintained by a community rather than a product launch; somebody opening a
chart should understand what is true of this patient and when it became true without reading twice.
The honest north star for both halves is comprehension, and neither half invents a feeling the
product does not support. **Register.** The public routes are institutional and dense rather than
airy, with photography used as a band rather than as an ornament; the workspace is operational,
quiet and built for scanning and repeated action. Two stances hold the product together and a
competing product could rationally invert either: **evidence over reassurance** on the public
routes, and **the record over the interface** in the workspace.

**Mode.** Committed to light and designed fully in light. There is no dark mode to grade.

**Palette by role.** One deep, soft blue is the institutional colour and is the only colour in the
product that grounds a whole surface: the sticky header, the workspace sidebar, the section title
band above the news index, and every display heading wear it and nothing else does. The announcement
bar, the support panel and the highlight block behind a news title all take a deep, vivid cyan.
Two reds exist and neither may take the other's work: a mid, vivid red carries every route heading
and a footer link under the pointer, and a second mid, vivid red carries the single contribute
control, which is the only saturated ground anywhere in the header. The default page ground is a
near-white neutral and cards, the header bar and form controls sit on it. Body copy is a deep cool
neutral, and the same deep cool neutral one step lighter carries secondary copy and footer links. A
near-white cool neutral draws every rule and border and is the ground a feature card takes under the
pointer. A near-white, muted cyan is what a header link becomes under the pointer and appears
nowhere else. A mid, vivid blue belongs to the category badge in the module directory
alone. A deep, soft teal belongs to the zero-fee platform card and the charitable-status badge
alone. A light, vivid amber belongs to the sticky note on the not-found route alone. No gradient is applied to any surface the
product styles itself, which is most of why this reads as institutional rather than commercial. The
exact shades are yours, so long as each meaning keeps its colour exclusively and the contrast floors
below hold.

In the workspace the same palette is spent differently: the sidebar takes the institutional colour,
every working surface sits on the page ground, and three meanings are the only saturated colour on a
working screen, one for a fact that is refused or abnormal, one for a fact that is settled and
signed, and one for a fact still in progress. A state that is none of the three borrows none of
them, and no state is signalled by colour alone: every one carries a word beside it.

**Type.** Body copy uses the reader's own system stack and loads no font file at all. That is a real
decision with a real consequence, paragraphs render in a different face on every operating system,
and it is kept rather than tidied away. Headings use `Source Sans 3`, under the SIL Open Font
License, self-hosted at two weights and subset to the copy the product renders, with the system sans
behind it so a failed font load never blocks text. A monospace stack carries digests, medical record
numbers, coded values and money columns and nothing else. Body copy sits at `16px` on a line height
of `23.2px`, and that line height recurs across four sizes because it is inherited rather than set
per step; it is not normalised to a ratio. Figures line up on tabular numerals wherever amounts,
counts or identifiers stack, which here means every column in the workspace, every digest on the
download route and every money column on a claim. The full scale is in the front-end specification
below.

**Motion.** One entrance exists in the whole product: a line of text fades in while rising a short
distance, plays once, and ends at its resting position rather than a little below it. Everything
else that moves is a colour change under the pointer, and every one of them runs at one short
duration on one symmetrical curve, so the whole product moves at one speed and nothing uses a
different speed to feel special. The full-bleed photographic bands offset vertically against scroll
position, more slowly than the document, without moving the text over them. The announcement
carousel advances on a timer long enough to read the longer of its two announcements, pauses while a
pointer is over it or focus is inside it, and stops for good once a visitor uses either chevron.
Under a reduced-motion preference the entrance does not animate and its element renders at its end
state, the background offset stops and the image sits still, the carousel does not advance by itself
while its controls keep working, and every transition drops to no duration while the states
themselves still change. Nothing in the workspace moves while somebody is reading a queue.

**Density and layout.** The public routes are dense rather than airy: the feature grid carries eight
cards in one arrangement and the home route stacks nine full-width bands rather than spacing out
three. The workspace inverts nothing and adds compactness: its layout archetype is a persistent
sidebar, its working surface is a grid of worklist cards, and rows sit tight enough that a full
worklist is read without scrolling. Anything created in the workspace is written in the row itself,
so the queue never disappears while it is being worked, and the one moment that earns a route of its
own is the confirmation after signing.

**Components.** Every control carries resting, pointed-at, pressed, focused and unavailable states,
and unavailable is never signalled by colour alone. The support control is a button with an expanded
state rather than a link: it opens on click and on Enter or Space, closes on Escape returning focus
to whatever opened it, closes on an outside click, and moves through its items with the arrow keys.
Its item under the pointer gains contrast rather than losing it. Every form control carries a
persistent visible label, never a placeholder standing in for one, and a field in error carries a
message beside it rather than a colour alone.

**Accessibility floors, which are contract rather than taste.** The product meets WCAG 2.1 level AA
and the workspace is held to the same bar, because that is where this gets skipped and where staff
spend the day. Body text reaches at least `4.5:1` against its ground, and large display text,
interface components and the focus ring reach at least `3:1`. Every route carries a skip link as its
first focusable element, one banner, one navigation, one main and one footer landmark, exactly one
level-one heading and no skipped level. Keyboard navigation reaches every control, including the
support panel, the collapsed navigation, the announcement carousel and the worklist board, and the
visible focus ring is never removed anywhere; against the institutional ground it becomes a solid
outline in the light text colour rather than a translucent halo. Colour is never the only carrier of
meaning: the dot for the current announcement carries a second signal beyond its fill, and the copy
control confirms in words. Every content image carries alternative text and a decorative image
declares itself decorative rather than being described. Nothing flashes more than three times a
second.

**Responsive.** Five layout tiers and the product reflows rather than hides: nothing on a handset is
missing that a wide screen has, except the billboard lead line, which is hidden at the narrowest
viewport and therefore says nothing that is said nowhere else. Above the third breakpoint the header
carries its navigation in one row; below it the navigation collapses behind a toggle, expands in
flow rather than overlaying the route so it is not focus-trapped, and Escape collapses it and
returns focus to the toggle. The contribute control stays visible beside the collapsed toggle rather
than being buried inside it. The action cards run two across then four, the feature grid one then
two then four, the news grid one then two then three and four at the widest, and the worklist board
one then two then three with the sidebar persistent. Footer columns stack, then two, then four. A
ground that appears under the pointer must not persist after a tap. No route scrolls sideways at the
narrowest supported viewport at twice the size, and only the credentials table and the digest
strings scroll within their own box.

**What it must not look like.** A startup home page is the wrong answer here in four specific ways,
and each is rejectable on sight. An oversized hero standing in for content pushes the four actions
this route exists for below the fold. A gradient anywhere on a surface the product styles for itself
breaks the flat institutional reading the whole palette is built on. Editorial spacing and
decorative imagery around a worklist turn a working queue into a brochure. And a clinical state
legible only as a colour swatch, with no word beside it, is a state that half the readers of this
product cannot read at all.

## Technical requirements

Front end: SvelteKit, server-rendering every route so the browser receives complete markup on first
paint rather than an application shell, with interactivity added only where a reader needs it: the
announcement carousel, the module category filter, the schedule grid and the worklist board. Back
end: Express on Node 20, serving the HTTP API on the same origin under the `/api` prefix, with both
halves served by one process on the container-internal port. Store: PostgreSQL, reached at
`DATABASE_URL`, which the environment also exports as `DB_URL` with the same value. Auth:
app-implemented email and password with bearer tokens, passwords stored hashed. Health:
`GET /api/health` returns `200` once the app is ready.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing service
available in this environment is PostgreSQL, and reaching for anything else is a contract violation.

PostgreSQL is already running and reachable at that variable. Do not download, install, compile or
start a copy of it, and never hardcode a host, a port or a credential that the environment supplies.

Machine-readable surfaces: every public route serves its own title and its own meta description and
no two routes share either; a route title reads as the route's own name, then a separator, then
`Kestrel`. Every public route also declares a social preview title and a preview image, and the
preview image resolves rather than answering not found.

Every response on every route carries the security headers `Strict-Transport-Security`,
`X-Content-Type-Options` reading `nosniff`, `X-Frame-Options` reading `DENY`, `Referrer-Policy`
reading `no-referrer` and `Content-Security-Policy`. Nothing the browser downloads carries a
credential, a database URL or a token.

No third-party origin is contacted at runtime by any route: no font service, no analytics, no tag
manager, no video player and no consent tool. The two display font faces are self-hosted.

Application logs are structured lines on standard output carrying the request method, the path, the
status and the elapsed milliseconds, and they carry no patient name, no birth date and no medical
record number.

All timestamps are UTC and are sent as ISO 8601 strings ending in `Z`. Money is an integer count of
minor units in `usd`, and the currency accompanies every amount the API returns. No floating point
value appears in any money field.

## Data model

Twenty-eight tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**`account`** - `id`, `email` unique, `password_hash`, `display_name`, `role` which is one of
`clinician`, `front_desk`, `biller` or `patient`, `created_at`. Two addresses can never share an
account.

**`care_team_member`** - `id`, `patient_id`, `account_id`, `role_on_team`, `period_start`,
`period_end`.

**`emergency_access`** - `id`, `account_id`, `patient_id`, `reason`, `declared_at`, `expires_at`.
The `reason` is at least twenty characters and is stored as typed. One row names one patient.

**`audit_event`** - `id`, `actor_id`, `patient_id`, `action`, `outcome`, `purpose`, `entity_refs`,
`selector`, `occurred_at`, `prev_hash`, `hash`. Rows are only ever added; the app updates none and
removes none, and each row's `prev_hash` is the `hash` of the row before it.

**`patient`** - `id`, `mrn` unique, `family_name`, `given_name`, `birth_date`,
`birth_date_precision` which is `year`, `month` or `day`, `sex`, `address_line`, `postal_code`,
`telephone`, `status`, `version_id`, `supersedes`, `reason`, `recorded_at`, `recorded_by`. A
correction inserts a new version; no row is rewritten.

**`patient_identifier`** - `id`, `patient_id`, `system`, `value`, `type`, `period_start`,
`period_end`, `assigner`. Unique on `system`, `value` and `period_start` together, never on `value`
alone: a member number is reissued when a policy ends and a new subscriber takes it.

**`patient_link`** - `id`, `survivor_id`, `subsumed_id`, `merged_at`, `merged_by`, `reason`,
`reversed_at`, `reversed_by`, `reversal_reason`.

**`identity_review`** - `id`, `candidate_mrn`, `matched_mrn`, `score`, `twin_warning`, `state`,
`opened_at`, `outcome`, `outcome_by`.

**`availability_template`** - `id`, `provider_id`, `location`, `weekday`, `start_local`, `end_local`,
`slot_minutes`, `effective_start`, `effective_end`. `start_local` and `end_local` are wall-clock
times rather than instants, because a clinic at nine o'clock is at nine o'clock all year.

**`appointment`** - `id`, `number` unique, `patient_id`, `provider_id`, `room`, `starts_at`,
`ends_at`, `local_time`, `zone_id`, `status` which is `booked`, `cancelled`, `completed` or
`no_show`, `created_at`.

**`resource_occupancy`** - `id`, `appointment_id`, `resource_kind`, `resource_id`, `period_start`,
`period_end`. One row per resource an appointment holds. Two overlapping rows for one resource must
never both exist, and that must hold under simultaneous requests rather than only when the app looks
first.

**`encounter`** - `id`, `number` unique, `patient_id`, `clinician_id`, `class`, `started_at`,
`ended_at`, `status` which is `open` or `signed`, `created_at`.

**`clinical_note`** - `id`, `encounter_id`, `version_id`, `supersedes`, `body`, `status` which is
`draft`, `signed`, `amended`, `addended` or `entered_in_error`, `reason`, `recorded_at`,
`recorded_by`. A save carries the `version_id` it loaded, and a save against a stale version changes
nothing.

**`note_signature`** - `id`, `note_id`, `note_version_id`, `signed_by`, `signed_at`,
`rendering_hash`, `template_version`, `terminology_versions`, `included_refs`. `included_refs`
carries the identity and the version of every fact the note pulled in, which is what makes the
rendering reproducible after the underlying facts have moved on.

**`condition`** - `id`, `patient_id`, `encounter_id`, `code_system`, `code`, `code_display`,
`code_version`, `clinical_status`, `sensitivity` which is `normal` or `restricted`, `effective_time`,
`recorded_time`, `version_id`, `supersedes`, `reason`, `recorded_by`.

**`service_request`** - `id`, `number` unique, `encounter_id`, `patient_id`, `code_system`, `code`,
`code_display`, `code_version`, `intent`, `priority`, `status` which is `draft`, `active`,
`completed`, `revoked` or `entered_in_error`, `filler_number`, `effective_time`, `recorded_time`,
`version_id`. The `number` this app assigns and the `filler_number` the performer assigns are
different identifiers and neither is assumed unique on its own.

**`observation`** - `id`, `service_request_id`, `patient_id`, `code_system`, `code`, `code_display`,
`code_version`, `value_number`, `comparator`, `unit_code`, `reference_low`, `reference_high`,
`abnormal_flag`, `status` which is `preliminary`, `final`, `corrected` or `entered_in_error`,
`control_id`, `effective_time`, `recorded_time`, `version_id`, `supersedes`, `reason`. Two
observations can never share a `control_id`, which is what makes a repeat land once.

**`unmatched_result`** - `id`, `control_id`, `payload`, `stated_mrn`, `received_at`, `state`,
`outcome`, `outcome_by`.

**`allergy`** - `id`, `patient_id`, `substance`, `reaction`, `criticality`, `assertion` which is
`allergy` or `no_known_allergies`, `recorded_by`, `recorded_at`. A patient with no row at all is
reported as `not_asked`, which is a derived reading rather than a stored value and is not the same
statement as `no_known_allergies`.

**`medication_request`** - `id`, `number` unique, `patient_id`, `encounter_id`, `code_system`,
`code`, `code_display`, `code_version`, `dose_quantity`, `dose_unit`, `dose_route`,
`frequency_per_day`, `duration_days`, `dispense_quantity`, `dispense_unit`, `refills_authorised`,
`patient_instruction`, `sensitivity`, `status`, `recorded_at`, `recorded_by`. `patient_instruction`
is derived from the structured fields rather than stored independently of them.

**`coverage`** - `id`, `patient_id`, `payer_name`, `member_number`, `rank` which is `primary` or
`secondary`, `period_start`, `period_end`. Unique on `payer_name`, `member_number` and
`period_start` together.

**`eligibility_check`** - `id`, `number` unique, `coverage_id`, `checked_at`, `active`,
`coverage_level`, `raw_response`.

**`claim`** - `id`, `number` unique, `encounter_id`, `patient_id`, `coverage_id`,
`eligibility_check_id`, `status` which is `queued`, `submitted`, `paid` or `denied`, `diagnoses` as
an ordered list of coded values, `total_charge_minor`, `currency`, `queued_at`.

**`claim_line`** - `id`, `claim_id`, `line_number`, `code_system`, `code`, `code_display`,
`unit_qualifier` which is `unit` or `minute`, `units`, `charge_minor`, `diagnosis_pointers` as an
ordered list of positions into the claim's own `diagnoses`.

**`remittance`** - `id`, `number` unique, `claim_id`, `received_at`, `state` which is `posted` or
`quarantined`, `quarantine_reason`.

**`remittance_line`** - `id`, `remittance_id`, `claim_line_id`, `paid_minor`, `adjustments` as a
list of entries each carrying `group`, `reason` and `amount_minor`, where `group` is one of
`contractual`, `patient_responsibility`, `payer_initiated` or `other`.

**`ledger_entry`** - `id`, `transaction_id`, `account_bucket`, `patient_id`, `claim_id`,
`amount_minor`, `currency`, `source`, `occurred_at`, `recorded_at`. Rows are only ever added, and
the entries sharing one `transaction_id` sum to zero. A balance is the sum over entries rather than
a stored column that is incremented.

**`site_release`** and **`site_artifact`** - the release carries `version`, `released_on` and
`notes_url`; each artifact carries `channel`, `label`, `href`, `sha256` and `sha512`.

**`site_article`** - `id`, `slug` unique, `title`, `headline`, `excerpt`, `body`, `published_at`,
`reading_minutes`, `featured`. `reading_minutes` is stored at publish time rather than recomputed on
render, because a figure that changes when the renderer changes is a figure nobody trusts.

**`site_module`** - `id`, `slug` unique, `name`, `vendor`, `summary`, `categories`,
`min_core_version`, `source_url`, `licence`, `sends_data_outside`, `last_verified_on`.

**`site_announcement`** - `id`, `label`, `body`, `link_label`, `link_href`, `rank`.

**`page_view`** - `id`, `path`, `referrer`, `status`, `viewed_at`. It carries nothing that identifies
a visitor.

**Seed data.** Six accounts as listed in `## User roles`. Seven patients: `KH-100234` Amara Okafor
born `1974-03-11`; `KH-100235` Tobias Vance born `1991-07-02`; `KH-100236` Noor Haddad born `1988`
at year precision; the twins `KH-100237` Lena Farrow and `KH-100238` Lars Farrow, both born
`2016-05-09` and sharing an address and a telephone; and the merged pair `KH-100239` subsumed into
`KH-100240`, both Ivo Brenner. `KH-100234` carries three conditions, of which the `F11.20` one is
`restricted` and the other two are `normal`; `KH-100235` carries a `no_known_allergies` assertion
and `KH-100236` carries no allergy row at all.

`ENC-2026-0001` is signed, with its locked note, its released order `ORD-2026-0001` and its queued
claim `CLM-2026-0001`. `ENC-2026-0002` is open, with a `draft` note authored by
`clinician@example.com`. The potassium observation on `ENC-2026-0001` has two versions, `6.2` then
`4.1`, and a troponin observation carries the comparator `<` at `0.01` `ng/mL`. One unmatched result
sits in the reconciliation queue. `RX-2026-0001` is the seeded prescription.

`clinician@example.com` holds a weekly availability template on `2026-09-21` whose slots are all
booked except the last one, `APT-2026-0002` is `cancelled` and `APT-2026-0003` is `no_show`. Four
claims are seeded, `CLM-2026-0001` `queued`, `CLM-2026-0002` `submitted`, `CLM-2026-0003` `paid` and
`CLM-2026-0004` `denied`, with `ELG-2026-0001` the eligibility snapshot the first relied on.
`REM-2026-0001` balances and `REM-2026-0002` is one minor unit out.

Three articles, four modules, one release with two digests per artifact and two announcements are
seeded for the project site.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

The visual detail the six sections above state as intent, written out surface by surface. Nothing
here is decoration: every paragraph describes something a reader can see and a reviewer can reject.

**The type scale, carried exactly.**

| Step | Size | Line height | What carries it |
|---|---|---|---|
| fine print and legal lines | `11.9px` | `11.9px` | the footer's four closing lines |
| secondary copy, captions, table cells | `13.6px` | `23.2px` | the credentials table, digests, dates |
| dense list copy | `14px` | `23.2px` | the module directory |
| category and status badges | `14.4px` | `17.28px` | every pill |
| body copy | `16px` | `23.2px` | every paragraph |
| subheads | `17.6px` | `21.12px` | card subheads |
| lead paragraphs | `20px` | `23.2px` | the opening line of an article |
| card titles | `22.4px` | `23.2px` | news cards |
| subordinate section headings | `28.8px` | `34.56px` | a second-level band heading |
| section headings | `32px` | `38.4px` | every band heading |

Inside an article the heading scale runs `2.2rem`, `2rem`, `1.8rem`, `1.6rem`, `1.4rem` and `1.2rem`
from the first level to the sixth. Every first-level heading takes the route-heading red and every
display heading takes the institutional blue. The hero display line is `3rem`, falling to `2.25rem`
on a medium screen and `1.75rem` at the narrowest, and it carries a hard offset shadow where it sits
over the billboard ground: an unfashionable choice, and the only thing keeping that line legible
over an image nobody controls.

**Shape, depth and grid.** Corners are barely softened and the softening is not uniform. Six shapes
exist and stay unmistakably different from one another: the default softening on controls and
buttons, a card's leading image softened on its top two corners only, a card's footer softened on
its bottom two, a slightly larger softening on the copy control, a larger one again on the platform
cards, and a full capsule on a badge. A status dot and an address dot are circles. The exact radii
are yours as long as those six stay distinguishable at a glance.

One shadow exists in the whole product: an even halo spread equally on all sides with no vertical
offset, carried by the news card alone, and it reads as a halo rather than as a lift. Every
horizontal rule renders at a quarter opacity, and articles use rules as their section separators.
There are exactly three stacking levels and no others: the support panel above the page, the sticky
header above that, and the fixed mirror behind the document that carries the photographic bands. The
layout runs on five container widths and one gutter, and every spacing value is a multiple of one
base unit, which is yours to choose.

**The chrome.** The announcement bar sits in flow at the very top of the home route, full bleed and
centred, carrying a label reading `New:`, the announcement text, a trailing link, a chevron on each
side and one dot per announcement with the current one distinguished by more than its fill. The main
header is sticky, full bleed and one row: the wordmark at the left, the navigation at the centre
right, the support control, the contribute control and the source repository mark at the far right.
The bar stays as the page moves under it while the announcement above it scrolls away. The wordmark
is one link to the home route whose accessible name is the product name, with its drawn mark hidden
from assistive technology. The footer carries four columns, the wordmark and three link columns
headed for the project, for help and for developers, then four centred lines of fine print. The
attribution line survives and credits whatever this build's own drawn geometry derives from: quietly
deleting a credit line because the assets it credited were replaced is how a licence obligation gets
broken by accident.

**Icons and imagery.** No image file, no icon font and no video ships. Every symbol is drawn as
inline vector geometry, a decorative icon is hidden from assistive technology, and an icon that is
the only content of its control hands its name to the control rather than carrying one itself. Eight
icons sit above the eight feature cards: a calendar, a prescription document, a billing document, a
stacked report pair, a laboratory vial with a syringe, a branching rule flow, a padlock and a globe
drawn as a meridian construction rather than as filled continents. Four icons sit above the four
action cards: a heart in a circle, a monitor with a pointer and no surrounding circle, a question
mark in a circle and a download arrow in a circle, and the third of the four carrying no circle is
deliberate rather than an oversight. The three organisation marks in the adopter row are third-party
trademarks and are not drawn, approximated or redrawn: they are set as the organisation's name in
the display face, centred in a cell of the image's own height. A certification mark is likewise not
drawn; it is replaced by a bordered plate carrying the programme name, the product, the version and
the date as text. Card lead images and the video still are generated at build time from a seed
derived from the record's own slug, so the same article always gets the same plate and a rebuild
never silently changes what the product looks like. The not-found illustration is a tilted sticky
note with a strip of tape over one corner and a hand-lettered word, built from four shapes and a
shadow. No third-party video player is loaded before a visitor asks for one: a still frame and a
control named for its own subject stand in its place, and the player is fetched only on activation.

**The home route, band by band.** Nine bands in this order: the announcement bar; the hero billboard
on the institutional ground carrying the campaign headline as a link, the positioning line as a
paragraph that carries the visual weight of a heading without being one, and the four action cards;
the open-source statement on the page ground; the latest-news pair; the eight-card feature grid; a
full-bleed photographic band; the adopter row; a second photographic band; and the contribution
appeal. Every photographic band runs the full width at the height of the window, carries a colour
overlay rather than an image treatment, carries no text at all, and is exposed as decorative. At the
narrowest viewport a further dark wash goes over the band so that anything nearby stays readable.
Because no band carries any words, a band that fails to load costs the route its atmosphere and none
of its meaning, and that property is worth protecting deliberately.

**The workspace.** A persistent sidebar carrying the six worklists, the register, the schedule and
the claims; a working area that is a grid of cards; and a chart that reads top to bottom as
demographics, then conditions, then medications and allergies, then orders and results, then
encounters. Every card in the worklist board carries its list's name, its depth and the age of its
oldest item, and a list with nothing in it says so rather than rendering an empty card. Every row
that can be acted on is acted on in the row: a note is written in the row, an order line is added in
the row, and an outcome is recorded in the row.

**The signing confirmation.** The one moment in the product that earns a route of its own. It states
the encounter number, the locked note version, the number of orders released and the queued claim
number, each as its own labelled line, and it offers exactly two onward actions: back to the chart,
and on to the next unsigned note.

**The forms.** Every form control carries a persistent visible label above it, errors are associated
with their field and are stated in text beside it, success is announced, and nothing a person typed
is cleared when a submission fails.

## Constraints

- One clinic, one record, one site. No second tenant, no multi-facility routing and no cross-clinic
  record sharing.
- No inpatient surface: no beds, no theatre lists, no ward rounds and no discharge summaries.
- No wire message interface: nothing here parses or emits a positional clinical message format, and
  no laboratory, hospital or clearing house connects to this app directly.
- No population export, no third-party application authorization, no de-identified research extract,
  no decision-support rule engine and no quality-measure reporting.
- No payments, no invoicing to a card, no plans and no cart. Money here is what an insurer paid and
  what a patient owes, never a transaction this app performs.
- No email, no SMS and no push. Every acknowledgement is on the screen.
- No file upload and no object storage. Nothing in this product stores an image, a document or an
  attachment.
- No third-party analytics, tag manager, bot-defence service, font service or video host. Nothing on
  any route calls out to another service at runtime.
- No site search, no comments, no likes, no messaging and no public profiles.
- One language, English, and one currency, `usd`.
- No native app and no offline mode.
- The app stays responsive with the seeded record plus a few thousand patients, a few thousand
  encounters and their claims.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
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

**API shapes.** Field names are exact. A list endpoint returns a top-level JSON array. A successful
call returns the named resource or shape; an invalid or unauthorized call is rejected as a client
error, never as a server error and never as a silent success, and carries a message naming the
reason.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | - | `status` |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `email`, `role` |
| `GET /api/site/release` | - | `version`, `released_on`, `notes_url`, `artifacts` each with `channel`, `label`, `href`, `sha256`, `sha512` |
| `GET /api/site/articles` | - | `slug`, `title`, `headline`, `excerpt`, `published_at`, `reading_minutes` |
| `GET /api/site/modules` | `category` | `slug`, `name`, `vendor`, `categories`, `min_core_version`, `licence`, `source_url`, `sends_data_outside`, `last_verified_on` |
| `GET /api/site/page-views` | - | `path`, `referrer`, `status`, `viewed_at` |
| `GET /api/patients` | `family`, `birth_date` | `patients` the caller may open, and `total` over that same set |
| `GET /api/patients/{mrn}` | - | `mrn`, `family_name`, `given_name`, `birth_date`, `birth_date_precision`, and `moved_to` when the identity was merged |
| `POST /api/patients` | `family_name`, `given_name`, `birth_date`, `birth_date_precision`, `address_line`, `postal_code`, `telephone`, `identifiers` | `mrn`, and `possible_match` when one exists |
| `POST /api/patients/{mrn}/break-glass` | `reason` | `expires_at` |
| `GET /api/patients/{mrn}/conditions` | `as_known_at` | `conditions` with all four code fields, `sensitivity`, `effective_time`, `recorded_time`, and `total` over the visible set |
| `GET /api/patients/{mrn}/allergies` | - | `assertion`, and `entries` when the assertion is `allergy` |
| `GET /api/appointments/availability` | `provider`, `date` | the free `slots` for that provider on that date |
| `POST /api/appointments` | `mrn`, `provider`, `room`, `starts_at` | `number`, `starts_at`, `status` |
| `POST /api/appointments/{number}/cancel` | - | `number`, `status` |
| `POST /api/appointments/{number}/reschedule` | `starts_at` | `number`, `starts_at`, `status` |
| `POST /api/encounters` | `mrn`, `class` | `number`, `status` |
| `GET /api/encounters/{number}` | - | `number`, `status`, `patient_mrn`, and `note` only for a reader entitled to it |
| `PATCH /api/encounters/{number}/note` | `body`, `version_id` | the stored note and its `version_id`, or the current version on a refusal |
| `POST /api/encounters/{number}/conditions` | `code_system`, `code`, `code_display`, `code_version`, `effective_time` | the stored condition |
| `POST /api/encounters/{number}/orders` | `code_system`, `code`, `code_display`, `code_version`, `intent`, `priority` | `number`, `status` |
| `POST /api/encounters/{number}/sign` | - | `encounter_number`, `note_version_id`, `rendering_hash`, `orders_released`, `claim_number` |
| `GET /api/encounters/{number}/rendering` | - | `rendered_text`, `rendering_hash`, `signed_at` |
| `POST /api/encounters/{number}/addendum` | `body`, `reason` | the stored addendum |
| `POST /api/encounters/{number}/amendment` | `body`, `reason` | the new note version |
| `GET /api/observations/{id}/history` | - | every version, newest first, each with `version_id`, `value_number`, `recorded_time`, `supersedes`, `reason` |
| `POST /api/conditions/{id}/retract` | `reason` | the condition at status `entered_in_error`, with no row removed |
| `GET /api/orders` | `status` | `number`, `status`, `code`, `encounter_number` |
| `POST /api/results` | `placer_number`, `control_id`, `code_system`, `code`, `code_display`, `code_version`, `value_number`, `comparator`, `unit_code`, `reference_low`, `reference_high`, `abnormal_flag`, `effective_time` | the stored observation, or the first outcome on a repeat |
| `GET /api/results/unmatched` | - | `control_id`, `stated_mrn`, `received_at`, `state` |
| `POST /api/prescriptions` | `mrn`, `code_system`, `code`, `code_display`, `code_version`, `dose_quantity`, `dose_unit`, `dose_route`, `frequency_per_day`, `duration_days`, `dispense_quantity`, `dispense_unit`, `refills_authorised` | `number`, `patient_instruction`, and `conflict` with its `severity` when one exists |
| `POST /api/eligibility` | `mrn`, `coverage_id` | `number`, `checked_at`, `active`, `coverage_level` |
| `GET /api/claims` | `status` | `number`, `status`, `total_charge_minor`, `currency`, `patient_mrn` |
| `GET /api/claims/{number}` | - | the claim, its ordered `diagnoses`, its `lines` with their `diagnosis_pointers`, and `patient_balance_minor` |
| `POST /api/claims/{number}/submit` | - | `number`, `status` |
| `POST /api/claims/{number}/lines` | `code_system`, `code`, `code_display`, `unit_qualifier`, `units`, `charge_minor`, `diagnosis_pointers` | the stored line, or a refusal when a pointer names no position |
| `GET /api/claims/{number}/ledger` | - | the `entries` and their `sum_minor` |
| `POST /api/remittances` | `claim_number`, `lines` each with `claim_line_number`, `paid_minor` and `adjustments` | `number`, `state`, and `quarantine_reason` when it did not balance |
| `POST /api/allocations` | `amount_minor`, `shares` | the ordered `shares`, each with its own `amount_minor`, summing to the whole |
| `GET /api/worklists` | - | `key`, `owner_role`, `depth`, `oldest_age_hours` |
| `POST /api/worklists/{key}/items/{id}/close` | `outcome` | the closed item with its `outcome` and `outcome_by` |
| `GET /api/portal/record` | - | the calling patient's own record |
| `GET /api/portal/access-log` | - | `actor_email`, `action`, `outcome`, `occurred_at`, newest first |
| `POST /api/portal/amendment-requests` | `statement`, `about` | the stored request |
| `POST /api/portal/appointment-requests` | `preferred_date`, `note` | the stored request |
| `POST /api/portal/demographic-proposals` | `field`, `proposed_value` | the stored proposal |

Bearer auth is required on everything except `GET /api/health`, `POST /api/auth/login` and the
`GET /api/site/*` read endpoints other than `GET /api/site/page-views`.

**No mocks.** PostgreSQL is the only place a record of any kind exists. An in-memory list of
patients, a JSON file of seed data read at request time, a computed answer the app returns to itself
without a stored row behind it, a claim total held in a variable rather than summed from stored
lines, or an audit entry written to a log file instead of a table are all the same failure wearing
different clothes. The named provider is the fact - the app's UI and its own tables can only reflect
what lives in the provider, never substitute for it.

## Definition of done

A clinician signs in, opens an encounter, writes its note, codes its diagnosis, places its order and
signs, and lands on a confirmation naming the locked note version, the orders released and the claim
queued. That signed note re-renders to the same stored hash a day later, whatever has happened to
the patient's medication list since. A clinician with no relationship to a patient cannot tell that
patient's record from one that was never issued, and the patient can see every read of their own
record. A remittance that is one minor unit out posts nothing at all.
