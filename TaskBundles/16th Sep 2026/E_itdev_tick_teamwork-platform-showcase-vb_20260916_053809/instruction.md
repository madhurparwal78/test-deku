# Northwind

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, read the public estate, compute a price for a team of `300` users, and
then sign in as `member@example.com` and drag the work item `FIN-2` from
`In progress` into `Ready for review`, and see that item's own history gain an
entry naming the member and both status names, without hitting an error page.
The hard part is that the drag is not a column change: the move must be refused
unless the workflow joins those two statuses, the history entry must be a real
stored record rather than something the screen remembers, the automation rule
bound to that transition must set the assignee, and the confirmation email must
arrive in `mailpit` addressed to that new assignee alone.

## Overview

Northwind is two products sold as one. The first is a public marketing estate of
sixteen routes that sells a family of work products. The second is the work
platform those routes advertise: a shared graph of work items that teams move
through configurable states.

A visitor to the estate compares products, reads a customer story, searches a
template catalogue, computes a price for their own team size, and signs up with a
work email. The estate is not one page repeated. It carries three different
header treatments, and which one a visitor sees tells them where they are: the
company chrome on the home and company routes, a product chrome on each product
route, and a legacy chrome that this build retires in favour of the first. On a
product route the whole top strip changes, and a solid blue square appears hard
in the corner, bleeding to the edges of the screen while everything else keeps
its gutter. That square is the estate's single most distinctive detail and it is
what reads as a door back to the company.

A signed-in member opens a project, filters a board with a saved query, and drags
a work item into the next column. Underneath, that asks the workflow whether the
move is allowed, writes the new status, appends an entry to that item's history,
fires the automation rules listening to that transition, and notifies whoever
those rules just made responsible.

The genuinely hard part, and the problem the whole permission design exists to
answer, is that visibility is decided item by item rather than project by
project, so every list, every count and every total a person is shown must be
computed over what that person alone is allowed to see. Tenancy isolation is
absolute: a project is the unit of isolation and no query path may return rows
from a project the asker is not in.

Northwind deliberately is not: a real-time collaborative editor, a separate
search index, a reporting warehouse, a marketplace running customer code, or a
billing system. The estate's own copy advertises some of those, because the
company sells a platform larger than this build. Advertising them is in scope;
building them is not.

## User roles

Three roles. Every account is seeded and the console does not accept signups. The
estate's own signup form is a real entry point and reports an outcome, which is
specified in Core features.

| Role | Can read | Can write | Cannot |
|---|---|---|---|
| `requester` | only the requests they raised, in projects that admit requests | raise a request in a project that admits requests; comment on a request they raised | **see any item they did not raise**, **see any board**, **transition anything**, **see any other person's request** |
| `member` | every work item in the projects they belong to | create, edit, assign and transition items in those projects; save a filter and share it with a project | **see or act on an item in a project they do not belong to**, **change a status, a transition or an automation rule**, **read the page-view log** |
| `admin` | every work item in every project | everything a member can, plus statuses, transitions and automation rules, and reading the page-view log | **nothing within this product** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `member` session
to any `admin`-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged.

Scope is by relationship and not by role alone. A member belongs to a set of
projects, and a project they do not belong to is invisible to them: absent from
the project list, refused at the board, and contributing nothing to any count
they are shown. A requester sees the requests they raised and nothing else, not
even the existence of other requests in the same project.

Seeded accounts, every one using the password `deku-demo-pw-2026`:

| Account | Role | Belongs to |
|---|---|---|
| `admin@example.com` | `admin` | every project |
| `member@example.com` | `member` | `FIN` |
| `member2@example.com` | `member` | `MKT` |
| `requester@example.com` | `requester` | `SUP` |
| `requester2@example.com` | `requester` | `SUP` |

A membership is `invited`, `active` or `deactivated`. A deactivated person keeps
their history entries and their name on past changes, loses every session, and is
excluded from every listing and every permission grant, including one that names
them directly.

## Core features

### Auth

Email and password, implemented by the app. Passwords are stored hashed; the
literal `deku-demo-pw-2026` must work at login for every seeded account. A
successful `POST /api/auth/login` returns `access_token`, the bearer token the
client sends on every later call.
An expired token leaves the attempted action undone and returns the person to
the sign-in route with their destination preserved. The console accepts no
signups.

### The board and the transition

The console's work surface is a split detail pane: the board's columns on the
left, the selected work item on the right, each scrolling independently. Selecting
a card gives the right pane the item and gives the browser the item's own address,
so a selected item is linkable.

1. Dragging a card from one column to another succeeds only when a transition
   joins the card's current status to the target status in that project, or when
   the transition is global. A drag with no such transition is rejected as
   invalid, the card returns to the column it came from, and the item's stored
   status is unchanged.
2. A successful transition writes the new status, appends exactly one entry to
   that item's history naming the person who moved it, the moment, the status it
   left and the status it reached, and leaves the item's key untouched.
3. A transition attempted by a `requester`, or by a `member` in a project they do
   not belong to, is denied, and the item's stored status and history are both
   unchanged.
4. Concurrency is resolved at the item. Two people dragging the same card at the
   same moment do not both succeed.
   Exactly one move is written; the other is refused as a conflict naming the
   status the item has actually reached, and the refused attempt appends no
   history entry.
5. Dragging one card to a new position between two others changes the position of
   that card alone. The other cards in the column keep the positions they had.
6. The card moves into its new column the instant it is dropped, before the write
   is confirmed. If the write is refused the card returns to where it was and a
   message in place says why, replacing the card's own row rather than covering
   the board.
7. A transition carries three kinds of rule and they are three because they run at
   different moments. A condition decides whether the move is offered at all and
   runs every time anybody looks at the item, so it must be cheap and must change
   nothing. A validator decides whether what was submitted is acceptable and runs
   once, when somebody commits the move, so it may be expensive. A post-function
   is what else must happen because of the move and runs after the new status is
   written. Collapsing the condition and the validator into one hook makes opening
   a busy board slower the more rules a customer has written, which is backwards.
8. Executing a transition re-evaluates the person's right to transition and
   re-evaluates every condition, because the set of moves the screen offered may
   be out of date by the time the drop lands.
9. Post-functions run after the new status is committed rather than inside the
   same write, because some of them reach outside the product and cannot be
   undone. Each is retried on failure with a growing backoff and must therefore be
   safe to run twice. The consequence is stated rather than hidden: a transition
   can be complete while one of its post-functions has not finished, and a
   post-function that fails for good leaves the transition committed and raises a
   visible failure on the item rather than being swallowed. Two post-functions
   that both edit the same item run in the order the transition declares, never at
   once. This is the atomicity the product trades away, and what it owes in return
   is that the item's history shows the move and each consequence separately.
10. Editing a workflow produces a draft and the live workflow is untouched until
   it is published. Publishing computes a migration for every status being
   removed or renamed, and is refused until the administrator has named a
   destination status for the items sitting in each. The migration writes a
   history entry per item attributed to the administrator and naming the publish
   as the reason, because work that changes state with no record of why is how a
   team stops trusting the tool. While a migration runs, transitions on the
   affected items are refused with a clear message rather than allowed against a
   half-changed definition.
11. Every feature above is opt-in and none of it is on by default. A project
   created with no configuration gets a simple three-status workflow mapping one
   to one onto the three status categories, with unrestricted transitions and no
   conditions, and somebody who never opens the workflow editor never meets a
   concept from this rule set.

### Automation rules bound to transitions

12. A rule names one transition it listens to, one named actor it runs as, and one
   action. When that transition is executed the rule runs, and every read and
   write the rule performs is subject to what its actor is allowed to see and
   change, not to what the person who triggered it is allowed to see and change.
13. Every action a rule takes appears in the item's history attributed to the
   rule's actor and marked as automated, so a person reading the history can tell
   an automatic change from a typed one.
14. A rule does not fire when it already appears in the chain of the change that
   would trigger it for the same item. Rule executions therefore terminate, and a
   rule that would trigger itself simply does not.
15. Metering counts one rule execution as one metered unit no matter how many
   actions it took, because a meter a customer cannot predict from reading their
   own rule is a billing dispute waiting to happen. The allowance is per plan: `100` rule runs per month on Free, `1700`
   rule runs per month on Standard, `1000` rule runs per user per month on
   Premium, and unlimited on Enterprise. Reaching the allowance queues further
   executions rather than discarding them silently, and a discarded execution is
   still recorded with the reason.
16. Editing a live rule creates a new version, and a past execution reads against
   the version that ran rather than the version that exists now.
17. A rule's body is a tree rather than a list. A component is a condition that
   stops the branch when its predicate is false, an action that has an effect, a
   branch that selects a set and runs its sub-tree once per member, or a
   conditional block choosing between sub-trees. A branch that selects zero
   entities is not a failure; it is the commonest outcome and must not raise.
   Branch bodies run one after another, and branching is capped per execution
   rather than per branch, so nesting cannot multiply the cap.
18. A rule interpolates values from the item that triggered it into the text it
   writes. That interpolation is a closed template vocabulary with property
   access and a fixed set of functions, never arbitrary code, and every
   interpolated value is escaped for wherever it is going, so an item summary
   can never become an injection into something else. A path that resolves to
   nothing yields empty and records a warning on the execution rather than
   aborting the rule, because a rule that stops because one optional field was
   blank is a rule that fails in the middle of the night.
19. Creating or editing a rule requires a right that is not granted by default,
   and the actor a rule runs as must be a principal its editor is themselves
   allowed to act as. Without that, anyone who can write a rule can write one
   that reads everything in the site.

The seeded rule is `Assign review to the project lead` on project `FIN`. It
listens to the transition `Send to review`, runs as `admin@example.com`, and sets
the item's assignee to that project's lead. Because `FIN-2` starts with no
assignee, moving it into `Ready for review` is what makes the rule observable.

### Notification

20. When an automation rule changes an item's assignee, the app sends one email
   over real SMTP at `SMTP_HOST` and `SMTP_PORT` to the new assignee's address
   alone, with no cc and no bcc.
21. The subject begins with `Northwind work update:` followed by a space, the
   item key, a space, and the item summary. Moving `FIN-2` into
   `Ready for review` therefore produces the subject
   `Northwind work update: FIN-2 Validate transaction UX`.
22. The body is not empty and names the item key, the status the item reached and
   the person who moved it.
23. No email is sent for a transition that leaves the assignee unchanged, for an
   edit to a summary or description, or for a comment. The person who performed
   the change is never the recipient of the notification for their own change: a
   rule that would assign an item to the person who just moved it sends nothing.

### Per-item visibility

24. Every listing, every board and every search result contains only items the
   asking person is allowed to see.
25. Every count and every total shown to a person is computed over that person's
   own visible set. A person who may see one of the nine seeded items in `FIN`
   and `MKT` is shown a total of one, never nine. A count that reveals how many
   items exist beyond a person's reach is itself the leak.
26. Requesting an item directly by its key, from a session with no right to it,
   is denied rather than answered with an empty body or a redirect.
27. Visibility is granted through a permission scheme attached to a project, and
   a scheme is attached to more than one project so an administrator can change
   a rule once for several. Changing a scheme does not rewrite every affected
   item while the administrator waits: the change takes effect for every project
   the scheme is attached to, and until the incremental recomputation behind it
   has caught up, every affected listing is answered by the slower per-item
   evaluation instead. Correct and slow, never fast and wrong. An item whose
   visibility cannot currently be determined is absent from listings rather than
   present with a stale answer, because absent is safe and stale is not.
28. The two ways of answering the same question, the fast listing filter and the
   careful per-item check, must agree. Testing that they agree is part of the
   product: a check picks people, permissions and items and compares both
   answers, and a disagreement is a defect rather than a tolerance.
29. A permission-aware aggregate is the only kind. Any count, total or chart is
   computed over the asking person's own visible set and never from a stored
   figure that ignored who was asking.
30. A comment carries its own visibility, evaluated separately from the item's.
   An item a person may read can contain a comment they may not, and the item
   must render with no trace of it: no count, no gap, no marker saying one is
   hidden. Per-field visibility is deliberately not offered; where it would be
   wanted, the answer is a separate item.

### The query language and saved filters

31. A member can write a query over the item set, save it under a name, and share
   it with a project. The language supports a field, an operator and an operand,
   joined by `AND` or `OR`, with an optional `ORDER BY`. The operators are `=`,
   `!=`, `IN` and `WAS`. `NOT` binds tightest, then `AND`, then `OR`, and the
   precedence is the language's own rather than any host language's.
32. `WAS` asks the item's history rather than its current row, so
   `status WAS "Ready for review"` selects items that reached that status at some
   point even if they have since left it. A history clause is planned separately
   from a current-state clause and always after it: the planner narrows with the
   current-state clauses first and only then goes to the history, never the
   reverse, because the history is much larger than the thing it describes.
33. The function `currentUser()` resolves to whoever is asking, not to whoever
   saved the filter. The seeded filter `My open work` is owned by
   `member@example.com`, shared with `FIN`, and its text is
   `assignee = currentUser() AND status != Done ORDER BY rank ASC`.
34. Running a shared filter returns the reader's own visible set. Two people
   running the same saved filter see different items, and neither sees an item
   the permission rules deny them. A saved filter is a shared question and never
   a shared answer.
35. A subscription runs a saved filter on a schedule and executes as the
   subscriber, never as the filter's owner. Executing as the owner is a
   straightforward way to mail somebody a list of items they are not allowed to
   see, and it is an easy mistake because the owner is the name closest to hand.
36. A query that names a field the site does not define is refused with a message
   naming the offending token and the caret position, rather than silently
   returning everything or nothing. Customers write these by hand.
37. Every execution carries a budget and exceeding it returns a structured
   message naming the limit rather than a timeout. The budget bounds the parse
   depth, so a pathological nested expression is refused; the clause count after
   normalisation; a candidate ceiling on how many rows may be examined before
   the query aborts; and the number of executions running at once for one person.
   A message saying which bound was reached and suggesting a narrowing clause
   resolves itself; a timeout teaches the customer nothing.
38. A saved filter may reference another saved filter, which makes a cycle
   possible. A save that would create one is refused at the moment of saving
   rather than discovered when somebody runs it, and deleting a filter that a
   board or another filter references is refused with the referencing objects
   named.

### The estate: signup, forms and consent

39. The product routes carry a real signup form asking for a work email. One
   submission produces one of three outcomes, decided by the address's domain:
   an address at a domain already claimed by an organisation with open enrolment
   joins that organisation's site; an address at a claimed domain whose
   enrolment is by approval creates a pending request and says plainly that the
   person is waiting; an address at an unclaimed domain, including a free-mail
   address, starts a new organisation. A free-mail address is accepted and not
   rejected.
40. Every form rejects invalid input in place, names the field it is complaining
   about, and writes nothing. The field keeps what was typed. Placeholder text is
   never the only label a control has.
41. A first-time visitor is asked once about non-essential cookies, with accept,
   reject and manage offered as three controls of equal visual weight. Nothing
   that measures a visitor runs before that decision. Closing the dialogue
   without choosing counts as declining, and declining is remembered for as long
   as accepting is.
42. No form anywhere in the estate collects a password, a payment instrument or a
   government identifier.

### The estate: pricing

43. The pricing route carries a team-size field and a billing-period choice of
   `Monthly` or `Annually`. Changing either recomputes every figure on the page
   as the digits are typed, with no page reload and no network request: the rate
   tables arrive with the page. Dragging the team size from `10` to `10000` must
   issue no request at all.
44. Rates are graduated bands, so the users in each band are charged that band's
   rate and the displayed per-user figure is the total divided by the team size.
   Figures are computed at full precision and rounded once, at the point of
   display.

Monthly rates, in integer minor units of `usd`, per user per month:

| Band | Standard | Premium |
|---|---|---|
| users 1 to 10 | `850` | `1700` |
| users 11 to 100 | `760` | `1520` |
| users 101 to 1000 | `640` | `1290` |
| users 1001 and above | `520` | `1050` |

Annual rates, in integer minor units of `usd`, per user per year:

| Band | Standard | Premium | Enterprise |
|---|---|---|---|
| users 1 to 10 | `8500` | `17000` | not sold |
| users 11 to 100 | `7600` | `15200` | `26400` |
| users 101 to 1000 | `6400` | `12900` | `22800` |
| users 1001 and above | `5200` | `10500` | `18600` |

Worked examples, which the app must reproduce exactly:

| Team size | Plan | Period | Total | Displayed per user |
|---|---|---|---|---|
| `300` | Standard | Monthly | `204900` | `683` |
| `7` | Standard | Monthly | `5950` | `850` |
| `300` | Premium | Monthly | `411800` | `1373` |

The first row is the one that disambiguates the algorithm: `10` users at `850`,
then `90` at `760`, then `200` at `640` is `204900`, which divides exactly. The
third row disambiguates the rounding: the true quotient runs past two places and
is rounded once for display.

45. Free is always a total of `0` and is capped at `10` users. Above `10` users
   the Free column shows the words `Not available above 10 users` in place of an
   amount. Enterprise shows no amount at all while `Monthly` is chosen, and in
   its place a sentence whose words `Billed annually.` are a link that moves the
   shared billing choice to `Annually`, so the whole table changes with it and
   not that column alone.
46. The saving badge reads `SAVE UP TO 17%` and sits after the `Annually` option.
47. The team size and the billing period are both carried in the address, so a
   computed view can be sent to somebody else and restored from the address on
   load.

### The estate: catalogue, stories and content

48. The template catalogue carries a search band and three facets that combine:
   product, team and type. The teams are `Software`, `Marketing`, `IT`,
   `Product`, `Design`, `HR`, `Finance`, `Legal` and `Operations`. The types are
   `board`, `document`, `whiteboard`, `form` and `dashboard`. Every facet value
   shows how many results it would return, the counts update as other facets are
   applied, and a value that would return nothing is shown disabled rather than
   removed, so the shape of the catalogue stays legible.
49. The search query and every applied facet are carried in the address. The
   search field sits in a form with a submit, so pressing return works before
   any script has run.
50. A customer story carries exactly three labelled paragraphs, `Challenge:`,
   `Solution:` and `Impact:`, as three separate fields. A story missing any one
   of the three cannot be published.
51. An announcement carries a real start and end moment and the estate computes
   its own relevance from them, so a strip naming a date takes itself down once
   that date has passed rather than advertising a deadline that went by.
52. Dismissing an announcement strip is remembered against that strip's own
   content, so changing the words brings it back and re-reading the same words
   does not.

### The estate: the launch surface

53. The site serves a favicon and declares it in the document head.
54. Every public route declares a social preview title and a preview image, and
   the image resolves.
55. A terms page is reachable from the footer of every page and is linked from
   the signup form.
56. Each page view is recorded with the route it names and the moment it
   happened, and an `admin` can read that log. Nobody else can.
57. An unknown address renders Northwind's own not-found page, carrying the full
   header and the full footer, and answers with a not-found status rather than a
   success. The page's search field arrives prefilled with a guess taken from
   the address that was tried: its last segment with separators turned into
   spaces.

## User flow

### Routes

The information architecture is the route table below plus the navigation tree
above it. Every route must exist, must be reachable, and must paint its first
response without client-side scripting. The two collection routes render from
data rather than from one template per instance.

| Route | Purpose | Auth |
|---|---|---|
| `/` | the scroll-journey landing route | public |
| `/products` | the product hub, a card grid | public |
| `/products/work` | the work product, signup hero | public |
| `/products/work/pricing` | the calculating pricing table | public |
| `/products/docs` | the knowledge workspace product | public |
| `/products/service` | the service management product | public |
| `/products/ai` | the assistant product, centred hero | public |
| `/platform` | the platform explainer, anchor nav | public |
| `/enterprise` | the enterprise segment route | public |
| `/customers` | the customer story index | public |
| `/customers/<slug>` | one customer story | public |
| `/templates` | the template catalogue | public |
| `/migration` | the migration programme route | public |
| `/teams/<slug>` | one solution-by-team route | public |
| `/company/contact/<slug>` | the contact form route | public |
| `/terms` | the terms page | public |
| `/login` | sign in | public |
| `/app` | redirects to the project list | signed in |
| `/app/projects` | the project list | signed in |
| `/app/projects/<key>` | the board, split detail pane | member of that project, or `admin` |
| `/app/projects/<key>/items/<item_key>` | the same board with that item selected | member of that project, or `admin` |
| `/app/projects/<key>/filters` | saved filters for that project | member of that project, or `admin` |
| `/app/projects/<key>/rules` | automation rules | `admin` |
| `/app/projects/<key>/workflow` | statuses and transitions | `admin` |
| `/app/requests` | a requester's own requests | `requester` |
| `/app/insights` | the page-view log | `admin` |

### Entry and redirects

An unauthenticated request for any console route lands on `/login` and, after a
successful sign-in, continues to the address that was asked for. A sign-in with
no pending destination lands on `/app/projects`. Signing out returns to `/login`
and the previous session's token stops working. A token that expires part-way
through an action leaves that action undone. A signed-in person who is neither a
member of a project nor an `admin` is refused that project's board and is not
shown the project in their list.

Navigation is a drill-down and the breadcrumb is the navigation. Above the
project list every console route shows `Projects / <project name> / <item key>`
as far as it has gone, and each segment is a link back up a level.

### Journeys

1. **A visitor prices a team of three hundred.** Open `/products/work/pricing`.
   Type `300` into the team-size field. Every figure below recomputes as the
   digits land, and Standard shows a total of `204900` with `683` per user.
   Choose `Annually`. Every figure recomputes again, the badge `SAVE UP TO 17%`
   stays, and Enterprise now shows an amount where it showed none. The address
   carries both choices, and reloading the page restores them.
2. **A visitor narrows the catalogue.** Open `/templates`. Type into the search
   band. The results settle and update. Apply the product facet, then the team
   facet `IT`. The counts beside the remaining values drop, and a value that
   would now return nothing is shown disabled. The address carries the query and
   both facets, and sending that address to somebody else opens the same view.
3. **A member moves a work item.** Sign in at `/login` as `member@example.com`
   with `deku-demo-pw-2026`. Open `/app/projects/FIN`. Apply the saved filter
   `My open work`. Drag the card `FIN-2` from `In progress` into
   `Ready for review`. The card lands in the new column at once. The right pane
   shows `FIN-2` with its new status, an assignee the rule
   `Assign review to the project lead` has just set, and one new history entry
   naming `member@example.com`, `In progress` and `Ready for review`. One email
   arrives in `mailpit`, addressed to the new assignee alone, with the subject
   `Northwind work update: FIN-2 Validate transaction UX`.
4. **A member is refused another project.** Sign in as `member2@example.com`, who
   belongs to `MKT` and not to `FIN`. Ask for `/app/projects/FIN` directly. The
   request is denied, `FIN` does not appear in the project list, and no listing
   returns a `FIN` item. The count of items shown is computed over `MKT` alone.
5. **A requester raises and is contained.** Sign in as `requester@example.com`.
   Open `/app/requests` and raise a request in `SUP`. It appears. Sign in as
   `requester2@example.com` and open `/app/requests`. The first requester's
   request is absent, and asking for it directly by key is denied.

### States

Every list has an empty state that names what would fill it rather than showing
an empty frame. Every route has a loading state. A refused save leaves the card
where it was and explains in place. A component that fails renders its own empty
state and does not take the route down with it; a route that fails renders the
not-found page with the matching status. An unknown address is the not-found page
and not a redirect to the home route.

## UI/UX notes

The estate and the console are two registers of one product and the brief keeps
them apart. The estate is a shop window and may carry atmosphere, with the
subject seen before any decoration. The console is an operational surface: quiet,
dense but organised, built for scanning and for the same action repeated a
hundred times. What somebody should understand in the first moment is that one
company sells several products over a single shared graph of work, and that they
can see their own part of it. Comprehension over persuasion in the console, and
the subject over the frame on the estate.

**Palette, by role.** The page and card ground is a near-white neutral. Inset
regions and the banded rows of the comparison matrix sit on a fractionally darker
near-white neutral, row hover a step darker again, and a press darker still;
those four must stay tellable apart without a rule drawn between them. Body copy
is a deep neutral and headings are a separate, darker near-black neutral, which
is a deliberate difference and not an oversight. Secondary copy is a mid cool
neutral, captions and eyebrows a lighter one, and form outlines a light cool
neutral. One mid, vivid blue carries the brand, every link and the primary
action, deepening to a soft blue on pointer-over and to a deep, muted blue on
press; the focus ring is a light, vivid blue and the tinted announcement bands a
near-white cool neutral. A visited link is a mid, soft indigo that deepens to a
deep, muted indigo and is reused for nothing else.

Three colours carry meaning and appear nowhere else in the interface: a mid,
vivid red for something that has gone wrong, a deep, soft lime for something that
worked, and a light, vivid amber for something still in progress. Success is a
lime and not the deep, soft teal that also exists in the scale, which is a brand
decision worth reproducing rather than tidying away. Nothing but a warning ever
uses the amber ground, and inverse text is never set on it. Beside those sits a
ten-hue accent scale at four depths, named blue, gray, green, lime, magenta,
orange, purple, red, teal and yellow, whose members include a mid, soft magenta,
a mid, vivid orange, a deep, vivid orange, a deep, vivid amber, a mid, soft cyan
and a mid, soft indigo. It exists to colour things a customer created, and a
project or a label takes its hue from a stable hash of its own identifier, never
at random, so the same project is the same colour in every session and to every
person. The near-white, muted blue and the deep cool neutral in that scale are
for tinted panels. The exact values are yours, so long as every pairing clears
the bar below and no meaning colour is borrowed for a state that is none of the
three.

**Type.** Two variable families: `Northwind Sans` across weights `100` to `900`
in upright and italic for everything, and `Northwind Mono` across `100` to `800`
for identifiers and for figures that must line up in a column. Headings are set
at weight `653`, which is exact on a variable axis and rounds to `700` on a
static fallback. The fallback stack is `ui-sans-serif, -apple-system,
BlinkMacSystemFont, "Segoe UI", Ubuntu, "Helvetica Neue", sans-serif`, reproduced
exactly because its metrics were chosen so that no line of text moves when the
real face arrives.

**Shape and density.** Corners round by what a thing is rather than uniformly:
form fields barely at all, badges and chips a little more, cards generously,
primary buttons fully as lozenges, icon buttons as circles. There is one border
width in the whole system. The estate reads comfortable and the console reads
compact, with board rows sitting tight enough that a full column fits one screen.

**Motion.** Everything moves on one small set of characters, and the character is
eased: things that arrive rise a short distance while fading in, and when several
arrive together each waits a fraction behind the one before so a row of cards
lands like a dealt hand rather than one slab. Things that slide in start exactly
off the edge of the screen whatever its width and creep the last part of the
distance, which is what makes them feel heavy. Four named roles cover every
transition in the product: one for interaction, one for entry with an instant
start and a long tail, one for things settling, and one for panels and drawers.
The logo band is three rows sliding at three different speeds so it never reads
as one block, it fades out at both ends rather than being cut off, and it pauses
on pointer-over and on focus within. Nothing declares a transition on every
property. Under a reduced-motion preference every reveal resolves immediately to
its end state, the logo band stops, the home route's journey does not pin, and
transitions shorten rather than vanish so that completion still fires.

**Accessibility.** Text and its ground meet a contrast ratio of `4.5:1`, and
large display text meets `3:1`. Every interactive target is at least `44px` in
its smaller dimension at the narrow band. Focus is never removed, only restyled,
and the ring is drawn outside the control's own box so it stays visible on a
filled button. Full keyboard navigation reaches every control in document order,
a skip link is the first focusable element on every route, and the mega-menu is
removed from the accessibility tree while closed rather than merely made
transparent, because a transparent panel of several hundred links is still
several hundred links and still a stop each. Icon-only controls carry an
accessible name, meaning is never carried by colour alone, and every decorative
shape is hidden from assistive technology while every informative illustration
carries a description of what it shows.

**Responsive.** Three bands separated by two breakpoints: narrow, middle and
wide. The content column is fixed and centred at the wide band with generous
gutters, goes fluid below it, and the gutters halve and halve again as the
viewport narrows. At the middle band the header nav folds to a hamburger, card
grids go from three across to two, and the pricing table goes from four columns
to two. At the narrow band everything is one column, the comparison matrix
becomes one plan at a time behind a plan selector, and the home route's journey
does not run at all. The fold is decided by the band and never by measuring
whether the nav happens to fit, because measuring means a longer translation
silently changes when it folds. Display sizes interpolate between the bands so a
two-line headline does not flip to three and back across a few pixels of resize;
body sizes step instead. The layout holds at every width between the named bands,
and nothing scrolls sideways. Every hover-only affordance has a tap equivalent or
does not matter on touch: the card lift needs none, the mega-menu does and gets
the drawer, and the horizontal card rail is swipeable while keeping its arrow
controls, because a swipeable region with no visible control is undiscoverable.
The narrow-band drawer traps focus while open, returns focus to the button that
opened it on close, closes on `Escape`, and stops the page behind it scrolling
without moving its scroll position. A row that opens a mobile submenu carries the
small right-pointing chevron, and that submenu opens in place beneath its row
rather than sliding the drawer sideways.

**One primary action.** Each page leads with exactly one primary action, visually
distinct from every secondary one, and a page with two things competing for that
role has none.

**What it must not look like.** Not a page dominated by a single hue family with
no second signal. Not decoration standing in for content. Not a marketing
composition where the working board belongs. And the home route's board
illustration must not read as a screenshot of software: one card is knocked
slightly out of the grid and one carries a hand-drawn scribble, and without those
two the whole thing reads as a photograph of a product rather than a drawing
about one.

## Technical requirements

The frontend is `React` with `Vite`. The backend is `Flask`. The rendering model
is a single-page application over a JSON interface: the browser receives an
application shell and each route's data arrives as JSON from the same origin
under the `/api` prefix. The public estate's routes are additionally rendered
into that first response at build time and made interactive afterwards, so every
public route shows its content with no script available. No route needs script to
display its content or to follow a link.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing services available in this environment are
`postgres` and `mailpit`, and reaching for anything else is a contract
violation.

The datastore is PostgreSQL, reached at `DATABASE_URL`. Mail is sent over real
SMTP to `mailpit`, reached at `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and
`SMTP_PASS`. Both are already running and reachable at those variables. Do not
download, install, compile or start a copy of either. Never hardcode a host or a
port; read every one from the environment.

Auth is email and password implemented by the app, with bearer tokens on every
call except login and health. Passwords are stored hashed. `GET /api/health`
returns `200` once the app is ready. Application logs are written to standard
output.

Interactivity is added to the delivered markup one component at a time rather
than by rebuilding the page, and the set of components that need it is small and
known: the mega-menu, the pricing calculator, the catalogue search and its
facets, the tab strips, the accordions, the card rail, the forms, the board, and
the home route's journey. Only the journey runs continuous work.

State is kept in four places and they do not mix. The current route and its data
belong to the router. Anything two people might want to share a link to belongs
in the address: the pricing team size and billing period, and the catalogue query
and facets. Anything private to the moment belongs to the component: a menu open,
a drawer open, an accordion open. A visitor's own preferences belong in
persistent storage: a dismissed strip, the consent decision, the chosen locale.
Putting a shared control in component state is the single most likely thing to
get wrong here, and it works perfectly until somebody sends a colleague a link.

Addresses follow three rules. A trailing slash is stripped and redirected with a
permanent redirect. The locale is a path prefix and never a query parameter or a
cookie. A product route and its children share a prefix, so choosing which chrome
to render is a prefix match rather than a lookup table. A collection detail route
takes a slug that is fixed when the record is published and never edited
afterwards, because those addresses are linked from outside; changing a published
slug creates a redirect from the old one automatically.

Localisation: every content field is translatable and falls back through a chain
declared per locale rather than assumed. A partly translated record publishes
with fallbacks rather than being withheld, and the payload marks which runs are
untranslated so the estate can declare their language. Line lengths were
art-directed around the source language, so every translatable field carries a
character budget and exceeding it is a publishing warning rather than a silent
overflow.

Structured data and discovery: product routes, story routes and the catalogue
emit structured metadata describing themselves, and a sitemap is generated from
the published set rather than maintained by hand, excluding anything not
published in the current locale.

Instrumentation: one analytics container, gated on the consent decision,
receiving a small named and versioned set of events rather than automatic
capture. The named events are signup submitted, signup outcome, plan control
changed, catalogue query, facet applied, story video played, journey skipped and
journey completed. That last pair is how anyone ever learns whether the most
expensive thing on the estate earns its cost.

The performance budget, per route, at the wide band and compressed over the wire:
markup within `60 KB`, blocking stylesheet within `40 KB`, blocking script at
`0 KB`, deferred script on first load within `180 KB`, fonts on first load within
`120 KB` across two faces, above-the-fold imagery within `200 KB`, and no video
byte at all before a play control is used. Two font files load, not fourteen, and
the upright face alone is preloaded, subset to the Latin range for the default
locale with further ranges loaded on demand. Set explicit metric overrides on the
fallback stack so the swap to the real face moves no line of text. Every image
declares its dimensions or an aspect ratio. The home route's journey loads
everything it needs before it pins and fetches nothing while pinned, animates
nothing that forces the browser to recompute layout, and takes its reserved
scroll distance from a fixed value rather than by measuring rendered content, so
the first frame is correct and the page never resettles after load.

The site serves a favicon and declares it in the document head, and every public
route declares its own title, its own description and a social preview title and
preview image, with no two routes sharing them.

The estate is rendered by the application for every status it can produce,
including not-found. The delivery layer in front of it forwards and never answers
with an error document of its own, because such a document carries no navigation,
no branding and no way back.

## Data model

Sixteen tables. All timestamps are UTC.

Two properties shape the whole model and are worth stating before the tables. The
schema is per-tenant and editable while the product is running: which statuses
exist, which transitions join them and which automation rules watch them are
customer data rather than product code, and an administrator can change them this
afternoon. And history is a first-class entity rather than a side effect, and it
grows larger than the items it describes, because a question about how things
were cannot be answered from how things are.

Every entity below carries an internal identifier that is opaque and sortable,
separate from any identifier a person reads. No identifier encodes the project or
the site in a way somebody could vary to reach another one: scoping is enforced
by the query, never by the shape of a key.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account
so a grader can sign in.

`users` - `id`, `email` unique, `name`, `role` one of `requester`, `member`,
`admin`, `membership_state` one of `invited`, `active`, `deactivated`, `active`.

`projects` - `id`, `key` unique, `name`, `lead_id`, `admits_requests`,
`archived`.

`project_members` - `project_id`, `user_id`, unique together.

`statuses` - `id`, `project_id`, `name`, `category` one of `to_do`,
`in_progress`, `done`, `position`. The category, not the name, is what a board
colours by and what a count groups on, which is how a project can carry many
statuses and still report meaningfully.

`work_items` - `id`, `project_id`, `item_key`, `summary`, `description`,
`item_type`, `status_id`, `assignee_id`, `reporter_id`, `rank`, `created_at`,
`updated_at`. `item_key` is `<PROJECT KEY>-<n>` from a per-project sequence, is
unique within the project, is what people quote to each other, and never changes
once assigned. `rank` is a string that sorts lexicographically rather than a
number, so there is always room to write a new value between any two existing
ones.

`work_item_parents` - `child_id`, `parent_id`. Items form a forest rather than a
tree: an item has at most one parent, a parent sits at a higher level of the
hierarchy, and the depth is bounded by how many levels the customer has defined
rather than by a constant. A cycle must be impossible, so a reparent that would
close a loop is rejected at the moment it is attempted rather than detected
later.

`sprints` - `id`, `project_id`, `name`, `state` one of `future`, `active`,
`closed`, `start_at`, `end_at`, `goal`. A board may group its items by sprint.

`transitions` - `id`, `project_id`, `name`, `from_status_id` which is null for a
transition available from every status, `to_status_id`, `required_role`.

`history_entries` - the item's audit trail, and it is immutable: an entry is
appended and then never changed, so the trail can be trusted as evidence of what
happened rather than as a summary somebody could revise. Columns are `id`,
`item_id`, `actor_id`, `at`, `field`, `from_value`,
`to_value`, `from_display`, `to_display`. Both the stored identifier and the
rendered name are kept, because a status can be renamed later and a two-year-old
entry must still read correctly. Entries are appended and never updated or
deleted.

`automation_rules` - `id`, `project_id`, `name`, `trigger_transition_id`,
`actor_id`, `action`, `action_value`, `state`, `version`, `runs_this_period`.

`rule_executions` - `id`, `rule_id`, `rule_version`, `item_id`, `actor_id`,
`chain`, `outcome`, `at`, `metered_units`. `chain` records the rules that led to
this execution and is what makes a repeat visible.

`saved_filters` - `id`, `owner_id`, `name`, `query_text`, `share_scope`.

`page_views` - `id`, `route`, `at`, `viewer_id`.

`products` - `id`, `slug`, `name`, `mark`, `blurb`, `audiences`, `collections`,
`nav`, `featured`, `order`, `state`, `locale`.

`stories` - `id`, `slug`, `customer`, `person`, `role`, `quote`, `industry`,
`user_count`, `region`, `products`, `challenge`, `solution`, `impact`,
`outcomes`, `state`, `locale`.

`templates` - `id`, `slug`, `name`, `product`, `team`, `type`, `structure`,
`state`, `locale`.

`team_solutions` - `id`, `slug`, `team`, `hue`, `headline`, `subhead`, `tabs`,
`state`, `locale`.

`plans` - `id`, `tier`, `strapline`, `rate_table`, `inclusions`, `features`,
`state`, `locale`.

`announcements` - `id`, `body`, `link`, `start_at`, `end_at`, `severity`,
`scope`, `state`, `locale`. `start_at` and `end_at` are real moments and the
estate computes its own relevance from them.

A content record is `draft`, `in review`, `scheduled`, `published` or `archived`,
and `archived` is reachable only from `published`. A scheduled record is simply
not visible before its moment.

Derived rather than stored: an item's project key prefix, every price on the
pricing route, every facet count in the catalogue, and the relevance of an
announcement.

**Invariants, stated as properties of the running system.** An item key is unique
within its project and never changes. A transition is refused unless a transition
row joins the item's current status to the target status in that project or is
global. Two simultaneous transitions of the same item do not both succeed:
exactly one is written and the other is refused as a conflict, and the refused
one leaves no history entry and no partial state. Moving one card between two
others changes the position of that one card and no other. A history entry, once
written, is never updated and never deleted. A rule that appears in the chain of
the change that would trigger it does not fire for that item. One rule execution
counts as one metered unit. Every count returned to a person equals the number of
items that person is permitted to see.

**Seed data.** Three projects: `FIN` named `Banking Portal` led by
`member@example.com`, `MKT` named `Campaign Refresh` led by
`member2@example.com`, and `SUP` named `Service Desk` led by
`admin@example.com`. `SUP` admits requests; the other two do not.

`FIN` and `MKT` each carry four statuses in this order: `Blocked` in category
`to_do`, `In progress` in `in_progress`, `Ready for review` in `in_progress`, and
`Done` in `done`. `SUP` carries three: `To do`, `In progress`, `Done`, one per
category.

Nine work items:

| Key | Summary | Status | Assignee |
|---|---|---|---|
| `FIN-1` | `Partner review of banking portal` | `Blocked` | `member@example.com` |
| `FIN-2` | `Validate transaction UX` | `In progress` | none |
| `FIN-3` | `QA banking portal front-end` | `Ready for review` | `member@example.com` |
| `FIN-4` | `Build transaction service` | `Done` | `member@example.com` |
| `FIN-5` | `Document reporting requirements` | `Blocked` | none |
| `FIN-6` | `Develop account creation service` | `In progress` | `member@example.com` |
| `MKT-1` | `Draft rollout strategy` | `In progress` | `member2@example.com` |
| `MKT-2` | `Map chart of accounts` | `Blocked` | none |
| `MKT-3` | `Develop main account screens` | `Ready for review` | `member2@example.com` |

`FIN-2` carries no assignee on purpose: it sits one transition short of
`Ready for review`, which is the transition the seeded rule listens to.

`FIN` and `MKT` each carry a transition between every adjacent pair of their
statuses, in both directions, so a card can move one column at a time either way.
A pair that is not adjacent has no transition, so `Blocked` to `Done` is not a
legal move. The transition from `In progress` to `Ready for review` is named
`Send to review`. A newly created item starts in its project's first status. `FIN`
also carries the automation rule
`Assign review to the project lead` bound to it, running as
`admin@example.com`, whose action sets the item's assignee to the project's lead.
`FIN` also carries the saved filter `My open work`, owned by
`member@example.com`, shared with `FIN`, with the text
`assignee = currentUser() AND status != Done ORDER BY rank ASC`.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual specification in full. Nothing in it changes a
rule stated above.

### The design system

Every visual value resolves from a named token and no component carries a literal
colour. The naming grammar is a role, an optional hue, a depth and an optional
interaction state, where the roles are background, border, text, icon, link,
surface, shadow, space, blanket, skeleton, opacity, interaction, elevation and
font; the depths are bolder, bold, boldest, subtle, subtler and subtlest; and the
states are hovered and pressed. A colour that is not in the token table is a
defect and not a variant. Some token identifiers are contract because other
things read them: the tinted band ground is `--ds-background-brand-subtlest` with
`--ds-background-brand-subtlest-hovered` beside it, and the warning pair is
`--ds-background-warning-bold` with `--ds-text-warning`. Inverse text is never
set on that warning ground.

Space runs on one small base unit, with every step a multiple of it and negative
counterparts for the same steps. Elevation has three levels and no more: a raised
level for a resting card, an overlay level for a panel that sits above the page,
and an overflow level for a surface whose content runs past its edge. A card at
rest already carries a shadow the same colour as the page and of no size, which
exists only so the hover shadow has something to grow from, and that is what makes
the lift read as smooth rather than abrupt.

Corner radii vary by component and the variation is the system, not an accident:
form fields and legacy controls barely rounded, badges and tags slightly more,
mega-menu row hit areas and search fields rounded further, cards and card media
generously, primary buttons fully as lozenges, and circular icon buttons. A pill
whose height comes from its content uses a very large radius rather than a
percentage; a percentage is used only where the box is known to be square.

A disabled control drops in opacity, loses its pointer events and is declared
disabled to assistive technology. A lowered opacity on its own is not a disabled
state.

The layout column is fixed and centred at the wide band with generous gutters,
capped so it stops growing past the widest band, and the header row, the hero
copy column and every card grid align to it. Card grids are three across at the
wide band inside that column.

The source estate carries two live inconsistencies and neither is inherited here.
It is halfway through a repaint and carries two generations of its palette at
once, with a few older routes still painting from the earlier one; and it runs
two content systems at once, the newer routes out of one and the older out of
another. Build one palette, the newer generation described in UI/UX notes, and
one content source, everywhere. A half-finished repaint is a thing to inherit
deliberately or not at all.

### The motion vocabulary

The vocabulary is closed. Bind every movement in the product to one of four named
roles and use the role name in component code rather than restating a curve: an
interaction role for colour, scale and fade on pointer-over, an entry role that
starts instantly and has a long tail, a settle role for things that arrive, and a
panel role for drawers and menus. Two further characters exist in the source and
are worth naming so nobody invents a fifth: a long decelerate for large surfaces,
and a symmetric ease where a thing must feel the same going out as coming in. A
near-duplicate of the default ease is a defect rather than a variant; collapse it
onto the default.

The named reveals are three. A reveal on entry, which is the estate's standard:
the element rises a short distance while fading in, and siblings stagger so each
starts a fraction after the one before. A slide in from the side, used on list
items in a horizontally assembling region, starting exactly off the edge of the
screen whatever its width. And a headline and paragraph fade that runs once and
stays arrived.

Two spinners, and only two. The indeterminate spinner turns forever and its
rotation is deliberately not even: it lurches forward early and again past the
middle, which is what makes a wait read as progress rather than as a stuck wheel.
The overlay spinner turns evenly and completes one full rotation each cycle.
Both keep turning under a reduced-motion preference, because a still spinner
communicates nothing.

Loading and progress keyframes sweep a highlight across the placeholder, once
narrow and once wide. Move a fixed-size shape rather than growing and
repositioning a real box, so the browser is never asked to recompute layout on
every frame.

The marquee of the logo wall is three rows at three speeds, the slowest taking
well over a minute to come round.

The declared transitions the estate actually relies on are few: the mega-menu
panel's fade, a card's lift and its shadow, a link's colour, an image's fade-in,
the moving indicator under a tab strip, an icon button's press, the focus ring's
overshoot, the accordion's opening, and the progress bar's fill. Name the
properties each one animates. A transition declared on every property is a
performance defect rather than a design decision, and the source carries tens of
thousands of them.

### Iconography

Every mark is drawn as geometry in the page. No icon font, and no icon fetched as
a separate request. One component per mark, sized by a single value that sets both
dimensions. Stroked marks take the colour they inherit; filled marks do too unless
the mark is a brand lockup. An icon that is the only content of a control carries
an accessible name; an icon beside a text label is hidden from assistive
technology.

The marks the estate needs: a small downward chevron beside every mega-menu
trigger and every disclosure row, drawn as three points joined by a stroke with
round caps and joins; a small right-pointing chevron meaning "this row opens a
submenu"; a larger downward chevron for accordions and for the comparison
matrix; a filled downward chevron for dense controls where a stroke would read
too heavy; a search mark drawn as one shape with the lens punched out as a hole
rather than as a stroked circle with a line stuck on, so whatever sits behind it
shows through; a small right-pointing arrow trailing every text link, drawn once
and rotated for the other three directions; and a back arrow at a larger scale in
the brand blue. Filled marks declare a `fill-rule` and a `clip-rule` of `evenodd`, so a
punched hole stays a hole rather than being flooded.

The menu button at the narrow band is not an icon but four horizontal rules, the
middle two stacked in the same place so a closed menu reads as three bars. On
open, the outer two fade away and the middle two rotate a quarter turn in
opposite directions to land as a cross, which is what makes it read as one object
turning rather than one picture swapped for another.

The company mark is a small square glyph followed by a gap and a wordmark set
solid, the whole lockup vertically centred in the header. Draw your own to that
envelope.

### The three chromes and the strips

The company chrome is a sticky header on a near-white neutral ground, carrying
the brand lockup, five nav triggers, a circular search control and a sign-in
link. It participates in layout, so the first section needs no compensating
offset, and one named value is the single source of its height: anchor scroll
offsets, sticky sub-navigations and the mega-menu's top edge all read it.

The product chrome replaces it on every product route. A solid blue square sits
flush to the top and left edges of the viewport, breaking the gutter every other
element respects, carrying the company mark drawn in a near-white neutral; beside
it the product's own wordmark as geometry rather than a picture, then that
product's own nav, then a solid call to action, the search control and a sign-in
link. The call to action's label is content: it reads `Get it free` on the work
and knowledge routes, `Try Aide` on the assistant route, and `Contact sales` on
the enterprise route, and that last substitution is the whole positioning of that
route in one control.

The legacy chrome is taller, sits on a near-white neutral ground rather than
white, uses a wider column on a narrower gutter and a raster brand mark. This
build retires it: every route takes the company chrome and the standard column.
The jog in the left edge of the content that a visitor sees moving between the
two is a defect and not a style, and the migration route is the one that keeps it
in the source.

Routes belonging to a family carry a second nav bar directly beneath the header:
a bold family name, then sibling links, then optionally a call to action pinned
right. It becomes sticky beneath the header once the page scrolls past its
natural position, and the current sibling is marked as the current page.

Three strips can appear under the header. A thin announcement strip, full bleed,
on a near-white cool neutral, one line of copy centred with a link and a dismiss
control at the right. A taller notice banner on the same ground for operational
messages, with multi-line copy and an inline link. And a locale banner suggesting
another language, shown only when the visitor's declared language does not match
the path prefix, offered once and never redirecting on its own. Every strip sits
in the document flow rather than fixed, so dismissing one leaves no gap, and each
carries an accessible name and a labelled dismiss control.

The footer is a rounded container on a slightly darker near-white neutral,
carrying a brand glyph and four link columns headed `Company`, `Products`,
`Resources` and `Learn`, with a legal row beneath. Column heads are uppercase and
letter-spaced in the lightest neutral; entries sit in the body colour and move to
the link blue on pointer-over. The `Company` column reads `Company`, `Careers`,
`Events`, `Blogs`, `Investor Relations`, `Northwind Foundation`, `Press kit` and
`Contact us`.

Three pieces of persistent corner furniture live in the lower corners and overlap
content: a bot-score badge, a support chat launcher above it, and on a first
visit the consent dialogue, which stacks above everything else. Nothing the
product itself draws may stack that high.

### The mega-menu

The company header carries five top-level entries, four of which open one wide
panel and one of which is a direct link. There is one panel in the document, not
five: it slides sideways to sit under whichever trigger opened it and fades in
over an eighth of a second or so, fast enough to feel instant and slow enough not
to flicker. It sits on a near-white neutral with a soft shadow, its top edge
flush with the bottom of the header. Those are the panel mechanics, and they are
one element reused rather than five panels.

The Products entry is two panes side by side. The left is an audience switcher
with the rows `Featured`, `Developers`, `Product Managers`, `IT professionals`,
`Business Teams` and `Leadership Teams`; choosing a row swaps the right pane. The
right holds a product grid under the heading `Featured apps`, then a collections
grid under `Northwind Collections`, then a footer strip reading `Powered by`
beside `Aide` and the line
`AI-powered apps, driven by your team's knowledge.`

The product grid and its one-line descriptions, which are content and are read
from the same product collection the hub renders from:

| Product | Description |
|---|---|
| `Flow` | `Flexible project management` |
| `Compendium` | `Knowledge, all in one place` |
| `Flow Service Management` | `Deliver service at high velocity` |
| `Sourcebank` | `Source code and CI/CD` |
| `Aide Dev` | `Agentic AI for developers` |
| `Pipelines` | `Scalable CI/CD automation` |
| `Signal` | `Measure productivity and AI impact` |
| `Flow Product Discovery` | `Capture and prioritize ideas` |
| `Vault` | `Enhanced cloud security` |
| `Cardly` | `Capture and organize your tasks` |
| `Reel` | `Quick, async video updates` |
| `Customer Service Management` | `Customer experiences reimagined` |
| `Scope` | `Enterprise-scale strategic planning` |
| `Roster` | `Knowledge workforce planning` |
| `Chart` | `Enterprise-wide work planning and value` |

`Signal` is the engineering measurement product, `Reel` the async video product,
`Cardly` the lightweight board product, `Roster` the workforce planning product,
`Chart` the portfolio planning product and `Vault` the cloud security product.

The collections grid beneath it:

| Collection | Strapline | Members |
|---|---|---|
| `Teamwork Collection` | `Supercharge teamwork seamlessly` | `Flow`, `Compendium`, `Reel` |
| `Strategy Collection` | `Optimize strategy and outcomes confidently` | `Scope`, `Roster`, `Chart` |
| `Service Collection` | `Deliver service at high-velocity` | `Flow Service Management`, `Customer Service Management`, `Assets` |
| `Software Collection` | `Ship high-quality software fast` | `Aide Dev`, `Signal`, `Pipelines`, `Sourcebank` |
| `Product Collection` | `Build products with confidence` | `Flow Product Discovery`, `Feedback`, `Aide` |

Solutions is four columns: `By Use Case`, `By Team`, `By Size` and `By Industry`,
four entries each. By Use Case reads `Team collaboration`,
`Strategy and planning`, `Service management`, `Software development`. By Team
reads `Software`, `Marketing`, `IT`, `Product`. By Size reads `Enterprise`,
`Small Business`, `Startup`, `Non-profit`. By Industry reads `Retail`,
`Telecommunications`, `Professional Services`, `Government`.

Why Northwind is a flat list of eight entries each with a one-line description,
two of which carry a `New` badge: `System of Work`, `Ecosystem` with the badge,
`Marketplace`, `Customers`, `Public sector`, `Resilience` described as
`Enterprise-grade and highly performant infrastructure`, `Platform` described as
`Our deeply integrated, reliable and secure platform`, and `Trust center`.
Resources is two columns of entries with descriptions plus a support column and a
resources column of plain links, and its `Templates` entry carries the other
`New` badge. Enterprise is a direct link with no panel.

The panel is a genuine disclosure: its triggers are buttons that declare whether
they are expanded and what they control, the audience switcher is a tab pattern
with arrow-key navigation, `Escape` closes the panel from anywhere inside it and
returns focus to its trigger, focus leaving the panel closes it, and the document
behind it does not scroll-lock. The panel is hidden from the accessibility tree
while closed, which is the difference between a keyboard user reaching the page
content immediately and walking through several hundred links on every route.

### Components

**Button.** Four variants. A primary on the brand blue with near-white text,
fully rounded, deepening on pointer-over and deeper again on press. A secondary
that is transparent with body-coloured text, gaining a hairline border and a
faint ground on pointer-over. A subtle link in the brand blue whose trailing
arrow slides a short distance to the right on pointer-over. And a menu variant
that carries a trailing chevron and opens a menu rather than navigating, which is
a menu button declaring that it has a popup and whether it is expanded, operable
by keyboard with `Escape` to close and arrow keys to move within.

**Card.** The workhorse: generously rounded, on a near-white neutral, lifting on
pointer-over as its shadow grows. Three fills on the same geometry: plain for
product cards, a saturated accent ground for resource cards, and a media-topped
variant whose upper region is an image or a generated placeholder.

**Card, resource variant.** A solid accent ground, an illustration above on a
contrasting tint, a category pill reading `VIDEO`, `REPORT` or `EBOOK`, a two- or
three-line title in a near-white neutral, and a call to action with the trailing
arrow. The grounds seen are a lime, a burnt orange, an indigo and a blue.

**Logo wall.** Customer marks rendered as silhouettes and then tinted to whatever
colour the section needs, so one source serves both a light and a dark ground and
nobody maintains two sets. The band is three rows sliding at three different
speeds, masked to fade at both ends rather than clipped, duplicating its content
rather than translating one copy so there is never a gap at the wrap, pausing on
pointer-over and on focus within, and stopping entirely under a reduced-motion
preference.

**Segmented control.** The leading segment rounded on its outer corners, the
trailing one mirrored, nothing rounded between. The selected segment takes the
brand blue with inverse text and the rest are transparent. Implemented as a radio
group so arrow keys move between options and the selection is announced, with a
moving indicator where one is present.

**Tab strip.** Fully rounded pill tabs on a light ground, the active one filled
with a deep accent and inverse text and the rest outlined at the single border
width. A real tab pattern: a tab list, arrow-key navigation, and panels removed
from the accessibility tree when not selected.

**Search input.** A rounded pill on the estate and a circle in the header. The
catalogue's field is a full-width near-white pill on a near-black ground with the
search mark inset from the left.

**Form field.** A near-white ground darkening slightly on pointer-over, a
hairline border in a light cool neutral, barely rounded on legacy surfaces and
fully rounded on the product hero forms. Focus draws the ring in the light, vivid
blue, and the ring springs a little past its size and settles rather than
appearing flat, which is a deliberate and reproducible detail. Helper text sits
one line beneath in the lightest neutral and is present before any error.

**Accordion.** The disclosure opens to its content's natural height without
anyone measuring that height first, the chevron rotates, and the panel stays in
the document when closed only where its content is wanted by in-page search.

**Comparison matrix.** A real table with a scope declared on every header cell. A
sticky header row of plan names, banded section headings on the darker near-white
neutral, feature rows whose label is a disclosure that expands a description row
rather than opening a dialogue, and cells holding either a tick in a filled
circle on the success lime or a short string. The section band seen is
`Project management essentials` and its feature rows are `Unlimited goals`,
`Unlimited work items`, `Unlimited spaces`, `Unlimited forms`,
`Customizable workflows`, `Custom fields`, `Automation` and `Templates`. The
`Automation` row holds strings and not ticks, and they differ in kind between
columns, reading `100 rule runs per month`, `1,700 rule runs per month`,
`1,000 rule runs per user per month` and `Unlimited`, which is why a cell's type
is part of the data rather than a rendering choice.

**Media block.** An image or video, generously rounded, with an optional play
control drawn as a near-white circle with a centred triangle, and a caption
below. Video never autoplays with sound, a poster frame is always present, and
the play control is a button whose accessible name includes the media's title.
The video itself is not loaded until the play control is used.

**Facts rail.** A right-hand column of labelled facts with a hairline between
groups, sticky beneath the header for as long as the prose beside it is taller,
returning to the flow when the prose ends.

**The angled section edge.** Where one colour band meets the next the edge tilts
rather than running straight, lower on one side than the other. The two bands
each carry their own instruction for where to cut and the two are complements, so
always generate both from one angle value; two hand-written shapes drift apart
and leave a pale line across the page.

**The grid backdrop.** A faint square grid of hairlines behind the home hero and
several product heroes, fading out at its edges so it reads as a hint rather than
as a table.

**The fade-to-ground overlay.** A gradient from transparent to the page colour
over the bottom of a media block, so content beneath appears to emerge from the
page rather than to be cut off.

### The routes

**Home.** Its shape is a header, a hero on a near-white neutral, a board
illustration overlapping the hero's lower edge, a resource rail, the journey on a
near-black ground, a closing call to action, and the footer.

The hero carries the grid backdrop, a centred two-line headline reading
`Unleash your teams and their agents` with its final two words in a mid, soft
indigo while the rest takes the heading colour, a narrower two-line subhead
reading `Everyone. Working on the right things. In Flow, teams and AI agents
plan, execute, and deliver outcomes together.`, and a control row of one primary
reading `Get started with Flow` beside a subtle link reading `Contact us`.
Beneath, a wide light panel showing a four-column board labelled `Blocked`,
`In progress`, `Ready for review` and `Done`, each column with a coloured status
chip, a small round product mark and a disclosure chevron, and cards carrying a
title, a reference code, an icon and a stack of overlapping round avatars. One
card is tilted a few degrees out of the grid and one carries a hand-drawn
scribble.

Then the resource rail, a horizontally scrolling row of resource cards, four
visible at the wide band with a fifth clipped, driven by real overflow with
scroll snapping rather than by transform so a trackpad swipe and the arrow keys
both work. Two circular controls sit beneath it, right-aligned; the previous
control is disabled at the left end rather than hidden.

Then the journey, which is the most distinctive and most expensive thing in the
estate. The document reserves a long stretch of scroll distance, pins a
viewport-sized stage inside it, and reads the visitor's scroll through that
stretch as progress through the stage rather than as movement down the page. When
the stage completes the reserved distance collapses and the sections beneath
close up behind it. The scroll system exposes its own custom properties for a raw
position, a smoothed position that lags, a velocity and a direction sign; the
naming is worth adopting even where a build drives the stage another way.

Its stages, in order: a light hero; a light rail with the dark region's top edge
appearing beneath; fully dark, with a portrait centred in a blue disc and
labelled nodes connected by solid and dashed lines, tool marks on the connectors,
a composer panel at the bottom, a progress bar and a skip control; a whiteboard
surface flying in over the graph carrying sticky notes and a named cursor with a
caption at the left; the graph swinging to a new arc under a status banner
reading `Pulling in context...` with three linked context rows beneath; a new
caption at the lower left with the arc inverted; the graph densifying with many
more nodes and two more portraits; the widest state, a centred two-line caption
over a full mesh in four link colours; and light again, with a closing headline
reading `Start your journey with the best teams today`, a subhead reading
`Join millions unleashing the power of teamwork.` and one primary reading
`Get started`. The captions across the stages read
`Connecting knowledge and teams.`, `Keeping everyone in sync.`,
`To accelerate teamwork.` and `So you can make smarter moves, faster`. The skip
control is labelled `Skip`.

The node vocabulary carries meaning and must stay consistent: a rounded rectangle
with an icon and a label for a work concept, named from `Project`, `Sprint`,
`Team`, `Video`, `Goal`, `Idea`, `Release`, `Meeting notes` and `Comment`; a
small rounded square in a solid colour for a tool; a circle filled with a
portrait for a person; and a hexagon for an agent. Links are solid for a direct
relationship and dashed for an inferred one, with arrowheads at intervals along
the line rather than only at the end and small beads riding the line to suggest
flow, in four link colours: a blue, a gray, an amber and a green. The composer is
a rounded panel with a gradient edge running through several hues, carrying a
line of text, a plus control, a settings control, a microphone and a circular
send control; it is the only thing in the journey that looks like a control
rather than a diagram.

Requirements for the journey, and they are what make it hard. It must hold the
pinned frame while the document scrolls through the reserved distance and release
it at both ends without a jump. Progress must be a continuous function of scroll
offset rather than a sequence of triggered playbacks, so scrolling up runs it
backwards. It must reach a correct visual state from any progress value,
including one it was never scrolled through, because a visitor can land in the
middle of it from a restored scroll position and must not watch the first half
replay at speed to catch up. It must not run at all below the narrow band, where
the stages render instead as a plain vertical stack of caption and still, in
order, with no pinning and no reserved distance. It must not break the browser's
own scroll restoration, its find-in-page or its scrolling to an anchor. And it
must not intercept smooth scrolling, emulate momentum or take over the wheel and
touch events, because none of that is needed and all of it breaks the keyboard.
The progress bar is a `progressbar` carrying `aria-valuemin`, `aria-valuemax` and
a live `aria-valuenow`, so it reports its value to assistive technology as the
stage advances, and the skip control is a real button, is reachable by keyboard
the moment the stage pins, is the first focusable element inside it, and on
activation scrolls past the reserved distance and collapses it at once.

Other scroll behaviour is deliberately small. Two soft radial glow blobs sit
behind the product routes' content and brighten as they come into view. They are
one component with a colour input, seen in a pale cyan, a near-white neutral and
a lime. A staggered list entry uses the slide from the side. Everything else on
every other route reveals on entry and then stops; continuous scroll-linked work
is the journey's alone, and entry reveals use an intersection observer rather
than a scroll handler.

At the middle band the hero headline breaks to three lines and the board
illustration shows four columns at reduced card density, and the journey still
runs over a shorter reserved distance. At the narrow band the board is one
column, clipped and tilted, and the journey does not run.

**Product hub.** Its shape is a featured strip, a hub heading, a recommended grid
and further grids. The featured strip sits on a near-white cool neutral carrying
an eyebrow reading `FEATURED APP` then a bullet then the product name, a one-line
display headline `Great outcomes start with Flow`, a two-line body reading
`AI-powered project management that removes the work around work. Keep teams in
sync and on track.`, a primary reading `Try now` and a subtle link reading
`Learn more`. Behind the product still sit an angled magenta panel and an angled
blue panel, both rotated a few degrees and bleeding off the right edge, with a
hand-drawn arrow curving between two parts of the still. Beneath, a centred
heading `Explore Northwind products`, a subhead
`For every team, from startup to enterprise`, and card grids under their own
headings, the first headed `Recommended` with the lede
`Top apps to kickstart your productivity`.

Each product card is a near-white card with a hairline border carrying a product
mark, the product name beside it and a three- or four-line description; the whole
card is the link and its accessible name is the product name plus its
description, never `read more`. The data behind the grids is the product
collection, and the mega-menu reads the same one, so a product added once appears
in both places.

**Work management product.** The template every product route follows. Its shape
is the product header, an announcement strip, a hero, an oversized product still
and alternating feature sections.

The hero is two columns. The left carries a three-line display headline
`Turn plans into agent-ready tasks` breaking at chosen points rather than
wherever the words run out, and a two-line subhead `Then build. Orchestrate work
across your team and agents, with complete context.` The right carries a signup
card that is a real entry point and not a lead-capture form: the label
`Work email`, a fully rounded full-width field with the placeholder
`you@company.com`, a helper line reading
`Use a work email to find teammates and get access to Aide`, a full-width primary
reading `Sign up`, a hairline divider with `Or continue with` centred over it,
and one or more full-width secondary pills each carrying a provider mark and the
provider's name as text, because a mark alone is not enough. The grid backdrop
sits behind the headline and fades out under the card so the card's border reads
cleanly.

The product still below the hero shows the product's board view: a row of view
tabs with icons reading `Timeline`, `Backlog`, `Board`, `List` and `Goals` plus a
plus control, the active tab underlined in the brand blue; a filter control; a
stack of member avatars with an overflow count; then board columns with an
uppercase column label, a count chip, and cards carrying a title, a type icon, a
reference code and an avatar. The panel is deliberately wider than the content
column and is clipped by the viewport at both edges, so the board reads as
continuing past the screen.

The product nav reads `Features`, `Solutions`, `Guides`, `Templates`, `Pricing`,
two of which carry a chevron and open menus. The announcement strip reads
`Join us September 22 for State of AI Delivery: a digital summit on how AI is
reshaping software development. Register now`.

**Pricing.** Its shape is the header and product nav, a headline block, a control
row, the plan table, plan detail rows, the comparison matrix, and the footer.

The headline is a single centred display line
`Transparent pricing for every team.` with a hand-drawn loose double-loop swash
beneath its last two words, drawn as a stroked path and not a rule; it is the
only hand-drawn mark in the product chrome and it is what stops the route reading
as a spreadsheet.

The control row carries a bold `Team size:` label, a numeric field on the darker
near-white neutral with no visible border and the word `users` after it, then a
bold `Bill me:` label and a two-option radio group reading `Monthly` and
`Annually`, the selected one marked with a filled ring in the brand blue, with
the badge after it. The field is numeric and declares itself numeric for a touch
keyboard, has a minimum of one and a sensible maximum, and recomputes on input
after a short settle rather than on blur.

The plan table is four equal columns inside a generously rounded bordered
container with hairline internal rules. The straplines read
`Free forever for 10 users`, `Everything you need to get started`,
`Align multiple teams` and
`Advanced analytics, scale and security for enterprises`, and the calls to action
read `Get it now`, `Start free trial`, `Start free trial` and `Contact sales`.
The Premium column carries a near-black ribbon across its top reading
`RECOMMENDED` in inverse text and its border is drawn darker than its neighbours
for its whole height.

Under each price sits a heading reading `Includes:`,
`Everything from Free, plus:`, `Everything from Standard, plus:` or
`Everything from Premium, plus:`, and a list of four to six inclusions, each with
a right-pointing chevron. Every tier after the first states its inclusions
relative to the tier before it, which is what keeps four columns of features from
becoming a wall. The plan facts read `Up to 10 users`,
`Up to 100,000 users per site`, `99.9% uptime SLA` and `99.95% uptime SLA`.

Then a centred heading `Compare features`, a subtle link
`Learn about features`, and the comparison matrix.

**Knowledge workspace product.** Structurally the work product, and what differs
is small and deliberate. The product nav carries a `More +` entry rather than an
`Enterprise` entry, and the plus is a literal character in the label rather than
an icon. The signup card is a single row with the field and the button fused into
one lozenge rather than stacked. One federated provider is offered rather than
four. The headline reads `The AI workspace that works with you` and the subhead
`Compendium is the one place for all your ideas, docs, knowledge, and human+AI
teammates.` The product still shows a document surface rather than a board: a
document title, a byline row with a reading time and reaction counts, body copy
with an inline highlighted phrase, a floating comment bar over the highlight, a
named collaborator cursor and a right-hand assistant panel with a prompt and a
generated draft.

The collaborator cursor is a coloured triangular pointer with a rounded label tag
beside it carrying a person's name, in a solid accent ground with inverse text.
Its colour comes from a stable hash of the person's identifier, so a given person
is the same colour to everyone looking. In this build the cursor is depicted in
the still and the product does not implement live collaboration.

**Service management product.** The same template with a hero filled to the full
viewport width in a warm amber tint ending on the angled edge, lower on the left
than on the right. What differs is the eyebrow, a two-part lockup reading
`PART OF` then a filled chip carrying a collection name in that collection's own
accent colour, then the word `Collection`; the chip is rendered from a field on
the product record, so reorganising the collections moves the badges, and a
product in more than one collection shows its primary one. The headline reads
`Unlock high-velocity service management` and the subhead `End bad service
management for good. Unite teams on a single AI-powered platform to deliver
service at scale.`, with a subtle link reading `Join demo`. Four federated
providers sit in a two-by-two grid beneath the divider, each a near-white pill
with the provider mark and name. Below the hero, a centred heading
`Service management for all teams`, the lede `Scale experiences across service
teams including IT, HR, facilities, and more.`, and a row of pill category tabs
that switch the content beneath them without navigating.

**AI assistant product.** The one product route with no signup card, and what
differs is the whole hero: fully centred, with a two-line headline at the largest
display size in the estate reading `Meet Aide: AI that knows your business`, one
primary reading `Get Aide` and no secondary. Its product nav reads `Features`,
`Connectors`, `Use cases`, `Guides`, `Licensing`.

The composer still sits beneath, centred: a rounded input box with a thin
multi-hue gradient border about a hairline thick, containing the prompt text
`Create Flow work items, with timing and acceptance criteria per this Feature
Spec` with an inline document reference chip, a plus control at the lower left,
and an automatic-mode toggle and a microphone at the lower right, with a small
rounded role tag with a triangular pointer in a lime ground at the upper right.
Three outlined suggestion chips sit beneath reading `Stay up to date`,
`Analyze feedback` and `Brainstorm ideas`.

The gradient border is a gradient-filled box with an inset solid fill rather than
a border image, so the corner radius stays true at any size, and it degrades to a
single-colour border where a gradient border is unavailable. The same treatment
appears on the journey composer and on the journey's status banner.

**Platform.** Its shape is an anchor nav on a near-white neutral, a stepped
feature list, a tinted explainer and further alternating sections. The anchor nav
reads `Platform` then `the work graph`, `Platform Apps` and
`Enterprise Grade Infrastructure`.

The stepped feature list is two columns. The left is a vertical list of three or
more entries, each a heading and a short paragraph, reading
`Maximize team flow.`, `See the full picture.` and `Get AI value faster.` The
active entry lifts onto a near-white card with a bar down its left edge in the
brand blue and the card shadow, while the inactive entries sit flat on the page
ground with no card. The right column holds a still that changes with the active
entry: two panels offset from one another, the rear one solid in the brand blue,
the front one a light interface panel showing a recommendation list with per-row
source labels and action buttons. It is a tab pattern and not a hover effect: the
active entry is selected by click and by arrow key. Advancing it on scroll is
allowed as an enhancement and must never be the only way to change the selection,
or a keyboard user cannot reach the second item at all.

The tinted explainer is a full-width band on the near-white cool neutral with an
angled upper edge, carrying a centred heading
`An entirely new way to collaborate` and a lede that ends in an ellipsis and
continues into the content below it.

**Enterprise.** Its shape is the header with the word `Enterprise` as the
wordmark and three nav entries reading `Overview`, `Success` and `Resources`; a
notice strip; a hero on a mid blue tint running full bleed with a centred
headline `Accelerate enterprise innovation` and the subhead
`Connect, accelerate, and scale your entire enterprise`; a three-up; a story
panel; and further sections. The header call to action here reads
`Contact sales` rather than `Get it free`, which is the whole positioning of the
route in one control.

The three-up is three columns, each with a small line-drawn mark above its
heading drawn in the body colour rather than in an accent, a medium heading and
three lines of body.

The story panel is two equal halves with no gap between them, sharing one outer
radius: a deep cool neutral panel of text on the left carrying a customer mark, a
heading, a three-line paragraph and a subtle link in inverse colour, and a video
still on the right with the play control centred. The panel is a block with a
heading link and a separate play button; a button is never nested inside a link.

The dated notice names a specific end-of-support date, and that date is a typed
field rather than words in a template, so the strip takes itself down once the
date has passed. A hard-coded date in a template is how a marketing estate ends
up advertising a deadline that went by two years ago.

**Customer index.** Its shape is a masonry grid of cards of unequal height, three
across at the wide band, mixing two card kinds. A quote card carries a cut-out
portrait at the top over composed shapes, then the person's name at a medium
heading, then their job title in uppercase letter-spaced secondary colour, then a
quotation of two to eight lines wrapped in typographic quotation marks. A story
card carries a customer mark at the top left, then the same portrait treatment,
then the person's name below.

Each portrait is a monochrome cut-out laid over two or three flat accent shapes,
a circle, a wedge and a triangle, with occasional hand-drawn line marks over them
such as a flight path, a plus, a small starburst, a bar chart or a smile, and the
shoulders are clipped by the card's top edge so the person leans into the card
rather than posing.

Hover has a trap worth naming: some of the trailing arrows are drawn as a
pseudo-element rather than as part of the link text, so a rule that recolours only
the element leaves the arrow behind at the old colour. Recolour both. Cards move
from their resting placeholder shadow to the lift shadow on the same curve.

The header call to action on this route alone carries a trailing chevron and
opens a menu rather than navigating, so it is a menu button declaring that it has
a popup and whether it is expanded, operable by keyboard with `Escape` to close
and arrow keys to move within.

The index renders from the story collection, and filtering by industry, region
and product is possible from the address even where no filter control is shown,
because that is what makes the index linkable from sales material.

**Customer story.** Its shape is a hero with the customer mark, a headline and a
summary; an outcome strip; a two-column body; and a row of related story cards.

The outcome strip is a band on the darker near-white neutral of three or four
columns, each a single sentence naming a measurable result, with no headings and
no icons. It is the densest piece of persuasion on the route and it works
precisely because the sentences are the same shape as each other.

The prose is three labelled paragraphs, each opening with a bold run-in label
followed by a colon: `Challenge:` holds the situation before in two to four
sentences, `Solution:` what was adopted, and `Impact:` what changed. These are
three fields on the story record rather than one block of text with bold words
typed into it.

The facts rail is the right column, roughly one third of the width, beginning
level with the video: the customer mark at its natural width up to a cap, a large
`About` heading, four to eight lines of description, a hairline, then fact groups
each a small bold label above a value, labelled `Industry`, `Number of users` and
`Location`, then a list of product marks with names under an uppercase
letter-spaced label reading `NORTHWIND CLOUD APPS`.

The video sits at the head of the prose column at a widescreen ratio, generously
rounded, with a near-white play circle centred. It is not loaded until the play
control is used; before that the block is a poster image with a button over it,
which is the difference between a story route costing a fraction of a megabyte
and costing several.

**Template catalogue.** Its shape is a hero with a headline and lede, a product
entry row of three columns each with a product mark, a heading, a paragraph and a
subtle link, the search band, and the results grid.

The search band is the one full-bleed near-black region outside the home journey,
carrying a centred display heading `Search all templates` in a near-white
neutral, the lede
`Discover the workflows your team needs to make any idea possible.` and a
near-white search pill with the search mark inset from the left and the
placeholder `Search templates`. The three product entry ledes read
`Flow templates. Track and manage everything from simple tasks to complex
projects with flexible boards and timelines.`,
`Compendium templates. Skip the blank page. Kickstart any project with ready-made
documents, whiteboards, and diagrams.` and
`Flow Service Management templates. Deliver service faster with customizable
workflows and AI-powered agents.`

The result card is a near-white card with a hairline border whose upper region is
a preview rendered from the template's own structure rather than a stored
picture. Beneath sit the template name, the product it belongs to and a team
category.

**Migration programme.** Its shape is the section nav carrying the family name
`Northwind Uplift` with the entries `Learn`, `Prepare`, `Adopt` and `Resources`
and a right-pinned pill reading `Claim free trial`; a notice strip reading
`Learn the secrets of cloud and AI transformation. Watch our webinar for
real-world insights and strategies. Watch now`; a hero on the darker near-white
neutral with an angled lower edge; a dated notice card; and further sections.

The hero carries an eyebrow, a two-line headline
`Rise to new heights with Northwind Cloud`, a two-line subhead `We're with you
every step of the way, helping you chart your path to cloud, at your pace.`, a
primary reading `Contact us`, and the hero illustration at the right: a dark
massif against a deep cool neutral sky, a blue diagonal field, paler foothills,
orange and near-white ladders laid against the slope, and round portrait avatars
climbing them. Copy that appears over an illustration is real text positioned
over it and never drawn into it, because text inside a picture cannot be read
aloud and cannot be translated.

The dated notice card is generously rounded and inset in the column, carrying an
icon, a bold heading naming the end-of-life date `28 March 2029` for
`Server Edition`, and a paragraph. The date is a typed field and the phase
language about winding down support over the next three years is derived from it
rather than written beside it.

**Solution by team.** Its shape is a hero on a vertical gradient from a mid to a
very pale tint of one accent hue running full bleed, two columns with the
headline `Empowering IT teams to deliver excellent service` and a subhead on the
left and the hero illustration on the right; a section head
`Industry-leading ITSM and ESM solutions` with a two-line lede; a tab strip; and
per-tab panels on near-white.

The hero illustration is a flat line-and-fill drawing made entirely of tints of
that same hue so it reads as texture rather than as a picture: a stylised circuit
board of rounded traces, terminals and pads with a rounded square at its centre
carrying two dots and a curve for a face. Because everything is one hue plus
transparency, giving another team's route its own colour is a one-value change,
and each instance takes its hue from the accent scale.

The tabs read `ITSM`, `IT operations`, `Incident management` and
`Enterprise service management`, the first selected in a deep indigo with inverse
text and the rest outlined. The selected tab is written to the address as a
fragment so a specific tab is linkable, and a fragment on load selects it without
scrolling the page to the strip. The collection behind the route carries a team,
a slug, a hue, a headline, a subhead, an illustration seed and its tabs, each tab
carrying a label, a heading, a body and its links.

**Contact.** The form route and the shortest route in the estate. Its shape is
the header, a section nav carrying the family label `Company` and eight siblings
reading `Customers`, `Careers`, `Investors`, `Events`, `Blog`, `Newsroom`,
`Press kit` and `Contact`; a notice strip carrying an operational message about a
high volume of calls and tickets; a hero on the darker near-white neutral with
the headline `Have a general question for us?` and the subhead `Our team can help
answer questions about your account, privacy and security, or product advice.`;
the form region; and the rail card.

The form is progressive. The first control is a full-width select on the darker
near-white neutral with the filled chevron at its right, under the bold label
`How can we help you?`, and choosing a category reveals the fields that category
needs and only those, appended in the document rather than swapped, with focus
moving to the first new field. Every control has a real label element associated
with it. Validation checks format on blur and completeness on submit, error text
appears beneath its field and is associated with it, and the first errored field
receives focus on a failed submit. The submit control enters a pending state and
is disabled for the duration, and a success replaces the form with a confirmation
reading `Thanks for contacting us!` in the same position rather than navigating
away.

The rail card is a bordered, generously rounded card beside the form carrying a
heading, two lines of body and a secondary pill. It is an unrelated cross-sell:
it sits to the right visually but comes after the form in the document and is
marked as a complementary region, so a keyboard user reaches the form first.

Bot protection on this route is passive and invisible, produces a score rather
than a verdict, and presents a challenge only above a risk threshold and only on
submission, never on arrival. Somebody who cannot pass a challenge is offered
another way to reach a person rather than a closed door: this is a support form
and the people using it are already having a bad day. The badge is not hidden
while scoring continues.

**Not found.** Its shape is the header, a short centred block and the full
footer. The status numeral is set at the largest display size in the estate,
centred, in a deep, muted blue, then the line
`Sorry, the page you're looking for cannot be found`, then
`Visit our homepage, get help, or try searching` with two inline links, then a
bordered field beside a small solid submit reading `Search`.

The rules matter more than the design here. The response status is a real
not-found status and never a success. The route carries the full header and the
full footer, because most people who see it arrived from a search result and this
is their only page. The search field is prefilled with a guess derived from the
requested path. And the route is rendered by the application, never by the
delivery layer.

### The five form surfaces

Five surfaces take input and they answer to one contract. The hero signup on the
product routes creates an account. The federated signup beside it does the same
through an existing identity, and each provider is a button rather than a link
carrying the provider's mark plus its name as text, because the mark alone is not
sufficient; activation opens the provider's own flow in the same tab and the
return lands on a route that knows what the visitor was doing before they left.
The catalogue search queries the template collection. The not-found search
queries the estate. The contact form routes an enquiry to a team.

The signup field is an email field declaring itself as one for autofill and for a
touch keyboard, with spellcheck off. Validation on blur checks the shape only and
never attempts to decide whether an address exists. The helper line reads as
guidance rather than as a warning and is present before any error. The submit
control shows a pending state within a tenth of a second of activation.

### The seeded content

The estate renders from its collections and the collections are seeded. Nine
customer stories, whose customers are `Vanguard Auto` in the automotive industry,
`NBQ` a bank, `Voyagio` in travel, `Peoplera`, `Dataroom`, `Nexon` in networking,
`Ripple` a forum, `Buildly` in construction and `Sprigs` in analytics. The
`Vanguard Auto` story carries the facts `Industry: Automotive.`,
`Number of users: 50,000.` and `Location: Germany.`

Three of the stories are quote cards on the index, and their quotations and
attributions are content that must appear as written:

| Quote | Attribution |
|---|---|
| `"Aide works the way our teams already work. Instead of asking our team to adopt another standalone AI tool, we brought AI into Flow Service Management, chat, and Compendium. That's what turns AI from a test into part of how the business runs."` | `Rowan Blake, VICE PRESIDENT OF IT` |
| `"Our Aide Agents feel like teammates. They don't just return search results. They produce structured insights to support decision making."` | `Florian Meyer, NORTHWIND PLATFORM OWNER` |
| `"Aide reduces noise and helps teams find blind spots earlier. It's our digital twin, helping us surface broader connections, reduce mundane work, and automate intelligently."` | `Dan Whitfield, SYSTEMIC DELIVERY COACH` |

Each testimonial author's name and job title are two separate fields on the story
record, because the index sets them in two different treatments.

The enterprise route's three columns read `Scale with confidence.`, with the body
`Northwind provides the flexibility to scale any transformation. Move faster,
scale new instances, and respond to demands quickly.`; then
`Streamlined automation.` with the body `Get rid of repetitive motions with rules
to run your workflows that meet your team's needs.`; then
`Seamless extensibility.` with the body `Rapidly scale up, down, and across. Our
open ecosystem and interfaces allow continuous integration with other
best-in-class software.` Its story panel reads `Journey to enterprise.` with the
body `This 200-year old bank is still innovating and changing the way their
50,000 employees think and work.` and a link reading
`Check out more customer stories`. Its notice reads `Rise to new heights with
Northwind Cloud. Server Edition support ends on 28 March 2029. Together, we'll
make this transition a success. Learn more and get support`.

The contact route's rail card reads `Investor Info.` with the body
`Read shareholder letters, watch webcasts and more.` and a control reading
`Go to Investor Info`.

The footer's resources column reads `Technical support`,
`Purchasing and licensing`, `Templates`, `Community`, `Knowledge base`,
`Marketplace`, `My account` and `Create support ticket`. Its learn column reads
`Partners`, `Training and certification`, `Documentation`,
`Developer resources`, `Enterprise services` and `See all resources`. Its
products column carries a single `See all products` link. The skip link reads
`Skip to content` and the sign-in link reads `Sign in`.

### Generating every picture

This build ships no binary. Every image in the estate is generated from data the
build already has, and a substitute that needs a designer is not a substitute.
The type is the one exception: name any variable family with a compatible weight
axis and a clear licence, fetched from the app's own delivery layer like any
other font.

Portraits and avatars are drawn per card from a seed derived from the person's
identifier: two or three flat forms from a closed set of a circle, a wedge, a
triangle and a torn rectangle, sized between roughly two fifths and nine tenths
of the card width, positioned and rotated from the seed within a modest angle
either way, in three distinct hues from the accent scale, with no two adjacent
cards sharing a first hue; then a generated silhouette rather than a photograph,
an ellipse for the head, a trapezoid for the shoulders and a neck rectangle in a
neutral, with a soft inner gradient to suggest form, clipped by the card's top
edge; then one hand-drawn overlay from a closed set of a dotted arc for a flight
path, a plus, a four-point starburst, three ascending bars and a smile, stroked
with round caps in the inverse of the ground it sits on and chosen from the
customer's industry rather than from the seed, so a travel customer reliably gets
the flight path; and finally a single tiling noise layer at low alpha over the
whole composition, which is what stops flat shapes reading as clip art. Round
avatars elsewhere use the first two steps only, fully rounded, with the shapes
reduced to one filled disc.

Product stills are not drawn. Render the real components at a reduced scale into
a static region populated from a fixture, with pointer events suppressed and the
whole region hidden from assistive technology, because it is a picture of an
interface and not an interface. The still is then never out of date, it inherits
every token change, its text is real text, and it weighs a fraction of an image.
The tilted card and the hand-drawn scribble in the home board come from the
fixture rather than from code.

Template previews are rendered from each template record's structure field rather
than stored. A board template draws three or four columns from the structure's
column names, each with a count chip and two to four card rectangles at varied
heights. A document template draws a title rule at roughly three fifths width,
then eight paragraph rules at varied widths with two heading rules interspersed
at the structure's heading positions. A whiteboard template draws six to ten
small rounded rectangles in three accent hues at seeded positions with two
connector lines. A form template draws a label rule and a field rectangle
repeated for each field in the structure. A dashboard template draws a
two-by-two grid of panels, each with a title rule and one of a bar, a line or a
donut from a fixed shape set. All are drawn at the card's own size in the token
palette, so several hundred templates cost no assets at all and adding a template
adds none.

Illustrations are parametric compositions in a single hue plus alpha, drawn from
a small closed vocabulary. The ascent scene on the migration route takes one dark
polygon massif, a diagonal field, two paler foothill polygons, three to five
ladder glyphs and four to eight round avatar discs positioned along the ladders,
parameterised by hue, avatar count, ladder angle and seed. The conversation scene
on the contact route takes four to six rounded rectangles at varied sizes with
three text rules each, two circular badge glyphs and two small figure
silhouettes on either side, parameterised by hue, bubble count and seed. The
circuit scene on the solution route takes a rounded square core with two dot eyes
and an arc mouth, plus traces drawn as orthogonal paths with rounded corners
terminating in pads and pins, parameterised by hue, trace density and seed. Each
takes exactly one hue from the accent scale and derives every other value from it
by alpha. The recipes draw no text at all: copy over an illustration is real
text positioned over it.

Customer marks are a generated wordmark: the customer's name set in the brand
sans at the heading weight, letter-spaced to a fixed width, optionally preceded
by a generated glyph built from two overlapping primitives seeded by the name,
rendered as a silhouette so the logo wall's tinting works unchanged. This is the
substitution furthest from the original and it is recorded as such: a real
customer mark is typographically distinctive and a generated one is not.

No video ships. The poster frame is a generated composition at a widescreen crop
with the play control over it, and using the control reveals a caption panel
carrying the transcript rather than a player. The transcript is a required field
on the story record. A build that later adds real video replaces the panel and
keeps the poster, the control, the transcript and the loading rules unchanged.
This substitution most changes the product and it is honest to say so: a page
with a transcript where a video was is a different page.

Textures and the grid: the grid backdrop is a repeating hairline gradient in one
axis with the same declaration rotated for the other. Grain is an inline
turbulence filter at a fine frequency over several octaves with its colour
removed, tiled large enough that the repetition is invisible at card scale, at an
alpha present at a glance and invisible on inspection. The glow blobs are radial
gradients behind a small blur, one component with a colour input.

## Constraints

Single tenant in the sense that there is one Northwind organisation; the
three-level structure of organisation, site and project is modelled, and only one
organisation is seeded. No real-time collaborative editing and no live
collaborator cursor: the knowledge product's still depicts one and the product
does not implement one. No separate search index, no reporting or metrics store,
no customer-installed code and no app sandbox, no billing, no invoices and no
payment instruments, no data residency controls, no export or erasure flows, no
directory provisioning, no federated sign-in beyond the buttons the estate
displays, no distributed tracing, and no native application. No outbound network
call at run time to anything other than the two named backing services. No
locale beyond declaring the document's language and keeping the locale a path
prefix. No comments on work items beyond a requester commenting on their own
request. The catalogue, the story index and the board must stay responsive with
three projects, nine work items, the seeded content collections and a page-view
log of a few thousand rows.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written
  to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server - never a dev
  server.
- The server must keep running after this session ends and must not be a child of
  the shell. An ordinary background job dies with its shell, and the app will not
  be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body or query | Returns |
|---|---|---|
| `POST /api/auth/login` | `email`, `password` | `access_token` carrying the bearer token, plus the signed-in person's `email`, `name` and `role` |
| `GET /api/health` | none | a readiness body |
| `GET /api/projects` | none | a top-level JSON array of the projects the caller may see, each with `key`, `name`, `lead`, `admits_requests` |
| `GET /api/projects/<key>/items` | optional `filter` naming a saved filter | a top-level JSON array of the items the caller may see, each with `item_key`, `summary`, `status`, `status_category`, `assignee`, `rank` |
| `GET /api/projects/<key>/summary` | none | `total`, counted over the caller's visible set alone |
| `GET /api/items/<item_key>` | none | the item, or a denial when the caller may not see it |
| `POST /api/items` | `project`, `summary`, `item_type` | the created item at its project's first status, including its `item_key` |
| `POST /api/items/<item_key>/transition` | `to_status` | the item at its new status, or a rejection naming the reason |
| `PATCH /api/items/<item_key>/rank` | `rank` | the item with its new `rank` |
| `GET /api/items/<item_key>/history` | none | a top-level JSON array, oldest first, each entry with `actor`, `at`, `field`, `from_display`, `to_display`, `automated` |
| `GET /api/filters` | none | a top-level JSON array of the filters the caller may run |
| `POST /api/filters` | `name`, `query_text`, `share_scope` | the saved filter |
| `GET /api/filters/<id>/run` | none | a top-level JSON array of items, resolved as the caller |
| `GET /api/rules` | none | a top-level JSON array of rules, for an `admin` only |
| `GET /api/rules/<id>/executions` | none | a top-level JSON array of executions with `rule_version`, `chain`, `outcome`, `metered_units` |
| `GET /api/plans` | none | a top-level JSON array of tiers with their rate tables |
| `GET /api/templates` | optional `q`, `product`, `team`, `type` | matching templates and a count per facet value |
| `GET /api/stories` | optional `industry`, `region`, `product` | matching stories |
| `GET /api/products` | none | the product collection |
| `GET /api/announcements` | none | the announcements currently relevant |
| `POST /api/signup` | `email` | one of the three signup outcomes, naming which |
| `POST /api/contact` | `category` and that category's fields | an acknowledgement |
| `GET /api/page-views` | none | a top-level JSON array, for an `admin` only |

Bearer auth is required on everything except `/api/auth/login`, health and the public
content endpoints. A list endpoint returns a top-level JSON array. A successful
call returns the named resource or shape. An invalid or unauthorized call is
rejected as a client error, never as a server error and never as a silent
success, with a message naming the reason.

### No mocks

The named services are the fact. An in-memory list of items that the app returns
to itself, a history assembled in the browser from what the screen remembers, a
hardcoded acknowledgement that no mail server ever saw, or a row written nowhere
but a variable, are all contract violations however good the interface looks. A
work item exists when its row exists in `postgres`; a notification exists when
the message exists in `mailpit`, addressed to the person the rule made
responsible. The app's own interface and its own tables can only reflect what
lives in the provider, never substitute for it.

## Definition of done

A visitor can read every public route with no script, price a team of `300` users
and get `683` per user on Standard monthly, narrow the template catalogue by
product and team, and send somebody the resulting address and have it open the
same view. A member can sign in, open their project's board, drag `FIN-2` into
`Ready for review`, and see the move reflected in that item's stored history with
the assignee the bound rule set and one email waiting for that assignee. A member
of another project asking for that board directly is refused, and every count
they are shown is the number of items they can actually see.
