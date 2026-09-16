# Build report: S_local_cont_architecture-studio-showcase-vb_20260916_072142

Rendered from `_handoff/S_local_cont_architecture-studio-showcase-vb_20260916_072142.gates.jsonl`. No verdict in this file was typed by hand.

## Identity

| | |
|---|---|
| Task code | `S_local_cont_architecture-studio-showcase-vb_20260916_072142` |
| Task id | `deku/architecture-studio-showcase-vb` |
| Product | Norrgaard Architectural Bureau |
| Cell as ordered | `solo_founder` / `portfolio-agency` / `media-gallery` |
| Cell as minted | `solo_founder` / `local-services` / `content-publishing` |
| Service profile | `P4-db-storage`, two slots: `backend = postgres`, `storage = minio` |
| Variant | `b`, axes `critical_depth`, `spec_sections` (a companion document was supplied) |
| Language | `python` |
| Design direction | `companion` (reference/L L.6.1; the draw does not govern once a companion is supplied) |
| Launch surface | `alt_text, form_validation, meta_tags, spam_protection, terms_page` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field, `Output/` root from `config/kit-config.yaml` |
| Vendored grader | `0.22.0` (INV5) |
| Target schema | `1.4` |
| Harbor version | `0.20.0` |
| Companion | `kononenko_prd.md`, 2,037 lines, 25 sections |

The ordered taxonomy cell `portfolio-agency` / `media-gallery` is not in the kit's registry.
It was substituted to the nearest registered pair, `local-services` / `content-publishing`,
and both spellings are recorded in `_spec/S_local_cont_architecture-studio-showcase-vb_20260916_072142/00-decisions.md`. The archetype, the idea and
the product are the ones ordered; only the registry labels moved.

## Exit state

```
GATES RED (one gate, deliberately), NO-SOLUTION
```

NOT ADMISSIBLE, on two separate counts.

1. **No reference app (D20).** The bundle carries no application. It becomes admissible only
   when the app is built downstream from `solution/checklist.md` and `harbor run -a oracle`
   returns `1.0` twice. `solution/solve.sh` is a stub that exits non-zero for exactly this
   reason.
2. **G40 is red by instruction.** The build was ordered with the adversarial QC pass
   withheld. No QC prompt was run against this bundle, so no `_handoff/S_local_cont_architecture-studio-showcase-vb_20260916_072142.receipts.json`
   exists, so `prompt_receipt_lint.py` reports UNCITED and `output_qc.py` (G47) reports the
   red gate downstream of it. Both reds are the same fact, recorded honestly rather than
   papered over. See **Withheld** below.

Every other gate in the sweep is green: 28 PASS, 2 NOT-APPLICABLE, 2 FAIL.

## Kit gate log

One row per receipt, verbatim from the sweep. The `inputs` hashes in the receipt file bind
each row to the bytes it examined.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 2 | NOT-APPLICABLE |
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
| G40 | `prompt_receipt_lint.py` | 1 | FAIL |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 1 | FAIL |

`G2/G16` is NOT-APPLICABLE: `validate_task.py` needs the harness schema validator, which is
not vendored. `G59/G60` is NOT-APPLICABLE: `tests/rubric.json` carries no
`evaluation_target: "source"` criterion, so there is no source-read criterion to lint.

## Withheld: the QC battery

The order for this bundle was *just create the task, do not qc it*. Accordingly none of the
seven adversarial QC prompts was run, and none of their scorecards was written:

| Prompt | Gate | State |
|---|---|---|
| `QC_instruction.md` | G34 | NOT RUN |
| `QC_spec.md` | G35 | NOT RUN |
| `qc_toml.md` | G36 | NOT RUN |
| `qc_docker.md` | G36 | NOT RUN |
| `qc_rubric.md` | G30b | NOT RUN |
| `qc_solution_checklist.md` | G37b | NOT RUN |
| `task_code_verifier.md` | G23 | NOT RUN |

This is a withheld step, not a passed one. Anyone picking the bundle up should run the
battery before treating the prose as adjudicated. The mechanical gates that overlap those
prompts did run and are green, which is a floor, not a substitute: `source_lint.py` (G51)
proves every claim traces to the companion, `prescription_lint.py` (G43) proves the spec
carries no mechanism, `checklist_qc.py` (G37) proves the checklist's shape, `rubric_lint.py`
and `rubric_context_lint.py` (G27/G30/G52) prove the rubric's shape and its anchoring, and
`truth_lint.py` (G48) proves the answer key agrees with the graders. What no tool can prove
is whether the brief is *right*, and that is what the withheld battery reads for.

## Content ledger

| | |
|---|---|
| `instruction.md` H2 sections | 11 |
| Numbered core-feature rules | 69 |
| `solution/checklist.md` items | 131 |
| Pinned literals in the ledger | 144 |
| `tests/workflows.yaml` workflows | 16 |
| Browser substeps | 34 |
| Pytest substeps | 60 |
| `tests/test_output.py` test functions | 60 |
| Trajectory steps in `grounding.yaml` | 10 |
| Rejected routes, each with a distinct control | 14 |
| Compiled rubric items | 18 |
| Judged criteria in `tests/rubric.json` | 17 |
| Seeded tables | 12 |

## Slots and their observation

| Slot | Provider | Observed by |
|---|---|---|
| `backend` | `postgres` | rows read through `capabilities.make_backend()` in the pytest suite |
| `storage` | `minio` | objects read through `capabilities.make_store()`, plus an anonymous fetch that must be refused |

Both declared slots are observed. There are no unmet slots.

## Reconciliations against the companion

Three places where the companion document and the kit's own rules disagreed. In each the
kit governs the mechanism and the companion governs the product; the divergence is recorded
rather than silently resolved.

1. The companion specifies a client-side router. The kit's pattern default is
   `mpa-progressive`. The brief carries the observable (a route change leaves the scrolled
   surface continuous) and names no router.
2. The companion states the site needs no account. The pattern requires roles. The brief
   keeps the whole public surface anonymous and adds `editor` and `reader` behind a studio
   surface the visitor never has to meet.
3. The companion's default project view is Grid. The kit's table-first default is List. The
   brief pins `List` as the default and carries all three arrangements.

## Route-back table

| Red gate | Route back to |
|---|---|
| G40 | the QC battery, withheld by instruction; running it and writing `receipts.json` clears both G40 and G47 |
| G47 | resolves by itself once G40 is green |
