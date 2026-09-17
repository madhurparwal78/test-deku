# Build report: E_itdev_appr_workflow-orchestration-platform-vb_20260916_053324

Rendered from `_handoff/E_itdev_appr_workflow-orchestration-platform-vb_20260916_053324.gates.jsonl`. Every verdict below is the receipt's
own exit code and verdict string. Nothing here is transcribed by hand.

## Identity

| | |
|---|---|
| Task code | `E_itdev_appr_workflow-orchestration-platform-vb_20260916_053324` |
| Task id | `deku/workflow-orchestration-platform-vb` |
| Cell | enterprise / it-devtools / approval-workflow |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Service profile | `P3-db-auth` (`backend = postgres`, `auth = keycloak`) |
| Language | python (Litestar) behind Preact + Vite |
| Design direction | `companion` (the drawn `editorial-serif` does not govern) |
| Launch surface | `favicon`, `form_validation`, `meta_tags`, `single_cta`, `spam_protection` |
| Companion | `n8n_prd.md`, 5,149 lines, 42,130 words |
| Kit | deku-green-field, grader pin 0.22.0, schema 1.4 |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## What the bundle carries

| | |
|---|---|
| Workflows | 23 (enterprise band 13 to 23) |
| Browser substeps | 52 |
| Pytest substeps | 46 |
| Critical substeps | 14 |
| Test functions | 46, all in one `tests/test_output.py` |
| Checklist items | 246 across ten section codes |
| Judged criteria | 15 (13 positive, 2 negative) |
| Literals ledger | 123 pinned values |

## Companion carriage (G51)

35 of 35 source colours described by family and tone, 326 of 326 topics carried,
771 of 771 enumerated items carried. Five waivers, each recorded in
`Output/_spec/E_itdev_appr_workflow-orchestration-platform-vb_20260916_053324/00-decisions.md`.

## Kit gate log

31 PASS, 1 NOT-APPLICABLE, 0 FAIL.

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
| G59/G60 | `codequality_lint.py` | 2 | ? |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 0 | PASS |

## Red gates, with their own findings

None.
## Blocking findings

**G24 is red on seventeen checklist items, all in `## Technical requirements`.**
Each names an obligation the brief states and no channel can observe: structured
logs, metrics, insight accumulation, run-output streaming and retention, binary
offload, the operator-code sandbox, egress control, and expression resolution.
`stage-3-checklist.md` names this class and instructs the author to record and
escalate rather than fabricate a citation or drop the item. Both refusals are
honoured here. The full table is in `Output/_spec/E_itdev_appr_workflow-orchestration-platform-vb_20260916_053324/00-decisions.md` under
"D-H escalation". Closing it needs a decision on OPEN-DECISIONS D-H.

**G40 is red because the adversarial QC prompts have not been run.**
`prompts/QC_instruction.md` (24 checks), `prompts/QC_spec.md` (15),
`prompts/qc_docker.md` (105), `prompts/qc_rubric.md` (16),
`prompts/qc_solution_checklist.md` and `prompts/qc_toml.md` (120) each owe a
receipt carrying a per-check scorecard. `prompts/task_code_verifier.md` (G3) WAS
run and returned VALID on all twelve checks; its receipt is recorded.
Until the rest are run, G34, G35, G36 and G53 are UNCITED, and an uncited PASS
is a FAIL.

**G47 is red in consequence**: an output carrying a red gate is not a finished
output.

## Not proven here

Battery 3 is handoff-owned and needs Docker and the harness: G13, G15, G18, G19,
G20, G21, G25. The answer key's replay half (compiled tests accept the oracle and
reject the known-wrong controls) is DEFERRED by G48 until the app exists.

## Budget

`turns_expected = 210`, `tokens_expected = 7500000`. The reasoning: this task
carries two products behind one brief (a thirteen-route marketing site and a
signed-in console over an execution engine), the brief runs past 45,000
characters, and the seed alone is twenty tables. That is above the corpus median
for an approval-workflow task, which is why both numbers sit above the
`team-expense-approval` baseline of 180 turns and 6.5M tokens.
