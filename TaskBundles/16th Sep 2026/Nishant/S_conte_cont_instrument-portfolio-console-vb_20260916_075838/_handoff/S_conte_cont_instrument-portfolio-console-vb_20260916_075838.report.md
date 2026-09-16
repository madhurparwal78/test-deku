# Build report: S_conte_cont_instrument-portfolio-console-vb_20260916_075838

Rendered from `_handoff/S_conte_cont_instrument-portfolio-console-vb_20260916_075838.gates.jsonl`. No verdict in this file is written by hand.

| | |
|---|---|
| Task code | `S_conte_cont_instrument-portfolio-console-vb_20260916_075838` |
| Task id | `deku/instrument-portfolio-console-vb` |
| Cell | solo_founder / content-publishing / content-publishing |
| Archetype | `instrument-portfolio-console`, variant `b` |
| Service profile | `P4-db-storage` |
| Providers | `postgres` (db), `minio` (storage) |
| Variant axes | `critical_depth`, `spec_sections` |
| Language | python |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Grader pin | `0.22.0` |
| Target schema | `1.4` |
| Verifier mode | `separate` |
| Exit state | **MECHANICALLY-GREEN-WITH-ONE-RED, NO-SOLUTION** |

## Input

Task Order: solo_founder / content-publishing / content-publishing /
instrument-portfolio-console. Companion document supplied:
`/Users/apple/Downloads/futamura_prd.md`, 6,290 lines, 44 sections, 301 headings,
1,687 enumerated items, 21 distinct colour values.

The Task Order arrived with `domain: portfolio-agency`, which is not one of the 36
domains in reference/A. Normalised to `content-publishing` and recorded as decision D1;
the tasker owns the cell, so this is reported rather than silently absorbed.

Because a companion was supplied, the variant is `b` per `companion_variant`, and the
variant-`a` concurrency reminder is deleted from the brief.

## Derived design values

| Axis | Value | Source |
|---|---|---|
| design_direction | `companion` | reference/L L.6.1; the bank draw was `dense-ops-console` and does not govern |
| render_model | `spa-json-api` | companion override of the `mpa-progressive` draw, decision D5 |
| backend | `FastAPI` | re-drawn inside the spa bank at offset 8 |
| frontend | `React + Vite` | re-drawn inside the spa bank at offset 16 |
| nav | `top-nav` | draw at offset 24 |
| work_surface | `table-first` | draw at offset 32; the console's own scene governs the public side |
| create_flow | `dedicated-route` | draw at offset 40, realised as `/studio/work/new` |
| feedback | `inline-banner` | draw at offset 48, realised as the status banner |
| launch_surface | `colour_contrast, page_view_log, security_headers, social_preview, spam_protection` | reference/O O.3 draw |

`flag_lint` reports the brief carries **10** bank obligations, the drawn five plus five
the companion already stated. Above the floor, which is the correct outcome.

## Feature resolution

| Feature | Verdict | Where | Reason |
|---|---|---|---|
| The public console, one read, five destinations | INCLUDED | Core features 1-7 | the companion's whole subject |
| The parallel structure | INCLUDED | Core features 6 | the only channel that can observe a drawn interface |
| Accounts and sessions | INCLUDED | Core features 8-11 | the extension the Task Order asks for |
| The work entry dossier | INCLUDED | Core features 12-16 | the primary workflow's subject |
| Publish, unpublish, the preview object | INCLUDED | Core features 17-22 | the pattern's critical focus |
| The shelf | INCLUDED | Core features 23-27 | the Task Order's "orders the shelf" |
| The contact form and the inbox | INCLUDED | Core features 28-33 | the Task Order's "sends a message" |
| The failure surface | INCLUDED | Core features 34-36 | companion section 16, and the `custom_404` shape |
| The page-view log | INCLUDED | Core features 37 | drawn launch surface `page_view_log` |
| Loading and first entry | INCLUDED | Core features 38-40 | companion section 10 |
| The voice of every string | INCLUDED | Core features 41 | companion section 41.12 |
| The recognition editor | DROPPED | Constraints | seeded read-only content instead; every added feature owes a grader and this one would have had none inside the budget |
| The audio layer | DROPPED | Constraints | nine generated beds and eighteen cues, no channel can observe them |
| Real-time, export, i18n, offline hold, migration tooling | DROPPED | Constraints | recorded as scope-outs so the agent is told not to build them |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | 5 tests assert stored rows through the backend adapter |
| `storage` | `minio` | MET | `test_published_entry_preview_object_exists_in_the_bucket` lists the bucket and matches the stored key; `test_draft_entry_preview_object_is_denied_to_an_anonymous_caller` proves the draft object is refused |

## Grading surface

| | |
|---|---|
| Workflows | 16 (band 10-16) |
| Browser substeps | 18 |
| Pytest substeps | 37 |
| Critical substeps | 23 |
| Non-happy-path ids | 10: `draft_entry_detail_cannot_be_read_by_a_visitor`, `draft_preview_object_is_denied_to_an_unauthenticated_caller`, `editor_owner_only_writes_are_forbidden_at_the_api`, `editor_inbox_and_log_access_is_denied`, `unauthenticated_studio_request_is_denied`, `invalid_form_input_is_refused_inline`, `bot_submissions_are_refused_by_the_decoy_and_the_limit`, `concurrent_entry_writes_accept_at_most_one`, `duplicate_position_reorder_is_refused_and_positions_survive`, `sign_in_failures_reach_the_lockout_limit` |
| Pytest module | one, `tests/test_output.py`, 37 tests |
| Sections covered | core features, data integrity, authorization, edge cases |
| Rubric criteria | 18 judged (16 positive, 2 negative), positive total 46 |
| Compiled rubric items | 35, all `mode: compiled` against committed graders |
| Checklist items | 335 across ten section codes |
| Coverage | G24 two-way holds; G39 reports 64 of 64 judgment obligations graded |

### Rubric dimension budget

| Dimension | Positive score | Share | Target |
|---|---|---|---|
| `instruction_following` | 13 | 0.28 | 0.30 |
| `functionality` | 11 | 0.24 | 0.25 |
| `ux_flow` | 6 | 0.13 | 0.15 |
| `ui_visual` | 6 | 0.13 | 0.15 |
| `motion` | 4 | 0.09 | 0.05 |
| `accessibility` | 4 | 0.09 | 0.05 |
| `responsiveness` | 2 | 0.04 | 0.05 |

## Literals Ledger

| Class | Values |
|---|---|
| `account` | 2 |
| `copy` | 57 |
| `credential` | 1 |
| `design_token` | 1 |
| `env_var` | 8 |
| `number` | 15 |
| `route` | 27 |
| `seed_record` | 12 |
| `status` | 29 |
| `table` | 10 |

Total 162 pinned values. Every one is carried by at least one of
`instruction.md`, `tests/conftest.py`, `tests/test_output.py`, `task.toml`, and G6
holds the bijection in both directions.

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Core features | 16,154 | 2,400 | past-slice |
| User flow | 5,221 | 1,900 | past-slice |
| UI/UX notes | 8,148 | 1,700 | past-slice |
| Constraints | 1,901 | 800 | over-reference |
| User roles | 2,617 | 1,000 | past-slice |
| Overview | 1,699 | 700 | over-reference |
| Joined | 35,740 | 8,800 | past-slice |

**This is a measurement, not a defect, and it was a deliberate choice.** The brief has
no length limit and `window_lint` fails nothing on length. What the numbers say is that
`run_rubric.py` will slice `## Core features` at 2,500 characters, so the judge reads
roughly the first quarter of it. The judged criteria are self-contained and carry their
own `evaluation_rule` (reference/I I.8), and `judge_score` never touches reward, so the
cost is a diagnostic number rather than anything that counts. Cutting a real rule to fit
the window would have traded reward-driving completeness for that number. The visual
specification was moved into the unbudgeted `## Front-end specification` for exactly
this reason, which is what reference/G G.3 recommends.

## Companion carriage (G51)

| Measure | Result |
|---|---|
| Colours described by family and tone | 21 of 21 |
| Topics carried into the brief | 290 of 301 |
| Enumerated items carried | 1,574 of 1,687 |
| Waivers declared | 96 |

Every waiver is on the record in `S_conte_cont_instrument-portfolio-console-vb_20260916_075838.g51-waivers.txt`. They fall into four groups, and
none of them is a dropped product requirement:

1. **The audio layer** (11 waivers). Cut with the asset budget and recorded in
   `## Constraints`, so the agent is told the product has none.
2. **Exact motion and scene numbers** (easing curves, durations, radii, offsets). The
   settled number rule forbids a millisecond or a `cubic-bezier` anywhere in the brief;
   the moments are carried as words instead.
3. **The companion's own evidence notes** (what the capture found, what could not be
   measured, the reference manifest, the deliberate-departures table). These describe
   how the companion was written, not what the product must do.
4. **The companion's test plan and acceptance checklist.** INV10 forbids the brief from
   stating the exam, so carrying these would have failed G44 by construction.

## Kit gate log

Rendered from the receipts. Each row carries the SHA-256 of every input it read.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS |
| `G1/G12` | `layout_lint.py` | 0 | PASS |
| `G46` | `structure_lint.py` | 1 | FAIL |
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
| `G59/G60` | `codequality_lint.py` | 2 | ? |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS |
| `G6` | `fixture_lint.py` | 0 | PASS |
| `G24` | `coverage_map.py` | 0 | PASS |
| `G37` | `checklist_qc.py` | 0 | PASS |
| `G39` | `rubric_align_lint.py` | 0 | PASS |
| `G28/G29` | `channel_lint.py` | 0 | PASS |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN |
| `G0/INV5` | `vendor_check.py` | 0 | PASS |
| `G47` | `output_qc.py` | 1 | FAIL |

`G59/G60` exit 2 is NOT-APPLICABLE: the bundle carries no code-quality rubric.
`G40` is WARN and says why: every prompt gate is SELF-ATTESTED, because this was a
single-agent run and the kit's rule is owner != verifier. The verdicts are recorded,
never independent.

## Blocking findings

**G46 (`structure_lint.py`) is RED, and it is a placement finding rather than a content
finding.**

```
CON-1 placement: bundle is INSIDE the generation kit
('/Users/apple/Downloads/GreenField-GenKit2').
```

CON-1 requires `Output/` to be a **sibling of the generation kit**, and
`structure_lint.py` resolves the kit root as the parent of `deku-green-field`, which is
the repository root. The output root was set to
`/Users/apple/Downloads/GreenField-GenKit2/Output/16sept-futamura` because that is where
this run was asked to write, and every bundle already in this repository's `Output/`
tree fails the same check for the same reason. Verified against
`Output/16sept-rive/S_saasm_cont_interactive-animation-studio_20260916_061700`, which
reports both CON-1 findings identically.

Nothing inside the bundle causes it and nothing inside the bundle can fix it. The
resolution is an operator one: move the corpus to `/Users/apple/Downloads/Output/`, or
amend `structure_lint.py`'s kit-root resolution if `deku-green-field` rather than its
parent is meant to be the kit tree. **G47 is red only because G46 is red** and says so.

## Not proven here

| Battery | Gates |
|---|---|
| Handoff-owned (needs Docker or the harness) | G13, G15, G18, G19, G20, G21, G25 |
| Adversarial LLM, self-attested this run | G23, G34, G35, G36, G37b, G53 |

## Budget estimate

`turns_expected` 170, `tokens_expected` 6,000,000. Reasoning: ten must-have features
against a companion-backed brief at variant `b`, with a drawn-scene public console that
has to hold one surface across every destination change, a parallel accessibility
structure that duplicates every string the scene draws, a generated preview image
written to an object store, and a keyboard-normative reorder. That is well above the
five-feature baseline, and the two numbers were raised with the feature count rather
than left at the default.

## Exit state

```
MECHANICALLY-GREEN-WITH-ONE-RED, NO-SOLUTION
```

**NOT ADMISSIBLE.** Thirty of thirty-two battery gates are PASS, one is WARN by design,
and one is the placement FAIL above. The bundle carries no reference application: it is
built downstream from `solution/checklist.md`, and nothing counts toward corpus targets
until `harbor run -a oracle` returns `1.0` twice.
