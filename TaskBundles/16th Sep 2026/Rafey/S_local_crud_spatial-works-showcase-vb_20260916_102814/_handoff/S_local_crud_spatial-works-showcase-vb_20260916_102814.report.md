# Build report - S_local_crud_spatial-works-showcase-vb_20260916_102814

## Identity

| Field | Value |
|---|---|
| task code | `S_local_crud_spatial-works-showcase-vb_20260916_102814` |
| task id | `deku/spatial-works-showcase-vb` |
| cell | solo_founder / local-services / crud-catalog |
| service_profile | `P2-db-email` |
| providers | `backend = postgres`, `email = mailpit` |
| variant | `b` on `critical_depth` and `spec_sections` |
| language | `typescript` |
| design_direction | `companion` (draw `dense-ops-console` recorded, not governing) |
| launch_surface | `alt_text,cookie_choice,form_validation,mobile_viewport,no_broken_links` |
| kit revision | `806eb0a` |
| vendored grader | `0.22.0` |
| verifier mode | `separate` |
| exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

The Task Order's `domain: portfolio-agency` and `pattern: catalog-browse` are not kit enum
members; mapped to `local-services` and `crud-catalog` and recorded in `00-decisions.md`.

Draws from `sha256("spatial-works-showcase")`: `render_model = spa-json-api`,
`backend = NestJS`, `frontend = Lit + Vite`, `nav = top-nav`, `work_surface = table-first`,
`create_flow = dedicated-route`, `feedback = toast`.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| The spatial gallery | INCLUDED | ## Core features 1 | the Task Order's scroll driven 3D gallery with rings and spiral |
| The Works catalogue | INCLUDED | ## Core features 2 | the Task Order's filterable grid and list by discipline; carries the facet pattern |
| Project detail | INCLUDED | ## Core features 3 | named in the Task Order; companion Section 11 is an implied contract |
| The studio page | INCLUDED | ## Core features 4 | named in the Task Order |
| Contact and enquiry | INCLUDED | ## Core features 5 | the Task Order's terminal action; carries the email slot |
| The studio inbox | INCLUDED | ## Core features 6 | not in the companion; the smallest surface where the crud-catalog critical row is read back |
| Localisation | INCLUDED | ## Core features 7 | companion Sections 2.3 and 20 |
| Consent | INCLUDED | ## Core features 8 | companion Sections 5.6 and 20.4; the drawn cookie_choice obligation |
| The 404 television | INCLUDED | ## Core features 9 | companion Section 15 |
| The site's own surface | INCLUDED | ## Core features 10 | the drawn alt_text, mobile_viewport and no_broken_links obligations plus the privacy page |
| Headless CMS | DROPPED | 00-decisions | replaced by PostgreSQL seed rows; no second service |
| Ambient audio | DROPPED | ## Constraints | companion Section 8.6 marks it optional and off by default |
| Third-party analytics | DROPPED | ## Constraints | no external network at runtime; the consent choice is still recorded |
| Mailto fallback | DROPPED | 00-decisions | companion offers it only absent a form backend |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | postgres | MET | `test_an_accepted_enquiry_is_stored_exactly_as_submitted` and `test_a_status_change_is_stored_and_survives_a_reload` (critical) read the stored rows back through the shared adapter |
| `email` | mailpit | MET | `test_an_enquiry_notification_mail_reaches_the_studio_inbox_alone` (critical) reads exactly one notification to the studio address alone with the pinned subject |

## Grading surface

| Measure | Value |
|---|---|
| workflows | 14 |
| browser substeps | 20 |
| pytest substeps | 43 |
| browser:pytest ratio | 0.47 |
| critical substeps | 6 |
| judged criteria | 13 |
| checklist items | 247 |

Category mix: `business_rule` 10, `core_outcome` 2, `data_integrity` 6, `notification` 1, `presentation` 10, `security` 9, `validation` 5.

| Workflow id | Browser | Pytest | Critical |
|---|---|---|---|
| `spatial_gallery_is_served_from_one_origin` | 4 | 5 | 0 |
| `wrong_password_login_is_refused` | 1 | 4 | 2 |
| `catalogue_facets_narrow_with_computed_counts` | 3 | 4 | 0 |
| `invalid_discipline_or_slug_answers_not_found` | 0 | 2 | 0 |
| `project_page_steps_through_the_catalogue` | 2 | 2 | 0 |
| `languages_switch_content_and_chrome` | 1 | 3 | 0 |
| `studio_page_tells_the_story` | 1 | 1 | 0 |
| `enquiry_is_stored_and_mailed_to_the_studio` | 2 | 3 | 2 |
| `invalid_enquiry_is_refused_and_nothing_is_stored` | 0 | 2 | 0 |
| `visitor_is_denied_the_stored_enquiries` | 0 | 3 | 1 |
| `studio_status_change_survives_a_reload` | 2 | 4 | 1 |
| `consent_comes_before_any_cookie` | 1 | 2 | 0 |
| `site_edges_are_designed_not_defaulted` | 3 | 7 | 0 |
| `enquiry_limit_refuses_a_flood` | 0 | 1 | 0 |

## Checklist

| Section | Items |
|---|---|
| `C-CF` | 96 |
| `C-CN` | 6 |
| `C-DC` | 16 |
| `C-DM` | 19 |
| `C-FE` | 21 |
| `C-OV` | 10 |
| `C-RL` | 13 |
| `C-TR` | 17 |
| `C-UF` | 27 |
| `C-UX` | 22 |

Tag mix: `capability` 23, `constraint` 39, `contract` 34, `data` 11, `literal` 52, `role` 7, `ui` 81.

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

Positive total 47; `task completion` 9/13.

## Literals ledger

| Class | Count | Verifier-only | Example |
|---|---|---|---|
| `account` | 2 | 0 | `studio@example.com` |
| `address` | 1 | 0 | `hello@avx-studio.example.com` |
| `copy` | 39 | 0 | `Enquiry from ` |
| `credential` | 1 | 0 | `deku-demo-pw-2026` |
| `design_phrase` | 8 | 0 | `electric ultramarine blue` |
| `discipline` | 5 | 0 | `branding` |
| `endpoint` | 9 | 0 | `/api/health` |
| `env_var` | 9 | 4 | `DATABASE_URL` |
| `number` | 13 | 0 | `4173` |
| `project` | 20 | 0 | `amts-card` |
| `project_client` | 18 | 0 | `AMTS Catania` |
| `project_title` | 20 | 0 | `AMTS Card` |
| `role` | 1 | 0 | `studio` |
| `route` | 8 | 0 | `/works` |
| `scheme` | 2 | 0 | `company_website` |
| `seed_record` | 11 | 0 | `Giulia Ferro` |
| `status` | 3 | 0 | `new` |

## Grading window

```
VERDICT  PASS   (/Users/apple/Desktop/deku/Output/16sept-k95/S_local_crud_spatial-works-showcase-vb_20260916_102814/instruction.md)
section        H2                chars  reference  flag
core_features  Core features     14388       2400  past-slice
user_flow      User flow          3152       1900  past-slice
ui_ux_notes    UI/UX notes        4316       1700  past-slice
constraints    Constraints         705        800  ok
user_roles     User roles         1367       1000  over-reference
overview       Overview           1721        700  over-reference
joined total                     25649       8800  past-slice
first four                       22561       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```

## Kit gate log

| Gate | Tool | Exit | Verdict | Inputs hashed |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | 24 |
| G1/G12 | `layout_lint.py` | 0 | PASS | 24 |
| G46 | `structure_lint.py` | 0 | PASS | 24 |
| G50 | `docker_lint.py` | 0 | PASS | 24 |
| G55 | `runtime_deps_lint.py` | 1 | FAIL | 24 |
| G63 | `secret_lint.py` | 0 | PASS | 24 |
| G48 | `truth_lint.py` | 0 | PASS | 24 |
| G51 | `source_lint.py` | 0 | PASS | 24 |
| G52 | `rubric_context_lint.py` | 0 | PASS | 24 |
| G54 | `comment_lint.py` | 0 | PASS | 24 |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | 24 |
| G11 | `leak_scan.py` | 0 | PASS | 24 |
| G33 | `window_lint.py` | 0 | PASS | 24 |
| G4/G5 | `contract_lint.py` | 0 | PASS | 24 |
| G43 | `prescription_lint.py` | 0 | PASS | 24 |
| G44 | `disclosure_lint.py` | 0 | PASS | 24 |
| G10 | `no_sdk_lint.py` | 0 | PASS | 24 |
| G31 | `determinism_lint.py` | 0 | PASS | 24 |
| G14 | `reward_path_lint.py` | 0 | PASS | 24 |
| G27/G30 | `rubric_lint.py` | 0 | PASS | 24 |
| G41 | `flag_lint.py` | 0 | PASS | 24 |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | 24 |
| G59/G60 | `codequality_lint.py` | 2 | ? | 24 |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | 24 |
| G6 | `fixture_lint.py` | 0 | PASS | 24 |
| G24 | `coverage_map.py` | 0 | PASS | 24 |
| G37 | `checklist_qc.py` | 0 | PASS | 24 |
| G39 | `rubric_align_lint.py` | 0 | PASS | 24 |
| G28/G29 | `channel_lint.py` | 0 | PASS | 24 |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | 24 |
| G0/INV5 | `vendor_check.py` | 0 | PASS | 24 |
| G47 | `output_qc.py` | 1 | FAIL | 24 |

## Certification receipts

| Gate | Prompt | Verdict | PASS | WARN | N/A | FAIL |
|---|---|---|---|---|---|---|
| G3 | `task_code_verifier.md` | VALID | 12 | 0 | 0 | 0 |
| G34 | `QC_spec.md` | PASS | 13 | 2 | 0 | 0 |
| G34 | `QC_instruction.md` | PASS | 21 | 3 | 0 | 0 |
| G35 | `qc_docker.md` | PASS | 84 | 4 | 17 | 0 |
| G36 | `qc_toml.md` | PASS | 111 | 1 | 8 | 0 |
| G37 | `qc_solution_checklist.md` | PASS | 0 | 0 | 0 | 0 |
| G53 | `qc_rubric.md` | PASS | 14 | 1 | 1 | 0 |

## Companion carry

| Measure | Value |
|---|---|
| source | `/Users/apple/Desktop/deku/Drive_PRDs/16_sept/k95_prd.md`, 1,310 lines |
| colours described | 26 of 26 by family and tone |
| topics carried | 89 of 89 |
| enumerated items carried | 202 of 202 |
| waivers | 20 tokens in `_handoff/S_local_crud_spatial-works-showcase-vb_20260916_102814.sources.json` |

## Blocking findings

None for this bundle. Kit defects met again and reported: `QC_instruction.md` A1/B3 vs
`generate_instruction.md` 2.1 on `## Build plan`; `qc_docker.md` CMP-011 vs CMP-022 on
`ports:`; the mailpit fragment publishes host ports; the companion's placeholder contact address
ends in a reserved final label that G55 RD-6 fails, so the brief uses `hello@avx-studio.example.com`.

## Exit

**MECHANICALLY-GREEN, NO-SOLUTION.** Not admissible until the reference app lands and
`harbor run -a oracle` returns `1.0` twice.
