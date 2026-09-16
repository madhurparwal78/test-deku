# Build report - S_saasm_cont_spreadsheet-database-platform-vb_20260916_065044

## Identity

| | |
|---|---|
| Task code | `S_saasm_cont_spreadsheet-database-platform-vb_20260916_065044` |
| Task id | `deku/spreadsheet-database-platform-vb` |
| Cell | solo_founder / saas-micro-tools / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | backend = `postgres`, storage = `minio` |
| Variant | `b`, axes `critical_depth`, `spec_sections` (companion-backed, corpus-targets `companion_variant`) |
| Language | `typescript` |
| Design direction | `companion` (reference/L L.6.1); the bank draw `warm-hospitality` is recorded, not applied |
| Launch surface | `colour_contrast`, `cookie_choice`, `form_validation`, `no_broken_links`, `security_headers` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Vendored grader | 0.22.0 |
| Target schema | 1.4 |
| Verifier mode | `separate` |
| Aligned to kit | `806eb0a` (5 commits past `b3d0577`) |

## Alignment to kit 806eb0a

Built on kit `b3d0577`, then aligned to the five commits pulled at 15:31 on 2026-09-16:

| Commit | Change | Applied to this bundle |
|---|---|---|
| `1b99060` | `code_quality` joins the authored code-quality dimensions | nothing to apply: the rubric carries no `evaluation_target: source` criterion; G59/G60 NOT-APPLICABLE |
| `da24d3b` | pytest module renamed `test_output.py`; generated file becomes `test_ans.py` | `tests/test_pytest.py` renamed, the generated file regenerated under its new name, 40 workflow substep ids, `tests/Dockerfile`, both sidecars updated |
| `11eaf7b` | `[verifier].environment_mode = separate` by default | `task.toml` switched to `separate`; the grader runtime is kept in the agent image, which is legal and grades under either mode |
| `78e5ba6` | comment-stripped `test.sh`, grader pin re-minted | `tests/test.sh` re-vendored from `vendor/grader-0.22.0`; vendor_check passes |
| `806eb0a` | `solution/USER_README.md` restored as a GENERATED file | `recompute.py` re-vendored and re-run; the file now carries the seeded literals and the canary |

Receipts for the five prompts whose bytes changed (qc_toml, generate_instruction, toml_generator, pytest_generator, rubric_author) were re-reviewed against the diffs and re-minted. No check id was added or removed.

## Input

Task Order plus one companion document, the supplied product requirements document for
the reference spreadsheet-database product. The Task Order named `domain: saas-productivity`,
which is not a member of the closed enum; it resolved to `saas-micro-tools`, the enum member
the companion's own Section 26.6 describes as the nearest legal one. Recorded in
`_spec/<code>/00-decisions.md`.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Accounts, sessions, open reader signup | INCLUDED | Core features, Auth | pattern row roles author/reader, solo_founder opens signup |
| Route records with a draft boundary | INCLUDED | Core features rules 1-6 | the pattern's critical focus: unpublished content is not publicly readable |
| Four templates behind forty routes | INCLUDED | Core features rules 7-11 | companion Section 8, the graded workflow it names |
| The thirteen-section home route | INCLUDED | Core features rules 12-17 | companion Sections 7 and 24, measured copy |
| Shared chrome: bar, header, band, footer | INCLUDED | Core features rules 18-23 | companion Sections 5 and 19.3 |
| Media library in the object store | INCLUDED | Core features rules 24-28 | the storage slot; companion Section 25 |
| Free trial creating a team site | INCLUDED | Core features rules 29-33 | the Task Order's stated end state |
| Cookie consent and link integrity | INCLUDED | Core features rules 34-36 | drawn launch surface plus companion 22.2 C4 |
| The document model and storage | DROPPED | companion Section 11 | the product application on the second origin; companion 1.1 requires the split |
| The formula engine | DROPPED | companion Section 12 | same, and companion 26.6 says it would carry a different pattern |
| Access rules | DROPPED | companion Section 13 | same |
| Collaboration and the action log | DROPPED | companion Section 14 | same |
| Forms and anonymous ingestion | DROPPED | companion Section 15 | same |
| The assistant under access rules | DROPPED | companion Section 16 | same |
| Automations and the public interface | DROPPED | companion Section 17 | same |
| Self-hosting, tenancy and billing | DROPPED | companion Section 18 | same |

Every DROPPED row is declared to G51 with `--waive`, so the decision is in the gate receipt
as well as here. G51 reports 145 of 145 topics and 454 of 454 enumerated items carried or
declared, and 14 of 14 measured colours described in the brief by family and tone.

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| backend | `postgres` | MET | `test_route_rows_are_persisted_and_survive_a_reload` (critical), `test_seeded_accounts_and_routes_are_stored_once` |
| storage | `minio` | MET | `test_uploaded_file_lands_in_the_bucket_at_its_scheme_key` (critical), `test_draft_attachment_is_not_publicly_readable` (critical) |

## Grading layer

| | |
|---|---|
| Workflows | 16 (band 10 to 16) |
| Browser substeps | 19 |
| pytest substeps | 40 |
| Critical substeps | 11 |
| Non-happy-path ids | 8: `draft_route_denied_to_a_reader`, `reader_cannot_publish_a_route`, `reader_cannot_upload_an_image`, `draft_attachment_denied_to_the_public`, `concurrent_team_names_leave_at_most_one_trial`, `duplicate_trial_submission_writes_nothing_new`, `invalid_trial_input_is_refused`, `trial_signup_list_is_forbidden_to_a_reader` |
| pytest modules | one, `tests/test_output.py`, 40 test functions |
| Sections covered | core features, data integrity, authorization, edge cases, storage, presentation |

Substep categories: `business_rule` 9, `core_outcome` 3, `data_integrity` 8, `presentation` 4, `security` 11, `validation` 5.

## Rubric

17 judged criteria, 16 positive and 1 negative, generated
from `solution/trinity/grounding.yaml` by the vendored `recompute.py`.

| Dimension | Share | Target band | Criteria |
|---|---|---|---|
| `instruction_following` | 0.294 | 0.30 | 4 |
| `functionality` | 0.235 | 0.25 | 2 |
| `ux_flow` | 0.118 | 0.15 | 2 |
| `ui_visual` | 0.235 | 0.15 | 4 |
| `motion` | 0.029 | small | 1 |
| `accessibility` | 0.059 | small | 2 |
| `responsiveness` | 0.029 | small | 1 |

The reference rubric in `solution/trinity/rubrics.json` carries 10 items at a
compiled weight share of 0.925, above the 0.60 floor G48 enforces.

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Core features | 14003 | 2400 | past-slice |
| User flow | 4784 | 1900 | past-slice |
| UI/UX notes | 9082 | 1700 | past-slice |
| Constraints | 901 | 800 | over-reference |
| User roles | 2004 | 1000 | over-reference |
| Overview | 3130 | 700 | past-slice |
| **joined** | **33904** | 8800 | past-slice |

Length is reported, never failed. `## Core features` runs long because the companion
states 36 numbered rules the brief carries in full; the tail reaches the agent and stops
reaching the judge, and the judged criteria are self-contained and carry their own
`evaluation_rule`, so nothing on the reward path is lost. Recorded as QC_instruction C7 WARN.

## Literals ledger

| Class | Count |
|---|---|
| `account` | 3 |
| `credential` | 1 |
| `design_phrase` | 4 |
| `env_var` | 8 |
| `motion_moment` | 4 |
| `number` | 5 |
| `route` | 14 |
| `scheme` | 2 |
| `seed_record` | 6 |
| `status` | 60 |
| **total** | **107** |

One entry is `verifier_only`: `DB_ADMIN_URL`, carried by `task.toml` `[verifier].env`
alone and absent from the brief and from `[environment].env` (INV4). Every other entry
appears verbatim in `instruction.md` and in at least one grader file; `fixture_lint.py`
checks the bijection in both directions.

## Authoring documents

| Document | Fed |
|---|---|
| `_spec/<code>/00-decisions.md` | the draws, the residual calls, the companion carry table, the G51 waiver list |
| `_spec/<code>/01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `_spec/<code>/02-TRD.md` | `## Technical requirements` |
| `_spec/<code>/03-app-flow.md` | `## User flow` |
| `_spec/<code>/04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `_spec/<code>/05-backend-schema.md` | `## Data model`, `## User roles` |
| `_spec/<code>/06-implementation-plan.md` | nothing in the brief; `## Build plan` is not baseline |

The folder sits beside the bundle, never inside it (CON-5).

## Kit gate log

Rendered from `_handoff/<code>.gates.jsonl`. Each row carries the tool's own exit code
and the SHA-256 of every file it read. No verdict below was transcribed.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 2 | NOT-APPLICABLE |
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

## Handoff gates, undecided

G13, G15, G18, G19, G20, G21 and G25 need Docker and the harness, which this kit does
not have. Commands and expected verdicts are in `<code>.handoff.md`.

## Blocking findings

1. `task.toml` carries no `[delivery]` block. `[delivery.images]` requires a real
   `@sha256:` manifest-list digest per image and reference/C section C.4 forbids a
   fabricated one; this run had no registry access, so the block was omitted rather than
   invented. `validate_task.py` grandfathers the absence at exit 2. The operator resolves
   three digests and adds it.
2. Thirteen brief obligations are stated and graded by no channel, so they are absent from
   `solution/checklist.md` rather than carried as items no grader cites: the two stack-name
   asks, the two absent-service asks, the structured-logging ask, `/app/USER_README.md`,
   the two reserved directories, the production-build ask, and the four App Contract
   negatives about copying a backing service, edge functions, volumes and container names.
   Each is unobservable through HTTP, the database or the object store, and G10 forbids a
   reward-bearing test from reading the agent's source. This is OPEN-DECISIONS D-H,
   recorded here rather than closed by a fabricated citation.
3. G40 is WARN, not PASS: owner and verifier are the same agent. See the handoff contract.

## Budget

`turns_expected = 170`, `tokens_expected = 7000000`: the documented hard band. A
companion-backed variant `b` carries a whole measured product as input, the brief states
36 numbered core rules across nine feature groups, and the build spans a content model, an
authoring console, an object store and a contention-safe signup. `difficulty` stays the
empty string; calibration writes it, never the author.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

Not admissible. The bundle carries no reference app. It becomes admissible when the app is
built downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
