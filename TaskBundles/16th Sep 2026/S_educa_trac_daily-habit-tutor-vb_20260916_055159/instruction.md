# Larkwise

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser, scroll
a strip of forty-two subjects on the marketing page, try a real exercise from one of them
without an account, sign up, finish a twelve-exercise lesson, and see their streak extend
to cover today, without hitting an error page. Finishing that same lesson a second time
must not extend the streak a second time, must not award its points a second time and must
not write a second set of attempts: the stored record must show exactly one completed
lesson. A number the page adds up for itself is not a record; the record is what the
service recomputed from the answers that were actually given.

## Overview

Larkwise is a free daily learning application wrapped in the single page that sells it.
The learning half is short lessons, a memory model that decides what comes back and when,
hearts, points, streaks and a weekly league. The marketing half is one long page, a course
index, a page per subject, a terms page, a privacy page and one honest not-found page.

It is not only languages, and that fact shapes everything underneath. The subject picker
carries forty-two entries and two of them, `Chess` and `Math`, are not languages at all.
The session engine, the memory model, the economy and the day arithmetic are therefore
subject-agnostic and work unchanged for a subject that has no target language. What differs
between subjects is only the exercise set and the answer matching, and both are declared per
subject. An engine with "translate this sentence" wired into it cannot teach chess.

Two people are never in the same place at the same time here, so the product is a private
one: a learner sees their own path, their own history, their own hearts and their own
streak, and the only thing they see of anybody else is a row in a weekly standings table.
It deliberately is not several things. There are no friends, no feed, no direct messages,
no comments, no payments, no subscription, no notifications of any kind, and no offline
mode. The full scope-out list is in `## Constraints` and it is part of the specification.

The genuinely hard part is that almost every number in this product is derived rather than
stored, and the arithmetic is unforgiving. Whether an answer is right is a graph of
accepted forms rather than a string comparison. When a word comes back is a decaying
probability rather than a ladder of fixed intervals. Whether today counts towards a streak
is a question about a local calendar date in a named timezone, which is a different
question from how many seconds have passed. And a lesson that is finished twice, or
reported twice, must land exactly once.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `learner` | Enrol in any open subject. Start, answer and finish lesson, practice and review sessions. Read and change their own timezone, day shift, daily goal and target retention. Read their own streak, hearts, points, history, traces and standings row. Read the standings of the cohort they are in. | **Cannot read, change or delete another account's progress, hearts, streak, attempts, traces, settings or enrolments, by any route.** **Cannot write their own points, streak length, heart count or standings position directly.** **Cannot start a session in a subject that is not open.** |

A `restricted` learner is the same role with one absolute rule attached rather than a
second role. Signup collects a year of birth, and an account whose learner is under
thirteen is created `restricted`. A restricted account is never shown anything to buy,
anywhere, under any condition. When a restricted learner runs out of hearts the only routes
offered are practice and waiting. There is no price, no upgrade prompt and no store link on
any page a restricted account can reach, and the setting cannot be turned off from inside
the product.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in
the UI is not authorization: a direct API call from a `learner` session to another
account's data or to any endpoint that writes a derived total must be rejected by the
server (an unauthorized request is denied, not served), leaving the protected state
unchanged.

Signup is open. Anyone can create an account from the signup form and every signup creates
a `learner`. A visitor may answer the sample exercises on a subject page without an
account at all; that anonymous progress is held against a browsing token and is carried
into the account created from the same browser.

Seeded accounts, all with the password `deku-demo-pw-2026`:

| Email | Display name | Timezone | Restricted |
|---|---|---|---|
| `learner@example.com` | Nadia Fenn | `Europe/Lisbon` | no |
| `learner2@example.com` | Bram Oduya | `Africa/Nairobi` | no |
| `learner3@example.com` | Ines Caro | `America/Bogota` | yes |

Ten further seeded learners exist at `learner4@example.com` through `learner13@example.com`,
same password, to fill the weekly cohort described in `## Data model`.

## Core features

### Auth

Larkwise owns its accounts itself. Each one is an email, a password kept only as a hash
that leaves the service in no response on any route, and a year of birth that decides
whether the account is `restricted`. Signing in mints a bearer token that rides every later
request for 24 hours before the learner has to sign in again. The public half of the site,
signup, login and the health route take no token at all, because a visitor has to be able
to try a subject before deciding to have an account.

1. An email that already belongs to an account cannot be signed up twice: the attempt is
   rejected as invalid, the form says which field is at fault, and the accounts table gains
   no row.
2. A correct email with a wrong password is rejected in the same words an unknown email
   gets, so the answer settles nothing about who has an account here.
3. A token that is missing, a token that has expired and a token that has been altered are
   each rejected as unauthorized, on every route outside that public half.
4. Signing up from a browser already holding a browsing token carries that token's sample
   attempts onto the new account, after which the browsing token answers nothing.

### The subject picker and the subject pages

The picker is the primary navigation of the whole product and it is not a decorative
carousel. It is a single horizontal strip of forty-two entries with a control at each end,
it scrolls by pointer, by drag and by keyboard, the arrow keys move between entries, the
scroll position follows focus, and the end controls page by a whole screen of entries
rather than by one. Each entry is a language mark and the subject name.

The order is not alphabetical and is not by popularity. The three promoted subjects come
first and the remainder is alphabetical by English name, with the constructed and
endangered languages left in their alphabetical places rather than segregated into a group
of their own. The order, exactly:

```
English, Chess, Math, Spanish, French, German, Italian, Portuguese, Dutch, Japanese,
Arabic, Czech, Welsh, Danish, Greek, Esperanto, Finnish, Irish, Scottish Gaelic, Hebrew,
Hindi, Haitian Creole, Hungarian, High Valyrian, Hawaiian, Indonesian, Korean, Latin,
Norwegian (Bokmal), Navajo, Polish, Romanian, Russian, Swedish, Swahili, Klingon, Turkish,
Ukrainian, Vietnamese, Yiddish, Chinese (Simplified), Zulu
```

A mark is not a national flag. A flag maps a language onto one country, which is wrong for
most languages on any subject list and contentious for several of them. A mark is a rounded
square carrying the subject's own two or three letter code, set in the display face, on a
ground derived from that code so the same code always produces the same ground.

5. `English`, `Chess` and `Math` are open. The other thirty-nine entries resolve to a real
   subject page that states the subject is not open yet and offers the picker; starting a
   session in one of them is rejected as invalid and nothing is written.
6. Every subject page states what the subject teaches, roughly how long it takes, the
   framework level it reaches where it declares one, whether audio exercises are available,
   and for a language the writing systems taught, which for several subjects is the largest
   part of the work and is invisible from the name alone. A subject that is not a language
   states its prerequisite in place of the writing systems.
7. An open subject page carries the unit list by section with the concepts each unit
   introduces, and **two real, playable sample exercises from the first unit**, answerable
   with no account. A page that describes a subject without letting somebody try it wastes
   the one moment a visitor is willing to try.
8. `English` is taught from Spanish. Its prompts are in Spanish and its answers are in
   English, and every text run on the page declares which language it is in, because the
   two are on screen at once.

### Enrolling

Enrolling happens in the picker row itself. Pressing an open entry expands that row in
place into a short confirmation carrying the daily goal choice of `1`, `2` or `3` lessons,
default `1`, and a start control. Nothing navigates away and no separate page is involved.

9. Enrolling twice in the same subject leaves exactly one enrolment and does not reset the
   daily goal, the pinned version or any recorded progress.

### The session

A session is assembled once, at the start, and its exercise list is fixed for its lifetime.
Exercises may be re-queued inside it but no new exercise is fetched mid-session.

10. A session is assembled with exactly `12` exercises for a lesson, drawn from concepts
    that are due, concepts that are nearly due, and new concepts where new material is
    allowed.
11. No more than `3` consecutive exercises are of one type, and no more than `2`
    consecutive exercises are on one concept.
12. New material is interleaved at positions `2`, `5` and `9` rather than delivered in a
    block. The first `2` exercises are the easiest in the session and the hardest sit in the
    middle third.
13. The session ends on an exercise the learner is likely to get right. A session that ends
    on a failure is remembered as a failed session.
14. An attempt lands in exactly one of four states: `correct`, accepted with nothing shown;
    `correct_with_note`, accepted with a spelling or accent note; `incorrect`, rejected with
    the canonical answer shown; and `skipped`, no answer given, which counts as incorrect
    for scheduling and costs no heart. `correct_with_note` is a state of its own and is
    never folded into `correct`, because it feeds the memory model differently.
15. An incorrect answer re-queues that exercise later in the same session, at least `3`
    exercises further on, at most once, and the re-queued instance uses a **different**
    exercise for the same concept where one exists. Re-showing the identical prompt tests
    recall of the last thirty seconds rather than of the concept.
16. The frustration guard: three consecutive incorrect attempts on one concept within a
    session end that concept's appearances for the session and queue it for the next one.
    Continuing to ask somebody the same thing they have got wrong three times is not teaching,
    it is grinding, and it is the point at which sessions get abandoned.
17. The answer is marked on the page immediately, without a page load and without waiting
    for the service. The service marks every answer again at reconciliation and its result
    is the one that is stored. Where the two disagree the service wins.
18. Interruption is handled, not ignored. Hiding the tab pauses the session and stops its
    timers. Closing the tab mid-session leaves the session resumable for `86400` seconds from
    its exercise index with hearts and attempts intact. On return the learner is **offered**
    the resumable session: it is never silently resumed and never silently discarded.
19. The same account opening the same session in a second place is offered a read-only view
    or a takeover, and two places never both earn from one session.

### Reconciliation, and the rule that governs the whole product

A finished session is reported once. Everything it earned is recomputed by the service from
the stored attempts. The numbers the page showed while the learner played are a display and
never an input.

20. **A session is reconciled at most once.** Idempotency here is the rule the whole product
    rests on. The first report is accepted and its result is
    stored. Every later report of the same session returns that same stored result: no
    second points award, no second streak extension, no second heart deduction, no second
    attempt row, and no change to any total. This holds whether the second report arrives a
    second later or a day later.
21. **Two reports of the same session arriving at the same time produce exactly one accepted
    result.** Exactly one wins, the other receives the winner's stored result, and no total
    is applied twice. A failed report leaves no partial state: no half-written attempt rows,
    no points applied without a streak update, no heart spent without an attempt to account
    for it.
22. Every attempt in a report must name an exercise from the list that session was assembled
    with, and the attempts must arrive in presentation order. A report naming an exercise
    outside the list, or carrying attempts out of order, is rejected in full and nothing is
    written.
23. An attempt faster than the human floor for its exercise type is recorded and earns
    nothing. The session still completes and the learner is told nothing about it.
24. The learner's own clock is never trusted for anything that earns. The report carries the
    browser's clock offset, the offset is recorded, and every award uses the service's clock.

### Grading and answer matching

A solution is not a string. It is the canonical form shown when the learner is wrong, a set
of accepted forms, a set of required tokens for order-free subjects, a set of forbidden
patterns that are wrong in an instructive way, and the notes that go with a near miss.

25. The accepted set is expanded from a compact grammar rather than typed out by hand. The
    grammar carries optional segments, alternations for synonyms the subject accepts,
    contractions in both directions and regional spellings with the subject's own preference
    as canonical. A grammar expanding beyond `10000` forms is rejected as invalid content and
    that subject does not load.
26. Before comparison an answer is normalized, in this exact order, and the order is part of
    the requirement: normalize to a single Unicode composed form; strip zero-width and
    bidirectional control characters; fold case using the target language's own rules;
    collapse internal whitespace and trim; strip terminal punctuation only, and only where
    the subject permits it; hold the diacritic-stripped form as a **separate** comparison and
    never as the primary one; and segment scripts that are not written with spaces by the
    subject's declared segmenter rather than by whitespace.
27. Case folding is language-aware. The Turkish dotted and dotless letter i is not the same
    letter as the English i, and a single locale-blind fold is wrong for every Turkish
    learner while working perfectly for everybody checking it in English.
28. Terminal punctuation only is stripped. An internal apostrophe or hyphen is part of the
    word in most target languages, and stripping all punctuation makes two different words
    identical.
29. A missing accent is `correct_with_note`, never a silent `correct`. Folding diacritics
    into the primary comparison teaches learners that accents are decorative, and in several
    languages an accent changes the meaning of the word.
30. An answer not in the accepted set is compared against every accepted form by
    Damerau-Levenshtein distance over extended grapheme clusters, not over code units. The
    threshold is `1` edit for answers up to `4` clusters, `2` for answers up to `10`, and
    `2 + floor(length / 10)` beyond that. A transposition of two adjacent characters counts
    as one edit, because an adjacent-key slip is the commonest typo there is.
31. An answer accepted on distance is `correct_with_note`, never `correct`.
32. **A near miss that is itself another form the learner has already been taught in this
    subject is `incorrect`.** If `bear` is one edit from `beer` and both have been taught,
    accepting `beer` for `bear` teaches the wrong word, which is worse than marking it down.
33. Distance tolerance is never applied to a single-character answer, to a number, or to an
    exercise whose whole point is a minimal pair.
34. For a subject that permits free word order the answer is graded as a multiset match over
    the required tokens after normalization, with a separate check on any token whose
    position the content declares fixed. The answer matcher never infers which positions are free;
    inferring it accepts word salad.
35. There is no partial credit. An answer is accepted or it is not.
36. No distractor in a word bank is a valid alternative answer. This is checked when the
    subject content is loaded, not at answer time, and a subject whose bank contains a second
    correct answer is rejected as invalid content and does not load. Distractors are drawn
    from the learner's own subject at or below the current level, never from a global list: a
    distractor the learner has never seen teaches nothing and is answered by elimination.
37. A word bank holds every solution token plus `2` to `4` distractors, shuffled from a seed
    derived from the session id so a reload does not reshuffle. A solution needing a word
    twice has that word in the bank twice. Tapping a placed token returns it to its **original
    bank position**, not to the end: returning tokens to the end reorders the bank under the
    learner's fingers mid-answer.
38. Free-text answers are never filtered by character and autocorrect is never switched off.
    The grading rules above are what tolerate what a keyboard does. Accented characters are
    offered on a strip above the field for subjects that need them.
39. When an accepted set is corrected because a learner reported a missing answer, attempts
    within the last `2592000` seconds that were marked incorrect and would now be correct are
    identified, those learners have their hearts refunded and their traces recomputed, and
    each is told once in a single message naming the exercise. Points and standings are
    **not** adjusted retroactively, because a settled competition cannot be reopened. This
    asymmetry is deliberate.

### The memory model

What is tracked is concepts, not exercises and not lessons. A concept is a word sense, an
inflection, a grammatical pattern, a character, an opening, a tactic or a rule; one exercise
touches several. An engine that schedules exercises will re-show one sentence forever and
never notice the learner stopped understanding the tense it was demonstrating.

40. A trace holds a strength, the last time the concept was seen, how often it has been seen,
    answered correctly and lapsed, a half-life in seconds, a due time and a state of `new`,
    `learning`, `review`, `lapsed` or `burned_in`.
41. The probability the learner still recalls a concept at a time `t` is
    `2 ^ (-(t - last_seen) / half_life)`. Worked example: a concept last seen `86400` seconds
    ago with a half-life of `86400` seconds has a recall probability of `0.5`; at `172800`
    seconds it is `0.25`; at `0` seconds it is `1.0`.
42. The half-life is fitted from that learner's own history on that concept, the concept's
    difficulty across all learners, the learner's overall accuracy and the elapsed time.
    Nothing about how the exercise was presented enters it. A fixed ladder of intervals treats
    a word somebody has known for a year the same as one they met yesterday.
43. `correct_with_note` lengthens the half-life less than a clean `correct` does, and does
    not shorten it the way an `incorrect` does.
44. **A lapse shortens the half-life rather than resetting it.** A full reset discards
    everything the learner knew, and one bad morning erasing a month is the single most
    demoralising thing a scheduler can do.
45. The half-life is clamped to the range `60` seconds to `15768000` seconds. A concept at
    the ceiling is `burned_in` and stops being scheduled unless the learner asks for it.
46. The due time is `last_seen + half_life * log2(1 / target_retention)`, with
    `target_retention` at `0.90` by default and settable per learner. Worked example: a
    concept last seen at a given instant with a half-life of `86400` seconds and a target
    retention of `0.90` falls due about `13136` seconds later; at a target retention of
    `0.50` it falls due `86400` seconds later.
47. Due is a hint, not an obligation. The assembler chooses from what is due, what is nearly
    due and what is new, under the session budget. Showing everything due, in due order, on
    every session produces sessions of wildly varying length and a queue that grows without
    bound after a week away.
48. **A returning learner is never shown their backlog in full.** Sessions stay their normal
    length, the assembler prioritises by strength against concept importance, and the backlog
    is displayed as a proportion of the subject and never as a count of overdue items. A
    number like "1,847 items due" is a reason to quit.
49. A concept overdue by months has its half-life re-estimated downward once on first
    re-exposure, not repeatedly.
50. New concepts are introduced only while the learner's due load is below a threshold, so
    adding material never buries review. The threshold adapts to how often that learner
    actually studies.
51. A trace is derived and is rebuildable in full from the stored attempts. When an accepted
    set is corrected the trace is recomputed from the attempts rather than patched.
52. The model is never shown as a number. The learner is told which skills are strong, which
    need practice, and what is due today. There is no percentage, no mastery score and no
    bar that empties while they sleep.
53. Two evaluations of the same trace at the same instant produce the same number.

### Difficulty

54. An ability estimate per subject area is updated after every attempt, incrementally, never
    by a batch recompute, and getting a hard exercise right moves it more than getting an easy
    one right. A new learner starts at the subject's median, not at zero, and the estimate is
    clamped so a run of luck cannot push somebody three levels up at once.
55. Difficulty adapts by choosing **which** exercises, never by changing what counts as
    correct. The grading rules above are identical for every learner. A build that loosens
    grading for a struggling learner has stopped teaching them.
56. The levers are the exercise type mix, the prompt length, the ratio of new material to
    review, and how close the distractors are. Time pressure exists only in a timed practice
    session and never in an ordinary lesson.
57. An exercise's difficulty across all learners is frozen until it has at least `200`
    recorded attempts.

### Hearts

58. A learner holds up to `5` hearts. The current count is computed **on read** from the
    stored count and the stored refill mark, never by a background job:
    `current = min(5, stored + floor((now - last_refill_at) / 14400))`, with `last_refill_at`
    advanced by the whole intervals consumed so the partial interval carries forward.
59. **The carry is the rule that gets missed.** Setting the refill mark to now on every read
    means a learner who opens the app every ten minutes never regenerates a heart at all.
    Worked example: a learner with `2` hearts and a refill mark `10800` seconds ago reads the
    page and sees `2` hearts with the mark unchanged; `3600` seconds later they read again,
    see `3` hearts, and the mark has advanced by exactly `14400` seconds, not to now.
60. Spending: an incorrect answer in a lesson costs `1` heart. An incorrect answer in a
    review, a practice or a sample costs nothing.
61. Running out of hearts mid-lesson ends the lesson and **keeps** the progress made in it.
    Discarding the lesson punishes twice for the same mistakes.
62. Restoring: a completed practice session restores `1` heart, at most once per `14400`
    seconds. There is no other route to a heart in this build.
63. A learner with no hearts is offered practice or waiting, and the page states how long
    until the next heart. A restricted account, which is what an account belonging to a minor
    is, is offered practice or waiting and nothing else. A payment prompt in front of a
    nine-year-old who has just run out of hearts is not made acceptable by a consent box
    somewhere, which is why this product has neither.

### Streaks and the day boundary

A streak is the count of consecutive learner-local days on which the daily goal was met.

64. The last completed day is stored as a **local calendar date**, not as an instant. Storing
    an instant and deriving the date at read time gives a different answer depending on where
    the reader is.
65. The learner holds one timezone, an IANA name such as `Europe/Lisbon`, never a fixed
    offset. An offset is wrong twice a year.
66. Changing timezone is allowed at most once per `86400` seconds and **never shortens the
    current streak**. A day already completed stays completed. A gap a timezone change would
    create is forgiven once per change, which is the only correct behaviour for somebody on a
    plane.
67. The day boundary is local midnight, which on a daylight-saving transition day makes one
    day 23 hours and another 25 hours. Both are one day. Counting days by dividing elapsed
    seconds by `86400` grants a free day in one direction and destroys a streak in the other.
68. A local midnight that does not exist resolves to the first instant that does. A local
    midnight that happens twice resolves to the first occurrence.
69. A learner may shift their own day by up to `6` hours, and the shift applies identically
    to the boundary and to every countdown.
70. A learner is capable of holding up to `2` freezes, which in this build are earnable by
    completing a week of daily goals and are not purchasable, because nothing here is. A
    freeze is consumed automatically at the day boundary when the goal was not met, and one
    freeze covers exactly one missed day.
71. **A freeze is consumed at most once per account per local date.** A boundary pass that
    runs twice, or that retries after a failure, must not consume two freezes for one missed
    day.
72. The learner is told a freeze was used on their next visit, not at the moment it was used.
73. A lapsed streak may be repaired within `172800` seconds of the missed day, at most once
    per `2592000` seconds. Repair restores the exact previous length plus any intervening days
    that were also completed. It does not restore to a rounded number and it does not restore
    a streak that lapsed before the last repair.
74. **The streak is computed from the stored history whenever it is read.** Any scheduled
    boundary work exists to consume freezes, not to define the streak. A streak that only
    exists after a job has run is wrong for everybody whose job has not reached them.
75. Displaying the streak: the countdown to the day boundary is shown in the learner's own
    timezone. When the
    browser's clock disagrees with the service's by more than `300` seconds the display uses
    the corrected time and says nothing about the discrepancy.

### Experience points, leagues and the leaderboard

76. Experience points are awarded for completing a session, with a bonus for a perfect session and a
    bonus for the first session of the learner's local day. A lesson awards `10`, a review
    `6`, a practice `4`, a perfect session a further `5`, and the first session of the day a
    further `5`. Worked example: a perfect first lesson of the day awards `20`; a second
    lesson the same day with one wrong answer awards `10`.
77. **Every award is computed by the service from the stored attempts.** The page displays;
    it never proposes.
78. A cohort holds at most `30` learners and is filled by matching on tier and on recent
    activity, so a returning learner is not placed against people earning ten times their
    weekly points.
79. A learner joins a cohort on their **first earning action of the week**, not at the start
    of the week. Creating cohorts in advance for everybody produces cohorts full of people who
    never showed up and a top thirty of three.
80. The tiers are `Copper`, `Bronze`, `Silver`, `Gold`, `Sapphire`, `Ruby`, `Emerald`,
    `Amethyst`, `Pearl` and `Diamond`, in that order. The top `7` of a cohort are promoted and
    the bottom `5` are demoted, except that nobody is demoted out of `Copper` and nobody is
    promoted out of `Diamond`.
81. **Ties are broken by the earlier last earning time.** Ties are the normal case at the
    promotion line, because many learners stop at a round number. Breaking ties by account
    identifier sorts by account age, systematically promotes older accounts, and is
    discoverable and unfair.
82. A cohort's week ends at one fixed instant for every member, the end of the ISO week in a
    single reference zone, shown to each member converted into their own timezone. It does not
    end at each member's local midnight, which would let whoever is last see the final
    standings before deciding how much more to do.
83. A closed week is frozen and stored and is never recomputed.
84. A cohort that closes while a member is mid-session counts that session's points in the
    new week, and the learner is told which week they counted for.
85. The reader's own row in the leaderboard is always current even when the rest of the board
    is up to `10` seconds stale. Somebody who has just earned points and does not see their own
    row move has been told the product is broken.
86. Anti-cheat is deliberately quiet. Points earned at a rate above the product's own ceiling sustained over an hour leave the
    standing held back from promotion and reviewed. A held-back account is **never** publicly
    marked, never removed from its cohort mid-week and never has points visibly deducted. The
    most likely explanation for a suspicious week is a genuinely brilliant week, and accusing
    somebody of cheating is far worse than letting one through.

### The subject graph and its versioning

87. The structure of a subject is a directed acyclic graph of units, each unit holding
    lessons and introducing concepts. The graph is validated when the subject
    loads: no cycles, every unit reachable from the start, and no unit exercising a concept
    that no earlier unit introduced. That last check is what stops a subject teaching the past
    tense in unit 3 and introducing the verb in unit 7.
88. Progress references units and concepts by **stable identity**, never by position. A
    unit's order may change; its identity may not.
89. **No content change ever reduces a learner's recorded progress, relocks content they had
    unlocked, or takes a crown away.** Inserting a unit in the middle leaves anybody already
    past that position untouched and does not require it of them. Splitting a unit gives both
    halves the original's completion. Merging two takes the higher completion of the two.
    Removing a unit leaves a tombstone and everybody who completed it keeps the credit.
    Reordering changes positions and nothing else. Retiring a concept archives its traces
    rather than deleting them and stops scheduling it.
90. A learner is pinned to a subject version at **session assembly**, not at sign-in, so a
    content change cannot alter the exercises underneath a session in progress. A session
    assembled against a version reconciles against that version, and a version stays available
    for at least `2592000` seconds or until no unreconciled session references it. The learner
    moves to the current version between sessions.
91. Every unit carries a short explanation in the learner's own language. An explanation with
    no translation falls back to the subject's base language with a marker and is **never
    hidden**. Hiding untranslated help is how learners in smaller languages get a worse product
    without anybody noticing.
92. Content authoring safety: a subject is refused at load, with the reason named, if any
    exercise's accepted set is empty or expands past its bound, if any word-bank distractor
    is an accepted answer, if any concept an exercise uses is introduced by no earlier unit,
    if any canonical solution is empty once normalized, which catches a solution that was
    only punctuation, or if any prompt contains a concept from a later unit, checked by the
    subject's own segmenter rather than by whitespace.
93. Internationalization and text handling are structural here rather than a late addition,
    because two languages are on screen at once on every language exercise. Every text run
    declares its own language. The subject catalogue names each subject in the reader's
    language and in its own. Text that is not written with spaces between words is segmented
    by the subject's declared segmenter wherever a word boundary matters, which is grading,
    prompt checking and line breaking. Thai, Khmer, Lao and Burmese are the cases that make
    this real: they put no spaces between words, so they need a dictionary-based segmenter
    rather than a rule that splits on whitespace. A translated string is assembled from named
    placeholders and never from concatenated fragments, because word order differs between
    languages and a concatenated sentence is right only in the language it was written in.

### The public pages

94. `/` and `/feed` serve the same page, with the same content and the same document title.
95. The marketing page runs in seven movements in a strict alternation: a hero with the
    headline and two actions beside the character scene; the subject picker; four claim
    sections reading `free, fun, effective`, `backed by science`, `stay motivated` and
    `personalized learning`, each a scene and a short heading with one paragraph, alternating
    which side the scene sits on; a platforms band headed `learn anytime, anywhere`; the
    proficiency band; a closing invitation; and the footer. At the narrowest tier the
    alternation collapses to a single column with the scene above the text every time, and the
    page carries the same content rather than a reduced set.
96. The two hero actions are `GET STARTED` and `I ALREADY HAVE AN ACCOUNT`, both the same
    width, stacked, the second set in capitals and the first not. That is the one place in the
    design where case carries the hierarchy rather than size or weight.
97. No claim about how many people use Larkwise, how effective it is, or how it compares with
    any other method appears anywhere on the site. The first claim section describes the method
    instead and carries no figure and no research link.
98. The footer carries six groups and below them a site-language list in which **each
    language is written in its own name for itself**, not its English name. A Greek speaker
    looks for the Greek word. The groups and their entries:

    | Group | Entries |
    |---|---|
    | `About us` | Courses, Mission, Approach, Efficacy, Handbook, Research, Careers, Brand guidelines, Store, Press, Investors, Contact us |
    | `Products` | Larkwise, Larkwise for Schools, Larkwise Certify, Podcast, Business, Larkwise Plus, Gift Larkwise Plus, Larkwise Max |
    | `Apps` | Android, iOS |
    | `Help and support` | product FAQs, schools FAQs, test FAQs, Status |
    | `Privacy and terms` | Community guidelines, Terms, Privacy, Do Not Sell or Share My Personal Information |
    | `Social` | Blog, and six social profiles |

    Every entry in the first four groups and the first three of `Privacy and terms`
    resolves to a real page in this build under `/about/{slug}`, `/products/{slug}`,
    `/help/{slug}` or its own path, all built from one long-form template. The six social
    profiles and the two `Apps` entries are plain text rather than links, because no
    address outside this application is referenced anywhere and no native application
    exists.
99. **Every internal link on every public route resolves.** A link in the header, the footer,
    the picker, a claim section or a subject page that answers not-found is a defect of the
    page that carries it.
100. A terms page is reachable from the footer of every page and is linked from the signup form
    itself. A privacy page is reachable from the footer of every page and states what Larkwise
    records about a learner and how long it is kept.
101. `Do Not Sell or Share My Personal Information` is a control, not a document. It opens a
    first-party preference panel that records a decision per category, is reachable from every
    route, never blocks first paint, and makes refusing exactly as easy as accepting.
102. **One not-found page.** An unknown address answers not-found and renders Larkwise's own
     page, titled `Error 404` in the document title and on the page, carrying a short line in
     the product's voice, a character in a puzzled pose, a `GET STARTED` action, a link to the
     subject index, and the address that failed so a report can name it. The title always
     matches the response: a page that answers not-found while the tab claims to be a real
     subject page is a defect.
103. An address that looks like it was meant to be a subject renders a distinct page reading
     that there is no subject at that address, with the full picker underneath. With
     forty-two subjects, a large share of wrong addresses are a mistyped subject name, and
     answering them generically wastes the site's commonest failure.
104. Every page view is recorded with its route and the time it happened, and a learner can
     read back their own views. No view is sent anywhere outside this application.
105. The long-form template serves `/terms`, `/privacy`, `/about/{slug}`,
     `/products/{slug}`, `/help/{slug}`, `/community-guidelines`, `/status` and the
     editorial route. It carries a table of contents, a last-updated date, a one-line
     summary of what changed, the author and the date on an editorial post, a measure
     capped so a line never runs beyond about seventy-five characters at any width, body
     copy at the product's own body size rather than a smaller editorial one, and no
     motion beyond the entrance animation the rest of the product uses.
106. `/blog` is editorial and lays itself out differently, because reading a long article is
     not scanning a marketing page. It uses the **same** tokens, the same radii and the same
     depth idiom as everything else: one design system, not two. A second set of ingredients
     under one product costs something forever afterwards, and a reader crossing from one to
     the other can feel the difference without being able to name it.
107. `/products/larkwise-certify` describes the certified proficiency test, and
     `/products/larkwise-for-schools` and `/products/larkwise-junior` describe the classroom
     and early-literacy products. `/products/larkwise-plus` and `/products/larkwise-max`
     describe the two paid tiers as products that exist elsewhere and carry **no price and no
     purchase route in this build**. `Larkwise Junior` has its own illustration set, the same
     chrome, the same footer and the same motion vocabulary.
108. `Pip`, the mascot, is a bird and is one of the generated cast. Pip appears on the hero,
     on the not-found page in a puzzled pose, on the session summary in a celebrating pose,
     and on an empty state in an encouraging pose.
109. The audiences the marketing page must serve are named on it: somebody starting a
     subject reaches `GET STARTED` and the picker; a returning learner reaches
     `I ALREADY HAVE AN ACCOUNT`; a parent or a teacher reaches the schools and
     early-literacy products from the footer; and somebody who wants a certificate reaches
     the proficiency band.
110. The first view of `/` transfers under `1MB` in total, and no binary of any kind is
     among it: no image file, no font file, no audio file. Interaction latency on the
     exercise player stays under `200` milliseconds at the seventy-fifth percentile
     measured over a session, which is what the rendering and the answer marking are
     budgeted against.
111. The interface is assembled from a small set of primitives, each with its own states:
     the slab button, the outline button, the text link, the field, the tile, the card, the
     row, the toast, the panel and the progress element. Every one of them is built once and
     used everywhere; a second implementation of the same control is a defect.
112. The utility routes, which are every route that is neither the marketing page, a subject
    page nor a learner surface, all answer honestly: a page that exists is found and served
    with a success response, and one that does not is not found and says so.
113. Nothing in the build references an address outside this application: not a font
     service, not a content delivery host, not an analytics endpoint, not a social widget,
     not a verification widget. A build that reaches outside is a contract violation however
     good it looks.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the marketing page, seven movements | public |
| `/feed` | the same page, same content, same title | public |
| `/courses` | the index of all forty-two subjects | public |
| `/courses/{slug}` | one subject, with two playable samples | public |
| `/terms` | the terms page | public |
| `/privacy` | the privacy page | public |
| `/community-guidelines` | the community guidelines | public |
| `/status` | the service status page | public |
| `/blog` | the editorial route, long-form | public |
| `/about/{slug}` | the twelve `About us` pages | public |
| `/products/{slug}` | the product family pages | public |
| `/help/{slug}` | the three FAQ properties | public |
| `/preferences` | the consent and privacy control panel | public |
| `/signup` | create an account | public |
| `/login` | sign in | public |
| `/learn` | the subject path, a vertical timeline | learner |
| `/session/{id}` | the exercise player | learner |
| `/session/{id}/summary` | what the session earned | learner |
| `/history` | the day-by-day activity timeline | learner |
| `/profile` | streak, points, league, strong and weak skills | learner |
| `/league` | this week's cohort standings | learner |
| `/settings` | timezone, day shift, daily goal, target retention, motion | learner |

**Entry and redirects.** An unauthenticated request for a learner route goes to `/login`
with the destination remembered and lands there after signing in. Signing in from the
marketing page lands on `/learn`. Signing out returns to `/`. A token that expires
mid-session returns the learner to `/login` and the session stays resumable with its
attempts intact. A signed-in learner who opens `/login` or `/signup` is sent to `/learn`.
An unknown address renders the not-found page with a not-found response.

**Journeys.**

1. A visitor opens `/`, scrolls the picker with the keyboard to `Chess`, opens
   `/courses/chess`, answers the two sample exercises and gets one wrong with the canonical
   answer shown, presses `GET STARTED`, creates an account with an email and
   `deku-demo-pw-2026`, and lands on `/learn` with the sample attempts already in their
   history.
2. Nadia signs in at `/login` as `learner@example.com`, opens `/learn`, presses the next unit
   on the vertical path, answers twelve exercises getting two wrong, sees each wrong one come
   back later in the session as a different exercise for the same concept, finishes, and sees
   `/session/{id}/summary` naming the points earned and the streak now covering today.
3. Nadia opens `/session/{id}/summary` again and refreshes it, and the summary is unchanged:
   the points are the same, the streak is the same, and `/history` shows one entry for that
   lesson.
4. Bram signs in as `learner2@example.com`, opens `/league`, and sees the `Bronze` cohort of
   twelve for the current ISO week with the promotion zone across the top seven rows, the
   demotion zone across the bottom five, the two learners tied on `150` points ordered with
   the earlier earner above, his own row current, and the deadline shown in
   `Africa/Nairobi`.
5. Ines signs in as `learner3@example.com`, answers enough wrong to run out of hearts, and is
   offered practice or waiting with the time to the next heart, and no price anywhere.
6. A learner opens `/settings`, changes their timezone from `Europe/Lisbon` to
   `Pacific/Auckland`, and their streak length is unchanged.

**States.** Every list has an empty state written in the product's own words: a path with no
unit started, a history with no days, a standings table before the first earning action of
the week, and a picker filtered to nothing. Every page has a loading state, and the loading
state is the three breathing dots rather than a blank. An error never blanks the page: it
arrives as a toast over the surface that was already there, and the surface stays usable.

## UI/UX notes

The product should feel like a toy that respects you, not a form. Somebody should understand
in the first moment that this asks for about ten minutes and gives something back they can
feel. The register is consumer and playful: it is used by children and by adults standing on
a bus, so everything is one step larger and one step heavier than an ordinary interface, and
that is the single decision the rest of the look follows from. The character is bright and
energetic, the type is a rounded geometric sans, and the motion is springy: things that
arrive arrive with a visible overshoot and settle.

**Colour, by role.** Every palette entry is stored as its three components rather than as a
finished colour, so any transparent variant of any colour is free without adding a second
entry, which is what keeps a palette this size from doubling again. A semantic alias points
at the entry and every component reads the alias, so changing what correct means changes
every correct answer in the product at once. The brand colour, every primary action and
every correct answer are a mid, vivid green, and nothing else on a page wears it. Its shadow
face is a mid, vivid lime. Links and the second action are a mid, vivid cyan, whose own
shadow face is a darker mid, vivid cyan, and the two-tone block on a progress element is that
same cyan with a hard stop halfway rather than a blend. Incorrect, destructive and the hearts
are a light, vivid red, and that red appears nowhere that is not one of those three things.
Points are a mid, vivid amber; streaks a mid, vivid orange; the highest tier a light, soft
indigo. Body text is a deep neutral, secondary text a mid neutral, disabled and placeholder
text a light neutral, borders and the default slab a near-white neutral, section grounds a
slightly darker near-white neutral, and surfaces the lightest near-white neutral in the set.
Tints are a light, soft cyan and a near-white, muted green, and the headline over a tinted
section is a near-black, muted blue. An always-light and an always-dark variant exists for
every role, because a component sitting inside a permanently light surface must not follow
the theme; that is what makes a dark mode possible later without revisiting every component.
Commit to light and design it fully. The exact values are yours so long as every rule above
holds.

**Type and typography.** No font binary ships and naming a family is not a dependency. The display role is
`"Segoe UI Rounded", "SF Pro Rounded", system-ui, -apple-system, Arial, sans-serif` and the
text role is `system-ui, -apple-system, "Segoe UI", Arial, sans-serif`, with the rounding
never simulated where the rounded face is unavailable. Two weights exist, `500` and `700`,
and there is no lighter weight anywhere: a `300` is an invention. The body of the whole
product is `17px` at weight `500` with a `20px` line height, and control labels are `17px` at
weight `500` with the line height set by the control. Secondary body is `16px` at `400`, dense
body `16px` at `400` on `18.4px`, small print `15px` at `400`, captions `14px` at `400`,
subheadings `15px` at `700` on `27px`, which are generously leaded on purpose, emphasised body `17px` at `700` on `20.4px`, section
headlines `32px` at `700`, and lead paragraphs `25px` at `400` on `34px`. Figures use tabular
forms wherever amounts stack, which is the standings table, the points readout and the streak
count.

**Depth.** This is the one thing that carries the product's character and it is not a
shadow in the atmospheric sense. An interactive surface is a coloured face sitting on a
solid slab of its own darker shadow face, with no blur at all, so it reads as physical
thickness the way a key on a keyboard does. Pressing it moves the face down onto the slab
and removes the offset, so the control visibly compresses; it does not scale and it does not
fade. The only blurred shadow anywhere in the system belongs to the header once the page has
scrolled, and it is barely perceptible. Do not add a blurred shadow scale; that is a
different design.

**Shape and density.** Buttons carry the dominant radius of the system, secondary buttons and
cards a smaller one, images and illustration frames a larger one, and a few controls are
fully round, which is what the small circular controls at the ends of the picker are. Density is comfortable rather than packed: the product is read at arm's length,
so rows breathe and nothing is compressed to fit more on a screen. Space over dividers,
throughout: sections read as separate at a glance without a rule between them.

**Hover and states.** Every control has a resting, pointed-at, pressed, focused and
unavailable state, and unavailable is never signalled by colour alone. Solid buttons hover by
brightness rather than by swapping colour, with a pale control darkening and a saturated one
brightening, so the control always moves away from what is behind it; a hover colour per
palette entry would double the palette. The outline button moves its background, its border
and its slab together, all a shade darker at once, and that triple is what makes it feel like
a real object rather than a rectangle that changed colour. Every hover state lives inside a
hover-capable query so a touch device never gets a stuck hover. Escape closes any panel, and a
destructive action confirms first.

**Motion.** Movement is springy and uniform: elements enter from a side, overshoot and settle,
and four travel distances exist with the overshoot always the same fraction of the distance
travelled, so the smallest element does not visibly wobble while the largest barely moves. A
panel rises fully into place from below its own height, paired with an overlay that turns half a revolution behind it. The plainest movement in the product, and the most used, is a plain fade-in from no opacity to full. A reward sparkle twinkles twice per
cycle and never appears to rotate. The loading spinner turns three full times, unevenly, fast
then slow then fast, so it reads as effort rather than as a machine ticking over, and the
three loading dots breathe in sequence as one animation at three phases rather than one
animation with delays, so the sequence is right from the very first cycle. Every transition
names the property it moves and none of them animate everything at once. Under a request for
reduced motion the spring resolves to a fade rather than to nothing, the sparkle holds at its
first frame, the spinner becomes a static indicator with a text label, the dots hold, the
picker stops advancing by itself and the scroll-driven hero scene holds at its first frame;
the fade is preserved, not removed as well.

**Layout and scroll.** Five breakpoints and no more, every query written from the narrow end
upward, and the arrangement must hold at every width in between rather than only at the named
tiers. Exactly one element on the marketing page is driven by scrolling, the hero scene, and
at the narrowest viewport it is replaced by its own first frame as a still picture rather than
running heavier there. There is no parallax, nothing pinned and no scroll-linked colour
change anywhere; the life in the page comes from the illustrations and from things springing
into place as they arrive. Stacking uses a named scale of six rather than ad hoc numbers, and
nothing in this product is allowed to sit above the toast layer.

**At a narrow viewport nothing overflows sideways and every navigation target stays
reachable**, the picker stays a horizontal scrolling strip rather than becoming a wrapped
grid, the two hero actions go full width, and the claim sections stack scene above text. On a
mobile phone the page carries exactly the content the widest arrangement carries: content is
never dropped to fit, so the narrow page is taller, not smaller.

**Illustration and iconography.** No image file ships and no external address is referenced, and the substitution is the same one throughout: a zero-asset build in which every drawing in the inventory is generated. That is the guide the whole visual layer follows. The characters
are drawn as geometry from a seed, each with a rounded bilaterally symmetric body, a small
closed set of eye and mouth shapes positioned within a fixed proportion band, three to five
colours from the palette above, and four poses: neutral, celebrating, encouraging and
thinking. They are a system with fixed poses rather than a set of arbitrary drawings, they
occupy the same positions and sizes throughout so every layout stays balanced, and being
geometry they stay crisp at any size. Section illustrations and spot art are generated compositions of a
ground, two to four simple forms from the same shape set and a single accent colour,
deterministic from the section they belong to. Icons are inline geometry on a twenty-four
unit grid with a two unit stroke, round caps and colour inherited from the text, and there is
no icon font anywhere: an icon font is invisible to a screen reader and its icons are absent
until it arrives. The required set is the heart, the flame for streaks, the gem for points,
the shield for freezes, the trophy, chevrons in four directions, close, check, speaker, slow
speaker, microphone, keyboard, the lightbulb for hints, lock, crown, person, people, cog, the
flag for reporting, and one tile per subject. The app-store badges are other companies' marks
and are replaced by plain tiles carrying the store name as text, which has the side benefit of
being readable aloud and translatable. The brand mark is a rounded square carrying the initial
of the product in the display face, and the wordmark is the product name in the same face.

**Accessibility.** Body text and its background meet the **contrast** bar of WCAG AA, and so
does anything that carries meaning, which specifically includes the placeholder and disabled
text and the footer links: a muted grey that fails the bar is raised where it means something
rather than left because it looks calmer. Focus is visible on every interactive element, and
on a solid button the focus ring sits outside the slab, because a ring inside a saturated face
is invisible. Touch targets are comfortably sized in both dimensions, including the small round
controls at the ends of the picker. Full keyboard navigation reaches every control, the arrow
keys move through the picker, and the scroll position follows focus. Every icon-only control
carries a label and every generated illustration carries a text alternative describing what is
happening in it, while the animated hero scene is hidden from assistive technology because it
conveys nothing. **Every text run carries its own language attribute**, which on a picker of
forty-two language names and on a lesson with two languages on screen at once is the
difference between a screen reader being useful and being unintelligible noise. Correct and
incorrect are distinguished by a shape and by words, never by green and red alone: those two
moments are the most colour-coded in the product and also the two that matter most.

**Copy that is pinned.** The session controls read `Continue`, `Skip`, `Check`,
`Can't listen now` and `Can't speak now`. Feedback reads `Nice!`, `Correct solution:`,
`Another correct solution:`, `You have a typo` and `Pay attention to the accents`. Hearts read
`Full hearts`, `Next heart in {time}` and `Practice to earn hearts`. Streaks read `Day {n}`,
`Streak freeze used` and `Extend your streak`. The league reads `Promotion zone`,
`Demotion zone` and `{n} to go`. Four system messages are requirements rather than decoration
and may not be softened into generic error text: `We were marking an answer wrong. Your hearts
are back.`, `Your streak counted for {date}, even though we were down.`, `You have a few things
to review. We will fit them in.`, and `We are having trouble hearing you. Skip this one, no
penalty.` Each of those is a place where the product tells somebody the truth about something
that affects them.

**Each page leads with one clear primary action**, visually distinct from every secondary one:
the marketing page leads with `GET STARTED`, the path leads with the next unit, and the summary
leads with continuing.

**What it must not be.** Not a form, not a dashboard, and not a marketing composition where
the working interface belongs. No page dominated by a single hue family with no second signal.
No decoration standing in for content. No soft atmospheric shadow anywhere. And no bar that
visibly empties while somebody sleeps: a decaying number is a very effective way of making
somebody feel they are failing at something they are actually doing well at.

## Technical requirements

Pages are produced on the server: the app is a server-rendered multi-page application built
with **NestJS** and **Handlebars** templates, so the browser receives finished HTML on first
paint for every route, signed in or out, with no client framework and no client router. The
front end is **vanilla progressive enhancement**: hand-written JavaScript that upgrades forms
which already work without it. The exercise player is the one surface that must not reload
between exercises, and it is built by enhancing a form that posts normally when the
enhancement is absent.

The datastore is **PostgreSQL**, reached at `DATABASE_URL`, read from the environment and
never hardcoded. It is already running.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor. The only backing
service available in this environment is `postgres`, reached at `DATABASE_URL`, and reaching
for anything else is a contract violation.

Auth is implemented by the app: email and password, passwords stored hashed, a bearer token
returned on login and required on every request except signup, login, health and the public
pages, expiring after 24 hours. An anonymous visitor holds a browsing token that carries
sample progress until it is exchanged at signup.

`GET /api/health` returns `200` once the app can reach PostgreSQL. Request logging is
structured, one line per request, and never carries a password, a token or an email address.

The service clock decides every day boundary, every award and every due time. The browser's
clock is used only to render a countdown, corrected by an offset the service supplies.

**Every public route carries its own social preview title, description and preview image,
and the preview image resolves.** The preview image is generated by the application from its
own geometry rather than loaded from a file or from any address outside this application, and
two public routes never declare the same preview title.

No credential, no token and nothing that can be used to sign in appears in anything the
browser downloads.

The module architecture is layered and the layers are not allowed to reach past each other:
tokens, then primitives, then composed components, then routes. A route may not restyle a
primitive, and a primitive may not know which route it is on.

Performance is a requirement rather than an aspiration, and the two budgets that carry it are
in `## Core features`: the weight of the first view of `/`, and the interaction latency of the
exercise player. Rendering follows from the first of those: the server sends finished markup,
the enhancement layer is small enough to parse without blocking the first paint, and nothing
on any route waits on a request to a second host because there is no second host.

The `/status` page states whether the application can reach PostgreSQL, and nothing else about
the machinery underneath.

## Data model

Thirteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
not a secret. Hash it as normal; the exact literal must work at login, and it must be written
into `/app/USER_README.md` alongside each account so a grader can sign in.

### accounts

`id`, `email` (unique, stored lowercased), `password_hash`, `display_name`, `timezone` (an
IANA name), `day_shift_hours` (an integer from `0` to `6`), `daily_goal_lessons` (`1`, `2` or
`3`), `target_retention` (default `0.90`), `restricted` (boolean), `created_at`. No endpoint
ever returns `password_hash`.

### courses

`id` (a kebab-case slug), `name`, `from_language`, `to_language`, `kind` (`language` or
`subject`), `picker_order`, `mark_code`, `is_open`, `version`, `unit_count`, `approx_hours`,
`framework_level`, `writing_systems`, `prerequisite`, `audio_available`. Forty-two rows;
three are open.

### units

`id`, `course_id`, `section_order`, `order`, `title`, `cefr_band`, `guidebook`,
`introduces_concept_ids`, `tombstoned`. The `order` is changeable; the `id` is not.

### lessons

`id`, `unit_id`, `order`, `kind`.

### concepts

`id`, `course_id`, `kind` (`lexeme`, `inflection`, `pattern` or `character`), `label`,
`difficulty`, `importance`, `introduced_in_unit_id`.

### exercises

`id`, `course_id`, `lesson_ids`, `concept_ids`, `type`, `prompt_text`, `prompt_image_refs`,
`solution_canonical`, `solution_grammar`, `required_tokens`, `forbidden_patterns`,
`distractors`, `cefr_level`, `difficulty`, `attempt_count`, `introduced_in`, `script`,
`direction`, `segmentation`. The `type` is one of `translate_text`, `translate_tokens`,
`select_image`, `match_pairs`, `listen_type`, `listen_select`, `speak`, `complete_cloze`,
`judge_grammar`, `arrange_dialogue` and `story_choice`. An exercise carries the concepts it
exercises, not only the words it contains. `arrange_dialogue` presents an out-of-order
conversation and takes an ordering as its answer; `story_choice` presents a narrative branch
point and takes a selection.

### enrolments

`account_id`, `course_id`, `course_version_pinned`, `daily_goal_lessons`, `started_at`,
`last_active_at`. Unique on `(account_id, course_id)`.

### unit_states

`account_id`, `unit_id`, `crowns`, `lessons_done`, `locked`. Keyed by unit identity, never by
position. No write may lower `crowns`, raise `locked` from false to true, or reduce
`lessons_done`.

### sessions

`id`, `account_id`, `course_id`, `course_version`, `unit_id`, `lesson_id`, `kind` (`lesson`,
`practice` or `review`), `exercise_ids` (ordered, fixed at assembly), `state` (`in_progress`,
`completed` or `abandoned`), `hearts_at_start`, `device_clock_offset_ms`, `started_at`,
`ended_at`, `reconciled_at`, `reconcile_result`. `reconciled_at` is written exactly once for
any session; a later report of the same session returns the stored `reconcile_result` and
changes nothing.

### attempts

`id`, `session_id`, `account_id`, `exercise_id`, `presented_index`, `answer_raw`, `state`
(`correct`, `correct_with_note`, `incorrect` or `skipped`), `note_kind`, `elapsed_ms`,
`earned`, `created_at`. Unique on `(session_id, presented_index)`. This table is the source of
truth for every derived number in the product.

### traces

`account_id`, `concept_id`, `strength`, `last_seen_at`, `seen_count`, `correct_count`,
`lapse_count`, `half_life_seconds`, `due_at`, `state` (`new`, `learning`, `review`, `lapsed`
or `burned_in`). Unique on `(account_id, concept_id)`. Derived: the whole table must be
rebuildable from `attempts` alone.

### streaks

`account_id`, `length`, `last_day_completed` (a date, never a timestamp), `freezes_held`,
`freezes_used_on` (a list of local dates), `repair_available_until`, `timezone`.

### hearts

`account_id`, `current`, `max`, `last_refill_at`. `current` as stored is a mark; the value
shown is always recomputed on read from `last_refill_at`.

### cohorts and standings

`cohorts`: `id`, `tier`, `week_id`, `member_count`, `created_at`, `closed_at`,
`frozen_result`. `standings`: `cohort_id`, `account_id`, `xp_this_week`, `joined_at`,
`last_earned_at`. A cohort holds at most `30` standings rows.

### page_views

`id`, `route`, `account_id`, `viewed_at`.

### Invariants

1. A session is reconciled at most once. Two reports of the same session, arriving together
   or apart, produce exactly one accepted result and one set of totals; the second report
   returns the first one's result.
2. A freeze is consumed at most once for one account on one local date, however many times a
   boundary pass runs.
3. `traces` and `unit_states` are derived values whose source of truth is `attempts`, and both
   must be rebuildable from it.
4. No write reduces a learner's recorded progress, relocks an unlocked unit, or lowers a crown
   count.
5. A failed reconciliation leaves no partial state: no orphaned attempt rows, no points applied
   without the streak update that belongs with them.
6. Every derived number the learner sees is computed by the service from `attempts`.

### Seed data

Three accounts, as listed in `## User roles`, each with the password `deku-demo-pw-2026`.

Forty-two `courses` rows in the picker order given in `## Core features`. `english`, `chess`
and `math` are open; the other thirty-nine are not. `english` is taught from Spanish. Each
open subject carries `3` units, `2` lessons per unit and `24` exercises, and the concepts of
each unit are introduced before any unit that exercises them.

Nadia Fenn is enrolled in `english`, has a streak of `4` days ending on the day before first
start, holds `2` freezes, and has `120` points this week. Bram Oduya is enrolled in `chess`
with `180` points this week. Ines Caro is enrolled in `math` with `0` points, is
`restricted`, and has joined no cohort because she has earned nothing this week.

One cohort exists, tier `Bronze`, in the current ISO week, and it holds exactly `12` members:
Nadia, Bram, and ten further seeded learners at `learner4@example.com` through
`learner13@example.com`, each named for a bird and each with the same password. Twelve members
is the number at which the top `7` and the bottom `5` partition the board exactly, with
nobody in both zones and nobody in neither. Two of the ten hold exactly `150` points each and
sit at the promotion line at positions `7` and `8`; the one at position `7` is the one whose
last earning time is earlier.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

### The chrome

The bar across the top has exactly two states and it swaps its contents rather than growing,
so nothing shifts when it changes. At rest, at the very top of the page, it carries the brand
lockup on the left and a `Site language:` control with a chevron on the right, with no shadow
and no ground. Once the page has scrolled at all, the language control is **replaced** by a
solid `GET STARTED` action, and the bar becomes sticky and gains the one barely-perceptible
blurred shadow in the whole system. The bar's own height is published as a single value that
every in-page anchor and every sticky offset reads, rather than repeated.

### The marketing page

The home page's spine is those seven movements in order, and it is the same spine at every
width. The alternation of scene and text down the seven movements is the page's whole layout rule,
and it is strict: the hero puts the scene on one side and the text on the other, and each of
the four claim sections flips which side the scene is on. Claim headings are set in the brand
green at the headline size, in lower case, and the four read `free, fun, effective`,
`backed by science`, `stay motivated` and `personalized learning`. Body copy underneath each
is at the product's body size.

The picker sits directly under the hero on white, above a hairline in the border colour, as a
single horizontal row with a chevron control at each end. Each entry is the language mark then
the subject name at the product body size and weight.

The platforms band is centred under the heading `learn anytime, anywhere`, with two store
tiles below it whose sub-labels read `Download on the` and `Get it on` above the store name.

### The path

`/learn` is a vertical timeline: the units of the enrolled subject in order down the page,
the completed ones behind the learner's position, the current one marked and carrying the
only primary action on the screen, and the ones ahead visible but quiet. The path scrolls to
the current unit on load. Beside it sit the streak count with its flame, the points total with
its gem, the hearts with their count, and the current league tier with its trophy, all of them
reading the derived value rather than a stored one.

### The exercise player

One exercise fills the screen. The prompt is at the top, the answer surface beneath it, and a
single `Check` action at the bottom which becomes `Continue` once the answer has been marked.
A progress element across the top fills as the session advances and is the two-tone cyan block
described in `## UI/UX notes`, not a gradient. The hearts sit beside it. Marking is immediate:
the result appears without a page load, correct in the brand green with a check shape and the
word, incorrect in the red with a cross shape and the canonical answer, and a note when the
answer was accepted with a typo or a missing accent. The word bank wraps to as many rows as it
needs and never scrolls horizontally.

### The history timeline

`/history` is a day-by-day timeline, newest first, one row per local day carrying the date in
the learner's own timezone, the sessions completed, the points earned and whether the day
counted towards the streak, with a freeze day marked as a freeze rather than as a gap.

### Toasts

Every system message arrives as a toast over the surface that was already there, never as a
page replacement and never as a modal that blocks the work. A toast is dismissable, is
announced to assistive technology, and never covers the primary action of the page beneath it.

### Generated assets only

No image file, no font binary, no audio file and no external address is referenced anywhere in
the build. Every character, illustration, mark, icon and preview image is drawn by the
application from the geometry described in `## UI/UX notes`, deterministically from its own
seed, so the same seed always produces the same drawing.

## Constraints

Single tenant: every account sees only its own learning record, and the only shared surface in
the product is the weekly standings table.

Not in this product, and not to be built:

**Audio, speech and pronunciation.** There is no audio output and no audio playback anywhere:
no speech is generated, cached or played, no microphone is read, no utterance is scored for
whether it is recognizable as the sentence, and no speech rejection rate is measured by age
band. The `listen_type`, `listen_select` and `speak` exercise types are declared in the
model and are suppressed by the session assembler because no speech service is configured,
leaving every open subject completable without them.

**Offline and synchronization.** The app does not keep working with the network off: a lost
connection interrupts the session in progress. Nothing is prefetched ahead of time, nothing is
queued and nothing is caught up later, so there is no conflict to resolve between a device and
the service.

**Notifications.** No push, no email, no reminders, no quiet hours, no tone rules and no
delivery deduplication. Everything the product has to say, it says on a page the learner is
already looking at.

**Billing.** No payments, no subscription, no store receipt validation, no refund, no
chargeback, no entitlement revocation, no family plan of up to six seats, no gifting, no
downgrade, no proration and no price anywhere a learner can reach. The two paid tiers exist
only as described product pages.

**Social.** No friends, no friend graph, no discovery by username or invitation link, no
contact-book discovery, no friend feed, no quests, no private messaging, no comments, no
likes and no user-generated text that another learner can read. The only shared surface is
the weekly standings table, and a held-back account is not discoverable there in any special
way: it appears in no search, no suggestion and no separate listing, because none of those
exist.

**Moderation and identity review.** No moderation queue, no report review workflow, no
display-name screening for embedded contact details, and no account review beyond holding a
standing back from promotion.

**Experiments.** No feature assignment, no exposure logging, no guardrail metric, no sample
ratio mismatch halt, no permanent holdback population and no kill switch.

**Scaling, regions and degradation.** The app runs in one region, on one database, with no
read replica. There is no consistency
guarantee weaker than reading what was just written, no outbox, no partitioned fanout stream,
no backpressure ladder, no degradation ladder and no content edge cache. Content is treated
as read-mostly and immutable per version, and that is the whole of it.

**Safety beyond the restricted account.** A minor's account is restricted and shown nothing to
buy; that is the entirety of the safety surface here, because there is no user-generated text,
no display name visible to anybody else, and nothing for one learner to report about another.

**Observability.** No grading disagreement metric, no rejection-rate alarm, no recovery drill
and no migration dry run beyond the recorded invariant that no write reduces progress.

**Everything external.** No third-party script, no analytics vendor, no external network call
at run time, and no address outside this application referenced anywhere. No native
application and no app store submission; the store tiles on the marketing page are tiles, not
links to a store. No interface language other than English and no right-to-left interface,
although a subject's own content may be in any script, including the scripts that are written
without spaces between words.

The app must stay responsive with `42` subjects, `3` open subjects of `3` units each, `144`
exercises, `500` accounts, `5000` sessions and `60000` attempts.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses.
  Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable
  from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{"email", "password", "display_name", "birth_year", "timezone"}` | the account and a bearer token |
| `POST /api/auth/login` | `{"email", "password"}` | the account and a bearer token |
| `GET /api/auth/me` | none | the signed-in account |
| `POST /api/auth/anonymous` | none | a browsing token |
| `GET /api/courses` | optional `open` | a top-level JSON array of subjects in picker order |
| `GET /api/courses/{slug}` | none | the subject, its units and its two sample exercises |
| `POST /api/enrolments` | `{"course_id", "daily_goal_lessons"}` | the enrolment |
| `GET /api/enrolments` | none | a top-level JSON array of the caller's enrolments |
| `GET /api/path/{course_id}` | none | the caller's units in order with their crowns and lock state |
| `POST /api/sessions` | `{"course_id", "unit_id", "lesson_id", "kind"}` | the assembled session with its ordered exercises |
| `GET /api/sessions/{id}` | none | the session and its remaining exercises |
| `POST /api/sessions/{id}/reconcile` | `{"attempts": [{"exercise_id", "presented_index", "answer_raw", "elapsed_ms"}], "device_clock_offset_ms"}` | the recomputed result: attempt states, points earned, hearts spent, streak after, units advanced |
| `GET /api/hearts` | none | the recomputed heart count and the time to the next |
| `GET /api/streak` | none | the streak recomputed from history, with the local date it covers |
| `POST /api/streak/repair` | none | the repaired streak |
| `GET /api/traces` | optional `course_id`, `due_only` | a top-level JSON array of the caller's traces |
| `GET /api/history` | optional `from`, `to` | a top-level JSON array of local days, newest first |
| `GET /api/league` | none | the caller's cohort, its tier, its week, its ordered standings and its deadline |
| `GET /api/profile` | none | streak, points, tier, strong skills, weak skills, what is due today |
| `PATCH /api/settings` | any of `{"timezone", "day_shift_hours", "daily_goal_lessons", "target_retention"}` | the updated account |
| `POST /api/preferences` | `{"category", "allowed"}` | the recorded preference |
| `GET /api/page-views` | none | a top-level JSON array of the caller's own recorded views |
| `GET /api/health` | none | `200` |

Field names are exact. Every list endpoint returns a top-level JSON array. A successful call
returns the named resource or shape; an invalid or unauthorized call is rejected as a client
error, never as a server error and never as a silent success, and carries a message naming the
reason. Bearer auth is required on every endpoint except signup, login, anonymous, health, the
public subject reads and the preference write.

### No mocks

PostgreSQL is the only place any of this lives. An in-memory list of attempts, a streak
counter held in the page, a points total the browser adds up and the service stores without
recomputing, traces kept only in a process that restarts empty, and a heart count written
whenever the page asks for one are all contract violations, however good the product looks.
The named provider is the fact: the app's UI and its own tables can only reflect what lives in
the provider, never substitute for it.

## Definition of done

A stranger can open the marketing page, try a real exercise from `Chess` with no account, sign
up, finish a twelve-exercise lesson and see today counted towards their streak. Reporting that
same lesson again changes nothing: the points, the streak and the history stay exactly as the
first report left them. Every number a learner sees is one the service worked out from the
answers they actually gave, and a learner under thirteen is never offered anything to buy.
