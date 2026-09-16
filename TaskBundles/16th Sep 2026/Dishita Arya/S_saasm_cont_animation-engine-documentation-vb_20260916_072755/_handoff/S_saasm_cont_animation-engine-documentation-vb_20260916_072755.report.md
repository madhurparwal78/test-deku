# Build report -- S_saasm_cont_animation-engine-documentation-vb_20260916_072755

Rendered from `_handoff/S_saasm_cont_animation-engine-documentation-vb_20260916_072755.gates.jsonl` and `_handoff/S_saasm_cont_animation-engine-documentation-vb_20260916_072755.receipts.json`. No verdict on this page was typed by hand.

## Identity

| | |
|---|---|
| Task code | `S_saasm_cont_animation-engine-documentation-vb_20260916_072755` |
| Task id | `deku/animation-engine-documentation-vb` |
| Cell | solo_founder / saas-micro-tools / content-publishing |
| Service profile | `P4-db-storage` -- slots `db`, `storage` |
| Providers | backend `postgres`, storage `minio` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `python` |
| Rendering model | `ssr-islands`, overriding the raw draw `spa-json-api` |
| Stack | FastAPI behind SvelteKit, one origin, one port |
| Design direction | `companion` |
| Launch surface | colour_contrast, cookie_choice, no_broken_links, privacy_page, spam_protection |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Companion | `prds/animejs_prd.md` |
| Kit | deku-green-field, grader pin `0.22.0`, schema `1.4` |

## Gate log

One row per gate, exactly as the receipt records it.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS |
| G1/G12 | `layout_lint.py` | 0 | PASS |
| G46 | `structure_lint.py` | 1 | FAIL |
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
| G47 | `output_qc.py` | 1 | FAIL |

32 gates recorded, 2 red.

### Red gates

- **G46** (`structure_lint.py`) exit 1.
- **G47** (`output_qc.py`) exit 1.

G46 is an operator-configuration red, not a bundle defect: `output_root` in `config/kit-config.yaml` points inside the tree that holds the kit, and CON-1 requires a sibling. G47 is red only because it reads G46's row. The remedy is in the handoff contract and changes nothing inside the bundle.

## Certification receipts

| Prompt | Gate | Scope | Checks | Verdict | Verifier |
|---|---|---|---|---|---|
| `QC_instruction.md` | G34 | HARD | 24 | PASS | self |
| `QC_spec.md` | G34 | HARD | 15 | PASS | self |
| `docker_generator.md` | S5 | advisory | 0 | PASS | self |
| `generate_instruction.md` | S2 | advisory | 0 | PASS | self |
| `pytest_generator.md` | S7 | advisory | 0 | PASS | self |
| `qc_docker.md` | G35 | HARD | 105 | PASS | self |
| `qc_rubric.md` | G53 | HARD | 16 | PASS | self |
| `qc_solution_checklist.md` | G37 | HARD | 0 | PASS | self |
| `qc_toml.md` | G36 | HARD | 120 | PASS | self |
| `rubric_author.md` | S8 | advisory | 0 | PASS | self |
| `solution_checklist.md` | S3 | advisory | 0 | PASS | self |
| `task_code_verifier.md` | G3 | HARD | 12 | VALID | self |
| `toml_generator.md` | S4 | advisory | 0 | PASS | self |

292 declared checks answered, 10 recorded WARN. Every WARN names the rule the check contradicts; none is a softened failure. Every verdict is SELF-ATTESTED: one agent authored and certified, which the kit records rather than counts as independent.

## Feature resolution

| Feature | Verdict | Where it landed |
|---|---|---|
| The scroll-driven tour | INCLUDED | `## Core features`, `## Front-end specification` |
| The instrument and its four degradation states | INCLUDED | `## Core features`, `## Front-end specification` |
| Versioned documentation and its three-column shell | INCLUDED | `## Core features`, `## Data model` |
| A documentation page and the whole-tree pager | INCLUDED | `## Core features`, `## Data model` |
| Documentation search over a per-version index artifact | INCLUDED | `## Core features`, `## Technical requirements` |
| The browser-only curve editor | INCLUDED | `## Core features`, `## Front-end specification` |
| The subscription lifecycle | INCLUDED | `## Core features`, `## Data model` |
| Funding, sponsorship and the advertising slot | INCLUDED | `## Core features`, `## Data model` |
| The content pipeline and its nine publish checks | INCLUDED | `## Core features` |
| Background work and the watched signals | INCLUDED | `## Core features`, `## Technical requirements` |
| The companion's build order (its section 34) | DROPPED | a work order rather than a specification; `## Build plan` is not emitted at variant b, and its one product decision, the ring before the scene, is carried into `## Core features` |
| The reference's evidence tiers and capture conditions | DROPPED | properties of the companion's own capture process, waived on the record in the G51 waiver file |
| The reference's CSS token names, hexes and millisecond values | DROPPED | carried as family, tone and shade, and as motion character; `source_lint.py` A5 forbids a value anywhere in the brief |

## Slot obligations

| Slot | Provider | Verdict | Critical substep |
|---|---|---|---|
| db | postgres | MET | `test_seeded_pages_carry_a_gapless_flattened_sequence`, `test_a_second_current_version_is_refused_by_the_database` |
| storage | minio | MET | `test_search_index_is_a_real_object_in_the_bucket_at_its_key`, `test_sponsor_marks_and_the_roster_document_are_first_party_objects` |

## Grading channels

| | |
|---|---|
| Workflows | 16 |
| Substeps | 174 (90 pytest, 84 browser) |
| Critical substeps | 37 |
| Non-happy-path workflow ids | 5: tour_survives_a_scene_that_cannot_run, subscription_form_is_no_oracle_and_machine_submissions_are_rejected, unauthenticated_studio_and_draft_reads_are_denied, publish_with_a_broken_internal_link_is_refused, concurrent_scheduled_runs_and_a_runaway_sweep_are_refused |
| Pytest module | `tests/test_output.py`, 90 tests, 19 of them page-driven |
| Checklist items | 725 |
| Traceability matrix | 281 core asks, 0 not fully graded |

Category mix: business_rule 21, core_outcome 11, data_integrity 30, presentation 13, security 14, validation 1.

Checklist items by section: C-CF 383, C-CN 16, C-DC 26, C-DM 70, C-FE 81, C-OV 13, C-RL 17, C-TR 47, C-UF 30, C-UX 42.

Checklist items by tag: capability 163, constraint 172, contract 60, data 63, literal 102, role 12, ui 153.

## Rubric

35 judged criteria, 31 positive and 4 negative. Positive total 105; negative magnitude 8.

| Dimension | Points | Share | Target |
|---|---|---|---|
| instruction_following | 30 | 0.29 | 0.30 |
| functionality | 29 | 0.28 | 0.25 |
| ux_flow | 16 | 0.15 | 0.15 |
| ui_visual | 15 | 0.14 | 0.15 |
| motion | 5 | 0.05 | 0.05 |
| accessibility | 5 | 0.05 | 0.05 |
| responsiveness | 5 | 0.05 | 0.05 |

18 compiled rubric items sit in `solution/trinity/rubrics.json`, each naming a committed grader; the compiled-weight share is 1.0, above the floor.

## Literals ledger

224 pinned values, by class.

| Class | Count |
|---|---|
| account | 6 |
| credential | 1 |
| endpoint | 13 |
| env_var | 26 |
| number | 18 |
| route | 9 |
| scheme | 34 |
| seed_record | 97 |
| status | 20 |

| Value | Class | Carriers |
|---|---|---|
| `maintainer@example.com` | account | instruction.md, conftest.py |
| `Elias Marchand` | seed_record | instruction.md, conftest.py |
| `intro` | seed_record | instruction.md, conftest.py, test_output.py |
| `toolbox` | seed_record | instruction.md, conftest.py |
| `intuitive` | seed_record | instruction.md, conftest.py |
| `composition` | seed_record | instruction.md, conftest.py |
| `scroll` | seed_record | instruction.md, conftest.py, test_output.py, workflows.yaml, task.toml |
| `staggering` | seed_record | instruction.md, conftest.py |
| `svg-utilities` | seed_record | instruction.md, conftest.py |
| `draggable` | seed_record | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `clockwork` | seed_record | instruction.md, conftest.py |
| `responsive` | seed_record | instruction.md, conftest.py |
| `modules` | seed_record | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `sponsors` | seed_record | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `2` | number | instruction.md, conftest.py, test_output.py, workflows.yaml, task.toml |
| `NEW` | env_var | instruction.md, conftest.py, test_output.py |
| `remap` | seed_record | instruction.md, conftest.py, test_output.py |
| `utilities/remap-and-clamp` | seed_record | instruction.md |
| `120` | number | instruction.md, conftest.py |
| `10` | number | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `37` | number | conftest.py, workflows.yaml |
| `default` | seed_record | instruction.md, conftest.py, test_output.py |
| `snappy` | seed_record | instruction.md, conftest.py |
| `bouncy` | seed_record | instruction.md, conftest.py, test_output.py |
| `strong` | seed_record | instruction.md, conftest.py |
| `in` | seed_record | instruction.md, conftest.py, test_output.py, workflows.yaml, task.toml |
| `out` | seed_record | instruction.md, conftest.py, test_output.py, workflows.yaml, task.toml |
| `in-out` | seed_record | instruction.md, conftest.py, test_output.py |
| `out-in` | seed_record | instruction.md, conftest.py |
| `CSS` | env_var | instruction.md, conftest.py, test_output.py |
| `JS` | env_var | instruction.md, conftest.py |
| `3` | number | instruction.md, conftest.py, test_output.py, workflows.yaml, task.toml |
| `family` | seed_record | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `member` | seed_record | instruction.md, conftest.py, test_output.py |
| `p1x` | seed_record | instruction.md, conftest.py |
| `p1y` | seed_record | instruction.md, conftest.py |
| `p2x` | seed_record | instruction.md, conftest.py |
| `p2y` | seed_record | instruction.md, conftest.py |
| `bounce` | seed_record | instruction.md, conftest.py, test_output.py |
| `duration` | seed_record | instruction.md, conftest.py, workflows.yaml |
| `course_waitlist` | seed_record | instruction.md, conftest.py |
| `newsletter` | seed_record | instruction.md, conftest.py |
| `128` | number | instruction.md, conftest.py, workflows.yaml |
| `7` | number | instruction.md, conftest.py, workflows.yaml, task.toml |
| `20` | number | instruction.md, conftest.py, test_output.py, workflows.yaml, task.toml |
| `company_website` | seed_record | instruction.md, conftest.py |
| `200` | number | instruction.md, conftest.py, test_output.py, task.toml |
| `upper` | seed_record | instruction.md, conftest.py, workflows.yaml |
| `1` | number | instruction.md, conftest.py, test_output.py, workflows.yaml, task.toml |
| `lower` | seed_record | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `send_confirmation` | seed_record | instruction.md, conftest.py |
| `send_welcome` | seed_record | instruction.md, conftest.py |
| `process_mail_events` | seed_record | instruction.md, conftest.py |
| `sync_sponsor_roster` | seed_record | instruction.md, conftest.py, test_output.py |
| `sweep_expired_subscriptions` | seed_record | instruction.md, conftest.py, test_output.py |
| `expire_badges` | seed_record | instruction.md, conftest.py, test_output.py |
| `rebuild_index` | seed_record | instruction.md, conftest.py, test_output.py |
| `purge_caches` | seed_record | instruction.md, conftest.py |
| `warm_caches` | seed_record | instruction.md, conftest.py |
| `check_roster_freshness` | seed_record | instruction.md, conftest.py, test_output.py |
| `5` | number | instruction.md, conftest.py, test_output.py, workflows.yaml, task.toml |
| `500` | number | instruction.md, conftest.py, test_output.py, task.toml |
| `24` | number | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `STORAGE_BUCKET` | env_var | instruction.md, task.toml |
| `STORAGE_ACCESS_KEY` | env_var | instruction.md, task.toml |
| `STORAGE_SECRET_KEY` | env_var | instruction.md, task.toml |
| `48` | number | instruction.md, conftest.py, workflows.yaml, task.toml |
| `20000` | number | instruction.md |
| `5000` | number | instruction.md, task.toml |
| `deku-demo-pw-2026` | credential | instruction.md, conftest.py |
| `index/<version_label>/search-index.json` | scheme | instruction.md |
| `sponsors/<external_id>/mark.svg` | scheme | instruction.md |
| `posters/<version_label>/<module_slug>/<page_slug>.svg` | scheme | instruction.md |
| `roster/current.json` | scheme | instruction.md, conftest.py |
| `4.5.0` | seed_record | instruction.md, conftest.py |
| `4.4.0` | seed_record | instruction.md, conftest.py |
| `4.6.0` | seed_record | instruction.md, conftest.py |
| `pv_9f2c41be` | seed_record | instruction.md, conftest.py |
| `16` | number | instruction.md, conftest.py, workflows.yaml, task.toml |
| `getting-started` | seed_record | instruction.md, conftest.py |
| `red` | seed_record | instruction.md, conftest.py, test_output.py, workflows.yaml, task.toml |
| `utilities` | seed_record | instruction.md, conftest.py, test_output.py |
| `king` | seed_record | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `adapters` | seed_record | instruction.md, conftest.py, test_output.py |
| `purple` | seed_record | instruction.md, conftest.py |
| `text` | seed_record | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `2026-12-01` | seed_record | instruction.md, conftest.py |
| `getting-started/installation` | seed_record | instruction.md |
| `getting-started/your-first-animation` | seed_record | instruction.md |
| `timer/create-timer` | seed_record | instruction.md |
| `adapters/adapter-limits` | seed_record | instruction.md |
| `47` | number | conftest.py, workflows.yaml |
| `svg` | seed_record | instruction.md, conftest.py, test_output.py |
| `scene` | status | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `getting-started/configuration` | seed_record | instruction.md, conftest.py |
| `Ravelin` | seed_record | instruction.md, conftest.py |
| `Corvid` | seed_record | instruction.md, conftest.py |
| `2026-08-31` | seed_record | instruction.md, conftest.py |
| `confirmed@example.com` | account | instruction.md, conftest.py |
| `pending@example.com` | account | instruction.md, conftest.py |
| `expired@example.com` | account | instruction.md, conftest.py |
| `2026-09-09` | seed_record | instruction.md, conftest.py, test_output.py |
| `complained@example.com` | account | instruction.md, conftest.py |
| `complained` | status | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `unsubscribed@example.com` | account | instruction.md, conftest.py |
| `unsubscribed` | status | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `DOCS` | env_var | instruction.md, conftest.py, test_output.py |
| `EASINGS` | env_var | instruction.md, conftest.py |
| `LEARN` | env_var | instruction.md, conftest.py, test_output.py |
| `EXAMPLES` | env_var | instruction.md, conftest.py |
| `SOURCE` | env_var | instruction.md, conftest.py |
| `SPONSOR` | env_var | instruction.md, conftest.py, test_output.py |
| `Skip to content` | seed_record | instruction.md, conftest.py |
| `SPONSORS` | env_var | instruction.md, conftest.py, test_output.py |
| `SITE` | env_var | instruction.md, conftest.py |
| `SOCIALS` | env_var | instruction.md, conftest.py |
| `STAY IN TOUCH` | seed_record | instruction.md, conftest.py |
| `ads via Carbonate` | seed_record | instruction.md, conftest.py |
| `One engine for every animation.` | seed_record | instruction.md, conftest.py |
| `A small, fast library for moving anything on the web.` | seed_record | instruction.md, conftest.py |
| `npm i lumenjs` | seed_record | instruction.md, conftest.py |
| `LEARN MORE` | seed_record | instruction.md, conftest.py |
| `Start animating` | seed_record | instruction.md, conftest.py |
| `Our sponsors` | seed_record | instruction.md, conftest.py |
| `Documentation` | seed_record | instruction.md, conftest.py |
| `Upper sponsors` | seed_record | instruction.md, conftest.py |
| `Lower sponsors` | seed_record | instruction.md, conftest.py |
| `Become a sponsor` | seed_record | instruction.md, conftest.py |
| `PREVIOUS` | env_var | instruction.md, conftest.py |
| `NEXT` | env_var | instruction.md, conftest.py, test_output.py |
| `SEARCH` | env_var | instruction.md, conftest.py, test_output.py |
| `No pages match that.` | seed_record | instruction.md, conftest.py, test_output.py |
| `Search is unavailable. Use the menu on the left.` | seed_record | instruction.md, conftest.py |
| `PREVIEW` | env_var | instruction.md, conftest.py, test_output.py |
| `EXPORT` | env_var | instruction.md, conftest.py, test_output.py |
| `Copied` | seed_record | instruction.md, conftest.py |
| `Join the waiting list` | seed_record | instruction.md, conftest.py |
| `SUBSCRIBE` | env_var | instruction.md, conftest.py, test_output.py |
| `If the form fails, write to hello[at]lumenjs.example.` | seed_record | instruction.md, conftest.py |
| `Check your inbox to confirm.` | seed_record | instruction.md, conftest.py |
| `That does not look like an email address.` | seed_record | instruction.md, conftest.py |
| `Too many attempts. Try again shortly.` | seed_record | instruction.md, conftest.py |
| `You are on the list.` | seed_record | instruction.md, conftest.py |
| `Nothing here` | seed_record | instruction.md, conftest.py, test_output.py |
| `That address does not exist. Try one of these.` | seed_record | instruction.md, conftest.py |
| `Something broke` | seed_record | instruction.md, conftest.py |
| `TRY AGAIN` | seed_record | instruction.md, conftest.py |
| `Built and maintained by Elias Marchand` | seed_record | instruction.md, conftest.py |
| `In this section` | seed_record | instruction.md, conftest.py |
| `Learn how this site was built.` | seed_record | instruction.md, conftest.py |
| `/api/health` | endpoint | instruction.md, conftest.py |
| `/api/subscribe` | endpoint | instruction.md, test_output.py |
| `/api/subscribe/confirm` | endpoint | instruction.md |
| `/api/subscribe/token` | endpoint | instruction.md |
| `/api/unsubscribe` | endpoint | instruction.md |
| `/api/versions` | endpoint | instruction.md |
| `/api/sponsors` | endpoint | instruction.md |
| `/api/ad-slot` | endpoint | instruction.md |
| `/api/events` | endpoint | instruction.md |
| `/api/storage-choice` | endpoint | instruction.md |
| `/api/auth/login` | endpoint | instruction.md |
| `/api/auth/logout` | endpoint | instruction.md |
| `/api/hooks/mail` | endpoint | instruction.md |
| `/documentation` | route | instruction.md, conftest.py |
| `/easing-editor` | route | instruction.md, conftest.py |
| `/learn` | route | instruction.md, conftest.py |
| `/privacy` | route | instruction.md, conftest.py |
| `/confirm` | route | instruction.md, conftest.py |
| `/unsubscribe` | route | instruction.md, conftest.py |
| `/sitemap.xml` | route | instruction.md, conftest.py, test_output.py |
| `/studio` | route | instruction.md, conftest.py, test_output.py |
| `/login` | route | instruction.md, conftest.py, test_output.py |
| `APP_PUBLIC_URL` | env_var | instruction.md, task.toml |
| `APP_PUBLIC_PORT` | env_var | instruction.md, task.toml |
| `DATABASE_URL` | env_var | instruction.md, task.toml |
| `STORAGE_ENDPOINT` | env_var | instruction.md, task.toml |
| `data-primary-action` | scheme | instruction.md, test_output.py |
| `data-scene-state` | scheme | instruction.md, test_output.py |
| `data-current-stop` | scheme | instruction.md, test_output.py |
| `data-stop` | scheme | instruction.md, test_output.py |
| `data-module-tile` | scheme | instruction.md, test_output.py |
| `data-arc` | scheme | instruction.md, test_output.py |
| `data-arc-lit` | scheme | instruction.md, test_output.py |
| `data-tree-item` | scheme | instruction.md, test_output.py |
| `data-tree-expanded` | scheme | instruction.md, test_output.py |
| `data-demo-panel` | scheme | instruction.md, test_output.py |
| `data-demo-running` | scheme | instruction.md, test_output.py |
| `data-current` | scheme | instruction.md, test_output.py |
| `data-pager` | scheme | instruction.md, test_output.py |
| `data-search-field` | scheme | instruction.md, test_output.py |
| `data-search-result` | scheme | instruction.md, test_output.py |
| `data-version-control` | scheme | instruction.md, test_output.py |
| `data-preset-tile` | scheme | instruction.md, test_output.py |
| `data-preset-active` | scheme | instruction.md, test_output.py |
| `data-handle` | scheme | instruction.md, test_output.py |
| `data-onion-skin` | scheme | instruction.md, test_output.py |
| `data-export-block` | scheme | instruction.md, test_output.py |
| `data-copy-control` | scheme | instruction.md, test_output.py |
| `data-copy-state` | scheme | instruction.md, test_output.py |
| `data-specimen` | scheme | instruction.md, test_output.py |
| `data-sponsor-card` | scheme | instruction.md, test_output.py |
| `data-recruitment-card` | scheme | instruction.md, test_output.py |
| `data-ad-slot` | scheme | instruction.md |
| `data-storage-bar` | scheme | instruction.md, test_output.py |
| `data-storage-accept` | scheme | instruction.md, test_output.py |
| `data-storage-refuse` | scheme | instruction.md, test_output.py |
| `pending` | status | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `confirmed` | status | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `bounced` | status | instruction.md, conftest.py, test_output.py |
| `draft` | status | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `published` | status | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `archived` | status | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `queued` | status | instruction.md, conftest.py, test_output.py |
| `delivered` | status | instruction.md, conftest.py, test_output.py |
| `dead` | status | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `running` | status | instruction.md, conftest.py, test_output.py |
| `succeeded` | status | instruction.md, conftest.py, test_output.py |
| `failed` | status | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `refused` | status | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `fills` | status | instruction.md, conftest.py, test_output.py |
| `empty` | status | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `slow` | status | instruction.md, conftest.py |
| `inline` | status | instruction.md, conftest.py |
| `DB_ADMIN_URL` | env_var | task.toml |

## Spec folder

| Doc | Fed |
|---|---|
| `00-decisions.md` | the audit trail, the draws, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | recorded, not emitted: `## Build plan` is absent at variant b |

## Grading window

| Section | Chars | Reference |
|---|---|---|
| Core features | 36277 | 2400 |
| User flow | 5034 | 1900 |
| UI and UX notes | 11991 | 1700 |
| Constraints | 2465 | 800 |
| User roles | 1334 | 1000 |
| Overview | 2924 | 700 |
| Joined | 59627 | 8800 |

The brief has no length limit and G33 fails nothing on length. The judge reads the first 2,500 characters of each section and 9,000 of the join, so the graded rules are front-loaded inside `## Core features` and the detail runs on into `## Front-end specification`, which the judge never parses and the agent receives in full.

## Budget

`turns_expected` 200 and `tokens_expected` 7500000. Ten must-have features, three front ends, a nineteen-table schema and a ninety-test grading surface sit at the top of the documented band rather than above it: the absolute ceiling is 8,000,000 tokens.

## Blocking findings

- G46: the operator's `output_root` sits inside the kit's own tree. Remedy in the handoff contract; nothing inside the bundle changes.
- No reference application exists. G13, G15, G18, G19, G20, G21 and G25 are undecided and are listed with their commands in the handoff contract.

## Exit state

`MECHANICALLY-GREEN EXCEPT G46, NO-SOLUTION`. Not admissible. Nothing counts toward corpus targets until the application lands downstream and `harbor run -a oracle` returns `1.0` twice.
