# Build report - I_learn_cont_segmented-survey-report-vb_20260916_111650

## Identity

| Field | Value |
|---|---|
| Task code | `I_learn_cont_segmented-survey-report-vb_20260916_111650` |
| Task id | `deku/segmented-survey-report-vb` |
| Cell | individual / learning-study / content-publishing |
| Service profile | `P4-db-storage`: slot `backend` -> `postgres`, slot `storage` -> `minio` |
| Verifier mode | `separate`: the grader ships its own image from `tests/Dockerfile` on `deku-verifier-base` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `javascript` |
| Stack draw | `mpa-progressive` / `Express + Nunjucks` / `HTMX + server templates`, over `[metadata].archetype` |
| Design direction | `companion` (the `clinical-precision` draw does not govern; reference/L SS L.6.1) |
| Launch surface | `colour_contrast, custom_404, no_broken_links, spam_protection, terms_page` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit revision | `806eb0a` |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Authors | `utsav.jain@ethara.ai` (QL), `mohd.rafey@ethara.ai` (contributor) |

## Task Order, as received and as minted

| Field | Supplied | Minted | Why |
|---|---|---|---|
| category | `individual` | `individual` | legal as given |
| domain | `learning-study` | `learning-study` | legal as given |
| pattern | `content-publishing` | `content-publishing` | legal as given |
| archetype | `segmented-survey-report` | unchanged, `-vb` suffix | three tokens, kebab-case, unclaimed |
| profile | none | `P4-db-storage` | the only legal profile for the content-publishing pattern |
| companion | `Drive_PRDs/16_sept/stateofaidesign_prd.md` | variant `b` | stage-1: a companion forces variant b on `critical_depth` and `spec_sections` |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| One dataset of results by wave, question, option and profile cell | INCLUDED | ## Core features, ## Data model | the companion's SS 6 grain, stored by the service the pattern requires |
| Typed arithmetic, single rounding, movement states, suppression, intervals, supported differences | INCLUDED | ## Core features | companion SS 6 and SS 13.8 |
| Three chapters in six chart forms with regenerated headings, text equivalents, rail, takeaways | INCLUDED | ## Core features, ## Front-end specification | companion SS 7 and SS 10 |
| Segments that compose, live in the address and recompute in place | INCLUDED | ## Core features | the idea's filter, companion SS 13 |
| Comparison of two segments | INCLUDED | ## Core features | the idea's comparison, companion SS 13.4 |
| Markdown export and citation | INCLUDED | ## Core features | the idea's export, companion SS 14 |
| A private library of saved exports in object storage | INCLUDED | ## Core features, ## Technical requirements | the pattern's storage slot and critical focus |
| Reading position and stored segment for signed-in readers | INCLUDED | ## Core features | the idea's keeping one's place, companion SS 15 |
| Case-study set with announced members, about and methodology | INCLUDED | ## Core features | companion SS 8, SS 11, SS 12 |
| Terms page, not-found page, working links, contrast bar, bot refusal | INCLUDED | ## Core features, ## UI/UX notes | the launch-surface draw |
| The reference's findings, quotations, partners, logos and credits | DROPPED | ## Constraints | companion SS 21.4 refusals |
| Case-study films with captions and transcripts | DROPPED | 00-decisions.md | no film ships, so the obligation has nothing to attach to |
| Offline reading and a device-held store | DROPPED | companion SS 15.1, SS 15.5, waived | the dataset lives with the service |
| Acceptance checklist and evidence gaps | DROPPED | companion SS 21, SS 23, waived | provenance notes and grading meta, INV10 |

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_every_stored_result_row_matches_the_seed_generation_rule` (critical), `test_a_reading_position_survives_a_reload_and_a_new_session` (critical) and further tests reading rows through the shared backend adapter |
| `storage` | `minio` | MET | `test_a_saved_export_is_stored_as_an_object_whose_bytes_match_the_export_download` (critical), `test_removing_a_saved_export_deletes_its_row_and_its_object` and the anonymous-read refusal, through the shared storage adapter |

No slot is UNMET.

## Grading surface

| Measure | Value |
|---|---|
| Workflows | 11 (individual band 6 to 11) |
| Browser substeps | 37 |
| Pytest substeps | 76 |
| Browser to pytest substep ratio | 0.49 (G45 band 0.40 to 2.00) |
| Critical substeps | 9 |
| Non-happy-path workflow ids | 3: `visitor_filters_the_report_and_an_invalid_segment_link_falls_back_to_everyone`, `a_reader_cannot_read_another_readers_saved_export`, `accounts_terms_and_bot_submissions_are_rejected_and_unknown_paths_answer_404` |
| Pytest module | one, `tests/test_output.py`, 76 tests |
| Sections covered | core features, data integrity, authorization, edge cases, storage |
| Checklist items | 176 |
| Judged criteria | 13 |

Rubric split: 13 positive, 0 negative. Positive point total 45.

| Dimension | Share | Target | Delta |
|---|---|---|---|
| `instruction_following` | 0.222 | 0.30 | -0.078 |
| `functionality` | 0.289 | 0.25 | +0.039 |
| `ux_flow` | 0.178 | 0.15 | +0.028 |
| `ui_visual` | 0.244 | 0.15 | +0.094 |
| `motion` | 0.022 | 0.05 | -0.028 |
| `accessibility` | 0.022 | 0.05 | -0.028 |
| `responsiveness` | 0.022 | 0.05 | -0.028 |

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Overview | 1987 | 700 | over-reference |
| User roles | 1479 | 1000 | over-reference |
| Core features | 25465 | 2400 | past-slice |
| User flow | 5492 | 1900 | past-slice |
| UI/UX notes | 4238 | 1700 | past-slice |
| Constraints | 902 | 800 | over-reference |
| joined total | 39563 | 8800 | past-slice |

Length is reported, never failed. The dataset rules every grader rests on open `## Core features`,
so the part of that section the advisory judge reads is the part the task turns on.

## Literals ledger

| Class | Count | Values |
|---|---|---|
| `account` | 2 | `reader@example.com`, `reader2@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `endpoint` | 18 | `/api/health`, `/api/report`, `/api/segments`, `/api/export.md`, `/api/auth/sign-up`, `/api/auth/sign-in`, `/api/auth/sign-out`, `/api/auth/me`, `/api/progress`, `/api/preferences`, `/api/exports`, `/api/subscriptions`, `/api/chapters/{slug}`, `/api/cases/{slug}`, `/api/exports/{id}/download`, `/api/exports/{id}`, `/api/progress/{chapter}`, `/api/chapters/{slug}/findings/{id}/citation` |
| `env_var` | 10 | `DATABASE_URL`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`, `DB_ADMIN_URL`, `DEKU_SERVICE_BACKEND`, `DEKU_SERVICE_STORAGE` |
| `number` | 8 | `869`, `709`, `30`, `1.96`, `200`, `4.5:1`, `16px`, `13px` |
| `route` | 11 | `/chapters/tools`, `/chapters/craft`, `/chapters/teams`, `/about`, `/terms`, `/sign-in`, `/sign-up`, `/library`, `/library/new`, `/library/new/compare`, `/library/new/review` |
| `scheme` | 14 | `exports/{account_id}/{export_id}.md`, `segment=all`, `vs_size`, `vs_env`, `vs_exp`, `website`, `result`, `cell`, `progress`, `preference`, `export`, `subscription`, `tied_with_next`, `margin_points` |
| `seed_record` | 61 | `Studio Signals`, `Northbeam Research`, `Aster & Vale`, `Ines Park`, `Tomas Reyes`, `Harbour Type Co.`, `Kestrel Health`, `Fieldwork Studio`, `TYPE FOUNDRY`, `HEALTHCARE`, `AGENCY`, `harbour-type`, `kestrel-health`, `fieldwork-studio`, `lumen-transit`, `oakline-bank`, `parcel-and-post`, `quarry-games`, `Startups (1 to 50)`, `Growth (51 to 500)`, `Scale-up (501 to 2K)`, `Enterprise (2,000+)`, `In-house`, `Agency`, `Freelance`, `Under 10 years`, `10 years or more`, `usage-frequency`, `stack-tools`, `tool-count`, `confidence`, `stick-reasons`, `craft-shift`, `team-policy`, `hiring-outlook`, `stack-ranked`, `stack-movement`, `confidence-by-size`, `46% use AI tools every day, up 16 points since 2025.`, `Designers use 5.8 AI tools in a typical week.`, `Showing Startups (1 to 50). 223 of 869 respondents.`, `Showing all respondents.`, `Too few respondents in this group to report. 20 answered.`, `That link asks for a group this report doesn't have. Showing everyone.`, `Directional, not a benchmark. See methodology.`, `Figures carry a 95% confidence interval.`, `47%, give or take 7. Based on 195 answers.`, `Too close to call for these two groups.`, `A real difference between these two groups.`, `No change since 2025.`, `No detectable change since 2025.`, `Not asked in 2025`, `Asked differently in 2025, so the two are not compared.`, `Too few 2025 answers to compare.`, `These two are too close to separate.`, `That email and password do not match`, `Page not found`, `Back to the report`, `About this report`, `Coming soon`, `studio-signals-2026.md` |
| `status` | 21 | `rise`, `fall`, `no-change`, `not-detectable`, `not-asked`, `not-comparable`, `suppressed`, `not-started`, `part-way`, `finished`, `closers`, `reader`, `single`, `multi`, `numeric`, `part-to-whole`, `ranked-bars`, `ordered-ranking`, `movement-list`, `two-wave`, `segment-breakdown` |

146 entries. 3 are `verifier_only` and live in `[verifier].env` alone: `DB_ADMIN_URL`, `DEKU_SERVICE_BACKEND`, `DEKU_SERVICE_STORAGE`. Every other entry has `instruction.md` as a carrier, and G6
holds the bijection in both directions.

## Authoring documents

| Doc | Fed |
|---|---|
| `_spec/I_learn_cont_segmented-survey-report-vb_20260916_111650/00-decisions.md` | the draws, the taxonomy, where the Task Order, the pattern and the companion disagree, the judgment calls, the identity recast, the certification repairs and the companion carry table |
| `_spec/I_learn_cont_segmented-survey-report-vb_20260916_111650/01-PRD.md` | ## Overview, ## Core features, ## Constraints |
| `_spec/I_learn_cont_segmented-survey-report-vb_20260916_111650/02-TRD.md` | ## Technical requirements |
| `_spec/I_learn_cont_segmented-survey-report-vb_20260916_111650/03-app-flow.md` | ## User flow, ## Deployment contract API shapes |
| `_spec/I_learn_cont_segmented-survey-report-vb_20260916_111650/04-uiux-brief.md` | ## UI/UX notes, ## Front-end specification |
| `_spec/I_learn_cont_segmented-survey-report-vb_20260916_111650/05-backend-schema.md` | ## Data model, ## User roles |
| `_spec/I_learn_cont_segmented-survey-report-vb_20260916_111650/06-implementation-plan.md` | not emitted: `## Build plan` is not baseline |

## Certification reviews

Rendered from `_handoff/I_learn_cont_segmented-survey-report-vb_20260916_111650.receipts.json`.

| Prompt | Gate | Verdict | Checks | Warn | N/A | Verifier |
|---|---|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | 4 | 0 | self |
| `QC_spec.md` | G34 | PASS | 15 | 4 | 0 | self |
| `qc_docker.md` | G35 | PASS | 105 | 1 | 3 | self |
| `qc_rubric.md` | G53 | PASS | 16 | 0 | 1 | self |
| `qc_solution_checklist.md` | G37 | CHANGES REQUIRED | 0 | 0 | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | 0 | 7 | self |
| `task_code_verifier.md` | G3 | VALID | 12 | 0 | 0 | self |

### QC_instruction.md

- Cycle 1, B2: the pattern's critical focus, a stored object that is not publicly readable, was prose in `### The library`. It is now four numbered rules, each with its negative case: another reader's download and removal answer `404` with the record and object unchanged, a request with no session answers `401`, and the bucket refuses an anonymous read.
- Cycle 1, A7: the seeded password appeared only in `## User roles`; `## Data model`'s seed now restates it with the `/app/USER_README.md` instruction.
- Cycle 1, C2: rule 6 set the interval-in-words threshold at `100` while its example used a base of `195`; the threshold is now `200`, matching both the example and the graders.
- Cycle 1, C2: the export's `2025` cell had no text for a `not-comparable` or `suppressed` movement; it now reads `Not compared`. `previous` is pinned on `movement-list` rows as well as `two-wave` rows, and a breakdown row's `option` is pinned as the band slug.
- Cycle 1, D2: the comparison sentence's shares were unnamed for ranked and breakdown forms; they are now the focus option's shares, and a numeric finding or one with no focus carries none.
- Cycle 1, D2: whether a chapter link carries the segment was implied by the address rule but unstated; the sidebar's chapter links, the rail and the previous and next controls now carry it.
- Cycle 1, D5: captions were set on the reading leading, which inverts the companion's SS 4.2 (the 1.2 ratio belongs in a caption). Captions now run `13px` on `15.6px`.
- A3: the thirteen canonical contract lines are present unaltered.
- A8: the agent variables are DATABASE_URL, APP_PUBLIC_URL, APP_PUBLIC_PORT, STORAGE_ENDPOINT, STORAGE_BUCKET, STORAGE_ACCESS_KEY and STORAGE_SECRET_KEY.
- B1: individual collapses the content-publishing row's author and reader to one `reader` role; PostgreSQL and MinIO are the declared providers.
- B4: two seeded readers with empty libraries give the two tenants the isolation boundary needs; the segment `?size=growth&env=freelance` (20 respondents) and `?size=startup&env=freelance&exp=10-plus` (2025 base 26) carry the suppression boundaries.
- C5: every figure is derived at request time from `result` rows; seeding is stated idempotent.
- C6: Express, Nunjucks, HTMX, `pg`, `@aws-sdk/client-s3` and the font packages appear only in `## Technical requirements`; the typeface names in `## UI/UX notes` are the A5 type rule.
- D1: the lazy build (typed headings, a separate export template, exports on disk, a hidden card) is refused by the numbered rules and the No mocks block.
- D3 and D4: no sentence names a verifier, grader, harness or checker.
- D5: reduced motion, the heading-survival rule, position by finding, the export needing no address, the rail becoming a control at a narrow width and the derived footer year all agree with their companion lines.
- A1: `## Build plan` is absent and `## Front-end specification` stands in its place. generate_instruction.md SS 2.1 states a Build plan is not baseline; A1 still lists it. The companion's visual specification needs the Front-end section, which SS 1 rule 2 names as its legal home.
- B3: Two of the three levers are emitted; `## Build plan` is the third and SS 2.1 forbids it at baseline. Same kit contradiction as A1.
- C4: `## UI/UX notes` carries exact type families and pixel sizes. C4 treats pinned type as a value sheet; generate_instruction.md SS 4, the A5 number rule, requires the exact family and size, and G51 measures it. Colour is family, tone and shade words; motion and breakpoints are words; no hex, millisecond or cubic-bezier appears.
- C7: `## Core features` (about 25,000 characters) runs past the judge's 2,500-character slice. G33 retired length as a failure. The dataset rules open the section, so the part the judge reads is the arithmetic every grader rests on.

### QC_spec.md

- Cycle 1, S2: `01-PRD.md` listed seven must-have features against a band of three to six; comparison is folded into segments and citation into the export, leaving six.
- Cycle 1, G2: `05-backend-schema.md` now states that unchosen segment columns on `export` are null, as the brief does.
- B1: the content-publishing row is db plus storage with PostgreSQL and MinIO; the individual modifier leaves one role, `reader`.
- B2: two seeded readers for export isolation, and seed cells whose intersections fall below the threshold.
- G1: `reader@example.com` and `reader2@example.com` with `deku-demo-pw-2026` appear in both spec and brief.
- G2: every endpoint in the brief's API table appears in `03-app-flow.md`, and the tables and columns in `05-backend-schema.md` match the brief's entities.
- G3: every entry under `Where the Task Order, the pattern and the companion disagree`, `Judgment calls`, `Identity recast` and `Consistency repairs made during certification` is reflected in the brief.
- S10: no placeholder and no canary text; seeded emails follow `<role>@example.com`.
- S1: Six documents are present; `06-implementation-plan.md` is not. It maps to `## Build plan`, which generate_instruction.md SS 2.1 forbids at baseline. Same kit contradiction as QC_instruction A1.
- S5: `04-uiux-brief.md` carries colour as family, tone and shade words and motion as words rather than hex and millisecond values. generate_instruction.md SS 4, the A5 number rule, bans those values; reference/L SS L.6.1 hands the design axes to the companion.
- S7: No implementation plan exists to shape, for the reason given under S1.
- S8: `00-decisions.md` opens with a `draw:` block. S8 calls restated derivation facts noise; generate_instruction.md SS 2.9 and SS 2.10 require these lines and G49 reads them.

### qc_docker.md

- RUN-001 and BC-004: the TRD declares Node.js 22 with Express; the image installs Node 22 from the NodeSource registry over the digest-pinned python:3.12-slim-bookworm base, and the app's own packages install from npm at build time.
- CMP-004: `main` waits for `minio-init` to report healthy, and that healthcheck stats the `deku` bucket, so seeding never races the bucket's creation.
- HAL-001: the MinIO image is pulled from quay.io/minio/minio by digest, the upstream project's own registry, because Docker Hub answered 401 to the digest lookup.
- CMP-018: PostgreSQL and MinIO state sit on the named volumes `postgres-data` and `minio-data`; the only bind mount is the read-only bundle-relative init SQL.
- SEC-001: the MinIO root credential in compose equals the STORAGE_SECRET_KEY default the app needs to write objects; the bucket's anonymous policy is set to none.
- SEC-003: the image runs as root, as every reference environment under tasks/ does.
- DEP-015: no `--break-system-packages` and no pip fallback appear.
- DEP-016, DEP-017 and BP-008 concern compiled languages and musl bases; the language is JavaScript on a glibc base.
- CMP-011: `main` publishes `4173:4173`. CMP-022 and stage-5 C12 require `main` to set `ports` and `extra_hosts`, because a missing host-gateway mapping loses every trial; CMP-022 governs. `postgres`, `minio` and `minio-init` publish nothing.

### qc_rubric.md

- Cycle 1, RC-12: R13 asked whether labels sit above their bars, which two bounding boxes decide; it now judges whether a narrow chart stays readable with every label matched to its bar.
- Cycle 1, R-3 and R-4: R2 and R3 carried the pronoun `it` and R6 the word `without`; each criterion now names its surface.
- RC-04: no criterion restates a pytest or browser observation. The cover title's existence is a browser item and its legibility over the moving ground is R2; the withdrawal copy is a browser item and its composed layout is R10.
- RC-05 and RC-07: every criterion names a surface from the route table or headings, and every rule opens by saying what that surface is.
- RC-01: every judgment-class checklist item is claimed by a criterion or cited by a browser substep, never both; 13 items are claimed by criteria.
- RC-13: positive shares are instruction_following 0.222, functionality 0.289, ux_flow 0.178, ui_visual 0.244, motion 0.022, accessibility 0.022, responsiveness 0.022; 10 of 13 criteria are task completion.
- RC-10: no negative criterion is emitted, because the brief licenses none.
- RC-14: tests/rubric.json was produced by recompute.py from grounding.yaml.
- RC-15: converged on cycle 2 of a permitted three.

### qc_solution_checklist.md

- NEEDS REVIEW. The machine layer reports no structural failure, no uncovered obligation and no ledger shortfall. Two values are declared under `Referenced but not pinned`: the export id inside the key scheme, and the word count behind a chapter's reading time. Neither is asserted as a literal: an id is the service's to choose, and the reading time rests on prose the builder writes, so graders check its format and its agreement with the API. SS 5 grades an unpinned value that does not block as NEEDS REVIEW.
- Each of the 176 items was written beside its observer, a browser step, a pytest function or a judged criterion, and the builder refused any citation sharing fewer than two content words with its observer; 46 such problems in the first pass were reworded or moved before emission. Every section carries at least as many items as obligation-bearing sentences.
- Two export-table header items contain a pipe and are tagged `contract` rather than `literal`, because a pipe cannot sit in the pinned-literals table.

### qc_toml.md

- META-009: keywords read greenfield, individual, javascript, postgres, minio, survey, report.
- TAX-005: `language = "javascript"` matches the TRD's Node.js with Express.
- SVC-004 and VERIF-006: `backend = postgres` then `storage = minio`, with markers DEKU_SERVICE_BACKEND and DEKU_SERVICE_STORAGE.
- VERIF-007: the four STORAGE_ variables are in `[verifier].env` with the defaults `[environment].env` uses.
- SEC-001: DB_ADMIN_URL sits in `[verifier].env` only.
- INST-001: the storage slot is exercised by the saved-export library; no email, payments or search journey exists and none is provisioned.
- META-010: uuid_v5 was minted by `task_code.py uuid5` for this task code.
- BENCH-001: the Standard tier values are exact.
- SIGN-001 to SIGN-003 are retired rows; TAX-006, BENCH-002 and INST-007 govern trivial tasks and an absent brief; TAX-008 is informational and the mint ledger holds uniqueness.

### task_code_verifier.md

- The code reads I, learn, cont, segmented-survey-report, vb, 20260916_111650: individual, learning-study, content-publishing, the archetype, variant b and a well-formed stamp.
- PROFILES for the individual content-publishing cell: P4-db-storage alone. task.toml declares P4-db-storage.
- Every Task Order value is legal as given; no substitution was needed.
- Global archetype uniqueness is not checkable from one code; the mint ledger enforces it.

## Kit gate log

Rendered from `_handoff/I_learn_cont_segmented-survey-report-vb_20260916_111650.gates.jsonl`. Never transcribed.

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

## Handoff gate list

Undecided here. See `_handoff/I_learn_cont_segmented-survey-report-vb_20260916_111650.handoff.md` for commands and expected verdicts:
G13, G15, G18, G19, G20, G21, G25.

## Blocking findings

None blocks a test. Two values are referenced but not pinned, the export id inside the key scheme
and the word count behind a chapter's reading time; no grader asserts either as a literal.
`qc_solution_checklist` records that as NEEDS REVIEW.

## Effort estimate

`turns_expected = 200`, `tokens_expected = 8000000`. The build is an Express application with
server-rendered Nunjucks pages and HTMX swaps, a query layer that aggregates stored result rows
with typed arithmetic, movement states, suppression, intervals and a supported-difference test,
regenerated headings, six chart forms, a markdown export and citation from the same resolution, a
reading position and stored segment per reader, and a private library of exports in MinIO.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`
