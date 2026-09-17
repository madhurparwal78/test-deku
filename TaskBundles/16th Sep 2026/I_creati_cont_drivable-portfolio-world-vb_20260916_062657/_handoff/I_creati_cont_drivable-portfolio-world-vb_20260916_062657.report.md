# Build report - I_creati_cont_drivable-portfolio-world-vb_20260916_062657

## Identity

| | |
|---|---|
| Task code | `I_creati_cont_drivable-portfolio-world-vb_20260916_062657` |
| Task id | `deku/drivable-portfolio-world-vb` |
| Cell | individual / creative-personal / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | `backend = postgres`, `storage = minio` |
| Variant | `b`, axes `spec_sections`, `critical_depth` |
| Language | `python` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1, no device sharding configured |
| Source document | `9.16_prds/prd2/brunosimon_prd.md`, a companion PRD of 3,558 lines |

The Task Order named `prd1`; that folder holds an unrelated document. `prd2` is the one
whose `url.md` is the subject of this task, and it is what was carried.

## Derived-design draws, R4, SHA-256 over the archetype

| Axis | Value |
|---|---|
| render_model | `mpa-progressive` |
| backend | FastAPI with Jinja templates |
| frontend | HTMX over server-rendered templates |
| nav | `top-nav`, which governs the studio; the public world carries no navigation |
| work_surface | `card-grid` |
| create_flow | `slide-over` |
| feedback | `full-page-confirmation` |
| design_direction | `companion`; the drawn `clinical-precision` does not govern, reference/L S L.6.1 |
| launch_surface | `cookie_choice`, `no_broken_links`, `page_view_log`, `single_cta`, `spam_protection` |

## Feature resolution

| Candidate | Verdict | Where it landed |
|---|---|---|
| The drivable world and its objects | INCLUDED | `## Core features` rules 17-25, `## Front-end specification` |
| The private studio and the publish boundary | INCLUDED | `## Core features` rules 3-8, the critical focus |
| Poster bytes in the object store | INCLUDED | `## Core features` rules 9-11 |
| The text route | INCLUDED | `## Core features` rules 15-16 |
| Achievements, map, circuit, whispers | INCLUDED | `## Core features` rules 26-39 |
| Shared state, page views, cookie choice | INCLUDED | `## Core features` rules 40-44 |
| The companion's binary socket transport | TRANSLATED | carried as observable behaviour; no realtime provider is declared for this profile |
| Companion S 22 build order | WAIVED | a numbered implementation sequence is banned outside `## Build plan`, INV9 |
| Companion S 25 evidence gaps | WAIVED | evidence provenance about a captured reference, not a product requirement |
| Companion data-volume line | DECLARED, UNGRADED | stated in `## Constraints`; no grader can seed 200 projects inside a run |

## Slot obligations

| Slot | Provider | Status | Observed by |
|---|---|---|---|
| `backend`, the db slot | postgres | MET | `test_publish_persists_row_and_stored_object`, critical |
| `storage` | minio | MET | `test_poster_upload_lands_in_bucket_at_scheme_key`, critical |

No slot is UNMET.

## Grading surface

| | |
|---|---|
| Workflows | 10, against an individual band of 6 to 11 |
| Browser substeps | 19 |
| Pytest substeps | 40 |
| Critical substeps | 9 |
| Non-happy-path workflow ids | `publish_at_occupied_coordinates_conflict`, `concurrent_publish_at_one_point_has_one_winner`, `anonymous_cannot_reach_a_draft`, `anonymous_write_attempts_are_denied`, `visitor_leaves_a_whisper_over_the_limit`, `visitor_runs_a_timed_lap_with_invalid_splits` |
| Pytest module | one, `tests/test_output.py`, 40 test functions |
| Section concerns covered | core features, data integrity, authorization, edge cases, storage |
| Checklist items | 118, every one cited by at least one grader, G24 |
| Rubric criteria | 12, all positive, all product-dimension |

### Rubric dimension shares

| Dimension | Points | Share | Target |
|---|---|---|---|
| `instruction_following` | 11 | 0.324 | 0.30 |
| `functionality` | 8 | 0.235 | 0.25 |
| `ux_flow` | 6 | 0.176 | 0.15 |
| `ui_visual` | 6 | 0.176 | 0.15 |
| `motion` | 1 | 0.029 | 0.05 |
| `accessibility` | 1 | 0.029 | 0.05 |
| `responsiveness` | 1 | 0.029 | 0.05 |

## Literals ledger

| Class | Count |
|---|---|
| `account` | 1 |
| `credential` | 1 |
| `design_phrase` | 9 |
| `endpoint` | 17 |
| `env_var` | 8 |
| `motion_moment` | 6 |
| `number` | 2 |
| `route` | 10 |
| `scheme` | 6 |
| `seed_record` | 30 |
| `status` | 52 |

Total 142 pinned values. One is `verifier_only`, `DB_ADMIN_URL`, carried in
`[verifier].env` and absent from the brief, INV4.

## Grading window

| Section | Chars | Reference |
|---|---|---|
| Core features | 13725 | 2400 |
| User flow | 3959 | 1900 |
| UI/UX notes | 4738 | 1700 |
| Constraints | 1667 | 800 |
| User roles | 1511 | 1000 |
| Overview | 1929 | 700 |

The six join to roughly 27,500 characters against a 9,000-character judge window. This is
reported, never failed: `window_lint.py` caps nothing and `judge_score` never touches
reward. The critical publish-boundary rules are front-loaded into the first 2,500
characters of `## Core features` so the judge reads them, and the tail reaches the agent
in full. The long visual specification lives in the unbudgeted
`## Front-end specification`, which is what that section exists for.

## Spec folder

Authored at `9.16_tasks/task 2/_spec/I_creati_cont_drivable-portfolio-world-vb_20260916_062657/`, outside the bundle, CON-5.

| Doc | Fed |
|---|---|
| `00-decisions.md` | the audit trail, the draws, the companion carry table, the G51 waivers |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing: `## Build plan` is not emitted at baseline |

## Kit gate log

Rendered from `_handoff/I_creati_cont_drivable-portfolio-world-vb_20260916_062657.gates.jsonl`, never transcribed.

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

`G59/G60` exits 2, NOT-APPLICABLE: the bundle carries no code-quality rubric, because
`recompute.py` renders `tests/rubric.json` from `judged_criteria`, whose dimension enum
admits only the seven product dimensions.

### Warnings carried, not suppressed

- `G41 launch_surface`: the brief carries ten bank obligations, the five drawn plus five
  the companion volunteered. Five is a floor, so an overlap is correct behaviour.
- `G41 window`: `## Core features` runs past the judge slice. See the grading window above.
- `G40`: every certification prompt is SELF-ATTESTED. Owner and verifier are one agent in
  this run, so these are recorded verdicts, never independent ones.
- `G40`: `solution_checklist.md`, `pytest_generator.md` and `rubric_author.md` carry no
  receipt and are UNCITED. Those three stages were built from the distilled contracts in
  `reference/G`, `reference/J` and `reference/I` rather than from the prompts themselves.
  All three are advisory under that gate.

## Blocking findings

None for this bundle. Both declared providers resolve to a pinned image in
`reference/C` S C.2.1.

`[delivery.images]` is deliberately absent. G2 validates the block without it, the digest
pins cannot be resolved offline, and fabricating one is forbidden by `reference/C` S C.4.
The operator resolves the manifest-list digests at build time.

## Budget

`turns_expected = 260`, `tokens_expected = 7800000`. The companion carries a whole product
rather than five lines, and the brief states ten must-have features with a grader for each,
so the estimate sits near the top of the documented band rather than at the baseline.
`tokens_expected` is held inside the 200,000 to 8,000,000 absolute range `qc_toml` BENCH-004
pins.

## Versions

| | |
|---|---|
| Kit | `deku-green-field`, tree as re-synced 2026-09-16 12:45 |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Verifier mode | `shared`, D2 |
| Canary | present in `solution/TRUTH.md` and `solution/USER_README.md`, absent from the brief |

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. No reference app exists, and nothing here has been compiled or run.
