# Build report - I_perso_trac_subscription-spend-tracker-vb_20260916_054233

Rendered from `_handoff/I_perso_trac_subscription-spend-tracker-vb_20260916_054233.gates.jsonl` and `I_perso_trac_subscription-spend-tracker-vb_20260916_054233.receipts.json`. No verdict below is transcribed or authored.

## Identity

| | |
|---|---|
| task code | `I_perso_trac_subscription-spend-tracker-vb_20260916_054233` |
| task id | `deku/subscription-spend-tracker-vb` |
| cell | individual / personal-finance / tracker-log |
| service_profile | P1-db |
| providers per slot | `backend` = postgres |
| variant | `b`, axes `critical_depth`, `spec_sections` |
| language | typescript |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 (no device sharding configured) |
| kit | deku-green-field, grader pin 0.22.0, target schema 1.4 |
| companion | `prds/subscrr.app_prd.md`, 70 headings, 251 enumerated items, 16 pinned colours |

## Feature resolution

| Candidate | Verdict | Where it landed | Reason |
|---|---|---|---|
| Subscriptions and the overview (companion 12) | INCLUDED | instruction.md `## Core features` rules 1-8 | the product's own home screen |
| Honest-math engine (13) | INCLUDED | `## Core features` rules 9-15 | the companion's expert tier and this task's hardest surface |
| Renewal dates and reminders (14) | INCLUDED | `## Core features` rules 16-21 | carries the pattern's critical focus |
| Import and portability (15) | INCLUDED | `## Core features` rules 22-26 | the companion's one-screenshot promise, re-cast as pasted text |
| Receipt reader (16) | INCLUDED | `## Core features` rules 27-30 | staged, with hash-only retention |
| Glanceable surfaces (17) | INCLUDED | `## Core features` rules 31-33 | four standalone routes |
| Premium and the paywall (18) | INCLUDED | `## Core features` rules 34-37 | the store-level cap |
| Insights (19) | INCLUDED | `## Core features` rules 38-41 | price-effective history is the graded item |
| Undo, bin and keyboard (20) | INCLUDED | `## Core features` rules 42-44 | batch collapse is the graded item |
| Sync, snapshot and erasure (21) | INCLUDED | `## Core features` rules 45-48 | two sessions and a versioned snapshot |
| The public site (2-10) | INCLUDED | `## Core features` rules 49-54 and `## Front-end specification` | the product's other half, not an eleventh feature |
| Offline after first visit (26) | DROPPED | waived to `source_lint.py` | needs a service worker, invisible over HTTP, and the runtime has no network to lose |
| Three-dimensional library (30.5) | DROPPED | waived | the companion records that it renders nothing |
| Native widget and watch surfaces (17) | DROPPED | re-cast as browser routes | the deliverable is a browser application |
| External help centre (2.1) | DROPPED | plain footer text | out of scope in the companion too, and unreachable at runtime |
| Frame-rate and paint bars (26) | DROPPED | waived | not deterministic under a grading run |
| Numbered build order (27) | DROPPED | `_spec/06-implementation-plan.md` only | a build sequence is forbidden outside `## Build plan`, which this variant does not emit |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | postgres | MET | `test_seeded_rows_are_stored_and_survive_a_restart_with_no_duplicates` reads the `subscription` rows out of the declared store; G32 green in `workflow_lint.py` |

## Graders

- workflows: **11**, inside the `individual` band of 6 to 11
- browser substeps: **35** · pytest substeps: **62** · critical substeps: **7**
- non-happy-path workflow ids: `"duplicate_reminder_pass_writes_no_second_entry"`, `"unauthenticated_app_requests_are_denied"`, `"seventh_subscription_beyond_the_free_cap_is_denied"`
- one pytest module, `tests/test_output.py`, carrying **62** test functions
- category mix: `business_rule` 18 · `core_outcome` 1 · `data_integrity` 18 · `presentation` 13 · `security` 6 · `validation` 6
- checklist items: **712**, every one cited (G24 green in both directions)

## Rubric

21 judged criteria, 19 positive and 2 negative, positive total 45.

| Dimension | Share | Target | Criteria |
|---|---|---|---|
| `instruction_following` | 0.311 | 0.30 | 5 |
| `functionality` | 0.244 | 0.25 | 3 |
| `ux_flow` | 0.156 | 0.15 | 3 |
| `ui_visual` | 0.156 | 0.15 | 4 |
| `motion` | 0.044 | 0.05 | 2 |
| `accessibility` | 0.044 | 0.05 | 2 |
| `responsiveness` | 0.044 | 0.05 | 2 |

`design_direction = "companion"` (reference/L S.L.6.1): the drawn direction `editorial-serif` is recorded and does not govern. R14 and R20 are whole-product criteria declared with `--waive-criterion`.

## Grading window

| Section | Chars | Target |
|---|---|---|
| Core features | 19355 | 2400 |
| User flow | 3412 | 1900 |
| UI/UX notes | 8496 | 1700 |
| Constraints | 1232 | 800 |
| User roles | 1450 | 1000 |
| Overview | 1548 | 700 |
| **joined six** | **35493** | 8800 |

`window_lint.py` reports length and fails nothing on it (G33). `## Core features`, `## User flow` and `## UI/UX notes` run past the judge's slice; no rule was cut to fit, per `generate_instruction.md` S.4.

## Literals ledger

181 entries: `account` 3 · `credential` 1 · `env_var` 3 · `fixture` 155 · `route` 19

| Value | Class | Carriers |
|---|---|---|
| `hello@driplog.app` | account | instruction.md, conftest.py |
| `user2@example.com` | account | instruction.md, conftest.py, workflows.yaml |
| `user@example.com` | account | instruction.md, conftest.py, workflows.yaml |
| `deku-demo-pw-2026` | credential | instruction.md, conftest.py |
| `APP_PUBLIC_PORT` | env_var | instruction.md, test_output.py, task.toml |
| `APP_PUBLIC_URL` | env_var | instruction.md, test_output.py, task.toml |
| `DATABASE_URL` | env_var | instruction.md, task.toml |
| `(C) 2026 Driplog. All rights reserved.` | fixture | instruction.md, conftest.py |
| `.browser_screenshots` | fixture | instruction.md, conftest.py |
| `.downloads` | fixture | instruction.md, conftest.py |
| `0.006740` | fixture | instruction.md, conftest.py |
| `0.2723` | fixture | instruction.md, conftest.py |
| `09:00` | fixture | instruction.md, conftest.py, test_output.py |
| `1.0850` | fixture | instruction.md, conftest.py |
| `1.2640` | fixture | instruction.md, conftest.py |
| `100` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `1000` | fixture | instruction.md, conftest.py, test_output.py |
| `1024` | fixture | instruction.md, conftest.py, test_output.py |
| `1099` | fixture | instruction.md, conftest.py |
| `1200` | fixture | instruction.md, conftest.py |
| `126219` | fixture | instruction.md, conftest.py |
| `131700` | fixture | instruction.md, conftest.py |
| `1499` | fixture | instruction.md, conftest.py |
| `1514633` | fixture | instruction.md, conftest.py |
| ... | | 157 further entries in `_handoff/I_perso_trac_subscription-spend-tracker-vb_20260916_054233.literals-ledger.json` |

## Authoring documents

| Document | Fed |
|---|---|
| `_spec/I_perso_trac_subscription-spend-tracker-vb_20260916_054233/00-decisions.md` | every residual call, the draws, the companion carry table |
| `_spec/I_perso_trac_subscription-spend-tracker-vb_20260916_054233/01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `_spec/I_perso_trac_subscription-spend-tracker-vb_20260916_054233/02-TRD.md` | `## Technical requirements` |
| `_spec/I_perso_trac_subscription-spend-tracker-vb_20260916_054233/03-app-flow.md` | `## User flow`, `## Deployment contract` API shapes |
| `_spec/I_perso_trac_subscription-spend-tracker-vb_20260916_054233/04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `_spec/I_perso_trac_subscription-spend-tracker-vb_20260916_054233/05-backend-schema.md` | `## Data model`, `## User roles` |
| `_spec/I_perso_trac_subscription-spend-tracker-vb_20260916_054233/06-implementation-plan.md` | authoring only; `## Build plan` is not emitted at this variant |

## Kit gate log

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS |
| G1/G12 | `layout_lint.py` | 0 | PASS |
| G46 | `structure_lint.py` | 1 | FAIL |
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
| G47 | `output_qc.py` | 1 | FAIL |

## Certification prompt receipts

| Prompt | Gate | Verdict | Checks answered | Verifier |
|---|---|---|---|---|
| `task_code_verifier.md` | G3 | VALID | 12 | self |
| `QC_instruction.md` | G34 | PASS | 24 | self |
| `QC_spec.md` | G34 | PASS | 15 | self |
| `qc_rubric.md` | G53 | PASS | 16 | self |
| `qc_solution_checklist.md` | G37 | PASS | 0 | self |
| `qc_docker.md` | G35 | PASS | 105 | self |
| `qc_toml.md` | G36 | PASS | 120 | self |

Every certification receipt is `verifier: self`. `prompt_receipt_lint.py` records that as SELF-ATTESTED rather than as an independent verdict, because a single-agent run cannot satisfy owner != verifier. Ten defects were raised and fixed across those passes; each is named in the receipts file.

## Blocking findings

- **G46** (`structure_lint.py`) exit 1: 
- **G47** (`output_qc.py`) exit 1: 

G46 is red for one reason and it is a placement choice, not a bundle defect: `structure_lint.py` resolves the generation kit as `tools/../..`, so every bundle under `GreenField-GenKit2` fails CON-1 whatever `output_root` says. The output root was set to `output_16sep` on the operator's instruction, and the two bundles already there carry the same red. Moving the output root beside the kit clears it; nothing inside this bundle changes.

## Budget

`turns_expected = 260`, `tokens_expected = 8000000`. The corpus baseline is 200 and 7.5M for a five-line order carrying three to six must-have features. This task carries ten, drawn from a companion, so both are raised; 8M is the documented absolute ceiling and the budget sits on it.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. No reference app exists, nothing here has been compiled or run, and no gate in battery 3 has been attempted. `solution/solve.sh` exits non-zero and says so.
