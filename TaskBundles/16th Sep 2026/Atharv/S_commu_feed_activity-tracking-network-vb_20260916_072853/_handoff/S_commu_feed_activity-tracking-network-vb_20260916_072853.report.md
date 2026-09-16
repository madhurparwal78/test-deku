# Build report: S_commu_feed_activity-tracking-network-vb_20260916_072853

Rendered from `_handoff/S_commu_feed_activity-tracking-network-vb_20260916_072853.gates.jsonl`. Every verdict below is the receipt's
own exit code and verdict string. Nothing here is transcribed by hand.

## Identity

| | |
|---|---|
| Task code | `S_commu_feed_activity-tracking-network-vb_20260916_072853` |
| Task id | `deku/activity-tracking-network-vb` |
| Cell | solo_founder / community-social / feed-social |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Service profile | `P4-db-storage` (`backend = postgres`, `storage = minio`) |
| Language | typescript (Fastify) behind Nuxt 3, server-rendered with hydrated islands |
| Design direction | `companion` (the drawn `clinical-precision` does not govern) |
| Launch surface | `cookie_choice`, `custom_404`, `mobile_viewport`, `no_broken_links`, `social_preview` |
| Companion | `strava_prd.md`, 2,897 lines, 22,320 words |
| Kit | deku-green-field, grader pin 0.22.0, schema 1.4 |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## What the bundle carries

| | |
|---|---|
| Workflows | 16 (solo_founder band 10 to 16) |
| Browser substeps | 105 |
| Pytest substeps | 89 |
| Critical substeps | 19 |
| Test functions | 89, all in one `tests/test_output.py` |
| Checklist items | 384 across ten section codes |
| Trajectory steps | 16 |
| Rejected routes | 32 |
| Judged criteria | 15 (13 positive, 2 negative) |
| Literals ledger | 128 pinned values |

## Companion carriage (G51)

23 of 23 source colours described by family and tone, 170 of 170 topics carried,
465 of 465 enumerated items carried. Five waivers, each recorded in
`Output/_spec/S_commu_feed_activity-tracking-network-vb_20260916_072853/00-decisions.md`, and all five are the capture's own
provenance rather than product content.

## Kit gate log

31 PASS, 1 NOT-APPLICABLE, 0 FAIL.

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

## Red gates, with their own findings

None.
## Recorded, not blocking

**G40 is green on receipts that name `verifier: self`.** The six adversarial QC
prompts each carry a per-check scorecard at `_handoff/S_commu_feed_activity-tracking-network-vb_20260916_072853.receipts.json`, and
every receipt records its own author as the verifier. The kit's rule is
owner != verifier, so these are RECORDED verdicts rather than independent ones,
and `prompt_receipt_lint` says so on every run. An independent reviewer
re-running the six is the remaining strengthening step.

**One registry deviation, recorded in the qc_docker receipt.** The kit's MinIO
provider fragment pins `minio/minio` on Docker Hub, which now refuses an
anonymous manifest read, so an unauthenticated build cannot pull it. The same
release tag is served anonymously from MinIO's own registry, and
`environment/docker-compose.yaml` pins `quay.io/minio/minio` at that tag with
its resolved index digest. Everything else in the fragment is carried verbatim.

**`difficulty` is emitted empty.** CON-5 lists it DO-NOT-EMIT while stage-4, the
toml_generator section 11 template and qc_toml BENCH-006 all require it present
and uncalibrated. The kit's executable gate (G2) accepts the empty string, so
that is what ships, and the contradiction is left on the record.

## Not proven here

Battery 3 is handoff-owned and needs Docker and the harness: G13, G15, G18, G19,
G20, G21, G25. The answer key's replay half -- compiled tests accept the oracle
and reject the known-wrong controls -- is DEFERRED by G48 until the app exists.

## Budget

`turns_expected = 210`, `tokens_expected = 7500000`. The reasoning: the visible
product is a feed of cards, and underneath it are five subsystems that have to
agree on one transaction -- stream derivation, curve matching against a spatial
index, per-viewer leaderboards, hybrid feed fan-out, and a privacy model that
truncates stored geometry. The brief runs past 97,000 characters and the seed
carries nine synthesised fixture tracks whose answers are pinned. That is above
the corpus median for a feed-social task, which is why both numbers sit above
the `streak-habit-tracker` baseline.
