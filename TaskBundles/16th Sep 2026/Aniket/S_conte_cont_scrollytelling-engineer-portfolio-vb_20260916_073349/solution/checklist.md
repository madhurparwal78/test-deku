# Checklist: Fieldline
Items: 293
Unpinned values flagged: 7
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-1` `capability` The product is one personal portfolio read on a single continuous scroll `src: Overview p1`
- [ ] `C-OV-2` `capability` Each shipped system is presented as a drawing of how the system works `src: Overview p1`
- [ ] `C-OV-3` `capability` The index is one scrubbed timeline of nine bands in a fixed order `src: Overview p1`
- [ ] `C-OV-4` `constraint` An unpublished piece stays closed until the owning author publishes `src: Overview p5`
- [ ] `C-OV-5` `constraint` Publishing is the single act that opens the row, the page, the stored object `src: Overview p5`
- [ ] `C-OV-6` `constraint` The only state a visitor creates is a note, a subscription, a page-view tally `src: Overview p4`

## C-RL User roles

- [ ] `C-RL-1` `role` A signed-out visitor reads any published piece `src: User roles table`
- [ ] `C-RL-2` `role` A signed-out visitor sends a note without an account `src: User roles table`
- [ ] `C-RL-3` `role` A signed-out visitor cannot reach the studio `src: User roles table`
- [ ] `C-RL-4` `role` A signed-out visitor cannot reach the desk `src: User roles table`
- [ ] `C-RL-5` `role` A signed-out visitor cannot read another sender's thread `src: User roles table`
- [ ] `C-RL-6` `role` A reader sees their own notes on the account route `src: User roles table`
- [ ] `C-RL-7` `role` A reader cannot publish anything `src: User roles table`
- [ ] `C-RL-8` `role` An author composes a piece with a diagram in the studio `src: User roles table`
- [ ] `C-RL-9` `role` An author cannot publish a piece owned by another account `src: User roles table`
- [ ] `C-RL-10` `role` An author replies to a note only after pressing send `src: User roles table`

## C-CF Core features

- [ ] `C-CF-1` `capability` Signup is open to anyone from the sign-up route `src: User roles signup policy`
- [ ] `C-CF-2` `literal` Every seeded account signs in with the password `deku-demo-pw-2026` `src: User roles seeded table`
- [ ] `C-CF-3` `literal` The seeded author account is `author@example.com` `src: User roles seeded table`
- [ ] `C-CF-4` `literal` The second seeded author account is `author2@example.com` `src: User roles seeded table`
- [ ] `C-CF-5` `literal` The seeded reader account is `reader@example.com` `src: User roles seeded table`
- [ ] `C-CF-6` `capability` A successful sign in returns a bearer token `src: Core features auth`
- [ ] `C-CF-7` `constraint` A bearer token expires after twelve hours `src: Core features auth`
- [ ] `C-CF-8` `constraint` An expired bearer token is refused `src: Core features auth`
- [ ] `C-CF-9` `constraint` Passwords are stored hashed `src: Core features auth`
- [ ] `C-CF-10` `constraint` Signup lowercases the submitted email `src: Core features auth`
- [ ] `C-CF-11` `constraint` A second signup on a taken email is rejected as invalid `src: Core features rule 1`
- [ ] `C-CF-12` `constraint` A rejected duplicate signup leaves no second account row `src: Core features rule 1`
- [ ] `C-CF-13` `constraint` An invalid form submission names the field that is wrong `src: Core features rule 2`
- [ ] `C-CF-14` `constraint` An invalid form submission writes nothing to the datastore `src: Core features rule 2`
- [ ] `C-CF-15` `contract` The bands endpoint returns a top-level JSON array of nine entries `src: Core features rule 3`
- [ ] `C-CF-16` `data` Each band entry carries a slug, a name, a start fraction, an end fraction `src: Core features rule 3`
- [ ] `C-CF-17` `constraint` The nine band ranges tile from zero to one with no gap `src: Core features rule 3`
- [ ] `C-CF-18` `constraint` The nine band ranges tile from zero to one with no overlap `src: Core features rule 3`
- [ ] `C-CF-19` `literal` The band slugs are `hero`, `manifesto`, `experience`, `philosophy`, `systems`, `open-source`, `stack`, `signal`, `footer` `src: Core features rule 3`
- [ ] `C-CF-20` `ui` The left rail names the band the reader is currently in `src: Core features rule 4`
- [ ] `C-CF-21` `contract` The rail marks the current band with the `aria-current` attribute `src: Core features rule 4`
- [ ] `C-CF-22` `contract` The three in-page top-bar entries scroll to a band rather than navigating `src: Core features rule 4`
- [ ] `C-CF-23` `contract` The blog entry in the top bar navigates to the archive route `src: Core features rule 4`
- [ ] `C-CF-24` `capability` The experience band carries six roles across four employers `src: Core features rule 5`
- [ ] `C-CF-25` `ui` An employer header stays pinned to the top of the screen through the employer's roles `src: Core features rule 5`
- [ ] `C-CF-26` `capability` The philosophy band carries four numbered principles `src: Core features rule 5`
- [ ] `C-CF-27` `capability` The systems band carries five entries `src: Core features rule 5`
- [ ] `C-CF-28` `ui` The first screen carries a turning triangulated wireframe volume `src: Core features wireframe field`
- [ ] `C-CF-29` `ui` The headline sits inside the field in front of the drawn edges `src: Core features wireframe field`
- [ ] `C-CF-30` `constraint` The field is drawn as a single drawing call `src: Core features rule 6`
- [ ] `C-CF-31` `ui` The field dissolves into the page ground rather than ending at a hard edge `src: Core features rule 6`
- [ ] `C-CF-32` `constraint` The field render loop stops once the field is fully covered `src: Core features rule 7`
- [ ] `C-CF-33` `constraint` The field render loop stops once the document is hidden `src: Core features rule 7`
- [ ] `C-CF-34` `constraint` The field falls back to a still frame under a reduced-motion preference `src: Core features rule 8`
- [ ] `C-CF-35` `constraint` The still fallback is vector line geometry rather than a raster image `src: Core features rule 8`
- [ ] `C-CF-36` `data` A diagram is declared as a structure of nodes, edges, annotations, a timeline, a layout `src: Core features diagram language`
- [ ] `C-CF-37` `literal` A node kind is one of `box`, `gate`, `store`, `terminal` `src: Core features rule 9`
- [ ] `C-CF-38` `literal` An edge kind is one of `plain`, `active`, `drift` `src: Core features rule 9`
- [ ] `C-CF-39` `literal` A timeline effect is one of `travel`, `sweep`, `gate`, `promote`, `drift`, `enter`, `pulse` `src: Core features rule 9`
- [ ] `C-CF-40` `contract` The validate endpoint reports every illegal kind with the offending item named `src: Core features rule 9`
- [ ] `C-CF-41` `contract` The validate endpoint reports every edge naming a node that does not exist `src: Core features rule 9`
- [ ] `C-CF-42` `contract` The validate endpoint reports every timeline stop outside zero to one `src: Core features rule 9`
- [ ] `C-CF-43` `constraint` The same structure renders the same drawing on two consecutive renders `src: Core features rule 10`
- [ ] `C-CF-44` `constraint` Two stops on one mark at one instant resolve to the later entry in list order `src: Core features rule 10`
- [ ] `C-CF-45` `ui` One structure renders the tall layout plus the wide layout with no second input `src: Core features rule 11`
- [ ] `C-CF-46` `data` The tall layout runs its stages down a column `src: Core features rule 11`
- [ ] `C-CF-47` `data` The wide layout runs its stages across a row `src: Core features rule 11`
- [ ] `C-CF-48` `data` A system diagram carries a run log of exactly four rows `src: Core features rule 12`
- [ ] `C-CF-49` `ui` Run-log rows complete in order as the diagram is scrolled through `src: Core features rule 12`
- [ ] `C-CF-50` `ui` The waiting run-log row is the only mark in a diagram wearing the accent colour `src: Core features rule 12`
- [ ] `C-CF-51` `data` A status row sits under the run log with a left label plus a right label `src: Core features rule 12`
- [ ] `C-CF-52` `constraint` Every diagram carries a text alternative describing its nodes in order `src: Core features rule 13`
- [ ] `C-CF-53` `constraint` A diagram's animated marks are hidden from assistive technology `src: Core features rule 13`
- [ ] `C-CF-54` `capability` An author composes a piece in a three-step wizard `src: Core features writing drafts studio`
- [ ] `C-CF-55` `ui` Each wizard step sits at its own address `src: Core features writing drafts studio`
- [ ] `C-CF-56` `ui` The diagram step offers a scrub bar driving progress from zero to one `src: Core features writing drafts studio`
- [ ] `C-CF-57` `capability` Creating a piece stores the piece with the draft status `src: Core features rule 14`
- [ ] `C-CF-58` `constraint` Creating a piece derives a unique kebab-case slug from the title `src: Core features rule 14`
- [ ] `C-CF-59` `constraint` A piece takes the next unused number within its own series `src: Core features rule 14`
- [ ] `C-CF-60` `constraint` The engineering series numbers independently of the essay series `src: Core features rule 14`
- [ ] `C-CF-61` `literal` A diagram still is written under the key scheme `diagrams/{diagram_id}/{sha256_of_bytes}.{ext}` `src: Core features rule 15`
- [ ] `C-CF-62` `literal` A piece still is written under the key scheme `posts/{post_id}/{sha256_of_bytes}.{ext}` `src: Core features rule 15`
- [ ] `C-CF-63` `constraint` The row stores the object key rather than the drawn bytes `src: Core features rule 15`
- [ ] `C-CF-64` `constraint` Exporting into a diagram owned by another account is denied `src: Core features rule 15`
- [ ] `C-CF-65` `constraint` A denied export writes no object into the bucket `src: Core features rule 15`
- [ ] `C-CF-66` `constraint` An export is refused when validation reports a finding `src: Core features rule 16`
- [ ] `C-CF-67` `constraint` A failed export leaves no orphaned object in the bucket `src: Core features rule 16`
- [ ] `C-CF-68` `constraint` A draft piece answers only the owning author's session `src: Core features rule 17`
- [ ] `C-CF-69` `constraint` A draft piece still returns no bytes to an anonymous request `src: Core features rule 17`
- [ ] `C-CF-70` `constraint` A draft piece still returns no bytes to the second author account `src: Core features rule 17`
- [ ] `C-CF-71` `constraint` A draft piece never appears in the published listing `src: Core features rule 17`
- [ ] `C-CF-72` `constraint` A draft diagram answers only its owner through the diagram endpoint `src: Core features rule 17`
- [ ] `C-CF-73` `constraint` A published piece answers any requester `src: Core features rule 17`
- [ ] `C-CF-74` `capability` Publishing moves the piece to the published status with a publication timestamp `src: Core features rule 18`
- [ ] `C-CF-75` `constraint` Publishing a piece whose diagram exported no still is rejected as invalid `src: Core features rule 18`
- [ ] `C-CF-76` `constraint` Publishing a piece owned by another account is denied `src: Core features rule 18`
- [ ] `C-CF-77` `constraint` A repeated publish leaves exactly one published piece `src: Core features rule 19`
- [ ] `C-CF-78` `constraint` A repeated publish leaves the stored object key unchanged `src: Core features rule 19`
- [ ] `C-CF-79` `constraint` Two simultaneous publishes of one draft accept exactly one `src: Core features rule 19`
- [ ] `C-CF-80` `ui` The fixed contact control opens a panel over the page rather than navigating `src: Core features contact channel`
- [ ] `C-CF-81` `contract` The contact panel is also reachable at its own address `src: Core features contact channel`
- [ ] `C-CF-82` `constraint` A note name shorter than `2` characters is rejected as invalid `src: Core features rule 20`
- [ ] `C-CF-83` `constraint` A note name longer than `80` characters is rejected as invalid `src: Core features rule 20`
- [ ] `C-CF-84` `literal` A note intent is one of `Hiring`, `Consulting`, `Collaboration`, `Something else` `src: Core features rule 20`
- [ ] `C-CF-85` `constraint` A note message shorter than `20` characters is rejected as invalid `src: Core features rule 20`
- [ ] `C-CF-86` `constraint` A note message longer than `4000` characters is rejected as invalid `src: Core features rule 20`
- [ ] `C-CF-87` `ui` The budget band appears only when the intent is the consulting option `src: Core features rule 20`
- [ ] `C-CF-88` `constraint` A rejected note keeps everything the sender typed `src: Core features rule 20`
- [ ] `C-CF-89` `contract` Creating a note returns a thread token `src: Core features rule 21`
- [ ] `C-CF-90` `data` A stored note records the band the reader was in when the panel opened `src: Core features rule 21`
- [ ] `C-CF-91` `constraint` A thread token reaches exactly one note `src: Core features rule 21`
- [ ] `C-CF-92` `constraint` A thread token appears in no listing anywhere in the product `src: Core features rule 21`
- [ ] `C-CF-93` `constraint` A request for a note without its token answers not found `src: Core features rule 21`
- [ ] `C-CF-94` `capability` A sender adds a message to their own thread `src: Core features rule 22`
- [ ] `C-CF-95` `constraint` A sender cannot delete a note `src: Core features rule 22`
- [ ] `C-CF-96` `capability` Subscribing records the address in the pending state `src: Core features rule 23`
- [ ] `C-CF-97` `constraint` A pending address is on no list until the confirmation link is followed `src: Core features rule 23`
- [ ] `C-CF-98` `constraint` A confirmation token expires after `7` days `src: Core features rule 23`
- [ ] `C-CF-99` `constraint` An expired confirmation token is refused as gone `src: Core features rule 23`
- [ ] `C-CF-100` `capability` The unsubscribe link moves the address to the unsubscribed state in one action `src: Core features rule 23`
- [ ] `C-CF-101` `constraint` A fourth note from one address inside an hour is refused `src: Core features rule 24`
- [ ] `C-CF-102` `constraint` A refused note leaves no fourth note row `src: Core features rule 24`
- [ ] `C-CF-103` `literal` A rate-limited submission answers `That is a few too many in an hour. Try again later.` `src: Core features rule 24`
- [ ] `C-CF-104` `data` A note's sorting total is computed once at creation from six signals `src: Core features rule 25`
- [ ] `C-CF-105` `ui` The desk prints the six signal weights on screen `src: Core features rule 25`
- [ ] `C-CF-106` `literal` A note whose total reaches `4` lands in the `signal` lane `src: Core features rule 26`
- [ ] `C-CF-107` `literal` A note whose total sits from `0` to `3` lands in the `unsorted` lane `src: Core features rule 26`
- [ ] `C-CF-108` `literal` A note whose total falls below zero lands in the `likely noise` lane `src: Core features rule 26`
- [ ] `C-CF-109` `constraint` No note is ever deleted by the sorting pass `src: Core features rule 26`
- [ ] `C-CF-110` `ui` The noise lane is presented collapsed with reopening available in one action `src: Core features rule 26`
- [ ] `C-CF-111` `constraint` A note arriving when sorting cannot run is stored with no lane `src: Core features rule 27`
- [ ] `C-CF-112` `contract` The desk shows three lanes `src: Core features rule 28`
- [ ] `C-CF-113` `data` A desk card carries the sender's name, the intent, the first two lines, the age `src: Core features rule 28`
- [ ] `C-CF-114` `literal` The desk card actions are `Reply`, `Snooze`, `Close`, `Mark noise` `src: Core features rule 28`
- [ ] `C-CF-115` `constraint` No reply leaves the desk without the author pressing send `src: Core features rule 28`
- [ ] `C-CF-116` `capability` A note in the best lane is offered three slots from the next two weeks `src: Core features rule 29`
- [ ] `C-CF-117` `constraint` A booking holds a slot for `10` minutes before the hold expires `src: Core features rule 29`
- [ ] `C-CF-118` `constraint` An abandoned hold expires with the slot returned to the offer `src: Core features rule 29`
- [ ] `C-CF-119` `constraint` Two bookings for one slot confirm exactly one `src: Core features rule 29`
- [ ] `C-CF-120` `constraint` A refused booking leaves no slot stuck in the held state `src: Core features rule 29`
- [ ] `C-CF-121` `ui` A first-time visitor is asked once about non-essential cookies `src: Core features rule 30`
- [ ] `C-CF-122` `constraint` The cookie answer survives a reload `src: Core features rule 30`
- [ ] `C-CF-123` `ui` The cookie refusal sits beside the acceptance at the same size, the same reach `src: Core features rule 30`
- [ ] `C-CF-124` `data` A page view is recorded with its route, the day, the deepest band reached `src: Core features rule 31`
- [ ] `C-CF-125` `constraint` A page-view record holds no value that could identify one reader `src: Core features rule 31`
- [ ] `C-CF-126` `constraint` The page-view aggregate answers the author account only `src: Core features rule 31`
- [ ] `C-CF-127` `constraint` Every internal link on every public route resolves `src: Core features rule 32`
- [ ] `C-CF-128` `literal` An unknown address renders the code `404` `src: Core features rule 33`
- [ ] `C-CF-129` `literal` The not-found page carries the pinned single-line explanation `src: Core features rule 33`
- [ ] `C-CF-130` `literal` The not-found page carries the action `Return home` `src: Core features rule 33`
- [ ] `C-CF-131` `ui` The not-found page keeps the top bar with the rail absent `src: Core features rule 33`
- [ ] `C-CF-132` `capability` A privacy page is reachable from the footer of every route `src: Core features rule 34`
- [ ] `C-CF-133` `literal` The privacy page states a retention window of `13` months `src: Core features rule 34`

## C-UF User flow

- [ ] `C-UF-1` `contract` The index route is public `src: User flow route table`
- [ ] `C-UF-2` `contract` The archive route is public `src: User flow route table`
- [ ] `C-UF-3` `contract` The studio route answers an author session only `src: User flow route table`
- [ ] `C-UF-4` `contract` The desk route answers an author session only `src: User flow route table`
- [ ] `C-UF-5` `contract` The account route answers a signed-in session only `src: User flow route table`
- [ ] `C-UF-6` `constraint` A signed-out request for a protected route lands on the sign-in route `src: User flow entry and redirects`
- [ ] `C-UF-7` `constraint` A successful sign in returns to the route that was asked for `src: User flow entry and redirects`
- [ ] `C-UF-8` `constraint` An author signing in with no pending destination lands on the studio `src: User flow entry and redirects`
- [ ] `C-UF-9` `constraint` A reader signing in with no pending destination lands on the account route `src: User flow entry and redirects`
- [ ] `C-UF-10` `constraint` A reader reaching the studio is refused with a message naming the author account `src: User flow entry and redirects`
- [ ] `C-UF-11` `constraint` A signed-out request for a draft piece renders the not-found page `src: User flow entry and redirects`
- [ ] `C-UF-12` `constraint` A thread link with no note behind the token renders the not-found page `src: User flow entry and redirects`
- [ ] `C-UF-13` `ui` Every list carries an empty state naming the absence in one sentence `src: User flow states`
- [ ] `C-UF-14` `literal` The empty desk reads `Nothing waiting` over the pinned arrival sentence `src: User flow states`
- [ ] `C-UF-15` `literal` The empty diagram editor reads `No diagram open` over `Create one or open an existing diagram to begin.` `src: User flow states`
- [ ] `C-UF-16` `ui` A loading state is shimmering blocks in the shape of the final layout `src: User flow states`
- [ ] `C-UF-17` `ui` An error renders inside the page chrome with a retry repeating the same request `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-1` `ui` The page reads as an evenly stepped neutral ramp `src: UI/UX notes colour`
- [ ] `C-UX-2` `ui` Exactly one saturated colour appears in the whole interface `src: UI/UX notes colour`
- [ ] `C-UX-3` `ui` The accent is a mid, vivid orange carrying the rail marker `src: UI/UX notes colour`
- [ ] `C-UX-4` `ui` The accent carries the current band name, the contact control, the waiting run-log row `src: UI/UX notes colour`
- [ ] `C-UX-5` `ui` A deep, soft blue is the second signal confined to the principle number `src: UI/UX notes colour`
- [ ] `C-UX-6` `ui` A light, soft blue carries inline links in long-form writing `src: UI/UX notes colour`
- [ ] `C-UX-7` `ui` Prose sits in one family with every label, figure, timestamp, annotation in a mono family `src: UI/UX notes type`
- [ ] `C-UX-8` `ui` Long-form measure is capped near sixty characters `src: UI/UX notes type`
- [ ] `C-UX-9` `ui` Figures line up in a column wherever values stack `src: UI/UX notes type`
- [ ] `C-UX-10` `ui` Bands separate by space rather than by a dividing line `src: UI/UX notes shape and density`
- [ ] `C-UX-11` `ui` Density is spacious in the reading bands, compact in the studio grid `src: UI/UX notes shape and density`
- [ ] `C-UX-12` `ui` One house ease governs every hover, entrance, scrubbed reveal `src: UI/UX notes motion`
- [ ] `C-UX-13` `ui` The headline arrives word by word sharpening from a blur `src: UI/UX notes motion`
- [ ] `C-UX-14` `ui` A gate mark collapses to a sliver of its height, dims, stays there `src: UI/UX notes motion`
- [ ] `C-UX-15` `ui` A promote mark draws a path in, then retracts `src: UI/UX notes motion`
- [ ] `C-UX-16` `constraint` A reduced-motion preference holds the field on its first frame `src: UI/UX notes reduced motion`
- [ ] `C-UX-17` `constraint` A reduced-motion preference renders every diagram in its final state `src: UI/UX notes reduced motion`
- [ ] `C-UX-18` `constraint` The counter keeps counting under a reduced-motion preference `src: UI/UX notes reduced motion`
- [ ] `C-UX-19` `constraint` Body text meets WCAG AA contrast against the page ground `src: UI/UX notes accessibility`
- [ ] `C-UX-20` `constraint` Every control carries a visible focus ring under keyboard navigation `src: UI/UX notes accessibility`
- [ ] `C-UX-21` `constraint` The contact panel traps focus, returns focus to the opening control `src: UI/UX notes accessibility`
- [ ] `C-UX-22` `constraint` The contact panel closes on the escape key `src: UI/UX notes accessibility`
- [ ] `C-UX-23` `constraint` Scrolling to a band from the top bar moves keyboard focus to that band `src: UI/UX notes accessibility`
- [ ] `C-UX-24` `constraint` The wireframe field is hidden from assistive technology `src: UI/UX notes accessibility`
- [ ] `C-UX-25` `constraint` Nothing overflows sideways at a narrow viewport `src: UI/UX notes responsive`
- [ ] `C-UX-26` `ui` The rail is hidden at a narrow viewport with the contact control a full-width bar `src: UI/UX notes responsive`
- [ ] `C-UX-27` `ui` Diagrams take the tall layout at a narrow viewport `src: UI/UX notes responsive`
- [ ] `C-UX-28` `ui` Each route leads with one primary action distinct from every secondary one `src: UI/UX notes one primary action`
- [ ] `C-UX-29` `ui` Every control carries a resting, pointed-at, pressed, focused, unavailable state `src: UI/UX notes component states`

## C-TR Technical requirements

- [ ] `C-TR-1` `contract` Each route is rendered on the server as a complete document `src: Technical requirements p1`
- [ ] `C-TR-2` `contract` The first response carries every diagram's final geometry as markup `src: Technical requirements p2`
- [ ] `C-TR-3` `literal` The datastore address is read from `DATABASE_URL` `src: Technical requirements p1`
- [ ] `C-TR-4` `literal` The object-store address is read from `STORAGE_ENDPOINT` `src: Technical requirements p1`
- [ ] `C-TR-5` `literal` The object-store bucket is read from `STORAGE_BUCKET` `src: Technical requirements p1`
- [ ] `C-TR-6` `contract` The health endpoint answers once the app is ready `src: Technical requirements p1`
- [ ] `C-TR-7` `constraint` No host, port, credential is hardcoded anywhere in the app `src: Technical requirements p3`
- [ ] `C-TR-8` `constraint` No second datastore, cache, queue, object store, mail vendor is introduced `src: Technical requirements p4`
- [ ] `C-TR-9` `constraint` No message of any kind leaves the application `src: Technical requirements no message`
- [ ] `C-TR-10` `data` An outbound message is recorded as a row with a recipient, a kind, a delivery state `src: Technical requirements no message`
- [ ] `C-TR-11` `constraint` No credential appears in anything the browser downloads `src: Technical requirements no secret`
- [ ] `C-TR-12` `constraint` The object store is reached by the server only `src: Technical requirements no secret`
- [ ] `C-TR-13` `capability` The site serves a favicon declared in the document head `src: Technical requirements site icon`
- [ ] `C-TR-14` `constraint` The archive route creates no drawing context `src: Technical requirements performance`
- [ ] `C-TR-15` `constraint` Nothing in the scroll path writes a layout property `src: Technical requirements performance`
- [ ] `C-TR-16` `constraint` Nothing reflows once the fonts finish loading `src: Technical requirements performance`
- [ ] `C-TR-17` `ui` The counter climbs continuously from the elapsed time on the page `src: Technical requirements live counter`
- [ ] `C-TR-18` `literal` The counter carries the pinned synapse phrase beside its figure `src: Technical requirements live counter`
- [ ] `C-TR-19` `constraint` The counter never resets on scroll `src: Technical requirements live counter`

## C-DM Data model

- [ ] `C-DM-1` `data` The datastore carries sixteen tables `src: Data model p1`
- [ ] `C-DM-2` `data` Every timestamp is stored in UTC `src: Data model p1`
- [ ] `C-DM-3` `data` An account row carries an email stored lowercase, a password hash, a display name, a role `src: Data model accounts`
- [ ] `C-DM-4` `constraint` An account email is unique across the accounts table `src: Data model accounts`
- [ ] `C-DM-5` `data` A career role row carries an employer, a city, a title, a start date, an end date, a summary `src: Data model career_roles`
- [ ] `C-DM-6` `data` A system row carries a position, a year, a title, a subtitle, a status, a contribution `src: Data model systems`
- [ ] `C-DM-7` `data` A diagram row stores a structure, a text alternative, an owner, a status, an object key `src: Data model diagrams`
- [ ] `C-DM-8` `literal` A diagram's sampled series is a fixed table of `70` values `src: Data model diagrams`
- [ ] `C-DM-9` `data` A post row carries a slug, a series, a number, a title, a body, a status, an object key `src: Data model posts`
- [ ] `C-DM-10` `constraint` A post number is unique within its own series `src: Data model posts`
- [ ] `C-DM-11` `data` A note row carries an intent, a state, a lane, a thread token, a creation timestamp `src: Data model notes`
- [ ] `C-DM-12` `data` A note message row carries an author kind of sender or owner `src: Data model note_messages`
- [ ] `C-DM-13` `data` A subscriber row carries a lowercased email, a state, a confirm token, an unsubscribe token `src: Data model subscribers`
- [ ] `C-DM-14` `constraint` A subscriber email is unique across the subscribers table `src: Data model subscribers`
- [ ] `C-DM-15` `data` A page-view row is one row per route per day carrying a count, a deepest band `src: Data model page_views`
- [ ] `C-DM-16` `data` A booking row carries a start time, a state, a hold expiry `src: Data model bookings`
- [ ] `C-DM-17` `literal` The first seeded published piece carries the pinned video-map headline `src: Data model seed data`
- [ ] `C-DM-18` `literal` The second seeded published piece is `A developer's guide to taste in the age of AI` `src: Data model seed data`
- [ ] `C-DM-19` `literal` The seeded draft piece is `Everything I got wrong about retrieval` `src: Data model seed data`
- [ ] `C-DM-20` `literal` The first seeded system is `Ferrite` `src: Data model seed data`
- [ ] `C-DM-21` `literal` The client system carries the pinned confidentiality line `src: Data model seed data`
- [ ] `C-DM-22` `literal` The index headline reads `I build machines that read the world.` `src: Data model seed data`
- [ ] `C-DM-23` `literal` The manifesto line reads `I learned engineering from broken things.` `src: Data model seed data`
- [ ] `C-DM-24` `literal` The role line reads `AI Engineer / Founder of Ferrite / Halifax` `src: Data model seed data`
- [ ] `C-DM-25` `constraint` Seeding is idempotent across a restart `src: Data model close`

## C-FE Front-end specification

- [ ] `C-FE-1` `capability` A fixed top bar spans the full width on every route `src: Front-end specification top bar`
- [ ] `C-FE-2` `literal` The top-bar entries read `blog`, `systems`, `open source`, `signal` `src: Front-end specification top bar`
- [ ] `C-FE-3` `ui` A theme control is the only control in the chrome carrying a name plus a pressed state `src: Front-end specification top bar`
- [ ] `C-FE-4` `ui` The rail is a vertical ruler of hairline ticks with a longer mark at each band boundary `src: Front-end specification left rail`
- [ ] `C-FE-5` `literal` The fixed contact control is labelled `LET'S TALK` `src: Front-end specification contact button`
- [ ] `C-FE-6` `literal` The footer credit reads `Designed by Studio Halvard` `src: Front-end specification footer`
- [ ] `C-FE-7` `ui` Four drawn glyphs exist as geometry rather than as a font `src: Front-end specification iconography`
- [ ] `C-FE-8` `ui` Depth runs field, overlay gradients, content, diagram overlay, rail, top bar, curtain `src: Front-end specification surfaces`
- [ ] `C-FE-9` `ui` A small share of field edges take thread hues chosen as connected paths `src: Front-end specification wireframe field`
- [ ] `C-FE-10` `ui` A radial scrim sits behind the headline keeping the type readable over the mesh `src: Front-end specification wireframe field`
- [ ] `C-FE-11` `data` Every diagram is built from seven kinds of mark with no eighth `src: Front-end specification diagram language`
- [ ] `C-FE-12` `ui` The index scrolls smoothly with several diagrams playing at once `src: Front-end specification scroll system`
- [ ] `C-FE-13` `data` Each diagram maps its own range to one normalised value every mark reads `src: Front-end specification scroll system`
- [ ] `C-FE-14` `literal` The hero cue reads `scroll down` `src: Front-end specification route index`
- [ ] `C-FE-15` `literal` The philosophy divider reads `HOW I BUILD` `src: Front-end specification route index`
- [ ] `C-FE-16` `literal` The systems heading reads `Things people depend on at work.` `src: Front-end specification route index`
- [ ] `C-FE-17` `literal` The contribution label reads `MY PART:` `src: Front-end specification route index`
- [ ] `C-FE-18` `literal` The archive subtitle is the pinned frequency-log line `src: Front-end specification route archive`
- [ ] `C-FE-19` `ui` An archive entry carries a bracketed code beside a date in the mono family `src: Front-end specification route archive`
- [ ] `C-FE-20` `ui` The reading column is offset left rather than centred `src: Front-end specification route piece`
- [ ] `C-FE-21` `literal` The contact panel is titled `Send a signal` `src: Front-end specification contact panel`
- [ ] `C-FE-22` `literal` The panel subtitle reads `A sentence about what you are working on is plenty.` `src: Front-end specification contact panel`
- [ ] `C-FE-23` `literal` A short message answers `A little more detail would help.` `src: Front-end specification contact panel`
- [ ] `C-FE-24` `literal` An invalid address answers `That address does not look right.` `src: Front-end specification contact panel`
- [ ] `C-FE-25` `ui` The studio index is a grid of cards, one per piece, one per diagram `src: Front-end specification studio and desk`
- [ ] `C-FE-26` `ui` Saving, validating, exporting, publishing report in an inline banner inside the page `src: Front-end specification studio and desk`
- [ ] `C-FE-27` `ui` The field, the diagrams are the only moving surfaces on the index `src: Front-end specification module architecture`
- [ ] `C-FE-28` `constraint` No image file, video file, font file ships with the build `src: Front-end specification zero-asset`
- [ ] `C-FE-29` `ui` Each repository row carries a name, a one-line description, a language chip `src: Front-end specification route index`

## C-CN Constraints

- [ ] `C-CN-1` `constraint` There is one portfolio with no tenancy of any kind `src: Constraints p1`
- [ ] `C-CN-2` `constraint` No comment, like, reaction, follower graph, direct message exists `src: Constraints p2`
- [ ] `C-CN-3` `constraint` No payment, pricing, money movement exists anywhere in the product `src: Constraints p2`
- [ ] `C-CN-4` `constraint` No third-party analytics service is called `src: Constraints p2`
- [ ] `C-CN-5` `constraint` No external reputation service feeds the note sorting `src: Constraints p2`
- [ ] `C-CN-6` `constraint` No external network call is made at runtime beyond the two backing services `src: Constraints p2`
- [ ] `C-CN-7` `constraint` The stack band is authored content stating nothing about how the app is built `src: Constraints p3`
- [ ] `C-CN-8` `constraint` The archive renders its full seeded list without the page stalling `src: Constraints p5`

## C-DC Deployment contract

- [ ] `C-DC-1` `contract` The app is reachable at the public address environment variable `src: Deployment contract`
- [ ] `C-DC-2` `literal` The container-internal port is `4173` `src: Deployment contract`
- [ ] `C-DC-3` `contract` The HTTP API is served on the same origin under the api prefix `src: Deployment contract`
- [ ] `C-DC-4` `contract` The health endpoint returns success once the app is ready `src: Deployment contract`
- [ ] `C-DC-5` `contract` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-6` `literal` Login credentials are written to `/app/USER_README.md` `src: Deployment contract`
- [ ] `C-DC-7` `literal` The reserved directory `.browser_screenshots/` exists at the app root `src: Deployment contract`
- [ ] `C-DC-8` `literal` The reserved directory `.downloads/` exists at the app root `src: Deployment contract`
- [ ] `C-DC-9` `constraint` A production build is served rather than a development server `src: Deployment contract`
- [ ] `C-DC-10` `constraint` The server keeps running after the session ends `src: Deployment contract`
- [ ] `C-DC-11` `literal` The listener binds `0.0.0.0` `src: Deployment contract`
- [ ] `C-DC-12` `constraint` No backing service is downloaded, installed, started by the app `src: Deployment contract`
- [ ] `C-DC-13` `constraint` No persistent volume is declared by the app `src: Deployment contract`
- [ ] `C-DC-14` `contract` A list endpoint returns a top-level JSON array `src: Deployment contract api shapes`
- [ ] `C-DC-15` `contract` An invalid call is rejected as a client error `src: Deployment contract api shapes`
- [ ] `C-DC-16` `contract` An unauthorized call is never answered with a success shape `src: Deployment contract api shapes`
- [ ] `C-DC-17` `constraint` Exported still bytes live in the bucket rather than on the app's own disk `src: Deployment contract no mocks`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the password every seeded account uses | `C-CF-2` |
| `author@example.com` | the seeded author account | `C-CF-3` |
| `author2@example.com` | the second seeded author account | `C-CF-4` |
| `reader@example.com` | the seeded reader account | `C-CF-5` |
| `hero` | the first band slug | `C-CF-19` |
| `manifesto` | the second band slug | `C-CF-19` |
| `experience` | the third band slug | `C-CF-19` |
| `philosophy` | the fourth band slug | `C-CF-19` |
| `systems` | the fifth band slug | `C-CF-19` |
| `open-source` | the sixth band slug | `C-CF-19` |
| `stack` | the seventh band slug | `C-CF-19` |
| `signal` | the eighth band slug | `C-CF-19` |
| `footer` | the ninth band slug | `C-CF-19` |
| `box` | the first legal node kind | `C-CF-37` |
| `gate` | the second legal node kind, also a timeline effect | `C-CF-37` |
| `store` | the third legal node kind | `C-CF-37` |
| `terminal` | the fourth legal node kind | `C-CF-37` |
| `plain` | the first legal edge kind | `C-CF-38` |
| `active` | the second legal edge kind | `C-CF-38` |
| `drift` | the third legal edge kind, also a timeline effect | `C-CF-38` |
| `travel` | the mark-in-transit timeline effect | `C-CF-39` |
| `sweep` | the whole-drawing traverse timeline effect | `C-CF-39` |
| `promote` | the draw-in-then-retract timeline effect | `C-CF-39` |
| `enter` | the rise-and-fade timeline effect | `C-CF-39` |
| `pulse` | the node-under-load timeline effect | `C-CF-39` |
| `diagrams/{diagram_id}/{sha256_of_bytes}.{ext}` | the diagram still key scheme | `C-CF-61` |
| `posts/{post_id}/{sha256_of_bytes}.{ext}` | the piece still key scheme | `C-CF-62` |
| `2` | the shortest legal note name | `C-CF-82` |
| `80` | the longest legal note name | `C-CF-83` |
| `Hiring` | the first note intent | `C-CF-84` |
| `Consulting` | the second note intent | `C-CF-84` |
| `Collaboration` | the third note intent | `C-CF-84` |
| `Something else` | the fourth note intent | `C-CF-84` |
| `20` | the shortest legal note message | `C-CF-85` |
| `4000` | the longest legal note message | `C-CF-86` |
| `7` | the confirmation token lifetime in days | `C-CF-98` |
| `That is a few too many in an hour. Try again later.` | the rate-limit message | `C-CF-103` |
| `4` | the lane floor for the best lane | `C-CF-106` |
| `0` | the lane floor for the middle lane | `C-CF-107` |
| `3` | the lane ceiling for the middle lane | `C-CF-107` |
| `signal` | the best lane name | `C-CF-106` |
| `unsorted` | the middle lane name | `C-CF-107` |
| `likely noise` | the lowest lane name | `C-CF-108` |
| `Reply` | the first desk card action | `C-CF-114` |
| `Snooze` | the second desk card action | `C-CF-114` |
| `Close` | the third desk card action | `C-CF-114` |
| `Mark noise` | the fourth desk card action | `C-CF-114` |
| `10` | the slot hold in minutes | `C-CF-117` |
| `404` | the not-found code | `C-CF-128` |
| `This page could not be found.` | the not-found line | `C-CF-129` |
| `Return home` | the not-found action | `C-CF-130` |
| `13` | the page-view retention window in months | `C-CF-133` |
| `Nothing waiting` | the empty desk title | `C-UF-14` |
| `Notes appear here as they arrive.` | the empty desk sentence | `C-UF-14` |
| `No diagram open` | the empty editor title | `C-UF-15` |
| `Create one or open an existing diagram to begin.` | the empty editor sentence | `C-UF-15` |
| `DATABASE_URL` | the datastore connection variable | `C-TR-3` |
| `STORAGE_ENDPOINT` | the object-store address variable | `C-TR-4` |
| `STORAGE_BUCKET` | the object-store bucket variable | `C-TR-5` |
| `synapses fired while you're here` | the counter phrase | `C-TR-18` |
| `70` | the number of sampled values in a diagram series | `C-DM-8` |
| `Most video AI gives you bullet points. I built one that gives you a map.` | the first seeded published piece | `C-DM-17` |
| `A developer's guide to taste in the age of AI` | the second seeded published piece | `C-DM-18` |
| `Everything I got wrong about retrieval` | the seeded draft piece | `C-DM-19` |
| `Ferrite` | the first seeded system | `C-DM-20` |
| `Client system. The names, the internals, and the data stay with the client.` | the confidentiality line | `C-DM-21` |
| `I build machines that read the world.` | the index headline | `C-DM-22` |
| `I learned engineering from broken things.` | the manifesto line | `C-DM-23` |
| `AI Engineer / Founder of Ferrite / Halifax` | the role line | `C-DM-24` |
| `blog` | the first top-bar entry | `C-FE-2` |
| `systems` | the second top-bar entry | `C-FE-2` |
| `open source` | the third top-bar entry | `C-FE-2` |
| `signal` | the fourth top-bar entry | `C-FE-2` |
| `LET'S TALK` | the fixed contact control label | `C-FE-5` |
| `Designed by Studio Halvard` | the footer credit | `C-FE-6` |
| `scroll down` | the hero cue | `C-FE-14` |
| `HOW I BUILD` | the philosophy divider | `C-FE-15` |
| `Things people depend on at work.` | the systems heading | `C-FE-16` |
| `MY PART:` | the contribution label | `C-FE-17` |
| `Frequency log - tuning into thoughts on AI, taste, and craft` | the archive subtitle | `C-FE-18` |
| `Send a signal` | the contact panel title | `C-FE-21` |
| `A sentence about what you are working on is plenty.` | the panel subtitle | `C-FE-22` |
| `A little more detail would help.` | the short-message message | `C-FE-23` |
| `That address does not look right.` | the invalid-address message | `C-FE-24` |
| `4173` | the container-internal port | `C-DC-2` |
| `/app/USER_README.md` | the credential file path | `C-DC-6` |
| `.browser_screenshots/` | the reserved screenshot directory | `C-DC-7` |
| `.downloads/` | the reserved download directory | `C-DC-8` |
| `0.0.0.0` | the bind address | `C-DC-11` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact colour values behind every named role | `C-UX-2` |
| the exact type families behind the stated split | `C-UX-7` |
| the exact type sizes behind the stated hierarchy | `C-UX-8` |
| the exact motion timings behind the stated character | `C-UX-12` |
| the exact breakpoint widths behind the stated behaviour | `C-UX-25` |
| the exact spacing base unit behind the stated rhythm | `C-UX-10` |
| the exact vertex count behind the stated field character | `C-FE-9` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 3 | 6 |
| User roles | 2 | 10 |
| Core features | 34 | 133 |
| User flow | 4 | 17 |
| UI and UX notes | 8 | 29 |
| Technical requirements | 7 | 19 |
| Data model | 5 | 25 |
| Front-end specification | 9 | 29 |
| Constraints | 3 | 8 |
| Deployment contract | 12 | 17 |
