# Stage 2-QC report (G34)

Reviewers: `prompts/QC_spec.md` (15 checks) and `prompts/QC_instruction.md` (22 checks),
adjudicated at temperature 0 in a separate pass from authoring.

## VERDICT: PASS

FAIL = 0. No SKIP. Three checks are recorded as SUPERSEDED rather than judged, each
because the prompt's text disagrees with a rule that a gate now enforces; the supersession
is named, not assumed.

## QC_instruction.md scorecard

| ID | Verdict | Evidence |
|---|---|---|
| A1 | PASS | Ten of the eleven H2s present, canonically spelled, in order. `## Build plan` is absent, which is correct at baseline (`generate_instruction.md` section 2.1: 6/6 shipped briefs omit it). `## Front-end specification` is present as the optional unbudgeted section (reference/G section G.3). |
| A2 | PASS | The framing paragraph sits between the H1 and `## Overview` and names one end-to-end outcome (open, try an exercise without an account, sign up, finish a lesson, extend the streak), followed by the trap stated in product-truth form. |
| A3 | PASS | `contract_lint.py` (G4) reports every canonical line verbatim, exit 0. The stale spatial rationale is absent. |
| A4 | PASS | No `{{ }}`, no TODO, no TBD, no FIXME, no bracketed instruction. The braces present are copy placeholders the product itself renders (`{time}`, `{n}`, `{date}`) and route parameters (`{slug}`, `{id}`), both pinned in the Literals Ledger. |
| A5 | PASS | `leak_scan.py` (G11) reports no canary text, exit 0. |
| A6 | PASS | No mention of a spec folder anywhere in the brief. |
| A7 | PASS | `deku-demo-pw-2026` appears in the `## Data model` verbatim block with the `/app/USER_README.md` instruction, and every seeded account uses it. |
| A8 | PASS | Env vars used: `DATABASE_URL`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`. All canonical. No invented variable, no hardcoded host or port. |
| B1 | PASS | Pattern `tracker-log`: slot `db`, provider PostgreSQL, one role. Category `solo_founder` modifier applied: signup is open, seeded accounts exist for grading. The role is renamed `user` to `learner` per the role-fit rule, keeping the count and the permission shape. No provider beyond the row. |
| B2 | PASS | The critical focus (idempotent write, no double-count) is numbered rule 20 with its negative case, and rule 21 states the concurrent form: two reports of one session produce exactly one accepted result. Rules 71 and 22 carry the second and third idempotency surfaces. |
| B3 | SUPERSEDED | The check asks for all three difficulty levers at variant `a`. This bundle is variant `b` (a companion document was supplied, `stage-1-derive.md`). `## Technical requirements` and `## Data model` are present; `## Build plan` is correctly absent, and the variant-`a` reminder clause is deleted as `generate_instruction.md` section 4 requires above `a`. |
| B4 | PASS | The seeds carry the boundary the critical focus needs: a cohort of exactly `12` so the top `7` and bottom `5` partition it, a tie at the promotion line at positions `7` and `8` with a decidable earlier earner, a learner with a live `4` day streak and `2` freezes, and a `restricted` account. |
| C1 | PASS | Every numbered rule is verifiable from outside, through a page or through the API. Negative cases are stated as outcomes (rejected as invalid, denied, nothing written) and no HTTP status is pinned. |
| C2 | PASS | 132 literals pinned and cross-checked by script against the brief before the ledger was written; the Literals Ledger carries every account, route, endpoint, status string, number, seeded record, naming scheme, env var, motion moment and design phrase. |
| C3 | PASS | Route table, journeys, API shapes and `## Data model` agree. Two contradictions found and fixed in this pass: journey 4 described seven promotion rows against a seeded cohort of two, and the seed said the two zones were both visible on a two-member board. The cohort is now seeded at `12` with ten further accounts declared in `## User roles`. |
| C4 | PASS with one SUPERSEDED clause | Every axis is present as direction: palette by role with the contrast requirement, type by personality and role with tabular figures, shape and density by feel, components by their five states with Escape-to-close and confirm-before-destroy, motion by character with reduced motion respected, an explicit light-mode commitment, and the accessibility and responsive bars. No behavioural statement leaks in: the copy block is content fact and the single-primary-action line is the drawn launch-surface obligation routed here by reference/O. **SUPERSEDED:** the clause failing "pinned type sizes or line-heights" is the retired half of the number rule. `generate_instruction.md` section 4, "The number rule, DECIDED" (A5), carries the exact font family and the exact sizes deliberately, and `source_lint.py` (G51) enforces it. Colour carries no hex, motion carries no duration and no curve, and space, radius and breakpoints carry no pixel, all of which this check does still bind. |
| C5 | PASS with one SUPERSEDED clause | Derived values are computed on read and stated so: hearts, the streak, the traces and every total. Seeding is stated idempotent. **SUPERSEDED:** the clause requiring concurrency invariants to be named as storage-level constraints (unique or partial-unique index) is exactly what INV9 forbids and `prescription_lint.py` (G43) fails. The invariants are stated as observable properties instead, which is the substitution INV9 mandates. |
| C6 | PASS | The only place a framework is named is `## Technical requirements` (NestJS, Handlebars, vanilla progressive enhancement). PostgreSQL is a declared provider and G5 requires it to be named; it appears in `## Technical requirements`, `## Data model` and the No mocks block, which is the shipped-brief convention. `## Overview` names what the product is not. `## Constraints` is a flat scope-out list. |
| C7 | WARN, by design | `window_lint.py` (G33) reports every graded section past its reference length and the join past the slice. This is reported, never failed: the brief has no length limit, the judge grades against self-contained criteria carrying their own evaluation rule, and `judge_score` never touches reward. The companion is 4,336 lines and G51 requires 266 topics and 695 enumerated items to reach the brief; trimming to the judge's window would trade reward-driving completeness for a diagnostic number. The critical focus (rules 20 to 24) is front-loaded within `## Core features`. |
| D1 | PASS | The laziest build is blocked at four points: every total is recomputed by the service from the stored attempts and the page's own numbers are declared a display; the streak is computed from stored history on read, not held in the page; hearts are computed from a stored refill mark with the carry, so a counter in memory fails the worked example; and the No mocks block names the concrete substitutes as violations. |
| D2 | PASS | Each rule was read for divergent readings. Three were tightened during authoring: the tie-break now names which of two equal rows wins and why; the heart carry now carries a worked example with both reads; and the due formula carries two worked examples at different target retentions. |
| D3 | PASS | No rule requires an admin credential, a boot-time environment action, or anything the agent cannot do from inside its own application. |

## QC_spec.md scorecard

| ID | Verdict | Evidence |
|---|---|---|
| S1 | PASS | Seven spec docs authored in the order 01, 05, 02, 03, 04, 06 with 00-decisions written alongside. |
| S2 | PASS | `01-PRD.md` states ten must-have features, inside the 6 to 10 band a companion raises the cap to (reference/G section G.2.1), with an explicit out-of-scope list. |
| S3 | PASS | `02-TRD.md` records the drawn stack and its rationale against the section 2.9 bounds; S5 derives the base image from it. |
| S4 | PASS | `03-app-flow.md` carries the route map, entry and redirects, journeys and states, written to the drawn navigation, work surface, create flow and feedback. |
| S5 | PASS | `04-uiux-brief.md` is derived from the companion section by section in the companion's own register, not re-authored from the draw. |
| S6 | PASS | `05-backend-schema.md` carries entities, ownership, invariants and seed data, authored before the TRD. |
| S7 | PASS | `06-implementation-plan.md` exists for author reference and does not surface in the brief. |
| S8 | PASS | Every draw is recorded as a `draw:` line in `00-decisions.md`. |
| S9 | PASS | Every residual judgment call is one line in `00-decisions.md`, including the 45-versus-42 picker discrepancy, the three open subjects, the invented league tier names and the scope calls. |
| S10 | PASS | The companion carry table records one row per companion section with its destination or its waiver, and the twelve G51 waivers are reproduced verbatim. |
| B1 | PASS | No value in the spec folder contradicts a value in the brief. |
| B2 | PASS | The spec folder is at `Output/_spec/<code>/` and never inside the bundle (CON-5). |
| G1 | PASS | The identity is re-cast onto the companion's own placeholder brand, `Larkwise`, rather than invented. The mapping is recorded. |
| G2 | PASS | The companion's efficacy claim and learner-count figure are deliberately NOT inherited, and the brief requires their absence. |
| G3 | PASS | No fact in the brief comes from outside the companion, the Task Order or the kit's closed world. |

## Findings raised and fixed in this pass

1. **C3, MAJOR.** Journey 4 described a promotion zone of seven rows and a demotion zone of
   five against a cohort seeded with two members. Fixed: the cohort is seeded at `12`, ten
   further learner accounts are declared in `## User roles`, and the journey now names the
   tie at the promotion line.
2. **G43, BLOCKER.** `## Constraints` said "no service worker", which names a mechanism
   nobody using the app can see. Fixed: replaced with the observable, that the app does not
   keep working with the network off and nothing is caught up later.
3. **G1 identity, MAJOR.** The first draft invented the product name `Daylark` while the
   companion's own placeholder table names `Larkwise`. Fixed throughout, and the mascot
   `Pip` and the product family were carried with it.
