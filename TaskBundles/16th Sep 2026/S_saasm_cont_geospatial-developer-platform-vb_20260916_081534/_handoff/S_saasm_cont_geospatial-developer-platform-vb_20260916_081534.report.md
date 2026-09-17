# Build report - S_saasm_cont_geospatial-developer-platform-vb_20260916_081534

## Identity

| | |
|---|---|
| task code | `S_saasm_cont_geospatial-developer-platform-vb_20260916_081534` |
| task id | `deku/geospatial-developer-platform-vb` |
| cell | solo_founder / saas-micro-tools / content-publishing |
| archetype | `geospatial-developer-platform` |
| variant | `b`, axes `critical_depth`, `spec_sections` |
| service_profile | `P4-db-storage` |
| providers | backend `postgres` · storage `minio` |
| language | typescript (Fastify server, Preact interface bundled by Vite, spa-json-api) |
| verifier mode | `separate` (kit default as of commit 11eaf7b) |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 (no device sharding configured) |
| kit | deku-green-field, self-test green (32 checks) |
| vendored grader | 0.22.0 |
| target schema | 1.4 |
| companion | `prd and input/mapbox_prd.md` (source site https://mapbox.com) |

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
| backend | postgres | MET | `test_records_live_in_postgres` is the slot's `critical` substep, with `test_seeded_rows_match_the_fixture` and `test_seeding_is_idempotent` beside it, all reading through `capabilities.make_backend()` |
| storage | minio | MET | `test_upload_bytes_land_in_the_bucket_at_the_pinned_key` and `test_private_tile_is_not_anonymously_readable_in_the_bucket` read the bucket through `capabilities.make_store()`; the first is the slot's `critical` substep |

## Grading surface

| | |
|---|---|
| workflows | 16 (solo_founder band 10 to 16) |
| browser substeps | 60 |
| pytest substeps | 52 |
| critical substeps | 8 |
| non-happy-path ids | 5: duplicate_signup_is_refused, private_tileset_cannot_be_read_before_publishing, concurrent_edits_to_one_path_leave_one_winner, reader_is_denied_every_studio_surface, bounded_service_refuses_past_its_limit |
| pytest module | one, `tests/test_output.py`, 52 functions |
| sections covered | core features, authorization, data integrity, edge cases, storage |
| rubric criteria | 17 (15 positive, 2 negative) |
| checklist items | 294 across ten section codes |

### Rubric dimension shares (positives only)

| Dimension | Points | Share | Target | Inside 0.10 |
|---|---|---|---|---|
| `instruction_following` | 11 | 0.282 | 0.30 | yes |
| `functionality` | 8 | 0.205 | 0.25 | yes |
| `ux_flow` | 4 | 0.103 | 0.15 | yes |
| `ui_visual` | 9 | 0.231 | 0.15 | yes |
| `motion` | 3 | 0.077 | 0.05 | yes |
| `accessibility` | 3 | 0.077 | 0.05 | yes |
| `responsiveness` | 1 | 0.026 | 0.05 | yes |

## Grading window

| Section | Chars | Reference | Judge slice |
|---|---|---|---|
| `core_features` | 22120 | 2400 | past 2500 |
| `user_flow` | 4471 | 1900 | past 2500 |
| `ui_ux_notes` | 6624 | 1700 | past 2500 |
| `constraints` | 1126 | 800 | inside |
| `user_roles` | 2217 | 1000 | inside |
| `overview` | 2009 | 700 | inside |
| **joined** | **38567** | 8800 | past 9000 |

Length is reported, never failed: `window_lint.py` (G33) retired the caps and the brief has no
limit. Prose past the slice reaches the agent in full and stops reaching the judge. It is
deliberate here: trimming would drop rules carried from the companion, and the judged criteria
are self-contained (reference/I I.8), so the judge does not depend on the brief.

## Literals ledger

| Class | Count | Values |
|---|---|---|
| `account` | 3 | `author@example.com`, `author2@example.com`, `reader@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `design_phrase` | 5 | `near-black`, `mid, vivid blue`, `light, vivid cyan`, `light, vivid indigo`, `cool neutral ladder` |
| `env_var` | 8 | `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`, `DB_ADMIN_URL` |
| `motion_moment` | 5 | `house easing`, `expanding ripple`, `letter by letter`, `glides sideways`, `shimmer` |
| `number` | 2 | `4173`, `0.0.0.0` |
| `route` | 15 | `/api/health`, `/api`, `/ev`, `/mts`, `/ja`, `/studio`, `/signup`, `/login`, `/blog`, `/pricing`, `/contact`, `/dei`, `/esg`, `/v2`, `/g/d` |
| `scheme` | 4 | `/app/USER_README.md`, `.browser_screenshots/`, `.downloads/`, `uploads/{upload_id}/{sha256_of_bytes}.{ext}` |
| `seed_record` | 3 | `Harbor Basemap`, `Globe View`, `Data Overlay (2D)` |
| `status` | 31 | `queued`, `processing`, `complete`, `failed`, `private`, `public`, `address`, `place`, `poi`, `region`, `driving`, `walking`, `cycling`, `driving-traffic`, `Do more with maps & navigation`, `Explore Geoform live`, `Flexibility and control you can trust`, `BUILD with Geoform`, `SUBSCRIBE`, `HIRING`, `Ready to get started?`, `Geoform for EV`, `Page Not Found`, `Rotating 3D globe`, `Live seismic event heatmap`, `Dawn`, `Day`, `Dusk`, `Night`, `Default`, `Faded` |

Two entries are `verifier_only` and carry `task.toml` as their sole carrier: `DB_ADMIN_URL` and
`EMAIL_INBOX_API_URL`. Neither appears in `instruction.md` or in `[environment].env` (INV4,
checked by G6 and G17).

## Spec folder

Authoring-side at `Output/16sep/_spec/S_saasm_cont_geospatial-developer-platform-vb_20260916_081534/`, excluded from the bundle (CON-5).

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

Rendered from `_handoff/S_saasm_cont_geospatial-developer-platform-vb_20260916_081534.gates.jsonl`. Not transcribed.

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
