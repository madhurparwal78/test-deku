# Build report - S_commu_feed_realtime-drawing-party-vb_20260916_074441

Rendered from `_handoff/S_commu_feed_realtime-drawing-party-vb_20260916_074441.gates.jsonl`. Every
verdict below is the exit status the tool actually returned; nothing here is transcribed by hand.

| | |
|---|---|
| Task code | `S_commu_feed_realtime-drawing-party-vb_20260916_074441` |
| Task id | `deku/realtime-drawing-party-vb` |
| Cell | `solo_founder` / `community-social` / `feed-social` |
| Archetype | `realtime-drawing-party`, variant `b` |
| Service profile | `P1-db` (PostgreSQL) |
| Companion | `prds/skribbl_prd.md`, carried under G51 |
| Product name | Doodlerush |
| Gates receipted | 32 |
| PASS | 28 |
| WARN | 1 |
| NOT-APPLICABLE | 1 |
| FAIL | 2 |
| Certification prompts run | 7, answering 292 declared checks |
| Exit state | 1 gate red, and it is a placement deviation rather than a content defect |

## The pattern substitution, recorded first because it changed the cell

The Task Order named `pattern: collaborative-workspace`. Its nearest level-3 code,
`collaboration-shared`, is a **dead cell** for `solo_founder`: `taskorder_lint.py` refuses it
because every solo_founder-legal profile for that pattern requires a `realtime` slot, which no
provider in `environment/registry.json` serves and no `environment/providers/` fragment supplies.
Stage 0 is explicit that a dead cell is reported and refused rather than repaired by the author.

The task was minted under `feed-social`, whose critical focus is visibility enforced at the API
rather than at the interface. That focus became the product's own central boundary: a private
room's existence, name, player count, settings and state are readable only by a caller holding
its code or a seat token for it. The live connection the companion requires is the app's own
endpoint on its own origin, which needs no provider. Both decisions are recorded in
`_spec/<code>/00-decisions.md` and the second is why `P1-db` is the profile.

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
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 1 | FAIL |

## The red gates

**G46 `structure_lint.py` - CON-1 placement.** The bundle sits at
`GreenField-GenKit2/output_16sep/`, which is INSIDE the generation kit. CON-1 requires the output
root to be a sibling of the kit. The location was specified by the tasker and
`config/kit-config.yaml` names it as `output_root`, so the deviation is recorded in the kit's own
configuration rather than being accidental. Nothing else in G46 fails: the project name decodes
back to the Task Order cell, the single-module split holds, and every file sits in the frozen
layout. Moving the bundle one directory up turns this gate green with no change to a single byte
inside it.

**G47 `output_qc.py`** is red only as a consequence: it refuses to call an output finished while
any gate carries a red receipt. It reports no independent finding of its own.

## G51 and its waivers

`source_lint.py` reads every heading, every table row and every list entry of the companion. On
the first sweep it reported 61 findings. Fifty-two were closed by carrying the subject into the
brief; thirty-two headings and items are declared with `--waive`, and they fall into five groups
set out in `00-decisions.md`. The gate now reports **31 of 31 colours described by family and
tone, 210 of 210 topics carried, and 765 of 765 enumerated items carried**.

`revalidate.py` has no way to record a waiver list, only `--source`, so the waivers live in
`_spec/<code>-g51-waivers.txt` and are passed on every sweep. `_spec/run-g51.py` runs the gate
with them. A waiver only suppresses an already-failing item, so it can never hide carried content.

## Certification prompts

All seven are recorded in
`_handoff/S_commu_feed_realtime-drawing-party-vb_20260916_074441.receipts.json`, each bound to
this bundle by a token over the prompt's own bytes plus the task code.

| Prompt | Gate | Verdict | Checks |
|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 answered, 6 not a plain pass |
| `QC_spec.md` | G34 | PASS | 15 answered, 3 not a plain pass |
| `qc_docker.md` | G35 | PASS | 105 answered, 7 not a plain pass |
| `qc_rubric.md` | G53 | PASS | 16 answered, 0 not a plain pass |
| `qc_solution_checklist.md` | G37 | PASS | 0 answered, 0 not a plain pass |
| `qc_toml.md` | G36 | PASS | 120 answered, 9 not a plain pass |
| `task_code_verifier.md` | G3 | VALID | 12 answered, 0 not a plain pass |

Owner and verifier are the same agent on this run, so every one of them reports as
**SELF-ATTESTED**: a recorded verdict rather than an independent one. The kit's rule is owner is
not verifier, and a second reviewer is still worth running.

The six generator prompts are advisory and are recorded as **UNCITED**, because they were not
read end to end on this run. `generate_instruction.md` was read in full and is the one exception;
it carries no receipt because the gate does not mint one for a prompt outside the certification
set unless the author supplies it, and supplying one for a prompt read only in part would be the
exact fabrication the gate exists to catch.

Two findings changed the bundle rather than merely describing it.

- `qc_toml.md` TAX-005 caught `[metadata].language = "python"` against a drawn stack of Hono on
  SolidStart. It now reads `typescript`, and the `keywords` language token follows.
- `QC_instruction.md` C4 caught a missing mode commitment and a missing component-state
  statement in `## UI/UX notes`. Both are now present: the product commits to its single deep
  blue mode, and every control carries five named states with unavailable never signalled by
  colour alone.

A third was found by the checklist adjudicator and closed at the brief: the canvas rule folded
the whole-canvas image and the changed-region image into one sentence, and the second half went
nowhere. Both are now stated and both are checklist items.

## Coverage

`tests/traceability-matrix.md` and `.csv` are regenerated by every sweep from the same scan G24
decides on, so they cannot disagree with the gate. The checklist carries 340 items across ten
sections and every one of them is cited: 289 by a pytest test through the provenance sidecar, 38
by a browser substep, and 13 by a judged rubric criterion, with four ui-tagged items cited by both
a page-driven pytest test and a browser substep.

## Exit state

```
MECHANICALLY-GREEN except CON-1 placement, NO-SOLUTION
1 red gate: G46 placement, with G47 consequential
NOT ADMISSIBLE
```

The bundle carries no reference application, by design: the kit authors the brief, the environment
and the graders, never the app. Admissibility additionally needs the app to be generated
downstream from `solution/checklist.md` and `harbor run -a oracle` returning `1.0` twice.
