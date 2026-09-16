# Checklist QC report

---

## VERDICT: PASS

Adjudicated. `checklist_qc.py` decided structure, ids, tags, citations and ledger
arithmetic in full and proposed the obligation segmentation; the pairing, the invention
sweep and the referenced-but-not-pinned rows below were decided by reading
`instruction.md` against `solution/checklist.md`.

---

| | |
|---|---|
| Checklist | `solution/checklist.md` |
| Items in body | 608 |
| Sections | 10 |
| Pinned literals | 237 |
| Referenced but not pinned | 5 |
| Machine verdict | PASS |
| Adjudicated verdict | PASS |

## Structural findings (decided in full by the script)

- none: structure, ids, tags, citations and reconciliation hold.

## Coverage-ledger arithmetic (decided in full)

- none: every ledger row carries at least as many items as the section has
  obligation-bearing sentences, and each row matches the body.

## Obligation segmentation, adjudicated

The machine proposal is confirmed. Every section carries more items than obligations
because the brief states several asks per sentence: the four minigame tables alone put
eleven items behind one rule. Pairing below is COVERED for every section; no obligation
was left without an item, and no item describes an ask the brief does not state.

| Instruction section | Obligations proposed | Items in the section | Adjudication |
|---|---|---|---|
| Overview | 4 | 20 | COVERED |
| User roles | 3 | 24 | COVERED |
| Core features | 34 | 335 | COVERED |
| User flow | 10 | 17 | COVERED |
| UI/UX notes | 4 | 50 | COVERED |
| Technical requirements | 4 | 28 | COVERED |
| Data model | 6 | 28 | COVERED |
| Front-end specification | 4 | 66 | COVERED |
| Constraints | 2 | 14 | COVERED |
| Deployment contract | 11 | 26 | COVERED |
| Definition of done | 0 | - | the section restates asks stated elsewhere; it earns no item of its own |

## Invention sweep

Every item traces to a sentence, a table row or a pinned literal in `instruction.md`.
Three families were checked by hand because they are the ones an author invents:

- **The four game tables.** Each item key, label, worth and maximum count in C-CF-67,
  C-CF-69, C-CF-71 and C-CF-73 was compared against the tables in `## Core features`, and
  the four game maxima in C-CF-74 were recomputed from them.
- **The seeded boards.** C-DM-18 to C-DM-26 were compared row by row against the seed
  table, including the two entries that share 640 and the reserved name served
  anonymously at rank 1.
- **The French copy.** Every backticked French string in the checklist appears verbatim in
  the brief, including the no-break spaces in tips 3 to 6 and the typographic
  apostrophes.

## Referenced but not pinned, adjudicated

Five values are named by the brief without a settled value. Each is deliberate: the
brief states the relation and leaves the number to the builder, so a checklist item that
pinned one would grade a value the brief never gave.

| What | Item | Adjudication |
|---|---|---|
| the exact colour value behind each named family, tone, shade | C-UX-03 | ACCEPTED: the brief names families and tones, and the rubric grades the relation |
| the exact easing curve behind the eased motion character | C-UX-30 | ACCEPTED: the brief pins four speeds, never a curve |
| the handwriting face used in the notebook | C-UX-14 | ACCEPTED: the brief pins one handwriting face and where it may appear, never its name |
| the dialogue of the fifteen travellers beyond the four keeper lines | C-CF-171 | ACCEPTED: the four keeper lines are pinned; the rest is the builder's writing |
| the per-letter delay of the title animation | C-CF-139 | ACCEPTED: the brief pins the order and the settle, never the delay |

## Method and limits

The script decides structure, ids, citations and ledger arithmetic in full. Segmentation,
pairing and invention are adjudicated above by reading both documents. A checklist can
conform in full and still describe the wrong application; that judgement belongs to the
QL review of `instruction.md`, not to this file.
