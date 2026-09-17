# Checklist: The Line Studio

Items: 181
Unpinned values flagged: 6
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` A public catalogue of the studio's directed films is the product's primary surface `src: Overview`
- [ ] `C-OV-02` `capability` A visitor reaches any readable film in two interactions from any route `src: Overview`
- [ ] `C-OV-03` `capability` An editorial back office exists where staff draft, review, schedule, embargo, publish every public record `src: Overview`
- [ ] `C-OV-04` `constraint` A visitor needs no account to browse, to filter, to read, to search `src: Overview`
- [ ] `C-OV-05` `capability` A customer account exists so a buyer returns to re-download a purchase `src: Overview`
- [ ] `C-OV-06` `constraint` No client portal exists where a client reviews work in progress `src: Overview`
- [ ] `C-OV-07` `constraint` No comments, no likes, no follower graph, no visitor-to-visitor messaging exist `src: Overview`
- [ ] `C-OV-08` `capability` Record state, embargo instant, rights window, client naming permission are applied inside the query selecting records `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A Visitor role browses the catalogue, filters, opens a case study, reads the feed, plays a podcast preview, searches `src: User roles`
- [ ] `C-RL-02` `role` A Visitor is refused every draft, scheduled, embargoed, expired, archived, confidential record at every address `src: User roles`
- [ ] `C-RL-03` `role` A Customer buys a product, sees their own orders, downloads what the same customer owns `src: User roles`
- [ ] `C-RL-04` `role` A Customer is refused another customer's order, entitlement, download, shipment under any identifier `src: User roles`
- [ ] `C-RL-05` `role` An Editor creates, updates, reads drafts of case studies, articles, slate entries, episodes, jobs `src: User roles`
- [ ] `C-RL-06` `role` An Editor is refused publish, unpublish, schedule, reorder, embargo, delete `src: User roles`
- [ ] `C-RL-07` `role` A Publisher reorders, publishes, unpublishes, schedules, sets an embargo `src: User roles`
- [ ] `C-RL-08` `role` A Publisher is refused lifting an embargo early `src: User roles`
- [ ] `C-RL-09` `role` A Publisher is refused publishing a record the same Publisher authored `src: User roles`
- [ ] `C-RL-10` `role` A Producer changes a rights window, changes a client naming permission, merges two people, deletes a record `src: User roles`
- [ ] `C-RL-11` `role` A Shopkeeper manages products, versions, drops, stock, fulfilment, refunds, entitlements `src: User roles`
- [ ] `C-RL-12` `role` An Owner lifts an embargo early, manages staff accounts, exports the subscriber list `src: User roles`
- [ ] `C-RL-13` `contract` Authorization is enforced server-side on every mutating endpoint, leaving protected state unchanged on refusal `src: User roles`
- [ ] `C-RL-14` `literal` Every seeded account signs in with the password `deku-demo-pw-2026` `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` Sign-in exchanges an email plus a password for a bearer token carrying an expiry `src: Core features`
- [ ] `C-CF-02` `capability` An expired bearer token is refused, with nothing written `src: Core features`
- [ ] `C-CF-03` `constraint` No public route carries a staff sign-in control `src: Core features`
- [ ] `C-CF-04` `constraint` A staff credential presented to a public route handler is refused `src: Core features`
- [ ] `C-CF-05` `capability` A wrong password is rejected without naming which half was wrong `src: Core features`
- [ ] `C-CF-06` `capability` The response to a sign-in link request is identical for a known address, for an unknown address `src: Core features`
- [ ] `C-CF-07` `literal` The catalogue header prints the live total `[ 6 ]` on seeded data `src: Core features`
- [ ] `C-CF-08` `literal` The facet control prints `All [ 6 ]`, `Branded [ 3 ]`, `Entertainment [ 3 ]` `src: Core features`
- [ ] `C-CF-09` `contract` The total, every facet count, the list itself derive from one predicate `src: Core features`
- [ ] `C-CF-10` `capability` Publishing a film raises the total, raises the same film's facet count `src: Core features`
- [ ] `C-CF-11` `capability` Embargoing a film lowers the total, lowers the same film's facet count `src: Core features`
- [ ] `C-CF-12` `capability` Facet options derive from types present on readable case studies, never from a fixed list `src: Core features`
- [ ] `C-CF-13` `literal` The facet `All` is first, carrying the total `src: Core features`
- [ ] `C-CF-14` `literal` Choosing a facet rewrites the address to `/work?type=branded` `src: Core features`
- [ ] `C-CF-15` `capability` Choosing a facet re-renders the grid without reloading the route `src: Core features`
- [ ] `C-CF-16` `capability` A filtered catalogue survives a reload, survives a back navigation `src: Core features`
- [ ] `C-CF-17` `contract` A persisted row matches what the catalogue displayed, surviving a reload `src: Core features`
- [ ] `C-CF-18` `capability` An unknown facet value falls back to all films with a message, never an error page `src: Core features`
- [ ] `C-CF-19` `constraint` Facets are exclusive; an address requesting two facets takes the first `src: Core features`
- [ ] `C-CF-20` `literal` Two view modes exist, `Grid` plus `List`, toggled by a floating control `src: Core features`
- [ ] `C-CF-21` `capability` The chosen view mode persists across route changes, across reloads, without a server round trip `src: Core features`
- [ ] `C-CF-22` `contract` The current view mode is carried in a stable machine-readable attribute on the grid container `src: Core features`
- [ ] `C-CF-23` `capability` Default ordering is publication date newest first, overridden by an editor-set manual position `src: Core features`
- [ ] `C-CF-24` `capability` Ordering is stable: two films sharing a date break the tie on identity `src: Core features`
- [ ] `C-CF-25` `literal` A tile prints the labels `Type` plus `Director` with the value after a slash `src: Core features`
- [ ] `C-CF-26` `capability` A tile identity counts from `01` within the current ordering, so a filtered catalogue renumbers `src: Core features`
- [ ] `C-CF-27` `capability` A film with several directors lists all of them, each linking to a filtered catalogue `src: Core features`
- [ ] `C-CF-28` `constraint` A film with no director recorded renders no director row, cannot be published `src: Core features`
- [ ] `C-CF-29` `literal` An empty facet renders `No films under <TYPE> yet.` with a control returning to all films `src: Core features`
- [ ] `C-CF-30` `contract` Every media box is laid out at final size, filled before media arrives, so nothing reflows `src: Core features`
- [ ] `C-CF-31` `contract` Every film is fully written into the markup with title, with synopsis, readable without scripting `src: Core features`
- [ ] `C-CF-32` `constraint` No route requests a video byte before its own content has painted `src: Core features`
- [ ] `C-CF-33` `capability` Duration is stored in seconds, rendered `M:SS` under an hour, rendered `H:MM:SS` above an hour `src: Core features`
- [ ] `C-CF-34` `constraint` A record whose poster job has not completed cannot be published `src: Core features`
- [ ] `C-CF-35` `contract` One media source plays at a time across video, across audio `src: Core features`
- [ ] `C-CF-36` `capability` A case study hero prints frame rate, type, running time, month, year `src: Core features`
- [ ] `C-CF-37` `capability` Director values link to a filtered catalogue; client values are plain text `src: Core features`
- [ ] `C-CF-38` `data` Case study modules are an ordered mixed sequence drawn from a closed set of kinds `src: Core features`
- [ ] `C-CF-39` `constraint` A module payload failing its validation is refused at the write, never skipped at render `src: Core features`
- [ ] `C-CF-40` `capability` Crew renders from the people directory, so a name correction propagates everywhere `src: Core features`
- [ ] `C-CF-41` `literal` Credits print in the industry order beginning `Director`, `Producer`, `Production Manager` `src: Core features`
- [ ] `C-CF-42` `literal` `Halle Brandt` is absent from the squad list, still credited on her films `src: Core features`
- [ ] `C-CF-43` `capability` The onward link goes to the next film inside the filter the visitor arrived under `src: Core features`
- [ ] `C-CF-44` `capability` The onward link wraps to the first film when the current film is last `src: Core features`
- [ ] `C-CF-45` `contract` The publication gate returns every failure at once, never only the first `src: Core features`
- [ ] `C-CF-46` `constraint` Publication requires a director credit, an existing type, a positive duration, a poster, alternative text `src: Core features`
- [ ] `C-CF-47` `capability` An Editor moves a record to review; a Publisher then publishes, schedules, returns to draft with a note `src: Core features`
- [ ] `C-CF-48` `contract` An embargoed record answers at its own address exactly as an address that never existed `src: Core features`
- [ ] `C-CF-49` `contract` An embargoed record is absent from the list, the counts, the home route, the search results, the machine index `src: Core features`
- [ ] `C-CF-50` `capability` The onward link of an embargoed record's neighbour resolves past the embargoed record `src: Core features`
- [ ] `C-CF-51` `capability` An embargoed record stays visible in the back office, marked, carrying its lift instant `src: Core features`
- [ ] `C-CF-52` `constraint` A record past its rights end is publicly unreadable, undeleted, visible in the back office `src: Core features`
- [ ] `C-CF-53` `contract` A withheld client name appears in no response field for that film `src: Core features`
- [ ] `C-CF-54` `contract` A mutation commits with its editorial log row, or neither commits `src: Core features`
- [ ] `C-CF-55` `constraint` The editorial log is append-only: no update, no delete `src: Core features`
- [ ] `C-CF-56` `capability` A stale record version is refused as a conflict, returning the current record `src: Core features`

- [ ] `C-CF-57` `capability` Every content image carries alternative text; a decorative image declares itself decorative `src: Core features`
- [ ] `C-CF-58` `capability` Every internal link on every public route resolves `src: Core features`
- [ ] `C-CF-59` `capability` Every public route declares its own social preview image, which resolves `src: Core features`
- [ ] `C-CF-60` `constraint` A form submitted repeatedly in quick succession is refused rather than served `src: Core features`
- [ ] `C-CF-61` `capability` A terms page is reachable from the footer of every public route `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `literal` The route `/work` serves the catalogue with its facet control, its counts `src: User flow`
- [ ] `C-UF-02` `literal` The route `/work/<slug>` serves a case study `src: User flow`
- [ ] `C-UF-03` `literal` The routes `/entertainment`, `/about`, `/blog`, `/podcast`, `/shop`, `/contact` each serve their surface `src: User flow`
- [ ] `C-UF-04` `literal` The routes `/privacy`, `/terms`, `/storage` serve the three documents `src: User flow`
- [ ] `C-UF-05` `literal` The route `/account` serves a customer's own orders, entitlements, downloads `src: User flow`
- [ ] `C-UF-06` `literal` The route `/studio` serves the back office to staff `src: User flow`
- [ ] `C-UF-07` `constraint` Site credits open as an overlay carrying no address, no history entry `src: User flow`
- [ ] `C-UF-08` `capability` An unauthenticated request for `/account` reaches the customer sign-in, returning afterwards `src: User flow`
- [ ] `C-UF-09` `capability` A staff command outside a role leaves the underlying database row unchanged `src: User flow`
- [ ] `C-UF-10` `capability` A slug in the redirect table issues a permanent redirect, never the not-found page `src: User flow`
- [ ] `C-UF-11` `capability` An unknown address renders the product's own not-found page with three routes back to the catalogue `src: User flow`
- [ ] `C-UF-12` `capability` Every asynchronous surface resolves to one of six states: reserved, skeleton, partial, settled, empty, failed `src: User flow`
- [ ] `C-UF-13` `capability` A container empty by structure does not render; a container empty for now renders a message `src: User flow`
- [ ] `C-UF-14` `literal` A count failing to compute renders `[ ]`, never `0` `src: User flow`
- [ ] `C-UF-15` `capability` A failing module renders its own failed state, leaving the rest of the route alive `src: User flow`
- [ ] `C-UF-16` `ui` Every outcome, every staleness notice, every outage renders as an inline banner in place `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The default ground on every route is a near-white neutral sheet `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The signal is a light, vivid red marking the current route, the live dot, the active facet, the full-bleed panel, the reserved media box `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The signal colour appears nowhere beyond the surfaces named for the signal `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Body text meets WCAG AA contrast against its background on every route `src: UI/UX notes`
- [ ] `C-UX-05` `literal` Type is one variable family, `Inter`, carrying a continuous axis covering 300 to 500 `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Every display line height is `0.8` of its size across all three display steps `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Motion character is eased: movement covers most of its distance at once, settling afterwards `src: UI/UX notes`
- [ ] `C-UX-08` `constraint` No looping decorative animation exists anywhere in the product `src: UI/UX notes`
- [ ] `C-UX-09` `ui` A leading dot scales up from nothing when its item becomes current, never fading in `src: UI/UX notes`
- [ ] `C-UX-10` `ui` A section enters once at a threshold, never leaving, so scrolling back replays nothing `src: UI/UX notes`
- [ ] `C-UX-11` `constraint` Reduced motion removes smooth scroll, the custom scrollbar, the custom pointer, scroll-driven transforms, text reveals, every autoplay `src: UI/UX notes`
- [ ] `C-UX-12` `ui` The primary navigation carries eight items in one fixed order, repeated by the footer in the same order `src: UI/UX notes`
- [ ] `C-UX-13` `ui` At a narrow viewport nothing overflows sideways, with every navigation target reachable `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `constraint` Every icon is inline geometry; no icon font, no icon file ships `src: Front-end specification`
- [ ] `C-FE-02` `ui` The crop-mark overlay prints three concentric labelled rectangles plus an aspect-ratio bracket `src: Front-end specification`
- [ ] `C-FE-03` `contract` The crop-mark overlay is decorative, hidden from assistive technology `src: Front-end specification`
- [ ] `C-FE-04` `contract` A separator slash is a real character in a real element, never a border, never a pseudo-element `src: Front-end specification`
- [ ] `C-FE-05` `ui` A separator slash is hidden from assistive technology `src: Front-end specification`
- [ ] `C-FE-06` `contract` The machine-readable hooks listed in the brief appear exactly as written `src: Front-end specification`
- [ ] `C-FE-07` `ui` The header is fixed at every width, never hiding on scroll, never shrinking `src: Front-end specification`
- [ ] `C-FE-08` `ui` The header location fades out to reveal the contact address on hover, on focus, unconditionally on a coarse pointer `src: Front-end specification`
- [ ] `C-FE-09` `ui` The navigation overlay moves focus to its close control, traps focus, returns focus to the toggle `src: Front-end specification`
- [ ] `C-FE-10` `ui` The footer is uncovered from behind the page as the last section scrolls off `src: Front-end specification`
- [ ] `C-FE-11` `ui` The shop is a fixed two-panel composition at desktop, at tablet, stacking at handset `src: Front-end specification`

- [ ] `C-FE-12` `ui` The catalogue prints its live total beside the facet control at the head of the route `src: Front-end specification`
- [ ] `C-FE-13` `ui` Each facet option in the opened list prints its own count beside its label `src: Front-end specification`
- [ ] `C-FE-14` `ui` A catalogue tile prints the label `Type` followed by a slash before the value `src: Front-end specification`
- [ ] `C-FE-15` `ui` The header prints the studio open state beside a dot filled during opening hours `src: Front-end specification`
- [ ] `C-FE-16` `ui` The onward control at the foot of a case study leads to another film of the same type `src: Front-end specification`
- [ ] `C-FE-17` `ui` The catalogue view mode a visitor chooses is the mode shown after a reload `src: Front-end specification`
- [ ] `C-FE-18` `ui` A film tile reserves its media box at full size in the signal red before the media arrives `src: Front-end specification`
- [ ] `C-FE-19` `ui` The shop presents its digital products as a scattered pile holding one arrangement across visits `src: Front-end specification`
- [ ] `C-FE-20` `ui` A facet with an empty result shows a message naming the type beside a control back to every film `src: Core features`
- [ ] `C-FE-21` `ui` An unresolved count prints as an empty bracket pair `src: User flow`
- [ ] `C-FE-22` `ui` The podcast archive groups its episodes under a season heading, newest season first `src: Front-end specification`
- [ ] `C-FE-23` `ui` An embargoed film is absent from the catalogue tiles a visitor sees `src: Core features`
- [ ] `C-FE-24` `ui` An unknown facet value keeps the catalogue on screen with a message `src: Core features`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The datastore is `PostgreSQL`, reached at `DATABASE_URL` from the environment `src: Technical requirements`
- [ ] `C-TR-02` `contract` Every public route renders its content on the server before media attaches `src: Technical requirements`
- [ ] `C-TR-03` `literal` The app reads `APP_PUBLIC_URL` plus `APP_PUBLIC_PORT` from the environment, hardcoding neither `src: Technical requirements`
- [ ] `C-TR-04` `contract` A request identifier is returned to the client in a response header, in every error body `src: Technical requirements`
- [ ] `C-TR-05` `constraint` No credential, no API key, no administrative token appears in anything the browser downloads `src: Technical requirements`
- [ ] `C-TR-06` `contract` Every response carries the standard security headers with a strict transport policy, a no-sniff content-type policy `src: Technical requirements`
- [ ] `C-TR-07` `constraint` No response header, no error body names the framework, the platform, a version, a table, a query `src: Technical requirements`
- [ ] `C-TR-08` `constraint` No route accepts a field named for a card at any depth `src: Technical requirements`
- [ ] `C-TR-09` `constraint` No third-party script loads on any public route `src: Technical requirements`
- [ ] `C-TR-10` `capability` Every asset is generated deterministically from a record seed; no binary ships with the task `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Every amount is an integer in minor units carrying a lowercase currency code `src: Data model`
- [ ] `C-DM-02` `data` No table stores bytes; every media column references the asset table `src: Data model`
- [ ] `C-DM-03` `data` A case study is publicly readable only under the four-part read predicate `src: Data model`
- [ ] `C-DM-04` `data` One entitlement row exists per customer per product, unique `src: Data model`
- [ ] `C-DM-05` `data` Availability is total stock minus sold minus reserved, never below zero `src: Data model`
- [ ] `C-DM-06` `contract` Two simultaneous purchases of the last item produce one acceptance, one refusal `src: Data model`
- [ ] `C-DM-07` `contract` An order submitted twice under one idempotency key produces one order, one entitlement `src: Data model`
- [ ] `C-DM-08` `data` Season plus number identify an episode uniquely `src: Data model`
- [ ] `C-DM-09` `data` A published slug is immutable, leaving a redirect behind on change, never reused `src: Data model`
- [ ] `C-DM-10` `constraint` Deleting a person holding credits is refused `src: Data model`
- [ ] `C-DM-11` `constraint` Deleting a product holding entitlements is refused `src: Data model`
- [ ] `C-DM-12` `data` Every customer-owned row carries its customer identity, filtered inside the selecting query `src: Data model`
- [ ] `C-DM-13` `literal` Nine case studies seed, six publicly readable: `Constellations`, `The Summit`, `Jungle All Stars`, `A Hundred Years of Sweet`, `Mistfall`, `Kerb Kings` `src: Data model`
- [ ] `C-DM-14` `contract` Seeding is idempotent: restarting the app duplicates no row `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One studio exists: no second tenant, no organisation switcher `src: Constraints`
- [ ] `C-CN-02` `constraint` No card details, no payment provider, no externally hosted checkout, no framed payment surface exists `src: Constraints`
- [ ] `C-CN-03` `constraint` No mail delivery happens; enquiries, subscriptions, notifications are stored `src: Constraints`
- [ ] `C-CN-04` `constraint` No object store, no delivery network, no cache tier, no queue broker, no search service exists `src: Constraints`
- [ ] `C-CN-05` `constraint` No third-party analytics, no advertising pixel, no tag manager, no chat widget, no cookie banner exists `src: Constraints`
- [ ] `C-CN-06` `constraint` No external network call happens at runtime `src: Constraints`
- [ ] `C-CN-07` `constraint` No native application, no installable shell, no push notification exists `src: Constraints`
- [ ] `C-CN-08` `constraint` The product stays responsive at a few hundred case studies, a few hundred articles, a few thousand orders `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173` `src: Deployment contract`
- [ ] `C-DC-03` `literal` The HTTP API is served on the same origin under the `/api` prefix `src: Deployment contract`
- [ ] `C-DC-04` `literal` `GET /api/health` returns `200` once the app is ready `src: Deployment contract`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-06` `contract` A production build is served behind a static server, never a dev server `src: Deployment contract`
- [ ] `C-DC-07` `contract` The server keeps running after the session ends, never a child of the shell `src: Deployment contract`
- [ ] `C-DC-08` `literal` The server binds `0.0.0.0`, never `127.0.0.1`, never `localhost` `src: Deployment contract`
- [ ] `C-DC-09` `contract` A list endpoint returns a top-level JSON array `src: Deployment contract`
- [ ] `C-DC-10` `contract` An invalid request is rejected as a client error, never a server error, never a silent success `src: Deployment contract`
- [ ] `C-DC-11` `contract` Bearer authentication is required on everything beyond health, public reads, sign-in `src: Deployment contract`
- [ ] `C-DC-12` `contract` A hidden record produces the same response as a record that never existed, headers included `src: Deployment contract`
- [ ] `C-DC-13` `constraint` An in-memory array, an on-disk file, a hardcoded count standing in for PostgreSQL is a contract violation `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the corpus password | `C-RL-14` |
| `editor@example.com` | the seeded Editor | `C-RL-14` |
| `publisher@example.com` | the seeded Publisher | `C-RL-14` |
| `producer@example.com` | the seeded Producer | `C-RL-14` |
| `shopkeeper@example.com` | the seeded Shopkeeper | `C-RL-14` |
| `owner@example.com` | the seeded Owner | `C-RL-14` |
| `customer@example.com` | the seeded Customer owning one product | `C-RL-14` |
| `customer2@example.com` | the seeded Customer owning nothing | `C-RL-14` |
| `[ 6 ]` | the catalogue total on seeded data | `C-CF-07` |
| `All [ 6 ]` | the All facet with its count | `C-CF-08` |
| `Branded [ 3 ]` | the Branded facet with its count | `C-CF-08` |
| `Entertainment [ 3 ]` | the Entertainment facet with its count | `C-CF-08` |
| `All` | the first facet | `C-CF-13` |
| `/work?type=branded` | the filtered catalogue address | `C-CF-14` |
| `Grid` | the grid view mode | `C-CF-20` |
| `List` | the list view mode | `C-CF-20` |
| `Type` | the tile type label | `C-CF-25` |
| `Director` | the tile director label | `C-CF-25` |
| `01` | the first tile identity in the current ordering | `C-CF-26` |
| `No films under <TYPE> yet.` | the empty facet copy | `C-CF-29` |
| `12` | the attached-video ceiling in the catalogue | `C-CF-34` |
| `M:SS` | the duration format under an hour | `C-CF-33` |
| `H:MM:SS` | the duration format above an hour | `C-CF-33` |
| `Producer` | the second credit role in industry order | `C-CF-41` |
| `Production Manager` | the third credit role in industry order | `C-CF-41` |
| `Halle Brandt` | the departed staff member still credited | `C-CF-42` |
| `/work` | the catalogue route | `C-UF-01` |
| `/work/<slug>` | the case study route | `C-UF-02` |
| `/entertainment` | the slate route | `C-UF-03` |
| `/about` | the studio route | `C-UF-03` |
| `/blog` | the feed route | `C-UF-03` |
| `/podcast` | the podcast route | `C-UF-03` |
| `/shop` | the shop route | `C-UF-03` |
| `/contact` | the contact route | `C-UF-03` |
| `/privacy` | the privacy document route | `C-UF-04` |
| `/terms` | the terms of sale route | `C-UF-04` |
| `/storage` | the storage statement route | `C-UF-04` |
| `/account` | the customer account route | `C-UF-05` |
| `/studio` | the back office route | `C-UF-06` |
| `[ ]` | the honest empty count | `C-UF-14` |
| `0` | the count a failure must never print | `C-UF-14` |
| `Inter` | the one type family | `C-UX-05` |
| `0.8` | the display line-height ratio | `C-UX-06` |
| `Astro` | the frontend framework | `C-TR-01` |
| `Fastify` | the backend framework | `C-TR-02` |
| `PostgreSQL` | the datastore | `C-TR-01` |
| `DATABASE_URL` | the datastore environment variable | `C-TR-01` |
| `APP_PUBLIC_URL` | the public address environment variable | `C-TR-03` |
| `APP_PUBLIC_PORT` | the public port environment variable | `C-TR-03` |
| `Constellations` | the first seeded film | `C-DM-13` |
| `The Summit` | the seeded film whose client may not be named | `C-DM-13` |
| `Jungle All Stars` | a seeded Entertainment film | `C-DM-13` |
| `A Hundred Years of Sweet` | a seeded Branded film | `C-DM-13` |
| `Mistfall` | a seeded Entertainment film | `C-DM-13` |
| `Kerb Kings` | the seeded film also on the slate | `C-DM-13` |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | `C-DC-02` |
| `/api` | the API prefix | `C-DC-03` |
| `GET /api/health` | the health endpoint | `C-DC-04` |
| `200` | the ready health status | `C-DC-04` |
| `/app/USER_README.md` | the credentials file | `C-DC-06` |
| `.browser_screenshots/` | the reserved screenshots directory | `C-DC-07` |
| `.downloads/` | the reserved downloads directory | `C-DC-07` |
| `0.0.0.0` | the bind address | `C-DC-08` |
| `127.0.0.1` | the forbidden loopback bind | `C-DC-08` |
| `localhost` | the forbidden loopback name | `C-DC-08` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the bearer token expiry interval | `C-CF-02` |
| the reserved stock window before a reservation expires | `C-DM-05` |
| the download link lifetime | `C-DM-04` |
| the desktop, tablet, handset threshold widths | `C-UX-13` |
| the first-load ceiling before the preloader dismisses | `C-UF-12` |
| the rate limits per address, per source | `C-CF-06` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 7 | 8 |
| User roles | 3 | 14 |
| Core features | 40 | 61 |
| User flow | 10 | 16 |
| UI and UX notes | 8 | 13 |
| Front-end specification | 11 | 24 |
| Technical requirements | 6 | 10 |
| Data model | 8 | 14 |
| Constraints | 3 | 8 |
| Deployment contract | 12 | 13 |
