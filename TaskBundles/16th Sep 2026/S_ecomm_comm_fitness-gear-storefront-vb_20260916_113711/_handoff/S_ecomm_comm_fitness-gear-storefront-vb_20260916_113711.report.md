# Build report - deku/fitness-gear-storefront-vb

Task code: `S_ecomm_comm_fitness-gear-storefront-vb_20260916_113711`

Gates run: 32 | ok: 32 | red: 0

**ALL GATES GREEN.** Exit state MECHANICALLY-GREEN, NO-SOLUTION. NOT ADMISSIBLE until a reference app exists and `harbor run -a oracle` returns 1.0 twice.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | validate_task.py | 0 | PASS |
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
| G59/G60 | codequality_lint.py | 2 | ? |
| G7/G8/G9/G32/G45 | workflow_lint.py | 0 | PASS |
| G6 | fixture_lint.py | 0 | PASS |
| G24 | coverage_map.py | 0 | PASS |
| G37 | checklist_qc.py | 0 | PASS |
| G39 | rubric_align_lint.py | 0 | PASS |
| G28/G29 | channel_lint.py | 0 | PASS |
| G40 | prompt_receipt_lint.py | 0 | WARN |
| G0/INV5 | vendor_check.py | 0 | PASS |
| G47 | output_qc.py | 0 | PASS |

G40 records WARN because every certification receipt is SELF-ATTESTED (owner equals verifier) and the generator prompts carry no receipt, which is advisory. The checklist adjudication receipt carries CHANGES REQUIRED: observable asks in the unbudgeted Front-end specification and Technical requirements (fit confidence, kit assembly, merchandising schedules, search suggestions, legacy route resolution, page views, request logs, the remaining notification rows) have no grader, and six Constraints and Deployment contract asks cannot be observed by a separate-container grader. See the receipt findings.

## Cell and configuration

| Field | Value |
|---|---|
| cell | solo_founder / ecommerce-retail / commerce-checkout |
| service_profile | P5-db-pay-email |
| providers | backend postgres, email mailpit, payments killbill |
| variant | b, axes critical_depth, spec_sections |
| language | python (drawn: spa-json-api, Litestar, Angular) |
| capability_flags | aesthetic |
| design_direction | companion |
| launch_surface | alt_text, custom_404, no_frontend_secrets, privacy_page, social_preview |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| grader / schema | 0.22.0 / 1.4 |

## Graders

Workflows 15 | browser substeps 30 | pytest substeps 57 | critical substeps 40 | largest workflow 9 substeps, so every workflow is all-or-nothing. One module, `tests/test_output.py`, 57 tests. Rubric 20 criteria, all positive, none grading what pytest or a browser substep settles. Checklist 226 items, 0 not fully graded (`tests/traceability-matrix.md`).

## Slot obligations

| Slot | Provider | Critical substep | Observed by |
|---|---|---|---|
| backend | postgres | test_two_bags_racing_for_the_last_unit_hold_it_once, test_placements_needing_more_than_on_hand_sell_it_once and more | MET |
| email | mailpit | test_a_code_for_a_known_phone_goes_only_to_the_email_on_file, test_cash_on_delivery_order_needs_a_verified_phone | MET |
| payments | killbill | test_cash_on_delivery_invoice_appears_only_at_delivery_and_only_once, test_a_partial_advance_is_invoiced_at_placement_and_the_rest_at_delivery | MET |

## Carriage of the companion PRD (G51)

Colours 24 of 24 described by family and tone with no hex in the brief; topics 164 of 164; enumerated items 458 of 458, of which 449 carried and 9 declared with `--waive` (`sizeprofile`, `fitfeedback`, `bundlerule`, `orderconfidence`, `postalstats`, `paymentmethod`, `placedat`, `orderid, variantid`, `unitpriceminor`: PRD schema rows whose underscores the gate strips from the source side only; each table and field is carried in the Data model with its underscores).

## Grading window

core_features 2423, user_flow 1744, ui_ux_notes 2163, constraints 570, user_roles 1257, overview 805; joined 8962 of 9000.
