# Build report - S_saasm_crud_animation-library-catalogue-vb_20260916_090008

## Identity

| Field | Value |
|---|---|
| task code | `S_saasm_crud_animation-library-catalogue-vb_20260916_090008` |
| task id | `deku/animation-library-catalogue-vb` |
| cell | solo_founder / saas-micro-tools / crud-catalog |
| service_profile | `P5-db-pay-email` |
| providers | `backend = postgres`, `payments = killbill`, `email = mailpit` |
| variant | `b` on `critical_depth` and `spec_sections` |
| language | `typescript` |
| design_direction | `companion` (the draw for this archetype, `warm-hospitality`, is recorded and does not govern) |
| launch_surface | `favicon,meta_tags,privacy_page,security_headers,terms_page` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 (single-operator run) |
| kit revision | `806eb0a` |
| vendored grader | `0.22.0` |
| verifier mode | `separate` |
| pytest module | `tests/test_output.py` |
| target schema | `1.4` |
| exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

Two Task Order fields are not kit enum members and were mapped, not silently re-keyed:
`domain: saas-productivity` became `saas-micro-tools`, and `pattern: catalog-browse` became
`crud-catalog`. The companion's own Section 37.7 records the same reasoning. Both are in
`_spec/.../00-decisions.md`.

Every derived-design value is drawn from `sha256("animation-library-catalogue")`:
`render_model = ssr-islands`, `backend = Hono`, `frontend = Nuxt 3`, `nav = top-nav`,
`work_surface = card-grid`, `create_flow = modal`, `feedback = optimistic-row`.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Versioned documentation for three runtimes | INCLUDED | ## Core features 1 | named in the Task Order; the unversioned and versioned addresses are the contract |
| The filterable example gallery | INCLUDED | ## Core features 2 | the Task Order's 'browses the gallery, filters it by runtime and category'; facets as addresses |
| The section library and theme file | INCLUDED | ## Core features 3 | the Task Order's 'pre-built interface sections'; nine measured categories, twelve theme values |
| The live preview | INCLUDED | ## Core features 4 | the Task Order's 'opens a live preview'; the enforceable half of the isolation model |
| Lifetime access | INCLUDED | ## Core features 5 | the Task Order's 'buys lifetime access'; carries the payments and email slots |
| Entitlement | INCLUDED | ## Core features 6 | the only thing standing between the paid source and anyone asking for it |
| Saved examples | INCLUDED | ## Core features 7 | the Task Order's 'saves an example to their account'; carries the crud-catalog critical focus |
| The member showcase | INCLUDED | ## Core features 8 | named in the Task Order; the human publish decision stays inside one role |
| The changelog and the magazine | INCLUDED | ## Core features 9 | named in the Task Order; one dated record shape |
| The site's own surface | INCLUDED | ## Core features 10 | the five drawn launch-surface obligations plus the server-rendered not-found status |
| Accounts | INCLUDED | ## Core features ### Auth | required once a purchase and a save need an owner |
| Per-seat team plan | DROPPED | ## Constraints bullet 2 | companion 27.1, 27.5, 13.3; a renewal on a deployment whose billing catalog is empty |
| Refunds, dunning, tax | DROPPED | ## Constraints bullets 3-4 | companion 27.4, 27.6, 27.7; not referenceable on the Kill Bill surface |
| Animation performance audit service | DROPPED | ## Constraints bullet 5 | companion 29; a worker fleet and a grading service are a task of their own |
| Agent context service | DROPPED | ## Constraints bullet 6 | companion 30; outside the Task Order |
| Moderation worker and transcoding | DROPPED | ## Constraints bullet 7 | companion 31.4-31.8; the human decision is kept, the machinery is not |
| Site-wide search overlay | DROPPED | ## Constraints bullet 9 | companion 25.6-25.7; the gallery's own narrowing carries the findable subjects |
| Book, sponsor, advertise, troubleshooting routes | DROPPED | ## Constraints bullet 10 | companion 2.2, 16.5; advertised but outside the Task Order |
| Five uncaptured section categories | DROPPED | 00-decisions | companion 37.1 names them without blurbs; inventing blurbs would be invented fact |
| Distinct registrable preview origin | DROPPED | waived on G51 (`registrable`) | companion 28.2; impossible on one origin, so feature 4 carries the enforceable half |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | postgres | MET | `test_a_saved_row_survives_a_reload_and_matches_the_grid` (critical) writes a save and reads the stored row back through the shared adapter; `test_seeded_accounts_are_stored_once_with_hashed_passwords` (critical) and the content-row and foreign-key graders read the same store |
| `payments` | killbill | MET, NARROWED | `test_a_purchase_creates_one_billing_account_under_the_licence_key` (critical) reads the account back from Kill Bill by external key, with name, address, currency and country; `test_a_repeated_purchase_is_refused_by_the_billing_key_conflict` (critical) proves the repeat is refused by the platform's own key uniqueness. No invoice is asserted: see Blocking findings 1 |
| `email` | mailpit | MET | `test_the_receipt_mail_reaches_the_buyer_inbox_and_nobody_else` (critical) reads Mailpit for exactly one receipt to the buyer alone with the pinned subject prefix; `test_a_refused_purchase_sends_no_mail_at_all` asserts the inbox is unchanged after a refusal |

## Grading surface

| Measure | Value |
|---|---|
| workflows | 16 (solo_founder band 10-16) |
| browser substeps | 32 |
| pytest substeps | 66 |
| browser:pytest ratio | 0.48 (G45 band 0.40-2.00) |
| critical substeps | 10 |
| non-happy-path workflow ids | 3 |
| judged criteria | 13 positive, 0 negative |
| checklist items | 678 |

Category mix: `business_rule` 17, `core_outcome` 2, `data_integrity` 14, `notification` 2, `presentation` 15, `security` 13, `validation` 3.

| Workflow id | Browser | Pytest | Critical |
|---|---|---|---|
| `seeded_catalogue_is_served_from_one_origin` | 2 | 8 | 0 |
| `wrong_password_login_is_refused` | 1 | 4 | 2 |
| `gallery_facets_are_shareable_addresses` | 3 | 3 | 1 |
| `gallery_facets_split_access_and_order_the_grid` | 1 | 4 | 0 |
| `an_example_page_shows_the_source_it_may_show` | 2 | 2 | 0 |
| `paid_source_is_denied_to_an_unlicensed_reader` | 2 | 6 | 1 |
| `the_preview_frame_reaches_nothing` | 1 | 3 | 1 |
| `the_paid_route_shows_only_the_band_that_applies` | 2 | 3 | 0 |
| `one_payment_writes_one_billing_account` | 2 | 4 | 2 |
| `a_repeat_purchase_hits_the_billing_key_conflict` | 1 | 2 | 1 |
| `a_saved_row_survives_a_reload` | 3 | 4 | 1 |
| `a_save_begun_signed_out_completes_after_signing_in` | 2 | 1 | 0 |
| `a_submitted_project_stays_its_owner_s_own` | 2 | 3 | 1 |
| `the_section_library_counts_and_tunes_itself` | 3 | 5 | 0 |
| `the_manual_and_the_record_answer_for_one_release` | 3 | 9 | 0 |
| `the_site_own_edges_are_designed_not_defaulted` | 2 | 5 | 0 |

## Checklist

| Section | Items |
|---|---|
| `C-CF` | 240 |
| `C-CN` | 17 |
| `C-DC` | 43 |
| `C-DM` | 70 |
| `C-FE` | 101 |
| `C-OV` | 12 |
| `C-RL` | 19 |
| `C-TR` | 71 |
| `C-UF` | 49 |
| `C-UX` | 56 |

Tag mix: `capability` 79, `constraint` 179, `contract` 94, `data` 36, `literal` 131, `role` 8, `ui` 151. Every item names one
grader and shares at least two stemmed words with it (G24); the emitter refuses to write
unless every pytest test, browser substep and judged criterion is cited.

## Judged rubric

| Dimension | Points | Share | Target | Inside 0.10 band |
|---|---|---|---|---|
| `instruction_following` | 13 | 0.277 | 0.30 | yes |
| `functionality` | 15 | 0.319 | 0.25 | yes |
| `ux_flow` | 6 | 0.128 | 0.15 | yes |
| `ui_visual` | 6 | 0.128 | 0.15 | yes |
| `motion` | 3 | 0.064 | 0.05 | yes |
| `accessibility` | 1 | 0.021 | 0.05 | yes |
| `responsiveness` | 3 | 0.064 | 0.05 | yes |

Positive total 47. `task completion` share 9/13, inside the 60-80% band.
`tests/rubric.json` is GENERATED from `solution/trinity/grounding.yaml`; G48 re-runs the
generator under `--check` on every sweep.

## Literals ledger

| Class | Count | Verifier-only | Example |
|---|---|---|---|
| `account` | 3 | 0 | `member@example.com` |
| `article` | 3 | 0 | `springs-over-easing` |
| `article_title` | 3 | 0 | `Springs over easing curves` |
| `author_handle` | 1 | 0 | `alex` |
| `band` | 2 | 0 | `list` |
| `billing_key` | 3 | 0 | `orbit-amelia` |
| `category` | 9 | 0 | `hero-sections` |
| `category_name` | 9 | 0 | `Hero sections` |
| `changelog_entry` | 4 | 0 | `spring-presets` |
| `changelog_kind` | 3 | 0 | `feature` |
| `changelog_title` | 4 | 0 | `Five named spring presets` |
| `copy` | 50 | 0 | `First impressions with editorial reveals an...` |
| `country` | 1 | 0 | `US` |
| `credential` | 1 | 0 | `deku-demo-pw-2026` |
| `currency` | 1 | 0 | `USD` |
| `design_phrase` | 10 | 0 | `grid of cards` |
| `doc_page` | 7 | 0 | `installation` |
| `doc_title` | 5 | 0 | `Installation` |
| `endpoint` | 16 | 0 | `/api/health` |
| `env_var` | 15 | 5 | `DATABASE_URL` |
| `example` | 7 | 0 | `scroll-velocity` |
| `example_title` | 7 | 0 | `Scroll velocity` |
| `handle` | 3 | 0 | `nova` |
| `header` | 1 | 0 | `X-Client-Region` |
| `licence` | 2 | 0 | `tempo-plus-nova` |
| `money` | 3 | 0 | `$249.00` |
| `motion_moment` | 5 | 0 | `leaves upward as the incoming word arrives` |
| `number` | 25 | 0 | `4173` |
| `region` | 1 | 0 | `IN` |
| `route` | 14 | 0 | `/docs` |
| `runtime` | 3 | 0 | `react` |
| `scheme` | 1 | 0 | `tempo-plus-` |
| `section` | 6 | 0 | `editorial-stagger-hero` |
| `section_title` | 6 | 0 | `Editorial stagger hero` |
| `seed_record` | 24 | 0 | `Nova Reyes` |
| `status` | 6 | 0 | `personal-perpetual` |
| `theme_key` | 12 | 0 | `transitions.snap` |
| `theme_value` | 14 | 0 | `1218` |
| `version` | 4 | 0 | `13.1.0` |

294 entries, 5 verifier-only. Carriers are resolved against the bytes
on disk, so a claimed carrier always contains the value contiguously.

## Authoring spec folder

At `Output/16sept-motion/_spec/S_saasm_crud_animation-library-catalogue-vb_20260916_090008/`, excluded from the bundle (CON-5): the seven
documents `00-decisions.md` to `06-implementation-plan.md`.

## Grading window

```
VERDICT  PASS   (/Users/apple/Desktop/deku/Output/16sept-motion/S_saasm_crud_animation-library-catalogue-vb_20260916_090008/instruction.md)
section        H2                chars  reference  flag
core_features  Core features     22175       2400  past-slice
user_flow      User flow          6161       1900  past-slice
ui_ux_notes    UI/UX notes        7090       1700  past-slice
constraints    Constraints        1994        800  over-reference
user_roles     User roles         1794       1000  over-reference
overview       Overview           2048        700  over-reference
joined total                     41262       8800  past-slice
first four                       37420       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```

## Kit gate log

Rendered from `_handoff/S_saasm_crud_animation-library-catalogue-vb_20260916_090008.gates.jsonl`. Not transcribed.

| Gate | Tool | Exit | Verdict | Inputs hashed |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | 25 |
| G1/G12 | `layout_lint.py` | 0 | PASS | 25 |
| G46 | `structure_lint.py` | 0 | PASS | 25 |
| G50 | `docker_lint.py` | 0 | PASS | 25 |
| G55 | `runtime_deps_lint.py` | 0 | PASS | 25 |
| G63 | `secret_lint.py` | 0 | PASS | 25 |
| G48 | `truth_lint.py` | 0 | PASS | 25 |
| G51 | `source_lint.py` | 0 | PASS | 25 |
| G52 | `rubric_context_lint.py` | 0 | PASS | 25 |
| G54 | `comment_lint.py` | 0 | PASS | 25 |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | 25 |
| G11 | `leak_scan.py` | 0 | PASS | 25 |
| G33 | `window_lint.py` | 0 | PASS | 25 |
| G4/G5 | `contract_lint.py` | 0 | PASS | 25 |
| G43 | `prescription_lint.py` | 0 | PASS | 25 |
| G44 | `disclosure_lint.py` | 0 | PASS | 25 |
| G10 | `no_sdk_lint.py` | 0 | PASS | 25 |
| G31 | `determinism_lint.py` | 0 | PASS | 25 |
| G14 | `reward_path_lint.py` | 0 | PASS | 25 |
| G27/G30 | `rubric_lint.py` | 0 | PASS | 25 |
| G41 | `flag_lint.py` | 0 | PASS | 25 |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | 25 |
| G59/G60 | `codequality_lint.py` | 2 | ? | 25 |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | 25 |
| G6 | `fixture_lint.py` | 0 | PASS | 25 |
| G24 | `coverage_map.py` | 0 | PASS | 25 |
| G37 | `checklist_qc.py` | 0 | PASS | 25 |
| G39 | `rubric_align_lint.py` | 0 | PASS | 25 |
| G28/G29 | `channel_lint.py` | 0 | PASS | 25 |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | 25 |
| G0/INV5 | `vendor_check.py` | 0 | PASS | 25 |
| G47 | `output_qc.py` | 0 | PASS | 25 |

`G59/G60` exits 2, NOT-APPLICABLE: no `evaluation_target: "source"` criterion. `G40`
exits 0 with a WARN because the receipts are self-attested on a single-agent run.

## Certification receipts

| Gate | Prompt | Verdict | PASS | WARN | N/A | FAIL |
|---|---|---|---|---|---|---|
| G3 | `task_code_verifier.md` | VALID | 12 | 0 | 0 | 0 |
| G34 | `QC_spec.md` | PASS | 13 | 2 | 0 | 0 |
| G34 | `QC_instruction.md` | PASS | 21 | 3 | 0 | 0 |
| G35 | `qc_docker.md` | PASS | 84 | 4 | 17 | 0 |
| G36 | `qc_toml.md` | PASS | 109 | 3 | 8 | 0 |
| G37 | `qc_solution_checklist.md` | PASS | 0 | 0 | 0 | 0 |
| G53 | `qc_rubric.md` | PASS | 14 | 1 | 1 | 0 |

The review raised real grader defects, fixed before the final sweep. Three of them would
have scored a correct app at zero or corrupted later runs:

1. **T11** listed Kill Bill's upstream password `password` among values that must never
   appear in a browser download. Every login form carries that word.
2. **T01 and T14** read `/proc/net/tcp` for port 4173. Under `separate` mode that is the
   verifier container's own network namespace, so the port is never listening there.
3. **T48** posted a purchase as `member2@example.com` to probe validation the brief never
   pins; a lenient app would have written `tempo-plus-kit` permanently and broken the
   no-licence assertions in T50/T51 for every later run.

A further sixteen graders asserted something the brief does not pin (a header name, a
status-code equality, invented endpoints, a response nesting). Each was relaxed to what the
brief states, or the brief was tightened where the behaviour is genuinely needed: the
`title` ordering ignores case, an empty `entitlements` is what "cannot be resolved" means,
and a signed-out save goes to `/login?next=<the page>&save=<slug>`.

## Companion carry

| Measure | Value |
|---|---|
| source | `/Users/apple/Desktop/deku/Drive_PRDs/16_sept/motion_prd.md`, 4,676 lines |
| colours described | 14 of 14, by family and tone; zero hexes in the brief |
| topics carried | 301 of 301 |
| enumerated items carried | 924 of 924 |
| waivers | 158 tokens, recorded in `_handoff/S_saasm_crud_animation-library-catalogue-vb_20260916_090008.sources.json` |

The waivers fall into the companion's own apparatus, design VALUES the A5 number rule
keeps out of the brief, class-name fingerprints, and the services the Task Order does not
scope. The one behavioural departure is `registrable`.

## Blocking findings

None block this bundle's exit state. Five kit defects were met and are reported:

1. **No referenceable Kill Bill call creates an invoice.** reference/K K.4 requires a
   payments brief to assert "an invoice exists for the right amount" and requires a named
   plan to come from `availableBasePlans`. The deployment's `killbill-init.sh` and
   `fleet/killbill/seed.sh` create a tenant and three accounts and nothing else, so the
   catalog is empty, no subscription can exist, and `invoices/pagination` can only ever be
   empty. `fleet/tools/verify_data.py` tells the operator to fix that by running a seed
   script that does not do it. This bundle asserts the billing account and the key
   conflict (both referenceable) and pins the amount on the order and in the receipt.
2. **`secret_hygiene_lint.py` (G17) contradicts its own docstring.** It says payments
   credentials are not flagged, but `ADMIN_PAT = _ADMIN_` flags `PAYMENTS_ADMIN_USER` and
   `PAYMENTS_ADMIN_PASSWORD`, which reference/C lists as agent-visible. The agent here
   receives them as `PAYMENTS_BASIC_USER` / `PAYMENTS_BASIC_PASSWORD` whose values are
   indirections to the canonical names; the verifier keeps the canonical names. One-line
   fix: exempt the `PAYMENTS_` and `STORAGE_` prefixes.
3. **`QC_instruction.md` A1/B3 vs `generate_instruction.md` 2.1** on `## Build plan`,
   resolved in favour of 2.1.
4. **`qc_docker.md` CMP-011 vs CMP-022** on `ports:`. Sidecars publish nothing here
   (the mailpit fragment's host ports were dropped); `main` publishes `4173:4173`.
5. **The killbill-init seed's bootstrap addresses end in the reserved `.example` label**,
   which G55 RD-6 fails; carried as `.example.com`. The fragment needs the same edit.

## Corpus-level gates

| Gate | Verdict | Why |
|---|---|---|
| G42 `corpus_overlap` | NOT-APPLICABLE | one bundle in this output root |
| G49 `diversity_lint` | NOT-APPLICABLE | same; the `draw:` lines are recorded for the corpus run |
| G61 `corpus_report` | ADVISORY | no bundle carries a difficulty yet |
| G38 `kit_selftest` | see the S10 run | once per kit revision |

## Budget

`turns_expected = 200`, `tokens_expected = 8000000`, the Standard tier at the BENCH-004
ceiling: ten graded features over three backing services, a server-rendered catalogue, a
sandboxed preview, an integration with a billing platform and a mail transport.

## Exit

**MECHANICALLY-GREEN, NO-SOLUTION.** Not admissible until the reference app lands
downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
