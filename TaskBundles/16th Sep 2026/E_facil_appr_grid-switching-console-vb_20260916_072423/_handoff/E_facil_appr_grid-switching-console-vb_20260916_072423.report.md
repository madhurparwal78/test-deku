# Build report: E_facil_appr_grid-switching-console-vb_20260916_072423

## Identity

| Field | Value |
|---|---|
| Task code | `E_facil_appr_grid-switching-console-vb_20260916_072423` |
| Task id | `deku/grid-switching-console-vb` |
| Cell | enterprise / facilities-assets / approval-workflow |
| Service profile | `P3-db-auth` |
| Providers | `backend` = `postgres`, `auth` = `keycloak` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `typescript` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 (single-task run) |
| Companion | `9.16_prds/prd5/switchyard-prd.md`, 5,940 lines |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Sign-in through the identity provider | INCLUDED | `## Core features` Auth | the auth slot is declared and the companion forbids a product-held password |
| Versioned network model with two-person publication | INCLUDED | `## Core features` rules 13 to 23 | the companion binds every artefact to an immutable model version |
| Live measurements with a mandatory quality flag | INCLUDED | `## Core features` rules 24 to 31 | permit validation reads quality, so the flag is load-bearing |
| Alarms with a server-computed ranking | INCLUDED | `## Core features` rules 32 to 43 | the companion computes priority server-side and forbids a client value |
| Incidents with command transfer and blocked closure | INCLUDED | `## Core features` rules 44 to 58 | the closure blockers are the companion's own list |
| Switching orders: study, approval, execution | INCLUDED | `## Core features` rules 59 to 109 | the pattern's critical focus and the task order's own sentence |
| Isolation permits validated from telemetry | INCLUDED | `## Core features` rules 110 to 123 | the companion's safety-document rule, carried whole |
| Crew dispatch with a single-claim lease | INCLUDED | `## Core features` rules 124 to 126 | a second contention surface the companion states |
| Append-only hash-chained record | INCLUDED | `## Core features` rules 127 to 135 | mandatory for the enterprise category |
| Shift handover with mandatory dispositions | INCLUDED | `## Core features` rules 136 to 141 | the companion's J-008 journey |
| Launch surface: terms, cookie choice, form validation, spam refusal, alt text | INCLUDED | `## Core features` rules 142 to 148, `## UI/UX notes` | the reference/O draw for this archetype |
| Contingency sweeps over thousands of cases | DROPPED | `## Constraints` | a fleet-scale planning capability with no bearing on the critical focus |
| Policy authoring and policy simulation | DROPPED | `## Constraints` | authorization here is a fixed role and area model, not a document a user writes |
| SCIM provisioning, SAML metadata, break-glass | DROPPED | `## Constraints` | no user-observable surface inside one seeded tenant |
| eDiscovery export, legal hold, DLP | DROPPED | `## Constraints` | the record is readable and recomputable in-product and is not exported |
| Media, webhooks, notifications, search, reliability reporting | DROPPED | `## Constraints` | no declared slot serves them in the closed provider world |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | 24 critical and non-critical pytest substeps read rows directly; G32 slot vocabulary satisfied by `test_seeded_rows_survive_a_re_read`, `test_seeding_is_idempotent` and others |
| `auth` | `keycloak` | MET | `test_operator_login_returns_access_token` is the slot's critical substep; `test_malformed_token_is_denied` and the six authorization tests observe the boundary |

## Grading surface

- Workflows: **21** (enterprise band 13 to 23)
- Browser substeps: **33**   pytest substeps: **59**   critical substeps: **20**
- Non-happy-path workflow ids: `unauthenticated_caller_is_denied_every_surface`, `invalid_suppression_is_refused`, `operator_cannot_approve_an_order`, `self_approval_at_risk_class_two_is_denied`, `operator_outside_the_area_is_denied`, `concurrent_execute_emits_one_instruction`, `concurrent_crew_assignment_leaves_one_holder`, `measurement_with_invalid_quality_is_refused`, `publishing_is_refused_while_an_order_executes`, `handover_with_an_undispositioned_item_cannot_submit`, `spam_submission_to_the_public_form_is_refused`, `empty_and_unknown_surfaces_answer_for_themselves`
- One pytest module, `tests/test_output.py`, carrying **59** test functions across the core-features, authorization, data-integrity and edge-case concerns
- Rubric criteria: **17** (16 positive, 1 negative)

| Dimension | Target | Share |
|---|---|---|
| `instruction_following` | 0.30 | 0.31 |
| `functionality` | 0.25 | 0.26 |
| `ux_flow` | 0.15 | 0.14 |
| `ui_visual` | 0.15 | 0.14 |
| `motion` | 0.05 | 0.05 |
| `accessibility` | 0.05 | 0.05 |
| `responsiveness` | 0.05 | 0.05 |

## Literals ledger

213 pinned values across 11 classes. Carriers are `instruction.md`, `tests/conftest.py` and `tests/test_output.py`; verifier-only values carry `task.toml` alone.

| Class | Count |
|---|---|
| `account` | 5 |
| `credential` | 1 |
| `design_phrase` | 10 |
| `endpoint` | 26 |
| `env_var` | 11 |
| `motion_moment` | 6 |
| `number` | 36 |
| `route` | 15 |
| `scheme` | 9 |
| `seed_record` | 20 |
| `status` | 74 |

## Authoring documents

| Document | Fed |
|---|---|
| `00-decisions.md` | the draw record and the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at baseline |

## Grading window

| Section | Chars | Reference |
|---|---|---|
| Core features | 21953 | 2400 |
| User flow | 7281 | 1900 |
| UI/UX notes | 14634 | 1700 |
| Constraints | 2893 | 800 |
| User roles | 3408 | 1000 |
| Overview | 2826 | 700 |

The brief carries no length limit and `window_lint.py` fails nothing on length. Prose past the judge's 2,500-character slice still reaches the agent in full; `judge_score` never touches reward.

## Kit gate log

Rendered from `_handoff/E_facil_appr_grid-switching-console-vb_20260916_072423.gates.jsonl`. Never transcribed.

| Gate | Tool | Exit | Verdict | Evidence |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | 25 input file(s) hashed |
| `G1/G12` | `layout_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G46` | `structure_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G50` | `docker_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G63` | `secret_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G48` | `truth_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G51` | `source_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G52` | `rubric_context_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G54` | `comment_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G11` | `leak_scan.py` | 0 | PASS | 25 input file(s) hashed |
| `G33` | `window_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G4/G5` | `contract_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G43` | `prescription_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G44` | `disclosure_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G10` | `no_sdk_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G31` | `determinism_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G14` | `reward_path_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G41` | `flag_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G59/G60` | `codequality_lint.py` | 2 | ? | 25 input file(s) hashed |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G6` | `fixture_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G24` | `coverage_map.py` | 0 | PASS | 25 input file(s) hashed |
| `G37` | `checklist_qc.py` | 0 | PASS | 25 input file(s) hashed |
| `G39` | `rubric_align_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G28/G29` | `channel_lint.py` | 0 | PASS | 25 input file(s) hashed |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | 25 input file(s) hashed |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | 25 input file(s) hashed |
| `G47` | `output_qc.py` | 0 | PASS | 25 input file(s) hashed |

## Certification prompt receipts

| Prompt | Gate | Verdict | Checks | Verifier |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | self |
| `QC_spec.md` | G34 | PASS | 15 | self |
| `generate_instruction.md` | S2 | PASS | 0 | self |
| `qc_docker.md` | G35 | PASS | 105 | self |
| `qc_rubric.md` | G53 | PASS | 16 | self |
| `qc_solution_checklist.md` | G37 | PASS | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | self |
| `task_code_verifier.md` | G3 | VALID | 12 | self |

Every certification verdict above is **SELF-ATTESTED**: the same agent authored the artefact and ran the reviewer, so owner and verifier are one identity. That is a recorded verdict, never an independent one. Findings raised on those runs:

- `QC_instruction.md` A1: ten canonical H2s plus `## Front-end specification`; `## Build plan` is not emitted at baseline (generate_instruction.md 2.1, reference/A A.7)
- `QC_instruction.md` A8: the brief reads AUTH_URL, AUTH_REALM, AUTH_CLIENT_ID and AUTH_CLIENT_SECRET for the declared auth slot; reference/C C.2 owns that split
- `QC_instruction.md` B3: two levers emitted (`## Technical requirements`, `## Data model`); `## Build plan` is excluded at baseline by 2.1
- `QC_instruction.md` C7: `## Core features` 21,953 chars, `## UI/UX notes` 14,634, `## User flow` 7,281 run past the judge's slice; the brief has no length limit (G33) and judge_score never touches reward
- `generate_instruction.md` advisory receipt: the prompt was read end to end before authoring; it declares no check registry, so the scorecard is the verdict alone
- `qc_docker.md` BP-004: the Node 20 repository is authenticated by the dearmoured signing key in /etc/apt/keyrings rather than by a per-artifact checksum, which is the integrity mechanism apt itself provides
- `qc_toml.md` TAX-008: archetype `grid-switching-console` is unclaimed in Output/ledger.jsonl; global uniqueness across 3,335 archetypes cannot be proved from these inputs
- `qc_toml.md` BENCH-003/BENCH-005: difficulty is the required calibration placeholder, so the turns/tokens band cannot be evaluated; turns_expected 200 and tokens_expected 8000000 sit at the top of the documented range

## Blocking findings

- None inside the kit's reach. Every battery-1 and battery-2 gate is green.
- The companion supplies far more product than one agent budget can build. `## Constraints` records what was scoped out, and `_spec/<code>/00-decisions.md` carries the companion carry table with a waiver and a reason for every dropped subject. 140 G51 waivers are declared in `_spec/<code>/g51-waivers.txt`.

## Versions

| Field | Value |
|---|---|
| Kit | `deku-green-field` |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Harbor | `0.20.0` |
| Verifier mode | `separate` |

## Execution budget

`turns_expected = 200`, `tokens_expected = 8000000`. Eleven core features, four roles, two backing services, 62 numbered rules and a large front-end specification put this at the top of the documented band; `tokens_expected` sits at the absolute ceiling rather than above it.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference app. Nothing counts toward corpus targets until the app lands downstream and `harbor run -a oracle` returns `1.0` twice.
