# Build report - E_itdev_cont_structured-content-platform-vb_20260916_073627

Rendered from `_handoff/E_itdev_cont_structured-content-platform-vb_20260916_073627.gates.jsonl`
and `_handoff/E_itdev_cont_structured-content-platform-vb_20260916_073627.receipts.json`.
No verdict in this file was typed by hand.

## Identity

| Field | Value |
|---|---|
| Task code | `E_itdev_cont_structured-content-platform-vb_20260916_073627` |
| Task id | `deku/structured-content-platform-vb` |
| Cell | enterprise / it-devtools / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | `backend = postgres`, `storage = minio` |
| Variant | `b`, axes `critical_depth` + `spec_sections` |
| Language | `typescript` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Capability flags | `aesthetic` |
| Design direction | `companion` (reference/L L.6.1: a supplied companion beats the draw) |
| Launch surface | cookie_choice, custom_404, no_broken_links, sitemap_robots, spam_protection |
| Shard | 1 of 1 |
| uuid_v5 | `34f17a85-fbd9-5a38-b133-1e978aff4fe6` |

## The input, and the two mappings it needed

The Task Order named `domain: it-service-management` and
`pattern: collaborative-workspace`. Neither is a member of the closed enums in
reference/A, so each was carried to its nearest legal cell and the decision recorded in
`_spec/<code>/00-decisions.md`:

| Task Order field | Carried as | Why |
|---|---|---|
| `it-service-management` | `it-devtools` | the enterprise domain for platforms built for engineering teams |
| `collaborative-workspace` | `content-publishing` | the idea's spine is a document store, drafts and publishing, an image pipeline and a document reaching every connected surface. `collaboration-shared` is the nearer NAME and is a dead cell in all three categories: its only legal profile needs a `realtime` slot no provider in `environment/registry.json` serves. The live collaboration in the idea is carried in full and is served by the application's own event stream on its own origin. |

`taskorder_lint.py` (G0) passed on the mapped order before any design work began.

## Derived-design draws

Drawn by SHA-256 over the archetype `structured-content-platform`, per
generate_instruction 2.9 / 2.10 and reference/O O.3.

```
draw: render_model = mpa-progressive
draw: backend = NestJS + Handlebars
draw: frontend = Alpine.js + server templates
draw: design_direction = companion        (bank draw was brutalist-utility; L.6.1 hands the axis to the companion)
draw: nav = top-nav
draw: work_surface = table-first
draw: create_flow = modal
draw: feedback = full-page-confirmation
draw: launch_surface = cookie_choice, custom_404, no_broken_links, sitemap_robots, spam_protection
```

The drawn stack is unusual for an editor with live collaboration, which is the mechanism
working rather than failing: the brief states the rendering model as an observable
consequence (every route is produced on the server; the browser receives the content of a
route on first paint) and leaves the rest to the builder. Both entries install from the
official package registry at image build time and serve a production build on `4173`
bound `0.0.0.0`, which are the only two bounds 2.9 allows a draw to be rejected on.

## Feature resolution

| Candidate | Verdict | Where |
|---|---|---|
| Document store, reserved fields, keyed array items | INCLUDED | Core features 7-10, Data model |
| Portable Text: split, merge, decorators against annotations, serializer contract | INCLUDED | Core features 11-21 |
| Drafts, four states, publish as one transaction, revision chain, perspectives, preview grant | INCLUDED | Core features 22-28 |
| Mutations, patches by key, transactions, revision base, idempotency, mutation by query | INCLUDED | Core features 29-38 |
| References, strong and weak, publish dependency | INCLUDED | Core features 39-42 |
| Query language, parameters, functions, cost model, bounds | INCLUDED | Core features 43-51 |
| Event stream, gap detection, live queries, backpressure | INCLUDED | Core features 52-58 |
| Collaborative editing, presence, no locks, replay, cursor position | INCLUDED | Core features 59-64 |
| Studio: schema as code, affordances against security, validation, document table | INCLUDED | Core features 65-70 |
| Assets: asset against use, dedup, hotspot and crop order, derived images, upload safety | INCLUDED | Core features 71-80 |
| Migrations: dry run default, idempotence, resumability, expand-migrate-contract, key preservation | INCLUDED | Core features 81-86 |
| Datasets: visibility, copy, deletion window | INCLUDED | Core features 87-90 |
| Tokens and grants, no field-level security, perspective downgrade | INCLUDED | Core features 91-95 |
| Webhooks: filter, projection, recorded deliveries, coalescing | INCLUDED | Core features 96-98 |
| Scheduling and releases, lazily executed | INCLUDED | Core features 99-101 |
| Search: editor against consumer, span-boundary token, grants at query time | INCLUDED | Core features 102-107 |
| Internationalization: two patterns, fallback flag, empty against missing | INCLUDED | Core features 108-111 |
| Public site: home spine, docs, blog on the product's own model, 404, consent, sitemap | INCLUDED | Core features 112-126 |
| The twelve honesty strings | INCLUDED | Core features 127 |
| Hero video and adaptive player | DROPPED | the companion ships no binary (its Section 42); the hero ground is a generated inline vector scene. Recorded in 00-decisions |
| Outbound webhook delivery, signature verification, retry, dead letter | DROPPED | no outbound network call at runtime. Constraints |
| Regions, replicas, residency, edge cache, backups and restore drills | DROPPED | Constraints |
| Federated identity, second factor, password reset, signup | DROPPED | Constraints, and the enterprise modifier closes signup |
| Billing, plans, quotas, usage metering | DROPPED | Constraints |
| Third-party consent vendor, analytics vendor, tag manager | DROPPED | replaced by a first-party consent control. Constraints |

## Slot obligations

| Slot | Provider | Status | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_publish_stores_one_published_row_and_removes_the_draft` (critical), `test_concurrent_increments_are_all_stored`, `test_replayed_transaction_id_applies_once` (critical) |
| `storage` | `minio` | MET | `test_uploaded_bytes_live_in_the_bucket_at_the_pinned_key` (critical), `test_identical_uploads_deduplicate_to_one_asset`, `test_derived_rendering_is_cached_under_its_own_prefix` |

## Grading layer

| Measure | Value |
|---|---|
| Workflows | 20 (enterprise band 13-23) |
| Browser substeps | 40 |
| Pytest substeps | 66 |
| Critical substeps | 18 |
| Browser-to-pytest ratio | 0.61 (band 0.40-2.00) |
| Workflows carrying a browser substep | 20 of 20 |
| Non-happy-path ids | `wrong_password_is_rejected_at_sign_in`, `contributor_cannot_publish_a_document`, `cross_department_read_is_denied`, `anonymous_reader_cannot_see_a_draft`, `array_items_keep_their_keys_under_concurrent_edits`, `duplicate_transaction_id_applies_once`, `publish_with_unpublished_dependency_is_rejected`, `invalid_upload_is_refused_before_it_is_decoded` |
| Pytest module | one, `tests/test_output.py`, 66 functions |
| Concerns covered | core features, authorization, data integrity, edge cases, storage |
| Category mix | security 18, data_integrity 20, core_outcome 3, business_rule 12, validation 9, presentation 4 |

### Rubric

18 judged criteria, generated from `solution/trinity/grounding.yaml` by the vendored
`recompute.py`. 16 positive, 2 negative.

| Dimension | Positive points | Share | Target |
|---|---|---|---|
| instruction_following | 13 | 0.31 | 0.30 |
| functionality | 11 | 0.26 | 0.25 |
| ux_flow | 6 | 0.14 | 0.15 |
| ui_visual | 6 | 0.14 | 0.15 |
| motion | 2 | 0.05 | 0.05 |
| accessibility | 2 | 0.05 | 0.05 |
| responsiveness | 2 | 0.05 | 0.05 |

The reference rubric in `solution/trinity/rubrics.json` carries 16 items, every one
`mode: compiled` and bound to a committed test function, so the compiled weight share is
`1.0` against the 0.60 floor.

## Answer key

`solution/trinity/grounding.yaml` carries 17 trajectory steps whose `checkers` set equals
the 66 functions of `tests/test_output.py` in both directions, and 12 rejected routes each
naming a distinct `known_wrong_control`. `truth_lint.py` (G48) re-ran `recompute.py` under
`--check` and reported no drift; its replay half is DEFERRED because the bundle carries no
reference app.

## Literals ledger

264 entries. Every one appears verbatim in `instruction.md`; the three `verifier_only`
entries appear in `task.toml` `[verifier].env` and in neither the brief nor any
agent-visible grader.

| Class | Count |
|---|---|
| status | 113 |
| number | 26 |
| route | 28 |
| endpoint | 27 |
| seed_record | 25 |
| env_var | 12 (3 verifier-only) |
| design_phrase | 10 |
| scheme | 9 |
| motion_moment | 8 |
| account | 5 |
| credential | 1 |

## spec/ folder

Seven documents at `_spec/E_itdev_cont_structured-content-platform-vb_20260916_073627/`,
authored in the order 01 -> 05 -> 02 -> 03 -> 04 -> 06 plus `00-decisions.md`.

| Document | Fed |
|---|---|
| `01-PRD.md` | Overview, Core features, Constraints |
| `05-backend-schema.md` | Data model, User roles |
| `02-TRD.md` | Technical requirements |
| `03-app-flow.md` | User flow |
| `04-uiux-brief.md` | UI/UX notes, Front-end specification |
| `06-implementation-plan.md` | nothing: `## Build plan` is not emitted at this variant |
| `00-decisions.md` | the draws, the two enum mappings, the companion carry table |

## Companion carriage (G51)

Source: `C:/Users/Utkarsh/Downloads/sanity_prd.md`, 4,444 lines, recorded in
`_handoff/<project>.sources.json`.

| Measure | Result |
|---|---|
| Colours described by family and tone | 15 of 15 |
| Topics carried | 269 of 269 (5 waived) |
| Enumerated items carried | 722 of 722 (6 waived) |
| Hex values anywhere in the brief | 0 |

Waived topics: `0.2 Normative versus informational`, `43.1 The capture`,
`43.2 Reconstructions, not measurements`, `43.6 What a re-capture should collect`,
`44. Acceptance checklist`. Each is the companion describing itself rather than the
product. Waived items: the `<HEADLINE_FACE>` / `<BODY_FACE>` / `<MONO_FACE>` and host
placeholder rows, the four radius values the companion itself records as drift and does
not reproduce, one hover row that reduces to colour notation, and the `pulse` keyframe row
that reduces to a duration and a curve, both of which the number rule forbids in the brief.

## Grading-window measurement

| Section | Chars | Reference | Flag |
|---|---|---|---|
| core_features | 58,295 | 2,400 | past-slice |
| user_flow | 7,883 | 1,900 | past-slice |
| ui_ux_notes | 14,013 | 1,700 | past-slice |
| constraints | 2,662 | 800 | past-slice |
| user_roles | 3,702 | 1,000 | past-slice |
| overview | 2,255 | 700 | over-reference |
| joined | 88,810 | 8,800 | past-slice |

Length is reported and never failed: generate_instruction 4 retired the cap and
`window_lint.py` measures without judging. The prose past the slice reaches the agent in
full and stops reaching the judge, whose criteria are self-contained and carry their own
`evaluation_rule`. Carrying 722 of 722 enumerated items out of a 4,444-line companion is
what makes the sections long, and G51 is the gate that would fail if they were cut.

## Kit gate log

Every row below is a receipt in `<project>.gates.jsonl`, carrying the SHA-256 of every
input file it examined.

| Gate | Tool | Exit | Verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS |
| G1/G12 | `layout_lint.py` | 0 | PASS |
| G46 | `structure_lint.py` | 0 | PASS |
| G50 | `docker_lint.py` | 0 | PASS |
| G55 | `runtime_deps_lint.py` | 0 | PASS |
| G63 | `secret_lint.py` | 0 | PASS |
| G48 | `truth_lint.py` | 0 | PASS |
| G51 | `source_lint.py` | 0 | PASS |
| G52 | `rubric_context_lint.py` | 0 | PASS |
| G54 | `comment_lint.py` | 0 | PASS |
| G17 | `secret_hygiene_lint.py` | 0 | PASS |
| G11 | `leak_scan.py` | 0 | PASS |
| G33 | `window_lint.py` | 0 | PASS |
| G4/G5 | `contract_lint.py` | 0 | PASS |
| G43 | `prescription_lint.py` | 0 | PASS |
| G44 | `disclosure_lint.py` | 0 | PASS |
| G10 | `no_sdk_lint.py` | 0 | PASS |
| G31 | `determinism_lint.py` | 0 | PASS |
| G14 | `reward_path_lint.py` | 0 | PASS |
| G27/G30 | `rubric_lint.py` | 0 | PASS |
| G41 | `flag_lint.py` | 0 | PASS |
| G56/G57/G58 | `if_lint.py` | 0 | PASS |
| G59/G60 | `codequality_lint.py` | 2 | NOT-APPLICABLE |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 0 | PASS |
| G38 | `kit_selftest.py` | 0 | PASS (32 checks, once per kit revision) |

`G59/G60` is NOT-APPLICABLE because the bundle carries no `evaluation_target: "source"`
criterion: the vendored `recompute.py` renders `judged_criteria` only, so a bundle with
source criteria could not prove its rubric regenerates (stage-3.6). That is a legal,
reported state rather than a silent pass.

`G40` is WARN for one reason and one only: every certification prompt was run by the same
agent that authored the artifact, so each receipt is SELF-ATTESTED. The kit's rule is
owner is not verifier; this is a recorded verdict, never an independent one.

## Prompt receipts (G40, the certification half)

| Prompt | Gate | Verdict | Checks | Findings |
|---|---|---|---|---|
| `task_code_verifier.md` | G3 | VALID | 12 | 0 |
| `QC_spec.md` | G34 | PASS | 15 | 3 |
| `QC_instruction.md` | G34 | PASS | 24 | 5 |
| `qc_toml.md` | G36 | PASS | 120 | 3 |
| `qc_docker.md` | G35 | PASS | 105 | 1 |
| `qc_solution_checklist.md` | G37 | PASS | 0 | 0 |
| `qc_rubric.md` | G53 | PASS | 16 | 1 |

Every finding is a WARN recording a place where a QC prompt predates a later kit decision,
or a deliberate deviation with its reason. No finding is an outstanding defect. The full
text of each is in `<project>.receipts.json`.

The five QC_instruction WARNs, in short: `## Build plan` is absent and
`## Front-end specification` is present in its place (A1, B3); two env-injected timing
seams sit outside the canonical slot list (A8); the Data model states its invariants as
observable properties because G43 forbids the DDL form (C5); and `## Core features` runs
far past the judge's slice because the companion had to be carried in full (C7).

## One deliberate departure from the kit's A5 number rule

`generate_instruction.md` section 4 ("The number rule, DECIDED") makes type the one axis
whose exact family and exact sizes are carried into the brief. The authoring guideline
supplied with this Task Order says the opposite for sizes: font sizes, line heights and
weights are the builder's, and only the accessibility floors are written out. The guideline
is the later and more specific instruction for this run, so it governs here and the
departure is recorded rather than taken quietly.

What changed: `## UI/UX notes` and `## Front-end specification` describe a seven-step scale
by relation (body is the size the rest are measured against; a section heading is roughly
twice body and is the widest jump; the smallest label earns its target area from padding)
instead of naming seven pixel values, and the heading weight is described as the
intermediate cut between the regular and the medium of the same face instead of being
pinned. What did not change: the contrast ratios and the minimum target dimension stay
written out, because the guideline requires an accessibility floor exactly; and every
machine-readable hook, content fact, route, field name, status word and pinned copy string
stays exact. The brief carries no hex, no millisecond, no easing curve and no pixel outside
that one floor.

Ten ledger entries went with the change (`10px` `12px` `13px` `15px` `16px` `24px` `32px`
`400` `425` `500`). G51 is unaffected: the companion's typography section is carried by its
subjects rather than by its numbers, and `source_lint.py` matches on words only.

## Blocking findings

NONE. No spec gap and no harness gap prevented a required test.

Two scope boundaries are stated rather than silently dropped, and both are in
`## Constraints`: webhook deliveries are recorded rather than sent, because the
environment makes no outbound network call at runtime; and scheduling and releases execute
lazily, because the baseline forbids cron, workers and queues.

## Budget

| Field | Value | Reasoning |
|---|---|---|
| `turns_expected` | 180 | a two-half product with a store, an editor, an image pipeline, a migration runner and a public site; the upper rung of the band |
| `tokens_expected` | 6,500,000 | 66 graded assertions across five concerns, 20 workflows, and an 88,000-character brief the agent reads before writing a line |
| Resource tier | Standard | cpus 4, memory 8192 MB, storage 20480 MB, build 900 s, agent 18000 s, verifier 3600 s |
| `difficulty` | `""` | written by calibration, never by the kit |

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. Nothing counts this bundle toward corpus targets until the reference app is
built downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0`
twice. The handoff contract beside this file carries the seven gates the kit cannot run.
