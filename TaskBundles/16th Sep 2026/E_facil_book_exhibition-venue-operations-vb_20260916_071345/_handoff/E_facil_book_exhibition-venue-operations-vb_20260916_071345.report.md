# Build report: Verwick Xpo

Rendered from `_handoff/E_facil_book_exhibition-venue-operations-vb_20260916_071345.gates.jsonl`.
No verdict below is transcribed; every row is the receipt the sweep wrote.

## Identity

| Field | Value |
|---|---|
| Task code | `E_facil_book_exhibition-venue-operations-vb_20260916_071345` |
| Task id | `deku/exhibition-venue-operations-vb` |
| Cell | enterprise / facilities-assets / booking-scheduling |
| Archetype | `exhibition-venue-operations` |
| Variant | `b` (companion-backed) |
| Variant axes | `critical_depth`, `spec_sections` |
| Service profile | `P1-db` |
| Providers per slot | `backend` = `postgres` |
| Language | `typescript` |
| Design direction | `companion` |
| Launch surface | `alt_text`, `colour_contrast`, `form_validation`, `mobile_viewport`, `terms_page` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit gate log | `_handoff/E_facil_book_exhibition-venue-operations-vb_20260916_071345.gates.jsonl` |

## Source material

A companion PRD was supplied with the Task Order and is carried in the bundle at
`_handoff/E_facil_book_exhibition-venue-operations-vb_20260916_071345.companion-prd.md`
(1,714 lines, 41 sections). G51 measured its carriage into `instruction.md`:

| Measure | Result |
|---|---|
| Colours described by family and tone | 13 of 13 |
| Topics carried | 59 of 59 |
| Enumerated items carried | 294 of 294 |
| Declared waivers | 1 (`--color-background, --color-light #ffffff page ground`) |

The one waiver is recorded in the handoff contract with its reason: the colour
reaches the brief as `near-white neutral`, and the row's remaining content words
are two CSS custom-property names and a hex value, neither of which may appear in
a brief under the A5 number rule.

## Feature resolution

| Candidate | Verdict | Landed in | Reason |
|---|---|---|---|
| Public site, three languages, 29 routes | INCLUDED | `## Core features`, `## User flow`, `## Front-end specification` | companion sections 2, 7 to 13, 38 |
| Campus space graph with combinations | INCLUDED | `## Core features`, `## Data model` | companion 15; the pattern's critical focus |
| Licensed capacity per space, layout and combination | INCLUDED | `## Core features`, `## Data model` | companion 9, 15 |
| Enquiry, ranked options, challenge, atomic confirmation | INCLUDED | `## Core features` | companion 16 |
| Phases as occupancy, turnaround, cascades, resources | INCLUDED | `## Core features` | companion 17, 26 |
| Floor-plan planner with live constraint validation | INCLUDED | `## Core features` | companion 18 |
| Accreditation, evidence expiry, delegation, cascade | INCLUDED | `## Core features` | companion 19 |
| Entrance modes, badges, scans, degraded entrance | INCLUDED | `## Core features` | companion 20 |
| Occupancy on the graph, exits, incidents, evacuation | INCLUDED | `## Core features` | companion 21 |
| Services, catering, technical orders with cut-offs | INCLUDED | `## Core features` | companion 22 |
| Invoicing in integer minor units, variance, disputes | INCLUDED | `## Core features` | companion 23 |
| Publishing, publication state, translations | INCLUDED | `## Core features` | companion 24 |
| Exhibitor portal scoped to one stand | INCLUDED | `## Core features` | companion 25 |
| Reporting across the ledgers | INCLUDED | `## Core features` | companion 27 |
| Ticketing, parking, accounting interfaces | INCLUDED | `## Core features` | companion 28, recast as internal boundaries |
| Wayfinding, offline visitor map, written directions | INCLUDED | `## Core features` | companion 29 |
| Annual campus plan, recurring holds, scenarios | INCLUDED | `## Core features` | companion 30 |
| Consent, cookie declaration, page-view record | INCLUDED | `## Core features` | companion 5.3, plus the launch-surface draw |
| Build order and difficulty map (companion 37) | DROPPED | recorded in `_spec/00-decisions.md` | an ordering and calibration note, not a product requirement; every graded row it names is carried as a rule elsewhere |
| Evidence gaps (companion 40) | DROPPED | recorded in `_spec/00-decisions.md` | authoring provenance about the capture, not a product requirement |
| Nine venue job titles as nine roles | COLLAPSED | `## User roles` | six seeded roles preserve the permission shape; the nine functions are named as the console's desks |

## Slot obligations

| Slot | Provider | State | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | 32 pytest tests assert stored rows read back over the JSON API; `test_competing_confirmations_leave_exactly_one_stored_booking` is the `critical` substep for the slot and asserts the single-booking guarantee in the store |

## Grading surface

| Measure | Count |
|---|---|
| Workflows | 23 |
| Browser substeps | 31 |
| Pytest substeps | 73 |
| Critical substeps | 23 |
| Browser to pytest ratio | 0.42 (band 0.40 to 2.00) |
| Non-happy-path workflow ids | 10 |
| Pytest modules emitted | 1 (`tests/test_output.py`) |
| Sections covered by the module | core features, authorization, data integrity, edge cases, presentation |
| Checklist items | 779 across ten sections |
| Rubric criteria | 16, all positive |

Non-happy-path ids: `concurrent_confirmations_leave_one_booking`,
`phases_occupy_the_hall_and_a_tight_turnaround_raises_a_conflict`,
`invalid_stand_placement_is_refused_on_the_plan`,
`planner_cannot_approve_an_own_revision`, `expired_evidence_stops_its_badge`,
`exhibitor_cannot_read_another_stand`, `lower_role_is_denied_at_the_api`,
`unauthenticated_console_request_is_denied`, `audit_row_cannot_be_altered`,
`duplicate_option_rank_is_refused`.

## Rubric

| Dimension | Criteria | Positive share | Target |
|---|---|---|---|
| `instruction_following` | 4 | 0.30 | 0.30 |
| `functionality` | 2 | 0.25 | 0.25 |
| `ux_flow` | 2 | 0.15 | 0.15 |
| `ui_visual` | 2 | 0.15 | 0.15 |
| `motion` | 2 | 0.05 | 0.05 |
| `accessibility` | 2 | 0.05 | 0.05 |
| `responsiveness` | 2 | 0.05 | 0.05 |

No negative criterion is emitted: the brief licenses no commission the positives
do not already cover, and a negative mirroring a positive is a G29 failure.

`tests/rubric.json` is GENERATED by the vendored `recompute.py` from
`solution/trinity/grounding.yaml`. G48 re-runs the generator and compares bytes,
so a hand edit is a failure by construction.

## Literals ledger

56 pinned values, each carried by `instruction.md` and by at least one grader.

| Class | Count | Examples |
|---|---|---|
| `account` | 7 | `coordinator@example.com`, `operations@example.com`, `exhibitor@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `number` | 22 | hall areas `6090` to `7685`, licensed capacities `1620` to `5160`, combination capacity `7400` against the summed `8820`, `2500` parking spaces, `1450000` minor units |
| `seed` | 20 | `Hall 1` to `Hall 6`, `The Event Hall`, `The Concourse`, `The Transit`, `Palmarosa`, `Bookmark Fair`, `Ironwood Interiors`, `S-118` |
| `copy` | 6 | `when ideas need space`, `Open to the public`, `Trade fair - registration required`, `Search entire website`, `Skip to main content`, `(C) 2026 Verwick Xpo` |

## Spec folder

`Output/_spec/E_facil_book_exhibition-venue-operations-vb_20260916_071345/`, seven
documents.

| Document | Fed |
|---|---|
| `00-decisions.md` | the identity re-cast, the draws, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features` |
| `02-TRD.md` | `## Technical requirements`, `environment/` |
| `03-app-flow.md` | `## User flow`, `### API shapes` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model` |
| `06-implementation-plan.md` | downstream build ordering; not part of the brief |

## Grading window

Measured by `window_lint.py`. Length is reported, never failed.

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Core features | 36,344 | 2,400 | past-slice |
| User flow | 7,731 | 1,900 | past-slice |
| UI/UX notes | 6,857 | 1,700 | past-slice |
| Constraints | 1,388 | 800 | over-reference |
| User roles | 4,874 | 1,000 | past-slice |
| Overview | 2,494 | 700 | over-reference |
| Joined total | 59,688 | 8,800 | past-slice |

The brief carries the whole of a 1,714-line companion, as G51 requires, and
`## Front-end specification`, `## Technical requirements` and `## Data model` are
unbudgeted sections outside the judged join. The judged criteria are generated
and carry their own facts, so what sits past the slice reaches the agent in full
and is graded by pytest, by the browser substeps and by the criteria rather than
by the brief excerpt.

## Kit gate log

| Gate | Tool | Verdict | Exit |
|---|---|---|---|
| `G2/G16` | `validate_task.py` | PASS | 0 |
| `G1/G12` | `layout_lint.py` | PASS | 0 |
| `G46` | `structure_lint.py` | PASS | 0 |
| `G50` | `docker_lint.py` | PASS | 0 |
| `G55` | `runtime_deps_lint.py` | PASS | 0 |
| `G63` | `secret_lint.py` | PASS | 0 |
| `G48` | `truth_lint.py` | PASS | 0 |
| `G51` | `source_lint.py` | PASS | 0 |
| `G52` | `rubric_context_lint.py` | PASS | 0 |
| `G54` | `comment_lint.py` | PASS | 0 |
| `G17` | `secret_hygiene_lint.py` | PASS | 0 |
| `G11` | `leak_scan.py` | PASS | 0 |
| `G33` | `window_lint.py` | PASS | 0 |
| `G4/G5` | `contract_lint.py` | PASS | 0 |
| `G43` | `prescription_lint.py` | PASS | 0 |
| `G44` | `disclosure_lint.py` | PASS | 0 |
| `G10` | `no_sdk_lint.py` | PASS | 0 |
| `G31` | `determinism_lint.py` | PASS | 0 |
| `G14` | `reward_path_lint.py` | PASS | 0 |
| `G27/G30` | `rubric_lint.py` | PASS | 0 |
| `G41` | `flag_lint.py` | PASS | 0 |
| `G56/G57/G58` | `if_lint.py` | PASS | 0 |
| `G59/G60` | `codequality_lint.py` | NOT-APPLICABLE | 2 |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | PASS | 0 |
| `G6` | `fixture_lint.py` | PASS | 0 |
| `G24` | `coverage_map.py` | PASS | 0 |
| `G37` | `checklist_qc.py` | PASS | 0 |
| `G39` | `rubric_align_lint.py` | PASS | 0 |
| `G28/G29` | `channel_lint.py` | PASS | 0 |
| `G40` | `prompt_receipt_lint.py` | WARN | 0 |
| `G0/INV5` | `vendor_check.py` | PASS | 0 |
| `G47` | `output_qc.py` | PASS | 0 |
| `G38` | `kit_selftest.py` | PASS (32 checks) | 0 |
| `G3` | `task_code.py decode` + `task_code_verifier.md` | VALID | 0 |
| `G42` | `corpus_overlap.py` | NOT-APPLICABLE | 0 |
| `G49` | `diversity_lint.py` | PASS (WARN mode) | 0 |
| `G61` | `corpus_report.py` | NOT-APPLICABLE | 0 |

`G40` is WARN because all seven certification prompts were run by the same agent
that authored the artifacts: every receipt reads `verifier: self`. The kit's rule
is owner is not verifier, so these are recorded verdicts, never independent ones.

## Prompt receipts

From `_handoff/E_facil_book_exhibition-venue-operations-vb_20260916_071345.receipts.json`.

| Prompt | Gate | Verdict | Checks | Non-pass |
|---|---|---|---|---|
| `task_code_verifier.md` | `G3` | VALID | 12 | none |
| `QC_spec.md` | `G34` | PASS | 15 | `S2` WARN |
| `QC_instruction.md` | `G34` | PASS | 24 | `C1`, `C5`, `C7` WARN |
| `qc_solution_checklist.md` | `G37` | PASS | 0 | none |
| `qc_rubric.md` | `G53` | PASS | 16 | `RC-10` NOT-APPLICABLE |
| `qc_toml.md` | `G36` | PASS | 120 | `VERIF-001` WARN; 4 SKIP; 6 NOT-APPLICABLE |
| `qc_docker.md` | `G35` | PASS | 105 | `CMP-011`, `CMP-020` WARN; 4 NOT-APPLICABLE |

## Blocking findings

None that prevent a required check. Three recorded contradictions between a QC
prompt and a newer kit decision, each carried as a WARN with its reasoning in the
receipts:

1. `QC_toml VERIF-001` asks for `environment_mode = "separate"`; OPEN-DECISIONS
   D2 and `stage-4-task-toml.md` mandate `"shared"`, and G17 enforces the shared
   credential split. Shared is emitted.
2. `qc_docker CMP-011` and `CMP-020` forbid a `ports:` key and extra keys on
   `main`; `CMP-022` and reference/C C12 require both. C12 is the newer rule and
   is honoured.
3. `QC_instruction C7` treats a section past its reference length as a defect;
   G33 retired length failures because the judged criteria are generated and
   self-contained. Length is reported in the table above.

One authoring waiver, recorded rather than silent: `G51 --waive
"color-background"`.

## Versions

| Item | Value |
|---|---|
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Harbor version | `0.20.0` |
| Rubric version | `1` |
| Judge pin | `claude-sonnet-4-6` |
| Canary | present in `solution/TRUTH.md` and `solution/USER_README.md`, one GUID for the corpus |

## Budget

`turns_expected = 200`, `tokens_expected = 7000000`. Reasoning: the brief carries
a 29-route trilingual public site plus a thirteen-desk operations console, an
interactive floor plan generated from the space model, and nine expert-tier
invariants that have to hold in the store rather than in application code. The
graded surface is 779 checklist items against 73 pytest tests, 31 browser
substeps and 16 judged criteria. That is the top of the band, and the calibration
fields stay empty for the Calibration Engineer to write.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing here counts toward corpus targets until the reference app
is built downstream from `solution/checklist.md` and `harbor run -a oracle`
returns `1.0` twice.
