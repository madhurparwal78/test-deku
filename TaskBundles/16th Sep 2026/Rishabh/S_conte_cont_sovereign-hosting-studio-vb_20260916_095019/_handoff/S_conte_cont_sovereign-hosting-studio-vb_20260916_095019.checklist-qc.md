# Checklist QC report

---

## VERDICT: PASS

The four round-13 fixes (C-UF-34, C-UF-35, C-CF-312, C-CF-313) are in place with the specified wording, and two full passes in both directions found no confirmed gap, no invention, no unresolved finding and no structural failure. Start with "Findings the audit added" for the verification and the notes.

---

| | |
|---|---|
| Instruction | instruction.md (1282 lines, modified 17:13) |
| Checklist | solution/checklist.md (818 items, modified 18:11) |
| Adjudicated | yes |
| Machine verdict before adjudication | PASS |

## Summary

This is the fourteenth audit of solution/checklist.md. It was checked against instruction.md, which has not changed since round 6. The checklist has 818 items in 10 sections, 548 pinned-literal rows and 4 `UNPINNED` rows. checklist_qc.py was run again on the current files. Its output went only to the scratchpad (checklist-qc-machine-rerun14.md, .json and .out). The script reports PASS with no structural or ledger finding and counts 818 items in the body. A recount from the files gives the same numbers. Nothing under Output was edited, and the stale handoff machine report was ignored.

All four round-13 fixes are in place with the wording round 13 specified:
- C-UF-34 is at checklist line 404 and C-UF-35 at line 405.
- C-CF-312 is at line 366 and C-CF-313 at line 367.
- The header reads `Items: 818`. The Core features ledger row reads 313 and the User flow row reads 35.

The browser steps in tests/workflows.yaml now perform each action on the page and confirm that it took effect:
- Line 236 adds a system in the side panel. Line 237 credits C-UF-35.
- Line 347 attaches a PDF, sends it and confirms that the founder's side panel for that reference offers the brief. Line 348 credits C-UF-34.
- Line 453 attaches a PDF with scripts switched off and confirms that it is stored. Line 454 credits C-UF-34.
- Line 612 adds a record in the side panel, publishes it, confirms the unpublish and confirms that the record leaves /builds. Line 613 credits C-CF-312 and C-CF-313.

The audit then read the whole instruction again against the items, and the items against the instruction. The first pass raised three candidates, all resolved as notes below. Two further full passes (hats 1 to 4) found nothing new. No item is invented, nothing is unresolved, and no action is required.

## Findings requiring action

None.

## Findings the checker raised and the audit overturned

- The script's proposed count of obligation sentences is too low, as in rounds 3 to 13. For example, it proposes 11 for User flow, against 35 traced items. Its "items >= sentences" check therefore tells the reader nothing about coverage. This decision is carried forward.
- The script proposes 1 obligation sentence for Definition of done. The checklist's ledger footnote says 2. Lines 1278-1282 hold two sentences, and both restate Core features rules 1, 2, 6, 7 and 8, which the footnote says. The difference is in the segmentation proposal only, and no item is affected.
- Decisions carried forward from earlier rounds and not reopened:
  - Restatement pairs: C-TR-26 and C-FE-101, C-UF-24 and C-CF-271, C-CN-06 and C-CF-238, and C-TR-26 and C-FE-214.
  - Line 965 is treated as architecture.
  - "Studio endpoint" in C-RL-11 is read as the founder-only endpoints.
  - Prefix-only and paraphrase pins are accepted: C-CF-130, C-FE-17, C-FE-20, C-FE-36, C-FE-39, C-FE-44, C-FE-46, C-FE-51 to C-FE-53, C-FE-66, C-FE-72, C-FE-80, C-FE-84 to C-FE-90, C-FE-92, C-FE-118, C-FE-125 and C-FE-186.
  - Cross-section citations are accepted: C-RL-30, C-UF-25 and C-UF-26.

## Findings the audit added

- Verification of round 13. C-UF-34, C-UF-35, C-CF-312 and C-CF-313 are present with the specified wording. Their browser steps (workflows.yaml lines 236-237, 347-348, 453-454 and 612-613) perform and confirm each action. The traceability matrix lists the new ids (tests/traceability-matrix.csv rows A48, A53 and A55). Resolved.
- Hat 1, the class sweep again. Each page action in the instruction was checked for an item that requires the action to take effect in the page. The sources were the route table (lines 476-492), the role table (lines 50-52), the eight journeys (lines 508-554), rule 29 (lines 451-466) and the Overview's list of studio actions (lines 35-36). Every action now has such an item:
  - Composer send with an attached brief: C-UF-34.
  - Adding a system: C-UF-35.
  - Recording checks: C-UF-32.
  - Appending a note: C-UF-31.
  - Adding, publishing and unpublishing a record: C-CF-312, C-UF-14 and C-CF-313.
  - Portrait upload: C-CF-276 and C-UF-15.
  - Inbox, panel, brief download and status change: C-CF-242 to C-CF-245 and C-UF-13.
  - Page-view log: C-CF-234.
  - Signup and sign-in: C-UF-02, C-CF-239 and C-CF-240.
  - The client's list and download: C-RL-06, C-CF-79 and C-UF-33.
- Hat 2, pairings with two verbs or more than 20 words. The refusal-writes-nothing sentences were reread for partial capture:
  - Lines 91-92: C-CF-15.
  - Lines 147-149: C-CF-50 and C-CF-55.
  - Lines 157-158: C-CF-54 and C-CF-55.
  - Line 183: C-CF-69.
  - Line 187: C-CF-71.
  - Lines 243-244: C-CF-263.
  - Lines 287-288: C-CF-124.
  - Lines 335-336: C-CF-273.
  - Lines 348-349: C-CF-171.
  - Lines 412-413: C-CF-277.
  - Lines 499-501: C-UF-06.

  The denial sentences at lines 54-58, 195-196 and 291-292 were also reread (C-RL-24, C-RL-25, C-CF-78 and C-CF-268). Each second verb has an item. No strength drift or scope drift was found.
- Hat 3, sentences that describe behaviour without a modal. The instruction was walked sentence by sentence, including the API table rows, the seed paragraph and the code block at lines 204-211. The three candidates below were raised and resolved as notes. Nothing else was found.
  - Line 1135 says an unpublished record is "absent from every public read". C-CF-164 says "every public list", and C-DC-29 does not repeat "published". The ask is still bound, because C-CF-165 ("An unpublished record address answers not-found") covers the API address as well as the page. The pytest at workflows.yaml line 667 credits C-CF-165 for requesting the draft "over the API and as a page". This is a note.
  - Lines 147-148 say "A submission must name the current version". C-CF-50 names a retired or unknown version, not a missing one. A missing version is an invalid call under C-DC-14, and the scripted and form paths always send the field under C-FE-82. This is a note.
  - The Definition of done sentence count is covered under the overturned findings above. It is a note.
- Hat 4, recounting. Nothing new. See the coverage account.
- Notes, not failures, carried forward unchanged:
  - Round 13:
    - Measurement entry stays API-bound (lines 52, 333 and 1241).
    - C-UF-12 is graded by an in-page send.
    - The top-bar labels in C-CF-241 are not stated to be links.
  - Round 12: line 425 (the phone-number reading) and line 110 (the value of `v`).
  - Round 11: C-CF-265 spacing, C-FE-182 outline-only visual clauses and C-CF-206 "at full strength".
  - Round 9: lines 106-107, 147, 1082-1083 and 453-454, and the null `nextCheckAt` for C-CF-91.
  - Rounds 4 to 6: C-DM-44, C-FE-147, C-FE-58, line 916, C-DC-16, C-DM-09, C-DM-13, C-CF-48, C-CF-40, C-UX-66, and the outline-only visual clauses.
- Two consecutive full passes (hats 1 to 4) after the candidates were resolved found nothing new.

## Unresolved

None.

## Coverage account

| Measure | Machine | After adjudication |
|---|---|---|
| Obligations identified | segmentation proposal only (sums to 73 sentences) | 818 item-level asks traced to quoted spans, with no page action left unbound |
| Covered | not paired by the script | 818 |
| Gaps | 0 | 0 |
| Items confirmed invented | 0 | 0 |

Section totals, recounted from the file:

| Section | Items |
|---|---|
| Overview | 8 |
| User roles | 30 |
| Core features | 313 |
| User flow | 35 |
| UI/UX notes | 70 |
| Front-end specification | 221 |
| Technical requirements | 35 |
| Data model | 51 |
| Constraints | 9 |
| Deployment contract | 46 |
| Total | 818 |

The total matches the header (`Items: 818`) and the coverage ledger. Each section is numbered from 01 with no gap, and every item line parses. The type tags are:

| Tag | Items |
|---|---|
| literal | 285 |
| capability | 249 |
| constraint | 119 |
| ui | 101 |
| role | 34 |
| contract | 18 |
| data | 12 |

The longest item body is 291 characters. Three items cite a section other than their own: C-RL-30, C-UF-25 and C-UF-26. Earlier rounds accepted all three. Every `src:` citation names a real position in its section.

## Pinned literals

The pinned table has 548 rows holding 548 distinct values. Every row points at an item whose body contains that value, and every backticked value in a `literal` item has a row. The four new items are `capability` items, and each backticked value they use already has a row: `/studio/systems`, `/studio/builds` and `/builds`.

The four `UNPINNED` rows point at C-TR-17, C-TR-34, C-UX-29 and C-UX-37, which matches the header count of 4. The instruction gives no value for any of them, so none blocks a build.

Forty-six backticked instruction values appear in no item body verbatim. This is the same set as in rounds 9 to 13, and every one is of a kind accepted earlier:
- worked-example display strings and times, whose values items state in other words
- long copy pinned by prefix
- page titles pinned as parts joined by a bar
- the negated addresses `127.0.0.1` and `localhost`
- the section reference `## User roles`
- `POST /build-request`, which C-CF-62 and C-CF-63 cover as a route

From the instruction side, a downstream reader has no value left to guess.

## Structural findings

These are carried over unchanged from the fresh checklist_qc.py run (scratchpad checklist-qc-machine-rerun14.md), which found none. Structure, ids, tags, section-level citations and ledger reconciliation all hold. These findings were not reviewed, because they are not reviewable.

## Method and limits

Files were read in this order:

1. instruction.md, all 1282 lines.
2. solution/checklist.md: all 818 items, the pinned table, the unpinned rows and the ledger.
3. The fresh checklist_qc.py report.
4. The round-13 adjudicated report.

The helper qc6_scan.py was run again. It recounted the file, checked the pinned rows and listed the backticked instruction values missing from item bodies.

tests/workflows.yaml and tests/traceability-matrix.csv were used only to confirm the round-13 credits and the grading of C-CF-165.

Coverage was judged by reading, not measured. The Hat 2 sample covered every pairing with two verbs on the write and denial paths, not every pairing in the file. A checklist can conform to its format in full and still describe the wrong application.
