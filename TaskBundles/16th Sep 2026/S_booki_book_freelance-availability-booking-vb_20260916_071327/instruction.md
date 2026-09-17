# Atelier Moreau

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, read the work, open the availability page, hold an open project window,
submit a scoped enquiry against it, receive a confirmation in a real inbox, and
then, as the studio, propose a start date the visitor accepts into a booking,
without hitting an error page. Two people accepting a start date against the
last remaining capacity of one window must not both succeed: exactly one booking
exists afterwards, the window's committed days never pass its capacity, and the
confirmation mail must be a real message in `mailpit`, not a success the app
reports to itself.

## Overview

Atelier Moreau is the portfolio and enquiry desk of a freelance creative
developer, and the booking layer behind it. The public site establishes craft,
shows nine projects, states availability, and converts a visitor into a scoped
enquiry. The booking layer turns that enquiry into an agreed start date: an open
window, a brief written against it, a proposal, and a confirmed booking.

Three audiences arrive: a founder with a product to build, who wants proof of
craft and whether he is free; a product lead at a studio, who wants the work
and what he actually does; and a recruiter comparing people, who wants the
services and the experience. A returning client is the fourth, and the only one
who signs in.

Three kinds of person use it. A **visitor** with no account reads the work,
checks availability, holds a window while writing and sends a brief; they never
sign up, and that is deliberate. A **client** is somebody who sent an enquiry
and took an account afterwards so they can follow it, reply and accept a start
date. The **studio** is the site's owner: one account, who reads the pipeline,
replies, proposes, declines, and opens or closes windows.

The information architecture is small on purpose: three public documents, a
handful of extension routes behind them, and no page that exists only to hold a
link. The public half is three scrolling documents on alternating grounds, with fixed
chrome carrying the name lockup, the availability pill, a sound control and four
navigation targets. It is composed rather than laid out, because what is being
sold is taste. The operational half behind the sign-in is the opposite: quiet,
dense and built for repeated work.

It deliberately is not several things. It takes no money: a booking is an agreed
start date, recorded, and every commercial act happens elsewhere. There is no
file upload anywhere. There is no password policy, no staff hierarchy, no
newsletter, no third-party analytics and no translation. The full scope-out list
is in `## Constraints` and is part of the specification.

The genuinely hard part is capacity. A hold reserves the right to be considered
and commits nothing; capacity is committed only when a proposal is accepted.
That ordering is what stops one enquiry that was never going to convert from
blocking a month of the calendar, and it is what makes two simultaneous
acceptances against the last place a real race that exactly one of them must
win.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `client` | Read every public route. Hold an open window. Submit an enquiry. Read, reply on, accept a proposal on and withdraw their own enquiries. Take an account and read their own enquiries and bookings. | **Cannot read, reply on, accept or withdraw an enquiry belonging to somebody else.** **Cannot propose a start date, decline an enquiry, create, move or close a window, edit a project, or read the pipeline or the export.** |
| `studio` | Everything a client can do, plus: read any enquiry, reply on any enquiry, propose a start date, decline an enquiry, create, move and close windows, edit a project, read the pipeline and take the export. | **Cannot accept a proposal on behalf of a client, and cannot withdraw a client's enquiry.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
control in the UI is not authorization: a direct API call from a `client`
session to any `studio`-only endpoint must be rejected by the server (an
unauthorized request is denied, not served), leaving the protected state
unchanged.

**Authentication** is by email and password on the account, and by a link for
anybody who would rather not have one. The signed-in behaviour of each route is
in `## User flow`; the capability matrix below is what the server enforces.

| Capability | anonymous | `client` | `studio` |
|---|---|---|---|
| view every public route | yes | yes | yes |
| view open windows | yes | yes | yes |
| submit an enquiry | yes | yes | yes |
| hold a window | yes | yes | yes |
| view an enquiry | with the token | own | any |
| reply on an enquiry | with the token | own | any |
| accept a proposal | with the token | own | no |
| withdraw an enquiry | with the token | own | no |
| propose a start date | no | no | yes |
| decline an enquiry | no | no | yes |
| create, move or close a window | no | no | yes |
| edit a project | no | no | yes |
| read the pipeline or the export | no | no | yes |

An anonymous visitor is not a role, and is deliberately allowed more than a
commerce site would allow. With no account at all a visitor may read everything
public, hold an open window for `72 hours`, and submit an enquiry. An enquiry
confirmation carries a token in its address which grants read and reply on that
one enquiry, and the right to accept or withdraw it, for `90 days` without any
session. The whole point is to make getting in touch cheap; putting a
registration in front of the contact form is the most expensive mistake this
product could make.

The enquiry token is never a session and never carries a role. It opens one
enquiry and nothing else.

**The single-operator risk is named rather than designed around.** One `studio`
account is one point of failure, so three things are required: the account
carries a recovery address distinct from its sign-in address, the enquiry
notification is addressed to a second address that is not the studio account's
so a locked-out operator still sees work arriving, and the whole pipeline is
exportable in one action so the business is never trapped inside the site.

Signup is open. Anyone can create an account, and every signup creates a
`client`. There is exactly one `studio` account and it exists only by seed.

Seeded accounts, both with the password `deku-demo-pw-2026`:

| Email | Display name | Organisation | Role |
|---|---|---|---|
| `studio@example.com` | Elian Moreau | Atelier Moreau | `studio` |
| `client@example.com` | Alex Renard | Northgate | `client` |

## Core features

### Auth

Email and password accounts implemented by the app itself. Passwords are stored
hashed and no endpoint ever returns a hash. A successful login returns a bearer
token; the client sends it on every request except signup, login, health and the
public reads. A token expires after `24 hours`.

1. Signing up with an email that already has an account is rejected as invalid,
   the form names the field at fault, and no second account row is written.
2. A signup always produces a `client`. A role named in the request body is
   ignored, never honoured.
3. A request carrying no token, an expired token or a tampered token is rejected
   as unauthorized on every route except signup, login, health and the public
   reads.
4. `POST /api/auth/link` requests a sign-in link for an address and is always
   accepted, whether or not that address has an enquiry. The response says
   `If that address has an enquiry with us, a sign-in link is on its way.`
   whichever it is, so the endpoint cannot be used to discover who has written
   in.

### The public documents

Three scrolling routes on alternating grounds, each with the fixed chrome.

5. `/` carries the hero, the about section and the selected-work preview in that
   order. `/work` carries the nine-project index. `/contact` carries the enquiry
   form. `/availability` carries the current state and the open windows.
6. `/work/` redirects permanently to `/work`. One canonical form for one
   document.
7. `Home` and `About` are anchors into the home document and update the
   fragment; `Work` and `Contact` are routes and update the path. An anchor
   reached on a cold load scrolls to its own position rather than landing at the
   top.
8. The chrome carries the name lockup, the availability pill, a sound control
   reading `Sound | OFF` or `Sound | ON`, and the four navigation targets. It is
   present on every public route.
9. The sound control's visible string states the current state and its
   accessible name states the action, so a control reading `Sound | OFF` is
   named `Turn sound on`. No state, confirmation or error is signalled by sound
   alone.

### Projects and services

10. Nine projects are seeded, each with a title, a discipline, a year, a slug
    and a position, and they are drawn from one record set in two presentations:
    as rules-and-rows on the home page, and as the staggered pill index on
    `/work`. Changing a project changes both.
11. The work index states its own count, and with nine published projects it
    reads `(09)`.
12. `/work/{slug}` resolves to one project. A slug with no project renders the
    product's own not-found surface and answers not-found.
13. Three services are seeded, each a title and a line.

### Availability, derived and never typed

14. The availability mode is **computed from the windows on every read** and is
    never stored as a typed string. No endpoint accepts a mode. The four modes
    and their conditions:

    | Condition | Mode | Pill reads |
    |---|---|---|
    | a window is `open` and starts within `14 days` | `open_now` | `available now for work` |
    | a window is `open` and starts later | `open_from` | `available from` and the month |
    | every window is `booked` or `closed`, and one is `booked` | `booked_until` | `booked until` and the month |
    | no window exists | `not_taking` | `not taking new work` |

15. The pill and the availability page read the same record, so they can never
    disagree. The pill is never absent.
16. The availability state is always carried in the pill's words. It is never
    signalled by the dot's colour alone.
17. The studio may set a free `note`, which is shown on the availability page
    and never in the pill. The pill's words come from the model and cannot be
    typed over.
18. `/availability` lists the next open windows, each with a start date, a
    length in weeks and a capacity in days per week, then what a window means,
    then a control reading `Start an enquiry` against a chosen window.

### Windows and holds

19. A window is a start date, a length in `weeks`, a `capacity_days` between `1`
    and `5`, and a `committed_days` that starts at `0`. Its state is one of
    `open`, `held`, `booked` or `closed`.
20. Pressing `Start an enquiry` against an open window creates a hold on it that
    expires after `72 hours` and opens the enquiry form with that window named
    at its head.
21. **A hold commits no capacity.** It does not change `committed_days` and it
    does not reduce what another visitor may be offered.
22. At most `3` live holds may exist on one window. A fourth attempt is refused
    with `This window is nearly full. Send an enquiry without holding it.` and
    the enquiry form still opens, without a window.
23. A hold on a window that is not `open`, or on a window with no remaining
    capacity, is refused with the reason stated under the control.
24. A hold is released immediately when its enquiry is withdrawn, and when the
    studio closes the window it sits on. Releasing a hold by hand is immediate
    and stays undoable for ten seconds, with no confirmation asked for first.

### The enquiry

The form carries six numbered fields, each a label over an underlined input.

| No. | Label | Required | Constraint | Error copy |
|---|---|---|---|---|
| `01.` | `My Name` | yes | 1 to 80 characters | `We need something to call you.` |
| `02.` | `My Email` | yes | a valid address | `We need an address to reply to.` |
| `03.` | `I work at` | no | up to 120 characters | `That is longer than we can store.` |
| `04.` | `I am looking for` | yes | 3 to 200 characters | `A few words about what you need.` |
| `05.` | `My budget is` | yes | one of the four bands | `Choose a range, even a rough one.` |
| `06.` | `My message` | yes | 20 to 4000 characters | `Tell us a little more, at least twenty characters.` |

25. The budget bands are a select carrying exactly these four options in this
    descending order: `USD $20001 and up`, `USD $10001-$20000`,
    `USD $5001-$10000`, `USD $2000-$5000`. The largest band is the first option
    a visitor sees, and the currency is named on every one.
26. There is no band below the lowest. Under the select sits the line
    `Smaller than that? Say so in your message and we will point you somewhere good.`
    The band stays required and the floor stays where it is.
27. The submit control reads `Send it now :)`.
28. Validation runs on blur, never on keystroke. A field that has failed
    re-validates on keystroke until it passes. The form re-validates on submit.
    A rejected field names itself in words, writes nothing, and leaves every
    other answer as the visitor typed it.
29. A privacy link sits beside the submit control, not only in the footer,
    because the form is where the name, the address and the employer are
    collected.
30. Submitting creates an enquiry in state `new`, linked to the held window,
    with an opaque `token` valid for `90 days`. The visitor lands on
    `/enquiry/{id}` carrying that token. A confirmation reaches the sender and a
    notification reaches the studio.
31. If the hold expired while the visitor was writing, the enquiry is still
    accepted, without a window, and says so. The form keeps every answer and a
    band reads `Your hold on that window ran out. You can still send this.`
32. The enquiry form is rate limited per address. A refusal names how long to
    wait, in words. A submission carrying a spam signal is held for the studio
    to review rather than dropped silently: a false positive that eats a real
    enquiry is worse than one the studio has to glance at, because the sender is
    never told and never writes again.

### Enquiry to booking

This is the workflow the product exists for.

33. The studio reads the pipeline and opens an enquiry. The state moves from
    `new` to `reading`, and the client's own enquiry page shows it.
34. Either side may reply. A reply creates a message and mails the other side.
    A reply changes no state.
35. The studio proposes a start date, a length in weeks, a capacity in days per
    week and a free note. The proposal's dates must fall inside the enquiry's
    window and its days per week may not exceed what the window has left. The
    enquiry becomes `proposed`, the hold is extended to the proposal's expiry,
    and the client is mailed.
36. At most one proposal per enquiry is `live` at a time. Proposing again
    supersedes the previous one.
37. The client, or the token holder, accepts. A booking exists, the enquiry
    becomes `booked`, the window's `committed_days` rises by the proposal's days
    per week, and if the window is now full its state becomes `booked`.
38. **Capacity is committed at acceptance, never at hold.** Two acceptances
    against the last remaining capacity of one window must not both succeed:
    exactly one booking is written, `committed_days` never passes
    `capacity_days`, and no partial booking survives. The refused acceptance
    reads `That window filled up. Here is what is open.` and carries the open
    windows with it.
39. Accepting a proposal whose expiry has passed is refused with
    `That proposal has expired. Ask for a new one.` and a control to ask again.
40. The client, or the token holder, may withdraw. The enquiry becomes
    `withdrawn`, the hold is released immediately, and nothing is deleted.
41. The studio may decline. The enquiry becomes `declined` and the client is
    always mailed. A silent decline is not available.
42. An enquiry with no reply for `30 days` becomes `lapsed` and its hold is
    released. Nobody is mailed about it.
43. An enquiry is never deleted. `withdrawn`, `declined` and `lapsed` are
    states, because who asked and what happened is the studio's own history.
44. After a booking the availability mode re-derives itself on the next read. If
    no window remains open the pill has moved to its booked form. Nobody typed
    it.

### The pipeline

45. `/studio/pipeline` shows enquiries laid out as a calendar grid by window and
    by state, newest first within each state.
46. It filters by state and by budget band, and the current filter is carried in
    the address so a filtered view can be shared and returned to.
47. `GET /api/export` returns every enquiry, message, proposal, booking and
    window in one response, to the studio alone, in one action.

### Transactional mail

The app sends over real SMTP at `SMTP_HOST` and `SMTP_PORT`, reading
`SMTP_USER` and `SMTP_PASS` from the environment. Every message is plain text,
carries one primary link, and states at its foot which address it went to and
why.

48. Ten messages, each with its exact subject, each addressed to exactly the
    recipient named, with no cc and no bcc:

    | Trigger | To | Subject begins |
    |---|---|---|
    | an enquiry is submitted | the sender | `We have your enquiry` |
    | an enquiry is submitted | the studio | `New enquiry` |
    | the studio replies | the sender | `A reply to your enquiry` |
    | the client replies | the studio | `A reply from` |
    | a proposal is sent | the client | `A start date for your project` |
    | a proposal is accepted | the client | `Booked` |
    | a proposal is accepted | the studio | `Booked` |
    | a proposal expires within `48 hours` | the client, once | `Your start date offer expires soon` |
    | an enquiry is declined | the client | `About your enquiry` |
    | a sign-in link is requested | that address | `Your sign-in link` |

    A worked example: an enquiry submitted by `client@example.com` produces a
    message to `client@example.com` whose subject begins `We have your enquiry`
    followed by a space and the enquiry id.

49. The confirmation to the sender carries their own six answers back to them,
    as submitted. It is their copy of what they asked for.
50. Mail is sent **after** the state change commits. A mail failure never fails
    the action: the enquiry is submitted, the page says so, and the failure is
    flagged on the studio's pipeline with a control to send it again.
51. **The non-transition rule.** No mail is sent when an enquiry lapses, when a
    hold expires, when the studio reads an enquiry, or on creating or closing a
    window, where mail is not applicable at all. There is no follow-up chasing an unanswered enquiry, no
    newsletter, and no marketing of any kind derived from what an enquiry
    disclosed.

### Notifications in the product

52. Three surfaces and no others. A **band** under the chrome, full width,
    carrying something true right now and staying until the condition clears. An
    **inline confirmation** under the control that caused it, for about two
    seconds. An **action band** above the control that failed, staying until it
    is dismissed or the action is retried.
53. One band at a time, the highest priority winning, in this order: offline;
    a hold expired while writing; a proposal awaiting the visitor; a proposal
    expiring within `48 hours`; the studio has replied.

### The public edge

54. `/legal/privacy` states what the enquiry form stores, how long an enquiry is
    kept, and how long a booking is kept. It is linked from the footer of every
    public route and from beside the submit control.
55. `/legal/terms` states the terms of use and is linked from the footer of
    every public route.
56. A first-time visitor is asked once about non-essential cookies. The answer
    survives a reload. A page view is recorded only when the answer was yes,
    and the record carries the route and the time and nothing about the person.
57. Every public route declares its own social preview title plus its own
    preview image, no two routes declare the same pair, and every declared
    preview image resolves.

### Finding things, and what stays live

58. The work index needs no search: nine projects are a list, not a corpus. The
    pipeline does, and its search behaviour is one field matching the
    enquiry's name, organisation and subject line, applied on top of the state
    and band filters rather than replacing them.
59. The pipeline sorts newest first by default and can sort by budget band,
    largest band first, which is the order the bands are offered in.
60. **What is optimistic, and what is not.** A reply appears in the thread the
    moment it is sent, before the server confirms it, and rolls back with a
    message above the control if the send fails. Nothing touching capacity is
    ever optimistic: a hold, a proposal and an acceptance each wait for the
    server, because the hold is a shared resource and an optimistic rollback of
    a booking is a booking somebody has already been told about.
61. **Presence is a fact about the enquiry, not about the person.** An enquiry
    open in the studio's pipeline shows on the client's own page that it is
    being read. No cursor position, no typing indicator and no last-seen time
    is shown to anybody.
62. A change one side makes reaches the other side's already-open enquiry page
    without that person reloading, within a few seconds.

### The clock, and how things are written

63. The footer renders the studio's local time from the stored timezone as a
    twelve-hour clock with its offset named, so `01:59 PM GMT+2` is the shape.
    The internationalisation posture is stated rather than assumed: the product
    ships in one language and is not translated.
64. Formatting is consistent everywhere it appears. A date is written as a day,
    a month name and a year. A window's length is written in weeks and its
    capacity in days per week. A budget band is written exactly as its option
    reads, currency included. A timestamp shown to a client is rendered in that
    client's own timezone, and a timestamp shown to the studio in the studio's.

### Instrumentation

65. **Instrumentation is local and small.** Seven events are recorded and no
    others, each with the properties named beside it and nothing more: an
    availability view, with the count of open windows; a hold created, with the
    window and the days until it starts; an enquiry submitted, with the budget
    band, whether it had a window and the length of the message; an enquiry
    abandoned, when a draft is thirty days old and unsent, with the furthest
    field reached; a proposal sent, with the days since the enquiry; a proposal
    accepted, with the days since the proposal; and the moving ground rendering
    degraded, with the stage it fell back to. No event ever carries a name, an
    address, an employer or a message body.
66. Those four numbers are the ones that matter to the studio, so the studio
    can read them: how many arrived, how many started an enquiry, how many
    finished it, and how many became a booking.
67. Nothing is recorded at all until the cookie answer is yes, and revoking the
    answer stops the recording from the next page onward.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the home document: hero, about, selected work | public |
| `/work` | the nine-project index | public |
| `/work/{slug}` | one project | public |
| `/contact` | the six-field enquiry form | public |
| `/availability` | the current state and the open windows | public |
| `/legal/privacy` | what the enquiry form stores | public |
| `/legal/terms` | terms of use | public |
| `/signin` | request a sign-in link, or sign in | public |
| `/enquiry/{id}` | one enquiry and its thread | token, owner, or studio |
| `/account` | the client's own enquiries and bookings | client |
| `/studio` | the studio's home | studio |
| `/studio/pipeline` | the calendar grid of enquiries | studio |

**Entry and redirects.** An unauthenticated request for `/account`, `/studio` or
`/studio/pipeline` lands on `/signin` with the destination remembered, and
signing in continues to it; a remembered destination is honoured only when it is
a path on this origin beginning with a single slash. A `client` reaching a
studio route gets the denied surface, not a redirect. A `studio` session
reaching `/account` is sent to `/studio`. `/enquiry/{id}` opens for its token,
its owner and the studio, and for anybody else renders the denied surface, which
is byte-identical whether the enquiry exists or not. An expired token renders a
distinct surface saying the link has expired, with a control to ask for another.
Signing out returns to `/` and the previous private route is not reachable by
going back.

**Journeys.**

1. **Read the work.** Open `/`. The name lockup slides in from the left and the
   availability pill arrives from the upper left. Scroll: the pale about sheet
   slides up over the dark hero, and the statement's words rise one at a time
   over their own faint twins. Reach selected work, then open `/work` and see
   the nine projects as staggered pills with the count reading `(09)`.
2. **Check availability.** Open `/availability`. The current state is at display
   size; under it the open windows, each with a start date, a length in weeks
   and a capacity in days per week; under that what a window means; under that
   `Start an enquiry`.
3. **Hold and enquire.** Press `Start an enquiry` against the first open window.
   The form opens with that window named at its head and a `72 hour` hold
   created. Fill the six numbered fields, choose `USD $10001-$20000`, and press
   `Send it now :)`. The enquiry exists in `new` against the window, a message
   whose subject begins `We have your enquiry` arrives for the sender carrying
   their six answers back, a message whose subject begins `New enquiry` reaches
   `studio@example.com`, and the visitor lands on `/enquiry/{id}`.
4. **The studio reads and proposes.** Sign in as `studio@example.com` with
   `deku-demo-pw-2026`, open `/studio/pipeline`, and find the enquiry in the
   `new` column with its budget band and window. Open it: the state becomes
   `reading`. Reply with a question; the client is mailed. The client replies
   and the state does not change. Propose a start date inside the window, a
   length and a capacity; the slide-over shows the window's remaining capacity
   live above the fields. The enquiry becomes `proposed` and the client is
   mailed `A start date for your project`.
5. **Accept.** As the client, open the enquiry and accept. A booking exists, the
   enquiry becomes `booked`, the window's committed days rise, and both parties
   receive a message whose subject begins `Booked`.
6. **The pill re-derives.** Reload any public route. If no window remains open,
   the pill now reads `booked until` and the month. Nobody edited it.
7. **Two acceptances, one place left.** Two live proposals sit against the last
   remaining capacity of one window and both are accepted at once. Exactly one
   booking exists. The other acceptance is refused reading
   `That window filled up. Here is what is open.` with the open windows
   attached, and the window's committed days never pass its capacity.
8. **The hold lapses.** A visitor holds a window and writes slowly until the
   hold expires. A band reads `Your hold on that window ran out. You can still
   send this.` The form keeps every answer, the submit still works, and the
   enquiry is accepted without a window and says so.

**States.** While a surface is loading it shows its own quiet placeholder in
place rather than collapsing and jumping when the content arrives, and a
control that is working shows it on itself rather than blocking the page. A
client with no enquiries reads
`An enquiry appears here once you send one.` An empty pipeline reads
`The pipeline is clear.` A work index with
nothing published reads `No projects listed.` A failed read reads
`That did not load.` with a control reading `Try again`. A denied surface reads
`That is not yours to open.` and a missing one reads `We cannot find that.` A
visitor with no connection reads `You are offline. Your draft is safe.` and the
enquiry draft survives a reload in the same browser. While something is sending,
the submit control's own outline draws itself around and holds; there is no
spinner anywhere in this product. No route shows a blank screen or an unhandled
error.

## UI/UX notes

The north star: somebody arriving should understand in the first screen that
this is one person's craft rather than an agency's brochure, and should be able
to find out whether he is free without scrolling, reading or asking. The
register is editorial and unhurried, with a point of view: the subject is the
work, and the page is composed rather than laid out. This is a register where
atmosphere is earned, because what is being sold is taste. The studio surfaces
behind the sign-in are the opposite register, quiet and operational, using the
same tokens with none of the theatre.

Because the site must convey value, it takes space around the subject, one thing
dominant per view, and the largest type reserved for the two things that carry
the argument, the name and the statement. Because it must reassure at the moment
of enquiry, when a person is about to disclose their budget and their employer,
that surface is still, plainly worded, carries no decoration, and puts the
privacy link beside the send control. Because the pipeline is repeated
operational work, that surface goes dense and stable and spends none of the home
page's theatre. Outline over fill on the display face: a competing portfolio
would set its display type solid for impact, and this one strokes it and lets
the ground show through. One curve over a motion vocabulary, which is why the
page reads as one object rather than a collection of effects. Drawn over faded on
every stroked mark. Derived over typed on availability, because a badge somebody
has to remember to update is a badge that lies.

**Colour.** Two grounds alternate down the document and the alternation is the
structure: a near-black neutral for the hero, the contact surface and the
footer, and a pale cool near-white neutral, lavender in cast, for the about and
work surfaces. One accent, a deep soft indigo, which is the ink on the pale
ground and the fill of every solid control; two brighter indigos appear only as
the stops of the hero's halo and nowhere else. The supporting roles are all
neutral: a near-white for text on the dark ground and for solid pills on the
pale one, the palest cool near-white for cards and panels, a light cool neutral
for secondary text and for placeholders, a deeper near-black for the footer
ground, and a near-black panel for form fields on dark.

One signal colour, a mid soft green, meaning exactly one thing: he is available.
A build that uses the green for anything else has broken the system. The single
permitted second use is the focus rule on the dark ground, allowed only because
focus and availability never land on the same element. Two exclusivity rules
carry the rest: the green never sits on the pale ground, where it has neither
the contrast nor a meaning; and the availability state is always in the pill's
words, never in the dot's colour alone, so somebody who cannot tell the green
from the grey reads the sentence and gets the same answer. A dependency ships an
alphabetical lookup table of standard colour names, among them a mid vivid red
and a mid vivid amber; none of them renders here and none may. There is no red
anywhere, which means an error cannot be red: an error is the product's own
purple selection tint plus the words saying what is wrong. The exact shades are
yours, so long as the two grounds stay distinguishable at a glance, the accent
is the only non-neutral ink, and the green appears nowhere but availability and
focus.

**Type.** The two real typefaces are the product's voice, and their letterforms
are the one thing a substitution cannot recover. Three faces: a working face
for all body and interface text, its bold
for headings and emphasis, and a condensed display face used only as an outline.
Each is named with a metrics-matched fallback so the page does not reflow when
the faces arrive, and no font binary ships. The display face is stroked, not
filled: on the hero eyebrow and on both section titles the glyphs are drawn with
a stroke and a transparent fill. The one place it is filled is the name itself,
directly under an outlined eyebrow in the same face, and that pairing is the
hero's whole typographic idea. The scale is one ratio applied repeatedly to one
root size, which is why several steps land on fractions; reproducing the
derivation reproduces them. Two rules govern it and nothing sits between them:
display type is set solid, its line box equal to its size, and body type is set
loose at half again. The one deliberate exception is the about statement, which
is display size set loose, because it is a paragraph rather than a heading.

**Shape and depth.** Corners come in two families and no others: a generous
rounding for anything that is a surface, a smaller one for anything sitting on a
surface, and a full pill radius for anything that is a control. Some panels are
rounded on two corners only, and that asymmetry is what makes the sections read
as sheets sliding over one another rather than as stacked blocks; the route
label carries a single rounded corner where it meets the page edge. Depth is
shallow and ordered: a render layer behind the document, the document, sticky
and pinned things above it, the chrome above those, and the cursor and the modal
at the top. The chrome is one layer whose children are ordered in the document,
never three layers pretending to be one.

**Motion.** One signature curve carries nearly everything: it holds still,
accelerates hard, and stops hard, symmetric at both ends. One duration, around
half a second, on almost every transform; two shorter ones for control states,
one quick and one nearly instant on press; and one long fade, roughly seven
times slower than anything else, on the hero's invitation to scroll, which
arrives only after everything else has settled. Do not put a transition on
everything: name the properties that move. Two effects define the product and
neither may be substituted. The first is the shadow reveal: the about statement
is split per word, every word has a faint twin behind it, and the word itself
rises over its twin as the document advances, one word at a time rather than as
a single fade, while the statement stays selectable and is announced as one
string. The second is stroke drawing: every stroked mark draws itself on rather
than appearing, and a build that fades them in has the same content and a
different product. The named moments are the chrome sliding in from the left on
load, the pill arriving from the upper left, the route label rising on a route
change, the per-word reveal under scroll, the stroke draw on enter or
activation, the burger crossing, the quick control state, the micro press, the
colour shift at a section change, the slow prompt fade, the card stack
scrubbing, the header blur scrubbing, and the window settling when a booking
window is chosen. Under a reduced-motion preference every one of them resolves
to its rest state: drawn marks are drawn but not animated, the reveal is present
at full opacity, the render layer holds one frame, the header blur is applied at
rest, the card stack is static, the prompt fades quickly, and the document
scrolls natively. Nothing is removed; movement stops. The submit's pending state
is the stroke drawing around its own outline, and there is no spinner anywhere.

**Iconography.** Every mark in the product is drawn geometry rather than an
image file, single colour, and recoloured with the surface it sits on. The
site's own marks are the monogram, the burger, the arrow, the sixteen-point
asterisk and the text arc; each is a stroked path and each draws itself on. Two
groups of marks in the reference are not the site's own, the award badges and
the tool band, and both are replaced with neutral drawn marks.

**Density and layout.** The public site is spacious; the pipeline is compact,
with a full column of enquiries and their windows on one screen, rows sitting
tight, and controls holding the same position between sessions. Four
breakpoints and no others: a small-phone correction, the dominant mobile switch,
a mid switch and a wide-desktop switch. A reference tuned by hand with twenty
queries, five of them within eighty pixels of each other, is not a system: those
are individual fixes, and a layout needing one specific width is a layout with a
bug just past it. Across those breakpoints the navigation folds to a burger
below the mid switch, the lockup drops to the monogram on the smallest, the hero
name and the about statement each step down two sizes, the work index loses its
horizontal stagger and stacks in one left-aligned column in date order, the
project view becomes a panel rather than a modal, the fixed rail is hidden below
the mid switch, the contact form goes to one column, and the tool band shows
fewer marks. At a narrow viewport nothing overflows sideways and every
navigation target stays reachable. That matrix is the whole responsive
specification; a defect worth fixing in the reference was twenty hand-tuned
queries, and collapsing them to four is the fix.

Two motion details complete the vocabulary. The scroll prompt carries a single
weighted bounce, a keyframe whose ease differs on the way out and on the way
back, and it is the only bounce in the product. A handful of runtime animations
run once on load with a long tail rather than being scrubbed against scroll,
and they are the entrance of the chrome, the pill and the flag bar. Sound is
off by default, and the default is stated in the control rather than discovered.

**Touch.** Below the mid switch the custom cursor is not rendered at all and the
label it carried becomes a visible control on each row. The grayscale-to-colour
treatment on media is tied to entering the frame rather than to hover, because a
hover effect is invisible on a phone. Every control is a comfortably sized
fingertip target, achieved with padding. The tool band scrolls on touch and does
not auto-scroll while it is being touched.

**Accessibility floors.** Body text and its background meet WCAG AA contrast.
The reference's placeholder colour does not, and it carries meaning here because
the placeholders are worked examples, so it is replaced with the secondary text
colour, which is already in the palette and passes. Focus is visible on every
interactive element, green on the dark ground and indigo on the pale one, and is
never removed; focus is not hover, and the ring and a hover treatment must be
able to happen at once. The two split treatments, the per-word statement and the
per-character work headline, are hidden from assistive technology as split
elements with the original string present once in reading order, because without
that rule a screen reader reads a sixty-nine-word statement twice, once for the
shadow twins. Every icon-only control carries a name, and keyboard navigation
reaches every control on every route.

**What this must not look like.** Not a dashboard with a portfolio pasted on top;
the public routes are composed documents and the operational density belongs
behind the sign-in. Not a page dominated by one hue family with no second signal.
Not a build whose stroked marks fade in, which is the one substitution that keeps
every measurement and loses the product. Not a page that degrades into nothing
when the moving ground cannot run: the graceful degradation is a still ground in
the same colours, never an empty rectangle, and the hero reads correctly without
it. Not an error state in red. And not a
floating message arriving from a corner: the chrome is already deep and the
document already carries many scrubbed effects, so a fourth thing flying in would
read as part of the choreography rather than as a message.

## Technical requirements

The browser receives an application shell on first paint and every later screen
is assembled in the browser from JSON served by the app's own API. This is the
coherent model for the product: the document is scroll-driven with many scrubbed
effects and a fixed chrome that must survive a route change, and a full page load
between routes would restart every one of them.

- **Frontend:** Svelte with Vite, built to a production bundle.
- **Backend:** Hono on Node, serving the HTTP API on the same origin under the
  `/api` prefix.
- **Database:** PostgreSQL, reached at `DATABASE_URL`.
- **Mail:** `mailpit`, reached over real SMTP at `SMTP_HOST` and `SMTP_PORT`
  with `SMTP_USER` and `SMTP_PASS`.
- **Auth:** email and password implemented by the app, with bearer tokens.
  Passwords hashed. Tokens expire after `24 hours`.
- **Health:** `GET /api/health` returns `200` once the app is ready.
- **Logging:** request logs to stdout.

Read every host, port and credential from the environment; never hardcode one.
The backing services named in this brief are already running and reachable at
those environment variables. Do not download, install, compile or start a copy
of either of them.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing services available in this environment are
PostgreSQL and `mailpit`, and reaching for anything else is a contract
violation.

**Capacity under contention.** Two acceptances against the last remaining
capacity of one window resolve to exactly one booking. The window's
`committed_days` never exceeds its `capacity_days`, no partial booking survives
a refusal, and the refused caller is told which window filled and what is still
open. A hold changes no capacity at all.

**Mail is real.** A message named in `## Core features` exists as a real message
in `mailpit`, addressed to exactly the recipient named, with no cc and no bcc.
It is sent after the state change commits, and a send failure leaves the state
change standing.

**Authorisation per write.** Every write decides authorisation from the session
or from the enquiry token, never from a field in the request body. A role named
in a request body is ignored.

**Rate limits.** The enquiry form and the sign-in link request are each rate
limited per address, and a refusal states how long to wait in words.

**Security headers.** Every response carries the standard security headers,
including a strict transport policy and a nosniff content-type policy.

**No secrets in the bundle.** No credential, API key or admin token appears in
anything the browser downloads.

**Security and abuse.** The enquiry form is the attack surface. It is rate
limited, its stored values are rendered as text and never as markup, and a
hostile input is shown back to the studio exactly as it was typed rather than
interpreted. Tokens are opaque, single-purpose and expire. A session ends on
sign-out and cannot be resumed by going back.

**The font budget.** Three faces in a modern format, each subset to the glyphs
the product actually sets, with a legacy format offered only where the modern
one is refused. The reference shipped its faces unsubset and paid megabytes for
them; a further subset on demand is available for any face that needs one. The
metrics-matched fallbacks are what let the first screen render before any of
them arrive.

**Performance, and what is deferred.** The first screen of the home document
renders before the display faces arrive, which is what the metrics-matched
fallbacks are for. Everything below the first screen, every project medium and
the moving hero ground are deferred until they are needed or the document
reaches them. Scroll stays smooth at the size in the responsiveness bar below.

**Instrumentation.** The seven events named in `## Core features` are recorded
in this product's own store and sent nowhere else.

**Responsiveness bar.** The app stays responsive with `9` projects, `40`
windows, `500` enquiries and `2000` messages, and the home document keeps
scrolling smoothly at that size.

**Discovery.** `GET /sitemap.xml` lists every public route and `GET /robots.txt`
points at that sitemap by its absolute address.

## Data model

Twelve tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account
so a grader can sign in.

### accounts

`id`, `email` (unique, case-folded on write), `password_hash` (never returned by
any endpoint), `display_name` (1 to 60), `organisation` (0 to 120), `role`
(`client` or `studio`), `timezone`, `created_at`, `last_seen_at`. Signup always
writes `client`; exactly one `studio` exists, by seed.

### projects

`id`, `slug` (unique, kebab-case), `title`, `discipline`, `year`, `description`,
`link`, `position` (unique, ascending), `state` (`published` or `draft`).

### services

`id`, `title`, `body`, `position`.

### social_links

`id`, `label`, `href`, `position`.

### site_meta

`id`, `version`, `predecessor_label`, `predecessor_link`, `local_timezone`. One
row, read by the footer. It is content, not a build constant.

### windows

`id`, `starts_on` (date), `weeks`, `capacity_days` (`1` to `5`),
`committed_days` (starts at `0`), `state` (`open`, `held`, `booked`, `closed`).

### holds

`id`, `window_id`, `enquiry_id` (null until the enquiry exists), `days`,
`expires_at`, `released_at` (null while live). A hold is live when `released_at`
is null and `expires_at` has not passed.

### enquiries

`id`, `token` (unique, opaque), `account_id` (null when the sender took no
account), `name`, `email`, `organisation`, `looking_for`, `budget_band`,
`message`, `window_id` (null when the hold lapsed before submit), `state`
(`new`, `reading`, `proposed`, `booked`, `declined`, `withdrawn`, `lapsed`),
`created_at`.

### messages

`id`, `enquiry_id`, `author` (`client` or `studio`), `body` (1 to 4000),
`created_at`.

### proposals

`id`, `enquiry_id`, `starts_on`, `weeks`, `days_per_week`, `note`, `state`
(`live`, `accepted`, `expired`, `superseded`), `expires_at`, `created_at`.

### bookings

`id`, `enquiry_id` (unique), `window_id`, `starts_on`, `weeks`, `days_per_week`,
`confirmed_at`.

### page_views

`id`, `route`, `viewed_at`. Written only when the cookie answer was yes, read by
the studio alone, and carrying nothing about the person.

### Relationships

| From | To | Cardinality |
|---|---|---|
| `window` | `hold` | one to many, at most `3` live |
| `window` | `booking` | one to many, bounded by `capacity_days` |
| `enquiry` | `message` | one to many |
| `enquiry` | `proposal` | one to many, at most one `live` |
| `enquiry` | `booking` | one to at most one |
| `account` | `enquiry` | one to many, and an enquiry may have no account |

### Persistence

Every entity above survives a reload, a new tab and a new device. A hold is
server-side and is tied to its enquiry rather than to a browser, so it survives
all three. Three things live in the browser and nowhere else: the enquiry
draft, the sound setting and the session. The draft is the one that matters,
and it is why an offline visitor keeps their answers.

A schema migration runs before the app serves its first request, and running it
twice changes nothing.

### Invariants

- `windows.committed_days` equals the sum of `days_per_week` over that window's
  bookings, always, and never exceeds `capacity_days`.
- Two acceptances against the last remaining capacity of one window resolve to
  exactly one booking; no partial booking survives the refusal.
- A window carries at most `3` live holds.
- A hold changes no `committed_days`.
- At most one proposal per enquiry is `live`.
- One booking per enquiry, at most.
- The availability mode is derived on every read and is stored nowhere.
- An enquiry row is never deleted.
- A project `position` is unique and ascending.

### Seed data

Two accounts as listed in `## User roles`, with the display names Elian Moreau
and Alex Renard.

Three windows, measured from the first start: one `open` starting in `10` days
for `6` weeks at `3` capacity days, one `open` starting in `40` days for `8`
weeks at `2` capacity days, and one `booked` starting in `90` days for `4` weeks
at `2` capacity days with `2` committed. The first is what makes a fresh install
show the open-now pill; the third is the boundary the capacity rule is attacked
at.

Nine projects, in position order: `Meridian` (Development, `2026`),
`Auriga Concept` (Design & Development, `2025`), `Portfolio 2.0`
(Design & Development, `2024`), `Uplink Usability` (Design, `2023`),
`Tower Supervision` (Design, `2023`), `Colisa` (Design, `2023`),
`UBX Roadmap` (Design & Development, `2022`), `Aera Unity`
(Design & Development, `2023`), `Baba Quiz` (Design & Development, `2021`).

Three services: `SEO`, `UX Design` and `Web & Mobile Development`. Three social
links. One `site_meta` row.

One seeded enquiry from Alex Renard against the first open window, in state
`proposed`, carrying two messages and one live proposal. It is deliberately the
most interesting state in the workflow, so a fresh install opens on something
rather than on an empty pipeline.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual detail in full. It states no rule that is not
already a requirement elsewhere; it says what the surfaces are and how they
behave.

### The fixed chrome

Present on every public route at every width. Four slots: the name lockup at the
left, two stacked lines for the given and family names with a small monogram of
two stepped keycaps set to their upper right, carrying the two initials; the
availability pill at the centre; the sound control at the right; and the four
navigation targets at the right, folding into a burger below the mid switch.

The header has no ground of its own at the top of the document and acquires a
blurred, darkened ground as content passes under it, scrubbed against scroll
position rather than played on a timer.

The lockup enters by sliding in from the left rather than fading. The pill
enters from the upper left. Both arrive on load.

### The availability pill

A pill-radius control with a hairline border in the signal green over the dark
ground, carrying its state in words and a small filled circle with a soft halo
of the same green. It sits inside a container with the smaller surface rounding.

It has one job and it must never lie: it reads the derived mode, it is never
absent, and no interface anywhere allows its words to be typed.

### The route label

Present on every route except the home document. It names the current route in
the top left of the content area, under the chrome, with a single rounded corner
where it meets the page edge. It enters by rising into place on a route change.

### The fixed rail

At the left edge on every public route above the mid switch: a narrow strip
carrying two award badges and a vertical label reading `Honors`, rotated to read
bottom to top. It never scrolls and it is neither chrome nor content. Below the
mid switch it is hidden.

### The custom cursor

Above the mid switch, over the project rows of the work index, the pointer is
replaced by a circular element and a label naming the action, reading `View`.
Below the mid switch it is not rendered and the label becomes a visible control
on each row.

### The hero

The eyebrow reads `Creative Developer`, set in the display face and stroked. The
name sits under it at display size in the same face, filled. `Located in France`
sits below with a three-segment bar under it in blue, white and red, the French
flag rendered as a bar rather than as an image. The prompt reads
`Scroll down to explore` with a stroked arrow, and it is the last thing to
arrive, fading in slowly after everything else has settled.

A moving ground sits behind the name, with a halo in the two bright indigos. It
holds one frame under a reduced-motion preference.

### The about section

Reached where the pale sheet slides up over the dark hero. Its title is the word
`About`, a sixteen-point asterisk, and the word `me`, set in the stroked display
face in the accent indigo on the pale ground with a drawn underline beneath it.
Both section titles on the site use this construction and there is no other
heading system.

Under it the statement, at display size set loose, split per word with the
shadow reveal. Beside it the figure `5+` with the label `years of experience`.
Then the three services, each a title and a line. Then a horizontally scrolling
band of tool marks, each carrying an accessible name, hidden from assistive
technology as a group and not auto-scrolling while it is touched.

### The selected-work preview and the work index

The home preview shows the nine projects as rules and rows: a rule, a title at
the left, a credit line right-aligned in the same row carrying the discipline
and the year, then a rule. The `/work` route shows the same nine as a staggered
pill layout with a title pill and a description pill. One record set, two
presentations, one component at two densities.

A quadratic text arc sits in the home preview with text set along it, bending as
the document advances.

### The contact surface

On the dark ground with a faint contour texture. The headline reads
`LET'S BUILD YOUR IDEA TOGETHER :)` in the stroked display face across four
lines, the typed emoticon set at the same size as the rest and rendered as
outlined glyphs, not as a drawing. A circular portrait with an accent ring sits
beside the first line.

The six fields are numbered, each a label over an underlined input with no box.
The rule under each input is a hairline, turning to the signal green on focus
over the dark ground and to the accent indigo over the pale one. The required
mark is its own element. Errors are the accent's selection tint plus the words,
never red. Placeholders are worked examples and use the secondary text colour so
they can be read.

A side column carries `Further Inquiries` with the contact address and
`Located in France 📍`, then `Social Media` with the three links.

### The studio surfaces

Behind the sign-in, under a persistent left sidebar rather than the public
chrome. The pipeline is a calendar grid laid out by window and by state, with
rows in the same treatment the work preview uses at its densest. The proposal
form opens as a slide-over from the right, carrying a start date constrained to
the window, a length in weeks, a capacity in days per week constrained by what
the window has left, and a free note, with the window's remaining capacity shown
live above the fields.

### The footer

Four heads: `Local Time`, `Version`, `Resource` and `Social Media`. The clock
renders the studio's local time. The version and the predecessor label are read
from the stored meta row rather than from a build constant, so the footer cannot
claim a version that is not live. A credit line closes it.

### The module boundary

The product divides into two module groups and the boundary between them is
worth holding: the public documents, which read and render, and the booking
layer, which writes. The public component architecture is the chrome, the
document sections, the row component at its two densities, the field, the pill
and the drawn mark. The booking layer adds the pipeline grid, the thread, the
proposal slide-over and the account panel, and it introduces no new shape and
no new colour.

### Procedural assets, no binaries, a zero-asset guide

Every asset in this product is drawn in code. Name the three font families and
give each a metrics-matched fallback rather than shipping a font file. Draw the
monogram, the burger, the arrow, the sixteen-point asterisk and the text arc as
inline vector geometry, each as a stroked path that draws itself on. The two
award badges and the tool marks belong to other organisations and are replaced
with neutral drawn marks. The nine projects' media is generated from each
project's own record rather than shipped as images. The hero's ground is drawn,
not a video. No audio file ships either: the sound control exists and remembers
its setting, and the cue set behind it is out of scope.

### Copy that is pinned

- The availability pill: `available now for work`, `available from`,
  `booked until`, `not taking new work`.
- The sound control: `Sound | OFF` and `Sound | ON`.
- Navigation: `Home`, `About`, `Work`, `Contact`. The rail: `Honors`. The
  cursor: `View`.
- The hero: `Creative Developer`, `Located in France`, `Scroll down to explore`.
- The about statement, one string, set at display size and revealed word by
  word: `An award-winning, product-minded frontend engineer with a background
  in aerospace engineering and human factors. I design and build visually
  striking web and mobile products where usability, reliability and performance
  matter, from concept to launch, with a strong focus on thoughtful UX,
  engaging interactions and practical AI-powered workflows.`
- The about figure: `5+` and `years of experience`.
- The three services, each a title and a line: `SEO` with
  `Optimizing data to improve search engine rankings.`; `UX Design` with
  `From product's exploration to evaluation.`; and `Web & Mobile Development`
  with `Industry-leading tools such as React, Three, Framer will be used to
  build your app.`
- The three social links, in order: `Linkedin`, `Postline`, `Showcase`.
- The work headline:
  `Elevate user experience through cutting-edge technology and design`.
- The contact headline: `LET'S BUILD YOUR IDEA TOGETHER :)` and the submit
  `Send it now :)`.
- The footer heads: `Local Time`, `Version`, `Resource`, `Social Media`.
- Everything else the interface says is listed against its rule in
  `## Core features`.

## Constraints

Single tenancy: one studio, one site, no organisations above the account.

Not built, and each for a stated reason. **Payment of any kind**, because a
booking here is an agreed start date and nothing more; no contract, no invoice,
no card, and nothing that reads as one. **File upload anywhere**, because the
enquiry is six text fields and an attachment brings scanning, storage and
retention duties a contact form does not need. **The twenty-one sound cues**:
the control, its two strings and the rule that no state is carried by sound
alone are all required, but the cue set itself is not built. **The
three-dimensional render pipeline** behind the hero: a moving drawn ground is
required, a real-time scene graph is not. **A password policy, a staff
hierarchy, an editor role and an admin role**, because this is one person's site
and a hierarchy for a single operator is work nobody will use. **Follow-up mail
chasing an unanswered enquiry, newsletters, and any marketing use of what an
enquiry disclosed.** **Third-party analytics**: the page-view record is local
and gated on the cookie answer. **Translation**: the product ships in one
language.

No borrowed identity ships. No third party brand name, no proprietary font
binary, no logo file, no award badge and no tool mark belonging to another
organisation is included; every asset is drawn in code. Any class-name prefix
your tooling generates is a framework artefact and must not carry a product
name.

The app must stay responsive at `9` projects, `40` windows, `500` enquiries and
`2000` messages.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server, never a dev server.
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

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{"email", "password", "display_name", "organisation"}` | the account and a bearer token |
| `POST /api/auth/login` | `{"email", "password"}` | the account and a bearer token |
| `GET /api/auth/me` | none | the account with `enquiry_count` and `booking_count` |
| `POST /api/auth/link` | `{"email"}` | an acceptance, always |
| `GET /api/health` | none | `200` |
| `GET /api/meta` | none | `{"version", "predecessor_label", "local_time"}` |
| `GET /api/projects` | none | a top-level JSON array in position order |
| `GET /api/projects/{slug}` | none | the project |
| `GET /api/services` | none | a top-level JSON array |
| `GET /api/availability` | none | `{"mode", "from_date", "note", "windows"}` |
| `POST /api/windows` | `{"starts_on", "weeks", "capacity_days"}` | the created window |
| `PATCH /api/windows/{id}` | `{"state"}` or `{"capacity_days"}` | the updated window |
| `POST /api/holds` | `{"window_id", "days"}` | the created hold with `expires_at` |
| `DELETE /api/holds/{id}` | none | an empty success |
| `POST /api/enquiries` | the six fields plus optional `hold_id` | the enquiry with its `token` |
| `GET /api/enquiries/{id}` | optional `token` query | `{"enquiry", "messages", "proposal", "booking"}` |
| `PATCH /api/enquiries/{id}` | `{"state"}` | the updated enquiry |
| `POST /api/enquiries/{id}/messages` | `{"body"}` | the created message |
| `POST /api/enquiries/{id}/proposals` | `{"starts_on", "weeks", "days_per_week", "note"}` | the created proposal |
| `POST /api/enquiries/{id}/accept` | `{"proposal_id"}` | the created booking |
| `POST /api/enquiries/{id}/withdraw` | none | the updated enquiry |
| `GET /api/pipeline` | optional `state`, `band` | a top-level JSON array, newest first |
| `GET /api/export` | none | every enquiry, message, proposal, booking and window |
| `POST /api/consent` | `{"accepted"}` | the recorded choice |
| `GET /api/page-views` | none | a top-level JSON array |

Field names are exact. Every list endpoint returns a top-level JSON array. A
successful call returns the named resource or shape; an invalid or unauthorized
call is rejected as a client error, never as a server error and never as a
silent success, and carries a message naming the reason. Bearer auth is required
on every endpoint except signup, login, health, the sign-in link request, the
consent record and the public reads; the enquiry endpoints additionally accept
the enquiry token.

### No mocks

`mailpit` is the only place a message lives. An in-memory `sent` array, a
hardcoded success the app returns to itself, a log line standing in for a send,
and a message the app claims to have sent that is not in the inbox are all
contract violations, however correct the page looks. The named provider is the
fact: the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it. The same holds for capacity: the window row
in PostgreSQL is the fact, and a count the interface keeps for itself is not a
booking.

## Definition of done

A visitor can read the work, see from the badge that the studio is free, hold an
open window, send a scoped brief, and find a confirmation carrying their own six
answers waiting in their inbox. The studio can read it, propose a start date,
and have the visitor accept it into a booking, after which the badge tells the
truth about the new calendar without anybody editing it. When two people accept
the last place in one window at the same moment, exactly one of them is booked
and the other is told which window filled and what is still open.
