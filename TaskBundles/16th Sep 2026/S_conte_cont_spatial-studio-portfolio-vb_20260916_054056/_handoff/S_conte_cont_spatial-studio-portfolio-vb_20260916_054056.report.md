# Build report - S_conte_cont_spatial-studio-portfolio-vb_20260916_054056

## Identity

| | |
|---|---|
| Task code | `S_conte_cont_spatial-studio-portfolio-vb_20260916_054056` |
| Task id | `deku/spatial-studio-portfolio-vb` |
| Cell | solo_founder / content-publishing / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | `db` -> `postgres` - `storage` -> `minio` |
| Variant | `b`, on axes `critical_depth` + `spec_sections` |
| Language | `typescript` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 (no device shard configured) |
| Kit | deku-green-field |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Companion | `3dweblab_prd.md`, 4379 lines |
| Verifier mode | `separate`: the grader runs in its own image, built from `tests/Dockerfile` on `deku-verifier-base` |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Derived-design draws

| Axis | Value | Source |
|---|---|---|
| `render_model` | ssr-islands | S-2.9, sha256(archetype) offset 0 |
| `backend` | Hono | S-2.9, offset 8 |
| `frontend` | SvelteKit | S-2.9, offset 16 |
| `nav` | top-nav | S-2.10, offset 24 |
| `work_surface` | split detail-pane | S-2.10, offset 32 |
| `create_flow` | dedicated-route | S-2.10, offset 40 |
| `feedback` | optimistic-row | S-2.10, offset 48 |
| `design_direction` | companion | reference/L S-L.6.1; the bank pick `editorial-serif` is recorded but does not govern |
| `launch_surface` | alt_text, colour_contrast, single_cta, sitemap_robots, spam_protection | reference/O S-O.3 |

## Feature resolution

| Candidate | Verdict | Where it landed | Reason |
|---|---|---|---|
| The permanent three-dimensional stage | INCLUDED | `## Core features`, `## Front-end specification` | the companion's whole product proposition; graded by the rubric because it is a rendered surface |
| Three product lines, one template | INCLUDED | `## Core features`, `## Data model` | counts are exact and assertable over the API |
| Four service disciplines, one route | INCLUDED | `## Core features` | four bullets each is a deterministic count |
| Numbered case index into full write-ups | INCLUDED | `## Core features` | the pattern's core outcome |
| The draft boundary on unpublished work | INCLUDED | `## Core features` rule 3 | the pattern row's critical focus |
| Media in the object store | INCLUDED | `## Core features` | the storage slot's observable side effect |
| Contact enquiry with spam refusal | INCLUDED | `## Core features` | the Task Order's own closing action; carries the drawn `spam_protection` token |
| Legal routes, cookie choice, page-view log | INCLUDED | `## Core features` | companion sections 15 and 21.2, plus the volunteered launch-surface tokens |
| Sitemap and robots | INCLUDED | `## Core features`, `## Technical requirements` | the drawn `sitemap_robots` token |
| Third-party analytics collection | DROPPED | waived in `_spec/00-decisions.md` | outside the closed provider world of reference/K; the observable half is carried as the local page-view log |
| The reference viewport `maximum-scale` / `user-scalable` values | DROPPED | waived in `_spec/00-decisions.md` | the companion itself instructs the build not to reproduce them |
| A named renderer, mesh loader or post-processing library | DROPPED | waived on G51 | labelled `Observed implementation, informational` by the companion; naming one is a mechanism pin under INV9 |
| `## Build plan` | DROPPED | not emitted | not baseline (generate_instruction S-2.1) |
| `[delivery]` block in task.toml | DROPPED | not emitted | every `[delivery.images]` value must be a `@sha256:` digest present in `environment/`, and the docker rules forbid pinning by digest; no registry access here, so a fabricated digest was refused. validate_task returns NOT-APPLICABLE (grandfathered) |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `db` | `postgres` | MET | `test_enquiry_is_persisted_as_a_row` asserts the stored row through the backend capability, and is the slot's `critical` substep |
| `storage` | `minio` | MET | `test_uploaded_media_file_lands_in_the_object_store` asserts the object exists in the bucket at its scheme key, and is the slot's `critical` substep |

## Grading surface

| | |
|---|---|
| Workflows | 16 (band [10, 16]) |
| Browser substeps | 20 |
| Pytest substeps | 31 |
| Critical substeps | 7 |
| Non-happy-path workflow ids | 6: `draft_case_is_denied_to_a_visitor`, `draft_case_media_is_denied_to_a_reader`, `reader_cannot_publish_a_case`, `unauthenticated_caller_is_denied_the_studio_api`, `invalid_enquiry_is_refused`, `duplicate_case_number_is_refused` |
| Pytest module | one, `tests/test_output.py`, 31 test functions |
| Sections covered | core features, data integrity, authorization, edge cases, storage slot |
| Rubric criteria | 15 (13 positive, 2 negative) |

### Rubric dimension shares, positives only

| Dimension | Share | Target | Within 0.10 |
|---|---|---|---|
| `instruction_following` | 0.289 | 0.30 | yes |
| `functionality` | 0.244 | 0.25 | yes |
| `ux_flow` | 0.133 | 0.15 | yes |
| `ui_visual` | 0.133 | 0.15 | yes |
| `motion` | 0.067 | 0.05 | yes |
| `accessibility` | 0.067 | 0.05 | yes |
| `responsiveness` | 0.067 | 0.05 | yes |

## Literals ledger

150 pinned values. Carriers are computed from the files themselves, so a declared carrier that lacks the value is a G6 failure rather than a claim.

| Class | Values | Carriers seen |
|---|---|---|
| `account` | 3 | `conftest.py`, `instruction.md` |
| `credential` | 1 | `conftest.py`, `instruction.md` |
| `design_phrase` | 24 | `instruction.md` |
| `endpoint` | 14 | `conftest.py`, `instruction.md`, `test_output.py` |
| `env_var` | 7 | `instruction.md`, `task.toml` |
| `motion_moment` | 3 | `instruction.md` |
| `number` | 8 | `conftest.py`, `instruction.md`, `task.toml`, `test_output.py` |
| `route` | 22 | `conftest.py`, `instruction.md`, `test_output.py` |
| `scheme` | 2 | `instruction.md` |
| `seed_record` | 56 | `conftest.py`, `instruction.md`, `task.toml`, `test_output.py` |
| `status` | 10 | `conftest.py`, `instruction.md`, `task.toml`, `test_output.py` |

Verifier-only values: none in the ledger; the admin datastore credential lives in `task.toml` `[verifier].env` alone and is deliberately not a brief literal (INV4)

## Spec folder, and what each doc fed

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the judgment calls, the G51 waiver list, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow`, the API shapes in `## Deployment contract` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at baseline |

## Grading window

| Section | Chars | Reference | |
|---|---|---|---|
| Core features | 13558 | 2400 | past slice |
| User flow | 4919 | 1900 | past slice |
| UI/UX notes | 9979 | 1700 | past slice |
| Constraints | 1175 | 800 | within slice |
| User roles | 1413 | 1000 | within slice |
| Overview | 2225 | 700 | within slice |
| **joined** | **33269** | 8800 | past slice |

The brief has no length limit (generate_instruction S-4). What sits past the slice reaches the agent in full and stops reaching the judge; the judged criteria are self-contained and carry their own `evaluation_rule`, so nothing graded depends on the tail.

## Kit gate log, rendered from the receipts

Source: `_handoff/S_conte_cont_spatial-studio-portfolio-vb_20260916_054056.gates.jsonl`. Never transcribed.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 2 | NOT-APPLICABLE |
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

## Prompt receipts

| Prompt | Gate | Verdict | Verifier | Checks |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | self | 24 |
| `QC_spec.md` | G34 | PASS | self | 15 |
| `docker_generator.md` | S5 | PASS | self | no registry |
| `generate_instruction.md` | S2 | PASS | self | no registry |
| `pytest_generator.md` | S7 | PASS | self | no registry |
| `qc_docker.md` | G35 | PASS | self | 105 |
| `qc_rubric.md` | G53 | PASS | self | 16 |
| `qc_solution_checklist.md` | G37 | PASS | self | no registry |
| `qc_toml.md` | G36 | PASS | self | 120 |
| `rubric_author.md` | S8 | PASS | self | no registry |
| `solution_checklist.md` | S3 | PASS | self | no registry |
| `task_code_verifier.md` | G3 | VALID | self | 12 |
| `toml_generator.md` | S4 | PASS | self | no registry |

Every certification prompt is SELF-ATTESTED: one agent authored and reviewed. The kit's rule is owner != verifier, so these are recorded verdicts, never independent ones.

## Blocking findings

| Finding | Effect |
|---|---|
| The Task Order arrived with `domain: portfolio-agency`, which is not in the 36-domain enum | Resolved by the tasker to `content-publishing` before the mint. The folder name and the ledger row carry the resolved value |
| The companion excludes a contact form; the Task Order requires an enquiry | The Task Order wins. Recorded as a deliberate divergence, and the companion's copy controls are kept beside the form rather than replaced |
| `[delivery]` requires `@sha256:` image digests that the docker rules forbid pinning | `[delivery]` is not emitted. G2 returns NOT-APPLICABLE (grandfathered) rather than carrying a fabricated digest |
| 147 of 521 checklist items are cited with `(earned: ...)` | Scope-out and contract obligations whose observation is an absence. Each is carried by a browser journey that walks the surface and records what is missing |

## Kit alignment, 2026-09-16

Re-aligned to kit commits `da24d3b`, `11eaf7b`, `78e5ba6` and `806eb0a`: the section suite is `tests/test_output.py` and the compiled-rubric file is `solution/trinity/test_ans.py`; `[verifier].environment_mode` is `separate`; `tests/test.sh` and `solution/trinity/recompute.py` are re-vendored from the current `grader-0.22.0` pin; `solution/USER_README.md` is generated again and carries the second copy of the canary. Prompt pins were re-minted upstream, so every receipt token was re-issued.

The agent image still installs the grader's Python pins and Chromium. Under `separate` it no longer owes them; they are kept because they are harmless, let the agent drive a browser during its own session, and keep the image valid if an operator flips the bundle back to `shared`.

## Budget estimate

`turns_expected = 260`, `tokens_expected = 1400000`. The reasoning: this is a variant-`b` companion-backed task whose brief runs past 100 KB and whose product is eleven public routes, a studio console, nine tables, a generated three-dimensional stage and a zero-asset asset pipeline. The brief alone is a substantial read before any code is written, and the frame budget forces a tuning pass the kit cannot shortcut. The standard resource tier applies (`cpus 4`, `memory_mb 8192`, `storage_mb 20480`).

## Exit

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference app. Nothing counts toward corpus targets until the app lands downstream and `harbor run -a oracle` returns `1.0` twice.

Requirement traceability ships inside the bundle at `tests/traceability-matrix.md` and `tests/traceability-matrix.csv`, regenerated by every sweep from the scan G24 makes.
