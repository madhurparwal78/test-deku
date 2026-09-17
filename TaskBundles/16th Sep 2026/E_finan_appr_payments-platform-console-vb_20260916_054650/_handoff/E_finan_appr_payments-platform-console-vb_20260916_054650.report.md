# Build report - E_finan_appr_payments-platform-console-vb_20260916_054650

Rendered from `_handoff/E_finan_appr_payments-platform-console-vb_20260916_054650.gates.jsonl`.
No verdict in this file is transcribed; every one is read from a receipt.

## Identity

| | |
|---|---|
| Task code | `E_finan_appr_payments-platform-console-vb_20260916_054650` |
| Task id | `deku/payments-platform-console-vb` |
| Cell | enterprise / finance-accounting / approval-workflow |
| Archetype | `payments-platform-console` |
| Variant | `b` (companion supplied, per stage-1-derive.md) |
| Variant axes | `critical_depth`, `spec_sections` |
| Service profile | `P3-db-auth` |
| Providers | `backend = postgres`, `auth = keycloak` |
| Language | `typescript` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit version | deku-green-field, this working copy |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Companion source | `stripe_prd.md`, 6,973 lines |
| Verifier mode | `separate` (the kit default since commit 11eaf7b; `tests/Dockerfile` ships the grader image on `deku-verifier-base:0.22.0`) |

## The input, and the one mapping it needed

The Task Order named `pattern: admin-console`, which is not a member of the fifteen-pattern
enum `task_code.py codes` prints. It was mapped to `approval-workflow`: the Task Order's own
idea names "approve a refund that moves money out of the account balance", which is exactly
that pattern's critical focus, and `approval-workflow` is legal only in `enterprise`, which
the Task Order also declares. `admin-console` is carried as the product's shape, not as a
taxonomy key. Recorded in `_spec/<code>/00-decisions.md`.

## Derived-design draws

Identity for every draw is the archetype `payments-platform-console` (reference/L L.4,
reference/O O.3).

| Axis | Value |
|---|---|
| `render_model` | `spa-json-api` |
| `backend` | Hono |
| `frontend` | SolidJS + Vite |
| `nav` | `sidebar-nav` |
| `work_surface` | split detail-pane |
| `create_flow` | dedicated-route |
| `feedback` | inline-banner |
| `design_direction` | `companion` (the draw returns `dense-ops-console`; reference/L L.6.1 hands the axis to the companion and the draw is recorded, not applied) |
| `launch_surface` | `custom_404`, `favicon`, `sitemap_robots`, `social_preview`, `spam_protection` |

Every drawn axis is visible in the brief: the refund composer sits at its own address
(`dedicated-route`), the payments and approvals routes are a list beside a detail pane
(`split detail-pane`), the console is a left rail under a fixed bar (`sidebar-nav`), and
every confirmation and refusal is an inline banner in the region that produced it
(`inline-banner`).

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| India storefront: home, three product routes, two content indexes, pricing, privacy, lead form | INCLUDED | Core features, User flow | The Task Order names marketing routes, guides, stories and rupee pricing |
| Availability gate on the analytics product | INCLUDED | Core features 60 | Companion section 10.4; the highest-value storefront rule |
| Sign-in, account chooser, two environments | INCLUDED | Core features 1-9 | Companion 14-15; the Task Order names scoped roles across sandbox and live |
| Payments, double-entry ledger, balances, payouts | INCLUDED | Core features 10-34 | Companion 18; the Task Order names payouts |
| Refund ceiling, refund request, approval, expiry | INCLUDED | Core features 14-27 | The pattern's critical focus and the companion's section 1.5 workflow |
| Disputes | INCLUDED | Core features 35-37 | The Task Order names disputes |
| API credentials, webhook endpoints, events | INCLUDED | Core features 38-45 | The Task Order names webhook endpoints and API keys |
| Hash-chained audit log | INCLUDED | Core features 46-50 | Companion 25; the enterprise tier's evidence obligation |
| Lead form with decoy and dedup | INCLUDED | Core features 69-72 | Companion 9.7, plus the drawn `spam_protection` |
| Not-found page, favicon, sitemap, robots, social preview | INCLUDED | Core features 73, Technical requirements | The four remaining drawn launch surfaces |
| Careers route and application form | DROPPED | WAIVED at G51 | The Task Order's idea names marketing, guides, stories, pricing and the console, not hiring |
| Subscriptions, invoices, usage meters, dunning | DROPPED | Constraints | Out of the Task Order's idea; carried as an explicit scope-out in the companion's own vocabulary |
| Query workspace, reports, exports | DROPPED | Constraints | Same |
| Connected accounts and platform money flows | DROPPED | Constraints | Same |
| Federated identity, provisioning, break-glass | DROPPED | Constraints | No second identity provider at baseline |
| Notifications, email, outbound webhook delivery | DROPPED | Constraints | No `email` slot is declared by `P3-db-auth` |
| Onboarding and verification data capture | DROPPED | Constraints | Accounts are seeded already verified or restricted |
| Risk scoring and rule authoring | DROPPED | Constraints | The fraud product route describes the product; it does not operate it |
| Build order (companion 38) | DROPPED | WAIVED at G51 | A build order is a work order; `## Build plan` is not emitted at baseline |
| Evidence-gap and acceptance tables (companion 41, 42) | DROPPED | WAIVED at G51 | Provenance of the companion's own measurement, not a product requirement |

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| `db` | `postgres` | MET | `test_refund_within_ceiling_is_persisted` (critical), `test_seeded_northbeam_balance_row_is_stored`, `test_balance_row_equals_sum_of_ledger_entries` |
| `auth` | `keycloak` | MET | `test_login_returns_bearer_token` (critical), `test_support_cannot_approve_request_denied` (critical), `test_cross_account_payment_read_denied` (critical) |

## Grading layer

| | |
|---|---|
| Workflows | 21 (band 6-23) |
| Browser substeps | 27 |
| pytest substeps | 56 |
| Critical substeps | 16 |
| Test module | one, `tests/test_output.py`, 56 functions |
| Sections covered | core features, data integrity, authorization, edge cases, presentation |
| Non-happy-path ids | `support_cannot_approve_request_denied`, `requester_self_approval_forbidden`, `administrator_cannot_create_refund_denied`, `cross_account_read_denied`, `unauthenticated_console_read_denied`, `duplicate_approval_at_most_one_refund`, `concurrent_approvals_resolve_to_one_refund`, `duplicate_refund_key_is_a_no_op`, `expired_request_cannot_be_approved`, `invalid_refund_amounts_are_refused`, `empty_states_and_the_gated_product` |
| Checklist items | 190 across ten section codes |
| Coverage | two-way, G24 green; every `cov:` tag earned |

### Rubric

| | |
|---|---|
| Criteria | 18 |
| Positive / negative | 16 / 2 |
| Positive score total | 42 |
| Type mix | 12 task completion, 4 instruction following, 2 commission (66.7 percent task completion, band 60-80) |

| Dimension | Criteria | Share of positive score | Target |
|---|---|---|---|
| `instruction_following` | 3 | 0.310 | 0.30 |
| `functionality` | 3 | 0.262 | 0.25 |
| `ux_flow` | 2 | 0.143 | 0.15 |
| `ui_visual` | 2 | 0.143 | 0.15 |
| `motion` | 2 | 0.048 | 0.05 |
| `accessibility` | 2 | 0.048 | 0.05 |
| `responsiveness` | 2 | 0.048 | 0.05 |

The three small dimensions are earnable because `## UI/UX notes` states a motion character,
an accessibility floor and a responsive contract that a judge can decide against.

## Literals ledger

151 pinned values plus two verifier-only entries, in
`_handoff/<code>.literals-ledger.json`.

| Class | Count |
|---|---|
| `credential` | 1 |
| `account` | 4 |
| `seed_record` | 33 |
| `status` | 40 |
| `number` | 29 |
| `scheme` | 15 |
| `route` | 14 |
| `endpoint` | 5 |
| `env_var` | 10 (8 agent-visible, 2 verifier-only) |

Verifier-only, absent from `instruction.md` and from `[environment].env` (INV4):
`DB_ADMIN_URL`, `AUTH_ADMIN_TOKEN`.

## spec/ folder

Written to `Output/16-sep-2026/_spec/<code>/`, never inside the bundle (CON-5).

| Document | Fed |
|---|---|
| `00-decisions.md` | the draws, the R1 judgment calls, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | authoring-side only; `## Build plan` is not emitted at baseline |

## Companion carriage (G51)

| Measure | Result |
|---|---|
| Source colours described in the brief by family and tone | 40 / 40 |
| Source topics carried | 317 / 317 (6 waived) |
| Source enumerated items carried | 1,836 / 1,836 (7 waived) |

Waivers, all recorded in the G51 receipt: the companion's own document-meta sections
(normative-versus-informational, the build order, the evidence-gap and acceptance
tables), the careers demographic row, four colour-notation rows whose content is a
gradient or media-query value the brief may not carry, one asset-manifest filename row,
and five data-model rows whose content words are underscored identifiers the gate's item
normalisation collapses while the brief spells them with the underscore.

## Grading-window measurement

| Section | Chars | Reference | Flag |
|---|---|---|---|
| `core_features` | 26,472 | 2,400 | past-slice |
| `user_flow` | 6,542 | 1,900 | past-slice |
| `ui_ux_notes` | 10,007 | 1,700 | past-slice |
| `constraints` | 4,800 | 800 | past-slice |
| `user_roles` | 2,665 | 1,000 | past-slice |
| `overview` | 2,400 | 700 | past-slice |
| joined | 52,886 | 8,800 | past-slice |

This is reported, never failed: `window_lint.py` measures length and fails nothing on it,
and the brief has no cap. The cause is deliberate. A 6,973-line companion had to reach the
agent in full (G51, CON-6), and the brief is the only file the agent ever sees. What the
slice costs is the judge's context, not reward: the judged criteria are self-contained per
reference/I I.8 and carry their own facts, `judge_score` never touches reward, and every
graded rule past the cut is graded by pytest or by a browser substep. Recorded here so the
trade is visible rather than discovered.

## Kit gate log

Read from the receipts file. Both signals recorded: exit code and verdict string.

| Gate | Tool | Exit | Verdict | stdout SHA |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | `ad11bcdfd48b0035` |
| `G1/G12` | `layout_lint.py` | 0 | PASS | `36e4b0118a4ad4cd` |
| `G46` | `structure_lint.py` | 0 | PASS | `cfb7ff2e2f4025d4` |
| `G50` | `docker_lint.py` | 0 | PASS | `380ed7d1c830de35` |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | `a0c21dca8bc5f78a` |
| `G63` | `secret_lint.py` | 0 | PASS | `e912b42bb5ca8206` |
| `G48` | `truth_lint.py` | 0 | PASS | `2e2828b9eb813a33` |
| `G51` | `source_lint.py` | 0 | PASS | `7269dccdda4c1ef5` |
| `G52` | `rubric_context_lint.py` | 0 | PASS | `a7207b31daddaf7e` |
| `G54` | `comment_lint.py` | 0 | PASS | `95a70bf330de4154` |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | `00aa458a3e25d0cc` |
| `G11` | `leak_scan.py` | 0 | PASS | `cab9d6a1574f41e7` |
| `G33` | `window_lint.py` | 0 | PASS | `0f5b85733a1d8cc9` |
| `G4/G5` | `contract_lint.py` | 0 | PASS | `5a9551532a387f76` |
| `G43` | `prescription_lint.py` | 0 | PASS | `5ef4b5f9a3aff47d` |
| `G44` | `disclosure_lint.py` | 0 | PASS | `8766a042e7ed2a37` |
| `G10` | `no_sdk_lint.py` | 0 | PASS | `f350349f036cf217` |
| `G31` | `determinism_lint.py` | 0 | PASS | `ecfc3d18e84a787d` |
| `G14` | `reward_path_lint.py` | 0 | PASS | `53bac13e217061a9` |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | `2c4bae0135d881f2` |
| `G41` | `flag_lint.py` | 0 | PASS | `16b233db1afb78f6` |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | `cdf20c83e9056866` |
| `G59/G60` | `codequality_lint.py` | 2 | NOT-APPLICABLE | `e23941dd85e0253b` |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | `68a37075d8b5358b` |
| `G6` | `fixture_lint.py` | 0 | PASS | `f999f39a1f34539e` |
| `G24` | `coverage_map.py` | 0 | PASS | `844418e5a94b0911` |
| `G37` | `checklist_qc.py` | 0 | PASS | `09a48c22ebbff3ea` |
| `G39` | `rubric_align_lint.py` | 0 | PASS | `90296329e8c052a4` |
| `G28/G29` | `channel_lint.py` | 0 | PASS | `9b377922a07907bd` |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | `e6a25b03734f1932` |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | `9691ea0bb8e6a7f8` |
| `G47` | `output_qc.py` | 0 | PASS | `f625764a7ec0b07e` |

`G0`'s ledger-claim half is deliberately excluded from the re-run: the archetype was
claimed at S1 by this run, so re-running it would produce a guaranteed false FAIL. Its
vendor half is re-run above and is idempotent.

`G38` (`kit_selftest.py`) is per kit revision rather than per task: PASS, 32 checks.

The kit moved under this build while it ran. Three commits landed between the first and
the final sweep and the bundle was re-synced to each: `da24d3b` renamed the section pytest
module to `tests/test_output.py` and the generated compiled-rubric file to
`solution/trinity/test_ans.py`; `78e5ba6` re-pinned `tests/test.sh`, which was re-vendored;
`806eb0a` restored `solution/USER_README.md` as a GENERATED file, which
`solution/trinity/recompute.py` now writes from the same `grounding.yaml` as the rest of
the answer key. `11eaf7b` moved the emitted `[verifier].environment_mode` to `separate`,
which this bundle now carries. Every one of those is reflected in the bytes the final
receipts hash.

`G40` is WARN rather than PASS for one reason, recorded in its own receipt: every
certification prompt was run by the same agent that authored the artifact, so all seven
verdicts are SELF-ATTESTED. The kit's rule is owner != verifier. Four advisory generator
prompts carry no receipt and are reported as UNCITED, which the gate treats as a note.

## Prompt receipts (G40, the certification half)

| Prompt | Gate | Verdict | Checks answered | Non-PASS |
|---|---|---|---|---|
| `task_code_verifier.md` | G3 | VALID | 12 / 12 | none |
| `QC_spec.md` | G34 | PASS | 15 / 15 | S2, S5, S6 WARN |
| `QC_instruction.md` | G34 | PASS | 24 / 24 | A1, A8, B3, C5, C7 WARN |
| `qc_toml.md` | G36 | PASS | 120 / 120 | SCHEMA-011, ENV-007 WARN |
| `qc_docker.md` | G35 | PASS | 105 / 105 | CMP-011 WARN |
| `qc_solution_checklist.md` | G37 | PASS | registry empty | none |
| `qc_rubric.md` | G53 | PASS | 16 / 16 | RC-01 WARN |

Every WARN carries a finding naming the check and the reason in the receipts file. Nine of
the twelve are one shape: a QC row written before a later kit decision superseded it (the
A5 number rule, the INV9 mechanism ban, `## Build plan` leaving the baseline, the auth-slot
env vars, the reference/J J.9 TTL seam, the CON-2 `[delivery]` block, the C12 `main`
ports rule). Each records which document now owns the rule. The remaining three are real
observations: the grading-window slice (C7), the ten-feature PRD under a companion (S2),
and the split of judgment-class obligations across the rubric and the browser channel
(RC-01).

## Blocking findings

None. The one recorded deviation is the omitted `[delivery.images]` table, which
`validate_task.py` treats as optional and which cannot be filled honestly without a
network; see the handoff contract.

## Budget

| | |
|---|---|
| `turns_expected` | 180 |
| `tokens_expected` | 6,500,000 |

Reasoning: two surfaces in one deployment, fifteen tables with a double-entry ledger, a
three-role authorization layer with per-resource ceilings, a two-environment storage
dimension, an approval workflow with idempotency and a contended single-winner transition,
a hash-chained audit log, and a storefront carrying a measured design system with
scroll-driven demonstrations. That is materially more surface than the corpus median, so the
budget sits above the medium band and below the expert ceiling. `difficulty` stays the empty
placeholder: it is written by calibration, never by the author.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the reference app is built
downstream and `harbor run -a oracle` returns `1.0` twice.
