# Build report - S_creato_dire_armillary-ecosystem-roster-vb_20260916_123203

## Identity

| Field | Value |
|---|---|
| Task code | `S_creato_dire_armillary-ecosystem-roster-vb_20260916_123203` |
| Task id | `deku/armillary-ecosystem-roster-vb` |
| Cell | solo_founder / creator-monetization / directory-matching |
| Task Order as received | domain `creator-media`, pattern `directory-profiles` (not in reference/A; normalised, see _spec 00-decisions.md) |
| Service profile | `P2-db-email` |
| Providers | backend `postgres`, email `mailpit` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | python (FastAPI) with a React + Vite front end |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Companion | `prd/steven_prd.md` |
| Shard | 1 of 1 |
| Kit | deku-green-field at GreenField-GenKit2 806eb0a |
| Grader pin | 0.22.0 |
| Target schema | 1.4 |

## Feature resolution table

| Candidate (companion section) | Verdict | Landed in | Reason |
|---|---|---|---|
| Front door, armillary, arrival, transition (7, 8, 11) | INCLUDED | Core features, Front-end specification | the idea's entry point |
| Global chrome, menu, clock, toggle, footer, consent (5) | INCLUDED | Core features | measured chrome |
| Division template and scenes (9, 12) | INCLUDED | Core features, Front-end specification | the idea's divisions |
| Sketch mode (10) | INCLUDED | Core features | declared mode |
| Roster, profiles, search, filter, sort (13, 14, 23) | INCLUDED | Core features | directory-matching core |
| Join us and application (15) | INCLUDED | Core features | the only sign up |
| Legal routes (16) | INCLUDED | Core features | terms_page launch surface |
| Profile editor, review queue (17.2, 17.3) | INCLUDED | Core features | the graded workflow |
| Division editor, discipline vocabulary editor (17.4, 17.5) | DROPPED | none | principal-only, out of solo_founder role band |
| Sign in, verification (18.1 to 18.3) | INCLUDED | Core features | bearer token per kit baseline |
| Password reset, session lists (18.4, 18.5) | DROPPED | none | scope |
| Roles (19) | INCLUDED as creator and curator | User roles | solo_founder band of two roles |
| Primary workflow (20) | INCLUDED | Core features, User flow | the graded path |
| Forms and states (21, 22) | INCLUDED | User flow, Front-end specification | |
| Real-time and offline replay (24, 22.3) | DROPPED | Constraints | no realtime slot |
| Notifications and mail (25) | INCLUDED (four mails) | Core features | email slot |
| Data model and contract (26) | INCLUDED | Data model, Deployment contract | |
| Persistence and seed (27) | INCLUDED | Data model | |
| Internationalisation (28) | DROPPED except formatting | Technical requirements | English only |
| Analytics (29) | INCLUDED as first-party events behind consent | Core features | no third-party collector |
| Security and abuse (30) | INCLUDED | Core features, Technical requirements | spam_protection, headers |
| Test plan, build order, evidence gaps (31, 36, 39) | WAIVED | none | apparatus; corrections carried |

## Slot obligation table

| Slot | Provider | Critical substep | Observation | Status |
|---|---|---|---|---|
| db | postgres | `test_application_creates_unconfirmed_creator_and_applying_profile`, `test_seeded_rows_persisted_once` path | rows read through DB_ADMIN_URL | MET |
| email | mailpit | `test_application_sends_confirmation_mail` | message read from EMAIL_INBOX_API_URL | MET |

## Graders

- Workflows: 16 (solo_founder band 10 to 16)
- Browser substeps: 45
- Pytest substeps: 63, one module `tests/test_output.py`; critical substeps: 18
- Non-happy-path workflow ids: `visitor_filters_to_an_empty_roster_and_searches`, `duplicate_or_invalid_application_is_refused`, `creator_is_denied_studio_routes_and_other_profiles`, `unauthenticated_writes_are_denied`, `repeated_sign_in_attempts_hit_the_limit`
- Checklist items: 410 (C-OV 8, C-RL 20, C-CF 277, C-UF 15, C-UX 24, C-TR 14, C-DM 13, C-FE 25, C-CN 5, C-DC 9); declared but ungraded: 4

## Rubric

- Judged criteria: 21 (20 positive, 1 negative); compiled reference items: 12, compiled share 1.0
- Dimension shares of positive points:

| Dimension | Points | Share | Target |
|---|---|---|---|
| instruction_following | 12 | 0.300 | 0.30 |
| functionality | 9 | 0.225 | 0.25 |
| ux_flow | 6 | 0.150 | 0.15 |
| ui_visual | 7 | 0.175 | 0.15 |
| motion | 2 | 0.050 | 0.05 |
| accessibility | 2 | 0.050 | 0.05 |
| responsiveness | 2 | 0.050 | 0.05 |

## Literals ledger

| Value | Class | Verifier only | Carriers |
|---|---|---|---|
| `curator@example.com` | account | False | instruction.md, conftest.py |
| `creator@example.com` | account | False | instruction.md, conftest.py |
| `creator2@example.com` | account | False | instruction.md, conftest.py |
| `deku-demo-pw-2026` | credential | False | instruction.md, conftest.py |
| `/api/auth/login` | route | False | instruction.md |
| `/api/me` | route | False | instruction.md, conftest.py, test_output.py |
| `/api/site` | route | False | instruction.md, test_output.py |
| `/api/divisions/{slug}` | route | False | instruction.md, conftest.py |
| `/api/profiles` | route | False | instruction.md, conftest.py, test_output.py |
| `/api/profiles/{slug}` | route | False | instruction.md |
| `/api/applications` | route | False | instruction.md, test_output.py |
| `/api/accounts/verifications` | route | False | instruction.md |
| `/api/me/profile` | route | False | instruction.md, conftest.py |
| `/api/me/profile/disciplines` | route | False | instruction.md |
| `/api/me/profile/links` | route | False | instruction.md |
| `/api/me/profile/credits` | route | False | instruction.md |
| `/api/me/profile/transitions` | route | False | instruction.md |
| `/api/profiles/{slug}/transitions` | route | False | instruction.md |
| `/api/studio/roster-order` | route | False | instruction.md |
| `/api/notices/{kind}` | route | False | instruction.md |
| `/api/events` | route | False | instruction.md |
| `/api/health` | route | False | instruction.md, test_output.py |
| `/sitemap.xml` | route | False | instruction.md, test_output.py |
| `/robots.txt` | route | False | instruction.md, test_output.py |
| `/legal/terms-and-conditions` | route | False | instruction.md, test_output.py |
| `The Operating System for the Creator Economy` | copy | False | instruction.md, conftest.py |
| `Our purpose is to shorten the road back to human.` | copy | False | instruction.md, conftest.py |
| `creator-media` | slug | False | instruction.md, conftest.py, test_output.py |
| `creator-communities` | slug | False | instruction.md, conftest.py, test_output.py |
| `creator-products` | slug | False | instruction.md, conftest.py, test_output.py |
| `creator-tech` | slug | False | instruction.md, conftest.py, test_output.py |
| `juno-okafor` | slug | False | instruction.md, conftest.py, test_output.py |
| `ada-moreau` | slug | False | instruction.md, conftest.py, test_output.py |
| `partnerships` | slug | False | instruction.md, conftest.py, test_output.py |
| `https://media.example.com/portraits/` | address | False | instruction.md, conftest.py |
| `Confirm your address` | subject | False | instruction.md, conftest.py, test_output.py |
| `Your entry needs a change` | subject | False | instruction.md, conftest.py |
| `You are on the roster` | subject | False | instruction.md, conftest.py |
| `Your entry has been taken down` | subject | False | instruction.md, conftest.py |
| `Something in there is still a placeholder.` | copy | False | instruction.md, conftest.py |
| `Confirm your address first.` | copy | False | instruction.md, conftest.py |
| `That address already has an account.` | copy | False | instruction.md, conftest.py |
| `We need a picture.` | copy | False | instruction.md, conftest.py |
| `Say what needs changing.` | copy | False | instruction.md, conftest.py |
| `Give us your name.` | copy | False | instruction.md, conftest.py |
| `Eighty characters at least. Tell us what you do.` | copy | False | instruction.md, conftest.py |
| `validation_failed` | enum | False | instruction.md, test_output.py |
| `not_authenticated` | enum | False | instruction.md, test_output.py |
| `not_authorised` | enum | False | instruction.md, test_output.py |
| `not_verified` | enum | False | instruction.md, test_output.py |
| `not_found` | enum | False | instruction.md, test_output.py |
| `conflict` | enum | False | instruction.md, test_output.py |
| `version_conflict` | enum | False | instruction.md, test_output.py |
| `state_not_allowed` | enum | False | instruction.md, test_output.py |
| `rate_limited` | enum | False | instruction.md, test_output.py |
| `data-acquired` | hook | False | instruction.md, test_output.py |
| `data-mode` | hook | False | instruction.md |
| `data-sketch` | hook | False | instruction.md, test_output.py |
| `data-arrival` | hook | False | instruction.md, conftest.py, test_output.py |
| `data-primary-action` | hook | False | instruction.md, test_output.py |
| `data-division` | hook | False | instruction.md, test_output.py |
| `Terms & Conditions` | copy | False | instruction.md, conftest.py, test_output.py |
| `PEOPLE ARE THE PLATFORM` | copy | False | instruction.md, conftest.py |
| `deku_admin` | credential | True | test_output.py |

## Spec documents and the sections they fed

| Doc | Fed |
|---|---|
| 00-decisions.md | every residual call, the draws, the Task Order normalisation |
| 01-PRD.md | Overview, Core features, Constraints |
| 02-TRD.md | Technical requirements |
| 03-app-flow.md | User flow |
| 04-uiux-brief.md | UI/UX notes, Front-end specification |
| 05-backend-schema.md | Data model, User roles |
| 06-implementation-plan.md | author reference only (Build plan not baseline) |

## Grading window

H2 sections present: Overview, User roles, Core features, User flow, UI/UX notes, Technical requirements, Data model, Front-end specification, Constraints, Deployment contract, Definition of done. `## Core features` is past the 2500-character judge slice by design (window_lint reports, never fails); judged obligations are restated in the rubric criteria, which carry their own facts (G52).

## Kit gate log (rendered from `_handoff/S_creato_dire_armillary-ecosystem-roster-vb_20260916_123203.gates.jsonl`)

| Gate | Tool | Exit | Verdict | stdout sha |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | `71352990ba6881fa` |
| G1/G12 | `layout_lint.py` | 0 | PASS | `347cd805ec7df5f8` |
| G46 | `structure_lint.py` | 0 | PASS | `58778bcbb4218501` |
| G50 | `docker_lint.py` | 0 | PASS | `380ed7d1c830de35` |
| G55 | `runtime_deps_lint.py` | 0 | PASS | `a0c21dca8bc5f78a` |
| G63 | `secret_lint.py` | 0 | PASS | `d0ea1c180bb5570b` |
| G48 | `truth_lint.py` | 0 | PASS | `6e1e99c89edc8949` |
| G51 | `source_lint.py` | 0 | PASS | `c586a4c05bc337f3` |
| G52 | `rubric_context_lint.py` | 0 | PASS | `511cd9b3d420b3eb` |
| G54 | `comment_lint.py` | 0 | PASS | `5bbc0fbd906212db` |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | `5bda9fb4c59d1024` |
| G11 | `leak_scan.py` | 0 | PASS | `9212f762868da97e` |
| G33 | `window_lint.py` | 0 | PASS | `97827c4bd7493a15` |
| G4/G5 | `contract_lint.py` | 0 | PASS | `c593120dd5339350` |
| G43 | `prescription_lint.py` | 0 | PASS | `48a37154126f7f09` |
| G44 | `disclosure_lint.py` | 0 | PASS | `90c5d79ea4a7ff65` |
| G10 | `no_sdk_lint.py` | 0 | PASS | `0efa3e10ead905a5` |
| G31 | `determinism_lint.py` | 0 | PASS | `48e4a471503ad8a3` |
| G14 | `reward_path_lint.py` | 0 | PASS | `6726a2d6442d5109` |
| G27/G30 | `rubric_lint.py` | 0 | PASS | `7118bff887fc30ac` |
| G41 | `flag_lint.py` | 0 | PASS | `a3901c92d5212c6a` |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | `cdf20c83e9056866` |
| G59/G60 | `codequality_lint.py` | 2 | ? | `e23941dd85e0253b` |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | `85929d5a4547e413` |
| G6 | `fixture_lint.py` | 0 | PASS | `46c95ad9e0328321` |
| G24 | `coverage_map.py` | 0 | PASS | `89ebad2679afcafc` |
| G37 | `checklist_qc.py` | 0 | PASS | `8c50440108a367dd` |
| G39 | `rubric_align_lint.py` | 0 | PASS | `84dfcc95a909f91c` |
| G28/G29 | `channel_lint.py` | 0 | PASS | `168c1b526581ab95` |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | `983f08e2bacdc70f` |
| G0/INV5 | `vendor_check.py` | 0 | PASS | `f68a520b3476c1d7` |
| G47 | `output_qc.py` | 0 | PASS | `610eb22e78aff543` |

G38 `kit_selftest.py`: PASS (32 checks). G59/G60 exit 2: no source criteria, because the vendored recompute.py at grader 0.22.0 accepts only the seven product dimensions. G40 WARN: receipts self-attested (owner equals verifier); 14 WARN rows are registry rows superseded by newer gates, each named in the receipt findings.

G51 was swept with `--source prd/steven_prd.md` and the 39 waivers in `waivers.sh` (also `_handoff/S_creato_dire_armillary-ecosystem-roster-vb_20260916_123203.waivers.json`): 6/6 colours, 266/266 topics, 1350/1350 items.

## Handoff gate list (undecided)

| Gate | Command | Expect |
|---|---|---|
| STEP 0 | build the reference app from `solution/checklist.md`, then write `solve.sh` | an app satisfying the brief |
| G13 | `docker build -f environment/Dockerfile environment` | exit 0 on linux/amd64 and linux/arm64 |
| G13 | `docker build -f tests/Dockerfile tests` | exit 0 |
| G15 | `docker compose -f environment/docker-compose.yaml up --wait` (scrubbed env) | postgres and mailpit healthy |
| G19 | `harbor run -p <task> -a oracle` twice | reward 1.0 both times |
| G18 | read `deployed` from either oracle run | 1.0 |
| G20 | `harbor run -p <task> -a nop` | reward 0.0 |
| G21 | apply a fake-integration patch (confirmation link logged, not mailed), re-run oracle | reward below 1.0 |
| G25 | reviewer exploit sweep, reference library F | 0 of 11 succeed |

## Blocking findings

None for the kit battery. Known risks for the downstream builder, not defects: the front door's WebGL scene in headless Chromium may fall back to the list, which the brief and the keyboard tests accept; portrait addresses point at an external origin and are expected to fail to load, which the generated-still fallback covers.

## Budget

`turns_expected = 200`, `tokens_expected = 8000000` (the absolute cap in qc_toml BENCH-004): a full-stack build with a WebGL front door, four scenes, a SPA of seventeen routes, SMTP mail and a versioned review workflow.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION`
