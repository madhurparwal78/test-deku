# Bytefold

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser, narrow a catalogue of 240 algorithm
problems down to one slice, open a problem, write a solution in the page, submit it, and read a
verdict computed from hidden tests, without hitting an error page. A different stranger, signed in
as someone else, must NOT be able to read that submission, that draft or those hidden tests by any
means, including a direct request to the API with a valid session of their own. A solution that
loops forever must come back as `Time Limit Exceeded` and not as a request that never answers: the
program has to be stopped by something outside itself, and a verdict the app hands to itself
without running anything is not a verdict.

## Overview

Bytefold is a practice platform for programmers preparing for technical interviews. Its centre of
gravity is a catalogue of algorithm problems, each carrying a statement, constraints, a
language-specific starter signature and a set of tests the solver never sees. A visitor filters the
catalogue, opens a problem, writes a solution in an editor embedded in the page, and submits it. The
product compiles or interprets that solution, runs it against the hidden tests under a time and a
memory limit, and returns a verdict, a runtime, a memory figure and a percentile against everyone
else who solved the same problem.

Around that core sit five further surfaces. A marketing route is the unauthenticated pitch, with an
employer wall and a read-only editor demonstration. The catalogue is a faceted browse over the whole
problem set, with topic, category, difficulty, status and employer facets. Contests are scheduled
competitions with a live countdown, a scored ladder and a rating. Learning is curated multi-chapter
explore cards and ordered study plans with per-member progress. Community is a discussion feed with
categories, votes and view counts. A paid tier sells two subscription terms, priced by region, which
gate part of the catalogue.

Three actors use it. A visitor, signed out, browses the catalogue, reads free statements, reads
discussion, watches a contest and sees the pricing route. A member, signed in, does all of that and
also submits, saves progress, keeps a streak, registers for contests, posts and votes. A subscriber,
signed in and entitled, does all of that and also reaches the gated catalogue, the employer facet,
and the editorial solutions.

It deliberately is not several things. There is no native or mobile application. There is no
external payment processor, no card and no invoice. There is no outbound mail of any kind. There is
no file upload and no object store. There is no third-party analytics collector, no performance
agent and no bot-challenge service. No binary asset ships at all: no image file, no font file, no
icon font and no video.

The genuinely hard part is that the product's central claim, that a stranger's program is run on
your machines against tests they cannot see and scored in seconds, is a claim about machinery that
never appears on a screenshot, and a build that renders 240 rows beautifully while evaluating
submitted code inside its own request handler is not a partial build of this product but a different
product wearing the same paint.

## User roles

| Role | Can do |
|---|---|
| Visitor (signed out) | Browse and filter the catalogue, read a free statement, read discussion and solutions, view a contest and its standings, view study plans and explore cards, view the pricing route, run a solution against the visible example cases. **Cannot submit, cannot save a draft to the service, cannot register for a contest, cannot vote, cannot post, cannot read any member's submissions.** |
| Member (signed in, `active`) | Everything a visitor can, plus submit, keep a solved set and a streak, save drafts and notes, create saved lists, register for and compete in a contest, post and vote. **Cannot read another member's submissions, drafts, notes or lists; cannot read a gated statement, an editorial body, the employer facet or the frequency histogram; cannot read any problem's test cases.** |
| Subscriber (signed in, entitled) | Everything a member can, plus the gated problems, the editorial bodies, the employer facet and its three orderings, the frequency histogram, the debugger, and unlimited saved playgrounds. **Cannot read another member's private records either, and cannot read any problem's test cases.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a Member session to any Subscriber-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged.

Three checks are separate and must stay separate. Who is calling: absent or invalid credentials are
refused as unauthenticated. What their plan allows: a signed-in member asking for a gated body is
refused as payment-required, never as forbidden and never as missing, because the padlock affordance
says plainly that the thing exists. What this identity may do to this record: a request for another
member's submission answers as if it does not exist, because saying "not allowed" confirms that it
does.

Signup is **open**: anyone may register. Three accounts are seeded for grading, and every one of
them uses the password `deku-demo-pw-2026`.

| Email | Username | Role |
|---|---|---|
| `member@example.com` | `nadia_roux` | Member, no entitlement |
| `member2@example.com` | `tomas_iversen` | Member, no entitlement |
| `subscriber@example.com` | `priya_shah` | Subscriber, yearly term, region `US` |

## Core features

### Auth and accounts

Accounts are email and password, implemented by the app itself. A successful sign-in answers `200` with an `access_token`
field carrying a bearer token for programmatic use, and sets an opaque session cookie for browser use. Session state
lives on the server, so signing out ends that session and its bearer token stops working at once. The session cookie
alone is never accepted as authorization on `/api`, where every authenticated call carries the bearer token. The
minimum password length is `8` characters and the maximum is not less than `128`, with no composition rule and no
forced rotation; a shorter password is rejected as invalid input. A failed sign-in answers `401`. A password never
appears in any response body, including an error.

1. A member is in exactly one state: `unverified`, `active`, `restricted`, `locked` or `deleted`, and `GET /api/me`
   reports it. A newly registered member is `unverified`. An `unverified` member may submit, and that is deliberate:
   the fastest path from landing to a first accepted solution is the product. An `unverified` member may not vote and
   may not register for a contest; both are refused as forbidden.
2. `5` consecutive failed sign-ins lock an account. A `locked` account is refused sign-in even with the correct
   password, with exactly the message a wrong password produces, so a caller cannot tell a locked account from a
   wrong guess.
3. Registration validates the address syntactically, normalises it for comparison by lowercasing the domain only
   while preserving the local part exactly as given, and holds uniqueness on the normalised form, so an address that
   differs only in the case of its domain signs in to the same account. A username that collides with an existing one
   case-insensitively is rejected as invalid input, and so is one that collides after confusable-character folding,
   so that two accounts cannot look identical on a leaderboard.
4. Registration **responds identically whether or not the address is already registered**. Registering
   `member@example.com` a second time returns exactly the response a fresh address returns, creates no second
   account, and changes nothing about the existing one: its original password still signs in. This is the rule that
   stops the product being used to test a list of stolen addresses against.
5. Verification is completed inside the product, from a link on the account route, and moves the member from
   `unverified` to `active`. Settings lists every session with a device label and a last-seen time, and ending one
   from there signs that device out.
6. Signing out ends the server-side session and clears the cookie, and returns the same response whether or not a
   session existed. A bearer token used after its session was signed out is refused as unauthenticated. A sign-out on
   one device leaves the others alone.

### The catalogue

The catalogue at `/problemset/` lists 240 published problems. It carries a left rail, two rows of
topic chips with an `Expand` control, a row of category pills, a control row and, at the widest
tier, a right rail of panels.

1. Six axes filter the list. `category` selects exactly one of `algorithms`, `database`, `shell`,
   `concurrency`, `javascript` or `pandas`, shown as the pills `All Topics`, `Algorithms`,
   `Database`, `Shell`, `Concurrency`, `JavaScript` and `Pandas`, with `All Topics` the default and
   exactly one active at a time. `topics` selects zero or
   more of the 47 topic tags. `difficulty` selects zero or more of `Easy`, `Medium` and `Hard`.
   `status` selects exactly one of `all`, `unsolved`, `solved` or `attempted`. `employers` selects
   zero or more employer tags. `search` is free text over the number and the title.
2. Between axes the filters combine as **and**. Within `topics` they combine as **and**, not or:
   selecting `Array` and `Two Pointers` returns only problems carrying both tags. Within
   `difficulty` and within `employers` they combine as **or**: selecting `Easy` and `Hard` returns
   both. These two are deliberately opposite, because a technique filter narrows and a difficulty
   filter widens, and a build that makes them the same has made one of them useless.
3. `status` is evaluated against the caller's own solved and attempted sets. For a signed-out
   caller, any `status` other than `all` is **rejected as invalid input**, never answered with an
   empty list, because an empty list looks like an answer.
4. Every facet value is shown with a count, and the count beside a value is **the number of problems
   that would be returned if that value were added to the current filter set**, computed with every
   other axis applied and with that value's own axis excluded from the multi-select axes. Worked:
   with `Medium` selected and `Array` not selected, the count beside `Array` is the number of
   `Medium` problems tagged `Array`. The count beside `Easy` is the number of problems tagged as the
   current topics are, at `Easy`, ignoring that `Medium` is currently selected. There are two facet-count mistakes and only one of them
   ships. A build that applies the full filter to every facet shows `0` beside every unselected
   difficulty, which is wrong and obviously wrong. A build that applies no filter at all shows the
   same numbers forever, which is wrong and not obvious, and that is the one that ships.
5. Topic chips are ordered by problem count descending, then by name ascending. The tie-break is not
   optional: two tags on the same count must appear in the same order on every request.
6. The default order is problem number ascending. The other orders are acceptance descending,
   difficulty ascending as `easy` then `medium` then `hard`, frequency bucket descending, and title
   ascending case-insensitively. **Every one of them is ordered by its key and then by the problem
   number ascending, without exception**, because a list ordered by a column that ties will otherwise
   show one row twice across two pages and never show another.
7. Pagination is by cursor. Pages carry fifty rows and are addressed by a cursor that encodes the ordering key and the
   tie-break value of the last row on the previous page, never by a row offset. Walking every page
   of any ordering must yield each of the 240 problems exactly once, with no repeat and no omission.
   A page past the end returns an empty list, a null cursor and a successful response, never a
   not-found, and the total count is still correct.
8. The day's featured problem is **pinned above the result set and is not part of it**. Page one
   carries fifty rows plus the pinned row; page two begins at row fifty-one of the ordering, not at
   row fifty. A build that folds the pinned row into the query loses a problem at the page boundary.
9. The shuffle control opens a problem drawn uniformly **from the problems that survive the current
   filter set**, never from the whole catalogue. With a filter applied that matches three problems,
   fifty presses of shuffle open only those three.
10. Rows are zebra striped on alternate rows and hover to a fainter fill. Every row carries a status
    mark, the title as `<number>. <title>`, an acceptance percentage to
    one decimal place, a difficulty word and a five-bar frequency histogram. `Easy`, `Med.` and
    `Hard` are the words in a row; `Easy`, `Medium` and `Hard` are the words in a filter. Both
    spellings ship. The frequency histogram and the employer facet are behind the entitlement: for a
    member without one the histogram renders greyed under a padlock and an `employers` filter is
    **refused as payment-required**, while a subscriber filtering by two employers receives the
    problems of either.
11. **The row payload is identical for every caller.** The member's solved or attempted mark is not
    in it. A second, per-member request keyed by the member and by the identifiers on the page
    returns the status for those fifty, and the page composes them. A row payload that varies by
    caller cannot be shared, and a shared payload that carries one member's ticks will show them to
    another.
12. **What the product shows is what the product stored.** Every value a screen displays for a
    member, the solved mark on a row, the draft in the editor, the verdict and its figures, the
    streak, the plan progress, the entitlement, is read back from storage on the next request and
    comes back the same. Reloading a page, or opening the same address in a fresh session signed in
    as the same member, returns the values that were shown, and a value that exists only in the page
    that drew it is a defect however correct it looked.
13. The filter state lives in the query string in full: topic, category, difficulty, status,
    employer, sort and page. A filtered view is therefore a link, and opening that link in a fresh
    session reproduces the same list in the same order.
14. Search behaviour: it matches the problem number and the title. Searching `Two Sum` returns `1. Two Sum`, and a
    query that is entirely digits matches the number first and exactly, so that typing `1` finds `1. Two Sum` first
    rather than below three hundred titles containing the digit.
15. The control row carries a search field with the placeholder `Search questions`, a sort control,
    a filter control, a solved counter reading `0/240 Solved` beside a progress ring, and the
    shuffle control. The right rail carries a daily calendar with a streak badge, a `Weekly Premium`
    strip of five slots labelled `W1` to `W5`, a coin balance with a `Redeem` link and a `Rules`
    link, and a trending-employers panel whose search field reads `Search for a company...`.
16. **Every internal link on every public route resolves.** `Library`, `Quest`, `Explore`,
    `Study Plan`, `Online Interview`, `Assessment`, `Store`, `Redeem`, `Download App`,
    `Help Center`, `Bug Bounty`, `Terms` and `Privacy Policy` are all reachable pages of this
    product, and a visitor who follows any of them from any route arrives somewhere real rather than
    at a not-found page. An address that matches no route renders the product's own not-found page
    inside the application shell, with a way back to the catalogue, and answers not-found. An unknown
    problem slug does the same on the workspace route, so an error never blanks the page.

### The problem workspace

1. A problem is addressed by slug and never by number: `/problems/two-sum/` is canonical, and the
   number is display only. Four tabs sit under that slug, each a real address the browser can be
   reloaded on: `/description/`, `/editorial/`, `/solutions/` and `/submissions/`. A reload lands on
   the same tab. A signed-out visitor opening `/submissions/` sees a sign-in prompt, not an empty
   list and not a not-found.
2. The statement renders paragraphs, lists, tables, fenced code in the monospace stack with no
   syntax colouring, inline mathematics with a fallback that does not shift the layout, labelled
   `Input`, `Output` and optional `Explanation` example blocks, and a constraints list. It carries no
   image element of any kind; any diagram is drawn inline.
3. Below the statement sit the topic tags behind a `Topics` disclosure that is closed by default,
   the employer tags behind the entitlement and a second disclosure, one disclosure per hint, a
   metadata strip carrying the accepted count, the submission count, the acceptance rate and a
   `Discussion` link with a count, and a like and dislike pair with counts.
4. **A closed spoiler disclosure is genuinely absent from what the server delivers.** For a problem
   the member has not solved, the topic tag names must not appear anywhere in the delivered markup
   of `/problems/<slug>/description/`. Opening the page source is not a way to read the answer. The
   same holds for the employer tags without an entitlement: they are omitted from the response, not
   present and hidden.
5. Above the wide breakpoint the workspace is two panes side by side with a draggable divider, the
   statement tabs on the left and the editor above a console on the right. Below it the panes become
   a two-tab switcher labelled `Problem` and `Code`. The divider position is remembered per member
   and per width tier, a double click restores the default, and the divider is reachable by keyboard
   as a separator carrying a value.
6. The workspace is the only route that suppresses the left rail and the footer, because both panes
   scroll independently and a footer under a split pane is unreachable.
7. The top bar on this route gains a problem navigator reading `<current> / <total>` with previous
   and next controls, over whatever list the member arrived from. That list context is carried in
   the query string so that a reload keeps it.

### The editor, drafts and the console

1. The editor offers the languages the problem has a signature for. This build offers `python3` and
   `javascript`, and a run or a submission in any other language is rejected as invalid input. The
   editor provides syntax colouring from a grammar rather than a keyword list, line
   numbers with a fold marker on any line that opens a block, bracket matching with the closing
   character overtyped rather than duplicated, find and replace scoped to the buffer with a
   regular-expression mode, a size control, a soft-wrap toggle that is off by default because a
   solution's line length is meaningful, and per-language indentation, so pressing return after a
   line that opens a block in `python3` indents the next line by four spaces.
2. **A draft is keyed by member, problem and language.** Switching from `python3` to `javascript`
   does not overwrite the `python3` draft, and switching back restores it exactly. Changing language
   three times and returning must produce the buffer that was left behind, character for character.
3. A signed-in member's draft is written through to the service. A signed-out visitor keeps a local
   draft only and cannot write one to the service, and on signing in that local draft is offered as a merge rather than silently
   uploaded or silently discarded. A draft is never what gets judged: what is judged is the buffer
   at the moment the control was pressed, carried in the submission.
4. The console carries three tabs, `Testcase`, `Result` and `Debugger`. `Testcase` shows the
   problem's example inputs as one editable field per parameter, typed from the problem's signature,
   so a parameter declared as an integer array refuses a bare string, and a run whose case gives a
   string for that parameter is rejected as invalid input. A member may add at most `10`
   custom cases per problem and they persist with the draft; a run carrying more is rejected as invalid input.
5. A custom case is **never used to judge**. It runs, its output is shown, and nothing is compared,
   because there is no expected value for it: its result carries the produced output and no expected
   value. A build that compares a custom run against a hidden
   case will tell members they are wrong when they are right.
6. `Debugger` is behind the entitlement and runs in the same sandbox under the same limits.
7. The toolbar carries, left to right, a language selector, `Reset`, `Format`, `Copy`, `Run`,
   `Submit`, `Notes` and `Timer`. `Timer` is a stopwatch, member-visible only. `Reset` destroys work
   and therefore confirms first.

### Run, submit and the judge

`Run` and `Submit` are two different operations. They share the sandbox and share nothing else.

| | `Run` | `Submit` |
|---|---|---|
| Who | anyone, signed in or not | a signed-in member |
| Cases | the problem's example cases plus the caller's custom cases | the full hidden set |
| Counters | none | the submission count, and the accepted count on success |
| Solved set | never | on `Accepted` |
| Contest | never scores | scores and penalises in a contest context |
| Output shown | everything, per case, produced and expected | only what the revelation rule allows |
| Idempotency | not required | required: a submission without an `Idempotency-Key` is rejected as invalid input |

1. Admission happens at intake and performs its checks before anything is written: the session, the
   problem exists and is published, the member is entitled if it is premium, the contest context, the
   language is offered, and the source is within `64KB`. **Nothing is written until every one of them
   has passed.** A gated problem submitted by an unentitled member is **refused as payment-required**,
   and no submission row exists afterwards.
2. A submission in the context of a contest the member did not register for is **refused as
   forbidden**. The problems of a contest that has not started are not in the catalogue and are not
   served to anyone, so asking for them answers as not-found.
3. **Intake does not block on judging.** The call that accepts a submission returns promptly,
   carrying the submission identifier and the state `pending`, and it returns before the program has
   run. The page asks for the verdict again until the submission is done.
4. A submission moves through `pending`, then `judging`, then `done`. Its verdict is one of exactly
   nine values and nothing else is ever stored in the field: `Accepted`, `Wrong Answer`,
   `Time Limit Exceeded`, `Memory Limit Exceeded`, `Runtime Error`, `Compile Error`,
   `Output Limit Exceeded`, `Internal Error`, `Rejected`.
5. Cases are run in their stored order and **judging stops at the first failure**, recording that
   case index. The same wrong program submitted twice must name the same case both times: a member
   cannot debug against a moving target.
6. The verdict is decided by what was observed, and these mappings are exact. Exited cleanly with
   matching output is `Accepted`. Exited cleanly with output that does not satisfy the comparator is
   `Wrong Answer`. **Exited cleanly having produced no output where output was required is
   `Wrong Answer`, not `Runtime Error`.** Stopped for exceeding the time limit is
   `Time Limit Exceeded`. Stopped for exceeding the memory limit is `Memory Limit Exceeded`, and
   that must be decided from what actually happened to the process rather than guessed from an exit
   code, so an out-of-memory stop is never reported as a crash. Exited non-zero for any other reason is `Runtime Error` with the captured standard error.
   Output past the byte cap is `Output Limit Exceeded`. A source the interpreter refuses to load, such
   as a `python3` syntax error, is `Compile Error` with the diagnostic reproduced verbatim and not truncated.
7. **The limit on the submitted program is enforced from outside it.** A timer, an alarm or a
   watchdog running inside the program cannot stop a program that blocks signals, spins without
   yielding or never returns control. Submitting a solution that loops forever must return
   `Time Limit Exceeded` within the judging deadline, and the request that asked for the verdict
   must answer.
8. A program that sleeps rather than computes is stopped by a wall-clock limit at three times the
   processor-time limit, so a solution that sleeps for thirty seconds settles as `Time Limit Exceeded`.
9. The base limit for a problem is `2000` ms of processor time and `262144` KB of memory. Every
   language carries a declared multiplier applied at execution: `javascript` is `2.0` and `python3`
   is `3.0`. The multiplier is part of the problem's public metadata and is shown to the member in
   the verdict when a time limit is hit. A build that applies one limit to every language has made
   the intended solution impossible in the slower one. A runtime that reserves a large address space
   at start and touches little of it still starts, because memory is judged on what the program held.
10. **Isolation.** The executing program has no route to the network, no route to this app's own HTTP
    surface and no route to the database, and nothing in its environment names a database, the member,
    the problem or the submission. Its working directory is discarded between every single case, so a file
    one case writes is not there for the next. A submitted program that tries to open a socket still
    receives a verdict, and no packet leaves.
11. A comparator is declared on every problem, reported in its public metadata as `comparator`, and never
    defaulted. `exact` compares the serialised answer. `numeric-tolerance` accepts a value within the
    declared absolute tolerance or within the declared relative tolerance, so `4. Median of Two Sorted
    Arrays` accepts a median off by `1e-7` and refuses one off by `0.1`. `unordered` is **multiset**
    equality at the top level, so `46. Permutations` accepts every ordering listed in any order and
    refuses an answer that lists one ordering twice. `unordered-deep` applies the same rule at every
    nested level, and `any-of` compares against a stored set of acceptable answers. **A floating-point
    value is never compared for equality anywhere in the product.**
12. What a failing verdict reveals is bounded. A failing example case reveals everything: input,
    expected and produced. A failing hidden case reveals the case index and the input, the expected
    output and the produced output each truncated to `1000` characters, with the truncation marked
    and the full input never available at any size. `Time Limit Exceeded` reveals the case index,
    the limit and the multiplier applied, never the input. `Memory Limit Exceeded` reveals the case
    index, the limit and the peak, never the input. `Runtime Error` reveals standard error truncated
    to `4KB` and the case index, never the input. No response of any kind carries a problem's hidden cases.
13. A submission carries an `Idempotency-Key` scoped to the member. A repeat with the same key and
    the same body returns the original submission and creates no second one. A repeat with the same
    key and a different body is rejected as a conflicting request. Separately, a submission whose
    source, problem and language match that member's immediately previous submission **within
    `10s`** is refused as a conflict with a message saying so, which catches a double press without
    catching a legitimate resubmission a minute later.
14. **Two accepted submissions for the same problem from the same member, arriving at the same
    moment, produce exactly one row in that member's solved set.** The solved set is the single
    source of progress truth and a problem appears in it at most once, whatever the concurrency. A
    submission that was not accepted adds nothing to the solved set, and the problem reads as attempted.
15. The acceptance figure shown on a row is the accepted count divided by the submission count,
    computed when it is read and rounded to one decimal place, never stored as a third number that
    can disagree with the two it comes from. The denominator counts submissions and not members. A
    practice submission moves the submission count by one and an accepted one moves the accepted count
    by one; a run moves neither.
16. Neither counter is maintained by reading a value into the application and writing it back, and
    the accepted count must never exceed the submission count under simultaneous submissions to one
    problem.
17. Submissions made in a contest context against a contest problem do not move that problem's public
    counters until the contest ends.
18. **Determinism.** The same source, against the same hidden cases, in the same language, must
    produce the same verdict and the same failing case every time, except where the member's own program is nondeterministic.

### Progress, the daily challenge and the streak

1. **A day is a calendar day in `UTC`, the same zone for every member on earth**, and never taken
   from the member's own clock. The member's zone is used to
   display an instant and never to decide which day it falls in. A day in the member's own zone is
   the considerate design and it is wrong here: the day's problem would be ambiguous for hours, a
   member who travels would gain or lose a day of streak, and a member who can choose their zone can
   extend a day they were about to lose.
2. The day's featured problem is authored in advance and scheduled. The catalogue pins it above the result set with a calendar mark,
   and the right rail shows a month grid with the current day filled, a `Day 1` label and a
   countdown to the end of the day in `UTC`, read to the second. `GET /api/problems/<slug>/daily` reports the
   current `UTC` day and the seconds left in it.
3. A day counts toward the streak when the member has an accepted submission first accepted within
   that day, on any problem and in any context.
4. The streak update is exact. With `d` the current day and `l` the last qualifying day: if `l`
   equals `d`, nothing changes; if `l` is the day before `d`, the current run increments by one; if
   `l` is earlier than that, the current run resets to one; if `l` is unset, the current run becomes one. The longest
   run is updated whenever the current run exceeds it, so the longest run is never below the current run.
5. **The streak advances by at most one on a given day, however many accepted submissions arrive and
   however close together.** A second accepted submission on the same day changes nothing, and two accepted
   submissions arriving in the same second on the first solve of a day must not increment it twice.
6. Coins are an append-only ledger of signed, non-zero deltas, each carrying one of the reasons
   `daily`, `streak_milestone`, `contest`, `redemption`, `purchase`, `adjustment` or `refund`, and a
   reference to whatever caused it. A balance is the sum of that ledger. **A redemption reads the balance and
   writes the debit as one indivisible act that fails if the balance moved, and a balance can never
   go negative**: a redemption larger than the balance is refused and leaves the balance unchanged, and
   two tabs redeeming the same coins must not both succeed.
7. An accepted submission records a runtime and a memory figure taken from the accepted run, and a
   percentile against the accepted submissions of other members on the same problem in the same
   language. A rejected verdict records neither.
8. A member's own submission history for a problem lives under the `Submissions` tab, newest first,
   each row carrying the verdict, the language, the runtime, the memory and the time. **Another
   member's history is not readable at all**, and asking for one of their submissions by identifier
   answers as if it does not exist.

### Learning and community

1. Study plans at `/studyplan/` are a featured row and then rows grouped by theme, each plan a card
   carrying a title, an item count and, for a signed-in member, a progress figure. The seeded plans
   are `Bytefold 75` at `/studyplan/bytefold-75/`, `Top Interview 150`, `SQL 50` subtitled `Crack SQL Interview in 50 Qs`, and
   `Introduction to Pandas` subtitled `Learn Basic Pandas in 15 Qs`, grouped under the headings
   `Cracking Coding Interview`, `Advanced Algorithms` and `Most Liked`. A plan detail route lists its problems in the authored order with the member's own
   status beside each.
2. **Plan progress is derived, never stored**: it is the count of the plan's problems that are in
   the member's solved set, over the plan's item count. Solving a problem from the catalogue advances
   every plan that contains it, without the member opening the plan.
3. Explore cards at `/explore/` are multi-chapter cards with a cover, a chapter count and an item
   count, each opening to an ordered chapter list. The seeded cards are `crash-course`, `beginners-guide` and
   `cheatsheet`, a crash course, a
   beginner's guide and a cheatsheet, each carrying a two-line excerpt that clamps rather than
   reflowing the card. `cheatsheet` is premium: its chapter bodies are behind the
   entitlement while the card itself stays listed.
4. Discussion at `/discuss/` is a feed of at least `3` seeded posts with a category, a title, an author, a vote score, a
   view count and a reply count, shown as an upvote arrow with a count, an eye with a view count and
   a speech bubble with a reply count. The default order is `Best`; `Hot`, `Newest` and `Most Votes` are the other orders.
5. **A member has at most one vote on a target.** Voting again with the same direction removes the
   vote; voting the opposite direction replaces it, so an up-vote changed to a down-vote moves the score by `-2`. Two simultaneous votes from the same member on
   the same target leave exactly one vote and one score contribution.
6. A view count increments at most once per member per post per day, so reading a post a second time on
   the same day does not raise its count.
7. A solution post that contains a full answer is collapsed behind a spoiler control by default.

### Contests

1. A contest carries a title, a start instant and a duration (never a start and an end), a cadence of
   `weekly` or `biweekly`, four problems each with a score, and a state of `scheduled`, `running` or
   `finished`. `/contest/` shows the running contest, the upcoming pair with a countdown, then a ladder of ranked
   competitors, then the past contests each reading `0 / 4`.
2. Registration is open while a contest is `scheduled` or `running`. **A scheduled contest's problem
   list is not served before the window opens** to anyone, registered or not: asking for it
   answers as not-found.
3. A participant's score is the sum of the scores of the problems they solved, where a problem is
   solved if they have at least one `Accepted` submission in the contest context inside the window.
4. The scoring arithmetic is exact. A participant's penalty is summed **over solved problems
   only**, and for each such problem it is
   the elapsed seconds from the contest start to their first accepted submission for it, plus `300`
   seconds for each of their submissions for that problem inside the window that was not accepted
   and was made **before** the accepted one.
5. Three consequences follow and each is a rule in its own right. **Wrong submissions on a problem
   that was never solved contribute nothing at all**: eleven failures on a fourth problem they never
   solved add zero to the penalty. **Wrong submissions made after the accepted one contribute
   nothing**: a tidier version that fails after the solve is not penalised. A `Compile Error` does
   count as a wrong submission.
6. Standings are ordered by score descending, then penalty ascending, then the elapsed time of the
   participant's last accepted submission ascending, then their registration instant ascending, then
   their identifier ascending. The last key guarantees a total order, which is what makes the
   standings stable across repeated reads.
7. Standings live at their own address under the contest so that a rank is linkable without the
   problem list.
8. The ladder carries each competitor's rating and their attended count.

### The paid tier

1. `/subscribe/` shows two terms against a region price list. Every price is an integer of the
   currency's minor unit plus a currency code, and there is no floating-point value anywhere on the
   money path. The seeded `US` price list in `usd` is `3500` for the monthly term and `15900` for the
   yearly term, with a list price of `42000` on the yearly card; the cards read `$35.00`, `$159.00` and the struck `$420.00`.
2. The saving shown on the yearly card is computed from the pair rather than authored, and reads `62%`. The
   per-month figure on the yearly card is the annual amount divided by twelve and rounded to the
   currency's minor unit, `1325`, which reads `$13.25`. `usd` carries `100` minor units to the
   major unit.
3. A price is a time-bounded record with a start and an end, and a region may
   be priced and not available for sale: the `EU` list in `eur` at `3200` monthly and `14900` yearly is seeded and
   not available, and subscribing in `EU` is rejected as invalid input.
4. The entitlement gates the premium problems' statements, the premium explore cards' and study
   plans' bodies, the editorial bodies, the employer facet, the frequency histogram, the debugger,
   **autocomplete** (smart code autocompletion based on the chosen language, so a signature does not
   have to be memorised) and unlimited saved playgrounds with folders.
   The monthly card is plain and the yearly card is tinted warm, marked `Most Popular`, and carries
   the term billed yearly, the annual amount, the per-month figure and the strike price beside it.
   Subscribing completes inside the product against its own price list: no card form and no page on
   another origin.
5. **Gating is enforced at the service on every read, and a gated field is absent from the response
   rather than present and hidden**, because hiding a field in the page is information leakage with
   an extra step. The employer tags on a problem are never in the
   problem's public payload: adding them and hiding them in the page is the same as publishing them.
6. A gated read by a signed-in member without an entitlement is **refused as payment-required**,
   never as forbidden and never as not-found, because the padlock says plainly that the thing exists.
   **The catalogue row for a premium problem stays public**: its number, title, difficulty,
   acceptance and premium flag are served to everyone, and only the statement, the signature and the
   tests are not. A build that hides the row has broken the padlock the design depends on.
7. Subscribing takes effect on the next read without a full page reload: a statement refused as
   payment-required before subscribing is served on the very next request after it, and the previously cached
   unentitled list must not survive into the entitled view or leak into another account.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the marketing pitch, employer wall, embedded editor demonstration | public |
| `/problemset/` | the catalogue | public |
| `/problems/<slug>/description/` | statement, constraints, examples, editor | public |
| `/problems/<slug>/editorial/` | the authored walkthrough | public route, gated body |
| `/problems/<slug>/solutions/` | member-written solution posts | public |
| `/problems/<slug>/submissions/` | the member's own attempts on this problem | member |
| `/contest/` | running contest, upcoming pair, ladder, past contests | public |
| `/contest/<slug>/` | contest detail | public |
| `/contest/<slug>/ranking/` | standings | public |
| `/explore/` | learning cards | public |
| `/explore/<card>/` | card chapters | public |
| `/studyplan/` | featured and grouped plans | public |
| `/studyplan/<slug>/` | the plan's ordered items with progress | public |
| `/discuss/` | the discussion feed | public |
| `/discuss/post/<id>/` | a thread | public |
| `/subscribe/` | the two terms and the feature list | public |
| `/accounts/login/` | sign in | public |
| `/accounts/signup/` | register | public |
| `/list/` | the member's saved lists | member |
| `/quest/` | the guided track | member |
| `/playground/` | a saved scratch buffer | member |
| `/store/` | the coin store | member |
| `/store/redeem/` | coin redemption | member |
| `/interview/online-interview/` | the online interview surface | public |
| `/interview/assessment/` | the assessment surface | public |
| `/u/<username>/` | a public profile | public |
| `/privacy/`, `/terms/`, `/help/`, `/bug-bounty/`, `/download/` | the pages the footer names | public |

**Entry and redirects.** An unauthenticated request for a member-only route lands on
`/accounts/login/` carrying the intended path in a `next` query parameter, and signing in lands on that path rather than on a
dashboard. Signing out returns the visitor to the route they were on when it is public and to `/`
when it is not. A signed-in member without an
entitlement opening a gated body sees the padlocked affordance and the price, never a blank page and
never a not-found. An address that matches no route renders the product's own not-found page with a
way back.

**Journeys.**

1. **Filter and open.** Open `/problemset/`. Note the count shown beside `Dynamic Programming`. Tick
   `Medium`, tick `Dynamic Programming`, set status to `Unsolved`. The list's total matches the
   count that was shown beside `Dynamic Programming` before it was ticked, with the other axes
   applied. The address bar now carries every axis. Copy the address, open it signed out in a fresh
   session, and the same rows appear in the same order. Click `1. Two Sum` and arrive at
   `/problems/two-sum/description/`.
2. **Write and run.** Sign in as `member@example.com` with `deku-demo-pw-2026`. Choose `python3`,
   type a solution, switch the language selector to `javascript`, type something else, switch back.
   The `python3` buffer is exactly as it was left. Press `Run`. The console's `Result` tab shows
   every example case with its input, its expected output, the output produced and a pass mark.
3. **Submit and settle.** Press `Submit`. The verdict panel shows `pending`, then `judging`, then a
   single verdict and never two at once. On `Accepted` it shows the runtime, the memory and both
   percentiles; the `Submissions` tab lists the attempt newest first; the catalogue row carries the
   solved mark on the next visit; and the problem's acceptance figure has moved. Press `Submit`
   again immediately with the same source and the second press is refused as a conflict.
4. **The trap, deliberately.** Submit a solution that loops forever. Within the judging deadline the
   panel reads `Time Limit Exceeded` and names the case index, the limit and the multiplier for the
   chosen language, and the page is still usable.
5. **Contest.** Open `/contest/`, register for the scheduled contest, and confirm that its problems
   are not readable yet. Register for the running contest, submit a wrong solution to one of its
   problems in the contest context, then a right one, then a wrong one again. Open
   `/contest/<slug>/ranking/` and read a penalty that counts the first wrong submission and not the third.
6. **Streak.** Solve any problem. The calendar marks the day, the streak badge advances by one and the
   countdown continues to the end of the day. Solve another. Nothing changes.
7. **Subscribe.** Sign in as `subscriber@example.com` and open a premium problem: the statement
   renders and the employer facet returns results. Sign in as `member@example.com` and open the same
   problem: the row is there with its padlock, and the statement is refused as payment-required.

**States.** Every list has an empty state that names what would fill it and offers the action that
does: a filtered catalogue with no matches says so and offers to clear the narrowest facet; an
empty submission list invites a first attempt. Every page has a loading state, and the catalogue's
is a skeleton of rows at the row's own height so that nothing jumps when the data lands. An error
never blanks the page: the chrome stays, the failed region carries a message and a retry, and a
transient message announces it. A verdict panel shows exactly one verdict.

## UI/UX notes

The product is a working instrument used repeatedly by the same person, so it reads quiet, dense and
organised, and the marketing route is the single exception that carries atmosphere. The north star:
a solver opening the catalogue should understand within one screen which slice of the problem set is
theirs today, and a solver reading a verdict should understand within one line whether the machine
is telling them they were wrong, slow, greedy or unlucky. Comprehension over expression, everywhere
except the one route that has to sell.

**Two shells, and they are not variants of one another.** The marketing shell, on the root route
only, is a full-bleed single column of bands: a dark hero cut by a diagonal wedge, alternating
image-and-text bands, an embedded editor demonstration and a wall of employer marks. The application
shell, on every other route, is a fixed top bar with a left rail, a centre column and, at the widest
tier, a right rail of supplementary panels. A visitor who lands on the marketing route and presses
its primary action arrives inside the application shell without the change reading as a different
site.

**Palette by role.** The page ground behind cards is a near-white neutral and the card surfaces are
pure white in the light theme, across all three elevations. Primary text is a near-black neutral,
secondary text and timestamps are a mid neutral, and placeholders and disabled labels are a light
neutral. One hairline border value carries the entire product and it is the most frequent colour on
any screen. The brand mark, the paid-tier link and every earned or premium affordance wear
a mid, vivid orange, and nothing else on any page wears it.
The primary action is a mid, vivid blue and there is one of them per page. Difficulty is carried by
a mid, vivid teal for `Easy`, a mid, vivid amber for `Medium` and a mid, vivid red for `Hard`, and the word is always present beside the
colour, so difficulty is never signalled by colour alone. An accepted verdict is a mid, vivid green;
a warning is the same amber; a failure is the same red; and a pending or judging state is a mid
neutral, deliberately not red, because a fault of the platform is not the member's failure and must
not be dressed as one. Badges, streak flames and event ribbons draw on five accents: a light, vivid
green, a deep, soft indigo, a light, vivid red, a light, vivid cyan and a light, vivid amber. The
component palette reaches only these semantic roles; the underlying blue, green, teal, amber, red,
violet and magenta ramps are not addressed directly by any component. The exact shades are yours, so
long as each role keeps its exclusivity and its meaning.

**Two themes ship.** Light and dark, switched instantly, remembered per member, and following the
operating system preference until the member overrides it. The dark theme is not a filter over the
light one: every role has an independently authored dark value, and the dark theme darkens the ground
rather than the shadow.

**Contrast is a requirement, not a preference.** Every route meets WCAG AA contrast in both themes.
The difficulty label is the known risk, because it is set small and semibold and two of its three
colours do not clear the small-text bar on white. Resolve all three the same way rather than fixing
the two that fail: put the label on a tinted chip in its own hue, or darken the ink of all three.
Shipping the measured colours at the measured size is the one thing this may not do.

**Typography.** The interface stack is `system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue",
Arial, sans-serif`. Code and the editor use `ui-monospace, SFMono-Regular, Menlo, Consolas,
"Liberation Mono", monospace`. Inline mathematics falls back to an italic serif without shifting the
layout. No font file ships. The scale: body text is `14px` on `21px`, dense rows `14px` on `20px`,
metadata and counts `12px` on `16px`, chips `14px` on `14px`, an emphasised row title `14px` at
weight `500` on `20px`, the difficulty label `12px` at weight `500` on `16px`, a statement body
`16px` on `24px`, card body `16px` on `22px`, card titles `18px` at weight `600` on `28px`, section
headings `24px` at weight `500` on `32px`, paid-tier headings `24px` at weight `600` on `30px`,
marketing body `16px` and the marketing lead `15px` on `28.5px`. Spacing is a four-step grid and
every gap, padding and radius sits on it. The whole application is built at
the body size: anything larger is a heading and anything smaller is metadata, and there is no third
register. Figures are tabular wherever amounts stack, so acceptance percentages, runtimes,
penalties and standings align on the decimal point down a column.

**Iconography and gradients.** Every icon is drawn inline as stroke geometry that takes its colour
from the text around it, at one consistent weight, on one consistent square, with round joins and
round caps; there is no icon font and no icon image. Two icon systems must not coexist: pick one
geometry and dress every glyph in it. Four gradients belong to the system and no more: a warm
amber-to-orange ribbon on an earned or premium badge, a faint left-to-right orange wash behind a
paid-tier row, the same wash anchored at the left edge, and a diagonal stripe on a progress bar.
Every learning-card cover is a two-stop vertical pair of a hue and a darker sibling of the same hue,
repeated at a low alpha for the card's resting state. No gradient is a photograph and no gradient
carries information on its own.

**Shape, density, elevation.** Buttons, rows and inputs carry a small, near-square softness. Pills,
chips, the search field and the avatar are fully round. The learning cards are softer, and each is
one visual object built from a head and a foot with complementary corners so that the play control
can overhang the seam. Density is compact in the application shell: rows sit tight so that a full
page of results fits with minimal scrolling, and the marketing shell alone is spacious. Elevation is
three steps, a resting card lift, a hover lift and a modal lift, with the contest ladder row carrying
its own deeper, cooler lift.

**Motion.** One easing curve carries the application shell and there is no second one. Three lengths
and no fourth: a very short one for anything that only changes colour, background, border or
opacity; a slightly longer one for a transform on a control the pointer is already over; a longer one
for anything that changes size, position or panel state. A group staggers by index in two steps,
never by a delay computed per child. The marketing shell keeps its own separate curve family and must
not be unified with the application shell by accident. **The build names the properties it animates**:
asking the browser to transition every property is what makes a box that has just gained a line of
text slide instead of appearing.

Seven moments are named and each is built. The **skeleton breath** is a slow pulse on placeholder
rows while the catalogue loads, and a horizontal shimmer travels across a skeleton block for content
that has not arrived yet. The **topic rail expanding** moves height, position and transform
together as the hidden rows of chips arrive. The **contest ladder entrance** is the product's only
piece of choreography: rows arrive in index order, each popping in with a blur that resolves, its
inner content fading up a beat behind it and its trailing link a beat behind that, then a single
longer settle reserved for this row and nothing else. The **reward badge** arrives past its resting
size and returns. The **toast** rises from below and overshoots once on arrival, then leaves
on opacity alone; it holds for a few seconds when it is informational and until it is dismissed when
it is an error; at most three stack and a fourth replaces the oldest. The **floating card**
drifts slowly and endlessly on one marketing band. The **theme cross-fade** is symmetric and is the
one place the two themes meet.

Under a reduced-motion preference every endless animation stops, including the skeleton breath and
the marketing drifts; the ladder rows appear in order on opacity alone with no pop; transient
messages fade rather than overshoot; colour and opacity transitions survive, because they carry
meaning and move nothing; and nothing that communicates state is animation-only.

**Components.** Every control has a resting, pointed-at, pressed, focused and unavailable state, and
unavailable is never signalled by colour alone. Focus is always visible. `Escape` closes the topmost
overlay and only then leaves the editor. Destructive actions confirm first, which is why `Reset` asks
before it discards a buffer. Validation is inline: a form names the field that is wrong, says what
would be valid, and writes nothing when it rejects. Creating a saved list opens in a modal that traps focus while it is open and
returns focus to the control that opened it when it closes.

**One primary action leads each page**, visually distinct from every secondary one and never
competing with a second: the marketing hero's single call to action, the catalogue's search field,
the workspace's `Submit`, the pricing route's chosen term. A page with two equally weighted primary
actions has told the reader nothing about what to do next.

**Layout, width and touch.** The layout archetype is a top navigation bar. The catalogue, explore and
study-plan routes carry the left rail; the contest, discussion and pricing routes do not; the
workspace suppresses both the rail and the footer. Four width tiers, and the arrangement holds at
every width between them. At the narrowest, the rail becomes a drawer behind a menu control, the top
bar keeps only the mark, the search field and the account slot, the catalogue row drops its frequency
column, the workspace becomes a two-tab switcher, the price cards stack and the card rails become
one-and-a-half cards wide with a snap. On the tablet tier the rail returns as an icon-only strip and
the contest pair stacks. On the desktop tier the rail returns with its labels and the workspace
splits into two panes. At the widest, the right rails appear and the main column stops growing and
centres. Nothing overflows sideways at a narrow viewport and every navigation target stays reachable
there.

**A panel that disappears at a boundary gains an entry point in the main column**, or it has been
quietly deleted from the product for everyone on a phone: the daily calendar and streak become a
compact streak chip in the control row that opens the calendar in a sheet, the employer chips become
an `Employers` facet inside the filter control, and the discussion digest becomes a `Topics` control
above the feed. Every hit target is comfortably sized in both axes on the narrowest tier, including
the row's status glyph. The topic rail scrolls horizontally with momentum, snaps to
chip boundaries and fades at both ends.

**Accessibility.** The catalogue is a table with a header row because its columns have meanings, and
a sortable header carries its sort state. The status tick is named `Solved` and its absence is named
nothing at all, so that someone listening to hundreds of rows hears the exception rather than the
rule. Facet controls are grouped and named, the topic chips as a multi-select group and the category
pills as a single-select group. The result count is announced politely on every filter change, and
the pager marks the current page as current rather than merely styling it. The workspace split is two
labelled regions and the divider is a separator carrying a value, a minimum and a maximum with
arrow-key support. The editor is a labelled multi-line text control in which `Tab` inserts an indent
while focus is inside and `Escape` then `Tab` leaves, and that escape sequence is stated in the
editor's own description, because an undiscoverable escape is the same as none. Line numbers are
decorative and are not read. The console's three tabs are a tab list, the result panel is a live
region, and the failing-case block is named with its case index. Announcements are graded by politeness: a filter change and its
new count, a run starting and a submission being queued, and an informational toast are polite; a
verdict and a rate-limit refusal and an error toast are assertive; a saved draft is announced not at
all, because it is not news. The contest countdown is a named timer that updates
far less often for assistive technology than it updates on screen. Full keyboard navigation reaches every control, and a shortcut sheet lists the chords: `/`
focuses the global search, `g` then `p` opens the catalogue, `g` then `c` opens contests, the
platform modifier with `Enter` runs, the modifier with `Shift` and `Enter` submits, `[` and `]` move
through the current list context, and `?` opens the sheet, which is also reachable from the account
menu.

**What this must not look like.** Not a page dominated by a single hue family with no second signal.
Not decoration standing in for content. Not a marketing composition where the working instrument
belongs: the hero lives on one route and the catalogue is a tool.

## Technical requirements

The stack is a server-rendered multi-page application. The backend is NestJS with Handlebars
templates; the browser layer is HTMX over those same server-rendered templates. Every screen is
composed on the server and delivered as HTML, so the browser receives a painted document on the
first request rather than an empty root element that then fetches its own data: the catalogue's first
response already carries its rows. Interactive fragments
(the facet rail recomputing its counts, the verdict panel arriving, the console switching tabs, the
create-list modal) are server-rendered fragments swapped into the page in place, requested by the `hx-`
attributes the markup carries. Data lives in
**PostgreSQL**, reached at `DATABASE_URL`. The app's public origin and port come from
`APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Read every one of these from the environment and never
hardcode a host or a port.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database,
cache, queue, object store, identity provider or mail vendor: the only backing service available in
this environment is **PostgreSQL**, and reaching for anything else is a contract violation.
PostgreSQL is already running and reachable at `DATABASE_URL`. Do not download, install, compile or
start a copy of it: the catalogue, the members and the submissions live in that running database.

`GET /api/health` returns `200` once the app holds a database connection and its seed has completed.
Every response carries an `X-Correlation-Id` header, and a failure's `trace` field carries the same
value, so that a member reporting a fault by its reference can be traced.

The part of the system that executes a member's submitted program is separated from the part that
knows about members. The executing side is handed a source file, a set of cases and a set of limits,
and returns an exit status, the bytes produced and the resources consumed. It holds no database
credential, has no route to this app's own HTTP surface, and carries nothing in its environment
naming the member, the problem, the submission or the infrastructure. The stopping of a program that
exceeds its limits is performed by something outside that program, because a program can ignore any
alarm set inside it. The working area is discarded between every case so that nothing one run leaves
behind is reachable by the next.

Accepting a submission and running it are separated in time. The request that accepts a submission
records it and answers; the program runs afterwards; the verdict is attached to the recorded
submission when it is known.

Publicly identical payloads (a catalogue row, a problem statement, a facet count) and per-member
payloads (a status overlay, a streak, a draft) are answered separately, so that a response computed
for one member can never reach another. A publicly identical payload may be cached and shared;
anything that varies by member may not be, and the two are never assembled into one response.

Every list response carries the total count where it is cheap to know, the page size and the cursor
for the next page or a null. Every read accepts a `fields` parameter, a comma-separated list in which
a leading `+` adds to the default set and a bare list replaces it: `GET /api/problems?fields=+category`
adds `category` to every row, and `fields=number,slug` returns rows carrying `number` and `slug` and none
of the other default fields. Every mutating request accepts an `Idempotency-Key` header.

Every failure answers in one shape, always: a `type` drawn from `invalid_data`, `not_found`,
`not_allowed`, `unauthorized`, `conflict`, `payment_required`, `unexpected_state`, `rate_limited` or
`judge_unavailable`; a `message` that is safe to show a member and is never a stack trace; a stable
machine-readable `code`; optional field-level `details` for invalid input; and a `trace` carrying the
correlation identifier, always present. The status and the `type` travel together: `400` is
`invalid_data`, `401` is `unauthorized`, `402` is `payment_required`, `403` is `not_allowed`, `404` is
`not_found` and `409` is `conflict`.

Every public route carries its own title and description and declares a social preview title and a
social preview image, and the image resolves from this app's own origin. No two routes share a title
and no two share a description. The site serves a favicon and declares it in the document head. Every
asset the browser fetches comes from this origin: no font file, no image file, no icon font and no
script is fetched from anywhere else, and no credential, API key or admin token appears in anything
the browser downloads. The served pages carry no development tooling, such as a hot-reload client.

No binary file of any kind ships. **Zero-asset substitution is the rule**: every mark, glyph,
illustration, employer logo and avatar monogram is drawn inline as vector geometry or composed from
styles, including the favicon and the social preview image, both of which are served as vector
documents from this origin. An avatar is a monogram of the member's initials on a ground derived
from their name, so that the same member always gets the same one. Stylesheets transition named
properties only and never `all`.

All timestamps are UTC. Every duration is stored as an integer of its smallest unit: milliseconds for
runtimes, seconds for contest windows and penalties. Money is an integer
of the currency's minor unit with its currency code beside it. An instant crosses the API as an ISO 8601
UTC string and a calendar day as `YYYY-MM-DD`.

## Data model

Twenty-four tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**members.** `id`, opaque and sortable by creation; `email` unique on the normalised form, which
lowercases the domain and preserves the local part exactly; `username` unique case-insensitively and
after confusable folding; `display_name`; `password_hash`;
`state` from `unverified`, `active`, `restricted`, `locked`, `deleted`; `region`; `theme`;
`created_at`.

**sessions.** `id`, `member_id`, `created_at`, `last_seen_at`, `device_label` and `revoked_at`. The
state lives here, on the server, so that ending a session takes effect at once.

**problems.** An opaque `id`, which is the only thing anything else references; `number`, an integer
unique among published problems and display only; `slug`, lowercase kebab, unique and immutable once
published; `title`; `difficulty` from `easy`, `medium`, `hard`; `category` from `algorithms`,
`database`, `shell`, `concurrency`, `javascript`, `pandas`; `statement`, `constraints`, `examples`
and `hints`; `is_premium`; `state` from `draft`, `published`, `withdrawn`;
`published_at`; `accepted_count`; `submission_count`; `like_count`; `dislike_count`;
`test_set_version`. **`difficulty` is authored and is never derived from the acceptance rate**: the
seed contains a `Hard` problem accepted by two thirds of attempts and a `Med.` problem accepted by a
fifth, and both are correct. **`number` is not a key and nothing references it**: a submission refers
to its problem by `problem_id`, never by number.

**tags** and **problem_tags.** A tag carries `id`, `slug`, `name` (`Heap (Priority Queue)` is a real
name and parentheses are legal), `kind` of `topic` or `employer`, and a `problem_count`. The join
carries `problem_id`, `tag_id` and, for an employer tag, a `frequency` bucket from `1` to `5`.

**problem_signatures.** One row per problem per language, carrying `problem_id`, `language`, `starter`
exactly as the editor opens it including its comments, an `entry_point` naming the symbol the harness
calls, the `imports` preamble for that language, an ordered `parameters` list of name and type, a
`returns` type, `mutates` as the ordered list of parameter positions to read back after the call, and
`indent`. Parameter and return types are drawn from one vocabulary: `int`, `double`, `bool`, `string`,
`char`, `array<T>`, `list-node`, `tree-node` and `graph-node`. A signature is a separate row from the problem.

**test_sets** and **test_cases.** A test set carries `problem_id`, `version`, a `comparator`, an
absolute and a relative tolerance where the comparator needs them, a `time_limit_ms`, a
`memory_limit_kb` and an `output_limit_bytes` defaulting to `65536`. A case carries `test_set_id`, an
`index`, an `input`, an `expected` value and an `is_example` flag. **The test set is readable only by
the judging path.** It is in no response and in no publicly shared payload; the only route from a test
case to a member is the bounded revelation in a verdict.

**submissions.** `id` opaque and sortable, carrying no member information because it appears in
shared links; `member_id`; `problem_id`; `language`; `source` stored verbatim and capped at `64KB`;
`source_hash`; `test_set_version`; `context` of `practice` or `contest:<slug>`;
`state` from `pending`, `judging`, `done`, `failed`; `verdict`, null until done;
`failed_case_index`; `runtime_ms` and `memory_kb`, null unless accepted; `runtime_percentile` and
`memory_percentile`; `attempt`; `idempotency_key` unique per member; `created_at` and `judged_at`.

**run_requests.** The same shape for an unscored run, touching no counter and no solved set.

**solved_set** and **attempted_set.** One row per member per problem, carrying `member_id`,
`problem_id` and `first_accepted_at` or `first_attempted_at`. The solved set is the single source of
progress truth, and **a member has at most one row per problem in it even when two accepted
submissions land at the same instant**.

**streaks.** `member_id`, `current`, `longest` and `last_qualifying_day`, stored as a date in `UTC`
rather than as an instant.

**drafts.** `member_id`, `problem_id`, `language`, `body`, `version` and `updated_at`. **A member
has at most one draft per problem per language**, and writing from two tabs leaves one row whose
content is one of the two writes and never a blend of both.

**study_plans** and **study_plan_items.** A plan carries `slug`, `title`, `group`, `is_featured`,
`is_premium` and `position`; an item carries `plan_id`, `problem_id` and `position`. Progress is derived
by intersecting the plan's items with the member's solved set and is never stored.

**contests**, **contest_problems** and **participations.** A contest carries `slug`, `title`,
`starts_at`, `duration_seconds`, a `cadence` of `weekly` or `biweekly` and a `state` from `scheduled`,
`running`, `finished`, and no end column. A contest problem carries `contest_id`, `problem_id`,
`position` and `score`. A participation carries `contest_id`, `member_id`, `registered_at`, `score`,
`penalty` and `rank`, and there is **at most one participation per member per contest** even under
simultaneous registration attempts.

**prices** and **entitlements.** A price carries a `plan` of `monthly` or `yearly`, `region`,
`currency`, `amount_minor`, `list_amount_minor`, `available`, `effective_from` and `effective_to`; it
is a time-bounded record rather than an edited field. An entitlement carries `member_id`, `plan`,
`region`, `currency`, `amount_minor`, `period_start`, `period_end` and a `state` from `active`,
`canceled`, `expired`, and **a member has at most one active entitlement** however many times the
subscribe action is pressed.

**posts** and **votes.** A post carries `id`, `member_id`, `problem_id`, a `kind` of `discussion` or
`solution`, `language`, `title`, `body`, `view_count`, `state` and `created_at`. A vote carries
`member_id`, `target_id` and a `value` of `-1` or `1`, and **a member has at most one vote per
target** even when two votes arrive together.

**coin_ledger.** Append-only: `member_id`, `sequence`, a signed non-zero `delta`, a `reason` from `daily`,
`streak_milestone`, `contest`, `redemption`, `purchase`, `adjustment`, `refund`, a `reference` to the
cause and `created_at`. A balance is the sum of the ledger and **can never be negative**: two
redemptions of the same coins arriving together must not both succeed.

**Seed data.** Three accounts as listed in `## User roles`. 240 published problems. The first thirty
carry these numbers, titles, difficulties and acceptance figures exactly: `3568. Minimum Moves to
Clean the Classroom` `47.4%` `Med.`; `1. Two Sum` `58.1%` `Easy`; `2. Add Two Numbers` `49.2%`
`Med.`; `3. Longest Substring Without Repeating Characters` `39.9%` `Med.`;
`4. Median of Two Sorted Arrays` `47.5%` `Hard`; `5. Longest Palindromic Substring` `38.6%` `Med.`; `6. Zigzag Conversion`
`55.0%` `Med.`; `7. Reverse Integer` `32.4%` `Med.`; `8. String to Integer (atoi)` `21.7%` `Med.`;
`9. Palindrome Number` `60.9%` `Easy`; `37. Sudoku Solver` `65.6%` `Hard`; `38. Count and Say`;
`39. Combination Sum`; `40. Combination Sum II`; `41. First Missing Positive` `43.6%` `Hard`;
`42. Trapping Rain Water` `68.1%` `Hard`; `43. Multiply Strings`; `44. Wildcard Matching` `32.7%`
`Hard`; `45. Jump Game II`; `46. Permutations`; `47. Permutations II`; `48. Rotate Image`;
`49. Group Anagrams`; `50. Pow(x, n)`; `51. N-Queens` `76.4%` `Hard`; `52. N-Queens II` `79.3%`
`Hard`; `53. Maximum Subarray`; `54. Spiral Matrix`; `55. Jump Game`; `56. Merge Intervals`. The
remaining problems are generated with numbers that do not collide, spread across the six categories
and the topic tags so that every category and every topic tag carries at least one problem. Exactly one problem in each difficulty band is
premium. `3568. Minimum Moves to Clean the Classroom` is the day's featured problem and is pinned.

Forty-seven topic tags are seeded by name: `Array`, `String`, `Hash Table`, `Math`, `Dynamic
Programming`, `Sorting`, `Greedy`, `Depth-First Search`, `Binary Search`, `Database`, `Bit
Manipulation`, `Matrix`, `Prefix Sum`, `Tree`, `Two Pointers`, `Breadth-First Search`, `Heap
(Priority Queue)`, `Simulation`, `Counting`, `Graph Theory`, `Binary Tree`, `Stack`, `Sliding
Window`, `Enumeration`, `Design`, `Backtracking`, `Number Theory`, `Union-Find`, `Segment Tree`,
`Linked List`, `Ordered Set`, `Monotonic Stack`, `Divide and Conquer`, `Combinatorics`, `Trie`,
`Queue`, `Bitmask`, `Recursion`, `Binary Indexed Tree`, `Geometry`, `Hash Function`, `Memoization`,
`Binary Search Tree`, `Shortest Path`, `Topological Sort`, `String Matching`, `Rolling Hash`. Their
counts are derived from the seeded catalogue rather than authored. `1. Two Sum` is tagged `Array` and
`Hash Table`.

Every published problem carries a signature in both `python3` and `javascript`, at least `10` test
cases, at least one example case, and an explicitly declared comparator.

**`1. Two Sum` carries a pinned signature, so its solution shape is fixed.** In both languages its
entry point takes exactly two parameters, `nums` of type `array<int>` and `target` of type `int`, and
returns an `array<int>` of the two zero-based indices whose values add to `target`, smaller
index first. Its `mutates` list is empty and its comparator is `exact`. Its hidden cases each have
exactly one answer, and at least one of them has more than four values in `nums`.

Two further signatures are pinned so the comparators are observable. `4. Median of Two Sorted Arrays`
takes `nums1` and `nums2`, both `array<int>`, returns a `double`, and declares `numeric-tolerance`
with an absolute tolerance of `1e-5`. `46. Permutations` takes `nums` of type `array<int>` holding
distinct values, returns an `array<array<int>>` listing every ordering of them, and declares
`unordered`.

Three contests are seeded. `weekly-contest-431` is finished and carries four catalogue problems.
`weekly-contest-432` is scheduled and carries four problems of its own that are not in the catalogue.
`biweekly-contest-150` starts when the app first starts, runs for `14` days, and carries `1. Two Sum`
scored `3`, `2. Add Two Numbers` scored `4`, `4. Median of Two Sorted Arrays` scored `5` and
`37. Sudoku Solver` scored `6`. Those four carry the slugs `two-sum`, `add-two-numbers`,
`median-of-two-sorted-arrays` and `sudoku-solver`, and `46. Permutations` carries `permutations`.

Four study plans are seeded: `Bytefold 75` with slug `bytefold-75`, `Top Interview 150` with slug
`top-interview-150` and premium, `SQL 50` and `Introduction to Pandas`. `Bytefold 75` includes
`1. Two Sum`. Three explore cards are seeded
with slugs `crash-course`, `beginners-guide` and `cheatsheet`, the last premium. At least `3`
discussion posts are seeded, one of them a `solution` post on `1. Two Sum` carrying a full
answer. The `US` price list in `usd` carries `3500` monthly and `15900` yearly
against a `42000` list price and is available; the `EU` list in `eur` carries `3200` and `14900` and
is not available. `subscriber@example.com` holds an active yearly entitlement in region `US`.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- Single tenant. There is no organisation, no team and no workspace boundary above the member.
- No native or mobile application ships; the footer's download page is a page of this product.
- No external payment processor, no card, no invoice, no refund flow. The subscribe action grants the
  entitlement against the product's own price list.
- No outbound mail of any kind. Verification is completed inside the product.
- No file upload, no object store, no user-supplied image. Avatars are drawn monograms.
- No third-party analytics collector, no performance agent, no bot-challenge service, no captcha and
  no federated identity provider.
- No operator console and no impersonation: `/admin/` answers not-found.
- No compiled languages: the offered set is `python3` and `javascript` and nothing else.
- No external network call at run time from any part of the product, including from a submitted
  program.
- The product must stay responsive at 240 published problems, 47 topic tags, six categories and tens
  of thousands of submissions across all members.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
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
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Field names are exact. A list endpoint returns a top-level JSON array or an object
carrying one. A successful call returns the named resource or shape; an invalid or unauthorized call
is rejected as a client error, never as a server error and never as a silent success. Bearer auth is
required on everything except login, registration, sign-out, health, a run, and the public reads a
signed-out visitor is allowed. Every response carries an `X-Correlation-Id` header. On the catalogue,
`topics` and `employers` take comma-separated tag slugs, `difficulty` takes comma-separated `Easy`,
`Medium` and `Hard`, `order` is one of `number`, `acceptance`, `difficulty`, `frequency` and `title`, and
`after` is the opaque `next_cursor` of the previous page. The status overlay's `ids` are problem `id`
values. The standings take the last `rank` read as `after`. A draft write carries the `version` last
read, `0` for a new draft. A problem read accepts `fields=+topic_tags` and `fields=+employer_tags`.
A verdict's `reveal` is an object carrying `case_index` and, only where the revelation rule allows,
`input`, `expected`, `produced`, `stderr`, `diagnostic`, `limit`, `multiplier` and `peak_kb`.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/register` | `{email, username, password}` | `{member_id, username, state}` |
| `POST /api/auth/login` | `{email, password}` | `{access_token, member_id, username, state}` |
| `POST /api/auth/logout` | none | `{ok}` |
| `POST /api/auth/verify` | none | `{member_id, state}` |
| `GET /api/sessions` | none | `[{id, device_label, last_seen_at, current}]` |
| `DELETE /api/sessions/<id>` | none | `{ok}` |
| `GET /api/me` | none | `{member_id, username, state, entitlement}` where `entitlement` is `{plan, region, currency, state, period_end}` or null |
| `GET /api/problems` | `category, topics, difficulty, status, employers, search, order, after, limit` | `{count, limit, next_cursor, pinned, rows[]}` where a row is `{id, number, slug, title, difficulty, acceptance_rate, is_premium, frequency_bucket}` |
| `GET /api/problems/facets` | the same query | `{categories[], topics[], difficulty[], employers[]}`, each entry `{value, count}` where `value` is the category value, the tag slug or the difficulty word |
| `GET /api/problems/status` | `ids` | `[{problem_id, status}]` where status is `solved`, `attempted` or `unsolved` |
| `GET /api/problems/<slug>` | none | `{id, number, slug, title, difficulty, category, statement, constraints[], examples[], hints[], is_premium, accepted_count, submission_count, like_count, dislike_count, comparator, time_limit_ms, memory_limit_kb, multipliers, topic_tags[]}` where `multipliers` is an object keyed by language with `topic_tags` present only when asked for and `employer_tags` present only with an entitlement |
| `GET /api/problems/<slug>/signature` | `language` | `{language, starter, entry_point, parameters[], returns, mutates[], indent}` where a parameter is `{name, type}` |
| `GET /api/problems/<slug>/daily` | none | `{is_daily, day, seconds_remaining}` |
| `POST /api/problems/<slug>/run` | `{language, source, cases[]}` where a case is an object keyed by parameter name, such as `{"nums": [2, 7], "target": 9}` | `{run_id, results[]}` where a result is `{index, kind, input, expected, produced, passed, stderr}`, `kind` is `example` or `custom`, and a `custom` result carries `expected` and `passed` as null |
| `POST /api/submissions` | `{problem_slug, language, source, context}` with `context` of `practice` or `contest:<slug>`, and an `Idempotency-Key` header | `{submission_id, state}` with `state` of `pending` |
| `GET /api/submissions/<id>` | none | `{submission_id, problem_slug, language, state, verdict, failed_case_index, runtime_ms, memory_kb, runtime_percentile, memory_percentile, reveal, created_at, judged_at}` |
| `GET /api/submissions` | `problem, limit, after` | the caller's own submissions, newest first |
| `GET /api/drafts/<slug>` | `language` | `{problem_slug, language, body, version}` |
| `PUT /api/drafts/<slug>` | `{language, body, version}` | `{problem_slug, language, version}` |
| `GET /api/streak` | none | `{current, longest, last_qualifying_day}` |
| `GET /api/coins` | none | `{balance, entries[]}` |
| `POST /api/coins/redeem` | `{amount, reference}` | `{balance}` |
| `GET /api/studyplans` | none | `[{slug, title, group, is_featured, is_premium, item_count, solved_count}]` |
| `GET /api/studyplans/<slug>` | none | `{slug, title, items[], item_count, solved_count}` where an item is `{position, slug, title, difficulty, status}` |
| `GET /api/contests` | none | `{running[], upcoming[], past[], ladder[]}` where a contest entry is `{slug, title, starts_at, duration_seconds, cadence, state}` |
| `GET /api/contests/<slug>/problems` | none | `[{position, slug, title, score}]`, not-found before the window opens |
| `POST /api/contests/<slug>/register` | none, with an `Idempotency-Key` header | `{contest_slug, registered_at}` |
| `GET /api/contests/<slug>/ranking` | `limit, after` | `[{rank, username, score, penalty, solved[]}]` |
| `GET /api/prices` | `region` | `[{plan, region, currency, amount_minor, list_amount_minor, available, effective_from, effective_to}]` |
| `POST /api/subscribe` | `{plan, region}` and an `Idempotency-Key` header | `{plan, region, currency, amount_minor, period_start, period_end, state}` |
| `GET /api/posts` | `category, problem, order, limit, after` | `[{id, title, category, author, score, view_count, reply_count}]` |
| `GET /api/posts/<id>` | none | `{id, title, body, category, author, score, view_count, reply_count}` |
| `POST /api/posts/<id>/vote` | `{value}` | `{target_id, score, my_vote}` |
| `GET /api/health` | none | `{status}` |

**No mocks.** The judge is the fact. An in-memory list of verdicts the app returns to itself, a
hardcoded `Accepted` for a source that was never executed, a comparison performed against an
expected value the page already held, a time limit implemented as a delay rather than as a program
being stopped, and a solved set written without a submission having been judged are all violations.
The submitted program is really executed, really bounded, and really compared against cases the page
never sent; the app's UI and its own tables can only reflect what actually ran, never substitute for
it.

## Definition of done

A visitor can narrow 240 problems to one slice, open a problem, write a solution, submit it, and
read a verdict computed from cases they were never shown, with a runtime and a percentile beside it.
A solution that never terminates comes back as `Time Limit Exceeded` inside the deadline. A member's
solved count and streak move once on a first solve and never again, and no member can reach another
member's submissions or drafts. A premium problem shows its padlocked row to everyone while its
statement reaches only a subscriber.
