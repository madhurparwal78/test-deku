# Sovereign Hosting Studio

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, describe a software build with a Germany-only data requirement, attach
a written brief, send it, and receive a reference number and an indicative
figure the server agrees with, without hitting an error page. A different
stranger, signed in as another client or signed in as nobody at all, must NOT be
able to read that request or download the brief attached to it, by any means:
not from a list, not by typing its address, and not by asking the object store
for the file directly. The attached brief must live as a real object in the
`minio` bucket at its scheme's key; a copy on the app container's own disk does
not count.

## Overview

`Vela Studio` is a one-person software studio in Marburg. Its founder,
`Anton Ferber`, writes production software and runs it on hardware the studio
owns in Europe. The site sells three things at once: the work, the independence
of the infrastructure under it, and the fact that the person who answers the
mail is the person who writes the code. Its buyer is a European, technical or
technical-adjacent, who has been handed software they cannot see into and
hosting they cannot point at on a map.

The site makes the argument, proves it, and lets the buyer start a job. The
argument is a dark, scroll-driven home page: a philosophy statement that writes
itself word by word, and four pinned capability cards whose line diagrams draw
themselves while the card holds still. The proof is a public status board for
every system the studio runs, with an honest incident record, and a library of
finished builds in which every number was measured on a stated day. The job
starts with a scoped build request that returns an indicative figure from a
published rule table, works with scripts switched off, and talks to no other
company's server.

Behind it sits the studio: the founder reviews requests, records checks,
annotates incidents, publishes build records and uploads the portrait. A buyer
may sign up to follow the requests they sent while signed in.

This is not a shop, a blog or a helpdesk. There is no payment, no comment, no
chat, no newsletter, no search, no menu bar on the public site and no cookie on
any route. The hard part is the request boundary: a request and its attached
brief belong to the studio and to the client who sent it, and to nobody else.

## User roles

Two roles, and an anonymous visitor who holds neither.

| Role | Can do |
|---|---|
| anonymous visitor | Reads every public route, watches the status board, reads incidents and published build records, and submits a build request with or without an attached brief. **Cannot** read any submitted request, **cannot** download any attached brief, **cannot** reach `/account` or any `/studio` route, and **cannot** write anything except a build request and a page view. |
| `client` | Everything the visitor can do, plus a list at `/account` of the requests they submitted while signed in, each with its status, and a download of the brief attached to one of those. **Cannot** read another client's request or brief, **cannot** change any status, **cannot** reach any `/studio` route or any studio endpoint. Signup always creates a `client`. |
| `founder` | The studio. Reads every request and every attached brief, moves a request through its review statuses, creates systems and records their checks, appends notes to incidents, creates, publishes and unpublishes build records and their measurements, uploads the portrait, and reads the page-view log. The founder account is seeded and is never created through signup. |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `client` session
to any `founder`-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged. The same
holds for an anonymous caller against any endpoint that needs a session.

Signup is open. `POST /api/auth/signup` creates a `client` whatever role the
request body claims. Seeded accounts, each with the password
`deku-demo-pw-2026`:

| Email | Role |
|---|---|
| `founder@example.com` | `founder` |
| `client@example.com` | `client` |
| `client2@example.com` | `client` |

## Core features

**1. The request boundary.** A build request and the brief attached to it are
readable by the `founder` and by the `client` who submitted it while signed in,
and by nobody else. Any other caller, whether anonymous or another `client`,
who asks for the request by its reference, lists requests, or asks for its
attached brief is refused, and the refusal reveals nothing about the request.
The object in the bucket is not anonymously readable either: the app never
widens the bucket's access, so a request for the object's address sent straight
to `minio` without the storage credentials is refused. A request submitted
while signed out belongs to the studio alone and appears in no `client`'s list.
The seeded request `VS-2026-0001` belongs to `client@example.com` and carries an
attached brief; `client2@example.com` must reach neither.

**2. Attached briefs live in the object store.** A build request may carry at
most one attached brief: a PDF, PNG or JPEG file of at most `5 MB`, which is
`5242880` bytes. The type is decided by the file's own bytes, not by its name or
its declared type. Its bytes are stored in `minio`, the S3-compatible object
store, at the key `requests/{reference}/{sha256_of_bytes}.{ext}`, where `{ext}`
is `pdf`, `png` or `jpg`, for example `requests/VS-2026-0003/9f2a...d0.pdf`. The
database row records where the bytes are; the bucket is where they are. A file
whose bytes are anything else, or a larger one, is rejected as invalid, and the
whole submission writes nothing: no request row, no attachment row, no object.
The owner and the founder read the brief through
the app, by one of two mechanisms, and the app picks one and uses it everywhere:
an authenticated endpoint that streams the bytes itself, or a presigned link
that expires within five minutes and is never issued to anybody who is not
entitled.

**3. The composer.** `/build-request` is a form headed `Describe the build`. It
asks for: the capabilities wanted, at least one of `software`, `website` and
`hosting`; the hosting posture, `managed` or `handover`; the data residency,
`eu` or `de`; the timeline, `flexible`, `standard` or `accelerated`; the budget
band, `under-10k`, `10k-25k`, `25k-60k` or `over-60k`; a description of what
exists today, between `20` and `4000` characters; a contact name; a contact
email; and an optional attached brief. The indicative figure updates as fields
change. Every field except the contact details and the file is written into the
page's address, so a half-finished request survives a reload and can be pasted
to a colleague: the address carries `cap`, `posture`, `residency`, `timeline`,
`budget`, `desc` and `v`, in that order, with `cap` listing the chosen
capabilities comma-separated in the order `software`, `website`, `hosting`, and
`v` naming the rule table version. Two copies of the same composed state produce
byte-identical addresses. Opening such an address restores every field and
shows the same figure. The address is replaced as the visitor edits rather than
added to history, so the back button leaves the composer rather than walking
back through keystrokes. Beneath the form a small `Sign in` link opens `/login`
carrying the composer's current address as the page to return to.

**4. The indicative figure.** The figure comes from a published rule table and
is stored in integer euro cents, currency `eur`. Version `2026-09` is current:

- capability amounts: `software` `1200000`, `website` `600000`, `hosting`
  `300000`, summed over the chosen capabilities;
- posture: `managed` adds nothing, `handover` adds `150000`;
- residency: `eu` adds nothing, `de` adds ten percent of the capability sum;
- timeline: the subtotal is multiplied by `90` percent for `flexible`, `100`
  percent for `standard`, `125` percent for `accelerated`;
- the result is rounded to the nearest `50000`, and an exact half rounds up.

It is shown as `EUR` followed by whole euros with a comma between thousands, for
example `EUR 12,000`. These rows are worked examples of the rule:

| Capabilities | Posture | Residency | Timeline | Figure |
|---|---|---|---|---|
| `software` | `managed` | `eu` | `standard` | `1200000`, shown `EUR 12,000` |
| `website` | `managed` | `eu` | `flexible` | `550000`, shown `EUR 5,500` |
| `hosting` | `managed` | `de` | `standard` | `350000`, shown `EUR 3,500` |
| `website` | `managed` | `de` | `accelerated` | `850000`, shown `EUR 8,500` (the subtotal times the rate is `825000`, an exact half, so it rounds up) |
| `software`, `website` | `handover` | `de` | `accelerated` | `2650000`, shown `EUR 26,500` |

The budget band never changes the figure; it is stored and shown beside it.

**5. The rule table is versioned.** Version `2026-03` is retired. It carries the
capability amounts `software` `1000000`, `website` `500000` and `hosting`
`250000`, and every other rule of `2026-09` unchanged, so `software`, `managed`,
`eu`, `standard` gives `1000000`, shown `EUR 10,000`. A composed address naming
`v=2026-03` reopens showing the figure quoted under `2026-03`, labelled with that
version, rather than today's figure. A submission must name the current version;
one naming a retired or unknown version is rejected as invalid, the rejection
names `rules_version`, and nothing is written. `GET /api/pricing-rules` returns
the current table with its `version`, and `GET /api/pricing-rules/{version}`
returns any version, current or retired.

**6. The server checks the figure.** Every submission names the rule table
version it used, as `rules_version`. The composer's scripted submission also
carries the figure the page computed, as `indicative_minor`. The server always
recomputes the figure from its own copy of that table. When a submission carries
a figure and the two differ, the submission is rejected as invalid, the
rejection names `indicative_minor`, and nothing is written. A submission that
carries no figure is accepted and stored with the server's figure. A stored
request keeps its figure and its version forever: later changes to the table
never rewrite it. In a JSON submission `capabilities` is an array of the keys;
repeated keys count once, and the stored list is always in the order
`software`, `website`, `hosting`.

**7. Reference numbers.** Every accepted request receives a reference of the
form `VS-<year>-<NNNN>`: the UTC year of submission and a four-digit sequence
within that year, zero padded, starting at `0001`. The two seeded requests are
`VS-2026-0001` and `VS-2026-0002`, so the next request accepted in 2026 is
`VS-2026-0003`. No two requests share a reference, and a later request always
carries the higher number. Two requests accepted at the same moment still
receive two different references, with no number skipped or repeated.

**8. It works with no scripts.** With scripts switched off, the same form at
`/build-request` posts as a plain form to `/build-request`, with the same field
names the API uses, and the server answers with a rendered summary page headed
`Request received`. The page shows the new reference, the figure, the rule
table version and the status `new`. When a submission carries no figure, the
server computes it; the reference comes from the same sequence the scripted path
uses. A form submission may carry `capabilities` repeated once per capability or
as one comma-separated value, and both are accepted.

**9. Spam is refused without watching anyone.** The form carries a decoy field,
`contact_fax`, that a person never sees and never fills. A submission with any
value in it is refused and writes nothing. A visitor who submits the same
enquiry repeatedly, meaning the same contact email with the same description
again from the same network address within ten minutes, has the repeat refused
as a duplicate, and the repeat writes nothing. There is no third-party
challenge, no tracking script and no cookie, and the network address used to
spot a repeat is never written to any table.

**10. Reviewing a request.** A request starts `new`. The founder moves it to
`reviewing`, then `quoted`, then `accepted` or `declined`; a `new` or
`reviewing` request may also go straight to `declined`. `accepted` and
`declined` are final. Any other move, such as `new` to `quoted` or `accepted`
back to `reviewing`, is rejected as invalid and the request is unchanged. A
`client` who tries to change a status is denied and the request is unchanged. A
signed-in `client` sees each of their own requests on `/account` with its
reference, its figure and its current status.

**11. The status feed.** `GET /api/uptime/projects` is public, needs no session
and answers from the site's own origin. It returns one envelope, and this is the
one endpoint whose body is not a top-level array:

```
{ "data": { "nextCheckAt": "<timestamp>" or null,
            "projects": [ { "id", "slug", "name", "position",
                            "currentStatus", "uptimePercent",
                            "latestResponseMs", "latestCheckedAt",
                            "lastStatusChangeAt",
                            "bars": [ { "status", "checkedAt" } ] } ] } }
```

A failure answers `{ "error": { "message": "<sentence>" } }`. Timestamps are ISO
8601 in UTC. `projects` is sorted by `position`, the order the studio set, and
never by name. `currentStatus` is one of `up`, `slow`, `degraded`, `down` and
`unknown`, and is the status of the system's latest check, or `unknown` when the
system has none. `latestResponseMs` and `latestCheckedAt` come from the latest
check, and both are null when there is none. `lastStatusChangeAt` is the time of
the first check in the system's current unbroken run of its current status,
counting real checks only, so an unknown slot never breaks or starts a run; it
is null when the system has no check. `nextCheckAt` is the
earliest, across all systems, of a system's latest check time plus that
system's check interval, and the `Next check` tile counts down to it rather than
to the page's own refresh. The feed carries no client name, no address and no
identifier beyond an opaque system id.

**12. Recording checks.** The founder records a check for a system with
`POST /api/systems/{slug}/checks`, carrying `checked_at`, `status` and
`response_ms`. The status is one of `up`, `slow`, `degraded` and `down`;
`unknown` is never recorded, because it means nobody checked, and a check
posted with it is rejected as invalid. `response_ms` is a whole number of
milliseconds, zero or more, or null. One system holds at most one check for a
given time. An exact repeat, meaning the same `checked_at` with the same
`status`, is accepted and changes nothing, whatever its `response_ms`; a
different status for a time already recorded is rejected. The same check sent
twice at the same moment still leaves one row. Checks arrive in time order, and
a check older than the system's latest recorded check that is not an exact
repeat is rejected. A check for an unknown slug answers not-found.

The founder creates a system with `POST /api/systems`. Each system has a check
interval, in seconds, set when it is created and `300` unless stated; the
interval is a whole number of at least `60`. A slug that is already taken, an
interval below `60`, or a threshold below `1` is rejected as invalid and creates
nothing.

**13. Unknown slots and the uptime figure.** Between two consecutive checks
`a` and `b`, the feed places unknown slots for every interval the collector
missed: their count is the gap divided by the interval, rounded to the nearest
whole number, minus one, and never below zero. Each unknown slot carries the
time it should have been checked. `bars` holds the system's most recent `90`
slots, oldest first, unknown slots included, and ends with the latest check.
`uptimePercent` is the share of the real checks inside those slots whose status
is `up` or `slow`, as a percentage rounded to two decimals; unknown slots count
neither for nor against it, and a system with no check reports null. A window
the collector missed is never shown as up. Worked examples, all at an interval
of `300`:

| Checks recorded | Bars | `uptimePercent` |
|---|---|---|
| `10:00` up, `10:05` up, `10:10` down, `10:25` up | up, up, down, unknown, unknown, up | `75.00` |
| `10:00` up, `10:05` slow, `10:10` degraded, `10:15` up | up, slow, degraded, up | `75.00` |
| `10:00` up, `10:05` up, `10:10` down | up, up, down | `66.67` |

**14. Incidents open and close with hysteresis.** Each system stores two
thresholds, `open_after` and `close_after`, set when it is created and `3` and
`2` unless stated. A check whose status is `degraded` or `down` is failing; `up`
and `slow` are available. An incident opens when `open_after` consecutive checks
are failing, and its opening time is the first of those checks. It resolves when
`close_after` consecutive checks are available after it opened, and its
resolution time is the check that completed the run. A system holds at most one
open incident. A single failing check is not an incident and a single available
check is not a recovery, so a system flapping between the two produces one
incident, not one per flap. For example, a system with `open_after` `2` and
`close_after` `3` whose ten checks, five minutes apart from `11:00`, read down,
down, up, down, up, down, up, up, up, up holds exactly one incident: opened at
`11:00` and resolved at `11:40`. An incident's reference is the system's slug, the
opening date and the opening hour and minute, joined by hyphens, for example
`vela-studio-console-20260901-1420`. Replaying the same stream of checks
produces the same incidents with the same references and nothing new.

**15. The incident record is append-only.** Each incident carries a log of
entries, each with a `seq`, a `kind` of `opened`, `note` or `resolved`, a body and
a time. `seq` counts upward by one across every entry of every incident of one
system, starting at `1`. Opening and resolving each write one entry. The founder
appends a note with `POST /api/uptime/incidents/{ref}/notes`, days later if need
be, and the note joins the log without changing anything before it. No entry is
ever edited or deleted: a request to change or remove one is rejected and the
log is unchanged. Two notes appended at the same moment receive two consecutive
`seq` values, never the same one. Anybody may read `GET /api/uptime/incidents`,
newest first, where each incident names its system by slug in `system`, and
`GET /api/uptime/incidents/{ref}`. A note from anybody but the founder is denied,
and an empty note is rejected as invalid. The seeded incident
`vela-studio-console-20260901-1420` opened at `2026-09-01T14:20:00Z`, resolved at
`2026-09-01T14:40:00Z`, and carries three entries: `opened`, `resolved`, then the
note
`Disk pressure on the Frankfurt node; the database moved to Falkenstein while the volume was replaced.`

**16. The status board.** `/uptime` lists every system as a card in feed order.
Four tiles sit above the cards and are worked out in the page from the feed,
never sent by the server: `Systems`, the count; `Operational`, the count whose
status is `up`, a slash with no space on either side, and the total, as in `6/7`; `Average uptime`, the mean of every
system's uptime that is a number, to two decimals; and `Next check`, the whole
seconds until `nextCheckAt` rounded up and followed by `s`, as in `27s`,
recomputed every second, reading `Due now` once that moment has passed. The
tiles appear only when there is data. Each card names the system, shows a pill with the status in words beside
a dot, the four values `Uptime`, `Response time`, `Last checked` and
`Last status change`, and a strip of bars, one per slot, as many of the most
recent as fit the card's width. A null response time shows a single dash; a null
check time shows `Awaiting checks`. The first load shows a shimmering skeleton;
later refreshes swap values in place with no skeleton and no spinner. The page
refreshes every thirty seconds, only while the tab is visible, and never starts a
refresh while one is still open. A failed refresh replaces the list and removes
the tiles, showing the failure block, rather than leaving old numbers dressed as
current. An empty project list shows the empty block. Below the cards, an
`Incident history` section lists incidents newest first with the system name,
the opening time and the resolution time or `Ongoing`, each opening its own
page at `/uptime/incidents/<ref>`, which lists the entries in `seq` order; with no
incident it reads `No incidents recorded.` With scripts switched off, the board
still renders its heading, lede, incident history and notice, and in place of
the cards says `Live status needs JavaScript to load.`

**17. The build library.** `/builds` lists the published build records as cards,
newest delivery first, and filters them by capability. Choosing a capability
narrows the list without a full page load and writes the choice into the
address as `/builds?capability=software`, `website` or `hosting`; the back
button walks back through the filters. With scripts switched off the same
filters are plain links. Each record at `/builds/<slug>` shows its title, its
capability, its summary, its body, its stack, its start and delivery dates, its
client, its measurements and its diagram. A record whose client is withheld
shows `Client withheld` in place of a name. Every figure on a record is a stored
measurement shown with the date it was measured, and a record with no
measurement shows `Not yet measured` rather than any number. The founder adds a
measurement with `POST /api/builds/{slug}/measurements`: the `metric` is one of
`lcp_ms`, `cls`, `p95_api_ms` and `uptime_percent`, the `value` is a number of
zero or more, and `measured_on` is a date; anything else is rejected as invalid
and nothing is saved. A record that is not published is absent from every public
list and its address answers not-found, revealing nothing about whether it
exists. Publishing makes it listed and readable in one act; unpublishing
withdraws both at once. A slug that is already taken is rejected as invalid.

**18. Diagrams are data.** A build record's diagram is an ordered list of
primitives. Each primitive is an object whose `kind` is `rect`, `path` or
`circle`, with a `role` of `accent`, `structure` or `faint`, and the SVG
attribute names of its kind: `x`, `y`, `width`, `height` and an optional `rx` for
a `rect`; `d` for a `path`; `cx`, `cy` and `r` for a `circle`. The record
page draws the list in list order, under the same drawing rules as the four home
diagrams, and labels the drawing `Diagram:` followed by the record's title. A
record saved with a primitive of any other kind, or without a role, is rejected
as invalid and nothing is saved.

**19. The capability links reach real builds.** On card `02` the link
`Scope a build` opens the most recently delivered published record whose
capability is `software`; on card `03` `See a build` does the same for
`website`; on card `04` `See the stack` does the same for `hosting`. A record
that is not published is never the target. When a capability has no published
record, its link opens `/builds?capability=` with that capability instead. With
the seed data the three links open `/builds/harbour-ledger`,
`/builds/kestrel-storefront` and `/builds/lahn-clinic-hosting`, and the draft
`/builds/aurora-payroll-portal` is never one of them, although it was delivered
more recently than `harbour-ledger`. Card `05`'s `Status & uptime` opens
`/uptime`. The hero button `Talk to an engineer` and the contact prompt
`talk to an engineer_` open `/build-request`.

**20. The home argument.** `/` is one long argument in six numbered beats: the
hero; the pinned philosophy statement `01`; the heading `What we build`; the four
pinned capability cards `02` to `05`; the contact section `06`; and, below it,
the teaser to the founder page. Inside a pinned section the page holds still
while its content advances with the scroll. The philosophy statement and every
card's body are revealed one word at a time, each word coming out of a grey blur
into white, or into the amber accent for the words the studio marks, as a soft
edge a little over two words wide travels along the sentence. The reveal is
driven by how far the reader has scrolled through the section, not by a timer,
so scrolling back up un-reveals the words in exactly the reverse order. Beside
each card's words its diagram draws itself one line at a time in the listed
order, and finishes about two thirds of the way through the card's hold, well
before the next card arrives. A hairline under the philosophy statement fills
from the left as a progress bar. The hero drifts upward more slowly than the page
and fades away as the reader leaves it. In-page links glide to their target
rather than jumping, taking longer for longer distances, and a click with a
modifier key still opens a new tab. `See what we build` does not stop at the top
of card `02`, where nothing has been drawn yet: it lands at the moment that card
has finished drawing itself.

**21. A position can be shared.** While the reader scrolls through a pinned
section, the address records where they are as `at=<section>-<percent>`, where
`<section>` is one of `philosophy`, `software-platforms`, `websites`,
`managed-hosting` and `infrastructure` on `/`, or `craft` and `principle` on
`/about`, and `<percent>` is a whole number from `0` to `100`; for example
`/?at=managed-hosting-80`. The address is replaced as the reader settles, not
added to history, so the back button returns to the previously visited page and
never to an earlier scroll position. Two shares of the same moment produce
byte-identical addresses. Opening such an address in a fresh window, at a
different width and with the fonts not yet loaded, lands within one word of the
same reveal. With reduced motion requested, the same address lands at the top of
the named section with everything already revealed.

**22. Reduced motion and no scripts.** With reduced motion requested, no scroll
effect loads, the page keeps native scrolling, every word is shown at its
finished colour, every diagram is complete, and no animation loops. With scripts
switched off, every public route renders its complete copy from the server,
legible and styled, and every diagram is complete. The reveal only presents text
that is already in the page: no word is inserted by script, no word is removed
after it is revealed, and the paragraph reads in full with styles switched off,
with the spaces between words intact.

**23. The founder page.** `/about` opens with the founder's round portrait beside
the headline, inside a wide, soft amber halo, then two pinned statements, `01`
and `02`, revealed exactly as the home statement is, then a personal contact
section `03` whose prompt reads `about me_` and points at the founder's own site.
The portrait is the one photograph on the site, shown at two display sizes from
the one stored file. The founder uploads it at `/studio/portrait`, as a PNG or
JPEG file of at most `5 MB` decided by its bytes; anything else is rejected as
invalid and stores nothing. It is stored in `minio` at
`portrait/{sha256_of_bytes}.{ext}`, where `{ext}` is `png` or `jpg`, and served
to anyone at `GET /api/portrait`, with the alternative text
`Anton Ferber, founder of Vela Studio`. A later upload replaces the one shown.
Until one is uploaded, the page draws a lit, dark stand-in with a warm rim of
light, never a face, whose accessible name is `Portrait placeholder`, and
`GET /api/portrait` answers not-found.

**24. The legal documents.** `/impressum` and `/agb` are plain documents: a
centred column of text, one clause per block with a fine line above it, and an
in-flow link at the top reading `Back to Vela Studio`. They carry no script
element and load no script of any kind, no grain, no glow and no fixed chrome.
They are the only pages that carry the studio's phone number.

**25. The footer and the back pill.** Every public route ends with the same
footer, built from one list of five, `Home`, `About`, `Legal Notice`, `Terms` and
`Status/Uptime`, filtered by the current route: it never links to the page it is
on. `/about` and `/uptime` carry a fixed back pill at the top left reading
`Back`, which returns to `/`.

**26. Every internal link resolves.** Every internal link on every public route,
in the footer, the cards, the teaser, the board and the build library, opens a
page that exists.

**27. The page-view log.** Each public page view records one row carrying only
the route and the time, and nothing that identifies a person. The server records
a row when it renders a public route, which covers the legal pages that run no
script. `POST /api/page-views` records one row for a named public route, for a
view that happened without a page render, and a page never posts a view the
server already recorded. Only the `founder` reads the log, at
`/studio/page-views`; everyone else is denied it.

**28. No cookie, no identifier, no third party.** No response from any route sets
a cookie, including sign-in. No identifier is generated, stored or transmitted
about a visitor. The running site loads nothing from, and sends nothing to, any
origin but its own; there is no analytics script, no tag manager, no consent
banner and no web font fetched from elsewhere.

**29. The studio.** `/login` signs in both roles; the founder lands on `/studio`,
a client on `/account`. A sign-in lasts for the browser tab it was made in, until
the person signs out or closes the tab, and is never carried by a cookie; the
signed-in pages hold no private data in their markup and load it with the
session. `/studio` has a top bar reading `Requests`, `Builds`, `Systems`,
`Portrait` and `Page views`, with a `Sign out` button at its right end;
`/account` carries the same `Sign out` button above its list. The request inbox is a grid of cards, newest first,
each showing the reference, the contact name, the capabilities, the figure and
the status. Opening a card slides a panel in from the side over the inbox,
showing the request in full with its attached brief, and changing its status
there confirms with a brief toast reading `Status updated`. `/studio/builds` is a
grid of every record, published or not, and adding one, or adding a system at
`/studio/systems`, opens the same kind of side panel. A side panel closes with
the Escape key. Declining a request and unpublishing a record each ask for
confirmation first. Every studio route is refused to a `client` and to an
anonymous caller.

**30. Contrast holds.** Interactive text reaches a contrast ratio of at least
`4.5:1` against the page ground. The faintest grey is raised one step wherever it
is a link, including every footer link.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the argument: hero, `01` to `06`, teaser | none |
| `/about` | the founder page | none |
| `/uptime` | the status board and incident history | none |
| `/uptime/incidents/<ref>` | one incident and its log | none |
| `/impressum` | the legal notice | none |
| `/agb` | the terms | none |
| `/builds` | the build library, filtered by `capability` | none |
| `/builds/<slug>` | one published build record | none |
| `/build-request` | the composer, and the no-script summary on submit | none |
| `/signup` | creates a `client` | none |
| `/login` | sign-in for both roles | none |
| `/account` | the client's own requests | `client` |
| `/studio` | the request inbox | `founder` |
| `/studio/builds` | every build record | `founder` |
| `/studio/systems` | systems and their checks | `founder` |
| `/studio/portrait` | the portrait upload | `founder` |
| `/studio/page-views` | the page-view log | `founder` |

**Entry and redirects.** A signed-out visitor who opens `/account` or any
`/studio` route is sent to `/login`. Signing in as `founder@example.com` lands on
`/studio`; signing in as a `client` lands on `/account`. Signing out returns to
`/`. A sign-in started from the composer's `Sign in` link returns to that
exact composer address, with every field restored, instead of `/studio` or
`/account`. A build request needs no session, but a request sent with a session
that has since gone missing is refused with `401` and writes nothing; so is any
other action taken with a missing session. The page then goes to `/login`, and
from a composer page the sign-in again returns to the same composer address.
A `client` who opens a `/studio` route is refused and told the page belongs to
the studio. There is no menu bar on any public route: a visitor moves by the
footer, by the back pill on `/about` and `/uptime`, by the back link on the
legal pages, and by the composer's `Sign in` link.

**The wrong client.** Signs in as `client2@example.com` and follows a link a
colleague forwarded to `VS-2026-0001`: the request is refused and its brief is
refused, with nothing about either shown. Signed out, the same link is refused
too, and so is the stored file's own address. Opening
`/builds/aurora-payroll-portal` meets not-found. Trying to move a request's status
is denied, with nothing changed.

**The reader.** Opens `/`, sees the two-line headline and the city names along
the foot, scrolls, and watches the hero drift away as the philosophy statement
writes itself while its hairline fills. Scrolls back a little and watches the
words un-write in reverse, then on through `What we build` and the four cards,
each holding still while its words and its drawing complete. Returns to the top,
presses `See what we build`, and glides to card `02` already drawn. Ends on the
command-line contact screen, follows the teaser to `/about`, and uses the back
pill to return.

**The sharer.** Midway through card `04`, copies the address, which reads like
`/?at=managed-hosting-80`, opens it in a fresh window at a phone width, and lands
on the same card at the same point of its reveal.

**The watcher.** Opens `/uptime`, sees the skeleton once, then seven cards in the
studio's order, `Vela Studio` first and `Anton Ferber Portfolio` last reading
`Awaiting checks`. Watches the `Next check` tile count down, or read `Due now`
while a check is overdue, and the cards refresh in place. Scrolls to `Incident history` and opens
`vela-studio-console-20260901-1420`.

**The buyer.** Presses `Scope a build` on card `02` and reads
`/builds/harbour-ledger`. Presses `Talk to an engineer`, chooses `software`,
`handover`, `de` and `standard`, picks `25k-60k`, describes the job, and watches
the figure read `EUR 14,500`. Copies the address for a colleague, attaches a PDF
brief, enters a name and an email, and sends it. The summary reads
`Request received` with a reference such as `VS-2026-0003`.

**The buyer without scripts.** Fills the same form with scripts switched off,
sends it, and receives the rendered summary with a reference of the same shape
and the figure the server computed.

**The client.** Opens `/signup`, creates an account, signs in, sends a request,
and finds it on `/account` with the status `new` and the brief ready to
download.

**The founder.** Signs in as `founder@example.com`, opens a card in the inbox,
reads the request in the side panel, downloads the brief, moves the request to
`reviewing` and sees the toast `Status updated`. Adds a system in
`/studio/systems`, records its checks, sees one incident open, and appends a
note. Publishes a build record in `/studio/builds` and finds it on `/builds`.
Uploads the portrait at `/studio/portrait` and sees it on `/about`. Reads `/studio/page-views`.

**States.** Every list has an empty state: `No systems available` on the board,
`No incidents recorded.` in the incident history, `No build records yet.` in the
library, and `No requests yet.` on `/account` and in the inbox. Every page that
fetches shows a loading state. The composer marks each invalid field inline,
names it, and writes nothing. No error ever shows a raw server page.

## UI/UX notes

The north star: in the first moment a visitor should understand that one person
works here, in the dark, writing software and owning the machines it runs on,
and that the page itself is being written just ahead of them. The register is an
editorial argument on the story routes, a plain document on the legal routes,
and a quiet instrument on the status board and in the studio. Darkness over
decoration: the whole site is one near-black sheet, and anything that is not the
work or the argument stays out of the way.

**Accessibility.** Interactive text meets WCAG AA contrast against the ground.
Every interactive element shows a visible amber focus ring when reached by
keyboard, and on the amber button the ring turns dark; focus order follows the
page, text before drawing. Keyboard navigation reaches everything, and focusing
something below the fold scrolls to it without snapping back. Every genuine
target is comfortably sized for a finger, through padding rather than a bigger
visual box; the uptime bars are not targets. Every section is labelled by its
heading, every drawing carries a sentence of description, every icon-only
control carries a label, every decorative layer is hidden from assistive
technology, and every content image carries alternative text. Status is never
shown by colour alone: every pill states its status in words and every bar
states its status and time. The board announces that it is loading and announces
a failure. The status page has a heading level between the page title and each
system's name. In forced colours the drawings keep their strokes.

**Motion.** The motion character is quiet and eased. When a page loads, the lines
of the opening block rise into place one after another, each arriving from
slightly below and sharpening as it comes. After that exactly five things move
on their own: the back pill's dot breathes, the teaser arrow nudges sideways and
stops the moment it is pointed at, a solid block cursor blinks at the end of the
contact line like a terminal waiting for input, the status skeleton shimmers
while the first numbers load, and the dot beside a healthy system pulses gently;
every other status dot sits still. Every other movement happens because the
visitor scrolls or points. Hover follows one rule: amber things turn white and
white or grey things turn amber, a hover that changes a background or a border
takes a touch longer than one that changes a colour, and no hover transition
takes longer than a fifth of a second. Only two things change size on hover: the
main button lifts by a hair, and an uptime bar grows slightly taller from its
base. Nothing bounces and nothing loops quickly. When a reduced motion preference
is set, every loop and the entrance stop, and every scroll effect shows its
finished state.

**Palette by role.** The site is dark only; there is no light mode. The ground is
a near-black neutral, with the landing and status blocks one step warmer and a
near-black neutral at the foot of the page's light wash. One accent does the work
of a brand colour: a mid, vivid orange, a warm amber, used for every link, every
label that matters and every drawn accent stroke, and for nothing decorative. A
light, vivid orange is reserved for the hover of a solid amber fill. Sentences
are a near-white neutral; legal body text is a near-white warm neutral; ledes,
notes and the back pill label are a mid neutral; eyebrows and small labels are a
fainter mid neutral, which is raised to the brighter one wherever it is a link.
A word not yet revealed starts as a deep neutral. Status carries its own closed
set: operational is the amber itself, slow a lighter amber, degraded an amber
pushed toward red, down a light, soft red, and unknown the same deep neutral as
an unrevealed word. There is no box with its own colour: an edge is one hairline
of translucent white, and a raised surface is a wash of white at a very low
strength over the ground, never an opaque grey panel. The exact shades are yours,
so long as those roles and relationships hold.

**Type and shape.** Every sentence and heading is set in `Geist`, and so are the
underlined hero link and the legal back link. Every other label, number and link
is set in `Geist Mono`. Eyebrows, the hero meta line and foot, the back pill, the
arrow links (the four card links and the status notice link), the status tile
labels, card labels and pill are in capitals with wide tracking, and the card
number keeps its digits with the same wide tracking. The footer links, the teaser
and the mail link keep their written case with slight tracking; the contact line
keeps its written case with tight tracking; and the portal host inside the notice
link keeps its written case with no added tracking. Grotesk
headings are tracked tight. Numbers that change on the status board use figures
of equal width so neighbours never shift. Big display type stretches with the
window and small type never does; the sizes are in the front-end specification.
Buttons and pills are fully rounded; status cards, tiles and panels have soft,
generous corners; the uptime bars are barely rounded; the portrait is a circle.

**Density and layout.** Spacious on the story routes, with one proportional side
gutter that breathes with the window; a fixed, comfortable reading width on the
legal routes; comfortable on the status board and in the studio. The public site
has no menu bar. The studio has a top bar, and its inbox and record list are
card grids with side panels.

**Responsive.** The layout changes at four moments and adapts by itself
everywhere else. A little below the width of a small laptop window each
capability card puts its drawing below its text; at a slightly wider width the
founder page gains a second column for the portrait and swaps the small avatar
for the large portrait; at a phone width the headline stops being two placed
lines and wraps, and the uptime bars become fewer and wider. The status tiles
and card values fill rows by a minimum width and need no breakpoint of their
own. At a narrow viewport nothing scrolls sideways and every footer link stays
reachable. On a phone, the first screen and every pinned panel fill exactly
what is visible with the address bar showing, and the pinned sections keep
their timing when the bar hides.

## Front-end specification

### The chrome

Three things are everywhere. Behind everything sit a light wash of three faint
pools of warm light over the ground, a grid of dots that is present in the
middle of the window and gone well before the corners, and, on `/` and `/about`
only, a fine film of grain over the whole window. All three are drawn by the page
itself, never fetched as pictures, never intercept the pointer and never repaint
on scroll. The grain is generated noise composited so that it sits in the image
rather than on top of it, at a strength where it breaks banding and no more, and
it never shows colour. Where a browser cannot fade the dot grid, the grid is
hidden rather than shown to the edges; where it cannot blend the grain, the
grain is shown plainly and fainter.

The footer is a centred row of small mono links with a hairline above it. The
back pill is a small frosted rounded tab at the top left holding a breathing
amber dot, a left arrow and the word `Back`; the page shows softly through it,
and where frosting is unavailable its ground simply darkens. The back pill sits
above the grain, and the section glows sit behind their own section's content.
Selected text sits on the amber at two-thirds strength. The document's own
ground fills the overscroll area at the top and bottom, never white. Nothing
scrolls sideways on any route.

### Type sizes

The three widths the sizes below are measured at are windows `1440`, `990` and
`390` pixels wide, called wide, tablet-width and phone here. Body copy is `16px`
at all three. Mono labels come in three sizes, set by role and the same at every
width: `10px` for the status tile labels, the card value labels and the status
pill; `11px` for every eyebrow, the hero foot and the back pill; `12px` for the
hero meta line, the card number, the card and notice links, and the footer. The hero title is
`100.8px` on a wide window, `69.3px` on a tablet-width one and `32.76px` on a
phone, where it wraps as ordinary text; it has two lines on wider windows, the
second in the mid neutral, and each line is held on one line. The pinned
statement is `66.24px`, `45.54px` and `32px` at the same three widths, held to a
narrow measure of about twenty characters so it reads as short lines. A card
heading is `48px` on a wide window, and a card body is `23.04px` on a wide window
and `16.8px` below. The section heading `What we build` is `48px` on a wide
window. The contact line is set in the mono face at `70.4px`, `51.48px` and
`22.4px`. The hero lede is `18px` on a wide window and `16px` below. On the
status board the heading is up to `64px`, a system name is `19px`, a tile value
`26px`, a card value `16px` and a feedback heading `20px`. Legal body text is
`15px` with a `20px` clause heading, dropping to `14px` and `17px` on a phone. The
legal page heading is the tightest-tracked text on the site. Both families are
variable. Text appears at once in a fallback face measured to occupy the same
space, and the real face replaces it when it arrives without moving a line, so
the hero does not jump. Text is antialiased in
greyscale on every route, which keeps white text the same weight at every size.

### The controls

There are four interactive shapes. The primary button is a solid amber pill with
near-black text, at most one per page, which lifts by a hair and lightens on
hover. The underlined text link is a mid neutral sentence-case link that turns
white on hover. The mono arrow link is an amber capitals link followed by an
arrow, and link and arrow both turn white on hover. The pill is either the
interactive back pill or the non-interactive status pill, which carries a small
status dot and the status in words.

### The four home diagrams

Nothing on the site is a picture file except the portrait. Each diagram is a list
of rectangles, lines and circles drawn in the page, which is why it stays sharp
and can draw itself, and it is drawn in exactly this order. Structural strokes
are translucent white at a handful of strengths; strokes the diagram wants the
eye on are amber. Each carries a few mono words inside it, placed wherever reads
best.

- Card `02`, `Diagram: interface, API and workers over a Postgres database`: an
  amber box above two boxes and a fainter box beneath them, joined by four
  elbow lines, with a small amber dot in the top box. Words: `interface` in
  white, `api`, `workers` and `postgres` in the mid neutral.
- Card `03`, `Diagram: a browser window with Core Web Vitals scores`: a window
  frame with a title bar rule and three dots, three rounded bars standing in for
  text, an amber pill, and a progress track underneath whose first fifth is
  filled in amber at twice the track's stroke. Words: `LCP 0.6s` in amber, then
  `CLS 0.00` and `100 / 100` in the mid neutral.
- Card `04`, `Diagram: a server rack with encrypted uplinks`: a tall frame of six
  slots, the top slot amber and the rest fading downward, three status dots,
  brackets running off to each side, and a small amber padlock drawn as a body
  and a curved shackle. Words: `uplink` and `encrypted`.
- Card `05`, `Diagram: four interconnected nodes across Falkenstein, Frankfurt and Eygelshoven`:
  the widest drawing, four amber rounded squares at the corners of a square,
  the perimeter drawn as one continuous stroke, the two diagonals at a quarter of
  its strength, and an amber dot at each corner. Words: `FSN`, `FRA`, `EYG-1` and
  `EYG-2` near their nodes, with the city names `Falkenstein`, `Frankfurt`,
  `Eygelshoven` and `Eygelshoven` beside them in the fainter neutral.

A filled dot appears rather than draws; a shape that reports no length fades in
instead. Drawings may extend past their own box and are never clipped. The one
drawn icon is the arrow on the status notice link, two strokes of the link's own
colour.

### The pinned card

Each capability card is three windows tall with a one-window panel that holds
still; the four run back to back. The panel has its own opaque ground, a hairline
along its leading edge and a large soft shadow thrown upward, so the next card
slides over the one before it like a dealt card, with the outgoing card still
selectable text while it is being covered; nothing is stacked as moving layers.
The left side, very slightly the wider, holds a tag row with the two-digit amber
number and a small eyebrow, the heading, the revealed body at a comfortable
measure, and the arrow link; the right side holds the drawing. Below the card
collapse width the drawing moves below the text and the card keeps its timing.
The body starts revealing a little way into the hold and finishes with a little
over a fifth of the hold to spare; the philosophy statement starts a little
later into its longer hold and finishes with a seventh to spare. The numbering
runs through the whole page: the statement is `01`, the cards are `02` to `05`,
contact is `06`. Cards `02` to `04` carry the eyebrow `Capability` and card `05`
carries `Infrastructure`.

### The scroll behaviour

Wheel and keyboard scrolling are smoothed into a heavy, slightly delayed glide;
touch scrolling is left to the device. Native scrolling is never disabled and the
page is never moved by sliding a wrapper. Find-in-page, keyboard focus, anything
scrolling an element into view, back and forward navigation, dragging the
scrollbar, a resize, a rotation and a font arriving all move the smoothed
position and repaint the reveal for where the page lands. Words, drawings,
hairline and hero are painted together in one frame, and a dropped frame never
makes the reveal skip. The routes that smooth scrolling are `/`, `/about` and
`/uptime`; the legal routes use the browser's own scrolling, which glides for an
in-page jump. The status board does not reveal by scroll: its heading, lede,
tiles, cards, feedback and notice fade and rise into place once each as they
enter the window, including cards that arrive after the first paint. Only
paragraphs near the window are marked for animation, and the painted properties
carry no transition of their own.

### The home route in order

The hero fills the first screen. Its meta line is a small amber dot, `Vela Studio`,
a slash and `Marburg, DE`. The title reads `Software built in Germany.` then
`Hosted in Europe.`, the second line in the mid neutral. The lede reads
`We write production software and run it on our own machines. No US cloud providers. No black boxes. You own the stack.`
The actions are the button `Talk to an engineer` and the text link
`See what we build`. Along the foot, in small capitals, the three city names
`Frankfurt`, `Falkenstein` and `Eygelshoven` are separated by a middle dot with a
space either side, and on the right the word `Scroll` sits beside a short
vertical line fading downward. A soft pool of amber light sits behind the hero.

The philosophy section carries the eyebrow `01 - Philosophy`, a fainter amber
pool of light, the statement and its hairline:
`We build privacy-first software and infrastructure that stays honest: reliable, transparent, entirely yours, hosted in Europe, and never a black box.`
The words `reliable`, `transparent`, `entirely yours` and `never a black box`
reveal in amber, and the comma or full stop right after each of them lights up
as a step of its own.

The heading row reads `What we build` on the left and the eyebrow `Capabilities`
on the right, and carries the anchor `#leistungen`; the contact section carries
`#kontakt`.

The four cards:

| Number | Eyebrow | Heading | Body | Amber words | Link |
|---|---|---|---|---|---|
| `02` | `Capability` | `Software & Platforms` | `SaaS products, internal tools, APIs and the backends behind them. Built to be maintainable, documented on the way in, and handed over entirely yours - source, pipeline, runbook.` | `maintainable`, `entirely yours` | `Scope a build` |
| `03` | `Capability` | `High-performing websites` | `Marketing sites and web apps that load in under a second on real connections. Server-rendered, accessible, measured - no tracking scripts, no cookie theatre.` | `under a second`, `no tracking scripts` | `See a build` |
| `04` | `Capability` | `Managed hosting, privacy-first` | `Your workload runs on our own hardware in Europe - no hyperscaler underneath, no subprocessor you did not agree to. GDPR is the floor: encrypted at rest and in transit, patched and restored by the people who wrote it.` | `our own hardware`, `GDPR is the floor` | `See the stack` |
| `05` | `Infrastructure` | `Four nodes. One jurisdiction.` | `Falkenstein, Frankfurt and two sites in Eygelshoven. Our racks, our keys, interconnected in Europe. Frankfurt. Not Virginia.` | `Our racks, our keys` | `Status & uptime` |

The hyphen in each body stands for a long dash, which the build shows as a long
dash that reveals as a word of its own. Apostrophes throughout the copy are plain
straight apostrophes, exactly as written here.

The contact section fills most of a screen with a wide, low pool of amber light,
the eyebrow `06 - Contact`, and one line reading as a command prompt: an amber
chevron, the words `talk to an engineer_` in the mono face with the underscore
as part of the text, and a solid amber block cursor blinking after it. The
prompt line rests white and turns amber on hover. Beneath it the note
`Reply within one working day, from the person who would write the code.` and
the address `hello@vela.example.com` as an amber mail link, which turns white on
hover. Below the contact section the teaser is a single link in two rows:
`Curious who's actually behind the racks?` in the mid neutral, then
`(a real human)` in the fainter neutral beside an amber arrow that nudges
sideways; on hover the link turns white, the parenthetical turns amber and the
arrow stops. It is the only link on `/` to the founder page.

### The founder page in order

The back pill reads `Back`. The meta line reads `About`, a slash and
`Anton Ferber`. The title reads `Why I build` then `Vela Studio.`, and it wraps
within its column. The lede reads
`I'm Anton. I started Vela Studio because I was tired of handing people software they couldn't see into, running on infrastructure nobody in Europe controlled.`
The foot reads `Marburg`, a middle dot and `Germany` on the left, and `Scroll` on
the right. On a wide window the round portrait sits in the right column inside
its halo and long shadow; below that width a small round avatar sits above the
text instead, and only one of the two is ever shown. The portrait rises into
place a moment after the text.

Statement `01 - The craft`:
`I build software the way I'd want it built for me: owned outright, documented, and running on hardware I can point to - not rented from a hyperscaler an ocean away.`
Amber words: `owned outright`, `documented`, `hardware I can point to`.

Statement `02 - The principle`:
`Privacy isn't a feature I bolt on at the end. It's the starting condition. Your data stays in Europe, on machines I maintain, answerable to you - never a black box.`
Amber words: `the starting condition`, `answerable to you`.

The contact section carries the eyebrow `03 - Elsewhere`, the prompt `about me_`,
the note `More of what I make, write and tinker with lives on my personal site.`
and the link `anton-ferber.example.com`. The prompt line behaves exactly as the
home page's does, resting white and turning amber on hover, while the link under
it is white and turns amber, the opposite end of the rule from the home page's
amber mail link, which turns white.

### The status board in order

The back pill reads `Back`. The eyebrow `System status` is amber here, because on
this page it names a state rather than a section. The heading reads
`Live reliability, shown in public.` and the lede reads
`Every Vela Studio system, monitored continuously. This page updates automatically - no login required.`
The tile labels are `Systems`, `Operational`, `Average uptime` and `Next check`;
the card labels are `Uptime`, `Response time`, `Last checked` and
`Last status change`; the status words are `Operational`, `Slow`, `Degraded`,
`Down` and `Unknown`. Times read like `1 Sept 2026, 15:38`. Each bar's `title` attribute reads
`<status word> at <time>`, for example `Operational at 1 Sept 2026, 15:38`, and each
strip carries the `aria-label` `Recent uptime history for <system name>`. The skeleton is
three placeholder cards with two shimmering lines and a row of shimmering bars
whose shimmer travels along the row.

The failure block reads `Status temporarily unavailable` over
`The live status feed could not be loaded right now.` and the feed's own message,
or `The uptime feed is unavailable.` when it gave none. The empty block reads
`No systems available` over `No monitored systems are currently visible.` and
`The monitoring feed returned an empty project scope.` Both are announced.

The seven systems, in `position` order:

| Position | Name | Slug |
|---|---|---|
| `1` | `Vela Studio` | `vela-studio` |
| `2` | `Vela Studio Finance` | `vela-studio-finance` |
| `3` | `Vela Studio Analytics` | `vela-studio-analytics` |
| `4` | `Vela Studio Console` | `vela-studio-console` |
| `5` | `Vela Studio DB Controller` | `vela-studio-db-controller` |
| `6` | `Vela Studio Tickets` | `vela-studio-tickets` |
| `7` | `Anton Ferber Portfolio` | `anton-ferber-portfolio` |

The notice block closes the page:
`Looking for incident history, deeper diagnostics, or want to open a ticket? Full detail lives in the customer portal.`
followed by the link `Open customer portal` holding the host
`portal.vela.example.com` in the fainter neutral and the drawn arrow; it opens in
a new tab and passes no referrer.

### The legal documents

Both pages carry the back link `Back to Vela Studio`, an amber eyebrow and a large
heading. `/impressum` carries the eyebrow `LEGAL NOTICE`, the heading
`Information pursuant to § 5 DDG`, and nine blocks: `Provider`, reading
`Vela Studio`, `Anton Ferber`, `Ketzerbach 21`, `35037 Marburg` and `Germany`, one
line each; `Contact`, reading `Phone:` with `+49 6421 555 0142` as a link,
`Email:` with `hello@vela.example.com` as a link, and `WhatsApp Business:` with
the same number as a link; `Registered office`, the address again; `VAT`, reading
`VAT identification number: DE123456789`; `Responsible for content`, the founder
and the address; `Liability for content`; `Liability for links`; and `Copyright`.
German legal terms inside the English text are marked as German. `/agb` carries
the eyebrow `TERMS`, the heading `General Terms and Conditions`, and eight
numbered clauses: `1. Scope`, `2. Services`, `3. Client cooperation`,
`4. Fees and payment`, `5. Operations and availability`, `6. Rights of use`,
`7. Liability` and `8. Final provisions`. Clause 5 says, in the studio's own
words, that the site's claims about availability, resilience, performance, data
protection and hosting location describe the technical approach rather than a
guaranteed service level. The wording of the remaining clauses is the studio's
to write, stating the substance each heading names.

### The build library, the composer and the studio

The library, the composer, the account page and the studio use the same ground,
type and controls as the rest of the site. The library heading is `Builds`; its
filter labels read `All`, `Software & Platforms`, `High-performing websites` and
`Managed hosting, privacy-first`. The composer's capability choices are three
checkboxes named `capabilities`, with the values `software`, `website` and
`hosting`, carrying those three labels; the posture choices read `We run it on our racks` for `managed` and
`Hand it over to run yourself` for `handover`; the residency choices read
`Anywhere in the EU` for `eu` and `Germany only` for `de`; the timeline choices
read `Flexible`, `Standard` and `Accelerated`; the budget choices read
`Under EUR 10,000`, `EUR 10,000 to 25,000`, `EUR 25,000 to 60,000` and
`Over EUR 60,000`. The figure is labelled `Indicative figure`, and the send
button reads `Send build request`, which is the page's one primary action. The
form controls are named exactly as the API fields: `capabilities`, `posture`,
`residency`, `timeline`, `budget_band`, `description`, `contact_name`,
`contact_email`, `contact_fax`, `rules_version`, `indicative_minor` and
`attachment`. The account page is headed `Your build requests`. The studio top
bar, the card grids and the side panels are quiet and comfortable, with the
amber reserved for the one action in each panel.

### Metadata and sharing

Every public route carries its own title and its own description, and no two
routes share either. The titles:

- `/`: `Vela Studio | Software Made in Germany, Hosted in Europe`
- `/about`: `About | Vela Studio`
- `/uptime`: `System Status | Vela Studio`
- `/impressum`: `Legal Notice | Vela Studio`
- `/agb`: `Terms & Conditions | Vela Studio`
- `/builds`: `Builds | Vela Studio`
- `/build-request`: `Build request | Vela Studio`

The home description reads
`Software and websites made in Germany, hosted in Europe on privacy-first infrastructure with a 4-node European cluster, monitoring, backups, recovery workflows, and DSGVO-conscious operations.`
Every public route also declares a canonical address and a social card with a
large preview image that resolves. The preview image is generated from the
site's own ground, wash, wordmark, one amber dot and tagline, never drawn by
hand, and its alternative text reads `Vela Studio - Software that scales`. The
site's name in the document head is `Vela Studio`, its category is
`Software development`, and pages may be indexed and followed. The document head
carries no keyword list.

### Module and component architecture

The site is three shells sharing one footer and one set of design tokens, and
nothing else. The story shell, on `/` and `/about`, holds the grain, the back
pill where it appears, the hero, the pinned statement with its hairline, the
capability card with its diagram slot, the contact block and the teaser. The
status shell, on `/uptime`, holds the back pill, the board with its tiles, cards,
states and timers, and the enter reveal. The document shell, on `/impressum` and
`/agb`, holds the back link, the eyebrow, the heading and the clause list. The
scroll reveal adds nothing visible of its own: it works from what the finished
page already contains, the revealed paragraphs, the pinned sections, the drawn
shapes, the hairlines, the hero block and the in-page links. The smoothed
scrolling, the grain and the two reveal behaviours belong to their own shell and
never appear on a route whose shell does not carry them. On the public routes
nothing about the visitor is remembered from one page to the next.

### Zero-asset substitution

No design file and no image asset ships except the uploaded portrait. The grain
is noise the page generates; the pools of light are gradients; the dot grid is
two hairline patterns crossed and faded out; the four diagrams and every build
record diagram are shape lists; every dot, bar and rule is a plain shape. The
portrait stand-in is drawn in the page: the ground, a soft amber glow, an open
amber arc of light wrapping part of the circle, and a soft dark silhouette in
its lower part, clipped to a circle, never a face, and named
`Portrait placeholder` so nobody ships it by mistake. The social card and the
square tile image are generated at build time from the site's own tokens, so
they change when the tokens change.

### What is deliberately not built

None of these is built: a header menu, a comparison table, a
questions-and-answers block, a large multi-column footer, an animated map, a
founder-notes panel, or any animation belonging to them.

## Technical requirements

The studio's pages are rendered by `Flask` through `Jinja` templates, and
`Alpine.js` adds behaviour on top of that finished markup; with scripts off, each
page still reads in full. The same `Flask` app serves the JSON API under `/api`
on the site's own origin. The scroll reveal, the status
board client and the composer are the app's own code; no animation or smoothing
library is added.

Records for accounts, systems, checks, incidents, incident entries, build
records, measurements, build requests, attachments, page views and portraits go
into `PostgreSQL`, found at `DATABASE_URL`. Every attached brief and the portrait
are kept as objects in `minio`. The app reaches that store at
`STORAGE_ENDPOINT`, signs with `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`, and
writes into the bucket named by `STORAGE_BUCKET`. That bucket already exists and is not readable without
those credentials, and the app never changes that. Accounts sign in with an email
and a password the app itself checks; passwords are stored hashed, and a
successful sign-in or signup returns the account and an `access_token`, which
the client sends as a bearer token. Once the app is ready to serve,
`GET /api/health` answers `200`. Each request the server handles writes a single
line to stdout.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor - the only backing services available in this environment are
`PostgreSQL` and `minio`, and reaching for anything else is a contract violation.
Hosts, ports, keys and passwords all come from environment variables, and none is
written into the code.

**Three shells.** `/` and `/about` load the scroll reveal, the grain and the
pinned sections. `/uptime` loads the smoothed scrolling, the enter reveal and the
feed client, and no grain. `/impressum` and `/agb` load no script at all, so a
legal page never downloads the scroll reveal.

**The feed and the board.** The board fetches with the browser cache bypassed,
refreshes every thirty seconds only while the tab is visible, never overlaps two
refreshes, and applies new values without blocking input. The countdown ticking
each second never disturbs the cards: a card being read or pointed at does not
flicker, lose its hover or jump. The feed is servable from a short-lived cache and
needs no session.

**Budgets on a cold cache at a wide window.** The document and the critical
stylesheet each stay small; no script runs before first paint on the legal
routes and very little elsewhere; the scroll reveal is deferred; each font family
loads one Latin subset at first paint; the uploaded portrait is the only
photograph, shown with its dimensions declared so nothing moves when it arrives,
and the social card and tile images are generated rather than drawn; the largest
paint on a mid-range
connection lands well within a second and a quarter; and content shifts after it
appears by almost nothing.

**Scrolling stays smooth.** The words and the drawing on one screen never drift
apart from each other, a slow frame never makes the reveal jump or skip, and a
long page of revealed paragraphs scrolls as smoothly at the bottom as at the top.
A hover or a style change elsewhere on the page never fights the reveal.

**Write contracts are protected by network, not identity.** The build request and
the page-view record are the only anonymous writes. The site holds no visitor
identity, so repeat refusal works from the network address in memory and never
from a stored identifier, a cookie or browser storage.

**Nothing the browser downloads carries a credential.** No storage secret,
database password or bearer token belonging to anybody but the viewer appears in
any document, script, stylesheet or source map.

## Data model

Eleven tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account so
a grader can sign in.

**accounts.** An id, an `email` unique without regard to case, a password hash, a
`role` that is `founder` or `client`, and a creation time.

**systems.** An id, a unique `slug`, a `name`, a unique `position` that fixes the
board's order, `interval_seconds`, `open_after`, `close_after`, and a creation
time. A system created later takes the next position after the last.

**checks.** An id, the owning system, `checked_at`, a `status` that is `up`,
`slow`, `degraded` or `down`, `response_ms` that is a non-negative whole number or
null, and a creation time. A system holds at most one check for a given
`checked_at`. `unknown` is never stored: unknown slots, `uptimePercent`,
`currentStatus`, `lastStatusChangeAt` and `nextCheckAt` are derived on read.

**incidents.** An id, a unique `ref`, the owning system, `opened_at`, and a
`resolved_at` that is null while the incident is open. Incidents are derived from
the checks under the thresholds of their system.

**incident_entries.** An id, the owning incident, the owning system, a `seq`
unique within the system, a `kind` that is `opened`, `note` or `resolved`, a
`body`, and `recorded_at`. Rows are only ever added.

**build_records.** An id, a unique `slug`, a `title`, a `capability` that is
`software`, `website` or `hosting`, a `summary`, a `body`, a `stack` as an ordered
list of names, `started_on` and `delivered_on` dates, a `client_name`, a
`client_visible` flag, a `diagram` as an ordered list of primitives, a `published`
flag, a `published_at` that is null while unpublished, and a creation time.

**measurements.** An id, the owning build record, a `metric` that is `lcp_ms`,
`cls`, `p95_api_ms` or `uptime_percent`, a numeric `value`, a `measured_on` date
and a `source`.

**build_requests.** An id, a unique `reference`, the submitting account or null,
`contact_name`, `contact_email`, `capabilities` as an ordered list, `posture`,
`residency`, `timeline`, `budget_band`, `description`, `rules_version`,
`indicative_minor` in integer euro cents, `currency`, a `status` that is `new`,
`reviewing`, `quoted`, `accepted` or `declined`, a creation time and
`status_changed_at`. No column holds a network address, a browser signature or a
cookie value.

**attachments.** An id, the owning request, a unique `object_key`, a
`content_type` that is `application/pdf`, `image/png` or `image/jpeg`, a
`byte_size`, the `sha256` of the bytes, the `original_name`, and a creation time.
A request owns at most one.

**page_views.** An id, the `route`, and `viewed_at`. Nothing else.

**portraits.** An id, an `object_key`, a `content_type`, and `uploaded_at`. The
newest row is the portrait shown.

**Invariants, as properties of the running system.**

- A request and its attachment are readable by the founder and by the owning
  client only, and the stored object is readable by nobody without the storage
  credentials.
- A stored figure always equals the rule table computation for its stored
  version, and a mismatch or a retired version is refused before anything is
  written.
- References are unique and increase within a year.
- Sending the same check twice leaves one row; an unknown slot is never counted
  as up and never counted at all in `uptimePercent`.
- A flapping system produces one incident, and replaying its checks produces the
  same `ref` values and no new entry. Entry `seq` values rise by one within a
  system and existing entries never change.
- An unpublished build record is absent from every public read, and is never a
  capability link's target.
- A refused write writes nothing at all: no row, no partial row, no object.

**Seed data.** Three accounts, as listed in `## User roles`. Seven systems, in
the order the status board lists them, with an interval of `300`, `open_after`
`3` and `close_after` `2`. The first five each hold twelve `up` checks five
minutes apart, the last at first start, each with a `response_ms` of `48`.
`Vela Studio Tickets` spans the same twelve slots but holds ten `up` checks at
`48`, with the seventh and eighth slots missed, so its bars show two unknown
slots. `Anton Ferber Portfolio` holds no check at all. `Vela Studio Console`
also holds the checks behind its seeded incident, at `14:15` up, `14:20`, `14:25`
and `14:30` down, `14:35` and `14:40` up on `2026-09-01`, and the incident
`vela-studio-console-20260901-1420` with its three entries. Four build records:
`harbour-ledger`, `Harbour Ledger`, `software`, started `2026-02-02`, delivered
`2026-06-30`, client `Lahnhafen Logistik` shown, stack `Python` and `PostgreSQL`,
one measurement `p95_api_ms` `180` measured `2026-07-14`; `kestrel-storefront`,
`Kestrel Storefront`, `website`, started `2026-05-11`, delivered `2026-08-12`,
client `Kestrel Outdoor` shown, stack `Python` and `Alpine.js`, measurements
`lcp_ms` `640` and `cls` `0.01` measured `2026-08-20`; `lahn-clinic-hosting`,
`Lahn Clinic Hosting`, `hosting`, started `2026-03-16`, delivered `2026-05-02`,
client withheld, stack `PostgreSQL`, no measurement; all three published. And
`aurora-payroll-portal`, `Aurora Payroll Portal`, `software`, started
`2026-07-01`, delivered `2026-09-05`, client `Aurora Personal` shown, not
published. Every record carries a one-sentence summary, a short body and a
diagram of at least four primitives. Two build requests,
both on rule table `2026-09`: `VS-2026-0001` from `client@example.com`,
`software`, `handover`, `de`, `standard`, `25k-60k`, figure `1450000`, status
`reviewing`, with an attached PDF brief named `billing-brief.pdf` stored in the
bucket under `requests/VS-2026-0001/`; and `VS-2026-0002`
from `client2@example.com`, `website`, `managed`, `eu`, `flexible`, `under-10k`,
figure `550000`, status `new`, with no attachment. No page view and no portrait
are seeded.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- One studio and one founder. There is no organisation, no team and no second
  tenant.
- No incident email subscriptions. There is no mail service in this environment,
  and the board says nothing about subscribing.
- No field performance collection from visitors. The figures on a build record
  are measurements the founder entered with their dates.
- One language, English. There is no locale switch; German legal terms are marked
  inside the English text.
- No third-party scheduling page and no external booking link. A build starts
  with the build request.
- No payment, no checkout, no comment, no chat, no newsletter, no search box, no
  menu bar on public routes, and no cookie banner, because nothing asks for
  consent.
- No cookie, no analytics, no tag manager, no external font and no call to any
  other origin at run time.
- No bitmap ships except the portrait the founder uploads. The grain, the glows,
  the grid, the diagrams, every dot and bar, and the social card are generated.
- The few words inside the four home diagrams, and the exact start of the
  three multi-word amber phrases, are placed wherever reads best within what
  this brief states. The four unhealthy statuses behave as the Core features
  rules on checks and incidents define.
- The product must stay responsive with the seeded content and with a few
  thousand checks, requests and page-view rows.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and
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
| `POST /api/auth/signup` | `email`, `password` | the created `client` account and an `access_token` |
| `POST /api/auth/login` | `email`, `password` | the account, with its `role`, and an `access_token` |
| `GET /api/health` | none | a health object |
| `GET /api/uptime/projects` | none | the status envelope described in Core features |
| `GET /api/uptime/incidents` | none | a top-level array of incidents, newest first, each with `ref`, `system`, `opened_at` and `resolved_at` |
| `GET /api/uptime/incidents/{ref}` | none | one incident with its `entries`, each carrying `seq`, `kind`, `body` and `recorded_at` |
| `POST /api/uptime/incidents/{ref}/notes` | `body` | the appended entry; `founder` only |
| `POST /api/systems` | `slug`, `name`, optional `interval_seconds`, `open_after`, `close_after` | the created system; `founder` only |
| `POST /api/systems/{slug}/checks` | `checked_at`, `status`, `response_ms` | the recorded check; `founder` only |
| `GET /api/builds` | optional `capability` | a top-level array of published records, newest delivery first |
| `GET /api/builds/{slug}` | none | one published record with its `measurements` and `diagram` |
| `GET /api/studio/builds` | none | a top-level array of every record, published or not; `founder` only |
| `POST /api/builds` | `slug`, `title`, `capability`, `summary`, `body`, `stack`, `started_on`, `delivered_on`, `client_name`, `client_visible`, `diagram` | the created record, unpublished; `founder` only |
| `POST /api/builds/{slug}/publish` | none | the published record; `founder` only |
| `POST /api/builds/{slug}/unpublish` | none | the unpublished record; `founder` only |
| `POST /api/builds/{slug}/measurements` | `metric`, `value`, `measured_on`, `source` | the created measurement; `founder` only |
| `GET /api/pricing-rules` | none | the current rule table with its `version` |
| `GET /api/pricing-rules/{version}` | none | that rule table |
| `POST /api/build-requests` | a JSON body, or a multipart form with an optional file part `attachment`, carrying `capabilities`, `posture`, `residency`, `timeline`, `budget_band`, `description`, `contact_name`, `contact_email`, `rules_version`, `indicative_minor` and `contact_fax` | the created request with `reference`, `status`, `indicative_minor`, `currency` and `rules_version`; a signed-in `client` becomes its owner |
| `GET /api/build-requests` | none | a top-level array of every request, newest first; `founder` only |
| `GET /api/build-requests/mine` | none | a top-level array of the caller's own requests; `client` only |
| `GET /api/build-requests/{reference}` | none | one request with its `attachment`; the `founder` or the owning `client` only |
| `GET /api/build-requests/{reference}/attachment` | none | the attached bytes, or a link to them; the `founder` or the owning `client` only |
| `POST /api/build-requests/{reference}/status` | `status` | the updated request; `founder` only |
| `POST /api/studio/portrait` | the image as file part `portrait` | the stored portrait with its `object_key`; `founder` only |
| `GET /api/portrait` | none | the portrait bytes, or not-found when none exists |
| `POST /api/page-views` | `route` | the recorded view |
| `GET /api/page-views` | none | a top-level array of views, newest first; `founder` only |
| `POST /build-request` | the composer's form fields | the rendered summary page headed `Request received` |

Field names are exact. Apart from the status envelope, a list endpoint returns a
top-level JSON array. A successful call returns the named resource or shape; an
invalid or unauthorized call is rejected as a client error, never as a server
error and never as a silent success, and an invalid one names the field at
fault. Bearer authentication is required on everything except signup, login,
health, the public reads, the build request, the page-view record and the
portrait read.

### No mocks

`minio` is where the bytes live. An in-memory buffer the app hands back to
itself, a file written to the app container's own filesystem, a base64 column in
`PostgreSQL`, a bucket opened to anonymous reads, or a stored object key pointing
at nothing are each a contract violation however good the upload looks. The
status board's numbers come from recorded checks, never from values typed into a
template, and the indicative figure comes from the rule table on the server,
never from whatever the page sent. The named provider is the fact: the app's UI
and its own tables can only reflect what lives in the provider, never substitute
for it.

## Definition of done

A stranger describes a build, sends it with an attached brief, and receives a
reference number and an indicative figure that the server computed the same way,
with scripts running or switched off. The attached brief lives in the `minio`
bucket at its scheme's key, and nobody but the studio and the client who sent it
can read the request or its brief.
