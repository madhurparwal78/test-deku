# Handoff: S_local_book_broadcast-reel-index_20260916_072048

QL: Abhishek Shaw, abhishek.shaw@ethara.ai
Contributor: Atharv Mahalwar, atharv.mahalwar@ethara.ai

## State

Built, not QC'd. The requester asked for the task to be created without the QC
layer, so the prompt-driven QC batteries were not run. Everything mechanical that
does not depend on them is green.

## Gates

30 of 32 green. Receipts: `<code>.gates.jsonl`.

### Red, and why

**G40 `prompt_receipt_lint` -- no receipt file.** G40 asks whether the prompts that
own the hard QC gates were actually read over these bytes. Those prompts are
`QC_instruction.md` (G34, 24 checks), `QC_spec.md` (G34, 15), `qc_docker.md` (G35,
105), `qc_toml.md` (G36, 120), `qc_rubric.md` (G53, 16), `qc_solution_checklist.md`
(G37) and `task_code_verifier.md` (G3, 12). None was run, because running them is
the QC pass that was explicitly excluded from this request. No receipt was written,
because a receipt for a battery nobody executed is a false attestation and would
make every downstream gate read green on nothing.

**G47 `output_qc` -- red because G40 is red.** G47 refuses any output carrying a red
gate. It clears the moment G40 does.

To close both: run the seven prompts above against this bundle, write the receipts
to `_handoff/<code>.receipts.json` with the tokens from
`python tools/prompt_receipt_lint.py tokens --task-code <code>`, then re-run
`tools/revalidate.py`.

### Warnings worth a reader's eye

- `## Core features` is 5,780 characters. `run_rubric.py` slices each graded section
  at 2,500, so the tail of that section reaches the building agent in full but not
  the judge. The sections were ordered, and the seed table relocated to
  `## Data model`, so that everything a criterion depends on falls inside the window;
  a later edit that grows Core features can silently push material out of it again.
- `launch_surface` drew 5 obligations; the brief carries 9. The extra four
  (`colour_contrast`, `cookie_choice`, `form_validation`, `no_frontend_secrets`) are
  stated in the brief but not drawn, which is additive rather than a conflict.
  `cookie_choice` in particular is stated only as an exclusion: the Constraints
  section forbids a cookie consent surface.

## Re-running the sweep

G51 needs the companion PRD and its waiver list:

```
python tools/revalidate.py <bundle> $(while read w; do printf -- '--waive %q ' "$w"; done < <bundle>/_handoff/<code>.g51-waivers.txt)
```

The source path itself is recorded in `<code>.sources.json`, so `--source` is not
needed; `revalidate.py` reads it.

## What a reviewer should check by hand

1. **The two Task Order substitutions.** `portfolio-agency -> local-services` and
   `media-gallery -> booking-scheduling`. The second drives the whole grader layer.
   If a reviewer disagrees with it, the rubric dimension shares and the workflow
   categories both move.
2. **The 177 G51 waivers.** Grouped and justified in the report. Three of them waive
   topics that ARE carried under different wording (`22.4 Concurrency`,
   `22.5 Validation and hardening`, `reduced-motion honoured everywhere`); the rest
   waive material the brief deliberately scopes out. A waiver is a judgement, and
   these are the ones most worth disagreeing with.
3. **The 18 unobservable citations.** Listed in `<code>.unobservable.txt`. Each is
   cited so G24 can see it, and flagged so the traceability matrix does not claim a
   channel observes it. If any of them can in fact be observed, it should be graded
   instead of flagged.
4. **The seeded corpus.** Seventeen productions, eleven of them featured, with the
   home ordering stored independently of the index ordering. A build that derives one
   from the other is wrong, and `test_home_ordering_is_not_derived_from_index_ordering`
   is the test that says so.

## Not proven here

Battery 3, handoff-owned: G13, G15, G18, G19, G20, G21, G25.
Prose and adversarial: G23, G34, G35, G36, G37b.

A mechanically-green sweep is not admissibility. That needs the reference app and
`harbor run -a oracle` returning 1.0 twice.
