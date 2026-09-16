# Proofworks Academy

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, sign in as
`learner@example.com`, enrol in a course against a partner program's budget, finish a module,
sit a timed exam, submit a project, have `reviewer@example.com` approve it and
`registrar@example.com` issue the credential, then read that credential back from the public
verification address while signed out, without hitting an error page. A different stranger must
NOT be able to move a project out of review, issue a credential, or read another learner's
work, by any means. The credential must exist as one append-only row in the public ledger with
the exact reference this brief defines; a badge the app draws for itself does not count.

## Overview

Proofworks Academy certifies developer skill. Workforce and education teams buy places on it
for the people they are training; learners, addressed throughout as `Artisan`, work through it
and come out with a credential an employer can check without asking anybody's permission.

Four businesses sit on one identity and one progress ledger. A consumer academy of chains,
courses, modules, lessons and pages. A credentialing authority of timed tests, projects,
credentials and revocations. Partner programs with their own treasuries, which fund seats for
named cohorts. And a bounty board that only credential holders can reach.

The hard part is that the credential is the product, and three parties want it to be wrong:
the learner who wants it without the work, the partner who wants seats without paying for
them, and the employer who stops trusting every credential the moment one turns out to be
unearned. So issuance is the last thing that happens, it is countersigned by a role the
learner does not hold, and what it writes cannot be edited afterwards.

Three personas use the platform and there is no fourth: the Artisan who learns, the reviewer
who judges the work, and the registrar who signs the credential and owns the budget that paid
for it.

Not built: course authoring, card payments, a chat community, outbound email, video hosting,
a wallet or a token swap, and any execution of learner-supplied code.

## User roles

Three roles. Every seeded account uses the password `deku-demo-pw-2026`.

| Role | Can read | Can write |
|---|---|---|
| `learner` | own enrolments, own progress, own assessments, own projects, own credentials and rewards; published course metadata; free pages everywhere; paid pages only where entitled | own progress; own consents; own exam answers; own project submission |
| `reviewer` | everything a learner can, plus projects and proctor event counts for learners funded by the reviewer's own program | approve a project, request changes on it, clear a `Suspicious` exam. **Cannot issue or revoke a credential, cannot create a program, cannot move a treasury, and cannot read or touch a project belonging to another program.** |
| `registrar` | everything, including every program roster and treasury | issue and revoke credentials, create programs, invite seats, fund treasuries, publish announcements. **Cannot approve a project, and cannot be the reviewer of record on one.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI
is not authorization: a direct API call from a `learner` session to any `registrar`-only
endpoint must be rejected by the server (an unauthorized request is denied, not served),
leaving the protected state unchanged.

Signup is closed. Accounts exist only because they were seeded or invited into a program, and
there is no public registration form. Seeded accounts: `learner@example.com` (`Ada Okonkwo`,
`learner`, in `Northgate Cohort 2026`), `learner2@example.com` (`Bruno Salas`, `learner`, in
`Halcyon Cohort 2026`), `learner3@example.com` (`Cleo Marsh`, `learner`, in no program),
`reviewer@example.com` (`Dara Feng`, `reviewer`, attached to `Northgate Cohort 2026`) and
`registrar@example.com` (`Elin Vasquez`, `registrar`).

A learner's program scopes what they see; it never adds what they can do. A row carrying no
`program_id` is public and visible to everybody. A row carrying one is visible only to accounts
whose `program_id` matches it. `learner3@example.com` carries none, and must still see every
public course.

## Core features

### Auth

Sign-in exchanges an email and password for a bearer token returned as `access_token`, which
the client sends as
`Authorization: Bearer <token>` on every call except `GET /api/health`,
`POST /api/auth/login`, `GET /api/catalogue` and `GET /api/credentials/proof/{ledger_ref}`.
The role and the program on the token's account are read from the account row on the server;
a `role` or `program_id` field in a request body is ignored, always. A disabled account is
refused on every request and not only at sign-in, so revoking access does not wait for a token
to expire.

### The catalogue and the reader

1. Content is five levels: chain, course, module, lesson, page. Every page is addressable at
   `/content/{course_id}/{module_id}/{lesson_id}/{page_id}` and carries its position as
   `page_current`, `page_total`, `lesson_current` and `lesson_total`.
2. Marking a page complete records one `page_progress` row for that account and page, and
   `enrolment.course_progress` is recomputed in the same write. Marking the same page complete
   twice creates no second row and does not move the percentage a second time.
3. A page whose status is already `complete` never returns to `in_progress`. A late write
   carrying the earlier status is refused as invalid and the stored status does not change.
4. A module flips to complete when every page under it is complete, and only then.
5. `intro-javascript` is deprecated. It stays readable to anybody already enrolled and holding
   a credential against it, and it never appears in the enrolable catalogue.

### Entitlement, the paywall and the program restriction

1. A module whose `order` is at or past its course's `first_paywalled_module` requires
   entitlement. `first_paywalled_module` null means the whole course is free; `0` means the
   whole course is paid. Null and `0` are different values and behave differently.
2. `restricted_to_program` is a separate gate that stacks with the paywall. A course can be
   free and restricted at once: `solidity-intermediate` is free and restricted to
   `Halcyon Cohort 2026`, so `learner@example.com` cannot read it and `learner2@example.com`
   can.
3. Entitlement is: the module is free, or the enrolment is `unlocked`; and the course is not
   restricted, or the account is in the program it is restricted to; and the course is
   published.
4. An unentitled request for a paid page body is denied and returns no body text at all. The
   course and module titles stay visible, because the catalogue is public.

### Enrolment against a partner treasury

1. Enrolling in a free unrestricted course succeeds for any learner and sets
   `entitlement_source` to `free`.
2. Enrolling in a paid course requires a partner program with enough treasury. The enrolment
   reserves `course.price_minor` from `partner_program.treasury_remaining` and increments
   `seats_granted`, and it sets `entitlement_source` to `program`.
3. `Northgate Cohort 2026` holds `10000` minor units and `solana-intern` costs `10000`, so one
   funded seat remains. **Two simultaneous enrolments in `solana-intern` against
   `Northgate Cohort 2026` must not both succeed: exactly one wins, the other is refused with
   a reason naming the exhausted treasury, `treasury_remaining` never goes below zero, and no
   half-written enrolment is left behind.** This must hold under real concurrency.
4. A learner already enrolled in a course who enrols again reactivates the same enrolment row.
   There is never a second row for one account and one course.
5. Every enrolment records `program_id` at the moment it happened. The program a learner is in
   today and the program that funded an enrolment are separate facts and are never read
   interchangeably.
6. The single-course-in-flight rule is advisory. A learner with an unfinished course is warned
   with the exact text `We recommend finishing the course you have already started so you can
   get rewarded.` and may continue anyway.

### The assessment state machine

This is the critical path end-to-end, and every edge case below it is one the product must
survive rather than one it may treat as unlikely.

1. `assessment.status` takes exactly `PreAssessment`, `Exam`, `ExamReview`, `Project`,
   `ProjectReview` and `Completed`, with that casing, and it is set only by the server.
2. An assessment is created in `PreAssessment` when a module's curriculum reaches complete and
   the learner is entitled to the module.
3. `PreAssessment` advances to `Exam` only when `accepted_terms`, `accepted_camera_monitor`
   and `verified_identity` are all true on the assessment. A start request with any of them
   false is refused as invalid, and the status does not change.
4. `Exam` advances to `ExamReview` on a learner submit, or when the server observes
   `exam.ends_at` has passed. A learner who never submits still reaches `ExamReview`.
5. `ExamReview` advances to `Project` when the result is at or above `70` and no blocking
   proctor signal was recorded, setting `exam.status` to `Passed`.
6. `ExamReview` returns to `PreAssessment` when the result is below `70`, setting `exam.status`
   to `Failed`, and a retake of the same module is refused for the next `300` seconds.
7. `ExamReview` stays where it is when proctor signals exceed the threshold, setting
   `exam.status` to `Suspicious`. It moves only when a reviewer clears it, and the clearing
   writes an audit entry naming the reviewer.
8. `Project` advances to `ProjectReview` on submission, and straight to `Completed` when the
   module carries `disable_project` true.
9. `ProjectReview` advances to `Completed` on approval, or back to `Project` on a request for
   changes, which increments `project.revision_count`.
10. Asking for a transition the table does not allow is refused as invalid and changes nothing.
    Opening the exam route while the status is not `Exam` sends the learner back to the gate.

### The proctored exam

1. `exam.ends_at` is set by the server when the exam starts, at `1800` seconds after
   `started_at`. A client-supplied end time is ignored. When the two disagree the server wins,
   and `exam.timeout_source` records `Browser` or `Server` accordingly.
2. Questions are served with their `prompt`, their `kind` of `MultipleChoice` or
   `MultipleChoiceCode`, and their options. `answer_key` appears in no learner-facing response
   at any point, including after the exam ends.
3. Proctor events are recorded with `kind` from `AnswerSubmitted`, `OffFocus`, `OnFocus`,
   `NoFaceDetected`, `MultipleFaceDetected`, `FaceResolved`, `TestStarted`, `TestResumed` and
   `TestSubmitted`, each with an `occurred_at`. Inference happens in the browser; only these
   events reach the server and no image ever does.
4. Three or more events of kind `NoFaceDetected` or `MultipleFaceDetected` in one attempt make
   the exam `Suspicious`. A proctor signal never fails an exam by itself, because a signal a
   learner's own machine produced is evidence for a person to weigh and not a verdict.
5. Camera unavailable is not silently the same as camera watching. The learner is told which
   mode they are in before starting, `exam.proctoring_mode` records `full`, `degraded` or
   `none`, and a credential issued from a `none` attempt carries that fact.
6. Withdrawing camera consent during an exam ends the attempt at once, voids it, and offers a
   retake. A voided attempt consumes no retake allowance.

### Project review

1. A project submission carries a `repo_url` and a `demo_url`. A submission missing either is
   refused as invalid and no project row is written.
2. A project belongs to the review board of the program that funded its enrolment. A reviewer
   attached to another program is denied both reading and approving it.
3. **A reviewer must not be the learner. An approval request whose caller is the project's own
   learner is denied, and `project.status` still reads `InReview` afterwards.** This is the
   rule the whole product rests on, so it is checked on the server on every approval, never in
   the interface.
4. `project.status` takes exactly `InProgress`, `InReview` and `Approved`.
5. Approving writes `approved_by`, `approved_at` and an audit entry. Requesting changes returns
   the project to `InProgress` and increments `revision_count`.

### The credential and the public ledger

1. Only a `registrar` issues. An issue request from a `learner` or a `reviewer` is denied and
   the credential is not created.
2. Issuance requires the assessment in `Completed`. Issuing against any other status is
   refused as invalid.
3. Issuance appends exactly one `ledger_entry`. `ledger_ref` is the lowercase SHA-256 hex of
   the string `{credential_id}|{account_id}|{course_id}|{module_id}|{issued_at}`, where
   `issued_at` is an ISO 8601 UTC instant with second precision, for example
   `2026-09-16T07:46:01Z`.
4. **Issuing the same credential twice writes no second ledger entry and returns the original
   `ledger_ref`.** Two simultaneous issue requests for one completed assessment produce exactly
   one credential and exactly one ledger entry.
5. `GET /api/credentials/proof/{ledger_ref}` needs no credential and answers with the holder's
   display name, the course and module titles, `issued_at`, `proctoring_mode` and `status`. An
   unknown reference is reported as not found rather than as an error.
6. Revoking is a `registrar` action. It writes `credential.status` `revoked` with a
   `revoked_reason`, and it appends a second ledger entry of kind `revocation`. **It never
   edits or deletes the issuance entry.** Verification afterwards still resolves and reports
   `revoked`.
7. A refund or a deprecated course never revokes a credential. The learner did the work.

### Rewards and the thirty-day window

1. `reward.kind` takes `nft`, `coupon`, `token` and `fiat`, and `reward_earn.status` takes
   `in_progress`, `redeemed` and `expired`.
2. `enrolment.reward_window_ends_at` is computed once, at enrolment, as thirty days later. The
   learner is told the absolute date, never only a number of days left. The exact text
   `Your 30-day countdown timer for completing and claiming any bonus rewards will begin as
   soon as you purchase the course.` appears on the course overview.
3. The window gates bonus rewards only. Course completion, the credential and the recorded
   skills are never time limited.
4. Expiry is inclusive to the end of the thirtieth day in UTC. A claim landing in the same
   second as expiry is resolved in the learner's favour.
5. Extending a window is a `registrar` action only, is bounded to one further thirty day
   period, and writes an audit entry naming who extended it and why. Nobody else can move the
   date, because an unaudited extension is a treasury leak.
6. `reward.quota_total` is never oversold. Two simultaneous claims of the last unit of a reward
   produce exactly one `reward_earn`, and the other is refused with a reason.
7. A reward balance and a treasury balance are different kinds of money and are never added
   together or converted into one another.

### Bounties

1. A bounty carries `status` from `open`, `work_started`, `submissions`, `concluded`,
   `expired` and `canceled`. A learner's own relationship to it carries `status` from `viewed`,
   `bookmarked`, `applied`, `accepted`, `rejected`, `work_started`, `submitted` and `canceled`.
2. The two are separate. A learner sitting at `work_started` on a bounty that has moved to
   `canceled` sees both states named and an explanation, never one silently standing in for
   the other.
3. A bounty gated on a credential is not applicable to an account that holds none: the
   application is denied and no application row is written.

### Consent, retention and erasure

1. Each consent is a separate, informed opt-in, never bundled into one control and never
   pre-ticked, and it is irreversible in effect for the attempt it governs: withdrawing it
   later ends the attempt rather than rewriting what was already recorded. Two consents are
   versioned and recorded separately. `accepted_terms` carries
   `terms_version`; `accepted_camera_monitor` carries `camera_consent_at`. A plain-language
   disclosure appears before the camera activates, naming what is detected, what leaves the
   machine and what does not.
2. Face detection runs on the learner's own machine. No image, no frame and no video ever
   reaches the server, and biometric signals are never used to train or tune any model.
3. Proctor events are kept for `90` days from the attempt, or thirty days after the review of
   that attempt concludes, whichever is sooner, and are then removed. The retention
   schedule is stated on the privacy page beside every other kind of record: an audit entry is
   kept for seven years, a ledger entry is permanent, and a project submission is kept for
   twenty four months after the last activity on it.
4. A learner may ask for erasure at `POST /api/erasure-requests`. The request is recorded
   with the moment it arrived and a thirty day grace period in which the learner can cancel
   it. On execution, personal fields on
   the account are cleared, `deleted_at` is set, and the account row survives as a tombstone so
   the ledger's references stay resolvable. **The credential in the ledger is the documented
   exception: it is permanent, it is not erased, and the learner is told so at consent time and
   again at the moment of deletion.**
5. A partner cannot export a roster's contact details. `GET /api/programs/{program_id}/roster`
   returns completion state and never an email address, because a partner buys places on a
   course and not a list of people.

### The audit trail

1. Every issuance, revocation, approval, change request, suspicious clearance, treasury
   movement and erasure execution appends an `audit_entry` naming the actor, the action, the
   subject and the reason. The table is append only: no update, no delete.
2. Each entry carries `prev_hash` and `entry_hash`, so the chain can be read end to end and a
   removed or edited entry is visible as a break in it. `GET /api/audit` is a `registrar`
   surface and returns the chain in recorded order.
3. The audit trail and the learner's own activity feed are different things and live in
   different tables. The activity feed is a product feature a learner reads; the audit trail is
   evidence and nothing in the product may rewrite it.

### Money, quota and rate

1. Pricing resolution happens on the server and never from the request. Where a program
   carries a `discount_percent`, it applies to the course price once. A program specific price and a
   program discount never compound: the more specific value wins outright.
2. `partner_program.treasury_total` minus `treasury_remaining` always equals the sum of the
   funded enrolments drawn against that program. A reconciliation read that disagrees is a
   defect in the write path, not a rounding difference.
3. Reward points are an internal balance. They are never presented as redeemable for cash and
   never added to or converted into a treasury amount, because the two are different kinds of
   money.
4. Mutating requests are rate limited per account, and a refused request says when to retry.
   The response carries `RateLimit-Limit`, `RateLimit-Remaining` and `RateLimit-Reset`, and a
   refusal carries `Retry-After`.
5. A mutating request may carry an `Idempotency-Key` header. Replaying a request with a key
   already seen returns the first response and performs the action once. This is what makes a
   retried enrolment or a retried issuance safe.

### The public product surface

1. A privacy page at `/privacy`, linked from the footer of every page, states what Proofworks
   records about an Artisan, how long each kind of record is kept, and that a credential once
   written to the ledger is permanent and cannot be erased.
2. A first-time visitor is asked once about non-essential cookies. The answer is remembered and
   survives a reload, and the question is not asked again.
3. Every page view is recorded with its route and the moment it happened, and a `registrar` can
   read the counts per route.
4. Every form rejects invalid input in place, names the field at fault, and writes nothing.
5. An unknown address renders the product's own not-found page, which offers a way back into
   the catalogue and answers as not found rather than as an error. A page address that is
   correct but whose page does not exist renders the reader's own not-found page inside the
   module, so the Artisan keeps their place in the lesson rail.
6. Every internal link on every public route resolves.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | public catalogue of chains and courses | none |
| `/proof/<ledger_ref>` | public credential verification | none |
| `/privacy` | the privacy page | none |
| `/login` | sign in | none |
| `/home` | the Artisan dashboard | all |
| `/courses/<chain_id>` | one chain's courses | all |
| `/content/<course_id>` | course overview, enrol, reward window | all |
| `/content/<course_id>/<module_id>/<lesson_id>/<page_id>` | the reader | all |
| `/content/<course_id>/<module_id>/assessment` | the gate and the three consents | all |
| `/content/<course_id>/<module_id>/assessment/exam` | the timed exam | all |
| `/content/<course_id>/<module_id>/assessment/project` | project submission | all |
| `/credentials` | the learner's own credentials | all |
| `/bounties` | the bounty board | all |
| `/review` | the review board, by state | reviewer, registrar |
| `/review/<project_id>` | one project under review | reviewer, registrar |
| `/registrar` | the issuance board | registrar |
| `/programs` | programs, rosters and treasuries | registrar |
| `/programs/new` | step one, name the program and its treasury | registrar |
| `/programs/new/seats` | step two, the seats | registrar |
| `/programs/new/review` | step three, confirm and create | registrar |

**Entry and redirects.** A signed-out request for a signed-in route goes to `/login` and then
on to the route that was asked for; with no destination it lands on `/home`. Sign-out returns
to `/`. A token that expires mid-action keeps the typed values and asks for a sign-in again,
then completes the action. A `learner` reaching `/review`, `/registrar` or `/programs` is
refused and nothing changes. Reaching the exam route while the assessment is not in `Exam`
returns to the gate rather than rendering.

**Journeys.**

1. Sign in as `learner@example.com`, open `/courses/solana`, open `/content/solana-intern`,
   enrol against `Northgate Cohort 2026`, and see the funded seat counted and the reward
   window's absolute date.
2. Read through module `solana-intern-basics`, mark its last page complete, watch the module
   turn complete and the assessment gate open at `PreAssessment`.
3. Accept terms, accept camera monitoring, verify identity, start the exam, answer three
   questions, submit, and land in `ExamReview` with a result.
4. Submit a project with a `repo_url` and a `demo_url`, watch it appear on `/review` for
   `reviewer@example.com`, have it approved, and reach `Completed`.
5. Sign in as `registrar@example.com`, open `/registrar`, issue the credential, then open
   `/proof/<ledger_ref>` signed out and read it back.
6. Sign in as `learner2@example.com` and ask for `learner@example.com`'s project directly: the
   request is refused and the project does not move.

**States.** Every list has an empty state that names what to do next, and every route has a
loading state. A refused action reverts its optimistic row in place and states the reason
beside it. Errors never take over the page.

## UI/UX notes

The direction comes from the supplied specification rather than from a house style: an ornate,
gold-on-dark arcane manuscript wrapped around a working console. North star: an Artisan always
knows where they are in a long course, and a reviewer can clear a queue without reading
anything twice. The register is operational, so the boards and the reader read quiet and are
built for scanning and repeated action, and the atmosphere is confined to the ornamental frame
and the chain badges. The product commits to dark; a light mode is optional and never implied
to be graded.

Colour by role. The ground is a deep cool neutral, and three further deep cool neutral steps
carry the menu, the raised panel and the premium panel, so surfaces separate by luminance
rather than by an outline. Primary text is a near-white muted amber and is the only thing on a
page wearing it. The muted border is a mid warm neutral and is decorative only: it never
carries text. A light vivid green means done, a light soft red means refused, a light soft
amber means in progress, and a mid vivid cyan means a person is still looking at it. Chain
badges carry one accent each, drawn from a light vivid cyan, a light vivid blue, a light vivid
violet, a mid vivid violet and a deep soft violet, and those accents appear nowhere else. The
public catalogue alone carries a mid vivid green signal colour. Exact shades are yours, so long
as they hold the roles and the exclusivities above.

Type is two voices and one identity. Display is `Alexon` with the fallback stack
`"Trajan Pro", Optima, Palatino, Georgia, serif`; body is `CircularXX` with the fallback
`ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial,
sans-serif`; code is `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
"Liberation Mono", "Courier New", monospace`. The scale is `10px`, `12px`, `14px`, `16px`,
`20px`, `24px` and `40px`, and code never renders below `14px`, because this product puts code
on almost every page and inside exam options. Figures align in columns wherever treasury
amounts or scores stack.

Shape and density. The ornamental frame is one component with variants, not fifteen bespoke
rules: variants card, module, module-title, video-preview, circular, toast and offer; tones
gold, dark and double; states default, selected, locked and failed. It is drawn rather than
shipped as a file, and where it is clipped to a non-rectangular outline the focus ring renders
outside the clip so it is never cut. Density is comfortable in the reader and compact on the
boards, so a full review queue fits one screen.

Motion is eased and restrained. Every transition carries state feedback and nothing else:
transform and opacity animate, every reveal has a static end state reachable at once, and the
reader carries no entrance animation because somebody working through a long course does not
want one on each page. Under a reduced-motion preference the whole interface stays functional
and still.

Components are specified by behaviour. A control carries resting, pointed-at, pressed, focused
and unavailable states, an input shows its label and its error in a fixed place, Escape closes
a layer and returns focus to its trigger, and a destructive action confirms first.
Unavailability is never signalled by colour alone.

Accessibility is contract, not taste. Body text and its background meet the WCAG AA contrast
bar, and large text and interface boundaries meet the three-to-one bar; the muted border fails
the body bar, which is exactly why it carries no text anywhere in this product. Every command
has a keyboard route with a visible focus ring, icon-only controls carry labels, and no
information is carried by colour alone.

Responsive behaviour holds at every width between the phone, tablet and desktop tiers, and it
is checked at all three breakpoints rather than only at the widest. At the narrowest viewport
nothing overflows sideways, every navigation target stays reachable, and no route is more than
twice as tall as its desktop arrangement. Every route stays usable at four hundred percent zoom
and at three hundred and twenty pixels of effective width with no loss of content or function.

A progress save, an answer save and an issuance outcome are announced politely rather than
silently, because an Artisan who cannot see the screen still needs to know their work was kept.
Where the product shows a video it carries captions and a transcript and never plays on its own
with sound.

## Constraints

One academy. A learner never reads another learner's rows, and a reviewer never reads a
project funded by a program they are not attached to. No card payments, no invoices and no
refunds: money moves only as a partner treasury balance in integer minor units of `usd`. No
external network call is made at run time beyond the two backing services.

Not built and not to be added: course authoring or a content management system; any identity
provider other than the one named here, and no federated sign-in, directory provisioning or
second factor; a chat community, role mirroring, notifications or any outbound email; video
hosting, transcoding or a player integration; an assistant, a model vendor or any execution of
learner-supplied code; a skills-taxonomy vendor; an affiliate network; a hosted analytics or
tracing vendor; an avatar pipeline; a wallet, an exchange or a token swap; stored camera
frames or identity documents; a background job queue, a cache or a search index; a marketing
site or a blog; a native mobile application.

The app stays responsive at `4000` content pages across `8` modules, `500` enrolments,
`2000` proctor events on one attempt, and `1000` ledger entries.

## Technical requirements

Stack: Node 20 with `Express` serving a JSON API on the same origin under `/api`, and a
`Svelte + Vite` single-page front end compiled to a production bundle and served from that same
origin. The browser receives the application shell on first paint and every record arrives from
the API afterwards. Storage is PostgreSQL. Authentication is Keycloak.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
services available in this environment are PostgreSQL and Keycloak, and reaching for anything
else is a contract violation.

Read every connection detail from the environment and never hardcode a host or a port.
PostgreSQL is at `DATABASE_URL`. Keycloak is at `AUTH_URL`, with realm `deku` and client
`proofworks` already configured and every seeded account already present in it. The app's own
address is `APP_PUBLIC_URL` and its outside port is `APP_PUBLIC_PORT`. Both backing services
are already running and must not be downloaded, installed, compiled or started.

`POST /api/auth/login` exchanges an email and password for a bearer token by asking Keycloak,
and returns it as `access_token` beside the caller's `account_id` and `role`. The role and the program are
read from the application's own `account` row on every request; a `role` or `program_id` in a
request body is ignored. `GET /api/health` returns `200` with no credential once the app has
connected to PostgreSQL, reached Keycloak and finished seeding.

Application logs go to standard output, one line per request carrying the method, the path, the
outcome and the elapsed milliseconds, and never a password, a token, an email address or an
answer key. That log is the whole of the observability surface: there is no trace pipeline and
no metrics exporter.

No route's transferred script exceeds `250` kilobytes gzipped. Nothing that runs on the
server is reachable from a browser bundle, and no database client, schema definition or field
enumeration ever ships to one.

Performance and availability are product properties here, not operations concerns. The
catalogue, the reader and the two boards answer under a second of work at the seeded volumes
above. When the database is briefly unreachable the app stays up, says so in a banner, and
serves what it can read rather than turning every route into an error page.

Security rests on one rule and one place. Every authorization decision is made on the server
from the account row, in one policy path that every endpoint goes through, rather than in
scattered checks at each handler. The threat this defends against is the one that matters most
here: an account that holds a lower role reaching an endpoint that belongs to a higher one, or
one program's learner reaching another program's rows. Compliance and data governance are
carried in the product itself, as the consent, retention, erasure and audit rules above, rather
than as a document somebody keeps separately.

Three trust zones scope every request. A public edge anybody reaches, which is `/`,
`/privacy`, `/proof/{ledger_ref}`, `GET /api/catalogue` and
`GET /api/credentials/proof/{ledger_ref}`; an account surface behind a bearer token, which is
everything else; and an issuance surface inside that, reachable only by a `registrar`. The
boundary that matters is the last one, because it reads and writes the same tables the account
surface does.

No credential, key or token appears in anything the browser downloads. The answer key for a
test question is served to nobody: it exists only in the column and in the grading path.

Every public route carries its own title and its own meta description, and no two public routes
share either. The site serves a favicon and declares it in the document head.

Paging on `GET /api/catalogue`, `GET /api/projects` and `GET /api/credentials` is by opaque
cursor, never an offset, at most `25` items a page, with the cursor returned in the
`X-Next-Cursor` response header and absent on the last page. Offset paging is forbidden on
every collection, because a list that grows between two pages silently skips rows.

Caching is `private, no-store` on anything specific to one account, and the public catalogue
and the public verification response are cacheable for `60` seconds with their freshness stated
in the body. Anything addressed by `ledger_ref` is immutable and may be cached indefinitely.

Rate limiting is per account: `600` mutating requests a minute sustained with a burst of
`100`. Every response carries `RateLimit-Limit`, `RateLimit-Remaining` and `RateLimit-Reset`,
and a refused request carries `Retry-After` and a body that explains when to retry.

Validation rejects a malformed body before anything is written, names the field at fault in the
response, and leaves no partial row behind. A request carrying an unknown field is refused
rather than silently ignored, because a silently ignored field is a rule nobody notices is
missing.

A failed enrolment leaves no partial state: no orphaned enrolment row, no treasury reserved
against nothing, and no seat counted for a learner who is not enrolled. A failed issuance
leaves no credential without a ledger entry and no ledger entry without a credential.

## Data model

Twenty-six tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
not a secret. Hash it as normal; the exact literal must work at login, and it must be written
into `/app/USER_README.md` alongside each account so a grader can sign in.

`account`: `id`, `email`, `display_name`, `username`, `country`, `proficiency`, `role`,
`program_id`, `status`, `email_verified_at`, `last_seen_at`, `deleted_at`, `created_at`.
`email` and `username` are unique, and `username` is checked against the same reserved segment
denylist the partner slug uses, so a public handle can never shadow a route. `country` is an
ISO 3166-1 alpha-2 code. `proficiency` is `beginner`, `intermediate` or `advanced`. `role` is
`learner`, `reviewer` or `registrar`. `status` is `enabled` or `disabled`, and a `disabled`
account is refused on every request rather than only at sign-in. `program_id` is nullable and
null means the public tenant. `deleted_at` is the erasure tombstone: the row survives with its
personal fields cleared so the ledger's references stay resolvable.

`partner`: `id`, `name`, `slug`, `email_domain`, `created_at`. `slug` is unique and is checked
against the reserved route segments at creation, so a partner can never take `content`,
`review`, `registrar`, `programs`, `credentials`, `bounties`, `privacy`, `proof`, `login`,
`home` or `api`.

`partner_program`: `id`, `partner_id`, `name`, `starts_on`, `ends_on`, `treasury_total`,
`treasury_remaining`, `treasury_spent`, `seat_cap`, `seats_granted`, `discount_percent`,
`allow_assessments`, `status`, `created_at`. Money is integer minor units of `usd`.
`treasury_remaining` never goes below zero, and two simultaneous funded enrolments against the
last funded seat never both succeed. `status` is `active`, `suspended` or `terminated`, and a
suspended program stops new enrolments while leaving every enrolment it already funded intact.
A program is a time-bounded grant: after `ends_on` no new enrolment is funded, an assessment
already in flight runs to its end, and the entitlements the program bought stay valid.
`seats_granted` and `treasury_spent` move in the same operation as the enrolment that moved
them, and `treasury_total` minus `treasury_remaining` always equals `treasury_spent`.
`discount_percent` is an integer from `0` to `100` and never compounds with a program specific
price.

`program_invite`: `id`, `program_id`, `email`, `token_hash`, `status`, `expires_at`,
`created_at`. `status` is `Pending`, `Sent` or `Accepted`.

`chain`: `id`, `name`, `slug`, `category`, `accent`, `order`. `course`: `id`, `chain_id`,
`identifier`, `title`, `order`, `first_paywalled_module`, `restricted_to_program_id`,
`price_minor`, `is_published`, `is_deprecated`. `identifier` is unique.
`first_paywalled_module` is nullable, and null and `0` are distinct values.

`module`: `id`, `course_id`, `slug`, `title`, `order`, `project_type`, `disable_project`,
`estimated_hours`. `project_type` is `code` or `storyNode`. `lesson`: `id`, `module_id`,
`slug`, `title`, `order`. `page`: `id`, `lesson_id`, `slug`, `title`, `order`, `body_markdown`.

`enrolment`: `id`, `account_id`, `course_id`, `program_id`, `unlocked`, `entitlement_source`,
`course_progress`, `reward_window_ends_at`, `status`, `created_at`. Unique on
`(account_id, course_id)`. `entitlement_source` is `free` or `program`. `status` is
`in_progress` or `complete`. `course_progress` is an integer percentage written in the same
operation as the page progress that moved it.

`page_progress`: `id`, `account_id`, `page_id`, `status`, `completed_at`. Unique on
`(account_id, page_id)`. `status` is `in_progress` or `complete` and never regresses.

`assessment`: `id`, `account_id`, `module_id`, `status`, `accepted_terms`,
`accepted_camera_monitor`, `verified_identity`, `created_at`, `updated_at`. Unique on
`(account_id, module_id)`. `status` is `PreAssessment`, `Exam`, `ExamReview`, `Project`,
`ProjectReview` or `Completed`.

`exam`: `id`, `assessment_id`, `status`, `result_percent`, `started_at`, `ends_at`, `submitted_at`,
`timeout_source`, `proctoring_mode`, `attempt_number`, `question_seed`. `attempt_number` counts
the attempts on this module for this account, starting at `1`; an attempt voided by a platform
fault consumes none. `question_seed` fixes which questions are served and in what order, so a
retake is reproducible and two learners do not see the same order. `status` is `InProgress`, `Passed`,
`Suspicious` or `Failed`. `timeout_source` is `Browser` or `Server`. `proctoring_mode` is
`full`, `degraded` or `none`. `ends_at` is set by the server and is `1800` seconds after
`started_at`.

`exam_question`: `id`, `module_id`, `prompt`, `kind`, `options`, `answer_key`, `order`. `kind`
is `MultipleChoice` or `MultipleChoiceCode`. `answer_key` is derived into a score and is
returned by no endpoint.

`proctor_event`: `id`, `exam_id`, `kind`, `occurred_at`. `kind` is `AnswerSubmitted`,
`OffFocus`, `OnFocus`, `NoFaceDetected`, `MultipleFaceDetected`, `FaceResolved`, `TestStarted`,
`TestResumed` or `TestSubmitted`.

`project`: `id`, `assessment_id`, `account_id`, `program_id`, `repo_url`, `demo_url`, `status`,
`revision_count`, `approved_by`, `approved_at`, `created_at`. `status` is `InProgress`,
`InReview` or `Approved`. `approved_by` is never the project's own `account_id`.

`credential`: `id`, `account_id`, `course_id`, `module_id`, `module_ids`, `issued_by`,
`issued_at`, `status`, `proctoring_mode`, `revoked_reason`, `revoked_at`. `module_ids` is the
array of every module the credential attests, so a credential outlives a course that is later
deprecated and the modules it named stay resolvable. Unique on
`(account_id, course_id, module_id)`. `status` is `issued` or `revoked`.

`ledger_entry`: `id`, `credential_id`, `kind`, `ledger_ref`, `payload`, `recorded_at`. Append
only: no row is ever updated or deleted. `kind` is `issuance` or `revocation`. `ledger_ref` is
unique and is the lowercase SHA-256 hex of
`{credential_id}|{account_id}|{course_id}|{module_id}|{issued_at}`, for example
`4b2f8d1c0a97e3546b8f10d2c73a95e6018df4b7a3c295e621f08dc4a7b3e520`. There is exactly one
`issuance` entry per credential.

`reward`: `id`, `program_id`, `course_id`, `title`, `kind`, `quota_total`, `quota_claimed`.
`kind` is `nft`, `coupon`, `token` or `fiat`. `quota_claimed` never exceeds `quota_total`.
`reward_earn`: `id`, `reward_id`, `account_id`, `status`, `claimed_at`, `expires_at`. Unique on
`(reward_id, account_id)`. `status` is `in_progress`, `redeemed` or `expired`.

`bounty`: `id`, `program_id`, `title`, `kind`, `status`, `requires_credential`, `closes_at`.
`kind` is `job` or `levelUp`. `status` is `open`, `work_started`, `submissions`, `concluded`,
`expired` or `canceled`. `bounty_application`: `id`, `bounty_id`, `account_id`, `status`,
`created_at`. `status` is `viewed`, `bookmarked`, `applied`, `accepted`, `rejected`,
`work_started`, `submitted` or `canceled`.

`announcement`: `id`, `program_id`, `title`, `body`, `published_at`. A null `program_id` is
public. `page_view`: `id`, `route`, `account_id`, `viewed_at`. `audit_entry`: `id`, `actor_id`,
`action`, `subject_type`, `subject_id`, `reason`, `prev_hash`, `entry_hash`, `recorded_at`.
Append only, and the hash of each entry covers the previous one, so the chain reads end to end
and a removed entry shows as a break. `erasure_request`: `id`, `account_id`, `status`,
`requested_at`, `grace_ends_at`, `executed_at`. `status` is `requested`, `cancelled` or
`executed`. `idempotency_key`: `id`, `account_id`, `key`, `endpoint`, `response_body`,
`created_at`, unique on `(account_id, key)`.

**Derived, not stored.** `enrolment.course_progress` is the integer percentage of that course's
pages the account has marked complete, and a module's completion is derived from its pages, not
held in a column. A program's treasury burn is `treasury_total` minus `treasury_remaining`.
Entitlement is computed on read from the enrolment, the course and the account's program.

**Seed data.** Seven chains, which are this product's technology tracks and are first-class
rows rather than tags on a course, because a learner belongs to one the way a member belongs to
a faction: `Solidity` (slug `solidity`, category `blockchain`), `Avalanche` (slug `avax`,
`blockchain`), `Polygon` (slug `poly`, `blockchain`), `Flow` (slug `flow`, `blockchain`),
`Solana` (slug `solana`, `blockchain`), `Javascript` (slug `javascript`, `languages`) and
`AI` (slug `ai`, `artificialIntelligence`). Each carries its own accent and its own order.

Seven courses. `solidity-beginner`, title `ETH Proof: Beginner`, on `Solidity`,
`first_paywalled_module` null, not restricted, three modules. `solidity-intermediate`, title
`ETH Proof: Intermediate`, on `Solidity`, `first_paywalled_module` null, restricted to
`Halcyon Cohort 2026`, two modules. `solana-intern`, title `SOL Proof: Beginner`, on `Solana`,
`first_paywalled_module` `1`, `price_minor` `10000`, two modules. `polygon-advanced`, title
`POLY Proof: Advanced`, on `Polygon`, free, one module. `avax-advanced`, title
`AVAX Proof: Advanced`, on `Avalanche`, `first_paywalled_module` `1`, `price_minor` `10000`,
one module. `chatgpt-and-generative-ai`, title `AI Proof: Generative AI Unleashed`, on `AI`,
`first_paywalled_module` `1`, `price_minor` `10000`, one module. `intro-javascript`, title
`JS Proof: Beginner`, on `Javascript`, deprecated, one module. `course.order` carries gaps,
because a course that is withdrawn keeps its place rather than being renumbered.

Modules on `solana-intern`: `solana-intern-basics`, title `Accounts and Rent`, order `0`,
`project_type` `code`, `disable_project` false; `solana-intern-programs`, title
`Your First Program`, order `1`, `project_type` `code`, `disable_project` false. Module
`solidity-beginner-story`, title `The Zeronian Archive`, on `solidity-beginner`, order `2`,
`project_type` `storyNode`, `disable_project` true. Each module carries two lessons and each
lesson four pages.

Partners `Northgate Institute` (slug `northgate`) and `Halcyon Labs` (slug `halcyon`).
Programs `Northgate Cohort 2026` with `treasury_total` `50000`, `treasury_remaining` `10000`,
`seat_cap` `3`, `seats_granted` `2`; and `Halcyon Cohort 2026` with `treasury_total` `50000`,
`treasury_remaining` `50000`, `seat_cap` `10`, `seats_granted` `1`.

Accounts as named in `## User roles`, all on `deku-demo-pw-2026`. `learner@example.com` is
already enrolled in `solidity-beginner` and has read its first lesson.

Questions on `solana-intern-basics`: three, each `MultipleChoice` with four options, pass mark
`70`. Reward `Founding Artisan` on `Northgate Cohort 2026` for `solana-intern`, kind `token`,
`quota_total` `1`, `quota_claimed` `0`. Bounty `Audit a Vault` on `Northgate Cohort 2026`,
kind `job`, status `open`, `requires_credential` true.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the supplied visual and behavioural specification. Every value in it is
contract. Where it leaves a value open, it says so.

### Information architecture

Navigation is a persistent left sidebar on every signed-in route, carrying `Courses`,
`Bounties`, `Houses` and `AI Creations` as the four primary destinations, with the review and
registrar boards appearing only for the roles that hold them. Above the sidebar sits a
breadcrumb, because the content hierarchy is five levels deep and an Artisan who cannot see
chain, course, module, lesson and page at once loses their place. The header carries the brand
mark, a chain switcher, an announcements bell and the account control.

The work surface on `/review` and `/registrar` is a board: one column per state, cards moving
between columns. Creating a partner program is a wizard across three of its own addresses, one
per step, each linkable and each restorable on a back navigation. Step two invites seats from a
pasted CSV of email addresses: the rows are parsed and validated, previewed with a per-row
error report naming the line and the reason, and written only when the registrar confirms the
preview. A file with one bad row does not silently import the other forty nine. Feedback is an optimistic
row: the card moves to its new column at once and, if the server refuses, moves back with the
reason written beside it rather than in a layer that has to be dismissed.

### Colour

The ground and its surfaces are four ordered deep cool neutral steps: the page ground, the menu
surface above it, the raised panel above that, and the premium panel at the top. The interval
is the requirement, not the value: each step sits a small, even distance in luminance above the
one below, so a panel reads as raised with no outline at all. A build that adds a hairline
because a step looks subtle in isolation has produced a different product.

The muted border is a mid warm neutral. It is the only decorative colour in the system and it
never carries text, because it does not clear the body contrast bar against the ground.

Brand colour carries the product's own token names, because a builder needs to call them
something. `honey-gold-light` is a near-white muted amber and is primary text and the wordmark;
`honey-gold-dark` is a light soft amber and is its pressed and secondary state. The public catalogue alone carries `signal green`, a mid vivid
green, and `magenta glow`, a mid vivid violet used once as a box shadow under the hero; neither
appears on any signed-in route.

Semantic colour is rationed to four: `green`, a light vivid green, for done; a light soft red for
refused; a light soft amber for in progress; and a mid vivid cyan for waiting on a person.
Each carries a second signal beside the colour, so a reviewer scanning a board in greyscale
still reads it correctly.

Chain accents are one per faction and appear only on the chain badge: a light vivid cyan, a
light vivid blue, a light vivid violet, a mid vivid violet and a deep soft violet. Two further
gradient endpoints, a light vivid violet and a light soft violet, belong to the chain badge's
sweep and nowhere else.

Contrast is a build requirement and not a review item. Body text on the ground clears the WCAG
AA bar; large text and interface boundaries clear the three-to-one bar. The mid warm neutral
border clears neither at body size and is therefore never a text colour here. This is the rule
that stops a gold-on-dark palette drifting into unreadable elegance, which is how every dark
fantasy interface fails.

### Type

Display `Alexon`, body `CircularXX`, both with the normative fallback stacks given in
`## UI/UX notes`, so a first paint is never blank and never shifts when a face arrives. The
scale is `10px` micro, `12px` eyebrow, `14px` body, `16px` lead, `20px` title, `24px` title
large and `40px` heading. Code renders in the monospace stack at `14px` minimum, including
inside the options of a `MultipleChoiceCode` question. Numerals align in columns wherever
treasury amounts, results or seat counts stack.

### The ornamental frame

The frame is the product's visual signature and it is one component, not a set of one-off
rules. `variant` takes card, module, module-title, video-preview, circular, toast and offer.
`tone` takes gold, dark and double. `state` takes default, selected, locked and failed.
Nothing about it ships as a file: it is drawn from the palette. Where a variant is clipped to a
non-rectangular outline, the focus indicator renders on a wrapping element outside the clip, so
the clip can never cut it.

### Motion

State changes are perceivable and reversible. Only transform and opacity animate. Every reveal
has a static end state reachable at once. Feedback lands quickly, element transitions are
unhurried, and section reveals are slower still, with nothing anywhere a learner is trying to
work taking long enough to be waited on. In the reader and the whole assessment flow, reveals
are off entirely and only the shortest feedback remains, because somebody reading four thousand
pages does not want a theatrical entrance on each one.

Under `prefers-reduced-motion: reduce` the interface is fully functional and non-animated, and
continuous motion stops rather than slowing.

### Components and chrome

Every component carries resting, pointed-at, pressed, focused and unavailable states, and
unavailability is never signalled by colour alone. Escape closes any layer and returns focus to
its trigger. A destructive action, which here means revoking a credential or closing a program,
confirms first and states what will happen. Progressive dimming marks locked content: a
paywalled module reads as present and unavailable rather than absent.

### Pinned copy

`Welcome, ARTISAN.` on the dashboard. `Ready to start this course?` on a free course overview
and `Ready to buy this course?` on a paid one. `Successfully registered for course!` on
enrolment. `We recommend finishing the course you have already started so you can get
rewarded.` where a course is in flight. `Your 30-day countdown timer for completing and
claiming any bonus rewards will begin as soon as you purchase the course.` beside the reward
window. `No rewards for this course!` for an empty reward list. `Start Assessment`,
`Continue Assessment`, `Review Assessment`, `Continue Course` and `Continue Learning` on the
assessment controls. `Terms of Service`, `Privacy Policy`, `Cookie Policy` and `Manage Cookies`
in the footer of every page.

### Typography, spacing, radius and elevation

Typography is the two voices already named, and the scale is the one already given. Spacing
runs on a single small base unit doubling through a short ordered ramp, so every gap in the
product is a multiple of one number rather than a guess; the ramp is yours, the single base is
the requirement. Radius has four steps and no more: a small one on inputs and table cells, a
medium one on controls and cards, a larger one on panels, and fully round on an avatar.
Elevation is carried by two drop shadows only, a deeper one for a raised card on the dark
ground and a shallower one for anything on a light surface, plus two blur strengths behind an
open layer. Hover and pressed states brighten a surface slightly rather than recolouring it,
and locked content dims progressively rather than disappearing.

### The reader and its states

The reader is a single column of content with two rails: a lesson rail on the left showing
every lesson and page in the module with its completion mark, and a context rail on the right
carrying what the page teaches and what comes next. At tablet width the rails move into
drawers; at phone width the column fills the screen and a sticky bottom bar carries previous,
next and mark complete.

Six states, and each is specified rather than left to chance.

| State | What the Artisan sees |
|---|---|
| Loading | A skeleton matching the final layout's metrics, so nothing shifts when the content arrives. No full-page spinner. |
| Ready | The page body, the rails, and the position counter reading its place in the lesson and in the module. |
| Paywalled | The module's teaser, the lesson rail still visible with locked markers, and the enrolment control. The body text is absent, not blurred. |
| Empty | A named next action rather than a blank panel. |
| Not found | The reader's own not-found panel inside the module, keeping the rails and the place. |
| Refused | An inline explanation naming what was refused and why, with the surface unchanged behind it. |

The reader's address is the content contract: `/content/{courseID}/{moduleID}/{lessonID}/{pageID}`,
five levels and every one of them addressable, so any page in the product can be linked to
directly and restored on a back navigation.

Page navigation stitches across boundaries. The last page of a lesson advances to the first
page of the next lesson; the last page of the last lesson advances to the assessment gate. It
never advances to the site root, because an Artisan four hundred pages into a course who lands
on the front page has lost their place.

### Recommended next

The dashboard leads with the course in flight and then with a recommended next course, chosen
from the Artisan's recorded proficiency and the prerequisite courses each course declares. A
course whose prerequisites are unmet is shown with the unmet one named rather than hidden.

### Texture, badges and the wordmark

Nothing ships as a binary. The parchment ground is a drawn texture rather than an image file:
a fine, low-contrast grain over the deep cool neutral ground, subtle enough that body text over
it still clears its contrast bar. A chain badge is a lettermark tile, the chain's initial set in
the display face on that chain's own accent, so seven tracks are distinguishable at a glance
with no logo files anywhere in the build. The wordmark is the product name drawn in the display
voice as capitals, tracked open, and it is never coloured with a semantic colour.

### The board surface

`/review` and `/registrar` are boards, one column per state, cards in each. A reviewer's board
carries `InReview` and `InProgress`; a registrar's board carries `Completed` assessments
awaiting issuance and `issued` credentials. Each card shows the Artisan, the module, how long
it has been waiting, and the program that funded it. A card opens to a detail route showing the
submitted repository address and demo address beside the module's brief, with the previous
revision's reason visible where there was one.

Moving a card is optimistic: it lands in its new column at once, and a refusal returns it to
where it was with the reason written beside it. The board is operable from the keyboard alone,
and a move is announced when it completes.

### Verbatim copy on the public surface

`Where devs learn web3, earn rewards, land a job.` leads the public catalogue.
`Start Learning` is its primary action. `Invest in skills you need to succeed` heads the
value block, with the body
`Our courses are based on the actual skills, projects and even interview questions web3 companies use when hiring.`
The meta description of the public catalogue is
`Where developers learn from blockchain experts, earn rewards, and land their next web3 job.`
The bounty board opens with
`Proofworks invites you to join our talent pool to unlock opportunities for bounties, internships, and jobs with web3 employers.`
and
`We know exactly what companies are looking for - our platform guides you through projects that connect you with web3 job opportunities.`

### Responsiveness

Three tiers: phone, tablet and desktop. The sidebar is persistent at desktop, collapses behind
one control at tablet, and becomes a full-height panel over the page at phone width; opening
that panel traps focus, holds its own scroll position and restores the page's on close. The
board surface goes from three columns to one at phone width and the cards keep their column
label. Type steps at the tier switches rather than scaling continuously. Nothing drags the page
sideways at any width, and no route's phone height exceeds twice its desktop height.

### Accessibility

Every interactive element carries a visible focus indicator that clears contrast against both
the ground and a field. Focus order follows reading order on every route. A layer traps focus
and restores it to its trigger. Every command is reachable from the keyboard, including the
board, where a card moves between columns by keyboard alone and the move is announced. The
assessment flow in particular is completable end to end without a pointer, because a timed exam
that can only be answered with a mouse fails the people it is least fair to fail. Every content
image carries alternative text and decorative images declare themselves decorative.

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
| `GET /api/health` | - | `{ "status" }` |
| `POST /api/auth/login` | `{ "email", "password" }` | `{ "access_token", "account_id", "role", "program_id" }` |
| `GET /api/me` | - | `{ "id", "email", "display_name", "username", "role", "program_id", "status" }` |
| `GET /api/catalogue` | `?chain_id=&cursor=` | a top-level array of `{ "id", "identifier", "title", "chain_id", "first_paywalled_module", "restricted_to_program_id", "price_minor", "is_deprecated" }`, with `X-Next-Cursor` |
| `GET /api/courses/{course_id}` | - | `{ "id", "identifier", "title", "modules", "entitled", "reward_window_ends_at" }` |
| `GET /api/pages/{page_id}` | - | `{ "id", "title", "body_markdown", "page_current", "page_total", "lesson_current", "lesson_total" }` |
| `POST /api/pages/{page_id}/progress` | `{ "status" }` | `{ "page_id", "status", "course_progress" }` |
| `POST /api/enrolments` | `{ "course_id", "program_id" }` | `{ "id", "course_id", "program_id", "unlocked", "entitlement_source", "reward_window_ends_at" }` |
| `GET /api/enrolments` | - | a top-level array of `{ "id", "course_id", "program_id", "course_progress", "status" }` |
| `GET /api/assessments/{module_id}` | - | `{ "id", "module_id", "status", "accepted_terms", "accepted_camera_monitor", "verified_identity" }` |
| `POST /api/assessments/{module_id}/consent` | `{ "accepted_terms", "accepted_camera_monitor", "verified_identity" }` | `{ "id", "status", "accepted_terms", "accepted_camera_monitor", "verified_identity" }` |
| `POST /api/assessments/{module_id}/exam` | `{ "proctoring_mode" }` | `{ "exam_id", "status", "started_at", "ends_at", "proctoring_mode", "questions" }` |
| `POST /api/exams/{exam_id}/events` | `{ "kind", "occurred_at" }` | `{ "id", "kind", "occurred_at" }` |
| `POST /api/exams/{exam_id}/submit` | `{ "answers" }` | `{ "exam_id", "status", "result_percent", "assessment_status" }` |
| `POST /api/projects` | `{ "assessment_id", "repo_url", "demo_url" }` | `{ "id", "status", "revision_count" }` |
| `GET /api/projects` | `?status=&cursor=` | a top-level array of `{ "id", "account_id", "program_id", "repo_url", "demo_url", "status", "revision_count" }`, with `X-Next-Cursor` |
| `POST /api/projects/{project_id}/approve` | - | `{ "id", "status", "approved_by", "approved_at" }` |
| `POST /api/projects/{project_id}/changes` | `{ "reason" }` | `{ "id", "status", "revision_count" }` |
| `POST /api/exams/{exam_id}/clear` | `{ "reason" }` | `{ "exam_id", "status", "assessment_status" }` |
| `POST /api/credentials` | `{ "assessment_id" }` | `{ "id", "ledger_ref", "issued_at", "status", "proctoring_mode" }` |
| `GET /api/credentials` | `?cursor=` | a top-level array of `{ "id", "course_id", "module_id", "ledger_ref", "issued_at", "status" }`, with `X-Next-Cursor` |
| `POST /api/credentials/{credential_id}/revoke` | `{ "reason" }` | `{ "id", "status", "revoked_reason", "revoked_at" }` |
| `GET /api/credentials/proof/{ledger_ref}` | - | `{ "ledger_ref", "display_name", "course_title", "module_title", "issued_at", "proctoring_mode", "status" }` |
| `GET /api/ledger` | `?credential_id=` | a top-level array of `{ "id", "credential_id", "kind", "ledger_ref", "recorded_at" }` |
| `POST /api/rewards/{reward_id}/claim` | - | `{ "id", "reward_id", "status", "claimed_at", "expires_at" }` |
| `GET /api/programs` | - | a top-level array of `{ "id", "name", "treasury_total", "treasury_remaining", "seat_cap", "seats_granted" }` |
| `POST /api/programs` | `{ "partner_id", "name", "starts_on", "ends_on", "treasury_total", "seat_cap" }` | `{ "id", "name", "treasury_total", "treasury_remaining", "seat_cap" }` |
| `GET /api/programs/{program_id}/roster` | - | a top-level array of `{ "account_id", "display_name", "course_progress", "status" }` |
| `GET /api/bounties` | - | a top-level array of `{ "id", "title", "kind", "status", "requires_credential", "closes_at" }` |
| `POST /api/bounties/{bounty_id}/applications` | - | `{ "id", "bounty_id", "status" }` |
| `POST /api/erasure-requests` | - | `{ "id", "status", "requested_at", "grace_ends_at" }` |
| `GET /api/audit` | `?cursor=` | a top-level array of `{ "id", "actor_id", "action", "subject_type", "subject_id", "reason", "entry_hash", "recorded_at" }` |
| `GET /api/page-views` | - | a top-level array of `{ "route", "count" }` |
| `POST /api/page-views` | `{ "route" }` | `{ "route", "viewed_at" }` |
| `POST /api/cookie-choice` | `{ "accepted" }` | `{ "accepted", "recorded_at" }` |
| `GET /api/cookie-choice` | - | `{ "accepted", "recorded_at" }` |

Every list endpoint returns a top-level JSON array. Field names are exact. Bearer auth is
required on everything except `GET /api/health`, `POST /api/auth/login`, `GET /api/catalogue`
and `GET /api/credentials/proof/{ledger_ref}`. A successful call returns the named shape; an
invalid or unauthorized call is rejected as a client error, never a `5xx` and never a silent
success, and carries a reason. The agent chooses conventional codes.

### No mocks

PostgreSQL and Keycloak are the facts. An in-memory accounts dictionary, a hardcoded
`{"status":"issued"}` response the app returns to itself, a token the app signed for itself
instead of asking Keycloak, a ledger kept in process memory, or a roster served from a fixture
file are all contract violations however good the interface looks. The named provider is the
fact: the app's UI and its own tables can only reflect what lives in the provider, never
substitute for it.

## Definition of done

An Artisan signs in, enrols against a partner program's budget, reads a module, consents to
camera monitoring, sits a timed exam and submits a project. A reviewer who is not that learner
approves the work, and only then does a registrar issue the credential. The credential resolves
at its public address for somebody with no account, and it resolves there exactly once however
many times issuance is asked for. When the last funded seat in a treasury is claimed by two
people at the same moment, one of them is enrolled and the other is told why not.
