# Build report: S_commu_dire_token-citizen-directory-vb_20260916_071749

## Identity

| | |
|---|---|
| Task code | `S_commu_dire_token-citizen-directory-vb_20260916_071749` |
| Task id | `deku/token-citizen-directory-vb` |
| Cell | solo_founder / community-social / directory-matching |
| Service profile | `P4-db-storage` |
| Providers | `backend = postgres`, `storage = minio` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `python` |
| Design direction | `companion` (the drawn `editorial-serif` is recorded, and does not govern) |
| Launch surface | `alt_text,form_validation,meta_tags,privacy_page,spam_protection` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Companion | `kprverse_prd.md`, 4237 lines, 38 sections |

## Derived design draws

```
draw: render_model = spa-json-api
draw: backend = Litestar
draw: frontend = Preact + Vite
draw: design_direction = companion
draw: nav = top-nav
draw: work_surface = card-grid
draw: create_flow = modal
draw: feedback = optimistic-row
```

The pattern was keyed from the Task Order's `directory-profiles`, which is outside
the closed fifteen-pattern enum, onto `directory-matching`: the enum member whose
critical focus, cross-tenant isolation on a direct request, is this product's own
write boundary. The companion records the same substitution in its section 37.5.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Story route, pinned scroll sequence | INCLUDED | `## Core features`, `## Front-end specification` | companion sections 7, 8, 9 |
| Protocol route and the hold control | INCLUDED | `## Core features`, `## Front-end specification` | companion sections 8.6, 10 |
| Catalogue, packed index, thirteen facets | INCLUDED | `## Core features`, `## Data model` | companion section 11 |
| Standalone filter route | INCLUDED | `## Core features` | companion section 12 |
| Registration and address binding | INCLUDED | `## Core features`, `## User flow` | companion sections 13, 20 |
| Citizen directory and passport documents | INCLUDED | `## Core features`, `## Data model` | companion sections 14, 22, 24 |
| Journal, media library, about, legal | INCLUDED | `## Core features` | companion sections 15 to 18 |
| Console overlay | INCLUDED | `## Core features`, `## Front-end specification` | companion section 19 |
| Mint route | INCLUDED as a closed state | `## Core features` | companion section 37.3 names the erroring route as a defect |
| Wallet signature cryptography | DROPPED | recorded in `_spec/.../00-decisions.md` | no chain node and no wallet provider exist in the closed world; every itemised property of companion 20.5 is preserved as a server-issued single-use challenge |
| External content system | DROPPED | recorded in `_spec/.../00-decisions.md` | replaced by seeded editorial rows; companion 1.2's no-editor-role constraint is preserved |
| Ownership indexing service | DROPPED | recorded in `_spec/.../00-decisions.md` | replaced by a seeded holdings ledger; companion 22.7's cache-is-never-the-authority rule is preserved |
| Headless-browser render mechanism | DROPPED | recorded in `_spec/.../00-decisions.md` | INV9 forbids naming the mechanism; the harness route, its signed parameter and its ready signal are all kept |
| Build order and difficulty grading | WAIVED | `--waive "grade distribution"` | companion section 34 grades the authoring work, not the product |
| Acceptance checklist | WAIVED | `--waive "acceptance checklist"` | companion section 38 is restated as the product's own rules |

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_challenge_binds_the_address_and_the_row_survives_a_reload`, `test_owner_edits_persist_and_the_record_survives_a_reload`, `test_seeded_catalogue_carries_ten_thousand_records` |
| `storage` | `minio` | MET | `test_catalogue_index_file_is_stored_in_the_bucket`, `test_passport_object_is_stored_in_the_bucket_at_its_key`, `test_another_citizens_passport_document_is_denied` |

## Grading surface

| | |
|---|---|
| Workflows | 16 (solo_founder band 10 to 16) |
| Browser substeps | 31 |
| Pytest substeps | 34 |
| Critical substeps | 19 |
| Non-happy-path ids | `invalid_profile_edit_is_refused_with_the_field_named`, `cross_account_profile_write_is_denied`, `another_citizens_passport_document_is_denied`, `concurrent_nickname_claims_accept_at_most_one` |
| Pytest module | `tests/test_output.py`, one module, 34 functions |
| Banners covered | core features, data integrity, authorization, edge cases |
| Checklist items | 320 |
| Item classes | capability 17, constraint 126, contract 23, data 38, literal 52, role 14, ui 50 |

### Pytest functions and the obligations each discharges

| Function | Checklist items |
|---|---|
| `test_health_and_deployment_contract` | 20 |
| `test_public_routes_carry_distinct_titles_and_descriptions` | 15 |
| `test_privacy_page_is_linked_from_every_page_footer` | 5 |
| `test_signup_creates_account_and_refuses_a_duplicate_email` | 7 |
| `test_seeded_accounts_sign_in_with_the_corpus_password` | 7 |
| `test_challenge_binds_the_address_and_the_row_survives_a_reload` | 18 |
| `test_address_comparison_is_case_insensitive` | 3 |
| `test_seeded_catalogue_carries_ten_thousand_records` | 12 |
| `test_identifier_shift_resolves_every_worked_example` | 5 |
| `test_citizen_record_is_assembled_from_the_seeded_row` | 13 |
| `test_holdings_response_names_whether_a_citizen_record_exists` | 5 |
| `test_journal_category_filter_and_media_counts_sum` | 15 |
| `test_unpublished_achievement_is_absent_from_every_list` | 6 |
| `test_media_download_address_is_minted_per_request` | 7 |
| `test_console_echoes_typed_input_as_text` | 5 |
| `test_unknown_address_renders_the_product_not_found_page` | 5 |
| `test_owner_edits_persist_and_the_record_survives_a_reload` | 12 |
| `test_omitted_field_is_left_alone_and_an_explicit_null_clears_it` | 2 |
| `test_catalogue_index_file_is_stored_in_the_bucket` | 19 |
| `test_passport_object_is_stored_in_the_bucket_at_its_key` | 9 |
| `test_repeated_generation_request_returns_the_run_in_flight` | 8 |
| `test_concurrent_nickname_claims_accept_at_most_one` | 2 |
| `test_refused_nickname_claim_stores_nothing` | 2 |
| `test_cross_account_profile_write_is_denied_and_the_row_is_unchanged` | 11 |
| `test_unauthenticated_profile_write_is_denied` | 3 |
| `test_citizen_record_hides_renders_from_every_other_caller` | 3 |
| `test_another_citizens_passport_document_is_denied` | 5 |
| `test_render_harness_refuses_without_a_signed_parameter` | 6 |
| `test_no_credential_appears_in_anything_the_browser_downloads` | 4 |
| `test_form_validation_refuses_invalid_input_and_stores_nothing` | 10 |
| `test_unowned_representative_item_is_refused` | 2 |
| `test_replayed_challenge_nonce_is_refused` | 4 |
| `test_challenge_for_another_address_is_refused` | 5 |
| `test_automated_form_submission_is_refused` | 4 |

## Rubric

| | |
|---|---|
| Judged criteria | 13 |
| Positive / negative | 11 / 2 |
| Positive total | 33 |
| Negative magnitude | 6 |
| Compiled reference items | 34, compiled-weight share 1.0 |

| Dimension | Positive criteria | Share | Target |
|---|---|---|---|
| `instruction_following` | 2 | 0.30 | 0.30 |
| `functionality` | 2 | 0.24 | 0.25 |
| `ux_flow` | 2 | 0.18 | 0.15 |
| `ui_visual` | 2 | 0.18 | 0.15 |
| `motion` | 1 | 0.03 | 0.05 |
| `accessibility` | 1 | 0.03 | 0.05 |
| `responsiveness` | 1 | 0.03 | 0.05 |

Criterion-to-item provenance is in `_handoff/S_commu_dire_token-citizen-directory-vb_20260916_071749.rubric-provenance.json`;
`rubric_align_lint.py` (G39) confirms every criterion cites a real checklist item
and every judgment-class item is graded by a criterion or a browser substep.

## Literals ledger

| Class | Count | Sample |
|---|---|---|
| `account` | 3 | `member@example.com`, `member2@example.com`, `member3@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `design_phrase` | 9 | `corner cut`, `drafting grid`, `light vivid lime`, `deep muted teal` ... |
| `endpoint` | 23 | `/api/health`, `/api/auth/signup`, `/api/auth/login`, `/api/auth/logout` ... |
| `env_var` | 8 | `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` ... |
| `motion_moment` | 9 | `rise a short distance while fading in`, `type on character by character`, `flash in a run of hard opacity steps`, `pulse outward and fade` ... |
| `number` | 14 | `10000`, `13`, `5022`, `4978` ... |
| `route` | 17 | `/protocol`, `/gallery`, `/filters`, `/journal` ... |
| `scheme` | 4 | `citizens/<address_lower>/<face>/<content_hash>.png`, `thumbs/<digest>.png`, `images/<digest>.png`, `images_fullbleed/<digest>.png` |
| `seed_record` | 69 | `0xA7d3F1b2C4e5D6a7B8c9D0e1F2a3B4c5D6e7F801`, `0xB2c4E5d6F7a8B9c0D1e2F3a4B5c6D7e8F9a0B102`, `0xC3d5F6a7B8c9D0e1F2a3B4c5D6e7F8a9B0c1D203`, `SIGN IN` ... |
| `status` | 26 | `pending`, `ready`, `failed`, `active` ... |

Total pinned values: 183. `fixture_lint.py` (G6) confirms the
bijection in both directions between the ledger, `instruction.md` and the graders.

## Spec folder

Written to `Output/16-sep-2026/_spec/S_commu_dire_token-citizen-directory-vb_20260916_071749/`, never inside the bundle.

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the residual judgment calls, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow`, `## Deployment contract` API shapes |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at this variant |

## Grading window

| Section | Chars | Chars the judge reads |
|---|---|---|
| `Core features` | 35855 | 2500 |
| `User flow` | 5025 | 2500 |
| `UI/UX notes` | 11443 | 2500 |
| `Constraints` | 1072 | 1072 |
| `User roles` | 3875 | 2500 |
| `Overview` | 2916 | 2500 |

Joined across the six judged sections: 13572 against the 9,000 slice.
`window_lint.py` (G33) reports length and fails nothing on it. The judged criteria
are self-contained and carry their own `evaluation_rule`, so prose past the slice
costs a diagnostic number rather than reward.

## Kit gate log

Rendered from `_handoff/S_commu_dire_token-citizen-directory-vb_20260916_071749.gates.jsonl`. Never transcribed.

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

`G59/G60` exits 2 because the bundle ships no code-quality rubric, which is legal:
that channel is advisory and optional. `G40` exits 0 with verdict WARN because every
prompt receipt records `verifier: self`.

## Prompt receipts

| Prompt | Gate | Verdict | Checks | Non-PASS | Verifier |
|---|---|---|---|---|---|
| `QC_spec.md` | G34 | PASS | 15 | 3 | self |
| `QC_instruction.md` | G34 | PASS | 24 | 7 | self |
| `qc_toml.md` | G36 | PASS | 120 | 10 | self |
| `qc_docker.md` | G35 | PASS | 105 | 14 | self |
| `qc_solution_checklist.md` | G37 | PASS | 0 | 0 | self |
| `task_code_verifier.md` | G3 | VALID | 12 | 0 | self |
| `generate_instruction.md` | S2 | PASS | 0 | 0 | self |
| `solution_checklist.md` | S3 | PASS | 0 | 0 | self |
| `toml_generator.md` | S4 | PASS | 0 | 0 | self |
| `docker_generator.md` | S5 | PASS | 0 | 0 | self |
| `pytest_generator.md` | S7 | PASS | 0 | 0 | self |
| `rubric_author.md` | S8 | PASS | 0 | 0 | self |
| `qc_rubric.md` | G53 | PASS | 16 | 1 | self |

Every non-PASS check carries a finding in `_handoff/S_commu_dire_token-citizen-directory-vb_20260916_071749.receipts.json`. The seven
WARNs on `QC_instruction.md` and the three on `QC_spec.md` are all the same shape: a
check written before the settled number rule and before `## Build plan` left the
baseline, answered against the rule that now governs and recorded rather than hidden.

## Handoff gates, undecided here

The kit has no harness access, so these are stated with their commands and expected
verdicts and decided downstream: G13, G15, G18, G19, G20, G21, G25. See
`_handoff/S_commu_dire_token-citizen-directory-vb_20260916_071749.handoff.md`.

## Blocking findings

NONE. No spec gap and no harness gap prevented a required check. Two G51 subject
groups are waived on the record, both because the companion states values the brief
may not carry: the CSS custom-property rows in companion section 3, whose content is
a token name and a length, and the audio synthesis recipes in companion section 36.4,
whose content is a frequency and a duration. Both subjects reach the brief as words,
which is what the number rule requires; only their numeric bodies are dropped.

## Budget

`turns_expected = 170`, `tokens_expected = 7000000`. The build carries seventeen
routes, a ten thousand row catalogue seed with thirteen facets, an object-store write
path, an asynchronous generation surface and a scene layer, which is the hard band
rather than the medium one.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the app is built downstream
from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
