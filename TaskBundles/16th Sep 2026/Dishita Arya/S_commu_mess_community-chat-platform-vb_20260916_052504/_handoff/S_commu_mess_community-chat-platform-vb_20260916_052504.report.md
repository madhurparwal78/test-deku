# Build report - S_commu_mess_community-chat-platform-vb_20260916_052504

Rendered from `_handoff/S_commu_mess_community-chat-platform-vb_20260916_052504.gates.jsonl`. Every verdict below is the exit status the
tool actually returned; nothing here is transcribed by hand.

| | |
|---|---|
| Task code | `S_commu_mess_community-chat-platform-vb_20260916_052504` |
| Task id | `deku/community-chat-platform-vb` |
| Cell | `solo_founder` / `community-social` / `messaging-notifications` |
| Archetype | `community-chat-platform`, variant `b` |
| Service profile | `P2-db-email` (PostgreSQL, Mailpit) |
| Companion | `prds/discord_prd.md`, carried under G51 |
| Kit revision | rebuilt against `806eb0a`, five commits after the first build |
| Gates receipted | 32 |
| PASS | 29 |
| NOT-APPLICABLE | 1 |
| FAIL | 2 |
| Certification prompts run | 7, answering 292 declared checks |
| Exit state | 1 gate red, and it is a placement deviation rather than a content defect |

## What the kit revision changed in this bundle

Five kit commits landed after the first build. Each is folded in here; nothing was rebuilt.

| Kit commit | What moved in this bundle |
|---|---|
| `1b99060` code_quality dimension | Nothing. The dimension is authorable in `_vocab`, but the vendored `recompute.py` renders `judged_criteria` only and its `JUDGED_DIMENSIONS` excludes `code_quality`, so no criterion can reach `tests/rubric.json` through the generator. `tests/rubric.json` is GENERATED, so hand-writing one would be a G48 failure by construction. G59/G60 stays NOT-APPLICABLE. |
| `da24d3b` module rename | `tests/test_pytest.py` is now `tests/test_output.py`, and the generated compiled-rubric module is `solution/trinity/test_ans.py`. Every `test:` id in `workflows.yaml` and the `COPY` line in `tests/Dockerfile` follow. |
| `11eaf7b` verifier mode | `[verifier].environment_mode` is now `separate`. The grader ships its own image from `tests/Dockerfile`. `qc_docker.md` DEP-011 moves to NOT-APPLICABLE with it, because that check is conditioned on shared mode. |
| `78e5ba6` test.sh re-pin | `tests/test.sh` re-copied from the re-pinned vendor tree; `vendor_check` is byte-identical to the new MANIFEST. |
| `806eb0a` USER_README restored | `solution/USER_README.md` is back as a GENERATED file and now carries the corpus canary alongside `solution/TRUTH.md`. G12 checks both copies and both hold. |

## Gate log

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
| G59/G60 | `codequality_lint.py` | 2 | NOT-APPLICABLE |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | PASS |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 1 | FAIL |

## The red gates

**G46 `structure_lint.py` - CON-1 placement.** The bundle sits at
`GreenField-GenKit2/output_16sep/`, which is INSIDE the generation kit. CON-1 requires the
output root to be a sibling of the kit. The location was specified by the tasker, and
`config/kit-config.yaml` now names it as `output_root`, so the deviation is recorded in the
kit's own configuration rather than being accidental. Nothing else in G46 fails: the project
name decodes back to the Task Order cell, the single-module split holds, and every file is in
the frozen layout. Moving the bundle one directory up turns this gate green with no change to
a single byte inside it.

**G47 `output_qc.py`** is red only as a consequence: it refuses to call an output finished
while any gate carries a red receipt. It reports no independent finding.

## Certification prompts

All seven are recorded in `_handoff/S_commu_mess_community-chat-platform-vb_20260916_052504.receipts.json`, each
bound to this bundle by a token over the prompt's own bytes plus the task code. `qc_toml.md`
changed in `11eaf7b`, so its receipt was re-minted against the new bytes; its registry is
unchanged at 120 checks and VERIF-001 now expects the `separate` mode the bundle declares.

| Prompt | Gate | Verdict | Checks |
|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 answered, 3 not a plain pass |
| `QC_spec.md` | G34 | PASS | 15 answered, 2 not a plain pass |
| `qc_docker.md` | G35 | PASS | 105 answered, 4 not a plain pass |
| `qc_rubric.md` | G53 | PASS | 16 answered, 0 not a plain pass |
| `qc_solution_checklist.md` | G37 | PASS | 0 answered, 0 not a plain pass |
| `qc_toml.md` | G36 | PASS | 120 answered, 8 not a plain pass |
| `task_code_verifier.md` | G3 | VALID | 12 answered, 0 not a plain pass |

Owner and verifier are the same agent on this run, so every one of them reports as
**SELF-ATTESTED**: a recorded verdict rather than an independent one. The kit's rule is
owner is not verifier, and a second reviewer would still be worth running.

One finding changed the bundle rather than merely describing it. `QC_instruction.md` D2 found
that the mention rule said a notice is sent when the mentioned member has no live session,
which could be read as covering any account holding an issued token. The brief now defines a
live session as an open connection to that account's event stream.

## Coverage

`tests/traceability-matrix.md` and `.csv` are regenerated by every sweep from the same scan
G24 decides on, so they cannot disagree with the gate. Read them there rather than here.

## Exit state

```
MECHANICALLY-GREEN except CON-1 placement, NO-SOLUTION
NOT ADMISSIBLE
```

The bundle carries no reference application, by design: the kit authors the brief, the
environment and the graders, never the app. Admissibility additionally needs the app to be
generated downstream from `solution/checklist.md` and `harbor run -a oracle` returning `1.0`
twice.
