# Build report: S_commu_crud_crowdsourced-cartography-platform-vb_20260916_062745

task_id      : deku/crowdsourced-cartography-platform-vb
cell         : solo_founder / community-social / crud-catalog
variant      : b (companion-backed, axes critical_depth and spec_sections)
profile      : P1-db (PostgreSQL)
grader pin   : 0.22.0
kit revision : 806eb0a (madhur-test, pulled 2026-09-16)
exit state   : MECHANICALLY-GREEN, NO-SOLUTION

## Input

Task Order   : openstreetmap_input.amended.yaml
Companion    : openstreetmap_prd.md (1276 lines, carried under G51)
QL           : kaustubh.dalvi@ethara.ai
Contributor  : kunal.singh.int5@ethara.ai

The Task Order as supplied named `pattern: collaborative-workspace`, which is not
in the closed enum, and its nearest neighbour `collaboration-shared` is a D19 dead
cell for solo_founder because no provider serves the `realtime` slot. The tasker
chose `crud-catalog`, which is the live cell nearest the alternative the PRD's own
section 27.1 records having rejected. Recorded, never silently repaired.

## Gate log, rendered from the receipts

This table is a rendering of `S_commu_crud_crowdsourced-cartography-platform-vb_20260916_062745.gates.jsonl`. No verdict here was written by
hand.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G1/G12 | `layout_lint.py` | 0 | PASS |
| G10 | `no_sdk_lint.py` | 0 | PASS |
| G11 | `leak_scan.py` | 0 | PASS |
| G14 | `reward_path_lint.py` | 0 | PASS |
| G17 | `secret_hygiene_lint.py` | 0 | PASS |
| G2/G16 | `validate_task.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G27/G30 | `rubric_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G31 | `determinism_lint.py` | 0 | PASS |
| G33 | `window_lint.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G4/G5 | `contract_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G41 | `flag_lint.py` | 0 | PASS |
| G43 | `prescription_lint.py` | 0 | PASS |
| G44 | `disclosure_lint.py` | 0 | PASS |
| G46 | `structure_lint.py` | 0 | PASS |
| G47 | `output_qc.py` | 0 | PASS |
| G48 | `truth_lint.py` | 0 | PASS |
| G50 | `docker_lint.py` | 0 | PASS |
| G51 | `source_lint.py` | 0 | PASS |
| G52 | `rubric_context_lint.py` | 0 | PASS |
| G54 | `comment_lint.py` | 0 | PASS |
| G55 | `runtime_deps_lint.py` | 0 | PASS |
| G56/G57/G58 | `if_lint.py` | 0 | PASS |
| G59/G60 | `codequality_lint.py` | 2 | ? |
| G6 | `fixture_lint.py` | 0 | PASS |
| G63 | `secret_lint.py` | 0 | PASS |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |

G59/G60 exits 2, NOT-APPLICABLE: the bundle carries no code-quality rubric. The
2026-09-16 pull added `code_quality` to the authored code dimensions, but
`recompute.py` still restricts `judged_criteria` to the seven product dimensions
and `tests/rubric.json` is GENERATED, so a source criterion cannot currently be
emitted from `grounding.yaml` without failing G48. Recorded as a kit-side gap
rather than worked around.

G40 exits 0 with WARN: every certification prompt has a receipt, and each is
recorded SELF-ATTESTED because one agent both authored and reviewed. The four
generator prompts are UNCITED and advisory.

## Rebuilt against the 2026-09-16 pull

Five commits landed after the first green sweep and four of them changed this
bundle:

- the pytest module is `tests/test_output.py`, not `test_pytest.py`; all 51
  workflow substep ids and the tests Dockerfile COPY moved with it
- the compiled rubric layer is `solution/trinity/test_ans.py`, not
  `test_output.py`
- `solution/USER_README.md` is restored as a GENERATED file carrying the seeded
  logins beside the canary; G12 now checks the canary in both generated copies
- the vendored `test.sh` was re-pinned with its whole-line comments stripped, so
  it was re-vendored to match the new MANIFEST hash
- `[verifier].environment_mode` is now `"separate"` by default and `qc_toml`
  VERIF-001 expects it. This bundle was minted after that change, so it was
  switched. The one test that read `/app` from the grader was removed with it: a
  separate verifier runs in its own container and cannot see the agent's app
  root. C-DC-07 is now carried by a browser substep with an earned clause naming
  G13 and G18 as the gates that discharge it.

## What the QC prompts found

Running the certification prompts rather than assuming them produced thirteen
repairs the mechanical battery did not see. `qc_toml.md` found a wrong
`harbor_version`, two retired keys still present, a `language` that disagreed with
the TRD, a missing `difficulty` placeholder, mis-ordered `spec_sections_given`,
two off-tier budgets, a missing `APP_PUBLIC_URL`, and after the pull a stale
`environment_mode`. `qc_docker.md` found a missing long-lived `CMD`, a
`--break-system-packages` pip invocation with a fallback, a missing `EXPOSE` and
a `restart:` on the sidecar. `QC_spec.md` found the seventh spec doc absent. Full
scorecards are in `S_commu_crud_crowdsourced-cartography-platform-vb_20260916_062745.receipts.json`.

## Coverage

130 checklist items, all cited. 51 pytest tests in one module, 16 workflows,
11 judged criteria. Channels are exclusive: no part of any ask is graded twice.
The requirement matrix ships inside the bundle at `tests/traceability-matrix.md`
and `.csv`; it is regenerated by every sweep and is not restated here.

## Known warnings, carried deliberately

- `## Core features` runs past the 2500-char judge slice. G33 fails nothing on
  length and the judged criteria are self-contained, so no rule was cut to fit.
- The brief carries nine launch-surface obligations against a floor of five. The
  extra four were already stated by the PRD, which is an overlap rather than a
  conflict.
- `SCHEMA-013` and `SCHEMA-014` are WARN: section and key order were not diffed
  against the canonical template key-by-key.
