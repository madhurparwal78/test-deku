# Build report - S_ecomm_comm_travel-luggage-storefront-vb_20260916_121653

| | |
|---|---|
| Task code | `S_ecomm_comm_travel-luggage-storefront-vb_20260916_121653` |
| Task id | `deku/travel-luggage-storefront-vb` |
| Cell | solo_founder / ecommerce-retail / commerce-checkout |
| Service profile | `P5-db-pay-email` |
| Providers | `backend` = `postgres`, `email` = `mailpit`, `payments` = `killbill` |
| Variant | `b` on axes ['critical_depth', 'spec_sections'] |
| Language | `typescript` |
| Capability flags | `aesthetic` |
| Design direction | `companion` |
| Launch surface | `custom_404,favicon,no_broken_links,privacy_page,single_cta` |
| Spec sections given | ['overview', 'roles', 'features', 'flow', 'uiux', 'frontend', 'techrequirements', 'datamodel', 'constraints', 'contract'] |
| Shard | 1 of 1 |
| Kit | deku-green-field, gate index G0-G63 |
| Grader pin | `0.22.0` |
| Target schema | `1.4` |
| Verifier mode | `separate` |
| Built at | `Output/S_ecomm_comm_travel-luggage-storefront-vb_20260916_121653/` |
| Delivered to | `/home/grt/Downloads/Greenfield_testing/GreenField-GenKit2/output/16-sep-2026/S_ecomm_comm_travel-luggage-storefront-vb_20260916_121653/` |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Task Order and taxonomy recast

The Task Order (`task-orders/travel-luggage-storefront.yaml`) was written from the tasker's inputs:
`solo_founder` / `ecommerce-retail` / `transactional-checkout` / `travel-luggage-storefront`.
`transactional-checkout` is not a pattern in reference/A A.3, so the order was recast to the legal
`commerce-checkout` before the mint. That pattern keeps the idea intact: a cart, a checkout and a
paid order on a database plus a payments provider, with the email slot added for the
confirmation.

| Field | Tasker input | Emitted |
|---|---|---|
| category | solo_founder | solo_founder |
| domain | ecommerce-retail | ecommerce-retail |
| pattern | transactional-checkout | commerce-checkout |
| archetype | travel-luggage-storefront | travel-luggage-storefront |
| variant | (absent) | b |
| QL / contributor | utsav.jain@ethara.ai / anuj.soni@ethara.ai | `[task].authors`, `contributor_id` |

## Output placement

The operator asked for the task under `GreenField-GenKit2/output/16-sep-2026`. G46 (CON-1)
rejects a bundle built inside the kit tree, so the bundle was built and swept at the kit's
sibling output root, `Output/`, and then copied, with its spec folder, to the requested folder.
The copy is byte-identical; the receipts describe these bytes.

## Source material

The tasker supplied `/home/grt/Downloads/Greenfield_testing/prd/mokobara_prd.md`, a measured capture of the reference storefront,
and it is carried in full. G51 was run against it: 97/97 topics and 353/353 enumerated items
carried, with four author waivers for capture meta (24.1 The capture, 24.5 Observed
implementation, 24.6 Deliberate scope cuts, 25 Acceptance checklist). The companion carry table
sits in `Output/_spec/<code>/00-decisions.md`.

Following the operator's instructions, the section-length targets are waived and the brief
describes every interface element in words: it names no pixel, position, size, colour code,
animation or motion name, curve, function name or parameter value. It does name the stack. The
measured values live in `00-decisions.md` and `04-uiux-brief.md` only. G43 (prescription) and G44
(disclosure) are green on that text.

## Derived design draws

Drawn by SHA-256 over `[metadata].archetype`, never chosen:

```
draw: render_model = spa-json-api
draw: backend = Express
draw: frontend = Svelte + Vite
draw: design_direction = companion
draw: nav = sidebar-nav
draw: work_surface = table-first
draw: create_flow = slide-over
draw: feedback = toast
draw: launch_surface = custom_404,favicon,no_broken_links,privacy_page,single_cta
```

The design-direction draw returned `editorial-serif`. A measured companion was supplied, so
reference/L L.6.1 applies and `design_direction = "companion"` governs.

## Payments narrowing

The commerce-checkout row of reference/B names "an invoice on the account for the right amount"
as the critical focus. The 0.22.0 killbill surface exposes accounts only, so no grader can read an
invoice or a charge amount at the provider. The observable is narrowed to: every paid order names
a billing account, `valisette-<number>`, that exists in `killbill`, and the order becomes `paid`
only after the app reads that account back. Amounts are graded from PostgreSQL and from the
confirmation email in Mailpit. Corporate billing reuses the three seeded killbill accounts
(`orbit-northwind` in USD takes the order; `orbit-acme` and `orbit-amelia` in EUR are refused).

## Feature resolution

| Candidate | Verdict | Where it landed | Reason |
|---|---|---|---|
| Catalogue on a size axis and a collection axis, colourways with own stock and price | INCLUDED | Overview, Core features | PRD 1, 9, 10, 20 |
| Thirty-one rule-driven collections with sort, filter and paging on the server | INCLUDED | Core features, Front-end specification | PRD 9; membership derived, never hand-kept |
| The running sale derived at read time, with a server-clock countdown | INCLUDED | Core features | PRD 10.4, 20.2 item 5 |
| Token cart, stock bound read at every change, personalisation as recorded intent | INCLUDED | Core features | PRD 10.6, 11.1, 11.2 |
| Checkout with price re-read, locked stock step, billing account, one transaction, idempotent key | INCLUDED | Core features, Data model | PRD 11.3, 20.4 |
| Confirmation email through Mailpit | INCLUDED | Core features | the idea's confirmation; email slot |
| Accounts, order history, saved addresses | INCLUDED | Core features, Front-end specification | PRD 13 |
| Owner endpoints for renames, prices, delisting, stock movements, sale end, fulfil and cancel | INCLUDED | User roles, Core features | stock as an append-only ledger (PRD 20.2) |
| Store directory, search, newsletter, gift card balance | INCLUDED | Core features | PRD 12, 14, 5.5 |
| Ten standing pages, privacy statement, own not-found page, favicon | INCLUDED | Core features | PRD 15 plus the drawn launch surface |
| Drawn product pictures, editorial tiles, video still and icons | INCLUDED | Front-end specification | PRD 23 zero-asset substitution |
| Full chrome, home, collection, product, cart, checkout, account and phone layouts | INCLUDED | UI/UX notes, Front-end specification | PRD 2 to 18, in words |
| Invoices or charge amounts at the provider | DROPPED | - | killbill exposes accounts only at grader 0.22.0 |
| Card entry, tokens, declines, refunds, payment callbacks | DROPPED | - | no card processor in the environment |
| Store map, geolocation, distance sort | DROPPED | - | no map provider |
| Personalisation preview and generated artwork | DROPPED | - | PRD 10.6 records intent only |
| Licensed web font, photography, video files | DROPPED | - | zero-asset rule; system font and drawn pictures instead |
| Third-party analytics, instalment and identity widgets | DROPPED | - | Constraints bullet 8 |
| Owner console in the browser | DROPPED | - | owner work through endpoints only |
| Stdout logging, Core Web Vitals figures | DROPPED | - | no channel observes them |

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_paid_order_rows_are_persisted_with_captured_prices` (critical), `test_stock_equals_the_sum_of_movements` (critical), plus the seed and table tests |
| `email` | `mailpit` | MET | `test_confirmation_email_is_delivered_once` (critical), `test_confirmation_email_names_the_order`, `test_reset_email_goes_to_known_addresses_only` |
| `payments` | `killbill` | MET | `test_checkout_opens_the_billing_account_in_killbill` (critical), `test_unknown_corporate_account_is_refused` (critical), `test_provider_refuses_a_reused_external_key`, `test_seeded_billing_accounts_exist_in_killbill` |

No slot is UNMET.

## Graders

- Workflows: **16** (solo_founder band 10-16)
- Browser substeps: **68** - pytest substeps: **163** - ratio **0.42** (G45 band 0.40-2.00)
- Critical substeps: **14**
- Non-happy-path workflow ids: `shopper_filters_a_collection_down_to_empty`, `expired_sale_reprices_the_cart`, `concurrent_checkouts_for_the_last_unit`, `cart_quantity_limit_holds`, `customer_cannot_read_another_customers_order`, `customer_denied_owner_endpoints`, `invalid_checkout_or_corporate_account_is_refused`
- One pytest module, `tests/test_output.py`, **163** tests across accounts, catalogue, collections, the sale, carts, checkout, killbill billing, confirmation email, orders, addresses, stock movements, owner edits, search, stores, standing pages, the not-found page and the page-driven front-end hooks (Playwright `page` fixture defined in conftest).
- Checklist: **943** items across 10 section codes (`capability` 228, `constraint` 201, `contract` 27, `data` 40, `literal` 251, `role` 38, `ui` 158)
- Shared state a test moves (the sale end, stock, a product's title, price or listing) is restored in a `finally` block, so the suite can run after the browser pass and run twice.

### Declared but ungraded by an automated channel

One browser substep carries an `earned:` note. These items live on the agent container, which a separate-mode grader cannot read. The substep proves the seeded login they carry works; the operator observes the rest by hand at the oracle run.

| Item | What it covers |
|---|---|
| `C-TR-05` | The back end is Express on Node.js 20 in TypeScript, serving `/api` with the built front end. |
| `C-TR-19` | The app adds no second database, cache, queue, object store, identity provider or mail vendor. |
| `C-TR-20` | Every host, port, credential is read from the environment. |
| `C-DM-01` | `/app/USER_README.md` lists each seeded account with `deku-demo-pw-2026`. |
| `C-DC-02` | The port mapping is `${APP_PUBLIC_PORT}:4173`. |
| `C-DC-03` | `4173` is the container-internal port, both ports read from the environment. |
| `C-DC-06` | The app starts from the environment image with no manual steps. |
| `C-DC-07` | Login credentials are written to `/app/USER_README.md`. |
| `C-DC-08` | Reserved `.browser_screenshots/` with `.downloads/` directories exist at the app root, empty. |
| `C-DC-12` | The backing services are already running; the app downloads, installs, starts no copy. |
| `C-DC-13` | The app uses only the named providers, with no edge functions. |
| `C-DC-14` | The app relies on no persistent volumes, fixed container names, custom networks. |
| `C-TR-29` | The app uses only the named libraries plus their direct dependencies. |

## Rubric

54 judged criteria: 43 positive totalling 113, 11 negative (total magnitude 35). Every negative has its own checklist obligations and mirrors no positive. The operator's request for detailed UI and UX yields 158 `ui` items, every one claimed by exactly one criterion (G39, G28/G29).

| Dimension | Criteria | Positive share | Target | Delta |
|---|---|---|---|---|
| `instruction_following` | 13 | 0.301 | 0.30 | +0.001 |
| `functionality` | 11 | 0.177 | 0.25 | -0.073 |
| `ux_flow` | 4 | 0.124 | 0.15 | -0.026 |
| `ui_visual` | 16 | 0.204 | 0.15 | +0.054 |
| `motion` | 3 | 0.044 | 0.05 | -0.006 |
| `accessibility` | 4 | 0.088 | 0.05 | +0.038 |
| `responsiveness` | 3 | 0.062 | 0.05 | +0.012 |

Task-completion share 0.69 (band 0.60-0.80). The rubric is GENERATED from `judged_criteria` in `solution/trinity/grounding.yaml`; G48 re-runs the generator under `--check` on every sweep.

## Literals ledger

548 pinned values, every one present verbatim in `instruction.md` and in at least one grader:

| Class | Count |
|---|---|
| `account` | 7 |
| `credential` | 1 |
| `error_code` | 21 |
| `literal` | 476 |
| `message` | 13 |
| `order_number` | 4 |
| `route` | 16 |
| `sku` | 10 |

No value is `verifier_only` in the ledger; the verifier-only credentials (`DB_ADMIN_URL`, `EMAIL_INBOX_API_URL`, `PAYMENTS_ADMIN_USER`, `PAYMENTS_ADMIN_PASSWORD`) live in `task.toml` `[verifier].env` alone (INV4). The checklist lists three values the brief refers to without pinning: the non-luggage figures, the swatch colour values and the description blocks.

## Spec folder

Written to `Output/_spec/<code>/` (and copied beside the delivered bundle), never inside the bundle (CON-5).

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the taxonomy recast, the residual judgment calls, the companion carry table |
| `01-PRD.md` | Overview, Core features, Constraints |
| `02-TRD.md` | Technical requirements |
| `03-app-flow.md` | User flow, the API table, error codes |
| `04-uiux-brief.md` | UI/UX notes, Front-end specification (measured values stay here, never in the brief) |
| `05-backend-schema.md` | Data model, User roles, named storage constraints, seed tables |
| `06-implementation-plan.md` | author-side only; Build plan is not emitted |

## Grading window

```
section        H2                chars  reference  flag
core_features  Core features     42342       2400  past-slice
user_flow      User flow          6861       1900  past-slice
ui_ux_notes    UI/UX notes       11470       1700  past-slice
constraints    Constraints        1219        800  over-reference
user_roles     User roles         1909       1000  over-reference
overview       Overview           2101        700  over-reference
joined total                     65902       8800  past-slice
first four                       61892       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```

The operator waived the section targets so the brief could describe every UI and UX element in
full. G33 measures length and fails nothing on it. Content past the slice still reaches the agent
in full but not the advisory judge; `judge_score` never touches reward. The prompt receipts record
this again as QC_instruction C7.

## Kit gate log

Rendered from `_handoff/<code>.gates.jsonl`. Never transcribed.

| Gate | Tool | Exit | Verdict | Seconds |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | 0.04 |
| `G1/G12` | `layout_lint.py` | 0 | PASS | 0.03 |
| `G46` | `structure_lint.py` | 0 | PASS | 0.04 |
| `G50` | `docker_lint.py` | 0 | PASS | 0.02 |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | 0.04 |
| `G63` | `secret_lint.py` | 0 | PASS | 0.03 |
| `G48` | `truth_lint.py` | 0 | PASS | 0.39 |
| `G51` | `source_lint.py` | 0 | PASS | 0.06 |
| `G52` | `rubric_context_lint.py` | 0 | PASS | 0.04 |
| `G54` | `comment_lint.py` | 0 | PASS | 0.03 |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | 0.04 |
| `G11` | `leak_scan.py` | 0 | PASS | 0.05 |
| `G33` | `window_lint.py` | 0 | PASS | 0.03 |
| `G4/G5` | `contract_lint.py` | 0 | PASS | 0.05 |
| `G43` | `prescription_lint.py` | 0 | PASS | 0.1 |
| `G44` | `disclosure_lint.py` | 0 | PASS | 0.05 |
| `G10` | `no_sdk_lint.py` | 0 | PASS | 0.12 |
| `G31` | `determinism_lint.py` | 0 | PASS | 0.19 |
| `G14` | `reward_path_lint.py` | 0 | PASS | 0.04 |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | 0.05 |
| `G41` | `flag_lint.py` | 0 | PASS | 0.07 |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | 0.03 |
| `G59/G60` | `codequality_lint.py` | 2 | ? | 0.04 |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | 0.12 |
| `G6` | `fixture_lint.py` | 0 | PASS | 0.26 |
| `G24` | `coverage_map.py` | 0 | PASS | 0.15 |
| `G37` | `checklist_qc.py` | 0 | PASS | 0.14 |
| `G39` | `rubric_align_lint.py` | 0 | PASS | 0.19 |
| `G28/G29` | `channel_lint.py` | 0 | PASS | 0.1 |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | 0.06 |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | 0.04 |
| `G47` | `output_qc.py` | 0 | PASS | 0.08 |

`G59/G60` exits 2 with no verdict: the code rubric has no generator in this kit revision, so the sweep records the row as not applicable. `G40` is WARN because every receipt is self-attested. `G63` and `G41` pass with standing WARNs: Kill Bill's built-in `admin`/`password` credential is an upstream pin, and `## Core features` runs past the judge's slice by the operator's waiver.

Corpus-level gates, run once over the output root:

| Gate | Tool | Verdict |
|---|---|---|
| `G42` | `corpus_overlap.py` | PASS - 26 bundles, 1 cross-archetype pair compared, none over 60% substep overlap |
| `G49` | `diversity_lint.py` | PASS (WARN mode) - one concentration finding: `design_direction` is 35% `companion` (9/26) against a 30% cap. This bundle is one of the nine, and L.6.1 requires `companion` whenever a measured companion is supplied. An earlier verbatim-run finding against the sibling bundle's UI/UX notes was fixed by rewording three sentences for this product. |
| `G61` | `corpus_report.py` | NOT-APPLICABLE - 26 minted, 26 unproven; no admissible bundle to measure a mix against |
| `G38` | `kit_selftest.py` | PASS - 32 cross-file agreement checks |

## Prompt receipts

`_handoff/<code>.receipts.json`, 292 declared checks answered across 13 prompts.

| Prompt | Gate | Verdict | Checks | Non-PASS |
|---|---|---|---|---|
| `docker_generator.md` | S5 | PASS | 0 | - |
| `generate_instruction.md` | S2 | PASS | 0 | - |
| `pytest_generator.md` | S7 | PASS | 0 | - |
| `qc_docker.md` | G35 | PASS | 105 | ARCH-002 NOT-APPLICABLE, BP-003 WARN, CMP-007 WARN, CMP-011 WARN, CMP-021 WARN, CON-006 WARN, DEP-004 WARN, DEP-011 NOT-APPLICABLE, DEP-016 NOT-APPLICABLE, DEP-017 NOT-APPLICABLE |
| `QC_instruction.md` | G34 | PASS | 24 | A1 WARN, A8 WARN, B1 WARN, B2 WARN, B3 WARN, C4 WARN, C5 WARN, C7 WARN |
| `qc_rubric.md` | G53 | PASS | 16 | RC-13 WARN |
| `qc_solution_checklist.md` | G37 | PASS | 0 | - |
| `QC_spec.md` | G34 | PASS | 15 | B1 WARN, S3 WARN, S5 WARN |
| `qc_toml.md` | G36 | PASS | 120 | BENCH-002 NOT-APPLICABLE, INST-007 NOT-APPLICABLE, SCHEMA-011 WARN, SCHEMA-013 WARN, SIGN-001 NOT-APPLICABLE, SIGN-002 NOT-APPLICABLE, SIGN-003 NOT-APPLICABLE, TAX-012 WARN, VERIF-005 WARN |
| `rubric_author.md` | S8 | PASS | 0 | - |
| `solution_checklist.md` | S3 | PASS | 0 | - |
| `task_code_verifier.md` | G3 | VALID | 12 | - |
| `toml_generator.md` | S4 | PASS | 0 | - |

Every receipt is SELF-ATTESTED: the QC prompts were run by reviewer sub-agents of the same run, so owner and verifier are one run. The kit requires owner != verifier, so these are recorded verdicts, not independent ones. The non-PASS findings:

- `qc_docker.md` DEP-004 WARN: environment/Dockerfile installs the grader runtime (pytest==8.4.1 pytest-json-ctrf==0.3.5 httpx==0.28.1 pyyaml==6.0.2 psycopg[binary]==3.2.3 boto3==1.35.99 playwright==1.49.1, the 21 Chromium libraries, `playwright install chromium`) although task.toml sets [verifier].environment_mode = "separate", so the grader runs in its own image from tests/Dockerfile. This is the settled kit stance: keep it so the image works under either mode (reference/C C.4 carve-out; G55 RD-1 skips under separate). Contradiction: qc_docker DEP-004/DEP-011 and reference/C C.4 still assume shared mode. Also, `boto3==1.35.99` is outside this task's slot-scoped set. docker_generator.md GRADER RUNTIME section 1 and tools/runtime_deps_lint.py PROVIDER_DRIVERS require boto3 only for minio/floci/floci-docker, and this task declares postgres/mailpit/killbill. But qc_docker DEP-011 and vendor/grader-0.22.0/Dockerfile list it unconditionally. Non-blocking. Optional fix: drop `boto3==1.35.99` from the second `pip install` RUN.
- `qc_docker.md` BP-003 WARN: the `nodejs` package floats within the NodeSource 20.x line (setup_20.x plus an unpinned `apt-get install nodejs`), so the Node patch version depends on build date. The TRD declares only "Node.js 20", and the docker_generator.md SKELETON prescribes exactly this unpinned form, so the file follows Tier 1 (it also guarantees Node >= 20.19, which current Vite requires). npm (10.9.2), the pip set and Chromium (via playwright 1.49.1) are pinned. Non-blocking. Optional fix: pin `nodejs=20.<x>.<y>-1nodesource1`.
- `qc_docker.md` CON-006 WARN: the Dockerfile departs from the docker_generator.md fixed section order and SKELETON in functionally inert ways, none traced to a lower-priority source. (a) Eight RUNs do not open with `set -eux;` (both apt layers, `update-ca-certificates`, `npm install -g`, both pip RUNs, `playwright install chromium`, `mkdir`), against the VALIDATION line "every RUN opens with `set -eux;`". All are single commands or `&&` chains that already fail fast, and the generator's own GRADER RUNTIME section 2 emits `RUN apt-get update && ...` and `RUN playwright install chromium` without it, so the generator contradicts itself. (b) The base-package apt RUN (section 7) comes before the CA-trust RUNs (section 6) and before WORKDIR, and the CHROME_LIBS_A/B build ARGs (section 2) come after the proxy/CA ARGs (section 3). CA trust still precedes the first HTTPS download (NodeSource), and apt uses deb.debian.org over HTTP. (c) The `curl | bash -` pipe has no pipefail under /bin/sh, so a failed download is masked; the build still fails loudly at `npm install -g npm@10.9.2`, because Debian's fallback nodejs 18 ships no npm. The file is byte-identical to three sibling bundles that passed. Non-blocking.
- `qc_docker.md` CMP-007 WARN: `killbill/mariadb:0.24` is a minor-line vendor tag that is re-pushed in place. The registry shows the current linux/amd64 image created 2026-09-09T13:12:38Z with ARG MARIADB_VERSION=1:11.8.9+maria~ubu2404, so the content behind the tag changes without a tag change. It is the pin recorded verbatim in reference/C C.2.1 and environment/providers/killbill/service.yaml, Kill Bill publishes no patch tag for it, and changing it in the bundle would break CMP-004 and G38. Bundle-side this is correct; non-blocking. Kit-level fix: pin the index digest in C.2.1 and the fragment together once an operator verifies it.
- `qc_docker.md` CMP-011 WARN: the literal fail condition ("Any service has a `ports:` key") is met by `main` (`ports: ["4173:4173"]`). That key is MANDATORY under qc_docker CMP-022 (Critical), docker_generator.md THE `main` SERVICE, and validate_task.py C12, so the prompt contradicts itself. Every sidecar (postgres, killbill, killbill-init, killbill-db, mailpit) is free of `ports:`, which is the rule's real subject. No change; the prompt's CMP-011 row should scope itself to sidecars.
- `qc_docker.md` CMP-021 WARN: three standing, kit-convention exposures on the agent-reachable network; none is a bundle defect. (1) The INV4 verifier-only DB_ADMIN_URL user `deku_admin` (POSTGRES_USER, the database superuser) has the same password `deku-local-dev` as the agent's own `deku_app` in DATABASE_URL. The agent can list roles via pg_roles and log in as the superuser, which defeats the "superuser stays with the verifier" intent of providers/postgres/init.sql. This is mandated by toml_generator.md section 10.3, the postgres fragment and qc_toml ENV-006, so a bundle-only change would break CMP-005/ENV-006 alignment. Kit-level fix: give deku_admin a distinct value across the fragment (POSTGRES_PASSWORD), the toml_generator convention and [verifier].env DB_ADMIN_URL together. (2) Kill Bill's built-in admin/password is handed to the agent as PAYMENTS_API_USER/PAYMENTS_API_PASSWORD. reference/C C.2 declares payments credentials legitimately shared, and G63 SEC-3 reports it as a standing WARN (an upstream shiro pin that also exposes the word `password` to Harbor's scrubber). (3) Mailpit's unauthenticated inbox API (mailpit:8025, the INV4 EMAIL_INBOX_API_URL target) is reachable from `main` on the default network; only the URL is withheld. Non-blocking.
- `qc_docker.md` DEP-011 NOT-APPLICABLE: the precondition is `[verifier].environment_mode = "shared"`; task.toml sets "separate". For the record, all seven packages match vendor/grader-0.22.0/Dockerfile pins exactly (pytest 8.4.1, pytest-json-ctrf 0.3.5, httpx 0.28.1, psycopg[binary] 3.2.3, boto3 1.35.99, pyyaml 6.0.2, playwright 1.49.1), and G55 PASS.
- `qc_docker.md` DEP-016 NOT-APPLICABLE: there is no compiled-language build stage ([metadata].language = "typescript") and no COPY instruction at all.
- `qc_docker.md` DEP-017 NOT-APPLICABLE: [metadata].language is "typescript", not "java".
- `qc_docker.md` ARCH-002 NOT-APPLICABLE: no image anywhere (environment/Dockerfile, tests/Dockerfile, compose) is pinned by digest. All six compose/base tags were confirmed as multi-arch OCI or Docker indexes carrying linux/amd64 and linux/arm64.
- `QC_instruction.md` A1 WARN (settled generator plus operator override 3): '## Build plan' is absent. generate_instruction §2.1 does not emit Build plan at baseline, and task.toml spec_sections_given has no 'buildplan' token. The other ten required H2s are present, spelled exactly, in canonical order. The extra '## Front-end specification' is legal: reference/G says it is optional and unbudgeted, token 'frontend' is declared, and it sits after Data model and before Constraints. No fix.
- `QC_instruction.md` A8 WARN (settled kit facts plus operator override 3): the brief reads names outside A8's list. DB_URL (L815) is MINOR under A8, and reference/C §C.2 plus task.toml export it beside DATABASE_URL. PAYMENTS_API_KEY and PAYMENTS_API_SECRET (L819-820) are the killbill auth that reference/C §C.2 and reference/K §K.4 require, and task.toml exports both. PAYMENTS_API_USER and PAYMENTS_API_PASSWORD (L818) are the settled agent credential names; the PAYMENTS_ADMIN_* names collide with G17. No host or port is hardcoded; 4173 is the canonical contract port. No fix.
- `QC_instruction.md` B1 WARN (settled kit fact, reference/A): the commerce-checkout row gives db + payments, PG + killbill, role 'customer'. The brief adds Mailpit and a seeded 'owner'. Neither is creep. reference/A §A.3 makes P5-db-pay-email the only legal profile for solo_founder x commerce-checkout, so the email slot is mandatory for this cell (and the idea asks for a confirmation). reference/A §A.1 gives solo_founder a 1-2 role band. The solo_founder modifier holds: 'Signup is open: every account created at /account/register is a customer' (L56-57). No fix.
- `QC_instruction.md` B2 WARN (settled fact, override 3: killbill exposes accounts only): the row's critical focus, 'Invoice exists on the account, right amount and currency', is narrowed to 'every paid order names a billing account that exists in killbill', as logged in 00-decisions 'Payments narrowing'. The narrowed focus is numbered and attackable. The framing (L8-10) uses requirement form. Checkout rule 6 (L387-394) opens the account with POST /1.0/kb/accounts, reads it back before 'paid', and says 'never marks an order paid on the strength of its own request alone'. Negative cases carry exact rejection outcomes: rule 5 out_of_stock writes 'no billing account'; rule 7 has billing_account_unknown and billing_account_currency with exact messages; rule 9 makes a repeat create 'no second billing account' (provider 409); rule 10 sells the last unit once, never below zero. Amount and currency are graded through the order's `usd` totals and the email opening. No real charge exists (TR L824-825). No fix.
- `QC_instruction.md` B3 WARN (settled generator plus operator override 3): B3 expects variant a with all three lever sections. This task is variant 'b' with variant_axes ['critical_depth','spec_sections']. Technical requirements and Data model are present. Build plan is withheld per generate_instruction §2.1 and spec_sections_given. No fix.
- `QC_instruction.md` C4 WARN (direction complete; justified by operator override 2 plus two notes): palette and type are given in words only, per override 2. The generator's number rule (generate_instruction §4) would carry the exact font family and sizes; 00-decisions records the override. (a) Success and in-progress colour roles are not named. They are implicitly colourless: 'Three colours carry meaning' (L703) plus 'The single green in the product is reserved for the size tile' (L705-706) rule out a success colour, as in companion §3.1's three meaning colours. One explicit sentence would close the axis, e.g. 'success and in-progress carry no colour of their own'. (b) Several palette words differ from the kit's derived vocabulary (source_lint.colour_words on the 04 values): the hairline #E5E7EB derives as 'near-white neutral' (brief: 'light cool neutral'); the divider #DEDEDE as 'near-white neutral' (brief: 'light neutral'); the form border #D1D5DB as 'near-white cool neutral' (brief: 'light cool neutral'); the coverage highlight #FFC314 as 'mid, vivid orange' (brief: 'vivid amber'). Every other axis is present: roles, contrast floors, type by role with aligned figures, shape and density, component states with Escape and confirm-before-destroy, two-curve motion with a complete reduced-motion list, full light-mode commitment, and the WCAG 2.2 AA a11y and responsive bar. There are no hex, px or ms values. No blocking fix.
- `QC_instruction.md` C5 WARN (settled generator conflicts with C5): C5 asks for invariants named as storage-level constraints plus the reminder that app-level checks alone fail. generate_instruction §4 (Data model) says 'At variant b and above, delete that clause', and G43 (prescription_lint PASS) bans naming the index or lock construct. The brief states the invariants as observable storage properties instead: `checkout_key` unique, 'One order per checkout_key, however many times or however simultaneously it is submitted' (L889-890), 'Two checkouts for the last unit ... never both become paid' (L916-917), and 'At most one default address per account' (L871). Derived-on-read values are listed (L898-903), and idempotent seeding is stated (L943-944). No fix.
- `QC_instruction.md` C7 WARN (operator override 1: section length waived): window_lint (current file) gives core_features 42,342 (target 2,400), user_flow 6,861 (1,900), ui_ux_notes 11,453 (1,700), constraints 1,219 (800), user_roles 1,909 (1,000), overview 2,101 (700); joined 65,885. At the judge's 2,500-char slice: Core features is cut inside the '### The catalogue' intro, so every graded rule from the catalogue onward (sale, cart and item_count, stock ceiling, price re-read, payment and billing account, idempotency, last unit, confirmation email) is past the cut. User flow is cut inside journey 1. UI/UX notes is cut inside Palette. The 9,000-char join ends inside User roles, so Overview is never read. The settled generator says 'Do not cut a real rule to fit'; judge_score is advisory and rubric criteria are self-contained. window_lint undercounts the real join by about 130 chars; use QC_V3 C-05 for exact figures. No fix under the waiver.
- `qc_rubric.md` RC-13 WARN (new loop, cycle 1): every share is within 0.10 of its frozen weight: instruction_following 0.301, functionality 0.177, ux_flow 0.124, ui_visual 0.204, motion 0.044, accessibility 0.088, responsiveness 0.062 (43 positive criteria, 113 points). The small-dimension split, motion 3 (R34-R36), accessibility 4 (R37-R40) and responsiveness 3 (R41-R43), exceeds the one-criterion cap in reference/I I.5 and rubric_author check 20. It is kept deliberately at the task owner's explicit request for detailed UI/UX; this WARN records that operator request as the waiver. No fix is required.
- `qc_solution_checklist.md` F1 FIXED: C-FE-138 lists all six exclusion tags, including `Heat, fire & chemicals`, and the browser substep reads them. Evidence: Fixed in cycle 2 and unchanged since. C-FE-138 carries `Heat, fire & chemicals` with a pinned row, and substep coverage_dialog_and_accordions_explain_the_luggage #2 reads it (instruction.md 1171-1173).
- `qc_solution_checklist.md` F2 FIXED: The pinned front-end copy strings are carried by items or pinned rows and graded by browser substeps. Evidence: Fixed in cycle 2 and unchanged since. The only brief values still absent from the checklist are table cells covered by table-level data items, worked-example paths and emails covered by paraphrase or template items, and route paths covered by C-FE-14.
- `qc_solution_checklist.md` F3 FIXED: All cycle-1 declarative asks have items with a channel. Evidence: Unchanged since cycle 2. C-UX-95, C-UX-96, C-FE-202 and C-FE-204 to C-FE-206 are rubric-claimed; C-FE-203 and C-FE-219 to C-FE-223 are browser-graded.
- `qc_solution_checklist.md` F4 FIXED: The API-shape, seed and requirement values are itemised and asserted, and the earned note now covers the library rule. Evidence: The earned note on storefront_is_served_from_a_production_build #1 now reads '... the port mapping and the compose shape and the dependency manifest live on the agent container ...', which covers C-TR-29. The seed and response assertions were verified in cycle 2 and are unchanged.
- `qc_solution_checklist.md` F5 FIXED: C-FE-19 now captures all three parts of the rail-block sentence: both controls on collection pages, SORT BY alone on the search page, and no block on any other page. The comparing substep checks the block is entirely absent elsewhere. Evidence: Re-check at 06:39Z. instruction.md 976-978: '... the search page shows the same block with `SORT BY` alone, and no other page shows it.' C-FE-19: 'The fourth rail block appears on collection pages with `SORT BY` above `FILTER BY`, on the search page with `SORT BY` alone, on no other page.' Browser substep shopper_filters_a_collection_down_to_empty #4 now ends '... the home page, the cart and the store directory show no fourth rail block at all'. The search-page clause is walked by shopper_searches_by_colour #2 ('find SORT BY offered in the rail and FILTER BY absent'), which cites C-FE-176. Non-blocking: C-FE-19 and C-FE-176 now state the search-page fact twice, once from the Rail paragraph and once from the Search page paragraph. Section 3.5 would prefer one item with two citations, but ids are immovable and both items are graded, so nothing is counted wrongly.
- `qc_solution_checklist.md` F6 FIXED: The drawer-heading count is resolved, and C-FE-224 now carries both citations. Evidence: C-FE-224 src reads 'Front-end specification, Cart para; Front-end specification, Product page para' (brief 1209 and 1152-1154). C-FE-127 and C-CF-391 are unchanged from cycle 2 and are graded.
- `qc_solution_checklist.md` F7 FIXED: C-UX-18 now carries only the dialog veil, and rubric R18 claims and grades it. Evidence: C-UX-18: 'The dialog veil sits on translucent black.' C-FE-89 still owns the caption scrim and C-UX-87/C-FE-192 the phone header. The rubric-provenance sidecar moves C-UX-18 from R14 to R18, whose yes-case reads 'the Details dialog on a luggage product sits over a see-through black veil'. The remaining restatement pairs each sit inside one criterion (R2, R6, R42).
- `qc_solution_checklist.md` F8 FIXED: The recount reconciles. My cycle-2 claim that C-UX-96 was mis-cited was wrong; its added second citation is correct. Evidence: Correction: the Motion paragraph already read 'the loading bars hold still' in the 05:51Z copy (snap1 line 759) and still does (line 761). In cycle 2 I relied on my cycle-1 reading of that paragraph, so C-UX-96's original citation was right. Its src now reads 'UI/UX notes, Motion para; Front-end specification, Product card para'. That is a correct section 3.5 double citation, because line 1080-1081 restates the ask. Recount on the 06:31Z file: 943 items (OV 16, RL 40, CF 391, UF 51, UX 96, TR 29, DM 45, FE 238, CN 12, DC 25), equal to the header and to the ledger sum. Ids are contiguous. Tags: 251 literal, 228 capability, 201 constraint, 158 ui, 40 data, 38 role, 27 contract. 592 pinned rows, none pointing at an unknown id. 3 'Referenced but not pinned' rows. Ledger obligation counts equal the checklist_qc proposal.
- `qc_solution_checklist.md` F9 FIXED: The order page content and the sign-in page's account-creation link are itemised and graded. Evidence: New items: C-FE-236 (lines as bought with colourway, size class, quantity, personalisation and captured prices), C-FE-237 (delivery address, state, arrival window, amount charged) and C-FE-238 (create-account link below LOGIN). customer_cannot_read_another_customers_order #3 now reads 'size class cabin, quantity 1, at the captured price $179, then the delivery address 42 Alder Lane, the state Fulfilled, the arrival window and the amount charged $179'. account_holder_signs_in_and_resets_a_password #1 reads 'a link to create an account below the LOGIN button'.
- `qc_solution_checklist.md` F10 FIXED: The twelve visual and layout details are itemised and claimed. Evidence: C-FE-225 to C-FE-235 are ui items, claimed in R11 (C-FE-225), R6 (C-FE-226), R21 (C-FE-227, C-FE-233), R18 (C-FE-228), R20 (C-FE-229), R10 (C-FE-230 to C-FE-232) and R43 (C-FE-234, C-FE-235), each with matching criterion and rule text (G39 158/158). C-FE-141 now includes 'separated by colons', and substep expired_sale_reprices_the_cart #1 reads the colons.
- `QC_spec.md` S3 WARN (settled kit facts plus operator override 3): the 02-TRD stack is complete (frontend, backend, database, auth, health, logging), and the no-second-store line is present (L22-24). Its env list (L17-20) uses names outside §5.2. `DB_URL` is MINOR by §5.2 itself, and reference/C §C.2 and task.toml export it. `PAYMENTS_API_KEY` and `PAYMENTS_API_SECRET` are the killbill auth that reference/C §C.2 and reference/K §K.4 require, and task.toml exports both. `PAYMENTS_API_USER` and `PAYMENTS_API_PASSWORD` are the settled agent credential names; the PAYMENTS_ADMIN_* names collide with G17. Minor: the list is labelled '(canonical)' while it includes off-canon aliases and omits `SMTP_USER`/`SMTP_PASS`, which its own Mail row (L9) names. 02-TRD now also carries the no-credentials-in-the-browser rule (L29-30); the env list is unchanged. No blocking fix.
- `QC_spec.md` S5 WARN (settled kit rules and operator override 2): 04-uiux-brief.md carries a hex palette by role, size/line type pairs, motion values with the reduced-motion rule, the a11y bar (44x44, 4.5:1, visible focus) and a Mode commitment (L3). It does not carry the house values that S5 names (`250ms`, `cubic-bezier(0.16, 1, 0.3, 1)`). Instead it carries the companion's measured §6.1/§6.2 values (`cubic-bezier(0.4, 0, 0.2, 1)`, `cubic-bezier(0.34, 1.56, 0.64, 1)`, 150/175/200/300/350/500/60000ms). With design_direction = "companion", reference/L §L.6.1 makes the companion's measured character govern. The kit itself is split on 04: reference/G §G.2 wants no hex and motion in words, while S5 and operator override 2 put the literal values in 04 only. Both earlier 04 leftovers are fixed: the reduced-motion line lists 'loading bars stop pulsing', and the radius line (L47) now reads '9999px swatches (carousel indicators are thin 24x3px bars)', which agrees with 00-decisions L44 and the brief. No fix.
- `QC_spec.md` B1 WARN (settled kit fact, reference/A): the row gives PG + killbill and role 'customer'. 02-TRD adds Mailpit and 05 adds a seeded `owner`. reference/A §A.3 makes P5-db-pay-email the only legal profile for this cell, so the email slot is mandatory. reference/A §A.1 gives solo_founder a 1-2 role band. The solo_founder open-signup modifier is honoured (05 'Roles': customer by open signup, owner seeded only). No fix.
- `qc_toml.md` SCHEMA-011 WARN: task.toml carries a [delivery] block (format, schema_version, reward_path, reward_key, reward_range, reward_full, network_policy), which the toml_generator.md s11 canonical template does not define. The contradiction is with stage-4-task-toml.md ('Every new bundle must include a [delivery] block'), which the block follows, and validate_task.py G2 lint_delivery validates it (PASS: schema_version equals the top level, network_policy = public). [delivery.images] is omitted, which is correct offline. The template, not the bundle, lags; no bundle change. Kit fix: add [delivery] to the s11 template and to the SCHEMA-011 allow-list.
- `qc_toml.md` TAX-012 WARN: spec_sections_given omits `buildplan` although the SPEC folder holds an implementation plan (_spec/.../06-implementation-plan.md). Under qc_toml TAX-012 read literally, and toml_generator.md s9 ('buildplan -> Implementation Plan doc'; 'sections PRESENT across the SPEC folder'), that is content without its token. The settled kit rule says otherwise, and the bundle follows it: the qc_toml TAX-011 note ('like buildplan it is absent at baseline and present only when the brief emits that H2'), the s11 template list, and generate_instruction.md s2.1 (Build plan NOT baseline). instruction.md has no '## Build plan' H2, and 00-decisions.md records 'the brief has no build plan section'. Each of the 10 emitted tokens maps 1:1 to a brief H2, including `frontend` -> '## Front-end specification', in canonical order. No bundle change. Kit fix: reword TAX-012 and generator s9 to key tokens on the brief's H2s.
- `qc_toml.md` VERIF-005 WARN: [verifier].env has APP_PUBLIC_URL = "${APP_PUBLIC_URL:-http://main:4173}"; VERIF-005, toml_generator.md s10.4 and the s11 template pin the default `http://localhost:4173`. This contradicts VERIF-001 and generator s10.1, which require environment_mode = "separate" (the grader runs in its own image from tests/Dockerfile on deku-verifier-base). In that image `localhost` is the verifier container. tests/test.sh probes ${APP_PUBLIC_URL}/api/health and would score deploy 0.0 against a correct app, so `main:4173` (the compose service that publishes 4173) is the working value; sibling S_creato_cont_remixable-timeline-editor-vb uses it too. No bundle change. Kit fix: update VERIF-005 and generator s10.4/s11 to main:4173 for separate mode.
- `qc_toml.md` SCHEMA-013 WARN: section order is [task], [metadata], [metadata.services], [agent], [environment], [environment.healthcheck], [verifier], [delivery], [[artifacts]]. Every template section keeps its canonical relative order, and [[artifacts]] is still last, as generator s13 requires. The only deviation is the [delivery] section, which the s11 template gives no slot (same root cause as SCHEMA-011). stage-4 requires the block and names no position, so placing it after [verifier] is the kit's working convention. No bundle change.
- `qc_toml.md` BENCH-002 NOT-APPLICABLE: the task is non-trivial (three sidecars, three roles, nineteen tables, last-unit concurrency), so the Trivial tier does not apply; BENCH-001 governs and passes.
- `qc_toml.md` INST-007 NOT-APPLICABLE: instruction.md is present (bundle root, 12 H2 sections) and was read in full for Technical requirements, Constraints and Deployment contract.
- `qc_toml.md` SIGN-001 NOT-APPLICABLE: deprecated 2026-09-15 and superseded by SIGN-004, which passes (no [signoff] table; G62 clean).
- `qc_toml.md` SIGN-002 NOT-APPLICABLE: deprecated 2026-09-15 and superseded by SIGN-004, which passes (no [signoff] table; G62 clean).
- `qc_toml.md` SIGN-003 NOT-APPLICABLE: deprecated 2026-09-15 and superseded by SIGN-004, which passes (no [signoff] table; G62 clean).

## Blocking findings

None open. Resolved rather than shipped:

- **The pattern's invoice observable does not exist at grader 0.22.0.** Narrowed to the billing
  account per paid order (above), recorded in `00-decisions.md`.
- **The provider seed script used a reserved `.example` TLD.** G55 RD-6 flagged the two seeded
  killbill emails; the task copy uses `example.com` addresses.
- **Mailpit's HTTP paths read as unpinned app routes.** G6 harvests every `/api/` string; the
  conftest builds the Mailpit base from separate pieces so only app routes are harvested.
- **One judged-looking item had no observable** (the app adding no second backing service). It
  moved to the earned environment substep and is listed for the hand check, with the library rule.
- **The QC reviews found real defects, and they were fixed rather than waived.** QC_instruction
  found three ambiguities (carousel indicators as discs or bars, the amber rule against the drawn
  amber illustrations, the signed-out order read), a reviewer-facing phrase and an inverted
  reduced-motion clause. qc_rubric found rules that would fail a correct app, four negatives that
  mirrored positives, undefined terms and two criteria a judge could not stage.
  qc_solution_checklist found two brief contradictions (where the sort block and the cart count
  live on the search and product pages), about forty unpinned copy strings and a dozen unitemised
  asks. The brief, checklist (now 943 items), workflows, tests and judged criteria were revised
  together, two page-fixture tests were added, and the reviews were re-run until they converged.
- **qc_toml ENV-006 and qc_docker BLD-005** were fixed in place: `SMTP_USER`/`SMTP_PASS` now ship
  with empty defaults, and the NodeSource setup layer cleans its package lists.

## Budget

`turns_expected` 200, `tokens_expected` 8000000. The reasoning: a two-layer build on one origin
(a Svelte SPA with server-rendered collection pages and an Express JSON API), nineteen tables with
append-only stock and concurrency-safe checkout, a real killbill account per order with read-back,
SMTP confirmation, thirty-one derived collections, and a very detailed drawn front end with phone,
keyboard and reduced-motion behaviour. The token budget sits at the qc_toml ceiling. `difficulty`
stays the empty calibration placeholder.

## Exit

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts this bundle toward corpus targets until the reference app is built
downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
