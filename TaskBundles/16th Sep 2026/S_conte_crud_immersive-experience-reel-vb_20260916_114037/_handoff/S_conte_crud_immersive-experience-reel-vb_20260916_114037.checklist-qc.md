# Checklist QC report

---

## VERDICT: NEEDS REVIEW

The checklist has no confirmed invention and no structural failure, but 38 brief obligations have no item because no grader can observe them from outside the running app, and the kit has not yet decided where such obligations belong (open decision D-H). Start with the Unresolved section.

---

| | |
|---|---|
| Instruction | instruction.md |
| Checklist | solution/checklist.md |
| Adjudicated | yes |
| Machine verdict before adjudication | PASS |

## Summary

The audit read instruction.md first, then solution/checklist.md, then the machine report from checklist_qc.py. The checklist holds 306 items across ten sections, 81 pinned literal rows and 5 referenced-but-not-pinned values. The machine layer passed: every id is sequential, every citation starts with a real H2, every literal item's value has a pinned row, and every section's item count is at least its count of obligation-bearing sentences.

Reading the brief sentence by sentence found no item that restates something the brief does not ask, and no pinned value a downstream reader would have to guess. It did find obligations the checklist does not carry. Each one was checked against the graders available to this bundle: an outside HTTP client, a database reader, the Mailpit inbox, a page-driving Chromium session, an LLM browser grader and the rubric judge. Nine of them could be observed, and graders and items were added for them during this audit (listed under Findings the audit added). The remaining 38 cannot be observed by any of those channels, for example an audio gain level, a mail retry schedule, a thirty-day session lifetime or a build-time glyph check.

Stage 3 of the kit forbids both fabricating a citation for such an item and dropping it silently, and its proposed resolution, a Declared but ungraded checklist part, is not yet adopted. They are therefore recorded here as unresolved rather than turned into items no grader cites.

## Findings requiring action

None beyond the Unresolved section.

## Findings the checker raised and the audit overturned

None. The machine layer raised no coverage finding; its seven wording findings on earlier drafts (bare pronouns and connectors inside quoted literal copy) were fixed by restating those items without the quoted sentence while keeping the sentence in the Pinned literals table.

## Findings the audit added

1. Line 173, "The producer's pitch page and any studio member with the queue open see new messages and state changes within twenty seconds while the tab is visible": no item. Added C-CF item "A studio reply reaches an open pitch page within twenty seconds with no reload" and the grader test_pitch_page_shows_a_studio_reply_without_a_reload.
2. Line 212, "The session is therefore not kept in browser storage": no item. Added the storage item, graded in test_unsafe_next_falls_back_to_the_desk.
3. Line 333, "every state-changing request made with it carries a request token, a mismatch being refused as forbidden": no item. Added C-TR item for a cookie-only write, graded in test_sign_out_ends_the_session_on_the_server.
4. Line 192, "a pitch mail to the producer links to their pitch page, a mail to the studio queue links to /studio/pitches, and enquiry mails link to /contact": no item. Added the mail link item, graded in two mail tests.
5. Line 105, "an empty one with Ask a question first.": no item. Added the literal item, graded in test_assistant_refuses_empty_or_long_questions.
6. Line 148, "A reel created by starring without a reel gets the title Untitled reel": no item. Added, graded by a browser step.
7. Line 165, "opens the pitch form listing the reel's items, read-only there": no item. Added, graded by a browser step.
8. Line 138, "The account panel, opened from that capsule, lists the display name and organisation, Your reels with a count, Your pitches with a count, Audio, and Sign out": no item. Added, graded by a browser step.
9. Line 212, "The active reel defaults to the most recently updated reel on a new machine": no item. Added, graded in test_offline_star_is_held_then_sent_in_order, which reads the capsule count on a fresh browser.

Hat 2 sampled every item drawn from a sentence with two verbs and every sentence over twenty words in Core features Accounts, Reels and Pitches. Three partial captures from the first draft had already been split into separate items (reset first-mail, reset single use and reset dies on sign in; stale version and current reel; withdraw returns reel and withdraw mails studio) and no further partial capture was found.

## Unresolved

Each needs a kit decision on D-H (whether an obligation no outside channel can observe belongs in the checklist, and in what part). The brief still carries every one of them.

1. Line 41: the wheel accumulator decays after 0.4s, and touch drag counts at 1.5 times.
2. Line 55: the studio mark is not a link.
3. Line 101: opening the assistant focuses the input without changing scene state.
4. Line 108: the assistant failure copy and retry control, the refused-or-empty answer copy, and a scroll closing the panel.
5. Line 117: the audio setting kept on the account follows the producer to another machine.
6. Line 119: ducking to 0.3 while an answer streams.
7. Line 124: exactly two cookie categories.
8. Line 131: sign up lands on /desk with the unverified banner. A browser sign up would spend the sign-up budget the pytest layer needs.
9. Line 135: the reset token lasts 60 minutes.
10. Line 136: sessions last 30 days and extend on use.
11. Line 154: the note counter at 450 characters, and a failed save retrying twice.
12. Line 161: nothing is deleted with both a typed confirmation and an undo.
13. Line 169: a failed submission is never retried automatically.
14. Line 178: mail is sent after the store, a mail failure never fails the action, retries three times, then shows Notification not delivered.
15. Line 192: no mail for anything else, never for an assistant conversation.
16. Line 199: held changes survive closing the page, and pitch submission and assistant questions are disabled offline.
17. Line 200: one banner at a time, in the stated priority.
18. Line 205: the three reconciliation rules after a conflict.
19. Line 206: rollback restores scroll position and focus.
20. Line 207: another tab catching up on visibility change, and an unpublished project leaving the reel state.
21. Line 213: signing out with held changes warns first.
22. Line 236: an expired session keeps typed text, and a sign out in another tab removes the capsule.
23. Line 267: the lower-left luminance ceiling enforced by the build.
24. Line 269: tablet and short-landscape layout, the phone copy block and description truncation.
25. Line 279: the interface fade clamped at nine tenths.
26. Line 281: the loading field's thirty by thirteen geometry beyond the judged resolve.
27. Line 285: lift, move and drop announcements, the phone long press and up and down controls.
28. Line 301: scene composition order, lighting, and particles placed from scene_seed.
29. Line 303: the degradation ladder and render_degraded reporting.
30. Line 323: the build failing on a missing glyph, locale selection order, date and number formats.
31. Line 325: the module layering, the seventeen components and the stores.
32. Line 333: the request log line and its exclusions.
33. Lines 352, 354, 356, 359: the address-block limits for sign in, sign up, assistant and API reads. Grading them would exhaust the verifier's own budget from the same address.
34. Line 369: performance budgets, deferrals and preloads.
35. Line 379: account deletion anonymising the account.
36. Line 432: numbered forward-only migrations.
37. Lines 439 to 446: the negative scope constraints (no payments, one locale, no native app).
38. Lines 454 and 455: /app/USER_README.md and the reserved directories, which a verifier running in a separate container cannot read.

## Coverage account

| Measure | Machine | After adjudication |
|---|---|---|
| Obligation sentences identified | 119 | 119 |
| Items | 297 | 306 |
| Asks with no item, now graded and added | 0 | 9 |
| Asks with no item, ungradeable, unresolved | 0 | 38 |
| Items confirmed invented | 0 | 0 |

## Pinned literals

The brief pins the seeded accounts and password, the entry copy, the intent labels and addresses, the worked filter, every refusal message, every mail subject prefix, the budget and timing slugs, the seeded reel, note, pitch and studio message, and the head titles. The Pinned literals table carries 81 of them. The five referenced-but-not-pinned rows (colour values, the typeface name, the easing curve, the drag handle label and the search field name) are left to the builder by the brief, and no grader asserts them. No graded value is left for a reader to guess.

## Structural findings

None. The machine layer's structural checks passed and were not re-reviewed, because they are not reviewable.

## Method and limits

The brief was read in full, then the checklist, then the machine report. Coverage was judged by reading, not by lexical match. Hat 2 sampled the two-verb and long sentences in three sections rather than every pairing. This audit was run by the same agent that authored the checklist, so it is a recorded verdict, not an independent one. A checklist can conform to its format and still describe the wrong application; the correct and naive reference builds used to exercise the graders are evidence about the graders, not about this checklist.
