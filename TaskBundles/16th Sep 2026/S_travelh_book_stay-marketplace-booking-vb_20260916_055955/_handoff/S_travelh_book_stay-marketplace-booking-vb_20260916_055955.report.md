# Build report: S_travelh_book_stay-marketplace-booking-vb_20260916_055955

| | |
|---|---|
| Task code | `S_travelh_book_stay-marketplace-booking-vb_20260916_055955` |
| Task id | `deku/stay-marketplace-booking-vb` |
| Cell | solo_founder / travel-hospitality / booking-scheduling |
| Archetype | `stay-marketplace-booking`, variant `b` |
| Service profile | `P1-db` (providers: `postgres`) |
| Variant axes | `critical_depth`, `spec_sections` |
| Language | typescript |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Verifier mode | `separate` (kit default since commit 11eaf7b; the agent image keeps the grader runtime anyway, recorded in 00-decisions.md) |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Input

Task Order (five fields plus the two addresses), and one companion document: a
3,896-line product requirements specification for a short-stay marketplace, supplied
with the order. `design_direction` is therefore `companion` (reference/L L.6.1): the
drawn direction `clinical-precision` is recorded in `_spec/.../00-decisions.md` and does
not govern.

The order arrived keyed `domain: travel-booking`, which is not a member of the kit's
domain enum. The only travel domain legal under `solo_founder` is `travel-hospitality`,
and the companion's own taxonomy table describes the same subject, so the order was keyed
to `travel-hospitality` and G0 passes on that.

## Derived design (all drawn from sha256 over the archetype)

| Axis | Value |
|---|---|
| render_model | `ssr-islands` |
| backend | `Hono` |
| frontend | `Remix` (React Router 7) |
| nav | `sidebar-nav` (companion overrides on the guest side; the draw governs the host area, which the companion never reached) |
| work_surface | `timeline` (companion governs search, listing and checkout; the draw governs host reservation management) |
| create_flow | `dedicated-route` |
| feedback | `optimistic-row` (applied to the host calendar editor only) |
| design_direction | `companion` (drawn: `clinical-precision`) |
| launch_surface | `colour_contrast, custom_404, meta_tags, mobile_viewport, terms_page` |

## Feature resolution

| Feature | Verdict | Where | Reason |
|---|---|---|---|
| Accounts and sessions | INCLUDED | `## Core features` Auth | open signup, two roles |
| Search, query in the address, cursor paging, map | INCLUDED | `## Core features` Search | companion 8, 10, 24 |
| Listing detail and the booking panel | INCLUDED | `## Core features` Listing detail | companion 11 |
| Pricing engine, fixed order, rounding, quote | INCLUDED | `## Core features` Pricing | companion 22 |
| Availability and reservations, holds, policy snapshot | INCLUDED | `## Core features` Availability | companion 21 |
| Checkout, idempotency, five failure paths | INCLUDED | `## Core features` Checkout | companion 12 |
| Payment authorise/capture, currency, webhooks, payouts | INCLUDED | `## Core features` Payment | companion 23, modelled in-product |
| Trips, messaging, wishlists, reviews, account | INCLUDED | `## Core features` | companion 13 |
| Trust, location, anti-discrimination, audit | INCLUDED | `## Core features` | companion 25, 26 |
| Host listings, calendar, reservations, earnings | INCLUDED | `## Core features` Host surfaces | companion 14 |
| Public surfaces, link grid, error views, terms | INCLUDED | `## Core features` Public surfaces | companion 9, 15, 29 |
| External map tiles, card acquiring, tax vendor, FX feed, mail vendor, analytics vendor, search engine | DROPPED | `## Constraints` | no runtime network; each becomes an in-product component with the same observable contract |
| Experiences and services booking flows | DROPPED | `## Constraints` | inventory type and route only |
| Mobile app promotion banner | DROPPED | `## Front-end specification` | the companion's own decision table recommends omitting it |
| Build plan | DROPPED | not emitted | non-baseline at variant b |

## Slot obligations

| Slot | Provider | Status | Evidence |
|---|---|---|---|
| backend (db) | `postgres` | MET | `test_seeded_listing_rows_are_persisted_and_not_duplicated`, `critical`, asserts rows in the declared datastore |

## Grading layer

| | |
|---|---|
| Workflows | 15 (solo_founder band 10 to 16) |
| Browser substeps | 36 |
| pytest substeps | 44 |
| Critical substeps | 8 |
| Non-happy-path ids | `concurrent`, `duplicate`/`at_most`, `cannot`, `denied`, `forbidden`, `expired`, `invalid`, `limit`, `empty` |
| pytest module | `tests/test_output.py`, one module, 44 tests |
| Rubric criteria | 22 (18 positive, 4 negative) |
| Judgment obligations graded | 28 of 28 |
| Checklist items | 164 across ten section codes |

Rubric dimension shares over positive scores: `instruction_following` 0.26,
`functionality` 0.22, `ux_flow` 0.14, `ui_visual` 0.24, `motion` 0.03,
`accessibility` 0.07, `responsiveness` 0.03. Every one is inside the 0.10 band
`rubric_lint.py` enforces.

## Grading window

| Section | Characters | Reference |
|---|---|---|
| core_features | 32,146 | 2,400 |
| user_flow | 4,171 | 1,900 |
| ui_ux_notes | 10,376 | 1,700 |
| constraints | 1,413 | 800 |
| user_roles | 2,275 | 1,000 |
| overview | 1,967 | 700 |

Reported, never failed. The companion states more graded rules than the judge's window
holds; `judge_score` never touches reward, and `generate_instruction.md` 4 says plainly
not to cut a real rule to fit. Every criterion carries its own facts, so the judge does
not depend on the sliced text.

## Literals ledger

217 literals: 4 accounts, 1 credential, 6 environment variables (1 verifier-only),
22 routes, 31 endpoints, 23 statuses, 7 numbers, 4 seeded listings, 60 schemes and
field names, 49 pinned copy strings, 6 motion moments, 10 design phrases. Full file at
`_handoff/S_travelh_book_stay-marketplace-booking-vb_20260916_055955.literals-ledger.json`.

## Kit gate log (rendered from the receipts, never transcribed)

| Gate | Tool | Exit | Verdict | Verdict line |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | (no verdict line) |
| `G1/G12` | `layout_lint.py` | 0 | PASS | (no verdict line) |
| `G46` | `structure_lint.py` | 0 | PASS | (no verdict line) |
| `G50` | `docker_lint.py` | 0 | PASS | (no verdict line) |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | (no verdict line) |
| `G63` | `secret_lint.py` | 0 | PASS | (no verdict line) |
| `G48` | `truth_lint.py` | 0 | PASS | (no verdict line) |
| `G51` | `source_lint.py` | 0 | PASS | (no verdict line) |
| `G52` | `rubric_context_lint.py` | 0 | PASS | (no verdict line) |
| `G54` | `comment_lint.py` | 0 | PASS | (no verdict line) |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | (no verdict line) |
| `G11` | `leak_scan.py` | 0 | PASS | (no verdict line) |
| `G33` | `window_lint.py` | 0 | PASS | (no verdict line) |
| `G4/G5` | `contract_lint.py` | 0 | PASS | (no verdict line) |
| `G43` | `prescription_lint.py` | 0 | PASS | (no verdict line) |
| `G44` | `disclosure_lint.py` | 0 | PASS | (no verdict line) |
| `G10` | `no_sdk_lint.py` | 0 | PASS | (no verdict line) |
| `G31` | `determinism_lint.py` | 0 | PASS | (no verdict line) |
| `G14` | `reward_path_lint.py` | 0 | PASS | (no verdict line) |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | (no verdict line) |
| `G41` | `flag_lint.py` | 0 | PASS | (no verdict line) |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | (no verdict line) |
| `G59/G60` | `codequality_lint.py` | 2 | NOT-APPLICABLE | (no verdict line) |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | (no verdict line) |
| `G6` | `fixture_lint.py` | 0 | PASS | (no verdict line) |
| `G24` | `coverage_map.py` | 0 | PASS | (no verdict line) |
| `G37` | `checklist_qc.py` | 0 | PASS | (no verdict line) |
| `G39` | `rubric_align_lint.py` | 0 | PASS | (no verdict line) |
| `G28/G29` | `channel_lint.py` | 0 | PASS | (no verdict line) |
| `G40` | `prompt_receipt_lint.py` | 0 | PASS | (no verdict line) |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | (no verdict line) |
| `G47` | `output_qc.py` | 0 | PASS | (no verdict line) |

Run-level, outside the per-bundle sweep:

| Gate | Tool | Verdict |
|---|---|---|
| G38 | `kit_selftest.py` | PASS, 32 checks |
| G49 | `diversity_lint.py` | PASS; concentration NOT-APPLICABLE at 3 bundles |
| G42 | `corpus_overlap.py` | NOT-APPLICABLE, one complete comparable bundle in this output root |
| G26 / G61 | `corpus_report.py` | NOT-APPLICABLE, no admissible bundle yet. This is not a pass |

## Prompt receipts (G40)

Every certification prompt carries a current, bundle-bound receipt with the scorecard its
own registry declares: `task_code_verifier.md` (G3), `QC_spec.md` and `QC_instruction.md`
(G34), `qc_toml.md` (G36), `qc_docker.md` (G35), `qc_solution_checklist.md` (G37),
`qc_rubric.md` (G53). Three generator prompts carry receipts too: `generate_instruction.md`,
`toml_generator.md`, `docker_generator.md`.

**Every one is SELF-ATTESTED.** The kit's rule is owner is not verifier; one agent
authored these artifacts and ran the reviewers, so these are recorded verdicts, never
independent ones. An independent QC pass is the first thing a reviewer should add.

Fourteen checks across the seven registries resolved WARN rather than PASS, each because a
prompt's own rule has been superseded by a newer owner. They are listed in full with their
evidence in `_handoff/S_travelh_book_stay-marketplace-booking-vb_20260916_055955.receipts.json`; the recurring ones are the retired baseline
`## Build plan`, the settled no-numbers rule for design values, and the variant-b deletion
of the concurrency reminder.

## Blocking findings

None mechanical. Three brief obligations are stated in `instruction.md` and carried by no
channel, because no channel can observe them: the credentials file at
`/app/USER_README.md`, the reserved `.browser_screenshots/` and `.downloads/` directories,
and the no-edge-functions / no-persistent-volumes clause. They are App Contract clauses
enforced by review (G3) rather than product features. This is OPEN-DECISIONS D-H, recorded
rather than fabricated into a citation.

## Budget

`turns_expected = 220`, `tokens_expected = 3200000`. The reasoning: ten must-have features
against the companion-backed 6 to 10 cap, 23 routes, 36 API endpoints, 23 tables and a
pricing engine with a fixed order of operations. That is well above the six-feature
baseline the standard band was drawn for, and `reference/G` G.2.1 says plainly to raise
the budget with the feature count rather than pretend ten features build in the time six
do.

## Kit revision

Rebuilt against `deku-green-field` at commit `806eb0a` (five commits: the `code_quality`
code-rubric dimension, the `test_output.py` / `test_ans.py` rename, the `separate`
verifier-mode default, the `test.sh` comment strip and re-pin, and the restored generated
`solution/USER_README.md`). Every VENDORED file was re-copied at the new pin, the answer
key regenerated by `recompute.py` at `truth-generator-7`, and `qc_toml.md` re-adjudicated
because its receipt token moved with the prompt.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference application. Build one downstream from
`solution/checklist.md`, then run the handoff gates in
`_handoff/S_travelh_book_stay-marketplace-booking-vb_20260916_055955.handoff.md`.
