# Checklist QC report

---

## VERDICT: NEEDS REVIEW

Four window-section asks that no outside request can observe remain declared ungraded, and the unbudgeted companion depth was not decomposed item by item. Start with Unresolved.

---

| | |
|---|---|
| Instruction | instruction.md |
| Checklist | solution/checklist.md |
| Adjudicated | yes |
| Machine verdict before adjudication | PASS |

## Summary

The audit read instruction.md first, then solution/checklist.md, then the machine report from checklist_qc.py. The reading covered every sentence of Overview, User roles, Core features, User flow, UI/UX notes, Constraints, Deployment contract and Definition of done, and the HTTP contract tables in Technical requirements. The Technical requirements prose and the Front-end specification carry the companion product requirements in full and were read for contradictions, not decomposed into items one sentence at a time.

The machine layer passed structure, ids, citations and ledger arithmetic. Adjudication found eight asks in the window sections with no item or a partial item, all closed before this report: the Entry rule in User flow, the completed-move half of Core features rule 2, the eligibility clause of rule 5, the spotter and dispatcher rows of the role table, the customer half of the portal identity sentence, the console rail in UI/UX notes, and twelve UI/UX asks added when the section gained its missing palette, shape, component and access axes. A second pass added the closed-signup rule and the security administrator and analyst role cells, both now pinned in the brief and graded, and a replayed contact submission. The checklist now holds 177 items.

Four window-section asks stay without an item because the brief pins no observable a separately running grader can reach. They are declared ungraded in the checklist ledger and listed under Unresolved. A reader should decide whether each needs a pinned observable in the brief or stays declared.

## Findings requiring action

None open. Every confirmed gap below was closed by adding an item and a grading channel.

## Findings the checker raised and the audit overturned

- Machine segmentation proposed 1 obligation-bearing sentence each for Overview, User roles, Core features, User flow and UI/UX notes. Overturned: the segmenter treats a numbered list, a table or a wrapped paragraph as one unit. The ledger counts, recomputed by reading, are Overview 2, User roles 7, Core features 31, User flow 10, UI/UX notes 24.
- Machine proposed 130 obligation sentences in Technical requirements against 78 items, 46 in Front-end specification against 14, 9 in Data model against 3 and 6 in Deployment contract against 3. Not overturned and not confirmed as gaps: the balance is the carried companion depth, declared ungraded in the ledger. See Method and limits.

## Findings the audit added

1. Line 115, "Every console and portal route needs a session; an unauthenticated visit renders a sign in panel in place and never serves data." No item. NEW GAP, closed by C-UF-09 (a call without a session is refused unauthenticated, graded by test_unauthenticated_console_call_unauthenticated) and C-UF-10 (the sign in panel in place, graded by a browser substep).
2. Line 68, "a cancelled or completed move frees its destination." C-CF-07 covered the cancelled half only. Partial capture, closed by C-CF-30, graded by test_manually_completed_move_frees_destination.
3. Line 77, "eligibility is read when the decision is made." No item. NEW GAP, closed by C-CF-31, graded by test_approver_eligibility_read_at_decision_time.
4. Line 46, the spotter row, "their own assigned moves and issue reports | any other move." No item. NEW GAP, closed by C-RL-06, graded by test_spotter_cannot_accept_move_assigned_to_another_spotter.
5. The dispatcher row, "moves, the map, exceptions, shifts, dock read | approving." No item. NEW GAP, closed by C-RL-07, graded by test_dispatcher_approval_forbidden_request_pending.
6. Line 56, "Haulier and customer users sign in to the portal, a separate identity space." C-RL-04 named haulier users only. Scope drift, closed by rewording C-RL-04 to haulier or customer users and citing the customer report test as a grader.
7. Line 152, "the console is a rail on the left." No item. NEW GAP, closed by C-UX-24, graded by rubric criterion R37.
8. UI/UX notes lines 133 to 165, the palette, type, shape, component and access sentences added in this revision. Twelve asks with no item. Closed by C-UX-12 to C-UX-23, each graded by one rubric criterion, R25 to R36.

## Unresolved

- Line 130, "stale, which dims and disables writes." The state needs a live channel failure that no request from outside the app can induce. Settling it needs either a pinned way to force staleness or an in-container check.
- Line 4151, "The console stays responsive with two thousand assets on the map and a year of visits at a site." No pinned measurement a grader could take. Settling it needs a seeded load and a pinned threshold.
- The network manager row. No seeded member holds the role, so no call can exercise it. Settling it needs a seeded network manager.
- Overview line 20, "moves are assigned without asking." Automatic assignment is pinned as a site setting that is off at every seeded site, so graders can assign by hand without racing it; its cost model has no pinned observable outcome.

## Coverage account

| Measure | Machine | After adjudication |
|---|---|---|
| Items in body | 166 | 177 |
| Window-section asks identified | proposal only | 85 |
| Window-section asks covered by an item | not paired | 81 |
| Window-section asks declared ungraded | not paired | 4 |
| Gaps closed during adjudication | 0 | 10 |
| Items confirmed invented | 0 | 0 |

## Pinned literals

The instruction pins the corpus password deku-demo-pw-2026, the watchlist plates TX-9KR-221 and TX-4LM-870, the registrations MC-400932 and MC-300771, the site codes DAL1 and RNO2 with the zone America/Chicago, the member dual@tidewater.example.com and the realm junction. The checklist records ten literal values across nine items tagged literal; C-TR-64 carries both DAL1 and America/Chicago. The literals ledger in _handoff carries 146 values, and fixture_lint G6 passes in both directions, so no graded value is left for a builder to guess.

## Structural findings

Carried from the machine report unchanged: none. Structure, ids, tags, citations and ledger arithmetic hold. They were not reviewed because they are not reviewable.

## Method and limits

Coverage was judged by reading. The instruction was read before the machine report. The window sections and the HTTP contract were paired sentence by sentence; the unbudgeted Technical requirements prose and the Front-end specification were read for contradictions and for asks a grader relies on, and their remaining obligations were not each given an item. Two full passes over the window sections after the fixes added no new finding. A second check ran every pytest grader against a scratch reference of the pinned contract backed by real PostgreSQL and Mailpit: all 75 pass, and each of 21 naive defaults fails exactly its target test. That run found one grader defect, a JSON parse of an HTML page, fixed before this report. A checklist can conform to its format in full and still describe the wrong application.
