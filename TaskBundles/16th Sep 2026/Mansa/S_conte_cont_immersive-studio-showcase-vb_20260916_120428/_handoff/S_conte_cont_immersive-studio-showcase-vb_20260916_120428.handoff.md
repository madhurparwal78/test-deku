# Handoff - S_conte_cont_immersive-studio-showcase-vb_20260916_120428

## What this is

A Harbor greenfield task built from `https://dogstudio.co/` and its companion PRD at
`9.16_prds/prd4/dogstudio_prd.md`. The product is Northform, a multidisciplinary creative
studio's own marketing and portfolio site: a real-time three-dimensional mascot, a running-dog
loader, a featured-projects reel, case studies, a studio and values narrative, a careers list,
a journal, an ambient sound bed, and two conversions - a contact enquiry and a newsletter
subscription.

The graded core is the pattern's critical focus for `content-publishing`: **an object in the
store, and protected content that is not publicly readable.** A case study, a journal post or an
open role is `draft` or `published`, and a draft record's hero image sits in the same MinIO
bucket as a published one. Listing the bucket, guessing the key, or holding a link minted while
the record was published must not read it, and the refusal must be indistinguishable from
absence.

## Identity

| | |
|---|---|
| task_code | `S_conte_cont_immersive-studio-showcase-vb_20260916_120428` |
| task_id | `deku/immersive-studio-showcase-vb` |
| uuid_v5 | `b965516d-84f6-5ef2-b7b8-44206c2292bb` |
| cell | solo_founder / content-publishing / content-publishing |
| service profile | `P4-db-storage` (postgres, minio) |
| language | typescript |
| design direction | `companion` - a real product supplies the character, so the bank draw does not govern |
| launch surface | `custom_404,favicon,meta_tags,single_cta,sitemap_robots` |

## What is in the bundle

- `instruction.md` - the only file the agent sees. Eleven H2 sections, including an unbudgeted
  `## Front-end specification` carrying the visual detail the UI/UX section states in summary.
- `solution/checklist.md` - 297 items, the coverage target.
- `solution/trinity/grounding.yaml` - the answer-key source. `recompute.py` regenerates
  `TRUTH.md`, `USER_README.md`, `trinity/rubrics.json`, `trinity/test_ans.py` and
  `tests/rubric.json` from it byte-identically.
- `tests/workflows.yaml` - 16 workflows, 44 pytest substeps, 41 browser substeps.
- `tests/test_output.py` - 44 tests, black-box over HTTP plus the declared providers.
- `environment/` - the agent image, the compose file and the postgres bootstrap seed.

## Coverage

Every one of the 297 checklist items is cited by at least one grader: 196 by pytest, 110 by a
browser substep, 27 by a rubric criterion, with 30 legitimately shared between pytest and the
browser. No `ui` item is claimed by an HTTP-only test, no `contract`, `data` or `role` item is
claimed by the rubric, and no item is judged twice by both a browser substep and a criterion.

## What is NOT proven here

- **Admissibility.** No reference application exists, so `harbor run -a oracle` has never run.
  `solve.sh` is the NO-SOLUTION stub and exits non-zero on purpose.
- **Rubric liveness.** `truth_lint` reports the replay half DEFERRED: compiled tests accepting
  the oracle and rejecting the known-wrong controls cannot be shown without an app.
- **`[delivery]`.** The block is absent, which `validate_task.py` grandfathers to
  NOT-APPLICABLE. It requires `@sha256:` digests for the `node` and `postgres` images, and a
  fabricated digest is worse than an absent block, so it is left for whoever can pull the
  images and read the real ones.
- **Calibration.** `difficulty`, `reference_model_used`, `pass_rate`, `pass_rate_ci` and
  `calibration_trials` hold the exact placeholders the schema requires. No metric here is
  measured and none is invented.
- **Independent review.** Every certification prompt was run by the agent that authored the
  artifact, so `G40` records SELF-ATTESTED. An independent pass over `QC_instruction.md`,
  `qc_toml.md`, `qc_docker.md` and `qc_rubric.md` is still owed.
- **Gates G13, G15, G18-G21, G25** are handoff-owned, and **G23, G34-G36, G37b** are prose or
  adversarial-LLM gates. Neither battery runs in the mechanical sweep.

## Next steps

1. Build the reference application from `instruction.md` alone and run the verifier against it.
2. Fill `[delivery]` once the image digests can be read.
3. Run the calibration trials and replace the placeholders.
4. Have somebody other than the author re-run the four certification prompts.
