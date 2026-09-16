# Tallow

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, read the numbered index of
seventeen productions, open one and watch its film, and book a fifteen minute introductory call
against the agency's published availability, without hitting an error page and without making an
account. Two different strangers reaching for the same fifteen minutes must NOT both end up with
it: exactly one confirmation exists afterwards and the other is told the slot has gone. This
cannot be faked in the interface. Hiding a taken slot from a grid while the endpoint behind it
still accepts a booking is not protection, and the rule must hold when both requests arrive at
the same instant rather than one after the other.

## Overview

Tallow is a two-principal advertising agency. The site does one commercial job: turn a brand
marketing director who has ten minutes and a shortlist into a booked introductory call.

Almost all of the product is the work. Seventeen productions, numbered, each carrying its client,
its category and its running time. Opening one gives a case study built around a hero reel, the
credits for the crew assembled for it, and galleries of stills where every still carries a
caption. The index flips between a grid of cards and a dense list without leaving the page, and
the flip changes the shape only: the same seventeen, in the same order.

One conversion action appears on every route and there is never a second one competing with it:
book a fifteen minute call. The agency publishes its availability, a visitor picks a slot, the
slot is held while they type their details, and confirming it sends them a message. The two
people who run the agency sign in to read what has been booked and to publish more time.

There are no visitor accounts, no cart, no dashboard, no comments and no search. The genuinely
hard part is the booking: a hold has to expire, a repeat submission must not make a second
booking, and two simultaneous confirmations of one slot must leave exactly one.

## User roles

| Role | Can do |
|---|---|
| `visitor` | Read the index in either shape, open any case study, watch a film, read the about and privacy pages, and book a call. Needs no account for any of it. **Cannot read the agency's booking list. Cannot publish or withdraw availability. Cannot see who else has booked a slot.** |
| `principal` | Everything a visitor can do, plus: sign in, read the booking list, publish availability, and withdraw a slot nobody has taken. **Cannot withdraw a slot carrying a confirmed booking. Cannot publish or withdraw availability belonging to the other principal.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI
is not authorization: a direct API call from a `visitor` session to any `principal`-only endpoint
must be rejected by the server (an unauthorized request is denied, not served), leaving the
protected state unchanged.

There is no public signup. Accounts exist only because they are seeded. There is no password
reset and no invitation flow. Booking deliberately requires no account at all.

Seeded accounts, all sharing the password `deku-studio-2026`:

| Email | Display name | Role |
|---|---|---|
| `dara@tallow.agency` | Dara Okonjo | `principal` |
| `otis@tallow.agency` | Otis Vandermeer | `principal` |
| `casey@tallow.agency` | Casey Brandt | `visitor` |

## Core features

### Booking a call

This is the rule the product exists to get right.

1. Asking for availability returns only slots whose state is `published` and which carry no
   confirmed booking. A slot already taken is never offered.
2. Choosing a slot places a hold on it. While that hold is live, a second request to hold the
   same slot is refused as a conflict, and a booking attempt on it by anyone else is refused the
   same way.
3. A hold lasts `600` seconds from creation. Once it has lapsed the slot is offered again, and
   confirming against the lapsed hold is refused as gone rather than silently succeeding.
4. Confirming a held slot creates one booking with status `confirmed`, recording the attendee's
   name, address, timezone and agenda.
5. **Two confirmations of the same slot arriving at the same instant must not both succeed.**
   Exactly one confirmed booking exists for that slot afterwards and the other caller is refused
   as a conflict. **This must hold at the database level, not only in application logic.** A
   rejected confirmation leaves no partial state: no orphaned hold, no second booking row.
6. A booking request carries an idempotency key. Submitting the same key twice returns the
   booking already created and creates no second one, whatever the interval between the two.
7. An agenda outside one to `2000` characters, or an attendee name outside two to `80`, is
   rejected as invalid and writes nothing.
8. Booking requires no account. A signed-out visitor completes the whole flow.

### The confirmation message

1. A booking reaching `confirmed` sends exactly one message.
2. It is addressed to that booking's own attendee address, with no cc and no bcc.
3. Its subject begins `Call confirmed:` followed by a space and the principal's display name, so
   a call booked with Dara Okonjo carries the subject `Call confirmed: Dara Okonjo`.
4. Its body is not empty and names the principal and the start time.
5. Nothing else in the product sends mail. Placing a hold sends none, a hold lapsing sends none,
   withdrawing an untaken slot sends none, and a refused booking sends none.

### The index and its two orderings

Seventeen productions are seeded, listed under `## Data model`.

1. The work index returns all seventeen in `sort_index` order, numbered from `01` to `17`.
2. The home feed returns the eleven carrying `featured_on_home`, in `home_sort_index` order.
3. **The two orderings are independent.** The home feed is not the first eleven of the index and
   not the index order with six removed: it is its own sequence. A build that derives either
   ordering from the other is wrong.
4. A production carries a `home_sort_index` if and only if it carries `featured_on_home`.
5. Flipping the index between its grid shape and its list shape changes neither the membership
   nor the order. The same seventeen appear in the same sequence in both.
6. Every count the interface shows is counted rather than written down: the work count beside
   the navigation, the count beside the index heading and the count on the home feed all come
   from the stored rows.

### A case study

1. Opening a production at its own address returns its title, client, category, running time,
   year, its hero reel, its credits in stored order, and its galleries.
2. Every gallery still carries a caption, and the caption is required in the stored data rather
   than only in the interface. A still with no caption cannot be stored.
3. Galleries are returned in their stored order, and the stills within a gallery in theirs.
4. An unknown production slug renders the product's own not-found page rather than a blank or an
   unstyled error.

### The principal surfaces

1. A principal signs in and reads the booking list: attendee, time and slot for every confirmed
   booking against them.
2. A principal publishes further availability, which appears in what visitors are offered.
3. A principal withdraws a slot nobody has taken; it stops being offered.
4. **Withdrawing a slot that carries a confirmed booking is refused.** A confirmed booking is
   never taken away silently, and the refusal says so.
5. A principal acting on the other principal's availability is denied, and the row does not
   change.
6. A `visitor` session asking for any principal endpoint is denied by the server, and nothing
   changes.

### The public surface

These hold on every route a signed-out visitor can reach.

1. A privacy page states what the agency records about a person who books, and is reachable from
   the footer of every route.
2. Every internal link on every public route resolves. A link in the rail, in the index, in a
   case study or in a footer that leads nowhere is a defect.
3. An address that matches no route renders the product's own not-found page, carrying a way
   back, and answers as not found rather than as success.
4. Every form rejects invalid input inline, names the field that is wrong in words beside it, and
   writes nothing.

### Auth

Email and password. A successful sign-in returns a bearer token in a field named `access_token`,
and the client sends it on every authenticated request. Passwords are stored hashed, never in
plain text, and no endpoint returns a password or its hash. A token is valid for twenty-four
hours from issue; an expired or malformed token is denied exactly as a missing one.

1. Signing in with a seeded email and `deku-studio-2026` succeeds and returns `access_token`.
2. Signing in with a seeded email and any other password is denied, and the response does not
   reveal whether the address exists.
3. Signing in with an unknown address is denied identically.
4. Reading the session with a valid token returns that account's address, display name and role.
   Reading it without a token is denied.

## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/` | The home feed of eleven, the agency band, the information band, the contact band | none |
| `/work` | All seventeen, numbered, in grid or list | none |
| `/work/{slug}` | One case study: hero reel, credits, captioned galleries | none |
| `/about` | What the agency does, how it works, who runs it | none |
| `/contact` | The address, set large, and the booking entry point | none |
| `/book` | The booking panel as its own address, for a visitor who arrives cold | none |
| `/privacy` | What the agency records about a person who books | none |
| `/legal` | The disclaimer | none |
| `/sign-in` | Sign in | none |
| `/studio` | The principal's booking list | `principal` |
| `/studio/availability` | Publish and withdraw availability | `principal` |

### Entry and redirects

A signed-out visitor who opens `/studio` or `/studio/availability` is sent to `/sign-in`, and
after a successful sign-in lands on the address originally asked for rather than a generic home.
A signed-in `visitor` who opens either is shown a refusal saying the surface belongs to the
agency, and is not sent to sign in again. Signing out returns the visitor to `/` and discards the
token. A token that expires mid-action leaves the principal on the same surface with a message
saying the session ended and a control to sign in again. A hold that lapses while the booking
panel is open stops the countdown, disables confirm, and offers to hold again, keeping every
detail already typed.

### Journeys

1. **Read the work.** Open `/`. The feed shows eleven productions beginning with Vertical Mile
   and then Master the Route. Follow the work link to `/work`: seventeen, numbered `01` to `17`,
   beginning with Vertical Mile and ending with Steppe Space Shuttle. Flip to the list shape and
   verify the same seventeen in the same order. Open `norvel-drift` and read its credits and its
   captioned galleries.
2. **Book a call, signed out.** From any route take the single call to action. The panel opens
   over the page. Pick a published slot with Dara Okonjo. A countdown starts. Give a name, an
   address, a timezone and an agenda, and confirm. The panel's content is replaced in place by a
   confirmation naming Dara Okonjo and the time. The attendee address holds one message whose
   subject is `Call confirmed: Dara Okonjo`.
3. **The slot goes while you type.** Two visitors hold the same slot in turn: the second is
   refused as a conflict, the grid refreshes in place, and the details already typed are kept.
4. **The agency reads its day.** Sign in as `dara@tallow.agency`. Open `/studio`: the booking
   from journey 2 is listed with its attendee and time. Open `/studio/availability` and withdraw
   an untaken slot; it stops being offered. Attempt to withdraw the slot from journey 2: refused,
   and the booking is untouched.
5. **A visitor is refused.** Sign in as `casey@tallow.agency`. Open `/studio`: refused as an
   agency surface. Ask the availability endpoint directly with that session's token: denied, and
   no row changes.

### States

Every list has an empty state written for that list: a principal with nothing booked is told no
call has been booked yet; a day with no free slot is told the day is full rather than shown an
empty grid. The index is never empty, because all seventeen are seeded. Every route has a loading
state holding the final layout's shape so nothing jumps when content arrives. An unknown slug and
an unknown address both reach the product's own not-found page, carrying a link home and a link
to the work index. A failed request says what failed and offers the action again. No route may
leave the visitor on a blank page or an unstyled error.

## UI/UX notes

The design direction is `playful-consumer`. The mood is bright, energetic and consumer-grade. The
type personality is a geometric sans with one characterful display face. The motion character is
`springy`. The density is comfortable. The layout archetype is a persistent rail beside the
content column, because the navigation is a rail.

**North star.** A marketing director with ten minutes should come away believing these people
make excellent film, and should never once have to hunt for how to talk to them.

**Register.** Editorial, and the subject is the film. The interface is the frame around the
picture and never the picture.

**The work over the interface. One action over many. A held promise over a quick yes.**

### Ground and the four meanings

The ground is dark and near-neutral, because the product is a wall of film stills and a light
ground would fight them. Two slightly deeper variants of that ground exist and their only job is
to mark where one band of content ends and the next begins. Cards sit on a surface barely lighter
than the ground, and a card must stay visibly separate from it without a border and without a
shadow, which means the separation is carried by the difference between those two surfaces alone.

Four colours carry meaning and each belongs to exactly one job. One accent marks the single call
to action, and it is the only saturated colour anywhere in the interface. One marks a refusal.
One marks a hold that is still running. One marks a slot already taken. A surface that is none of
those four borrows none of them. The exact shades are yours, so long as they hold those rules and
clear the contrast floors below.

`energetic` is scoped to that one accent. The call to action is the brightest thing on every
route and nothing else competes with it, which is the point: a page of dark film stills with
exactly one lit control. Every other button in the product is quiet. Each page leads with that
one primary action, visually distinct from every secondary one, and no page carries a second
action dressed to look equally important.

Text carries three levels of presence and no more: the thing being read, the label naming it, and
the quiet metadata beneath.

**Mode.** The product ships one fully designed dark appearance and no second one. There is no
light mode and no theme switch. The work is film, it is viewed against a dark ground the way film
always is, and a single known ground is a requirement rather than a limitation. Every contrast
floor below is stated against that one appearance.

### Type

`geometric sans` carries the whole interface. One characterful display face is reserved for the
largest type only: a production title on its own case study, and the agency's address on the
contact route, which is set enormous because at that size the address is the design of the page.
Nothing between those two sizes uses the display face. Section labels and counts are set in a
monospace, small, in square brackets, and that is the only place monospace appears in the
product. Running times and ordinals line up in a column wherever they stack, which on the index
is every row.

### Density and rhythm

Comfortable. The gap between two bands of content is roughly three times the gap beneath a
heading, and about halves on a narrow screen. Every gap derives from one base unit, which is
yours to choose, and no gap is a value that is not a multiple of it. Bands must read as separate
at a glance without a dividing line; if they do not, the gap is too small rather than the divider
missing.

### Motion

`springy` is bound to the booking confirmation and to nothing else. When a slot becomes the
visitor's, the confirmation settles into place with a slight overshoot, once. A film card being
pointed at does not overshoot, a panel opening does not overshoot, and no other surface in the
product does either. That restriction is what makes the overshoot mean "this is yours now".

The index flip is the other piece of motion that matters, and it is not springy. Moving between
the grid shape and the list shape, each card travels from where it was to where it lands, so the
eye can follow one production across the change. Cards do not fade out and back in, because a
fade loses the thing the visitor was looking at. The hold countdown runs continuously and
visibly while a slot is held.

A reader who has asked their system to reduce motion gets the whole product with every transition
removed: the flip becomes an instant relayout, the confirmation simply appears, and the countdown
remains a live number.

### The surfaces

**The rail.** Persistent beside the content on every route. It carries the wordmark, the four
destinations with the live work count beside the work link, and the single call to action. It
does not scroll with the page. On a narrow viewport it collapses to the wordmark and one control
that opens it as a full-height panel, and the call to action stays reachable without opening it.

**The work index.** The split shape: the list of productions beside the one currently selected,
so choosing a production does not throw away the list. Each row carries its ordinal, title,
client, category and running time. In the grid shape the same rows become cards with the still
above the same metadata. One column on a phone, two on a tablet, three on a wide screen, with a
gap that never collapses and a layout that holds at every width between.

**A case study.** Leads with the hero reel at the full width of the content column. Then the
credits as a plain two-column list of role and name. Then the galleries, each under its own
bracketed label, every still carrying its caption as visible text rather than only as a text
alternative.

**The booking panel.** Slides over whatever was being read rather than replacing it, so the
visitor keeps their place. A month view shows only days carrying a free slot. Times are shown in
the visitor's own zone with the zone named, and the agency's own city stated beside it. Choosing
a time starts the countdown. The details form sits under the chosen time, never on a separate
step. On success the panel's content is replaced in place by a confirmation naming the principal
and the time; it is a banner within the panel, not a new page, and it does not disappear on its
own.

**The principal surfaces.** Quiet and dense, built for a person checking their day. The booking
list is a table of attendee, time and slot. No hero, no oversized heading.

### Components and their states

One primary action style, carrying the accent, and one quieter alternative carrying neither.
Both have resting, pointed-at, pressed, focused and unavailable states, and unavailable is never
signalled by colour alone: it also loses its fill and takes a cursor that says it cannot be used.
Every field has resting, focused, filled, invalid and disabled states, and an invalid field says
what is wrong beneath it in words rather than only changing colour.

### Accessibility

Body text and every control label clear the WCAG AA contrast floor against whichever ground sits
behind them, and large type clears the large-text floor. Every control is reachable by keyboard
navigation in the order it reads on the page, and the focus indicator is visible against all of
the grounds named above rather than only the darkest. Every still carries its caption as its text
alternative. The film player is operable from the keyboard and each of its controls is labelled.
The countdown is announced as it changes rather than only drawn.

### Responsive

The layout holds from a narrow phone viewport to a wide desktop, and must survive every width
between rather than only at the breakpoints you pick. Where those fall is yours. At a narrow
viewport nothing overflows sideways: no surface scrolls horizontally, and the hero reel scales to
the column rather than pushing it. Every navigation target stays reachable there, which includes
the rail behind its single control, every row of the index, and the call to action.

### What it must not look like

Not a dashboard. Not a page whose chrome competes with the film. Not decoration standing in for
work. Not a layout borrowed from a subject unrelated to this one.

## Technical requirements

The application is one client-routed document against a JSON API. The index, the case studies and
the booking panel all run without a full page load, which is what lets the single call to action
stay reachable from wherever the visitor is reading.

- Frontend: Vue 3 with Vite.
- Backend: Litestar, serving one JSON API under the `/api` prefix on the same origin.
- Datastore: PostgreSQL, reached through `DATABASE_URL`.
- Mail: Mailpit over real SMTP, reached through `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and
  `SMTP_PASS`.
- Further environment: `AUTH_SECRET`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`.

Both PostgreSQL and Mailpit are already running and reachable at those variables.

The API surface:

| Method and path | Purpose | Auth |
|---|---|---|
| `POST /api/auth/login` | Sign in, returns `access_token` | none |
| `GET /api/session` | The current account | token |
| `GET /api/health` | Readiness | none |
| `GET /api/productions` | All seventeen in index order | none |
| `GET /api/productions/{slug}` | One case study with credits and galleries | none |
| `GET /api/home-feed` | The eleven in home order | none |
| `GET /api/availability` | Published slots carrying no confirmed booking | none |
| `POST /api/holds` | Hold a slot | none |
| `DELETE /api/holds/{id}` | Release a hold | none |
| `POST /api/bookings` | Confirm a held slot | none |
| `GET /api/principal/bookings` | The signed-in principal's bookings | `principal` |
| `POST /api/principal/availability` | Publish a slot | `principal` |
| `POST /api/principal/availability/{id}/withdraw` | Withdraw an untaken slot | `principal` |

A booking request carries its idempotency key in an `Idempotency-Key` header of one to `200`
characters.

Outcomes are reported as: `200` for a read, `201` for a creation, `400` for a malformed body,
`401` for a missing, expired or bad token, `403` for a caller who is authenticated but not
entitled, `404` for an address or identifier that is unknown, `409` for a slot already held or
already booked and for a withdrawal refused by a confirmed booking, `410` for a hold that has
lapsed, and `422` for a value outside its declared range.

The application serves a production build on the container-internal port `4173`, bound to
`0.0.0.0`. Every dependency installs at image build time; there is no network at run time.

## Data model

Eight tables. All timestamps are UTC. **Every table carries its own `id`, the child tables
included**, with no exceptions.

`accounts`: `id`, `email` unique, `display_name`, `role` one of `principal` or `visitor`,
`password_hash`, `timezone`, `created_at`. Three seeded rows as listed under User roles.

`productions`: `id`, `slug` unique, `title`, `client_name`, `category`, `duration_seconds`,
`year`, `sort_index` unique, `featured_on_home`, `home_sort_index` nullable and unique among the
rows that carry one, `status`, `created_at`. `category` is a closed set of seven: `Campaign`,
`Film`, `Documentary`, `Re-Brand`, `Out-of-Home`, `Collaboration`, `Integrated`.

Seventeen seeded rows. The `#` column is `sort_index` and the `Home` column is `home_sort_index`;
a dash means the row carries neither `featured_on_home` nor a `home_sort_index`.

| # | Slug | Title | Client | Category | Seconds | Home |
|---|---|---|---|---|---|---|
| 1 | `tanaka-vertical-mile` | Vertical Mile | Tanaka | `Campaign` | 240 | 1 |
| 2 | `arden-cold-start` | Cold Start | Arden | `Documentary` | 60 | 6 |
| 3 | `norvel-no-quiet-miles` | No Quiet Miles | Norvel | `Film` | 60 | 5 |
| 4 | `pharos-science-endures` | Science Endures | Pharos | `Re-Brand` | 60 | 11 |
| 5 | `kavi-low-priced-groceries` | Improbably Low-Priced Groceries | Kavi | `Campaign` | 30 | 8 |
| 6 | `bout-fight-game` | Shaking Up The Fight Game | Bout | `Campaign` | 60 | 7 |
| 7 | `printwise-unreturnable` | Unreturnable | Printwise | `Campaign` | 47 | - |
| 8 | `norvel-drift` | Drift | Norvel | `Film` | 46 | - |
| 9 | `pawsure-quit-procrastinating` | Quit Procrastinating | PawSure | `Campaign` | 30 | 4 |
| 10 | `fell-rover-ride-harder` | Ride Harder This Winter | Fell Rover | `Campaign` | 30 | 9 |
| 11 | `grillhouse-24-hours` | 24 Hours | Grillhouse | `Out-of-Home` | 72 | - |
| 12 | `norvel-master-the-route` | Master the Route | Norvel | `Campaign` | 60 | 2 |
| 13 | `pulsebody-quiet-in-the-din` | Quiet In The Din | Pulsebody | `Film` | 30 | 3 |
| 14 | `kopje-gold-marked-by-courage` | Marked By Courage | Kopje Gold | `Collaboration` | 120 | 10 |
| 15 | `nord-loan` | Loan | Nord | `Integrated` | 166 | - |
| 16 | `tanaka-stagger-wagon` | Stagger Wagon | Tanaka | `Campaign` | 149 | - |
| 17 | `tanaka-steppe-space-shuttle` | Steppe Space Shuttle | Tanaka | `Campaign` | 50 | - |

Read in `home_sort_index` order, the home feed therefore runs Vertical Mile, Master the Route,
Quiet In The Din, Quit Procrastinating, No Quiet Miles, Cold Start, Shaking Up The Fight Game,
Improbably Low-Priced Groceries, Ride Harder This Winter, Marked By Courage, Science Endures.

`production_galleries`: `id`, `production_id` referencing `productions`, `label`, `title`,
`sort_index`. Two seeded rows per production, labelled `[S.01]` and `[S.02]`.

`gallery_images`: `id`, `gallery_id` referencing `production_galleries`, `caption`, `sort_index`.
Three seeded rows per gallery. `caption` is required in the stored data; a row with no caption
cannot be written.

`production_credits`: `id`, `production_id` referencing `productions`, `role`, `person_name`,
`sort_index`. Four seeded rows per production.

`availability_slots`: `id`, `principal_id` referencing `accounts`, `starts_at`, `ends_at`,
`state` one of `published` or `withdrawn`, `created_at`. Every slot runs fifteen minutes.
Sixteen seeded rows, all `published`: four on each of `2026-10-05` and `2026-10-06` for
`dara@tallow.agency`, and four on each of `2026-10-07` and `2026-10-08` for
`otis@tallow.agency`, beginning at `14:00`, `14:15`, `14:30` and `14:45` UTC on each of those
days.

`slot_holds`: `id`, `slot_id` referencing `availability_slots`, `fingerprint`, `expires_at`,
`created_at`. Not seeded.

`bookings`: `id`, `slot_id` unique referencing `availability_slots`, `principal_id`,
`attendee_name`, `attendee_email`, `attendee_timezone`, `agenda`, `status` one of `confirmed` or
`cancelled`, `idempotency_key` unique, `created_at`. One seeded row: the `2026-10-05` `14:00`
slot with Dara Okonjo, confirmed for `Marta Iglesias` at `marta@example.com`.

Invariants that must hold in the stored data rather than only in the code that writes it:

- A `sort_index` is unique across productions, and a `home_sort_index` is unique among the rows
  carrying one.
- A production carries a `home_sort_index` if and only if it carries `featured_on_home`.
- A gallery image always carries a caption.
- At most one `confirmed` booking exists for any slot, whatever order two requests arrive in.
- A live hold and a confirmed booking never both exist for one slot.
- An `idempotency_key` appears at most once across all bookings.
- A slot carrying a confirmed booking is never in state `withdrawn`.

## Constraints

- Single tenancy. One agency, two principals, one set of work.
- No visitor accounts, no public signup, no password reset, no invitation, no account deletion.
- No cart, no payment, no pricing.
- No comments, no likes, no reactions, no search, no tag pages, no newsletter, no messaging
  beyond the one confirmation described above.
- No rescheduling and no cancellation by the visitor. A booking, once confirmed, is changed only
  by the agency and never silently.
- No crew operations, no day rates, no availability for anyone but the two principals.
- No awards detail rows and no client roster page.
- No transcode pipeline, no signed media addresses, no upload of any kind. Every still and every
  reel is seeded.
- No cookie consent surface and no analytics.
- No audit trail and no outbox.
- No second theme. The product ships one appearance.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
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
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

## Definition of done

- A signed-out visitor reads seventeen numbered productions at `/work`, flips between grid and
  list with the membership and order unchanged, and opens `norvel-drift` to read its credits and
  its captioned galleries.
- The home feed returns eleven productions beginning Vertical Mile, Master the Route, Quiet In
  The Din, and that order is stored separately from the index order rather than derived from it.
- A signed-out visitor holds a published slot, sees a countdown, confirms, and lands on a
  confirmation naming the principal and the time.
- The attendee address holds exactly one message whose subject is `Call confirmed: Dara Okonjo`,
  with no cc and no bcc, and a body naming the principal and the start time.
- A second caller holding or booking an already-held slot is refused as a conflict, and the
  details already typed survive the refusal.
- Two simultaneous confirmations of one slot leave exactly one confirmed booking, and the loser
  is refused.
- The same booking request sent twice with one idempotency key leaves one booking.
- Confirming against a lapsed hold is refused as gone.
- `dara@tallow.agency` reads the booking list, withdraws an untaken slot, and is refused when
  withdrawing the slot that carries a confirmed booking.
- `casey@tallow.agency` is denied by the server at every principal endpoint called directly, and
  no row changes.
- A gallery still with no caption cannot be stored.
- Every internal link on every public route resolves, an unknown address reaches the product's
  own not-found page and answers as not found, and a privacy page is reachable from every footer.
- The interface reads as `playful-consumer`: one `energetic` accent on the single call to action
  and nowhere else, a `geometric sans` throughout with one display face for the largest type,
  and a `springy` settle on the booking confirmation alone.
- Reduced-motion visitors get the whole product with every transition removed.
- Contrast clears WCAG AA on body text and labels against every ground, every control is
  reachable and visibly focused under keyboard navigation, and every still carries its caption.
- The layout holds at every viewport width from a narrow phone to a wide desktop, and nothing
  overflows sideways at the narrow end.
