# Build report - S_creato_cont_interactive-comic-studio-vb_20260916_101911

Exit state: **NOT MECHANICALLY-GREEN: G6, G24, G40, G47**. NO-SOLUTION: the bundle carries no reference app and is not admissible.

Rendered from `_handoff/S_creato_cont_interactive-comic-studio-vb_20260916_101911.gates.jsonl`. Every verdict below is copied from a receipt; none is authored here.

## Identity

| Field | Value |
|---|---|
| task code | S_creato_cont_interactive-comic-studio-vb_20260916_101911 |
| task id | deku/interactive-comic-studio-vb |
| category | solo_founder |
| domain | creator-monetization |
| pattern | content-publishing |
| archetype | interactive-comic-studio |
| service profile | P4-db-storage |
| providers per slot | backend = postgres, storage = minio |
| variant | b |
| variant axes | critical_depth, spec_sections |
| language | python |
| spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| design direction | companion |
| launch surface | cookie_choice,meta_tags,page_view_log,single_cta,spam_protection |
| grader version | 0.22.0 |
| schema version | 1.4 |
| verifier mode | separate |
| authors | kaustubh.dalvi@ethara.ai (QL), ananya.tandon.int43@ethara.ai (contributor) |
| turns / tokens expected | 170 / 7000000 |
| shard | 1 of 1 |

turns and tokens sit on the hard anchor. The qc_toml reviewer noted that the brief's scope (28 tables, about 75 endpoints, a canvas reader, a studio console) reads closer to the expert anchor; `difficulty` stays the empty string because calibration writes it, never the author.

## Inputs

- Task Order: category solo_founder, domain creator-media, pattern content-publishing, archetype interactive-comic-studio, the supplied idea, the QL and contributor addresses.
- Companion PRD: `C:/Users/Admin/Desktop/Deku/Prds/ponponmania_prd.md`, reference site https://ponpon-mania.com/Site. Variant `b` per `companion_variant`.
- `creator-media` is not in the level-2 enum; minted as `creator-monetization`, the member matching a creator publishing to an audience with tipping as its model. Recorded in `_spec/.../00-decisions.md`.

## Feature resolution table

| Candidate (from the companion) | Verdict | Where | Reason |
|---|---|---|---|
| Serialised reading model: volume, chapter, board, panel, layer | INCLUDED | Overview, Data model | the idea's centre of gravity |
| Title screen, record rack, full-window scene reader | INCLUDED | Core features, Front-end specification | named by the idea |
| Scene engine: parallax layers, camera stops, text mode | INCLUDED | Core features, Front-end specification | observable reading model |
| Two languages with a full catalogue and prefix routes | INCLUDED | Core features, localisation | named by the idea |
| Reader accounts, progress sync across devices | INCLUDED | Core features, reader identity | a tip must attach to someone |
| Tipbox tips, signed webhooks, early access, refunds | INCLUDED | Core features, tips | tips unlock the next chapter early, per the idea |
| Scheduled drops published within 60 seconds | INCLUDED | Core features, release scheduling | named by the idea |
| Studio console: content, composer, translations, releases, supporters, insights, settings | INCLUDED | Core features, User flow | named by the idea |
| Texture pipeline: content tag, asset version, signed addresses | INCLUDED | Core features, Technical requirements | the storage slot |
| Consent strip, first-party measurement, server counts | INCLUDED | Core features, consent | drawn launch surface cookie_choice, page_view_log |
| Surprise easter egg | INCLUDED | Core features, delight | companion 19.x |
| Passwordless link, invitations, drop mail, mailed export | DROPPED | Constraints, 00-decisions | no email slot on P4-db-storage |
| Second factor, recovery codes, team management | DROPPED | Constraints | authors are seeded; one-request sign-in contract |
| Debug parameters | DROPPED | G51 waiver | development aids; the brief forbids them |
| Tier classification, evidence gaps | DROPPED | G51 waivers | framing for reviewers, provenance of the capture |
| Performance budgets, architecture, build order | DROPPED | G51 waivers | not observable or not emitted at variant b |
| Texture compression formats and hardware classes | DROPPED | Constraints | images are stored PNGs |

## Slot obligation table

| Slot | Provider | Critical pytest substep | Status |
|---|---|---|---|
| backend | postgres | `test_concurrent_duplicate_tip_deliveries_store_one_tip_row`, `test_concurrent_progress_writes_from_two_devices_end_in_one_merged_row` | MET |
| storage | minio | `test_imported_layer_image_is_stored_reencoded_in_bucket_at_content_hash_key` | MET |

G32 (workflow_lint) confirms both slots observed.

## Graders

- workflows: 16 (solo_founder band 10 to 16)
- browser substeps: 53; pytest substeps: 129; critical substeps: 11; browser:pytest 0.41
- substep categories: `business_rule` 31, `core_outcome` 7, `data_integrity` 21, `presentation` 38, `security` 20, `validation` 12
- non-happy-path workflow ids: 8 - `visitor_is_denied_scheduled_chapter_content`, `forged_or_duplicate_tip_notification_is_rejected`, `refunded_tip_revokes_early_access`, `reader_session_forbidden_on_studio_surface`, `invalid_translation_placeholder_is_rejected`, `declined_consent_leaves_only_functional_keys`, `duplicate_signup_and_locked_out_sign_in_rejected`, `stale_layer_edit_conflict_is_rejected`
- test module: `tests/test_output.py`, 129 test functions, grouped as seed and platform, access and reader accounts, tips, studio and release, public pages, studio pages
- rubric criteria: 14 (13 positive, 1 negative); task completion share 74%

| Dimension | Positive share | Target | Criteria |
|---|---|---|---|
| instruction_following | 0.355 | 0.30 | 3 |
| ui_visual | 0.194 | 0.15 | 5 |
| ux_flow | 0.161 | 0.15 | 3 |
| motion | 0.032 | small | 1 |
| functionality | 0.258 | 0.25 | 2 |

## Literals ledger

484 entries. Full values and carriers are in `_handoff/S_creato_cont_interactive-comic-studio-vb_20260916_101911.literals-ledger.json`.

| Class | Count | Examples |
|---|---|---|
| account | 6 | `author@example.com`, `author2@example.com`, `reader@example.com`, `reader2@example.com` |
| copy | 475 | `Camille Rouyer`, `Damien Lorca`, `Doudou Fever`, `Europe/Paris` |
| credential | 1 | `deku-demo-pw-2026` |
| route | 1 | `/api/health` |
| secret | 1 | `tbx_whsec_5f3a9c2e81d7` |

## spec/ documents

Authored outside the bundle at `Output/16sept_ponponmania/_spec/S_creato_cont_interactive-comic-studio-vb_20260916_101911/`.

| Document | Feeds |
|---|---|
| 00-decisions.md | draws, residual calls, companion carry table |
| 01-PRD.md | Overview, Core features, Constraints |
| 02-TRD.md | Technical requirements, Deployment contract |
| 03-app-flow.md | User flow, API shapes |
| 04-uiux-brief.md | UI/UX notes, Front-end specification |
| 05-backend-schema.md | Data model, User roles |
| 06-implementation-plan.md | authoring-side only; Build plan is not emitted at variant b |

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Core features | 60216 | 2400 | past-slice |
| User flow | 6774 | 1900 | past-slice |
| UI/UX notes | 7583 | 1700 | past-slice |
| Constraints | 1054 | 800 | over-reference |
| User roles | 2979 | 1000 | past-slice |
| Overview | 3024 | 700 | past-slice |
| total | 81630 | 8800 | past-slice |
| joined total | 81630 | 8800 | past-slice |
| four | 75627 | 7100 | over-reference |
| first four | 75627 | 7100 | over-reference |

G33 reports length and fails nothing on it. The tail of a long section reaches the agent in full and the judge not at all; the judged criteria carry their own self-contained evaluation rules.

## Kit gate log

| Gate | Tool | Exit | Verdict | stdout sha |
|---|---|---|---|---|
| G2/G16 | validate_task.py | 0 | PASS | `328bffb2678ff3e2` |
| G1/G12 | layout_lint.py | 0 | PASS | `4342bcbee2d22fc2` |
| G46 | structure_lint.py | 0 | PASS | `8d8c57123170e7ad` |
| G50 | docker_lint.py | 0 | PASS | `380ed7d1c830de35` |
| G55 | runtime_deps_lint.py | 0 | PASS | `a0c21dca8bc5f78a` |
| G63 | secret_lint.py | 0 | PASS | `7af90fa9e9834e79` |
| G48 | truth_lint.py | 0 | PASS | `73dfada245ec2edf` |
| G51 | source_lint.py | 0 | PASS | `2c270846a350b245` |
| G52 | rubric_context_lint.py | 0 | PASS | `c326bd8c5986b153` |
| G54 | comment_lint.py | 0 | PASS | `0d104176580b548d` |
| G17 | secret_hygiene_lint.py | 0 | PASS | `67d71492bc4dd364` |
| G11 | leak_scan.py | 0 | PASS | `367a44d168d42b24` |
| G33 | window_lint.py | 0 | PASS | `de39988c76a0939f` |
| G4/G5 | contract_lint.py | 0 | PASS | `8d679a5a090bd797` |
| G43 | prescription_lint.py | 0 | PASS | `eb7b2b6de7224b58` |
| G44 | disclosure_lint.py | 0 | PASS | `7bbe90d1e0e87a4d` |
| G10 | no_sdk_lint.py | 0 | PASS | `f2bc743948cb43eb` |
| G31 | determinism_lint.py | 0 | PASS | `f4e6e83d411799ae` |
| G14 | reward_path_lint.py | 0 | PASS | `14456cbb0082477f` |
| G27/G30 | rubric_lint.py | 0 | PASS | `b69bb38f56582682` |
| G41 | flag_lint.py | 0 | PASS | `c9aae9d3cd875fab` |
| G56/G57/G58 | if_lint.py | 0 | PASS | `cdf20c83e9056866` |
| G59/G60 | codequality_lint.py | 2 | ? | `e23941dd85e0253b` |
| G7/G8/G9/G32/G45 | workflow_lint.py | 0 | PASS | `350cfcd102ff59e0` |
| G6 | fixture_lint.py | 1 | FAIL | `6b6ff6c7814f0b8c` |
| G24 | coverage_map.py | 1 | FAIL | `0ad55e8a635da629` |
| G37 | checklist_qc.py | 0 | PASS | `3bba8d7d41595e54` |
| G39 | rubric_align_lint.py | 0 | PASS | `53b76f8d367f3d4d` |
| G28/G29 | channel_lint.py | 0 | PASS | `dedd6a8b912c374d` |
| G40 | prompt_receipt_lint.py | 1 | FAIL | `0605207caf4553e1` |
| G0/INV5 | vendor_check.py | 0 | PASS | `3c29c071d92ab31f` |
| G47 | output_qc.py | 1 | FAIL | `53dc1f1b91f21d42` |

Adversarial QC prompts, run by reviewer subagents distinct from the authoring agent, with receipts in `_handoff/S_creato_cont_interactive-comic-studio-vb_20260916_101911.receipts.json`:

| Prompt | Gate | Verdict | Verifier | History |
|---|---|---|---|---|
| task_code_verifier.md | G3 | VALID | subagent:task-code-verifier |  |
| QC_instruction.md | G34 | PASS | subagent:QC_instruction | pass 1 FAIL, pass 2 FAIL (C3, D2), pass 3 FAIL (D5), pass 4 PASS, pass 5 PASS (two consecutive clean passes); passes 4 and 5 ran past the 3-cycle fix-or-abort rule, reported in the handoff |
| QC_spec.md | G34 | PASS | subagent:QC_spec | pass 1 FAIL, pass 2 FAIL (7 checks), pass 3 FAIL (4), pass 4 FAIL (S5, S9), pass 5 FAIL (S5), pass 6 PASS; passes 4 to 6 ran past the 3-cycle fix-or-abort rule, reported in the handoff |

The G34 prompts ran past the stage's 3-cycle fix-or-abort rule: QC_instruction took 8 passes and QC_spec 8 before two consecutive clean passes on the final bytes. Each late pass followed a mechanical-gate edit or a reviewer finding, never a disputed verdict. That overrun is reported here, not hidden.

## Blocking findings

**G24 coverage is RED on 30 declared-ungraded item(s).** The checklist carries 1409 items and 1379 are cited by a grader that observes them.

| Item | Tag | Ask | Why no grader can observe it |
|---|---|---|---|
| C-CF-330 | constraint | Adding a third locale needs locale data plus translations, not a code change. | source |
| C-CF-681 | constraint | Nothing is written to the app's own disk. | container |
| C-CN-02 | constraint | A third language is addable as data. | source |
| C-CN-03 | constraint | The app sends no outbound mail of any kind. | network |
| C-CN-09 | constraint | The app makes no outbound Tipbox call, reconciliation pull or outbound studio webhook. | network |
| C-DC-04 | literal | The port mapping is `${APP_PUBLIC_PORT}:4173` with `4173` the container-internal port. | harness |
| C-DC-05 | contract | Both ports are read from the environment, never hardcoded. | source |
| C-DC-07 | contract | The app starts from the environment image with no manual steps. | harness |
| C-DC-08 | contract | `/app/USER_README.md` holds the login credentials. | container |
| C-DC-09 | contract | Reserved `.browser_screenshots/` with `.downloads/` directories exist at the app root, empty. | container |
| C-DC-11 | contract | The server keeps running after the session ends, not a child of the shell. | harness |
| C-DC-12 | contract | The backing services are used where already running, never downloaded, installed, compiled or started. | harness |
| C-DC-13 | contract | Only the providers named in the brief are used, with no edge functions. | source |
| C-DC-14 | contract | No persistent volumes, fixed container names or custom networks are used. | harness |
| C-DM-04 | contract | `/app/USER_README.md` lists each seeded account with the password. | container |
| C-DM-10 | constraint | The studio `image_signing_key` is kept across restarts. | harness |
| C-TR-03 | contract | The backend is Litestar on Python 3.12 in one server process serving the API, front end, sitemaps, page documents. | source |
| C-TR-05 | contract | The front end is Preact with Vite with TypeScript. | source |
| C-TR-13 | contract | Structured logging writes one JSON line per request on stdout with `request_id`, method, route, status, duration. | container |
| C-TR-14 | constraint | Request log lines never carry an address, password, token or signature. | container |
| C-TR-15 | contract | The app reads `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` from the environment. | source |
| C-TR-16 | constraint | The app hardcodes no host, port or credential. | source |
| C-TR-17 | constraint | The app uses only the named libraries plus direct dependencies. | source |
| C-TR-18 | constraint | The app introduces no second database, cache, queue, object store, identity provider or mail vendor. | source |
| C-TR-40 | constraint | The scheduler works on absolute instants, never wall-clock comparisons. | source |
| C-TR-44 | constraint | No binary asset ships with the build. | source |
| C-TR-49 | constraint | The app makes no outbound network call at runtime. | network |
| C-TR-50 | constraint | The app makes no call to Tipbox at runtime. | network |
| C-UX-36 | constraint | Spacing is placed by feel against the scene with no grid of spacing constants. | source |
| C-UX-91 | constraint | Full-height surfaces follow the window's real visible height as a phone browser bar retracts. | browser |

- **source** (13): observable only by reading the app's source; the reward path may not read source (INV6) and the vendored recompute.py renders no code_criteria block.
- **container** (6): a file, directory or log stream inside the app container; under `environment_mode = "separate"` the verifier has no view of `/app` or the app's stdout.
- **network** (4): a negative about the app's own outbound traffic; the verifier cannot observe egress from the app container.
- **harness** (6): a property of how the environment is started, restarted or wired; decided by the harness gates (G13, G15, G19), not by a test.
- **browser** (1): Playwright's mobile emulation has no retracting browser bar, so neither a browser substep nor pytest can reproduce it.

Stage 3 says neither invent a citation nor drop the obligation: record and escalate. This is that record, OPEN-DECISION D-H. Every other ask is graded: pytest asserts the API, the database, the object store and page markup; browser substeps and rubric criteria judge what renders; each citation shares its wording with the test or step that observes it (G24 earned check).

G47 is red because G24 is red: output_qc refuses to call an output with a red gate finished.

## Handoff gates

Undecided here; see `S_creato_cont_interactive-comic-studio-vb_20260916_101911.handoff.md`.

## Versions

- kit: deku-green-field (GreenField-GenKit2)
- vendored grader: 0.22.0
- target schema: 1.4

Exit state: **NOT MECHANICALLY-GREEN: G6, G24, G40, G47**
