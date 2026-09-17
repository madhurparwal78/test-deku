# Checklist: Vellum - Audio Gated Portfolio
Items: 194
Unpinned values flagged: 5
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-CN, C-TR, C-DM, C-DC, C-FE

## C-OV Overview
- [ ] `C-OV-01` `capability` The product serves one public showcase site for a brand studio. `src: Overview`
- [ ] `C-OV-02` `capability` A signed-in console lets the studio publish its own work. `src: Overview`
- [ ] `C-OV-03` `capability` The public site collects one new-business enquiry action. `src: Overview`
- [ ] `C-OV-04` `constraint` A draft project stays unreachable to everyone but its own author. `src: Overview`

## C-RL User roles
- [ ] `C-RL-01` `role` An `author` creates, edits, publishes, unpublishes their own projects. `src: User roles`
- [ ] `C-RL-02` `role` An `author` uploads a poster onto an owned project. `src: User roles`
- [ ] `C-RL-03` `role` An `author` promotes one published project to `lead`. `src: User roles`
- [ ] `C-RL-04` `role` An `author` reads the enquiry queue. `src: User roles`
- [ ] `C-RL-05` `role` An `author` cannot touch another author's project. `src: User roles`
- [ ] `C-RL-06` `role` A `reader` account reads published surfaces only. `src: User roles`
- [ ] `C-RL-07` `role` An anonymous visitor sends an enquiry without signing in. `src: User roles`
- [ ] `C-RL-08` `constraint` A direct API call from a `reader` session to an `author`-only endpoint is denied server-side. `src: User roles`
- [ ] `C-RL-09` `constraint` A denied mutating call leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-10` `constraint` Signup is open, creating a `reader` account. `src: User roles`
- [ ] `C-RL-11` `constraint` An `author` account is seeded only, never created by signup. `src: User roles`

## C-CF Core features
- [ ] `C-CF-01` `capability` Email plus password login issues a bearer token. `src: Core features, Auth`
- [ ] `C-CF-02` `constraint` An expired token on a mutating call is rejected. `src: Core features, Auth`
- [ ] `C-CF-03` `constraint` A rejected expired-token call leaves the record unchanged. `src: Core features, Auth`
- [ ] `C-CF-04` `capability` `/projects` lists published projects only. `src: Core features, The work`
- [ ] `C-CF-05` `capability` `GET /api/projects` returns published projects ordered by `position` ascending. `src: Core features, The work`
- [ ] `C-CF-06` `constraint` A draft project appears on neither the wall nor the projects endpoint. `src: Core features, The work`
- [ ] `C-CF-07` `constraint` A draft project route answers its own author alone. `src: Core features, The work`
- [ ] `C-CF-08` `constraint` An anonymous caller asking for a draft poster is refused. `src: Core features, The work`
- [ ] `C-CF-09` `constraint` A signed-in `reader` asking for a draft poster is refused. `src: Core features, The work`
- [ ] `C-CF-10` `constraint` The studio's other author asking for a draft poster is refused. `src: Core features, The work`
- [ ] `C-CF-11` `contract` Poster bytes live in the MinIO bucket under the pinned poster key scheme. `src: Core features, The work`
- [ ] `C-CF-12` `constraint` A poster key recorded for an object never written to the bucket is invalid. `src: Core features, The work`
- [ ] `C-CF-13` `capability` At most one project carries `lead` true at any moment. `src: Core features, The work`
- [ ] `C-CF-14` `constraint` Two simultaneous promotions of different projects leave exactly one winner. `src: Core features, The work`
- [ ] `C-CF-15` `constraint` A failed promotion leaves neither two lead rows nor zero lead rows. `src: Core features, The work`
- [ ] `C-CF-16` `capability` Filtering the wall by a facet re-lays the wall out with no page load. `src: Core features, The work`
- [ ] `C-CF-17` `capability` The active facet is reflected in the browser location. `src: Core features, The work`
- [ ] `C-CF-18` `capability` A back-navigation after filtering restores the previous set. `src: Core features, The work`
- [ ] `C-CF-19` `capability` `GET /api/projects?facet=Motion` returns the same set the facet pill shows. `src: Core features, The work`
- [ ] `C-CF-20` `constraint` A project slug is exactly two lowercase letters. `src: Core features, The work`
- [ ] `C-CF-21` `constraint` A project slug equal to a reserved top-level segment is rejected as invalid. `src: Core features, The work`
- [ ] `C-CF-22` `constraint` A rejected project creation stores nothing. `src: Core features, The work`
- [ ] `C-CF-23` `capability` The index route renders the intro overlay before any other content. `src: Core features, The gate`
- [ ] `C-CF-24` `constraint` No audio plays before an intro door is pressed. `src: Core features, The gate`
- [ ] `C-CF-25` `capability` Either intro door dismisses the overlay with no page reload. `src: Core features, The gate`
- [ ] `C-CF-26` `capability` The audio choice made at the intro holds for the rest of the session. `src: Core features, The gate`
- [ ] `C-CF-27` `data` `POST /api/enquiries` accepts a name, an email, a message, two optional fields. `src: Core features, The enquiry`
- [ ] `C-CF-28` `constraint` A missing enquiry name is rejected with a reason for that field. `src: Core features, The enquiry`
- [ ] `C-CF-29` `constraint` A malformed enquiry email is rejected with a reason for that field. `src: Core features, The enquiry`
- [ ] `C-CF-30` `constraint` A rejected enquiry submission stores nothing. `src: Core features, The enquiry`
- [ ] `C-CF-31` `capability` A stored enquiry is durable before the response is sent. `src: Core features, The enquiry`
- [ ] `C-CF-32` `data` A stored enquiry response carries a reference. `src: Core features, The enquiry`
- [ ] `C-CF-33` `constraint` A repeat enquiry with an identical email plus message stores one row. `src: Core features, The enquiry`
- [ ] `C-CF-34` `constraint` A repeat enquiry with an identical email plus message returns the first reference. `src: Core features, The enquiry`
- [ ] `C-CF-35` `constraint` An enquiry carrying a value in the honeypot field stores nothing. `src: Core features, The enquiry`
- [ ] `C-CF-36` `constraint` An enquiry carrying a value in the honeypot field answers as a stored one does. `src: Core features, The enquiry`
- [ ] `C-CF-37` `capability` Every public route's footer links to the terms page. `src: Core features, The rest of the site`
- [ ] `C-CF-38` `constraint` Every internal link on every public route resolves. `src: Core features, The rest of the site`

## C-UF User flow
- [ ] `C-UF-01` `capability` `/` is the index route carrying the intro gate. `src: User flow`
- [ ] `C-UF-02` `capability` `/projects` is the filterable wall of published work. `src: User flow`
- [ ] `C-UF-03` `capability` `/world` is the drag-to-explore scene route. `src: User flow`
- [ ] `C-UF-04` `capability` `/contact` carries the studio details plus the enquiry form. `src: User flow`
- [ ] `C-UF-05` `capability` A two-letter top-level segment resolves one case study. `src: User flow`
- [ ] `C-UF-06` `capability` `/login` signs an existing account in. `src: User flow`
- [ ] `C-UF-07` `capability` `/signup` creates a reader account. `src: User flow`
- [ ] `C-UF-08` `capability` `/studio/projects` shows the project table to an `author`. `src: User flow`
- [ ] `C-UF-09` `capability` `/studio/enquiries` shows the enquiry queue to an `author`. `src: User flow`
- [ ] `C-UF-10` `constraint` An anonymous request to a studio route lands on `/login`. `src: User flow`
- [ ] `C-UF-11` `capability` Signing in returns to the requested studio route. `src: User flow`
- [ ] `C-UF-12` `constraint` A signed-in `reader` asking for a studio route is refused. `src: User flow`
- [ ] `C-UF-13` `capability` Signing in sends an `author` to `/studio/projects`. `src: User flow`
- [ ] `C-UF-14` `capability` Signing in sends a `reader` to `/`. `src: User flow`
- [ ] `C-UF-15` `constraint` Signing out invalidates the bearer token. `src: User flow`
- [ ] `C-UF-16` `constraint` An unknown path renders the not-found surface. `src: User flow`
- [ ] `C-UF-17` `constraint` A draft route asked for by anyone but its owner renders the not-found surface. `src: User flow`
- [ ] `C-UF-18` `ui` Every list surface has an empty state naming what would appear there. `src: User flow`
- [ ] `C-UF-19` `ui` Every route has a loading state. `src: User flow`
- [ ] `C-UF-20` `ui` A failed request shows a message without breaking the page. `src: User flow`

## C-UX UI and UX notes
- [ ] `C-UX-01` `ui` The studio console reads command-line in character. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` Console type is monospace everywhere. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Console motion character is instant, with nothing easing in. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Console density is compact, so a full project table fits one screen. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The console layout archetype is a fixed side rail beside a table. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` A saved console row appears before the server answers. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` A saved console row corrects itself when the server disagrees. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Public routes carry one blush ground under near-black ink. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` The coral accent belongs to the intro gate alone. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` One curve carries every public transition. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Every control has resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Escape closes whatever opened over the page. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Unpublishing asks for confirmation first. `src: UI/UX notes`
- [ ] `C-UX-14` `constraint` Text plus controls meet WCAG AA contrast. `src: UI/UX notes`
- [ ] `C-UX-15` `constraint` Every control is reachable by keyboard with a visible focus ring. `src: UI/UX notes`
- [ ] `C-UX-16` `constraint` Icon-only controls carry labels. `src: UI/UX notes`
- [ ] `C-UX-17` `constraint` Meaning is never carried by colour alone. `src: UI/UX notes`
- [ ] `C-UX-18` `constraint` Layout holds at every viewport width between the named tiers. `src: UI/UX notes`

## C-CN Constraints
- [ ] `C-CN-01` `constraint` The product is single tenant. `src: Constraints`
- [ ] `C-CN-02` `constraint` No comments surface exists. `src: Constraints`
- [ ] `C-CN-03` `constraint` No search surface exists. `src: Constraints`
- [ ] `C-CN-04` `constraint` No email is sent by the product. `src: Constraints`
- [ ] `C-CN-05` `constraint` No payment surface exists. `src: Constraints`
- [ ] `C-CN-06` `constraint` No third-party analytics tag is loaded. `src: Constraints`
- [ ] `C-CN-07` `constraint` No outbound network call happens at run time. `src: Constraints`
- [ ] `C-CN-08` `constraint` The build ships no binary asset. `src: Constraints`
- [ ] `C-CN-09` `constraint` PostgreSQL plus MinIO are the only backing services. `src: Constraints`
- [ ] `C-CN-10` `constraint` The app stays responsive with two hundred projects. `src: Constraints`

## C-TR Technical requirements
- [ ] `C-TR-01` `contract` The frontend is Astro with islands. `src: Technical requirements`
- [ ] `C-TR-02` `contract` The HTTP API is served under the `/api` prefix on the app origin. `src: Technical requirements`
- [ ] `C-TR-03` `contract` Route markup arrives on first paint before any script runs. `src: Technical requirements`
- [ ] `C-TR-04` `contract` PostgreSQL is reached at `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-05` `contract` MinIO is reached at `STORAGE_ENDPOINT`. `src: Technical requirements`
- [ ] `C-TR-06` `contract` The bucket name comes from `STORAGE_BUCKET`. `src: Technical requirements`
- [ ] `C-TR-07` `contract` Storage credentials come from the pinned storage key variables. `src: Technical requirements`
- [ ] `C-TR-08` `contract` The app origin comes from `APP_PUBLIC_URL`. `src: Technical requirements`
- [ ] `C-TR-09` `contract` The app port comes from `APP_PUBLIC_PORT`. `src: Technical requirements`
- [ ] `C-TR-10` `constraint` No host is hardcoded anywhere in the app. `src: Technical requirements`
- [ ] `C-TR-11` `contract` Passwords are stored hashed. `src: Technical requirements`
- [ ] `C-TR-12` `contract` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements`
- [ ] `C-TR-13` `contract` Block media keys follow the pinned block key scheme. `src: Technical requirements`
- [ ] `C-TR-14` `constraint` An accepted poster is a PNG or a JPEG at most 8388608 bytes. `src: Technical requirements`
- [ ] `C-TR-15` `constraint` A poster type is decided by reading the content, never the extension. `src: Technical requirements`
- [ ] `C-TR-16` `contract` Protected media uses one of the two named mechanisms consistently. `src: Technical requirements`
- [ ] `C-TR-17` `constraint` A presigned URL for protected media lasts at most five minutes. `src: Technical requirements`
- [ ] `C-TR-18` `capability` The whole page scrolls from a transformed scroll surface, not natively. `src: Technical requirements`
- [ ] `C-TR-19` `capability` One normalised progress value drives the scene camera. `src: Technical requirements`
- [ ] `C-TR-20` `constraint` Nothing reads the native scroll offset. `src: Technical requirements`
- [ ] `C-TR-21` `constraint` No second frame timer runs anywhere. `src: Technical requirements`
- [ ] `C-TR-22` `capability` The scene sheds particles first under load. `src: Technical requirements`
- [ ] `C-TR-23` `capability` The ambient bed is shaped through a filter node in the browser audio graph. `src: Technical requirements`
- [ ] `C-TR-24` `constraint` The build ships no font file. `src: Technical requirements`
- [ ] `C-TR-25` `constraint` Every response carries the standard security headers. `src: Technical requirements`
- [ ] `C-TR-26` `constraint` No credential appears in anything the browser downloads. `src: Technical requirements`
- [ ] `C-TR-27` `contract` The site serves a favicon, declared in the document head. `src: Technical requirements`

## C-DM Data model
- [ ] `C-DM-01` `data` Seven tables carry the whole model. `src: Data model`
- [ ] `C-DM-02` `data` All timestamps are UTC. `src: Data model`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model`
- [ ] `C-DM-04` `data` A user email is unique, case-insensitive. `src: Data model`
- [ ] `C-DM-05` `data` A user role is either `author` or `reader`. `src: Data model`
- [ ] `C-DM-06` `data` A project slug is unique across the whole table. `src: Data model`
- [ ] `C-DM-07` `data` Project facets hold one to three of the three named facet values. `src: Data model`
- [ ] `C-DM-08` `data` A project publication timestamp is non-null exactly when the status is published. `src: Data model`
- [ ] `C-DM-09` `data` A project lead flag is true only on a published row. `src: Data model`
- [ ] `C-DM-10` `data` A project block kind is one of the four named kinds. `src: Data model`
- [ ] `C-DM-11` `data` Project blocks are ordered by position. `src: Data model`
- [ ] `C-DM-12` `data` Project awards are ordered by position. `src: Data model`
- [ ] `C-DM-13` `data` An enquiry reference is unique. `src: Data model`
- [ ] `C-DM-14` `data` The site globals table holds exactly one row. `src: Data model`
- [ ] `C-DM-15` `data` Facet counts are derived on read, never stored. `src: Data model`
- [ ] `C-DM-16` `literal` The seeded author accounts are `author@example.com`, `author2@example.com`. `src: Data model`
- [ ] `C-DM-17` `literal` The seeded reader account is `reader@example.com`. `src: Data model`
- [ ] `C-DM-18` `data` Four projects are seeded across the two publication statuses. `src: Data model`
- [ ] `C-DM-19` `data` The seeded draft project carries a poster object in the bucket. `src: Data model`
- [ ] `C-DM-20` `data` The seeded lead project carries five ordered blocks. `src: Data model`
- [ ] `C-DM-21` `data` The seeded lead project carries two ordered awards. `src: Data model`
- [ ] `C-DM-22` `literal` One enquiry with reference `ENQ-1001` is seeded. `src: Data model`
- [ ] `C-DM-23` `literal` The studio contact address is `projects@vellum.co`. `src: Data model`
- [ ] `C-DM-24` `constraint` Seeding is idempotent across a restart. `src: Data model`

## C-DC Deployment contract
- [ ] `C-DC-01` `contract` The app is reachable at the public origin variable. `src: Deployment contract`
- [ ] `C-DC-02` `contract` The container-internal port is `4173`. `src: Deployment contract`
- [ ] `C-DC-03` `contract` The health endpoint answers `200` once ready. `src: Deployment contract`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-05` `contract` A production build is served behind a static or preview server. `src: Deployment contract`
- [ ] `C-DC-06` `contract` The server outlives the shell that started the server. `src: Deployment contract`
- [ ] `C-DC-07` `contract` The listener binds `0.0.0.0`. `src: Deployment contract`
- [ ] `C-DC-08` `data` Every listed endpoint uses the exact field names given. `src: Deployment contract`
- [ ] `C-DC-09` `data` A list endpoint returns a top-level JSON array. `src: Deployment contract`
- [ ] `C-DC-10` `constraint` An invalid call is rejected as a client error, never a server error. `src: Deployment contract`
- [ ] `C-DC-11` `constraint` Poster bytes on the app container filesystem are a contract violation. `src: Deployment contract`
- [ ] `C-DC-12` `constraint` An in-memory list standing in for the projects table is a contract violation. `src: Deployment contract`

## C-FE Front-end specification
- [ ] `C-FE-01` `ui` Three circular corner controls are pinned on every route. `src: Front-end specification`
- [ ] `C-FE-02` `ui` The overlay menu carries four numbered destinations in fixed order. `src: Front-end specification`
- [ ] `C-FE-03` `ui` No persistent visible menu bar exists on any route. `src: Front-end specification`
- [ ] `C-FE-04` `literal` The primary ground is the blush `rgb(239, 222, 217)`. `src: Front-end specification`
- [ ] `C-FE-05` `literal` Ink is `#212121`. `src: Front-end specification`
- [ ] `C-FE-06` `literal` The loader accent box is the coral `#f6c8c3`. `src: Front-end specification`
- [ ] `C-FE-07` `ui` Root sizing is derived from the viewport, not fixed. `src: Front-end specification`
- [ ] `C-FE-08` `ui` Two families carry the public routes. `src: Front-end specification`
- [ ] `C-FE-09` `ui` The largest display tier uses the display serif italic. `src: Front-end specification`
- [ ] `C-FE-10` `ui` Every icon is inline vector geometry. `src: Front-end specification`
- [ ] `C-FE-11` `ui` The eyes mark blinks by sliding two mask rectangles. `src: Front-end specification`
- [ ] `C-FE-12` `ui` The eyes pupils morph to a heart on hover. `src: Front-end specification`
- [ ] `C-FE-13` `ui` A button fill wipes through an animated mask, never a background transition. `src: Front-end specification`
- [ ] `C-FE-14` `ui` Headings split into per-character elements before revealing. `src: Front-end specification`
- [ ] `C-FE-15` `ui` Scrolling backwards un-reveals split text. `src: Front-end specification`
- [ ] `C-FE-16` `ui` The loader boxes run an infinite four-second linear loop. `src: Front-end specification`
- [ ] `C-FE-17` `ui` A case study runs roughly seven to nine viewports tall. `src: Front-end specification`
- [ ] `C-FE-18` `ui` The filmstrip track translates sideways as the reader scrolls down. `src: Front-end specification`
- [ ] `C-FE-19` `ui` The awards list scrolls inside its own frame. `src: Front-end specification`
- [ ] `C-FE-20` `ui` The cursor circle trails the pointer with eased interpolation. `src: Front-end specification`
- [ ] `C-FE-21` `ui` The custom cursor is disabled on coarse pointers. `src: Front-end specification`
- [ ] `C-FE-22` `ui` The drag arrows appear in the cursor over a draggable scene. `src: Front-end specification`
- [ ] `C-FE-23` `constraint` A reduced-motion preference freezes the scene to a still composition. `src: Front-end specification`
- [ ] `C-FE-24` `constraint` Meshes are composed from primitives, never loaded as files. `src: Front-end specification`
- [ ] `C-FE-25` `constraint` Lighting textures are drawn on a canvas at load. `src: Front-end specification`
- [ ] `C-FE-26` `constraint` Project posters are seeded gradients keyed per project slug. `src: Front-end specification`
- [ ] `C-FE-27` `literal` The home document title is `Vellum - Brand, Digital & Motion`. `src: Front-end specification`
- [ ] `C-FE-28` `ui` Delivery prerenders every route's copy at the server. `src: Front-end specification`
- [ ] `C-FE-29` `ui` The contact route lays out two columns on desktop, stacking on mobile. `src: Front-end specification`
- [ ] `C-FE-30` `ui` Screen-reader-only labels use the visually-hidden clip pattern. `src: Front-end specification`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the seeded account password | `C-DM-03` |
| `author@example.com` | the first studio author | `C-DM-16` |
| `author2@example.com` | the second studio author | `C-DM-16` |
| `reader@example.com` | the seeded reader account | `C-DM-17` |
| `ENQ-1001` | the seeded enquiry reference | `C-DM-22` |
| `projects@vellum.co` | the studio new-business address | `C-DM-23` |
| `rgb(239, 222, 217)` | the blush ground | `C-FE-04` |
| `#212121` | the near-black ink | `C-FE-05` |
| `#f6c8c3` | the coral loader accent | `C-FE-06` |
| `Vellum - Brand, Digital & Motion` | the home document title | `C-FE-27` |
| `/projects` | the wall of published work | `C-CF-04` |
| `GET /api/projects` | the published projects endpoint | `C-CF-05` |
| `GET /api/projects?facet=Motion` | the facet-filtered projects endpoint | `C-CF-19` |
| `position` | the project ordering field | `C-CF-05` |
| `lead` | the single-lead flag | `C-CF-13` |
| `POST /api/enquiries` | the new-business endpoint | `C-CF-27` |
| `GET /api/health` | the readiness endpoint | `C-TR-12` |
| `200` | the ready response status | `C-TR-12` |
| `/api` | the API prefix | `C-TR-02` |
| `DATABASE_URL` | the PostgreSQL connection variable | `C-TR-04` |
| `STORAGE_ENDPOINT` | the MinIO endpoint variable | `C-TR-05` |
| `STORAGE_BUCKET` | the bucket-name variable | `C-TR-06` |
| `APP_PUBLIC_URL` | the public origin variable | `C-TR-08` |
| `APP_PUBLIC_PORT` | the public port variable | `C-TR-09` |
| `8388608` | the poster byte ceiling | `C-TR-14` |
| `4173` | the container-internal port | `C-DC-02` |
| `/app/USER_README.md` | the credentials file | `C-DC-05` |
| `.browser_screenshots/` | the reserved screenshot directory | `C-DC-06` |
| `.downloads/` | the reserved download directory | `C-DC-07` |
| `0.0.0.0` | the bind address | `C-DC-07` |
| `author` | the studio role | `C-DM-05` |
| `reader` | the visitor role | `C-DM-05` |
| `/login` | the sign-in route | `C-UF-06` |
| `/signup` | the open signup route | `C-UF-07` |
| `/studio/projects` | the studio project table route | `C-UF-08` |
| `/studio/enquiries` | the studio enquiry queue route | `C-UF-09` |
| `/contact` | the contact route | `C-UF-04` |
| `/world` | the drag-to-explore route | `C-UF-03` |
| `/` | the index route | `C-UF-01` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact wording of every inline field error message | `C-CF-28` |
| the camera keyframe path through the room, marked inferred | `C-TR-19` |
| the butterfly wing flap loop, marked inferred | `C-FE-24` |
| the exact hex of the failure, success, in-progress signal colours | `C-UX-17` |
| the chosen grotesque, the chosen display serif | `C-FE-08` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 1 | 4 |
| User roles | 4 | 11 |
| Core features | 7 | 38 |
| User flow | 7 | 20 |
| UI and UX notes | 2 | 18 |
| Constraints | 1 | 10 |
| Technical requirements | 5 | 27 |
| Data model | 6 | 24 |
| Deployment contract | 9 | 12 |
| Front-end specification | 14 | 30 |
