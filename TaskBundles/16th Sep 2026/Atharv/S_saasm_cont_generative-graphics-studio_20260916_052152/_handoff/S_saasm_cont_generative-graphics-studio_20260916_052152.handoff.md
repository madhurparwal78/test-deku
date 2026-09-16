# Handoff contract

```
BUNDLE          Output/S_saasm_cont_generative-graphics-studio_20260916_052152/
TASK CODE       S_saasm_cont_generative-graphics-studio_20260916_052152
TASK ID         deku/generative-graphics-studio
STATE           MECHANICALLY-GREEN, NO-SOLUTION
                NOT ADMISSIBLE. No reference application exists yet, so the oracle
                gate has never run. Three gates are RED and are named below.

CELL            solo_founder / saas-micro-tools / content-publishing
                TWO ENUM SUBSTITUTIONS, both forced and both recorded in
                Output/_spec/S_saasm_cont_generative-graphics-studio_20260916_052152/00-decisions.md:
                  domain  `saas-productivity` is not one of the 36 -> saas-micro-tools
                  pattern `media-gallery`     is not one of the 15 -> content-publishing
                `feed-social` was the closer NAME and was rejected on its critical
                focus: it grades "Block/visibility enforced at API" and this product
                has no blocking, so honouring it would mean inventing a feature to
                satisfy a label. content-publishing grades "Object in store;
                protected content not publicly readable", which is the boundary the
                product already turns on.

SOURCE          c:/Users/Admin/Downloads/fffuel_prd.md (6,012 lines), recorded in
                _handoff/S_saasm_cont_generative-graphics-studio_20260916_052152.sources.json. The source designs a much larger product
                than one task can carry: 67 tools, a public generation API, real-time
                collaboration, workspaces, moderation and colour science. The brief
                scopes to one buildable task and names every omission in
                ## Constraints.

GRADER VERSION  0.22.0, vendored byte-identical (G0 PASS)
SERVICE PROFILE P4-db-storage -> PostgreSQL + MinIO
DRAWS           render_model mpa-progressive / Express + Nunjucks / vanilla
                progressive enhancement; design_direction clinical-precision;
                nav sidebar-nav; work_surface card-grid; create_flow dedicated-route;
                feedback full-page-confirmation; launch_surface cookie_choice,
                form_validation, mobile_viewport, no_broken_links, terms_page.
                NO DRAW WAS OVERRIDDEN.

MEASURES        instruction.md 42,192 chars, ASCII only, zero em or en dashes
                checklist 630 items, all 630 cited by a grader (G24 PASS)
                workflows 16, browser-carrying 13 (81%), pytest substeps 48
                rubric 19 judged criteria + 24 compiled items
                every table carries its own id, the child tag table included

OPEN RED GATES
  G40  prompt_receipt_lint  FAIL, and deliberately so. The gate asks for a receipt
                            attesting that each prompt-driven QC pass was READ and
                            RUN: 24 + 15 + 105 + 16 + 120 + 12 = 292 checks across
                            six HARD prompts. Those passes were NOT run in this
                            session, only the mechanical tool battery was. Writing
                            receipts for them would be fabricated attestation, which
                            is the exact failure G40 exists to catch, so the gate is
                            left red. To close it, run the six prompts against this
                            bundle and emit the receipts they produce.
  G51  source_lint          FAIL, 248 findings. It compares the 6,012-line source
                            against a brief scoped to one task. Two substantive gaps
                            it found WERE fixed: the source's output palette now
                            reaches ## UI/UX notes as described colours rather than
                            being absent, and the permalink, history, randomize and
                            grid-ordering asks are now either carried or named in
                            ## Constraints. The residual is the scoped-out half of
                            the source; 76 headings are waived in
                            _handoff/waived-sections.json.
  G47  output_qc            FAIL, entirely downstream of the two above.

HANDOFF GATES   in this order:
  STEP 0  build the reference app, point DEKU_REFERENCE_APP at it, leave solve.sh
          as shipped. solution/app/ is RETIRED: the app never ships in the bundle.
  G13  docker build -f environment/Dockerfile .   expect exit 0
  G13  docker build -f tests/Dockerfile .         expect exit 0, needs
       deku-verifier-base:0.2 built from vendor/grader-0.22.0/Dockerfile
  G15  docker compose up --wait                   expect postgres + minio healthy
  G19  harbor run -a oracle                       expect reward == 1.0, twice
  G20  harbor run -a nop                          expect reward == 0.0
  G21  fake-integration patch, re-run oracle      expect reward < 1.0
  G25  reviewer exploit sweep                     expect 0 of 11 succeed

KNOWN UNPROVEN  nothing here has been compiled or run. No image was built, no
                container started, no test executed. The 48 pytest functions are
                authored against the vendored adapters and have never met an app.
```

## Gate log

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 2 | NOT-APPLICABLE |
| G1/G12 | `layout_lint.py` | 0 | PASS |
| G46 | `structure_lint.py` | 0 | PASS |
| G50 | `docker_lint.py` | 0 | PASS |
| G55 | `runtime_deps_lint.py` | 0 | PASS |
| G63 | `secret_lint.py` | 0 | PASS |
| G48 | `truth_lint.py` | 0 | PASS |
| G51 | `source_lint.py` | 1 | FAIL |
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
| G40 | `prompt_receipt_lint.py` | 1 | FAIL |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 1 | FAIL |
