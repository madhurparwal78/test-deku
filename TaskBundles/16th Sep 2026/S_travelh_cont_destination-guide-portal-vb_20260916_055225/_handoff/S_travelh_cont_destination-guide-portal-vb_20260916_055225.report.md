# Build report: S_travelh_cont_destination-guide-portal-vb_20260916_055225

## Identity

| field | value |
|---|---|
| task code | `S_travelh_cont_destination-guide-portal-vb_20260916_055225` |
| task id | `deku/destination-guide-portal-vb` |
| uuid_v5 | `ec6c0f57-7105-591d-99a4-5ad6e18a46fe` |
| cell | solo_founder / travel-hospitality / content-publishing |
| service_profile | `P4-db-storage` |
| providers per slot | backend = `postgres`, storage = `minio` |
| variant | `b` |
| variant_axes | `critical_depth`, `spec_sections` |
| language | typescript |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 |
| kit revision | GreenField-GenKit2 @ b3d0577 |
| vendored grader | 0.22.0 |
| target schema | 1.4 |
| authors | `utsav.jain@ethara.ai` (QL), `mohd.rafey@ethara.ai` (contributor) |
| companion document | `Drive_PRDs/16_sept/keralatourism_prd.md`, 1,926 lines |

## Derived-design draws

Every draw is SHA-256 over the archetype `destination-guide-portal`, never Python's builtin hash.

| axis | value | note |
|---|---|---|
| render_model | `ssr-islands` | governs |
| backend | `Fastify` | governs |
| frontend | `Nuxt 3` | governs |
| design_direction | `companion` | a companion document beats the draw (reference/L S-L.6.1); the raw draw was `terminal-mono` |
| nav | `top-nav` | override: the companion measures a fixed top header; the raw draw was `sidebar-nav` |
| work_surface | `card-grid` | draw and companion agree |
| create_flow | `dedicated-route` | draw and companion agree |
| feedback | `toast` | override: the companion specifies a corner toast stack; the raw draw was `full-page-confirmation` |
| launch_surface | `alt_text,mobile_viewport,no_broken_links,privacy_page,terms_page` | the reference/O S-O.3 draw |

## Feature resolution

| candidate | verdict | where it landed | reason |
|---|---|---|---|
| Draft invisibility with mediated object reads | INCLUDED | `## Core features` rules 1 to 5 | the pattern's critical focus |
| Objects in the store, under the pinned key scheme | INCLUDED | `## Core features` rules 6 to 9 | storage slot |
| The events calendar and its server-side expiry | INCLUDED | `## Core features` rules 10 to 13 | the companion's third graded behaviour |
| The place index and a place entry | INCLUDED | `## Core features` rules 14 to 18 |  |
| Themed collections | INCLUDED | `## Core features` rules 19 to 21 |  |
| The guide library and the photo gallery | INCLUDED | `## Core features` rules 22 to 26 |  |
| The editor desk | INCLUDED | `## Core features` rules 27 to 33 |  |
| Publish and return to draft | INCLUDED | `## Core features` rules 34 to 36 |  |
| The standing pages | INCLUDED | `## Core features` rules 37 to 40 | the drawn launch surface |
| Auth | INCLUDED | `## Core features` rules 41 to 43 |  |
| Editor-created events | DROPPED | - | the companion gives the desk no event endpoint, so events are seed-only |
| Editor-created collections | DROPPED | - | the companion fixes the three collections as seeded |
| Visitor accounts, booking, payment, email, search | DROPPED | `## Constraints` | out of scope in the companion's own section 1 |
| A build order | DROPPED | - | generate_instruction.md S-2.1 keeps `## Build plan` out of the emission |

## Slot obligations

| slot | provider | state | observed by |
|---|---|---|---|
| backend | `postgres` | MET | `test_published_entry_fields_survive_a_reread`, `test_seed_holds_the_eight_published_places_and_one_draft`, `test_two_concurrent_publishes_of_one_slug_admit_one_winner` (critical) |
| storage | `minio` | MET | `test_uploaded_picture_object_exists_in_the_bucket` (critical), `test_uploaded_object_key_follows_the_gallery_scheme`, `test_unpublished_entry_objects_stop_resolving_at_once` (critical) |

## Grading surface

| measure | count | note |
|---|---|---|
| workflows | 15 | solo_founder band is 10 to 16 (reference/B B.3) |
| browser substeps | 47 |  |
| pytest substeps | 68 | one per test, bijective (G8) |
| critical substeps | 12 | every declared slot and every permission boundary |
| non-happy-path workflow ids | 5 | visitor_filter_matching_nothing_shows_an_empty_state, visitor_cannot_reach_a_draft_place_denied, draft_picture_bytes_are_denied_to_a_visitor, unauthenticated_desk_request_is_denied, editor_publish_is_refused_when_invalid |
| pytest module | `tests/test_output.py` | 68 tests, one module (CON-2, G46) |
| checklist items | 855 | capability 156, constraint 193, contract 21, data 30, literal 223, role 16, ui 216 |
| judged criteria | 15 | 14 positive, 1 negative |
| reference rubric items | 17 | compiled-weight share 0.8657, floor 0.60 |
| literals ledger | 186 | 1 verifier-only (`DB_ADMIN_URL`) |

### Judged rubric, per dimension

| dimension | criteria | positive score | share | target | difference |
|---|---|---|---|---|---|
| instruction_following | 3 | 11 | 0.250 | 0.3 | 0.050 |
| functionality | 4 | 12 | 0.273 | 0.25 | 0.023 |
| ux_flow | 2 | 4 | 0.091 | 0.15 | 0.059 |
| ui_visual | 3 | 8 | 0.182 | 0.15 | 0.032 |
| motion | 1 | 3 | 0.068 | 0.05 | 0.018 |
| accessibility | 1 | 3 | 0.068 | 0.05 | 0.018 |
| responsiveness | 1 | 3 | 0.068 | 0.05 | 0.018 |

Positive total 44; negative magnitude 3, cap 132. `task completion` is 10/15, inside the 60 to 80 percent band.

## Grading window

| section | chars | reference | flag |
|---|---|---|---|
| Core features | 11637 | 2400 | past-slice |
| User flow | 5370 | 1900 | past-slice |
| UI/UX notes | 5878 | 1700 | past-slice |
| Constraints | 1474 | 800 | over-reference |
| User roles | 1497 | 1000 | over-reference |
| Overview | 1265 | 700 | over-reference |
| joined six | 27121 | 8800 | past-slice |

Length is reported, never failed (G33). `## Core features` runs past the 2,500-char slice, so the judge reads its first 2,500 characters; the draft-invisibility and object-store rules are front-loaded there deliberately, and the tail reaches the agent in full. The unbudgeted `## Front-end specification` carries the companion's measured design content.

## Companion carriage (G51)

20/20 source colours described by family, tone and shade; 137/137 topics carried; 295/295 enumerated items carried, with ten declared waivers.

Every sweep must pass the same ten `--waive` tokens, because `revalidate.py` re-reads only `sources` from `_handoff/<project>.sources.json` and never a waiver list. The tokens are recorded in that file and in `_spec/<code>/00-decisions.md`.

## Literals ledger

| class | values | sample |
|---|---|---|
| account | 1 | `editor@example.com` |
| credential | 1 | `deku-demo-pw-2026` |
| design_phrase | 87 | `Playfair Display`, `IBM Plex Sans Condensed`, `Georgia, "Times New Roman", serif`, `system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif`, ... |
| endpoint | 20 | `/api/health`, `/api/entries`, `/api/entries/{slug}`, `/api/collections`, ... |
| env_var | 8 | `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, ... |
| motion_moment | 8 | `long reveal`, `nudge`, `fade out`, `drawer slide`, ... |
| number | 4 | `24`, `240`, `20000`, `4173` |
| route | 13 | `/destination`, `/destination/<slug>`, `/collection/<slug>`, `/event`, ... |
| scheme | 4 | `entries/<entry_id>/gallery/<sha256_of_bytes>.<ext>`, `entries/<entry_id>/brochure/<sha256_of_bytes>.pdf`, `regional/<brochure_id>/<sha256_of_bytes>.pdf`, `entries/4/gallery/9f2a...d0.jpg` |
| seed_record | 35 | `visit@example.com`, `alder-cove`, `thistle-bay`, `rook-hollow`, ... |
| status | 5 | `draft`, `published`, `404`, `403`, ... |

Full ledger: `_handoff/<code>.literals-ledger.json`. Every non-verifier value appears verbatim in `instruction.md`; `DB_ADMIN_URL` is verifier-only and appears in `task.toml` `[verifier].env` alone (INV4).

## Authoring documents

| document | instruction.md sections it fed |
|---|---|
| `00-decisions.md` | the draws, the overrides, the residual judgment calls, the companion carry table, the ten waivers |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | authoring-side only; `## Build plan` is not emitted |

They live at `Output/16sept-keralatourism/_spec/S_travelh_cont_destination-guide-portal-vb_20260916_055225/`, outside the bundle (CON-5).

## Kit gate log

Rendered from `_handoff/<code>.gates.jsonl`, one row per gate, each carrying the SHA-256 of every input file it read. No verdict in this table was typed by hand (ISSUES C-02).

| gate | tool | exit | verdict | elapsed |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | 0.04s |
| G1/G12 | `layout_lint.py` | 0 | PASS | 0.03s |
| G46 | `structure_lint.py` | 0 | PASS | 0.04s |
| G50 | `docker_lint.py` | 0 | PASS | 0.04s |
| G55 | `runtime_deps_lint.py` | 0 | PASS | 0.04s |
| G63 | `secret_lint.py` | 0 | PASS | 0.02s |
| G48 | `truth_lint.py` | 0 | PASS | 0.18s |
| G51 | `source_lint.py` | 0 | PASS | 0.04s |
| G52 | `rubric_context_lint.py` | 0 | PASS | 0.03s |
| G54 | `comment_lint.py` | 0 | PASS | 0.02s |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | 0.03s |
| G11 | `leak_scan.py` | 0 | PASS | 0.03s |
| G33 | `window_lint.py` | 0 | PASS | 0.03s |
| G4/G5 | `contract_lint.py` | 0 | PASS | 0.03s |
| G43 | `prescription_lint.py` | 0 | PASS | 0.05s |
| G44 | `disclosure_lint.py` | 0 | PASS | 0.03s |
| G10 | `no_sdk_lint.py` | 0 | PASS | 0.05s |
| G31 | `determinism_lint.py` | 0 | PASS | 0.06s |
| G14 | `reward_path_lint.py` | 0 | PASS | 0.03s |
| G27/G30 | `rubric_lint.py` | 0 | PASS | 0.03s |
| G41 | `flag_lint.py` | 0 | PASS | 0.04s |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | 0.02s |
| G59/G60 | `codequality_lint.py` | 2 | ? | 0.03s |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | 0.05s |
| G6 | `fixture_lint.py` | 0 | PASS | 0.06s |
| G24 | `coverage_map.py` | 0 | PASS | 0.07s |
| G37 | `checklist_qc.py` | 0 | PASS | 0.06s |
| G39 | `rubric_align_lint.py` | 0 | PASS | 0.15s |
| G28/G29 | `channel_lint.py` | 0 | PASS | 0.04s |
| G40 | `prompt_receipt_lint.py` | 1 | FAIL | 0.03s |
| G0/INV5 | `vendor_check.py` | 0 | PASS | 0.02s |
| G47 | `output_qc.py` | 1 | FAIL | 0.04s |

30/32 green; RED: G40, G47

### Corpus-level gates

| gate | tool | verdict | note |
|---|---|---|---|
| G26/G61 | `corpus_report.py` | NOT-APPLICABLE | no admissible bundle in this output root yet; 1 minted, 1 unproven |
| G42 | `corpus_overlap.py` | NOT-APPLICABLE | cross-archetype overlap needs two or more bundles; this root holds one |
| G49 | `diversity_lint.py` | NOT-APPLICABLE | the concentration check needs two or more bundles; this root holds one |
| G38 | `kit_selftest.py` | PASS | 32 checks; run once per kit revision, not per task |

## Prompt receipts (G40)

| prompt | gate | verdict | verifier | checks | FAIL | WARN |
|---|---|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | qc-instruction-reviewer-c3 | 24 | 0 | 9 |
| `QC_spec.md` | G34 | FAIL | qc-spec-reviewer-c3 | 15 | 1 | 2 |
| `qc_docker.md` | G35 | PASS | qc-docker-reviewer-c2 | 105 | 0 | 0 |
| `qc_rubric.md` | G53 | FAIL | qc-rubric-adjudicator-c3 | 16 | 7 | 1 |
| `qc_solution_checklist.md` | G37 | FAIL | qc-checklist-adjudicator-c3 | 17 | 9 | 2 |
| `qc_toml.md` | G36 | PASS | qc-toml-reverifier-c4 | 120 | 0 | 7 |
| `task_code_verifier.md` | G3 | VALID | task-code-verifier | 12 | 0 | 0 |

### Findings carried by the reviewers

Abridged. Every finding, verbatim, is in `_handoff/<code>.receipts.json`, which is the artifact G40 reads. A finding is the reviewer's own words at the cycle it was raised and is never edited afterwards, so an earlier cycle's finding can describe bytes a later repair has replaced. One does: `qc_docker` F-6 reads the MinIO root user as `minioadmin7f3a`, a value this bundle carried for one cycle and no longer has anywhere. `qc_toml` cycle 3 ENV-006 re-measured it and passes on `minioadmin`; F-6 is superseded. A finding raised before the kit `806eb0a` alignment also spells the pytest module `test_pytest.py`, which commit `da24d3b` renamed to `test_output.py`; the file the finding is about is the same one under its new name.

- `QC_instruction.md` [CYCLE-2 REPAIRS · verified against current bytes] All five hold. C2 per-state counts: `GET /api/desk/entries` returns "a top-level JSON array of the entries the state filter selects" and the new `GET /api/desk/entries/counts` returns `{"all": <n>, "published": <n>, "draft": <n>}`, named in rule 28 as the source of ...
- `QC_instruction.md` [MECHANICAL CORROBORATION] `contract_lint.py` PASS (G4/G5 App Contract verbatim + provider presence), `disclosure_lint.py` PASS (G44), `prescription_lint.py` PASS (G43), `if_lint.py` PASS (G56/G57/G58). No `{{…}}`, `TODO`, `TBD`, `FIXME`, `<ASSIGN…>`, `[insert…]`, canary text, `spec/` reference, or stale "different ...
- `QC_instruction.md` [A1 · WARN] `## Build plan` is absent. The other ten required H2s are present in order, plus the unbudgeted `## Front-end specification`. Not failed: `generate_instruction.md` §2.1 states "`## Build plan` is NOT baseline — 6/6 shipped human-authored reference briefs omit it, a build plan is a work order not a specif...
- `QC_instruction.md` [B3 · WARN] Two of the three difficulty-lever sections are present (`## Technical requirements`, `## Data model`); the third, `## Build plan`, is absent by design at baseline — the same prompt drift recorded at A1, not a missing lever.
- `QC_instruction.md` [B1 · WARN] The `content-publishing` row is honoured — slots `db + storage`, providers `PostgreSQL` + `MinIO`, two roles (`author`→`editor`, `reader`→`visitor`, count and permission shape kept), critical focus carried — but the `solo_founder` modifier "signup is **open**" is departed: "Signup is closed. A `visitor` ...
- `QC_instruction.md` [C1 · WARN] Rules 17, 19–21, 25, 26 and 37–40 are composition or presence rules and carry no negative case. Each is still individually verifiable from outside (a route, a response body, or a rendered surface), and every rule that can be refused — 18, 27, 31, 32, 34, 35, 42 — names its rejection outcome as a client-s...
- `QC_instruction.md` [C2 · WARN] Two request defaults are unpinned: `GET /api/desk/entries` is documented only as `?state=all|published|draft` and `GET /api/entries` only as `sort=name|recent&…`, so neither states what a call with the parameter absent returns (rule 28 implies both states for the desk list; the index's default grid order...
- `QC_instruction.md` [C3 · WARN] The footer's third column is named twice, differently: "**Board** holds `Privacy`" and then "The `Enquiries` string is the Board column's heading over the enquiry address rather than a link of its own", while the copy deck pins only `Enquiries` (`footer enquiries heading`) and carries no string for `Plac...
- `QC_instruction.md` ... 4 further finding(s); the full text is in `_handoff/<code>.receipts.json`
- `QC_spec.md` {'id': 'G2', 'severity': 'MAJOR', 'defect': 'A graded API endpoint is one-sided (brief only), and the spec misattributes its output to a different endpoint.', 'evidence': 'The brief grades `GET /api/desk/entries/counts` twice: `## Core features` rule 28 - "the three filter counts come from `GET /api/desk/entries/cou...
- `QC_spec.md` {'id': 'G2', 'severity': 'MAJOR', 'defect': 'A graded response-field literal is one-sided (brief only) - the same class of defect the `published_count` repair just closed.', 'evidence': 'Brief `## Core features` rule 28: "The picture count is carried as `picture_count` on each row of the response behind it", repeate...
- `QC_spec.md` {'id': 'S8', 'severity': 'MINOR', 'defect': 'The cycle-2 repair row in the identity-recast table is the one row not indented into the table, so the tenth name risks rendering outside it.', 'evidence': '00-decisions.md line 50 begins at column 0 - "| the name the desk journeys write, held by no entry | `Ferrow Sands`...
- `QC_spec.md` {'id': 'S5', 'severity': 'MINOR', 'defect': "04-uiux-brief.md does not name the five breakpoint tiers, although 00-decisions.md's companion carry table certifies that it does.", 'evidence': '00-decisions.md carry row: "| 3.4 Layout and breakpoints | ## Front-end specification | five tiers named, widths as words |". ...
- `QC_spec.md` {'id': 'S5', 'severity': 'NOTE', 'defect': 'Prompt-level staleness, carried over from cycle 2, not a defect in the bundle.', 'evidence': 'QC_spec.md S5 demands a "hex palette" and motion "`150ms` / `250ms` / `cubic-bezier(0.16, 1, 0.3, 1)`", which reference/G G.2 forbids for this doc: "palette by role/family/tone (n...
- `QC_spec.md` {'id': 'S2', 'severity': 'NOTE', 'defect': 'Prompt-level staleness, carried over from cycle 2, not a defect in the bundle.', 'evidence': 'QC_spec.md S2 states "3-6 must-have features" without the companion clause; reference/G G.2.1 states "3-6 must-have features for a bare Task Order. 6-10 when a companion document ...
- `QC_spec.md` {'id': 'B1', 'severity': 'NOTE', 'defect': 'The solo_founder open-signup modifier is departed from rather than applied; recorded, and judged conformant on purpose.', 'evidence': 'reference/B B.1 content-publishing row gives slots "db + storage", providers "PG + MinIO", roles "author, reader", critical focus "Object ...
- `qc_docker.md` F-1 (Informational, kit-level, no bundle change): DEP-012 and G50 cannot both be satisfied for this package set, and the cycle-1 answer reproduces exactly. Inlining the 21 Chromium package names measures 226 and 229 characters against tools/docker_lint.py MAX_LINE = 200; with MAX_APT_UPDATE = 2 and the mandatory `rm...
- `qc_docker.md` F-2 (Informational, kit-level, no bundle change): RUN-005 versus the mandated SKELETON. prompts/docker_generator.md line 143 prescribes `ARG NODE_MAJOR` and the nodesource `node_${NODE_MAJOR}.x nodistro main` channel, so the floating patch level is a Tier-1 shape the bundle is required to reproduce, and Section 3 sa...
- `qc_docker.md` F-3 (Informational, kit defect in the reviewing prompt): prompts/qc_docker.md defines DEP-015 twice with two unrelated checks -- a Medium `--break-system-packages` / pip-fallback rule in section B and a Critical compiled-language multi-stage rule further down the same table -- while the registry carries the id once....
- `qc_docker.md` F-4 (Informational, kit wording contradiction): CMP-011 reads "Any service has a `ports:` key" while CMP-022 (Critical) requires `ports` on main, and prompts/docker_generator.md resolves it -- line 222 scopes the ban to sidecars, line 202 mandates the main block, and line 435's own checklist then says "no ports: on ...
- `qc_docker.md` F-5 (Informational, kit-level, affects every future bundle): the kit's own provider fragments still carry the two defects this cycle repaired. environment/providers/postgres/service.yaml and environment/providers/minio/service.yaml both set `restart: unless-stopped`, which CMP-019 fails as Medium, and the postgres f...
- `qc_docker.md` F-6 (Informational, no action): the minio fragment sets MINIO_ROOT_USER `minioadmin` while this bundle uses `minioadmin7f3a`. The bundle is internally consistent -- both task.toml env tables carry STORAGE_ACCESS_KEY minioadmin7f3a and the compose healthcheck and minio-init chain use the same value -- so CMP-005 hold...
- `qc_docker.md` High findings outstanding: NONE. All three cycle-1 High flags are closed -- CMP-021 by the repaired bytes, DEP-012 and RUN-005 by answers this cycle accepts and records as kit-level findings (F-1, F-2). No finding in this report carries Critical, High, Medium or Low severity against the bundle; F-1 through F-6 are I...
- `qc_rubric.md` ABORT: rubric QC unrecoverable after 3 cycles: RC-01, RC-04, RC-07, RC-09, RC-11, RC-12, RC-15. Cycle 3 closed four of the seven cycle-2 findings (RC-03, RC-08, and the RC-16 comma tic) but left three open and opened two new ones, so the loop did not converge inside the three cycles GENKIT-PLAN_main.md 15.1 allows. ...
- `qc_rubric.md` RC-01 coverage 215/215 judgment obligations claimed mechanically, 82 by the rubric and 133 by browser substeps, with no id claimed twice. The claim is not the look. G24's citation-honesty check, coverage_map.check_cov_earned, only inspects a citation that carries `evidence`, and coverage_map._cite passes evidence=""...
- `qc_rubric.md` RC-01 R8 (tests/rubric.json R8; grounding.yaml judged_criteria R8) grades a print preview and nothing else after the cycle-2 fix dropped its on-screen reading-column clause, yet it still owns C-UX-26 `Density reads as spacious, with a generous reading measure.`, C-UX-42 `Headings descend without skipping a level.` a...
- `qc_rubric.md` RC-01 R15 grades one card per row at phone width and nothing else, yet it owns C-FE-110 `The triptych is three cards in a row on a wide screen, stacked below the `md` tier.`, C-FE-130 `The place grid is three cards across at `xl`, two at `md`, one below.`, C-FE-159 `The library grid is four cards across at `xl`, thr...
- `qc_rubric.md` RC-01 R1 owns C-FE-90 `The home header motion layer is muted, looping, playing inline, with no controls.` and its rule never mentions muted, looping, inline or controls. The one grader that does observe those four flags, test_home_header_media_declares_a_poster_and_defers_play in tests/test_pytest.py, cites C-TR-41,...
- `qc_rubric.md` RC-01 R7's only cited obligation is C-FE-150 `The month groups are real headings so a screen reader jumps between months.` R7 grades whether a month with no event gets a heading, which is a different question; nothing in R7's criterion or rule decides whether the groups are real heading elements. Smallest fix: cite ...
- `qc_rubric.md` RC-01 the routing of C-FE-188, C-FE-189 and C-FE-190 to test_five_named_breakpoints_drive_the_pinned_column_counts is not honest. The test sweeps only /destination, /brochures and /photo-gallery. C-FE-188 is the featured row on `/` and C-FE-190 is the event row on `/event`; the test visits neither route, so two of t...
- `qc_rubric.md` RC-01 the reduction on C-CF-04 `The app applies the published filter once in the data layer.` and C-FE-186 `A view receiving an entry carries no state check of its own.` is defensible in principle and dishonest as shipped. INV6 bars reading the agent's source, so only the effect is observable, and the kit provides e...
- `qc_rubric.md` ... 23 further finding(s); the full text is in `_handoff/<code>.receipts.json`
- `qc_solution_checklist.md` H1-01 CONFIRMED GAP, four exact copy strings have no item at all. instruction.md:1084 the row `| events call to action | See the full calendar |`, instruction.md:1086 the guide promotion body `A printed companion to every place in this guide, with maps, seasons and the roads between them. Free to download, made to b...
- `qc_solution_checklist.md` H1-03 CONFIRMED INVENTION, C-FE-233 reads "The lightbox link label carries the words `Read about` ahead of the place name". instruction.md:1129 pins the fixed string `Read about this place`; no place name is interpolated anywhere in the brief. The item invents an interpolation the spec closed and, by naming only `Re...
- `qc_solution_checklist.md` H1-04 UNPINNED LITERAL, `picture_count` is named twice in the brief and pinned nowhere in the checklist. instruction.md:161 reads `The picture count is carried as `picture_count` on each row of the response behind it`, and instruction.md:1238 repeats it in the API shapes row for `GET /api/desk/entries`. The string `...
- `qc_solution_checklist.md` H1-04 UNPINNED LITERAL, the request and response keys of `POST /api/desk/uploads` are pinned in the brief and absent from the checklist. instruction.md:1245 gives the request body `{"entry_id","kind","filename","content_type"}` and the response `{"url","method","headers","object_key"}`. C-DC-43 names `object_key` al...
- `qc_solution_checklist.md` H2-01 REJECTED PAIRING, wrong ask. C-DC-38 reads "The app answers `GET /api/desk/entries` with every entry in both states carrying a count per state", cited `src: Deployment contract, API shapes table`. The row it cites, instruction.md:1238, returns `a top-level JSON array of the entries the state filter selects, ea...
- `qc_solution_checklist.md` H2-02 PARTIAL CAPTURE, nine items pin only the opening of a string the brief marks exact, so a build that ships the fragment alone passes the item. C-UF-48 `a message beginning `Published.`` against instruction.md:1162 `Published. It is live now.` (also journey 9, instruction.md:281). C-UF-50 `beginning `Returned to...
- `qc_solution_checklist.md` H2-04 SCOPE DRIFT, C-CF-180 reads "The app answers `GET /api/desk/entries/{id}` with one draft entry carrying its `images`, its guide document". instruction.md:1240 reads `one entry in either state with its `images` and its `brochure``. The item narrows the brief's `either state` to `draft`, which is the half of the...
- `qc_solution_checklist.md` H3-03 NEW, a table cell carrying a second requirement with no item. The `GET /api/desk/entries` row at instruction.md:1238 states both the `?state=all|published|draft` selector and the per-row field list `id`, `slug`, `name`, `state`, `themes`, `picture_count`, `updated_at`. No item states that field list; the only ...
- `qc_solution_checklist.md` ... 16 further finding(s); the full text is in `_handoff/<code>.receipts.json`
- `qc_toml.md` VERIF-001 (re-verified against the current prompt bytes, PASS): [verifier].environment_mode is "separate", which is now the exact value the row demands; toml_generator.md 10.1 emits the same string and generate_instruction.md 2.9 states the matching consequence (the grader ships its own image built from tests/Docker...
- `qc_toml.md` INST-002/INST-006 (Informational, no defect): environment/Dockerfile still carries the grader dependency pins (pytest 8.4.1, pytest-json-ctrf, httpx, psycopg[binary], boto3, pyyaml, playwright + chromium) and PYTHONPATH=/tests, which 01-OUTPUT-CONTRACT.md now describes as needed only "under shared mode". Judgment: R...
- `qc_toml.md` SCHEMA-005 (Informational, kit contradiction, not a bundle defect): toml_generator.md 10.5b requires [metadata].rubric_version = "1", and this task.toml carries no such key. The key is absent from 11's canonical template, which 9 names as "the single owner of the field list"; validate_task.py META_REQUIRED does not ...
- `qc_toml.md` SCHEMA-011 (Informational, sanctioned by a non-template authority): [delivery] and [delivery.images] are emitted and neither appears in the 11 canonical template, whose fail condition is any field/section/key the template does not define. They are nonetheless required elsewhere in the same authority: toml_generator....
- `qc_toml.md` SCHEMA-013 (Informational, consequence of SCHEMA-011): the section sequence is [task], [metadata], [metadata.services], [agent], [environment], [environment.healthcheck], [verifier], [delivery], [delivery.images], [[artifacts]]. Every section the 11 template names is in the template's exact relative order; the devia...
- `qc_toml.md` TAX-008 (Informational, as the row itself directs): archetype "destination-guide-portal" cannot be shown globally unique from the supplied inputs. The only corpus record reachable from here is Output/16sept-keralatourism/ledger.jsonl, which holds this one row; no corpus-wide archetype index is among the inputs. Reco...
- `qc_toml.md` BENCH-005 (Informational, vacuous by construction): difficulty is the empty calibration placeholder "" that BENCH-006 and TAX-010 both mandate, so there is no declared difficulty for the complexity signals to contradict and the row cannot be decided as written. On the determinate legs the file is self-consistent: 2 ...
- `qc_toml.md` COV-003 (Informational, deliberate and documented): the Implementation Plan's phased build order and per-phase exit criteria (_spec/06-implementation-plan.md, nine phases) are represented in the task.toml only indirectly, through the difficulty/budget tier, and carry no buildplan token in spec_sections_given. This i...
- `qc_toml.md` ... 2 further finding(s); the full text is in `_handoff/<code>.receipts.json`

## Certification state after the three cycles

The kit allows three repair cycles (GENKIT-PLAN_main.md 15.1). All seven prompts ran to the end of that budget. Three closed clean: `QC_instruction` (0 FAIL), `qc_toml` (0 FAIL, 120/120) and `qc_docker`, with `task_code_verifier` VALID. The other three ended as below, and the receipts carry every finding verbatim.

| prompt | verdict | state |
|---|---|---|
| `QC_spec` | FAIL, 1 check (G2) | All four findings repaired after the review closed: the `GET /api/desk/entries/counts` row and the corrected `GET /api/desk/entries` contract in `03-app-flow.md`, `picture_count` named in `05-backend-schema.md`, the five tier names in `04-uiux-brief.md`, and the unindented recast row here. NOT re-reviewed. |
| `qc_solution_checklist` | FAIL, 9 checks | It overturned all thirteen cycle-2 finding classes and raised eleven new ones, every one repaired afterwards: four unpinned copy strings, `picture_count`, the upload and login body shapes, the desk-row field list, `C-FE-233`'s invented interpolation, `C-DC-38`'s wrong ask, `C-CF-180`'s narrowed scope, and the 47-item `para N` locator drift. NOT re-reviewed. |
| `qc_rubric` | FAIL, 7 checks -- **ABORT** under 15.1 | The loop did not converge in three cycles. What it found that was mechanically checkable is fixed (see the row below). What remains open is the re-faceting work: RC-04's seven shared (anchor, facet) pairs between the rubric and the deterministic channels, four of which this cycle's own RC-12 repair created by writing a grader for an observation a criterion still grades; and RC-01's item ownerships on R1, R7, R8 and R15. The reviewer's remedy for several is to delete the criterion, which would break the dimension budget RC-13 verifies as intact, so it is recorded rather than guessed at. This bundle is NOT rubric-certified. |

`qc_rubric` also caught three defects no gate could see, all now fixed and re-swept:

| defect | what was done |
|---|---|
| `tests/workflows.yaml` did not parse | five `do:` scalars carried an unquoted colon, so `yaml.safe_load` raised at line 105. `workflow_lint.py` (G7/G8/G9/G32/G45) scans the file line by line with regexes and never parses it, so every gate stayed green over a file the runtime `run_workflows.py` could not open. The colons are gone and `build_workflows.py` now parses what it writes before writing it. |
| the `earned:` notes reached no file | the note saying what a grader cannot see of the item it is cited on lived only in the emitter. It now ships in both provenance sidecars, under an `earned` key with a line saying what it means. |
| 21 more items were parked under a criterion | on top of the 40 already routed. My own audit missed them: it matched the grader key as `R<n>` exactly, and each of these carried an `earned:` suffix after the id. 61 is the reviewer's original count. All 21 are routed, and the corrected audit now reports zero. |

## Blocking findings

| finding | what the operator must do |
|---|---|
| `[delivery.images]` carries `main` only | the kit has no Docker and no network, and reference/C forbids a fabricated or single-arch sidecar digest. The operator resolves the manifest-list digests for `postgres:16.4-bookworm` and `minio/minio:RELEASE.2024-10-13T13-34-11Z` at packaging time and adds them beside `main`. |
| the shared grader files | CON-2 ships only `test.sh` and expects the other seven vendored grader files in `deku-verifier-base:0.22.0`. Under `environment_mode = "separate"` the grader runs in the image `tests/Dockerfile` builds FROM that base, so confirm the base actually carries those seven files on `PYTHONPATH=/tests` before the first oracle run. |
| no reference app | D20: the bundle is NO-SOLUTION by design. `solution/solve.sh` exits non-zero and says so. |

## Kit defects met on this run

| defect | detail |
|---|---|
| `# syntax=` parser directive | `stage-5-dockerfile.md` and `stage-9-assemble.md` both say the `# syntax=docker/dockerfile:1.6` line is the one permitted `#` line, and `comment_lint.py` (G54) agrees. `docker_lint.py` (G50) fails it outright. G50 is the mechanical authority, so both Dockerfiles ship without it and the two stage files are wrong. |
| `revalidate.py` drops recorded waivers | the sweep re-reads only `sources` from `_handoff/<project>.sources.json`, never a waiver list, so a re-sweep without the ten `--waive` tokens turns G51 red on unchanged bytes. Known; the launcher in the handoff contract passes them. |
| `stage-2-instruction.md` vs CON-1 | the stage says the spec folder lives at `Output/_spec/<code>/`; `01-OUTPUT-CONTRACT.md` says `_spec/` is retired. The folder is written outside the bundle, so no gate reads it either way. |
| `qc_docker.md` DEP-012 vs G50 | DEP-012 requires Chromium's 21 package names inline in the `apt-get install`. `docker_lint.py` caps a physical line at 200 characters, caps `apt-get update` at two occurrences, and requires every install layer to end with `rm -rf /var/lib/apt/lists/*`, which forces one update per install layer. Measured: the inlined RUN lines are 226 and 229 characters, and no split under 200 fits in two install layers. The `ARG CHROMIUM_LIBS_A/B` form is the only shape that satisfies G50, and G55 confirms the browser launchable. |
| `qc_docker.md` CMP-011 vs CMP-022 | CMP-011 fails any service carrying a `ports:` key while CMP-022 requires `ports` on `main`. Scored on CMP-011's Tier-1 wording, which says sidecar. |
| `qc_docker.md` DEP-015 is defined twice | once Medium, for a pip fallback construct, and once Critical, for a compiled-language multi-stage build. The id needs splitting. |
| `qc_toml.md` S-11 template omits `[delivery]` | the canonical template ends at `[verifier]` then `[[artifacts]]`, while S-10.1 and `validate_task.py` both require the block. The two disagree. |
| `qc_spec.md` S5 is stale | it demands a hex palette and millisecond motion values, which `reference/G` G.2 contradicts for `04-uiux-brief.md` and the number rule forbids corpus-wide. Judged on the parts both authorities agree on: exact type, the accessibility bars as values, and a Mode commitment. |
| `qc_spec.md` S2 carries the bare-order feature band | it requires 3 to 6 must-have features, while `reference/G` G.2.1 raises the band to 6 to 10 when a companion is supplied. This task is companion-backed with nine. |
| the `solo_founder` open-signup modifier has no escape | `generate_instruction.md` S-2.2 opens signup for every `solo_founder` task. Here the public role holds no account at all, so the only role an open registration could mint is `editor`, which would breach the pattern row's own critical focus. The modifier needs the kind of conditional `individual` already carries. |
| `secret_lint.py` cannot see a task.toml default | `INDIRECT_RE` (`^\$\{[^}]*\}$`) matches a whole `${VAR:-default}` string, so `classify()` returns before SEC-1 or SEC-2 reads the default; `SH_DEFAULT_RE`, which does read a default, is applied only to `environment/*.sh`. Since `toml_generator.md` S-10.3 MANDATES the expansion form, G63 examines no default value in any task.toml. Measured this run: `classify('STORAGE_ACCESS_KEY', 'minioadmin')` FAILs while `classify('STORAGE_ACCESS_KEY', '${STORAGE_ACCESS_KEY:-minioadmin}')` returns None. The residual exposure is real and is for the operator: harbor scrubs the RESOLVED value, so confirm whether it treats `STORAGE_ACCESS_KEY` as sensitive before the first trial. An earlier repin of this value was retracted as an authored value with no source. |
| `environment/providers/postgres/service.yaml` gives both roles one password | `POSTGRES_PASSWORD: deku-local-dev` is also the `deku_app` password `postgres-init.sql` mints, so the agent holds a credential that reconnects as superuser `deku_admin` and can satisfy a workflow by writing rows directly, which is exactly what the init script says the split prevents. This bundle diverges deliberately: the superuser carries `deku-admin-9c41e7`. Unless the fragment is corrected, `environment/compose.py` regenerates the defect in the next postgres task. |
| both provider fragments set `restart: unless-stopped` | `qc_docker.md` CMP-019 fails it, and `environment/providers/{postgres,minio}/service.yaml` both carry it, so every generated compose inherits a Medium finding. Removed here; the fragments still have it. |

## Cost estimate

`turns_expected = 170`, `tokens_expected = 7000000`. Nine graded features across fourteen routes, seven tables, an object store with a mediated read path, and a front-end specification carrying a measured design system. Comparable to the corpus's other companion-backed variant-`b` tasks, whose briefs run to a similar length.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`

NOT ADMISSIBLE. Nothing counts toward corpus targets until the reference app lands downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.

