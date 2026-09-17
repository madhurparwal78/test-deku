# Build report - S_conte_cont_immersive-portfolio-ascent-vb_20260916_100808

## Identity

| Field | Value |
|---|---|
| task code | `S_conte_cont_immersive-portfolio-ascent-vb_20260916_100808` |
| task id | `deku/immersive-portfolio-ascent-vb` |
| cell | solo_founder / content-publishing / content-publishing |
| archetype | `immersive-portfolio-ascent` |
| service_profile | `P4-db-storage` |
| providers | backend `postgres`, storage `minio` |
| variant | `b`, axes `critical_depth` + `spec_sections` |
| language | `typescript` (SvelteKit on Node 20 fronting FastAPI on Python 3.12) |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 (single-operator run) |
| companion | `PRD/laurens_prd.md`, recorded in `_handoff/<code>.sources.json` |
| contributor | kunal.singh.int5@ethara.ai |
| QL | kaustubh.dalvi@ethara.ai |

## Feature resolution

| Candidate | Verdict | Graded in | Reason |
|---|---|---|---|
| The immersive home journey | INCLUDED | tests/test_output.py | server-computed bands at GET /api/journey; 5 pytest checks |
| The contact form | INCLUDED | tests/test_output.py | row in PostgreSQL plus the console read |
| Case study hub and detail | INCLUDED | tests/test_output.py + rubric R4 | record fields by API, rendered rail by judge |
| Playground and highlights overlays | INCLUDED | rubric R7, R8 | overlay return position is not deterministic |
| Curriculum vitae | INCLUDED | tests/test_output.py + rubric R13 | selectedWork by API, print output by judge |
| The peer review workflow | INCLUDED | tests/test_output.py | 9 pytest checks across state, denial and freeze |
| The case study composer | INCLUDED | tests/test_output.py | findings shape and the failure_required rule |
| Installation telemetry | INCLUDED | tests/test_output.py | idempotent ingest, trust floor, frozen figures |
| Ranked corpus search | INCLUDED | tests/test_output.py | type weights and group order |
| Capability ladder and the flat build | INCLUDED | rubric R3, R11, R12 | rung selection is measured in the browser, not assertable over HTTP |
| custom_404 | INCLUDED | tests/test_output.py | status plus the pinned heading and link |
| mobile_viewport | INCLUDED | rubric R13 + narrow_page fixture | no sideways overflow at phone width |
| no_broken_links | INCLUDED | tests/test_output.py | sitemap round-trip against the public route set |
| page_view_log | INCLUDED | tests/test_output.py | route and time only, console read |
| sitemap_robots | INCLUDED | tests/test_output.py | absolute URLs under APP_PUBLIC_URL, no private route |
| Real hardware devices | DROPPED | - | out of scope by the PRD: telemetry is exercised through its HTTP ingest contract alone |
| Outbound email | DROPPED | - | no mail provider exists in this environment; confirmation happens in the reviewer's own page |

## Slot obligations

| Slot | Verdict | Observing tests |
|---|---|---|
| backend (postgres) | MET | test_owner_upload_is_stored_in_the_bucket_under_its_sha256_object_key (critical), test_contact_message_is_persisted_as_a_row_the_owner_reads (critical), test_telemetry_event_triple_is_stored_exactly_once (critical) |
| storage (minio) | MET | test_owner_upload_is_stored_in_the_bucket_under_its_sha256_object_key (critical), test_identical_uploads_leave_exactly_one_stored_object_and_row (critical), test_published_media_file_is_served_byte_for_byte_from_the_object_store |

## Grading surface

- workflows: 16 (category band for solo_founder is 10 to 16)
- browser substeps: 28 | pytest substeps: 55 | browser ratio 0.51 (G45 band 0.40 to 2.00)
- critical substeps: 14
- category mix: {'business_rule': 12, 'core_outcome': 1, 'data_integrity': 12, 'presentation': 5, 'security': 13, 'validation': 12}
- non-happy-path workflow ids (10): invalid_journey_request_is_refused, invalid_contact_submission_is_refused, visitor_searches_and_an_empty_search_offers_suggestions, owner_uploads_project_media_and_a_duplicate_leaves_one_object, invalid_media_upload_is_refused, draft_work_and_its_media_cannot_be_read_by_the_public, expired_invitation_and_invalid_review_are_refused, unpublished_review_cannot_reach_the_public_wall, reviewer_and_signed_out_caller_are_denied_the_console, telemetry_ingest_is_denied_without_a_device_key
- pytest module: one, `tests/test_output.py`, carrying the core-features, data-integrity, authorization and edge-case sections plus the db and storage slot observations
- rubric criteria: 16 (13 positive, 3 negative), positive total 45

| Dimension | Target | Share | Criteria |
|---|---|---|---|
| instruction_following | 0.30 | 0.29 | 3 |
| functionality | 0.25 | 0.24 | 3 |
| ux_flow | 0.15 | 0.13 | 2 |
| ui_visual | 0.15 | 0.13 | 2 |
| motion | 0.05 | 0.07 | 1 |
| accessibility | 0.05 | 0.07 | 1 |
| responsiveness | 0.05 | 0.07 | 1 |

## Coverage

- checklist items: 436, every one cited by at least one grader (G24 forward and reverse)
- pytest citations: 204 across 55 test functions
- rubric citations: 127 across 16 criteria
- browser substep citations: 105, wording-checked against the item each claims (G24 `check_cov_earned`)
- traceability matrix: `tests/traceability-matrix.md` and `.csv`, regenerated by every sweep from the same scan G24 decides on

## Literals ledger

305 values a grader may assert, each present verbatim in `instruction.md` and in at least one grader file. Classes:

- `account`: 3
- `credential`: 1
- `literal`: 301

Seeded accounts, all on `deku-demo-pw-2026`: `owner@example.com` (owner), `reviewer@example.com`, `reviewer2@example.com` (reviewer).

## Spec documents and the sections they fed

| Document | Fed |
|---|---|
| `00-decisions.md` | the draws, the residual judgment calls and the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements`, `## Deployment contract` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | withheld: variant `b` drops `## Build plan` on the spec_sections axis |

## Grading window

| Section | Chars | Target | Judge sees |
|---|---|---|---|
| core_features | 17756 | 2400 | 2500 |
| user_flow | 4131 | 1900 | 2500 |
| ui_ux_notes | 4650 | 1700 | 2500 |
| constraints | 931 | 800 | 931 |
| user_roles | 2152 | 1000 | 2152 |
| overview | 2199 | 700 | 2199 |
| joined, each capped at 2500 | 12782 | 9000 | within the join cap |

`## Core features` runs well past its target, so the run_rubric judge reads only its first 2500 characters. window_lint (G33) passes because the brief carries no length limit, and the exposure is closed from the other side: every judged criterion carries its own facts rather than pointing at the brief (G52), so the judge never depends on the excerpt.

## Kit gate log

Rendered from `_handoff/<code>.gates.jsonl`. No verdict on this page was typed by hand.

| Gate | Tool | Exit | Verdict | Receipt |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | ok |
| G1/G12 | `layout_lint.py` | 0 | PASS | ok |
| G46 | `structure_lint.py` | 0 | PASS | ok |
| G50 | `docker_lint.py` | 0 | PASS | ok |
| G55 | `runtime_deps_lint.py` | 0 | PASS | ok |
| G63 | `secret_lint.py` | 0 | PASS | ok |
| G48 | `truth_lint.py` | 0 | PASS | ok |
| G51 | `source_lint.py` | 0 | PASS | ok |
| G52 | `rubric_context_lint.py` | 0 | PASS | ok |
| G54 | `comment_lint.py` | 0 | PASS | ok |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | ok |
| G11 | `leak_scan.py` | 0 | PASS | ok |
| G33 | `window_lint.py` | 0 | PASS | ok |
| G4/G5 | `contract_lint.py` | 0 | PASS | ok |
| G43 | `prescription_lint.py` | 0 | PASS | ok |
| G44 | `disclosure_lint.py` | 0 | PASS | ok |
| G10 | `no_sdk_lint.py` | 0 | PASS | ok |
| G31 | `determinism_lint.py` | 0 | PASS | ok |
| G14 | `reward_path_lint.py` | 0 | PASS | ok |
| G27/G30 | `rubric_lint.py` | 0 | PASS | ok |
| G41 | `flag_lint.py` | 0 | PASS | ok |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | ok |
| G59/G60 | `codequality_lint.py` | 2 | ? | ok |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | ok |
| G6 | `fixture_lint.py` | 0 | PASS | ok |
| G24 | `coverage_map.py` | 0 | PASS | ok |
| G37 | `checklist_qc.py` | 0 | PASS | ok |
| G39 | `rubric_align_lint.py` | 0 | PASS | ok |
| G28/G29 | `channel_lint.py` | 0 | PASS | ok |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | ok |
| G0/INV5 | `vendor_check.py` | 0 | PASS | ok |
| G47 | `output_qc.py` | 0 | PASS | ok |

32 of 32 gate rows green; 0 red.

## Adversarial prompt gates

| Gate | Prompt | Verdict | Checks | Verifier |
|---|---|---|---|---|
| G3 | `task_code_verifier.md` | VALID | 12 PASS | self (SELF-ATTESTED) |
| G34 | `QC_spec.md` | PASS | 14 PASS, 1 WARN | self (SELF-ATTESTED) |
| G34 | `QC_instruction.md` | PASS | 21 PASS, 3 WARN | self (SELF-ATTESTED) |
| G35 | `qc_docker.md` | PASS | 6 NOT-APPLICABLE, 99 PASS | self (SELF-ATTESTED) |
| G36 | `qc_toml.md` | PASS | 10 NOT-APPLICABLE, 109 PASS, 1 WARN | self (SELF-ATTESTED) |
| G37 | `qc_solution_checklist.md` | PASS | no registry | self (SELF-ATTESTED) |
| G53 | `qc_rubric.md` | PASS | 16 PASS | self (SELF-ATTESTED) |

Every row is SELF-ATTESTED: one agent authored the artifact and ran its reviewer, so the kit's owner-is-not-verifier rule is not satisfied. These are recorded verdicts, never independent ones. The findings each review raised, and the fixes applied, are in `_handoff/<code>.receipts.json`.

## Findings carried forward

Repaired during this run:

1. `tests/rubric.json` R5 restated R15's negative, so one observation moved the score twice (qc_rubric RC-03). R5's rule now turns on the attribution line.
2. `tests/rubric.json` R3 graded a presence assertion the pytest layer already owned (RC-04). R3 now grades the document form.
3. Five product terms were used in criteria with no definition for a judge reading one criterion cold (RC-07). Each is bound in its own rule now.
4. `C-TR-13` and `C-TR-14` pin the seven per-component journey bands, and the suite asserted component NAMES only. Both journey tests now assert every component start and end on both branches.
5. `[environment].env` carried `DB_URL`, an off-canon duplicate of `DATABASE_URL` the brief never names (qc_toml ENV-006). Removed.
6. One compose line ran to 213 characters (qc_docker BP-020). Folded to a block scalar with a byte-equivalent resolved command.

Open, and recorded rather than repaired:

1. `## Core features` is 17756 characters against a 2400 target. See the grading window section above for why this is recorded rather than cut.
2. `[metadata].language` is `typescript` on a task whose JSON API is FastAPI on Python. The enum holds one value and the task is genuinely two-language; `typescript` names the half that owns the public listener.
3. `## UI/UX notes` bans overshoot in interface motion while `Atmosphere` gives each bird an overshoot on its wing recovery. Different subjects, neither graded.
4. `## Data model` reads `so a grader can sign in`. It names an external checker without locating it outside the app, so it sits below the QC_instruction D4 blocker bar.

G51 waivers (34), each a reference-implementation internal the brief deliberately states behaviourally rather than prescribing (fluid-simulation shader constants, liquid-type tuning values, CSS root class names, SVG path data, `.glb` model files the brief forbids shipping, and three PRD meta sections). The list is `_handoff/g51-waivers.txt` and every sweep must pass it:

- `normative versus informational`
- `the splat program, verbatim`
- `acceptance checklist`
- `splat injecting velocity`
- `feimage`
- `ridged noise`
- `will-change`
- `sb-w`
- `sharpen 18`
- `stagger 0.18`
- `entrysharpen`
- `fillimagescale`
- `1 splat inject velocity`
- `2 curl compute vorticity`
- `4 divergence compute`
- `6 pressure jacobi`
- `gradientsubtract`
- `8 advection advect`
- `simresolution`
- `dyeresolution`
- `densitydissipation`
- `velocitydissipation`
- `pressureiterations`
- `curl 0 vorticity`
- `splatforce`
- `hostsplatradius`
- `maskgain`
- `flipvelx`
- `is-hero-boot`
- `tier changes mutate`
- `colour interpolation assert`
- `safe-area-inset-bottom`
- `<contactemail>`
- `characterwithputdowncompressed`

## Versions

| Field | Value |
|---|---|
| kit | `deku-green-field`, G38 self-test green, 32 checks |
| vendored grader | `0.22.0` (`tests/test.sh`, `solution/trinity/recompute.py`) |
| target schema | `1.4` |
| verifier mode | `separate` |
| rubric judge | `claude-sonnet-4-6`, rubric_version `1` |
| corpus canary | present in `solution/TRUTH.md` and `solution/USER_README.md` |

## Budget

`turns_expected = 200`, `tokens_expected = 7500000`. The brief carries ten must-have features, a ten-table schema, thirty-nine endpoints, a real-time scene and four separate rule systems (composer validation, telemetry trust, search ranking, the capability ladder). That is the top of the Standard tier rather than the middle, and the figure sits inside the 200000 to 8000000 band.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference app, so nothing here has been compiled or run. It counts toward no corpus target until the app lands downstream and `harbor run -a oracle` returns `1.0` twice.
