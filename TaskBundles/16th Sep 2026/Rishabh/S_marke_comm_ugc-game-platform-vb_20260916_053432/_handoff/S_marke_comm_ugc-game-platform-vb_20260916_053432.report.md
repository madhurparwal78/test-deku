# Build report - S_marke_comm_ugc-game-platform-vb_20260916_053432

## Identity

| | |
|---|---|
| Task code | `S_marke_comm_ugc-game-platform-vb_20260916_053432` |
| Task id | `deku/ugc-game-platform-vb` |
| Cell | solo_founder / marketplace / commerce-checkout |
| Service profile | `P5-db-pay-email` |
| Providers | `backend = postgres`, `email = mailpit`, `payments = killbill` |
| Variant | `b`, axes `critical_depth` + `spec_sections` |
| Language | typescript |
| Design direction | `companion` (drawn `dense-ops-console`, recorded and overridden per reference/L S-L.6.1) |
| Launch surface | `colour_contrast, custom_404, no_frontend_secrets, security_headers, sitemap_robots` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Grader pin | 0.22.0 |
| Target schema | 1.4 |
| Verifier mode | `separate` |
| Answer-key generator | `truth-generator-7` (writes `solution/USER_README.md` and `solution/trinity/test_ans.py`) |
| Companion document | `roblox_prd.md`, 2,890 lines, recorded in `_handoff/S_marke_comm_ugc-game-platform-vb_20260916_053432.sources.json` |

## Derivation draws

Every draw is SHA-256 over the archetype `ugc-game-platform`, recorded as `draw:` lines in
`Output/_spec/S_marke_comm_ugc-game-platform-vb_20260916_053432/00-decisions.md`.

| Axis | Value |
|---|---|
| render_model | `ssr-islands` |
| backend | Fastify |
| frontend | Remix (React Router 7) |
| nav | `top-nav` |
| work_surface | `split detail-pane` |
| create_flow | `dedicated-route` |
| feedback | `toast` |
| design_direction | `companion` (drawn `dense-ops-console`) |
| launch_surface | `colour_contrast, custom_404, no_frontend_secrets, security_headers, sitemap_robots` |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Age-gated signup, derived age band | INCLUDED | `## Core features`, `## Data model` | companion S-16; date of birth stored, band derived at read time |
| Four authentication routes | INCLUDED | `## Core features` | companion S-9.2, S-16.1 I5 |
| Kredz ledger, derived balances | INCLUDED | `## Core features`, `## Data model` | companion S-17; the pattern's own money surface |
| Kredz pack purchase through Kill Bill | INCLUDED | `## Core features` | the `commerce-checkout` critical focus (reference/B B.1) |
| Receipt mail through Mailpit | INCLUDED | `## Core features` | the `email` slot of `P5-db-pay-email` |
| Marketplace split, rounding, rate version | INCLUDED | `## Core features` | companion S-18 |
| Creator payouts, six conditions | INCLUDED | `## Core features` | companion S-18.4 |
| Publishing pipeline, ten states | INCLUDED | `## Core features` | companion S-19 |
| Derived preview imagery, four states | INCLUDED | `## Core features` | companion S-19.4 |
| Scoped search, cursor paging, age filter | INCLUDED | `## Core features` | companion S-5.3, S-20 |
| Join reservations, presence lease | INCLUDED | `## Core features` | companion S-21, carried as HTTP only |
| Safety, enforcement, appeals | INCLUDED | `## Core features` | companion S-22 |
| Telemetry, localisation, flags, experiments | INCLUDED | `## Core features` | companion S-12, S-13, S-14 |
| Design system, motion, three colour modes | INCLUDED | `## UI/UX notes`, `## Front-end specification` | companion S-3, S-6, S-7 |
| Kavora Studio desktop tool | DROPPED | `## Constraints` | named by the companion, out of scope for a web build |
| Separate creator application origin | DROPPED | `## Constraints` | the App Contract allows one container |
| Independent per-service deployments | REFRAMED | `## Technical requirements` | carried as route prefixes with their own readiness |
| Third-party bot defence, error sink, analytics | REFRAMED | `## Core features`, `## Constraints` | first-party gate that fails closed; no run-time outbound calls |
| Object storage for uploads | DROPPED | `## Core features` | `storage` is not a declared slot; payload carries a declared type inline |
| Real settlement rails | DROPPED | `## Constraints` | a payout settles to a recorded request |
| Numbered build order | WAIVED | - | INV9: a build sequence is the one thing the brief may not carry |

## Slot obligations

| Slot | Provider | Critical substep | Observing test | State |
|---|---|---|---|---|
| backend | postgres | yes | `test_balance_is_derived_from_stored_ledger_rows` | MET |
| email | mailpit | yes | `test_pack_receipt_email_reaches_the_buyer` | MET |
| payments | killbill | yes | `test_kredz_pack_purchase_creates_one_invoice_for_the_price` | MET |

No UNMET slot.

## Grading surface

| | |
|---|---|
| Workflows | 16 (solo_founder band 10-16) |
| Browser substeps | 43 |
| pytest substeps | 71 |
| Critical substeps | 5 |
| Non-happy-path ids | `signup_with_invalid_input_is_rejected`, `duplicate_pack_submit_charges_once`, `age_restricted_purchase_is_denied`, `concurrent_contention_on_a_scarce_resource`, `player_cannot_reach_creator_routes` |
| pytest modules | one, `tests/test_output.py`, 71 tests |
| Sections covered | core features, data integrity, authorization, edge cases, email, payments |
| Checklist items | 220, every one cited by exactly one channel |
| Rubric criteria | 14 (12 positive, 2 negative) |

### Rubric dimension shares (positive scores only)

| Dimension | Points | Share | Target | Within 0.10 |
|---|---|---|---|---|
| `instruction_following` | 11 | 0.289 | 0.30 | yes |
| `functionality` | 8 | 0.211 | 0.25 | yes |
| `ux_flow` | 6 | 0.158 | 0.15 | yes |
| `ui_visual` | 4 | 0.105 | 0.15 | yes |
| `motion` | 3 | 0.079 | 0.05 | yes |
| `accessibility` | 3 | 0.079 | 0.05 | yes |
| `responsiveness` | 3 | 0.079 | 0.05 | yes |

## Literals ledger

207 pinned values, at `_handoff/S_marke_comm_ugc-game-platform-vb_20260916_053432.literals-ledger.json`.

| Class | Count |
|---|---|
| `account` | 5 |
| `credential` | 1 |
| `design_phrase` | 11 |
| `endpoint` | 33 |
| `env_var` | 14 |
| `motion_moment` | 8 |
| `number` | 21 |
| `route` | 15 |
| `scheme` | 17 |
| `seed_record` | 16 |
| `status` | 66 |

Two values are `verifier_only` and appear in `[verifier].env` alone: `DB_ADMIN_URL`,
`EMAIL_INBOX_API_URL`.

## Authoring documents

| Document | Fed |
|---|---|
| `00-decisions.md` | the draws, the Task Order mapping, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements`, the graded API surface |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing; `## Build plan` is not emitted at baseline |

They live at `Output/_spec/S_marke_comm_ugc-game-platform-vb_20260916_053432/` and never ship inside the bundle (CON-5).

## Grading window

`window_lint.py` reports, never fails. `run_rubric.py` slices one section at 2,500 characters
and the join at 9,000.

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Core features | 29,899 | 2,400 | past-slice |
| User flow | 4,132 | 1,900 | past-slice |
| UI/UX notes | 14,034 | 1,700 | past-slice |
| Constraints | 1,235 | 800 | over-reference |
| User roles | 2,274 | 1,000 | over-reference |
| Overview | 1,581 | 700 | over-reference |

The brief is 78,103 bytes. The companion carries 549 enumerated obligations and G51 requires
every one of them to reach the brief, so the sections run long by construction. Content past
the slice reaches the agent in full and stops reaching the judge; `judge_score` never touches
reward. No rule was cut to fit.

## Kit gate log

Rendered from `_handoff/S_marke_comm_ugc-game-platform-vb_20260916_053432.gates.jsonl`. Never transcribed by hand.

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

`G59/G60` returns NOT-APPLICABLE: the bundle ships no `evaluation_target: "source"` criterion,
which is a legal state (stage-3.6-overlays.md). `G42`, `G49` and `G61` are corpus-level and are
recorded under "Corpus-level gates" below.

## Prompt receipts (G40)

Rendered from `_handoff/S_marke_comm_ugc-game-platform-vb_20260916_053432.receipts.json`.

| Gate | Prompt | Verdict | Checks answered | Verifier |
|---|---|---|---|---|
| G3 | `task_code_verifier.md` | VALID | 12 | self |
| G34 | `QC_instruction.md` | PASS | 24 | self |
| G34 | `QC_spec.md` | PASS | 15 | self |
| G35 | `qc_docker.md` | PASS | 105 | self |
| G36 | `qc_toml.md` | PASS | 120 | self |
| G37 | `qc_solution_checklist.md` | PASS | 0 | self |
| G53 | `qc_rubric.md` | PASS | 16 | self |
| S2 | `generate_instruction.md` | PASS | 0 | self |
| S3 | `solution_checklist.md` | PASS | 0 | self |
| S4 | `toml_generator.md` | PASS | 0 | self |
| S5 | `docker_generator.md` | PASS | 0 | self |
| S7 | `pytest_generator.md` | PASS | 0 | self |
| S8 | `rubric_author.md` | PASS | 0 | self |

Every certification prompt was run by the same agent that authored the artifact, so each verdict
is **SELF-ATTESTED** rather than independent: the kit's rule is owner != verifier and this run had
one agent. Seven checks carry a non-PASS verdict and each names its finding in the receipt.

## Corpus-level gates

| Gate | Tool | Result |
|---|---|---|
| G38 | `kit_selftest.py` | PASS, 32 checks |
| G42 | `corpus_overlap.py` | NOT-APPLICABLE: no cell holds two distinct archetypes across the four bundles in the output root |
| G49 | `diversity_lint.py` | PASS in WARN mode; its one finding names two other bundles, not this one |
| G61 | `corpus_report.py` | NOT-APPLICABLE: no ADMISSIBLE bundle exists yet, so the 0/10/30/40/20 mix has nothing to measure |

## Blocking findings

None that stop the handoff. Three recorded deviations, each justified in the receipts:

1. **`PAYMENTS_ADMIN_USER` / `PAYMENTS_ADMIN_PASSWORD` are not in `[environment].env`.**
   `reference/C` C.2 lists them as agent variables for the payments slot, and
   `secret_hygiene_lint.py` (G17) fails any `_ADMIN_` key placed there. The gate is mechanical
   and blocking, the reference is prose, so the gate wins: both values reach the agent container
   through the compose `main` service's `environment` block and both sit in `[verifier].env`, so
   the agent and the verifier share one Kill Bill tenant. **Raise with the kit owner**: G17 and
   reference/C disagree, and every payments task will hit it.
2. **`[delivery.images]` is omitted.** `validate_task.lint_delivery` requires each image value to
   be a `@sha256:` digest present in `environment/`, while `reference/C` C.4 forbids pinning by
   digest because a single-architecture child digest breaks the dual-arch build. The block is
   optional, so it is left out rather than satisfied wrongly.
3. **`G63 SEC-3` WARN stands.** `PAYMENTS_ADMIN_PASSWORD` is Kill Bill's built-in `password`.
   The kit does not choose it and cannot change it without mounting a custom shiro.ini; the
   durable fix is word-boundary-aware scrubbing in the harness.

## Budget

`turns_expected = 200`, `tokens_expected = 8000000`. The reasoning: thirteen feature areas, one
of them a ledger with contention and idempotency obligations, a second a billing integration
against a real external service, and a design system carried from a 2,890-line companion. That
is the top of the documented band, and the band's ceiling is 8,000,000 tokens.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference application. Nothing counts toward corpus
targets until the app lands downstream and `harbor run -a oracle` returns `1.0` twice.
