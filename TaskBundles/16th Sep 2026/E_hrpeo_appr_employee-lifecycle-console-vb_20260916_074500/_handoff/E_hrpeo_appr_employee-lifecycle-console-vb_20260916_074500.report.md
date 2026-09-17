# Build report - E_hrpeo_appr_employee-lifecycle-console-vb_20260916_074500

Rendered from `_handoff/<code>.gates.jsonl` and `_handoff/<code>.receipts.json`. No verdict in
this file is hand-written; every one is the receipt a tool or a prompt left behind.

## Identity

| | |
|---|---|
| Task code | `E_hrpeo_appr_employee-lifecycle-console-vb_20260916_074500` |
| Task id | `deku/employee-lifecycle-console-vb` |
| Cell | enterprise / hr-people-ops / approval-workflow |
| Service profile | `P3-db-auth` (slots `db`, `auth`) |
| Providers | `backend` = postgres · `auth` = keycloak |
| Variant | `b`, axes `critical_depth` + `spec_sections` |
| Language | typescript |
| Design direction | `companion` (reference/L §L.6.1: a companion beats the draw) |
| Launch surface | `custom_404,favicon,no_broken_links,no_frontend_secrets,single_cta` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Companion | `/Users/apple/Downloads/greythr_prd.md` (2366 lines) |
| Shard | 1 of 1 |
| Exit state | `MECHANICALLY-GREEN, NO-SOLUTION`, with G46 red on placement |

## Why variant b, and why these draws

A companion document was supplied, so `config/corpus-targets.yaml` `companion_variant` puts
the task one rung up at `b` on the `critical_depth` and `spec_sections` axes: a task built
from a real product carries far more graded surface than five lines can, and shipping it at
the gentle rung wastes the one input that makes it hard. Above `a`, §4.0-B deletes the
concurrency reminder from the brief, so the Data model states each contention rule as an
observable invariant and never says where the window is.

Every derived-design value is a SHA-256 draw over the archetype, recorded as a `draw:` line
in `_spec/<code>/00-decisions.md`:

| Axis | Value |
|---|---|
| render_model | `ssr-islands` |
| backend | `Hono` |
| frontend | `Nuxt 3` |
| nav | `sidebar-nav` |
| work_surface | `queue-list` |
| create_flow | `inline-row` |
| feedback | `optimistic-row` |
| design_direction | `companion` (the bank would have drawn `editorial-serif`) |

The interaction draw and the companion agree without being made to: the companion's own
product shell is a left rail, its approval surface is one queue, and its Section 26.5 asks
for an optimistic queue action. The design draw was overridden per §L.6.1 because
`editorial-serif` would have written a serif print register over a measured white-and-violet
data product.

## Feature resolution

| Feature | Verdict | Where it landed |
|---|---|---|
| Identity through the declared provider, and the employee record | INCLUDED | Core features, Data model, Technical requirements |
| The leave policy engine | INCLUDED | Core features, Data model |
| Applying for leave, and the derived balance ledger | INCLUDED | Core features, Data model |
| Attendance: append-only punches, the day computation, regularisation | INCLUDED | Core features, Data model |
| Claims with limits and escalation | INCLUDED | Core features |
| One approval queue, scoped by the reporting line | INCLUDED | Core features, User flow |
| The payroll run lifecycle and the statutory rule set | INCLUDED | Core features, Data model |
| The register | INCLUDED | Core features, Front-end specification |
| Sign-off with same-actor separation | INCLUDED | Core features |
| The employee surface | INCLUDED | Core features |
| The launch surface (five drawn obligations) | INCLUDED | Core features, Technical requirements, UI/UX notes |
| Onboarding, exit, the final settlement | DROPPED | Constraints. Out of scope per the Task Order's daily loop |
| The typed assistant | DROPPED | Constraints. A second product |
| The report builder, scheduling, export delivery | DROPPED | Constraints. A second product |
| Payroll pre-flight, the statutory calendar, workforce cost planning | DROPPED | Constraints. The companion marks all three as proposals |
| Approval delegation, support impersonation | DROPPED | Constraints. Needs roles the pattern row does not carry |
| Billing, integrations, letters, outbound email | DROPPED | Constraints. No slot declared for any of them |
| The marketing website (companion Sections 7 to 9) | DROPPED | Waived at G51. The Task Order is the console behind the login |

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| backend | postgres | MET | the persistence, ledger, payslip and reconciliation checks, through the verifier's own connection |
| auth | keycloak | MET | the denial checks, the tampered-token check and the issuer-claim check |

## The grading surface

| | |
|---|---|
| Workflows | 23 (enterprise band 13-23) |
| Browser substeps | 71 |
| pytest substeps | 60 |
| `critical` substeps | 14 |
| Non-happy-path workflow ids | 7 |
| pytest module | one, `tests/test_output.py`, 60 test functions |
| Sections it covers | core features, authorization, data integrity, edge cases |
| Rubric criteria | 17 (15 positive, 2 negative) |
| Checklist items | 614 |
| Core asks in the traceability matrix | 100, none partially graded |

Non-happy-path ids: `peer_manager_decision_denied`, `manager_self_decision_denied`, `concurrent_and_repeat_decisions_conflict`, `duplicate_punch_raw_ref_writes_no_second_row`, `claim_escalates_or_is_refused_as_invalid`, `same_actor_signoff_denied_and_wrong_total_refused`, `unauthenticated_and_employee_requests_denied`

### Checklist by section

| Section | Items |   | Class | Items |
|---|---|---|---|---|
| `C-CF` | 181 |  | `capability` | 25 |
| `C-CN` | 16 |  | `constraint` | 89 |
| `C-DC` | 50 |  | `contract` | 132 |
| `C-DM` | 88 |  | `data` | 66 |
| `C-FE` | 78 |  | `literal` | 117 |
| `C-OV` | 11 |  | `role` | 29 |
| `C-RL` | 51 |  | `ui` | 156 |
| `C-TR` | 44 |  |  |  |
| `C-UF` | 39 |  |  |  |
| `C-UX` | 56 |  |  |  |

### Rubric dimensions, positive score share against the frozen budget

| Dimension | Criteria | Positive points | Share | Target | Within 0.10 |
|---|---|---|---|---|---|
| `instruction_following` | 3 | 11 | 0.268 | 0.30 | yes |
| `functionality` | 3 | 11 | 0.268 | 0.25 | yes |
| `ux_flow` | 2 | 6 | 0.146 | 0.15 | yes |
| `ui_visual` | 4 | 6 | 0.146 | 0.15 | yes |
| `motion` | 1 | 3 | 0.073 | 0.05 | yes |
| `accessibility` | 2 | 2 | 0.049 | 0.05 | yes |
| `responsiveness` | 2 | 2 | 0.049 | 0.05 | yes |
| negatives (outside the budget) | 2 | -4 | - | - | - |

Rubric provenance: 17 criteria, 21 checklist items claimed, no id claimed twice.

## Literals ledger

204 pinned values. G6 holds the bijection in both directions: every value
appears verbatim in the carriers it declares, and every literal the graders assert is pinned in
`instruction.md`.

| Class | Count |
|---|---|
| `account` | 7 |
| `credential` | 1 |
| `design_phrase` | 13 |
| `endpoint` | 24 |
| `env_var` | 8 |
| `number` | 32 |
| `route` | 12 |
| `scheme` | 15 |
| `seed_record` | 40 |
| `status` | 52 |

Verifier-only (INV4, absent from the brief and from `[environment].env`): `DB_ADMIN_URL`, `AUTH_ADMIN_TOKEN`.

## The spec folder, and what each doc fed

| Doc | Feeds |
|---|---|
| `00-decisions.md` | the draws, every residual judgment call, and the companion carry table |
| `01-PRD.md` | Overview, Core features, Constraints |
| `02-TRD.md` | Technical requirements |
| `03-app-flow.md` | User flow, and the graded API surface |
| `04-uiux-brief.md` | UI/UX notes, Front-end specification |
| `05-backend-schema.md` | Data model, User roles |
| `06-implementation-plan.md` | authoring-side only; `## Build plan` is not emitted at baseline |

The spec folder lives at `Output/16sept-greythr/_spec/<code>/` and never inside the bundle (CON-5).

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| core_features | 12988 | 2400 | past-slice |
| user_flow | 2963 | 1900 | past-slice |
| ui_ux_notes | 4620 | 1700 | past-slice |
| constraints | 1332 | 800 | over-reference |
| user_roles | 2909 | 1000 | past-slice |
| overview | 1258 | 700 | over-reference |
| joined | 26070 | 8800 | past-slice |

Recorded, not paid for. `window_lint.py` reports length and fails nothing; §4 of
`generate_instruction.md` states there is no length limit and forbids cutting a real rule to
fit. The cost is that the judge reads the first 2500 characters of Core features and none of
the payroll, sign-off or launch-surface rules. `judge_score` never touches reward, and the
17 judged criteria are self-contained per reference/I §I.8, so the loss is a diagnostic
number rather than a scored one. It is the largest open trade-off in this bundle and
QC_instruction C7 carries it as a WARN.

## Declared but ungraded

22 checklist items were removed because no channel this bundle carries can observe them. Each
remains a requirement in `instruction.md`, which is the only file the agent reads, so nothing
was dropped from the specification. This is the D-H shape stage-3 names and leaves open.

| Item | Why no channel can see it |
|---|---|
| The stack is TypeScript on Node 20 | framework identity is source-visible only; G10 bars the reward path from reading source |
| Nuxt 3 renders the routes on the server | as above. The observable half, complete HTML on first paint, is kept and is graded |
| Only the named libraries are used | source-visible only |
| No second database, cache, queue or identity provider | source-visible only. The observable half, the issuer claim, is kept and is graded |
| Logs go to standard output, one line per request | no admissible channel reads container logs |
| A log line carries method, path, outcome, elapsed ms | as above |
| A log line never carries a password, token, email or salary | as above |
| There is no trace pipeline | as above |
| There is no metrics exporter | as above |
| No edge function is used | an environment declaration the kit's own gates enforce, not app behaviour |
| No persistent volume, fixed container name or custom network | as above; validate_task C1/C11 and docker_lint own it |
| The schema holds twenty-three tables | a table count is an implementation shape, not an observable |
| All timestamps are UTC | no pinned fixture makes this falsifiable in a bounded run |
| An employee record is retained for its jurisdiction's statutory period | unmeasurable in a bounded grading run |
| Punches are retained 3 years | as above |
| Audit entries are retained 7 years | as above |
| The directory stays responsive at 10000 employees | the seed holds 120; the volume cannot be reached |
| The month grid stays responsive at 1000 by 31 | as above |
| The register stays responsive at 10000 by 40 | as above |
| Reporting reads stay responsive over 12 months | as above |
| The type scale is a reconstruction rather than a measurement | a fact about the companion document, not an obligation on the product |
| The colour roles are exact | as above |

## Kit gate log

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS |
| G1/G12 | `layout_lint.py` | 0 | PASS |
| G46 | `structure_lint.py` | 1 | FAIL |
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
| G47 | `output_qc.py` | 1 | FAIL |

Every row above is a receipt carrying the SHA-256 of the bytes it examined.

## Prompt receipts (the adversarial gates)

| Prompt | Gate | Verdict | Checks answered | Non-PASS |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | A1, A8, B1, B3, C5, C7, D4 |
| `QC_spec.md` | G34 | PASS | 15 | B1, S2, S3, S5, S6 |
| `qc_docker.md` | G35 | PASS | 105 | ARCH-002, ARCH-003, BLD-004, BP-004, BP-005, CMP-011, CMP-020, CMP-021, CON-004, DEP-011, DEP-012, DEP-013, DEP-015, DEP-016, DEP-017, ENV-003, ENV-004, ENV-006 |
| `qc_rubric.md` | G53 | PASS | 16 | RC-12 |
| `qc_solution_checklist.md` | G37 | PASS | 0 | none |
| `qc_toml.md` | G36 | PASS | 120 | BENCH-002, BENCH-003, BENCH-005, COV-004, INST-007, INT-007, SIGN-001, SIGN-002, SIGN-003, TAX-006, TAX-008, VERIF-007 |
| `task_code_verifier.md` | G3 | VALID | 12 | none |

Every one is SELF-ATTESTED: one agent authored the artifact and ran its reviewer. The kit's
rule is owner != verifier, so these are recorded verdicts and never independent ones, and
`prompt_receipt_lint.py` reports that state on every row rather than in a footnote.

### What the reviewers actually changed

The QC passes were not decoration. Eleven defects were found and fixed before sign-off:

- **QC_instruction C2/C3/D2** - the largest finding of the run. Journey 1 and five pytest
  checks read a pending leave approval raised by `E-1001`, a pending approval raised by
  `E-1003` and a claim approval waiting on a payroll account. Seed data implied the first
  through a pending ledger entry and stated neither of the others, so a correct application
  could have been graded as broken on three checks. All three are now pinned by date and
  approver.
- **QC_instruction C4** - `## UI/UX notes` committed to no mode. It now commits to light.
- **qc_toml SCHEMA-011** - the one Critical. `[metadata]` carried `rubric_version`, which is
  in no template; the judge pin is one corpus fact and lives in `config/kit-config.yaml`.
- **qc_toml META-003** - `openhands_version` and `calibration_date` were present; schema 1.4
  retires both.
- **qc_toml SCHEMA-013/014** - the whole file is re-emitted in the canonical key order.
- **qc_toml ENV-010** - the healthcheck carried 120.0/90 instead of the pinned 60.0/60.
- **qc_docker HAL-007/BC-006** - `NODE_ENV=development` contradicted the production-build
  requirement and no source supported it.
- **qc_docker DEP-004/HAL-010** - `git` and `curl` were installed with no supporting source.
- **qc_docker CMP-019** - `restart:` was set on both sidecars.
- **QC_spec S6/S7/G1/G2** - the spec folder lacked the idempotent-seeding sentence, ended
  before deploy and self-test, named no seeded account, and listed no API endpoint.
- **qc_solution_checklist, hat 3** - 273 of 626 citations came from a step that does not
  observe the item claimed. Every one was re-homed or justified in writing, and six new
  browser workflows were added so the design system, the responsive matrix, the scope
  boundary, the role matrix, the bulk decisions and the deployment contract are walked.

## Blocking findings

**G46 placement, and it is the only red gate.** `kit_config.output_root()` resolves the
contract's output root to `/Users/apple/Downloads/Output`, a sibling of the kit tree. This
bundle sits at `GreenField-GenKit2/Output/16sept-greythr/`, inside the tree, because that
location was requested explicitly. It is recorded rather than silently moved. The finding
fires on all ten bundles currently under that path, so it describes where this corpus is
being written rather than anything about these bytes. G47 is red only because G46 is. The
handoff carries the one-command fix.

No other blocking finding. No spec gap prevented a required test; no harness gap left a
declared slot unobserved.

## Versions

| | |
|---|---|
| Kit | deku-green-field, this working tree |
| Vendored grader | 0.22.0, `test.sh` byte-identical to the pin |
| Target schema | 1.4 |
| Harbor | 0.20.0 |
| Corpus canary | present in `solution/TRUTH.md` and `solution/USER_README.md`, absent from the brief |

## Budget, and the reasoning

`turns_expected = 160`, `tokens_expected = 5500000`. Eleven must-have features against the
companion cap of 6 to 10, three roles with relationship scoping rather than role scoping, a
payroll computation with five statutory heads and two worked examples, and a seed of 120
employees with a year of ledger history. That is past the medium band (120-140 turns, 4.5M
to 5M tokens) and short of hard (170 turns, 7M). `difficulty` stays the empty placeholder
BENCH-006 requires; the Calibration Engineer writes it, never the author, so qc_toml
BENCH-003 and INT-007 are recorded as warnings rather than guessed into a pass.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION -- with G46 red on placement
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the app is built downstream from
`solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
