# Build report - deku/multiplayer-room-infrastructure-vb

Task code: `E_itdev_appr_multiplayer-room-infrastructure-vb_20260916_073437`

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

G40 records WARN because every certification receipt is SELF-ATTESTED (owner equals verifier), and those receipts predate the difficulty revision. The checklist adjudication receipt carries CHANGES REQUIRED: five App Contract and Constraints asks cannot be observed by a separate-container grader, and the unbudgeted carriage sections were not decomposed item by item. See the receipt findings.

## Cell and configuration

| Field | Value |
|---|---|
| cell | enterprise / it-devtools / approval-workflow |
| service_profile | P6-db-auth-email |
| providers | backend postgres, auth keycloak, email mailpit |
| variant | b, axes critical_depth, spec_sections, data_shape |
| language | typescript (drawn: ssr-islands, Fastify, Astro + islands) |
| capability_flags | aesthetic, concurrency_hardening, observability, data_scale |
| design_direction | companion |
| launch_surface | alt_text, custom_404, favicon, page_view_log, spam_protection |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| grader / schema | 0.22.0 / 1.4 |

## Graders

Workflows 20 | browser substeps 34 | pytest substeps 81 | critical substeps 35 | largest workflow 9 substeps, so every workflow is all-or-nothing. One module, `tests/test_output.py`, 81 tests. Rubric 23 criteria, all positive. Checklist 173 items, 0 not fully graded (`tests/traceability-matrix.md`). Difficulty revision of 2026-09-16: see the handoff.

## Slot obligations

| Slot | Provider | Critical substep | Observed by |
|---|---|---|---|
| backend | postgres | test_connection_past_ceiling_refused_others_undisturbed_count and nine more | MET |
| auth | keycloak | test_revocation_revokes_member_sessions_token_denied, test_analyst_role_denied_approval_row_untouched | MET |
| email | mailpit | test_break_glass_second_factor_code_arrives_by_email_and_executes | MET |

## Carriage of the companion PRD (G51)

Colours 20 of 20 described by family and tone with no hex in the brief; topics 391 of 391; enumerated items 1702 of 1702, of which 1700 carried and 2 declared with `--waive` (`inboxentry(` and `apikey(`: PRD index definitions whose underscores the gate strips from the source side only, substance carried in the Data model index paragraph).

## Grading window

core_features 2288, user_flow 2013, ui_ux_notes 1836, constraints 469, user_roles 963, overview 651; joined 8220 of 9000.

## Runtime smoke check performed during authoring

The three sidecars were booted from `environment/docker-compose.yaml` with ports published on a scratch copy: all eight seeded accounts obtain tokens by password grant against realm `roomstack` with `accessTokenLifespan` 3600, a wrong password answers 401, `deku_app` can create tables in `deku`, a Mailpit snippet begins with the first line of the body, and the grader's audit tamper probe rewrites and restores a row through an append-only trigger that refuses the application credential.

Rendered from the receipts. No verdict here is hand-written.
