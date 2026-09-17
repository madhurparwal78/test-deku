# Build report - S_saasm_comm_founder-license-storefront-vb_20260916_101219

| Field | Value |
|---|---|
| Task code | `S_saasm_comm_founder-license-storefront-vb_20260916_101219` |
| Task id | `deku/founder-license-storefront-vb` |
| Cell | Greenfield / solo_founder / saas-micro-tools / commerce-checkout |
| Service profile | `P5-db-pay-email` (db `postgres`, email `mailpit`, payments `killbill`) |
| Variant | `b`, axes `critical_depth` and `spec_sections` |
| Language | typescript (SolidStart and Express on Node 20) |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Withheld | `## Build plan` (the variant b lever) |
| Shard | 1 of 1 |
| Kit | deku-green-field, GreenField-GenKit2 |
| Vendored grader | 0.22.0 |
| Target schema | 1.4 |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

MECHANICALLY-GREEN names the kit-run gates only. Of the seven certification prompts, `qc_docker`, `QC_spec` and `task_code_verifier` return clean; `qc_toml`, `QC_instruction`, `qc_solution_checklist` and `qc_rubric` return outstanding findings, each one recorded under Blocking findings with the owner of its repair. Three of those four are gate-against-gate or prompt-against-variant conflicts rather than bundle defects; none is silently carried.

## Source resolution

| Input | Given | Resolved | Why |
|---|---|---|---|
| domain | `saas-productivity` | `saas-micro-tools` | the given value is not in the taxonomy; G0 rejected it and this is the solo_founder domain the product sits in |
| pattern | `transactional-checkout` | `commerce-checkout` | same reason; it is the pattern whose mandatory slots are db and payments |
| everything else | as given | unchanged | archetype, variant, category, both identities |

Companion source: `PRD/lineaprompt_prd.md`, recorded in `_handoff/S_saasm_comm_founder-license-storefront-vb_20260916_101219.sources.json` and carried by G51 (139 topics, 508 items, 21 colours, all present).

## Coverage

- checklist items: **658**  `C-CF` 154  `C-CN` 4  `C-DC` 11  `C-DM` 47  `C-FE` 287  `C-OV` 6  `C-RL` 17  `C-TR` 33  `C-UF` 53  `C-UX` 46
- item classes: capability 170, constraint 105, contract 11, data 36, literal 182, role 16, ui 138
- pytest tests: **68**, discharging 516 item citations
- browser substeps: **38**, rubric criteria: **27** over 110 item citations
- G24 two-way coverage holds: every item is cited by pytest, the browser channel or the rubric, and every citation resolves

## Workflows

- workflows: **16** (solo_founder band 10 to 16)
- substeps: **38** browser, **68** pytest, ratio 0.56
- categories: business_rule 12, core_outcome 2, data_integrity 10, notification 1, presentation 28, security 10, validation 5
- critical substeps: **6**

| Workflow | Critical test |
|---|---|
| `visitor_registers_for_the_beta` | `test_access_link_email_goes_to_the_registrant_only` |
| `registrant_opens_the_access_link_and_reaches_the_download` | `test_access_link_opens_a_session_and_reports_the_founder_place` |
| `founder_places_survive_concurrent_registration` | `test_concurrent_registrations_store_distinct_contiguous_places` |
| `founder_places_survive_concurrent_registration` | `test_founder_place_opens_one_billing_account_in_killbill` |
| `founder_checkout_cannot_open_before_launch` | `test_checkout_before_launch_is_refused_and_creates_no_billing_record` |
| `operator_endpoints_are_denied_to_a_registrant` | `test_operator_endpoints_are_denied_to_a_visitor_and_a_registrant` |

- non-happy-path ids: `duplicate_registration_is_absorbed`, `invalid_registration_is_refused`, `access_link_opens_at_most_five_times`, `expired_access_link_is_refused`, `founder_places_survive_concurrent_registration`, `founder_cohort_limit_closes_at_one_thousand`, `founder_checkout_cannot_open_before_launch`, `operator_endpoints_are_denied_to_a_registrant`
- one pytest module, `tests/test_output.py`, covering core features, data integrity, authorization, edge cases and the three declared slots, with the rendered surfaces driven through a real Chromium page.

## Rubric

- criteria: **27**, all positive, scores summing to 45
- type share: 21/27 task completion

| Dimension | Share | Target | Criteria |
|---|---|---|---|
| instruction_following | 0.267 | 0.30 | 4 |
| functionality | 0.222 | 0.25 | 4 |
| ux_flow | 0.178 | 0.15 | 6 |
| ui_visual | 0.156 | 0.15 | 5 |
| motion | 0.067 | 0.05 | 3 |
| accessibility | 0.044 | 0.05 | 2 |
| responsiveness | 0.067 | 0.05 | 3 |

The judged rubric grades only what no pytest assertion and no browser substep observes: material, palette roles, motion character, typography, the instrument behaviours a screenshot can settle, and the narrow-viewport layout.

## Literals ledger

- entries: **99** (config 3, copy 57, credential 4, enum 4, fixture 23, header 3, identifier 5)
- every graded value is pinned verbatim in `instruction.md`; the two verifier-only values (the admin database URL and the inbox API URL) appear in neither the brief nor `[environment].env`.
- provider credentials are read from the environment by the grader rather than pinned in `conftest.py`, so no credential ships inside the bundle.

## Spec documents

| File | Fed |
|---|---|
| `_spec/<code>/00-decisions.md` | the draw, the residual decisions, the companion carry table |
| `_spec/<code>/01-PRD.md` | Overview, User roles, Core features |
| `_spec/<code>/02-TRD.md` | Technical requirements, Deployment contract |
| `_spec/<code>/03-app-flow.md` | User flow, the route table, the journeys, the states |
| `_spec/<code>/04-uiux-brief.md` | UI/UX notes, Front-end specification |
| `_spec/<code>/05-backend-schema.md` | Data model, Seed data |
| `_spec/<code>/06-implementation-plan.md` | author reference only; the brief withholds the build plan at variant b |
| `_spec/<code>/task-order.yaml` | the resolved Task Order this run was built from |

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Core features | 10208 | 2400 | past-slice |
| User flow | 4524 | 1900 | past-slice |
| UI/UX notes | 4695 | 1700 | past-slice |
| Constraints | 978 | 800 | over-reference |
| User roles | 1866 | 1000 | over-reference |
| Overview | 1875 | 700 | over-reference |
| joined total | 24146 | 8800 | past-slice |
| first four | 20405 | 7100 | over-reference |

G33 reports length and never fails it. The prose past the slice reaches the agent in full and the judge in part, which is why every judged criterion carries its own facts rather than pointing at the brief.

## Certification receipts

| Prompt | Gate | Verdict | Checks | Findings |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | CHANGES REQUIRED | 24 | 11 |
| `QC_spec.md` | G34 | PASS | 15 | 7 |
| `qc_docker.md` | G35 | PASS | 105 | 1 |
| `qc_rubric.md` | G53 | FAIL | 16 | 5 |
| `qc_solution_checklist.md` | G37 | PASS | 5 | 2 |
| `qc_toml.md` | G36 | CHANGES REQUIRED | 120 | 8 |
| `task_code_verifier.md` | G3 | VALID | 12 | 0 |

Each receipt carries the bundle-bound token, a verdict for every check id the prompt declares, and the findings that verdict rests on. The reviews ran as independent agents, so no receipt is self-attested by the author of the artifact it judges.

## Kit gate log

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
| G59/G60 | `codequality_lint.py` | 2 | NOT-APPLICABLE |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 0 | PASS |

Rendered from `_handoff/S_saasm_comm_founder-license-storefront-vb_20260916_101219.gates.jsonl`. Every gate is green.

## Blocking findings

Each of these is recorded rather than repaired, and each names who owns the repair.

- **No reference application.** The bundle ships NO-SOLUTION, so `solution/solve.sh` is a loud-fail stub and every oracle gate is undecided. Owner: the downstream build, STEP 0 of the handoff.
- **G39's implementation against G39's own design, surfacing as qc_rubric RC-04 and RC-12.** The gate index and `rubric_align_lint.py` both describe the reverse direction as exempting DETERMINISTIC items, but the code exempts on the `ui` TAG alone, and a tag cannot carry that distinction: `C-FE-31` (uppercase labels under thirteen pixels carry open letter spacing) and `C-FE-32` (display sizes scale with the viewport) are tagged `ui` and are computed exactly by a committed Playwright assertion. So ten such items must be held by the rubric, and RC-04 objects that the rubric then restates a committed test. The recommended repair is NOT to broaden G39 to accept any pytest test, which would let an API assertion stand in for a visual one, but to exempt a `ui` item when the pytest-provenance sidecar shows a committed assertion already grades it; the lint already reads that sidecar for its forward direction. Owner: `rubric_align_lint.py` with INV7.
- **qc_toml VERIF-005.** The kit template pins the verifier-side APP_PUBLIC_URL default at `http://localhost:4173`, which is what this bundle carries. Under the separate verifier mode the kit now defaults to, that default resolves inside the grader container rather than at the app, so it only holds while the harness injects the variable. Every other verifier-side default addresses a sidecar by compose service name. Owner: `toml_generator.md` section 10.4, with the handoff naming the one-value change if an oracle run reports the app unreachable.
- **G17 against reference/C C.2.** `PAYMENTS_ADMIN_USER` and `PAYMENTS_ADMIN_PASSWORD` are agent-visible by the service matrix and rejected in `[environment].env` by `secret_hygiene_lint`. They reach the agent through the compose `main` service instead, which satisfies both. Owner: `secret_hygiene_lint.py`, whose own docstring exempts payments credentials while its regex does not.
- **QC_instruction A1 and B3.** Both read for a `## Build plan` unconditionally. It is withheld here because variant b withholds it, and `[metadata].spec_sections_given` says so. Owner: `QC_instruction.md`, one amendment reading the section set from the toml.
- **QC_instruction B2.** The pattern's critical focus is an invoice on the account with the right amount. This product takes no money before 1.0: Kill Bill holds one account per founder place and no invoice, subscription or payment method is created anywhere. Asserting an invoice would contradict the source PRD. Recorded as a deviation from reference/B B.1, already logged in `_spec/<code>/00-decisions.md`.
- **QC_instruction C7, the grading window.** Measured: `## Core features` is 10,208 characters against a 2,400 reference, and the six-section join is past the judge's slice, so `## Overview` reaches the judge at nothing and `## User roles` at 522 of 1,866. Accepted rather than repaired: G33 reports length and never fails it, every judged criterion carries its own facts under G52, and 658 checklist items cite brief positions by `src:`, so moving prose between H2s would land the repair cost on the coverage gates. Owner: a future S2 pass that front-loads the graded rules.
- **No cohort boundary in the seed.** Proving the closed state costs about a thousand registrations, which is what the last pytest test does. A seeded near-cap fixture would make it cheap and would also change the product story. Owner: S3, if the runtime cost proves unacceptable downstream.

## Estimates

- `turns_expected = 150`: sixteen content surfaces, a seven-instrument front end, the cohort ledger and three providers, against the 120 a two-surface task takes.
- `tokens_expected = 6000000`: the brief is 24k characters of specification and the build spans a frontend, an API, a schema and three integrations.
- `difficulty = hard`: concurrency with a hard cap, an emailed credential, a signed feed and a launch surface, none of which an agent can fake past the graders.

## Handoff

See `_handoff/S_saasm_comm_founder-license-storefront-vb_20260916_101219.handoff.md` for the gate list the downstream build owns, in order, with the expected verdicts.
