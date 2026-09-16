# Checklist: teamwork-platform-showcase-vb

Items: 133
Unpinned values flagged: 3
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The product ships a public marketing estate of sixteen routes `src: Overview`
- [ ] `C-OV-02` `capability` The product ships a signed-in console over a shared graph of work items `src: Overview`
- [ ] `C-OV-03` `constraint` Three header chrome treatments exist, one per route family `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A `requester` reads only the requests raised by that same account `src: User roles`
- [ ] `C-RL-02` `role` A `member` reads every work item in the projects holding that membership `src: User roles`
- [ ] `C-RL-03` `role` An `admin` alone edits statuses, transitions, automation rules `src: User roles`
- [ ] `C-RL-04` `contract` Authorization is enforced server-side on every mutating endpoint `src: User roles`
- [ ] `C-RL-05` `contract` An unauthenticated request for a work item is denied server-side `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `literal` Every seeded account signs in with the password `deku-demo-pw-2026` `src: Core features, Auth`
- [ ] `C-CF-02` `capability` A successful login returns a bearer access token for later calls `src: Core features, Auth`
- [ ] `C-CF-03` `constraint` The signed-in console accepts no signups `src: Core features, Auth`
- [ ] `C-CF-04` `capability` The console work surface is a split detail pane beside the board columns `src: Core features, The board`
- [ ] `C-CF-05` `capability` Selecting a card gives the browser that work item's own address `src: Core features, The board`
- [ ] `C-CF-06` `capability` A drag succeeds only where a transition joins the two statuses `src: Core features rule 1`
- [ ] `C-CF-07` `capability` A drag with no joining transition is rejected as invalid `src: Core features rule 1`
- [ ] `C-CF-08` `data` A rejected drag leaves the stored status unchanged `src: Core features rule 1`
- [ ] `C-CF-09` `data` A successful transition writes the new status, appending one history entry `src: Core features rule 2`
- [ ] `C-CF-10` `data` A transition persists across a fresh re-read of the work item `src: Core features rule 2`
- [ ] `C-CF-11` `data` A history entry names the actor, the moment, both status names `src: Core features rule 2`
- [ ] `C-CF-12` `capability` A transition attempted by a `requester` is denied `src: Core features rule 3`
- [ ] `C-CF-13` `capability` Two simultaneous drags of one card yield exactly one written move `src: Core features rule 4`
- [ ] `C-CF-14` `data` Reordering one card changes the rank of that one card alone `src: Core features rule 5`
- [ ] `C-CF-15` `ui` The card enters its new column before the write is confirmed `src: Core features rule 6`
- [ ] `C-CF-16` `ui` A refused write returns the card, explaining in place `src: Core features rule 6`
- [ ] `C-CF-17` `capability` A transition carries conditions, validators, post-functions as three hooks `src: Core features rule 7`
- [ ] `C-CF-18` `capability` Publishing a workflow is refused until every removed status names a destination `src: Core features rule 10`
- [ ] `C-CF-19` `constraint` A project created with no configuration gets three statuses, no conditions `src: Core features rule 11`
- [ ] `C-CF-20` `capability` An automation rule names one trigger transition, one actor, one action `src: Core features rule 12`
- [ ] `C-CF-21` `data` A rule action appears in history attributed to its actor, marked automated `src: Core features rule 13`
- [ ] `C-CF-22` `capability` A rule already in the chain does not fire again for that work item `src: Core features rule 14`
- [ ] `C-CF-23` `data` One rule execution meters one unit regardless of actions taken `src: Core features rule 15`
- [ ] `C-CF-24` `literal` Rule allowances read `100`, `1700`, `1000` per user, unlimited `src: Core features rule 15`
- [ ] `C-CF-25` `capability` An assignee change by a rule sends one email over real SMTP `src: Core features rule 20`
- [ ] `C-CF-26` `literal` The subject begins `Northwind work update:` then the item key `src: Core features rule 21`
- [ ] `C-CF-27` `constraint` No email is sent where the assignee is unchanged `src: Core features rule 23`
- [ ] `C-CF-28` `capability` A member is denied another project board plus every listing drawn from that board `src: Core features rule 24`
- [ ] `C-CF-29` `data` Every count is computed over the asking account's own visible set `src: Core features rule 25`
- [ ] `C-CF-30` `capability` Only an `admin` reads the page-view log, a member being denied `src: Core features rule 56`
- [ ] `C-CF-31` `capability` A shared saved filter resolves as the reader rather than its owner `src: Core features rule 34`
- [ ] `C-CF-32` `capability` An unknown query field name is refused with the offending token named `src: Core features rule 36`
- [ ] `C-CF-33` `capability` One signup submission produces one of three named outcomes `src: Core features rule 39`
- [ ] `C-CF-34` `capability` The project list shows only the projects the signed-in account belongs to `src: Core features rule 24`
- [ ] `C-CF-35` `ui` An invalid form entry is rejected in place, naming its own field `src: Core features rule 40`
- [ ] `C-CF-36` `ui` Accept, reject, manage carry equal visual strength in the consent dialogue `src: Core features rule 41`
- [ ] `C-CF-37` `capability` Changing team size recomputes every figure with no network request `src: Core features rule 43`
- [ ] `C-CF-38` `capability` Graduated bands charge the users in each band at that band's rate `src: Core features rule 44`
- [ ] `C-CF-39` `literal` Above ten users the Free column reads `Not available above 10 users` `src: Core features rule 45`
- [ ] `C-CF-40` `literal` The saving badge reads `SAVE UP TO 17%` `src: Core features rule 46`
- [ ] `C-CF-41` `capability` The catalogue combines product, team, type facets `src: Core features rule 48`
- [ ] `C-CF-42` `ui` Every facet value shows a result count, updating as others apply `src: Core features rule 48`
- [ ] `C-CF-43` `literal` A customer story carries `Challenge:`, `Solution:`, `Impact:` as three fields `src: Core features rule 50`
- [ ] `C-CF-44` `capability` A terms page is reachable from every footer, linked from signup `src: Core features rule 55`
- [ ] `C-CF-45` `data` Each page view is recorded with its route plus the moment `src: Core features rule 56`
- [ ] `C-CF-46` `capability` An unknown address answers with a not-found status of its own `src: Core features rule 57`

## C-UF User flow

- [ ] `C-UF-01` `contract` Every route in the route table exists, reachable without client-side scripting `src: User flow, Routes`
- [ ] `C-UF-02` `literal` The public routes include `/`, `/products`, `/products/work/pricing` `src: User flow, Routes`
- [ ] `C-UF-03` `literal` The console routes include `/login`, `/app/projects` `src: User flow, Routes`
- [ ] `C-UF-04` `capability` An unauthenticated console request lands on the sign-in route `src: User flow, Entry`
- [ ] `C-UF-05` `capability` Signing out stops the previous bearer token working `src: User flow, Entry`
- [ ] `C-UF-06` `capability` A non-member sees neither the project nor its board `src: User flow, Entry`
- [ ] `C-UF-07` `ui` The breadcrumb names each ancestor as a link back up a level `src: User flow, Entry`
- [ ] `C-UF-08` `capability` The pricing journey restores both controls from the address `src: User flow journey 1`
- [ ] `C-UF-09` `capability` The catalogue journey opens the same view from a shared address `src: User flow journey 2`
- [ ] `C-UF-10` `ui` Every list carries an empty state naming what would fill the list `src: User flow, States`
- [ ] `C-UF-11` `ui` A failing component renders its own empty state without taking the route `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The estate carries atmosphere, the console reading quiet, dense, organised `src: UI/UX notes`
- [ ] `C-UX-02` `ui` Three meaning colours appear nowhere else in the interface `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Success takes a lime rather than the teal in the same accent scale `src: UI/UX notes`
- [ ] `C-UX-04` `ui` A project takes its accent hue from a stable hash of its own identifier `src: UI/UX notes`
- [ ] `C-UX-05` `literal` Headings are set at the `653` axis value in `Northwind Sans` `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Arriving elements rise a short distance, staggered behind one another `src: UI/UX notes`
- [ ] `C-UX-07` `literal` Body text meets a contrast ratio of `4.5:1`, large display text `3:1` `src: UI/UX notes`
- [ ] `C-UX-08` `ui` The mega-menu leaves the accessibility tree when closed `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Every icon-only control carries an accessible name `src: UI/UX notes`
- [ ] `C-UX-10` `ui` At a narrow viewport the pricing table stacks behind a plan selector `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The frontend is `React` with `Vite`, the backend `Flask` `src: Technical requirements`
- [ ] `C-TR-02` `contract` Route data arrives as JSON from the same origin under `/api` `src: Technical requirements`
- [ ] `C-TR-03` `contract` Every public route shows its content with no script available `src: Technical requirements`
- [ ] `C-TR-04` `literal` The datastore is reached at `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-05` `literal` Mail is sent to `mailpit` at `SMTP_HOST`, `SMTP_PORT` `src: Technical requirements`
- [ ] `C-TR-06` `constraint` No second database, cache, queue, object store, mail vendor is introduced `src: Technical requirements`
- [ ] `C-TR-07` `contract` `GET /api/health` returns `200` once the app is ready `src: Technical requirements`
- [ ] `C-TR-08` `capability` A trailing slash is stripped, redirected permanently `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Sixteen tables carry the model, every timestamp being UTC `src: Data model`
- [ ] `C-DM-02` `data` An item key is unique within its project, never changing `src: Data model`
- [ ] `C-DM-03` `data` Rank is a lexicographically sorting string rather than a number `src: Data model`
- [ ] `C-DM-04` `data` A history entry is appended, never updated, never deleted `src: Data model`
- [ ] `C-DM-05` `data` A status carries a category from `to_do`, `in_progress`, `done` `src: Data model`
- [ ] `C-DM-06` `literal` Three projects are seeded: `FIN`, `MKT`, `SUP` `src: Data model, Seed data`
- [ ] `C-DM-07` `literal` `FIN` carries statuses `Blocked`, `In progress`, `Ready for review`, `Done` `src: Data model, Seed data`
- [ ] `C-DM-08` `data` Seeding is idempotent, a restart duplicating no row `src: Data model, Seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Every visual value resolves from a named token, never a literal colour `src: Front-end specification`
- [ ] `C-FE-02` `ui` Elevation carries three levels: raised, overlay, overflow `src: Front-end specification`
- [ ] `C-FE-03` `ui` A resting card carries a zero-size shadow for the hover shadow to grow from `src: Front-end specification`
- [ ] `C-FE-04` `ui` Corner radii vary by component, primary buttons being full lozenges `src: Front-end specification`
- [ ] `C-FE-05` `ui` A disabled control drops opacity, losing its pointer events `src: Front-end specification`
- [ ] `C-FE-06` `ui` One palette generation is built, the newer of the two `src: Front-end specification`
- [ ] `C-FE-07` `ui` Motion binds to four named roles used in component code `src: Front-end specification, motion`
- [ ] `C-FE-08` `ui` The indeterminate spinner lurches rather than turning evenly `src: Front-end specification, motion`
- [ ] `C-FE-09` `constraint` Nothing declares a transition on every property `src: Front-end specification, motion`
- [ ] `C-FE-10` `ui` Every icon is drawn as geometry, never fetched as a separate request `src: Front-end specification, Iconography`
- [ ] `C-FE-11` `ui` The search mark is one shape with its lens punched out as a hole `src: Front-end specification, Iconography`
- [ ] `C-FE-12` `ui` The narrow-band menu button is four rules, two rotating to a cross `src: Front-end specification, Iconography`
- [ ] `C-FE-13` `ui` A solid blue square bleeds to the viewport corner on product routes `src: Front-end specification, chromes`
- [ ] `C-FE-14` `literal` The product call to action label differs per route family `src: Front-end specification, chromes`
- [ ] `C-FE-15` `ui` The legacy chrome is retired in favour of the company chrome `src: Front-end specification, chromes`
- [ ] `C-FE-16` `ui` One mega-menu panel slides beneath whichever trigger opened the panel `src: Front-end specification, mega-menu`
- [ ] `C-FE-17` `capability` `Escape` closes the panel, returning focus to its trigger `src: Front-end specification, mega-menu`
- [ ] `C-FE-18` `ui` The audience switcher is a tab pattern with arrow-key navigation `src: Front-end specification, mega-menu`
- [ ] `C-FE-19` `ui` Customer marks are silhouettes tinted per section `src: Front-end specification, Components`
- [ ] `C-FE-20` `ui` The pricing plan table carries a ribbon reading `RECOMMENDED` across its third column `src: Front-end specification, Pricing`
- [ ] `C-FE-21` `ui` The work product route places a signup card beside its headline `src: Front-end specification, routes`
- [ ] `C-FE-22` `ui` The comparison matrix is a real table with a scope per header cell `src: Front-end specification, Components`
- [ ] `C-FE-23` `ui` The automation matrix row holds strings rather than tick marks `src: Front-end specification, Components`
- [ ] `C-FE-24` `ui` Angled section edges are generated as complements from one angle value `src: Front-end specification, Components`
- [ ] `C-FE-25` `capability` The home journey pins a stage across reserved scroll distance `src: Front-end specification, Home`
- [ ] `C-FE-26` `capability` Journey progress is a continuous function of scroll offset `src: Front-end specification, Home`
- [ ] `C-FE-27` `constraint` The home journey does not run below the narrow band `src: Front-end specification, Home`
- [ ] `C-FE-28` `ui` One board illustration card is tilted out of the grid `src: Front-end specification, Home`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No real-time collaborative editing ships `src: Constraints`
- [ ] `C-CN-02` `constraint` No separate search index, metrics store, app sandbox, billing ships `src: Constraints`
- [ ] `C-CN-03` `constraint` No outbound network call at run time beyond the two named services `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173` `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served on that same origin under `/api` `src: Deployment contract`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-05` `contract` Credentials are written to `/app/USER_README.md` `src: Deployment contract`
- [ ] `C-DC-06` `contract` Reserved `.browser_screenshots/`, `.downloads/` exist at the app root `src: Deployment contract`
- [ ] `C-DC-07` `contract` A production build is served behind a static preview server `src: Deployment contract`
- [ ] `C-DC-08` `contract` The server outlives the agent session, never a child of the shell `src: Deployment contract`
- [ ] `C-DC-09` `contract` The listener binds `0.0.0.0` rather than loopback `src: Deployment contract`
- [ ] `C-DC-10` `contract` Named backing services are already running, never started by the app `src: Deployment contract`
- [ ] `C-DC-11` `contract` Every list endpoint returns a top-level JSON array `src: Deployment contract, API shapes`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the corpus password | `C-CF-01` |
| `100` | the Free rule allowance | `C-CF-24` |
| `1700` | the Standard rule allowance | `C-CF-24` |
| `1000` | the Premium per-user rule allowance | `C-CF-24` |
| `Northwind work update:` | the notification subject prefix | `C-CF-26` |
| `Not available above 10 users` | the Free column text above ten users | `C-CF-39` |
| `SAVE UP TO 17%` | the saving badge | `C-CF-40` |
| `Challenge:` | the first story label | `C-CF-43` |
| `Solution:` | the second story label | `C-CF-43` |
| `Impact:` | the third story label | `C-CF-43` |
| `/` | the home route | `C-UF-02` |
| `/products` | the product hub route | `C-UF-02` |
| `/products/work/pricing` | the pricing route | `C-UF-02` |
| `/login` | the sign-in route | `C-UF-03` |
| `/app/projects` | the project list route | `C-UF-03` |
| `653` | the heading axis value | `C-UX-05` |
| `Northwind Sans` | the text face | `C-UX-05` |
| `4.5:1` | the body contrast bar | `C-UX-07` |
| `3:1` | the large-text contrast bar | `C-UX-07` |
| `DATABASE_URL` | the datastore variable | `C-TR-04` |
| `mailpit` | the mail provider slug | `C-TR-05` |
| `SMTP_HOST` | the mail host variable | `C-TR-05` |
| `SMTP_PORT` | the mail port variable | `C-TR-05` |
| `FIN` | the first seeded project key | `C-DM-06` |
| `MKT` | the second seeded project key | `C-DM-06` |
| `SUP` | the third seeded project key | `C-DM-06` |
| `Blocked` | the first seeded status | `C-DM-07` |
| `In progress` | the second seeded status | `C-DM-07` |
| `Ready for review` | the third seeded status | `C-DM-07` |
| `Done` | the fourth seeded status | `C-DM-07` |

### Referenced but not pinned

| Value | Item |
|---|---|
| the exact colour values, left to the builder by role, family, tone | `C-UX-02` |
| the exact motion durations, given as character rather than value | `C-FE-07` |
| the exact breakpoint widths, given as three named bands | `C-UX-01` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 2 | 3 |
| User roles | 1 | 5 |
| Core features | 33 | 46 |
| User flow | 10 | 11 |
| UI/UX notes | 7 | 10 |
| Technical requirements | 7 | 8 |
| Data model | 7 | 8 |
| Front-end specification | 25 | 28 |
| Constraints | 2 | 3 |
| Deployment contract | 10 | 11 |
