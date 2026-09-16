# Build report - S_conte_cont_webgl-agency-showcase-vb_20260916_065929

Rendered from `_handoff/S_conte_cont_webgl-agency-showcase-vb_20260916_065929.gates.jsonl`. No verdict below is transcribed; every row is the
machine receipt `revalidate.py` wrote. S10 renders, it never authors (ISSUES C-02).

**Aligned to the kit at commit `806eb0a`.** This bundle has now been realigned twice: once from
`7a667b7` to `b3d0577`, and again from `b3d0577` to `806eb0a`. Both passes are recorded below.

## Identity

| Field | Value |
|---|---|
| Task code | `S_conte_cont_webgl-agency-showcase-vb_20260916_065929` |
| Task id | `deku/webgl-agency-showcase-vb` |
| uuid_v5 | `23f55d8b-e735-55b2-b7da-fe427e51a3e3` |
| Bundle | `Output/16sept-phantom/S_conte_cont_webgl-agency-showcase-vb_20260916_065929/` -- flat, one level under the output root |
| Cell | solo_founder / content-publishing / content-publishing |
| Service profile | `P4-db-storage` (`backend = postgres`, `storage = minio`) |
| Variant | `b`, axes `[critical_depth, spec_sections]` |
| Authors | `abhishek.shaw@ethara.ai` (QL), `nishant.dubey@ethara.ai` (contributor) |
| Verifier mode | `separate` -- the kit default since `11eaf7b`; the grader ships its own image from `tests/Dockerfile` |
| Design direction | `warm-hospitality` |
| Launch surface | `no_frontend_secrets, privacy_page, security_headers, sitemap_robots, terms_page` |
| Stack drawn | NestJS behind React with Vite, `spa-json-api` |
| Kit | `deku-green-field` at `806eb0a` |
| Vendored grader | `0.22.0`, re-pinned at `78e5ba6` |

## Realignment, second pass (`b3d0577` to `806eb0a`)

| Commit | Change | What it cost here |
|---|---|---|
| `da24d3b` | the pytest module is `tests/test_output.py`; the compiled-rubric file becomes `trinity/test_ans.py` | module renamed again, every reference in workflows, grounding and the tests Dockerfile followed, and the stale `trinity/test_output.py` deleted |
| `11eaf7b` | `[verifier].environment_mode` defaults to `separate` | flipped; the grader now builds its own image from `tests/Dockerfile`, and qc_toml VERIF-001 was re-read against its revised row |
| `78e5ba6` | the vendored `test.sh` is stripped of whole-line comments and re-pinned | re-vendored; `vendor_check` confirms byte-identity with the new MANIFEST |
| `806eb0a` | `solution/USER_README.md` returns as a GENERATED file | now emitted by `recompute.py`, which writes five artifacts rather than four. It is generated, never authored: the seeded logins and the canary both descend from `grounding.yaml` |
| `1b99060` | `code_quality` added as an authored code-quality rubric dimension | attempted and **blocked**; see the G24 finding |

The bundle lives at `Output/16sept-phantom/<code>/`, per the operator's naming convention:
`<todaydate>-<prdname>`, where `phantom` is the supplied companion `phantom_prd.md`. That folder
is the output root for this run, so the bundle sits FLAT one level under it, which is what the
second half of the CON-1 placement rule asks for; the mint ledger sits beside it at
`Output/16sept-phantom/ledger.jsonl`. Sweeps set
`DEKU_OUTPUT_ROOT=/Users/apple/Downloads/GreenField-GenKit2/Output/16sept-phantom` rather than
editing the shared `config/kit-config.yaml`.

## Realignment, first pass (`7a667b7` to `b3d0577`)

Variant `b` re-mint for a companion task; `[task].authors` reduced to two bare addresses;
`uuid_v5` minted; `[signoff]` retired; per-substep `category` and derived `weight` (G9);
`solution/app/` retired and the canary moved to `solution/TRUTH.md`; `solve.sh` reduced to the
NO-SOLUTION stub; A5 applied, so the brief carries no hex and no easing curve and the type
families are named exactly; G51 item coverage closed at 303/303; and the five-token launch
surface drawn, written in as product prose and given five graders.

## Branch provenance, and what this bundle deliberately does not carry

Built on `madhur-test` at its tip, `806eb0a`, on the operator's instruction to stay on that
branch only.

`origin/yasir-test` carries one commit `madhur-test` does not: `066e565`, "Add PRD mode and link
mode: run.yaml, G64/G65, prd-generator integration". The two branch tips differ by exactly that
commit; the five commits above are content-identical on both branches and differ only in sha
after a rebase.

That commit would have applied to this task, since it is PRD-driven. Under it a run is described
by a `run.yaml` in PRD mode (`idea_file`, `plain_prd`, `ql_email`, `author_email`),
`tools/run_lint.py` (G64) validates it and writes `_handoff/<project>.sources.json`, and
`revalidate.py` reads the recorded source so a sweep needs no `--source`. This bundle carries
none of that: it has no `run.yaml` and no `sources.json`, and its sweeps are run with
`--source /Users/apple/Downloads/phantom_prd.md` passed explicitly. A bare Task Order with a
companion document remains valid under `066e565`, so nothing here is invalidated by the gap; the
bundle simply predates PRD mode and is recorded as such.

Gate range for this bundle is therefore G0-G63. G64 and G65 do not exist on this branch.

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | `postgres` | **MET** | `test_public_count_endpoint_matches_published_total`, `test_seeded_thumbnail_objects_exist_in_the_store`, both critical |
| `storage` | `minio` | **MET** | `test_uploaded_thumbnail_lands_in_the_store_under_the_key_scheme`, `test_wildcard_application_file_lands_in_the_store`, both critical |

## Grading layers

| Measure | Value |
|---|---|
| Workflows | 16 (solo_founder band 10-16) |
| Browser substeps | 34 |
| Pytest substeps | 29, each carrying a category and a derived weight |
| Critical substeps | 19 |
| Category mix | `security` 8, `data_integrity` 6, `core_outcome` 6, `presentation` 5, `business_rule` 3, `validation` 1 |
| Pytest module | `tests/test_output.py`, 29 functions |
| Judged rubric | 13 criteria, 11 positive and 2 negative, `|score|` matched to `importance` |
| Checklist | 503 items, 494 cited by a grader |
| Companion carriage | 16/16 colours as words, 167/167 topics, 303/303 enumerated items |

## Kit gate log

32 gates: 27 PASS, 1 WARN, 1 NOT-APPLICABLE, 3 FAIL.

| Gate | Tool | Exit | Verdict | Evidence |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | **PASS** | clean |
| `G1/G12` | `layout_lint.py` | 0 | **PASS** | clean |
| `G46` | `structure_lint.py` | 1 | **FAIL** | clean |
| `G50` | `docker_lint.py` | 0 | **PASS** | clean |
| `G55` | `runtime_deps_lint.py` | 0 | **PASS** | clean |
| `G63` | `secret_lint.py` | 0 | **PASS** | clean |
| `G48` | `truth_lint.py` | 0 | **PASS** | clean |
| `G51` | `source_lint.py` | 0 | **PASS** | clean |
| `G52` | `rubric_context_lint.py` | 0 | **PASS** | clean |
| `G54` | `comment_lint.py` | 0 | **PASS** | clean |
| `G17` | `secret_hygiene_lint.py` | 0 | **PASS** | clean |
| `G11` | `leak_scan.py` | 0 | **PASS** | clean |
| `G33` | `window_lint.py` | 0 | **PASS** | clean |
| `G4/G5` | `contract_lint.py` | 0 | **PASS** | clean |
| `G43` | `prescription_lint.py` | 0 | **PASS** | clean |
| `G44` | `disclosure_lint.py` | 0 | **PASS** | clean |
| `G10` | `no_sdk_lint.py` | 0 | **PASS** | clean |
| `G31` | `determinism_lint.py` | 0 | **PASS** | clean |
| `G14` | `reward_path_lint.py` | 0 | **PASS** | clean |
| `G27/G30` | `rubric_lint.py` | 0 | **PASS** | clean |
| `G41` | `flag_lint.py` | 0 | **PASS** | clean |
| `G56/G57/G58` | `if_lint.py` | 0 | **PASS** | clean |
| `G59/G60` | `codequality_lint.py` | 2 | **?** | clean |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | **PASS** | clean |
| `G6` | `fixture_lint.py` | 0 | **PASS** | clean |
| `G24` | `coverage_map.py` | 1 | **FAIL** | clean |
| `G37` | `checklist_qc.py` | 0 | **PASS** | clean |
| `G39` | `rubric_align_lint.py` | 0 | **PASS** | clean |
| `G28/G29` | `channel_lint.py` | 0 | **PASS** | clean |
| `G40` | `prompt_receipt_lint.py` | 0 | **WARN** | clean |
| `G0/INV5` | `vendor_check.py` | 0 | **PASS** | clean |
| `G47` | `output_qc.py` | 1 | **FAIL** | clean |

## Blocking findings

### G46 - CON-1 placement, DECLARED DEVIATION

Half of this finding is closed: the bundle sits flat, one level under the output root
`Output/16sept-phantom`, which is what the second half of the rule asked for. What remains is the
first half.
`structure_lint.py` resolves the generation kit as `tools/../..`, which is the whole checkout, so
it refuses any bundle under `GreenField-GenKit2/Output/`. CON-1's own diagram draws `<root>/`
holding `<generation-kit>/` and `Output/` as siblings, which is exactly this layout, and every
other bundle in this tree sits there too. The kit disagrees with itself; the operator specified
this location twice, and the finding is recorded rather than worked around.

### G24 - nine unobservable obligations, ESCALATED (OPEN-DECISIONS D-H)

494 of 503 checklist items are cited. The nine that are not -- `C-DC-09`, `C-DC-10` (the two
reserved directories), `C-TR-01`, `C-TR-02` (the named frontend and server frameworks) and
`C-TR-18` to `C-TR-22` (the five logging rules) -- are structurally uncitable by the three reward
channels: two are filesystem facts with no HTTP surface, two would require reading source, which
INV6 bars from the reward path, and five describe stdout.

**The `code_quality` dimension added in `1b99060` was tried and does not close this.**
`tools/_vocab.py` now lists `code_quality`, `rubric_lint.check_source_battery` names it as one of
the three a task may author, and CON-2 says the code-quality criteria live in `tests/rubric.json`
under `evaluation_target: "source"`. But `tests/rubric.json` is GENERATED, G48 re-runs the
generator and compares bytes, and `recompute.py` at both pins still validates
`judged_criteria.dimension` against the seven product dimensions only. Authored and re-run, it
exits:

```
recompute: judged criterion 'J14' has dimension 'code_quality', which the runtime judge
would drop (legal: instruction_following, functionality, ux_flow, ui_visual, motion,
accessibility, responsiveness)
```

So three separate places now describe a source channel that the only legal author of the file
refuses to write. One line -- `JUDGED_DIMENSIONS` in the vendored generator -- closes it, and
with it these nine items and G24.

### G47 - cascade

`output_qc.py` reports no independent defect. Its traceability finding names core asks `A58`,
`A62` and `A168`, the rollup of the same nine items.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION   -- with three declared red gates
```

**NOT ADMISSIBLE.** `solution/` carries no reference application (D20). The bundle becomes
admissible only when the app is generated from `solution/checklist.md` and `harbor run -a oracle`
returns `1.0` twice.
