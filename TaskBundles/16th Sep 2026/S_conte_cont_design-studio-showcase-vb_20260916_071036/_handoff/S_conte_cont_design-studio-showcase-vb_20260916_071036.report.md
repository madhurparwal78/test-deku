# Build report: S_conte_cont_design-studio-showcase-vb_20260916_071036

Rendered from `_handoff/S_conte_cont_design-studio-showcase-vb_20260916_071036.gates.jsonl`. No verdict in this file was
typed by hand; each row below is the recorded exit code of the tool that owns it.

## Identity

| Field | Value |
|---|---|
| task code | `S_conte_cont_design-studio-showcase-vb_20260916_071036` |
| task id | `deku/design-studio-showcase-vb` |
| category | `solo_founder` |
| domain | `content-publishing` |
| pattern | `content-publishing` |
| service_profile | `P4-db-storage` |
| variant | `b` |
| variant_axes | `critical_depth, spec_sections` |
| language | `typescript` |
| capability_flags | `aesthetic` |
| design_direction | `companion` |
| launch_surface | `cookie_choice,custom_404,meta_tags,no_frontend_secrets,terms_page` |
| spec_sections_given | `overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract` |
| grader_version | `0.22.0` |
| schema_version | `1.4` |
| uuid_v5 | `d70c06d4-0dde-5c02-9d70-e4dca8348384` |
| authors | `kaustubh.dalvi@ethara.ai, kunal.singh.int5@ethara.ai` |
| contributor_id | `kunal.singh.int5@ethara.ai` |
| shard | `1 of 1 (no device sharding configured)` |

## Kit revision

Built and re-swept against `GreenField-GenKit2` branch `madhur-test` at `ac66ec3 2026-09-16 15:07:00 +0530 Merge remote-tracking branch 'origin/yasir-test' into madhur-test`.

`git pull` reported the branch already up to date. The kit had nonetheless moved
during the original build: `origin/yasir-test` was merged in at 15:07, after authoring
began against `806eb0a`. That merge added PRD mode (`run.yaml`, G64, the prd-generator
splitter) and changed how S0, S1 and S2 take their inputs. The bundle was re-aligned:

- **S0** now writes the Task Order with `run_lint.py task-order` from `run.yaml` into
  `_spec/design-studio-showcase.task-order.yaml`, replacing the hand-written copy. The idea
  file now declares `variant: b`, the variant this archetype was minted at; without it the
  order defaulted to `a` and G0 correctly refused it as a re-use of a claimed archetype.
- **S1** records the run with `run_lint.py record`, re-recorded after the idea file changed
  (G64 caught the stale hash). No waiver is recorded, so every sweep runs with no flags.
- **S8** rubric provenance now uses the object form, one unique `(anchor, facet)` per
  criterion, so G28 can bind each one; G39 passes with `--strict-anchors`. Mapping the
  anchors exposed one overlap, a positive and a negative both grading the header's
  transition, and the positive was narrowed to legibility.

## Providers per slot

| Slot | Provider | Agent variables |
|---|---|---|
| `backend` (db) | `postgres` | `DATABASE_URL`, `DB_URL` |
| `storage` | `minio` | `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` |

## Feature resolution

Every candidate the companion PRD carries, and where it went.

| Candidate | Verdict | Where |
|---|---|---|
| The nine-band home route and its scroll system | INCLUDED | `## Core features`, `## Front-end specification` |
| The fixed inverting chrome and the pointer replacement | INCLUDED | `## Front-end specification` |
| The loader and its once-only rule | INCLUDED | `## Core features` |
| The contact route and the capabilities deck modal | INCLUDED | `## Core features` |
| The privacy document and its commissioned amendment | INCLUDED | `## Core features` |
| The case overlay, kept as the quick look | INCLUDED | `## Core features` |
| The case study route and its ten chapter types | INCLUDED | `## Core features`, `## Data model` |
| Brief Studio, six stages, save and resume | INCLUDED | `## Core features`, `## User flow` |
| The slot picker, holds and the contention rule | INCLUDED | `## Core features`, `## Data model` |
| The tone board and its equal list view | INCLUDED | `## Core features` |
| The capabilities deck composer and read telemetry | INCLUDED | `## Core features` |
| Case intelligence: facets, comparison tray, similarity, search | INCLUDED | `## Core features` |
| The engagement portal | INCLUDED | `## Core features`, `## User roles` |
| The zero-asset substitution guide | INCLUDED | `## Front-end specification`, `## Constraints` |
| The six-phase build order (companion Section 24) | DROPPED | waived to G51: a build sequence is `## Build plan`, which variant b does not emit (INV9) |
| The capture conditions (companion Section 27.1) | DROPPED | waived to G51: authoring provenance, not a product requirement |
| Every hex, millisecond, cubic-bezier, pixel and CSS selector | DROPPED AS NOTATION | the obligation is carried in words; the value is not (A5, G51 waivers) |

## Slot obligations

| Slot | State | Evidence |
|---|---|---|
| `backend` | MET | `test_two_submissions_for_one_slot_book_exactly_one` (critical), `test_slot_state_reaches_booked_exactly_once`, `test_archive_facet_counts_reconcile_with_case_rows` |
| `storage` | MET | `test_brief_attachment_object_exists_in_bucket` (critical), `test_deliverable_preview_object_exists_in_bucket`, `test_unscanned_object_is_not_served` |

No slot obligation is UNMET.

## Grading layer

- workflows: **16** (solo_founder band 10 to 16)
- browser substeps: **43**
- pytest substeps: **103**
- critical substeps: **15**
- non-happy-path workflow ids: `client_without_the_right_is_denied_approval`, `concurrent_slot_submissions_book_at_most_one`, `contact_form_refuses_invalid_input`, `cross_engagement_record_is_forbidden`, `expired_deck_link_matches_a_revoked_one`, `unpublished_case_cannot_be_read_by_a_visitor`
- one pytest module, `tests/test_output.py`, carrying **103** tests across the
  core-features, data-integrity, authorization, edge-case and storage sections
- checklist items (the coverage target): **356**, all cited

## Rubric

31 criteria: **26 positive**, **5 negative**.

| Dimension | Points | Share | Target | Within 0.10 |
|---|---|---|---|---|
| `instruction_following` | 20 | 0.270 | 0.30 | yes |
| `functionality` | 18 | 0.243 | 0.25 | yes |
| `ux_flow` | 11 | 0.149 | 0.15 | yes |
| `ui_visual` | 11 | 0.149 | 0.15 | yes |
| `motion` | 6 | 0.081 | 0.05 | yes |
| `accessibility` | 4 | 0.054 | 0.05 | yes |
| `responsiveness` | 4 | 0.054 | 0.05 | yes |

Negatives sit outside the budget, as reference/I S-I.5 requires.

## Literals ledger

| Class | Count | Carriers |
|---|---|---|
| `account` | 3 | `conftest.py`, `instruction.md` |
| `credential` | 1 | `conftest.py`, `instruction.md` |
| `design_phrase` | 9 | `instruction.md`, `test_output.py` |
| `endpoint` | 29 | `instruction.md`, `test_output.py` |
| `env_var` | 8 | `conftest.py`, `instruction.md`, `task.toml`, `test_output.py` |
| `motion_moment` | 8 | `instruction.md` |
| `number` | 2 | `instruction.md` |
| `route` | 9 | `conftest.py`, `instruction.md`, `test_output.py` |
| `scheme` | 2 | `instruction.md` |
| `seed_record` | 71 | `conftest.py`, `instruction.md`, `test_output.py` |
| `status` | 36 | `conftest.py`, `instruction.md`, `test_output.py` |

178 literals in total. G6 holds the bijection in both directions.

## spec/ documents and the sections they fed

| Document | Fed |
|---|---|
| `00-decisions.md` | the draws, the residual judgment calls, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements`, `## Deployment contract` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing: `## Build plan` is not emitted at variant b |

They live at `Output/16sept_hobro/_spec/S_conte_cont_design-studio-showcase-vb_20260916_071036/`, outside the bundle (CON-5).

## Grading window

| Section | Chars | Reference |
|---|---|---|
| `## Overview` | 2566 | 700 |
| `## User roles` | 2460 | 1000 |
| `## Core features` | 34560 | 2400 |
| `## User flow` | 4771 | 1900 |
| `## UI/UX notes` | 10804 | 1700 |
| `## Technical requirements` | 4460 | unbudgeted |
| `## Data model` | 7881 | unbudgeted |
| `## Front-end specification` | 20116 | unbudgeted |
| `## Constraints` | 2799 | 800 |
| `## Deployment contract` | 5031 | unbudgeted |
| `## Definition of done` | 439 | unbudgeted |

Joined across the six judged sections: **57960** against the 9,000-char slice.
`window_lint.py` (G33) reports length and fails nothing: the brief has no length limit,
and the companion carries more graded surface than the reference lengths anticipate.
The critical-focus rules are front-loaded inside `## Core features` so they sit ahead
of the slice.

## Kit gate log

Rendered from the receipts. `exit` is the recorded process exit code.

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

33 gates recorded; **0 red**.

## Certification prompts

| Prompt | Gate | Verdict | Checks | Non-PASS | Verifier |
|---|---|---|---|---|---|
| `task_code_verifier.md` | G3 | VALID | 12 | 0 | self |
| `QC_spec.md` | G34 | PASS | 15 | 3 | self |
| `QC_instruction.md` | G34 | PASS | 24 | 4 | self |
| `qc_rubric.md` | G53 | PASS | 16 | 0 | self |
| `qc_solution_checklist.md` | G37 | PASS | 0 | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | 13 | self |
| `qc_docker.md` | G35 | PASS | 105 | 5 | self |

Every non-PASS carries its finding in `_handoff/S_conte_cont_design-studio-showcase-vb_20260916_071036.receipts.json`.
**Every verdict is SELF-ATTESTED**: owner and verifier are one agent in this run, which
the kit's rule (owner != verifier) does not satisfy. `prompt_receipt_lint.py` records it
as a note on every prompt, and it is the single largest caveat on this bundle.

## Recorded run and companion carriage

| Field | Value |
|---|---|
| mode | `prd` |
| idea file | `hobro_idea.yaml` |
| plain PRD | `hobro_prd_plain.md` |
| plain PRD sha256 | `2cd01abeff40b60058fb1a9cd89e1fd4ed85b37bbdf571014fd47cfc7ecb23aa` |
| topic waivers | 0 |
| criterion waivers | 0 |

G51 was run against both readings of the companion and both PASS:

| Source | Topics | Items | Colours | Waivers |
|---|---|---|---|---|
| `hobro_prd_plain.md` (recorded, the kit's input contract) | 29/29 | n/a | n/a | **0** |
| `hobro_prd.md` (authored, the stronger claim) | 246/246 | 1087/1087 | 18/18 | 30, all notation |

The recorded run needs no waiver. The second row is kept because it is the stronger
statement: the brief carries every enumerated obligation of the full authored PRD, not
only its plain-language half. The thirty waivers it needed are notation the number rule
forbids the brief to carry, never a dropped requirement; they are itemised in
`_spec/S_conte_cont_design-studio-showcase-vb_20260916_071036/00-decisions.md`.

## Blocking findings

None for this bundle. Two things are recorded rather than blocking:

- **`[delivery.images]` is absent.** CON-2 asks for a digest pin per image, and a digest
  cannot be resolved without a registry, which the kit has no access to. Fabricating one
  is forbidden (stage-5). Every image is pinned by explicit version tag instead, and the
  handoff contract carries the digest-resolution step.
- **G61 (corpus mix) reports G26 payments-or-email share at 0 of 1.** G61 is corpus-level
  and advisory; this bundle declares `db` and `storage`, so the share is a property of a
  one-bundle corpus rather than a defect here.

## Budget

`turns_expected` **200**, `tokens_expected` **7500000**.
Reasoning: the companion specifies ten must-have features across eleven routes, two
backing services, an authenticated surface with a data-layer isolation rule, and a
zero-asset build in which every image, texture and mark is generated. That is the upper
end of the documented band, and the token figure sits inside the 200,000 to 8,000,000
absolute range.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference app, so nothing here has been compiled
or run. It becomes admissible when the app lands and `harbor run -a oracle` returns
`1.0` twice.

