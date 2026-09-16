# Checklist: Verdigris Studio

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 483
Unpinned values flagged: 2
## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public portfolio site for a brand design studio. `src: Overview, para 1`
- [ ] `C-OV-02` `capability` The app serves a booking surface for a strategic call. `src: Overview, para 2`
- [ ] `C-OV-03` `constraint` Booking a strategic call changes stored state. `src: Overview, para 2`
- [ ] `C-OV-04` `constraint` Submitting the enquiry form changes stored state. `src: Overview, para 2`
- [ ] `C-OV-05` `constraint` Every other public action reads published content only. `src: Overview, para 3`
- [ ] `C-OV-06` `data` The app renders published content from stored records. `src: Overview, para 3`
- [ ] `C-OV-07` `constraint` The app offers no cart. `src: Overview, para 4`
- [ ] `C-OV-08` `constraint` The app offers no comment surface. `src: Overview, para 4`
- [ ] `C-OV-09` `constraint` The app personalises no route to a visitor. `src: Overview, para 4`
- [ ] `C-OV-10` `constraint` One calendar slot yields at most one call. `src: Overview, para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` An anonymous visitor reads every published route. `src: User roles, table row 1`
- [ ] `C-RL-02` `role` An anonymous visitor submits the enquiry form. `src: User roles, table row 1`
- [ ] `C-RL-03` `role` An anonymous visitor reads the slot calendar. `src: User roles, table row 1`
- [ ] `C-RL-04` `constraint` An anonymous visitor cannot hold a slot. `src: User roles, table row 1`
- [ ] `C-RL-05` `constraint` An anonymous visitor cannot reach the console. `src: User roles, table row 1`
- [ ] `C-RL-06` `role` A client holds a slot on the calendar. `src: User roles, table row 2`
- [ ] `C-RL-07` `role` A client confirms a held call. `src: User roles, table row 2`
- [ ] `C-RL-08` `role` A client cancels a call the same client confirmed. `src: User roles, table row 2`
- [ ] `C-RL-09` `constraint` A client cannot read another client's booking. `src: User roles, table row 2`
- [ ] `C-RL-10` `constraint` A client cannot open a calendar slot. `src: User roles, table row 2`
- [ ] `C-RL-11` `constraint` A client cannot read a stored enquiry. `src: User roles, table row 2`
- [ ] `C-RL-12` `constraint` A client cannot publish a project. `src: User roles, table row 2`
- [ ] `C-RL-13` `role` The studio account opens a calendar slot. `src: User roles, table row 3`
- [ ] `C-RL-14` `role` The studio account closes a calendar slot. `src: User roles, table row 3`
- [ ] `C-RL-15` `role` The studio account reads every stored enquiry. `src: User roles, table row 3`
- [ ] `C-RL-16` `role` The studio account publishes a project. `src: User roles, table row 3`
- [ ] `C-RL-17` `constraint` The server rejects a client call to a studio endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-18` `constraint` A denied request leaves the protected row unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-19` `role` Signup creates an account holding the client role. `src: User roles, signup paragraph`
- [ ] `C-RL-20` `constraint` Signup never creates an account holding the studio role. `src: User roles, signup paragraph`
- [ ] `C-RL-21` `literal` The app seeds the studio account `studio@example.com`. `src: User roles, seeded accounts table row 1`
- [ ] `C-RL-22` `literal` The app seeds the client account `client@example.com`. `src: User roles, seeded accounts table row 2`
- [ ] `C-RL-23` `literal` The app seeds the client account `client2@example.com`. `src: User roles, seeded accounts table row 3`
- [ ] `C-RL-24` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles, seeded accounts paragraph`

## C-CF Core features

- [ ] `C-CF-01` `capability` Signup with an email plus a password returns a bearer token. `src: Core features, Auth and accounts rule 1`
- [ ] `C-CF-02` `constraint` A second signup with a stored address is rejected as invalid. `src: Core features, Auth and accounts rule 1`
- [ ] `C-CF-03` `constraint` A rejected signup creates no second account. `src: Core features, Auth and accounts rule 1`
- [ ] `C-CF-04` `constraint` A signup body naming the studio role still creates a client. `src: Core features, Auth and accounts rule 2`
- [ ] `C-CF-05` `capability` Login with a seeded address returns a bearer token. `src: Core features, Auth and accounts para 1`
- [ ] `C-CF-06` `constraint` Login with a wrong password returns no bearer token. `src: Core features, Auth and accounts rule 3`
- [ ] `C-CF-07` `constraint` A login failure reveals nothing about whether an address exists. `src: Core features, Auth and accounts rule 3`
- [ ] `C-CF-08` `data` The app stores every password hashed. `src: Core features, Auth and accounts para 1`
- [ ] `C-CF-09` `constraint` No endpoint returns a stored password hash. `src: Core features, Auth and accounts para 1`
- [ ] `C-CF-10` `contract` A guarded endpoint denies a call carrying no bearer token. `src: Core features, Auth and accounts para 1`
- [ ] `C-CF-11` `constraint` A guarded endpoint denies a call carrying an expired bearer token. `src: Core features, Auth and accounts para 1`
- [ ] `C-CF-12` `capability` Every public route carries the wordmark at the left of the header. `src: Core features, The site shell and its pages para 1`
- [ ] `C-CF-13` `capability` Every public route carries one navigation control at the right of the header. `src: Core features, The site shell and its pages para 1`
- [ ] `C-CF-14` `capability` Every public route ends with the booking block before the footer. `src: Core features, The site shell and its pages rule 1`
- [ ] `C-CF-15` `literal` The booking block prints the promise line `reply within 24 hours`. `src: Core features, The site shell and its pages rule 1`
- [ ] `C-CF-16` `capability` The footer repeats the six primary destinations in plain view. `src: Core features, The site shell and its pages para 1`
- [ ] `C-CF-17` `capability` The footer lists the eight services. `src: Core features, The site shell and its pages para 1`
- [ ] `C-CF-18` `capability` The footer carries the directory rating badge. `src: Core features, The site shell and its pages para 1`
- [ ] `C-CF-19` `capability` The navigation control opens a panel covering the viewport. `src: Core features, The site shell and its pages rule 2`
- [ ] `C-CF-20` `capability` The navigation panel nests the eight services under the primary destinations. `src: Core features, The site shell and its pages rule 2`
- [ ] `C-CF-21` `constraint` The route beneath the open navigation panel does not scroll. `src: Core features, The site shell and its pages rule 2`
- [ ] `C-CF-22` `constraint` Focus stays inside the open navigation panel. `src: Core features, The site shell and its pages rule 2`
- [ ] `C-CF-23` `constraint` Closing the navigation panel returns focus to the opening control. `src: Core features, The site shell and its pages rule 2`
- [ ] `C-CF-24` `constraint` Every internal link on a public route resolves to a real route. `src: Core features, The site shell and its pages rule 3`
- [ ] `C-CF-25` `capability` An unknown address renders the studio's own not-found page. `src: Core features, The site shell and its pages rule 4`
- [ ] `C-CF-26` `constraint` The not-found response reports the address as not found. `src: Core features, The site shell and its pages rule 4`
- [ ] `C-CF-27` `capability` The not-found page carries a link back into the archive. `src: Core features, The site shell and its pages rule 4`
- [ ] `C-CF-28` `literal` The footer of every route links the route `/privacy`. `src: Core features, The site shell and its pages rule 5`
- [ ] `C-CF-29` `capability` The privacy route states what the studio stores about a visitor. `src: Core features, The site shell and its pages rule 5`
- [ ] `C-CF-30` `literal` The route `/projects` lists every published project. `src: Core features, The project archive para 1`
- [ ] `C-CF-31` `data` The archive lists projects in stored editorial order. `src: Core features, The project archive para 1`
- [ ] `C-CF-32` `capability` An archive card joins a project's tags with a spaced hyphen. `src: Core features, The project archive para 1`
- [ ] `C-CF-33` `capability` The archive offers eight service filters. `src: Core features, The project archive rule 1`
- [ ] `C-CF-34` `literal` The archive offers a ninth control labelled `All`. `src: Core features, The project archive rule 1`
- [ ] `C-CF-35` `capability` Choosing a filter narrows the grid to projects carrying that service. `src: Core features, The project archive rule 1`
- [ ] `C-CF-36` `constraint` Choosing a filter reloads no page. `src: Core features, The project archive rule 2`
- [ ] `C-CF-37` `capability` The address reflects the chosen filter. `src: Core features, The project archive rule 2`
- [ ] `C-CF-38` `capability` Opening a filtered address directly renders the same narrowed grid. `src: Core features, The project archive rule 2`
- [ ] `C-CF-39` `constraint` Choosing a filter leaves the scroll position unmoved. `src: Core features, The project archive rule 3`
- [ ] `C-CF-40` `capability` The archive announces the resulting count to assistive technology. `src: Core features, The project archive rule 3`
- [ ] `C-CF-41` `capability` A card revealed once stays revealed for the life of the page. `src: Core features, The project archive rule 4`
- [ ] `C-CF-42` `constraint` A card re-entering the grid never replays the reveal. `src: Core features, The project archive rule 4`
- [ ] `C-CF-43` `constraint` A filter matching no published project renders an empty state naming the service. `src: Core features, The project archive rule 5`
- [ ] `C-CF-44` `constraint` An unpublished project never appears in the archive. `src: Core features, The project archive rule 6`
- [ ] `C-CF-45` `constraint` The announced count excludes unpublished projects. `src: Core features, The project archive rule 6`
- [ ] `C-CF-46` `constraint` A direct request for an unpublished project answers as not found. `src: Core features, The project archive rule 6`
- [ ] `C-CF-47` `data` A project carries between one tag plus five more. `src: Core features, The project archive rule 7`
- [ ] `C-CF-48` `constraint` The longest service line wraps rather than being clipped. `src: Core features, The project archive rule 7`
- [ ] `C-CF-49` `literal` The route `/projects/{slug}` renders one published project. `src: Core features, The case study para 1`
- [ ] `C-CF-50` `capability` The case study headline is the client name. `src: Core features, The case study para 1`
- [ ] `C-CF-51` `capability` The case study eyebrow names the deliverable in lower case. `src: Core features, The case study para 1`
- [ ] `C-CF-52` `capability` The case study tag line repeats the archive card's hyphen joined form. `src: Core features, The case study para 1`
- [ ] `C-CF-53` `capability` The outbound action carries the client site's host name as the visible label. `src: Core features, The case study rule 1`
- [ ] `C-CF-54` `contract` The outbound action opens in a new context. `src: Core features, The case study rule 1`
- [ ] `C-CF-55` `contract` The outbound action declares a relationship that withholds the referrer. `src: Core features, The case study rule 1`
- [ ] `C-CF-56` `data` The media sequence is an ordered list of stored entries. `src: Core features, The case study rule 2`
- [ ] `C-CF-57` `literal` A media entry carries a layout hint of `full` or `half`. `src: Core features, The case study rule 2`
- [ ] `C-CF-58` `data` The media sequence renders in stored order. `src: Core features, The case study rule 2`
- [ ] `C-CF-59` `constraint` A media entry saved without alternative text is rejected as invalid. `src: Core features, The case study rule 3`
- [ ] `C-CF-60` `constraint` A rejected media entry writes no row. `src: Core features, The case study rule 3`
- [ ] `C-CF-61` `capability` Related work lists published projects sharing a service with the case study. `src: Core features, The case study rule 4`
- [ ] `C-CF-62` `constraint` Related work never lists the case study's own project. `src: Core features, The case study rule 4`
- [ ] `C-CF-63` `literal` The route `/expertise` lists the eight services in stored index order. `src: Core features, The expertise tree para 1`
- [ ] `C-CF-64` `literal` The route `/expertise/{slug}` argues one service at length. `src: Core features, The expertise tree para 1`
- [ ] `C-CF-65` `data` The eight services form one vocabulary across the tree plus the tags plus the filters. `src: Core features, The expertise tree rule 1`
- [ ] `C-CF-66` `constraint` No page carries a tag that no service defines. `src: Core features, The expertise tree rule 1`
- [ ] `C-CF-67` `capability` A service route lists the projects tagged with that service. `src: Core features, The expertise tree rule 2`
- [ ] `C-CF-68` `constraint` A service route's project count matches the archive filtered to that service. `src: Core features, The expertise tree rule 2`
- [ ] `C-CF-69` `literal` The route `/offers` carries the three packages in a row. `src: Core features, The offers para 1`
- [ ] `C-CF-70` `literal` The first package is named `Opening Note`. `src: Core features, The offers para 1`
- [ ] `C-CF-71` `literal` The second package is named `Full Measure`. `src: Core features, The offers para 1`
- [ ] `C-CF-72` `literal` The third package is named `Open Shelf`. `src: Core features, The offers para 1`
- [ ] `C-CF-73` `literal` `Opening Note` carries the price floor `350000`. `src: Core features, The offers rule 1`
- [ ] `C-CF-74` `literal` `Full Measure` carries the price floor `750000`. `src: Core features, The offers rule 1`
- [ ] `C-CF-75` `literal` `Open Shelf` carries the price floor `1200000`. `src: Core features, The offers rule 1`
- [ ] `C-CF-76` `literal` Every price floor is stored in the currency `usd`. `src: Core features, The offers rule 1`
- [ ] `C-CF-77` `literal` A rendered price reads `From $3,500 plus tax`. `src: Core features, The offers rule 2`
- [ ] `C-CF-78` `constraint` A rendered price without the from label is a defect. `src: Core features, The offers rule 2`
- [ ] `C-CF-79` `constraint` A rendered price without the tax status is a defect. `src: Core features, The offers rule 2`
- [ ] `C-CF-80` `literal` `Full Measure` carries the badge `Recommended`. `src: Core features, The offers rule 3`
- [ ] `C-CF-81` `constraint` A second recommended package is refused on save. `src: Core features, The offers rule 3`
- [ ] `C-CF-82` `literal` The first accordion panel is labelled `Who the package suits`. `src: Core features, The offers rule 4`
- [ ] `C-CF-83` `literal` The second accordion panel is labelled `What the package contains`. `src: Core features, The offers rule 4`
- [ ] `C-CF-84` `literal` The third accordion panel is labelled `What the studio delivers`. `src: Core features, The offers rule 4`
- [ ] `C-CF-85` `literal` The fourth accordion panel is labelled `What can be added`. `src: Core features, The offers rule 4`
- [ ] `C-CF-86` `capability` The first accordion panel carries a qualifying list. `src: Core features, The offers rule 5`
- [ ] `C-CF-87` `capability` The first accordion panel carries a disqualifying list. `src: Core features, The offers rule 5`
- [ ] `C-CF-88` `capability` A disqualifying entry naming another package links to that package. `src: Core features, The offers rule 5`
- [ ] `C-CF-89` `constraint` The disqualifying list is never omitted. `src: Core features, The offers rule 5`
- [ ] `C-CF-90` `capability` Every accordion panel is closed at first paint. `src: Core features, The offers rule 6`
- [ ] `C-CF-91` `constraint` Each accordion panel opens without closing another panel. `src: Core features, The offers rule 6`
- [ ] `C-CF-92` `capability` Each accordion control exposes whether the panel is expanded. `src: Core features, The offers rule 6`
- [ ] `C-CF-93` `constraint` Every accordion panel's content is present at first paint. `src: Core features, The offers rule 6`
- [ ] `C-CF-94` `literal` The route `/method` names the method `Throughline(TM)`. `src: Core features, The method para 1`
- [ ] `C-CF-95` `constraint` The method name carries the mark at every occurrence. `src: Core features, The method rule 1`
- [ ] `C-CF-96` `capability` The method route carries four numbered steps in stored order. `src: Core features, The method rule 1`
- [ ] `C-CF-97` `capability` The method route carries a qualifying audience list. `src: Core features, The method rule 1`
- [ ] `C-CF-98` `capability` The method route carries a disqualifying audience list. `src: Core features, The method rule 1`
- [ ] `C-CF-99` `literal` The first method step is titled `Diagnostic`. `src: Core features, The method rule 2`
- [ ] `C-CF-100` `literal` The second method step is titled `Art direction`. `src: Core features, The method rule 2`
- [ ] `C-CF-101` `literal` The third method step is titled `Digital experience`. `src: Core features, The method rule 2`
- [ ] `C-CF-102` `literal` The fourth method step is titled `Brand alignment`. `src: Core features, The method rule 2`
- [ ] `C-CF-103` `data` The home route renders the method from the one stored method record. `src: Core features, The method rule 3`
- [ ] `C-CF-104` `data` The about route renders the third differentiator from the method record. `src: Core features, The method rule 3`
- [ ] `C-CF-105` `literal` The awards wall carries the row `2023` `Vare Studio` `Honourable Mention`. `src: Core features, Proof rule 1`
- [ ] `C-CF-106` `literal` The awards wall carries the row `2024` `Verdigris Studio` `Nominee`. `src: Core features, Proof rule 1`
- [ ] `C-CF-107` `literal` The awards wall carries the row `2025` `Verdigris Studio` `Nominee`. `src: Core features, Proof rule 1`
- [ ] `C-CF-108` `constraint` The earliest award row keeps an entity name differing from the later two. `src: Core features, Proof rule 1`
- [ ] `C-CF-109` `data` The awards wall renders on the home route from the one stored record. `src: Core features, Proof rule 2`
- [ ] `C-CF-110` `data` The awards wall renders on the about route from the one stored record. `src: Core features, Proof rule 2`
- [ ] `C-CF-111` `literal` The proof band prints the delivered count `148`. `src: Core features, Proof rule 3`
- [ ] `C-CF-112` `capability` The proof band renders on the home route. `src: Core features, Proof rule 3`
- [ ] `C-CF-113` `capability` The proof band renders on the archive route. `src: Core features, Proof rule 3`
- [ ] `C-CF-114` `capability` The proof band renders on the about route. `src: Core features, Proof rule 3`
- [ ] `C-CF-115` `literal` The directory badge prints the rating `4.3`. `src: Core features, Proof rule 4`
- [ ] `C-CF-116` `literal` The directory badge prints the verdict `Very good`. `src: Core features, Proof rule 4`
- [ ] `C-CF-117` `literal` The directory badge names the source `Studio Index`. `src: Core features, Proof rule 4`
- [ ] `C-CF-118` `capability` The directory badge's accessible name spells out all five stored fields. `src: Core features, Proof rule 4`
- [ ] `C-CF-119` `literal` The route `/book` renders the studio calendar as a grid of slots. `src: Core features, Booking a strategic call para 1`
- [ ] `C-CF-120` `data` Every calendar slot lasts 30 minutes. `src: Core features, Booking a strategic call para 1`
- [ ] `C-CF-121` `capability` A taken slot stays visible on the calendar. `src: Core features, Booking a strategic call para 1`
- [ ] `C-CF-122` `constraint` A taken slot cannot be chosen. `src: Core features, Booking a strategic call para 1`
- [ ] `C-CF-123` `constraint` A closed slot cannot be chosen. `src: Core features, Booking a strategic call para 1`
- [ ] `C-CF-124` `data` Choosing a slot places a hold lasting 8 minutes. `src: Core features, Booking a strategic call para 1`
- [ ] `C-CF-125` `capability` The remaining hold time counts down in place. `src: Core features, Booking a strategic call para 1`
- [ ] `C-CF-126` `literal` The route `/book/hold/{reference}` collects the sector plus the topic. `src: Core features, Booking a strategic call para 1`
- [ ] `C-CF-127` `literal` The route `/book/confirm/{reference}` reads the slot back before confirming. `src: Core features, Booking a strategic call para 1`
- [ ] `C-CF-128` `literal` The route `/book/done/{reference}` renders the confirmed call. `src: Core features, Booking a strategic call para 1`
- [ ] `C-CF-129` `constraint` Moving back a step keeps the hold running. `src: Core features, Booking a strategic call para 1`
- [ ] `C-CF-130` `constraint` A slot carries at most one booking that is held or confirmed. `src: Core features, Booking a strategic call rule 1`
- [ ] `C-CF-131` `constraint` Two simultaneous holds on one slot never both succeed. `src: Core features, Booking a strategic call rule 1`
- [ ] `C-CF-132` `constraint` The losing hold request is rejected with a stated reason. `src: Core features, Booking a strategic call rule 1`
- [ ] `C-CF-133` `contract` The single winner rule holds at the database level. `src: Core features, Booking a strategic call rule 1`
- [ ] `C-CF-134` `capability` The loser of a race is offered the three nearest open slots. `src: Core features, Booking a strategic call rule 1`
- [ ] `C-CF-135` `constraint` The loser of a race never reaches a confirmation. `src: Core features, Booking a strategic call rule 1`
- [ ] `C-CF-136` `constraint` A rejected hold leaves no held booking behind. `src: Core features, Booking a strategic call rule 2`
- [ ] `C-CF-137` `constraint` A rejected hold leaves the winner's booking untouched. `src: Core features, Booking a strategic call rule 2`
- [ ] `C-CF-138` `constraint` A hold past 8 minutes stops being live. `src: Core features, Booking a strategic call rule 3`
- [ ] `C-CF-139` `capability` A slot whose hold lapsed becomes choosable again by anybody. `src: Core features, Booking a strategic call rule 3`
- [ ] `C-CF-140` `capability` An abandoned booking page reports the lapsed hold at the next interaction. `src: Core features, Booking a strategic call rule 3`
- [ ] `C-CF-141` `constraint` Confirming a lapsed hold is rejected. `src: Core features, Booking a strategic call rule 3`
- [ ] `C-CF-142` `constraint` Confirming a lapsed hold creates no booking. `src: Core features, Booking a strategic call rule 3`
- [ ] `C-CF-143` `constraint` Holding a slot requires a signed-in client. `src: Core features, Booking a strategic call rule 4`
- [ ] `C-CF-144` `capability` An anonymous visitor choosing a slot is sent to sign in. `src: Core features, Booking a strategic call rule 4`
- [ ] `C-CF-145` `capability` A visitor returning from sign-in lands back on the same slot. `src: Core features, Booking a strategic call rule 4`
- [ ] `C-CF-146` `capability` Confirming writes the booking in the confirmed state. `src: Core features, Booking a strategic call rule 5`
- [ ] `C-CF-147` `constraint` Confirming sends exactly one message over SMTP. `src: Core features, Booking a strategic call rule 5`
- [ ] `C-CF-148` `literal` The confirmation subject begins `Call confirmed:`. `src: Core features, Booking a strategic call rule 5`
- [ ] `C-CF-149` `literal` The confirmation subject reads `Call confirmed: 2026-09-18 09:00 UTC` for a slot starting then. `src: Core features, Booking a strategic call rule 5`
- [ ] `C-CF-150` `constraint` The confirmation is addressed to the booking account's own email. `src: Core features, Booking a strategic call rule 5`
- [ ] `C-CF-151` `constraint` The confirmation carries no cc recipient. `src: Core features, Booking a strategic call rule 5`
- [ ] `C-CF-152` `constraint` The confirmation carries no bcc recipient. `src: Core features, Booking a strategic call rule 5`
- [ ] `C-CF-153` `data` The confirmation body names the booking reference. `src: Core features, Booking a strategic call rule 5`
- [ ] `C-CF-154` `constraint` Placing a hold sends no message. `src: Core features, Booking a strategic call rule 6`
- [ ] `C-CF-155` `constraint` A lapsing hold sends no message. `src: Core features, Booking a strategic call rule 6`
- [ ] `C-CF-156` `constraint` A cancellation sends no message. `src: Core features, Booking a strategic call rule 6`
- [ ] `C-CF-157` `constraint` Submitting the enquiry form sends no message. `src: Core features, Booking a strategic call rule 6`
- [ ] `C-CF-158` `literal` A booking reference reads `vs-7f3a9c1d4e20` in form. `src: Core features, Booking a strategic call rule 7`
- [ ] `C-CF-159` `constraint` A booking reference is unguessable. `src: Core features, Booking a strategic call rule 7`
- [ ] `C-CF-160` `capability` A client cancels a call the same client confirmed. `src: Core features, Booking a strategic call rule 8`
- [ ] `C-CF-161` `capability` Cancelling returns the slot to the grid as choosable. `src: Core features, Booking a strategic call rule 8`
- [ ] `C-CF-162` `constraint` A client cancelling another client's booking is denied. `src: Core features, Booking a strategic call rule 8`
- [ ] `C-CF-163` `constraint` A denied cancellation leaves the other client's booking unchanged. `src: Core features, Booking a strategic call rule 8`
- [ ] `C-CF-164` `literal` The booking sector is one of `beauty`, `wellness`, `food` or `lifestyle`. `src: Core features, Booking a strategic call rule 9`
- [ ] `C-CF-165` `constraint` An empty booking topic is rejected as invalid. `src: Core features, Booking a strategic call rule 9`
- [ ] `C-CF-166` `constraint` A rejected booking step names the offending field inline. `src: Core features, Booking a strategic call rule 9`
- [ ] `C-CF-167` `constraint` A rejected booking step keeps the hold running. `src: Core features, Booking a strategic call rule 9`
- [ ] `C-CF-168` `literal` The route `/contact` offers the written path before the booked path. `src: Core features, The enquiry para 1`
- [ ] `C-CF-169` `capability` The enquiry form carries eight fields plus a consent control. `src: Core features, The enquiry para 1`
- [ ] `C-CF-170` `constraint` The surname field is required. `src: Core features, The enquiry rule 1`
- [ ] `C-CF-171` `constraint` The first name field is required. `src: Core features, The enquiry rule 1`
- [ ] `C-CF-172` `constraint` The electronic mail field is required. `src: Core features, The enquiry rule 1`
- [ ] `C-CF-173` `literal` The project type field offers `Launch` or `Redesign`. `src: Core features, The enquiry rule 1`
- [ ] `C-CF-174` `literal` The budget field offers the band `Under $5,000`. `src: Core features, The enquiry rule 1`
- [ ] `C-CF-175` `literal` The budget field offers the band `$5,000 to $10,000`. `src: Core features, The enquiry rule 1`
- [ ] `C-CF-176` `literal` The budget field offers the band `Over $10,000`. `src: Core features, The enquiry rule 1`
- [ ] `C-CF-177` `literal` The budget field offers the band `Not sure yet`. `src: Core features, The enquiry rule 1`
- [ ] `C-CF-178` `contract` The server enforces enquiry validation. `src: Core features, The enquiry rule 2`
- [ ] `C-CF-179` `constraint` An invalid enquiry is rejected as invalid. `src: Core features, The enquiry rule 2`
- [ ] `C-CF-180` `capability` An invalid enquiry names every offending field inline. `src: Core features, The enquiry rule 2`
- [ ] `C-CF-181` `constraint` An invalid enquiry keeps the typed values on the form. `src: Core features, The enquiry rule 2`
- [ ] `C-CF-182` `constraint` An invalid enquiry writes no row. `src: Core features, The enquiry rule 2`
- [ ] `C-CF-183` `constraint` The consent control is never checked by default. `src: Core features, The enquiry rule 3`
- [ ] `C-CF-184` `constraint` An enquiry submitted without consent is rejected as invalid. `src: Core features, The enquiry rule 3`
- [ ] `C-CF-185` `data` A stored enquiry records the moment consent was given. `src: Core features, The enquiry rule 3`
- [ ] `C-CF-186` `data` A stored enquiry records when a reply is due. `src: Core features, The enquiry rule 4`
- [ ] `C-CF-187` `data` The due moment is the arrival moment plus 24 hours. `src: Core features, The enquiry rule 4`
- [ ] `C-CF-188` `literal` An enquiry reference reads `vq-4c81be09fa37` in form. `src: Core features, The enquiry rule 4`
- [ ] `C-CF-189` `capability` The contact route prints the reply promise. `src: Core features, The enquiry rule 5`
- [ ] `C-CF-190` `data` The promise renders from the one stored promise value. `src: Core features, The enquiry rule 5`
- [ ] `C-CF-191` `literal` The route `/studio` is reachable only by the studio account. `src: Core features, The studio console para 1`
- [ ] `C-CF-192` `literal` The route `/studio/slots` lists the calendar. `src: Core features, The studio console rule 1`
- [ ] `C-CF-193` `capability` The console opens a calendar slot. `src: Core features, The studio console rule 1`
- [ ] `C-CF-194` `capability` The console closes a calendar slot. `src: Core features, The studio console rule 1`
- [ ] `C-CF-195` `constraint` Closing a slot carrying a confirmed booking is rejected. `src: Core features, The studio console rule 1`
- [ ] `C-CF-196` `constraint` A rejected close leaves the slot open. `src: Core features, The studio console rule 1`
- [ ] `C-CF-197` `constraint` Opening a slot at an existing start time is rejected as invalid. `src: Core features, The studio console rule 1`
- [ ] `C-CF-198` `literal` The route `/studio/enquiries` lists every enquiry newest first. `src: Core features, The studio console rule 2`
- [ ] `C-CF-199` `capability` The enquiry list shows when a reply is due. `src: Core features, The studio console rule 2`
- [ ] `C-CF-200` `capability` Recording a first response stores the moment. `src: Core features, The studio console rule 2`
- [ ] `C-CF-201` `constraint` A second recording does not move the stored moment. `src: Core features, The studio console rule 2`
- [ ] `C-CF-202` `literal` The route `/studio/projects` publishes a project. `src: Core features, The studio console rule 3`
- [ ] `C-CF-203` `capability` The console unpublishes a project. `src: Core features, The studio console rule 3`
- [ ] `C-CF-204` `capability` The console sets a project's editorial order. `src: Core features, The studio console rule 3`
- [ ] `C-CF-205` `constraint` Publishing a project whose media lacks alternative text is rejected. `src: Core features, The studio console rule 3`
- [ ] `C-CF-206` `constraint` A rejected publish leaves the project unpublished. `src: Core features, The studio console rule 3`
- [ ] `C-CF-207` `constraint` Every console endpoint refuses a client session. `src: Core features, The studio console rule 4`
- [ ] `C-CF-208` `constraint` Every console endpoint refuses an anonymous request. `src: Core features, The studio console rule 4`
- [ ] `C-CF-209` `constraint` A refused console call leaves the underlying row unchanged. `src: Core features, The studio console rule 4`

## C-UF User flow

- [ ] `C-UF-01` `literal` The route `/` renders the home argument. `src: User flow, route table row 1`
- [ ] `C-UF-02` `literal` The route `/about` renders the founder plus the manifesto plus the awards. `src: User flow, route table row 8`
- [ ] `C-UF-03` `literal` The route `/account/bookings` lists a client's own calls. `src: User flow, route table row 18`
- [ ] `C-UF-04` `literal` The route `/login` signs an account in. `src: User flow, route table row 16`
- [ ] `C-UF-05` `literal` The route `/signup` creates a client account. `src: User flow, route table row 17`
- [ ] `C-UF-06` `capability` An anonymous request for a guarded route goes to the sign-in route. `src: User flow, entry and redirects`
- [ ] `C-UF-07` `capability` The intended address survives the sign-in detour. `src: User flow, entry and redirects`
- [ ] `C-UF-08` `capability` A client signing in with no intended address lands on the bookings route. `src: User flow, entry and redirects`
- [ ] `C-UF-09` `capability` The studio account signing in lands on the console. `src: User flow, entry and redirects`
- [ ] `C-UF-10` `capability` Logging out returns to the home route. `src: User flow, entry and redirects`
- [ ] `C-UF-11` `constraint` A token stops working the moment an account logs out. `src: User flow, entry and redirects`
- [ ] `C-UF-12` `constraint` A session expiring mid-booking leaves the page in place. `src: User flow, entry and redirects`
- [ ] `C-UF-13` `capability` A session expiring mid-booking keeps the typed sector. `src: User flow, entry and redirects`
- [ ] `C-UF-14` `constraint` A client reaching a console route is refused with a stated reason. `src: User flow, entry and redirects`
- [ ] `C-UF-15` `capability` A signed-in client reaches a confirmed call from the calendar. `src: User flow, journey 1`
- [ ] `C-UF-16` `capability` Two clients racing for one slot yield exactly one confirmed call. `src: User flow, journey 2`
- [ ] `C-UF-17` `capability` A lapsed hold returns the slot to the grid. `src: User flow, journey 3`
- [ ] `C-UF-18` `capability` A filtered archive address reopens with the same narrowed grid. `src: User flow, journey 4`
- [ ] `C-UF-19` `capability` A reader reaches a related project from a case study. `src: User flow, journey 5`
- [ ] `C-UF-20` `capability` A reader reaches the named package from a disqualifying entry. `src: User flow, journey 6`
- [ ] `C-UF-21` `capability` The studio account records a first response against an enquiry. `src: User flow, journey 8`
- [ ] `C-UF-22` `constraint` A client requesting another client's booking by reference is denied. `src: User flow, journey 9`
- [ ] `C-UF-23` `capability` Every list carries an empty state naming what would be there. `src: User flow, states`
- [ ] `C-UF-24` `constraint` Every route carries a loading state rather than a blank frame. `src: User flow, states`
- [ ] `C-UF-25` `capability` An error renders in place as an inline banner. `src: User flow, states`
- [ ] `C-UF-26` `constraint` An error never replaces a route with a stack trace. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The ground alternates between a near-white neutral plus a near-white warm neutral. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-02` `ui` A section sits on one ground rather than on a gradient between two. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-03` `ui` Body copy sits on a deep neutral. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-04` `ui` Headings sit on the strongest ink in the product. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-05` `ui` Exactly one saturated hue carries the brand. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-06` `ui` The brand hue is a mid, soft red. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-07` `ui` A light, vivid orange marks a hold running down. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-08` `ui` The hold colour appears on nothing other than a live hold. `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-09` `literal` Headlines are set in `Playfair Display`. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-10` `literal` The interface face is `Syne`. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-11` `literal` Body copy is set in `Lexend Deca`. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-12` `ui` A headline is one sentence in one size with words leaning into true italic. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-13` `ui` Display type is set solid with leading equal to size. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-14` `ui` Interface type never interpolates with viewport width. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-15` `ui` Display type never steps at a breakpoint. `src: UI/UX notes, type paragraph`
- [ ] `C-UX-16` `ui` The product's own surfaces carry no radius. `src: UI/UX notes, shape paragraph`
- [ ] `C-UX-17` `ui` The product's own surfaces carry no shadow. `src: UI/UX notes, shape paragraph`
- [ ] `C-UX-18` `ui` The recommended badge is the one filled coloured surface. `src: UI/UX notes, shape paragraph`
- [ ] `C-UX-19` `ui` Sections read as separate without a dividing line. `src: UI/UX notes, density paragraph`
- [ ] `C-UX-20` `ui` Navigation lives in a panel rather than in a bar. `src: UI/UX notes, layout archetype paragraph`
- [ ] `C-UX-21` `ui` The header inverts to white over a dark section. `src: UI/UX notes, layout archetype paragraph`
- [ ] `C-UX-22` `ui` One eased character carries every moment in the product. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-23` `ui` Scrolling continues briefly after a gesture stops. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-24` `ui` A block is uncovered from one side as the block enters view. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-25` `ui` The client mark strip runs without stopping. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-26` `ui` A reduced motion preference disables the inertial scroll. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-27` `ui` A reduced motion preference delivers blocks already uncovered. `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-28` `ui` A translucent overlay carries type across an image. `src: UI/UX notes, ground over imagery paragraph`
- [ ] `C-UX-29` `ui` Every control carries a resting state plus four more. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-30` `ui` An unavailable control is never signalled by colour alone. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-31` `ui` The active archive filter differs from a hovered filter by more than colour. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-32` `ui` Cancelling a confirmed call asks once before happening. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-33` `ui` The Escape key closes the navigation panel. `src: UI/UX notes, components paragraph`
- [ ] `C-UX-34` `contract` Body text meets WCAG AA contrast against the ground. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-35` `contract` Keyboard navigation reaches every control with a visible focus ring. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-36` `contract` Every content image carries alternative text. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-37` `contract` A decorative image declares the decorative role. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-38` `ui` Icon-only controls carry names. `src: UI/UX notes, accessibility paragraph`
- [ ] `C-UX-39` `ui` The archive is three across at the widest layout. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-40` `ui` The archive is one across at phone width. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-41` `ui` The three offer cards stack at phone width. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-42` `ui` The recommended badge stays attached to the card edge at every width. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-43` `ui` The calendar shows one day at a time at the narrowest layout. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-44` `ui` Nothing overflows sideways at a narrow viewport. `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-45` `ui` Every navigation destination stays reachable at a narrow viewport. `src: UI/UX notes, responsive paragraph`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The frontend is built with SolidJS plus Vite. `src: Technical requirements, para 1`
- [ ] `C-TR-02` `contract` The backend is FastAPI on Python. `src: Technical requirements, para 1`
- [ ] `C-TR-03` `contract` The browser receives an application shell. `src: Technical requirements, para 1`
- [ ] `C-TR-04` `contract` Every route renders in the browser from JSON the API returns. `src: Technical requirements, para 1`
- [ ] `C-TR-05` `literal` The datastore is PostgreSQL at `DATABASE_URL`. `src: Technical requirements, para 2`
- [ ] `C-TR-06` `literal` Mail leaves over SMTP at `SMTP_HOST`. `src: Technical requirements, para 2`
- [ ] `C-TR-07` `literal` The SMTP port is read from `SMTP_PORT`. `src: Technical requirements, para 2`
- [ ] `C-TR-08` `literal` The public origin is read from `APP_PUBLIC_URL`. `src: Technical requirements, para 2`
- [ ] `C-TR-09` `constraint` No host is hardcoded anywhere in the app. `src: Technical requirements, para 2`
- [ ] `C-TR-10` `constraint` The app introduces no second datastore. `src: Technical requirements, para 3`
- [ ] `C-TR-11` `constraint` The app introduces no mail vendor beyond the named one. `src: Technical requirements, para 3`
- [ ] `C-TR-12` `contract` Authentication is implemented by the app rather than an identity provider. `src: Technical requirements, para 4`
- [ ] `C-TR-13` `literal` The route `GET /api/health` returns `200` once the app is ready. `src: Technical requirements, para 5`
- [ ] `C-TR-14` `constraint` The health route reports ready only once the seed has completed. `src: Technical requirements, para 5`
- [ ] `C-TR-15` `contract` Application logs go to standard output. `src: Technical requirements, para 5`
- [ ] `C-TR-16` `data` Each log line carries the request method. `src: Technical requirements, para 5`
- [ ] `C-TR-17` `constraint` No two public routes share a title. `src: Technical requirements, para 6`
- [ ] `C-TR-18` `constraint` No two public routes share a description. `src: Technical requirements, para 6`
- [ ] `C-TR-19` `literal` A route title ends with the studio name `Verdigris Studio`. `src: Technical requirements, para 6`
- [ ] `C-TR-20` `contract` Every public route declares a social preview image. `src: Technical requirements, para 6`
- [ ] `C-TR-21` `constraint` A declared preview image resolves when requested by the declared address. `src: Technical requirements, para 6`
- [ ] `C-TR-22` `constraint` The route identity is present in the document the server sends. `src: Technical requirements, para 6`
- [ ] `C-TR-23` `data` A media entry stores the generator plus the seed plus the aspect. `src: Technical requirements, para 7`
- [ ] `C-TR-24` `constraint` The app offers no file upload surface. `src: Technical requirements, para 7`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema carries sixteen tables. `src: Data model, para 1`
- [ ] `C-DM-02` `contract` Every stored timestamp is UTC. `src: Data model, para 1`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model, password paragraph`
- [ ] `C-DM-04` `literal` The seeded logins are written to `/app/USER_README.md`. `src: Data model, password paragraph`
- [ ] `C-DM-05` `data` The `accounts` table holds a unique email per row. `src: Data model, accounts`
- [ ] `C-DM-06` `literal` An account role is `client` or `studio`. `src: Data model, accounts`
- [ ] `C-DM-07` `data` The `services` table holds eight rows. `src: Data model, services`
- [ ] `C-DM-08` `literal` The first service is named `Experience design`. `src: Data model, services`
- [ ] `C-DM-09` `literal` The service vocabulary includes `Visual identity`. `src: Data model, services`
- [ ] `C-DM-10` `literal` The service vocabulary includes `Digital communication`. `src: Data model, services`
- [ ] `C-DM-11` `data` A service's `taxonomy_key` joins a service to a project's tags. `src: Data model, services`
- [ ] `C-DM-12` `data` The `projects` table holds twelve rows. `src: Data model, projects`
- [ ] `C-DM-13` `literal` A project's ground is `light` or `dark`. `src: Data model, projects`
- [ ] `C-DM-14` `data` The `project_media` table keys a position unique within a project. `src: Data model, project_media`
- [ ] `C-DM-15` `constraint` A media row without alternative text is rejected. `src: Data model, project_media`
- [ ] `C-DM-16` `data` The `packages` table holds three rows. `src: Data model, packages`
- [ ] `C-DM-17` `constraint` At most one package row is recommended at any moment. `src: Data model, packages`
- [ ] `C-DM-18` `data` The `package_panels` table holds four rows per package. `src: Data model, package_panels`
- [ ] `C-DM-19` `literal` A fit row's kind is `positive` or `negative`. `src: Data model, package_fit`
- [ ] `C-DM-20` `constraint` Only a negative fit row carries a redirect package. `src: Data model, package_fit`
- [ ] `C-DM-21` `data` The `awards` table holds three rows. `src: Data model, awards`
- [ ] `C-DM-22` `data` The `method_steps` table holds four rows. `src: Data model, method_steps`
- [ ] `C-DM-23` `data` The `studio_profile` table holds one row. `src: Data model, studio_profile`
- [ ] `C-DM-24` `data` A slot's start time is unique across the `slots` table. `src: Data model, slots`
- [ ] `C-DM-25` `literal` A slot state is `open` or `closed`. `src: Data model, slots`
- [ ] `C-DM-26` `data` A slot's end time is 30 minutes after the start time. `src: Data model, slots`
- [ ] `C-DM-27` `literal` A booking state is one of `held`, `confirmed`, `cancelled` or `expired`. `src: Data model, bookings`
- [ ] `C-DM-28` `contract` The invariant `booking_one_live_per_slot` allows one live booking per slot. `src: Data model, bookings invariant`
- [ ] `C-DM-29` `constraint` A lapsed held booking does not count as live. `src: Data model, bookings invariant`
- [ ] `C-DM-30` `data` An enquiry's due moment is derived on write. `src: Data model, enquiries`
- [ ] `C-DM-31` `literal` The stored promise is `24` hours. `src: Data model, enquiries`
- [ ] `C-DM-32` `data` The `page_identity` table holds one row per public route. `src: Data model, page_identity`
- [ ] `C-DM-33` `data` An archive card's service line is derived on read. `src: Data model, derived paragraph`
- [ ] `C-DM-34` `data` A booking's remaining hold time is derived rather than stored. `src: Data model, derived paragraph`
- [ ] `C-DM-35` `data` Every string appearing on more than one route is a stored field. `src: Data model, principles paragraph`
- [ ] `C-DM-36` `data` Every list rendered in more than one place is one stored list. `src: Data model, principles paragraph`
- [ ] `C-DM-37` `contract` A booking is readable by the account that created the booking. `src: Data model, delivery paragraph`
- [ ] `C-DM-38` `contract` A booking is readable by the studio account. `src: Data model, delivery paragraph`
- [ ] `C-DM-39` `constraint` A booking is never listed to any other account. `src: Data model, delivery paragraph`
- [ ] `C-DM-40` `data` Archive order is a stored value rather than a sort computed on read. `src: Data model, ordering paragraph`
- [ ] `C-DM-41` `literal` The first seeded project client is `Aster & Bloom`. `src: Data model, seed data paragraph`
- [ ] `C-DM-42` `literal` The seeded projects include `Saltbox Kitchen`. `src: Data model, seed data paragraph`
- [ ] `C-DM-43` `literal` The seeded projects include `Slow Sunday`. `src: Data model, seed data paragraph`
- [ ] `C-DM-44` `literal` The seeded projects include `Bread & Bone`. `src: Data model, seed data paragraph`
- [ ] `C-DM-45` `data` Six calendar slots are seeded open. `src: Data model, seed data paragraph`
- [ ] `C-DM-46` `data` Five seeded slots fall on the next day. `src: Data model, seed data paragraph`
- [ ] `C-DM-47` `data` Exactly one seeded slot falls alone on the day after next. `src: Data model, seed data paragraph`
- [ ] `C-DM-48` `constraint` Seeding is idempotent across a restart. `src: Data model, seed data paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `capability` The header carries two elements only. `src: Front-end specification, the global chrome`
- [ ] `C-FE-02` `capability` The header stays with the viewport for the whole scroll. `src: Front-end specification, the global chrome`
- [ ] `C-FE-03` `capability` The navigation panel rises a distance expressed in the panel's own type size. `src: Front-end specification, the global chrome`
- [ ] `C-FE-04` `capability` The navigation panel lists the six primary destinations in stated order. `src: Front-end specification, the global chrome`
- [ ] `C-FE-05` `capability` The booking block carries four lines in stated order. `src: Front-end specification, the global chrome`
- [ ] `C-FE-06` `capability` The booking action shrinks slightly under the pointer. `src: Front-end specification, the global chrome`
- [ ] `C-FE-07` `constraint` The footer wordmark is set as type rather than as an image. `src: Front-end specification, the global chrome`
- [ ] `C-FE-08` `constraint` The primary destination list is emitted once into the document. `src: Front-end specification, the global chrome`
- [ ] `C-FE-09` `capability` The home route stacks eleven blocks in fixed order. `src: Front-end specification, route home`
- [ ] `C-FE-10` `capability` The hero is the one block complete at first paint. `src: Front-end specification, route home`
- [ ] `C-FE-11` `capability` The hero headline is legible before the background image decodes. `src: Front-end specification, route home`
- [ ] `C-FE-12` `constraint` The hero image is darkened rather than covered by a panel. `src: Front-end specification, route home`
- [ ] `C-FE-13` `capability` The asterisk opening a qualifying line is a text character. `src: Front-end specification, route home`
- [ ] `C-FE-14` `constraint` The home work grid carries no service tags on a card. `src: Front-end specification, route home`
- [ ] `C-FE-15` `constraint` The offers route opens on a type hero rather than photography. `src: Front-end specification, route offers`
- [ ] `C-FE-16` `capability` The accordion marker reads as a minus when the panel is open. `src: Front-end specification, route offers`
- [ ] `C-FE-17` `capability` The recommended badge breaks the outline of the middle card. `src: Front-end specification, route offers`
- [ ] `C-FE-18` `capability` A filter control at rest carries a hairline border in the mid cool neutral. `src: Front-end specification, route projects`
- [ ] `C-FE-19` `capability` A hovered filter takes the brand red on the label plus the border together. `src: Front-end specification, route projects`
- [ ] `C-FE-20` `capability` The whole archive card is the link. `src: Front-end specification, route projects`
- [ ] `C-FE-21` `capability` Load more appends cards into the same grid. `src: Front-end specification, route projects`
- [ ] `C-FE-22` `capability` Appended cards leave the scroll position unmoved. `src: Front-end specification, route projects`
- [ ] `C-FE-23` `capability` Keyboard focus lands on the first appended card. `src: Front-end specification, route projects`
- [ ] `C-FE-24` `capability` The load more action is removed once the archive is exhausted. `src: Front-end specification, route projects`
- [ ] `C-FE-25` `capability` The case study hero is a four part stack. `src: Front-end specification, route case study`
- [ ] `C-FE-26` `capability` Media layers drift inside their frames as the page passes. `src: Front-end specification, route case study`
- [ ] `C-FE-27` `capability` Method steps are separated by full width hairlines. `src: Front-end specification, route method`
- [ ] `C-FE-28` `capability` The founder block is written in the first person singular. `src: Front-end specification, route about`
- [ ] `C-FE-29` `literal` The manifesto renders at 16px over 24px. `src: Front-end specification, route about`
- [ ] `C-FE-30` `capability` The manifesto sits on a narrower measure than surrounding blocks. `src: Front-end specification, route about`
- [ ] `C-FE-31` `constraint` Form fields carry a visible label rather than a placeholder standing in. `src: Front-end specification, route contact`
- [ ] `C-FE-32` `constraint` A rejected field is named beneath the field. `src: Front-end specification, route contact`
- [ ] `C-FE-33` `constraint` A rejected field is marked by something other than colour. `src: Front-end specification, route contact`
- [ ] `C-FE-34` `capability` The calendar shows days as columns at the widest layout. `src: Front-end specification, route book`
- [ ] `C-FE-35` `capability` A slot cell prints the start time. `src: Front-end specification, route book`
- [ ] `C-FE-36` `constraint` A taken slot says taken rather than going quiet. `src: Front-end specification, route book`
- [ ] `C-FE-37` `constraint` The countdown updates without the surrounding layout moving. `src: Front-end specification, route book`
- [ ] `C-FE-38` `capability` Each booking step shows which of the three steps is current. `src: Front-end specification, route book`
- [ ] `C-FE-39` `capability` The confirm step holds still for a reader. `src: Front-end specification, route book`
- [ ] `C-FE-40` `constraint` A lost race renders as an inline banner rather than a dialog. `src: Front-end specification, route book`
- [ ] `C-FE-41` `capability` The spinner rotates continuously during a fetch. `src: Front-end specification, iconography`
- [ ] `C-FE-42` `capability` Icons inherit the current text colour. `src: Front-end specification, iconography`
- [ ] `C-FE-43` `constraint` Depth is expressed by stacking order rather than by shadow. `src: Front-end specification, depth and stacking`
- [ ] `C-FE-44` `capability` The inline banner sits above the header. `src: Front-end specification, depth and stacking`
- [ ] `C-FE-45` `constraint` The marquee runs at a constant rate rather than eased. `src: Front-end specification, motion inventory`
- [ ] `C-FE-46` `capability` One reveal wrapper covers every revealing block. `src: Front-end specification, components earned by repetition`
- [ ] `C-FE-47` `capability` A carousel pauses under a resting pointer. `src: Front-end specification, carousel mechanics`
- [ ] `C-FE-48` `capability` A carousel stops entirely under a reduced motion preference. `src: Front-end specification, carousel mechanics`
- [ ] `C-FE-49` `constraint` Every carousel item is reachable from a plain link elsewhere. `src: Front-end specification, carousel mechanics`
- [ ] `C-FE-50` `capability` A client mark is generated as a wordmark set in the interface face. `src: Front-end specification, generated imagery`
- [ ] `C-FE-51` `constraint` The build ships no video file. `src: Front-end specification, generated imagery`
- [ ] `C-FE-52` `constraint` The build ships no image file. `src: Front-end specification, generated imagery`
- [ ] `C-FE-53` `capability` The document declares the page language. `src: Front-end specification, language and locale`
- [ ] `C-FE-54` `constraint` The product ships one language with no locale switcher. `src: Front-end specification, language and locale`
- [ ] `C-FE-55` `literal` The interface type ramp is `12px`, `13px`, `14px`, `15px`, `16px`, `20px`, `30px`. `src: Front-end specification, typography strategy`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app serves one studio with no second tenant. `src: Constraints, bullet 1`
- [ ] `C-CN-02` `constraint` The app takes no money. `src: Constraints, bullet 2`
- [ ] `C-CN-03` `constraint` The app carries no messaging surface. `src: Constraints, bullet 3`
- [ ] `C-CN-04` `constraint` The app carries no visitor shortlist. `src: Constraints, bullet 5`
- [ ] `C-CN-05` `constraint` The app carries no quote configurator. `src: Constraints, bullet 5`
- [ ] `C-CN-06` `constraint` The app embeds no third party widget. `src: Constraints, bullet 6`
- [ ] `C-CN-07` `constraint` The app makes no external network call at runtime. `src: Constraints, bullet 7`
- [ ] `C-CN-08` `constraint` The app ships no native client. `src: Constraints, bullet 8`
- [ ] `C-CN-09` `constraint` Only the studio account edits a collection. `src: Constraints, bullet 9`
- [ ] `C-CN-10` `constraint` The archive stays responsive at a few hundred published projects. `src: Constraints, bullet 10`
- [ ] `C-CN-11` `constraint` The calendar stays responsive at a few hundred slots. `src: Constraints, bullet 10`
- [ ] `C-CN-12` `constraint` The app offers no offline mode. `src: Constraints, bullet 8`
- [ ] `C-CN-13` `constraint` Six named addresses answer as not found. `src: Constraints, bullet 12`
- [ ] `C-CN-14` `literal` The reserved directories sit at `/app/.browser_screenshots`. `src: Constraints, bullet 13`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-02` `literal` The container-internal port is `4173`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-03` `literal` The public port is read from `APP_PUBLIC_PORT`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-04` `literal` The HTTP API is served under the `/api` prefix. `src: Deployment contract, bullet 2`
- [ ] `C-DC-05` `contract` The API shares the origin of the app. `src: Deployment contract, bullet 2`
- [ ] `C-DC-06` `literal` The route `GET /api/health` returns `200` once ready. `src: Deployment contract, bullet 3`
- [ ] `C-DC-07` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract, bullet 4`
- [ ] `C-DC-08` `literal` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract, bullet 5`
- [ ] `C-DC-09` `literal` The reserved directory `.browser_screenshots/` exists at the app root. `src: Deployment contract, bullet 6`
- [ ] `C-DC-10` `literal` The reserved directory `.downloads/` exists at the app root. `src: Deployment contract, bullet 6`
- [ ] `C-DC-11` `contract` The app serves a production build behind a preview server. `src: Deployment contract, bullet 7`
- [ ] `C-DC-12` `constraint` The app serves no development server. `src: Deployment contract, bullet 7`
- [ ] `C-DC-13` `contract` The server keeps running after the session ends. `src: Deployment contract, bullet 8`
- [ ] `C-DC-14` `constraint` The server is not a child of the shell. `src: Deployment contract, bullet 8`
- [ ] `C-DC-15` `literal` The server binds `0.0.0.0`. `src: Deployment contract, bullet 9`
- [ ] `C-DC-16` `constraint` The server never binds a loopback address. `src: Deployment contract, bullet 9`
- [ ] `C-DC-17` `constraint` The app starts no copy of a backing service. `src: Deployment contract, bullet 10`
- [ ] `C-DC-18` `constraint` The app uses no edge function. `src: Deployment contract, bullet 11`
- [ ] `C-DC-19` `constraint` The app requires no persistent volume. `src: Deployment contract, bullet 12`
- [ ] `C-DC-20` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-21` `contract` An invalid call is rejected as a client error. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-22` `constraint` An invalid call is never answered as a server error. `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-23` `literal` The route `POST /api/auth/login` returns an `access_token`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-24` `literal` The route `POST /api/slots/{id}/hold` returns the created booking. `src: Deployment contract, API shapes table`
- [ ] `C-DC-25` `literal` The route `POST /api/bookings/{reference}/confirm` returns the confirmed booking. `src: Deployment contract, API shapes table`
- [ ] `C-DC-26` `literal` The route `POST /api/enquiries` returns a `reference`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-27` `constraint` A confirmation message exists only in the named mail provider. `src: Deployment contract, no mocks paragraph`
- [ ] `C-DC-28` `constraint` A booking living only in the running process is no booking. `src: Deployment contract, no mocks paragraph`
## Pinned literals

| Value | What the instruction calls it | Item | Source |
|---|---|---|---|
| `studio@example.com` | the app seeds the studio account `studio@example.com` | C-RL-21 | User roles, seeded accounts table row 1 |
| `client@example.com` | the app seeds the client account `client@example.com` | C-RL-22 | User roles, seeded accounts table row 2 |
| `client2@example.com` | the app seeds the client account `client2@example.com` | C-RL-23 | User roles, seeded accounts table row 3 |
| `deku-demo-pw-2026` | every seeded account signs in with the password `deku-demo-pw-2026` | C-RL-24 | User roles, seeded accounts paragraph |
| `reply within 24 hours` | the booking block prints the promise line `reply within 24 hours` | C-CF-15 | Core features, The site shell and its pages rule 1 |
| `/privacy` | the footer of every route links the route `/privacy` | C-CF-28 | Core features, The site shell and its pages rule 5 |
| `/projects` | the route `/projects` lists every published project | C-CF-30 | Core features, The project archive para 1 |
| `All` | the archive offers a ninth control labelled `all` | C-CF-34 | Core features, The project archive rule 1 |
| `/projects/{slug}` | the route `/projects/{slug}` renders one published project | C-CF-49 | Core features, The case study para 1 |
| `full` | a media entry carries a layout hint of `full` or `half` | C-CF-57 | Core features, The case study rule 2 |
| `half` | a media entry carries a layout hint of `full` or `half` | C-CF-57 | Core features, The case study rule 2 |
| `/expertise` | the route `/expertise` lists the eight services in stored index order | C-CF-63 | Core features, The expertise tree para 1 |
| `/expertise/{slug}` | the route `/expertise/{slug}` argues one service at length | C-CF-64 | Core features, The expertise tree para 1 |
| `/offers` | the route `/offers` carries the three packages in a row | C-CF-69 | Core features, The offers para 1 |
| `Opening Note` | the first package is named `opening note` | C-CF-70 | Core features, The offers para 1 |
| `Full Measure` | the second package is named `full measure` | C-CF-71 | Core features, The offers para 1 |
| `Open Shelf` | the third package is named `open shelf` | C-CF-72 | Core features, The offers para 1 |
| `350000` | `opening note` carries the price floor `350000` | C-CF-73 | Core features, The offers rule 1 |
| `750000` | `full measure` carries the price floor `750000` | C-CF-74 | Core features, The offers rule 1 |
| `1200000` | `open shelf` carries the price floor `1200000` | C-CF-75 | Core features, The offers rule 1 |
| `usd` | every price floor is stored in the currency `usd` | C-CF-76 | Core features, The offers rule 1 |
| `From $3,500 plus tax` | a rendered price reads `from $3,500 plus tax` | C-CF-77 | Core features, The offers rule 2 |
| `Recommended` | `full measure` carries the badge `recommended` | C-CF-80 | Core features, The offers rule 3 |
| `Who the package suits` | the first accordion panel is labelled `who the package suits` | C-CF-82 | Core features, The offers rule 4 |
| `What the package contains` | the second accordion panel is labelled `what the package contains` | C-CF-83 | Core features, The offers rule 4 |
| `What the studio delivers` | the third accordion panel is labelled `what the studio delivers` | C-CF-84 | Core features, The offers rule 4 |
| `What can be added` | the fourth accordion panel is labelled `what can be added` | C-CF-85 | Core features, The offers rule 4 |
| `/method` | the route `/method` names the method `throughline(tm)` | C-CF-94 | Core features, The method para 1 |
| `Throughline(TM)` | the route `/method` names the method `throughline(tm)` | C-CF-94 | Core features, The method para 1 |
| `Diagnostic` | the first method step is titled `diagnostic` | C-CF-99 | Core features, The method rule 2 |
| `Art direction` | the second method step is titled `art direction` | C-CF-100 | Core features, The method rule 2 |
| `Digital experience` | the third method step is titled `digital experience` | C-CF-101 | Core features, The method rule 2 |
| `Brand alignment` | the fourth method step is titled `brand alignment` | C-CF-102 | Core features, The method rule 2 |
| `2023` | the awards wall carries the row `2023` `vare studio` `honourable mention` | C-CF-105 | Core features, Proof rule 1 |
| `Vare Studio` | the awards wall carries the row `2023` `vare studio` `honourable mention` | C-CF-105 | Core features, Proof rule 1 |
| `Honourable Mention` | the awards wall carries the row `2023` `vare studio` `honourable mention` | C-CF-105 | Core features, Proof rule 1 |
| `2024` | the awards wall carries the row `2024` `verdigris studio` `nominee` | C-CF-106 | Core features, Proof rule 1 |
| `Verdigris Studio` | the awards wall carries the row `2024` `verdigris studio` `nominee` | C-CF-106 | Core features, Proof rule 1 |
| `Nominee` | the awards wall carries the row `2024` `verdigris studio` `nominee` | C-CF-106 | Core features, Proof rule 1 |
| `2025` | the awards wall carries the row `2025` `verdigris studio` `nominee` | C-CF-107 | Core features, Proof rule 1 |
| `148` | the proof band prints the delivered count `148` | C-CF-111 | Core features, Proof rule 3 |
| `4.3` | the directory badge prints the rating `4.3` | C-CF-115 | Core features, Proof rule 4 |
| `Very good` | the directory badge prints the verdict `very good` | C-CF-116 | Core features, Proof rule 4 |
| `Studio Index` | the directory badge names the source `studio index` | C-CF-117 | Core features, Proof rule 4 |
| `/book` | the route `/book` renders the studio calendar as a grid of slots | C-CF-119 | Core features, Booking a strategic call para 1 |
| `/book/hold/{reference}` | the route `/book/hold/{reference}` collects the sector plus the topic | C-CF-126 | Core features, Booking a strategic call para 1 |
| `/book/confirm/{reference}` | the route `/book/confirm/{reference}` reads the slot back before confirming | C-CF-127 | Core features, Booking a strategic call para 1 |
| `/book/done/{reference}` | the route `/book/done/{reference}` renders the confirmed call | C-CF-128 | Core features, Booking a strategic call para 1 |
| `Call confirmed:` | the confirmation subject begins `call confirmed:` | C-CF-148 | Core features, Booking a strategic call rule 5 |
| `Call confirmed: 2026-09-18 09:00 UTC` | the confirmation subject reads `call confirmed: 2026-09-18 09:00 utc` for a slot starting then | C-CF-149 | Core features, Booking a strategic call rule 5 |
| `vs-7f3a9c1d4e20` | a booking reference reads `vs-7f3a9c1d4e20` in form | C-CF-158 | Core features, Booking a strategic call rule 7 |
| `beauty` | the booking sector is one of `beauty`, `wellness`, `food` or `lifestyle` | C-CF-164 | Core features, Booking a strategic call rule 9 |
| `wellness` | the booking sector is one of `beauty`, `wellness`, `food` or `lifestyle` | C-CF-164 | Core features, Booking a strategic call rule 9 |
| `food` | the booking sector is one of `beauty`, `wellness`, `food` or `lifestyle` | C-CF-164 | Core features, Booking a strategic call rule 9 |
| `lifestyle` | the booking sector is one of `beauty`, `wellness`, `food` or `lifestyle` | C-CF-164 | Core features, Booking a strategic call rule 9 |
| `/contact` | the route `/contact` offers the written path before the booked path | C-CF-168 | Core features, The enquiry para 1 |
| `Launch` | the project type field offers `launch` or `redesign` | C-CF-173 | Core features, The enquiry rule 1 |
| `Redesign` | the project type field offers `launch` or `redesign` | C-CF-173 | Core features, The enquiry rule 1 |
| `Under $5,000` | the budget field offers the band `under $5,000` | C-CF-174 | Core features, The enquiry rule 1 |
| `$5,000 to $10,000` | the budget field offers the band `$5,000 to $10,000` | C-CF-175 | Core features, The enquiry rule 1 |
| `Over $10,000` | the budget field offers the band `over $10,000` | C-CF-176 | Core features, The enquiry rule 1 |
| `Not sure yet` | the budget field offers the band `not sure yet` | C-CF-177 | Core features, The enquiry rule 1 |
| `vq-4c81be09fa37` | an enquiry reference reads `vq-4c81be09fa37` in form | C-CF-188 | Core features, The enquiry rule 4 |
| `/studio` | the route `/studio` is reachable only by the studio account | C-CF-191 | Core features, The studio console para 1 |
| `/studio/slots` | the route `/studio/slots` lists the calendar | C-CF-192 | Core features, The studio console rule 1 |
| `/studio/enquiries` | the route `/studio/enquiries` lists every enquiry newest first | C-CF-198 | Core features, The studio console rule 2 |
| `/studio/projects` | the route `/studio/projects` publishes a project | C-CF-202 | Core features, The studio console rule 3 |
| `/` | the route `/` renders the home argument | C-UF-01 | User flow, route table row 1 |
| `/about` | the route `/about` renders the founder plus the manifesto plus the awards | C-UF-02 | User flow, route table row 8 |
| `/account/bookings` | the route `/account/bookings` lists a client's own calls | C-UF-03 | User flow, route table row 18 |
| `/login` | the route `/login` signs an account in | C-UF-04 | User flow, route table row 16 |
| `/signup` | the route `/signup` creates a client account | C-UF-05 | User flow, route table row 17 |
| `Playfair Display` | headlines are set in `playfair display` | C-UX-09 | UI/UX notes, type paragraph |
| `Syne` | the interface face is `syne` | C-UX-10 | UI/UX notes, type paragraph |
| `Lexend Deca` | body copy is set in `lexend deca` | C-UX-11 | UI/UX notes, type paragraph |
| `DATABASE_URL` | the datastore is postgresql at `database_url` | C-TR-05 | Technical requirements, para 2 |
| `SMTP_HOST` | mail leaves over smtp at `smtp_host` | C-TR-06 | Technical requirements, para 2 |
| `SMTP_PORT` | the smtp port is read from `smtp_port` | C-TR-07 | Technical requirements, para 2 |
| `APP_PUBLIC_URL` | the public origin is read from `app_public_url` | C-TR-08 | Technical requirements, para 2 |
| `GET /api/health` | the route `get /api/health` returns `200` once the app is ready | C-TR-13 | Technical requirements, para 5 |
| `200` | the route `get /api/health` returns `200` once the app is ready | C-TR-13 | Technical requirements, para 5 |
| `/app/USER_README.md` | the seeded logins are written to `/app/user_readme.md` | C-DM-04 | Data model, password paragraph |
| `client` | an account role is `client` or `studio` | C-DM-06 | Data model, accounts |
| `studio` | an account role is `client` or `studio` | C-DM-06 | Data model, accounts |
| `Experience design` | the first service is named `experience design` | C-DM-08 | Data model, services |
| `Visual identity` | the service vocabulary includes `visual identity` | C-DM-09 | Data model, services |
| `Digital communication` | the service vocabulary includes `digital communication` | C-DM-10 | Data model, services |
| `light` | a project's ground is `light` or `dark` | C-DM-13 | Data model, projects |
| `dark` | a project's ground is `light` or `dark` | C-DM-13 | Data model, projects |
| `positive` | a fit row's kind is `positive` or `negative` | C-DM-19 | Data model, package_fit |
| `negative` | a fit row's kind is `positive` or `negative` | C-DM-19 | Data model, package_fit |
| `open` | a slot state is `open` or `closed` | C-DM-25 | Data model, slots |
| `closed` | a slot state is `open` or `closed` | C-DM-25 | Data model, slots |
| `held` | a booking state is one of `held`, `confirmed`, `cancelled` or `expired` | C-DM-27 | Data model, bookings |
| `confirmed` | a booking state is one of `held`, `confirmed`, `cancelled` or `expired` | C-DM-27 | Data model, bookings |
| `cancelled` | a booking state is one of `held`, `confirmed`, `cancelled` or `expired` | C-DM-27 | Data model, bookings |
| `expired` | a booking state is one of `held`, `confirmed`, `cancelled` or `expired` | C-DM-27 | Data model, bookings |
| `24` | the stored promise is `24` hours | C-DM-31 | Data model, enquiries |
| `Aster & Bloom` | the first seeded project client is `aster & bloom` | C-DM-41 | Data model, seed data paragraph |
| `Saltbox Kitchen` | the seeded projects include `saltbox kitchen` | C-DM-42 | Data model, seed data paragraph |
| `Slow Sunday` | the seeded projects include `slow sunday` | C-DM-43 | Data model, seed data paragraph |
| `Bread & Bone` | the seeded projects include `bread & bone` | C-DM-44 | Data model, seed data paragraph |
| `12px` | the interface type ramp is `12px`, `13px`, `14px`, `15px`, `16px`, `20px`, `30px` | C-FE-55 | Front-end specification, typography strategy |
| `13px` | the interface type ramp is `12px`, `13px`, `14px`, `15px`, `16px`, `20px`, `30px` | C-FE-55 | Front-end specification, typography strategy |
| `14px` | the interface type ramp is `12px`, `13px`, `14px`, `15px`, `16px`, `20px`, `30px` | C-FE-55 | Front-end specification, typography strategy |
| `15px` | the interface type ramp is `12px`, `13px`, `14px`, `15px`, `16px`, `20px`, `30px` | C-FE-55 | Front-end specification, typography strategy |
| `16px` | the interface type ramp is `12px`, `13px`, `14px`, `15px`, `16px`, `20px`, `30px` | C-FE-55 | Front-end specification, typography strategy |
| `20px` | the interface type ramp is `12px`, `13px`, `14px`, `15px`, `16px`, `20px`, `30px` | C-FE-55 | Front-end specification, typography strategy |
| `30px` | the interface type ramp is `12px`, `13px`, `14px`, `15px`, `16px`, `20px`, `30px` | C-FE-55 | Front-end specification, typography strategy |
| `/app/.browser_screenshots` | the reserved directories sit at `/app/.browser_screenshots` | C-CN-14 | Constraints, bullet 13 |
| `4173` | the container-internal port is `4173` | C-DC-02 | Deployment contract, bullet 1 |
| `APP_PUBLIC_PORT` | the public port is read from `app_public_port` | C-DC-03 | Deployment contract, bullet 1 |
| `/api` | the http api is served under the `/api` prefix | C-DC-04 | Deployment contract, bullet 2 |
| `.browser_screenshots/` | the reserved directory `.browser_screenshots/` exists at the app root | C-DC-09 | Deployment contract, bullet 6 |
| `.downloads/` | the reserved directory `.downloads/` exists at the app root | C-DC-10 | Deployment contract, bullet 6 |
| `0.0.0.0` | the server binds `0.0.0.0` | C-DC-15 | Deployment contract, bullet 9 |
| `POST /api/auth/login` | the route `post /api/auth/login` returns an `access_token` | C-DC-23 | Deployment contract, API shapes table |
| `access_token` | the route `post /api/auth/login` returns an `access_token` | C-DC-23 | Deployment contract, API shapes table |
| `POST /api/slots/{id}/hold` | the route `post /api/slots/{id}/hold` returns the created booking | C-DC-24 | Deployment contract, API shapes table |
| `POST /api/bookings/{reference}/confirm` | the route `post /api/bookings/{reference}/confirm` returns the confirmed booking | C-DC-25 | Deployment contract, API shapes table |
| `POST /api/enquiries` | the route `post /api/enquiries` returns a `reference` | C-DC-26 | Deployment contract, API shapes table |
| `reference` | the route `post /api/enquiries` returns a `reference` | C-DC-26 | Deployment contract, API shapes table |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the exact shade of every palette role | C-UX-01 | named by family, tone and shade so the builder chooses the value |
| the gap between two sections | C-UX-19 | given as a relationship to the gap under a heading rather than as a size |
## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 10 |
| User roles | 1 | 24 |
| Core features | 28 | 209 |
| User flow | 5 | 26 |
| UI and UX notes | 15 | 45 |
| Technical requirements | 9 | 24 |
| Data model | 6 | 48 |
| Front-end specification | 13 | 55 |
| Constraints | 1 | 14 |
| Deployment contract | 10 | 28 |
