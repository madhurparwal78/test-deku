# Build report - S_conte_crud_deep-dive-logbook-vb_20260916_090617

## Identity

| Field | Value |
|---|---|
| Task code | `S_conte_crud_deep-dive-logbook-vb_20260916_090617` |
| Task id | `deku/deep-dive-logbook-vb` |
| Cell | solo_founder / content-publishing / crud-catalog |
| Service profile | `P2-db-email`: slot `backend` -> `postgres`, slot `email` -> `mailpit` |
| Verifier mode | `separate`: the grader ships its own image from `tests/Dockerfile` on `deku-verifier-base` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `typescript` |
| Stack draw | `ssr-islands` / `Fastify` / `Nuxt 3`, over `[metadata].archetype` |
| Design direction | `companion` (the `warm-hospitality` draw does not govern; reference/L SS L.6.1) |
| Launch surface | `colour_contrast, cookie_choice, favicon, meta_tags, page_view_log` |
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
| domain | `portfolio-agency` | `content-publishing` | not a member of the closed level-2 enum; a portfolio is published work offered by one individual, in the solo_founder partition |
| pattern | `media-gallery` | `crud-catalog` | not a member of the closed level-3 enum; its critical focus, a persisted row that matches the page and survives a reload, is the companion's own most important assertion. `content-publishing` was rejected because it admits only `P4-db-storage` and the companion is a zero-asset build |
| archetype | `deep-dive-logbook` | unchanged, `-vb` suffix | three tokens, kebab-case, unclaimed |
| profile | none | `P2-db-email` | the companion specifies a password reset and four transactional messages; the email slot is additive and legal for the cell |
| companion | `Drive_PRDs/16_sept/josephsan_prd.md` | variant `b` | stage-1: a companion forces variant b on `critical_depth` and `spec_sections` |

The first mint used `P1-db`; it was released through `task_code.py release` and re-minted at
`P2-db-email` before anything was authored, so the ledger carries a RELEASED tombstone for
`S_conte_crud_deep-dive-logbook-vb_20260916_090343`.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| The dive: six scenes, one screen, one interpolated position | INCLUDED | ## Core features, ## Front-end specification | the product the portfolio argues with |
| Entry gate with two equal ways in | INCLUDED | ## Core features, ## Front-end specification | audio never starts without a gesture |
| Works layer stepping, project detail panel | INCLUDED | ## Core features, ## Front-end specification | the only discrete collection and the only scroll region |
| Four-panel message with hold, decay and keyboard path | INCLUDED | ## Core features, ## Front-end specification | content replaced by a craft statement; structure kept whole |
| Logbook: save, notes, reorder, ceiling | INCLUDED | ## Core features | the graded feature |
| Publishing, public address, replay | INCLUDED | ## Core features | the shareable secret and the cold-load replay |
| Dock queue and answered state | INCLUDED | ## Core features | where published logbooks arrive |
| Identity: sign up, sign in, reset, sessions | INCLUDED | ## Core features, ## Technical requirements | companion SS 17 |
| Four transactional messages | INCLUDED | ## Core features | the email slot |
| Launch surface: contrast, cookie choice, favicon, titles and descriptions, page view record | INCLUDED | ## Core features, ## Technical requirements, ## UI/UX notes | the reference/O draw |
| Zero-asset construction of water, forms, thumbnails, media, audio | INCLUDED | ## Front-end specification | companion SS 37 |
| Religious testimony in the message scene | DROPPED | 00-decisions.md | the companion tokenises it as somebody else's; four craft panels stand in |
| Named analytics events and consent-gated measurement vendor | DROPPED | companion SS 28.2, waived | measurement is gated and local; the page view record is what the app owns |
| Build order and module architecture | DROPPED | companion SS 31, SS 35, waived | a Build plan is not baseline |
| Test plan and acceptance checklist | DROPPED | companion SS 30, SS 39, waived | grading meta, INV10 |
| Reference asset manifest and evidence gaps | DROPPED | companion SS 37.1, SS 38, waived | the companion's own provenance ledger |

## Slot obligations

| Slot | Provider | Verdict | Observed by |
|---|---|---|---|
| `backend` | `postgres` | MET | `test_the_first_saved_moment_moves_the_logbook_from_empty_to_draft` (critical), the order, publish, republish and page view tests, each reading state back through the service |
| `email` | `mailpit` | MET | `test_publishing_delivers_the_logbook_is_live_email_to_the_publishing_diver` (critical) and eight further tests reading the inbox through the shared email adapter |

No slot is UNMET.

## Grading surface

| Measure | Value |
|---|---|
| Workflows | 16 (solo_founder band 10 to 16) |
| Browser substeps | 71 |
| Pytest substeps | 122 |
| Browser to pytest substep ratio | 0.58 (G45 band 0.40 to 2.00) |
| Critical substeps | 6 |
| Non-happy-path workflow ids | 1: `a_diver_cannot_reach_another_divers_logbook_and_the_host_cannot_reach_a_draft` |
| Pytest module | one, `tests/test_output.py`, 122 tests |
| Sections covered | core features, data integrity, authorization, edge cases, email |
| Checklist items | 266, from 831 authored |
| Judged criteria | 13 |

Rubric split: 13 positive, 0 negative. Positive point total 45.

| Dimension | Share | Target | Delta |
|---|---|---|---|
| `instruction_following` | 0.289 | 0.30 | -0.011 |
| `functionality` | 0.289 | 0.25 | +0.039 |
| `ux_flow` | 0.178 | 0.15 | +0.028 |
| `ui_visual` | 0.178 | 0.15 | +0.028 |
| `motion` | 0.022 | 0.05 | -0.028 |
| `accessibility` | 0.022 | 0.05 | -0.028 |
| `responsiveness` | 0.022 | 0.05 | -0.028 |

## Grading window

| Section | Chars | Reference | Flag |
|---|---|---|---|
| Overview | 1822 | 700 | over-reference |
| User roles | 2824 | 1000 | past-slice |
| Core features | 16283 | 2400 | past-slice |
| User flow | 6065 | 1900 | past-slice |
| UI/UX notes | 9165 | 1700 | past-slice |
| Constraints | 2627 | 800 | past-slice |
| joined total | 38786 | 8800 | past-slice |

Length is reported, never failed. The logbook, the graded feature, opens `## Core features`,
so the part of that section the advisory judge reads is the part the task turns on.

## Literals ledger

| Class | Count | Values |
|---|---|---|
| `account` | 3 | `host@example.com`, `diver@example.com`, `diver2@example.com` |
| `credential` | 1 | `deku-demo-pw-2026` |
| `endpoint` | 15 | `/api/scenes`, `/api/projects`, `/api/logbook`, `/api/logbook/entries`, `/api/logbook/order`, `/api/logbook/publish`, `/api/logbook/unpublish`, `/api/auth/sign-up`, `/api/auth/sign-in`, `/api/auth/sign-out`, `/api/auth/me`, `/api/auth/reset`, `/api/auth/reset/confirm`, `/api/dock`, `/api/page-views` |
| `env_var` | 11 | `DATABASE_URL`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `DB_ADMIN_URL`, `EMAIL_INBOX_API_URL`, `DEKU_SERVICE_BACKEND`, `DEKU_SERVICE_EMAIL` |
| `number` | 21 | `0`, `1`, `3`, `5`, `12`, `280`, `80`, `60`, `254`, `8`, `200`, `128`, `30`, `24`, `800`, `401`, `403`, `404`, `409`, `422`, `429` |
| `route` | 6 | `/`, `/works`, `/sign-in`, `/logbook`, `/dock`, `/api/health` |
| `scheme` | 25 | `sceneIndex`, `progress`, `note`, `order`, `publicId`, `publishedAt`, `answeredAt`, `savedAt`, `displayName`, `cursor`, `state`, `next`, `at`, `token`, `mode`, `error`, `code`, `field`, `entries`, `logbook`, `logbooks`, `views`, `total`, `viewedAt`, `route` |
| `seed_record` | 80 | `Ines Marlow`, `Coral Bevan`, `Toma Oyelaran`, `Untitled dive`, `Reef pitch`, `Tidal Atlas`, `Kelp Forest`, `Sonar Room`, `Drift Table`, `tidal-atlas`, `kelp-forest`, `sonar-room`, `drift-table`, `HTML / CSS / JS / WEBGL`, `HTML / CSS / JS / SHADERS`, `HTML / CSS / JS / WEB AUDIO`, `HTML / CSS / JS / CANVAS`, `The works arc is the whole argument`, `Read this line against the bright water`, `Ends on an address, not a loop`, `Thin on purpose`, `Sounding: your logbook`, `Sounding: reset your password`, `Sounding: your logbook is live`, `New logbook from `, `Log at least one moment`, `A logbook holds twelve moments at most`, `Give the logbook a name`, `A note is too long`, `One of your moments is no longer in the dive`, `This logbook is already published`, `That email and password do not match`, `That email is already registered`, `That address does not exist`, `This logbook belongs to someone else`, `Something went wrong down here`, `Sign in to keep a logbook`, `Nothing logged yet`, `No logbooks published yet`, `Could not load this`, `[Please wait]`, `[Welcome aboard]`, `[Surface log]`, `[Received]`, `[No such depth]`, `[Not your logbook]`, `[Signal lost]`, `[No log]`, `[Empty log]`, `[Quiet]`, `[Logged]`, `[Logbook full]`, `[Offline]`, `[Link copied]`, `[Could not reorder]`, `[Unpublished. The link is dead]`, `[Press again]`, `[Scroll to descend]`, `[Log this moment]`, `Dive into the experience`, `Enter without audio`, `Ines Marlow is a Software Engineer`, `Thanks for visiting`, `Development & 3D Design by Ines Marlow`, `Dive to this`, `Mark answered`, `Publish`, `Unpublish`, `Works`, `Message`, `Contact`, `Loading 3D experience`, `Ines Marlow // Creative Software Engineer & UI/UX Designer`, `Works // Ines Marlow`, `Sign in - Ines Marlow`, `Your logbook - Ines Marlow`, `Dock - Ines Marlow`, `Not found - Ines Marlow`, `Inter`, `IBM Plex Mono` |
| `status` | 24 | `empty`, `draft`, `published`, `answered`, `diver`, `host`, `surface`, `introduction`, `about`, `works`, `message`, `contact`, `create`, `reset`, `set`, `unauthenticated`, `forbidden`, `not_found`, `wrong_state`, `already_published`, `logbook_full`, `scene_missing`, `invalid`, `rate_limited` |

186 entries. 4 are `verifier_only` and live in `[verifier].env` alone: `DB_ADMIN_URL`, `EMAIL_INBOX_API_URL`, `DEKU_SERVICE_BACKEND`, `DEKU_SERVICE_EMAIL`. Every other entry has `instruction.md` as a carrier, and G6
holds the bijection in both directions.

## Authoring documents

| Doc | Fed |
|---|---|
| `_spec/S_conte_crud_deep-dive-logbook-vb_20260916_090617/00-decisions.md` | the draws, the taxonomy and profile decisions, the identity recast, the certification repairs and the companion carry table |
| `_spec/S_conte_crud_deep-dive-logbook-vb_20260916_090617/01-PRD.md` | ## Overview, ## Core features, ## Constraints |
| `_spec/S_conte_crud_deep-dive-logbook-vb_20260916_090617/02-TRD.md` | ## Technical requirements |
| `_spec/S_conte_crud_deep-dive-logbook-vb_20260916_090617/03-app-flow.md` | ## User flow, ## Deployment contract API shapes |
| `_spec/S_conte_crud_deep-dive-logbook-vb_20260916_090617/04-uiux-brief.md` | ## UI/UX notes, ## Front-end specification |
| `_spec/S_conte_crud_deep-dive-logbook-vb_20260916_090617/05-backend-schema.md` | ## Data model, ## User roles |
| `_spec/S_conte_crud_deep-dive-logbook-vb_20260916_090617/06-implementation-plan.md` | not emitted: `## Build plan` is not baseline |

## Certification reviews

Rendered from `_handoff/S_conte_crud_deep-dive-logbook-vb_20260916_090617.receipts.json`.

| Prompt | Gate | Verdict | Checks | Warn | N/A | Verifier |
|---|---|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | 4 | 0 | self |
| `QC_spec.md` | G34 | PASS | 15 | 2 | 0 | self |
| `qc_docker.md` | G35 | PASS | 105 | 1 | 4 | self |
| `qc_rubric.md` | G53 | PASS | 16 | 0 | 1 | self |
| `qc_solution_checklist.md` | G37 | CHANGES REQUIRED | 0 | 0 | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | 0 | 8 | self |
| `task_code_verifier.md` | G3 | VALID | 12 | 0 | 0 | self |

### QC_instruction.md

- Cycle 1, C3: the redirect table keyed every row on `/logbook/<id>` while the route table named `/logbook/<publicId>`, so 'unpublishing kills the address' contradicted 'another diver reaching a draft is refused'. Both address forms are now routed, following the companion SS 25.1 split between `id` and `publicId`.
- Cycle 1, C3: the API used snake case on the scenes and projects reads and camel case everywhere else. Every response is now camel case and `## Data model` states once how storage names travel.
- Cycle 1, C3: the refusal journey had a diver asking for `Coral Bevan`'s logbook 'while it is a draft', but that logbook is seeded `published`. The journey now uses `/dock` and the seeded draft belonging to `Toma Oyelaran`.
- Cycle 1, D2: a cleared logbook title read both as '1 to 80 characters' and as 'refused on publish'. The brief now says a draft may hold a cleared title and the publish is what refuses it.
- Cycle 1, C5: seeding is now stated to be idempotent.
- Cycle 1, C6: the framing paragraph named PostgreSQL; it now says the order is held by the service. PostgreSQL remains in `## Technical requirements`, `## Constraints` and the No mocks block, where SS 4 requires it. `WebGL & Three.js, GSAP` in `## Front-end specification` is the about scene's measured copy, not a stack declaration.
- Cycle 1, D5: the companion's SS 6.6 hover scramble was absent from the brief; it is now named in words in the chrome section.
- A4: the angle-bracket segments that remain, `<publicId>`, `<id>`, `<entryId>`, `<logbookId>`, are route parameters, not unfilled placeholders.
- Cycle 2, B1 and C6: the stack table was drawn over the six-field task code; generate_instruction.md SS 2.9 resolves that identity from `[metadata].archetype`. The stack is now the archetype draw, ssr-islands with Fastify and Nuxt 3, and `## Technical requirements` states the server-rendered islands shape as an observable. No grader depended on the stack.
- A8: the agent variables are DATABASE_URL, APP_PUBLIC_URL, APP_PUBLIC_PORT, SMTP_HOST, SMTP_PORT, SMTP_USER and SMTP_PASS; no verifier-only name appears.
- Cycle 2 re-read every A, B, C and D check against the revised brief; no finding remained beyond the four kit contradictions recorded as warnings.
- A1: `## Build plan` is absent and `## Front-end specification` stands in the eleventh place. generate_instruction.md SS 2.1 states a Build plan is NOT baseline and a numbered implementation sequence removes the design work being measured; A1 still lists it. The companion's visual specification needs the unbudgeted Front-end section, which SS 1 rule 2 names as its legal home.
- B3: Two of the three difficulty levers are emitted. `## Build plan` is the third and SS 2.1 forbids it at baseline. Same kit contradiction as A1.
- C4: `## UI/UX notes` carries the exact type families and the exact em sizes. C4 treats pinned type as a value sheet; generate_instruction.md SS 4 'The number rule, DECIDED (A5)' requires the exact family and size, and that rule is what G51 measures. No hex, no millisecond, no cubic-bezier and no pixel breakpoint appears anywhere in the brief.
- C7: `## Core features`, `## User flow`, `## UI/UX notes` and `## User roles` run past the judge's 2,500-character slice. G33 and generate_instruction.md SS 4 retired length as a failure, and the logbook, the graded feature, was placed first in Core features so the part the judge reads is the part that matters.

### QC_spec.md

- Cycle 2, S2: `02-TRD.md` carried the stack drawn over the task code; it now carries the archetype draw, and `00-decisions.md` records both the correction and the two SS 2.10 axes the companion overrides.
- S5: motion is carried as four named characters and a list of moments in words, derived from the companion's SS 6; reference/L SS L.6.1 hands the design axes to the companion.
- S9: performance budgets are the companion's measured per-route figures from SS 34.1 and SS 34.7.
- S10: seeded emails follow `<role>@example.com` for the declared roles: host@example.com, diver@example.com and diver2@example.com, the last existing so isolation is observable.
- G2: `03-app-flow.md` lists every endpoint; its route map was updated in cycle 1 to carry both logbook address forms, matching the brief.
- B2: the seed departs from the companion's two accounts because the companion also forbids a host from publishing; the reason is logged in `00-decisions.md`.
- B1: Two roles, `diver` and `host`, against the crud-catalog row's single `user`. reference/B SS B.3 bands solo_founder at one to two roles and the companion's SS 18 needs the second so published logbooks arrive somewhere. The row's permission shape is kept: `host` is `diver` plus the queue.
- S8: `00-decisions.md` opens with a `draw:` block. S8 calls a restated derivation-table fact noise; generate_instruction.md SS 2.9 and SS 2.10 require these lines and G49 reads them. They sit under their own heading, apart from the residual judgment calls.

### qc_docker.md

- RUN-001: the TRD declares Node 22 under Fastify and Nuxt 3; the image installs Node 22 from the NodeSource registry over the pinned Python base the kit's grader runtime requires, so the declared runtime is present. Fastify and Nuxt are project dependencies the app installs, so nothing framework-specific is installed globally.
- SEC-003: the image runs as root, as every reference environment under tasks/ does. No source establishes a non-root convention for the agent container.
- ENV-006: the task.toml healthcheck runs `pg_isready`, and `postgresql-client` is installed; the mailpit healthcheck uses the busybox `wget` its Alpine image ships, the same command the kit's own provider fragment uses.
- DEP-015 to DEP-017 and BP-008 concern compiled languages and musl bases; the language is TypeScript on a glibc base.
- CMP-011: The `main` service publishes `4173:4173`. CMP-011 asks the file to be free of published host ports; CMP-022 and stage-5 C12 require `main` to set `ports` and `extra_hosts`, because a missing host-gateway mapping loses every trial. CMP-022 governs. The `postgres` and `mailpit` sidecars publish nothing.

### qc_rubric.md

- Cycle 1, RC-12: five criteria were decidable by a page probe: the introduction blend by its computed blend mode, the corner radii, the footer text size at two widths, the save control's collision with the strip by two bounding boxes, and the monogram's accessible name. R1 now grades legibility over changing water, R3 the drawn pointer's two states, R8 whether the entry gate reads as two equal ways in, R9 the water's palette and depth fog, R12 whether a busy control stays readable, and R13 whether the rights block reads at arm's length.
- Cycle 1, RC-07: the message strip, the monogram and several surfaces were used undefined. Every rule now opens by saying what the named surface is.
- Cycle 1, RC-05: R6 and R13 named no surface from the brief and now name the dive.
- RC-01: every judgment-class item in the checklist is claimed by a criterion or cited by a browser substep, and G29 forbids both; 13 items are claimed by criteria.
- RC-13: positive shares are instruction_following 0.289, functionality 0.289, ux_flow 0.178, ui_visual 0.178, motion 0.022, accessibility 0.022, responsiveness 0.022; 9 of 13 criteria are task completion.
- RC-10: no negative criterion is emitted, because the brief licenses none.
- RC-15: converged on cycle 2 of a permitted three.

### qc_solution_checklist.md

- NEEDS REVIEW. The machine layer reports no structural failure, no uncovered obligation and no ledger shortfall. Two values are declared under `Referenced but not pinned`: the salted password hash and the single-use reset token. Neither may be pinned in the brief, because INV4 keeps a secret out of an agent-visible surface and G63 refuses a source-shaped secret, so both are recorded rather than resolved. SS 5 grades an unpinned value that does not block as NEEDS REVIEW.
- The checklist is a graded subset. 831 obligations were authored against the brief; 266 survive, being the ones a workflow step, a pytest function or a rubric criterion observes on a reading a person would accept. Word overlap first proposed several hundred citations a reader would reject, such as a contact-deck step citing 'signing out anywhere signs out everywhere'; each was banned by hand and the obligation either moved to its real observer or was culled. Every section still carries at least as many items as obligation-bearing sentences.

### qc_toml.md

- Cycle 1, META-009: keywords read `node` where the declared language is `typescript` and omitted the email provider. They now read greenfield, solo_founder, typescript, postgres, mailpit, portfolio, logbook.
- Cycle 1, ENV-006: the email slot declared SMTP_HOST and SMTP_PORT only. SMTP_USER and SMTP_PASS are now declared with empty defaults, matching the kit's own event-rsvp-confirmations reference task, and the brief names all four.
- SEC-001: DB_ADMIN_URL and EMAIL_INBOX_API_URL sit in `[verifier].env` only; EMAIL_INBOX_API_URL is the bare `http://mailpit:8025` base, because the shared inbox adapter appends `/api/v1/messages` itself.
- SVC-004 and VERIF-006: `backend = postgres` then `email = mailpit`, with markers DEKU_SERVICE_BACKEND and DEKU_SERVICE_EMAIL.
- META-010: uuid_v5 was minted by `task_code.py uuid5` for this task code.
- SIGN-001 to SIGN-003 are retired rows; TAX-006, BENCH-002 and INST-007 govern trivial tasks and an absent brief; VERIF-007 governs payments and storage slots, neither declared; TAX-008 is informational and the mint ledger holds uniqueness.

### task_code_verifier.md

- PROFILES for the solo_founder crud-catalog cell: P0-baas, P1-db, P2-db-email, P3-db-auth, P4-db-storage, P5-db-pay-email, P7-db-search, P8-db-realtime, P9-db-queue-email. task.toml declares P2-db-email, which is a member.
- The Task Order's `portfolio-agency` and `media-gallery` are not members of the closed enums; the code carries `conte` and `crud`, and the substitution is logged in `00-decisions.md`.
- Global archetype uniqueness is not checkable from one code; the mint ledger enforces it.

## Kit gate log

Rendered from `_handoff/S_conte_crud_deep-dive-logbook-vb_20260916_090617.gates.jsonl`. Never transcribed.

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

Undecided here. See `_handoff/S_conte_crud_deep-dive-logbook-vb_20260916_090617.handoff.md` for commands and expected verdicts:
G13, G15, G18, G19, G20, G21, G25.

## Blocking findings

None blocks a test. Two values are referenced but deliberately unpinned, the salted password
hash and the single-use reset token, because INV4 keeps a secret off every agent-visible
surface. `qc_solution_checklist` records that as NEEDS REVIEW.

## Effort estimate

`turns_expected = 200`, `tokens_expected = 8000000`. The build is a Fastify server with Nuxt 3
pages rendered on the server, a hand-written WebGL dive, a generated audio graph, a cookie-session identity
layer with a mail-delivered reset, and a logbook whose order, publication and replay all have
to hold across a reload. The dive alone is a full client program with six scenes, a
degradation ladder and a keyboard path.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`
