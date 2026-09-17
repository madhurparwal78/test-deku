# Build report

## Identity

| | |
|---|---|
| Task code | `E_custo_mess_agentic-support-workspace-vb_20260916_063029` |
| Task id | `deku/agentic-support-workspace-vb` |
| Cell | enterprise / customer-support / messaging-notifications |
| Archetype | `agentic-support-workspace` |
| Variant | `b` (a companion document was supplied: `config/corpus-targets.yaml` `companion_variant`) |
| Variant axes | `critical_depth`, `spec_sections_given` |
| Service profile | `P2-db-email` |
| Providers per slot | `backend` = postgres, `email` = mailpit |
| Language | typescript |
| `spec_sections_given` | overview, roles, features, flow, uiux, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field, revision of 2026-09-16 |
| Vendored grader | 0.22.0 |
| Target schema | 1.4 |

The Task Order named `domain: it-service-management` and `pattern: messaging-inbox`.
Neither is a member of the closed taxonomy, so each was mapped to its nearest legal
enum member before the mint: `customer-support` and `messaging-notifications`. The
mapping is recorded here rather than applied silently.

## Derived-design draws

Every value below descends from SHA-256 over the archetype, per reference/L L.4.

```
draw: render_model = ssr-islands
draw: backend = Express
draw: frontend = SvelteKit
draw: nav = top-nav
draw: work_surface = queue-list
draw: create_flow = modal
draw: feedback = inline-banner
draw: design_direction = companion
draw: launch_surface = alt_text,custom_404,favicon,mobile_viewport,social_preview
```

`design_direction` is `companion` rather than the drawn `clinical-precision`:
reference/L L.6.1 hands the axis to the supplied document, so the eight-token bank's
distinctive phrases no longer govern and G51 carries the real design instead.

`draw: nav = top-nav` is OVERRIDDEN to the companion's measured navigation, a narrow
permanent icon rail. Rule 0 of "Supplied source documents" governs: the draws fill
only what the companion leaves silent, and the companion is not silent here. The
override is recorded in `spec/00-decisions.md`. The public help surface keeps a top
navigation bar, which is what the companion measured for its public pages.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Shared omnichannel inbox, six views, three empty states | INCLUDED | `## Core features`, C-CF-07..C-CF-18 | the Task Order's central surface |
| Conversation thread of typed parts, two composer modes | INCLUDED | `## Core features`, C-CF-19..C-CF-29 | carries the agent's reasoning inline, which the companion shows |
| Auto Agent: retrieval, reasoning, tools, approval ceiling, handover | INCLUDED | `## Core features`, C-CF-30..C-CF-39 | the archetype's defining feature |
| Governed knowledge: collections, versions, audiences, gap queue | INCLUDED | `## Core features`, C-CF-40..C-CF-43 | the agent answers only from published articles |
| Service level policies, timer, sweep, breach | INCLUDED | `## Core features`, C-CF-44..C-CF-47 | the Task Order's resolution targets |
| Invitation, acceptance, role change, routing | INCLUDED | `## Core features`, C-CF-48..C-CF-56 | the Task Order's named administrator workflow |
| Two mail transitions, single recipient each | INCLUDED | `## Core features`, C-CF-57..C-CF-61 | the pattern's critical focus |
| Resolution report scoped by reach | INCLUDED | `## Core features`, C-CF-62..C-CF-65 | the Task Order's manager job |
| Public help surface, metadata, not-found page | INCLUDED | `## Core features`, C-CF-66..C-CF-67 | carries three of the five drawn launch-surface tokens |
| Onboarding checklist, sample data, audit record | INCLUDED | `## Core features`, C-CF-68..C-CF-69 | the companion's first-run section |
| Marketing site and its four measured routes | DROPPED | waived at G51 | outside the Task Order's subject |
| Billing, trials, plans, invoices, spend caps | DROPPED | waived at G51 | no payments slot; outside the Task Order |
| Outbound campaigns, proactive messages, ratings | DROPPED | waived at G51 | outside the Task Order |
| Public interface, apps, integrations, webhooks, events | DROPPED | waived at G51 | no partner_api slot exists in the profile |
| Federated identity, provisioning, second factors | DROPPED | waived at G51 | no auth slot in `P2-db-email` |
| Residency, erasure, legal hold, export | DROPPED | waived at G51 | outside the Task Order |
| Tickets as a separate configurable record, trackers | DROPPED | `## Constraints` | the conversation's own state carries the work |
| Realtime transport, presence over a socket | DROPPED | `## Constraints` | no realtime slot; `soketi` is UNRESOLVED in reference/C C.2.1 |
| Attachments, storage, translation, merging | DROPPED | `## Constraints` | no storage slot in the profile |

Every DROPPED row is declared to G51 with `--waive` and appears in the companion
carry table in `spec/00-decisions.md`, so each is a recorded decision rather than an
omission.

## Slot obligations

| Slot | Provider | Status | Evidence |
|---|---|---|---|
| `backend` | postgres | MET | critical pytest substep `test_repeating_one_client_key_appends_a_single_stored_part`; slot vocabulary present in test names (`stored`, `row`, `seeded`, `persist`) |
| `email` | mailpit | MET | critical pytest substep `test_the_invitation_mail_reaches_the_invited_address_only`; slot vocabulary present (`mail`, `invitation`, `handover`) |

## Grading channels

| | Count |
|---|---|
| Workflows | 23 (band 13 to 23) |
| Browser substeps | 28 |
| Pytest substeps | 60 |
| Critical substeps | 23 |
| Non-happy-path workflow ids | `duplicate_invitation_leaves_a_single_live_invitation`, `invitation_to_an_existing_member_is_invalid_and_is_rejected`, `teammate_cannot_reach_a_conversation_outside_their_teams`, `teammate_cannot_open_settings_or_invite_anybody`, `elevated_role_assignment_is_denied_at_the_server`, `unauthenticated_request_is_denied_on_every_workspace_endpoint`, `duplicate_send_with_one_client_key_appends_one_part`, `concurrent_claims_of_one_conversation_leave_one_assignee`, `duplicate_agent_trigger_creates_no_second_run`, `an_invalid_part_kind_is_refused_and_the_thread_is_unchanged` |
| Pytest module | `tests/test_output.py`, one module, 60 tests |
| Sections covered | core features, authorization, data integrity, edge cases, email |
| Category mix | core_outcome 6, data_integrity 14, security 18, business_rule 12, validation 2, notification 3, presentation 5 |
| Rubric criteria | 17, all positive |
| Positive / negative split | 17 / 0 |

### Rubric dimension shares against the frozen budget

| Dimension | Target | Share | Criteria |
|---|---|---|---|
| `instruction_following` | 0.30 | 0.326 | 4 |
| `functionality` | 0.25 | 0.256 | 3 |
| `ux_flow` | 0.15 | 0.140 | 2 |
| `ui_visual` | 0.15 | 0.140 | 2 |
| `motion` | 0.05 | 0.047 | 2 |
| `accessibility` | 0.05 | 0.047 | 2 |
| `responsiveness` | 0.05 | 0.047 | 2 |

Every share sits inside the 0.10 tolerance `rubric_lint.py` enforces. The three
small dimensions carry criteria because the brief states something measurable about
each: motion character and the reduced-motion rule, the WCAG AA contrast floor and
the keyboard path, and the narrow-viewport plus touch-target bars.

## Coverage

`solution/checklist.md` carries 182 items across nine section codes. G24 reports the
join complete in both directions: every `C-XX-NN` is covered by at least one workflow
substep, pytest test or rubric criterion, and every grader citation resolves to a real
item. `tests/traceability-matrix.md` and `.csv` are regenerated by every sweep from
that same scan.

| Section | Obligation sentences | Items |
|---|---|---|
| Overview | 3 | 4 |
| User roles | 1 | 12 |
| Core features | 28 | 69 |
| User flow | 9 | 14 |
| UI and UX notes | 21 | 32 |
| Technical requirements | 6 | 11 |
| Data model | 8 | 16 |
| Constraints | 3 | 6 |
| Deployment contract | 14 | 18 |

## Literals ledger

125 entries, each verified present in every carrier it declares and absent from the
brief where `verifier_only` is true.

| Class | Count | Examples |
|---|---|---|
| `account` | 4 | `admin@example.com`, `manager@example.com`, `teammate@example.com`, `teammate2@example.com` |
| `credential` | 2 | `deku-demo-pw-2026` (brief + graders), `deku_admin` (verifier only) |
| `route` | 8 | `/signin`, `/help`, `/w/northwind/inbox`, `/w/northwind/reports` |
| `endpoint` | 23 | `/api/health`, `/api/conversations`, `/api/reports/resolution`, `access_token`, `client_key` |
| `status` | 42 | `open`, `snoozed`, `closed`, `on_track`, `at_risk`, `breached`, every `conversation_part.kind` |
| `number` | 5 | `5000`, `60`, `480`, `2000`, `usd` |
| `seed_record` | 21 | `Northwind Trading`, `Billing Support`, `Refund for duplicate charge`, `Standard support` |
| `scheme` | 13 | `Support workspace invitation:`, `Handover needed:`, `Auto Agent's thoughts (Step 1)`, `CONTENT GAP` |
| `env_var` | 9 | `DATABASE_URL`, `SMTP_HOST`, `APP_PUBLIC_URL`; `DB_ADMIN_URL` and `EMAIL_INBOX_API_URL` verifier only |

## Spec folder

Authoring side only, at `_spec/E_custo_mess_agentic-support-workspace-vb_20260916_063029/`,
outside the bundle per CON-5.

| Document | Feeds |
|---|---|
| `00-decisions.md` | the draws, the R1 judgment calls, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing: `## Build plan` is not emitted at this variant |

## Grading window

`window_lint.py` reports length, never fails on it. The brief has no length limit
(generate_instruction.md 4), so graded rules were front-loaded rather than cut.

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Core features | ~22,600 | 2,400 | past-slice |
| User flow | ~5,400 | 1,900 | past-slice |
| UI/UX notes | ~15,600 | 1,700 | past-slice |
| Constraints | ~1,300 | 800 | over-reference |
| User roles | ~3,300 | 1,000 | past-slice |
| Overview | ~2,400 | 700 | over-reference |

The cost of a past-slice section is a diagnostic number the judge computes from less
context. `judge_score` never touches reward, so no reward-driving rule was traded for
the window.

## Kit gate log

Rendered from `_handoff/E_custo_mess_agentic-support-workspace-vb_20260916_063029.gates.jsonl`.
No verdict below was written by hand.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS |
| `G1/G12` | `layout_lint.py` | 0 | PASS |
| `G46` | `structure_lint.py` | 0 | PASS |
| `G50` | `docker_lint.py` | 0 | PASS |
| `G55` | `runtime_deps_lint.py` | 0 | PASS |
| `G63` | `secret_lint.py` | 0 | PASS |
| `G48` | `truth_lint.py` | 0 | PASS |
| `G51` | `source_lint.py` | 0 | PASS |
| `G52` | `rubric_context_lint.py` | 0 | PASS |
| `G54` | `comment_lint.py` | 0 | PASS |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS |
| `G11` | `leak_scan.py` | 0 | PASS |
| `G33` | `window_lint.py` | 0 | PASS |
| `G4/G5` | `contract_lint.py` | 0 | PASS |
| `G43` | `prescription_lint.py` | 0 | PASS |
| `G44` | `disclosure_lint.py` | 0 | PASS |
| `G10` | `no_sdk_lint.py` | 0 | PASS |
| `G31` | `determinism_lint.py` | 0 | PASS |
| `G14` | `reward_path_lint.py` | 0 | PASS |
| `G27/G30` | `rubric_lint.py` | 0 | PASS |
| `G41` | `flag_lint.py` | 0 | PASS |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS |
| `G59/G60` | `codequality_lint.py` | 2 | NOT-APPLICABLE |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS |
| `G6` | `fixture_lint.py` | 0 | PASS |
| `G24` | `coverage_map.py` | 0 | PASS |
| `G37` | `checklist_qc.py` | 0 | PASS |
| `G39` | `rubric_align_lint.py` | 0 | PASS |
| `G28/G29` | `channel_lint.py` | 0 | PASS |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN |
| `G0/INV5` | `vendor_check.py` | 0 | PASS |
| `G47` | `output_qc.py` | 0 | PASS |

`G38` (`kit_selftest.py`) is per kit revision rather than per task: PASS over 32
checks.

`G59/G60` is NOT-APPLICABLE: the bundle carries no `evaluation_target: "source"`
criterion, because the vendored `recompute.py` renders `judged_criteria` only and
`tests/rubric.json` is GENERATED. Stage 3.6 names this state as legal and asks that
it be declared, which this line does.

`G40` is WARN rather than PASS. Every certification prompt carries a current,
bundle-bound receipt with the full scorecard its own registry declares, and each is
recorded SELF-ATTESTED: the same agent authored the artifacts and ran the QC prompts,
so the kit's owner != verifier rule is unmet and is reported rather than claimed.

## Findings recorded in the prompt receipts

| Check | State | Finding |
|---|---|---|
| `QC_instruction.md` A1 | WARN | Ten of the eleven canonical H2 sections are present. `## Build plan` is absent by design: generate_instruction.md 2.1 forbids it at baseline. |
| `QC_instruction.md` C5 | WARN | The Data model states concurrency invariants as observable properties rather than as named index constructs. C5 asks for the DDL form; INV9 and G43 ban that vocabulary mechanically. |
| `QC_instruction.md` C7 | WARN | Four sections and the joined total run past the judge's slice. The brief has no length limit and past-slice is information, not a finding. |
| `QC_spec.md` B1 | WARN | Three roles instead of the pattern row's one, recorded as an R1 judgment call: the Task Order names an administrator, a teammate and managers, and one role expresses none of the three workflows. |
| `QC_spec.md` S5 | WARN | The UI/UX spec carries colour as family, tone and shade rather than as literal values, because the settled number rule forbids a hex anywhere in the brief. |

Nothing above is a Critical or an outstanding High.

## Blocking findings

```
NONE for the static phase. The one operator prerequisite is the absent
[delivery.images] digest block, recorded in the handoff contract: reference/C C.4
forbids a fabricated digest and the kit has no registry access, so the operator
resolves the three manifest-list digests.
```

## Budget

| | |
|---|---|
| `turns_expected` | 180 |
| `tokens_expected` | 6,500,000 |

Reasoning: three roles with relationship-scoped reach, an agent runtime with a
retrieval path and an approval ceiling, a versioned knowledge store, service level
timers, two mail transitions with a single-recipient rule, a report scoped by reach,
and a public help surface with its own metadata. That is nine distinct subsystems
plus a design direction derived from a measured companion, which sits above the
medium band and below the ceiling of 8,000,000.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing here counts toward corpus targets until the reference app is
built downstream from `solution/checklist.md` and `harbor run -a oracle` returns
`1.0` twice.
