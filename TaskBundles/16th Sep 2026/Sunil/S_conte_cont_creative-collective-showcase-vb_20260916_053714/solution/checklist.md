# Checklist: Kanso London Creative Collective Showcase

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, techrequirements, datamodel, frontend, constraints, contract
Sections absent: buildplan
Items: 188
Unpinned values flagged: 4

## C-OV Overview

- [ ] `C-OV-01` `capability` The app presents the studio's published projects to a visitor who has not signed in. `src: Overview para 1`
- [ ] `C-OV-02` `constraint` The app offers no customer account, no cart, no payment, no comments, no search. `src: Overview para 4`
- [ ] `C-OV-03` `capability` The app collects one enquiry from a visitor as the single conversion action. `src: Overview para 1`

## C-RL User roles

- [ ] `C-RL-01` `role` An anonymous visitor reads every published route without signing in. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An anonymous visitor is refused every press-kit object. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A `reader` downloads the press kit of any published project. `src: User roles table row 2`
- [ ] `C-RL-04` `role` A `reader` is refused the enquiry list. `src: User roles table row 2`
- [ ] `C-RL-05` `role` A `reader` is refused every console path. `src: User roles table row 2`
- [ ] `C-RL-06` `role` An `author` creates a project through the studio console. `src: User roles table row 3`
- [ ] `C-RL-07` `role` Registration at `/signup` produces a `reader` account only. `src: User roles signup para`
- [ ] `C-RL-08` `role` The server refuses a mutating request made with a `reader` token against an author-only endpoint. `src: User roles authorization para`
- [ ] `C-RL-09` `literal` The app seeds the account `author@example.com`. `src: User roles seeded accounts table`
- [ ] `C-RL-10` `literal` The app seeds the account `reader@example.com`. `src: User roles seeded accounts table`

## C-CF Core features

- [ ] `C-CF-01` `capability` A sign-in with a seeded email plus the correct password returns a bearer token. `src: Core features rule 1`
- [ ] `C-CF-02` `constraint` A sign-in with a wrong password returns no token. `src: Core features rule 1`
- [ ] `C-CF-03` `constraint` A request to an author-only endpoint carrying no token leaves the targeted state unchanged. `src: Core features rule 2`
- [ ] `C-CF-04` `capability` The header survives a route change. `src: Core features persistent shell para`
- [ ] `C-CF-05` `capability` The footer survives a route change. `src: Core features persistent shell para`
- [ ] `C-CF-06` `capability` A route change updates the address bar to the destination path. `src: Core features rule 3`
- [ ] `C-CF-07` `capability` The browser back control restores the previous route. `src: Core features rule 3`
- [ ] `C-CF-08` `capability` A cold load of `/work` renders the work route directly. `src: Core features rule 4`
- [ ] `C-CF-09` `ui` The header carries the primary trio `Home`, `Work`, `Services`. `src: Core features rule 5`
- [ ] `C-CF-10` `ui` The header carries the secondary set `team`, `contact`, `PRESS & NEWS` in the casing given. `src: Core features rule 5`
- [ ] `C-CF-11` `capability` Each of the three world clocks shows the current wall time in the named city. `src: Core features rule 6`
- [ ] `C-CF-12` `constraint` The three world clocks are computed on the visitor's device rather than fetched. `src: Core features rule 6`
- [ ] `C-CF-13` `constraint` Every internal link on every public route resolves. `src: Core features rule 7`
- [ ] `C-CF-14` `ui` The footer carries the call to action `WE WOULD LOVE TO HEAR FROM YOU.`. `src: Core features rule 8`
- [ ] `C-CF-15` `literal` The footer carries the contact address `hello@kanso.studio`. `src: Core features rule 8`
- [ ] `C-CF-16` `ui` The hero renders a drifting colour field behind the headline. `src: Core features rule 9`
- [ ] `C-CF-17` `ui` The hero renders a circular lens that bends the content beneath. `src: Core features rule 9`
- [ ] `C-CF-18` `ui` The hero headline is selectable text rather than painted pixels. `src: Core features rule 10`
- [ ] `C-CF-19` `ui` The hero headline reads `We are a brand` on the first line. `src: Core features rule 10`
- [ ] `C-CF-20` `constraint` The hero words are readable before the animated field starts. `src: Core features rule 11`
- [ ] `C-CF-21` `capability` The hero falls back to a still frame where the animated field cannot run. `src: Core features rule 11`
- [ ] `C-CF-22` `ui` The reel carries the eyebrow `RECENT WORK`. `src: Core features rule 12`
- [ ] `C-CF-23` `capability` The reel pins to the screen as the reel content advances. `src: Core features rule 12`
- [ ] `C-CF-24` `capability` The reel rewinds when the visitor scrolls back. `src: Core features rule 12`
- [ ] `C-CF-25` `literal` The reel holds the four seeded projects flagged `featured_home`. `src: Core features rule 13`
- [ ] `C-CF-26` `constraint` The reel never holds an unpublished project. `src: Core features rule 13`
- [ ] `C-CF-27` `ui` The reel closes on a pill reading `Discover all projects`. `src: Core features rule 14`
- [ ] `C-CF-28` `literal` The work filter bar carries the eight controls beginning `All`, `SPATIAL`, `Campaign`. `src: Core features rule 16`
- [ ] `C-CF-29` `capability` Choosing a work filter narrows the grid without a page reload. `src: Core features rule 17`
- [ ] `C-CF-30` `capability` Choosing a work filter reflects the choice in the URL query. `src: Core features rule 17`
- [ ] `C-CF-31` `capability` Loading a filtered work URL directly shows the same projects. `src: Core features rule 17`
- [ ] `C-CF-32` `capability` Choosing `All` shows every published project. `src: Core features rule 17`
- [ ] `C-CF-33` `capability` A work filter matching no published project shows the index empty state. `src: Core features rule 18`
- [ ] `C-CF-34` `capability` A project cover plays only when pointed at, pausing otherwise. `src: Core features rule 20`
- [ ] `C-CF-35` `literal` The press filter set carries a derived count beside each of `News`, `Events`, `Features`, `Articles`. `src: Core features rule 21`
- [ ] `C-CF-36` `literal` The seeded press collection yields the badge `Features [3]`. `src: Core features rule 21`
- [ ] `C-CF-37` `capability` The press feed lists items newest first. `src: Core features rule 22`
- [ ] `C-CF-38` `ui` The press feed item carries the label `Read more`. `src: Core features rule 22`
- [ ] `C-CF-39` `literal` The series block carries the tag `Designing for the future`. `src: Core features rule 23`
- [ ] `C-CF-40` `literal` The series block carries the three volumes beginning `Vol 01`. `src: Core features rule 23`
- [ ] `C-CF-41` `ui` The series collage tiles settle at different depths as the scroll passes. `src: Core features rule 23`
- [ ] `C-CF-42` `capability` Each series image loads a blurred preview before the full image. `src: Core features rule 23`
- [ ] `C-CF-43` `ui` The press route repeats the contact invitation as three pill links. `src: Core features rule 24`
- [ ] `C-CF-44` `ui` The team route opens on a three-line heading revealed line by line. `src: Core features rule 25`
- [ ] `C-CF-45` `literal` The team route carries the footnote `[ a city-based global network ]`. `src: Core features rule 25`
- [ ] `C-CF-46` `ui` The team banner draws in against the scroll rather than on entry. `src: Core features rule 26`
- [ ] `C-CF-47` `literal` The member grid closes on the derived count `11 members`. `src: Core features rule 27`
- [ ] `C-CF-48` `literal` The team route closes on the two dated chapters `2011`, `2019`. `src: Core features rule 28`
- [ ] `C-CF-49` `literal` An unknown address renders the heading `Page not found`. `src: Core features rule 29`
- [ ] `C-CF-50` `capability` An unknown address answers not found rather than answering success. `src: Core features rule 29`
- [ ] `C-CF-51` `capability` A valid enquiry submission stores the enquiry. `src: Core features rule 30`
- [ ] `C-CF-52` `ui` A valid enquiry submission replaces the form in place with the success state. `src: Core features rule 30`
- [ ] `C-CF-53` `constraint` An enquiry with an empty name writes no row. `src: Core features rule 31`
- [ ] `C-CF-54` `ui` An enquiry rejected inline names the field at fault. `src: Core features rule 31`
- [ ] `C-CF-55` `literal` An enquiry carrying anything in the hidden field `company_website` is refused. `src: Core features rule 32`
- [ ] `C-CF-56` `literal` A fourth enquiry from one visitor inside `60` seconds is refused. `src: Core features rule 32`
- [ ] `C-CF-57` `constraint` A refused enquiry leaves no row behind. `src: Core features rule 32`
- [ ] `C-CF-58` `role` The enquiry list at `/studio/enquiries` is served to an `author` alone. `src: Core features rule 33`
- [ ] `C-CF-59` `ui` The cookie rail states that the website uses cookies. `src: Core features rule 34`
- [ ] `C-CF-60` `capability` The cookie choice survives a page reload. `src: Core features rule 34`
- [ ] `C-CF-61` `constraint` No analytics tag loads before the cookie choice is accepted. `src: Core features rule 35`
- [ ] `C-CF-62` `capability` The app records each page view with the route plus the moment. `src: Core features rule 36`
- [ ] `C-CF-63` `role` An anonymous request for a console path is sent to `/login`. `src: Core features rule 37`
- [ ] `C-CF-64` `role` A `reader` request for a console path is refused outright. `src: Core features rule 37`
- [ ] `C-CF-65` `capability` Project creation runs as three steps, each at a separate address. `src: Core features rule 38`
- [ ] `C-CF-66` `capability` Returning to a wizard step restores what the editor entered. `src: Core features rule 38`
- [ ] `C-CF-67` `ui` Finishing the wizard lands on a full-page confirmation naming the new project. `src: Core features rule 39`
- [ ] `C-CF-68` `constraint` A project made through the wizard starts as a draft. `src: Core features rule 39`
- [ ] `C-CF-69` `literal` An uploaded cover lands in the bucket at `projects/{project_id}/{sha256_of_bytes}.{ext}`. `src: Core features rule 40`
- [ ] `C-CF-70` `literal` An uploaded press kit lands in the bucket at `press-kits/{project_id}/{sha256_of_bytes}.{ext}`. `src: Core features rule 40`
- [ ] `C-CF-71` `constraint` Object bytes never live on the app's own filesystem. `src: Core features rule 40`
- [ ] `C-CF-72` `capability` Publishing a project makes the project visible on the public index. `src: Core features rule 41`
- [ ] `C-CF-73` `capability` Unpublishing a project removes the project from every discipline filter. `src: Core features rule 41`
- [ ] `C-CF-74` `constraint` Publishing an already-published project creates no second project. `src: Core features rule 41`
- [ ] `C-CF-75` `constraint` A draft project is absent from the work index. `src: Core features rule 42`
- [ ] `C-CF-76` `constraint` A draft project is absent from every one of the eight filters. `src: Core features rule 42`
- [ ] `C-CF-77` `constraint` A direct request for a draft project's public address answers not found. `src: Core features rule 42`
- [ ] `C-CF-78` `role` A draft project's cover object is served to an `author` alone. `src: Core features rule 43`
- [ ] `C-CF-79` `constraint` A request for a draft cover carrying a `reader` token returns no bytes. `src: Core features rule 43`
- [ ] `C-CF-80` `role` A press-kit object is served to a signed-in account alone. `src: Core features rule 44`
- [ ] `C-CF-81` `constraint` An anonymous request for a press-kit object returns no bytes. `src: Core features rule 44`
- [ ] `C-CF-82` `constraint` The app never makes a bucket publicly readable. `src: Core features rule 45`
- [ ] `C-CF-83` `constraint` A request made straight to the store for an object key returns no bytes. `src: Core features rule 45`
- [ ] `C-CF-84` `literal` The route `/sitemap.xml` lists every public route. `src: Core features rule 46`
- [ ] `C-CF-85` `constraint` The sitemap names no draft project. `src: Core features rule 46`
- [ ] `C-CF-86` `literal` The route `/robots.txt` names the sitemap address. `src: Core features rule 47`

## C-UF User flow

- [ ] `C-UF-01` `capability` The app serves the route `/` as the hero plus reel. `src: User flow route table`
- [ ] `C-UF-02` `capability` The app serves the route `/press` as the dated feed. `src: User flow route table`
- [ ] `C-UF-03` `capability` The app serves the route `/team` as the studio story. `src: User flow route table`
- [ ] `C-UF-04` `capability` The app serves the route `/privacy` with authored content. `src: User flow route table`
- [ ] `C-UF-05` `capability` A successful sign-in lands on the path originally requested. `src: User flow entry para`
- [ ] `C-UF-06` `capability` Signing out returns the visitor to `/`. `src: User flow entry para`
- [ ] `C-UF-07` `constraint` An expired token leaves the attempted action unwritten. `src: User flow entry para`
- [ ] `C-UF-08` `ui` The work grid under a filter matching nothing shows an empty state. `src: User flow states para`
- [ ] `C-UF-09` `ui` The console enquiry list before the first enquiry shows an empty state. `src: User flow states para`
- [ ] `C-UF-10` `constraint` A failed region never takes the whole route down. `src: User flow states para`
- [ ] `C-UF-11` `ui` Each wizard step makes the editor's position in the three-step sequence legible. `src: User flow states para`
- [ ] `C-UF-12` `ui` A loading state reserves the layout so nothing jumps when the content lands. `src: User flow states para`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The work route ground is a near-white neutral. `src: UI/UX notes colour para`
- [ ] `C-UX-02` `ui` The home route ground is a near-black cool neutral. `src: UI/UX notes colour para`
- [ ] `C-UX-03` `ui` The single action accent is a deep, soft teal used rarely. `src: UI/UX notes colour para`
- [ ] `C-UX-04` `constraint` The action accent never appears on body-size text on the paper ground. `src: UI/UX notes colour para`
- [ ] `C-UX-05` `ui` A failure state wears a colour that appears nowhere else. `src: UI/UX notes meaning-carrying colour para`
- [ ] `C-UX-06` `constraint` Meaning is never carried by colour alone. `src: UI/UX notes accessibility para`
- [ ] `C-UX-07` `ui` The site commits to one designed scheme with no second theme. `src: UI/UX notes mode para`
- [ ] `C-UX-08` `literal` Display, body plus interface type is set in `Inter`. `src: UI/UX notes type para`
- [ ] `C-UX-09` `literal` The Japanese glyphs beneath the lens are set in `Noto Sans JP`. `src: UI/UX notes type para`
- [ ] `C-UX-10` `ui` A swash letter is an inline element around one glyph rather than a change of family. `src: UI/UX notes swash para`
- [ ] `C-UX-11` `ui` A screen reader reads a swash word as one word. `src: UI/UX notes swash para`
- [ ] `C-UX-12` `ui` Motion character across the whole site is eased. `src: UI/UX notes motion para`
- [ ] `C-UX-13` `ui` A leaving element accelerates away harder than the same element arrived. `src: UI/UX notes motion para`
- [ ] `C-UX-14` `ui` Pointing at the primary pill moves the arrow plus both glyph layers together. `src: UI/UX notes motion para`
- [ ] `C-UX-15` `capability` A reduced-motion request holds the hero on a still frame. `src: UI/UX notes reduced motion para`
- [ ] `C-UX-16` `constraint` A reduced-motion request keeps the fade where the movement is removed. `src: UI/UX notes reduced motion para`
- [ ] `C-UX-17` `ui` The work grid runs two columns at desktop width. `src: UI/UX notes responsive para`
- [ ] `C-UX-18` `ui` The work grid runs one column at phone width. `src: UI/UX notes responsive para`
- [ ] `C-UX-19` `capability` The work filters swap to a native select control at narrow widths. `src: UI/UX notes responsive para`
- [ ] `C-UX-20` `constraint` Nothing overflows sideways at the narrow viewport. `src: UI/UX notes responsive para`
- [ ] `C-UX-21` `ui` Body text meets the WCAG AA contrast bar against the text's own ground. `src: UI/UX notes accessibility para`
- [ ] `C-UX-22` `capability` Every interactive element is operable by keyboard navigation with a visible focus ring. `src: UI/UX notes accessibility para`
- [ ] `C-UX-23` `capability` The navigation overlay traps focus until the overlay closes. `src: UI/UX notes accessibility para`
- [ ] `C-UX-24` `capability` The filtered result count is announced to a non-visual visitor. `src: UI/UX notes accessibility para`
- [ ] `C-UX-25` `ui` Every content image carries alternative text. `src: UI/UX notes accessibility para`
- [ ] `C-UX-26` `ui` The studio console reads as a plain working surface rather than the public display register. `src: UI/UX notes register para`
- [ ] `C-UX-27` `ui` The enquiry success state reads as a reply from the studio rather than a system notice. `src: UI/UX notes register para`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app reads the datastore address from `DATABASE_URL`. `src: Technical requirements para 2`
- [ ] `C-TR-02` `contract` The app reads the object store address from `STORAGE_ENDPOINT`. `src: Technical requirements para 2`
- [ ] `C-TR-03` `constraint` The app never hardcodes a host or a port. `src: Technical requirements para 2`
- [ ] `C-TR-04` `constraint` The app introduces no second datastore beyond PostgreSQL. `src: Technical requirements para 4`
- [ ] `C-TR-05` `constraint` No credential appears in anything the browser downloads. `src: Technical requirements para 5`
- [ ] `C-TR-06` `capability` Every public route carries a title distinct from every other public route. `src: Technical requirements para 6`
- [ ] `C-TR-07` `constraint` The build ships no image file. `src: Technical requirements zero-asset para`
- [ ] `C-TR-08` `constraint` The build ships no font file. `src: Technical requirements zero-asset para`
- [ ] `C-TR-09` `capability` The hero pauses the hero loop when the tab is hidden. `src: Technical requirements performance para`
- [ ] `C-TR-10` `capability` An image swaps from preview to full asset without reflowing the layout. `src: Technical requirements performance para`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema holds a `projects` table carrying a `status` field. `src: Data model projects para`
- [ ] `C-DM-02` `data` A project's disciplines live in a `project_disciplines` table. `src: Data model projects para`
- [ ] `C-DM-03` `data` The schema holds a `press_items` table carrying a `category` field. `src: Data model press_items para`
- [ ] `C-DM-04` `data` The schema holds an `enquiries` table carrying a `source` field. `src: Data model enquiries para`
- [ ] `C-DM-05` `constraint` The press category count is computed on read rather than stored. `src: Data model press_items para`
- [ ] `C-DM-06` `constraint` The member count is computed on read rather than stored. `src: Data model team_members para`
- [ ] `C-DM-07` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model password block`
- [ ] `C-DM-08` `contract` Each seeded account is written into `/app/USER_README.md`. `src: Data model password block`
- [ ] `C-DM-09` `literal` The seed carries eight published projects plus one draft. `src: Data model seed para`
- [ ] `C-DM-10` `literal` The seed carries the draft project `AMBERLINE ‣ STUDIO REBRAND`. `src: Data model seed para`
- [ ] `C-DM-11` `literal` The seed carries seven press items. `src: Data model seed para`
- [ ] `C-DM-12` `constraint` Restarting the app duplicates no seeded row. `src: Data model closing line`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The palette is exposed as custom properties named on the document root. `src: Front-end specification token layer`
- [ ] `C-FE-02` `literal` The token `--colorTealAction` carries the one accent. `src: Front-end specification token layer`
- [ ] `C-FE-03` `literal` Body type resolves to `16px` over `18.4px`. `src: Front-end specification type ramp`
- [ ] `C-FE-04` `literal` The display line resolves to `45px` over `48.915px`. `src: Front-end specification type ramp`
- [ ] `C-FE-05` `ui` The wordmark is drawn by the app rather than loaded. `src: Front-end specification iconography`
- [ ] `C-FE-06` `ui` The wordmark appears inside the route-transition veil. `src: Front-end specification iconography`
- [ ] `C-FE-07` `literal` The marker between a client plus a piece stays the typed character `‣`. `src: Front-end specification typed characters`
- [ ] `C-FE-08` `ui` The not-found route carries no reveal, no parallax. `src: Front-end specification not-found para`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app serves a single studio with no second tenant. `src: Constraints list`
- [ ] `C-CN-02` `constraint` The app sends no email. `src: Constraints list`
- [ ] `C-CN-03` `constraint` The app makes no external network call at run time. `src: Constraints list`
- [ ] `C-CN-04` `constraint` The app opens no realtime channel. `src: Constraints list`
- [ ] `C-CN-05` `constraint` The app stays responsive with a few thousand stored enquiries. `src: Constraints list`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract line 1`
- [ ] `C-DC-02` `contract` The container-internal port is `4173`. `src: Deployment contract line 1`
- [ ] `C-DC-03` `contract` The HTTP API is served under the `/api` prefix on the same origin. `src: Deployment contract line 2`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract line 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract line 4`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract line 5`
- [ ] `C-DC-07` `contract` The directory `.browser_screenshots/` exists at the app root, empty. `src: Deployment contract line 6`
- [ ] `C-DC-08` `contract` The app serves a production build behind a static or preview server. `src: Deployment contract line 7`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends. `src: Deployment contract line 8`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0` rather than a loopback address. `src: Deployment contract line 9`
- [ ] `C-DC-11` `contract` The app starts no copy of a backing service named in the brief. `src: Deployment contract line 10`
- [ ] `C-DC-12` `contract` The app uses no persistent volume. `src: Deployment contract line 12`
- [ ] `C-DC-13` `capability` A list endpoint returns a top-level JSON array. `src: Deployment contract API shapes para`
- [ ] `C-DC-14` `constraint` An unauthorized call is rejected as a client error rather than a server error. `src: Deployment contract API shapes para`
- [ ] `C-DC-15` `constraint` An in-memory store standing in for the bucket is a violation of the contract. `src: Deployment contract no mocks para`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | seeded password for every account | C-DM-07 | Data model password block |
| `author@example.com` | seeded studio editor email | C-RL-09 | User roles seeded accounts table |
| `reader@example.com` | seeded press contact email | C-RL-10 | User roles seeded accounts table |
| `hello@kanso.studio` | studio contact address in the footer | C-CF-15 | Core features rule 8 |
| `/sitemap.xml` | route listing every public route | C-CF-84 | Core features rule 46 |
| `/robots.txt` | route pointing at the sitemap | C-CF-86 | Core features rule 47 |
| `/studio/enquiries` | console route serving the enquiry list | C-CF-58 | Core features rule 33 |
| `/api/health` | health route | C-DC-04 | Deployment contract line 3 |
| `/api` | API prefix on the app's own origin | C-DC-03 | Deployment contract line 2 |
| `APP_PUBLIC_URL` | environment variable carrying the app address | C-DC-01 | Deployment contract line 1 |
| `DATABASE_URL` | environment variable carrying the datastore address | C-TR-01 | Technical requirements para 2 |
| `STORAGE_ENDPOINT` | environment variable carrying the object store address | C-TR-02 | Technical requirements para 2 |
| `4173` | container-internal port | C-DC-02 | Deployment contract line 1 |
| `200` | ready answer from the health route | C-DC-04 | Deployment contract line 3 |
| `0.0.0.0` | bind address | C-DC-10 | Deployment contract line 9 |
| `/app/USER_README.md` | file carrying the seeded logins | C-DC-06 | Deployment contract line 5 |
| `.browser_screenshots/` | reserved directory at the app root | C-DC-07 | Deployment contract line 6 |
| `company_website` | hidden decoy field on the enquiry form | C-CF-55 | Core features rule 32 |
| `60` | seconds inside which a fourth enquiry is refused | C-CF-56 | Core features rule 32 |
| `11 members` | derived member count on the team grid | C-CF-47 | Core features rule 27 |
| `Features [3]` | derived press badge for the seeded collection | C-CF-36 | Core features rule 21 |
| `RECENT WORK` | eyebrow above the recent-work reel | C-CF-22 | Core features rule 12 |
| `Discover all projects` | label on the reel call to action | C-CF-27 | Core features rule 14 |
| `PRESS & NEWS` | header link label in the casing given | C-CF-10 | Core features rule 5 |
| `Read more` | label on a press feed item link | C-CF-38 | Core features rule 22 |
| `Designing for the future` | tag on the featured series block | C-CF-39 | Core features rule 23 |
| `Vol 01` | index label of the first series volume | C-CF-40 | Core features rule 23 |
| `Page not found` | heading on the not-found route | C-CF-49 | Core features rule 29 |
| `This website uses cookies.` | copy on the cookie rail | C-CF-59 | Core features rule 34 |
| `[ a city-based global network ]` | footnote on the team intro | C-CF-45 | Core features rule 25 |
| `WE WOULD LOVE TO HEAR FROM YOU.` | footer call to action | C-CF-14 | Core features rule 8 |
| `We are a brand` | first line of the hero headline | C-CF-19 | Core features rule 10 |
| `All` | reset control on the work filter bar | C-CF-28 | Core features rule 16 |
| `SPATIAL` | discipline filter label | C-CF-28 | Core features rule 16 |
| `Campaign` | discipline filter label | C-CF-28 | Core features rule 16 |
| `News` | press category label | C-CF-35 | Core features rule 21 |
| `Events` | press category label | C-CF-35 | Core features rule 21 |
| `Features` | press category label | C-CF-35 | Core features rule 21 |
| `Articles` | press category label | C-CF-35 | Core features rule 21 |
| `featured_home` | project field flagging a home-reel project | C-CF-25 | Core features rule 13 |
| `projects/{project_id}/{sha256_of_bytes}.{ext}` | object key scheme for a project cover | C-CF-71 | Core features rule 40 |
| `press-kits/{project_id}/{sha256_of_bytes}.{ext}` | object key scheme for a press kit | C-CF-72 | Core features rule 40 |
| `AMBERLINE ‣ STUDIO REBRAND` | the one seeded draft project | C-DM-10 | Data model seed para |
| `2011` | year of the first studio chapter | C-CF-48 | Core features rule 28 |
| `2019` | year of the second studio chapter | C-CF-48 | Core features rule 28 |
| `Inter` | family carrying display, body plus interface type | C-UX-08 | UI/UX notes type para |
| `Noto Sans JP` | family carrying the Japanese glyphs | C-UX-09 | UI/UX notes type para |
| `--colorTealAction` | custom property carrying the one accent | C-FE-02 | Front-end specification token layer |
| `16px` | rendered body size | C-FE-03 | Front-end specification type ramp |
| `18.4px` | rendered body line height | C-FE-03 | Front-end specification type ramp |
| `45px` | rendered display size | C-FE-04 | Front-end specification type ramp |
| `48.915px` | rendered display line height | C-FE-04 | Front-end specification type ramp |
| `‣` | marker between a client plus a piece in a project title | C-FE-07 | Front-end specification typed characters |
| `Home` | header link label | C-CF-09 | Core features rule 5 |
| `Work` | header link label | C-CF-09 | Core features rule 5 |
| `Services` | header link label | C-CF-09 | Core features rule 5 |
| `team` | header link label in lower case | C-CF-10 | Core features rule 5 |
| `contact` | header link label in lower case | C-CF-10 | Core features rule 5 |
| `/work` | filterable project index route | C-CF-08 | Core features rule 4 |
| `/press` | press route | C-UF-02 | User flow route table |
| `/team` | team route | C-UF-03 | User flow route table |
| `/privacy` | privacy route | C-UF-04 | User flow route table |
| `/` | home route | C-UF-01 | User flow route table |
| `/login` | sign-in route | C-CF-66 | Core features rule 37 |
| `/signup` | open registration route | C-RL-07 | User roles signup para |
| `author` | role token for the studio editor | C-RL-06 | User roles table row 3 |
| `reader` | role token for a registered press contact | C-RL-03 | User roles table row 2 |
| `status` | projects field carrying draft or published | C-DM-01 | Data model projects para |
| `projects` | table holding every project | C-DM-01 | Data model projects para |
| `project_disciplines` | table holding a project's disciplines | C-DM-02 | Data model projects para |
| `press_items` | table holding every press item | C-DM-03 | Data model press_items para |
| `category` | press_items field carrying the press category | C-DM-03 | Data model press_items para |
| `enquiries` | table holding every enquiry | C-DM-04 | Data model enquiries para |
| `source` | enquiries field naming the surface of origin | C-DM-04 | Data model enquiries para |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the exact shade of every colour in the palette | C-UX-03 | carried as family, tone plus shade so the builder chooses the value |
| the duration of every motion moment | C-UX-12 | carried as character so the builder tunes the value |
| the pixel width of each designed breakpoint | C-UX-17 | carried as phone, tablet plus desktop so the builder chooses the value |
| the corner radius of each round register | C-UX-01 | carried as pill, card plus circle so the builder chooses the value |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 3 |
| User roles | 1 | 10 |
| Core features | 15 | 86 |
| User flow | 4 | 12 |
| UI and UX notes | 7 | 27 |
| Technical requirements | 4 | 10 |
| Data model | 5 | 12 |
| Front-end specification | 0 | 8 |
| Constraints | 2 | 5 |
| Deployment contract | 10 | 15 |

Definition of done carries one obligation-bearing sentence, restating the core outcome plus the hardest guarantee. Both already hold items in Core features, so the section mints no item of its own.
