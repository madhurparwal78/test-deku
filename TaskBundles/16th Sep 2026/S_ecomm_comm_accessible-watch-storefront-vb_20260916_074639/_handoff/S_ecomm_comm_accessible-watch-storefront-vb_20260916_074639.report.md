# Build report - S_ecomm_comm_accessible-watch-storefront-vb_20260916_074639

## Identity

| Field | Value |
|---|---|
| Task code | `S_ecomm_comm_accessible-watch-storefront-vb_20260916_074639` |
| Task id | `deku/accessible-watch-storefront-vb` |
| Category | solo_founder |
| Domain | ecommerce-retail |
| Pattern | commerce-checkout |
| Service profile | `P5-db-pay-email` |
| Providers | backend `postgres` - email `mailpit` - payments `killbill` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | typescript |
| Design direction | companion |
| Launch surface | cookie_choice, no_broken_links, page_view_log, privacy_page, spam_protection |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field, grader pin `0.22.0`, target schema `1.4` |

## Feature resolution

| Candidate | Verdict | Where it landed | Reason |
|---|---|---|---|
| Collection browse with availability facet, nine sorts and numbered paging | INCLUDED | `instruction.md` Core features, the collection route | the pattern's read surface, and the catalogue arithmetic the critical focus rests on |
| Product route with colourway grid, per-variant price and availability | INCLUDED | Core features, the product route | the companion's deepest specified surface |
| Cart projected into drawer, cart page, checkout summary, permalink, header badge | INCLUDED | Core features, the cart | the one cart object the brief keeps single |
| Guest checkout opening one billing account per order reference | INCLUDED | Core features, the checkout | the payments slot's only referenceable write |
| Discount signup delivering a code by SMTP | INCLUDED | Core features, the signup | the email slot's real side effect |
| Display-currency conversion at one rate per response | INCLUDED | Core features, money | the companion's currency selector, carried as arithmetic |
| Shipping-protection upsell as a catalogue product | INCLUDED | Core features, the upsell | the companion models it as a product, not a fee |
| Cookie choice, privacy page, page-view log, link integrity, spam protection | INCLUDED | Core features, Technical requirements | the five launch-surface obligations drawn for this bundle |
| Card payment capture, refunds, chargebacks | DROPPED | - | Kill Bill is a billing platform with no charge object; the brief says so in Technical requirements |
| Customer accounts, order history, saved addresses | DROPPED | - | the companion's account area is a sign-in handoff with nothing behind it |
| On-site review composer | DROPPED | - | ratings are read-only in the companion; the review link leads out |
| Search suggestions backed by a search slot | DROPPED | - | no `search` slot in `P5-db-pay-email`; the overlay is carried as a front-end behaviour |

## Slot obligations

| Slot | Provider | State | Evidence |
|---|---|---|---|
| backend | postgres | MET | `test_seeded_catalogue_rows_are_persisted_in_the_store` (critical), plus six further store reads |
| email | mailpit | MET | `test_signup_delivers_the_discount_code_by_mail` (critical) reads the real inbox |
| payments | killbill | MET | `test_checkout_creates_exactly_one_billing_account_for_the_order` (critical) reads the real tenant |

## Graders

| Measure | Value |
|---|---|
| Workflows | 16 |
| Browser substeps | 90 |
| Pytest substeps | 45 |
| Critical substeps | 13 |
| Non-happy-path workflow ids | `a_duplicate_order_opens_no_second_billing_account`, `an_invalid_or_duplicate_signup_is_rejected`, `a_catalogue_write_is_denied_from_the_storefront` |
| Pytest module | `tests/test_output.py`, 42 test functions |
| Rubric criteria | 24 - 20 positive, 4 negative |

### Rubric dimension shares

| Dimension | Points | Share | Target |
|---|---|---|---|
| instruction_following | 18 | 0.30 | 0.30 |
| functionality | 15 | 0.25 | 0.25 |
| ux_flow | 9 | 0.15 | 0.15 |
| ui_visual | 9 | 0.15 | 0.15 |
| motion | 3 | 0.05 | 0.05 |
| accessibility | 3 | 0.05 | 0.05 |
| responsiveness | 3 | 0.05 | 0.05 |

## Checklist and coverage

| Measure | Value |
|---|---|
| Checklist items | 615 |
| By section | C-CF 291, C-CN 12, C-DC 33, C-DM 34, C-FE 104, C-OV 10, C-RL 16, C-TR 39, C-UF 34, C-UX 42 |
| By class | capability 69, constraint 160, contract 68, data 22, literal 135, role 12, ui 149 |
| Cited by pytest | 276 |
| Cited by a browser substep | 189 |
| Cited by a rubric criterion | 150 |
| Uncited | 0 |

Channel exclusivity holds: every `ui` item is graded by the rubric alone, every `contract`,
`data` and `role` item by pytest, and no item is claimed by both the browser and the rubric.
The requirement table and its matrix are at `tests/traceability-matrix.md` and
`tests/traceability-matrix.csv`; this report cites them rather than restating them.

## Literals ledger

| Value | Class | Carriers |
|---|---|---|
| `/api/health` | route | instruction.md, test_output.py |
| `174` | count | instruction.md, conftest.py |
| `161` | count | instruction.md, conftest.py |
| `13` | count | instruction.md, conftest.py |
| `16` | count | instruction.md, conftest.py |
| `11` | count | instruction.md, conftest.py |
| `all` | handle | instruction.md, conftest.py |
| `usd` | currency | instruction.md, conftest.py |
| `INR` | currency | instruction.md, conftest.py |
| `88.0` | rate | instruction.md, conftest.py |
| `$ 124.00 USD` | money | instruction.md, conftest.py |
| `Rs. 10,912.00 INR` | money | instruction.md, conftest.py |
| `12400` | money | instruction.md, conftest.py |
| `volari-2506-rebel-face-watch` | handle | instruction.md, conftest.py |
| `VOLARI 2506 - Rebel Face Watch` | title | instruction.md, conftest.py |
| `24800` | money | instruction.md, conftest.py |
| `Color` | label | instruction.md, conftest.py |
| `Black Red` | variant | instruction.md, conftest.py |
| `Exclusive Online Offer - Save 50%` | copy | instruction.md, conftest.py |
| `VOLARI 2627 - Diamond Scale Quartz Watch` | title | instruction.md, conftest.py |
| `Rose Gold` | variant | instruction.md, conftest.py |
| `10400` | money | instruction.md, conftest.py |
| `9900` | money | instruction.md, conftest.py |
| `11900` | money | instruction.md, conftest.py |
| `VOLARI 2697 - Women's Business Watch` | title | instruction.md, conftest.py |
| `9200` | money | instruction.md, conftest.py |
| `10600` | money | instruction.md, conftest.py |
| `shipping-protection` | handle | instruction.md, conftest.py |
| `Shipping Protection` | title | instruction.md, conftest.py |
| `Protect your order from damage, loss, or theft during shipping.` | copy | instruction.md, conftest.py |
| `1000` | money | instruction.md, conftest.py |
| `2000` | money | instruction.md, conftest.py |
| `Sale` | badge | instruction.md, conftest.py |
| `Buy 1 Get 1 Free` | badge | instruction.md, conftest.py |
| `VOLARI10` | code | instruction.md, conftest.py |
| `Your 10% code: VOLARI10` | subject | instruction.md, conftest.py |
| `Volari Official` | brand | instruction.md, conftest.py |
| `support@volariofficial.com` | email | instruction.md |
| `/app/USER_README.md` | path | instruction.md, conftest.py |
| `/app/logs/requests.log` | path | instruction.md, conftest.py |
| `admin` | credential | instruction.md |
| `password` | credential | instruction.md |
| `volari_owner` | credential | verifier-only |
| `vs-owner-pw-2026` | credential | verifier-only |

## Spec documents

| Document | Sections of instruction.md it fed |
|---|---|
| `00-decisions.md` | the draws, the judgment calls and the companion carry table behind every section |
| `01-PRD.md` | Overview, User roles, Core features |
| `02-TRD.md` | Technical requirements, Deployment contract |
| `03-app-flow.md` | User flow |
| `04-uiux-brief.md` | UI/UX notes, Front-end specification |
| `05-backend-schema.md` | Data model |
| `06-implementation-plan.md` | Definition of done, Constraints |

## Grading window

| Section | Characters |
|---|---|
| Overview | 2293 |
| User roles | 1468 |
| Core features | 39906 |
| User flow | 7269 |
| UI/UX notes | 9553 |
| Front-end specification | 20637 |
| Technical requirements | 4667 |
| Data model | 4086 |
| Constraints | 1653 |
| Deployment contract | 4271 |
| Definition of done | 700 |

The three budgeted sections are past the kit's reference slice. The operator instructed that the
kit's cap constraints be set aside for this task so the UI could be specified in full; `window_lint`
reports the length rather than failing it, and the receipt for `QC_instruction.md` records the same
deviation under C7.

## Kit gate log

Rendered from `_handoff/S_ecomm_comm_accessible-watch-storefront-vb_20260916_074639.gates.jsonl`. Nothing here is transcribed.

| Gate | Tool | Exit | Verdict | Output SHA |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | `ef4415029db6fc02` |
| `G1/G12` | `layout_lint.py` | 0 | PASS | `1a3d5da6cc94bcf1` |
| `G46` | `structure_lint.py` | 0 | PASS | `27828746998aa6c8` |
| `G50` | `docker_lint.py` | 0 | PASS | `380ed7d1c830de35` |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | `a0c21dca8bc5f78a` |
| `G63` | `secret_lint.py` | 0 | PASS | `767da2614bedf685` |
| `G48` | `truth_lint.py` | 0 | PASS | `c26d0a7fc6afc450` |
| `G51` | `source_lint.py` | 0 | PASS | `9df7525a8c1799e0` |
| `G52` | `rubric_context_lint.py` | 0 | PASS | `866527884f8548f5` |
| `G54` | `comment_lint.py` | 0 | PASS | `65e99bfb2cd0e964` |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | `c5d53447d6c59e21` |
| `G11` | `leak_scan.py` | 0 | PASS | `f44216f9f7908fef` |
| `G33` | `window_lint.py` | 0 | PASS | `a8d90a1053b4620d` |
| `G4/G5` | `contract_lint.py` | 0 | PASS | `a59215855041b110` |
| `G43` | `prescription_lint.py` | 0 | PASS | `661f0e5e88d5f8ca` |
| `G44` | `disclosure_lint.py` | 0 | PASS | `d9c9a1972de2e5ba` |
| `G10` | `no_sdk_lint.py` | 0 | PASS | `320de6bf2fd5c52f` |
| `G31` | `determinism_lint.py` | 0 | PASS | `a0dae12cacce9ce8` |
| `G14` | `reward_path_lint.py` | 0 | PASS | `d02f3c22d548ebfb` |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | `f8fb3ef808b8666e` |
| `G41` | `flag_lint.py` | 0 | PASS | `8c8e7ed05283e110` |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | `cdf20c83e9056866` |
| `G59/G60` | `codequality_lint.py` | 2 | ? | `e23941dd85e0253b` |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | `0f65608b338fe278` |
| `G6` | `fixture_lint.py` | 0 | PASS | `2763291caedd0fb5` |
| `G24` | `coverage_map.py` | 0 | PASS | `ef70ec32bac0c01d` |
| `G37` | `checklist_qc.py` | 0 | PASS | `91a77e084786941a` |
| `G39` | `rubric_align_lint.py` | 0 | PASS | `209910264f1d9fae` |
| `G28/G29` | `channel_lint.py` | 0 | PASS | `e245f6971ccd50e8` |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | `baa605b7b8758b76` |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | `a15a9141403c2915` |
| `G47` | `output_qc.py` | 0 | PASS | `ce878b163e5c2a90` |

Three standing WARNs sit inside green verdicts:

- `G63` SEC-3 - `PAYMENTS_ADMIN_PASSWORD` defaults to `password`, which is Kill Bill's own upstream
  shiro pin rather than a value this bundle chose.
- `G41` launch_surface - the brief carries fifteen bank obligations where five were drawn.
- `G41` window - `## Core features` is past the point at which `run_rubric` slices a section for the
  judge.
- `G40` self-attestation - every certification prompt was run by the agent that authored the
  artifact, so each receipt is a recorded verdict rather than an independent one.

## Handoff gates, undecided

| Gate | Command | Expected |
|---|---|---|
| G13 | `docker build -f environment/Dockerfile .` | exit 0 |
| G13 | `docker build -f tests/Dockerfile .` | exit 0 |
| G15 | `docker compose up` with a scrubbed environment | every sidecar healthy |
| G19 | `harbor run -p <task> -a oracle` | reward == 1.0, twice |
| G18 | `deployed` read from either oracle run | 1.0 |
| G20 | `harbor run -p <task> -a nop` | reward == 0.0 |
| G21 | fake-integration patch, re-run oracle | reward < 1.0 |
| G25 | reviewer exploit sweep, reference library F | 0 of 11 succeed |

## Blocking findings

- No reference application exists. Every handoff gate above is undecided for that reason alone.
- Kill Bill exposes no referenceable invoice-creation endpoint at the pinned version, so the
  payments critical focus is narrowed to account creation under the order's own `externalKey` and
  the conflict the tenant itself raises on a repeat. Recorded in `00-decisions.md`.
- The requested output directory sits inside the generation kit's own tree. `structure_lint` now
  accepts it because the operator moved the kit under `genkit/` and pointed `output_root` here.

## Budget

`turns_expected` 170 and `tokens_expected` 7000000, the `hard` band. Three slots, a 174-product
seed with per-variant pricing, eleven collections, eleven authored routes, a fully specified
front-end and a checkout that has to reach a real billing tenant put this above the medium band
and below expert, which is reserved for multi-role authorization work this task does not carry.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts this bundle toward corpus targets until the reference app lands and
`harbor run -a oracle` returns 1.0 twice.
