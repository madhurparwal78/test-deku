# Build report: S_ecomm_crud_sustainable-outdoor-catalogue-vb_20260916_100714

## Identity

| Field | Value |
|---|---|
| Task code | `S_ecomm_crud_sustainable-outdoor-catalogue-vb_20260916_100714` |
| Task id | `deku/sustainable-outdoor-catalogue-vb` |
| Cell | solo_founder / ecommerce-retail / crud-catalog |
| Pattern note | the order named `catalog-browse`, which is not in the pattern table (G0); corrected to `crud-catalog` on the requester's instruction |
| Service profile | `P2-db-email` |
| Providers | `backend` = `postgres`, `email` = `mailpit` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `typescript` (NestJS API, Lit with Vite front end, both drawn) |
| Design direction | `companion` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 (single-task run) |
| Companion | `9.16_prds/prd7/floema_prd.md`, 9,714 lines |
| Reference site | https://www.floema.com/en |
| QL | kaustubh.dalvi@ethara.ai |
| Contributor | mansa.gupta@ethara.ai |

## Feature resolution

| Candidate | Verdict | Where |
|---|---|---|
| Staff sign-in | INCLUDED | `## Core features` rules 1 to 5 |
| Localisation: four locales and their addresses | INCLUDED | `## Core features` rules 6 to 16 |
| The catalogue | INCLUDED | `## Core features` rules 17 to 30 |
| Collections | INCLUDED | `## Core features` rules 31 to 35 |
| The product route | INCLUDED | `## Core features` rules 36 to 48 |
| The options modal | INCLUDED | `## Core features` rules 49 to 56 |
| The wishlist | INCLUDED | `## Core features` rules 57 to 66 |
| The quotation request | INCLUDED | `## Core features` rules 67 to 82 |
| Gated file requests | INCLUDED | `## Core features` rules 83 to 92 |
| The newsletter | INCLUDED | `## Core features` rules 93 to 101 |
| Contact enquiries and abuse controls | INCLUDED | `## Core features` rules 102 to 114 |
| Delivery and mail, for two audiences (the visitor and the staff) | INCLUDED | `## Core features` rules 115 to 122 |
| Search | INCLUDED | `## Core features` rules 123 to 130 |
| Journal, careers and pages | INCLUDED | `## Core features` rules 131 to 145 |
| Consent, privacy and legal pages (one privacy regime: the EU general data protection regulation) | INCLUDED | `## Core features` rules 146 to 153 |
| Not-found and error pages | INCLUDED | `## Core features` rules 154 to 158 |
| The back office | INCLUDED | `## Core features` rules 159 to 170 |
| Hosted headless content store, editing interface, drafts, previews | DROPPED | `## Constraints`; `00-decisions.md`: no content provider in the closed world; content is seeded, publish and unpublish survive |
| Sales platform delivery | DROPPED | `## Constraints`; `00-decisions.md`: re-cast onto the new-enquiry notification in Mailpit |
| Recruitment platform, job applications | DROPPED | `## Constraints`; `00-decisions.md`: seeded positions link out; no application data accepted |
| Consent vendor, analytics relay, funnel measurement | DROPPED | `## Constraints`; `00-decisions.md`: first-party consent with an append-only receipt; no processor to relay to |
| Per-client-network rate bucket | DROPPED | `## Constraints`; `00-decisions.md`: every visitor reaches the app from one address here, so it cannot be enforced honestly |
| Prices, cart, checkout, payments | DROPPED | `## Constraints`; `00-decisions.md`: out of scope for a quotation catalogue |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | quotation, quotation_item, lead, file_request, subscriber, consent_receipt, audit_event and staff_account rows are read directly by the pytest module |
| `email` | `mailpit` | MET | quotation, enquiry, file-link and double opt-in messages are read from the Mailpit API; staff notifications are checked for the no-contents rule |

## Grading surface

- Workflows: **16** (solo_founder band 10 to 16)
- Browser substeps: **58**   pytest substeps: **118**   critical substeps: **8**
- Non-happy-path workflow ids: `duplicate_quotation_submit_creates_one_enquiry`, `invalid_form_input_is_refused_inline`, `repeated_contact_submissions_hit_the_limit`, `editor_is_denied_enquiry_contents`, `unauthenticated_caller_cannot_reach_the_office`
- One pytest module, `tests/test_output.py`, carrying **118** test functions
- Rubric criteria: **19** (18 positive, 1 negative)
- Solution checklist: **659** items in `solution/checklist.md`

| Dimension | Share |
|---|---|
| `instruction_following` | 0.35 |
| `functionality` | 0.29 |
| `ux_flow` | 0.13 |
| `ui_visual` | 0.07 |
| `motion` | 0.05 |
| `accessibility` | 0.05 |
| `responsiveness` | 0.05 |

## Literals ledger

261 pinned values across 11 classes, every one present verbatim in `instruction.md`; verifier-only values carry `task.toml` alone.

| Class | Count |
|---|---|
| `account` | 3 |
| `credential` | 1 |
| `design_phrase` | 9 |
| `endpoint` | 55 |
| `env_var` | 7 |
| `motion_moment` | 5 |
| `number` | 10 |
| `route` | 31 |
| `scheme` | 18 |
| `seed_record` | 95 |
| `status` | 27 |

## Authoring documents

| Document | Fed |
|---|---|
| `00-decisions.md` | the draw record, input correction, scope calls and the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at baseline |

## Grading window

| Section | Chars |
|---|---|
| Overview | 2688 |
| User roles | 2240 |
| Core features | 52892 |
| User flow | 6264 |
| UI/UX notes | 8895 |
| Technical requirements | 7215 |
| Data model | 10467 |
| Front-end specification | 41491 |
| Constraints | 1438 |
| Deployment contract | 7520 |
| Definition of done | 533 |

The order waived per-section caps. The brief carries no length limit and `window_lint.py` fails nothing on length; prose past the judge's slice still reaches the agent in full.

## UI/UX carriage

Per the order and `generation_instruction_guidelines (1).md`, the visual system is described in words only: no pixel values, positions, sizes, colour codes, animation or motion names, function names or parameter values appear in the brief. Tech stacks are named. Accessibility floors (contrast ratios) stay numeric.

## Kit gate log

Rendered from `_handoff/S_ecomm_crud_sustainable-outdoor-catalogue-vb_20260916_100714.gates.jsonl`. Never transcribed.

| Gate | Tool | Exit | Verdict | Evidence |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | 24 input file(s) hashed |
| `G1/G12` | `layout_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G46` | `structure_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G50` | `docker_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G63` | `secret_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G48` | `truth_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G51` | `source_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G52` | `rubric_context_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G54` | `comment_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G11` | `leak_scan.py` | 0 | PASS | 24 input file(s) hashed |
| `G33` | `window_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G4/G5` | `contract_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G43` | `prescription_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G44` | `disclosure_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G10` | `no_sdk_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G31` | `determinism_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G14` | `reward_path_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G41` | `flag_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G59/G60` | `codequality_lint.py` | 2 | ? | 24 input file(s) hashed |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G6` | `fixture_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G24` | `coverage_map.py` | 0 | PASS | 24 input file(s) hashed |
| `G37` | `checklist_qc.py` | 0 | PASS | 24 input file(s) hashed |
| `G39` | `rubric_align_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G28/G29` | `channel_lint.py` | 0 | PASS | 24 input file(s) hashed |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | 24 input file(s) hashed |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | 24 input file(s) hashed |
| `G47` | `output_qc.py` | 0 | PASS | 24 input file(s) hashed |

`G59/G60` exits 2 (NOT-APPLICABLE): the bundle carries no reference code to lint.

## Certification prompt receipts

| Prompt | Gate | Verdict | Checks | Verifier |
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

Every certification verdict above is **SELF-ATTESTED**: the same agent authored the artefact and ran the reviewer, so owner and verifier are one identity. That is a recorded verdict, never an independent one. Findings raised on those runs:

- `QC_instruction.md` A1: ten canonical H2s plus `## Front-end specification`; `## Build plan` is not emitted at baseline (generate_instruction.md 2.1)
- `QC_instruction.md` B3: two levers emitted (`## Technical requirements`, `## Data model`); `## Build plan` is excluded at baseline by 2.1
- `QC_instruction.md` C7: `## Core features` and `## Front-end specification` run long by design (170 numbered rules, per-surface UI prose); the order waived section caps and G33 sets no length limit
- `docker_generator.md` advisory receipt: the prompt was read end to end before authoring; it declares no check registry, so the scorecard is the verdict alone
- `generate_instruction.md` advisory receipt: the prompt was read end to end before authoring; it declares no check registry, so the scorecard is the verdict alone
- `pytest_generator.md` advisory receipt: the prompt was read end to end before authoring; it declares no check registry, so the scorecard is the verdict alone
- `qc_docker.md` BP-004: the Node 20 repository is authenticated by the dearmoured signing key in /etc/apt/keyrings rather than by a per-artifact checksum, which is the integrity mechanism apt itself provides
- `qc_toml.md` TAX-008: archetype `sustainable-outdoor-catalogue` is unclaimed in the task 7 ledger.jsonl; global uniqueness cannot be proved from these inputs
- `qc_toml.md` BENCH-003/BENCH-005: difficulty is the required calibration placeholder, so the turns/tokens band cannot be evaluated; turns_expected 200 and tokens_expected 8000000 sit at the top of the documented range
- `rubric_author.md` advisory receipt: the prompt was read end to end before authoring; it declares no check registry, so the scorecard is the verdict alone
- `solution_checklist.md` advisory receipt: the prompt was read end to end before authoring; it declares no check registry, so the scorecard is the verdict alone
- `toml_generator.md` advisory receipt: the prompt was read end to end before authoring; it declares no check registry, so the scorecard is the verdict alone

## Blocking findings

- None inside the kit's reach. Every battery-1 and battery-2 gate is green.
- The companion supplies far more product than one agent budget can build. `## Constraints` records what was scoped out, and `_spec/S_ecomm_crud_sustainable-outdoor-catalogue-vb_20260916_100714/00-decisions.md` carries the companion carry table. 59 G51 waivers are declared in `_spec/S_ecomm_crud_sustainable-outdoor-catalogue-vb_20260916_100714/g51-waivers.txt`.

## Versions

| Field | Value |
|---|---|
| Kit | `deku-green-field` |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Harbor | `0.20.0` |
| Verifier mode | `separate` |

## Execution budget

`turns_expected = 200`, `tokens_expected = 8000000`. Four locales, two backing services, 170 numbered rules, a back office and a large front-end specification put this at the top of the documented band.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference app. Nothing counts toward corpus targets until the app lands downstream and `harbor run -a oracle` returns `1.0` twice.
