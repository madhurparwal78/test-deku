# Build report - S_creato_cont_remixable-timeline-editor-vb_20260916_103719

| | |
|---|---|
| Task code | `S_creato_cont_remixable-timeline-editor-vb_20260916_103719` |
| Task id | `deku/remixable-timeline-editor-vb` |
| Cell | solo_founder / creator-monetization / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | `backend` = `postgres`, `storage` = `minio` |
| Variant | `b` on axes ['critical_depth', 'spec_sections'] |
| Language | `python` |
| Capability flags | `aesthetic` |
| Design direction | `companion` |
| Launch surface | `favicon,form_validation,meta_tags,page_view_log,privacy_page` |
| Spec sections given | ['overview', 'roles', 'features', 'flow', 'uiux', 'frontend', 'techrequirements', 'datamodel', 'constraints', 'contract'] |
| Shard | 1 of 1 |
| Kit | deku-green-field, gate index G0-G63 |
| Grader pin | `0.22.0` |
| Target schema | `1.4` |
| Verifier mode | `separate` |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Task Order and taxonomy recast

The Task Order (`task-orders/remixable-timeline-editor.yaml`) named `solo_founder` /
`creator-media` / `media-gallery`. Neither `creator-media` nor `media-gallery` is in the enum
(reference/A A.2, A.3). The tasker confirmed the recast before the mint:

| Field | Task Order | Emitted |
|---|---|---|
| category | solo_founder | solo_founder |
| domain | creator-media | creator-monetization |
| pattern | media-gallery | content-publishing |
| variant | (absent) | b |

`content-publishing` keeps the Task Order's intent: upload, organise and view collections on a
database plus an object store, with a critical focus on protected media never being publicly
readable, which is the PRD's share-link rule.

## Source material

The tasker supplied `/home/grt/Downloads/Greenfield_testing/prd/butter-video_prd.md`, a measured capture of the reference product, and it is carried in
full. G51 was run against it: 4/4 source colours described by family and tone (the brief carries
no colour code), 147/147 topics and 358/358 enumerated items carried. Fifteen author waivers
cover document meta, measured CSS values and the evidence notes, each recorded in the companion
carry table in `Output/_spec/<code>/00-decisions.md`.

Following the operator's instruction, the brief describes every interface element in words. It
names no pixel, position, size, colour code, font family, animation name, curve, function name or
parameter value. It does name the stack. G43 (prescription) and G44 (disclosure) are both green
on that text.

## Derived design draws

Drawn by SHA-256 over `[metadata].archetype`, never chosen:

```
draw: render_model = ssr-islands
draw: backend = FastAPI
draw: frontend = Astro + islands
draw: design_direction = companion
draw: nav = sidebar-nav
draw: work_surface = table-first
draw: create_flow = inline-row
draw: feedback = full-page-confirmation
draw: launch_surface = favicon,form_validation,meta_tags,page_view_log,privacy_page
```

The design-direction draw returned `glass-depth`. Because a measured companion was supplied,
reference/L section L.6.1 applies and `design_direction = "companion"` governs. The drawn token
is recorded in `00-decisions.md` only.

## Feature resolution

| Candidate | Verdict | Where it landed | Reason |
|---|---|---|---|
| Accounts, sign-in and the owned workspace | INCLUDED | Core features, User flow | PRD sections 12 and 18; public signup is the solo_founder modifier |
| Plans and the pricing page with a computed annual saving | INCLUDED | Core features, Front-end specification | PRD section 10; stored values, saving computed rather than typed |
| Seven stored limits per plan, three monthly allowances and four ceilings, enforced on the server | INCLUDED | Core features, Data model | PRD section 18; exactly one claim on the last unit succeeds |
| Seats, invitations and in-app charges with proration | INCLUDED | Core features | PRD section 18.3 items 1 to 4; charges are the app's own records |
| The library of blocks, templates and brand kits | INCLUDED | Core features, Front-end specification | PRD sections 8 and 13 |
| Remix, Describe and Code | INCLUDED | Core features | PRD section 13; Describe spends one variation |
| Projects and the timeline with revision-checked saves | INCLUDED | Core features, Data model | PRD section 13; one of two saves from one revision lands |
| Saved blocks with versions, owned by the workspace | INCLUDED | Core features | PRD section 13.4; the per-plan cap resolved to one stored value |
| Media in the object store under a content digest | INCLUDED | Core features, Data model | the pattern's critical focus; private bucket, app routes only |
| Frozen versions and exports against the plan's quota | INCLUDED | Core features | PRD section 18; rendered in the browser, validated by the server, idempotent on a request key |
| Share links with expiry, passphrase, recipients and a download switch | INCLUDED | Core features | PRD section 19 A to E |
| Timecoded comments, approvals and notifications | INCLUDED | Core features | PRD section 19; the reviewer is a separate role reached only by invitation |
| Five client compound cases | INCLUDED | Core features | PRD sections 13.7 and 18.7, the observable subset |
| The marketing site, blog, contact form and creator pages | INCLUDED | Core features, Front-end specification | PRD sections 7 to 11 |
| The consent panel | INCLUDED | Core features, Front-end specification | PRD section 7.5; reject is as prominent as accept |
| Soft-404 and API-404 fixes | INCLUDED | Core features | PRD section 23.3 defects fixed |
| The three-dimensional hero | INCLUDED | Front-end specification | PRD section 6; seven pieces with a still fallback |
| Payment provider, callbacks, replay protection, failed renewals | DROPPED | - | no payment slot in P4-db-storage |
| Captioning, speech, background removal, stock media | DROPPED | - | no engine in the environment; published as `coming_soon`, allowances stored and never spent |
| ProRes and 4K export | DROPPED | - | no server-side encoder; browser rendering caps the size |
| Real-time co-editing | DROPPED | - | no realtime slot; replaced by revision-checked saves |
| Viewer-tied watermarks and domain-restricted playback | DROPPED | - | needs server-side frame rendering or referrer checks no channel can grade |
| The save-conflict screen | DROPPED | - | reference/N gives the browser grader one tab; G24 has no waiver for an unobservable item |
| Undo across members, panel open on a deleted item | DROPPED | - | needs two live sessions |
| Stdout request logging, byte budgets, will-change hints | DROPPED | - | no channel observes them |

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_seeded_subscription_rows_are_persisted` (critical), `test_seeded_library_rows_are_persisted` (critical), plus the tests that read the quota, charge, share and approval tables the brief names |
| `storage` | `minio` | MET | `test_uploaded_file_is_stored_in_the_bucket_under_its_digest` (critical), `test_bucket_objects_are_not_publicly_readable` (critical), `test_store_and_bucket_hold_the_records_the_api_reports` |

No slot is UNMET.

## Graders

- Workflows: **15** (solo_founder band 10-16)
- Browser substeps: **55** - pytest substeps: **116** - ratio **0.47** (G45 band 0.40-2.00)
- Critical substeps: **22**
- Non-happy-path workflow ids: `concurrent_timeline_saves_conflict`, `saved_block_limit_refuses_the_extra`, `seat_limit_holds_under_concurrent_invites`, `variation_allowance_limit_under_concurrency`, `share_download_denied_when_switched_off`, `reviewer_cannot_reach_workspace_work`
- One pytest module, `tests/test_output.py`, **116** tests across accounts, plans,
  quotas, seats, the library, timelines, saved blocks, media, exports, shares, comments,
  approvals, authorization and storage.
- Checklist: **661** items across 10 section codes (`capability` 189, `constraint` 146, `contract` 28, `data` 118, `literal` 58, `role` 21, `ui` 101)

### Declared but ungraded by an automated channel

One browser substep carries an `earned:` note. These App Contract items live on the agent
container, which a separate-mode grader cannot read. The substep proves that the seeded login
they carry works, and the operator observes the files themselves by hand at the oracle run
(OPEN-DECISIONS D-H).

| Item | What it covers |
|---|---|
| `C-DM-02` | Every seeded login is written to `/app/USER_README.md` with the corpus password. |
| `C-DC-07` | Login credentials are written to the credentials file at the app root. |
| `C-DC-08` | Empty `.browser_screenshots/` plus `.downloads/` directories exist at the app root. |
| `C-DC-06` | The app starts from the environment image with no manual steps. |
| `C-DC-03` | The public port is read from `APP_PUBLIC_PORT`. |
| `C-DC-12` | The backing services are used as already running. |
| `C-DC-13` | The app uses only the named providers with no edge functions. |
| `C-DC-14` | The app adds no persistent volumes, fixed container names or custom networks. |
| `C-TR-11` | The app starts no copy of PostgreSQL or MinIO. |

## Rubric

27 judged criteria: 26 positive totalling 66, 1 negative
(R27 at -5). The negative has its own checklist
obligations and does not mirror a positive (qc_rubric RC-02).

| Dimension | Criteria | Positive share | Target | Delta |
|---|---|---|---|---|
| `instruction_following` | 5 | 0.288 | 0.30 | -0.012 |
| `functionality` | 4 | 0.182 | 0.25 | -0.068 |
| `ux_flow` | 3 | 0.167 | 0.15 | +0.017 |
| `ui_visual` | 5 | 0.197 | 0.15 | +0.047 |
| `motion` | 3 | 0.045 | 0.05 | -0.005 |
| `accessibility` | 5 | 0.106 | 0.05 | +0.056 |
| `responsiveness` | 1 | 0.015 | 0.05 | -0.035 |

Task-completion share 0.80 (band 0.60-0.80). The rubric is GENERATED from
`judged_criteria` in `solution/trinity/grounding.yaml`, and G48 re-runs the generator under
`--check` on every sweep, so it cannot be hand-edited.

## Literals ledger

354 pinned values, every one present verbatim in `instruction.md`:

| Class | Count |
|---|---|
| `account` | 7 |
| `credential` | 3 |
| `endpoint` | 28 |
| `env_var` | 9 |
| `number` | 19 |
| `route` | 22 |
| `scheme` | 3 |
| `seed_record` | 182 |
| `status` | 81 |

2 values are `verifier_only`: `DB_ADMIN_URL`, `deku_admin`, carried by
`task.toml` `[verifier].env` alone (INV4).

The checklist also lists two values the brief refers to without pinning: the stored consent
wording (C-CF-304) and a creator's credit line (C-CF-123). The builder chooses both texts, and no
grader asserts either one.

## Spec folder

Written to `Output/_spec/<code>/`, never inside the bundle (CON-5).

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the taxonomy recast, the residual judgment calls, the companion carry table |
| `01-PRD.md` | Overview, Core features, Constraints |
| `02-TRD.md` | Technical requirements |
| `03-app-flow.md` | User flow |
| `04-uiux-brief.md` | UI/UX notes, Front-end specification (author-side values stay here, never in the brief) |
| `05-backend-schema.md` | Data model, User roles |
| `06-implementation-plan.md` | author-side only; Build plan is not emitted at baseline |

## Grading window

```
section        H2                chars  reference  flag
core_features  Core features     37691       2400  past-slice
user_flow      User flow          6198       1900  past-slice
ui_ux_notes    UI/UX notes        9832       1700  past-slice
constraints    Constraints        1297        800  over-reference
user_roles     User roles         2515       1000  past-slice
overview       Overview           1698        700  over-reference
joined total                     59231       8800  past-slice
first four                       55018       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```

The operator waived the section targets so the brief could describe every UI and UX element in
full. G33 measures length and fails nothing on it. Content past the slice still reaches the agent
in full but no longer reaches the advisory judge, and `judge_score` never touches reward. The
prompt receipts record this again as QC_instruction C7.

## Kit gate log

Rendered from `_handoff/<code>.gates.jsonl`. Never transcribed.

| Gate | Tool | Exit | Verdict | Seconds |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | 0.07 |
| `G1/G12` | `layout_lint.py` | 0 | PASS | 0.05 |
| `G46` | `structure_lint.py` | 0 | PASS | 0.06 |
| `G50` | `docker_lint.py` | 0 | PASS | 0.04 |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | 0.06 |
| `G63` | `secret_lint.py` | 0 | PASS | 0.04 |
| `G48` | `truth_lint.py` | 0 | PASS | 0.37 |
| `G51` | `source_lint.py` | 0 | PASS | 0.07 |
| `G52` | `rubric_context_lint.py` | 0 | PASS | 0.04 |
| `G54` | `comment_lint.py` | 0 | PASS | 0.04 |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | 0.04 |
| `G11` | `leak_scan.py` | 0 | PASS | 0.06 |
| `G33` | `window_lint.py` | 0 | PASS | 0.04 |
| `G4/G5` | `contract_lint.py` | 0 | PASS | 0.05 |
| `G43` | `prescription_lint.py` | 0 | PASS | 0.1 |
| `G44` | `disclosure_lint.py` | 0 | PASS | 0.05 |
| `G10` | `no_sdk_lint.py` | 0 | PASS | 0.12 |
| `G31` | `determinism_lint.py` | 0 | PASS | 0.13 |
| `G14` | `reward_path_lint.py` | 0 | PASS | 0.04 |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | 0.06 |
| `G41` | `flag_lint.py` | 0 | PASS | 0.07 |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | 0.03 |
| `G59/G60` | `codequality_lint.py` | 2 | ? | 0.05 |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | 0.11 |
| `G6` | `fixture_lint.py` | 0 | PASS | 0.22 |
| `G24` | `coverage_map.py` | 0 | PASS | 0.12 |
| `G37` | `checklist_qc.py` | 0 | PASS | 0.11 |
| `G39` | `rubric_align_lint.py` | 0 | PASS | 0.1 |
| `G28/G29` | `channel_lint.py` | 0 | PASS | 0.09 |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | 0.06 |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | 0.04 |
| `G47` | `output_qc.py` | 0 | PASS | 0.08 |

`G59/G60` exits 2 with no verdict. The code rubric has no generator in this kit revision
(stage 3.6 is absent from 00-RUN), so nothing exists for the lint to check, and the sweep records
the row as not applicable. `G40` is WARN because every receipt is self-attested (below).

Corpus-level gates, run once over the whole output root rather than per bundle:

| Gate | Tool | Verdict |
|---|---|---|
| `G42` | `corpus_overlap.py` | PASS - 25 bundles, 1 cross-archetype pair compared, none over 60% substep overlap |
| `G49` | `diversity_lint.py` | PASS (WARN mode) - one concentration finding: `design_direction` is 32% `companion` (8/25) against a 30% cap. This bundle is one of the eight, and L.6.1 requires `companion` whenever a measured companion is supplied. No shared prose run over the per-section caps; this bundle's auth paragraph was reworded to clear one |
| `G61` | `corpus_report.py` | NOT-APPLICABLE - 25 minted, 25 unproven; no admissible bundle to measure a mix against |
| `G38` | `kit_selftest.py` | PASS - 32 cross-file agreement checks |

## Prompt receipts

`_handoff/<code>.receipts.json`, 292 declared checks answered across 9 prompts.

| Prompt | Gate | Verdict | Checks | Non-PASS |
|---|---|---|---|---|
| `generate_instruction.md` | S2 | PASS | 0 | - |
| `qc_docker.md` | G35 | PASS | 105 | ARCH-002 NOT-APPLICABLE, ARCH-003 NOT-APPLICABLE, BLD-004 NOT-APPLICABLE, BP-005 NOT-APPLICABLE, DEP-011 NOT-APPLICABLE, DEP-015 NOT-APPLICABLE, DEP-016 NOT-APPLICABLE, DEP-017 NOT-APPLICABLE, ENV-003 NOT-APPLICABLE, ENV-004 NOT-APPLICABLE |
| `QC_instruction.md` | G34 | PASS | 24 | A8 WARN, B3 WARN, C5 WARN, C7 WARN |
| `qc_rubric.md` | G53 | PASS | 16 | - |
| `qc_solution_checklist.md` | G37 | PASS | 0 | - |
| `QC_spec.md` | G34 | PASS | 15 | - |
| `qc_toml.md` | G36 | PASS | 120 | BENCH-002 NOT-APPLICABLE, INST-007 NOT-APPLICABLE, SCHEMA-011 WARN, SCHEMA-013 WARN, SIGN-001 NOT-APPLICABLE, SIGN-002 NOT-APPLICABLE, SIGN-003 NOT-APPLICABLE, TAX-006 NOT-APPLICABLE, TAX-008 WARN, VERIF-005 WARN |
| `solution_checklist.md` | S3 | PASS | 0 | - |
| `task_code_verifier.md` | G3 | VALID | 12 | - |

Every receipt is SELF-ATTESTED: this run used one agent as both owner and verifier. The kit
requires owner != verifier, so these are recorded verdicts, not independent ones. The WARNs:

- QC_instruction A8, B3 and C5 flag the operator's no-values rule, which conflicts with the
  prompt's request for measured values. C7 flags the waived section targets.
- qc_toml SCHEMA-011 and SCHEMA-013 flag `[delivery]` shipping without `[delivery.images]`
  (no digest exists offline). VERIF-005 flags the `localhost` default the prompt still expects.
  TAX-008 flags the recast domain and pattern.

## Blocking findings

None. These obligations were resolved rather than shipped:

- **Unobservable brief sentences were cut.** No channel could observe token expiry, the
  save-conflict screen, an upload size ceiling, per-member favourites, quota-window rollover, a
  hidden tab, storage-refusal copy or a session expiring mid-action. G24 has no waiver for an
  uncitable item.
- **The billing half of the PRD has no provider in P4-db-storage.** Charges are the app's own
  records with proration. Provider callbacks, replay protection and failed renewals are out of
  scope and recorded in `00-decisions.md`.
- **The sibling bundle's `tests/workflows.yaml` does not parse under `yaml.safe_load`.** This
  bundle double-quotes every `do`, `purpose` and `cov` value so the harness can load it.

## Budget

`turns_expected` 200, `tokens_expected` 8000000. The reasoning:
two layers on one origin (a server-rendered marketing site with islands, and a signed-in editor),
seven quota meters with concurrency-safe spending, in-app charges with proration, an idempotent
export path that renders in the browser and validates on the server, a private object store served
through app routes only, and a review layer with share links, timecoded comments and approvals. The
token budget sits at the qc_toml ceiling. `difficulty` stays the empty calibration placeholder: the
Calibration Engineer writes it, never the author.

## Exit

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts this bundle toward corpus targets until the reference app is
built downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
