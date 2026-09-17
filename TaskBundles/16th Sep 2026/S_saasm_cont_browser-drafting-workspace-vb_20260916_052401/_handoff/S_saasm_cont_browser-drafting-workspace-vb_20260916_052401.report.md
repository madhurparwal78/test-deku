# Build report - S_saasm_cont_browser-drafting-workspace-vb_20260916_052401

## Identity

| | |
|---|---|
| Task code | `S_saasm_cont_browser-drafting-workspace-vb_20260916_052401` |
| Task id | `deku/browser-drafting-workspace-vb` |
| Cell | solo_founder / saas-micro-tools / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | backend `postgres`, storage `minio` |
| Variant | `b`, axes ['critical_depth', 'spec_sections'] |
| Language | `python` |
| Capability flags | `aesthetic` |
| Design direction | `companion` |
| Launch surface | `form_validation,privacy_page,sitemap_robots,social_preview,terms_page` |
| spec_sections_given | ['overview', 'roles', 'features', 'flow', 'uiux', 'frontend', 'techrequirements', 'datamodel', 'constraints', 'contract'] |
| Shard | 1 of 1 |

The Task Order arrived keyed `domain: saas-productivity`, `pattern:
collaborative-workspace`. Neither is a member of the closed enum. The literal
reading of the pattern, `collaboration-shared`, is refused by `taskorder_lint.py`
as a dead cell: every solo_founder-legal profile for it needs a `realtime` slot
and no provider in `environment/registry.json` serves one. Filed at the nearest
legal pair, `saas-micro-tools` + `content-publishing`, whose `P4-db-storage`
profile is the one the product actually needs. Recorded in
`_spec/S_saasm_cont_browser-drafting-workspace-vb_20260916_052401/00-decisions.md`.

## Derived-design draws

Drawn over the bare archetype `browser-drafting-workspace`, per reference/L L.4
and reference/O O.3.

```text
draw: render_model = spa-json-api
draw: backend = Litestar
draw: frontend = Preact + Vite
draw: design_direction = companion
draw: nav = sidebar-nav
draw: work_surface = card-grid
draw: create_flow = multi-step-wizard
draw: feedback = toast
```

The design-direction draw selects `glass-depth`; it does not govern, because a
companion PRD was supplied and reference/L L.6.1 hands the axis to the source.
`work_surface = card-grid` governs the drawing library, which the companion never
saw; the companion's infinite canvas governs the editor.

## Feature resolution

| Feature | Verdict | Where | Reason |
|---|---|---|---|
| Accounts and sessions | INCLUDED | `## Core features` / Auth | pattern baseline, open signup |
| Drawing library + three-step creation | INCLUDED | `## Core features` | the drawn create flow |
| Workspace, canvas, pan and zoom | INCLUDED | `## Core features` | companion sections 8, 23 |
| Precision input and the command input | INCLUDED | `## Core features` | companion section 9 |
| Creation and modification toolsets | INCLUDED | `## Core features` | companion sections 10, 11 |
| Layers and object properties | INCLUDED | `## Core features` | companion section 12 |
| Annotation and blocks | INCLUDED | `## Core features` | companion sections 13, 14 |
| Versions in the object store | INCLUDED | `## Core features` | the critical focus |
| Sharing, presence, comments, live reach | INCLUDED | `## Core features` | companion sections 18, 19 |
| Measure, markup, assistant | INCLUDED | `## Core features` | companion sections 17, 20 |
| The public edge | INCLUDED | `## Core features`, `## Technical requirements` | the drawn launch surface |
| Industry binary drawing format | DROPPED | `## Constraints` | undocumented, version evolving; an approximation corrupts real drawings (companion 21.2) |
| 3D solids, booleans, unified 2D/3D rendering | DROPPED | `## Constraints` | companion 21.1, 21.9: specialist work, not buildable in the agent budget |
| Variational constraint solver, dynamic block authoring | DROPPED | `## Constraints` | companion 21.4 |
| Massive assemblies with demand loading | DROPPED | `## Constraints` | companion 21.7 |
| External references and underlays | DROPPED | `## Constraints` | companion section 15 |
| Plotting, plot styles, publishing | DROPPED | `## Constraints` | companion section 16, partially kept as the paper space tab |
| Tables with formulas, fields, annotative scaling | DROPPED | `## Constraints` | companion section 13 tail |

Ten must-have features, inside the companion cap of 6-10
(`config/corpus-targets.yaml` `companion_feature_cap`). Every one is graded: the
G24 join closes in both directions.

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| db | `postgres` | MET | critical pytest substeps in `seeded_rows_survive_a_restart` and `drafter_draws_geometry_on_a_named_layer` |
| storage | `minio` | MET | critical pytest substeps in `drafter_saves_a_version_file_to_the_store` and `concurrent_saves_conflict_to_one_winner` |

## Grading surface

| | |
|---|---|
| Workflows | 16 (band for solo_founder is 10-16) |
| Browser substeps | 63 |
| Pytest substeps | 40 |
| Critical substeps | 15 |
| Non-happy-path ids | `unauthenticated_caller_is_denied`, `concurrent_saves_conflict_to_one_winner`, `reviewer_cannot_write_geometry`, `unshared_drawing_is_denied_to_everyone_else`, `invalid_input_is_refused_and_nothing_is_written` |
| Pytest module | one, `tests/test_output.py`, covering core features, data integrity, authorization, edge cases and the storage slot |
| Pytest functions | 40 |
| Checklist items | 256, at core-ask granularity |

## Rubric

23 judged criteria, 19 positive and 4 negative, all
GENERATED from `solution/trinity/grounding.yaml` through the vendored
`recompute.py` (`--check` reports no drift). Compiled-weight share of the
reference rubric: 0.9, above the 0.60 floor.

| Dimension | Criteria | Share | Target |
|---|---|---|---|
| `instruction_following` | 4 | 0.30 | 0.30 |
| `functionality` | 3 | 0.25 | 0.25 |
| `ux_flow` | 3 | 0.15 | 0.15 |
| `ui_visual` | 3 | 0.15 | 0.15 |
| `motion` | 2 | 0.07 | 0.05 |
| `accessibility` | 2 | 0.07 | 0.05 |
| `responsiveness` | 2 | 0.03 | 0.05 |

## Literals ledger

120 pinned values across 11 classes:
`account` 6, `credential` 1, `design_phrase` 18, `endpoint` 21, `env_var` 8, `motion_moment` 7, `number` 6, `route` 13, `scheme` 6, `seed_record` 14, `status` 20.
G6 holds the bijection in both directions between the ledger, `instruction.md`
and the graders.

## spec/ documents

Emitted to `Output/_spec/S_saasm_cont_browser-drafting-workspace-vb_20260916_052401/`, never inside the bundle (CON-5).

| Doc | Fed |
|---|---|
| `00-decisions.md` | the audit trail, the draws, and the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at this variant |

## Companion carriage

`autocad_prd.md` was supplied with the Task Order and is recorded in
`_handoff/S_saasm_cont_browser-drafting-workspace-vb_20260916_052401.sources.json`. G51 reports
24/24 source colours described by family and tone, 70/70 topics carried and
175/175 enumerated items carried, with nine declared waivers: the source's own
evidence-gap and acceptance-checklist sections, the observed-stack identifiers,
the motion curve values the number rule forbids, and the suggested component-tree
names. Each waiver and its reason is in `00-decisions.md`.

## Grading window

Reported by `window_lint.py`, never failed (G33 retired the length cap).

| Section | Chars | Reference |
|---|---|---|
| core_features | 18518 | 2400 |
| user_flow | 5048 | 1900 |
| ui_ux_notes | 9972 | 1700 |
| constraints | 2240 | 800 |
| user_roles | 1997 | 1000 |
| overview | 1941 | 700 |

The brief has no length limit. `## Core features`, `## User flow` and
`## UI/UX notes` run past the judge's 2,500-char slice; the tail reaches the agent
in full. No rule was cut to fit, and the judged criteria carry their own facts
(G52 PASS), so the slice costs a diagnostic number rather than reward.

## Kit gate log

Rendered from `_handoff/S_saasm_cont_browser-drafting-workspace-vb_20260916_052401.gates.jsonl`. Input fingerprint covers
23 bundle files.

| Gate | Tool | Exit | Verdict | State |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | ok |
| `G1/G12` | `layout_lint.py` | 0 | PASS | ok |
| `G46` | `structure_lint.py` | 0 | PASS | ok |
| `G50` | `docker_lint.py` | 0 | PASS | ok |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | ok |
| `G63` | `secret_lint.py` | 0 | PASS | ok |
| `G48` | `truth_lint.py` | 0 | PASS | ok |
| `G51` | `source_lint.py` | 0 | PASS | ok |
| `G52` | `rubric_context_lint.py` | 0 | PASS | ok |
| `G54` | `comment_lint.py` | 0 | PASS | ok |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | ok |
| `G11` | `leak_scan.py` | 0 | PASS | ok |
| `G33` | `window_lint.py` | 0 | PASS | ok |
| `G4/G5` | `contract_lint.py` | 0 | PASS | ok |
| `G43` | `prescription_lint.py` | 0 | PASS | ok |
| `G44` | `disclosure_lint.py` | 0 | PASS | ok |
| `G10` | `no_sdk_lint.py` | 0 | PASS | ok |
| `G31` | `determinism_lint.py` | 0 | PASS | ok |
| `G14` | `reward_path_lint.py` | 0 | PASS | ok |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | ok |
| `G41` | `flag_lint.py` | 0 | PASS | ok |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | ok |
| `G59/G60` | `codequality_lint.py` | 2 | ? | ok |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | ok |
| `G6` | `fixture_lint.py` | 0 | PASS | ok |
| `G24` | `coverage_map.py` | 0 | PASS | ok |
| `G37` | `checklist_qc.py` | 0 | PASS | ok |
| `G39` | `rubric_align_lint.py` | 0 | PASS | ok |
| `G28/G29` | `channel_lint.py` | 0 | PASS | ok |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | ok |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | ok |
| `G47` | `output_qc.py` | 0 | PASS | ok |

`G59/G60` returns exit 2 NOT-APPLICABLE: the bundle carries no code-quality
rubric. `G40` returns WARN because every certification prompt was run by the same
agent that authored the artifact, which the kit records as SELF-ATTESTED rather
than as an independent verdict.

## Certification prompts

All seven receipts are in `_handoff/S_saasm_cont_browser-drafting-workspace-vb_20260916_052401.receipts.json`, each bound to this
task code, each carrying a verdict for every id in its own registry: 292 check
verdicts in total, zero FAIL. Four divergences between a QC prompt's registry and
the kit's current emission rules are recorded there as findings against the
prompt rather than the bundle (the eleven-section list, the three-lever list, the
storage-level-invariant wording, and the numeric UI/UX value sheet), each one
superseded by `generate_instruction.md` §2.1 / §4, INV9/G43 or the retired G33
length cap.

Two real defects the prompts found were fixed during the pass and are recorded:
`tokens_expected` was above the absolute 8,000,000 ceiling, and the database
credentials diverged from the canonical `deku_app` / `deku_admin` /
`deku-local-dev` convention the kit's own provider fragment seeds. Four gaps in
the spec folder were fixed the same way.

## Budget

`turns_expected` 200, `tokens_expected` 8,000,000: the top of the documented
range, which is where a ten-feature companion-backed task at variant `b` sits.
`difficulty` stays the mandated empty placeholder; calibration writes it.

## Blocking findings

None. No spec gap and no harness gap prevented a required test. `[delivery.images]`
is deliberately empty pending registry access, as the handoff contract records.

## Versions

| | |
|---|---|
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Harbor | `0.20.0` |
| Kit self-test (G38) | PASS, 32 checks |

## Exit state

```text
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the reference app lands
downstream and `harbor run -a oracle` returns `1.0` twice.
