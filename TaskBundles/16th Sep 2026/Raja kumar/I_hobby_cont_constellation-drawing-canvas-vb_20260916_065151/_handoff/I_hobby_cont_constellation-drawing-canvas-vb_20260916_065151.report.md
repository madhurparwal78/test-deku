# Build report: I_hobby_cont_constellation-drawing-canvas-vb_20260916_065151

State: MECHANICALLY-GREEN, NO-SOLUTION. Not admissible.

Authors: utsav.jain@ethara.ai (QL), raja.kumarint17@ethara.ai (contributor).
Verifier mode: separate, the kit default as of commit 11eaf7b.

## Kit gate log

Rendered from `_handoff/I_hobby_cont_constellation-drawing-canvas-vb_20260916_065151.gates.jsonl`. Never transcribed.

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

Gates recorded: 32. All green: True.

## Prompt receipts (battery 2)

| Prompt | Gate | Verdict | Checks answered | Verifier |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | self |
| `QC_spec.md` | G34 | PASS | 15 | self |
| `generate_instruction.md` | S2 | PASS | 0 | self |
| `qc_docker.md` | G35 | PASS | 105 | self |
| `qc_rubric.md` | G53 | PASS | 16 | self |
| `qc_solution_checklist.md` | G37 | PASS | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | self |
| `task_code_verifier.md` | G3 | VALID | 12 | self |

Every certification verdict above is SELF-ATTESTED: the same agent authored the artifact and ran its review prompt, so the kit's owner-is-not-verifier rule is not satisfied. These are recorded verdicts, never independent ones.

## Findings carried out of the review prompts

- **QC_instruction.md** B3: the third difficulty lever, `## Build plan`, is deliberately not emitted. generate_instruction SS2.1 excludes it at baseline and G43 forbids a numbered build sequence; the variant's spec_sections axis is discharged by `## Front-end specification` instead
- **QC_instruction.md** D5: the companion contradicts itself on star resolution. Section 9.1 requires a hit test 'biased toward the brighter star when two are close'; section 16.1 describes the Picker as resolving 'to the nearest star'. The brief carries the 9.1 sense, which is the one stated as a capability requirement, and the note is recorded here rather than resolved silently
- **QC_instruction.md** C7: the judge window is exceeded: core_features 9025 chars and ui_ux_notes 7502 against the 2500 slice, joined 21886 against the 9000 join. window_lint reports this and never fails it; the tail reaches the agent in full and judge_score never touches reward, so the brief was not trimmed to fit a diagnostic number
- **QC_instruction.md** D5: the companion states 'There is no account, no signup and no scrolling'. This brief seeds two accounts and closes signup. The change is deliberate and recorded in 00-decisions: content-publishing's critical focus needs an ownership boundary, and with one account that boundary collapses to 'is signed in', which a build can satisfy while getting ownership wrong. The companion's own SS24.4 states its section 20 is a contract to build to rather than a transcription
- **QC_spec.md** S1: the seven spec docs are authored outside the bundle at _spec/<code>/, because CON-5 forbids a spec/ folder inside a shipped bundle
- **generate_instruction.md** read in full before authoring: SS2 derivation, SS2.9 and SS2.10 draws, SS3 phases, SS4 section spec and the number rule, SS4.9 flags, SS5 universal rules, SS6 App Contract, SS7 voice, SS8 self-check
- **generate_instruction.md** the other five generator prompts (docker_generator, pytest_generator, rubric_author, solution_checklist, toml_generator) carry NO receipt and are reported UNCITED. They are advisory. Their artifacts were authored from the stage files and reference libraries instead, and every mechanical gate over those artifacts is green
- **qc_docker.md** CMP-004: the compose minio image is quay.io/minio/minio at the tag reference/C SS C.2.1 pins, not docker.io/minio/minio. Docker Hub refuses anonymous scoped tokens for minio/minio (the token returns access: []), so the pinned repository cannot be resolved or pulled without credentials and its digest cannot be obtained honestly. quay.io is MinIO's own registry, the tag is identical, and the digest sha256:9535594ad4122b7a78c6632788a989b96d9199b483d3bd71a5ceae73a922cdfa was read from the live manifest index. Graded Medium rather than High: same publisher, same tag, digest verified. Operator action: confirm the registry substitution or supply Docker Hub credentials and re-pin
- **qc_rubric.md** RC-02 and RC-03 fired on the first pass: C-UX-02 was claimed by R1 and R6, and C-FE-03 by R3 and R8. Split into C-UX-11 and C-FE-07 so every criterion owns one obligation
- **qc_rubric.md** RC-12 fired on the first pass: R1 asked for two figures in two palette colours and R6 for the toolbar dot carrying the last colour picked, both of which a pytest assertion could read. Both were rewritten to the judgment the brief actually needs
- **qc_solution_checklist.md** the prompt declares no numbered check registry; the machine layer is checklist_qc.py, which passes, and the adjudication found no invented obligation and no unpinned literal
- **qc_toml.md** SIGN-001 to SIGN-003 are marked deprecated in the registry itself and superseded by SIGN-004, which passes: task.toml carries no [signoff] table

## Corpus-level gates

- G42 `corpus_overlap.py` NOT-APPLICABLE: one bundle under this output root, so no cross-archetype pair was compared. Not a pass.
- G49 `diversity_lint.py` NOT-APPLICABLE: diversity needs at least two bundles.
- G61 `corpus_report.py` NOT-APPLICABLE: no admissible bundle in the ledger yet.
- G38 `kit_selftest.py` PASS over 32 checks, once per kit revision rather than per task.

## Declared but ungraded

Obligations the brief states that no channel can observe. Recorded rather than dropped or falsely cited.

- The production build against a development server: no deterministic black-box signal.
- The Angular and FastAPI stack: asserting it would read the implementation, which INV6 and G23 bar from the reward path.
- Credentials written to `/app/USER_README.md` and the reserved `.browser_screenshots` / `.downloads` directories: under `environment_mode = "separate"` the grader runs in its own container and never sees the agent's `/app`.

## Hardening pass, 16 Sept 2026

**Scorer crash fixed.** `tests/workflows.yaml` carried unquoted `cov: C-XX-NN (earned: why)` values, which are invalid YAML. The vendored `score.py` and `run_workflows.py` load that file with `yaml.safe_load`, so every trial would have scored 0.0 as `scorer_crashed`, a correct build included. Every `cov:`, `purpose:` and `do:` value is now JSON-quoted and the file parses.

**task.toml brought to the toml_generator template.** `capability_flags` is `aesthetic` alone (the Task Order declares none); `rubric_version = "1"`; `harbor_version = "0.20.0"`; `language = "python"` for the FastAPI backend; keywords in slot order; `APP_PUBLIC_URL` added to the agent env; healthcheck timings 60.0 and 60; verifier timeout 3600.0; authors in the template's two-line form. The companion is recorded in `_handoff/<code>.sources.json`. Sidecar `restart:` removed from compose (qc_docker CMP-019).

**One unfair assertion removed.** The simultaneous publish test required a `409` for the second request, but a correct build that serialises the two requests answers the second as a replay. The brief now allows either answer, and the test fires four warmed requests and requires one published row and one share token.

**Six critical traps added, each stated in the brief first:**

| Workflow | Test | Wrong default it fails |
|---|---|---|
| first_light_sky_and_catalogue | `test_signing_out_ends_that_session_alone` | a self-contained token that sign out cannot end |
| pick_resolves_the_brighter_star | `test_pick_measures_great_circle_separation_across_the_seam_and_near_a_pole` | a box prefilter in right ascension and declination |
| draw_and_persist_a_constellation | `test_simultaneous_segments_each_take_their_own_position` | highest position plus one, then insert |
| draw_and_persist_a_constellation | `test_simultaneous_undos_each_remove_a_segment_of_their_own` | delete the highest position read a moment earlier |
| invalid_segment_and_name_are_refused | `test_another_stargazer_is_refused_on_every_write_route` | owner checks on reads and segment writes only |
| private_render_denied_to_another_stargazer | `test_simultaneous_renders_each_take_a_revision_of_their_own` | number a render from a count read before writing |

`POST /api/auth/logout` was added to the API shapes, because the brief already required a signed out token to stop working and named no route for it. The suite is now 50 pytest substeps and 20 browser substeps over the same 8 workflows.

**Live runs.** A throwaway Flask stub with a correct mode and a naive mode ran against the pinned PostgreSQL and MinIO images, outside the bundle, with a connection pool. Over five runs each, correct mode passed all seven tests every time (35 of 35) and naive mode failed all seven every time (35 of 35), each for its intended reason.

## Not proven here

- Battery 3, handoff-owned: G13, G15, G18, G19, G20, G21, G25. The kit has no Docker and no harness.
- G23 implementation-agnosticism stays human-owned.
- G48's replay half is DEFERRED: there is no reference app and no known-wrong controls yet.
- No full reference application exists. The six traps added by the hardening pass and the rewritten publish race ran against a throwaway stub; the other 43 tests have not run against a real app. The pass rate is a prediction until calibration.
- The certification prompts were not re-run over the hardening pass; its checks were the full gate sweep and the live runs above.
- G59/G60 returned NOT-APPLICABLE, and that is the only reachable state: `_vocab.CODE_QUALITY_AUTHORED` now carries `code_quality`, but the vendored `recompute.py` at all three pins still refuses any dimension outside the seven product ones, so a GENERATED `tests/rubric.json` cannot carry a source criterion. Hand-adding one would fail G48's regeneration check.
- The five generator prompts other than `generate_instruction.md` carry no receipt and are UNCITED. They are advisory.

## Traceability

`tests/traceability-matrix.md` and `.csv` ship inside the bundle and are regenerated by every sweep from the G24 scan.
