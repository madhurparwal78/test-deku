# Build report - S_local_crud_downhole-friction-catalogue-vb_20260916_070221

Rendered from `_handoff/<project>.gates.jsonl`. No verdict on this page was
transcribed or composed: every gate row is read out of the receipt file the
sweep wrote (ISSUES C-02).

## Identity

| | |
|---|---|
| Task code | `S_local_crud_downhole-friction-catalogue-vb_20260916_070221` |
| Task id | `deku/downhole-friction-catalogue-vb` |
| Cell | solo_founder / local-services / crud-catalog |
| Service profile | P1-db |
| Providers per slot | backend -> postgres |
| Variant | b, axes ['critical_depth', 'spec_sections'] |
| Language | typescript |
| Design direction | companion |
| Capability flags | aesthetic |
| Launch surface | alt_text,form_validation,mobile_viewport,no_broken_links,single_cta |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Grader pin | 0.22.0 |
| Target schema | 1.4 |
| Verifier mode | separate |

## The draws

All keyed on the archetype `downhole-friction-catalogue` (reference/L L.4,
reference/O O.3), never on the six-field code.

| Axis | Value |
|---|---|
| render_model | ssr-islands |
| backend | FastAPI |
| frontend | Astro + islands |
| design_direction | companion |
| nav | sidebar-nav |
| work_surface | table-first |
| create_flow | inline-row |
| feedback | optimistic-row |
| launch_surface | alt_text,form_validation,mobile_viewport,no_broken_links,single_cta |

`design_direction` is `companion`: a PRD was supplied, so reference/L L.6.1 hands
the axis to the measured document and the drawn `playful-consumer` does not govern.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Product catalogue, five families, ten variants | INCLUDED | instruction.md ## Core features | companion 10, 11 |
| Field-evidence library, ten cases | INCLUDED | instruction.md ## Core features | companion 12, 13 |
| Four-step engineering service cycle | INCLUDED | instruction.md ## Core features | companion 14 |
| Firm profile, word-fill statements | INCLUDED | instruction.md ## Core features | companion 15 |
| Enquiry funnel into a modelling request | INCLUDED | instruction.md ## Core features | the graded workflow, companion 1.3 |
| Modelling-request desk | INCLUDED | instruction.md ## Core features | kit-added: crud-catalog needs a surface that displays the persisted row |
| Privacy route | INCLUDED | instruction.md ## Core features | companion 17, load-bearing for both consent labels |
| Two locales, prefix only | INCLUDED | instruction.md ## Core features | companion 2.3 |
| Case map with a vector-map provider | DROPPED | waived at G51 | no map slot in reference/K and no runtime network; companion 9.9 already requires the degraded list, which is what ships |
| Rendered 3D descent sequence | DROPPED | waived at G51 | compiled geometry the companion itself could not recover (its 26.1); its 8.8 requires a static replacement, which ships |
| Hero and product video | DROPPED | waived at G51 | companion 25.3 says do not ship video |
| Build plan section | DROPPED | spec/06-implementation-plan.md | not emitted at baseline (generate_instruction 2.1) |

## Slot obligations

| Slot | Provider | State | Evidence |
|---|---|---|---|
| backend (db) | postgres | MET | G32 in `workflow_lint.py`: the db slot carries critical pytest substeps asserting real rows in `modelling_request` and `subscriber` through `capabilities.make_backend()` |

## Grading surface

| | |
|---|---|
| Workflows | 16 (band 10-16) |
| Browser substeps | 16 |
| Pytest substeps | 38 |
| Critical substeps | 11 |
| Non-happy-path ids | 4: duplicate_submission_creates_no_second_row, anonymous_caller_cannot_reach_the_request_desk, invalid_status_transition_is_refused, engineer_cannot_delete_a_request |
| Pytest module | one, `tests/test_output.py`, 38 test functions |
| Sections covered | core features, data integrity, authorization, edge cases |
| Checklist items | 371 graded |
| Declared but ungraded | 26, each with a `why:` (D-H escalation) |
| Rubric criteria | 17, all positive |

### Rubric dimension shares against the frozen bands

| Dimension | Criteria | Share | Target | Drift |
|---|---|---|---|---|
| instruction_following | 3 | 0.255 | 0.30 | 0.045 |
| functionality | 3 | 0.216 | 0.25 | 0.034 |
| ux_flow | 2 | 0.118 | 0.15 | 0.032 |
| ui_visual | 3 | 0.137 | 0.15 | 0.013 |
| motion | 2 | 0.078 | 0.05 | 0.028 |
| accessibility | 2 | 0.118 | 0.05 | 0.068 |
| responsiveness | 2 | 0.078 | 0.05 | 0.028 |

## Literals ledger

| Class | Count | Values |
|---|---|---|
| account | 2 | `engineer@example.com`, `engineer2@example.com` |
| credential | 1 | `deku-demo-pw-2026` |
| design_phrase | 8 | `graph paper`, `more rules than filled areas`, `Dark inserts, not a dark theme`, `pointer, not a colour scheme`, `all eight corners`, `the name is the product`, `Monument Grotesk`, `two full digit cycles` |
| endpoint | 14 | `/api/health`, `/api/auth/login`, `/api/auth/signup`, `/api/products`, `/api/cases`, `/api/enquiry`, `/api/subscribe`, `/api/requests`, +6 more |
| env_var | 3 | `DATABASE_URL`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT` |
| motion_moment | 6 | `spins up`, `one at a time`, `one bar per line`, `word by word in reading order`, `wipes open from the middle outward`, `never settles into lockstep` |
| number | 8 | `4,025 m`, `2,938 m`, `100`, `510`, `2000`, `500`, `1225`, `3500` |
| route | 14 | `/en/products`, `/en/products/frs`, `/en/products/svr`, `/en/products/x1`, `/en/products/x3`, `/en/products/x6`, `/en/cases`, `/en/cases/22061`, +6 more |
| scheme | 2 | `/api/cases/{well_number}`, `/api/requests/{request_ref}` |
| seed_record | 19 | `REQ-1001`, `FRS`, `SVR`, `TRANSFER X1`, `TRANSFER X3`, `TRANSFER X6`, `FRS-89`, `FRS-102`, +11 more |
| status | 6 | `new`, `modelling`, `configured`, `reported`, `declined`, `Done` |

Every value is carried by the files its `carriers` list names, in both directions (G6, `fixture_lint.py`).

## spec/ docs and the brief sections they fed

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the companion carry table, every residual call |
| `01-PRD.md` | ## Overview, ## Core features, ## Constraints |
| `02-TRD.md` | ## Technical requirements |
| `03-app-flow.md` | ## User flow |
| `04-uiux-brief.md` | ## UI/UX notes, ## Front-end specification |
| `05-backend-schema.md` | ## Data model, ## User roles |
| `06-implementation-plan.md` | author-side only; ## Build plan is not emitted at baseline |

## Grading window

| Section | chars | reference |
|---|---|---|
| Core features | 27225 | 2400 |
| User flow | 3476 | 1900 |
| UI/UX notes | 10369 | 1700 |
| Constraints | 1077 | 800 |
| User roles | 1243 | 1000 |
| Overview | 2851 | 700 |

`window_lint.py` (G33) reports length and fails nothing: the brief has no cap. `## Core features` runs past the 2,500-char slice `run_rubric.py` takes, so its tail reaches the agent in full and the judge in part. It was not cut - generate_instruction sect.4 forbids cutting a real rule to fit - and the graded workflow was moved to the head of the section so the judge's slice sees it first.

## Kit gate log

Verbatim from the receipts. `argv_sha` binds each row to the exact invocation; `inputs` carries the SHA-256 of every file the gate read.

| Gate | Tool | Exit | Verdict | Inputs hashed |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | 24 |
| G1/G12 | `layout_lint.py` | 0 | PASS | 24 |
| G46 | `structure_lint.py` | 0 | PASS | 24 |
| G50 | `docker_lint.py` | 0 | PASS | 24 |
| G55 | `runtime_deps_lint.py` | 0 | PASS | 24 |
| G63 | `secret_lint.py` | 0 | PASS | 24 |
| G48 | `truth_lint.py` | 0 | PASS | 24 |
| G51 | `source_lint.py` | 0 | PASS | 24 |
| G52 | `rubric_context_lint.py` | 0 | PASS | 24 |
| G54 | `comment_lint.py` | 0 | PASS | 24 |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | 24 |
| G11 | `leak_scan.py` | 0 | PASS | 24 |
| G33 | `window_lint.py` | 0 | PASS | 24 |
| G4/G5 | `contract_lint.py` | 0 | PASS | 24 |
| G43 | `prescription_lint.py` | 0 | PASS | 24 |
| G44 | `disclosure_lint.py` | 0 | PASS | 24 |
| G10 | `no_sdk_lint.py` | 0 | PASS | 24 |
| G31 | `determinism_lint.py` | 0 | PASS | 24 |
| G14 | `reward_path_lint.py` | 0 | PASS | 24 |
| G27/G30 | `rubric_lint.py` | 0 | PASS | 24 |
| G41 | `flag_lint.py` | 0 | PASS | 24 |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | 24 |
| G59/G60 | `codequality_lint.py` | 2 | ? | 24 |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | 24 |
| G6 | `fixture_lint.py` | 0 | PASS | 24 |
| G24 | `coverage_map.py` | 0 | PASS | 24 |
| G37 | `checklist_qc.py` | 0 | PASS | 24 |
| G39 | `rubric_align_lint.py` | 0 | PASS | 24 |
| G28/G29 | `channel_lint.py` | 0 | PASS | 24 |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | 24 |
| G0/INV5 | `vendor_check.py` | 0 | PASS | 24 |
| G47 | `output_qc.py` | 0 | PASS | 24 |

**ALL GATES GREEN** - 32 rows, 31 at exit 0.

## Prompt receipts (G40)

| Prompt | Gate | Verdict | Checks | Verifier |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | self |
| `QC_spec.md` | G34 | PASS | 15 | self |
| `docker_generator.md` | S5 | PASS | 0 | self |
| `generate_instruction.md` | S2 | PASS | 0 | self |
| `qc_docker.md` | G35 | PASS | 105 | self |
| `qc_rubric.md` | G53 | PASS | 16 | self |
| `qc_solution_checklist.md` | G37 | PASS | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | self |
| `task_code_verifier.md` | G3 | PASS | 12 | self |

Every certification prompt reports **SELF-ATTESTED**: one agent authored the artifacts and ran the reviews, so `owner != verifier` does not hold. These are recorded verdicts, never independent ones. Findings raised and repaired during those reviews are listed in the receipt file.

## Blocking findings

| Finding | Effect |
|---|---|
| `[delivery.images]` carries no digest pin | The block is emitted without the optional `images` table. `environment/Dockerfile` pins by explicit manifest-list tag, which `docker_generator.md` requires and which cannot be restated as a digest without inventing one. The operator pins digests when the image is built. |
| 26 checklist obligations are Declared but ungraded | Each names why no channel observes it (OPEN-DECISIONS D-H). They remain product requirements and move no score. |
| The taxonomy cell was re-keyed | The Task Order named `hardware-iot` and `catalog-browse`, neither a member of the closed enum. Re-keyed to `local-services` and `crud-catalog`; recorded in `00-decisions.md`. |

## Budget

`turns_expected = 140`, `tokens_expected = 5000000`. The medium band, reasoned from: twelve public routes plus three desk routes; one backing service; two roles; a front-end specification carrying a full measured design system; and one stateful workflow whose hard part is persistence rather than concurrency.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. No reference app exists and nothing here has been compiled or run.
