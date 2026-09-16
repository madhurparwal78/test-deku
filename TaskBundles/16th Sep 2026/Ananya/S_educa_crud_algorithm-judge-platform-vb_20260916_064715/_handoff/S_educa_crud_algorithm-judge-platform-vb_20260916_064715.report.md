# Build report - S_educa_crud_algorithm-judge-platform-vb_20260916_064715

Exit state: **NOT MECHANICALLY-GREEN: G24, G47**. NO-SOLUTION: the bundle carries no reference app and is not admissible.

Rendered from `_handoff/S_educa_crud_algorithm-judge-platform-vb_20260916_064715.gates.jsonl`. Every verdict below is copied from a receipt; none is authored here.

## Identity

| Field | Value |
|---|---|
| task code | S_educa_crud_algorithm-judge-platform-vb_20260916_064715 |
| task id | "deku/algorithm-judge-platform-vb" |
| category | "solo_founder" |
| domain | "education-courses" |
| pattern | "crud-catalog" |
| service profile | "P1-db" |
| providers per slot | backend = postgres |
| variant | "b" |
| variant axes | ["critical_depth", "spec_sections"] |
| language | "typescript" |
| spec sections given | ["overview", "roles", "features", "flow", "uiux", "techrequirements", "datamodel", "constraints", "contract"] |
| design direction | "companion" |
| launch surface | "colour_contrast,favicon,no_broken_links,single_cta,social_preview" |
| grader version | "0.22.0" |
| schema version | "1.4" |
| authors | kaustubh.dalvi@ethara.ai (QL), ananya.tandon.int43@ethara.ai (contributor) |
| turns / tokens expected | 170 / 7000000 |
| shard | 1 of 1 |

turns and tokens sit on the hard tier: a companion-backed task whose graded surface includes a judging service, sixteen workflows and a 505-item coverage target.

## Inputs

- Task Order: category solo_founder, domain education-courses, pattern crud-catalog, archetype algorithm-judge-platform, the supplied idea, QL and contributor addresses.
- Companion PRD: `Prds/leetcode_prd.md`, 7,860 lines. Variant `b` per `companion_variant`.
- The Task Order named the pattern `catalog-browse`, which is not in the level-3 enum. Minted as `crud-catalog`; recorded in `_spec/.../00-decisions.md`.

## Feature resolution table

| Candidate (from the companion) | Verdict | Where | Reason |
|---|---|---|---|
| Catalogue with six filter axes, facet counts, cursor pages | INCLUDED | Core features, catalogue | the Task Order's own centre of gravity |
| Problem workspace, tabs, spoiler disclosures, split pane | INCLUDED | Core features, workspace | named by the idea |
| Editor, drafts per language, console | INCLUDED | Core features, editor | named by the idea |
| Run against submit, the judge, verdicts, limits, isolation, comparators | INCLUDED | Core features, judge | named by the idea |
| Solved set, counters, percentiles, submission history | INCLUDED | Core features, progress | named by the idea |
| Daily challenge, streak, coins | INCLUDED | Core features, progress | companion Section 31 |
| Study plans, explore cards, discussion | INCLUDED | Core features, learning | study plans named by the idea |
| Contests, scoring, standings, ladder | INCLUDED | Core features, contests | timed contests named by the idea |
| Accounts, sessions, lockout, in-product verification | INCLUDED | Core features, auth | per-user history needs identity |
| Paid tier, region price list, entitlement gate | INCLUDED | Core features, paid tier | companion Sections 16 and 35 |
| External card processor | DROPPED | Constraints | no payments slot on P1-db; entitlement granted in-app |
| Outbound mail for verification and recovery | DROPPED | Constraints | no email slot; verification completed in-product, recovery cut |
| Live channel for verdicts | DROPPED | Constraints | no realtime slot; the page asks again until the verdict settles |
| Fourteen compiled and managed languages | DROPPED | Constraints | python3 and javascript only, both in the image |
| Operator console, impersonation | DROPPED | Constraints | admin work cannot be asked of the agent (INV4); /admin/ answers not-found |
| Outbox, rate limits, quotas, plagiarism screening, observability, response budgets | DROPPED | G51 waivers | internal mechanisms no grader in this verifier observes |
| Streak freezes, rating recomputation, virtual contest runs | DROPPED | G51 waivers | time-dependent or offline mechanisms with no observable grader |
| Account deletion, recovery tokens, session lifetimes | DROPPED | G51 waivers | need days of wall clock or outbound mail to observe |
| Output normalisation rule | DROPPED | G51 waiver | invisible under a function-signature harness; comparators pinned on seeded problems instead |
| Print stylesheet, forced colours | DROPPED | G51 waivers | neither grader can emulate print or forced colours |
| Graph endpoint | DROPPED | 00-decisions | one REST surface; the graph surface was informational |
| Icon path coordinates, asset recipes | DROPPED | 00-decisions, G51 waiver | asset recipe, not an observable |

## Slot obligation table

| Slot | Provider | Critical pytest substep | Status |
|---|---|---|---|
| backend | postgres | `test_accepted_submission_persists_a_solved_row_for_that_member` and five more critical data-integrity substeps | MET |

## Graders

- workflows: 16 (solo_founder band 10 to 16)
- browser substeps: 45; pytest substeps: 132; critical substeps: 18
- non-happy-path workflow ids: 4 - `a_runaway_solution_is_rejected_by_the_limits`, `counters_and_duplicate_submissions_hold_under_contention`, `another_members_records_cannot_be_read`, `a_gated_problem_is_denied_without_an_entitlement`
- test module: `tests/test_output.py`, 132 test functions, grouped as core features, authorization, data integrity and edge cases
- rubric criteria: 17 (15 positive, 2 negative)

| Dimension | Positive share | Target | Band |
|---|---|---|---|
| instruction_following | 0.289 | 0.30 | inside |
| functionality | 0.178 | 0.25 | inside |
| ux_flow | 0.156 | 0.15 | inside |
| ui_visual | 0.200 | 0.15 | inside |
| motion | 0.022 | 0.05 | inside |
| accessibility | 0.067 | 0.05 | inside |
| responsiveness | 0.089 | 0.05 | inside |

## Literals Ledger

191 entries. Full values and carriers are in `_handoff/S_educa_crud_algorithm-judge-platform-vb_20260916_064715.literals-ledger.json`.

| Class | Count | Examples |
|---|---|---|
| account | 6 | `member@example.com`, `member2@example.com`, `subscriber@example.com`, `nadia_roux` |
| credential | 1 | `deku-demo-pw-2026` |
| design_phrase | 28 | `top navigation bar`, `two-tab switcher`, `split`, `compact` |
| endpoint | 17 | `/api/health`, `/api/auth/register`, `/api/auth/login`, `/api/auth/logout` |
| env_var | 4 | `DATABASE_URL`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `DB_ADMIN_URL` |
| motion_moment | 8 | `skeleton breath`, `topic rail expanding`, `contest ladder entrance`, `reward badge` |
| number | 18 | `240`, `300`, `64KB`, `65536` |
| route | 13 | `/problemset/`, `/problems/two-sum/description/`, `/contest/`, `/studyplan/` |
| scheme | 22 | `<number>. <title>`, `Search questions`, `0/240 Solved`, `Search for a company...` |
| seed_record | 42 | `1. Two Sum`, `58.1%`, `2. Add Two Numbers`, `4. Median of Two Sorted Arrays` |
| status | 32 | `Accepted`, `Wrong Answer`, `Time Limit Exceeded`, `Memory Limit Exceeded` |

## spec/ documents

Authored outside the bundle at `Output/16sept_leetcode/_spec/S_educa_crud_algorithm-judge-platform-vb_20260916_064715/`.

| Document | Feeds |
|---|---|
| 00-decisions.md | draw lines, residual calls, companion carry table |
| 01-PRD.md | Overview, Core features, Constraints |
| 02-TRD.md | Technical requirements |
| 03-app-flow.md | User flow, API shapes |
| 04-uiux-brief.md | UI/UX notes |
| 05-backend-schema.md | Data model, User roles |
| 06-implementation-plan.md | authoring-side only; Build plan is not emitted |

## Grading window

| Section | Chars | Reference | Note |
|---|---|---|---|
| Core features | 33966 | 2400 | past the 2,500 slice |
| User flow | 5332 | 1900 | past the 2,500 slice |
| UI/UX notes | 13135 | 1700 | past the 2,500 slice |
| Constraints | 1067 | 800 | inside |
| User roles | 2389 | 1000 | inside |
| Overview | 2510 | 700 | past the 2,500 slice |
| joined six | 58399 | 8,800 | past the 9,000 join slice |

G33 reports length and fails nothing on it. The tail of a long section reaches the agent in full and the judge not at all.

## Kit gate log

| Gate | Tool | Exit | Verdict | stdout sha |
|---|---|---|---|---|
| G2/G16 | validate_task.py | 0 | PASS | `d922e4efa593ff33` |
| G1/G12 | layout_lint.py | 0 | PASS | `be8e2347197a585e` |
| G46 | structure_lint.py | 0 | PASS | `160ddfb00f9156f4` |
| G50 | docker_lint.py | 0 | PASS | `380ed7d1c830de35` |
| G55 | runtime_deps_lint.py | 0 | PASS | `a0c21dca8bc5f78a` |
| G63 | secret_lint.py | 0 | PASS | `0ee6ea136a6e8566` |
| G48 | truth_lint.py | 0 | PASS | `015f7c533c402fd0` |
| G51 | source_lint.py | 0 | PASS | `e8414aaa260eeeec` |
| G52 | rubric_context_lint.py | 0 | PASS | `0927ddd77a7799e7` |
| G54 | comment_lint.py | 0 | PASS | `2af186057965f198` |
| G17 | secret_hygiene_lint.py | 0 | PASS | `3d2cd173f5565e7e` |
| G11 | leak_scan.py | 0 | PASS | `c361e20bcabd1959` |
| G33 | window_lint.py | 0 | PASS | `685accd33b443c9f` |
| G4/G5 | contract_lint.py | 0 | PASS | `edebf2a86002474d` |
| G43 | prescription_lint.py | 0 | PASS | `07c40ffbed121044` |
| G44 | disclosure_lint.py | 0 | PASS | `10637141c33a66f9` |
| G10 | no_sdk_lint.py | 0 | PASS | `739dce12f23b07d6` |
| G31 | determinism_lint.py | 0 | PASS | `56211af5679a77fe` |
| G14 | reward_path_lint.py | 0 | PASS | `b7a2f9ee042fb72b` |
| G27/G30 | rubric_lint.py | 0 | PASS | `bf69cd64a41f02c7` |
| G41 | flag_lint.py | 0 | PASS | `55c59ed77319052d` |
| G56/G57/G58 | if_lint.py | 0 | PASS | `cdf20c83e9056866` |
| G59/G60 | codequality_lint.py | 2 | ? | `e23941dd85e0253b` |
| G7/G8/G9/G32/G45 | workflow_lint.py | 0 | WARN | `7f9e8168f09d2add` |
| G6 | fixture_lint.py | 0 | PASS | `16ce02959fc5c691` |
| G24 | coverage_map.py | 1 | FAIL | `9df33c12d4e79c9f` |
| G37 | checklist_qc.py | 0 | PASS | `13ae4797af8c46ef` |
| G39 | rubric_align_lint.py | 0 | PASS | `3ad35676744c659a` |
| G28/G29 | channel_lint.py | 0 | PASS | `7fb450ce16615bcb` |
| G40 | prompt_receipt_lint.py | 0 | WARN | `bf01063a20bf2236` |
| G0/INV5 | vendor_check.py | 0 | PASS | `a33c590e389e766c` |
| G47 | output_qc.py | 1 | FAIL | `e848f19aab4be106` |

G59/G60 exits 2: the bundle carries no code-quality criteria, so the gate is NOT-APPLICABLE. The vendored recompute.py renders no code_criteria block, so the advisory source channel cannot be generated here.

G45 is advisory and reports WARN: browser:pytest substeps 45:132. The standard verifier tier fixes timeout_sec at 3600.0 (qc_toml VERIF-002), so browser substeps carry two asks each rather than one.

Adversarial QC prompts, run in this session, with receipts in `_handoff/S_educa_crud_algorithm-judge-platform-vb_20260916_064715.receipts.json`: task_code_verifier (G3), QC_instruction and QC_spec (G34), qc_docker (G35), qc_toml (G36), qc_solution_checklist (G37), qc_rubric (G53). Every one is SELF-ATTESTED: the same agent authored and reviewed, so owner != verifier is not satisfied and an independent reviewer should re-run them.

## Blocking findings

**G24 coverage is RED on 7 declared-ungraded item(s).** The checklist carries 505 items and 498 are cited by a grader that observes them.

| Item | Tag | Ask |
|---|---|---|
| C-TR-01 | constraint | The backend is a NestJS application rendering Handlebars templates. |
| C-TR-06 | constraint | The app uses only the named libraries, no second database, cache, queue, object store, identity provider, mail vendor. |
| C-DM-02 | literal | `/app/USER_README.md` lists each seeded account beside the password `deku-demo-pw-2026`. |
| C-CN-10 | constraint | The server makes no external network call at run time. |
| C-DC-06 | literal | `/app/USER_README.md` carries the seeded credentials. |
| C-DC-07 | contract | Reserved `.browser_screenshots/`, `.downloads/` directories exist at the app root. |
| C-DC-12 | constraint | The app uses only the named providers with no edge function, persistent volume, fixed container name or custom network. |

Every other ask is graded: pytest tests assert the API, the database and page markup; browser substeps and rubric criteria judge what renders. Each citation shares its wording with the test or step that observes it (G24 earned check), each part is graded by one judgment channel (G28/G29), and every ui item has a browser substep or criterion (G39).

Four are observable only by reading the app's source: the NestJS and Handlebars stack, the named-libraries rule, the server's own outbound network, and the providers, volumes and networks bullet. The reward path may not read source (INV6), and the advisory source channel cannot be rendered by the vendored recompute.py. Three concern files inside the app container, `/app/USER_README.md` and the reserved `.browser_screenshots/` and `.downloads/` directories: under `[verifier].environment_mode = "separate"` the grader runs in its own image and has no view of `/app`, so the test that read them was removed rather than left to fail. Stage 3 says neither invent a citation nor drop the obligation: record and escalate. This is that record, OPEN-DECISION D-H.

## Handoff gates

Undecided here; see `S_educa_crud_algorithm-judge-platform-vb_20260916_064715.handoff.md`.

## Versions

- kit: deku-green-field (GreenField-GenKit2)
- vendored grader: "0.22.0"
- target schema: "1.4"

Exit state: **NOT MECHANICALLY-GREEN: G24, G47**
