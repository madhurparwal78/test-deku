# Build report

**Exit state: `MECHANICALLY-GREEN, NO-SOLUTION`.** Not admissible. Nothing counts toward
corpus targets until the app is built downstream from `solution/checklist.md` and
`harbor run -a oracle` returns `1.0` twice.

## Identity

| | |
|---|---|
| Task code | `S_saasm_cont_market-charting-showcase-vb_20260916_053556` |
| Task id | `deku/market-charting-showcase-vb` |
| uuid_v5 | `c46e9c86-9e80-5be9-b356-9dc56aa79f2a` |
| Cell | solo_founder / saas-micro-tools / content-publishing |
| Archetype | `market-charting-showcase` |
| Service profile | `P4-db-storage` |
| Providers | db to `postgres`, storage to `minio` |
| Variant | `b`, on axes `critical_depth` and `spec_sections` |
| Language | `typescript` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Vendored grader | 0.22.0 |
| Target schema | 1.4 |

The Task Order named `saas-productivity`, which is not a taxonomy domain. It was mapped to
`saas-micro-tools`, the only solo_founder domain covering a charting and analysis tool sold by
public signup. The companion document records the same substitution in its own section 22.

## Derived-design draws

All drawn by SHA-256 over the archetype, recorded as `draw:` lines in
`_spec/<code>/00-decisions.md` and read by G49.

| Axis | Value |
|---|---|
| render_model | `ssr-islands` |
| backend | `Hono` |
| frontend | `SolidStart` |
| nav | `top-nav` |
| work_surface | `table-first` |
| create_flow | `modal` |
| feedback | `full-page-confirmation` |
| design_direction | `companion` (the draw landed on `playful-consumer`; reference/L L.6.1 hands the axis to the companion) |
| launch_surface | `alt_text,cookie_choice,mobile_viewport,no_frontend_secrets,single_cta` |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Open signup and sign in | INCLUDED | Core features, Auth | solo_founder opens signup; the seeded accounts grade it |
| Live streaming market summary | INCLUDED | Core features rules 3 to 5 | the companion's dominant technical surface |
| Idea drafting with a stored snapshot | INCLUDED | Core features rules 6 to 7 | the pattern's storage slot |
| Draft protection | INCLUDED | Core features rule 8 | the pattern's critical focus |
| Idempotent publish under contention | INCLUDED | Core features rule 9 | variant `b` critical depth |
| Ideas listing and boosting | INCLUDED | Core features rules 10 to 11 | the companion's ideas river |
| Partner futures landing | INCLUDED | Core features rules 12 to 14 | the companion's second real route |
| Platform capability page | INCLUDED | Core features rule 15 | carries the companion's six capabilities |
| Cookie choice | INCLUDED | Core features rule 16 | drawn launch-surface token |
| Not-found chrome | INCLUDED | Core features rule 17 | the companion's art-directed 404 |
| Alt text, narrow viewport, one primary action | INCLUDED | UI/UX notes | drawn launch-surface tokens |
| No secret in the browser | INCLUDED | Technical requirements | drawn launch-surface token |
| In-browser script editor for `Beamscript` | DROPPED | Constraints | the capability lives behind the application host; the storefront links to it |
| Backtest runner | DROPPED | Constraints | same boundary |
| Chart drawing tools, comment threads, follower graph | DROPPED | Constraints | out of the captured surface; would add ungraded product |
| Section 19 build order | DROPPED | recorded in the carry table | a work order, not a specification; `## Build plan` is not emitted above the baseline lever set |

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| db | `postgres` | MET | `test_persisted_account_row_survives_a_reload` reads the accounts row back through the backend adapter; `test_form_validation_refuses_invalid_input` counts rows across two refused submissions |
| storage | `minio` | MET | `test_snapshot_bytes_are_stored_in_the_bucket_at_their_key` heads the object at its key; `test_snapshot_upload_across_accounts_is_denied` compares the bucket listing across a denied upload |

## Grading surface

| | |
|---|---|
| Workflows | 16 (band 10 to 16) |
| Browser substeps | 23 |
| pytest substeps | 26 |
| Critical substeps | 15 |
| Non-happy-path ids | `invalid_signup_is_refused_with_the_field_named`, `draft_idea_is_denied_to_every_other_account`, `publish_across_accounts_is_denied`, `anonymous_boost_is_denied`, `reader_cannot_reach_the_author_studio` |
| Test module | one, `tests/test_output.py`, 26 top-level test functions |
| Sections covered | core features, data integrity, authorization, edge cases, storage, front end |
| Checklist items | 172 across ten section codes, every one cited |
| Rubric criteria | 19: 16 positive, 3 negative |

Six of the twenty-six tests take the `page` fixture and drive a real browser, which is what
lets them carry the `ui`-tagged obligations channel_lint permits a page-driving test to claim.

### Rubric dimension shares against the frozen weights

| Dimension | Points | Share | Target |
|---|---|---|---|
| instruction_following | 18 / 60 | 0.30 | 0.30 |
| functionality | 15 / 60 | 0.25 | 0.25 |
| ux_flow | 9 / 60 | 0.15 | 0.15 |
| ui_visual | 9 / 60 | 0.15 | 0.15 |
| motion | 3 / 60 | 0.05 | 0.05 |
| accessibility | 3 / 60 | 0.05 | 0.05 |
| responsiveness | 3 / 60 | 0.05 | 0.05 |

## Literals ledger

109 entries in `_handoff/<code>.literals-ledger.json`, bijective against the brief and the
graders (G6 PASS).

| Class | Count |
|---|---|
| seed_record | 64 |
| endpoint | 13 |
| status | 11 |
| env_var | 8 |
| route | 4 |
| account | 3 |
| number | 3 |
| scheme | 2 |
| credential | 1 |

One entry is `verifier_only`: `DB_ADMIN_URL`, carried by `task.toml` `[verifier].env` alone.

## Spec folder

Written to `Output/16-sep-2026/_spec/<code>/`, never inside the bundle.

| Doc | Fed |
|---|---|
| `00-decisions.md` | the audit trail, the draws, the companion carry table, the G51 waivers |
| `01-PRD.md` | Overview, Core features, Constraints |
| `02-TRD.md` | Technical requirements |
| `03-app-flow.md` | User flow |
| `04-uiux-brief.md` | UI/UX notes, Front-end specification |
| `05-backend-schema.md` | Data model, User roles |
| `06-implementation-plan.md` | authoring reference only; `## Build plan` is not emitted |

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| core_features | 8,376 | 2,400 | past-slice |
| user_flow | 3,478 | 1,900 | past-slice |
| ui_ux_notes | 7,731 | 1,700 | past-slice |
| constraints | 1,375 | 800 | over-reference |
| user_roles | 1,534 | 1,000 | over-reference |
| overview | 1,498 | 700 | over-reference |
| joined | 23,992 | 8,800 | past-slice |

Reported, not failed. The brief has no length limit and `generate_instruction.md` forbids
cutting a real rule to fit the judge's window; `judge_score` never touches reward. The
companion is 1,419 lines and G51 requires every colour, topic and enumerated item to reach
the brief, which is where the length comes from.

## Companion carriage (G51)

| Measure | Result |
|---|---|
| Source colours described by family and tone | 36 / 36 |
| Topics carried | 84 / 84 |
| Enumerated items carried | 219 / 219 |
| Hex values anywhere in the brief | 0 |

Six units are waived on the record, each the document talking about itself rather than about
the product: the normative-versus-informational register note, every `Observed implementation`
label, the evidence-gap section, the acceptance checklist whose every line is carried as a
product rule, and the two gradient rows whose notation A5 forbids the brief to carry. The
reasons are in `_spec/<code>/00-decisions.md`.

## Kit gate log

Rendered from `_handoff/<code>.gates.jsonl`. Every row carries the tool's exit code, its
verdict string and the SHA-256 of the bytes it examined. No verdict here was transcribed.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS |
| `G1/G12` | `layout_lint.py` | 0 | PASS |
| `G46` | `structure_lint.py` | 0 | PASS |
| `G50` | `docker_lint.py` | 0 | PASS |
| `G55` | `runtime_deps_lint.py` | 0 | PASS |
| `G63` | `secret_lint.py` | 0 | PASS |
| `G48` | `truth_lint.py` | 0 | PASS |
| `G51` | `source_lint.py` | 0 | PASS |
| `G52` | `rubric_context_lint.py` | 0 | PASS |
| `G54` | `comment_lint.py` | 0 | PASS |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS |
| `G11` | `leak_scan.py` | 0 | PASS |
| `G33` | `window_lint.py` | 0 | PASS |
| `G4/G5` | `contract_lint.py` | 0 | PASS |
| `G43` | `prescription_lint.py` | 0 | PASS |
| `G44` | `disclosure_lint.py` | 0 | PASS |
| `G10` | `no_sdk_lint.py` | 0 | PASS |
| `G31` | `determinism_lint.py` | 0 | PASS |
| `G14` | `reward_path_lint.py` | 0 | PASS |
| `G27/G30` | `rubric_lint.py` | 0 | PASS |
| `G41` | `flag_lint.py` | 0 | PASS |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS |
| `G59/G60` | `codequality_lint.py` | 2 | NOT-APPLICABLE |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS |
| `G6` | `fixture_lint.py` | 0 | PASS |
| `G24` | `coverage_map.py` | 0 | PASS |
| `G37` | `checklist_qc.py` | 0 | PASS |
| `G39` | `rubric_align_lint.py` | 0 | PASS |
| `G28/G29` | `channel_lint.py` | 0 | PASS |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN |
| `G0/INV5` | `vendor_check.py` | 0 | PASS |
| `G47` | `output_qc.py` | 0 | PASS |

`G38` (`kit_selftest.py`) is per kit revision, not per task, and was green over 32 checks
before this handoff was written.

Three advisory WARNs stand on a green sweep, and each is information rather than a defect:
the brief carries eleven launch-surface bank obligations where five were drawn, because the
companion already stated six of them; `## Core features` runs past the judge's slice, as the
window table above records; and `aesthetic` notes that `tests/rubric.json` is read at runtime
as of grader 0.21.0. `G40` exits WARN because every prompt receipt records `verifier: self`.

## Handoff gates, undecided

The seven gates the kit cannot run are listed with their commands and expected verdicts in
`_handoff/<code>.handoff.md`. None has been attempted: no reference code exists, and nothing
in this bundle has been compiled or run.

## Blocking findings

None. No spec gap and no harness gap prevented a required test. `[delivery.images]` is absent
by decision rather than by omission; the reason and the packaging-time remedy are in the
handoff contract.

## Applied after the build: kit changes of 2026-09-16

The kit moved under this bundle after the first green sweep. Four commits were applied to
the bundle rather than rebuilding it, and the sweep is green over the result.

| Kit commit | What changed here |
|---|---|
| `da24d3b` rename the pytest module | `tests/test_pytest.py` became `tests/test_output.py`; the generated compiled-rubric file became `solution/trinity/test_ans.py`; all 26 substep ids moved to the `test_output.py::` prefix; `tests/Dockerfile` COPYs the new name |
| `11eaf7b` separate verifier mode | `[verifier].environment_mode` flipped from `shared` to `separate`. The grader now ships its own image from `tests/Dockerfile` on `deku-verifier-base`. G55 RD-1 skips under separate; the agent image keeps its grader packages, which costs size and breaks nothing, and keeps `postgresql-client` because the healthcheck still runs from the agent container |
| `78e5ba6` stripped vendored `test.sh` | `tests/test.sh` re-vendored from the re-pinned grader-0.22.0; `vendor_check` is byte-identical to the new MANIFEST |
| `806eb0a` restore `solution/USER_README.md` | `solution/trinity/recompute.py` re-vendored at `truth-generator-7`; the generator now writes a fifth artifact, `solution/USER_README.md`, carrying the seeded logins and the canary. G12 now checks the canary in both generated copies |

Prompt pins were re-minted in three of those commits, so every receipt token in
`_handoff/<code>.receipts.json` was re-minted too. `qc_toml` VERIF-001 now requires
`separate` and passes on the flipped value; `pytest_generator` now names the module
`test_output.py` and passes on the rename.

## Budget

`turns_expected = 170`, `tokens_expected = 7000000`: the hard band. The task carries ten
must-have features rather than the bare-order three to six, two backing services, a browser
half whose visual specification runs to a full unbudgeted section, and a critical focus that
has to hold under contention. `difficulty` stays the empty calibration placeholder; the
Calibration Engineer writes it, never the author.
