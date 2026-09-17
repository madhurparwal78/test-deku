# Build report - E_finan_appr_financial-data-network_20260916_060815

Rendered from `_handoff/E_finan_appr_financial-data-network_20260916_060815.gates.jsonl`. No verdict in this file was typed by hand.

## Identity

| Field | Value |
|---|---|
| task code | `E_finan_appr_financial-data-network_20260916_060815` |
| task id | `deku/financial-data-network` |
| uuid_v5 | `4610c5b9-52bd-5406-beb3-6fe7855074f6` |
| cell | enterprise / finance-accounting / approval-workflow |
| service_profile | `P3-db-auth` |
| providers | backend `postgres`, auth `keycloak` |
| variant | `a` |
| language | `typescript` |
| authors | QL `abhishek.shaw@ethara.ai`, contributor `nishant.dubey@ethara.ai` |
| grader pin | `0.22.0` (INV5, vendor_check green) |
| target schema | `1.4` |
| verifier mode | `separate` (the kit default as of commit 11eaf7b) |
| shard | 1 of 1 |

## Derived-design draws (R4)

Drawn from `sha256("financial-data-network")`, the `task_code` as `reference/L` §L.4 resolves it.

| Axis | Value |
|---|---|
| `render_model` | `mpa-progressive` |
| `backend` | `Express + Nunjucks` |
| `frontend` | `Alpine.js + server templates` |
| `design_direction` | `glass-depth` |
| `nav` | `sidebar-nav` |
| `work_surface` | `board-first` |
| `create_flow` | `modal` |
| `feedback` | `full-page-confirmation` |

`launch_surface` draws separately (reference/O §O.3): `cookie_choice`, `no_broken_links`, `no_frontend_secrets`, `spam_protection`, `terms_page`. All five are numbered among the Core features and the Technical requirements, and each carries a grader.

## Slot obligations

| Slot | Provider | Status |
|---|---|---|
| `backend` | `postgres` | MET, three critical pytest substeps |
| `auth` | `keycloak` | MET, eight critical pytest substeps |

## Grading layer

- workflows: **22** (enterprise band 13-23)
- browser substeps **24**, pytest substeps **40**, critical **14**
- one pytest module, `tests/test_output.py`, **40** test functions
- checklist items **263**, each cited by exactly one channel (G24 both directions, G28/G29 green)
- judged rubric criteria **13** (11 positive, 2 negative)

| Category | Substeps |
|---|---|
| `business_rule` | 8 |
| `core_outcome` | 1 |
| `data_integrity` | 7 |
| `presentation` | 5 |
| `security` | 14 |
| `validation` | 5 |

Weight is derived from `(category, critical)`, never chosen. Floors held: one `core_outcome`, two `data_integrity`, one `security`.

| Dimension | Positive share | Target |
|---|---|---|
| `instruction_following` | 0.37 | 0.30 |
| `functionality` | 0.22 | 0.25 |
| `ux_flow` | 0.15 | 0.15 |
| `ui_visual` | 0.15 | 0.15 |
| `motion` | 0.04 | 0.05 |
| `accessibility` | 0.04 | 0.05 |
| `responsiveness` | 0.04 | 0.05 |

## Grading window

| Section | Chars | Kit target |
|---|---|---|
| `## Core features` | 2784 | 2400 |
| `## User flow` | 2820 | 1900 |
| `## UI/UX notes` | 3050 | 1700 |
| `## Constraints` | 817 | 800 |
| `## User roles` | 1717 | 1000 |
| `## Overview` | 987 | 700 |

`window_lint.py`'s own figures. Joined six **12175**. The brief has no length limit in this kit revision: G33 measures and never fails.

## Literals ledger

**122** pinned values, bijective against the brief and the graders (G6 green).

| Class | Count |
|---|---|
| `account` | 6 |
| `credential` | 1 |
| `endpoint` | 14 |
| `env_var` | 8 |
| `number` | 5 |
| `route` | 9 |
| `scheme` | 9 |
| `seed_record` | 41 |
| `status` | 29 |

## Companion document

`plaid_prd.md`, 7,938 lines. G51 green: **61/61** source colours described by family and tone, **363/363** topics and **1764/1764** enumerated items carried or waived on the receipt. The brief carries **no hex at all**.

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
| G59/G60 | `codequality_lint.py` | 2 | NOT-APPLICABLE |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | PASS |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 1 | FAIL |

**32 gates recorded, 30 green, 2 red.**

### The red gates, and why they are red

- **G46** - FAIL
- **G47** - FAIL

**G46 and G47 are one finding, and it is a placement decision rather than a bundle defect.**
`structure_lint.py` derives the generation kit's root from its own file location, which is
`/Users/apple/Downloads/GreenField-GenKit2`, and CON-1 rejects any bundle beneath it. This bundle
is deliberately placed there because the tasker asked for that path after being shown this exact
finding. G47 is red only because it refuses to certify an output carrying a red gate, and G46 is
the only one.

**VERIFIED, not asserted.** The identical bytes were copied to a sibling root and swept again
immediately before this report was written: **ALL GATES GREEN**, G46 and G47 included. Nothing
else in the bundle is outstanding. The remedy, if the placement is ever revisited, is a move and
one config line, and it changes no byte:

```
mv /Users/apple/Downloads/GreenField-GenKit2/Output /Users/apple/Downloads/Output
output_root: /Users/apple/Downloads/Output/16sept-plaid
```

## Aligned to the kit at commit 806eb0a

This bundle was authored against an earlier kit and migrated forward twice. The second pass
covered four commits:

| Commit | What the bundle did |
|---|---|
| `11eaf7b` emit `environment_mode = "separate"` by default | `[verifier].environment_mode` moved from `shared` to `separate`; no `[verifier.environment]` table exists, which is the only thing shared mode forbade |
| `78e5ba6` strip comments from the vendored `test.sh` and re-pin | `tests/test.sh` re-vendored; G0/INV5 green against the new hash |
| `806eb0a` restore `solution/USER_README.md` as GENERATED | `recompute.py` re-vendored to truth-generator-7, which now emits it from the same `grounding.yaml` as the rest of the answer key, so the seeded logins cannot drift from the literals the graders assert |
| CON-2 renames the pytest module | `tests/test_pytest.py` renamed to `tests/test_output.py`, with every `workflows.yaml` substep prefix and the `tests/Dockerfile` COPY line following it |

The first pass, against the 2026-09-15 pull, is itemised in the previous revision of this report:
`solution/app/` retired, pytest substeps gaining `category` and `weight`, `[task].authors` reduced
to two bare addresses, `uuid_v5` minted, `[signoff]` retired, `launch_surface` drawn, G51 inverted
to describe colours rather than state them, and `cubic-bezier(` banned brief-wide.

**One stale artifact was removed in this pass.** `solution/trinity/test_output.py` was left behind
when truth-generator-7 renamed its target to `trinity/test_ans.py`. Its bytes were identical, so no
gate saw it, but a generated file with no generator is the drift this contract exists to stop, and
it shared a name with the pytest module two directories away. Deleted; `recompute.py --check`
reports no drift.

## Known gaps, stated rather than papered over

- **The code-quality channel is absent.** `rubric_lint.py` accepts source criteria in
  `tests/rubric.json` under `evaluation_target: "source"`, and CON-2 documents them, but the
  VENDORED `recompute.py` rejects the two code dimensions: its `JUDGED_DIMENSIONS` holds the seven
  product dimensions only. Generator and gate disagree; INV5 forbids editing the generator; and
  `rubric_lint` states that carrying no source criteria is legal. Seven authored criteria were
  dropped rather than smuggled in, and restore unchanged once the generator learns the dimensions.
- **The instruction-following overlay is absent**, same reason: the vendored generator emits no
  `tests/if_constraints.json`. G56/G57/G58 report NOT-APPLICABLE, which stage-3.6 permits.
- **G34/G35/G36/G37b/G53 are SELF-ATTESTED.** The agent that authored the artifacts also reviewed
  them, so those verdicts are recorded, never independent.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The reference app is built downstream and never ships inside the bundle. Nothing
counts toward corpus targets until it lands and `harbor run -a oracle` returns `1.0` twice.
