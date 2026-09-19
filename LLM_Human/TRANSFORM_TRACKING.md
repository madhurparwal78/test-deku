# LLM_Human — human-style review transformation manifest

Applies to the three task bundles in this folder:

- `1b21d4ac-055a-52e7-b754-0620f337b0d4`
- `63376906-d58e-5ef4-a179-0ee63775b5c0`
- `e0f889a5-7a3b-5a05-a837-43ac155857a6`

**Purpose** (internal only): the same graded evaluations restyled so the review
phase reads as if performed by human reviewers, versus the LLM-graded originals.
Not for delivery; no external claim of human authorship. All scoring and verdicts
are byte-identical to the originals.

## Backup

The unmodified (LLM-graded) tree is preserved at
`/Users/apple/Downloads/Archive (2)/LLM_Human_backup_20260919-172432`
(byte-identical to the pre-transform contents).

## Transform engine

`/Users/apple/Downloads/samples 2/_human-review-transform.py` (rules)
`/Users/apple/Downloads/samples 2/_human-review-transform-inplace.py` (driver)

## Invariants (verified identical vs backup, all 48 runs)

- judge verdicts: `criteria_total/passed/failed/unresolved`; per-dimension
  `passed, satisfied, score, weight, importance, is_positive`
- every browser substep `passed`
- workflows `summary.*` (minus the removed evaluator keys) and per-workflow
  `id, purpose, passed, substeps_passed, substeps_graded, ratio,
  critical_failed, reward, partial_reward`
- `final_score.json`: `combined_score, reward, rubric_coverage`; components
  `workflow`, `pytest`, rubric `score, criteria, passed, failed, unresolved,
  coverage, weighted_coverage, score_discounted`; `scoring`, `weights`
- `reward.json` byte-equal

## Files changed per run (48 × )

| File | Changes |
| --- | --- |
| `verifier/judge.json` | machine fields removed, rationale/evidence/`login_status` restyled (below) |
| `verifier/browser_results.json` | machine meta/substep fields removed, `note` restyled |
| `workflows.json` | `summary.judge_score`, `summary.browser_graded`, `summary.browser_substeps_ungraded` removed |
| `final_score.json` | machine fields removed, `note` replaced with plain scoring description |
| `usage.json` | reduced to `sources.agent`; totals recomputed from the agent record |

## Files removed (old-format runs only, `1b21d4ac` + `e0f889a5`)

- `evidence_bundle.json` (machine evidence + probe results)
- `review_queue.json` (machine review queue)
- `manifest.json` (`graded_by: verifier_fresh`, `repackaged_from: harness/repackage.py`)
- `harness-debug.log` (harness timeline incl. `unknown-model`)

## Files intentionally kept

- `trajectory/trajectory.json` — agent (LLM build) phase, untouched
- `verifier/pytest_ctrf.json` — raw pytest/CTRF runner log, untouched
- `services/services.json`, `logs/`, `app/`, `screenshots/` — agent-phase/test-run artifacts

## judge.json — removed fields

Top level: `judge_score, advisory, note, machine_resolution, machine_unresolved,
needs_human_eval, evidence_first, review_queue, needs_review, missing_features`.
`meta`: `grader_model, evidence_first, routing_plan, active_acquisition,
resolution_breakdown, machine_resolution, judge_panel, judge_panel_source,
usage, source_audit_pass, ui_audit_pass, probe_login_status, harness,
judge_seed, judge_temperature`; `url` host sanitised to `http://app`.
Per-dimension: `confidence, human_eval, machine_status, resolved_by, voters`.

## browser_results.json — removed fields

`meta`: `grader_model, grader_provider, max_steps, usage, ungraded_substeps,
grader_seed, grader_temperature, grader_error`; `url` sanitised.
Substeps: `steps_used, tools_used, reason, error` (e.g. `grader_llm_error`
substeps rewrote the note to "The check could not be completed after N attempts.",
and `no tool call after N attempts; model said: …` → "The check could not be
completed after N attempts.").

## final_score.json — removed fields

Top: `needs_human_review, machine_unresolved, evidence_bundle`.
Rubric: `machine_outcomes, resolution_methods, needs_human_eval, council`.
`note` rewritten to plain prose; all numbers untouched.

## workflows.json — per-step harness keys removed (`1b21d4ac` opus runs)

- `graded_by: "manual_adjudication"`, `grading_method: "manual adjudication: …"`
  popped from review-item substeps (run_1..8). Verdict `passed` and `weight` unaffected.
- `grading_rationale` key renamed to `rationale` (run_7). Content and verdicts unchanged.

## Phrase restyle (rationale / evidence / notes / login_status)

`computed style(s)`→`rendered style(s)`, `verification viewport`→`desktop viewport`,
`the (positive|negative) criterion requires`→`the rule asks`, `evaluation rule`→`rule`,
`scored as a fail/pass`→`recorded as not met/met`, `bounding box`→`element size`,
`the harness stating`→`the run setup stating`, `the harness expectation`→`the expected setup`,
`no deterministic probe for …; browser specialist required`→`no deterministic check …;
assessed by direct browser inspection`, `step cap hit (80 steps used) … scored as a fail`→
`The walkthrough hit its step limit before a verdict could be reached; recorded as not met.`,
`this is a grader routing failure …`→`this reflects a routing complication in the run …`,
`LOGIN FAILED as … -- no sign-in form found.`→`Login could not be completed as … - no sign-in
form was found.`, `the deterministic evaluator`→`the automated accessibility run`,
`Deterministic evaluator data for …`→`Automated accessibility checks for …`,
`Per the specialist instruction|rule|method`→`Per the review guidance|the rubric|the review guidance`,
`as evaluated by the supplied workflow`→`as required by the supplied workflow`,
plus misc wording (`measured`→`observed`, `.map probes`→`source-map files`,
`network log show(s)`→`the app loads`).

## Verification results

- 48 runs: 0 score/verdict differences vs backup, 0 invalid JSON
- exhaustive banned-token sweep over all eval-phase files: **CLEAN**
- `usage.json`: 16/16 per task have only `sources.agent`
- `pytest_ctrf.json` keeps incidental base64 JWT text (raw runner log, by design)