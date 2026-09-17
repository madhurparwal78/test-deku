# Build report - E_healthc_crud_clinical-records-platform-vb_20260916_075848

Rendered from `_handoff/<project>.gates.jsonl` and `_handoff/<project>.receipts.json`.
No verdict in this file was typed by hand.

## Identity

| Field | Value |
|---|---|
| task code | `E_healthc_crud_clinical-records-platform-vb_20260916_075848` |
| task id | `deku/clinical-records-platform-vb` |
| cell | enterprise / healthcare-clinical / crud-catalog |
| archetype | `clinical-records-platform` |
| variant | `b`, axes `critical_depth` and `spec_sections` |
| service_profile | `P1-db` |
| providers | `backend` = `postgres` (PostgreSQL 16.4) |
| language | typescript |
| capability_flags | `aesthetic` |
| design_direction | `companion` (reference/L L.6.1; the bank draw `glass-depth` is recorded and does not govern) |
| launch_surface | `meta_tags,no_broken_links,page_view_log,security_headers,social_preview` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| grader_version | 0.22.0 (vendored, byte-identical) |
| shard | 1 of 1 |

## Derived-design draws

Digest identity is `[metadata].archetype`; SHA-256 at the documented byte offsets.

```
draw: render_model = ssr-islands
draw: backend = Express
draw: frontend = SvelteKit
draw: design_direction = companion
draw: nav = sidebar-nav
draw: work_surface = card-grid
draw: create_flow = inline-row
draw: feedback = full-page-confirmation
draw: launch_surface = meta_tags,no_broken_links,page_view_log,security_headers,social_preview
```

## Kit gate log

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

32 of 32 gate rows green. `codequality_lint.py` returns NOT-APPLICABLE: the bundle declares no `evaluation_target: "source"` criterion, which is a legal state and is reported rather than passed silently.

## QC prompt receipts

| Prompt | Gate | Verdict | Checks answered | Findings |
|---|---|---|---|---|
| `QC_spec.md` | G34 | PASS | 15 | 4 |
| `QC_instruction.md` | G34 | PASS | 24 | 4 |
| `qc_toml.md` | G36 | PASS | 120 | 2 |
| `qc_docker.md` | G35 | PASS | 105 | 2 |
| `qc_solution_checklist.md` | G37 | PASS | 0 | 0 |
| `task_code_verifier.md` | G3 | VALID | 12 | 0 |
| `generate_instruction.md` | S2 | PASS | 0 | 1 |
| `solution_checklist.md` | S3 | PASS | 0 | 1 |
| `toml_generator.md` | S4 | PASS | 0 | 1 |
| `docker_generator.md` | S5 | PASS | 0 | 1 |
| `pytest_generator.md` | S7 | PASS | 0 | 1 |
| `rubric_author.md` | S8 | PASS | 0 | 1 |
| `qc_rubric.md` | G53 | PASS | 16 | 0 |

Every certification prompt was read and answered check by check; the seven carry 292 declared checks between them. `verifier: self` on every row: owner and verifier are the same agent in this run, so each verdict is **SELF-ATTESTED** and recorded as such rather than claimed as independent.

### Non-PASS checks, with their findings

**`QC_spec.md`**

- `B1` WARN - 05-backend-schema.md declares five roles (clinician, front_desk, biller, patient, plus a second clinician account) against the crud-catalog row's single `user`. Recorded as a deliberate call in 00-decisions.md: row-level authorization by relationship is the companion's core subject and the enterprise category's defining character.
- `S10` WARN - the front desk account is seeded at frontdesk@example.com rather than front_desk@example.com, so the address drops the underscore the role name carries. Every other seeded address follows <role>@example.com and the password is the corpus literal.
- `S2` WARN - 01-PRD.md lists twelve must-have features against the prompt's 3-6 band, which generate_instruction.md widens to 6-10 for a companion-backed task. The companion states twelve product areas and dropping six of them would drop the task; recorded rather than trimmed.
- `S5` WARN - 04-uiux-brief.md states motion as character (one entrance, one transition duration on one curve, the scroll offset) rather than as literal millisecond and cubic-bezier values, and states no minimum touch-target size. The settled number rule in generate_instruction.md section 4 forbids those values in the brief; the spec doc follows the brief so the two cannot drift.

**`QC_instruction.md`**

- `A2` WARN - the framing paragraph names a multi-part outcome (read the project site, copy a release digest, then open, document, code, order and sign an encounter) rather than one. The parts are one continuous journey through both halves of the product, and splitting them would describe only one half.
- `B1` WARN - the brief declares five roles against the crud-catalog row's single `user`. Same deliberate call as QC_spec B1, recorded in 00-decisions.md.
- `B3` WARN - `## Build plan` is absent. generate_instruction.md section 2.1 removes it from the baseline emission (6 of 6 shipped reference briefs omit it), so two of the three levers are present by design. Cited rather than repaired: the prompt predates that change.
- `C7` WARN - `## Core features` runs about 27,000 characters against the 2,400 reference point, and the joined six sections run about 47,000 against 8,800. window_lint (G33) reports the overrun and fails nothing; the tasker instructed that the per-section and joined ceilings be set aside so the UI and UX requirements could be written out in full. Content past the slice reaches the agent and not the judge.

**`qc_toml.md`**

- `BENCH-002` NOT-APPLICABLE
- `BENCH-003` NOT-APPLICABLE
- `BENCH-005` NOT-APPLICABLE
- `INST-007` NOT-APPLICABLE
- `SCHEMA-011` WARN - `[delivery]` and `[delivery.images]` are emitted and the prompt's section 11 template does not carry them. 01-OUTPUT-CONTRACT.md CON-2 requires `[delivery]` on every new bundle and validate_task.py checks it, so the template is the stale side. `[delivery.images]` is omitted because no image digest is resolvable offline.
- `SCHEMA-013` WARN - `[delivery]` sits between `[verifier]` and `[[artifacts]]`, a position the prompt's canonical order does not describe because the section postdates it. Same cause as SCHEMA-011.
- `SIGN-001` NOT-APPLICABLE
- `SIGN-002` NOT-APPLICABLE
- `SIGN-003` NOT-APPLICABLE
- `TAX-008` NOT-APPLICABLE
- `VERIF-007` NOT-APPLICABLE

**`qc_docker.md`**

- `ARCH-002` NOT-APPLICABLE
- `ARCH-003` NOT-APPLICABLE
- `CMP-011` WARN - the `main` service sets `ports: 4173:4173`. CMP-022 and docker_generator C12 REQUIRE `main` to carry `ports` and `extra_hosts`; the no-published-ports rule is a sidecar rule, and the postgres sidecar publishes none. The two rows contradict each other and the newer C12 rule governs.
- `CMP-020` WARN - `main` carries `ports` and `extra_hosts` beyond `depends_on`. Required by CMP-022 and docker_generator C12; without `extra_hosts` the agent's first completion fails on name resolution and the trial is lost rather than scored.
- `DEP-011` NOT-APPLICABLE
- `DEP-017` NOT-APPLICABLE

## Feature resolution

| Feature | Verdict | Reason |
|---|---|---|
| Public project site: home, downloads, demo, support, news, modules, contribute, privacy | INCLUDED | companion section 'Site map'; every route pinned in `## User flow` |
| Accounts and sessions, seeded only | INCLUDED | enterprise category modifier closes signup; the companion refuses self-registration |
| Patient register, identifiers, matching, merge | INCLUDED | companion 'Identity'; twins and the merged pair are seeded |
| Appointment book with contention | INCLUDED | companion 'The appointment book'; the store refuses the second booking |
| Encounter, note versioning, signing | INCLUDED | the Task Order's own sentence; the core outcome |
| Results, corrections, reconciliation queue | INCLUDED | companion 'Orders and results', observable half only |
| Prescribing, allergies, the unnamed conflict | INCLUDED | companion 'Prescribing' |
| Coverage, eligibility, claims, remittance, ledger | INCLUDED | companion 'Coverage, eligibility and the claim' and 'Money' |
| Authorization by relationship, uniform not-found, filtered counts | INCLUDED | companion 'Access is a relationship' and 'Filtering must not leak through arithmetic' |
| Audit record, read through the patient access log | INCLUDED | companion 'The audit record'; observed without a fifth staff role |
| Patient portal, release by default, requests | INCLUDED | companion 'The patient portal' |
| Worklists with owner, age and recorded outcome | INCLUDED | companion 'Worklists' |
| Wire message format for laboratory and clearing-house traffic | DROPPED | a positional message grammar is observable through no declared channel; the observable half is kept |
| Bulk population export | DROPPED | a product of its own; the Task Order names none of it |
| Third-party application authorization | DROPPED | as above |
| De-identified research extract | DROPPED | as above |
| Decision-support rules and quality measurement | DROPPED | as above |
| Object storage for attachments | DROPPED | `P1-db` declares no storage slot; nothing in this build uploads a file |
| Email and SMS notification | DROPPED | no email slot declared; every acknowledgement is on the screen |

## Slot obligations

| Slot | Provider | Observed by | Status |
|---|---|---|---|
| backend | postgres | `test_output.py::test_seeded_records_are_persisted`, `::test_two_simultaneous_bookings_leave_exactly_one_appointment`, `::test_signing_locks_releases_and_queues` | MET |

## Grading surface

| Measure | Value |
|---|---|
| workflows | 23 (enterprise band 13-23) |
| browser substeps | 74 |
| pytest substeps | 89 |
| browser:pytest ratio | 0.83 (G45 band 0.40-2.00) |
| critical substeps | 39 |
| non-happy-path workflow ids | 8: `unauthenticated_request_is_denied_at_the_api`, `concurrent_bookings_leave_one_appointment`, `signed_note_cannot_be_edited`, `draft_note_is_forbidden_to_another_clinician`, `duplicate_result_is_recorded_once`, `prescriber_is_warned_without_the_conflicting_entry_named`, `unbalanced_remittance_is_invalid`, `unrelated_clinician_cannot_find_the_chart` |
| pytest module | one, `tests/test_output.py`, 89 test functions |
| rubric criteria | 23 (21 positive, 2 negative) |
| checklist items | 494 |
| ledger literals | 182 |

### Rubric dimension shares, over positive scores

| Dimension | Criteria | Share | Target |
|---|---|---|---|
| instruction_following | 6 | 0.34 | 0.30 |
| functionality | 5 | 0.25 | 0.25 |
| ux_flow | 3 | 0.15 | 0.15 |
| ui_visual | 3 | 0.12 | 0.15 |
| motion | 2 | 0.07 | 0.05 |
| accessibility | 2 | 0.07 | 0.05 |
| responsiveness | 0 | 0.00 | 0.05 |

## Coverage

- 494 checklist items, every one cited: pytest 384 citations across 89 tests, 114 browser-substep citations, 35 rubric citations across 23 criteria.
- 35 judgment-class (`ui`) obligations, all 35 graded by the rubric and by nothing else (G28 rule 3).
- `tests/traceability-matrix.md` and `.csv` are regenerated by every sweep from the same scan G24 makes.

## Literals ledger

| Class | Count |
|---|---|
| account | 6 |
| credential | 2 |
| env_var | 7 |
| number | 20 |
| route | 19 |
| scheme | 1 |
| seed_record | 54 |
| status | 73 |

4 entries are `verifier_only` and carry `task.toml` alone as their carrier (INV4): they never reach `instruction.md` or `[environment].env`.

## spec/ documents and where each one fed

| Document | Fed |
|---|---|
| `00-decisions.md` | the draws, the residual calls and the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements`, and `environment/Dockerfile` through S5 |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at baseline |

## Grading window

| Section | Chars | Reference |
|---|---|---|
| Core features | 27087 | 2400 |
| User flow | 4374 | 1900 |
| UI/UX notes | 9363 | 1700 |
| Constraints | 1349 | 800 |
| User roles | 3520 | 1000 |
| Overview | 2120 | 700 |

Every judged section runs past its reference point, and the joined six run past the 9,000-character slice. `window_lint.py` (G33) reports this and fails nothing: the brief carries no length limit. The tasker instructed that the per-section and joined ceilings be set aside so the UI and UX requirements could be written out in full. Content past the slice reaches the agent in full; it stops reaching the judge, which costs a diagnostic number and no reward.

## Blocking findings

NONE. No spec gap and no harness gap prevented a required test. Every declared slot is MET, every `ui` obligation is graded, and no check was recorded UNMET.

## Versions

| Field | Value |
|---|---|
| kit | deku-green-field, revision of 2026-09-16 |
| vendored grader | 0.22.0 |
| target schema | 1.4 |
| verifier mode | separate |
| harbor_version | 0.20.0 |

## Budget

`turns_expected = 180`, `tokens_expected = 6500000`. Reasoning: the product is two surfaces under one codebase, nineteen public and workspace routes, twenty-eight tables and one signing transaction that has to hold three effects together. That is above the corpus median and below the 8,000,000 ceiling, and it sits one step above the `qualitative-fieldwork-agency` bundle, which carried 165 turns for a smaller data model.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference application. Nothing here counts toward corpus targets until the app is built downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
