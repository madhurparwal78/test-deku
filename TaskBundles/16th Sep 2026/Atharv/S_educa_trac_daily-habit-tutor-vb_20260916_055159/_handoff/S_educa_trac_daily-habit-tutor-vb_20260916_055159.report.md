# Build report: S_educa_trac_daily-habit-tutor-vb_20260916_055159

Rendered from `_handoff/S_educa_trac_daily-habit-tutor-vb_20260916_055159.gates.jsonl` and `_handoff/S_educa_trac_daily-habit-tutor-vb_20260916_055159.receipts.json`. No verdict in this file was typed by hand.

## Identity

| | |
|---|---|
| Task code | `S_educa_trac_daily-habit-tutor-vb_20260916_055159` |
| Task id | `deku/daily-habit-tutor-vb` |
| Product | Larkwise |
| Cell | `solo_founder` / `education-courses` / `tracker-log` |
| Service profile | `P1-db`, one slot: `backend = postgres` |
| Variant | `b`, axes `critical_depth`, `spec_sections` (a companion document was supplied) |
| Language | `typescript` |
| Design direction | `companion` (reference/L L.6.1; the draw was `playful-consumer` and does not govern) |
| Launch surface | `colour_contrast, mobile_viewport, no_broken_links, social_preview, terms_page` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field, `Output/` root from `config/kit-config.yaml` |
| Vendored grader | `0.22.0` (INV5) |
| Target schema | `1.4` |
| Companion | `duolingo_prd.md`, 4,336 lines, 43 sections |

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference app (D20). It becomes admissible only
when the app is built downstream from `solution/checklist.md` and `harbor run -a oracle`
returns `1.0` twice.

## Kit gate log

One row per receipt, verbatim from the sweep. The `inputs` hashes in the receipt file bind
each row to the bytes it examined.

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

`G2/G16` reports NOT-APPLICABLE because `task.toml` carries no `[delivery]` block, which is
grandfathered by the validator. `G59/G60` reports NOT-APPLICABLE because the bundle ships no
code-quality rubric. Both are recorded, never rewritten as PASS.

## Prompt receipts

| Prompt | Gate | Verdict | Checks answered | Findings |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | 3 |
| `QC_spec.md` | G34 | PASS | 15 | 0 |
| `qc_docker.md` | G35 | PASS | 105 | 2 |
| `qc_rubric.md` | G53 | PASS | 16 | 0 |
| `qc_solution_checklist.md` | G37 | PASS | 0 | 0 |
| `qc_toml.md` | G36 | PASS | 120 | 0 |
| `task_code_verifier.md` | G3 | VALID | 12 | 0 |

Every one is SELF-ATTESTED: a single agent authored and reviewed. The kit's rule is
owner != verifier, so these are recorded verdicts, never independent ones. The four
generator prompts (`generate_instruction.md`, `toml_generator.md`, `docker_generator.md`,
`pytest_generator.md`, `rubric_author.md`, `solution_checklist.md`) carry no receipt and are
reported UNCITED by G40, which is advisory for generator prompts.

### Findings raised by the prompts, and their resolution

- **QC_instruction.md** - C4: the clause failing 'pinned type sizes or line-heights' is superseded by generate_instruction.md section 4 'The number rule, DECIDED' (A5), which carries the exact font family and the exact sizes deliberately and is enforced by source_lint.py (G51). Every other C4 clause holds: colour carries no hex, motion carries no duration and no curve, space and radius and breakpoints carry no pixel.
- **QC_instruction.md** - C5: the clause requiring concurrency invariants to be named as storage-level constraints (unique or partial-unique index) is what INV9 forbids and prescription_lint.py (G43) fails. The invariants are stated as observable properties instead, which is the substitution INV9 mandates. Derived-on-read and idempotent-seeding clauses hold.
- **QC_instruction.md** - C7: window_lint.py (G33) reports every graded section past its reference length and the join past the 9000-char slice. Reported, never failed: the brief has no length limit, judge_score never touches reward, and G51 requires 266 companion topics and 695 enumerated items to reach the brief. The critical focus (rules 20 to 24) is front-loaded inside Core features.
- **qc_docker.md** - CMP-011: the `main` service publishes `4173:4173`, which CMP-011 reads as a published host port. CMP-022 and docker_generator C12 REQUIRE `main` to set `ports` and `extra_hosts`, and CMP-022 is Critical while CMP-011 is High. Resolution recorded rather than silently chosen: no SIDECAR publishes a host port, which is the concurrency hazard CMP-011 exists for, and `main` is Harbor's own agent container.
- **qc_docker.md** - CMP-020: `main` carries `extra_hosts` and `ports` beyond `depends_on`, which CMP-020 (Low) reads as excess. CMP-022 (Critical) requires exactly those two keys, so CMP-020 is superseded for this shape. Recorded rather than resolved silently.

## Feature resolution

| Companion subject | Verdict | Where it landed |
|---|---|---|
| The public site: hero, picker, four claims, platforms band, footer | INCLUDED | `## Core features`, `## Front-end specification` |
| Subject pages with two playable samples and no account | INCLUDED | `## Core features` rules 6 to 8 |
| Accounts, anonymous progress, restricted minors | INCLUDED | `## User roles`, `## Core features` Auth |
| The learning session and its integrity rules | INCLUDED | `## Core features` The session |
| Grading and answer matching | INCLUDED | `## Core features` Grading and answer matching |
| The memory model and scheduling | INCLUDED | `## Core features` The memory model |
| Difficulty adaptation and session assembly | INCLUDED | `## Core features` Difficulty |
| Hearts and the lesson economy | INCLUDED | `## Core features` Hearts |
| Streaks, day boundaries and time | INCLUDED | `## Core features` Streaks and the day boundary |
| Experience, leagues and leaderboards | INCLUDED | `## Core features` Experience points, leagues and the leaderboard |
| The course graph and its versioning | INCLUDED | `## Core features` The subject graph and its versioning |
| Internationalization and text handling | INCLUDED | `## Core features` rule 93 |
| Design system, motion, layout, accessibility, copy deck | INCLUDED | `## UI/UX notes`, `## Front-end specification` |
| Zero-asset substitution guide | INCLUDED | `## UI/UX notes` Illustration and iconography |
| Notifications and scheduling | DROPPED | `## Constraints`; no email or push channel exists in a `P1-db` task |
| Speech and audio | DROPPED in part | `## Constraints`; the suppression rule of companion 41.4 IS carried |
| Offline and synchronization | DROPPED | `## Constraints`; no observable surface without a service worker, which INV9 forbids naming |
| Billing, subscriptions and store receipts | DROPPED | `## Constraints`; no payments slot |
| Friends, quests and social | DROPPED | `## Constraints`; the idempotency half of 30.5 IS carried as the product's central rule |
| Experiments and feature assignment | DROPPED | `## Constraints` |
| Scaling, regions and degradation | DROPPED | `## Constraints` |
| Observability and recovery | DROPPED in part | structured logging and the never-logged rule ARE carried in `## Technical requirements` |
| Moderation and identity review | DROPPED | `## Constraints`; no user-generated text exists to moderate |
| Build order | NOT CARRIED | a build order is a work order; `## Build plan` is not baseline |
| Evidence gaps and the acceptance checklist | NOT CARRIED | document-meta about the companion's own capture |

## Slot obligations

| Slot | Provider | State | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_attempt_rows_persist_and_survive_a_reread`, `test_seeding_is_idempotent_across_a_restart`, `test_sample_attempt_is_stored_without_an_account`, and eleven further tests reading rows through `capabilities.make_backend()` |

No slot is UNMET. G32 reports slot observation green inside `workflow_lint.py`.

## Grading surface

| | |
|---|---|
| Workflows | 16 (solo_founder band is 10 to 16) |
| Browser substeps | 45 |
| Pytest substeps | 90 |
| Critical substeps | 11 |
| Test functions in `tests/test_output.py` | 90 |
| Checklist items | 170 |
| Rubric criteria | 17 (16 positive, 1 negative) |
| Non-happy-path workflow ids | 6: `duplicate_session_report_does_not_double_count`, `concurrent_session_reports_resolve_to_one`, `cross_account_progress_read_is_denied`, `unauthenticated_learner_route_is_denied`, `freeze_is_consumed_at_most_once_per_local_date`, `session_in_a_closed_subject_is_invalid` |

Section banners in the one module: core features, data integrity, authorization, edge cases.

### Category mix

| Category | Substeps |
|---|---|
| `business_rule` | 41 |
| `core_outcome` | 1 |
| `data_integrity` | 17 |
| `presentation` | 19 |
| `security` | 7 |
| `validation` | 5 |

### Rubric dimension shares

| Dimension | Target | Share of the positive total | Criteria |
|---|---|---|---|
| `instruction_following` | 0.30 | 0.31 | 3 |
| `functionality` | 0.25 | 0.26 | 3 |
| `ux_flow` | 0.15 | 0.14 | 2 |
| `ui_visual` | 0.15 | 0.14 | 2 |
| `motion` | 0.05 | 0.05 | 2 |
| `accessibility` | 0.05 | 0.05 | 2 |
| `responsiveness` | 0.05 | 0.05 | 2 |

The one negative criterion is a `commission` at `-3`, well inside the three-times-positive cap.

## Literals ledger

132 pinned values across 11 classes. `fixture_lint.py` (G6) reports the bijection green in both directions.

| Class | Count | Values |
|---|---|---|
| `account` | 3 | `learner@example.com`, `learner2@example.com`, `learner3@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `design_phrase` | 7 | `one step larger and one step heavier`, `solid slab`, `Space over dividers`, `tabular`, `comfortable rather than packed`, `no blur at all`, `shape and by words` |
| `endpoint` | 18 | `/api/health`, `/api/auth/signup`, `/api/auth/login`, `/api/auth/me`, `/api/auth/anonymous`, `/api/courses`, `/api/enrolments`, `/api/sessions`, `/api/hearts`, `/api/streak`, and 8 more |
| `env_var` | 4 | `DATABASE_URL`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `DB_ADMIN_URL` |
| `motion_moment` | 7 | `overshoot and settle`, `twinkles twice`, `rises fully into place`, `three full times`, `breathe in sequence`, `the spring resolves to a fade`, `visibly compresses` |
| `number` | 14 | `14400`, `86400`, `172800`, `2592000`, `15768000`, `0.90`, `10000`, `300`, `200`, `60000`, and 4 more |
| `route` | 15 | `/feed`, `/courses`, `/terms`, `/privacy`, `/preferences`, `/community-guidelines`, `/status`, `/blog`, `/signup`, `/login`, and 5 more |
| `scheme` | 9 | `/courses/{slug}`, `/about/{slug}`, `/products/{slug}`, `/help/{slug}`, `/session/{id}`, `/session/{id}/summary`, `/api/path/{course_id}`, `/api/courses/{slug}`, `/api/sessions/{id}/reconcile` |
| `seed_record` | 44 | `Nadia Fenn`, `Bram Oduya`, `Ines Caro`, `Europe/Lisbon`, `Africa/Nairobi`, `America/Bogota`, `Pacific/Auckland`, `Bronze`, `Copper`, `Diamond`, and 34 more |
| `status` | 10 | `correct_with_note`, `incorrect`, `skipped`, `in_progress`, `completed`, `abandoned`, `burned_in`, `lapsed`, `learning`, `restricted` |

One value is `verifier_only`: `DB_ADMIN_URL`, carried by `task.toml` `[verifier].env` alone (INV4).

## Spec folder

Authored at `Output/_spec/S_educa_trac_daily-habit-tutor-vb_20260916_055159/`, never inside the bundle (CON-5).

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the identity re-cast, the scope calls, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at baseline |

## Grading window

| Section | Chars | Reference |
|---|---|---|
| `## Overview` | 1988 | 700 |
| `## User roles` | 2335 | 1000 |
| `## Core features` | 36787 | 2400 |
| `## User flow` | 3900 | 1900 |
| `## UI/UX notes` | 12635 | 1700 |
| `## Constraints` | 3831 | 800 |

Every graded section runs past its reference length and the joined six run past the
9,000-char slice `run_rubric.py` applies. `window_lint.py` (G33) reports this and fails
nothing: the brief has no length limit, the judge grades against self-contained criteria
carrying their own `evaluation_rule`, and `judge_score` never touches reward. The companion
is 4,336 lines and G51 requires 266 of its topics and 695 of its enumerated items to reach
the brief, so trimming to the judge's window would trade reward-driving completeness for a
diagnostic number. The critical focus (rules 20 to 24) is front-loaded inside `## Core features`.

## Traceability

`tests/traceability-matrix.md` and `tests/traceability-matrix.csv` are regenerated by every
`revalidate.py` sweep from the scan G24 makes, so they cannot disagree with the gate. Read
them there rather than here.

## Blocking findings

| Finding | Effect |
|---|---|
| `task.toml` carries no `[delivery]` block | `[delivery.images]` requires a `@sha256:` digest present in `environment/`, and reference/C C.4 forbids both a fabricated digest and a single-architecture child digest. The kit has no registry access, so the digest cannot be resolved here. `validate_task.py` grandfathers the absence (exit 2). The operator resolves the manifest-list digests for `python:3.12-slim-bookworm` and `postgres:16.4-bookworm` and adds the block. |
| `config/kit-config.yaml` carries unresolved merge-conflict markers around `author_email` | Not a bundle defect: this run took both addresses from the Task Order, so the fallback was never read. Worth clearing before the next run that omits `author_email`. |
| The grader pin is `0.22.0` while `vendor/grader-0.23.0/` records what the harness runs at v2final | The kit's standing DRIFT NOTICE (C11). Not this bundle's to resolve: flipping the pin needs to know which generation `deku-verifier-base` is built from. |

## Budget

`turns_expected = 220`, `tokens_expected = 8000000`, the top of the documented band.
Reasoning: ten must-have features (the companion raises the cap from 3 to 6 per reference/G
G.2.1), 42 seeded subjects with three carrying real content, a server-rendered multi-page
application plus an enhanced exercise player, and two engines (answer matching and the memory
model) that the companion itself calls the two most likely to be built wrongly.

## Exit

```
MECHANICALLY-GREEN, NO-SOLUTION
```
