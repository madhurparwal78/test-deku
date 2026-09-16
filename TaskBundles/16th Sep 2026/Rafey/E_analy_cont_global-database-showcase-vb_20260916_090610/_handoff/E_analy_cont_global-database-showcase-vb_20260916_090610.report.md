# Build report: E_analy_cont_global-database-showcase-vb_20260916_090610

## Identity

| field | value |
|---|---|
| task code | `E_analy_cont_global-database-showcase-vb_20260916_090610` |
| task id | `deku/global-database-showcase-vb` |
| uuid_v5 | `cc658403-9ebd-5f4b-ab07-55f5999e8b42` |
| cell | enterprise / analytics-reporting / content-publishing |
| Task Order domain | `data-analytics-bi`, re-keyed to `analytics-reporting` because G0 rejects the original key |
| service_profile | `P4-db-storage` |
| providers per slot | backend = `postgres`, storage = `minio` |
| variant | `b` |
| variant_axes | `critical_depth`, `spec_sections` |
| language | typescript |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 |
| kit revision | GreenField-GenKit2 @ 806eb0a |
| vendored grader | 0.22.0 |
| target schema | 1.4 |
| authors | `utsav.jain@ethara.ai` (QL), `mohd.rafey@ethara.ai` (contributor) |
| companion document | `Drive_PRDs/16_sept/cloudgoogle_prd.md`, 1,765 lines |

## Derived-design draws

Every draw is SHA-256 over the archetype `global-database-showcase`, never Python's builtin hash.

| axis | value | note |
|---|---|---|
| render_model | `ssr-islands` | governs |
| backend | `Fastify` | governs |
| frontend | `SolidStart` | governs; a first carry copied the sibling's `Nuxt 3` and was corrected to the draw |
| design_direction | `companion` | a companion document beats the draw (reference/L S-L.6.1); the raw draw was `editorial-serif` |
| nav | `sidebar-nav` | applied to the desk; the companion's top bar with its mega-menu governs the public chrome |
| work_surface | `split detail-pane` | governs the desk product list |
| create_flow | `dedicated-route` | governs, `/desk/product/new` |
| feedback | `full-page-confirmation` | overridden: the companion names a toast on its dialog layer (3.7), and a full-page confirmation would take the editor out of the composer between save and attaching art |
| launch_surface | `alt_text,colour_contrast,cookie_choice,meta_tags,page_view_log` | the reference/O S-O.3 draw, keyed on `[metadata].archetype`; a first draw keyed on the full task code was rejected by G41 and corrected |

## Feature resolution

| candidate | verdict | where it landed | reason |
|---|---|---|---|
| Draft invisibility with mediated object reads | INCLUDED | `## Core features` rules 1 to 4, 37 | the pattern's critical focus |
| Launch obligations: alternative text, cookie choice, page metadata, page-view log | INCLUDED | `## Core features` rules 5 to 10 | the drawn `alt_text`, `cookie_choice`, `meta_tags` and `page_view_log` obligations; `colour_contrast` sits in `## UI/UX notes` |
| The consistency console | INCLUDED | `## Core features` rules 11 to 21 | the companion's centrepiece; server-backed, not client-simulated |
| Public product index, product pages and three families | INCLUDED | `## Core features` rules 22 to 30 |  |
| The industry-solutions explorer | INCLUDED | `## Core features` rules 31 to 32 |  |
| The datasheet library and the art gallery | INCLUDED | `## Core features` rules 33 to 37 | storage slot |
| Contact sales and the assistant surface | INCLUDED | `## Core features` rules 38 to 41 | the idea's ending action |
| The desk and its three staff roles | INCLUDED | `## Core features` rules 42 to 56 | the enterprise role band, 4 roles with the visitor |
| Standing pages and not-found | INCLUDED | `## Core features` rules 57 to 58 |  |
| The companion's six mega-menu product families | NARROWED | three families | each family owes a graded index; six would spend the budget on repetition |
| The companion's eleven industries | NARROWED | six industries | same budget reason |
| A streaming language-model assistant | DROPPED | `## Constraints` | INV6 and the no-third-party-runtime-call rule; the assistant is a stored-response surface whose counter is graded |
| Visitor accounts, payments, email, search service, localisation | DROPPED | `## Constraints` | out of scope in the companion's own framing |
| A build order | DROPPED | - | generate_instruction.md S-2.1 keeps `## Build plan` out of the emission |

## Slot obligations

| slot | provider | state | observed by |
|---|---|---|---|
| backend | `postgres` | MET | `test_published_product_fields_survive_a_reread`, `test_seed_holds_the_eight_published_products_and_one_draft`, `test_two_concurrent_publishes_of_one_slug_admit_one_winner` (critical), `test_strong_read_never_returns_a_stale_value` (critical) |
| storage | `minio` | MET | `test_uploaded_art_object_exists_in_the_bucket` (critical), `test_uploaded_object_key_follows_the_art_scheme`, `test_unpublished_product_objects_stop_resolving_at_once` (critical) |

## Grading surface

| measure | count | note |
|---|---|---|
| workflows | 19 | the enterprise band (reference/B B.3) |
| browser substeps | 59 |  |
| pytest substeps | 113 | one per test, bijective (G8) |
| critical substeps | 25 | every declared slot and every permission boundary |
| non-happy-path workflow ids | 5 | visitor_cannot_reach_a_draft_product_denied, draft_object_bytes_are_denied_to_a_visitor, visitor_filter_matching_nothing_shows_an_empty_state, editor_drafts_a_product_and_cannot_publish, unauthenticated_desk_request_is_denied |
| pytest module | `tests/test_output.py` | 113 tests, one module (CON-2, G46) |
| checklist items | 797 | capability 185, constraint 211, contract 13, data 18, literal 292, role 19, ui 59 |
| judged criteria | 14 | 13 positive, 1 negative |
| reference rubric items | 18 | compiled-weight share 0.9634, floor 0.60 |
| literals ledger | 259 | 1 verifier-only (`DB_ADMIN_URL`) |

### Judged rubric, per dimension

| dimension | criteria | positive score | share | target | difference |
|---|---|---|---|---|---|
| instruction_following | 3 | 11 | 0.256 | 0.3 | 0.044 |
| functionality | 2 | 8 | 0.186 | 0.25 | 0.064 |
| ux_flow | 2 | 6 | 0.140 | 0.15 | 0.010 |
| ui_visual | 4 | 9 | 0.209 | 0.15 | 0.059 |
| motion | 1 | 3 | 0.070 | 0.05 | 0.020 |
| accessibility | 1 | 3 | 0.070 | 0.05 | 0.020 |
| responsiveness | 1 | 3 | 0.070 | 0.05 | 0.020 |

Positive total 43; negative magnitude 3, cap 129. `task completion` is 11/14, inside the 60 to 80 percent band.

## Grading window

| section | chars | reference | flag |
|---|---|---|---|
| Core features | 13210 | 2400 | past-slice |
| User flow | 5313 | 1900 | past-slice |
| UI/UX notes | 6315 | 1700 | past-slice |
| Constraints | 1351 | 800 | over-reference |
| User roles | 1906 | 1000 | over-reference |
| Overview | 2254 | 700 | over-reference |
| joined six | 30349 | 8800 | past-slice |

Length is reported, never failed (G33). `## Core features` runs past the 2,500-char slice, so the judge reads its first 2,500 characters; the draft-invisibility and object-store rules are front-loaded there deliberately, and the tail reaches the agent in full. The unbudgeted `## Front-end specification` carries the companion's measured design content.

## Companion carriage (G51)

35/35 source colours described by family and tone; 158/158 topics carried; 186/186 enumerated items carried, with seventeen declared waivers.

Every sweep must pass the same seventeen `--waive` tokens, because `revalidate.py` re-reads only `sources` from `_handoff/<project>.sources.json` and never a waiver list. The tokens are recorded in that file and in `_spec/<code>/00-decisions.md`.

## Literals ledger

| class | values | sample |
|---|---|---|
| account | 3 | `editor@example.com`, `publisher@example.com`, `administrator@example.com` |
| credential | 1 | `deku-demo-pw-2026` |
| design_phrase | 119 | `SolidStart`, `Fastify`, `data-page-type`, `Americas`, ... |
| endpoint | 28 | `/api/health`, `/api/products`, `/api/products/{slug}`, `/api/families`, ... |
| env_var | 8 | `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, ... |
| motion_moment | 9 | `fade in from below`, `advancing one card`, `panel drop`, `short decelerating travel`, ... |
| number | 8 | `24`, `240`, `500`, `1000`, ... |
| role | 4 | `editor`, `publisher`, `administrator`, `visitor` |
| route | 18 | `/product`, `/product/{slug}`, `/family`, `/family/{slug}`, ... |
| scheme | 3 | `products/<product_id>/art/<sha256_of_bytes>.<ext>`, `products/<product_id>/datasheet/<sha256_of_bytes>.pdf`, `platform/<datasheet_id>/<sha256_of_bytes>.pdf` |
| seed_record | 54 | `tessera`, `slipstream`, `beacon-enterprise`, `quarry`, ... |
| status | 4 | `draft`, `published`, `404`, `200` |

Full ledger: `_handoff/<code>.literals-ledger.json`. Every non-verifier value appears verbatim in `instruction.md`; `DB_ADMIN_URL` is verifier-only and appears in `task.toml` `[verifier].env` alone (INV4).

## Authoring documents

| document | instruction.md sections it fed |
|---|---|
| `00-decisions.md` | the draws, the overrides, the residual judgment calls, the companion carry table, the seventeen waivers |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | authoring-side only; `## Build plan` is not emitted |

They live at `Output/16sept-cloudgoogle/_spec/E_analy_cont_global-database-showcase-vb_20260916_090610/`, outside the bundle (CON-5).

## Kit gate log

Rendered from `_handoff/<code>.gates.jsonl`, one row per gate, each carrying the SHA-256 of every input file it read. No verdict in this table was typed by hand (ISSUES C-02).

| gate | tool | exit | verdict | elapsed |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | 0.03s |
| G1/G12 | `layout_lint.py` | 0 | PASS | 0.03s |
| G46 | `structure_lint.py` | 0 | PASS | 0.03s |
| G50 | `docker_lint.py` | 0 | PASS | 0.02s |
| G55 | `runtime_deps_lint.py` | 0 | PASS | 0.03s |
| G63 | `secret_lint.py` | 0 | PASS | 0.02s |
| G48 | `truth_lint.py` | 0 | PASS | 0.18s |
| G51 | `source_lint.py` | 0 | PASS | 0.03s |
| G52 | `rubric_context_lint.py` | 0 | PASS | 0.03s |
| G54 | `comment_lint.py` | 0 | PASS | 0.02s |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | 0.03s |
| G11 | `leak_scan.py` | 0 | PASS | 0.03s |
| G33 | `window_lint.py` | 0 | PASS | 0.02s |
| G4/G5 | `contract_lint.py` | 0 | PASS | 0.03s |
| G43 | `prescription_lint.py` | 0 | PASS | 0.05s |
| G44 | `disclosure_lint.py` | 0 | PASS | 0.03s |
| G10 | `no_sdk_lint.py` | 0 | PASS | 0.05s |
| G31 | `determinism_lint.py` | 0 | PASS | 0.05s |
| G14 | `reward_path_lint.py` | 0 | PASS | 0.02s |
| G27/G30 | `rubric_lint.py` | 0 | PASS | 0.02s |
| G41 | `flag_lint.py` | 0 | PASS | 0.03s |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | 0.02s |
| G59/G60 | `codequality_lint.py` | 2 | ? | 0.02s |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | 0.05s |
| G6 | `fixture_lint.py` | 0 | PASS | 0.08s |
| G24 | `coverage_map.py` | 0 | PASS | 0.07s |
| G37 | `checklist_qc.py` | 0 | PASS | 0.06s |
| G39 | `rubric_align_lint.py` | 0 | PASS | 0.05s |
| G28/G29 | `channel_lint.py` | 0 | PASS | 0.04s |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | 0.03s |
| G0/INV5 | `vendor_check.py` | 0 | PASS | 0.03s |
| G47 | `output_qc.py` | 0 | PASS | 0.04s |

32/32 green.

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
| `QC_instruction.md` | G34 | FAIL | qc-instr-cyc3 | 24 | 1 | 0 |
| `QC_spec.md` | G34 | FAIL | qc-spec-reviewer-c3 | 15 | 5 | 1 |
| `qc_docker.md` | G35 | PASS | opus5-qc-docker-c2 | 105 | 0 | 2 |
| `qc_rubric.md` | G53 | FAIL | qc-rubric-opus5-c3 | 16 | 9 | 0 |
| `qc_solution_checklist.md` | G37 | FAIL | qc-checklist-c3 | 0 | 0 | 0 |
| `qc_toml.md` | G36 | PASS | qctoml-opus5-c3 | 120 | 0 | 4 |
| `task_code_verifier.md` | G3 | VALID | tcv-opus5-c1 | 12 | 0 | 0 |

### Findings carried by the reviewers

Abridged. Every finding, verbatim, is in `_handoff/<code>.receipts.json`, which is the artifact G40 reads. A finding is the reviewer's own words at the cycle it was raised and is never edited afterwards, so an earlier cycle's finding can describe bytes a later repair has replaced.

- `QC_instruction.md` [C2 · BLOCKER] New in cycle 3: a graded response shape is still unpinned. Evidence: API shapes `GET /api/desk/views` answers `{"counts", "recent"}`: "a count per public route ordered by count descending, and recent views each carrying `route` and `viewed_at`". `recent` names its element fields; `counts` names neithe...
- `QC_instruction.md` [C2 · CLOSED, WARN] Cycle-2 console literals verified against the bytes. Rule 13 pins ISO 8601 UTC with milliseconds (`2026-09-16T09:06:10.123Z`) and refuses a write missing its key or value. Rule 14 pins staleness as whole milliseconds behind the latest acknowledged write, `0` for `strong`, with latency in whole ms...
- `QC_instruction.md` [D5 · CLOSED] All three cycle-2 inversions repaired. (a) The effects vocabulary is "seven entries", adding "the skeleton shimmer over a waiting surface; and the focus ring" (companion 3.6), and the 00-decisions.md carry row reads "the seven-entry effects vocabulary". (b) "Each utility mark takes the colour of the te...
- `QC_instruction.md` [D3 · CLOSED] Definition of done is two sentences, 56 words, ending "stay unreadable to anyone outside the desk until it is published." It names no harness, and the role-row restatement is gone.
- `QC_instruction.md` [D2 · CLOSED] Rule 3 now reads: "answer not found to a request carrying no valid desk bearer token ... and are served to a request carrying one". This agrees with the two media rows ("not found where the owning product is `draft` and the request carries no valid desk bearer token"), the API-shapes opening ("except t...
- `QC_instruction.md` [C3 · CLOSED, WARN] All seven cycle-2 gaps verified closed: `POST /api/desk/datasheets` (with rule 46 page-count-at-registration and unknown-key refusal), `art_pieces` `width`/`height`, the assistant answering nothing (rule 41 and Constraints), rail cards as "a deep neutral fill with near-white text ... the band its...
- `QC_instruction.md` [C1 · CLOSED] The negatives are present. Rule 16: bounded with no or malformed bound, or exact with no timestamp, is refused and names the field. Rule 17: severing an already-severed region or restoring a joined one changes nothing. Rule 21: a reset with nothing severed answers the seeded state. Rule 25: an unknown ...
- `QC_instruction.md` [C6 · CLOSED] "Components keep clear module boundaries" and the state-check sentence are gone (grep finds no `module` or `state check`). Mechanisms are restated as moments: "a quick change when something is pointed at, focused or opened; an entrance, or a loop while a surface waits; and the fade in from below". The ...
- `QC_instruction.md` ... 4 further finding(s); the full text is in `_handoff/<code>.receipts.json`
- `QC_spec.md` [S5 · MAJOR] 04-uiux-brief.md's new motion table gives every moment a value, but it credits the companion with values the companion does not give, and three rows contradict it. 04 line 5 says 'the companion's measured motion values sit beside the words', and the column is headed 'Companion token and value'. Evidence...
- `QC_spec.md` [S8 · MINOR] Two entries in 00-decisions.md's residual judgment calls restate derivation facts rather than record a judgment. Evidence: line 59 'Enterprise closes signup; applied, with the three desk roles seeded and no registration or reset.' restates the enterprise category modifier (QC_spec 5.1: 'enterprise -> se...
- `QC_spec.md` [S9 · MAJOR] 04-uiux-brief.md still uses adjectives for shape and spacing, although the companion supplies numbers and a grader asserts one. Evidence: lines 69-73 'One soft product radius on cards ..., tighter on buttons and fields, softer on feature tiles, a full pill on chips ... An eight-step rhythm; the gutter a...
- `QC_spec.md` [G2 · MAJOR] The copy strings now round-trip, but several graded limits and pinned rules are still stated only in the brief. Evidence: (a) the brief's Messages paragraph says 'A message dismisses after five seconds or on press, the stack holds at most three, and a fourth displaces the oldest'. tests/conftest.py pins...
- `QC_spec.md` [G3 · MINOR] The corrected 3.2 row in the carry table still claims one token more than 04 carries, and one companion colour role changed without a log entry. Evidence: 00-decisions.md line 84 says '34 of 35 tokens by family and tone, each with its role; `--yellow-tint` waived'. 04's palette table has role rows for 3...
- `QC_spec.md` [S5 · WARN, kit conflict, not counted] 04 still carries no hex palette. S5 and QC_spec 5.3 ask for one, but reference/G G.2 ('no hex') and generate_instruction.md's number rule forbid it. Every colour word checked matches tools/source_lint.py colour_words(). The claimed contrasts reproduce exactly: deep neutral on -...
- `QC_spec.md` [S2 · WARN, kit conflict, not counted] 01-PRD.md has ten must-have features. That is inside the companion band of 6 to 10 (reference/G G.2.1) and outside QC_spec S2's 3 to 6. The problem statement and a 13-item out-of-scope list are present.
- `QC_spec.md` [G3 · WARN, outside QC_spec scope, not counted] The carry table has no row or waiver for companion 6.7's top-of-page load bar (`progress-indeterminate-1..4`) or 6.2's `pulse` live-status dots. The 6.1-6.8 row lists six keyframes, and neither thing reaches the brief. This belongs to QC_instruction D5 / G51.
- `QC_spec.md` ... 1 further finding(s); the full text is in `_handoff/<code>.receipts.json`
- `qc_docker.md` Cycle-1 FAILs CMP-005 (Critical), CMP-015 (High) and CMP-018 (Medium) are CLOSED: environment/postgres-init.sql now ships (478 bytes, 21 lines). It is the body of environment/providers/postgres/init.sql with the 28 comment lines and the blank line after them removed, and it is byte-identical to 16sept-keralatourism/...
- `qc_docker.md` HAL-007 cycle-1 WARN is CLOSED: environment/Dockerfile line 8 now reads `ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1`, and the file now matches the docker_generator.md SKELETON line for line. Every remaining ENV key (DEBIAN_FRONTEND, LANG, TZ, PIP_DISABLE_PIP_VERSION_CHECK, PYTHO...
- `qc_docker.md` Stack change checked, no finding: instruction.md Technical requirements now reads `Build the server as `Fastify` and the client as `SolidStart` in TypeScript`, and solution/TRUTH.md records frontend `SolidStart`. Both run on Node, and the image still installs nodejs from NodeSource node_22.x (NODE_MAJOR=22), which s...
- `qc_docker.md` CMP-013 WARN, unchanged by decision (owned by task.toml / G36, not a bundle FAIL here): `[verifier].env APP_PUBLIC_URL = "${APP_PUBLIC_URL:-http://localhost:4173}"` sits beside `[verifier].environment_mode = "separate"`, while the agent side uses `http://main:4173` and the other verifier hosts are compose service na...
- `qc_docker.md` DEP-011 NOT-APPLICABLE and BP-002 WARN, carried from cycle 1: task.toml sets `environment_mode = "separate"` and tests/Dockerfile builds FROM deku-verifier-base:0.22.0, which already carries the grader pins. The agent image's pytest/httpx/psycopg/boto3/pyyaml/playwright pins and Chromium layers are therefore redunda...
- `qc_docker.md` Kit gate gap, still open at 806eb0a (no check id; fix at kit): re-run on a scratch copy of this bundle with only environment/postgres-init.sql deleted, tools/layout_lint.py (G1) still prints `VERDICT PASS`, as do docker_lint.py (G50) and runtime_deps_lint.py (G55). A compose bind source that does not exist, which is...
- `qc_docker.md` Kit doc drift, still open at 806eb0a (no bundle change): 01-OUTPUT-CONTRACT.md line 144 still annotates docker-compose.yaml with `Per-provider init scripts stay out (reference/C §C.6)`, which contradicts reference/C §C.6, stage-5 and docker_generator.md shipping `./postgres-init.sql`. stage-9-assemble.md line 50 (`t...
- `qc_rubric.md` ABORT: rubric QC unrecoverable after 3 cycles: RC-04: R4 and R13 still grade (anchor, facet) pairs that committed pytest tests already assert, and RC-09/RC-11 still hold criteria a correct app cannot pass (R2, R4, R10). Route to S3.5 (judged_criteria in solution/trinity/grounding.yaml, then regenerate). Do not re-ru...
- `qc_rubric.md` RC-01: coverage is 44/44 rubric-routed `ui` obligations claimed by a criterion, and 59/59 judgment obligations are graded across channels (G39 PASS; 15 `ui` items sit on browser substeps). The claimed moves check out in the bytes: C-FE-41 (console stacking) is on the narrow /console substep with no earned note, C-FE...
- `qc_rubric.md` RC-04: R4 repeats a committed pytest assertion. test_shape_and_spacing_follow_the_product_rhythm loads /product (the product index) and asserts `a resting card on /product draws no shadow` (test_output.py lines 1904 and 1914-1916, citing C-FE-24). R4's yes case requires `a card rests on a pale hairline border with n...
- `qc_rubric.md` RC-04: R13 repeats a committed pytest assertion. test_only_the_skeleton_animates_indefinitely calls emulate_media(reduced_motion='reduce') on / and asserts that no running animation still translates, transforms or rotates (test_output.py lines 1959-1968, citing C-UX-17 and C-FE-118). R13's criterion `neither travels...
- `qc_rubric.md` RC-04: R9 grades a facet that its sibling substep reads, and claims the item that substep reads. The substep publisher_publishes_and_returns_to_draft[0] reads `select Kestrel in the desk product list, read its detail pane with its name, badge, summary and art pieces`. That is C-FE-137's pane-fill facet (`Selecting a...
- `qc_rubric.md` RC-04 (smaller): R14's no case `the sub-nav, hero and highlights touch or overlap` re-grades test_product_route_moves_its_sub_nav_and_rail_below_lg. At NARROW_VIEWPORT (390px, conftest.py line 98) on /product/tessera, that test asserts the highlights rail's top sits at or below the h1's bottom. `Set in tiny type` re...
- `qc_rubric.md` RC-06: R4 names elements that its surface does not have. The product index (instruction.md lines 803-807) holds a breadcrumb, a heading, a count line, a sticky filter bar with a name field and two selectors, and the card grid. It has no chip, no named divider and no control that is ever unavailable, and the family p...
- `qc_rubric.md` RC-07: three product terms are used with no definition in the rule. R10 uses `the console's commit-wait bar` and `the diamond mark`. R13 uses `the product rail`. R14 uses `the highlights` and `the dropdown sub-nav`. A judge has met none of them. Fix: R10 rule `The COMMIT-WAIT BAR is the bar in the console's clock re...
- `qc_rubric.md` ... 7 further finding(s); the full text is in `_handoff/<code>.receipts.json`
- `qc_solution_checklist.md` GAP and UNPINNED (instruction.md lines 682-688 and copy row line 977, header navigation): no item carries the six primary navigation labels. C-FE-52 reads `Each primary navigation label opens its matching public route` and names none; `Datasheets`, `Console` and `Contact us` appear nowhere in the checklist, `Product...
- `qc_solution_checklist.md` GAP and UNPINNED (instruction.md lines 479-527, Data model): no item names any of the thirteen tables (`accounts`, `sessions`, `products`, `families`, `highlights`, `art_pieces`, `datasheets`, `industries`, `customers`, `console_writes`, `partitions`, `sales_enquiries`, `page_views`), which prompts/solution_checklis...
- `qc_solution_checklist.md` GAP (instruction.md lines 129-131 and 182-185, Core features rules 17 and 36, both named in the claimed brief v3 negatives): `restoring one already joined, changes nothing and answers the same five regions` has no item; C-CF-66 carries the severing half only. `a slug naming no family answers a top-level empty array`...
- `qc_solution_checklist.md` INVENTION (C-UX-77, checklist line 403): `At a phone width the product route reads comfortably, nothing crowding the next.` cites the responsive paragraph (instruction.md lines 394-395), which says only that at a narrow viewport nothing overflows sideways, every navigation target stays reachable and rows of cards fo...
- `qc_solution_checklist.md` PARTIAL CAPTURE and SCOPE DRIFT (Hat 2): C-CF-17 `Returning a product to draft stops its art with its datasheet bytes at once` drops `for every caller without a desk session` (line 83-84) and, read unconditionally, contradicts C-CF-16. C-DC-13 drops `and leaves the stored state unchanged` from the API preamble (line...
- `qc_solution_checklist.md` PARTIAL CAPTURE (reduced motion and motion, lines 332-335, 378-380, 853-856): C-UX-17 drops `and every control still works`; `Nothing is carried by colour or motion alone` has an item for colour (C-UX-15, C-UX-16) and none for motion; C-FE-117 weakens `every write, read and partition control still works from the key...
- `qc_solution_checklist.md` GAP (chrome and layout presentation, instruction.md lines 653-655, 671-674, 690-720): no item carries: mega-menu group headings at the micro step in a mid cool neutral, links at the small step in a deep neutral warming to the mid, vivid blue, and the panel fading open (691-693); the drawer as a full-height panel ove...
- `qc_solution_checklist.md` GAP (home and product route presentation, instruction.md lines 727-790): no item carries: the hero, the console and the customer proof on the page ground (729; C-FE-69 carries the section-ground half only); the filled and outline treatments of the hero controls (736) and of the closing band controls, which C-FE-83 d...
- `qc_solution_checklist.md` ... 8 further finding(s); the full text is in `_handoff/<code>.receipts.json`
- `qc_toml.md` META-008 (PASS, cycle-2 FAIL resolved): [task].description now reads "An enterprise cloud platform's public product site with an interactive consistency console and a private staff desk that publishes or holds each product page." It is one sentence with no marketing phrasing. Each part traces to the revised sources:...
- `qc_toml.md` Brief/spec revision re-check (PASS, no task.toml effect): the four roles (`visitor`, `editor`, `publisher`, `administrator`) are unchanged across instruction.md ## User roles and 05-backend-schema.md ## Roles, so sub_category = "enterprise" still holds (TAX-003). The administrator seed address is now administrator@e...
- `qc_toml.md` VERIF-005 (PASS, tension recorded, unchanged from cycle 2): [verifier].env APP_PUBLIC_URL = "${APP_PUBLIC_URL:-http://localhost:4173}" matches the registry row and toml_generator.md 10.4 byte for byte. Under environment_mode = "separate", localhost:4173 inside the verifier container is not the app, so grading reache...
- `qc_toml.md` SCHEMA-005 (Informational, WARN, a kit contradiction, unchanged): toml_generator.md 10.5b asks for [metadata].rubric_version = "1", but the 11 template, validate_task.py META_REQUIRED and config/kit-config.yaml leave it out. Fix: in the kit, delete 10.5b or add the key to the template and validator. No bundle change...
- `qc_toml.md` SCHEMA-011 (Informational, WARN, unchanged): [delivery] and [delivery.images] are not in the 11 template, but toml_generator.md 10.1 sanctions them and validate_task.py lint_delivery checks them. All values hold, and images.main matches the environment/Dockerfile FROM pin. Fix: add [delivery] to the kit's 11 templat...
- `qc_toml.md` SCHEMA-013 (Informational, WARN, follows from SCHEMA-011, unchanged): all template sections are in template order. The template gives [delivery] no position, so its place between [verifier] and [[artifacts]] cannot be checked. Fix: give [delivery] a fixed position in the kit's 11 template.
- `qc_toml.md` TAX-008 (Informational, WARN, as the row directs): archetype "global-database-showcase" cannot be shown globally unique from the supplied inputs. Fix: none in the bundle; check against the corpus ledger at merge time.
- `qc_toml.md` Re-run on the current bytes (task.toml mtime 16:17): validate_task.py task.toml PASS (G2/G16), secret_hygiene_lint.py task.toml PASS (G17), secret_lint.py on the bundle directory PASS (G63), flag_lint.py PASS (G41, 3 advisory warnings), layout_lint.py PASS (G1/G12), taskorder_lint.py on scratchpad/cloud/taskorder.ya...
- `task_code_verifier.md` CODE E_analy_cont_global-database-showcase-vb_20260916_090610 VERDICT VALID LEVELS category=enterprise domain=analytics-reporting pattern=content-publishing archetype=global-database-showcase variant=b created=2026-09-16T09:06:10Z TASK_ID deku/global-database-showcase-vb PROFILES P4-db-storage
- `task_code_verifier.md` All 12 checks pass; `task_code.py decode` agrees (VALID: all levels decode and every taxonomy rule holds). Timestamp 2026-09-16T09:06:10Z is a real UTC instant, after 2024-01-01 and not after the run date 2026-09-16, so timestamp-sanity raises no warning.
- `task_code_verifier.md` task.toml agrees with the code: [task].name = deku/global-database-showcase-vb; [metadata] sub_category = enterprise, domain = analytics-reporting, pattern = content-publishing, archetype = global-database-showcase, variant = b, task_code = the full code, service_profile = P4-db-storage (the only legal profile for e...
- `task_code_verifier.md` The bundle directory basename is exactly E_analy_cont_global-database-showcase-vb_20260916_090610.
- `task_code_verifier.md` [task].uuid_v5 = cc658403-9ebd-5f4b-ab07-55f5999e8b42 recomputes byte-identically from `task_code.py uuid5 <code>`.
- `task_code_verifier.md` The mint ledger /Users/apple/Desktop/deku/Output/16sept-cloudgoogle/ledger.jsonl has one row, recording this code exactly once with matching category, domain, pattern, archetype, variant, service_profile P4-db-storage and minted_utc 2026-09-16T09:06:10Z; `task_code.py ledger --list` reports 1 unique archetype and no...
- `task_code_verifier.md` Domain re-key is correct and faithful. The Task Order's `data-analytics-bi` is not one of the 36 level-2 domains, so G0 is right to reject it. Of the twelve enterprise domains, `analytics-reporting` is the only one about data analysis and reporting, and BI (business intelligence) is reporting and analytics by defini...
- `task_code_verifier.md` Note: the Task Order yaml still says `domain: data-analytics-bi`, so the bundle records a deliberate departure from its input. The departure is documented only in _spec/.../00-decisions.md, not in task.toml.

## Certification state

4 of 7 certification prompts carry no FAIL check: `qc_docker.md`, `qc_solution_checklist.md`, `qc_toml.md`, `task_code_verifier.md`.

Still carrying a FAIL, with every finding verbatim in the receipts: `QC_instruction.md`, `QC_spec.md`, `qc_rubric.md`.

## Blocking findings

| finding | what the operator must do |
|---|---|
| `[delivery.images]` carries `main` only | the kit has no Docker and no network, and reference/C forbids a fabricated or single-arch sidecar digest. The operator resolves the manifest-list digests for `postgres:16.4-bookworm` and `minio/minio:RELEASE.2024-10-13T13-34-11Z` at packaging time and adds them beside `main`. |
| the shared grader files | CON-2 ships only `test.sh` and expects the other seven vendored grader files in `deku-verifier-base:0.22.0`. Under `environment_mode = "separate"` the grader runs in the image `tests/Dockerfile` builds FROM that base, so confirm the base actually carries those seven files on `PYTHONPATH=/tests` before the first oracle run. |
| `APP_PUBLIC_URL` under separate mode | `[verifier].env` keeps the `http://localhost:4173` default VERIF-005 and `toml_generator.md` S-10.4 require. In a separate verifier container localhost is not the app, so confirm Harbor injects `APP_PUBLIC_URL` before the first oracle run. |
| no reference app | D20: the bundle is NO-SOLUTION by design. `solution/solve.sh` exits non-zero and says so. |

## Kit defects met on this run

| defect | detail |
|---|---|
| `# syntax=` parser directive | `stage-5-dockerfile.md` and `stage-9-assemble.md` both say the `# syntax=docker/dockerfile:1.6` line is the one permitted `#` line, and `comment_lint.py` (G54) agrees. `docker_lint.py` (G50) fails it outright. G50 is the mechanical authority, so both Dockerfiles ship without it and the two stage files are wrong. |
| `revalidate.py` drops recorded waivers | the sweep re-reads only `sources` from `_handoff/<project>.sources.json`, never a waiver list, so a re-sweep without the seventeen `--waive` tokens turns G51 red on unchanged bytes. Known; the launcher in the handoff contract passes them. |
| `stage-2-instruction.md` vs CON-1 | the stage says the spec folder lives at `Output/_spec/<code>/`; `01-OUTPUT-CONTRACT.md` says `_spec/` is retired. The folder is written outside the bundle, so no gate reads it either way. |
| `qc_docker.md` DEP-012 vs G50 | DEP-012 requires Chromium's 21 package names inline in the `apt-get install`. `docker_lint.py` caps a physical line at 200 characters, caps `apt-get update` at two occurrences, and requires every install layer to end with `rm -rf /var/lib/apt/lists/*`, which forces one update per install layer. Measured: the inlined RUN lines are 226 and 229 characters, and no split under 200 fits in two install layers. The `ARG CHROMIUM_LIBS_A/B` form is the only shape that satisfies G50, and G55 confirms the browser launchable. |
| `qc_docker.md` CMP-011 vs CMP-022 | CMP-011 fails any service carrying a `ports:` key while CMP-022 requires `ports` on `main`. Scored on CMP-011's Tier-1 wording, which says sidecar. |
| `qc_docker.md` DEP-015 is defined twice | once Medium, for a pip fallback construct, and once Critical, for a compiled-language multi-stage build. The id needs splitting. |
| `qc_toml.md` S-11 template omits `[delivery]` | the canonical template ends at `[verifier]` then `[[artifacts]]`, while S-10.1 and `validate_task.py` both require the block. The two disagree. |
| `qc_spec.md` S5 is stale | it demands a hex palette and millisecond motion values, which `reference/G` G.2 contradicts for `04-uiux-brief.md` and the number rule forbids corpus-wide. Judged on the parts both authorities agree on: exact type, the accessibility bars as values, and a Mode commitment. |
| `qc_spec.md` S2 carries the bare-order feature band | it requires 3 to 6 must-have features, while `reference/G` G.2.1 raises the band to 6 to 10 when a companion is supplied. This task is companion-backed with nine. |
| `flag_lint.py` keys the launch draw on the archetype but names the argument `task_code` | `launch_surface(task_code)` hashes `f"{task_code}:launch-surface"`, and G41 calls it with `[metadata].archetype`. Read at face value it draws over the full task code, which is what this run did first; G41 then rejected the declared set as chosen rather than derived. The parameter name should say archetype. |
| the colour vocabulary collapses distinct tokens | `source_lint.colour_words()` maps five distinct blues to `mid, vivid blue` and six greys to `near-white neutral`, so a brief can only tell those roles apart by adding a relative step (`one step lighter`) the vocabulary itself cannot express. |
| `build_workflows` and the YAML runtime disagree about `cov:` | `coverage_map.CITE_RE` reads a `cov:` tag by regex, so an `(earned: ...)` note inside it is fine to the gate, but the colon-space it adds is invalid in a plain YAML scalar and `run_workflows.py` loads the file. The value has to be quoted, and nothing in the kit says so. |
| `secret_lint.py` cannot see a task.toml default | `INDIRECT_RE` (`^\$\{[^}]*\}$`) matches a whole `${VAR:-default}` string, so `classify()` returns before SEC-1 or SEC-2 reads the default; `SH_DEFAULT_RE`, which does read a default, is applied only to `environment/*.sh`. Since `toml_generator.md` S-10.3 MANDATES the expansion form, G63 examines no default value in any task.toml. Measured this run: `classify('STORAGE_ACCESS_KEY', 'minioadmin')` FAILs while `classify('STORAGE_ACCESS_KEY', '${STORAGE_ACCESS_KEY:-minioadmin}')` returns None. The residual exposure is real and is for the operator: harbor scrubs the RESOLVED value, so confirm whether it treats `STORAGE_ACCESS_KEY` as sensitive before the first trial. An earlier repin of this value was retracted as an authored value with no source. |
| `environment/providers/postgres/service.yaml` gives both roles one password | `POSTGRES_PASSWORD: deku-local-dev` is also the `deku_app` password `postgres-init.sql` mints, so the agent holds a credential that reconnects as superuser `deku_admin` and can satisfy a workflow by writing rows directly, which is exactly what the init script says the split prevents. This bundle diverges deliberately: the superuser carries `deku-admin-9c41e7`. Unless the fragment is corrected, `environment/compose.py` regenerates the defect in the next postgres task. |
| VERIF-005 vs `environment_mode = "separate"` | S-10.4 and VERIF-005 pin the verifier default to `http://localhost:4173`, while VERIF-001 defaults the verifier to its own container, where localhost does not reach `main`. Both qc_toml and qc_docker record the tension; no kit document says whether Harbor injects the value. |
| G1 misses a missing compose bind source | cycle 1 shipped without `environment/postgres-init.sql`; Compose mounts an empty directory and postgres exits 1, yet `layout_lint.py` (G1), `docker_lint.py` (G50) and `runtime_deps_lint.py` (G55) all PASS on that shape. Only the qc_docker reviewer caught it. |
| `generate_instruction.md` S-4 verbatim block vs G33 | the Technical requirements provider sentence is mandated verbatim and carries an em dash; `window_lint.py` (G33) fails any em or en dash in the brief as house style. The brief carries the block with a spaced hyphen, so a strict verbatim check and G33 cannot both pass. |
| S-2.10 draws are not gated | no mechanical gate checks that `nav`, `work_surface`, `create_flow` and `feedback` draws are recorded in `00-decisions.md`; the QC_spec reviewer found them missing at cycle 2 on a bundle every gate passed. |
| both provider fragments set `restart: unless-stopped` | `qc_docker.md` CMP-019 fails it, and `environment/providers/{postgres,minio}/service.yaml` both carry it, so every generated compose inherits a Medium finding. Removed here; the fragments still have it. |

## Cost estimate

`turns_expected = 170`, `tokens_expected = 7000000`, the `hard` row. Nine graded feature groups across thirteen public routes and six desk routes, four roles, thirteen tables, an object store with a mediated read path, a server-side consistency store with an ordering invariant and a partition case, and a front-end specification carrying a measured design system.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION, CERTIFICATION ABORTED`

Kit S-15.1 allows three fix-or-abort cycles per certification prompt. After cycle 3, `qc_toml`, `qc_docker` and `task_code_verifier` carry no FAIL. `QC_instruction` (1 FAIL: the `counts` shape of `GET /api/desk/views`), `QC_spec` (5 FAIL), `qc_solution_checklist` (item-level gaps, chiefly presentation clauses not itemised one by one) and `qc_rubric` (9 FAIL) ended cycle 3 with a FAIL, so each is ABORT. The receipt schema has no ABORT verdict, so the receipts carry the reviewers' FAIL verbatim.

### Changes made after the cycle-3 reviews, not re-reviewed

A fourth review cycle is not permitted, so these repairs, each taken from a cycle-3 finding's own fix text, have passed every mechanical gate but no reviewer:

- `instruction.md`: `counts` pinned as an array of `route` and `count` entries; customers carry `id` and `name`; journey 3 reads a staleness of `0`; desk badge words sit on their fill. `tests/test_output.py` reads `count` only.
- `_spec/`: 04 motion and radius/spacing tables with a source column naming the companion section or `assigned; companion silent`; the chevron, search overlay and scrim rows corrected; 03 States carries the message stack, megabyte format and `Retail` default; 05 carries the seeded datasheet composition; 00 drops two restated lines and logs the promo-banner ground departure.
- Rubric: R2, R4, R9, R10, R13 and R14 rules and the R2, R6, R7, R12, R13 openers replaced with qc_rubric cycle-3 fix texts; eleven checklist items rerouted to the substeps those fixes named.
- Not addressed: qc_solution_checklist cycle-3 findings 1 to 15 (per-clause presentation items, table and column items, restatement merges, `and`-to-`with` wording) and QC_instruction's `/gallery` discoverability WARN.

NOT ADMISSIBLE. Nothing counts toward corpus targets until the reference app lands downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.

