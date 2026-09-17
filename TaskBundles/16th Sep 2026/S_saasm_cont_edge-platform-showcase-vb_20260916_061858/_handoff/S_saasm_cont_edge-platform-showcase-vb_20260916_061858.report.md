# Build report - S_saasm_cont_edge-platform-showcase-vb_20260916_061858

## Identity

| | |
|---|---|
| Task code | `S_saasm_cont_edge-platform-showcase-vb_20260916_061858` |
| Task id | `deku/edge-platform-showcase-vb` |
| Cell | solo_founder / saas-micro-tools / content-publishing |
| Service profile | `P4-db-storage` |
| Providers | backend = `postgres`, storage = `minio` |
| Variant | `b` (a companion document was supplied) |
| variant_axes | `critical_depth`, `spec_sections` |
| Language | `python` (Litestar backend, Angular frontend, spa-json-api) |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 (no device sharding in this run) |
| Kit | deku-green-field @ 806eb0a, G38 self-test green (32 checks) |
| Verifier mode | `separate` (the kit default; the grader ships its own image) |
| Vendored grader | 0.22.0 |
| Target schema | 1.4 |
| Companion | `prd/fastly_prd.md` |

## Feature resolution

| Candidate | Verdict | Where it landed | Reason |
|---|---|---|---|
| Shared chrome: two-row bar, seven menu triggers, deep footer | INCLUDED | instruction.md ## Core features, ## Front-end specification | companion 5.1-5.4 |
| Services catalogue, thirty-two named services | INCLUDED | ## Core features, seeded `service` table | companion 21.3, the site's own taxonomy |
| Network globe | INCLUDED | ## Core features, ## Front-end specification | companion 8.10 |
| Live statistics band, five rows | INCLUDED | ## Core features, seeded `statistic` table | companion 8.9 |
| Eight capability modules with pinned result lines | INCLUDED | ## Core features, seeded `capability` table | companion 8.1-8.8 |
| Blog index, article, editorial desk, cover images | INCLUDED | ## Core features, `article` table, MinIO | pattern critical focus: object in the store, draft not publicly readable |
| Free trial signup | INCLUDED | ## Core features, ## User flow | the Task Order's closing flow |
| Cookie choice, custom not-found, no broken links, one primary action, narrow viewport | INCLUDED | ## Core features, ## UI/UX notes | reference O draw over the archetype |
| Newsletter / demo request / contact mail | DROPPED | - | the profile carries no mail slot; every call routes to /signup instead |
| Payment, plan purchase, invoice | DROPPED | ## Constraints | no payments slot; the pricing route describes plans only |
| Optional live metrics feed (companion 19) | DROPPED | - | no outbound network at run time; the modules read the app's own seeded rows |
| Third-party chat, consent platform, analytics tag | DROPPED | ## Constraints, ## Technical requirements | out of scope in the companion and forbidden at run time |
| Real translation of the seven locales | DROPPED | ## Constraints | the companion captured one locale; the control records the choice only |
| Icon coordinate tables, easing curves, keyframe bodies, font families and sizes | DROPPED from the brief | kept in `_spec/04-uiux-brief.md` | the tasker's instruction: describe the element, never name the value |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| backend (db) | `postgres` | MET | `test_seeded_article_rows_carry_their_pinned_fields`, `test_seeding_is_idempotent_across_every_seeded_table` read real rows through the declared backend |
| storage | `minio` | MET | `test_cover_upload_lands_in_the_object_store_under_its_key` reads the object out of the declared bucket at the scheme's key |

## Grading layer

- Workflows: 16 (band 10-16)
- Browser substeps: 68
- pytest substeps: 36
- Critical substeps: 12
- Non-happy-path ids: signup_with_an_invalid_address_is_refused, wrong_password_sign_in_is_denied, draft_article_and_its_cover_are_denied_to_every_other_reader, members_article_body_is_denied_to_a_visitor, reader_cannot_reach_the_desk_and_an_author_cannot_reach_what_it_does_not_own, invalid_article_write_is_refused
- One pytest module, `tests/test_output.py`, 36 tests covering core features, data integrity, storage, authorization and the edge cases
- Checklist: 799 items (capability 135, constraint 144, contract 35, data 40, literal 126, role 40, ui 279)

## Rubric

- Criteria: 19 (18 positive, 1 negative)
- Positive total: 40

| Dimension | Share | Target | Within band |
|---|---|---|---|
| instruction_following | 0.30 | 0.30 | yes |
| functionality | 0.25 | 0.25 | yes |
| ux_flow | 0.15 | 0.15 | yes |
| ui_visual | 0.15 | 0.15 | yes |
| motion | 0.07 | 0.05 | yes |
| accessibility | 0.05 | 0.05 | yes |
| responsiveness | 0.03 | 0.05 | yes |

## Literals ledger

204 entries. One verifier-only value (`DB_ADMIN_URL`), carried by `task.toml` alone.

| Class | Entries |
|---|---|
| `account` | 3 |
| `credential` | 1 |
| `endpoint` | 20 |
| `env_var` | 4 |
| `number` | 9 |
| `scheme` | 35 |
| `seed_record` | 129 |
| `status` | 3 |

## Spec folder

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the recast, the companion carry table, the G51 waivers |
| `01-PRD.md` | ## Overview, ## Core features, ## Constraints |
| `02-TRD.md` | ## Technical requirements |
| `03-app-flow.md` | ## User flow |
| `04-uiux-brief.md` | ## UI/UX notes, ## Front-end specification |
| `05-backend-schema.md` | ## Data model, ## User roles |
| `06-implementation-plan.md` | nothing: ## Build plan is not emitted at baseline |

## Grading window

```
VERDICT  PASS   (/home/grt/Downloads/Greenfield_testing/output/16-sep-2026/S_saasm_cont_edge-platform-showcase-vb_20260916_061858/instruction.md)
section        H2                chars  reference  flag
core_features  Core features     28083       2400  past-slice
user_flow      User flow          4734       1900  past-slice
ui_ux_notes    UI/UX notes       12721       1700  past-slice
constraints    Constraints        1013        800  over-reference
user_roles     User roles         1872       1000  over-reference
overview       Overview           2660        700  past-slice
joined total                     51083       8800  past-slice
first four                       46551       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```

The brief carries no length limit (`generate_instruction.md` section 4). Every section past its
reference length is reported, never failed: the tail reaches the agent in full and the judge reads
a truncated excerpt. The tasker asked explicitly for the UI and UX detail, so nothing was cut to fit.

## Kit gate log (rendered from the receipts, never transcribed)

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

Receipts: `_handoff/S_saasm_cont_edge-platform-showcase-vb_20260916_061858.gates.jsonl`, one row per gate carrying the SHA-256 of every byte it read.

## Blocking findings

NONE. Every battery-1 and battery-2 gate is green, no spec gap and no harness gap prevented a
required check, and every declared slot is MET.

Two states are recorded rather than outstanding:

- **G59/G60 NOT-APPLICABLE.** The bundle carries no source-target criterion. `00-RUN.md`'s
  stage table runs S3.5 straight into S4 and lists no S3.6, and the vendored `recompute.py` has
  no `code_criteria` handling at all, so a code rubric authored into `grounding.yaml` today
  would be a key no generator reads. Commit 1b99060 says the same in its own words: code_quality
  is enforced at author time and is not yet read by the judge.
- **G40 WARN, SELF-ATTESTED.** Every certification prompt has a current, bundle-bound receipt,
  but `verifier` reads `self` on all of them: one agent authored and certified. The kit's rule is
  owner != verifier, so these are recorded verdicts, never independent ones.

One placement decision is on the record rather than outstanding: the tasker first named
`GreenField-GenKit2/output/16-sep-2026/`, which sits inside the generation kit and fails CON-1. The
bundle was moved one level up to `output/16-sep-2026/`, beside the kit, and G46 and G47 are green
there. Nothing inside the bundle changed.

## Budget

`turns_expected = 150`, `tokens_expected = 5200000`. The reasoning: two role boundaries, five
seeded content tables, thirty-two catalogue rows and eight animated modules put this above the
120-140 turn band a medium task carries, while the single object-store slot and the absence of
payments, mail and realtime keep it below the 170-turn hard band. `difficulty` stays empty until
calibration measures it.

## Exit state

`MECHANICALLY-GREEN, NO-SOLUTION` - **not admissible**. The bundle carries no reference app. Build
one downstream from `solution/checklist.md`, then run the seven handoff gates listed in
`_handoff/S_saasm_cont_edge-platform-showcase-vb_20260916_061858.handoff.md`.
