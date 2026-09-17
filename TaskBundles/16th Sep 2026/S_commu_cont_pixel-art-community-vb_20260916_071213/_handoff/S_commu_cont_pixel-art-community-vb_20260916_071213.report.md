# Build report: S_commu_cont_pixel-art-community-vb_20260916_071213

Rendered from `_handoff/S_commu_cont_pixel-art-community-vb_20260916_071213.gates.jsonl`. No verdict in this file was typed by hand.

## Identity

| | |
|---|---|
| Task code | `S_commu_cont_pixel-art-community-vb_20260916_071213` |
| Task id | `deku/pixel-art-community-vb` |
| Cell | solo_founder / community-social / content-publishing |
| Service profile | P4-db-storage |
| Providers | backend = postgres, storage = minio |
| Variant | `b`, axes `spec_sections`, `critical_depth` |
| Language | typescript |
| Design direction | `companion` (reference/L L.6.1; the bank drew `glass-depth`, which does not govern) |
| Launch surface | alt_text, mobile_viewport, no_frontend_secrets, single_cta, terms_page |
| Companion | `PRD/pixilart_prd_plain.md`, the plain projection of `pixilart_prd.md` |
| Run file | `PRD/pixilart_run.yaml`, PRD mode, recorded in `_handoff/<code>.sources.json` |
| Shard | 1 of 1 |
| Exit state | MECHANICALLY-GREEN, NO-SOLUTION |

## Gate log

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
| G64 | `run_lint.py` | 0 | PASS |
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

## Certification prompts

| Prompt | Gate | Checks answered | Verdict | Verifier |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | 24 | PASS | self |
| `QC_spec.md` | G34 | 15 | PASS | self |
| `qc_docker.md` | G35 | 105 | PASS | self |
| `qc_rubric.md` | G53 | 16 | PASS | self |
| `qc_solution_checklist.md` | G37 | 0 | PASS | self |
| `qc_toml.md` | G36 | 120 | PASS | self |
| `task_code_verifier.md` | G3 | 12 | VALID | self |

Every one is SELF-ATTESTED: one agent authored the artifact and ran its review, so the
kit's owner-is-not-verifier rule is recorded as unmet rather than claimed as met.
The generator prompts for S2, S3, S4, S5, S7 and S8 carry no receipt: the artifacts were
built from the stage files and the reference libraries, which is advisory rather than
blocking, and is recorded here rather than left to be discovered.

## Outstanding review findings

- `QC_instruction.md` C4: `## UI/UX notes` commits to a light interface by describing a near-white cool neutral ground, but never says in one sentence that light is the committed mode and dark is out of scope. A reader has to infer it from the palette roles.
- `QC_instruction.md` C7: `## Core features` is 56105 characters against the 2500-character point where the judge slices it. The tail reaches the agent in full and the judged criteria are self-contained, so this costs a diagnostic reading rather than reward, but the section is far past the window.
- `QC_spec.md` S7: 06-implementation-plan.md orders the phases by dependency but names no per-phase exit condition and no deploy phase. The document is authoring-side only and `## Build plan` is not emitted at baseline, so nothing downstream reads it.
- `QC_spec.md` S9: 05-backend-schema.md states the seed shape and defers the exact seeded values to the literals ledger and the brief rather than restating them. The values are pinned in both, so the concreteness lives one file away rather than being absent.
- `qc_docker.md` RUN-004: environment/Dockerfile pins `python:3.12-slim`, a tag that floats across patch releases. It is the shape docker_generator.md itself emits and G55 RD-3 documents the choice, so it is recorded rather than changed. The two sidecar images are pinned to an exact release.
- `qc_docker.md` BP-003: the same floating base tag is the one version-sensitive component left unpinned. NODE_MAJOR is pinned to 20 and both sidecar images carry exact release tags.
- `qc_docker.md` BP-004: the NodeSource setup script is piped into a shell with no integrity check. No checksum for it is published in any kit source, and this is the reference shape the kit's own images use.
- `qc_toml.md` SCHEMA-011: task.toml carries a `[delivery]` block. stage-4-task-toml.md and 01-OUTPUT-CONTRACT.md CON-2 require one on every new bundle; the qc_toml section 11 template predates that requirement and does not list it. The newer of the two kit documents was followed and the disagreement is recorded here.

## Feature resolution

| Companion area | Verdict | Where |
|---|---|---|
| Editor: canvas, tools, document, colour, export | INCLUDED | `## Core features` |
| Local persistence, autosave, versions, offline | INCLUDED | `## Core features` |
| Publishing to the object store, renditions, quota | INCLUDED | `## Core features` |
| Gallery feeds, cursors, popular snapshot, lineage | INCLUDED | `## Core features` |
| Profiles, handle namespace, follows, comments | INCLUDED | `## Core features` |
| Moderation states, review, audit chain | INCLUDED | `## Core features` |
| Search and discovery, with the image-search refusal | INCLUDED | `## Core features` |
| Home, art centre, not-found, consent, privacy, terms | INCLUDED | `## Core features` |
| Embeds, scoped tokens, webhooks, supporter tier | INCLUDED | `## Core features` |
| Design system, chrome, drawer, footer, icons, copy | INCLUDED | `## UI/UX notes`, `## Front-end specification` |
| Real-time collaborative drawing | DROPPED | no realtime slot in P4-db-storage; `## Constraints` |
| Multi-region placement and an edge cache tier | DROPPED | one process; `## Constraints` |
| Payment capture | DROPPED | no payments slot; the tier is an entitlement only |
| Email delivery | DROPPED | no email slot; notices are in-product notifications |
| Acceptance checklist (section 42) | DROPPED | a checklist of the other sections; naming it would state the exam (INV10). Waived on the record at G51 |

## Slot obligations

| Slot | Provider | State | Observing test |
|---|---|---|---|
| backend | postgres | MET | `test_like_count_equals_row_count`, `test_seeded_rows_appear_exactly_once` |
| storage | minio | MET | `test_published_artwork_object_exists_in_the_bucket`, `test_object_key_follows_the_pinned_scheme` |

## Grading surface

| | |
|---|---|
| Workflows | 16 (solo_founder band 10 to 16) |
| Browser substeps | 49 |
| Pytest substeps | 42 |
| Critical substeps | 10 |
| Non-happy-path workflow ids | 8: remix_of_an_ancestor_is_rejected, reader_cannot_publish_denied, author_cannot_modify_another_authors_piece_forbidden, private_piece_cannot_be_read_by_another_account, private_artwork_object_request_is_denied, unauthenticated_engagement_is_denied, duplicate_publish_key_creates_one_piece, invalid_submissions_are_refused |
| Test module | `tests/test_output.py`, 42 functions |
| Section banners |  |
| Checklist items | 356 |

Checklist items per section: C-CF 180, C-CN 12, C-DC 18, C-DM 24, C-FE 16, C-OV 6, C-RL 16, C-TR 26, C-UF 28, C-UX 30.

## Rubric

Criteria: 14 (14 positive, 0 negative). Positive score total 34.

| Dimension | Criteria | Share | Target |
|---|---|---|---|
| instruction_following | 2 | 0.294 | 0.3 |
| functionality | 2 | 0.235 | 0.25 |
| ux_flow | 2 | 0.118 | 0.15 |
| ui_visual | 5 | 0.206 | 0.15 |
| motion | 1 | 0.029 | 0.05 |
| accessibility | 1 | 0.088 | 0.05 |
| responsiveness | 1 | 0.029 | 0.05 |

The compiled reference rubric in `solution/trinity/rubrics.json` carries 18 items, all
`mode: compiled`, so the compiled weight share is 1.0 against a floor of 0.6.

## Literals ledger

92 literals, every one carried by at least one real file.

| Class | Count |
|---|---|
| account | 3 |
| credential | 1 |
| design_phrase | 6 |
| endpoint | 29 |
| env_var | 7 |
| motion_moment | 6 |
| number | 5 |
| route | 8 |
| scheme | 2 |
| seed_record | 16 |
| status | 9 |

## Grading window

| Section | Chars | Reference | |
|---|---|---|---|
| Overview | 2282 | 700 | over reference |
| User roles | 2317 | 1000 | over reference |
| Core features | 56105 | 2400 | past the judge's slice |
| User flow | 4095 | 1900 | past the judge's slice |
| UI/UX notes | 8904 | 1700 | past the judge's slice |
| Technical requirements | 14000 | unbudgeted |  |
| Data model | 6910 | unbudgeted |  |
| Front-end specification | 10641 | unbudgeted |  |
| Constraints | 1791 | 800 | over reference |
| Deployment contract | 4807 | unbudgeted |  |
| Definition of done | 480 | unbudgeted |  |

`## Core features` runs far past the 2500-character point where the judge slices it. The
tail reaches the agent in full, and every judged criterion carries its own facts, so the
cost is a diagnostic reading rather than reward. It is recorded rather than trimmed,
because cutting a real rule to fit the window trades completeness for a number.

## Authoring inputs

| spec/ document | Fed |
|---|---|
| `00-decisions.md` | the draws, the launch-surface draw, the companion carry table, the G51 waivers |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | authoring-side only; `## Build plan` is not emitted at baseline |

They live at `Output/16sept_pixilart/_spec/S_commu_cont_pixel-art-community-vb_20260916_071213/`, a sibling of the bundle, and never ship.

## Traceability

`tests/traceability-matrix.md` and `.csv` are regenerated by every sweep from the same scan
G24 makes, so they cannot disagree with the gate. They are not restated here.

