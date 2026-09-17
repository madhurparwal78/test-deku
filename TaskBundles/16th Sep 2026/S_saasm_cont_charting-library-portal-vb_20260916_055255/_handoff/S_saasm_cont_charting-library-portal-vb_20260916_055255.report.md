# Build report - S_saasm_cont_charting-library-portal-vb_20260916_055255

## Identity

| Field | Value |
|---|---|
| task code | `S_saasm_cont_charting-library-portal-vb_20260916_055255` |
| task id | `deku/charting-library-portal-vb` |
| cell | solo_founder / saas-micro-tools / content-publishing |
| service_profile | `P4-db-storage` |
| providers | `backend = postgres`, `storage = minio` |
| variant | `b` on `critical_depth` and `spec_sections` |
| language | `python` |
| design_direction | `companion` (the draw for this archetype, `playful-consumer`, is recorded and does not govern) |
| launch_surface | `custom_404,favicon,privacy_page,social_preview,spam_protection` |
| spec_sections_given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| shard | 1 of 1 (single-operator run) |
| kit revision | `806eb0a` |
| vendored grader | `0.22.0`, FORKED: `test.sh` was stripped of its 35 whole-line comments and `MANIFEST.json` re-minted in kit 78e5ba6, so the INV5 pin now attests to the kit's copy rather than the harness's |
| verifier mode | `separate` (the kit default as of 11eaf7b; `shared` stays legal) |
| pytest module | `tests/test_output.py` (renamed from `test_pytest.py` in da24d3b; the generated compiled-rubric file took `test_ans.py`) |
| target schema | `1.4` |
| exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

The Task Order arrived with `domain: saas-productivity`, which is not one of the kit's
36 domains. The companion's own Section 51.4 records the same substitution and says the
enum has no member for open source developer tooling. Mapped to `saas-micro-tools`, the
nearest solo_founder member. Recorded in `_spec/.../00-decisions.md` rather than silently
re-keyed.

Every derived-design value is drawn from `sha256("charting-library-portal")`, the
archetype identity reference/L §L.4 fixes, not the six-field code:
`render_model = mpa-progressive`, `backend = FastAPI + Jinja`,
`frontend = Alpine.js + server templates`, `nav = sidebar-nav`,
`work_surface = split detail-pane`, `create_flow = inline-row`, `feedback = toast`.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| The versioned option reference | INCLUDED | ## Core features rules 4-12 | the Task Order names it first; the whole portal funnels through it |
| The interface reference | INCLUDED | ## Core features rules 13-15 | named in the Task Order; same shell, disjoint fragment space |
| The searchable example gallery | INCLUDED | ## Core features rules 16-20 | named in the Task Order; the companion's three missing additions become requirements |
| The live example editor | INCLUDED | ## Core features rules 21-25 | named in the Task Order; carries the sandbox and both failure shapes |
| Shared snippets | INCLUDED | ## Core features rules 26-29 | the Task Order's 'saves the result as a shared snippet' |
| The theme designer and registry | INCLUDED | ## Core features rules 30-34 | named in the Task Order; import validation is the stranger-data boundary |
| The custom bundle builder | INCLUDED | ## Core features rules 35-38 | the Task Order's 'or a custom compiled bundle' |
| The release archive | INCLUDED | ## Core features rules 39-42 | the Task Order's 'a release archive' |
| Contributed examples | INCLUDED | ## Core features rules 43-46 | carries the content-publishing critical focus: object in the store, not publicly readable |
| The portal's own surface | INCLUDED | ## Core features rules 47-49 | the five drawn launch-surface obligations, numbered among the features |
| Accounts | INCLUDED | ## Core features ### Auth | required once seeded accounts exist; exists only so a contributor manages what they made |
| Spreadsheet converter | DROPPED | ## Constraints bullet 2 | companion Section 19; outside the Task Order's six named surfaces |
| Live co-editing of a snippet | DROPPED | ## Constraints bullet 3 | companion Sections 21.9, 35.4, 35.5; a convergent-edit channel is a task of its own |
| Palette extraction from an image | DROPPED | ## Constraints bullet 4 | companion Section 39.4; needs an image upload the portal does not have |
| Second language | DROPPED | ## Constraints bullet 5 | companion Sections 2.3, 27; one language keeps the route table assertable |
| Handbook, FAQ, cheat sheet, resources, extensions | DROPPED | ## Constraints bullet 6 | companion Sections 2.5, 16, 17.7, 23.6 |
| Community section | DROPPED | ## Constraints bullet 7 | companion Sections 23, 41 |
| Security route and advisory feed | DROPPED | ## Constraints bullet 8 | companion Sections 24, 37.6 |
| Telemetry dashboard | DROPPED | ## Constraints bullet 9 | companion Section 43.5; the privacy stance is carried, the dashboard is not |
| Schema migration engine | DROPPED | ## Constraints bullet 10 | companion Section 31; the removed-property answer stands without a rewriter |
| Chart recommendation | DROPPED | ## Constraints bullet 2 | companion Section 40; follows the spreadsheet converter out |
| Global cross-document search | DROPPED | waived on G51 | companion Section 38; the in-document search and the gallery search are carried |
| Distinct playground registrable domain | DROPPED | waived on G51 (`registrable`) | companion Sections 34.2, 42.6; impossible on one origin, so rule 25 carries the enforceable half |

## Slot obligations

| Slot | Provider | Verdict | Evidence |
|---|---|---|---|
| `backend` | postgres | MET | `test_seeded_accounts_are_stored_once_with_hashed_passwords` (critical) reads PostgreSQL through the shared adapter and asserts the seeded rows, the hash and the credentials file; three more seed graders read the same store |
| `storage` | minio | MET | `test_a_proposed_thumbnail_upload_lands_in_the_object_store` (critical) asserts the object exists in the bucket at its digest key and that no copy sits on the container's disk; `test_stored_object_keys_follow_their_declared_key_schemes` and `test_a_ready_bundle_artifact_is_uploaded_to_the_object_store` read it too |

No slot is UNMET.

## Grading surface

| Measure | Value |
|---|---|
| workflows | 16 (solo_founder band 10-16) |
| browser substeps | 27 |
| pytest substeps | 63 |
| browser:pytest ratio | 0.43 (G45 band 0.40-2.00) |
| critical substeps | 8 |
| non-happy-path workflow ids | 7 |
| pytest module | one, `tests/test_output.py`, carrying core features, data integrity, authorization, edge cases and the storage slot |
| judged criteria | 13 positive, 0 negative |
| checklist items | 739 |

Category mix: `business_rule` 21, `core_outcome` 1, `data_integrity` 12, `presentation` 13, `security` 11, `validation` 5. G9's floors are
met: 1 `core_outcome`, 12 `data_integrity` with a `backend` slot
declared, and 11 `security` with three workflow ids carrying a denial
token.

| Workflow id | Browser | Pytest | Critical |
|---|---|---|---|
| `seeded_corpus_is_served_from_one_origin` | 3 | 8 | 1 |
| `wrong_password_login_is_refused` | 2 | 3 | 1 |
| `reader_cannot_reach_a_contributor_endpoint` | 1 | 3 | 1 |
| `option_path_to_editor_to_shared_snippet` | 2 | 3 | 1 |
| `property_block_states_which_kind_of_default_it_has` | 1 | 5 | 0 |
| `older_version_omits_a_later_property` | 2 | 3 | 0 |
| `document_search_ranks_by_the_first_matching_segment` | 1 | 3 | 0 |
| `gallery_search_and_filters_narrow_the_corpus` | 2 | 3 | 0 |
| `editor_budget_stops_an_evaluation_that_never_ends` | 2 | 2 | 0 |
| `withdrawn_snippet_answers_gone` | 1 | 3 | 0 |
| `theme_import_is_refused_for_a_function_value` | 2 | 3 | 0 |
| `unknown_module_selection_is_refused` | 1 | 3 | 0 |
| `two_identical_bundle_requests_build_once` | 1 | 3 | 0 |
| `published_release_edit_is_denied` | 1 | 4 | 1 |
| `proposed_thumbnail_is_forbidden_to_everyone_but_its_owner` | 2 | 8 | 3 |
| `portal_surface_states_its_own_pages` | 3 | 6 | 0 |

## Checklist

| Section | Items |
|---|---|
| `C-CF` | 211 |
| `C-CN` | 14 |
| `C-DC` | 56 |
| `C-DM` | 100 |
| `C-FE` | 146 |
| `C-OV` | 8 |
| `C-RL` | 24 |
| `C-TR` | 50 |
| `C-UF` | 52 |
| `C-UX` | 78 |

Tag mix: `capability` 68, `constraint` 224, `contract` 39, `data` 6, `literal` 160, `role` 13, `ui` 229. Every item carries
exactly one named grader, and the emitter refuses to write unless every pytest test,
every browser substep and every judged criterion is cited by at least one item.

## Judged rubric

| Dimension | Points | Share | Target | Inside 0.10 band |
|---|---|---|---|---|
| `instruction_following` | 13 | 0.289 | 0.30 | yes |
| `functionality` | 11 | 0.244 | 0.25 | yes |
| `ux_flow` | 6 | 0.133 | 0.15 | yes |
| `ui_visual` | 6 | 0.133 | 0.15 | yes |
| `motion` | 3 | 0.067 | 0.05 | yes |
| `accessibility` | 3 | 0.067 | 0.05 | yes |
| `responsiveness` | 3 | 0.067 | 0.05 | yes |

Positive total 45; no negative criteria, so the negative-magnitude cap is trivially
satisfied. `task completion` share 10/13, inside the 60-80% band.
`tests/rubric.json` is GENERATED from `solution/trinity/grounding.yaml` by the vendored
`recompute.py`; G48 re-runs the generator under `--check` on every sweep.

## Literals ledger

| Class | Count | Verifier-only | Example |
|---|---|---|---|
| `account` | 3 | 0 | `contributor@example.com` |
| `credential` | 1 | 0 | `deku-demo-pw-2026` |
| `design_phrase` | 7 | 0 | `drawn as the object a reader is about to write` |
| `endpoint` | 13 | 0 | `/api/health` |
| `env_var` | 10 | 3 | `DATABASE_URL` |
| `motion_moment` | 5 | 0 | `unfold one after another` |
| `number` | 37 | 0 | `5.4.3` |
| `route` | 15 | 0 | `/login` |
| `scheme` | 47 | 0 | `title.show` |
| `seed_record` | 50 | 0 | `Noor Haddad` |
| `status` | 38 | 0 | `proposed` |

226 entries, 3 verifier-only. Carriers are resolved against the bytes on
disk rather than declared by hand, so a claimed carrier always contains the value.

## Authoring spec folder

At `Output/16sept-echarts/_spec/S_saasm_cont_charting-library-portal-vb_20260916_055255/`, excluded from the bundle (CON-5).

| Doc | Fed |
|---|---|
| `00-decisions.md` | the draws, the taxonomy substitution, the residual calls, the companion carry table |
| `01-PRD.md` | `## Overview`, `## Core features`, `## Constraints` |
| `02-TRD.md` | `## Technical requirements` |
| `03-app-flow.md` | `## User flow`, `## Deployment contract` API shapes |
| `04-uiux-brief.md` | `## UI/UX notes`, `## Front-end specification` |
| `05-backend-schema.md` | `## Data model`, `## User roles` |
| `06-implementation-plan.md` | nothing: `## Build plan` is not emitted at this variant |

## Grading window

```
VERDICT  PASS   (/Users/apple/Desktop/deku/Output/16sept-echarts/S_saasm_cont_charting-library-portal-vb_20260916_055255/instruction.md)
section        H2                chars  reference  flag
core_features  Core features     19627       2400  past-slice
user_flow      User flow          7190       1900  past-slice
ui_ux_notes    UI/UX notes       11680       1700  past-slice
constraints    Constraints        1423        800  over-reference
user_roles     User roles         1865       1000  over-reference
overview       Overview           1718        700  over-reference
joined total                     43503       8800  past-slice
first four                       39920       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```

`## Core features`, `## User flow` and `## UI/UX notes` all run past the judge's
2,500-char slice, as they do on the shipped `15sept-erpnext` bundle. G33 reports length
and fails nothing, and the judged criteria are self-contained: G52 now fails a criterion
that points at the brief instead of carrying its own facts. The tail reaches the agent in
full, which is what sets reward.

## Kit gate log

Rendered from `_handoff/S_saasm_cont_charting-library-portal-vb_20260916_055255.gates.jsonl`, one row per gate with the SHA-256 of every
input it examined. Not transcribed.

| Gate | Tool | Exit | Verdict | Inputs hashed |
|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 0 | PASS | 24 |
| G1/G12 | `layout_lint.py` | 0 | PASS | 24 |
| G46 | `structure_lint.py` | 0 | PASS | 24 |
| G50 | `docker_lint.py` | 0 | PASS | 24 |
| G55 | `runtime_deps_lint.py` | 0 | PASS | 24 |
| G63 | `secret_lint.py` | 0 | PASS | 24 |
| G48 | `truth_lint.py` | 0 | PASS | 24 |
| G51 | `source_lint.py` | 0 | PASS | 24 |
| G52 | `rubric_context_lint.py` | 0 | PASS | 24 |
| G54 | `comment_lint.py` | 0 | PASS | 24 |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | 24 |
| G11 | `leak_scan.py` | 0 | PASS | 24 |
| G33 | `window_lint.py` | 0 | PASS | 24 |
| G4/G5 | `contract_lint.py` | 0 | PASS | 24 |
| G43 | `prescription_lint.py` | 0 | PASS | 24 |
| G44 | `disclosure_lint.py` | 0 | PASS | 24 |
| G10 | `no_sdk_lint.py` | 0 | PASS | 24 |
| G31 | `determinism_lint.py` | 0 | PASS | 24 |
| G14 | `reward_path_lint.py` | 0 | PASS | 24 |
| G27/G30 | `rubric_lint.py` | 0 | PASS | 24 |
| G41 | `flag_lint.py` | 0 | PASS | 24 |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | 24 |
| G59/G60 | `codequality_lint.py` | 2 | ? | 24 |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | 24 |
| G6 | `fixture_lint.py` | 0 | PASS | 24 |
| G24 | `coverage_map.py` | 0 | PASS | 24 |
| G37 | `checklist_qc.py` | 0 | PASS | 24 |
| G39 | `rubric_align_lint.py` | 0 | PASS | 24 |
| G28/G29 | `channel_lint.py` | 0 | PASS | 24 |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | 24 |
| G0/INV5 | `vendor_check.py` | 0 | PASS | 24 |
| G47 | `output_qc.py` | 0 | PASS | 24 |

`G59/G60` exits 2, NOT-APPLICABLE: the bundle ships no `evaluation_target: "source"`
criterion, so there is no code-quality channel to check. `G40` exits 0 with a WARN
because `verifier` is `self` on a single-agent run, which the receipt records as
SELF-ATTESTED rather than as an independent verification.

## Certification receipts

Rendered from `_handoff/S_saasm_cont_charting-library-portal-vb_20260916_055255.receipts.json`. Each token is
`blake2b(prompt_bytes + task_code + gate)`, so a receipt is worthless in any other run.

| Gate | Prompt | Verdict | PASS | WARN | N/A | FAIL |
|---|---|---|---|---|---|---|
| G3 | `task_code_verifier.md` | VALID | 12 | 0 | 0 | 0 |
| G34 | `QC_spec.md` | PASS | 13 | 2 | 0 | 0 |
| G34 | `QC_instruction.md` | PASS | 21 | 3 | 0 | 0 |
| G35 | `qc_docker.md` | PASS | 83 | 5 | 17 | 0 |
| G36 | `qc_toml.md` | PASS | 111 | 1 | 8 | 0 |
| G37 | `qc_solution_checklist.md` | PASS | 0 | 0 | 0 | 0 |
| G53 | `qc_rubric.md` | PASS | 14 | 1 | 1 | 0 |

Five findings were raised by these reviews and fixed before the final sweep:

1. **qc_rubric RC-01/RC-04.** `C-CF-15` ("a leaf row in the tree reads the name followed
   by the default in a quieter tone") was assigned to a browser walkthrough, which cannot
   settle "a quieter tone", while R1's rule already graded it. Retargeted to R1.
2. **QC_instruction C2.** Two graders asserted status codes the brief never pinned. The
   withdrawn-snippet grader now requires its answer to differ from the unknown-address
   answer rather than to equal `410`; the rate-limit grader now requires a client error
   naming the wait rather than `429`.
3. **QC_instruction C3.** The brief pinned a drawn count of `240` point marks for
   `basic-line-smooth` against its own seven seeded values. Now `7`, one per category.
4. **QC_instruction D2.** "the elapsed milliseconds to exactly two decimal places and
   `ms`" left the spacing open to two readings. Now "and then `ms` with no space before
   it".
5. **QC_instruction D5.** The companion's Section 9.4 requires the narrow-screen
   reference tabs to reorder to Option, API, Tutorial, GL. The brief carried the strip
   without the reorder. Now carried, with a checklist item and R13's rule extended.

## Companion carry

| Measure | Value |
|---|---|
| source | `/Users/apple/Desktop/deku/Drive_PRDs/16_sept/echarts_prd.md`, 6,703 lines |
| colours described | 24 of 24, by family, tone and shade; zero hexes in the brief |
| topics carried | 406 of 406 |
| enumerated items carried | 1,106 of 1,106 |
| waivers | 82 tokens, recorded in `_handoff/S_saasm_cont_charting-library-portal-vb_20260916_055255.sources.json` |

The waivers fall in three groups: the companion's own authoring apparatus (its evidence,
capture and acceptance sections); design VALUES the A5 number rule forbids the brief to
carry (curves, keyframes, durations, rgb triples, class-name fingerprints, icon path
geometry); and the routes and services the Task Order does not scope. The one behavioural
departure is `registrable`: a distinct registrable playground origin is impossible on a
single-origin deployment, so rule 25 carries the enforceable half.

## Blocking findings

None for this bundle. Three kit contradictions were met and are reported rather than
worked around:

1. **`QC_instruction.md` A1/B3 vs `generate_instruction.md` 2.1.** A1 lists eleven H2s
   including `## Build plan`; 2.1 makes that section non-baseline and
   `spec_sections_given` omits `buildplan`. Resolved in favour of 2.1, recorded as a WARN
   on both checks.
2. **`qc_docker.md` CMP-011 vs CMP-022.** CMP-011 (High) bans a `ports:` key on any
   service; CMP-022 (Critical) requires `main` to set one. No sidecar publishes a port;
   `main` publishes `4173:4173`. Resolved in favour of the Critical check.
3. **`reference/C` C.2.1's minio image no longer resolves.** `registry-1.docker.io`
   answers 401 for `minio/minio:RELEASE.2024-10-13T13-34-11Z` with a valid pull token.
   The same tag resolves at `quay.io/minio/minio`, index digest
   `sha256:9535594ad4122b7a78c6632788a989b96d9199b483d3bd71a5ceae73a922cdfa`, and the
   compose file pins that. `reference/C` and `environment/providers/minio/` need the same
   repin.

One further contradiction is noted without a workaround: `QC_spec.md` S2 reads "3-6
must-have features" while `generate_instruction.md` Phase 1 sets the band at "3-6 (6-10
with a companion)". `01-PRD.md` carries nine, inside the governing band.

## Aligned to the 2026-09-16 pull

Five commits landed after the first green sweep. Each was read and the bundle was
re-aligned, then re-swept to 32/32 green.

| Commit | Change | What this bundle did |
|---|---|---|
| `1b99060` | `code_quality` becomes an authored code-quality dimension | nothing to change: the bundle carries no `evaluation_target: "source"` criterion, so G59/G60 stays NOT-APPLICABLE. The dimension is now available if a code-quality channel is wanted later |
| `da24d3b` | the section pytest module is renamed `test_output.py`; the generated compiled-rubric file becomes `test_ans.py` | the emitter writes `tests/test_output.py`, `workflows.yaml` addresses `test_output.py::<test>`, the pytest-provenance sidecar's `module` follows, `tests/Dockerfile` COPYs the new name, and the stale `tests/test_pytest.py` and `solution/trinity/test_output.py` were deleted rather than left beside their replacements |
| `11eaf7b` | `[verifier].environment_mode = "separate"` by default | switched. This retires the prerequisite the first handoff raised, that shared mode expects seven vendored grader files in an image built from `environment/Dockerfile` where `deku-verifier-base` is unused. Under separate mode `tests/Dockerfile` builds `FROM deku-verifier-base:0.2`, which carries them |
| `78e5ba6` | the vendored `test.sh` loses its whole-line comments and is re-pinned | re-vendored; 125 lines became 90 and `vendor_check` passes against the new manifest. Recorded above as a fork of the pin |
| `806eb0a` | `solution/USER_README.md` returns as a GENERATED file | `recompute.py` re-vendored at `truth-generator-7` and re-run; it now emits five artifacts and G12 checks the canary preamble in both `solution/TRUTH.md` and `solution/USER_README.md` |

## Corpus-level gates

| Gate | Verdict | Why |
|---|---|---|
| G42 `corpus_overlap` | NOT-APPLICABLE | needs two or more bundles to compare; this output root holds one |
| G49 `diversity_lint` | NOT-APPLICABLE | same reason; the `draw:` lines are recorded in `00-decisions.md` for the corpus-wide run |
| G61 `corpus_report` | ADVISORY | no bundle carries a difficulty yet, so the 0/10/30/40/20 mix cannot be read. Its G26 payments-or-email floor reads 0% over this one-bundle root; that floor is a whole-corpus target, not a per-run one, and this cell's profile carries no payments or email slot |
| G38 `kit_selftest` | PASS | 32 checks, once per kit revision |

## Budget

`turns_expected = 200`, `tokens_expected = 8000000`, the Standard tier. Nine graded
features over two backing services, 739 checklist items and 63 committed graders put this
at the top of the band: the agent has to extract a versioned schema, build two generated
document shells, run untrusted code inside a budget, compile a reproducible artifact and
hold an ownership boundary over an object store. The tier is not raised because 8,000,000
is the absolute ceiling `qc_toml.md` BENCH-004 allows.

## Exit

**MECHANICALLY-GREEN, NO-SOLUTION.** Not admissible. The bundle carries no reference app
(D20), so nothing in it has been compiled or run. It becomes admissible when the app
lands downstream from `solution/checklist.md` and `harbor run -a oracle` returns `1.0`
twice. `_handoff/S_saasm_cont_charting-library-portal-vb_20260916_055255.handoff.md` carries the seven gates the kit cannot run.
