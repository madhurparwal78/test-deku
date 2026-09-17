# Build report - deku/encrypted-messenger-platform-vb

- Task code: `S_commu_mess_encrypted-messenger-platform-vb_20260916_111958`
- Cell: solo_founder / community-social / messaging-notifications; service profile P2-db-email (backend postgres, email mailpit)
- Variant b; variant_axes critical_depth; language javascript; spec_sections_given overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract, buildplan
- Kit grader pin 0.22.0; schema 1.4; shard 1 of 1

## Source carry (G51)

- note  signal_prd.md: 19/19 source colour(s) described in the brief by family and tone
- note  signal_prd.md: 82/82 topic(s) carried into the brief
- note  signal_prd.md: 193/193 enumerated item(s) carried into the brief
- VERDICT  PASS   G51: every supplied source document is carried into instruction.md (/Users/apple/Downloads/Greenfield_trajectories/16sept_task_folder/task_07/S_commu_mess_encrypted-messenger-platform-vb_20260916_111958/instruction.md)

## Graders

- Workflows 16; browser substeps 22; pytest substeps 49; critical pytest substeps 18
- One section module `tests/test_output.py` with 49 tests
- Checklist items 590
- Judged rubric criteria 24 (19 positive, 5 negative); positive share by dimension: accessibility 0.02, functionality 0.20, instruction_following 0.29, motion 0.02, responsiveness 0.02, ui_visual 0.22, ux_flow 0.22

## Kit gate log (rendered from the receipts)

| Gate | Tool | Exit | Verdict | Output sha |
|---|---|---|---|---|
| G2/G16 | validate_task.py | 0 | PASS | 50296c00861d9142 |
| G1/G12 | layout_lint.py | 0 | PASS | f70d7d23fa9e0d11 |
| G46 | structure_lint.py | 0 | PASS | c58f6cc61e3bab39 |
| G50 | docker_lint.py | 0 | PASS | 380ed7d1c830de35 |
| G55 | runtime_deps_lint.py | 0 | PASS | a0c21dca8bc5f78a |
| G63 | secret_lint.py | 0 | PASS | 564d9e40eee18156 |
| G48 | truth_lint.py | 0 | PASS | 071f4c57559a94f1 |
| G51 | source_lint.py | 0 | PASS | 04516fb6ceef37ee |
| G52 | rubric_context_lint.py | 0 | PASS | 53f20ccd0059bdd4 |
| G54 | comment_lint.py | 0 | PASS | ec81ec1597e29c40 |
| G17 | secret_hygiene_lint.py | 0 | PASS | 23325b5d105f3617 |
| G11 | leak_scan.py | 0 | PASS | f0ddc3b2639cdc51 |
| G33 | window_lint.py | 0 | PASS | e7a210394e0fac86 |
| G4/G5 | contract_lint.py | 0 | PASS | 215acd991cb42b0a |
| G43 | prescription_lint.py | 0 | PASS | 01a52f84739b2b6d |
| G44 | disclosure_lint.py | 0 | PASS | 1aff876ced2ac478 |
| G10 | no_sdk_lint.py | 0 | PASS | 16b02d728302d018 |
| G31 | determinism_lint.py | 0 | PASS | 7a69183b0f4520a9 |
| G14 | reward_path_lint.py | 0 | PASS | c563207dedc4a6ac |
| G27/G30 | rubric_lint.py | 0 | PASS | 0fadd45712e45d33 |
| G41 | flag_lint.py | 0 | PASS | 5c3def147d9d0df9 |
| G56/G57/G58 | if_lint.py | 0 | PASS | cdf20c83e9056866 |
| G59/G60 | codequality_lint.py | 2 | ? | e23941dd85e0253b |
| G7/G8/G9/G32/G45 | workflow_lint.py | 0 | PASS | fa88f08e5a938c79 |
| G6 | fixture_lint.py | 0 | PASS | 86ac3e487a6a4f74 |
| G24 | coverage_map.py | 0 | PASS | a567916b09764505 |
| G37 | checklist_qc.py | 0 | PASS | ec0940fdd62d4b9f |
| G39 | rubric_align_lint.py | 0 | PASS | 34178819cc35118a |
| G28/G29 | channel_lint.py | 0 | PASS | 8922bfcb1e97c0c4 |
| G40 | prompt_receipt_lint.py | 0 | WARN | 6441ce98ee990bc0 |
| G0/INV5 | vendor_check.py | 0 | PASS | 27d407c2de45b717 |
| G47 | output_qc.py | 0 | PASS | 67c3f2a0886bcbdb |

## Certification prompt receipts (G40)

| Prompt | Gate | Verdict | Verifier | Checks answered | Findings |
|---|---|---|---|---|---|
| QC_instruction.md | G34 | FAIL | subagent:qc-instruction | 24 | 8 |
| QC_spec.md | G34 | FAIL | subagent:qc-spec | 15 | 6 |
| qc_docker.md | G35 | PASS | subagent:qc-docker | 105 | 0 |
| qc_rubric.md | G53 | CHANGES REQUIRED | subagent:qc-rubric | 16 | 12 |
| qc_solution_checklist.md | G37 | FAIL | subagent:qc-solution-checklist | 0 | 55 |
| qc_toml.md | G36 | PASS | subagent:qc-toml | 120 | 2 |
| task_code_verifier.md | G3 | VALID | subagent:task-code-verifier | 12 | 0 |

## Exit state

MECHANICALLY-GREEN, NO-SOLUTION. Not admissible until a reference app is built downstream and `harbor run -a oracle` returns 1.0 twice.
