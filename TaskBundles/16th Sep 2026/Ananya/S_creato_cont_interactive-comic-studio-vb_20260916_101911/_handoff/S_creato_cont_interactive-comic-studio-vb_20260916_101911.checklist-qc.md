# Checklist QC report

---

## VERDICT: NEEDS REVIEW

The checklist has no gap, invention or unresolved finding left. The one remaining note is that the brief never pins two values the checklist correctly records as referenced-but-not-pinned; Section 5 grades this NEEDS REVIEW rather than PASS. Start with "Findings requiring action", item 1, which is for the specification author, not the checklist author.

---

| | |
|---|---|
| Instruction | instruction.md |
| Checklist | solution/checklist.md |
| Adjudicated | yes |
| Machine verdict before adjudication | PASS |

## Summary

This pass confirms the fix for the only finding of pass 3 and re-establishes the verdict for the current files: instruction.md SHA-256 5509b2d3 and checklist.md SHA-256 4c7962ba.

The audit compared both files against the copies taken at the start of pass 3, which that pass read in full. instruction.md is byte-identical. checklist.md differs in exactly one line, line 1312, which is C-CN-12. The other 1402 item lines, the pinned literals table, the referenced-but-not-pinned table, the ledger and the header are all unchanged.

checklist_qc.py was re-run on the current files with `--instruction`, writing its draft to scratch. It reports PASS, 1403 items, 791 pinned-literal rows, 2 unpinned values, no structural finding and no ledger-arithmetic finding. The audit's own scripts give the same results as in pass 3:
- All 60 API rows have a response item, and all 33 rows with a request cell have a request item, each matching its brief cell.
- 184 of 184 catalogue values match the brief.
- All 32 page titles and descriptions and all 48 seeded descriptions are recorded.
- Every one of the 791 literal values appears verbatim in the brief.

C-CN-12 now reads "The app accepts no debug query parameters." Constraints bullet 8 (line 1189) reads "No debug query parameters." The item carries the prohibition without narrowing its scope, so pass 3's finding is resolved. With it, all 491 obligation-bearing units are covered.

What keeps the verdict at NEEDS REVIEW is not a checklist defect. The brief refers to session expiry and to three responsive width steps without giving values, and the checklist records both in its referenced-but-not-pinned table. Section 5 of the adjudication prompt assigns NEEDS REVIEW when a non-blocking unpinned literal remains. No change to checklist.md is needed. The specification author may pin the two values, or accept that graders choose representative ones.

## Findings requiring action

1. **Two values are referenced by the brief but never pinned (for the specification author, non-blocking).**
   - Session lifetime: line 770, "A session that has expired or been revoked mid-action: the next request is denied", and the `expires_at` columns of `studio_sessions` (line 995) and `reader_sessions` (lines 998 and 999). No duration is given. The checklist records this against C-UF-24 in its referenced-but-not-pinned table. Expiry can still be exercised through revocation.
   - Responsive widths: lines 894 to 901 name "a tablet width", "slightly narrower", "a phone width" and "the narrowest supported width" without pixel values. The checklist records this against C-UX-84.

   Neither is a credential, route, status or grant threshold, and neither blocks a build or a grader. Resolution: either pin a session lifetime and the three width steps in instruction.md, or record that graders may choose representative values. Either way, nothing in checklist.md changes.

## Findings the checker raised and the audit overturned

- **Machine verdict PASS: adjusted to NEEDS REVIEW.** Structure and coverage hold, but the two non-blocking unpinned values in item 1 remain. Section 5 grades that NEEDS REVIEW.
- **Obligation segmentation proposal (126 sentences): rejected as an undercount.** The script's proposal is unchanged from earlier passes. Counting rules, bullets, table rows and paragraphs, the audit found 491 obligation-bearing units.
- **Coverage-ledger arithmetic "none": confirmed.** The ledger is unchanged from pass 3. Item counts per section match the body (20, 32, 819, 57, 91, 51, 133, 63, 16, 121), and no row has fewer items than sentences.

## Findings the audit added

None in this pass. Pass 3's single finding (C-CN-12) is resolved.

The pass-3 observations still apply and are recorded so they are not re-opened:
- **C-DC renumbering.** C-DC ids from C-DC-29 onward were renumbered between passes 2 and 3; any grader citation written against pass 2 may point at a different item. Grader coverage was not audited. This pass changed no id.
- **Duplicates.** Some restatements are minted twice rather than carrying two citations, for example C-RL-07, C-CF-26 and C-DC-17. No ask is lost.
- **Non-ASCII symbols.** Ten literals-table lines hold the sparkle and heart symbols from `consent.message` and `support.chip_tip`. Character conformance is the script's domain, and it passed them.

## Unresolved

None.

## Coverage account

| Measure | Machine | After adjudication |
|---|---|---|
| Obligation-bearing units identified | 126 (sentences, proposed) | 491 (rules, bullets, table rows, paragraphs) |
| Units fully covered | not computed | 491 |
| Units with at least one confirmed gap | 0 | 0 |
| API shapes table rows with a response item | not reported | 60 of 60 |
| API rows with a request cell that have a request item | not reported | 33 of 33 |
| Catalogue key and locale values itemised | not reported | 184 of 184 |
| Items confirmed invented | 0 | 0 |
| Items needing a faithfulness rewrite | 0 | 0 |
| Non-blocking unpinned values in the brief | 2 | 2 |
| Unresolved findings | 0 | 0 |

A unit is a numbered rule, a bullet, a table body row or a prose paragraph of instruction.md. Five label lines were excluded as context: lines 56, 730, 1024, 1066 and 1077.

## Pinned literals

The pinned literals table has 791 rows and is unchanged from pass 3. Every row points at an existing item, and every value appears verbatim in instruction.md; both were recomputed by script. There are 529 items tagged `literal`. Every value the brief pins was found in an item or a literals row. The only values a downstream reader would have to guess are the two the brief itself leaves open: the session lifetimes and the responsive width steps (item 1). The checklist lists both in its referenced-but-not-pinned table and sets its header count to 2.

## Structural findings

Carried through from the machine draft unchanged: none, meaning structure, ids, tags, citations and reconciliation hold. These were not reviewed, because they are not reviewable. The audit's recount agrees: 1403 items, ids sequential with no gaps in all ten blocks, no malformed item lines, and no hits for " and ", " while ", " including " or " as well as " in item text.

## Method and limits

This pass did not re-read every item by eye. It rests on the full pass-3 reading of both files (SHA-256 5509b2d3 and b8e219c1), which the audit held as copies. A file-level diff against those copies found one changed line (C-CN-12), and a line-by-line comparison of all item lines confirmed the other 1402 are identical. C-CN-12 was read against Constraints bullet 8. The audit also re-ran checklist_qc.py and its own scripts (ids, counts, literal rows and values, catalogue and seed transcription, API row coverage) on the current files, with the results given above. Copies of both current files were taken at the start of this pass.

Coverage was judged by reading, in pass 3 and for the changed line here, not by lexical score. The unit counts depend on the unit definition given in the coverage account. The audit does not establish which tests or rubric entries cite which items, and it did not review the tests, rubric provenance or other files other stages wrote into the bundle. A checklist can conform to its format in full and still describe the wrong application. By this audit's reading, this one transcribes the brief completely.

{"verdict": "NEEDS REVIEW", "unresolved": 0, "findings": ["No checklist change required; C-CN-12 fix confirmed", "Spec-level, non-blocking: brief leaves session lifetimes (C-UF-24) and responsive width steps (C-UX-84) unpinned"]}
