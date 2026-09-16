# Build report - S_conte_cont_creative-studio-showcase-vb_20260916_103045

## Identity

| Field | Value |
|---|---|
| Task code | `S_conte_cont_creative-studio-showcase-vb_20260916_103045` |
| Task id | `deku/creative-studio-showcase-vb` |
| Cell | solo_founder / content-publishing / content-publishing |
| Service profile | `P4-db-storage`: slot `backend` -> `postgres`, slot `storage` -> `minio` |
| Verifier mode | `separate`: the grader ships its own image from `tests/Dockerfile` on `deku-verifier-base` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `python` |
| Stack draw | `mpa-progressive` / `Flask + Jinja` / `Alpine.js + server templates`, over `[metadata].archetype` |
| Design direction | `companion` (the `editorial-serif` draw does not govern; reference/L SS L.6.1) |
| Launch surface | `custom_404, no_broken_links, page_view_log, privacy_page, social_preview` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Kit revision | `806eb0a` |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Authors | `utsav.jain@ethara.ai` (QL), `mohd.rafey@ethara.ai` (contributor) |

## Task Order, as received and as minted

| Field | Supplied | Minted | Why |
|---|---|---|---|
| category | `solo_founder` | `solo_founder` | legal as given |
| domain | `portfolio-agency` | `content-publishing` | not a member of the closed level-2 enum; a studio portfolio is published work, in the solo_founder partition |
| pattern | `content-publishing` | `content-publishing` | legal as given |
| archetype | `creative-studio-showcase` | unchanged, `-vb` suffix | three tokens, kebab-case, unclaimed |
| profile | none | `P4-db-storage` | the only legal profile for the content-publishing pattern |
| companion | `Drive_PRDs/16_sept/noth_prd.md` | variant `b` | stage-1: a companion forces variant b on `critical_depth` and `spec_sections` |

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Scroll-driven home route of thirteen bands as the manifesto | INCLUDED | ## Core features, ## Front-end specification | the idea's home route |
| Works index of seven published case studies | INCLUDED | ## Core features, ## Front-end specification | the idea's catalogue |
| Case study route with next subject and compact list | INCLUDED | ## Core features, ## Front-end specification | one route per project |
| Muted showreel and manifesto film with the SOUND toggle | INCLUDED | ## Core features, ## Front-end specification | the idea's reel; stand-ins drawn and streamed into `video` elements |
| Playful not-found route with a real 404 | INCLUDED | ## Core features, ## Front-end specification | the idea's not-found route and the custom_404 draw |
| Booking a call files an enquiry from a slide-over panel | INCLUDED | ## Core features | the Task Order's conversion; the companion's third-party scheduler replaced |
| Author and reader accounts, open signup, studio console | INCLUDED | ## User roles, ## Core features | the content-publishing row's roles |
| Drafts invisible by route, record, list and exact storage key | INCLUDED | ## Core features | the pattern's critical focus |
| Images as content-addressed objects in a private bucket | INCLUDED | ## Core features, ## Technical requirements | the storage slot |
| Privacy page, social previews, working links, page view record | INCLUDED | ## Core features, ## Technical requirements | the launch-surface draw |
| Pointer layer, object field, interference overlay, wordmark mechanism | INCLUDED | ## Front-end specification | companion SS 4, SS 8, SS 9 |
| Third-party scheduler for booking | DROPPED | 00-decisions.md | no network at run time; the call lands as an enquiry |
| Scrubbed-selector census and identifier naming | DROPPED | companion SS 7.9, SS 14.10, waived | build meta |
| Build order | DROPPED | companion SS 19, waived | a Build plan is not baseline |
| Evidence gaps and acceptance checklist | DROPPED | companion SS 22, SS 23, waived | provenance notes and grading meta, INV10 |

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_a_filed_enquiry_is_stored_as_a_row_carrying_every_submitted_field` (critical), `test_a_public_page_view_is_stored_as_a_row_with_route_and_time` (critical) and further tests reading rows through the shared backend adapter |
| `storage` | `minio` | MET | `test_an_uploaded_cover_is_stored_in_the_object_store_under_the_key_scheme` (critical), `test_a_draft_image_answers_404_by_its_exact_storage_key_to_a_visitor_and_a_reader` (critical) and further tests reading objects through the shared storage adapter |

No slot is UNMET.

## Grading surface

| Measure | Value |
|---|---|
| Workflows | 16 (solo_founder band 10 to 16) |
| Browser substeps | 64 |
| Pytest substeps | 107 |
| Browser to pytest substep ratio | 0.6 (G45 band 0.40 to 2.00) |
| Critical substeps | 13 |
| Non-happy-path workflow ids | 3: `booking_panel_rejects_invalid_fields_and_files_nothing`, `a_reader_cannot_read_another_readers_enquiry_or_reach_the_studio_console`, `a_draft_case_study_and_its_images_are_denied_to_everyone_but_an_author` |
| Pytest module | one, `tests/test_output.py`, 107 tests |
| Sections covered | core features, data integrity, authorization, edge cases |
| Checklist items | 281 |
| Judged criteria | 13 |

Rubric split: 13 positive, 0 negative. Positive point total 45.

| Dimension | Share | Target | Delta |
|---|---|---|---|
| `instruction_following` | 0.222 | 0.30 | -0.078 |
| `functionality` | 0.289 | 0.25 | +0.039 |
| `ux_flow` | 0.178 | 0.15 | +0.028 |
| `ui_visual` | 0.244 | 0.15 | +0.094 |
| `motion` | 0.022 | 0.05 | -0.028 |
| `accessibility` | 0.022 | 0.05 | -0.028 |
| `responsiveness` | 0.022 | 0.05 | -0.028 |

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Overview | 1977 | 700 | over-reference |
| User roles | 2254 | 1000 | over-reference |
| Core features | 10572 | 2400 | past-slice |
| User flow | 4413 | 1900 | past-slice |
| UI/UX notes | 7110 | 1700 | past-slice |
| Constraints | 787 | 800 | within |
| joined total | 27113 | 8800 | past-slice |

Length is reported, never failed. The draft rule, the graded critical focus, opens `## Core features`,
so the part of that section the advisory judge reads is the part the task turns on.

## Literals ledger

| Class | Count | Values |
|---|---|---|
| `account` | 4 | `author@example.com`, `reader@example.com`, `reader2@example.com`, `studio@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `endpoint` | 14 | `/api/health`, `/api/works`, `/api/services`, `/api/people`, `/api/settings`, `/api/auth/sign-up`, `/api/auth/sign-in`, `/api/auth/sign-out`, `/api/auth/me`, `/api/enquiries`, `/api/page-views`, `/api/works/{id}`, `/api/works/{id}/media`, `/api/works/{id}/unpublish` |
| `env_var` | 8 | `DATABASE_URL`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `DB_ADMIN_URL`, `DEKU_SERVICE_BACKEND`, `DEKU_SERVICE_STORAGE` |
| `number` | 10 | `1000`, `80`, `60`, `200`, `8`, `4.5:1`, `100px`, `90px`, `12px`, `10.8px` |
| `route` | 8 | `/works`, `/privacy`, `/sign-in`, `/sign-up`, `/account`, `/studio`, `/studio/enquiries`, `/og/<route name>.png` |
| `scheme` | 5 | `works/{work_id}/{sha256_of_bytes}.{ext}`, `og:title`, `og:image`, `page_view`, `enquiry` |
| `seed_record` | 43 | `solace`, `urbana`, `un-charted`, `kwm`, `tactify`, `kine`, `chemie-union`, `veloce`, `Solace`, `Urbana`, `Un_Charted`, `Kwm`, `Tactify`, `Kine`, `Chemie Union`, `Veloce`, `Lena March`, `Paolo Ferri`, `Ada Rinaldi`, `Amelie Ronsard`, `Motion & development by`, `Brand identities`, `Campaigns`, `Digital experiences`, `Events`, `Visual systems`, `founders & management`, `creative partners`, `Where taste meets meaning.`, `Creative studio in Milan`, `©24 . 26`, `Naught' to see here...`, `Naught'`, `Tell us your name`, `We need an email to reply to`, `That company name is too long`, `Pick what you have in mind`, `Pick a date from today on`, `Pick a time of day`, `Say a little about the project`, `That email and password do not match`, `That email is already registered`, `Thanks. We'll be in touch within one working day.` |
| `status` | 13 | `new`, `contacted`, `closed`, `author`, `reader`, `cover`, `gallery`, `morning`, `afternoon`, `full-bleed`, `coloured-band`, `split`, `gradient-band` |

106 entries. 3 are `verifier_only` and live in `[verifier].env` alone: `DB_ADMIN_URL`, `DEKU_SERVICE_BACKEND`, `DEKU_SERVICE_STORAGE`. Every other entry has `instruction.md` as a carrier, and G6
holds the bijection in both directions.

## Authoring documents

| Doc | Fed |
|---|---|
| `_spec/S_conte_cont_creative-studio-showcase-vb_20260916_103045/00-decisions.md` | the draws, the taxonomy substitution, where the Task Order and the companion disagree, the identity recast, the certification repairs and the companion carry table |
| `_spec/S_conte_cont_creative-studio-showcase-vb_20260916_103045/01-PRD.md` | ## Overview, ## Core features, ## Constraints |
| `_spec/S_conte_cont_creative-studio-showcase-vb_20260916_103045/02-TRD.md` | ## Technical requirements |
| `_spec/S_conte_cont_creative-studio-showcase-vb_20260916_103045/03-app-flow.md` | ## User flow, ## Deployment contract API shapes |
| `_spec/S_conte_cont_creative-studio-showcase-vb_20260916_103045/04-uiux-brief.md` | ## UI/UX notes, ## Front-end specification |
| `_spec/S_conte_cont_creative-studio-showcase-vb_20260916_103045/05-backend-schema.md` | ## Data model, ## User roles |
| `_spec/S_conte_cont_creative-studio-showcase-vb_20260916_103045/06-implementation-plan.md` | not emitted: `## Build plan` is not baseline |

## Certification reviews

Rendered from `_handoff/S_conte_cont_creative-studio-showcase-vb_20260916_103045.receipts.json`.

| Prompt | Gate | Verdict | Checks | Warn | N/A | Verifier |
|---|---|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | 4 | 0 | self |
| `QC_spec.md` | G34 | PASS | 15 | 4 | 0 | self |
| `qc_docker.md` | G35 | PASS | 105 | 1 | 3 | self |
| `qc_rubric.md` | G53 | PASS | 16 | 0 | 1 | self |
| `qc_solution_checklist.md` | G37 | CHANGES REQUIRED | 0 | 0 | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | 0 | 7 | self |
| `task_code_verifier.md` | G3 | VALID | 12 | 0 | 0 | self |

### QC_instruction.md

- Cycle 1, D2: the films were specified as stand-ins drawn on a drawing surface while the film contract speaks of muting, looping and caption tracks, so a canvas build and a video build both read as correct. `## Core features` now pins each film as a `video` element with the drawing surface streamed into it.
- Cycle 1, C2: 'announces its state to assistive technology' allowed a changing label, a live region or a pressed state. The toggle is now pinned as a toggle button that reads as pressed while sound is on.
- Cycle 1, C2: `GET /api/works` named the query `featured` with no value; it now reads `featured=true`.
- Cycle 1, C3: the rule that another reader's enquiry answers as a missing record had no read path in the API table. `GET /api/enquiries/{id}` is added, with `404` for anything but the owner or an author.
- Cycle 1, C2: nothing said where the entities live by name; each entity is now one table named as the entity, and a page view's route is stored as the path, such as `/works`.
- Cycle 1, C6: `PostgreSQL` had crept into a `## Data model` sentence; it now says table. The provider remains named in `## Technical requirements`, `## Constraints` and the No mocks block, where SS 4 requires it.
- Cycle 1, D3a: the Definition of done ran to 101 words and restated the not-found rule and the sound constraint. It is now three sentences and 84 words: the stranger's booking, reader isolation, and the draft boundary including the exact storage key.
- A3: the thirteen canonical contract lines are present unaltered, and the stale 'different container' rationale appears nowhere.
- A4: the remaining angle-bracket segments, `<slug>`, `<storage key>` and `<route name>`, are route parameters, not unfilled placeholders.
- A8: the agent variables are DATABASE_URL, APP_PUBLIC_URL, APP_PUBLIC_PORT, STORAGE_ENDPOINT, STORAGE_BUCKET, STORAGE_ACCESS_KEY and STORAGE_SECRET_KEY. `DB_URL` exists only in task.toml as the kit's alias.
- B2: 'Drafts and publication' is numbered rules 1 to 5 with the negative case stated: a draft's route, record, list entry and images, including a request by exact storage key, answer `404` to anyone but an author, and the object stays in the store.
- B4: the seed carries `Veloce`, a draft with a cover and four gallery objects, and two readers with one enquiry each, so both boundaries are observable.
- D1: the lazy build that hides a draft's card but serves its route or image is named as a contract violation in the No mocks block and refused by rules 1 and 3; enquiries must be rows and images must be objects.
- D3 and D4: no sentence names a verifier, grader, harness or checker, and none says what backing service is inspected.
- D5: the sound toggle's state lasting for the session while every film starts muted on a route change looks like a contradiction, but both lines are the companion's own, SS 5.7 and SS 9.2 point 2, and are carried as stated. No brief line inverts its source.
- A1: `## Build plan` is absent and `## Front-end specification` stands in its place. generate_instruction.md SS 2.1 states a Build plan is not baseline and a numbered implementation sequence removes the design work being measured; A1 still lists it. The companion's visual specification needs the Front-end section, which SS 1 rule 2 names as its legal home.
- B3: Two of the three levers are emitted; `## Build plan` is the third and SS 2.1 forbids it at baseline. Same kit contradiction as A1.
- C4: `## UI/UX notes` carries exact type families and pixel sizes. C4 treats pinned type as a value sheet; generate_instruction.md SS 4 'The number rule, DECIDED (A5)' requires the exact family and size, and G51 measures it. Colour is family, tone and shade words; motion, space and breakpoints are words; no hex, millisecond or cubic-bezier appears.
- C7: `## Core features` (about 10,300 characters), `## User flow` and `## UI/UX notes` run past the judge's 2,500-character slice. G33 retired length as a failure. The draft rule, the graded critical focus, is the first subsection of Core features, so the part the judge reads is the part that matters.

### QC_spec.md

- Cycle 1, G2: `05-backend-schema.md` named the enquiry column `service_label` while the brief and the API table say `service`. The spec now says `service`, and states that each entity is one table named as the entity.
- Cycle 1, G2: `03-app-flow.md` lacked `GET /api/enquiries/{id}` and the `featured=true` query that the brief gained during certification; both are now listed.
- B1: the content-publishing row is db plus storage, PostgreSQL plus MinIO, roles author and reader, critical focus 'object in store; protected content not publicly readable'. 02-TRD declares both providers, 05-schema both roles, and solo_founder open signup is stated.
- B2: the seed has one draft with five stored objects and two readers with one enquiry each.
- G1: author@example.com, reader@example.com, reader2@example.com and studio@example.com appear in both spec and brief with `deku-demo-pw-2026`.
- G3: every entry under `Where the Task Order and the companion disagree`, `Judgment calls`, `Identity recast` and `Consistency repairs made during certification` is reflected in the brief.
- S10: no placeholder, no canary text; seeded emails follow `<role>@example.com`, with `reader2@example.com` for isolation.
- S1: Six documents are present; `06-implementation-plan.md` is not. It maps to `## Build plan`, which generate_instruction.md SS 2.1 forbids at baseline. Same kit contradiction as QC_instruction A1.
- S5: `04-uiux-brief.md` carries colour as family, tone and shade words and motion as words, not the hex and millisecond values S5 asks for. generate_instruction.md SS 4, the A5 number rule, bans those values and G51 carries the companion's measured facts in words; reference/L SS L.6.1 hands the design axes to the companion.
- S7: No implementation plan exists to shape, for the reason given under S1.
- S8: `00-decisions.md` opens with a `draw:` block. S8 calls restated derivation facts noise; generate_instruction.md SS 2.9 and SS 2.10 require these lines and G49 reads them.

### qc_docker.md

- Cycle 1, CMP-004: `main` depended on `minio` being healthy but not on the bucket existing, and the app seeds into that bucket on start. `minio-init` now carries a healthcheck on `mc stat local/deku`, and `main` waits for it to be healthy.
- RUN-001 and BC-004: the TRD declares Python 3.12 with Flask, Jinja, gunicorn, psycopg, boto3 and Pillow; the base is the digest-pinned python:3.12-slim-bookworm and each library is pinned in the image.
- HAL-001: the MinIO image is pulled from quay.io/minio/minio by digest, because Docker Hub answered 401 to the digest lookup. It is the upstream project's own registry and the same release.
- CMP-018: PostgreSQL and MinIO state sit on the named volumes `postgres-data` and `minio-data`; the only bind mount is the read-only bundle-relative init SQL.
- SEC-001: the MinIO root credential in the compose file equals the STORAGE_SECRET_KEY default in task.toml, which the app needs to write objects; the bucket's anonymous policy is set to none.
- SEC-003: the image runs as root, as every reference environment under tasks/ does.
- DEP-015: no `--break-system-packages` and no pip fallback appear; the language is Python, so the compiled-language multi-stage rule does not apply.
- DEP-016, DEP-017 and BP-008 concern compiled languages and musl bases; the language is Python on a glibc base.
- CMP-011: `main` publishes `4173:4173`. CMP-011 asks for no published ports; CMP-022 and stage-5 C12 require `main` to set `ports` and `extra_hosts`, because a missing host-gateway mapping loses every trial. CMP-022 governs. `postgres`, `minio` and `minio-init` publish nothing.

### qc_rubric.md

- Cycle 1, RC-12: three criteria were decidable by a page probe: the neutral public palette by computed colours, the resting pill label's contrast by computed colours, and touch pill borders by computed border alpha. R2 now grades whether the home route keeps the work in front with nothing covering it, R12 whether keyboard focus on the booking panel's service pills is visible, and R13 whether the not-found letters gather toward the middle at a phone width.
- Cycle 1, RC-04: the home route markup pytest also asserted the manifesto centre line that R5 judges; the pytest no longer reads that line.
- Cycle 1, RC-09: R6 offered a third state ('mostly vertically'); the rule is now binary.
- Cycle 1, RC-05: R11 named no surface; the criterion now names the works index.
- RC-01: every judgment-class checklist item is claimed by a criterion or cited by a browser substep, never both; 13 items are claimed by criteria.
- RC-07: every rule opens by saying what its named surface is.
- RC-13: positive shares are instruction_following 0.222, functionality 0.289, ux_flow 0.178, ui_visual 0.244, motion 0.022, accessibility 0.022, responsiveness 0.022; 10 of 13 criteria are task completion.
- RC-10: no negative criterion is emitted, because the brief licenses none.
- RC-14: rubric.json and tests/rubric.json were produced by recompute.py from grounding.yaml, not edited.
- RC-15: converged on cycle 2 of a permitted three.

### qc_solution_checklist.md

- NEEDS REVIEW. The machine layer reports no structural failure, no uncovered obligation and no ledger shortfall. Two values are declared under `Referenced but not pinned`: the bearer token and the generated stand-in images. Neither is asserted as a literal by any grader, a token's format is the app's to choose, and the stand-in bytes are generated, so both are recorded rather than resolved. SS 5 grades an unpinned value that does not block as NEEDS REVIEW.
- Each of the 281 items was written against its observer: a browser step, a pytest function or a judged criterion. The builder refused any citation where the item and the observer shared fewer than two content words, and the 53 wording and citation problems its first pass raised were fixed before emission. Every section carries at least as many items as obligation-bearing sentences.

### qc_toml.md

- META-009: keywords read greenfield, solo_founder, python, postgres, minio, portfolio, studio: category, sub_category, language, providers in slot order, then topical terms.
- SVC-004 and VERIF-006: `backend = postgres` then `storage = minio`, with markers DEKU_SERVICE_BACKEND and DEKU_SERVICE_STORAGE.
- VERIF-007: STORAGE_ENDPOINT, STORAGE_BUCKET, STORAGE_ACCESS_KEY and STORAGE_SECRET_KEY are in `[verifier].env` with the same defaults as `[environment].env`, so the verifier reads the same bucket the app writes.
- SEC-001: DB_ADMIN_URL sits in `[verifier].env` only.
- INST-001: the storage slot is exercised by the draft boundary and the key scheme; no email, payments or search journey exists, and none is provisioned.
- META-010: uuid_v5 was minted by `task_code.py uuid5` for this task code.
- BENCH-001: the Standard tier values are exact.
- SIGN-001 to SIGN-003 are retired rows; TAX-006, BENCH-002 and INST-007 govern trivial tasks and an absent brief; TAX-008 is informational and the mint ledger holds uniqueness.

### task_code_verifier.md

- The code reads S, conte, cont, creative-studio-showcase, vb, 20260916_103045: solo_founder, content-publishing domain, content-publishing pattern, the archetype, variant b and a well-formed stamp.
- PROFILES for the solo_founder content-publishing cell: P4-db-storage alone. task.toml declares P4-db-storage.
- The Task Order's `portfolio-agency` is not a member of the closed domain enum; the code carries `conte`, and the substitution is logged in `00-decisions.md`.
- Global archetype uniqueness is not checkable from one code; the mint ledger enforces it.

## Kit gate log

Rendered from `_handoff/S_conte_cont_creative-studio-showcase-vb_20260916_103045.gates.jsonl`. Never transcribed.

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
| G59/G60 | `codequality_lint.py` | 2 | ? |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS |
| G6 | `fixture_lint.py` | 0 | PASS |
| G24 | `coverage_map.py` | 0 | PASS |
| G37 | `checklist_qc.py` | 0 | PASS |
| G39 | `rubric_align_lint.py` | 0 | PASS |
| G28/G29 | `channel_lint.py` | 0 | PASS |
| G40 | `prompt_receipt_lint.py` | 0 | WARN |
| G0/INV5 | `vendor_check.py` | 0 | PASS |
| G47 | `output_qc.py` | 0 | PASS |

## Handoff gate list

Undecided here. See `_handoff/S_conte_cont_creative-studio-showcase-vb_20260916_103045.handoff.md` for commands and expected verdicts:
G13, G15, G18, G19, G20, G21, G25.

## Blocking findings

None blocks a test. Two values are referenced but not pinned, the bearer token and the generated
stand-in image bytes; no grader asserts either as a literal. `qc_solution_checklist` records that
as NEEDS REVIEW.

## Effort estimate

`turns_expected = 200`, `tokens_expected = 8000000`. The build is a Flask application with
server-rendered Jinja pages and Alpine islands, a hand-written scroll and pointer layer driving
thirteen scrubbed bands, generated films streamed into video elements, a generated audio graph,
an identity layer with bearer tokens and cookies, a studio console, and a private object store
behind a media route that has to refuse a draft's image even by its exact key.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`
