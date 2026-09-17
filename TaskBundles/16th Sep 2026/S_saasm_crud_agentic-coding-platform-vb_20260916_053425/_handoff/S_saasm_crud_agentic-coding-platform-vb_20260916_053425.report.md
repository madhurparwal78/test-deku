# Build report - S_saasm_crud_agentic-coding-platform-vb_20260916_053425

Rendered from `_handoff/S_saasm_crud_agentic-coding-platform-vb_20260916_053425.gates.jsonl` and `_handoff/S_saasm_crud_agentic-coding-platform-vb_20260916_053425.receipts.json`.
No verdict on this page was typed by hand.

## Identity

| | |
|---|---|
| task code | `S_saasm_crud_agentic-coding-platform-vb_20260916_053425` |
| task id | `deku/agentic-coding-platform-vb` |
| cell | solo_founder / saas-micro-tools / crud-catalog |
| archetype | `agentic-coding-platform` |
| variant | `b`, on the `critical_depth` and `spec_sections` axes |
| service profile | `P5-db-pay-email` |
| providers | backend `postgres`, email `mailpit`, payments `killbill` |
| language | python |
| spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 |
| kit | deku-green-field |
| vendored grader | 0.22.0 |
| target schema | 1.4 |
| companion | `cursor_prd.md`, 8211 lines, recorded in `_handoff/S_saasm_crud_agentic-coding-platform-vb_20260916_053425.sources.json` |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Marketing chrome, footer and the public route family | INCLUDED | instruction.md ## Core features | the companion's own route table, minus the three out-of-scope prefixes |
| Model registry, benchmark plot and leaderboard | INCLUDED | ## Core features | one dataset with three consumers is the companion's sharpest correctness requirement |
| Value calculator | INCLUDED | ## Core features | client-only, integer minor units, a worked example that pins the arithmetic |
| Marketplace catalogue, filters, detail and install | INCLUDED | ## Core features | the Task Order names it, and the tie-break is a real defect class |
| Download and platform resolution | INCLUDED | ## Core features | a pure function over seeded artifact rows, cheap to grade |
| Accounts, workspaces, seats and the invitation | INCLUDED | ## Core features | the Task Order's journey ends here |
| Plans, tiers, checkout into killbill | INCLUDED | ## Core features | the plan ladder is the commercial spine |
| Usage, allowance, overage and the spend limit | INCLUDED | ## Core features | usage-based overage is named in the Task Order idea |
| The five drawn launch-surface obligations | INCLUDED | ## Core features, ## Technical requirements, ## UI/UX notes | reference/O draw over the archetype |
| Agent execution platform and the run list | DROPPED | spec/00-decisions.md | no run surface on the Task Order's journey; waived at G51 |
| Hosted code product | DROPPED | spec/00-decisions.md | out of scope; waived at G51 |
| Integration, trigger and webhook registry | DROPPED | spec/00-decisions.md | out of scope; waived at G51 |
| Marketplace publishing and moderation | DROPPED | spec/00-decisions.md | the catalogue is built, the pipeline is not |
| Documentation site and help centre | DROPPED | spec/00-decisions.md | separate front ends; waived at G51 |
| Blog, careers, community, students, workshops, brand, future | DROPPED | spec/00-decisions.md | no commercial function on the journey |
| Single sign-on and directory synchronisation | DROPPED | ## Constraints | no identity provider exists in this environment |
| Invoice and purchase-order billing | DROPPED | ## Constraints | no receivables surface in the payment platform here |
| Refunds, payment methods, chargebacks | DROPPED | ## Constraints | reference/K K.4 does not expose them |

## Slot obligations

| Slot | Provider | State | Critical substep |
|---|---|---|---|
| backend | postgres | MET | `test_model_registry_seed_rows_are_persisted` |
| email | mailpit | MET | `test_invitation_email_reaches_only_the_invited_address` |
| payments | killbill | MET | `test_checkout_creates_the_billing_account_in_the_payment_platform` |

## Grading layer

| | |
|---|---|
| workflows | 16 |
| browser substeps | 75 |
| pytest substeps | 49 |
| critical substeps | 10 |
| non-happy-path ids | `calculator_invalid_allocation_is_refused`, `duplicate_install_creates_no_second_installation`, `duplicate_checkout_creates_no_second_billing_account`, `member_cannot_invite_a_colleague`, `cross_workspace_usage_is_denied`, `anonymous_account_request_is_unauthenticated`, `duplicate_usage_key_creates_no_second_event`, `usage_past_the_spend_limit_is_refused`, `empty_route_renders_the_custom_not_found_page` |
| pytest module | `tests/test_output.py`, one module, 49 test functions |
| concerns covered | core features, authorization, data integrity, payments, email, edge cases |
| checklist items | 315 across ten section codes |
| traceability | `tests/traceability-matrix.md` and `.csv`, 166 core asks, 186 graders, 0 not fully graded |

## Rubric

| | |
|---|---|
| criteria | 15 |
| positive / negative | 12 / 3 |
| compiled weight share, reference rubric | 0.870, floor 0.60 |

| Dimension | Share | Target | Within 0.10 |
|---|---|---|---|
| instruction_following | 0.295 | 0.30 | yes |
| functionality | 0.227 | 0.25 | yes |
| ux_flow | 0.136 | 0.15 | yes |
| ui_visual | 0.136 | 0.15 | yes |
| motion | 0.068 | 0.05 | yes |
| accessibility | 0.068 | 0.05 | yes |
| responsiveness | 0.068 | 0.05 | yes |

## Literals ledger

| Class | Count | Examples |
|---|---|---|
| account | 3 | `owner@example.com`, `member@example.com`, `owner2@example.com` |
| credential | 1 | `deku-demo-pw-2026` |
| design_phrase | 10 | `paper lifted a hair`, `fades to about three-quarters strength`, `runs off the trailing edge inside a clipped container`, `one ink mixed into the ground` |
| endpoint | 25 | `/api/health`, `/api/auth/signup`, `/api/auth/signin`, `/api/me` |
| env_var | 14 | `DATABASE_URL`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` |
| motion_moment | 5 | `a spinner that turns`, `a pulse that breathes to half strength`, `a bar of light sweeping across a loading row`, `a tile that pops in` |
| number | 92 | `2000`, `20000`, `6000`, `60000` |
| route | 32 | `/product`, `/cloud`, `/cli`, `/fixbot` |
| scheme | 6 | `marlin-ws-<workspace-slug>`, `marlin-ws-aurora-data`, `marlin-ws-northlight`, `marlin-user-<user-id>` |
| seed_record | 148 | `Devan Ashworth`, `Priya Raghunathan`, `Marguerite Sandoval`, `meridian-4-max` |
| status | 38 | `active`, `past_due`, `canceled`, `invited` |

Two entries are `verifier_only` and appear in `task.toml` `[verifier].env` alone: `PAYMENTS_ADMIN_USER`, `PAYMENTS_ADMIN_PASSWORD`, `DB_ADMIN_URL`, `EMAIL_INBOX_API_URL`.

## spec/ documents and what each fed

| Document | Fed |
|---|---|
| `00-decisions.md` | every residual call, the eight draw lines, the companion carry table |
| `01-PRD.md` | ## Overview, ## Core features, ## Constraints |
| `02-TRD.md` | ## Technical requirements |
| `03-app-flow.md` | ## User flow |
| `04-uiux-brief.md` | ## UI/UX notes, ## Front-end specification |
| `05-backend-schema.md` | ## Data model, ## User roles |
| `06-implementation-plan.md` | nothing: ## Build plan is not emitted at baseline |

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Core features | 42135 | 2400 | past-slice |
| User flow | 4547 | 1900 | past-slice |
| UI/UX notes | 12761 | 1700 | past-slice |
| Constraints | 1415 | 800 | over-reference |
| User roles | 1899 | 1000 | over-reference |
| Overview | 2315 | 700 | over-reference |
| joined | 65072 | 8800 | past-slice |

Length is measured, never failed: `window_lint.py` (G33) caps nothing, the judged criteria are self-contained and carry their own `evaluation_rule`, and `judge_score` never touches reward. The companion's route set cannot be stated inside the slice without deleting requirements.

## Kit gate log

Rendered from the receipts. `argv_sha` and `stdout_sha` bind each row to the execution that produced it.

| Gate | Tool | Exit | Verdict | argv_sha | stdout_sha |
|---|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | `6ba7de1182de9003` | `836e3270a226fe89` |
| G1/G12 | `layout_lint.py` | 0 | PASS | `b9a4e5af2114499b` | `3c78b3db8290b22b` |
| G46 | `structure_lint.py` | 0 | PASS | `b9a4e5af2114499b` | `a0e14140c05a354a` |
| G50 | `docker_lint.py` | 0 | PASS | `b9a4e5af2114499b` | `380ed7d1c830de35` |
| G55 | `runtime_deps_lint.py` | 0 | PASS | `b9a4e5af2114499b` | `a0c21dca8bc5f78a` |
| G63 | `secret_lint.py` | 0 | PASS | `b9a4e5af2114499b` | `b0c7279b3fe36443` |
| G48 | `truth_lint.py` | 0 | PASS | `b9a4e5af2114499b` | `956fe824981c3b27` |
| G51 | `source_lint.py` | 0 | PASS | `4867263b29c79f62` | `0049239a7e62ee43` |
| G52 | `rubric_context_lint.py` | 0 | PASS | `b9a4e5af2114499b` | `f9ee85a062d828a9` |
| G54 | `comment_lint.py` | 0 | PASS | `b9a4e5af2114499b` | `90ee5dc20877c199` |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | `6ba7de1182de9003` | `0e132190a74d2abf` |
| G11 | `leak_scan.py` | 0 | PASS | `fac65ddf63f9011a` | `84ea40d2bc89f1d8` |
| G33 | `window_lint.py` | 0 | PASS | `fac65ddf63f9011a` | `e51da3bb01b59cbb` |
| G4/G5 | `contract_lint.py` | 0 | PASS | `f1fc2f3d5889f7b9` | `8f32381bf37e1398` |
| G43 | `prescription_lint.py` | 0 | PASS | `fac65ddf63f9011a` | `014b33e5c95a24f5` |
| G44 | `disclosure_lint.py` | 0 | PASS | `fac65ddf63f9011a` | `b3879651ccbab0a2` |
| G10 | `no_sdk_lint.py` | 0 | PASS | `f82e419846e99d0f` | `4c71304fc74c79f1` |
| G31 | `determinism_lint.py` | 0 | PASS | `f82e419846e99d0f` | `6c299ffebcac92a9` |
| G14 | `reward_path_lint.py` | 0 | PASS | `739513f75c7f4578` | `35cdbe97ee3a60ba` |
| G27/G30 | `rubric_lint.py` | 0 | PASS | `fa2dc51d11b20183` | `11b0afc0941db8e7` |
| G41 | `flag_lint.py` | 0 | PASS | `b9a4e5af2114499b` | `9bcb64e5e9eace72` |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | `b9a4e5af2114499b` | `cdf20c83e9056866` |
| G59/G60 | `codequality_lint.py` | 2 | ? | `b9a4e5af2114499b` | `e23941dd85e0253b` |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | `f4edc0363f45c4ff` | `8c825c6e57843b24` |
| G6 | `fixture_lint.py` | 0 | PASS | `4e03a2bd11898d5f` | `74f9b1756a627b84` |
| G24 | `coverage_map.py` | 0 | PASS | `3387f780887786ca` | `e17f4cf7323e51a7` |
| G37 | `checklist_qc.py` | 0 | PASS | `810a049ffc0aae12` | `2d116108d6300729` |
| G39 | `rubric_align_lint.py` | 0 | PASS | `0690e796d846023f` | `a2c199794c5be629` |
| G28/G29 | `channel_lint.py` | 0 | PASS | `c12bf0ba81be52d0` | `251d7dc5379e92c8` |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | `c62622958b477905` | `89501b07e5f3eb66` |
| G0/INV5 | `vendor_check.py` | 0 | PASS | `bd0354c0521def68` | `183837d1235356c8` |
| G47 | `output_qc.py` | 0 | PASS | `ed7769861fa07ba3` | `69fbe6543c10395e` |

## Prompt receipts

| Prompt | Gate | Verdict | Verifier | Checks answered |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | self | 24 |
| `QC_spec.md` | G34 | PASS | self | 15 |
| `docker_generator.md` | S5 | PASS | self | 0 |
| `generate_instruction.md` | S2 | PASS | self | 0 |
| `pytest_generator.md` | S7 | PASS | self | 0 |
| `qc_docker.md` | G35 | PASS | self | 105 |
| `qc_rubric.md` | G53 | PASS | self | 16 |
| `qc_solution_checklist.md` | G37 | PASS | self | 0 |
| `qc_toml.md` | G36 | PASS | self | 120 |
| `rubric_author.md` | S8 | PASS | self | 0 |
| `solution_checklist.md` | S3 | PASS | self | 0 |
| `task_code_verifier.md` | G3 | VALID | self | 12 |
| `toml_generator.md` | S4 | PASS | self | 0 |

Every certification receipt is SELF-ATTESTED: one agent authored and reviewed. The kit's rule is owner is not verifier, so these are recorded verdicts, never independent ones.

## Handoff gates, undecided here

| Gate | Command | Expected |
|---|---|---|
| G13 | `docker build -f environment/Dockerfile .` | exit 0 on linux/amd64 and linux/arm64 |
| G13 | `docker build -f tests/Dockerfile .` | exit 0 |
| G15 | `docker compose up, scrubbed env` | every sidecar healthy |
| G19 | `harbor run -p <task> -a oracle` | reward == 1.0 |
| G19 | `harbor run -p <task> -a oracle` | reward == 1.0, flakiness check |
| G18 | `read deployed from either oracle run` | deployed == 1.0 |
| G20 | `harbor run -p <task> -a nop` | reward == 0.0; above 0 is a P0 |
| G21 | `apply the fake-integration patch, re-run oracle` | reward < 1.0 |
| G25 | `reviewer exploit sweep, reference library F` | 0 of 11 succeed |

## Blocking findings

None. Every declared slot resolves to an image in reference/C C.2.1, every declared slot earns a critical pytest substep, and no requirement was dropped for want of an observable.

Two standing notes, neither blocking:

- G63 SEC-3 WARN: the payment platform's built-in credential is the literal word `password`. The kit does not choose it and cannot change it without mounting a custom shiro configuration into a service that boots for minutes. The durable fix is word-boundary-aware scrubbing in the harness.
- G40 SELF-ATTESTED on all seven certification prompts.

## Budget

`turns_expected = 180`, `tokens_expected = 7000000`. The companion carries thirty-three routes, a fifteen-model registry, a seventeen-entry catalogue, a twenty-three-row artifact matrix and a seven-tier plan ladder, plus an account surface with seats, invitations over real mail and a metered allowance. That is above the standard band because a companion-backed task at variant `b` carries far more graded surface than a five-line Task Order.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference app. Nothing counts toward corpus targets until the app lands downstream and `harbor run -a oracle` returns `1.0` twice.

