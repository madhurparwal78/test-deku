# Build report - E_sales_crud_crm-metadata-workspace-vb_20260916_063125

## Identity

| | |
|---|---|
| task code | `E_sales_crud_crm-metadata-workspace-vb_20260916_063125` |
| task id | `deku/crm-metadata-workspace-vb` |
| cell | enterprise / sales-crm / crud-catalog |
| archetype | `crm-metadata-workspace` |
| variant | `b`, axes `critical_depth`, `spec_sections` |
| service_profile | `P2-db-email` |
| providers | backend `postgres` · email `mailpit` |
| language | python (FastAPI server, SolidStart interface, ssr-islands) |
| verifier mode | `separate` (kit default as of commit 11eaf7b) |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 (no device sharding configured) |
| kit | deku-green-field, self-test green (32 checks) |
| vendored grader | 0.22.0 |
| target schema | 1.4 |
| run mode | PRD mode, `prd and input/twenty.com_run.yaml` (G64) |
| idea file | `prd and input/twenty.com_idea.yaml` |
| companion | `prd and input/twenty.com_prd_plain.md`, split by prd-generator from the authored `twenty.com_prd.md` (source site https://twenty.com/) |

## Feature resolution

| Candidate | Verdict | Lands in | Reason |
|---|---|---|---|
| Public marketing site, twelve routes plus not-found | INCLUDED | instruction.md `## Core features`, `## User flow` | the companion's Sections 2 and 7 to 12 |
| Live product mocks driven by the real components | INCLUDED | `## Core features` | companion Section 6.2; the mocks are the product |
| Halftone generator tool | INCLUDED | `## Core features` | companion Section 12; it is the asset pipeline for every plate |
| Metadata engine with dependency integrity | INCLUDED | `## Core features`, `## Data model` | companion Section 14, the graded core |
| Views engine: table, kanban, calendar | INCLUDED | `## Core features` | companion Sections 15 and 16 |
| Record page and unified timeline | INCLUDED | `## Core features` | companion Section 17 |
| Search, filters, command palette | INCLUDED | `## Core features` | companion Section 18 |
| Workflow engine | INCLUDED | `## Core features`, `## Technical requirements` | companion Section 19 |
| AI chat, scaffolding, apps | INCLUDED | `## Core features` | companion Section 20, shipped as a deterministic stub |
| Permissions, identity, audit | INCLUDED | `## Core features`, `## User roles` | companion Section 21, the second graded core |
| Import, export, keyed interface, webhooks | INCLUDED | `## Core features`, `## Deployment contract` | companion Section 22 |
| Dashboards and plan gating | INCLUDED | `## Core features` | companion Sections 23 and 24 |
| Build order and difficulty map | DROPPED | - | a build order is a work order; `## Build plan` is not emitted at baseline and difficulty is never brief content |
| Evidence gaps and substitutions | DROPPED | - | authoring-side provenance about how the source was captured; declared to G51 with --waive |
| Acceptance checklist | DISSOLVED | the rules it restates | an acceptance checklist in the brief is the exam, not the product (INV10) |
| External identity provider (auth slot) | DROPPED | - | the companion's own identity story is email plus password with a second factor, which is the kit's baseline app auth |
| Object storage slot | DROPPED | - | the build ships no binary asset at all, so nothing needs a bucket |

## Slot obligations

| Slot | Provider | State | Evidence |
|---|---|---|---|
| backend | postgres | MET | `test_seeded_companies_match_the_pinned_fixture`, `test_cell_edit_survives_a_reload`, `test_seeding_is_idempotent` read the database through `capabilities.make_backend()` |
| email | mailpit | MET | `test_workflow_email_reaches_only_the_addressed_inbox` and `test_refused_run_sends_no_email` read the inbox through `capabilities.make_inbox()`; the first is the slot's `critical` substep |

## Grading surface

| | |
|---|---|
| workflows | 23 (enterprise band 13 to 23) |
| browser substeps | 88 |
| pytest substeps | 60 |
| critical substeps | 13 |
| non-happy-path ids | 8: invalid_field_type_change_is_refused, concurrent_schema_editors_leave_one_winner, member_cannot_reach_another_members_rows, member_is_denied_schema_and_settings_writes, unauthenticated_caller_is_denied, expired_session_cannot_write, row_rule_creation_is_rejected_on_the_cheaper_plan, self_triggering_workflow_halts_at_the_limit |
| pytest module | one, `tests/test_output.py`, 60 functions |
| sections covered | core features, authorization, data integrity, edge cases, email |
| rubric criteria | 15 (13 positive, 2 negative) |
| checklist items | 328 across ten section codes |

### Rubric dimension shares (positives only)

| Dimension | Points | Share | Target | Inside 0.10 |
|---|---|---|---|---|
| `instruction_following` | 11 | 0.297 | 0.30 | yes |
| `functionality` | 8 | 0.216 | 0.25 | yes |
| `ux_flow` | 4 | 0.108 | 0.15 | yes |
| `ui_visual` | 7 | 0.189 | 0.15 | yes |
| `motion` | 3 | 0.081 | 0.05 | yes |
| `accessibility` | 3 | 0.081 | 0.05 | yes |
| `responsiveness` | 1 | 0.027 | 0.05 | yes |

## Grading window

| Section | Chars | Reference | Judge slice |
|---|---|---|---|
| `core_features` | 35550 | 2400 | past 2500 |
| `user_flow` | 5490 | 1900 | past 2500 |
| `ui_ux_notes` | 6398 | 1700 | past 2500 |
| `constraints` | 1134 | 800 | inside |
| `user_roles` | 2966 | 1000 | past 2500 |
| `overview` | 2069 | 700 | inside |
| **joined** | **53607** | 8800 | past 9000 |

Length is reported, never failed: `window_lint.py` (G33) retired the caps and the brief has no
limit. Prose past the slice reaches the agent in full and stops reaching the judge. It is
deliberate here: trimming would drop rules carried from the companion, and the judged criteria
are self-contained (reference/I I.8), so the judge does not depend on the brief.

## Literals ledger

| Class | Count | Values |
|---|---|---|
| `account` | 4 | `owner@example.com`, `admin@example.com`, `member@example.com`, `member2@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `design_phrase` | 9 | `--surface`, `--color-blue`, `--color-chalk`, `--color-charcoal`, `--color-green`, `--color-error`, `traffic dots`, `monogram tile`, `eased` |
| `env_var` | 9 | `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `DATABASE_URL`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `DB_ADMIN_URL`, `EMAIL_INBOX_API_URL` |
| `motion_moment` | 4 | `house settle`, `armed by scroll`, `confetti`, `skeleton cards` |
| `number` | 8 | `4173`, `0.0.0.0`, `55.9K`, `7.2K`, `$9`, `$19`, `$50k`, `-25%` |
| `route` | 13 | `/api/health`, `/api`, `/terms`, `/privacy-policy`, `/why-thirty`, `/halftone`, `/workspace`, `/product`, `/pricing`, `/customers`, `/partners`, `/apps`, `/releases` |
| `scheme` | 3 | `/app/USER_README.md`, `.browser_screenshots/`, `.downloads/` |
| `seed_record` | 13 | `Stage change notice`, `Sales Dashboard`, `OPP-1`, `Arcadia Labs`, `arcadialabs.ai`, `Meshwork`, `Chatterbox`, `Papertrail`, `Pixelforge`, `Codeharbor`, `Wanderstay`, `Ledgerline`, `Quartz Capital` |
| `status` | 17 | `Workflow:`, `Identified`, `Qualified`, `All Companies - 9`, `All opportunities 9`, `Identified 3`, `Qualified 1`, `Type is Customer`, `Employees > 500`, `Export selection as CSV`, `G then P`, `404: This page could not be found.`, `Idle auto-rotate is active`, `Build your Enterprise CRM at AI Speed`, `+10k others`, `(C) 2026 - Thirty`, `npx create-thirty-app` |

Two entries are `verifier_only` and carry `task.toml` as their sole carrier: `DB_ADMIN_URL` and
`EMAIL_INBOX_API_URL`. Neither appears in `instruction.md` or in `[environment].env` (INV4,
checked by G6 and G17).

## Spec folder

Authoring-side at `Output/16sep/_spec/E_sales_crud_crm-metadata-workspace-vb_20260916_063125/`, excluded from the bundle (CON-5).

| Doc | Feeds |
|---|---|
| `00-decisions.md` | the eight `draw:` lines G49 reads, the companion carry table, every residual judgment call |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements`, and the base image S5 derived |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing in the brief: `## Build plan` is not emitted at baseline |

## Kit gate log

Rendered from `_handoff/E_sales_crud_crm-metadata-workspace-vb_20260916_063125.gates.jsonl`. Not transcribed.

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

## Blocking findings

**None.** Every gate in batteries 1 and 2 is green on this kit, at this location, with no
environment override. Three notes that are states rather than defects:

1. **G59/G60 NOT-APPLICABLE, and it is the only reachable state.** Commit 1b99060 added
   `code_quality` to the AUTHORED code-quality dimensions, but `tests/rubric.json` is
   GENERATED and the vendored recompute.py at the 0.22.0 pin accepts only the seven
   product dimensions. A source-target criterion would stop the generator, and adding one
   by hand is what G48's regeneration check exists to catch. `revalidate.py` carries
   G59/G60 in NA_LEGAL for exactly this reason. It becomes authorable when a grader pin
   renders the source half.
2. **G40 WARN, SELF-ATTESTED.** All seven certification prompts carry a current,
   bundle-bound receipt with the full scorecard their own registries declare, but owner
   and verifier were the same agent. An independent reviewer re-running the seven prompts
   is what turns these into independent verdicts. Six advisory generator prompts are
   UNCITED and are recorded as such rather than claimed.
3. **G51 takes its waiver on the command line here.** The bundle records the one dropped
   topic in `_handoff/<project>.sources.json`, but only `tools/run_lint.py` teaches
   `revalidate.py` to read it, and that tool arrives in commit 066e565 which this kit does
   not carry. Until then a sweep passes
   `--waive "Evidence gaps and substitutions"`. The recorded file is already in the shape
   that commit expects, so nothing needs re-recording when it lands.

## Corpus layout

CON-1 requires `Output/` to be a SIBLING of the generation kit. The repository had
`deku-green-field` directly under its root, so `tools/../..` resolved to the repository
itself and every bundle under `Output/` read as generated data inside the kit tree. The kit
was moved one level down to `genkit/deku-green-field`, which is the layout CON-1 documents
(`<root>/<generation-kit>/deku-green-field/`), and `config/kit-config.yaml` now pins
`output_root` to the corpus directory. The corpus did not move: it is still at
`Output/16sep/`, the location the task order fixed. The three sibling bundles in that
directory cleared the same finding at the same time.

## Budget

`turns_expected = 200`, `tokens_expected = 8000000`: the expert extrapolation of the documented
band. The reasoning is the surface, not a guess. Twelve public routes plus thirteen workspace
routes, a metadata engine whose every mutation must enumerate its dependents, three view
renderers over one view model, a durable workflow runner, one permission authority that eight
read paths must share, a CSV import with an undo, and a rendering tool that produces the site's
own illustrations at build time. `difficulty` stays empty: calibration owns it, never the kit.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

Not admissible. The bundle carries no reference app (D20). Nothing counts toward corpus targets
until the app lands downstream and `harbor run -a oracle` returns `1.0` twice.
