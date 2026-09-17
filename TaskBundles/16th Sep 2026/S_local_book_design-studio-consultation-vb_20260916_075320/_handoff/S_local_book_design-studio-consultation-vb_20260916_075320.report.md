# Build report - S_local_book_design-studio-consultation-vb_20260916_075320

## Identity

| Field | Value |
|---|---|
| task code | `S_local_book_design-studio-consultation-vb_20260916_075320` |
| task id | `deku/design-studio-consultation-vb` |
| cell | solo_founder / local-services / booking-scheduling |
| archetype | `design-studio-consultation` |
| service profile | `P2-db-email` |
| providers | `backend = postgres`, `email = mailpit` |
| variant | `b`, axes `critical_depth`, `spec_sections` |
| language | `python` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 |
| design direction | `companion` (reference/L L.6.1: a supplied companion beats the bank draw) |
| launch surface | `alt_text, custom_404, form_validation, no_broken_links, social_preview` |

The Task Order arrived with `domain: portfolio-agency`, which is not one of the 36 enum domains.
It was recast to `local-services` and confirmed with the tasker before the mint. Every other field
is as supplied.

## Draws (SHA-256 over `[metadata].archetype`)

| Axis | Value |
|---|---|
| render_model | `spa-json-api` |
| backend | FastAPI |
| frontend | SolidJS + Vite |
| nav | `sidebar-nav` (honoured as the companion's panel navigation) |
| work_surface | `calendar-grid` (the booking slot grid) |
| create_flow | `multi-step-wizard` (the three addressed booking steps) |
| feedback | `inline-banner` (a lost race, an ended hold, a rejected field) |
| design_direction | `companion` (bank draw `brutalist-utility` recorded and overridden) |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Project archive and its filters | INCLUDED | Core features, Front-end specification | the proof surface; the only live control on the public site |
| Case study template | INCLUDED | Core features | ordered media records, outbound action, related work |
| Eight-service expertise tree | INCLUDED | Core features | one vocabulary for the tree, the tags and the filters |
| Three packaged offers | INCLUDED | Core features | floors, four panels, the disqualifying list |
| Named method | INCLUDED | Core features | `Throughline(TM)`, four steps, the mark on every route |
| Awards wall, proof band, directory badge | INCLUDED | Core features | one record, several placements |
| Booking a strategic call | INCLUDED | Core features | the critical focus: one slot, one live booking |
| The enquiry and its promise | INCLUDED | Core features | consent moment plus a derived due moment |
| The studio console | INCLUDED | Core features | slots, enquiries, publishing, the authorization boundary |
| Launch surface (alt text, not-found, links, validation, preview) | INCLUDED | Core features, UI/UX notes, Technical requirements | the five drawn obligations, written as product features |
| Scope configurator emitting a versioned quote | DROPPED | 00-decisions companion carry table | a separate product; breaks the 6-10 companion feature cap |
| Case study outcome ledger | DROPPED | 00-decisions companion carry table | needs a scheduled re-verification job outside this scope |
| Visitor-assembled shortlist | DROPPED | 00-decisions companion carry table | a separate product; breaks the cap |
| Third party consent dialog geometry | DROPPED | 00-decisions companion carry table | somebody else's component; its measurements describe that component |

## Slot obligations

| Slot | Provider | State | Evidence |
|---|---|---|---|
| backend | `postgres` | MET | critical substeps in `concurrent_holds_yield_one_call` and `expired_hold_returns_the_slot`; `booking_one_live_per_slot` asserted through `capabilities.make_backend()` |
| email | `mailpit` | MET | critical substep `test_confirmation_email_reaches_only_the_booking_account`; three non-transition checks assert silence |

## Grading surface

| Measure | Value |
|---|---|
| workflows | 15 (solo_founder band 10-16) |
| browser substeps | 64 |
| pytest substeps | 108 |
| browser : pytest ratio | 0.59 (G45 floor 0.40) |
| critical substeps | 25 |
| non-happy-path ids | `concurrent_holds_yield_one_call`, `expired_hold_returns_the_slot`, `client_cannot_reach_another_clients_booking`, `client_is_denied_the_studio_console`, `unauthenticated_caller_is_denied_every_guarded_endpoint`, `invalid_enquiry_is_refused_inline`, `visitor_meets_an_empty_state_and_an_unknown_address` |
| pytest module | `tests/test_output.py`, 108 test functions |
| banners covered | core features, data integrity, edge cases, email, authorization |
| checklist items | 483 |
| category mix | business_rule 28, core_outcome 4, data_integrity 17, notification 6, presentation 24, security 18, validation 11 |

## Rubric

17 judged criteria: 15 positive, 2 negative (commission). Positive total 53.

| Dimension | Points | Share | Target |
|---|---|---|---|
| instruction_following | 15 | 0.283 | 0.30 |
| functionality | 13 | 0.245 | 0.25 |
| ux_flow | 8 | 0.151 | 0.15 |
| ui_visual | 8 | 0.151 | 0.15 |
| motion | 6 | 0.113 | 0.05 |
| accessibility | 1 | 0.019 | 0.05 |
| responsiveness | 2 | 0.038 | 0.05 |

Every one of the 38 `ui`-tagged checklist items is claimed by exactly one criterion
(G39 forward and reverse), and no browser substep claims any of them (G28 rule three).

## Literals ledger

127 entries. Classes: account 3, credential 1, design_phrase 10, env_var 2, number 21, route 16, scheme 1, seed_record 59, status 14.
Two entries are `verifier_only` and carry `task.toml` alone: `DB_ADMIN_URL`, `EMAIL_INBOX_API_URL`.
Every other entry carries `instruction.md` and `tests/conftest.py`, and G6 round-trips both ways.

## spec/ folder

At `Output/_spec/S_local_book_design-studio-consultation-vb_20260916_075320/`, never inside the bundle (CON-5).

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the cell recast, the companion carry table, the waiver list |
| `01-PRD.md` | Overview, Core features, Constraints |
| `02-TRD.md` | Technical requirements |
| `03-app-flow.md` | User flow, Deployment contract API shapes |
| `04-uiux-brief.md` | UI/UX notes, Front-end specification |
| `05-backend-schema.md` | Data model, User roles |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at this baseline |

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Core features | 14390 | 2400 | past-slice |
| User flow | 4687 | 1900 | past-slice |
| UI/UX notes | 8465 | 1700 | past-slice |
| Constraints | 1289 | 800 | over-reference |
| User roles | 1696 | 1000 | over-reference |
| Overview | 1732 | 700 | over-reference |

Joined 32259 against the 9000-char join point. **Deliberate.** The tasker
asked for a fully detailed brief, in particular on UI and UX, and accepted that prose past the slice
reaches the agent in full but not the judge. G33 fails nothing on length, the judged criteria are
self-contained and carry their own `evaluation_rule`, and `judge_score` never touches reward.
Recorded as QC_instruction C7 WARN in the receipts.

## Kit gate log (rendered from `S_local_book_design-studio-consultation-vb_20260916_075320.gates.jsonl`)

| Gate | Tool | Exit | Verdict | Note |
|---|---|---|---|---|
| G2/G16 | validate_task.py | 0 | PASS |  |
| G1/G12 | layout_lint.py | 0 | PASS |  |
| G46 | structure_lint.py | 0 | PASS |  |
| G50 | docker_lint.py | 0 | PASS |  |
| G55 | runtime_deps_lint.py | 0 | PASS |  |
| G63 | secret_lint.py | 0 | PASS |  |
| G48 | truth_lint.py | 0 | PASS |  |
| G51 | source_lint.py | 0 | PASS |  |
| G52 | rubric_context_lint.py | 0 | PASS |  |
| G54 | comment_lint.py | 0 | PASS |  |
| G17 | secret_hygiene_lint.py | 0 | PASS |  |
| G11 | leak_scan.py | 0 | PASS |  |
| G33 | window_lint.py | 0 | PASS |  |
| G4/G5 | contract_lint.py | 0 | PASS |  |
| G43 | prescription_lint.py | 0 | PASS |  |
| G44 | disclosure_lint.py | 0 | PASS |  |
| G10 | no_sdk_lint.py | 0 | PASS |  |
| G31 | determinism_lint.py | 0 | PASS |  |
| G14 | reward_path_lint.py | 0 | PASS |  |
| G27/G30 | rubric_lint.py | 0 | PASS |  |
| G41 | flag_lint.py | 0 | PASS |  |
| G56/G57/G58 | if_lint.py | 0 | PASS |  |
| G59/G60 | codequality_lint.py | 2 | ? |  |
| G7/G8/G9/G32/G45 | workflow_lint.py | 0 | PASS |  |
| G6 | fixture_lint.py | 0 | PASS |  |
| G24 | coverage_map.py | 0 | PASS |  |
| G37 | checklist_qc.py | 0 | PASS |  |
| G39 | rubric_align_lint.py | 0 | PASS |  |
| G28/G29 | channel_lint.py | 0 | PASS |  |
| G40 | prompt_receipt_lint.py | 0 | WARN |  |
| G0/INV5 | vendor_check.py | 0 | PASS |  |
| G47 | output_qc.py | 0 | PASS |  |

## Prompt receipts

9 prompts recorded, 292 declared checks answered,
19 findings. All seven certification prompts are SELF-ATTESTED:
owner and verifier are one agent in this run, which the kit records rather than counts as independent.

Non-PASS checks, each with its finding in `S_local_book_design-studio-consultation-vb_20260916_075320.receipts.json`:

- QC_instruction A1, B3 - `## Build plan` deliberately absent (generate_instruction section 2.1).
- QC_instruction C7 - the grading window deliberately exceeded, at the tasker's instruction.
- QC_spec S2 - ten must-have features against the prompt's 3-6; `companion_feature_cap` is [6, 10].
- qc_docker BP-004, SEC-003 - inherited from the kit's own Dockerfile skeleton.
- qc_docker DEP-011, DEP-016, DEP-017 - NOT-APPLICABLE under `separate` mode and `language = python`.
- qc_toml SCHEMA-011, SCHEMA-013 - `[delivery]` is mandated by stage-4 and absent from the section 11 template.
- qc_toml VERIF-005 - `APP_PUBLIC_URL` defaults to `main:4173`, which `separate` mode requires.
- qc_toml VERIF-007, BENCH-002, TAX-006, SIGN-001, SIGN-002, SIGN-003, INST-007 - NOT-APPLICABLE.

## Blocking findings

NONE. No spec gap and no harness gap prevented a required grader.

## Corpus-level gates

| Gate | Verdict |
|---|---|
| G22 `overlap.py` | NOT-APPLICABLE: this archetype has one variant, so there is no sibling to compare |
| G42 `corpus_overlap.py` | NOT-APPLICABLE: fewer than two comparable bundle directories at this root |
| G49 `diversity_lint.py` | PASS (WARN mode). No finding names this bundle |
| G38 `kit_selftest.py` | PASS, 32 checks |

## Versions and budget

Kit `deku-green-field` (2026-09-16 revision) - vendored grader pin `0.22.0` - target schema `1.4` -
`harbor_version` `0.20.0`. `turns_expected` 165 and `tokens_expected` 6000000 are the Standard tier
for a companion-backed variant `b`: ten product features, sixteen tables, a browser layer and a
concurrency invariant, which is the same shape as the shipped variant `b` bundles.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`
