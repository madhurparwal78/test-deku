# Build report

| | |
|---|---|
| Task code | `S_creato_crud_animation-studio-catalogue-vb_20260916_112758` |
| Task id | `deku/animation-studio-catalogue-vb` |
| Cell | solo_founder / creator-monetization / crud-catalog |
| Service profile | `P1-db`, one slot: `backend = postgres` |
| Variant | `b`, axes `critical_depth` + `spec_sections` (companion supplied) |
| Language | typescript |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field, GreenField-GenKit2 |
| Vendored grader | 0.22.0 |
| Target schema | 1.4 |
| Companion | PRD/thelinestudio_prd.md, 6508 lines, 44 sections |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Feature resolution

Every companion section, and where it landed. The full table is `_spec/<code>/00-decisions.md`, the companion carry table; this is its summary.

| Verdict | Count | Companion sections |
|---|---|---|
| INCLUDED | 41 | 1 to 39 and 41 to 43, carried into the H2 the carry table names |
| DROPPED | 3 | 0 (a reading guide for the companion), 40 (a work order rather than a property of the product), 44 (an acceptance checklist, which a brief may not carry per the disclosure ban) |

Twenty-one brief obligations no grading channel can observe were removed from the coverage target rather than given a fabricated citation. They are recorded with their reasons in `_handoff/S_creato_crud_animation-studio-catalogue-vb_20260916_112758.declared-but-ungraded.md`.

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| backend | postgres | **MET** | `test_seeded_rows_are_not_duplicated`, `test_published_film_survives_a_reread`, `test_editorial_log_row_accompanies_a_mutation`, `test_last_item_sells_exactly_once_under_concurrency`, `test_repeated_order_key_creates_one_order` |

## Grading channels

- Workflows: **16**, inside the solo_founder band of 10 to 16.
- Browser substeps: **47**.
- Pytest substeps: **41**, one per test function.
- Critical substeps: **11**.
- Non-happy-path workflow ids: **9** -- `"unknown_facet_is_invalid_and_falls_back"`, `"editor_cannot_publish_a_record"`, `"publisher_cannot_lift_an_embargo_early"`, `"unauthenticated_write_is_denied"`, `"customer_cannot_reach_another_customers_download"`, `"expired_rights_window_removes_the_film"`, `"invalid_writes_are_refused_with_reasons"`, `"duplicate_order_key_creates_one_order"`, `"concurrent_purchase_of_the_last_item"`.
- Category mix: .

One pytest module, `tests/test_output.py`, carrying **41** test functions across core features, data integrity, authorization and edge cases. The section banners the pytest contract describes are omitted because a shipped bundle carries no comments (G54); the assertion, not a banner, places each test.

## Rubric

23 judged criteria: **21 positive**, **2 negative**. Every criterion is GENERATED from `solution/trinity/grounding.yaml` through the vendored `recompute.py`; `recompute.py --check` is byte-clean.

| Dimension | Points | Share | Target | Within 0.10 |
|---|---|---|---|---|
| `instruction_following` | 16 | 0.246 | 0.30 | yes |
| `functionality` | 11 | 0.169 | 0.25 | yes |
| `ux_flow` | 9 | 0.138 | 0.15 | yes |
| `ui_visual` | 14 | 0.215 | 0.15 | yes |
| `motion` | 6 | 0.092 | 0.05 | yes |
| `accessibility` | 6 | 0.092 | 0.05 | yes |
| `responsiveness` | 3 | 0.046 | 0.05 | yes |

## Literals ledger

66 entries, at `_handoff/S_creato_crud_animation-studio-catalogue-vb_20260916_112758.literals-ledger.json`. One is `verifier_only` (`DB_ADMIN_URL`, carried by `task.toml` alone, per INV4).

| Class | Count |
|---|---|
| `account` | 7 |
| `credential` | 1 |
| `endpoint` | 1 |
| `env_var` | 4 |
| `number` | 9 |
| `route` | 15 |
| `scheme` | 8 |
| `seed_record` | 14 |
| `status` | 7 |

## Coverage target

`solution/checklist.md` carries **181** items across ten sections. G24 joins them to the graders in both directions and G37's first layer confirms the structure, the ids, the citations and the ledger arithmetic.

| Section | Items |
|---|---|
| Overview | 8 |
| User roles | 14 |
| Core features | 61 |
| User flow | 16 |
| UI and UX notes | 13 |
| Front-end specification | 24 |
| Technical requirements | 10 |
| Data model | 14 |
| Constraints | 8 |
| Deployment contract | 13 |

The requirement traceability table and its matrix are regenerated on every sweep into `tests/traceability-matrix.md` and `tests/traceability-matrix.csv`. Read them there rather than here: a second copy of a generated table is a second thing to drift.

## Spec folder

| Document | Fed |
|---|---|
| `00-decisions.md` | the draws, the overrides, the identity re-cast, the G51 waivers, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing: `## Build plan` is not emitted at this variant, so the document stays author-side |

## Grading window

Measured by `window_lint.py`, which reports length and fails nothing on it.

| Section | Chars | Reference | |
|---|---|---|---|
| Core features | 42127 | 2400 | past-slice |
| User flow | 7483 | 1900 | past-slice |
| UI/UX notes | 11293 | 1700 | past-slice |
| Constraints | 1457 | 800 | over-reference |
| User roles | 3958 | 1000 | past-slice |
| Overview | 2289 | 700 | over-reference |
| **joined six** | **68607** | 8800 | past-slice |

The six judged sections run well past the judge's slice. That is the measured cost of carrying a 6508-line companion in full, which G51 requires and which the generator explicitly permits: the brief has no length limit and a real rule is never cut to fit. The graded rules are front-loaded inside each section, content past the slice still reaches the agent in full, and `judge_score` never touches reward. Recorded rather than hidden: it is the one QC check this bundle answers WARN.

## Kit gate log

Rendered from `_handoff/S_creato_crud_animation-studio-catalogue-vb_20260916_112758.gates.jsonl`. 32 receipts, each carrying the SHA-256 of every input it read. Never transcribed.

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

`G59/G60` exits 2: NOT-APPLICABLE, because the bundle carries no code-quality rubric. `G7/G8/G9/G32/G45` and `G40` exit 0 carrying warnings, both recorded below.

## Certification prompts

Receipts at `_handoff/S_creato_crud_animation-studio-catalogue-vb_20260916_112758.receipts.json`, each token bound to this bundle.

| Prompt | Gate | Checks answered | Verdict |
|---|---|---|---|
| `QC_instruction.md` | G34 | 24 | PASS |
| `QC_spec.md` | G34 | 15 | PASS |
| `generate_instruction.md` | S2 | 0 | PASS |
| `qc_docker.md` | G35 | 105 | PASS |
| `qc_rubric.md` | G53 | 16 | PASS |
| `qc_solution_checklist.md` | G37 | 0 | PASS |
| `qc_toml.md` | G36 | 120 | PASS |
| `task_code_verifier.md` | G3 | 12 | VALID |

**Every one is SELF-ATTESTED.** One agent authored and reviewed this bundle, so the kit's owner-is-not-verifier rule is unmet. The verdicts are recorded, never independent, and an independent pass over the seven prompts is the remaining QC step.

## Blocking findings

None outstanding. Three were found and repaired during the run, each recorded in its prompt receipt:

1. `task.toml` shipped without `harbor_version`, with `build_timeout_sec` at 1800.0 rather than the Standard tier's 900.0, and with no `APP_PUBLIC_URL` in the agent env table. All three are corrected.
2. The postgres sidecar carried `restart: unless-stopped`, copied from the provider fragment. Removed.
3. The routed contact addresses used the reserved `.example` TLD, which the mail validator rejects outright. Moved to `example.com`.

Two standing caveats, neither blocking:

- Fifty G51 waivers are recorded in `_handoff/<code>.sources.json`, each a companion subject that is informational in the companion's own register (observed library versions, icon path coordinates, declaration counts, the reference asset manifest) or that names infrastructure absent from this environment (webhooks, backups, release pipelines). The reasons are in `_spec/<code>/00-decisions.md`.
- Twenty-one checklist obligations were removed as unobservable, listed with reasons in `_handoff/S_creato_crud_animation-studio-catalogue-vb_20260916_112758.declared-but-ungraded.md`.
- The corpus-level gates report NOT-APPLICABLE or ADVISORY against this output root, which holds one bundle: G42 and G49 need a second bundle to compare against, and G26's payments-or-email share floor of 28 percent is a property of a whole corpus rather than of one db-only task. Re-run both once this bundle is merged into the corpus root.

## Budget

`turns_expected = 120`, `tokens_expected = 4000000`. The reasoning: the product is a twelve-route public site plus a back office over a thirty-eight table schema, with three hidden-record conditions, an editorial state machine and a small commerce surface. That is above the easy band on every axis and below the largest enterprise tasks, so the estimate sits at the top of the medium band. `difficulty` stays the empty string: calibration writes it, never the author.

## Exit

```
MECHANICALLY-GREEN, NO-SOLUTION
```

Not admissible. Nothing counts toward corpus targets until the reference app is built downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice. The handoff contract beside this file carries the nine gates that decide it.
