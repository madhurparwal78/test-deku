# Build report - S_saasm_cont_website-builder-marketing-vb_20260916_070503

Rendered from `S_saasm_cont_website-builder-marketing-vb_20260916_070503.gates.jsonl`.
No verdict in this file is transcribed; every row below is a receipt written by
`revalidate.py` over the bytes it hashed.

## Identity

| | |
|---|---|
| Task code | `S_saasm_cont_website-builder-marketing-vb_20260916_070503` |
| Task id | `deku/website-builder-marketing-vb` |
| uuid_v5 | `2933b77b-e96c-5bdc-9ac7-0feb335f9e28` |
| Cell | `solo_founder` / `saas-micro-tools` / `content-publishing` |
| Service profile | `P4-db-storage` |
| Providers | `backend = postgres`, `storage = minio` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `typescript` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Companion | `wix_prd.md`, 4951 lines, supplied with the Task Order |

The Task Order named `domain: saas-productivity`, which is not a member of the kit's closed
level-2 enum. The companion's own Section 34.1 records that value as its nearest legal member
for a different taxonomy. It was mapped to `saas-micro-tools`, the only SaaS domain legal under
`solo_founder`, and the mapping is recorded in `_spec/<code>/00-decisions.md`. Nothing else in
the Task Order was substituted.

## Derived-design draws

Drawn from `sha256("website-builder-marketing")`, never chosen.

```
draw: render_model = ssr-islands
draw: backend = Express
draw: frontend = Remix (React Router 7)
draw: nav = top-nav
draw: work_surface = table-first
draw: create_flow = inline-row
draw: feedback = full-page-confirmation
draw: design_direction = companion
draw: launch_surface = custom_404,favicon,single_cta,social_preview,terms_page
```

The `aesthetic` bank draw for this archetype is `clinical-precision`. It does not govern: a
companion was supplied, so `reference/L` L.6.1 hands the axis to the measured design and
`[metadata].design_direction` is `companion`. `flag_lint.py` still enforces the three obligation
bags in `## UI/UX notes`, and G51 proves the companion's own design content reached the brief.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Home route, seventeen bands | INCLUDED | `## Front-end specification` | the companion's measured surface |
| Point of sale route | INCLUDED | `## Front-end specification` | second measured route |
| Not-found route | INCLUDED | `## Core features` | drawn `custom_404` plus the companion's Section 11 |
| Nine campaign aliases | INCLUDED | `## Core features` | companion Section 2.2, normative |
| Domain availability search | INCLUDED | `## Core features` | the one pre-auth write path the companion measured |
| Public template listing | INCLUDED | `## Core features` | companion Section 28.4 |
| Sign-up creating account, workspace, first site | INCLUDED | `## Core features` | the Task Order's own end state |
| Owner console, inline-row create | INCLUDED | `## Core features` | the `table-first` plus `inline-row` draw |
| Media upload to the object store | INCLUDED | `## Core features` | the `storage` slot, and the pattern's critical focus |
| Publish, rollback, draft privacy | INCLUDED | `## Core features` | the pattern's critical focus |
| Terms page, privacy page | INCLUDED | `## Core features` | drawn `terms_page` plus the companion's legal row |
| Favicon, social preview, per-route metadata | INCLUDED | `## Technical requirements` | drawn `favicon`, `social_preview` |
| One primary action per page | INCLUDED | `## UI/UX notes` | drawn `single_cta` |
| Collaborative editing canvas | DROPPED | `## Constraints` | companion Section 21 is a design, never reachable from the web surface |
| Site generation service | DROPPED | `## Constraints` | companion Section 23, same reason |
| Commerce, payments, the money ledger | DROPPED | `## Constraints` | companion Section 25; no payments slot in `P4-db-storage` |
| Automation engine | DROPPED | `## Constraints` | companion Section 26 |
| Analytics ingestion and query | DROPPED | `## Constraints` | companion Section 27 |
| Extension runtime | DROPPED | `## Constraints` | companion Section 29 |
| Reliability programme | DROPPED | `## Constraints` | companion Section 30 |
| Custom domain registration and certificates | DROPPED | `## Constraints` | companion Section 22 past the availability query |
| Outbound email | DROPPED | `## Constraints` | no `email` slot in `P4-db-storage` |

## Slot obligations

| Slot | Provider | Verdict | Observing tests |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_seeded_sites_stored_rows_match_the_brief`, `test_sites_row_is_persisted_for_owner_only`, `test_templates_library_holds_thirty_three_rows`, `test_concurrent_publish_leaves_one_live_revision` |
| `storage` | `minio` | MET | `test_media_upload_stores_object_in_the_bucket`, `test_media_upload_file_key_follows_the_scheme`, `test_duplicate_media_upload_leaves_one_file`, `test_draft_media_file_is_denied_to_anonymous` |

Each slot carries at least one `critical` pytest substep, which is what G9 requires.

## Grading surface

| | |
|---|---|
| Workflows | 16 (band 10 to 16) |
| Browser substeps | 43 |
| Pytest substeps | 40 |
| Critical substeps | 12 |
| Non-happy-path ids | `anonymous_request_for_a_draft_picture_is_denied`, `second_owner_is_forbidden_from_the_first_owners_site`, `visitor_cannot_open_the_owner_console`, `domain_answers_are_stable_and_an_empty_label_is_invalid`, `duplicate_signup_creates_no_second_tenant`, `concurrent_publish_leaves_one_live_revision` |
| Category mix | data_integrity 9, presentation 9, security 8, business_rule 6, validation 6, core_outcome 2 |
| Pytest module | one, `tests/test_output.py`, 40 test functions |
| Sections covered | core features, data integrity, authorization, edge cases, storage |
| Checklist items | 166 across ten section codes |
| Core asks | 10, all 10 fully graded (`tests/traceability-matrix.md`) |

## Rubric

16 criteria, 16 positive, 0 negative, positive total 50. 10 of 16 are `type: task completion`,
which is 62.5 percent against the 60 to 80 band.

| Dimension | Points | Share | Target |
|---|---|---|---|
| `instruction_following` | 15 | 0.30 | 0.30 |
| `functionality` | 11 | 0.22 | 0.25 |
| `ux_flow` | 8 | 0.16 | 0.15 |
| `ui_visual` | 10 | 0.20 | 0.15 |
| `motion` | 3 | 0.06 | 0.05 |
| `accessibility` | 3 | 0.06 | 0.05 |
| `responsiveness` | 0 | 0.00 | 0.05 |

`responsiveness` carries no criterion on purpose: the narrow-viewport obligation is graded by a
browser substep, so a criterion would be a G29 collision. Its 0.05 redistributes.

## Literals ledger

86 entries, one verifier-only.

| Class | Count |
|---|---|
| `seed_record` | 18 |
| `status` | 15 |
| `route` | 13 |
| `env_var` | 8 |
| `design_phrase` | 8 |
| `endpoint` | 7 |
| `motion_moment` | 6 |
| `number` | 5 |
| `account` | 3 |
| `scheme` | 2 |
| `credential` | 1 |

Carriers are computed from the files rather than declared, so a lying ledger cannot survive G6.
The single verifier-only value is `DB_ADMIN_URL`, carried by `task.toml` alone and absent from
`instruction.md` and from `[environment].env`, which is INV4.

## Spec folder

`Output/16sept_wix/_spec/S_saasm_cont_website-builder-marketing-vb_20260916_070503/`, seven docs,
authoring-side only and never shipped.

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the residual judgment calls, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow`, `## Deployment contract` API shapes |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing; `## Build plan` is not baseline |

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| `core_features` | 14789 | 2400 | past-slice |
| `user_flow` | 3712 | 1900 | past-slice |
| `ui_ux_notes` | 8362 | 1700 | past-slice |
| `constraints` | 4169 | 800 | past-slice |
| `user_roles` | 1592 | 1000 | over-reference |
| `overview` | 1861 | 700 | over-reference |
| joined total | 34485 | 8800 | past-slice |

Length is measured and never failed: `window_lint.py` fails nothing on length and
`generate_instruction.md` 4 says plainly not to cut a real rule to fit. The content past the
slice reaches the agent in full; it stops reaching the judge, and the judge grades generated,
self-contained criteria rather than the brief.

## Companion carriage

`source_lint.py` over `wix_prd.md`: 19 of 19 colours described by family and tone, 280 of 280
topics carried, 707 of 707 enumerated items carried. Twenty-eight waivers are recorded in the
receipt, every one of them either a subsystem `## Constraints` scopes out by name, a hex value
the A5 number rule bars from the brief, or a keyframe curve the brief-wide mechanism ban
forbids. The carry table in `00-decisions.md` records where each companion section landed.

## Kit gate log

| Gate | Tool | Verdict | Exit | stdout SHA |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | NOT-APPLICABLE | 2 | `68012655f608d8bc` |
| `G1/G12` | `layout_lint.py` | PASS | 0 | `2891cdb38890a699` |
| `G46` | `structure_lint.py` | PASS | 0 | `15aa40dc558f45a3` |
| `G50` | `docker_lint.py` | PASS | 0 | `380ed7d1c830de35` |
| `G55` | `runtime_deps_lint.py` | PASS | 0 | `a0c21dca8bc5f78a` |
| `G63` | `secret_lint.py` | PASS | 0 | `e4ebb61f3025363f` |
| `G48` | `truth_lint.py` | PASS | 0 | `1f76bf3029a8eae3` |
| `G51` | `source_lint.py` | PASS | 0 | `c37b52491073885e` |
| `G52` | `rubric_context_lint.py` | PASS | 0 | `423b706474573ee0` |
| `G54` | `comment_lint.py` | PASS | 0 | `11ca2f172b34a038` |
| `G17` | `secret_hygiene_lint.py` | PASS | 0 | `687a0643ff015bf9` |
| `G11` | `leak_scan.py` | PASS | 0 | `6e2dc5c7e42dbe29` |
| `G33` | `window_lint.py` | PASS | 0 | `d8523950f1f6fac1` |
| `G4/G5` | `contract_lint.py` | PASS | 0 | `347c09e5c827dbe2` |
| `G43` | `prescription_lint.py` | PASS | 0 | `6c848c0e323e906d` |
| `G44` | `disclosure_lint.py` | PASS | 0 | `afb4a6332c5adfa0` |
| `G10` | `no_sdk_lint.py` | PASS | 0 | `4bfac2ca61614774` |
| `G31` | `determinism_lint.py` | PASS | 0 | `2ce11eb1cd2c62d2` |
| `G14` | `reward_path_lint.py` | PASS | 0 | `4ccd500b68abed38` |
| `G27/G30` | `rubric_lint.py` | PASS | 0 | `753e14cc922901b9` |
| `G41` | `flag_lint.py` | PASS | 0 | `638f6debb84c4273` |
| `G56/G57/G58` | `if_lint.py` | PASS | 0 | `cdf20c83e9056866` |
| `G59/G60` | `codequality_lint.py` | NOT-APPLICABLE | 2 | `e23941dd85e0253b` |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | PASS | 0 | `b8ff39347afe3947` |
| `G6` | `fixture_lint.py` | PASS | 0 | `fe875ffe2d17d2c9` |
| `G24` | `coverage_map.py` | PASS | 0 | `4c4a7508b780a538` |
| `G37` | `checklist_qc.py` | PASS | 0 | `aa5f329d124f6bc3` |
| `G39` | `rubric_align_lint.py` | PASS | 0 | `67d4a5e173a64919` |
| `G28/G29` | `channel_lint.py` | PASS | 0 | `5f4dabed7eb57c8d` |
| `G40` | `prompt_receipt_lint.py` | WARN | 0 | `fafc3183ed12073e` |
| `G0/INV5` | `vendor_check.py` | PASS | 0 | `71747987483835d3` |
| `G47` | `output_qc.py` | PASS | 0 | `efa6223f604d9faa` |

Run-level gates, run once over the output root rather than per bundle:

| Gate | Tool | Verdict | Why |
|---|---|---|---|
| `G38` | `kit_selftest.py` | PASS | 32 cross-file checks agree |
| `G42` | `corpus_overlap.py` | NOT-APPLICABLE | needs two or more bundles to compare; this root holds one |
| `G49` | `diversity_lint.py` | NOT-APPLICABLE | same reason |
| `G61` | `corpus_report.py` | NOT-APPLICABLE | no admissible bundle yet; 1 minted, 1 unproven |

## Prompt receipts

`S_saasm_cont_website-builder-marketing-vb_20260916_070503.receipts.json`. Every certification
prompt carries a bundle-bound receipt with the scorecard its own registry declares. Every one is
`verifier: self`, so every one is SELF-ATTESTED rather than independent: this run had one agent.

| Prompt | Gate | Verdict | Checks answered |
|---|---|---|---|
| `task_code_verifier.md` | G3 | VALID | 12 of 12 |
| `QC_spec.md` | G34 | PASS | 15 of 15 |
| `QC_instruction.md` | G34 | PASS | 24 of 24 |
| `qc_toml.md` | G36 | PASS | 120 of 120 |
| `qc_docker.md` | G35 | PASS | 105 of 105 |
| `qc_solution_checklist.md` | G37 | PASS | registry declares none |
| `qc_rubric.md` | G53 | PASS | 16 of 16 |
| `generate_instruction.md` | S2 | PASS | advisory, registry declares none |

Four advisory generator prompts carry no receipt and are recorded UNCITED by G40:
`toml_generator.md`, `docker_generator.md`, `pytest_generator.md`, `rubric_author.md`. Their
artifacts were authored from `reference/C`, `reference/I`, `reference/J` and the stage files
instead. That is the honest record; a generator prompt that was not read surfaces downstream as
a broken artifact the mechanical gates catch, which is why G40 treats it as a note.

## Defects found by QC and repaired

| Check | Artifact | Defect | Repair |
|---|---|---|---|
| `C4` (QC_instruction) | `instruction.md` | `## UI/UX notes` named no meaning-carrying colour for failure, success or in-progress, no hover or border role, no mode commitment, no error placement | all four added |
| `S3` (QC_spec) | `02-TRD.md` | no no-second-store constraint | added |
| `S5` (QC_spec) | `04-uiux-brief.md` | words where the authoring doc owes literal values | measured palette, measured motion table, numeric accessibility bar, mode commitment added |
| `S6` (QC_spec) | `05-backend-schema.md` | no storage-level invariant, no derived-rather-than-stored list | both added |
| `S7` (QC_spec) | `06-implementation-plan.md` | ended before deploy and self-test | hardening phase plus a detached-start deploy phase added |
| `G2` (QC_spec) | `03-app-flow.md` | endpoints did not round-trip to the spec folder | interface surface listing every graded endpoint, status and pinned value added |
| `BENCH-004` (qc_toml) | `task.toml` | `tokens_expected` 9000000, outside 200000 to 8000000 | 8000000 with `turns_expected` 200 |
| `ENV-006` (qc_toml) | `task.toml` | storage vars were plain literals | all three now use default-expansion, matching compose byte for byte |
| `CMP-019` (qc_docker) | `docker-compose.yaml` | `restart:` on both sidecars | removed |
| `BP-009` (qc_docker) | `environment/Dockerfile` | `# syntax=` directive is still a `#` line under G50 | removed |
| `RD-6` (G55) | `tests/conftest.py` | probe addresses used the reserved `.test` TLD | moved to `example.com` |
| hat 2 (qc_solution_checklist) | `tests/workflows.yaml` | two `cov:` citations shared no wording with the step claiming them | re-pointed at the steps that observe them |

## Blocking findings

**`[delivery]` is absent from `task.toml`.** CON-2 requires every `[delivery.images]` value to be
a `@sha256:` digest present in `environment/`; `reference/C` C.4 requires the images to be pinned
by explicit version tag and forbids inventing a digest. This kit has no registry access, so the
block was omitted rather than fabricated, and G2 reports NOT-APPLICABLE (grandfathered). The
handoff contract carries the three `docker buildx imagetools inspect` commands that resolve it.

No other blocking finding. No spec gap prevented a required test, and no slot obligation is UNMET.

## Versions

| | |
|---|---|
| Kit | `deku-green-field` |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Judge pin | `claude-sonnet-4-6` |
| Rubric version | `1` |
| Canary | present in `solution/TRUTH.md` only |

## Budget estimate

`turns_expected = 200`, `tokens_expected = 8000000`, the top legal band. Reasoning: the brief
carries three rendered routes, seventeen home bands assembled from seventeen components, a
second route on a dark ground, thirteen endpoints, eight tables, a seeded registry, a seeded
template library of thirty-three rows, and a launch surface of five drawn obligations. The
front-end alone is larger than any single-feature task in the corpus, and the scaling model has
to be right before any band can be built. `difficulty` stays the empty calibration placeholder;
the Calibration Engineer writes it, never the author.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the reference app lands downstream
from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.

## Alignment to kit 806eb0a

The kit was pulled forward five commits, `b3d0577..806eb0a`, on 2026-09-16. This bundle was
migrated to the new contract and re-swept; the gate log below is rendered from that sweep and
supersedes any earlier gate table in this file.

| Commit | What it changed | What this bundle now carries |
|---|---|---|
| `1b99060` | adds `code_quality` as an authored code-quality rubric dimension | nothing required; the rubric carries no source criterion, so G59/G60 stay NOT-APPLICABLE |
| `da24d3b` | the section pytest module is renamed `test_output.py`; the generated compiled-rubric file becomes `test_ans.py` | `tests/test_output.py`, `solution/trinity/test_ans.py`; every `workflows.yaml` substep, the `tests/Dockerfile` COPY line, the pytest-provenance `module` and the literals-ledger carriers follow |
| `11eaf7b` | the kit emits `[verifier].environment_mode = "separate"` | `environment_mode = "separate"` in `task.toml` |
| `78e5ba6` | the vendored `tests/test.sh` is stripped of comments and re-pinned | the 90-line `test.sh`, byte-identical to the new pin (G0/INV5) |
| `806eb0a` | `solution/USER_README.md` returns as a GENERATED file carrying the seeded literals and the canary | `solution/USER_README.md`, rendered by the re-vendored `recompute.py` |

**One deliberate choice.** The agent image still installs the grader runtime (the pinned Python
packages, Chromium's libraries and the browser). Under `separate` it is not owed, and G55 RD-1 no
longer checks it. It was kept because commit `11eaf7b` itself records that nothing in the kit or
the vendored grader can verify an orchestrator honours `separate`; if one ran this bundle shared,
an image without those packages would score every trial zero. qc_docker DEP-004 and HAL-005 treat
the set as justified, so keeping it costs image size only.

**Receipts.** The certification prompt `qc_toml.md` changed in one row, VERIF-001, which now
requires `separate`; its receipt was re-bound and VERIF-001 re-adjudicated PASS against the new
`task.toml`. The advisory generator receipts whose prompts changed only by the module rename or the
mode line were re-bound with a finding saying so.

**Companion carriage.** `instruction.md` is byte-identical to the previous green sweep, so G51 is
unchanged. The source and the 28 waiver tokens are now recorded in
`S_saasm_cont_website-builder-marketing-vb_20260916_070503.sources.json` and `S_saasm_cont_website-builder-marketing-vb_20260916_070503.g51-waivers.json`, so a later sweep needs no one's
shell history.

Sweep result: ALL GATES GREEN.

| Gate | Tool | Verdict | Exit | stdout SHA |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | NOT-APPLICABLE | 2 | `68012655f608d8bc` |
| `G1/G12` | `layout_lint.py` | PASS | 0 | `2891cdb38890a699` |
| `G46` | `structure_lint.py` | PASS | 0 | `15aa40dc558f45a3` |
| `G50` | `docker_lint.py` | PASS | 0 | `380ed7d1c830de35` |
| `G55` | `runtime_deps_lint.py` | PASS | 0 | `a0c21dca8bc5f78a` |
| `G63` | `secret_lint.py` | PASS | 0 | `e4ebb61f3025363f` |
| `G48` | `truth_lint.py` | PASS | 0 | `1f76bf3029a8eae3` |
| `G51` | `source_lint.py` | PASS | 0 | `c37b52491073885e` |
| `G52` | `rubric_context_lint.py` | PASS | 0 | `423b706474573ee0` |
| `G54` | `comment_lint.py` | PASS | 0 | `11ca2f172b34a038` |
| `G17` | `secret_hygiene_lint.py` | PASS | 0 | `687a0643ff015bf9` |
| `G11` | `leak_scan.py` | PASS | 0 | `6e2dc5c7e42dbe29` |
| `G33` | `window_lint.py` | PASS | 0 | `d8523950f1f6fac1` |
| `G4/G5` | `contract_lint.py` | PASS | 0 | `347c09e5c827dbe2` |
| `G43` | `prescription_lint.py` | PASS | 0 | `6c848c0e323e906d` |
| `G44` | `disclosure_lint.py` | PASS | 0 | `afb4a6332c5adfa0` |
| `G10` | `no_sdk_lint.py` | PASS | 0 | `4bfac2ca61614774` |
| `G31` | `determinism_lint.py` | PASS | 0 | `2ce11eb1cd2c62d2` |
| `G14` | `reward_path_lint.py` | PASS | 0 | `4ccd500b68abed38` |
| `G27/G30` | `rubric_lint.py` | PASS | 0 | `753e14cc922901b9` |
| `G41` | `flag_lint.py` | PASS | 0 | `638f6debb84c4273` |
| `G56/G57/G58` | `if_lint.py` | PASS | 0 | `cdf20c83e9056866` |
| `G59/G60` | `codequality_lint.py` | NOT-APPLICABLE | 2 | `e23941dd85e0253b` |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | PASS | 0 | `b8ff39347afe3947` |
| `G6` | `fixture_lint.py` | PASS | 0 | `fe875ffe2d17d2c9` |
| `G24` | `coverage_map.py` | PASS | 0 | `4c4a7508b780a538` |
| `G37` | `checklist_qc.py` | PASS | 0 | `aa5f329d124f6bc3` |
| `G39` | `rubric_align_lint.py` | PASS | 0 | `67d4a5e173a64919` |
| `G28/G29` | `channel_lint.py` | PASS | 0 | `5f4dabed7eb57c8d` |
| `G40` | `prompt_receipt_lint.py` | WARN | 0 | `fafc3183ed12073e` |
| `G0/INV5` | `vendor_check.py` | PASS | 0 | `71747987483835d3` |
| `G47` | `output_qc.py` | PASS | 0 | `efa6223f604d9faa` |
