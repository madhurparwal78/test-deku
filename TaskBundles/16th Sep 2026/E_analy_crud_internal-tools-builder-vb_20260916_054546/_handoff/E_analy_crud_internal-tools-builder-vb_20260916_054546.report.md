# Build report - E_analy_crud_internal-tools-builder-vb_20260916_054546

| | |
|---|---|
| Task code | `E_analy_crud_internal-tools-builder-vb_20260916_054546` |
| Task id | `deku/internal-tools-builder-vb` |
| Cell | enterprise / analytics-reporting / crud-catalog |
| Service profile | `P2-db-email` |
| Providers | `backend` = postgres, `email` = mailpit |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | typescript |
| Capability flags | `aesthetic` |
| Design direction | `companion` (a supplied PRD governs, reference/L S-L.6.1) |
| Launch surface | alt_text, favicon, meta_tags, security_headers, sitemap_robots |
| Companion document | `_handoff/E_analy_crud_internal-tools-builder-vb_20260916_054546.companion-prd.md` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Grader pin | 0.22.0 |
| Target schema | 1.4 |
| Verifier mode | separate (the kit default since 2026-09-16; the grader ships its own image from `tests/Dockerfile` on `deku-verifier-base`) |
| Exit state | MECHANICALLY-GREEN, NO-SOLUTION |

## Feature resolution

| Candidate | Verdict | Where it landed | Reason |
|---|---|---|---|
| Marketing surface: home, pillar template, blog, demo, search, not-found | INCLUDED | instruction.md `## Core features`, `## Front-end specification` | the companion's measured half; observable over served markup |
| Prompt composer with atomic source chips | INCLUDED | `## Core features` | the companion's primary funnel and its most under-built component |
| Falling-blocks game on the not-found route | INCLUDED | `## Core features` | measured in the companion and the most distinctive single surface in it |
| Sign-in, sessions, enumeration resistance | INCLUDED | `## Core features` | every graded journey passes through it |
| Resources, write-only credentials, reachability probe | INCLUDED | `## Core features` | observable at the API with no admin credential |
| Query contract with a closed outcome set | INCLUDED | `## Core features` | the product's core round trip |
| Canvas, operation log, undo across a reload | INCLUDED | `## Core features` | carries the crud-catalog critical focus |
| Components, inspector, bindings | INCLUDED | `## Core features` | the runtime the canvas produces |
| Data grid with server-side paging | INCLUDED | `## Core features` | asserted on the request rather than on the screen |
| Versions, releases, environments, approvals | INCLUDED | `## Core features` | the release boundary the companion grades hardest |
| Permission groups, deny-wins resolution, policies | INCLUDED | `## Core features` | the companion's own governing section |
| Members and invitations over real SMTP | INCLUDED | `## Core features` | the declared email slot's observable side effect |
| Append-only hash-chained audit trail | INCLUDED | `## Core features` | verifiable at the API without reading source |
| Workflow scheduler, run history, webhook receipt | DROPPED | `## Constraints` | no queue slot is declared and no scheduler is observable in one session |
| Federated identity, second factor, provisioning | DROPPED | `## Constraints` | baseline auth is app-implemented; no auth slot is declared |
| Residency regions, erasure across derived stores | DROPPED | `## Constraints` | one datastore exists, so neither is observable |
| Object store, queue, warehouse, model-provider execution | DROPPED | `## Constraints` | declarable resource kinds only; no matching slot exists |

## Slot obligations

| Slot | Provider | State | Evidence |
|---|---|---|---|
| backend | postgres | MET | `test_canvas_operations_persist_positions_sizes_and_bindings` is a critical substep and carries the `persist` vocabulary G9/G32 read |
| email | mailpit | MET | `test_invitation_email_reaches_only_the_invited_inbox` is a critical substep and asserts delivery at the mail sink |

## Grading surface

| Measure | Value |
|---|---|
| Workflows | 23 (enterprise band 13 to 23) |
| Browser substeps | 23 |
| Pytest substeps | 54 |
| Critical substeps | 16 |
| Non-happy-path ids | 11: unauthenticated_console_request_is_denied, operator_write_is_denied_at_the_api, auditor_cannot_read_an_app, removed_member_is_denied_on_the_next_action, concurrent_promotions_yield_at_most_one_release, duplicate_submission_writes_exactly_once, concurrent_saves_end_in_a_conflict_not_an_overwrite, duplicate_invitation_acceptance_is_rejected, invalid_demo_request_is_refused_with_its_values_kept, empty_state_reads_differently_from_a_refusal, referenced_resource_delete_is_rejected |
| Pytest module | `tests/test_output.py`, 54 tests |
| Sections covered | core features, data integrity, authorization, edge cases, email |
| Checklist items | 380 across 10 section codes |
| Rubric criteria | 20: 18 positive, 2 negative |

### Rubric dimension shares, against the frozen weights

| Dimension | Positive points | Share | Target |
|---|---|---|---|
| instruction_following | 12 | 0.30 | 0.30 |
| functionality | 10 | 0.25 | 0.25 |
| ux_flow | 6 | 0.15 | 0.15 |
| ui_visual | 6 | 0.15 | 0.15 |
| motion | 2 | 0.05 | 0.05 |
| accessibility | 2 | 0.05 | 0.05 |
| responsiveness | 2 | 0.05 | 0.05 |

## Literals ledger

218 pinned values. Every one appears verbatim in at least one declared carrier, and every verifier-only value appears in `task.toml` alone.

| Class | Count | Carriers seen |
|---|---|---|
| account | 6 | conftest.py, instruction.md, workflows.yaml |
| credential | 1 | conftest.py, instruction.md, workflows.yaml |
| design_phrase | 10 | instruction.md |
| endpoint | 25 | instruction.md, test_output.py |
| env_var | 9 | instruction.md, task.toml |
| motion_moment | 7 | instruction.md |
| number | 6 | conftest.py, instruction.md, task.toml, test_output.py |
| route | 18 | instruction.md, test_output.py, workflows.yaml |
| scheme | 46 | conftest.py, instruction.md, test_output.py, workflows.yaml |
| seed_record | 30 | conftest.py, instruction.md, test_output.py, workflows.yaml |
| status | 60 | conftest.py, instruction.md, task.toml, test_output.py, workflows.yaml |

## spec/ documents emitted

| Document | Fed |
|---|---|
| `00-decisions.md` | the draws, the taxonomy substitutions, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at baseline |

## Generated answer-key files

Rendered by the vendored `solution/trinity/recompute.py` at generator revision `truth-generator-7` and re-run byte-identically under G48: `solution/TRUTH.md`, `solution/USER_README.md` (restored 2026-09-16: the harness greps the corpus canary by that filename), `solution/trinity/rubrics.json`, `solution/trinity/test_ans.py` and `tests/rubric.json`. None is hand-edited.

## Grading window measurement

Reported, never failed: the brief carries no length limit (G33).

| Section | Characters | Reference |
|---|---|---|
| Core features | 36314 | 2400 |
| User flow | 5583 | 1900 |
| UI/UX notes | 6859 | 1700 |
| Constraints | 2414 | 800 |
| User roles | 2792 | 1000 |
| Overview | 1824 | 700 |
| joined six | 55786 | 8800 |

The judge slices each section at 2,500 characters and the join at 9,000. `## Core features` runs far past that slice and the join does too. Nothing was trimmed: the tail reaches the agent in full, the criteria the judge grades against are self-contained, and `judge_score` never touches reward, so cutting a graded rule to fit the window would trade reward for a diagnostic number.

## Kit gate log

Rendered from `E_analy_crud_internal-tools-builder-vb_20260916_054546.gates.jsonl`. Every row is a tool exit code and a verdict string over the bytes whose SHA-256 the receipt carries. No verdict on this page was written by hand.

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
| G59/G60 | `codequality_lint.py` | 2 | NOT-APPLICABLE |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 0 | PASS |

`G59/G60` returns NOT-APPLICABLE: the bundle ships the product half of `tests/rubric.json` alone. The vendored `recompute.py` renders `judged_criteria` only, so a source criterion could not be generated and a hand-appended one is a G48 failure by construction. This is the legal state stage-3.6 names, recorded rather than passed silently.

## Prompt receipts

| Gate | Prompt | Verdict | Checks answered | Verifier |
|---|---|---|---|---|
| G3 | `task_code_verifier.md` | VALID | 12 | self |
| G34 | `QC_spec.md` | PASS | 15 | self |
| G34 | `QC_instruction.md` | PASS | 24 | self |
| G35 | `qc_docker.md` | PASS | 105 | self |
| G36 | `qc_toml.md` | PASS | 120 | self |
| G37 | `qc_solution_checklist.md` | PASS | 0 | self |
| G53 | `qc_rubric.md` | PASS | 16 | self |

Every certification prompt was run by the same agent that authored the artifact, so each verdict is recorded as SELF-ATTESTED. The kit's rule is owner is not verifier; these are recorded verdicts, never independent ones, and G23, G34, G35, G36 and G37 layer two remain open for a human reviewer.

### Findings carried on the receipts

**G34 `QC_spec.md`**

- B1: the crud-catalog row names the db slot alone. This bundle also declares the email slot, which is legal for the E+crud cell as profile P2-db-email and is recorded as a deliberate call in spec/00-decisions.md; the invitation is a real side effect no database assertion can observe.

**G34 `QC_instruction.md`**

- B1: the pattern row is honoured for the db slot; the added email slot is the recorded P2-db-email deviation described in spec/00-decisions.md.
- B3: two of the three difficulty levers are emitted. `## Build plan` is absent by the baseline rule, and `## Front-end specification` carries the third body of detail instead.
- C7: `## Core features` runs far past the 2500-character judge slice and the joined six run past 9000. Reported, never trimmed: the brief has no length limit and cutting a graded rule to fit the window would lose reward to buy a diagnostic number.

**G35 `qc_docker.md`**

- DEP-011: the pinned grader package rule is scoped to `[verifier].environment_mode = "shared"`. This bundle emits the kit default `separate`, so the grader ships its own image built from tests/Dockerfile on deku-verifier-base. The packages stay installed in the agent image anyway, at the grader-0.22.0 pins, so a later switch back to shared mode costs nothing.
- ARCH-002: the base image is pinned by explicit version tag rather than by digest, which reference/C C.4 prefers because an official tag is a multi-architecture manifest list. No digest is present to judge.
- ARCH-003: no image digest appears in either environment file.
- BP-004: no build-time download carries a source-provided checksum; every artifact comes from apt, pip or npm with its own signature chain.
- BP-005: a single stage is correct here. The final image must carry Node, Python and Chromium, so no build-only toolchain could be dropped from it.
- DEP-015: `language` is typescript, so the go/rust/java multi-stage rule does not apply, and the file carries no `--break-system-packages` and no pip fallback.
- DEP-016: no compiled-language build stage exists.
- DEP-017: `language` is not java.
- SEC-003: no source or reference convention establishes non-root execution for the agent image; the harness runs the agent as root by convention.
- SEC-005: no secret-bearing variable is set by ENV; every credential reaches the container from task.toml at run time.
- ENV-003: the App Contract forbids persistent volumes, so no VOLUME is required and none is present.
- ENV-004: no ENTRYPOINT is present, which is correct: CMD carries the long-lived process.
- CMP-018: no sidecar persists provider state, so no named volume is required.
- CMP-011: superseded by CMP-022. The `main` service publishes 4173 because C12 requires it; no sidecar publishes a host port.
- CMP-020: superseded by CMP-022. `main` carries extra_hosts and ports as well as depends_on, which C12 makes mandatory.

**G36 `qc_toml.md`**

- SCHEMA-011: the file carries a `[delivery]` block, which the canonical template in toml_generator.md section 11 does not show. CON-2 and stage-4-task-toml.md require it on every new bundle and validate_task.py checks it, so the higher authority wins and the block stays.
- BENCH-002: this is not a trivial or smoke task, so the Trivial resource tier does not apply; the Standard tier holds exactly.
- SIGN-001: retired 2026-09-15 with the `[signoff]` table.
- SIGN-002: retired 2026-09-15 with the `[signoff]` table.
- SIGN-003: retired 2026-09-15 with the `[signoff]` table.
- TAX-006: `language` is typescript, so the `any` rule does not apply.
- INST-007: instruction.md is present, so the spec folder is not treated as the brief.
- VERIF-007: neither payments nor storage is declared, so no shared provider credential is required in the verifier environment.

## Blocking findings

None mechanical. Three states are recorded rather than resolved:

- the advisory code-quality channel is absent, for the vendored-generator reason recorded above;
- 36 companion items and topics are carried under an explicit `--waive`, all of them raw value rows (hex ladders, easing tokens, gradient and keyframe declarations, a font fallback stack, placeholder tokens) or authoring-register sections. The colour half of G51 independently proves 88 of 88 source colours reached the brief as family, tone and shade;
- no reference application exists, so G13, G15, G18 to G21 and G25 are undecided and the replay half of G48 is deferred.

## Budget

`turns_expected` 200 and `tokens_expected` 7,000,000. The brief is a companion-backed variant `b` carrying two deployable surfaces, four roles, 380 checklist obligations and 54 graded assertions, which sits at the top of the enterprise band rather than the middle of it.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`. Not admissible. Nothing counts toward corpus targets until the application is built downstream from `solution/checklist.md` and an oracle run returns 1.0 twice.
