# Build report - S_saasm_cont_design-agent-showcase-vb_20260916_055811

## Identity

| | |
|---|---|
| Task code | `S_saasm_cont_design-agent-showcase-vb_20260916_055811` |
| Task id | `deku/design-agent-showcase-vb` |
| Cell | solo_founder / saas-micro-tools / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | backend `postgres`, storage `minio` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `python` |
| Design direction | `companion` (drawn `terminal-mono`, superseded per reference/L SS L.6.1) |
| Launch surface | `colour_contrast, custom_404, no_broken_links, page_view_log, privacy_page` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 (no device sharding) |
| Kit | deku-green-field at commit `806eb0a`, vendored grader `0.22.0`, target schema `1.4` |
| Verifier mode | `separate` (kit default since 2026-09-16); the grader ships its own image |
| Companion source | `prd/framer_prd.md` (1693 lines), carried under 15 declared G51 waivers |

## Derived-design draws

| Axis | Value |
|---|---|
| render_model | `spa-json-api` |
| backend | `Flask` |
| frontend | `Vue 3 + Vite` |
| nav | `top-nav` on the public site, drawn `sidebar-nav` inside the studio |
| work_surface | `split detail-pane` |
| create_flow | `dedicated-route` |
| feedback | `inline-banner` |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Five marketing routes and the shared chrome | INCLUDED | `instruction.md` ## Core features | companion SS10-SS14 |
| Four scroll-scrubbed product replicas | INCLUDED | `instruction.md` ## Core features | companion SS9, SS16.2 |
| Customer-story desk with covers in the object store | INCLUDED | `instruction.md` ## Core features | the pattern's critical focus |
| Answer-engine scanner and its graded report | INCLUDED | `instruction.md` ## Core features | companion SS14, SS20.4 |
| Newsletter, contact message, cookie choice, page views | INCLUDED | `instruction.md` ## Core features | companion SS20.2, SS20.3, SS20.7 |
| Launch surface: privacy page, custom not-found, link health, page-view log, contrast | INCLUDED | ## Core features, ## UI/UX notes | reference/O draw |
| Confirmation and acknowledgement mail | DROPPED | - | `P4-db-storage` declares no email slot; carried as a no-mail two-step confirmation |
| Outbound fetch of the scanned address | DROPPED | - | no outbound network at run time; the scan grades from the site's own published methodology |
| Named frontend and backend framework as checklist items | DROPPED | `_spec/00-decisions.md` | not observable black-box; stated in ## Technical requirements only |
| Icon coordinate tables, the capture's evidence ledger | DROPPED | `_spec/00-decisions.md` | authoring provenance, declared as G51 waivers |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| backend | `postgres` | MET | `test_database_at_the_database_url_holds_the_seeded_rows`, plus 20 further tests reading rows through `capabilities.make_backend()` |
| storage | `minio` | MET | `test_uploaded_cover_bytes_live_in_the_object_store_at_the_key_scheme` (critical), `test_seeded_story_covers_exist_in_the_object_store`, `test_object_store_at_the_storage_endpoint_holds_the_cover_bytes` |

## Grading surface

| | |
|---|---|
| Checklist items | 168 |
| Workflows | 16 (band [10, 16] for solo_founder) |
| Browser substeps | 31 |
| pytest substeps | 75 |
| Critical substeps | 19 |
| Browser:pytest ratio | 0.413 (G45 band [0.40, 2.00]) |
| Non-happy-path workflow ids | 8: `invalid_scan_submission_is_refused_and_writes_nothing`, `visitor_subscribes_and_a_duplicate_address_creates_no_second_record`, `draft_story_is_denied_to_every_other_account`, `members_story_body_cannot_be_read_while_signed_out`, `reader_and_unauthenticated_requests_for_the_studio_are_denied`, `cover_upload_lands_in_the_object_store_and_an_invalid_one_is_refused`, `concurrent_story_creates_on_one_slug_leave_exactly_one`, `duplicate_signup_and_an_expired_token_are_both_refused` |
| pytest module | one merged `tests/test_output.py`, 75 test functions |
| Category mix | business_rule 14, core_outcome 6, data_integrity 16, presentation 12, security 17, validation 10 |

Sections the one module covers: core features, authorization, data integrity, edge cases, and both
declared slots. Coverage is two-way and green (G24): every checklist item is cited by at least one
grader and every citation resolves, with every `cov:` tag earned by shared wording.

## Rubric

17 judged criteria, 15 positive and 2 negative (commission).
`task completion` share 0.706 (band 0.60-0.80).

| Dimension | Criteria | Positive share | Target |
|---|---|---|---|
| `instruction_following` | 3 | 0.289 | 0.30 |
| `functionality` | 2 | 0.222 | 0.25 |
| `ux_flow` | 2 | 0.133 | 0.15 |
| `ui_visual` | 2 | 0.133 | 0.15 |
| `motion` | 3 | 0.111 | 0.05 |
| `accessibility` | 2 | 0.089 | 0.05 |
| `responsiveness` | 1 | 0.022 | 0.05 |

The reference rubric in `solution/trinity/rubrics.json` carries 14 items at a compiled-weight share
of 0.893 (floor 0.60). Both rubrics are GENERATED from `solution/trinity/grounding.yaml` by the
vendored `recompute.py`; neither is hand-edited, and G48 re-runs the generator to prove it.

## Literals ledger

162 entries. By class: account 3, credential 1, design_phrase 19, endpoint 21, env_var 8, motion_moment 8, number 3, route 14, scheme 3, seed_record 52, status 30.
Every non-verifier-only value appears verbatim in `instruction.md`; the one `verifier_only` value
(`DB_ADMIN_URL`) appears only in `task.toml` `[verifier].env`. Verified both directions by G6.

## Spec folder

Authoring docs at `output/16-sep-2026/_spec/S_saasm_cont_design-agent-showcase-vb_20260916_055811/`, excluded from the bundle per CON-5.

| Doc | Feeds |
|---|---|
| `00-decisions.md` | the draws, every residual call, the companion carry table, the G51 waivers |
| `01-PRD.md` | ## Overview, ## Core features, ## Constraints |
| `02-TRD.md` | ## Technical requirements |
| `03-app-flow.md` | ## User flow |
| `04-uiux-brief.md` | ## UI/UX notes, ## Front-end specification |
| `05-backend-schema.md` | ## Data model, ## User roles |
| `06-implementation-plan.md` | nothing: `## Build plan` is not emitted at baseline |

## Grading window

Measured by `window_lint.py` (G33), which reports length and fails nothing.

| Section | Chars | Reference |
|---|---|---|
| core_features | 27080 | 2400 |
| user_flow | 6251 | 1900 |
| ui_ux_notes | 11365 | 1700 |
| constraints | 1671 | 800 |
| user_roles | 1965 | 1000 |
| overview | 2210 | 700 |

Deliberate, and recorded: the tasker set the section caps aside so the companion's UI and UX
specification could be carried in full, and `generate_instruction.md` SS4 states the brief has no
length limit. Content past a slice reaches the agent whole and the judge in part; `judge_score`
never touches reward, so no reward-driving rule was trimmed. The critical focus sits in the first
third of `## Core features`.

## Kit gate log (RENDERED from `_handoff/S_saasm_cont_design-agent-showcase-vb_20260916_055811.gates.jsonl`, never transcribed)

| Gate | Tool | Exit | Verdict | Tool line |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS |  |
| `G1/G12` | `layout_lint.py` | 0 | PASS |  |
| `G46` | `structure_lint.py` | 0 | PASS |  |
| `G50` | `docker_lint.py` | 0 | PASS |  |
| `G55` | `runtime_deps_lint.py` | 0 | PASS |  |
| `G63` | `secret_lint.py` | 0 | PASS |  |
| `G48` | `truth_lint.py` | 0 | PASS |  |
| `G51` | `source_lint.py` | 0 | PASS |  |
| `G52` | `rubric_context_lint.py` | 0 | PASS |  |
| `G54` | `comment_lint.py` | 0 | PASS |  |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS |  |
| `G11` | `leak_scan.py` | 0 | PASS |  |
| `G33` | `window_lint.py` | 0 | PASS |  |
| `G4/G5` | `contract_lint.py` | 0 | PASS |  |
| `G43` | `prescription_lint.py` | 0 | PASS |  |
| `G44` | `disclosure_lint.py` | 0 | PASS |  |
| `G10` | `no_sdk_lint.py` | 0 | PASS |  |
| `G31` | `determinism_lint.py` | 0 | PASS |  |
| `G14` | `reward_path_lint.py` | 0 | PASS |  |
| `G27/G30` | `rubric_lint.py` | 0 | PASS |  |
| `G41` | `flag_lint.py` | 0 | PASS |  |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS |  |
| `G59/G60` | `codequality_lint.py` | 2 | NOT-APPLICABLE |  |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS |  |
| `G6` | `fixture_lint.py` | 0 | PASS |  |
| `G24` | `coverage_map.py` | 0 | PASS |  |
| `G37` | `checklist_qc.py` | 0 | PASS |  |
| `G39` | `rubric_align_lint.py` | 0 | PASS |  |
| `G28/G29` | `channel_lint.py` | 0 | PASS |  |
| `G40` | `prompt_receipt_lint.py` | 0 | PASS |  |
| `G0/INV5` | `vendor_check.py` | 0 | PASS |  |
| `G47` | `output_qc.py` | 0 | PASS |  |

Traceability: `tests/traceability-matrix.md` and `.csv`, regenerated by the same sweep from the
scan G24 makes, so they cannot disagree with the gate.

## Prompt receipts (G40)

Seven certification prompts carry a current, bundle-bound receipt with the scorecard their own
registry declares: `task_code_verifier.md` (VALID, 12/12), `QC_spec.md` (PASS, 15/15),
`QC_instruction.md` (PASS, 22 PASS + 2 WARN), `qc_toml.md` (PASS, 113 PASS + 1 WARN + 6
NOT-APPLICABLE), `qc_docker.md` (PASS, 98 PASS + 7 NOT-APPLICABLE), `qc_solution_checklist.md`
(PASS), `qc_rubric.md` (PASS, 16/16). Every one is **SELF-ATTESTED**: owner and verifier are the
same agent, which the kit records rather than counts as independent review.

## Kit alignment, 2026-09-16

Re-aligned to kit HEAD (`1b99060` through `806eb0a`) after the bundle was first built:

| Kit change | Applied here |
|---|---|
| `da24d3b` pytest module renamed | `tests/test_pytest.py` -> `tests/test_output.py`; every `test:` in `workflows.yaml`, the `tests/Dockerfile` COPY list and both module docstrings follow |
| `da24d3b` compiled rubric renamed | `solution/trinity/test_output.py` -> `test_ans.py`, regenerated by the re-vendored `recompute.py` |
| `806eb0a` USER_README restored | `solution/USER_README.md` is GENERATED again, carrying the literals and both canary lines; G12 checks it in TRUTH.md and here |
| `11eaf7b` verifier mode | `[verifier].environment_mode` = `separate`; the agent image drops the grader runtime (pytest, playwright, chromium, its system libraries and `PYTHONPATH=/tests`) and keeps `flask`, `gunicorn`, `psycopg`, `boto3`, Node 20 and `postgresql-client`. G55 RD-1 and RD-2 correctly skip under this mode |
| `78e5ba6` test.sh re-pinned | `tests/test.sh` re-copied; `vendor_check.py` is byte-identical to the new MANIFEST |
| `11eaf7b` qc_toml VERIF-001 | the row now expects `separate`; the prompt was re-read, the check re-answered PASS and the G36 receipt re-pinned to `pr_b46d6748` |
| `1b99060` code_quality dimension | no change: this bundle carries no `evaluation_target: "source"` criterion, so G59/G60 stay NOT-APPLICABLE |

## Corpus-level gates (run at S10, over the whole output root)

The root now holds a second bundle in the SAME cell, `S_saasm_cont_edge-platform-showcase-vb_20260916_061858`,
so the two comparison gates have something to compare and no longer report NOT-APPLICABLE.

| Gate | Result | What was compared |
|---|---|---|
| G42 `corpus_overlap.py` | **PASS** | 2 bundles, 1 cross-archetype pair; no pair exceeds the 60% substep-overlap cap |
| G49 `diversity_lint.py` | **PASS** | the verbatim-reuse half ran over both briefs: no shared literal run over the per-section caps. The concentration half stays NOT-APPLICABLE until 5 bundles exist |
| G26 `corpus_report.py` | **FAIL, corpus-level** | payments-or-email share 0.0% against a 28% floor, 0 of 2. Structural for this cell: `S`+`cont` resolves to `P4-db-storage`, which carries neither slot, so no content-publishing bundle can move this number. It clears as bundles land in payments and email cells |
| G61 `corpus_report.py` | **WARN, advisory** | no bundle carries a `difficulty` yet; the mix cannot be read until a calibration sweep has run |

## Blocking findings

NONE. Three companion obligations are declared un-gradeable rather than dropped silently and are
recorded in `_spec/S_saasm_cont_design-agent-showcase-vb_20260916_055811/00-decisions.md`: the named frontend framework, the named backend framework,
and "no second backing service". All three remain stated in `## Technical requirements`; none is
minted as an uncitable checklist item.

## Budget

`turns_expected = 180`, `tokens_expected = 900000`. Reasoning: nine tables, sixteen routes, four
staged replicas and a long visual specification put this above a plain CRUD build; the agent writes
one Flask service, one Vue application and a seed, with no second runtime to stand up.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. No reference application exists and nothing here has been compiled or run.
