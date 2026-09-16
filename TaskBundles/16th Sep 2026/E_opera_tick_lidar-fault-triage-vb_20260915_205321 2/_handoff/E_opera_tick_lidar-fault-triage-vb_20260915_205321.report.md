# Build report: E_opera_tick_lidar-fault-triage-vb_20260915_205321

## Identity

| Field | Value |
|---|---|
| task code | `E_opera_tick_lidar-fault-triage-vb_20260915_205321` |
| task id | `deku/lidar-fault-triage-vb` |
| cell | enterprise / operations-field-service / ticketing-queue |
| service profile | `P2-db-email` |
| providers | backend = `postgres`, email = `mailpit` |
| variant | `b`, axes `critical_depth`, `spec_sections` |
| language | typescript (drawn stack: Fastify backend, Svelte + Vite frontend, spa-json-api) |
| spec_sections_given | overview, roles, features, flow, uiux, techrequirements, datamodel, constraints, contract |
| authors | QL `madhur.parwal@ethara.ai`, contributor `yasiraliint17@ethara.ai` |
| kit | deku-green-field, grader pin 0.22.0, schema 1.4 |
| turns / tokens | 170 / 7,000,000 (hard band: ten feature areas, a contention rule, an email slot, three roles) |

## Input

Link mode. `https://drone.riotters.com/` was captured by prd-generator (863 responses, 324
screenshots) into `Output/_prd/drone/`. The site is a single-page showcase for an inspection drone;
eleven other captured paths answered the framework's not-found page. The PRD (`drone_prd.md`) passed
all thirteen prd_lint gates and G65, and the plain PRD is the recorded companion.

## KIT GATE LOG (rendered from `_handoff/<code>.gates.jsonl`, 32 receipts, 24 input hashes each)

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | validate_task.py | 2 | NOT-APPLICABLE (schema and taxonomy hold; `[delivery]` absent, grandfathered) |
| G1/G12 | layout_lint.py | 0 | PASS |
| G46 | structure_lint.py | 0 | PASS |
| G50 | docker_lint.py | 0 | PASS |
| G55 | runtime_deps_lint.py | 0 | PASS |
| G63 | secret_lint.py | 0 | PASS |
| G48 | truth_lint.py | 0 | PASS |
| G51 | source_lint.py | 0 | PASS |
| G52 | rubric_context_lint.py | 0 | PASS |
| G54 | comment_lint.py | 0 | PASS |
| G17 | secret_hygiene_lint.py | 0 | PASS |
| G11 | leak_scan.py | 0 | PASS |
| G33 | window_lint.py | 0 | PASS |
| G4/G5 | contract_lint.py | 0 | PASS |
| G43 | prescription_lint.py | 0 | PASS |
| G44 | disclosure_lint.py | 0 | PASS |
| G10 | no_sdk_lint.py | 0 | PASS |
| G31 | determinism_lint.py | 0 | PASS |
| G14 | reward_path_lint.py | 0 | PASS |
| G27/G30 | rubric_lint.py | 0 | PASS |
| G41 | flag_lint.py | 0 | PASS |
| G56/G57/G58 | if_lint.py | 0 | PASS |
| G59/G60 | codequality_lint.py | 2 | NOT-APPLICABLE (no source criteria) |
| G7/G8/G9/G32/G45 | workflow_lint.py | 0 | PASS |
| G6 | fixture_lint.py | 0 | PASS |
| G24 | coverage_map.py | 0 | PASS |
| G37 | checklist_qc.py | 0 | PASS |
| G39 | rubric_align_lint.py | 0 | PASS |
| G28/G29 | channel_lint.py | 0 | PASS |
| G40 | prompt_receipt_lint.py | 0 | WARN (every receipt is self-attested) |
| G0/INV5 | vendor_check.py | 0 | PASS |
| G47 | output_qc.py | 0 | PASS |

G64 `run_lint.py` carries no receipt here: that tool arrives with kit commit 066e565 (PRD and
link mode), which is on `yasir-test` and not on `madhur-test`, where this sweep ran. The L8
verdicts below were recorded on the authoring kit, which had it.

Also run outside the sweep: G0 `taskorder_lint.py` PASS at S0, G3 `task_code.py decode` VALID at
S1, G38 `kit_selftest.py` PASS (32 checks), G65 `run_lint.py prd` PASS at L8.

## Slot obligation table

| Slot | Provider | Status | Evidence |
|---|---|---|---|
| db | postgres | MET | `test_pilot_logged_survey_faults_are_stored_as_open_rows` (critical) reads fault rows |
| email | mailpit | MET | `test_confirmed_fault_sends_one_email_to_the_site_owner` (critical) reads the owner's inbox |

## Feature resolution

| Feature | Verdict | Graded by |
|---|---|---|
| Staff sign in | INCLUDED | pytest security, browser |
| Site register | INCLUDED | pytest validation and role tests, browser |
| Survey log | INCLUDED | pytest data_integrity and validation, browser |
| Triage queue order and filter | INCLUDED | pytest business_rule, browser |
| Claim, single winner | INCLUDED | pytest data_integrity (8-round race), browser |
| Decisions | INCLUDED | pytest security and business_rule, browser |
| Owner email | INCLUDED | pytest notification |
| Operations overview | INCLUDED | pytest data_integrity, browser |
| Public landing page | INCLUDED | rubric |
| Page view record | INCLUDED | pytest business_rule |
| Point cloud viewer, video, flight control, processing-software integration, studio contact | DROPPED | declared in Constraints and the PRD scope |

## Grading surface

- Workflows: 13; browser substeps 19; pytest substeps 46; critical substeps 11; non-happy ids include
  `concurrent`, `invalid`, `denied`, `cannot`, `forbidden`, `unauthenticated`, `refused`.
- Pytest module: `tests/test_output.py`, 46 tests; categories security 12, validation 10,
  business_rule 9, data_integrity 8, notification 3, presentation 3, core_outcome 1.
- Rubric: 23 judged criteria, all positive; shares instruction_following 0.293, functionality 0.320,
  ux_flow 0.187, ui_visual 0.080, motion 0.040, accessibility 0.040, responsiveness 0.040.
- Answer key: `grounding.yaml` 11 trajectory steps whose checkers equal the 46 tests, 6 rejected routes,
  13 rubric items; generated `TRUTH.md`, `USER_README.md`, `rubrics.json`, `test_ans.py`,
  `tests/rubric.json`.
- Checklist: 126 items; traceability matrix 75 core asks, 134 graders, 0 not fully graded.

## Literals ledger

50 literals in `_handoff/<code>.literals-ledger.json`: 4 accounts, 1 credential, 5 seed records,
11 statuses and enums, 9 endpoints, 10 schemes and field names, 5 environment variables (2
verifier-only), 3 motion moments, 3 design phrases. G6 bijection PASS.

## spec docs

`Output/_spec/E_opera_tick_lidar-fault-triage-vb_20260915_205321/`: 00-decisions (draws, companion
overrides, carry table), 01-PRD, 02-TRD, 03-app-flow, 04-uiux-brief, 05-backend-schema,
06-implementation-plan.

## Grading window

Core features 6213, User flow 2961, UI/UX notes 4620, Constraints 822, User roles 1332, Overview 1120;
joined about 17000 against the 9000 slice. Reported, never failed; the judge does not read the tail.

## QC performed and repaired (prompt receipts, self-attested)

| Prompt | Gate | Checks | Verdict |
|---|---|---|---|
| task_code_verifier.md | G3 | 12 | VALID |
| QC_spec.md | G34 | 15 | PASS, 2 WARN |
| QC_instruction.md | G34 | 24 | PASS, 2 WARN |
| qc_toml.md | G36 | 120 | PASS, 2 repaired |
| qc_docker.md | G35 | 105 | PASS, 4 WARN, 3 repaired |
| qc_rubric.md | G53 | 16 | PASS, 1 WARN, 1 repaired |
| qc_solution_checklist.md | G37 | 0 | PASS |

Repairs: base image pinned to `python:3.12.7-slim-bookworm` (the floating tag resolves to trixie, where
`libasound2` is renamed and the build would fail); host ports removed from mailpit; `restart:` removed
from sidecars; `task.toml` description tightened; turns and tokens set to the hard band; brief now
commits to light mode; implementation plan gained a deploy exit; rubric R12 reworded to stay
affirmative.

## Handoff gate list (undecided)

G13, G15, G18, G19, G20, G21, G25. Commands in the handoff file.

## Blocking findings

None for the kit battery. The QC verdicts are self-attested (owner equals verifier).

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`. Not admissible until an app is built downstream and
`harbor run -a oracle` returns 1.0 twice.
