# Build report: S_conte_trac_playable-portfolio-world-vb_20260916_101849

Rendered from `_handoff/S_conte_trac_playable-portfolio-world-vb_20260916_101849.gates.jsonl`. No verdict in this file was typed by hand;
each row below is the recorded exit code of the tool that owns it.

## Identity

| Field | Value |
|---|---|
| task code | `S_conte_trac_playable-portfolio-world-vb_20260916_101849` |
| task id | `deku/playable-portfolio-world-vb` |
| category | `solo_founder` |
| domain | `content-publishing` |
| pattern | `tracker-log` |
| service_profile | `P1-db` |
| variant | `b` |
| variant_axes | `critical_depth, spec_sections` |
| language | `typescript` |
| capability_flags | `aesthetic` |
| design_direction | `companion` |
| launch_surface | `form_validation,meta_tags,mobile_viewport,single_cta,social_preview` |
| spec_sections_given | `overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract` |
| grader_version | `0.22.0` |
| schema_version | `1.4` |
| uuid_v5 | `5b2ded2e-72f7-53e6-9a32-ea14e8ed41d8` |
| authors | `kaustubh.dalvi@ethara.ai, kunal.singh.int5@ethara.ai` |
| contributor_id | `kunal.singh.int5@ethara.ai` |
| exit state | `MECHANICALLY-GREEN, NO-SOLUTION` |

## Kit revision

Built against `GreenField-GenKit2` branch `madhur-test` at
`ac66ec3 2026-09-16 15:07:00 +0530`, PRD mode (`00-RUN.md`, `run.yaml`, G64, the
prd-generator splitter).

The output root was set per invocation with `DEKU_OUTPUT_ROOT`, not by editing
`config/kit-config.yaml`: that file is shared and already points at another run's
folder, and rewriting it would move a sibling bundle's root. Every gate command in
this report was run with

```
export DEKU_OUTPUT_ROOT="C:/Users/Admin/Downloads/Sep/Sep-16/Task 6-10/Output/16sept_paodao"
```

## Inputs

| Input | Path |
|---|---|
| PRD (companion source) | `Task 6-10/PRD/paodao_prd.md`, split by `prd-generator/tools/split_prd.py` into `paodao_prd_plain.md` and `paodao_prd_technical.md` |
| Input details | `Task 6-10/PRD/paodao_input.yaml` |
| Idea file (authored) | `Task 6-10/PRD/paodao_idea.yaml` |
| Run file (authored) | `Task 6-10/PRD/paodao_run.yaml` |
| G51 recorded source | `paodao_prd_plain.md`, 28 of 28 sections carried |

## Providers per slot

| Slot | Provider | Agent variables | Verifier marker |
|---|---|---|---|
| `backend` (db) | `postgres` | `DATABASE_URL`, `DB_URL` | `DEKU_SERVICE_BACKEND`, `DB_ADMIN_URL` |

No second store, cache, queue, object store, identity provider or mail vendor is
declared. The live leaderboard is served by the app itself over an event stream, so the
`realtime` slot stays UNRESOLVED and undeclared (in-app behaviour is not a service slot).

## Taxonomy mapping

The Task Order named `portfolio-agency` as the domain and `tracker-logging` as the
pattern. Neither is a legal level-2 or level-3 code, and `taskorder_lint.py` refused
them. They were mapped to the nearest legal cell and the mapping is recorded in
`_spec/S_conte_trac_playable-portfolio-world-vb_20260916_101849/00-decisions.md`:

| Task Order | Recorded as | Why |
|---|---|---|
| `portfolio-agency` | `content-publishing` | a one-page published portfolio is a publishing surface; the same mapping the sibling `design-studio-showcase` bundle uses |
| `tracker-logging` | `tracker-log` | the graded spine counts runs and totals per player and serves a board over them |

## Grading layer

| Channel | Count | Notes |
|---|---|---|
| workflows | 16 | solo_founder band is 10 to 16 |
| browser substeps | 38 | ratio 0.40 against the pytest substeps |
| pytest tests | 94 | one module, `tests/test_output.py` |
| judged rubric criteria | 54 | `tests/rubric.json`, generated from `grounding.yaml` |
| compiled rubric items | 30 | `solution/trinity/rubrics.json`, compiled weight share 1.0 |
| checklist items | 608 | 236 core asks, 236 fully graded, 0 uncovered |
| literals ledger | 82 | 1 verifier-only (`DB_ADMIN_URL`) |

Channel split (G28/G29): pytest 420 items, browser 72, rubric 123, with 7 items
legitimately shared between pytest and the browser.

About thirty of the pytest tests drive Playwright against the rendered world, which is
what makes the front-end half of the brief gradeable at all: the exact French copy, the
pinned type sizes, the layer rules, the settings, the notebook, the gamepad and touch
paths, and the no-3D fallback. The event stream, the rate limit, the name rules and the
denial matrix are HTTP and database assertions.

## Kit gate log

33 gates recorded, 0 red.

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
| G64 | `run_lint.py` | 0 | PASS |
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

## Certification prompts

| Prompt | Gate | Scope | Checks | Verdict | Verifier |
|---|---|---|---|---|---|
| `QC_instruction.md` | G34 | certification | 24 | PASS | self |
| `QC_spec.md` | G34 | certification | 15 | PASS | self |
| `docker_generator.md` | S5 | advisory | 0 | PASS | self |
| `generate_instruction.md` | S2 | advisory | 0 | PASS | self |
| `pytest_generator.md` | S7 | advisory | 0 | PASS | self |
| `qc_docker.md` | G35 | certification | 105 | PASS | self |
| `qc_rubric.md` | G53 | certification | 16 | PASS | self |
| `qc_solution_checklist.md` | G37 | certification | 0 | PASS | self |
| `qc_toml.md` | G36 | certification | 120 | PASS | self |
| `rubric_author.md` | S8 | advisory | 0 | PASS | self |
| `solution_checklist.md` | S3 | advisory | 0 | PASS | self |
| `task_code_verifier.md` | G3 | certification | 12 | VALID | self |
| `toml_generator.md` | S4 | advisory | 0 | PASS | self |

Findings recorded by those runs:

- C7 WARN: the grading window is wide for the standard tier. The brief earns 38 browser substeps and 94 pytest tests, and the world loads twice before most front-end assertions can run.
- CMP-011 WARN: the main service publishes 4173:4173. CMP-022 requires main to carry ports, and every reference bundle publishes the app port there, so the two rows conflict and CMP-022 wins. No sidecar publishes a host port.
- DEP-004 WARN: build-essential, python3 and pkg-config are installed for node-gyp native rebuilds (a password hash module is the likely consumer). No source names them, so they are justified by inference rather than by the TRD.
- RC-02 WARN: four items (C-CF-131, C-FE-02, C-FE-18, C-UX-36) are cited by two criteria each. In every case one criterion states the requirement and its mirror states the defect, so the pair grades two facets rather than one twice.
- INST-004 WARN: the grading layer is 38 browser substeps and 94 pytest tests, about 30 of which drive Playwright through two world loads. The standard-tier [verifier].timeout_sec of 3600.0 is kept for tier conformance, and calibration should confirm the browser pass fits inside it.

Every verdict above is SELF-ATTESTED: one agent authored the artifacts and ran the QC
prompts over them. The kit's standard is owner != verifier, and this run does not meet
it.

## Known caveats

- **No reference application exists.** `solution/solve.sh` prints NO-SOLUTION and exits
  1. Every verdict in this report is static analysis over authored bytes; nothing has
  been compiled or run.
- **`[delivery.images]` is absent.** A registry digest cannot be resolved without network
  access to the registry, and stage 5 forbids fabricating one. Resolve and pin
  `node:20.18.1-bookworm-slim` and `postgres:16.4-bookworm` before packaging.
- **The grading window is wide for the standard tier.** `[verifier].timeout_sec` is the
  tier value `3600.0`; with 38 browser substeps and about thirty Playwright tests that
  each cross two world loads, calibration should confirm the pass fits, and raise the
  budget if it does not.
- **`## Core features` is 29,333 characters**, past the 2,500-character point where
  `run_rubric.py` slices a section for the judge. The whole section reaches the agent;
  the judge sees the head of it, which is why every rubric criterion carries its own
  facts rather than pointing at the brief (G52).
- **Two pytest tests read `/app` from the verifier** (`USER_README.md` and the reserved
  directories). The vendored `run_workflows.py` reads `/app/USER_README.md` the same way
  under `environment_mode = "separate"`, so the assumption is the harness's own; if
  Harbor does not mount the app tree into the verifier, those two tests fail and the
  obligations C-DC-05 and C-DC-06 lose their observation.
- **Four checklist items are graded by two rubric criteria each** (C-CF-131, C-FE-02,
  C-FE-18, C-UX-36). In each pair one criterion states the requirement and the other
  states the defect, which is the negative half of the battery rather than double
  grading.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

Not admissible. The bundle carries no reference app, so G13, G15, G18, G19, G20, G21 and
G25 are unproven. Build the app downstream from `solution/checklist.md`, then run the
handoff gates in `_handoff/S_conte_trac_playable-portfolio-world-vb_20260916_101849.handoff.md`.
