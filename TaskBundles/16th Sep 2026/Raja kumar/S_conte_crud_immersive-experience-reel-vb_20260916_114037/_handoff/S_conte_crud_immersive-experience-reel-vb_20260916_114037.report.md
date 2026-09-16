# Build report: S_conte_crud_immersive-experience-reel-vb_20260916_114037

State: MECHANICALLY-GREEN, NO-SOLUTION. Not admissible.

Authors: utsav.jain@ethara.ai (QL), raja.kumarint17@ethara.ai (contributor). Verifier mode: separate.

Companion: prd-generator/output/activetheory/activetheory_prd.md (3,688 lines). Task uuid_v5: 804cc479-7816-548b-af23-be3fd64fd467.

## Kit gate log

Rendered from `_handoff/S_conte_crud_immersive-experience-reel-vb_20260916_114037.gates.jsonl`. Never transcribed.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS |
| G1/G12 | `layout_lint.py` | 0 | PASS |
| G46 | `structure_lint.py` | 0 | PASS |
| G50 | `docker_lint.py` | 0 | PASS |
| G55 | `runtime_deps_lint.py` | 0 | PASS |
| G63 | `secret_lint.py` | 0 | PASS |
| G48 | `truth_lint.py` | 0 | PASS |
| G51 | `source_lint.py` | 0 | PASS |
| G52 | `rubric_context_lint.py` | 0 | PASS |
| G54 | `comment_lint.py` | 0 | PASS |
| G17 | `secret_hygiene_lint.py` | 0 | PASS |
| G11 | `leak_scan.py` | 0 | PASS |
| G33 | `window_lint.py` | 0 | PASS |
| G4/G5 | `contract_lint.py` | 0 | PASS |
| G43 | `prescription_lint.py` | 0 | PASS |
| G44 | `disclosure_lint.py` | 0 | PASS |
| G10 | `no_sdk_lint.py` | 0 | PASS |
| G31 | `determinism_lint.py` | 0 | PASS |
| G14 | `reward_path_lint.py` | 0 | PASS |
| G27/G30 | `rubric_lint.py` | 0 | PASS |
| G41 | `flag_lint.py` | 0 | PASS |
| G56/G57/G58 | `if_lint.py` | 0 | PASS |
| G59/G60 | `codequality_lint.py` | 2 | ? |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 0 | PASS |

Gates recorded: 32.

## Prompt receipts

| Prompt | Gate | Verdict | Checks answered | Verifier |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | self |
| `QC_spec.md` | G34 | PASS | 15 | self |
| `qc_docker.md` | G35 | PASS | 105 | self |
| `qc_rubric.md` | G53 | PASS | 16 | self |
| `qc_solution_checklist.md` | G37 | CHANGES REQUIRED | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | self |
| `task_code_verifier.md` | G3 | VALID | 12 | self |

Every certification verdict is SELF-ATTESTED: the author ran its own review prompts, so owner-is-not-verifier is not satisfied. The checklist adjudication is recorded as CHANGES REQUIRED because 38 brief obligations no outside grader can observe have no item, pending kit decision D-H; they are listed in `_handoff/S_conte_crud_immersive-experience-reel-vb_20260916_114037.checklist-qc.md`.

## Findings carried out of the review prompts

- **QC_instruction.md** A1 and B3: ## Build plan is not emitted; generate_instruction.md section 2.1 excludes it at baseline and G43 forbids a numbered build sequence; the spec_sections axis is carried by ## Front-end specification
- **QC_instruction.md** B1: crud-catalog mandates the db slot; the email slot comes from the legal P2-db-email profile because the companion sends real mail on sign up, reset, pitch, reply, withdrawal and enquiry
- **QC_instruction.md** C1: presentation rules in Core features state their negative case as a prohibition (never a full-screen refusal, never a dropdown); every rule that accepts input names its refusal and message
- **QC_instruction.md** C4: the type scale is pinned in px because the task owner's rule requires font family and size to match the PRD exactly and the companion says the scale is exact; colours stay roles and motion stays words, with no hex, millisecond or curve value
- **QC_instruction.md** C5: the concurrency reminder that app-level checks alone fail is deleted at variant b by stage-1 and generate_instruction section 5; the storage-level uniqueness rules are stated
- **QC_instruction.md** D4: the only checker mention is the generator's verbatim password block, so a grader can sign in, which section 4 of generate_instruction.md mandates word for word
- **QC_instruction.md** D5: motion, reduced-motion, audio and consent sentences were compared with PRD sections 6.5, 6.6, 14.3 and 15; reduced motion shortens the panel fade to a short fade rather than removing it, matching the companion's 0.2s substitute
- **QC_spec.md** S1: the seven spec docs sit outside the bundle at _spec/<code>/, because CON-5 forbids a spec/ folder inside a shipped bundle; 01 to 06 were authored during this review after S1 found only 00-decisions.md present
- **QC_spec.md** S5: 04-uiux-brief.md carries the companion's measured palette, type pairs and easing values for maintainers; the brief itself carries colours as roles and motion as words, per the task owner's rule that no colour value appears in the brief
- **QC_spec.md** S8: the draw lines in 00-decisions.md restate derivations, but G49 reads them, so they stay
- **QC_spec.md** G1: studio@example.com and hello@example.com were one-sided on the first pass and were added to 03-app-flow.md
- **QC_spec.md** G3: the session cookie Secure-on-https decision and the API-reads scope of the read limit were applied in the brief and were missing from 00-decisions.md on the first pass; both are now logged, with a companion carry table
- **qc_docker.md** CMP-011 and CMP-020: main publishes ${APP_PUBLIC_PORT:-4173}:4173 and sets extra_hosts because CMP-022 requires both; no sidecar publishes a port
- **qc_docker.md** DEP-012: the Playwright python base image ships Chromium and its system libraries at the pinned tag, so no install step is added
- **qc_docker.md** DEP-011: environment_mode is separate, so the grader does not share this image
- **qc_docker.md** DEP-015, DEP-016 and DEP-017: language is python
- **qc_docker.md** CMP-015: the mailpit healthcheck uses wget, which the Alpine-based mailpit image ships through busybox
- **qc_docker.md** ARCH-003: every digest was pulled and run on this machine during the reference-stub verification
- **qc_rubric.md** cycle 2 of 2: cycle 1 found RC-12 on the phone-width ticker criterion, a visibility fact a page test asserts, so it moved to test_phone_width_never_scrolls_sideways; it also found RC-07 and RC-16, rules using chrome capsule, entry state and intent list unbound and every rule opening Answer yes when; the rules were rewritten with the terms defined in place and varied sentence shapes
- **qc_rubric.md** RC-01: 34 of 34 judgment obligations are owned, 15 by the rubric and 19 by browser substeps, with none owned by both
- **qc_rubric.md** RC-13: positive points 42, instruction_following 14, functionality 8, ux_flow 6, ui_visual 9, motion 4, accessibility 1; the weighted shares sit within 0.10 of the frozen weights
- **qc_solution_checklist.md** adjudicated verdict NEEDS REVIEW, recorded here as CHANGES REQUIRED: no invention and no structural failure; nine uncovered asks were given graders and items during the audit; 38 obligations no outside channel can observe remain unresolved pending kit decision D-H, listed in _handoff/<code>.checklist-qc.md
- **qc_toml.md** SIGN-001 to SIGN-003 are deprecated in the registry and superseded by SIGN-004, which passes
- **qc_toml.md** SCHEMA-011: [delivery] and [delivery.images] are outside the section 11 template but required by stage-4-task-toml.md and G2; the stage owner is followed
- **qc_toml.md** BENCH-003 and BENCH-005: difficulty is the calibration placeholder, so the band is read against the standard tier and the 200 turns and 8000000 tokens the kit emits
- **qc_toml.md** VERIF-007: no payments or storage slot is declared
- **qc_toml.md** SEC-003: SMTP_USER reel-mailer-3f8a and SMTP_PASS mail-relay-91c2d7 are local-dev convention values for a Mailpit that accepts any credential
- **task_code_verifier.md** all twelve checks pass: S solo_founder, conte content-publishing, crud crud-catalog legal for S, archetype immersive-experience-reel has three lowercase tokens with the -vb suffix, 2026-09-16T11:40:37Z is a real UTC time not in the future
- **task_code_verifier.md** legal profiles for the cell: P0-baas, P1-db, P2-db-email, P3-db-auth, P4-db-storage, P5-db-pay-email, P7-db-search, P8-db-realtime, P9-db-queue-email; task.toml selects P2-db-email
- **task_code_verifier.md** global archetype uniqueness is not checkable from one code; the mint ledger enforces it

## Carriage of the companion (G51)

- Colours: 3/3 source colours described in the brief by family and tone; no hex or rgb value appears in the brief.
- Topics: 256/256 carried.
- Enumerated items: 785/785 carried.
- Twenty waivers, all capture apparatus or tokenisation artefacts: topics 0.2 normative versus informational, 0.4 colour notation, 34.7 what is not tested here, 37.5 the two easing notations, 37.7 two ledger artifacts, 38 acceptance checklist; items for the third-party tracker paths, the unstyled default link colour, eight underscore-joined field and event rows that tokenise into single words, the reconstructed mark silhouette, the unmeasured autoplay state and the evidence legend.
- Type: one monospaced grotesque family in Regular, Bold and Light, with the companion's exact scale (16px/400 normal, 16px/30px intent list, 14px/21px description, 14px/700 title, 13px/19.5px metadata, 12px/18px consent, 10px/30px ticker, 13.3333px form controls).

## Difficulty

16 workflows, 91 pytest substeps (54 critical) and 37 browser substeps; a workflow passes only at 90 percent of its substeps with no critical failure. The rubric carries 14 judged criteria plus 24 compiled items, and never touches reward.

Critical traps, each stated in the brief and observable from outside the app:

- server-rendered head per public address, and a document-level 404 for unserved addresses, draft slugs, stale share tokens and a dev-server path
- scene words present as document text, a keyboard path that never reloads the document and never moves on Tab, the exact interface type scale, a usable site with WebGL disabled, no request to another origin
- catalogue: or-within and and-across filters, accent and case folding, title matches before description matches, oldest as the exact reverse of recent
- drafts hidden through listing, search, reel adds and assistant context; editor refused publishing; producer refused studio endpoints
- case-folded unique email, a real confirmation mail whose earlier link dies on resend, a lock keyed on the folded email, one reset mail per hour, a reset link that dies on sign in, sign out ending the server session, a cookie-only write refused without its request token, no session token in browser storage
- reel versions: +1 per accepted write, stale writes refused with the current reel, six simultaneous writes on one version accept one; order and notes stored as rows; soft delete
- optimistic star held offline then sent, and a refused star rolled back before its failure shows
- another producer's reel or pitch answers exactly as a missing one; share links for any signed in role
- four simultaneous submissions create one pitch and one mail pair; an unavailable item is excluded; an unverified producer is refused; a studio reply moves the pitch and mails the producer, and reaches an open pitch page within twenty seconds
- assistant answers with no outbound link, stops at forty questions a session, stores turns with no account column
- analytics stored before consent only for the exempt three; typed text refused; enquiry decoy refused with nothing stored or mailed; two plain-text enquiry mails
- a role change ends every session; two admins demoting each other at one instant leave one admin

## Verified outside the kit, against a reference stub

A throwaway Flask plus vanilla-JS stub with a correct mode and a naive mode ran the whole suite on the pinned PostgreSQL, Mailpit and Playwright images, outside the bundle. The naive mode drops the locks, folds nothing, keeps tokens alive, serves one head and a 200 for every path, refuses a machine without WebGL, stores every event and holds nothing offline.

Final runs on fresh stacks: the correct stub passed 91 of 91 tests on each of two runs, and on three earlier full runs of the pre-hardening suite; the naive stub failed the same 19 trap tests on every run (the missing render context, document-level not-found, server-rendered head, draft leak, case-folded email, casing lockout, reset mail count, reset link after sign in, reel write race, offline hold, refused-star rollback, other producer's reel, pitch race, unavailable item, live reply, assistant link, analytics consent, role change sessions, admin race), and passed the rest, which grade what its switches do not break.

During verification the brief gained two solvability fixes: the session cookie is Secure only when APP_PUBLIC_URL is https (a Secure cookie is dropped on the plain http address a verifier uses), and the 600-per-minute read limit counts API reads only, so a page's static assets cannot trip it. The suite's peak read rate against the stub was under 350 per minute, counting static files.

## Not proven here

- Battery 3, handoff-owned: G13, G15, G18, G19, G20, G21, G25.
- G23 stays human-owned. G48's replay half is DEFERRED with no reference app.
- G59/G60 NOT-APPLICABLE: the vendored generator accepts no source-target criterion.
- The 37 browser substeps are graded by an LLM browser agent and were not run here; the reference stub exercises the pytest layer only.
- The rate limits for sign in, sign up, assistant and API reads per address block are carried in the brief and not graded, because the verifier shares one address with the browser pass.
- Advisory generator prompts are UNCITED.
