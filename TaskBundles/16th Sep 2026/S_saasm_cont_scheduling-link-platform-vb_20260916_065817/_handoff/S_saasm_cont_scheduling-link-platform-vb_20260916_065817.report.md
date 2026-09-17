# Build report - S_saasm_cont_scheduling-link-platform-vb_20260916_065817

| | |
|---|---|
| Task code | `S_saasm_cont_scheduling-link-platform-vb_20260916_065817` |
| Task id | `deku/scheduling-link-platform-vb` |
| Cell | solo_founder / saas-micro-tools / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | backend `postgres`, storage `minio` |
| Variant | `b`, axes `critical_depth`, `spec_sections` (companion-backed, `config/corpus-targets.yaml` `companion_variant`) |
| Language | typescript |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Companion | `Prds/cal.com_prd.md`, 1,883 lines |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Derivation draws

All eight are SHA-256 draws over the archetype `scheduling-link-platform`
(reference/L S-L.4 identity), never Python's builtin `hash()`.

| Axis | Value |
|---|---|
| render_model | `ssr-islands` |
| backend | Fastify |
| frontend | SvelteKit |
| nav | `top-nav` |
| work_surface | `split detail-pane` |
| create_flow | `multi-step-wizard` |
| feedback | `optimistic-row` |
| design_direction | `companion` (reference/L S-L.6.1: a companion beats the draw; the bank draw was `brutalist-utility` and is recorded, not applied) |
| launch_surface | `alt_text, mobile_viewport, no_broken_links, page_view_log, social_preview` (reference/O S-O.3) |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Fifteen public routes from one content model | INCLUDED | Core features, User flow | companion S-2.1, the product's whole surface |
| Home page, twelve bands in order | INCLUDED | Core features | companion S-7, normative band order |
| The other marketing routes, teams to docs | INCLUDED | Core features | companion S-8 to S-13 |
| Global chrome, header, dropdowns, footer | INCLUDED | Core features, Front-end specification | companion S-5 |
| Three-step page composer, split studio | INCLUDED | Core features, User flow | the `multi-step-wizard` and `split detail-pane` draws |
| Draft and published visibility boundary | INCLUDED | Core features | the pattern's critical focus (reference/B: object in store, protected content not publicly readable) |
| Media in the object store under a pinned key scheme | INCLUDED | Core features | the `storage` slot |
| Trial signup creating a booking page | INCLUDED | Core features | Task Order idea, closing clause |
| Page-view log and per-route totals | INCLUDED | Core features | drawn `page_view_log` |
| Internal links resolve | INCLUDED | Core features | drawn `no_broken_links` |
| Social preview per public route | INCLUDED | Technical requirements | drawn `social_preview` |
| Alternative text, narrow-viewport behaviour | INCLUDED | UI/UX notes | drawn `alt_text`, `mobile_viewport` |
| Scheduling application, companion S-14 to S-22 | DROPPED | Constraints | out of the Task Order's scope; the public pages promise it, this build does not implement it |
| Real telephony behind the voice page | DROPPED | Constraints | companion S-9 states it as marketing surface |
| Payments, email, background jobs | DROPPED | Constraints | no `payments`, `email` or `queue` slot is declared |
| Build order and difficulty map, companion S-28 | DROPPED | (waived) | a build order is a work order, not a specification (INV9) |
| Acceptance checklist, companion S-32 | DROPPED | (waived) | it restates S-3 to S-27 as a grading list; carrying it puts the exam in the brief (INV10) |
| Evidence gaps, companion S-31 | DROPPED | (waived) | authoring provenance about the capture, not a product obligation |

## Slot obligations

| Slot | Provider | Status | Evidence |
|---|---|---|---|
| backend | postgres | MET | `test_new_page_row_is_stored_as_draft` (critical), `test_seed_is_present_and_survives_a_reload`, plus every SiteStore assertion over the capability adapter |
| storage | minio | MET | `test_upload_lands_in_the_bucket_under_the_key_scheme` (critical, asserts the object exists in the bucket), `test_draft_media_object_is_refused_without_author_session` (critical) |

## Graders

| | |
|---|---|
| Workflows | 16 (solo_founder band 10-16) |
| Browser substeps | 37 |
| Pytest substeps | 53 |
| Critical substeps | 9 |
| Pytest module | one, `tests/test_output.py`, 53 test functions |
| Sections covered | core features, data integrity, authorization, edge cases, storage |
| Non-happy-path ids | `draft_page_is_denied_to_an_anonymous_visitor`, `draft_media_cannot_be_read_without_an_author_session`, `reader_publish_attempt_is_rejected`, `duplicate_upload_of_one_image_creates_one_object`, `signup_with_an_invalid_username_is_refused`, `concurrent_publish_leaves_at_most_one_winner`, `unauthenticated_caller_is_denied_at_the_interface` |

## Rubric

16 criteria: 13 positive, 3 negative (commission). Positive score total 37.

| Dimension | Share | Target |
|---|---|---|
| instruction_following | 0.324 | 0.30 |
| functionality | 0.270 | 0.25 |
| ux_flow | 0.162 | 0.15 |
| ui_visual | 0.162 | 0.15 |
| motion | 0.027 | 0.05 |
| accessibility | 0.027 | 0.05 |
| responsiveness | 0.027 | 0.05 |

Generated from `solution/trinity/grounding.yaml` by the vendored `recompute.py`;
never hand-edited. `judge_score` remains advisory and never drives reward.

## Literals ledger

53 entries, in `_handoff/S_saasm_cont_scheduling-link-platform-vb_20260916_065817.literals-ledger.json`.

| Class | Count |
|---|---|
| account | 2 |
| credential | 1 |
| env_var | 8 (one verifier-only: `DB_ADMIN_URL`) |
| endpoint | 10 |
| status | 4 |
| route | 7 |
| scheme | 2 |
| number | 1 |
| seed_record | 5 |
| motion_moment | 6 |
| design_phrase | 7 |

The last two classes are the companion-only classes: they carry the design and
motion commitments the source states in words, so a paraphrase of them is a G6
failure rather than a silent loss.

## Coverage

`solution/checklist.md` holds 124 items across ten section codes. G24 joins them
both ways against 53 pytest tests (through the pytest-provenance sidecar), 37
browser substeps (through `cov:` tags) and 16 rubric criteria (through the
rubric-provenance sidecar). Every item is cited; every citation resolves.
`tests/traceability-matrix.md` and `.csv` are regenerated from that same scan on
every sweep.

Channel split reported by G28/G29: pytest 78 items, browser 42, rubric 26, with
22 items legitimately shared by pytest and browser.

## Companion carriage (G51)

| | |
|---|---|
| Colours described by family and tone | 38 / 38 |
| Topics carried | 68 / 68 |
| Enumerated items carried | 373 / 373 |

19 waivers, all naming the signed-in scheduling application, the build-order and
difficulty tables, the acceptance checklist or the evidence-gaps appendix. Each is
recorded in the G51 receipt and in `_spec/.../00-decisions.md`'s carry table.

## Grading window

| Section | Chars | Reference |
|---|---|---|
| Core features | 18,250 | 2,400 |
| User flow | 3,043 | 1,900 |
| UI/UX notes | 7,015 | 1,700 |
| Constraints | 1,000 | 800 |
| User roles | 1,320 | 1,000 |
| Overview | 1,417 | 700 |
| Joined | 32,045 | 8,800 |

Reported, not repaired. `window_lint.py` fails nothing on length and
`generate_instruction.md` S-4 settles the question: the brief has no limit, the
tail reaches the agent in full, and cutting a real rule to fit a diagnostic
window trades reward-driving completeness for a judge's excerpt. A 1,883-line
companion is the input that makes this task worth building.

## Kit gate log

Rendered from `_handoff/S_saasm_cont_scheduling-link-platform-vb_20260916_065817.gates.jsonl`.
32 receipts, each carrying the SHA-256 of every file it read.

| Gate | Tool | Verdict | Exit |
|---|---|---|---|
| G2/G16 | validate_task.py | PASS | 0 |
| G1/G12 | layout_lint.py | PASS | 0 |
| G46 | structure_lint.py | PASS | 0 |
| G50 | docker_lint.py | PASS | 0 |
| G55 | runtime_deps_lint.py | PASS | 0 |
| G63 | secret_lint.py | PASS | 0 |
| G48 | truth_lint.py | PASS | 0 |
| G51 | source_lint.py | PASS | 0 |
| G52 | rubric_context_lint.py | PASS | 0 |
| G54 | comment_lint.py | PASS | 0 |
| G17 | secret_hygiene_lint.py | PASS | 0 |
| G11 | leak_scan.py | PASS | 0 |
| G33 | window_lint.py | PASS | 0 |
| G4/G5 | contract_lint.py | PASS | 0 |
| G43 | prescription_lint.py | PASS | 0 |
| G44 | disclosure_lint.py | PASS | 0 |
| G10 | no_sdk_lint.py | PASS | 0 |
| G31 | determinism_lint.py | PASS | 0 |
| G14 | reward_path_lint.py | PASS | 0 |
| G27/G30 | rubric_lint.py | PASS | 0 |
| G41 | flag_lint.py | PASS | 0 |
| G56/G57/G58 | if_lint.py | PASS | 0 |
| G59/G60 | codequality_lint.py | NOT-APPLICABLE | 2 |
| G7/G8/G9/G32/G45 | workflow_lint.py | PASS | 0 |
| G6 | fixture_lint.py | PASS | 0 |
| G24 | coverage_map.py | PASS | 0 |
| G37 | checklist_qc.py | PASS | 0 |
| G39 | rubric_align_lint.py | PASS | 0 |
| G28/G29 | channel_lint.py | PASS | 0 |
| G40 | prompt_receipt_lint.py | WARN | 0 |
| G0/INV5 | vendor_check.py | PASS | 0 |
| G47 | output_qc.py | PASS | 0 |
| G38 | kit_selftest.py | PASS (32 checks) | 0 |

G40 is WARN, not PASS, and the reason is recorded rather than smoothed over: every
certification prompt carries a current, bundle-bound receipt with the full scorecard
its own registry declares, but `verifier: self` throughout. This run had one agent,
so owner and verifier are the same party. That is a recorded verdict, never an
independent one.

## Prompt-gate scorecards (G40)

| Prompt | Gate | Verdict | Checks answered | Non-PASS |
|---|---|---|---|---|
| `task_code_verifier.md` | G3 | VALID | 12 | none |
| `QC_spec.md` | G34 | PASS | 15 | none |
| `QC_instruction.md` | G34 | PASS | 24 | A1, B3, C3, C5, C7 WARN |
| `qc_toml.md` | G36 | PASS | 120 | SCHEMA-011, SCHEMA-013 WARN; 9 NOT-APPLICABLE; TAX-008 SKIP |
| `qc_docker.md` | G35 | PASS | 105 | 11 NOT-APPLICABLE |
| `qc_rubric.md` | G53 | PASS | 16 | RC-12 WARN |
| `qc_solution_checklist.md` | G37 | PASS | (no registry) | none |

Every WARN names a place where an older QC prompt disagrees with a later settled
rule, and in each case the settled rule was followed and the deviation written down.
The full finding text is in `_handoff/S_saasm_cont_scheduling-link-platform-vb_20260916_065817.receipts.json`.

## Blocking findings

None. Two decisions are recorded rather than repaired:

1. **`[delivery.images]` is omitted.** `validate_task.py` only checks the block when
   it is present, and it demands `@sha256:` digest pins. reference/C C.4 forbids
   pinning by a single-architecture child digest and forbids inventing one. The
   operator fills it at packaging time from the digests the build resolves.
2. **`## Build plan` is not emitted.** `generate_instruction.md` S-2.1 removes it
   from the baseline; `spec_sections_given` records the omission, and
   `_spec/.../06-implementation-plan.md` keeps the phasing author-side.

## Budget estimate

`turns_expected = 170`, `tokens_expected = 7000000`, the `hard` band. The reasoning:
fifteen public routes rendered from a content model, a 1,883-line companion whose
copy deck must be reproduced, a three-step authoring surface, an object store with a
pinned key scheme, and a visibility boundary that has to hold at the interface and at
the store. That is more surface than a medium task and less machinery than an expert
one; the single expert-shaped rule is the publish race, which is one invariant rather
than an engine.

## Versions

| | |
|---|---|
| Kit | deku-green-field, this checkout |
| Vendored grader | 0.22.0 |
| Target schema | 1.4 |
| Rubric version | 1 |
| Judge pin | claude-sonnet-4-6 |
| Canary | present in `solution/TRUTH.md` only, rendered from `grounding.yaml` |

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the reference app is
built downstream from `solution/checklist.md` and `harbor run -a oracle` returns
`1.0` twice.

## Alignment to kit 806eb0a

The kit was pulled forward five commits, `b3d0577..806eb0a`, on 2026-09-16. This bundle was
migrated to the new contract and re-swept; the gate log below is rendered from that sweep and
supersedes any earlier gate table in this file.

| Commit | What it changed | What this bundle now carries |
|---|---|---|
| `1b99060` | adds `code_quality` as an authored code-quality rubric dimension | nothing required; the rubric carries no source criterion, so G59/G60 stay NOT-APPLICABLE |
| `da24d3b` | the section pytest module is renamed `test_output.py`; the generated compiled-rubric file becomes `test_ans.py` | `tests/test_output.py`, `solution/trinity/test_ans.py`; every `workflows.yaml` substep, the `tests/Dockerfile` COPY line, the pytest-provenance `module` and the literals-ledger carriers follow |
| `11eaf7b` | the kit emits `[verifier].environment_mode = "separate"` | `environment_mode = "separate"` in `task.toml` |
| `78e5ba6` | the vendored `tests/test.sh` is stripped of comments and re-pinned | the 90-line `test.sh`, byte-identical to the new pin (G0/INV5) |
| `806eb0a` | `solution/USER_README.md` returns as a GENERATED file carrying the seeded literals and the canary | `solution/USER_README.md`, rendered by the re-vendored `recompute.py` |

**One deliberate choice.** The agent image still installs the grader runtime (the pinned Python
packages, Chromium's libraries and the browser). Under `separate` it is not owed, and G55 RD-1 no
longer checks it. It was kept because commit `11eaf7b` itself records that nothing in the kit or
the vendored grader can verify an orchestrator honours `separate`; if one ran this bundle shared,
an image without those packages would score every trial zero. qc_docker DEP-004 and HAL-005 treat
the set as justified, so keeping it costs image size only.

**Receipts.** The certification prompt `qc_toml.md` changed in one row, VERIF-001, which now
requires `separate`; its receipt was re-bound and VERIF-001 re-adjudicated PASS against the new
`task.toml`. The advisory generator receipts whose prompts changed only by the module rename or the
mode line were re-bound with a finding saying so.

**Companion carriage.** `instruction.md` is byte-identical to the previous green sweep, so G51 is
unchanged. The source and the 21 waiver tokens are now recorded in
`S_saasm_cont_scheduling-link-platform-vb_20260916_065817.sources.json` and `S_saasm_cont_scheduling-link-platform-vb_20260916_065817.g51-waivers.json`, so a later sweep needs no one's
shell history.

Sweep result: ALL GATES GREEN.

| Gate | Tool | Verdict | Exit | stdout SHA |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | PASS | 0 | `8a7492baa51c471e` |
| `G1/G12` | `layout_lint.py` | PASS | 0 | `6f0ac604d5711d4c` |
| `G46` | `structure_lint.py` | PASS | 0 | `10f62ec57d64c7f0` |
| `G50` | `docker_lint.py` | PASS | 0 | `380ed7d1c830de35` |
| `G55` | `runtime_deps_lint.py` | PASS | 0 | `a0c21dca8bc5f78a` |
| `G63` | `secret_lint.py` | PASS | 0 | `7abe10c8aa1e593d` |
| `G48` | `truth_lint.py` | PASS | 0 | `5412094e7180bd89` |
| `G51` | `source_lint.py` | PASS | 0 | `cb3b749e5f00a4e5` |
| `G52` | `rubric_context_lint.py` | PASS | 0 | `52986bb59d4e8d1c` |
| `G54` | `comment_lint.py` | PASS | 0 | `e5a1c2d9d989d610` |
| `G17` | `secret_hygiene_lint.py` | PASS | 0 | `96ffc72b48c0766d` |
| `G11` | `leak_scan.py` | PASS | 0 | `3c56147eb29f446b` |
| `G33` | `window_lint.py` | PASS | 0 | `51b608206bcac3d8` |
| `G4/G5` | `contract_lint.py` | PASS | 0 | `f90e93dc9c4f1be7` |
| `G43` | `prescription_lint.py` | PASS | 0 | `9de65a529ed53113` |
| `G44` | `disclosure_lint.py` | PASS | 0 | `4c10b0518757c1d6` |
| `G10` | `no_sdk_lint.py` | PASS | 0 | `064b8451c1697b92` |
| `G31` | `determinism_lint.py` | PASS | 0 | `9468247fbe7a81e0` |
| `G14` | `reward_path_lint.py` | PASS | 0 | `7fb760068874347e` |
| `G27/G30` | `rubric_lint.py` | PASS | 0 | `e28d97c9df5e00e3` |
| `G41` | `flag_lint.py` | PASS | 0 | `8e45950d0eaa6895` |
| `G56/G57/G58` | `if_lint.py` | PASS | 0 | `cdf20c83e9056866` |
| `G59/G60` | `codequality_lint.py` | NOT-APPLICABLE | 2 | `e23941dd85e0253b` |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | PASS | 0 | `a69c81baea584759` |
| `G6` | `fixture_lint.py` | PASS | 0 | `97aab989d2be5b19` |
| `G24` | `coverage_map.py` | PASS | 0 | `3fdf69ce76c239fb` |
| `G37` | `checklist_qc.py` | PASS | 0 | `4ff7dd098b958dc0` |
| `G39` | `rubric_align_lint.py` | PASS | 0 | `d086871e5a9797e5` |
| `G28/G29` | `channel_lint.py` | PASS | 0 | `ea5a318ade245bf0` |
| `G40` | `prompt_receipt_lint.py` | WARN | 0 | `60ea7c5b5db51ae6` |
| `G0/INV5` | `vendor_check.py` | PASS | 0 | `8cb8ad9b2f80c926` |
| `G47` | `output_qc.py` | PASS | 0 | `5c2feeaeb06a9a06` |
