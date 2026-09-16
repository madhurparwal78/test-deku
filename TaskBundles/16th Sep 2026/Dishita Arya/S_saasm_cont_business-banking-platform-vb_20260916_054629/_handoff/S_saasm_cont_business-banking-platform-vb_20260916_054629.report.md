# Build report -- S_saasm_cont_business-banking-platform-vb_20260916_054629

Rendered from `_handoff/S_saasm_cont_business-banking-platform-vb_20260916_054629.gates.jsonl`. No verdict on this page was typed by hand.

## Identity

| | |
|---|---|
| Task code | `S_saasm_cont_business-banking-platform-vb_20260916_054629` |
| Task id | `deku/business-banking-platform-vb` |
| Cell | solo_founder / saas-micro-tools / content-publishing |
| Archetype | `business-banking-platform` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Service profile | `P4-db-storage` |
| Providers | `backend = postgres`, `storage = minio` |
| Language | `python` |
| Design direction | `companion` (a PRD was supplied, so reference/L L.6.1 hands the character to it) |
| Launch surface | `colour_contrast, favicon, meta_tags, no_broken_links, single_cta` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Verifier mode | `separate` (the kit default since 11eaf7b; the grader builds its own image from `tests/Dockerfile`) |
| Exit state | MECHANICALLY-GREEN except G46, NO-SOLUTION |

## Gate log

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | ? |
| G1/G12 | `layout_lint.py` | 0 | ? |
| G46 | `structure_lint.py` | 1 | ? |
| G50 | `docker_lint.py` | 0 | ? |
| G55 | `runtime_deps_lint.py` | 0 | ? |
| G63 | `secret_lint.py` | 0 | ? |
| G48 | `truth_lint.py` | 0 | ? |
| G51 | `source_lint.py` | 0 | ? |
| G52 | `rubric_context_lint.py` | 0 | ? |
| G54 | `comment_lint.py` | 0 | ? |
| G17 | `secret_hygiene_lint.py` | 0 | ? |
| G11 | `leak_scan.py` | 0 | ? |
| G33 | `window_lint.py` | 0 | ? |
| G4/G5 | `contract_lint.py` | 0 | ? |
| G43 | `prescription_lint.py` | 0 | ? |
| G44 | `disclosure_lint.py` | 0 | ? |
| G10 | `no_sdk_lint.py` | 0 | ? |
| G31 | `determinism_lint.py` | 0 | ? |
| G14 | `reward_path_lint.py` | 0 | ? |
| G27/G30 | `rubric_lint.py` | 0 | ? |
| G41 | `flag_lint.py` | 0 | ? |
| G56/G57/G58 | `if_lint.py` | 0 | ? |
| G59/G60 | `codequality_lint.py` | 2 | NOT-APPLICABLE |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | ? |
| G6 | `fixture_lint.py` | 0 | ? |
| G24 | `coverage_map.py` | 0 | ? |
| G37 | `checklist_qc.py` | 0 | ? |
| G39 | `rubric_align_lint.py` | 0 | ? |
| G28/G29 | `channel_lint.py` | 0 | ? |
| G40 | `prompt_receipt_lint.py` | 0 | ? |
| G0/INV5 | `vendor_check.py` | 0 | ? |
| G47 | `output_qc.py` | 1 | ? |

### Red gates


## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| The marketing and documentation site | INCLUDED | instruction.md ## Core features | the Task Order's own subject |
| The disclosure layer and the footnote registry | INCLUDED | ## Core features, ## Front-end specification | companion section 8, normative on every route |
| One fee source behind pricing, the schedule and the support answers | INCLUDED | ## Core features | companion sections 8.4, 11.2, 18, 28.22 |
| The account application to a decision | INCLUDED | ## Core features, ## User flow | the Task Order ends on it |
| The append-only ledger with derived balances | INCLUDED | ## Core features, ## Data model | companion section 19, the decision everything rests on |
| Accounts, two balances, holds, interest, sweep | INCLUDED | ## Core features | companion section 20 |
| Six payment rails with returns, cutoffs and a calendar | INCLUDED | ## Core features | companion section 21 |
| Cards: authorisation, clearing, disputes | INCLUDED | ## Core features | companion section 22 |
| The developer interface, events, webhooks and agent tokens | INCLUDED | ## Core features | companion sections 10 and 23 |
| Onboarding, screening and retention | INCLUDED | ## Core features | companion section 24 |
| Approvals, roles and spend controls | INCLUDED | ## User roles, ## Core features | companion section 25 |
| Reconciliation, statements and the audit chain | INCLUDED | ## Core features | companion section 26 |
| The editorial surface behind the site | INCLUDED | ## Core features | the pattern's critical focus needs a draft that is not publicly readable |
| The nine-phase build order | DROPPED | waived in 00-decisions.md | a build order is a work order; ## Build plan is not emitted at variant b |
| The named CSS keyframes and design tokens | DROPPED | carried as words instead | the tasker's direction: describe the moment, never the mechanism name or the value |
| The failure-mode diagnosis columns | DROPPED | the correct behaviour each row prescribes is carried | carrying the diagnosis would state the exam |
| Real audio, a real processor, a real KYC or sanctions vendor | DROPPED | ## Constraints | outside the two declared slots; modelled inside the app |

## Slot obligations

| Slot | Provider | State | Evidence |
|---|---|---|---|
| backend | postgres | MET | `test_seeded_organisations_and_bank_accounts_are_stored_rows` is critical and reads rows out of PostgreSQL |
| storage | minio | MET | `test_uploaded_formation_document_lands_in_the_object_store_at_its_key` is critical and asserts the object exists under its pinned key |

## Grading channels

| | |
|---|---|
| Workflows | 16 |
| Browser substeps | 29 |
| Pytest substeps | 66 |
| Critical substeps | 22 |
| Non-happy-path workflow ids | `concurrent_postings_and_ledger_edits_rejected`, `cross_organisation_statement_download_denied`, `duplicate_idempotency_key_creates_one_payment`, `editor_publishes_and_the_draft_is_denied_to_a_visitor`, `initiator_and_bookkeeper_cannot_move_money` |
| Pytest module | `tests/test_output.py`, 66 tests, covering core features, data integrity, authorization and edge cases across both declared slots |
| Checklist items | 319 |

## Rubric

17 criteria, 15 positive and 2 negative, positive total 41.

| Dimension | Points | Share | Target | Within band |
|---|---|---|---|---|
| instruction_following | 13 | 0.32 | 0.30 | yes |
| functionality | 11 | 0.27 | 0.25 | yes |
| ux_flow | 7 | 0.17 | 0.15 | yes |
| ui_visual | 7 | 0.17 | 0.15 | yes |
| motion | 1 | 0.02 | 0.05 | yes |
| accessibility | 1 | 0.02 | 0.05 | yes |
| responsiveness | 1 | 0.02 | 0.05 | yes |

## Literals ledger

147 entries. By class: account 9, credential 1, design_phrase 11, endpoint 2, env_var 8, motion_moment 7, number 22, route 16, scheme 3, seed_record 15, status 53.

| Value | Class | Verifier only | Carriers |
|---|---|---|---|
| `deku-demo-pw-2026` | credential | no | instruction.md, conftest.py |
| `editor@example.com` | account | no | instruction.md, conftest.py |
| `reader@example.com` | account | no | instruction.md, conftest.py |
| `owner@example.com` | account | no | instruction.md, conftest.py |
| `admin@example.com` | account | no | instruction.md, conftest.py |
| `approver@example.com` | account | no | instruction.md, conftest.py |
| `initiator@example.com` | account | no | instruction.md, conftest.py |
| `bookkeeper@example.com` | account | no | instruction.md, conftest.py |
| `cardholder@example.com` | account | no | instruction.md, conftest.py |
| `owner2@example.com` | account | no | instruction.md, conftest.py |
| `Meridian Robotics` | seed_record | no | instruction.md, conftest.py |
| `meridian-robotics` | seed_record | no | instruction.md, conftest.py |
| `Calder Textiles` | seed_record | no | instruction.md, conftest.py |
| `calder-textiles` | seed_record | no | instruction.md, conftest.py |
| `Meridian Operating` | seed_record | no | instruction.md, conftest.py |
| `Meridian Treasury` | seed_record | no | instruction.md, conftest.py |
| `Meridian Card` | seed_record | no | instruction.md, conftest.py |
| `Calder Operating` | seed_record | no | instruction.md, conftest.py |
| `Northgate Bank` | seed_record | no | instruction.md, conftest.py |
| `Talbot National` | seed_record | no | instruction.md, conftest.py |
| `Jane Black` | seed_record | no | instruction.md, conftest.py |
| `rcpt_4d82e1af` | seed_record | no | instruction.md, conftest.py |
| `Viktor Halberd` | seed_record | no | instruction.md, conftest.py |
| `rcpt_9c11b7d3` | seed_record | no | instruction.md, conftest.py |
| `Treasury sweep explained` | seed_record | no | instruction.md, conftest.py |
| `/products/treasury-sweep` | route | no | instruction.md, conftest.py |
| `wire_outgoing_domestic` | status | no | instruction.md, conftest.py |
| `wire_outgoing_international` | status | no | instruction.md, conftest.py |
| `ach_outgoing` | status | no | instruction.md, conftest.py |
| `realtime_outgoing` | status | no | instruction.md, conftest.py |
| `cheque_outgoing` | status | no | instruction.md, conftest.py |
| `card_replacement` | status | no | instruction.md, conftest.py |
| `monthly_maintenance` | status | no | instruction.md, conftest.py |
| `draft` | status | no | instruction.md, conftest.py, test_output.py |
| `pendingApproval` | status | no | instruction.md, conftest.py |
| `approved` | status | no | instruction.md, conftest.py, test_output.py |
| `scheduled` | status | no | instruction.md, conftest.py, test_output.py |
| `submitted` | status | no | instruction.md, conftest.py, test_output.py |
| `settled` | status | no | instruction.md, conftest.py, test_output.py |
| `failed` | status | no | instruction.md, conftest.py, test_output.py |
| `returned` | status | no | instruction.md, conftest.py, test_output.py |
| `cancelled` | status | no | instruction.md, conftest.py |
| `recallRequested` | status | no | instruction.md, conftest.py |
| `internal` | status | no | instruction.md, conftest.py, test_output.py |
| `ach` | status | no | instruction.md, conftest.py, test_output.py |
| `wire` | status | no | instruction.md, conftest.py, test_output.py |
| `realtime` | status | no | instruction.md, conftest.py, test_output.py |
| `cheque` | status | no | instruction.md, conftest.py |
| `card` | status | no | instruction.md, conftest.py, test_output.py |
| `insufficient_funds` | status | no | instruction.md, conftest.py, test_output.py |
| `account_closed` | status | no | instruction.md, conftest.py, test_output.py |
| `unauthorised` | status | no | instruction.md, conftest.py |
| `notification_of_change` | status | no | instruction.md, conftest.py |
| `customer_deposit` | status | no | instruction.md, conftest.py, test_output.py |
| `in_transit` | status | no | instruction.md, conftest.py, test_output.py |
| `fee_income` | status | no | instruction.md, conftest.py |
| `interest_expense` | status | no | instruction.md, conftest.py |
| `card_authorisation_hold` | status | no | instruction.md, conftest.py |
| `returns_suspense` | status | no | instruction.md, conftest.py |
| `partner_bank_settlement` | status | no | instruction.md, conftest.py |
| `unmatched_clearing` | status | no | instruction.md, conftest.py |
| `rounding_residual` | status | no | instruction.md, conftest.py |
| `timing` | status | no | instruction.md, conftest.py |
| `amount` | status | no | instruction.md, conftest.py, test_output.py |
| `missing` | status | no | instruction.md, conftest.py, test_output.py |
| `unexpected` | status | no | instruction.md, conftest.py, test_output.py |
| `operating` | status | no | instruction.md, conftest.py, test_output.py |
| `treasury` | status | no | instruction.md, conftest.py, test_output.py |
| `credit` | status | no | instruction.md, conftest.py, test_output.py |
| `debit` | status | no | instruction.md, conftest.py |
| `published` | status | no | instruction.md, conftest.py, test_output.py |
| `owner` | status | no | instruction.md, conftest.py, test_output.py |
| `admin` | status | no | instruction.md, conftest.py |
| `approver` | status | no | instruction.md, conftest.py, test_output.py |
| `initiator` | status | no | instruction.md, conftest.py, test_output.py |
| `bookkeeper` | status | no | instruction.md, conftest.py, test_output.py |
| `card_only` | status | no | instruction.md, conftest.py |
| `usd` | status | no | instruction.md, conftest.py |
| `USD` | status | no | instruction.md, conftest.py |
| `1000000` | number | no | instruction.md, conftest.py, test_output.py |
| `1500` | number | no | instruction.md, conftest.py |
| `2500` | number | no | instruction.md, conftest.py, test_output.py |
| `150` | number | no | instruction.md, conftest.py |
| `500` | number | no | instruction.md, conftest.py, test_output.py |
| `4000` | number | no | instruction.md, conftest.py |
| `4800` | number | no | instruction.md, conftest.py |
| `120` | number | no | instruction.md, conftest.py |
| `10` | number | no | instruction.md, conftest.py, test_output.py |
| `24` | number | no | instruction.md, conftest.py, test_output.py |
| `25000000` | number | no | instruction.md, conftest.py, test_output.py |
| `420` | number | no | instruction.md, conftest.py |
| `365` | number | no | instruction.md, conftest.py |
| `200,000` | number | no | instruction.md, conftest.py |
| `4.20%` | number | no | instruction.md, conftest.py |
| `16:30` | number | no | instruction.md, conftest.py |
| `15:00` | number | no | instruction.md, conftest.py |
| `America/New_York` | scheme | no | instruction.md, conftest.py |
| `2026-11-26` | number | no | instruction.md, conftest.py |
| `2026-12-25` | number | no | instruction.md, conftest.py |
| `2026-09-01` | number | no | instruction.md, conftest.py |
| `2026-09-15` | number | no | instruction.md, conftest.py, test_output.py |
| `2026-08` | number | no | instruction.md, conftest.py |
| `vault/{kind}/{owner_id}/{sha256_of_bytes}.{ext}` | scheme | no | instruction.md |
| `Idempotency-Key` | scheme | no | instruction.md, conftest.py |
| `/developers` | route | no | instruction.md, conftest.py, test_output.py |
| `/pricing` | route | no | instruction.md, conftest.py, test_output.py |
| `/faq` | route | no | instruction.md, conftest.py, test_output.py |
| `/apply` | route | no | instruction.md, test_output.py |
| `/login` | route | no | instruction.md, test_output.py |
| `/studio` | route | no | instruction.md, conftest.py |
| `/legal/fees` | route | no | instruction.md, conftest.py, test_output.py |
| `/sitemap.xml` | route | no | instruction.md, test_output.py |
| `/robots.txt` | route | no | instruction.md, test_output.py |
| `/favicon.ico` | route | no | instruction.md, test_output.py |
| `/app/payments/new` | route | no | instruction.md |
| `/app/statements` | route | no | instruction.md, conftest.py |
| `/app/reconciliation` | route | no | instruction.md |
| `/app/audit` | route | no | instruction.md, conftest.py |
| `/app/agents` | route | no | instruction.md |
| `/api/health` | endpoint | no | instruction.md |
| `/api` | endpoint | no | instruction.md |
| `APP_PUBLIC_URL` | env_var | no | instruction.md |
| `APP_PUBLIC_PORT` | env_var | no | instruction.md |
| `DATABASE_URL` | env_var | no | instruction.md |
| `STORAGE_ENDPOINT` | env_var | no | instruction.md |
| `STORAGE_BUCKET` | env_var | no | instruction.md |
| `STORAGE_ACCESS_KEY` | env_var | no | instruction.md |
| `STORAGE_SECRET_KEY` | env_var | no | instruction.md |
| `A U R E L I A` | design_phrase | no | instruction.md, conftest.py |
| `Radically different banking` | design_phrase | no | instruction.md, conftest.py |
| `Enter your email` | design_phrase | no | instruction.md, conftest.py |
| `Open account` | design_phrase | no | instruction.md, conftest.py |
| `Launch demo` | design_phrase | no | instruction.md, conftest.py |
| `Get started fast. And never stop moving.` | design_phrase | no | instruction.md, conftest.py |
| `Programmable finances for developers & agents` | design_phrase | no | instruction.md, conftest.py |
| `Install CLI` | design_phrase | no | instruction.md, conftest.py |
| `Skip to main content` | design_phrase | no | instruction.md, conftest.py |
| `500: Internal Server Error` | design_phrase | no | instruction.md, conftest.py |
| `Real-time payments are here - instant, free, 24/7/365.` | design_phrase | no | instruction.md, conftest.py |
| `rises a short distance while fading up` | motion_moment | no | instruction.md |
| `fades while blurring slightly` | motion_moment | no | instruction.md |
| `backwards tilt from its top edge` | motion_moment | no | instruction.md |
| `ripple spreads and fades` | motion_moment | no | instruction.md |
| `notes fall the height of the page` | motion_moment | no | instruction.md |
| `passing behind the centre` | motion_moment | no | instruction.md |
| `grain drifts across a section ground` | motion_moment | no | instruction.md |
| `DB_ADMIN_URL` | env_var | yes | task.toml |

## Spec folder

Written to `output_16sep/_spec/S_saasm_cont_business-banking-platform-vb_20260916_054629/`, never inside the bundle.

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the taxonomy call, the companion carry table |
| `01-PRD.md` | ## Overview, ## Core features, ## Constraints |
| `02-TRD.md` | ## Technical requirements |
| `03-app-flow.md` | ## User flow |
| `04-uiux-brief.md` | ## UI/UX notes, ## Front-end specification |
| `05-backend-schema.md` | ## Data model, ## User roles |
| `06-implementation-plan.md` | nothing: ## Build plan is not emitted at variant b |

## Grading window

| Section | Chars | Reference |
|---|---|---|
| Core features | 31242 | 2400 |
| User flow | 8252 | 1900 |
| UI/UX notes | 11419 | 1700 |
| Constraints | 1738 | 800 |
| User roles | 3173 | 1000 |
| Overview | 2667 | 700 |
| **joined** | **58491** | **8800** |

The brief carries no length limit (G33 reports, never fails). The overflow costs the judge's view of the tail, never reward: `judge_score` is advisory and the criteria are self-contained. `tests/traceability-matrix.md` and `tests/traceability-matrix.csv` carry the requirement-to-grader table and are regenerated by every sweep.

