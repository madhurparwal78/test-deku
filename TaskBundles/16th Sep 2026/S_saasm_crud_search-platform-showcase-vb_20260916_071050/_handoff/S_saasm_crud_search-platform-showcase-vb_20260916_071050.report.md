# Build report: S_saasm_crud_search-platform-showcase-vb_20260916_071050

## Identity

| | |
|---|---|
| Task code | `S_saasm_crud_search-platform-showcase-vb_20260916_071050` |
| Task id | `deku/search-platform-showcase-vb` |
| Cell | solo_founder / saas-micro-tools / crud-catalog |
| Archetype | `search-platform-showcase` |
| Service profile | `P1-db` |
| Providers per slot | `backend = postgres` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `typescript` |
| Design direction | `companion` (drawn `clinical-precision`, overridden per reference/L L.6.1) |
| Launch surface | `colour_contrast,cookie_choice,meta_tags,mobile_viewport,privacy_page` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Vendored grader | 0.22.0 |
| Target schema | 1.4 |

## Source material

A companion PRD of 6,187 lines was supplied with the Task Order and is carried in
`_handoff/S_saasm_crud_search-platform-showcase-vb_20260916_071050.companion-prd.md`. G51 measured the carry:
43 of 43 source colours described by family and tone, 279 of 279 topics carried,
1,085 of 1,085 enumerated items carried, with six declared waivers recorded in the
G51 receipt. The waived subjects are the companion's own register meta, its
conformance suite, its taxonomy classification and gate-deviation notes, two
value-only rows that the A5 number rule forbids the brief from carrying, and the
asset-filename manifest.

## Feature resolution

| Candidate | Verdict | File | Reason |
|---|---|---|---|
| Site search overlay, two modes, live disjunctive counts | INCLUDED | instruction.md `## Core features` | the companion's section 8, the product demonstration |
| Eight-criterion ranking cascade with no score | INCLUDED | instruction.md `## Core features` | the companion's section 22.5, the core contract |
| Disjunctive facet counting and deduplication | INCLUDED | instruction.md `## Core features` | the companion's sections 23.4 and 23.6 |
| Faceted customer-story index | INCLUDED | instruction.md `## Core features` | the companion's section 12, the Task Order's catalog-browse shape |
| Four plans and the comparison grid | INCLUDED | instruction.md `## Core features` | the companion's section 10 |
| Demo request form, the one state-touching route | INCLUDED | instruction.md `## Core features` | the companion's section 13, the Task Order's ending action |
| Operator console, eleven destinations | INCLUDED | instruction.md `## Core features` | the companion's section 16 |
| Merchandising rules, synonyms, personalization, split runs | INCLUDED | instruction.md `## Core features` | the companion's section 24 |
| Keys, secured keys, quotas, audit | INCLUDED | instruction.md `## Core features` | the companion's section 26 |
| Events, attribution, rollups | INCLUDED | instruction.md `## Core features` | the companion's section 27 |
| Hybrid retrieval and the grounded answer | INCLUDED, translated | instruction.md `## Core features` | the companion's section 25; the model provider is replaced by an in-app vector and an extractive answer, recorded in 00-decisions.md |
| Multi-region cluster and physical replication | DROPPED | instruction.md `## Constraints` | one container; the observable half stays as generation binding, the task queue and the minimum-task read header |
| Automatic synonyms and query categorization | DROPPED | instruction.md `## Core features` rule 49 | the companion's section 35.5 records both as gaps; the comparison grid shows them absent in every column |
| Third-party consent, chat, tag manager, advertising, video player | DROPPED | instruction.md `## Constraints` | the companion's section 33.9 removes rather than replaces them |
| Payment of any kind | DROPPED | instruction.md `## Constraints` | no payments slot; the plans are displayed copy |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| backend | `postgres` | MET | G32 inside the G7/G8/G9/G32/G45 receipt; the critical pytest substeps read the persisted rows through the `db` capability adapter |

## Graded surface

| | |
|---|---|
| Workflows | 16 (solo_founder band 10 to 16) |
| Browser substeps | 29 |
| Pytest substeps | 53 |
| Critical substeps | 16 |
| Non-happy-path workflow ids | 5: `invalid_filter_is_refused_with_the_span_named`, `deduplicated_listing_counts_groups_without_duplicate_hits`, `signup_creates_a_workspace_and_an_invalid_form_is_refused`, `lower_role_write_is_denied_at_the_api`, `secured_key_cannot_be_widened_and_an_out_of_scope_index_is_denied` |
| Pytest module | one, `tests/test_output.py`, 53 test functions |
| Checklist items | 1002 over ten section codes |
| Banners covered | core features, authorization, data integrity, edge cases |

## Rubric

19 judged criteria, 19 positive and 0 negative, positive total 57. Per-dimension share of the positive total against the frozen weight:

| Dimension | Criteria | Share | Target | Within 0.10 |
|---|---|---|---|---|
| `instruction_following` | 4 | 0.25 | 0.30 | yes |
| `functionality` | 3 | 0.16 | 0.25 | yes |
| `ux_flow` | 3 | 0.16 | 0.15 | yes |
| `ui_visual` | 5 | 0.23 | 0.15 | yes |
| `motion` | 2 | 0.11 | 0.05 | yes |
| `accessibility` | 1 | 0.05 | 0.05 | yes |
| `responsiveness` | 1 | 0.05 | 0.05 | yes |

The answer key carries 53 compiled rubric items, one per committed grader, for a compiled-weight share of 1.0 against the 0.60 floor.

## Literals ledger

285 pinned values. By class:

| Class | Count |
|---|---|
| `account` | 5 |
| `credential` | 7 |
| `design_phrase` | 9 |
| `endpoint` | 6 |
| `env_var` | 4 |
| `motion_moment` | 7 |
| `number` | 20 |
| `route` | 8 |
| `scheme` | 8 |
| `seed_record` | 195 |
| `status` | 16 |

Carriers are `instruction.md` for every agent-visible value, plus `conftest.py` or
`test_output.py` where a grader asserts it. One value is `verifier_only`:
`DB_ADMIN_URL`, carried by `task.toml` alone per INV4.

## Spec folder

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the residual calls, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at this variant |

## Grading window

| Section | Chars | Reference | Past the slice |
|---|---|---|---|
| `Core features` | 63483 | 2400 | yes |
| `User flow` | 5493 | 1900 | yes |
| `UI/UX notes` | 17216 | 1700 | yes |
| `Constraints` | 1850 | 800 | no |
| `User roles` | 2363 | 1000 | no |
| `Overview` | 2649 | 700 | yes |
| joined (each capped at 2,500) | 14213 | 8,800 | yes |

The brief has no length limit and G33 reports rather than fails. The companion is
6,187 lines and G51 requires every enumerated item to reach the brief, so
`## Core features` runs long by construction; the cost is a diagnostic number, not
reward. `## Front-end specification` is unbudgeted and carries the visual half.

## Kit gate log

Rendered from the receipts. Never transcribed.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | - |
| G1/G12 | `layout_lint.py` | 0 | - |
| G46 | `structure_lint.py` | 0 | - |
| G50 | `docker_lint.py` | 0 | - |
| G55 | `runtime_deps_lint.py` | 0 | - |
| G63 | `secret_lint.py` | 0 | - |
| G48 | `truth_lint.py` | 0 | - |
| G51 | `source_lint.py` | 0 | - |
| G52 | `rubric_context_lint.py` | 0 | - |
| G54 | `comment_lint.py` | 0 | - |
| G17 | `secret_hygiene_lint.py` | 0 | - |
| G11 | `leak_scan.py` | 0 | - |
| G33 | `window_lint.py` | 0 | - |
| G4/G5 | `contract_lint.py` | 0 | - |
| G43 | `prescription_lint.py` | 0 | - |
| G44 | `disclosure_lint.py` | 0 | - |
| G10 | `no_sdk_lint.py` | 0 | - |
| G31 | `determinism_lint.py` | 0 | - |
| G14 | `reward_path_lint.py` | 0 | - |
| G27/G30 | `rubric_lint.py` | 0 | - |
| G41 | `flag_lint.py` | 0 | - |
| G56/G57/G58 | `if_lint.py` | 0 | - |
| G59/G60 | `codequality_lint.py` | 2 | - |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | - |
| G6 | `fixture_lint.py` | 0 | - |
| G24 | `coverage_map.py` | 0 | - |
| G37 | `checklist_qc.py` | 0 | - |
| G39 | `rubric_align_lint.py` | 0 | - |
| G28/G29 | `channel_lint.py` | 0 | - |
| G40 | `prompt_receipt_lint.py` | 0 | - |
| G0/INV5 | `vendor_check.py` | 0 | - |
| G47 | `output_qc.py` | 0 | - |

Every receipt carries the SHA-256 of each file it read; `output_qc.py --final`
re-checks those hashes against the bundle's current bytes.

## Prompt receipts

| Prompt | Gate | Verdict | Checks answered | Verifier |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | self |
| `QC_spec.md` | G34 | PASS | 15 | self |
| `qc_docker.md` | G35 | PASS | 105 | self |
| `qc_rubric.md` | G53 | PASS | 16 | self |
| `qc_solution_checklist.md` | G37 | PASS | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | self |
| `task_code_verifier.md` | G3 | VALID | 12 | self |

Every certification prompt was read and answered against its own registry. The
verifier is `self` on all seven: owner and verifier are one agent in this run, which
G40 records as SELF-ATTESTED rather than as an independent verdict. The five
advisory generator prompts other than `generate_instruction.md` carry no receipt and
are reported UNCITED, which is the honest state.

## Blocking findings

None that prevented a required test. Four recorded deviations, each with its
reasoning in `_spec/S_saasm_crud_search-platform-showcase-vb_20260916_071050/00-decisions.md`:

1. The Task Order's `domain` and `pattern` as written by the tasker are not members
   of the kit's closed enums; the mint uses the nearest legal members, which is the
   mapping the companion's own section 35.6 argues for.
2. The `crud-catalog` baseline of one role is raised to four, from the companion's
   section 16.7 permission matrix. Providers and slots are unchanged.
3. The answer pipeline and the vector store are specified without an external model,
   which the environment does not carry. Every observable of the companion's
   sections 25.1 to 25.4 survives the translation.
4. The physical cluster of the companion's section 28.1 is waived; its observable
   half is carried as generation binding, the task queue and the minimum-task header.

## Budget

`turns_expected = 180`, `tokens_expected = 7500000`. The bundle is a variant `b`
build with one datastore slot, four roles, a 1,002-item coverage target and a
6,187-line companion carried into the brief, so it sits above the corpus median on
surface area and at the top of the standard tier on budget.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

Not admissible. The bundle carries no reference app. It becomes admissible when the
app is built downstream from `solution/checklist.md` and `harbor run -a oracle`
returns `1.0` twice.
