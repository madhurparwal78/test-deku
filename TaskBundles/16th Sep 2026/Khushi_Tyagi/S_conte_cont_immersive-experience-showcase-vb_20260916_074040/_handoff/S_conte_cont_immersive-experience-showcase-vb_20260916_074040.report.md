# Build report: S_conte_cont_immersive-experience-showcase-vb_20260916_074040

| | |
|---|---|
| Task code | `S_conte_cont_immersive-experience-showcase-vb_20260916_074040` |
| Task id | `deku/immersive-experience-showcase-vb` |
| Cell | solo_founder / content-publishing / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | `backend = postgres`, `storage = minio` |
| Variant | `b` on `spec_sections`, `critical_depth`, `data_shape` |
| Language | `python` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field, gate battery G0 to G63 |
| Grader pin | `0.22.0` |
| Target schema | `1.4` |
| Verifier mode | `separate` |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Source

One companion document was supplied with the Task Order, a 6,328-line build
specification for a realtime three-dimensional studio showcase. `source_lint.py`
(G51) reports **420 of 420 topics**, **1,260 of 1,260 enumerated items** and
**11 of 11 source colours** carried into `instruction.md`, with nine declared
waivers recorded in `_spec/<code>/00-decisions.md`.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Content model, six types, controlled discipline vocabulary | INCLUDED | `## Core features` | the pattern's authoring surface; graded by four pytest checks and one workflow |
| The draft gate and the server-verified preview token | INCLUDED | `## Core features` | the critical focus; six pytest checks, three of them critical |
| Four-state publish boundary with a role split | INCLUDED | `## Core features` | the companion's central mechanic; producer refusal graded critical |
| Cross-record publish gate, nine rules | INCLUDED | `## Core features` | one seeded record is gated by a deriving media; graded critical |
| Append-only publish log | INCLUDED | `## Core features` | the one audit surface; removal attempt graded critical |
| Curated home reel as an explicit ordered list | INCLUDED | `## Core features` | separable from the collection; four pytest checks and one workflow |
| Media pipeline into content-addressed object storage | INCLUDED | `## Core features` | the storage slot's obligation; six pytest checks, four of them critical |
| Mailing list intake that never discloses membership | INCLUDED | `## Core features` | the one anonymous write path; graded critical |
| Behind the scenes reel with the captioning constraint | INCLUDED | `## Core features` | the accessibility rule enforced in the schema; graded critical |
| Virtual scroller, persistent scene, nine-level opacity system | INCLUDED | `## Front-end specification` | the companion's largest surface; judged by eight rubric criteria |
| Launch surface: privacy page, security headers, form validation, spam protection, no frontend secrets | INCLUDED | `## Core features` | the reference/O draw, four pytest checks |
| Mail delivery of the confirmation | DROPPED | - | no mail slot; the companion composes the confirmation into an outbox row and the link is the state change |
| Third-party analytics, consent management or tag vendor | DROPPED | - | no run-time third-party call is available; the consent gate and the four measured events survive |
| Client portal, invoice, price, payment | DROPPED | - | the companion states each as out of scope; the mailbox is the pipeline |
| Realtime collaboration on a record | DROPPED | - | the companion settles on a version conflict at this team size |
| Binary assets: models, photographs, video, fonts, sound | DROPPED | - | the zero asset substitution section replaces every class with a generator recipe |
| `## Build plan` | DROPPED | - | not baseline (generate_instruction.md section 2.1) |

## Slot obligations

| Slot | Provider | Status | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_publish_log_row_is_written_for_every_transition` (critical), `test_producer_publish_transition_is_denied_and_state_is_unchanged` (critical), `test_preview_token_is_stored_as_a_hash`, plus eleven further row assertions |
| `storage` | `minio` | MET | `test_media_master_is_stored_in_the_bucket_at_its_content_hash` (critical), `test_rendition_key_follows_the_content_addressed_shape` (critical), `test_rendition_bytes_live_in_the_bucket_and_nowhere_else` (critical) |

No slot is UNMET.

## Grading surface

| Workflows | 14 (solo_founder band 10 to 16) |
|---|---|
| Browser substeps | 23 |
| Pytest substeps | 49 |
| Critical substeps | 22 |
| Non-happy-path ids | 1: `producer_writes_a_draft_and_cannot_publish` |
| Pytest module | one, `tests/test_output.py`, 49 functions |
| Rubric criteria | 22 (19 positive, 3 negative) |
| Checklist items | 436 |

Sections the one module covers: the content model, the draft gate, the publish
boundary, the publish log, the home reel, the media pipeline, the intake,
authorization and the launch surface.

### Rubric dimension shares, against the frozen targets

| Dimension | Positive points | Share | Target | Delta |
|---|---|---|---|---|
| `instruction_following` | 16 | 0.225 | 0.30 | 0.075 |
| `functionality` | 13 | 0.183 | 0.25 | 0.067 |
| `ux_flow` | 8 | 0.113 | 0.15 | 0.037 |
| `ui_visual` | 9 | 0.127 | 0.15 | 0.023 |
| `motion` | 7 | 0.099 | 0.05 | 0.049 |
| `accessibility` | 15 | 0.211 | 0.05 | 0.161 |
| `responsiveness` | 3 | 0.042 | 0.05 | 0.008 |

## Literals ledger

| Class | Count |
|---|---|
| `account` | 4 |
| `copy` | 4 |
| `credential` | 1 |
| `enum` | 38 |
| `env_var` | 8 |
| `field` | 1 |
| `key` | 1 |
| `prefix` | 1 |
| `role` | 2 |
| `route` | 15 |
| `slug` | 12 |
| `title` | 7 |
| `token` | 1 |

95 pinned values, none of them `verifier_only`. `DB_ADMIN_URL` is the
one escape hatch and appears in `task.toml` `[verifier].env` alone; the four
`STORAGE_*` names are legitimately shared, because the verifier must interrogate
the same bucket the app wrote to. Every ledger value appears verbatim in
`instruction.md`, and `fixture_lint.py` (G6) proves the bijection in both
directions against the grader files.

## Authoring documents

| Document | Fed |
|---|---|
| `00-decisions.md` | every residual call, the eight draws, the companion carry table, the nine G51 waivers |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements`, `## Deployment contract` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing; `## Build plan` is not baseline |

## Grading window

| Section | Chars | Reference | Reaches the judge |
|---|---|---|---|
| `Core features` | 27565 | 2400 | first 2,500 |
| `User flow` | 6603 | 1900 | first 2,500 |
| `UI/UX notes` | 8710 | 1700 | first 2,500 |
| `Constraints` | 1655 | 800 | first 2,500 |
| `User roles` | 2566 | 1000 | first 2,500 |
| `Overview` | 2699 | 700 | first 2,500 |
| joined | 49798 | 8,800 | first 9,000 |

Every judged section runs past its reference length. `window_lint.py` (G33)
reports length and fails nothing, and the brief has no cap. What the judge does
not read is graded by the pytest layer or by a workflow substep instead; the
twenty-two judged criteria each carry their own facts and are decidable without
the brief, which `rubric_context_lint.py` (G52) checks.

## Kit gate log

Rendered from `_handoff/<code>.gates.jsonl`. Never transcribed.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS |
| `G1/G12` | `layout_lint.py` | 0 | PASS |
| `G46` | `structure_lint.py` | 0 | PASS |
| `G50` | `docker_lint.py` | 0 | PASS |
| `G55` | `runtime_deps_lint.py` | 0 | PASS |
| `G63` | `secret_lint.py` | 0 | PASS |
| `G48` | `truth_lint.py` | 0 | PASS |
| `G51` | `source_lint.py` | 0 | PASS |
| `G52` | `rubric_context_lint.py` | 0 | PASS |
| `G54` | `comment_lint.py` | 0 | PASS |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS |
| `G11` | `leak_scan.py` | 0 | PASS |
| `G33` | `window_lint.py` | 0 | PASS |
| `G4/G5` | `contract_lint.py` | 0 | PASS |
| `G43` | `prescription_lint.py` | 0 | PASS |
| `G44` | `disclosure_lint.py` | 0 | PASS |
| `G10` | `no_sdk_lint.py` | 0 | PASS |
| `G31` | `determinism_lint.py` | 0 | PASS |
| `G14` | `reward_path_lint.py` | 0 | PASS |
| `G27/G30` | `rubric_lint.py` | 0 | PASS |
| `G41` | `flag_lint.py` | 0 | PASS |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS |
| `G59/G60` | `codequality_lint.py` | 2 | ? |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS |
| `G6` | `fixture_lint.py` | 0 | PASS |
| `G24` | `coverage_map.py` | 0 | PASS |
| `G37` | `checklist_qc.py` | 0 | PASS |
| `G39` | `rubric_align_lint.py` | 0 | PASS |
| `G28/G29` | `channel_lint.py` | 0 | PASS |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN |
| `G0/INV5` | `vendor_check.py` | 0 | PASS |
| `G47` | `output_qc.py` | 0 | PASS |

## Prompt receipts

`prompt_receipt_lint.py` (G40) reports WARN: every certification prompt carries a
receipt with a verdict for each check it declares, and every one is
**SELF-ATTESTED**. The kit's rule is owner is not verifier; one agent authored and
reviewed this bundle, so these are recorded verdicts rather than independent ones.
Thirteen checks across five prompts are recorded as WARN with their evidence, each
naming a place where a QC prompt predates a later rule the gates now enforce.

## Blocking findings

None inside the kit's reach. Two things this bundle cannot decide for itself:

- No image digests are pinned in `[delivery.images]`. Minting one needs registry
  access the kit does not have, and fabricating a digest is forbidden. The operator
  pins them at packaging time.
- Nothing here has been compiled or run. See the handoff contract.

## Budget

`turns_expected = 160`, `tokens_expected = 5500000`. The medium band, at its upper
edge. Reasoning: two service slots, a twenty-one-table model, a four-state publish
boundary split across two roles, a server-verified capability token, a content
addressed derivation pipeline that must never leave a published route pointing at
a rendition that does not exist, and a front-end specification carrying a virtual
scroller, a persistent realtime scene and a zero asset substitution recipe for
every binary class. `difficulty` stays empty; calibration owns it.

## Exit state

**MECHANICALLY-GREEN, NO-SOLUTION.** Not admissible. No reference application
exists, and nothing in this bundle has been built or executed.

