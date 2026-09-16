# Build report - I_produ_crud_encrypted-note-vault-vb_20260916_094402

Rendered from `_handoff/I_produ_crud_encrypted-note-vault-vb_20260916_094402.gates.jsonl` and the sidecars beside it. No verdict on this page was typed by hand.

## Identity

| Field | Value |
|---|---|
| Task code | `I_produ_crud_encrypted-note-vault-vb_20260916_094402` |
| Task id | `deku/encrypted-note-vault-vb` |
| Cell | individual / productivity-self-management / crud-catalog |
| Task Order normalisation | `journaling-notes` -> `productivity-self-management`, `crud-records` -> `crud-catalog` (both outside the closed enums; see `_spec/.../00-decisions.md`) |
| Service profile | `P4-db-storage` |
| Providers per slot | `backend` = `postgres`, `storage` = `minio` |
| Variant | `b` on axes ['critical_depth', 'data_shape'] |
| Language | `javascript` |
| Design direction | `companion` |
| Launch surface | `form_validation,meta_tags,no_broken_links,no_frontend_secrets,social_preview` |
| spec_sections_given | ['overview', 'roles', 'features', 'flow', 'uiux', 'frontend', 'techrequirements', 'datamodel', 'constraints', 'contract'] |
| Shard | 1 of 1 (single-task run) |
| Kit | deku-green-field, grader pin `0.22.0`, schema `1.4` |
| Authors | QL `abhishek.shaw@ethara.ai`, contributor `sunil.kumar@ethara.ai` |
| uuid_v5 | `fc363d88-db89-5ae6-8552-b2e67e687d66` |
| Verifier mode | `separate` |
| Pytest module | `tests/test_output.py` |
| Companion | `prd/standardnotes_prd.md`, carried with 56 recorded G51 waivers |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Accounts where the password never leaves the device | INCLUDED | `## Core features` | companion 17 to 19; the idea's defining promise |
| Sessions, refresh rotation, reuse detection | INCLUDED | `## Core features` | companion 19.3 |
| Sealed item store and opaque-cursor sync | INCLUDED | `## Core features`, `## Deployment contract` | companion 20; documented protocol per 27.1 |
| Conflicts kept as copies, tombstone deletion | INCLUDED | `## Core features` | companion 21; the idea's closing act |
| Six note types, tags, folders, saved views, pin, archive, trash, protect | INCLUDED | `## Core features` | the idea names notes of several kinds, folders and tags |
| Device-only search and a lock that clears the page | INCLUDED | `## Core features` | companion 19.6, 25 |
| Revision history by plan | INCLUDED | `## Core features` | the idea names revision history |
| Encrypted file attachments in minio | INCLUDED | `## Core features` | the idea names attached files |
| Plans, entitlement, lapse, shared subscription | INCLUDED | `## Core features` | the idea names a paid tier |
| Export, import, account deletion | INCLUDED | `## Core features` | companion 27 |
| Home, plans, two essays, demo, not-found; drawn launch surface | INCLUDED | `## Core features`, `## Front-end specification` | reduced public surface; reference/O draw |
| Features page, help centre, knowledge base, blog, press, testimonials | DROPPED | `## Constraints` | content libraries the idea does not name |
| Regional pricing, checkout | DROPPED | `## Constraints` | no payments slot |
| Nightly mail backups and all email | DROPPED | `## Constraints` | no email slot |
| Two-factor, hardware keys, biometrics | DROPPED | `## Constraints` | no authenticator device in a headless grader; web only |
| Spreadsheet and journal types, note links, plugins, web clipper, cloud backups, self-hosting setting | DROPPED | `## Constraints` | scope; recorded in 00-decisions |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_note_written_in_browser_leaves_no_plaintext_on_server`, `test_duplicate_identifier_signup_is_refused` and `test_account_deletion_removes_items_and_frees_identifier` read rows through the capability fixture; G9 and G32 green |
| `storage` | `minio` | MET | `test_uploaded_chunks_are_stored_under_the_vault_key_scheme` (critical) asserts each chunk object exists at `vault/<file uuid>/<index>`; `test_expired_account_new_upload_is_refused` asserts nothing is stored for a refused upload |

No UNMET slot obligation.

## Grading layer

| Measure | Value |
|---|---|
| Workflows | 11 (individual band 6-11) |
| Browser substeps | 26 |
| Pytest substeps | 47 |
| Critical substeps | 10 |
| Non-happy-path ids | 5: `foreign_account_access_denied`, `synced_vault_delivers_duplicate_free_pages`, `stale_edit_conflict_keeps_both_versions`, `unknown_account_sign_in_is_denied_identically`, `expired_subscription_limit_keeps_existing_work` |
| Test module | one, `tests/test_output.py`, 47 test functions (HTTP, page-driven via Playwright, database and object store) |
| Rubric criteria | 32 (30 positive, 2 negative) |
| Checklist items | 212 across 10 sections, plus 31 declared-but-ungraded obligations |

### Rubric dimension shares, positives only

| Dimension | Points | Share | Target | Within 0.10 |
|---|---|---|---|---|
| `instruction_following` | 14 | 0.241 | 0.30 | yes |
| `functionality` | 14 | 0.241 | 0.25 | yes |
| `ux_flow` | 11 | 0.190 | 0.15 | yes |
| `ui_visual` | 12 | 0.207 | 0.15 | yes |
| `motion` | 2 | 0.034 | 0.05 | yes |
| `accessibility` | 4 | 0.069 | 0.05 | yes |
| `responsiveness` | 1 | 0.017 | 0.05 | yes |

### Checklist item classes

| Tag | Count |
|---|---|
| `capability` | 50 |
| `constraint` | 43 |
| `contract` | 15 |
| `data` | 6 |
| `literal` | 15 |
| `role` | 5 |
| `ui` | 78 |

## Literals ledger

`_handoff/I_produ_crud_encrypted-note-vault-vb_20260916_094402.literals-ledger.json` carries 73 pinned values; `DB_ADMIN_URL` is the one `verifier_only` entry.

| Class | Count |
|---|---|
| `account` | 3 |
| `credential` | 1 |
| `design_phrase` | 2 |
| `endpoint` | 12 |
| `env_var` | 7 |
| `motion_moment` | 2 |
| `number` | 3 |
| `route` | 10 |
| `scheme` | 1 |
| `seed_record` | 21 |
| `status` | 11 |

## Spec documents and the sections they fed

| Document | Fed |
|---|---|
| `00-decisions.md` | normalisation, draws, variant, identity re-cast, scope, companion carry table, waivers |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow`, the API shapes in `## Deployment contract` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at baseline |

## Grading window

Reported, never failed: the brief has no length limit (G33).

| Section | Chars | Reference |
|---|---|---|
| Core features | 25618 | 2400 |
| User flow | 5243 | 1900 |
| UI/UX notes | 5792 | 1700 |
| Constraints | 1414 | 800 |
| User roles | 1919 | 1000 |
| Overview | 2377 | 700 |
| **joined** | **42363** | 8800 |

## Kit gate log

One row per gate, rendered from the receipt file. `inputs` on every receipt carries the SHA-256 of each bundle file the sweep examined.

| Gate | Tool | Exit | Verdict | Elapsed |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | 0.18s |
| G1/G12 | `layout_lint.py` | 0 | PASS | 0.16s |
| G46 | `structure_lint.py` | 0 | PASS | 0.17s |
| G50 | `docker_lint.py` | 0 | PASS | 0.1s |
| G55 | `runtime_deps_lint.py` | 0 | PASS | 0.11s |
| G63 | `secret_lint.py` | 0 | PASS | 0.09s |
| G48 | `truth_lint.py` | 0 | PASS | 0.42s |
| G51 | `source_lint.py` | 0 | PASS | 0.2s |
| G52 | `rubric_context_lint.py` | 0 | PASS | 0.1s |
| G54 | `comment_lint.py` | 0 | PASS | 0.1s |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | 0.09s |
| G11 | `leak_scan.py` | 0 | PASS | 0.2s |
| G33 | `window_lint.py` | 0 | PASS | 0.14s |
| G4/G5 | `contract_lint.py` | 0 | PASS | 0.14s |
| G43 | `prescription_lint.py` | 0 | PASS | 0.23s |
| G44 | `disclosure_lint.py` | 0 | PASS | 0.15s |
| G10 | `no_sdk_lint.py` | 0 | PASS | 0.12s |
| G31 | `determinism_lint.py` | 0 | PASS | 0.13s |
| G14 | `reward_path_lint.py` | 0 | PASS | 0.12s |
| G27/G30 | `rubric_lint.py` | 0 | PASS | 0.1s |
| G41 | `flag_lint.py` | 0 | PASS | 0.12s |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | 0.08s |
| G59/G60 | `codequality_lint.py` | 2 | ? | 0.1s |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | 0.14s |
| G6 | `fixture_lint.py` | 0 | PASS | 0.27s |
| G24 | `coverage_map.py` | 0 | PASS | 0.13s |
| G37 | `checklist_qc.py` | 0 | PASS | 0.12s |
| G39 | `rubric_align_lint.py` | 0 | PASS | 0.19s |
| G28/G29 | `channel_lint.py` | 0 | PASS | 0.12s |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | 0.11s |
| G0/INV5 | `vendor_check.py` | 0 | PASS | 0.1s |
| G47 | `output_qc.py` | 0 | PASS | 0.19s |

32 of 32 rows green; 0 red.

## Certification prompt receipts

| Prompt | Gate | Verdict | Checks |
|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | PASS 17, WARN 7 |
| `QC_spec.md` | G34 | PASS | PASS 10, WARN 5 |
| `qc_docker.md` | G35 | PASS | NOT-APPLICABLE 9, PASS 94, WARN 2 |
| `qc_rubric.md` | G53 | PASS | PASS 14, WARN 2 |
| `qc_solution_checklist.md` | G37 | PASS | no declared registry |
| `qc_toml.md` | G36 | PASS | NOT-APPLICABLE 10, PASS 108, WARN 2 |
| `solution_checklist.md` | S3 | PASS | no declared registry |
| `task_code_verifier.md` | G3 | VALID | PASS 12 |

Every receipt is self-attested (`verifier: self`): the same agent authored and reviewed, so these are recorded verdicts rather than independent ones. `rubric_author.md` and `toml_generator.md` carry no receipt because they were not read in full for this build.

## Handoff gates, undecided here

| Gate | Command | Expected |
|---|---|---|
| G13 | `docker build -f environment/Dockerfile .` | exit 0 |
| G13 | `docker build -f tests/Dockerfile .` | exit 0 |
| G15 | `docker compose up` on a scrubbed host | postgres and minio healthy, minio-init parked |
| G18 | read `deployed` from either oracle run | `deployed == 1.0` |
| G19 | `harbor run -p <task> -a oracle`, twice | `reward == 1.0` both times |
| G20 | `harbor run -p <task> -a nop` | `reward == 0.0` |
| G21 | fake-integration patch (server-side encryption, or bytes on the app disk), then oracle | `reward < 1.0` |
| G25 | reviewer exploit sweep, reference library F | 0 of 11 succeed |

## Blocking findings

None. No gate is red and no slot obligation is UNMET.

### Non-blocking findings carried from the certification receipts

**`QC_instruction.md`**

- A1: `## Build plan` is absent. generate_instruction.md S-2.1 makes it non-baseline; the other ten H2s are present and canonical, and `## Front-end specification` is the optional eleventh.
- B1: one role as the individual category modifier requires, renamed `Account holder` by the role-fit rule; the storage slot is the legal P4 add-on recorded in 00-decisions.md.
- B3: Technical requirements and Data model are present; Build plan is withheld as baseline, per A1.
- C1: a minority of rules are not black-box checkable and are listed under `## Declared but ungraded` in the checklist with a why each: token lifetimes, the memory-hard derivation, constant-time comparison, offline catch-up, tag normalisation and folder-loop repair inside sealed items, retention floors.
- C7: Core features, User flow and UI/UX notes run past the 2,500-character slice and the join past 9,000. window_lint reports and fails nothing; the judged criteria carry their own facts.
- D1: the laziest passing build would seal notes with a homemade reversible cipher under a random nonce: the DB scan, encoding scan and fresh-envelope check all pass while the protection is weak. No black-box grader can tell real authenticated encryption from that; companion 30.1 calls the same test a hiring question. Residual and recorded.
- D5: the companion states an exact type scale and two licensed families; the brief carries one freely licensed geometric grotesque family by role with no sizes, following the tasker's standing directive over reference A5. Recorded in 00-decisions.md with the reason; no other contradiction found.

**`QC_spec.md`**

- S2: 01-PRD.md lists ten must-have features where S2 asks for three to six. config/corpus-targets.yaml companion_feature_cap is [6, 10] for a companion-backed task and generate_instruction.md Phase 1 says 6-10 with a companion; the prompt row predates that cap.
- S5: 04-uiux-brief.md carries no hex palette and no millisecond or cubic-bezier values. The settled number rule (generate_instruction.md S-4) carries colour as family, tone and shade and motion as character, and G51 checks the colour words; the tasker's standing directive also leaves type sizes to the builder. Accessibility values (4.5:1, 44 by 44) are literal. S5's value demand is superseded.
- S7: 06-implementation-plan.md is written as bulleted stages in dependency order with exit conditions on the core stages, not numbered phases each with an exit. It is author-side only because `## Build plan` is not baseline, and prescription_lint forbids a numbered build sequence in the brief.
- S8: 00-decisions.md records decisions in paragraphs and tables rather than one line each, because generate_instruction.md requires the companion carry table, the identity re-cast and the draw lines there as well. Every residual judgment call is still its own bullet.
- B1: the crud-catalog row names db only; the bundle adds the storage slot through P4-db-storage, a legal profile for I+crud chosen because the idea names attached files. Role count (one) matches.

**`qc_docker.md`**

- CMP-011: `main` publishes `${APP_PUBLIC_PORT:-4173}:4173`. CMP-011 forbids `ports:` while CMP-022 requires it on `main`, and validate_task enforces CMP-022 under G2. No sidecar publishes a port.
- CMP-020: `main` carries `extra_hosts` and `ports` beyond `depends_on`. Both are required by CMP-022 and stage-5-dockerfile.md C12, so the Low-severity CMP-020 row is superseded.
- DEP-011: `[verifier].environment_mode` is `separate`; the grader ships its own image.
- DEP-012: no playwright is installed in the agent image; the verifier image carries Chromium.
- DEP-015: `language` is `javascript`.
- DEP-016: no build stage exists and nothing is COPYed into the image.
- DEP-017: `language` is not `java`.
- BP-004: the Node setup script is fetched from its official registry, which publishes no checksum for it.
- BP-005: there is no build output to carry forward; the agent writes the app at run time.
- BP-008: the base is glibc Debian bookworm, not musl.
- SEC-003: no source establishes non-root execution for the agent image, and the agent writes to /app.

**`qc_rubric.md`**

- RC-08: the broken saved view criterion (This view cannot be evaluated) needs a view that fails to evaluate, which no seeded record provides, so a judge may have no instance to look at. The criterion is kept because the brief states the behaviour and the rule says where to look.
- RC-12: the WCAG contrast criterion on the notes page is arithmetic over two computed colours and could be a page-driven pytest assertion (reference/O S-O.2 routes colour_contrast to pytest). It is not a drawn token here, so it stays with the judge, which is advisory. Residual and recorded.

**`qc_toml.md`**

- SCHEMA-011: `[delivery]` is emitted and is not in the toml_generator.md S-11 template. It is required of new bundles by 01-OUTPUT-CONTRACT.md CON-2 and validated by validate_task under G2. `[delivery.images]` is omitted because the images are tag-pinned rather than digest-pinned, which validate_task accepts; no digest was fabricated.
- SCHEMA-013: `[delivery]` sits between `[verifier]` and `[[artifacts]]`; the template defines no position for it. See SCHEMA-011.
- BENCH-002: not a trivial task; the Standard tier applies (BENCH-001).
- BENCH-003: `difficulty` is the mandated empty placeholder, so there is no declared tier to band against. turns_expected 200 and tokens_expected 8000000 sit inside BENCH-004's absolute range.
- BENCH-005: `difficulty` is empty; nothing to check consistency against.
- INT-007: same as BENCH-005.
- TAX-006: `language` is `javascript`, not `any`.
- TAX-008: global archetype uniqueness is not verifiable from the inputs; the mint ledger refused no claim for `encrypted-note-vault`.
- INST-007: `instruction.md` is present.
- SIGN-001: deprecated 2026-09-15, superseded by SIGN-004.
- SIGN-002: deprecated 2026-09-15, superseded by SIGN-004.
- SIGN-003: deprecated 2026-09-15, superseded by SIGN-004.

### Residual risks the static kit cannot retire

- Page-driven pytest tests depend on the pinned labels (`Email`, `Password`, `Sign in`, `Title`, `Note body`, `Create note`, `Search notes`, `Passcode`, `Turn on lock`, `Lock now`, `Unlock`). They are pinned in the brief, but only an oracle run proves the selectors resolve against a real build.
- Seeded-account sign-in runs the app's memory-hard derivation in Chromium; the page timeout is 120 seconds per action. A very slow derivation parameter choice would time out.
- `test_signup_form_names_invalid_field_and_creates_nothing` accepts either `aria-invalid` on the Password field or a visible message mentioning the password.

## Budget

`turns_expected = 200`, `tokens_expected = 8000000` (the BENCH-004 ceiling). Ten companion features, client-side cryptography in vanilla scripts, a sync protocol with conflicts and tombstones, chunked file storage and a public surface. `difficulty` stays the empty placeholder the Calibration Engineer fills.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference app. Nothing counts toward a corpus target until the app lands and `harbor run -a oracle` returns `1.0` twice.
