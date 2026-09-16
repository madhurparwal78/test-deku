# Build report - S_conte_cont_athlete-brand-platform-vb_20260916_075118

**Rendered from `_handoff/S_conte_cont_athlete-brand-platform-vb_20260916_075118.gates.jsonl`.** Every verdict below is read out of the
receipt file that `revalidate.py` wrote; none is transcribed and none is authored here.
The receipts carry the SHA-256 of all 24 bundle files each gate examined.

## Identity

| | |
|---|---|
| Task code | `S_conte_cont_athlete-brand-platform-vb_20260916_075118` |
| Task id | `deku/athlete-brand-platform-vb` |
| uuid_v5 | `d3e9aba7-c9ba-5277-92f1-d34808a6a2a5` |
| Cell | solo_founder / content-publishing / content-publishing |
| Archetype | `athlete-brand-platform`, variant `b` |
| Variant axes | `critical_depth`, `spec_sections` (a companion document was supplied) |
| Service profile | `P4-db-storage` |
| Providers | `backend = postgres`, `storage = minio` |
| Language | typescript |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field, gates G0..G63 |
| Grader pin | `vendor/grader-0.22.0` |
| Target schema | 1.4 |
| Verifier mode | `separate` |
| Companion | `/Users/apple/Downloads/landonorris_prd.md`, 6,713 lines |

## The deterministic draws

| Axis | Value | Digest source |
|---|---|---|
| render model | `spa-json-api` | sha256(task_code)[0:8] |
| backend | Fastify | sha256(task_code)[8:16] |
| frontend | Angular | sha256(task_code)[16:24] |
| navigation | top-nav | sha256(task_code)[24:32] |
| work surface | card-grid | sha256(task_code)[32:40] |
| create flow | dedicated-route | sha256(task_code)[40:48] |
| feedback | optimistic-row | sha256(task_code)[48:56] |
| design direction | `companion` (drawn `editorial-serif`, overridden per reference/L L.6.1) | sha256(archetype) |
| launch surface | custom_404, form_validation, meta_tags, no_broken_links, privacy_page | sha256(archetype + ":launch-surface") |

## Feature resolution

| Candidate | Verdict | File | Reason |
|---|---|---|---|
| Derived public visibility (`published` plus a publication instant not in the future) | INCLUDED | instruction.md, tests/test_output.py | the PRD's section 22.1 normative rule, and the seam three graders attack |
| Authenticated photograph boundary over MinIO | INCLUDED | instruction.md, tests/test_output.py | PRD section 20.5 plus the storage slot; the only externally observable object-store fact |
| Ingestion reconciliation, idempotency and monotonic ordering | INCLUDED | instruction.md, tests/test_output.py | PRD sections 24.4 and 24.5; carried as an editor-submitted payload so it is observable |
| Double opt-in with two single-purpose tokens | INCLUDED | instruction.md, tests/test_output.py | PRD section 28.2, re-expressed without an email slot |
| Pre-publication validation blocks | INCLUDED | instruction.md, tests/test_output.py | PRD section 22.3; a refusal, never a dismissible warning |
| Opaque public identifiers | INCLUDED | instruction.md, tests/test_output.py | PRD section 20.6 enumeration resistance |
| Next-round correctness | INCLUDED | instruction.md, tests/test_output.py | PRD section 25.7, the single most load-bearing live figure |
| Real-time helmet layer with a still-frame fallback | INCLUDED, judged only | instruction.md, tests/rubric.json | PRD section 8.9 states the fallback as a contract; no pytest assertion can see a rendered frame |
| Track visualiser, scroll scrub, split heading, print sheet | INCLUDED, judged or walked | instruction.md, tests/workflows.yaml | rendered surfaces; graded by the rubric or by a browser substep |
| Email sending, broadcasts, delivery feedback | DROPPED | - | the service profile declares no email slot; confirmation travels as a token the API returns, and the brief says no email is sent |
| Search index and its ranking | DROPPED | - | no search slot; declared with a G51 waiver rather than dropped in silence |
| Outbound webhooks and event delivery | DROPPED | - | no external network at run time |
| Cache posture, stale-while-revalidate, invalidation | DROPPED | - | no cache service; the brief forbids a second backing service |
| Separate admin origin | DROPPED, re-expressed | instruction.md | one published port; the workspace is path-scoped under `/studio` and the deviation is waived on the record |

## Slot obligations

| Slot | Provider | State | Observing test |
|---|---|---|---|
| backend | `postgres` | MET | `test_seeded_photograph_objects_exist_in_the_store` (critical), plus every stored-row assertion |
| storage | `minio` | MET | `test_uploaded_photograph_lands_in_the_store_under_the_key_scheme` (critical) |

## Grading surface

| Measure | Value |
|---|---|
| Workflows | 16 |
| Browser substeps | 32 |
| Pytest substeps | 45 |
| Critical substeps | 29 |
| Non-happy-path workflow ids | 8: `confirmation_token_cannot_unsubscribe_an_address`, `invalid_enquiry_submission_is_refused`, `duplicate_slug_and_empty_alt_text_are_refused`, `non_public_story_read_is_denied_to_public_sessions`, `non_public_photograph_bytes_denied_to_public_sessions`, `lower_roles_cannot_write_to_the_catalogue`, `audience_reads_are_forbidden_below_their_rung`, `ingestion_replay_is_a_duplicate_and_a_conflict_holds_the_result` |
| Pytest category mix | business_rule 6, core_outcome 8, data_integrity 8, presentation 6, security 16, validation 1 |
| Test module emitted | one, `tests/test_output.py`, 45 test functions |
| Sections covered by that module | core features, data integrity, authorization, edge cases, plus the backend and storage slots |
| Rubric criteria | 15 (14 positive, 1 negative) |
| Checklist items | 1007 |

### Rubric dimension shares, against the frozen budget

| Dimension | Criteria | Positive points | Share | Target |
|---|---|---|---|---|
| instruction_following | 2 | 10 | 0.312 | 0.30 |
| functionality | 3 | 8 | 0.250 | 0.25 |
| ux_flow | 2 | 4 | 0.125 | 0.15 |
| ui_visual | 2 | 4 | 0.125 | 0.15 |
| motion | 2 | 2 | 0.062 | 0.05 |
| accessibility | 2 | 2 | 0.062 | 0.05 |
| responsiveness | 2 | 2 | 0.062 | 0.05 |

### Checklist by section, and by type tag

| Section | Items | | Tag | Items |
|---|---|---|---|---|
| C-CF | 181 | | capability | 18 |
| C-CN | 25 | | constraint | 75 |
| C-DC | 73 | | contract | 326 |
| C-DM | 118 | | data | 58 |
| C-FE | 319 | | literal | 141 |
| C-OV | 21 | | role | 43 |
| C-RL | 54 | | ui | 346 |
| C-TR | 85 | |  | 0 |
| C-UF | 78 | |  | 0 |
| C-UX | 53 | |  | 0 |

Channel split, as `channel_lint.py` counted it: pytest 89 citations across
45 tests, rubric 337 items across
15 criteria, and the remainder on browser substeps. No item is graded
by two channels, and none is graded by none.

## Literals ledger

189 values, every one of them carried by `instruction.md` and by at least one
grader or the brief alone.

| Class | Values |
|---|---|
| account | 4 |
| config | 11 |
| copy | 65 |
| credential | 1 |
| endpoint | 24 |
| enum | 61 |
| route | 23 |

Three values are deliberately unpinned and recorded under "Referenced but not pinned" in
`solution/checklist.md`: the grotesque family, the display serif, and the exact shades behind
the palette roles. Each is a builder choice under the A5 colour rule, and none is a
credential, a route, a status code or a threshold.

## spec/ folder, and what each document fed

| Document | Fed |
|---|---|
| `00-decisions.md` | the draws, and eleven residual judgment calls |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | not emitted into the brief: `## Build plan` is not baseline (generate_instruction.md 2.1) |

## Grading window

Reported by `window_lint.py`, never failed: the brief has no length limit (G33, reference/L L.3).

| Section | Chars | Reference |
|---|---|---|
| Core features | 7851 | 2400 |
| User flow | 3818 | 1900 |
| UI/UX notes | 3637 | 1700 |
| Constraints | 1014 | 800 |
| User roles | 1578 | 1000 |
| Overview | 1165 | 700 |
| joined | 15451 | 8800 |

Everything past the 9,000-character join slice is graded by a committed pytest assertion
rather than by the judge, which is recorded in the QC_instruction receipt under C7.

## Traceability

`tests/traceability-matrix.md` and `.csv` are emitted by every sweep from the same scan G24
makes: 0 core-ask rows. They are regenerated, never authored.

## KIT GATE LOG

| Gate | Tool | Exit | Verdict | argv sha |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | `2c46dec59ba118fd` |
| G1/G12 | `layout_lint.py` | 0 | PASS | `a164c681cb3beaaa` |
| G46 | `structure_lint.py` | 1 | FAIL | `a164c681cb3beaaa` |
| G50 | `docker_lint.py` | 0 | PASS | `a164c681cb3beaaa` |
| G55 | `runtime_deps_lint.py` | 0 | PASS | `a164c681cb3beaaa` |
| G63 | `secret_lint.py` | 0 | PASS | `a164c681cb3beaaa` |
| G48 | `truth_lint.py` | 0 | PASS | `a164c681cb3beaaa` |
| G51 | `source_lint.py` | 0 | PASS | `cc3b6762a3252ea4` |
| G52 | `rubric_context_lint.py` | 0 | PASS | `a164c681cb3beaaa` |
| G54 | `comment_lint.py` | 0 | PASS | `a164c681cb3beaaa` |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | `2c46dec59ba118fd` |
| G11 | `leak_scan.py` | 0 | PASS | `f6b224e96bacdad8` |
| G33 | `window_lint.py` | 0 | PASS | `f6b224e96bacdad8` |
| G4/G5 | `contract_lint.py` | 0 | PASS | `74b571f2c99af02d` |
| G43 | `prescription_lint.py` | 0 | PASS | `f6b224e96bacdad8` |
| G44 | `disclosure_lint.py` | 0 | PASS | `f6b224e96bacdad8` |
| G10 | `no_sdk_lint.py` | 0 | PASS | `ecfeb38363781808` |
| G31 | `determinism_lint.py` | 0 | PASS | `ecfeb38363781808` |
| G14 | `reward_path_lint.py` | 0 | PASS | `e9bed7a45f67461b` |
| G27/G30 | `rubric_lint.py` | 0 | PASS | `6f9ee95e00c7cb73` |
| G41 | `flag_lint.py` | 0 | PASS | `a164c681cb3beaaa` |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | `a164c681cb3beaaa` |
| G59/G60 | `codequality_lint.py` | 2 | ? | `a164c681cb3beaaa` |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | `bb0d5e1c1da8718c` |
| G6 | `fixture_lint.py` | 0 | PASS | `e6c2b6db6fa97340` |
| G24 | `coverage_map.py` | 0 | PASS | `f16e3273c952d474` |
| G37 | `checklist_qc.py` | 0 | PASS | `907651fc1521d997` |
| G39 | `rubric_align_lint.py` | 0 | PASS | `4b67fbc9fd84a884` |
| G28/G29 | `channel_lint.py` | 0 | PASS | `f1179f0e2e12c59c` |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | `0f34ad53aa01381f` |
| G0/INV5 | `vendor_check.py` | 0 | PASS | `5fad4adbfaf96927` |
| G47 | `output_qc.py` | 1 | FAIL | `37e94022c5783a73` |

`codequality_lint.py` exits 2 (NOT-APPLICABLE): the bundle carries no code rubric, which is
legal. `prompt_receipt_lint.py` exits 0 with WARN: every certification prompt has a current,
bundle-bound receipt, and all seven are SELF-ATTESTED, which is its own recorded state and
never a pass.

## BLOCKING FINDINGS

**G46 is RED, and so is G47 in consequence.** `structure_lint.py` reports:

> CON-1 placement: bundle is INSIDE the generation kit
> (`/Users/apple/Downloads/GreenField-GenKit2`).

This is a placement condition of the checkout, not a defect in the bundle. `structure_lint.py`
derives the generation-kit root from its own `__file__` two levels up, which resolves to the
directory that holds both `deku-green-field/` and `Output/`, so **every bundle written under
`GreenField-GenKit2/Output/` fails this check**, including the six already in this corpus.
Verified by running `structure_lint.py` against
`Output/16sept-phantom/S_conte_cont_webgl-agency-showcase-vb_20260916_065929`, which fails
identically.

The output location was set by the operator's instruction. Two things resolve it, neither of
them a change to this bundle:

1. move `Output/` to `/Users/apple/Downloads/Output/`, a sibling of the kit rather than a
   child of the directory that holds it, and re-run the sweep; or
2. set `output_root` in `deku-green-field/config/kit-config.yaml` to a path outside the kit
   tree, which `kit_config.output_root()` owns.

`G47` carries exactly one finding, that `G46` is red. No other gate is red, and the two
`_handoff` files it wanted are the ones rendered by this stage.

No spec gap and no harness gap prevented a required test.

## Adversarial review receipts

Seven certification prompts, each with a bundle-bound receipt in
`_handoff/S_conte_cont_athlete-brand-platform-vb_20260916_075118.receipts.json`:

| Prompt | Gate | Verdict | Verifier | Non-pass checks |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | self | A1 WARN, B3 WARN, C3 WARN, C7 WARN, D2 WARN |
| `QC_spec.md` | G34 | PASS | self | S10 WARN, S3 WARN, S9 WARN |
| `qc_docker.md` | G35 | PASS | self | BLD-002 NOT-APPLICABLE, BLD-004 NOT-APPLICABLE, BP-004 NOT-APPLICABLE, BP-005 NOT-APPLICABLE, DEP-011 NOT-APPLICABLE, DEP-015 NOT-APPLICABLE, DEP-017 NOT-APPLICABLE |
| `qc_rubric.md` | G53 | PASS | self | RC-01 WARN, RC-16 WARN |
| `qc_solution_checklist.md` | G37 | PASS | self | none |
| `qc_toml.md` | G36 | PASS | self | BENCH-002 NOT-APPLICABLE, BENCH-003 NOT-APPLICABLE, BENCH-005 NOT-APPLICABLE, INST-007 NOT-APPLICABLE, INT-007 NOT-APPLICABLE, SIGN-001 NOT-APPLICABLE, SIGN-002 NOT-APPLICABLE, SIGN-003 NOT-APPLICABLE, TAX-006 NOT-APPLICABLE, TAX-008 NOT-APPLICABLE |
| `task_code_verifier.md` | G3 | VALID | self | none |

The one defect these reviews found and repaired: `qc_toml.md` META-003, `task.toml` carried
the retired `openhands_version` and `calibration_date` keys. Both were removed and
`validate_task.py` re-run green. `QC_instruction.md` also drove two artifact changes: the
Definition of done was cut from 111 words to 76 (D3a), and the storage-level concurrency
invariant was added to `## Data model` (C5).

## Estimates

`turns_expected` 120, `tokens_expected` 4,500,000. The reasoning: two halves to build, a
public site of six routes and a workspace of eight, over eleven tables; one real-time
rendering layer with a fallback contract; and four seams that each need their own care, the
derived visibility rule, the authenticated object route, the ingestion reconciliation and the
double opt-in. That is the medium band rather than the hard one because the role model is
four flat roles with no tenancy, there is no payment surface and no mail to send, and the
season feed arrives as a payload rather than as a live third party.

## EXIT STATE

```
GATES-RED, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference application. Nothing counts toward corpus
targets until the app lands downstream and `harbor run -a oracle` returns `1.0` twice. The
handoff contract beside this file carries the seven gates the kit cannot run.
