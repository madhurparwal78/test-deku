# Build report - S_conte_cont_scrollytelling-engineer-portfolio-vb_20260916_073349

Rendered from `_handoff/S_conte_cont_scrollytelling-engineer-portfolio-vb_20260916_073349.gates.jsonl`. No verdict in this file was typed by hand.

## Identity

| Field | Value |
|---|---|
| Task code | `S_conte_cont_scrollytelling-engineer-portfolio-vb_20260916_073349` |
| Task id | `deku/scrollytelling-engineer-portfolio-vb` |
| Cell | solo_founder / content-publishing / content-publishing |
| Archetype | `scrollytelling-engineer-portfolio` |
| Service profile | `P4-db-storage` |
| Providers | db: `postgres` - storage: `minio` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `python` |
| Capability flags | `aesthetic` |
| Design direction | `companion` (reference/L L.6.1: a companion beats the draw) |
| Launch surface | `cookie_choice`, `favicon`, `mobile_viewport`, `no_broken_links`, `page_view_log` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Companion | `melboucierayane_prd.md`, recorded in `_handoff/S_conte_cont_scrollytelling-engineer-portfolio-vb_20260916_073349.sources.json` |

## Derived-design draws (R4, SHA-256 over the archetype)

| Axis | Value |
|---|---|
| render_model | `mpa-progressive` |
| backend | `Flask + Jinja` |
| frontend | `Alpine.js + server templates` |
| nav | `sidebar-nav` |
| work_surface | `card-grid` |
| create_flow | `multi-step-wizard` |
| feedback | `inline-banner` |
| design_direction (drawn) | `brutalist-utility`, superseded by `companion` |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Single-scroll index, nine bands | INCLUDED | `## Core features`, `## Front-end specification` | the companion's whole information architecture |
| Wireframe field with a still fallback | INCLUDED | `## Core features`, `## Technical requirements` | companion section 7, three normative capability requirements |
| Declarative diagram language, two layouts | INCLUDED | `## Core features`, `## Data model` | companion sections 8 and 17.2 |
| Writing archive, coded series | INCLUDED | `## Core features`, `## Front-end specification` | companion sections 11 and 12 |
| Studio wizard, validate and export | INCLUDED | `## Core features`, `## User flow` | companion section 17, and the pattern's object-store focus |
| Contact channel, token thread | INCLUDED | `## Core features` | companion section 14 |
| Signal desk, scoring, availability | INCLUDED | `## Core features`, `## Data model` | companion section 16 |
| Cookie choice, favicon, link map, page views, narrow viewport | INCLUDED | `## Core features`, `## Technical requirements`, `## UI/UX notes` | the five drawn launch-surface obligations |
| Outbound email, SMS, push | DROPPED | `## Constraints`, `## Technical requirements` | no mail slot exists at `P4-db-storage`; recorded as an `outbound_messages` row instead, with the double opt-in rule intact |
| `## Build plan` | DROPPED | - | not in the baseline lever set (generate_instruction.md S2.1) |
| Companion section 22, build order | DROPPED | - | a work order, not a specification; waived on the record |

## Slot obligations

| Slot | Provider | State | Evidence |
|---|---|---|---|
| db | `postgres` | MET | `DATABASE_URL` named in `## Technical requirements`; G5 and G32 green; 16 tables in `## Data model` |
| storage | `minio` | MET | the four `STORAGE_*` variables named; the pinned key schemes graded by `test_still_bytes_live_in_the_bucket_at_their_key`; G32 green |

## Grading layer

| Measure | Value |
|---|---|
| Workflows | 16 |
| Browser substeps | 46 |
| pytest substeps | 57 |
| Critical substeps | 23 |
| Non-happy-path ids | `visitor_signs_up_and_invalid_input_is_refused`, `unauthenticated_request_for_a_protected_route_is_denied`, `diagram_structure_with_an_invalid_kind_is_refused`, `draft_piece_cannot_be_read_by_anyone_else`, `concurrent_publishes_of_one_draft_accept_at_most_one`, `fourth_note_in_an_hour_hits_the_rate_limit`, `desk_sorts_notes_and_two_choosers_conflict_on_one_slot`, `cookie_choice_and_the_empty_surfaces_hold_at_any_width` |
| Test module | `tests/test_output.py`, one merged section module, 57 functions |
| Checklist items | 293 across ten section blocks |
| Checklist tags | capability 18, constraint 110, contract 25, data 25, literal 52, role 10, ui 53 |

## Judged rubric

14 criteria, 14 positive and 0 negative, positive total 32.

| Dimension | Criteria | Share | Target |
|---|---|---|---|
| `instruction_following` | 2 | 0.312 | 0.30 |
| `functionality` | 2 | 0.250 | 0.25 |
| `ux_flow` | 2 | 0.125 | 0.15 |
| `ui_visual` | 2 | 0.125 | 0.15 |
| `motion` | 2 | 0.062 | 0.05 |
| `accessibility` | 2 | 0.062 | 0.05 |
| `responsiveness` | 2 | 0.062 | 0.05 |

## Literals ledger

148 pinned values, bijective with the brief and the graders (G6 green).

| Class | Count |
|---|---|
| `account` | 3 |
| `credential` | 1 |
| `design_phrase` | 11 |
| `endpoint` | 1 |
| `env_var` | 8 |
| `motion_moment` | 9 |
| `number` | 17 |
| `route` | 4 |
| `scheme` | 4 |
| `seed_record` | 47 |
| `status` | 43 |

## spec/ documents

Authoring-side only, at `_spec/S_conte_cont_scrollytelling-engineer-portfolio-vb_20260916_073349/`. None ships in the bundle (CON-5).

| Document | Fed |
|---|---|
| `00-decisions.md` | the draws, every residual call, the companion carry table, the G51 waiver record |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow`, plus the API surface the `## Deployment contract` table grades |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing in the brief; `## Build plan` is not emitted at this lever set |

## Grading window

Reported, never failed (G33). The tasker directed that the section ceilings be set
aside for this task so the companion's detail reaches the agent in full.

| Section | Chars | Reference |
|---|---|---|
| `Core features` | 17077 | 2400 |
| `User flow` | 4863 | 1900 |
| `UI/UX notes` | 10242 | 1700 |
| `Constraints` | 1288 | 800 |
| `User roles` | 2127 | 1000 |
| `Overview` | 2504 | 700 |
| joined six | 38101 | 8800 |

## Kit gate log

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS |
| `G1/G12` | `layout_lint.py` | 0 | PASS |
| `G46` | `structure_lint.py` | 0 | PASS |
| `G50` | `docker_lint.py` | 0 | PASS |
| `G55` | `runtime_deps_lint.py` | 0 | PASS |
| `G63` | `secret_lint.py` | 0 | PASS |
| `G48` | `truth_lint.py` | 0 | PASS |
| `G51` | `source_lint.py` | 0 | PASS |
| `G52` | `rubric_context_lint.py` | 0 | PASS |
| `G54` | `comment_lint.py` | 0 | PASS |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS |
| `G11` | `leak_scan.py` | 0 | PASS |
| `G33` | `window_lint.py` | 0 | PASS |
| `G4/G5` | `contract_lint.py` | 0 | PASS |
| `G43` | `prescription_lint.py` | 0 | PASS |
| `G44` | `disclosure_lint.py` | 0 | PASS |
| `G10` | `no_sdk_lint.py` | 0 | PASS |
| `G31` | `determinism_lint.py` | 0 | PASS |
| `G14` | `reward_path_lint.py` | 0 | PASS |
| `G27/G30` | `rubric_lint.py` | 0 | PASS |
| `G41` | `flag_lint.py` | 0 | PASS |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS |
| `G59/G60` | `codequality_lint.py` | 2 | ? |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS |
| `G6` | `fixture_lint.py` | 0 | PASS |
| `G24` | `coverage_map.py` | 0 | PASS |
| `G37` | `checklist_qc.py` | 0 | PASS |
| `G39` | `rubric_align_lint.py` | 0 | PASS |
| `G28/G29` | `channel_lint.py` | 0 | PASS |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN |
| `G0/INV5` | `vendor_check.py` | 0 | PASS |
| `G47` | `output_qc.py` | 0 | PASS |

Traceability: `tests/traceability-matrix.md` and `tests/traceability-matrix.csv`,
regenerated by the sweep that decided G24. Cited, not restated.

## Handoff gates, undecided here

Listed with their commands in `_handoff/S_conte_cont_scrollytelling-engineer-portfolio-vb_20260916_073349.handoff.md`: G13, G15, G18, G19, G20, G21, G25.

## Blocking findings

None. No declared slot lacks an image, no gate is uncited, and no spec gap
prevented a required grader.

## Versions

| Field | Value |
|---|---|
| Kit | `deku-green-field` |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Harbor | `0.20.0` |
| Verifier mode | `separate` |

## Effort estimate

`turns_expected = 170`, `tokens_expected = 7000000`. Reasoning: two browser
renderers that carry no library the brief names, a declarative diagram format with
its own validator, sixteen tables, thirty-four endpoints and nine content bands of
pinned copy. The field and the diagram renderer are each a from-scratch piece of
work, and the copy deck alone is a long seeding pass.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`. NOT ADMISSIBLE: the bundle carries no reference
app, so nothing here has been compiled or run.
