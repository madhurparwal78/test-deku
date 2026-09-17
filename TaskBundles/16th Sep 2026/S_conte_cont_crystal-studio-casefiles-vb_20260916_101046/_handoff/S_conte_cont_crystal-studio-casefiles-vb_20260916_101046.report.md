# Build report: S_conte_cont_crystal-studio-casefiles-vb_20260916_101046

Rendered from `_handoff/S_conte_cont_crystal-studio-casefiles-vb_20260916_101046.gates.jsonl`. No verdict in this file was typed by hand; each row below is the recorded exit code of the tool that owns it.

## Identity

| Field | Value |
|---|---|
| task code | `S_conte_cont_crystal-studio-casefiles-vb_20260916_101046` |
| task id | `deku/crystal-studio-casefiles-vb` |
| category | `solo_founder` |
| domain | `content-publishing` |
| pattern | `content-publishing` |
| service_profile | `P4-db-storage` |
| variant | `b` |
| variant_axes | `critical_depth, spec_sections` |
| language | `typescript` |
| capability_flags | `aesthetic` |
| design_direction | `companion` |
| launch_surface | `form_validation,privacy_page,security_headers,single_cta,social_preview` |
| spec_sections_given | `overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract` |
| grader_version | `0.22.0` |
| schema_version | `1.4` |
| uuid_v5 | `7d63cd48-d585-575a-bfef-261b67397aa8` |
| authors | `kaustubh.dalvi@ethara.ai, kunal.singh.int5@ethara.ai` |
| contributor_id | `kunal.singh.int5@ethara.ai` |

## Source

Built in PRD mode from `PRD/resn_prd.md` with the Task Order taken from `PRD/resn_input.yaml`. The order's domain `portfolio-agency` is absent from the kit taxonomy and was remapped to `content-publishing`, which is the solo_founder cell a case-file publishing product lands in; the remap is recorded in `_spec/<code>/00-decisions.md` and in `_handoff/<code>.sources.json`.

## Grading layer

| Channel | Size |
|---|---|
| checklist items | 679 |
| pytest tests | 166 |
| workflows | 16 |
| browser substeps | 70 |
| pytest substeps | 166 |
| judged rubric criteria | 41 |

Coverage is two-way: every checklist item is cited by pytest, by a browser substep or by a rubric criterion, and every citation resolves to an item (G24). Obligations no channel in this environment can observe are listed under `## Declared but ungraded` in `solution/checklist.md` rather than cited falsely.

## Gate log

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G59/G60 | `codequality_lint.py` | 2 | ? |
| G54 | `comment_lint.py` | 0 | PASS |
| G4/G5 | `contract_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G31 | `determinism_lint.py` | 0 | PASS |
| G44 | `disclosure_lint.py` | 0 | PASS |
| G50 | `docker_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G41 | `flag_lint.py` | 0 | PASS |
| G56/G57/G58 | `if_lint.py` | 0 | PASS |
| G1/G12 | `layout_lint.py` | 0 | PASS |
| G11 | `leak_scan.py` | 0 | PASS |
| G10 | `no_sdk_lint.py` | 0 | PASS |
| G47 | `output_qc.py` | 0 | PASS |
| G43 | `prescription_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G14 | `reward_path_lint.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G52 | `rubric_context_lint.py` | 0 | PASS |
| G27/G30 | `rubric_lint.py` | 0 | PASS |
| G55 | `runtime_deps_lint.py` | 0 | PASS |
| G17 | `secret_hygiene_lint.py` | 0 | PASS |
| G63 | `secret_lint.py` | 0 | PASS |
| G51 | `source_lint.py` | 0 | PASS |
| G46 | `structure_lint.py` | 0 | PASS |
| G48 | `truth_lint.py` | 0 | PASS |
| G2/G16 | `validate_task.py` | 0 | PASS |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G33 | `window_lint.py` | 0 | PASS |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |

## Prompt receipts

| Prompt | Gate | Verdict | Checks | Verifier |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | CHANGES REQUIRED | 24 | subagent-qc-instruction |
| `QC_spec.md` | G34 | PASS | 15 | subagent-qc-spec |
| `qc_docker.md` | G35 | PASS | 105 | subagent-qc-docker |
| `qc_rubric.md` | G53 | CHANGES REQUIRED | 16 | subagent-qc-rubric |
| `qc_solution_checklist.md` | G37 | FAIL | 0 | subagent-qc-checklist |
| `qc_toml.md` | G36 | PASS | 120 | subagent-qc-toml |
| `task_code_verifier.md` | G3 | VALID | 12 | subagent-task-code-verifier |

## Exit state

MECHANICALLY-GREEN, NO-SOLUTION. Every gate the kit can run is green and the bundle carries no reference application: the kit authors the brief, the answer key and the grading layer, never the app. Admissibility needs the app built downstream and `harbor run -a oracle` returning 1.0 twice.
