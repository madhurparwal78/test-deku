# Checklist: drivable-portfolio-world-vb

Items: 118
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC
Unpinned values flagged: 6

## C-OV Overview

- [ ] `C-OV-01` `capability` The public portfolio is delivered as a continuously rendered world rather than as a document `src: Overview`
- [ ] `C-OV-02` `capability` Every published piece of owner content stands in the terrain as an object a visitor drives to `src: Overview`
- [ ] `C-OV-03` `constraint` No navigation bar appears anywhere on the public surface `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor opens the world without signing in `src: User roles`
- [ ] `C-RL-02` `role` A visitor cannot see, list, open or fetch anything belonging to an unpublished project by any address `src: User roles`
- [ ] `C-RL-03` `role` A visitor cannot create, edit, publish or unpublish anything `src: User roles`
- [ ] `C-RL-04` `role` A visitor cannot read the page view record `src: User roles`
- [ ] `C-RL-05` `role` The owner signs in, then writes, edits, publishes, unpublishes owner content `src: User roles`
- [ ] `C-RL-06` `contract` Authorization is enforced server-side on every mutating endpoint, so a direct call from a visitor session to an owner-only endpoint is denied with the protected state unchanged `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `literal` Signing in at `POST /api/auth/login` with `owner@example.com` plus `deku-demo-pw-2026` returns an `access_token` `src: Core features rule 1`
- [ ] `C-CF-02` `capability` Signing in with the seeded email plus any other password is rejected as invalid, returning no token `src: Core features rule 1`
- [ ] `C-CF-03` `capability` The rejected sign-in says the credentials did not match without naming which half was wrong `src: Core features rule 1`
- [ ] `C-CF-04` `capability` An owner request carrying no token, an expired token, a malformed token is denied with the targeted state unchanged `src: Core features rule 2`
- [ ] `C-CF-05` `constraint` Passwords are stored hashed, never in plain text `src: Core features Auth`
- [ ] `C-CF-06` `constraint` No signup form exists, no public route creates an account `src: Core features Auth`
- [ ] `C-CF-07` `capability` An unpublished project is absent from the world manifest at `GET /api/world` `src: Core features rule 3`
- [ ] `C-CF-08` `capability` An unpublished project is absent from the text route listing `src: Core features rule 3`
- [ ] `C-CF-09` `capability` An unpublished project answers at its own address as if the project does not exist `src: Core features rule 3`
- [ ] `C-CF-10` `capability` An unpublished project has poster bytes unreadable by a request carrying no owner token `src: Core features rule 3`
- [ ] `C-CF-11` `literal` Publishing a project whose world coordinates match an already published project is rejected with the error code `coordinates_occupied` `src: Core features rule 4`
- [ ] `C-CF-12` `literal` The refusal carries the message `Another published project already stands at those coordinates.` `src: Core features rule 4`
- [ ] `C-CF-13` `capability` The refusal names the slug of the project already standing at those coordinates `src: Core features rule 4`
- [ ] `C-CF-14` `capability` A refused project stays a draft with an empty published timestamp `src: Core features rule 5`
- [ ] `C-CF-15` `capability` A refused publish leaves the project already in place untouched `src: Core features rule 5`
- [ ] `C-CF-16` `capability` Two publish requests arriving together for two drafts at one set of coordinates produce exactly one published project, the other refused as a conflict `src: Core features rule 5`
- [ ] `C-CF-17` `constraint` A direct call to the publish endpoint is refused the same way a studio control would be, so hiding a control does not satisfy the rule `src: Core features rule 6`
- [ ] `C-CF-18` `capability` Unpublishing removes the project from the world, from the text route, freeing the coordinates for a different draft `src: Core features rule 7`
- [ ] `C-CF-19` `literal` Publishing a project with no poster image is rejected as invalid with the error code `poster_required` `src: Core features rule 8`
- [ ] `C-CF-20` `literal` Poster bytes live in the object store under the key scheme `projects/{project_id}/posters/{sha256_of_bytes}.{ext}` `src: Core features rule 9`
- [ ] `C-CF-21` `constraint` No image bytes exist on the app container filesystem, no image bytes exist in a database column `src: Core features rule 9`
- [ ] `C-CF-22` `capability` A published project poster is readable through the streaming endpoint by any request `src: Core features rule 10`
- [ ] `C-CF-23` `capability` An unpublished project poster is readable through the streaming endpoint only with the owner bearer token `src: Core features rule 10`
- [ ] `C-CF-24` `capability` Uploading one file twice for one project produces one stored object, one row `src: Core features rule 11`
- [ ] `C-CF-25` `capability` Every poster carries owner-written alternative text that travels with the image `src: Core features rule 11`
- [ ] `C-CF-26` `capability` Project order is walked from the adjacency relation, never derived from a date field `src: Core features rule 13`
- [ ] `C-CF-27` `capability` The text route lists published projects only, in adjacency order `src: Core features rule 16`
- [ ] `C-CF-28` `capability` Every internal link on every public surface resolves rather than answering not-found `src: Core features rule 16`
- [ ] `C-CF-29` `capability` Exactly one consumer owns the keyboard at any moment, named on the root element `src: Core features rule 19`
- [ ] `C-CF-30` `capability` A whisper submission that fills the unlabelled decoy field is refused, writing nothing `src: Core features rule 39`
- [ ] `C-CF-31` `capability` A whisper submission arriving repeatedly from one visitor identifier inside a short window is refused `src: Core features rule 39`
- [ ] `C-CF-32` `literal` A first-time visitor is asked once about non-essential measurement, the answer stored under `cookie-choice`, surviving a reload `src: Core features rule 44`
- [ ] `C-CF-33` `capability` Every public page view is recorded with its route plus the moment, readable by the owner alone `src: Core features rule 43`
- [ ] `C-CF-34` `capability` A lap whose checkpoint splits do not sum to its stated duration is refused, recording nothing `src: Core features rule 34`
- [ ] `C-CF-35` `capability` The daily board holds the fastest lap per visitor for the current UTC day `src: Core features rule 35`
- [ ] `C-CF-36` `capability` The world stays fully explorable when the shared endpoints are unreachable, with no feature hidden `src: Core features rule 41`
- [ ] `C-CF-37` `capability` A write attempted against unreachable shared endpoints does nothing, queues nothing, replays nothing afterwards `src: Core features rule 41`
- [ ] `C-CF-38` `capability` Achievement progress survives a reload, held under browser keys tied to no account `src: Core features rule 26`
- [ ] `C-CF-39` `capability` Both achievement progress modes work: counting occurrences, collecting a distinct named group `src: Core features rule 27`
- [ ] `C-CF-40` `capability` The map is a top-down view of the world rendered at the moment of asking, never an authored picture `src: Core features rule 30`
- [ ] `C-CF-41` `capability` A whisper with an empty message, a missing country code, a message over the stated limit is rejected as invalid, writing nothing `src: Core features rule 38`

## C-UF User flow

- [ ] `C-UF-01` `capability` A request for a studio route without a valid session goes to the sign-in route, continuing afterwards to the route originally asked for `src: User flow Entry and redirects`
- [ ] `C-UF-02` `capability` An unknown address renders the product not-found page carrying a way back into the world `src: User flow Entry and redirects`
- [ ] `C-UF-03` `capability` Publishing lands the browser on a full confirmation page naming the project, naming its coordinates `src: User flow journey 7`
- [ ] `C-UF-04` `capability` A refused publish returns to the editing panel with the reason stated, nothing written `src: User flow journey 6`
- [ ] `C-UF-05` `ui` Writing a project opens a panel sliding in from the right edge over the list, the list staying visible behind `src: User flow journey 4`
- [ ] `C-UF-06` `capability` Every list carries an empty state saying what would be there `src: User flow States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The interface reads as a hairline drawing over a rendered scene, never as filled cards competing with the scene `src: UI/UX notes`
- [ ] `C-UX-02` `ui` One dark scheme only, with no light theme `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Three meaning-carrying colours are reserved, so a state that is none of the three borrows none of them `src: UI/UX notes`
- [ ] `C-UX-04` `ui` A surface takes an inset hairline rather than a border, brightening when pointed at `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Interface motion runs at two speeds only, with entrance easing differing from exit easing `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Each surface leads with one primary action, visually distinct from every secondary one `src: UI/UX notes`
- [ ] `C-UX-07` `constraint` Body text meets WCAG AA contrast against its ground, touch targets stay comfortably sized `src: UI/UX notes`
- [ ] `C-UX-08` `constraint` Keyboard navigation reaches every overlay with a visible focus ring, focus staying inside an open overlay, returning on close `src: UI/UX notes`
- [ ] `C-UX-09` `ui` The interface layer steps down twice as the window narrows, with the menu reorienting by the shape of its frame rather than by a pixel count `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The server renders the HTML for every address, so the browser receives a rendered document on first paint `src: Technical requirements`
- [ ] `C-TR-02` `literal` PostgreSQL is reached at `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-03` `literal` MinIO is reached at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` `src: Technical requirements`
- [ ] `C-TR-04` `capability` A shared value on an already open page changes without a page reload `src: Technical requirements`
- [ ] `C-TR-05` `contract` The root element carries six class families whose exact names are contract `src: Technical requirements`
- [ ] `C-TR-06` `contract` Exactly one input-filter class is present at any moment, naming the single consumer owning the keyboard `src: Technical requirements`
- [ ] `C-TR-07` `contract` Behaviour hooks are prefixed separately from styling names, so neither depends on the other `src: Technical requirements`
- [ ] `C-TR-08` `capability` The interface layer never waits on the world, so an overlay opens at once whenever the world is still resolving `src: Technical requirements`
- [ ] `C-TR-09` `capability` Local persistence uses three browser keys only, none synchronised anywhere `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Eleven tables exist, with all timestamps in UTC `src: Data model`
- [ ] `C-DM-02` `literal` The seeded account uses the password `deku-demo-pw-2026`, written into `/app/USER_README.md` `src: Data model`
- [ ] `C-DM-03` `data` A project row carries a unique slug, a title, a summary, a link, three world coordinates, a zone, two adjacency fields, a published flag, a published timestamp `src: Data model project`
- [ ] `C-DM-04` `data` At most one project with the published flag set exists for any one combination of the three world coordinates `src: Data model project`
- [ ] `C-DM-05` `data` A project may not name itself as its own previous or next `src: Data model project`
- [ ] `C-DM-06` `data` A project image row holds the object key, never the bytes `src: Data model project_image`
- [ ] `C-DM-07` `data` At most 30 whisper rows exist, with at most one row per visitor identifier `src: Data model whisper`
- [ ] `C-DM-08` `literal` Four projects are seeded: `Lantern Run`, `Paper Tide`, `Copper Garden` published, `Night Ferry` held as a draft `src: Data model Seed data`
- [ ] `C-DM-09` `data` Seeding is idempotent, so restarting the app duplicates no rows `src: Data model Seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The type scale is carried exactly, stepping as a set against a root size `src: Front-end specification type scale`
- [ ] `C-FE-02` `ui` Every appearance uses the two-phase display-then-visible sequence, so nothing arrives without its fade `src: Front-end specification motion moments`
- [ ] `C-FE-03` `ui` Nothing scrolls the document itself, so the only scrolling regions sit inside panels `src: Front-end specification two layers`
- [ ] `C-FE-04` `ui` Loading progress is an arc closing into an ellipse, carrying no percentage, no bar, no word `src: Front-end specification the opening`
- [ ] `C-FE-05` `literal` The call to action reads `CLICK TO START` beside the island, in the display face `src: Front-end specification the opening`
- [ ] `C-FE-06` `ui` Two stacked triggers sit at the right edge, absent until the visitor has started `src: Front-end specification edge triggers`
- [ ] `C-FE-07` `ui` Six menu contents live behind one shell, so switching never remounts the shell `src: Front-end specification the menu`
- [ ] `C-FE-08` `literal` The options content carries the rows `Audio`, `Quality`, `I'm stuck!`, `Reset`, `Renderer`, `Server` `src: Front-end specification the menu`
- [ ] `C-FE-09` `ui` The controls content is the one surface answering window height, tightening row spacing as the window shortens `src: Front-end specification the menu`
- [ ] `C-FE-10` `ui` A map location label reveals on hover with a pointer, standing permanently on a touch device `src: Front-end specification the map`
- [ ] `C-FE-11` `ui` A locked reward is shown behind a scrim rather than hidden `src: Front-end specification achievements`
- [ ] `C-FE-12` `ui` An empty daily board shows one stated line rather than an empty table `src: Front-end specification the circuit`
- [ ] `C-FE-13` `ui` The whisper submit control starts visibly inert, lighting up only once the message can be sent `src: Front-end specification the whisper composer`
- [ ] `C-FE-14` `literal` The document title is `Marek's`, the description is `Marek Vance's creative portfolio` `src: Front-end specification document metadata`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No visitor account exists, no signup exists, no password reset exists for anyone `src: Constraints`
- [ ] `C-CN-02` `constraint` No comment, no like, no follow, no visitor-to-visitor message exists `src: Constraints`
- [ ] `C-CN-03` `constraint` No binary asset ships in the deployed build: no image file, no audio file, no model, no texture container, no video `src: Constraints`
- [ ] `C-CN-04` `constraint` Every public surface is reachable with no sign-in, so nothing on the world, the text route or an overlay demands an account `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`, both read from the environment `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served on that same origin under the `/api` prefix `src: Deployment contract`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the app is ready `src: Deployment contract`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md` `src: Deployment contract`
- [ ] `C-DC-07` `contract` Reserved `.browser_screenshots/` plus `.downloads/` directories exist at the app root, empty `src: Deployment contract`
- [ ] `C-DC-08` `contract` A production build is served behind a static or preview server, never a dev server `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends, never a child of the shell `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0`, never `127.0.0.1` or `localhost` `src: Deployment contract`
- [ ] `C-DC-11` `contract` The named backing services are already running, so none is downloaded, installed, compiled, started `src: Deployment contract`
- [ ] `C-DC-12` `contract` `GET /api/world` returns the published projects together with the areas as one object `src: Deployment contract API shapes`
- [ ] `C-DC-13` `contract` `GET /api/projects` returns a top-level JSON array of published projects `src: Deployment contract API shapes`
- [ ] `C-DC-14` `contract` `GET /api/whispers` returns a top-level JSON array of at most 30 whispers `src: Deployment contract API shapes`
- [ ] `C-DC-15` `contract` An invalid or unauthorized call is rejected as a client error, never as a server error, never as a silent success `src: Deployment contract API shapes`
- [ ] `C-DC-16` `contract` Poster bytes exist as real objects in the MinIO bucket at their scheme key `src: Deployment contract No mocks`
- [ ] `C-DC-17` `constraint` The publish refusal is a property of the stored data, never of one request handler memory `src: Deployment contract No mocks`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `owner@example.com` | the seeded owner email | `C-CF-01` |
| `deku-demo-pw-2026` | the corpus password | `C-CF-01` |
| `POST /api/auth/login` | the sign-in endpoint | `C-CF-01` |
| `access_token` | the bearer token field | `C-CF-01` |
| `coordinates_occupied` | the exclusive-placement error code | `C-CF-11` |
| `Another published project already stands at those coordinates.` | the exclusive-placement message | `C-CF-12` |
| `poster_required` | the missing-poster error code | `C-CF-19` |
| `projects/{project_id}/posters/{sha256_of_bytes}.{ext}` | the object key scheme | `C-CF-20` |
| `cookie-choice` | the stored cookie answer key | `C-CF-32` |
| `DATABASE_URL` | the database environment variable | `C-TR-02` |
| `STORAGE_ENDPOINT` | the object store endpoint variable | `C-TR-03` |
| `STORAGE_BUCKET` | the bucket name variable | `C-TR-03` |
| `STORAGE_ACCESS_KEY` | the object store access key variable | `C-TR-03` |
| `STORAGE_SECRET_KEY` | the object store secret key variable | `C-TR-03` |
| `/app/USER_README.md` | the credentials file | `C-DM-02` |
| `Lantern Run` | the first seeded published project | `C-DM-08` |
| `Paper Tide` | the second seeded published project | `C-DM-08` |
| `Copper Garden` | the third seeded published project | `C-DM-08` |
| `Night Ferry` | the seeded draft project | `C-DM-08` |
| `CLICK TO START` | the opening call to action | `C-FE-05` |
| `Audio` | the first options row label | `C-FE-08` |
| `Quality` | the second options row label | `C-FE-08` |
| `I'm stuck!` | the recovery row label | `C-FE-08` |
| `Reset` | the reset row label | `C-FE-08` |
| `Renderer` | the renderer status row label | `C-FE-08` |
| `Server` | the connection status row label | `C-FE-08` |
| `No score yet today` | the empty leaderboard line | `C-FE-12` |
| `Marek's` | the document title | `C-FE-14` |
| `Marek Vance's creative portfolio` | the document description | `C-FE-14` |
| `APP_PUBLIC_URL` | the public address variable | `C-DC-01` |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | `C-DC-02` |
| `/api` | the API prefix | `C-DC-03` |
| `GET /api/health` | the health endpoint | `C-DC-04` |
| `200` | the health response status | `C-DC-04` |
| `.browser_screenshots/` | the first reserved directory | `C-DC-07` |
| `.downloads/` | the second reserved directory | `C-DC-07` |
| `0.0.0.0` | the bind address | `C-DC-10` |
| `127.0.0.1` | the forbidden bind address | `C-DC-10` |
| `localhost` | the forbidden bind hostname | `C-DC-10` |
| `GET /api/projects` | the public project list endpoint | `C-DC-13` |
| `GET /api/whispers` | the public whisper list endpoint | `C-DC-14` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact world coordinates each seeded project holds | `C-DM-08` |
| the reset moment at which the daily board clears | `C-DM-01` |
| the short window within which a repeated whisper is refused | `C-CF-30` |
| the range at which an interactive point raises its affordance | `C-OV-02` |
| the number of play areas beyond the required three | `C-OV-01` |
| the exact shades, spacings, radii, durations left to the builder | `C-UX-02` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 1 | 3 |
| User roles | 1 | 6 |
| Core features | 24 | 41 |
| User flow | 4 | 6 |
| UI and UX notes | 5 | 9 |
| Technical requirements | 7 | 9 |
| Data model | 7 | 9 |
| Front-end specification | 13 | 14 |
| Constraints | 2 | 4 |
| Deployment contract | 16 | 17 |
