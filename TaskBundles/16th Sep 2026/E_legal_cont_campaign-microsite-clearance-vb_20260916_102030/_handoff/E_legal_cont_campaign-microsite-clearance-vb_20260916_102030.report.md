# Build report - E_legal_cont_campaign-microsite-clearance-vb_20260916_102030

## Identity

| Field | Value |
|---|---|
| task code | `E_legal_cont_campaign-microsite-clearance-vb_20260916_102030` |
| task id | `deku/campaign-microsite-clearance-vb` |
| cell | enterprise / legal-compliance / content-publishing |
| service_profile | `P4-db-storage` |
| providers | `backend = postgres`, `storage = minio` |
| variant | `b` on `critical_depth` and `spec_sections` (companion PRD supplied) |
| language | `python` |
| design_direction | `companion` (the draw for this archetype, `dense-ops-console`, is recorded and does not govern) |
| launch_surface | `form_validation,meta_tags,mobile_viewport,privacy_page,single_cta` |
| kit revision | `806eb0a` |
| vendored grader | `0.22.0` |
| verifier mode | `separate` |
| pytest module | `tests/test_output.py` |
| authors | `utsav.jain@ethara.ai` (QL), `mohd.rafey@ethara.ai` (contributor) |
| exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

The Task Order's `domain: retail and ecommerce` and `pattern: content publishing and approval
platform` are not kit enum members. They were mapped, not silently re-keyed: the domain to
`legal-compliance` (the enterprise domain naming the archetype's defining property, per-market legal
clearance; `ecommerce-retail` exists only under solo_founder) and the pattern to `content-publishing`.
Both are recorded in `_spec/E_legal_cont_campaign-microsite-clearance-vb_20260916_102030/00-decisions.md`.

Derived-design draws from `sha256("campaign-microsite-clearance")`: `render_model = mpa-progressive`,
`backend = Django + templates`, `frontend = HTMX + server templates`, `nav = top-nav`,
`work_surface = split detail-pane`, `create_flow = inline-row`, `feedback = toast`.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| The public drop page | INCLUDED | ## Core features 1 | the Task Order's 'scroll one long narrative page'; companion 5, 7, 10, 11 |
| Locales, the switcher and discovery | INCLUDED | ## Core features 2 | seven locales as data; companion 3.2, 5.2, 21.4 |
| Product cards and the storefront hand-off | INCLUDED | ## Core features 3 | the Task Order's 'link built from a per-market template'; companion 3.3, 8, 20.1 |
| Products, prices and attribution slots | INCLUDED | ## Core features 4 | companion 13.2, 14.4, 20.2, 26.5; the currency invariant |
| Grants and refusals | INCLUDED | ## Core features 5 | the Task Order's 'expiring grants'; companion 2.2 R1, R3, R4, R6, R7 |
| Translations | INCLUDED | ## Core features 6 | the Task Order's 'translate'; companion 21.2, 21.3 |
| Per-market review, approval, publication | INCLUDED | ## Core features 7 | the Task Order's 'legally clear each market's page separately'; companion 13.4, 16, 27 rollback |
| Images and artifacts in the object store | INCLUDED | ## Core features 8 | the storage slot and the content-publishing critical focus; companion 16.2, 24.2 |
| The audit log | INCLUDED | ## Core features 9 | the Task Order's 'immutable audit log'; companion 17 |
| The site's own pages | INCLUDED | ## Core features 10 | the five drawn launch-surface obligations; companion 26.1, 9.2 |
| Staff accounts | INCLUDED | ## Core features ### Auth | kit baseline email and password; signup closed for enterprise |
| Federated identity, SCIM, MFA, break-glass | DROPPED | ## Constraints bullet 3 | companion 15, 26.4; no identity provider in the environment |
| Change freeze, platform administrator | DROPPED | ## Constraints bullet 4 | companion 16.3; folded into the owner |
| Notifications and webhooks | DROPPED | ## Constraints bullet 5 | companion 18, 19; no mail slot |
| Link integrity, catalogue reconciliation, vendor exchange | DROPPED | ## Constraints bullet 6 | companion 18, 20.3; each needs a call to another host |
| Hero film, family track, per-market colourways, reduced prices | DROPPED | ## Constraints bullet 7 | companion 7.7, 7.12, 13.2, 26.5; recorded in 00-decisions |
| Measurement layer, consent platform, newsletter | DROPPED | ## Constraints bullet 8 | companion 20.4, 26.2, 30 E-12 |
| Observability stack, CDN purge, environments | DROPPED | ## Constraints bullet 10 | companion 22, 23, 28 |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | postgres | MET | `test_a_price_in_another_currency_is_refused_and_nothing_changes`, `test_approvals_bind_to_the_content_hash_and_an_edit_supersedes_them` and `test_every_write_and_every_refusal_records_one_audit_event` (all critical) read stored rows through the shared adapter; `test_the_database_refuses_to_rewrite_audit_rows_for_the_app_role` (critical) connects with the application's own role |
| `storage` | minio | MET | `test_an_upload_is_stored_at_its_digest_key_in_the_object_store` (critical) reads the object back from the bucket; `test_an_image_of_a_market_that_is_not_live_is_not_public` (critical) carries the content-publishing critical focus; `test_the_bucket_refuses_an_anonymous_read` and `test_each_publish_stores_a_versioned_artifact_in_the_object_store` complete it |

## Grading surface

| Measure | Value |
|---|---|
| workflows | 17 (enterprise band 13-23) |
| browser substeps | 38 |
| pytest substeps | 92 |
| browser:pytest ratio | 0.41 (G45 band 0.40-2.00) |
| critical substeps | 10 |
| judged criteria | 14 positive, 0 negative |
| checklist items | 604 |

Category mix: `business_rule` 21, `core_outcome` 2, `data_integrity` 19, `presentation` 20, `security` 24, `validation` 6.

| Workflow id | Browser | Pytest | Critical |
|---|---|---|---|
| `campaign_index_and_public_discovery` | 2 | 7 | 0 |
| `visitor_arrives_in_their_own_language` | 5 | 4 | 0 |
| `the_drop_page_reads_without_motion_or_script` | 2 | 6 | 0 |
| `the_language_choice_keeps_the_document` | 2 | 4 | 0 |
| `the_storefront_link_carries_colourway_and_attribution` | 2 | 5 | 1 |
| `absent_or_unpriced_products_never_mislead` | 1 | 4 | 0 |
| `staff_sign_in_and_studio_entry` | 2 | 4 | 1 |
| `one_market_is_cleared_and_published` | 6 | 4 | 1 |
| `an_edit_withdraws_approval` | 1 | 5 | 1 |
| `grants_bound_every_write` | 3 | 6 | 1 |
| `the_owner_lets_the_agency_in` | 4 | 4 | 0 |
| `product_fields_belong_to_the_merchandiser` | 2 | 9 | 1 |
| `translations_carry_the_market_language` | 1 | 7 | 0 |
| `publication_is_guarded_repeatable_and_reversible` | 1 | 5 | 0 |
| `draft_media_stays_private` | 1 | 5 | 2 |
| `the_audit_log_cannot_be_rewritten` | 3 | 6 | 2 |
| `the_site_holds_on_a_phone_and_leaks_nothing` | 0 | 7 | 0 |

## Checklist

| Section | Items |
|---|---|
| `C-CF` | 307 |
| `C-CN` | 5 |
| `C-DC` | 27 |
| `C-DM` | 55 |
| `C-FE` | 32 |
| `C-OV` | 24 |
| `C-RL` | 32 |
| `C-TR` | 26 |
| `C-UF` | 55 |
| `C-UX` | 41 |

Tag mix: `capability` 22, `constraint` 260, `contract` 68, `data` 25, `literal` 155, `role` 20, `ui` 54. Every item names one grader and shares
at least two stemmed words with it (G24).

## Judged rubric

| Dimension | Points | Share | Target | Inside 0.10 band |
|---|---|---|---|---|
| `instruction_following` | 11 | 0.250 | 0.30 | yes |
| `functionality` | 11 | 0.250 | 0.25 | yes |
| `ux_flow` | 6 | 0.136 | 0.15 | yes |
| `ui_visual` | 8 | 0.182 | 0.15 | yes |
| `motion` | 4 | 0.091 | 0.05 | yes |
| `accessibility` | 1 | 0.023 | 0.05 | yes |
| `responsiveness` | 3 | 0.068 | 0.05 | yes |

Positive total 44. `task completion` share 9/14. Every criterion was re-faceted in
certification cycle 2 onto an observation no browser substep and no pytest assertion makes.

## Literals ledger

| Class | Count | Verifier-only | Example |
|---|---|---|---|
| `account` | 8 | 0 | `owner@example.com` |
| `credential` | 1 | 0 | `deku-demo-pw-2026` |
| `design_phrase` | 1 | 0 | `Memphis-revival` |
| `endpoint` | 12 | 0 | `/api/health` |
| `env_var` | 1 | 1 | `DB_ADMIN_URL` |
| `motion_moment` | 4 | 0 | `portrait window` |
| `number` | 9 | 0 | `2000` |
| `route` | 16 | 0 | `/privacy/` |
| `scheme` | 21 | 0 | `hscamp` |
| `seed_record` | 97 | 0 | `Maren Holt` |
| `status` | 36 | 0 | `draft` |

206 entries, 1 verifier-only (`DB_ADMIN_URL`).

## Grading window

```
VERDICT  PASS   (/Users/apple/Desktop/deku/Output/16sept-yestalgia/E_legal_cont_campaign-microsite-clearance-vb_20260916_102030/instruction.md)
section        H2                chars  reference  flag
core_features  Core features     31495       2400  past-slice
user_flow      User flow          5554       1900  past-slice
ui_ux_notes    UI/UX notes        5447       1700  past-slice
constraints    Constraints        1455        800  over-reference
user_roles     User roles         2707       1000  past-slice
overview       Overview           1844        700  over-reference
joined total                     48502       8800  past-slice
first four                       43951       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```

## Kit gate log

Rendered from `_handoff/E_legal_cont_campaign-microsite-clearance-vb_20260916_102030.gates.jsonl`.

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

`G59/G60` exits 2, NOT-APPLICABLE: no `evaluation_target: "source"` criterion.

## Certification receipts

| Gate | Prompt | Verdict | PASS | WARN | N/A | FAIL |
|---|---|---|---|---|---|---|
| G3 | `task_code_verifier.md` | VALID | 12 | 0 | 0 | 0 |
| G34 | `QC_instruction.md` | PASS | 13 | 11 | 0 | 0 |
| G34 | `QC_spec.md` | PASS | 8 | 7 | 0 | 0 |
| G35 | `qc_docker.md` | PASS | 93 | 8 | 4 | 0 |
| G36 | `qc_toml.md` | PASS | 114 | 1 | 5 | 0 |
| G37 | `qc_solution_checklist.md` | PASS | 0 | 0 | 0 | 0 |
| G53 | `qc_rubric.md` | PASS | 8 | 7 | 1 | 0 |

Every receipt was produced by an independent reviewer subagent that did not author the bundle. Cycle 1
drew CHANGES REQUIRED or FAIL from QC_spec, QC_instruction, qc_solution_checklist and qc_rubric. The
reward-zero defects it found and cycle 2 fixed: the studio preview grader asserted `noindex` the brief never
pinned; the menu grader used `offsetParent`, which is always null for a fixed full-viewport overlay;
`product_order`, the sign-in button label, audit id ordering and the translations-list shape were
unpinned; the wordmark's accessible name contradicted the new-tab suffix rule; one audit grader depended on
events left by earlier tests. Seven judged criteria double-graded browser or pytest observations and one
contradicted the brief's teal hero triangle; all fourteen were re-faceted. The checklist lost duplicates and
unobservable items and gained role-refusal, seed-matrix, seeded-staff and narrow-studio coverage through three
new graders (T89-T91). Cycle 3 pinned the remaining either-way choices (the overlay menu inert or a native
modal dialog, a wrapping or `for` label, partial and empty `product_order`, studio forms that always submit),
gave the type-size grader a half-pixel tolerance, added T92 (fixed bar on scroll, one colour mode), and
wired audit action names, seed literals and toasts to graders that read them; QC_instruction and qc_rubric
passed. qc_solution_checklist still found four ungraded obligations after cycle 3 (the `product_order`
semantics, `product.update`, the privacy page's third-party and erasure clause, the narrow menu column and the
two shop-action copies). They were fixed in T64, T77 and T78, and with the author's approval a fourth checklist
review ran past the kit's 3-cycle fix-or-abort limit (00-RUN section 5). That exception is recorded here. The author's reviewer briefs for QC_instruction had
also listed a mistyped registry (A1-A5, B1-B6, C1-C7, D1-D6), so the cycle 1-3 scorecards answered the wrong ids;
the receipt builder refused them, and a fresh reviewer re-ran QC_instruction on the prompt's own registry over
the final bundle (PASS). Its one reward-risk note, the floating shop copy required outside the `header`, was
removed from T78.

## Companion carry

| Measure | Value |
|---|---|
| source | `/Users/apple/Desktop/deku/Drive_PRDs/16_sept/yestalgia_prd.md`, 1,656 lines |
| colours described | 14 of 14, by family and tone; zero hexes in the brief |
| topics carried | 108 of 108 |
| enumerated items carried | 511 of 511 |
| waivers | 81 tokens, recorded in `_handoff/E_legal_cont_campaign-microsite-clearance-vb_20260916_102030.sources.json` |

## Blocking findings

None block this bundle's exit state. Kit defects met and reported:

1. **`revalidate.py` forwards G51 waivers as `--waive <token>`**, so a token beginning with `--` (a CSS
   custom property such as `--spacing`) is parsed by `source_lint.py` as a flag; argparse exits 2 and the
   sweep reports G51 as "no companion document was supplied". Worked around with dash-free tokens.
   One-line fix: build `--waive=<token>` in `plan()`.
2. **`qc_docker.md` CMP-011 vs CMP-022** on `ports:` (resolved for the Critical check), and the postgres
   provider fragment gives `deku_admin` and `deku_app` the same password, so the admin/app split is nominal
   on every postgres task (qc_docker SEC-002 WARN).
3. **`QC_instruction.md` A1/B3 vs `generate_instruction.md` 2.1** on `## Build plan`; **C4** treats pinned
   type sizes as a defect while the generator's number rule requires them.
4. **`QC_spec.md` S2** reads 3-6 features where the generator allows 6-10 with a companion.
5. **reference/C minio image** no longer resolves on Docker Hub; pinned to quay.io at the same release.
6. **`toml_generator.md`** requires `[delivery]` and documents `rubric_version` in 10.5b, but its 11 template
   omits both and 13 says the file ends at `[[artifacts]]` (qc_toml note).
7. **Verifier `APP_PUBLIC_URL` under `environment_mode = "separate"`**: qc_toml VERIF-005 (High) requires the
   `http://localhost:4173` default, but in separate mode the verifier's localhost is its own container, so the
   harness must inject the app's reachable URL; QC_instruction D6 flags the same line as a WARN.

## Corpus-level gates

| Gate | Verdict | Why |
|---|---|---|
| G42 `corpus_overlap` | NOT-APPLICABLE | one bundle in this output root |
| G49 `diversity_lint` | NOT-APPLICABLE | same; `draw:` lines are recorded |
| G61 `corpus_report` | ADVISORY | corpus-level |

## Exit

**MECHANICALLY-GREEN, NO-SOLUTION.** Not admissible until the reference app lands downstream from
`solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
