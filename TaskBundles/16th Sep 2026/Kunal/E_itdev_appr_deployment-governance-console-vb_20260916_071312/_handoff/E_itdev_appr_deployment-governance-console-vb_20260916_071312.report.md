# Build report - E_itdev_appr_deployment-governance-console-vb_20260916_071312

## Identity

| | |
|---|---|
| task code | `E_itdev_appr_deployment-governance-console-vb_20260916_071312` |
| task id | `deku/deployment-governance-console-vb` |
| cell | enterprise / it-devtools / approval-workflow |
| archetype | `deployment-governance-console` |
| variant | `b` (a companion PRD was supplied; corpus-targets `companion_variant`) |
| variant axes | `critical_depth`, `spec_sections` |
| service profile | `P3-db-auth` |
| providers | backend = `postgres`, auth = `keycloak` |
| language | `python` (the drawn backend; the drawn frontend is Preact with Vite) |
| design direction | `companion` (reference/L L.6.1; the drawn `terminal-mono` is recorded, not applied) |
| launch surface | `no_broken_links,privacy_page,single_cta,sitemap_robots,terms_page` |
| shard | 1 of 1 |
| grader pin | `0.22.0` |
| schema | `1.4` |
| exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Derived-design draws (SHA-256 over the archetype, reference/L L.4)

```
draw: render_model = spa-json-api
draw: backend = FastAPI
draw: frontend = Preact + Vite
draw: design_direction = terminal-mono     (recorded; `companion` governs)
draw: nav = breadcrumbed-drill-down
draw: work_surface = board-first
draw: create_flow = multi-step-wizard
draw: feedback = full-page-confirmation
draw: launch_surface = no_broken_links,privacy_page,single_cta,sitemap_robots,terms_page
```

## Companion carriage (G51)

| | |
|---|---|
| run mode | PRD mode: `PRD/vercel_run.yaml` |
| idea file | `PRD/vercel_idea.yaml` |
| source GenKit reads | `PRD/vercel_prd_plain.md`, 44 sections |
| topics carried | 44 / 44 |
| enumerated items carried | 10 / 10 |
| declared waivers | 0 |
| brief also carries, from the authored PRD | 359 / 359 topics, 1073 / 1073 items, 18 / 18 colours |

GenKit reads the PLAIN PRD, which `prd-generator/tools/split_prd.py` derives from the authored
file alongside a technical twin. The technical file is a build spec full of literals a brief
may not carry, and the kit records 1,018 G51 findings against it on the huly task against 0
for the plain one. Measured here the same swap took this bundle from 35 declared waivers to
zero: every waiver had been a CSS token row, a keyframe body or a vendor inventory, which is
the class the plain file excludes by construction.

The brief itself is unchanged by the swap and still carries the authored PRD in full, which
is a superset of the plain one. The second row of the table above is that measurement, kept
because it is the stronger claim.

## Checklist and coverage

| | |
|---|---|
| checklist items | 258 |
| by tag | `capability` 17, `constraint` 16, `contract` 54, `data` 37, `literal` 24, `role` 28, `ui` 82 |
| pinned literals | 47 agent-visible, 2 verifier-only |
| coverage | two-way, G24 green: every item cited by a grader, every citation resolving |

**79 items were removed from the checklist on cycle 2 and this is the report's most
important line.** They are obligations `instruction.md` states that no channel can observe
from outside the app: scheduled jobs that never run inside a grading window, startup
assertions, cache-key construction, outbox internals, break-glass, residency, retention and
erasure, and outbound webhook delivery mechanics. They remain in the brief, because the
product needs them. They are not coverage targets, because inventing a citation for an
unobservable ask is the false-coverage defect G24 exists to catch, and dropping them in
silence is the other half of the same defect.

## Graders

| | |
|---|---|
| workflows | 22 (enterprise band 13-23) |
| non-happy-path ids | 14: `invalid_login_is_refused`, `anonymous_read_is_unauthenticated`, `duplicate_webhook_delivery_creates_one_deployment`, `invalid_webhook_signature_is_refused`, `failed_build_cannot_move_production`, `requester_cannot_approve_own_request` ... |
| browser substeps | 21 |
| pytest substeps | 39 |
| critical substeps | 20 |
| pytest module | `tests/test_output.py`, one module, 39 tests |
| sections covered | core features, data integrity, authorization, edge cases |

## Rubric

| | |
|---|---|
| criteria | 18 (16 positive, 2 negative) |
| positive total | 42 |
| dimension shares against the frozen weights | accessibility 0.048; functionality 0.262; instruction_following 0.31; motion 0.048; responsiveness 0.048; ui_visual 0.143; ux_flow 0.143 |
| compiled answer-key items | 39 at mode `compiled`, share 1.0 against a 0.6 floor |

## Grading-window measurement (reported, never failed)

| section | chars | reference |
|---|---|---|
| Core features | 42906 | 2400 |
| User flow | 8310 | 1900 |
| UI/UX notes | 15060 | 1700 |
| Constraints | 1416 | 800 |
| User roles | 3095 | 1000 |
| Overview | 3164 | 700 |

`## Core features` runs far past the 2,500-char point where `run_rubric.py` slices one
section, so its tail reaches the agent in full and the judge not at all. This is recorded
and NOT repaired: `window_lint.py` and `generate_instruction.md` section 4 both state that
length is measured and never failed, and that cutting a real rule to fit the window trades
reward-driving completeness for a diagnostic number. The judged criteria are self-contained
and carry their own `evaluation_rule`, so nothing graded depends on the sliced prose.

## Kit gate log (rendered from the receipts, never transcribed)

32 of 33 gate runs green.

| gate | tool | exit | verdict |
|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS |
| G1/G12 | `layout_lint.py` | 0 | PASS |
| G46 | `structure_lint.py` | 0 | PASS |
| G50 | `docker_lint.py` | 0 | PASS |
| G55 | `runtime_deps_lint.py` | 0 | PASS |
| G63 | `secret_lint.py` | 0 | PASS |
| G48 | `truth_lint.py` | 0 | PASS |
| G51 | `source_lint.py` | 0 | PASS |
| G64 | `run_lint.py` | 0 | PASS |
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

`G59/G60` exits 2 NOT-APPLICABLE: the bundle ships no `evaluation_target: "source"`
criterion, which is a legal state the vendored `recompute.py` requires (it renders
`judged_criteria` only and rejects a code dimension). `G40` exits 0 WARN: every
certification prompt has a current bundle-bound receipt, and the warnings are the
SELF-ATTESTED notes plus the advisory generator prompts.

## Prompt-driven gates (G40 receipts)

| prompt | gate | verdict | checks answered | verifier |
|---|---|---|---|---|
| `QC_instruction.md` | G34 | CHANGES REQUIRED | 24 | self |
| `QC_spec.md` | G34 | PASS | 15 | self |
| `qc_docker.md` | G35 | PASS | 105 | self |
| `qc_rubric.md` | G53 | PASS | 16 | self |
| `qc_solution_checklist.md` | G37 | PASS | 0 | self |
| `qc_toml.md` | G36 | PASS | 120 | self |
| `task_code_verifier.md` | G3 | VALID | 12 | self |

`QC_instruction.md` returns CHANGES REQUIRED on three WARN checks that were adjudicated and
deliberately not repaired: **A8**, the three `AUTH_*` variables that the section 2.3
canonical table has no row for because it carries no auth slot at all; **B3**, the third
difficulty lever, which section 2.1 retires from the baseline emission; and **C7**, the
grading-window overrun described above. Each is a place where two kit documents disagree
and the newer one governs. They are on the record rather than resolved by weakening a check.

## Blocking findings

NONE at the kit layer. The bundle is MECHANICALLY-GREEN.

Two things are not proven here and cannot be: nothing has been built, started or run, and
the seven certification prompts were self-attested rather than independently reviewed.

## Budget estimate

`turns_expected = 220`, `tokens_expected = 8000000`. The reasoning: the brief carries a
full public surface of fifteen routes plus a console of eighteen, twenty-three tables, and
a contended promotion path that has to be right under concurrency. That is at the top of
the corpus band rather than the middle, and the concurrency work in particular is where a
model spends turns rediscovering that a read-modify-write loses an approval.

## Exit state

**MECHANICALLY-GREEN, NO-SOLUTION.** Not admissible. Nothing counts toward corpus targets
until the app lands downstream and `harbor run -a oracle` returns 1.0 twice.
