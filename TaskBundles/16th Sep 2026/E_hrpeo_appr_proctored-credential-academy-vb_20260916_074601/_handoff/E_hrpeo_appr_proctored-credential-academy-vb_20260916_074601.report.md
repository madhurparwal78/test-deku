# Build report: E_hrpeo_appr_proctored-credential-academy-vb_20260916_074601

Rendered from `_handoff/E_hrpeo_appr_proctored-credential-academy-vb_20260916_074601.gates.jsonl`. No verdict on this page was typed by hand.

## Identity

| | |
|---|---|
| task code | `E_hrpeo_appr_proctored-credential-academy-vb_20260916_074601` |
| task id | `deku/proctored-credential-academy-vb` |
| cell | enterprise / hr-people-ops / approval-workflow |
| archetype | `proctored-credential-academy`, variant `b` |
| service_profile | `P3-db-auth` |
| providers | `backend` = postgres, `auth` = keycloak |
| variant axes | critical_depth, spec_sections |
| language | javascript |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 |
| kit | deku-green-field |
| grader pin | 0.22.0 |
| target schema | 1.4 |
| verifier mode | separate |
| companion document | metacrafters_prd.md, 3,962 lines |

## Derived-design draws

Drawn over the archetype `proctored-credential-academy`, per reference/L L.4.

| axis | value |
|---|---|
| render_model | spa-json-api |
| backend | Express |
| frontend | Svelte + Vite |
| design_direction | companion (the drawn `dense-ops-console` is recorded and does not govern, reference/L L.6.1) |
| nav | sidebar-nav |
| work_surface | board-first |
| create_flow | multi-step-wizard |
| feedback | optimistic-row |
| launch_surface | colour_contrast, cookie_choice, favicon, meta_tags, privacy_page |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Catalogue and five-level reader | INCLUDED | Core features, Front-end specification | the companion's measured content hierarchy |
| Enrolment against a partner treasury | INCLUDED | Core features | the Task Order's funding mechanism, and the contention boundary |
| Paywall and program restriction, orthogonal | INCLUDED | Core features | companion 6.4, the two gates stack |
| Six-state assessment machine | INCLUDED | Core features | companion 8.4, transitions are the specification |
| Proctored exam with server clock | INCLUDED | Core features | companion 8.5, evidence rather than enforcement |
| Project review by a person | INCLUDED | Core features | the pattern's critical focus lives here |
| Credential issuance to a public ledger | INCLUDED | Core features | the archetype's reason to exist |
| Reward window and quota | INCLUDED | Core features | companion 8.7, an exact contract with the learner |
| Bounty board gated on a credential | INCLUDED | Core features | companion 8.6, two coupled state machines |
| Consent, retention, erasure, audit trail | INCLUDED | Core features | companion 16.x, the permanent-ledger exception |
| Launch surface: privacy, cookies, favicon, meta, contrast | INCLUDED | Core features, Technical requirements, UI/UX notes | the five drawn tokens, reference/O |
| Stripe checkout and refunds | DROPPED | Constraints | no payments slot is declared; treasury funding replaces it |
| Discord community mirroring | DROPPED | Constraints | outside the closed provider world, reference/K |
| Solana credential minting | RECAST | Core features | the product's own append-only ledger with a public proof address |
| AWS Cognito identity | RECAST | Technical requirements | Keycloak, the declared auth slot provider |
| Strapi content authoring | RECAST | Data model | course content is seeded in PostgreSQL |
| Vimeo, Wistia, OpenAI, Lightcast, Rakuten, Axiom, Pallet, Gravatar, KYC vendor | DROPPED | Constraints | vendor surfaces outside the closed world; each waived on the record |
| Enterprise SSO and SCIM | DROPPED | Constraints | a second identity provider the environment does not carry |
| Queue, outbox, cache, search index | DROPPED | Constraints | no such slot is declared; ordering is stated as an outcome instead |
| Break-glass access to proctor media | DROPPED | 00-decisions | no camera frame is stored, so there is nothing to break glass on |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| backend | postgres | MET | G32 reads a test name carrying the db vocabulary and asserting a real row; 25 tests read stored rows through `capabilities.make_backend()` |
| auth | keycloak | MET | G32 reads a test name carrying the auth vocabulary; denial at the API is asserted from four role sessions, each logging in through the app's own endpoint per reference/J J.13 |

## Grading surface

| | |
|---|---|
| workflows | 22 (enterprise band 13 to 23) |
| browser substeps | 47 |
| pytest substeps | 57 |
| critical substeps | 13 |
| non-happy-path workflow ids | 9 |
| pytest module | one, `tests/test_output.py`, 57 tests |
| checklist items | 535 |
| rubric criteria | 16 (14 positive, 2 negative) |

Non-happy-path ids: `unauthenticated_request_is_denied`, `concurrent_enrolment_for_the_last_funded_seat_at_most_one_wins`, `duplicate_enrolment_creates_no_second_row`, `paywalled_module_body_cannot_be_read_without_entitlement`, `program_restricted_course_is_forbidden_outside_its_program`, `learner_self_approval_of_a_project_is_denied`, `duplicate_issuance_writes_no_second_ledger_entry`, `learner_issuance_attempt_is_rejected`, `reward_claim_at_the_quota_limit_yields_at_most_one_grant`

## Rubric dimension shares

| Dimension | Share | Target | Within 0.10 |
|---|---|---|---|
| instruction_following | 0.32 | 0.30 | yes |
| functionality | 0.24 | 0.25 | yes |
| ux_flow | 0.16 | 0.15 | yes |
| ui_visual | 0.16 | 0.15 | yes |
| motion | 0.03 | 0.05 | yes |
| accessibility | 0.08 | 0.05 | yes |
| responsiveness | 0.03 | 0.05 | yes |

## Literals ledger

222 pinned values. G6 holds the bijection in both directions.

| Class | Count |
|---|---|
| account | 5 |
| credential | 1 |
| design_phrase | 16 |
| endpoint | 56 |
| env_var | 6 |
| motion_moment | 5 |
| number | 13 |
| route | 15 |
| scheme | 3 |
| seed_record | 31 |
| status | 71 |

## spec/ documents emitted

| Doc | Feeds |
|---|---|
| `00-decisions.md` | the audit trail, the draws, the companion carry table |
| `01-PRD.md` | Overview, Core features, Constraints |
| `02-TRD.md` | Technical requirements |
| `03-app-flow.md` | User flow |
| `04-uiux-brief.md` | UI/UX notes, Front-end specification |
| `05-backend-schema.md` | Data model, User roles |
| `06-implementation-plan.md` | nothing: Build plan is not emitted at this variant |

## Grading window

Measured by `window_lint.py` (G33), which reports length and fails nothing.

| Section | Chars | Reference |
|---|---|---|
| Core features | see the G33 receipt | 2400 |
| User flow | see the G33 receipt | 1900 |
| UI/UX notes | see the G33 receipt | 1700 |
| Constraints | see the G33 receipt | 800 |
| User roles | see the G33 receipt | 1000 |
| Overview | see the G33 receipt | 700 |

`## Core features` runs past the judge's 2,500-character slice. The tail reaches the agent in
full and stops reaching the judge; `judge_score` never touches reward, and the critical focus,
the role boundary and the entitlement rules are inside the first slice.

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

## Blocking findings

### G46 FAIL, `structure_lint.py`


### G47 FAIL, `output_qc.py`


**G46, diagnosed.** `structure_lint.py` computes the generation kit as the grandparent of
its own `tools/` directory, which in this checkout is the repository root, and the output
root `kit_config.output_root()` resolves to a directory inside it. CON-1 places `Output/`
as a sibling of the kit and the kit is expected to sit one level deeper than it does here,
so under this checkout no default location satisfies both. The bundle itself is correct:
copied unchanged to a root outside the repository, `structure_lint.py` returns
`VERDICT PASS   G46 placement (CON-1) + full-code name (CON-4) + single module & verifier
Dockerfile (CON-2) hold`. The remedy is the operator's: nest the kit one level deeper, or
export `DEKU_OUTPUT_ROOT` to a path outside the repository. Nothing in the bundle changes.

**G47** is red only because it reads the G46 receipt; it reports no defect of its own.

## Advisory notes carried forward

- G41 reports the brief carrying 13 launch-surface obligations against a drawn floor of 5.
  Above the floor is the correct outcome when a companion already states some of them.
- G39 notes `C-UX-22` graded by two criteria. They observe different facets: R8 judges the
  refusal feedback on a board, R13 judges the keyboard focus indicator across the assessment
  flow. Confirmed, not collapsed.
- G40 returns WARN: every certification prompt carries a current, bundle-bound receipt, and
  four advisory generator prompts carry none. Every QC verdict is SELF-ATTESTED: owner and
  verifier are one agent in this run, which the kit records rather than counts as independent.
- G59/G60 return NOT-APPLICABLE: the bundle carries no code-quality rubric.

## Budget

`turns_expected = 180`, `tokens_expected = 6000000`. Reasoning: nine must-have features with a
six-state machine, two contention invariants and an append-only ledger, on a stack of Express
plus a Svelte single-page front end, against a brief carrying a companion PRD's obligations.
That is above the six-feature baseline in both surface and depth, so both numbers sit above the
Standard-tier midpoint and inside the documented band.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

Not admissible. The bundle carries no reference application; `solution/solve.sh` exits
non-zero and says so. Nothing counts toward corpus targets until the app is built downstream
from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
