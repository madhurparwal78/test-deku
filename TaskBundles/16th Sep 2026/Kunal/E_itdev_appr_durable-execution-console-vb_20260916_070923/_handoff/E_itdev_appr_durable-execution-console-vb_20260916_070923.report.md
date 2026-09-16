# Build report - E_itdev_appr_durable-execution-console-vb_20260916_070923

## Identity

| | |
|---|---|
| Task code | `E_itdev_appr_durable-execution-console-vb_20260916_070923` |
| Task id | `deku/durable-execution-console-vb` |
| Cell | enterprise / it-devtools / approval-workflow |
| Service profile | `P3-db-auth` (the cell's minimal legal profile) |
| Providers | `backend` = `postgres`, `auth` = `keycloak` |
| Variant | `b`, axes `["critical_depth", "spec_sections"]` |
| Language | `python` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field @ `ac66ec3` (branch `madhur-test`, merging `origin/yasir-test`) |
| Grader pin | `0.22.0` |
| Target schema | `1.4` |

**Input: a PRD-mode run file**, `PRD/temporal_run.yaml`, as the kit revision requires. S0 ran
`run_lint.py check` (G64), wrote the Task Order from the run file with `run_lint.py task-order`
into `Output/16sept_temporal/_spec/durable-execution-console.task-order.yaml`, and linted that
file (G0). The tasker's original `PRD/temporal_input.yaml` arrived with `domain:
it-service-management` and `pattern: admin-console`, neither in the closed enum, so the idea file
`PRD/temporal_idea.yaml` carries the corrected `it-devtools` and `approval-workflow`, confirmed
with the tasker before minting. Recorded in `_spec/E_itdev_appr_durable-execution-console-vb_20260916_070923/00-decisions.md`.

Earlier stages were authored against revision `806eb0a`; the merge to `ac66ec3` landed mid-build.
It changed the input model and the G51 waiver procedure, and no rule governing the bundle's own
files, so conforming needed process changes only. Every gate below was re-run on `ac66ec3`.

## Derived-design draws

All from `sha256("durable-execution-console")` =
`d8142d0105526811ada41ef96f3b7ed7a9f2b4bdcd78183d69bd9427e0fb76f2`.

| Axis | Value |
|---|---|
| render_model | `spa-json-api` |
| backend | `FastAPI` |
| frontend | `Svelte + Vite` |
| design_direction | `companion` (a supplied PRD beats the bank, reference/L L.6.1) |
| nav | `breadcrumbed-drill-down` |
| work_surface | `queue-list` |
| create_flow | `modal` |
| feedback | `full-page-confirmation` |
| launch_surface | favicon, form_validation, privacy_page, security_headers, sitemap_robots |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Public product surface + demonstrator | INCLUDED | Core features 1 | companion 8, 10, 15; carries 4 of the 5 drawn launch tokens |
| Change requests, review and approval | INCLUDED | Core features 2 | companion 34; the pattern's critical focus and the variant-b depth axis |
| Namespaces and regions | INCLUDED | Core features 3 | companion 26; isolation is the strongest public claim |
| Workflow executions and event history | INCLUDED | Core features 4 | companion 27; the product's deepest screen |
| Principals, roles, grants, policy | INCLUDED | Core features 5 | companion 25; the enterprise tier's defining property |
| Workers, task queues, deployments | INCLUDED | Core features 6 | companion 29, reduced to fleet health |
| Audit trail | INCLUDED | Core features 7 | companion 32; append-only evidence |
| Console shell, tables, resilience | INCLUDED | Core features 8 | companion 24, 42 |
| Billing, metering, invoices | DROPPED | Constraints | companion 33; no money path in this build, so the whole rating pipeline is out |
| Schedules and batch operations | DROPPED | Constraints | companion 28; orthogonal to the graded core |
| Outbound webhooks and notifications | DROPPED | Constraints | companion 35; needs a second provider slot the cell does not permit |
| Observability dashboards | DROPPED | Constraints | companion 30 |
| Service-account key issuance | DROPPED | Constraints | companion 31; the principal model is carried, the key screens are not |
| Fourteen marketing routes | DROPPED | Constraints | companion 10-23; named individually so the cut is on the record |

Eight must-have features, inside the 6-10 companion cap (reference/G G.2.1).

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | stored-row assertions across the suite; `critical` on `test_seeded_namespace_rows_exist` |
| `auth` | `keycloak` | MET | denial and token assertions; `critical` on `test_seeded_principal_login_token_is_accepted` |

## Grading surface

| | |
|---|---|
| Workflows | 22 (enterprise band 13-23) |
| Browser substeps | 22 |
| pytest substeps | 51 |
| `critical` substeps | 17 |
| Non-happy-path workflow ids | 7 |
| pytest module | one, `tests/test_output.py`, 51 test functions |
| Banners covered | core features, authorization, data integrity, edge cases (enterprise earns authorization) |
| Checklist items | 343 |

Non-happy-path ids: `requester_cannot_approve_their_own_request`, `developer_cannot_apply_or_create_and_row_is_denied`, `authorisation_cannot_be_laundered_through_approval`, `cross_tenant_read_is_denied_at_the_api`, `expired_and_denied_grants_cannot_be_used`, `unauthenticated_mutation_is_denied`, `last_owner_and_directory_group_cannot_be_edited`.

## Rubric

| | |
|---|---|
| Criteria | 12 |
| Positive / negative | 11 / 1 |
| Positive total | 25 |
| Negative magnitude | 3 (cap is 3x positive) |
| `task completion` share | 75% (band 60-80%) |

| Dimension | Points | Share | Target | Verdict |
|---|---|---|---|---|
| instruction_following | 8 | 0.32 | 0.30 | within 0.10 |
| functionality | 6 | 0.24 | 0.25 | within 0.10 |
| ux_flow | 4 | 0.16 | 0.15 | within 0.10 |
| ui_visual | 4 | 0.16 | 0.15 | within 0.10 |
| motion | 1 | 0.04 | 0.05 | within 0.10 |
| accessibility | 1 | 0.04 | 0.05 | within 0.10 |
| responsiveness | 1 | 0.04 | 0.05 | within 0.10 |

The code-quality channel is **absent by necessity**: every vendored `recompute.py`
(0.20.0 through 0.23.0) restricts `judged_criteria` to the seven product dimensions, so a
`scope_discipline` or `internal_consistency` criterion cannot be rendered into
`tests/rubric.json` without editing a vendored file, which INV5 forbids. The channel is advisory
and a bundle may ship without it (`rubric_lint.check_source_battery`), so G59/G60 return
NOT-APPLICABLE. Two such criteria were authored and then withdrawn; they are recorded here so the
omission is a decision rather than an oversight.

## Literals ledger

`_handoff/E_itdev_appr_durable-execution-console-vb_20260916_070923.literals-ledger.json`, 123 entries.

| Class | Count |
|---|---|
| `account` | 5 |
| `credential` | 1 |
| `design_phrase` | 17 |
| `endpoint` | 6 |
| `env_var` | 6 |
| `motion_moment` | 6 |
| `number` | 6 |
| `route` | 9 |
| `scheme` | 9 |
| `seed_record` | 24 |
| `status` | 34 |

Two entries are `verifier_only` (`DB_ADMIN_URL`, `AUTH_ADMIN_TOKEN`) and appear in neither the
brief nor `[environment].env` (INV4, verified by G6 and G17).

## spec/ docs emitted

At `Output/16sept_temporal/_spec/E_itdev_appr_durable-execution-console-vb_20260916_070923/`, never inside the bundle (`layout_lint.FORBIDDEN_DIRS`
contains `spec`).

| Doc | Fed |
|---|---|
| `00-decisions.md` | the eight `draw:` lines G49 reads, the residual judgment calls, and the companion carry table |
| `01-PRD.md` | Overview, Core features, Constraints |
| `02-TRD.md` | Technical requirements; S5 derives the base image from it |
| `03-app-flow.md` | User flow |
| `04-uiux-brief.md` | UI/UX notes, Front-end specification |
| `05-backend-schema.md` | Data model, User roles |
| `06-implementation-plan.md` | nothing in the brief: `## Build plan` is not emitted above variant `a`, and withholding it is one of the two declared variant axes |

## Companion carriage (G51) and the recorded run (G64)

The run is RECORDED, which is this corpus's convention: `PRD/temporal_prd.md` was split with
`prd-generator/tools/split_prd.py` into a plain projection and a technical projection, and
`run_lint.py record` wrote the run into `_handoff/E_itdev_appr_durable-execution-console-vb_20260916_070923.sources.json` with a SHA-256 of
the idea file and of the plain PRD. `revalidate.py` therefore needs **no `--source` and no
`--waive` flags**, and G64 is a real PASS rather than NOT-APPLICABLE.

| | |
|---|---|
| Authored PRD | `PRD/temporal_prd.md`, 7,859 lines, 49 sections |
| Recorded source | `PRD/temporal_prd_plain.md` (the plain-language projection G64 reads) |
| Topics carried | 49 / 49 |
| Waivers | **1** |
| Colours described | 29 / 29 from the authored PRD, by family, tone and shade; the brief carries no hex anywhere (A5) |

The single waiver is companion Section 48, the acceptance checklist: it is the document's own
apparatus, and its sixty rows became numbered rules inside the features they belong to rather
than a section of the brief. Recorded with `run_lint.py waive`, so it lives in the bundle's
`sources.json` rather than in a shell invocation.

Measured against the **authored** PRD instead, the same brief carries 347/347 headings and
1,126/1,126 enumerated items but needs 83 waivers, because the authored file quotes notation the
brief may not carry at all: hexes, `cubic-bezier` curves, keyframe blocks and millisecond
durations are forbidden by A5, and `source_lint.items()` strips underscores before extracting
words, so a snake_case column row reduces to glued tokens no brief can match. The plain
projection is the contractual source and is what the receipts cite.

## Grading window (G33)

| Section | Chars | Reference |
|---|---|---|
| Core features | 24,254 | 2,400 |
| UI/UX notes | 7,576 | 1,700 |
| User flow | 6,300 | 1,900 |
| User roles | 3,234 | 1,000 |
| Overview | 2,654 | 700 |
| Constraints | 1,889 | 800 |
| Joined | ~43,600 | 8,800 |

`window_lint.py` fails nothing on length and the brief has no limit. The joined total is past
`run_rubric.py`'s 9,000-char slice, so the tail reaches the agent in full and the judge in part.
Accepted deliberately: `judge_score` never touches reward, and G51 requires the companion's 1,126
enumerated items to be carried. Recorded rather than trimmed.

## Kit gate log

Rendered from `_handoff/E_itdev_appr_durable-execution-console-vb_20260916_070923.gates.jsonl`. 33 receipts,
31 green, 2 red.

| Gate | Tool | Exit | Verdict | State | stdout SHA |
|---|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | green | `230c05dd6263eef7` |
| `G1/G12` | `layout_lint.py` | 0 | PASS | green | `101289804ba74932` |
| `G46` | `structure_lint.py` | 0 | PASS | green | `0e66ee4fea8d2469` |
| `G50` | `docker_lint.py` | 0 | PASS | green | `380ed7d1c830de35` |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | green | `a0c21dca8bc5f78a` |
| `G63` | `secret_lint.py` | 0 | PASS | green | `513e7024656ce884` |
| `G48` | `truth_lint.py` | 0 | PASS | green | `dff97fe1f73e5aa8` |
| `G51` | `source_lint.py` | 0 | PASS | green | `d350e1d3f59466f3` |
| `G64` | `run_lint.py` | 0 | PASS | green | `50e907499437c713` |
| `G52` | `rubric_context_lint.py` | 0 | PASS | green | `c51e86ce4c60c7a5` |
| `G54` | `comment_lint.py` | 0 | PASS | green | `f0cd955e315863c3` |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | green | `1881993ee324d483` |
| `G11` | `leak_scan.py` | 0 | PASS | green | `fc82ee31ce1946f9` |
| `G33` | `window_lint.py` | 0 | PASS | green | `3065a4f66d850602` |
| `G4/G5` | `contract_lint.py` | 0 | PASS | green | `6fd5517dd92ca1b1` |
| `G43` | `prescription_lint.py` | 0 | PASS | green | `aa8dde568307b772` |
| `G44` | `disclosure_lint.py` | 0 | PASS | green | `8267b0c24157bf02` |
| `G10` | `no_sdk_lint.py` | 0 | PASS | green | `165f63ab0afcf99e` |
| `G31` | `determinism_lint.py` | 0 | PASS | green | `43f17821cff40b01` |
| `G14` | `reward_path_lint.py` | 0 | PASS | green | `18dbdf6b8162128f` |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | green | `b93acd1b3eb3335d` |
| `G41` | `flag_lint.py` | 0 | PASS | green | `fac903b6aa7abf18` |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | green | `cdf20c83e9056866` |
| `G59/G60` | `codequality_lint.py` | 2 | ? | green | `e23941dd85e0253b` |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | green | `06eef1f9e28bb1f4` |
| `G6` | `fixture_lint.py` | 0 | PASS | green | `1d82354e48b049d7` |
| `G24` | `coverage_map.py` | 1 | FAIL | **RED** | `25aac8bfe728f723` |
| `G37` | `checklist_qc.py` | 0 | PASS | green | `5fdcfd303819cc4e` |
| `G39` | `rubric_align_lint.py` | 0 | PASS | green | `27bfa237c760f1be` |
| `G28/G29` | `channel_lint.py` | 0 | PASS | green | `d9a59bbe835a8589` |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | green | `8cdbd872df25b344` |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | green | `afd5548f4604344a` |
| `G47` | `output_qc.py` | 1 | FAIL | **RED** | `46a4c3edb6545683` |

`G59/G60` exits 2 = NOT-APPLICABLE: the bundle carries no code rubric (see the rubric section
for why). `G64` is a real PASS: the run is recorded. G40 exits 0 with WARN: all seven certification prompts carry a current, bundle-bound
receipt, and every one is SELF-ATTESTED because a single agent authored and reviewed the bundle.
The kit's rule is owner != verifier, so those are recorded verdicts, never independent ones.

## Gates run outside the per-bundle sweep

`revalidate.py` runs only per-bundle gates. These were run separately on the same kit revision,
and their output lines are quoted verbatim; none of them writes a receipt row.

| Gate | Command | Result |
|---|---|---|
| G0 | `taskorder_lint.py _spec/durable-execution-console.task-order.yaml` | `VERDICT PASS` - G0 Task Order valid |
| G64 | `run_lint.py check PRD/temporal_run.yaml` | `VERDICT PASS` - prd mode run file is valid |
| G3 | `task_code.py decode <code>` | `VALID: all levels decode and every taxonomy rule holds` |
| G38 | `kit_selftest.py` | `VERDICT PASS (32 checks)` |
| G22 | `overlap.py` | NOT-APPLICABLE - no sibling variant of `durable-execution-console` exists in any ledger |
| G42 | `corpus_overlap.py` over the four `Output/16sept_*` bundles | `VERDICT PASS (4 bundles, 1 cross-archetype pairs compared)` - no pair above 60% substep overlap |
| G49 | `diversity_lint.py Output/` | `PASS` - no shared run over the per-section caps; concentration NOT-APPLICABLE under 5 bundles |
| G61 / G26 | `corpus_report.py` | NOT-APPLICABLE - no admissible bundle in this run's ledger (1 minted, 1 unproven); explicitly not a pass |

The G42 pair worth naming is this bundle against
`16sept_vercel/E_itdev_appr_deployment-governance-console-vb_20260916_071312`, which sits in the
same cell (enterprise, it-devtools, approval-workflow). Their substep overlap is under the 60% cap.

## Adversarial QC (G3, G34, G35, G36, G37b, G53)

`_handoff/E_itdev_appr_durable-execution-console-vb_20260916_070923.receipts.json`, 292 declared checks answered across seven prompts.

| Prompt | Gate | Verdict | Checks |
|---|---|---|---|
| `task_code_verifier.md` | G3 | VALID | 12 PASS |
| `QC_instruction.md` | G34 | PASS | 23 PASS, 1 WARN |
| `QC_spec.md` | G34 | PASS | 15 PASS |
| `qc_toml.md` | G36 | PASS | 110 PASS, 8 NOT-APPLICABLE, 2 SKIP |
| `qc_docker.md` | G35 | PASS | 96 PASS, 9 NOT-APPLICABLE |
| `qc_solution_checklist.md` | G37 | PASS | registry declares none |
| `qc_rubric.md` | G53 | PASS | 16 PASS |

Seven defects were raised by running the prompts and all seven were repaired:

1. **QC_instruction D4** - the No-mocks block read "readable by a separate connection using
   `DATABASE_URL`", which names an external checker and locates it outside the app's own code.
   G44 deliberately cannot express this form, so the author owns it. Rewritten to product-truth
   form.
2. **QC_spec S1** - only `00-decisions.md` existed in `_spec/`; the six remaining docs were
   authored, with `02-TRD.md` carrying the stack S5 derives the base image from.
3. **qc_toml META-009** - `keywords` carried `typescript` out of the documented order. Removed.
4. **qc_toml BENCH-003** - `turns_expected` was 240, outside the expert band. Lowered to 200.
5. **qc_toml ENV-006** - the per-slot credentials used a task-local convention instead of the
   canonical `deku_app` / `deku_admin` / `deku-local-dev`. Realigned across four files.
6. **qc_docker CMP-019** - both sidecars carried `restart: unless-stopped`, which CMP-019 forbids.
   Removed. The central kit fragment still carries it, which is where the shape came from.
7. **qc_rubric RC-03** - three criteria shared the anchor "change request detail" at facet
   "existence". Split so each names a distinct part.

Generator prompts read: `generate_instruction.md` in full (all 2,004 lines). `toml_generator.md`,
`docker_generator.md`, `solution_checklist.md` and `pytest_generator.md` were consulted in part,
against their reference libraries, and carry no receipt; G40 reports each as UNCITED-advisory,
which is accurate.

## Blocking findings

**G24 is RED on 21 checklist items, and G47 is RED only because G24 is.** This is
OPEN-DECISIONS **D-H** (ISSUES D-4), still unanswered by the kit.

The items, with why no runtime channel may observe them:

| Items | Obligation | Why unobservable |
|---|---|---|
| `C-TR-01`, `C-TR-02`, `C-TR-17` | the frontend is Svelte + Vite; the backend is FastAPI; validation is declared once per operation | observing these means reading the agent's source, which **INV6 and G10 forbid on the reward path**. Unobservable by invariant, not by accident |
| `C-TR-07`, `C-TR-08`, `C-TR-09`, `C-TR-10` | no second database or identity provider; every host read from the environment; the app creates no realm | absence of a thing, black-box |
| `C-DC-08`, `C-DC-09` | `.browser_screenshots/` and `.downloads/` exist empty at the app root | a filesystem fact; under `environment_mode = "separate"` the grader cannot read the app container's disk |
| `C-DC-14`, `C-DC-15` | the backing services are never downloaded or started by the app | absence of an action during a build the grader does not watch |
| `C-DC-16`, `C-DC-17`, `C-DC-18` | no edge function, no persistent volume, no custom network | facts about `environment/docker-compose.yaml`, already checked by G1, G2 C1/C11 and G50 -- but by a kit gate, not a runtime channel |
| `C-CN-07`, `C-CN-09`, `C-CN-10`, `C-CN-11` | nothing reaches the public internet at runtime; no native app; no email sent; no payload parsed | three are absences; `C-CN-10` has no inbox capability to assert against because the `email` slot is not declared |
| `C-CN-12` | responsive at the stated data volume | needs a 200,000-event seed; the seed carries 40 events, which is what the cursor-paging assertions need |
| `C-FE-24`, `C-FE-25` | degraded behaviour when PostgreSQL or the codec endpoint is unreachable | needs a dependency taken down mid-run, which is chaos the browser and pytest channels cannot perform (reference/N) |

Per `stage-3-checklist.md` the author's only two options are to fabricate a citation or silently
drop the item, and the kit's instruction is to **do neither** and escalate. The proposed
resolution is a fourth checklist part, `## Declared but ungraded` with a mandatory `why:`, which
`checklist_qc.py` does not yet parse. Nothing here was fabricated and nothing was dropped.

Coverage actually achieved: **322 of 343 items cited**, 254 by pytest, 13 by browser substeps, 55
by rubric criteria, with G28/G29 green (every part of every ask graded by exactly one channel) and
G39 green (56/56 judgment obligations graded).

Two further kit-level contradictions were resolved in favour of the tool that runs, and are
recorded rather than quietly absorbed:

- **`spec/` placement.** CON-1 calls `_spec/` retired while `stage-2-instruction.md` still
  requires the folder and `diversity_lint.read_draws()` reads `../_spec/<basename>/00-decisions.md`.
  Written to `Output/16sept_temporal/_spec/<code>/`: outside the bundle, where both tools agree.
- **The `# syntax=` directive.** `stage-5-dockerfile.md` and `stage-9-assemble.md` require it on
  line 1; `docker_lint.py` (G50) forbids every `#` line including that one, and says so in its own
  docstring. Followed the tool.

## Budget

`turns_expected = 200`, `tokens_expected = 8000000`. Eight must-have features against the 6-10
companion cap, three seeded roles, two organisations, an append-only history with cursor paging,
and a concurrency surface with four single-winner invariants. The companion feature cap raises the
budget with the count (reference/G G.2.1), and 200 turns is the top of the documented band while
`difficulty` stays the unwritten placeholder the Calibration Engineer owns.

## Exit state

```
GATES RED (G24, G47), NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the reference app lands downstream from
`solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
