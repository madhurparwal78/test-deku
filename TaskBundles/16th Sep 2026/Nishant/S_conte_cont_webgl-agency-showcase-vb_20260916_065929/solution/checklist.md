# Checklist: Spectre Studio Showcase

Source: instruction.md
Sections present: overview, roles, features, enquirycareers, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 503
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public studio site for clients, candidates, press. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app serves a private publishing console for the studio curator. `src: Overview para 1`
- [ ] `C-OV-03` `capability` The home route presents published projects as a draggable throwable wall. `src: Overview para 2`
- [ ] `C-OV-04` `constraint` The app offers no comments feature. `src: Overview para 2`
- [ ] `C-OV-05` `constraint` The app offers no likes feature. `src: Overview para 2`
- [ ] `C-OV-06` `constraint` The app offers no payment feature. `src: Overview para 2`
- [ ] `C-OV-07` `constraint` The app is not a client portal. `src: Overview para 2`
- [ ] `C-OV-08` `constraint` An unpublished project stays unreadable to everyone other than a signed-in curator. `src: Overview para 3`
- [ ] `C-OV-09` `constraint` The stored image of an unpublished project stays unreadable on direct request. `src: Overview para 3`

## C-RL User roles

- [ ] `C-RL-01` `role` A `visitor` reads published projects. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A `visitor` reads the images of published projects. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A `visitor` reads the open roles list. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A `visitor` reads the site configuration. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A `visitor` submits an enquiry. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A `visitor` submits a wildcard application carrying one file. `src: User roles table row 1`
- [ ] `C-RL-07` `role` A `visitor` is denied any read of a draft project. `src: User roles table row 1`
- [ ] `C-RL-08` `role` A `visitor` is denied the image bytes behind a draft project. `src: User roles table row 1`
- [ ] `C-RL-09` `role` A `visitor` is denied any read of a closed role. `src: User roles table row 1`
- [ ] `C-RL-10` `role` A `visitor` is denied creating a project. `src: User roles table row 1`
- [ ] `C-RL-11` `role` A `visitor` is denied uploading to a project. `src: User roles table row 1`
- [ ] `C-RL-12` `role` A `visitor` is denied publishing a project. `src: User roles table row 1`
- [ ] `C-RL-13` `role` A `visitor` is denied reading the enquiry inbox. `src: User roles table row 1`
- [ ] `C-RL-14` `role` A `visitor` is denied reading the application inbox. `src: User roles table row 1`
- [ ] `C-RL-15` `role` A `curator` creates a project. `src: User roles table row 2`
- [ ] `C-RL-16` `role` A `curator` uploads a project thumbnail. `src: User roles table row 2`
- [ ] `C-RL-17` `role` A `curator` publishes a project. `src: User roles table row 2`
- [ ] `C-RL-18` `role` A `curator` reads a draft project. `src: User roles table row 2`
- [ ] `C-RL-19` `role` A `curator` reads closed roles. `src: User roles table row 2`
- [ ] `C-RL-20` `role` A `curator` reads both inboxes. `src: User roles table row 2`
- [ ] `C-RL-21` `role` Signup never creates a `curator` account. `src: User roles table row 2, para 3`
- [ ] `C-RL-22` `constraint` The server enforces authorization on every mutating endpoint. `src: User roles para 2`
- [ ] `C-RL-23` `constraint` A direct API call from a `visitor` session to a curator-only endpoint is denied. `src: User roles para 2`
- [ ] `C-RL-24` `constraint` A denied call leaves the protected state unchanged. `src: User roles para 2`
- [ ] `C-RL-25` `capability` Signup is open to anyone. `src: User roles para 3`
- [ ] `C-RL-26` `literal` The seeded curator account is `curator@example.com`. `src: User roles para 3`
- [ ] `C-RL-27` `literal` The seeded visitor account is `visitor@example.com`. `src: User roles para 3`
- [ ] `C-RL-28` `literal` Both seeded accounts use the password `deku-demo-pw-2026`. `src: User roles para 3`

## C-CF Core features

- [ ] `C-CF-01` `capability` The app authenticates a user by email address plus password. `src: Technical requirements, auth para`
- [ ] `C-CF-02` `constraint` The app stores every password hashed. `src: Technical requirements, auth para`
- [ ] `C-CF-03` `capability` Login returns a bearer token. `src: Technical requirements, auth para`
- [ ] `C-CF-04` `literal` The client sends the token as `Authorization: Bearer <token>`. `src: Technical requirements, auth para`
- [ ] `C-CF-05` `constraint` Login, signup, health require no bearer token. `src: Technical requirements, auth para`
- [ ] `C-CF-06` `literal` A token expires after `24 hours`. `src: Technical requirements, auth para`
- [ ] `C-CF-07` `constraint` An expired token is refused. `src: Technical requirements, auth para`
- [ ] `C-CF-08` `constraint` Signup always produces a `visitor`. `src: Technical requirements, auth para`
- [ ] `C-CF-09` `constraint` The app offers no password reset. `src: Technical requirements, auth para`
- [ ] `C-CF-10` `data` A project carries a `status` of exactly `draft` or `published`. `src: Core features, catalogue rule 1`
- [ ] `C-CF-11` `constraint` Creating a project always produces `draft`. `src: Core features, catalogue rule 1`
- [ ] `C-CF-12` `capability` Publishing a project is a separate explicit action. `src: Core features, catalogue rule 1`
- [ ] `C-CF-13` `constraint` The public catalogue holds published projects only. `src: Core features, catalogue rule 2`
- [ ] `C-CF-14` `constraint` A draft project is absent from the public catalogue. `src: Core features, catalogue rule 2`
- [ ] `C-CF-15` `constraint` A direct request for a draft by slug from an anonymous session is refused. `src: Core features, catalogue rule 2`
- [ ] `C-CF-16` `constraint` A direct request for a draft by slug from a `visitor` session is refused. `src: Core features, catalogue rule 2`
- [ ] `C-CF-17` `constraint` A refused draft request serves no partial project. `src: Core features, catalogue rule 2`
- [ ] `C-CF-18` `capability` The canvas header shows the live count of published projects computed on read. `src: Core features, catalogue rule 3`
- [ ] `C-CF-19` `literal` The canvas header reads `6 projects` against the shipped seed. `src: Core features, catalogue rule 3`
- [ ] `C-CF-20` `literal` The canvas header reads `7 projects` once a seventh project is published. `src: Core features, catalogue rule 3`
- [ ] `C-CF-21` `capability` Public ordering runs `display_order` ascending then `published_at` newest first. `src: Core features, catalogue rule 4`
- [ ] `C-CF-22` `constraint` Filtering by discipline never exposes a draft. `src: Core features, catalogue rule 4`
- [ ] `C-CF-23` `constraint` Filtering by tag never exposes a draft. `src: Core features, catalogue rule 4`
- [ ] `C-CF-24` `capability` The publish wizard runs three steps named details, media, review. `src: Core features, publishing rule 1`
- [ ] `C-CF-25` `constraint` Each publish wizard step has its own address. `src: Core features, publishing rule 1`
- [ ] `C-CF-26` `constraint` Stepping back in the wizard discards nothing already entered. `src: Core features, publishing rule 1`
- [ ] `C-CF-27` `capability` Wizard step two uploads exactly one image into `minio`. `src: Core features, publishing rule 2`
- [ ] `C-CF-28` `literal` An uploaded project image is stored under `projects/{project_id}/{sha256_of_bytes}.{ext}`. `src: Core features, publishing rule 2`
- [ ] `C-CF-29` `constraint` Project image bytes are absent from the app filesystem. `src: Core features, publishing rule 2`
- [ ] `C-CF-30` `constraint` Project image bytes are absent from any database column. `src: Core features, publishing rule 2`
- [ ] `C-CF-31` `data` A project `slug` is unique. `src: Core features, publishing rule 3`
- [ ] `C-CF-32` `constraint` A second create with a taken slug is rejected as invalid. `src: Core features, publishing rule 3`
- [ ] `C-CF-33` `constraint` A rejected create leaves no project row. `src: Core features, publishing rule 3`
- [ ] `C-CF-34` `constraint` A rejected create leaves no stored object. `src: Core features, publishing rule 3`
- [ ] `C-CF-35` `capability` Publishing sets `status` to `published`. `src: Core features, publishing rule 4`
- [ ] `C-CF-36` `capability` Publishing stamps `published_at` once. `src: Core features, publishing rule 4`
- [ ] `C-CF-37` `constraint` Publishing an already published project changes nothing. `src: Core features, publishing rule 4`
- [ ] `C-CF-38` `constraint` Publishing an already published project is not an error. `src: Core features, publishing rule 4`
- [ ] `C-CF-39` `capability` One authenticated route on the app origin serves image bytes. `src: Core features, visibility rule 1`
- [ ] `C-CF-40` `capability` The image route answers any caller for a published project. `src: Core features, visibility rule 1`
- [ ] `C-CF-41` `constraint` The image route answers only a signed-in `curator` for a draft project. `src: Core features, visibility rule 1`
- [ ] `C-CF-42` `constraint` An anonymous request for a draft project image is denied. `src: Core features, visibility rule 2`
- [ ] `C-CF-43` `constraint` A signed-in `visitor` request for a draft project image is denied. `src: Core features, visibility rule 2`
- [ ] `C-CF-44` `capability` A `curator` request for a draft project image returns the bytes. `src: Core features, visibility rule 2`
- [ ] `C-CF-45` `constraint` A denied image request returns no thumbnail. `src: Core features, visibility rule 3`
- [ ] `C-CF-46` `constraint` A denied image request returns no redirect to the store. `src: Core features, visibility rule 3`
- [ ] `C-CF-47` `constraint` A denied image request returns no presigned link. `src: Core features, visibility rule 3`
- [ ] `C-CF-48` `constraint` A denied image request leaves the stored object untouched. `src: Core features, visibility rule 3`
- [ ] `C-CF-49` `constraint` The public roles list holds open roles only. `src: Enquiry and careers, rule 1`
- [ ] `C-CF-50` `constraint` A closed role is absent from the public roles list. `src: Enquiry and careers, rule 1`
- [ ] `C-CF-51` `constraint` A direct request for a closed role from a non-curator session is refused. `src: Enquiry and careers, rule 1`
- [ ] `C-CF-52` `capability` The wildcard application accepts one file into `minio`. `src: Enquiry and careers, rule 2`
- [ ] `C-CF-53` `literal` A wildcard file is stored under `applications/{application_id}/{sha256_of_bytes}.{ext}`. `src: Enquiry and careers, rule 2`
- [ ] `C-CF-54` `literal` A wildcard application returns a reference shaped `WLD-00001`. `src: Enquiry and careers, rule 2`
- [ ] `C-CF-55` `data` Enquiry step one records `intent` as one of `collaboration`, `hiring`, `anything-else`. `src: Enquiry and careers, rule 3`
- [ ] `C-CF-56` `capability` The `anything-else` intent shows the direct contact details. `src: Enquiry and careers, rule 3`
- [ ] `C-CF-57` `constraint` The `anything-else` intent stores no enquiry form. `src: Enquiry and careers, rule 3`
- [ ] `C-CF-58` `data` Enquiry step two takes `readiness` as an integer `0`, `1`, `2`. `src: Enquiry and careers, rule 4`
- [ ] `C-CF-59` `capability` The readiness value comes from a three-stop slider. `src: Enquiry and careers, rule 4`
- [ ] `C-CF-60` `constraint` The enquiry full name field is required. `src: Enquiry and careers, rule 4`
- [ ] `C-CF-61` `constraint` The enquiry email field is required. `src: Enquiry and careers, rule 4`
- [ ] `C-CF-62` `constraint` The enquiry company field is required. `src: Enquiry and careers, rule 4`
- [ ] `C-CF-63` `constraint` The enquiry note field is optional. `src: Enquiry and careers, rule 4`
- [ ] `C-CF-64` `constraint` An enquiry missing a required field is rejected as invalid. `src: Enquiry and careers, rule 4`
- [ ] `C-CF-65` `constraint` A rejected enquiry keeps every value already entered. `src: Enquiry and careers, rule 4`
- [ ] `C-CF-66` `capability` A rejected enquiry names the field at fault. `src: Enquiry and careers, rule 4`
- [ ] `C-CF-67` `literal` A stored enquiry returns a reference shaped `ENQ-00001`. `src: Enquiry and careers, rule 5`
- [ ] `C-CF-68` `capability` The curator inbox shows the same enquiry reference returned to the sender. `src: Enquiry and careers, rule 5`
- [ ] `C-CF-69` `capability` A privacy page at `/privacy` is reachable from the footer of every route. `src: Core features, public pages rule 1`
- [ ] `C-CF-70` `capability` The privacy page states what the studio stores about an enquiry. `src: Core features, public pages rule 1`
- [ ] `C-CF-71` `capability` A terms page at `/terms` is reachable from the footer of every route. `src: Core features, public pages rule 2`
- [ ] `C-CF-72` `capability` The signup form links to the terms page beside its submit control. `src: Core features, public pages rule 2`
- [ ] `C-CF-73` `capability` An unknown address answers as not found rather than as a page that exists. `src: Core features, public pages rule 3`

## C-UF User flow

- [ ] `C-UF-01` `capability` The route `/` serves the throwable wall of published work. `src: User flow route table row 1`
- [ ] `C-UF-02` `capability` The route `/projects/:slug` serves one published project. `src: User flow route table row 2`
- [ ] `C-UF-03` `capability` The route `/about` serves the studio narrative with offices, team counts. `src: User flow route table row 3`
- [ ] `C-UF-04` `capability` The route `/careers` serves the studio spirit, open roles, the wildcard. `src: User flow route table row 4`
- [ ] `C-UF-05` `capability` The route `/contact` serves enquiry step one. `src: User flow route table row 5`
- [ ] `C-UF-06` `capability` The route `/contact/enquiry` serves enquiry step two. `src: User flow route table row 6`
- [ ] `C-UF-07` `capability` The route `/contact/complete` serves the enquiry confirmation. `src: User flow route table row 7`
- [ ] `C-UF-08` `capability` The route `/privacy` serves privacy, modern slavery, AI policy. `src: User flow route table row 8`
- [ ] `C-UF-09` `capability` The route `/login` serves sign in. `src: User flow route table row 9`
- [ ] `C-UF-10` `capability` The route `/signup` serves open registration. `src: User flow route table row 9`
- [ ] `C-UF-11` `capability` The route `/studio` lists draft projects beside published ones. `src: User flow route table row 10`
- [ ] `C-UF-12` `capability` The route `/studio/projects/new/details` serves wizard step one. `src: User flow route table row 11`
- [ ] `C-UF-13` `capability` The route `/studio/projects/new/media` serves wizard step two. `src: User flow route table row 12`
- [ ] `C-UF-14` `capability` The route `/studio/projects/new/review` serves wizard step three. `src: User flow route table row 13`
- [ ] `C-UF-15` `capability` The route `/studio/enquiries` serves the enquiry inbox. `src: User flow route table row 14`
- [ ] `C-UF-16` `constraint` Every `/studio` route requires a curator session. `src: User flow route table rows 10 to 14`
- [ ] `C-UF-17` `capability` An unauthenticated `/studio` request redirects to `/login`. `src: User flow, entry para`
- [ ] `C-UF-18` `capability` A successful sign in lands on the route originally asked for. `src: User flow, entry para`
- [ ] `C-UF-19` `constraint` A signed-in `visitor` at a `/studio` route is refused with a message. `src: User flow, entry para`
- [ ] `C-UF-20` `constraint` A signed-in `visitor` at a `/studio` route is never looped back to sign in. `src: User flow, entry para`
- [ ] `C-UF-21` `capability` A `curator` lands on `/studio` after login. `src: User flow, entry para`
- [ ] `C-UF-22` `capability` A `visitor` lands on `/` after login. `src: User flow, entry para`
- [ ] `C-UF-23` `capability` Logout discards the token. `src: User flow, entry para`
- [ ] `C-UF-24` `capability` Logout lands on `/`. `src: User flow, entry para`
- [ ] `C-UF-25` `capability` A token expiring mid-action refuses the action. `src: User flow, entry para`
- [ ] `C-UF-26` `capability` A token expiring mid-action returns the user to `/login`. `src: User flow, entry para`
- [ ] `C-UF-27` `capability` A draft slug at `/projects/:slug` shows the not-found route. `src: User flow, entry para`
- [ ] `C-UF-28` `capability` An unknown slug at `/projects/:slug` shows the not-found route. `src: User flow, entry para`
- [ ] `C-UF-29` `literal` The canvas header reads `All projects` beside the count. `src: User flow journey 1`
- [ ] `C-UF-30` `capability` Dragging the wall tracks the pointer one to one. `src: User flow journey 1`
- [ ] `C-UF-31` `capability` Releasing a drag keeps the wall travelling before easing to a stop. `src: User flow journey 1`
- [ ] `C-UF-32` `capability` Continued dragging keeps bringing further cards into view. `src: User flow journey 1`
- [ ] `C-UF-33` `constraint` The wall surface never reaches an end in any drag direction. `src: User flow journey 1`
- [ ] `C-UF-34` `capability` Pointing at a thumbnail resolves in the client name, the year, the pills. `src: User flow journey 1`
- [ ] `C-UF-35` `capability` The list view shows the same published set one row each. `src: User flow journey 1`
- [ ] `C-UF-36` `capability` Returning from a project leaves the wall at the position last held. `src: User flow journey 1`
- [ ] `C-UF-37` `capability` The `/studio` list shows eight seeded projects. `src: User flow journey 2`
- [ ] `C-UF-38` `capability` A newly created project stays absent from `/` until published. `src: User flow journey 2`
- [ ] `C-UF-39` `capability` Publishing a new project raises the public count by one. `src: User flow journey 2`
- [ ] `C-UF-40` `constraint` A signed-out request for `/projects/brand-standards` is not found. `src: User flow journey 3`
- [ ] `C-UF-41` `constraint` A signed-out request for the `brand-standards` image route is denied. `src: User flow journey 3`
- [ ] `C-UF-42` `constraint` A `visitor` request for the `brand-standards` image route is denied. `src: User flow journey 3`
- [ ] `C-UF-43` `capability` A `curator` request for the `brand-standards` image route is served. `src: User flow journey 3`
- [ ] `C-UF-44` `literal` The enquiry confirmation shows `Nice one!`. `src: User flow journey 4`
- [ ] `C-UF-45` `capability` The curator enquiry inbox shows the reference returned to the sender. `src: User flow journey 4`
- [ ] `C-UF-46` `capability` The careers route lists four open roles. `src: User flow journey 5`
- [ ] `C-UF-47` `constraint` The careers route omits `Motion Designer (AKL)`. `src: User flow journey 5`
- [ ] `C-UF-48` `capability` A role row expands to show detail. `src: User flow journey 5`
- [ ] `C-UF-49` `capability` Every list carries an empty state naming what is missing. `src: User flow, states para`
- [ ] `C-UF-50` `capability` Every route carries a loading state. `src: User flow, states para`
- [ ] `C-UF-51` `capability` The canvas carries a loading state of its own. `src: User flow, states para`
- [ ] `C-UF-52` `capability` A rejected submission puts the reason against the offending field. `src: User flow, states para`
- [ ] `C-UF-53` `constraint` No error leaves the app on a blank page. `src: User flow, states para`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The site reads as a welcoming studio front of house. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The work is seen before the interface. `src: UI/UX notes para 1`
- [ ] `C-UX-03` `ui` The enquiry flow carries the warmth of the voice visually. `src: UI/UX notes para 1`
- [ ] `C-UX-04` `ui` A display face carries body copy through to the wall-sized headline. `src: UI/UX notes para 2`
- [ ] `C-UX-05` `ui` A monospace face is reserved for small technical labels. `src: UI/UX notes para 2`
- [ ] `C-UX-06` `ui` Body copy is set in a rounded humanist sans. `src: UI/UX notes para 2`
- [ ] `C-UX-07` `ui` Figures align wherever numbers stack. `src: UI/UX notes para 2`
- [ ] `C-UX-08` `ui` The ground is the deepest value in the system. `src: UI/UX notes para 3`
- [ ] `C-UX-09` `ui` One warm accent carries highlight plus focus. `src: UI/UX notes para 3`
- [ ] `C-UX-10` `constraint` The warm accent appears nowhere decorative. `src: UI/UX notes para 3`
- [ ] `C-UX-11` `constraint` A separate colour means failure, appearing nowhere else. `src: UI/UX notes para 3`
- [ ] `C-UX-12` `ui` Sections read as separate without a dividing rule. `src: UI/UX notes para 3`
- [ ] `C-UX-13` `ui` Motion is springy with a visible overshoot before settling. `src: UI/UX notes para 4`
- [ ] `C-UX-14` `ui` Elements enter by rising a short distance then fading in. `src: UI/UX notes para 4`
- [ ] `C-UX-15` `ui` Headlines assemble one word at a time. `src: UI/UX notes para 4`
- [ ] `C-UX-16` `constraint` Every transition shares one motion character. `src: UI/UX notes para 4`
- [ ] `C-UX-17` `constraint` A reduced-motion preference collapses all travel to a cross fade in place. `src: UI/UX notes para 4`
- [ ] `C-UX-18` `constraint` A reduced-motion preference loses nothing that carries information. `src: UI/UX notes para 4`
- [ ] `C-UX-19` `ui` Text contrast meets WCAG AA. `src: UI/UX notes para 5`
- [ ] `C-UX-20` `ui` Touch targets are comfortably sized. `src: UI/UX notes para 5`
- [ ] `C-UX-21` `ui` Keyboard navigation reaches every card on the wall. `src: UI/UX notes para 5`
- [ ] `C-UX-22` `ui` Every focusable element shows a visible focus ring. `src: UI/UX notes para 5`
- [ ] `C-UX-23` `ui` Every icon-only control carries a label. `src: UI/UX notes para 5`
- [ ] `C-UX-24` `constraint` Meaning is never carried by colour alone. `src: UI/UX notes para 5`
- [ ] `C-UX-25` `constraint` The custom pointer never stands in for a real focus ring. `src: UI/UX notes para 5`
- [ ] `C-UX-26` `ui` The layout is top-nav with a floating route pill. `src: UI/UX notes para 6`
- [ ] `C-UX-27` `ui` The wall fills the viewport. `src: UI/UX notes para 6`
- [ ] `C-UX-28` `ui` The reading routes sit in a centred column with generous gutters. `src: UI/UX notes para 6`
- [ ] `C-UX-29` `constraint` The wall stays draggable at every width. `src: UI/UX notes para 6`
- [ ] `C-UX-30` `constraint` The reading column never runs edge to edge. `src: UI/UX notes para 6`
- [ ] `C-UX-31` `constraint` No page is dominated by one hue family with no second signal. `src: UI/UX notes para 7`
- [ ] `C-UX-32` `constraint` The console reads as a working interface rather than a marketing page. `src: UI/UX notes para 7`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The frontend is built with React on Vite. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The backend is built with NestJS. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The browser receives an application shell on first paint. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` Route content arrives as JSON from the same origin. `src: Technical requirements para 1`
- [ ] `C-TR-05` `constraint` The server renders no page HTML. `src: Technical requirements para 1`
- [ ] `C-TR-06` `contract` Both halves install from the public npm registry at image build time. `src: Technical requirements para 2`
- [ ] `C-TR-07` `contract` The app runs on the Node 20 runtime already in the image. `src: Technical requirements para 2`
- [ ] `C-TR-08` `literal` Relational storage is PostgreSQL reached at `DATABASE_URL`. `src: Technical requirements para 3`
- [ ] `C-TR-09` `literal` Object storage is MinIO reached at `STORAGE_ENDPOINT`. `src: Technical requirements para 3`
- [ ] `C-TR-10` `literal` The bucket name is read from `STORAGE_BUCKET`. `src: Technical requirements para 3`
- [ ] `C-TR-11` `literal` The store access key is read from `STORAGE_ACCESS_KEY`. `src: Technical requirements para 3`
- [ ] `C-TR-12` `literal` The store secret key is read from `STORAGE_SECRET_KEY`. `src: Technical requirements para 3`
- [ ] `C-TR-13` `constraint` No host is hardcoded anywhere in the app. `src: Technical requirements para 3`
- [ ] `C-TR-14` `constraint` No credential is hardcoded anywhere in the app. `src: Technical requirements para 3`
- [ ] `C-TR-15` `contract` Auth is app-implemented email plus password with bearer tokens. `src: Technical requirements para 4`
- [ ] `C-TR-16` `constraint` The app uses no external identity provider. `src: Technical requirements para 4`
- [ ] `C-TR-17` `literal` The route `GET /api/health` returns `200` with a JSON body once ready. `src: Technical requirements para 5`
- [ ] `C-TR-18` `capability` Request logging is structured to stdout, one line per request. `src: Technical requirements para 5`
- [ ] `C-TR-19` `data` Each log line carries method, path, status, duration. `src: Technical requirements para 5`
- [ ] `C-TR-20` `constraint` No log line carries a password. `src: Technical requirements para 5`
- [ ] `C-TR-21` `constraint` No log line carries a token. `src: Technical requirements para 5`
- [ ] `C-TR-22` `constraint` No log line carries object bytes. `src: Technical requirements para 5`
- [ ] `C-TR-23` `constraint` Every image lives in `minio`, nowhere else. `src: Technical requirements para 6`
- [ ] `C-TR-24` `constraint` Every uploaded file lives in `minio`, nowhere else. `src: Technical requirements para 6`
- [ ] `C-TR-25` `contract` Protected bytes are served through an authenticated streaming route on the app origin. `src: Technical requirements para 6`
- [ ] `C-TR-26` `constraint` The app hands out no presigned URLs. `src: Technical requirements para 6`
- [ ] `C-TR-27` `constraint` The app uses only the libraries named in the brief plus their direct dependencies. `src: Technical requirements para 7`
- [ ] `C-TR-28` `constraint` The app introduces no second database. `src: Technical requirements para 7`
- [ ] `C-TR-29` `constraint` The app introduces no cache. `src: Technical requirements para 7`
- [ ] `C-TR-30` `constraint` The app introduces no queue. `src: Technical requirements para 7`
- [ ] `C-TR-31` `constraint` The app introduces no second object store. `src: Technical requirements para 7`
- [ ] `C-TR-32` `constraint` The app introduces no mail vendor. `src: Technical requirements para 7`
- [ ] `C-TR-33` `constraint` No served document carries a database password. `src: Technical requirements, credentials para`
- [ ] `C-TR-34` `constraint` No served document carries an object-store access key. `src: Technical requirements, credentials para`
- [ ] `C-TR-35` `constraint` No served document carries a seeded account bearer token. `src: Technical requirements, credentials para`
- [ ] `C-TR-36` `contract` Every response carries a strict transport policy header. `src: Technical requirements, headers para`
- [ ] `C-TR-37` `contract` Every response carries a nosniff content-type policy header. `src: Technical requirements, headers para`
- [ ] `C-TR-38` `capability` A sitemap at `/sitemap.xml` lists every public route. `src: Technical requirements, sitemap para`
- [ ] `C-TR-39` `capability` A robots file at `/robots.txt` names the sitemap location. `src: Technical requirements, sitemap para`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema holds seven tables. `src: Data model para 1`
- [ ] `C-DM-02` `constraint` All timestamps are UTC. `src: Data model para 1`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model para 2`
- [ ] `C-DM-04` `constraint` The seeded password is hashed as normal. `src: Data model para 2`
- [ ] `C-DM-05` `constraint` The exact password literal works at login. `src: Data model para 2`
- [ ] `C-DM-06` `literal` Each seeded account is written into `/app/USER_README.md`. `src: Data model para 2`
- [ ] `C-DM-07` `data` The `users` table carries id, email, password_hash, role, created_at. `src: Data model, users`
- [ ] `C-DM-08` `data` The `users.email` column is unique. `src: Data model, users`
- [ ] `C-DM-09` `data` The `users.role` column is restricted to `curator` or `visitor`. `src: Data model, users`
- [ ] `C-DM-10` `data` The `projects` table carries id, slug, title, client, year, discipline, tags, summary, status, thumbnail_key, display_order, created_at, published_at. `src: Data model, projects`
- [ ] `C-DM-11` `data` The `projects.discipline` column is restricted to `Experience`, `Communication`, `Product`. `src: Data model, projects`
- [ ] `C-DM-12` `data` The `projects.status` column is `draft` on create. `src: Data model, projects para 2`
- [ ] `C-DM-13` `constraint` The `published_at` value is stamped on first publish, never rewritten. `src: Data model, projects para 2`
- [ ] `C-DM-14` `constraint` The `thumbnail_key` column holds an object key rather than bytes. `src: Data model, projects para 2`
- [ ] `C-DM-15` `data` A project slug is unique across the whole table. `src: Data model, projects invariant`
- [ ] `C-DM-16` `constraint` Slug uniqueness holds under concurrent creates. `src: Data model, projects invariant`
- [ ] `C-DM-17` `constraint` Two simultaneous creates of one slug never both succeed. `src: Data model, projects invariant`
- [ ] `C-DM-18` `constraint` A losing concurrent create leaves no orphaned row. `src: Data model, projects invariant`
- [ ] `C-DM-19` `constraint` A losing concurrent create leaves no orphaned object. `src: Data model, projects invariant`
- [ ] `C-DM-20` `data` The `roles_open` table carries id, slug, discipline, title, office, detail, apply_url, open. `src: Data model, roles_open`
- [ ] `C-DM-21` `data` The `roles_open.discipline` column is restricted to `technology`, `partnership`, `creative`. `src: Data model, roles_open`
- [ ] `C-DM-22` `data` The `roles_open.office` column is restricted to `London` or `Auckland`. `src: Data model, roles_open`
- [ ] `C-DM-23` `data` The `enquiries` table carries id, reference, intent, readiness, name, email, company, message, created_at. `src: Data model, enquiries`
- [ ] `C-DM-24` `data` The `enquiries.reference` column is unique. `src: Data model, enquiries`
- [ ] `C-DM-25` `data` An enquiry reference is `ENQ-` followed by the id zero padded to five digits. `src: Data model, enquiries para 2`
- [ ] `C-DM-26` `data` The `applications` table carries id, reference, name, email, portfolio_url, message, file_key, created_at. `src: Data model, applications`
- [ ] `C-DM-27` `data` An application reference is `WLD-` followed by the id zero padded to five digits. `src: Data model, applications`
- [ ] `C-DM-28` `data` The `consent_events` table carries id, choice, created_at. `src: Data model, consent_events`
- [ ] `C-DM-29` `data` The `consent_events.choice` column is restricted to `accept` or `decline`. `src: Data model, consent_events`
- [ ] `C-DM-30` `data` The `site_config` table holds exactly one row carrying a jsonb payload. `src: Data model, site_config`
- [ ] `C-DM-31` `constraint` The published-project count is derived rather than stored. `src: Data model, derived para`
- [ ] `C-DM-32` `constraint` The per-discipline about counts are derived rather than stored. `src: Data model, derived para`
- [ ] `C-DM-33` `constraint` The two office clock times are computed in the browser from each office timezone. `src: Data model, derived para`
- [ ] `C-DM-34` `literal` The seed creates `curator@example.com` with role `curator`. `src: Data model, seed para 1`
- [ ] `C-DM-35` `literal` The seed creates `visitor@example.com` with role `visitor`. `src: Data model, seed para 1`
- [ ] `C-DM-36` `data` The seed creates eight projects, six published, two draft. `src: Data model, seed project table`
- [ ] `C-DM-37` `literal` The seeded draft projects are `brand-standards`, `handset-for-travel`. `src: Data model, seed project table rows 7 to 8`
- [ ] `C-DM-38` `constraint` Every seeded project carries a real thumbnail object in `minio`. `src: Data model, seed para 3`
- [ ] `C-DM-39` `capability` Every seeded thumbnail is generated procedurally at seed time. `src: Data model, seed para 3`
- [ ] `C-DM-40` `data` The seed creates five open-role rows, four open, one closed. `src: Data model, seed role table`
- [ ] `C-DM-41` `literal` The seeded closed role is `motion-designer-akl`. `src: Data model, seed role table row 5`
- [ ] `C-DM-42` `data` The seed creates one `site_config` row carrying offices, social, legal, counts. `src: Data model, seed para 5`
- [ ] `C-DM-43` `literal` The seeded London office email is `hello@spectre.agency`. `src: Data model, seed para 5`
- [ ] `C-DM-44` `literal` The seeded Auckland office email is `kia@spectre.nz`. `src: Data model, seed para 5`
- [ ] `C-DM-45` `constraint` Seeding is idempotent so a restart duplicates no rows. `src: Data model, seed closing line`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The design tokens sit on a fixed root with hard breakpoints. `src: Front-end specification, scaling`
- [ ] `C-FE-02` `ui` Three widths anchor the responsive matrix at desktop, tablet, mobile. `src: Front-end specification, scaling`
- [ ] `C-FE-03` `ui` The palette is near-monochrome built from black, white, their alphas. `src: Front-end specification, colour tokens`
- [ ] `C-FE-04` `literal` The primary text token is `#ffffff`. `src: Front-end specification, colour token table row 1`
- [ ] `C-FE-05` `literal` The secondary ground token is `#202020`. `src: Front-end specification, colour token table row 2`
- [ ] `C-FE-06` `literal` The dominant page ground is `#000000`. `src: Front-end specification, colour token table row 3`
- [ ] `C-FE-07` `literal` The third near-black surface is `#222222`. `src: Front-end specification, colour token table row 5`
- [ ] `C-FE-08` `literal` The hairline token is `#444444`. `src: Front-end specification, colour token table row 6`
- [ ] `C-FE-09` `literal` The muted label token is `#929292`. `src: Front-end specification, colour token table row 7`
- [ ] `C-FE-10` `literal` The off-white inversion token is `#dfdfdf`. `src: Front-end specification, colour token table row 8`
- [ ] `C-FE-11` `literal` The single warm accent is `#ff6b00`. `src: Front-end specification, accent table row 1`
- [ ] `C-FE-12` `literal` The cookie confirm hover is `#50baa3`. `src: Front-end specification, accent table row 2`
- [ ] `C-FE-13` `literal` The messaging confirm hover is `#47bb56`. `src: Front-end specification, accent table row 3`
- [ ] `C-FE-14` `literal` The signal green is `#1eff66`. `src: Front-end specification, accent table row 4`
- [ ] `C-FE-15` `literal` The signal teal is `#03fdc7`. `src: Front-end specification, accent table row 5`
- [ ] `C-FE-16` `literal` The pale teal wash is `#a1f4e2`. `src: Front-end specification, accent table row 6`
- [ ] `C-FE-17` `literal` The failure colour is `#a52a2a`. `src: Front-end specification, accent table row 7`
- [ ] `C-FE-18` `literal` The inverted-surface focus outline is `#9932cc`. `src: Front-end specification, accent table row 8`
- [ ] `C-FE-19` `literal` The wildcard upload warm neutral is `#deb887`. `src: Front-end specification, accent table row 9`
- [ ] `C-FE-20` `ui` The alpha system is expressed against white plus black at the stated stops. `src: Front-end specification, alpha para`
- [ ] `C-FE-21` `ui` Two theme functions derive tints without adding tokens. `src: Front-end specification, alpha para`
- [ ] `C-FE-22` `ui` The type system carries a display grotesque plus a mono detail face. `src: Front-end specification, type scale`
- [ ] `C-FE-23` `ui` The type ramp reproduces the stated sizes rather than inventing intermediate steps. `src: Front-end specification, type scale`
- [ ] `C-FE-24` `ui` The radius scale carries eight named values from pill to full round. `src: Front-end specification, radius`
- [ ] `C-FE-25` `ui` Elevation is expressed as layering rather than shadow. `src: Front-end specification, radius`
- [ ] `C-FE-26` `ui` The `z-index` ladder places the three-dimensional canvas behind content. `src: Front-end specification, radius`
- [ ] `C-FE-27` `ui` The `z-index` ladder places the custom cursor above everything. `src: Front-end specification, radius`
- [ ] `C-FE-28` `ui` The about route uses a two-column split of mono rail plus body column. `src: Front-end specification, spacing`
- [ ] `C-FE-29` `ui` The careers route uses a two-column split of mono rail plus body column. `src: Front-end specification, spacing`
- [ ] `C-FE-30` `ui` The canvas route fills the viewport, ignoring the content column. `src: Front-end specification, spacing`
- [ ] `C-FE-31` `constraint` Every icon is inline vector geometry rather than a file. `src: Front-end specification, iconography`
- [ ] `C-FE-32` `ui` The sound control is a twenty-four dot grid on a three by eight lattice. `src: Front-end specification, iconography`
- [ ] `C-FE-33` `ui` The day office shows a dot, the night office shows a moon. `src: Front-end specification, iconography`
- [ ] `C-FE-34` `ui` The slider track is drawn as unit rectangles rather than a line. `src: Front-end specification, iconography`
- [ ] `C-FE-35` `capability` The slider tick count is derived from the track width. `src: Front-end specification, iconography`
- [ ] `C-FE-36` `ui` The header is fixed carrying wordmark, sound toggle, tagline, clock, CTA. `src: Front-end specification, global chrome`
- [ ] `C-FE-37` `literal` The header CTA reads `Let's talk`. `src: Front-end specification, global chrome`
- [ ] `C-FE-38` `literal` The sound toggle label reads `Sound [OFF]` in the off state. `src: Front-end specification, global chrome`
- [ ] `C-FE-39` `ui` A gradient blur bar sits behind the header, fading to nothing lower down. `src: Front-end specification, global chrome`
- [ ] `C-FE-40` `ui` Top-anchored chrome enters on a downward slide from off-screen. `src: Front-end specification, header entrance`
- [ ] `C-FE-41` `ui` Bottom-anchored chrome enters on an upward slide from off-screen. `src: Front-end specification, header entrance`
- [ ] `C-FE-42` `ui` The bottom pill navigation carries `Work`, `About`, `Careers`. `src: Front-end specification, bottom pill`
- [ ] `C-FE-43` `ui` The active route in the pill is shown as a filled white pill. `src: Front-end specification, bottom pill`
- [ ] `C-FE-44` `capability` The dual clock shows a live time per office updated once per minute. `src: Front-end specification, dual clock`
- [ ] `C-FE-45` `constraint` The clock times are computed client side rather than fetched. `src: Front-end specification, dual clock`
- [ ] `C-FE-46` `ui` The footer repeats both offices as full postal blocks. `src: Front-end specification, footer`
- [ ] `C-FE-47` `literal` The footer certification line reads `ISO 27001`. `src: Front-end specification, footer`
- [ ] `C-FE-48` `ui` The footer carries three legal links. `src: Front-end specification, footer`
- [ ] `C-FE-49` `ui` The cookie banner slides up from the bottom of the viewport. `src: Front-end specification, cookie banner`
- [ ] `C-FE-50` `ui` The cookie banner offers `Accept` beside `Decline`. `src: Front-end specification, cookie banner`
- [ ] `C-FE-51` `capability` The cookie choice is persisted. `src: Front-end specification, cookie banner`
- [ ] `C-FE-52` `capability` The cookie choice gates analytics. `src: Front-end specification, cookie banner`
- [ ] `C-FE-53` `ui` Elements travel a short distance on entry. `src: Front-end specification, motion language`
- [ ] `C-FE-54` `ui` Interactive surfaces move under the pointer with a sense of momentum. `src: Front-end specification, motion language`
- [ ] `C-FE-55` `ui` The named keyframe library carries the eight stated entrances. `src: Front-end specification, motion language`
- [ ] `C-FE-56` `ui` The default easing is a firm ease with a hair of anticipation. `src: Front-end specification, motion language`
- [ ] `C-FE-57` `ui` The card entrance uses the spring-plus-fade transition. `src: Front-end specification, motion language`
- [ ] `C-FE-58` `constraint` Reduced motion collapses drag inertia to an immediate settle. `src: Front-end specification, reduced motion`
- [ ] `C-FE-59` `constraint` Reduced motion holds the mascot in a static pose. `src: Front-end specification, reduced motion`
- [ ] `C-FE-60` `constraint` Reduced motion stops the clock dot blinking. `src: Front-end specification, reduced motion`
- [ ] `C-FE-61` `ui` Scrolling on the reading routes is eased rather than native. `src: Front-end specification, scroll`
- [ ] `C-FE-62` `constraint` The home canvas drags rather than scrolls. `src: Front-end specification, scroll`
- [ ] `C-FE-63` `ui` Elements reveal on entry by rising then fading. `src: Front-end specification, reveal`
- [ ] `C-FE-64` `ui` About separators scrub their horizontal scale outward as each enters. `src: Front-end specification, scrubbed`
- [ ] `C-FE-65` `ui` Display headlines reveal per word or per letter on a short stagger. `src: Front-end specification, split text`
- [ ] `C-FE-66` `capability` A full-viewport three-dimensional layer composites behind the content. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-67` `capability` The mascot appears as loader mark, not-found hero, careers character. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-68` `constraint` One persistent rendering context serves the whole session. `src: Front-end specification, renderer contract`
- [ ] `C-FE-69` `constraint` The rendering context is capped at a device pixel ratio of `2`. `src: Front-end specification, renderer contract`
- [ ] `C-FE-70` `capability` A post-processing chain carries a render pass plus a full-screen effect pass. `src: Front-end specification, renderer contract`
- [ ] `C-FE-71` `capability` The render loop pauses when nothing animates. `src: Front-end specification, renderer contract`
- [ ] `C-FE-72` `capability` The render loop pauses when the tab is hidden. `src: Front-end specification, renderer contract`
- [ ] `C-FE-73` `ui` The mascot reads as a lit semi-transparent object floating in a void. `src: Front-end specification, mascot material`
- [ ] `C-FE-74` `capability` The mascot carries a slow idle bob plus rotation at rest. `src: Front-end specification, mascot material`
- [ ] `C-FE-75` `capability` The mascot tracks the pointer on a lagged follow. `src: Front-end specification, pointer binding`
- [ ] `C-FE-76` `capability` The mascot degrades to a static generated silhouette without a rendering context. `src: Front-end specification, fallback`
- [ ] `C-FE-77` `constraint` No content depends on the three-dimensional layer. `src: Front-end specification, fallback`
- [ ] `C-FE-78` `ui` The loader holds first paint behind a mascot, a headline, a progress bar. `src: Front-end specification, loader`
- [ ] `C-FE-79` `capability` The loader exit variant is chosen per load. `src: Front-end specification, loader`
- [ ] `C-FE-80` `constraint` The loader blocks no interaction past its exit. `src: Front-end specification, loader handoff`
- [ ] `C-FE-81` `capability` The loader holds at a near-full bar when assets still stream. `src: Front-end specification, loader handoff`
- [ ] `C-FE-82` `constraint` No audio plays before a user gesture. `src: Front-end specification, audio`
- [ ] `C-FE-83` `capability` The first enabling gesture starts the ambient bed. `src: Front-end specification, audio`
- [ ] `C-FE-84` `capability` The sound choice persists across routes plus reloads. `src: Front-end specification, audio`
- [ ] `C-FE-85` `ui` The sound control dots pulse when sound is on. `src: Front-end specification, audio`
- [ ] `C-FE-86` `capability` Interface cues fire on canvas grab, view toggle, panel open. `src: Front-end specification, audio`
- [ ] `C-FE-87` `constraint` Every cue is a generated tone rather than a file. `src: Front-end specification, audio`
- [ ] `C-FE-88` `capability` Pointer-down anywhere on the field grabs the wall. `src: Front-end specification, canvas`
- [ ] `C-FE-89` `capability` Pointer-up releases the wall with inertia. `src: Front-end specification, canvas`
- [ ] `C-FE-90` `capability` The field wraps so dragging far brings further projects into view. `src: Front-end specification, canvas`
- [ ] `C-FE-91` `capability` Momentum decays on a weighted curve so a hard flick travels far. `src: Front-end specification, canvas`
- [ ] `C-FE-92` `ui` Distant thumbnails sit smaller, dimmer than near ones. `src: Front-end specification, canvas depth`
- [ ] `C-FE-93` `ui` A thumbnail reveals title, client, pills, year on hover or focus. `src: Front-end specification, thumbnail`
- [ ] `C-FE-94` `ui` Pills carry one discipline plus free tags from the stated vocabulary. `src: Front-end specification, thumbnail`
- [ ] `C-FE-95` `ui` Moving the pointer on the canvas drags a trail of images behind. `src: Front-end specification, image trail`
- [ ] `C-FE-96` `ui` The custom cursor inverts whatever sits behind. `src: Front-end specification, image trail`
- [ ] `C-FE-97` `ui` A control pinned bottom-left toggles grid against list. `src: Front-end specification, grid and list`
- [ ] `C-FE-98` `capability` Switching view plays a cue then cross-animates the layout. `src: Front-end specification, grid and list`
- [ ] `C-FE-99` `capability` Keyboard enter on a focused thumbnail opens the project. `src: Front-end specification, entering a project`
- [ ] `C-FE-100` `ui` The thumbnail expands into the detail hero rather than a hard navigation. `src: Front-end specification, entering a project`
- [ ] `C-FE-101` `ui` The custom cursor follows the pointer on a lag. `src: Front-end specification, cursor`
- [ ] `C-FE-102` `ui` The custom cursor takes a grab state over the canvas. `src: Front-end specification, cursor`
- [ ] `C-FE-103` `constraint` The custom cursor is suppressed for touch. `src: Front-end specification, cursor`
- [ ] `C-FE-104` `ui` The about wall headline splits to individual letters revealed on a stagger. `src: Front-end specification, route detail`
- [ ] `C-FE-105` `ui` The about route shows three focuses linking into filtered work. `src: Front-end specification, route detail`
- [ ] `C-FE-106` `ui` The client logo grid enters on an overshoot pop. `src: Front-end specification, route detail`
- [ ] `C-FE-107` `ui` The careers route shows three value sections beside the mascot. `src: Front-end specification, route detail`
- [ ] `C-FE-108` `ui` A careers role row expands on an accordion. `src: Front-end specification, route detail`
- [ ] `C-FE-109` `ui` The contact panel opens over any route as a full-screen overlay. `src: Front-end specification, route detail`
- [ ] `C-FE-110` `capability` Opening the contact panel records history state rather than a hard navigation. `src: Front-end specification, route detail`
- [ ] `C-FE-111` `ui` Contact step one shows three intent tiles. `src: Front-end specification, route detail`
- [ ] `C-FE-112` `ui` The anything-else tile reveals two copyable direct contacts. `src: Front-end specification, route detail`
- [ ] `C-FE-113` `ui` Contact step two numbers its five fields `01` to `05`. `src: Front-end specification, route detail`
- [ ] `C-FE-114` `capability` The readiness slider snaps to the nearest of three stops. `src: Front-end specification, route detail`
- [ ] `C-FE-115` `ui` Contact step three shows three numbered boxes explaining what happens next. `src: Front-end specification, route detail`
- [ ] `C-FE-116` `ui` The contact form carries idle, submitting, success, failure states. `src: Front-end specification, route detail`
- [ ] `C-FE-117` `ui` The not-found route shows the mascot floating large on the black ground. `src: Front-end specification, not found`
- [ ] `C-FE-118` `constraint` The seven captured stub addresses never become public routes. `src: Front-end specification, not found`
- [ ] `C-FE-119` `ui` The legal route carries privacy, modern slavery, AI policy as three sections. `src: Front-end specification, not found`
- [ ] `C-FE-120` `contract` One shell holds the persistent chrome, the persistent render layer, a routed region. `src: Front-end specification, module architecture`
- [ ] `C-FE-121` `constraint` One reveal primitive drives every entrance in the product. `src: Front-end specification, module architecture`
- [ ] `C-FE-122` `data` The catalogue is fetched once then held for the session. `src: Front-end specification, state`
- [ ] `C-FE-123` `capability` The enquiry wizard holds its draft across all three addresses. `src: Front-end specification, state`
- [ ] `C-FE-124` `capability` The enquiry panel pushes real history entries so back moves one step. `src: Front-end specification, state`
- [ ] `C-FE-125` `ui` Below `599px` the bottom pill navigation becomes the primary route switch. `src: Front-end specification, responsive`
- [ ] `C-FE-126` `ui` Below `599px` the list view is the default arrangement of the work. `src: Front-end specification, responsive`
- [ ] `C-FE-127` `capability` Hover metadata resolves on tap-and-hold for touch. `src: Front-end specification, responsive`
- [ ] `C-FE-128` `ui` Each route carries one `main` landmark. `src: Front-end specification, accessibility`
- [ ] `C-FE-129` `capability` The contact panel traps focus when open. `src: Front-end specification, accessibility`
- [ ] `C-FE-130` `capability` Escape closes the contact panel, returning focus to the opening control. `src: Front-end specification, accessibility`
- [ ] `C-FE-131` `capability` The readiness slider is operable by arrow keys with its stop announced. `src: Front-end specification, accessibility`
- [ ] `C-FE-132` `constraint` The custom cursor is hidden from assistive technology. `src: Front-end specification, accessibility`
- [ ] `C-FE-133` `capability` The canvas draws only thumbnails within or just beyond the viewport. `src: Front-end specification, performance`
- [ ] `C-FE-134` `capability` Card nodes are reused as the field wraps. `src: Front-end specification, performance`
- [ ] `C-FE-135` `capability` Thumbnails load lazily in view order. `src: Front-end specification, performance`
- [ ] `C-FE-136` `constraint` Nothing blocks first paint apart from the loader. `src: Front-end specification, performance`
- [ ] `C-FE-137` `constraint` No measurement runs before a consent choice is recorded. `src: Front-end specification, analytics`
- [ ] `C-FE-138` `capability` The consent choice is posted to the app own consent endpoint. `src: Front-end specification, analytics`
- [ ] `C-FE-139` `constraint` Measurement covers route views, enquiry funnel steps, wildcard submission only. `src: Front-end specification, analytics`
- [ ] `C-FE-140` `constraint` The app carries no third-party tag. `src: Front-end specification, analytics`
- [ ] `C-FE-141` `data` A project detail body is an ordered list of blocks. `src: Front-end specification, content model`
- [ ] `C-FE-142` `data` The block vocabulary carries text, full-bleed media, two-up pair, pull quote. `src: Front-end specification, content model`
- [ ] `C-FE-143` `literal` The header tagline reads `Spectre is a technology-led creative agency crafting experiences for global brands.`. `src: Front-end specification, copy deck`
- [ ] `C-FE-144` `literal` The careers roles heading reads `Roles we are on the lookout for:`. `src: Front-end specification, copy deck`
- [ ] `C-FE-145` `literal` The careers open-application label reads `Open submissions`. `src: Front-end specification, copy deck`
- [ ] `C-FE-146` `literal` The not-found route reads `Page not found`. `src: Front-end specification, copy deck`
- [ ] `C-FE-147` `constraint` Nothing in the build depends on a binary file. `src: Front-end specification, zero-asset`
- [ ] `C-FE-148` `capability` The mascot form is generated as geometry at start-up. `src: Front-end specification, zero-asset`
- [ ] `C-FE-149` `capability` The ambient bed is synthesised from layered low oscillators. `src: Front-end specification, zero-asset`
- [ ] `C-FE-150` `capability` One deterministic image per project is generated from the project slug. `src: Front-end specification, zero-asset`
- [ ] `C-FE-151` `capability` Grain is generated as a noise pass rather than a tiled image. `src: Front-end specification, zero-asset`
- [ ] `C-FE-152` `ui` The project detail template is a reconstruction flagged as needing adjustment. `src: Front-end specification, evidence gaps`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app serves one studio as a single tenant. `src: Constraints sentence 1`
- [ ] `C-CN-02` `constraint` The app has no client portal. `src: Constraints sentence 2`
- [ ] `C-CN-03` `constraint` The app has no per-client login. `src: Constraints sentence 2`
- [ ] `C-CN-04` `constraint` The app has no messaging between visitors. `src: Constraints sentence 3`
- [ ] `C-CN-05` `constraint` The app has no blog. `src: Constraints sentence 4`
- [ ] `C-CN-06` `constraint` The app has no newsletter. `src: Constraints sentence 4`
- [ ] `C-CN-07` `constraint` The app has no search. `src: Constraints sentence 4`
- [ ] `C-CN-08` `constraint` The app offers no rich-text authoring beyond the project summary. `src: Constraints sentence 5`
- [ ] `C-CN-09` `constraint` The app has no billing surface. `src: Constraints sentence 6`
- [ ] `C-CN-10` `constraint` The app sends no email. `src: Constraints sentence 7`
- [ ] `C-CN-11` `capability` Enquiries are read in the console. `src: Constraints sentence 7`
- [ ] `C-CN-12` `constraint` The app ships no native application. `src: Constraints sentence 8`
- [ ] `C-CN-13` `constraint` The app uses no analytics vendor. `src: Constraints sentence 9`
- [ ] `C-CN-14` `constraint` The consent choice is recorded in the app own table. `src: Constraints sentence 9`
- [ ] `C-CN-15` `constraint` The app makes no external network calls at run time. `src: Constraints sentence 10`
- [ ] `C-CN-16` `constraint` No binary asset ships with the build. `src: Constraints sentence 11`
- [ ] `C-CN-17` `constraint` Every image, icon, sound, three-dimensional form is generated in code. `src: Constraints sentence 11`
- [ ] `C-CN-18` `constraint` The app stays responsive with 500 projects on the wall. `src: Constraints sentence 12`
- [ ] `C-CN-19` `constraint` The app stays responsive with 5,000 stored enquiries. `src: Constraints sentence 12`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `literal` The container-internal port is `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `constraint` Neither port is hardcoded. `src: Deployment contract bullet 1`
- [ ] `C-DC-05` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-06` `literal` The route `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-07` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-08` `literal` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-09` `literal` An empty `.browser_screenshots/` directory exists at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-10` `literal` An empty `.downloads/` directory exists at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-11` `contract` The app serves a production build behind a static or preview server. `src: Deployment contract bullet 7`
- [ ] `C-DC-12` `constraint` The app never serves a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-13` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-14` `constraint` The server is never a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-15` `literal` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-16` `constraint` The server never binds a loopback address. `src: Deployment contract bullet 9`
- [ ] `C-DC-17` `contract` The backing services are reached at their environment variables. `src: Deployment contract bullet 10`
- [ ] `C-DC-18` `constraint` The app downloads no copy of a backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-19` `constraint` The app installs no copy of a backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-20` `constraint` The app starts no copy of a backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-21` `constraint` The app uses only the providers named in the brief. `src: Deployment contract bullet 11`
- [ ] `C-DC-22` `constraint` The app uses no edge functions. `src: Deployment contract bullet 11`
- [ ] `C-DC-23` `constraint` The app declares no persistent volumes. `src: Deployment contract bullet 12`
- [ ] `C-DC-24` `constraint` The app declares no fixed container names. `src: Deployment contract bullet 12`
- [ ] `C-DC-25` `constraint` The app declares no custom networks. `src: Deployment contract bullet 12`
- [ ] `C-DC-26` `literal` The endpoint `POST /api/auth/signup` returns a token beside a role. `src: Deployment contract, API shapes table row 1`
- [ ] `C-DC-27` `literal` The endpoint `POST /api/auth/login` returns a token beside a role. `src: Deployment contract, API shapes table row 2`
- [ ] `C-DC-28` `literal` The endpoint `GET /api/projects` returns a top-level JSON array of published projects. `src: Deployment contract, API shapes table row 4`
- [ ] `C-DC-29` `literal` The endpoint `GET /api/projects/count` returns the published count. `src: Deployment contract, API shapes table row 5`
- [ ] `C-DC-30` `literal` The endpoint `POST /api/projects` returns a project with `status` `draft`. `src: Deployment contract, API shapes table row 7`
- [ ] `C-DC-31` `literal` The endpoint `POST /api/projects/{}/thumbnail` accepts a multipart field named `file`. `src: Deployment contract, API shapes table row 8`
- [ ] `C-DC-32` `literal` The endpoint `POST /api/projects/{}/publish` returns the project with `status` `published`. `src: Deployment contract, API shapes table row 9`
- [ ] `C-DC-33` `literal` The endpoint `GET /api/projects/{}/thumbnail` returns the image bytes. `src: Deployment contract, API shapes table row 10`
- [ ] `C-DC-34` `literal` The endpoint `GET /api/studio/projects` returns every project. `src: Deployment contract, API shapes table row 11`
- [ ] `C-DC-35` `literal` The endpoint `GET /api/roles` returns a top-level JSON array of open roles. `src: Deployment contract, API shapes table row 12`
- [ ] `C-DC-36` `literal` The endpoint `GET /api/studio/roles` returns every role. `src: Deployment contract, API shapes table row 13`
- [ ] `C-DC-37` `literal` The endpoint `POST /api/enquiries` returns an id beside a reference. `src: Deployment contract, API shapes table row 14`
- [ ] `C-DC-38` `literal` The endpoint `GET /api/enquiries` returns a top-level JSON array of stored enquiries. `src: Deployment contract, API shapes table row 15`
- [ ] `C-DC-39` `literal` The endpoint `POST /api/applications` returns an id beside a reference. `src: Deployment contract, API shapes table row 16`
- [ ] `C-DC-40` `literal` The endpoint `GET /api/config` returns offices, social, legal, counts. `src: Deployment contract, API shapes table row 17`
- [ ] `C-DC-41` `literal` The endpoint `POST /api/consent` records the consent choice. `src: Deployment contract, API shapes table row 18`
- [ ] `C-DC-42` `constraint` Field names in the API shapes are exact. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-43` `constraint` Bearer auth is required on every endpoint apart from login, signup, health. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-44` `constraint` An invalid call is rejected as a client error. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-45` `constraint` An unauthorized call is rejected as a client error. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-46` `constraint` A rejected call never returns a `5xx`. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-47` `constraint` A rejected call never returns a silent success. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-48` `constraint` An in-memory map holding uploaded bytes is a contract violation. `src: Deployment contract, No mocks para`
- [ ] `C-DC-49` `constraint` Image bytes written to the app filesystem are a contract violation. `src: Deployment contract, No mocks para`
- [ ] `C-DC-50` `constraint` A database column carrying base64 image data is a contract violation. `src: Deployment contract, No mocks para`
- [ ] `C-DC-51` `constraint` A hardcoded upload response the app returns to itself is a contract violation. `src: Deployment contract, No mocks para`
- [ ] `C-DC-52` `constraint` A project list served from a repository JSON file is a contract violation. `src: Deployment contract, No mocks para`
- [ ] `C-DC-53` `constraint` The app own tables never substitute for what lives in `minio`. `src: Deployment contract, No mocks para`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | seeded password for every account | C-RL-28 | User roles para 3, Data model para 2 |
| `curator@example.com` | seeded curator email | C-RL-26 | User roles para 3 |
| `visitor@example.com` | seeded visitor email | C-RL-27 | User roles para 3 |
| `Authorization: Bearer <token>` | the auth header the client sends | C-CF-04 | Technical requirements, auth para |
| `24 hours` | token lifetime | C-CF-06 | Technical requirements, auth para |
| `draft` | project status on create | C-CF-10 | Core features, catalogue rule 1 |
| `status` | the project state field | C-CF-10 | Core features, catalogue rule 1 |
| `published` | project status after publish | C-CF-10 | Core features, catalogue rule 1 |
| `6 projects` | canvas count against the shipped seed | C-CF-19 | Core features, catalogue rule 3 |
| `7 projects` | canvas count after a seventh publish | C-CF-20 | Core features, catalogue rule 3 |
| `projects/{project_id}/{sha256_of_bytes}.{ext}` | project thumbnail key scheme | C-CF-28 | Core features, publishing rule 2 |
| `applications/{application_id}/{sha256_of_bytes}.{ext}` | wildcard file key scheme | C-CF-53 | Enquiry and careers, rule 2 |
| `WLD-00001` | wildcard application reference shape | C-CF-54 | Enquiry and careers, rule 2 |
| `ENQ-00001` | enquiry reference shape | C-CF-67 | Enquiry and careers, rule 5 |
| `collaboration` | enquiry intent value | C-CF-55 | Enquiry and careers, rule 3 |
| `hiring` | enquiry intent value | C-CF-55 | Enquiry and careers, rule 3 |
| `anything-else` | enquiry intent value | C-CF-55 | Enquiry and careers, rule 3 |
| `0` | lowest readiness stop | C-CF-58 | Enquiry and careers, rule 4 |
| `1` | middle readiness stop | C-CF-58 | Enquiry and careers, rule 4 |
| `2` | highest readiness stop | C-CF-58 | Enquiry and careers, rule 4 |
| `All projects` | canvas header label | C-UF-29 | User flow journey 1 |
| `Nice one!` | enquiry confirmation headline | C-UF-44 | User flow journey 4 |
| `Motion Designer (AKL)` | the seeded closed role title | C-UF-47 | User flow journey 5 |
| `DATABASE_URL` | database connection variable | C-TR-08 | Technical requirements para 3 |
| `STORAGE_ENDPOINT` | object store endpoint variable | C-TR-09 | Technical requirements para 3 |
| `STORAGE_BUCKET` | object store bucket variable | C-TR-10 | Technical requirements para 3 |
| `STORAGE_ACCESS_KEY` | object store access key variable | C-TR-11 | Technical requirements para 3 |
| `STORAGE_SECRET_KEY` | object store secret key variable | C-TR-12 | Technical requirements para 3 |
| `GET /api/health` | health route | C-TR-17 | Technical requirements para 5 |
| `200` | health route success status | C-TR-17 | Technical requirements para 5 |
| `minio` | the object store provider slug | C-TR-23 | Technical requirements para 6 |
| `curator` | the publishing role | C-DM-09 | Data model, users |
| `visitor` | the public role | C-DM-09 | Data model, users |
| `Experience` | project discipline value | C-DM-11 | Data model, projects |
| `Communication` | project discipline value | C-DM-11 | Data model, projects |
| `Product` | project discipline value | C-DM-11 | Data model, projects |
| `technology` | role discipline value | C-DM-21 | Data model, roles_open |
| `partnership` | role discipline value | C-DM-21 | Data model, roles_open |
| `creative` | role discipline value | C-DM-21 | Data model, roles_open |
| `London` | office value | C-DM-22 | Data model, roles_open |
| `Auckland` | office value | C-DM-22 | Data model, roles_open |
| `accept` | consent choice value | C-DM-29 | Data model, consent_events |
| `decline` | consent choice value | C-DM-29 | Data model, consent_events |
| `brand-standards` | seeded draft project slug | C-DM-37 | Data model, seed project table row 7 |
| `handset-for-travel` | seeded draft project slug | C-DM-37 | Data model, seed project table row 8 |
| `motion-designer-akl` | seeded closed role slug | C-DM-41 | Data model, seed role table row 5 |
| `hello@spectre.agency` | seeded London office email | C-DM-43 | Data model, seed para 5 |
| `kia@spectre.nz` | seeded Auckland office email | C-DM-44 | Data model, seed para 5 |
| `/app/USER_README.md` | the credentials file path | C-DM-06 | Data model para 2, Deployment contract bullet 5 |
| `#ffffff` | primary text token | C-FE-04 | Front-end specification, colour token table |
| `#202020` | secondary ground token | C-FE-05 | Front-end specification, colour token table |
| `#000000` | dominant page ground | C-FE-06 | Front-end specification, colour token table |
| `#222222` | third near-black surface | C-FE-07 | Front-end specification, colour token table |
| `#444444` | hairline token | C-FE-08 | Front-end specification, colour token table |
| `#929292` | muted label token | C-FE-09 | Front-end specification, colour token table |
| `#dfdfdf` | off-white inversion token | C-FE-10 | Front-end specification, colour token table |
| `#ff6b00` | the single warm accent | C-FE-11 | Front-end specification, accent table |
| `#50baa3` | cookie confirm hover | C-FE-12 | Front-end specification, accent table |
| `#47bb56` | messaging confirm hover | C-FE-13 | Front-end specification, accent table |
| `#1eff66` | signal green | C-FE-14 | Front-end specification, accent table |
| `#03fdc7` | signal teal | C-FE-15 | Front-end specification, accent table |
| `#a1f4e2` | pale teal wash | C-FE-16 | Front-end specification, accent table |
| `#a52a2a` | failure colour | C-FE-17 | Front-end specification, accent table |
| `#9932cc` | inverted-surface focus outline | C-FE-18 | Front-end specification, accent table |
| `#deb887` | wildcard upload warm neutral | C-FE-19 | Front-end specification, accent table |
| `z-index` | the layering property the ladder pins | C-FE-26 | Front-end specification, radius |
| `Let's talk` | header CTA label | C-FE-37 | Front-end specification, global chrome |
| `Sound [OFF]` | sound toggle label while off | C-FE-38 | Front-end specification, global chrome |
| `Work` | bottom pill label | C-FE-42 | Front-end specification, bottom pill |
| `About` | bottom pill label | C-FE-42 | Front-end specification, bottom pill |
| `Careers` | bottom pill label | C-FE-42 | Front-end specification, bottom pill |
| `ISO 27001` | footer certification line | C-FE-47 | Front-end specification, footer |
| `Accept` | cookie banner control label | C-FE-50 | Front-end specification, cookie banner |
| `Decline` | cookie banner control label | C-FE-50 | Front-end specification, cookie banner |
| `599px` | the mobile breakpoint edge | C-FE-125 | Front-end specification, responsive |
| `main` | the per-route landmark | C-FE-128 | Front-end specification, accessibility |
| `01` | first numbered contact field | C-FE-113 | Front-end specification, route detail |
| `05` | last numbered contact field | C-FE-113 | Front-end specification, route detail |
| `Spectre is a technology-led creative agency crafting experiences for global brands.` | header tagline | C-FE-143 | Front-end specification, copy deck |
| `Roles we are on the lookout for:` | careers roles heading | C-FE-144 | Front-end specification, copy deck |
| `Open submissions` | careers open-application label | C-FE-145 | Front-end specification, copy deck |
| `Page not found` | not-found route heading | C-FE-146 | Front-end specification, copy deck |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | C-DC-02 | Deployment contract bullet 1 |
| `4173` | container-internal port | C-DC-03 | Deployment contract bullet 1 |
| `APP_PUBLIC_URL` | the public app URL variable | C-DC-01 | Deployment contract bullet 1 |
| `/api` | the API prefix | C-DC-05 | Deployment contract bullet 2 |
| `.browser_screenshots/` | reserved directory | C-DC-09 | Deployment contract bullet 6 |
| `.downloads/` | reserved directory | C-DC-10 | Deployment contract bullet 6 |
| `0.0.0.0` | the bind address | C-DC-15 | Deployment contract bullet 9 |
| `POST /api/auth/signup` | signup endpoint | C-DC-26 | API shapes table |
| `POST /api/auth/login` | login endpoint | C-DC-27 | API shapes table |
| `GET /api/projects` | public catalogue endpoint | C-DC-28 | API shapes table |
| `GET /api/projects/count` | published count endpoint | C-DC-29 | API shapes table |
| `POST /api/projects` | project create endpoint | C-DC-30 | API shapes table |
| `POST /api/projects/{}/thumbnail` | thumbnail upload endpoint | C-DC-31 | API shapes table |
| `file` | the multipart field name on upload | C-DC-31 | API shapes table |
| `POST /api/projects/{}/publish` | publish endpoint | C-DC-32 | API shapes table |
| `GET /api/projects/{}/thumbnail` | image bytes endpoint | C-DC-33 | API shapes table |
| `GET /api/studio/projects` | console project endpoint | C-DC-34 | API shapes table |
| `GET /api/roles` | public roles endpoint | C-DC-35 | API shapes table |
| `GET /api/studio/roles` | console roles endpoint | C-DC-36 | API shapes table |
| `POST /api/enquiries` | enquiry create endpoint | C-DC-37 | API shapes table |
| `GET /api/enquiries` | enquiry inbox endpoint | C-DC-38 | API shapes table |
| `POST /api/applications` | wildcard application endpoint | C-DC-39 | API shapes table |
| `GET /api/config` | site configuration endpoint | C-DC-40 | API shapes table |
| `POST /api/consent` | consent record endpoint | C-DC-41 | API shapes table |
| `5xx` | the server-error class a rejection never uses | C-DC-46 | API shapes closing para |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the display face and the mono detail face | C-UX-04 | named by personality with no family pinned, so two builds may choose differently |
| the exact shades behind the palette roles | C-UX-09 | the brief hands the shade to the builder, pinning only the exclusivity rules |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 9 |
| User roles | 1 | 28 |
| Core features | 9 | 73 |
| User flow | 4 | 53 |
| UI and UX notes | 3 | 32 |
| Technical requirements | 2 | 39 |
| Data model | 3 | 45 |
| Front-end specification | 19 | 152 |
| Constraints | 2 | 19 |
| Deployment contract | 9 | 53 |
