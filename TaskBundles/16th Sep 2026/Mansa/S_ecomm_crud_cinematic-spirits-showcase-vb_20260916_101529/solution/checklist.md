# Checklist: cinematic-spirits-showcase-vb

Items: 501
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC
Unpinned values flagged: 5

## C-OV Overview

- [ ] `C-OV-01` `capability` The Nocturne Collection is three flavours of one bottle `src: Overview`
- [ ] `C-OV-02` `literal` The three flavours are `MARSHMALLOW COFFEE & CREAM`, `ORANGE CHOCOLATE & CREAM`, `MINT CHOCOLATE & CREAM` `src: Overview`
- [ ] `C-OV-03` `literal` Each flavour is `13% ABV` in a `700 ML` bottle `src: Overview`
- [ ] `C-OV-04` `capability` One continuous rendered scene fills the whole window, eighteen chapters long `src: Overview`
- [ ] `C-OV-05` `capability` The document underneath the film never scrolls `src: Overview`
- [ ] `C-OV-06` `ui` Every surface, figure, column, cloud carries engraved parallel lines that stay stuck to the surface as the surface moves `src: Overview`
- [ ] `C-OV-07` `ui` The palette is ink, paper, one saturated red, with the three flavour tints as the only other colours in the film `src: Overview`
- [ ] `C-OV-08` `ui` The bottle with the cocktail glass are the only two objects drawn realistically `src: Overview`
- [ ] `C-OV-09` `capability` Four additions are reachable only from the last quarter of the film `src: Overview`
- [ ] `C-OV-10` `constraint` The product offers no cart, no checkout, no payment of any kind `src: Overview`
- [ ] `C-OV-11` `constraint` The product runs no third-party analytics, no advertising `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` Signup is open: anybody opens a `visitor` account by asking for a sign-in link `src: User roles`
- [ ] `C-RL-02` `role` An anonymous caller cannot hold a bottle, set an alert, hold seats, book, save a ritual `src: User roles table`
- [ ] `C-RL-03` `role` A `visitor` confirms allocations on the visitor's own shelf `src: User roles table`
- [ ] `C-RL-04` `role` A `visitor` cannot release another visitor's allocation `src: User roles table`
- [ ] `C-RL-05` `role` A `visitor` cannot change any venue's stock reading `src: User roles table`
- [ ] `C-RL-06` `role` A `visitor` cannot cancel a tasting session `src: User roles table`
- [ ] `C-RL-07` `role` A `host` changes the stock readings of the host's own venue `src: User roles table`
- [ ] `C-RL-08` `role` A `host` cancels sessions of the host's own venue `src: User roles table`
- [ ] `C-RL-09` `role` A `host` cannot change another venue's readings `src: User roles`
- [ ] `C-RL-10` `role` A `host` cannot cancel another venue's sessions `src: User roles`
- [ ] `C-RL-11` `role` A `visitor` cannot read the host venue surface `src: User roles`
- [ ] `C-RL-12` `contract` Authorization runs server-side on every mutating endpoint, leaving the protected state unchanged on a denial `src: User roles`
- [ ] `C-RL-13` `role` Nobody edits or deletes another visitor's ritual `src: User roles`
- [ ] `C-RL-14` `literal` The seeded accounts are `visitor@example.com`, `visitor2@example.com`, `host@example.com`, `host2@example.com` `src: User roles`
- [ ] `C-RL-15` `literal` Every seeded account uses the password `deku-demo-pw-2026` `src: User roles`
- [ ] `C-RL-16` `literal` `host@example.com` is host of `The Gilded Nave` `src: User roles`
- [ ] `C-RL-17` `literal` `host2@example.com` is host of `Salt & Vesper` `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `literal` Seeded accounts sign in at `POST /api/auth/login`, receiving `access_token` `src: Core features rule 1`
- [ ] `C-CF-02` `capability` A wrong password is denied without saying which half was wrong `src: Core features rule 1`
- [ ] `C-CF-03` `literal` `POST /api/v1/auth/link` answers `202` whether an account exists or not `src: Core features rule 2`
- [ ] `C-CF-04` `literal` The sign-in message subject is exactly `Your Vesperi sign-in link` `src: Core features rule 2`
- [ ] `C-CF-05` `literal` The first body line of the sign-in message reads `Sign-in code:` followed by the code `src: Core features rule 2`
- [ ] `C-CF-06` `capability` The second body line of the sign-in message carries the link holding the code `src: Core features rule 2`
- [ ] `C-CF-07` `capability` The sign-in message goes to the requesting address only, with no cc, no bcc `src: Core features rule 2`
- [ ] `C-CF-08` `literal` `POST /api/v1/auth/session` exchanges a code for `session` `src: Core features rule 3`
- [ ] `C-CF-09` `capability` A sign-in code works once within the code's ten-minute life `src: Core features rule 3`
- [ ] `C-CF-10` `capability` A sign-in code is at least 24 characters of letters, digits, hyphen, underscore `src: Core features rule 2`
- [ ] `C-CF-11` `literal` An unknown or expired code is denied with the reason `invalid_token` `src: Core features rule 3`
- [ ] `C-CF-12` `capability` An address with no account becomes a visitor account on the first exchange `src: Core features rule 4`
- [ ] `C-CF-13` `constraint` Asking for a sign-in link creates no account `src: Core features rule 4`
- [ ] `C-CF-14` `constraint` An account opened by a link stores no password `src: Core features rule 4`
- [ ] `C-CF-15` `literal` `GET /api/v1/me` returns the account's `email` with the account's `role` `src: Core features rule 5`
- [ ] `C-CF-16` `capability` A request with no token, an unknown token or a malformed token is denied `src: Core features rule 5`
- [ ] `C-CF-17` `literal` `POST /api/auth/logout` ends the session, after which the same token is denied `src: Core features rule 5`
- [ ] `C-CF-18` `capability` Sessions last 14 days from creation `src: Core features rule 6`
- [ ] `C-CF-19` `capability` The role comes from the token on the server, never from the client `src: Core features rule 6`
- [ ] `C-CF-20` `capability` A signed-out visitor pressing an account control returns to the same place with the action completed `src: Core features rule 7`
- [ ] `C-CF-21` `literal` The whole film lives on `/` `src: Core features rule 8`
- [ ] `C-CF-22` `capability` Wheel, trackpad, touch, key input turns into one story position `src: Core features rule 8`
- [ ] `C-CF-23` `capability` Driving the story backwards returns every chapter to the frame shown on the way forward `src: Core features rule 9`
- [ ] `C-CF-24` `capability` A flick keeps travelling, then slows to a stop `src: Core features rule 9`
- [ ] `C-CF-25` `capability` Stopping the input stops the picture within one frame `src: Core features rule 9`
- [ ] `C-CF-26` `constraint` The story position has no rubber band at either end `src: Core features rule 9`
- [ ] `C-CF-27` `capability` A full pass takes roughly two minutes of steady scrolling `src: Core features rule 10`
- [ ] `C-CF-28` `capability` Arrow keys with page keys step the story, with `Home` with `End` jumping to either end `src: Core features rule 11`
- [ ] `C-CF-29` `literal` The chapters run in a fixed order from `wander` to `footer` `src: Core features rule 12`
- [ ] `C-CF-30` `capability` Moving between two chapters is a blend of contributions, never a cut `src: Core features rule 12`
- [ ] `C-CF-31` `literal` The title lockup reads `THE NOCTURNE EXPERIENCE` `src: Core features rule 13`
- [ ] `C-CF-32` `ui` The hooded figure walks left to right through mist on paper in three comic panels `src: Core features rule 13`
- [ ] `C-CF-33` `ui` The monolith stands under a hatched moon at the top of a long stair `src: Core features rule 13`
- [ ] `C-CF-34` `ui` The portal fills the frame as a deep red disc of engraved rings; a life-size hand reaches in from the right `src: Core features rule 13`
- [ ] `C-CF-35` `ui` The temple interior shows two rows of red columns, a pair of engraved eyes, an altar carrying three bottles `src: Core features rule 13`
- [ ] `C-CF-36` `ui` The colonnade opens in paper white with the figure walking away in a flavour-coloured robe `src: Core features rule 13`
- [ ] `C-CF-37` `ui` The columns fracture against flat red as the figure lifts off the floor `src: Core features rule 13`
- [ ] `C-CF-38` `literal` `EXPERIENCE` returns the story to the start of `wander` `src: Core features rule 14`
- [ ] `C-CF-39` `literal` `COLLECTION` moves the story to the start of `products` `src: Core features rule 14`
- [ ] `C-CF-40` `literal` The header destinations are `#experience`, `#collection` `src: Core features rule 14`
- [ ] `C-CF-41` `capability` A header move is animated, with the wheel able to interrupt the move `src: Core features rule 14`
- [ ] `C-CF-42` `capability` A header move passing a held gesture marks the gesture satisfied `src: Core features rule 14`
- [ ] `C-CF-43` `capability` Reverse travel to the start restores the header state, the ground colour, the sound mix `src: Core features rule 15`
- [ ] `C-CF-44` `constraint` The age question is not asked again on reverse travel `src: Core features rule 15`
- [ ] `C-CF-45` `constraint` The film offers no replay control `src: Core features rule 15`
- [ ] `C-CF-46` `capability` A browser that cannot draw the film is sent to `/unsupported` `src: Core features rule 16`
- [ ] `C-CF-47` `literal` `/unsupported` says `Your browser is not supported` `src: Core features rule 16`
- [ ] `C-CF-48` `literal` `/?mode=still` renders the still page in place of the film `src: Core features rule 16`
- [ ] `C-CF-49` `literal` The rotate panel reads `Please rotate your device.` `src: Core features rule 17`
- [ ] `C-CF-50` `ui` On an upright handset the rotate panel covers everything, the age panel too `src: Core features rule 17`
- [ ] `C-CF-51` `capability` Each rotate word is a separate element, with the whole line once as hidden text `src: Core features rule 17`
- [ ] `C-CF-52` `capability` The loader shows real progress, never a timed fake `src: Core features rule 18`
- [ ] `C-CF-53` `capability` A failed load falls through to the still page `src: Core features rule 18`
- [ ] `C-CF-54` `literal` The age panel asks `Are you of legal age?` `src: Core features rule 19`
- [ ] `C-CF-55` `ui` The age panel offers two controls, Yes with No `src: Core features rule 19`
- [ ] `C-CF-56` `capability` Nothing behind the age panel moves before Yes is chosen `src: Core features rule 19`
- [ ] `C-CF-57` `constraint` The age answer is never remembered across a full page load `src: Core features rule 19`
- [ ] `C-CF-58` `literal` Full page loads of `/terms`, `/unsupported`, `/alerts/cancel`, plus the sign-in link page, skip the age question `src: Core features rule 19`
- [ ] `C-CF-59` `literal` Choosing No shows `ACCESS DENIED` with `You need to be of legal age to access.` `src: Core features rule 20`
- [ ] `C-CF-60` `literal` The denied state offers `GO BACK`, returning to the question `src: Core features rule 20`
- [ ] `C-CF-61` `capability` After Yes the header bar appears once the loader has finished `src: Core features rule 21`
- [ ] `C-CF-62` `capability` The story waits at each held gate, resisting the wheel before springing back `src: Core features rule 22`
- [ ] `C-CF-63` `constraint` Neither gate completes on the gate's own `src: Core features rule 22`
- [ ] `C-CF-64` `literal` The portal prompt reads `HOLD & MOVE` `src: Core features rule 23`
- [ ] `C-CF-65` `capability` Pressing then moving with the pointer held opens the portal as the rings widen `src: Core features rule 23`
- [ ] `C-CF-66` `capability` Letting go early drains the accumulated movement back to nothing `src: Core features rule 23`
- [ ] `C-CF-67` `capability` The confirm key with arrow keys accumulates portal movement `src: Core features rule 23`
- [ ] `C-CF-68` `literal` The pour prompt reads `HOLD & POUR` `src: Core features rule 24`
- [ ] `C-CF-69` `capability` Holding fills the glass; letting go keeps the glass as full as the glass was `src: Core features rule 24`
- [ ] `C-CF-70` `capability` At the pedestal the visitor picks one flavour, which sets the poured liquid, the robe tint, the carousel starting flavour `src: Core features rule 24`
- [ ] `C-CF-71` `constraint` The glass never overfills `src: Core features rule 24`
- [ ] `C-CF-72` `capability` When the glass is full the pour gate releases the story `src: Core features rule 24`
- [ ] `C-CF-73` `literal` Moving on without choosing a flavour, or arriving by a header move, chooses `MARSHMALLOW COFFEE & CREAM` `src: Core features rule 24`
- [ ] `C-CF-74` `capability` The reaching hand with the tilted bottle signal the gesture with the prompt hidden `src: Core features rule 25`
- [ ] `C-CF-75` `capability` A completed gate is not asked for again after reverse travel `src: Core features rule 26`
- [ ] `C-CF-76` `capability` Each held gate exists in the hidden text as a control named by the gate's prompt `src: Core features rule 27`
- [ ] `C-CF-77` `capability` Under a reduced-motion preference each gate becomes a single press `src: Core features rule 27`
- [ ] `C-CF-78` `constraint` No sound exists before `Toggle audio` is pressed `src: Core features rule 28`
- [ ] `C-CF-79` `capability` The mix follows the story position, so scrubbing backwards scrubs the mix `src: Core features rule 28`
- [ ] `C-CF-80` `capability` Silencing is instant at the master, surviving chapter changes `src: Core features rule 28`
- [ ] `C-CF-81` `capability` The bed is five drones, a jazz thread, wind over the outdoor chapters `src: Core features rule 29`
- [ ] `C-CF-82` `capability` The portal movement sound rises with the accumulated drag `src: Core features rule 30`
- [ ] `C-CF-83` `capability` One-off sounds are never retriggered by small movement around a boundary `src: Core features rule 31`
- [ ] `C-CF-84` `capability` Every sound is synthesised in the browser as the page runs `src: Core features rule 32`
- [ ] `C-CF-85` `capability` Idle input ducks the interaction sounds, bringing the bed forward `src: Core features rule 31`
- [ ] `C-CF-86` `ui` The audio meter dances with sound on, resting as a two-bar glyph with sound off `src: Core features rule 33`
- [ ] `C-CF-87` `capability` The audio control is the first interactive element after the age panel closes `src: Core features rule 33`
- [ ] `C-CF-88` `literal` The promise chapter sets `INDULGE NOW` over `ATONE LATER` `src: Core features rule 34`
- [ ] `C-CF-89` `ui` The poster type reads through the glass, bent by the liquid `src: Core features rule 35`
- [ ] `C-CF-90` `ui` The carousel bottle stays in place, turning, as the flavour names slide `src: Core features rule 36`
- [ ] `C-CF-91` `capability` Next with previous steps one flavour; a side label jumps to the side label's flavour `src: Core features rule 36`
- [ ] `C-CF-92` `capability` Marshmallow tasting notes pair toasted marshmallow, cold brew, vanilla cream, bitter cocoa `src: Core features rule 37`
- [ ] `C-CF-93` `capability` Orange tasting notes pair candied orange peel, milk chocolate, cream, a warm clove finish `src: Core features rule 37`
- [ ] `C-CF-94` `capability` Mint tasting notes pair garden mint, dark chocolate, sweet cream, a cool long finish `src: Core features rule 37`
- [ ] `C-CF-95` `capability` The carousel order is marshmallow, orange, mint `src: Core features rule 37`
- [ ] `C-CF-96` `literal` The tint tokens are `flavour-a` for marshmallow, `flavour-c` for orange, `flavour-b` for mint `src: Core features rule 37`
- [ ] `C-CF-97` `literal` The data strip reads `NOCTURNE N.02`, `13% ABV`, `700 ML` `src: Core features rule 38`
- [ ] `C-CF-98` `capability` The hold control beneath the data strip carries the keep label `src: Core features rule 38`
- [ ] `C-CF-99` `literal` The retail chapter shows `Select Houses Forthcoming` `src: Core features rule 39`
- [ ] `C-CF-100` `capability` The retail chapter lists the nearest venues once a location is known `src: Core features rule 39`
- [ ] `C-CF-101` `literal` `GET /api/v1/content` returns `releases`, `flavours`, `chapters`, `credits`, `legal` `src: Core features rule 40`
- [ ] `C-CF-102` `literal` The flavour ids are `marshmallow-coffee`, `orange-chocolate`, `mint-chocolate` `src: Core features rule 40`
- [ ] `C-CF-103` `constraint` The content document carries no colour value `src: Core features rule 40`
- [ ] `C-CF-104` `capability` The story renders from the content document already held when the network fails `src: Core features rule 41`
- [ ] `C-CF-105` `ui` The shelf renders bottles standing on an engraved stone ledge, each turning slowly `src: Core features rule 42`
- [ ] `C-CF-106` `literal` An empty shelf reads `AN EMPTY SHELF IS A KIND OF PATIENCE` `src: Core features rule 42`
- [ ] `C-CF-107` `capability` The header pill shows how many bottles are on the shelf `src: Core features rule 42`
- [ ] `C-CF-108` `capability` The shelf lists every release with the release's remaining count beside a hold control `src: Core features rule 42`
- [ ] `C-CF-109` `literal` `GET /api/v1/releases/{releaseId}` returns `total`, `claimed`, `remaining` `src: Core features rule 43`
- [ ] `C-CF-110` `literal` `GET /api/v1/releases` lists the releases with `claimed` with `remaining` `src: Deployment contract`
- [ ] `C-CF-111` `literal` The home page HTML carries the corner words `VESPERI`, `SPIRITS`, `NOCTURNE`, `COLLECTION` with the subtitle `AN ODE TO THE NIGHT, YOUR NIGHT` `src: Front-end specification, copy`
- [ ] `C-CF-112` `capability` Claimed counts the allocations held, offered or confirmed `src: Core features rule 43`
- [ ] `C-CF-113` `literal` `POST /api/v1/cellar/holds` answers `201` with a `held` item `src: Core features rule 44`
- [ ] `C-CF-114` `capability` A hold expires seventy-two hours after the claim, at an absolute server-issued instant `src: Core features rule 44`
- [ ] `C-CF-115` `literal` A held bottle's control reads `YOURS FOR 72 HOURS` `src: Core features rule 44`
- [ ] `C-CF-116` `literal` An unknown flavour is refused with `invalid_flavour` `src: Core features rule 45`
- [ ] `C-CF-117` `literal` A claim outside the release window is refused with `closed` `src: Core features rule 45`
- [ ] `C-CF-118` `literal` A second live claim on one release is refused with `already_held` `src: Core features rule 46`
- [ ] `C-CF-119` `literal` A claim on an exhausted release answers `exhausted` with a `position` `src: Core features rule 47`
- [ ] `C-CF-120` `literal` A waitlisted visitor reads `YOU ARE NUMBER {n} IN LINE` `src: Core features rule 47`
- [ ] `C-CF-121` `capability` Two simultaneous claims on the last allocation leave one hold plus one waitlist entry `src: Core features rule 48`
- [ ] `C-CF-122` `capability` Held, offered, confirmed allocations of a release never exceed the release total `src: Core features rule 48`
- [ ] `C-CF-123` `capability` A repeated claim with one `Idempotency-Key` returns the earlier item `src: Core features rule 49`
- [ ] `C-CF-124` `capability` A claim waiting on the server never shows the bottle as held `src: Core features rule 49`
- [ ] `C-CF-125` `literal` `GET /api/v1/cellar` returns `items` carrying `allocationId`, `releaseId`, `flavour`, `state`, `expiresAt` `src: Core features rule 50`
- [ ] `C-CF-126` `capability` A hold with under six hours left reads expiring, showing a countdown `src: Core features rule 50`
- [ ] `C-CF-127` `capability` An expired hold shows the went-back line `src: Core features rule 51`
- [ ] `C-CF-128` `literal` A freed allocation moves the first visitor in line from `waitlisted` to `offered` `src: Core features rule 51`
- [ ] `C-CF-129` `capability` A waitlist position closes up when a visitor ahead leaves the line `src: Core features rule 51`
- [ ] `C-CF-130` `literal` `DELETE /api/v1/cellar/holds/{allocationId}` answers `204` `src: Core features rule 52`
- [ ] `C-CF-131` `capability` A released allocation is offered to the head of the waitlist for twelve hours `src: Core features rule 52`
- [ ] `C-CF-132` `literal` The offer message subject begins `A bottle came back for you:` `src: Core features rule 52`
- [ ] `C-CF-133` `literal` `POST /api/v1/cellar/holds/{allocationId}/accept` turns an offer into a hold `src: Core features rule 53`
- [ ] `C-CF-134` `literal` `POST /api/v1/cellar/holds/{allocationId}/decline` gives the offer up to the next visitor in line `src: Core features rule 53`
- [ ] `C-CF-135` `literal` An offer left unaccepted for twelve hours reads `lapsed`, its bottle passing on or back to `remaining` `src: Core features rule 53`
- [ ] `C-CF-136` `literal` Accepting an item that is not offered is refused with `not_offered` `src: Core features rule 53`
- [ ] `C-CF-137` `capability` An offer shows both accept with decline, where decline passes the offer on `src: Core features rule 53`
- [ ] `C-CF-138` `literal` `POST /api/v1/cellar/holds/{allocationId}/confirm` twice returns the same confirmed item `src: Core features rule 54`
- [ ] `C-CF-139` `capability` A shelf holding no bottles returns an empty item list `src: Core features rule 42`
- [ ] `C-CF-140` `capability` After a reload or on another browser, the same bottles appear in the same states `src: Core features rule 50`
- [ ] `C-CF-141` `constraint` Granting a hold sends no message `src: Core features rule 55`
- [ ] `C-CF-142` `constraint` Joining a waitlist sends no message `src: Core features rule 55`
- [ ] `C-CF-143` `constraint` Confirming a hold sends no message `src: Core features rule 55`
- [ ] `C-CF-144` `constraint` Releasing a hold sends the owner no message `src: Core features rule 55`
- [ ] `C-CF-145` `constraint` Declining an offer sends no further message `src: Core features rule 55`
- [ ] `C-CF-146` `capability` Releasing a waitlisted item leaves the queue, moving everyone behind up one `src: Core features rule 52`
- [ ] `C-CF-147` `capability` With the connection cut, the shelf renders the last copy marked as possibly out of date `src: Core features rule 56`
- [ ] `C-CF-148` `capability` With the connection cut, the hold control is unavailable with the reason in words `src: Core features rule 56`
- [ ] `C-CF-149` `capability` The shelf renders zero, one or three bottles, with held, expiring, confirmed side by side `src: Core features rule 57`
- [ ] `C-CF-150` `literal` Release `N02` has a total of `240` `src: Core features rule 58`
- [ ] `C-CF-151` `literal` Release `N02-CASK` has a total of `1` `src: Core features rule 58`
- [ ] `C-CF-152` `literal` Releases `N02-SALON`, `N02-VESTRY` each hold one bottle `src: Core features rule 58`
- [ ] `C-CF-153` `literal` Release `N01` is closed; release `N04` opens later `src: Core features rule 58`
- [ ] `C-CF-154` `literal` Every venue lists hours of `17:00 to 01:00` in the venue zone `src: Core features rule 74`
- [ ] `C-CF-155` `literal` `GET /api/v1/venues/{id}` returns the venue with `address`, `hours`, `timezone` `src: Core features rule 64`
- [ ] `C-CF-156` `literal` `visitor2@example.com` holds one confirmed allocation of `N02` `src: Core features rule 58`
- [ ] `C-CF-157` `literal` `visitor2@example.com` also holds one expired allocation of `N01` `src: Core features rule 58`
- [ ] `C-CF-158` `literal` Release `N02-EMBER` holds one bottle, with a seeded `offered` allocation for `visitor2@example.com` from thirteen hours back `src: Core features rule 58`
- [ ] `C-CF-159` `literal` The seeded session `Early Pour at Salt & Vesper` started one hour before first start `src: Core features rule 89`
- [ ] `C-CF-160` `literal` `N02` starts with `239` remaining `src: Core features rule 58`
- [ ] `C-CF-161` `ui` Venues list beside a drawn plan on `/where` `src: Core features rule 59`
- [ ] `C-CF-162` `constraint` The venue plan is never drawn by a mapping service `src: Core features rule 59`
- [ ] `C-CF-163` `capability` Refused location offers a place field, never a default city `src: Core features rule 60`
- [ ] `C-CF-164` `literal` `GET /api/v1/places?q=` lists every place whose name starts with the typed text `src: Core features rule 60`
- [ ] `C-CF-165` `literal` A search for `Newport` lists `Newport, Wales` beside `Newport, Isle of Wight` `src: Core features rule 60`
- [ ] `C-CF-166` `literal` `GET /api/v1/venues` answers a `region` with `venues` `src: Core features rule 61`
- [ ] `C-CF-167` `literal` `radius` runs from `1` to `50`, otherwise the reason is `invalid_radius` `src: Core features rule 61`
- [ ] `C-CF-168` `capability` Venues are sorted nearest first `src: Core features rule 61`
- [ ] `C-CF-169` `capability` Distance is great-circle kilometres on a sphere of radius 6371 km, rounded to one decimal `src: Core features rule 62`
- [ ] `C-CF-170` `literal` Within `5` of Soho the list is `The Gilded Nave` at `0.2`, then `Salt & Vesper` at `4.1` `src: Core features rule 62`
- [ ] `C-CF-171` `literal` Within `3` of Soho only `The Gilded Nave` lists `src: Core features rule 62`
- [ ] `C-CF-172` `literal` Stock is one of `in`, `low`, `out`, `unknown` `src: Core features rule 63`
- [ ] `C-CF-173` `capability` A reading more than seventy-two hours old reads unknown `src: Core features rule 63`
- [ ] `C-CF-174` `capability` A venue with no reading for a flavour reads unknown for the flavour `src: Core features rule 63`
- [ ] `C-CF-175` `capability` Without a flavour, stock combines the readings, best first `src: Core features rule 63`
- [ ] `C-CF-176` `literal` A stale reading shows `LAST SEEN {n} DAYS AGO` `src: Core features rule 63`
- [ ] `C-CF-177` `capability` The venue detail returns per-flavour stock under the same seventy-two-hour rule `src: Core features rule 64`
- [ ] `C-CF-178` `capability` A coordinate's region is the region of the nearest seeded place `src: Core features rule 65`
- [ ] `C-CF-179` `literal` `GET /api/v1/regions/{code}` returns `listingAllowed` with `notice` `src: Core features rule 65`
- [ ] `C-CF-180` `capability` A region with listing refused answers an empty venue list `src: Core features rule 65`
- [ ] `C-CF-181` `literal` A region with listing refused shows `WE CANNOT LIST HOUSES WHERE YOU ARE` `src: Core features rule 65`
- [ ] `C-CF-182` `constraint` A page in a region with listing refused asks for no venues `src: Core features rule 65`
- [ ] `C-CF-183` `literal` An empty radius shows `NOTHING NEAR YOU YET` with a widen action beside the alert action `src: Core features rule 66`
- [ ] `C-CF-184` `capability` A radius holding no venue returns an empty list `src: Core features rule 66`
- [ ] `C-CF-185` `ui` Venue marks arrive nearest first; opening a venue moves the plan in without changing page `src: Core features rule 67`
- [ ] `C-CF-186` `literal` `POST /api/v1/alerts` answers `201` in state `active` `src: Core features rule 68`
- [ ] `C-CF-187` `capability` Setting the same alert again returns the existing alert `src: Core features rule 68`
- [ ] `C-CF-188` `literal` An alert in a region with listing refused is refused with `restricted` `src: Core features rule 68`
- [ ] `C-CF-189` `literal` An alert on an unknown place id is refused with `invalid_place` `src: Deployment contract`
- [ ] `C-CF-190` `literal` Setting an alert sends a message whose subject begins `Alert set:` `src: Core features rule 69`
- [ ] `C-CF-191` `capability` Every alert message opens with the cancel line carrying the `/alerts/cancel?token=` link `src: Core features rule 69`
- [ ] `C-CF-192` `literal` Opening the cancellation link, signed in or not, shows `THAT ALERT IS OFF` `src: Core features rule 69`
- [ ] `C-CF-193` `capability` Reopening the cancellation link shows the same line again `src: Core features rule 69`
- [ ] `C-CF-194` `capability` A host setting a reading of in or low inside the radius fires the alert `src: Core features rule 70`
- [ ] `C-CF-195` `literal` A firing alert becomes `fired`, its message subject beginning with the landed prefix `src: Core features rule 70`
- [ ] `C-CF-196` `constraint` A fired or cancelled alert never sends again `src: Core features rule 70`
- [ ] `C-CF-197` `capability` An alert without a flavour fires for a reading of any flavour `src: Core features rule 70`
- [ ] `C-CF-198` `capability` A reading of in fires matching active alerts even when the reading has not changed `src: Core features rule 70`
- [ ] `C-CF-199` `constraint` A venue outside the alert's radius of the alert's place fires nothing `src: Core features rule 70`
- [ ] `C-CF-200` `literal` `GET /api/v1/alerts` lists the visitor's own alerts `src: Core features rule 71`
- [ ] `C-CF-201` `literal` `DELETE /api/v1/alerts/{id}` cancels an alert, answering `204` `src: Core features rule 71`
- [ ] `C-CF-202` `capability` With the connection cut, the last venue list renders stamped with the list's age, refusing new alerts `src: Core features rule 72`
- [ ] `C-CF-203` `literal` Seeded places include `Soho`, `Shoreditch`, `Leith`, `Bergen` `src: Core features rule 73`
- [ ] `C-CF-204` `literal` The `NO` region carries the pinned notice refusing listings `src: Core features rule 73`
- [ ] `C-CF-205` `literal` Seeded venues include `The Gilded Nave`, `Salt & Vesper`, `The Chapel Cellar`, `Le Confessionnal`, `Nordlys Bar` `src: Core features rule 74`
- [ ] `C-CF-206` `capability` The mint reading at The Gilded Nave dates from five days before first start `src: Core features rule 74`
- [ ] `C-CF-207` `ui` The tastings page lists sessions beside the chosen session's detail, behaving like a form `src: Core features rule 75`
- [ ] `C-CF-208` `literal` `GET /api/v1/tastings` lists `startsAt`, `timezone`, `capacity`, `remaining`, `price` `src: Core features rule 76`
- [ ] `C-CF-209` `literal` `3500` is `$35.00` in integer minor units of `usd` `src: Core features rule 76`
- [ ] `C-CF-210` `literal` With no query, the tastings list carries every `scheduled` session, one that has already started included `src: Core features rule 76`
- [ ] `C-CF-211` `contract` Every instant in a request or response is an ISO 8601 string in UTC ending in `Z` `src: Deployment contract`
- [ ] `C-CF-212` `capability` Times show in the venue's zone, with the visitor's own time beside when different `src: Core features rule 77`
- [ ] `C-CF-213` `literal` `POST /api/v1/tastings/{id}/holds` answers `holdId` with `expiresAt` fifteen minutes ahead `src: Core features rule 78`
- [ ] `C-CF-214` `literal` Party size runs `1` to `8`, otherwise the reason is `invalid_party_size` `src: Core features rule 78`
- [ ] `C-CF-215` `literal` A party above the seats remaining is refused with `insufficient` `src: Core features rule 78`
- [ ] `C-CF-216` `literal` A hold at a second session is refused with `hold_elsewhere` `src: Core features rule 78`
- [ ] `C-CF-217` `literal` `DELETE /api/v1/tastings/holds/{holdId}` gives held seats back `src: Core features rule 78`
- [ ] `C-CF-218` `capability` Held plus booked seats never exceed capacity under simultaneous holds `src: Core features rule 79`
- [ ] `C-CF-219` `literal` Held seats show `SEATS HELD FOR {n}` counting down `src: Core features rule 80`
- [ ] `C-CF-220` `capability` An expired seat hold returns the visitor to the party size step with the choices kept `src: Core features rule 80`
- [ ] `C-CF-221` `literal` `POST /api/v1/bookings` answers `201` in state `booked` `src: Core features rule 81`
- [ ] `C-CF-222` `literal` `GET /api/v1/bookings` lists the visitor's own bookings `src: Core features rule 83`
- [ ] `C-CF-223` `capability` A repeated booking with one `Idempotency-Key` returns the same booking `src: Core features rule 81`
- [ ] `C-CF-224` `literal` The booking message subject begins `Tasting booked:` `src: Core features rule 82`
- [ ] `C-CF-225` `capability` The booking message body names the venue with the time in the venue zone `src: Core features rule 82`
- [ ] `C-CF-226` `capability` The confirmation returns the visitor to the poster composition carrying the session `src: Core features rule 82`
- [ ] `C-CF-227` `literal` `DELETE /api/v1/bookings/{id}` answers `204` more than forty-eight hours ahead `src: Core features rule 83`
- [ ] `C-CF-228` `literal` Cancelling inside forty-eight hours is refused with `late` `src: Core features rule 83`
- [ ] `C-CF-229` `capability` A late cancel shows the too-late line offering a move `src: Core features rule 83`
- [ ] `C-CF-230` `literal` `POST /api/v1/bookings/{id}/reschedule` takes `sessionId`, moving the booking once to a session with room `src: Core features rule 84`
- [ ] `C-CF-231` `literal` A second move is refused with `already_rescheduled` `src: Core features rule 84`
- [ ] `C-CF-232` `capability` A move to a session without room is refused as insufficient `src: Core features rule 84`
- [ ] `C-CF-233` `literal` A full session shows `FULL. JOIN THE LINE` `src: Core features rule 85`
- [ ] `C-CF-234` `literal` `POST /api/v1/tastings/{id}/waitlist` answers `201` with a `position` `src: Core features rule 85`
- [ ] `C-CF-235` `literal` Joining the list of a session with room is refused with `409`, reason `not_full` `src: Core features rule 85`
- [ ] `C-CF-236` `capability` Joining the same list twice answers with the existing position `src: Core features rule 85`
- [ ] `C-CF-237` `capability` A host cancelling a session moves every booking on the session to session_cancelled `src: Core features rule 86`
- [ ] `C-CF-238` `literal` A cancelled session message subject begins `Tasting cancelled:` `src: Core features rule 86`
- [ ] `C-CF-239` `literal` A hold on a cancelled session is refused with `409`, reason `closed` `src: Core features rule 105`
- [ ] `C-CF-240` `literal` A move to a cancelled session is refused with `closed` `src: Core features rule 84`
- [ ] `C-CF-241` `literal` An owner edit more than twenty-four hours after saving is refused with `edit_window_closed` `src: Core features rule 98`
- [ ] `C-CF-242` `literal` A move to a session that has already started is refused with `session_started` `src: Core features rule 84`
- [ ] `C-CF-243` `literal` A session that has already started takes no new holds, giving `session_started` `src: Core features rule 78`
- [ ] `C-CF-244` `constraint` Holding seats sends no message `src: Core features rule 87`
- [ ] `C-CF-245` `constraint` A visitor cancelling a booking is sent no message `src: Core features rule 87`
- [ ] `C-CF-246` `constraint` Rescheduling a booking sends no message `src: Core features rule 87`
- [ ] `C-CF-247` `constraint` Joining a tasting waitlist sends no message `src: Core features rule 87`
- [ ] `C-CF-248` `capability` With the connection cut, existing bookings render, with new holds refused `src: Core features rule 88`
- [ ] `C-CF-249` `literal` `Late Pour at Salt & Vesper` starts thirty hours after first start `src: Core features rule 89`
- [ ] `C-CF-250` `literal` `Cellar Tasting at The Chapel Cellar` has capacity `2` `src: Core features rule 89`
- [ ] `C-CF-251` `literal` `Sold Out Supper at The Gilded Nave` is fully booked by `visitor2@example.com` `src: Core features rule 89`
- [ ] `C-CF-252` `literal` `Nocturne Night at The Gilded Nave` costs `3500`, in `Europe/London` `src: Core features rule 89`
- [ ] `C-CF-253` `literal` `Soiree Nocturne at Le Confessionnal` runs in `Europe/Paris` `src: Core features rule 89`
- [ ] `C-CF-254` `literal` `Last Call at Salt & Vesper` is a seeded session `src: Core features rule 89`
- [ ] `C-CF-255` `ui` The ritual builder uses a red ground with paper type `src: Core features rule 90`
- [ ] `C-CF-256` `capability` Each added ingredient tints the liquid in the glass at once `src: Core features rule 90`
- [ ] `C-CF-257` `capability` A visitor who leaves mid-build finds the draft kept on the same device `src: Core features rule 90`
- [ ] `C-CF-258` `literal` `GET /api/v1/ingredients` returns `mixers`, `ices`, `garnishes` `src: Core features rule 91`
- [ ] `C-CF-259` `literal` The mixers are `cold-brew`, `tonic`, `oat-milk`, `soda`, `espresso`, `ginger-ale` `src: Core features rule 91`
- [ ] `C-CF-260` `literal` The ices are `no-ice`, `cubed`, `crushed`, `single-block` `src: Core features rule 91`
- [ ] `C-CF-261` `literal` The garnishes are `no-garnish`, `orange-twist`, `mint-sprig`, `grated-nutmeg`, `cocoa-dust` `src: Core features rule 91`
- [ ] `C-CF-262` `literal` The withdrawn garnish `gold-leaf` is refused with `invalid_ingredient` `src: Core features rule 92`
- [ ] `C-CF-263` `literal` More than four mixers is refused with `too_many_mixers` `src: Core features rule 92`
- [ ] `C-CF-264` `literal` A name outside `3` to `40` characters is refused with `invalid_name` `src: Core features rule 92`
- [ ] `C-CF-265` `literal` `POST /api/v1/rituals` answers `201` with the `slug` `src: Core features rule 92`
- [ ] `C-CF-266` `literal` A name carrying `casino`, `crypto`, `loan`, `viagra` or a web address is refused with `name_refused` `src: Core features rule 93`
- [ ] `C-CF-267` `capability` A refused name returns to naming with the reason shown, the build intact `src: Core features rule 93`
- [ ] `C-CF-268` `capability` The same ritual saved twice returns the existing slug `src: Core features rule 94`
- [ ] `C-CF-269` `literal` A sixth new save within an hour answers `429` with `rate_limited` `src: Core features rule 95`
- [ ] `C-CF-270` `literal` The cooling-down state reads `ENOUGH FOR NOW. TRY AGAIN IN {n}` `src: Core features rule 95`
- [ ] `C-CF-271` `capability` A save answering with an existing slug does not count toward the hourly limit `src: Core features rule 95`
- [ ] `C-CF-272` `literal` A slug reads like `velvet-hour-7k2q` `src: Core features rule 96`
- [ ] `C-CF-273` `literal` `GET /api/v1/rituals/{slug}` returns `name`, `flavour`, `mixers`, `ice`, `garnish` `src: Core features rule 97`
- [ ] `C-CF-274` `constraint` A public ritual read carries no account id, no email, no display name `src: Core features rule 97`
- [ ] `C-CF-275` `capability` Only the owner edits a ritual, within twenty-four hours of saving `src: Core features rule 98`
- [ ] `C-CF-276` `literal` `PATCH /api/v1/rituals/{slug}` by anyone but the owner is denied with `forbidden` `src: Core features rule 98`
- [ ] `C-CF-277` `literal` `DELETE /api/v1/rituals/{slug}` answers `204` for the owner `src: Core features rule 98`
- [ ] `C-CF-278` `capability` A shared link opens under the poured-for-you line `src: Core features rule 99`
- [ ] `C-CF-279` `capability` A shared link shows the age question first, then the pour, then the story `src: Core features rule 99`
- [ ] `C-CF-280` `literal` A shared page's HTML names ingredients by display name, for example `Gold leaf`, `Espresso`, `Oat milk` `src: Core features rule 99`
- [ ] `C-CF-281` `literal` A deleted or unknown slug shows `THAT ONE IS GONE. POUR YOUR OWN` `src: Core features rule 99`
- [ ] `C-CF-282` `capability` With the connection cut, saving a ritual is refused with the reason in words `src: Core features rule 100`
- [ ] `C-CF-283` `ui` The finished ritual card arrives with the product's only overshoot `src: Core features rule 101`
- [ ] `C-CF-284` `literal` The seeded ritual `midnight-confession-a1b2` is `Midnight Confession` with `gold-leaf` `src: Core features rule 102`
- [ ] `C-CF-285` `ui` The host page is a plain document on paper, unreachable from the film `src: Core features rule 103`
- [ ] `C-CF-286` `capability` The host page shows each reading with the reading's age, next to upcoming sessions `src: Core features rule 103`
- [ ] `C-CF-287` `literal` `GET /api/v1/host/venue` returns the host venue's `name`, `stock`, `sessions` `src: Core features rule 104`
- [ ] `C-CF-288` `literal` `PUT /api/v1/venues/{id}/stock` takes `flavour` with `reading` `src: Core features rule 104`
- [ ] `C-CF-289` `literal` An unknown stock reading is refused with `invalid_reading` `src: Core features rule 104`
- [ ] `C-CF-290` `literal` `POST /api/v1/tastings/{id}/cancel` answers the session in state `cancelled` `src: Core features rule 105`
- [ ] `C-CF-291` `capability` A cancelled session takes no new holds `src: Core features rule 105`
- [ ] `C-CF-292` `capability` A visitor calling a host endpoint is denied, the row unchanged `src: Core features rule 106`
- [ ] `C-CF-293` `literal` A wrong password answers the reason `invalid_credentials` `src: Core features rule 1`
- [ ] `C-CF-294` `capability` A host calling for another venue is denied, the row unchanged `src: Core features rule 106`
- [ ] `C-CF-295` `literal` A host calling a visitor-only endpoint is denied with `forbidden` `src: Core features rule 106`
- [ ] `C-CF-296` `literal` A visitor calling a host endpoint gets the reason `forbidden` `src: Core features rule 106`
- [ ] `C-CF-297` `literal` A terms page lives at `/terms` `src: Core features rule 107`
- [ ] `C-CF-298` `capability` The footer Legal link on every page leads to the terms page `src: Core features rule 107`
- [ ] `C-CF-299` `capability` The sign-in form links to the terms page `src: Core features rule 107`
- [ ] `C-CF-300` `capability` The terms page states the conditions of use, the legal drinking age requirement, what the product keeps about a visitor `src: Core features rule 107`
- [ ] `C-CF-301` `capability` A first-time visitor is asked once about non-essential cookies after the age panel `src: Core features rule 108`
- [ ] `C-CF-302` `literal` `POST /api/v1/cookie-choice` records `nonEssentialAccepted` `src: Core features rule 108`
- [ ] `C-CF-303` `literal` `GET /api/v1/cookie-choice` returns the recorded choice after a reload `src: Core features rule 108`
- [ ] `C-CF-304` `literal` A malformed body is refused with `invalid_request` `src: Deployment contract`
- [ ] `C-CF-305` `ui` The ritual builder carries a save control `src: Core features rule 90`
- [ ] `C-CF-306` `literal` A favicon is served at `/favicon.ico`, declared in every page head `src: Core features rule 109`
- [ ] `C-CF-307` `literal` `/sitemap.xml` lists `/`, `/where`, `/tastings`, `/ritual`, `/terms` `src: Core features rule 110`
- [ ] `C-CF-308` `capability` Every public page carries a title with a description of the page's own `src: Technical requirements, launch files`
- [ ] `C-CF-309` `literal` `/robots.txt` carries a `Sitemap:` line `src: Core features rule 110`
- [ ] `C-CF-310` `literal` `/og/default.png` is a PNG generated at request time `src: Core features rule 111`
- [ ] `C-CF-311` `literal` A ritual page names `/og/ritual/{slug}.png` for sharing, generated the same way `src: Core features rule 111`
- [ ] `C-CF-312` `capability` Every page declares a social preview title with an image `src: Core features rule 111`
- [ ] `C-CF-313` `capability` The still page carries the product data as a description list `src: Core features rule 112`
- [ ] `C-CF-314` `capability` The still page shows a still picture of each chapter's composition `src: Core features rule 112`
- [ ] `C-CF-315` `capability` The HTML of the home page carries the narration, the collection copy, the flavour names with tasting notes `src: Core features rule 113`
- [ ] `C-CF-316` `capability` The collection chapters with the footer link to the four additions `src: Core features rule 39`
- [ ] `C-CF-317` `literal` The hidden control names include `Toggle audio`, `previous slide`, `next slide`, `left text`, `right text` `src: Core features rule 113`

## C-UF User flow

- [ ] `C-UF-01` `constraint` Moving between routes inside the app after answering does not ask the age question again `src: Core features rule 19`
- [ ] `C-UF-02` `literal` The footer offers `INSTAGRAM`, `hello@example.com`, `Legal`, `Tastings`, with `Legal` opening `/terms` `src: User flow, footer`
- [ ] `C-UF-03` `literal` A signed-out request for `/host` goes to `/sign-in` `src: User flow, entry and redirects`
- [ ] `C-UF-04` `literal` The addition routes are `/cellar`, `/where`, `/tastings`, `/ritual` `src: User flow route table`
- [ ] `C-UF-05` `literal` `/ritual/{slug}` is a shared ritual page `src: User flow route table`
- [ ] `C-UF-06` `literal` `/alerts/cancel` cancels an alert from a message `src: User flow route table`
- [ ] `C-UF-07` `literal` `/sign-in` asks for a sign-in link `src: User flow route table`
- [ ] `C-UF-08` `capability` The sign-in landing route exchanges the token for a session `src: User flow route table`
- [ ] `C-UF-09` `literal` `/host` is the host's own venue page `src: User flow route table`
- [ ] `C-UF-10` `capability` A signed-out request for the shelf goes to sign-in, then back `src: User flow, entry and redirects`
- [ ] `C-UF-11` `capability` A host password sign-in lands on the host page `src: User flow, entry and redirects`
- [ ] `C-UF-12` `capability` A visitor requesting the host page gets the product's own permission surface `src: User flow, entry and redirects`
- [ ] `C-UF-13` `capability` A session expiring mid-action leaves the action unapplied, restoring the page after sign-in `src: User flow, entry and redirects`
- [ ] `C-UF-14` `ui` An upright handset on an addition route gets the page laid out for the upright handset `src: User flow, entry and redirects`
- [ ] `C-UF-15` `capability` The keep journey lands back on the mint bottle with the hold placed `src: User flow journey 2`
- [ ] `C-UF-16` `capability` The queue journey ends with the offer on `Nocturne N.02 Vestry Pour` accepted `src: User flow journey 4`
- [ ] `C-UF-17` `capability` The Leith journey ends with an alert cancelled from the message link `src: User flow journey 5`
- [ ] `C-UF-18` `capability` The booking journey moves `Late Pour at Salt & Vesper` to `Soiree Nocturne at Le Confessionnal` `src: User flow journey 7`
- [ ] `C-UF-19` `capability` The ritual journey opens `/ritual/midnight-confession-a1b2` showing the gold leaf garnish `src: User flow journey 9`
- [ ] `C-UF-20` `ui` Every list has an empty state distinct from the list's loading state `src: User flow, states`
- [ ] `C-UF-21` `ui` Every failure names what failed, why, the one next action `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The subject, first the story then the bottle, is always the first thing seen `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The four additions read as plain documents wearing the same ink, paper, red, type `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Almost nothing moves on the page by itself; the story moves as far as the visitor's wheel `src: UI/UX notes, stances`
- [ ] `C-UX-04` `ui` Tone is made of engraved lines rather than smooth shading `src: UI/UX notes, stances`
- [ ] `C-UX-05` `ui` From the promise chapter onward every word the visitor needs is readable, still `src: UI/UX notes, stances`
- [ ] `C-UX-06` `ui` Ink is a near-black neutral used for the dark ground with every engraved line `src: UI/UX notes, colour`
- [ ] `C-UX-07` `ui` Paper is a near-white warm neutral plate `src: UI/UX notes, colour`
- [ ] `C-UX-08` `ui` Blood is a mid, vivid red reserved for the temple, emphasis words, the header ornament, the hold control `src: UI/UX notes, colour`
- [ ] `C-UX-09` `ui` The robe is a light, muted orange in three close steps `src: UI/UX notes, colour`
- [ ] `C-UX-10` `ui` Marshmallow Coffee is a light, vivid cyan tint `src: UI/UX notes, colour`
- [ ] `C-UX-11` `ui` Mint Chocolate is a light, soft green tint `src: UI/UX notes, colour`
- [ ] `C-UX-12` `ui` Orange Chocolate is a light, soft amber tint `src: UI/UX notes, colour`
- [ ] `C-UX-13` `ui` The ground changes with the chapter between ink, paper, blood, with the house mark inverting `src: UI/UX notes, colour`
- [ ] `C-UX-14` `ui` The display face is tall, very high-contrast, in capitals `src: UI/UX notes, type`
- [ ] `C-UX-15` `ui` The interface face is a heavy, rounded geometric sans in letterspaced capitals `src: UI/UX notes, type`
- [ ] `C-UX-16` `ui` The largest chapter title is the largest thing in the product `src: UI/UX notes, type`
- [ ] `C-UX-17` `ui` Corners are square throughout the film `src: UI/UX notes, space`
- [ ] `C-UX-18` `ui` Comic panel edges are four separate wobbly strokes with constant ink `src: UI/UX notes, space`
- [ ] `C-UX-19` `ui` The motion character is eased, confined to the furniture `src: UI/UX notes, motion`
- [ ] `C-UX-20` `ui` The only overshoot in the product is the finished ritual card `src: UI/UX notes, motion`
- [ ] `C-UX-21` `ui` Reduced motion turns the film into still compositions stepped by scroll `src: UI/UX notes, motion`
- [ ] `C-UX-22` `ui` Moving between ink, blood, paper at full frame never flashes `src: UI/UX notes, motion`
- [ ] `C-UX-23` `ui` Text meets WCAG 2.2 AA contrast on every ground the chapter passes through `src: UI/UX notes, accessibility`
- [ ] `C-UX-24` `ui` Keyboard navigation reaches every control with a visible focus ring `src: UI/UX notes, accessibility`
- [ ] `C-UX-25` `ui` The age panel keeps focus inside the panel for as long as the panel is open `src: UI/UX notes, accessibility`
- [ ] `C-UX-26` `ui` Every content image carries alternative text `src: UI/UX notes, accessibility`
- [ ] `C-UX-27` `ui` The film camera reframes, preserving the vertical extent of every shot `src: UI/UX notes, responsive`
- [ ] `C-UX-28` `ui` At a narrow viewport the additions show no sideways overflow `src: UI/UX notes, responsive`
- [ ] `C-UX-29` `ui` On `/where` the list with the plan stack at a narrow viewport `src: UI/UX notes, responsive`
- [ ] `C-UX-30` `ui` Each surface leads with one primary action carrying the strongest contrast `src: UI/UX notes, primary action`
- [ ] `C-UX-31` `ui` Every gap in the additions is a multiple of one base unit `src: UI/UX notes, space`
- [ ] `C-UX-32` `ui` The product keeps the product's own grounds, offering no separate light or dark mode `src: UI/UX notes, colour`
- [ ] `C-UX-33` `ui` Figures in the additions line up in columns `src: UI/UX notes, type`
- [ ] `C-UX-34` `ui` The promise paragraph is set in a light long-form face `src: UI/UX notes, type`
- [ ] `C-UX-35` `ui` No text a visitor must read is smaller than the base text `src: UI/UX notes, type`
- [ ] `C-UX-36` `capability` The age panel hands focus back to the page when the panel closes `src: UI/UX notes, accessibility`
- [ ] `C-UX-37` `capability` The drawing surface is hidden from assistive technology, never taking focus `src: UI/UX notes, accessibility`
- [ ] `C-UX-38` `ui` Interactive targets meet the WCAG 2.2 AA target size, with meaning never carried by colour alone `src: UI/UX notes, accessibility`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The frontend is SolidStart built as a production server-rendered bundle `src: Technical requirements`
- [ ] `C-TR-02` `contract` The backend is Fastify on Node 20 in the same process `src: Technical requirements`
- [ ] `C-TR-03` `contract` PostgreSQL at `DATABASE_URL` holds every record `src: Technical requirements`
- [ ] `C-TR-04` `contract` Mailpit over SMTP at `SMTP_HOST` carries every message `src: Technical requirements`
- [ ] `C-TR-05` `capability` The first response for every route is complete HTML `src: Technical requirements`
- [ ] `C-TR-06` `constraint` The only backing services are PostgreSQL with Mailpit `src: Technical requirements`
- [ ] `C-TR-07` `capability` The film rebuilds at the current story position after the drawing context is lost `src: Technical requirements, film machinery`
- [ ] `C-TR-08` `capability` Removing the four additions leaves the film working `src: Technical requirements, module architecture`
- [ ] `C-TR-09` `constraint` The product carries no font editor, statistics panel, surface editor or save control `src: Technical requirements, module architecture`
- [ ] `C-TR-10` `contract` The app uses only the libraries named, plus browser film libraries installed from the npm registry `src: Technical requirements, stack`
- [ ] `C-TR-11` `contract` Logs are one structured JSON object per line carrying no email, code, token, password `src: Technical requirements, logging`
- [ ] `C-TR-12` `capability` A refused or failed request leaves no partial state `src: Technical requirements, concurrency`
- [ ] `C-TR-13` `capability` Generated assets stay under four megabytes in total `src: Technical requirements, zero shipped assets`
- [ ] `C-TR-14` `capability` The film simplifies itself from measured frame time before falling to the still page `src: Technical requirements, performance budgets`
- [ ] `C-TR-15` `literal` `GET /api/health` returns `200` once PostgreSQL with the SMTP host answer `src: Technical requirements, health`
- [ ] `C-TR-16` `constraint` No log line carries an email address, a sign-in code, a session token, a password `src: Technical requirements, logging`
- [ ] `C-TR-17` `capability` Repeated claims, bookings, ritual saves carrying one key create nothing new `src: Technical requirements, concurrency`
- [ ] `C-TR-18` `constraint` No credential appears in anything the browser downloads `src: Technical requirements, security`
- [ ] `C-TR-19` `capability` Every response carries a nosniff content-type policy among the standard security headers `src: Technical requirements, security`
- [ ] `C-TR-20` `literal` Every page head carries a viewport declaration of `width=device-width` `src: Technical requirements, launch files`

## C-DM Data model

- [ ] `C-DM-01` `data` The data model holds twenty-two tables with UTC timestamps `src: Data model`
- [ ] `C-DM-02` `data` Every id an endpoint returns is the id of the row named `src: Data model`
- [ ] `C-DM-03` `data` `app_user.email` is unique, stored lower case `src: Data model, app_user`
- [ ] `C-DM-04` `data` `app_user.password_hash` never holds a readable password `src: Data model, app_user`
- [ ] `C-DM-05` `data` `release` claimed with remaining are derived on read `src: Data model, release`
- [ ] `C-DM-06` `data` The allocations held, offered, confirmed per release never outnumber `release.total` `src: Data model, allocation`
- [ ] `C-DM-07` `data` A user holds at most one live allocation per release `src: Data model, allocation`
- [ ] `C-DM-08` `data` `venue_stock` keeps one row per venue per flavour, with unknown derived on read `src: Data model, venue_stock`
- [ ] `C-DM-09` `data` A user has at most one active alert per place per flavour `src: Data model, landing_alert`
- [ ] `C-DM-10` `data` Active held seats plus booked seats never exceed `capacity` `src: Data model, seat_hold`
- [ ] `C-DM-11` `data` `booking.reschedule_count` never exceeds one `src: Data model, booking`
- [ ] `C-DM-12` `data` `ritual.slug` is unique; a deleted ritual keeps the row with `deleted_at` set `src: Data model, ritual`
- [ ] `C-DM-13` `data` `cookie_choice.visitor_token` is unique `src: Data model, cookie_choice`
- [ ] `C-DM-14` `data` The chapter table holds eighteen rows in positions `0` to `17` `src: Data model, chapter`
- [ ] `C-DM-15` `data` Seeding is idempotent, so a restart duplicates nothing `src: Data model, seed data`
- [ ] `C-DM-16` `data` The seed holds the six releases, the eight places, the five venues, the six sessions `src: Data model, seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The chrome of mark, header pill, audio meter, footer persists across every chapter `src: Front-end specification, stack of layers`
- [ ] `C-FE-02` `ui` The house mark swaps between white with ink at the chapter boundary, never through a blend `src: Front-end specification, the mark`
- [ ] `C-FE-03` `ui` The header word matching the chapter sits at full ink strength `src: Front-end specification, the header pill`
- [ ] `C-FE-04` `ui` The header background unrolls sideways once the loader has finished `src: Front-end specification, the header pill`
- [ ] `C-FE-05` `ui` The header words rise into the bar one after another like dealt cards `src: Front-end specification, the header pill`
- [ ] `C-FE-06` `ui` The age panel exits as two shutters sliding apart, tipping away with perspective `src: Front-end specification, the age panel`
- [ ] `C-FE-07` `ui` Hovering an age panel control turns the control's frame with text blood red `src: Front-end specification, the age panel`
- [ ] `C-FE-08` `ui` The footer credits Lanternfish Studio with Low Hum Audio, both names underlined as links `src: Front-end specification, the footer`
- [ ] `C-FE-09` `ui` Every mark is geometry drawn in the page, never an image file `src: Front-end specification, iconography`
- [ ] `C-FE-10` `ui` Comic panel frames keep the ink thickness constant as panels grow `src: Front-end specification, iconography`
- [ ] `C-FE-11` `ui` Figures keep a wider band of in-between tone than stone `src: Front-end specification, the engraved material`
- [ ] `C-FE-12` `ui` A column fifty deep in the colonnade reads as separate drawn lines `src: Front-end specification, the engraved material`
- [ ] `C-FE-13` `ui` The portal with the column fracture advance in discrete jerks `src: Front-end specification, shared mechanisms`
- [ ] `C-FE-14` `ui` One wind bends robe, grass, rocks, beams the same way `src: Front-end specification, shared mechanisms`
- [ ] `C-FE-15` `ui` The temple light beams breathe as volumes rather than glows `src: Front-end specification, effect catalogue`
- [ ] `C-FE-16` `ui` Contact shadows under figures are hatched, stippled, never a soft blur `src: Front-end specification, effect catalogue`
- [ ] `C-FE-17` `ui` The drawn pointer follows the real pointer a beat behind `src: Front-end specification, effect catalogue`
- [ ] `C-FE-18` `ui` A narration box is pinned to a corner of the panel, overhanging, with blood red emphasis `src: Front-end specification, comic panels`
- [ ] `C-FE-19` `capability` With sound off, words light from the story position rather than waiting for a voice `src: Front-end specification, drawn type`
- [ ] `C-FE-20` `literal` The hidden text joins the poster into `Chill your spirit. The night starts after dinner. Shake your spirit. Let the night play on. Pour your spirit. What happens next is up to you.` `src: Front-end specification, the hidden text`
- [ ] `C-FE-21` `ui` The promise chapter justifies one light paragraph at about a third of the frame width `src: Front-end specification, the collection act`
- [ ] `C-FE-22` `ui` The bottle label wraps the pour line around the bottle, grained like paper `src: Front-end specification, the collection act`
- [ ] `C-FE-23` `ui` A handset held sideways gets circular previous with next arrows beside the bottle `src: Front-end specification, layout`
- [ ] `C-FE-24` `ui` The shelf entrance matches the header unroll `src: Front-end specification, the additions`
- [ ] `C-FE-25` `ui` An invalid field is named inline with the reason, keeping what was typed `src: Front-end specification, the additions`
- [ ] `C-FE-26` `ui` A closed release turns the hold control into a closed state naming why `src: Front-end specification, the additions`
- [ ] `C-FE-27` `capability` Figures breathe on the clock only when the story is still `src: Front-end specification, idle life`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` Two roles only, with hosts existing only as seeded accounts `src: Constraints`
- [ ] `C-CN-02` `constraint` No external network call at run time, no map tiles, no remote fonts `src: Constraints`
- [ ] `C-CN-03` `constraint` The age answer is never stored, on the server or in the browser `src: Constraints`
- [ ] `C-CN-04` `constraint` Nothing that changes stock, seats, rituals is queued for later `src: Constraints`
- [ ] `C-CN-05` `constraint` No messaging, comments, reviews, ratings, social feed `src: Constraints`
- [ ] `C-CN-06` `constraint` No chapter exists beyond the eighteen listed `src: Constraints`
- [ ] `C-CN-07` `constraint` Every one of the eighteen chapters is reachable by driving the story `src: Constraints`
- [ ] `C-CN-08` `constraint` The film ships no image, model, font atlas or sound file `src: Constraints`
- [ ] `C-CN-09` `capability` The app stays responsive with 5,000 allocations, 2,000 venues, 1,000 sessions, 10,000 rituals `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `contract` The URL with the port are read from the environment, never hardcoded `src: Deployment contract`
- [ ] `C-DC-03` `contract` The deployment uses no edge functions, persistent volumes, fixed container names, custom networks `src: Deployment contract`
- [ ] `C-DC-04` `contract` A list endpoint returns a top-level JSON array unless the table shows a wrapping object `src: Deployment contract`
- [ ] `C-DC-05` `literal` A call without a valid session answers `401` with the reason `unauthenticated` `src: Deployment contract`
- [ ] `C-DC-06` `literal` A missing row answers `404` with the reason `not_found` `src: Deployment contract`
- [ ] `C-DC-07` `literal` `GET /api/health` returns `status` with `checks` `src: Deployment contract`
- [ ] `C-DC-08` `literal` A ritual save beyond the hourly limit carries `cooldownSeconds` `src: Deployment contract`
- [ ] `C-DC-09` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173` `src: Deployment contract`
- [ ] `C-DC-10` `contract` The HTTP API sits on the same origin under `/api` `src: Deployment contract`
- [ ] `C-DC-11` `literal` `GET /api/health` returns `200` once ready `src: Deployment contract`
- [ ] `C-DC-12` `contract` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-13` `contract` Seeded logins are written to `/app/USER_README.md` `src: Deployment contract`
- [ ] `C-DC-14` `contract` Reserved `.browser_screenshots/` with `.downloads/` directories exist, empty `src: Deployment contract`
- [ ] `C-DC-15` `contract` A production build is served, never a dev server `src: Deployment contract`
- [ ] `C-DC-16` `contract` The server keeps running after the session ends, outside the shell `src: Deployment contract`
- [ ] `C-DC-17` `contract` The server binds `0.0.0.0`, never `127.0.0.1` or `localhost` `src: Deployment contract`
- [ ] `C-DC-18` `contract` The app never downloads or starts a copy of a backing service `src: Deployment contract`
- [ ] `C-DC-19` `contract` The app reads `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` for Mailpit `src: Deployment contract, environment variables`
- [ ] `C-DC-20` `contract` A refusal body carries `reason` with `message` `src: Deployment contract, API shapes`
- [ ] `C-DC-21` `contract` A client error is never answered as a server error or a silent success `src: Deployment contract, API shapes`
- [ ] `C-DC-22` `contract` Every call outside the public ones carries the bearer token `src: Deployment contract, API shapes`
- [ ] `C-DC-23` `contract` A claim, booking or ritual save accepts an optional `Idempotency-Key` header `src: Deployment contract, API shapes`
- [ ] `C-DC-24` `contract` A shelf, venue list or booking kept only in the browser is a contract violation `src: Deployment contract, no stand-ins`
- [ ] `C-DC-25` `contract` A confirmation reported as sent without a real message in Mailpit is a contract violation `src: Deployment contract, no stand-ins`

## Pinned literals

| Value | What it is | Item |
|---|---|---|
| `MARSHMALLOW COFFEE & CREAM` | pinned by Overview | `C-OV-02` |
| `ORANGE CHOCOLATE & CREAM` | pinned by Overview | `C-OV-02` |
| `MINT CHOCOLATE & CREAM` | pinned by Overview | `C-OV-02` |
| `13% ABV` | pinned by Overview | `C-OV-03` |
| `700 ML` | pinned by Overview | `C-OV-03` |
| `visitor@example.com` | pinned by User roles | `C-RL-14` |
| `visitor2@example.com` | pinned by User roles | `C-RL-14` |
| `host@example.com` | pinned by User roles | `C-RL-14` |
| `host2@example.com` | pinned by User roles | `C-RL-14` |
| `deku-demo-pw-2026` | pinned by User roles | `C-RL-15` |
| `The Gilded Nave` | pinned by User roles | `C-RL-16` |
| `Salt & Vesper` | pinned by User roles | `C-RL-17` |
| `POST /api/auth/login` | pinned by Core features rule 1 | `C-CF-01` |
| `access_token` | pinned by Core features rule 1 | `C-CF-01` |
| `POST /api/v1/auth/link` | pinned by Core features rule 2 | `C-CF-03` |
| `202` | pinned by Core features rule 2 | `C-CF-03` |
| `Your Vesperi sign-in link` | pinned by Core features rule 2 | `C-CF-04` |
| `Sign-in code:` | pinned by Core features rule 2 | `C-CF-05` |
| `POST /api/v1/auth/session` | pinned by Core features rule 3 | `C-CF-08` |
| `session` | pinned by Core features rule 3 | `C-CF-08` |
| `invalid_token` | pinned by Core features rule 3 | `C-CF-11` |
| `GET /api/v1/me` | pinned by Core features rule 5 | `C-CF-15` |
| `email` | pinned by Core features rule 5 | `C-CF-15` |
| `role` | pinned by Core features rule 5 | `C-CF-15` |
| `POST /api/auth/logout` | pinned by Core features rule 5 | `C-CF-17` |
| `/` | pinned by Core features rule 8 | `C-CF-21` |
| `wander` | pinned by Core features rule 12 | `C-CF-29` |
| `footer` | pinned by Core features rule 12 | `C-CF-29` |
| `THE NOCTURNE EXPERIENCE` | pinned by Core features rule 13 | `C-CF-31` |
| `EXPERIENCE` | pinned by Core features rule 14 | `C-CF-38` |
| `COLLECTION` | pinned by Core features rule 14 | `C-CF-39` |
| `products` | pinned by Core features rule 14 | `C-CF-39` |
| `#experience` | pinned by Core features rule 14 | `C-CF-40` |
| `#collection` | pinned by Core features rule 14 | `C-CF-40` |
| `/unsupported` | pinned by Core features rule 16 | `C-CF-47` |
| `Your browser is not supported` | pinned by Core features rule 16 | `C-CF-47` |
| `/?mode=still` | pinned by Core features rule 16 | `C-CF-48` |
| `Please rotate your device.` | pinned by Core features rule 17 | `C-CF-49` |
| `Are you of legal age?` | pinned by Core features rule 19 | `C-CF-54` |
| `/terms` | pinned by Core features rule 19 | `C-CF-58` |
| `/alerts/cancel` | pinned by Core features rule 19 | `C-CF-58` |
| `ACCESS DENIED` | pinned by Core features rule 20 | `C-CF-59` |
| `You need to be of legal age to access.` | pinned by Core features rule 20 | `C-CF-59` |
| `GO BACK` | pinned by Core features rule 20 | `C-CF-60` |
| `HOLD & MOVE` | pinned by Core features rule 23 | `C-CF-64` |
| `HOLD & POUR` | pinned by Core features rule 24 | `C-CF-68` |
| `INDULGE NOW` | pinned by Core features rule 34 | `C-CF-88` |
| `ATONE LATER` | pinned by Core features rule 34 | `C-CF-88` |
| `flavour-a` | pinned by Core features rule 37 | `C-CF-96` |
| `flavour-c` | pinned by Core features rule 37 | `C-CF-96` |
| `flavour-b` | pinned by Core features rule 37 | `C-CF-96` |
| `NOCTURNE N.02` | pinned by Core features rule 38 | `C-CF-97` |
| `Select Houses Forthcoming` | pinned by Core features rule 39 | `C-CF-99` |
| `GET /api/v1/content` | pinned by Core features rule 40 | `C-CF-101` |
| `releases` | pinned by Core features rule 40 | `C-CF-101` |
| `flavours` | pinned by Core features rule 40 | `C-CF-101` |
| `chapters` | pinned by Core features rule 40 | `C-CF-101` |
| `credits` | pinned by Core features rule 40 | `C-CF-101` |
| `legal` | pinned by Core features rule 40 | `C-CF-101` |
| `marshmallow-coffee` | pinned by Core features rule 40 | `C-CF-102` |
| `orange-chocolate` | pinned by Core features rule 40 | `C-CF-102` |
| `mint-chocolate` | pinned by Core features rule 40 | `C-CF-102` |
| `AN EMPTY SHELF IS A KIND OF PATIENCE` | pinned by Core features rule 42 | `C-CF-106` |
| `GET /api/v1/releases/{releaseId}` | pinned by Core features rule 43 | `C-CF-109` |
| `total` | pinned by Core features rule 43 | `C-CF-109` |
| `claimed` | pinned by Core features rule 43 | `C-CF-109` |
| `remaining` | pinned by Core features rule 43 | `C-CF-109` |
| `GET /api/v1/releases` | pinned by Deployment contract | `C-CF-110` |
| `VESPERI` | pinned by Front-end specification, copy | `C-CF-111` |
| `SPIRITS` | pinned by Front-end specification, copy | `C-CF-111` |
| `NOCTURNE` | pinned by Front-end specification, copy | `C-CF-111` |
| `AN ODE TO THE NIGHT, YOUR NIGHT` | pinned by Front-end specification, copy | `C-CF-111` |
| `POST /api/v1/cellar/holds` | pinned by Core features rule 44 | `C-CF-113` |
| `201` | pinned by Core features rule 44 | `C-CF-113` |
| `held` | pinned by Core features rule 44 | `C-CF-113` |
| `YOURS FOR 72 HOURS` | pinned by Core features rule 44 | `C-CF-115` |
| `invalid_flavour` | pinned by Core features rule 45 | `C-CF-116` |
| `closed` | pinned by Core features rule 45 | `C-CF-117` |
| `already_held` | pinned by Core features rule 46 | `C-CF-118` |
| `exhausted` | pinned by Core features rule 47 | `C-CF-119` |
| `position` | pinned by Core features rule 47 | `C-CF-119` |
| `YOU ARE NUMBER {n} IN LINE` | pinned by Core features rule 47 | `C-CF-120` |
| `GET /api/v1/cellar` | pinned by Core features rule 50 | `C-CF-125` |
| `items` | pinned by Core features rule 50 | `C-CF-125` |
| `allocationId` | pinned by Core features rule 50 | `C-CF-125` |
| `releaseId` | pinned by Core features rule 50 | `C-CF-125` |
| `flavour` | pinned by Core features rule 50 | `C-CF-125` |
| `state` | pinned by Core features rule 50 | `C-CF-125` |
| `expiresAt` | pinned by Core features rule 50 | `C-CF-125` |
| `waitlisted` | pinned by Core features rule 51 | `C-CF-128` |
| `offered` | pinned by Core features rule 51 | `C-CF-128` |
| `DELETE /api/v1/cellar/holds/{allocationId}` | pinned by Core features rule 52 | `C-CF-130` |
| `204` | pinned by Core features rule 52 | `C-CF-130` |
| `A bottle came back for you:` | pinned by Core features rule 52 | `C-CF-132` |
| `POST /api/v1/cellar/holds/{allocationId}/accept` | pinned by Core features rule 53 | `C-CF-133` |
| `POST /api/v1/cellar/holds/{allocationId}/decline` | pinned by Core features rule 53 | `C-CF-134` |
| `lapsed` | pinned by Core features rule 53 | `C-CF-135` |
| `not_offered` | pinned by Core features rule 53 | `C-CF-136` |
| `POST /api/v1/cellar/holds/{allocationId}/confirm` | pinned by Core features rule 54 | `C-CF-138` |
| `N02` | pinned by Core features rule 58 | `C-CF-150` |
| `240` | pinned by Core features rule 58 | `C-CF-150` |
| `N02-CASK` | pinned by Core features rule 58 | `C-CF-151` |
| `1` | pinned by Core features rule 58 | `C-CF-151` |
| `N02-SALON` | pinned by Core features rule 58 | `C-CF-152` |
| `N02-VESTRY` | pinned by Core features rule 58 | `C-CF-152` |
| `N01` | pinned by Core features rule 58 | `C-CF-153` |
| `N04` | pinned by Core features rule 58 | `C-CF-153` |
| `17:00 to 01:00` | pinned by Core features rule 74 | `C-CF-154` |
| `GET /api/v1/venues/{id}` | pinned by Core features rule 64 | `C-CF-155` |
| `address` | pinned by Core features rule 64 | `C-CF-155` |
| `hours` | pinned by Core features rule 64 | `C-CF-155` |
| `timezone` | pinned by Core features rule 64 | `C-CF-155` |
| `N02-EMBER` | pinned by Core features rule 58 | `C-CF-158` |
| `Early Pour at Salt & Vesper` | pinned by Core features rule 89 | `C-CF-159` |
| `239` | pinned by Core features rule 58 | `C-CF-160` |
| `GET /api/v1/places?q=` | pinned by Core features rule 60 | `C-CF-164` |
| `Newport` | pinned by Core features rule 60 | `C-CF-165` |
| `Newport, Wales` | pinned by Core features rule 60 | `C-CF-165` |
| `Newport, Isle of Wight` | pinned by Core features rule 60 | `C-CF-165` |
| `GET /api/v1/venues` | pinned by Core features rule 61 | `C-CF-166` |
| `region` | pinned by Core features rule 61 | `C-CF-166` |
| `venues` | pinned by Core features rule 61 | `C-CF-166` |
| `radius` | pinned by Core features rule 61 | `C-CF-167` |
| `50` | pinned by Core features rule 61 | `C-CF-167` |
| `invalid_radius` | pinned by Core features rule 61 | `C-CF-167` |
| `5` | pinned by Core features rule 62 | `C-CF-170` |
| `0.2` | pinned by Core features rule 62 | `C-CF-170` |
| `4.1` | pinned by Core features rule 62 | `C-CF-170` |
| `3` | pinned by Core features rule 62 | `C-CF-171` |
| `in` | pinned by Core features rule 63 | `C-CF-172` |
| `low` | pinned by Core features rule 63 | `C-CF-172` |
| `out` | pinned by Core features rule 63 | `C-CF-172` |
| `unknown` | pinned by Core features rule 63 | `C-CF-172` |
| `LAST SEEN {n} DAYS AGO` | pinned by Core features rule 63 | `C-CF-176` |
| `GET /api/v1/regions/{code}` | pinned by Core features rule 65 | `C-CF-179` |
| `listingAllowed` | pinned by Core features rule 65 | `C-CF-179` |
| `notice` | pinned by Core features rule 65 | `C-CF-179` |
| `WE CANNOT LIST HOUSES WHERE YOU ARE` | pinned by Core features rule 65 | `C-CF-181` |
| `NOTHING NEAR YOU YET` | pinned by Core features rule 66 | `C-CF-183` |
| `POST /api/v1/alerts` | pinned by Core features rule 68 | `C-CF-186` |
| `active` | pinned by Core features rule 68 | `C-CF-186` |
| `restricted` | pinned by Core features rule 68 | `C-CF-188` |
| `invalid_place` | pinned by Deployment contract | `C-CF-189` |
| `Alert set:` | pinned by Core features rule 69 | `C-CF-190` |
| `THAT ALERT IS OFF` | pinned by Core features rule 69 | `C-CF-192` |
| `fired` | pinned by Core features rule 70 | `C-CF-195` |
| `GET /api/v1/alerts` | pinned by Core features rule 71 | `C-CF-200` |
| `DELETE /api/v1/alerts/{id}` | pinned by Core features rule 71 | `C-CF-201` |
| `Soho` | pinned by Core features rule 73 | `C-CF-203` |
| `Shoreditch` | pinned by Core features rule 73 | `C-CF-203` |
| `Leith` | pinned by Core features rule 73 | `C-CF-203` |
| `Bergen` | pinned by Core features rule 73 | `C-CF-203` |
| `NO` | pinned by Core features rule 73 | `C-CF-204` |
| `The Chapel Cellar` | pinned by Core features rule 74 | `C-CF-205` |
| `Le Confessionnal` | pinned by Core features rule 74 | `C-CF-205` |
| `Nordlys Bar` | pinned by Core features rule 74 | `C-CF-205` |
| `GET /api/v1/tastings` | pinned by Core features rule 76 | `C-CF-208` |
| `startsAt` | pinned by Core features rule 76 | `C-CF-208` |
| `capacity` | pinned by Core features rule 76 | `C-CF-208` |
| `price` | pinned by Core features rule 76 | `C-CF-208` |
| `3500` | pinned by Core features rule 76 | `C-CF-209` |
| `$35.00` | pinned by Core features rule 76 | `C-CF-209` |
| `usd` | pinned by Core features rule 76 | `C-CF-209` |
| `scheduled` | pinned by Core features rule 76 | `C-CF-210` |
| `POST /api/v1/tastings/{id}/holds` | pinned by Core features rule 78 | `C-CF-213` |
| `holdId` | pinned by Core features rule 78 | `C-CF-213` |
| `8` | pinned by Core features rule 78 | `C-CF-214` |
| `invalid_party_size` | pinned by Core features rule 78 | `C-CF-214` |
| `insufficient` | pinned by Core features rule 78 | `C-CF-215` |
| `hold_elsewhere` | pinned by Core features rule 78 | `C-CF-216` |
| `DELETE /api/v1/tastings/holds/{holdId}` | pinned by Core features rule 78 | `C-CF-217` |
| `SEATS HELD FOR {n}` | pinned by Core features rule 80 | `C-CF-219` |
| `POST /api/v1/bookings` | pinned by Core features rule 81 | `C-CF-221` |
| `booked` | pinned by Core features rule 81 | `C-CF-221` |
| `GET /api/v1/bookings` | pinned by Core features rule 83 | `C-CF-222` |
| `Tasting booked:` | pinned by Core features rule 82 | `C-CF-224` |
| `DELETE /api/v1/bookings/{id}` | pinned by Core features rule 83 | `C-CF-227` |
| `late` | pinned by Core features rule 83 | `C-CF-228` |
| `POST /api/v1/bookings/{id}/reschedule` | pinned by Core features rule 84 | `C-CF-230` |
| `sessionId` | pinned by Core features rule 84 | `C-CF-230` |
| `already_rescheduled` | pinned by Core features rule 84 | `C-CF-231` |
| `FULL. JOIN THE LINE` | pinned by Core features rule 85 | `C-CF-233` |
| `POST /api/v1/tastings/{id}/waitlist` | pinned by Core features rule 85 | `C-CF-234` |
| `409` | pinned by Core features rule 85 | `C-CF-235` |
| `not_full` | pinned by Core features rule 85 | `C-CF-235` |
| `Tasting cancelled:` | pinned by Core features rule 86 | `C-CF-238` |
| `edit_window_closed` | pinned by Core features rule 98 | `C-CF-241` |
| `session_started` | pinned by Core features rule 84 | `C-CF-242` |
| `Late Pour at Salt & Vesper` | pinned by Core features rule 89 | `C-CF-249` |
| `Cellar Tasting at The Chapel Cellar` | pinned by Core features rule 89 | `C-CF-250` |
| `2` | pinned by Core features rule 89 | `C-CF-250` |
| `Sold Out Supper at The Gilded Nave` | pinned by Core features rule 89 | `C-CF-251` |
| `Nocturne Night at The Gilded Nave` | pinned by Core features rule 89 | `C-CF-252` |
| `Europe/London` | pinned by Core features rule 89 | `C-CF-252` |
| `Soiree Nocturne at Le Confessionnal` | pinned by Core features rule 89 | `C-CF-253` |
| `Europe/Paris` | pinned by Core features rule 89 | `C-CF-253` |
| `Last Call at Salt & Vesper` | pinned by Core features rule 89 | `C-CF-254` |
| `GET /api/v1/ingredients` | pinned by Core features rule 91 | `C-CF-258` |
| `mixers` | pinned by Core features rule 91 | `C-CF-258` |
| `ices` | pinned by Core features rule 91 | `C-CF-258` |
| `garnishes` | pinned by Core features rule 91 | `C-CF-258` |
| `cold-brew` | pinned by Core features rule 91 | `C-CF-259` |
| `tonic` | pinned by Core features rule 91 | `C-CF-259` |
| `oat-milk` | pinned by Core features rule 91 | `C-CF-259` |
| `soda` | pinned by Core features rule 91 | `C-CF-259` |
| `espresso` | pinned by Core features rule 91 | `C-CF-259` |
| `ginger-ale` | pinned by Core features rule 91 | `C-CF-259` |
| `no-ice` | pinned by Core features rule 91 | `C-CF-260` |
| `cubed` | pinned by Core features rule 91 | `C-CF-260` |
| `crushed` | pinned by Core features rule 91 | `C-CF-260` |
| `single-block` | pinned by Core features rule 91 | `C-CF-260` |
| `no-garnish` | pinned by Core features rule 91 | `C-CF-261` |
| `orange-twist` | pinned by Core features rule 91 | `C-CF-261` |
| `mint-sprig` | pinned by Core features rule 91 | `C-CF-261` |
| `grated-nutmeg` | pinned by Core features rule 91 | `C-CF-261` |
| `cocoa-dust` | pinned by Core features rule 91 | `C-CF-261` |
| `gold-leaf` | pinned by Core features rule 92 | `C-CF-262` |
| `invalid_ingredient` | pinned by Core features rule 92 | `C-CF-262` |
| `too_many_mixers` | pinned by Core features rule 92 | `C-CF-263` |
| `40` | pinned by Core features rule 92 | `C-CF-264` |
| `invalid_name` | pinned by Core features rule 92 | `C-CF-264` |
| `POST /api/v1/rituals` | pinned by Core features rule 92 | `C-CF-265` |
| `slug` | pinned by Core features rule 92 | `C-CF-265` |
| `casino` | pinned by Core features rule 93 | `C-CF-266` |
| `crypto` | pinned by Core features rule 93 | `C-CF-266` |
| `loan` | pinned by Core features rule 93 | `C-CF-266` |
| `viagra` | pinned by Core features rule 93 | `C-CF-266` |
| `name_refused` | pinned by Core features rule 93 | `C-CF-266` |
| `429` | pinned by Core features rule 95 | `C-CF-269` |
| `rate_limited` | pinned by Core features rule 95 | `C-CF-269` |
| `ENOUGH FOR NOW. TRY AGAIN IN {n}` | pinned by Core features rule 95 | `C-CF-270` |
| `velvet-hour-7k2q` | pinned by Core features rule 96 | `C-CF-272` |
| `GET /api/v1/rituals/{slug}` | pinned by Core features rule 97 | `C-CF-273` |
| `name` | pinned by Core features rule 97 | `C-CF-273` |
| `ice` | pinned by Core features rule 97 | `C-CF-273` |
| `garnish` | pinned by Core features rule 97 | `C-CF-273` |
| `PATCH /api/v1/rituals/{slug}` | pinned by Core features rule 98 | `C-CF-276` |
| `forbidden` | pinned by Core features rule 98 | `C-CF-276` |
| `DELETE /api/v1/rituals/{slug}` | pinned by Core features rule 98 | `C-CF-277` |
| `Gold leaf` | pinned by Core features rule 99 | `C-CF-280` |
| `Espresso` | pinned by Core features rule 99 | `C-CF-280` |
| `Oat milk` | pinned by Core features rule 99 | `C-CF-280` |
| `THAT ONE IS GONE. POUR YOUR OWN` | pinned by Core features rule 99 | `C-CF-281` |
| `midnight-confession-a1b2` | pinned by Core features rule 102 | `C-CF-284` |
| `Midnight Confession` | pinned by Core features rule 102 | `C-CF-284` |
| `GET /api/v1/host/venue` | pinned by Core features rule 104 | `C-CF-287` |
| `stock` | pinned by Core features rule 104 | `C-CF-287` |
| `sessions` | pinned by Core features rule 104 | `C-CF-287` |
| `PUT /api/v1/venues/{id}/stock` | pinned by Core features rule 104 | `C-CF-288` |
| `reading` | pinned by Core features rule 104 | `C-CF-288` |
| `invalid_reading` | pinned by Core features rule 104 | `C-CF-289` |
| `POST /api/v1/tastings/{id}/cancel` | pinned by Core features rule 105 | `C-CF-290` |
| `cancelled` | pinned by Core features rule 105 | `C-CF-290` |
| `invalid_credentials` | pinned by Core features rule 1 | `C-CF-293` |
| `POST /api/v1/cookie-choice` | pinned by Core features rule 108 | `C-CF-302` |
| `nonEssentialAccepted` | pinned by Core features rule 108 | `C-CF-302` |
| `GET /api/v1/cookie-choice` | pinned by Core features rule 108 | `C-CF-303` |
| `invalid_request` | pinned by Deployment contract | `C-CF-304` |
| `/favicon.ico` | pinned by Core features rule 109 | `C-CF-306` |
| `/sitemap.xml` | pinned by Core features rule 110 | `C-CF-307` |
| `/where` | pinned by Core features rule 110 | `C-CF-307` |
| `/tastings` | pinned by Core features rule 110 | `C-CF-307` |
| `/ritual` | pinned by Core features rule 110 | `C-CF-307` |
| `/robots.txt` | pinned by Core features rule 110 | `C-CF-309` |
| `Sitemap:` | pinned by Core features rule 110 | `C-CF-309` |
| `/og/default.png` | pinned by Core features rule 111 | `C-CF-310` |
| `/og/ritual/{slug}.png` | pinned by Core features rule 111 | `C-CF-311` |
| `Toggle audio` | pinned by Core features rule 113 | `C-CF-317` |
| `previous slide` | pinned by Core features rule 113 | `C-CF-317` |
| `next slide` | pinned by Core features rule 113 | `C-CF-317` |
| `left text` | pinned by Core features rule 113 | `C-CF-317` |
| `right text` | pinned by Core features rule 113 | `C-CF-317` |
| `INSTAGRAM` | pinned by User flow, footer | `C-UF-02` |
| `hello@example.com` | pinned by User flow, footer | `C-UF-02` |
| `Legal` | pinned by User flow, footer | `C-UF-02` |
| `Tastings` | pinned by User flow, footer | `C-UF-02` |
| `/host` | pinned by User flow, entry and redirects | `C-UF-03` |
| `/sign-in` | pinned by User flow, entry and redirects | `C-UF-03` |
| `/cellar` | pinned by User flow route table | `C-UF-04` |
| `/ritual/{slug}` | pinned by User flow route table | `C-UF-05` |
| `GET /api/health` | pinned by Technical requirements, health | `C-TR-15` |
| `200` | pinned by Technical requirements, health | `C-TR-15` |
| `width=device-width` | pinned by Technical requirements, launch files | `C-TR-20` |
| `Chill your spirit. The night starts after dinner. Shake your spirit. Let the night play on. Pour your spirit. What happens next is up to you.` | pinned by Front-end specification, the hidden text | `C-FE-20` |
| `401` | pinned by Deployment contract | `C-DC-05` |
| `unauthenticated` | pinned by Deployment contract | `C-DC-05` |
| `404` | pinned by Deployment contract | `C-DC-06` |
| `not_found` | pinned by Deployment contract | `C-DC-06` |
| `status` | pinned by Deployment contract | `C-DC-07` |
| `checks` | pinned by Deployment contract | `C-DC-07` |
| `cooldownSeconds` | pinned by Deployment contract | `C-DC-08` |
| `/sign-in/verify?token=` | the sign-in link path | `C-CF-06` |
| `Listing where drink is sold is not permitted in this region.` | the NO region notice | `C-CF-204` |
| `Toasted marshmallow and cold brew over vanilla cream, finishing on bitter cocoa.` | the marshmallow tasting notes | `C-CF-92` |
| `Candied orange peel folded into milk chocolate and cream, with a warm clove finish.` | the orange tasting notes | `C-CF-93` |
| `Garden mint over dark chocolate and sweet cream, cool and long.` | the mint tasting notes | `C-CF-94` |
| `NAME IT` | the ritual save label | `C-CF-305` |
| `Made by Lanternfish Studio and Low Hum Audio` | the footer credit line | `C-FE-08` |
| `Nocturne N.02 Salon Pour` | the salon release name | `C-CF-152` |
| `Idempotency-Key` | the repeat-safety header | `C-DC-23` |
| `KEEP THIS ONE` | the keep label | `C-CF-98` |
| `IT WENT BACK. CLAIM ANOTHER` | the went-back line | `C-CF-127` |
| `TELL ME WHEN IT LANDS` | the alert action | `C-CF-183` |
| `Cancel this alert:` | the cancel line | `C-CF-191` |
| `It has landed near you:` | the landed prefix | `C-CF-195` |
| `TOO LATE TO CANCEL. MOVE IT INSTEAD` | the too-late line | `C-CF-229` |
| `SOMEONE POURED THIS FOR YOU` | the poured-for-you line | `C-CF-278` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact shades behind each named colour role | `C-UX-06` |
| the exact type families, the exact sizes | `C-UX-14` |
| the base spacing unit the additions derive from | `C-UX-31` |
| the exact durations behind the named movements | `C-UX-19` |
| the widths at which the additions stack | `C-UX-28` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 2 | 11 |
| User roles | 1 | 17 |
| Core features | 64 | 317 |
| User flow | 10 | 21 |
| UI and UX notes | 12 | 38 |
| Technical requirements | 6 | 20 |
| Data model | 6 | 16 |
| Front-end specification | 13 | 27 |
| Constraints | 0 | 9 |
| Deployment contract | 12 | 25 |
