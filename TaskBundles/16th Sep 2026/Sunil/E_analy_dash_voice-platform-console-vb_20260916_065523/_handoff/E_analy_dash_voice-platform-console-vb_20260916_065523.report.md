# Build report - E_analy_dash_voice-platform-console-vb_20260916_065523

Rendered from `_handoff/E_analy_dash_voice-platform-console-vb_20260916_065523.gates.jsonl` and the sidecars beside it.
No verdict on this page was typed by hand.

## Identity

| Field | Value |
|---|---|
| Task code | `E_analy_dash_voice-platform-console-vb_20260916_065523` |
| Task id | `deku/voice-platform-console-vb` |
| Cell | enterprise / analytics-reporting / dashboard-analytics |
| Service profile | `P1-db` |
| Providers per slot | `backend` = `postgres` |
| Variant | `b` on axes ['critical_depth', 'data_shape'] |
| Language | `javascript` |
| Design direction | `companion` |
| Launch surface | `custom_404,no_broken_links,security_headers,single_cta,terms_page` |
| spec_sections_given | ['overview', 'roles', 'features', 'flow', 'uiux', 'frontend', 'techrequirements', 'datamodel', 'constraints', 'contract'] |
| Shard | 1 of 1 (single-task run) |
| Kit | deku-green-field, grader pin `0.22.0`, schema `1.4` |
| uuid_v5 | `39034532-ca4b-5a6a-9354-4f77b4e35bff` |
| Verifier mode | `separate` |
| Pytest module | `tests/test_output.py` |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Sign in and the authenticated shell | INCLUDED | instruction.md `## Core features` | closed signup, seeded accounts, bearer tokens |
| Organisation and project switchers | INCLUDED | instruction.md `## Core features` | the switch-reset trap is the companion's own H6 |
| Projects with archival | INCLUDED | instruction.md `## Core features` | archival preserves billable history |
| Scoped credentials | INCLUDED | instruction.md `## Core features` | the Task Order names the first production credential |
| Playground recognition and synthesis | INCLUDED | instruction.md `## Core features` | the Task Order names accuracy and latency |
| Metering intake | INCLUDED | instruction.md `## Core features` | what makes an issued credential do work |
| Usage and reconciliation | INCLUDED | instruction.md `## Core features` | the pattern's critical focus |
| Billing, balance and invoices | INCLUDED | instruction.md `## Core features` | usage is attributed to invoices per the idea |
| Roles, deny overrides, audit | INCLUDED | instruction.md `## Core features` | roles differ per project per the idea |
| Launch surface (terms, not-found, links, headers, one primary action) | INCLUDED | instruction.md `## Core features` / `## Technical requirements` / `## UI/UX notes` | reference/O draw |
| Marketing site, 28 public routes | DROPPED | instruction.md `## Constraints` | a separate product surface the Task Order does not name |
| Request-serving plane, audio socket | DROPPED | instruction.md `## Constraints` | no realtime slot in P1-db; unbuildable in this environment |
| Microphone capture | DROPPED | instruction.md `## Constraints` | no capture device in a headless container |
| Object storage for audio | DROPPED | instruction.md `## Constraints` | no storage slot; the console holds no audio |
| Federated identity, SCIM | DROPPED | instruction.md `## Constraints` | no auth slot |
| Real payment provider | DROPPED | instruction.md `## Constraints` | no payments slot |
| Mail, invitations, notifications | DROPPED | instruction.md `## Constraints` | no email slot |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_playground_recognition_meters_exactly_one_row`, `test_repeat_idempotency_key_writes_no_second_row` and `test_daily_rollup_recomputes_from_rows` each read rows through the capability fixture; G32 green in the sweep |

No UNMET slot obligation.

## Grading layer

| Measure | Value |
|---|---|
| Workflows | 22 (enterprise band 13-23) |
| Browser substeps | 23 |
| Pytest substeps | 33 |
| Critical substeps | 14 |
| Non-happy-path ids | 9: `duplicate_delivery_writes_no_second_row`, `member_cannot_create_project`, `administrator_cannot_read_invoice`, `member_denied_project_is_not_found`, `self_approval_rejected_for_elevated_scope`, `revoked_credential_cannot_report_usage` |
| Test module | one, `tests/test_pytest.py`, 33 test functions |
| Sections covered | core features, data integrity, authorization, edge cases |
| Rubric criteria | 14 (12 positive, 2 negative) |
| Checklist items | 215 across 10 sections |

### Rubric dimension shares, positives only

| Dimension | Points | Share | Target | Within 0.10 |
|---|---|---|---|---|
| `instruction_following` | 11 | 0.324 | 0.30 | yes |
| `functionality` | 8 | 0.235 | 0.25 | yes |
| `ux_flow` | 6 | 0.176 | 0.15 | yes |
| `ui_visual` | 6 | 0.176 | 0.15 | yes |
| `motion` | 1 | 0.029 | 0.05 | yes |
| `accessibility` | 1 | 0.029 | 0.05 | yes |
| `responsiveness` | 1 | 0.029 | 0.05 | yes |

### Checklist item classes

| Tag | Count |
|---|---|
| `capability` | 25 |
| `constraint` | 13 |
| `contract` | 46 |
| `data` | 43 |
| `literal` | 42 |
| `role` | 10 |
| `ui` | 36 |

## Literals ledger

`_handoff/E_analy_dash_voice-platform-console-vb_20260916_065523.literals-ledger.json` carries 185 pinned values.

| Class | Count |
|---|---|
| `account` | 6 |
| `credential` | 1 |
| `design_phrase` | 25 |
| `endpoint` | 24 |
| `env_var` | 3 |
| `motion_moment` | 8 |
| `number` | 25 |
| `route` | 15 |
| `scheme` | 12 |
| `seed_record` | 27 |
| `status` | 39 |

Every entry carries `instruction.md` as a carrier and none is `verifier_only`; G6 confirms the bijection in both directions.

## Spec documents and the sections they fed

| Document | Fed |
|---|---|
| `00-decisions.md` | the draws, the variant, the scope record, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow`, the API shapes in `## Deployment contract` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at baseline |

## Grading window

Reported, never failed: the brief has no length limit (G33).

| Section | Chars | Reference |
|---|---|---|
| Core features | 16740 | 2400 |
| User flow | 4788 | 1900 |
| UI/UX notes | 7278 | 1700 |
| Constraints | 1343 | 800 |
| User roles | 2307 | 1000 |
| Overview | 1769 | 700 |
| **joined** | **34225** | 8800 |

## Kit gate log

One row per gate, rendered from the receipt file. `inputs` on every receipt carries the SHA-256 of each bundle file the sweep examined.

| Gate | Tool | Exit | Verdict | Elapsed |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | 0.13s |
| G1/G12 | `layout_lint.py` | 0 | PASS | 0.1s |
| G46 | `structure_lint.py` | 0 | PASS | 0.12s |
| G50 | `docker_lint.py` | 0 | PASS | 0.1s |
| G55 | `runtime_deps_lint.py` | 0 | PASS | 0.11s |
| G63 | `secret_lint.py` | 0 | PASS | 0.09s |
| G48 | `truth_lint.py` | 0 | PASS | 0.37s |
| G51 | `source_lint.py` | 0 | PASS | 0.14s |
| G52 | `rubric_context_lint.py` | 0 | PASS | 0.1s |
| G54 | `comment_lint.py` | 0 | PASS | 0.12s |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | 0.1s |
| G11 | `leak_scan.py` | 0 | PASS | 0.1s |
| G33 | `window_lint.py` | 0 | PASS | 0.09s |
| G4/G5 | `contract_lint.py` | 0 | PASS | 0.1s |
| G43 | `prescription_lint.py` | 0 | PASS | 0.13s |
| G44 | `disclosure_lint.py` | 0 | PASS | 0.1s |
| G10 | `no_sdk_lint.py` | 0 | PASS | 0.12s |
| G31 | `determinism_lint.py` | 0 | PASS | 0.11s |
| G14 | `reward_path_lint.py` | 0 | PASS | 0.09s |
| G27/G30 | `rubric_lint.py` | 0 | PASS | 0.09s |
| G41 | `flag_lint.py` | 0 | PASS | 0.14s |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | 0.09s |
| G59/G60 | `codequality_lint.py` | 2 | ? | 0.1s |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | 0.13s |
| G6 | `fixture_lint.py` | 0 | PASS | 0.14s |
| G24 | `coverage_map.py` | 0 | PASS | 0.13s |
| G37 | `checklist_qc.py` | 0 | PASS | 0.12s |
| G39 | `rubric_align_lint.py` | 0 | PASS | 0.11s |
| G28/G29 | `channel_lint.py` | 0 | PASS | 0.11s |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | 0.12s |
| G0/INV5 | `vendor_check.py` | 0 | PASS | 0.11s |
| G47 | `output_qc.py` | 0 | PASS | 0.14s |

32 of 32 rows green; 0 red.

## Certification prompt receipts

| Prompt | Gate | Verdict | Checks |
|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | PASS 18, WARN 6 |
| `QC_spec.md` | G34 | PASS | PASS 13, WARN 2 |
| `qc_docker.md` | G35 | PASS | NOT-APPLICABLE 13, PASS 91, WARN 1 |
| `qc_rubric.md` | G53 | PASS | PASS 16 |
| `qc_solution_checklist.md` | G37 | PASS | no declared registry |
| `qc_toml.md` | G36 | PASS | NOT-APPLICABLE 11, PASS 107, WARN 2 |
| `task_code_verifier.md` | G3 | VALID | PASS 12 |

Every non-pass check carries a matching finding in the receipt file. The findings are reproduced under BLOCKING FINDINGS below.

## Handoff gates, undecided here

| Gate | Command | Expected |
|---|---|---|
| G13 | `docker build -f environment/Dockerfile .` | exit 0 |
| G13 | `docker build -f tests/Dockerfile .` | exit 0 |
| G15 | `docker compose up` on a scrubbed host | every sidecar healthy |
| G18 | read `deployed` from either oracle run | `deployed == 1.0` |
| G19 | `harbor run -p <task> -a oracle`, twice | `reward == 1.0` both times |
| G20 | `harbor run -p <task> -a nop` | `reward == 0.0` |
| G21 | fake-integration patch, then oracle | `reward < 1.0` |
| G25 | reviewer exploit sweep, reference library F | 0 of 11 succeed |

## Blocking findings

None. No gate is red and no slot obligation is UNMET.

### Non-blocking findings carried from the certification receipts

**`QC_instruction.md`**

- A1: `## Build plan` is absent. generate_instruction.md S-2.1 states it is NOT baseline and that 6/6 shipped reference briefs omit it, so its absence is the baseline shape rather than a missing section. The other ten H2s are present and canonically spelled, and `## Front-end specification` is emitted as the optional eleventh.
- B1: the pattern row names one baseline role; four are carried for the enterprise band. Same finding as QC_spec B1, recorded in 00-decisions.md.
- B3: the three difficulty levers are Technical requirements, Data model and Build plan; the first two are present and Build plan is withheld as baseline, per A1.
- C1: two numbered rules enumerate fields rather than stating an attackable behaviour - Projects rule 1 (a project carries a name, a slug, a region, a retention period, a state) and Scoped credentials rule 1. Both are externally verifiable through the project and credential read endpoints, so neither is code-only, but neither carries a negative case of its own.
- C7: four of the six judged sections run past the 2,500-character slice, and the join runs past 9,000. window_lint reports this and fails nothing: the brief has no length limit, the judged criteria are self-contained and carry their own evaluation_rule, and content past the slice still reaches the agent in full.
- D1: the laziest build returns a constant for `latency_ms` rather than a measured elapsed time. The brief states the latency is measured by the app, but no black-box assertion can distinguish a constant from a measurement in a single run, so the pytest layer asserts only that it is a positive integer. Residual and recorded.

**`QC_spec.md`**

- S5: 04-uiux-brief.md carries no hex palette and no millisecond or cubic-bezier motion values. This is the settled A5 number rule (generate_instruction.md S-4, 'The number rule, DECIDED'), which carries colour as family/tone/shade and motion as character; G51 checks the colour words and the brief would fail G33 and the house style with a hex. The type scale, the accessibility bar (4.5:1, 44x44) and the Mode commitment are carried literally, as that rule requires. S5's demand for literal palette and motion values is superseded.
- B1: the reference/B row for dashboard-analytics names one baseline role (`user`), while the enterprise band in reference/B S-B.3 is three to five roles and the companion states a six-role matrix. Four roles are carried (owner, administrator, member, auditor) and the deviation is recorded in 00-decisions.md under 'Six roles, four seeded'. Providers and slots match the row exactly.

**`qc_docker.md`**

- CMP-011: the `main` service publishes `4173:4173`. CMP-011 forbids a `ports:` key on any service while CMP-022 requires one on `main`, and validate_task's COMPOSE_MAIN_REQUIRED enforces CMP-022 mechanically under G2. No sidecar publishes a port, which is the defect CMP-011 exists to catch.
- DEP-011: `[verifier].environment_mode` is `separate`, so the grader ships its own image built from `tests/Dockerfile` on `deku-verifier-base` and the agent image owes it no Python package. G55 RD-1 skips under this mode for the same reason.
- DEP-012: no `playwright` package is installed in the agent image. The browser grader runs in the verifier image, which carries Chromium already.
- DEP-015: `language` is `javascript`, so the compiled-language multi-stage rule does not apply.
- DEP-016: no build stage exists and nothing is COPYed into the image; the agent writes the application at run time.
- DEP-017: `language` is not `java`, so no JRE is required.
- BP-005: a multi-stage build would separate nothing. The image ships a toolchain for an application that does not exist at build time, so there is no build output to carry forward into a leaner runtime stage.
- BP-008: the base is `python:3.12-slim`, a glibc Debian image; no musl or Alpine base is used.
- ARCH-005: no `TARGETARCH` case or switch is present.
- ARCH-006: `TARGETARCH` is neither declared nor used.
- ARCH-009: no `TARGETARCH` branching is present.
- BP-004: no build-time download in this Dockerfile has a checksum published by any source, so there is none to verify against.
- ENV-002: no `EXPOSE` directive is emitted, so there is nothing that can disagree with the configured port. The compose file publishes the container-internal 4173.
- SEC-003: no source establishes non-root execution for the agent image, and the agent must write to /app, so root is the convention the reference images follow.

**`qc_toml.md`**

- SCHEMA-011: `[delivery]` and `[delivery.images]` are emitted and are not in the toml_generator.md S-11 template. They are required of every new bundle by 01-OUTPUT-CONTRACT.md CON-2 and are validated by validate_task.lint_delivery, which G2 runs. The template is the stale side.
- SCHEMA-013: section order follows the template through `[verifier]`, then places `[delivery]` and `[delivery.images]` before `[[artifacts]]`. The template defines no position for them; see SCHEMA-011.
- BENCH-002: not a trivial or smoke task, so the Trivial tier does not apply. The Standard tier is asserted by BENCH-001.
- BENCH-003: `difficulty` is the mandated empty placeholder (BENCH-006), so there is no declared tier to band against. turns_expected 170 and tokens_expected 7000000 sit in the documented hard band and inside the absolute range BENCH-004 checks.
- BENCH-005: `difficulty` is the empty placeholder, so there is nothing to check for consistency against.
- INT-007: same as BENCH-005 - two of the three terms exist and the third is the placeholder the Calibration Engineer fills.
- TAX-006: `language` is `javascript`, not `any`, so the trivial-task restriction does not apply.
- TAX-008: global archetype uniqueness cannot be verified from the supplied inputs. It is enforced by the mint ledger, which refused no claim for `voice-platform-console`. Recorded as unverifiable, per the row's own instruction.
- VERIF-007: no payments and no storage slot is declared, so there is no shared provider credential to place in `[verifier].env`.
- INST-007: `instruction.md` is present, so the SPEC-as-brief fallback does not apply.
- SIGN-001: deprecated 2026-09-15, superseded by SIGN-004.
- SIGN-002: deprecated 2026-09-15, superseded by SIGN-004.
- SIGN-003: deprecated 2026-09-15, superseded by SIGN-004.

## Budget

`turns_expected = 170`, `tokens_expected = 7000000`. The hard band, chosen because the console carries fifteen tables, four roles with a per-project override, and three arithmetic invariants that must agree across `usage_events`, `usage_rollup_daily` and `invoices`. `difficulty` stays the empty placeholder the Calibration Engineer fills.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference app. Nothing counts toward a corpus target until the app lands and `harbor run -a oracle` returns `1.0` twice.
