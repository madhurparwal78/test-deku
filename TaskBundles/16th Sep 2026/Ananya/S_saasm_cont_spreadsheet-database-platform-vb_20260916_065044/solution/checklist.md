# Checklist: Sheaf

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, technical, datamodel, constraints, deployment, definition of done
Sections absent: buildplan
Items: 308
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a marketing site for a spreadsheet product. `src: Overview para 1`
- [ ] `C-OV-02` `constraint` The app holds no product surface of its own. `src: Overview para 2`
- [ ] `C-OV-03` `constraint` The app never renders a signed in product state. `src: Overview para 2`
- [ ] `C-OV-04` `literal` The app sends every sign in link to `https://app.sheaf.example`. `src: Overview para 2`
- [ ] `C-OV-05` `capability` The app links out to a documentation origin. `src: Overview para 3`
- [ ] `C-OV-06` `capability` The app links out to a community forum origin. `src: Overview para 3`
- [ ] `C-OV-07` `capability` The app links out to a public source repository. `src: Overview para 3`
- [ ] `C-OV-08` `capability` The app carries one sector route for each named sector. `src: Overview para 3`
- [ ] `C-OV-09` `capability` The app carries one comparison route for each competing product. `src: Overview para 3`
- [ ] `C-OV-10` `capability` The app carries company routes for about, our team, partners, work with us, contact, trademark. `src: Overview para 3`
- [ ] `C-OV-11` `capability` The app lets a marketing editor add a sector route with no deploy. `src: Overview para 4`
- [ ] `C-OV-12` `constraint` The app offers no comment feature. `src: Overview para 5`
- [ ] `C-OV-13` `constraint` The app offers no like feature. `src: Overview para 5`
- [ ] `C-OV-14` `constraint` The app offers no messaging feature. `src: Overview para 5`
- [ ] `C-OV-15` `constraint` The app takes no money for a trial. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed out visitor reads every `published` route. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A signed out visitor is denied every `draft` route. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A signed out visitor is denied the authoring console. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A reader reads the trial belonging to that reader. `src: User roles table row 2`
- [ ] `C-RL-05` `role` A reader is denied the creation of a route. `src: User roles table row 2`
- [ ] `C-RL-06` `role` A reader is denied the publishing of a route. `src: User roles table row 2`
- [ ] `C-RL-07` `role` A reader is denied the upload of an image. `src: User roles table row 2`
- [ ] `C-RL-08` `role` A reader is denied the trial of another reader. `src: User roles table row 2`
- [ ] `C-RL-09` `role` A reader is denied the trial signup list. `src: User roles table row 2`
- [ ] `C-RL-10` `role` An author creates a route. `src: User roles table row 3`
- [ ] `C-RL-11` `role` An author publishes a route. `src: User roles table row 3`
- [ ] `C-RL-12` `role` An author unpublishes a route. `src: User roles table row 3`
- [ ] `C-RL-13` `role` An author uploads an image. `src: User roles table row 3`
- [ ] `C-RL-14` `role` An author reads the trial signup list. `src: User roles table row 3`
- [ ] `C-RL-15` `role` The server rejects a reader request to an author only endpoint. `src: User roles para 2`
- [ ] `C-RL-16` `role` A rejected reader request leaves the protected state unchanged. `src: User roles para 2`
- [ ] `C-RL-17` `role` A `draft` route requested with no session is answered as not found. `src: User roles para 2`
- [ ] `C-RL-18` `capability` The app lets anyone create a `reader` account from the signup form. `src: User roles para 3`
- [ ] `C-RL-19` `literal` The app seeds an author account at `author@example.com`. `src: User roles table row 5`
- [ ] `C-RL-20` `literal` The app seeds a second author account at `author2@example.com`. `src: User roles table row 6`
- [ ] `C-RL-21` `literal` The app seeds a reader account at `reader@example.com`. `src: User roles table row 7`
- [ ] `C-RL-22` `literal` Every seeded account signs in with `deku-demo-pw-2026`. `src: User roles para 4`

## C-CF Core features

- [ ] `C-CF-01` `capability` The app issues a bearer token on a successful login. `src: Core features, Auth`
- [ ] `C-CF-02` `capability` The app denies a protected endpoint request carrying no token. `src: Core features, Auth`
- [ ] `C-CF-03` `capability` The app denies a protected endpoint request carrying an expired token. `src: Core features, Auth`
- [ ] `C-CF-04` `constraint` The app stores every password hashed. `src: Core features, Auth`
- [ ] `C-CF-05` `capability` The app creates a `reader` on signup. `src: Core features, Auth`
- [ ] `C-CF-06` `constraint` The app offers no password reset. `src: Core features, Auth`
- [ ] `C-CF-07` `constraint` The app offers no external identity provider. `src: Core features, Auth`
- [ ] `C-CF-08` `data` A route record carries a `slug`. `src: Core features rule 1`
- [ ] `C-CF-09` `data` A route record carries a `template`. `src: Core features rule 1`
- [ ] `C-CF-10` `data` A route record carries an ordered list of sections. `src: Core features rule 1`
- [ ] `C-CF-11` `literal` A route record carries a `status` of `draft` or `published`. `src: Core features rule 1`
- [ ] `C-CF-12` `data` A route record leaves `published_at` empty on a `draft` route. `src: Core features rule 1`
- [ ] `C-CF-13` `capability` The app serves a `published` route to anyone. `src: Core features rule 2`
- [ ] `C-CF-14` `capability` The app serves a `draft` route only to an author. `src: Core features rule 3`
- [ ] `C-CF-15` `capability` The app answers a `draft` slug as not found for a reader. `src: Core features rule 3`
- [ ] `C-CF-16` `constraint` A not found answer for a `draft` slug carries no title. `src: Core features rule 3`
- [ ] `C-CF-17` `constraint` A not found answer for a `draft` slug carries no image key. `src: Core features rule 3`
- [ ] `C-CF-18` `capability` Publishing a route stamps `published_at`. `src: Core features rule 4`
- [ ] `C-CF-19` `capability` Unpublishing a route clears `published_at`. `src: Core features rule 4`
- [ ] `C-CF-20` `capability` An unpublished route stops being readable from the next request. `src: Core features rule 4`
- [ ] `C-CF-21` `role` The app denies a reader request to edit a route. `src: Core features rule 5`
- [ ] `C-CF-22` `constraint` The app leaves the stored route unchanged after a denied reader edit. `src: Core features rule 5`
- [ ] `C-CF-23` `constraint` The app holds at most one route for a given slug. `src: Core features rule 6`
- [ ] `C-CF-24` `capability` The app rejects a second route carrying a slug already taken. `src: Core features rule 6`
- [ ] `C-CF-25` `literal` The app carries exactly four templates named `sector`, `capability`, `comparison`, `content`. `src: Core features rule 7`
- [ ] `C-CF-26` `capability` Adding a route is a content operation with no deploy. `src: Core features rule 7`
- [ ] `C-CF-27` `literal` A `sector` route carries the adaptability heading `Custom <sector noun> that adapts to your workflow`. `src: Core features rule 8`
- [ ] `C-CF-28` `literal` A `sector` route carries the shared core claim `The structure of a database, the flexibility of a spreadsheet`. `src: Core features rule 8`
- [ ] `C-CF-29` `capability` The shared core claim is stored once, then inherited by every sector route. `src: Core features rule 8`
- [ ] `C-CF-30` `capability` A `sector` route carries one sector specific control section. `src: Core features rule 8`
- [ ] `C-CF-31` `capability` A `sector` route carries three template cards filtered to that sector. `src: Core features rule 8`
- [ ] `C-CF-32` `literal` A `sector` route carries a cross link reading `Sheaf Solutions`. `src: Core features rule 8`
- [ ] `C-CF-33` `literal` A `sector` route carries a question set headed `Frequently asked questions`. `src: Core features rule 8`
- [ ] `C-CF-34` `literal` A `capability` route carries three numbered steps named `Build`, `Share`, `Analyze`. `src: Core features rule 9`
- [ ] `C-CF-35` `literal` A `capability` route carries a differentiation section headed `Why Sheaf?`. `src: Core features rule 9`
- [ ] `C-CF-36` `capability` A `capability` route closes with one action linking into the product. `src: Core features rule 9`
- [ ] `C-CF-37` `capability` The app rejects a `capability` route carrying a step count other than three. `src: Core features rule 9`
- [ ] `C-CF-38` `data` A comparative claim carries its own `source`. `src: Core features rule 10`
- [ ] `C-CF-39` `data` A comparative claim carries its own `checked_on` date. `src: Core features rule 10`
- [ ] `C-CF-40` `capability` A comparison route renders the source beside the claim. `src: Core features rule 10`
- [ ] `C-CF-41` `capability` A comparison route renders the checked date beside the claim. `src: Core features rule 10`
- [ ] `C-CF-42` `capability` The app rejects a claim saved with no source. `src: Core features rule 10`
- [ ] `C-CF-43` `capability` The app rejects a claim saved with no date. `src: Core features rule 10`
- [ ] `C-CF-44` `constraint` The app writes nothing when a claim is rejected. `src: Core features rule 10`
- [ ] `C-CF-45` `capability` A comparison table is a real table carrying real header cells. `src: Core features rule 10`
- [ ] `C-CF-46` `constraint` A competitor name never appears in the site own typeface. `src: Core features rule 10`
- [ ] `C-CF-47` `capability` A content index carries one featured article. `src: Core features rule 11`
- [ ] `C-CF-48` `literal` A content index carries a heading reading `All Posts`. `src: Core features rule 11`
- [ ] `C-CF-49` `data` A `case_study` article carries a `sector` field. `src: Core features rule 11`
- [ ] `C-CF-50` `data` A `case_study` article carries an `organisation_size` field. `src: Core features rule 11`
- [ ] `C-CF-51` `data` A `case_study` article carries a `capability_demonstrated` field. `src: Core features rule 11`
- [ ] `C-CF-52` `capability` A sector route filters its proof cards on `sector`. `src: Core features rule 11`
- [ ] `C-CF-53` `capability` Every route carries exactly one first-level heading. `src: Core features rule 11`
- [ ] `C-CF-54` `capability` Every card title on a content index is a third-level heading. `src: Core features rule 11`
- [ ] `C-CF-55` `capability` The home route carries thirteen full-width sections in a fixed order. `src: Core features rule 12`
- [ ] `C-CF-56` `literal` The home route document title begins `Spreadsheet Software to End Data Chaos`. `src: Core features rule 12`
- [ ] `C-CF-57` `literal` The home route carries the closing heading `Unlock a better way to organize data.` `src: Core features rule 12`
- [ ] `C-CF-58` `literal` The hero carries the headline `Turn the spreadsheets running your business into secure applications`. `src: Core features rule 13`
- [ ] `C-CF-59` `literal` The hero subtitle states that cell-level access rules control who sees what. `src: Core features rule 13`
- [ ] `C-CF-60` `literal` The hero carries a primary action reading `Get started`. `src: Core features rule 13`
- [ ] `C-CF-61` `literal` The hero carries a secondary action reading `Build with a prompt`. `src: Core features rule 13`
- [ ] `C-CF-62` `literal` The hero carries an arrow link reading `Security for regulated industries`. `src: Core features rule 13`
- [ ] `C-CF-63` `ui` The hero gives the secondary action prominence equal to the primary action. `src: Core features rule 13`
- [ ] `C-CF-64` `ui` The hero carries a product demonstration with a poster frame. `src: Core features rule 13`
- [ ] `C-CF-65` `literal` The capability section carries six third-level headings naming the product capabilities. `src: Core features rule 14`
- [ ] `C-CF-66` `literal` The `Access rules` capability carries a supporting line naming granular data permissions. `src: Core features rule 14`
- [ ] `C-CF-67` `literal` The `Flexible layout` capability carries a supporting line about arranging data on screen. `src: Core features rule 14`
- [ ] `C-CF-68` `literal` The power tools section carries three third-level headings named `Super-charged formulas`, `Extensible`, `Unprecedented control`. `src: Core features rule 15`
- [ ] `C-CF-69` `literal` The power tools section carries a link reading `Sheaf for developers`. `src: Core features rule 15`
- [ ] `C-CF-70` `capability` The security section carries a role card for the technology department. `src: Core features rule 15`
- [ ] `C-CF-71` `literal` The home route names three reference customers, `Northgate Digital Service`, `Merrow Instruments`, `Halliwell Electrical`. `src: Core features rule 16`
- [ ] `C-CF-72` `ui` Each reference customer renders as a name set in type. `src: Core features rule 16`
- [ ] `C-CF-73` `literal` The home route names three featured templates, `Investment Research Tracker`, `Class Enrolment Register`, `Customer Records Lite`. `src: Core features rule 17`
- [ ] `C-CF-74` `capability` A template card opens `https://app.sheaf.example`. `src: Core features rule 17`
- [ ] `C-CF-75` `capability` An announcement bar sits above the header on every route. `src: Core features rule 18`
- [ ] `C-CF-76` `literal` The announcement bar reads `Looking for a Latticework alternative? See how Sheaf compares.` `src: Core features rule 18`
- [ ] `C-CF-77` `capability` The announcement bar is dismissible. `src: Core features rule 18`
- [ ] `C-CF-78` `capability` The announcement bar dismissal survives a reload. `src: Core features rule 18`
- [ ] `C-CF-79` `literal` The header carries five menu triggers reading `Product`, `Solutions`, `Developers`, `Resources`, `Pricing`. `src: Core features rule 19`
- [ ] `C-CF-80` `ui` Each header trigger opens a menu panel rather than navigating. `src: Core features rule 19`
- [ ] `C-CF-81` `literal` Every menu panel carries a closing strip reading `Get started`, `Contact sales`. `src: Core features rule 19`
- [ ] `C-CF-82` `capability` A closed menu panel is removed from the focus order. `src: Core features rule 20`
- [ ] `C-CF-83` `capability` A closed menu panel is removed from the accessibility tree. `src: Core features rule 20`
- [ ] `C-CF-84` `literal` The star count control reads a count from `GET /api/stars`. `src: Core features rule 21`
- [ ] `C-CF-85` `literal` The star count control renders the word `Star` when no count is available. `src: Core features rule 21`
- [ ] `C-CF-86` `ui` The star count control reserves the space for the number from first paint. `src: Core features rule 21`
- [ ] `C-CF-87` `literal` Every route other than the home route ends with a band headed `Create a free site`. `src: Core features rule 22`
- [ ] `C-CF-88` `constraint` The home route carries no closing action band. `src: Core features rule 22`
- [ ] `C-CF-89` `ui` The footer carries multiple link columns. `src: Core features rule 23`
- [ ] `C-CF-90` `ui` The footer carries a social row of six links. `src: Core features rule 23`
- [ ] `C-CF-91` `literal` Every stored image key follows the scheme `media/{route_id}/{sha256_of_bytes}.{ext}`. `src: Core features rule 24`
- [ ] `C-CF-92` `constraint` No image byte lives on the app container filesystem. `src: Core features rule 24`
- [ ] `C-CF-93` `constraint` No image byte lives in a database column. `src: Core features rule 24`
- [ ] `C-CF-94` `capability` Uploading identical bytes twice for one route returns the existing key. `src: Core features rule 25`
- [ ] `C-CF-95` `constraint` Uploading identical bytes twice for one route creates no second object. `src: Core features rule 25`
- [ ] `C-CF-96` `role` The app denies a reader request to upload an image. `src: Core features rule 26`
- [ ] `C-CF-97` `constraint` The app writes no object to the bucket after a denied upload. `src: Core features rule 26`
- [ ] `C-CF-98` `capability` The app denies a signed out request for an image attached to a `draft` route. `src: Core features rule 27`
- [ ] `C-CF-99` `capability` The app serves that image once the route is `published`. `src: Core features rule 27`
- [ ] `C-CF-100` `capability` The app serves protected bytes through an authenticated endpoint on the app own origin. `src: Core features rule 27`
- [ ] `C-CF-101` `capability` The app rejects an image saved with no alternative text. `src: Core features rule 28`
- [ ] `C-CF-102` `capability` A rejected image save names the missing field. `src: Core features rule 28`
- [ ] `C-CF-103` `capability` A decorative image declares itself decorative. `src: Core features rule 28`
- [ ] `C-CF-104` `literal` `POST /api/trials` takes `email`, `team_name`, `sector`. `src: Core features rule 29`
- [ ] `C-CF-105` `capability` The app creates a trial from a valid submission. `src: Core features rule 29`
- [ ] `C-CF-106` `literal` The team site address follows the scheme `https://{team_slug}.sheaf.example`. `src: Core features rule 29`
- [ ] `C-CF-107` `literal` The team name `Merrow Instruments` produces `https://merrow-instruments.sheaf.example`. `src: Core features rule 29`
- [ ] `C-CF-108` `capability` The confirmation route carries the team site address. `src: Core features rule 29`
- [ ] `C-CF-109` `constraint` The app holds at most one trial for a given team slug. `src: Core features rule 30`
- [ ] `C-CF-110` `capability` Two simultaneous submissions of one team name leave exactly one trial. `src: Core features rule 30`
- [ ] `C-CF-111` `capability` The losing submission of that race is rejected as a conflict. `src: Core features rule 30`
- [ ] `C-CF-112` `capability` A repeated submission of one email with one team name creates no second trial. `src: Core features rule 31`
- [ ] `C-CF-113` `capability` A repeated submission returns the first team site address unchanged. `src: Core features rule 31`
- [ ] `C-CF-114` `capability` Starting a trial signs a signed out visitor in as a `reader`. `src: Core features rule 32`
- [ ] `C-CF-115` `role` The app denies a reader request for the trial of another reader. `src: Core features rule 32`
- [ ] `C-CF-116` `role` The app serves `GET /api/trials` only to an author. `src: Core features rule 32`
- [ ] `C-CF-117` `capability` Every form rejects invalid input inline. `src: Core features rule 33`
- [ ] `C-CF-118` `capability` A rejected form names the field rejected. `src: Core features rule 33`
- [ ] `C-CF-119` `constraint` A rejected form writes nothing. `src: Core features rule 33`
- [ ] `C-CF-120` `capability` The app rejects a trial carrying an email with no `@`. `src: Core features rule 33`
- [ ] `C-CF-121` `capability` The app rejects a trial carrying a sector outside the published sector list. `src: Core features rule 33`
- [ ] `C-CF-122` `capability` A first-time visitor is asked once about non essential cookies. `src: Core features rule 34`
- [ ] `C-CF-123` `ui` The cookie bar offers accept, decline as two equally reachable controls. `src: Core features rule 34`
- [ ] `C-CF-124` `capability` The cookie answer survives a reload. `src: Core features rule 34`
- [ ] `C-CF-125` `constraint` The visitor is not asked a second time about cookies. `src: Core features rule 34`
- [ ] `C-CF-126` `constraint` No third-party script is requested before the cookie answer is accept. `src: Core features rule 35`
- [ ] `C-CF-127` `constraint` The site own origin is the only origin contacted on a first paint. `src: Core features rule 35`
- [ ] `C-CF-128` `capability` The video embed renders a poster frame with a play control before any embed loads. `src: Core features rule 35`
- [ ] `C-CF-129` `capability` Every internal link on a published route resolves to a published route. `src: Core features rule 36`
- [ ] `C-CF-130` `literal` `GET /api/links` returns every internal link with a resolved status. `src: Core features rule 36`

## C-UF User flow

- [ ] `C-UF-01` `literal` The app serves the home route at `/`. `src: User flow table row 1`
- [ ] `C-UF-02` `literal` The app serves a template gallery at `/templates/`. `src: User flow table row 11`
- [ ] `C-UF-03` `literal` The app serves a sector index at `/solutions/`. `src: User flow table row 12`
- [ ] `C-UF-04` `literal` The app serves a comparison route at `/lookup/latticework/`. `src: User flow table row 16`
- [ ] `C-UF-05` `literal` The app serves a content index at `/blog/`. `src: User flow table row 17`
- [ ] `C-UF-06` `literal` The app serves a case study index at `/case-studies/`. `src: User flow table row 18`
- [ ] `C-UF-07` `literal` The app serves a privacy route at `/privacy/` stating what the site stores about a visitor. `src: User flow table row 23`
- [ ] `C-UF-08` `literal` The app serves a trial form at `/trial/`. `src: User flow table row 25`
- [ ] `C-UF-09` `literal` The app serves a trial confirmation at `/trial/started/` to a reader. `src: User flow table row 26`
- [ ] `C-UF-10` `literal` The app serves an authoring console at `/studio/` to an author. `src: User flow table row 29`
- [ ] `C-UF-11` `capability` A signed out request for `/studio/` redirects to `/login`. `src: User flow, Entry and redirects`
- [ ] `C-UF-12` `capability` A successful sign in lands on the address originally requested. `src: User flow, Entry and redirects`
- [ ] `C-UF-13` `capability` A reader reaching `/studio/` is refused with a way back to `/`. `src: User flow, Entry and redirects`
- [ ] `C-UF-14` `capability` Signing out returns the visitor to `/`. `src: User flow, Entry and redirects`
- [ ] `C-UF-15` `capability` A token expiring mid edit leaves the typed text in place. `src: User flow, Entry and redirects`
- [ ] `C-UF-16` `capability` An unknown address renders the site own not found page with a way back. `src: User flow, Entry and redirects`
- [ ] `C-UF-17` `capability` The authoring route table lists every route with slug, template, status, last edit. `src: User flow, Journey 2`
- [ ] `C-UF-18` `ui` Every list carries an empty state naming what would appear there. `src: User flow, States`
- [ ] `C-UF-19` `ui` Every route carries a loading state reserving the space its content will occupy. `src: User flow, States`
- [ ] `C-UF-20` `constraint` No failure shows a stack trace. `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The accent colour is a mid, vivid teal. `src: UI/UX notes para 2`
- [ ] `C-UX-02` `ui` The accent colour appears on nothing decorative. `src: UI/UX notes para 2`
- [ ] `C-UX-03` `ui` Headings carry a deep, muted blue. `src: UI/UX notes para 2`
- [ ] `C-UX-04` `ui` Body text carries a mid neutral. `src: UI/UX notes para 2`
- [ ] `C-UX-05` `ui` The footer carries a near-black cool neutral background with light neutral text. `src: UI/UX notes para 2`
- [ ] `C-UX-06` `ui` The colour meaning a refused form is a mid, vivid red used nowhere else. `src: UI/UX notes para 2`
- [ ] `C-UX-07` `ui` One gradient runs teal on the left to green on the right. `src: UI/UX notes para 3`
- [ ] `C-UX-08` `constraint` The site carries no second gradient. `src: UI/UX notes para 3`
- [ ] `C-UX-09` `constraint` No component binds a preset value from the publishing system palette. `src: UI/UX notes para 3`
- [ ] `C-UX-10` `ui` One text family in four weights is declared as a single token. `src: UI/UX notes para 5`
- [ ] `C-UX-11` `constraint` The build ships no font file. `src: UI/UX notes para 5`
- [ ] `C-UX-12` `literal` The type scale carries six heading steps with one body step at `16`. `src: UI/UX notes para 5`
- [ ] `C-UX-13` `literal` Heading 5 renders uppercase at `14` with letter spacing of `0.075em`. `src: UI/UX notes para 5`
- [ ] `C-UX-14` `ui` The type scale gains one step so no two roles share a size. `src: UI/UX notes para 5`
- [ ] `C-UX-15` `ui` Social links are rounded on one diagonal, square on the other. `src: UI/UX notes para 6`
- [ ] `C-UX-16` `ui` The build carries exactly one shadow, flat, offset, with no blur. `src: UI/UX notes para 6`
- [ ] `C-UX-17` `ui` The build carries two container widths with no third. `src: UI/UX notes para 6`
- [ ] `C-UX-18` `ui` Motion character is eased, with movement leaving quickly, arriving slowly. `src: UI/UX notes para 7`
- [ ] `C-UX-19` `ui` Hovering a link grows an underline from one side. `src: UI/UX notes para 7`
- [ ] `C-UX-20` `ui` The underline appears on keyboard focus. `src: UI/UX notes para 7`
- [ ] `C-UX-21` `constraint` Nothing on the site moves in response to scroll position. `src: UI/UX notes para 7`
- [ ] `C-UX-22` `capability` The product demonstration does not autoplay under a reduced motion preference. `src: UI/UX notes para 7`
- [ ] `C-UX-23` `capability` Any looping figure offers a pause control. `src: UI/UX notes para 7`
- [ ] `C-UX-24` `ui` Escape closes an open menu panel, returning focus to the trigger. `src: UI/UX notes para 8`
- [ ] `C-UX-25` `ui` Unpublishing a route confirms first. `src: UI/UX notes para 8`
- [ ] `C-UX-26` `ui` A control whose only content is a symbol carries a programmatic name. `src: UI/UX notes para 8`
- [ ] `C-UX-27` `ui` Text contrast meets WCAG AA per token pair. `src: UI/UX notes para 9`
- [ ] `C-UX-28` `ui` Footer text contrast on the footer background is confirmed explicitly. `src: UI/UX notes para 9`
- [ ] `C-UX-29` `ui` Keyboard navigation reaches every interactive element in visual order. `src: UI/UX notes para 9`
- [ ] `C-UX-30` `ui` Every route carries header, navigation, main, footer landmarks. `src: UI/UX notes para 9`
- [ ] `C-UX-31` `ui` Heading order runs without skipping a level. `src: UI/UX notes para 9`
- [ ] `C-UX-32` `constraint` Meaning is never carried by colour alone. `src: UI/UX notes para 9`
- [ ] `C-UX-33` `ui` The build declares four breakpoints as tokens. `src: UI/UX notes para 10`
- [ ] `C-UX-34` `ui` No route overflows sideways at any width down to a small phone. `src: UI/UX notes para 10`
- [ ] `C-UX-35` `ui` The first-level heading steps down at the narrow widths. `src: UI/UX notes para 10`
- [ ] `C-UX-36` `ui` The five menu panels collapse to a single accordion below the narrow breakpoint. `src: UI/UX notes para 10`
- [ ] `C-UX-37` `ui` The build commits to a light mode designed in full. `src: UI/UX notes para 11`

## C-FE Front-end specification

- [ ] `C-FE-01` `literal` A section style is one of default, light, dark, brand gradient, large pattern, small pattern. `src: Front-end specification para 1`
- [ ] `C-FE-02` `ui` Both background patterns are drawn procedurally rather than fetched. `src: Front-end specification para 1`
- [ ] `C-FE-03` `ui` Every glyph is inline vector. `src: Front-end specification para 2`
- [ ] `C-FE-04` `ui` Four first-party blocks build every section of the home route. `src: Front-end specification para 3`
- [ ] `C-FE-05` `ui` Every section, container, content block carries a shared block-name prefix. `src: Front-end specification para 3`
- [ ] `C-FE-06` `ui` A closed mega-menu panel stays out of the focus order. `src: Front-end specification para 4`
- [ ] `C-FE-07` `ui` The mark is a three-by-three arrangement of rounded squares with cells omitted. `src: Front-end specification para 6`
- [ ] `C-FE-08` `constraint` The build ships no binary asset. `src: Front-end specification para 7`
- [ ] `C-FE-09` `ui` Card artwork is seeded from the card own title. `src: Front-end specification para 7`
- [ ] `C-FE-10` `ui` Each capability figure carries a caption describing what a real recording would show. `src: Front-end specification para 7`
- [ ] `C-FE-11` `ui` Every generated substitute is deterministic from its seed. `src: Front-end specification para 7`
- [ ] `C-FE-12` `constraint` No feature demonstration ships as an animated raster image. `src: Front-end specification para 8`
- [ ] `C-FE-13` `ui` Images below the fold are deferred. `src: Front-end specification para 8`
- [ ] `C-FE-14` `constraint` The build own stacking scale carries no value above four digits. `src: Front-end specification para 9`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The browser receives complete HTML for every public route on first paint. `src: Technical requirements para 1`
- [ ] `C-TR-02` `literal` The datastore is `PostgreSQL`, read from `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-03` `literal` Images live in `MinIO`, read from `STORAGE_ENDPOINT`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `literal` The bucket name is read from `STORAGE_BUCKET`. `src: Technical requirements para 1`
- [ ] `C-TR-05` `literal` The object store credentials are read from `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. `src: Technical requirements para 1`
- [ ] `C-TR-06` `literal` The public address is read from `APP_PUBLIC_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-07` `literal` The public port is read from `APP_PUBLIC_PORT`. `src: Technical requirements para 1`
- [ ] `C-TR-08` `literal` `GET /api/health` returns `200` without a token. `src: Technical requirements para 3`
- [ ] `C-TR-09` `constraint` A log line never carries a password. `src: Technical requirements para 3`
- [ ] `C-TR-10` `contract` Every response carries a strict transport policy header. `src: Technical requirements para 4`
- [ ] `C-TR-11` `contract` Every response carries a nosniff content-type policy header. `src: Technical requirements para 4`
- [ ] `C-TR-12` `contract` The not-found response carries the same security headers. `src: Technical requirements para 4`
- [ ] `C-TR-13` `constraint` Nothing the browser downloads carries an object store secret. `src: Technical requirements para 4`
- [ ] `C-TR-14` `capability` Read access to unpublished content is decided on the server for every request. `src: Technical requirements para 5`
- [ ] `C-TR-15` `constraint` A content index shows the published count rather than the total. `src: Technical requirements para 5`
- [ ] `C-TR-16` `constraint` The app makes no outbound network request at runtime. `src: Technical requirements para 7`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema carries seven tables. `src: Data model para 1`
- [ ] `C-DM-02` `data` Every timestamp is UTC. `src: Data model para 1`
- [ ] `C-DM-03` `literal` The seeded password `deku-demo-pw-2026` works at login. `src: Data model para 2`
- [ ] `C-DM-04` `contract` The seeded logins are written into `/app/USER_README.md`. `src: Data model para 2`
- [ ] `C-DM-05` `data` The `users` table carries a unique lowercased `email`. `src: Data model, users`
- [ ] `C-DM-06` `data` The `users` table carries a `role` of `author` or `reader`. `src: Data model, users`
- [ ] `C-DM-07` `data` The `routes` table carries a `slug` unique across the table. `src: Data model, routes`
- [ ] `C-DM-08` `data` The `sections` table carries a `position` unique within a route. `src: Data model, sections`
- [ ] `C-DM-09` `data` A route reads its sections in `position` order. `src: Data model, sections`
- [ ] `C-DM-10` `data` The `claims` table requires `source`, `checked_on`. `src: Data model, claims`
- [ ] `C-DM-11` `data` The `articles` table carries a `kind` of `post`, `webinar`, `case_study`. `src: Data model, articles`
- [ ] `C-DM-12` `data` Exactly one article per content index carries `tier` of `featured`. `src: Data model, articles`
- [ ] `C-DM-13` `data` The `media` table holds the pair `(route_id, sha256)` at most once. `src: Data model, media`
- [ ] `C-DM-14` `data` The `trials` table carries a `team_slug` unique across the table. `src: Data model, trials`
- [ ] `C-DM-15` `data` The app seeds nine `published` routes. `src: Data model, Seed data`
- [ ] `C-DM-16` `literal` The app seeds a `draft` sector route at `/solutions/legal/`. `src: Data model, Seed data`
- [ ] `C-DM-17` `literal` The app seeds a `draft` comparison route at `/lookup/rowbase/`. `src: Data model, Seed data`
- [ ] `C-DM-18` `data` The app seeds three case study articles, one per reference customer. `src: Data model, Seed data`
- [ ] `C-DM-19` `data` The app seeds one media row on the `draft` legal route. `src: Data model, Seed data`
- [ ] `C-DM-20` `data` The app seeds one trial for `reader@example.com` named `Merrow Instruments`. `src: Data model, Seed data`
- [ ] `C-DM-21` `constraint` Restarting the app duplicates no row. `src: Data model, Seed data`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The site is single tenant. `src: Constraints para 1`
- [ ] `C-CN-02` `constraint` The site carries no per-customer branding. `src: Constraints para 1`
- [ ] `C-CN-03` `constraint` The site carries no formula editor. `src: Constraints para 1`
- [ ] `C-CN-04` `constraint` The site carries no access-rule editor. `src: Constraints para 1`
- [ ] `C-CN-05` `constraint` The site carries no form builder. `src: Constraints para 1`
- [ ] `C-CN-06` `constraint` The site carries no assistant. `src: Constraints para 1`
- [ ] `C-CN-07` `constraint` The site carries no billing screen. `src: Constraints para 1`
- [ ] `C-CN-08` `constraint` The site sends no email. `src: Constraints para 1`
- [ ] `C-CN-09` `constraint` The site carries no full-text search. `src: Constraints para 1`
- [ ] `C-CN-10` `constraint` The site carries no second language. `src: Constraints para 1`
- [ ] `C-CN-11` `constraint` The site carries no native application. `src: Constraints para 1`
- [ ] `C-CN-12` `constraint` The site reproduces no third-party mark. `src: Constraints para 1`
- [ ] `C-CN-13` `constraint` The site stays responsive at roughly forty routes. `src: Constraints para 1`
- [ ] `C-CN-14` `constraint` The site stays responsive at one thousand trials. `src: Constraints para 1`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The container-internal port is `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The app hardcodes neither the public address nor the port. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-05` `literal` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-07` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-08` `contract` The server is not a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-09` `literal` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-10` `literal` `POST /api/auth/login` returns the bearer token as `access_token`. `src: Deployment contract, API shapes row 2`
- [ ] `C-DC-11` `literal` `GET /api/pages` returns a top-level JSON array of route summaries. `src: Deployment contract, API shapes row 5`
- [ ] `C-DC-12` `literal` `GET /api/pages/{slug}` returns the route with its `sections` in order. `src: Deployment contract, API shapes row 6`
- [ ] `C-DC-13` `literal` `POST /api/pages` creates a route at `status` `draft`. `src: Deployment contract, API shapes row 7`
- [ ] `C-DC-14` `literal` `POST /api/media` returns `{ "object_key" }`. `src: Deployment contract, API shapes row 10`
- [ ] `C-DC-15` `literal` `POST /api/trials` returns `{ "team_slug", "team_site_url" }`. `src: Deployment contract, API shapes row 12`
- [ ] `C-DC-16` `literal` `POST /api/consent` stores a `choice` of `accept` or `decline`. `src: Deployment contract, API shapes row 15`
- [ ] `C-DC-17` `capability` An invalid call is rejected as a client error rather than a server error. `src: Deployment contract, API shapes para`
- [ ] `C-DC-18` `constraint` A media object exists in the `MinIO` bucket rather than in an in-memory array. `src: Deployment contract, No mocks`
- [ ] `C-DC-19` `constraint` A route row exists in `PostgreSQL` rather than in a JSON file on disk. `src: Deployment contract, No mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `Spreadsheet Software to End Data Chaos` | the home route document title, before the product name | C-CF-56 | Core features rule 12 |
| `No-code apps, self-hosted or fully managed. Cell-level access rules control who sees what, including the AI assistant.` | the hero subtitle | C-CF-59 | Core features rule 13 |
| `Collaborate with confidence and peace of mind, using a unique system of granular data permissions.` | the Access rules supporting line | C-CF-66 | Core features rule 14 |
| `Arrange your data on screen to maximize the productivity of you and your team.` | the Flexible layout supporting line | C-CF-67 | Core features rule 14 |
| `Lock down insider risk by eliminating spreadsheet sprawl.` | the technology role card line | C-CF-70 | Core features rule 15 |
| `IT` | the technology role card heading | C-CF-70 | Core features rule 15 |
| `Try it now!` | the capability route closing action | C-CF-36 | Core features rule 9 |
| `access_token` | the field a successful login returns | C-DC-10 | Deployment contract, API shapes row 2 |
| `https://app.sheaf.example` | the product origin every sign in link leaves for | C-OV-04 | Overview para 2 |
| `author@example.com` | seeded author email | C-RL-19 | User roles table row 5 |
| `author2@example.com` | seeded second author email | C-RL-20 | User roles table row 6 |
| `reader@example.com` | seeded reader email | C-RL-21 | User roles table row 7 |
| `deku-demo-pw-2026` | seeded password for every account | C-RL-22 | User roles para 4 |
| `status` | value pinned by the brief | C-CF-11 | Core features rule 1 |
| `draft` | value pinned by the brief | C-CF-11 | Core features rule 1 |
| `published` | value pinned by the brief | C-CF-11 | Core features rule 1 |
| `sector` | value pinned by the brief | C-CF-25 | Core features rule 7 |
| `capability` | value pinned by the brief | C-CF-25 | Core features rule 7 |
| `comparison` | value pinned by the brief | C-CF-25 | Core features rule 7 |
| `content` | value pinned by the brief | C-CF-25 | Core features rule 7 |
| `Custom <sector noun> that adapts to your workflow` | value pinned by the brief | C-CF-27 | Core features rule 8 |
| `The structure of a database, the flexibility of a spreadsheet` | value pinned by the brief | C-CF-28 | Core features rule 8 |
| `Sheaf Solutions` | value pinned by the brief | C-CF-32 | Core features rule 8 |
| `Frequently asked questions` | value pinned by the brief | C-CF-33 | Core features rule 8 |
| `Build` | value pinned by the brief | C-CF-34 | Core features rule 9 |
| `Share` | value pinned by the brief | C-CF-34 | Core features rule 9 |
| `Analyze` | value pinned by the brief | C-CF-34 | Core features rule 9 |
| `Why Sheaf?` | value pinned by the brief | C-CF-35 | Core features rule 9 |
| `All Posts` | value pinned by the brief | C-CF-48 | Core features rule 11 |
| `Unlock a better way to organize data.` | value pinned by the brief | C-CF-57 | Core features rule 12 |
| `Turn the spreadsheets running your business into secure applications` | value pinned by the brief | C-CF-58 | Core features rule 13 |
| `Get started` | value pinned by the brief | C-CF-60 | Core features rule 13 |
| `Build with a prompt` | value pinned by the brief | C-CF-61 | Core features rule 13 |
| `Security for regulated industries` | value pinned by the brief | C-CF-62 | Core features rule 13 |
| `Access rules` | value pinned by the brief | C-CF-66 | Core features rule 14 |
| `Flexible layout` | value pinned by the brief | C-CF-67 | Core features rule 14 |
| `Super-charged formulas` | value pinned by the brief | C-CF-68 | Core features rule 15 |
| `Extensible` | value pinned by the brief | C-CF-68 | Core features rule 15 |
| `Unprecedented control` | value pinned by the brief | C-CF-68 | Core features rule 15 |
| `Sheaf for developers` | value pinned by the brief | C-CF-69 | Core features rule 15 |
| `Northgate Digital Service` | value pinned by the brief | C-CF-71 | Core features rule 16 |
| `Merrow Instruments` | value pinned by the brief | C-CF-71 | Core features rule 16 |
| `Halliwell Electrical` | value pinned by the brief | C-CF-71 | Core features rule 16 |
| `Investment Research Tracker` | value pinned by the brief | C-CF-73 | Core features rule 17 |
| `Class Enrolment Register` | value pinned by the brief | C-CF-73 | Core features rule 17 |
| `Customer Records Lite` | value pinned by the brief | C-CF-73 | Core features rule 17 |
| `Looking for a Latticework alternative? See how Sheaf compares.` | value pinned by the brief | C-CF-76 | Core features rule 18 |
| `Product` | value pinned by the brief | C-CF-79 | Core features rule 19 |
| `Solutions` | value pinned by the brief | C-CF-79 | Core features rule 19 |
| `Developers` | value pinned by the brief | C-CF-79 | Core features rule 19 |
| `Resources` | value pinned by the brief | C-CF-79 | Core features rule 19 |
| `Pricing` | value pinned by the brief | C-CF-79 | Core features rule 19 |
| `Contact sales` | value pinned by the brief | C-CF-81 | Core features rule 19 |
| `GET /api/stars` | value pinned by the brief | C-CF-84 | Core features rule 21 |
| `Star` | value pinned by the brief | C-CF-85 | Core features rule 21 |
| `Create a free site` | value pinned by the brief | C-CF-87 | Core features rule 22 |
| `media/{route_id}/{sha256_of_bytes}.{ext}` | value pinned by the brief | C-CF-91 | Core features rule 24 |
| `POST /api/trials` | value pinned by the brief | C-CF-104 | Core features rule 29 |
| `email` | value pinned by the brief | C-CF-104 | Core features rule 29 |
| `team_name` | value pinned by the brief | C-CF-104 | Core features rule 29 |
| `https://{team_slug}.sheaf.example` | value pinned by the brief | C-CF-106 | Core features rule 29 |
| `https://merrow-instruments.sheaf.example` | value pinned by the brief | C-CF-107 | Core features rule 29 |
| `GET /api/links` | value pinned by the brief | C-CF-130 | Core features rule 36 |
| `/` | value pinned by the brief | C-UF-01 | User flow table row 1 |
| `/templates/` | value pinned by the brief | C-UF-02 | User flow table row 11 |
| `/solutions/` | value pinned by the brief | C-UF-03 | User flow table row 12 |
| `/lookup/latticework/` | value pinned by the brief | C-UF-04 | User flow table row 16 |
| `/blog/` | value pinned by the brief | C-UF-05 | User flow table row 17 |
| `/case-studies/` | value pinned by the brief | C-UF-06 | User flow table row 18 |
| `/privacy/` | value pinned by the brief | C-UF-07 | User flow table row 23 |
| `/trial/` | value pinned by the brief | C-UF-08 | User flow table row 25 |
| `/trial/started/` | value pinned by the brief | C-UF-09 | User flow table row 26 |
| `/studio/` | value pinned by the brief | C-UF-10 | User flow table row 29 |
| `16` | value pinned by the brief | C-UX-12 | UI/UX notes para 5 |
| `14` | value pinned by the brief | C-UX-13 | UI/UX notes para 5 |
| `0.075em` | value pinned by the brief | C-UX-13 | UI/UX notes para 5 |
| `PostgreSQL` | value pinned by the brief | C-TR-02 | Technical requirements para 1 |
| `DATABASE_URL` | value pinned by the brief | C-TR-02 | Technical requirements para 1 |
| `MinIO` | value pinned by the brief | C-TR-03 | Technical requirements para 1 |
| `STORAGE_ENDPOINT` | value pinned by the brief | C-TR-03 | Technical requirements para 1 |
| `STORAGE_BUCKET` | value pinned by the brief | C-TR-04 | Technical requirements para 1 |
| `STORAGE_ACCESS_KEY` | value pinned by the brief | C-TR-05 | Technical requirements para 1 |
| `STORAGE_SECRET_KEY` | value pinned by the brief | C-TR-05 | Technical requirements para 1 |
| `APP_PUBLIC_URL` | value pinned by the brief | C-TR-06 | Technical requirements para 1 |
| `APP_PUBLIC_PORT` | value pinned by the brief | C-TR-07 | Technical requirements para 1 |
| `GET /api/health` | value pinned by the brief | C-TR-08 | Technical requirements para 3 |
| `200` | the ready answer from the health route | C-TR-08 | Technical requirements para 3 |
| `/solutions/legal/` | value pinned by the brief | C-DM-16 | Data model, Seed data |
| `/lookup/rowbase/` | value pinned by the brief | C-DM-17 | Data model, Seed data |
| `4173` | the container-internal port | C-DC-02 | Deployment contract bullet 1 |
| `0.0.0.0` | the bind address | C-DC-09 | Deployment contract bullet 9 |
| `POST /api/auth/login` | value pinned by the brief | C-DC-10 | Deployment contract, API shapes row 2 |
| `GET /api/pages` | value pinned by the brief | C-DC-11 | Deployment contract, API shapes row 5 |
| `GET /api/pages/{slug}` | value pinned by the brief | C-DC-12 | Deployment contract, API shapes row 6 |
| `sections` | value pinned by the brief | C-DC-12 | Deployment contract, API shapes row 6 |
| `POST /api/pages` | value pinned by the brief | C-DC-13 | Deployment contract, API shapes row 7 |
| `POST /api/media` | value pinned by the brief | C-DC-14 | Deployment contract, API shapes row 10 |
| `{ "object_key" }` | value pinned by the brief | C-DC-14 | Deployment contract, API shapes row 10 |
| `{ "team_slug", "team_site_url" }` | value pinned by the brief | C-DC-15 | Deployment contract, API shapes row 12 |
| `POST /api/consent` | value pinned by the brief | C-DC-16 | Deployment contract, API shapes row 15 |
| `choice` | value pinned by the brief | C-DC-16 | Deployment contract, API shapes row 15 |
| `accept` | value pinned by the brief | C-DC-16 | Deployment contract, API shapes row 15 |
| `decline` | value pinned by the brief | C-DC-16 | Deployment contract, API shapes row 15 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the transfer budget for the home route before consent | C-FE-13 | named as strict with no number given |
| the sector specific compliance concern on a sector route | C-CF-30 | named per sector with no list given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 5 | 15 |
| User roles | 1 | 22 |
| Core features | 16 | 130 |
| User flow | 10 | 20 |
| UI and UX notes | 8 | 37 |
| Front-end specification | 5 | 14 |
| Technical requirements | 12 | 16 |
| Data model | 5 | 21 |
| Constraints | 1 | 14 |
| Deployment contract | 14 | 19 |

Definition of done restates obligations already carried by Core features, Constraints
and Deployment contract, so it produces no separate block, per the restatement rule.
