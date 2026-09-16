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
- Solution checklist: **501** items in `solution/checklist.md`

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
| Core features | 46834 |
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
| `G33` | `window_lint.py` | 0 | PASS | `8da67946f7139cda` |
| `G4/G5` | `contract_lint.py` | 0 | PASS | `66da11b948b843f2` |
| `G43` | `prescription_lint.py` | 0 | PASS | `c2026524c6716f40` |
| `G44` | `disclosure_lint.py` | 0 | PASS | `40b0b49d23609083` |
| `G10` | `no_sdk_lint.py` | 0 | PASS | `4b51e847a5f2e328` |
| `G31` | `determinism_lint.py` | 0 | PASS | `c73323ac382cee1b` |
| `G14` | `reward_path_lint.py` | 0 | PASS | `1acc6ea17571593c` |
| `G27/G30` | `rubric_lint.py` | 0 | PASS | `b4146d142747301d` |
| `G41` | `flag_lint.py` | 0 | PASS | `9ed60ea29af1a8f3` |
| `G56/G57/G58` | `if_lint.py` | 0 | PASS | `cdf20c83e9056866` |
| `G59/G60` | `codequality_lint.py` | 2 | ? | `e23941dd85e0253b` |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | 0 | PASS | `a2227f769bbec512` |
| `G6` | `fixture_lint.py` | 0 | PASS | `ed3c6bd27efe183e` |
| `G24` | `coverage_map.py` | 0 | PASS | `ded15f4b9c9dc085` |
| `G37` | `checklist_qc.py` | 0 | PASS | `3cdcaf290aae4d15` |
| `G39` | `rubric_align_lint.py` | 0 | PASS | `fc693824c4f5dca2` |
| `G28/G29` | `channel_lint.py` | 0 | PASS | `a6d778ab9cd7009f` |
| `G40` | `prompt_receipt_lint.py` | 0 | WARN | `70eb37d6d424793b` |
| `G0/INV5` | `vendor_check.py` | 0 | PASS | `e05d8ce49ed806ca` |
| `G47` | `output_qc.py` | 0 | PASS | `0a55f21716c15cb9` |

`G59/G60` exits 2 (NOT-APPLICABLE) when present: the bundle carries no reference code to lint.

## Certification prompt receipts

| Prompt | Gate | Verdict | Checks | Non-pass | Verifier |
|---|---|---|---|---|---|
| `QC_instruction.md` | G34 | FAIL | 24 | A1, A2, A3, B1, B2, B3, C2, C3, C4, C5, C7, D2, D3 | independent-subagent-reviewer |
| `QC_spec.md` | G34 | PASS | 15 | S6 | independent-subagent-reviewer |
| `docker_generator.md` | S5 | PASS | 0 | - | self |
| `generate_instruction.md` | S2 | PASS | 0 | - | self |
| `pytest_generator.md` | S7 | PASS | 0 | - | self |
| `qc_docker.md` | G35 | PASS | 105 | BP-001, BP-003, BP-007, CMP-011, CON-004, RUN-005 | independent-subagent-reviewer |
| `qc_rubric.md` | G53 | PASS | 16 | RC-01, RC-03, RC-04, RC-05, RC-06, RC-07, RC-08, RC-09, RC-11, RC-12, RC-16 | independent-subagent-reviewer |
| `qc_solution_checklist.md` | G37 | CHANGES REQUIRED | 0 | - | independent-subagent-reviewer |
| `qc_toml.md` | G36 | PASS | 120 | INT-007, SCHEMA-011, VERIF-005 | independent-subagent-reviewer |
| `rubric_author.md` | S8 | PASS | 0 | - | self |
| `solution_checklist.md` | S3 | PASS | 0 | - | self |
| `task_code_verifier.md` | G3 | VALID | 12 | - | independent-subagent-reviewer |
| `toml_generator.md` | S4 | PASS | 0 | - | self |

The certification verdicts were produced by separate reviewer subagents that did not author the artefacts. They ran in the same session as the author, so they are independent reviews rather than independent identities. Generator prompts carry advisory self receipts. Findings recorded on non-passing checks:

- `QC_instruction.md` D2 [MAJOR] (new in the delta): rule 76 (L442) says 'With no query, every `scheduled` session is listed however far ahead'. The new seed `Early Pour at Salt & Vesper` started one hour before first start (L492). Under the literal reading a started session is still in state `scheduled` and is listed. Under the common reading ('however far ahead' implying an upcoming-only list, as the host page's 'upcoming sessions' in rule 103 also suggests) it is hidden. Tests need it in the unfiltered list: test_hold_larger_than_remaining_is_refused and test_second_reschedule_is_refused call session_by_title(SESSION_EARLY) on `GET /api/v1/tastings` with no query, and an upcoming-only build fails both. Fix: L442 'With no query, every `scheduled` session is listed, including one that has already started, however far ahead or behind;'.
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
- `QC_spec.md` S6 [MINOR]: the new `N02-EMBER` seed is stored as one state but must read as another, and 05 never says how the lapse is applied. 05 line 107 seeds 'one `offered` allocation of `N02-EMBER` ... offered thirteen hours before first start and never accepted, so it reads `lapsed` and ... its bottle is back in `remaining`'. The line 40 invariant counts 'held, offered and confirmed rows', and the `allocation` row does not list `lapsed` as derived. Taken literally, a stored `offered` row still counts, so `N02-EMBER` would show `0` remaining, not `1`. The brief's rule 58 has the same wording, so G2 still agrees; the gap is in how exactly the seed can be checked by value. Fix: in 05, either (a) seed the row as state `lapsed` with `offered_at` = first start minus 13 h and `offer_expires_at` = first start minus 1 h, or (b) add to the `allocation` rules: 'an `offered` row past `offer_expires_at` is `lapsed` (applied on read or by a sweep before any count) and is excluded from the stock count'. Mirror the chosen wording in brief rule 53/58.
- `qc_docker.md` CMP-011 [High by the letter; kit-mandated, so WARN]: docker-compose.yaml sets main.ports: ["4173:4173"]. CMP-011 fails on 'any service has a ports: key'. However, docker_generator.md mandates that exact block on main, and CMP-022 (Critical) requires it. The rows contradict each other, and the bundle follows the Tier-1 generator. Fix in the kit, not the bundle: scope CMP-011 to sidecars. This earlier finding remains.
- `qc_docker.md` RUN-005 / BP-003 [High by the letter; WARN]: Node comes from the NodeSource node_${NODE_MAJOR}.x channel with ARG NODE_MAJOR=20 and an unversioned `apt-get install nodejs`, so minor and patch versions float between builds. The TRD (instruction.md line 825) says only 'Node 20', and the docker_generator SKELETON prescribes this exact pattern, so the Tier-1 source sanctions it. Justified. Optional fix: pin nodejs=20.x.y-1nodesource1. This earlier finding remains. The npm@10 part of it is gone, because that RUN was removed.
- `qc_docker.md` BP-007 [Low]: gnupg (and curl) stay in the final image after their only use, fetching and dearmoring the NodeSource key. This is non-blocking. Optional fix: apt-get purge -y gnupg after the keyring step. This is partly resolved: the redundant `npm install -g npm@10` RUN is gone.
- `qc_docker.md` BP-001 [Low]: the keyring RUN and the `echo ... > nodesource.list` RUN are two separate layers for one concern. The skeleton puts '<nodesource keyring, then nodejs>' in one RUN. Optional fix: merge the keyring, list and nodejs install into one or two RUNs, keeping each line under 200 characters.
- `qc_docker.md` CON-004 [Low]: the proxy/CA passthrough ARGs from DOCKERFILE STRUCTURE section 3 (http_proxy/https_proxy/no_proxy, and CA path/PEM) are absent, and the skeleton's ARG CA_CERT_PEM="" was removed together with its dead-ARG issue. Section 3 may be omitted 'when not applicable', so this is a minor structural deviation from the skeleton, not a defect. Optional fix: restore the empty-default proxy ARGs if scrubbed or proxied build hosts are expected.
- `qc_docker.md` RESOLVED since pass 1 (earlier CON-004 seed item): environment/postgres-init.sql now matches the SQL of the central environment/providers/postgres/init.sql exactly, with the comments stripped. It is idempotent (IF NOT EXISTS), uses current_database(), and sets ALTER DEFAULT PRIVILEGES on tables and sequences. deku_app/deku-local-dev matches DATABASE_URL, and deku_admin matches DB_ADMIN_URL, so CMP-005 passes.
- `qc_rubric.md` RC-01 [WARN]: Every claimed item is now observed: R21 grades C-FE-07 (hover) and C-CF-169 (plan move-in), and R22 grades C-UX-22 (no flash). Some items are still only partly observed. R11 (unchanged) never grades C-CF-135 (the offline hold control's reason in words), C-CF-182 (the list's age and alert refusal) or C-CN-04 (nothing queued). Fix J11 by adding 'the shelf's hold control says in words why it is unavailable, the venue list says how old it is and refuses a new alert' and 'or an action appears accepted to be sent later'. R24 grades only map services for C-CN-02. R5 grades square corners only on panels (C-UX-17) and never the red narration emphasis (C-FE-18). R1 has no no-case for C-UX-01. R2 does not grade C-UX-08's reserved red uses. WAIVED by the task owner, and recorded as WARN because only a real app run can stage them: C-CF-121 and C-CF-136 need a near-expiry hold, and C-UF-10 in R12 needs a sign-in to expire mid-action.
- `qc_rubric.md` RC-03 [WARN]: Two overlaps are unchanged. R1's no-case 'any surface is smoothly shaded' also fails the soft shadow R25 grades. R11 and R13 both grade the wording of offline refusals. Fix: narrow J1's no-case to 'columns, sky or figures are smoothly shaded'.
- `qc_rubric.md` RC-04 [WARN]: The R23 rotate-panel clause is gone, so the FAIL is resolved. Four minor facet overlaps remain. R15's reload clause overlaps pytest C-CF-273. R1's 'mark arrives as an image file' overlaps the browser network check for C-CN-07 (public_pages#4). R18's 'bottles stand on a hatched ledge' overlaps browser substep visitor_signs_in_with_a_link_and_keeps_a_bottle#2. R21's 'header background unrolling after the loader' overlaps browser C-CF-60 (visitor_drives_the_film_end_to_end#1). Each measures a different item, so none is a straight restatement.
- `qc_rubric.md` RC-05 [WARN]: R14 still bundles the header pill with the primary actions on four addition pages. R22 and R23 are whole-product checks, which is acceptable for a one-criterion small dimension.
- `qc_rubric.md` RC-06 [WARN]: R3 is fixed: it now runs 'from the portal through the collapse after the pour', matching the chapter order in instruction.md:149-151. Three smaller issues remain. R5 still says 'outdoor chapters', but panels also appear in target, anti-gravity and pillar-crumble (instruction.md:1133-1142); fix to 'comic panels in the film'. R21 defines furniture as the age panel, header pill and venue marks, while the brief means mark, header pill and audio meter (instruction.md:1005-1007). R25 still counts 'the reaching hand' as a figure with a shadow beneath it.
- `qc_rubric.md` RC-07 [WARN]: Several terms remain undefined. R4 'the new tint' and 'its liquid changes colour' name no flavour-to-tint mapping, so a wrong tint passes. R7 'venues with the chosen flavour' does not say whether a low or unknown reading counts. R18 'a sensible arrangement' is undefined. R19 does not define 'the title lockup'. R22 'comfortably sized' and 'images' are undefined. R2 calls bone 'pure white' (brief: near-white, instruction.md:714).
- `qc_rubric.md` RC-08 [WARN]: R6 is fixed: slow-scroll stop, with coasting, breathing and pulsing explicitly allowed. R3's 'robe, grass, floating rocks and beams all lean with one wind' plus 'A yes needs all of this on screen' may lead a strict judge to look for grass, which is not in the portal-to-collapse range. Fix: drop 'grass' from J3. R8 'recognisably the chapter's composition' gives the judge no reference. R22 asks for WCAG AA contrast by eye. WAIVED by the task owner as WARN: R10 needs silence before the first press, which a screenshot or DOM grader cannot hear, so the rule names only the observable meter behaviour where it can; R12's expired sign-in, R9's expiring half and R18's expiring state need a real app run to stage.
- `qc_rubric.md` RC-09 [WARN]: The R12 'each event' fix and the widened no-cases for R15, R18, R19 and R21 are in place. Minor gaps remain: R1 has no no-case for a frame that does not lead with its subject; R5 has none for missing red emphasis; R7 has none for red on a venue without the flavour; R4 has none for a wrong tint.
- `qc_rubric.md` RC-11 [WARN]: R3's robe colour and wind list now match the brief. Small drifts remain: R22's 'comfortably sized' is weaker than the WCAG 2.2 AA target size (instruction.md:794); R2 says 'pure white bone'; R21 uses its own definition of furniture.
- `qc_rubric.md` RC-12 [WARN]: Some clauses could be measured deterministically, but they are acceptable as visual proxies: contrast and alternative text in R22 (DOM/axe), requests to an outside map service in R24 (network), spacing multiples in R20 (computed style), and 'a mark arrives as an image file' in R1 (network, already checked by a browser substep).
- `qc_rubric.md` RC-16 [WARN]: Every rule is still one yes sentence and one no sentence, with rotated openers ('Yes if', 'Answer yes when', 'A yes needs', 'Say yes when', 'Yes when'). R22 opens with 'Checks:'. R9's criterion 'shows the absence of any countdown' is stilted. G52 passes and the pasted definitions are gone, so this is style only.
- `qc_toml.md` VERIF-005 [High by the letter; justified, so WARN]: task.toml [verifier].env still has APP_PUBLIC_URL = "${APP_PUBLIC_URL:-http://main:4173}". The toml_generator.md section 11 template and qc_toml VERIF-005 require http://localhost:4173. That value dates from shared mode. This bundle declares environment_mode = "separate" (toml_generator 10.1), so the grader runs in its own container, where localhost:4173 would not reach the app. main:4173 is the working value. It agrees with the instruction.md Deployment contract and with tests/test.sh, which curls ${APP_PUBLIC_URL}/api/health. G2 validate_task passes. Justified as the one listed High under the PASS rule. Fix: none in the bundle. In the kit, amend section 11 / 10.4 and VERIF-005 to say http://main:4173 when environment_mode = "separate". This earlier finding remains, downgraded to justified.
- `qc_toml.md` SCHEMA-011 [WARN; Critical if read literally]: two elements are absent from the section 11 canonical template. (1) The [delivery] table (format, schema_version, reward_path, reward_key, reward_range, reward_full, network_policy) is sanctioned by toml_generator 10.1 ('when a [delivery] block is emitted') and checked by validate_task (G2 '[delivery] hold'). (2) [metadata].rubric_version = "1" is mandated by toml_generator 10.5b; it was added since the first pass. Both are kit-sanctioned and both pass the tool, so neither is a bundle defect. Fix in the kit: add [delivery] (after [verifier], before [[artifacts]]) and rubric_version (after grader_version) to the section 11 template. The earlier finding remains, now kit-side only.
- `qc_toml.md` INT-007 [WARN, informational]: difficulty is the calibration placeholder "", so turns_expected = 200 and tokens_expected = 8000000 (the expert band and the absolute maximum) cannot be checked against a declared difficulty. BENCH-003 and BENCH-005 are therefore NOT-APPLICABLE. BENCH-004 passes: 8000000 is within 200000-8000000. The standard tier values are exact (4/8192/20480/900.0/18000.0/3600.0). Fix: none now. At calibration, lower the budget if difficulty lands below expert. The earlier finding remains.

## Review state, honestly

Each certification prompt was run by a reviewer subagent that did not author the artifact, over several passes. The receipts carry each reviewer's own last written verdict. Two of those verdicts describe a state the bundle has already moved past, because the reviewers hit their account session limit before they could confirm the final edits:

- `QC_instruction.md` reads FAIL on one check, D2. Its single blocker was that rule 76 left it open whether a session that has already started appears in the unfiltered tastings list, which two tests need. That sentence was fixed in the brief and in `05-backend-schema.md` straight after the review, and the checklist item was reworded with it. Every other check on that pass is PASS or an owner-accepted WARN.
- `qc_solution_checklist.md` reads CHANGES REQUIRED, mapped from the reviewer's own words, NEEDS REVIEW. At that pass its only open finding was that two brief asks, `session_started` and the twelve-hour offer lapse, carried no checklist item because no grader could stage them. Both were then made observable by seeding: the session `Early Pour at Salt & Vesper` has already started, and `N02-EMBER` carries an offer made thirteen hours before first start. Items and tests for both now exist, and the mechanical G37 layer passes.
- The other prompts, `QC_spec.md`, `qc_rubric.md`, `qc_toml.md`, `qc_docker.md` and `task_code_verifier.md`, carry PASS or VALID verdicts on the current files.

Known gaps the author accepts, recorded rather than hidden:

- Sound is graded by a browser walk that cannot hear it. That substep asks only for what a walker can see or read in the network view.
- A few contract asks, the library list, the JSON log lines, the production build, the log and README bullets, rest on the harness deploy check rather than on a test in this bundle.
- Some browser substeps stand in for asks a walker cannot stage, such as losing the drawing context or counting stored rows.
- The rubric's small dimensions, motion, accessibility and responsiveness, each carry one merged criterion, so their rules run long. That is a deliberate trade against the kit's pressure for two criteria per dimension.


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
