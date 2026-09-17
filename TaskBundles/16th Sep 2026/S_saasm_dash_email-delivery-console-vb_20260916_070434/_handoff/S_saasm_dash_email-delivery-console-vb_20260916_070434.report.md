# Build report - S_saasm_dash_email-delivery-console-vb_20260916_070434

| | |
|---|---|
| Task code | `S_saasm_dash_email-delivery-console-vb_20260916_070434` |
| Task id | `deku/email-delivery-console-vb` |
| Cell | solo_founder / saas-micro-tools / dashboard-analytics |
| Service profile | `P2-db-email` |
| Providers per slot | db -> `postgres` (postgres:16.4-bookworm) · email -> `mailpit` (axllent/mailpit:v1.30.6) |
| Variant | `b` · variant_axes `critical_depth`, `spec_sections` |
| Language | `python` (Flask backend, Svelte + Vite frontend) |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Minted | 2026-09-16T07:04:34Z |
| Kit | deku-green-field, 00-RUN.md pipeline |
| Vendored grader | 0.22.0 |
| Target schema | 1.4 |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Alignment with the kit pull of 2026-09-16 (5 commits, 1b99060..806eb0a)

| Commit | Change in the kit | What changed in this bundle |
|---|---|---|
| `1b99060` | `code_quality` joins the authored code-quality dimensions | nothing: the bundle carries no `evaluation_target: "source"` criteria, so G59/G60 stay NOT-APPLICABLE |
| `da24d3b` | the section pytest module is named `test_output.py`; the generated compiled-rubric file becomes `test_ans.py` | `tests/test_pytest.py` renamed to `tests/test_output.py`; every `workflows.yaml` test id, the `tests/Dockerfile` COPY line, the pytest-provenance `module` and the literals-ledger carriers follow; `solution/trinity/test_output.py` regenerated as `test_ans.py` |
| `11eaf7b` | `[verifier].environment_mode = "separate"` is the default | `task.toml` switched from `"shared"` to `"separate"`. The three tests that read the agent's filesystem were replaced by observable deployment-contract checks (see below) |
| `78e5ba6` | vendored `test.sh` stripped of comments and re-pinned | `tests/test.sh` re-copied from `vendor/grader-0.22.0`; `vendor_check` PASS against the re-minted manifest |
| `806eb0a` | `solution/USER_README.md` restored as a GENERATED file (truth-generator-7) | `solution/trinity/recompute.py` re-copied and re-run; `solution/USER_README.md` now carries the seeded literals and the canary |

**Three tests replaced.** `test_sign_in_credentials_are_written_to_the_app_readme`,
`test_a_reserved_screenshots_directory_exists_empty` and
`test_a_reserved_downloads_directory_exists_empty` read `/app` directly. That already broke
`pytest_generator.md`'s isolation rule ("No filesystem inspection of the agent's tree"), and
under separate mode the verifier container has no `/app` to read. They are replaced by
`test_every_list_endpoint_returns_a_top_level_json_array`,
`test_login_signup_health_answer_without_a_bearer_token` and
`test_the_log_reflects_message_rows_stored_in_the_named_datastore`, which grade three
`## Deployment contract` statements that ARE observable. Checklist items C-DC-05, C-DC-06 and
C-DC-07 were re-pointed to match, and the three filesystem obligations are recorded as declared
but ungraded under OPEN-DECISIONS D-H in the handoff contract.

**Receipts.** `qc_toml.md` changed (VERIF-001 now expects `"separate"`), so its receipt went
stale and was re-issued after re-reading the row. VERIF-005 now carries a WARN naming the
`localhost` fallback under separate mode. `qc_docker` DEP-011 is NOT-APPLICABLE under separate
mode. No other certification prompt changed bytes.

**Not changed.** The environment Dockerfile still installs the grader's Python packages.
Under separate mode the agent image no longer owes them, but `docker_generator.md` was not
updated in this pull and still emits them, so they are kept to match what the kit generates.

## Input

A five-field Task Order plus a companion PRD (`Prds/resend_prd.md`, 8,411 lines).

| Field | Supplied | Used |
|---|---|---|
| category | `solo_founder` | `solo_founder` |
| domain | `saas-productivity` | `saas-micro-tools` |
| pattern | `dashboard-analytics` | `dashboard-analytics` |
| archetype | `email-delivery-console` | `email-delivery-console` |
| ql_email | `kaustubh.dalvi@ethara.ai` | `[task].authors[0]` |
| author_email | `ananya.tandon.int43@ethara.ai` | `[task].authors[1]`, `[metadata].contributor_id` |

`saas-productivity` is not a member of the 36-domain enum. The nearest legal cell under
`solo_founder` is `saas-micro-tools`, and the idea sits in it squarely. Recorded as judgment
call 1 in `_spec/S_saasm_dash_email-delivery-console-vb_20260916_070434/00-decisions.md` rather than silently corrected.

`service_profile` is `P2-db-email` rather than the default `P1-db`: the product's subject is
mail delivery, so the email slot carries a real observable side effect and a real grader.

## Derived design values

| Axis | Value | How |
|---|---|---|
| design_direction | `companion` | reference/L S-L.6.1: a companion document beats the draw. Drawn value `terminal-mono` recorded, not governing |
| launch_surface | `custom_404, form_validation, no_broken_links, security_headers, terms_page` | reference/O S-O.3 draw over the archetype |
| render_model | `spa-json-api` | generate_instruction.md S-2.9 draw |
| backend | `Flask` | same digest, offset 8 |
| frontend | `Svelte + Vite` | same digest, offset 16 |
| nav | `sidebar-nav` | S-2.10 draw against the dashboard-analytics legal subset |
| work_surface | `chart-grid` | same |
| create_flow | `dedicated-route` | same |
| feedback | `optimistic-row` | same, written as behaviour rather than as the banned noun |

## Feature resolution

| # | Candidate | Verdict | Where | Reason |
|---|---|---|---|---|
| 1 | Accounts, workspace and three roles | INCLUDED | `## User roles`, `## Core features` | companion S-2.2, S-2.3 |
| 2 | Sending domains and per-record verification | INCLUDED | `## Core features` | companion S-18, S-30 |
| 3 | API credentials, secret shown once | INCLUDED | `## Core features` | companion S-19, S-2.4 |
| 4 | The sending interface with required idempotency | INCLUDED | `## Core features` | companion S-27 |
| 5 | The emails log and the message timeline | INCLUDED | `## Core features` | companion S-17 |
| 6 | The overview counters and delivery chart | INCLUDED | `## Core features` | companion S-16; the pattern's critical focus |
| 7 | Audiences, contacts and broadcasts | INCLUDED | `## Core features` | companion S-21, S-22 |
| 8 | Event notification endpoints and replay | INCLUDED | `## Core features` | companion S-20, S-31 |
| 9 | Usage metering against the allowance | INCLUDED | `## Core features` | companion S-37 |
| 10 | Terms page, not-found page, form validation, internal links, security headers | INCLUDED | `## Core features`, `## Technical requirements` | the drawn launch surface |
| - | Marketing site, thirty-five public routes | DROPPED | `## Constraints` | out of scope; declared to G51 with `--waive` |
| - | Documentation application | DROPPED | `## Constraints` | as above |
| - | Visual broadcast editor, templates, automations | DROPPED | `## Constraints` | as above |
| - | Inbound mail routing | DROPPED | `## Constraints` | companion S-1.5 already scopes it thin |
| - | Payment processor, invoices, dunning | DROPPED | `## Constraints` | no payments slot declared |
| - | Open and click tracking | DROPPED | `## Constraints` | the companion turns both off by default |

Ten features is the top of the six-to-ten band reference/G S-G.2.1 sets for a companion-backed
task. Every one owes a grader and has one; `turns_expected` and `tokens_expected` were raised
with the count.

## Slot obligations

| Slot | Provider | Status | Observed by |
|---|---|---|---|
| db | `postgres` | MET | `test_the_seeded_workspace_rows_persisted_with_three_membership_roles` (critical), plus 14 further row assertions |
| email | `mailpit` | MET | `test_an_ordinary_recipient_receives_real_mail` (critical), read out of band through the inbox capability |

## Grading surface

| | |
|---|---|
| Workflows | 16 (band 10-16) |
| Browser substeps | 32 |
| pytest substeps | 85 |
| Critical substeps | 11 |
| Non-happy-path workflow ids | `duplicate_and_concurrent_sends_admit_at_most_one_message`, `invalid_send_requests_are_refused`, `member_write_actions_are_denied`, `unauthenticated_and_cross_workspace_requests_are_denied`, `cross_workspace_lookup_cannot_be_read`, `usage_metering_stops_at_the_allowance_limit` |
| pytest module | one, `tests/test_output.py`, 85 test functions |
| Sections covered | core features · email slot · authorization · data integrity · technical requirements · deployment contract · constraints · launch surface |
| Rubric criteria | 15, all positive |
| Positive / negative split | 15 / 0 (the brief licenses no negative) |
| Checklist items | 130 across ten section codes |
| Core asks: 10  ·  graders: 115  ·  not fully graded: 0 | see `tests/traceability-matrix.md` |

### Rubric dimension shares (positive scores only)

| Dimension | Target | Actual | Criteria |
|---|---|---|---|
| instruction_following | 0.30 | 0.316 | 4 |
| functionality | 0.25 | 0.228 | 3 |
| ux_flow | 0.15 | 0.140 | 2 |
| ui_visual | 0.15 | 0.158 | 3 |
| motion | 0.05 | 0.053 | 1 |
| accessibility | 0.05 | 0.053 | 1 |
| responsiveness | 0.05 | 0.053 | 1 |

## Literals ledger

62 entries in `_handoff/S_saasm_dash_email-delivery-console-vb_20260916_070434.literals-ledger.json`, every one carried by at least one of
`instruction.md`, `tests/conftest.py`, `tests/test_output.py` or `task.toml`, and every graded
value present verbatim in the brief (G6 PASS, both directions).

Classes: `credential` (1) · `account` (6) · `seed-record` (7) · `literal` (5) ·
`number` (2) · `header` (2) · `status` (14) · `route` (13) · `path` (1) ·
`env-var` (5 agent-visible, 2 verifier-only).

The two verifier-only entries -- `DB_ADMIN_URL` and `EMAIL_INBOX_API_URL` -- appear in
`[verifier].env` and in neither `instruction.md` nor `[environment].env` (INV4, G17 PASS).

## Spec folder

Authored at `Output/16sept_resend/_spec/S_saasm_dash_email-delivery-console-vb_20260916_070434/`, never inside the bundle (CON-5).

| Doc | Feeds |
|---|---|
| `00-decisions.md` | the nine judgment calls and every `draw:` line G49 reads |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | not emitted; variant b did not request `## Build plan` |

## Grading window

Reported, never failed -- the brief has no length limit (G33).

| Section | Chars | Reference | Flag |
|---|---|---|---|
| core_features | 21,517 | 2,400 | past-slice |
| user_flow | 4,082 | 1,900 | past-slice |
| ui_ux_notes | 6,788 | 1,700 | past-slice |
| constraints | 1,246 | 800 | over-reference |
| user_roles | 2,950 | 1,000 | past-slice |
| overview | 1,829 | 700 | over-reference |
| joined | 38,600 | 8,800 | past-slice |

Content past the slice reaches the agent in full and stops reaching the judge. The judged
criteria are self-contained and carry their own `evaluation_rule`, and `judge_score` never
touches reward, so nothing reward-bearing was trimmed to fit.

## Companion carriage (G51)

| | |
|---|---|
| Source | `Prds/resend_prd.md` |
| Colours described by family and tone | 33 / 33 |
| Topics carried | 455 / 455 |
| Enumerated items carried | 1,787 / 1,787 |

Declared waivers -- every one a deliberate omission, on the record:

- `normative versus informational`
- `testimonial`
- `cross-linking`
- `the calculator`
- `currency and tax`
- `machine-readable index`
- `12.9 feedback`
- `22.4 styles`
- `23.3 editing`
- `25.2 setup`
- `choosing the primitive`
- `the outbox`
- `37.4 overage`
- `double-grant race`
- `dunning`
- `vulnerability disclosure`
- `zero-asset substitution guide`
- `pricing, enterprise and the feature routes`
- `taxonomy substitutions`
- `what a second capture should collect`
- `what is specification, not observation`
- `sdkpackage`
- `idpone`
- `partnerone`
- `partnertwo`
- `partnerthree`
- `published price list`
- `/clubs`
- `/insiders`
- `/wallpapers`
- `the logo links /home`
- `woff2`
- `font-display`
- `font-mono`
- `texture-btn.png`
- `.webp`
- `rem calc(`
- `linear-gradient`
- `gray-a3`
- `two arcs`
- `soc 2`
- `cubic-bezier`
- `conic border angle`
- `plop`
- `scroll-x`
- `caret-blink`
- `linkability`
- `in the feed of section`
- `not needed to succeed`
- `inlined styles`
- `currently published version`
- `spam and malware`
- `local forwarding mode`
- `personid`
- `workspaceid`
- `signingsecretref`
- `previewtext`
- `inboundmessage`
- `nextattemptat`
- `enterprise negotiated`
- `enterprise terms`
- `enterprise buyer`
- `traceid`
- `data processing addendum`
- `prefers-reduced-motion`
- `announcement pill`
- `language row`
- `framework row`
- `deliverability heading`
- `blocklist tracking`
- `company branding`
- `attribution 1`
- `attribution 2`
- `attribution 3`
- `third-party controls`
- `image/svg+xml`
- `one revolution over`
- `inline vector graphics`
- `saas-productivity`
- `/pricing and /enterprise`
- `out-of-order processor notification`
- `cancellation is completable`
- `client-side scripting`

## KIT GATE LOG

Rendered from `_handoff/S_saasm_dash_email-delivery-console-vb_20260916_070434.gates.jsonl`. Not transcribed, not authored.

| Gate | Tool | Exit | Verdict | Result | Elapsed | stdout SHA |
|---|---|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | PASS | 0.21s | `fd4a560df098` |
| `G1/G12` | `layout_lint.py` | 0 | PASS | PASS | 0.18s | `18c0992d4f1a` |
| `G46` | `structure_lint.py` | 0 | PASS | PASS | 0.22s | `cc49ae00918c` |
| `G50` | `docker_lint.py` | 0 | PASS | PASS | 0.31s | `380ed7d1c830` |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | PASS | 0.26s | `a0c21dca8bc5` |
| `G63` | `secret_lint.py` | 0 | PASS | PASS | 0.24s | `a77b3f897077` |
| `G48` | `truth_lint.py` | 0 | PASS | PASS | 0.95s | `b5e27ba0267f` |
| `G51` | `source_lint.py` | 0 | PASS | PASS | 0.33s | `36788a9883dc` |
| `G52` | `rubric_context_lint.py` | 0 | PASS | PASS | 0.18s | `5f304656bf8a` |
| `G54` | `comment_lint.py` | 0 | PASS | PASS | 0.25s | `04a625bf4232` |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | PASS | 0.24s | `7f53773a04de` |
| `G11` | `leak_scan.py` | 0 | PASS | PASS | 0.21s | `a05dfe32f8c7` |
| `G33` | `window_lint.py` | 0 | PASS | PASS | 0.15s | `d6f56df0b70b` |
| `G4/G5` | `contract_lint.py` | 0 | PASS | PASS | 0.15s | `2b90c3925585` |
| `G43` | `prescription_lint.py` | 0 | PASS | PASS | 0.26s | `4d54a8b8fad0` |
| `G44` | `disclosure_lint.py` | 0 | PASS | PASS | 0.17s | `2835cb53c644` |
| `G10` | `no_sdk_lint.py` | 0 | PASS | PASS | 0.21s | `9c6e1a2f44d4` |
| `G31` | `determinism_lint.py` | 0 | PASS | PASS | 0.23s | `9ce45f7ab4cc` |
| `G14` | `reward_path_lint.py` | 0 | PASS | PASS | 0.16s | `209a0ad7724e` |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | PASS | 0.17s | `6d4ad3ea86cf` |
| `G41` | `flag_lint.py` | 0 | PASS | PASS | 0.25s | `84f39a4672a5` |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | PASS | 0.22s | `cdf20c83e905` |
| `G59/G60` | `codequality_lint.py` | 2 | ? | PASS | 0.18s | `e23941dd85e0` |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | PASS | 0.38s | `7911c20178cd` |
| `G6` | `fixture_lint.py` | 0 | PASS | PASS | 0.53s | `a2bac7984853` |
| `G24` | `coverage_map.py` | 0 | PASS | PASS | 0.28s | `ee7b882d0f87` |
| `G37` | `checklist_qc.py` | 0 | PASS | PASS | 0.27s | `c3b2e55c8c6e` |
| `G39` | `rubric_align_lint.py` | 0 | PASS | PASS | 0.25s | `20676e8175fa` |
| `G28/G29` | `channel_lint.py` | 0 | PASS | PASS | 0.32s | `2c4674c44cf2` |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | PASS | 0.31s | `8405be3e031a` |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | PASS | 0.22s | `bdb13013dc3b` |
| `G47` | `output_qc.py` | 0 | PASS | PASS | 0.30s | `b69ec2e28375` |

`G59/G60` returns exit 2 NOT-APPLICABLE: the bundle carries no `evaluation_target: "source"`
criteria, which is a real state rather than a gate that failed to run.

`G40` returns WARN: every certification prompt has a current, bundle-bound receipt, and all
seven are SELF-ATTESTED because owner and verifier were one agent. The four generator prompts
(`generate_instruction.md`, `toml_generator.md`, `docker_generator.md`, `pytest_generator.md`,
`solution_checklist.md`, `rubric_author.md`) are advisory and carry no receipt.

## PROMPT RECEIPTS

| Prompt | Gate | Verdict | Checks answered | Findings | Verifier | Token |
|---|---|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | 3 | self | `pr_ce5cfad2` |
| `QC_spec.md` | G34 | PASS | 15 | 4 | self | `pr_baa67ef8` |
| `qc_docker.md` | G35 | PASS | 105 | 1 | self | `pr_949caf8c` |
| `qc_rubric.md` | G53 | PASS | 16 | 0 | self | `pr_d23bd97f` |
| `qc_solution_checklist.md` | G37 | PASS | 0 | 0 | self | `pr_c64a5fdc` |
| `qc_toml.md` | G36 | PASS | 120 | 5 | self | `pr_6fb29706` |
| `task_code_verifier.md` | G3 | VALID | 12 | 0 | self | `pr_cca352bd` |

Ten findings are recorded across the certification scorecards. Every one is a place where two
kit documents disagree and the mechanical gate or the dated decision was followed; each is
written out in full in `_handoff/S_saasm_dash_email-delivery-console-vb_20260916_070434.receipts.json`. In summary:

- `QC_instruction` A1 asks for eleven H2 sections; `generate_instruction.md` S-2.1 retired
  `## Build plan` from the baseline. Ten sections plus `## Front-end specification` emitted.
- `QC_instruction` C4 and `QC_spec` S5 ask for hexes, pixel type scales and millisecond motion
  values; the settled number rule (A5) bans every one of them and keeps only the exact font
  family and size, which is what the brief carries.
- `QC_instruction` C5 and `QC_spec` S6 ask for named index or constraint vocabulary; INV9 and
  G43 forbid it in `## Technical requirements` and `## Data model`, so every concurrency rule
  is stated as an observable invariant instead.
- `QC_spec` S2 caps must-have features at six; reference/G S-G.2.1 raises the cap to ten for a
  companion-backed task and requires a grader for each, which is discharged.
- `QC_spec` B1: the pattern row names one role and the brief carries three, a role-fit rename
  recorded as judgment call 6.
- `qc_toml` SCHEMA-011: `[delivery]` is absent from the generator template and required by
  CON-2, stage-4 and `validate_task.py`. `[delivery.images]` is omitted rather than filled
  with fabricated digests.
- `qc_toml` BENCH-003, BENCH-005 and INT-007 depend on `difficulty`, which holds the mandated
  empty placeholder, so they cannot be decided at authoring time.
- `qc_docker` CMP-011 asks for no published host port; CMP-022 requires one on `main`. Both
  sidecars publish nothing; `main` publishes 4173 because the Critical rule wins.

## HANDOFF GATE LIST (undecided here)

See `_handoff/S_saasm_dash_email-delivery-console-vb_20260916_070434.handoff.md`. G13, G15, G18, G19, G20, G21 and G25 need Docker and the
harness, which this kit does not have (S-2.2).

## BLOCKING FINDINGS

None. No spec gap and no harness gap prevented a required grader.

## Budget

`turns_expected = 200`, `tokens_expected = 7500000`.

Ten features, three roles, two service slots, an idempotency invariant that has to hold under
real concurrency, an aggregate that has to reconcile with its rows, and a companion-backed
visual specification. That is the top of the documented band, and it is set there because the
feature count was raised from the bare-Task-Order cap rather than in spite of it.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`

Not admissible. Nothing counts this bundle toward corpus targets until the reference app lands
downstream and `harbor run -a oracle` returns `1.0` on two consecutive runs.
