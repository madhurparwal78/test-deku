# Checklist: Proofworks Academy

Source: instruction.md
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-CN, C-TR, C-DM, C-FE, C-DC
Sections absent: C-BP
Unpinned values flagged: 4
Items: 535

## C-OV Overview

- [ ] `C-OV-1` `capability` Proofworks Academy certifies developer skill for workforce teams. `src: Overview`
- [ ] `C-OV-2` `capability` The application addresses a learner as `Artisan` throughout. `src: Overview`
- [ ] `C-OV-3` `data` The product holds chains, courses, modules, lessons, pages. `src: Overview`
- [ ] `C-OV-4` `capability` The product holds timed exams, projects, credentials, revocations. `src: Overview`
- [ ] `C-OV-5` `data` A partner program carries its own treasury that funds seats for a cohort. `src: Overview`
- [ ] `C-OV-6` `capability` A bounty board is reachable only by a holder of a credential. `src: Overview`
- [ ] `C-OV-7` `constraint` Issuance of a credential happens last in the flow. `src: Overview`
- [ ] `C-OV-8` `role` Issuance is countersigned by a role the learner does not hold. `src: Overview`
- [ ] `C-OV-9` `constraint` What issuance writes cannot be edited afterwards. `src: Overview`
- [ ] `C-OV-10` `role` Three personas use the platform, the Artisan, the reviewer, the registrar. `src: Overview`
- [ ] `C-OV-11` `constraint` The product builds no course authoring surface. `src: Overview`
- [ ] `C-OV-12` `constraint` The product takes no card payment. `src: Overview`

## C-RL User roles

- [ ] `C-RL-1` `role` The application has exactly three roles, `learner`, `reviewer`, `registrar`. `src: User roles table`
- [ ] `C-RL-2` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles`
- [ ] `C-RL-3` `role` A `learner` reads own enrolments, own progress, own assessments. `src: User roles table row 1`
- [ ] `C-RL-4` `role` A `learner` reads own projects, own credentials, own rewards. `src: User roles table row 1`
- [ ] `C-RL-5` `role` A `learner` reads published course metadata. `src: User roles table row 1`
- [ ] `C-RL-6` `role` A `learner` reads a free page anywhere. `src: User roles table row 1`
- [ ] `C-RL-7` `role` A `learner` reads a paid page only where entitled. `src: User roles table row 1`
- [ ] `C-RL-8` `role` A `learner` writes own progress, own consents, own answers, own project submission. `src: User roles table row 1`
- [ ] `C-RL-9` `role` A `reviewer` reads projects for learners funded by the reviewer's own program. `src: User roles table row 2`
- [ ] `C-RL-10` `role` A `reviewer` reads proctor event counts for learners funded by that same program. `src: User roles table row 2`
- [ ] `C-RL-11` `role` A `reviewer` approves a project. `src: User roles table row 2`
- [ ] `C-RL-12` `role` A `reviewer` requests changes on a project. `src: User roles table row 2`
- [ ] `C-RL-13` `role` A `reviewer` clears a `Suspicious` exam. `src: User roles table row 2`
- [ ] `C-RL-14` `role` A `reviewer` cannot issue a credential. `src: User roles table row 2`
- [ ] `C-RL-15` `role` A `reviewer` cannot revoke a credential. `src: User roles table row 2`
- [ ] `C-RL-16` `role` A `reviewer` cannot create a partner program. `src: User roles table row 2`
- [ ] `C-RL-17` `role` A `reviewer` cannot move a treasury balance. `src: User roles table row 2`
- [ ] `C-RL-18` `role` A `reviewer` cannot read a project belonging to another program. `src: User roles table row 2`
- [ ] `C-RL-19` `role` A `registrar` reads every program roster, every treasury. `src: User roles table row 3`
- [ ] `C-RL-20` `role` A `registrar` issues a credential. `src: User roles table row 3`
- [ ] `C-RL-21` `role` A `registrar` revokes a credential. `src: User roles table row 3`
- [ ] `C-RL-22` `role` A `registrar` creates a partner program. `src: User roles table row 3`
- [ ] `C-RL-23` `role` A `registrar` invites seats to a program. `src: User roles table row 3`
- [ ] `C-RL-24` `role` A `registrar` publishes an announcement. `src: User roles table row 3`
- [ ] `C-RL-25` `role` A `registrar` cannot approve a project. `src: User roles table row 3`
- [ ] `C-RL-26` `contract` Authorization is enforced server-side on every mutating endpoint. `src: User roles`
- [ ] `C-RL-27` `contract` A direct API call from a `learner` session to a `registrar` endpoint is denied by the server. `src: User roles`
- [ ] `C-RL-28` `contract` A denied call from a `learner` session leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-29` `capability` Signup is closed, with no public registration form. `src: User roles`
- [ ] `C-RL-30` `literal` The seeded learners are `learner@example.com`, `learner2@example.com`, `learner3@example.com`. `src: User roles`
- [ ] `C-RL-31` `literal` The seeded reviewer is `reviewer@example.com`. `src: User roles`
- [ ] `C-RL-32` `literal` The seeded registrar is `registrar@example.com`. `src: User roles`
- [ ] `C-RL-33` `data` `learner@example.com` belongs to `Northgate Cohort 2026`. `src: User roles`
- [ ] `C-RL-34` `data` `learner2@example.com` belongs to `Halcyon Cohort 2026`. `src: User roles`
- [ ] `C-RL-35` `data` `learner3@example.com` belongs to no program. `src: User roles`
- [ ] `C-RL-36` `constraint` A row carrying no `program_id` is public, visible to every account. `src: User roles`
- [ ] `C-RL-37` `constraint` A row carrying a `program_id` is visible only to accounts whose `program_id` matches. `src: User roles`
- [ ] `C-RL-38` `constraint` An account in a program gains no extra capability from the program. `src: User roles`

## C-CF Core features

- [ ] `C-CF-1` `capability` Sign-in exchanges an email plus a password for an `access_token`. `src: Core features, Auth`
- [ ] `C-CF-2` `contract` Every endpoint outside the public set carries `Authorization: Bearer <token>`. `src: Core features, Auth`
- [ ] `C-CF-3` `contract` The caller's role is read from the account row on the server. `src: Core features, Auth`
- [ ] `C-CF-4` `constraint` A `role` field in a request body is ignored. `src: Core features, Auth`
- [ ] `C-CF-5` `constraint` A `program_id` field in a request body is ignored. `src: Core features, Auth`
- [ ] `C-CF-6` `constraint` A disabled account is refused on every request, not only at sign-in. `src: Core features, Auth`
- [ ] `C-CF-7` `data` Content has five levels, chain, course, module, lesson, page. `src: Core features, catalogue`
- [ ] `C-CF-8` `literal` A page is addressable at `/content/{course_id}/{module_id}/{lesson_id}/{page_id}`. `src: Core features, catalogue rule 1`
- [ ] `C-CF-9` `data` A page response carries `page_current`, `page_total`, `lesson_current`, `lesson_total`. `src: Core features, catalogue rule 1`
- [ ] `C-CF-10` `capability` Marking a page complete records one `page_progress` row for that account plus page. `src: Core features, catalogue rule 2`
- [ ] `C-CF-11` `capability` `enrolment.course_progress` is recomputed in the same write as the page progress. `src: Core features, catalogue rule 2`
- [ ] `C-CF-12` `constraint` Marking one page complete twice creates no second `page_progress` row. `src: Core features, catalogue rule 2`
- [ ] `C-CF-13` `constraint` Marking one page complete twice does not move the percentage a second time. `src: Core features, catalogue rule 2`
- [ ] `C-CF-14` `constraint` A page already `complete` never returns to `in_progress`. `src: Core features, catalogue rule 3`
- [ ] `C-CF-15` `constraint` A late write carrying the earlier status is refused as invalid. `src: Core features, catalogue rule 3`
- [ ] `C-CF-16` `capability` A module becomes complete only when every page under the module is complete. `src: Core features, catalogue rule 4`
- [ ] `C-CF-17` `constraint` A deprecated course stays readable to an account already enrolled. `src: Core features, catalogue rule 5`
- [ ] `C-CF-18` `constraint` A deprecated course never appears in the enrolable catalogue. `src: Core features, catalogue rule 5`
- [ ] `C-CF-19` `constraint` A module whose `order` is at or past `first_paywalled_module` needs entitlement. `src: Core features, entitlement rule 1`
- [ ] `C-CF-20` `literal` `first_paywalled_module` null means the whole course is free. `src: Core features, entitlement rule 1`
- [ ] `C-CF-21` `literal` `first_paywalled_module` `0` means the whole course is paid. `src: Core features, entitlement rule 1`
- [ ] `C-CF-22` `constraint` `restricted_to_program` is a separate gate stacking with the paywall. `src: Core features, entitlement rule 2`
- [ ] `C-CF-23` `data` `solidity-intermediate` is free, restricted to `Halcyon Cohort 2026`. `src: Core features, entitlement rule 2`
- [ ] `C-CF-24` `role` `learner@example.com` cannot read `solidity-intermediate`. `src: Core features, entitlement rule 2`
- [ ] `C-CF-25` `role` `learner2@example.com` can read `solidity-intermediate`. `src: Core features, entitlement rule 2`
- [ ] `C-CF-26` `constraint` An unentitled request for a paid page body returns no body text. `src: Core features, entitlement rule 4`
- [ ] `C-CF-27` `capability` A course title stays visible to an unentitled account. `src: Core features, entitlement rule 4`
- [ ] `C-CF-28` `capability` Enrolling in a free unrestricted course sets `entitlement_source` to `free`. `src: Core features, enrolment rule 1`
- [ ] `C-CF-29` `capability` Enrolling in a paid course reserves `course.price_minor` from `partner_program.treasury_remaining`. `src: Core features, enrolment rule 2`
- [ ] `C-CF-30` `capability` A funded enrolment increments `partner_program.seats_granted`. `src: Core features, enrolment rule 2`
- [ ] `C-CF-31` `literal` A funded enrolment sets `entitlement_source` to `program`. `src: Core features, enrolment rule 2`
- [ ] `C-CF-32` `data` `Northgate Cohort 2026` holds `10000` minor units of treasury. `src: Core features, enrolment rule 3`
- [ ] `C-CF-33` `data` `solana-intern` costs `10000` minor units. `src: Core features, enrolment rule 3`
- [ ] `C-CF-34` `constraint` Two simultaneous enrolments in `solana-intern` against `Northgate Cohort 2026` do not both succeed. `src: Core features, enrolment rule 3`
- [ ] `C-CF-35` `constraint` The losing simultaneous enrolment is refused with a reason naming the exhausted treasury. `src: Core features, enrolment rule 3`
- [ ] `C-CF-36` `constraint` `treasury_remaining` never falls below zero. `src: Core features, enrolment rule 3`
- [ ] `C-CF-37` `constraint` A refused enrolment leaves no half-written enrolment row. `src: Core features, enrolment rule 3`
- [ ] `C-CF-38` `constraint` Enrolling twice in one course reactivates the same enrolment row. `src: Core features, enrolment rule 4`
- [ ] `C-CF-39` `constraint` No second enrolment row exists for one account plus one course. `src: Core features, enrolment rule 4`
- [ ] `C-CF-40` `data` An enrolment records the `program_id` that funded the enrolment. `src: Core features, enrolment rule 5`
- [ ] `C-CF-41` `constraint` The program an account belongs to today is never read as the program that funded an enrolment. `src: Core features, enrolment rule 5`
- [ ] `C-CF-42` `ui` A learner with an unfinished course sees the observed course-in-flight recommendation copy. `src: Core features, enrolment rule 6`
- [ ] `C-CF-43` `capability` A learner warned about a course in flight may continue enrolling. `src: Core features, enrolment rule 6`
- [ ] `C-CF-44` `literal` `assessment.status` takes `PreAssessment`, `Exam`, `ExamReview`, `Project`, `ProjectReview`, `Completed`. `src: Core features, assessment rule 1`
- [ ] `C-CF-45` `constraint` `assessment.status` is set only by the server. `src: Core features, assessment rule 1`
- [ ] `C-CF-46` `capability` An assessment is created in `PreAssessment` when a module's curriculum reaches complete. `src: Core features, assessment rule 2`
- [ ] `C-CF-47` `constraint` `PreAssessment` advances to `Exam` only when all three consents are true. `src: Core features, assessment rule 3`
- [ ] `C-CF-48` `constraint` A start request with any consent false is refused as invalid. `src: Core features, assessment rule 3`
- [ ] `C-CF-49` `constraint` A refused start leaves `assessment.status` unchanged. `src: Core features, assessment rule 3`
- [ ] `C-CF-50` `capability` `Exam` advances to `ExamReview` on a learner submit. `src: Core features, assessment rule 4`
- [ ] `C-CF-51` `capability` `Exam` advances to `ExamReview` when the server observes `exam.ends_at` has passed. `src: Core features, assessment rule 4`
- [ ] `C-CF-52` `constraint` A learner who never submits still reaches `ExamReview`. `src: Core features, assessment rule 4`
- [ ] `C-CF-53` `literal` `ExamReview` advances to `Project` at a `result_percent` of `70` or above with no blocking proctor signal. `src: Core features, assessment rule 5`
- [ ] `C-CF-54` `literal` A passing auto-grade sets `exam.status` to `Passed`. `src: Core features, assessment rule 5`
- [ ] `C-CF-55` `literal` A `result_percent` below `70` returns the assessment to `PreAssessment`. `src: Core features, assessment rule 6`
- [ ] `C-CF-56` `literal` A failing auto-grade sets `exam.status` to `Failed`. `src: Core features, assessment rule 6`
- [ ] `C-CF-57` `literal` A retake of one module is refused for `300` seconds after a failure. `src: Core features, assessment rule 6`
- [ ] `C-CF-58` `literal` Proctor signals above the threshold set `exam.status` to `Suspicious`. `src: Core features, assessment rule 7`
- [ ] `C-CF-59` `constraint` A `Suspicious` assessment stays in `ExamReview` until a reviewer clears the assessment. `src: Core features, assessment rule 7`
- [ ] `C-CF-60` `capability` Clearing a `Suspicious` exam writes an audit entry naming the reviewer. `src: Core features, assessment rule 7`
- [ ] `C-CF-61` `capability` `Project` advances to `ProjectReview` on submission. `src: Core features, assessment rule 8`
- [ ] `C-CF-62` `capability` A module carrying `disable_project` true advances from `Project` straight to `Completed`. `src: Core features, assessment rule 8`
- [ ] `C-CF-63` `capability` `ProjectReview` advances to `Completed` on approval. `src: Core features, assessment rule 9`
- [ ] `C-CF-64` `capability` A request for changes returns the assessment to `Project`. `src: Core features, assessment rule 9`
- [ ] `C-CF-65` `capability` A request for changes increments `project.revision_count`. `src: Core features, assessment rule 9`
- [ ] `C-CF-66` `constraint` A transition the table does not allow is refused as invalid. `src: Core features, assessment rule 10`
- [ ] `C-CF-67` `constraint` A refused transition changes nothing. `src: Core features, assessment rule 10`
- [ ] `C-CF-68` `constraint` Opening the exam route outside status `Exam` returns the learner to the gate. `src: Core features, assessment rule 10`
- [ ] `C-CF-69` `literal` `exam.ends_at` is `1800` seconds after `started_at`. `src: Core features, proctored rule 1`
- [ ] `C-CF-70` `constraint` `exam.ends_at` is set by the server. `src: Core features, proctored rule 1`
- [ ] `C-CF-71` `constraint` A client-supplied end time is ignored. `src: Core features, proctored rule 1`
- [ ] `C-CF-72` `literal` `exam.timeout_source` records `Browser` or `Server`. `src: Core features, proctored rule 1`
- [ ] `C-CF-73` `data` A question is served with `prompt`, `kind`, options. `src: Core features, proctored rule 2`
- [ ] `C-CF-74` `literal` `exam_question.kind` takes `MultipleChoice` or `MultipleChoiceCode`. `src: Core features, proctored rule 2`
- [ ] `C-CF-75` `constraint` `answer_key` appears in no learner-facing response at any point. `src: Core features, proctored rule 2`
- [ ] `C-CF-76` `literal` `proctor_event.kind` takes `AnswerSubmitted`, `OffFocus`, `OnFocus`, `NoFaceDetected`, `MultipleFaceDetected`, `FaceResolved`, `TestStarted`, `TestResumed`, `TestSubmitted`. `src: Core features, proctored rule 3`
- [ ] `C-CF-77` `data` A proctor event carries an `occurred_at`. `src: Core features, proctored rule 3`
- [ ] `C-CF-78` `constraint` No image reaches the server from the camera. `src: Core features, proctored rule 3`
- [ ] `C-CF-79` `literal` Three events of kind `NoFaceDetected` or `MultipleFaceDetected` in one attempt make the exam `Suspicious`. `src: Core features, proctored rule 4`
- [ ] `C-CF-80` `constraint` A proctor signal never fails an exam by itself. `src: Core features, proctored rule 4`
- [ ] `C-CF-81` `ui` The learner is told the proctoring mode before starting. `src: Core features, proctored rule 5`
- [ ] `C-CF-82` `literal` `exam.proctoring_mode` records `full`, `degraded` or `none`. `src: Core features, proctored rule 5`
- [ ] `C-CF-83` `data` A credential issued from a `none` attempt carries that mode. `src: Core features, proctored rule 5`
- [ ] `C-CF-84` `capability` Withdrawing camera consent during an attempt ends the attempt at once. `src: Core features, proctored rule 6`
- [ ] `C-CF-85` `constraint` A voided attempt consumes no retake allowance. `src: Core features, proctored rule 6`
- [ ] `C-CF-86` `data` A project submission carries a `repo_url` plus a `demo_url`. `src: Core features, project rule 1`
- [ ] `C-CF-87` `constraint` A submission missing either address is refused as invalid. `src: Core features, project rule 1`
- [ ] `C-CF-88` `constraint` A refused submission writes no project row. `src: Core features, project rule 1`
- [ ] `C-CF-89` `role` A project belongs to the review board of the program that funded the enrolment. `src: Core features, project rule 2`
- [ ] `C-CF-90` `role` A reviewer attached to another program is denied reading that project. `src: Core features, project rule 2`
- [ ] `C-CF-91` `role` A reviewer attached to another program is denied approving that project. `src: Core features, project rule 2`
- [ ] `C-CF-92` `role` An approval request whose caller is the project's own learner is denied. `src: Core features, project rule 3`
- [ ] `C-CF-93` `constraint` After a denied self-approval `project.status` still reads `InReview`. `src: Core features, project rule 3`
- [ ] `C-CF-94` `literal` `project.status` takes `InProgress`, `InReview`, `Approved`. `src: Core features, project rule 4`
- [ ] `C-CF-95` `capability` Approving a project writes `approved_by`, `approved_at`. `src: Core features, project rule 5`
- [ ] `C-CF-96` `capability` Approving a project writes an audit entry. `src: Core features, project rule 5`
- [ ] `C-CF-97` `role` Only a `registrar` issues a credential. `src: Core features, credential rule 1`
- [ ] `C-CF-98` `constraint` An issue request from a `learner` is denied. `src: Core features, credential rule 1`
- [ ] `C-CF-99` `constraint` An issue request from a `reviewer` is denied. `src: Core features, credential rule 1`
- [ ] `C-CF-100` `constraint` A denied issue request creates no credential. `src: Core features, credential rule 1`
- [ ] `C-CF-101` `constraint` Issuance requires the assessment in `Completed`. `src: Core features, credential rule 2`
- [ ] `C-CF-102` `constraint` Issuing against any other assessment status is refused as invalid. `src: Core features, credential rule 2`
- [ ] `C-CF-103` `capability` Issuance appends exactly one `ledger_entry`. `src: Core features, credential rule 3`
- [ ] `C-CF-104` `data` `ledger_ref` is the lowercase SHA-256 hex of the canonical issuance payload, pipe-joined from the credential id, the account id, the course id, the module id, the issuance instant. `src: Core features, credential rule 3`
- [ ] `C-CF-105` `constraint` Issuing one credential twice writes no second ledger entry. `src: Core features, credential rule 4`
- [ ] `C-CF-106` `constraint` Issuing one credential twice returns the original `ledger_ref`. `src: Core features, credential rule 4`
- [ ] `C-CF-107` `constraint` Two simultaneous issue requests for one completed assessment produce exactly one credential. `src: Core features, credential rule 4`
- [ ] `C-CF-108` `literal` `GET /api/credentials/proof/{ledger_ref}` needs no credential. `src: Core features, credential rule 5`
- [ ] `C-CF-109` `data` The public proof endpoint answers with the holder's display name, the course title, the module title, `issued_at`, `proctoring_mode`, `status`. `src: Core features, credential rule 5`
- [ ] `C-CF-110` `constraint` An unknown reference is reported as not found rather than as an error. `src: Core features, credential rule 5`
- [ ] `C-CF-111` `role` Revoking a credential is a `registrar` action. `src: Core features, credential rule 6`
- [ ] `C-CF-112` `capability` Revoking writes `credential.status` `revoked` with a `revoked_reason`. `src: Core features, credential rule 6`
- [ ] `C-CF-113` `capability` Revoking appends a second ledger entry of kind `revocation`. `src: Core features, credential rule 6`
- [ ] `C-CF-114` `constraint` Revoking never edits the issuance entry. `src: Core features, credential rule 6`
- [ ] `C-CF-115` `constraint` Revoking never deletes the issuance entry. `src: Core features, credential rule 6`
- [ ] `C-CF-116` `capability` The public proof endpoint after a revocation still resolves, reporting `revoked`. `src: Core features, credential rule 6`
- [ ] `C-CF-117` `constraint` A deprecated course never revokes a credential. `src: Core features, credential rule 7`
- [ ] `C-CF-118` `literal` `reward.kind` takes `nft`, `coupon`, `token`, `fiat`. `src: Core features, rewards rule 1`
- [ ] `C-CF-119` `literal` `reward_earn.status` takes `in_progress`, `redeemed`, `expired`. `src: Core features, rewards rule 1`
- [ ] `C-CF-120` `capability` `enrolment.reward_window_ends_at` is computed once, at enrolment, thirty days later. `src: Core features, rewards rule 2`
- [ ] `C-CF-121` `ui` The learner is shown the absolute reward window date. `src: Core features, rewards rule 2`
- [ ] `C-CF-122` `ui` The course overview carries the observed reward-window countdown copy. `src: Core features, rewards rule 2`
- [ ] `C-CF-123` `constraint` The reward window gates bonus rewards only. `src: Core features, rewards rule 3`
- [ ] `C-CF-124` `constraint` Course completion is never time limited. `src: Core features, rewards rule 3`
- [ ] `C-CF-125` `constraint` Expiry is inclusive to the end of the thirtieth day in UTC. `src: Core features, rewards rule 4`
- [ ] `C-CF-126` `constraint` A claim landing in the same second as expiry resolves in the learner's favour. `src: Core features, rewards rule 4`
- [ ] `C-CF-127` `role` Extending a reward window is a `registrar` action only. `src: Core features, rewards rule 5`
- [ ] `C-CF-128` `capability` An extension writes an audit entry naming who extended the window. `src: Core features, rewards rule 5`
- [ ] `C-CF-129` `constraint` `reward.quota_total` is never oversold. `src: Core features, rewards rule 6`
- [ ] `C-CF-130` `constraint` Two simultaneous claims of the last unit produce exactly one `reward_earn`. `src: Core features, rewards rule 6`
- [ ] `C-CF-131` `constraint` A reward balance is never added to a treasury balance. `src: Core features, rewards rule 7`
- [ ] `C-CF-132` `literal` `bounty.status` takes `open`, `work_started`, `submissions`, `concluded`, `expired`, `canceled`. `src: Core features, bounties rule 1`
- [ ] `C-CF-133` `literal` `bounty_application.status` takes `viewed`, `bookmarked`, `applied`, `accepted`, `rejected`, `work_started`, `submitted`, `canceled`. `src: Core features, bounties rule 1`
- [ ] `C-CF-134` `ui` A learner at `work_started` on a `canceled` bounty sees both states named. `src: Core features, bounties rule 2`
- [ ] `C-CF-135` `constraint` An application to a credential-gated bounty from an account holding none is denied. `src: Core features, bounties rule 3`
- [ ] `C-CF-136` `constraint` A denied bounty application writes no application row. `src: Core features, bounties rule 3`
- [ ] `C-CF-137` `constraint` Each consent is a separate opt-in, never pre-ticked. `src: Core features, consent rule 1`
- [ ] `C-CF-138` `data` `accepted_terms` carries `terms_version`. `src: Core features, consent rule 1`
- [ ] `C-CF-139` `data` `accepted_camera_monitor` carries `camera_consent_at`. `src: Core features, consent rule 1`
- [ ] `C-CF-140` `ui` A plain-language disclosure appears before the camera activates. `src: Core features, consent rule 1`
- [ ] `C-CF-141` `constraint` Face detection runs on the learner's own machine. `src: Core features, consent rule 2`
- [ ] `C-CF-142` `constraint` Biometric signals are never used to train any model. `src: Core features, consent rule 2`
- [ ] `C-CF-143` `literal` Proctor events are kept for `90` days from the attempt. `src: Core features, consent rule 3`
- [ ] `C-CF-144` `ui` The privacy page states the retention schedule for every kind of record. `src: Core features, consent rule 3`
- [ ] `C-CF-145` `capability` An erasure request records a thirty day grace period. `src: Core features, consent rule 4`
- [ ] `C-CF-146` `capability` Erasure execution clears the personal fields on the account. `src: Core features, consent rule 4`
- [ ] `C-CF-147` `capability` Erasure execution sets `deleted_at`. `src: Core features, consent rule 4`
- [ ] `C-CF-148` `constraint` A credential in the ledger is never erased. `src: Core features, consent rule 4`
- [ ] `C-CF-149` `constraint` `GET /api/programs/{program_id}/roster` returns no email address. `src: Core features, consent rule 5`
- [ ] `C-CF-150` `capability` Every issuance appends an `audit_entry` naming the actor, the action, the subject. `src: Core features, audit rule 1`
- [ ] `C-CF-151` `constraint` `audit_entry` is append only, never updated, never deleted. `src: Core features, audit rule 1`
- [ ] `C-CF-152` `data` Each audit entry carries `prev_hash`, `entry_hash`. `src: Core features, audit rule 2`
- [ ] `C-CF-153` `role` `GET /api/audit` is a `registrar` surface. `src: Core features, audit rule 2`
- [ ] `C-CF-154` `constraint` The audit trail lives in a different table from the learner activity feed. `src: Core features, audit rule 3`
- [ ] `C-CF-155` `constraint` Pricing resolution happens on the server, never from the request. `src: Core features, money rule 1`
- [ ] `C-CF-156` `constraint` A program discount applies to a course price once. `src: Core features, money rule 1`
- [ ] `C-CF-157` `constraint` `treasury_total` minus `treasury_remaining` equals the sum of funded enrolments. `src: Core features, money rule 2`
- [ ] `C-CF-158` `constraint` A reward balance is never presented as redeemable for cash. `src: Core features, money rule 3`
- [ ] `C-CF-159` `capability` A mutating request is rate limited per account. `src: Core features, money rule 4`
- [ ] `C-CF-160` `literal` A response carries `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`. `src: Core features, money rule 4`
- [ ] `C-CF-161` `literal` A refused rate-limited request carries `Retry-After`. `src: Core features, money rule 4`
- [ ] `C-CF-162` `capability` Replaying a request carrying a known `Idempotency-Key` returns the first response. `src: Core features, money rule 5`
- [ ] `C-CF-163` `constraint` A replayed idempotent request performs the action once. `src: Core features, money rule 5`
- [ ] `C-CF-164` `ui` A privacy page at `/privacy` is reachable from the footer of every page. `src: Core features, public surface rule 1`
- [ ] `C-CF-165` `ui` The privacy page states what Proofworks records about an Artisan. `src: Core features, public surface rule 1`
- [ ] `C-CF-166` `ui` The privacy page states that a credential in the ledger is permanent. `src: Core features, public surface rule 1`
- [ ] `C-CF-167` `capability` A first-time visitor is asked once about non-essential cookies. `src: Core features, public surface rule 2`
- [ ] `C-CF-168` `constraint` The cookie answer survives a reload. `src: Core features, public surface rule 2`
- [ ] `C-CF-169` `constraint` The cookie question is not asked a second time. `src: Core features, public surface rule 2`
- [ ] `C-CF-170` `capability` Each page view is recorded with its route plus the moment of the view. `src: Core features, public surface rule 3`
- [ ] `C-CF-171` `role` A `registrar` reads the page-view counts per route. `src: Core features, public surface rule 3`
- [ ] `C-CF-172` `ui` Every form rejects invalid input in place, naming the field at fault. `src: Core features, public surface rule 4`
- [ ] `C-CF-173` `constraint` A rejected form writes nothing. `src: Core features, public surface rule 4`
- [ ] `C-CF-174` `ui` An unknown address renders the product's own not-found page. `src: Core features, public surface rule 5`
- [ ] `C-CF-175` `ui` The not-found page offers a way back into the catalogue. `src: Core features, public surface rule 5`
- [ ] `C-CF-176` `constraint` An unknown address answers as not found rather than as an error. `src: Core features, public surface rule 5`
- [ ] `C-CF-177` `constraint` Every internal link on every public route resolves. `src: Core features, public surface rule 6`

## C-UF User flow

- [ ] `C-UF-1` `literal` `/` serves the public catalogue of chains plus courses. `src: User flow table`
- [ ] `C-UF-2` `literal` `/proof/<ledger_ref>` serves the public credential proof page. `src: User flow table`
- [ ] `C-UF-3` `literal` `/privacy` serves the privacy page. `src: User flow table`
- [ ] `C-UF-4` `literal` `/login` serves sign-in. `src: User flow table`
- [ ] `C-UF-5` `literal` `/home` serves the Artisan dashboard. `src: User flow table`
- [ ] `C-UF-6` `literal` `/courses/<chain_id>` serves one chain's courses. `src: User flow table`
- [ ] `C-UF-7` `literal` `/content/<course_id>` serves the course overview. `src: User flow table`
- [ ] `C-UF-8` `literal` `/content/<course_id>/<module_id>/<lesson_id>/<page_id>` serves the reader. `src: User flow table`
- [ ] `C-UF-9` `literal` `/content/<course_id>/<module_id>/assessment` serves the gate plus the three consents. `src: User flow table`
- [ ] `C-UF-10` `literal` `/content/<course_id>/<module_id>/assessment/exam` serves the timed exam. `src: User flow table`
- [ ] `C-UF-11` `literal` `/content/<course_id>/<module_id>/assessment/project` serves project submission. `src: User flow table`
- [ ] `C-UF-12` `literal` `/credentials` serves the learner's own credentials. `src: User flow table`
- [ ] `C-UF-13` `literal` `/bounties` serves the bounty board. `src: User flow table`
- [ ] `C-UF-14` `literal` `/review` serves the review board. `src: User flow table`
- [ ] `C-UF-15` `literal` `/review/<project_id>` serves one project under review. `src: User flow table`
- [ ] `C-UF-16` `literal` `/registrar` serves the issuance board. `src: User flow table`
- [ ] `C-UF-17` `literal` `/programs` serves programs, rosters, treasuries. `src: User flow table`
- [ ] `C-UF-18` `literal` `/programs/new` serves wizard step one. `src: User flow table`
- [ ] `C-UF-19` `literal` `/programs/new/seats` serves wizard step two. `src: User flow table`
- [ ] `C-UF-20` `literal` `/programs/new/review` serves wizard step three. `src: User flow table`
- [ ] `C-UF-21` `capability` A signed-out request for a signed-in route goes to `/login`. `src: User flow, Entry and redirects`
- [ ] `C-UF-22` `capability` Sign-in returns the visitor to the route asked for. `src: User flow, Entry and redirects`
- [ ] `C-UF-23` `capability` Sign-in with no destination lands on `/home`. `src: User flow, Entry and redirects`
- [ ] `C-UF-24` `capability` Sign-out returns the visitor to `/`. `src: User flow, Entry and redirects`
- [ ] `C-UF-25` `capability` A token expiring mid-action keeps the typed values. `src: User flow, Entry and redirects`
- [ ] `C-UF-26` `role` A `learner` reaching `/review` is refused. `src: User flow, Entry and redirects`
- [ ] `C-UF-27` `role` A `learner` reaching `/registrar` is refused. `src: User flow, Entry and redirects`
- [ ] `C-UF-28` `role` A `learner` reaching `/programs` is refused. `src: User flow, Entry and redirects`
- [ ] `C-UF-29` `capability` A learner enrols in `solana-intern` against `Northgate Cohort 2026`. `src: User flow, journey 1`
- [ ] `C-UF-30` `ui` The funded seat count is shown after enrolment. `src: User flow, journey 1`
- [ ] `C-UF-31` `capability` Marking the last page of `solana-intern-basics` complete opens the assessment gate. `src: User flow, journey 2`
- [ ] `C-UF-32` `capability` Accepting the three consents starts the timed exam. `src: User flow, journey 3`
- [ ] `C-UF-33` `capability` Submitting answers lands the assessment in `ExamReview` with a `result_percent`. `src: User flow, journey 3`
- [ ] `C-UF-34` `capability` A submitted project appears on `/review` for `reviewer@example.com`. `src: User flow, journey 4`
- [ ] `C-UF-35` `capability` Approval of the project reaches `Completed`. `src: User flow, journey 4`
- [ ] `C-UF-36` `capability` `registrar@example.com` issues the credential from `/registrar`. `src: User flow, journey 5`
- [ ] `C-UF-37` `capability` `/proof/<ledger_ref>` reads the credential back signed out. `src: User flow, journey 5`
- [ ] `C-UF-38` `role` `learner2@example.com` asking for `learner@example.com`'s project is refused. `src: User flow, journey 6`
- [ ] `C-UF-39` `constraint` A refused cross-account project request leaves the project unmoved. `src: User flow, journey 6`
- [ ] `C-UF-40` `ui` Every list carries an empty state naming the next action. `src: User flow, States`
- [ ] `C-UF-41` `ui` Every route carries a loading state. `src: User flow, States`
- [ ] `C-UF-42` `ui` A refused action reverts its optimistic row in place. `src: User flow, States`
- [ ] `C-UF-43` `ui` A refused action states the reason beside the row. `src: User flow, States`
- [ ] `C-UF-44` `constraint` An error never takes over the page. `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-1` `ui` The direction is an ornate gold-on-dark arcane manuscript over a working console. `src: UI/UX notes`
- [ ] `C-UX-2` `ui` The register is operational, so the boards read quiet, built for scanning. `src: UI/UX notes`
- [ ] `C-UX-3` `ui` Atmosphere is confined to the ornamental frame plus the chain badges. `src: UI/UX notes`
- [ ] `C-UX-4` `ui` The product commits to dark. `src: UI/UX notes`
- [ ] `C-UX-5` `ui` The ground is a deep cool neutral. `src: UI/UX notes`
- [ ] `C-UX-6` `ui` Three further deep cool neutral steps carry the menu, the raised panel, the premium panel. `src: UI/UX notes`
- [ ] `C-UX-7` `ui` Surfaces separate by luminance rather than by an outline. `src: UI/UX notes`
- [ ] `C-UX-8` `ui` Primary text is a near-white muted amber, worn by nothing else on a page. `src: UI/UX notes`
- [ ] `C-UX-9` `ui` The muted border is a mid warm neutral, decorative only, never carrying text. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` A light vivid green means done. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` A light soft red means refused. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` A light soft amber means in progress. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` A mid vivid cyan means a person is still looking. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` A chain badge carries one accent, appearing nowhere else. `src: UI/UX notes`
- [ ] `C-UX-15` `ui` The public catalogue alone carries a mid vivid green signal colour. `src: UI/UX notes`
- [ ] `C-UX-16` `literal` The display face is `Alexon`. `src: UI/UX notes`
- [ ] `C-UX-17` `literal` The body face is `CircularXX`. `src: UI/UX notes`
- [ ] `C-UX-18` `literal` Code never renders below `14px`. `src: UI/UX notes`
- [ ] `C-UX-19` `ui` Figures align in columns wherever treasury amounts stack. `src: UI/UX notes`
- [ ] `C-UX-20` `ui` The ornamental frame is one component carrying variants, tones, states. `src: UI/UX notes`
- [ ] `C-UX-21` `ui` The frame is drawn rather than shipped as a file. `src: UI/UX notes`
- [ ] `C-UX-22` `ui` A focus ring renders outside a non-rectangular clip. `src: UI/UX notes`
- [ ] `C-UX-23` `ui` Density is comfortable in the reader, compact on the boards. `src: UI/UX notes`
- [ ] `C-UX-24` `ui` Motion is eased, restrained, carrying state feedback only. `src: UI/UX notes`
- [ ] `C-UX-25` `ui` Only transform plus opacity animate. `src: UI/UX notes`
- [ ] `C-UX-26` `ui` Every reveal has a static end state reachable at once. `src: UI/UX notes`
- [ ] `C-UX-27` `ui` The reader carries no entrance animation. `src: UI/UX notes`
- [ ] `C-UX-28` `ui` The interface stays functional under a reduced-motion preference. `src: UI/UX notes`
- [ ] `C-UX-29` `ui` A control carries resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes`
- [ ] `C-UX-30` `ui` An input shows its label plus its error in a fixed place. `src: UI/UX notes`
- [ ] `C-UX-31` `ui` Escape closes a layer, returning focus to the trigger. `src: UI/UX notes`
- [ ] `C-UX-32` `ui` A destructive action confirms first. `src: UI/UX notes`
- [ ] `C-UX-33` `ui` Unavailability is never signalled by colour alone. `src: UI/UX notes`
- [ ] `C-UX-34` `ui` Body text meets the WCAG AA contrast bar. `src: UI/UX notes`
- [ ] `C-UX-35` `ui` Large text meets the three-to-one contrast bar. `src: UI/UX notes`
- [ ] `C-UX-36` `ui` Every command has a keyboard route with a visible focus ring. `src: UI/UX notes`
- [ ] `C-UX-37` `ui` An icon-only control carries a label. `src: UI/UX notes`
- [ ] `C-UX-38` `ui` Responsive behaviour holds at phone, tablet, desktop tiers. `src: UI/UX notes`
- [ ] `C-UX-39` `ui` Nothing overflows sideways at the narrowest viewport. `src: UI/UX notes`
- [ ] `C-UX-40` `ui` Every route stays usable at four hundred percent zoom. `src: UI/UX notes`
- [ ] `C-UX-41` `ui` A progress save is announced politely. `src: UI/UX notes`

## C-CN Constraints

- [ ] `C-CN-1` `constraint` A learner never reads another learner's rows. `src: Constraints`
- [ ] `C-CN-2` `constraint` A reviewer never reads a project funded by an unattached program. `src: Constraints`
- [ ] `C-CN-3` `constraint` Money moves only as a partner treasury balance in integer minor units of `usd`. `src: Constraints`
- [ ] `C-CN-4` `constraint` No external network call is made at run time beyond the two backing services. `src: Constraints`
- [ ] `C-CN-5` `constraint` No course authoring surface is built. `src: Constraints`
- [ ] `C-CN-6` `constraint` No identity provider other than the one named is built. `src: Constraints`
- [ ] `C-CN-7` `constraint` No chat community is built. `src: Constraints`
- [ ] `C-CN-8` `constraint` No outbound email is sent. `src: Constraints`
- [ ] `C-CN-9` `constraint` No video hosting is built. `src: Constraints`
- [ ] `C-CN-10` `constraint` No learner-supplied code is executed. `src: Constraints`
- [ ] `C-CN-11` `constraint` No wallet is built. `src: Constraints`
- [ ] `C-CN-12` `constraint` No camera frame is stored. `src: Constraints`
- [ ] `C-CN-13` `constraint` No background job queue is built. `src: Constraints`
- [ ] `C-CN-14` `constraint` No cache is built. `src: Constraints`
- [ ] `C-CN-15` `constraint` No search index is built. `src: Constraints`
- [ ] `C-CN-16` `constraint` No native mobile application is built. `src: Constraints`
- [ ] `C-CN-17` `literal` The app stays responsive at `4000` content pages. `src: Constraints`
- [ ] `C-CN-18` `literal` The app stays responsive at `500` enrolments. `src: Constraints`
- [ ] `C-CN-19` `literal` The app stays responsive at `1000` ledger entries. `src: Constraints`

## C-TR Technical requirements

- [ ] `C-TR-1` `contract` The backend is `Express` on Node 20. `src: Technical requirements`
- [ ] `C-TR-2` `contract` The JSON API is served on the same origin under `/api`. `src: Technical requirements`
- [ ] `C-TR-3` `contract` The front end is `Svelte + Vite`, compiled to a production bundle. `src: Technical requirements`
- [ ] `C-TR-4` `contract` The browser receives the application shell on first paint. `src: Technical requirements`
- [ ] `C-TR-5` `contract` Storage is PostgreSQL. `src: Technical requirements`
- [ ] `C-TR-6` `contract` Authentication is Keycloak. `src: Technical requirements`
- [ ] `C-TR-7` `constraint` No second database, cache, queue, object store, identity provider is introduced. `src: Technical requirements`
- [ ] `C-TR-8` `literal` PostgreSQL is reached at `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-9` `literal` Keycloak is reached at `AUTH_URL`. `src: Technical requirements`
- [ ] `C-TR-10` `literal` The Keycloak realm is `deku`. `src: Technical requirements`
- [ ] `C-TR-11` `literal` The Keycloak client is `proofworks`. `src: Technical requirements`
- [ ] `C-TR-12` `contract` Connection details are read from the environment, never hardcoded. `src: Technical requirements`
- [ ] `C-TR-13` `contract` The backing services are already running, never started by the app. `src: Technical requirements`
- [ ] `C-TR-14` `literal` `POST /api/auth/login` returns `access_token`, `account_id`, `role`. `src: Technical requirements`
- [ ] `C-TR-15` `literal` `GET /api/health` returns `200` with no credential once seeding has finished. `src: Technical requirements`
- [ ] `C-TR-16` `contract` Logs go to standard output, one line per request. `src: Technical requirements`
- [ ] `C-TR-17` `constraint` A log line never carries a password, a token, an email address, an answer key. `src: Technical requirements`
- [ ] `C-TR-18` `literal` No route's transferred script exceeds `250` kilobytes gzipped. `src: Technical requirements`
- [ ] `C-TR-19` `constraint` No database client or field enumeration ships to a browser bundle. `src: Technical requirements`
- [ ] `C-TR-20` `capability` The app serves what can be read when the database is briefly unreachable. `src: Technical requirements`
- [ ] `C-TR-21` `contract` Every authorization decision is made on the server from the account row. `src: Technical requirements`
- [ ] `C-TR-22` `constraint` No credential, key, token appears in anything the browser downloads. `src: Technical requirements`
- [ ] `C-TR-23` `constraint` The answer key for a question is served to nobody. `src: Technical requirements`
- [ ] `C-TR-24` `ui` Every public route carries its own title plus its own meta description. `src: Technical requirements`
- [ ] `C-TR-25` `constraint` No two public routes share a title. `src: Technical requirements`
- [ ] `C-TR-26` `ui` The site serves a favicon declared in the document head. `src: Technical requirements`
- [ ] `C-TR-27` `literal` Paging returns at most `25` items a page. `src: Technical requirements`
- [ ] `C-TR-28` `literal` The paging cursor is returned in the `X-Next-Cursor` response header. `src: Technical requirements`
- [ ] `C-TR-29` `constraint` Offset paging is used on no collection. `src: Technical requirements`
- [ ] `C-TR-30` `literal` Anything specific to one account is served `private, no-store`. `src: Technical requirements`
- [ ] `C-TR-31` `literal` The public catalogue is cacheable for `60` seconds. `src: Technical requirements`
- [ ] `C-TR-32` `literal` Rate limiting allows `600` mutating requests a minute per account. `src: Technical requirements`
- [ ] `C-TR-33` `constraint` A malformed body is rejected before anything is written. `src: Technical requirements`
- [ ] `C-TR-34` `constraint` A request carrying an unknown field is refused rather than ignored. `src: Technical requirements`
- [ ] `C-TR-35` `constraint` A failed enrolment leaves no orphaned enrolment row. `src: Technical requirements`
- [ ] `C-TR-36` `constraint` A failed issuance leaves no credential without a ledger entry. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-1` `data` The schema has twenty-six tables. `src: Data model`
- [ ] `C-DM-2` `data` All timestamps are UTC. `src: Data model`
- [ ] `C-DM-3` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model`
- [ ] `C-DM-4` `contract` The seeded password is written into `/app/USER_README.md` beside each account. `src: Data model`
- [ ] `C-DM-5` `data` `account` carries `id`, `email`, `display_name`, `username`, `country`, `proficiency`, `role`, `program_id`, `status`. `src: Data model`
- [ ] `C-DM-6` `data` `account.email` is unique. `src: Data model`
- [ ] `C-DM-7` `data` `account.username` is unique. `src: Data model`
- [ ] `C-DM-8` `constraint` `account.username` is checked against the reserved segment denylist. `src: Data model`
- [ ] `C-DM-9` `literal` `account.proficiency` takes `beginner`, `intermediate`, `advanced`. `src: Data model`
- [ ] `C-DM-10` `literal` `account.status` takes `enabled` or `disabled`. `src: Data model`
- [ ] `C-DM-11` `data` `partner` carries `id`, `name`, `slug`, `email_domain`. `src: Data model`
- [ ] `C-DM-12` `constraint` A partner slug can never take a reserved route segment. `src: Data model`
- [ ] `C-DM-13` `data` `partner_program` carries `treasury_total`, `treasury_remaining`, `treasury_spent`, `seat_cap`, `seats_granted`. `src: Data model`
- [ ] `C-DM-14` `literal` `partner_program.status` takes `active`, `suspended`, `terminated`. `src: Data model`
- [ ] `C-DM-15` `constraint` A suspended program stops new enrolments, leaving funded enrolments intact. `src: Data model`
- [ ] `C-DM-16` `constraint` After `ends_on` no new enrolment is funded. `src: Data model`
- [ ] `C-DM-17` `constraint` An assessment already in flight runs to its end after `ends_on`. `src: Data model`
- [ ] `C-DM-18` `literal` `discount_percent` is an integer from `0` to `100`. `src: Data model`
- [ ] `C-DM-19` `literal` `program_invite.status` takes `Pending`, `Sent`, `Accepted`. `src: Data model`
- [ ] `C-DM-20` `data` `chain` carries `id`, `name`, `slug`, `category`, `accent`, `order`. `src: Data model`
- [ ] `C-DM-21` `data` `course.identifier` is unique. `src: Data model`
- [ ] `C-DM-22` `literal` `module.project_type` takes `code` or `storyNode`. `src: Data model`
- [ ] `C-DM-23` `data` `enrolment` is unique on `(account_id, course_id)`. `src: Data model`
- [ ] `C-DM-24` `literal` `enrolment.entitlement_source` takes `free` or `program`. `src: Data model`
- [ ] `C-DM-25` `literal` `enrolment.status` takes `in_progress` or `complete`. `src: Data model`
- [ ] `C-DM-26` `data` `page_progress` is unique on `(account_id, page_id)`. `src: Data model`
- [ ] `C-DM-27` `data` `assessment` is unique on `(account_id, module_id)`. `src: Data model`
- [ ] `C-DM-28` `literal` `exam.status` takes `InProgress`, `Passed`, `Suspicious`, `Failed`. `src: Data model`
- [ ] `C-DM-29` `data` `exam.attempt_number` counts the attempts on one module for one account. `src: Data model`
- [ ] `C-DM-30` `data` `exam.question_seed` fixes which questions are served, in what order. `src: Data model`
- [ ] `C-DM-31` `constraint` `project.approved_by` is never the project's own `account_id`. `src: Data model`
- [ ] `C-DM-32` `data` `credential` is unique on `(account_id, course_id, module_id)`. `src: Data model`
- [ ] `C-DM-33` `literal` `credential.status` takes `issued` or `revoked`. `src: Data model`
- [ ] `C-DM-34` `data` `credential.module_ids` holds every module the credential attests. `src: Data model`
- [ ] `C-DM-35` `constraint` `ledger_entry` is append only, never updated, never deleted. `src: Data model`
- [ ] `C-DM-36` `literal` `ledger_entry.kind` takes `issuance` or `revocation`. `src: Data model`
- [ ] `C-DM-37` `data` `ledger_entry.ledger_ref` is unique. `src: Data model`
- [ ] `C-DM-38` `constraint` Exactly one `issuance` entry exists per credential. `src: Data model`
- [ ] `C-DM-39` `constraint` `reward.quota_claimed` never exceeds `reward.quota_total`. `src: Data model`
- [ ] `C-DM-40` `data` `reward_earn` is unique on `(reward_id, account_id)`. `src: Data model`
- [ ] `C-DM-41` `literal` `bounty.kind` takes `job` or `levelUp`. `src: Data model`
- [ ] `C-DM-42` `data` `announcement` with a null `program_id` is public. `src: Data model`
- [ ] `C-DM-43` `data` `idempotency_key` is unique on `(account_id, key)`. `src: Data model`
- [ ] `C-DM-44` `literal` `erasure_request.status` takes `requested`, `cancelled`, `executed`. `src: Data model`
- [ ] `C-DM-45` `data` `enrolment.course_progress` is derived from the pages marked complete. `src: Data model`
- [ ] `C-DM-46` `data` A module's completion is derived from its pages rather than held in a column. `src: Data model`
- [ ] `C-DM-47` `data` Seven chains are seeded. `src: Data model`
- [ ] `C-DM-48` `data` Seven courses are seeded. `src: Data model`
- [ ] `C-DM-49` `literal` `solana-intern` carries `first_paywalled_module` `1`. `src: Data model`
- [ ] `C-DM-50` `data` `solana-intern` carries the modules `solana-intern-basics`, `solana-intern-programs`. `src: Data model`
- [ ] `C-DM-51` `data` `solidity-beginner-story` carries `project_type` `storyNode` with `disable_project` true. `src: Data model`
- [ ] `C-DM-52` `data` Each seeded module carries two lessons; each lesson carries four pages. `src: Data model`
- [ ] `C-DM-53` `data` Partners `Northgate Institute`, `Halcyon Labs` are seeded. `src: Data model`
- [ ] `C-DM-54` `literal` `Halcyon Cohort 2026` holds `treasury_remaining` `50000`. `src: Data model`
- [ ] `C-DM-55` `data` `learner@example.com` is already enrolled in `solidity-beginner`. `src: Data model`
- [ ] `C-DM-56` `literal` `solana-intern-basics` carries three `MultipleChoice` questions. `src: Data model`
- [ ] `C-DM-57` `data` Reward `Founding Artisan` is seeded with `quota_total` `1`. `src: Data model`
- [ ] `C-DM-58` `data` Bounty `Audit a Vault` is seeded with `requires_credential` true. `src: Data model`
- [ ] `C-DM-59` `constraint` Seeding is idempotent, so restarting duplicates no row. `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-1` `ui` Navigation is a persistent left sidebar on every signed-in route. `src: Front-end specification`
- [ ] `C-FE-2` `literal` The sidebar carries `Courses`, `Bounties`, `Houses`, `AI Creations`. `src: Front-end specification`
- [ ] `C-FE-3` `ui` The review board appears only for the roles holding the board. `src: Front-end specification`
- [ ] `C-FE-4` `ui` A breadcrumb sits above the sidebar. `src: Front-end specification`
- [ ] `C-FE-5` `ui` The header carries the brand mark, a chain switcher, an announcements bell, the account control. `src: Front-end specification`
- [ ] `C-FE-6` `ui` `/review` is a board of one column per state. `src: Front-end specification`
- [ ] `C-FE-7` `ui` Creating a partner program is a wizard across three of its own addresses. `src: Front-end specification`
- [ ] `C-FE-8` `capability` Wizard step two invites seats from a pasted CSV of email addresses. `src: Front-end specification`
- [ ] `C-FE-9` `ui` The CSV preview carries a per-row error report naming the line plus the reason. `src: Front-end specification`
- [ ] `C-FE-10` `constraint` CSV seats are written only when the registrar confirms the preview. `src: Front-end specification`
- [ ] `C-FE-11` `ui` A card moves to its new column at once, reverting with a reason on refusal. `src: Front-end specification`
- [ ] `C-FE-12` `ui` The ground plus its surfaces are four ordered deep cool neutral steps. `src: Front-end specification`
- [ ] `C-FE-13` `ui` Each ground step sits an even distance in luminance above the step below. `src: Front-end specification`
- [ ] `C-FE-14` `literal` `honey-gold-light` is a near-white muted amber, used for primary text. `src: Front-end specification`
- [ ] `C-FE-15` `literal` `honey-gold-dark` is a light soft amber, used for the pressed state. `src: Front-end specification`
- [ ] `C-FE-16` `literal` `signal green` is a mid vivid green, used on the public catalogue only. `src: Front-end specification`
- [ ] `C-FE-17` `literal` `magenta glow` is a mid vivid violet, used once as a box shadow. `src: Front-end specification`
- [ ] `C-FE-18` `ui` Semantic colour is rationed to four meanings. `src: Front-end specification`
- [ ] `C-FE-19` `ui` Each semantic colour carries a second signal beside the colour. `src: Front-end specification`
- [ ] `C-FE-20` `ui` Five chain accents appear only on the chain badge. `src: Front-end specification`
- [ ] `C-FE-21` `ui` The mid warm neutral border is never a text colour. `src: Front-end specification`
- [ ] `C-FE-22` `literal` The display fallback stack is `"Trajan Pro", Optima, Palatino, Georgia, serif`. `src: Front-end specification`
- [ ] `C-FE-23` `literal` The body fallback stack begins `ui-sans-serif, system-ui, -apple-system`. `src: Front-end specification`
- [ ] `C-FE-24` `literal` The type scale is `10px`, `12px`, `14px`, `16px`, `20px`, `24px`, `40px`. `src: Front-end specification`
- [ ] `C-FE-25` `ui` Numerals align in columns wherever scores stack. `src: Front-end specification`
- [ ] `C-FE-26` `ui` Spacing runs on a single small base unit doubling through an ordered ramp. `src: Front-end specification`
- [ ] `C-FE-27` `ui` Radius has four steps. `src: Front-end specification`
- [ ] `C-FE-28` `ui` Elevation is carried by two drop shadows only. `src: Front-end specification`
- [ ] `C-FE-29` `ui` Locked content dims progressively rather than disappearing. `src: Front-end specification`
- [ ] `C-FE-30` `ui` The frame carries variants card, module, module-title, video-preview, circular, toast, offer. `src: Front-end specification`
- [ ] `C-FE-31` `ui` The frame carries tones gold, dark, double. `src: Front-end specification`
- [ ] `C-FE-32` `ui` The frame carries states default, selected, locked, failed. `src: Front-end specification`
- [ ] `C-FE-33` `ui` The reader is a single column with a lesson rail plus a context rail. `src: Front-end specification`
- [ ] `C-FE-34` `ui` At tablet width the rails move into drawers. `src: Front-end specification`
- [ ] `C-FE-35` `ui` At phone width a sticky bottom bar carries previous, next, mark complete. `src: Front-end specification`
- [ ] `C-FE-36` `ui` The reader loading state is a skeleton matching the final layout metrics. `src: Front-end specification`
- [ ] `C-FE-37` `ui` The paywalled state shows a teaser with the lesson rail still visible. `src: Front-end specification`
- [ ] `C-FE-38` `constraint` The paywalled body text is absent rather than blurred. `src: Front-end specification`
- [ ] `C-FE-39` `ui` The reader not-found panel keeps the rails plus the place. `src: Front-end specification`
- [ ] `C-FE-40` `capability` The last page of a lesson advances to the first page of the next lesson. `src: Front-end specification`
- [ ] `C-FE-41` `capability` The last page of the last lesson advances to the assessment gate. `src: Front-end specification`
- [ ] `C-FE-42` `constraint` Page navigation never advances to the site root. `src: Front-end specification`
- [ ] `C-FE-43` `ui` The dashboard leads with the course in flight. `src: Front-end specification`
- [ ] `C-FE-44` `capability` The dashboard recommends a next course from the recorded proficiency. `src: Front-end specification`
- [ ] `C-FE-45` `ui` A course with an unmet prerequisite names the unmet prerequisite. `src: Front-end specification`
- [ ] `C-FE-46` `constraint` Nothing ships as a binary asset. `src: Front-end specification`
- [ ] `C-FE-47` `ui` The parchment ground is a drawn grain over the deep cool neutral ground. `src: Front-end specification`
- [ ] `C-FE-48` `ui` A chain badge is a lettermark tile in the display face on that chain's accent. `src: Front-end specification`
- [ ] `C-FE-49` `ui` The wordmark is drawn in the display voice as capitals, tracked open. `src: Front-end specification`
- [ ] `C-FE-50` `ui` A review card shows the Artisan, the module, the waiting time, the funding program. `src: Front-end specification`
- [ ] `C-FE-51` `ui` A card opens to a detail route showing the repository address beside the module brief. `src: Front-end specification`
- [ ] `C-FE-52` `ui` The board is operable from the keyboard alone. `src: Front-end specification`
- [ ] `C-FE-53` `literal` The public catalogue leads with `Where devs learn web3, earn rewards, land a job.` `src: Front-end specification`
- [ ] `C-FE-54` `literal` The public catalogue primary action reads `Start Learning`. `src: Front-end specification`
- [ ] `C-FE-55` `literal` The value block heads `Invest in skills you need to succeed`. `src: Front-end specification`
- [ ] `C-FE-56` `literal` The dashboard salutation reads `Welcome, ARTISAN.` `src: Front-end specification`
- [ ] `C-FE-57` `ui` A free course overview asks the reader to confirm the start of the course. `src: Front-end specification`
- [ ] `C-FE-58` `ui` A paid course overview asks the reader to confirm the purchase of the course. `src: Front-end specification`
- [ ] `C-FE-59` `literal` Enrolment success reads `Successfully registered for course!` `src: Front-end specification`
- [ ] `C-FE-60` `ui` An empty reward list names the absence of a reward for the course. `src: Front-end specification`
- [ ] `C-FE-61` `literal` The footer carries `Terms of Service`, `Privacy Policy`, `Cookie Policy`, `Manage Cookies`. `src: Front-end specification`
- [ ] `C-FE-62` `ui` The sidebar collapses behind one control at tablet width. `src: Front-end specification`
- [ ] `C-FE-63` `ui` The sidebar becomes a full-height panel over the page at phone width. `src: Front-end specification`
- [ ] `C-FE-64` `ui` Opening the phone panel traps focus, restoring the page scroll on close. `src: Front-end specification`
- [ ] `C-FE-65` `ui` The board goes from three columns to one at phone width. `src: Front-end specification`
- [ ] `C-FE-66` `ui` Type steps at the tier switches rather than scaling continuously. `src: Front-end specification`
- [ ] `C-FE-67` `constraint` No route's phone height exceeds twice its desktop height. `src: Front-end specification`
- [ ] `C-FE-68` `ui` Focus order follows reading order on every route. `src: Front-end specification`
- [ ] `C-FE-69` `ui` The assessment flow is completable end to end without a pointer. `src: Front-end specification`
- [ ] `C-FE-70` `ui` Every content image carries alternative text. `src: Front-end specification`

## C-DC Deployment contract

- [ ] `C-DC-1` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-2` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-3` `contract` Both the port plus the address are read from the environment. `src: Deployment contract`
- [ ] `C-DC-4` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-5` `literal` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract`
- [ ] `C-DC-6` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-7` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-8` `contract` Reserved `.browser_screenshots/` plus `.downloads/` directories exist at the app root, empty. `src: Deployment contract`
- [ ] `C-DC-9` `contract` A production build is served behind a static or preview server. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends. `src: Deployment contract`
- [ ] `C-DC-11` `contract` The server is not a child of the shell. `src: Deployment contract`
- [ ] `C-DC-12` `literal` The server binds `0.0.0.0`. `src: Deployment contract`
- [ ] `C-DC-13` `contract` No backing service is downloaded, installed, compiled or started by the app. `src: Deployment contract`
- [ ] `C-DC-14` `constraint` No edge function is used. `src: Deployment contract`
- [ ] `C-DC-15` `constraint` No persistent volume, fixed container name, custom network is declared. `src: Deployment contract`
- [ ] `C-DC-16` `literal` `GET /api/me` returns the caller's `id`, `email`, `role`, `program_id`. `src: Deployment contract, API shapes`
- [ ] `C-DC-17` `literal` `GET /api/catalogue` returns a top-level array of course records. `src: Deployment contract, API shapes`
- [ ] `C-DC-18` `literal` `POST /api/enrolments` takes `course_id` plus `program_id`. `src: Deployment contract, API shapes`
- [ ] `C-DC-19` `literal` `POST /api/pages/{page_id}/progress` returns `course_progress`. `src: Deployment contract, API shapes`
- [ ] `C-DC-20` `literal` `POST /api/assessments/{module_id}/consent` takes the three consent flags. `src: Deployment contract, API shapes`
- [ ] `C-DC-21` `literal` `POST /api/assessments/{module_id}/exam` returns `exam_id`, `ends_at`, `questions`. `src: Deployment contract, API shapes`
- [ ] `C-DC-22` `literal` `POST /api/exams/{exam_id}/events` takes `kind` plus `occurred_at`. `src: Deployment contract, API shapes`
- [ ] `C-DC-23` `literal` `POST /api/exams/{exam_id}/submit` returns `status`, `result_percent`, `assessment_status`. `src: Deployment contract, API shapes`
- [ ] `C-DC-24` `literal` `POST /api/projects` takes `assessment_id`, `repo_url`, `demo_url`. `src: Deployment contract, API shapes`
- [ ] `C-DC-25` `literal` `POST /api/projects/{project_id}/approve` returns `status`, `approved_by`. `src: Deployment contract, API shapes`
- [ ] `C-DC-26` `literal` `POST /api/credentials` takes `assessment_id`, returning `ledger_ref`. `src: Deployment contract, API shapes`
- [ ] `C-DC-27` `literal` `POST /api/credentials/{credential_id}/revoke` takes a `reason`. `src: Deployment contract, API shapes`
- [ ] `C-DC-28` `literal` `GET /api/ledger` returns a top-level array of ledger entries. `src: Deployment contract, API shapes`
- [ ] `C-DC-29` `literal` `POST /api/rewards/{reward_id}/claim` returns `status`, `expires_at`. `src: Deployment contract, API shapes`
- [ ] `C-DC-30` `literal` `GET /api/programs` returns `treasury_total`, `treasury_remaining`, `seats_granted`. `src: Deployment contract, API shapes`
- [ ] `C-DC-31` `literal` `POST /api/bounties/{bounty_id}/applications` returns `bounty_id` plus `status`. `src: Deployment contract, API shapes`
- [ ] `C-DC-32` `literal` `GET /api/cookie-choice` returns `accepted` plus `recorded_at`. `src: Deployment contract, API shapes`
- [ ] `C-DC-33` `constraint` Every list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes`
- [ ] `C-DC-34` `constraint` An invalid or unauthorized call is rejected as a client error. `src: Deployment contract, API shapes`
- [ ] `C-DC-35` `constraint` An invalid call never returns a `5xx`. `src: Deployment contract, API shapes`
- [ ] `C-DC-36` `constraint` PostgreSQL plus Keycloak are the facts behind the interface. `src: Deployment contract, No mocks`
- [ ] `C-DC-37` `constraint` An in-memory accounts dictionary is a contract violation. `src: Deployment contract, No mocks`
- [ ] `C-DC-38` `constraint` A token the app signed for itself is a contract violation. `src: Deployment contract, No mocks`
- [ ] `C-DC-39` `constraint` A ledger kept in process memory is a contract violation. `src: Deployment contract, No mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `Ready to start this course?` | the free-course start confirmation copy | `C-FE-57` | Front-end specification, Pinned copy |
| `Ready to buy this course?` | the paid-course purchase confirmation copy | `C-FE-58` | Front-end specification, Pinned copy |
| `No rewards for this course!` | the empty reward list copy | `C-FE-60` | Front-end specification, Pinned copy |
| `We recommend finishing the course you have already started so you can get rewarded.` | the course-in-flight recommendation copy | `C-CF-42` | Core features, enrolment rule 6 |
| `Your 30-day countdown timer for completing and claiming any bonus rewards will begin as soon as you purchase the course.` | the reward-window countdown copy | `C-CF-133` | Core features, rewards rule 2 |
| `{credential_id}/{account_id}/{course_id}/{module_id}/{issued_at}` | the pipe-joined canonical issuance payload | `C-CF-104` | Core features, credential rule 3 |
| `deku-demo-pw-2026` | Every seeded account uses the password deku-demo-pw-2026 | `C-RL-2` | User roles |
| `learner@example.com` | The seeded learners are learner@example.com, learner2@example.co... | `C-RL-30` | User roles |
| `learner2@example.com` | The seeded learners are learner@example.com, learner2@example.co... | `C-RL-30` | User roles |
| `learner3@example.com` | The seeded learners are learner@example.com, learner2@example.co... | `C-RL-30` | User roles |
| `reviewer@example.com` | The seeded reviewer is reviewer@example.com | `C-RL-31` | User roles |
| `registrar@example.com` | The seeded registrar is registrar@example.com | `C-RL-32` | User roles |
| `/content/{course_id}/{module_id}/{lesson_id}/{page_id}` | A page is addressable at /content/{course_id}/{module_id}/{lesson_... | `C-CF-8` | Core features, catalogue rule 1 |
| `first_paywalled_module` | first_paywalled_module null means the whole course is free | `C-CF-20` | Core features, entitlement rule 1 |
| `0` | first_paywalled_module 0 means the whole course is paid | `C-CF-21` | Core features, entitlement rule 1 |
| `entitlement_source` | A funded enrolment sets entitlement_source to program | `C-CF-31` | Core features, enrolment rule 2 |
| `program` | A funded enrolment sets entitlement_source to program | `C-CF-31` | Core features, enrolment rule 2 |
| `assessment.status` | assessment.status takes PreAssessment, Exam, ExamReview, P... | `C-CF-44` | Core features, assessment rule 1 |
| `PreAssessment` | assessment.status takes PreAssessment, Exam, ExamReview, P... | `C-CF-44` | Core features, assessment rule 1 |
| `Exam` | assessment.status takes PreAssessment, Exam, ExamReview, P... | `C-CF-44` | Core features, assessment rule 1 |
| `ExamReview` | assessment.status takes PreAssessment, Exam, ExamReview, P... | `C-CF-44` | Core features, assessment rule 1 |
| `Project` | assessment.status takes PreAssessment, Exam, ExamReview, P... | `C-CF-44` | Core features, assessment rule 1 |
| `ProjectReview` | assessment.status takes PreAssessment, Exam, ExamReview, P... | `C-CF-44` | Core features, assessment rule 1 |
| `Completed` | assessment.status takes PreAssessment, Exam, ExamReview, P... | `C-CF-44` | Core features, assessment rule 1 |
| `result_percent` | ExamReview advances to Project at a result_percent of 70 or... | `C-CF-53` | Core features, assessment rule 5 |
| `70` | ExamReview advances to Project at a result_percent of 70 or... | `C-CF-53` | Core features, assessment rule 5 |
| `exam.status` | A passing auto-grade sets exam.status to Passed | `C-CF-54` | Core features, assessment rule 5 |
| `Passed` | A passing auto-grade sets exam.status to Passed | `C-CF-54` | Core features, assessment rule 5 |
| `Failed` | A failing auto-grade sets exam.status to Failed | `C-CF-56` | Core features, assessment rule 6 |
| `300` | A retake of one module is refused for 300 seconds after a failure | `C-CF-57` | Core features, assessment rule 6 |
| `Suspicious` | Proctor signals above the threshold set exam.status to Suspicious | `C-CF-58` | Core features, assessment rule 7 |
| `exam.ends_at` | exam.ends_at is 1800 seconds after started_at | `C-CF-69` | Core features, proctored rule 1 |
| `1800` | exam.ends_at is 1800 seconds after started_at | `C-CF-69` | Core features, proctored rule 1 |
| `started_at` | exam.ends_at is 1800 seconds after started_at | `C-CF-69` | Core features, proctored rule 1 |
| `exam.timeout_source` | exam.timeout_source records Browser or Server | `C-CF-72` | Core features, proctored rule 1 |
| `Browser` | exam.timeout_source records Browser or Server | `C-CF-72` | Core features, proctored rule 1 |
| `Server` | exam.timeout_source records Browser or Server | `C-CF-72` | Core features, proctored rule 1 |
| `exam_question.kind` | exam_question.kind takes MultipleChoice or MultipleChoiceCode | `C-CF-74` | Core features, proctored rule 2 |
| `MultipleChoice` | exam_question.kind takes MultipleChoice or MultipleChoiceCode | `C-CF-74` | Core features, proctored rule 2 |
| `MultipleChoiceCode` | exam_question.kind takes MultipleChoice or MultipleChoiceCode | `C-CF-74` | Core features, proctored rule 2 |
| `proctor_event.kind` | proctor_event.kind takes AnswerSubmitted, OffFocus, OnFocus... | `C-CF-76` | Core features, proctored rule 3 |
| `AnswerSubmitted` | proctor_event.kind takes AnswerSubmitted, OffFocus, OnFocus... | `C-CF-76` | Core features, proctored rule 3 |
| `OffFocus` | proctor_event.kind takes AnswerSubmitted, OffFocus, OnFocus... | `C-CF-76` | Core features, proctored rule 3 |
| `OnFocus` | proctor_event.kind takes AnswerSubmitted, OffFocus, OnFocus... | `C-CF-76` | Core features, proctored rule 3 |
| `NoFaceDetected` | proctor_event.kind takes AnswerSubmitted, OffFocus, OnFocus... | `C-CF-76` | Core features, proctored rule 3 |
| `MultipleFaceDetected` | proctor_event.kind takes AnswerSubmitted, OffFocus, OnFocus... | `C-CF-76` | Core features, proctored rule 3 |
| `FaceResolved` | proctor_event.kind takes AnswerSubmitted, OffFocus, OnFocus... | `C-CF-76` | Core features, proctored rule 3 |
| `TestStarted` | proctor_event.kind takes AnswerSubmitted, OffFocus, OnFocus... | `C-CF-76` | Core features, proctored rule 3 |
| `TestResumed` | proctor_event.kind takes AnswerSubmitted, OffFocus, OnFocus... | `C-CF-76` | Core features, proctored rule 3 |
| `TestSubmitted` | proctor_event.kind takes AnswerSubmitted, OffFocus, OnFocus... | `C-CF-76` | Core features, proctored rule 3 |
| `exam.proctoring_mode` | exam.proctoring_mode records full, degraded or none | `C-CF-82` | Core features, proctored rule 5 |
| `full` | exam.proctoring_mode records full, degraded or none | `C-CF-82` | Core features, proctored rule 5 |
| `degraded` | exam.proctoring_mode records full, degraded or none | `C-CF-82` | Core features, proctored rule 5 |
| `none` | exam.proctoring_mode records full, degraded or none | `C-CF-82` | Core features, proctored rule 5 |
| `project.status` | project.status takes InProgress, InReview, Approved | `C-CF-94` | Core features, project rule 4 |
| `InProgress` | project.status takes InProgress, InReview, Approved | `C-CF-94` | Core features, project rule 4 |
| `InReview` | project.status takes InProgress, InReview, Approved | `C-CF-94` | Core features, project rule 4 |
| `Approved` | project.status takes InProgress, InReview, Approved | `C-CF-94` | Core features, project rule 4 |
| `GET /api/credentials/proof/{ledger_ref}` | GET /api/credentials/proof/{ledger_ref} needs no credential | `C-CF-108` | Core features, credential rule 5 |
| `reward.kind` | reward.kind takes nft, coupon, token, fiat | `C-CF-118` | Core features, rewards rule 1 |
| `nft` | reward.kind takes nft, coupon, token, fiat | `C-CF-118` | Core features, rewards rule 1 |
| `coupon` | reward.kind takes nft, coupon, token, fiat | `C-CF-118` | Core features, rewards rule 1 |
| `token` | reward.kind takes nft, coupon, token, fiat | `C-CF-118` | Core features, rewards rule 1 |
| `fiat` | reward.kind takes nft, coupon, token, fiat | `C-CF-118` | Core features, rewards rule 1 |
| `reward_earn.status` | reward_earn.status takes in_progress, redeemed, expired | `C-CF-119` | Core features, rewards rule 1 |
| `in_progress` | reward_earn.status takes in_progress, redeemed, expired | `C-CF-119` | Core features, rewards rule 1 |
| `redeemed` | reward_earn.status takes in_progress, redeemed, expired | `C-CF-119` | Core features, rewards rule 1 |
| `expired` | reward_earn.status takes in_progress, redeemed, expired | `C-CF-119` | Core features, rewards rule 1 |
| `bounty.status` | bounty.status takes open, work_started, submissions, concl... | `C-CF-132` | Core features, bounties rule 1 |
| `open` | bounty.status takes open, work_started, submissions, concl... | `C-CF-132` | Core features, bounties rule 1 |
| `work_started` | bounty.status takes open, work_started, submissions, concl... | `C-CF-132` | Core features, bounties rule 1 |
| `submissions` | bounty.status takes open, work_started, submissions, concl... | `C-CF-132` | Core features, bounties rule 1 |
| `concluded` | bounty.status takes open, work_started, submissions, concl... | `C-CF-132` | Core features, bounties rule 1 |
| `canceled` | bounty.status takes open, work_started, submissions, concl... | `C-CF-132` | Core features, bounties rule 1 |
| `bounty_application.status` | bounty_application.status takes viewed, bookmarked, applied... | `C-CF-133` | Core features, bounties rule 1 |
| `viewed` | bounty_application.status takes viewed, bookmarked, applied... | `C-CF-133` | Core features, bounties rule 1 |
| `bookmarked` | bounty_application.status takes viewed, bookmarked, applied... | `C-CF-133` | Core features, bounties rule 1 |
| `applied` | bounty_application.status takes viewed, bookmarked, applied... | `C-CF-133` | Core features, bounties rule 1 |
| `accepted` | bounty_application.status takes viewed, bookmarked, applied... | `C-CF-133` | Core features, bounties rule 1 |
| `rejected` | bounty_application.status takes viewed, bookmarked, applied... | `C-CF-133` | Core features, bounties rule 1 |
| `submitted` | bounty_application.status takes viewed, bookmarked, applied... | `C-CF-133` | Core features, bounties rule 1 |
| `90` | Proctor events are kept for 90 days from the attempt | `C-CF-143` | Core features, consent rule 3 |
| `RateLimit-Limit` | A response carries RateLimit-Limit, RateLimit-Remaining, RateL... | `C-CF-160` | Core features, money rule 4 |
| `RateLimit-Remaining` | A response carries RateLimit-Limit, RateLimit-Remaining, RateL... | `C-CF-160` | Core features, money rule 4 |
| `RateLimit-Reset` | A response carries RateLimit-Limit, RateLimit-Remaining, RateL... | `C-CF-160` | Core features, money rule 4 |
| `Retry-After` | A refused rate-limited request carries Retry-After | `C-CF-161` | Core features, money rule 4 |
| `/` | / serves the public catalogue of chains plus courses | `C-UF-1` | User flow table |
| `/proof/<ledger_ref>` | /proof/<ledger_ref> serves the public credential proof page | `C-UF-2` | User flow table |
| `/privacy` | /privacy serves the privacy page | `C-UF-3` | User flow table |
| `/login` | /login serves sign-in | `C-UF-4` | User flow table |
| `/home` | /home serves the Artisan dashboard | `C-UF-5` | User flow table |
| `/courses/<chain_id>` | /courses/<chain_id> serves one chain's courses | `C-UF-6` | User flow table |
| `/content/<course_id>` | /content/<course_id> serves the course overview | `C-UF-7` | User flow table |
| `/content/<course_id>/<module_id>/<lesson_id>/<page_id>` | /content/<course_id>/<module_id>/<lesson_id>/<page_id> serves the... | `C-UF-8` | User flow table |
| `/content/<course_id>/<module_id>/assessment` | /content/<course_id>/<module_id>/assessment serves the gate plus ... | `C-UF-9` | User flow table |
| `/content/<course_id>/<module_id>/assessment/exam` | /content/<course_id>/<module_id>/assessment/exam serves the timed... | `C-UF-10` | User flow table |
| `/content/<course_id>/<module_id>/assessment/project` | /content/<course_id>/<module_id>/assessment/project serves projec... | `C-UF-11` | User flow table |
| `/credentials` | /credentials serves the learner's own credentials | `C-UF-12` | User flow table |
| `/bounties` | /bounties serves the bounty board | `C-UF-13` | User flow table |
| `/review` | /review serves the review board | `C-UF-14` | User flow table |
| `/review/<project_id>` | /review/<project_id> serves one project under review | `C-UF-15` | User flow table |
| `/registrar` | /registrar serves the issuance board | `C-UF-16` | User flow table |
| `/programs` | /programs serves programs, rosters, treasuries | `C-UF-17` | User flow table |
| `/programs/new` | /programs/new serves wizard step one | `C-UF-18` | User flow table |
| `/programs/new/seats` | /programs/new/seats serves wizard step two | `C-UF-19` | User flow table |
| `/programs/new/review` | /programs/new/review serves wizard step three | `C-UF-20` | User flow table |
| `Alexon` | The display face is Alexon | `C-UX-16` | UI/UX notes |
| `CircularXX` | The body face is CircularXX | `C-UX-17` | UI/UX notes |
| `14px` | Code never renders below 14px | `C-UX-18` | UI/UX notes |
| `4000` | The app stays responsive at 4000 content pages | `C-CN-17` | Constraints |
| `500` | The app stays responsive at 500 enrolments | `C-CN-18` | Constraints |
| `1000` | The app stays responsive at 1000 ledger entries | `C-CN-19` | Constraints |
| `DATABASE_URL` | PostgreSQL is reached at DATABASE_URL | `C-TR-8` | Technical requirements |
| `AUTH_URL` | Keycloak is reached at AUTH_URL | `C-TR-9` | Technical requirements |
| `deku` | The Keycloak realm is deku | `C-TR-10` | Technical requirements |
| `proofworks` | The Keycloak client is proofworks | `C-TR-11` | Technical requirements |
| `POST /api/auth/login` | POST /api/auth/login returns access_token, account_id, role | `C-TR-14` | Technical requirements |
| `access_token` | POST /api/auth/login returns access_token, account_id, role | `C-TR-14` | Technical requirements |
| `account_id` | POST /api/auth/login returns access_token, account_id, role | `C-TR-14` | Technical requirements |
| `role` | POST /api/auth/login returns access_token, account_id, role | `C-TR-14` | Technical requirements |
| `GET /api/health` | GET /api/health returns 200 with no credential once seeding has... | `C-TR-15` | Technical requirements |
| `200` | GET /api/health returns 200 with no credential once seeding has... | `C-TR-15` | Technical requirements |
| `250` | No route's transferred script exceeds 250 kilobytes gzipped | `C-TR-18` | Technical requirements |
| `25` | Paging returns at most 25 items a page | `C-TR-27` | Technical requirements |
| `X-Next-Cursor` | The paging cursor is returned in the X-Next-Cursor response header | `C-TR-28` | Technical requirements |
| `private, no-store` | Anything specific to one account is served private, no-store | `C-TR-30` | Technical requirements |
| `60` | The public catalogue is cacheable for 60 seconds | `C-TR-31` | Technical requirements |
| `600` | Rate limiting allows 600 mutating requests a minute per account | `C-TR-32` | Technical requirements |
| `account.proficiency` | account.proficiency takes beginner, intermediate, advanced | `C-DM-9` | Data model |
| `beginner` | account.proficiency takes beginner, intermediate, advanced | `C-DM-9` | Data model |
| `intermediate` | account.proficiency takes beginner, intermediate, advanced | `C-DM-9` | Data model |
| `advanced` | account.proficiency takes beginner, intermediate, advanced | `C-DM-9` | Data model |
| `account.status` | account.status takes enabled or disabled | `C-DM-10` | Data model |
| `enabled` | account.status takes enabled or disabled | `C-DM-10` | Data model |
| `disabled` | account.status takes enabled or disabled | `C-DM-10` | Data model |
| `partner_program.status` | partner_program.status takes active, suspended, terminated | `C-DM-14` | Data model |
| `active` | partner_program.status takes active, suspended, terminated | `C-DM-14` | Data model |
| `suspended` | partner_program.status takes active, suspended, terminated | `C-DM-14` | Data model |
| `terminated` | partner_program.status takes active, suspended, terminated | `C-DM-14` | Data model |
| `discount_percent` | discount_percent is an integer from 0 to 100 | `C-DM-18` | Data model |
| `100` | discount_percent is an integer from 0 to 100 | `C-DM-18` | Data model |
| `program_invite.status` | program_invite.status takes Pending, Sent, Accepted | `C-DM-19` | Data model |
| `Pending` | program_invite.status takes Pending, Sent, Accepted | `C-DM-19` | Data model |
| `Sent` | program_invite.status takes Pending, Sent, Accepted | `C-DM-19` | Data model |
| `Accepted` | program_invite.status takes Pending, Sent, Accepted | `C-DM-19` | Data model |
| `module.project_type` | module.project_type takes code or storyNode | `C-DM-22` | Data model |
| `code` | module.project_type takes code or storyNode | `C-DM-22` | Data model |
| `storyNode` | module.project_type takes code or storyNode | `C-DM-22` | Data model |
| `enrolment.entitlement_source` | enrolment.entitlement_source takes free or program | `C-DM-24` | Data model |
| `free` | enrolment.entitlement_source takes free or program | `C-DM-24` | Data model |
| `enrolment.status` | enrolment.status takes in_progress or complete | `C-DM-25` | Data model |
| `complete` | enrolment.status takes in_progress or complete | `C-DM-25` | Data model |
| `credential.status` | credential.status takes issued or revoked | `C-DM-33` | Data model |
| `issued` | credential.status takes issued or revoked | `C-DM-33` | Data model |
| `revoked` | credential.status takes issued or revoked | `C-DM-33` | Data model |
| `ledger_entry.kind` | ledger_entry.kind takes issuance or revocation | `C-DM-36` | Data model |
| `issuance` | ledger_entry.kind takes issuance or revocation | `C-DM-36` | Data model |
| `revocation` | ledger_entry.kind takes issuance or revocation | `C-DM-36` | Data model |
| `bounty.kind` | bounty.kind takes job or levelUp | `C-DM-41` | Data model |
| `job` | bounty.kind takes job or levelUp | `C-DM-41` | Data model |
| `levelUp` | bounty.kind takes job or levelUp | `C-DM-41` | Data model |
| `erasure_request.status` | erasure_request.status takes requested, cancelled, executed | `C-DM-44` | Data model |
| `requested` | erasure_request.status takes requested, cancelled, executed | `C-DM-44` | Data model |
| `cancelled` | erasure_request.status takes requested, cancelled, executed | `C-DM-44` | Data model |
| `executed` | erasure_request.status takes requested, cancelled, executed | `C-DM-44` | Data model |
| `solana-intern` | solana-intern carries first_paywalled_module 1 | `C-DM-49` | Data model |
| `1` | solana-intern carries first_paywalled_module 1 | `C-DM-49` | Data model |
| `Halcyon Cohort 2026` | Halcyon Cohort 2026 holds treasury_remaining 50000 | `C-DM-54` | Data model |
| `treasury_remaining` | Halcyon Cohort 2026 holds treasury_remaining 50000 | `C-DM-54` | Data model |
| `50000` | Halcyon Cohort 2026 holds treasury_remaining 50000 | `C-DM-54` | Data model |
| `solana-intern-basics` | solana-intern-basics carries three MultipleChoice questions | `C-DM-56` | Data model |
| `Courses` | The sidebar carries Courses, Bounties, Houses, AI Creations | `C-FE-2` | Front-end specification |
| `Bounties` | The sidebar carries Courses, Bounties, Houses, AI Creations | `C-FE-2` | Front-end specification |
| `Houses` | The sidebar carries Courses, Bounties, Houses, AI Creations | `C-FE-2` | Front-end specification |
| `AI Creations` | The sidebar carries Courses, Bounties, Houses, AI Creations | `C-FE-2` | Front-end specification |
| `honey-gold-light` | honey-gold-light is a near-white muted amber, used for primary text | `C-FE-14` | Front-end specification |
| `honey-gold-dark` | honey-gold-dark is a light soft amber, used for the pressed state | `C-FE-15` | Front-end specification |
| `signal green` | signal green is a mid vivid green, used on the public catalogue only | `C-FE-16` | Front-end specification |
| `magenta glow` | magenta glow is a mid vivid violet, used once as a box shadow | `C-FE-17` | Front-end specification |
| `"Trajan Pro", Optima, Palatino, Georgia, serif` | The display fallback stack is "Trajan Pro", Optima, Palatino, Geor... | `C-FE-22` | Front-end specification |
| `ui-sans-serif, system-ui, -apple-system` | The body fallback stack begins ui-sans-serif, system-ui, -apple-sy... | `C-FE-23` | Front-end specification |
| `10px` | The type scale is 10px, 12px, 14px, 16px, 20px, 24px, ... | `C-FE-24` | Front-end specification |
| `12px` | The type scale is 10px, 12px, 14px, 16px, 20px, 24px, ... | `C-FE-24` | Front-end specification |
| `16px` | The type scale is 10px, 12px, 14px, 16px, 20px, 24px, ... | `C-FE-24` | Front-end specification |
| `20px` | The type scale is 10px, 12px, 14px, 16px, 20px, 24px, ... | `C-FE-24` | Front-end specification |
| `24px` | The type scale is 10px, 12px, 14px, 16px, 20px, 24px, ... | `C-FE-24` | Front-end specification |
| `40px` | The type scale is 10px, 12px, 14px, 16px, 20px, 24px, ... | `C-FE-24` | Front-end specification |
| `Where devs learn web3, earn rewards, land a job.` | The public catalogue leads with Where devs learn web3, earn reward... | `C-FE-53` | Front-end specification |
| `Start Learning` | The public catalogue primary action reads Start Learning | `C-FE-54` | Front-end specification |
| `Invest in skills you need to succeed` | The value block heads Invest in skills you need to succeed | `C-FE-55` | Front-end specification |
| `Welcome, ARTISAN.` | The dashboard salutation reads Welcome, ARTISAN. | `C-FE-56` | Front-end specification |
| `Successfully registered for course!` | Enrolment success reads Successfully registered for course! | `C-FE-59` | Front-end specification |
| `Terms of Service` | The footer carries Terms of Service, Privacy Policy, Cookie Po... | `C-FE-61` | Front-end specification |
| `Privacy Policy` | The footer carries Terms of Service, Privacy Policy, Cookie Po... | `C-FE-61` | Front-end specification |
| `Cookie Policy` | The footer carries Terms of Service, Privacy Policy, Cookie Po... | `C-FE-61` | Front-end specification |
| `Manage Cookies` | The footer carries Terms of Service, Privacy Policy, Cookie Po... | `C-FE-61` | Front-end specification |
| `${APP_PUBLIC_PORT}:4173` | The port mapping is ${APP_PUBLIC_PORT}:4173 | `C-DC-2` | Deployment contract |
| `0.0.0.0` | The server binds 0.0.0.0 | `C-DC-12` | Deployment contract |
| `GET /api/me` | GET /api/me returns the caller's id, email, role, program_id | `C-DC-16` | Deployment contract, API shapes |
| `id` | GET /api/me returns the caller's id, email, role, program_id | `C-DC-16` | Deployment contract, API shapes |
| `email` | GET /api/me returns the caller's id, email, role, program_id | `C-DC-16` | Deployment contract, API shapes |
| `program_id` | GET /api/me returns the caller's id, email, role, program_id | `C-DC-16` | Deployment contract, API shapes |
| `GET /api/catalogue` | GET /api/catalogue returns a top-level array of course records | `C-DC-17` | Deployment contract, API shapes |
| `POST /api/enrolments` | POST /api/enrolments takes course_id plus program_id | `C-DC-18` | Deployment contract, API shapes |
| `course_id` | POST /api/enrolments takes course_id plus program_id | `C-DC-18` | Deployment contract, API shapes |
| `POST /api/pages/{page_id}/progress` | POST /api/pages/{page_id}/progress returns course_progress | `C-DC-19` | Deployment contract, API shapes |
| `course_progress` | POST /api/pages/{page_id}/progress returns course_progress | `C-DC-19` | Deployment contract, API shapes |
| `POST /api/assessments/{module_id}/consent` | POST /api/assessments/{module_id}/consent takes the three consent... | `C-DC-20` | Deployment contract, API shapes |
| `POST /api/assessments/{module_id}/exam` | POST /api/assessments/{module_id}/exam returns exam_id, ends_a... | `C-DC-21` | Deployment contract, API shapes |
| `exam_id` | POST /api/assessments/{module_id}/exam returns exam_id, ends_a... | `C-DC-21` | Deployment contract, API shapes |
| `ends_at` | POST /api/assessments/{module_id}/exam returns exam_id, ends_a... | `C-DC-21` | Deployment contract, API shapes |
| `questions` | POST /api/assessments/{module_id}/exam returns exam_id, ends_a... | `C-DC-21` | Deployment contract, API shapes |
| `POST /api/exams/{exam_id}/events` | POST /api/exams/{exam_id}/events takes kind plus occurred_at | `C-DC-22` | Deployment contract, API shapes |
| `kind` | POST /api/exams/{exam_id}/events takes kind plus occurred_at | `C-DC-22` | Deployment contract, API shapes |
| `occurred_at` | POST /api/exams/{exam_id}/events takes kind plus occurred_at | `C-DC-22` | Deployment contract, API shapes |
| `POST /api/exams/{exam_id}/submit` | POST /api/exams/{exam_id}/submit returns status, result_percen... | `C-DC-23` | Deployment contract, API shapes |
| `status` | POST /api/exams/{exam_id}/submit returns status, result_percen... | `C-DC-23` | Deployment contract, API shapes |
| `assessment_status` | POST /api/exams/{exam_id}/submit returns status, result_percen... | `C-DC-23` | Deployment contract, API shapes |
| `POST /api/projects` | POST /api/projects takes assessment_id, repo_url, demo_url | `C-DC-24` | Deployment contract, API shapes |
| `assessment_id` | POST /api/projects takes assessment_id, repo_url, demo_url | `C-DC-24` | Deployment contract, API shapes |
| `repo_url` | POST /api/projects takes assessment_id, repo_url, demo_url | `C-DC-24` | Deployment contract, API shapes |
| `demo_url` | POST /api/projects takes assessment_id, repo_url, demo_url | `C-DC-24` | Deployment contract, API shapes |
| `POST /api/projects/{project_id}/approve` | POST /api/projects/{project_id}/approve returns status, approv... | `C-DC-25` | Deployment contract, API shapes |
| `approved_by` | POST /api/projects/{project_id}/approve returns status, approv... | `C-DC-25` | Deployment contract, API shapes |
| `POST /api/credentials` | POST /api/credentials takes assessment_id, returning ledger_ref | `C-DC-26` | Deployment contract, API shapes |
| `ledger_ref` | POST /api/credentials takes assessment_id, returning ledger_ref | `C-DC-26` | Deployment contract, API shapes |
| `POST /api/credentials/{credential_id}/revoke` | POST /api/credentials/{credential_id}/revoke takes a reason | `C-DC-27` | Deployment contract, API shapes |
| `reason` | POST /api/credentials/{credential_id}/revoke takes a reason | `C-DC-27` | Deployment contract, API shapes |
| `GET /api/ledger` | GET /api/ledger returns a top-level array of ledger entries | `C-DC-28` | Deployment contract, API shapes |
| `POST /api/rewards/{reward_id}/claim` | POST /api/rewards/{reward_id}/claim returns status, expires_at | `C-DC-29` | Deployment contract, API shapes |
| `expires_at` | POST /api/rewards/{reward_id}/claim returns status, expires_at | `C-DC-29` | Deployment contract, API shapes |
| `GET /api/programs` | GET /api/programs returns treasury_total, treasury_remaining,... | `C-DC-30` | Deployment contract, API shapes |
| `treasury_total` | GET /api/programs returns treasury_total, treasury_remaining,... | `C-DC-30` | Deployment contract, API shapes |
| `seats_granted` | GET /api/programs returns treasury_total, treasury_remaining,... | `C-DC-30` | Deployment contract, API shapes |
| `POST /api/bounties/{bounty_id}/applications` | POST /api/bounties/{bounty_id}/applications returns bounty_id p... | `C-DC-31` | Deployment contract, API shapes |
| `bounty_id` | POST /api/bounties/{bounty_id}/applications returns bounty_id p... | `C-DC-31` | Deployment contract, API shapes |
| `GET /api/cookie-choice` | GET /api/cookie-choice returns accepted plus recorded_at | `C-DC-32` | Deployment contract, API shapes |
| `recorded_at` | GET /api/cookie-choice returns accepted plus recorded_at | `C-DC-32` | Deployment contract, API shapes |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the bearer token lifetime | `C-TR-14` |
| the proctor signal threshold for a degraded attempt | `C-CF-84` |
| the exact ramp of the spacing base unit | `C-FE-26` |
| the reserved segment denylist in full | `C-DM-8` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 0 | 12 |
| User roles | 0 | 38 |
| Core features | 0 | 177 |
| User flow | 0 | 44 |
| UI and UX notes | 0 | 41 |
| Constraints | 0 | 19 |
| Technical requirements | 0 | 36 |
| Data model | 0 | 59 |
| Front-end specification | 0 | 70 |
| Deployment contract | 0 | 39 |
