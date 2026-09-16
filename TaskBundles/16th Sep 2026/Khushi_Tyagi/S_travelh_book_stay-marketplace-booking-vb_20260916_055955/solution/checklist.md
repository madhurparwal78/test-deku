# Checklist: Havenn

Items: 164
Unpinned values flagged: 6
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The product serves travellers searching for a place to stay plus hosts publishing one, as one application. `src: Overview paragraph 1`
- [ ] `C-OV-02` `capability` The category bar offers four inventory kinds, with a full booking flow built only for stays. `src: Overview paragraph 1`
- [ ] `C-OV-03` `constraint` The application makes no network call at run time to any outside service. `src: Overview paragraph 4`

## C-RL User roles

- [ ] `C-RL-01` `role` An anonymous visitor may browse, search, open a listing, read published reviews, read the terms page. `src: User roles table`
- [ ] `C-RL-02` `role` An anonymous visitor is refused any reservation, message, review, wishlist, exact address. `src: User roles table`
- [ ] `C-RL-03` `role` A signed-in guest reserves, cancels, messages, wishlists, reviews a completed stay. `src: User roles table`
- [ ] `C-RL-04` `role` A guest requesting another guest's reservation, thread, wishlist, receipt is refused by the server. `src: User roles table`
- [ ] `C-RL-05` `role` A guest requesting any host-only endpoint is refused by the server, leaving the protected row unchanged. `src: User roles table`
- [ ] `C-RL-06` `role` A host reads plus writes only their own listings, calendars, reservations, payouts. `src: User roles table`
- [ ] `C-RL-07` `role` A host requesting another host's listing, calendar, reservation, payout is refused by the server. `src: User roles table`
- [ ] `C-RL-08` `role` Signup is open, any visitor may create a guest account, any signed-in account may create a host profile. `src: User roles signup policy`
- [ ] `C-RL-09` `literal` Four accounts are seeded: `guest@example.com`, `guest2@example.com`, `host@example.com`, `host2@example.com`. `src: User roles seeded accounts`
- [ ] `C-RL-10` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles seeded accounts`

## C-CF Core features

- [ ] `C-CF-01` `capability` `POST /api/auth/signup` creates a guest account, returning a bearer token. `src: Core features rule 1`
- [ ] `C-CF-02` `capability` A signup reusing an existing address is refused as invalid, creating no second account. `src: Core features rule 1`
- [ ] `C-CF-03` `capability` `POST /api/auth/login` returns a bearer token for a seeded address with the corpus password. `src: Core features rule 2`
- [ ] `C-CF-04` `capability` A login with a wrong password is denied, returning no token. `src: Core features rule 2`
- [ ] `C-CF-05` `capability` Every endpoint other than signup, login, health, the payment webhook refuses a request carrying no bearer token. `src: Core features rule 3`
- [ ] `C-CF-06` `capability` The search control carries three segments labelled `Where`, `When`, `Who`, over one submit. `src: Core features Search`
- [ ] `C-CF-07` `capability` Every search parameter lives in the address, so a copied address reproduces the same results. `src: Core features rule 4`
- [ ] `C-CF-08` `capability` Guests are counted as four separate classes: adults, children, infants, pets. `src: Core features rule 5`
- [ ] `C-CF-09` `capability` An infant counts toward neither occupancy nor the extra-guest threshold. `src: Core features rule 5`
- [ ] `C-CF-10` `capability` A pet charges one fee per stay, being refused on a listing disallowing pets. `src: Core features rule 5`
- [ ] `C-CF-11` `capability` `GET /api/listings` answers a conjunction of geography, availability, attributes, total price. `src: Core features rule 6`
- [ ] `C-CF-12` `capability` The bounding box is authoritative over the place name, so moving the map changes the address. `src: Core features rule 6`
- [ ] `C-CF-13` `capability` A bounding box crossing the antimeridian returns the listings inside a two-degree span. `src: Core features rule 6`
- [ ] `C-CF-14` `capability` Availability is answered inside the query, so a dense area returns a full page in one round trip. `src: Core features rule 7`
- [ ] `C-CF-15` `capability` Pagination is by opaque `cursor`, never by offset. `src: Core features rule 8`
- [ ] `C-CF-16` `capability` A cursor issued against a different query is refused as invalid. `src: Core features rule 8`
- [ ] `C-CF-17` `capability` Booking a listing above the page-one boundary leaves page two neither hiding nor repeating a result. `src: Core features rule 8`
- [ ] `C-CF-18` `capability` Search renders four distinct states: no results, over-narrow filters, component unavailable, partial. `src: Core features rule 9`
- [ ] `C-CF-19` `capability` A map pin's label carries the total for the queried dates, never the nightly rate. `src: Core features rule 10`
- [ ] `C-CF-20` `capability` The booking panel itemises the whole price before the guest commits. `src: Core features rule 11`
- [ ] `C-CF-21` `capability` With no dates chosen the panel shows a from-price, showing no total. `src: Core features rule 12`
- [ ] `C-CF-22` `capability` The availability view carries three states per date, the third being bookable but not as an arrival. `src: Core features rule 13`
- [ ] `C-CF-23` `capability` Instant book confirms on authorisation, request to book creates a pending hold instead. `src: Core features rule 14`
- [ ] `C-CF-24` `capability` The cancellation policy, house rules, total, rating sit above the booking control. `src: Core features rule 15`
- [ ] `C-CF-25` `data` The nightly subtotal sums each date's own price across the half-open range. `src: Core features rule 16`
- [ ] `C-CF-26` `data` The length-of-stay discount reduces the nightly subtotal alone, never a fee, never a tax. `src: Core features rule 17`
- [ ] `C-CF-27` `data` The cleaning fee is charged once per stay, identical on a two-night stay or a thirty-night stay. `src: Core features rule 18`
- [ ] `C-CF-28` `data` The extra-guest fee is charged per extra guest per night. `src: Core features rule 18`
- [ ] `C-CF-29` `data` The guest service fee is a rate over the accommodation total. `src: Core features rule 19`
- [ ] `C-CF-30` `data` Tax comes from a stored jurisdiction table, dropping to zero at a jurisdiction's exemption threshold. `src: Core features rule 20`
- [ ] `C-CF-31` `data` The pricing steps run in one fixed order, producing named intermediate totals nobody displays. `src: Core features rule 21`
- [ ] `C-CF-32` `data` Rounding is half up, away from zero, at every multiplication, so displayed lines sum exactly to the displayed total. `src: Core features rule 22`
- [ ] `C-CF-33` `capability` A quote pins its inputs for a lifetime read from `QUOTE_TTL_SEC`, being consumed once. `src: Core features rule 23`
- [ ] `C-CF-34` `data` A stay is a half-open range of local dates, so the third to the fifth is two nights. `src: Core features rule 24`
- [ ] `C-CF-35` `data` A departure date may equal another guest's arrival date on one listing. `src: Core features rule 24`
- [ ] `C-CF-36` `data` Simultaneous confirms for one listing over one range leave exactly one reservation stored. `src: Core features rule 25`
- [ ] `C-CF-37` `data` A losing confirm leaves no orphan row, no held night, no authorisation. `src: Core features rule 25`
- [ ] `C-CF-38` `capability` Six availability rules plus advance notice plus the availability window all gate a range. `src: Core features rule 26`
- [ ] `C-CF-39` `capability` An expired pending hold stops counting against availability with nothing having read the reservation. `src: Core features rule 27`
- [ ] `C-CF-40` `capability` `POST /api/maintenance/release-expired-holds` is idempotent, releasing each authorisation. `src: Core features rule 27`
- [ ] `C-CF-41` `data` A reservation stores a copy of the cancellation policy, so a later policy edit leaves the terms unchanged. `src: Core features rule 28`
- [ ] `C-CF-42` `capability` The refund quote is computed from the stored policy against the listing's local time, being shown before confirmation. `src: Core features rule 29`
- [ ] `C-CF-43` `capability` Checkout re-prices plus re-checks availability on arrival, surfacing any difference for fresh consent. `src: Core features rule 30`
- [ ] `C-CF-44` `capability` A replayed `Idempotency-Key` returns the original result, creating no second reservation, no second authorisation. `src: Core features rule 31`
- [ ] `C-CF-45` `capability` Five named checkout failures each have their own path, with an unwritable reservation voiding the authorisation. `src: Core features rule 32`
- [ ] `C-CF-46` `capability` Before confirming, the guest sees the charged currency named in words. `src: Core features rule 33`
- [ ] `C-CF-47` `capability` Request to book authorises at confirmation, capturing only on host acceptance. `src: Core features rule 34`
- [ ] `C-CF-48` `capability` Inventory is arbitrated before any authorisation is attempted. `src: Core features rule 35`
- [ ] `C-CF-49` `data` Listing currency, display currency, settlement currency stay three separate values, with the rate stored on the reservation. `src: Core features rule 36`
- [ ] `C-CF-50` `capability` A payment needing an interactive challenge answers `requires_action`, holding inventory under a short deadline. `src: Core features rule 37`
- [ ] `C-CF-51` `capability` Payment events are applied by their own timestamps, idempotently on the event id, never by arrival order. `src: Core features rule 38`
- [ ] `C-CF-52` `data` A payout follows the check-in date in the listing's timezone, becoming eligible after a hold period. `src: Core features rule 39`
- [ ] `C-CF-53` `data` A partial refund is computed from the policy snapshot, itemised, stored. `src: Core features rule 40`
- [ ] `C-CF-54` `capability` `/trips` groups reservations as upcoming, current, past. `src: Core features rule 41`
- [ ] `C-CF-55` `capability` Contact details in a message before confirmation are redacted on the server, on write plus on read. `src: Core features rule 42`
- [ ] `C-CF-56` `data` A wishlist item stores the listing plus the dates the listing was saved under. `src: Core features rule 43`
- [ ] `C-CF-57` `capability` Neither review is published until both are submitted or the window closes. `src: Core features rule 44`
- [ ] `C-CF-58` `capability` An unpublished review never leaves the server to anyone other than the author. `src: Core features rule 44`
- [ ] `C-CF-59` `data` Rating aggregates count published reviews only, averaging six subratings independently. `src: Core features rule 45`
- [ ] `C-CF-60` `capability` Language, region, display currency are three independent account settings. `src: Core features rule 46`
- [ ] `C-CF-61` `data` A listing's approximate circle is offset by a stored vector, stable across every visit. `src: Core features rule 47`
- [ ] `C-CF-62` `capability` Exact coordinates reach only the confirmed reservation's guest plus the listing's host. `src: Core features rule 47`
- [ ] `C-CF-63` `capability` The accept-or-decline screen shows no guest photograph, no guest name. `src: Core features rule 48`
- [ ] `C-CF-64` `data` Reservations, payments, payouts, refunds, cancellations are append-only, so a correction is a new row. `src: Core features rule 50`
- [ ] `C-CF-65` `capability` Unpublishing a listing leaves existing reservations untouched. `src: Core features rule 51`
- [ ] `C-CF-66` `capability` A calendar edit appears in the row at once, reverting with a message naming the field on a failed save. `src: Core features rule 52`
- [ ] `C-CF-67` `capability` A late imported block over confirmed nights raises a conflict for a person, auto-cancelling nothing. `src: Core features rule 53`
- [ ] `C-CF-68` `capability` Accepting a request captures the authorisation, declining voids the authorisation, freeing the nights. `src: Core features rule 54`
- [ ] `C-CF-69` `capability` `/host/earnings` lists scheduled payouts, released payouts, outstanding recoveries. `src: Core features rule 55`
- [ ] `C-CF-70` `contract` The home route title reads Havenn, a vertical bar, then Holiday rentals, cabins, beach houses & more. `src: Core features rule 56`
- [ ] `C-CF-71` `literal` The skip link reads `Skip to content`, the home heading reads `Havenn homepage`. `src: Core features rule 56`
- [ ] `C-CF-72` `literal` The link grid is headed `Inspiration for future getaways`, carrying six named tabs plus `Show more`. `src: Core features rule 57`
- [ ] `C-CF-73` `capability` The link grid is present in the markup the server sends, so a crawler reads the grid. `src: Core features rule 57`
- [ ] `C-CF-74` `literal` An unknown address renders the not-found view carrying `Oops!`, `Error code: 404`, seven named links. `src: Core features rule 58`
- [ ] `C-CF-75` `literal` The server-error view carries `Error code: 500` plus the escalation naming the ongoing-reservation case. `src: Core features rule 58`
- [ ] `C-CF-76` `capability` A terms page at `/terms` is reachable from every footer, linked from the signup form. `src: Core features rule 59`

## C-UF User flow

- [ ] `C-UF-01` `capability` Twenty-three routes exist exactly as the route table names them. `src: User flow route table`
- [ ] `C-UF-02` `capability` An anonymous visitor opening a protected route is sent to sign-in, returning afterwards to the requested route. `src: User flow entry and redirects`
- [ ] `C-UF-03` `capability` An expired token mid-action leaves the action unperformed, asking for sign-in again. `src: User flow entry and redirects`
- [ ] `C-UF-04` `capability` The search-then-reserve journey ends with the reservation under `/trips` plus the nights gone from availability. `src: User flow journeys`
- [ ] `C-UF-05` `capability` The request-to-book journey ends with a pending reservation whose money is authorised, uncaptured. `src: User flow journeys`
- [ ] `C-UF-06` `capability` Every list carries an empty state naming what would fill the list. `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The subject, a place to stay, is the first thing seen on every browsing surface. `src: UI/UX notes north star`
- [ ] `C-UX-02` `ui` Surfaces where a guest is deciding stay still, with nothing moving during the decision. `src: UI/UX notes register`
- [ ] `C-UX-03` `ui` The palette is stated by role, with three meaning-carrying colours used for nothing else. `src: UI/UX notes palette`
- [ ] `C-UX-04` `ui` The brand colour belongs to the search submit alone, appearing far less often than the ink. `src: UI/UX notes brand colour`
- [ ] `C-UX-05` `ui` The search submit carries a six-stop radial glow shifting darker as one ramp when pressed. `src: UI/UX notes brand colour`
- [ ] `C-UX-06` `ui` One size carries the whole interface, with heaviness plus colour doing the work size variation would. `src: UI/UX notes type`
- [ ] `C-UX-07` `ui` Elevation grows in spread, never in darkness, with the flattest step an inset hairline. `src: UI/UX notes shape`
- [ ] `C-UX-08` `ui` Triggered movement settles the way a weighted object settles, sharing one house overshoot. `src: UI/UX notes motion`
- [ ] `C-UX-09` `ui` A request for reduced motion collapses every settle to an instant state change. `src: UI/UX notes motion`
- [ ] `C-UX-10` `ui` Every control carries resting, pointed-at, pressed, focused, unavailable states, with unavailable never signalled by colour alone. `src: UI/UX notes components`
- [ ] `C-UX-11` `ui` Each page leads with one primary action, visually distinct from every secondary one. `src: UI/UX notes components`
- [ ] `C-UX-12` `ui` Body text meets the WCAG AA contrast bar, with the secondary grey never used below body size. `src: UI/UX notes accessibility`
- [ ] `C-UX-13` `ui` Every route is fully operable from the keyboard, with a visible focus ring. `src: UI/UX notes accessibility`
- [ ] `C-UX-14` `ui` At a narrow viewport nothing overflows sideways, with every navigation target still reachable. `src: UI/UX notes responsive`
- [ ] `C-UX-15` `ui` At the narrow width the search control becomes a full-screen panel asking one question at a time. `src: UI/UX notes responsive`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The home route, the search results, the listing detail arrive as server-rendered markup. `src: Technical requirements paragraph 1`
- [ ] `C-TR-02` `contract` The frontend is Remix on React Router 7, the API is Hono, the runtime is Node 20. `src: Technical requirements paragraph 1`
- [ ] `C-TR-03` `contract` The datastore is PostgreSQL, reached at `DATABASE_URL` read from the environment. `src: Technical requirements paragraph 1`
- [ ] `C-TR-04` `constraint` The application reaches exactly one backing service, `postgres`, at `DATABASE_URL`. `src: Technical requirements paragraph 2`
- [ ] `C-TR-05` `contract` `GET /api/health` returns `200` once the application is ready. `src: Technical requirements paragraph 3`
- [ ] `C-TR-06` `capability` Every public route carries a distinct title plus a distinct description. `src: Technical requirements paragraph 4`
- [ ] `C-TR-07` `contract` `PENDING_HOLD_TTL_SEC` plus `QUOTE_TTL_SEC` are read from the environment at run time. `src: Technical requirements paragraph 5`
- [ ] `C-TR-08` `constraint` No credential, key, admin token appears in anything the browser downloads. `src: Technical requirements paragraph 4`
- [ ] `C-TR-09` `constraint` No price arithmetic happens in the browser, the breakdown renderer displaying a server-computed quote. `src: Technical requirements money paragraph`
- [ ] `C-TR-10` `capability` A just-booked listing still in the index opens with an honest message rather than a checkout failure. `src: Technical requirements index paragraph`

## C-DM Data model

- [ ] `C-DM-01` `data` Twenty-three tables exist, with every timestamp in UTC plus every stay date local to the listing. `src: Data model opening`
- [ ] `C-DM-02` `literal` The seeded password `deku-demo-pw-2026` works at login for every seeded account. `src: Data model password paragraph`
- [ ] `C-DM-03` `data` `listing` carries an `inventory_type`, a room type, a capacity, an IANA timezone, a currency, a status. `src: Data model listing`
- [ ] `C-DM-04` `data` `calendar_day` holds one row per listing per open local date, carrying availability plus price plus stay bounds. `src: Data model calendar_day`
- [ ] `C-DM-05` `data` At most one reservation whose status is `pending` or `confirmed` covers any night of any listing. `src: Data model reservation`
- [ ] `C-DM-06` `data` A payment stores no card number, no security code, no bank detail in any column. `src: Data model payment`
- [ ] `C-DM-07` `data` A payment's idempotency key is unique per user, so a replay finds the original row. `src: Data model payment`
- [ ] `C-DM-08` `data` A review row whose `published_at` is empty is readable only by the author. `src: Data model review`
- [ ] `C-DM-09` `literal` Four listings are seeded: `Cedar Loft`, `Harbour Cottage`, `Kite House`, `Salt Marsh Cabin`. `src: Data model seed data`
- [ ] `C-DM-10` `literal` `Salt Marsh Cabin` opens exactly one bookable window, every other night blocked. `src: Data model seed data`
- [ ] `C-DM-11` `data` Three tax jurisdictions cover a percentage shape, an exempting shape, a per-person-per-night shape. `src: Data model seed data`
- [ ] `C-DM-12` `data` Seeding is idempotent, so restarting the application duplicates no row. `src: Data model seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Changing one radius token moves every surface reading the radius token. `src: Front-end specification token layer`
- [ ] `C-FE-02` `ui` Eight corner radii form one ladder, with pill plus circle forms the only shapes outside the ladder. `src: Front-end specification token layer`
- [ ] `C-FE-03` `ui` Six settles are declared as a mass, a stiffness, a damping, so adding a seventh takes three numbers. `src: Front-end specification settles`
- [ ] `C-FE-04` `ui` Three settles arrive without overshoot, three overshoot by the same small amount. `src: Front-end specification settles`
- [ ] `C-FE-05` `ui` The only scrubbed movement is the header's compact transition, with the results grid attaching no per-row animation. `src: Front-end specification scroll`
- [ ] `C-FE-06` `ui` Hover styles apply only where a pointer exists, so a tap leaves no control stuck looking hovered. `src: Front-end specification breakpoints`
- [ ] `C-FE-07` `ui` One visually-hidden idiom clips every description meant to be announced rather than seen. `src: Front-end specification hidden text`
- [ ] `C-FE-08` `ui` Every icon is drawn in the page, with no icon font shipped. `src: Front-end specification iconography`
- [ ] `C-FE-09` `ui` The four category tabs read `All`, `Homes`, `Experiences`, `Services`, in a generously rounded pill form. `src: Front-end specification category tabs`
- [ ] `C-FE-10` `ui` The listing card carries photo, wishlist heart, title, meta, dates, price, rating. `src: Front-end specification listing card`
- [ ] `C-FE-11` `ui` Both error routes carry no header, no footer, no chrome, with the display line the largest type in the product. `src: Front-end specification error pages`
- [ ] `C-FE-12` `ui` Every generated image is deterministic, so rebuilding twice produces identical bytes. `src: Front-end specification generated imagery`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The application is single tenant, with one set of listings, no organisations. `src: Constraints`
- [ ] `C-CN-02` `constraint` No background scheduler runs, so deadline work happens on read or through the maintenance endpoint. `src: Constraints`
- [ ] `C-CN-03` `constraint` Experiences plus services carry an inventory type with a route, carrying no separate booking flow. `src: Constraints`
- [ ] `C-CN-04` `ui` Every image in the product is drawn in the page or generated from a seed, never downloaded as a file. `src: Constraints`
- [ ] `C-CN-05` `constraint` The application stays responsive with a thousand listings plus ten thousand calendar days loaded. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The application is reachable at `APP_PUBLIC_URL`, with the port mapping `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-02` `contract` The HTTP API is served on that same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-03` `contract` `GET /api/health` returns `200` once the application is ready. `src: Deployment contract`
- [ ] `C-DC-04` `contract` The application answers at its public URL with no manual step taken after the image starts. `src: Deployment contract`
- [ ] `C-DC-05` `contract` Every seeded account signs in with the password recorded at `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-06` `contract` The receipt on a confirmed reservation shows the same total the guest agreed to. `src: Deployment contract`
- [ ] `C-DC-07` `contract` A production build is served, so the home route arrives as finished markup rather than an empty shell. `src: Deployment contract`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends, being no child of the shell. `src: Deployment contract`
- [ ] `C-DC-09` `contract` The listener binds `0.0.0.0`, so the application answers from outside its container. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The application reaches `postgres` at its environment variable without starting a copy. `src: Deployment contract`
- [ ] `C-DC-11` `contract` The payment webhook receiver authenticates by signature rather than by a user token. `src: Deployment contract`
- [ ] `C-DC-12` `contract` A plain list endpoint returns a top-level JSON array, the search endpoint returning an object carrying a cursor. `src: Deployment contract API shapes`
- [ ] `C-DC-13` `contract` An invalid, unauthorized, conflicting call is refused as a client error carrying a message naming the reason. `src: Deployment contract API shapes`
- [ ] `C-DC-14` `contract` Bearer auth is required everywhere other than signup, login, health, the signed payment webhook. `src: Deployment contract API shapes`
- [ ] `C-DC-15` `contract` The reservation, the payment, the payout, the review are real rows in `postgres`. `src: Deployment contract No mocks`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `guest@example.com` | the first seeded guest | `C-RL-09` |
| `guest2@example.com` | the second seeded guest | `C-RL-09` |
| `host@example.com` | the first seeded host | `C-RL-09` |
| `host2@example.com` | the second seeded host | `C-RL-09` |
| `deku-demo-pw-2026` | the corpus password | `C-RL-10` |
| `/app/USER_README.md` | the credentials file | `C-DC-05` |
| `Skip to content` | the skip link | `C-CF-71` |
| `Havenn homepage` | the home route heading | `C-CF-71` |
| `Inspiration for future getaways` | the link grid heading | `C-CF-72` |
| `Show more` | the link grid expander | `C-CF-72` |
| `Oops!` | the error display line | `C-CF-74` |
| `Error code: 404` | the not-found code | `C-CF-74` |
| `Error code: 500` | the server-error code | `C-CF-75` |
| `Cedar Loft` | the Portland listing | `C-DM-09` |
| `Harbour Cottage` | the Amsterdam listing | `C-DM-09` |
| `Kite House` | the Kyoto listing | `C-DM-09` |
| `Salt Marsh Cabin` | the contested listing | `C-DM-09` |
| `/terms` | the terms route | `C-CF-76` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the guest service fee rate | `C-CF-29` |
| the host service fee rate | `C-CF-45` |
| the pending hold deadline in hours | `C-CF-37` |
| the review window in days | `C-CF-58` |
| the minimum review count before a rating shows | `C-CF-60` |
| the payout hold period | `C-CF-45` |

## Coverage ledger

| Section | Obligation sentences | Items |
|---|---|---|
| Overview | 1 | 3 |
| User roles | 1 | 10 |
| Core features | 35 | 76 |
| User flow | 5 | 6 |
| UI and UX notes | 9 | 15 |
| Technical requirements | 4 | 10 |
| Data model | 5 | 12 |
| Front-end specification | 10 | 12 |
| Constraints | 3 | 5 |
| Deployment contract | 12 | 15 |
