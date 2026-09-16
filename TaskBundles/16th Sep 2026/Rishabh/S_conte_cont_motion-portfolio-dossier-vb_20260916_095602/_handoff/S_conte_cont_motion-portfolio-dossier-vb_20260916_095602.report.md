# Build report: S_conte_cont_motion-portfolio-dossier-vb_20260916_095602

Rendered from `_handoff/S_conte_cont_motion-portfolio-dossier-vb_20260916_095602.gates.jsonl` by S10. No verdict below was written by hand.

## Identity

| Field | Value |
|---|---|
| task code | `S_conte_cont_motion-portfolio-dossier-vb_20260916_095602` |
| task id | `deku/motion-portfolio-dossier-vb` |
| cell | solo_founder / content-publishing / content-publishing |
| submitted cell | domain `portfolio-agency` (not in the 36-domain enum), resolved to `content-publishing`; pattern `content-publishing` as supplied; see `_spec/<code>/00-decisions.md` |
| service profile | `P4-db-storage` |
| providers | backend = `postgres`, storage = `minio` |
| variant | `b`, axes `critical_depth`, `spec_sections` |
| language | `python` (Flask + Jinja, Alpine.js over server templates) |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| design direction | `companion` (bank pick `playful-consumer` recorded, not governing) |
| launch surface | cookie_choice, form_validation, no_broken_links, privacy_page, security_headers |
| run mode | PRD mode: `Output/_prd/praga/run.yaml` (G64 PASS); idea file `praga_input.yaml`; plain PRD `praga_prd_plain.md`, split from `praga_prd.md` (the supplied `/Users/mac/Downloads/test/praga_prd.md`) by prd-generator `split_prd.py` |
| companion carry (G51) | against the plain PRD: 31/31 topics, 1 recorded waiver (`acceptance checklist`) |
| shard | 1 of 1 |
| kit / grader / schema | deku-green-field at origin/yasir-test 38cd9e3 (PRD mode, G0-G65), grader 0.22.0, schema 1.4, rubric_version 1 |
| QL / contributor | abhishek.shawa@ethara.ai / rishabh.tiwari@ethara.ai |
| reference link | https://spragadheeshraj.com/ (the captured site the companion was measured from; never named in the bundle, never contacted) |

## Feature resolution

| Candidate | Verdict | File | Reason |
|---|---|---|---|
| publish boundary: listings, address, suggestions, reading lists, media | INCLUDED | instruction.md CF-1 | the pattern's critical focus |
| images in minio at a hashed key, served only through the app | INCLUDED | CF-2 | storage slot |
| publish refused for an incomplete case study | INCLUDED | CF-3 | companion S-16.4 catalogue rule |
| work index with AND filters, three sorts, address state | INCLUDED | CF-4 | companion S-16, Task Order idea |
| computed suggestions, slot one exact, four-hop coverage | INCLUDED | CF-5 | companion S-16.5 |
| reading list with monotonic positions and stale-position reset | INCLUDED | CF-6 | Task Order idea, companion S-18 and S-24.3 |
| reading spine surfaces: rail marks, resume card, Carry on band | INCLUDED | CF-7 | companion S-18 |
| three motion levels with still states | INCLUDED | CF-8 | Task Order idea, companion S-17 |
| annotation layer with the amplitude from the constant | INCLUDED | CF-9 | companion S-19 |
| browser question, privacy page, link sweep, inline validation, headers | INCLUDED | CF-10..13, CF-15 | drawn launch surface |
| studio: split detail pane, dedicated create route, inline banners | INCLUDED | CF-14 | S-2.10 draws |
| per-visitor suggestion offer counts | DROPPED | decisions | cannot reach the companion's own four-hop rule; slot two is chosen for coverage over the published set |
| device orientation stored per account | DROPPED | decisions | a tilt permission belongs to a handset |
| optional opaque-token sync | REPLACED | decisions | built as the signed-in reader's server-side reading list |
| contact form, search, comments, light theme, page transitions | DROPPED | Constraints | companion S-15.4 |
| observed libraries (smoothing runtime, model loader, shaders) | DROPPED | decisions | observed implementation; INV9 mechanism pin |

## Slot obligations

| Slot | Provider | Status | Critical substep |
|---|---|---|---|
| backend | postgres | MET | `test_designer_creates_a_case_study_stored_as_a_draft`, `test_saved_case_study_is_stored_on_the_reading_list` |
| storage | minio | MET | `test_uploaded_image_lands_in_the_bucket`, `test_draft_media_is_refused_outside_the_studio` |

## Grading surface

- workflows: **16** (band 10 to 16 for solo_founder); browser substeps **87**; pytest substeps **90**; critical **10**
- non-happy-path ids: `work_index_with_empty_or_invalid_filters`, `draft_case_study_cannot_be_reached_by_the_public`, `invalid_or_incomplete_case_study_is_refused`, `invalid_reading_progress_is_refused`, `reader_cannot_reach_the_studio_or_another_readers_list`, `unauthenticated_requests_are_denied`, `signup_with_invalid_input_is_refused`
- pytest categories: {'presentation': 13, 'core_outcome': 3, 'business_rule': 20, 'data_integrity': 22, 'validation': 18, 'security': 14}
- test module: `tests/test_output.py`, **90** tests over core features, authorization, data integrity, edge cases and the storage slot; citations in `_handoff/S_conte_cont_motion-portfolio-dossier-vb_20260916_095602.pytest-provenance.json`
- checklist: **564** items; every one cited (G24), browser citations sharing wording with their step
- traceability: `tests/traceability-matrix.md` and `.csv`, regenerated by the sweep
- rubric: **21** judged criteria, 18 positive / 3 negative; reference rubric 24 compiled items (share 1.00)

| Dimension | Positive points | Share | Target |
|---|---|---|---|
| instruction_following | 12 | 0.30 | 0.30 |
| functionality | 8 | 0.20 | 0.25 |
| ux_flow | 5 | 0.12 | 0.15 |
| ui_visual | 9 | 0.23 | 0.15 |
| motion | 2 | 0.05 | 0.05 |
| accessibility | 2 | 0.05 | 0.05 |
| responsiveness | 2 | 0.05 | 0.05 |

## Literals ledger

| Class | Count | Examples | Carriers |
|---|---|---|---|
| account | 3 | `designer@example.com`, `reader@example.com`, `reader2@example.com` | conftest.py, instruction.md, test_output.py, workflows.yaml |
| credential | 1 | `deku-demo-pw-2026` | conftest.py, instruction.md, test_output.py, workflows.yaml |
| design_phrase | 6 | `one warm band`, `near-black neutral`, `brightness alone` | instruction.md, workflows.yaml |
| endpoint | 14 | `access_token`, `/api/health`, `/api/case-studies` | conftest.py, instruction.md, test_output.py |
| env_var | 8 | `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET` | conftest.py, instruction.md, task.toml |
| motion_moment | 8 | `inverts as they pass`, `settling a beat after`, `one character at a time` | instruction.md, workflows.yaml |
| number | 12 | `0.95`, `0.5`, `512` | conftest.py, instruction.md, task.toml, test_output.py, workflows.yaml |
| route | 11 | `/work`, `/privacy`, `/reading-list` | conftest.py, instruction.md, test_output.py, workflows.yaml |
| scheme | 2 | `reading_memory`, `case-studies/{case_study_id}/{sha256_of_bytes}.{ext}` | conftest.py, instruction.md, test_output.py, workflows.yaml |
| seed_record | 37 | `kestra-band`, `A Wearable That Knew When to Stay Quiet`, `Marisol Andrade` | conftest.py, instruction.md, test_output.py, workflows.yaml |
| status | 17 | `verity-biotics`, `brand-creative`, `spatial-experience` | conftest.py, instruction.md, task.toml, test_output.py, workflows.yaml |

## Spec documents (authoring aids, outside the bundle)

- `Output/_spec/S_conte_cont_motion-portfolio-dossier-vb_20260916_095602/00-decisions.md` fed every judgment call, the draws and the companion carry table
- `Output/_spec/S_conte_cont_motion-portfolio-dossier-vb_20260916_095602/01-PRD.md` fed Overview, User roles, Constraints
- `Output/_spec/S_conte_cont_motion-portfolio-dossier-vb_20260916_095602/02-TRD.md` fed Technical requirements and the Dockerfile base
- `Output/_spec/S_conte_cont_motion-portfolio-dossier-vb_20260916_095602/03-app-flow.md` fed User flow
- `Output/_spec/S_conte_cont_motion-portfolio-dossier-vb_20260916_095602/04-uiux-brief.md` fed UI/UX notes and Front-end specification
- `Output/_spec/S_conte_cont_motion-portfolio-dossier-vb_20260916_095602/05-backend-schema.md` fed Data model and User roles
- `Output/_spec/S_conte_cont_motion-portfolio-dossier-vb_20260916_095602/06-implementation-plan.md` author-side only; no Build plan at baseline

## Grading window

```
core_features  Core features     11600       2400  past-slice
user_flow      User flow          4336       1900  past-slice
ui_ux_notes    UI/UX notes        4602       1700  past-slice
constraints    Constraints         813        800  over-reference
user_roles     User roles         1685       1000  over-reference
overview       Overview           1467        700  over-reference
joined total                     24503       8800  past-slice
first four                       21351       7100  over-reference
```
Core features runs past the judge's slice. Rules 1 and 2, the publish boundary and the object store, sit inside it. Length is reported, never failed (G33).

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
| G7/G8/G9/G32/G45 | workflow_lint.py | 0 | PASS | 25 |
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
- G42 `corpus_overlap.py` against the two sibling portfolio bundles: PASS, no cross-archetype pair above 60% substep overlap
- G49 `diversity_lint.py`: no finding names this bundle (a Technical requirements run shared with sibling bundles was rewritten)
- G61 `corpus_report.py`: NOT-APPLICABLE, no admissible bundle in the ledger yet
- G22 `overlap.py`: NOT-APPLICABLE, this archetype has no sibling variant

Prompt receipts (G40): `_handoff/S_conte_cont_motion-portfolio-dossier-vb_20260916_095602.receipts.json`. The seven certification prompts were run by independent subagent reviewers in separate contexts; the six generator prompts carry `self` receipts. G3 VALID; G34 brief PASS, 2 WARN, 1 NOT-APPLICABLE; G34 spec PASS; G35 PASS, 1 WARN, 6 NOT-APPLICABLE; G36 PASS, 1 WARN, 5 NOT-APPLICABLE; G37 PASS; G53 PASS, 1 WARN.

## Corrections made during the QC passes

- QC_instruction (3 cycles):
  - rule 10 no longer adds anything to a first visit; the question markup stays hidden until the browser has something to keep;
  - create defaults, the studio top bar, publish refusal fields and copy, the reserved-slug message, the reader studio refusal and the withdraw confirmation are pinned;
  - five named hero film tiles, matching UI/UX;
  - the tilt answer and sort/view fall under the consent rule;
  - sign-in also sets an HttpOnly, Secure session cookie;
  - UI/UX is reordered (Motion, Accessibility and Responsive inside the judge's cut) and gains a Components paragraph;
  - the refused reader is the first journey, and the evaluator is renamed the prospective client;
  - Constraints are tidied, `completed` is computed on read, and the Definition of done is trimmed.
- QC_spec (3 cycles):
  - 04 now carries the literal token, curve, duration, spacing and accessibility values;
  - 06 gains phase 11;
  - 03 has numbered journeys plus "Limits and tokens", "API" and "Pinned strings" sections;
  - 05 adds named constraints, create defaults, `last_seen` and a chapter seed table;
  - 00 gains a one-line Decision index, three named routes, the verbatim pattern-row quote and notes for restated draws.
- qc_docker: `tests/Dockerfile` pins `deku-verifier-base:0.2`; the package lists are build-only ARGs placed directly after `ARG NODE_MAJOR`; the npm cache is cleaned.
- qc_toml: the turns and tokens budget is 200 / 7,500,000; the non-template `rubric_version` key was removed from `[metadata]`; ENV-006 stays a WARN as the corpus credential convention.
- qc_rubric (3 cycles):
  - 17 criteria were rewritten, and the link-blue and tablet-name checks moved to browser substeps (21 criteria, 3 negative);
  - nominal item claims were re-homed, and R17 now grades a new featured-hover item;
  - the R3, R8, R11 and R16 rules now have exhaustive no cases.
- qc_solution_checklist (3 cycles):
  - the checklist grew from 482 to 564 items and from 303 to 578 pinned rows, covering every API shape, chapter route, catalogue row, overlay string and accessibility rule;
  - the C-DD section was not added, because checklist_qc allows eleven codes and the Definition of done restates rule 8.
- Tests (still 90) were strengthened:
  - every chapter table is checked, along with the detail, list, entry and studio-list shapes;
  - catalogue product, end year, ongoing flag, template and placement are checked;
  - also the draft template, placement and chapters, the seeded `last_seen`, the publish refusal `field` values and the create defaults;
  - the draft not-found page must match a never-existing address, and the privacy page contents are checked.

## Handoff gates (undecided)

See `S_conte_cont_motion-portfolio-dossier-vb_20260916_095602.handoff.md`. G13, G15, G18, G19, G20, G21, G25 need Docker and the harness; the kit ran none of them.

## Blocking findings

- None prevent a required test.
- Unobservable to all three channels, discharged by the handoff gates (D-H): `/app/USER_README.md` contents, the reserved directories, one log line per request, the drawn stack names, and reading configuration from the environment.
- Observable only by absence on the desktop grader: the tilt permission gate and its copy render only on a permission-gated handset.
- Companion reconstructions (list entrance travel, nav meter fill, hero entrance, rendering surface contents, contact band, card placement, phone threshold, focus ring) are specified by behaviour; a tuning pass is expected once they run.

## Budget

`turns_expected = 200`, `tokens_expected = 7500000`: a seven-band home page, two case-study templates with eleven seeded documents, four extension systems, a studio, a server-backed reading list and two slots. Hard-to-expert tier of `prompts/toml_generator.md` 10.2.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
NOT ADMISSIBLE
```
