# Build report: deku/metaball-agency-portfolio-vb

Rendered from `_handoff/S_conte_cont_metaball-agency-portfolio-vb_20260916_053554.gates.jsonl`. No verdict in this file was
typed by hand; every row below is a receipt written by `revalidate.py`.

## Identity

| Field | Value |
|---|---|
| Task code | `S_conte_cont_metaball-agency-portfolio-vb_20260916_053554` |
| Task id | `deku/metaball-agency-portfolio-vb` |
| Cell | solo_founder / content-publishing / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | db `postgres`, storage `minio` |
| Variant | `b`, axes `critical_depth`, `spec_sections` (companion supplied) |
| Language | python |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Grader pin | 0.22.0 |
| Target schema | 1.4 |
| Verifier mode | shared |

## Derived draws

| Axis | Value |
|---|---|
| `render_model` | mpa-progressive |
| `backend` | Flask + Jinja |
| `frontend` | vanilla progressive enhancement |
| `nav` | top-nav |
| `work_surface` | card-grid |
| `create_flow` | multi-step-wizard |
| `feedback` | full-page-confirmation |
| `design_direction` | companion |
| `launch_surface` | cookie_choice, custom_404, form_validation, meta_tags, privacy_page |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Persistent metaball canvas and nine-control settings panel | INCLUDED | instruction.md `## Core features` | companion sections 8.1 to 8.7, the product's subject |
| Project index, case detail, credits, pagination | INCLUDED | `## Core features`, `## Front-end specification` | companion sections 13 and 14 |
| Topic index with category filter, topic detail | INCLUDED | `## Core features` | companion sections 17 and 18 |
| Team grid and company profile | INCLUDED | `## Core features` | companion sections 15 and 16 |
| Eleven-control enquiry form with consent gate | INCLUDED | `## Core features` | companion section 19, the one persisted state change |
| Editorial interface with a multi-step create sequence | INCLUDED | `## Core features` | companion 26.3 asks for an editorial interface; the wizard is the S1 draw |
| Bilingual editions at separate paths | INCLUDED | `## Core features` | companion section 21 |
| Privacy page, terms page, cookie choice, custom not-found, meta descriptions | INCLUDED | `## Core features` | reference/O launch-surface draw |
| Transactional acknowledgement email on enquiry | DROPPED | waived, recorded in `_spec/.../00-decisions.md` | no email slot in profile P4-db-storage; an unobservable obligation |
| Build order, seven stages | DROPPED | waived | a numbered implementation sequence is banned by INV9 |
| Evidence-gap and acceptance-checklist sections | DROPPED | waived | document provenance and exam material, not product obligations |

## Slot obligations

| Slot | Provider | State | Observed by |
|---|---|---|---|
| db | `postgres` | MET | `test_seeded_project_count_is_stable_across_repeat_reads`, `test_enquiry_submission_stores_exactly_one_record`, plus every store assertion |
| storage | `minio` | MET | `test_uploaded_hero_lands_in_the_bucket_under_the_key_scheme`, `test_draft_project_hero_object_really_exists_in_the_bucket` |

## Grading surface

| Measure | Value |
|---|---|
| Workflows | 16 (band 10 to 16) |
| Browser substeps | 45 |
| Pytest substeps | 44 |
| Critical substeps | 27 |
| Non-happy-path workflow ids | 6: draft_project_detail_is_denied_to_every_unentitled_caller, draft_topic_is_hidden_and_cannot_be_reached, enquiry_without_consent_is_rejected_at_the_api, enquiry_with_invalid_input_is_refused, reader_cannot_reach_the_editorial_surface, signup_cannot_escalate_to_the_editor_role |
| Pytest module | one, `tests/test_pytest.py`, 44 tests |
| Checklist items | 387 across ten section codes |
| Rubric criteria | 15 (12 positive, 3 negative) |

Checklist items by type tag: `capability` 75, `constraint` 40, `contract` 41, `data` 24, `literal` 54, `role` 15, `ui` 138.

The one pytest module carries every section: readiness and deployment contract, authorization, the draft boundary on both the route and the object store, the editorial create sequence, the enquiry channel with its four refusal paths, the seeded-content shape, and the site's own pages.

### Rubric dimension shares, positives only

| Dimension | Share | Target | Criteria |
|---|---|---|---|
| `instruction_following` | 0.310 | 0.30 | 3 |
| `functionality` | 0.238 | 0.25 | 2 |
| `ux_flow` | 0.143 | 0.15 | 2 |
| `ui_visual` | 0.143 | 0.15 | 2 |
| `motion` | 0.071 | 0.05 | 1 |
| `accessibility` | 0.071 | 0.05 | 1 |
| `responsiveness` | 0.024 | 0.05 | 1 |

## Literals ledger

129 entries. By class: `account` 2, `copy` 89, `credential` 1, `endpoint` 2, `env_var` 10, `number` 11, `route` 14.
Two entries are marked `verifier_only` and appear in neither the brief nor `[environment].env`. Every other entry is carried verbatim in `instruction.md`, and G6 holds the bijection in both directions.

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| `core_features` | 13040 | 2400 | past-slice |
| `user_flow` | 5155 | 1900 | past-slice |
| `ui_ux_notes` | 11482 | 1700 | past-slice |
| `constraints` | 1115 | 800 | over-reference |
| `user_roles` | 1649 | 1000 | over-reference |
| `overview` | 2336 | 700 | over-reference |

Length is reported and never failed (G33). The brief is long because the companion is a 3,900-line specification and CON-6 makes `instruction.md` the only file the agent reads: content dropped here was never asked for. `## Front-end specification` is unbudgeted and carries the visual detail that would otherwise push the six judged sections further past the slice.

## Kit gate log

One row per gate, rendered from the receipts.

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
| G59/G60 | `codequality_lint.py` | 2 | ? |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 1 | FAIL |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 1 | FAIL |

32 receipts. Red gates: 2.

## Blocking findings

1. **G40 prompt receipts, UNCITED.** The seven certification prompts (`QC_spec.md`, `QC_instruction.md`, `qc_toml.md`, `qc_docker.md`, `qc_solution_checklist.md`, `task_code_verifier.md`, `qc_rubric.md`) have not been run, so `_handoff/S_conte_cont_metaball-agency-portfolio-vb_20260916_053554.receipts.json` does not exist. Those are adversarial LLM reviews at temperature 0, and their registries total 292 declared checks. A receipt invented without running them is the exact defect G40 was built to catch, so none was written. **G47 is red only because G40 is**: its other four checks pass.

2. **`[delivery]` block omitted, grandfathered to NOT-APPLICABLE.** `[delivery.images]` requires a `@sha256:` digest for each image, while `reference/C` §C.4 forbids inventing digests and requires an architecture-neutral version tag. The two cannot both be satisfied without resolving real digests from a registry, which this run has no access to. The block is absent rather than fabricated, which `validate_task.py` grandfathers.

3. **The source half of `tests/rubric.json` is absent.** G59/G60 return NOT-APPLICABLE. The vendored `recompute.py` at pin 0.22.0 refuses any judged criterion whose dimension is outside the seven product dimensions, so the two authored code-quality dimensions (`scope_discipline`, `internal_consistency`) cannot pass through the generator. INV5 forbids editing the vendored generator, so the criteria were removed rather than the generator patched.

4. **Task Order domain re-keyed.** The order arrived with `domain: portfolio-agency`, which is not a member of the level-2 enum. It was re-keyed to `content-publishing`, the nearest legal domain for a studio site whose product is a project index, an editorial strand and their detail routes.

5. **Three scale constraints are judged, never measured.** `C-CN-10`, `C-CN-11` and `C-CN-12` state data volumes the app must stay responsive at. No channel in this bundle loads that volume, so they are carried by a rubric criterion rather than by a measurement.

## Handoff gates, undecided

See `_handoff/S_conte_cont_metaball-agency-portfolio-vb_20260916_053554.handoff.md`. Nothing in this bundle has been compiled, booted or run.

## Budget estimate

`turns_expected = 170`, `tokens_expected = 7000000`. The companion specifies twelve routes, two language editions, a continuous WebGL-class simulation with a nine-control panel, a motion system with five named reveal families, and an eleven-control form, all with zero shipped binaries. That is the hard rung of the kit's own band rather than the medium one, and variant `b` is the companion rung.

## Exit state

```
MECHANICALLY-GREEN (battery 1), NO-SOLUTION
G40 UNCITED -- the seven certification prompts have not been run
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the reference app lands downstream and `harbor run -a oracle` returns `1.0` twice.
