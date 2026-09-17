# Build report - E_legal_cont_governed-disclosure-platform-vb_20260916_072244

Rendered from `_handoff/E_legal_cont_governed-disclosure-platform-vb_20260916_072244.gates.jsonl`. No verdict in this file was transcribed by hand.

## Identity

| | |
|---|---|
| task code | `E_legal_cont_governed-disclosure-platform-vb_20260916_072244` |
| task id | `deku/governed-disclosure-platform-vb` |
| cell | enterprise / legal-compliance / content-publishing |
| service profile | `P4-db-storage` |
| providers | backend `postgres`, storage `minio` |
| variant | `b`, axes `critical_depth`, `spec_sections` |
| language | `python` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 (single-operator run) |
| companion | `prds/montfort_prd.md`, 7005 lines, carried under G51 |

## Derived-design draws

SHA-256 over the archetype `governed-disclosure-platform`, per reference/L S.L.4.

| axis | value | note |
|---|---|---|
| render_model | `ssr-islands` | kept as drawn |
| backend | `FastAPI` | kept as drawn |
| frontend | `SolidStart` | kept as drawn |
| design_direction | `companion` | raw draw `brutalist-utility`, overridden by reference/L S.L.6.1 |
| nav | `sidebar-nav` | kept as drawn, agrees with the companion console |
| work_surface | `table-first` | kept as drawn |
| create_flow | `dedicated-route` | kept as drawn |
| feedback | `toast` | kept as drawn |
| launch_surface | cookie_choice, favicon, no_frontend_secrets, single_cta, social_preview | drawn five; the brief carries eight more the companion already stated |

## Feature resolution

| candidate | verdict | file | reason |
|---|---|---|---|
| Auth, sessions and deactivation | INCLUDED | ## Core features / ### Auth | the closed-signup, bearer-token re-cast of companion section 29 |
| Divisions, memberships and the one decision | INCLUDED | ## Core features | companion sections 2, 30, 31; the spine of the brief |
| Records, revisions and the two hashes | INCLUDED | ## Core features, ## Data model | companion section 25; the current/published split is the critical distinction |
| The review chain | INCLUDED | ## Core features | companion section 26; the Task Order names it |
| Disclosure classification and the policy register | INCLUDED | ## Core features | companion section 27; the Task Order names the register |
| Embargo and scheduled publication | INCLUDED | ## Core features | companion sections 26.6 and 36.2; the Task Order names the embargo |
| Media in the object store | INCLUDED | ## Core features | the storage half of the pattern's critical focus |
| The public site | INCLUDED | ## Core features, ## User flow | companion sections 11 to 22 |
| The enquiry form and the visitor's own surfaces | INCLUDED | ## Core features | companion sections 19.4, 23 and 44; carries three drawn launch-surface tokens |
| The audit trail | INCLUDED | ## Core features, ## Data model | companion section 32; the Task Order's provable-mutation property |
| The confidential helpline | DROPPED | spec/00-decisions.md, Scope | not in the Task Order idea, and its three defining controls (region pinning, a separate deployable, a zero-third-party assertion) are unobservable in this environment |
| The live three dimensional scene layer | DROPPED | ## Constraints | waived as geometry; the scroll instrument, the chapter machine, the anchors and the authored no-layer variant are all carried |
| The ambient audio layer | DROPPED | ## Constraints | companion section 10; nothing survives once the bed is gone |
| Federated identity and step-up assurance | DROPPED | ## Constraints | no identity provider in this environment; re-cast to app email and password |
| Outbound webhooks and the event catalogue | DROPPED | ## Constraints | no runtime network; the outbox survives as the atomic publication requirement |
| Notifications by mail and chat | DROPPED | ## Constraints | no email slot; re-cast to in-console only |
| Residency, retention and erasure | DROPPED | ## Constraints | one region, no retention engine |
| Internationalisation | DROPPED | ## Constraints | one locale, scoped out on the record |
| Console search filters and index maintenance | DROPPED | spec/00-decisions.md carry table | the two-index separation is carried; the console filter set is out of the ten |

## Slot obligations

| slot | state | finding |
|---|---|---|
| backend (postgres) | MET | test_seeded_rows_are_stored_exactly_once is critical in the_seeded_corpus_is_stored_exactly_once and reads the store through the backend fixture |
| storage (minio) | MET | test_an_uploaded_object_lands_in_the_bucket_at_the_key_scheme is critical in media_upload_lands_in_the_bucket and asserts object_exists plus the byte equality at the pinned key |

## Grading channels

| | |
|---|---|
| workflows | 23 (band for enterprise is 13 to 23) |
| browser substeps | 39 |
| pytest substeps | 85 |
| critical substeps | 20 |
| non-happy-path workflow ids | 10: `author_self_approval_is_denied`, `dual_hatted_reviewer_cannot_decide_two_stages`, `group_admin_is_denied_an_unpublished_body`, `author_on_another_division_is_denied`, `publisher_cannot_approve_and_approver_cannot_publish`, `anonymous_caller_is_unauthenticated_on_the_console`, `embargoed_release_is_denied_to_the_public`, `concurrent_approvals_leave_at_most_one_decision`, `invalid_enquiry_is_refused`, `the_audit_trail_cannot_be_rewritten` |
| pytest module | `tests/test_output.py`, 85 test functions |
| banners earned | core features, authorization, edge cases, data integrity, storage |
| rubric criteria | 42 judged, all positive |
| checklist items | 1007 |

Checklist items by section: C-CF 419, C-CN 18, C-DC 52, C-DM 64, C-FE 129, C-OV 14, C-RL 50, C-TR 41, C-UF 40, C-UX 180.

Checklist items by tag: capability 134, constraint 266, contract 48, data 81, literal 136, role 16, ui 326.

## Rubric dimension shares

| dimension | criteria | positive points | share | target |
|---|---|---|---|---|
| instruction_following | 8 | 36 | 0.26 | 0.30 |
| functionality | 10 | 34 | 0.25 | 0.25 |
| ux_flow | 7 | 23 | 0.17 | 0.15 |
| ui_visual | 8 | 24 | 0.17 | 0.15 |
| motion | 4 | 10 | 0.07 | 0.05 |
| accessibility | 3 | 7 | 0.05 | 0.05 |
| responsiveness | 2 | 4 | 0.03 | 0.05 |

## Grading window

`window_lint.py` reports length and fails nothing on it (generate_instruction.md S4). The tasker
asked for the section ceilings to be set aside in favour of a fuller UI/UX specification, so the
six judged sections run past the judge's slice and the whole of that prose still reaches the agent.

| section | chars | reference |
|---|---|---|
| Core features | 42670 | 2400 |
| User flow | 6661 | 1900 |
| UI/UX notes | 21959 | 1700 |
| Constraints | 2474 | 800 |
| User roles | 4828 | 1000 |
| Overview | 3344 | 700 |
| joined total | 81936 | 8800 |

## Literals ledger

89 entries, none verifier-only. Class counts: account 10, credential 1, fixture 58, quantity 15, route 5.

| value | class | carriers |
|---|---|---|
| `deku-demo-pw-2026` | credential | instruction.md, conftest.py |
| `author@example.com` | account | instruction.md, conftest.py, workflows.yaml |
| `author2@example.com` | account | instruction.md, conftest.py |
| `legal_reviewer@example.com` | account | instruction.md, conftest.py, workflows.yaml |
| `compliance_officer@example.com` | account | instruction.md, conftest.py, workflows.yaml |
| `publisher@example.com` | account | instruction.md, conftest.py, workflows.yaml |
| `group_admin@example.com` | account | instruction.md, conftest.py, workflows.yaml |
| `group` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `trading` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `capital` | fixture | instruction.md, conftest.py, test_output.py |
| `maritime` | fixture | instruction.md, conftest.py |
| `kite-energy` | fixture | instruction.md, conftest.py |
| `Kite Energy` | fixture | instruction.md, conftest.py, test_output.py |
| `draft` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `in_review` | fixture | instruction.md, conftest.py |
| `legal_review` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `compliance_review` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `changes_requested` | fixture | instruction.md, conftest.py, test_output.py |
| `approved` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `embargoed` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `published` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `unpublished` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `archived` | fixture | instruction.md, conftest.py |
| `general` | fixture | instruction.md, conftest.py, test_output.py |
| `regulated` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `market_sensitive` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `restricted` | fixture | instruction.md, conftest.py |
| `page` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `release` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `product` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `vessel` | fixture | instruction.md, conftest.py |
| `investment` | fixture | instruction.md, conftest.py |
| `person` | fixture | instruction.md, conftest.py |
| `figures` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `policy` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `redirect` | fixture | instruction.md, conftest.py, test_output.py |
| `paragraph` | fixture | instruction.md, conftest.py, test_output.py |
| `subheading_2` | fixture | instruction.md, conftest.py |
| `subheading_3` | fixture | instruction.md, conftest.py |
| `list_unordered` | fixture | instruction.md, conftest.py |
| `list_ordered` | fixture | instruction.md, conftest.py |
| `quote` | fixture | instruction.md, conftest.py |
| `image` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `table` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `CH` | fixture | instruction.md, conftest.py, test_output.py |
| `AE-DIFC` | fixture | instruction.md, conftest.py, test_output.py |
| `SG` | fixture | instruction.md, conftest.py, test_output.py |
| `9` | quantity | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `6` | quantity | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `Calder joins Energy LEAP for Operational Excellence` | fixture | instruction.md, conftest.py |
| `Calder Maritime acquires its first vessel` | fixture | instruction.md, conftest.py |
| `Calder Trading agrees a multi-year naphtha supply arrangement` | fixture | instruction.md, conftest.py |
| `Calder restates its 2022 throughput figures` | fixture | instruction.md, conftest.py |
| `Superseded by a corrected statement` | fixture | instruction.md, conftest.py |
| `gva@calder.example.com` | account | instruction.md, conftest.py |
| `dxb@calder.example.com` | account | instruction.md, conftest.py |
| `sgp@calder.example.com` | account | instruction.md, conftest.py |
| `media@calder.example.com` | account | instruction.md, conftest.py |
| `15` | quantity | instruction.md, conftest.py |
| `27` | quantity | instruction.md, conftest.py, workflows.yaml |
| `35` | fixture | instruction.md, conftest.py, workflows.yaml |
| `22` | fixture | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `POL-CONDUCT` | fixture | instruction.md, conftest.py |
| `POL-PRIVACY-CH` | fixture | instruction.md, conftest.py, test_output.py |
| `POL-PRIVACY-AE` | fixture | instruction.md, conftest.py, test_output.py |
| `POL-PRIVACY-SG` | fixture | instruction.md, conftest.py, test_output.py |
| `POL-TERMS` | fixture | instruction.md, conftest.py |
| `POL-DISC-REG` | fixture | instruction.md, conftest.py |
| `30` | quantity | instruction.md, conftest.py, test_output.py |
| `90` | quantity | instruction.md, conftest.py |
| `3` | quantity | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `5` | quantity | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `24` | quantity | instruction.md, conftest.py, workflows.yaml |
| `60` | quantity | instruction.md, conftest.py, test_output.py |
| `48` | quantity | instruction.md, conftest.py |
| `96` | quantity | instruction.md, conftest.py |
| `20000` | quantity | instruction.md, conftest.py |
| `4000` | quantity | instruction.md, conftest.py |
| `/api/health` | route | instruction.md, conftest.py |
| `/api/auth/login` | route | instruction.md, conftest.py |
| `/news/` | route | instruction.md, conftest.py, test_output.py, workflows.yaml |
| `/news/{slug}/` | route | instruction.md, conftest.py |
| `/console/login` | route | instruction.md, conftest.py |
| `#WhoWeAre` | fixture | instruction.md, conftest.py |
| `#WhatWeDo` | fixture | instruction.md, conftest.py |
| `#GlobalConnectivity` | fixture | instruction.md, conftest.py |
| `#Sustainability` | fixture | instruction.md, conftest.py, test_output.py |
| `4173` | quantity | instruction.md, conftest.py |
| `/app/USER_README.md` | fixture | instruction.md, conftest.py |

## spec/ documents and where each one fed

| document | fed |
|---|---|
| `00-decisions.md` | the draws, the cell, the identity re-cast, the roles, the scope, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements`, `## Deployment contract` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing; `## Build plan` is not emitted at this variant |

## Kit gate log

Verbatim from the receipts. `exit` is the tool's own exit code.

| gate | tool | exit | verdict | argv sha |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | `7da044975aab42fa` |
| G1/G12 | `layout_lint.py` | 0 | PASS | `96077f7d6c85a84c` |
| G46 | `structure_lint.py` | 1 | FAIL | `96077f7d6c85a84c` |
| G50 | `docker_lint.py` | 0 | PASS | `96077f7d6c85a84c` |
| G55 | `runtime_deps_lint.py` | 0 | PASS | `96077f7d6c85a84c` |
| G63 | `secret_lint.py` | 0 | PASS | `96077f7d6c85a84c` |
| G48 | `truth_lint.py` | 0 | PASS | `96077f7d6c85a84c` |
| G51 | `source_lint.py` | 0 | PASS | `438ca3d58d85a571` |
| G52 | `rubric_context_lint.py` | 0 | PASS | `96077f7d6c85a84c` |
| G54 | `comment_lint.py` | 0 | PASS | `96077f7d6c85a84c` |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | `7da044975aab42fa` |
| G11 | `leak_scan.py` | 0 | PASS | `22a1c1bac3480d6b` |
| G33 | `window_lint.py` | 0 | PASS | `22a1c1bac3480d6b` |
| G4/G5 | `contract_lint.py` | 0 | PASS | `84c03366be420db2` |
| G43 | `prescription_lint.py` | 0 | PASS | `22a1c1bac3480d6b` |
| G44 | `disclosure_lint.py` | 0 | PASS | `22a1c1bac3480d6b` |
| G10 | `no_sdk_lint.py` | 0 | PASS | `1f558c81d80302fc` |
| G31 | `determinism_lint.py` | 0 | PASS | `1f558c81d80302fc` |
| G14 | `reward_path_lint.py` | 0 | PASS | `1fb78755648b3bb7` |
| G27/G30 | `rubric_lint.py` | 0 | PASS | `a1ffcdafbe9020f6` |
| G41 | `flag_lint.py` | 0 | PASS | `96077f7d6c85a84c` |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | `96077f7d6c85a84c` |
| G59/G60 | `codequality_lint.py` | 2 | NOT-APPLICABLE | `96077f7d6c85a84c` |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | `d2322a0dbd00678f` |
| G6 | `fixture_lint.py` | 0 | PASS | `fcc8a63e09152ff1` |
| G24 | `coverage_map.py` | 0 | PASS | `7e4e5a9545341de9` |
| G37 | `checklist_qc.py` | 0 | PASS | `8578923d41731531` |
| G39 | `rubric_align_lint.py` | 0 | PASS | `466b70015d17431a` |
| G28/G29 | `channel_lint.py` | 0 | PASS | `6293e2996563db97` |
| G40 | `prompt_receipt_lint.py` | 0 | PASS | `3122aaf56b1469ba` |
| G0/INV5 | `vendor_check.py` | 0 | PASS | `31e22116de5dc7ca` |
| G47 | `output_qc.py` | 1 | FAIL | `970c6c0bdf3d1b03` |

## Blocking findings

- **G46 (structure_lint.py) exit 1.**
- **G47 (output_qc.py) exit 1.**

### G46 is an operator-configuration red, not a bundle defect

`config/kit-config.yaml` sets `output_root` to `output_16sep/`, which sits inside the repository
that holds the generation kit, so `structure_lint.py` fails CON-1 on placement for every bundle
built into it. The tasker chose that destination and asked for the task to be written there.
The remedy is one line: point `output_root` at a directory that is a sibling of the kit rather
than a child of its repository, then move the bundle. Nothing inside the bundle changes.

Verified rather than asserted: `structure_lint.py` decides CON-1 in two independent clauses,
one comparing the bundle's parent against `output_root` and one testing whether the bundle path
starts with the generation kit's repository root. Only the second fires here, and it is decided
by the path alone.

### G40 is self-attested

One agent authored and certified this bundle, so every certification receipt in
`E_legal_cont_governed-disclosure-platform-vb_20260916_072244.receipts.json` records `verifier: self`. That is a recorded verdict, never an independent
one. Six receipts carry WARN checks whose findings name a standing contradiction between a QC
prompt and a later settled rule; each is written out in the receipt rather than resolved silently.

## Budget

`turns_expected` 200 and `tokens_expected` 8000000: the top of the documented expert band and the
ceiling BENCH-004 sets. The companion cap allowed ten must-have features and ten do not build in
six features' time, so the budget sits at the ceiling rather than at the median.

## Versions

| | |
|---|---|
| kit | `deku-green-field`, revision of 2026-09-16 |
| vendored grader | `0.22.0`, byte-identical to `vendor/grader-0.22.0/MANIFEST.json` |
| target schema | `1.4` |
| verifier mode | `separate` |

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

with one open red: **G46 placement**, which is operator configuration and is described above.
Not admissible. Nothing counts toward corpus targets until the reference app lands and
`harbor run -a oracle` returns `1.0` twice.
