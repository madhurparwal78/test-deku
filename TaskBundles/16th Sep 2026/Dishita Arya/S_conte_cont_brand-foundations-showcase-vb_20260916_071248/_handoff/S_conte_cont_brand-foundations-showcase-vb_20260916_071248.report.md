# Build report -- S_conte_cont_brand-foundations-showcase-vb_20260916_071248

## Identity

| | |
|---|---|
| task code | `S_conte_cont_brand-foundations-showcase-vb_20260916_071248` |
| task id | `deku/brand-foundations-showcase-vb` |
| cell | solo_founder / content-publishing / content-publishing |
| archetype | `brand-foundations-showcase`, variant `b` |
| service profile | `P4-db-storage` |
| providers | `backend = postgres`, `storage = minio` |
| variant axes | `spec_sections`, `critical_depth` |
| language | `python` |
| spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 |
| companion | `prds/brand_prd.md` |
| exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## The derived-design draws

Every one is a SHA-256 draw over the archetype, recorded as a `draw:` line in
`_spec/S_conte_cont_brand-foundations-showcase-vb_20260916_071248/00-decisions.md`.

```
render_model    = spa-json-api
backend         = FastAPI
frontend        = Lit + Vite
design_direction= companion            (reference/L L.6.1: a companion beats the draw;
                                        the bank token this archetype would have drawn is
                                        dense-ops-console, which contradicts the measured
                                        gallery character outright)
nav             = top-nav
work_surface    = card-grid
create_flow     = multi-step-wizard
feedback        = optimistic-row
launch_surface  = mobile_viewport, no_broken_links, single_cta, sitemap_robots, social_preview
```

## Feature resolution

| Candidate | Verdict | Where |
|---|---|---|
| Index carousel, five advertised chapters | INCLUDED | `## Core features`, `## Front-end specification` |
| Scroll-driven colour system, four tone groups per tier | INCLUDED | `## Core features`, `## UI/UX notes` |
| The named reveals and the scroll contract | INCLUDED | `## Core features`, `## UI/UX notes` |
| Colour chapter, poster stacks, swatch and shuffle | INCLUDED | `## Core features`, `## Front-end specification` |
| Logo chapter, mark-as-mask, lockups, in-use gallery | INCLUDED | `## Core features`, `## Front-end specification` |
| Three-dimensional model surface with a halting loop | INCLUDED | `## Core features` |
| Generated imagery in the object store | INCLUDED | `## Core features`, `## Deployment contract` |
| Free-trial capture, three pre-rendered states | INCLUDED | `## Core features` |
| Author surface: wizard, reorder, generate, publish | INCLUDED | `## Core features`, `## User flow` |
| Chrome, not-found body, launch surface | INCLUDED | `## Core features`, `## Technical requirements` |
| Companion section 21, the build order | DROPPED | a build order is a work order rather than a specification; `## Build plan` is not emitted at variant `b` |
| Reference DOM class names (scrubbed-selector rows) | DROPPED | observed implementation, not requirement; waived on G51 |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| backend | postgres | MET | `test_seeded_chapters_are_persisted_rows`, `test_section_reorder_leaves_positions_contiguous_and_stored`, `test_trial_signup_is_stored_once_per_address` |
| storage | minio | MET | `test_generated_object_exists_in_the_bucket_at_its_key`, `test_object_key_carries_the_digest_of_the_stored_bytes`, `test_bucket_is_not_publicly_readable` |

## The grading channels

| | |
|---|---|
| workflows | 16 (band for solo_founder is 10 to 16) |
| browser substeps | 77 |
| pytest substeps | 45 |
| critical substeps | 11 |
| non-happy-path ids | `duplicate_and_invalid_trial_submissions_are_refused`, `reader_is_denied_the_author_surface`, `draft_chapters_cannot_be_read_by_anyone_but_their_author` |
| pytest module | one, `tests/test_output.py`, 45 test functions |
| rubric criteria | 16, all positive, positive total 44 |
| checklist items | 619 across ten sections |

Rubric dimension shares, against the frozen weights:

| Dimension | Criteria | Share | Weight |
|---|---|---|---|
| instruction_following | 3 | 0.30 | 0.30 |
| functionality | 3 | 0.25 | 0.25 |
| ux_flow | 3 | 0.20 | 0.15 |
| ui_visual | 6 | 0.18 | 0.15 |
| motion | 1 | 0.07 | 0.05 |

`accessibility` and `responsiveness` carry no criterion: both are stated in the brief as bars
and are graded by the browser channel, which is where a bar that holds at three widths is
actually observed. `reference/I` I.5 allows the 0.05 dimensions to be empty.

## Coverage

Two-way, decided by `coverage_map.py` (G24) and `channel_lint.py` (G28/G29):

| Channel | Items cited |
|---|---|
| pytest | 175 |
| browser | 428 |
| rubric | 16 |
| **total** | **619 of 619** |

Zero items are graded by two channels. `rubric_align_lint.py` (G39) reports 190 of 190
judgment-class obligations graded.

## Literals ledger

`_handoff/S_conte_cont_brand-foundations-showcase-vb_20260916_071248.literals-ledger.json`, 212 entries, every carrier computed from the
bytes rather than claimed:

| Class | Count |
|---|---|
| `account` | 4 |
| `credential` | 1 |
| `design_phrase` | 19 |
| `endpoint` | 14 |
| `env_var` | 8 |
| `motion_moment` | 7 |
| `number` | 15 |
| `route` | 23 |
| `scheme` | 2 |
| `seed_record` | 55 |
| `status` | 64 |

One entry is `verifier_only`: `DB_ADMIN_URL`, carried by `task.toml` alone. G6 confirms it
appears in neither the brief nor any agent-visible grader.

## The spec folder

Written to `output_16sep/_spec/S_conte_cont_brand-foundations-showcase-vb_20260916_071248/`, outside the bundle (CON-5).

| Doc | Feeds |
|---|---|
| `00-decisions.md` | the draws, the taxonomy call, the identity re-cast, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing in the brief: `## Build plan` is not emitted at variant `b` |

## Grading window

Reported by `window_lint.py`, which measures and never fails:

| Section | Chars | Reference |
|---|---|---|
| Core features | 15458 | 2400 |
| UI/UX notes | 10974 | 1700 |
| User flow | 5185 | 1900 |
| Overview | 2836 | 700 |
| User roles | 1828 | 1000 |
| Constraints | 1299 | 800 |
| joined | 37556 | 8800 |

The tasker asked for the cap to be ignored on this bundle. Everything past the slice reaches the
agent in full and is graded by the pytest layer and the browser channel; what it loses is the
advisory judge score, which never touches reward.

## Kit gate log

Rendered from `_handoff/S_conte_cont_brand-foundations-showcase-vb_20260916_071248.gates.jsonl`. 29 green, 2 red, 1 not-applicable.

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
| G59/G60 | `codequality_lint.py` | 2 | ? |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 1 | FAIL |

### The red

**G46 `structure_lint.py`** -- CON-1 placement. The bundle sits inside the tree that holds the
generation kit. The tasker chose `output_16sep/` and reaffirmed it; `output_root` cannot move the
half of the check that reads the tool's own `__file__`. Recorded, not repaired, and not loosened.
**G47 `output_qc.py`** is red only because it reads G46's receipt.

### Certification prompts

`prompt_receipt_lint.py` (G40) exits 0 WARN. Every certification prompt has a bundle-bound
receipt carrying the scorecard its own registry declares:

| Prompt | Gate | Verdict | Checks answered |
|---|---|---|---|
| `QC_spec.md` | G34 | PASS | 15 |
| `QC_instruction.md` | G34 | PASS | 24 |
| `qc_rubric.md` | G53 | PASS | 16 |
| `qc_toml.md` | G36 | PASS | 120 |
| `qc_docker.md` | G35 | PASS | 105 |
| `qc_solution_checklist.md` | G37 | PASS | 0 |
| `task_code_verifier.md` | G3 | VALID | 12 |
| `generate_instruction.md` | S2 | PASS | 0 |

All eight are SELF-ATTESTED: one agent owned and verified. Five generator prompts are UNCITED
and say so on the receipt.

## Blocking findings

None inside the bundle. The one red is the placement the tasker chose, and the one omission is
`[delivery.images]`, both recorded in the handoff contract.

## Budget

`turns_expected = 200`, `tokens_expected = 7500000`. The task carries two backing services, two
roles plus a signed-out surface, a nine-table schema, a scroll-driven repaint system, a
three-dimensional surface and a companion-derived front-end specification, which puts it at the
top of the band rather than the middle.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

Not admissible. Nothing counts toward corpus targets until the reference app lands and
`harbor run -a oracle` returns `1.0` twice.
