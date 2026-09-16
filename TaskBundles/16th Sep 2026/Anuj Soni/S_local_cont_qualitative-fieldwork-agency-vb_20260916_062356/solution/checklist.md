# Checklist: Qualitative Fieldwork Agency

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 323
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public editorial site for a market research agency. `src: Overview, para 1`
- [ ] `C-OV-02` `capability` The app serves a staff console behind a sign-in boundary. `src: Overview, para 2`
- [ ] `C-OV-03` `constraint` The brief form is the only public action that changes stored state. `src: Overview, para 2`
- [ ] `C-OV-04` `constraint` The app keeps an unpublished record unreadable outside the console. `src: Overview, para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` An editor signs in to the console. `src: User roles, table row 1`
- [ ] `C-RL-02` `role` An editor reads an article in any status. `src: User roles, table row 1`
- [ ] `C-RL-03` `role` An editor publishes an article. `src: User roles, table row 1`
- [ ] `C-RL-04` `role` An editor advances the stage of any opportunity. `src: User roles, table row 1`
- [ ] `C-RL-05` `role` A client signs up from the public site. `src: User roles, table row 2`
- [ ] `C-RL-06` `role` A client reads the reference of their own request. `src: User roles, table row 2`
- [ ] `C-RL-07` `role` A client cannot open a console route. `src: User roles, table row 2`
- [ ] `C-RL-08` `role` A client cannot read an unpublished article. `src: User roles, table row 2`
- [ ] `C-RL-09` `role` A client cannot read another client's request. `src: User roles, table row 2`
- [ ] `C-RL-10` `role` A visitor who is not signed in submits a brief. `src: User roles, para after the table`
- [ ] `C-RL-11` `role` The server rejects a client call to an editor endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-12` `constraint` A denied request leaves the protected state unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-13` `role` Signup creates an account holding the client role. `src: User roles, signup paragraph`
- [ ] `C-RL-14` `constraint` No route lets an account change its own role. `src: User roles, signup paragraph`
- [ ] `C-RL-15` `literal` The app seeds the editor account `editor@example.com`. `src: User roles, seeded accounts table row 1`
- [ ] `C-RL-16` `literal` The app seeds the editor account `editor2@example.com`. `src: User roles, seeded accounts table row 2`
- [ ] `C-RL-17` `literal` The app seeds the client account `client@example.com`. `src: User roles, seeded accounts table row 3`
- [ ] `C-RL-18` `literal` The app seeds the client account `client2@example.com`. `src: User roles, seeded accounts table row 4`
- [ ] `C-RL-19` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles, seeded accounts paragraph`

## C-CF Core features

- [ ] `C-CF-01` `capability` Signup with an email plus a password returns a bearer token. `src: Core features, Accounts and sessions rule 1`
- [ ] `C-CF-02` `constraint` A second signup with a stored address is rejected as invalid. `src: Core features, Accounts and sessions rule 1`
- [ ] `C-CF-03` `capability` Login with a seeded address returns a bearer token. `src: Core features, Accounts and sessions rule 2`
- [ ] `C-CF-04` `constraint` Login with a wrong password returns no token. `src: Core features, Accounts and sessions rule 2`
- [ ] `C-CF-05` `constraint` A guarded endpoint denies a call carrying no token. `src: Core features, Accounts and sessions rule 3`
- [ ] `C-CF-06` `constraint` A signup body naming a role still creates a client. `src: Core features, Accounts and sessions rule 4`
- [ ] `C-CF-07` `data` The app stores every password hashed. `src: Core features, Accounts and sessions para 1`
- [ ] `C-CF-08` `constraint` No endpoint returns a stored password hash. `src: Core features, Accounts and sessions para 1`
- [ ] `C-CF-09` `capability` The route `/methodology` lists all thirteen seeded methods. `src: Core features, The editorial estate rule 1`
- [ ] `C-CF-10` `constraint` The method index hides no method behind pagination. `src: Core features, The editorial estate rule 1`
- [ ] `C-CF-11` `capability` The route `/sectors` lists all twelve seeded sectors. `src: Core features, The editorial estate rule 1`
- [ ] `C-CF-12` `ui` Each header dropdown panel lists its full child set. `src: Core features, The editorial estate rule 1`
- [ ] `C-CF-13` `capability` A method detail route renders one stored method record. `src: Core features, The editorial estate rule 2`
- [ ] `C-CF-14` `constraint` A method slug matching no published record renders the not-found page. `src: Core features, The editorial estate rule 2`
- [ ] `C-CF-15` `capability` The route `/services` lists the nine seeded services. `src: Core features, The editorial estate rule 3`
- [ ] `C-CF-16` `constraint` The two primary services sort above the seven supporting services. `src: Core features, The editorial estate rule 3`
- [ ] `C-CF-17` `capability` The second brief stage offers the same nine service records. `src: Core features, The editorial estate rule 3`
- [ ] `C-CF-18` `capability` The route `/network` renders the seeded countries as map pins. `src: Core features, The editorial estate rule 4`
- [ ] `C-CF-19` `ui` The country rail beneath the map is a keyboard-reachable list. `src: Core features, The editorial estate rule 4`
- [ ] `C-CF-20` `ui` The country rail becomes the interface below the primary threshold. `src: Core features, The editorial estate rule 4`
- [ ] `C-CF-21` `capability` The route `/about-us` publishes the six process steps in order. `src: Core features, The editorial estate rule 5`
- [ ] `C-CF-22` `capability` The home route publishes the three stored figures. `src: Core features, The editorial estate rule 6`
- [ ] `C-CF-23` `constraint` The three published figures come from stored records rather than a live count. `src: Core features, The editorial estate rule 6`
- [ ] `C-CF-24` `constraint` Every internal link on a public route resolves to a served route. `src: Core features, The editorial estate rule 7`
- [ ] `C-CF-25` `constraint` Publishing a record whose body links to a missing path is refused. `src: Core features, The editorial estate rule 7`
- [ ] `C-CF-26` `capability` The endpoint `GET /api/articles` returns published articles newest first. `src: Core features, The article library rule 1`
- [ ] `C-CF-27` `constraint` An article in draft is absent from the article list for every caller. `src: Core features, The article library rule 1`
- [ ] `C-CF-28` `capability` The article index filters on category. `src: Core features, The article library rule 2`
- [ ] `C-CF-29` `capability` The article index filters on region. `src: Core features, The article library rule 2`
- [ ] `C-CF-30` `capability` A category selection intersects with a region selection. `src: Core features, The article library rule 2`
- [ ] `C-CF-31` `capability` The filter selection lives in the query string. `src: Core features, The article library rule 2`
- [ ] `C-CF-32` `capability` A filter option shows how many articles would remain once the option is added. `src: Core features, The article library rule 3`
- [ ] `C-CF-33` `ui` A filter option that would leave nothing is shown unavailable. `src: Core features, The article library rule 3`
- [ ] `C-CF-34` `ui` Clearing every active filter takes one action. `src: Core features, The article library rule 3`
- [ ] `C-CF-35` `ui` An empty filtered result names the active filters. `src: Core features, The article library rule 4`
- [ ] `C-CF-36` `ui` An empty filtered result keeps a visible count reading zero. `src: Core features, The article library rule 4`
- [ ] `C-CF-37` `capability` An article route renders the stored body of a published article. `src: Core features, The article library rule 5`
- [ ] `C-CF-38` `ui` An article body holds the reading measure rather than the full grid width. `src: Core features, The article library rule 5`
- [ ] `C-CF-39` `constraint` The public path of an unpublished article answers not-found for a client. `src: Core features, The article library rule 6`
- [ ] `C-CF-40` `constraint` A refused draft path reveals nothing distinguishing a draft from a missing path. `src: Core features, The article library rule 6`
- [ ] `C-CF-41` `ui` An article card is a single link. `src: Core features, The article library rule 7`
- [ ] `C-CF-42` `ui` A chip drawn on an article card carries no link of its own. `src: Core features, The article library rule 7`
- [ ] `C-CF-43` `literal` An article card carries the accessible label `Read more about` before the title. `src: Core features, The article library rule 7`
- [ ] `C-CF-44` `capability` A method route lists related articles sharing a tag. `src: Core features, The article library rule 8`
- [ ] `C-CF-45` `ui` A related block with nothing to show is omitted rather than left empty. `src: Core features, The article library rule 8`
- [ ] `C-CF-46` `capability` The route `/contact` collects who is asking. `src: Core features, The staged brief rule 1`
- [ ] `C-CF-47` `capability` The route `/contact/study` collects the shape of the study. `src: Core features, The staged brief rule 1`
- [ ] `C-CF-48` `capability` The route `/contact/question` collects the challenge in the client's own words. `src: Core features, The staged brief rule 1`
- [ ] `C-CF-49` `constraint` The server rejects a brief naming a sector the site does not publish. `src: Core features, The staged brief rule 2`
- [ ] `C-CF-50` `constraint` The server rejects a brief naming a market that is not a seeded country. `src: Core features, The staged brief rule 2`
- [ ] `C-CF-51` `constraint` The server rejects a brief naming a method outside the seeded thirteen. `src: Core features, The staged brief rule 2`
- [ ] `C-CF-52` `constraint` The server rejects a brief naming a service outside the seeded nine. `src: Core features, The staged brief rule 2`
- [ ] `C-CF-53` `constraint` The server rejects a challenge shorter than twenty characters. `src: Core features, The staged brief rule 2`
- [ ] `C-CF-54` `constraint` A rejected brief names the field that failed. `src: Core features, The staged brief rule 2`
- [ ] `C-CF-55` `constraint` A rejected brief writes no stored request. `src: Core features, The staged brief rule 2`
- [ ] `C-CF-56` `constraint` A brief naming `Other` without the companion field is rejected as invalid. `src: Core features, The staged brief rule 3`
- [ ] `C-CF-57` `capability` An accepted brief returns a reference beginning `MF-`. `src: Core features, The staged brief rule 4`
- [ ] `C-CF-58` `ui` The route `/contact/sent` shows the reference of the accepted brief. `src: Core features, The staged brief rule 4`
- [ ] `C-CF-59` `constraint` A same-day repeat of one brief opens no second opportunity. `src: Core features, The staged brief rule 5`
- [ ] `C-CF-60` `capability` A same-day repeat of one brief returns the first reference. `src: Core features, The staged brief rule 5`
- [ ] `C-CF-61` `constraint` A same-day repeat of one brief leaves exactly one stored request. `src: Core features, The staged brief rule 5`
- [ ] `C-CF-62` `capability` A brief sent by a signed-in client appears at `/account/requests`. `src: Core features, The staged brief rule 6`
- [ ] `C-CF-63` `constraint` A brief sent by a visitor who is not signed in belongs to no account. `src: Core features, The staged brief rule 6`
- [ ] `C-CF-64` `constraint` The endpoint `GET /api/requests` returns only the caller's own requests. `src: Core features, The staged brief rule 7`
- [ ] `C-CF-65` `constraint` A client asking for another client's reference is answered as not found. `src: Core features, The staged brief rule 7`
- [ ] `C-CF-66` `literal` The brief form carries the unattended decoy field `company_website`. `src: Core features, Automated submission defence rule 1`
- [ ] `C-CF-67` `constraint` A submission arriving with the decoy field filled stores no request. `src: Core features, Automated submission defence rule 1`
- [ ] `C-CF-68` `constraint` A submitter posting repeatedly is refused after the third attempt in one minute. `src: Core features, Automated submission defence rule 2`
- [ ] `C-CF-69` `constraint` A refused submission discloses no refusing rule. `src: Core features, Automated submission defence rule 2`
- [ ] `C-CF-70` `capability` An accepted brief opens exactly one opportunity at stage `Brief`. `src: Core features, The opportunity board rule 1`
- [ ] `C-CF-71` `capability` An opportunity carries the reference of its own brief. `src: Core features, The opportunity board rule 1`
- [ ] `C-CF-72` `capability` A brief whose sector names an owner routes the opportunity to that owner. `src: Core features, The opportunity board rule 2`
- [ ] `C-CF-73` `literal` An owned opportunity stores the routing reason `sector_owner`. `src: Core features, The opportunity board rule 2`
- [ ] `C-CF-74` `capability` A brief whose sector names no owner leaves the opportunity unowned. `src: Core features, The opportunity board rule 2`
- [ ] `C-CF-75` `literal` An unowned opportunity stores the routing reason `no_sector_owner`. `src: Core features, The opportunity board rule 2`
- [ ] `C-CF-76` `constraint` An unowned opportunity stays visible to every editor. `src: Core features, The opportunity board rule 2`
- [ ] `C-CF-77` `capability` An opportunity copies its sensitivity class from the sector record. `src: Core features, The opportunity board rule 3`
- [ ] `C-CF-78` `literal` A brief naming `pharmaceutical` opens an opportunity at `elevated`. `src: Core features, The opportunity board rule 3`
- [ ] `C-CF-79` `literal` A brief naming an ordinary sector opens an opportunity at `standard`. `src: Core features, The opportunity board rule 3`
- [ ] `C-CF-80` `constraint` Sensitivity is never inferred from the wording of the challenge. `src: Core features, The opportunity board rule 3`
- [ ] `C-CF-81` `capability` An editor advances an opportunity one stage forward. `src: Core features, The opportunity board rule 4`
- [ ] `C-CF-82` `constraint` A stage change skipping a stage is rejected as invalid. `src: Core features, The opportunity board rule 4`
- [ ] `C-CF-83` `constraint` A stage change moving backwards is rejected as invalid. `src: Core features, The opportunity board rule 4`
- [ ] `C-CF-84` `constraint` A rejected stage change leaves the stored stage unchanged. `src: Core features, The opportunity board rule 4`
- [ ] `C-CF-85` `capability` An editor adds a note to an opportunity from the board. `src: Core features, The opportunity board rule 5`
- [ ] `C-CF-86` `data` A stored note records the address of the editor who wrote the note. `src: Core features, The opportunity board rule 5`
- [ ] `C-CF-87` `constraint` A stored note is never edited after writing. `src: Core features, The opportunity board rule 5`
- [ ] `C-CF-88` `capability` The board orders cards by arrival with the oldest brief first. `src: Core features, The opportunity board rule 6`
- [ ] `C-CF-89` `ui` An opportunity card shows the elapsed time since its brief arrived. `src: Core features, The opportunity board rule 6`
- [ ] `C-CF-90` `constraint` A client session is refused at every console endpoint. `src: Core features, The opportunity board rule 7`
- [ ] `C-CF-91` `capability` An editor creates an article in the `draft` status. `src: Core features, The editorial console rule 1`
- [ ] `C-CF-92` `constraint` Publishing an article carrying no search description is refused. `src: Core features, The editorial console rule 2`
- [ ] `C-CF-93` `constraint` Publishing an article carrying no body is refused. `src: Core features, The editorial console rule 2`
- [ ] `C-CF-94` `constraint` Publishing a case study carrying no client approval reference is refused. `src: Core features, The editorial console rule 2`
- [ ] `C-CF-95` `capability` A refused publish states the rule behind the refusal. `src: Core features, The editorial console rule 2`
- [ ] `C-CF-96` `constraint` A refused publish leaves the article in the `draft` status. `src: Core features, The editorial console rule 2`
- [ ] `C-CF-97` `literal` The seeded case study carries the client approval reference `CA-2026-014`. `src: Core features, The editorial console rule 3`
- [ ] `C-CF-98` `capability` Publishing sets the first-published moment once. `src: Core features, The editorial console rule 4`
- [ ] `C-CF-99` `constraint` A later edit never rewrites the first-published moment. `src: Core features, The editorial console rule 4`
- [ ] `C-CF-100` `capability` Unpublishing returns an article to the `draft` status. `src: Core features, The editorial console rule 5`
- [ ] `C-CF-101` `constraint` An unpublished article's public path answers not-found from that moment. `src: Core features, The editorial console rule 5`
- [ ] `C-CF-102` `constraint` A slug already taken by another article is refused. `src: Core features, The editorial console rule 6`
- [ ] `C-CF-103` `capability` An editor uploads a cover through `POST /api/articles/{slug}/cover`. `src: Core features, Images and the object store rule 1`
- [ ] `C-CF-104` `constraint` Uploaded image bytes live in the bucket named by `STORAGE_BUCKET`. `src: Core features, Images and the object store rule 1`
- [ ] `C-CF-105` `constraint` Uploaded image bytes never live on the app's own filesystem. `src: Core features, Images and the object store rule 1`
- [ ] `C-CF-106` `constraint` Uploaded image bytes never live inside a database column. `src: Core features, Images and the object store rule 1`
- [ ] `C-CF-107` `literal` A stored object key follows `articles/{article_id}/{sha256_of_bytes}.{ext}`. `src: Core features, Images and the object store rule 2`
- [ ] `C-CF-108` `constraint` The same bytes uploaded twice to one article leave one stored object. `src: Core features, Images and the object store rule 2`
- [ ] `C-CF-109` `capability` The app serves cover bytes at `GET /api/articles/{slug}/cover`. `src: Core features, Images and the object store rule 3`
- [ ] `C-CF-110` `constraint` A published article's cover is readable by any caller. `src: Core features, Images and the object store rule 3`
- [ ] `C-CF-111` `constraint` An unpublished article's cover is readable by an editor only. `src: Core features, Images and the object store rule 3`
- [ ] `C-CF-112` `constraint` A client asking for an unpublished cover is answered as not found. `src: Core features, Images and the object store rule 3`
- [ ] `C-CF-113` `constraint` An upload carrying neither alternative text nor a decorative marker is rejected. `src: Core features, Images and the object store rule 4`
- [ ] `C-CF-114` `constraint` An upload sent from a client session writes no object. `src: Core features, Images and the object store rule 5`
- [ ] `C-CF-115` `ui` A first-time visitor is asked once about non-essential cookies. `src: Core features, The cookie choice rule 1`
- [ ] `C-CF-116` `constraint` The essential cookie category stays locked on. `src: Core features, The cookie choice rule 1`
- [ ] `C-CF-117` `capability` A stored cookie decision survives a reload. `src: Core features, The cookie choice rule 2`
- [ ] `C-CF-118` `literal` Every route's footer carries the `Cookie Preferences` control. `src: Core features, The cookie choice rule 3`
- [ ] `C-CF-119` `constraint` An unknown address answers a true not-found status. `src: Core features, When a page does not exist rule 1`
- [ ] `C-CF-120` `ui` The not-found page states plainly that the page does not exist. `src: Core features, When a page does not exist rule 2`
- [ ] `C-CF-121` `ui` The not-found page offers a way back to `/articles`. `src: Core features, When a page does not exist rule 2`
- [ ] `C-CF-122` `constraint` The not-found page carries no site search. `src: Core features, When a page does not exist rule 3`

## C-UF User flow

- [ ] `C-UF-01` `capability` The app serves the twenty-two routes named in the route table. `src: User flow, route table`
- [ ] `C-UF-02` `constraint` An unauthenticated request for `/console` lands on `/login`. `src: User flow, entry and redirects`
- [ ] `C-UF-03` `capability` Signing in returns the visitor to the route that was asked for. `src: User flow, entry and redirects`
- [ ] `C-UF-04` `constraint` A client session asking for a console route is refused rather than redirected. `src: User flow, entry and redirects`
- [ ] `C-UF-05` `capability` An editor signing in lands on `/console`. `src: User flow, entry and redirects`
- [ ] `C-UF-06` `capability` A client signing in lands on `/account/requests`. `src: User flow, entry and redirects`
- [ ] `C-UF-07` `capability` Signing out returns the visitor to `/`. `src: User flow, entry and redirects`
- [ ] `C-UF-08` `constraint` A signed-out session opens neither guarded surface. `src: User flow, entry and redirects`
- [ ] `C-UF-09` `capability` An expired token returns the visitor to `/login`. `src: User flow, entry and redirects`
- [ ] `C-UF-10` `ui` A form keeps what the visitor typed when a submission fails. `src: User flow, states`
- [ ] `C-UF-11` `ui` Every list surface carries an empty state. `src: User flow, states`
- [ ] `C-UF-12` `ui` In-place content settles as a skeleton at the destination shape. `src: User flow, states`
- [ ] `C-UF-13` `ui` The board with nothing open names the editorial list as the next surface. `src: User flow, states`
- [ ] `C-UF-14` `ui` A refused stage change returns the row to its previous stage. `src: User flow, states`
- [ ] `C-UF-15` `ui` A refused stage change states beside the row what failed. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The public site reads as editorial with the subject seen first. `src: UI/UX notes, register paragraph`
- [ ] `C-UX-02` `ui` The console reads as operational with no editorial composition. `src: UI/UX notes, register paragraph`
- [ ] `C-UX-03` `ui` The page ground is a near-white warm neutral nearer paper than white. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-04` `ui` Every glyph is a deep warm neutral rather than true black. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-05` `ui` The primary accent is a light soft green grounding the home hero. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-06` `ui` Each secondary accent owns one thing on the site. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-07` `ui` A surface wearing one accent wears no second accent. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-08` `ui` The interface is set in the family `Space Grotesk`. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-09` `ui` Every type size interpolates between a narrow value plus a wide value. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-10` `ui` Figures line up on tabular numerals wherever counts stack. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-11` `ui` Reveals move with a considered ease carrying a long settle. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-12` `ui` Anything a pointer touches overshoots its end value before settling. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-13` `ui` A promise tile reveals by growing its ground out from nothing. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-14` `ui` Looping movement pauses when its container leaves the screen. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-15` `ui` A reduced-motion preference resolves every entrance to its end state. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-16` `ui` A reduced-motion preference stops all looping movement. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-17` `ui` The public site keeps one dominant subject per view. `src: UI/UX notes, density paragraph`
- [ ] `C-UX-18` `ui` The console navigation is a persistent sidebar. `src: UI/UX notes, density paragraph`
- [ ] `C-UX-19` `ui` The console board is a card grid of open opportunities. `src: UI/UX notes, density paragraph`
- [ ] `C-UX-20` `ui` A console change lands in the list before the store confirms. `src: UI/UX notes, density paragraph`
- [ ] `C-UX-21` `ui` Every control carries a resting state plus a pointed-at state. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-22` `ui` An unavailable control is never signalled by colour alone. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-23` `ui` Escape closes any open panel. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-24` `ui` Body text reaches a contrast ratio of at least `4.5:1` against its ground. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-25` `ui` Interface components reach a contrast ratio of at least `3:1`. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-26` `ui` Every route carries a skip link as its first focusable element. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-27` `ui` Every route carries exactly one level-one heading. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-28` `ui` Keyboard navigation reaches every control with a visible focus ring. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-29` `ui` A heading split into words also exists once as a single string. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-30` `ui` Every content image carries alternative text. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-31` `ui` The layout reflows at a narrow viewport rather than hiding content. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-32` `ui` The article grid runs three across above the primary breakpoint. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-33` `ui` The navigation collapses into a slide-in panel below the primary breakpoint. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-34` `ui` No route scrolls sideways at the narrowest supported viewport. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-35` `ui` The product commits to light mode throughout. `src: UI/UX notes, mode paragraph`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Every route is a complete document rendered on the server. `src: Technical requirements, para 1`
- [ ] `C-TR-02` `contract` Every route works with scripting switched off. `src: Technical requirements, para 1`
- [ ] `C-TR-03` `contract` The HTTP API is served under the `/api` prefix on the app's own origin. `src: Technical requirements, para 1`
- [ ] `C-TR-04` `contract` The app reads its database location from `DATABASE_URL`. `src: Technical requirements, para 1`
- [ ] `C-TR-05` `contract` The app reads its object store location from `STORAGE_ENDPOINT`. `src: Technical requirements, para 1`
- [ ] `C-TR-06` `contract` The app reads its bucket name from `STORAGE_BUCKET`. `src: Technical requirements, para 1`
- [ ] `C-TR-07` `contract` The endpoint `GET /api/health` returns `200` once the app is ready. `src: Technical requirements, para 1`
- [ ] `C-TR-08` `constraint` The app introduces no second database beyond PostgreSQL. `src: Technical requirements, para 2`
- [ ] `C-TR-09` `constraint` The app introduces no second object store beyond MinIO. `src: Technical requirements, para 2`
- [ ] `C-TR-10` `constraint` The app starts no copy of PostgreSQL. `src: Technical requirements, para 3`
- [ ] `C-TR-11` `capability` Every public route serves its own title. `src: Technical requirements, para 4`
- [ ] `C-TR-12` `capability` Every public route serves its own meta description. `src: Technical requirements, para 4`
- [ ] `C-TR-13` `constraint` No two public routes share a title. `src: Technical requirements, para 4`
- [ ] `C-TR-14` `literal` A route title ends with the separator before `Meridian Field`. `src: Technical requirements, para 4`
- [ ] `C-TR-15` `constraint` Nothing the browser downloads carries a credential. `src: Technical requirements, para 4`
- [ ] `C-TR-16` `contract` Every timestamp is sent as a UTC string ending in `Z`. `src: Technical requirements, para 5`

## C-DM Data model

- [ ] `C-DM-01` `data` The store holds thirteen tables. `src: Data model, para 1`
- [ ] `C-DM-02` `data` Every stored timestamp is UTC. `src: Data model, para 1`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model, password paragraph`
- [ ] `C-DM-04` `contract` The seeded logins are written into `/app/USER_README.md`. `src: Data model, password paragraph`
- [ ] `C-DM-05` `data` An account row carries a role of `editor` or `client`. `src: Data model, account paragraph`
- [ ] `C-DM-06` `constraint` A second account row for a stored address is refused. `src: Data model, account paragraph`
- [ ] `C-DM-07` `data` The store holds thirteen method rows. `src: Data model, method paragraph`
- [ ] `C-DM-08` `data` The store holds twelve sector rows. `src: Data model, sector paragraph`
- [ ] `C-DM-09` `data` A sector row carries a sensitivity class of `standard` or `elevated`. `src: Data model, sector paragraph`
- [ ] `C-DM-10` `data` A sector row carries an owner address that may be empty. `src: Data model, sector paragraph`
- [ ] `C-DM-11` `data` The store holds nine service rows ranked by kind. `src: Data model, service paragraph`
- [ ] `C-DM-12` `data` The store holds seven region rows. `src: Data model, region paragraph`
- [ ] `C-DM-13` `data` A country row carries two normalised map coordinates. `src: Data model, country paragraph`
- [ ] `C-DM-14` `data` The store holds five category rows. `src: Data model, category paragraph`
- [ ] `C-DM-15` `data` An article row carries a status from the four named values. `src: Data model, article paragraph`
- [ ] `C-DM-16` `data` An article row carries exactly one region. `src: Data model, article paragraph`
- [ ] `C-DM-17` `data` An article carries between one category plus three categories. `src: Data model, article category paragraph`
- [ ] `C-DM-18` `data` A brief row carries a dedupe key derived from the lowercased address. `src: Data model, brief paragraph`
- [ ] `C-DM-19` `constraint` The store holds one brief row per dedupe key. `src: Data model, brief paragraph`
- [ ] `C-DM-20` `data` An opportunity row carries a stage from the six published names. `src: Data model, opportunity paragraph`
- [ ] `C-DM-21` `constraint` The store holds exactly one opportunity per brief. `src: Data model, opportunity paragraph`
- [ ] `C-DM-22` `data` A note row records its author address. `src: Data model, opportunity note paragraph`
- [ ] `C-DM-23` `data` An asset row carries a unique object key. `src: Data model, content asset paragraph`
- [ ] `C-DM-24` `data` A site setting row carries the site name `Meridian Field`. `src: Data model, site setting paragraph`
- [ ] `C-DM-25` `constraint` The filter counts are derived on read rather than stored. `src: Data model, derived paragraph`
- [ ] `C-DM-26` `literal` The seeded sectors carry `beauty-cosmetics` at `elevated`. `src: Data model, seed data paragraph`
- [ ] `C-DM-27` `literal` The seeded regions carry `Worldwide` without a band. `src: Data model, seed data paragraph`
- [ ] `C-DM-28` `data` The store seeds twenty-four countries with twenty-two featured. `src: Data model, seed data paragraph`
- [ ] `C-DM-29` `data` The store seeds eleven attribution options with stable keys. `src: Data model, seed data paragraph`
- [ ] `C-DM-30` `data` The store seeds six published articles. `src: Data model, seeded article table`
- [ ] `C-DM-31` `literal` The store seeds the draft article `field-notes-from-lagos`. `src: Data model, seeded article table row 7`
- [ ] `C-DM-32` `literal` The store seeds the case study `five-markets-one-brief`. `src: Data model, seeded article table row 1`
- [ ] `C-DM-33` `literal` The seeded opportunity for `client@example.com` carries the reference `MF-2026-00001`. `src: Data model, seeded brief paragraph`
- [ ] `C-DM-34` `literal` The seeded opportunity for `client2@example.com` carries the reference `MF-2026-00002`. `src: Data model, seeded brief paragraph`
- [ ] `C-DM-35` `data` The store seeds two offices carrying their time zones. `src: Data model, offices paragraph`
- [ ] `C-DM-36` `constraint` Restarting the app duplicates no seeded row. `src: Data model, seeding paragraph`
- [ ] `C-DM-37` `constraint` Restarting the app writes no second copy of a seeded object. `src: Data model, seeding paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Body copy is set at `1rem` on a narrow screen. `src: Front-end specification, type scale table`
- [ ] `C-FE-02` `ui` Body copy is set at `1.0625rem` on a wide screen. `src: Front-end specification, type scale table`
- [ ] `C-FE-03` `ui` The hero display runs up to `10.875rem` on a wide screen. `src: Front-end specification, type scale table`
- [ ] `C-FE-04` `ui` Long-form copy holds a reading measure of `48rem`. `src: Front-end specification, type scale paragraph`
- [ ] `C-FE-05` `ui` The layout resolves on a sixteen-column grid. `src: Front-end specification, shape paragraph`
- [ ] `C-FE-06` `ui` Every spacing value is a multiple of one base unit. `src: Front-end specification, shape paragraph`
- [ ] `C-FE-07` `ui` The header is a floating capsule clear of all four edges. `src: Front-end specification, header paragraph`
- [ ] `C-FE-08` `ui` The header keeps the quote action in a capsule of its own. `src: Front-end specification, header paragraph`
- [ ] `C-FE-09` `ui` The header holds one height at every scroll position. `src: Front-end specification, header paragraph`
- [ ] `C-FE-10` `ui` A dropdown panel closes on the Escape key. `src: Front-end specification, panels paragraph`
- [ ] `C-FE-11` `ui` A closed dropdown panel is inert to assistive technology. `src: Front-end specification, panels paragraph`
- [ ] `C-FE-12` `ui` A button carries a circular icon disc at one end. `src: Front-end specification, button paragraph`
- [ ] `C-FE-13` `ui` Pointing at a button swaps its resting disc for a second disc. `src: Front-end specification, button paragraph`
- [ ] `C-FE-14` `ui` The home route stacks nine sections in the stated order. `src: Front-end specification, home route paragraph`
- [ ] `C-FE-15` `ui` Each promise tile links to one named route. `src: Front-end specification, home route paragraph`
- [ ] `C-FE-16` `ui` The three figures arrive one after another a beat apart. `src: Front-end specification, home route paragraph`
- [ ] `C-FE-17` `ui` A method route is composed from an ordered list of content blocks. `src: Front-end specification, method routes paragraph`
- [ ] `C-FE-18` `ui` An accordion question carries its own expanded state. `src: Front-end specification, method routes paragraph`
- [ ] `C-FE-19` `ui` Opening one accordion question closes no other question. `src: Front-end specification, method routes paragraph`
- [ ] `C-FE-20` `ui` The map is shown through a circular window. `src: Front-end specification, network route paragraph`
- [ ] `C-FE-21` `ui` A map pin grows to full size on hover or on focus. `src: Front-end specification, network route paragraph`
- [ ] `C-FE-22` `ui` The value carousel controls move the track by one card. `src: Front-end specification, network route paragraph`
- [ ] `C-FE-23` `ui` The section navigation marks the section being read. `src: Front-end specification, about route paragraph`
- [ ] `C-FE-24` `ui` The comparison block becomes two sequential lists below the primary threshold. `src: Front-end specification, about route paragraph`
- [ ] `C-FE-25` `ui` The filter bar floats near the foot of the viewport. `src: Front-end specification, article index paragraph`
- [ ] `C-FE-26` `ui` The filter panel traps focus at narrow widths. `src: Front-end specification, article index paragraph`
- [ ] `C-FE-27` `ui` A card image settles toward true size on hover. `src: Front-end specification, article index paragraph`
- [ ] `C-FE-28` `ui` Each brief stage states which stage the visitor is on. `src: Front-end specification, brief form paragraph`
- [ ] `C-FE-29` `ui` Every form control carries a persistent visible label. `src: Front-end specification, brief form paragraph`
- [ ] `C-FE-30` `ui` A field is checked once the visitor leaves the field. `src: Front-end specification, brief form paragraph`
- [ ] `C-FE-31` `ui` The submit control is never disabled. `src: Front-end specification, brief form paragraph`
- [ ] `C-FE-32` `ui` Submitting with errors moves focus to the first field in error. `src: Front-end specification, brief form paragraph`
- [ ] `C-FE-33` `ui` The decoy field is reachable by nothing a person uses. `src: Front-end specification, brief form paragraph`
- [ ] `C-FE-34` `ui` The first document of a session paints behind a cover. `src: Front-end specification, first load paragraph`
- [ ] `C-FE-35` `ui` The cover lifts when loading runs long. `src: Front-end specification, first load paragraph`
- [ ] `C-FE-36` `ui` A route change replaces the document title with the new route's own. `src: Front-end specification, first load paragraph`
- [ ] `C-FE-37` `ui` A route change moves focus to the new document's first heading. `src: Front-end specification, first load paragraph`
- [ ] `C-FE-38` `ui` A reveal fires once on arrival rather than reversing on scroll up. `src: Front-end specification, scroll paragraph`
- [ ] `C-FE-39` `ui` An in-page anchor lands clear of the floating header. `src: Front-end specification, scroll paragraph`
- [ ] `C-FE-40` `ui` The focus ring is shown for keyboard focus. `src: Front-end specification, focus paragraph`
- [ ] `C-FE-41` `ui` The focus ring is suppressed for pointer focus. `src: Front-end specification, focus paragraph`
- [ ] `C-FE-42` `ui` A focused button shows the ring rather than swapping its disc. `src: Front-end specification, focus paragraph`
- [ ] `C-FE-43` `ui` The console sidebar marks the current surface by more than colour. `src: Front-end specification, console paragraph`
- [ ] `C-FE-44` `ui` An opportunity card leads with the reference on its first line. `src: Front-end specification, console paragraph`
- [ ] `C-FE-45` `ui` The editorial list is a table carrying row headers plus column headers. `src: Front-end specification, console paragraph`
- [ ] `C-FE-46` `ui` The footer carries two office blocks showing local opening state. `src: Front-end specification, footer paragraph`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app carries no second tenant. `src: Constraints, bullet 1`
- [ ] `C-CN-02` `constraint` The app builds no questionnaire engine. `src: Constraints, bullet 2`
- [ ] `C-CN-03` `constraint` The app stores no session recording. `src: Constraints, bullet 2`
- [ ] `C-CN-04` `constraint` The app holds no participant record. `src: Constraints, bullet 2`
- [ ] `C-CN-05` `constraint` The app takes no payment. `src: Constraints, bullet 3`
- [ ] `C-CN-06` `constraint` The app sends no email. `src: Constraints, bullet 4`
- [ ] `C-CN-07` `constraint` The app calls no third-party service at runtime. `src: Constraints, bullet 5`
- [ ] `C-CN-08` `constraint` The app offers no site search. `src: Constraints, bullet 6`
- [ ] `C-CN-09` `constraint` The app carries no comment thread. `src: Constraints, bullet 6`
- [ ] `C-CN-10` `constraint` The app serves one language only. `src: Constraints, bullet 7`
- [ ] `C-CN-11` `constraint` A brief carries a budget band rather than a price. `src: Constraints, bullet 7`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-02` `contract` The app listens on the container-internal port `4173`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-03` `contract` The app reads its public port from `APP_PUBLIC_PORT`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-04` `contract` The HTTP API is served under the `/api` prefix. `src: Deployment contract, bullet 2`
- [ ] `C-DC-05` `contract` The endpoint `GET /api/health` returns `200`. `src: Deployment contract, bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract, bullet 4`
- [ ] `C-DC-07` `contract` The app writes credentials into `/app/USER_README.md`. `src: Deployment contract, bullet 5`
- [ ] `C-DC-08` `contract` The app root carries an empty `.browser_screenshots/` directory. `src: Deployment contract, bullet 6`
- [ ] `C-DC-09` `contract` The app root carries an empty `.downloads/` directory. `src: Deployment contract, bullet 6`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends. `src: Deployment contract, bullet 8`
- [ ] `C-DC-11` `contract` The server binds `0.0.0.0`. `src: Deployment contract, bullet 9`
- [ ] `C-DC-12` `contract` The app starts no copy of a backing service. `src: Deployment contract, bullet 10`
- [ ] `C-DC-13` `contract` The app uses no edge function. `src: Deployment contract, bullet 11`
- [ ] `C-DC-14` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-15` `contract` An invalid call is rejected as a client error rather than a server error. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-16` `contract` A rejected call carries a message naming the reason. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-17` `contract` Bearer auth is required on every endpoint outside the public set. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-18` `constraint` An uploaded image exists in MinIO rather than in a stand-in the app controls. `src: Deployment contract, no mocks paragraph`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | seeded password for every account | C-RL-19 | User roles, seeded accounts paragraph |
| `editor@example.com` | seeded editor account | C-RL-15 | User roles, seeded accounts table row 1 |
| `editor2@example.com` | second seeded editor account | C-RL-16 | User roles, seeded accounts table row 2 |
| `client@example.com` | seeded client account | C-RL-17 | User roles, seeded accounts table row 3 |
| `client2@example.com` | second seeded client account | C-RL-18 | User roles, seeded accounts table row 4 |
| `Read more about` | accessible label prefix on an article card | C-CF-43 | Core features, The article library rule 7 |
| `MF-` | prefix of every request reference | C-CF-57 | Core features, The staged brief rule 4 |
| `company_website` | the unattended decoy field on the brief form | C-CF-66 | Core features, Automated submission defence rule 1 |
| `sector_owner` | routing reason stored for an owned opportunity | C-CF-73 | Core features, The opportunity board rule 2 |
| `no_sector_owner` | routing reason stored for an unowned opportunity | C-CF-75 | Core features, The opportunity board rule 2 |
| `pharmaceutical` | sector slug carrying elevated sensitivity | C-CF-78 | Core features, The opportunity board rule 3 |
| `elevated` | sensitivity class of a pharmaceutical opportunity | C-CF-78 | Core features, The opportunity board rule 3 |
| `standard` | sensitivity class of an ordinary opportunity | C-CF-79 | Core features, The opportunity board rule 3 |
| `Brief` | first stage of every opportunity | C-CF-70 | Core features, The opportunity board rule 1 |
| `draft` | status an article is created in | C-CF-91 | Core features, The editorial console rule 1 |
| `CA-2026-014` | client approval reference on the seeded case study | C-CF-97 | Core features, The editorial console rule 3 |
| `POST /api/articles/{slug}/cover` | cover upload endpoint | C-CF-103 | Core features, Images and the object store rule 1 |
| `GET /api/articles/{slug}/cover` | cover read endpoint | C-CF-109 | Core features, Images and the object store rule 3 |
| `STORAGE_BUCKET` | environment variable naming the bucket | C-CF-104 | Core features, Images and the object store rule 1 |
| `articles/{article_id}/{sha256_of_bytes}.{ext}` | object key scheme | C-CF-107 | Core features, Images and the object store rule 2 |
| `Cookie Preferences` | the footer control that reopens the consent panel | C-CF-118 | Core features, The cookie choice rule 3 |
| `/articles` | the article index route | C-CF-121 | Core features, When a page does not exist rule 2 |
| `4.5:1` | minimum contrast ratio for body text | C-UX-24 | UI/UX notes, accessibility paragraph |
| `3:1` | minimum contrast ratio for interface components | C-UX-25 | UI/UX notes, accessibility paragraph |
| `Space Grotesk` | the one type family on the site | C-UX-08 | UI/UX notes, type paragraph |
| `1rem` | body copy size on a narrow screen | C-FE-01 | Front-end specification, type scale table |
| `1.0625rem` | body copy size on a wide screen | C-FE-02 | Front-end specification, type scale table |
| `10.875rem` | hero display size on a wide screen | C-FE-03 | Front-end specification, type scale table |
| `48rem` | reading measure for long-form copy | C-FE-04 | Front-end specification, type scale paragraph |
| `DATABASE_URL` | environment variable naming the store | C-TR-04 | Technical requirements, para 1 |
| `STORAGE_ENDPOINT` | environment variable naming the object store | C-TR-05 | Technical requirements, para 1 |
| `GET /api/health` | health route | C-TR-07 | Technical requirements, para 1 |
| `200` | status the health route returns | C-TR-07 | Technical requirements, para 1 |
| `Meridian Field` | the site name every route title ends with | C-TR-14 | Technical requirements, para 4 |
| `Z` | suffix on every emitted timestamp | C-TR-16 | Technical requirements, para 5 |
| `beauty-cosmetics` | the second sector slug carrying elevated sensitivity | C-DM-26 | Data model, seed data paragraph |
| `Worldwide` | the region seeded without a band | C-DM-27 | Data model, seed data paragraph |
| `field-notes-from-lagos` | slug of the seeded draft article | C-DM-31 | Data model, seeded article table row 7 |
| `five-markets-one-brief` | slug of the seeded case study | C-DM-32 | Data model, seeded article table row 1 |
| `MF-2026-00001` | reference of the first seeded opportunity | C-DM-33 | Data model, seeded brief paragraph |
| `MF-2026-00002` | reference of the second seeded opportunity | C-DM-34 | Data model, seeded brief paragraph |
| `/app/USER_README.md` | file carrying the seeded logins | C-DM-04 | Data model, password paragraph |
| `APP_PUBLIC_URL` | environment variable naming the public origin | C-DC-01 | Deployment contract, bullet 1 |
| `4173` | container-internal port | C-DC-02 | Deployment contract, bullet 1 |
| `APP_PUBLIC_PORT` | environment variable naming the public port | C-DC-03 | Deployment contract, bullet 1 |
| `/api` | prefix the HTTP API is served under | C-DC-04 | Deployment contract, bullet 2 |
| `.browser_screenshots/` | reserved empty directory at the app root | C-DC-08 | Deployment contract, bullet 6 |
| `.downloads/` | reserved empty directory at the app root | C-DC-09 | Deployment contract, bullet 6 |
| `0.0.0.0` | address the server binds | C-DC-11 | Deployment contract, bullet 9 |
| `Other` | attribution option requiring a companion field | C-CF-56 | Core features, The staged brief rule 3 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the budget band a brief carries | C-CN-11 | named as a field with no enumerated set of bands |
| the sample size per market | C-CF-47 | collected at the second stage with no stated bound |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 4 |
| User roles | 2 | 19 |
| Core features | 21 | 122 |
| User flow | 6 | 15 |
| UI/UX notes | 9 | 35 |
| Technical requirements | 4 | 16 |
| Data model | 4 | 37 |
| Front-end specification | 9 | 46 |
| Constraints | 1 | 11 |
| Deployment contract | 9 | 18 |
