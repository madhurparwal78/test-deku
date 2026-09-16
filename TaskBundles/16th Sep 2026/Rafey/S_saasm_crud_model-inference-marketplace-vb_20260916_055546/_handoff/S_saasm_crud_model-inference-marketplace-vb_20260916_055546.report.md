# Build report - S_saasm_crud_model-inference-marketplace-vb_20260916_055546

## Identity

| Field | Value |
|---|---|
| Task code | `S_saasm_crud_model-inference-marketplace-vb_20260916_055546` |
| Task id | `deku/model-inference-marketplace-vb` |
| Cell | solo_founder / saas-micro-tools / crud-catalog |
| Service profile | `P1-db`, slot `backend` -> provider `postgres` |
| Verifier mode | `separate`: the grader ships its own image from `tests/Dockerfile` on `deku-verifier-base` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `python` |
| Design direction | `companion` (the `terminal-mono` draw does not govern; reference/L SS L.6.1) |
| Launch surface | `custom_404, favicon, no_frontend_secrets, page_view_log, social_preview` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit revision | `806eb0a` |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |

## Task Order, as received and as mapped

| Field | Supplied | Minted | Why |
|---|---|---|---|
| category | `solo_founder` | `solo_founder` | legal as given |
| domain | `saas-productivity` | `saas-micro-tools` | not a member of the closed level-2 enum; nearest legal member, and the companion's SS 44.6 records the same substitution |
| pattern | `catalog-browse` | `crud-catalog` | not a member of the closed level-3 enum; the product's dominant shape is a filterable catalogue leading to a detail page with an action |
| archetype | `model-inference-marketplace` | unchanged | three tokens, kebab-case, unclaimed |
| companion | `Drive_PRDs/16_sept/replicate_prd.md` | variant `b` | stage-1: a companion forces variant b on `critical_depth` and `spec_sections` |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Public catalogue, collections, owner profile | INCLUDED | instruction.md ## Core features | the pattern's own surface |
| Schema-driven run form with the JSON and snippet tabs | INCLUDED | ## Core features, ## Front-end specification | the companion's hardest surface |
| Prediction lifecycle, four read modes, idempotency, cancellation | INCLUDED | ## Core features | the unit the meter reads |
| Per-second and per-unit metering, rollups, reconciliation | INCLUDED | ## Core features | the task's hard part |
| Spend caps at admission for every entry point | INCLUDED | ## Core features | the companion's SS 25.4 guarantee |
| Tokens: one-time display, scopes, rotation, revocation | INCLUDED | ## Core features | the credential is the product |
| Organisations, two roles, audit chain | INCLUDED | ## Core features | the tenancy boundary |
| Publishing wizard, derived schema, content digest | INCLUDED | ## Core features | half the catalogue's value |
| Deployments, releases, rollback, scaling policy | INCLUDED | ## Core features | what the pricing page sells |
| Outbox, delivery log, address refusal | INCLUDED | ## Core features | the ordering guarantee |
| Launch surface: not-found, favicon, page views, social preview, no frontend secrets | INCLUDED | ## Core features | the reference/O draw |
| File inputs and file outputs | DROPPED | ## Constraints | no storage slot is declared, so no object store exists to hold them |
| Image, video and audio renderers | DROPPED | ## Constraints | every seeded model returns text or a structured object |
| Payment capture, dunning, tax | DROPPED | ## Constraints | no payments slot; an issued invoice stays `open` |
| Fine tuning and training jobs | DROPPED | ## Constraints | the compute plane is simulated; a version arrives by publication |
| Federated sign in, SSO, SCIM, second factor | DROPPED | ## Constraints | no auth slot; email and password is the only way in |
| Comparison bench, editorial archive, change history, docs site, enterprise form | DROPPED | ## Constraints | out of scope for one bundle; the reserved routes answer not found |
| Multi-region placement and residency | DROPPED | ## Constraints | one region, one control plane |
| Content moderation pipeline | DROPPED | ## Constraints | a report is recorded and queued; nothing screens automatically |
| Outbound email and SMS | DROPPED | ## Constraints | no email slot; notices are in-product records |
| Worker sandbox and untrusted code containment | DROPPED | companion SS 32.5, waived | the platform runs every prediction itself |

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_data_lives_in_postgres_reached_through_the_database_url_with_no_hardcoded_host_or_credential` asserts the prediction exists as a row read through the shared backend adapter; twelve further tests read `predictions`, `usage_records`, `memberships`, `tokens`, `hardware_classes`, `outbox` and `idempotency_keys` directly |

No slot is UNMET.

## Grading surface

| Measure | Value |
|---|---|
| Workflows | 16 (solo_founder band 10 to 16) |
| Browser substeps | 82 |
| Pytest substeps | 182 |
| Browser to pytest substep ratio | 0.45 (G45 band 0.40 to 2.00) |
| Critical substeps | 54 |
| Non-happy-path workflow ids | 9: `anonymous_run_is_unauthenticated_and_returns_to_the_filled_form`, `cross_account_read_of_a_private_model_is_denied_as_missing`, `duplicate_create_runs_once_and_the_usage_rows_reconcile`, `invalid_form_input_is_refused_inline_and_writes_nothing`, `machine_interface_paginates_by_cursor_and_limits_by_token`, `owner_manages_membership_and_a_member_is_denied_the_endpoint`, `revoked_token_cannot_create_a_prediction`, `spend_cap_denied_at_the_form_and_at_the_machine_interface`, `webhook_to_a_loopback_address_is_rejected_at_create` |
| Pytest module | one, `tests/test_output.py`, 182 tests |
| Sections covered | core features, data integrity, authorization, edge cases |
| Checklist items | 409 |
| Judged criteria | 15 |

Rubric split: 14 positive, 1 negative. Positive point total 38.

| Dimension | Share | Target | Delta |
|---|---|---|---|
| `instruction_following` | 0.316 | 0.30 | +0.016 |
| `functionality` | 0.237 | 0.25 | -0.013 |
| `ux_flow` | 0.211 | 0.15 | +0.061 |
| `ui_visual` | 0.158 | 0.15 | +0.008 |
| `motion` | 0.026 | 0.05 | -0.024 |
| `accessibility` | 0.026 | 0.05 | -0.024 |
| `responsiveness` | 0.026 | 0.05 | -0.024 |

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Overview | 2128 | 700 | over-reference |
| User roles | 2706 | 1000 | past-slice |
| Core features | 46014 | 2400 | past-slice |
| User flow | 11900 | 1900 | past-slice |
| UI/UX notes | 14681 | 1700 | past-slice |
| Constraints | 2211 | 800 | over-reference |
| joined total | 79640 | 8800 | past-slice |

Length is reported, never failed: G33 and `generate_instruction.md` SS 4 retired the
brief's length limit outright. Content past the slice reaches the agent in full and
stops reaching the advisory judge, whose criteria are self-contained.

## Literals ledger

| Class | Count | Examples |
|---|---|---|
| `account` | 3 | `owner@example.com`, `member@example.com`, `member2@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `endpoint` | 16 | `/api/predictions`, `/api/tokens`, `/api/hardware`, `/api/collections` |
| `env_var` | 5 | `DATABASE_URL`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `DB_ADMIN_URL` |
| `number` | 18 | `25`, `100`, `1200`, `40000` |
| `route` | 21 | `/api/health`, `/explore`, `/pricing`, `/privacy` |
| `scheme` | 16 | `mp_`, `req_`, `pr`, `Idempotency-Key` |
| `seed_record` | 56 | `maren-vos`, `arden-hale`, `vela-research`, `northlight` |
| `status` | 37 | `starting`, `processing`, `succeeded`, `failed` |

173 entries. Two are `verifier_only` and live in `[verifier].env` alone:
`DB_ADMIN_URL` and `DEKU_SERVICE_BACKEND`. Every other entry carries at least one of
`instruction.md`, `conftest.py`, `test_pytest.py` and `task.toml` as a real carrier, and
G6 holds the bijection in both directions.

## Authoring documents

| Doc | Fed |
|---|---|
| `_spec/S_saasm_crud_model-inference-marketplace-vb_20260916_055546/00-decisions.md` | the draw record, the taxonomy substitutions, the judgment calls and the companion carry table |
| `_spec/S_saasm_crud_model-inference-marketplace-vb_20260916_055546/01-PRD.md` | ## Overview, ## Core features, ## Constraints |
| `_spec/S_saasm_crud_model-inference-marketplace-vb_20260916_055546/02-TRD.md` | ## Technical requirements |
| `_spec/S_saasm_crud_model-inference-marketplace-vb_20260916_055546/03-app-flow.md` | ## User flow, ## Deployment contract API shapes |
| `_spec/S_saasm_crud_model-inference-marketplace-vb_20260916_055546/04-uiux-brief.md` | ## UI/UX notes, ## Front-end specification |
| `_spec/S_saasm_crud_model-inference-marketplace-vb_20260916_055546/05-backend-schema.md` | ## Data model, ## User roles |
| `_spec/S_saasm_crud_model-inference-marketplace-vb_20260916_055546/06-implementation-plan.md` | not emitted into the brief: `## Build plan` is not baseline |

`_spec/` sits beside the bundle, never inside it (CON-5). CON-1 records the folder as
retired while `stage-2-instruction.md` still lists it as a Produces and `G49` reads its
`draw:` lines; it is written here so the draws, the substitutions and the carry table
have a home, and so `QC_spec.md` has an artifact to review.

## Kit gate log

Rendered from `_handoff/S_saasm_crud_model-inference-marketplace-vb_20260916_055546.gates.jsonl`. Never transcribed.

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
| G59/G60 | `codequality_lint.py` | 2 | ? |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 0 | PASS |


## Certification prompts

Recorded in `_handoff/S_saasm_crud_model-inference-marketplace-vb_20260916_055546.receipts.json`,
one scorecard per prompt over the registry the prompt itself declares, with the token bound
to the prompt bytes at kit revision `806eb0a`. Every one is SELF-ATTESTED: this was a
single-agent run, so the author and the reviewer are the same identity and the kit's
`owner != verifier` rule is not satisfied. These are recorded verdicts, never independent
ones.

| Gate | Prompt | Checks | Verdict |
|---|---|---|---|
| G34 | `QC_spec.md` | 15 | PASS, 2 WARN |
| G34 | `QC_instruction.md` | 24 | PASS, 4 WARN |
| G36 | `qc_toml.md` | 120 | PASS |
| G35 | `qc_docker.md` | 105 | PASS, 1 WARN |
| G37 | `qc_solution_checklist.md` | adjudication, no declared registry | CHANGES REQUIRED |
| G53 | `qc_rubric.md` | 16 | PASS, converged on cycle 2 |
| G3 | `task_code_verifier.md` | 12 | VALID |

The generator prompts `generate_instruction.md`, `solution_checklist.md`,
`toml_generator.md`, `docker_generator.md`, `pytest_generator.md` and `rubric_author.md`
carry no receipt and are reported UNCITED by G40 as advisory notes. `task.toml`,
`environment/`, the pytest layer and the rubric were authored from the stage files,
`reference/I`, `reference/J`, `reference/C` and the gate-green reference bundle under
`Output/15sept-erpnext/` rather than from those four prompts.

## Realignment to kit `806eb0a`

The bundle was first built on `b3d0577`. Five commits landed after it and each one touched
this bundle. What changed, and what was done:

| Commit | Change | Applied here |
|---|---|---|
| `1b99060` | `code_quality` becomes an authored code-quality rubric dimension | No change. The vendored `recompute.py` still renders `judged_criteria` alone, so a bundle carrying `source` criteria would need a hand-authored `tests/rubric.json` that G48's regeneration check cannot prove. This bundle ships the PRODUCT half only and `codequality_lint` reports NOT-APPLICABLE, which stage-3.6 names as a legal state that must be declared rather than passed silently |
| `da24d3b` | The section pytest module is renamed `tests/test_output.py`; the generated compiled-rubric file becomes `solution/trinity/test_ans.py` | Module renamed, every `test:` id in `workflows.yaml` rewritten to `test_output.py::<test>`, the `tests/Dockerfile` COPY line updated, the stale `solution/trinity/test_output.py` deleted and `test_ans.py` regenerated, and the literals ledger's carrier labels follow |
| `11eaf7b` | `[verifier].environment_mode` defaults to `"separate"` | Switched from `"shared"`. The grader now ships its own image built from `tests/Dockerfile` on `deku-verifier-base`, which this bundle already carried, so the shared-mode prerequisite that used to head the handoff contract is gone |
| `78e5ba6` | The vendored `test.sh` for grader `0.22.0` is stripped of its 35 whole-line comments and re-pinned | Re-copied byte-for-byte from `vendor/grader-0.22.0/`. 125 lines become 90. Noted below: the pin now attests to the kit's fork rather than to the harness's copy |
| `806eb0a` | `solution/USER_README.md` returns as a GENERATED file carrying the seeded logins and the canary | Regenerated by `recompute.py` at `truth-generator-7`, alongside `TRUTH.md`. G12 now checks the canary in both copies and passes on both |

Two consequences the operator should carry forward:

- **INV5 drift control is weaker than it was.** `78e5ba6` forks `test.sh` and re-mints
  `MANIFEST.json` to match, so `vendor_check` now compares this bundle against the kit's
  own copy rather than the harness's. If the harness ships a different `test.sh`, nothing
  in this bundle will say so first.
- **What the stripped comments recorded is gone from the file.** The note explaining why
  `test.sh` runs without `set -e` -- a failing pytest is a SCORE rather than a harness
  error, and aborting there strands the reward file so the trial is lost rather than scored
  zero -- no longer appears in the script anybody later tidies.

## Kit self-contradictions found, and how each was resolved

Each one is a place where two kit files disagree. None is a bundle defect, and none was
resolved by loosening a gate.

| Where | The disagreement | Resolved |
|---|---|---|
| `QC_instruction.md` A1, B3 vs `generate_instruction.md` SS 2.1 | A1 lists `## Build plan` among the eleven required H2s; SS 2.1 states it is NOT baseline and that a baseline brief omits it entirely | SS 2.1 governs. The section is absent; A1 and B3 recorded WARN |
| `QC_instruction.md` C4 vs `generate_instruction.md` SS 4 (A5) | C4 lists pinned type sizes as a MAJOR; A5 requires the exact font family and the exact sizes, and reference/L SS L.6 repeats it | A5 governs, and C4's own text says the two must agree. The brief carries the type scale and no hex, no millisecond, no curve and no pixel breakpoint |
| `QC_instruction.md` C7 vs G33 | C7 fails a section clearly over its reference length; G33 and SS 4 retired length as a failure | G33 governs. `window_lint` reports `past-slice`, which is information |
| `QC_spec.md` S8 vs `generate_instruction.md` SS 2.9 / SS 2.10 | S8 calls a decision restating a derivation-table fact noise; SS 2.9 requires a `draw:` line per axis in `00-decisions.md` and G49 reads them | Both honoured: the draws sit under their own heading, separate from the residual calls |
| `QC_spec.md` B1 vs `reference/B` SS B.3 | B1 keeps the pattern row's role count, which is one for crud-catalog; B.3 bands solo_founder at one to two roles | B.3 cited, the departure logged in `00-decisions.md`, the permission shape kept |
| `qc_docker.md` CMP-011 vs CMP-022 | CMP-011 asks the compose file to be free of published host ports; CMP-022 and stage-5 C12 require `main` to set `ports` and `extra_hosts` | CMP-022 governs: seven shipped tasks lost every trial by omitting `main` |
| `CON-1` vs `stage-2-instruction.md` and G49 | CON-1 records `_spec/` as retired; stage-2 lists it as a Produces and G49 reads its `draw:` lines | The folder is written beside the bundle, never inside it, so CON-5 holds and the draws have a home |
| `stage-9-assemble.md` vs G50 | Stage 9 tells `tests/Dockerfile` to lead with the `# syntax=` directive; G50 now refuses any `#` line in `environment/Dockerfile` | Scoped as written: neither Dockerfile carries one, and G54 permits the directive where it is wanted |
| `stage-7-graders.md` vs G54 | Stage 7 asks for `# --- core features ---` section banners inside the module; G54 refuses every comment in the bundle | The banners are module-level string constants, `_CORE_FEATURES` and its three siblings, so the sections stay legible and no comment ships |

## Blocking findings

None for the kit-executable batteries. Three things a downstream operator must know:

1. **`qc_solution_checklist.md` returned CHANGES REQUIRED (NEEDS REVIEW).** Two literals are
   declared under `Referenced but not pinned`: the per-endpoint webhook signing secret and
   the server-side pepper used when hashing a token. Neither may be pinned in the brief,
   because INV4 keeps a secret out of an agent-visible surface and G63 refuses a
   source-shaped secret value. SS 5 of that prompt grades an unpinned literal that does not
   block as NEEDS REVIEW, so that is the recorded verdict.
2. **The checklist is a graded subset, not an exhaustive restatement.** 409 items were
   emitted from a larger authored pool. The cull was driven by G24: an item no grader can
   honestly cite is coverage that reports itself as present, which the kit calls worse than
   absence. Eleven obligations were dropped on the record and are named in the receipt for
   that prompt.
3. **The code-quality rubric half is absent by design.** `codequality_lint` reports
   NOT-APPLICABLE because no `evaluation_target: "source"` criterion is carried. Stage-3.6
   allows this and requires it to be declared, which this line does.

## Budget

`turns_expected` 200 and `tokens_expected` 8000000, the standard tier. The reasoning: one
brief of roughly 145 KB, 25 tables, 41 machine endpoints, 33 page routes and 409 graded
obligations, with a schema-driven form and an exactly-once meter as the two surfaces that
take a rewrite to get right. `tokens_expected` sits at the top of the documented
200000 to 8000000 band because the brief alone is a substantial read before any code exists.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference application, and nothing in it has been
compiled or run. It becomes admissible when the app lands downstream from
`solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
