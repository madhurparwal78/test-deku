# Build report: Personal Telemetry Workbench

Rendered from `_handoff/I_produ_dash_personal-telemetry-workbench-vb_20260916_075139.gates.jsonl`.
No verdict in this file was written by hand.

## Identity

| Field | Value |
|---|---|
| Task code | `I_produ_dash_personal-telemetry-workbench-vb_20260916_075139` |
| Task id | `deku/personal-telemetry-workbench-vb` |
| Cell | `individual` / `productivity-self-management` / `dashboard-analytics` |
| Service profile | `P1-db` |
| Providers per slot | `backend = postgres` (`postgres:16.4-bookworm`) |
| Variant | `b`, axes `critical_depth` + `spec_sections` |
| Language | `typescript` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |

## Derived-design draws

Digest identity is `[metadata].archetype` = `personal-telemetry-workbench`, SHA-256 at the
documented offsets.

| Axis | Value |
|---|---|
| `render_model` | `spa-json-api` |
| `backend` | `NestJS` |
| `frontend` | `Lit + Vite` |
| `design_direction` | `companion` (bank draw `playful-consumer` recorded, does not govern) |
| `nav` | `top-nav` (OVERRIDDEN to the companion's eight-destination rail; recorded in `_spec/00-decisions.md`) |
| `work_surface` | `chart-grid` (honoured by the dashboard grid) |
| `create_flow` | `multi-step-wizard` (honoured: the three-step insight wizard) |
| `feedback` | `inline-banner` |
| `launch_surface` | `colour_contrast,form_validation,meta_tags,no_broken_links,security_headers` |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Event field with five zoom bands | INCLUDED | `## Core features`, `## Front-end specification` | the companion's central interaction |
| Brush to cohort, reconciled against raw rows | INCLUDED | `## Core features` | the pattern's critical focus |
| Insights, execution provenance, three-step wizard | INCLUDED | `## Core features` | companion plus the `create_flow` draw |
| Dashboards with filter override and conflict marker | INCLUDED | `## Core features` | companion |
| Session replay | INCLUDED, RECAST | `## Core features` | frames stored in the declared database; no storage slot is declared |
| Feature flags, blast radius, schedule, kill | INCLUDED | `## Core features` | companion |
| Experiments, deterministic assignment, atomic ship | INCLUDED | `## Core features` | companion |
| Error groups, unresolved frames, regrouping revisions | INCLUDED | `## Core features` | companion |
| Surveys, themes | INCLUDED | `## Core features` | companion |
| Pipeline, breaker, held backlog, replay | INCLUDED, RECAST | `## Core features` | served internally; no external network call at run time |
| Person timeline, access package, erasure certificate | INCLUDED | `## Core features` | companion, first-class subject rights |
| Share links, bounded and revocable | INCLUDED | `## Core features` | the only route to a second human |
| Held mode, pending work, conflicts | INCLUDED | `## Core features` | the observable half of local-first |
| Processing switch | INCLUDED | `## Core features` | the observable half of on-device processing |
| Health and cost | INCLUDED | `## Core features` | companion |
| Columnar store in the browser, WebGL internals, workers | DROPPED | waived | implementation mechanism, barred by INV9/G43 and not observable |
| Backend service map, gRPC, ClickHouse, segments | DROPPED | waived | mechanism; this environment declares one datastore |
| Entitlements, plan tiers, billing | DROPPED | waived | no payments slot |
| Realtime channels, outbound webhooks, external sources | DROPPED | waived | no external network call at run time |
| Performance profiles, SLOs, tracing, instrumentation | DROPPED | waived | not observable through any declared channel |
| Logging one line per request | CUT | removed from the brief | no channel can observe the app's stdout; G24 has no waiver, so the sentence and its checklist item were both removed rather than minting an uncitable obligation |

## Slot obligation

| Slot | Provider | Status | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_seeded_event_rows_are_stored_in_the_database`, `test_an_ingested_event_reaches_the_stored_rows`, `test_an_operation_row_is_never_updated_or_deleted` |

## Grading surface

| Measure | Value |
|---|---|
| Workflows | 11 (`individual` band 6 to 11) |
| Browser substeps | 65 |
| pytest substeps | 122 |
| Browser : pytest substep ratio | 0.53 (G45 band 0.40 to 2.00) |
| `critical` substeps | 18 |
| Non-happy-path workflow ids | `invalid`, `denied`, `duplicate`, `forbidden`, `concurrent` |
| pytest module | one, `tests/test_output.py`, 122 tests |
| Sections covered | core features, data integrity, authorization, edge cases, backend slot |
| Rubric criteria | 26, all positive, 19 `task completion` (73%) |
| Checklist items | 433 |
| Core asks traced | 199, all fully graded |

### Rubric dimension shares

| Dimension | Criteria | Share | Target | Delta |
|---|---|---|---|---|
| `instruction_following` | 5 | 0.288 | 0.30 | 0.012 |
| `functionality` | 5 | 0.288 | 0.25 | 0.038 |
| `ux_flow` | 3 | 0.136 | 0.15 | 0.014 |
| `ui_visual` | 6 | 0.152 | 0.15 | 0.002 |
| `motion` | 3 | 0.045 | 0.05 | 0.005 |
| `accessibility` | 2 | 0.061 | 0.05 | 0.011 |
| `responsiveness` | 2 | 0.030 | 0.05 | 0.020 |

## Grading window

Reported, never failed: the brief has no length limit.

| Section | Chars | Reference | Flag |
|---|---|---|---|
| `## Core features` | 30218 | 2400 | past-slice |
| `## User flow` | 6095 | 1900 | past-slice |
| `## UI/UX notes` | 15443 | 1700 | past-slice |
| `## Constraints` | 1074 | 800 | over-reference |
| `## User roles` | 2506 | 1000 | past-slice |
| `## Overview` | 2489 | 700 | over-reference |
| joined total | 57825 | 8800 | past-slice |

The critical-focus rules are the first subsection of `## Core features`, so they sit inside
the judge's slice.

## Literals ledger

196 entries across the classes `account`, `credential`, `seed`, `enum`, `status`, `hook`,
`route`, `path`, `env` and `count`. Every entry carries at least one of `instruction.md`,
`conftest.py` or `test_output.py` as a carrier, and G6 holds the bijection in both
directions. No entry is `verifier_only`.

## Sources carried

| Source | Colours | Topics | Items |
|---|---|---|---|
| `prd/tessera-prd.md` | 37/37 described by family and tone | 176/176 | 1139/1139 |
| `task-orders/personal-telemetry-workbench.prd.md` | none | 32/32 | 42/42 |

136 waivers were declared, one per deliberately dropped subject, and each is recorded in
`_spec/I_produ_dash_personal-telemetry-workbench-vb_20260916_075139/00-decisions.md`.

## Kit gate log

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS |
| `G1/G12` | `layout_lint.py` | 0 | PASS |
| `G46` | `structure_lint.py` | 0 | PASS |
| `G50` | `docker_lint.py` | 0 | PASS |
| `G55` | `runtime_deps_lint.py` | 0 | PASS |
| `G63` | `secret_lint.py` | 0 | PASS |
| `G48` | `truth_lint.py` | 0 | PASS |
| `G51` | `source_lint.py` | 0 | PASS |
| `G52` | `rubric_context_lint.py` | 0 | PASS |
| `G54` | `comment_lint.py` | 0 | PASS |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS |
| `G11` | `leak_scan.py` | 0 | PASS |
| `G33` | `window_lint.py` | 0 | PASS |
| `G4/G5` | `contract_lint.py` | 0 | PASS |
| `G43` | `prescription_lint.py` | 0 | PASS |
| `G44` | `disclosure_lint.py` | 0 | PASS |
| `G10` | `no_sdk_lint.py` | 0 | PASS |
| `G31` | `determinism_lint.py` | 0 | PASS |
| `G14` | `reward_path_lint.py` | 0 | PASS |
| `G27/G30` | `rubric_lint.py` | 0 | PASS |
| `G41` | `flag_lint.py` | 0 | PASS |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS |
| `G59/G60` | `codequality_lint.py` | 2 | NOT-APPLICABLE |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS |
| `G6` | `fixture_lint.py` | 0 | PASS |
| `G24` | `coverage_map.py` | 0 | PASS |
| `G37` | `checklist_qc.py` | 0 | PASS |
| `G39` | `rubric_align_lint.py` | 0 | PASS |
| `G28/G29` | `channel_lint.py` | 0 | PASS |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN |
| `G0/INV5` | `vendor_check.py` | 0 | PASS |
| `G47` | `output_qc.py` | 0 | PASS |

`G48` reports its replay/liveness half DEFERRED: the bundle carries no reference app and no
known-wrong controls exist yet, so that half runs downstream. `G59/G60` is NOT-APPLICABLE
because the bundle ships no `evaluation_target: "source"` criteria. `G40` is WARN on the
self-attestation notes: owner and verifier are one agent in this run, which is recorded
rather than hidden.

## Prompt receipts

292 declared checks answered across the seven certification prompts.

| Prompt | Gate | Verdict | Checks | WARN | NOT-APPLICABLE |
|---|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | 3 | 0 |
| `QC_spec.md` | G34 | PASS | 15 | 0 | 8 |
| `qc_docker.md` | G35 | PASS | 105 | 1 | 38 |
| `qc_rubric.md` | G53 | PASS | 16 | 0 | 0 |
| `qc_solution_checklist.md` | G37 | PASS | 0 | 0 | 0 |
| `qc_toml.md` | G36 | PASS | 120 | 4 | 12 |
| `task_code_verifier.md` | G3 | VALID | 12 | 0 | 0 |

Every WARN carries a matching finding in the receipt. The four `qc_toml` WARNs are
`SCHEMA-011`, `SCHEMA-013`, `SCHEMA-014` (the prompt's canonical template predates the
keys `META-011`, `META-013` and G41 require) and `VERIF-001` (`environment_mode` is
deliberately `shared`). The three `QC_instruction` WARNs are `B3` (Build plan is not
baseline), `C4` (no font family or size, per the tasker's authoring guideline) and `C7`
(sections past the judge's slice, which G33 reports and never fails). The one `qc_docker`
WARN is `BP-004` (no checksum is published for the Node setup script).

## Blocking findings

None.

## Budget

| Field | Value |
|---|---|
| `turns_expected` | 195 |
| `tokens_expected` | 6800000 |

Reasoning: eleven workflows, 122 pytest assertions and 26 judged criteria over a product
with a rendering surface, an ingest path, a flag and experiment engine, a replay pipeline
and an append-only log with a digest chain. The reconciliation property alone forces one
query compiler rather than two, and the brief is carried from a 3613-line companion.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the app lands downstream and
`harbor run -a oracle` returns `1.0` twice.
