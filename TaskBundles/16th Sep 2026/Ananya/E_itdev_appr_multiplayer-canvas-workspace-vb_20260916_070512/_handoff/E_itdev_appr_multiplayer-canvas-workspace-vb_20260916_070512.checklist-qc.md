# Checklist QC report

---

## VERDICT: PASS

No confirmed gap, no confirmed invention and no unresolved finding remain after two consecutive clean passes. Start with "Findings the audit added" for what changed.

---

| | |
|---|---|
| Instruction | instruction.md |
| Checklist | solution/checklist.md |
| Adjudicated | yes |
| Machine verdict before adjudication | PASS |

## Summary

The audit read instruction.md first, then solution/checklist.md, then the machine report from checklist_qc.py. The machine layer reported no structural failure. The adjudication then read every coverage pairing whose grader is a pytest function or a browser substep, walked the brief sentences the checker's segmentation treated as carrying no obligation, and recounted every table from the files.

The checklist now holds 167 items across ten sections, 26 pinned literal rows, 1 referenced-but-unpinned value, and 49 rows in a Declared but ungraded part. The audit found four defects on its first pass and none on the two passes that followed the repairs.

A reader acting on this report should know that 49 obligations the brief states are recorded as declared but ungraded, each with its reason. They are obligations the agent must meet and no channel this kit runs can observe; several are proven downstream by the handoff gates. That part answers OPEN-DECISIONS D-H rather than carrying citations nobody earned.

## Findings requiring action

None open.

## Findings the checker raised and the audit overturned

1. Technical requirements, obligation-bearing sentences proposed 13, items 12. Overturned as not a gap: the sentences on schema migration, API versioning, pagination, the fifty-address invitation cap, instrumentation, timestamp zones, round-trip permission evaluation, live propagation and the two-hundred-frame bar each carry an obligation no pytest, browser or rubric channel can observe from outside the app. Each is a row in Declared but ungraded with its reason. The ledger records 12 graded obligations against 12 items.
2. Deployment contract, obligation-bearing sentences proposed 12, items 10. Overturned as not a gap on the same ground: the production build, detached start, bind address, reserved directories, no backing-service copy, no edge function, and no volumes, names or networks are proven by the handoff gates that boot the image (G13, G15, G19), and are recorded in Declared but ungraded.
3. Core features, obligation-bearing sentences proposed 33 against a declared 30. Confirmed and corrected: the ledger row now declares 33, and 84 items cover them.

## Findings the audit added

1. Coverage claims that no grader made (Hat 2, right words, wrong ask). Several items were bound to tests that never asserted them: a withdrawal and an invalidated approval sending no mail, the approval mail, the closed audit vocabulary, a malformed invitation, a thread travelling from a branch on merge, a rename after a delete, the seeded members' identity-provider subject, the frame row in PostgreSQL, the access request writing no row, and the signup page being absent. Resolved by adding the missing assertions to the named tests, so each binding is now a claim the test checks.
2. Obligations with no observable path (Hat 2, strength drift). The fifteen-minute edit window, an explicit deny beating every allow, the file-only deny rule, active file-name uniqueness, append-on-restore and member deactivation had items bound to tests that could not observe them. Resolved by moving each to Declared but ungraded with its reason.
3. New asks with no item (Hat 3). The Keycloak realm `deku` and client `kanvo-app`, the invalidation returning a branch to `in_review`, a presence read counting the caller present, the access form's repeat limit, the requester's notification centre carrying transitions that send no mail, a review request appearing in the reviewer's centre, and the peer-team seed `Beacon`, `Beacon Web`, `Beacon Landing`. Each now has an item bound to the grader that observes it.
4. Stale tables after renumbering (Hat 4). The Referenced but not pinned table pointed at ids that had moved, and five of its six values are now pinned in the brief. Three pinned-literal rows pointed at an item that no longer carried the value. Both tables were rebuilt against the current ids and verified value by value.

## Unresolved

None.

## Coverage account

| Measure | Machine | After adjudication |
|---|---|---|
| Items | 167 | 167 |
| Obligation-bearing sentences proposed | 87 | 87 |
| Graded obligations declared in the ledger | 84 | 84 |
| Obligations declared but ungraded | not counted | 49 |
| Gaps | 0 | 0 |
| Items confirmed invented | 0 | 0 |

## Pinned literals

The brief pins the seeded password, the five seeded addresses, the three mail subject prefixes, the library and its two components, the organization, both teams, both projects, all three files, the datastore, identity and mail variables, and the Keycloak realm and client. Each has a row pointing at an item whose text carries the value. One value is referenced and deliberately unpinned: the name a member types when opening a branch, which graders generate per run.

## Structural findings

Carried through from the machine report unchanged: none. Structure, ids, tags, citations and ledger arithmetic are decided by checklist_qc.py and were not reviewed here because they are not reviewable.

## Method and limits

The audit read instruction.md, then checklist.md, then the machine report, in that order. Coverage was judged by reading each item beside the grader bound to it in tests/workflows.yaml, the pytest-provenance sidecar and the rubric-provenance sidecar, and by reading the assertions of the bound pytest functions. Every pinned-literal row and every ledger row was recounted from the files. This audit does not establish that the graders pass against a real application; no application exists yet, and a checklist can conform in full and still describe the wrong application.
