# Checklist QC report

---

## VERDICT: PASS

Machine draft from checklist_qc.py. The adjudicator reads instruction.md and checklist.md, resolves the coverage proposal below, and replaces this file.

---

| | |
|---|---|
| Checklist | checklist.md |
| Items in body | 168 |
| Sections | 10 |
| Pinned literals | 17 |
| Referenced but not pinned | 2 |
| Machine verdict | PASS |

## Structural findings (decided in full by the script)

- none: structure, ids, tags, citations and reconciliation hold.

## Coverage-ledger arithmetic (decided in full)

- none: every ledger row has items >= obligation sentences and matches the body.

## Obligation segmentation proposal (the adjudicator decides)

Recomputed obligation-bearing sentence counts per instruction section. The adjudicator confirms which are real obligations and pairs each to an item (COVERED / REVIEW / UNCOVERED).

| Instruction section | Obligation-bearing sentences (proposed) |
|---|---|
| Overview | 5 |
| User roles | 1 |
| Core features | 32 |
| User flow | 8 |
| UI/UX notes | 8 |
| Front-end specification | 2 |
| Technical requirements | 11 |
| Data model | 4 |
| Constraints | 1 |
| Deployment contract | 11 |
| Definition of done | 2 |

## Method and limits

This layer decides structure, ids, citations and ledger arithmetic in full. It only proposes obligation segmentation; coverage pairing and invention are the adjudicator's. A checklist can conform in full and still describe the wrong application.
