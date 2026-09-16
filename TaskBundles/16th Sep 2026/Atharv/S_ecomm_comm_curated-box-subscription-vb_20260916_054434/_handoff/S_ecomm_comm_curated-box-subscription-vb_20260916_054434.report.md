# Build report - S_ecomm_comm_curated-box-subscription-vb_20260916_054434

Rendered from `_handoff/S_ecomm_comm_curated-box-subscription-vb_20260916_054434.gates.jsonl`.
No verdict in this file was typed by hand.

## Identity

| Field | Value |
|---|---|
| Task code | `S_ecomm_comm_curated-box-subscription-vb_20260916_054434` |
| Task id | `deku/curated-box-subscription-vb` |
| uuid_v5 | `3860c34d-6255-5076-a998-109d090aabd9` |
| Cell | solo_founder / ecommerce-retail / commerce-checkout |
| Service profile | `P5-db-pay-email` |
| Providers | db `postgres`, email `mailpit`, payments `killbill` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `python` |
| spec_sections_given | overview, roles, features, flow, uiux, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Vendored grader | 0.22.0 |
| Target schema | 1.4 |
| QL | abhishek.shaw@ethara.ai |
| Contributor | atharv.mahalwar@ethara.ai |

**Task Order note.** The order arrived with `pattern: transactional-checkout`, which is
not a level-3 code. It was keyed to `commerce-checkout`, the only checkout pattern legal
for `solo_founder`, and the substitution is recorded in `_spec/.../00-decisions.md`
rather than applied silently.

## Derived-design draws

Every one is a SHA-256 draw over the archetype `curated-box-subscription`, never a
preference.

```text
draw: render_model = mpa-progressive
draw: backend = Django + templates
draw: frontend = Alpine.js + server templates
draw: design_direction = companion
draw: nav = top-nav
draw: work_surface = split detail-pane
draw: create_flow = inline-row
draw: feedback = full-page-confirmation
```

Two overrides, both on the record:

| Axis | Drawn | Used | Why |
|---|---|---|---|
| `design_direction` | `terminal-mono` | `companion` | reference/L L.6.1. The companion measured a white page with candy accents and three type families; `terminal-mono` would have contradicted every measured value. |
| `nav` | `sidebar-nav` | `top-nav` | Supplied-source rule 0: the draws fill only what the companion leaves silent, and the companion states its navigation outright. |

`work_surface`, `create_flow` and `feedback` are kept from the draw: the companion's
section 18.2 records that the ordering surface was never captured, so the box builder is
exactly where the draw still governs.

Launch surface, drawn by reference/O O.3:
`cookie_choice, form_validation, mobile_viewport, privacy_page, social_preview`.
`flag_lint` reports nine bank obligations carried in total, five drawn plus four the
companion already stated. Above the floor, which is correct.

## Companion document

One supplied source: `aardvark_prd.md`, 1,721 lines, recorded in
`_handoff/....sources.json` so the sweep can be re-run without the operator remembering
what the Task Order carried.

G51 result: **15/15 colours** carried as family and tone words, **118/118 topics**,
**212/212 enumerated items**. Twenty-nine waivers, every one a capture-process artifact
rather than a product obligation: the performance measurements of the captured site,
the zero-asset substitution recipe, the evidence-gap register, the acceptance checklist,
four hue rows whose only unmatched words are hex fragments, the CSS transition and
media-query inventories, and the document's own register and confidence tables. The full
waiver list is the argument vector in the sweep command recorded below.

## Feature resolution

| Candidate | Verdict | Landed in | Reason |
|---|---|---|---|
| Monthly reveal, atomic at the cycle open | INCLUDED | Core features, pytest, browser | The product's spine. |
| Box composition rule, evaluated on the finished set | INCLUDED | Core features, pytest, browser, rubric | The hard part, and the one a naive build gets wrong by greying out titles. |
| Pre-seeded box link as untrusted input | INCLUDED | Core features, pytest | Companion 15.1 addition; the one security-shaped rule in the product. |
| Pricing as a formula per country | INCLUDED | Core features, pytest | Companion 7.1. |
| Promotion with its three restrictions | INCLUDED | Core features, pytest | Expiry added per companion 16. |
| Credits as a ledger with a fixed spend order | INCLUDED | Core features, pytest | Companion 7.5, 15.4. |
| Charged-but-unchosen banks one credit | INCLUDED | Core features, pytest | The companion's unanswered question, resolved. |
| Invoice in the billing platform | INCLUDED | Core features, pytest | The pattern's critical focus. |
| Confirmation and e-gift-card mail | INCLUDED | Core features, pytest | The email slot's observable. |
| Gift issued, redeemed, never reused, buyer blind | INCLUDED | Core features, pytest | Companion 9.3, 15.6. |
| Annual vote, one ballot per member | INCLUDED | Core features, pytest, browser | Companion 8. |
| Special shipping recognised at address entry | INCLUDED | Core features, pytest, browser | Companion 7.4. |
| Flat tag taxonomy, kept flat | INCLUDED | Core features, pytest, rubric | Companion 6.2; the brand's voice. |
| Cover hue derived once at ingest | INCLUDED | Data model, pytest, rubric | Companion 6.1. |
| Design system: palette, type, shape, motion, chrome | INCLUDED | UI/UX notes, browser, rubric | Companion 3, 4, 5, 6.3, 10, 11. |
| Launch surface: privacy, terms, cookies, previews, form validation | INCLUDED | Core features, Technical requirements, pytest | reference/O draw. |
| The two-origin split | DROPPED | - | A capture fact about the reference site, not a requirement. Waived on the record. |
| Native mobile applications | DROPPED | Constraints | Companion 1.4 names three clients; this build ships the web client and the one API they would share. Scoped out explicitly. |
| Performance budget and asset pipeline | DROPPED | - | Companion 12 and 17 measure the captured site and give a zero-asset recipe. reference/O excludes load timing as non-deterministic in a container. Waived. |
| Real book titles, authors, imprints, press outlets | DROPPED | Constraints | Companion 18.4 refuses to reproduce them and so does this brief. Every name is invented. |
| Declined-card handling | DROPPED | - | `killbill` is a billing platform with no charge object, no card token and no decline code. An INVENTED-FACT if written. |

## Slot obligations

| Slot | Provider | Verdict | Critical substep |
|---|---|---|---|
| db | `postgres` | MET | `test_concurrent_placement_yields_exactly_one_order_row` |
| email | `mailpit` | MET | `test_placed_box_delivers_a_confirmation_email` |
| payments | `killbill` | MET | `test_placed_box_creates_a_billing_charge_for_the_total` |

## Grading layer

| Measure | Value |
|---|---|
| Workflows | 16 (band 10 to 16) |
| Browser substeps | 56 |
| Pytest substeps | 65 |
| Critical substeps | 13 |
| Non-happy-path ids | 8 of 16 |
| Test module | `tests/test_output.py`, 65 tests, one module |
| Sections covered | core features, data integrity, authorization, edge cases, email, payments, presentation |
| Checklist items | 304, all cited (G24 two-way) |
| Rubric criteria | 19: 16 positive, 3 negative |

Non-happy-path workflow ids: `box_missing_a_current_title_is_invalid`,
`fourth_book_hits_the_box_limit`, `summer_code_is_invalid_outside_the_usa`,
`duplicate_and_concurrent_placement_create_one_invoice`,
`gift_buyer_cannot_read_what_the_recipient_chose`,
`member_or_anonymous_caller_cannot_read_another_members_rows`,
`invalid_or_empty_input_is_refused_and_writes_nothing`,
`second_ballot_is_a_duplicate_and_is_refused`.

Category mix: `core_outcome` 1, `data_integrity` 23, `business_rule` 16, `security` 7,
`validation` 9, `notification` 3, `presentation` 6. Floors are 1 core_outcome,
2 data_integrity (db declared) and 1 security (denial tokens present).

### Rubric dimension shares, positive scores only

| Dimension | Points | Share | Target | Within band |
|---|---|---|---|---|
| `instruction_following` | 18 | 0.30 | 0.30 | yes |
| `functionality` | 15 | 0.25 | 0.25 | yes |
| `ux_flow` | 9 | 0.15 | 0.15 | yes |
| `ui_visual` | 9 | 0.15 | 0.15 | yes |
| `motion` | 3 | 0.05 | 0.05 | yes |
| `accessibility` | 3 | 0.05 | 0.05 | yes |
| `responsiveness` | 3 | 0.05 | 0.05 | yes |

Negative magnitudes total 7 against 60 positive, well inside the 3x cap.
Thirteen of nineteen criteria are `task completion`, which is 68 percent and inside the
60 to 80 band.

`tests/rubric.json` is GENERATED from `solution/trinity/grounding.yaml` through the
vendored `recompute.py`. G48 re-runs the generator and compares bytes, so a hand edit is
a failure by construction.

## Literals ledger

139 pinned values. Classes:

| Class | Count |
|---|---|
| `credential` | 1 |
| `account` | 5 |
| `route` | 12 |
| `endpoint` | 14 |
| `status` | 9 |
| `number` | 15 |
| `seed_record` | 20 |
| `scheme` | 16 |
| `env_var` | 14 |
| `motion_moment` | 9 |
| `design_phrase` | 24 |

Two values are `verifier_only` and carried by `task.toml` alone: `DB_ADMIN_URL` and
`EMAIL_INBOX_API_URL`. Neither appears in `instruction.md` or in `[environment].env`
(INV4, checked both ways by G6 and G17).

The last two classes are the companion defence. A ledger with no design class is how a
motion section becomes one line reading "motion character: eased" and comes out invented
in every build; the nine motion moments and twenty-four design phrases are pinned as
short distinctive phrases so the brief must carry them and G6 checks that it does.

## Spec folder

Written to `Output/_spec/S_ecomm_comm_curated-box-subscription-vb_20260916_054434/`,
outside the bundle (CON-5).

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the two overrides, the identity re-cast, twelve resolved companion questions, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |

`06-implementation-plan.md` is absent: `## Build plan` is not emitted at baseline
(generate_instruction.md 2.1), so the doc that feeds it has nothing to feed. Recorded in
the QC receipt as a warning, not a defect.

## Grading window

Length is reported, never failed: the brief has no limit (G33).

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Core features | 15,628 | 2,400 | past-slice |
| UI/UX notes | 8,322 | 1,700 | past-slice |
| User flow | 3,781 | 1,900 | past-slice |
| Overview | 1,726 | 700 | over-reference |
| User roles | 1,529 | 1,000 | over-reference |
| Constraints | 1,069 | 800 | over-reference |
| Technical requirements | 1,635 | unbudgeted | - |
| Data model | 6,789 | unbudgeted | - |
| Deployment contract | 3,658 | unbudgeted | - |
| Definition of done | 495 | unbudgeted | - |

The joined graded total is past the 9,000-char run_rubric join slice. That is the
expected shape for a companion-backed task and it costs a diagnostic number rather than
reward: the judged criteria are self-contained and carry their own facts (G52), and
`judge_score` never touches the reward path. Nothing was cut to fit.

## Kit gate log

Rendered from the receipts. 32 rows, every one carrying the SHA-256 of the bytes it read.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G1/G12 | `layout_lint.py` | 0 | PASS |
| G2/G16 | `validate_task.py` | 2 | NOT-APPLICABLE |
| G4/G5 | `contract_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G10 | `no_sdk_lint.py` | 0 | PASS |
| G11 | `leak_scan.py` | 0 | PASS |
| G14 | `reward_path_lint.py` | 0 | PASS |
| G17 | `secret_hygiene_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G27/G30 | `rubric_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G31 | `determinism_lint.py` | 0 | PASS |
| G33 | `window_lint.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G41 | `flag_lint.py` | 0 | PASS |
| G43 | `prescription_lint.py` | 0 | PASS |
| G44 | `disclosure_lint.py` | 0 | PASS |
| G46 | `structure_lint.py` | 0 | PASS |
| G47 | `output_qc.py` | 0 | PASS |
| G48 | `truth_lint.py` | 0 | PASS |
| G50 | `docker_lint.py` | 0 | PASS |
| G51 | `source_lint.py` | 0 | PASS |
| G52 | `rubric_context_lint.py` | 0 | PASS |
| G54 | `comment_lint.py` | 0 | PASS |
| G55 | `runtime_deps_lint.py` | 0 | PASS |
| G56/G57/G58 | `if_lint.py` | 0 | PASS |
| G59/G60 | `codequality_lint.py` | 2 | NOT-APPLICABLE |
| G63 | `secret_lint.py` | 0 | PASS |

G38 (`kit_selftest.py`) is green at 32 checks for this kit revision, which is what
licenses this report to exist at all.

Three verdicts are not PASS and each says why:

- **G2/G16 NOT-APPLICABLE.** `task.toml` carries no `[delivery]` block. The block
  requires `@sha256:` digests present in `environment/`, and a digest can only come from
  a real image build the kit never performs. Fabricating four was refused. The handoff
  contract names this as the one open prerequisite.
- **G40 WARN.** Every one of the thirteen prompts has a current, bundle-bound receipt
  carrying the scorecard its own registry declares. The WARN is the SELF-ATTESTED state:
  owner and verifier are the same agent in a single-agent run, so these are recorded
  verdicts rather than independent ones. The kit reports that rather than hiding it.
- **G59/G60 NOT-APPLICABLE.** The bundle ships no code-quality rubric. Every judged
  criterion grades the running product; none carries `evaluation_target: "source"`.

Sweep command, with the G51 waivers, reproducible verbatim:

```text
python3 "$KIT/tools/revalidate.py" "$OUT/S_ecomm_comm_curated-box-subscription-vb_20260916_054434" \
 --waive "12. performance" --waive "the budget" --waive "additions" --waive "zero-asset" \
 --waive "the manifest" --waive "evidence gaps" --waive "the capture could not see" \
 --waive "refusals" --waive "confidence" --waive "acceptance checklist" \
 --waive "green #8dec7e" --waive "orange #fbbe63" --waive "pink #feb6fa" --waive "yellow #ffd24a" \
 --waive "subscriptionbox-bg-left-ear" --waive "soft-overshoot" --waive "bounce-2.27" \
 --waive "clip-path" --waive "@media" --waive "image/svg+xml" --waive "package and box visuals" \
 --waive "three typefaces, in two formats" --waive "press logos, four" \
 --waive "domain ecommerce-retail" --waive "archetype curated-box-subscription" \
 --waive "byte counts for vectors" --waive "marketing copy" \
 --waive "observed implementation, informational" --waive "addition, normative"
```

## Traceability

`tests/traceability-matrix.md` and `tests/traceability-matrix.csv` are regenerated by
every sweep from the scan G24 makes, so they cannot disagree with the gate. They ship
inside `tests/`, which is held out for the whole agent phase. Read them there rather
than restated here.

## Blocking findings

**Twenty-two obligations were removed from the coverage target and escalated.** They are
listed in full, grouped by owner, in the handoff contract under DECLARED BUT UNGRADED.
All twenty-two remain requirements in `instruction.md`; what was removed is the claim
that this kit grades them. This is OPEN-DECISIONS **D-H**, which proposes a fourth
checklist part `## Declared but ungraded` and is still unanswered; until it is, the
kit's own rule stands that G24 fails an ungraded item so no bundle can ship carrying one.

The group worth a kit decision is the six clock-dependent rules. A controllable clock in
the verifier would make the monthly cutoff, the token expiry and the promotion expiry
gradeable, and the cutoff is the single most interesting rule in this product.

No spec gap blocked a test that the brief actually asks for.

## Budget

`turns_expected = 170`, `tokens_expected = 7000000`, the Standard resource tier.
Reasoning: this is a variant `b` task built from a 1,721-line companion. It carries
thirteen tables, three backing services, a composition rule evaluated on a set, a
concurrency invariant on four separate surfaces, a two-currency pricing formula, a
credit ledger, a gift lifecycle, an annual ballot, and a measured design system with a
named easing vocabulary and an asymmetric mascot animation. That is the hard band, not
the medium one, and the budget is set there.

## Exit state

```text
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts toward corpus targets until the reference app is built
downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.
