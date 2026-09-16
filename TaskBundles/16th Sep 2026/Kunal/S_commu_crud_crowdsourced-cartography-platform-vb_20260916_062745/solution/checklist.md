# Checklist: Openhaven

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, technical, datamodel, constraints, deployment
Sections absent: buildplan
Items: 130
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app presents one shared global map dataset to every visitor. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app serves readers who hold no account. `src: Overview para 2`
- [ ] `C-OV-03` `constraint` The app offers no likes, no follows, no private messages. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor reads the map without an account. `src: User roles table row 1`
- [ ] `C-RL-02` `constraint` A visitor creates no element. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A mapper opens a changeset after signing in. `src: User roles table row 2`
- [ ] `C-RL-04` `role` A mapper reverts a changeset written by another mapper. `src: User roles table row 2`
- [ ] `C-RL-05` `constraint` The app rejects a mutating API call from a signed-out session. `src: User roles para 3`
- [ ] `C-RL-06` `constraint` The app leaves protected state unchanged after rejecting an unauthorized call. `src: User roles para 3`

## C-CF Core features

- [ ] `C-CF-01` `capability` The app creates a mapper account from a submitted email with a password. `src: Core features, Auth rule 1`
- [ ] `C-CF-02` `constraint` The app rejects a signup for an email already in use. `src: Core features, Auth rule 1`
- [ ] `C-CF-03` `literal` The app returns a bearer token from `/api/auth/login`. `src: Core features, Auth rule 2`
- [ ] `C-CF-04` `constraint` The app stores every password hashed. `src: Core features, Auth rule 3`
- [ ] `C-CF-05` `constraint` The app denies a mutating request carrying an expired token. `src: Core features, Auth rule 4`
- [ ] `C-CF-06` `data` The app stores a node as a single point at a latitude with a longitude. `src: Core features, shared dataset rule 1`
- [ ] `C-CF-07` `data` The app stores a way as an ordered list of node references. `src: Core features, shared dataset rule 2`
- [ ] `C-CF-08` `data` The app stores a relation as an ordered list of members carrying roles. `src: Core features, shared dataset rule 3`
- [ ] `C-CF-09` `data` The app stores a version on every element. `src: Core features, shared dataset rule 4`
- [ ] `C-CF-10` `literal` The app stores tags as free-form `key=value` strings. `src: Core features, shared dataset rule 5`
- [ ] `C-CF-11` `capability` The app lets one way belong to several relations at once. `src: Core features, shared dataset rule 6`
- [ ] `C-CF-12` `constraint` The app refuses a way referencing a node that does not exist. `src: Core features, shared dataset rule 7`
- [ ] `C-CF-13` `literal` The app refuses deleting a node that is `still in use`. `src: Core features, shared dataset rule 8`
- [ ] `C-CF-14` `capability` The app opens a changeset for a signed-in mapper. `src: Core features, changeset rule 1`
- [ ] `C-CF-15` `capability` The app applies a batch of creates, modifies, deletes in one upload. `src: Core features, changeset rule 2`
- [ ] `C-CF-16` `constraint` The app applies no part of a batch when any element in the batch is refused. `src: Core features, changeset rule 3`
- [ ] `C-CF-17` `constraint` The app refuses a further upload to a closed changeset. `src: Core features, changeset rule 4`
- [ ] `C-CF-18` `capability` The app raises a touched element to exactly one higher version. `src: Core features, changeset rule 5`
- [ ] `C-CF-19` `data` The app computes a changeset bounding box from the elements the changeset touched. `src: Core features, changeset rule 6`
- [ ] `C-CF-20` `literal` The app rejects a changeset writing more than `500` elements. `src: Core features, changeset rule 7`
- [ ] `C-CF-21` `capability` The app returns the saved element value after a reload. `src: Core features, changeset rule 8`
- [ ] `C-CF-22` `capability` The app retains every version of every element. `src: Core features, history rule 1`
- [ ] `C-CF-23` `capability` The app returns every version of a node oldest first. `src: Core features, history rule 2`
- [ ] `C-CF-24` `literal` The app writes a delete as a new version marked `visible` false. `src: Core features, history rule 3`
- [ ] `C-CF-25` `capability` The app returns the changeset stream newest first. `src: Core features, history rule 4`
- [ ] `C-CF-26` `capability` The app lists the exact elements one changeset wrote. `src: Core features, history rule 5`
- [ ] `C-CF-27` `capability` The app resolves an element to the mapper who last touched the element. `src: Core features, history rule 6`
- [ ] `C-CF-28` `constraint` The app never alters an older version row. `src: Core features, history rule 7`
- [ ] `C-CF-29` `capability` The app creates a new changeset restoring elements a named changeset touched. `src: Core features, revert rule 1`
- [ ] `C-CF-30` `capability` The app attributes a revert to the mapper who asked for the revert. `src: Core features, revert rule 2`
- [ ] `C-CF-31` `constraint` The app keeps reverted versions readable. `src: Core features, revert rule 3`
- [ ] `C-CF-32` `constraint` The app refuses a revert whose elements moved to newer versions. `src: Core features, revert rule 4`
- [ ] `C-CF-33` `capability` The app warns before upload about a way crossing itself. `src: Core features, validation rule 1`
- [ ] `C-CF-34` `constraint` The app lets a mapper upload over a dismissed warning. `src: Core features, validation rule 2`
- [ ] `C-CF-35` `constraint` The app refuses only structural violations at upload. `src: Core features, validation rule 3`
- [ ] `C-CF-36` `capability` The app opens a full-viewport map of the dataset at the site root. `src: Core features, map surface rule 1`
- [ ] `C-CF-37` `capability` The app positions square tiles by a zoom-column-row address. `src: Core features, map surface rule 2`
- [ ] `C-CF-38` `ui` The app shows a welcome card to a first-time visitor. `src: Core features, map surface rule 3`
- [ ] `C-CF-39` `capability` The app keeps a dismissed welcome card dismissed across a reload. `src: Core features, map surface rule 3`
- [ ] `C-CF-40` `capability` The app drops a result pin for a matched place search. `src: Core features, map surface rule 5`
- [ ] `C-CF-41` `ui` The app shows an attribution line naming Openhaven contributors. `src: Core features, map surface rule 7`
- [ ] `C-CF-42` `literal` The app returns one map tile `256` pixels square. `src: Core features, tiles rule 1`
- [ ] `C-CF-43` `literal` The app serves tiles no deeper than zoom `19`. `src: Core features, tiles rule 2`
- [ ] `C-CF-44` `constraint` The app draws tiles on demand per tile. `src: Core features, tiles rule 4`
- [ ] `C-CF-45` `capability` The app caches a drawn tile. `src: Core features, tiles rule 5`
- [ ] `C-CF-46` `capability` The app marks a tile stale when an edit changes data inside the tile bounds. `src: Core features, tiles rule 6`
- [ ] `C-CF-47` `literal` The app returns every element inside a `bbox`. `src: Core features, spatial rule 1`
- [ ] `C-CF-48` `literal` The app rejects a bbox larger than `0.25` square degrees. `src: Core features, spatial rule 3`
- [ ] `C-CF-49` `literal` The app rejects a request returning more than `5000` elements. `src: Core features, spatial rule 4`
- [ ] `C-CF-50` `capability` The app returns a seconds-old element from a covering bbox request. `src: Core features, spatial rule 5`
- [ ] `C-CF-51` `capability` The app downloads raw elements for the area in view. `src: Core features, spatial rule 6`
- [ ] `C-CF-52` `ui` The app renders an about page carrying five named sections. `src: Core features, reading pages rule 1`
- [ ] `C-CF-53` `capability` The app lists diary entries newest first. `src: Core features, reading pages rule 2`
- [ ] `C-CF-54` `ui` The app makes a whole help card clickable. `src: Core features, reading pages rule 3`
- [ ] `C-CF-55` `constraint` The app rejects invalid form input inline, naming the wrong field. `src: Core features, reading pages rule 4`
- [ ] `C-CF-56` `capability` The app renders its own not-found page for an unmatched address. `src: Core features, reading pages rule 5`

## C-UF User flow

- [ ] `C-UF-01` `contract` The app routes a signed-out request for the editor to the login page. `src: User flow, entry and redirects`
- [ ] `C-UF-02` `capability` The app continues to the editor after a successful sign-in from that redirect. `src: User flow, entry and redirects`
- [ ] `C-UF-03` `capability` The app lands a direct sign-in on the map home. `src: User flow, entry and redirects`
- [ ] `C-UF-04` `capability` The app keeps an open changeset open after a token expires mid-edit. `src: User flow, entry and redirects`
- [ ] `C-UF-05` `capability` The app keeps every read route reachable signed out. `src: User flow, entry and redirects`
- [ ] `C-UF-06` `ui` The app shows a loading state during tile drawing. `src: User flow, states`
- [ ] `C-UF-07` `ui` The app shows an empty state for the changeset stream. `src: User flow, states`
- [ ] `C-UF-08` `ui` The app shows an empty state for the diary list. `src: User flow, states`
- [ ] `C-UF-09` `constraint` The app leaves the rest of a page usable after a failed request. `src: User flow, states`
- [ ] `C-UF-10` `capability` The app names the stored version to the mapper whose upload was rejected. `src: User flow, journey 3`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The app renders body text in a deep cool neutral. `src: UI/UX notes, palette`
- [ ] `C-UX-02` `ui` The app reserves a light, vivid blue for the primary action. `src: UI/UX notes, palette`
- [ ] `C-UX-03` `ui` The app reserves a light, soft green for the edit control. `src: UI/UX notes, palette`
- [ ] `C-UX-04` `ui` The app reserves a mid, vivid red for a destructive action. `src: UI/UX notes, palette`
- [ ] `C-UX-05` `literal` The app sets body copy at `14px`. `src: UI/UX notes, type`
- [ ] `C-UX-06` `ui` The app renders the body family from the system UI stack. `src: UI/UX notes, type`
- [ ] `C-UX-07` `ui` The app eases every entrance so movement reads as designed. `src: UI/UX notes, motion`
- [ ] `C-UX-08` `ui` The app stops every animation under reduced motion. `src: UI/UX notes, motion`
- [ ] `C-UX-09` `ui` The app meets the WCAG AA contrast bar on body text. `src: UI/UX notes, accessibility`
- [ ] `C-UX-10` `ui` The app shows a visible focus ring on every interactive control. `src: UI/UX notes, accessibility`
- [ ] `C-UX-11` `ui` The app carries alternative text on every content image. `src: UI/UX notes, accessibility`
- [ ] `C-UX-12` `ui` The app overflows nothing sideways at a narrow viewport. `src: UI/UX notes, responsive`

## C-FE Front-end specification

- [ ] `C-FE-01` `contract` The app fetches no image file. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-02` `contract` The app fetches no icon font. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-03` `ui` The app draws every icon as inline vector geometry. `src: Front-end specification, iconography`
- [ ] `C-FE-04` `ui` The app labels the search control with the word Search. `src: Front-end specification, copy identity`
- [ ] `C-FE-05` `ui` The app heads the welcome card with a greeting naming Openhaven. `src: Front-end specification, copy identity`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app runs a Remix frontend on Node 20. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The app runs a FastAPI backend on Python 3.12. `src: Technical requirements para 1`
- [ ] `C-TR-03` `literal` The app reads its datastore location from `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `constraint` The app introduces no second database. `src: Technical requirements para 2`
- [ ] `C-TR-05` `capability` The app applies exactly one of two simultaneous uploads claiming the same element version. `src: Technical requirements, contention para`
- [ ] `C-TR-06` `literal` The app answers the losing upload with a `409 Conflict` response. `src: Technical requirements, contention para`
- [ ] `C-TR-07` `constraint` The app creates no second version when an applied upload is replayed. `src: Technical requirements, contention para`
- [ ] `C-TR-08` `constraint` The app gives every public route a distinct title. `src: Technical requirements, meta para`
- [ ] `C-TR-09` `literal` The app serves a sitemap at `/sitemap.xml`. `src: Technical requirements, sitemap para`
- [ ] `C-TR-10` `literal` The app serves a robots file at `/robots.txt` naming the sitemap. `src: Technical requirements, sitemap para`

## C-DM Data model

- [ ] `C-DM-01` `data` The app stores ten tables. `src: Data model para 1`
- [ ] `C-DM-02` `data` The app records every timestamp in UTC. `src: Data model para 1`
- [ ] `C-DM-03` `literal` The app accepts `deku-demo-pw-2026` at login for every seeded account. `src: Data model, password paragraph`
- [ ] `C-DM-04` `literal` The app writes seeded credentials into `/app/USER_README.md`. `src: Data model, password paragraph`
- [ ] `C-DM-05` `data` The app identifies an element by an id together with a version. `src: Data model, nodes`
- [ ] `C-DM-06` `data` The app stores the order of a way's nodes as a sequence. `src: Data model, way_nodes`
- [ ] `C-DM-07` `literal` The app seeds a node named `Riverside Cafe`. `src: Data model, seed data`
- [ ] `C-DM-08` `literal` The app seeds a way named `Kingsway`. `src: Data model, seed data`
- [ ] `C-DM-09` `capability` The app seeds one way referenced by two relations. `src: Data model, seed data`
- [ ] `C-DM-10` `constraint` The app duplicates no row when the app restarts. `src: Data model, seed closing line`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app offers no GPS trace upload. `src: Constraints bullet 2`
- [ ] `C-CN-02` `constraint` The app offers no route planning. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The app offers no moderator tier. `src: Constraints bullet 7`
- [ ] `C-CN-04` `constraint` The app makes no external network call at runtime. `src: Constraints bullet 12`
- [ ] `C-CN-05` `constraint` The app downloads no binary asset. `src: Constraints bullet 14`
- [ ] `C-CN-06` `constraint` The app stays responsive with fifty thousand elements. `src: Constraints bullet 15`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app reads its public address from `APP_PUBLIC_URL`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-02` `contract` The app reads its outside port from `APP_PUBLIC_PORT`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-03` `literal` The app listens on container port `4173`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-04` `literal` The app serves the HTTP API under the `/api` prefix. `src: Deployment contract, bullet 2`
- [ ] `C-DC-05` `literal` The app answers `/api/health` with status `200`. `src: Deployment contract, bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract, bullet 4`
- [ ] `C-DC-07` `literal` The app creates an empty `.browser_screenshots/` directory at the app root. `src: Deployment contract, bullet 6`
- [ ] `C-DC-08` `contract` The app serves a production build behind a preview server. `src: Deployment contract, bullet 7`
- [ ] `C-DC-09` `contract` The app keeps the server running after the session ends. `src: Deployment contract, bullet 8`
- [ ] `C-DC-10` `literal` The app binds `0.0.0.0`. `src: Deployment contract, bullet 9`
- [ ] `C-DC-11` `constraint` The app starts no copy of the backing service. `src: Deployment contract, bullet 10`
- [ ] `C-DC-12` `constraint` The app returns a top-level JSON array from the node history endpoint. `src: Deployment contract, API shapes`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `/api/auth/login` | the login endpoint | C-CF-03 | Core features, Auth rule 2 |
| `key=value` | the tag string scheme | C-CF-10 | Core features, shared dataset rule 5 |
| `still in use` | the refusal wording for a referenced node | C-CF-13 | Core features, shared dataset rule 8 |
| `500` | the element ceiling on one changeset | C-CF-20 | Core features, changeset rule 7 |
| `visible` | the element flag a delete clears | C-CF-24 | Core features, history rule 3 |
| `256` | tile edge in pixels | C-CF-42 | Core features, tiles rule 1 |
| `19` | the deepest zoom served | C-CF-43 | Core features, tiles rule 2 |
| `bbox` | the bounding-box query parameter | C-CF-47 | Core features, spatial rule 1 |
| `0.25` | the bbox area cap in square degrees | C-CF-48 | Core features, spatial rule 3 |
| `5000` | the element ceiling on one map call | C-CF-49 | Core features, spatial rule 4 |
| `14px` | body copy size | C-UX-05 | UI/UX notes, type |
| `DATABASE_URL` | datastore location variable | C-TR-03 | Technical requirements para 1 |
| `409 Conflict` | the losing upload's response | C-TR-06 | Technical requirements, contention para |
| `/sitemap.xml` | the sitemap route | C-TR-09 | Technical requirements, sitemap para |
| `/robots.txt` | the robots route | C-TR-10 | Technical requirements, sitemap para |
| `deku-demo-pw-2026` | password for every seeded account | C-DM-03 | Data model, password paragraph |
| `/app/USER_README.md` | the credentials file path | C-DM-04 | Data model, password paragraph |
| `Riverside Cafe` | a seeded node name | C-DM-07 | Data model, seed data |
| `Kingsway` | a seeded way name | C-DM-08 | Data model, seed data |
| `APP_PUBLIC_URL` | public address variable | C-DC-01 | Deployment contract, bullet 1 |
| `APP_PUBLIC_PORT` | outside port variable | C-DC-02 | Deployment contract, bullet 1 |
| `4173` | container-internal port | C-DC-03 | Deployment contract, bullet 1 |
| `/api` | the API prefix | C-DC-04 | Deployment contract, bullet 2 |
| `/api/health` | health route | C-DC-05 | Deployment contract, bullet 3 |
| `200` | health status | C-DC-05 | Deployment contract, bullet 3 |
| `.browser_screenshots/` | a reserved directory | C-DC-07 | Deployment contract, bullet 6 |
| `0.0.0.0` | bind address | C-DC-10 | Deployment contract, bullet 9 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the token lifetime | C-CF-05 | stated in words, with no machine-readable literal beside them |
| the narrow viewport width | C-UX-12 | stated as a behaviour, with the exact width left to the pytest layer |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 0 | 3 |
| User roles | 1 | 6 |
| Core features | 24 | 56 |
| User flow | 5 | 10 |
| UI and UX notes | 7 | 12 |
| Front-end specification | 0 | 5 |
| Technical requirements | 5 | 10 |
| Data model | 3 | 10 |
| Constraints | 1 | 6 |
| Deployment contract | 9 | 12 |
