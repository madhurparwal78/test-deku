# Build report: S_ecomm_crud_consumer-device-catalogue-vb_20260916_063649

| | |
|---|---|
| Task code | `S_ecomm_crud_consumer-device-catalogue-vb_20260916_063649` |
| Task id | `deku/consumer-device-catalogue-vb` |
| Cell | solo_founder / ecommerce-retail / crud-catalog |
| Service profile | `P2-db-email` |
| Providers | `backend = postgres`, `email = mailpit` |
| Variant | `b` on `spec_sections`, `critical_depth`, `data_shape` |
| Language | `python` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field, gate battery G0 to G63 |
| Grader pin | `0.22.0` |
| Target schema | `1.4` |
| Verifier mode | `shared` |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Source

One companion document was supplied with the Task Order, a 2,924-line build
specification for a consumer device catalogue. `source_lint.py` (G51) reports
**169 of 169 topics** and **529 of 529 enumerated items** carried into
`instruction.md`, with six declared waivers recorded in `_spec/<code>/00-decisions.md`.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Family listing, facets, sort | INCLUDED | `## Core features` | the pattern's browse surface; graded by three pytest checks and one workflow |
| Variant resolution with a matrix hole | INCLUDED | `## Core features` | the critical focus; graded critical |
| Per-variant buy route, three modes | INCLUDED | `## Core features` | the companion's central mechanic; all three modes seeded |
| Cart held server side, checkout handover | INCLUDED | `## Core features` | persistence is observable; the payment step stays outside |
| Device registration | INCLUDED | `## Core features` | the durable workflow; graded critical |
| Support request with idempotency | INCLUDED | `## Core features` | the email slot's critical substep |
| Article helpfulness vote | INCLUDED | `## Core features` | update-not-insert is a clean data-integrity observation |
| Reading routes and the not-found ladder | INCLUDED | `## Core features` | the companion's largest surface; judged plus one pytest check |
| Launch surface: favicon, meta, social, sitemap, robots, no frontend secrets | INCLUDED | `## Technical requirements` | the reference/O draw, six pytest checks |
| Payment step | DROPPED | - | the companion places it on a separate origin and stops at the handover |
| Community forum, careers, experiments | DROPPED | - | external origins; rendered as outbound anchors only |
| Third-party analytics, consent, tag stack | DROPPED | - | no run-time third-party call is available; the outbound-click record survives |
| Order history | DROPPED | - | the companion records the account origin as captured signed out only |
| `## Build plan` | DROPPED | - | not baseline (generate_instruction.md section 2.1) |

## Slot obligations

| Slot | Provider | Status | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_registration_is_persisted_and_survives_a_reread` (critical), `test_resolved_variant_persisted_row_matches_the_api` (critical), plus five further row assertions |
| `email` | `mailpit` | MET | `test_support_request_delivers_one_confirmation_email` (critical), `test_duplicate_support_request_sends_no_second_confirmation_email`, `test_device_registration_sends_no_mail` |

No slot is UNMET.

## Grading surface

| Workflows | 15 (solo_founder band 10 to 16) |
|---|---|
| Browser substeps | 24 |
| Pytest substeps | 36 |
| Critical substeps | 7 |
| Non-happy-path ids | 7: `empty_family_listing_carries_no_products`, `invalid_address_answers_not_found`, `duplicate_support_request_sends_no_second_confirmation`, `anonymous_registration_is_denied`, `cross_account_support_request_is_forbidden`, `serial_already_held_cannot_be_registered`, `invalid_serial_is_refused` |
| Pytest module | one, `tests/test_output.py`, 36 functions |
| Rubric criteria | 21 (18 positive, 3 negative) |
| Checklist items | 325 |

Sections the one module covers: core features, data integrity, authorization,
edge cases, email.

### Rubric dimension shares, against the frozen targets

| Dimension | Positive points | Share | Target | Delta |
|---|---|---|---|---|
| `instruction_following` | 15 | 0.268 | 0.30 | 0.032 |
| `functionality` | 14 | 0.250 | 0.25 | 0.000 |
| `ux_flow` | 8 | 0.143 | 0.15 | 0.007 |
| `ui_visual` | 9 | 0.161 | 0.15 | 0.011 |
| `motion` | 4 | 0.071 | 0.05 | 0.021 |
| `accessibility` | 3 | 0.054 | 0.05 | 0.004 |
| `responsiveness` | 3 | 0.054 | 0.05 | 0.004 |

## Literals ledger

| Class | Count |
|---|---|
| `account` | 2 |
| `credential` | 1 |
| `design_phrase` | 10 |
| `endpoint` | 19 |
| `env_var` | 10 |
| `motion_moment` | 8 |
| `number` | 12 |
| `route` | 26 |
| `scheme` | 6 |
| `seed_record` | 48 |
| `status` | 33 |

175 pinned values. Two are `verifier_only` and appear in `task.toml`
`[verifier].env` alone: `DB_ADMIN_URL` and `EMAIL_INBOX_API_URL`. Every other value
appears verbatim in `instruction.md`, and `fixture_lint.py` (G6) proves the
bijection in both directions against the grader files.

## Authoring documents

| Document | Fed |
|---|---|
| `00-decisions.md` | every residual call, the eight draws, the companion carry table, the six G51 waivers |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements`, `## Deployment contract` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing; `## Build plan` is not baseline |

## Grading window

| Section | Chars | Reference | Reaches the judge |
|---|---|---|---|
| `Core features` | 25663 | 2400 | first 2,500 |
| `User flow` | 7123 | 1900 | first 2,500 |
| `UI/UX notes` | 9187 | 1700 | first 2,500 |
| `Constraints` | 1166 | 800 | first 2,500 |
| `User roles` | 1868 | 1000 | first 2,500 |
| `Overview` | 3150 | 700 | first 2,500 |
| joined | 48157 | 8,800 | first 9,000 |

Every judged section runs past its reference length. `window_lint.py` (G33)
reports length and fails nothing, and the brief has no cap. What the judge does
not read is graded by the pytest layer or by a workflow substep instead; the
twenty-one judged criteria each carry their own facts and are decidable without
the brief, which `rubric_context_lint.py` (G52) checks.

## Kit gate log

Rendered from `_handoff/<code>.gates.jsonl`. Never transcribed. The sweep ran with the
output root sited as CON-1 requires, beside the generation kit rather than inside it.
This repository keeps `Output/` inside the kit tree, so a sweep re-run against the
delivered path adds one finding, `structure_lint` CON-1 placement, which every bundle
already in that directory carries for the same reason.

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

## Prompt receipts

`prompt_receipt_lint.py` (G40) reports WARN: every certification prompt carries a
receipt with a verdict for each check it declares, and every one is
**SELF-ATTESTED**. The kit's rule is owner is not verifier; one agent authored and
reviewed this bundle, so these are recorded verdicts rather than independent ones.
Fourteen checks across five prompts are recorded as WARN with their evidence, each
naming a place where a QC prompt predates a later rule the gates now enforce.

## Blocking findings

None inside the kit's reach. Two things this bundle cannot decide for itself:

- No image digests are pinned in `[delivery.images]`. Minting one needs registry
  access the kit does not have, and fabricating a digest is forbidden. The operator
  pins them at packaging time.
- Nothing here has been compiled or run. See the handoff contract.

## Budget

`turns_expected = 140`, `tokens_expected = 5000000`. The medium band. Reasoning:
two service slots, a fifteen-table model, three fulfilment modes with a deliberate
hole in the variant matrix, one durable workflow carrying ownership, uniqueness and
idempotency at once, and a front-end specification that is the largest single
section in the brief. `difficulty` stays empty; calibration owns it.

## Exit state

**MECHANICALLY-GREEN, NO-SOLUTION.** Not admissible. No reference application
exists, and nothing in this bundle has been built or executed.

