# Flowmark

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser,
read the plans, search the node catalogue, sign in as an operator, start a run of a
workflow, watch it queue, dispatch to a worker and stop at a human approval step,
then sign in as an approver and resume it to completion, without hitting an error
page. A different stranger, holding only an operator session, must NOT be able to
decide that approval by any means: the decision must be refused by the server and
the run must still be waiting afterwards, with no approval recorded against it. A
credential's stored value must never come back out of any endpoint, to anyone,
including the person who typed it in; a field the interface shows as filled is not
the same thing as a value the interface will hand back.

## Overview

Flowmark is two things shipping together.

The first is a public marketing site: a dark, wide-format product site of thirteen
routes that sells the platform to technical operations teams. It carries a
scroll-driven home route, a four-tier pricing table priced on monthly workflow
executions rather than on steps or seats, a faceted catalogue of connector
listings with a real search, a case-study family, a comparison hub, and a footer
that glows warm from its left edge. Every route is composed from typed content
records rather than written into templates.

The second is the product itself: a workflow orchestration engine. An operator
draws a directed graph of steps on a canvas, binds credentials to the steps that
need them, and activates it. Something starts a run. The engine walks the graph,
hands each step its predecessor's output, pauses where a person has to approve, and
resumes when they decide. A run may outlive the process that started it, so a run
paused for a person holds no worker at all.

The audience is technical: IT operations, security operations, developer
operations, sales and support, addressed by name on the home route. The reader is
assumed able to read a node graph, and the site shows them one inside the first
screen and a half rather than explaining what one is.

Three non-goals, stated so nobody builds them: no marketing route renders a live
run, and the canvas in a product still is a picture on the site and an application
in the console. The catalogue lists connectors; it does not configure them. There is no
public signup, no payment capture, no native application, no comment thread and no
direct messaging.

The genuinely hard part is that a run must be able to stop for a person and start
again somewhere else: the engine has to write down everything about where it got
to, release its worker completely, and be picked up later by a different worker
from exactly that point.

## User roles

Everything a customer owns belongs to a **project**, never directly to a person, so
somebody leaving is a membership change rather than a data migration. Three roles,
scoped by project membership.

| Role | Can read | Can write |
|---|---|---|
| `operator` | workflows, versions, runs and step output in projects they belong to; the credential list as names and types only | create and rename workflows, add and remove steps, save a version, start a manual run, cancel a run they started, annotate a run |
| `approver` | everything an operator can read, in projects they belong to | everything an operator can write, plus decide a run that is waiting, inside a project they belong to |
| `owner` | everything above in every project, plus the audit stream and the member list | everything above, plus create and revoke credentials, bind a credential to a step, add and remove members, change a member's project role, transfer a project |

- An `operator` **cannot** decide an approval, **cannot** create or bind a
  credential, **cannot** add or remove a member, and **cannot** read the audit
  stream.
- An `approver` **cannot** decide a run in a project they do not belong to,
  **cannot** create or bind a credential, and **cannot** change membership.
- An `owner` **cannot** read a stored credential value. Nobody can, at any
  privilege, through any interface.
- Nobody, at any role, can read or write anything in a project they do not belong
  to. An `owner` belongs to every project.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from an `operator`
session to any `approver`-only endpoint must be rejected by the server (an
unauthorized request is denied, not served), leaving the protected state
unchanged.

Signup is closed. Accounts are seeded and no route creates one. Every seeded
account uses the password `deku-demo-pw-2026`.

| Email | Name | Role | Belongs to |
|---|---|---|---|
| `owner@example.com` | Wren Calloway | `owner` | Platform Ops, Revenue Ops |
| `approver@example.com` | Ines Varga | `approver` | Platform Ops |
| `approver2@example.com` | Tomas Beck | `approver` | Revenue Ops |
| `operator@example.com` | Dara Nwosu | `operator` | Platform Ops |
| `operator2@example.com` | Milo Fenn | `operator` | Revenue Ops |

Project membership also carries a project role of `admin`, `editor` or `viewer`.
Effective permission is the union of the instance role's grants and the project
role's grants. An `owner` administers membership of any project; reading the
credentials inside one is a separate grant and is recorded.

## Core features

### Auth

Sign-in takes an email and a password and returns a bearer token the client sends
on every later request. Passwords are stored hashed, never in the clear. Tokens
expire; an expired token leaves the action unapplied and returns the person to
sign-in with their destination preserved. There is no signup route and no password
reset route. Role is resolved from the session, never read from a request body: a
request that carries a role field is treated as though it did not.

1. A sign-in with a seeded email and `deku-demo-pw-2026` succeeds and returns a
   token.
2. A sign-in with a correct email and a wrong password is denied and returns no
   token.
3. A request to any console endpoint with no bearer token is denied.
4. Repeated failed sign-ins for one address are refused for a period, and a
   legitimate person can get back in without an administrator.
5. Sign-in may also be federated, via a standard assertion protocol, with the
   assertion's signature checked against a configured certificate, its audience and
   recipient checked, and replay prevented by recording assertion identifiers.
   Where federated sign-on is enforced, local password sign-in is disabled for
   everyone except one designated break-glass account, and any use of that account
   is an audit event.

### Projects and membership

6. A person sees exactly the projects they belong to, and an `owner` sees all of
   them.
7. A request for a project the caller does not belong to is denied and reveals
   nothing about whether that project exists.
8. Only an `owner` can add a member, remove a member, or change a member's project
   role, and every one of those is recorded in the audit stream with the actor, the
   subject, the time, and the value before and after.

### Workflows and the canvas

A workflow is a directed graph of steps. The graph is user-authored and arbitrary:
it may branch, merge, loop back on an ancestor, and call another workflow, and a
step unreachable from any trigger is legal and simply never runs.

9. Opening a workflow shows its steps on a dotted ground joined by curved edges,
   with the step list beside the canvas. A step is added as a new row at the end of
   that list, never in a modal.
10. A step carries a name unique within its workflow, a type of `trigger`, `regular`,
   `core` or `code`, a position, an on-error behaviour of `stop`, `continue` or
   `continue_error_output`, a disabled flag, a retry setting and a maximum number
   of tries.
11. A connection carries a source step, a source output index, a target step, a
    target input index, and a type of `main`, `ai_model`, `ai_memory`, `ai_tool` or
    `ai_output_parser`. The four non-main types are how a model, a memory and a set
    of tools hang off an agent step on typed edges carrying capability rather than
    data, and they are drawn as dashed edges.
12. Saving produces a new immutable version with a version number, an author and a
    time. A version is never rewritten. The version number shown on the canvas
    header increments on each save.
13. A workflow whose graph is invalid is refused at save time and named: a step
    type that does not exist, a connection referencing a step that is not there, or
    two steps sharing a name. It is refused as invalid, and nothing is written.
14. Comparing two versions reports steps added, removed, renamed and re-parameterised,
    and reports a step that only moved separately from a step whose behaviour
    changed, because dragging a box is not a change to what the workflow does.
15. A workflow that calls itself, directly or through a chain, is refused rather
    than allowed to exhaust the call stack, and the refusal names the chain.
16. A step may run another workflow, passing items in and receiving items back.
    Such a sub-workflow run is a first-class run with its own identifier, linked to
    its parent so an operator can open it, and the call depth is bounded with the
    ceiling stated. A sub-workflow resolves credentials in the child's own project
    rather than the caller's, so calling one cannot reach a credential the caller's
    project lacks. The parent may wait for the child or carry on without it.
17. Deleting a workflow is a soft-delete: it leaves the list immediately, and its
    runs are pruned on the ordinary retention schedule rather than removed in one
    transaction, so deleting a busy workflow does not stall everything else.

### Credentials

18. A credential belongs to a project, carries a name and a type, and is created
    only by an `owner`.
19. The stored value is never returned by any endpoint, for any actor, at any
    privilege. The interface shows which fields are set and never what is in them.
20. Testing a credential is the server making a probe call, never the value coming
    back to the browser.
21. Binding a credential to a step is an `owner` action and is recorded in the
    audit stream. A step that needs a credential and has none fails with a named
    error rather than running without one.
22. Revoking a credential that an active workflow depends on warns first, names
    every workflow that will break, and requires a confirmation.

### Running a workflow

A run is the traversal of a graph from a start step, producing for each step that
executes an ordered list of attempts, each holding what that step emitted.

23. Starting a run creates it at status `new` and places it on the queue. The run
    board gains a card in its first column.
24. A worker claims the run, sets its status to `running`, records the worker
    identifier, and keeps a heartbeat while the run is alive.
25. Exactly one worker claims a queued run. Two simultaneous claims of the same run
    must not both succeed: one wins, the other is refused, and the run's worker
    identifier does not change.
26. The engine keeps a ready stack rather than a fixed order. A step becomes ready
    when every incoming `main` connection has delivered data or has definitively
    been skipped.
27. Skipped is a first-class outcome, distinct from empty. A branch step executes
    one of its outputs; the steps on the untaken branch are marked `skipped`, not
    left `pending`. A step with several inputs where one is skipped and one
    delivers is ready. A step where every input is skipped is skipped.
28. Each attempt at a step is recorded as its own row, so a step that took three
    tries reads as three attempts rather than one. A step whose failure is
    definitionally permanent is not retried.
29. A step set to `continue_error_output` routes its failure to a second visible
    output on the canvas, so error handling is drawn rather than buried in a
    settings menu.
30. A loop that exceeds its iteration ceiling fails the run with an error naming
    the cycle, never with a generic timeout.
31. An expression in a later step that refers to a field from an earlier step
    resolves to the correct ancestor item, even when steps in between reordered or
    filtered the list. Where that ancestry cannot be determined and an expression
    needs it, the error names the step that broke the chain rather than quietly
    returning the first item.
32. A run can be started from a chosen step using the stored output of its
    ancestors from an earlier run, re-running only the ancestors whose stored
    output is stale.
33. Data pinned to a step is used on a manual run and refused on a production run,
    and the interface shows that pins exist.
34. Cancelling a run stops the engine scheduling further steps, signals the step in
    flight, and keeps every attempt produced up to that point.
35. A run that exceeds its maximum duration is marked `failed` with a timeout
    error, and the output produced so far is kept.
36. A run records the workflow version it executed against, so opening an old run
    shows the graph as it was rather than as it is now.

### Human approval

The durable wait's most important use, and the reason a run can outlive its worker.

37. An approval step persists the whole run state, sets the run's status to
    `waiting`, records what would resume it, and releases the worker. A run at
    `waiting` holds no worker identifier. A thousand runs waiting for a person cost
    a thousand rows and no workers.
38. The approval step mints one approve address and one reject address. Each is
    unguessable, single use, and carries a deadline read from the environment.
39. Approve, reject and expire are three distinct outcomes and route differently.
    Running out of time is not the same as being refused.
40. Only an `approver` or an `owner` who belongs to the run's project can decide
    it. A request from an `operator` session is denied by the server, the run is
    still `waiting` afterwards, and no approval decision is recorded against it.
41. An `approver` who belongs to a different project is denied the same way, and
    that run is also unchanged.
42. A decision records who made it and when. If the surface cannot identify the
    person, it records that it could not, rather than recording nobody.
43. Presenting the same single-use address a second time is refused and the
    recorded decision does not change.
44. On approval the run is placed back on the queue and may be picked up by a
    different worker than the one that paused it, continuing from exactly where it
    stopped. It reaches `succeeded` and the steps after the approval step carry
    output.
45. On rejection the run reaches `failed`, the steps after the approval step are
    marked `skipped`, and the rejection is visible on the run.
46. Every approval decision is an audit event.

### Step output, code steps and expressions

47. A step's output is readable as soon as that step finishes, while its run is
    still going. Opening a run that is `waiting` shows output on the steps that
    already ran rather than nothing until the run ends.
48. A run reports the byte size of the step output stored against it, and that
    size stays at or below the ceiling read from `RUN_OUTPUT_MAX_BYTES`. A run
    that would pass the ceiling fails with the error code
    `run_output_ceiling_exceeded` rather than exhausting its worker.
49. Where a step produces bytes, the run records a reference carrying an object
    identifier, a size in bytes, a declared media type and a checksum. The bytes
    themselves are never the stored output.
50. A run can be annotated with a note. An annotated run is exempt from pruning
    until the note is removed.
51. A step of type `code` runs the body in its `parameters` where the host's
    environment variables, filesystem, process and module loader are all out of
    reach, as are the credential store and any other run's data. A body that
    reaches for one of them fails that step with the error code
    `sandbox_denied`, and the run continues or stops per the step's on-error
    setting.
52. A code step that runs past its time or memory ceiling is stopped from
    outside with the error code `sandbox_timeout`, and stopping it disturbs
    nothing else: a run started afterwards on the same worker succeeds normally.
53. A code step receives its incoming items copied rather than shared. Two steps
    fed from one source, where the first mutates what it was given, leave the
    second seeing the original.

    The sandbox is described by what it refuses, so three bodies are worked out
    here. A body of `return [{'json': {'leak': str(process.env)}}]` reaches for
    the host's environment and is refused as `sandbox_denied`. A body of
    `while (true) { }` never returns and is stopped from outside as
    `sandbox_timeout`. A body of `items[0].json.touched = true; return items;`
    mutates what it was handed, which is legal inside its own branch and
    invisible to every other branch, because the items it received were copies.
54. A step whose `parameters.url` addresses an internal range fails with the
    error code `egress_denied`. The refusal happens after the name is resolved,
    so a public host name that resolves to a loopback or private address is
    refused exactly as a literal one is.
55. A value bound from an earlier step resolves just before the step that reads
    it runs, against that step's own named ancestor. The seeded workflow's
    `Post to channel` step binds a value from `Fetch incident`, and the run's
    output for that step carries the resolved value rather than the unresolved
    expression.
56. A value bound from a step that has not run in this run fails with the error
    code `expression_unresolved_reference`, and the message names the step and
    the field that could not be resolved.

### Triggers and inbound calls

57. A workflow starts in one of seven ways, and each names what owns it: a person
    pressing run, owned by the editor; a clock expression, owned by the coordinator
    that holds the schedule; an inbound call, which any main process or inbound
    processor may answer; a repeated poll of a service, owned by the same
    coordinator; an event stream, which is a subscription to a message broker held
    by a dedicated consumer; a chat message; and another workflow, owned by the
    calling run.
58. Activating a workflow that has an inbound trigger registers its path and
    method. Deactivating unregisters it. A path already held by another active
    workflow is refused at activation time, naming the other workflow, rather than
    resolved by whoever wrote last.
59. Every workflow has two separate inbound addresses: a production one, live only
    while the workflow is active, and a test one, live only while the editor is
    listening. They are different addresses, so a test call can never reach
    production.
60. A workflow may nominate a request header as an idempotency key. A repeat
    carrying the same key within the window returns the original response and its
    original run identifier, and starts no second run.
61. A schedule is stored with its own timezone, not the server's. A workflow that
    runs at nine every morning keeps running at nine when the clocks change.
62. A schedule missed because the instance was down is recorded as missed. It is
    not silently skipped and the backlog is not replayed by default.
63. Schedules are spread across a small window so that many workflows set for the
    same instant do not all start in the same second.

### Recovery and load

64. A run whose worker stops heartbeating past the threshold is marked `crashed`,
    keeps every attempt it produced, and is surfaced to a person. The engine does
    not re-run it: the engine cannot know which of its effects already happened.
65. A run may be re-run only on an explicit decision, or automatically where the
    workflow's author has declared that workflow safe to repeat, and the interface
    says so plainly at the moment they declare it.
66. A job on the queue carries the run identifier only, never the run's data.
67. Queue delivery is at-least-once, so a worker treats the receipt of a job as
    possibly a duplicate and claims the run before doing any work. A job lease is
    time-bounded and renewed by the worker's heartbeat while the run is alive, and
    a lease that expires unrenewed is delivered again.
68. A job that keeps failing and being delivered again is given up on after a
    bounded number of attempts and marked `crashed`, rather than circling the queue
    for ever.
69. A manual run started by a waiting person is not queued behind a large backlog
    of scheduled runs.
70. Concurrency is bounded in three places: how many runs one worker executes at
    once, how many the whole instance executes at once, and a per-workflow limit
    that may be set as low as one, which is how an operator serialises a workflow
    touching something that cannot take concurrent writes. Manual runs are exempt
    from the instance ceiling up to a smaller ceiling of their own, so an operator
    can always debug even when the instance is saturated.
71. When the instance is at its ceiling, new production runs are queued rather than
    refused, and their status reads as waiting for capacity. The editor stays
    usable and a workflow can still be switched off, because the first thing
    anybody does in an emergency is turn off whatever is causing it.
72. More than one coordinating process may run for high availability, and exactly
    one of them owns the schedule at any moment. Ownership is an election over a
    shared lease carrying a fencing token, and only the holder registers schedules
    and polling triggers. On loss of that lease the follower that acquires it
    re-registers every active trigger, and a schedule missed in the gap is recorded
    as missed rather than silently skipped. A stale holder that regains
    connectivity discovers it has been fenced and stands down before performing any
    write, because two coordinators both believing they own the schedule is what
    makes every nightly workflow run twice. Inbound registrations are shared state
    rather than held by the owner, so any coordinator can answer an inbound call,
    and a workflow activated on one is seen by all.
73. Under backpressure, when the queue depth passes its threshold, load is shed in
    a stated order: polling triggers slow down first, then new scheduled runs are
    skipped with the reason recorded rather than queued without bound, then inbound
    calls are answered with a retryable status and a hint at when to try again.
    Editor traffic and manual runs are shed last, because the person trying to fix
    the overload has to be able to get in.
74. Each project carries quotas: how many workflows may be active, how many runs
    may execute at once, how much run output may be stored, and how many runs may
    be started in a month. Passing a quota refuses new production runs with a named
    error and a visible notice, lets runs already in flight finish, and leaves the
    editor usable.

### Agent steps

75. An agent step consumes a model interface rather than a named model, so
    swapping the model does not rebuild the workflow.
76. The agent loop is bounded three ways, and each ceiling fails with its own named
    error: how many times it may go round, how long it may take, and how much it
    may spend.
77. An agent can call only the tools wired to it on the canvas. It cannot ask for
    another and cannot reach a credential the graph did not give it.
78. A tool argument the model invented is validated and the validation error is
    handed back to the model, rather than failing the run.
79. Every iteration is recorded as its own attempt, holding what was sent, what
    came back, which tools were called and what they returned.
80. Memory is keyed by a session identifier drawn from the input, so two
    conversations do not merge. A memory step with no session key is refused at
    activation.
81. Anything a tool brings back is labelled as data rather than as instructions.
82. A test run over a stored dataset scores each case and an aggregate, and is
    comparable across versions. It refuses to start when a step with external
    effects is neither pinned nor stood in for, and it names that step.

### The marketing site

83. Thirteen public routes render: home, product overview, AI, pricing,
    integrations, one connector listing, enterprise, case studies, one case study,
    contact, alternatives, one comparison and privacy. A plain-text machine-readable
    index is served as well, linked from the footer inside a screen-reader-only
    sentence.
84. Every public route carries its own title and its own description, and no two
    routes share either.
85. The site serves a favicon and declares it in the document head.
86. Each page leads with one clear primary action, visually distinct from every
    secondary one. The enterprise route offers no trial action at all, because that
    deal is negotiated and a self-serve button beside a talk-to-us button means most
    people press the wrong one.
87. An unknown address renders the product's own not-found page, with a way back,
    and answers not found rather than answering as though the page existed. Three
    address-shaped literals mined out of the script bundles, `/as`, `/gs` and
    `/g/d`, are fragments rather than routes: they are unlinked, they resolve to
    that same not-found page, and they are written down here so a later crawl does
    not rediscover them and treat them as missing pages.
88. Every internal link on every public route resolves.
89. The header carries a live count of stars on the public source repository beside
    the sign-in control. It is read from stored state, never fetched at request
    time, it never blocks first paint, and a failed refresh leaves the previous
    value in place rather than writing a zero or blanking the badge.

### Plans

90. Four plans render in order: `Starter`, `Pro`, `Business`, `Enterprise`. Each
    column carries a name, a pitch, a price, an execution-volume selector, an
    action, a hosting note, an inclusion lead and a ticked feature list.
91. A switch chooses `Monthly` or `Annually (Save 17%)`. Annual is the default.
    Flicking it rewrites every price on the page with no route change.
92. Prices are integer minor units in `usd`. Starter is `2900` monthly and `2400`
    annually; Pro is `7200` and `6000`; Business is `80000` and `66700`.
    `$24.00` is `2400`, not `24.00` and not `24`.
93. Starter includes `2500` workflow executions, Pro `10000` and Business `40000`.
    Changing one column's volume changes that column's price and no other column's.
94. The fourth column carries no price. It reads `Contact Sales` where the price
    would be, and `Custom number of workflow executions` where the volume selector
    would be.
95. The inclusion lead reads `This plan includes:` on Starter and
    `Everything in Starter plan, plus:`, `Everything in Pro plan, plus:` and
    `Everything in Business plan, plus:` on the other three, so each ticked list
    carries only what is new.
96. Two of the four action buttons carry a second line reading
    `No credit card required` inside the button.
97. A banner below the table carries the lead
    `Pay for full executions, not for each step` and an action reading `Read more`.
98. Below that sit two cards: `Start-up Plan`, offering a discount to companies
    under twenty employees, and `Community Edition`, pointing at the free
    self-hosted build and carrying the repository star count beside a `View docs`
    action. The self-hosted tier is not quietly dropped: it carries the credibility
    the other two conversions lean on.

### The node catalogue

99. The catalogue searches connector listings by free text over name and
    description, case insensitively and diacritic insensitively, ranking an exact
    name match above a description match.
100. A segmented control narrows by type: `All Types`, `Regular`, `Trigger`,
    `Core Nodes`. A facet rail on the left carries a `Categories` radio group
    beginning `All categories`, and a standalone `Partner built` checkbox in its own
    card.
101. A sort control offers `Popularity`, name and recency, and `Popularity` is the
    default.
102. A count above the grid reads the number of matches followed by the word
    `integrations`, and it is announced to assistive technology when it changes.
103. The whole query, the facets, the sort and the page live in the address, so
    pasting that address into a fresh window reproduces the same result set.
104. Facet counts reflect the other active filters rather than the whole corpus. A
    category matching nothing under the current query renders disabled rather than
    disappearing, so the list does not reflow while somebody types.
105. The grid pages rather than loading everything: twenty-four results a page by
    default and sixty at most. Paging keeps the scroll position and does not lose
    focus. A page number past the last page returns an empty result set with the
    correct total rather than an error.
106. A result set of zero renders an explicit empty state, never an empty grid.
107. The search settles before it runs rather than firing on every keystroke, and it
    updates the results with no route change.

### Case studies and comparisons

108. The case-study index renders cards two across, each carrying a customer mark,
    an outcome sentence whose metric alone is set bold, a divider, a pull quote, a
    name, a job title and a `Read Case Study` action.
109. The article at a case-study address carries the mark, the title, the outcome,
    the long-form body, the full pull quote with its attribution, and a closing
    action. The quote is truncated on the card and complete on the article.
110. The comparison hub carries one card per competitor, each headed with the two
    names and a body naming a specific limitation in the conditional: the pattern is
    `If you have encountered <LIMITATION>, you might find Flowmark appealing.` Keep
    the conditional. A comparison page that asserts rather than supposes reads as an
    attack.

### The one form

The site owns exactly one form. It is reachable from the footer and from the
enterprise route. The contact route deliberately has none: it is a switchboard,
and each of its rows hands off to a destination that owns its own form.

111. The form takes `email`, `first_name`, `company`, `message` and `consent`, plus
    three hidden campaign fields and a referrer. `email` and `consent` are always
    required and `consent` must be true; `first_name` and `company` are required on
    the sales variant.
112. Every field is validated again on the server. Invalid input is rejected inline,
    the message names the field that is wrong, and nothing is written.
113. The consent value is stored with a timestamp and the exact consent wording that
    was shown at the time.
114. The three campaign fields are hidden inputs filled from the query string and
    are stored with the request. A rebuild that silently drops them breaks
    attribution somebody depends on.
115. A submission is refused when an unattended decoy field arrives filled, and
    refused when the same form is submitted repeatedly in quick succession from one
    address. A human-verification step is applied as well; any equivalent that a
    person passes and an unattended script does not satisfies this.
116. The response carries no third-party identifier back to the page.

### Consent and what is stored

117. A first-time visitor is asked once about non-essential cookies, in a dialog
    with three categories where the essential one is preselected and locked, and
    four controls: show details, decline all, accept all, and save. The answer
    survives a reload and is honoured across routes.
118. Declining is exactly as easy as accepting: one press, the same size, the same
     prominence. The site is fully usable with everything declined.
119. No measurement that sets a persistent identifier runs before that decision.
120. A privacy page, reachable from the footer of every page, states what Flowmark
     records about a visitor and about an operator, and how long each is kept.

### Observability

121. Opening a run shows its status, its mode, what started it, its duration, the
     workflow version it ran, every step with its input summary, its output
     summary, its duration and its attempt count, and the error where one occurred.
122. The audit stream is append-only, is readable only by an `owner`, and is never
     removed by the retention job that prunes run output.
123. Health answers separately for liveness and for readiness, because conflating
     the two produces a restart loop during a brief database outage.

## User flow

### Routes

The information architecture is thirteen public routes plus a set of near-identical
use-case pages cast from one template, and the signed-in console. Nothing public is
more than two clicks from the front page.

| Route | Purpose | Auth |
|---|---|---|
| `/` | home, eleven blocks top to bottom | none |
| `/product` | product overview, a grid of feature cards | none |
| `/ai` | the AI route, and the template the use-case family is cast from | none |
| `/pricing` | four plans, the billing toggle, the volume selectors | none |
| `/integrations` | the node catalogue, search and facets | none |
| `/integrations/<slug>` | one connector listing | none |
| `/enterprise` | sales-led landing, no trial action | none |
| `/case-studies` | the index of case-study cards | none |
| `/case-studies/<slug>` | one case-study article | none |
| `/contact` | a routing page, no form | none |
| `/vs` | the comparison hub | none |
| `/vs/<slug>` | one comparison article | none |
| `/legal/privacy` | what the product stores and for how long | none |
| `/signin` | sign in | none |
| `/console` | the projects this person belongs to | any signed-in role |
| `/console/<project>/workflows` | workflow list for one project | project member |
| `/console/<project>/workflows/<id>` | the canvas and its step list | project member |
| `/console/<project>/runs` | the run board | project member |
| `/console/<project>/runs/<id>` | one run, step by step | project member |
| `/console/<project>/approvals` | runs waiting on a decision | project member |
| `/console/<project>/credentials` | credential list, values never shown | `owner` |
| `/console/<project>/members` | members and their project roles | `owner` |
| `/console/<project>/audit` | the audit stream | `owner` |
| `/approvals/<token>` | decide one run from a minted address | the address is the credential |

Console navigation is a drill-down with a breadcrumb: the project, then workflows
or runs, then one workflow or one run, and the breadcrumb is how you go back up.
The public site keeps a top navigation bar of six entries, four of which open a
panel.

### Entry and redirects

- An unauthenticated request for any `/console` route redirects to `/signin`, and a
  successful sign-in lands on the route that was asked for.
- A successful sign-in with no pending destination lands on `/console`.
- Signing out returns to `/`, and any later `/console` request redirects to
  `/signin`.
- A token that expires part way through an action leaves the action unapplied and
  returns the person to `/signin` with the destination preserved.
- A signed-in person who is not a member of the project named in the path is
  refused and shown the console's not-found page rather than the project's
  contents.
- An `operator` or an `approver` requesting a credentials, members or audit route
  is refused and stays signed in.

### Journeys

1. **An operator builds and runs.** Sign in as `operator@example.com` with
   `deku-demo-pw-2026`. Open Platform Ops, then Workflows, then `Incident triage`.
   Five steps sit on the canvas joined by curved edges. Add a step as a new row at
   the end of the step list, name it `Notify on call`, choose `regular`, and save.
   The version number in the canvas header increments. Press Run. The run board
   gains a card in its first column.
2. **The run is queued, dispatched and paused.** Open Runs. The new card moves from
   Queued to Running, carrying a worker identifier, and stops in the Waiting for
   approval column with the step name `Wait for approval` on the card. Open the
   run: each step shows a status and an output summary, and the approval step shows
   its deadline.
3. **An approver resumes it.** Sign in as `approver@example.com`. Open Approvals in
   Platform Ops. The waiting run is listed with its workflow name and the step it
   is paused at. Press Approve. A confirmation page of its own opens, carrying the
   run identifier and the word Approved. Return to Runs: the run has left the
   Waiting for approval column and reached Succeeded, and the steps after the
   approval step now carry output.
4. **An operator is refused.** Sign in as `operator@example.com` and open the run
   that is waiting. No approve or reject control is present. The run is still
   waiting.
5. **A visitor compares plans.** Open `/pricing`. Four columns, annual selected.
   Flick the toggle to `Monthly` and every price changes with no route change. Open
   Pro's volume selector and choose a larger execution count: only Pro's price
   changes.
6. **A visitor searches the catalogue.** Open `/integrations`, type into the search
   field, and the count above the grid updates while the address gains the query.
   Choose a category on the left and tick `Partner built`. Copy the address into a
   fresh window: the same result set comes back.
7. **A visitor reads a case study.** Open `/case-studies` and press
   `Read Case Study` on the Vantage card. The article shows the mark, the outcome
   with its metric bold, the full quote and its attribution.

### States

- Every list has an empty state that says what is missing and what to do, never a
  bare empty grid: no projects, no workflows, no runs, no approvals waiting, and no
  catalogue matches.
- Every page has a loading state. A route loading indicator sits at the top of the
  document, present and collapsed at rest, reaching a plausible intermediate width
  while a route is loading, then completing and fading rather than snapping to
  full.
- An error never crashes the application. A failed request leaves the page usable
  and states what failed.
- A run with no attempts yet renders its card with its status and nothing else
  rather than an error.

## UI/UX notes

Look and feel only. Every behaviour rule lives above.

**North star.** A person who has never seen Flowmark should understand, inside the
first screen and a half, that this is a machine that runs a drawn chain of steps,
and should be able to read one of those chains without anyone explaining it.

**Register.** The marketing site is a shop window and may carry atmosphere. The
console is a working interface: quiet, organised, built for scanning and repeated
action, with no oversized hero and no editorial composition. Comprehension over
expression, and density over decoration, on every console surface.

**Mode.** Dark, and only dark. There is no light theme and no theme toggle, and the
product is designed fully for the one mode rather than inverted from a light one.

**Palette by role.** Written down once as named custom properties on the document
root and consumed by name; no component hard-codes a colour that already exists as
a token.

The page ground is a near-black cool neutral, a black with a bruise of blue in it
rather than a true black, and the deepest ground behind media is a plain near-black
neutral. Raised surfaces, the header fill and card fills, are deep cool neutrals a
step above the ground, with a further deep cool neutral for the hover surface.

Body text is not white. It is a near-white neutral, warmer than white, and that one
choice is why the dark ground sits still instead of vibrating; headings take a
near-white neutral at full strength. Supporting text and captions are a light
neutral and that pairing is the floor, so nothing may be lightened on the ground or
greyed further on the text. Meta and disabled text is a mid neutral, rules and
dividers a deep neutral, an inactive icon on dark a mid cool neutral.

The accent is a mid, vivid red, with a light, vivid red tint above it and a deep
step below, and the eyebrow above a heading is a light, vivid orange. The
call-to-action gradient runs from a light, vivid orange into a mid, vivid red and
belongs to the one action a page most wants; nothing else wears it. The secondary
gradient runs from a mid, vivid cyan into a mid, vivid indigo, and the announcement
bar's button takes it deliberately so the announcement cannot compete with the hero
action. The tertiary gradient is two light neutrals for everything else.

Success is a mid, soft teal above a deep, soft teal. Failure is the accent's mid,
vivid red. In progress is the mid, vivid cyan. A run waiting on a person is the
light, vivid orange. Each appears nowhere else, so the colour alone names the
state, and each is also carried by a word or a shape so meaning is never by colour
alone. The wordmark's mark in the footer is a light, vivid red, distinct from the
accent.

A second, complete family belongs to the conference sub-brand and is light and
pink: a near-white ground, a near-black neutral, three neutral greys, a deep, muted
magenta, a light, vivid red and a light, soft red. It is quarantined to the
announcement bar and must appear nowhere else. Two further near-white neutrals
belong to inverted surfaces and are used nowhere else either. The exact shades are
yours, so long as they hold the relationships and the exclusivity rules above.

**The signature.** Surfaces are separated by a hairline inset ring rather than a
border, and that ring carries a second inset along the top edge only, at low alpha
of a salmon tone, so a card looks lit from above rather than outlined. The card's
background carries a warm radial highlight positioned just above its top edge and
slightly right of centre: a lamp hanging off that corner. Reproduce the position,
not only the colours. Toggle the top-edge inset off and the page should look
visibly cheaper. Behind sections sit large soft circles of deep brown and deep
violet light, blurred even though the gradient is already soft, because a large
low-alpha radial bands on a dark ground unless it is blurred.

**Type.** Two faces, both loaded with a swap display strategy: `Geomanist` at
weights 300, 400, 500 and 700 in normal and italic, and `Geomanist Book` at 400 in
normal and italic. The normative fallback stack is
`geomanist, ui-sans-serif, system-ui, sans-serif` plus the standard emoji faces.
Naming a typeface is a licensing dependency, not an asset dependency: no font file
is fetched, and the fallback stack above is normative. Where the typeface cannot be
licensed, substitute a geometric sans with a single-storey lowercase a, a circular
o and a tall x-height at the same four weights; the property to match is x-height
against cap height, because the display sizes set solid and a face with shorter
small letters leaves the headline looking loose exactly where it shows most.

Headline sizes set solid at `100%` line-height; body sizes set `150%`. The hero
headline is `80px`; the large page headline `54px`; the section heading `48px`; the
sub-heading `38px`; the block heading `32px`; the small heading `28px` at `120%`;
the lead `24px`; large body `20px`; raised body `18px`; body default `16px`;
the navigation label `15px` at `100%`; small `14px`; caption `12px`. Prose
line-heights are `1.25` tight, `1.5` normal and `1.625` relaxed, and only the
eyebrow widens its letter spacing. A two-line display headline mixes weights inside
one block, the first line light and the second normal, which is what makes the
second line read as the payload. Figures align wherever amounts stack, which here
means the pricing table and the run board's counts.

**Shape, density and space.** Every gap is a multiple of one small spacing step.
Radii run from a hair through small, medium and large steps to a generous step and
then a pill; cards take the generous step, buttons and inner frames a smaller one,
navigation panels a step between, and anything fully round is set as a pill rather
than as an enormous number. The footer's top corners are rounded and its bottom
corners square; the announcement bar is the reverse. Both are asymmetric on
purpose: each reads as a card that has slid off one edge of the screen. Density is
comfortable on the marketing site and compact in the console, where rows sit tight
so a full run board fits one screen.

**Motion.** The character is eased: considered entrance and exit easing, so
movement reads as a designed interface rather than a machine responding. Six curves
are in use, each with a job: a symmetric house curve, a slow-out for things that
settle, a curve that only decelerates for entrances, a curve that only accelerates
for exits, a gentle curve reserved for colour, and an overshoot curve used on
exactly one component. Spreading the overshoot wider makes the product feel bouncy in a way it
is not.

The split that matters: geometry moves on the house curve, colour moves on the
gentle curve, and colour is the faster of the two. Colour arrives before the
movement finishes, and that small gap is why pointing at something feels quick
rather than sluggish.

Named moments. Two rows of connector tiles animate sideways in opposite directions
at two cycle lengths with no common factor, so the rows never align and the wall
never appears to loop; both fade softly at their left and right edges rather than
being clipped, and the track holds its content twice and moves by exactly half so
the seam is invisible. A full turn marks anything loading. A band travels across a
placeholder while its content has not arrived. A tooltip fades in and out on
opacity alone. A navigation trigger's chevron rotates when its panel opens. A
navigation panel item's two background gradients sit fully transparent at rest and
raise their alpha on hover rather than swapping the image, the second delayed
slightly behind the first, which gives the item its sense of light arriving from
below. Pointing at the primary action raises a thin white veil from nothing and
swings the direction the gradient runs in while the colour stops stay put, so the
button looks as though it has caught the light and tilted towards you; that is the
nicest single effect here and it is worth getting exactly right. A tab underline
moves; an accordion animates height and opacity together. Content arrives once: a
block starts slightly below its resting place and fully transparent, then rises the
last short distance and fades up as it enters the viewport, firing once and never
reversing on the way back up, with siblings in a group staggered. The decorative
layer behind the footer drifts on both axes and brightens as you scroll through the
footer, and it is much wider than the footer so only a window of it is ever
visible. A row of testimonial cards scrolls sideways continuously, fading at both
ends, draggable by pointer, reachable by keyboard, and never capturing page scroll.
Gradient hover states animate their stops and their angle rather than cross-fading
two images.

**What drives the scroll.** Nothing but the browser. Scrolling is native: it is not
smoothed, not hijacked and does not fight a finger or a wheel. What is tied to
scroll position is the reveal, which is driven by the element entering the viewport
rather than by a scrubbed timeline, and the footer drift. A revealing element
starts a short distance low and fully transparent, and its rise is the last part of
that distance, removed as it arrives.

What deliberately does not happen: cards do not lift, grow or bounce when pointed
at. The craft is light and colour, not movement, and adding a lift will not match
however well everything else measures. Under a reduced-motion preference both
marquee rows stop on their first repetition, the drift does not run, every reveal
renders already in its final state, and the decorative background film is not
fetched at all; transitions on colour and opacity stay, because those are not
motion.

**Layout.** The chrome is inset from the window rather than flush to it: the
announcement bar and the header are cards floated in a gutter with a sliver of page
ground showing on both sides. The header is fixed, does not hide on scroll, does
not change height on scroll and changes nothing at all; the only scroll-linked
chrome is the route loading indicator. One grid carries deliberately stepped
negative vertical offsets across four columns, each nudged up more than its
neighbour, so it reads as hand-placed rather than ruled; those offsets are the
composition and are reproduced exactly. Frosted surfaces come in four strengths,
heaviest on the white-transparent card, then the announcement bar and the
navigation panels, lighter on the footer inner, lighter still on the gradient
tiles, lightest on the feature badges.

**Selection and focus.** A selected tab is marked by a short glowing rail down its
left side in the one pure red in the product, and it is never replaced with an
underline. The focus indicator is a real outline, distinct from both hover and that
rail: hover here is a change of colour and light, so a focus state that only
brightened would be indistinguishable from it.

**Responsive.** There is one real switch, at roughly the width of a small laptop.
Above that breakpoint the layout is multi-column; below it, a single stack, and
everything else is refinement. The hero gets three different answers rather than
one fluid one: at the widest viewport two columns with the media right; at the
middle width the same two columns squeezed until the media is cropped by the right
edge rather than scaled; at phone width the media dropped entirely, the headline
centred, the body above the buttons, and both buttons full width and stacked. Below
the switch the navigation collapses to a hamburger, the header's right zone keeps
only the primary action and the hamburger, the logo wall drops from four marks to
three, the pricing table stacks to one column, the catalogue's facet rail becomes a
collapsible panel above a single-column grid, the footer link grid goes four to two
to one, and the case-study grid goes to one. A route runs about half again as long
on a phone as on a laptop, and a phone build much shorter than that has dropped
content. Three narrow-only rules are negations rather than mirrors of the positive
queries and carry the phone-only marquee mask and the phone-only section logo; do
not fold them into the positive queries. Above the top breakpoint the content
column is bounded and the extra width becomes gutter, with the ambient glows
extending into it. At a narrow viewport nothing overflows sideways and every
navigation target stays reachable.

**Accessibility, and these are contract rather than taste.** Body text and its
background meet WCAG AA contrast, and non-text indicators including the selection
rail and the tick carry a shape difference as well as a colour difference. One
banner, one main and one content-info per route; one first-level heading per route,
being the hero headline, with section headings descending without skipping. Every
icon-only control carries a text alternative; the repository badge announces what
its number is rather than only the number; the consent badge announces that it
reopens cookie settings; every repeated `Read more` and `Read Case Study` control
announces its destination, because a list of identical `Read more` links is
unusable. Full keyboard navigation with a visible focus ring: the skip link is
first in tab order, navigation panels open on Enter and Space as well as pointer,
close on Escape and return focus to their trigger, tab strips use roving focus with
arrow keys, the volume listbox and the sort control work without a pointer, and
focus is never trapped except inside the consent dialog while it is open. Touch
targets are comfortably sized. Under forced colours, gradient backgrounds resolve
to system colours, the card's inset ring becomes a real border so cards keep their
edges, and the selection rail stays visible. Every content image carries
alternative text, decorative images declare themselves decorative, and the
decorative background film carries an empty text alternative.

**What it must not look like.** No page dominated by a single hue family with no
second signal. No decoration standing in for content. No marketing composition
where the working console belongs. No card that lifts on hover. No light surface
leaking in from a component's defaults. No second brand's colour on a customer
mark, which is why every mark is flattened to plain white.

## Technical requirements

The frontend is **Preact** built with **Vite** into a production bundle and served
by a static or preview server. The backend is **Litestar** on Python, serving a
JSON interface on the same origin under the `/api` prefix. The browser receives an
application shell on first paint and every route's content arrives as JSON from
that same origin, so the HTML that leaves the server is the shell and the content
is fetched. Storage is **PostgreSQL**, read from `DATABASE_URL`. Identity is
**Keycloak**, read from `AUTH_ISSUER_URL`, `AUTH_CLIENT_ID` and
`AUTH_CLIENT_SECRET`. The approval deadline in seconds is read from
`APPROVAL_DEADLINE_SEC`, and the per-run ceiling on stored step output in bytes
from `RUN_OUTPUT_MAX_BYTES`. The app's own address and port are read from
`APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a host, a port or a
deadline; read every one from the environment.

Use only the libraries named here plus their direct dependencies. Do not introduce
a second database, cache, queue, object store, identity provider or mail vendor:
the only backing services available in this environment are **PostgreSQL** and
**Keycloak**, and reaching for anything else is a contract violation. Both are
already running and reachable at those variables, and neither is to be downloaded,
installed, compiled or started.

`GET /api/health` returns `200` once the app is ready. Liveness and readiness
answer separately: liveness says whether the process should be restarted,
readiness says whether it should receive traffic and for the main role that
includes the database being reachable.

Authentication is email and password through the app's own sign-in, returning a
bearer token the client sends on every later call. Passwords are stored with a
memory-hard hash. Session tokens are invalidated on sign-out and on a role change.
Brute-force protection applies per account and per source address, and a
legitimate person can get back in without an administrator.

**Logging.** Every record is structured rather than prose and carries the run
identifier, the workflow identifier, the step name where one applies, the project
identifier, and a correlation identifier that survives from the inbound request
through the queue to the worker. Without that identifier, tracing one run across
several processes means reading several logs side by side and guessing. No
credential value, no resolved secret and no full step payload appears in a log
record; payloads are referenced rather than embedded.

**Metrics** are exposed for scraping: queue depth, jobs waiting, jobs running,
worker count, runs started and finished by status, run duration, step duration by
step type, credential resolution failures, inbound requests by status, active
workflow count, and database latency. Queue depth trending up over a sustained
window and the crashed-run rate are the two worth an alert: the first predicts an
outage and the second reveals one.

**Usage insights** per workflow and per project are accumulated into periodic
buckets as runs finish rather than counted from the whole history when somebody
opens the page: total runs, failures, average duration and time saved against a
per-workflow estimate. Rolling them up as runs finish is what lets the insight
figures survive the pruning of the run output they were derived from, and a
dashboard that scans raw runs instead stops working on the first large customer.

**Versioning.** Every save produces an immutable version carrying an identifier, an
author, a timestamp and an optional message, and every run references the version
it ran. The version a run references is retained for as long as that run is.

**Run output is the pressure point of this whole system.** It is the largest,
fastest-growing and least valuable data here: written on every run, read rarely,
and worthless after a period the customer chooses. Every scaling problem in a
product of this shape begins there, which is what the rest of this paragraph is
about. It is written as steps complete rather than accumulated whole and flushed at
the end, so a run over a very large list does not need that list in memory. A per-run ceiling on total step output fails that one run with a named
error rather than exhausting the worker holding it. Retention is configurable by
age and by count, separately for successful and failed runs, with failures kept
longer by default because those are the ones somebody comes back to. Pruning runs
continuously in bounded batches rather than as one nightly sweep. A run somebody
annotated is exempt until the annotation is removed. Audit records sit outside
retention entirely.

**Binary payloads** never enter the database and never enter the queue. They are
written to the store and referenced by an identifier, a size, a declared media type
and a checksum, and steps that do not touch them pass the reference along without
ever materialising the bytes.

**Code an operator writes inside a workflow is untrusted and is treated as
hostile**, including on a single-tenant installation, because the author of a
workflow is often not the owner of the credentials it uses. Each execution of that
code runs where it cannot reach the host runtime's globals, module loader, process,
filesystem, environment variables or network stack except where a grant says
otherwise; cannot reach the engine's own objects, including the credential store
and other runs' data; is bounded by a wall-clock limit and a memory ceiling
enforced from outside rather than by the guest's cooperation; is stopped hard on
breach with a named error, without disturbing anything else on the same worker; and
cannot start a subprocess, open a socket or bind a port. What it does get is its
incoming items deep-copied rather than shared, a small helper library, the
read-only evaluation context, and a return value checked against the item shape. A
guest that mutates its input must not be able to change what a sibling branch sees,
and that is a correctness requirement before it is a security one. Duration and
peak memory are recorded on the attempt, so a slow workflow can be traced to the
step that spent the time.

**Every outbound request, from any step and not only a code step, passes one egress
policy.** Internal address ranges are refused: loopback, link-local, private ranges
and the cloud metadata address. This is the request-forgery defence and it is not
optional for a product whose entire purpose is fetching from addresses an operator
typed. The check happens after the name is resolved and again on every redirect, so
a public name that resolves inward and a redirect that lands inward are both
refused; checking the address before it is resolved catches nothing. Redirect
chains are bounded, and per-request and per-response byte ceilings are enforced as
the bytes stream rather than by holding them and then measuring.

**Expressions** are resolved immediately before the step that carries them runs,
once per item where the step runs per item, and never earlier. The context is
read-only and holds the current item, the output of a named earlier step, the run's
own metadata, the project's variables, the run's start instant and a set of helper
methods. That instant is fixed for the whole run: a value read in the first step
and again in the twelfth returns the same moment, so a filename built from it is
the same filename twice. An expression is code and gets the same isolation as a
code step, with a shorter time limit because it runs per item, no network access at
all, and a context built so its helpers cannot be replaced. An expression error
names the step, the field and the expression, and where the failure is a missing
reference it says which reference was missing and which were available. A reference
to a step that has not run in this run is a different, separately named error from
a reference to a step that does not exist, because the fixes are different.
Coercion rules are stated and stable, and where an expression yields a type the
field cannot take, the failure is explicit rather than silent. The editor resolves
references against the graph at edit time, without evaluating them, and warns on a
reference to a step that cannot precede this one.

**Credential storage is envelope encryption.** Each credential's payload is
encrypted with its own data key under an authenticated cipher, and that data key is
itself encrypted under a key-encryption key that never sits in the database. The
envelope is what makes rotation affordable: changing the outer key re-wraps the
small keys rather than re-encrypting every payload in the system, which on a large
installation is the difference between minutes and days. What the database holds is the
ciphertext, the wrapped data key, the cipher identifier and the key identifier. The
authenticated cipher's associated data includes the credential identifier, so a
ciphertext moved from one credential's row to another's fails to decrypt rather
than quietly decrypting into the wrong record. Decryption happens in the executing
process, as late as possible, and the plaintext never reaches the run's output, the
logs or the queue. Rotating the key-encryption key re-wraps every data key without
decrypting and re-encrypting the payloads, runs while the instance serves traffic,
is resumable, and cannot delete a key any row still references; the system reports
how many credentials remain on a retired key. A credential field may instead hold a
reference to an external secret store, resolved at execution time, cached in memory
briefly and never persisted, with a resolution failure naming the store and the key
and never the secret. For credentials obtained by an authorisation redirect, the
redirect completes on the main role which holds the client secret and never on a
worker; the state parameter is single use, bound to the initiating session and
expiring; the redirect target is matched against a registered exact value rather
than a prefix; and refresh is serialised per credential so two runs sharing one
credential do not both refresh it, because many providers invalidate the old token
on use and the second refresh would destroy the first one's result. Refresh happens
ahead of expiry on a margin rather than on failure.

**Every input is validated against a schema at the boundary**, and a workflow
definition is validated when it is saved rather than discovered to be broken by a
run at three in the morning. Rich content from the editorial side is untrusted
input to the renderer: it is sanitised against an allow-list on the way in rather
than on the way out, a card body cannot inject markup that escapes its card, and a
link target is accepted only as a relative path or an http or https address.

**Transport and headers.** Every response carries the standard security headers,
including a strict transport policy and a nosniff content-type policy. Session
cookies are secure, http-only and same-site. The console forbids inline script.
Frames are denied except on the embedding surface, and there only against a list of
permitted origins.

**Isolation.** Every query is scoped by project where the data is fetched, once,
rather than by each call site remembering to add a filter. Object paths are
namespaced by project. No credential, interface key or admin token appears in
anything the browser downloads.

**The public interface** is versioned with the version in the path, and a breaking
change means a new version while the previous one is supported for a stated period.
Access is by scoped, revocable tokens that expire, carry a last-used time, are
shown once at creation and are stored hashed. Scopes are resource-and-operation
pairs, enforced per request against the project the resource belongs to. Listing is
cursor-paginated with a stable sort, because page numbers over a table being
written to skip and repeat rows. Rate limits return the limit, the remaining count
and the reset time. Every mutation accepts an idempotency key and honours it for a
stated window. Errors carry a stable machine-readable code, a human-readable
message and the correlation identifier. A machine-readable description of the whole
interface is published and generated from the same definitions the server validates
against, so it cannot drift. Three things it deliberately cannot do, written down
so a later request for one is recognised as a change to the security model rather
than a feature: no operation returns a credential's stored value under any scope
for any actor, no operation executes code a caller supplied, and no operation lets
a caller name the database or the queue.

**Data subject obligations.** Export of everything held about an identified person
across workflows, runs, step output, agent memory and audit records, and deletion
likewise with the audit records retained under a stated basis and the deletion
itself recorded. Both run as background work with a stated completion target and
both are audit events.

**Vulnerability handling.** A published reporting route with a stated
acknowledgement time. Dependencies are scanned continuously and the build fails on
a known critical advisory. Images are rebuilt on a base-image advisory rather than
only on release.

**Performance.** No decorative video byte is fetched before first contentful paint,
none is fetched at a narrow width, and none is fetched under a reduced-motion or
saved-data preference; a still frame stands in. Fonts load with a swap strategy,
subset to the range in use, with only the two weights the hero needs preloaded.
Every image carries intrinsic dimensions so nothing reflows on load, and connector
marks below the fold are fetched lazily and served at the size they render.
Blurred decorative layers are static and sit on their own compositing layer; no
more than two live backdrop surfaces overlap at any scroll position, and the
marquee rows move on transform alone. The hero headline, not the hero media, is
what should paint first: it is text and needs nothing beyond the font. Largest
contentful paint under two and a half seconds on a mid-tier device on a slow
connection, cumulative layout shift under one tenth, interaction latency under two
hundred milliseconds.

**No binary asset ships: every asset class is a zero-asset substitution.** The
whole build stands up with no image file, no video file and no font file arriving
from anywhere, and each of those is replaced here by a recipe rather than dropped.
Grain and the star layer are generated from an inline noise filter. The hero backdrop is generated: three overlapping radial gradients in
the accent orange, the indigo and the cyan, each drifting on its own slow path with
no common period, over the page ground, rendered small and scaled up, then
saturated, blurred and blended so it never resolves as footage; under reduced
motion or at a narrow width it renders a single static frame. Customer marks are
the placeholder names set as text in the site face at medium weight, flattened to
plain white at reduced opacity, letter-spaced to the proportion of the mark they
stand for; do not attempt an invented logotype, because a wall of wordmarks in one
face reads as deliberate while a wall of invented marks reads as wrong. Avatars are
a round canvas whose hue is derived by hashing the author's handle, carrying that
author's initials, so an avatar is stable everywhere that author appears.
Photographic slots are a seeded generator producing a vertical gradient between two
palette colours with a low-amplitude noise field and a few soft bright points, at
the aspect ratio of the slot and at low enough opacity that a generated field is
indistinguishable from a photograph. Product stills are not faked with an image at
all: compose the step graph in the page as real shapes, because it stays sharp at
any size, it takes the theme, and it can be described to somebody listening.

**Route content is composed from typed records rather than written into
templates**, and a route assembles blocks while a block renders what it is given. A
block that fetches its own content is a defect; the catalogue is the one exception,
because its state lives in the address. A route carries no style rule of its own: a
variant belongs to the block. The three layers are primitives, which know only the
tokens; blocks, which are built from primitives; and routes, which are built from
blocks. Nothing reaches across them.

**The site renders from its last good content snapshot when the content source is
unavailable.** A content outage is not a site outage. Media is served under
immutable, content-addressed names with a long cache lifetime, so a changed image
is a new name rather than a purge. No content credential ever reaches the browser.

## Data model

All timestamps are UTC. Twenty-two entities carry the whole product, and the structure
below is the contract: an entity not named here does not exist, and a field not
named here is not asserted against.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account so
a grader can sign in.

Twenty-two tables.

`users` carries `id`, `email` which is unique, `display_name`, `instance_role` and
`created_at`.

`projects` carries `id`, `name`, `slug` which is unique, and `created_at`.

`memberships` carries `id`, `project_id`, `user_id`, `project_role` and
`created_at`. One person holds at most one membership of one project.

`workflows` carries `id`, `project_id`, `name`, `slug` which is unique inside its
project, `active`, `current_version_id`, `created_at` and `updated_at`.

`workflow_versions` carries `id`, `workflow_id`, `version_number`, `author_id`,
`message` and `created_at`. A row here is never rewritten after it is first
stored.

`steps` carries `id`, `workflow_version_id`, `name` which is unique inside its
version, `step_type`, `parameters`, `position_x`, `position_y`, `on_error`,
`disabled`, `credential_id`, `retry_on_fail` and `max_tries`. `parameters` is the
step's own configuration: a `url` on a step that fetches, a `code` body on a step
of type `code`, and an expression anywhere a value may be bound from an earlier
step.

`connections` carries `id`, `workflow_version_id`, `from_step`,
`from_output_index`, `to_step`, `to_input_index` and `connection_type`.

`credentials` carries `id`, `project_id`, `name`, `credential_type`,
`secret_ciphertext`, `wrapped_data_key`, `key_id`, `created_at` and `updated_at`.
No endpoint returns `secret_ciphertext` or anything derived from its plaintext.

`runs` carries `id`, `workflow_id`, `workflow_version_id`, `mode`, `status`,
`started_at`, `stopped_at`, `worker_id`, `heartbeat_at`, `idempotency_key`,
`output_bytes`, `correlation_id` and `started_by_id`.

`run_steps` carries `id`, `run_id`, `step_name`, `status`, `attempt`, `started_at`,
`finished_at`, `output_summary`, `output_bytes`, `binary_ref`, `error_code`
and `error_message`.
`attempt` counts from `1` and a retry appends a row rather than replacing one.
`binary_ref`, where a step produced bytes, carries an `object_id`, a `size_bytes`,
a `media_type` and a `checksum` rather than the bytes themselves.

`run_logs` carries `id`, `run_id`, `workflow_id`, `project_id`, `step_name`,
`correlation_id`, `level`, `message` and `occurred_at`. A row never carries a
credential value or a whole step payload.

`run_annotations` carries `id`, `run_id`, `note`, `annotated_by_id` and
`annotated_at`. A run carrying one is exempt from pruning until the note is
removed.

`approvals` carries `id`, `run_id`, `step_name`, `decision`, `decided_by_id`,
`decided_at`, `deadline_at`, `approve_token`, `reject_token` and `token_used`.
Both tokens are unique across the table.

`audit_events` carries `id`, `actor_email`, `action`, `subject`, `occurred_at`,
`source_address`, `before_value` and `after_value`. Rows are appended and never
changed or removed.

`connectors` carries `id`, `slug` which is unique, `name`, `description`,
`node_type`, `partner_built`, `popularity` and `created_at`.
`connector_categories` carries `id`, `connector_id` and `category_slug`.

`plans` carries `id`, `name`, `slug` which is unique, `pitch`,
`price_monthly_cents`, `price_annual_cents`, `currency`, `hosting`,
`inherits_from`, `cta_label`, `cta_subtext` and `sort_order`. `plan_volumes`
carries `id`, `plan_id`, `execution_count`, `price_monthly_cents` and
`price_annual_cents`. `plan_features` carries `id`, `plan_id`, `label` and
`sort_order`.

`case_studies` carries `id`, `slug` which is unique, `customer_name`, `outcome`,
`outcome_metric`, `quote`, `quote_author`, `quote_author_title`, `body` and
`published_at`. `testimonials` carries `id`, `body`, `author_name` and
`author_handle`.

`contact_requests` carries `id`, `email`, `first_name`, `company`, `message`,
`consent`, `consent_text`, `consent_at`, `campaign_source`, `campaign_medium`,
`campaign_name`, `referrer` and `created_at`.

`page_meta` carries `id`, `route_path` which is unique, `title`,
`meta_description`, `og_title`, `og_image_path` and `noindex`.

Run output is large, write-heavy and short-lived, so it is kept apart from the
workflow definitions and pruning it never touches them.

### Derived rather than stored

A plan's displayed price is derived from the selected billing period and the
selected volume tier, never stored as a third price. A run's duration is derived
from its start and stop times. A catalogue facet's count is derived from the
current query. A workflow's step count is derived from its current version. An
approval is `expired` when it is read past `deadline_at` with no decision, derived
at read time rather than written by a sweeper.

### Values with exact casing

- `users.instance_role`: `operator`, `approver`, `owner`
- `memberships.project_role`: `admin`, `editor`, `viewer`
- `runs.status`: `new`, `running`, `waiting`, `succeeded`, `failed`, `cancelled`,
  `crashed`
- `runs.mode`: `manual`, `trigger`, `webhook`, `scheduled`, `retry`, `sub_workflow`
- `run_steps.status`: `pending`, `running`, `succeeded`, `failed`, `skipped`
- `steps.step_type`: `trigger`, `regular`, `core`, `code`
- `steps.on_error`: `stop`, `continue`, `continue_error_output`
- `connections.connection_type`: `main`, `ai_model`, `ai_memory`, `ai_tool`,
  `ai_output_parser`
- `approvals.decision`: `pending`, `approved`, `rejected`, `expired`
- `run_steps.error_code`, where a step failed for one of the engine's own
  reasons: `sandbox_denied`, `sandbox_timeout`, `egress_denied`,
  `expression_unresolved_reference`, `run_output_ceiling_exceeded`
- `connectors.node_type`: `regular`, `trigger`, `core`
- `plans.hosting`: `cloud`, `self`, `both`

### Invariants, stated as properties of the running system

- A run carries at most one approval row for a given `step_name`.
- Each of `approve_token` and `reject_token` works once. After one of them has been
  presented, presenting either again is refused and the recorded `decision` does
  not change.
- A run whose `status` is `waiting` holds no `worker_id`.
- Two simultaneous claims of the same queued run must not both succeed: one wins,
  the other is refused, and the run's `worker_id` does not change afterwards.
- Two inbound calls carrying the same `idempotency_key` for the same workflow
  produce exactly one run. The second returns the first run's identifier and starts
  nothing.
- A `workflow_versions` row, once stored, is byte-for-byte the same afterwards.
- A denied mutation leaves the target row exactly as it was: no status change, no
  approval row, no audit entry claiming it happened.
- A failed run leaves no partial state of its own making: no half-written approval,
  no run claimed by a worker that is gone without being marked `crashed`.

### Seed data

Seeding is idempotent: restarting the app must not duplicate rows.

Five people, the five seeded accounts above, with `deku-demo-pw-2026`.

Two projects: `Platform Ops` at slug `platform-ops` and `Revenue Ops` at slug
`revenue-ops`. `owner@example.com` is an `admin` of both. `approver@example.com`
and `operator@example.com` are `editor` of `platform-ops` only.
`approver2@example.com` and `operator2@example.com` are `editor` of `revenue-ops`
only.

Three workflows. `Incident triage` in Platform Ops, active, at version `1`, with
five steps. `Nightly backup sweep` in Platform Ops, inactive, with three steps.
`Lead handoff` in Revenue Ops, active, with four steps.

`Incident triage` version `1` carries these five steps in order, joined on `main`
connections: `Webhook trigger` of type `trigger`, `Fetch incident` of type
`regular`, `Classify impact` of type `regular`, `Wait for approval` of type
`core`, and `Post to channel` of type `regular`.

Two credentials: `Pager API token` of type `header_auth` in Platform Ops, bound to
`Fetch incident`; and `CRM OAuth` of type `oauth2` in Revenue Ops, bound to
nothing.

Three seeded runs. One run of `Incident triage` at status `waiting`, paused at
`Wait for approval`, carrying an approval row whose `decision` is `pending`. One
run of `Incident triage` at status `succeeded`. One run of `Lead handoff` at status
`waiting` in Revenue Ops, which is the run `approver@example.com` must not be able
to decide.

Thirty connectors across the eight categories `communication`, `data-and-storage`,
`developer-tools`, `marketing`, `productivity`, `sales-and-crm`, `security` and
`support`. At least one description is long enough to clamp and at least one name
long enough to wrap, and thirty rows against a default page of twenty-four means
the catalogue pages.

Four plans in order: `Starter`, `Pro`, `Business`, `Enterprise`, with the prices
and included execution counts pinned in Core features.

Four case studies. `Vantage` and `Northwind` are the two the home route shows.
Vantage's outcome reads
`How Vantage built an AI first company culture and saved 1,000 hours of manual work`,
attributed to `Ollie Marchese`, `Chief Technology Officer`. Northwind's reads
`How Flowmark revolutionized threat intelligence at Northwind and saved 2.2 Million`,
attributed to `Claire Vandermeer`,
`Cyber Operations Engineering Manager`.

Three testimonials, by `Robin Tindale` at handle `@robm`, by `Andervaal` at handle
`@Andervaal`, and by `Lucia Vidales`.

Eight customer marks for the logo wall: `Vantage`, `Northwind`, `Halcyon`,
`Bellweather`, `Cindermill`, `Ardenne`, `Kestrel Logistics` and `Perrin Foods`.
Four show at desktop width and three at phone width.

Two competitors for the comparison hub: `Tessellate` and `Pipeworks`.

## Front-end specification

This section carries the visual detail the marketing site was measured at. It
specifies appearance and arrangement; every behaviour rule lives in Core features.

### Design token names

The palette is declared once as custom properties on the document root and consumed
by name, so the names themselves are part of the contract even though the values
are yours. Ground and surface are `--color-shades-midnight-navy` for the page and
footer ground, `--color-base-dark` for the deepest ground behind media,
`--color-shades-dark-navy` for the raised surface and header fill,
`--color-shades-deep-navy` for card and tile fill,
`--color-shades-dark-navy-lighten` for the hover surface, and `--color-black`,
which is a gradient terminus only and is used for nothing else.

Text takes `--color-base-heading-primary` for headings,
`--color-base-text-primary` for body, `--color-base-text-secondary` for supporting
text and captions, `--color-shades-darker-gray` for disabled and meta,
`--color-base-heading-orange` for the eyebrow above a heading,
`--color-shades-hard-gray` for rules and dividers, and
`--color-shades-slate-blue` for an inactive icon on dark.

Accent and action take `--color-primary-400` as the accent tint,
`--color-primary-600` as the primary accent, `--color-primary-700` as the accent
pressed state, `--color-primary-900` as the accent deep step, and
`--color-base-red` as the glow source. The call-to-action gradient is built from
`--color-button-cta-from` and `--color-button-cta`; the secondary from
`--color-button-primary-from` and `--color-button-primary`; the tertiary from
`--color-button-tertiary-from` and `--color-button-tertiary`.
`--color-additional-500` is the violet used on badges and charts and
`--color-additional-600` the blue beside it. `--color-green-1` and
`--color-green-2` carry success deep and success. `--color-base-pink` is the
wordmark's mark in the footer.

The conference sub-brand's family is every token prefixed `--color-loop-`:
`--color-loop-bg`, `--color-loop-black`, `--color-loop-gray-15`,
`--color-loop-gray-30`, `--color-loop-gray-60`, `--color-loop-maroon`,
`--color-loop-pink` and `--color-loop-pink-soft`. Nothing outside the announcement
bar may consume one. Three further greys sit outside both families and belong to
inverted surfaces: `--color-shades-hazy-white`, `--color-shades-soft-gray` and
`--color-shades-dark-gray`.

The card's inset ring is `--shadow-card-top-glow` and the tab strip's selection rail
takes its glow from `--drop-shadow-red-glow`. Weights are `--font-weight-light`,
`--font-weight-normal`, `--font-weight-medium`, `--font-weight-semibold` and
`--font-weight-bold`; prose line-heights are `--leading-tight`, `--leading-normal`
and `--leading-relaxed`, and `--tracking-widest` appears only on the eyebrow.
Spacing steps from `--spacing`, and `--container-xl` bounds a section's description
rather than the section itself. Radii are `--radius-sm`, `--radius-md`,
`--radius-lg`, `--radius-xl`, `--radius-2xl`, `--radius-small`, `--radius-3xl`,
`--radius-default` and `--radius-huge`; blurs are `--blur-xs`, `--blur-sm`,
`--blur-md`, `--blur-lg`, `--blur-xl`, `--blur-2xl` and `--blur-3xl`. Breakpoints
are `--breakpoint-sm`, `--breakpoint-md`, `--breakpoint-lg`, `--breakpoint-xl`,
`--breakpoint-2xl` and `--breakpoint-xxl`, and it is the third of those that
carries about half of all the declared queries and is the one real switch.
Durations and easings are `--default-transition-duration`,
`--default-transition-timing-function`, `--ease-in-out` and `--ease-in`. Type
tokens are `--text-headline-xxl` down through `--text-headline-xs`,
`--text-headline-xxs`, `--text-xxl`, `--text-xl`, `--text-lg`, `--text-md`,
`--text-nav-link`, `--text-sm` and `--text-xs`, at the sizes given in UI/UX notes.

Depth is a stated ladder rather than an accident: a decorative glow sits behind
content, ordinary elements sit in flow, a raised child sits above its card's
background, a card's own content sits above its background layer, sticky
in-section furniture sits above that, overlay scrims above that, the fixed header
and its panels above those, and transient messages at the top.

### How a hover is expressed

A hover state is a before-and-after diff on named properties, never a swap of one
whole image for another. Pointing at the wordmark moves its `color` and its
`border-color`, and both of its pseudo-elements, from the body colour to the
heading colour. A navigation label and a navigation trigger move from their resting
opacity to full. A panel item moves its `color` the same way, and raises the alpha
of its `background-image`, which is two fully transparent gradients at rest; its
leading pseudo-element moves its `border-color` from fully transparent to white at
low alpha. The call-to-action button's `background-image` is two stacked
`linear-gradient` layers, the first a flat transparent white that becomes the veil
and the second the warm orange-to-red run; on hover the veil's alpha rises and the
second layer's angle swings, while its colour stops stay exactly where they are.

Backgrounds are built the same declarative way. The card's base variant is a
`radial-gradient` highlight positioned above its top edge and right of centre, over
a vertical `linear-gradient` and a third radial; the shine-blue variant is a wide
`radial-gradient` from below-left over a second from above-right. The ambient glows
are each a `radial-gradient` run through a blur: a brown circle, and a purple circle
whose falloff is gentler and whose blur is heavier.

### Global chrome

Everything here renders on every public route and is built once.

**The announcement bar** is a single-row card at the top of the document, its
bottom corners rounded and its top corners square so it reads as having dropped
from off-screen. It carries a heavy backdrop blur over a warm radial wash under a
dark linear wash, holds one centred sentence at body size followed by a pill
button, and is not dismissible: it is content and it scrolls away with the
document. The copy reads
`Convergence 2026, Lisbon, October 14. Early bird tickets are now on sale.` and the
button reads `Get your ticket` followed by a right arrow. That button wears the
secondary cyan-to-indigo gradient, never the call-to-action gradient, so the
announcement cannot compete with the hero action.

**The header** is fixed, full width inside the frame inset, with the wordmark
linked to `/` at the left, six navigation entries centred, and the repository
badge, `Sign in` and `Get Started` at the right. Its fill is the raised surface at
partial alpha over a backdrop blur so the page shows through as a wash. A
navigation label rests at reduced opacity and comes to full on hover. The bar's
height is set by its navigation triggers.

The six entries are `Product`, `Use cases`, `Docs`, `Community`, `Enterprise` and
`Pricing`. The first four open a panel; the last two are direct links to
`/enterprise` and `/pricing`. The Product panel holds Product overview,
Integrations, Templates and AI, and in that panel only each item also carries a
one-line description underneath at small size: `Product overview` reads
`Automate business processes without limits on your logic`; `Integrations` reads
`Seamlessly move and transform data between different apps with Flowmark.`;
`Templates` reads `Explore +10k workflow automation templates`; `AI` reads
`Get to prod faster - and with more flexibility than coding alone`. The Use cases
panel holds Building AI agents, RAG, IT operations, Security operations, Lead
automation, Supercharge your CRM, Limitless integrations, Backend prototyping,
Embedding and Case studies. The Docs panel holds Self-host, Documentation, Our
license and Changelog. The Community panel holds Forum, Learn, Careers, Blog,
Creators, Partners, Hire an expert, Events and Support. A panel trigger is a
button rather than a link and carries a chevron. A panel opens on pointer with
intent and on click or Enter, and closes on pointer leave after a delay, on Escape,
and when focus leaves it. The panel backdrop is the heaviest blur on the site,
which is what lets a panel sit over the hero with no solid fill. A panel item's
resting background is two fully transparent gradients whose alpha rises on hover.

**The repository badge** is a pill to the left of `Sign in`, carrying the
repository glyph and a live count at small size, formatted with thousands
separators in the visitor's locale.

**The footer** is the largest component and the one carrying the most craft: a card
with its top corners rounded and its bottom corners square, over the page ground at
half alpha and a backdrop blur, holding a four-column link grid, a brand block, a
social row and a legal rule. Behind it sits a layered background carrying three
images at once: one gradient fading the page ground in at the top, one fading it
back out at the bottom, and a warm orange light source at the left edge, vertically
centred. That whole layer is masked so the glow is invisible at the very top of the
footer and reaches full strength about a fifth of the way down; without the mask
the glow cuts a hard line against the section above. A decorative star layer sits
on top at reduced opacity and moves on scroll. The brand block carries the wordmark
with its mark in the light, vivid red, then the tagline `Automate without limits`
at body size and bold weight, then five social icons at reduced opacity.

The link grid's first column is `Careers` with a `Hiring` badge, `Contact`,
`Merch`, `Press`, `Legal` and `Tools`. The second is `Case Studies`,
`AI agent report`, `AI benchmark`, `Flowmark alternatives`, `Events` and
`Convergence` with an `Oct 2026` badge. The third is `Partners`,
`Affiliate program`, `Hire an expert`, `Join user tests, get a gift`,
`Brand guidelines` and `Flowmark on platform`. The fourth column carries the one
form. Below the grid a hairline divider, then a row carrying `Imprint`,
`Security`, `Privacy` and `Report a vulnerability` separated by pipe glyphs on the
left, and the copyright line `2026 Flowmark` with `All rights reserved.` on the
right. A screen-reader-only sentence around the machine-readable index link reads
`See llms.txt for all machine-readable content.`

**The closing block** sits immediately above the footer on every public route: a
centred two-line headline at the large page size, a one-line subhead in the
supporting colour, and a single call-to-action button, over the same warm light as
the footer so the two read as one continuous piece of furniture rather than two
stacked sections.

**The consent badge** is a round control pinned to the bottom-left corner, carrying
a ring-and-dots glyph and a soft shadow, and it reopens the consent dialog.

**The skip link** is a screen-reader-only link to the main landmark, first in tab
order, becoming visible on focus.

### Iconography

Every icon is geometry drawn inline, never a font, never a sprite request and never
a fetched file. Each takes the inherited text colour unless a fill is named, so one
icon serves every context, and stroke widths are carried as authored rather than
normalised. An icon inside a link inherits that link's colour transition and does
not animate on its own; only a navigation trigger's chevron rotates.

The set is: a chevron pointing down beside each panel name, a right-facing arrow at
the end of a link, three stacked lines for the narrow-width menu, a filled circular
tick beside every included plan feature, a lightning bolt, a cloud and a stack of
servers for the two ways of running the product, a repository glyph, a send glyph,
a sliders glyph, a quote glyph, and small cubes standing for the pieces a workflow
is built from: a cube, a split cube and a person on a card. The wordmark itself
reduces to a node-and-edge glyph: three small circles on the left at a shared
radius, one on the right at the same radius, joined by two curved edges meeting at
a junction.

### Components

Ten components assemble every public route.

**The card** is the workhorse: one component in eight background variants,
otherwise identical, with its content held above its background layer. The variants
are base, red, shine-blue, dark-navy, deep-navy, a call-to-action variant carrying
the closing-block glow, white-transparent with the heaviest backdrop blur, and
blank, which carries no background and is used as a spacer in the horizontal quote
row.

**The button** has three variants, all gradients, all built so their colour can
slide rather than jump: call to action for a trial or for starting to build,
primary for a secondary action or a read-more, and tertiary for neutral actions
such as talking to sales. Both gradient variants carry a two-layer image whose
first layer is a flat transparent white; that layer is not decoration, it is the
hover veil sitting at zero alpha so it has something to animate from. Under each
button sits an almost invisible shadow tinted with the button's own colour, which
is what stops it looking pasted on. The label is a span so gradient text can be
applied where needed, and the control is tall enough at desktop to be comfortable.

**The gradient tile** is a link styled as a small card in three colour variants,
with a light backdrop blur and two light sources, one off the top-right corner and
one below the bottom edge.

**The feature card** is a flat dark gradient with a dot pattern tiled over it,
masked so the pattern is dense at the centre and gone at the edges.

**The badge** comes in two kinds: a feature badge with a heavy radius, a
half-alpha deep surface, white text, a light backdrop blur and a ring, resting
slightly under full size and scaling to full when its section reveals; and a label
pill at a small radius on a flat low-alpha white, used for `Hiring` and for the
conference month in the footer.

**The tab strip** has triggers resting at reduced opacity on a transparent
background that raises on selection, with the active trigger marked by the glowing
red rail down its left side.

**The frosted surface** comes in the four strengths named in UI/UX notes.

**The ambient glow** is decorative spans placed behind content, each a radial
gradient run through a blur filter. The gradient sets the shape and the falloff and
the blur removes the banding a large low-alpha radial produces on an eight-bit
display; skip the filter and the glows band visibly on the dark ground.

**Gradient text** sets the eyebrow above a heading on the AI, enterprise and
comparison routes in a warm orange-to-red gradient clipped to the glyphs, with the
stops far enough apart that a short eyebrow reads as almost flat orange and a long
one visibly warms from left to right. It degrades to the flat eyebrow orange where
clipping to text is unavailable, and keeps its accessible name either way.

**The product still** is a framed composition of the step graph, in a flat
treatment and a tilted one; the tilted variant is rotated a few degrees and given
perspective, as on the AI route hero.

### Route: Home

Eleven blocks, top to bottom: hero, logo wall, role tab strip with a node graph,
social proof triplet, connector wall, AI feature pair, code and UI split, feedback
loop block, case studies, enterprise block, then community quotes and the closing
block.

The **hero** is two columns at desktop and one at phone width. Its headline is two
lines at the hero size set solid: line one `AI agents and workflows` at the light
weight in the body colour, line two `you can see and control` at normal weight in
the heading colour, so weight and colour both step up on the second line. The
actions are a call-to-action button `Get started for free` and a tertiary button
`Talk to sales`. The body is three lines at body size in the supporting colour:
`Build visually, go deep with code, connect to anything. Every step of your agents' reasoning, traceable on the canvas. Deploy on your infrastructure or ours.`
The media is a lightning bolt rendered against the dark ground, occupying the right
half and bleeding past the bottom of the hero, carrying a warm drop shadow on its
glow layer and a slight resting rotation, with the generated backdrop behind it at
raised brightness and the generated film behind that, saturated, blurred and
hard-light blended so it contributes moving colour rather than a recognisable
picture.

The **logo wall** carries the caption
`AI agents and workflows for technical teams at` at small size in the supporting
colour, then a row of customer marks forced to flat white at reduced opacity,
contained rather than stretched, aligned to the start.

The **role tab strip** is the most complex block on the route: a vertical tab list
on the left and a rendered step graph on the right. Five tabs, each reading a role
followed by `can` at bold weight and then a task line in the supporting colour, for
`IT Ops`, `Sec Ops`, `Dev Ops`, `Sales` and `You`. Selection is marked by the
glowing red rail. The right column renders a workflow graph as a still: rounded
square nodes on a dotted ground joined by curved edges, with circular sub-nodes
hanging below the agent node on dashed edges, each labelled. A hint over the graph
reads `Click on image to go to the template`. Changing tab swaps the graph, and the
strip is a single-selection widget with roving focus, arrow-key navigation and a
focus ring distinct from the selection rail.

The **social proof triplet** is three cards in a row, each a bold lead followed by
a supporting clause and carrying the wordmark small at the left: `Top 50 repository.`
with `202,851 stars. Read the source that earned them.`; `4.7/5 stars on reviews.`
with `To quote: "I can move fast and never feel boxed in."`; and
`200k+ community members.` with `This wouldn't be possible without you.` The third
card takes the shine-blue treatment and the first two the base.

The **connector wall** is headed `Find and build your own data & AI workflows` with
the subhead
`Use pre-built nodes for common apps. Custom API connections for everything else.`,
then two marquee rows of connector tiles running in opposite directions, then a
primary button `Browse all integrations`. Tiles are small rounded squares on a dark
fill, each holding one connector mark, and both rows are masked at their ends.

The **AI feature pair** is headed `Build AI agents you can actually follow` with
the subhead
`Connect any model. Inspect every decision. Keep humans in the loop.`, then a
two-column grid of tall cards: the left carrying a product still, the right a
simulated chat exchange built from stacked message bubbles on a half-alpha deep
surface, each with a soft inner shadow and a slight resting offset removed on
reveal. Below that, a card headed `Runs where you decide` with three ticked lines,
beside a card carrying the chat exchange.

The **code and UI split** is a wide card whose background runs a warm orange radial
from the top-left corner across roughly half its width, so the left column's text
sits on orange and the right column's product still sits on near-black. It is
headed `Code when you need it, UI when you don't` with the body
`Other tools limit you to either a visual building experience, or code. With Flowmark, you get the best of both worlds.`
and three items, each opening with a code-brackets glyph in the accent and a bold
lead: `Write JavaScript or Python` then
`anywhere in your workflow. Imagine it, then build it.`;
`See the inputs and outputs` then
`right next to the settings of every step. No unnecessary clicks.`; and
`Test AI workflows with real data` then
`to improve accuracy and catch errors before your customers do.`

The **feedback loop block** is headed `Move fast. Break nothing.` with the body
`Build with the short feedback loops that keep you in the flow.`, a two-column
ticked list of `Re-run single steps, not your entire workflow`,
`Replay or mock data to not wait for external systems`,
`Avoid endless debugging clicks with the logs view` and
`Evaluate AI natively to optimize performance`, then a primary button
`See full product overview`, and on the right a large circular badge on a faint
circuit-trace ground: concentric rings with a violet arc and a lightning glyph at
the centre.

The **case studies** block is a centred heading `Case Studies` above two cards side
by side, each carrying a flattened customer mark, a two-line outcome sentence with
the number alone at bold weight, a divider, a pull quote, a name, a job title and a
primary button `Read Case Study`.

The **enterprise block** carries a feature badge reading `Enterprise-ready`, the
heading `Reliable. Scalable. Secure.` set as three sentences on one line, the body
`Deploy on your infra or ours. Push workflows to production with the DevOps experience teams trust. Flowmark's security and governance features let you build, monitor, and scale agents without losing control.`,
two buttons `Explore Flowmark for enterprise` and `Talk to sales`, and a four-row
definition list. On the right sits a dim generated still of a server room at low
opacity with a floating quote card over it reading
`"The idea is that everybody in the organization can use Flowmark to manage data retrieval or data transformation."`
The four rows are `Security and control`, with
`Fully on-prem option, single sign-on, and directory sync, encrypted secret stores, version control, role-based permissions.`;
`Observability and transparency`, with
`Audit logs and log streaming to your monitoring stack, workflow history, real-time alerts, usage dashboards`;
`Developer experience`, with
`Git-based control, isolated environments, multi-user workflows, workflow diffs`;
and `AI governance`, with `Human-in-the-loop, guardrails, evaluations`.

The closing block's headline is `Simple enough to see.` over
`Powerful enough to ship.`, its subhead
`Join the teams building AI automation they can actually explain.`, and its action
`Start building`.

### Route: AI

The second-most-worked route and the template the eight use-case pages are cast
from. Its hero differs from the home hero three ways and is otherwise the same
skeleton: an eyebrow above the headline reading
`The potential of AI with the power of automation` in the gradient-text treatment;
a headline that is one sentence over two lines rather than a pair of contrasting
lines, reading `The practical way to make a business impact with AI`, all at normal
weight; and a tilted product still instead of a rendered object, showing the canvas
with a right-hand panel of delivery channels. The body reads
`Flowmark is about help, not hype. Build modular AI systems that are easy to debug, explainable by design, and maintainable as requirements change.`
The buttons are `Start building for free*` and `Talk to sales`, with the asterisk
footnoted directly below at caption size:
`* 14 days free trial. No credit card required.`

Below the hero sit three trust chips, each a lightning glyph in a small rounded
square followed by a label: `Over 200k repository stars`, `Self host-able` and
`Compliance certified`. This is the only route carrying chips rather than a logo
wall in that position.

Then the same tab-strip component as the home route with different content: the
eyebrow `Common use cases`, the heading
`Create complex AI agents with confidence`, the body
`Pair AI with explicit logic to stay in control of inputs and outcomes. Blend 500+ integrations, AI agents, human approvals, and code into flexible workflows that perform reliably in production.`,
and five roles, each with a task line: `ITOps can`
`Route employee requests to best model for type of inquiry`; `Support can`
`Use RAG to answer questions from internal PDFs`; `Sales can`
`Discover leads using connected services`; `Finance can`
`Automate operations with specialized agent teams`; and `Marketing can`
`Orchestrate agents for strategic research`.

Then the governance grid: the eyebrow `Why Flowmark?`, the heading
`AI does the 'what'. You decide the 'how'.`, the body
`Keep AI grounded in clean inputs and business rules, with human checkpoints, performance monitoring, and built-in audit trails.`,
and four cards in a two-by-two grid, each a sub-heading, a paragraph and, in two of
the four, an inline link reading `Get the playbook` followed by trailing text that
sits outside the link so the link's accessible name is only those three words. Each
card carries a product still at the top, cropped and bled off the card's top edge.
The four headings and bodies are:

- `Ensure human brains hold the reins` -
  `Autopilot is for planes, not production AI. Place human-in-the-loop checks at any point in a workflow or in front of any AI Agent tool. Get fine-grained control over when to enforce human approval and when AI can guide requests for user input.`
- `Guard your AI against going rogue` -
  `Boundaries matter. Combine AI with rule-based automation to constrain inputs, then validate and route outputs using explicit logic. Filter out malicious input, sanitize sensitive data, and handle errors early to keep AI behavior on the rails.`
- `Monitor every decision your AI makes` -
  `Ignorance of your AI is anything but bliss. With Flowmark, you can inspect every execution to see the prompt sent, model response, and what happened next. Stream logs to your favorite observability tools. Track changes and versions. And trace behavior for debugging, audits, and compliance.`
- `Reliable AI outputs, every time` -
  `Hope is a horrible deployment strategy. Control your workflows with evaluations that test AI reliability against defined metrics. Use the results to refine prompts and select models. Then monitor your workflows to detect drift and trigger follow-up actions.`

Then a pull quote: one wide card holding a customer mark, a large quotation at the
block heading size with its payload clause at bold weight, then an avatar, a name
and a job title, with typographic quotation marks as part of the copy.

Then the template library: the eyebrow `Template library`, the heading
`Automate out of the gate with thousands of templates`, the body
`Create workflows in no time with templates for the most common and complex AI use cases. Our active developer community shares new workflows every week that you can download and adapt.`,
a call-to-action button `Browse All Templates`, and a grid of template cards each
carrying a title, a row of node chips naming the steps that template uses, and a
count chip reading a plus and a number for the steps not shown.

### Route: Product overview

A landing route built almost entirely from the feature card in a two-column grid.
Each card is a product still at the top, a heading, a paragraph and a text link
ending in a right arrow. The observed card pairs, in order, are an expressions card
and a routing card, then a triggers card and an AI nodes card, headed
`Diverse triggers` and `AI nodes`, with link labels `See expressions`,
`Explore transformers`, `See triggers` and `Dive into AI`. The stills in this grid
are not screenshots of a whole application: they are cropped step graphs on the
dotted ground, showing six nodes in two rows of three for the triggers card and a
single agent with three sub-nodes for the AI card, each node a rounded square with
its icon centred and its name below at caption size. A text link inside a card is
not underlined: it is body text in the body colour followed by a small arrow, and
on hover the whole thing moves to the heading colour on the colour transition while
the arrow stays put. The same template with the trial button removed and a
talk-to-sales button in its place is the embedding route.

### Route: Pricing

The heading `Pricing` at the section heading size, then two body lines:
`All plans include unlimited users & workflows and every integration.` and
`Pricing based on monthly workflow executions, regardless of complexity.`

The billing toggle is a switch between `Monthly` and `Annually (Save 17%)`, its
track a pill filled with the secondary cyan-to-indigo gradient when annual is
chosen and its knob a white disc, with the label text either side of the switch
rather than inside it. It is a single switch with an accessible name naming both
states.

The plan table is four columns at desktop, each a base-variant card carrying the
same eight parts in order: name, pitch, price with its unit beside it, volume
selector, action, hosting row, inclusion lead, feature list. The pitches read
`Great for getting started and seeing the power of Flowmark.`,
`For solo builders and small teams running workflows in production.`,
`For companies with < 100 employees needing collaboration and scale.` and
`For organisations with strict compliance and governance needs.` The price unit
reads `/mo, billed annually`. The volume label reads `workflow executions` over
`with unlimited steps`. The fourth column replaces the price with `Contact Sales`
at the section heading size and the volume selector with a sliders glyph beside
`Custom number of workflow executions`.

The volume selector is a sub-panel inside the card on a low-alpha white fill,
holding the count at the block heading size with a two-line label beside it; on the
three paid plans it carries a chevron and is a listbox with a labelled trigger
rather than a native select dressed up.

The actions read `Start free trial` and `Contact sales`, and two of the four carry
a second line reading `No credit card required` at small size inside the button, so
size the control for two lines rather than clipping. The hosting row is an icon row
using the cloud and server glyphs and reads `Hosted by Flowmark`, `Self-hosted`, or
`Hosted by Flowmark` `or` `Self-hosted`. Sample features include
`1 shared project`, `5 concurrent executions`, `3 shared projects`,
`20 concurrent executions`, `6 shared projects`,
`Single sign-on and directory sync`, `Unlimited shared projects` and
`200+ concurrent executions`.

Below the table sits a wide red-variant banner spanning its width, carrying the
bold lead `Pay for full executions, not for each step`, the body
`Unlike other tools that charge per step or user, Flowmark lets you build freely and only pay when a workflow runs from start to finish.`
and a right-aligned call-to-action `Read more`, its background running a warm
gradient from the centre-right.

Then the alternatives pair: the heading `Looking for` over `something else?` in the
left third, and two cards in the remaining two thirds. `Start-up Plan` reads
`Under 20 employees? Check if you qualify for our Start-up Plan and get 50% off Business.`
with a tertiary button `Learn more`. `Community Edition` reads
`A standard, self-hosted version of Flowmark is available in the public repository.`
with the repository badge showing the star count beside a tertiary button
`View docs`. Then the logo wall with its caption on one line, then a comparison
table, then the closing block.

### Route: Integrations catalogue

The only route with a genuine search-and-filter interface. A centred heading
`Best app & software integrations` at the section heading size above a two-line
centred body reading
`Optimize your workflows with these top software integrations.` and
`Seamlessly move and transform data between different apps with Flowmark.`, with
the sub-heading `Connect anything to everything`.

The search bar spans the left two thirds on a low-alpha white fill, carrying a
magnifier glyph at the start and the placeholder
`Search for workflows, nodes, tasks...`. Beside it sits a segmented control of four
options, `All Types`, `Regular`, `Trigger` and `Core Nodes`, with the selected
segment filled and the others transparent.

The facet rail is a left column about a quarter of the width, holding a standalone
`Partner built` checkbox in its own bordered card, then a radio group headed
`Categories` in a second card beginning `All categories` and then the named
categories in alphabetical order, several carrying a chevron that expands to
sub-categories. Controls are native inputs restyled: the radio is a ring with a
filled centre in the accent when selected, the checkbox a small rounded square.

The result header carries the count on the left at the large body size, rendered as
the number followed by `integrations`, and a sort control on the right reading
`Sort:` followed by the current key and a chevron, defaulting to `Popularity`.

The result grid is three columns at desktop of deep-navy-variant cards, each a
connector mark in a rounded square, a name at the large body size, and a two-line
description clamped with an ellipsis. Each card links to that connector's own
listing.

### Route: Enterprise

An eyebrow `Flowmark for Enterprise` in gradient text, the headline
`The power of flexible AI workflows, fine-tuned for enterprise production` over
three lines at the section heading size, a four-line body reading
`Scale without breaking things. Collaborate without the mess. Meet strict compliance standards. Join the enterprises already using Flowmark's advanced security and DevOps features to build & monitor business-critical AI workflows.`,
and a single call-to-action button `Contact Sales`. There is no trial button on this
route. The media is a tilted product still showing an administrative settings
screen with a left rail of setting groups and a right pane listing external secret
stores. Below the hero the logo wall renders four marks with its caption on one
line and centred rather than left-aligned, then the same four capability rows as
the home route's enterprise block at full width, a term at bold weight on the left
and its contents on the right in the supporting colour, with no decoration at all:
this section is a list somebody is checking against their own requirements.

### Route: Case studies

The index is a heading above a grid of case-study cards two across, the same card
the home route uses. The outcome sentence mixes weights inside one sentence, the
metric at bold and the rest at normal; do not bold the whole sentence, because it
is the number alone being bold that makes the number the thing you remember. The
customer mark uses the same flattening as the logo wall, so a card never carries a
second brand's colour. The pull quote is truncated on the card and complete on the
article. The article at a case-study address carries the mark, a title, a hero
outcome, long-form body, one or more pull quotes attributed to a named person with
a job title, and a closing call to action.

### Route: Contact

A routing page, and the most important thing about it is that it has no form. A
feature badge reads `Contact`, the headline reads `Problems, questions, or bugs?`
at the section heading size, and a five-line body directs the reader to the
community forum first:
`If you have a question or encounter an issue, please post it in our forum. It's highly likely that if you need help with something now, someone else will need the same answer later. By addressing questions openly in the forum, we reduce duplicate enquiries and free up more time to focus on improving Flowmark.`
A primary button reads `Community`. The media is a large, very low-contrast
generated illustration of a person at a desk, sitting at the right and bleeding off
the top and right edges.

Below sits a routing list as a definition list, a term at bold weight on the left
and a description with a tertiary button on the right. The rows are `Sales team`,
with
`Interested in paid offerings like paid support, embedding, or an Enterprise plan? Contact our sales team to request a demo or learn more.`
and the action `Contact sales`; `Marketing team`, with
`For press, media inquiries, and marketing collaborations` and the action
`Contact marketing`; and `Affiliates`, with
`Interested in promoting Flowmark and earning commissions?` Every row's button is
tertiary rather than a call to action, because the page is a switchboard and no
destination is privileged.

### Route: Alternatives

An eyebrow `Flowmark alternatives` in gradient text, a headline
`Flowmark vs. other workflow` over `automation platforms`, and two body
paragraphs: `Looking for Flowmark alternatives? Perhaps considering a switch to Flowmark?`
and
`Understand how Flowmark compares to other products out there, so you can find the best fit for you.`
The media is a composition rather than a still: two rounded tiles holding two
logos, pushed apart from each other in opposite directions, with a `vs` glyph
between them sitting on a diagonal streak of warm light. That small push is what
makes the pair read as a confrontation rather than a row. Below, a grid of cards
two across, each headed with the two names and carrying a body naming a specific
limitation, ending in a primary button `Read more`.

### Route: Not found

A single centred block on the page ground, with no announcement bar, no header and
no footer. Everything else on the site has chrome; this has none. The headline at
the section heading size reads `Ooops...` in the heading colour followed by
`error 404` in the gradient-text treatment. The subhead reads `Page not found` in
the body colour at the large body size. One call-to-action button reads
`Back to home`. The block is centred both ways in the window, with the button about
one line-height below the subhead.

### Fixture volume

The front end needs enough content to exercise itself: thirteen routes of typed
sections, four plans with three volume tiers each, thirty connectors across eight
categories with a realistic long tail of popularity, four case studies and three
testimonials. The connector fixture exceeds one page of results so paging is
exercised, and includes one connector whose description is long enough to be
clamped and one whose name is long enough to wrap.

## Constraints

- One installation, two seeded projects. There is no organisation above a project
  and no cross-installation federation.
- No public signup, no password reset, no email of any kind. There is no mail
  vendor in this environment.
- No payment capture and no billing integration. The plan table sells; it does not
  charge.
- No third-party analytics, consent vendor, error reporter, feature-flag service or
  content delivery vendor. No outbound call to any of them at run time.
- No second database, cache, queue, object store or identity provider beyond the
  two named.
- No native application, no desktop client, no browser extension.
- No real-time collaborative editing of a workflow. One person edits at a time.
- No file upload from the browser.
- No conference sub-route. The light conference palette exists only as a rule about
  where it may not appear.
- No binary asset ships with the build: no image file, no video file, no font file
  fetched from anywhere.
- The app must stay responsive with 2 projects, 3 workflows, 30 connectors, 4
  plans, 4 case studies and up to 500 runs each carrying up to 20 step attempts.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of
  the shell. An ordinary background job dies with its shell, and the app will not
  be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy of
  any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `{"email", "password"}` | `{"access_token"}` |
| `GET /api/me` | - | `{"id", "email", "display_name", "instance_role", "projects"}` |
| `GET /api/health` | - | `{"status"}` |
| `GET /api/projects` | - | a top-level array of `{"id", "name", "slug", "project_role"}` |
| `GET /api/projects/{slug}/workflows` | - | a top-level array of `{"id", "name", "slug", "active", "current_version_id", "step_count"}` |
| `POST /api/projects/{slug}/workflows` | `{"name"}` | the created workflow |
| `GET /api/workflows/{id}` | - | `{"id", "name", "slug", "active", "version_number", "steps", "connections"}` |
| `POST /api/workflows/{id}/versions` | `{"message", "steps", "connections"}` | `{"id", "version_number", "created_at"}` |
| `POST /api/workflows/{id}/runs` | `{"mode"}` | `{"id", "status", "workflow_version_id"}` |
| `GET /api/projects/{slug}/runs` | `?status=<status>&page=<n>` | a top-level array of run summaries |
| `GET /api/runs/{id}` | - | `{"id", "status", "mode", "worker_id", "workflow_version_id", "started_at", "stopped_at", "steps"}` |
| `POST /api/runs/{id}/claim` | `{"worker_id"}` | the claimed run, or a client error when already claimed |
| `POST /api/runs/{id}/cancel` | - | the cancelled run |
| `GET /api/projects/{slug}/approvals` | - | a top-level array of `{"id", "run_id", "workflow_name", "step_name", "decision", "deadline_at"}` |
| `POST /api/approvals/{id}/decision` | `{"decision"}` where decision is `approved` or `rejected` | `{"id", "run_id", "decision", "decided_by", "decided_at"}` |
| `POST /api/approvals/token/{token}` | - | the recorded decision |
| `GET /api/projects/{slug}/credentials` | - | a top-level array of `{"id", "name", "credential_type", "fields_set"}` |
| `POST /api/projects/{slug}/credentials` | `{"name", "credential_type", "secret"}` | `{"id", "name", "credential_type", "fields_set"}` |
| `GET /api/projects/{slug}/credentials/{id}` | - | `{"id", "name", "credential_type", "fields_set"}`, never the stored value |
| `GET /api/projects/{slug}/members` | - | a top-level array of `{"user_id", "email", "instance_role", "project_role"}` |
| `PATCH /api/projects/{slug}/members/{user_id}` | `{"project_role"}` | the updated membership |
| `GET /api/projects/{slug}/audit` | - | a top-level array of `{"id", "actor_email", "action", "subject", "occurred_at"}` |
| `GET /api/runs/{id}/logs` | - | a top-level array of `{"run_id", "workflow_id", "project_id", "step_name", "correlation_id", "level", "message", "occurred_at"}` |
| `POST /api/runs/{id}/annotation` | `{"note"}` | `{"run_id", "note", "annotated_at"}` |
| `GET /api/projects/{slug}/insights` | - | `{"total_runs", "failed_runs", "average_duration_ms", "retention_days", "run_output_max_bytes"}` |
| `GET /api/metrics` | - | `{"queue_depth", "jobs_waiting", "jobs_running", "worker_count", "runs_by_status", "active_workflow_count"}` |
| `POST /api/hooks/{workflow_slug}` | any JSON body, optional `Idempotency-Key` header | `{"run_id", "duplicate"}` |
| `GET /api/connectors` | `?q=&type=&category=&partner_built=&sort=&page=&per_page=` | `{"total", "page", "per_page", "results", "facets"}` |
| `GET /api/connectors/{slug}` | - | one connector |
| `GET /api/plans` | `?period=monthly\|annual` | a top-level array of plans with their volumes and features |
| `GET /api/case-studies` | - | a top-level array of case studies |
| `GET /api/case-studies/{slug}` | - | one case study |
| `POST /api/contact` | `{"email", "first_name", "company", "message", "consent", "campaign_source", "campaign_medium", "campaign_name", "referrer"}` | `{"id", "created_at"}` |

Bearer auth is carried on everything except login, health, the public content
endpoints and the inbound trigger receiver. The inbound receiver authenticates by
the workflow's own configured scheme, never by a person's token. A successful call
returns the named resource or shape; an invalid or unauthorized call is rejected as
a client error, never as a server error and never as a silent success. List
endpoints marked above return a top-level JSON array.

### No mocks

The named provider is where the data actually lives. Every one of these is a
contract violation however good the interface looks: an in-memory list of runs that
disappears when the process restarts; a hardcoded approvals payload the app returns
to itself; workflow definitions held in a module-level dictionary rather than in
PostgreSQL; a sign-in that compares a password against a literal in the source
rather than against a stored hash; a run whose status is only ever a value in a
browser tab. The named provider is the fact - the app's UI and its own tables can
only reflect what lives in the provider, never substitute for it.

## Definition of done

A stranger can read the plans, search the node catalogue and open a case study
without signing in. An operator can sign in, draw a workflow on the canvas, save it
as a new version and start a run, and that run queues, reaches a worker, and stops
at the approval step with the run holding no worker. An approver in the same
project can resume it to completion, and the same request from an operator's
session is refused with the run left waiting and nothing recorded against it. A
stored credential value never comes back out of the product, to anyone.
