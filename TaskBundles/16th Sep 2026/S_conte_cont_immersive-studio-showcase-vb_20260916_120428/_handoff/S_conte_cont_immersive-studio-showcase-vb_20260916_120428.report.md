# Gate report - S_conte_cont_immersive-studio-showcase-vb_20260916_120428

Task: `deku/immersive-studio-showcase-vb`
Source companion: `9.16_prds/prd4/dogstudio_prd.md`
Swept by `tools/revalidate.py` over the whole bundle, with the deliberate-drop waivers listed
below.

## Verdict

**ALL GATES GREEN (MECHANICALLY-GREEN).** Thirty-two gate receipts, none red. This is not
admissibility: that needs a reference application and `harbor run -a oracle` returning `1.0`
twice, neither of which exists yet.

## Gate receipts

| Gate | Tool | Verdict | Exit |
|---|---|---|---|
| G2/G16 | `validate_task.py` | NOT-APPLICABLE | 2 |
| G1/G12 | `layout_lint.py` | PASS | 0 |
| G46 | `structure_lint.py` | PASS | 0 |
| G50 | `docker_lint.py` | PASS | 0 |
| G55 | `runtime_deps_lint.py` | PASS | 0 |
| G63 | `secret_lint.py` | PASS | 0 |
| G48 | `truth_lint.py` | PASS | 0 |
| G51 | `source_lint.py` | PASS | 0 |
| G52 | `rubric_context_lint.py` | PASS | 0 |
| G54 | `comment_lint.py` | PASS | 0 |
| G17 | `secret_hygiene_lint.py` | PASS | 0 |
| G11 | `leak_scan.py` | PASS | 0 |
| G33 | `window_lint.py` | PASS | 0 |
| G4/G5 | `contract_lint.py` | PASS | 0 |
| G43 | `prescription_lint.py` | PASS | 0 |
| G44 | `disclosure_lint.py` | PASS | 0 |
| G10 | `no_sdk_lint.py` | PASS | 0 |
| G31 | `determinism_lint.py` | PASS | 0 |
| G14 | `reward_path_lint.py` | PASS | 0 |
| G27/G30 | `rubric_lint.py` | PASS | 0 |
| G41 | `flag_lint.py` | PASS | 0 |
| G56/G57/G58 | `if_lint.py` | PASS | 0 |
| G59/G60 | `codequality_lint.py` | ? | 2 |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | PASS | 0 |
| G6 | `fixture_lint.py` | PASS | 0 |
| G24 | `coverage_map.py` | PASS | 0 |
| G37 | `checklist_qc.py` | PASS | 0 |
| G39 | `rubric_align_lint.py` | PASS | 0 |
| G28/G29 | `channel_lint.py` | PASS | 0 |
| G40 | `prompt_receipt_lint.py` | WARN | 0 |
| G0/INV5 | `vendor_check.py` | PASS | 0 |
| G47 | `output_qc.py` | PASS | 0 |

`G2/G16` reports NOT-APPLICABLE only because `task.toml` carries no `[delivery]` block; the
schema and taxonomy halves both pass. `G59/G60` reports exit 2 because the bundle ships no
code-quality rubric, which is optional. `G40` reports WARN because every certification prompt
was run by the same agent that authored the artifact, which the kit records as SELF-ATTESTED
rather than as an independent verdict.

## Prompt receipts

| Prompt | Gate | Verdict | Checks answered | Verifier |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | self |
| `QC_spec.md` | G34 | PASS | 15 | self |
| `docker_generator.md` | S5 | PASS | - | self |
| `generate_instruction.md` | S2 | PASS | - | self |
| `pytest_generator.md` | S7 | PASS | - | self |
| `qc_docker.md` | G35 | PASS | 105 | self |
| `qc_rubric.md` | G53 | PASS | 16 | self |
| `qc_solution_checklist.md` | G37 | PASS | - | self |
| `qc_toml.md` | G36 | PASS | 120 | self |
| `rubric_author.md` | S8 | PASS | - | self |
| `solution_checklist.md` | S3 | PASS | - | self |
| `task_code_verifier.md` | G3 | VALID | 12 | self |
| `toml_generator.md` | S4 | PASS | - | self |

### Recorded non-passes

- **`QC_instruction.md`** C7: the brief runs past the judge's 2500-character per-section slice in '## Core features' and past the 9000-character join slice. The section-cap constraint was waived by the task owner in favour of a fuller UI/UX specification; the tail reaches the agent in full and only the rubric judge reads less. Recorded, not repaired.
- **`qc_docker.md`** CMP-019: environment/docker-compose.yaml carries 'restart: unless-stopped' on the postgres and minio sidecars. Both lines are inherited verbatim from the kit's own central fragments at environment/providers/<p>/service.yaml, which environment/compose.py splices unchanged, so removing them would put the bundle out of step with the generator. Reported against the generator, not repaired in the bundle.
- **`qc_docker.md`** CMP-020: superseded for this bundle by CMP-022, which REQUIRES the main service to set extra_hosts and ports. The two rules disagree and CMP-022 is the specific one.

## Warnings carried, not repaired

- **Section length.** `## Core features` is about 11,900 characters and the whole brief about
  55,000. The rubric judge reads a 2,500-character slice per section and a 9,000-character
  join, so the tail reaches the agent in full and the judge in part. The task owner waived the
  section-cap constraint in favour of a fuller UI/UX specification, so this is a chosen
  trade-off rather than an oversight.
- **Launch surface above the floor.** The brief carries fifteen of the eighteen bank
  obligations where five were drawn. The companion PRD already stated ten of them, and the
  floor is a minimum, so carrying more is the correct outcome.
- **`restart: unless-stopped` on the sidecars.** `qc_docker` CMP-019 asks for compose sidecars
  free of `restart:`. Both lines come verbatim from the kit's own central fragments at
  `environment/providers/<provider>/service.yaml`, which `environment/compose.py` splices
  unchanged. Reported against the generator rather than repaired here.

## Defect found and repaired during certification

Running `qc_toml` CMP-005 and `qc_docker` against the bundle caught a Bug-2-shaped defect:
`[environment].env` injected `STORAGE_ACCESS_KEY = "deku_app"` and
`STORAGE_SECRET_KEY = "deku-local-dev"` while the MinIO service in
`environment/docker-compose.yaml` only ever creates the root user `minioadmin` with the
password `minio-root-3d81f7a2`. A complete, correct application would have failed every
object-store call and scored zero with nothing in the app to fix. Both variables now carry the
credentials the container actually has, on the agent side and on the verifier side.

## Deliberate drops from the companion (G51 waivers)

- `Normative versus informational`
- `Observed implementation, informational`
- `Evidence gaps and substitutions`
- `The loader-dominated capture`
- `SOCIALDRURL`
- `SOCIALTWURL`
- `max-width: 50.9275em`
- `Gold and amber`
- `ease-house`
- `ease in rare accelerations`
- `Our goal is to deliver amazing experiences`
- `The Whitfield Center Design Building an immersive website`
- `Grand Opera of Verdal Design Imagining and designing`
- `are transform and background-position`
- `dog.drc.glb`
- `matcap-combined-resized.jpg`
- `flag-en.jpg`

Each is either a raw design token the A5 number rule forbids the brief from carrying (a hex, a
cubic-bezier curve, a breakpoint in ems), a binary asset the zero-asset rule replaces, or a
passage of the PRD that describes the PRD rather than the product.
