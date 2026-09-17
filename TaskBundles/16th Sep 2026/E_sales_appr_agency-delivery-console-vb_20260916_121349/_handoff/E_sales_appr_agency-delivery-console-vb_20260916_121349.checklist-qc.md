# Checklist QC report

---

## VERDICT: NEEDS REVIEW

Window-section asks with no pinned observable remain declared ungraded, and the unbudgeted companion depth was itemised to its observable subset rather than sentence by sentence. Start with Unresolved.

---

| | |
|---|---|
| Instruction | instruction.md |
| Checklist | solution/checklist.md |
| Adjudicated | yes |
| Machine verdict before adjudication | PASS |

## Summary

The audit read instruction.md first, then solution/checklist.md, then the machine report from checklist_qc.py. Every sentence of Overview, User roles, Core features, User flow, UI/UX notes, Constraints, Deployment contract and Definition of done was read against the items. The contract tables, business rules and seeded fixtures in Technical requirements, the Data model invariants and the Front-end specification routes, templates, states, accessibility table and work-breakdown properties were paired to items where a grader can observe them.

The machine layer passed structure, ids, citations and ledger arithmetic, and every section carries at least as many items as the machine recount of its obligation-bearing sentences: Overview 6 against 2, User roles 20 against 1, Core features 37 against 3, User flow 20 against 2, UI/UX notes 28 against 2, Technical requirements 192 against 111, Data model 11 against 11, Front-end specification 89 against 67, Constraints 7 against 1, Deployment contract 8 against 6. The body holds 418 items.

Adjudication found seventeen window-section asks with no item or a partial item, and all seventeen were closed before this report with new items and graders: seven Never cells of the role table, the annotation and brief-completion steps of the journeys, and eight UI/UX asks. The asks that stay declared ungraded have no observable a separately running grader can reach, and are listed under Unresolved.

## Findings requiring action

None open. Every confirmed gap below was closed by adding an item and a grading channel.

## Findings the checker raised and the audit overturned

- The machine recount proposed 1 obligation-bearing sentence for User roles and 3 for Core features. Overturned as a floor, not as a finding: the segmenter reads a table row or a numbered rule as one unit and matches only modal markers, so the adjudicated asks are counted by reading, 20 role asks and 37 feature asks, each with an item.

## Findings the audit added

1. User roles table, finance admin row, "approves deliverables, opens the vault". No item for the vault half. NEW GAP, closed by C-RL-15, graded by test_role_table_never_cells_denied_at_api.
2. Account director row, "issues invoices". No item. NEW GAP, closed by C-RL-16, graded by the same test.
3. Analyst row, "writes outside reports". No item. NEW GAP, closed by C-RL-17.
4. Recruiter row, "applicants | client data". No item. NEW GAP, closed by C-RL-18.
5. Client finance row, "invoices and billing documents | deliverables". No item for the deliverables half. NEW GAP, closed by C-RL-19.
6. Producer row, "financial fields, standing credentials". C-RL-13 covered standing credentials only. Partial capture, closed by C-RL-14.
7. Security officer row, "approves its own break-glass". No item. NEW GAP, closed by C-RL-20.
8. User flow journey 1, "opens a shared deliverable, annotates a point, approves the version". The annotation verb had no item. Partial capture, closed by C-UF-18, graded by judged criterion R20.
9. User flow journey 4, "A visitor completes the six step brief on /start-a-project/ and sees the reference and expected response time." No item. NEW GAP, closed by C-UF-19, graded by a browser substep of gclid_without_consent_denied_storage.
10. UI/UX notes, "There is no light theme." No item for the mode commitment. NEW GAP, closed by C-UX-02, graded by R1.
11. UI/UX notes, "aligned figures use tabular digits". No window item. NEW GAP, closed by C-UX-03, graded by R11.
12. UI/UX notes, "a reduced motion preference turns entrances into a short fade". C-UX covered only the smooth-scroll half. Partial capture, closed by C-UX-04, graded by R13.
13. UI/UX notes, "Text meets WCAG 2.2 AA contrast". No item. NEW GAP, closed by C-UX-05 with C-FE-02 on the muted foreground, graded by R21.
14. UI/UX notes, "targets are comfortable to touch". No item. NEW GAP, closed by C-UX-06, graded by R16 once its criterion named touch-sized controls.
15. UI/UX notes, "icon-only controls carry labels". No item. NEW GAP, closed by C-UX-07, graded by R22.
16. UI/UX notes, "overlays close on Escape and return focus". The return of focus had no item. Partial capture, closed by C-UX-08, graded by the vault slide-over browser substep, whose step now confirms focus returns.
17. UI/UX notes, the palette paragraph lacked a shape axis and a hover state for primary actions. The brief gained the sentence "Cards and sheets are flat raised surfaces edged by hairlines, and primary buttons answer hover with a masked label swap", carried from the measured hover-swap primitive and the token table, with C-UX-28 graded by R18 and C-UX-27 by R19.

## Unresolved

- Overview, "Parallax is not a marketplace, has no self-serve signup, and does not host client websites." Closed signup is graded; the marketplace and hosting clauses have no observable. Settling them needs a pinned probe, and none is natural.
- User roles, the group admin row and the client viewer row. No seeded client viewer exists, and the group admin's Never cell restates the vault rule already graded for every principal. Settling the viewer row needs a seeded viewer.
- User flow journey 2, "the number appears and the draft leaves the queue". The browser walk runs before any draft exists. Settling it needs a seeded draft reserved for the browser walk.
- User flow States, "offline with staleness". Needs a network failure no outside request can induce.
- Constraints, the scope-out lines, the no-outbound-host line, instant zones, opaque identifiers and the responsiveness volume. No pinned observable.
- Deployment contract, /app/USER_README.md, the reserved directories, the production build, the health route, no edge functions and no persistent volumes, fixed container names or custom networks. A separately running grader cannot observe them.

## Coverage account

| Measure | Machine | After adjudication |
|---|---|---|
| Items in body | 401 | 418 |
| Window-section asks identified | proposal only | 129 |
| Window-section asks covered by an item | not paired | 118 |
| Window-section asks declared ungraded | not paired | 11 |
| Items confirmed invented | 0 | 0 |

## Pinned literals

The checklist pins the corpus password `deku-demo-pw-2026` and the Keycloak realm `parallax` as literal items. Every other value a grader asserts, seeded addresses, ticket references, contract and invoice numbers, secret values, refusal codes and email subjects, is stated verbatim in instruction.md and recorded in the literals ledger, which fixture_lint G6 reconciles in both directions. No value a grader depends on is left for a downstream reader to guess.

## Structural findings

None. Carried through from the machine report, which found structure, ids, tags, citations and ledger arithmetic sound; these were not reviewed because they are not reviewable.

## Method and limits

Read in this order: instruction.md, solution/checklist.md, the machine report. Coverage was judged by reading every window-section sentence and pairing it to an item; the unbudgeted sections were paired where a grader observes an ask and are otherwise declared. Every pytest grader was run against a scratch reference on real PostgreSQL and Mailpit, 80 of 80 passing, with 38 wrong-default switches each failing its target test. A second full pass over the window sections after the fixes added nothing new. A checklist can conform to its format in full and still describe the wrong application; this audit does not establish that the brief itself is the right product.
