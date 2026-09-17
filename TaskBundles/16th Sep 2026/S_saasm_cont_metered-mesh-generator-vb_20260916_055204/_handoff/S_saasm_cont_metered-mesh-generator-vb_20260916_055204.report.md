# Build report - S_saasm_cont_metered-mesh-generator-vb_20260916_055204

## Identity

| Field | Value |
|---|---|
| Task code | `S_saasm_cont_metered-mesh-generator-vb_20260916_055204` |
| Task id | `deku/metered-mesh-generator-vb` |
| Cell | solo_founder / saas-micro-tools / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | backend `postgres`, storage `minio` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `typescript` |
| Design direction | `companion` (drawn `glass-depth`, superseded per reference/L L.6.1) |
| Launch surface | `custom_404,meta_tags,privacy_page,social_preview,spam_protection` |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Grader version | `0.22.0` (vendored, byte-identical to the pin) |
| Target schema | `1.4` |
| Verifier mode | `separate` |
| Kit revision | `806eb0a` (madhur-test) |
| Companion | `modelfy_prd.md`, 1,582 lines |

## Kit re-alignment (806eb0a)

The bundle was first assembled against an earlier kit. Five commits landed the same
day and the bundle was brought level with all of them, then re-swept from scratch.

| Kit commit | Change | What moved in this bundle |
|---|---|---|
| `da24d3b` | the section pytest module is `test_output.py`; the compiled rubric file is `test_ans.py` | `tests/test_pytest.py` renamed to `tests/test_output.py`; every `workflows.yaml` reference and the `tests/Dockerfile` COPY follow; `solution/trinity/test_ans.py` regenerated, the old generated file removed |
| `11eaf7b` | `[verifier].environment_mode` defaults to `separate` | `task.toml` switched from `shared`; qc_toml VERIF-001 re-read |
| `78e5ba6` | the vendored `test.sh` is stripped of comments and re-pinned | `tests/test.sh` re-vendored; vendor_check passes on the new pin |
| `806eb0a` | `solution/USER_README.md` is restored as a GENERATED file | `recompute.py` re-vendored at `truth-generator-7`; `USER_README.md` generated with the seeded logins and the canary |
| `1b99060` | `code_quality` becomes an authorable code rubric dimension | nothing: this bundle carries no code-quality criteria, and the change is optional. G59/G60 stay NOT-APPLICABLE |

Prompt pins were re-minted by those commits, so every adversarial receipt was
re-issued against the current prompt bytes; `qc_toml.md` was re-read for its changed VERIF-001.

## Task Order resolution

The Task Order arrived with two fields outside the closed enums. Both were
referred back and resolved before the mint; neither was repaired silently.

| Supplied | Legal value | Why |
|---|---|---|
| `domain: saas-productivity` | `saas-micro-tools` | the only solo_founder domain covering a metered browser-delivered tool |
| `pattern: media-gallery` | `content-publishing` | the graded artefact is a stored file with an owner and a visibility boundary, which is the content-publishing critical focus verbatim |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Metered generator, four stored tiers, cost before commitment | INCLUDED | instruction.md Core features 2-3 | the product; PRD 5.1-5.3 |
| Licence stamped at creation, carried into the download | INCLUDED | Core features 4, 9-10 | PRD 16.4, the distinctive invariant |
| Retention date at creation, decided downgrade rule | INCLUDED | Core features 11 | PRD 16.5 plus the PRD's own open question |
| Credit ledger, reservation, settlement, refund, idempotency | INCLUDED | Core features 6 | PRD 16.3, PRD 20.2 |
| Anonymous allowance, pre-computed samples, claim path | INCLUDED | Core features 13 | PRD 1.2, 5.6, 16.7 |
| Asset library: filters, favourite, archive, tags, history | INCLUDED | Core features 12 | PRD 6 |
| Three local browser tools and the conversion matrix | INCLUDED | Core features 21 | PRD 7 |
| Gallery with source and tier per item | INCLUDED | Core features 18 | PRD 9.1 |
| Published figures stored with basis and date | INCLUDED | Core features 19-20 | PRD 9.2, 9.3, 16.6 |
| Three plans, promotion with a start and an end | INCLUDED | Core features 16-17 | PRD 8.1, 8.3 |
| Twelve translated route trees | DROPPED | Constraints | a translation exercise, not a build one; the formatting and language-declaration half is kept |
| Editorial routes /blog, /changelog, /docs | DROPPED | Constraints | no graded surface; PRD carries no content model for them |
| Four unlaunched AI surfaces and /waitlist | DROPPED | Constraints | PRD 2.3 requires an unlaunched route to be unreachable |
| Hosted payment provider and checkout | DROPPED | Constraints | payments is not a declared slot; plan changes are direct |
| Component-library scaffolding routes | DROPPED | Constraints | PRD 2.4 refusal, reproduced as a refusal |
| Testimonials with placeholder-avatar portraits | REFUSED | Constraints, rubric R16 | PRD 19.4 refusal; graded as a negative criterion |
| Copyrighted character as a gallery source | REFUSED | Constraints | PRD 19.4 refusal; the four gallery sources are generated subjects |

## Slot obligations

| Slot | Provider | State | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | 24 pytest checks read rows through the Backend adapter; G32 confirms slot observation |
| `storage` | `minio` | MET | 6 pytest checks read the bucket through the ObjectStore adapter, 3 of them `critical`; G32 confirms |

## Graded surface

| Measure | Value |
|---|---|
| Workflows | 16 (solo_founder band 10-16) |
| Browser substeps | 24 |
| Pytest substeps | 50 |
| `critical` substeps | 14 |
| Non-happy-path workflow ids | 7: `foreign_creator_cannot_read_another_library`, `unauthenticated_library_request_is_denied`, `concurrent_submissions_leave_one_accepted`, `duplicate_idempotency_key_returns_the_existing_job`, `anonymous_allowance_limit_is_refused`, `expired_claim_token_is_refused`, `invalid_source_format_is_refused` |
| Test module | `tests/test_output.py`, 50 functions, one module (G46) |
| Sections covered | core features, authorization, data integrity, edge cases, storage |
| Checklist items | 481 across 11 sections |
| Rubric criteria | 17: 15 positive, 2 negative |

Section banners are deliberately absent from the module: G54 forbids a comment
anywhere in the shipped bundle, and reference/B settles slot coverage on the
test FUNCTION name instead, which is what G9 and G32 read.

## Rubric dimension shares

| Dimension | Target | Actual | Within 0.10 |
|---|---|---|---|
| `instruction_following` | 0.30 | 0.324 | yes |
| `functionality` | 0.25 | 0.270 | yes |
| `ux_flow` | 0.15 | 0.162 | yes |
| `ui_visual` | 0.15 | 0.162 | yes |
| `motion` | 0.05 | 0.027 | yes |
| `accessibility` | 0.05 | 0.027 | yes |
| `responsiveness` | 0.05 | 0.027 | yes |

Positive score total 37. `type: task completion` is 12 of 17 (71%), inside the 60-80% band.
R12 is declared whole-product and waived for G52; every other criterion names a surface.

## Grading window

| Section | Chars | Target | |
|---|---|---|---|
| `core_features` | 16124 | 2400 | over |
| `user_flow` | 4226 | 1900 | over |
| `ui_ux_notes` | 5441 | 1700 | over |
| `constraints` | 1384 | 800 | over |
| `user_roles` | 1860 | 1000 | over |
| `overview` | 2605 | 700 | over |
| joined | 31640 | 8800 | over |

Reported, never failed: G33 settles that the brief carries no length limit.
Every rule sitting past the judge's slice is graded by the pytest channel, and
each judged criterion carries its own context per reference/I I.8, so nothing
graded depends on the excerpt the judge sees.

## Literals ledger

79 pinned values. Every one appears verbatim in `instruction.md` and in at least
one grader carrier; G6 proves the bijection in both directions.

| Class | Count | Examples |
|---|---|---|
| `account` | 3 | `creator2@example.com`, `creator3@example.com`, `creator@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `env` | 9 | `APP_PUBLIC_PORT`, `APP_PUBLIC_URL`, `DATABASE_URL`, `DB_URL`, `GENERATION_SECONDS`, `STORAGE_ACCESS_KEY` |
| `number` | 21 | `1000`, `128`, `15000`, `196`, `20`, `2026-09-01` |
| `record` | 19 | `Brass Compass`, `Broken Statue`, `Carved Owl`, `Ceramic Teapot`, `Harbour Crane`, `Paper Lantern` |
| `route` | 9 | `/api/assets`, `/api/claims/published`, `/api/gallery`, `/api/health`, `/api/jobs`, `/api/plans` |
| `status` | 17 | `CC-BY-4.0`, `completed`, `customer-owned`, `failed`, `fast`, `free` |

No ledger entry is `verifier_only`: the datastore admin URL never appears in the
brief or in `[environment].env`, which is INV4 and is what G17 checks.

## spec/ docs and what each fed

| Doc | Fed |
|---|---|
| `00-decisions.md` | the Task Order resolution, every draw, the role rename, the scope calls and the G51 waivers |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements`, and the base image S5 derived |
| `03-app-flow.md` | `## User flow` route table and journeys |
| `04-uiux-brief.md` | `## UI/UX notes` |
| `05-backend-schema.md` | `## Data model` and the seed block |
| `06-implementation-plan.md` | `## Build plan` |

## Kit gate log

Rendered from `_handoff/S_saasm_cont_metered-mesh-generator-vb_20260916_055204.gates.jsonl`. Not transcribed: every row carries the
exit code the tool returned and the SHA-256 of the bytes it examined.

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

Corpus-level gates, run once over the output root rather than per bundle:

| Gate | Tool | Verdict |
|---|---|---|
| G38 | `kit_selftest.py` | PASS, 32 checks |
| G42 | `corpus_overlap.py` | NOT-APPLICABLE, needs >= 2 comparable bundles |
| G49 | `diversity_lint.py` | PASS, no shared run over any per-section cap |

## Adversarial prompt receipts

| Prompt | Gate | Checks | Verdict | Verifier |
|---|---|---|---|---|
| `task_code_verifier.md` | G3 | 12 | PASS | self |
| `QC_spec.md` | G34 | 15 | PASS | self |
| `QC_instruction.md` | G34 | 24 | PASS | self |
| `qc_rubric.md` | G53 | 16 | PASS | self |
| `qc_solution_checklist.md` | G37 | 0 | PASS | self |
| `qc_toml.md` | G36 | 120 | PASS | self |
| `qc_docker.md` | G35 | 105 | PASS | self |

Every verdict above is **SELF-ATTESTED**: one agent authored the artifacts and
ran the review, so owner and verifier are the same identity. The kit's rule is
owner != verifier, so these are recorded verdicts and not independent ones, and
G40 reports them in that state rather than as a clean pass.

## Defects this review found and fixed

**`QC_spec.md`**

- G1 (MAJOR, fixed): the corpus password `deku-demo-pw-2026` appeared in spec/05-backend-schema.md and in tests/conftest.py but NOT in instruction.md. The grader signs in with that literal, so a complete app seeded with any other password would have scored zero -- the Bug-2 shape. Fixed: instruction.md `## Data model` now carries a Seed data block pinning the three accounts, their plans, their balances and that password.
- S3 (MAJOR, fixed): 02-TRD.md named no auth mechanism, no logging rule, no canonical env-var list and no no-second-store constraint. All four added.
- S4 (MAJOR, fixed): 03-app-flow.md carried a route table and journeys but no entry-and-redirect rules. Added, including the rule that a non-owner is answered not found rather than redirected.
- S5 (MAJOR, fixed): 04-uiux-brief.md carried character words only. The companion measures its own values (PRD 3.2-3.6, 11.2), so a Measured literals section was added: palette hex, size-over-line pairs, blur and stacking scales, the breakpoint ladder, the 44x44 / 4.5:1 a11y bar and the dark-only mode commitment.
- S6 (BLOCKER, fixed): 05-backend-schema.md stated invariants as prose with no storage-level constraint, which is the rule the hidden checklist attacks. Added named unique constraints for the monthly grant, the idempotency key, the representation kind and the published-claim key, the row-level lock on credit consumption, each with the note that an app-level check alone loses the race; plus a Derived-rather-than-stored section.
- S7 (MAJOR, fixed): 06-implementation-plan.md ended at the public pages. Added phase 15, deploy and self-test with a detached start and five observable exit reads.

**`QC_instruction.md`**

- D4 (BLOCKER, fixed): the framing paragraph read `a separate verifier reads the database and the object store directly`. That is harness-verifier prose naming an external checker by role, which G44 cannot catch by design. Rewritten to state the requirement observably: the boundary holds at the API and in the object store, not only in the interface.
- D3a (BLOCKER, fixed): `## Definition of done` was a 26-bullet checklist reading as a test plan. Rewritten as one 88-word, two-sentence product-truth paragraph carrying the core outcome and the single hardest guarantee.
- A7 (BLOCKER, fixed): the seeded-credentials block did not carry the `/app/USER_README.md` instruction beside the password literal. Added.
- A8 (MINOR, accepted with citation): `DB_URL` is off the A8 canon list, and `GENERATION_SECONDS` is not on it at all. Both are mandated elsewhere and are kept: reference/C C.2 requires DATABASE_URL and DB_URL to be injected with the same value (omitting DB_URL is a named reward-zero hazard), and reference/J J.9 requires a task-owned timing variable the verifier can bind low. The A8 list enumerates slot-provider variables only.
- C7 (accepted with citation): `## Core features` is far past the 2,500-char judge slice. G33/window_lint settles this -- the brief has no length limit and section counts are reported, never failed. Every rule sitting past the cut is graded by the pytest channel, and the judged criteria carry their own context per reference/I I.8, so nothing graded depends on the excerpt.
- C5 (accepted with citation): storage-level constraints are named in spec/05-backend-schema.md, not in the brief's `## Data model`. INV9 forbids naming an SQL locking construct or index DDL there and requires a tighter observable statement instead, which G43/prescription_lint enforces mechanically and which the brief carries.
- S2-equivalent (accepted with citation): 01-PRD.md lists 10 must-have features against the 3-6 baseline. reference/G G-spec-templates raises the cap to 6-10 when a companion document was supplied, which is this task.

**`qc_rubric.md`**

- RC-02 (fixed): C-CF-77 and C-CF-21 were each claimed by two criteria in the rubric-provenance sidecar, so one obligation would have moved the score twice. The backfill that assigned them now excludes already-claimed items.
- RC-01 (fixed): after that change R16 and R17 cited no obligation at all. Both negatives are now pinned to the constraint they grade -- R16 to C-CN-10 (no placeholder-avatar testimonial) and R17 to C-CF-136 (the list price is displayed after the promotion end date).
- RC-09 (fixed, cycle 1): nine criteria failed the mechanical text rules -- `it` as a bare pronoun in R4, R5, R7, R8 and R12, the connector `as well as` in R11, and `not`/`no` inside the two negatives. All rewritten; cycle 2 clean.
- RC-05 (fixed): R16 and R17 named no surface. Both now name one -- the gallery page and the pricing page.
- RC-05 (declared): R12 is deliberately whole-product -- every page leads with one primary action -- and is declared with --waive-criterion R12 rather than given a false single surface.
- RC-15: converged on cycle 2.

**`qc_solution_checklist.md`**

- The prompt declares no machine-readable check registry; the adjudication is the coverage and invention read. 481 items parse, ids are sequential per section with no gaps, every item cites a source section, the ledger arithmetic reconciles, and checklist_qc (G37 layer 1) returns PASS.
- Invention read: every item traces to a sentence in instruction.md. The three items added during this review (idempotent seeding, the pre-computed samples, the measurement date) were added to the brief first and to the checklist second, never the reverse.
- Unpinned: three values are declared referenced-but-not-pinned -- the client poller's retry interval, the accepted upload byte ceiling, and any per-account asset cap. None is asserted by a grader.

**`qc_toml.md`**

- META-002 (High, fixed): harbor_version was 0.22.0; the canonical template pins 0.20.0. Corrected.
- BENCH-001 (Critical, fixed): build_timeout_sec was 1200.0; the Standard tier pins 900.0. Corrected.
- BENCH-004 (High, fixed): tokens_expected was 9500000, outside the absolute 200000-8000000 range. Set to 8000000.
- TAX-011 (High, fixed): spec_sections_given carried `frontend` out of position. Reordered to the canonical token order.
- META-009 (Medium, fixed): keywords were ordered greenfield, sub_category, domain, pattern, topic, providers. Reordered to greenfield, sub_category, language, provider slugs in slot order, then two topical terms.
- SCHEMA-013/014 (Medium, fixed): section and key order diverged from the Section 11 template -- keywords sat before uuid_v5, authors was a one-line array, network_mode and allowed_hosts were separated from the environment block, and APP_PUBLIC_URL was missing from [environment].env. task.toml was rewritten against the template.
- SIGN-004 (Critical, PASS): no [signoff] table is present; the table is retired and G62 fails a bundle that still carries one.
- TAX-008 (Informational, unverifiable): global archetype uniqueness cannot be decided from one bundle. The mint ledger refused a duplicate at S1, which is the only evidence available here.
- VERIF-001 (High, fixed on kit re-alignment): kit commit 11eaf7b moved the canonical value to `environment_mode = "separate"`. task.toml was on `"shared"`, which stays legal but is no longer what the kit emits. Changed to `"separate"`; the grader now ships its own image from tests/Dockerfile on deku-verifier-base.
- BENCH-006 (Critical, PASS): the calibration block carries the exact placeholders -- difficulty, reference_model_used empty, pass_rate 0.0, pass_rate_ci [0.0, 0.0], calibration_trials 0. No metric is fabricated.

**`qc_docker.md`**

- CMP-004 (Critical, deviation recorded): reference/C C.2.1 pins `minio/minio:RELEASE.2024-10-13T13-34-11Z` on Docker Hub. That repository no longer exists on Docker Hub at all -- verified live against both the Hub API (`object not found` for the repository and the tag) and the registry (401 on the manifest). The same image and tag resolve at MinIO's own registry, so the compose file references quay.io/minio/minio at that tag, pinned to the manifest-list digest sha256:9535594a..., verified by a 200 from the quay registry. OPERATOR ACTION: reference/C C.2.1 needs updating, and the kit's own note that every pin must be confirmed to resolve is what produced this.
- ARCH-002 (High, PASS): all three digests are manifest-list (index) digests, not single-architecture child digests. Each was resolved live with an index Accept header.
- ARCH-003 (Critical, PASS): no digest is fabricated. python and postgres were resolved from Docker Hub and both match the digests the sibling bundle carries; minio was resolved from quay.io.
- DEP-011 (Critical, fixed): boto3 was pinned 1.35.36 against the grader's 1.35.99. Corrected, so the graded and shipped grader are the same grader. G55 now passes.
- DEP-011 (re-read after kit commit 11eaf7b): under `separate` mode the agent image owes the grader no Python package and G55 RD-1 skips. The pins are left in environment/Dockerfile because the docker_generator template still emits them; they remain byte-matched to the grader pin, so nothing drifts if the task is ever run shared.
- INV5 (re-vendored after kit commit 78e5ba6): tests/test.sh is the stripped, comment-free copy now pinned in vendor/grader-0.22.0/MANIFEST.json. vendor_check passes against the new pin.
- DEP-014 (High, PASS): the healthcheck runs pg_isready and postgresql-client is installed in the image.
- DEP-012 (High, PASS): playwright is installed with Chromium's system libraries and an explicit browser install step.
- SEC-001/SEC-002 (Critical, PASS): no credential is baked into the image, and no admin or service-role credential reaches the agent image. DB_ADMIN_URL is [verifier].env only (INV4), which G17 confirms.
- CMP-003/CMP-022 (Critical, PASS): the main service sets extra_hosts and ports and sets none of image, command, entrypoint or profiles.
- CMP-005 (Critical, PASS): every compose credential matches the value task.toml injects for the same service -- minioadmin / minio-root-3d81f7a2 and deku_app / deku-local-dev.
- HAL-001..004 (Critical, PASS): no runtime, framework, package manager or service appears that task.toml and the TRD do not declare.
- CON-*/BP-* (PASS): the one-shot minio-init parks on tail -f /dev/null rather than exiting, so `docker compose up --wait` is not stranded; G55 confirms.

## Blocking findings

One, and it is an operator action rather than a bundle defect.

**reference/C C.2.1 pins a MinIO image that no longer exists.** The matrix names
`minio/minio:RELEASE.2024-10-13T13-34-11Z` on Docker Hub. That repository has been
withdrawn from Docker Hub entirely: the Hub API answers `object not found` for both
the tag and the repository, and the registry answers 401 on the manifest. The same
image and tag are served from MinIO's own registry, so this bundle references
`quay.io/minio/minio` at that tag, pinned to the manifest-list digest
`sha256:9535594a...`, verified by a 200 from the quay registry. Every bundle in the
corpus that declares the `storage` slot is affected, and `docker compose up` would
fail on the Hub pin rather than score zero, which is a lost trial. reference/C
C.2.1 needs updating.

No spec gap and no harness gap prevented a required test.

## Budget

`turns_expected = 260`, `tokens_expected = 8000000`. The reasoning: two products in
one build, a metered cloud generator with an asynchronous job and an append-only
ledger, plus three genuinely local browser tools including a declared 128-pair
conversion matrix; 481 checklist obligations; 50 deterministic checks across five
concerns; and two boundaries that fail silently if approximated, the contended
balance and the object-ownership path. 8000000 is the absolute ceiling qc_toml
BENCH-004 permits, which is where a build of this size belongs.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

Not admissible. The bundle carries no reference app, so nothing here has been
compiled or run. It becomes admissible when the app is built downstream from
`solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
