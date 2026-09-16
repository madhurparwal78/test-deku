# Build report - E_itdev_appr_multiplayer-canvas-workspace-vb_20260916_070512

## Identity

| | |
|---|---|
| task code | `E_itdev_appr_multiplayer-canvas-workspace-vb_20260916_070512` |
| task id | `deku/multiplayer-canvas-workspace-vb` |
| cell | enterprise / it-devtools / approval-workflow |
| archetype | `multiplayer-canvas-workspace` |
| variant | `b`, axes ["critical_depth", "spec_sections"] |
| service_profile | `P6-db-auth-email` |
| providers | backend `postgres`, auth `keycloak`, email `mailpit` |
| language | `python` |
| spec_sections_given | ["overview", "roles", "features", "flow", "uiux", "frontend", "techrequirements", "datamodel", "constraints", "contract"] |
| design_direction | `companion` |
| launch_surface | `custom_404,no_broken_links,single_cta,sitemap_robots,spam_protection` |
| authors | kaustubh.dalvi@ethara.ai (QL), ananya.tandon.int43@ethara.ai (contributor) |
| shard | 1 of 1 |
| kit | deku-green-field, kit self-test G38 PASS (32 checks) |
| grader pin | `0.22.0` |
| target schema | `1.4` |
| exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Task Order reconciliation

The supplied Task Order named `domain: it-service-management` and `pattern: collaborative-workspace`;
neither is in the taxonomy. `it-devtools` was taken for the domain. The pattern's literal
neighbour `collaboration-shared` is a D19 dead cell (no `realtime` provider), so
`approval-workflow` was minted, confirmed by the operator. The first mint landed in another
session's output root because that session rewrote `config/kit-config.yaml` concurrently; the
orphaned claim was released with `task_code.py release` and every later command pinned
`DEKU_OUTPUT_ROOT` to `Output/16sept_figma`.

## Feature resolution table

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Branching, review, version-bound approval, merge refusal | INCLUDED | Core features, first subsection | companion 1.5, 15.5, 17.4; the critical focus |
| Identity and the workspace shell | INCLUDED | Core features | companion 13, 19 |
| Projects, files and the frame canvas | INCLUDED | Core features | companion 14, 15 |
| Presence and live cursors | INCLUDED | Core features | companion 14.5 |
| Comments on a frame | INCLUDED | Core features | companion 17.1, 17.2 |
| Component libraries | INCLUDED | Core features | companion 16 |
| Organization admin console | INCLUDED | Core features | companion 18 |
| Audit stream | INCLUDED | Core features | companion 30 |
| Public overview, access form, not-found page | INCLUDED | Core features | drawn launch surface |
| Marketing site, mega menu, carousels, marquee, icons | DROPPED | G51 waiver | outside the Task Order's product |
| Billing, credits, processor reconciliation | DROPPED | G51 waiver | no payments slot |
| Object storage, media delivery, uploads | DROPPED | G51 waiver | no storage slot |
| Search indexing and ranking | DROPPED | G51 waiver | no search slot |
| Realtime coordinator, jobs, outbox, caching | DROPPED | G51 waiver | no realtime or queue slot |
| Extensions, callbacks, ingestion | DROPPED | G51 waiver | outside scope |

G51 carried 18/18 companion colours, 362/362 topics and 1541/1541 enumerated items, with
164 recorded waivers (`_handoff/E_itdev_appr_multiplayer-canvas-workspace-vb_20260916_070512.g51-waivers.json`).

## Slot obligation table

| Slot | Provider | Status | Observing test |
|---|---|---|---|
| backend | `postgres` | MET | `test_frame_move_is_persisted_and_survives_reload` (critical) |
| auth | `keycloak` | MET | `test_editor_is_denied_on_the_decision_endpoint` (critical) |
| email | `mailpit` | MET | `test_review_request_delivers_mail_to_the_reviewer` (critical) |

## Graders

| Measure | Value |
|---|---|
| workflows | 20 |
| browser substeps | 22 |
| pytest substeps | 48 |
| critical substeps | 6 |
| pytest categories | {'business_rule': 9, 'core_outcome': 2, 'data_integrity': 13, 'notification': 3, 'presentation': 3, 'security': 12, 'validation': 6} |
| non-happy-path workflow ids | 11: invalid_frame_parent_is_rejected, concurrent_frame_inserts_keep_both, comment_edit_from_another_member_is_forbidden, library_publish_with_an_invalid_component_is_rejected, merge_after_a_later_push_is_denied, editor_cannot_approve_or_merge, unauthenticated_and_cross_team_requests_are_forbidden, duplicate_invitation_creates_no_second_row, review_request_with_an_empty_reviewer_is_invalid, access_request_with_an_invalid_decoy_is_rejected, repeated_sign_in_failures_reach_the_limit |
| test module | `tests/test_output.py`, 48 tests, sections: core features, authorization, data integrity, edge cases, email |

## Rubric

16 judged criteria: 14 positive, 2 negative; positive points 32.

| Dimension | Share | Weight |
|---|---|---|
| instruction_following | 0.344 | 0.30 |
| functionality | 0.250 | 0.25 |
| ux_flow | 0.156 | 0.15 |
| ui_visual | 0.156 | 0.15 |
| motion | 0.031 | 0.05 |
| accessibility | 0.031 | 0.05 |
| responsiveness | 0.031 | 0.05 |

## Checklist

167 graded items across 10 sections; tags {'capability': 18, 'role': 16, 'contract': 37, 'literal': 13, 'constraint': 22, 'ui': 42, 'data': 19}.
49 obligations the brief states are recorded under Declared but ungraded, each with a
reason (OPEN-DECISIONS D-H). Adjudicated report: `_handoff/E_itdev_appr_multiplayer-canvas-workspace-vb_20260916_070512.checklist-qc.md`.

## Literals Ledger

186 values; by class {'account': 5, 'count': 11, 'credential': 1, 'env': 11, 'literal': 40, 'route': 39, 'seed': 15, 'status': 64}. Carriers are
`instruction.md`, `tests/conftest.py` and `tests/test_output.py`; three verifier-only values
(`DB_ADMIN_URL`, `AUTH_ADMIN_TOKEN`, `EMAIL_INBOX_API_URL`) appear in no agent-visible file.

## Spec documents

`_spec/E_itdev_appr_multiplayer-canvas-workspace-vb_20260916_070512/`: 00-decisions (Task Order reconciliation, draws, companion carry table) fed
every section; 01-PRD fed Overview, Core features, Constraints; 02-TRD fed Technical requirements;
03-app-flow fed User flow and the API shapes; 04-uiux-brief fed UI/UX notes and Front-end
specification; 05-backend-schema fed Data model and User roles; 06-implementation-plan is
withheld from the brief at this variant.

## Grading window

```
VERDICT  PASS   (C:/Users/Admin/Desktop/Deku/Output/16sept_figma/E_itdev_appr_multiplayer-canvas-workspace-vb_20260916_070512/instruction.md)
section        H2                chars  reference  flag
core_features  Core features     18062       2400  past-slice
user_flow      User flow          4834       1900  past-slice
ui_ux_notes    UI/UX notes        9703       1700  past-slice
constraints    Constraints        1423        800  over-reference
user_roles     User roles         5191       1000  past-slice
overview       Overview           1456        700  over-reference
joined total                     40669       8800  past-slice
first four                       34022       7100  over-reference
length is reported, never failed -- the brief has no limit; `past-slice` marks prose the judge will not read
```

The approval spine is the first Core features subsection, so it sits inside the judge's slice.

## Kit gate log

Rendered from `_handoff/E_itdev_appr_multiplayer-canvas-workspace-vb_20260916_070512.gates.jsonl`; one receipt per gate with the SHA-256 of every input.

| Gate | Tool | Exit | Verdict | argv sha | inputs hashed |
|---|---|---|---|---|---|
| G2/G16 | `validate_task.py` | 2 | NOT-APPLICABLE | 82ff5f5c75db284a | 25 |
| G1/G12 | `layout_lint.py` | 0 | PASS | 34f83994beb4b69d | 25 |
| G46 | `structure_lint.py` | 0 | PASS | 34f83994beb4b69d | 25 |
| G50 | `docker_lint.py` | 0 | PASS | 34f83994beb4b69d | 25 |
| G55 | `runtime_deps_lint.py` | 0 | PASS | 34f83994beb4b69d | 25 |
| G63 | `secret_lint.py` | 0 | PASS | 34f83994beb4b69d | 25 |
| G48 | `truth_lint.py` | 0 | PASS | 34f83994beb4b69d | 25 |
| G51 | `source_lint.py` | 0 | PASS | a0a1a064465607ec | 25 |
| G52 | `rubric_context_lint.py` | 0 | PASS | 34f83994beb4b69d | 25 |
| G54 | `comment_lint.py` | 0 | PASS | 34f83994beb4b69d | 25 |
| G17 | `secret_hygiene_lint.py` | 0 | PASS | 82ff5f5c75db284a | 25 |
| G11 | `leak_scan.py` | 0 | PASS | 4f484eee06835169 | 25 |
| G33 | `window_lint.py` | 0 | PASS | 4f484eee06835169 | 25 |
| G4/G5 | `contract_lint.py` | 0 | PASS | b939f56660c24870 | 25 |
| G43 | `prescription_lint.py` | 0 | PASS | 4f484eee06835169 | 25 |
| G44 | `disclosure_lint.py` | 0 | PASS | 4f484eee06835169 | 25 |
| G10 | `no_sdk_lint.py` | 0 | PASS | 5596b7ab4ef93de0 | 25 |
| G31 | `determinism_lint.py` | 0 | PASS | 5596b7ab4ef93de0 | 25 |
| G14 | `reward_path_lint.py` | 0 | PASS | 22cda5e026cef898 | 25 |
| G27/G30 | `rubric_lint.py` | 0 | PASS | 03f1e6e39ea2e22b | 25 |
| G41 | `flag_lint.py` | 0 | PASS | 34f83994beb4b69d | 25 |
| G56/G57/G58 | `if_lint.py` | 0 | PASS | 34f83994beb4b69d | 25 |
| G59/G60 | `codequality_lint.py` | 2 | ? | 34f83994beb4b69d | 25 |
| G7/G8/G9/G32/G45 | `workflow_lint.py` | 0 | PASS | f87edc5902035427 | 25 |
| G6 | `fixture_lint.py` | 0 | PASS | 1bdbb3a82337b570 | 25 |
| G24 | `coverage_map.py` | 0 | PASS | 543ff2367a428507 | 25 |
| G37 | `checklist_qc.py` | 0 | PASS | 49ff3381826561c1 | 25 |
| G39 | `rubric_align_lint.py` | 0 | PASS | 856b4a91c2083d24 | 25 |
| G28/G29 | `channel_lint.py` | 0 | PASS | 98475e55cff7d359 | 25 |
| G40 | `prompt_receipt_lint.py` | 0 | WARN | 68774a443ae1dcd2 | 25 |
| G0/INV5 | `vendor_check.py` | 0 | PASS | 0db625396f5c0e08 | 25 |
| G47 | `output_qc.py` | 0 | PASS | 2f65984639b08465 | 25 |

Corpus-level, run once over `Output/16sept_figma`: G42 corpus_overlap NOT-APPLICABLE and G49
diversity_lint NOT-APPLICABLE (one bundle in this root), G61 corpus_report NOT-APPLICABLE (no
admissible bundle yet). G38 kit_selftest PASS.

## Certification prompt receipts (G40)

| Prompt | Gate | Verdict | Checks answered | WARN | Verifier | Cycle notes |
|---|---|---|---|---|---|---|
| `QC_instruction.md` | G34 | PASS | 24 | 7 | self | 3 |
| `QC_spec.md` | G34 | PASS | 15 | 2 | self | 3 |
| `qc_docker.md` | G35 | PASS | 105 | 1 | self | 4 |
| `qc_rubric.md` | G53 | PASS | 16 | 0 | self | 3 |
| `qc_solution_checklist.md` | G37 | PASS | 0 | 0 | self | 3 |
| `qc_toml.md` | G36 | PASS | 120 | 1 | self | 6 |
| `task_code_verifier.md` | G3 | VALID | 12 | 0 | self | 1 |

Every certification verdict is SELF-ATTESTED: the same agent authored and reviewed. The cycle
history in `_handoff/E_itdev_appr_multiplayer-canvas-workspace-vb_20260916_070512.receipts.json` records what each review found and what was repaired.

## Handoff gate list (undecided)

| Gate | Command | Expected |
|---|---|---|
| G13 | `docker build -f environment/Dockerfile environment` | exit 0 on linux/amd64 and linux/arm64 |
| G13 | `docker build -f tests/Dockerfile tests` | exit 0 |
| G15 | `docker compose -f environment/docker-compose.yaml up --wait` with a scrubbed env | postgres, keycloak and mailpit healthy |
| G19 | `harbor run -p <task> -a oracle`, twice | reward 1.0 both times |
| G18 | read `deployed` from either oracle run | 1.0 |
| G20 | `harbor run -p <task> -a nop` | reward 0.0 |
| G21 | fake-integration patch, then oracle | reward below 1.0 |
| G25 | reviewer exploit sweep, reference/F | 0 of 11 succeed |

## Blocking findings

1. `[delivery]` is absent from `task.toml`: its image digests must come from a real
   `docker build`, the kit has no Docker access, and a fabricated digest is forbidden. Add it
   after G13 (G2 reports NOT-APPLICABLE until then).
2. No reference application exists; nothing in this bundle has been compiled or run.

## Budget estimate

`turns_expected = 200`, `tokens_expected = 8000000`: eight
features plus four launch obligations across two runtimes, an external identity provider and
real SMTP put this at the expert band; tokens sit at the corpus ceiling of 8,000,000.

## Exit state

**MECHANICALLY-GREEN, NO-SOLUTION.** Not admissible until the application is built downstream
from `solution/checklist.md` and `harbor run -a oracle` returns 1.0 twice.
