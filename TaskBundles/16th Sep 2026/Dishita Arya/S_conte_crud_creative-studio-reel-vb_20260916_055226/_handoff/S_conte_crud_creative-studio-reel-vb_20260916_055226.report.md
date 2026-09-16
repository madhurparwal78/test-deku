# Build report - S_conte_crud_creative-studio-reel-vb_20260916_055226

## Identity

| | |
|---|---|
| task code | `S_conte_crud_creative-studio-reel-vb_20260916_055226` |
| task id | `deku/creative-studio-reel-vb` |
| cell | solo_founder / content-publishing / crud-catalog |
| archetype | `creative-studio-reel`, variant `b` |
| service profile | `P1-db`, one slot: `backend` = `postgres` |
| variant axes | `spec_sections`, `critical_depth` |
| language | `javascript` |
| spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 (no device sharding configured) |
| companion | `prds/rocani_prd.md`, 6650 lines, carried under G51 |
| design direction | `companion` (reference/L L.6.1); the draw was `brutalist-utility` and does not govern |
| launch surface | meta_tags, mobile_viewport, no_broken_links, privacy_page, terms_page |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Public archive, journal, detail routes | INCLUDED | `## Core features`, `## Front-end specification` | the companion's measured half |
| The reel: add, reorder, note, brief, send | INCLUDED | `## Core features` rules 17 to 34 | the graded workflow |
| Studio queue, answered state | INCLUDED | `## Core features` rules 31 to 34 | the companion's section 19.8 |
| Identity, reset, sessions | INCLUDED | `## Core features` rules 1 to 6 | the companion's section 17 |
| Optimistic writes and rollback | INCLUDED | `## Core features` rules 35 to 39 | the companion's section 23 |
| Named analytics events, consent | INCLUDED | `## Core features` rules 49 to 52 | carried as an owner-readable log, no third-party tag |
| Privacy page, terms page, meta descriptions, narrow viewport, internal links | INCLUDED | `## Core features`, `## Technical requirements`, `## UI/UX notes` | the five drawn launch-surface tokens |
| Object store for media | DROPPED | - | the companion's zero-asset rule means every picture is generated; no slot would earn a critical substep |
| SMTP provider | DROPPED | - | the four transactional messages are carried as an owner-readable outbox; no email slot is declared |
| The companion's test plan (section 30) | DROPPED | - | INV10: the brief states the product, never the exam |
| The companion's build order (section 35) | DROPPED | - | `## Build plan` is not emitted at this variant |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| backend | postgres | MET | `test_seed_rows_are_not_duplicated_on_a_second_read` and eleven further tests read the declared PostgreSQL through the backend capability; `workflow_lint.py` G32 green |

## Grading surface

- workflows: 16
- browser substeps: 64
- pytest substeps: 49
- critical substeps: 10
- non-happy-path workflow ids: 6 ("visitor_reads_the_contact_policy_and_invalid_address_screens", "reel_at_the_limit_refuses_a_thirteenth_project", "concurrent_reorder_resolves_to_one_whole_list_winner", "client_reading_the_studio_queue_is_forbidden", "invalid_send_is_refused", "anonymous_or_revoked_session_write_is_denied")
- one pytest module, `tests/test_output.py`, 49 test functions covering core features, data integrity, authorization and edge cases, plus the declared db slot
- checklist items: 538, every one cited (G24 green in both directions)
- rubric criteria: 17 (15 positive, 2 negative)

### Rubric dimension shares, against the frozen weights

| Dimension | Positive points | Share | Target | Within 0.10 |
|---|---|---|---|---|
| `instruction_following` | 12 | 0.279 | 0.30 | yes |
| `functionality` | 10 | 0.233 | 0.25 | yes |
| `ux_flow` | 6 | 0.140 | 0.15 | yes |
| `ui_visual` | 6 | 0.140 | 0.15 | yes |
| `motion` | 3 | 0.070 | 0.05 | yes |
| `accessibility` | 3 | 0.070 | 0.05 | yes |
| `responsiveness` | 3 | 0.070 | 0.05 | yes |

## Literals ledger

200 pinned values, every one carried by at least one file.

| Class | Count |
|---|---|
| `account` | 5 |
| `credential` | 1 |
| `design_phrase` | 10 |
| `endpoint` | 21 |
| `env_var` | 4 |
| `motion_moment` | 9 |
| `number` | 13 |
| `route` | 8 |
| `scheme` | 7 |
| `seed_record` | 110 |
| `status` | 12 |

The full ledger is `_handoff/S_conte_crud_creative-studio-reel-vb_20260916_055226.literals-ledger.json`, which `fixture_lint.py` (G6) reads in both directions.

## Spec folder

| Document | Fed |
|---|---|
| `00-decisions.md` | the draws, the overrides, the judgment calls, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing in the brief; `## Build plan` is not emitted at this variant |

The folder is at `_spec/S_conte_crud_creative-studio-reel-vb_20260916_055226/`, outside the bundle (CON-5).

## Grading window

| Section | Characters | Reference |
|---|---|---|
| `Overview` | 2833 | 700 |
| `User roles` | 3318 | 1000 |
| `Core features` | 22680 | 2400 |
| `User flow` | 7583 | 1900 |
| `UI/UX notes` | 16694 | 1700 |
| `Technical requirements` | 7786 | unbudgeted |
| `Data model` | 5182 | unbudgeted |
| `Front-end specification` | 74655 | unbudgeted |
| `Constraints` | 1832 | 800 |
| `Deployment contract` | 5918 | unbudgeted |
| `Definition of done` | 701 | unbudgeted |
| **joined six** | **54940** | **8800** |

Every parsed section runs past the judge's slice. `generate_instruction.md` section 4 removes the length limit outright, `window_lint.py` reports rather than fails, and the tasker asked for the cap to be set aside. The prose past the slice reaches the agent in full; it stops reaching the judge, and `judge_score` never touches reward.

## Kit gate log

Rendered from `_handoff/S_conte_crud_creative-studio-reel-vb_20260916_055226.gates.jsonl`. Never transcribed.

| Gate | Tool | Exit | Verdict | Headline |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS |  |
| G1/G12 | `layout_lint.py` | 0 | PASS |  |
| G46 | `structure_lint.py` | 1 | FAIL |  |
| G50 | `docker_lint.py` | 0 | PASS |  |
| G55 | `runtime_deps_lint.py` | 0 | PASS |  |
| G63 | `secret_lint.py` | 0 | PASS |  |
| G48 | `truth_lint.py` | 0 | PASS |  |
| G51 | `source_lint.py` | 0 | PASS |  |
| G52 | `rubric_context_lint.py` | 0 | PASS |  |
| G54 | `comment_lint.py` | 0 | PASS |  |
| G17 | `secret_hygiene_lint.py` | 0 | PASS |  |
| G11 | `leak_scan.py` | 0 | PASS |  |
| G33 | `window_lint.py` | 0 | PASS |  |
| G4/G5 | `contract_lint.py` | 0 | PASS |  |
| G43 | `prescription_lint.py` | 0 | PASS |  |
| G44 | `disclosure_lint.py` | 0 | PASS |  |
| G10 | `no_sdk_lint.py` | 0 | PASS |  |
| G31 | `determinism_lint.py` | 0 | PASS |  |
| G14 | `reward_path_lint.py` | 0 | PASS |  |
| G27/G30 | `rubric_lint.py` | 0 | PASS |  |
| G41 | `flag_lint.py` | 0 | PASS |  |
| G56/G57/G58 | `if_lint.py` | 0 | PASS |  |
| G59/G60 | `codequality_lint.py` | 2 | ? |  |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |  |
| G6 | `fixture_lint.py` | 0 | PASS |  |
| G24 | `coverage_map.py` | 0 | PASS |  |
| G37 | `checklist_qc.py` | 0 | PASS |  |
| G39 | `rubric_align_lint.py` | 0 | PASS |  |
| G28/G29 | `channel_lint.py` | 0 | PASS |  |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |  |
| G0/INV5 | `vendor_check.py` | 0 | PASS |  |
| G47 | `output_qc.py` | 1 | FAIL |  |

## Prompt receipts

| Prompt | Gate | Verdict | Checks answered | Verifier |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | self |
| `QC_spec.md` | G34 | PASS | 15 | self |
| `docker_generator.md` | S5 | PASS | 0 | self |
| `generate_instruction.md` | S2 | PASS | 0 | self |
| `pytest_generator.md` | S7 | PASS | 0 | self |
| `qc_docker.md` | G35 | PASS | 105 | self |
| `qc_rubric.md` | G53 | PASS | 16 | self |
| `qc_solution_checklist.md` | G37 | PASS | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | self |
| `rubric_author.md` | S8 | PASS | 0 | self |
| `solution_checklist.md` | S3 | PASS | 0 | self |
| `task_code_verifier.md` | G3 | VALID | 12 | self |
| `toml_generator.md` | S4 | PASS | 0 | self |

Every receipt is SELF-ATTESTED: one agent authored the artifacts and ran the QC prompts. The kit's rule is owner != verifier, so these are recorded verdicts, never independent ones. `prompt_receipt_lint.py` reports the same, per prompt.

## Blocking findings

- **G46 (structure_lint.py) exit 1** - 
- **G47 (output_qc.py) exit 1** - 

## Versions

| | |
|---|---|
| kit | `deku-green-field`, working tree at the S_conte mint |
| vendored grader | `0.22.0` (INV5); `vendor_check.py` green against the pinned manifest |
| target schema | `1.4` |
| verifier mode | `shared` |
| rubric | `tests/rubric.json` generated from `grounding.yaml`; READ at runtime since grader 0.21.0 |

## Budget

`turns_expected = 200`, `tokens_expected = 7500000`. The brief carries ten H2 sections, a 150 KB front-end specification derived from a 6650-line companion, sixteen routes, sixteen tables and a graded workflow with an ordering invariant that has to survive a reload, a race and a snapshot. That is at the top of the corpus band rather than the middle, and the standard resource tier carries it.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference app. Nothing counts toward corpus targets until the app lands downstream and `harbor run -a oracle` returns `1.0` twice.
