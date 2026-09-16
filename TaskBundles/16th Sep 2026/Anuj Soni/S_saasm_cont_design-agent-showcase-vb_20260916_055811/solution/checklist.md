# Checklist: Design Agent Showcase

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, technical, datamodel, constraints, deployment
Sections absent: buildplan
Items: 168
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public marketing site for an AI website builder named `Kanvo`. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app embeds animated replicas of the product inside the marketing routes. `src: Overview para 2`
- [ ] `C-OV-03` `capability` The app collects a visitor as a lead through the answer-engine scanner. `src: Overview para 2`
- [ ] `C-OV-04` `capability` The app keeps customer stories behind a sign-in boundary. `src: Overview para 4`
- [ ] `C-OV-05` `constraint` The app generates no website for a visitor. `src: Overview para 5`
- [ ] `C-OV-06` `constraint` The app calls no model at run time. `src: Overview para 5`
- [ ] `C-OV-07` `constraint` The app sends no email. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out visitor reads every published open story in full. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A signed-out visitor reads only the opening of a published members story. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A signed-out visitor cannot reach any /studio route. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A reader reads the full body of a published members story. `src: User roles table row 2`
- [ ] `C-RL-05` `role` A reader cannot read the leads desk. `src: User roles table row 2`
- [ ] `C-RL-06` `role` An author publishes a story that the same author owns. `src: User roles table row 3`
- [ ] `C-RL-07` `role` An author cannot edit another author's story. `src: User roles table row 3`
- [ ] `C-RL-08` `role` An author cannot read another author's draft story. `src: User roles table row 3`
- [ ] `C-RL-09` `role` An author reads the leads desk. `src: User roles table row 3`
- [ ] `C-RL-10` `role` The server rejects a reader request to any author-only endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-11` `role` Signup creates an account whose role is `reader`. `src: User roles, signup paragraph`
- [ ] `C-RL-12` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles, seeded accounts table`

## C-CF Core features

- [ ] `C-CF-01` `capability` The app issues a bearer token at login. `src: Core features, Auth`
- [ ] `C-CF-02` `capability` The app stores every account password hashed. `src: Core features, Auth rule 1`
- [ ] `C-CF-03` `capability` The app rejects a signup whose email already has an account. `src: Core features, Auth rule 2`
- [ ] `C-CF-04` `capability` The app denies a login carrying the wrong password. `src: Core features, Auth rule 3`
- [ ] `C-CF-05` `capability` The app refuses a call carrying an expired token. `src: Core features, Auth rule 4`
- [ ] `C-CF-06` `capability` The app shows the same fixed top bar on every route. `src: Core features, shared chrome rule 1`
- [ ] `C-CF-07` `capability` The app shows the same footer directory on every route. `src: Core features, shared chrome rule 5`
- [ ] `C-CF-08` `capability` The app opens a full-width panel of grouped links under each of the three menu labels. `src: Core features, shared chrome rule 1`
- [ ] `C-CF-09` `capability` Every internal link that leads somewhere resolves to a page. `src: Core features, shared chrome rule 6`
- [ ] `C-CF-10` `capability` The app asks a first-time visitor once about non-essential cookies. `src: Core features, shared chrome rule 7`
- [ ] `C-CF-11` `capability` The cookie choice survives a reload. `src: Core features, shared chrome rule 7`
- [ ] `C-CF-12` `capability` The app serves a privacy page at `/privacy` reachable from the footer. `src: Core features, privacy page`
- [ ] `C-CF-13` `capability` The privacy page names every class of record the site keeps about a visitor. `src: Core features, privacy page`
- [ ] `C-CF-14` `capability` The app renders its own not-found page for any address the site does not serve. `src: Core features, not-found rule 1`
- [ ] `C-CF-15` `literal` The not-found page answers status `404`. `src: Core features, not-found rule 2`
- [ ] `C-CF-16` `literal` A message sent from the not-found page records the source `not-found`. `src: Core features, not-found rule 3`
- [ ] `C-CF-17` `capability` The app records every view of a public route with the route. `src: Core features, page-view record rule 1`
- [ ] `C-CF-18` `capability` The app records every view of a public route with the moment of the view. `src: Core features, page-view record rule 1`
- [ ] `C-CF-19` `capability` A page-view record omits the account reference when the viewer declined the analytics cookie choice. `src: Core features, page-view record rule 2`
- [ ] `C-CF-20` `capability` The home route opens on a headline over a continuously moving fluid field. `src: Core features, Home rule 2`
- [ ] `C-CF-21` `capability` The fluid field stops when the fluid field is scrolled out of view. `src: Core features, Home rule 2`
- [ ] `C-CF-22` `capability` The home route shows eight customer wordmarks under the label `Meet our customers`. `src: Core features, Home rule 3`
- [ ] `C-CF-23` `capability` The home route plays three agent scenes under one heading. `src: Core features, Home rule 4`
- [ ] `C-CF-24` `capability` The home route shows a dense grid of platform tiles. `src: Core features, Home rule 5`
- [ ] `C-CF-25` `capability` The home route assembles one display line letter by letter against scroll. `src: Core features, Home rule 6`
- [ ] `C-CF-26` `capability` The AI route shows the canvas replica with a page tree rail. `src: Core features, AI route rule 2`
- [ ] `C-CF-27` `capability` The AI route walks four capability scenes under one heading. `src: Core features, AI route rule 4`
- [ ] `C-CF-28` `capability` The CMS route shows a collections rail beside a table of content rows. `src: Core features, CMS route rule 2`
- [ ] `C-CF-29` `capability` The CMS route plays the import scene in one fixed order against scroll. `src: Core features, CMS route rule 3`
- [ ] `C-CF-30` `capability` The CMS route lists the published customer stories with a category tag apiece. `src: Core features, CMS route rule 5`
- [ ] `C-CF-31` `capability` The SEO route shows a page-settings replica bound to content variables. `src: Core features, SEO route rule 2`
- [ ] `C-CF-32` `capability` The SEO route shows a vitals readout beside a well-known files panel. `src: Core features, SEO route rule 3`
- [ ] `C-CF-33` `capability` Each product replica renders the frame belonging to one progress input. `src: Core features, replicas rule 2`
- [ ] `C-CF-34` `capability` Each product replica renders the same frame for a repeated progress input. `src: Core features, replicas rule 2`
- [ ] `C-CF-35` `capability` Every word a product replica shows is stored content. `src: Core features, replicas rule 4`
- [ ] `C-CF-36` `capability` The app creates a story from its own address at `/studio/stories/new`. `src: Core features, story desk rule 2`
- [ ] `C-CF-37` `capability` A newly created story carries the state `draft`. `src: Core features, story desk rule 2`
- [ ] `C-CF-38` `capability` The app rejects a second story claiming a slug already held. `src: Core features, story desk rule 3`
- [ ] `C-CF-39` `capability` The app omits a draft story from the public story index. `src: Core features, story desk rule 4`
- [ ] `C-CF-40` `capability` The app refuses a signed-out request for a draft story by slug. `src: Core features, story desk rule 4`
- [ ] `C-CF-41` `capability` The app refuses another author's request for a draft story by identifier. `src: Core features, story desk rule 4`
- [ ] `C-CF-42` `capability` The app serves a published open story in full to a signed-out visitor. `src: Core features, story desk rule 5`
- [ ] `C-CF-43` `capability` The app withholds the body of a members story from a signed-out visitor. `src: Core features, story desk rule 6`
- [ ] `C-CF-44` `capability` The app lists published stories newest published first. `src: Core features, story desk rule 7`
- [ ] `C-CF-45` `capability` The app returns a story to the state `draft` on unpublish. `src: Core features, story desk rule 8`
- [ ] `C-CF-46` `capability` The server denies an author's edit of another author's story. `src: Core features, story desk rule 9`
- [ ] `C-CF-47` `capability` The app writes uploaded cover bytes into the object store bucket. `src: Core features, covers rule 1`
- [ ] `C-CF-48` `literal` The app names a cover object `stories/{story_id}/{sha256_of_bytes}.{ext}`. `src: Core features, covers rule 2`
- [ ] `C-CF-49` `capability` The app rejects a cover upload whose type is outside the three accepted image types. `src: Core features, covers rule 3`
- [ ] `C-CF-50` `capability` The app refuses to save a cover carrying no alternative text. `src: Core features, covers rule 4`
- [ ] `C-CF-51` `capability` The app keeps at most one cover for a story. `src: Core features, covers rule 5`
- [ ] `C-CF-52` `capability` The app streams cover bytes from its own route rather than a link to the store. `src: Core features, covers rule 6`
- [ ] `C-CF-53` `capability` The app refuses a draft story's cover to every caller but the owning author. `src: Core features, covers rule 7`
- [ ] `C-CF-54` `capability` The scanner card holds a website field beside two name fields. `src: Core features, scanner rule 2`
- [ ] `C-CF-55` `capability` The scanner refuses an address naming no host with a dot. `src: Core features, scanner rule 3`
- [ ] `C-CF-56` `capability` The scanner refuses a business email at a consumer mail domain. `src: Core features, scanner rule 4`
- [ ] `C-CF-57` `capability` An accepted submission answers with a scan reference. `src: Core features, scanner rule 5`
- [ ] `C-CF-58` `literal` A scan reference reads `scan-` followed by twelve lowercase hexadecimal characters. `src: Core features, scanner rule 5`
- [ ] `C-CF-59` `capability` A scan advances from queued to complete with no further visitor action. `src: Core features, scanner rule 6`
- [ ] `C-CF-60` `capability` A complete scan carries exactly four graded sections. `src: Core features, scanner rule 7`
- [ ] `C-CF-61` `capability` A complete scan carries an overall grade from three words. `src: Core features, scanner rule 7`
- [ ] `C-CF-62` `capability` Two scans of one address produce identical grades. `src: Core features, scanner rule 8`
- [ ] `C-CF-63` `capability` A scan report omits the name of the person who submitted the scan. `src: Core features, scanner rule 9`
- [ ] `C-CF-64` `capability` The scanner refuses a fourth scan from one business email inside an hour. `src: Core features, scanner rule 11`
- [ ] `C-CF-65` `capability` The newsletter records a new address with the status `pending`. `src: Core features, newsletter rule 2`
- [ ] `C-CF-66` `capability` The newsletter moves a confirmed address to the status `confirmed`. `src: Core features, newsletter rule 3`
- [ ] `C-CF-67` `capability` The newsletter creates no second record for a repeated address. `src: Core features, newsletter rule 4`
- [ ] `C-CF-68` `capability` The subscriber count rises once for one confirmed address. `src: Core features, newsletter rule 5`
- [ ] `C-CF-69` `capability` The app rejects a newsletter submission whose address is malformed. `src: Core features, newsletter rule 6`
- [ ] `C-CF-70` `capability` A contact message records the source of the submission. `src: Core features, contact message rule 1`
- [ ] `C-CF-71` `capability` The app rejects a contact message missing its body. `src: Core features, contact message rule 3`
- [ ] `C-CF-72` `capability` The leads desk shows every scan beside the business email that started the scan. `src: Core features, leads desk rule 1`
- [ ] `C-CF-73` `capability` The server denies a signed-out request for the leads desk. `src: Core features, leads desk rule 2`

## C-UF User flow

- [ ] `C-UF-01` `capability` The app serves the five marketing routes named in the route table. `src: User flow route table`
- [ ] `C-UF-02` `capability` The app sends a signed-out request for a studio route to `/login`. `src: User flow, entry and redirects`
- [ ] `C-UF-03` `capability` The app lands a signed-in author on the destination preserved before login. `src: User flow, entry and redirects`
- [ ] `C-UF-04` `capability` The app lands a signed-in author with no preserved destination on `/studio`. `src: User flow, entry and redirects`
- [ ] `C-UF-05` `capability` The app shows its own not-found page to a reader who opens a studio address. `src: User flow, entry and redirects`
- [ ] `C-UF-06` `capability` Signing out makes every studio address unreachable. `src: User flow, entry and redirects`
- [ ] `C-UF-07` `capability` Every list surface carries an empty state written for that surface. `src: User flow, States`
- [ ] `C-UF-08` `capability` Every route carries a loading state until its records arrive. `src: User flow, States`
- [ ] `C-UF-09` `capability` An error leaves the surface standing with an inline banner naming what went wrong. `src: User flow, States`
- [ ] `C-UF-10` `capability` A scan that has not completed shows progress rather than an empty report. `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The site reads as one continuous near-black scene from the first viewport to the footer. `src: UI/UX notes, Mode`
- [ ] `C-UX-02` `ui` The ground is the only background family on the site. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-03` `ui` Depth reads from a hairline stroke rather than from a large soft blur. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-04` `ui` The brand accent appears only on the product's own accent surfaces. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-05` `ui` Three meanings each own one colour that appears nowhere else. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-06` `ui` Interface type is small where the page reads as software. `src: UI/UX notes, Type`
- [ ] `C-UX-07` `ui` Display type is large where the page makes a statement. `src: UI/UX notes, Type`
- [ ] `C-UX-08` `ui` The primary action is the only pill shape on the site. `src: UI/UX notes, Shape`
- [ ] `C-UX-09` `ui` Marketing sections read as separate at a glance without a dividing line. `src: UI/UX notes, Density`
- [ ] `C-UX-10` `ui` Every surface moves on one speed with one curve. `src: UI/UX notes, Motion`
- [ ] `C-UX-11` `ui` A section reveal bound to scroll position runs backwards on scroll up. `src: UI/UX notes, Motion`
- [ ] `C-UX-12` `ui` Exactly three named animations loop infinitely at run time. `src: UI/UX notes, Motion`
- [ ] `C-UX-13` `ui` A reduced-motion preference holds the fluid field on a still frame. `src: UI/UX notes, Motion`
- [ ] `C-UX-14` `ui` Every control carries a resting, pointed-at, pressed, focused, unavailable state apiece. `src: UI/UX notes, Components`
- [ ] `C-UX-15` `ui` Body text meets the WCAG AA contrast bar against its background. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-16` `ui` Every interactive element is reachable by keyboard navigation with a visible focus ring. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-17` `ui` Masked text stays present in the document for assistive technology. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-18` `ui` Every content image carries alternative text. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-19` `ui` The layout holds at phone, tablet, desktop widths with no sideways overflow. `src: UI/UX notes, Responsive`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Text is set in the `Inter` family. `src: Front-end specification, type table`
- [ ] `C-FE-02` `ui` Display headings are set in the `Space Grotesk` family. `src: Front-end specification, type table`
- [ ] `C-FE-03` `ui` Display headings scale with the width of their column. `src: Front-end specification, display paragraph`
- [ ] `C-FE-04` `ui` Every symbol on the site is inline vector geometry rather than a picture file. `src: Front-end specification, Iconography`
- [ ] `C-FE-05` `ui` One reserved top layer carries the cookie card alone. `src: Front-end specification, layout paragraph`
- [ ] `C-FE-06` `ui` Customer wordmarks are drawn by the browser from the palette. `src: Front-end specification, Generated imagery`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app reaches its database at `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The app reaches its object store at `STORAGE_ENDPOINT`. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The app reads its bucket name from `STORAGE_BUCKET`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The browser receives an application shell on first paint. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` Every response carries a request identifier in an `X-Request-Id` header. `src: Technical requirements para 1`
- [ ] `C-TR-06` `capability` Two concurrent creates of one slug leave exactly one story. `src: Technical requirements, Contention and replay`
- [ ] `C-TR-07` `capability` Two concurrent cover uploads for one story leave exactly one cover. `src: Technical requirements, Contention and replay`
- [ ] `C-TR-08` `capability` Two concurrent subscriptions of one address leave exactly one subscriber. `src: Technical requirements, Contention and replay`
- [ ] `C-TR-09` `capability` A refused story create leaves no orphaned row behind. `src: Technical requirements, Contention and replay`
- [ ] `C-TR-10` `constraint` Nothing the browser downloads carries the store access key. `src: Technical requirements, What the browser downloads`
- [ ] `C-TR-11` `capability` The heading of every route is text that paints before the fluid field starts. `src: Technical requirements, Loading order`

## C-DM Data model

- [ ] `C-DM-01` `data` An account row holds a role of `author` or `reader`. `src: Data model, accounts`
- [ ] `C-DM-02` `data` A story row holds a state of `draft` or `published`. `src: Data model, stories`
- [ ] `C-DM-03` `data` A story row holds an access of `open` or `members`. `src: Data model, stories`
- [ ] `C-DM-04` `data` A story slug belongs to exactly one story row. `src: Data model, stories`
- [ ] `C-DM-05` `data` A cover row holds the object key of the bytes in the bucket. `src: Data model, story_covers`
- [ ] `C-DM-06` `data` A scan row holds a status of `queued`, `running` or `complete`. `src: Data model, scans`
- [ ] `C-DM-07` `data` A scan section row holds one of the four section names. `src: Data model, scan_sections`
- [ ] `C-DM-08` `data` A subscriber row holds a status of `pending` or `confirmed`. `src: Data model, subscribers`
- [ ] `C-DM-09` `data` A message row holds a source of `enterprise` or `not-found`. `src: Data model, messages`
- [ ] `C-DM-10` `data` The app seeds three accounts at first start. `src: Data model, Seed data`
- [ ] `C-DM-11` `data` The app seeds five customer stories at first start. `src: Data model, Seed data`
- [ ] `C-DM-12` `data` Restarting the app duplicates no seeded row. `src: Data model, Seed data`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app completes a scan without fetching the submitted address. `src: Constraints bullet 3`
- [ ] `C-CN-02` `constraint` The app takes no payment. `src: Constraints bullet 4`
- [ ] `C-CN-03` `constraint` The app accepts no upload beyond a story cover image. `src: Constraints bullet 7`
- [ ] `C-CN-04` `constraint` The app ships no binary asset. `src: Constraints bullet 8`
- [ ] `C-CN-05` `constraint` Nothing a reader types into a replica changes a stored record. `src: Constraints bullet 9`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app answers on the public origin named by `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The app listens on container-internal port `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The app reads its public port from `APP_PUBLIC_PORT`. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The app serves its HTTP API under the `/api` prefix on the same origin. `src: Deployment contract bullet 2`
- [ ] `C-DC-05` `contract` The app answers its health route with no manual start step. `src: Deployment contract bullet 3`
- [ ] `C-DC-06` `contract` The app writes login credentials to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` The app root carries an empty `.browser_screenshots/` directory. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` The app root carries an empty `.downloads/` directory. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` The app serves a production build rather than a development server. `src: Deployment contract bullet 7`
- [ ] `C-DC-10` `contract` The server still answers after the build session has ended. `src: Deployment contract bullet 8`
- [ ] `C-DC-11` `contract` The app answers on the public origin from outside its own container. `src: Deployment contract bullet 9`
- [ ] `C-DC-12` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes`
- [ ] `C-DC-13` `contract` An invalid call is rejected as a client error rather than a server error. `src: Deployment contract, API shapes`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | password for every seeded account | C-RL-12 | ## User roles, seeded accounts table |
| `404` | status the not-found page answers | C-CF-15 | ## Core features, not-found rule 2 |
| `not-found` | source recorded for a message sent from the not-found page | C-CF-16 | ## Core features, not-found rule 3 |
| `stories/{story_id}/{sha256_of_bytes}.{ext}` | object key scheme for a story cover | C-CF-48 | ## Core features, covers rule 2 |
| `scan-` | prefix of every scan reference | C-CF-57 | ## Core features, scanner rule 5 |
| `4.5:1` | minimum contrast ratio for body text | C-UX-15 | ## Technical requirements, Contrast |
| `44x44` | minimum interactive target size | C-UX-16 | ## Technical requirements, Contrast |
| `APP_PUBLIC_URL` | public origin the app answers on | C-DC-01 | ## Deployment contract bullet 1 |
| `4173` | container-internal port | C-DC-02 | ## Deployment contract bullet 1 |
| `APP_PUBLIC_PORT` | public port the app reads from the environment | C-DC-03 | ## Deployment contract bullet 1 |
| `/api` | prefix the HTTP API is served under | C-DC-04 | ## Deployment contract bullet 2 |
| `GET /api/health` | health route | C-DC-05 | ## Deployment contract bullet 3 |
| `200` | status the health route answers | C-DC-05 | ## Deployment contract bullet 3 |
| `/app/USER_README.md` | file the login credentials are written to | C-DC-06 | ## Deployment contract bullet 5 |
| `.browser_screenshots/` | reserved empty directory at the app root | C-DC-07 | ## Deployment contract bullet 6 |
| `.downloads/` | reserved empty directory at the app root | C-DC-08 | ## Deployment contract bullet 6 |
| `0.0.0.0` | bind address | C-DC-11 | ## Deployment contract bullet 9 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the eight customer wordmark names | C-CF-22 | named in the brief as content, never as a stored record |
| the seventeen comparison entries in the Compare group | C-CF-08 | present as labels with no destination |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 5 | 7 |
| User roles | 1 | 12 |
| Core features | 32 | 73 |
| User flow | 8 | 10 |
| UI/UX notes | 8 | 19 |
| Front-end specification | 2 | 6 |
| Technical requirements | 11 | 11 |
| Data model | 4 | 12 |
| Constraints | 1 | 5 |
| Deployment contract | 11 | 13 |
