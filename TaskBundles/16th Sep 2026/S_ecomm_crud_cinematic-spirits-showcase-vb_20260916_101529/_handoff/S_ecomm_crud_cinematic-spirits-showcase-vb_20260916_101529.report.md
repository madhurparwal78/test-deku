# Build report: S_ecomm_crud_cinematic-spirits-showcase-vb_20260916_101529

## Identity

| Field | Value |
|---|---|
| Task code | `S_ecomm_crud_cinematic-spirits-showcase-vb_20260916_101529` |
| Task id | `deku/cinematic-spirits-showcase-vb` |
| Cell | solo_founder / ecommerce-retail / crud-catalog |
| Pattern note | the order named `catalog-browse`, which is not in the pattern table (G0); substituted `crud-catalog`, the catalogue pattern the kit carries |
| Archetype | `cinematic-spirits-showcase` |
| Service profile | `P2-db-email` |
| Providers | `backend` = `postgres`, `email` = `mailpit` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `typescript` (Fastify API, SolidStart front end with server-rendered islands, all drawn) |
| Design direction | `companion` |
| Launch surface | cookie_choice, favicon, mobile_viewport, sitemap_robots, terms_page |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 (single-task run) |
| Companion | `9.16_prds/prd10/santioni_prd.md` |
| Reference site | https://santionispirits.com/ |
| QL | kaustubh.dalvi@ethara.ai |
| Contributor | mansa.gupta@ethara.ai |

## Feature resolution

| Candidate | Verdict | Where |
|---|---|---|
| Auth | INCLUDED | `## Core features` rules 1 to 7 |
| The experience | INCLUDED | `## Core features` rules 8 to 15 |
| Gates before the story | INCLUDED | `## Core features` rules 16 to 21 |
| The two held gestures | INCLUDED | `## Core features` rules 22 to 27 |
| Sound | INCLUDED | `## Core features` rules 28 to 33 |
| The collection act | INCLUDED | `## Core features` rules 34 to 41 |
| The Cellar | INCLUDED | `## Core features` rules 42 to 58 |
| Where to drink it | INCLUDED | `## Core features` rules 59 to 74 |
| Tastings | INCLUDED | `## Core features` rules 75 to 89 |
| The Ritual | INCLUDED | `## Core features` rules 90 to 102 |
| The host's venue | INCLUDED | `## Core features` rules 103 to 106 |
| The rest of the product | INCLUDED | `## Core features` rules 107 to 113 |
| Retail purchase, cart and checkout | DROPPED | `## Constraints`; `00-decisions.md`: no buying anything; the only price is a tasting's |
| Third-party analytics and advertising pixels | DROPPED | `## Constraints`; `00-decisions.md`: companion rule D6 dropped; no external call at run time |
| Hosted map tiles, geocoding and routing | DROPPED | `## Constraints`; `00-decisions.md`: venue search uses a seeded gazetteer of 8 places and a drawn plan |
| Authoring tools (font editor, render statistics, live surface editor) | DROPPED | `## Constraints`; `00-decisions.md`: evidence of the reference build, not product |
| Administrator surface and venue onboarding | DROPPED | `## Constraints`; `00-decisions.md`: two roles only; hosts exist because they are seeded |
| Shipped image, model, font atlas and sound files | DROPPED | `## Constraints`; `00-decisions.md`: every film asset is generated at run time |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | `postgres` | MET | allocation, waitlist, alert, venue_stock, seat_hold, booking, ritual and account rows are read directly by the pytest module |
| `email` | `mailpit` | MET | sign-in links, waitlist offers, alert confirmations and landings, booking confirmations and venue cancellations are read from the Mailpit API |

## Grading surface

- Workflows: **16** (solo_founder band 10 to 16)
- Browser substeps: **37**   pytest substeps: **76**   critical substeps: **15**
- Non-happy-path workflow ids: `other_visitor_cannot_touch_a_shelf`, `unauthenticated_caller_is_denied_the_cellar`, `concurrent_or_invalid_claims_are_settled_by_the_server`, `visitor_cannot_change_venue_stock_or_sessions`, `invalid_or_excess_ritual_saves_are_refused`
- One pytest module, `tests/test_output.py`, carrying **76** test functions
- Rubric criteria: **25** (23 positive, 2 negative)
- Solution checklist: **503** items in `solution/checklist.md`

| Dimension | Share |
|---|---|
| `instruction_following` | 0.31 |
| `functionality` | 0.26 |
| `ux_flow` | 0.16 |
| `ui_visual` | 0.21 |
| `motion` | 0.02 |
| `accessibility` | 0.02 |
| `responsiveness` | 0.02 |

## Literals ledger

330 pinned values across 11 classes, every one present verbatim in `instruction.md`; verifier-only values live in `task.toml` alone.

| Class | Count |
|---|---|
| `account` | 5 |
| `credential` | 1 |
| `design_phrase` | 6 |
| `endpoint` | 40 |
| `env_var` | 9 |
| `motion_moment` | 8 |
| `number` | 28 |
| `route` | 20 |
| `scheme` | 23 |
| `seed_record` | 99 |
| `status` | 91 |

## Authoring documents

| Document | Fed |
|---|---|
| `00-decisions.md` | the draw record, input correction, scope calls and the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow` |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` (measured values stay here, author-side) |
| `05-backend-schema.md` | `## Data model`, `## User roles`, `## Deployment contract` |
| `06-implementation-plan.md` | author-side only; `## Build plan` is not emitted at baseline |
| `g51-waivers.txt` | the 29 G51 waivers passed to the sweep |

## Grading window

| Section | Chars |
|---|---|
| Overview | 3565 |
| User roles | 2590 |
| Core features | 47105 |
| User flow | 7790 |
| UI/UX notes | 12712 |
| Technical requirements | 7687 |
| Data model | 5726 |
| Front-end specification | 27725 |
| Constraints | 1456 |
| Deployment contract | 8096 |
| Definition of done | 389 |

The order waived length and per-section caps. `window_lint.py` fails nothing on length; prose past the judge's slice still reaches the agent in full.

## UI/UX carriage

Per the order and `generation_instruction_guidelines (1).md`, the visual system is described in words only: a north star, a register, "X over Y" stances, colour by family and tone, type by personality, motion as named moments in plain words. No pixel values, positions, sizes, colour codes, durations, font family names, animation or function names or parameter values appear in the brief. Tech stacks are named. Hooks, copy, content facts and accessibility floors are written exactly. The measured values from the companion stay author-side in `04-uiux-brief.md`.

## Kit gate log

Rendered from `_handoff/S_ecomm_crud_cinematic-spirits-showcase-vb_20260916_101529.gates.jsonl`. Never transcribed.

| Gate | Tool | Exit | Verdict | Output SHA |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | 0 | PASS | `f8effc1b278f3a99` |
| `G1/G12` | `layout_lint.py` | 0 | PASS | `d7ac2898529eb5dc` |
| `G46` | `structure_lint.py` | 0 | PASS | `6cd81b95fcdbb62d` |
| `G50` | `docker_lint.py` | 0 | PASS | `380ed7d1c830de35` |
| `G55` | `runtime_deps_lint.py` | 0 | PASS | `a0c21dca8bc5f78a` |
| `G63` | `secret_lint.py` | 0 | PASS | `edf08d66c697cfd0` |
| `G48` | `truth_lint.py` | 0 | PASS | `5f74288ee1343865` |
| `G51` | `source_lint.py` | 0 | PASS | `825fd8134b8fa51f` |
| `G52` | `rubric_context_lint.py` | 0 | PASS | `f2537943e61facd1` |
| `G54` | `comment_lint.py` | 0 | PASS | `33af15f28efdbdf5` |
| `G17` | `secret_hygiene_lint.py` | 0 | PASS | `d9053573ad842071` |
| `G11` | `leak_scan.py` | 0 | PASS | `b40f41b8a6e4aafa` |
| `G33` | `window_lint.py` | 0 | PASS | `41b6c179a3e8a1ad` |
| `G4/G5` | `contract_lint.py` | 0 | PASS | `66da11b948b843f2` |
| `G43` | `prescription_lint.py` | 0 | PASS | `c2026524c6716f40` |
| `G44` | `disclosure_lint.py` | 0 | PASS | `40b0b49d23609083` |
| `G10` | `no_sdk_lint.py` | 0 | PASS | `4b51e847a5f2e328` |
| `G31` | `determinism_lint.py` | 0 | PASS | `c73323ac382cee1b` |
| `G14` | `reward_path_lint.py` | 0 | PASS | `1acc6ea17571593c` |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | `b4146d142747301d` |
| `G41` | `flag_lint.py` | 0 | PASS | `ac3d7f5fa4f8b8b3` |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | `cdf20c83e9056866` |
| `G59/G60` | `codequality_lint.py` | 2 | ? | `e23941dd85e0253b` |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | `a2227f769bbec512` |
| `G6` | `fixture_lint.py` | 0 | PASS | `ed3c6bd27efe183e` |
| `G24` | `coverage_map.py` | 0 | PASS | `63218807ace98618` |
| `G37` | `checklist_qc.py` | 0 | PASS | `3cdcaf290aae4d15` |
| `G39` | `rubric_align_lint.py` | 0 | PASS | `bb587b2532d0bb64` |
| `G28/G29` | `channel_lint.py` | 0 | PASS | `e280453e4b1e24e7` |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | `70eb37d6d424793b` |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | `e05d8ce49ed806ca` |
| `G47` | `output_qc.py` | 0 | PASS | `b9818d88bc2572d4` |

`G59/G60` exits 2 (NOT-APPLICABLE) when present: the bundle carries no reference code to lint.

## Certification prompt receipts

| Prompt | Gate | Verdict | Checks | Non-pass | Verifier |
|---|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | A1, A2, A3, B1, B2, B3, C2, C3, C4, C5, C7, D3 | independent-subagent-reviewer |
| `QC_spec.md` | G34 | PASS | 15 | - | independent-subagent-reviewer |
| `docker_generator.md` | S5 | PASS | 0 | - | self |
| `generate_instruction.md` | S2 | PASS | 0 | - | self |
| `pytest_generator.md` | S7 | PASS | 0 | - | self |
| `qc_docker.md` | G35 | PASS | 105 | BP-001, BP-003, BP-007, CMP-011, CON-004, RUN-005 | independent-subagent-reviewer |
| `qc_rubric.md` | G53 | PASS | 16 | RC-01, RC-03, RC-04, RC-05, RC-06, RC-07, RC-08, RC-09, RC-11, RC-12, RC-16 | independent-subagent-reviewer |
| `qc_solution_checklist.md` | G37 | PASS | 0 | - | independent-subagent-reviewer |
| `qc_toml.md` | G36 | PASS | 120 | INT-007, SCHEMA-011, VERIF-005 | independent-subagent-reviewer |
| `rubric_author.md` | S8 | PASS | 0 | - | self |
| `solution_checklist.md` | S3 | PASS | 0 | - | self |
| `task_code_verifier.md` | G3 | VALID | 12 | - | independent-subagent-reviewer |
| `toml_generator.md` | S4 | PASS | 0 | - | self |

The certification verdicts were produced by separate reviewer subagents that did not author the artefacts. They ran in the same session as the author, so they are independent reviews rather than independent identities. Generator prompts carry advisory self receipts. Findings recorded on non-passing checks:

- `QC_instruction.md` C3 [WARN] (delta): the lapse rules are consistent in substance, with minor gaps. Rule 53 (L341) gives no timing for a lapse, while rule 51 gives 'within one minute' for an expiry. The seeded Ember offer (13 hours old, 12-hour window) must already read `lapsed`, with `remaining` back at 1, when test_seeded_rows_survive_a_re_read reads it once without polling. Rule 53 also does not say that a lapse passing to the next visitor sends the offer message, as rule 51 does. The shelf has no stated rendering for a `lapsed` item (rule 42 correctly leaves it out of the header count). Rule 105 does not say whether a host may cancel a session that has already started (Early Pour). Fix: rule 53 'lapses at exactly its `offerExpiresAt`, reading `lapsed`, and within one minute passes to the next visitor in line with the offer message of rule 52, or back to `remaining`'; also state how a lapsed bottle shows on the shelf. Everything else in the delta checks out: seed counts agree (rule 58 lists seven releases, rule 89 seven sessions, the seed paragraph at L984 and L993 says seven and seven, and conftest has SEEDED_RELEASES = 7 and count_sessions == 7); `lapsed` is in the allocation state list (L940); the offer, lapse and edit-window seeds are dated in the past, so they do not decay with uptime; rule 102's two-day-old ritual matches rule 98 and the `edit_window_closed` test; `Early Pour` refusals (`session_started` on hold and on reschedule) match rules 78 and 84; the host page test needs only `Late Pour`, which is upcoming (rule 103); no journey references the new seeds; 00-decisions and 05-backend-schema agree.
- `QC_instruction.md` C2 [WARN]: every graded literal is now pinned, and all four pass-2 BLOCKERs are fixed. Status codes 401/403/404 and 400/409/422 are at L1406; the ISO 8601 Z instant format is at L1358; an absent or null alert flavour is at L398; the cancellation code charset and length are at L406; the tastings default list and query format are at L442. The tightened tests (401 unauthenticated, 403 forbidden, 202 link, 201 ritual save, 409 not_full, closed) all match the brief. Still unpinned, but no test asserts them: the ground-token strings, given only in prose (L987-991), and the item shapes of `GET /api/v1/alerts` and `GET /api/v1/bookings`, given only as 'the visitor's alerts/bookings' (L1384, L1392). The status of a successful owner PATCH is also implied rather than stated; the test expects 200. Fix: list one token string per chapter; write 'items shaped as the POST response'; say that PATCH answers `200` with the ritual.
- `QC_instruction.md` C3 [WARN] (carried over): the table shows `202, {sent}` (L1365), but rule 2 never mentions `sent`. Login and logout sit under `/api/auth/*` while every other route is under `/api/v1/*`. `/og/ritual/{slug}.png` (L581) is missing from the route table. Seeded reading ages and `Late Pour` (30 hours out) decay with uptime. L1026-1027 calls the red flourish 'the only part of it with motion of its own', yet the header words rise and lift on hover. None of these is a MAJOR route, journey, API or schema contradiction.
- `QC_instruction.md` C4 [WARN]: the palette contradiction is fixed (L727: only a failure colour, taken from blood; success and progress shown in ink with a word and a drawn mark). Two minor points remain. Confirm-before-destroy is stated only under Front-end specification (L1291), not in UI/UX notes. UI/UX notes still restate behaviour: 'both held gestures become single presses' (L786) and the upright rotate refusal (L809-810). Fix: move the destructive-confirmation sentence into UI/UX notes, and cut the restatements.
- `QC_instruction.md` C5 [WARN] (carried over): `booking.reschedule_count` (L970-971) is still a counter column. It is borderline, since it records state rather than an aggregate. Fix: a nullable `rescheduled_at`.
- `QC_instruction.md` C7 [MAJOR, recorded WARN by owner waiver]: window_lint reports core_features 46,255 chars (target 2,400), user_flow 7,786, ui_ux_notes 12,708, constraints 1,452, user_roles 2,586, overview 3,561, and a 74,348-char join against the 9,000 cap. The judge reads only the auth rules of Core features; rules 48 and 79 and the Motion and Accessibility paragraphs are past the cut. The owner waived length caps on purpose.
- `QC_instruction.md` A1 [WARN]: `## Build plan` is absent and `## Front-end specification` is added. Both are the owner's decision (no build plan) and legal. No change.
- `QC_instruction.md` A2 [WARN] (carried over): the framing paragraph (L3-13) chains about eight actions and three guarantees, close to a feature list. Optional fix: shorten it to one outcome.
- `QC_instruction.md` A3 [WARN] (carried over): contract_lint PASS. The canonical 'static or preview server' line (L1338) sits beside the Fastify server-rendering process (L825-826). This is not a contradiction. Optional fix: add 'the Fastify production server is the serving process' to Technical requirements.
- `QC_instruction.md` B1 [WARN] (carried over): the Mailpit slot is additive and allowed. The added `host` role is justified in 00-decisions but not recorded in task.toml variant_axes.
- `QC_instruction.md` B2 [WARN] (carried over): the reload guarantee is a numbered rule only for the shelf (rule 50, L329). For alerts, bookings and rituals it lives only in the 'No stand-ins' prose. Fix: widen rule 50 to 'every bottle, alert, booking and ritual the interface shows as kept'.
- `QC_instruction.md` B3 [WARN]: Build plan is absent by the owner's decision; the spec_sections axis has no recorded step. No change to the brief.
- `QC_instruction.md` D3 [WARN] (carried over): rule 83 (L471-472) 'Cancelling at forty-seven hours is refused; at forty-nine it succeeds.' reads like a boundary test case. Fix: delete it. The Definition of done is clean.
- `qc_docker.md` CMP-011 [High by the letter; kit-mandated, so WARN]: docker-compose.yaml sets main.ports: ["4173:4173"]. CMP-011 fails on 'any service has a ports: key'. However, docker_generator.md mandates that exact block on main, and CMP-022 (Critical) requires it. The rows contradict each other, and the bundle follows the Tier-1 generator. Fix in the kit, not the bundle: scope CMP-011 to sidecars. This earlier finding remains.
- `qc_docker.md` RUN-005 / BP-003 [High by the letter; WARN]: Node comes from the NodeSource node_${NODE_MAJOR}.x channel with ARG NODE_MAJOR=20 and an unversioned `apt-get install nodejs`, so minor and patch versions float between builds. The TRD (instruction.md line 825) says only 'Node 20', and the docker_generator SKELETON prescribes this exact pattern, so the Tier-1 source sanctions it. Justified. Optional fix: pin nodejs=20.x.y-1nodesource1. This earlier finding remains. The npm@10 part of it is gone, because that RUN was removed.
- `qc_docker.md` BP-007 [Low]: gnupg (and curl) stay in the final image after their only use, fetching and dearmoring the NodeSource key. This is non-blocking. Optional fix: apt-get purge -y gnupg after the keyring step. This is partly resolved: the redundant `npm install -g npm@10` RUN is gone.
- `qc_docker.md` BP-001 [Low]: the keyring RUN and the `echo ... > nodesource.list` RUN are two separate layers for one concern. The skeleton puts '<nodesource keyring, then nodejs>' in one RUN. Optional fix: merge the keyring, list and nodejs install into one or two RUNs, keeping each line under 200 characters.
- `qc_docker.md` CON-004 [Low]: the proxy/CA passthrough ARGs from DOCKERFILE STRUCTURE section 3 (http_proxy/https_proxy/no_proxy, and CA path/PEM) are absent, and the skeleton's ARG CA_CERT_PEM="" was removed together with its dead-ARG issue. Section 3 may be omitted 'when not applicable', so this is a minor structural deviation from the skeleton, not a defect. Optional fix: restore the empty-default proxy ARGs if scrubbed or proxied build hosts are expected.
- `qc_docker.md` RESOLVED since pass 1 (earlier CON-004 seed item): environment/postgres-init.sql now matches the SQL of the central environment/providers/postgres/init.sql exactly, with the comments stripped. It is idempotent (IF NOT EXISTS), uses current_database(), and sets ALTER DEFAULT PRIVILEGES on tables and sequences. deku_app/deku-local-dev matches DATABASE_URL, and deku_admin matches DB_ADMIN_URL, so CMP-005 passes.
- `qc_rubric.md` RC-01 [WARN]: No claimed item is unobserved. The new claim C-CF-136 (a lapsed bottle reads the went-back line with no countdown) is graded by R9, whose criterion and rule now name the lapsed N02-EMBER bottle beside the expired N01 one. C-UX-37 is now fully graded, since J24 reads 'the drawing surface is hidden from assistive technology and never takes focus'. Partials carried from cycle 3: R11 does not grade the offline hold-control reason, the venue list's age and alert refusal, or C-CN-04; R24 grades map services only for C-CN-02; R5 grades square corners on panels only (C-UX-17) and never the red narration emphasis (C-FE-18); R1 has no no-case for C-UX-01; R2 does not grade the reserved uses of red. C-CF-126, the expiring countdown, still needs a near-expiry hold, which the task owner waived; the seeding trick used for N02-EMBER would close it.
- `qc_rubric.md` RC-03 [WARN]: Unchanged. R1's 'any surface is smoothly shaded' also fails the soft shadow that R25 grades, and R11 and R13 both grade offline refusal wording.
- `qc_rubric.md` RC-04 [WARN]: No criterion restates a committed assertion. Four small facet overlaps remain: R15's reload clause with the pytest cookie-reload test, R1's image-file clause with the browser network check for C-CN-07, R18's ledge clause with the keep-a-bottle browser substep, and R21's header-unroll timing with browser C-CF-60.
- `qc_rubric.md` RC-05 [WARN]: R14 still bundles the header pill with four addition surfaces. R20's rule still grades numbers in columns and the absence of a light or dark mode while its criterion names only the red ground and the shared palette; the wording is fixed, the bundling is not. R22 remains an eleven-item list on one boolean.
- `qc_rubric.md` RC-06 [WARN]: Carried from cycle 3: R5 says 'outdoor chapters' though panels also appear in target, anti-gravity and pillar-crumble; R21 defines furniture as the age panel, header pill and venue marks against the brief's mark, header pill and audio meter; R25 counts the reaching hand as a figure with a contact shadow.
- `qc_rubric.md` RC-07 [WARN]: R20's overloaded 'figures' is fixed: the rule now reads 'numbers in lists, such as counts, prices and times', and the item is renamed 'Numbers in the additions line up in columns'. Still undefined for a judge with no brief: R22's 'base text' and 'comfortably sized', R4's tint mapping, R7's 'venues with the chosen flavour', R18's 'sensible arrangement', R19's 'title lockup', and R2's 'pure white bone' where the brief says near-white.
- `qc_rubric.md` RC-08 [WARN]: R9 now names both went-back bottles, which is decidable in a judging session because both are seeded. One wrinkle: R9 says 'none of the three bottles on that shelf shows a countdown', but the browser workflow released_bottle_is_offered_to_the_waitlist has visitor2 accept the N02-VESTRY offer, so a judge arriving after that walk sees four bottles. The verdict does not change, since a fresh 72-hour hold shows no countdown, but the count is wrong. Fix J9: 'and no bottle on that shelf shows a countdown'. Carried: R22's contrast and target size rest on the eye; R10's silence before the first press cannot be heard (waived); R18's three-bottle and expiring arrangements cannot be staged (waived).
- `qc_rubric.md` RC-09 [WARN]: R17's no-case now covers a paragraph 'set in the interface or display face', closing the gap from the last pass. Carried small gaps: R1 has no no-case for a frame that does not lead with its subject, R4 none for a wrong tint, R5 none for missing red emphasis, R7 none for red on a venue without the flavour.
- `qc_rubric.md` RC-11 [WARN]: Every clause traces to the brief. Carried drifts: R22's 'comfortably sized' is weaker than the WCAG 2.2 AA target size (instruction.md:794), R2's 'pure white bone' (:714), and R21's definition of furniture (:1005-1007).
- `qc_rubric.md` RC-12 [WARN]: R20's columns and light-or-dark-mode clauses and R22's contrast and alternative text are DOM or computed-style facts a script could read; acceptable as visual proxies.
- `qc_rubric.md` RC-16 [WARN]: Every rule is still one yes sentence and one no sentence with rotated openers, and R22's 'Checks:' list now runs to eleven items. Style only; G52 passes.
- `qc_toml.md` VERIF-005 [High by the letter; justified, so WARN]: task.toml [verifier].env still has APP_PUBLIC_URL = "${APP_PUBLIC_URL:-http://main:4173}". The toml_generator.md section 11 template and qc_toml VERIF-005 require http://localhost:4173. That value dates from shared mode. This bundle declares environment_mode = "separate" (toml_generator 10.1), so the grader runs in its own container, where localhost:4173 would not reach the app. main:4173 is the working value. It agrees with the instruction.md Deployment contract and with tests/test.sh, which curls ${APP_PUBLIC_URL}/api/health. G2 validate_task passes. Justified as the one listed High under the PASS rule. Fix: none in the bundle. In the kit, amend section 11 / 10.4 and VERIF-005 to say http://main:4173 when environment_mode = "separate". This earlier finding remains, downgraded to justified.
- `qc_toml.md` SCHEMA-011 [WARN; Critical if read literally]: two elements are absent from the section 11 canonical template. (1) The [delivery] table (format, schema_version, reward_path, reward_key, reward_range, reward_full, network_policy) is sanctioned by toml_generator 10.1 ('when a [delivery] block is emitted') and checked by validate_task (G2 '[delivery] hold'). (2) [metadata].rubric_version = "1" is mandated by toml_generator 10.5b; it was added since the first pass. Both are kit-sanctioned and both pass the tool, so neither is a bundle defect. Fix in the kit: add [delivery] (after [verifier], before [[artifacts]]) and rubric_version (after grader_version) to the section 11 template. The earlier finding remains, now kit-side only.
- `qc_toml.md` INT-007 [WARN, informational]: difficulty is the calibration placeholder "", so turns_expected = 200 and tokens_expected = 8000000 (the expert band and the absolute maximum) cannot be checked against a declared difficulty. BENCH-003 and BENCH-005 are therefore NOT-APPLICABLE. BENCH-004 passes: 8000000 is within 200000-8000000. The standard tier values are exact (4/8192/20480/900.0/18000.0/3600.0). Fix: none now. At calibration, lower the budget if difficulty lands below expert. The earlier finding remains.

## Review state, honestly

Every certification prompt was run by a reviewer subagent that did not author the artifact, over several passes, and each one's last verdict on these exact files is PASS, or VALID for the task code. The receipts carry each reviewer's own scorecard, warnings included.

- `QC_instruction.md` PASS: no FAIL. Its warnings are the owner-accepted ones (length past the judge window, no build plan) plus small unstated shapes no grader reads.
- `qc_solution_checklist.md` PASS: coverage, invention, unpinned literals and partial capture all clear. Remaining warnings are the waived harness-bound mappings and a few narrow assertions.
- `qc_rubric.md` PASS: no FAIL on the sixteen ids. Its warnings are the merged small-dimension criteria and undefined terms a judge has to read in context.
- `QC_spec.md` PASS with no findings; `qc_toml.md` and `qc_docker.md` PASS with justified warnings; `task_code_verifier.md` VALID.

Known gaps the author accepts, recorded rather than hidden:

- Sound is graded by a browser walk that cannot hear it. That substep asks only for what a walker can see or read in the network view.
- Rule 81's `expired` booking refusal carries no checklist item: a seat hold cannot be aged inside one run without a seeded past hold.
- A few contract asks, the library list, the JSON log lines, the production build, the log and README bullets, rest on the harness deploy check rather than on a test in this bundle.
- Some browser substeps stand in for asks a walker cannot stage, such as losing the drawing context or counting stored rows.
- The rubric's small dimensions, motion, accessibility and responsiveness, each carry one merged criterion, so their rules run long. That is a deliberate trade against the kit's pressure for two criteria per dimension.

Three seeds exist so that clock-bound rules can be graded in one run: the ritual saved two days before first start (`edit_window_closed`), the session `Early Pour at Salt & Vesper` that has already started (`session_started`), and `N02-EMBER` carrying an offer made thirteen hours before first start (the lapse).


## Blocking findings

- None inside the kit's reach.
- The companion describes more product than one agent budget can build. `## Constraints` records what was scoped out, and `_spec/S_ecomm_crud_cinematic-spirits-showcase-vb_20260916_101529/00-decisions.md` carries the companion carry table. 29 G51 waivers are declared in `_spec/S_ecomm_crud_cinematic-spirits-showcase-vb_20260916_101529/g51-waivers.txt`; they cover evidence of the reference build and mechanism names the order asked the brief to leave out.

## Versions

| Field | Value |
|---|---|
| Kit | `deku-green-field` |
| Vendored grader | `0.22.0` |
| Target schema | `1.4` |
| Harbor | `0.20.0` |
| Verifier mode | `separate` |

## Execution budget

`turns_expected = 200`, `tokens_expected = 8000000`. An eighteen-chapter generated film with synthesised sound, two held gestures, finite stock with waitlists, venue alerts, capacity-limited tastings, a ritual builder and a host role put this at the top of the documented band.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

NOT ADMISSIBLE. The bundle carries no reference app. Nothing counts toward corpus targets until the app lands downstream and `harbor run -a oracle` returns `1.0` twice.
