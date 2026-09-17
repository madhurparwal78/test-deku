# Verdigris Studio

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser, read a published case study, filter
the project archive down to one service and share that filtered view by its address, read what an
engagement costs, and then sign in and book a strategic call in the studio calendar, landing on a
confirmed call with a quotable reference and one confirmation message waiting in the studio's mail
server, without hitting an error page. A second stranger racing for the same slot at the same moment
must NOT also end up with a confirmed call, by any means, including a direct request to the booking
endpoint. The confirmation must exist as a real message in `mailpit`, addressed to that one account;
a success banner the app shows itself does not count.

## Overview

Verdigris Studio is a brand design studio that sells design and website engagements to founders in
four consumer verticals: beauty, wellness, food and lifestyle. The site is the studio's own proof.
It argues who the studio is for, shows the work, explains a named method, prices three packaged
engagements in the open, and closes on one action.

That action is booking a strategic call. The studio owns the calendar rather than sending a visitor
to somebody else's scheduling page, because the moment a visitor decides to talk is the moment the
site can least afford to hand them away. A visitor chooses a slot, the slot is held while they
answer two short questions, and confirming writes the booking and sends one message. The second
action that changes stored state is the enquiry form, which carries a project type, a budget band
and a consent checkbox, and which the studio answers inside a stated promise.

Everything else is reading. Twelve published projects, eight services, three packages, a four step
method, an awards wall, a founder story and a manifesto, all rendered from records rather than typed
into pages, so that a project tagged once carries the same tags in the archive, on the home route
and under the service that produced it.

It is deliberately not an application. There is no cart, no payment surface, no plan ladder and no
subscription. There are no comments, no likes and no messaging. There is no general purpose content
management: only the studio's own collections are editable, and only by the studio. Nothing on the
site is personalised to a visitor.

The genuinely hard part is that one calendar slot can be chosen by two people inside the same second,
and only one of them may end up with a call.

## User roles

| Role | Can do |
|---|---|
| Anonymous visitor | Read every published route: the home route, the offers, the expertise tree, the archive and its filters, a case study, the method, the about route, the privacy page. Submit the enquiry form. View the slot calendar. **Cannot hold or confirm a slot, cannot see anyone's bookings, cannot reach the console.** |
| `client` | Everything a visitor can do, plus: hold a slot, confirm the call, read and cancel their own calls. **Cannot see another client's booking or its reference, cannot open or close a slot, cannot read an enquiry, cannot publish or reorder anything.** |
| `studio` | Everything a visitor can do, plus the console: open and close calendar slots, read every enquiry and record a first response, publish and unpublish projects, set editorial order. **Cannot confirm a call on a client's behalf and cannot read a client's password.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `client` session to any `studio`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged. The same holds between two `client` sessions: one client requesting another client's
booking by its own reference is denied, and the booking is unchanged.

Signup is open and creates a `client`. A `studio` account cannot be created through signup and
exists only because it is seeded.

Seeded accounts, all three using the password `deku-demo-pw-2026`:

| Email | Role |
|---|---|
| `studio@example.com` | `studio` |
| `client@example.com` | `client` |
| `client2@example.com` | `client` |

## Core features

### Auth and accounts

Email and password, implemented by the app. A successful login returns a bearer token the client
sends as `Authorization: Bearer <token>` on every request except login, signup and health. Passwords
are stored hashed and never returned by any endpoint. A token lasts 24 hours and a request carrying
an expired one is rejected as unauthorized.

1. Signup takes an email and a password and creates a `client`. An email already in use is rejected
   as invalid, with the email field named, and no second account is created.
2. Signup may never create a `studio` account, whatever the request body carries. A request asking
   for one is rejected and the account, if it is created at all, is a `client`.
3. A login with a wrong password is rejected as unauthorized and returns no token and no hint about
   whether the email exists.

### The site shell and its pages

Every public route carries the same shell: a header with the wordmark at the left and a single
navigation control at the right, the route's own content, a booking block, then the footer. The
footer repeats the whole navigation graph in plain view: the six primary destinations, the eight
services, the studio sentence, the legal links and the directory rating badge.

1. The booking block is the last block before the footer on every public route without exception. It
   carries an eyebrow, a headline, the primary action into the calendar, and the response promise
   line reading `reply within 24 hours`.
2. The navigation control opens a panel covering the viewport, listing the six primary destinations
   with the eight services nested beneath them, plus the booking action. While the panel is open the
   route beneath it does not scroll, focus stays inside the panel, and closing it returns focus to
   the control that opened it.
3. Every internal link on every public route resolves to a real route of this app. An internal link
   that would lead nowhere is a defect, including a link to a project or a service whose slug has
   changed.
4. An unknown address renders the studio's own not-found page, carrying the same shell, the booking
   block and a link back into the archive, and the response says the address was not found rather
   than succeeding with an empty page.
5. `/privacy` is reachable from the footer of every route and states what the studio stores about a
   visitor who enquires or books, and for how long.

### The project archive

`/projects` lists every published project in stored editorial order, three across at the widest
layout. Each card is a generated image, the client name set in capitals, and a service line joining
the project's tags with a spaced hyphen, for example
`Visual identity - Art direction - Web development`.

1. Nine controls sit above the grid: the eight services plus an `All` control that is a control
   rather than a tag. Choosing one narrows the grid to projects carrying that service.
2. Filtering never reloads the page, and the chosen filter is reflected in the address so that a
   filtered view can be shared and opened again. Opening that address directly shows the same
   filtered grid.
3. Filtering leaves the scroll position where it was and announces the resulting count to assistive
   technology.
4. A card that has been revealed once stays revealed for the life of the page, however many times it
   is filtered out and back in. A card re-entering the grid never plays its reveal a second time.
5. A filter matching no published project shows an empty state naming the service and offering the
   `All` control, never a blank grid.
6. Unpublished projects never appear in the archive, are not counted in the announced count, and a
   direct request for an unpublished project's route is answered as not found rather than rendered.
7. A project carries between one and six tags. The longest service line wraps rather than being
   clipped at any layout.

### The case study

`/projects/<slug>` renders one published project: a lower case eyebrow naming the deliverable, the
client name as the headline, the same hyphen joined tag line the archive card uses, a summary of two
to four sentences, an outbound action, then the media sequence, then related work, then the booking
block.

1. The outbound action carries the client site's host name as its visible label, opens in a new
   context, and declares its relationship to this site so that it does not pass the visitor's
   referrer on.
2. The media sequence is an ordered list of entries, each with a layout hint of `full` or `half`, and
   renders in stored order. It is a record, not a block of markup typed into the page.
3. Every media entry carries alternative text written for it. A media entry saved without alternative
   text is rejected as invalid and nothing is written.
4. Related work shows other published projects sharing at least one service with this one, most
   recently published first, and never shows the project itself.

### The expertise tree

`/expertise` lists the eight services in stored index order, each with an index title, then a line
beginning with a dash describing what the service is, then a second dashed line naming what it gets
the client. `/expertise/<slug>` argues one service at length and lists the published
projects tagged with it.

1. The eight services are one vocabulary in one place. The same rows are the expertise index, the
   tags under an archive card, and the archive's filter controls. A service renamed once is renamed
   everywhere, and no page carries a ninth tag that no service defines.
2. A service's own route lists the projects tagged with it in the same editorial order the archive
   uses, and the count it shows matches the count the archive shows when filtered to that service.

### The offers

`/offers` carries the three packages in a row: `Opening Note`, `Full Measure` and `Open Shelf`, in
that order, each with a category word above the name, a one line promise, a fit paragraph, a price
floor and an accordion of four panels.

1. Prices are floors and are stored as integer minor units in `usd`. `Opening Note` is `350000`,
   `Full Measure` is `750000`, `Open Shelf` is `1200000`. `$3,500.00` is `350000`, not `3500`, not
   `3500.00`.
2. Every rendered price carries a from label and a tax status, on every surface that shows one. The
   rendered form is `From $3,500 plus tax`. A price rendered without both reads as a quote and is a
   defect.
3. Exactly one package is the recommended one. `Full Measure` carries a badge reading `Recommended`
   at the top edge of its card. A second recommended package is refused on save.
4. The four accordion panels are in fixed order with fixed labels: `Who the package suits`,
   `What the package contains`, `What the studio delivers`, `What can be added`.
5. `Who the package suits` carries two lists: a qualifying list and a disqualifying list. Each disqualifying
   entry may name another package as the remedy, and where it does, the name is a link to that
   package. The disqualifying list is the point of the page and is never omitted.
6. Panels are closed at first paint, are individually operable, expose whether they are expanded, and
   do not close each other. Their content is present in the document at first paint rather than
   fetched when a panel opens.

### The method

`/method` explains the studio's named method. The name is `Throughline(TM)` and it carries its mark
every time it appears, on every route that names it.

1. The route carries a promise of three sentences, four numbered steps in stored order, each with a
   title and a description, and two lists: who the method is for and who it is not for.
   Trademark handling is uniform: the mark is part of the stored name, it renders at every
   occurrence on every route including inside a headline, and it is never dropped to tidy a line.
2. The four step titles are `Diagnostic`, `Art direction`, `Digital experience` and `Brand
   alignment`, in that order.
3. The method is referenced from the home route and from the third differentiator on the about
   route, and both render from the one method record rather than repeating its words.

### Proof: awards, the delivered count and the directory badge

1. The awards wall is three rows, one per year, each carrying the year, the entity name as it was
   submitted and the distinction: `2023` `Vare Studio` `Honourable Mention`, `2024`
   `Verdigris Studio` `Nominee`, `2025` `Verdigris Studio` `Nominee`. The earliest row carries a
   different entity name from the later two and that difference is preserved rather than tidied.
2. The awards wall renders on both the home route and the about route from the one record. Changing
   a row changes both.
3. The proof band carries the delivered project count, `148`, and one line of range, and appears on
   the home route, the archive and the about route. It is a stored field, not a string typed into
   three templates.
4. The directory rating badge carries a score of `4.3`, a scale of `5`, the verdict `Very good`, the
   source `Studio Index` and a review count of `4`. Its accessible name spells all five out in one
   sentence.

### Booking a strategic call

`/book` renders the studio calendar as a grid of slots. Every slot is 30 minutes. A slot is
choosable when it is open and nothing live holds it; a slot that is taken or closed is visible and
is not choosable. Choosing a slot places a hold that lasts 8 minutes, and the remaining time counts
down in place. The booking then runs as three addressed steps, so that moving back a step never
drops the hold and the step a visitor is on is legible from the address:
`/book/hold/<reference>` asks for the sector and a one line topic, `/book/confirm/<reference>` shows
the slot back and confirms it, and `/book/done/<reference>` shows the confirmed call.

1. **A slot holds at most one booking that is `held` or `confirmed`. Two simultaneous requests to
   hold the same slot must not both succeed: exactly one wins, and the other is rejected with a
   stated reason. This must hold at the database level, not only in application logic.** The loser
   sees the three nearest open slots offered in place and never sees a confirmation.
2. A rejected attempt leaves no partial state: no `held` row for the loser, no orphaned reference,
   and the winner's booking is untouched.
3. A hold whose 8 minutes have passed is no longer live. The slot is choosable again by anybody, and
   the abandoned page says so in place at its next interaction rather than only after a reload.
   Confirming an expired hold is rejected and creates no booking.
4. Holding a slot requires a signed-in `client`. An anonymous visitor choosing a slot is sent to sign
   in and is returned to the same slot afterwards.
5. Confirming writes the booking as `confirmed` and sends exactly one message over SMTP at
   `SMTP_HOST` and `SMTP_PORT`. Its subject begins `Call confirmed:` followed by a space and the slot
   start rendered as `YYYY-MM-DD HH:MM UTC`, for example
   `Call confirmed: 2026-09-18 09:00 UTC`. It is addressed to the booking account's own email, with
   no cc and no bcc, and its body names the studio, the slot and the booking reference.
6. No other transition sends a message. Placing a hold sends nothing, a hold expiring sends nothing,
   a cancellation sends nothing, and submitting the enquiry form sends nothing.
7. A booking reference is the letters `vs-` followed by twelve lowercase hexadecimal characters, for
   example `vs-7f3a9c1d4e20`. It is unguessable and it is the only handle the client is shown.
8. A client may cancel their own confirmed call. Cancelling sets the booking to `cancelled` and
   returns the slot to the grid as choosable. A client cancelling another client's booking is denied
   and that booking is unchanged.
9. The sector must be one of `beauty`, `wellness`, `food` or `lifestyle`, and the topic must not be
   empty. An invalid step is rejected inline with the field named, the hold keeps running, and
   nothing is written.

### The enquiry

`/contact` offers two ways to start, in this order: write to the studio, or book a slot directly. The
written path is a form of eight fields and a consent control, in this order: surname, first name,
telephone, electronic mail, project type, budget, how can we help, how did you hear of us, consent.

1. Surname, first name, electronic mail and consent are required. Project type is one of `Launch` or
   `Redesign`. Budget is one of `Under $5,000`, `$5,000 to $10,000`, `Over $10,000` or
   `Not sure yet`.
2. Validation is enforced on the server and that is the only validation that counts. An invalid
   submission is rejected as invalid, names every offending field inline, keeps everything already
   typed, and writes no enquiry row at all.
3. The consent control is never checked by default. A submission without it is rejected as invalid.
   A valid submission stores the moment consent was given alongside the enquiry.
4. A valid submission stores the enquiry, computes when a reply is due as the moment it arrived plus
   the studio's promise of 24 hours, and shows the visitor a reference of the letters `vq-` followed
   by twelve lowercase hexadecimal characters, for example `vq-4c81be09fa37`.
5. The route states the reply promise, and the footer states it again. Both read from the one stored
   promise rather than repeating the number.

### The studio console

`/studio` is the owner's console and is reachable only by the `studio` account.

1. `/studio/slots` lists the calendar and opens or closes a slot. Closing a slot that carries a
   `confirmed` booking is rejected with a stated reason and the slot stays open. Opening a slot whose
   start time already exists is rejected as invalid.
2. `/studio/enquiries` lists every enquiry, newest first, with its reference, its budget band, when a
   reply is due and whether one has been recorded. Recording a first response stores the moment and
   the row then shows it. A second recording does not move the stored moment.
3. `/studio/projects` publishes and unpublishes a project and sets editorial order. Publishing a
   project whose media carries no alternative text is rejected with a stated reason and the project
   stays unpublished.
4. Every console endpoint is refused to a `client` session and to an anonymous request, and the
   underlying row does not change.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the whole argument in one scroll | public |
| `/offers` | three packages, their floors and their accordions | public |
| `/expertise` | the eight service index | public |
| `/expertise/<slug>` | one service, argued at length | public |
| `/projects` | the filtered archive | public |
| `/projects/<slug>` | one case study | public |
| `/method` | `Throughline(TM)` and its four steps | public |
| `/about` | founder, differentiators, manifesto, awards | public |
| `/contact` | the enquiry form and the two ways to start | public |
| `/privacy` | what the studio stores | public |
| `/book` | the slot calendar | public to read, `client` to hold |
| `/book/hold/<reference>` | sector and topic, while the hold runs | `client`, own booking |
| `/book/confirm/<reference>` | the slot shown back, and confirmed | `client`, own booking |
| `/book/done/<reference>` | the confirmed call and its reference | `client`, own booking |
| `/login` | sign in | public |
| `/signup` | create a `client` | public |
| `/account/bookings` | a client's own calls | `client` |
| `/studio` | the console | `studio` |
| `/studio/slots` | open and close slots | `studio` |
| `/studio/enquiries` | enquiries and first responses | `studio` |
| `/studio/projects` | publish, unpublish, reorder | `studio` |

**Entry and redirects.** An anonymous request for a `client` or `studio` route goes to `/login` with
the intended address kept, and lands on that address after signing in. A `client` signing in with no
intended address lands on `/account/bookings`; `studio@example.com` lands on `/studio`. Logging out
returns to `/` and the token stops working immediately. A token that expires part way through the
booking steps leaves the page in place, says inline that the session ended, keeps the sector and
topic already typed, and offers to sign in again. A `client` reaching a `/studio` route is refused
with a stated reason rather than being redirected silently. An address matching no route renders the
not-found page.

**Journeys.**

1. *Book a call.* Open `/`, follow the booking action in the closing block to `/book`, choose the
   open slot on the second seeded day, sign in as `client@example.com` with `deku-demo-pw-2026`,
   return to that same slot, see the countdown start, choose the sector `beauty` and type a one line
   topic, continue to the confirm step, confirm, and land on `/book/done/<reference>` showing the
   slot and the reference. One message addressed to `client@example.com` is now in the studio's mail
   server, and `/account/bookings` lists the call.
2. *Lose the race.* Two signed-in clients choose the same slot at the same moment. One reaches the
   hold step; the other sees an inline banner in place saying the slot has gone, with the three
   nearest open slots as links, and no confirmation.
3. *Let a hold lapse.* Choose a slot, leave the page, and return after the hold has run out. The page
   says in place that the hold has ended and the slot is back in the grid; confirming from that page
   is refused and no booking exists.
4. *Share a filtered archive.* Open `/projects`, choose the `Visual identity` filter, copy the
   address, open it in a new session, and see the same narrowed grid and the same count.
5. *Read a case study.* From the archive open `Aster & Bloom`, read the summary, follow the
   outbound action to the client's own site, come back, and follow a related project.
6. *Compare the offers.* Open `/offers`, open the `Who the package suits` panel on `Opening Note`, read the
   disqualifying entry, and follow the named package it points to.
7. *Enquire.* Open `/contact`, submit with consent unchecked and see the consent control named
   inline with everything else still typed, check it, submit, and see the reference.
8. *Work the console.* Sign in as `studio@example.com`, open `/studio/enquiries`, record a first
   response against the newest enquiry, then open `/studio/slots` and close a slot that carries no
   booking.
9. *Be refused.* Signed in as `client2@example.com`, request another client's booking by its
   reference and be denied; request `/studio/slots` and be denied. Nothing changes either way.

**States.** Every list has an empty state that says what would be there: an archive filtered to a
service with nothing published under it, a calendar with no open slot left, a client with no calls
yet, an enquiry list with nothing in it, a case study with no related work. Every route has a loading
state rather than a blank frame. Errors render in place as an inline banner naming what went wrong
and what to do next, and never replace the route with an error page or a stack trace.

## UI/UX notes

**North star.** Somebody arriving here should understand inside one screen that the studio's own work
is the argument, and should feel the page being composed for them as they scroll rather than served
to them all at once.

**Register.** This is editorial and portfolio, not an operational tool. It may carry atmosphere and a
point of view, and on any route that carries work, the work itself is the first thing seen. Nothing
here should read as a dashboard: no dense control chrome, no data density borrowed from an admin
surface, no card that exists only to hold a button.

**The chain.** The site has to convey value, so the subject gets space around it and one thing
dominates each view while everything around it stays quiet. It has to guide, so every route has one
obvious next action and every other control is quieter than it. It has to convey trust at the moment
a visitor commits to a call, so the booking steps are still: nothing moves while somebody is reading
back the slot they are about to take. Space over dividers. Composition over decoration. Stillness
over reassurance at the moment of commitment.

**Palette by role, and the one rule that governs it.** The ground alternates between a near-white
neutral and a near-white warm neutral, and a section is one or the other, never a gradient between
them. Body copy sits on a deep neutral and headings on a deeper neutral that is the strongest ink in
the product; a third, near-black neutral belongs to a border at the moment it is pointed at and to
nothing else. Hairlines are a near-white neutral and meta text is a mid cool neutral, and there is no
grey scale between them: the product is ink, paper, or the accent. Exactly one saturated hue carries
the brand, a mid, soft red, and it appears on the recommended badge, on a filter under the pointer,
and on links, and nowhere else. A second brand accent introduced anywhere is a defect rather than a
decision. One further saturated colour exists and carries a single meaning: a light, vivid orange
marks a hold that is running down, and it may not appear on anything that is not a live hold. Failure
is carried by the same red the brand uses, scoped to the message that failed; success is carried by
the strongest ink and by the word itself rather than by a green; a state that is none of these must
not borrow any of them. The exact values are yours, so long as the alternation, the single accent and
the exclusivity above all hold.

**Type.** Three families, and the mixing rule is the signature. Display is `Playfair Display` at
weights 400 and 500, roman and true italic. Interface is `Syne` at weights 400 through 800. Body is
`Lexend Deca` at weights 100 through 300. A headline is one sentence, in one size, in the display
face, with two or three words leaning into the true italic; it is never two sizes and never two
colours, and the italic must be a different set of letterforms rather than the same letterforms
tilted. The interface ramp is fixed at 12px, 13px, 14px, 15px, 16px, 20px and 30px, with body copy at
14px over 21px. Display type is fluid, clamped at both ends, running from about 37px to about 53px at
the widest layout, and it is set solid with its leading equal to its size, which is what lets a three
line headline stack into a block dense enough to read as a shape. Interface type never interpolates
and display type never steps. Tight display over loose interface. Figures line up in a column
wherever amounts stack, so the three price floors read as one column.

**Ground over imagery.** Where type has to read across an image, a translucent overlay in the
near-white neutral sits between them at part opacity, and the image itself is darkened rather than
being covered by a solid panel. The overlay is the only translucent surface in the product.

**Shape.** The site's own surfaces carry no radius and no shadow. Cards, images, panels and buttons
are square edged and separation is done with rules and whitespace. The only rounded shapes are the
footer's social marks, the carousel bullets and the form fields, and the fields are barely softened.
Every button on the site's own surfaces is a text button with an underline that belongs to its
resting state rather than to being pointed at; the recommended badge is the one filled coloured
surface the product draws.

**Density.** Spacious. Sections read as separate at a glance without needing a dividing line, the gap
between two sections is several times the gap beneath a heading, and that gap about halves at the
narrowest layout. Every gap is a multiple of one base unit, which is yours to choose.

**Layout archetype.** Navigation lives in a panel, not in a bar. The header carries the wordmark and
one control, and the whole graph opens over the route from that control, listing the six primary
destinations with the eight services nested beneath. The header stays with the scroll on every route
and inverts to white where the section behind it is dark, from one mark rather than two and without a
flash at the boundary.

**Motion.** Scrolling is inertial and applied globally: a wheel or trackpad gesture continues briefly
after the input stops, and every scroll driven animation reads from that eased position rather than
from the raw offset. It is not a decorative detail, it is why the whole route reads as one continuous
piece rather than a stack of separate blocks. One character throughout: eased, considered on entry
and on exit, so that movement reads as a designed interface rather than a set of separate effects. Eight moments carry it and nothing
else animates. A block rests behind an edge and is uncovered from one side as it enters view, once,
and then stays arrived. An image drifts slowly inside its frame as the page passes it. A strip of
client marks runs continuously in one direction and never stops or restarts. The navigation panel
fades up while rising a short distance measured in its own type size, so the distance scales with the
navigation type. A filter control changes its text and its border on the same beat when it is pointed
at. The booking action shrinks very slightly under the pointer and returns. An accordion opens its
height while its marker turns from a closed form to an open one. The remaining hold time counts down
in place without the page moving under it. Nothing uses a different speed to feel special. A block
revealed once stays revealed for the life of the page, across any number of filter changes. Under a
reduced motion preference the inertial scroll is off and the native scroll takes over without a
reload, the marquee and the parallax hold still, and blocks arrive already uncovered: the reveal is
replaced by the arrived state rather than merely shortened.

**Hover.** Three distinct hover behaviours exist and no control invents a fourth. A link changes its
colour only. A filter control changes its label colour and its border colour together on one beat. An
action shrinks very slightly and returns. Each hover delta is small enough that it reads as a
response rather than as a movement, and each has a keyboard equivalent on focus.

**Components and their states.** Every control has a resting, pointed-at, pressed, focused and
unavailable state, and unavailable is never signalled by colour alone. The active archive filter must
be distinguishable from a filter merely under the pointer by something other than its colour. A
destructive action, which here means cancelling a confirmed call, asks once before it happens. The
Escape key closes the navigation panel and any open dialog and returns focus where it came from.

**Accessibility.** The baseline is WCAG AA and it is a floor rather than a goal. Body text and its ground meet WCAG AA contrast, and so does every label that
carries meaning. Keyboard navigation reaches every control in a sensible order with a visible focus
ring that is never removed. Icon-only controls carry names. Every content image carries alternative
text written for it, and a decorative image declares itself decorative so that it is skipped. The
navigation panel traps focus while it is open. The archive announces its resulting count when a
filter changes. Touch targets are comfortably sized on a phone.

**Responsive.** Three layouts, and where they change is yours, but the arrangement at each is not.
The archive is three across wide, two at tablet and one at phone width, with a gap that never
collapses and a card whose service line may run to three lines at the narrowest viewport without the
grid clipping it. The three offer cards sit in a row wide and stack at phone width, and the
recommended badge stays attached to the top edge of its card in both. The home route's portrait
blocks put the image beside the text wide and above it narrow. The slot calendar shows a week across
at the widest layout and one day at a time at the narrowest, and in both the chosen slot and its
countdown stay visible without scrolling. At every width between the named tiers the layout holds:
nothing overflows sideways and every navigation destination stays reachable.

**What it must not look like.** Not a page dominated by a single hue family with no second signal.
Not decoration standing in for content, where a shape fills a space that has nothing to say. Not a
marketing composition dropped over the working parts of the site: the calendar, the form and the
console are surfaces somebody uses, and they inherit the same restraint rather than the same
atmosphere. Not a stock arrangement borrowed from an unrelated subject and dressed in this palette.

## Technical requirements

The frontend is **SolidJS** built with **Vite**. The backend is **FastAPI** on Python. The rendering
model is a single-page application over a JSON API: the browser receives an application shell and
every route is rendered in the browser from JSON the API returns under `/api`. The one thing the
server must produce before the shell runs is each route's own identity, described below.

The datastore is **PostgreSQL**, reached at `DATABASE_URL`. Mail leaves over real SMTP to
**Mailpit**, reached at `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS`. The app's own public
address and port are `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Read every one of these from the
environment; never hardcode a host or a port. Both `postgres` and `mailpit` are already running and
reachable at those variables.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing services
available in this environment are `postgres` and `mailpit`, and reaching for anything else is a
contract violation.

Authentication is implemented by the app: email and password, hashed at rest, exchanged for a bearer
token the client sends on every request except login, signup and health. There is no external
identity provider.

`GET /api/health` returns `200` once the app is ready, which means the database is reachable and the
seed has completed. Application logs go to standard output, one line per request, carrying the
method, the path, the response status and the duration.

Every public route declares its own title, its own description and its own social preview image, and
no two public routes share a title or a description. A route's title reads as the route's own name,
a separator, then `Verdigris Studio`. The preview image must resolve when it is requested by its
declared address rather than being a path that answers not found, and the declaration must be present
in the document the server sends rather than only after the shell has run, because the reader of that
declaration is not running the application.

Imagery is generated rather than uploaded. A media entry stores which generator produced it, the seed
that produced it and the aspect it was produced at, so that the same entry renders the same image
every time. There is no file upload surface anywhere in this product.

## Data model

Sixteen tables. All timestamps are UTC. Money is integer minor units in `usd`.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**`accounts`** - `id`, `email` (unique), `password_hash`, `role` (one of `client` or `studio`),
`display_name`, `created_at`. Three seeded rows.

**`services`** - `id`, `slug` (unique), `name`, `index_title`, `definition`, `outcome`,
`index_order` (unique), `nav_order` (unique), `taxonomy_key` (unique), `detail`. Eight rows, in index
order: `Experience design`, `Web development`, `Copywriting`, `Art direction`, `Visual identity`,
`Search visibility`, `Print communication`, `Digital communication`. `taxonomy_key` is what joins a
service to a project's tags, and it is why the tree, the tags and the filters are one vocabulary.

**`projects`** - `id`, `slug` (unique), `client_name`, `deliverable_line`, `summary`, `client_url`,
`editorial_order` (unique), `featured_home`, `section_ground` (one of `light` or `dark`),
`published`, `published_at`. Twelve rows.

**`project_tags`** - `project_id`, `service_id`, unique together. Between one and six rows per
project.

**`project_media`** - `id`, `project_id`, `position`, `recipe`, `seed`, `aspect`, `layout_hint` (one
of `full` or `half`), `alt_text`. `position` is unique within a project. `alt_text` is required: a
media row without it is rejected and nothing is written.

**`packages`** - `id`, `slug` (unique), `category_word`, `name`, `promise`, `fit`,
`price_floor_minor`, `price_currency`, `recommended`, `display_order` (unique). Three rows. At most
one row has `recommended` true at any time; a second is rejected and the first is unchanged.

**`package_panels`** - `id`, `package_id`, `position` (one to four, unique within a package),
`label`, `body`. Four rows per package.

**`package_fit`** - `id`, `package_id`, `kind` (one of `positive` or `negative`), `body`,
`redirect_package_id` which is set only on a `negative` row.

**`testimonials`** - `id`, `quote`, `author_first_name`, `project_id`, `display_order` (unique).
Three rows.

**`awards`** - `id`, `year`, `entity_name`, `distinction`, `display_order` (unique). Three rows.

**`method_steps`** - `id`, `position` (one to four, unique), `title`, `description`. Four rows.

**`method_audience`** - `id`, `kind` (one of `positive` or `negative`), `body`, `display_order`.

**`studio_profile`** - one row: `founder_story`, `manifesto`, `studio_sentence`,
`projects_delivered`, `range_line`, `response_promise_hours`, `directory_score`, `directory_scale`,
`directory_verdict`, `directory_source`, `directory_review_count`.

**`slots`** - `id`, `starts_at` (unique across the table), `ends_at`, `state` (one of `open` or
`closed`), `created_at`. `ends_at` is always 30 minutes after `starts_at`.

**`bookings`** - `id`, `reference` (unique), `slot_id`, `account_id`, `state` (one of `held`,
`confirmed`, `cancelled` or `expired`), `hold_expires_at`, `topic`, `sector`, `created_at`,
`confirmed_at`, `cancelled_at`.

> **The named invariant `booking_one_live_per_slot`.** A slot carries at most one booking that is
> `held` or `confirmed` at any moment. Two simultaneous holds on the same slot must not both succeed:
> exactly one wins and the other is rejected. A `held` booking whose `hold_expires_at` has passed is
> not live, so the slot is available again without anything having to rewrite the old row first.

**`enquiries`** - `id`, `reference` (unique), `surname`, `first_name`, `telephone`, `email`,
`project_type` (one of `Launch` or `Redesign`), `budget_band` (one of `Under $5,000`,
`$5,000 to $10,000`, `Over $10,000` or `Not sure yet`), `message`, `source`, `consent_at`,
`received_at`, `promise_due_at`, `first_response_at`, `booking_id`. `promise_due_at` is derived on
write from `received_at` plus the studio's `response_promise_hours`, which is `24`.

**`page_identity`** - `id`, `route` (unique), `title` (unique), `description` (unique),
`preview_image_path`. One row per public route.

**Principles.** Two principles govern this schema. Every string that appears on more than one
route is a field rather than text typed into a template: the delivered count, the response promise,
the method name and the service vocabulary all qualify. And every list rendered in more than one
place is one list: projects render in four places and carry the same tags in all four.

**Delivery and reach.** Content records are public and their responses are cacheable, including the
archive's filtered views, which are cacheable per filter. A booking and an enquiry are transactions
rather than content: they are readable by the account that created them and by the `studio` account,
they are addressed by an unguessable reference, they are never listed to anybody else, and they are
not enumerable by guessing a reference.

**Ordering.** Archive order is editorial. It is not alphabetical, not chronological and not grouped
by tag, so it is a stored value somebody changes rather than a sort computed on read.

**Derived rather than stored:** an archive card's service line, which is joined from `project_tags`
on read; the count the archive announces; a booking's remaining hold time; whether an enquiry is
overdue, which is `promise_due_at` against now and `first_response_at`.

**Seed data.** Three accounts as listed above. Eight services. Twelve projects in editorial order,
the first six with `featured_home` true: `Aster & Bloom`, `Northgrove`, `Saltbox Kitchen`,
`Linen House`, `Petal Theory`, `Quiet Hours`, `Ferment Co`, `Marlowe Home`, `Cobalt Skin`,
`Verity Greens`, `Bread & Bone`, `Slow Sunday`. All twelve are published, each with between one
and six tags and between three and six media entries, every entry carrying alternative text. Three
packages with the floors above. Three testimonials. Three award rows: `2023` `Vare Studio`
`Honourable Mention`, `2024` `Verdigris Studio` `Nominee`, `2025` `Verdigris Studio` `Nominee`. Four
method steps. One studio profile with `projects_delivered` of `148`, `response_promise_hours` of
`24`, and the directory fields `4.3`, `5`, `Very good`, `Studio Index` and `4`.

Six open slots, seeded relative to first start: five on the next day at `09:00`, `10:00`, `11:00`,
`14:00` and `15:00` UTC, and exactly one on the day after that at `09:00` UTC. That last slot is
alone on its day and is the one two visitors will reach for.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the composition in full: what sits where on each route, what each repeated
component is made of, and how each behaves. It adds detail to the direction above and contradicts
none of it. Where a value is not given, the decision is the builder's, so long as the relationships
stated here hold.

### The global chrome

**Header.** Two elements and nothing else: the wordmark at the left and a single navigation control
at the right, set in the interface face at the small semibold step. No navigation bar, no search, no
second action. It sits above the route's content and below the navigation panel, and it stays with
the viewport for the whole scroll of every route. Over a section whose ground is dark, the wordmark
renders white; this is one mark reading its own background rather than two marks swapped at a fixed
scroll offset, because section heights differ per route and a fixed offset flashes at the boundary.

**The navigation panel.** The control opens a panel that covers the viewport. It fades up while
rising a short distance expressed in its own type size, so the entrance scales with the navigation
type rather than staying fixed while the type grows. It carries the six primary destinations in this
order: Offers, Expertise, Method, Projects, About, Contact; the eight services nested under Expertise
in index order; and the booking action. It closes on its own close control and on the Escape key.
While it is open the route beneath does not scroll, focus cannot leave the panel, and closing returns
focus to the control that opened it.

**The booking block.** The last block before the footer on every public route, four lines in this
order: an eyebrow in the interface face at the small step; a headline in the display face with two
words in true italic; the primary action, a text button with a trailing arrow and a resting
underline; and the response promise line, set at the smallest step and quiet. Under the pointer the
action shrinks very slightly and returns.

**The footer.** Long, and it lays the whole graph out in the open, in this order: the wordmark at
display size set as type rather than as an image; the six primary destinations; the primary action
with its response line; the studio sentence as one paragraph; the eight service links; the
affiliation line and its marks; the legal list carrying the copyright, a rights line, the privacy
link and the terms link; four social marks; and the directory rating badge. The primary list is
written once and arranged for each layout, never emitted twice into the document.

### Route: home

Eleven blocks in this fixed order, and every block after the first is uncovered by the reveal as it
is reached.

1. **Hero.** The only full bleed image behind live type on the site, and the only block complete at
   first paint. The subject is cropped so that the eye line sits above the headline. Centred over it:
   an eyebrow in letterspaced capitals; the headline in the display face, three lines at the widest
   layout, with the four market words leaning into the true italic; a two line subline in letterspaced
   capitals; and two stacked underlined actions, the second carrying the trailing arrow. The headline
   is one sentence with four words leaning, never a headline plus a subheadline. It must be legible
   before the background image has decoded, and the image itself is darkened rather than covered with
   a panel.
2. **Proof band.** A client mark marquee above a two line statement: the delivered count with the
   number leaning into italic, then one line of range.
3. **Who it is for.** A portrait beside a headline carrying one italic phrase, a subheadline, and
   three qualifying lines each opening with an asterisk glyph. The asterisk is a text character and
   is the only ornament in the product; it opens every list item in this construction wherever it
   appears.
4. **The approach.** The same construction without the portrait, and a headline carrying three
   italic words in series: positioning, performance and usage. Those three words recur as the three
   promise columns on the offers route. They are one vocabulary, not three coincidences.
5. **The method.** A short block on the warm ground naming `Throughline(TM)`, a promise of three
   sentences, a paragraph, and a link through to the method route.
6. **The offers.** Three cards in a row, each a category word, the package name in the display face
   and a one line promise. No prices on this route. The block closes with one action into `/offers`.
7. **The work.** Six project cards in two rows, each an image, a client name and an action reading
   through to the case study. Cards here carry no service tags, which is what distinguishes this grid
   from the archive grid.
8. **Awards.** Three rows separated by full width hairlines, each carrying the year at the left, the
   entity name, and the distinction at the right edge as an underlined label.
9. **Testimonials.** A carousel of client quotations, each opening with a right pointing quotation
   glyph and closing with a first name, a client name and a link to that client's case study.
10. **Booking block.**
11. **Footer.**

### Route: offers

Seven blocks: a type hero of two display lines set solid with an eyebrow above and a subline below;
an observation block; a problem block; a promise block whose headline sits over three columns; the
three package cards; the booking block; the footer. The type hero is the template every route except
the home route uses.

**The package card**, in order: the category word in the interface face, small and letterspaced and
quiet; the package name in the display face at the large step; the promise on one line; the fit
paragraph of two sentences; the price floor with its from label and its tax status; the four panel
accordion, closed at first paint; and the primary action with a trailing arrow.

**The accordion control** is a full width row carrying the panel label and a marker that reads as a
minus when open and a plus when closed. Opening animates the panel's height while the marker turns.
Panels do not close each other.

**The recommended badge** sits at the top edge of the middle card and breaks its outline. It is set
in the interface face, in white, on the one saturated brand colour, and it is the only filled
coloured surface the product draws.

### Route: expertise and service detail

The index lists the eight services, each an index title in capitals, a definition line and an outcome
line, separated by hairlines. A service route uses the type hero, then the long form body, then the
projects tagged with it in the archive's own card form, then the booking block.

### Route: projects

The type hero with an italic phrase across two lines; the filter row; the grid; a load more action;
the proof band; the booking block; the footer.

**The filter row** is nine controls: the eight services and an `All` control. At rest a control
carries its label in the strongest ink inside a hairline border in the mid cool neutral. Under the
pointer the label takes the brand red and the border takes the near-black neutral, both on the same
beat. The active control is marked by something other than colour, so that it is still legible when
the pointer is elsewhere and to somebody who cannot separate the two hues.

**The card** is a generated image at full card width with no radius and no shadow, the client name in
the interface face in capitals at the body step, and the service line beneath it joining the
project's tags with a spaced hyphen, set tight and quiet. The whole card is the link; there is no
separate button on this route. A card with six tags wraps its service line rather than truncating it,
at every layout.

**Load more** appends the next page of cards into the same grid rather than paginating. Appended
cards are uncovered by the same reveal as the initial set, the scroll position does not move, keyboard
focus lands on the first appended card, and the action is removed rather than disabled once the
archive is exhausted.

### Route: case study

Five blocks: the hero, the media sequence, related work, the booking block, the footer.

**The hero** is a four part stack: a lower case eyebrow naming the deliverable; the client name in
the display face; the tag line in the same hyphen joined form the archive card uses; and a
description of two to four sentences. Beneath it sits the outbound action carrying the client site's
host name as its visible label.

**The media sequence** alternates full bleed single images with two up pairs, at zero radius, with no
captions. Each layer drifts slowly inside its frame as the page passes it.

### Route: method

The type hero; the method name with its mark; the promise; the four steps; the two audience lists;
the booking block; the footer. Each step is a row carrying a parenthesised superscript index, a title
and a paragraph, separated by full width hairlines. The same construction carries the three
differentiators on the about route, without the step thumbnails.

### Route: about

Eight blocks: the type hero naming the four markets; the awards wall; the founder block; the
differentiators; the proof band; the manifesto; the booking block; the footer.

**The voice change is deliberate and must survive.** The founder block is written in the first person
singular and every other block on the site is written in the first person plural. It is a founder's
practice that became a studio, and normalising the voice costs more than it tidies.

**The manifesto** is eight paragraphs of long form argument set in the body face at 16px over 24px,
which is the only place in the product where that pairing appears, and on a measure narrower than the
blocks around it. It is one long form field rendered as prose and is never broken into cards.

### Route: contact

Four blocks: the hero carrying the eyebrow, the headline, a proof line, an instruction, the promise
and the form; the alternative path offering a slot directly, with its two lines, the booking action
and a reassurance line reading that the call carries no commitment and no sales approach; the booking
block; the footer.

**The form.** Eight fields and a consent control, stacked in the order given in Core features, with
the two selects carrying a caret in the interface style. Fields sit on the quiet near-white ground,
are the only barely softened corners in the product, and carry a visible label rather than a
placeholder standing in for one. A rejected field is named beneath itself in the brand red, the
message says what is wrong rather than that something is wrong, and the field itself is also marked
by something other than colour. The submit action is a lower case imperative with a trailing arrow.

### Route: book

The type hero; the calendar; the steps; the booking block; the footer.

**The calendar** is a grid of slots. At the widest layout it shows a week across with days as columns
and times as rows; at the narrowest it shows one day at a time with a control to move between days.
Each slot cell carries its start time in the interface face and its state: choosable, taken or
closed. A taken slot stays visible and is not selectable, and it says taken rather than simply going
quiet, because a visitor needs to see that the calendar is busy rather than empty.

**The hold.** Choosing a slot marks it as yours and starts a countdown that renders in place in the
light, vivid orange that means nothing else in this product. The countdown updates without the
surrounding layout moving, so that nothing shifts under the pointer while somebody is reading.

**The steps.** Three addressed steps, each on its own address, each showing which of the three it is,
with a control back to the previous one that keeps the hold running. The confirm step reads the slot,
the sector and the topic back in plain words before the action that commits them, and nothing on that
step moves while it is being read.

**Losing the race, and the hold running out**, both render as an inline banner in place at the top of
the step rather than as a dialog or a redirect: a plain sentence saying the slot has gone or the hold
has ended, and then the three nearest open slots as links. Neither ever shows a confirmation first
and corrects it afterwards.

### Typography strategy

The three families are the product's typography and nothing else is introduced beside them. Each is
declared with a fallback stack so that text is readable while a face is still arriving and never
disappears while it loads: the display face falls back to an old style serif, the interface face to a
neutral sans, the body face to the system sans. No font ships as a binary with the app; all three are
open licence families fetched from a public font service, which is why naming them is not an asset
dependency. That is the whole font strategy: three families, declared with fallbacks, swapped in when
they arrive.

### Iconography

The icon set is small and closed: a close mark, a chevron for a select, a caret, a star for the
rating badge, a rule mark that reads as a minus when an accordion panel is open and a plus when it is
closed, a loading spinner, four social marks and the directory rating mark. All are drawn as vector
shapes on one grid at one stroke weight and inherit the current text colour rather than carrying
their own. Icon-only controls carry a name.

The spinner is the one icon that moves: it rotates continuously while something is being fetched, on
the same eased character as everything else, and it is replaced by content rather than fading into
it.

What is not an icon: the asterisk that opens a qualifying line, the arrow that trails an action, and
the quotation glyph that opens a testimonial. All three are text characters set in the surrounding
face, they inherit its size and colour, and drawing any of them as a mark would break the line they
sit on.

### Depth and stacking

Depth is expressed by stacking order alone, never by shadow. There are four levels and nothing else
occupies one: the route's own content sits at the base; the header sits above the content and below
everything else; an inline banner reporting a lost race or an ended hold sits above the header so
that it is never covered; and the navigation panel sits above all of them with its scrim directly
beneath it. Nothing else in the product is raised.

### Motion inventory and easing

One easing carries the whole inventory of moments listed in the direction above. Motion leaves
quickly and arrives slowly, and the only exception in the product is the marquee, which runs at a
constant rate because a strip that eased would read as stopping and starting. Nothing else varies its
character to feel distinctive.

### Carousel mechanics, defined

Two carousels exist: the testimonials on the home route and the related work on a case study. Their
mechanics are the same and are defined once. Each advances one item at a time, wraps from the last
item back to the first, pauses while the pointer is over it or while any of its content holds focus,
and stops entirely under a reduced motion preference. Each is operable by keyboard with the arrow
keys once the strip has focus, exposes which item is current, and never traps focus. Neither
auto-advances faster than a person can read the item it is showing, and neither carousel is the only
route to its content: every testimonial's project and every related project is reachable from a plain
link elsewhere on the site.

### Components earned by repetition

A component exists here because it repeats, not because it could. The modules earned by repetition
across this architecture are: the type hero used by every route except the home route; the reveal
wrapper; the archive card; the booking block; the accordion panel; the rule-separated numbered row
used by both the method steps and the about route's differentiators; the proof band; the awards row;
the carousel; the slot cell; and the inline banner. Anything appearing once is written where it
appears.

**The reveal wrapper is the important one.** It is the single most important component in the build,
because almost every block on the site is inside one and its rule is easy to get subtly wrong. One
wrapper covers every case: it uncovers its children once when they enter view, it remembers that it
has done so for the life of the page, and it is inert under a reduced motion preference. A block that
re-enters the document after filtering, after a load more, or after any list changes underneath it
must not run a second time.

### Stagger

A short delay between sibling elements revealing, so that a row of cards arrives one after another
rather than together, is permitted but is not required. It is unproven on the reference and it is
recorded here as a latitude rather than an obligation: where it is used it must be small enough that
the last sibling is not noticeably late, and it is removed entirely under a reduced motion
preference.

### Breakpoints and layout tiers

Three layout tiers: phone, tablet and desktop. Where each breakpoint sits is yours, but each tier's
arrangement is fixed by the responsive rules in the direction above, and the layout must hold at
every width between two breakpoints rather than only at the three named widths.

### Language and locale

The document declares its language so that assistive technology reads it correctly, and every route
inherits it. Dates and times render in one locale throughout, slot times carry their zone
explicitly, and amounts render with the currency symbol in front and grouped digits. The product
ships in one language; there is no locale switcher and no translated route.

### Generated imagery

The build ships no image, font binary, video or model file. Every image on the site is generated from
its stored recipe and seed, which means the same entry renders the same picture every time.

- **Photography.** Where the reference used a photograph, the build generates an abstract composition
  in the product's own palette at the same aspect and the same crop intent. A hero composition places
  its focal area above where the headline falls.
- **Client marks.** A client mark is generated as a wordmark set in the interface face, rendered flat
  and desaturated so that the marquee reads as one strip rather than as a row of competing logos.
- **Device mockups.** Where a case study shows work on a device, the mockup is drawn as geometry: a
  plain rounded rectangle outline holding a generated composition, never a photograph of hardware.
- **Texture and grain.** A very fine grain may be laid over a generated composition to stop it
  banding, at a strength that is invisible as texture and only visible as the absence of banding.
- **Video.** There is no video anywhere in this product. Where the reference carried one, the build
  carries a generated still.

Every generated image still carries alternative text written for it by a person.

### Copy identity

These strings are content and are rendered exactly: the response promise line `reply within 24 hours`;
the recommended badge `Recommended`; the four accordion labels `Who the package suits`,
`What the package contains`, `What the studio delivers`, `What can be added`; the four method step titles `Diagnostic`, `Art direction`,
`Digital experience`, `Brand alignment`; the archive's ninth control `All`; the four budget bands
`Under $5,000`, `$5,000 to $10,000`, `Over $10,000` and `Not sure yet`; the two project types
`Launch` and `Redesign`; the price form `From $3,500 plus tax`; the method name `Throughline(TM)`;
the directory verdict `Very good`; and the three award distinctions `Honourable Mention`, `Nominee`
and `Nominee`.

## Constraints

- One studio. There is no second tenant, no agency switcher and no organisation model.
- No cart, no payment surface, no plan ladder, no subscription, no invoice. Prices are published
  floors and nothing on this site takes money.
- No comments, no likes, no reactions, no messaging, no notification feed, no live chat.
- No file upload anywhere. Imagery is generated from a stored recipe and seed.
- No visitor-assembled shortlist, no self-serve quote configurator, no case study outcome ledger.
- No third party scheduling, analytics, consent or form protection vendor, and no embedded widget
  from any of them.
- No external network calls at runtime. The only backing services are the ones named in this brief.
- No native app, no offline mode, no push.
- No general purpose content management. Only the studio's own collections are editable, and only by
  the `studio` account.
- The archive stays responsive with a few hundred published projects and the calendar with a few
  hundred slots, which is the volume this studio reaches in a decade.
- Six addresses name surfaces this product deliberately does not have, and each answers as not
  found like any other unknown address: `/cart`, `/checkout`, `/comments`, `/shortlist`, `/quote`
  and `/messages`.
- The two reserved directories sit at `/app/.browser_screenshots` and `/app/.downloads`.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses.
  Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Field names are exact. A list endpoint returns a top-level JSON array. A successful
call returns the named resource or shape; an invalid or unauthorized call is rejected as a client
error, never as a server error and never as a silent success, and carries a message naming the
reason.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | - | `status` |
| `POST /api/auth/signup` | `email`, `password`, `display_name` | `access_token`, `email`, `role` |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `email`, `role` |
| `GET /api/services` | - | all eight: `slug`, `name`, `index_title`, `definition`, `outcome`, `index_order`, `nav_order`, `taxonomy_key` |
| `GET /api/services/{slug}` | - | one service with its `detail` and its tagged published projects |
| `GET /api/projects` | `service` | published projects in editorial order: `slug`, `client_name`, `deliverable_line`, `tags`, `editorial_order`, `featured_home`, `cover` |
| `GET /api/projects/{slug}` | - | one published project with `summary`, `client_url`, `tags`, `media`, `related`, or not found when it is unpublished |
| `GET /api/packages` | - | all three in display order: `slug`, `category_word`, `name`, `promise`, `fit`, `price_floor_minor`, `price_currency`, `recommended`, `panels`, `fit_positive`, `fit_negative` |
| `GET /api/method` | - | `name`, `promise`, `steps`, `audience_positive`, `audience_negative` |
| `GET /api/awards` | - | all three in display order: `year`, `entity_name`, `distinction` |
| `GET /api/testimonials` | - | all three in display order: `quote`, `author_first_name`, `project_slug` |
| `GET /api/studio-profile` | - | `founder_story`, `manifesto`, `studio_sentence`, `projects_delivered`, `range_line`, `response_promise_hours`, and the five directory fields |
| `GET /api/slots` | `from`, `to` | every slot in the window: `id`, `starts_at`, `ends_at`, `state`, `is_available` |
| `POST /api/slots/{id}/hold` | - | the created booking: `reference`, `slot_id`, `state`, `hold_expires_at`; or a refusal naming the slot as taken, carrying `alternatives` |
| `GET /api/bookings/{reference}` | - | the caller's own booking, or denied when it belongs to somebody else |
| `PATCH /api/bookings/{reference}` | `sector`, `topic` | the booking with its answers, or per-field errors when it is invalid |
| `POST /api/bookings/{reference}/confirm` | - | the `confirmed` booking, or a refusal when the hold has expired |
| `POST /api/bookings/{reference}/cancel` | - | the `cancelled` booking and the slot back as available |
| `GET /api/account/bookings` | - | the calling account's own calls only |
| `POST /api/enquiries` | `surname`, `first_name`, `telephone`, `email`, `project_type`, `budget_band`, `message`, `source`, `consent` | `reference`, `received_at`, `promise_due_at`, and per-field errors when it is invalid |
| `GET /api/studio/enquiries` | - | every enquiry, newest first, with `promise_due_at` and `first_response_at` |
| `POST /api/studio/enquiries/{reference}/response` | - | the enquiry with `first_response_at` set, unchanged if it was already set |
| `POST /api/studio/slots` | `starts_at` | the created slot, or a refusal when that start time already exists |
| `POST /api/studio/slots/{id}/close` | - | the closed slot, or a refusal naming the confirmed booking that blocks it |
| `POST /api/studio/projects/{slug}/publish` | - | the published project, or a refusal naming the media entry with no alternative text |
| `POST /api/studio/projects/{slug}/unpublish` | - | the project, back to unpublished |
| `PATCH /api/studio/projects/{slug}` | `editorial_order` | the reordered project |

Bearer auth is required on everything except `GET /api/health`, both auth endpoints,
`POST /api/enquiries` and the public read endpoints.

**No mocks.** `mailpit` is the only place a confirmation message exists. An in-memory list of sent
mail, a row written to a `messages` table and rendered back as proof, a log line saying a message was
sent, or a success banner the app returns to itself are all the same failure wearing different
clothes. The same holds for `postgres`: a booking that lives only in the browser or only in the
running process is not a booking. The named provider is the fact - the app's UI and its own tables
can only reflect what lives in the provider, never substitute for it.

## Definition of done

A visitor can read a case study, filter the archive down to one service and share that view by its
address, then sign in and take a slot in the studio calendar, landing on a confirmed call with its
own reference while one confirmation message arrives for that account alone. When two people reach
for the same slot at the same moment only one of them ends up with a call, the other is told the slot
has gone and offered three alternatives, and a hold nobody finishes returns the slot to the grid. The
studio owner, and nobody else, can open and close slots, read every enquiry and record when a reply
was sent.
