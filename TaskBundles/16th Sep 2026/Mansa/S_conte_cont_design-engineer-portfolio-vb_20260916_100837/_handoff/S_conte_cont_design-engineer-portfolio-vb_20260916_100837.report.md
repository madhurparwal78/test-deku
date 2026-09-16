# Build report -- S_conte_cont_design-engineer-portfolio-vb_20260916_100837

Rendered from `_handoff/S_conte_cont_design-engineer-portfolio-vb_20260916_100837.gates.jsonl`. No verdict in this file was typed by hand.

## Identity

| | |
|---|---|
| task code | `S_conte_cont_design-engineer-portfolio-vb_20260916_100837` |
| task id | `deku/design-engineer-portfolio-vb` |
| cell | solo_founder / content-publishing / content-publishing (the Task Order wrote the domain `portfolio-agency`, which is outside the reference/A taxonomy; mapped to `content-publishing`, recorded in `_spec/.../00-decisions.md`) |
| archetype | `design-engineer-portfolio` |
| service profile | `P4-db-storage` |
| providers | `backend = postgres`, `storage = minio` |
| variant | `b`, axes `["critical_depth", "spec_sections"]` |
| language | `python` (Flask with server-rendered Jinja templates, vanilla progressive enhancement) |
| design direction | `companion` (reference/L L.6.1; the draw was `warm-hospitality` and does not govern) |
| launch surface | `custom_404,mobile_viewport,no_broken_links,page_view_log,single_cta` |
| authentication | passcode only, no accounts: `/studio` (owner) and `/field-notes` (one gated article) |
| shard | 1 of 1 (single-operator run) |
| kit revision | git HEAD `806eb0a`, 2026-09-16 |
| vendored grader | `0.22.0` |
| target schema | `1.4` |
| verifier mode | `separate` |
| rubric | `tests/rubric.json` generated from `grounding.yaml`; READ at runtime as of grader 0.21.0 |
| companion | `9.16_prds/prd8/haoqi_prd.md` (site `haoqi.design`, renamed `atlas.design` in the brief) |
| authors | kaustubh.dalvi@ethara.ai (QL), mansa.gupta@ethara.ai (contributor) |

## Operator overrides

- The kit's per-section and overall character caps on `instruction.md` were set aside at the operator's request; the brief runs long on purpose, and `window_lint.py` reports length without failing.
- The visual half of the brief follows `generation_instruction_guidelines (1).md`: every surface, effect and motion is described in words by purpose, character and relationship, with no pixel sizes, positions, colour codes, font family names, animation or easing names, timings, function names or parameter values. Machine hooks, copy, content facts and accessibility floors stay exact because the grader reads them.
- The tech stack is named (Flask, Jinja, PostgreSQL, MinIO, vanilla JavaScript, one WebGL scene with a static fallback, the Web Audio API for the sound control).

## Grading layer

| | |
|---|---|
| workflows | 15 |
| browser substeps | 30 |
| pytest substeps | 62 |
| critical substeps | 20 |
| non-happy-path ids | 9: `friend_unlocks_field_notes_with_its_code`, `gated_article_denied_without_its_code`, `passcode_attempts_limit_and_invalid_input`, `visitor_cannot_reach_the_studio`, `draft_is_denied_everywhere`, `owner_unlocks_the_studio_and_previews_drafts`, `owner_publishes_a_case_study_with_a_figure`, `invalid_case_study_input_is_refused`, `duplicate_or_invalid_figure_upload_is_refused` |
| pytest module | `tests/test_output.py`, HTTP, database and bucket checks plus page-driven checks through Playwright |
| test functions | 62 |
| checklist items | 402 across 10 sections |

Checklist items per section: C-CF 157, C-CN 3, C-DC 19, C-DM 24, C-FE 59, C-OV 10, C-RL 18, C-TR 24, C-UF 26, C-UX 62.

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | critical substeps read persisted rows (`case_study`, `project_card`, `passcode_grant`, `page_view`) through the `backend` fixture |
| `storage` | `minio` | MET | the upload substeps read the object at `case-studies/{case_study_id}/figures/{sha256}.{ext}` through the `store` fixture |

## Rubric

22 judged criteria, 21 positive and 1 negative. Positive total 65.

| Dimension | Share | Target | Criteria |
|---|---|---|---|
| `instruction_following` | 0.262 | 0.3 | 5 |
| `functionality` | 0.185 | 0.25 | 4 |
| `ux_flow` | 0.215 | 0.15 | 4 |
| `ui_visual` | 0.200 | 0.15 | 5 |
| `motion` | 0.046 | 0.05 | 1 |
| `accessibility` | 0.046 | 0.05 | 1 |
| `responsiveness` | 0.046 | 0.05 | 1 |

Compiled answer key: 14 items in `solution/trinity/rubrics.json`, compiled-weight share 1.0, each naming a committed checker in `tests/test_output.py`.

## Grading window

| Section | Chars | Reference |
|---|---|---|
| `core_features` | 22963 | 2400 |
| `user_flow` | 5926 | 1900 |
| `ui_ux_notes` | 15123 | 1700 |
| `constraints` | 1228 | 800 |
| `user_roles` | 2380 | 1000 |
| `overview` | 1825 | 700 |
| joined | 49445 | 8,800 |

`window_lint.py` reports length and fails nothing. The operator lifted the caps. `## Core features` runs past the judge's 2,500-char slice; every rule past it that moves reward is graded by pytest or restated in the rubric criterion the judge reads.

## Literals ledger

212 pinned values.

| Class | Value | Carriers |
|---|---|---|
| `credential` | `5093` | `instruction.md`, `conftest.py`, `test_output.py` |
| `credential` | `2718` | `instruction.md`, `conftest.py` |
| `route` | `/studio` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/field-notes` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/kindling` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/almanac-mono` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/wasm-design-utils` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/ndrive` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/coast-icon` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/teamharbor` | `instruction.md`, `conftest.py`, `test_output.py` |
| `route` | `/nothing-here` | `instruction.md` |
| `endpoint` | `/api/passcode` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `/api/passcode/release` | `instruction.md`, `test_output.py` |
| `endpoint` | `/api/health` | `instruction.md`, `test_output.py` |
| `endpoint` | `/api/site` | `instruction.md`, `test_output.py` |
| `endpoint` | `/api/projects` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `/api/case-studies/{slug}` | `instruction.md`, `test_output.py` |
| `endpoint` | `/api/figures/{id}` | `instruction.md` |
| `endpoint` | `/api/studio/case-studies` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `/api/studio/case-studies/{id}/publish` | `instruction.md` |
| `endpoint` | `/api/studio/case-studies/{id}/stub` | `instruction.md` |
| `endpoint` | `/api/studio/case-studies/{id}/hold` | `instruction.md` |
| `endpoint` | `/api/studio/case-studies/{id}/figures` | `instruction.md` |
| `endpoint` | `/api/studio/page-views` | `instruction.md`, `test_output.py` |
| `endpoint` | `/app/USER_README.md` | `instruction.md`, `test_output.py` |
| `endpoint` | `.browser_screenshots/` | `instruction.md` |
| `endpoint` | `.downloads/` | `instruction.md` |
| `endpoint` | `external_url` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `column_start` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `column_span` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `column_start_lg` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `column_span_lg` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `sort_order` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `media_alt` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `year_label` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `character_count` | `instruction.md`, `test_output.py` |
| `endpoint` | `character_label` | `instruction.md`, `test_output.py` |
| `endpoint` | `last_updated_label` | `instruction.md`, `test_output.py` |
| `endpoint` | `composed_width` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `composed_height` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `outbound_url` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `gated_path` | `instruction.md`, `conftest.py` |
| `endpoint` | `published_at` | `instruction.md`, `test_output.py` |
| `endpoint` | `alt_text` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `object_key` | `instruction.md`, `test_output.py` |
| `endpoint` | `content_type` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `byte_size` | `instruction.md`, `test_output.py` |
| `endpoint` | `viewed_at` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `redaction_length` | `instruction.md`, `test_output.py` |
| `endpoint` | `timezone_label` | `instruction.md`, `test_output.py` |
| `endpoint` | `region_code` | `instruction.md`, `test_output.py` |
| `endpoint` | `contact_email` | `instruction.md`, `test_output.py` |
| `endpoint` | `brand_suffix` | `instruction.md`, `test_output.py` |
| `endpoint` | `discipline_label` | `instruction.md`, `test_output.py` |
| `endpoint` | `project_card` | `instruction.md`, `test_output.py` |
| `endpoint` | `passcode_gate` | `instruction.md`, `test_output.py` |
| `endpoint` | `code_hash` | `instruction.md`, `test_output.py` |
| `endpoint` | `slug_redirect` | `instruction.md`, `test_output.py` |
| `endpoint` | `old_slug` | `instruction.md`, `test_output.py` |
| `endpoint` | `page_view` | `instruction.md`, `test_output.py` |
| `endpoint` | `case_study_id` | `instruction.md`, `conftest.py`, `test_output.py` |
| `endpoint` | `passcode_grant` | `instruction.md`, `test_output.py` |
| `endpoint` | `released_at` | `instruction.md`, `test_output.py` |
| `endpoint` | `4173` | `instruction.md` |
| `status` | `draft` | `instruction.md`, `conftest.py`, `test_output.py` |
| `status` | `stub` | `instruction.md`, `conftest.py`, `test_output.py` |
| `status` | `published` | `instruction.md`, `conftest.py`, `test_output.py` |
| `status` | `rate_limited` | `instruction.md`, `conftest.py`, `test_output.py` |
| `status` | `position_taken` | `instruction.md`, `conftest.py` |
| `status` | `invalid_placement` | `instruction.md`, `conftest.py`, `test_output.py` |
| `status` | `invalid_slug` | `instruction.md`, `conftest.py` |
| `status` | `slug_reserved` | `instruction.md`, `conftest.py` |
| `status` | `slug_taken` | `instruction.md`, `conftest.py` |
| `status` | `incomplete` | `instruction.md`, `conftest.py`, `test_output.py` |
| `status` | `alt_text_required` | `instruction.md`, `conftest.py` |
| `status` | `invalid_dimensions` | `instruction.md`, `conftest.py` |
| `status` | `unsupported_type` | `instruction.md`, `conftest.py` |
| `status` | `file_too_large` | `instruction.md`, `conftest.py` |
| `status` | `429` | `instruction.md`, `test_output.py` |
| `status` | `invalid_media_alt` | `instruction.md`, `conftest.py` |
| `status` | `invalid_field` | `instruction.md`, `conftest.py` |
| `status` | `invalid_heading_levels` | `instruction.md`, `conftest.py` |
| `status` | `Refused` | `instruction.md`, `conftest.py` |
| `number` | `1440x900` | `instruction.md`, `test_output.py` |
| `number` | `390x844` | `instruction.md`, `test_output.py` |
| `number` | `Jan 15, 2026` | `instruction.md`, `test_output.py` |
| `number` | `2026-01-15` | `instruction.md`, `test_output.py` |
| `number` | `2020-2022` | `instruction.md`, `conftest.py`, `test_output.py` |
| `number` | `2024-2026` | `instruction.md`, `conftest.py` |
| `number` | `1,602` | `instruction.md`, `test_output.py` |
| `number` | `5, 1, 7, 6, 10, 1, 5, 9, 6, 10` | `instruction.md`, `conftest.py` |
| `number` | `16:9` | `instruction.md`, `conftest.py` |
| `number` | `1.54:1` | `instruction.md`, `conftest.py` |
| `number` | `0.71:1` | `instruction.md`, `conftest.py` |
| `number` | `1:1` | `instruction.md`, `conftest.py` |
| `seed_record` | `Tidewater Sketchbook` | `instruction.md`, `conftest.py` |
| `seed_record` | `tidewater` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Kindling` | `instruction.md`, `conftest.py` |
| `seed_record` | `Almanac Mono` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Wasm design utils` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `GlyphSymbols` | `instruction.md`, `conftest.py` |
| `seed_record` | `DuskMode` | `instruction.md`, `conftest.py` |
| `seed_record` | `nDrive` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Coast Icon` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Teamharbor` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Loop: See Hear Touch` | `instruction.md`, `conftest.py` |
| `seed_record` | `Loop: System Design` | `instruction.md`, `conftest.py` |
| `seed_record` | `Coding Project` | `instruction.md`, `conftest.py` |
| `seed_record` | `tools` | `instruction.md`, `conftest.py` |
| `seed_record` | `event` | `instruction.md`, `conftest.py` |
| `seed_record` | `https://www.example.com/plugins/glyphsymbols` | `instruction.md`, `conftest.py` |
| `seed_record` | `https://www.example.com/plugins/duskmode` | `instruction.md`, `conftest.py` |
| `seed_record` | `https://www.example.com/events/see-hear-touch` | `instruction.md`, `conftest.py` |
| `seed_record` | `https://www.example.com/events/system-design` | `instruction.md`, `conftest.py` |
| `seed_record` | `https://www.example.com/teamharbor` | `instruction.md`, `conftest.py` |
| `seed_record` | `https://www.example.com/almanac-mono/download` | `instruction.md`, `conftest.py` |
| `seed_record` | `Notes I keep for myself, shared with the people who ask.` | `instruction.md`, `conftest.py` |
| `seed_record` | `Work in progress - this page is not finished yet.` | `instruction.md`, `conftest.py` |
| `seed_record` | `Download Almanac Mono` | `instruction.md`, `conftest.py` |
| `seed_record` | `studio.rin@example.com` | `instruction.md`, `conftest.py` |
| `seed_record` | `Rin Alvez` | `instruction.md`, `test_output.py` |
| `seed_record` | `GMT+8` | `instruction.md`, `test_output.py` |
| `seed_record` | `CN` | `instruction.md`, `test_output.py` |
| `seed_record` | `atlas` | `instruction.md`, `test_output.py` |
| `seed_record` | `.design` | `instruction.md`, `test_output.py` |
| `seed_record` | `Sync, conflicts & recovery` | `instruction.md`, `conftest.py` |
| `seed_record` | `sync-conflicts-recovery` | `instruction.md`, `conftest.py` |
| `seed_record` | `offline-then-online` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `what-i-would-change` | `instruction.md`, `conftest.py`, `test_output.py` |
| `seed_record` | `Why another drive` | `instruction.md`, `conftest.py` |
| `seed_record` | `The merge sheet` | `instruction.md`, `conftest.py` |
| `seed_record` | `notes-2` | `instruction.md`, `test_output.py` |
| `seed_record` | `https://www.example.com/rin/x` | `instruction.md`, `conftest.py` |
| `seed_record` | `5,242,880` | `instruction.md` |
| `seed_record` | `https://www.example.com/rin/community` | `instruction.md`, `conftest.py` |
| `seed_record` | `https://www.example.com/rin/github` | `instruction.md`, `conftest.py` |
| `seed_record` | `Outside work, I build design tools for team efficiency.` | `instruction.md`, `conftest.py` |
| `seed_record` | `leading Design Engineering and AI exploration at` | `instruction.md`, `conftest.py` |
| `seed_record` | `Hirebase` | `instruction.md`, `conftest.py` |
| `seed_record` | `Orchard` | `instruction.md`, `conftest.py` |
| `scheme` | `case-studies/{case_study_id}/figures/{sha256_of_bytes}.{ext}` | `instruction.md` |
| `env_var` | `DATABASE_URL` | `instruction.md` |
| `env_var` | `STORAGE_ENDPOINT` | `instruction.md`, `test_output.py` |
| `env_var` | `STORAGE_BUCKET` | `instruction.md`, `test_output.py` |
| `env_var` | `STORAGE_ACCESS_KEY` | `instruction.md` |
| `env_var` | `STORAGE_SECRET_KEY` | `instruction.md` |
| `env_var` | `APP_PUBLIC_URL` | `instruction.md` |
| `env_var` | `APP_PUBLIC_PORT` | `instruction.md` |
| `design_phrase` | `Please enter passcode` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Passcode for` | `instruction.md`, `conftest.py` |
| `design_phrase` | `That code is not right. Try again.` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Too many attempts. Wait a minute and try again.` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Nothing is filed at this address.` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Back to the index` | `instruction.md`, `conftest.py` |
| `design_phrase` | `THEME[A]` | `instruction.md`, `conftest.py` |
| `design_phrase` | `SOUND[` | `instruction.md`, `conftest.py` |
| `design_phrase` | `COPIED` | `instruction.md`, `conftest.py`, `test_output.py` |
| `design_phrase` | `Metadata` | `instruction.md`, `conftest.py`, `test_output.py` |
| `design_phrase` | `Last Updated` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Dimensions` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Characters` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Case studies` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Index preview` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Page views` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Lock studio` | `instruction.md`, `conftest.py` |
| `design_phrase` | `New case study` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Selected work` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Innovate` | `instruction.md`, `conftest.py`, `test_output.py` |
| `design_phrase` | `Extraordinary` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Twitter/X` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Community` | `instruction.md`, `conftest.py` |
| `design_phrase` | `GitHub` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Thinking in systems.` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Designing with care.` | `instruction.md`, `conftest.py` |
| `design_phrase` | `I explore how to shape AI-era workflows` | `instruction.md`, `conftest.py` |
| `design_phrase` | `I bring` | `instruction.md`, `conftest.py` |
| `design_phrase` | `craft & taste` | `instruction.md`, `conftest.py` |
| `design_phrase` | `to digital work` | `instruction.md`, `conftest.py` |
| `design_phrase` | `Published to the index.` | `instruction.md` |
| `design_phrase` | `Held as a draft.` | `instruction.md` |
| `design_phrase` | `Marked as a stub.` | `instruction.md` |
| `design_phrase` | `Refused. Another card already holds that position.` | `instruction.md` |
| `design_phrase` | `data-scroller` | `instruction.md`, `test_output.py` |
| `design_phrase` | `data-page` | `instruction.md`, `test_output.py` |
| `design_phrase` | `data-index-grid` | `instruction.md`, `test_output.py` |
| `design_phrase` | `data-order` | `instruction.md`, `test_output.py` |
| `design_phrase` | `data-band` | `instruction.md`, `test_output.py` |
| `design_phrase` | `data-redacted` | `instruction.md`, `test_output.py` |
| `design_phrase` | `data-reading-rail` | `instruction.md`, `test_output.py` |
| `design_phrase` | `data-line-number` | `instruction.md`, `test_output.py` |
| `design_phrase` | `data-slot-state` | `instruction.md`, `test_output.py` |
| `design_phrase` | `data-status` | `instruction.md`, `test_output.py` |
| `design_phrase` | `not-found` | `instruction.md`, `test_output.py` |
| `design_phrase` | `case-study` | `instruction.md`, `test_output.py` |
| `design_phrase` | `aria-pressed` | `instruction.md`, `test_output.py` |
| `design_phrase` | `Contents` | `instruction.md`, `test_output.py` |
| `design_phrase` | `no gutter` | `instruction.md` |
| `design_phrase` | `warm off-white paper` | `instruction.md` |
| `design_phrase` | `one ink` | `instruction.md` |
| `design_phrase` | `sentence case` | `instruction.md` |
| `design_phrase` | `sandwiched between two drawing surfaces` | `instruction.md` |
| `design_phrase` | `Menu` | `instruction.md`, `conftest.py`, `test_output.py` |
| `design_phrase` | `first-screen` | `instruction.md`, `conftest.py` |
| `motion_moment` | `on-off flicker` | `instruction.md` |
| `motion_moment` | `one just behind the other` | `instruction.md` |
| `motion_moment` | `draws itself` | `instruction.md` |
| `motion_moment` | `growing sideways` | `instruction.md` |
| `motion_moment` | `squashing and stretching sideways` | `instruction.md` |
| `motion_moment` | `leaves faster` | `instruction.md` |
| `motion_moment` | `one character at a time from left to right` | `instruction.md` |
| `motion_moment` | `a beat behind its first` | `instruction.md` |
| `env_var` | `DB_ADMIN_URL` | `task.toml` |

## spec/ documents

Authored at `_spec/S_conte_cont_design-engineer-portfolio-vb_20260916_100837/`, outside the bundle (CON-5).

| Document | Fed |
|---|---|
| `00-decisions.md` | the audit trail, the draws, the domain mapping, waivers and the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements`, `## Deployment contract` |
| `03-app-flow.md` | `## User flow`, the API shapes and the copy deck |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing: `## Build plan` is not baseline and this variant does not request it |

## Kit gate log

Rendered from the receipts, one row per gate (last run).

| Gate | Tool | Exit | Verdict | Findings |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 2 | NOT-APPLICABLE | 0 |
| `G1/G12` | `layout_lint.py` | 0 | PASS | 0 |
| `G46` | `structure_lint.py` | 0 | PASS | 0 |
| `G50` | `docker_lint.py` | 0 | PASS | 0 |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | 0 |
| `G63` | `secret_lint.py` | 0 | PASS | 0 |
| `G48` | `truth_lint.py` | 0 | PASS | 0 |
| `G51` | `source_lint.py` | 0 | PASS | 0 |
| `G52` | `rubric_context_lint.py` | 0 | PASS | 0 |
| `G54` | `comment_lint.py` | 0 | PASS | 0 |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | 0 |
| `G11` | `leak_scan.py` | 0 | PASS | 0 |
| `G33` | `window_lint.py` | 0 | PASS | 0 |
| `G4/G5` | `contract_lint.py` | 0 | PASS | 0 |
| `G43` | `prescription_lint.py` | 0 | PASS | 0 |
| `G44` | `disclosure_lint.py` | 0 | PASS | 0 |
| `G10` | `no_sdk_lint.py` | 0 | PASS | 0 |
| `G31` | `determinism_lint.py` | 0 | PASS | 0 |
| `G14` | `reward_path_lint.py` | 0 | PASS | 0 |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | 0 |
| `G41` | `flag_lint.py` | 0 | PASS | 0 |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | 0 |
| `G59/G60` | `codequality_lint.py` | 2 | ? | 0 |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | 0 |
| `G6` | `fixture_lint.py` | 0 | PASS | 0 |
| `G24` | `coverage_map.py` | 0 | PASS | 0 |
| `G37` | `checklist_qc.py` | 0 | PASS | 0 |
| `G39` | `rubric_align_lint.py` | 0 | PASS | 0 |
| `G28/G29` | `channel_lint.py` | 0 | PASS | 0 |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | 0 |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | 0 |
| `G47` | `output_qc.py` | 0 | PASS | 0 |

Waivers passed to G51 (companion carriage), each a companion topic deliberately translated into words or dropped: `normative`, `keyframes`, `classification`, `acceptance checklist`, `cubic-bezier`, `rgb`, `lab(`, `alias of`, `background-deep`, `linear-gradient`, `rotate: -45deg`, `transform: rotate`, `hsstfade`, `ui-sans-serif`, `font-mono-2`, `portfolio-agency`, `design-engineer-portfolio`, `ledger fidelity`, `informational`, `style diff`, `oscillators`, `fractal turbulence`.

## Certification prompt receipts

| Prompt | Gate | Verdict | Checks answered | Attestation |
|---|---|---|---|---|
| `task_code_verifier.md` | `G3` | VALID | 12 | independent-subagent |
| `qc_rubric.md` | `G53` | PASS | 16 | independent-subagent |
| `QC_spec.md` | `G34` | PASS | 15 | independent-subagent |
| `QC_instruction.md` | `G34` | PASS | 24 | independent-subagent |
| `qc_solution_checklist.md` | `G37` | PASS | 0 | independent-subagent |
| `qc_toml.md` | `G36` | PASS | 120 | independent-subagent |
| `qc_docker.md` | `G35` | PASS | 105 | independent-subagent |

Each certification prompt was run by a separate reviewer subagent that did not write the bundle, over three cycles for the brief, spec, rubric and checklist. The findings from each cycle were fixed and the gates re-run. The reviewers ran under the same operator session, so this is independent review inside one run, not a second operator.

## Budget estimate

`turns_expected = 200`, `tokens_expected = 7500000`. Five pages, a passcode gate, a full owner studio with uploads and placement, ten tables and a heavy motion layer put this at the top of the documented band.

## Blocking findings

None for the mechanical battery. Two things are unresolved and are the operator's:

- `[delivery]` is absent. It is grandfathered, and filling it needs the `@sha256:` digests of `python:3.12-slim-bookworm`, `postgres:16.4-bookworm` and `minio/minio:RELEASE.2024-10-13T13-34-11Z`, which cannot be resolved without a registry.
- No reference application exists. The bundle carries a brief, a checklist, an answer key and a grading layer, and `solution/solve.sh` exits non-zero saying so.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`. Not admissible.
