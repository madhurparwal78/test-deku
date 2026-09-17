# Build report - S_local_cont_creative-studio-archive-vb_20260916_075740

| | |
|---|---|
| Task code | `S_local_cont_creative-studio-archive-vb_20260916_075740` |
| Task id | `deku/creative-studio-archive-vb` |
| Cell | solo_founder / local-services / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | `backend` = `postgres`, `storage` = `minio` |
| Variant | `b` on axes ['critical_depth', 'spec_sections'] |
| Language | `typescript` |
| Capability flags | `aesthetic` |
| Design direction | `companion` |
| Launch surface | `custom_404,form_validation,mobile_viewport,privacy_page,security_headers` |
| Spec sections given | ['overview', 'roles', 'features', 'flow', 'uiux', 'frontend', 'techrequirements', 'datamodel', 'constraints', 'contract'] |
| Shard | 1 of 1 |
| Kit | deku-green-field, gate index G0-G63 |
| Grader pin | `0.22.0` |
| Target schema | `1.4` |
| Verifier mode | `separate` |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Source material

A companion specification was supplied with the Task Order and is the tasker's real intent.
`task-orders/creative-studio-archive.prd.md` is the task-scoped distillation carried into the
brief; it descends from `prd/synchronized_prd.md`, the measured capture the tasker supplied.
G51 was run against the companion: 10/10 colours described by family and tone, 32/32 topics and
55/55 enumerated items carried. Swept against the RAW capture as well, for the record: 10/10
colours, 254/301 topics and 1124/1202 items, with the shortfall concentrated in the subsystems
this environment cannot carry (transactional mail, analytics, webhooks, the edge cache, the job
runner, a second content platform and multi-locale delivery). Every one of those is recorded in
the companion carry table in `Output/_spec/<code>/00-decisions.md` with its reason.

## Derived design draws

Drawn by SHA-256 over `[metadata].archetype`, never chosen:

```
draw: render_model = mpa-progressive
draw: backend = Express + Nunjucks
draw: frontend = vanilla progressive enhancement
draw: design_direction = companion
draw: nav = sidebar-nav
draw: work_surface = card-grid
draw: create_flow = slide-over
draw: feedback = toast
```

`design_direction` is `companion` rather than the bank token the draw selects: reference/L
section L.6.1 gives a supplied companion priority over the bank, because the bank exists to stop
monoculture when the only input is five lines, and this task came from a measured product.

## Feature resolution

| Candidate | Verdict | Where it landed | Reason |
|---|---|---|---|
| The eight-block home sequence | INCLUDED | Core features, Front-end specification | the companion's section 12, the product's spine |
| The numbered case stack with a derived veil | INCLUDED | Core features | the companion's section 12; the veil is the one derived number a grader can hold the app to |
| The draggable archive wall | INCLUDED | Core features, Front-end specification | the companion's section 13; the generated layout gives two deterministic invariants |
| The case study surface | INCLUDED | Core features | the companion's section 14; carries the draft-confidentiality boundary |
| The showreel | INCLUDED | Core features | the companion's section 15, scoped to poster plus renditions from the object store |
| Awards counted from win records | INCLUDED | Core features | the companion's section 16; counts derived on read |
| The work inquiry with its four defence layers | INCLUDED | Core features | the companion's section 17; carries the idempotency key |
| The studio console | INCLUDED | Core features, UI/UX notes | the companion's section 18 |
| Client preview and the publication gate | INCLUDED | Core features | the companion's section 19; the largest commercial risk in the product |
| Revisions, states and the append-only trail | INCLUDED | Core features, Data model | the companion's section 20 |
| Inquiry routing, merging and erasure | INCLUDED | Core features | the companion's section 21 |
| Imagery in the object store | INCLUDED | Core features | the companion's section 22; the pattern's critical focus |
| Transactional mail and the message catalogue | DROPPED | - | no email slot in P4-db-storage; an inquiry is acknowledged on the screen |
| Analytics collector and the event pipeline | DROPPED | - | no external calls at runtime; the studio's numbers are computed from stored rows |
| Webhook receivers and team chat | DROPPED | - | no inbound integration surface in this environment |
| Edge cache, tags and stale serving | DROPPED | - | no cache slot |
| Background job runner and the outbox | DROPPED | - | no queue slot; the link check and the retention sweep are console actions |
| One-time sign-in links and a second factor | DROPPED | - | no mail slot; staff sign in with the corpus password |
| Multi-locale delivery and translation documents | DROPPED | - | one language, recorded in Constraints |
| Scheduled publication | DROPPED | - | no job runner; publication is an action a lead takes |
| A logging rule no channel can observe | DROPPED | - | G24 has no waiver for an uncitable item, so no checklist item was minted for it |

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_seeded_case_veil_values_step_evenly_down_the_stack` (critical), plus 30 further tests reading the tables the brief names |
| `storage` | `minio` | MET | `test_an_uploaded_case_cover_is_stored_in_the_object_store_under_its_key` (critical), `test_the_uploaded_archive_image_lives_under_the_archive_key_prefix`, `test_an_uploaded_file_renamed_to_another_extension_is_refused` |

No slot is UNMET.

## Graders

- Workflows: **16** (solo_founder band 10-16)
- Browser substeps: **42** - pytest substeps: **85** - ratio **0.49** (G45 band 0.40-2.00)
- Critical substeps: **14**
- Non-happy-path workflow ids: `invalid_inquiry_is_rejected_with_a_message_per_field`, `duplicate_submission_key_creates_at_most_one_inquiry`, `writer_cannot_publish_a_case`, `unpublished_case_is_denied_to_a_stranger`, `stale_revision_save_is_rejected_on_conflict`
- One pytest module, `tests/test_output.py`, **85** tests across the core-features,
  data-integrity, authorization, edge-case and storage concerns.
- Checklist: **182** items across ten section codes (`capability` 56, `constraint` 6, `contract` 38, `data` 19, `literal` 4, `role` 8, `ui` 51)

## Rubric

20 judged criteria, all positive, no negative emitted: the brief licenses no
commission criterion that does not mirror a positive, and a mirrored negative fails RC-02.

| Dimension | Criteria | Positive share | Target | Delta |
|---|---|---|---|---|
| `instruction_following` | 3 | 0.283 | 0.30 | -0.017 |
| `functionality` | 4 | 0.261 | 0.25 | +0.011 |
| `ux_flow` | 2 | 0.130 | 0.15 | -0.020 |
| `ui_visual` | 3 | 0.152 | 0.15 | +0.002 |
| `motion` | 3 | 0.065 | 0.05 | +0.015 |
| `accessibility` | 3 | 0.065 | 0.05 | +0.015 |
| `responsiveness` | 2 | 0.043 | 0.05 | -0.007 |

Task-completion share 0.70 (band 0.60-0.80).
The rubric is GENERATED from `judged_criteria` in `solution/trinity/grounding.yaml`; G48 re-runs
the generator under `--check` on every sweep, so it cannot be hand-edited.

## Literals ledger

228 pinned values, every one present verbatim in `instruction.md`:

| Class | Count |
|---|---|
| `account` | 3 |
| `credential` | 1 |
| `design_phrase` | 3 |
| `endpoint` | 38 |
| `env_var` | 8 |
| `motion_moment` | 4 |
| `number` | 24 |
| `route` | 12 |
| `scheme` | 26 |
| `seed_record` | 75 |
| `status` | 34 |

One value is `verifier_only`: `DB_ADMIN_URL`, carried by `task.toml` `[verifier].env` alone (INV4).

## Spec folder

Written to `Output/_spec/<code>/`, never inside the bundle (CON-5).

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the residual judgment calls, the companion carry table |
| `01-PRD.md` | Overview, Core features, Constraints |
| `02-TRD.md` | Technical requirements |
| `03-app-flow.md` | User flow |
| `04-uiux-brief.md` | UI/UX notes, Front-end specification |
| `05-backend-schema.md` | Data model, User roles |
| `06-implementation-plan.md` | author-side only; Build plan is not emitted at baseline |

## Grading window

```
section        H2                chars  reference  flag
core_features  Core features     20960       2400  past-slice
user_flow      User flow          4099       1900  past-slice
ui_ux_notes    UI/UX notes       15762       1700  past-slice
constraints    Constraints        1163        800  over-reference
user_roles     User roles         1978       1000  over-reference
overview       Overview           2272        700  over-reference
joined total                     46234       8800  past-slice
first four                       41984       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```

The operator waived the section targets for this task so the UI and UX direction the companion
carries could be stated in full. G33 measures length and fails nothing on it: content past the
slice reaches the agent in full, stops reaching the advisory judge, and `judge_score` never
touches reward. Recorded again as QC_instruction C7 in the prompt receipts.

## Kit gate log

Rendered from `_handoff/<code>.gates.jsonl`. Never transcribed.

| Gate | Tool | Exit | Verdict | Seconds |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | 0.04 |
| `G1/G12` | `layout_lint.py` | 0 | PASS | 0.03 |
| `G46` | `structure_lint.py` | 0 | PASS | 0.04 |
| `G50` | `docker_lint.py` | 0 | PASS | 0.02 |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | 0.04 |
| `G63` | `secret_lint.py` | 0 | PASS | 0.02 |
| `G48` | `truth_lint.py` | 0 | PASS | 0.2 |
| `G51` | `source_lint.py` | 0 | PASS | 0.04 |
| `G52` | `rubric_context_lint.py` | 0 | PASS | 0.03 |
| `G54` | `comment_lint.py` | 0 | PASS | 0.03 |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | 0.03 |
| `G11` | `leak_scan.py` | 0 | PASS | 0.04 |
| `G33` | `window_lint.py` | 0 | PASS | 0.03 |
| `G4/G5` | `contract_lint.py` | 0 | PASS | 0.04 |
| `G43` | `prescription_lint.py` | 0 | PASS | 0.07 |
| `G44` | `disclosure_lint.py` | 0 | PASS | 0.04 |
| `G10` | `no_sdk_lint.py` | 0 | PASS | 0.06 |
| `G31` | `determinism_lint.py` | 0 | PASS | 0.06 |
| `G14` | `reward_path_lint.py` | 0 | PASS | 0.03 |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | 0.03 |
| `G41` | `flag_lint.py` | 0 | PASS | 0.05 |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | 0.03 |
| `G59/G60` | `codequality_lint.py` | 2 | ? | 0.03 |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | 0.07 |
| `G6` | `fixture_lint.py` | 0 | PASS | 0.1 |
| `G24` | `coverage_map.py` | 0 | PASS | 0.08 |
| `G37` | `checklist_qc.py` | 0 | PASS | 0.07 |
| `G39` | `rubric_align_lint.py` | 0 | PASS | 0.08 |
| `G28/G29` | `channel_lint.py` | 0 | PASS | 0.06 |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | 0.05 |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | 0.04 |
| `G47` | `output_qc.py` | 0 | PASS | 0.06 |

Corpus-level gates, run once over the whole output root rather than per bundle:

| Gate | Tool | Verdict |
|---|---|---|
| `G42` | `corpus_overlap.py` | PASS - 24 bundles, 1 cross-archetype pair compared, none over 60% substep overlap |
| `G49` | `diversity_lint.py` | PASS - 24 bundles, no concentration over cap, no shared run over the per-section caps |
| `G61` | `corpus_report.py` | NOT-APPLICABLE - 24 minted, 24 unproven; no admissible bundle to measure a mix against |
| `G38` | `kit_selftest.py` | PASS - 32 cross-file agreement checks |

## Prompt receipts

`_handoff/<code>.receipts.json`, 292 declared checks answered across 9 prompts.

| Prompt | Gate | Verdict | Checks | Non-PASS |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | A1 WARN, B1 WARN, B3 WARN, C4 WARN, C5 WARN, C7 WARN |
| `QC_spec.md` | G34 | PASS | 15 | B1 WARN, S2 WARN |
| `generate_instruction.md` | S2 | PASS | 0 | - |
| `qc_docker.md` | G35 | PASS | 105 | BLD-002 NOT-APPLICABLE, BP-004 NOT-APPLICABLE, CMP-011 WARN, CMP-020 WARN, DEP-004 WARN, DEP-011 NOT-APPLICABLE, DEP-015 NOT-APPLICABLE, DEP-016 NOT-APPLICABLE, DEP-017 NOT-APPLICABLE |
| `qc_rubric.md` | G53 | PASS | 16 | RC-10 NOT-APPLICABLE |
| `qc_solution_checklist.md` | G37 | PASS | 0 | - |
| `qc_toml.md` | G36 | PASS | 120 | BENCH-002 NOT-APPLICABLE, BENCH-003 NOT-APPLICABLE, BENCH-005 NOT-APPLICABLE, INST-007 NOT-APPLICABLE, INT-007 NOT-APPLICABLE, SCHEMA-011 WARN, SCHEMA-013 WARN, SIGN-001 NOT-APPLICABLE, SIGN-002 NOT-APPLICABLE, SIGN-003 NOT-APPLICABLE, TAX-006 NOT-APPLICABLE, TAX-008 NOT-APPLICABLE |
| `task_code_verifier.md` | G3 | VALID | 12 | - |
| `toml_generator.md` | S4 | PASS | 0 | - |

Every receipt is SELF-ATTESTED: owner and verifier are one agent in this run. The kit's rule is
owner != verifier, so these are recorded verdicts rather than independent ones. Four advisory
generator prompts carry no receipt and are reported UNCITED by G40 as notes rather than failures:
`solution_checklist.md`, `pytest_generator.md`, `docker_generator.md`, `rubric_author.md`.

## Blocking findings

None. Two obligations were resolved rather than shipped:

- The companion's logging rule (a log line never carries an inquiry's message text) is stated in
  the brief and carries no checklist item, because no channel in this environment can observe a
  log line and G24 has no waiver for an uncitable item.
- The `solo_founder` open-signup modifier is inverted: this product has no public account, and a
  route that mints one is a route that mints a reader of unpublished client work.

## Budget

`turns_expected` 165, `tokens_expected` 6000000. The reasoning: two surfaces in one
codebase, sixteen tables, a generated wall layout, a revision-bound approval gate and a
progressive-enhancement stack whose accelerated layers are optional. That is above the middle of
the band and below the top of it. `difficulty` stays the empty calibration placeholder: the
Calibration Engineer writes it, never the author.

## Exit

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts this bundle toward corpus targets until the reference app is
built downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
