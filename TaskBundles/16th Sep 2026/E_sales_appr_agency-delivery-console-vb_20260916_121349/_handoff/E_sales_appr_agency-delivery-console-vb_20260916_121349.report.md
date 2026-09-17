# Build report - deku/agency-delivery-console-vb

Task code: `E_sales_appr_agency-delivery-console-vb_20260916_121349`

Gates run: 32 | ok: 32 | red: 0

**ALL GATES GREEN.** Exit state MECHANICALLY-GREEN, NO-SOLUTION. NOT ADMISSIBLE until a reference app exists and `harbor run -a oracle` returns 1.0 twice.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | validate_task.py | 0 | PASS |
| G1/G12 | layout_lint.py | 0 | PASS |
| G46 | structure_lint.py | 0 | PASS |
| G50 | docker_lint.py | 0 | PASS |
| G55 | runtime_deps_lint.py | 0 | PASS |
| G63 | secret_lint.py | 0 | PASS |
| G48 | truth_lint.py | 0 | PASS |
| G51 | source_lint.py | 0 | PASS |
| G52 | rubric_context_lint.py | 0 | PASS |
| G54 | comment_lint.py | 0 | PASS |
| G17 | secret_hygiene_lint.py | 0 | PASS |
| G11 | leak_scan.py | 0 | PASS |
| G33 | window_lint.py | 0 | PASS |
| G4/G5 | contract_lint.py | 0 | PASS |
| G43 | prescription_lint.py | 0 | PASS |
| G44 | disclosure_lint.py | 0 | PASS |
| G10 | no_sdk_lint.py | 0 | PASS |
| G31 | determinism_lint.py | 0 | PASS |
| G14 | reward_path_lint.py | 0 | PASS |
| G27/G30 | rubric_lint.py | 0 | PASS |
| G41 | flag_lint.py | 0 | PASS |
| G56/G57/G58 | if_lint.py | 0 | PASS |
| G59/G60 | codequality_lint.py | 2 | ? |
| G7/G8/G9/G32/G45 | workflow_lint.py | 0 | PASS |
| G6 | fixture_lint.py | 0 | PASS |
| G24 | coverage_map.py | 0 | PASS |
| G37 | checklist_qc.py | 0 | PASS |
| G39 | rubric_align_lint.py | 0 | PASS |
| G28/G29 | channel_lint.py | 0 | PASS |
| G40 | prompt_receipt_lint.py | 0 | WARN |
| G0/INV5 | vendor_check.py | 0 | PASS |
| G47 | output_qc.py | 0 | PASS |

G59/G60 is the advisory code-quality channel and returns NOT-APPLICABLE because the bundle carries no source criteria. G40 notes that every certification receipt is SELF-ATTESTED (owner equals verifier). Prose verdicts recorded in the receipts: G34 CHANGES REQUIRED (QC_instruction.md), G34 PASS (QC_spec.md), G35 PASS (qc_docker.md), G53 PASS (qc_rubric.md), G37 CHANGES REQUIRED (qc_solution_checklist.md), G36 PASS (qc_toml.md), G3 VALID (task_code_verifier.md). See the receipt findings for each non-PASS verdict.

## Cell and configuration

| Field | Value |
|---|---|
| cell | enterprise / sales-crm / approval-workflow |
| service_profile | P6-db-auth-email |
| providers | backend postgres, auth keycloak, email mailpit |
| variant | b, axes critical_depth, spec_sections |
| language | typescript (drawn: ssr-islands, Express, SolidStart) |
| capability_flags | aesthetic |
| design_direction | companion |
| launch_surface | favicon, form_validation, no_frontend_secrets, privacy_page, sitemap_robots |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| grader / schema | 0.22.0 / 1.4 |
| turns / tokens | 200 / 8000000, the expert band: three services, sixteen roles, a companion carried in full |

## Graders

Workflows 20 | browser substeps 34 | pytest substeps 80 | critical substeps 32 | largest workflow 9 substeps, so one failed substep fails any workflow. One module, `tests/test_output.py`, 80 tests. Rubric 22 criteria, all positive, advisory and off the reward path. Checklist 418 items; every item is cited by pytest, a browser substep or a rubric criterion (G24, G28, G39).

## Rubric point shares

| Dimension | Points | Share | Target |
|---|---|---|---|
| instruction_following | 12 | 0.214 | 0.30 |
| functionality | 12 | 0.214 | 0.25 |
| ux_flow | 8 | 0.143 | 0.15 |
| ui_visual | 10 | 0.179 | 0.15 |
| motion | 5 | 0.089 | 0.05 |
| accessibility | 5 | 0.089 | 0.05 |
| responsiveness | 4 | 0.071 | 0.05 |

## Slot obligations

| Slot | Provider | Critical substep | Status |
|---|---|---|---|
| backend | postgres | test_concurrent_issues_take_contiguous_numbers_stored_once, test_concurrent_change_order_approvals_value_stored_sum, test_app_credential_cannot_update_or_delete_log_row and more | MET |
| auth | keycloak | test_project_manager_issue_denied_invoice_row_untouched, test_expired_grant_denied_on_next_request, test_reveal_needs_step_up_then_single_use_access and more | MET |
| email | mailpit | test_stage_assignees_notified_by_email_only_current_stage, test_confirmation_email_from_routed_entity | MET |

## Carriage of the companion PRD (G51)

- note  digital-cover_prd.md: 12/12 source colour(s) described in the brief by family and tone
- note  digital-cover_prd.md: 168/168 topic(s) carried into the brief
- note  digital-cover_prd.md: 778/778 enumerated item(s) carried into the brief
- VERDICT  PASS   G51: every supplied source document is carried into instruction.md (instruction.md)

No `--waive` was used.

## Grading window (G33)

core_features 2240, user_flow 1571, ui_ux_notes 1652, constraints 967, user_roles 1641, overview 792; joined 8863 of 9000.

## Runtime checks performed during authoring

The environment image was built from `environment/Dockerfile` and runs node v20.20.2, npm 10.8.2 and Python 3.12.3 with pg_isready and both reserved directories. PostgreSQL, Keycloak and Mailpit were booted from the pinned images in a scratch compose with ports published; the realm `parallax` imported and client `parallax-app` issued a password-grant token for owner@aeroline.example.com. Every image digest resolved with docker buildx imagetools inspect to a multi-platform index. A scratch reference server of the pinned contract, backed by that PostgreSQL and Mailpit, ran the pytest module; its record follows. No test ran against a built Parallax, because none exists.

# task_10 trap proof (scratch mock, 2026-09-16)

Correct reference, final run after every QC fix: 80 passed in 283.02s (full suite, run.sh with MOCK_BUG empty).

Each wrong-default switch against its trap test(s):

| Switch | Tests | Result :: first assertion |
|---|---|---|
| seq_race | test_concurrent_issues_take_contiguous_numbers_stored_once | 1 failed, 77 deselected in 0.30s :: E       AssertionError: concurrent issues shared a number: ['PXF-2026-00003', 'PXF-2026-00003', 'PXF-2026-00003', 'PXF-2026-00003', 'PXF-2026-00003', 'PXF-2026-00003'] |
| seq_consume_on_refusal | test_refused_issue_consumes_no_number | 1 failed, 77 deselected in 0.10s :: E       AssertionError: a refused issue consumed a number: issued 3, then 5 after the refusal |
| global_sequence | test_entity_sequences_independent_numbers | 1 failed, 77 deselected in 0.11s :: E       AssertionError: a Malta issue advanced the France sequence: 4 then 6 |
| per_line_rounding | test_issued_invoice_totals_from_lines_rounded_once | 1 failed, 77 deselected in 0.09s :: E       AssertionError: tax must be computed once on the subtotal: {'id': 'inv_6de288a9f8c303d8', 'doc_type': 'invoice', 'status': 'issued', 'number': 'PXF-2026-00003', ' |
| vat_any_number | test_invalid_vat_reverse_charge_issue_refused_draft_row_untouched | 1 failed, 77 deselected in 0.09s :: E       AssertionError: POST /api/invoices/inv_7c8f8c57fdbdf9c2/issue answered 200 code None, expected 422 'vat_number_invalid': {"id": "inv_7c8f8c57fdbdf9c2", "doc_type" |
| vies_ignore_age | test_stale_vies_validation_issue_refused | 1 failed, 77 deselected in 0.09s :: E       AssertionError: POST /api/invoices/inv_5e6129399b037948/issue answered 200 code None, expected 422 'vat_validation_stale': {"id": "inv_5e6129399b037948", "doc_typ |
| po_ignored | test_public_sector_without_po_issue_refused_no_number_stored | 1 failed, 77 deselected in 0.09s :: E       AssertionError: POST /api/invoices/inv_564f09c2424ee94c/issue answered 200 code None, expected 422 'po_required': {"id": "inv_564f09c2424ee94c", "doc_type": "invo |
| credit_shares_sequence | test_credit_note_own_sequence_voids_original_keeps_number | 1 failed, 77 deselected in 0.09s :: E       AssertionError: number 'PXF-2026-00004' is not PXFC-<year>-<five digits> |
| role_check_missing | test_project_manager_issue_denied_invoice_row_untouched | 1 failed, 77 deselected in 0.09s :: E       AssertionError: a project manager issued an invoice: 200 {"id": "inv_e54f28562ccabbeb", "doc_type": "invoice", "status": "issued", "number": "PXF-2026-00003", "ag |
| login_is_step_up | test_login_alone_is_not_step_up_issue_forbidden | 1 failed, 77 deselected in 0.08s :: E       AssertionError: POST /api/invoices/inv_f0de056d306f50da/issue answered 200 code None, expected 403 'step_up_required': {"id": "inv_f0de056d306f50da", "doc_type":  |
| entity_scope_missing | test_other_entity_finance_admin_issue_forbidden | 1 failed, 77 deselected in 0.09s :: E       AssertionError: a Malta finance admin issued a France invoice: 200 {"id": "inv_c9ca32658b274a94", "doc_type": "invoice", "status": "issued", "number": "PXF-2026-0 |
| sod_missing | test_uploader_decision_denied_separation_of_duties_row_unchanged | 1 failed, 77 deselected in 10.19s :: E       AssertionError: POST /api/approvals/apr_c4d22ccb6b35d014/decisions answered 200 code None, expected 403 'separation_of_duties': {"id": "apr_c4d22ccb6b35d014", "st |
| supersede_not_pending | test_decision_on_superseded_version_refused_current_version | 1 failed, 77 deselected in 10.20s :: E       AssertionError: POST /api/approvals/apr_a48fcb3d79ce45a5/decisions answered 409 code 'approval_not_pending', expected 409 'approval_superseded': {"type": "about:b |
| all_of_count | test_all_of_stage_waits_for_every_assignee_counted_once | 1 failed, 77 deselected in 20.26s :: E       AssertionError: a repeated decision completed the stage: {'id': 'apr_4491b1c2d9f42fc2', 'state': 'approved', 'current_stage': 2, 'value_minor': 3200000, 'version_ |
| approval_race | test_concurrent_all_of_final_decisions_one_draft_invoice_row | 1 failed, 77 deselected in 20.55s :: E       AssertionError: assert 'pending' == 'approved' |
| notify_all_stages | test_stage_assignees_notified_by_email_only_current_stage | 1 failed, 77 deselected in 20.25s :: E           AssertionError: owner@aeroline.example.com was emailed for stage 1 |
| threshold_missing | test_approver_below_value_threshold_denied_unchanged | 1 failed, 77 deselected in 20.29s :: E       AssertionError: POST /api/approvals/apr_fb52dfe1e6cbd82b/decisions answered 200 code None, expected 403 'approval_threshold_exceeded': {"id": "apr_fb52dfe1e6cbd82 |
| tenant_403 | test_other_tenant_project_denied_as_not_found | 1 failed, 77 deselected in 0.09s :: E       AssertionError: GET /api/projects/prj_dc58af42cf5d91e0 answered 403 code 'forbidden', expected 404 'not_found': {"type": "about:blank", "title": "forbidden", "sta |
| margin_null | test_project_manager_proposal_margin_absent_denied,test_client_owner_sees_sent_proposal_without_cost | 2 failed, 76 deselected in 0.12s :: E       AssertionError: margin reached a project manager without visibility: {'id': 'prp_be9a79cc72ad85d0', 'version': 2, 'status': 'sent', 'subtotal_minor': 3250000, 'di |
| reveal_reuse | test_reveal_needs_step_up_then_single_use_access | 1 failed, 77 deselected in 0.20s :: E       AssertionError: POST /api/vault/secrets/sec_c5fba2b384eb6341/reveal answered 200 code None, expected 409 'request_already_used': {"value": "vlt-verdane-cms-4471-Q |
| self_approve | test_requester_self_approval_forbidden | 1 failed, 77 deselected in 0.11s :: E       AssertionError: POST /api/vault/access-requests/var_b41b14d1cbcd1795/approve answered 200 code None, expected 403 'self_approval_forbidden': {"id": "var_b41b14d1c |
| break_glass_single | test_break_glass_needs_two_different_approvers_access,test_break_glass_awaiting_second_reveal_refused | 2 failed, 76 deselected in 0.22s :: E       AssertionError: {'id': 'var_e49a13c43fcbeefb', 'state': 'approved', 'break_glass': True, 'requested_ttl_minutes': 30, ...} |
| log_mutable | test_app_credential_cannot_update_or_delete_log_row | 1 failed, 77 deselected in 0.23s :: E       AssertionError: the application's own database credential rewrote a vault access log row |
| verify_links_only | test_tampered_log_entry_verify_reports_broken_at | 1 failed, 77 deselected in 0.23s :: E               AssertionError: rewriting entry 1 went undetected: {'valid': True, 'broken_at': None} |
| plaintext_store | test_database_holds_no_plaintext_secret_stored | 1 failed, 77 deselected in 0.19s :: E       AssertionError: a vault secret is stored in plaintext: ['"public"."vault_secrets" holds vlt-verdane-dns-3318-LM', '"public"."vault_secrets" holds vlt-aeroline-cms |
| grant_ignores_expiry | test_expired_grant_denied_on_next_request | 1 failed, 77 deselected in 12.34s :: E       AssertionError: GET /api/projects/prj_61b5d19842f770d2 answered 200 code 'INST-2026-01', expected 404 'not_found': {"id": "prj_61b5d19842f770d2", "code": "INST-20 |
| grant_cache | test_expired_grant_denied_on_next_request,test_revoked_grant_denied_immediately | 2 failed, 76 deselected in 0.18s :: E       AssertionError: GET /api/projects/prj_54deea9934382213 answered 404, expected (200,): {"type": "about:blank", "title": "not_found", "status": 404, "detail": "Not  |
| co_lost_update | test_concurrent_change_order_approvals_value_stored_sum | 1 failed, 77 deselected in 0.38s :: E       AssertionError: simultaneous approvals lost a delta: 3000000 + 110000 became 3010000 |
| lead_replay_race | test_concurrent_replayed_lead_one_row_one_confirmation_email | 1 failed, 77 deselected in 5.28s :: E       AssertionError: replays answered different leads: {'PXL-ED46ECCE', 'PXL-25D7D609', 'PXL-8A1D6046'} |
| entity_by_site | test_confirmation_email_from_routed_entity | 1 failed, 77 deselected in 5.15s :: E       AssertionError: a French company on the English site routed to [{'reference': 'PXL-ADFD4731', 'email': 'routed-fr-1900316c@example.com', 'status': 'new', 'budget' |
| gclid_always | test_gclid_not_stored_without_marketing_consent_row | 1 failed, 77 deselected in 5.16s :: E       AssertionError: a gclid was kept without marketing consent: [{'reference': 'PXL-66306F78', 'email': 'noconsent-ca311749@example.com', 'status': 'new', 'budget': ' |
| slug_404 | test_slug_change_old_path_permanent_redirect_stored_alias | 1 failed, 77 deselected in 0.08s :: E       AssertionError: the old address answered 404 None |
| hreflang_hardcoded | test_hreflang_alternates_derived_from_siblings | 1 failed, 77 deselected in 0.06s :: E       AssertionError: a single-language case study claims a French sibling: ['http://127.0.0.1:47173/work/verdane/', 'http://127.0.0.1:47173/fr/references/verdane/', 'h |
| sitemap_all | test_below_threshold_landing_noindex_excluded_from_sitemap | 1 failed, 77 deselected in 0.09s :: E       AssertionError: noindex pages in the sitemap |
| secret_in_bundle | test_served_assets_hold_no_secret_access_values | 1 failed, 77 deselected in 0.10s :: E       AssertionError: a served document exposes a secret: ['/assets/app.js carries parallax-client-secret-2026'] |
| no_skip_link | test_home_page_skip_links_first_images_carry_alt | 1 failed :: E AssertionError: the first focusable element is '<a href="#after-gallery">Skip visual gallery - view all projects as a list', expected a skip to content link |
| img_no_alt | test_home_page_skip_links_first_images_carry_alt | 1 failed :: E AssertionError: images without alt text: ['<img src="/media/verdane.jpg">'] |
| role_rows_open | test_role_table_never_cells_denied_at_api | 1 failed :: E AssertionError: a finance admin opened the vault: 200 [{"id": ..., "label": "Production CMS admin", ...}] |

## Handoff gates

G13, G15, G18, G19, G20, G21 and G25 are undecided; commands and expected verdicts are in the handoff file.

Rendered from the receipts. No verdict here is hand-written.
