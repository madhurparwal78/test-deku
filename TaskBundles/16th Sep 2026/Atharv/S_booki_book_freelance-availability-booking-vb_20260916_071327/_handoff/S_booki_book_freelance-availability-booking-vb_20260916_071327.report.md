# Build report - S_booki_book_freelance-availability-booking-vb_20260916_071327

## Identity

| | |
|---|---|
| Task code | `S_booki_book_freelance-availability-booking-vb_20260916_071327` |
| Task id | `deku/freelance-availability-booking-vb` |
| Cell | solo_founder / booking-services / booking-scheduling |
| Service profile | `P2-db-email` |
| Providers | backend `postgres`, email `mailpit` |
| Variant | `b`, axes ['critical_depth', 'spec_sections'] |
| Language | `typescript` |
| Capability flags | `aesthetic` |
| Design direction | `companion` |
| Launch surface | `cookie_choice,no_frontend_secrets,security_headers,social_preview,terms_page` |
| spec_sections_given | ['overview', 'roles', 'features', 'flow', 'uiux', 'frontend', 'techrequirements', 'datamodel', 'constraints', 'contract'] |
| Shard | 1 of 1 |

The Task Order arrived keyed `domain: portfolio-agency`, which is not a member of
the closed solo_founder domain enum in `taxonomy_name.py`. Filed at
`booking-services`, the legal domain whose cell carries the requested
`booking-scheduling` pattern and whose profile list contains the `P2-db-email`
this product needs: the brief sends ten transactional messages, so a
database-only profile would leave the mail slot undeclared. Recorded in
`_spec/S_booki_book_freelance-availability-booking-vb_20260916_071327/00-decisions.md`.

The Task Order's contributor address, `atharv/mahalwar@ethara.ai`, carries a
slash where an address takes a dot. Corrected to `atharv.mahalwar@ethara.ai` in
`[task].authors` and `[metadata].contributor_id`; a slash is not legal in the
local part of an address as written and `validate_task.py` would have refused it.

## Derived-design draws

Drawn over the bare archetype `freelance-availability-booking`, per reference/L
L.4 and reference/O O.3.

```text
draw: render_model = spa-json-api
draw: backend = Hono
draw: frontend = Svelte + Vite
draw: design_direction = companion
draw: nav = sidebar-nav
draw: work_surface = calendar-grid
draw: create_flow = slide-over
draw: feedback = toast        OVERRIDDEN
launch_surface = cookie_choice,no_frontend_secrets,security_headers,social_preview,terms_page
```

The design-direction draw does not govern: a companion PRD was supplied and
reference/L L.6.1 hands the axis to the source, which is why
`[metadata].design_direction` reads `companion`. The `feedback = toast` draw is
overridden for the same reason -- the companion bans a floating corner message by
name, and the brief carries its three notification surfaces instead. That
override is itself graded, as the negative criterion `R23`.

`nav = sidebar-nav` and `work_surface = calendar-grid` govern the studio surfaces
behind the sign-in, which the companion never saw; the companion's fixed chrome
governs the three public documents.

## Feature resolution

| Feature | Verdict | Where | Reason |
|---|---|---|---|
| Accounts, sessions and the sign-in link | INCLUDED | `## Core features` / Auth | pattern baseline, open signup |
| Three public scrolling documents | INCLUDED | `## Core features` | companion information architecture |
| Nine projects in two presentations | INCLUDED | `## Core features` | companion work index plus home preview |
| Availability derived from the windows | INCLUDED | `## Core features` | the archetype's own hard part |
| Windows and holds | INCLUDED | `## Core features` | the capacity model the booking pattern needs |
| The six-field enquiry with budget bands | INCLUDED | `## Core features` | companion contact section |
| Enquiry to proposal to booking | INCLUDED | `## Core features` | the workflow the product exists for |
| The studio pipeline and the export | INCLUDED | `## Core features` | single-operator risk, stated in `## User roles` |
| Ten transactional messages | INCLUDED | `## Core features` | drives the `email` slot |
| The public edge and the cookie answer | INCLUDED | `## Core features` | launch surface draw |
| Payment of any kind | EXCLUDED | `## Constraints` | a booking here is an agreed start date and nothing more |
| File upload anywhere | EXCLUDED | `## Constraints` | six text fields bring no scanning or retention duty |
| The twenty-one sound cues | EXCLUDED | `## Constraints` | the control, its two strings and the no-sound-alone rule stay |
| The three-dimensional render pipeline | EXCLUDED | `## Constraints` | a moving drawn ground is required, a scene graph is not |
| Password policy, staff hierarchy, roles above two | EXCLUDED | `## Constraints` | a hierarchy for a single operator is work nobody uses |
| Third-party analytics, translation, newsletters | EXCLUDED | `## Constraints` | the page-view record is local and gated |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| backend | `postgres` | MET | critical pytest substeps in `app_is_reachable_and_titled` and `two_acceptances_one_place_left` |
| email | `mailpit` | MET | critical pytest substeps in `mail_is_real_in_mailpit` |

## Grading surface

| | |
|---|---|
| Workflows | 16 (band for solo_founder is 10-16) |
| Browser substeps | 60 |
| Pytest substeps | 108 |
| Critical substeps | 13 |
| Non-happy-path ids | `enquiry_form_rejects_invalid_input`, `client_calls_are_denied_on_the_server` |
| Pytest module | one, `tests/test_output.py`, covering deployment, seed, auth, availability, capacity, the workflow, mail, the pipeline and the public edge |
| Pytest functions | 108 |
| Checklist items | 522, at core-ask granularity over 180 core asks |

Every checklist item is cited by exactly one channel and every grader is cited by
at least one item: G24 closes the join in both directions, G28/G29 holds channel
exclusivity, and the whole set descends from one generator table so the four
artifacts cannot drift apart.

## Rubric

23 judged criteria, 21 positive and 2 negative, all
GENERATED from `solution/trinity/grounding.yaml` through the vendored
`recompute.py`. The reference rubric alongside them carries 108
compiled items, one per committed grader; its compiled-weight share is 0.86,
above the 0.60 floor.

| Dimension | Criteria | Share | Target |
|---|---|---|---|
| `instruction_following` | 6 | 0.32 | 0.30 |
| `functionality` | 4 | 0.27 | 0.25 |
| `ux_flow` | 4 | 0.16 | 0.15 |
| `ui_visual` | 3 | 0.15 | 0.15 |
| `motion` | 2 | 0.05 | 0.05 |
| `accessibility` | 2 | 0.05 | 0.05 |

## Literals ledger

161 pinned values across 13 classes:
`account` 2, `credential` 1, `design_phrase` 33, `duration` 6, `enum_option` 6, `env_var` 8, `mail_subject` 10, `message` 9, `number` 15, `route` 2, `seed_record` 16, `state` 25, `ui_string` 28.
G6 holds the bijection in both directions between the ledger, `instruction.md`
and the graders.

Two pinned strings sit outside the ledger's table by necessity rather than by
choice: `Sound | OFF` and `Sound | ON` both contain a pipe, and the pinned
literals table is pipe-delimited. Both are stated verbatim in their own checklist
item instead, and the copy is not misspelled to fit the table.

## spec/ documents

Emitted to `Output/_spec/S_booki_book_freelance-availability-booking-vb_20260916_071327/`, never inside the bundle (CON-5).

- `00-decisions.md`
- `01-PRD.md`
- `02-TRD.md`
- `03-app-flow.md`
- `04-uiux-brief.md`
- `05-backend-schema.md`
- `06-implementation-plan.md`

`## Build plan` is NOT emitted at this variant, so nothing in
`06-implementation-plan.md` reaches `instruction.md` (G44 PASS).

## Companion carriage

`yannesidibe_prd.md` is archived at
`_handoff/S_booki_book_freelance-availability-booking-vb_20260916_071327.companion-prd.md` and carried under G51:

| | |
|---|---|
| Source colours described by family and tone | 18 of 18 |
| Topics carried into the brief | 272 of 272 |
| Enumerated items carried into the brief | 752 of 752 |
| Declared waivers | 50 items, 7 topics |

The waivers fall in four classes, each on the record in the sweep receipt: the
companion's own authoring apparatus, the design-token value sheets the number
rule keeps out of a brief, identifiers the lint renders unmatchable by stripping
their underscores, and the two reference bodies scoped out in `## Constraints`.
Nothing product-bearing was dropped silently.

## Grading window

Reported by `window_lint.py`, never failed (G33 retired the length cap).

| Section | Chars |
|---|---|
| Core features | 16947 |
| UI/UX notes | 11673 |
| Front-end specification | 8551 |
| User flow | 5247 |
| Data model | 5156 |
| Deployment contract | 4473 |

The brief has no length limit. The three largest sections run past the judge's
2,500-char slice; the tail reaches the agent in full. No rule was cut to fit, and
every judged criterion carries its own facts (G52 PASS at 23 of 23), so the slice
costs a diagnostic number rather than reward.

## Kit gate log

Rendered from `_handoff/S_booki_book_freelance-availability-booking-vb_20260916_071327.gates.jsonl`. Input fingerprint covers
23 bundle files.

| Gate | Tool | Exit | Verdict | State |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | ok |
| `G1/G12` | `layout_lint.py` | 0 | PASS | ok |
| `G46` | `structure_lint.py` | 0 | PASS | ok |
| `G50` | `docker_lint.py` | 0 | PASS | ok |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | ok |
| `G63` | `secret_lint.py` | 0 | PASS | ok |
| `G48` | `truth_lint.py` | 0 | PASS | ok |
| `G51` | `source_lint.py` | 0 | PASS | ok |
| `G52` | `rubric_context_lint.py` | 0 | PASS | ok |
| `G54` | `comment_lint.py` | 0 | PASS | ok |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | ok |
| `G11` | `leak_scan.py` | 0 | PASS | ok |
| `G33` | `window_lint.py` | 0 | PASS | ok |
| `G4/G5` | `contract_lint.py` | 0 | PASS | ok |
| `G43` | `prescription_lint.py` | 0 | PASS | ok |
| `G44` | `disclosure_lint.py` | 0 | PASS | ok |
| `G10` | `no_sdk_lint.py` | 0 | PASS | ok |
| `G31` | `determinism_lint.py` | 0 | PASS | ok |
| `G14` | `reward_path_lint.py` | 0 | PASS | ok |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | ok |
| `G41` | `flag_lint.py` | 0 | PASS | ok |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | ok |
| `G59/G60` | `codequality_lint.py` | 2 | ? | ok |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | ok |
| `G6` | `fixture_lint.py` | 0 | PASS | ok |
| `G24` | `coverage_map.py` | 0 | PASS | ok |
| `G37` | `checklist_qc.py` | 0 | PASS | ok |
| `G39` | `rubric_align_lint.py` | 0 | PASS | ok |
| `G28/G29` | `channel_lint.py` | 0 | PASS | ok |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | ok |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | ok |
| `G47` | `output_qc.py` | 0 | PASS | ok |

`G59/G60` returns exit 2 NOT-APPLICABLE: the bundle carries no code-quality
rubric. `G40` returns WARN because every certification prompt was run by the same
agent that authored the artifact, which the kit records as SELF-ATTESTED rather
than as an independent verdict.

## Certification prompts

All seven receipts are in `_handoff/S_booki_book_freelance-availability-booking-vb_20260916_071327.receipts.json`, each bound to this
task code, each carrying a verdict for every id in its own registry:
292 check verdicts in total, zero FAIL. The divergences between a QC
prompt's registry and the kit's current emission rules are recorded there as
findings against the prompt rather than the bundle -- the eleven-section list,
the three-lever list, the storage-level-invariant wording and the retired length
cap, each superseded by `generate_instruction.md` 2.1 / 4, INV9 with G43, or
G33.

Defects this pass found and fixed are recorded in the same file: the `uuid_v5`
was first minted over the archetype rather than the full task code, a global
`vite` pin in the Dockerfile would have clashed with whatever the agent's own
manifest resolves, the rules of `## Core features` did not ascend in document
order, the judged rubric's dimension budget sat at `ui_visual` 0.47 with
`functionality` empty, and one pinned string was wrapped across two lines so the
literals bijection could not see it.

## Budget

`turns_expected` 200, `tokens_expected` 8,000,000: the top of the documented
range, which is where a companion-backed task at variant `b` with a 67-rule
feature section sits. `difficulty` stays the mandated empty placeholder;
calibration writes it.

## Blocking findings

None. No spec gap and no harness gap prevented a required test.
`[delivery.images]` is deliberately empty pending registry access, as the handoff
contract records.

## Versions

| | |
|---|---|
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Harbor | `0.20.0` |

## Exit state

```text
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the reference app
lands downstream and `harbor run -a oracle` returns `1.0` twice.
