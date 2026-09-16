# Build report: S_conte_cont_creative-collective-showcase-vb_20260916_053714

## Identity

| Field | Value |
|---|---|
| Task code | `S_conte_cont_creative-collective-showcase-vb_20260916_053714` |
| Task id | `deku/creative-collective-showcase-vb` |
| Cell | solo_founder / content-publishing / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | `backend` = postgres, `storage` = minio |
| Variant | `b`, axes `critical_depth`, `data_shape` |
| Language | python (Django + server templates, HTMX) |
| Design direction | `companion` (reference/L L.6.1; the drawn `glass-depth` is recorded, not applied) |
| Launch surface | cookie_choice, form_validation, mobile_viewport, sitemap_robots, spam_protection |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 (single-operator run) |
| Companion | `prd/monopo_prd.md`, 2,046 lines |

## Feature resolution

| Candidate | Verdict | Lands in | Reason |
|---|---|---|---|
| The public showcase shell (5 content routes + 3 authored stubs) | INCLUDED | instruction.md `## Core features`, `## User flow` | companion 2.1, 2.2, 2.3 |
| WebGL fluid-gradient hero, grain, glass lens, still fallback | INCLUDED | `## Core features` rules 9-11, `## Front-end specification` | companion 8.1-8.6 |
| Scroll-pinned recent-work reel | INCLUDED | `## Core features` rules 12-14 | companion 9.2, 9.3 |
| Filterable work index, eight closed-set disciplines | INCLUDED | `## Core features` rules 15-20 | companion 10.1-10.5 |
| Press timeline, derived counts, 3D series collage | INCLUDED | `## Core features` rules 21-24 | companion 11.1-11.6 |
| Team story, member grid, founding chapters | INCLUDED | `## Core features` rules 25-28 | companion 12.1-12.5 |
| Custom not-found route | INCLUDED | `## Core features` rule 29 | companion 13; also launch-surface overlap |
| Enquiry write path with validation and bot refusal | INCLUDED | `## Core features` rules 30-33 | companion 18.4; drawn form_validation + spam_protection |
| Cookie choice and local page-view record | INCLUDED | `## Core features` rules 34-36 | companion 5.7, 18.5; drawn cookie_choice |
| Studio console: 3-step wizard, uploads, publish state | INCLUDED | `## Core features` rules 37-41 | the pattern's author role; companion silent on authoring |
| Protected boundary: draft cover and press kit | INCLUDED | `## Core features` rules 42-45 | pattern critical focus, stepped up at variant b |
| Sitemap and robots | INCLUDED | `## Core features` rules 46-47 | drawn sitemap_robots |
| Headless CMS as the content source | DROPPED | - | companion 18.1 marks it out of scope; the app owns its own store |
| `mailto:` contact affordance | DROPPED | `## Core features` rule 30 takes the form endpoint | companion 18.4 offers either; a mailto is unobservable from outside the browser |
| Captured component tree and CSS class names | DROPPED | - | companion 14 and 7.2 are artefacts of the captured build, not obligations; recorded as G51 waivers |
| Measured scroll extents | DROPPED | - | companion 7.3 states they are viewport-dependent, not layout constants |
| Audio toggle | DROPPED | - | named once in companion 5 with no specified behaviour; the shared media control carries the observable half |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | postgres | MET | `test_seed_rows_are_not_duplicated` counts seeded rows through the admin DSN; G32 green |
| `storage` | minio | MET | `test_cover_upload_is_stored_in_the_bucket`, `test_press_kit_upload_is_stored_in_the_bucket`, `test_bucket_is_not_publicly_readable` observe real objects; G32 green |

## Grading surface

- Workflows: **16** (solo_founder band 10-16)
- Browser substeps: **50** - pytest substeps: **50** - critical substeps: **9**
- Non-happy-path workflow ids: `invalid_enquiry_is_refused`, `draft_project_cannot_be_reached_by_the_public`, `protected_objects_are_denied_to_the_unentitled`, `reader_is_denied_the_studio_console`
- One pytest module, `tests/test_pytest.py`, **50** test functions covering core features, authorization, data integrity, edge cases and the storage slot
- Checklist items: **188**, every one cited by a grader (G24 green)
- Rubric criteria: **18** (18 positive, 0 negative)

| Dimension | Positive share | Target | Within 0.10 |
|---|---|---|---|
| `instruction_following` | 0.310 | 0.30 | yes |
| `functionality` | 0.238 | 0.25 | yes |
| `ux_flow` | 0.143 | 0.15 | yes |
| `ui_visual` | 0.167 | 0.15 | yes |
| `motion` | 0.048 | 0.05 | yes |
| `accessibility` | 0.048 | 0.05 | yes |
| `responsiveness` | 0.048 | 0.05 | yes |

## Grading window

| Section | Chars | Reference | Note |
|---|---|---|---|
| `## Core features` | 15024 | 2400 | past the judge slice |
| `## User flow` | 4170 | 1900 | past the judge slice |
| `## UI/UX notes` | 10580 | 1700 | past the judge slice |
| `## Constraints` | 922 | 800 | within |
| `## User roles` | 1854 | 1000 | within |
| `## Overview` | 2008 | 700 | within |
| joined six | 34558 | 8,800 | past the 9,000 join slice |

The brief has no length limit (G33). `## Core features` runs long because the companion carries 153 topics and 211 enumerated obligations, every one of which G51 requires in the brief. The tail reaches the agent in full; it stops reaching the advisory judge, which never touches reward.

## Literals ledger

| Class | Count | Values |
|---|---|---|
| `account` | 2 | `author@example.com`, `reader@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `design_phrase` | 7 | `eased`, `spacious`, `near-black cool neutral`, `deep, soft teal`, `hairline ring`, `three stacking bands`, `full-bleed` |
| `endpoint` | 17 | `/api/health`, `/api/auth/signup`, `/api/auth/login`, `/api/projects`, `/api/press/categories`, `/api/press`, `/api/series`, `/api/team` ... (17 total) |
| `env_var` | 8 | `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `DB_ADMIN_URL` |
| `motion_moment` | 5 | `house reveal`, `delayed entrance`, `link underline settle`, `route veil`, `icon settle` |
| `number` | 7 | `11 members`, `News [2]`, `Events [2]`, `Features [3]`, `Articles [0]`, `4173`, `60` |
| `route` | 16 | `/work`, `/press`, `/team`, `/services`, `/contact`, `/privacy`, `/sitemap.xml`, `/robots.txt` ... (16 total) |
| `scheme` | 5 | `projects/{project_id}/{sha256_of_bytes}.{ext}`, `press-kits/{project_id}/{sha256_of_bytes}.{ext}`, `team/{member_id}/{sha256_of_bytes}.{ext}`, `company_website`, `Authorization: Bearer` |
| `seed_record` | 27 | `HANWA RUNNER ‣ HARBOUR CAFE - POP-UP`, `NKALA COFFEE ‣ BRAND IDENTITY`, `FELDGREN x MEADOW & MOSS ‣ WINTER ACTIVATION`, `SEABRIGHT ‣ KOREAN FRIED CHICKEN ‣ BRANDING`, `RONIX ASTROX 88 ‣ Launch Campaign`, `PARIS WORLD CHAMPIONSHIPS ‣ RONIX PLAYERS LOUNGE`, `HANWA RUNNER ‣ FINISH LINE CAFE - POP-UP`, `QUEST PORTAL ‣ BRAND UNIVERSE` ... (27 total) |
| `status` | 19 | `draft`, `published`, `author`, `reader`, `footer`, `press`, `SPATIAL`, `Campaign` ... (19 total) |

Every one of the 114 literals carries its carriers and its `verifier_only` flag; `DB_ADMIN_URL` is the single verifier-only value and appears in `task.toml` `[verifier].env` alone (INV4). G6 green in both directions.

## Authoring spec folder

| Doc | Feeds |
|---|---|
| `00-decisions.md` | every draw, the variant rationale, the companion carry table, the G51 waiver reasons |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |

`06-implementation-plan.md` is not emitted: `## Build plan` is not part of the baseline emission, so the plan would feed no section of the brief.

## Kit gate log

Rendered from `_handoff/<code>.gates.jsonl`. Never transcribed.

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

## Prompt receipts

| Prompt | Gate | Verdict | Checks answered | Verifier |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | self |
| `QC_spec.md` | G34 | PASS | 15 | self |
| `qc_docker.md` | G35 | PASS | 105 | self |
| `qc_rubric.md` | G53 | PASS | 16 | self |
| `qc_solution_checklist.md` | G37 | PASS | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | self |
| `task_code_verifier.md` | G3 | PASS | 12 | self |

Every certification prompt was run and its scorecard recorded. **All seven are SELF-ATTESTED**: this was a single-agent run, so the kit's owner-is-not-verifier rule is not satisfied. These are recorded verdicts, never independent ones, and a reviewer should treat them as the weakest evidence in this report.

## Recorded findings from the QC passes

**`QC_instruction.md` (G34)**

- A1: `## Build plan` is absent. generate_instruction.md §2.1 removes it from the baseline emission and QC_instruction A1 predates that change; window_lint (G33) passes on the ten emitted H2s plus the unbudgeted `## Front-end specification`. Recorded rather than silently reconciled.
- B3: levers are read against variant `a`. This bundle is variant `b` (companion-backed, config/corpus-targets.yaml companion_variant). Both lever sections are present; the variant step is carried on critical_depth and data_shape, recorded in _spec/00-decisions.md.
- C4: QC_instruction C4 fails a brief for pinned type sizes and line heights. generate_instruction.md §4 'The number rule, DECIDED' (A5) requires the exact font family and the exact sizes to be carried, and source_lint (G51) enforces the same split. The newer settled rule governs; colour carries no hex anywhere.
- C5: QC_instruction C5 asks for concurrency invariants named as storage-level constraints (unique / partial-unique index). prescription_lint (G43) fails exactly that vocabulary in `## Data model`. The gate governs; every invariant is stated as an observable property instead.
- C7: `## Core features` runs past the judge's 2,500-char slice, as window_lint reports. The brief has no length limit (G33) and the companion's carriage obligation (G51) is the larger duty; the tail reaches the agent in full.

**`QC_spec.md` (G34)**

- S1: six docs are present, not seven. `06-implementation-plan.md` is not authored because `## Build plan` is not emitted at baseline (generate_instruction.md §2.1), so the plan would feed no brief section.
- S7: the 06 implementation-plan doc is absent for the reason recorded under S1; its deploy obligations are carried by `## Deployment contract` in the brief and verified verbatim by contract_lint (G4).

**`qc_docker.md` (G35)**

- CMP-011: the `main` service declares `ports`. CMP-022 and reference/C §C.6 (C12) require exactly that on `main`; the no-published-ports rule applies to the sidecars, and neither postgres nor minio publishes one.
- CMP-020: `main` carries `extra_hosts` and `ports` beyond `depends_on`, which CMP-022 mandates. The two rows disagree and the mandatory one governs.
- SEC-003: the image runs as root. No source establishes a non-root user, and the grader shares this image under environment_mode = shared.

**`qc_rubric.md` (G53)**

- RC-10: the rubric carries no negative criterion, so the defect-reading rule has nothing to judge. Every commission-shaped observation this brief licenses is already a deterministic pytest assertion, and a negative mirroring one would be a G28 channel collision.

**`qc_toml.md` (G36)**

- SCHEMA-011: `[delivery]` is not in the §11 canonical template. It is required by stage-4-task-toml.md for every new bundle and is validated by validate_task.py (G2) `lint_delivery`. The template predates the block; the gate governs.
- SCHEMA-013: section order follows the template with `[delivery]` inserted before `[[artifacts]]`, for the reason recorded under SCHEMA-011.
- SCHEMA-014: key order follows the template; `uuid_v5` sits inside `[task]` after `name`, which the template's own §11 listing places there.

## Budget

`turns_expected = 220`, `tokens_expected = 8000000`. The companion specifies ten must-have features against a baseline cap of six, a WebGL hero reconstructed from still frames, a scroll-pinned reel, a depth collage and a console behind an auth boundary, with every asset generated rather than shipped. That is the top of the documented band, and `tokens_expected` sits at the absolute ceiling qc_toml BENCH-004 allows.

## Blocking findings

None inside the kit's reach. Three standing conditions travel with the bundle:

1. **No reference app.** D20 defers it downstream; `solution/solve.sh` exits non-zero and says so.
2. **`[delivery.images]` is absent.** Digest pins need a registry pull the kit has no network for, and stage-5 forbids a fabricated digest. `validate_task.py` treats the key as optional; the packaging step must fill it from the built images.
3. **Grader pin drift.** `config/kit-config.yaml` holds `grader_version = "0.22.0"` while `vendor/grader-0.23.0/` exists and differs in every file. The kit deliberately does not flip the pin; the operator must confirm which generation `deku-verifier-base` is built from (INV5).

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the reference app lands and `harbor run -a oracle` returns `1.0` twice.

Kit: deku-green-field - vendored grader `0.22.0` - target schema `1.4` - canary policy `required`, corpus canary present in `solution/TRUTH.md` only.
