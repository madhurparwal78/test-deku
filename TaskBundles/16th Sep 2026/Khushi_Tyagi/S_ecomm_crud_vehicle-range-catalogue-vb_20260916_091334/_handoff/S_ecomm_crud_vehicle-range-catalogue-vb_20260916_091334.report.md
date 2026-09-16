# Build report - S_ecomm_crud_vehicle-range-catalogue-vb_20260916_091334
Rendered from `_handoff/S_ecomm_crud_vehicle-range-catalogue-vb_20260916_091334.gates.jsonl`. Never transcribed by hand (ISSUES C-02).

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`. The bundle carries no reference app; it is not admissible until one is built downstream and `harbor run -a oracle` returns `1.0` twice.

## Gate log

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
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | WARN |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 0 | PASS |

31 of 32 gates green.

## Not proven here

- Battery 3, handoff-owned: G13, G15, G18, G19, G20, G21, G25 - they need a built app and the harness.
- Adversarial LLM reviews G34, G35, G36, G37b and G53 were run by the build agent itself; `_handoff/S_ecomm_crud_vehicle-range-catalogue-vb_20260916_091334.receipts.json` records every check id and its verdict, and every one is SELF-ATTESTED rather than independent.

## Findings raised and resolved during the run

- **QC_instruction.md** C7: the six judged sections join to 40672 chars against the 9000-char judge slice; kept deliberately per generate_instruction section 4 (do not cut a real rule to fit) and reported by window_lint as past-slice, which costs a diagnostic number, never reward
- **QC_instruction.md** D5: the companion states at section 1.1 that there is no account anywhere and at section 17.2 that there is no write path; this brief adds an open signup and a signed-in owner who saves a comparison set, because the crud-catalog pattern row requires a persisted row and a permission boundary. Recorded as a deliberate extension in _spec/00-decisions.md; every public surface remains anonymous and unchanged
- **QC_spec.md** S7: 06-implementation-plan lists eight ordered steps but names no per-step exit condition and no deploy step. Build plan is not emitted in the brief at baseline, so the file is an authoring record only and the omission reaches no consumer
- **qc_toml.md** BENCH-002: the Trivial tier does not apply; this is a non-trivial task on the Standard tier
- **qc_toml.md** INST-007: instruction.md is present, so the SPEC folder is not treated as the brief
- **qc_toml.md** META-009: keywords carried the framework tokens flask and angular, which are not provider slugs. Corrected to greenfield, solo_founder, python, postgres, catalogue, facets
- **qc_toml.md** SIGN-001: deprecated 2026-09-15, superseded by SIGN-004
- **qc_toml.md** SIGN-002: deprecated 2026-09-15, superseded by SIGN-004
- **qc_toml.md** SIGN-003: deprecated 2026-09-15, superseded by SIGN-004
- **qc_toml.md** TAX-006: language is python, not any, so the trivial-task restriction does not apply
- **qc_toml.md** TAX-008: global archetype uniqueness cannot be decided from the supplied inputs; it is enforced by the mint ledger, which refused this archetype until the orphaned claim S_ecomm_crud_vehicle-range-catalogue-vb_20260916_061302 was released
- **qc_toml.md** VERIF-005: [verifier].env carried APP_PUBLIC_URL as http://main:4173; the verifier reaches the app on localhost. Corrected to ${APP_PUBLIC_URL:-http://localhost:4173}
- **qc_toml.md** VERIF-007: no payments or storage slot is declared under P1-db, so no shared provider credential is owed
- **qc_docker.md** ARCH-002: the base digest is the manifest-list digest carried by the kit's pinned node image
- **qc_docker.md** BP-005: no build-only toolchain is shipped that a second stage would remove
- **qc_docker.md** BP-008: the base is node:20-bookworm-slim, a glibc image, not musl or Alpine
- **qc_docker.md** CMP-005: environment/postgres-init.sql created deku_app with password deku-app-pw while task.toml injects deku_app:deku-local-dev, so the app could never authenticate. Corrected the init script to deku-local-dev
- **qc_docker.md** DEP-011: [verifier].environment_mode is separate, so the agent image owes no grader package
- **qc_docker.md** DEP-012: playwright is not installed in the agent image
- **qc_docker.md** DEP-013: playwright is not installed in the agent image
- **qc_docker.md** DEP-015: language is python, not go, rust or java; and the file carries no --break-system-packages
- **qc_docker.md** DEP-016: the image is single-stage with no compiled-language build stage
- **qc_docker.md** DEP-017: language is python, not java
