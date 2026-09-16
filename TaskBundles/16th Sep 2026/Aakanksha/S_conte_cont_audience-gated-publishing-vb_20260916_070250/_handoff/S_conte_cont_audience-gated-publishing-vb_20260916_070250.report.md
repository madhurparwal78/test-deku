# Build report: audience-gated-publishing (Foldline)

TASK CODE        S_conte_cont_audience-gated-publishing-vb_20260916_070250
TASK ID          deku/audience-gated-publishing-vb
CELL             solo_founder / content-publishing / content-publishing
SERVICE PROFILE  P4-db-storage
PROVIDERS        backend = postgres, storage = minio
VARIANT          b   (variant_axes: critical_depth, spec_sections; a companion PRD was supplied)
LANGUAGE         typescript
SPEC SECTIONS    overview, roles, features, flow, uiux, techrequirements, datamodel, buildplan, contract
CAPABILITY FLAGS concurrency_hardening, data_scale   (aesthetic injected always-on; design_direction = companion)
LAUNCH SURFACE   alt_text, no_broken_links, privacy_page, sitemap_robots, social_preview
SHARD            1 of 1

## Exit state

MECHANICALLY-GREEN, NO-SOLUTION. Not admissible until the app is generated downstream from
solution/checklist.md and `harbor run -a oracle` returns 1.0 twice.

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| Posts and composer with a free-word gate | INCLUDED | Core features, posts table | the writing spine |
| Audience field: move the gate, live projection of reach and revenue | INCLUDED | Core features, /field/{id} | the distinctive central interaction (EXT-1), scoped to a data-driven surface |
| Minimum-cohort projection refusal | INCLUDED | Core features, test_projection_refuses_below_min_cohort | the source PRD refuses below a minimum cohort |
| Gated audio edition as a protected object | INCLUDED | storage slot, test_gated_edition_* | content-publishing critical focus: object in store, protected content not readable |
| Tiers, discount offer, subscribe | INCLUDED | Core features, subscriptions | readers pay the writer |
| Idempotent subscribe under contention | INCLUDED | concurrency_hardening, test_concurrent_* | the money must stay honest under simultaneous requests |
| Double-entry ledger, balanced per transaction | INCLUDED | data model, test_ledger_* | the source PRD books revenue into a balanced ledger |
| Newsletter release as delivery records | INCLUDED | Core features, test_release_* | one delivery per recipient, no duplicates |
| Paginated audience/posts/ledger | INCLUDED | data_scale, test_posts_pagination_cursor | the audience is tens of thousands of rows |
| WebGL2 particle compositor | DROPPED | Constraints | not gradeable in a container; the field ships as a data-driven surface |
| CRDT collaborative composition (EXT-2) | DROPPED | Constraints | out of scope for a single-writer P4-db-storage build |
| Deliverability reputation and warmup (EXT-4) | DROPPED | Constraints | needs a real mail provider, out of the closed world |
| Dunning, custom domains, TLS, plan billing | DROPPED | Constraints | no real payment or certificate provider in the environment |

## Slot obligations

| Slot | Provider | Status | Evidence |
|---|---|---|---|
| backend | postgres | MET | test_ledger_reconciles_debits_equal_credits, test_seed_is_idempotent (data_integrity) |
| storage | minio | MET | test_publish_stores_one_audio_object (critical), test_gated_edition_denied_to_free_reader (critical) |

## Workflows and tests

- Workflows: 14 (solo_founder band 10-16). Browser substeps: 14. Pytest substeps: 31. Critical substeps: 6.
- Non-happy-path ids: gate_rejects_invalid_tier, paywall_forbidden_to_free_reader,
  concurrent_duplicate_subscribe_single, reader_forbidden_and_unauthenticated_denied,
  newsletter_release_no_duplicate_delivery, signup_duplicate_and_short_password.
- One pytest module: tests/test_output.py (31 tests). Sections observed: core features, data
  integrity, tiers/subscriptions, storage, authorization, data scale, presentation.

## Rubric

- 11 judged criteria (tests/rubric.json), all positive. Dimensions: instruction_following 2,
  functionality 2, ux_flow 2, ui_visual 2, motion 1, accessibility 1, responsiveness 1.
- Runtime-inert until run_rubric.py gains --rubric (D17); spec obligations enforced statically.

## Literals ledger

| Class | Value | Carriers |
|---|---|---|
| credential | deku-demo-pw-2026 | instruction.md, conftest.py |
| account | author@example.com, reader@example.com, reader2@example.com | instruction.md, conftest.py |
| number | 800, 600 | instruction.md, conftest.py |
| code | WELCOME25 | instruction.md, conftest.py |
| tier | premium | instruction.md, conftest.py |
| scheme | editions/ | instruction.md, conftest.py |
| env_var (verifier-only) | DB_ADMIN_URL | task.toml |

## Spec docs emitted

- _spec/.../00-decisions.md  -- residual judgment calls and the deterministic draws
- _spec/.../01-PRD.md        -- the condensed companion the brief is derived from (G51 source)

## KIT GATE LOG (rendered from gates.jsonl, never transcribed)

```
G2/G16    validate_task.py        exit=0 PASS      G43       prescription_lint.py    exit=0 PASS
G1/G12    layout_lint.py          exit=0 PASS      G44       disclosure_lint.py      exit=0 PASS
G46       structure_lint.py       exit=0 PASS      G10       no_sdk_lint.py          exit=0 PASS
G50       docker_lint.py          exit=0 PASS      G31       determinism_lint.py     exit=0 PASS
G55       runtime_deps_lint.py    exit=0 PASS      G14       reward_path_lint.py     exit=0 PASS
G63       secret_lint.py          exit=0 PASS      G27/G30   rubric_lint.py          exit=0 PASS
G48       truth_lint.py           exit=0 PASS      G41       flag_lint.py            exit=0 PASS
G51       source_lint.py          exit=0 PASS      G56/57/58 if_lint.py              exit=0 PASS
G52       rubric_context_lint.py  exit=0 PASS      G59/G60   codequality_lint.py     exit=2 N/A
G54       comment_lint.py         exit=0 PASS      G7/8/9/32/45 workflow_lint.py     exit=0 PASS
G17       secret_hygiene_lint.py  exit=0 PASS      G6        fixture_lint.py         exit=0 PASS
G11       leak_scan.py            exit=0 PASS      G24       coverage_map.py         exit=0 PASS
G33       window_lint.py          exit=0 PASS      G37       checklist_qc.py         exit=0 PASS
G4/G5     contract_lint.py        exit=0 PASS      G39       rubric_align_lint.py    exit=0 PASS
G28/G29   channel_lint.py         exit=0 PASS      G40       prompt_receipt_lint.py  exit=0 PASS
G0/INV5   vendor_check.py         exit=0 PASS      G47       output_qc.py            exit=0 PASS
```

Adversarial QC (self-attested, temp 0): G34 QC_instruction PASS, G34 QC_spec PASS,
G35 qc_docker PASS, G36 qc_toml PASS, G37 qc_solution_checklist PASS, G53 qc_rubric PASS,
G3 task_code_verifier VALID. Receipts in _handoff/*.receipts.json.

G59/G60 exit 2 = NOT-APPLICABLE: no code-quality (source) rubric is authored, which is optional.

## Handoff gates (undecided here, see the handoff contract)

G13, G15, G18, G19, G20, G21, G25 are handoff-owned; the kit cannot run them. Commands and
expected verdicts are in S_conte_cont_audience-gated-publishing-vb_20260916_070250.handoff.md.

## Blocking findings

NONE.

## Versions

Kit 806eb0a; vendored grader pin 0.22.0; target schema 1.4.

## Estimate

turns_expected ~ 90-140; tokens_expected high. Reasoning: two services (postgres + minio), a
protected-object paywall, an idempotent subscribe with a balanced double-entry ledger, a
computed-on-read projection with a cohort floor, cursor pagination, and a launch-surface set
(privacy, sitemap, social preview, alt text, internal links) each with its own grader.
