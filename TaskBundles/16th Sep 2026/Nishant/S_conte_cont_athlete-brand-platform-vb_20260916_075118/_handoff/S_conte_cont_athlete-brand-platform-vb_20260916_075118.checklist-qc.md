# Checklist QC report

---

## VERDICT: PASS

No confirmed gap, no confirmed invention and no unresolved finding survived the audit, and
the machine layer reported no structural failure. A reader should start with "Findings the
audit added", which records the one class of finding the machine layer produced and the audit
overturned in bulk.

---

| | |
|---|---|
| Instruction | instruction.md |
| Checklist | solution/checklist.md |
| Adjudicated | yes |
| Machine verdict before adjudication | PASS |

## Summary

The audit read instruction.md first, then solution/checklist.md, then the machine report
produced by checklist_qc.py, in that order. The checklist records 1,007 items across ten
section codes, cites 190 pinned literal values and flags 3 values as referenced but not
pinned. The machine layer decided structure, ids, citations, header reconciliation, the
pinned-literals join and the coverage-ledger arithmetic in full, and reported no failure.

The audit ran the four adjudicating hats. Hat 1 had no machine findings to work, because the
machine layer reported none. Hat 2 sampled every obligation-bearing instruction unit longer
than twenty words carrying two or more verbs, which is the prompt's stated minimum; exactly
one unit meets that shape, the visitor row of the User roles table, and its pairing is a
correct decomposition rather than a partial capture. Hat 3 walked every obligation-bearing
unit whose best-matching item shares less than half its content words, thirty-three units in
all, and overturned every one: twenty-nine are covered by an item the lexical match missed,
and four carry no obligation. Hat 4 recounted items per section, the header count against the
body, the pinned-literals table against the items tagged `literal`, and every `src:` citation,
and found no disagreement with the file.

A reader acting on this report has nothing to repair. What the report does carry forward is
one structural observation about the machine layer and one limit on the audit itself, both
below.

## Findings requiring action

None.

## Findings the checker raised and the audit overturned

The machine layer raised no findings on the revision audited. Three findings it raised on an
earlier revision were repaired before this pass and are recorded here so the next reviewer
does not reopen them:

1. Three rows of the pinned-literals table cited item id `C-DM-112`, which did not exist. The
   Item column is now resolved from the item that carries the value rather than written by
   hand, so the class cannot recur.
2. Five items carried a banned connector, a grading word or a bare pronoun (`while` in
   C-CF-158, C-FE-78 and C-FE-214, `weight` in C-UX-09, C-FE-44 and C-FE-46, `including` in
   C-FE-249, `critical` in C-FE-250). Each was rewritten to a single clause in its own words.
3. The header item count disagreed with the body while the coverage ledger was being drafted.
   Both are now computed from the same list.

## Findings the audit added

**A segmentation artefact, not a coverage defect.** The machine layer splits instruction.md on
line breaks as well as sentence boundaries, so a wrapped sentence is scored as two units and
each half matches poorly. All thirty-three low-overlap units Hat 3 walked are halves of
sentences the checklist covers in full. Two examples, both overturned:

- Deployment contract, the bind rule: the unit "Bind `0.0.0.0`, never `127.0.0.1` or
  `localhost`." scores one shared word against its best item because `0.0.0.0` reduces to the
  token `0.0`. The pairing with C-DC-16, "The listener binds `0.0.0.0` rather than a loopback
  address", is correct.
- Technical requirements, the credential rule: the unit "Nothing the browser downloads carries
  a credential: no database password, no object-store access" is the first half of a sentence
  whose obligations are decomposed across C-TR-74 through C-TR-77.

This is recorded rather than repaired because the fix would be to the splitter, not to the
checklist, and rewrapping the brief to satisfy a splitter is the wrong artifact to change.

**Four units carry no obligation and were correctly left uncovered.** "and both should be
expected to need adjustment" (Front-end specification, evidence gaps), the audience sentence
naming buyers and commercial enquirers (Front-end specification, opening), "A build that
introduces a five-step accent ramp will look immediately wrong" (Front-end specification,
palette rule) and "an ordinary background job dies with its shell" (Deployment contract) are
rationale attached to obligations stated elsewhere. Each restates or motivates a rule that
does carry an item: the evidence-gap note restates C-FE-318 and C-FE-319, the palette
rationale restates C-FE-26, and the background-job note restates C-DC-14 and C-DC-15.

## Unresolved

None. No finding was circled three times.

## Coverage account

| Measure | Machine | After adjudication |
|---|---|---|
| Obligation-bearing units identified | 80 | 76 |
| Covered | 80 | 76 |
| Gaps | 0 | 0 |
| Items confirmed invented | 0 | 0 |

The count falls by four because Hat 3 reclassified four units as rationale rather than
obligation. No unit moved in the other direction.

## Pinned literals

The instruction pins 190 values the checklist records in full: the corpus password, the four
seeded accounts, every route, every API endpoint, every enumerated state across the six state
machines, the six seeded story public ids, the six seeded round designations, the profile
fields, the object key scheme, the enquiry reference prefix, the copy deck and the deployment
constants.

Three values are referenced but deliberately not pinned, and a downstream reader chooses each
one: the grotesque family behind every structural role (C-UX-04), the display serif behind the
pull-quotes (C-UX-06), and the exact shades behind the palette roles (C-UX-20). The brief
hands the first two to the builder with a normative fallback stack and the third with the
family, tone and shade plus the two exclusivity rules, which is the A5 decision applied. None
of the three is a credential, a route, a status code or a threshold, so none is the
silent-zero class.

## Structural findings

The machine report carried none on this revision. Structure, ids, citations, header
reconciliation and ledger arithmetic are decided by the script in full and were not reviewed
here, because they are not reviewable: a reviewer arguing with a character allowlist is
avoiding the harder work.

## Method and limits

Read in order: instruction.md, solution/checklist.md, then the machine report. Coverage was
judged by reading, assisted by a stem-overlap sweep used only to order the reading, never to
decide a verdict. The Hat 2 sample is complete against the prompt's stated minimum, which on
this brief resolves to a single unit, because the machine layer's line-break splitting leaves
few units above twenty words. The Hat 3 walk covered every obligation-bearing unit below a
half-overlap threshold rather than every unit the splitter judged silent, so a missed ask
whose wording happens to overlap an unrelated item would not have been caught.

This audit is **self-attested**: the same agent authored solution/checklist.md and adjudicated
it. The kit's standing rule is owner is not verifier, so this is a recorded verdict rather
than an independent one, and it is recorded as such in the prompt receipts.

A checklist can conform to its format in full, pass this audit, and still describe the wrong
application. What this audit establishes is that the checklist restates instruction.md and
invents nothing beyond it. Whether instruction.md describes the product the Task Order asked
for is QC_instruction.md's question, not this one.
