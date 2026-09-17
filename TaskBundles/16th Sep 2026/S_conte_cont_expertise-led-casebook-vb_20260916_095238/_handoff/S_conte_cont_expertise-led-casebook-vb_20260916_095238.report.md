# Build report: S_conte_cont_expertise-led-casebook-vb_20260916_095238

Rendered from `_handoff/S_conte_cont_expertise-led-casebook-vb_20260916_095238.gates.jsonl` by S10. No verdict below was written by hand.

## Identity

| Field | Value |
|---|---|
| task code | `S_conte_cont_expertise-led-casebook-vb_20260916_095238` |
| task id | `deku/expertise-led-casebook-vb` |
| cell | solo_founder / content-publishing / content-publishing |
| submitted cell | domain `portfolio-agency` resolved to `content-publishing`; pattern `content-publishing` as submitted; see `_spec/<code>/00-decisions.md` |
| service profile | `P4-db-storage` |
| providers | backend = `postgres`, storage = `minio` |
| variant | `b`, axes `critical_depth`, `spec_sections` |
| language | `typescript` (Express server, Angular single-page application) |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| design direction | `companion` (bank pick `brutalist-utility` recorded, not governing) |
| launch surface | alt_text, meta_tags, page_view_log, single_cta, sitemap_robots |
| run mode | PRD mode: `Output/_prd/videinfra/run.yaml` (G64 PASS); idea file `videinfra_input.yaml`; plain PRD `videinfra_prd_plain.md`, split from `videinfra_prd.md` by prd-generator `split_prd.py` |
| companion carry (G51) | against the plain PRD: 46/49 topics carried, 3 recorded waivers (`test plan`, `acceptance checklist`, `internationalisation and formatting`) |
| shard | 1 of 1 |
| kit / grader / schema | deku-green-field at origin/yasir-test 38cd9e3 (PRD mode), grader 0.22.0, schema 1.4 |
| QL / contributor | abhishek.shawa@ethara.ai / rishabh.tiwari@ethara.ai |
| reference link | https://videinfra.com/ (the site the companion was measured from; never contacted by the bundle) |

## Feature resolution

| Candidate | Verdict | File | Reason |
|---|---|---|---|
| publish boundary for case study, address and cover | INCLUDED | instruction.md Core features 1, 2 | the pattern's critical focus |
| publish preconditions: expertise, tag, cover | INCLUDED | Core features 3 | companion S-22.5 plus the idea's cover |
| covers in minio, generated only | INCLUDED | Core features 4 | storage slot; companion S-38.4 and S-46.4 forbid uploads, so every cover is drawn from its saved seed and palette |
| version on every write, no merge | INCLUDED | Core features 5 | companion S-32.4, S-34.6 |
| idempotency key on creates | INCLUDED | Core features 6 | companion S-34.6 |
| shelf order with kept place, versioned reorder | INCLUDED | Core features 7 | companion S-23, S-32.3 to S-32.5; the idea's "reorders the shelf and republishes" |
| eight hand-filled feature slots | INCLUDED | Core features 8 | companion S-23.3, S-28.4 |
| front page, work index, case study, landings | INCLUDED | Core features 9 to 12 | companion S-11 to S-14 |
| brief form, spam floor, rate limit | INCLUDED | Core features 13, 14 | companion S-19, S-29, S-38.3 |
| brief inbox, owner only, plain text | INCLUDED | Core features 15 | companion S-24 |
| dashboard, editor, sign in, sessions, refusal page | INCLUDED | Core features 16 to 20 | companion S-21, S-22, S-25 to S-27 |
| not found, gone, privacy, page views, titles, sitemap, alt text | INCLUDED | Core features 21 to 24 | drawn launch surface plus companion S-20 |
| blog index, article, career page, article editor | DROPPED | Constraints | outside the idea; recorded |
| password reset, invitation, address change, five emails | DROPPED | Constraints | no mail slot in P4-db-storage |
| per-network rate limit | DROPPED | 00-decisions | every grader request shares one address |
| companion test plan, acceptance checklist | DROPPED | waived | the companion checking itself (INV10) |
| translatable strings and language order | DROPPED | waived | unobservable with one language shipped; one language and UTC dates kept |

## Slot obligations

| Slot | Provider | Status | Critical substep |
|---|---|---|---|
| backend | postgres | MET | `test_seed_is_idempotent_across_a_restart`, `test_stale_version_write_is_refused_as_a_conflict` |
| storage | minio | MET | `test_generated_cover_file_lands_in_the_object_store_bucket`, `test_draft_cover_bytes_are_refused_to_public_callers` |

## Grading surface

- workflows: **16** (band 10 to 16 for solo_founder); browser substeps **49**; pytest substeps **123**; critical **16**
- non-happy-path ids: `invalid_brief_is_refused_with_field_messages`, `spam_brief_is_absorbed_and_rate_limit_is_enforced`, `editor_is_forbidden_the_inbox_and_the_owner_controls`, `unauthenticated_caller_is_denied_the_studio`, `draft_case_study_cannot_be_read_by_the_public`, `conflict_on_a_stale_or_concurrent_write`, `invalid_address_answers_the_not_found_page`
- pytest categories: {'business_rule': 28, 'core_outcome': 5, 'data_integrity': 28, 'presentation': 14, 'security': 31, 'validation': 17}
- test module: `tests/test_output.py`, **123** tests (five drive a real page through Playwright), covering core features, authorization, data integrity, edge cases and the storage slot
- checklist: **644** items; every one cited (G24). Deployment-contract and source-shape asks no outside grader can observe are cited with a written justification on the health step and discharged by the handoff gates (OPEN-DECISIONS D-H).
- traceability: `tests/traceability-matrix.md` and `.csv`, regenerated by the sweep
- rubric: **35** judged criteria, 30 positive / 5 negative; reference rubric 123 compiled items (share 1.00)

| Dimension | Positive points | Share | Target |
|---|---|---|---|
| instruction_following | 17 | 0.27 | 0.30 |
| functionality | 11 | 0.18 | 0.25 |
| ux_flow | 7 | 0.11 | 0.15 |
| ui_visual | 12 | 0.19 | 0.15 |
| motion | 4 | 0.06 | 0.05 |
| accessibility | 7 | 0.11 | 0.05 |
| responsiveness | 4 | 0.06 | 0.05 |

## Literals ledger

| Class | Count | Examples | Carriers |
|---|---|---|---|
| account | 6 | `owner@example.com`, `editor@example.com`, `visitor@example.com` | conftest.py, instruction.md |
| credential | 1 | `deku-demo-pw-2026` | conftest.py, instruction.md |
| credential (verifier only) | 2 | `deku_admin`, `deku-admin-dev-7f3c` | task.toml |
| design_phrase | 9 | `Inter Tight`, `Helvetica Neue`, `flat pale grey` | conftest.py, instruction.md |
| endpoint | 44 | `POST /api/auth/signup`, `POST /api/auth/login`, `GET /api/auth/me` | conftest.py, instruction.md, test_output.py |
| env_var | 7 | `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET` | conftest.py, instruction.md |
| env_var (verifier only) | 1 | `DB_ADMIN_URL` | task.toml |
| motion_moment | 6 | `letter by letter`, `draws itself on`, `rolls upward` | instruction.md |
| number | 18 | `999999`, `1990`, `120` | conftest.py, instruction.md, test_output.py |
| route | 24 | `/`, `/work`, `/work/<slug>` | conftest.py, instruction.md, test_output.py |
| schema | 20 | `accounts`, `sessions`, `expertises` | conftest.py, instruction.md, test_output.py |
| scheme | 2 | `covers/{case_study_id}/{sha256_of_bytes}.{ext}`, `covers/7/9f2a...d0.png` | instruction.md |
| seed_record | 54 | `Mara Lind`, `Jonas Weller`, `Northform` | conftest.py, instruction.md, test_output.py |
| status | 40 | `owner`, `editor`, `visitor` | conftest.py, instruction.md, test_output.py |

## Spec documents (authoring aids, outside the bundle)

- `Output/_spec/S_conte_cont_expertise-led-casebook-vb_20260916_095238/00-decisions.md` fed every judgment call, the carry table and the waivers
- `Output/_spec/S_conte_cont_expertise-led-casebook-vb_20260916_095238/01-PRD.md` fed Overview, User roles, Constraints
- `Output/_spec/S_conte_cont_expertise-led-casebook-vb_20260916_095238/02-TRD.md` fed Technical requirements, the Dockerfile base
- `Output/_spec/S_conte_cont_expertise-led-casebook-vb_20260916_095238/03-app-flow.md` fed User flow, Core features
- `Output/_spec/S_conte_cont_expertise-led-casebook-vb_20260916_095238/04-uiux-brief.md` fed UI/UX notes, Front-end specification
- `Output/_spec/S_conte_cont_expertise-led-casebook-vb_20260916_095238/05-backend-schema.md` fed Data model, the seed
- `Output/_spec/S_conte_cont_expertise-led-casebook-vb_20260916_095238/06-implementation-plan.md` fed the channel split S6 to S8 followed

## Grading window

```
VERDICT  PASS   (/Users/mac/Downloads/test/Output/S_conte_cont_expertise-led-casebook-vb_20260916_095238/instruction.md)
section        H2                chars  reference  flag
core_features  Core features     18709       2400  past-slice
user_flow      User flow          4068       1900  past-slice
ui_ux_notes    UI/UX notes        5245       1700  past-slice
constraints    Constraints        1313        800  over-reference
user_roles     User roles         1710       1000  over-reference
overview       Overview           1346        700  over-reference
joined total                     32391       8800  past-slice
first four                       29335       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```
Core features runs past the judge's slice; rules 1 to 3, the critical focus, sit inside it. Length is reported, never failed (G33).

## Kit gate log

| Gate | Tool | Exit | Verdict | Inputs hashed |
|---|---|---|---|---|
| G2/G16 | validate_task.py | 2 | NOT-APPLICABLE | 25 |
| G1/G12 | layout_lint.py | 0 | PASS | 25 |
| G46 | structure_lint.py | 0 | PASS | 25 |
| G50 | docker_lint.py | 0 | PASS | 25 |
| G55 | runtime_deps_lint.py | 0 | PASS | 25 |
| G63 | secret_lint.py | 0 | PASS | 25 |
| G48 | truth_lint.py | 0 | PASS | 25 |
| G51 | source_lint.py | 0 | PASS | 25 |
| G64 | run_lint.py | 0 | PASS | 25 |
| G52 | rubric_context_lint.py | 0 | PASS | 25 |
| G54 | comment_lint.py | 0 | PASS | 25 |
| G17 | secret_hygiene_lint.py | 0 | PASS | 25 |
| G11 | leak_scan.py | 0 | PASS | 25 |
| G33 | window_lint.py | 0 | PASS | 25 |
| G4/G5 | contract_lint.py | 0 | PASS | 25 |
| G43 | prescription_lint.py | 0 | PASS | 25 |
| G44 | disclosure_lint.py | 0 | PASS | 25 |
| G10 | no_sdk_lint.py | 0 | PASS | 25 |
| G31 | determinism_lint.py | 0 | PASS | 25 |
| G14 | reward_path_lint.py | 0 | PASS | 25 |
| G27/G30 | rubric_lint.py | 0 | PASS | 25 |
| G41 | flag_lint.py | 0 | PASS | 25 |
| G56/G57/G58 | if_lint.py | 0 | PASS | 25 |
| G59/G60 | codequality_lint.py | 2 | ? | 25 |
| G7/G8/G9/G32/G45 | workflow_lint.py | 0 | WARN | 25 |
| G6 | fixture_lint.py | 0 | PASS | 25 |
| G24 | coverage_map.py | 0 | PASS | 25 |
| G37 | checklist_qc.py | 0 | PASS | 25 |
| G39 | rubric_align_lint.py | 0 | PASS | 25 |
| G28/G29 | channel_lint.py | 0 | PASS | 25 |
| G40 | prompt_receipt_lint.py | 0 | WARN | 25 |
| G0/INV5 | vendor_check.py | 0 | PASS | 25 |
| G47 | output_qc.py | 0 | PASS | 25 |

Corpus-level, run separately at S10:

- G38 `kit_selftest.py`: PASS, 32 checks
- G42 `corpus_overlap.py` over the five bundles in this cell: PASS, 10 cross-archetype pairs, none above 60% substep overlap
- G49 `diversity_lint.py`: WARN mode, 5 corpus findings, none naming this bundle; its `top-nav` and `companion` draws count toward two of the corpus-wide concentration warnings (`companion` is expected for PRD-built tasks)
- G61 `corpus_report.py`: NOT-APPLICABLE, no admissible bundle in the ledger yet

Prompt receipts (G40): `_handoff/S_conte_cont_expertise-led-casebook-vb_20260916_095238.receipts.json`. Each certification prompt was run by a separate reviewer agent, not by the author. G40 answers WARN only because the advisory generator prompts carry no receipt.

Review cycles: `task_code_verifier`, `qc_toml` and `qc_docker` passed in cycle 3. `QC_spec`, `QC_instruction`, `qc_solution_checklist` and `qc_rubric` passed in cycle 4. That cycle was authorised by the user after `qc_rubric` ended in ABORT at the three-cycle bound, and its receipt records RC-15 as WARN for that reason.

Environment decision: the admin role `deku_admin` uses its own password, `deku-admin-dev-7f3c`, set only in compose and the verifier-only `DB_ADMIN_URL`. The shared kit convention would let the agent's `DATABASE_URL` password log in as superuser (qc_toml SEC-002). `qc_toml` ENV-006 is WARN for the departure; the kit convention should split the two passwords.

- G3 `task_code_verifier.md`: VALID, verifier `subagent aeba7cf3f08bc037a (general-purpose, independent of the author)`
- G34 `QC_instruction.md`: PASS (2 WARN), verifier `subagent a61b33f7f6b8fe0b3 (general-purpose, independent of the author)`
- G34 `QC_spec.md`: PASS, verifier `subagent a61b33f7f6b8fe0b3 (general-purpose, independent of the author)`
- G36 `qc_toml.md`: PASS (5 NOT-APPLICABLE, 1 SKIP, 1 WARN), verifier `subagent aeba7cf3f08bc037a (general-purpose, independent of the author)`
- G35 `qc_docker.md`: PASS (7 NOT-APPLICABLE), verifier `subagent aeba7cf3f08bc037a (general-purpose, independent of the author)`
- G37 `qc_solution_checklist.md`: PASS, verifier `subagent a868f5b2599ca2c49 (general-purpose, independent of the author)`
- G53 `qc_rubric.md`: PASS (3 WARN), verifier `subagent a74120d77cb2140a7 (general-purpose, independent of the author)`

## Handoff gates (undecided)

See `S_conte_cont_expertise-led-casebook-vb_20260916_095238.handoff.md`. G13, G15, G18, G19, G20, G21, G25 need Docker and the harness; the kit ran none of them.

## Blocking findings

- None prevent a required test.
- The page-driven tests (titles, alt text, not found, type scale, long dash and embedded player) launch Chromium from the verifier image through a `page` fixture in `tests/conftest.py`; the base image ships Playwright but not the pytest plugin.
- The type-scale test holds the front page to the pinned wide-window sizes at a 1440 by 900 viewport; a build that scales type fluidly must land on those steps at that width.

## Open questions for the author

- The QL email is recorded as given, `abhishek.shawa@ethara.ai`; the kit's example spells it `abhishek.shaw@`. Confirm the spelling.
- The verifier's `APP_PUBLIC_URL` default `http://localhost:4173` only reaches the app in separate mode when the harness overrides it.
- The sibling bundle `S_conte_cont_talent-roster-reel-vb_20260916_071348` has an unquoted `(earned: ...)` value that breaks YAML parsing of its `tests/workflows.yaml`; reported, not changed.

## Budget

`turns_expected = 200`, `tokens_expected = 8000000`: a public site of seven routes plus a studio of seven routes, twenty-six core rules, a long front-end specification, and two slots with a publish boundary on both.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
NOT ADMISSIBLE
```
