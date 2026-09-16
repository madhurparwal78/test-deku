# Build report - E_legal_cont_brand-governance-portal-vb_20260916_064757

## Identity

| | |
|---|---|
| Task code | `E_legal_cont_brand-governance-portal-vb_20260916_064757` |
| Task id | `deku/brand-governance-portal-vb` |
| Product | Tessera Brand Guidelines |
| Cell | enterprise / legal-compliance / content-publishing |
| Archetype | `brand-governance-portal` |
| Variant | `b`, axes `critical_depth`, `spec_sections` (a companion document was supplied) |
| Service profile | `P4-db-storage` |
| Providers per slot | `backend` = `postgres`, `storage` = `minio` |
| Language | `python` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 (no device sharding configured) |
| Kit | deku-green-field, gate index G0..G63 |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Verifier mode | `separate` (the kit default since 2026-09-16; the grader ships its own image from `tests/Dockerfile`) |
| Companion | `prd/dropboxbrand_prd.md`, 6,393 lines, 47 sections |
| QL | abhishek.shaw@ethara.ai |
| Contributor | sunil.kumar@ethara.ai |

## Derived-design draws

Every draw is SHA-256 over the archetype `brand-governance-portal` (reference/L §L.4).

| Axis | Value |
|---|---|
| `stack` | python + postgres + minio |
| `interaction_shape` | document-read-then-governed-console |
| `nav` | overlay-only lateral movement, no breadcrumb, no next-chapter link |
| `design_direction` | `companion` (the draw returned `terminal-mono`; reference/L §L.6.1 hands the axis to the measured product) |
| `launch_surface` | `cookie_choice`, `custom_404`, `no_broken_links`, `security_headers`, `spam_protection` |

`flag_lint.launch_surface("brand-governance-portal")` returns exactly that five, and
`[metadata].launch_surface` records it. G41 is green, so each of the five reached the brief:
the cookie frame and the not-found page are in `## Core features`, the internal-link and
robot-refusal rules are there too, and the security header set is in
`## Technical requirements`.

## Feature resolution

| | |
|---|---|
| Brief | 79,472 chars across 11 H2 sections |
| H2 sections | Overview, User roles, Core features, User flow, UI/UX notes, Technical requirements, Data model, Front-end specification, Constraints, Deployment contract, Definition of done |
| Checklist items | 300 across 10 section codes |
| Item tags | capability 34, constraint 72, contract 22, data 73, literal 28, role 15, ui 56 |
| Roles | `visitor`, `employee`, `partner`, `reviewer` (enterprise band 3 to 5; signup closed) |
| Critical focus | one approval stage admits exactly one decision, under contention |

The category modifier for `enterprise` closes signup and scopes by relationship: a
`partner` is bounded by the asset classes their engagement grants and by its end date.

## Slot obligations

| Slot | Provider | Observed by |
|---|---|---|
| `db` | `postgres` | `test_seeded_principals_and_assets_persisted_and_idempotent`, `test_stored_deadline_survives_a_policy_change`, `test_audit_record_is_written_once_per_transition` |
| `storage` | `minio` | `test_employee_downloads_available_asset_and_row_is_recorded`, `test_protected_object_address_is_refused_anonymously`, `test_proof_upload_size_and_sniffed_type_are_enforced` |

G9 requires a `critical` substep per declared slot and G32 requires the test-name
vocabulary to match; both are green.

## Grading layer

| Channel | Size | Owner |
|---|---|---|
| pytest | 49 tests in one `test_output.py` | S7 |
| browser | 21 substeps across 18 workflows | S6 |
| rubric (judged) | 22 criteria, `R1`..`R22` | S3.5 via `recompute.py` |
| compiled rubric | 24 items, skip-wrappers in `solution/trinity/test_ans.py` | S3.5 |

`workflows.yaml` carries 49 pytest substeps and 10 `critical: true` vetoes.
`critical` appears in `workflows.yaml` and nowhere else, which is what G9 checks.

Channel exclusivity (INV7, G28/G29) holds in all three directions: no `ui`-tagged item
carries a pytest citation, because every test in this bundle speaks HTTP and the store
rather than driving a page; the rubric claims no `contract`, `data` or `role` item; and
no item is claimed by both a browser substep and a judged criterion.

### Rubric dimension shares, positives only

| Dimension | Criteria | Points | Share | Frozen weight |
|---|---|---|---|---|
| `instruction_following` | 4 | 18 | 0.22 | 0.30 |
| `functionality` | 3 | 13 | 0.16 | 0.25 |
| `ux_flow` | 2 | 6 | 0.07 | 0.15 |
| `ui_visual` | 5 | 13 | 0.16 | 0.15 |
| `motion` | 4 | 14 | 0.17 | 0.05 |
| `accessibility` | 3 | 13 | 0.16 | 0.05 |
| `responsiveness` | 1 | 5 | 0.06 | 0.05 |
| **total** | **22** | **82** | **1.00** | **1.00** |

The four budgeted dimensions all sit inside the 0.10 tolerance G30 allows, and each
carries at least two criteria. `type` is `task completion` on 16 of 22 (73%), inside the
60 to 80% band.

## Literals ledger

182 values, every one verified present in `instruction.md` before it was recorded.

| Class | Count |
|---|---|
| `seed_record` | 63 |
| `scheme` | 25 |
| `endpoint` | 18 |
| `status` | 16 |
| `route` | 15 |
| `motion_moment` | 13 |
| `design_phrase` | 12 |
| `number` | 9 |
| `account` | 5 |
| `env_var` | 5 |
| `credential` | 1 |

No entry is `verifier_only`, so INV4 has nothing to hold: the admin DSN lives in
`[verifier].env` alone and never appears in the brief. G6 proves the bijection both ways.

## Authoring documents

| File | Role |
|---|---|
| `instruction.md` | the only file the agent sees |
| `solution/checklist.md` | the coverage target every channel is joined against |
| `solution/trinity/grounding.yaml` | the single authored answer-key source |
| `solution/TRUTH.md` | GENERATED; the private golden trajectory, one of the two canary copies |
| `solution/USER_README.md` | GENERATED; the seeded literals and the canary the harness greps by filename |
| `solution/trinity/rubrics.json` | GENERATED reference rubric |
| `solution/trinity/test_ans.py` | GENERATED skip-wrappers citing the section graders |
| `tests/rubric.json` | GENERATED judged rubric, read at run time |
| `tests/traceability-matrix.md` / `.csv` | GENERATED on every sweep from the G24 scan |
| `_spec/<code>/00-decisions.md` | residual decisions and the `draw:` lines G49 reads |

## Companion carriage (G51)

| Measure | Result |
|---|---|
| Colours described by family and tone | 48 / 48 |
| Topics carried | 379 / 379 |
| Enumerated items carried | 1421 / 1421 |
| Declared waivers | 140 |

The brief carries no hex anywhere; every companion colour reaches it as its family, tone
and shade. The 140 waivers are recorded in `g51-waivers.txt` beside the bundle and cover
the companion's measurement apparatus rather than its product obligations: CSS custom
property declarations, `calc()` grid arithmetic, z-index stacks, raw SVG path data, the
easing catalogue, DOM selector censuses, angle-bracket placeholder spellings, the copy
deck body text, and the evidence-gap accounting. Each class is forbidden in a brief by
the number rule (A5) or by INV9, which is why it is declared rather than carried.

## Kit gate log

Rendered from `_handoff/E_legal_cont_brand-governance-portal-vb_20260916_064757.gates.jsonl`, one row per gate, with the exit code and the
SHA-256 of the bytes it examined. Never transcribed.

**32 gates: 30 PASS, 1 WARN, 1 NOT-APPLICABLE, 0 FAIL.**

| Gate | Tool | Exit | Verdict | Time |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS |  |
| `G1/G12` | `layout_lint.py` | 0 | PASS |  |
| `G46` | `structure_lint.py` | 0 | PASS |  |
| `G50` | `docker_lint.py` | 0 | PASS |  |
| `G55` | `runtime_deps_lint.py` | 0 | PASS |  |
| `G63` | `secret_lint.py` | 0 | PASS |  |
| `G48` | `truth_lint.py` | 0 | PASS |  |
| `G51` | `source_lint.py` | 0 | PASS |  |
| `G52` | `rubric_context_lint.py` | 0 | PASS |  |
| `G54` | `comment_lint.py` | 0 | PASS |  |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS |  |
| `G11` | `leak_scan.py` | 0 | PASS |  |
| `G33` | `window_lint.py` | 0 | PASS |  |
| `G4/G5` | `contract_lint.py` | 0 | PASS |  |
| `G43` | `prescription_lint.py` | 0 | PASS |  |
| `G44` | `disclosure_lint.py` | 0 | PASS |  |
| `G10` | `no_sdk_lint.py` | 0 | PASS |  |
| `G31` | `determinism_lint.py` | 0 | PASS |  |
| `G14` | `reward_path_lint.py` | 0 | PASS |  |
| `G27/G30` | `rubric_lint.py` | 0 | PASS |  |
| `G41` | `flag_lint.py` | 0 | PASS |  |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS |  |
| `G59/G60` | `codequality_lint.py` | 2 | NOT-APPLICABLE |  |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS |  |
| `G6` | `fixture_lint.py` | 0 | PASS |  |
| `G24` | `coverage_map.py` | 0 | PASS |  |
| `G37` | `checklist_qc.py` | 0 | PASS |  |
| `G39` | `rubric_align_lint.py` | 0 | PASS |  |
| `G28/G29` | `channel_lint.py` | 0 | PASS |  |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN |  |
| `G0/INV5` | `vendor_check.py` | 0 | PASS |  |
| `G47` | `output_qc.py` | 0 | PASS |  |

`G59/G60` is NOT-APPLICABLE by design: the vendored `recompute.py` at grader pin
`0.22.0` refuses any judged criterion whose `dimension` sits outside the seven product
dimensions, so the two code-quality dimensions cannot reach `tests/rubric.json`. INV5
forbids patching the generator, so the bundle carries no source-target criteria and the
gate reports that it did not run rather than passing having checked nothing.

### Certification prompt scorecards

| Prompt | Gate | Checks | Verdict | Non-PASS |
|---|---|---|---|---|
| `QC_instruction.md` | `G34` | 24 | PASS | `A1`, `B3`, `C7` |
| `QC_spec.md` | `G34` | 15 | PASS | `S1`, `S2`, `S3`, `S4`, `S5`, `S6`, `S7` |
| `qc_docker.md` | `G35` | 105 | PASS | `CMP-011` |
| `qc_rubric.md` | `G53` | 16 | PASS | none |
| `qc_solution_checklist.md` | `G37` | 0 | PASS | none |
| `qc_toml.md` | `G36` | 120 | PASS | `SIGN-001`, `SIGN-002`, `SIGN-003` |
| `task_code_verifier.md` | `G3` | 12 | VALID | none |

292 declared checks across the seven certification prompts, 14 recorded as WARN.
Every WARN is a prompt row that predates a mechanical gate and names both owners in its
finding. None is a defect in the artifact:

- `QC_spec.md` S1 to S7 audit the seven-doc `_spec/` package that CON-1 retires outright.
  S5 additionally demands hex, millisecond and easing literals that the number rule and
  G51 forbid.
- `QC_instruction.md` A1 counts `## Build plan` among the eleven H2s, which
  `generate_instruction.md` §2.1 makes non-baseline; B3 expects the levers that section
  carried, and §4.0-B deliberately deletes the concurrency reminder at variant `b`; C7
  enforces a length budget `window_lint.py` states it never fails.
- `qc_docker.md` CMP-011 forbids published host ports, which the App Contract itself pins
  as `${APP_PUBLIC_PORT}:4173` on `main`.
- `qc_toml.md` SIGN-001 to SIGN-003 are marked deprecated in their own registry rows and
  are superseded by SIGN-004, which passes.

Running these prompts for real surfaced one genuine defect, which was fixed rather than
waived: `qc_toml.md` BENCH-003 and BENCH-004 caught `tokens_expected = 9000000`, above the
8,000,000 absolute ceiling, alongside `turns_expected = 240`. Both were corrected to the
expert band (200 turns, 8,000,000 tokens) and `validate_task.py` re-run.

**All seven are SELF-ATTESTED.** Owner and verifier are one agent in this run, so G40
reports WARN rather than PASS and these verdicts are recorded, never independent.

## Corpus-level gates

| Gate | Scope | Status |
|---|---|---|
| `G42` | corpus overlap | run over the whole output root, not per bundle |
| `G49` | diversity | WARN mode until the §2.9/§2.10 banks are populated |
| `G61` | corpus mix against 0/10/30/40/20 | advisory, once per corpus at S10 |

This output root holds one bundle, so all three have nothing to compare against yet.

## Blocking findings

NONE. Every gate the kit can run is green, and the two that are not PASS say why in
their own words: G40 is WARN because owner and verifier are one agent, and G59/G60 is
NOT-APPLICABLE because the grader pin refuses source-target criteria.

## Budget

| | |
|---|---|
| `turns_expected` | 200 |
| `tokens_expected` | 8,000,000 |
| `[agent].timeout_sec` | 18000.0 |
| `[verifier].timeout_sec` | 3600.0 |
| Resource tier | Standard: 4 cpus, 8192 MB, 20480 MB storage |

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`

Not admissible. The bundle carries no reference app: D20 defers it downstream, and
`solution/solve.sh` exits non-zero saying so. It becomes admissible only when the app
lands and `harbor run -a oracle` returns `1.0` twice. Nothing here counts toward corpus
targets until then.
