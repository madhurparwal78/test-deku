# Build report - S_ecomm_comm_merch-supply-chain-vb_20260916_073356

## Identity

| Field | Value |
|---|---|
| task code | `S_ecomm_comm_merch-supply-chain-vb_20260916_073356` |
| task id | `deku/merch-supply-chain-vb` |
| cell | solo_founder / ecommerce-retail / commerce-checkout |
| service_profile | `P5-db-pay-email` |
| providers | backend `postgres`, email `mailpit`, payments `killbill` |
| variant | `b`, axes `critical_depth`, `spec_sections` |
| language | `python` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| capability_flags | `aesthetic`, `concurrency_hardening` |
| design_direction | `companion` (reference/L L.6.1: a supplied companion beats the draw) |
| launch_surface | `custom_404`, `no_broken_links`, `sitemap_robots`, `social_preview`, `terms_page` |
| shard | 1 of 1 |
| kit revision | deku-green-field, 2026-09-16 |
| grader pin | 0.22.0 |
| target schema | 1.4 |

The Task Order named the pattern `transactional-checkout`, which is not a level-3 code.
It was keyed to the enum member it describes, `commerce-checkout` (`comm`), the only
pattern legal for solo_founder that carries a payments slot. Every other field was taken
as supplied.

## Draws

```
draw: render_model = spa-json-api
draw: backend = Litestar
draw: frontend = SolidJS + Vite
draw: design_direction = companion
draw: nav = sidebar-nav
draw: work_surface = card-grid
draw: create_flow = dedicated-route
draw: feedback = optimistic-row
```

The design-direction draw is recorded in `_spec/<code>/00-decisions.md` and does not govern:
a companion PRD was supplied, so its measured character wins on every visual axis it states.

## Source document

One companion was supplied and is recorded in `_handoff/<code>.sources.json`:
`prds/nomu.store_prd.md`, 1,707 lines, 40 sections.

G51 (`source_lint.py`) reports **10/10 colours described by family and tone, 60/60 topics
carried, 280/280 enumerated items carried**, with two declared waivers:

| Waived | Why |
|---|---|
| `--color-white #ffffff cards` | the row reduces to a token name and a hex. The A5 number rule bans a hex anywhere in the brief; the colour itself is carried as the plain near-white the cards wear. |
| `The route crawl spent eighteen of its twenty-six slots on advertising` | capture provenance from the companion's evidence-gaps section, not a product obligation. |

The full companion carry table, one row per companion section with where it landed or why it
was waived, is in `_spec/<code>/00-decisions.md`.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| marketing site, nine routes | INCLUDED | `## Core features`, `## Front-end specification` | companion sections 2, 5, 7 to 12, 37 |
| physics word cloud | INCLUDED | `## Core features`, `## UI/UX notes` | companion section 6.2; graded by the browser channel and the rubric |
| catalogue driven by the quoting catalogue | INCLUDED | `## Core features` | companion section 8 |
| brief and the artwork gate | INCLUDED | `## Core features` | companion section 14 |
| sourcing, quotes and landed cost | INCLUDED | `## Core features`, `## Data model` | companion section 15 |
| samples and quality control | INCLUDED | `## Core features` | companion section 16 |
| production runs and split lots | INCLUDED | `## Core features` | companion section 17 |
| inventory ledger across two warehouses | INCLUDED | `## Core features`, `## Data model` | companion section 18 |
| storefront and gating | INCLUDED | `## Core features` | companion section 19 |
| checkout, two rails, one ledger | INCLUDED | `## Core features` | companion section 20, re-cast onto the billing platform |
| eleven fulfillment surfaces | INCLUDED | `## Core features` | companion section 21 |
| customs, duties and sales tax | INCLUDED | `## Core features` | companion section 22 |
| returns as a reverse run | INCLUDED | `## Core features` | companion section 23 |
| the delivery promise | INCLUDED | `## Core features` | companion section 24 |
| drops, gachas and pre-sales | INCLUDED | `## Core features` | companion section 25 |
| the agent channel | INCLUDED | `## Core features` | companion section 26 |
| reporting, support, procedures, email | INCLUDED | `## Core features` | companion section 27 |
| holder community and redemption | INCLUDED | `## Core features` | companion section 28 |
| production economics and capacity | INCLUDED | `## Core features` | companion section 29 |
| card processor, decline codes, test cards | DROPPED | none | the payments slot is a billing platform, not a card processor (reference/K K.4). The fiat rail is re-cast as an account keyed by the buyer with an invoice on it, which is what the verifier can observe. |
| a real chain node and wallet provider | DROPPED | none | outside the closed provider world. The token rail, its confirmation depth, its quote window and its reorganisation are modelled inside the product against operator-driven chain events, so every outcome stays observable over HTTP. |
| WebGL shader scene | DROPPED | none | the companion's section 39 item 9 records that no captured route needed one. |
| build order and difficulty grades | DROPPED | none | authoring meta, not product. Recorded as a waiver in the carry table. |

## Slot obligations

| Slot | Provider | State | Observed by |
|---|---|---|---|
| backend | `postgres` | MET | seeded catalogue rows, the inventory ledger, order and promise rows, read back through the API |
| email | `mailpit` | MET | the confirmation, the delivery update and the return authorisation, found in the inbox by subject prefix and recipient |
| payments | `killbill` | MET | an invoice for the order total in `USD` on the account keyed by the buyer's address, plus the three seeded tenant accounts |

## Grading surface

| Measure | Value |
|---|---|
| workflows | 16 (band 10 to 16) |
| browser substeps | 59 |
| pytest substeps | 135 |
| critical substeps | 58 |
| pytest module | one, `tests/test_output.py`, 2,374 lines |
| non-happy-path workflow ids | `expired_offer_cannot_be_accepted_after_the_comparison`, `concurrent_orders_for_the_last_unit_at_most_one_wins`, `gated_listing_is_denied_without_the_entitlement`, `duplicate_checkout_settles_one_invoice_and_one_mail`, `viewer_or_anonymous_write_is_denied` |
| checklist items | 449 across ten section codes |
| rubric criteria | 16 judged, all positive |
| compiled rubric items | 135, compiled-weight share 1.0 |

Substep categories: `data_integrity` 41, `business_rule` 36, `security` 25, `presentation` 16,
`core_outcome` 6, `notification` 6, `validation` 5.

Rubric dimension shares against their frozen targets:

| Dimension | Target | Actual |
|---|---|---|
| instruction_following | 0.30 | 0.310 |
| functionality | 0.25 | 0.238 |
| ux_flow | 0.15 | 0.143 |
| ui_visual | 0.15 | 0.167 |
| motion | 0.05 | 0.048 |
| accessibility | 0.05 | 0.048 |
| responsiveness | 0.05 | 0.048 |

## Sections emitted

`## Overview` `## User roles` `## Core features` `## User flow` `## UI/UX notes`
`## Technical requirements` `## Data model` `## Front-end specification` `## Constraints`
`## Deployment contract` `## Definition of done`. `## Build plan` is not emitted at baseline.

Grading-window measurement (`window_lint.py`, reported never failed):

| Section | Chars | Reference |
|---|---|---|
| Core features | 33,958 | 2,400 |
| User flow | 6,523 | 1,900 |
| UI/UX notes | 6,977 | 1,700 |
| Constraints | 1,252 | 800 |
| User roles | 3,383 | 1,000 |
| Overview | 2,945 | 700 |
| joined six | 54,878 | 8,800 |

The brief is deliberately long. The tasker set the section caps aside so the companion could
be carried whole; `generate_instruction.md` 4 removes the length limit outright and the
prose past the judge's slice still reaches the agent in full.

## Literals ledger

110 entries, none unused, bijection green in both directions.

| Class | Count |
|---|---|
| number | 55 |
| seed_record | 20 |
| scheme | 13 |
| env_var | 11 |
| account | 8 |
| route | 2 |
| credential | 1 |

Six entries are `verifier_only`: `DB_ADMIN_URL`, `EMAIL_INBOX_API_URL`,
`PAYMENTS_ADMIN_USER`, `PAYMENTS_ADMIN_PASSWORD` and the two admin spellings behind them.
None appears in `instruction.md` or in `[environment].env`.

## Spec folder

Six documents at `_spec/S_ecomm_comm_merch-supply-chain-vb_20260916_073356/`:

| Document | Feeds |
|---|---|
| `00-decisions.md` | the draws, the identity re-cast, the companion carry table, the waivers |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |

`06-implementation-plan.md` was not authored: `## Build plan` is not emitted at baseline, so
the document would feed no section of the brief.

## Kit gate log

Rendered from `_handoff/S_ecomm_comm_merch-supply-chain-vb_20260916_073356.gates.jsonl`,
one row per gate over the bundle's current bytes.

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

### Certification prompts

Recorded in `_handoff/S_ecomm_comm_merch-supply-chain-vb_20260916_073356.receipts.json`,
one scorecard per prompt over its own declared registry.

| Prompt | Gate | Verdict | Checks | Non-pass |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | A1, B3, C7 WARN |
| `QC_spec.md` | G34 | PASS | 15 | S1, S5 WARN; S7 NOT-APPLICABLE |
| `qc_toml.md` | G36 | PASS | 120 | ENV-006, COV-004 WARN; BENCH-003, BENCH-005, SIGN-001 to 003, INST-007 NOT-APPLICABLE |
| `qc_docker.md` | G35 | PASS | 105 | CMP-011, CMP-008, CMP-020, SEC-003, BP-002, BP-004, BP-005 WARN; DEP-011, DEP-015, DEP-017, ARCH-002, ARCH-003, CMP-018 NOT-APPLICABLE |
| `qc_rubric.md` | G53 | PASS | 16 | RC-05 WARN |
| `qc_solution_checklist.md` | G37 | PASS | 0 | none |
| `task_code_verifier.md` | G3 | VALID | 12 | none |

Every one is **SELF-ATTESTED**: one agent authored the artifact and ran the review. The kit's
rule is owner is not verifier, so these are recorded verdicts rather than independent ones,
and `prompt_receipt_lint.py` says so on every row. That is the honest state of a single-agent
run, not a defect in the bundle.

## Blocking findings

**One, and it is operator configuration rather than a bundle defect.**

`G46 CON-1 placement`. `config/kit-config.yaml` sets `output_root` to
`C:/Users/LENOVO/Desktop/prd/GreenField-GenKit2/output_16sep`, which is inside the tree that
holds the generation kit. `structure_lint.py` fails CON-1 for every bundle written there, and
`output_qc.py` (G47) then fails because one receipt is red. The remedy is one line: point
`output_root` at a sibling of the kit, or leave it as `FILL` to take the default
`<root>/Output/`, then re-run `revalidate.py`. Nothing in the bundle's own bytes changes:
CON-4 naming and CON-2 single-module both pass, and the directory decodes back to its Task
Order cell.

No spec gap and no harness gap prevented a required test. Every declared slot is observed,
every checklist item is graded, and the traceability matrix carries no `UNCOVERED` row and no
empty column.

## Advisory notes carried

- `G40` reports the seven certification receipts as current and complete, and notes that the
  six advisory generator prompts carry no receipt. Those are advisory by design.
- `G63 SEC-3` reports `PAYMENTS_ADMIN_PASSWORD='password'` as a known upstream exposure. It is
  Kill Bill's built-in shiro credential, which the kit does not choose and cannot change
  without mounting a custom shiro.ini into a service that boots for minutes. The durable fix
  is word-boundary-aware scrubbing in the harness.
- `G41` notes the brief carries thirteen launch-surface obligations, the five drawn plus eight
  the companion already stated in its own words.
- `G33` and `G41` both note `## Core features` runs past the judge's 2,500-character slice. The
  tail reaches the agent in full; the judged criteria are self-contained and carry their own
  evaluation rules, so nothing that drives reward depends on the slice.
- `G59/G60` return NOT-APPLICABLE: this bundle ships the product half of the rubric only. The
  vendored `recompute.py` renders `judged_criteria` and has no `code_criteria` loop, and INV5
  forbids editing it, so a source-reading criterion could not be proven to regenerate.

## Budget

`turns_expected` 200, `tokens_expected` 7,500,000. The reasoning: the brief carries nineteen
platform capability blocks over a marketing site that must be reproduced from a measured
companion, the graded surface is 135 pytest checks and 59 browser substeps across 16
workflows, and five of the hardest obligations are concurrency, dual-rail settlement,
per-line tax rounding, committed randomness and an atomic three-leg redemption. That is the
upper half of the standard tier rather than the middle of it.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

Every kit-executable gate passes over the bundle's current bytes except `G46`, which is the
operator placement red described above, and `G47`, which fails only because it reads that
receipt. **NOT ADMISSIBLE.** Nothing counts toward corpus targets until the app is built
downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
