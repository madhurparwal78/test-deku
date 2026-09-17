# Build report - S_commu_book_community-drive-planner-vb_20260916_053722

## Identity

| | |
|---|---|
| Task code | `S_commu_book_community-drive-planner-vb_20260916_053722` |
| Task id | `deku/community-drive-planner-vb` |
| Product | Waze Live Map |
| Cell | solo_founder / community-social / booking-scheduling |
| Archetype | `community-drive-planner` |
| Variant | `b`, axes `critical_depth`, `spec_sections` (a companion document was supplied) |
| Service profile | `P1-db` |
| Providers per slot | `backend` = `postgres` |
| Language | `python` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 (no device sharding configured) |
| Kit | deku-green-field, gate index G0..G63 |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Companion | `prd/waze_prd.md`, 1,141 lines, 41 sections |

## Derived-design draws

Every draw is SHA-256 over the archetype `community-drive-planner` (reference/L §L.4).

| Axis | Value |
|---|---|
| `render_model` | `mpa-progressive` |
| `backend` | FastAPI + Jinja |
| `frontend` | HTMX + server templates |
| `design_direction` | `companion` (the draw returned `brutalist-utility`; reference/L §L.6.1 hands the axis to the measured product) |
| `nav` | `sidebar-nav` |
| `work_surface` | `split detail-pane` |
| `create_flow` | `slide-over` |
| `feedback` | `full-page-confirmation` |
| `launch_surface` | `custom_404`, `page_view_log`, `security_headers`, `social_preview`, `spam_protection` |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Full viewport live tile map | INCLUDED | `## Core features` rules 4-7 | companion §7, the product's subject |
| Endpoint search with suggestions and swap | INCLUDED | rules 8-11 | companion §8 |
| Live road conditions coloured by drivers | INCLUDED | rules 12-14 | the Task Order's own wording; companion §9 |
| Community reporting and crowd verification | INCLUDED | rules 15-19 | companion §1, §16 observable half |
| Routing over the live graph | INCLUDED | rules 20-24 | companion §8, §24, §35 |
| Leave time scheduler | INCLUDED | rules 25-27 | the critical focus; companion §8 |
| Planned drives and the set-off reminder | INCLUDED | rules 28-32 | the Task Order's own ask |
| Global chrome and content routes | INCLUDED | rules 33-39 | companion §5, §11, §38 |
| Accounts | INCLUDED | `### Auth` rules 1-3 | solo_founder opens signup |
| Page-view record, security headers, social preview, bot refusal | INCLUDED | rules 40-41, `## Technical requirements` | drawn launch surface |
| Mobile turn-by-turn client, voice, offline regions | DROPPED | `## Constraints` | companion §15-20; the Task Order scopes this task to the open web |
| Telemetry ingestion, map matching, ML traffic, map data platform | DROPPED | `## Constraints` | companion §21-34, marked reconstructions by its own §40 |
| Advertising, partner exchange, carpool, chat, social graph | DROPPED | `## Constraints` | companion §18-20, §30-31 |

## Slot obligations

| Slot | Provider | Status | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_seeded_rows_persisted_and_idempotent_after_restart`, `test_planned_drive_is_persisted_with_solved_window`, `test_page_view_row_stored_for_each_public_route` assert real rows through `capabilities.make_backend()`; G32 green |

No other slot is declared, so none is owed.

## Grading layer

| | |
|---|---|
| Workflows | 16 (solo_founder band 10-16) |
| Browser substeps | 15 |
| pytest substeps | 37 |
| `critical` substeps | 7 |
| Non-happy-path workflow ids | 7: `concurrent_overlapping_windows_admit_at_most_one`, `visitor_cannot_report_or_save_a_drive`, `driver_cannot_reach_another_drivers_rows`, `stale_session_cannot_mutate`, `invalid_drive_and_report_input_is_refused`, `empty_state_reads_cleanly`, `duplicate_form_submissions_are_refused` |
| pytest module | one, `tests/test_pytest.py`, 37 test functions |
| Sections covered | core features, data integrity, authorization, edge cases |
| Checklist items | 188 across 10 section codes |
| Rubric criteria | 17 (13 positive, 4 negative) |

`critical` appears only in `tests/workflows.yaml`, which S6 owns; the pytest layer emits
no scoring field of any kind.

### Rubric dimension shares, positives only

| Dimension | Points | Share | Target | Within 0.10 |
|---|---|---|---|---|
| `instruction_following` | 10 | 0.303 | 0.30 | yes |
| `functionality` | 8 | 0.242 | 0.25 | yes |
| `ux_flow` | 4 | 0.121 | 0.15 | yes |
| `ui_visual` | 7 | 0.212 | 0.15 | yes |
| `motion` | 2 | 0.061 | 0.05 | yes |
| `accessibility` | 1 | 0.030 | 0.05 | yes |
| `responsiveness` | 1 | 0.030 | 0.05 | yes |

## Literals ledger

124 pinned values, every one verified present in `instruction.md`.

| Class | Count | Values |
|---|---|---|
| `account` | 3 | `driver2@example.com`, `driver3@example.com`, `driver@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `design_phrase` | 16 | `Baloo 2`, `Gotham Rounded`, `Noto Sans`, `Quicksand`, `Rubik`, `Waze Boing`, `breathes around it`, `comfortable on the map and compact in the rail` ... |
| `endpoint` | 11 | `/api/auth/login`, `/api/auth/signup`, `/api/drives`, `/api/health`, `/api/page-views`, `/api/places`, `/api/places/reverse`, `/api/reminders` ... |
| `env_var` | 3 | `APP_PUBLIC_PORT`, `APP_PUBLIC_URL`, `DATABASE_URL` |
| `motion_moment` | 13 | `events-user-location-pulse`, `fade-in`, `fade-out`, `jam-dash-animation-1`, `location-pulse`, `map-marker-pulse`, `overlay-spin`, `rcTriggerZoomIn` ... |
| `number` | 10 | `100 percent`, `15 minute lead`, `150 percent`, `180 minutes`, `250 percent`, `27 minutes`, `3 minutes`, `5 minute buffer` ... |
| `route` | 14 | `/412`, `/416`, `/417`, `/419`, `/as`, `/drives`, `/gs`, `/login` ... |
| `scheme` | 18 | `/row-tiles/live/base/{z}/{x}/{y}`, `28.459 | 77.025`, `Choose destination`, `Choose starting point`, `Don't have Waze yet?`, `Driving directions`, `Edit your arrival time`, `Find the best time to
leave, so you get to your destination on time` ... |
| `seed_record` | 17 | `2026-09-17T08:13:00Z`, `2026-09-17T08:28:00Z`, `2026-09-17T09:00:00Z`, `Akshardham Temple`, `Amrita Bose`, `Barapullah Elevated`, `Connaught Place`, `Cyber Hub Gurugram` ... |
| `status` | 18 | `active`, `canceled`, `carpool`, `clear`, `closure`, `completed`, `confirm`, `crash` ... |

No value is `verifier_only`: this bundle declares one slot and its admin credential
(`DB_ADMIN_URL`) lives in `[verifier].env` alone, never on the ledger and never in the brief.

## Authoring documents

`spec/` is authoring-side and ships nowhere near the bundle. It lives at
`Output/16sept-waze/_spec/S_commu_book_community-drive-planner-vb_20260916_053722/`.

| Doc | Fed |
|---|---|
| `00-decisions.md` | the audit trail, the eight `draw:` lines G49 reads, and the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles`, the API shapes table |
| `06-implementation-plan.md` | nothing: `## Build plan` is not emitted at baseline |

## Grading window

```
VERDICT  PASS   (C:/Users/Admin/Desktop/gen_-kit/Output/16sept-waze/S_commu_book_community-drive-planner-vb_20260916_053722\instruction.md)
section        H2                chars  reference  flag
core_features  Core features     13721       2400  past-slice
user_flow      User flow          4691       1900  past-slice
ui_ux_notes    UI/UX notes        4159       1700  past-slice
constraints    Constraints        1645        800  over-reference
user_roles     User roles         1665       1000  over-reference
overview       Overview           2037        700  over-reference
joined total                     27918       8800  past-slice
first four                       24216       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```

The brief has no length limit (`generate_instruction.md` §4). `past-slice` marks prose the
judge does not read; the agent receives it in full, and `judge_score` never touches reward.

## Kit gate log

Rendered from `_handoff/S_commu_book_community-drive-planner-vb_20260916_053722.gates.jsonl`. Each row carries the SHA-256 of every input
byte the tool examined. No verdict in this table was transcribed.

| Gate | Tool | Exit | Verdict | Elapsed |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | 0.14s |
| `G1/G12` | `layout_lint.py` | 0 | PASS | 0.10s |
| `G46` | `structure_lint.py` | 0 | PASS | 0.11s |
| `G50` | `docker_lint.py` | 0 | PASS | 0.09s |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | 0.13s |
| `G63` | `secret_lint.py` | 0 | PASS | 0.10s |
| `G48` | `truth_lint.py` | 0 | PASS | 0.36s |
| `G51` | `source_lint.py` | 0 | PASS | 0.12s |
| `G52` | `rubric_context_lint.py` | 0 | PASS | 0.10s |
| `G54` | `comment_lint.py` | 0 | PASS | 0.10s |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | 0.09s |
| `G11` | `leak_scan.py` | 0 | PASS | 0.11s |
| `G33` | `window_lint.py` | 0 | PASS | 0.09s |
| `G4/G5` | `contract_lint.py` | 0 | PASS | 0.10s |
| `G43` | `prescription_lint.py` | 0 | PASS | 0.13s |
| `G44` | `disclosure_lint.py` | 0 | PASS | 0.10s |
| `G10` | `no_sdk_lint.py` | 0 | PASS | 0.11s |
| `G31` | `determinism_lint.py` | 0 | PASS | 0.12s |
| `G14` | `reward_path_lint.py` | 0 | PASS | 0.09s |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | 0.10s |
| `G41` | `flag_lint.py` | 0 | PASS | 0.12s |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | 0.10s |
| `G59/G60` | `codequality_lint.py` | 2 | ? | 0.11s |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | 0.14s |
| `G6` | `fixture_lint.py` | 0 | PASS | 0.14s |
| `G24` | `coverage_map.py` | 0 | PASS | 0.14s |
| `G37` | `checklist_qc.py` | 0 | PASS | 0.12s |
| `G39` | `rubric_align_lint.py` | 0 | PASS | 0.12s |
| `G28/G29` | `channel_lint.py` | 0 | PASS | 0.12s |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | 0.12s |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | 0.12s |
| `G47` | `output_qc.py` | 0 | PASS | 0.14s |

**ALL GATES GREEN.** `G59/G60` exits 2, NOT-APPLICABLE: this bundle ships the product half
of `tests/rubric.json` and no `evaluation_target: "source"` criterion, because the vendored
`recompute.py` renders `judged_criteria` only. That is the legal state `stage-3.6-overlays.md`
names, and it is reported rather than silently passed.

`G40` exits 0 with WARN. Every certification prompt carries a current, bundle-bound receipt
answering its whole registry; the WARN records that owner and verifier are one agent.

### Certification prompt scorecards

Self-attested: G3 (task_code_verifier.md), G34 (QC_instruction.md), G34 (QC_spec.md), G35 (qc_docker.md), G36 (qc_toml.md), G37 (qc_solution_checklist.md), G53 (qc_rubric.md).

Non-PASS checks, every one with a recorded finding in
`_handoff/S_commu_book_community-drive-planner-vb_20260916_053722.receipts.json`:

| Gate | Prompt | Check | Verdict |
|---|---|---|---|
| `G34` | `QC_instruction.md` | `A1` | WARN |
| `G34` | `QC_instruction.md` | `B3` | WARN |
| `G34` | `QC_instruction.md` | `C1` | WARN |
| `G34` | `QC_instruction.md` | `C5` | WARN |
| `G34` | `QC_instruction.md` | `C7` | WARN |
| `G34` | `QC_spec.md` | `S2` | WARN |
| `G34` | `QC_spec.md` | `S5` | WARN |
| `G35` | `qc_docker.md` | `CMP-011` | WARN |
| `G35` | `qc_docker.md` | `CMP-020` | WARN |
| `G53` | `qc_rubric.md` | `RC-01` | WARN |
| `G53` | `qc_rubric.md` | `RC-12` | WARN |
| `G36` | `qc_toml.md` | `SCHEMA-011` | WARN |
| `G36` | `qc_toml.md` | `SCHEMA-013` | WARN |

## Corpus-level gates

| Gate | Verdict | Note |
|---|---|---|
| G42 `corpus_overlap.py` | NOT-APPLICABLE | one bundle in this output root; a cross-archetype comparison needs two. Not a pass |
| G49 `diversity_lint.py` | NOT-APPLICABLE | same cause. The eight `draw:` lines are recorded and will be read once a second bundle lands |
| G26 / G61 `corpus_report.py` | FAIL, advisory | payments-or-email share 0.0% against a 28% floor. `booking-scheduling` mandates neither slot, so this is a corpus composition target the tasker meets by minting other cells, not a defect in this bundle |

## Blocking findings

None in the bundle. Two standing conditions, recorded rather than papered over:

1. `[delivery.images]` is omitted. Every value there must be a `@sha256:` digest present in
   `environment/`, and a digest cannot be resolved without a registry, which the kit has no
   access to. `validate_task.py` accepts the omission; the harness operator fills the block
   when the images are first built. Fabricating a digest would fail at `docker compose up`,
   which is a lost trial rather than a scored zero.
2. The corpus mix gate above.

## Budget

`turns_expected = 200`, `tokens_expected = 7000000`. Raised above the Standard tier defaults
because the companion licenses 6-10 must-have features (reference/G §G.2.1) and this brief
carries nine plus the drawn launch surface: ten graded feature groups, a derived road-condition
model, a solved leave time and a contended departure window. `reference/G` §G.2.1 is explicit
that the cost of a raised feature cap shows up here rather than in the brief's length.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference app. Nothing counts toward corpus targets
until the app lands downstream and `harbor run -a oracle` returns `1.0` twice.
