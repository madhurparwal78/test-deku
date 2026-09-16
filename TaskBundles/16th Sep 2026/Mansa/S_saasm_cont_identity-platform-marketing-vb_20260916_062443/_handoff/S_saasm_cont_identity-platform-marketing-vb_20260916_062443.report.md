# Build report -- S_saasm_cont_identity-platform-marketing-vb_20260916_062443

Rendered from `_handoff/S_saasm_cont_identity-platform-marketing-vb_20260916_062443.gates.jsonl`. No verdict in this file was typed by hand.

## Identity

| | |
|---|---|
| task code | `S_saasm_cont_identity-platform-marketing-vb_20260916_062443` |
| task id | `deku/identity-platform-marketing-vb` |
| cell | solo_founder / saas-micro-tools / content-publishing |
| service profile | `P4-db-storage` |
| providers | `backend = postgres`, `storage = minio` |
| variant | `b`, axes `["critical_depth", "spec_sections"]` |
| language | `typescript` |
| design direction | `companion` (reference/L L.6.1; the draw was `playful-consumer` and does not govern) |
| launch surface | `cookie_choice,favicon,meta_tags,privacy_page,spam_protection` |
| spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 (single-operator run) |
| kit revision | git HEAD `806eb0a`, 2026-09-16 |
| vendored grader | `0.22.0` |
| target schema | `1.4` |
| verifier mode | `separate` (the kit default since commit `11eaf7b`) |
| rubric | `tests/rubric.json` generated from `grounding.yaml`; READ at runtime as of grader 0.21.0 |
| companion | `9.16_prds/prd1/clerk_prd.md`, 7,609 lines |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| The public marketing set, 28 routes | INCLUDED | `## Core features`, `## User flow`, `## Front-end specification` | the companion's measured half |
| The content library and publishing | INCLUDED | `## Core features` rules 1 to 5 | carries the pattern's critical focus |
| Media in the object store | INCLUDED | `## Core features` rules 6 to 8 | the declared storage slot |
| The documentation portal | INCLUDED | `## Core features` rules 9 to 12 | companion Section 17 |
| Pricing and the comparison matrix | INCLUDED | `## Core features` rules 13 to 17 | companion Section 16 |
| Changelog, glossary, blog, legal | INCLUDED | `## Core features` rules 18 to 25 | companion Sections 18, 19, 22, 29 |
| The model leaderboard | INCLUDED | `## Core features` rules 26 to 29 | companion Sections 20, 49 |
| The component theme editor | INCLUDED | `## Core features` rules 30 to 35 | companion Sections 21, 48 |
| Accounts and application instances | INCLUDED | `## Core features` rules 36 to 38 | the Task Order's end-to-end outcome |
| The launch surface | INCLUDED | `## Core features` rules 39 to 44 | the reference/O draw |
| The identity platform itself, Sections 36 to 47 | DROPPED | `## Constraints` | the product being sold, not the product being built; declared to G51 with `--waive` |
| Observability, Section 52, and operations, Section 55 | DROPPED | `## Constraints` | no channel observes them in a site build |
| The generated-answer surface, Section 51.2 | DROPPED | `## Constraints` | needs a model at run time; the index behind it is built |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_seeding_is_idempotent_across_a_restart`, `test_publish_writes_the_rendition_in_the_same_operation` assert persisted rows |
| `storage` | `minio` | MET | `test_uploaded_bytes_are_stored_in_the_bucket_and_nowhere_else` reads the bucket through the capability fixture |

## Grading layer

| | |
|---|---|
| workflows | 16 |
| browser substeps | 34 |
| pytest substeps | 65 |
| critical substeps | 28 |
| non-happy-path ids | 7: `draft_is_denied_to_everyone_but_its_author`, `reader_cannot_write_to_the_library`, `concurrent_publish_leaves_one_winner`, `invalid_entry_payload_is_refused`, `bot_submission_is_rejected_by_the_application_form`, `empty_states_and_the_not_found_page_read_correctly`, `seed_data_survives_a_restart_unduplicated` |
| pytest module | `tests/test_output.py`, one module covering core, data integrity, authorization, edge cases and the page-driven surface |
| test functions | 65 |
| checklist items | 367 across 10 sections |

Checklist items per section: C-CF 174, C-CN 14, C-DC 18, C-DM 28, C-FE 35, C-OV 6, C-RL 25, C-TR 17, C-UF 18, C-UX 32.

## Rubric

24 judged criteria, 23 positive and 1 negative. Positive total 73.

| Dimension | Share | Target | Criteria |
|---|---|---|---|
| `instruction_following` | 0.260 | 0.3 | 5 |
| `functionality` | 0.205 | 0.25 | 5 |
| `ux_flow` | 0.164 | 0.15 | 4 |
| `ui_visual` | 0.205 | 0.15 | 5 |
| `motion` | 0.082 | 0.05 | 2 |
| `accessibility` | 0.041 | 0.05 | 1 |
| `responsiveness` | 0.041 | 0.05 | 1 |

Compiled answer key: 26 items in `solution/trinity/rubrics.json`, compiled-weight share 1.0,
each naming a committed checker in `tests/test_output.py`.

## Grading window

| Section | Chars | Reference |
|---|---|---|
| `core_features` | 22283 | 2400 |
| `user_flow` | 6406 | 1900 |
| `ui_ux_notes` | 12303 | 1700 |
| `constraints` | 3865 | 800 |
| `user_roles` | 1668 | 1000 |
| `overview` | 1534 | 700 |
| joined | 48059 | 8,800 |

`window_lint.py` reports length and fails nothing. `## Core features` runs past the judge's
2,500-char slice; the rules that sit past it are the launch surface, 39 to 44, and every one of
them is graded by pytest rather than by the judge, so nothing that moves reward is lost.

## Literals ledger

194 pinned values.

| Class | Value | Carriers |
|---|---|---|
| `account` | `author@example.com` | `instruction.md`, `conftest.py` |
| `account` | `author2@example.com` | `instruction.md`, `conftest.py` |
| `account` | `reader@example.com` | `instruction.md`, `conftest.py` |
| `account` | `support@aegis.dev` | `instruction.md` |
| `account` | `security@aegis.dev` | `instruction.md` |
| `account` | `privacy@aegis.dev` | `instruction.md` |
| `credential` | `deku-demo-pw-2026` | `instruction.md`, `conftest.py` |
| `design_phrase` | `thin grey lines separating white boxes` | `instruction.md` |
| `design_phrase` | `only saturated colour` | `instruction.md` |
| `design_phrase` | `hairline ring` | `instruction.md` |
| `design_phrase` | `Space over dividers` | `instruction.md` |
| `design_phrase` | `per-band property` | `instruction.md` |
| `design_phrase` | `wide shallow trapezoidal notch` | `instruction.md` |
| `design_phrase` | `tabular lining numerals` | `instruction.md` |
| `design_phrase` | `barely softened` | `instruction.md` |
| `design_phrase` | `one obvious primary action` | `instruction.md` |
| `endpoint` | `/api/health` | `instruction.md` |
| `endpoint` | `/api/auth/sign-up` | `instruction.md` |
| `endpoint` | `/api/auth/login` | `instruction.md` |
| `endpoint` | `/api/entries` | `instruction.md` |
| `endpoint` | `/api/entries/{kind}/{slug}` | `instruction.md` |
| `endpoint` | `/api/entries/{id}/publish` | `instruction.md` |
| `endpoint` | `/api/entries/{id}/unpublish` | `instruction.md` |
| `endpoint` | `/api/entries/{id}/assets` | `instruction.md` |
| `endpoint` | `/api/entries/{entry_id}/assets/{asset_id}/content` | `instruction.md` |
| `endpoint` | `/api/renditions/{kind}/{slug}` | `instruction.md` |
| `endpoint` | `/api/renditions` | `instruction.md` |
| `endpoint` | `/api/plans` | `instruction.md` |
| `endpoint` | `/api/leaderboard` | `instruction.md` |
| `endpoint` | `/api/glossary/graph` | `instruction.md` |
| `endpoint` | `/api/compliance` | `instruction.md` |
| `endpoint` | `/api/applications` | `instruction.md` |
| `endpoint` | `/api/applications/{id}/instances` | `instruction.md` |
| `endpoint` | `/api/instances/{id}` | `instruction.md` |
| `endpoint` | `/api/startup-applications` | `instruction.md` |
| `endpoint` | `/api/consent` | `instruction.md` |
| `endpoint` | `/api/search` | `instruction.md` |
| `endpoint` | `access_token` | `instruction.md`, `conftest.py` |
| `env_var` | `DB_ADMIN_URL` (verifier-only) | `task.toml` |
| `env_var` | `DATABASE_URL` | `instruction.md` |
| `env_var` | `STORAGE_ENDPOINT` | `instruction.md` |
| `env_var` | `STORAGE_BUCKET` | `instruction.md` |
| `env_var` | `STORAGE_ACCESS_KEY` | `instruction.md` |
| `env_var` | `STORAGE_SECRET_KEY` | `instruction.md` |
| `env_var` | `APP_PUBLIC_URL` | `instruction.md` |
| `env_var` | `APP_PUBLIC_PORT` | `instruction.md` |
| `motion_moment` | `fans and settles` | `instruction.md` |
| `motion_moment` | `one character at a time` | `instruction.md` |
| `motion_moment` | `one slow heartbeat` | `instruction.md` |
| `motion_moment` | `rolls rather than being replaced` | `instruction.md` |
| `motion_moment` | `draws itself outward` | `instruction.md` |
| `motion_moment` | `blinking block cursor` | `instruction.md` |
| `motion_moment` | `slow float` | `instruction.md` |
| `motion_moment` | `cross-fade in place` | `instruction.md` |
| `motion_moment` | `Fast to answer, slow to forget` | `instruction.md` |
| `number` | `50,000` | `instruction.md` |
| `number` | `100` | `instruction.md` |
| `number` | `$20` | `instruction.md` |
| `number` | `$250` | `instruction.md` |
| `number` | `$9` | `instruction.md` |
| `number` | `$19` | `instruction.md` |
| `number` | `$0.02` | `instruction.md` |
| `number` | `$75` | `instruction.md` |
| `number` | `$10` | `instruction.md` |
| `number` | `1,000` | `instruction.md` |
| `number` | `100,000` | `instruction.md` |
| `number` | `$0.001` | `instruction.md` |
| `number` | `$0.00001` | `instruction.md` |
| `number` | `2,500` | `instruction.md` |
| `number` | `$100` | `instruction.md` |
| `number` | `$85` | `instruction.md` |
| `number` | `$105M` | `instruction.md` |
| `number` | `2019` | `instruction.md` |
| `number` | `15K+` | `instruction.md` |
| `number` | `53%` | `instruction.md` |
| `number` | `99.9%` | `instruction.md` |
| `number` | `99.99%` | `instruction.md` |
| `number` | `$50 million` | `instruction.md` |
| `number` | `$5 million` | `instruction.md` |
| `number` | `4.5 to 1` | `instruction.md` |
| `number` | `3 to 1` | `instruction.md` |
| `number` | `12 to 1` | `instruction.md` |
| `route` | `/` | `instruction.md` |
| `route` | `/user-authentication` | `instruction.md` |
| `route` | `/multi-tenancy` | `instruction.md` |
| `route` | `/billing` | `instruction.md` |
| `route` | `/react-authentication` | `instruction.md` |
| `route` | `/nextjs-authentication` | `instruction.md` |
| `route` | `/expo-authentication` | `instruction.md` |
| `route` | `/agents` | `instruction.md` |
| `route` | `/cli` | `instruction.md` |
| `route` | `/pricing` | `instruction.md` |
| `route` | `/docs` | `instruction.md` |
| `route` | `/changelog` | `instruction.md` |
| `route` | `/glossary` | `instruction.md` |
| `route` | `/llm-leaderboard` | `instruction.md` |
| `route` | `/components/theme-editor` | `instruction.md` |
| `route` | `/blog` | `instruction.md` |
| `route` | `/company` | `instruction.md` |
| `route` | `/careers` | `instruction.md` |
| `route` | `/startups` | `instruction.md` |
| `route` | `/security` | `instruction.md` |
| `route` | `/contact` | `instruction.md` |
| `route` | `/brand-assets` | `instruction.md` |
| `route` | `/legal` | `instruction.md` |
| `route` | `/legal/privacy` | `instruction.md` |
| `route` | `/legal/standard-terms` | `instruction.md` |
| `route` | `/legal/website-terms` | `instruction.md` |
| `route` | `/discord` | `instruction.md` |
| `route` | `/sign-in` | `instruction.md` |
| `route` | `/sign-up` | `instruction.md` |
| `route` | `/dashboard` | `instruction.md` |
| `route` | `/studio/library` | `instruction.md` |
| `route` | `/r/index.txt` | `instruction.md` |
| `scheme` | `data-band` | `instruction.md` |
| `scheme` | `data-sdk` | `instruction.md` |
| `scheme` | `data-entry-state` | `instruction.md` |
| `scheme` | `data-cell-band` | `instruction.md` |
| `scheme` | `data-plan` | `instruction.md` |
| `scheme` | `data-billing-period` | `instruction.md` |
| `scheme` | `data-theme-mode` | `instruction.md` |
| `scheme` | `data-consent` | `instruction.md` |
| `scheme` | `data-instance-state` | `instruction.md` |
| `scheme` | `data-glossary-letter` | `instruction.md` |
| `scheme` | `data-letter-state` | `instruction.md` |
| `scheme` | `bottom-decile` | `instruction.md` |
| `scheme` | `undecided` | `instruction.md` |
| `scheme` | `ruby-rails-sinatra` | `instruction.md` |
| `scheme` | `library/{entry_id}/{sha256_of_bytes}.{ext}` | `instruction.md` |
| `seed_record` | `Ada Renn` | `instruction.md` |
| `seed_record` | `Milo Vance` | `instruction.md` |
| `seed_record` | `Priya Shah` | `instruction.md` |
| `seed_record` | `Taskflow` | `instruction.md` |
| `seed_record` | `session-management` | `instruction.md` |
| `seed_record` | `Rotating a signing key without downtime` | `instruction.md` |
| `seed_record` | `Customize the reverification window` | `instruction.md` |
| `seed_record` | `Audit Dashboard activity with Admin Logs` | `instruction.md` |
| `seed_record` | `Custom OAuth scopes` | `instruction.md` |
| `seed_record` | `Adding Aegis auth to your CLI` | `instruction.md` |
| `seed_record` | `Going to production with Aegis Deploy` | `instruction.md` |
| `seed_record` | `Aegis Init: The fastest way to start a new project` | `instruction.md` |
| `seed_record` | `Aug 28` | `instruction.md` |
| `seed_record` | `Aug 25` | `instruction.md` |
| `seed_record` | `Aug 21` | `instruction.md` |
| `seed_record` | `Jun 4, 2026` | `instruction.md` |
| `seed_record` | `May 29, 2026` | `instruction.md` |
| `seed_record` | `May 11, 2026` | `instruction.md` |
| `seed_record` | `Default` | `instruction.md` |
| `seed_record` | `Dark` | `instruction.md` |
| `seed_record` | `Simple` | `instruction.md` |
| `seed_record` | `Library` | `instruction.md` |
| `seed_record` | `SOC 2 Type 2` | `instruction.md` |
| `seed_record` | `HIPAA` | `instruction.md` |
| `seed_record` | `GDPR / Data Privacy Framework` | `instruction.md` |
| `seed_record` | `CCPA` | `instruction.md` |
| `seed_record` | `PCI DSS` | `instruction.md` |
| `seed_record` | `Regional data residency` | `instruction.md` |
| `seed_record` | `Access Control List (ACL)` | `instruction.md` |
| `seed_record` | `Authenticator Apps (TOTP)` | `instruction.md` |
| `seed_record` | `Skip to main content` | `instruction.md` |
| `seed_record` | `Build with agents` | `instruction.md` |
| `seed_record` | `Aegis raises $50m Series C` | `instruction.md` |
| `seed_record` | `Sorry, we can't find the page you're looking for.` | `instruction.md` |
| `seed_record` | `Go to homepage` | `instruction.md` |
| `seed_record` | `Copied!` | `instruction.md` |
| `seed_record` | `We don't have any open positions at the moment.` | `instruction.md` |
| `seed_record` | `Thanks for joining the waitlist` | `instruction.md` |
| `seed_record` | `Trusted by fast-growing companies around the world.` | `instruction.md` |
| `seed_record` | `Secured by Aegis` | `instruction.md` |
| `seed_record` | `Search documentation` | `instruction.md` |
| `seed_record` | `Select your SDK` | `instruction.md` |
| `seed_record` | `Start building for free` | `instruction.md` |
| `seed_record` | `Talk to sales` | `instruction.md` |
| `seed_record` | `Got it` | `instruction.md` |
| `seed_record` | `Copy URL` | `instruction.md` |
| `seed_record` | `Copy CSS` | `instruction.md` |
| `seed_record` | `Reset to default` | `instruction.md` |
| `seed_record` | `Subscribe to RSS` | `instruction.md` |
| `seed_record` | `Explore all components` | `instruction.md` |
| `seed_record` | `Join our team` | `instruction.md` |
| `status` | `draft` | `instruction.md` |
| `status` | `published` | `instruction.md` |
| `status` | `pending` | `instruction.md` |
| `status` | `provisioning` | `instruction.md` |
| `status` | `live` | `instruction.md` |
| `status` | `failed` | `instruction.md` |
| `status` | `received` | `instruction.md` |
| `status` | `refused` | `instruction.md` |
| `status` | `Held` | `instruction.md` |
| `status` | `Not applicable` | `instruction.md` |
| `status` | `Not offered` | `instruction.md` |
| `status` | `Core 3` | `instruction.md` |
| `status` | `Core 2` | `instruction.md` |
| `status` | `Core 1` | `instruction.md` |

## spec/ documents

Authored at `_spec/S_saasm_cont_identity-platform-marketing-vb_20260916_062443/`, outside the bundle (CON-5).

| Document | Fed |
|---|---|
| `00-decisions.md` | the audit trail, the draws, and the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing: `## Build plan` is not baseline and this variant does not request it |

## Kit gate log

Rendered from the receipts, one row per gate.

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

## Certification prompt receipts

| Prompt | Gate | Verdict | Checks answered | Attestation |
|---|---|---|---|---|
| `QC_instruction.md` | `G34` | PASS | 24 | self |
| `QC_spec.md` | `G34` | PASS | 15 | self |
| `qc_docker.md` | `G35` | PASS | 105 | self |
| `qc_rubric.md` | `G53` | PASS | 16 | self |
| `qc_solution_checklist.md` | `G37` | PASS | 0 | self |
| `qc_toml.md` | `G36` | PASS | 120 | self |
| `task_code_verifier.md` | `G3` | VALID | 12 | self |

Every one is SELF-ATTESTED: a single agent authored and reviewed, so the kit's owner-is-not-verifier
rule is not satisfied. These are recorded verdicts, never independent ones. The six generator prompts
carry no receipt and report UNCITED, which is advisory.

## Budget estimate

`turns_expected = 200`, `tokens_expected = 7500000`. Ten must-have features at the companion-backed
ceiling, 28 routes, two interactive routes and a content pipeline put this at the top rung of the
documented band rather than the middle. `difficulty` stays the mandated calibration placeholder, so
the band is read off the scope rather than off a declared value.

## Blocking findings

None for the mechanical battery. Two things are unresolved and are the operator's:

- `[delivery]` is absent. It is grandfathered, and filling it needs the `@sha256:` digests of
  `python:3.12-slim-bookworm`, `postgres:16.4-bookworm` and
  `minio/minio:RELEASE.2024-10-13T13-34-11Z`, which cannot be resolved without a registry.
- No reference application exists. The bundle carries a brief, a checklist, an answer key and a
  grading layer, and `solution/solve.sh` exits non-zero saying so.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`. Not admissible.
