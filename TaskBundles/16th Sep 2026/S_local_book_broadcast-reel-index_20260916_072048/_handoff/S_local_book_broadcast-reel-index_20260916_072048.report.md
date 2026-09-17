# Build report: S_local_book_broadcast-reel-index_20260916_072048

Task name: Tallow
Archetype: broadcast-reel-index
Built: 2026-09-16

## What this bundle is

A greenfield task. An agent receives `instruction.md` and nothing else, and must
build and deploy a working web application for a two-principal advertising agency:
a numbered index of seventeen film productions, a case study per production with a
hero reel, credits and captioned still galleries, and a fifteen minute introductory
call booked against the agency's published availability.

The load-bearing difficulty is the booking. A hold expires after a fixed lifetime, a
repeated idempotency key must not create a second booking, and two confirmations of
one slot arriving at the same instant must leave exactly one confirmed booking, with
the loser refused. The brief states that this must hold at the database level rather
than in application logic alone, so an interface that merely hides a taken slot does
not satisfy it.

## Task Order substitutions

The Task Order named `portfolio-agency` as the domain and `media-gallery` as the
pattern. Neither is a member of the kit's enumerations, so each was mapped to the
nearest member and the mapping recorded in `Output/_spec/.../00-decisions.md`:

| Given | Used | Why |
|---|---|---|
| `portfolio-agency` | `local-services` | a single-location agency selling its own services |
| `media-gallery` | `booking-scheduling` | the slot-contention rule is the task's critical focus |

The `booking-scheduling` mapping is the stronger of the two. The supplied PRD's own
section 20.7 specifies exclusion constraints over booking ranges and section 14.3
specifies the simultaneous-confirmation edge case, so the booking pattern is what
the source document itself treats as the hard part.

## Layers

| Layer | Artifact | Size |
|---|---|---|
| Brief | `instruction.md` | 10 H2 sections |
| Checklist | `solution/checklist.md` | 519 items over 9 section blocks |
| Answer key | `solution/trinity/grounding.yaml` | 11 trajectory steps, 8 rejected routes |
| pytest | `tests/test_output.py` | 43 test functions |
| Browser | `tests/workflows.yaml` | 16 workflows, 58 browser substeps, 43 pytest substeps |
| Rubric | `tests/rubric.json` | 20 judged criteria, 17 positive, 3 negative |

## Coverage

Every one of the 519 checklist items is cited by exactly one grading channel, and
`channel_lint` confirms no part of any ask is graded twice:

| Channel | Items | Carriers |
|---|---|---|
| pytest | 232 | 41 test functions |
| browser | 226 | 56 substeps |
| rubric | 61 | 20 criteria |

`traceability-matrix.md` renders this as 149 core asks over 115 graders, all fully
graded, none uncovered.

Eighteen items are cited for the record but marked unobservable in
`<code>.unobservable.txt`: the frontend and backend frameworks, the build toolchain,
the process model, the container topology, and the token lifetime. No channel
available to the verifier can see any of them from inside the running system, and
saying so in the matrix is more honest than a citation that implies otherwise.

## The supplied PRD

`inkfish_prd.md` (126,032 bytes, sha256 `c4ef1ece5d8f8172...`) was supplied with the
Task Order and is recorded in `<code>.sources.json`. G51 reports 154/154 topics and
405/405 enumerated items carried, of which 177 are carried by explicit waiver listed
in `<code>.g51-waivers.txt`. The waivers fall into three kinds:

1. **Exact values the house style bars.** Hex colour codes, font file names, SVG path
   data, cubic-bezier curves and pixel extents. The brief states these by family and
   tone instead, which G51 confirms for all eight source colours.
2. **Topics the brief's own Constraints section scopes out.** Cookie consent and
   analytics, the transcode pipeline and object storage, calendar synchronisation,
   the outbox and audit trail, search, payments, the enquiry form, the cursor system,
   the marquee, and the performance and caching engineering.
3. **PRD material about the PRD.** The difficulty tiers, the module identifiers, the
   zero-asset substitution guide, the evidence-gap notes and the acceptance checklist
   describe how the source document was assembled, not what the product must do.

A reader checking this work should read the waiver list rather than trust the ratio:
a waiver is a decision, not a pass.

## Gate status

30 of 32 gates green. The two red ones are named in the handoff and neither is a
defect in the bundle.
