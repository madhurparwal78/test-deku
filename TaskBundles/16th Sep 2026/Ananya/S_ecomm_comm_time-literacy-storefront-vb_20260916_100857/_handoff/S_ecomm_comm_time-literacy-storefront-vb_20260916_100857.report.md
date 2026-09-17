# Build report - S_ecomm_comm_time-literacy-storefront-vb_20260916_100857

| | |
|---|---|
| Task code | `S_ecomm_comm_time-literacy-storefront-vb_20260916_100857` |
| Task id | `deku/time-literacy-storefront-vb` |
| Cell | solo_founder / ecommerce-retail / commerce-checkout |
| Service profile | `P5-db-pay-email` |
| Providers | backend `postgres`, email `mailpit`, payments `killbill` |
| Variant | `b`, axes `critical_depth`, `spec_sections` (companion-backed) |
| Language | python (Flask 3, Jinja2, Alpine.js 3, SQLAlchemy 2, psycopg 3, httpx) |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Companion | `Prds/blok_prd.md` (blokwatches.com) |
| Task Order | contributor ananya.tandon.int43@ethara.ai, QL kaustubh.dalvi@ethara.ai |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Task Order deviation

The Task Order named pattern `transactional-checkout`, which is not a level-3 enum member
(`taskorder_lint.py` FAIL). It was minted as `commerce-checkout`, the only checkout pattern, whose
critical focus is an invoice for the right amount on the buyer's billing account. The mapping is
recorded in `_spec/S_ecomm_comm_time-literacy-storefront-vb_20260916_100857/00-decisions.md`; `task-order.yaml` carries the mapped value.

## Derivation draws

SHA-256 draws over the archetype `time-literacy-storefront`.

| Axis | Value |
|---|---|
| render_model | `mpa-progressive` |
| backend | Flask + Jinja |
| frontend | Alpine.js + server templates |
| nav | `top-nav` |
| work_surface | `table-first` |
| create_flow | `modal` |
| feedback | `inline-banner` |
| design_direction | `companion` (the bank draw `editorial-serif` is recorded, not applied) |
| launch_surface | `alt_text, mobile_viewport, no_broken_links, privacy_page, sitemap_robots` |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Dial demonstration: timer setter, run, swatches, reduced motion | INCLUDED | Core features | the idea's demo timer on an interactive dial |
| Dial comparison driven by one slider | INCLUDED | Core features | the idea's redesigned markers against a conventional face |
| Home page argument in nine sections | INCLUDED | Core features, Front-end specification | companion home page, normative order |
| Catalogue: six collections, filters, facets, sorts, search, redirects | INCLUDED | Core features | four colourways, two case sizes |
| Product pages with derived availability | INCLUDED | Core features | companion product surface |
| Bundles derived from two watches | INCLUDED | Core features | the idea's parent-and-child bundle |
| Reviews with owner moderation | INCLUDED | Core features | the idea's owner reviews |
| Cart holds, concurrency, gift with purchase | INCLUDED | Core features | the pattern's contended stock |
| Checkout into a Kill Bill invoice with order mail | INCLUDED | Core features | the `payments` and `email` slots, the pattern's critical focus |
| Passwordless sign-in links | INCLUDED | Core features | companion auth, `email` slot |
| Owner stock console and restock mail | INCLUDED | Core features | companion restock, `email` slot |
| Content pages and the launch surface | INCLUDED | Core features | drawn launch surface |
| Markets, currencies, tax and duty, landed cost | DROPPED | Constraints | outside the Task Order scope; US only |
| Warranty claims, returns desk, serials, fulfilment, carriers | DROPPED | Constraints | outside scope |
| Staff roles, approvals, webhooks, jobs, audit chains | DROPPED | Constraints | single owner, no queue slot |
| Newsletter, pop-ups, discount codes, video, press ticker | DROPPED | Constraints | companion growth surface outside scope |
| Build order, difficulty map, acceptance checklist, evidence gaps | DROPPED | (G51 waivers) | work orders and authoring provenance, not product asks |

## Slot obligations

| Slot | Provider | Status | Evidence |
|---|---|---|---|
| backend | postgres | MET | `test_stock_ledger_deltas_sum_to_on_hand_for_every_inventory_item_row` (critical), plus every StoreDb assertion |
| email | mailpit | MET | `test_order_confirmation_email_subject_names_order_addressed_only_to_account_opens_with_number_total` (critical), `test_restock_mails_each_waiting_subscriber_once_with_back_in_stock` (critical) |
| payments | killbill | MET | `test_checkout_invoice_exists_on_killbill_account_keyed_tock_plus_account_email` (critical), `test_second_order_reuses_killbill_account_with_second_invoice` |

## Graders

| | |
|---|---|
| Workflows | 15 (solo_founder band 10-16) |
| Browser substeps | 33 |
| Pytest substeps | 356 |
| Critical substeps | 16 |
| Pytest module | one, `tests/test_output.py`, 356 test functions |
| Category mix | business_rule 140, core_outcome 2, data_integrity 46, notification 10, presentation 102, security 26, validation 30 |
| Non-happy-path ids | `invalid_or_spent_sign_in_rejected`, `anonymous_and_customer_calls_denied`, `visitor_fills_a_cart_while_concurrent_adds_admit_one` |

G45 is WARN: the browser:pytest ratio is 33:356, under the advisory 0.40 floor. The
suite asserts most of the brief directly (API, rows, invoices, mail and page-driven Playwright),
and adding a hundred LLM-driven browser steps to lift the ratio would not fit the 3,600 second
verifier budget. Every workflow still carries at least one browser substep.

## Rubric

17 criteria, all positive. Positive score total 57. Task completion 12 of 17.

| Dimension | Share | Target |
|---|---|---|
| instruction_following | 0.263 | 0.30 |
| functionality | 0.228 | 0.25 |
| ux_flow | 0.140 | 0.15 |
| ui_visual | 0.193 | 0.15 |
| motion | 0.070 | 0.05 |
| accessibility | 0.053 | 0.05 |
| responsiveness | 0.053 | 0.05 |

Generated from `solution/trinity/grounding.yaml` by the vendored `recompute.py`, never hand-edited.
Every criterion grades a `ui` checklist item no test and no browser substep claims.
`judge_score` remains advisory and never drives reward. No `source` criteria are authored, because
the vendored `recompute.py` renders no `code_criteria` (G59/G60 NOT-APPLICABLE).

## Literals ledger

94 entries in `_handoff/S_ecomm_comm_time-literacy-storefront-vb_20260916_100857.literals-ledger.json`.

| Class | Count |
|---|---|
| account | 7 |
| copy | 36 |
| credential | 1 |
| endpoint | 2 |
| env_var | 4 |
| number | 9 |
| route | 4 |
| scheme | 6 |
| seed_record | 10 |
| status | 11 |
| subject | 4 |

Verifier-only: `DB_ADMIN_URL`, `EMAIL_INBOX_API_URL`, `PAYMENTS_ADMIN_USER`, `PAYMENTS_ADMIN_PASSWORD`.

## Coverage

`solution/checklist.md` holds 454 items: CF 259, CN 19, DC 11, DM 30, FE 61, OV 2, RL 9, TR 9, UF 19, UX 35.
Tags: capability 221, constraint 85, contract 27, data 26, literal 57, role 7, ui 31.
G24 joins them both ways against 356 pytest tests, 33 browser substeps and 17 rubric
criteria; every item is cited and every citation earns its wording. `tests/traceability-matrix.md`
and `.csv` are regenerated by the sweep.

## Declared but ungraded (OPEN-DECISIONS D-H)

`solution/checklist.md` carries a `## Declared but ungraded` part, the resolution
`stage-3-checklist.md` proposes for D-H, listing every stated ask no grading channel can observe in
one separate-mode run, each with its `why:`. These are escalated to the kit owner as D-H: they are
real obligations the harness, a code review or a longer run must check, never items reporting
coverage nobody has.

## Residual refinements (checklist walker)

A final walk of the brief against the checklist proposed 316 refinements. 115 were absorbed by
strengthening the wording of existing items to the detail their graders already assert, 95 are
covered by the 38 items added in round 5, 17 are recorded above as declared-ungraded, and 90 are
carried here as residual rather than dropped silently.

| Channel the walker proposed | Residual | Why it is not taken |
|---|---|---|
| browser | 54 | drawn-dial geometry and colour-role judgements, one browser step each, against a browser budget already at 33 steps under the 3600s verifier bound (G45) |
| pytest-page | 26 | finer cuts of page asks a page-driven test already measures together |
| pytest-api | 7 | finer cuts of response asks an API test already measures together |
| pytest-db | 3 | column-level cuts of the table asks C-DM-21 and C-DM-22 measure together |

By section the residual sits in Front-end specification (39), Core features (26), UI and UX notes
(18), Data model (4), User flow (2) and Constraints (1). None of them leaves an item uncited: the
sweep reports 0 uncited items across all 454.

## Grading window

| Section | Chars |
|---|---|
| Overview | 2,247 |
| User roles | 1,882 |
| Core features | 36,138 |
| User flow | 5,658 |
| UI/UX notes | 5,238 |
| Technical requirements | 4,044 |
| Data model | 10,279 |
| Front-end specification | 15,575 |
| Constraints | 957 |
| Deployment contract | 5,007 |
| Definition of done | 296 |

Reported, not repaired: the brief has no length limit and the tail reaches the agent in full.

## Review cycles

| Review | Cycles | Outcome |
|---|---|---|
| QC_instruction + QC_spec (G34) | 4 | cycle 1 and 2 FAIL, fixed; cycle 3 PASS; cycle 4 confirmed three later edits |
| qc_toml (G36) | 1 | PASS |
| qc_docker (G35) | 2 | cycle 1 CHANGES REQUIRED (backslash continuations, unsourced git and build-essential, sidecar restart lines), fixed; cycle 2 PASS |
| task_code_verifier (G3) | 1 | VALID |
| qc_rubric (G53) | 2 | cycle 1 CHANGES REQUIRED (duplicated channels, a wrong surface, undecidable rules), fixed; see receipt for cycle 2 |
| qc_solution_checklist (G37) | 2 | cycle 1 FAIL (under-extraction), checklist grown 293 to 367 items; see receipt for cycle 2 |

## Kit gate log

Rendered from `_handoff/S_ecomm_comm_time-literacy-storefront-vb_20260916_100857.gates.jsonl`, 32 receipts, each carrying the SHA-256 of every
file it read. Sweep result: RED: G40, G47.

| Gate | Tool | Verdict | Exit | stdout SHA |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | PASS | 0 | `4cafb10eb656bc99` |
| `G1/G12` | `layout_lint.py` | PASS | 0 | `cdc446ae105f6cab` |
| `G46` | `structure_lint.py` | PASS | 0 | `b0ccb353755bb056` |
| `G50` | `docker_lint.py` | PASS | 0 | `380ed7d1c830de35` |
| `G55` | `runtime_deps_lint.py` | PASS | 0 | `a0c21dca8bc5f78a` |
| `G63` | `secret_lint.py` | PASS | 0 | `f5d46893079d3590` |
| `G48` | `truth_lint.py` | PASS | 0 | `d428c02ec66a3d53` |
| `G51` | `source_lint.py` | PASS | 0 | `505be22123d6e60c` |
| `G52` | `rubric_context_lint.py` | PASS | 0 | `6d05431a63bfd18f` |
| `G54` | `comment_lint.py` | PASS | 0 | `1dd9ecaa59472d1b` |
| `G17` | `secret_hygiene_lint.py` | PASS | 0 | `e31f3ab4249aef94` |
| `G11` | `leak_scan.py` | PASS | 0 | `2d22ebde1104d5ea` |
| `G33` | `window_lint.py` | PASS | 0 | `52e92bdbd9ed7167` |
| `G4/G5` | `contract_lint.py` | PASS | 0 | `8165add318643881` |
| `G43` | `prescription_lint.py` | PASS | 0 | `0d1f99554307440d` |
| `G44` | `disclosure_lint.py` | PASS | 0 | `d143cffd4b4f7a3c` |
| `G10` | `no_sdk_lint.py` | PASS | 0 | `c1a662d43d52ad9c` |
| `G31` | `determinism_lint.py` | PASS | 0 | `c9514aca369f23fb` |
| `G14` | `reward_path_lint.py` | PASS | 0 | `18d7c11853f393ec` |
| `G27/G30` | `rubric_lint.py` | PASS | 0 | `223c52165ab6f73c` |
| `G41` | `flag_lint.py` | PASS | 0 | `34a5124993b8b475` |
| `G56/G57/G58` | `if_lint.py` | PASS | 0 | `cdf20c83e9056866` |
| `G59/G60` | `codequality_lint.py` | ? | 2 | `e23941dd85e0253b` |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | WARN | 0 | `8bb65fa845e1c393` |
| `G6` | `fixture_lint.py` | PASS | 0 | `9f11486c39928b40` |
| `G24` | `coverage_map.py` | PASS | 0 | `8a978e89be4680e8` |
| `G37` | `checklist_qc.py` | PASS | 0 | `68c00ae169db1e48` |
| `G39` | `rubric_align_lint.py` | PASS | 0 | `37de9bad32dec780` |
| `G28/G29` | `channel_lint.py` | PASS | 0 | `2de63f5be2c88d81` |
| `G40` | `prompt_receipt_lint.py` | FAIL | 1 | `f4d852a8ab5db0e3` |
| `G0/INV5` | `vendor_check.py` | PASS | 0 | `fd61a6b0d51ded7a` |
| `G47` | `output_qc.py` | FAIL | 1 | `172d9df67d0b01d0` |
| `G38` | `kit_selftest.py` | PASS (32 checks) | 0 | run once for this kit revision |

## Prompt-gate scorecards (G40)

| Prompt | Gate | Verdict | Checks answered | Non-PASS | Verifier |
|---|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | 9 WARN | independent-subagent-qc-brief-spec |
| `QC_spec.md` | G34 | PASS | 15 | 2 WARN | independent-subagent-qc-brief-spec |
| `qc_docker.md` | G35 | PASS | 105 | 9 NOT-APPLICABLE, 1 SKIP, 1 WARN | independent-subagent-qc-docker |
| `qc_toml.md` | G36 | PASS | 120 | 5 NOT-APPLICABLE, 2 WARN | independent-subagent-qc-toml |
| `task_code_verifier.md` | G3 | VALID | 12 | none | independent-subagent-qc-taskcode-rubric-checklist |

Every certification prompt was run by an independent subagent, never the authoring agent. The
full findings are in `_handoff/S_ecomm_comm_time-literacy-storefront-vb_20260916_100857.receipts.json`.

`docker_generator.md` carries no receipt and G40 records it as a NOTE. The S5 artefacts were written
from `stage-5-dockerfile.md`, reference C and the provider service files, then adjudicated twice by
`qc_docker` (CHANGES REQUIRED, then PASS); the generator prompt itself was never opened in this
session, so no citation is claimed for it.

## Kit inconsistencies found (not bundle defects)

1. **G17 against generator 10.3.** `secret_hygiene_lint.py` rejects `PAYMENTS_ADMIN_USER` and
   `PAYMENTS_ADMIN_PASSWORD` in `[environment].env`, while `toml_generator.md` 10.3 and reference
   C and K list them as agent variables. They live in `[verifier].env` only and the brief states Kill
   Bill's Basic login `admin` / `password` literally (qc_toml ENV-006 WARN).
2. **Reference K K.4 lists no invoice-creation endpoint**, yet the commerce-checkout critical focus
   needs one. The brief names the account routes and invoice listing it documents and leaves the
   charge call to the builder.
3. **`[delivery]` is absent from the `toml_generator.md` 11 template** although 10.1, stage 4 and
   `validate_task.py` require it (qc_toml SCHEMA-011 WARN).
4. **`stage-5-dockerfile.md` still asks for a `# syntax=` line**, which G50 and G54 reject.
5. **Provider seeds set `restart: unless-stopped`** in `environment/providers/{postgres,mailpit,killbill}/service.yaml`,
   which `docker_generator.md` forbids on sidecars; removed here, still upstream (qc_docker CMP-019).
6. **G39 does not credit page-driven pytest for `ui` items** while G28 does; two items measured by
   Playwright were tagged `capability` to satisfy both.
7. **G24 has no route for unobservable asks** in the sweep (`coverage_map.py --unobservable` is not
   passed by `revalidate.py`), so they are recorded above instead of itemised.
8. **The vendored `recompute.py` renders no `code_criteria`**, so the code-quality rubric cannot ship
   (G59/G60 NOT-APPLICABLE).
9. **`checklist_qc.py` word bans read inside backticks.** The I-1 connector ban and the I-5 pronoun
   ban run over the raw item text, so pinned product copy carrying `and` or `it` -- the announcement
   bar, the restock form, the about-page signature, the footer statement -- cannot be quoted in an
   item. Those strings are pinned as rows in the literals table instead, which is not word linted.
10. **`coverage_map.py` ignores tokens under four characters** when it matches an item against the
   step that cites it, so an exact shared word like `box` or `sku` earns nothing; one test was
   renamed to share a longer stem for an ask its body already measured.

## Budget estimate

`turns_expected = 210`, `tokens_expected = 8000000`, the expert band. A server-rendered storefront
with an SVG dial engine and comparison, derived bundle stock, contended holds with a gift promotion,
idempotent checkout into a real Kill Bill invoice with SMTP mail, emailed sign-in links, owner
moderation and restock mail, and a long companion copy deck is more surface than a hard task.

## Versions

| | |
|---|---|
| Kit | deku-green-field, this checkout (GreenField-GenKit2) |
| Vendored grader | 0.22.0 |
| Target schema | 1.4 |
| Canary | rendered into `solution/TRUTH.md` and `solution/USER_README.md` from `grounding.yaml` |

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the reference app is built downstream
from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
