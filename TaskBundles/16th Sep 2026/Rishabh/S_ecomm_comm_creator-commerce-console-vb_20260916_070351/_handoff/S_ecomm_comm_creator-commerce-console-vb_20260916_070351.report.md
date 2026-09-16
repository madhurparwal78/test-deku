# Build report - S_ecomm_comm_creator-commerce-console-vb_20260916_070351

Rendered from `_handoff/S_ecomm_comm_creator-commerce-console-vb_20260916_070351.gates.jsonl`. No verdict in this file was typed by hand.

## Identity

| | |
|---|---|
| Task code | `S_ecomm_comm_creator-commerce-console-vb_20260916_070351` |
| Task id | `deku/creator-commerce-console-vb` |
| Cell | `solo_founder` / `ecommerce-retail` / `commerce-checkout` |
| Service profile | `P5-db-pay-email` -- `backend`=postgres, `email`=mailpit, `payments`=killbill |
| Variant | `b`, axes `critical_depth` + `spec_sections` (a companion PRD was supplied) |
| Language | `python` |
| Design direction | `companion` (drawn `glass-depth` recorded, does not govern) |
| Launch surface | `alt_text,form_validation,single_cta,spam_protection,terms_page` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit revision | 806eb0a |
| Grader pin | 0.22.0 |
| Target schema | 1.4 |

## Task Order mapping

The order named `domain: ecommerce-retail` and `pattern: transactional-checkout`.
The domain is in the closed enum; the pattern is not. It was mapped to
`commerce-checkout`, which is the cell the idea actually describes: a buyer picks a
tier, applies a discount and pays. Both the mapping and the pattern reading are
recorded as `decision:` lines in `Output/_spec/S_ecomm_comm_creator-commerce-console-vb_20260916_070351/00-decisions.md`.

## Scope

The bundle builds the storefront, the product page, the price-locking checkout, the
order and its double-entry ledger, the billing record in `killbill`, the receipt, the
buyer library, and the creator console's catalog, orders, ledger, discount and
pricing-decomposition surfaces. Forty-one companion subsystems are waived on the
record in `00-decisions.md`, each with its reason; `source_lint.py` (G51) reports
244/244 topics and 943/943 enumerated items carried or declared.

## Graded surface

| | |
|---|---|
| Workflows | 16 (solo_founder band 10-16) |
| Browser substeps | 23 |
| Pytest substeps | 40 |
| Critical substeps | 9 |
| Non-happy-path workflow ids | 7: `duplicate_confirm_creates_at_most_one_order`, `concurrent_confirms_leave_the_quantity_limit_intact`, `reader_cannot_read_creator_orders`, `another_readers_entitlement_request_is_denied`, `anonymous_console_request_is_unauthenticated`, `expired_discount_code_is_refused`, `invalid_signup_submission_is_refused` |
| Pytest module | `tests/test_output.py`, 40 test functions, one module (CON-2) |
| Checklist items | 285 |
| Rubric criteria | 15 (13 positive, 2 negative) |

### Rubric dimension shares (positive scores only)

| Dimension | Criteria | Share |
|---|---|---|
| `accessibility` | 1 | 0.03 |
| `functionality` | 3 | 0.26 |
| `instruction_following` | 3 | 0.31 |
| `motion` | 1 | 0.03 |
| `responsiveness` | 1 | 0.03 |
| `ui_visual` | 2 | 0.17 |
| `ux_flow` | 2 | 0.17 |

### Slot obligation table

| Slot | Provider | Status | Observed by |
|---|---|---|---|
| `backend` | postgres | MET | `test_paid_order_ledger_postings_are_stored_and_balance` |
| `payments` | killbill | MET | `test_paid_checkout_invoice_exists_for_worked_total` |
| `email` | mailpit | MET | `test_receipt_email_reaches_the_buying_reader_only` |

## Literals ledger

| Class | Count |
|---|---|
| `account` | 3 |
| `credential` | 1 |
| `design_phrase` | 6 |
| `endpoint` | 24 |
| `env_var` | 12 |
| `motion_moment` | 4 |
| `number` | 24 |
| `route` | 16 |
| `scheme` | 6 |
| `seed_record` | 21 |
| `status` | 18 |

Total 135 pinned values. `fixture_lint.py` (G6) reports the bijection
holding in both directions across `instruction.md`, `conftest.py` and `test_output.py`.

## Grading window

`window_lint.py` reports `## Core features` at 15,336 characters against the
2,500-character `run_rubric` slice and a joined total of 32,050 against 9,000. Nothing
was trimmed: the brief has no length limit, and the judged criteria are self-contained
and carry their own facts, so the judge does not depend on the sliced tail.

## Kit gate log

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
| `G59/G60` | `codequality_lint.py` | 2 | ? |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS |
| `G6` | `fixture_lint.py` | 0 | PASS |
| `G24` | `coverage_map.py` | 0 | PASS |
| `G37` | `checklist_qc.py` | 0 | PASS |
| `G39` | `rubric_align_lint.py` | 0 | PASS |
| `G28/G29` | `channel_lint.py` | 0 | PASS |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN |
| `G0/INV5` | `vendor_check.py` | 0 | PASS |
| `G47` | `output_qc.py` | 0 | PASS |

`G59/G60` exit 2 is NOT-APPLICABLE: the bundle carries no source-target rubric
criteria. The vendored `recompute.py` accepts only the seven product dimensions, so a
code-quality criterion cannot be rendered through it; the channel is advisory and
carrying none is legal.

`G40` is WARN, not PASS. See the self-attestation note below.

## Corpus-level gates

| Gate | Result |
|---|---|
| G42 `corpus_overlap.py` | NOT-APPLICABLE -- no second archetype in this cell |
| G49 `diversity_lint.py` | WARN mode; no finding names this bundle after the two shared prose runs were rewritten |
| G61 `corpus_report.py` | NOT-APPLICABLE -- no admissible bundle in the ledger yet |
| G38 `kit_selftest.py` | PASS, 32 checks |

## Blocking findings

None.

## Self-attestation

`G40` reports WARN. The six certification prompts -- `QC_spec.md`,
`QC_instruction.md`, `qc_toml.md`, `qc_docker.md`, `qc_rubric.md` and
`task_code_verifier.md` -- were run by the same agent that authored the artifacts they
certify. Owner and verifier are one identity, so every verdict in
`S_ecomm_comm_creator-commerce-console-vb_20260916_070351.receipts.json` is recorded rather than independent. Five checks are
WARN and eleven are NOT-APPLICABLE; the findings are in the receipt.

## Estimate

`turns_expected` 200, `tokens_expected` 8,000,000. Three service slots, a
double-entry ledger with a continuously-held trial-balance invariant, a two-audience
isolation boundary enforced server-side, a contention rule on a single-unit product,
and an arithmetic-parity obligation between the pricing surface and the order path.
That is the top of the band.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`

Not admissible. The bundle carries no reference app. It becomes admissible when the
app lands downstream from `solution/checklist.md` and `harbor run -a oracle` returns
`1.0` twice.
