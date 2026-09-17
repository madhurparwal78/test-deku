# Build report: E_sales_cont_agency-campaign-operations-vb_20260916_093701

| Field | Value |
|---|---|
| task code | `E_sales_cont_agency-campaign-operations-vb_20260916_093701` |
| task id | `deku/agency-campaign-operations-vb` |
| cell | enterprise / sales-crm / content-publishing |
| service_profile | `P4-db-storage` (db: postgres, storage: minio) |
| variant | `b`, axes ['critical_depth', 'spec_sections'] |
| language | `javascript` |
| spec_sections_given | ['overview', 'roles', 'features', 'flow', 'uiux', 'frontend', 'techrequirements', 'datamodel', 'constraints', 'contract'] |
| design_direction | `companion` |
| launch_surface | `alt_text,colour_contrast,page_view_log,sitemap_robots,terms_page` |
| shard | 1 of 1 |
| kit | generation-kit HEAD 806eb0a 2026-09-16 12:27:57 +0530; grader 0.22.0; schema 1.4 |
| turns / tokens expected | 200 / 8000000 |
| exit state | `MECHANICALLY-GREEN, NO-SOLUTION` |

turns_expected and tokens_expected reflect a two-surface product (a bilingual public site plus a
role-scoped studio), 42 tables, a private object store and 110 API graders plus
68 browser steps: a build of this size runs to hundreds of tool turns.

## Feature resolution

Every companion section and its landing place is in `Output/_spec/E_sales_cont_agency-campaign-operations-vb_20260916_093701/00-decisions.md`
(companion carry table, INCLUDED). Two companion subjects were dropped by G51 waiver and two by judgment call:

| Candidate | Verdict | File | Reason |
|---|---|---|---|
| S-39 acceptance checklist | DROPPED | instruction.md | every line restates a rule already in the brief |
| S-38 homepage probe note | DROPPED | instruction.md | describes the measuring instrument, not the product |
| executive role | DROPPED | instruction.md | a global bypass defeats the confidentiality wall |
| notification centre | DROPPED | instruction.md | no mail or push slot is declared; the brief states no notifications are sent |
| every other companion section | INCLUDED | instruction.md | see the carry table |

## Slot obligations

| Slot | Provider | State | Evidence |
|---|---|---|---|
| db | postgres | MET | G32 green; database-row graders read PostgreSQL through the verifier's adapter |
| storage | minio | MET | G32 green; storage-object graders read version and hero objects from the bucket |

## Graders

- workflows: 23; browser substeps: 68; pytest substeps: 110; critical: 30
- pytest categories: {'core_outcome': 4, 'business_rule': 30, 'validation': 10, 'data_integrity': 23, 'security': 32, 'presentation': 11}
- test module: `tests/test_output.py`, covering every section of `instruction.md`: Overview, User roles, Core features, User flow, UI/UX notes, Front-end specification, Technical requirements, Data model, Constraints, Deployment contract, Definition of done
- non-happy-path workflows: visitor_enquiry_is_stored_once_and_invalid_input_is_refused, embargoed_campaign_cannot_be_reached_before_release, publish_is_refused_until_every_gate_condition_holds, rival_account_job_is_denied_to_an_uncleared_creative, split_job_is_denied_unless_cleared_for_every_account, internal_comment_cannot_reach_the_client_view, legal_hold_lift_is_denied_to_a_producer, expired_talent_right_hides_the_campaign_in_that_market_only, departed_person_keeps_credits_and_invalid_credit_saves_are_refused, unauthenticated_studio_requests_are_denied_at_the_api
- checklist: 673 items, by kind {'capability': 121, 'constraint': 109, 'role': 44, 'literal': 162, 'ui': 177, 'contract': 48, 'data': 12}; traceability in `tests/traceability-matrix.md` and `.csv`

## Rubric

- judged criteria: 29 (25 positive, 4 negative)

| Dimension | Points | Share | Target |
|---|---|---|---|
| instruction_following | 18 | 0.327 | 0.30 |
| functionality | 12 | 0.218 | 0.25 |
| ux_flow | 7 | 0.127 | 0.15 |
| ui_visual | 11 | 0.200 | 0.15 |
| motion | 3 | 0.055 | 0.05 |
| accessibility | 3 | 0.055 | 0.05 |
| responsiveness | 1 | 0.018 | 0.05 |

## Literals ledger

`_handoff/E_sales_cont_agency-campaign-operations-vb_20260916_093701.literals-ledger.json` pins 210 literals (G6 green), by class: {'credential': 1, 'account': 10, 'status': 22, 'route': 12, 'endpoint': 46, 'number': 12, 'seed_record': 62, 'scheme': 4, 'env_var': 8, 'design_phrase': 26, 'motion_moment': 7}.

## Spec documents

| Doc | Fed |
|---|---|
| 00-decisions.md | draws, judgment calls, carry table, waivers |
| 01-PRD.md | Overview, User roles, Core features, Constraints |
| 02-TRD.md | Technical requirements, Deployment contract |
| 03-app-flow.md | User flow |
| 04-uiux-brief.md | UI/UX notes, Front-end specification |
| 05-backend-schema.md | Data model, Core features, API shapes |
| 06-implementation-plan.md | author-side only (variant b emits no build plan) |

## Grading window

```
VERDICT  PASS   (/Users/mac/Downloads/test/Output/E_sales_cont_agency-campaign-operations-vb_20260916_093701/instruction.md)
section        H2                chars  reference  flag
core_features  Core features     27097       2400  past-slice
user_flow      User flow          6885       1900  past-slice
ui_ux_notes    UI/UX notes        6621       1700  past-slice
constraints    Constraints        1151        800  over-reference
user_roles     User roles         3787       1000  past-slice
overview       Overview           1471        700  over-reference
joined total                     47012       8800  past-slice
first four                       41754       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```

## Kit gate log

| Gate | Tool | Exit | Verdict | Inputs hashed | stdout sha |
|---|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | 24 files | `e9c35c4fe1f6b759` |
| G1/G12 | `layout_lint.py` | 0 | PASS | 24 files | `9b5d14aaef4cc3d1` |
| G46 | `structure_lint.py` | 0 | PASS | 24 files | `d1300b716dada845` |
| G50 | `docker_lint.py` | 0 | PASS | 24 files | `380ed7d1c830de35` |
| G55 | `runtime_deps_lint.py` | 0 | PASS | 24 files | `a0c21dca8bc5f78a` |
| G63 | `secret_lint.py` | 0 | PASS | 24 files | `7edf90aadcadd1f7` |
| G48 | `truth_lint.py` | 0 | PASS | 24 files | `4d3d99ae56c3dc1d` |
| G51 | `source_lint.py` | 0 | PASS | 24 files | `dd6b6baf719b04e2` |
| G52 | `rubric_context_lint.py` | 0 | PASS | 24 files | `f63df51a455db761` |
| G54 | `comment_lint.py` | 0 | PASS | 24 files | `2c37e2940ba14fde` |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | 24 files | `76acf169889cc66d` |
| G11 | `leak_scan.py` | 0 | PASS | 24 files | `c3a399ac3dcd3fdf` |
| G33 | `window_lint.py` | 0 | PASS | 24 files | `dadd97611294adaf` |
| G4/G5 | `contract_lint.py` | 0 | PASS | 24 files | `5a8f88e10981d172` |
| G43 | `prescription_lint.py` | 0 | PASS | 24 files | `56979611c8648288` |
| G44 | `disclosure_lint.py` | 0 | PASS | 24 files | `9eaaa5264deb1df9` |
| G10 | `no_sdk_lint.py` | 0 | PASS | 24 files | `4d04647070f8ddf1` |
| G31 | `determinism_lint.py` | 0 | PASS | 24 files | `33d1264315dc44de` |
| G14 | `reward_path_lint.py` | 0 | PASS | 24 files | `deb61ade69f43dbf` |
| G27/G30 | `rubric_lint.py` | 0 | PASS | 24 files | `e35c6466177e0429` |
| G41 | `flag_lint.py` | 0 | PASS | 24 files | `24e0e0970da205f8` |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | 24 files | `cdf20c83e9056866` |
| G59/G60 | `codequality_lint.py` | 2 | ? | 24 files | `e23941dd85e0253b` |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | 24 files | `484905634df33709` |
| G6 | `fixture_lint.py` | 0 | PASS | 24 files | `5d300a87e22bd36e` |
| G24 | `coverage_map.py` | 0 | PASS | 24 files | `7b675a0c8a39ba0d` |
| G37 | `checklist_qc.py` | 0 | PASS | 24 files | `d9fc66dbd50a7ff7` |
| G39 | `rubric_align_lint.py` | 0 | PASS | 24 files | `7c12a56cf1f3be7f` |
| G28/G29 | `channel_lint.py` | 0 | PASS | 24 files | `4ae1cdf3ad8d6cc7` |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | 24 files | `4e5d77c60dd5e52e` |
| G0/INV5 | `vendor_check.py` | 0 | PASS | 24 files | `39a94bd22ce5f0e3` |
| G47 | `output_qc.py` | 0 | PASS | 24 files | `19b044aff531b266` |

## Prompt receipts (G40)

| Prompt | Gate | Verdict | Checks | FAIL | WARN | Verifier | Token |
|---|---|---|---|---|---|---|---|
| QC_instruction.md | G34 | PASS | 24 | 0 | 2 | independent subagent: QC brief and task code | `pr_bd78a247` |
| QC_spec.md | G34 | PASS | 15 | 0 | 0 | independent subagent: QC spec docs | `pr_28639285` |
| docker_generator.md | S5 | PASS | 0 | 0 | 0 | self | `pr_21fe0dbf` |
| generate_instruction.md | S2 | PASS | 0 | 0 | 0 | self | `pr_22b6b869` |
| pytest_generator.md | S7 | PASS | 0 | 0 | 0 | self | `pr_8f22a329` |
| qc_docker.md | G35 | FAIL | 105 | 1 | 0 | independent subagent: QC toml and docker | `pr_acda31af` |
| qc_rubric.md | G53 | PASS | 16 | 0 | 1 | independent subagent: QC rubric and checklist | `pr_18430b87` |
| qc_solution_checklist.md | G37 | PASS | 0 | 0 | 0 | independent subagent: QC rubric and checklist | `pr_ec9e2077` |
| qc_toml.md | G36 | PASS | 120 | 0 | 0 | independent subagent: QC toml and docker | `pr_662aefa2` |
| rubric_author.md | S8 | PASS | 0 | 0 | 0 | self | `pr_b38db40e` |
| solution_checklist.md | S3 | PASS | 0 | 0 | 0 | self | `pr_06960c3e` |
| task_code_verifier.md | G3 | PASS | 12 | 0 | 0 | independent subagent: QC brief and task code | `pr_75135e93` |
| toml_generator.md | S4 | PASS | 0 | 0 | 0 | self | `pr_1b356975` |

Findings behind each non-pass are recorded in `_handoff/E_sales_cont_agency-campaign-operations-vb_20260916_093701.receipts.json`.

Review history. Every certification prompt was run by an independent subagent, never by the author:

- QC_instruction: 4 cycles. Cycle 1 failed C2, C3 and D2; cycle 2 failed C4, the line heights added in the fix. The final state is WARN on C1 (display-only rules carry no negative case) and C7 (graded sections run past the judge's window, which the kit reports and never fails). Both were accepted.
- QC_spec: 5 cycles, ending PASS on all 15 checks.
- qc_rubric: run 1 ended in ABORT after 3 cycles (RC-13 motion share, RC-01 unclaimed asks). It was routed back to S3.5: the marquee and motion criteria were merged, split text moved to functionality, and a sustainability criterion added. Run 2 converged in 3 cycles to PASS on every check except RC-12 (exact pixel values graded by the judge), an accepted WARN.
- qc_solution_checklist: two runs; the adjudicated verdict is NEEDS REVIEW, with no gap or invention (see `_handoff/E_sales_cont_agency-campaign-operations-vb_20260916_093701.checklist-qc.md`).
- qc_toml: PASS after rubric_version was added.
- qc_docker: FAIL on CMP-004 only. The quay.io minio pin deviates from the reference/C Docker Hub pin, which no longer resolves; this is a kit fix.
- task_code_verifier: VALID.

## Handoff gates (undecided)

```
  STEP 0  build the reference app downstream from solution/checklist.md, then write solve.sh
          report any spec ambiguity found while building back to the author (plan 6.5.3)
  G13  docker build -f environment/Dockerfile environment/          expect exit 0
  G13  docker build -f tests/Dockerfile tests/                      expect exit 0 (needs deku-verifier-base:0.2)
  G15  docker compose -f environment/docker-compose.yaml up --wait  expect postgres, minio, minio-init healthy
  G19  harbor run -p Output/E_sales_cont_agency-campaign-operations-vb_20260916_093701 -a oracle                        expect reward == 1.0
  G19  harbor run -p Output/E_sales_cont_agency-campaign-operations-vb_20260916_093701 -a oracle                        expect reward == 1.0  (flakiness check)
  G18  read deployed from either oracle run                         expect deployed == 1.0
  G20  harbor run -p Output/E_sales_cont_agency-campaign-operations-vb_20260916_093701 -a nop                           expect reward == 0.0   -- above 0 is P0
  G21  apply fake-integration patch, re-run oracle                  expect reward  < 1.0
  G25  reviewer exploit sweep, reference library F                  expect 0 of 11 succeed
```

## Blocking findings

- None block the handoff gates.
- Kit defects recorded, not fixed here: the minio pin in reference/C C.2.1 no longer resolves on
  Docker Hub (qc_docker CMP-004); `stage-9-assemble.md` still asks for a `# syntax=` line that G50
  rejects; `tests/test.sh` looks for a `tests/instruction.md` the output contract retired;
  `generate_instruction.md` says enterprise keeps the row's role count while reference/B B.3 gives
  enterprise 3 to 5 roles.
