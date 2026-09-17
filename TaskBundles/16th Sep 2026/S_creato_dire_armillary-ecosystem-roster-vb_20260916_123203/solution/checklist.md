# Checklist: Halden

Items: 410
Unpinned values flagged: 3
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` Halden is organised around four divisions `src: Overview`
- [ ] `C-OV-02` `capability` Each division carries a name, a colour, a scene, a roster, a route `src: Overview`
- [ ] `C-OV-03` `ui` The front door is a single three-dimensional armillary filling one window `src: Overview`
- [ ] `C-OV-04` `capability` The roster route shows every live profile on one filterable grid `src: Overview`
- [ ] `C-OV-05` `capability` A creator owns exactly one roster profile `src: Overview`
- [ ] `C-OV-06` `capability` A curator publishes, sends back, takes down, moves or orders profiles `src: Overview`
- [ ] `C-OV-07` `ui` Every heading on the site is revealed line by line rather than fading in flat `src: Overview`
- [ ] `C-OV-08` `capability` A fresh visitor finds a moved creator on the second division route only `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor reads every live profile without an account `src: User roles`
- [ ] `C-RL-02` `role` A visitor cannot call any own-profile endpoint `src: User roles`
- [ ] `C-RL-03` `role` A creator reads the creator's own profile at any state `src: User roles`
- [ ] `C-RL-04` `role` A creator cannot read another creator's profile by any address `src: User roles`
- [ ] `C-RL-05` `role` A creator cannot change another creator's profile `src: User roles`
- [ ] `C-RL-06` `role` A creator cannot publish, send back, take down, move or reorder any profile `src: User roles`
- [ ] `C-RL-07` `role` A state filter sent by a creator is dropped `src: User roles`
- [ ] `C-RL-08` `role` A creator cannot submit before confirming the address `src: User roles`
- [ ] `C-RL-09` `role` A creator cannot edit a profile held with the studio `src: User roles`
- [ ] `C-RL-10` `role` A curator reads every submitted profile in the review queue `src: User roles`
- [ ] `C-RL-11` `role` A curator cannot change a creator's name or statement `src: User roles`
- [ ] `C-RL-12` `role` A curator cannot publish a profile that is not submitted `src: User roles`
- [ ] `C-RL-13` `role` A denied creator call leaves the protected state unchanged `src: User roles`
- [ ] `C-RL-14` `role` The role comes from the session on the server, never from the request body `src: User roles`
- [ ] `C-RL-15` `role` An anonymous profile write is denied `src: User roles`
- [ ] `C-RL-16` `role` Submitting the application creates one creator account `src: User roles`
- [ ] `C-RL-17` `literal` `curator@example.com` signs in as the seeded curator `src: User roles`
- [ ] `C-RL-18` `literal` `creator@example.com` owns the live profile `juno-okafor` `src: User roles`
- [ ] `C-RL-19` `literal` `creator2@example.com` owns the draft profile `ada-moreau` `src: User roles`
- [ ] `C-RL-20` `literal` Every seeded account signs in with `deku-demo-pw-2026` `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `contract` POST /api/auth/login returns a bearer access token for a seeded account `src: Core features > Sign in`
- [ ] `C-CF-02` `contract` The login response carries the account role `src: Core features > Sign in`
- [ ] `C-CF-03` `contract` The login response carries whether the address is confirmed `src: Core features > Sign in`
- [ ] `C-CF-04` `constraint` A wrong password is refused with no token `src: Core features > Sign in`
- [ ] `C-CF-05` `constraint` An email with no account is refused with no token `src: Core features > Sign in`
- [ ] `C-CF-06` `literal` A refused sign in answers the error token `not_authenticated` `src: Core features > Sign in`
- [ ] `C-CF-07` `constraint` Five failed sign-ins for one email within fifteen minutes refuse the next attempt `src: Core features > Sign in`
- [ ] `C-CF-08` `literal` The limited attempt answers `429` with the error token `rate_limited` `src: Core features > Sign in`
- [ ] `C-CF-09` `constraint` The limited attempt is refused even with the right password `src: Core features > Sign in`
- [ ] `C-CF-10` `contract` The limited attempt carries a retry_after number of seconds `src: Core features > Sign in`
- [ ] `C-CF-11` `capability` A successful sign in does not count towards the limit `src: Core features > Sign in`
- [ ] `C-CF-12` `ui` A limited sign in form shows `Too many for now. Try again in a little while.` `src: Core features > Sign in`
- [ ] `C-CF-13` `ui` The limited sign in submit stays unavailable until the wait is over `src: Core features > Sign in`
- [ ] `C-CF-14` `ui` The sign in layer carries an `Apply to join` link `src: Core features > Sign in`
- [ ] `C-CF-15` `ui` After signing in a creator lands on the profile editor `src: Core features > Sign in`
- [ ] `C-CF-16` `ui` After signing in a curator lands on the review queue `src: Core features > Sign in`
- [ ] `C-CF-17` `capability` A next path beginning with two slashes is ignored after sign in `src: Core features > Sign in`
- [ ] `C-CF-18` `contract` GET /api/me returns the caller's email, name, role, verified flag, profile slug `src: Core features > Sign in`
- [ ] `C-CF-19` `contract` GET /api/site returns the headline, the mission line, the divisions, the disciplines `src: Core features > Divisions, disciplines and addresses`
- [ ] `C-CF-20` `literal` Creator Media carries slug `creator-media` with colour token `red` `src: Core features > Divisions, disciplines and addresses`
- [ ] `C-CF-21` `literal` Creator Communities carries slug `creator-communities` with colour token `green` `src: Core features > Divisions, disciplines and addresses`
- [ ] `C-CF-22` `literal` Creator Products carries slug `creator-products` with colour token `blue` `src: Core features > Divisions, disciplines and addresses`
- [ ] `C-CF-23` `literal` Creator Tech carries slug `creator-tech` with colour token `yellow` `src: Core features > Divisions, disciplines and addresses`
- [ ] `C-CF-24` `constraint` No endpoint accepts a colour token `src: Core features > Divisions, disciplines and addresses`
- [ ] `C-CF-25` `capability` The twelve disciplines are served in the stated order `src: Core features > Divisions, disciplines and addresses`
- [ ] `C-CF-26` `literal` The discipline slug `partnerships` exists in the vocabulary `src: Core features > Divisions, disciplines and addresses`
- [ ] `C-CF-27` `capability` The front door always opens with the armillary at rest on the first segment `src: Core features > Divisions, disciplines and addresses`
- [ ] `C-CF-28` `ui` The bar is never rebuilt when the route changes `src: Core features > Global chrome`
- [ ] `C-CF-29` `ui` The wordmark inverts against whatever sits behind the wordmark `src: Core features > Global chrome`
- [ ] `C-CF-30` `ui` The menu control inverts against its background `src: Core features > Global chrome`
- [ ] `C-CF-31` `capability` The wordmark carries the accessible name `Halden` `src: Core features > Global chrome`
- [ ] `C-CF-32` `ui` The clock shows `L.A`, `LDN`, `NYC` with 24-hour times `src: Core features > Global chrome`
- [ ] `C-CF-33` `ui` The three clock cities cycle through one slot `src: Core features > Global chrome`
- [ ] `C-CF-34` `ui` The menu control reads `Close` once the menu opens `src: Core features > Global chrome`
- [ ] `C-CF-35` `ui` The menu overlay lists six links in the stated order `src: Core features > Global chrome`
- [ ] `C-CF-36` `ui` Each division menu link carries a line in the division colour `src: Core features > Global chrome`
- [ ] `C-CF-37` `ui` Pointing at a menu link draws a hand-drawn stroke across the link `src: Core features > Global chrome`
- [ ] `C-CF-38` `ui` Escape closes the menu overlay `src: Core features > Global chrome`
- [ ] `C-CF-39` `ui` The menu marks the current division link as active `src: Core features > A division`
- [ ] `C-CF-40` `ui` The light or dark toggle stays above the open menu `src: Core features > Global chrome`
- [ ] `C-CF-41` `capability` The root element carries `data-mode` naming the current mode `src: Core features > Global chrome`
- [ ] `C-CF-42` `capability` The mode choice persists under the browser storage key `mode` `src: Core features > Global chrome`
- [ ] `C-CF-43` `capability` With nothing stored the mode follows the system colour-scheme preference `src: Core features > Global chrome`
- [ ] `C-CF-44` `capability` The footer carries five items on every route except the front door `src: Core features > Global chrome`
- [ ] `C-CF-45` `capability` The footer terms link opens `/legal/terms-and-conditions` `src: Core features > Global chrome`
- [ ] `C-CF-46` `capability` The consent card offers `Accept All` or `No thanks` `src: Core features > Global chrome`
- [ ] `C-CF-47` `capability` The consent answer persists under the browser storage key `consent` `src: Core features > Global chrome`
- [ ] `C-CF-48` `ui` An answered consent card does not return `src: Core features > Global chrome`
- [ ] `C-CF-49` `ui` Keyboard focus reaches the consent card first whenever the card shows `src: Core features > Global chrome`
- [ ] `C-CF-50` `ui` Transient messages appear in the banner at the foot of the window `src: Core features > Global chrome`
- [ ] `C-CF-51` `capability` Each page carries exactly one element marked `data-primary-action` `src: Core features > Global chrome`
- [ ] `C-CF-52` `capability` The front door primary action reads `About Us` `src: Core features > Global chrome`
- [ ] `C-CF-53` `ui` `Control+K` opens the command palette from every page `src: Core features > The command palette`
- [ ] `C-CF-54` `ui` `/find` opens the front door with the palette already open `src: Core features > The command palette`
- [ ] `C-CF-55` `ui` The palette lists the divisions, the roster, join us, live creators by name `src: Core features > The command palette`
- [ ] `C-CF-56` `ui` Enter opens the highlighted palette entry `src: Core features > The command palette`
- [ ] `C-CF-57` `capability` The palette never lists a profile that is not live `src: Core features > The command palette`
- [ ] `C-CF-58` `ui` The arrival screen shows a white ground with near-black type `src: Core features > The arrival screen and the page transition`
- [ ] `C-CF-59` `ui` The Halden lettering draws in three passes on the arrival screen `src: Core features > The arrival screen and the page transition`
- [ ] `C-CF-60` `capability` The arrival counter reports real loading progress rather than a timed animation `src: Core features > The arrival screen and the page transition`
- [ ] `C-CF-61` `capability` A stalled arrival offers `Continue without the scene` after twenty seconds `src: Core features > The arrival screen and the page transition`
- [ ] `C-CF-62` `capability` The root element carries `data-arrival` set to `done` once the site is usable `src: Core features > The arrival screen and the page transition`
- [ ] `C-CF-63` `ui` Choosing a division never produces a white flash `src: Core features > The arrival screen and the page transition`
- [ ] `C-CF-64` `ui` The incoming division route opens at its top `src: Core features > The arrival screen and the page transition`
- [ ] `C-CF-65` `capability` The front door is exactly one window tall at every window size `src: Core features > The front door and the armillary`
- [ ] `C-CF-66` `ui` The front door carries no picture, video, logo wall or statistic `src: Core features > The front door and the armillary`
- [ ] `C-CF-67` `capability` The headline accessible name is the single sentence `The Operating System for the Creator Economy` `src: Core features > The front door and the armillary`
- [ ] `C-CF-68` `ui` The armillary shows four concentric rings around a glossy black sphere `src: Core features > The front door and the armillary`
- [ ] `C-CF-69` `capability` The armillary region carries `data-acquired` naming the acquired division `src: Core features > The front door and the armillary`
- [ ] `C-CF-70` `capability` The right arrow key steps the armillary one segment `src: Core features > The front door and the armillary`
- [ ] `C-CF-71` `capability` The armillary step wraps from the fourth division back to the first `src: Core features > The front door and the armillary`
- [ ] `C-CF-72` `capability` Enter on the focused armillary opens the acquired division route `src: Core features > The front door and the armillary`
- [ ] `C-CF-73` `ui` Dragging the object turns the armillary, then settles onto the nearest segment `src: Core features > The front door and the armillary`
- [ ] `C-CF-74` `ui` A wheel event moves the acquired segment `src: Core features > The front door and the armillary`
- [ ] `C-CF-75` `ui` The Next division control steps the object one segment `src: Core features > The front door and the armillary`
- [ ] `C-CF-76` `capability` Without three-dimensional rendering the front door falls back to a list of the four division names `src: Core features > The front door and the armillary`
- [ ] `C-CF-77` `capability` The fallback list still steps with the arrow keys `src: Core features > The front door and the armillary`
- [ ] `C-CF-78` `ui` The intro dispersion converges before the object settles `src: Core features > The front door and the armillary`
- [ ] `C-CF-79` `ui` A narrow viewport shows `Tap a section of our ecosystem to navigate.` beneath the object `src: Core features > The front door and the armillary`
- [ ] `C-CF-80` `contract` GET /api/divisions/{slug} returns the division with a roster of live profiles `src: Core features > A division`
- [ ] `C-CF-81` `constraint` An unknown division slug answers `404` with `not_found` `src: Core features > A division`
- [ ] `C-CF-82` `capability` A division roster accepts a discipline filter `src: Core features > A division`
- [ ] `C-CF-83` `literal` The Creator Media proposition reads `The new media empires will start with a person.` `src: Core features > A division`
- [ ] `C-CF-84` `literal` The Creator Media kicker reads `PEOPLE ARE THE PLATFORM` `src: Core features > A division`
- [ ] `C-CF-85` `literal` The Creator Communities proposition reads `Audiences become communities when somebody gives them a home.` `src: Core features > A division`
- [ ] `C-CF-86` `literal` The Creator Communities kicker reads `BELONGING AT SCALE` `src: Core features > A division`
- [ ] `C-CF-87` `literal` The Creator Products proposition reads `The best products start with the people who already use them.` `src: Core features > A division`
- [ ] `C-CF-88` `literal` The Creator Products kicker reads `MADE WITH CREATORS` `src: Core features > A division`
- [ ] `C-CF-89` `literal` The Creator Tech proposition reads `We build the engine that powers the person.` `src: Core features > A division`
- [ ] `C-CF-90` `literal` The Creator Tech kicker reads `ENGINEERING THE ECOSYSTEM` `src: Core features > A division`
- [ ] `C-CF-91` `literal` The Creator Media roster heading reads `The people behind the platform` `src: Core features > A division`
- [ ] `C-CF-92` `literal` The Creator Communities roster heading reads `The people who host them` `src: Core features > A division`
- [ ] `C-CF-93` `literal` The mission line reads `Our purpose is to shorten the road back to human.` `src: Core features > A division`
- [ ] `C-CF-94` `capability` Creator Tech lists four named products with name, tagline, address, pills `src: Core features > A division`
- [ ] `C-CF-95` `literal` Signal Desk carries the tagline `Less Noise, Better Work.` `src: Core features > A division`
- [ ] `C-CF-96` `ui` Each division route renders the template blocks in the stated order `src: Core features > A division`
- [ ] `C-CF-97` `ui` The tool box on Creator Tech shows each product with a Visit Site link `src: Core features > A division`
- [ ] `C-CF-98` `ui` Roster cards show the portrait, the name, the division line, discipline pills `src: Core features > A division`
- [ ] `C-CF-99` `capability` Each roster card links to the creator profile `src: Core features > A division`
- [ ] `C-CF-100` `capability` Each roster card carries `data-division` set to the division slug `src: Core features > A division`
- [ ] `C-CF-101` `ui` Pointing at a roster card lifts the card `src: Core features > A division`
- [ ] `C-CF-102` `ui` The roster grid runs three columns with the middle column set lower `src: Core features > A division`
- [ ] `C-CF-103` `ui` An empty division roster shows `Nobody here yet.` `src: Core features > A division`
- [ ] `C-CF-104` `ui` A division scene renders behind the content, driven by scroll `src: Core features > A division`
- [ ] `C-CF-105` `capability` `SKETCH MODE` switches `data-sketch` on the root element `src: Core features > Sketch mode`
- [ ] `C-CF-106` `capability` The sketch choice persists under the browser storage key `sketch` `src: Core features > Sketch mode`
- [ ] `C-CF-107` `capability` Sketch mode keeps every string identical `src: Core features > Sketch mode`
- [ ] `C-CF-108` `ui` Sketch mode re-sets headings in the hand-drawn lettering face `src: Core features > Sketch mode`
- [ ] `C-CF-109` `ui` Sketch mode replaces each scene with line art `src: Core features > Sketch mode`
- [ ] `C-CF-110` `contract` GET /api/profiles returns total, page, items `src: Core features > The roster`
- [ ] `C-CF-111` `constraint` A roster page carries at most 24 profile summaries `src: Core features > The roster`
- [ ] `C-CF-112` `contract` A profile summary carries slug, name, division, division name, colour token, disciplines, portrait address, position `src: Core features > The roster`
- [ ] `C-CF-113` `constraint` Public reads list a profile only when the profile is live `src: Core features > The roster`
- [ ] `C-CF-114` `capability` A division filter combined with a discipline filter intersects `src: Core features > The roster`
- [ ] `C-CF-115` `capability` A filter combination matching nobody answers total zero with empty items `src: Core features > The roster`
- [ ] `C-CF-116` `capability` Free text matches the statement of a profile `src: Core features > The roster`
- [ ] `C-CF-117` `capability` A name prefix match ranks above a name substring match `src: Core features > The roster`
- [ ] `C-CF-118` `constraint` Free text under two characters is ignored `src: Core features > The roster`
- [ ] `C-CF-119` `constraint` Free text over sixty characters is refused with `400` `src: Core features > The roster`
- [ ] `C-CF-120` `capability` Curated order follows position ascending by default `src: Core features > The roster`
- [ ] `C-CF-121` `capability` Name order sorts profiles alphabetically `src: Core features > The roster`
- [ ] `C-CF-122` `capability` Newest order sorts by publication time descending `src: Core features > The roster`
- [ ] `C-CF-123` `capability` A curator narrows the list by state `src: Core features > The roster`
- [ ] `C-CF-124` `ui` The roster page carries the heading `The roster` above a count line `src: Core features > The roster`
- [ ] `C-CF-125` `ui` Every roster filter lives in the address `src: Core features > The roster`
- [ ] `C-CF-126` `ui` A selected division filter value takes the division colour `src: Core features > The roster`
- [ ] `C-CF-127` `ui` Roster search settles after the last keystroke `src: Core features > The roster`
- [ ] `C-CF-128` `ui` A matched search run of text shows heavier than the text around the match `src: Core features > The roster`
- [ ] `C-CF-129` `ui` Filters matching nobody show `Nothing here.` with `Clear filters` `src: Core features > The roster`
- [ ] `C-CF-130` `ui` `Clear filters` resets every filter parameter `src: Core features > The roster`
- [ ] `C-CF-131` `ui` A roster card shows the division name in uppercase in the division colour `src: Core features > The roster`
- [ ] `C-CF-132` `contract` GET /api/profiles/{slug} returns statement, links, credits, publication time `src: Core features > A creator profile`
- [ ] `C-CF-133` `constraint` A not-live slug answers `404` exactly like an unknown slug `src: Core features > A creator profile`
- [ ] `C-CF-134` `constraint` A not-live profile answers `404` for a curator too `src: Core features > A creator profile`
- [ ] `C-CF-135` `ui` The profile page shows the portrait, name, division, pills, statement, links, credits in order `src: Core features > A creator profile`
- [ ] `C-CF-136` `ui` The profile division name links to the roster filtered by division `src: Core features > A creator profile`
- [ ] `C-CF-137` `ui` Each profile link sits beside a fixed mark `src: Core features > A creator profile`
- [ ] `C-CF-138` `literal` The link kinds are `site`, `photo`, `network`, `social`, `audio`, `document` `src: Core features > A creator profile`
- [ ] `C-CF-139` `capability` A portrait that fails to load shows a generated still with the initials `src: Core features > A creator profile`
- [ ] `C-CF-140` `ui` A not-live profile address shows `Not here.` `src: Core features > A creator profile`
- [ ] `C-CF-141` `ui` The owner sees an edit control on the owner's profile `src: Core features > A creator profile`
- [ ] `C-CF-142` `ui` A returned profile pins the curator note above the name for the owner `src: Core features > A creator profile`
- [ ] `C-CF-143` `ui` A curator sees `Take down` on a live profile `src: Core features > A creator profile`
- [ ] `C-CF-144` `ui` The join-us page shows four division controls in their own colours `src: Core features > Join us and the application`
- [ ] `C-CF-145` `ui` The application opens as a slide-over panel over the join-us page `src: Core features > Join us and the application`
- [ ] `C-CF-146` `ui` A division control opens the application with the division chosen `src: Core features > Join us and the application`
- [ ] `C-CF-147` `ui` Escape closes the application panel keeping the typed values `src: Core features > Join us and the application`
- [ ] `C-CF-148` `contract` POST /api/applications answers `201` with the account, the profile `src: Core features > Join us and the application`
- [ ] `C-CF-149` `data` An application stores one creator account with an unconfirmed address `src: Core features > Join us and the application`
- [ ] `C-CF-150` `data` An application stores one profile in state applying owned by the new account `src: Core features > Join us and the application`
- [ ] `C-CF-151` `capability` An invalid application answers `400` with a message for every field at fault `src: Core features > Join us and the application`
- [ ] `C-CF-152` `constraint` An invalid application creates no account, no profile, no mail `src: Core features > Join us and the application`
- [ ] `C-CF-153` `literal` A short name returns `Give us your name.` `src: Core features > Join us and the application`
- [ ] `C-CF-154` `literal` A short statement returns `Eighty characters at least. Tell us what you do.` `src: Core features > Join us and the application`
- [ ] `C-CF-155` `literal` A short password returns `Passwords are at least twelve characters.` `src: Core features > Join us and the application`
- [ ] `C-CF-156` `literal` A malformed email returns `That address does not look right.` `src: Core features > Join us and the application`
- [ ] `C-CF-157` `literal` Missing links return `Give us one place to see your work.` `src: Core features > Join us and the application`
- [ ] `C-CF-158` `literal` An unknown division returns `Pick a part of the ecosystem.` `src: Core features > Join us and the application`
- [ ] `C-CF-159` `constraint` Five disciplines in an application are refused `src: Core features > Join us and the application`
- [ ] `C-CF-160` `constraint` An application without consent is refused `src: Core features > Join us and the application`
- [ ] `C-CF-161` `constraint` An already registered email answers `409` with `conflict` `src: Core features > Join us and the application`
- [ ] `C-CF-162` `literal` The duplicate refusal reads `That address already has an account.` `src: Core features > Join us and the application`
- [ ] `C-CF-163` `constraint` Application emails compare without regard to case `src: Core features > Join us and the application`
- [ ] `C-CF-164` `constraint` Two simultaneous applications with one email leave exactly one account `src: Core features > Join us and the application`
- [ ] `C-CF-165` `ui` A successful application shows the full-page confirmation `Check your email.` `src: Core features > Join us and the application`
- [ ] `C-CF-166` `capability` Typed application values persist under `application_draft` until success `src: Core features > Join us and the application`
- [ ] `C-CF-167` `capability` A slug derives from the name in lowercase with hyphens `src: Core features > Join us and the application`
- [ ] `C-CF-168` `capability` A colliding slug gains a `-2` suffix `src: Core features > Join us and the application`
- [ ] `C-CF-169` `constraint` No request sets a slug `src: Core features > Join us and the application`
- [ ] `C-CF-170` `capability` A successful application mails `Confirm your address` to the applicant `src: Core features > Confirming the address`
- [ ] `C-CF-171` `capability` The confirmation mail body opens with the confirmation link `src: Core features > Confirming the address`
- [ ] `C-CF-172` `capability` The confirmation mail names the applicant `src: Core features > Confirming the address`
- [ ] `C-CF-173` `contract` POST /api/accounts/verifications answers `204` for a valid token `src: Core features > Confirming the address`
- [ ] `C-CF-174` `data` Confirming the address stores the confirmation time `src: Core features > Confirming the address`
- [ ] `C-CF-175` `data` Confirming the address moves an applying profile to draft `src: Core features > Confirming the address`
- [ ] `C-CF-176` `constraint` A used confirmation token answers `410` `src: Core features > Confirming the address`
- [ ] `C-CF-177` `constraint` An unknown confirmation token answers `400` `src: Core features > Confirming the address`
- [ ] `C-CF-178` `ui` A used confirmation link page reads `That link no longer works.` `src: Core features > Confirming the address`
- [ ] `C-CF-179` `ui` The confirmation link opens the editor with the banner `ADDRESS CONFIRMED` `src: Core features > Confirming the address`
- [ ] `C-CF-180` `capability` An unconfirmed creator signs in to edit the creator's own profile `src: Core features > Confirming the address`
- [ ] `C-CF-181` `contract` GET /api/me/profile returns the caller's own profile with pending, version `src: Core features > The profile editor`
- [ ] `C-CF-182` `constraint` An account with no profile answers `404` from the own-profile endpoint `src: Core features > The profile editor`
- [ ] `C-CF-183` `contract` PATCH /api/me/profile saves name, statement, portrait address, division against a version `src: Core features > The profile editor`
- [ ] `C-CF-184` `capability` Discipline, link, credit lists are replaced whole `src: Core features > The profile editor`
- [ ] `C-CF-185` `data` Every successful profile write raises the version by one `src: Core features > The profile editor`
- [ ] `C-CF-186` `constraint` A write carrying an older version answers `409` with `version_conflict` `src: Core features > The profile editor`
- [ ] `C-CF-187` `constraint` A stale write changes nothing stored `src: Core features > The profile editor`
- [ ] `C-CF-188` `constraint` A portrait address outside the portraits origin is refused with `We need a picture.` `src: Core features > The profile editor`
- [ ] `C-CF-189` `constraint` A link with a script scheme is refused with `That link does not look right.` `src: Core features > The profile editor`
- [ ] `C-CF-190` `constraint` A sixth link is refused `src: Core features > The profile editor`
- [ ] `C-CF-191` `constraint` A credit over eighty characters is refused `src: Core features > The profile editor`
- [ ] `C-CF-192` `constraint` A statement over four hundred characters is refused `src: Core features > The profile editor`
- [ ] `C-CF-193` `constraint` A refused profile value is not stored `src: Core features > The profile editor`
- [ ] `C-CF-194` `constraint` Editor writes on a submitted profile answer `422` with `state_not_allowed` `src: Core features > The profile editor`
- [ ] `C-CF-195` `ui` The editor shows the field column beside a live preview `src: Core features > The profile editor`
- [ ] `C-CF-196` `capability` The live preview updates as the creator types `src: Core features > The profile editor`
- [ ] `C-CF-197` `ui` A field saves on blur with the banner `SAVED` `src: Core features > The profile editor`
- [ ] `C-CF-198` `ui` The editor carries no save control `src: Core features > The profile editor`
- [ ] `C-CF-199` `ui` Adding a link opens a small slide-over `src: Core features > The profile editor`
- [ ] `C-CF-200` `capability` Typed editor text survives a reload before the field is left `src: Core features > The profile editor`
- [ ] `C-CF-201` `ui` The own entry page shows the entry state in words `src: Core features > The profile editor`
- [ ] `C-CF-202` `contract` A transition to submitted moves a complete profile to submitted `src: Core features > Submitting for review`
- [ ] `C-CF-203` `data` A submission stores the submission time `src: Core features > Submitting for review`
- [ ] `C-CF-204` `constraint` An unconfirmed creator submission answers `403` with `not_verified` `src: Core features > Submitting for review`
- [ ] `C-CF-205` `literal` The unconfirmed refusal reads `Confirm your address first.` `src: Core features > Submitting for review`
- [ ] `C-CF-206` `capability` A failing submission answers `422` naming every failing field `src: Core features > Submitting for review`
- [ ] `C-CF-207` `constraint` A failing submission changes no state `src: Core features > Submitting for review`
- [ ] `C-CF-208` `literal` A missing portrait returns `We need a picture.` `src: Core features > Submitting for review`
- [ ] `C-CF-209` `capability` A statement containing `INSERT NAME` trips the placeholder rule `src: Core features > Submitting for review`
- [ ] `C-CF-210` `capability` A credit reading `Pill Text` trips the placeholder rule `src: Core features > Submitting for review`
- [ ] `C-CF-211` `capability` `TODO` as a whole word trips the placeholder rule `src: Core features > Submitting for review`
- [ ] `C-CF-212` `constraint` A name holding those letters inside a longer word does not trip the placeholder rule `src: Core features > Submitting for review`
- [ ] `C-CF-213` `contract` The placeholder refusal lists the fields under meta placeholder_fields `src: Core features > Submitting for review`
- [ ] `C-CF-214` `literal` The placeholder message reads `Something in there is still a placeholder.` `src: Core features > Submitting for review`
- [ ] `C-CF-215` `ui` A failing submission shows every failure as a numbered list `src: Core features > Submitting for review`
- [ ] `C-CF-216` `ui` A successful submission shows the full-page confirmation `WITH THE STUDIO` `src: Core features > Submitting for review`
- [ ] `C-CF-217` `ui` The submitted editor is read-only `src: Core features > Submitting for review`
- [ ] `C-CF-218` `constraint` A submission sends no mail `src: Core features > Submitting for review`
- [ ] `C-CF-219` `ui` The review queue is a split view with the list beside the selected preview `src: Core features > The review queue`
- [ ] `C-CF-220` `capability` The review queue lists the oldest submission first `src: Core features > The review queue`
- [ ] `C-CF-221` `constraint` A creator calling the studio transition route answers `403` with `not_authorised` `src: Core features > The review queue`
- [ ] `C-CF-222` `constraint` An anonymous studio transition answers `401` `src: Core features > The review queue`
- [ ] `C-CF-223` `capability` Publishing a submitted profile makes the profile live at once `src: Core features > The review queue`
- [ ] `C-CF-224` `data` Publishing records the reviewing curator `src: Core features > The review queue`
- [ ] `C-CF-225` `data` Publishing sets the first publication time once `src: Core features > The review queue`
- [ ] `C-CF-226` `capability` A first publication takes the next curated position `src: Core features > The review queue`
- [ ] `C-CF-227` `capability` Sending back with a note moves the profile to changes requested `src: Core features > The review queue`
- [ ] `C-CF-228` `data` Sending back stores the note with the return time `src: Core features > The review queue`
- [ ] `C-CF-229` `constraint` A note under ten characters is refused with `Say what needs changing.` `src: Core features > The review queue`
- [ ] `C-CF-230` `constraint` A note over five hundred characters is refused `src: Core features > The review queue`
- [ ] `C-CF-231` `ui` Send back opens a slide-over holding one Note field `src: Core features > The review queue`
- [ ] `C-CF-232` `capability` Taking a published profile down removes the profile from every public surface `src: Core features > The review queue`
- [ ] `C-CF-233` `data` Taking down stores state unpublished with the live flag off `src: Core features > The review queue`
- [ ] `C-CF-234` `capability` An owner edit after a take down returns the profile to draft `src: Core features > The review queue`
- [ ] `C-CF-235` `constraint` Publishing a draft answers `422` with `state_not_allowed` `src: Core features > The review queue`
- [ ] `C-CF-236` `constraint` A second publish carrying the old version answers `409` `src: Core features > The review queue`
- [ ] `C-CF-237` `capability` A curator moves a profile to another division at once `src: Core features > The review queue`
- [ ] `C-CF-238` `data` A curator move records a moved event `src: Core features > The review queue`
- [ ] `C-CF-239` `constraint` The curator move route refuses a statement change with `403` `src: Core features > The review queue`
- [ ] `C-CF-240` `capability` The curated order is replaced from the complete list of live slugs `src: Core features > The review queue`
- [ ] `C-CF-241` `constraint` An incomplete order list is refused with nothing changed `src: Core features > The review queue`
- [ ] `C-CF-242` `ui` Moving a profile shows the banner `MOVED` `src: Core features > The review queue`
- [ ] `C-CF-243` `ui` Reordering the roster shows the banner `ORDER SAVED` `src: Core features > The review queue`
- [ ] `C-CF-244` `ui` Taking a profile down shows the banner `TAKEN DOWN` `src: Core features > The review queue`
- [ ] `C-CF-245` `capability` An owner edit to a live profile is held as pending `src: Core features > Rewriting a live profile`
- [ ] `C-CF-246` `capability` Public surfaces keep the live copy until the change is published `src: Core features > Rewriting a live profile`
- [ ] `C-CF-247` `capability` Publishing changes copies pending over the live copy without review `src: Core features > Rewriting a live profile`
- [ ] `C-CF-248` `constraint` An owner publishing own changes sends no mail `src: Core features > Rewriting a live profile`
- [ ] `C-CF-249` `constraint` Publishing with nothing pending answers `422` `src: Core features > Rewriting a live profile`
- [ ] `C-CF-250` `ui` Publishing changes shows the full-page confirmation `PUBLISHED` `src: Core features > Rewriting a live profile`
- [ ] `C-CF-251` `ui` The publication control reads `Publish changes` for an unchanged division `src: Core features > Rewriting a live profile`
- [ ] `C-CF-252` `capability` A published slug never changes `src: Core features > Rewriting a live profile`
- [ ] `C-CF-253` `constraint` An owner publish of a division change answers `422` `src: Core features > Moving to a different division`
- [ ] `C-CF-254` `capability` Sending a division change for review keeps the profile live on the old division `src: Core features > Moving to a different division`
- [ ] `C-CF-255` `capability` Publishing the division change lists the profile on the new division route `src: Core features > Moving to a different division`
- [ ] `C-CF-256` `capability` The moved profile leaves the old division roster `src: Core features > Moving to a different division`
- [ ] `C-CF-257` `data` The division change records a moved event naming both divisions `src: Core features > Moving to a different division`
- [ ] `C-CF-258` `ui` The publication control reads `Send changes for review` for a new division `src: Core features > Moving to a different division`
- [ ] `C-CF-259` `ui` The moved roster card shows the new division colour `src: Core features > Moving to a different division`
- [ ] `C-CF-260` `capability` Sending back mails `Your entry needs a change` carrying the note `src: Core features > Mail`
- [ ] `C-CF-261` `capability` Publishing mails `You are on the roster` with the profile address `src: Core features > Mail`
- [ ] `C-CF-262` `capability` Taking down mails `Your entry has been taken down` `src: Core features > Mail`
- [ ] `C-CF-263` `constraint` Mail goes only to the owner account email `src: Core features > Mail`
- [ ] `C-CF-264` `constraint` No mail ever goes to a curator `src: Core features > Mail`
- [ ] `C-CF-265` `constraint` A curator moving a profile sends no mail `src: Core features > Mail`
- [ ] `C-CF-266` `ui` The about page lists the four divisions with their propositions `src: Core features > About, legal notices, sitemap and robots`
- [ ] `C-CF-267` `contract` GET /api/notices/{kind} returns a title with a non-empty body `src: Core features > About, legal notices, sitemap and robots`
- [ ] `C-CF-268` `literal` The terms notice title reads `Terms & Conditions` `src: Core features > About, legal notices, sitemap and robots`
- [ ] `C-CF-269` `ui` Each notice page shows a last-updated line above a contents list `src: Core features > About, legal notices, sitemap and robots`
- [ ] `C-CF-270` `capability` `/sitemap.xml` lists every live profile address `src: Core features > About, legal notices, sitemap and robots`
- [ ] `C-CF-271` `constraint` `/sitemap.xml` omits every profile that is not live `src: Core features > About, legal notices, sitemap and robots`
- [ ] `C-CF-272` `capability` `/robots.txt` names the sitemap `src: Core features > About, legal notices, sitemap and robots`
- [ ] `C-CF-273` `capability` `/robots.txt` disallows the signed-in routes `src: Core features > About, legal notices, sitemap and robots`
- [ ] `C-CF-274` `contract` POST /api/events answers `204` for a closed event name `src: Core features > Consent and site events`
- [ ] `C-CF-275` `constraint` An unknown event name is refused with `400` `src: Core features > Consent and site events`
- [ ] `C-CF-276` `constraint` After `No thanks` the browser records no site event `src: Core features > Consent and site events`
- [ ] `C-CF-277` `capability` After `Accept All` the browser records site events `src: Core features > Consent and site events`

## C-UF User flow

- [ ] `C-UF-01` `ui` A signed-out visitor opening the own entry page is sent to sign in, then returned `src: User flow > Entry and redirects`
- [ ] `C-UF-02` `ui` A curator opening the profile editor sees `Not for you` `src: User flow > Entry and redirects`
- [ ] `C-UF-03` `ui` A creator opening the review queue address sees the live roster `src: User flow > Entry and redirects`
- [ ] `C-UF-04` `ui` An unknown address shows `Not here.` with `See the roster` `src: User flow > Entry and redirects`
- [ ] `C-UF-05` `ui` Opening the application as a creator with a profile opens the editor `src: User flow > Entry and redirects`
- [ ] `C-UF-06` `ui` A visitor enters a division through the armillary `src: User flow > Journeys`
- [ ] `C-UF-07` `ui` A visitor finds a creator through the command palette `src: User flow > Journeys`
- [ ] `C-UF-08` `ui` A curator publishes a resubmitted profile from the review queue `src: User flow > Journeys`
- [ ] `C-UF-09` `capability` A fresh visitor with no session sees the published profile on the division roster `src: User flow > Journeys`
- [ ] `C-UF-10` `ui` Loading keeps the space of the content without shimmer `src: User flow > States`
- [ ] `C-UF-11` `ui` An empty or failed collection shows one centred notice with at most one control `src: User flow > States`
- [ ] `C-UF-12` `capability` A refused form keeps every value with focus on the first field at fault `src: User flow > States`
- [ ] `C-UF-13` `capability` A submit control stays available on an incomplete form `src: User flow > States`
- [ ] `C-UF-14` `capability` Validation never runs on a keystroke `src: User flow > States`
- [ ] `C-UF-15` `ui` A failure surface never shows a status code or an error token `src: User flow > States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The ground is a near-black neutral on every route `src: UI/UX notes`
- [ ] `C-UX-02` `ui` One mid neutral grey carries the sentences a visitor reads `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The four division colours appear only in their division roles `src: UI/UX notes`
- [ ] `C-UX-04` `ui` The darker neutral never carries readable text `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Light mode swaps the ground with the text so every surface stays legible `src: UI/UX notes`
- [ ] `C-UX-06` `ui` A condensed display face in capitals sets the headline with every division title `src: UI/UX notes`
- [ ] `C-UX-07` `ui` The hand-drawn face appears only for sketch mode `src: UI/UX notes`
- [ ] `C-UX-08` `ui` No shadow or border appears anywhere `src: UI/UX notes`
- [ ] `C-UX-09` `ui` A field is an underline rather than a box `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Pointing at a pill grows a filled ellipse from the centre `src: UI/UX notes`
- [ ] `C-UX-11` `ui` A heading rises line by line on a short stagger `src: UI/UX notes`
- [ ] `C-UX-12` `ui` A link text colour changes before the mark beside the link `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Reduced motion gives every moment a substitute that arrives without travelling `src: UI/UX notes`
- [ ] `C-UX-14` `ui` Text contrast meets WCAG AA in both modes `src: UI/UX notes`
- [ ] `C-UX-15` `ui` Focus is outlined visibly in the text colour `src: UI/UX notes`
- [ ] `C-UX-16` `ui` No interactive target is smaller than 44 CSS pixels `src: UI/UX notes`
- [ ] `C-UX-17` `ui` Each route carries one first-level heading `src: UI/UX notes`
- [ ] `C-UX-18` `ui` Focus is held inside an open menu until the menu closes `src: UI/UX notes`
- [ ] `C-UX-19` `ui` The roster grid runs three, two, one columns keeping the offset `src: UI/UX notes`
- [ ] `C-UX-20` `ui` On a narrow viewport the clock moves into the menu overlay `src: UI/UX notes`
- [ ] `C-UX-21` `ui` The armillary is never hidden because of window size `src: UI/UX notes`
- [ ] `C-UX-22` `ui` No page is dominated by a single colour family `src: UI/UX notes`
- [ ] `C-UX-23` `capability` Nothing scrolls sideways at a narrow viewport `src: UI/UX notes`
- [ ] `C-UX-24` `ui` The editor wears the same type, ground, spacing as the public site `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` Every error answers JSON with error, message, fields, meta, retry_after `src: Technical requirements`
- [ ] `C-TR-02` `capability` Health answers `200` reporting the database apart from the mail server `src: Technical requirements`
- [ ] `C-TR-03` `constraint` A refused application writes neither an account nor a profile `src: Technical requirements`
- [ ] `C-TR-04` `constraint` Two profiles named alike at one instant never share a slug `src: Technical requirements`
- [ ] `C-TR-05` `capability` Markup typed into a name renders as visible text `src: Technical requirements`
- [ ] `C-TR-06` `capability` Every response carries `X-Frame-Options: DENY` `src: Technical requirements`
- [ ] `C-TR-07` `capability` Every response carries `X-Content-Type-Options: nosniff` `src: Technical requirements`
- [ ] `C-TR-08` `capability` Every response carries `Referrer-Policy: same-origin` `src: Technical requirements`
- [ ] `C-TR-09` `capability` Every response carries a Strict-Transport-Security header with includeSubDomains `src: Technical requirements`
- [ ] `C-TR-10` `constraint` No database address or signing secret appears in the browser bundle `src: Technical requirements`
- [ ] `C-TR-11` `capability` Relative times read as whole minutes, hours or days `src: Technical requirements`
- [ ] `C-TR-12` `capability` Absolute dates read as day, month name, year `src: Technical requirements`
- [ ] `C-TR-13` `capability` Stored times return in UTC as ISO 8601 `src: Technical requirements`
- [ ] `C-TR-14` `constraint` Mail is delivered over SMTP to Mailpit `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Each seeded account exists exactly once with a confirmed address `src: Data model`
- [ ] `C-DM-02` `data` Exactly four divisions exist with unique colour tokens `src: Data model`
- [ ] `C-DM-03` `data` Twelve disciplines exist `src: Data model`
- [ ] `C-DM-04` `data` Ten seeded profiles are live in state published `src: Data model`
- [ ] `C-DM-05` `data` The draft `ada-moreau` is stored with the live flag off `src: Data model`
- [ ] `C-DM-06` `data` Every live position is unique `src: Data model`
- [ ] `C-DM-07` `data` Profile events are appended for application, submission, return, publication, take down, move `src: Data model`
- [ ] `C-DM-08` `data` Site events are stored only for a consenting browser `src: Data model`
- [ ] `C-DM-09` `data` Three notices exist with non-empty bodies `src: Data model`
- [ ] `C-DM-10` `literal` Every seeded portrait address begins `https://media.example.com/portraits/` `src: Data model`
- [ ] `C-DM-11` `data` Each seeded row exists exactly once `src: Data model`
- [ ] `C-DM-12` `data` Account emails are stored lowercase `src: Data model`
- [ ] `C-DM-13` `literal` No live profile carries the discipline `partnerships` `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Every grey inverts with the mode `src: Front-end specification`
- [ ] `C-FE-02` `ui` One gradient fades the foot of each division scene into the ground `src: Front-end specification`
- [ ] `C-FE-03` `ui` Every mark takes the colour of the element holding the mark `src: Front-end specification`
- [ ] `C-FE-04` `ui` Interface marks are thin outlines on one small square `src: Front-end specification`
- [ ] `C-FE-05` `ui` Sketch lines are drawn on by their dash offset, never faded `src: Front-end specification`
- [ ] `C-FE-06` `ui` The clock slot slides between cities so the bar never reflows `src: Front-end specification`
- [ ] `C-FE-07` `ui` The consent card is the only rounded card in the product `src: Front-end specification`
- [ ] `C-FE-08` `ui` The armillary rings are dark brushed metal with a roll of light along each ring `src: Front-end specification`
- [ ] `C-FE-09` `ui` The centre sphere is high-gloss black glass reflecting the rings `src: Front-end specification`
- [ ] `C-FE-10` `ui` Creator Media shows a stack of thin discs as the division scene `src: Front-end specification`
- [ ] `C-FE-11` `ui` Creator Communities shows a ring of small spheres connected by fine rods `src: Front-end specification`
- [ ] `C-FE-12` `ui` Creator Products shows four nested rounded boxes `src: Front-end specification`
- [ ] `C-FE-13` `ui` Creator Tech shows a single sphere in the glass with a rippled displacement `src: Front-end specification`
- [ ] `C-FE-14` `ui` The roster grid middle column sits half a card lower `src: Front-end specification`
- [ ] `C-FE-15` `ui` A pending control replaces the label with a turning ring `src: Front-end specification`
- [ ] `C-FE-16` `ui` Slide-overs enter from the right edge over a dimmed page `src: Front-end specification`
- [ ] `C-FE-17` `ui` Skeleton blocks carry no shimmer or pulse `src: Front-end specification`
- [ ] `C-FE-18` `ui` A narrow profile page runs one column with the portrait full width `src: Front-end specification`
- [ ] `C-FE-19` `ui` The application slide-over runs full width on a narrow screen `src: Front-end specification`
- [ ] `C-FE-20` `ui` Legal pages use one centred reading column `src: Front-end specification`
- [ ] `C-FE-21` `capability` The front door fetches nothing from another origin `src: Front-end specification`
- [ ] `C-FE-22` `capability` Reordering by keyboard lifts a card with Space `src: Front-end specification`
- [ ] `C-FE-23` `ui` The arrival screen draws one red stroke across a resting grey stroke `src: Front-end specification`
- [ ] `C-FE-24` `ui` Focus order on the front door runs wordmark, menu control, toggle, primary control, armillary `src: Front-end specification`
- [ ] `C-FE-25` `ui` All four division names read in title case `src: Front-end specification`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` A statement is stored as plain text `src: Constraints`
- [ ] `C-CN-02` `constraint` The four divisions form a closed set `src: Constraints`
- [ ] `C-CN-03` `constraint` The six link kinds form a closed set `src: Constraints`
- [ ] `C-CN-04` `constraint` The ten site event names form a closed set `src: Constraints`
- [ ] `C-CN-05` `constraint` The browser opens no live update connection `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` The app answers at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `literal` The HTTP API is served under `/api` `src: Deployment contract`
- [ ] `C-DC-03` `literal` `GET /api/health` returns `200` `src: Deployment contract`
- [ ] `C-DC-04` `literal` Login credentials are written to `/app/USER_README.md` `src: Deployment contract`
- [ ] `C-DC-05` `literal` The reserved directory `.browser_screenshots/` exists empty `src: Deployment contract`
- [ ] `C-DC-06` `literal` The reserved directory `.downloads/` exists empty `src: Deployment contract`
- [ ] `C-DC-07` `constraint` Every studio route requires a bearer token `src: Deployment contract`
- [ ] `C-DC-08` `constraint` The roster list honours a state filter only with a curator token `src: Deployment contract`
- [ ] `C-DC-09` `capability` An invalid call is never answered as a server error `src: Deployment contract`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `curator@example.com` | a pinned value in the brief | `C-RL-17` | instruction.md |
| `creator@example.com` | a pinned value in the brief | `C-RL-18` | instruction.md |
| `juno-okafor` | a pinned value in the brief | `C-RL-18` | instruction.md |
| `creator2@example.com` | a pinned value in the brief | `C-RL-19` | instruction.md |
| `ada-moreau` | a pinned value in the brief | `C-RL-19` | instruction.md |
| `deku-demo-pw-2026` | a pinned value in the brief | `C-RL-20` | instruction.md |
| `not_authenticated` | a pinned value in the brief | `C-CF-06` | instruction.md |
| `429` | a pinned value in the brief | `C-CF-08` | instruction.md |
| `rate_limited` | a pinned value in the brief | `C-CF-08` | instruction.md |
| `creator-media` | a pinned value in the brief | `C-CF-20` | instruction.md |
| `red` | a pinned value in the brief | `C-CF-20` | instruction.md |
| `creator-communities` | a pinned value in the brief | `C-CF-21` | instruction.md |
| `green` | a pinned value in the brief | `C-CF-21` | instruction.md |
| `creator-products` | a pinned value in the brief | `C-CF-22` | instruction.md |
| `blue` | a pinned value in the brief | `C-CF-22` | instruction.md |
| `creator-tech` | a pinned value in the brief | `C-CF-23` | instruction.md |
| `yellow` | a pinned value in the brief | `C-CF-23` | instruction.md |
| `partnerships` | a pinned value in the brief | `C-CF-26` | instruction.md |
| `The new media empires will start with a person.` | a pinned value in the brief | `C-CF-83` | instruction.md |
| `PEOPLE ARE THE PLATFORM` | a pinned value in the brief | `C-CF-84` | instruction.md |
| `Audiences become communities when somebody gives them a home.` | a pinned value in the brief | `C-CF-85` | instruction.md |
| `BELONGING AT SCALE` | a pinned value in the brief | `C-CF-86` | instruction.md |
| `The best products start with the people who already use them.` | a pinned value in the brief | `C-CF-87` | instruction.md |
| `MADE WITH CREATORS` | a pinned value in the brief | `C-CF-88` | instruction.md |
| `We build the engine that powers the person.` | a pinned value in the brief | `C-CF-89` | instruction.md |
| `ENGINEERING THE ECOSYSTEM` | a pinned value in the brief | `C-CF-90` | instruction.md |
| `The people behind the platform` | a pinned value in the brief | `C-CF-91` | instruction.md |
| `The people who host them` | a pinned value in the brief | `C-CF-92` | instruction.md |
| `Our purpose is to shorten the road back to human.` | a pinned value in the brief | `C-CF-93` | instruction.md |
| `Less Noise, Better Work.` | a pinned value in the brief | `C-CF-95` | instruction.md |
| `site` | a pinned value in the brief | `C-CF-138` | instruction.md |
| `photo` | a pinned value in the brief | `C-CF-138` | instruction.md |
| `network` | a pinned value in the brief | `C-CF-138` | instruction.md |
| `social` | a pinned value in the brief | `C-CF-138` | instruction.md |
| `audio` | a pinned value in the brief | `C-CF-138` | instruction.md |
| `document` | a pinned value in the brief | `C-CF-138` | instruction.md |
| `Give us your name.` | a pinned value in the brief | `C-CF-153` | instruction.md |
| `Eighty characters at least. Tell us what you do.` | a pinned value in the brief | `C-CF-154` | instruction.md |
| `Passwords are at least twelve characters.` | a pinned value in the brief | `C-CF-155` | instruction.md |
| `That address does not look right.` | a pinned value in the brief | `C-CF-156` | instruction.md |
| `Give us one place to see your work.` | a pinned value in the brief | `C-CF-157` | instruction.md |
| `Pick a part of the ecosystem.` | a pinned value in the brief | `C-CF-158` | instruction.md |
| `That address already has an account.` | a pinned value in the brief | `C-CF-162` | instruction.md |
| `Confirm your address first.` | a pinned value in the brief | `C-CF-205` | instruction.md |
| `We need a picture.` | a pinned value in the brief | `C-CF-208` | instruction.md |
| `Something in there is still a placeholder.` | a pinned value in the brief | `C-CF-214` | instruction.md |
| `Terms & Conditions` | a pinned value in the brief | `C-CF-268` | instruction.md |
| `https://media.example.com/portraits/` | a pinned value in the brief | `C-DM-10` | instruction.md |
| `APP_PUBLIC_URL` | a pinned value in the brief | `C-DC-01` | instruction.md |
| `/api` | a pinned value in the brief | `C-DC-02` | instruction.md |
| `GET /api/health` | a pinned value in the brief | `C-DC-03` | instruction.md |
| `200` | a pinned value in the brief | `C-DC-03` | instruction.md |
| `/app/USER_README.md` | a pinned value in the brief | `C-DC-04` | instruction.md |
| `.browser_screenshots/` | a pinned value in the brief | `C-DC-05` | instruction.md |
| `.downloads/` | a pinned value in the brief | `C-DC-06` | instruction.md |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact shade behind each colour role and division colour | `C-UX-01` |
| the duration of the shared motion timing and the stagger interval | `C-UX-11` |
| the width at which each responsive range begins | `C-UX-19` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 3 | 8 |
| User roles | 4 | 20 |
| Core features | 72 | 277 |
| User flow | 11 | 15 |
| UI and UX notes | 4 | 24 |
| Technical requirements | 8 | 14 |
| Data model | 10 | 13 |
| Front-end specification | 20 | 25 |
| Constraints | 1 | 5 |
| Deployment contract | 8 | 9 |

## Declared but ungraded

| Obligation | Source | why |
|---|---|---|
| A field that fails to save keeps the value, marks the label in the error colour, then retries twice | Core features > The profile editor | why: a save failure cannot be induced from outside the app; the graders reach it only through HTTP, the database, the mail inbox and a browser that sees a working server |
| Losing the connection shows the banner OFFLINE, then BACK ONLINE when it returns | User flow > States | why: the graders cannot sever the network between the browser and the app for one step; the application and editor keeping values across a reload are graded instead |
| One log line per request never carries a password, token, statement or email address | Technical requirements | why: the app's standard output is not visible to any grader; nothing outside the container can read it |
| Assistive technology hears the polite and assertive announcements listed in the front-end specification | Front-end specification | why: live-region speech is not rendered on screen, so neither a page reader nor a sighted judge observes it; the one accessible sentence per heading is graded instead |
