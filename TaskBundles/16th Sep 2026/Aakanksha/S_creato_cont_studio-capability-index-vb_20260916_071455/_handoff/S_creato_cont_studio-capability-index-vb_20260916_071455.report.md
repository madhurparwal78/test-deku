# Build report: studio-capability-index (variant b)

- task_code: `S_creato_cont_studio-capability-index-vb_20260916_071455`
- task: `deku/studio-capability-index-vb`
- cell: solo_founder / creator-monetization / content-publishing
- service_profile: P4-db-storage (postgres + minio)
- capability_flags: concurrency_hardening, data_scale
- design_direction: companion (supplied PRD, oimachi)
- exit state: MECHANICALLY-GREEN, NO-SOLUTION

## Input mapping

The Task Order named `domain: portfolio-agency`, not a taxonomy value; it was mapped to the
nearest legal solo_founder domain `creator-monetization` (a small creative studio monetizing its
craft). Pattern `content-publishing` was supplied and is legal in solo_founder; profile
P4-db-storage. The mapping and the companion carry are recorded in `_spec/.../00-decisions.md`.

## Gate sweep

ALL GATES GREEN, rendered from the machine receipts in `<project>.gates.jsonl` (written by
`revalidate.py`). Every static gate passes: G2/G16, G1/G12, G46, G50, G55, G63, G48, G51, G52,
G54, G17, G11, G33, G4/G5, G43, G44, G10, G31, G14, G27/G30, G41, G56/G57/G58,
G7/G8/G9/G32/G45, G6, G24, G37, G39, G28/G29, G40, G0/INV5, G47. G59/G60 report NOT-APPLICABLE
(product-half rubric only, a legal state).

## Adversarial QC (self-attested)

The six certification prompts (G34, G35, G36, G37, G53) and G3 are recorded in
`<project>.receipts.json` with `verifier: self` (recorded verdicts, not independent reviews).

## Artifacts

- brief: `instruction.md` (11 H2 sections; companion PRD carried, G51 13/13 topics + 51/51 items)
- checklist: `solution/checklist.md` (39 items, G37)
- answer key: `solution/trinity/grounding.yaml` -> generated TRUTH.md, rubrics.json, test_output.py,
  tests/rubric.json (byte-identical under G48)
- pytest layer: `tests/test_pytest.py` (27 functions), `tests/conftest.py`, `tests/workflows.yaml`
  (16 workflows), vendored `tests/test.sh`
- environment: `environment/Dockerfile`, `docker-compose.yaml`, `postgres-init.sql`

The graded hard parts: a draft case study and its media are not publicly readable (content-publishing
critical focus), a project enquiry submitted twice under one idempotency key creates exactly one
record, and the case study / article / experiment reads are cursor-paginated.
