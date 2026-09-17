# Build report: S_local_crud_bilingual-agency-catalogue-vb_20260916_073159

| | |
|---|---|
| Task code | `S_local_crud_bilingual-agency-catalogue-vb_20260916_073159` |
| Task id | `deku/bilingual-agency-catalogue-vb` |
| Cell | solo_founder / local-services / crud-catalog |
| Archetype | `bilingual-agency-catalogue`, variant `b` |
| Service profile | `P2-db-email` (providers: `postgres`, `mailpit`) |
| Variant axes | `critical_depth`, `spec_sections` |
| Language | python |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit | deku-green-field |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Verifier mode | `separate` (kit default since commit 11eaf7b; the agent image keeps the grader runtime anyway, recorded in 00-decisions.md) |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Input

Task Order (five fields plus the two addresses), and one companion document: a
7,685-line, fifty-four-section product requirements specification for a bilingual web
design studio's own site, supplied with the order. `design_direction` is therefore
`companion` (reference/L L.6.1): the drawn direction `dense-ops-console` is recorded in
`_spec/.../00-decisions.md` and does not govern. Honouring it would have been unusually
expensive here -- it asks for one grotesque with tabular numerals at compact density,
against a measured site whose whole character is display type set enormous over a beige
ground at a root size that is a fraction of the window.

The order arrived keyed `domain: portfolio-agency` and `pattern: catalog-browse`, and
the companion's own Section 53.3 states that no enum substitution was necessary. Against
this kit both members are absent from `tools/taxonomy_name.py`: the companion was written
against a different enum revision, and its claim is recorded as wrong rather than quietly
honoured. The order was keyed to `local-services` (the member that names a small studio
selling a service in one city, which is the tier Section 1.2 argues) and `crud-catalog`
(the member that names the filterable-listing-to-detail shape the companion itself calls
the spine of the site). Both substitutions are visible in the task code, and G0 passes on
the rekeyed order.

## Derived design (all drawn from sha256 over the archetype)

| Axis | Value |
|---|---|
| render_model | `mpa-progressive` |
| backend | `Flask + Jinja` |
| frontend | `vanilla progressive enhancement` |
| nav | `command-palette-first` (governs the studio console, which the companion never reached; the public site keeps the measured overlay navigation) |
| work_surface | `table-first` (governs the console's record lists and the lead inbox; the public catalogue keeps its measured three-tier mosaic) |
| create_flow | `multi-step-wizard` (the public enquiry funnel and the console's new-project flow, one address per step) |
| feedback | `optimistic-row` (console row edits only; deliberately not applied to publish) |
| design_direction | `companion` (drawn: `dense-ops-console`) |
| launch_surface | `meta_tags, no_broken_links, privacy_page, security_headers, single_cta` |

## Feature resolution

| Feature | Verdict | Where | Reason |
|---|---|---|---|
| Accounts, sessions, one authorization decision | INCLUDED | `## Core features` Accounts | open signup, two console roles |
| Two locales, separate slugs, no header redirect | INCLUDED | `## Core features` Two languages | companion 2, 18 |
| Catalogue: three tiers, four facets, one read | INCLUDED | `## Core features` The catalogue | companion 10, 25 |
| Case study: eleven blocks, neighbour spacing, both crops | INCLUDED | `## Core features` The case study | companion 11, 22 |
| Home, expertise, agency, contact, footer | INCLUDED | `## Core features` The home route | companion 9, 12 to 16 |
| Record lifecycle, preflight, one publish transaction | INCLUDED | `## Core features` Records | companion 19, 23, 39 |
| Slug history, one-hop redirects, allow-list | INCLUDED | `## Core features` Addresses | companion 34 |
| Enquiry funnel: three branches, idempotency, consent | INCLUDED | `## Core features` The enquiry funnel | companion 29, **an addition to the reference, not a repair** |
| Acknowledgement committed with the lead, over SMTP | INCLUDED | `## Core features` The acknowledgement | companion 32; reference/K K.2 |
| Lead inbox, routing, states, questions as asked | INCLUDED | `## Core features` The lead inbox | companion 30, 33 |
| Applications, scan gate, step-up, log before target | INCLUDED | `## Core features` Applications | companion 24, 31 |
| Consent, retention, withdrawal certificate, append-only log | INCLUDED | `## Core features` Consent | companion 35 |
| Console shell: palette, tables, three creation steps | INCLUDED | `## Core features` The console shell | the 2.10 draws, where the companion is silent |
| Error routes, per-route titles, canonical addresses | INCLUDED | `## Core features` Error surfaces | companion 17, 34 |
| Two compiled three-dimensional award scenes | DROPPED | `## Constraints` | a compiled binary cannot ship and a generated substitute is not gradeable; the stage renders the poster composition the companion already specifies as its degraded state, with the scene layer declared absent |
| Analytics vendor, consent platform, error sink, search index, content delivery network, malware scanner | DROPPED | `## Constraints` | no runtime network; each becomes an in-product component with the same observable contract |
| Three of the five console roles | DROPPED | `## User roles` | owner, publisher and recruiter collapse into `editor` and `commercial`, the two permission shapes the boundary needs |
| External calendar import, connector mirroring, inbound webhooks | DROPPED | `## Constraints` | modelled as data and as observable outcomes, given no surface |
| Build plan | DROPPED | not emitted | non-baseline at variant b |

## Slot obligations

| Slot | Provider | Status | Evidence |
|---|---|---|---|
| backend (db) | `postgres` | MET | `test_simultaneous_submissions_under_one_key_produce_one_lead`, `critical`, asserts exactly one row in the declared datastore under contention |
| email | `mailpit` | MET | `test_the_acknowledgement_reaches_the_mail_server`, `critical`, reads the delivered message out of band through `EMAIL_INBOX_API_URL` |

The email slot is deliberate slot creep against the `crud-catalog` pattern row, which
fixes the db slot alone. The idea's terminal action is that a qualified enquiry "files a
lead into the studio's inbox", and companion Sections 29.5 and 32.2 commit the
acknowledgement inside the lead's own transaction. With no mail slot that clause is
unobservable and the idea's last sentence is ungraded. Recorded in `00-decisions.md` and
as a justified WARN under B1 in the QC_spec and QC_instruction receipts.

## Grading layer

| | |
|---|---|
| Workflows | 16 (solo_founder band 10 to 16) |
| Browser substeps | 74 |
| pytest substeps | 63 |
| Critical substeps | 23 |
| Non-happy-path ids | `cannot`, `denied`, `empty`, `expired`, `invalid` |
| pytest module | `tests/test_output.py`, one module, 63 tests |
| Rubric criteria | 22, all positive |
| Judgment obligations graded | 33 of 33 ui-tagged checklist items, partitioned with no double claim |
| Checklist items | 259 across ten section codes |

Rubric dimension shares: `instruction_following` 0.31, `functionality` 0.27,
`ui_visual` 0.13, `ux_flow` 0.12, `motion` 0.06, `accessibility` 0.06,
`responsiveness` 0.06. Every one is inside the 0.10 band `rubric_lint.py` enforces, and
every dimension carries at least two criteria.

## Grading window

| Section | Characters | Reference |
|---|---|---|
| core_features | 43,717 | 2,400 |
| ui_ux_notes | 9,248 | 1,700 |
| user_flow | 8,325 | 1,900 |
| overview | 4,631 | 700 |
| constraints | 2,736 | 800 |
| user_roles | 2,670 | 1,000 |

Reported, never failed. The operator's instruction for this run lifts the per-section
caps explicitly; the companion states more graded rules than the judge's window holds;
`judge_score` never touches reward; and `generate_instruction.md` 4 says plainly not to
cut a real rule to fit. Every judged criterion carries its own facts, so the judge does
not depend on the sliced text -- G52 proves that mechanically.

## Literals ledger

249 literals: 4 accounts, 1 credential, 9 environment variables (2 verifier-only),
47 routes, 29 endpoints, 28 statuses and enum members, 5 numbers, 81 pinned copy strings
and seeded records, 29 schemes and field names, 6 motion moments, 10 design phrases.
Full file at `_handoff/S_local_crud_bilingual-agency-catalogue-vb_20260916_073159.literals-ledger.json`. G6 proves the bijection in both
directions against `instruction.md`, `tests/conftest.py` and `tests/test_output.py`.

## Companion coverage (G51)

| | |
|---|---|
| Colour anchors | 17 of 17 carried by family and tone; no hex appears anywhere in the brief |
| Topics | 376 of 376 carried |
| Enumerated items | 1,930 of 1,930 carried |
| Waivers | 71 substrings, every one a pixel value, a cubic-bezier literal, a CSS class name, a named animation identifier, a named scroll library, a component-tree name, a three-dimensional material recipe, or a companion meta-table about its own taxonomy |

Every waiver is a deliberate drop under the kit's own rules rather than an omission: the
number rule forbids a hex, a pixel or a duration anywhere in the brief; INV9 and G43
forbid naming an implementation mechanism; and the operator's instruction for this run
forbids exact pixels, colour codes, animation names and function names by name. The
waiver list is recorded in the gate receipt.

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
| G38 | `kit_selftest.py` | PASS |
| G49 | `diversity_lint.py` | PASS |
| G42 | `corpus_overlap.py` | NOT-APPLICABLE, no second complete comparable bundle in this output root |
| G26 / G61 | `corpus_report.py` | NOT-APPLICABLE, no admissible bundle yet. This is not a pass |

## Prompt receipts (G40)

Every certification prompt carries a current, bundle-bound receipt with the scorecard its
own registry declares: `task_code_verifier.md` (G3, 12 checks), `QC_spec.md` (G34, 15),
`QC_instruction.md` (G34, 24), `qc_toml.md` (G36, 120), `qc_docker.md` (G35, 105),
`qc_solution_checklist.md` (G37), `qc_rubric.md` (G53, 16). Three generator prompts carry
receipts too: `generate_instruction.md`, `toml_generator.md`, `docker_generator.md`.

**Every one is SELF-ATTESTED.** The kit's rule is owner is not verifier; one agent
authored these artifacts and ran the reviewers, so these are recorded verdicts, never
independent ones. An independent QC pass is the first thing a reviewer should add.

Fourteen checks across the seven registries resolved other than PASS, each with its
evidence in `_handoff/S_local_crud_bilingual-agency-catalogue-vb_20260916_073159.receipts.json`. The recurring reasons are the retired
baseline `## Build plan`, the settled no-numbers rule for design values, the deliberate
email-slot creep, and the placeholders the companion's own copy deck interpolates at run
time.

## Blocking findings

None mechanical. Three brief obligations are stated in `instruction.md` and carried by no
channel, because no channel can observe them: the credentials file at
`/app/USER_README.md`, the reserved `.browser_screenshots/` and `.downloads/` directories,
and the no-edge-functions / no-persistent-volumes clause. They are App Contract clauses
enforced by review (G3) rather than product features. This is OPEN-DECISIONS D-H, recorded
rather than fabricated into a citation.

## Budget

`turns_expected = 220`, `tokens_expected = 3200000`. The reasoning: eleven must-have
features against the companion-backed 6 to 10 cap, eighteen public route shapes across two
locales plus fifteen console routes, 29 API endpoints, 25 entities, an enquiry funnel with
three branches and an address per step, and a publish transaction that spans five stores.
That is well above the six-feature baseline the standard band was drawn for, and
`reference/G` G.2.1 says plainly to raise the budget with the feature count rather than
pretend eleven features build in the time six do.

## Kit revision

Built against `deku-green-field` at commit `806eb0a`. During this run the kit tree was
relocated to `GreenField-GenKit2/genkit/deku-green-field/`, which makes
`GreenField-GenKit2/Output/` a genuine sibling of the kit: CON-1 now holds at the
operator's requested path, and the whole sweep ran there with no relocation.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference application. Build one downstream from
`solution/checklist.md`, then run the handoff gates in
`_handoff/S_local_crud_bilingual-agency-catalogue-vb_20260916_073159.handoff.md`.
