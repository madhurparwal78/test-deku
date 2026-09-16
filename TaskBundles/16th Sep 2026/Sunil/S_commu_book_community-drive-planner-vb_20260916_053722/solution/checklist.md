# Checklist: Waze Live Map

Items: 188
Unpinned values flagged: 6
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` A visitor opens a full viewport map without an account `src: Overview`
- [ ] `C-OV-02` `capability` Road conditions come from reports filed by drivers rather than from a published schedule `src: Overview`
- [ ] `C-OV-03` `capability` Choosing an arrival time turns a route lookup into a planned drive `src: Overview`
- [ ] `C-OV-04` `capability` The app holds what has already been drawn when the network drops `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor pans the map without an account `src: User roles`
- [ ] `C-RL-02` `role` A visitor searches a starting point without an account `src: User roles`
- [ ] `C-RL-03` `role` A visitor solves for a leave time without an account `src: User roles`
- [ ] `C-RL-04` `role` A visitor cannot file a report `src: User roles`
- [ ] `C-RL-05` `role` A visitor cannot save a planned drive `src: User roles`
- [ ] `C-RL-06` `role` A driver cannot read another driver's planned drive `src: User roles`
- [ ] `C-RL-07` `role` A driver cannot vote on a report the same driver filed `src: User roles`
- [ ] `C-RL-08` `role` Signup is open to anyone with an email address `src: User roles`
- [ ] `C-RL-09` `role` A direct call from a visitor session to a driver-only endpoint leaves the protected state unchanged `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` Signing up with an unregistered email returns a bearer token `src: Core features > Auth rule 1`
- [ ] `C-CF-02` `constraint` Signing up with an already registered email creates no second account `src: Core features > Auth rule 1`
- [ ] `C-CF-03` `capability` Signing in with a seeded email returns a bearer token `src: Core features > Auth rule 2`
- [ ] `C-CF-04` `constraint` A driver-only endpoint called with no token changes nothing `src: Core features > Auth rule 3`
- [ ] `C-CF-05` `capability` The map requests tiles only for the current viewport plus a small margin `src: Core features > The live map surface rule 4`
- [ ] `C-CF-06` `ui` A tile fades in on arrival rather than popping `src: Core features > The live map surface`
- [ ] `C-CF-07` `ui` A stack of circular controls sits at the bottom right of the map `src: Core features > The live map surface rule 5`
- [ ] `C-CF-08` `ui` The coordinate readout shows the map centre as two decimal degree values divided by a vertical bar `src: Core features > The live map surface rule 5`
- [ ] `C-CF-09` `literal` The map meta row carries the link `How suggestions work` `src: Core features > The live map surface rule 6`
- [ ] `C-CF-10` `ui` Report markers draw on a layer above the tiles `src: Core features > The live map surface rule 7`
- [ ] `C-CF-11` `capability` Typing into the starting point field opens ranked suggestions from the seeded place index `src: Core features > Endpoint search rule 8`
- [ ] `C-CF-12` `capability` Place search matches a place name on a case insensitive substring `src: Core features > Endpoint search rule 8`
- [ ] `C-CF-13` `constraint` A place search matching nothing says so rather than showing an empty list `src: Core features > Endpoint search rule 8`
- [ ] `C-CF-14` `capability` A reverse lookup returns the nearest seeded place to a coordinate `src: Core features > Endpoint search rule 9`
- [ ] `C-CF-15` `capability` The swap control exchanges the two resolved endpoints `src: Core features > Endpoint search rule 10`
- [ ] `C-CF-16` `literal` The starting point field carries the placeholder `Choose starting point` `src: Core features > Endpoint search`
- [ ] `C-CF-17` `literal` The destination field carries the placeholder `Choose destination` `src: Core features > Endpoint search`
- [ ] `C-CF-18` `data` A segment carrying two active `jam` reports reads `heavy` `src: Core features > Live road conditions rule 12`
- [ ] `C-CF-19` `data` A segment carrying exactly one active `jam` report reads `slowing` `src: Core features > Live road conditions rule 12`
- [ ] `C-CF-20` `data` A segment carrying one active `closure` report reads `heavy` `src: Core features > Live road conditions rule 12`
- [ ] `C-CF-21` `data` A segment carrying one active `hazard` report reads `slowing` `src: Core features > Live road conditions rule 12`
- [ ] `C-CF-22` `data` A segment carrying no active report reads `clear` `src: Core features > Live road conditions rule 12`
- [ ] `C-CF-23` `ui` A jammed road draws as a dashed line crawling along its own length `src: Core features > Live road conditions rule 13`
- [ ] `C-CF-24` `data` A segment whose only report has expired reads `clear` again `src: Core features > Live road conditions rule 14`
- [ ] `C-CF-25` `capability` The live road conditions answer without a bearer token `src: Core features > Live road conditions rule 14`
- [ ] `C-CF-26` `capability` A signed in driver files a report against one segment `src: Core features > Community reporting rule 15`
- [ ] `C-CF-27` `constraint` A report naming a type outside the nine named types creates no row `src: Core features > Community reporting rule 15`
- [ ] `C-CF-28` `constraint` A report naming a segment that does not exist creates no row `src: Core features > Community reporting rule 15`
- [ ] `C-CF-29` `data` A new report stays fresh for `60 minutes` from the moment of filing `src: Core features > Community reporting rule 15`
- [ ] `C-CF-30` `data` A report past its freshness reads `expired` `src: Core features > Community reporting rule 16`
- [ ] `C-CF-31` `capability` A driver votes `confirm` on another driver's report `src: Core features > Community reporting rule 17`
- [ ] `C-CF-32` `constraint` A second vote from one driver on one report changes nothing `src: Core features > Community reporting rule 17`
- [ ] `C-CF-33` `data` A confirming vote extends freshness to `60 minutes` after the vote `src: Core features > Community reporting rule 18`
- [ ] `C-CF-34` `data` Freshness is capped at `180 minutes` after filing `src: Core features > Community reporting rule 18`
- [ ] `C-CF-35` `data` A disputing vote from a driver of reputation 3 or more counts double `src: Core features > Community reporting rule 19`
- [ ] `C-CF-36` `data` A report reaching dispute strength 2 reads `dismissed` `src: Core features > Community reporting rule 19`
- [ ] `C-CF-37` `data` A dismissed report stops colouring the segment named on the report `src: Core features > Community reporting rule 19`
- [ ] `C-CF-38` `data` Driver reputation counts the driver's own reports that ever drew a confirming vote `src: Core features > Community reporting rule 19`
- [ ] `C-CF-39` `data` A route returns its ordered segments with a total travel time `src: Core features > Routing rule 20`
- [ ] `C-CF-40` `constraint` A route naming an endpoint that does not resolve draws nothing `src: Core features > Routing rule 20`
- [ ] `C-CF-41` `data` A clear segment contributes its free flow time at `100 percent` `src: Core features > Routing rule 21`
- [ ] `C-CF-42` `data` A slowing segment contributes its free flow time at `150 percent` `src: Core features > Routing rule 21`
- [ ] `C-CF-43` `data` A heavy segment contributes its free flow time at `250 percent` `src: Core features > Routing rule 21`
- [ ] `C-CF-44` `data` Each scaled segment time is rounded up to the next whole minute before the sum `src: Core features > Routing rule 21`
- [ ] `C-CF-45` `literal` A route over `Outer Ring Road` then `DND Flyway` has a travel time of `27 minutes` `src: Core features > Routing rule 21`
- [ ] `C-CF-46` `capability` A route accepts an arrival time in place of a departure time `src: Core features > Routing rule 22`
- [ ] `C-CF-47` `capability` A drawn route recalculates when a report changes the road underneath `src: Core features > Routing rule 23`
- [ ] `C-CF-48` `constraint` A faster alternative is offered only when the saving reaches at least `3 minutes` `src: Core features > Routing rule 24`
- [ ] `C-CF-49` `data` An arrival time solves to a leave time of the arrival less the travel time less a `5 minute buffer` `src: Core features > The leave time scheduler rule 25`
- [ ] `C-CF-50` `literal` An arrival time of `2026-09-17T09:00:00Z` over the 27 minute route solves to a leave time of `2026-09-17T08:28:00Z` `src: Core features > The leave time scheduler rule 25`
- [ ] `C-CF-51` `constraint` An arrival time already in the past produces no planned drive `src: Core features > The leave time scheduler rule 26`
- [ ] `C-CF-52` `capability` A visitor solves for a leave time without saving a planned drive `src: Core features > The leave time scheduler rule 27`
- [ ] `C-CF-53` `literal` The coaching tooltip carries the title `Edit your arrival time` `src: Core features > The leave time scheduler`
- [ ] `C-CF-54` `ui` The coaching tooltip carries a dismiss control that closes the tooltip `src: Core features > The leave time scheduler`
- [ ] `C-CF-55` `literal` The scheduler opens from a control labelled `Leave now` `src: Core features > The leave time scheduler`
- [ ] `C-CF-56` `capability` A signed in driver saves a solved result as a planned drive `src: Core features > Planned drives rule 28`
- [ ] `C-CF-57` `data` A saved planned drive starts in the state `scheduled` `src: Core features > Planned drives rule 28`
- [ ] `C-CF-58` `data` A saved planned drive stores the solved travel time `src: Core features > Planned drives rule 28`
- [ ] `C-CF-59` `literal` The reminder falls due at the leave time less a `15 minute lead` `src: Core features > Planned drives rule 29`
- [ ] `C-CF-60` `constraint` A driver lists only planned drives the same driver owns `src: Core features > Planned drives rule 30`
- [ ] `C-CF-61` `constraint` A request for another driver's planned drive leaves the row unchanged `src: Core features > Planned drives rule 30`
- [ ] `C-CF-62` `data` A cancelled planned drive reads `canceled` `src: Core features > Planned drives rule 30`
- [ ] `C-CF-63` `data` A cancelled planned drive holds no departure window `src: Core features > Planned drives rule 30`
- [ ] `C-CF-64` `constraint` A driver holds no two planned drives whose departure windows overlap `src: Core features > Planned drives rule 31`
- [ ] `C-CF-65` `constraint` Two simultaneous requests for overlapping departure windows leave exactly one row `src: Core features > Planned drives rule 31`
- [ ] `C-CF-66` `constraint` A refused planned drive leaves no orphaned row `src: Core features > Planned drives rule 31`
- [ ] `C-CF-67` `data` Two departure windows touching end to start do not overlap `src: Core features > Planned drives rule 31`
- [ ] `C-CF-68` `ui` The map header condenses to a nine dot launcher beside a three dot overflow menu `src: Core features > Global chrome rule 33`
- [ ] `C-CF-69` `literal` The app launcher lists the destination `Wazeopedia` `src: Core features > Global chrome rule 33`
- [ ] `C-CF-70` `literal` The overflow menu lists `Report an issue` `src: Core features > Global chrome rule 33`
- [ ] `C-CF-71` `literal` The marketing header carries the navigation entry `Waze for Cities` `src: Core features > Global chrome rule 34`
- [ ] `C-CF-72` `literal` The footer carries the tagline `Where drivers help drivers` `src: Core features > Global chrome rule 35`
- [ ] `C-CF-73` `literal` The footer carries the line `© 2006 - 2026 Waze Mobile. All Rights Reserved.` `src: Core features > Global chrome rule 35`
- [ ] `C-CF-74` `literal` The footer column `Live Map` lists `Plan a drive` `src: Core features > Global chrome rule 35`
- [ ] `C-CF-75` `literal` The language selector defaults to `English` `src: Core features > Global chrome rule 35`
- [ ] `C-CF-76` `literal` The download bar carries the sub label `Navigation & Live Traffic` `src: Core features > Global chrome rule 36`
- [ ] `C-CF-77` `literal` The download bar carries the control `Send to your phone` `src: Core features > Global chrome rule 36`
- [ ] `C-CF-78` `literal` The conversion route leads with `Don't have Waze yet?` `src: Core features > Content routes rule 37`
- [ ] `C-CF-79` `literal` The not found page carries the heading `Page not found` `src: Core features > Content routes rule 38`
- [ ] `C-CF-80` `literal` The not found page carries the subhead `The page you were looking for is out of reach` `src: Core features > Content routes rule 38`
- [ ] `C-CF-81` `constraint` An unknown address answers not found `src: Core features > Content routes rule 38`
- [ ] `C-CF-82` `ui` The not found page offers a way back to the map `src: Core features > Content routes rule 38`
- [ ] `C-CF-83` `capability` A privacy page is reachable from the footer of every page `src: Core features > Content routes rule 39`
- [ ] `C-CF-84` `capability` A terms page is reachable from the footer of every page `src: Core features > Content routes rule 39`
- [ ] `C-CF-85` `capability` The privacy page states what the product records about a driver `src: Core features > Content routes rule 39`
- [ ] `C-CF-86` `capability` Every view of a public route is recorded with the route viewed `src: Core features > The record of what was viewed rule 40`
- [ ] `C-CF-87` `data` A view taken without an account is recorded against no driver `src: Core features > The record of what was viewed rule 40`
- [ ] `C-CF-88` `constraint` A request for another driver's view records is denied `src: Core features > The record of what was viewed rule 40`
- [ ] `C-CF-89` `constraint` A submission arriving with the decoy field filled writes nothing `src: Core features > Refusing a bot rule 41`
- [ ] `C-CF-90` `constraint` A form submitted more than three times inside one minute from one origin writes nothing `src: Core features > Refusing a bot rule 41`

## C-UF User flow

- [ ] `C-UF-01` `contract` The route `/` renders the live map application `src: User flow route table`
- [ ] `C-UF-02` `contract` The route `/as` renders the same application as the default entry `src: User flow route table`
- [ ] `C-UF-03` `contract` The route `/gs` renders the same application as the default entry `src: User flow route table`
- [ ] `C-UF-04` `contract` An unauthenticated request for `/drives` is sent to `/login` `src: User flow > Entry and redirects`
- [ ] `C-UF-05` `contract` Signing in returns to the route originally asked for `src: User flow > Entry and redirects`
- [ ] `C-UF-06` `contract` Signing out returns to the default entry route `src: User flow > Entry and redirects`
- [ ] `C-UF-07` `contract` An expired token leaves the request denied rather than served `src: User flow > Entry and redirects`
- [ ] `C-UF-08` `contract` The route `/scheduler` opens the leave time scheduler over the rail `src: User flow route table`
- [ ] `C-UF-09` `contract` The route `/report` requires a signed in driver `src: User flow route table`
- [ ] `C-UF-10` `ui` The rail before either endpoint resolves shows two placeholders with no route `src: User flow > States`
- [ ] `C-UF-11` `ui` The planned drives route with nothing scheduled says so `src: User flow > States`
- [ ] `C-UF-12` `ui` The map holds a placeholder until tiles arrive `src: User flow > States`
- [ ] `C-UF-13` `ui` A failed route calculation leaves the previously drawn route in place `src: User flow > States`
- [ ] `C-UF-14` `ui` A refused report names the reason without changing anything `src: User flow > States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The primary action colour appears on one element per page `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The interface palette stays visibly separate from the report palette `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Every animation respects a reduced motion preference `src: UI/UX notes`
- [ ] `C-UX-04` `ui` The tile fade survives under a reduced motion preference `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Body text meets WCAG AA contrast against the background behind `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Every control is reachable by keyboard navigation with a visible focus ring `src: UI/UX notes`
- [ ] `C-UX-07` `ui` The rail spans the full width as a sheet at a narrow viewport `src: UI/UX notes`
- [ ] `C-UX-08` `ui` The rail floats over the map from the tablet breakpoint upward `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Nothing on the map animates unless a real road condition changed `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Icon only controls carry a visually hidden text label `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Every route arrives as markup rendered on the server `src: Technical requirements`
- [ ] `C-TR-02` `contract` The datastore is PostgreSQL reached at `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-03` `contract` The health endpoint answers only once the database is reachable `src: Technical requirements`
- [ ] `C-TR-04` `contract` Every response carries a strict transport policy header `src: Technical requirements`
- [ ] `C-TR-05` `contract` Every response carries a nosniff content type policy header `src: Technical requirements`
- [ ] `C-TR-06` `constraint` Nothing the browser downloads carries a credential `src: Technical requirements`
- [ ] `C-TR-07` `contract` Every public route declares a social preview title `src: Technical requirements`
- [ ] `C-TR-08` `constraint` No two public routes share a social preview title `src: Technical requirements`
- [ ] `C-TR-09` `contract` Every declared social preview image resolves `src: Technical requirements`
- [ ] `C-TR-10` `constraint` No log line carries a password `src: Technical requirements`
- [ ] `C-TR-11` `constraint` No tile image ships bundled with the app `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema holds seven tables `src: Data model`
- [ ] `C-DM-02` `data` All timestamps are UTC `src: Data model`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026` `src: Data model`
- [ ] `C-DM-04` `literal` The account `driver@example.com` is seeded `src: Data model > Seed data`
- [ ] `C-DM-05` `literal` The account `driver2@example.com` is seeded `src: Data model > Seed data`
- [ ] `C-DM-06` `literal` The account `driver3@example.com` is seeded `src: Data model > Seed data`
- [ ] `C-DM-07` `data` Six places are seeded `src: Data model > Seed data`
- [ ] `C-DM-08` `literal` The place `Connaught Place` is seeded `src: Data model > Seed data`
- [ ] `C-DM-09` `literal` The place `Cyber Hub Gurugram` is seeded `src: Data model > Seed data`
- [ ] `C-DM-10` `data` Five segments are seeded `src: Data model > Seed data`
- [ ] `C-DM-11` `literal` The segment `Ring Road North` is seeded `src: Data model > Seed data`
- [ ] `C-DM-12` `literal` The segment `DND Flyway` is seeded `src: Data model > Seed data`
- [ ] `C-DM-13` `data` Driver reputation is computed on read rather than stored `src: Data model > drivers`
- [ ] `C-DM-14` `data` The road condition level of a segment is computed on read rather than stored `src: Data model > segments`
- [ ] `C-DM-15` `literal` One planned drive arriving `2026-09-17T09:00:00Z` is seeded `src: Data model > Seed data`
- [ ] `C-DM-16` `data` Seeding leaves no duplicate row across a restart `src: Data model > Seed data`
- [ ] `C-DM-17` `data` A driver casts at most one vote on any one report `src: Data model > report_votes`
- [ ] `C-DM-18` `data` A segment path is stored as latitude longitude pairs separated by spaces `src: Data model > segments`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Every component colour references a named token rather than a raw value `src: Front-end specification > Colour tokens`
- [ ] `C-FE-02` `literal` The display face is `Waze Boing` `src: Front-end specification > Typography`
- [ ] `C-FE-03` `literal` The text face is `Noto Sans` `src: Front-end specification > Typography`
- [ ] `C-FE-04` `ui` Every face loads with a swap fallback `src: Front-end specification > Typography`
- [ ] `C-FE-05` `literal` Body copy renders at `16px` `src: Front-end specification > Typography`
- [ ] `C-FE-06` `ui` Stacking follows a fixed ladder with map panes at the base `src: Front-end specification > Layout and stacking`
- [ ] `C-FE-07` `ui` Icons are drawn as vector geometry rather than as image files `src: Front-end specification > Iconography`
- [ ] `C-FE-08` `ui` Each report type pairs a colour with a distinct glyph `src: Front-end specification > Report and traffic colour system`
- [ ] `C-FE-09` `ui` The suggestions panel casts an inset shadow from the top edge `src: Front-end specification > The driving directions rail in detail`
- [ ] `C-FE-10` `constraint` No binary from the original product ships in the build `src: Front-end specification > Generating every asset`
- [ ] `C-FE-11` `ui` The map placeholder is a flat fill with a centred loader `src: Front-end specification > Generating every asset`
- [ ] `C-FE-12` `ui` The position marker breathes so a visitor finds the marker at a glance `src: Front-end specification > Motion detail`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product carries no turn by turn navigation client `src: Constraints`
- [ ] `C-CN-02` `constraint` The product carries no telemetry ingestion from phones `src: Constraints`
- [ ] `C-CN-03` `constraint` The product carries no map editor tool `src: Constraints`
- [ ] `C-CN-04` `constraint` The product carries no ads `src: Constraints`
- [ ] `C-CN-05` `constraint` The product carries no carpool matching `src: Constraints`
- [ ] `C-CN-06` `constraint` The product makes no external network call at runtime `src: Constraints`
- [ ] `C-CN-07` `constraint` Every driver sees the same places `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `contract` The container-internal port is `4173` `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served under the `/api` prefix on the app origin `src: Deployment contract`
- [ ] `C-DC-04` `contract` The health endpoint returns `200` once the app is ready `src: Deployment contract`
- [ ] `C-DC-05` `contract` Credentials are written to `/app/USER_README.md` `src: Deployment contract`
- [ ] `C-DC-06` `contract` The directory `.browser_screenshots/` exists at the app root `src: Deployment contract`
- [ ] `C-DC-07` `contract` The directory `.downloads/` exists at the app root `src: Deployment contract`
- [ ] `C-DC-08` `contract` The app serves a production build rather than a development server `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0` `src: Deployment contract`
- [ ] `C-DC-11` `contract` A list endpoint returns a top-level JSON array `src: Deployment contract > API shapes`
- [ ] `C-DC-12` `contract` An invalid call is rejected as a client error rather than a server error `src: Deployment contract > API shapes`
- [ ] `C-DC-13` `contract` A route calculation answers without a bearer token `src: Deployment contract > API shapes`

## Pinned literals

| Value | Where the product uses it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the password on every seeded account | `C-DM-03` |
| `driver@example.com` | the seeded account of reputation 3 | `C-DM-04` |
| `driver2@example.com` | the seeded account of reputation 0 | `C-DM-05` |
| `driver3@example.com` | the seeded account of reputation 1 | `C-DM-06` |
| `Connaught Place` | a seeded place, the origin of the seeded drive | `C-DM-08` |
| `Cyber Hub Gurugram` | a seeded place, the destination of the seeded drive | `C-DM-09` |
| `Ring Road North` | a seeded segment reading heavy | `C-DM-11` |
| `DND Flyway` | a seeded segment reading clear | `C-DM-12` |
| `Outer Ring Road` | a seeded segment reading slowing | `C-CF-45` |
| `2026-09-17T09:00:00Z` | the arrival time of the seeded planned drive | `C-DM-15` |
| `2026-09-17T08:28:00Z` | the leave time solved from that arrival time | `C-CF-50` |
| `27 minutes` | the travel time of the worked route | `C-CF-45` |
| `60 minutes` | the freshness of a new report | `C-CF-29` |
| `180 minutes` | the ceiling on extended freshness | `C-CF-34` |
| `5 minute buffer` | the margin subtracted when solving a leave time | `C-CF-49` |
| `15 minute lead` | the margin before a leave time at which a reminder falls due | `C-CF-59` |
| `3 minutes` | the saving a faster alternative must reach before being offered | `C-CF-48` |
| `100 percent` | the scaling applied to a clear segment | `C-CF-41` |
| `150 percent` | the scaling applied to a slowing segment | `C-CF-42` |
| `250 percent` | the scaling applied to a heavy segment | `C-CF-43` |
| `jam` | a report type | `C-CF-18` |
| `closure` | a report type | `C-CF-20` |
| `hazard` | a report type | `C-CF-21` |
| `confirm` | a vote value | `C-CF-31` |
| `heavy` | a road condition level | `C-CF-18` |
| `slowing` | a road condition level | `C-CF-19` |
| `clear` | a road condition level | `C-CF-22` |
| `expired` | a report state | `C-CF-30` |
| `dismissed` | a report state | `C-CF-36` |
| `scheduled` | a planned drive state | `C-CF-57` |
| `canceled` | a planned drive state | `C-CF-62` |
| `How suggestions work` | a map meta row link | `C-CF-09` |
| `Choose starting point` | the starting point placeholder | `C-CF-16` |
| `Choose destination` | the destination placeholder | `C-CF-17` |
| `Edit your arrival time` | the coaching tooltip title | `C-CF-53` |
| `Got it` | the coaching tooltip dismiss | `C-CF-54` |
| `Leave now` | the control that opens the scheduler | `C-CF-55` |
| `Wazeopedia` | an app launcher destination | `C-CF-69` |
| `Report an issue` | an overflow menu entry | `C-CF-70` |
| `Waze for Cities` | a marketing header navigation entry | `C-CF-71` |
| `Where drivers help drivers` | the footer tagline | `C-CF-72` |
| `© 2006 - 2026 Waze Mobile. All Rights Reserved.` | the footer copyright line | `C-CF-73` |
| `Live Map` | a footer column heading | `C-CF-74` |
| `Plan a drive` | a link under the Live Map footer column | `C-CF-74` |
| `English` | the language selector default | `C-CF-75` |
| `Navigation & Live Traffic` | the download bar sub label | `C-CF-76` |
| `Send to your phone` | the download bar control | `C-CF-77` |
| `Don't have Waze yet?` | the conversion route lead | `C-CF-78` |
| `Page not found` | the not found page heading | `C-CF-79` |
| `The page you were looking for is out of reach` | the not found page subhead | `C-CF-80` |
| `Waze Boing` | the display face | `C-FE-02` |
| `Noto Sans` | the text face | `C-FE-03` |
| `16px` | the body copy size | `C-FE-05` |
| `DATABASE_URL` | the variable the datastore is reached at | `C-TR-02` |
| `APP_PUBLIC_URL` | the variable the app is reachable at | `C-DC-01` |
| `4173` | the container-internal port | `C-DC-02` |
| `/api` | the prefix the HTTP API is served under | `C-DC-03` |
| `200` | the ready answer from the health endpoint | `C-DC-04` |
| `/app/USER_README.md` | the file credentials are written to | `C-DC-05` |
| `.browser_screenshots/` | a reserved directory at the app root | `C-DC-06` |
| `.downloads/` | a reserved directory at the app root | `C-DC-07` |
| `0.0.0.0` | the address the server binds | `C-DC-10` |
| `/` | the default entry route | `C-UF-01` |
| `/as` | an alternate entry route | `C-UF-02` |
| `/gs` | an alternate entry route | `C-UF-03` |
| `/drives` | the planned drives route | `C-UF-04` |
| `/login` | the sign in route | `C-UF-04` |
| `/scheduler` | the scheduler route | `C-UF-08` |
| `/report` | the report panel route | `C-UF-09` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the small margin of tiles requested beyond the viewport | `C-CF-05` |
| the exact colour value behind every named token | `C-FE-01` |
| the corner radius of a panel | `C-FE-09` |
| the exact widths of the mobile ceiling, the tablet floor, the desktop step | `C-UX-07` |
| the duration of any animation | `C-UX-03` |
| the token expiry interval | `C-UF-07` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 2 | 4 |
| User roles | 1 | 9 |
| Core features | 11 | 90 |
| User flow | 8 | 14 |
| UI and UX notes | 4 | 10 |
| Technical requirements | 3 | 11 |
| Data model | 6 | 18 |
| Front-end specification | 5 | 12 |
| Constraints | 0 | 7 |
| Deployment contract | 8 | 13 |
