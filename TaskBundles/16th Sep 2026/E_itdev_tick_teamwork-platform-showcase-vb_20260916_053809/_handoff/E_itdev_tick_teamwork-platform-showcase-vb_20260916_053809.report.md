# Build report: E_itdev_tick_teamwork-platform-showcase-vb_20260916_053809

| | |
|---|---|
| Task code | `E_itdev_tick_teamwork-platform-showcase-vb_20260916_053809` |
| Task id | `deku/teamwork-platform-showcase-vb` |
| Cell | enterprise / it-devtools / ticketing-queue |
| Service profile | `P2-db-email` |
| Providers | `backend` = `postgres`, `email` = `mailpit` |
| Variant | `b`, axes `critical_depth`, `spec_sections` |
| Language | `python` |
| Spec sections given | overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract |
| Shard | 1 of 1 |
| Companion document | `atlassian_prd.md` |
| Exit state | **MECHANICALLY-GREEN, NO-SOLUTION** |

## Derived-design draws

Every axis is drawn by SHA-256 over the archetype `teamwork-platform-showcase`.

| Axis | Value |
|---|---|
| `render_model` | `spa-json-api` |
| `backend` | `Flask` |
| `frontend` | `React + Vite` |
| `nav` | `breadcrumbed-drill-down` |
| `work_surface` | `split detail-pane` |
| `create_flow` | `modal` |
| `feedback` | `optimistic-row` |
| `design_direction` | `companion` (reference/L L.6.1; the bank draw `brutalist-utility` is recorded, not applied) |
| `launch_surface` | `favicon,page_view_log,single_cta,social_preview,terms_page` |

## Feature resolution

| Feature | Verdict | Where |
|---|---|---|
| The marketing estate, sixteen routes, three chromes | INCLUDED | Core features, User flow, Front-end specification |
| The scroll-pinned home journey | INCLUDED | Front-end specification |
| The graduated pricing calculator | INCLUDED | Core features rules 43 to 47 |
| The faceted template catalogue | INCLUDED | Core features rules 48, 49 |
| Signup with three domain outcomes | INCLUDED | Core features rule 39 |
| The board, the transition, the history | INCLUDED | Core features rules 1 to 11 |
| Automation rules bound to transitions | INCLUDED | Core features rules 12 to 19 |
| The query language and saved filters | INCLUDED | Core features rules 31 to 38 |
| Per-item visibility and the aggregate rule | INCLUDED | Core features rules 24 to 30 |
| The append-only item history | INCLUDED | Data model |
| Real-time collaborative editing | DROPPED | no realtime provider exists in the environment; recorded in Constraints, waived to G51 |
| Search index, metrics store, app sandbox, billing | DROPPED | not observable in a single-container app; recorded in Constraints, waived to G51 |
| Residency, erasure, sharding, tracing | DROPPED | infrastructure the bundle cannot exhibit; recorded in Constraints, waived to G51 |

## Slot obligations

| Slot | Provider | Critical pytest substep | Verdict |
|---|---|---|---|
| `backend` | `postgres` | `test_transition_persists_across_reread` | MET |
| `email` | `mailpit` | `test_assignee_change_delivers_confirmation_email` | MET |

## Grading surface

| | |
|---|---|
| Checklist items | 133 |
| Workflows | 22 (enterprise band 13 to 23) |
| Browser substeps | 90 |
| Pytest substeps | 27 |
| Critical substeps | 7 |
| Non-happy-path workflow ids | 6 |
| Pytest module | `tests/test_output.py`, 27 test functions |
| Rubric criteria | 18 (16 positive, 2 negative) |
| Core asks traced | 57, all fully graded |

### Rubric dimension budget

| Dimension | Target | Actual share | Criteria |
|---|---|---|---|
| `instruction_following` | 0.30 | 0.310 | 3 |
| `functionality` | 0.25 | 0.262 | 3 |
| `ux_flow` | 0.15 | 0.143 | 2 |
| `ui_visual` | 0.15 | 0.143 | 2 |
| `motion` | 0.05 | 0.048 | 2 |
| `accessibility` | 0.05 | 0.048 | 2 |
| `responsiveness` | 0.05 | 0.048 | 2 |

## Grading window

Reported, never failed. The Task Order supplied a companion specification and the
brief carries it whole, so the six judged sections run past the judge's slice.
The tail reaches the agent complete, and `judge_score` never touches reward.

| Section | Characters |
|---|---|
| Core features | 19728 |
| User flow | 5335 |
| UI/UX notes | 7955 |
| Constraints | 1120 |
| User roles | 2337 |
| Overview | 2139 |

## Literals ledger

| Value | Class | Verifier only | Carriers |
|---|---|---|---|
| `deku-demo-pw-2026` | credential | no | instruction.md, conftest.py |
| `admin@example.com` | account | no | instruction.md, conftest.py |
| `member@example.com` | account | no | instruction.md, conftest.py |
| `member2@example.com` | account | no | instruction.md, conftest.py |
| `requester@example.com` | account | no | instruction.md, conftest.py |
| `requester2@example.com` | account | no | instruction.md, conftest.py |
| `requester` | status | no | instruction.md, conftest.py, test_pytest.py |
| `member` | status | no | instruction.md, conftest.py, test_pytest.py |
| `admin` | status | no | instruction.md, conftest.py, test_pytest.py |
| `FIN` | seed_record | no | instruction.md, conftest.py, test_pytest.py |
| `MKT` | seed_record | no | instruction.md, conftest.py, test_pytest.py |
| `SUP` | seed_record | no | instruction.md, conftest.py |
| `Banking Portal` | seed_record | no | instruction.md |
| `Campaign Refresh` | seed_record | no | instruction.md |
| `Service Desk` | seed_record | no | instruction.md |
| `Blocked` | status | no | instruction.md, conftest.py |
| `In progress` | status | no | instruction.md, conftest.py |
| `Ready for review` | status | no | instruction.md, conftest.py |
| `Done` | status | no | instruction.md, conftest.py |
| `To do` | status | no | instruction.md |
| `to_do` | status | no | instruction.md, conftest.py |
| `in_progress` | status | no | instruction.md, conftest.py |
| `done` | status | no | instruction.md, conftest.py |
| `FIN-2` | seed_record | no | instruction.md, conftest.py |
| `Validate transaction UX` | seed_record | no | instruction.md, conftest.py |
| `Send to review` | seed_record | no | instruction.md, conftest.py |
| `Assign review to the project lead` | seed_record | no | instruction.md, conftest.py |
| `My open work` | seed_record | no | instruction.md, conftest.py |
| `assignee = currentUser() AND status != Done ORDER BY rank ASC` | scheme | no | instruction.md, conftest.py |
| `Northwind work update:` | scheme | no | instruction.md, conftest.py |
| `Northwind work update: FIN-2 Validate transaction UX` | scheme | no | instruction.md, conftest.py |
| `204900` | number | no | instruction.md, conftest.py |
| `683` | number | no | instruction.md, conftest.py |
| `5950` | number | no | instruction.md, conftest.py |
| `850` | number | no | instruction.md, conftest.py |
| `411800` | number | no | instruction.md, conftest.py |
| `1373` | number | no | instruction.md, conftest.py |
| `Not available above 10 users` | scheme | no | instruction.md, conftest.py |
| `SAVE UP TO 17%` | scheme | no | instruction.md, conftest.py |
| `Billed annually.` | scheme | no | instruction.md |
| `100` | number | no | instruction.md, conftest.py |
| `1700` | number | no | instruction.md, conftest.py |
| `1000` | number | no | instruction.md, conftest.py |
| `/api/auth/login` | endpoint | no | instruction.md |
| `/api/health` | endpoint | no | instruction.md |
| `/api/items` | endpoint | no | instruction.md |
| `/api/projects` | endpoint | no | instruction.md |
| `/api/filters` | endpoint | no | instruction.md |
| `/api/page-views` | endpoint | no | instruction.md |
| `/api/plans` | endpoint | no | instruction.md |
| `/api/signup` | endpoint | no | instruction.md |
| `access_token` | endpoint | no | instruction.md, test_pytest.py |
| `/login` | route | no | instruction.md, test_pytest.py |
| `/app/projects` | route | no | instruction.md |
| `/templates` | route | no | instruction.md, conftest.py, test_pytest.py |
| `/customers` | route | no | instruction.md, conftest.py |
| `/enterprise` | route | no | instruction.md, conftest.py |
| `/terms` | route | no | instruction.md, conftest.py, test_pytest.py |
| `/products/work/pricing` | route | no | instruction.md, conftest.py, test_pytest.py |
| `DATABASE_URL` | env_var | no | instruction.md |
| `SMTP_HOST` | env_var | no | instruction.md |
| `SMTP_PORT` | env_var | no | instruction.md |
| `SMTP_USER` | env_var | no | instruction.md |
| `SMTP_PASS` | env_var | no | instruction.md |
| `APP_PUBLIC_URL` | env_var | no | instruction.md |
| `APP_PUBLIC_PORT` | env_var | no | instruction.md |
| `DB_ADMIN_URL` | env_var | yes | task.toml |
| `EMAIL_INBOX_API_URL` | env_var | yes | task.toml |
| `4.5:1` | number | no | instruction.md |
| `3:1` | number | no | instruction.md |
| `44px` | number | no | instruction.md |
| `653` | number | no | instruction.md |
| `Northwind Sans` | design_phrase | no | instruction.md |
| `Northwind Mono` | design_phrase | no | instruction.md |
| `near-white neutral` | design_phrase | no | instruction.md |
| `mid, vivid blue` | design_phrase | no | instruction.md |
| `deep, soft lime` | design_phrase | no | instruction.md |
| `light, vivid amber` | design_phrase | no | instruction.md |
| `split detail pane` | design_phrase | no | instruction.md |
| `rise a short distance` | motion_moment | no | instruction.md |
| `creep the last part` | motion_moment | no | instruction.md |
| `lurches forward` | motion_moment | no | instruction.md |
| `springs a little past its size` | motion_moment | no | instruction.md |

## Spec folder

Written to `Output/_spec/E_itdev_tick_teamwork-platform-showcase-vb_20260916_053809/`, never inside the bundle (CON-5).

| Doc | Feeds |
|---|---|
| `00-decisions.md` | the audit trail, the draws, the companion carry table |
| `01-PRD.md` | Overview, Core features, Constraints |
| `02-TRD.md` | Technical requirements |
| `03-app-flow.md` | User flow |
| `04-uiux-brief.md` | UI/UX notes |
| `05-backend-schema.md` | Data model, User roles |
| `06-implementation-plan.md` | authoring reference only; Build plan is not emitted at baseline |

## Generated answer key

Regenerated by the vendored `solution/trinity/recompute.py` from
`solution/trinity/grounding.yaml`. Nothing below is hand-written.

| File | What it is |
|---|---|
| `solution/TRUTH.md` | the golden trajectory, the rejected routes, the pinned literals, the canary |
| `solution/USER_README.md` | the seeded logins plus the canary the harness greps for by filename |
| `solution/trinity/rubrics.json` | the reference rubric |
| `solution/trinity/test_ans.py` | the compiled rubric tests |
| `tests/rubric.json` | the judged criteria the runtime judge reads |

## Kit gate log

Rendered from `_handoff/E_itdev_tick_teamwork-platform-showcase-vb_20260916_053809.gates.jsonl`. No verdict in this table was typed by
hand.

| Gate | Tool | Verdict | Exit | Result |
|---|---|---|---|---|
| `G2/G16` | `validate_task.py` | `PASS` | 0 | ok |
| `G1/G12` | `layout_lint.py` | `PASS` | 0 | ok |
| `G46` | `structure_lint.py` | `PASS` | 0 | ok |
| `G50` | `docker_lint.py` | `PASS` | 0 | ok |
| `G55` | `runtime_deps_lint.py` | `PASS` | 0 | ok |
| `G63` | `secret_lint.py` | `PASS` | 0 | ok |
| `G48` | `truth_lint.py` | `PASS` | 0 | ok |
| `G51` | `source_lint.py` | `PASS` | 0 | ok |
| `G52` | `rubric_context_lint.py` | `PASS` | 0 | ok |
| `G54` | `comment_lint.py` | `PASS` | 0 | ok |
| `G17` | `secret_hygiene_lint.py` | `PASS` | 0 | ok |
| `G11` | `leak_scan.py` | `PASS` | 0 | ok |
| `G33` | `window_lint.py` | `PASS` | 0 | ok |
| `G4/G5` | `contract_lint.py` | `PASS` | 0 | ok |
| `G43` | `prescription_lint.py` | `PASS` | 0 | ok |
| `G44` | `disclosure_lint.py` | `PASS` | 0 | ok |
| `G10` | `no_sdk_lint.py` | `PASS` | 0 | ok |
| `G31` | `determinism_lint.py` | `PASS` | 0 | ok |
| `G14` | `reward_path_lint.py` | `PASS` | 0 | ok |
| `G27/G30` | `rubric_lint.py` | `PASS` | 0 | ok |
| `G41` | `flag_lint.py` | `PASS` | 0 | ok |
| `G56/G57/G58` | `if_lint.py` | `PASS` | 0 | ok |
| `G59/G60` | `codequality_lint.py` | `?` | 2 | ok |
| `G7/G8/G9/G32/G45` | `workflow_lint.py` | `WARN` | 0 | ok |
| `G6` | `fixture_lint.py` | `PASS` | 0 | ok |
| `G24` | `coverage_map.py` | `PASS` | 0 | ok |
| `G37` | `checklist_qc.py` | `PASS` | 0 | ok |
| `G39` | `rubric_align_lint.py` | `PASS` | 0 | ok |
| `G28/G29` | `channel_lint.py` | `PASS` | 0 | ok |
| `G40` | `prompt_receipt_lint.py` | `WARN` | 0 | ok |
| `G0/INV5` | `vendor_check.py` | `PASS` | 0 | ok |
| `G47` | `output_qc.py` | `PASS` | 0 | ok |

## Blocking findings

None. Two advisory notes stand, both recorded rather than resolved:

- G45 reports a browser-to-pytest substep ratio of 90:27. The gate is
  advisory until its thresholds are signed off (ISSUES D-8). The ratio is high
  because the companion specifies a sixteen-route visual estate whose obligations
  are observed by a browser walk rather than by an HTTP assertion.
- G40 records every certification prompt as SELF-ATTESTED: one agent authored the
  bundle and ran the QC prompts over it. The kit's rule is owner not equal to
  verifier, so these are recorded verdicts rather than independent ones.

## Versions

| | |
|---|---|
| Kit | `deku-green-field` |
| Grader pin | `0.22.0` |
| Target schema | `1.4` |
| Verifier mode | `shared` |
| Judge pin | `claude-sonnet-4-6` |
| Canary | present in `solution/TRUTH.md` |

## Budget

`turns_expected = 200`, `tokens_expected = 8000000`. Ten graded must-have
features across a sixteen-route estate plus a signed-in console is materially
larger than a bare Task Order, so the budget sits at the top of the documented
band rather than in the middle of it.

## Exit state

**MECHANICALLY-GREEN, NO-SOLUTION.** Not admissible. The bundle carries no
reference app; nothing in it has been compiled or run.
