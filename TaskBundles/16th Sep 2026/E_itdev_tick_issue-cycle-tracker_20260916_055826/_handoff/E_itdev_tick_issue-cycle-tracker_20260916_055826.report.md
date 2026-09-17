# Build report: E_itdev_tick_issue-cycle-tracker_20260916_055826

## Identity

- Task code: `E_itdev_tick_issue-cycle-tracker_20260916_055826`
- Task id: `deku/issue-cycle-tracker`
- Cell: enterprise / it-devtools / ticketing-queue
- Service profile: P2-db-email (slots: db, email)
- Providers per slot: db -> postgres (postgres:16.4-bookworm); email -> mailpit (axllent/mailpit:v1.30.6)
- Variant: a; variant_axes: []
- Language: python; stack (drawn): Flask + Jinja + HTMX (mpa-progressive)
- design_direction: companion (a full PRD was supplied)
- capability_flags: aesthetic, concurrency_hardening
- launch_surface (drawn): colour_contrast, mobile_viewport, no_frontend_secrets, page_view_log, security_headers
- spec_sections_given: overview, roles, features, flow, uiux, techrequirements, datamodel, constraints, contract
- Shard 1 of 1

## Source resolution

The Task Order named `it-service-management` / `pipeline-kanban`, neither of
which is in the kit's closed taxonomy. They resolve to `it-devtools` (the only
enterprise IT domain; an internal software-team issue tracker is a developer
tool) and `ticketing-queue`: issues are tickets, the unassigned inbox is the
queue, and the idea's climax ("assign an owner, and the assignee is notified")
maps one to one onto ticketing-queue's critical focus, "Assignment persisted AND
notification delivered". Enterprise + ticketing-queue is a legal cell
(P2/P6/P9); P2-db-email is the variant-a profile, so the notification is a real
email delivered to the assignee through Mailpit.

A companion PRD (the dark "Cadence" issue-tracker brief) was supplied, so
`design_direction = "companion"`: its measured palette (carried by role and by
family/tone/shade words, never as hex), its exact type families and sizes, its
two-speed eased motion, its sidebar/board layout and its accessibility floors are
carried into `## UI/UX notes`. G51 (`source_lint`) PASSES with every colour,
heading and enumerated item carried; the capture-methodology, decorative-effect,
component-inventory and acceptance-checklist sections of the PRD are declared
waivers (out of scope for the reframed product, or forbidden by the no-numbers
rule).

## Feature resolution

| Candidate | Verdict | Where | Reason |
|---|---|---|---|
| File issue with priority, label, estimate; server-allocated team key | INCLUDED | Core features, Data model | The product substrate; key allocated in-transaction (idea, PRD 17.3) |
| Inbox triage: lead reads unassigned inbox, assigns an owner | INCLUDED | Core features, User roles | The queue mechanic; lead/admin only |
| Assignment persists AND delivers exactly one notification email | INCLUDED | Core features | The critical focus; db + email slots, both observed |
| Cycle board of five named workflow states; move issue between states | INCLUDED | Core features, UI/UX notes | The idea's central gesture |
| State change writes one activity record atomically | INCLUDED | Core features, Data model | PRD 17.4; data integrity |
| Server-side authorization: member moves only owned issues; cross-team 404 | INCLUDED | User roles, Core features | PRD 17.5, the graded rule |
| At most one active cycle per team; close returns unfinished to inbox | INCLUDED | Core features, Technical requirements | PRD 17.1/17.6; concurrency single-winner |
| Idempotent create-issue replay; keys unique under contention | INCLUDED | Technical requirements | concurrency_hardening obligation |
| Launch surface: contrast, mobile viewport, no frontend secrets, page-view log, security headers | INCLUDED | UI/UX notes, Core features, Technical requirements | reference/O draw, each graded |
| Realtime multi-user board sync (Soketi) | EXCLUDED | - | PRD optimism+reconcile is async; ticketing-queue declares no realtime slot |
| Marketing routes, grain overlay, shine sweep, capture methodology | WAIVED | - | Out of scope for the reframed product (G51 waivers) |

## Gate log

All mechanical gates (batteries 1-2) PASS; rendered from
`E_itdev_tick_issue-cycle-tracker_20260916_055826.gates.jsonl` (one row per gate,
each carrying the SHA-256 of the bytes it examined). G59/G60 return NOT-APPLICABLE
(no source-target code-quality rubric shipped). Battery 3 (G13, G15, G18-G21,
G25) and the adversarial-LLM gates (G23, G34, G35, G36, G37b, G53) are declared,
not proven here.

## Honest exit state

`MECHANICALLY-GREEN, NO-SOLUTION`. `solution/` carries the checklist, the answer
key (trinity) and the loud-fail `solve.sh`; no reference app ships. The bundle is
not admissible until the app is generated downstream from `solution/checklist.md`
and `harbor run -a oracle` returns 1.0 twice.
