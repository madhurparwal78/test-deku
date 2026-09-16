# Build report - S_saasm_cont_app-builder-marketing_20260916_060744

Rendered from `_handoff/S_saasm_cont_app-builder-marketing_20260916_060744.gates.jsonl`. Every verdict below is the receipt's
own exit code and verdict string; nothing here is transcribed by hand (ISSUES C-02).

## Identity

| Field | Value |
|---|---|
| Task code | `S_saasm_cont_app-builder-marketing_20260916_060744` |
| Task id | `deku/app-builder-marketing` |
| Cell | solo_founder / saas-micro-tools / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | `backend` = `postgres`, `storage` = `minio` |
| Variant | `a`, axes `[]` |
| Language | `typescript` |
| Design direction | `terminal-mono` (sha256 over `[metadata].archetype`) |
| Capability flags | `(none)` |
| spec_sections_given | `overview`, `roles`, `features`, `flow`, `uiux`, `frontend`, `techrequirements`, `datamodel`, `constraints`, `contract` |
| Launch surface | `alt_text`, `page_view_log`, `privacy_page`, `sitemap_robots`, `terms_page` (drawn) |
| Shard | 1 of 1 (single-task run) |

## Derived-design draws

Recorded in `_spec/S_saasm_cont_app-builder-marketing_20260916_060744/00-decisions.md`, which `tools/diversity_lint.py` (G49) parses.

| Axis | Value |
|---|---|
| `render_model` | spa-json-api |
| `backend` | NestJS |
| `frontend` | Svelte + Vite |
| `design_direction` | terminal-mono |
| `nav` | sidebar-nav |
| `work_surface` | card-grid |
| `create_flow` | slide-over |
| `feedback` | optimistic-row |

## Feature resolution

| Candidate | Verdict | Where it landed | Reason |
|---|---|---|---|
| Seven public routes and the shared not-found surface | INCLUDED | `## User flow`, `## Front-end specification` | PRD Sections 2, 10-17 |
| Persistent prompt composer and the build request | INCLUDED | `## Core features` 8-9, `## Technical requirements` | PRD Sections 5.3, 32.3 |
| Presigned attachment grant, content-sniffed | INCLUDED | `## Core features` 9, `## Technical requirements` | PRD Section 32.3 |
| Four collections with a draft boundary | INCLUDED | `## Core features` 1-5 | PRD Sections 32.5-32.8, pattern critical focus |
| Cover objects in MinIO with an authenticated read | INCLUDED | `## Core features` 6-7 | pattern critical focus, reference S2.7 |
| Double opt-in subscription with no membership leak | INCLUDED | `## Core features` 10 | PRD Section 32.4 |
| Machine-readable question set and docs index | INCLUDED | `## Technical requirements` | PRD Sections 12.6, 32.8 |
| Server-driven press pagination | INCLUDED | `## Technical requirements` | PRD Section 15.3 |
| Two independently tokenised design systems | INCLUDED | `## Technical requirements`, `## Front-end specification` | PRD Section 3.1 |
| Platform runtime: sync engine, computed columns, workflow engine, intelligence layer, metering | DROPPED | `## Constraints` | PRD Section 0.3 stops the site build at Section 21 plus Section 32; Sections 22-31 and 33 are designed rather than measured and no channel here can observe them. Declared on the G51 receipt as 37 waived topics. |
| Email delivery for the subscription confirmation | DROPPED | `## Constraints` | no `email` slot is legal for profile `P4-db-storage`; the subscription records a pending confirmation and stops |
| Payments and any price surface | DROPPED | `## Constraints` | no `payments` slot in this profile |

## Slot obligations

| Slot | Provider | Status | Evidence |
|---|---|---|---|
| `backend` (db) | `postgres` | MET | `test_seeded_accounts_are_persisted_rows`, `test_article_slug_is_unique`, `test_published_at_is_set_only_on_published_articles` assert real rows through `capabilities.Backend` |
| `storage` | `minio` | MET | `test_article_cover_upload_is_stored_in_the_object_store` asserts the object exists in the bucket at its scheme's key through `capabilities.ObjectStore` |

`tools/workflow_lint.py` (G32) decided both, and each slot carries a `critical` pytest substep.

## Grading layer

| Measure | Value |
|---|---|
| Workflows | 15 (band [10, 16]) |
| Browser substeps | 23 |
| pytest substeps | 36 |
| `critical` substeps | 33 |
| Non-happy-path ids | `draft_article_denied_to_every_reader_but_its_author`, `reader_cannot_reach_the_studio`, `cross_author_edit_is_denied_and_the_row_is_unchanged`, `concurrent_feature_requests_leave_one_featured_row`, `every_surface_carries_its_empty_and_loading_states` |
| pytest module | `tests/test_output.py`, 36 tests |
| Sections covered | core features, storage, authorization, data integrity |
| Checklist items | 130, all cited (G24 two-way) |

Coverage citations live in `_handoff/S_saasm_cont_app-builder-marketing_20260916_060744.pytest-provenance.json` rather than in
test docstrings: G54 forbids a comment in a shipped bundle, and `coverage_map.py`
accepts the sidecar for exactly that reason.

## Rubric

13 judged criteria: 11 positive, 2 negative. Generated from
`solution/trinity/grounding.yaml` through the vendored `recompute.py`; `rubric_version` is
`1`.

| Dimension | Criteria | Points | Share | Target |
|---|---|---|---|---|
| `instruction_following` | 2 | 8 | 0.320 | 0.30 |
| `functionality` | 2 | 6 | 0.240 | 0.25 |
| `ux_flow` | 2 | 4 | 0.160 | 0.15 |
| `ui_visual` | 2 | 4 | 0.160 | 0.15 |
| `motion` | 1 | 1 | 0.040 | 0.05 |
| `accessibility` | 1 | 1 | 0.040 | 0.05 |
| `responsiveness` | 1 | 1 | 0.040 | 0.05 |

Task-completion share 9/13 = 69% (band 60-80%).

## Grading window

```
core_features  Core features      2195       2400  ok
user_flow      User flow          2026       1900  over-reference
ui_ux_notes    UI/UX notes        2403       1700  over-reference
constraints    Constraints         736        800  ok
user_roles     User roles          994       1000  ok
overview       Overview            733        700  over-reference
joined total                      9087       8800  past-slice
first four                        7360       7100  over-reference
```

Every section sits inside the 2,500-char `run_rubric.py` slice and the join inside the
9,000-char cap, so no graded rule is truncated. The joined total sits a little over the
kit's 8,800 advisory target; recorded on the QC receipt as `QC_instruction.md` C7 WARN
rather than resolved by deleting graded content.

## Literals ledger

52 entries. Full file: `_handoff/S_saasm_cont_app-builder-marketing_20260916_060744.literals-ledger.json`.

| Class | Count | Values |
|---|---|---|
| `account` | 4 | `author@example.com`, `author2@example.com`, `reader@example.com`, `subscriber@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `endpoint` | 13 | `/api/health`, `/api/articles`, `/api/covers/`, `/api/press`, `/api/jobs`, `/api/questions`, `/api/site/attachments`, `/api/site/build-requests` ... |
| `env_var` | 8 | `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `DB_ADMIN_URL` |
| `number` | 4 | `4173`, `300`, `26214400`, `4000` |
| `route` | 9 | `/blog`, `/news`, `/jobs`, `/faqs`, `/docs`, `/byoa`, `/studio`, `/login` ... |
| `scheme` | 2 | `covers/{article_slug}/{sha256_of_bytes}.{ext}`, `build-requests/{request_id}/{sha256_of_bytes}.{ext}` |
| `seed_record` | 5 | `agents-reading-your-schema`, `spreadsheet-to-app-in-an-afternoon`, `what-your-warehouse-sheet-already-knows`, `field-marketing-lead`, `staff-frontend-engineer` |
| `status` | 6 | `draft`, `published`, `inline`, `pinned`, `author`, `reader` |

One entry is `verifier_only`: `DB_ADMIN_URL`, carried by `task.toml` `[verifier].env`
alone (INV4).

## Authoring documents

`_spec/S_saasm_cont_app-builder-marketing_20260916_060744/`, outside the bundle (CON-5, `spec` is a forbidden directory inside one).

| Document | Fed |
|---|---|
| `00-decisions.md` | the draws, and D1-D7 |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing: `## Build plan` is not a baseline section |

## Kit gate log

Verbatim from the receipts. `exit` is the tool's own exit code; `inputs` is the number of
bundle files whose SHA-256 the receipt records.

| Gate | Tool | Exit | Verdict | Inputs hashed |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | 24 |
| `G1/G12` | `layout_lint.py` | 0 | PASS | 24 |
| `G46` | `structure_lint.py` | 1 | FAIL | 24 |
| `G50` | `docker_lint.py` | 0 | PASS | 24 |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | 24 |
| `G63` | `secret_lint.py` | 0 | PASS | 24 |
| `G48` | `truth_lint.py` | 0 | PASS | 24 |
| `G51` | `source_lint.py` | 0 | PASS | 24 |
| `G52` | `rubric_context_lint.py` | 0 | PASS | 24 |
| `G54` | `comment_lint.py` | 0 | PASS | 24 |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | 24 |
| `G11` | `leak_scan.py` | 0 | PASS | 24 |
| `G33` | `window_lint.py` | 0 | PASS | 24 |
| `G4/G5` | `contract_lint.py` | 0 | PASS | 24 |
| `G43` | `prescription_lint.py` | 0 | PASS | 24 |
| `G44` | `disclosure_lint.py` | 0 | PASS | 24 |
| `G10` | `no_sdk_lint.py` | 0 | PASS | 24 |
| `G31` | `determinism_lint.py` | 0 | PASS | 24 |
| `G14` | `reward_path_lint.py` | 0 | PASS | 24 |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | 24 |
| `G41` | `flag_lint.py` | 0 | PASS | 24 |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | 24 |
| `G59/G60` | `codequality_lint.py` | 2 | ? | 24 |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | 24 |
| `G6` | `fixture_lint.py` | 0 | PASS | 24 |
| `G24` | `coverage_map.py` | 0 | PASS | 24 |
| `G37` | `checklist_qc.py` | 0 | PASS | 24 |
| `G39` | `rubric_align_lint.py` | 0 | PASS | 24 |
| `G28/G29` | `channel_lint.py` | 0 | PASS | 24 |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | 24 |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | 24 |
| `G47` | `output_qc.py` | 1 | FAIL | 24 |

Exit `2` is NOT-APPLICABLE: G56/G57 and G59/G60 report it because this bundle carries
neither `tests/if_constraints.json` nor `tests/code_rubric.json`.

### Corpus-level gates

| Gate | Tool | Verdict |
|---|---|---|
| G42 | `corpus_overlap.py` | NOT-APPLICABLE: needs at least 2 bundles, got 1. Not a pass; no comparison ran |
| G49 | `diversity_lint.py` | NOT-APPLICABLE: needs at least 2 bundles, got 1 |
| G61 / G26 | `corpus_report.py` | ADVISORY FAIL: payments-or-email share 0% against a 28% floor, which is arithmetic over a one-bundle corpus. No bundle carries a difficulty yet, so the 0/10/30/40/20 mix cannot be read until calibration runs |
| G38 | `kit_selftest.py` | PASS (32 checks) - run once per kit revision, green before this handoff was written |

### Certification prompts

`_handoff/S_saasm_cont_app-builder-marketing_20260916_060744.receipts.json`, decided by `prompt_receipt_lint.py` (G40).

| Prompt | Gate | Verdict | Checks answered |
|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 |
| `QC_spec.md` | G34 | PASS | 15 |
| `qc_toml.md` | G36 | PASS | 120 |
| `qc_docker.md` | G35 | PASS | 105 |
| `qc_solution_checklist.md` | G37 | PASS | 0 (the prompt declares no id registry) |
| `qc_rubric.md` | G53 | PASS | 16 |
| `task_code_verifier.md` | G3 | VALID | 12 |

Every one is **SELF-ATTESTED**: one agent authored the artifacts and ran the reviews, so
owner equals verifier. The kit's rule is owner != verifier, and G40 records this as a
recorded verdict rather than an independent one. An independent reviewer re-running the
seven prompts is the remaining step.

## Defects found and fixed

### First pass, against kit revision 7a667b7

| Found by | Defect | Fix |
|---|---|---|
| G6 `fixture_lint.py` | the graders asserted the seeded slug `spreadsheet-to-an-afternoon` while the brief pinned `spreadsheet-to-app-in-an-afternoon`: the Bug-2 shape, a complete app scoring zero | INV1 resync across every derived carrier, toward the brief |
| G6 `fixture_lint.py` | three endpoints were asserted by graders and pinned nowhere in the brief | added to the API shapes table and to the ledger |
| `qc_docker.md` | four `apt-get install` layers ran after `rm -rf /var/lib/apt/lists/*`, so the build would have died with no package index | restructured into two apt groups, each ending with its own cleanup |
| G55 RD-6 | probe emails used the RFC-6761 reserved TLD `.test` | moved to `@example.com` |
| G28/G29 `channel_lint.py` | seventeen checklist parts were judged twice | each contested part given to one channel |
| `qc_toml.md` TAX-011 | `spec_sections_given` listed `frontend` last instead of after `uiux` | reordered |
| `rubric_author.md` S5.3 | J13 was typed `discrimination`; a ruled-out layout is a commission | retyped and regenerated |
| `QC_instruction.md` C4 | the mode commitment was lost in a window-budget trim | restored |
| `QC_spec.md` S3/S5/S6/S7/G2 | the authoring docs lacked five required parts | all five added |

### Realignment, to kit revision b3d0577

The kit moved three commits while this bundle sat finished. What changed, and
what it cost here:

| Change upstream | What the bundle carried | What it carries now |
|---|---|---|
| `[task].authors` is two BARE addresses, the QL first and the contributor second; `authors_fixed` retired | seven `{ email = ... }` tables | `[abhishek.shaw@ethara.ai, nishant.dubey@ethara.ai]`, with `contributor_id` equal to the second (META-012) |
| `[task].uuid_v5` empty-string placeholder retired | `""` | minted by `task_code.py uuid5` |
| `[signoff]` retired (G62 / SIGN-004) | four empty rows | the block is gone |
| `[metadata].launch_surface` added, five drawn from an eighteen-token bank | absent | `alt_text`, `page_view_log`, `privacy_page`, `sitemap_robots`, `terms_page`, each an obligation in the brief |
| the pytest module is `test_pytest.py` on every task (CON-2) | `test_app.py` | renamed, with every substep id and the provenance sidecar updated. SUPERSEDED by `da24d3b` below, which moved the name again to `test_output.py` |
| `solution/app/` and `solution/USER_README.md` retired; the canary moves to `solution/TRUTH.md` | `solution/app/` with a README, a run manifest and `trinity/TRUTH.md` | `solution/TRUTH.md` generated from `grounding.yaml`; `solve.sh` is now a loud NO-SOLUTION stub |
| the canary is TWO lines, preamble plus GUID | one line | the preamble line added to `canary_block` and regenerated |
| `tests/traceability.md` and its CSV retired; only the matrix ships | both shipped | deleted |
| G9: every pytest substep declares a `category` and a DERIVED `weight` | neither | all 36 substeps categorised, weight derived from the category-and-critical pair, mix floors met |
| G27: `importance` must equal the score magnitude | three criteria disagreed | R10, R12 and R13 retyped and regenerated |
| A5: the brief carries NO hex anywhere; a companion colour is carried as family, tone and shade | 85 hex values | all 85 replaced with the phrase `source_lint.colour_words` derives, so the gate and the brief cannot drift |
| G43: `cubic-bezier(` is banned brief-wide | six easing tokens pinned by curve | each stated as its character in words |
| G51 (c): every enumerated item in the companion needs a footprint | 634 of 817 | 817 of 817, after carrying the named keyframes, the transitioned properties, the runtime bindings, the icon geometry, the documentation tree, the captured widths, the performance budget and the whole copy deck |
| G24: a `cov:` citation must share wording with the step that makes it | 55 citations shared none | the pytest lane cites through its sidecar, and twelve browser substeps were reworded to say what they actually observe |
| `QC_instruction.md` gained D5, the companion contradiction sweep | the brief said motion is `instant` and "nothing eases in" while carrying the companion's eight easing curves: a real inversion | `instant` is scoped to the studio; the seven public routes keep the measured house easing |

## Budget

`turns_expected` 120, `tokens_expected` 4,500,000: the Standard tier and the medium band.
Two services, two roles, one withheld lever, a large supplied visual specification to
carry, and a critical focus with two halves (the row and the object). `difficulty` is the
empty authoring placeholder; calibration writes the real value.

## Versions

| Component | Version |
|---|---|
| Kit | `deku-green-field` (this working tree) |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Verifier mode | `separate` |
| Harbor | `0.20.0` |

## Blocking findings

None from the kit's own battery. Two carried forward:

1. **Grader pin drift (C11).** `config/kit-config.yaml` pins `0.22.0` while
   `vendor/grader-0.23.0/` exists and differs in every file. The pin is deliberately not
   flipped: only `test.sh` ships per bundle and the rest lives in `deku-verifier-base`,
   which the kit cannot inspect. Ask the harness team which generation that image is built
   from before re-vendoring.
2. **`[delivery.images]` is absent.** `validate_task.py` requires every entry to be a
   `@sha256:` digest present in `environment/`, and the provider catalog pins by version
   tag. No digest was fabricated. The key is optional and the block validates without it;
   resolve the digests at packaging time.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. `solution/app/` carries no application code (D20, `app-deferred`), so
`solve.sh` fails loudly by design. Nothing counts toward corpus targets until the code
lands and `harbor run -a oracle` returns `1.0` twice.
