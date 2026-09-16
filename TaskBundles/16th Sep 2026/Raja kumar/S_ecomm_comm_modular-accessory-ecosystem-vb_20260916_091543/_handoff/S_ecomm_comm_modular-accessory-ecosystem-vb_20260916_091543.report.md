# Build report: S_ecomm_comm_modular-accessory-ecosystem-vb_20260916_091543

State: MECHANICALLY-GREEN, NO-SOLUTION. Not admissible.

Authors: utsav.jain@ethara.ai (QL), raja.kumarint17@ethara.ai (contributor). Verifier mode: separate.

## Kit gate log

Rendered from `_handoff/S_ecomm_comm_modular-accessory-ecosystem-vb_20260916_091543.gates.jsonl`. Never transcribed.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS |
| G1/G12 | `layout_lint.py` | 0 | PASS |
| G46 | `structure_lint.py` | 0 | PASS |
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
| G47 | `output_qc.py` | 0 | PASS |

Gates recorded: 32. All green: True.

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

Every certification verdict is SELF-ATTESTED: the author ran its own review prompts, so owner-is-not-verifier is not satisfied.

## Findings carried out of the review prompts

- **QC_instruction.md** A7: the seeded credentials are two phones and two emails; there is deliberately no password, per companion SS17.5
- **QC_instruction.md** A8: PAYMENTS_API_USER and PAYMENTS_API_PASSWORD are not in the SS2.3 canonical set; they replace the admin pair G17 forbids in the agent environment
- **QC_instruction.md** B3: Build plan is not emitted at baseline; the spec_sections axis is discharged by Front-end specification
- **QC_instruction.md** C7: the judge window is exceeded, Core features past the per-section slice; window_lint reports and never fails this, and nothing was trimmed from a reward-driving section
- **QC_instruction.md** D2: the two-readings sweep found five ambiguities a correct build could read differently from the graders, all closed in the brief before this receipt: the listing page default, the replayed invoice_id, the wishlist item fields, which colourway a product title uses, and three Kill Bill path placeholders written as angle tokens
- **QC_instruction.md** D5: three recorded departures from the companion, each forced by the environment: the one time code is delivered by email because the P5 profile has no SMS provider; checkout requires a signed in shopper so every paid order has a verified phone for its Kill Bill account key; and payment is a Kill Bill invoice because Kill Bill has no card object
- **QC_spec.md** S1: the seven spec docs live at _spec/<code>/ outside the bundle, because CON-5 forbids a spec/ folder in a shipped bundle
- **QC_spec.md** S3: the payments agent variables are PAYMENTS_API_USER and PAYMENTS_API_PASSWORD, a least-privilege Kill Bill user, instead of the canonical PAYMENTS_ADMIN_USER and PAYMENTS_ADMIN_PASSWORD, because G17 fails any _ADMIN_ key in the agent environment. Verified against a clean Kill Bill 0.24.21
- **QC_spec.md** S10: there is no corpus password. Companion SS17.5 and its acceptance item 46 require that no password exists anywhere, and sign in is a phone with a one time code
- **generate_instruction.md** read before authoring: supplied source rules, SS2 derivations, SS2.6 Kill Bill, SS2.9 to SS2.11 draws, SS3 phases, SS4 section spec and number rule, SS4.9 flags, SS5 to SS8
- **generate_instruction.md** the other generator prompts carry no receipt and are UNCITED; they are advisory
- **qc_docker.md** Fixed during this review: CMP-019 removed restart from every sidecar
- **qc_docker.md** CMP-011 is read as sidecars only; main publishes the app port because CMP-022 requires main to set ports and extra_hosts
- **qc_docker.md** CMP-020: main carries ports and extra_hosts as well as depends_on, because CMP-022 requires both; the two rows disagree
- **qc_docker.md** CMP-021: Kill Bill's built-in admin credential admin/password is an upstream default the agent can reach at killbill:8080; the agent environment carries only the least-privilege storefront user, and secret_lint records the same upstream pin as SEC-3
- **qc_docker.md** BP-003 and BLD-002: Node is installed from the NodeSource node_20.x channel without an exact version pin, as in the kit's reference bundles
- **qc_docker.md** DEP-015/016/017, BP-008, ARCH-004 to 007: no compiled language, no Alpine base, no architecture-specific download
- **qc_rubric.md** converged in one cycle: thirteen criteria, one obligation each, none deterministic, none cited by a workflow substep, budget within 0.10 of every weight
- **qc_solution_checklist.md** the prompt declares no numbered registry; checklist_qc.py passes over 166 items (156 at the first receipt, 10 added by the hardening pass below) with the coverage ledger reconciled against the live obligation count
- **qc_toml.md** Fixed during this review, before the receipt: ENV-005 added APP_PUBLIC_URL to the agent env; ENV-010 set the healthcheck timings to the template's 60.0 and 60; VERIF-002 and BENCH-001 set the verifier timeout to 3600.0; META-002 set harbor_version to 0.20.0; META-009 reordered keywords; SVC-004 reordered services to backend, email, payments; SCHEMA-013 and SCHEMA-014 reordered sections and keys to the SS11 template
- **qc_toml.md** ENV-006: the payments slot's agent credentials are a least-privilege Kill Bill user, not the canonical admin pair, because G17 fails the admin pair in the agent environment
- **qc_toml.md** SCHEMA-011: [delivery] and [delivery.images] are absent from the SS11 template but required by CON-2 and validated by G2; the template is behind the contract
- **qc_toml.md** BENCH-002, BENCH-003, TAX-006: the task is not trivial and difficulty is the empty calibration placeholder, so the trivial tier and the difficulty token band do not apply

## Verified outside the kit, with a running service

- `killbill/killbill:0.24.21` was started from its pinned image in a scratch compose. `POST /1.0/kb/invoices/charges/{accountId}?autoCommit=true` creates one committed invoice per call; both list endpoints report its amount as 0.0 permanently; `GET /1.0/kb/invoices/{invoiceId}` reports the real amount. The graders read by id for that reason, and the reader helper was run against the live service.
- The bundle's `killbill-init.sh` was run against a clean Kill Bill: before it the storefront user is refused (401); after it that user creates an INR account, posts a two-item charge and reads the invoice back, and is refused tenant creation (401). Re-running the script is idempotent.

## Hardening pass, 16 Sept 2026

**Scorer crash fixed.** `tests/workflows.yaml` carried unquoted `cov: C-XX-NN (earned: why)` values, which are invalid YAML. The vendored `score.py` and `run_workflows.py` load that file with `yaml.safe_load`, so every trial would have scored 0.0 as `scorer_crashed`, a correct build included. Every `cov:` and `purpose:` value is now JSON-quoted; the file parses, and `score.py` over synthetic results returns 1.0 for all passing and 11/12 for one failed critical substep.

**task.toml corrected.** `capability_flags` is `aesthetic` alone, because the Task Order declares no flags and S4 emits them verbatim; `rubric_version = "1"` added per toml_generator 10.5b.

**Eight critical traps added, each stated in the brief and drawn from companion SS24:**

| Workflow | Test | Wrong default it fails |
|---|---|---|
| sign_in_code_cannot_be_reused | `test_simultaneous_verifications_of_one_code_issue_one_session` | check the code is unused, then mark it |
| code_entry_locks_after_six_invalid_codes | `test_a_burst_of_simultaneous_wrong_codes_still_locks_the_phone` | read the wrong code count, then write it back |
| code_entry_locks_after_six_invalid_codes | `test_simultaneous_code_requests_send_at_most_five_codes` | count recent codes, then insert |
| other_shoppers_order_is_denied | `test_a_code_presented_with_another_phone_is_refused` | look a code up by its value alone |
| concurrent_checkout_sells_the_last_unit_once | `test_a_refused_order_takes_no_stock_from_its_other_lines` | take each line's stock in turn with no rollback |
| paid_order_invoices_the_exact_total_once | `test_simultaneous_payments_for_one_order_create_one_invoice` | check pending, then create the invoice |
| paid_order_invoices_the_exact_total_once | `test_paid_invoice_itemises_each_line_total_plus_paid_delivery` | one Kill Bill charge for the whole total |
| cart_prices_each_colourway_as_itself | `test_catalogue_edit_after_ordering_leaves_the_order_lines_unchanged` | read order lines back through live prices |

The suite is now 73 pytest substeps and 33 browser substeps over the same 12 workflows.

**Live runs.** A throwaway Flask stub with a correct mode and a naive mode ran against the pinned PostgreSQL, Mailpit and Kill Bill images, outside the bundle. Correct mode passed all eight tests on every run (44 of 44 test runs). Naive mode failed six traps on 5 of 5 runs with a connection per request; the two sign in races failed 1 of 5 and 4 of 5 that way, because connection setup spreads the requests apart, and 8 of 8 each once the naive stub used a connection pool, as ordinary apps do. The concurrent tests open their connections before releasing the burst for that reason.

## Not proven here

- Battery 3, handoff-owned: G13, G15, G18, G19, G20, G21, G25.
- G23 stays human-owned. G48's replay half is DEFERRED with no reference app.
- G59/G60 NOT-APPLICABLE: the vendored generator accepts no source-target criterion.
- No full reference application exists. The eight tests added by the hardening pass ran against a throwaway reference stub (below); the other 65 have not run against a real storefront. The pass rate is a prediction until calibration.
- The certification prompts were not re-run over the hardening pass; its checks were the full gate sweep and the live runs below.
- Advisory generator prompts other than generate_instruction.md are UNCITED.
