# Build report: hardware-companion-storefront (Opal)

TASK CODE        S_ecomm_comm_hardware-companion-storefront-vb_20260916_093652
TASK ID          deku/hardware-companion-storefront-vb
CELL             solo_founder / ecommerce-retail / commerce-checkout
SERVICE PROFILE  P5-db-pay-email
PROVIDERS        backend = postgres, payments = killbill, email = mailpit
VARIANT          b   (variant_axes: critical_depth, spec_sections; a companion PRD was supplied)
LANGUAGE         typescript
SPEC SECTIONS    overview, roles, features, flow, uiux, techrequirements, datamodel, buildplan, contract
CAPABILITY FLAGS concurrency_hardening, data_scale   (aesthetic injected always-on; design_direction = companion)
LAUNCH SURFACE   cookie_choice, mobile_viewport, page_view_log, single_cta, spam_protection
SHARD            1 of 1

## Exit state

MECHANICALLY-GREEN, NO-SOLUTION. Not admissible until the app is generated downstream from
solution/checklist.md and `harbor run -a oracle` returns 1.0 twice.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Storefront catalogue with cameras and accessories | INCLUDED | Core features, products/variants | the retail spine |
| Server side cart with a price snapshot and re-price | INCLUDED | Core features, test_cart_line_stores_price_snapshot | price integrity is the trust surface |
| Three-step guest checkout raising a killbill invoice | INCLUDED | payments slot, test_checkout_raises_invoice_on_account | commerce-checkout critical focus: invoice on the account |
| Order confirmation email | INCLUDED | email slot, test_order_confirmation_email_delivered | the transactional message the buyer expects |
| Idempotent checkout under contention | INCLUDED | concurrency_hardening, test_concurrent_* | the money must stay honest on a double submit |
| Founder letter over a full screen workshop film | INCLUDED | Overview, /, rubric R1/R9 | the distinctive launch surface of the source PRD |
| Device registration by serial and browser firmware flash | INCLUDED | Core features, test_flash_device_moves_firmware | the hardware-companion half of the idea |
| Companion desktop application release feed | INCLUDED | Core features, /downloads | the download-and-release half of the idea |
| Paginated catalogue and orders | INCLUDED | data_scale, test_orders_pagination_cursor | tens of thousands of rows |
| Card processor and hosted card element | DROPPED | Constraints | payment is booked as a killbill invoice, no card vendor in the closed world |
| Wallets, accelerated checkout, buy-now-pay-later | DROPPED | Constraints | out of scope; needs external wallet origins |
| Shipment protection, tax and shipping-zone engines | DROPPED | Constraints | third-party line items and zone resolvers out of scope |
| Warranty, returns, support desk, operations console | DROPPED | Constraints | staff-facing surfaces out of a single-buyer build |
| Object store for firmware and app binaries | DROPPED | Constraints | T4: P5 already carries db, payments and email; releases are db records |
| Webhooks, presets, cloud sync, search index | DROPPED | Constraints | out of the closed world |

## Slot obligations

| Slot | Provider | Status | Evidence |
|---|---|---|---|
| backend | postgres | MET | test_order_persisted_in_db (critical), test_seed_is_idempotent (data_integrity) |
| payments | killbill | MET | test_checkout_raises_invoice_on_account (critical), test_checkout_replay_no_second_invoice |
| email | mailpit | MET | test_order_confirmation_email_delivered (critical) |

## Workflows and tests

- Workflows: 12 (solo_founder band 10-16). Browser substeps: 12. Pytest substeps: 25. Critical substeps: 6.
- Non-happy-path ids: flash_forbidden_on_other_device, unauthenticated_and_cross_account_denied,
  signup_duplicate_and_short_password, concurrent_duplicate_checkout_single.
- One pytest module: tests/test_output.py (25 tests). Sections observed: core features, data
  integrity, payments, email, authorization, data scale, presentation.

## Rubric

- 11 judged criteria (tests/rubric.json), all positive. Dimensions: instruction_following 2,
  functionality 2, ux_flow 2, ui_visual 2, motion 1, accessibility 1, responsiveness 1.
- Runtime-inert until run_rubric.py gains --rubric (D17); spec obligations enforced statically.

## Literals ledger

| Class | Value | Carriers |
|---|---|---|
| credential | deku-demo-pw-2026 | instruction.md, conftest.py |
| account | customer@example.com, customer2@example.com | instruction.md, conftest.py |
| number | 79900 | instruction.md, conftest.py |
| currency | usd | instruction.md, conftest.py |
| status | paid | instruction.md, conftest.py |
| version | 1.1.0 | instruction.md, conftest.py |
| env_var (verifier-only) | DB_ADMIN_URL, PAYMENTS_ADMIN_PASSWORD | task.toml |

## Spec docs emitted

- _spec/.../00-decisions.md  -- residual judgment calls and the deterministic draws
- _spec/.../01-PRD.md        -- the condensed companion the brief is derived from (G51 source)

## KIT GATE LOG (rendered from gates.jsonl, never transcribed)

```
G2/G16    validate_task.py        exit=0 PASS      G43       prescription_lint.py    exit=0 PASS
G1/G12    layout_lint.py          exit=0 PASS      G44       disclosure_lint.py      exit=0 PASS
G46       structure_lint.py       exit=0 PASS      G10       no_sdk_lint.py          exit=0 PASS
G50       docker_lint.py          exit=0 PASS      G31       determinism_lint.py     exit=0 PASS
G55       runtime_deps_lint.py    exit=0 PASS      G14       reward_path_lint.py     exit=0 PASS
G63       secret_lint.py          exit=0 PASS      G27/G30   rubric_lint.py          exit=0 PASS
G48       truth_lint.py           exit=0 PASS      G41       flag_lint.py            exit=0 PASS
G51       source_lint.py          exit=0 PASS      G56/57/58 if_lint.py              exit=0 PASS
G52       rubric_context_lint.py  exit=0 PASS      G59/G60   codequality_lint.py     exit=2 N/A
G54       comment_lint.py         exit=0 PASS      G7/8/9/32/45 workflow_lint.py     exit=0 PASS
G17       secret_hygiene_lint.py  exit=0 PASS      G6        fixture_lint.py         exit=0 PASS
G11       leak_scan.py            exit=0 PASS      G24       coverage_map.py         exit=0 PASS
G33       window_lint.py          exit=0 PASS      G37       checklist_qc.py         exit=0 PASS
G4/G5     contract_lint.py        exit=0 PASS      G39       rubric_align_lint.py    exit=0 PASS
G28/G29   channel_lint.py         exit=0 PASS      G40       prompt_receipt_lint.py  exit=0 PASS
G0/INV5   vendor_check.py         exit=0 PASS      G47       output_qc.py            exit=0 PASS
```

Adversarial QC (self-attested, temp 0): G34 QC_instruction PASS, G34 QC_spec PASS,
G35 qc_docker PASS, G36 qc_toml PASS, G37 qc_solution_checklist PASS, G53 qc_rubric PASS,
G3 task_code_verifier VALID. Receipts in _handoff/*.receipts.json.

G59/G60 exit 2 = NOT-APPLICABLE: no code-quality (source) rubric is authored, which is optional.

## Handoff gates (undecided here, see the handoff contract)

G13, G15, G18, G19, G20, G21, G25 are handoff-owned; the kit cannot run them. Commands and
expected verdicts are in S_ecomm_comm_hardware-companion-storefront-vb_20260916_093652.handoff.md.

## Blocking findings

NONE.

## Versions

Kit 806eb0a; vendored grader pin 0.22.0; target schema 1.4.

## Estimate

turns_expected ~ 110-160; tokens_expected high. Reasoning: three backing services (postgres,
killbill, mailpit) with a slow-booting JVM payments provider, a server-side cart with price
integrity, an idempotent checkout raising a killbill invoice and sending a confirmation email,
a device registry with a browser firmware flash, cursor pagination, and a launch-surface set
(cookie consent, page-view log, contact decoy, single primary action, narrow viewport).
