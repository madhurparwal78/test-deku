# Build report - E_itdev_cont_connected-workspace-platform-vb_20260916_053702

Rendered from `E_itdev_cont_connected-workspace-platform-vb_20260916_053702.gates.jsonl`. No verdict on this page was typed by hand.

## Identity

| | |
|---|---|
| task code | `E_itdev_cont_connected-workspace-platform-vb_20260916_053702` |
| task id | `deku/connected-workspace-platform-vb` |
| cell | enterprise / it-devtools / content-publishing |
| service profile | P4-db-storage |
| providers | db -> `postgres`, storage -> `minio` |
| variant | `b`, axes `critical_depth`, `spec_sections` |
| language | python |
| design direction | `companion` (reference/L L.6.1) |
| launch surface | custom_404, favicon, no_broken_links, no_frontend_secrets, security_headers |
| spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| grader pin | 0.22.0 |
| target schema | 1.4 |
| verifier mode | separate (the kit default since 11eaf7b) |
| companion | `prds/notion_prd.md` |

## Derived-design draws

SHA-256 over the archetype `connected-workspace-platform`, per reference/L L.4.

```
draw: render_model = spa-json-api
draw: backend = FastAPI
draw: frontend = Lit + Vite
draw: design_direction = companion   (raw draw brutalist-utility, overridden per L.6.1)
draw: nav = sidebar-nav              (raw draw top-nav, overridden by the companion)
draw: work_surface = split detail-pane
draw: create_flow = modal
draw: feedback = optimistic-row
```

## Feature resolution

| Feature | Verdict | Where |
|---|---|---|
| Accounts and sessions | INCLUDED | ## Core features, Auth |
| Teamspaces and groups, three access modes | INCLUDED | ## Core features, Teamspaces and groups |
| Pages and blocks, editing and rich text | INCLUDED | ## Core features, Pages and blocks |
| Databases, views and nested filters | INCLUDED | ## Core features, Databases and views |
| The authorization decision | INCLUDED | ## Core features, The authorization decision |
| Attachments in the object store | INCLUDED | ## Core features, Attachments |
| Publishing to the web | INCLUDED | ## Core features, Publishing a page to the web |
| Admin console and the activity record | INCLUDED | ## Core features, Admin console |
| Workspace search | INCLUDED | ## Core features, Workspace search |
| The product's own surfaces | INCLUDED | ## Core features, The product's own surfaces |
| Realtime, presence, cursors | DROPPED | no realtime provider in environment/registry.json |
| AI assistant and agents | DROPPED | no model provider in this environment |
| Billing, seats, plans, invoices | DROPPED | no payments slot on P4-db-storage |
| Federated identity, SCIM, passkeys | DROPPED | no identity provider in this environment |
| Automations, connectors, webhooks | DROPPED | no queue and no outbound network at runtime |
| Notifications and email | DROPPED | no email slot on P4-db-storage |
| Custom domains and edge cache | DROPPED | the app serves published pages on its own origin |
| Marketing site | DROPPED | out of scope per the Task Order idea |

## Slot obligations

| Slot | Provider | State | Evidence |
|---|---|---|---|
| db | `postgres` | MET | `test_seeded_rows_are_stored_exactly_once`, `test_page_row_persisted_matches_what_the_page_endpoint_returned`, `test_activity_record_rows_are_stored_for_each_mutation` assert rows through the backend adapter |
| storage | `minio` | MET | `test_uploaded_attachment_object_exists_in_the_bucket_at_its_key` asserts the object through the S3 adapter; `test_attachment_bytes_are_not_stored_in_a_database_column` asserts the negative |

## Grading surface

| | |
|---|---|
| workflows | 23 |
| browser substeps | 30 |
| pytest substeps | 45 |
| critical substeps | 18 |
| non-happy-path workflow ids | 11 |
| pytest module | `tests/test_output.py` (one module, CON-2) |
| pytest functions | 40 |
| rubric criteria | 25 (23 positive, 2 negative) |
| checklist items | 400 |

Non-happy-path ids: `unpublished_page_is_denied_to_an_anonymous_reader`, `private_teamspace_cannot_be_discovered_or_reached`, `member_request_to_an_admin_endpoint_is_denied`, `guest_cannot_see_a_hidden_property`, `attachment_on_an_unpublished_page_is_forbidden_to_a_stranger`, `concurrent_block_writes_produce_exactly_one_winner`, `unauthenticated_request_for_a_workspace_route_is_denied`, `seeded_accounts_sign_in_and_signout_invalidates`, `invalid_block_depth_is_refused`, `deactivated_principal_cannot_continue`, `expired_grant_is_refused_on_the_next_read`

### Rubric dimension shares (positive scores only)

| Dimension | Criteria | Share | Target | Within 0.10 |
|---|---|---|---|---|
| instruction_following | 5 | 0.333 | 0.30 | yes |
| functionality | 3 | 0.238 | 0.25 | yes |
| ux_flow | 3 | 0.143 | 0.15 | yes |
| ui_visual | 4 | 0.143 | 0.15 | yes |
| motion | 4 | 0.048 | 0.05 | yes |
| accessibility | 3 | 0.048 | 0.05 | yes |
| responsiveness | 3 | 0.048 | 0.05 | yes |

### Checklist items per section

| Section | Items |
|---|---|
| C-CF | 150 |
| C-CN | 13 |
| C-DC | 25 |
| C-DM | 26 |
| C-FE | 28 |
| C-OV | 8 |
| C-RL | 20 |
| C-TR | 22 |
| C-UF | 24 |
| C-UX | 84 |

## Literals ledger

| Class | Count |
|---|---|
| account | 4 |
| credential | 1 |
| design_phrase | 12 |
| endpoint | 32 |
| env_var | 8 |
| motion_moment | 5 |
| number | 3 |
| route | 8 |
| scheme | 2 |
| seed_record | 39 |
| status | 23 |
| **total** | **137** |

Full values, their classes and their carriers are in `E_itdev_cont_connected-workspace-platform-vb_20260916_053702.literals-ledger.json` beside this report.

## Grading window

`window_lint.py` reports length and fails nothing on it (G33). Measured at this sweep:

| Section | Chars | Reference |
|---|---|---|
| core_features | 21322 | 2400 |
| user_flow | 4139 | 1900 |
| ui_ux_notes | 11741 | 1700 |
| constraints | 1839 | 800 |
| user_roles | 2126 | 1000 |
| overview | 2320 | 700 |

Past the judge's slice the prose still reaches the agent in full; what it loses is the advisory `judge_score`, which never touches reward. The tasker waived the section caps for this bundle and `generate_instruction.md` section 4 retired them.

## Kit gate log

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
| G59/G60 | `codequality_lint.py` | 2 | NOT-APPLICABLE |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | PASS |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 1 | FAIL |

### Red gates

**G46** (`structure_lint.py`, exit 1)


**G47** (`output_qc.py`, exit 1)


`G46` is red because the bundle sits under `GreenField-GenKit2/output_16sep/`, the path the tasker specified, and `structure_lint.py` resolves the generation kit as the whole `GreenField-GenKit2` tree rather than its `deku-green-field/` package. CON-1 wants the output root beside the kit; under the tool's resolution no path inside this repository can satisfy that, and `output_root` cannot change it because the second half of the check reads the tool's own `__file__`. The gate was not loosened and the bundle was not moved. Moving `output_16sep/` one level up, beside `GreenField-GenKit2/`, turns it green with no change to the bundle.

## Prompt receipts

| Prompt | Gate | Verdict | Checks answered | Verifier |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | self |
| `QC_spec.md` | G34 | PASS | 15 | self |
| `generate_instruction.md` | S2 | PASS | 0 | self |
| `qc_docker.md` | G35 | PASS | 105 | self |
| `qc_rubric.md` | G53 | PASS | 16 | self |
| `qc_solution_checklist.md` | G37 | PASS | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | self |
| `task_code_verifier.md` | G3 | VALID | 12 | self |

Every certification prompt was run and its scorecard recorded. Owner and verifier are the same agent on this run, so `prompt_receipt_lint.py` reports each one SELF-ATTESTED: a recorded verdict, never an independent one.

### Recorded non-pass checks

**`QC_instruction.md`** - A1 WARN, B3 WARN, C4 WARN, C5 WARN, C7 WARN

- A1: `## Build plan` is absent. generate_instruction.md 2.1 makes Build plan NOT baseline (6/6 shipped reference briefs omit it, and a numbered build sequence removes the design work this benchmark measures); task.toml `spec_sections_given` correspondingly omits `buildplan`. The ten emitted H2s plus the optional `## Front-end specification` are present and canonically spelled.
- B3: the third lever (`## Build plan`) is deliberately not emitted, for the reason recorded against A1. `## Technical requirements` and `## Data model` are both present, which is the baseline lever set generate_instruction.md 2.1 defines.
- C4: `## UI/UX notes` carries the exact type scale in pixels, which this check reads as a numeric recipe. generate_instruction.md 'The number rule, DECIDED (A5)' carries type exactly and forbids hex, milliseconds, cubic-bezier and breakpoint pixels; the brief holds none of those four. `44px by 44px` and `4.5 to 1` are accessibility floors, which the same rule writes out.
- C5: `## Data model` names no storage-engine construct for the concurrency rule, because INV9 and G43 forbid it. The rule is stated as the observable invariant instead: two writes carrying the same block version produce exactly one acceptance, under real concurrency. Derived-not-stored values and idempotent seeding are both stated.
- C7: `## Core features` is about 21,300 characters and the joined six about 43,100, past the judge's 2,500 and 9,000 slices. generate_instruction.md 4 retired the section budget ('there is no length limit ... do not cut a real rule to fit') and window_lint.py (G33) reports length without failing it; the tasker also waived the cap for this bundle. The rules past the cut still reach the agent in full and are graded by pytest and by the browser; what they lose is the advisory judge score, which never touches reward.

**`QC_spec.md`** - S2 WARN, S5 WARN, S6 WARN

- S2: 01-PRD.md carries NINE must-have features, not the 3-6 this prompt asks for. config/corpus-targets.yaml `companion_feature_cap: [6, 10]` raises the cap for a companion-backed task, and stage-1-derive.md routes this task to variant b for the same reason. The prompt predates that key; the config wins and the deviation is recorded rather than hidden.
- S5: 04-uiux-brief.md carries no hex palette, no millisecond durations and no cubic-bezier, which this check asks for. generate_instruction.md 'The number rule, DECIDED (A5)' and tools/source_lint.py (G51) forbid a hex anywhere in the corpus text and forbid a duration in the design brief; the exact type scale, the a11y bar and the mode commitment ARE carried as the same rule requires. The number rule is the later and machine-enforced decision.
- S6: 05-backend-schema.md states each concurrency rule as an observable invariant (two writes from one block version produce exactly one acceptance) rather than as a named index or constraint. INV9 and tools/prescription_lint.py (G43) forbid naming the storage-engine construct; the invariant is stated in the stronger observable form the gate requires.

**`qc_docker.md`** - CMP-020 WARN

- CMP-020: the `main` service carries `extra_hosts` and `ports` as well as `depends_on`, so it does not exist solely to express ordering. CMP-022 and reference/C C.6 (C12) require both keys on `main`; validate_task.py enforces them. CMP-020 is a Low-severity convention row that CMP-022 supersedes.

**`qc_toml.md`** - SCHEMA-011 WARN

- SCHEMA-011: task.toml carries a `[delivery]` table and a `[delivery.images]` placeholder-free omission that the canonical template in this prompt does not list. 01-OUTPUT-CONTRACT.md CON-2 and stage-4-task-toml.md require `[delivery]` on every schema-1.4 bundle, and validate_task.py (G2) validates it. `[delivery.images]` is omitted deliberately: CON-2 wants a `@sha256:` digest per image while reference/C C.4 forbids a single-architecture child digest and forbids a fabricated one, and no registry is reachable from this run to resolve a manifest-list digest. The validator treats an absent images table as legal.

## Blocking findings

- **G46 / CON-1 placement.** Recorded above. Not a defect in the bundle.
- **`[delivery.images]` omitted.** CON-2 asks for a `@sha256:` digest per image; reference/C C.4 forbids a single-architecture child digest and forbids a fabricated one, and no registry was reachable from this run to resolve a manifest-list digest. `validate_task.py` treats an absent images table as legal. The harness operator should fill it from the digests the first `docker build` resolves.
- **Thirty-two checklist obligations were dropped** rather than shipped ungraded. Each is listed in `_spec/<code>/00-decisions.md` under the declared-but-ungraded record, with the channel that would have had to observe it. This is the OPEN-DECISIONS D-H escalation, not a silent drop.

## Budget

`turns_expected = 200`, `tokens_expected = 8000000`. The task carries nine must-have features across two providers with an authorization decision that has to be right on five distinct seeded shapes, so it sits at the top of the Standard tier band rather than the middle.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION   (one red gate: G46 placement, recorded above)
```

NOT ADMISSIBLE. The bundle carries no reference app. Nothing counts toward corpus targets until the app is built downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
