# Build report - deku/yard-operating-system-vb

Task code: `E_suppl_inve_yard-operating-system-vb_20260916_101547`

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

G59/G60 is the advisory code-quality channel and returns NOT-APPLICABLE because the bundle carries no source criteria. G40 records WARN because every certification receipt is SELF-ATTESTED (owner equals verifier). Prose verdicts recorded in the receipts: G34 CHANGES REQUIRED (QC_instruction.md), G34 PASS (QC_spec.md), G35 PASS (qc_docker.md), G53 PASS (qc_rubric.md), G37 CHANGES REQUIRED (qc_solution_checklist.md), G36 PASS (qc_toml.md), G3 VALID (task_code_verifier.md). See the receipt findings for each non-PASS verdict.

## Cell and configuration

| Field | Value |
|---|---|
| cell | enterprise / supply-chain-inventory / inventory-allocation |
| service_profile | P6-db-auth-email |
| providers | backend postgres, auth keycloak, email mailpit |
| variant | b, axes critical_depth, spec_sections |
| language | python (drawn: spa-json-api, Litestar, Vue 3 + Vite) |
| capability_flags | aesthetic |
| design_direction | companion |
| launch_surface | custom_404, page_view_log, security_headers, spam_protection, terms_page |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| grader / schema | 0.22.0 / 1.4 |
| turns / tokens | 200 / 8000000, the expert band: three services, ten roles, a companion carried in full |

## Graders

Workflows 19 | browser substeps 31 | pytest substeps 75 | critical substeps 19 | largest workflow 9 substeps, so one failed substep fails any workflow. One module, `tests/test_output.py`, 75 tests. Rubric 37 criteria, all positive, advisory and off the reward path. Checklist 177 items; every item is cited by pytest, a browser substep or a rubric criterion (G24, G28, G39).

## Rubric point shares

| Dimension | Points | Share | Target |
|---|---|---|---|
| instruction_following | 21 | 0.313 | 0.30 |
| functionality | 13 | 0.194 | 0.25 |
| ux_flow | 12 | 0.179 | 0.15 |
| ui_visual | 11 | 0.164 | 0.15 |
| motion | 4 | 0.060 | 0.05 |
| accessibility | 4 | 0.060 | 0.05 |
| responsiveness | 2 | 0.030 | 0.05 |

## Slot obligations

| Slot | Provider | Critical substep | Status |
|---|---|---|---|
| backend | postgres | test_concurrent_portal_bookings_confirm_only_free_doors, test_concurrent_moves_same_asset_single_open_move, test_app_credential_cannot_rewrite_custody_event_row and more | MET |
| auth | keycloak | test_requester_self_approval_denied_visit_stays_held, test_revoked_grant_denied_same_token_next_request and more | MET |
| email | mailpit | test_booking_confirmation_email_once_on_idempotent_replay, test_approval_request_email_skips_requester_ineligible_member | MET |

## Carriage of the companion PRD (G51)

- note  terminal_prd.md: 25/25 source colour(s) described in the brief by family and tone
- note  terminal_prd.md: 502/502 topic(s) carried into the brief
- note  terminal_prd.md: 2300/2300 enumerated item(s) carried into the brief
- VERDICT  PASS   G51: every supplied source document is carried into instruction.md (instruction.md)

No `--waive` was used.

## Grading window (G33)

core_features 2220, user_flow 1802, ui_ux_notes 1952, constraints 805, user_roles 1433, overview 741; joined 8953 of 9000.

## Runtime smoke check performed during authoring

The three sidecars were booted from a scratch copy of `environment/docker-compose.yaml` with ports published, and all three reached healthy. Seeded members orgadmin, spotter2, publisher and security obtained tokens by password grant against realm `junction` with client `junction-app`, and a wrong password answered 401. The `deku_app` role created a table in `deku`; an append-only trigger refused its UPDATE, and the grader's `DO $tamper$` probe rewrote the row as `deku_admin`. Through the vendored `capabilities` adapters, the Mailpit inbox returned a sent message whose body opens with the booking reference, and `PostgresBackend` counted and read the row. No test ran against a built Junction, because none exists.

## Traps proven both ways

A scratch reference of the pinned HTTP contract, kept outside the bundle, ran the real `tests/test_output.py` against real PostgreSQL 16.4 and Mailpit v1.30.6 booted from `environment/docker-compose.yaml`. Correct mode: 75 of 75 pass, and the four race tests pass 5 of 5 runs. Each switch below turns on one naive default; its target fails on the intended assertion.

| Naive default | Target test | Result |
|---|---|---|
| portal booking check-then-insert | test_concurrent_portal_bookings_confirm_only_free_doors | 5 confirmed, expected 4; failed 5 of 5 runs |
| move creation check-then-insert | test_concurrent_moves_same_asset_single_open_move | 2 open moves created; failed 5 of 5 runs |
| closed interval overlap | test_adjacent_half_open_windows_both_confirmed | adjacent window refused door_unavailable |
| no version check on PATCH | test_stale_version_appointment_update_version_conflict | stale update answered 200 |
| staleness ignored | test_stale_position_move_refused_position_confirmation_task | stale move answered 201 |
| verified reachable by transition | test_move_transition_to_verified_illegal_transition | transition answered 200 |
| no self-approval rule | test_requester_self_approval_denied_visit_stays_held | requester's own decision answered 200 |
| roles unioned across sites | test_dual_role_gate_operator_scope_approval_forbidden | Reno manager decided a Dallas request |
| grants copied into the session | test_revoked_grant_denied_same_token_next_request, test_approver_eligibility_read_at_decision_time | revoked grants still worked |
| 403 for another company's booking | test_other_company_booking_not_found_same_as_nonexistent | answered 403, expected 404 |
| door in availability | test_availability_windows_expose_only_start_end | windows carried a door |
| no small-aggregate suppression | test_customer_fewer_than_five_loads_report_suppressed | three loads reported |
| append-only in application code only | test_app_credential_cannot_rewrite_custody_event_row | application credential UPDATE did not raise |
| Idempotency-Key ignored | test_booking_confirmation_email_once_on_idempotent_replay, test_idempotency_key_reused_different_body_conflict | replay created a second booking |
| approval mail to every site manager | test_approval_request_email_skips_requester_ineligible_member | ineligible Reno manager mailed |
| watchlist expiry ignored | test_expired_watchlist_plate_visit_not_refused | expired plate refused |
| wall clock shift duration | test_shift_duration_across_fall_back_daylight_saving, test_shift_duration_across_spring_forward_daylight_saving | 28800 seconds |
| single page application fallback | test_unknown_path_answers_404_not_found_document | unknown address answered 200 |
| replayed submission inserted | test_contact_replayed_submission_id_stored_once_single_row | replay answered a new id |
| page views logged by the browser | test_page_view_recorded_for_public_route_read_by_publisher | no page view recorded |
| weakest layer at full marks | test_grader_full_marks_fix_route_yard_security | fix route pointed at a module |

The run found one grader defect before it shipped: the page view test parsed the HTML page as JSON, which would have failed every correct build. It is fixed. The browser substeps and the rubric were not exercised, because the reference has no interface.

## Handoff gates

G13, G15, G18, G19, G20, G21 and G25 are undecided; commands and expected verdicts are in the handoff file.

Rendered from the receipts. No verdict here is hand-written.
