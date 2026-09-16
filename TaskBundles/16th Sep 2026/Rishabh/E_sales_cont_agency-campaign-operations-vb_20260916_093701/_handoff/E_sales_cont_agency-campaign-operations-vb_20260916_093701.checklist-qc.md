# Checklist QC report

---

## VERDICT: NEEDS REVIEW

No confirmed gap, invented item or structural failure remains, but a few design details from the brief have no item of their own and a few exact strings are pinned only in part. Start with the list under "Unresolved".

---

| | |
|---|---|
| Instruction | instruction.md |
| Checklist | solution/checklist.md |
| Adjudicated | yes, by an independent reviewer (two runs of qc_solution_checklist.md) |
| Machine verdict before adjudication | PASS |

## Summary

The audit checked `solution/checklist.md` (673 items in ten sections) against `instruction.md` (1,479 lines). The reviewer read the brief sentence by sentence and checked each item against the sentence it cites. Two independent review runs took place, with fixes between cycles.

The first run added 173 items across its cycles. They cover:
- role denials and grants;
- home, company and careers facts;
- ordering rules and award-entry states;
- error and offline states;
- split-text guarantees and the drawn marks;
- the two type faces, performance limits and seed facts;
- the sustainability page.

The second run added 26 more:
- a draft campaign's public address answering not-found;
- Escape cancelling a confirmation;
- colour never carrying meaning alone on public pages;
- motion moments, carousel contents, the home news section, the recruitment film dialog and the footer columns;
- the methodology page;
- exact pins for the menu destinations, the language pair, the chips, the officer titles and the ten unit names.

The final cycle of run 2 found no gap and no invented item. What remains is a short list of design details that are graded through broader items or rubric criteria and have no item of their own. None of them blocks. A reader should decide whether to give them their own items before the reference app is built.

## Findings requiring action

None are blocking. The entries under "Unresolved" are optional.

## Findings the checker raised and the audit overturned

- The machine checker's first-layer PASS was overturned twice in run 1, for missing obligations: role denials, home facts, company and careers records, ordering rules, error states, split text, the drawn marks and the sustainability page. Every one now has items, and the checker and the reviewer agree.
- The coverage-ledger row counts were corrected to the recount (Core features 30, Deployment contract 11). The Definition of done carries no obligation sentence of its own.

## Findings the audit added

- C-CF-273: a draft campaign's public address must answer the not-found status. It is graded by `test_draft_campaign_address_is_not_found`.
- C-CN-06 invented "eight newsroom pages"; it now reads "hundreds", as the brief says.
- Item and section-name drift was corrected in C-FE-55, C-FE-72, C-FE-79, C-FE-104, C-FE-105, C-TR-47 and C-CF-273.

## Unresolved

These are non-blocking. Each needs a decision from the task author.

1. **Design details without their own item.** These are graded through broader items or rubric criteria:
   - the six easing curves as a closed vocabulary (UI/UX notes, Motion);
   - the lightbox layering;
   - the seal geometry and "only ornament" (Front-end specification, Surfaces and marks);
   - the lattice and still-image recipes (Front-end specification, Generating every asset).
2. **Strings pinned only in part.**
   - C-FE-51 and C-FE-52 pin only the opening of the home positioning line and the whitespace line. The full strings contain connectors that the checklist text battery rejects inside one atomic item.
   - The other closing-marquee strings are unpinned.
3. **C-DM-36 pins only two of the thirteen Night Signal credit entries.** The full order is graded by `test_campaign_credits_keep_the_editorial_order`.
4. **C-UX-03 repeats the brief's wording** "acid yellow ... (by the colour vocabulary, a mid, vivid amber)". The amber gloss is required by the colour-vocabulary gate (G51). A reader could still read it as a contradiction with "never toward orange".

## Coverage account

| Measure | Machine | After adjudication |
|---|---|---|
| Items | 673 | 673 |
| Obligation-bearing sentences (proposed) | 69 | confirmed; each paired to at least one item |
| Gaps | 0 | 0 |
| Items confirmed invented | 0 | 0 (C-CN-06 corrected) |
| Unresolved | 0 | 4, all non-blocking |

## Pinned literals

The checklist records 264 pinned literals, and every literal item has its row in the table. Three values are referenced but not pinned, as the brief leaves them unset:
- the lifetime of a signed file link;
- the enquiry slowdown threshold;
- the marquee speed per band.

The partial pins are listed under "Unresolved".

## Structural findings

These were carried through from `checklist_qc.py` unchanged: structure, ids, tags, citations and reconciliation hold, and the ledger arithmetic matches the body. They were not reviewed, because they are decided in full by the script.

## Method and limits

The machine layer was `tools/checklist_qc.py` with `--instruction`. The adjudication was two independent review runs of `prompts/qc_solution_checklist.md`:
- run 1 had three cycles;
- run 2 had three cycles, the last with no new finding.

Each run read `instruction.md` in full and checked the checklist item by item.

This audit does not establish that the reference application satisfies any item. No application exists yet: the bundle is MECHANICALLY-GREEN, NO-SOLUTION.
