# Checklist: The New Hollywood Photography Exhibition

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, deployment
Sections absent: buildplan
Items: 436
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` A visitor scrolls the title sequence into the gallery chooser `src: Overview para 2`
- [ ] `C-OV-02` `capability` A visitor reserves a timed visit that comes back with a reservation code `src: Overview para 2`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out visitor opens every exhibition route other than the selection route without an account `src: User roles table row 1`
- [ ] `C-RL-02` `role` A signed-out API call saving a frame is denied `src: User roles authorization paragraph`
- [ ] `C-RL-03` `role` A signed-out API call reserving a visit is denied `src: User roles authorization paragraph`
- [ ] `C-RL-04` `role` A signed-out API call reading a selection is denied `src: User roles table row 1`
- [ ] `C-RL-05` `role` A signed-out API call listing reservations is denied `src: User roles table row 1`
- [ ] `C-RL-06` `role` A signed-out API call cancelling a reservation is denied `src: User roles table row 1`
- [ ] `C-RL-07` `role` One visitor cancelling another visitor's reservation is denied `src: User roles ownership paragraph`
- [ ] `C-RL-08` `data` A denied cancel leaves the other visitor's reservation row confirmed `src: User roles ownership paragraph`
- [ ] `C-RL-09` `data` A denied cancel leaves the places left of that entry time unchanged `src: User roles ownership paragraph`
- [ ] `C-RL-10` `role` A visitor's reservation list holds only that visitor's reservations `src: User roles ownership paragraph`
- [ ] `C-RL-11` `role` A visitor's selection list holds only that visitor's frames `src: User roles ownership paragraph`
- [ ] `C-RL-12` `capability` Anyone creates a visitor account at the signup route `src: User roles signup paragraph`
- [ ] `C-RL-13` `literal` Every seeded visitor signs in with `deku-demo-pw-2026` `src: User roles signup paragraph`
- [ ] `C-RL-14` `literal` `visitor@example.com` is seeded with display name `Nadia Rowe` `src: User roles signup paragraph`
- [ ] `C-RL-15` `literal` `visitor2@example.com` is seeded with display name `Omar Lindgren` `src: User roles signup paragraph`
- [ ] `C-RL-16` `literal` `visitor3@example.com` is seeded with display name `Hana Petrov` `src: User roles signup paragraph`

## C-CF Core features

- [ ] `C-CF-01` `contract` Signup creates a visitor row carrying the display name `src: Core features rule 1`
- [ ] `C-CF-02` `contract` The signup response carries `id`, `email`, `displayName` `src: Core features rule 1`
- [ ] `C-CF-03` `data` Signup stores the email lowercased `src: Core features rule 1`
- [ ] `C-CF-04` `contract` A signup with a registered email in another letter case is rejected `src: Core features rule 2`
- [ ] `C-CF-05` `contract` A signup password shorter than 10 characters is rejected naming `password` `src: Core features rule 3`
- [ ] `C-CF-06` `contract` A signup with a malformed email is rejected naming `email` `src: Core features rule 3`
- [ ] `C-CF-07` `contract` An email lacking one `@`, a character before the `@` or a dotted domain after the `@` is refused as malformed `src: Core features rule 3`
- [ ] `C-CF-08` `contract` A signup `displayName` that is empty or longer than 60 characters is rejected naming `displayName` `src: Core features rule 3`
- [ ] `C-CF-09` `contract` Login with the correct password returns an `access_token` `src: Core features rule 4`
- [ ] `C-CF-10` `contract` Login with a wrong password is denied `src: Core features rule 4`
- [ ] `C-CF-11` `constraint` The wrong-password refusal matches the refusal for an unregistered email `src: Core features rule 4`
- [ ] `C-CF-12` `contract` A visitor-only call with a malformed bearer token is denied `src: Core features rule 5`
- [ ] `C-CF-13` `contract` `GET /api/me` without a token is denied `src: Core features rule 5`
- [ ] `C-CF-14` `contract` A visitor-only call carries an `Authorization` header of `Bearer` followed by the token `src: Core features rule 5`
- [ ] `C-CF-15` `contract` `GET /api/me` returns `id`, `email`, `displayName` of the token's own visitor `src: Core features rule 6`
- [ ] `C-CF-16` `constraint` Passwords are stored hashed rather than as written `src: Core features rule 7`
- [ ] `C-CF-17` `ui` The signup form labels its fields Email, Password, Display name `src: Core features rule 8`
- [ ] `C-CF-18` `ui` The sign-in form labels its fields Email, Password `src: Core features rule 8`
- [ ] `C-CF-19` `literal` The signup form submits with a `Create account` button `src: Core features rule 8`
- [ ] `C-CF-20` `literal` The sign-in form submits with a `Sign in` button `src: Core features rule 8`
- [ ] `C-CF-21` `capability` A successful signup signs the visitor in `src: Core features rule 8`
- [ ] `C-CF-22` `literal` The sign-in form links to the signup route with `Create an account` `src: Core features rule 8`
- [ ] `C-CF-23` `literal` The landing route carries the document title `The New Hollywood Photography Exhibition` `src: Core features rule 9`
- [ ] `C-CF-24` `literal` The landing lock-up carries `THE`, `AURA`, `Gazette`, `HOLLYWOOD` `src: Core features rule 9`
- [ ] `C-CF-25` `ui` A handwritten script `and` joins the two partner titles in the lock-up `src: Core features rule 9`
- [ ] `C-CF-26` `ui` `HOLLYWOOD` sits largest in muted grey beneath the partner titles `src: Core features rule 9`
- [ ] `C-CF-27` `literal` The landing subtitle reads `As seen in the Beacon Tower, located in` over `New York City` `src: Core features rule 10`
- [ ] `C-CF-28` `ui` A small ring turns beneath the subtitle before the landing is scrolled `src: Core features rule 10`
- [ ] `C-CF-29` `capability` Scrolling the landing sends tilted photographic planes out of depth into two upright covers `src: Core features rule 11`
- [ ] `C-CF-30` `capability` Scrolling back up runs the title sequence in reverse into the lock-up `src: Core features rule 11`
- [ ] `C-CF-31` `literal` The chooser prompt reads `Choose which gallery you want to explore` `src: Core features rule 12`
- [ ] `C-CF-32` `capability` The AURA cover links to `/aura-intro` `src: Core features rule 12`
- [ ] `C-CF-33` `capability` The Gazette cover links to `/gazette-intro` `src: Core features rule 12`
- [ ] `C-CF-34` `ui` Both chooser covers are reachable by keyboard `src: Core features rule 12`
- [ ] `C-CF-35` `constraint` The AURA cover sits left of the Gazette cover in the chooser `src: Core features rule 12`
- [ ] `C-CF-36` `constraint` The landing carries no menu control `src: Core features rule 13`
- [ ] `C-CF-37` `constraint` The landing carries no header `src: Core features rule 13`
- [ ] `C-CF-38` `ui` Each introduction heading stacks THE, NEW, HOLLYWOOD one word per line `src: Core features rule 15`
- [ ] `C-CF-39` `literal` The AURA introduction route carries the document title `AURA: The New Hollywood` `src: Core features rule 14`
- [ ] `C-CF-40` `literal` The Gazette introduction route carries the document title `Gazette Goes to Hollywood` `src: Core features rule 14`
- [ ] `C-CF-41` `literal` The AURA manifesto reads as the three pinned paragraphs `src: Core features rule 16`
- [ ] `C-CF-42` `literal` The Gazette manifesto reads as the three pinned paragraphs `src: Core features rule 16`
- [ ] `C-CF-43` `ui` The manifesto reveals character by character as the passage scrolls into view `src: Core features rule 16`
- [ ] `C-CF-44` `ui` The manifesto characters un-reveal as the passage scrolls away `src: Core features rule 16`
- [ ] `C-CF-45` `ui` A hand-drawn signature draws itself on over the introduction credit `src: Core features rule 17`
- [ ] `C-CF-46` `literal` The AURA introduction credit reads `Photographs by Celine Armand` then `for AURA` `src: Core features rule 17`
- [ ] `C-CF-47` `literal` The Gazette introduction credit reads `Photographs by Tomas Ekwueme` then `for Gazette` `src: Core features rule 17`
- [ ] `C-CF-48` `constraint` The introductions carry no other footer, link row or social bar `src: Core features rule 17`
- [ ] `C-CF-49` `capability` `Go to Gallery` on an introduction opens that title's gallery `src: Core features rule 18`
- [ ] `C-CF-50` `literal` The AURA gallery route carries the document title `AURA: The New Hollywood` `src: Core features rule 19`
- [ ] `C-CF-51` `literal` The Gazette gallery route carries the document title `Gazette Goes to Hollywood` `src: Core features rule 19`
- [ ] `C-CF-52` `ui` Gallery wordmarks rest in a muted grey `src: Core features rule 19`
- [ ] `C-CF-53` `ui` The AURA gallery opens on an upright serif AURA wordmark over a near-black ground `src: Core features rule 19`
- [ ] `C-CF-54` `ui` The Gazette gallery opens on a swash Gazette wordmark over a pale grey ground `src: Core features rule 19`
- [ ] `C-CF-55` `literal` Each gallery carries the prompt `Scroll to explore` shown in capitals `src: Core features rule 20`
- [ ] `C-CF-56` `ui` The `Scroll to explore` prompt fades as the first photographs enter `src: Core features rule 20`
- [ ] `C-CF-57` `ui` The gallery header slides away on downward scroll `src: Core features rule 21`
- [ ] `C-CF-58` `ui` The gallery header slides back on upward scroll `src: Core features rule 21`
- [ ] `C-CF-59` `ui` The gallery header carries the text controls `View` beside `Menu` `src: Core features rule 21`
- [ ] `C-CF-60` `ui` Hiding the gallery header leaves the column layout in place `src: Core features rule 21`
- [ ] `C-CF-61` `data` The gallery API returns the frames in column order `src: Core features rule 25`
- [ ] `C-CF-62` `ui` Each photograph fills the column width from the centre, cropping rather than letterboxing `src: Core features rule 22`
- [ ] `C-CF-63` `ui` AURA frames carry a white AURA masthead `src: Core features rule 22`
- [ ] `C-CF-64` `ui` Gazette frames carry a pink Gazette masthead `src: Core features rule 22`
- [ ] `C-CF-65` `constraint` Each masthead over a photograph is live text rather than a picture `src: Core features rule 22`
- [ ] `C-CF-66` `literal` Frame alternative text names the subject followed by `photographed by` with the photographer `src: Core features rule 23`
- [ ] `C-CF-67` `ui` The grain, the pointer mark, the drawn strokes, the planes stay hidden from assistive technology `src: Core features rule 23`
- [ ] `C-CF-68` `capability` Pressing `View` in the header labels every frame in the column View `src: Core features rule 24`
- [ ] `C-CF-69` `capability` Pressing `View` again turns the frame labels off `src: Core features rule 24`
- [ ] `C-CF-70` `capability` Pressing a frame with the pointer opens its detail `src: Core features rule 24`
- [ ] `C-CF-71` `capability` A focused frame opens on Enter `src: Core features rule 24`
- [ ] `C-CF-72` `contract` The galleries API returns the two galleries in order `src: Core features rule 25`
- [ ] `C-CF-73` `contract` Each gallery row carries `id`, `slug`, `title`, `wordmarkFace`, `ground`, `mastheadColour`, `order` `src: Core features rule 25`
- [ ] `C-CF-74` `contract` The single gallery response carries `introduction` with `heading`, `manifesto`, `photographer` `src: Core features rule 25`
- [ ] `C-CF-75` `contract` An unknown gallery slug answers not-found `src: Core features rule 25`
- [ ] `C-CF-76` `contract` The frame API returns `id`, `galleryId`, `subject`, `photographer`, `publication`, `year`, `aspect`, `crop`, `order` `src: Core features rule 25`
- [ ] `C-CF-77` `contract` An unknown frame id answers not-found `src: Core features rule 25`
- [ ] `C-CF-78` `capability` Opening a frame shows the caption subject, photographer, publication, year `src: Core features rule 26`
- [ ] `C-CF-79` `ui` An open frame sits over a dimmed, grain-covered ground `src: Core features rule 26`
- [ ] `C-CF-80` `ui` An open frame shows large, centred in the window `src: Core features rule 26`
- [ ] `C-CF-81` `capability` The right arrow key moves the detail to the next frame `src: Core features rule 27`
- [ ] `C-CF-82` `capability` `Previous` moves the detail back to the previous frame `src: Core features rule 27`
- [ ] `C-CF-83` `capability` `Next` moves the detail forward to the next frame `src: Core features rule 27`
- [ ] `C-CF-84` `capability` The left arrow key moves the detail back to the previous frame `src: Core features rule 27`
- [ ] `C-CF-85` `constraint` `Previous` on the first frame of a gallery is unavailable `src: Core features rule 27`
- [ ] `C-CF-86` `constraint` `Next` on the last frame of a gallery is unavailable `src: Core features rule 27`
- [ ] `C-CF-87` `capability` Escape closes the detail at that frame's place in the column `src: Core features rule 28`
- [ ] `C-CF-88` `capability` The `Close` control closes the frame detail `src: Core features rule 28`
- [ ] `C-CF-89` `capability` Closing the detail restores the gallery header `src: Core features rule 28`
- [ ] `C-CF-90` `ui` Keyboard focus stays inside the open frame detail `src: Core features rule 29`
- [ ] `C-CF-91` `ui` Closing the detail returns focus to the opened frame `src: Core features rule 29`
- [ ] `C-CF-92` `capability` `Menu` opens a full-screen overlay `src: Core features rule 31`
- [ ] `C-CF-93` `capability` `Menu` appears on both galleries, both introductions, the visit, privacy, terms pages `src: Core features rule 31`
- [ ] `C-CF-94` `capability` `Menu` appears on the selection page `src: Core features rule 31`
- [ ] `C-CF-95` `capability` Escape closes the menu overlay `src: Core features rule 31`
- [ ] `C-CF-96` `ui` The Menu control becomes a cross labelled `Close` once the overlay opens `src: Core features rule 31`
- [ ] `C-CF-97` `literal` The overlay link `AURA gallery` goes to `/aura` `src: Core features rule 32`
- [ ] `C-CF-98` `literal` The overlay link `AURA introduction` goes to `/aura-intro` `src: Core features rule 32`
- [ ] `C-CF-99` `literal` The overlay link `Gazette gallery` goes to `/gazette` `src: Core features rule 32`
- [ ] `C-CF-100` `literal` The overlay link `Gazette introduction` goes to `/gazette-intro` `src: Core features rule 32`
- [ ] `C-CF-101` `literal` The overlay link `Reserve a visit` goes to `/visit` `src: Core features rule 32`
- [ ] `C-CF-102` `literal` The overlay link `Your selection` goes to `/selection` `src: Core features rule 32`
- [ ] `C-CF-103` `literal` The overlay link `Privacy` goes to `/privacy` `src: Core features rule 32`
- [ ] `C-CF-104` `literal` The overlay link `Terms` goes to `/terms` `src: Core features rule 32`
- [ ] `C-CF-105` `ui` Menu links are set in the display serif at heading scale `src: Core features rule 32`
- [ ] `C-CF-106` `ui` Menu links reveal letter by letter as the overlay opens `src: Core features rule 32`
- [ ] `C-CF-107` `capability` The count beside `Your selection` changes without a reload `src: Core features rule 33`
- [ ] `C-CF-108` `literal` The overlay states `The New Hollywood Photography Exhibition` `src: Core features rule 34`
- [ ] `C-CF-109` `literal` The overlay states the venue `Beacon Tower` `src: Core features rule 34`
- [ ] `C-CF-110` `literal` The overlay states the city `New York City` `src: Core features rule 34`
- [ ] `C-CF-111` `literal` The overlay states the run as the first date, `to`, the last date in `YYYY-MM-DD` `src: Core features rule 34`
- [ ] `C-CF-112` `contract` The exhibition API returns the title, venue, city, run dates `src: Core features rule 34`
- [ ] `C-CF-113` `capability` Signed out, the overlay offers `Sign in` `src: Core features rule 35`
- [ ] `C-CF-114` `literal` The overlay `Sign in` link goes to `/login` `src: Core features rule 35`
- [ ] `C-CF-115` `capability` Signed in, the overlay shows the visitor's display name `src: Core features rule 35`
- [ ] `C-CF-116` `capability` `Sign out` ends the session back on the landing route `src: Core features rule 35`
- [ ] `C-CF-117` `capability` Closing the overlay returns the visitor to the exact scroll position `src: Core features rule 36`
- [ ] `C-CF-118` `capability` `Save to selection` reads `Saved` the moment the control is pressed `src: Core features rule 37`
- [ ] `C-CF-119` `capability` A failed save returns the control to `Save to selection` `src: Core features rule 37`
- [ ] `C-CF-120` `capability` Pressing `Saved` removes the frame from the selection `src: Core features rule 37`
- [ ] `C-CF-121` `capability` Saving a frame signed out opens the login route `src: Core features rule 38`
- [ ] `C-CF-122` `capability` A successful sign in returns the visitor to the gallery `src: Core features rule 38`
- [ ] `C-CF-123` `contract` A selection write with action add saves the frame `src: Core features rule 39`
- [ ] `C-CF-124` `contract` A selection write with action `remove` deletes the saved frame `src: Core features rule 39`
- [ ] `C-CF-125` `contract` A successful selection write carries `ok` true `src: Core features rule 39`
- [ ] `C-CF-126` `contract` A successful selection write returns the whole selection `src: Core features rule 39`
- [ ] `C-CF-127` `contract` The selection in a successful write lists `frameId`, `galleryId`, `savedAt` rows newest first `src: Core features rule 39`
- [ ] `C-CF-128` `data` Adding an already saved frame leaves exactly one selection row `src: Core features rule 40`
- [ ] `C-CF-129` `contract` Removing a frame that is not saved returns success `src: Core features rule 40`
- [ ] `C-CF-130` `contract` A selection write with an unknown `frameId` is rejected `src: Core features rule 41`
- [ ] `C-CF-131` `contract` A selection write naming another gallery for the frame is rejected `src: Core features rule 41`
- [ ] `C-CF-132` `contract` A selection write with an unknown `action` is rejected `src: Core features rule 41`
- [ ] `C-CF-133` `data` A rejected selection write stores no selection row `src: Core features rule 41`
- [ ] `C-CF-134` `contract` A refused selection write carries `ok` false beside a `message` `src: Core features rule 41`
- [ ] `C-CF-135` `contract` The selection list returns saved frames newest first `src: Core features rule 42`
- [ ] `C-CF-136` `contract` Each selection row carries `frameId`, `galleryId`, `savedAt` `src: Core features rule 42`
- [ ] `C-CF-137` `data` The selection survives a new sign in `src: Core features rule 42`
- [ ] `C-CF-138` `ui` The selection page shows saved frames as a grid of tiles `src: Core features rule 43`
- [ ] `C-CF-139` `capability` A selection tile opens that frame's detail `src: Core features rule 43`
- [ ] `C-CF-140` `capability` `Remove` on a selection tile takes the frame out of the grid `src: Core features rule 43`
- [ ] `C-CF-141` `literal` An empty selection page reads `Nothing saved yet` `src: Core features rule 43`
- [ ] `C-CF-142` `capability` The empty selection page links to both galleries `src: Core features rule 43`
- [ ] `C-CF-143` `capability` Opening the selection route signed out lands on the login route `src: Core features rule 43`
- [ ] `C-CF-144` `literal` The exhibition run lasts thirty days `src: Core features rule 44`
- [ ] `C-CF-145` `literal` The run starts the UTC day before the app first started `src: Core features rule 44`
- [ ] `C-CF-146` `literal` Every run day has entry times `10:00`, `12:00`, `14:00`, `16:00`, `18:00` UTC `src: Core features rule 44`
- [ ] `C-CF-147` `literal` Each entry time holds `8` places `src: Core features rule 44`
- [ ] `C-CF-148` `contract` The slots API lists entry times earliest first `src: Core features rule 45`
- [ ] `C-CF-149` `contract` Each slot row carries `id`, `startsAt`, `capacity`, `placesLeft`, `status` `src: Core features rule 45`
- [ ] `C-CF-150` `literal` An entry time not yet started with a place left reads status `open` `src: Core features rule 45`
- [ ] `C-CF-151` `data` `placesLeft` equals capacity minus confirmed party sizes `src: Core features rule 45`
- [ ] `C-CF-152` `literal` A started entry time reads status `past` `src: Core features rule 45`
- [ ] `C-CF-153` `literal` An entry time with no place left reads status `full` `src: Core features rule 45`
- [ ] `C-CF-154` `ui` The visit route shows the entry times as a calendar grid of run days by entry times `src: Core features rule 46`
- [ ] `C-CF-155` `ui` Each grid cell shows its time with the places left, `Full` or `Past` `src: Core features rule 46`
- [ ] `C-CF-156` `literal` An open cell with several places reads from `8 places left` down to `2 places left` `src: Core features rule 46`
- [ ] `C-CF-157` `literal` An open cell with one place reads `1 place left` `src: Core features rule 46`
- [ ] `C-CF-158` `literal` Grid cells carry `data-slot-id` set to the entry time id `src: Core features rule 46`
- [ ] `C-CF-159` `literal` Grid cells carry `data-slot-state` set to `open`, `full` or `past` `src: Core features rule 46`
- [ ] `C-CF-160` `constraint` A Full cell cannot be chosen `src: Core features rule 46`
- [ ] `C-CF-161` `constraint` A Past cell cannot be chosen `src: Core features rule 46`
- [ ] `C-CF-162` `capability` Choosing an open cell signed out lands on the login route `src: Core features rule 47`
- [ ] `C-CF-163` `capability` A sign in from a chosen cell returns to the visit route `src: Core features rule 47`
- [ ] `C-CF-164` `ui` The reservation modal prefills Name with the display name `src: Core features rule 47`
- [ ] `C-CF-165` `ui` The reservation modal prefills Email with the account email `src: Core features rule 47`
- [ ] `C-CF-166` `literal` The reservation modal carries a field labelled `Party size` `src: Core features rule 47`
- [ ] `C-CF-167` `literal` The reservation modal submit reads `Reserve a visit` `src: Core features rule 47`
- [ ] `C-CF-168` `ui` The reservation modal shows the chosen date with the chosen time `src: Core features rule 47`
- [ ] `C-CF-169` `capability` Escape closes the reservation modal `src: Core features rule 47`
- [ ] `C-CF-170` `ui` The submit reads `Reserving` during the reservation write `src: Core features rule 48`
- [ ] `C-CF-171` `ui` The submit cannot be pressed again during the reservation write `src: Core features rule 48`
- [ ] `C-CF-172` `ui` A confirmed reservation shows an inline banner carrying the code `src: Core features rule 48`
- [ ] `C-CF-173` `literal` The confirmation banner reads `Reserved` beside the date with the time `src: Core features rule 48`
- [ ] `C-CF-174` `capability` The reservation modal closes on success `src: Core features rule 48`
- [ ] `C-CF-175` `ui` The confirmation banner appears at the top of the grid `src: Core features rule 48`
- [ ] `C-CF-176` `capability` The chosen cell's places left update without a reload `src: Core features rule 48`
- [ ] `C-CF-177` `contract` A reservation request confirms with an id, a slotId, a code `src: Core features rule 49`
- [ ] `C-CF-178` `data` A confirmed reservation row is stored with status `confirmed` `src: Core features rule 49`
- [ ] `C-CF-179` `literal` The reservation code is 8 capital letters or digits `src: Core features rule 49`
- [ ] `C-CF-180` `data` Reservation codes are unique across reservations `src: Core features rule 49`
- [ ] `C-CF-181` `data` Two simultaneous requests for the last place confirm exactly one reservation `src: Core features rule 50`
- [ ] `C-CF-182` `data` Booked places for an entry time never exceed its capacity of 8 `src: Core features rule 50`
- [ ] `C-CF-183` `contract` The losing request is rejected naming `slotId` `src: Core features rule 50`
- [ ] `C-CF-184` `contract` A party larger than the places left on an entry time with a place remaining is rejected naming `partySize` `src: Core features rule 51`
- [ ] `C-CF-185` `contract` A party size below 1 or above 4 is rejected naming `partySize` `src: Core features rule 51`
- [ ] `C-CF-186` `contract` A party size that is not a whole number is rejected naming `partySize` `src: Core features rule 51`
- [ ] `C-CF-187` `contract` A request for an entry time with no place left is refused naming `slotId` `src: Core features rule 51`
- [ ] `C-CF-188` `contract` A reservation for a past entry time is rejected naming `slotId` `src: Core features rule 52`
- [ ] `C-CF-189` `contract` A reservation for a full entry time is rejected naming `slotId` `src: Core features rule 52`
- [ ] `C-CF-190` `contract` A second reservation by one visitor for one entry time is rejected naming `slotId` even with places remaining `src: Core features rule 53`
- [ ] `C-CF-191` `contract` A reservation missing the name is rejected naming `name` `src: Core features rule 54`
- [ ] `C-CF-192` `contract` A reservation name longer than 80 characters is rejected naming `name` `src: Core features rule 54`
- [ ] `C-CF-193` `contract` A reservation with a malformed email is rejected naming `email` `src: Core features rule 54`
- [ ] `C-CF-194` `ui` The modal shows a refusal beside the named field `src: Core features rule 54`
- [ ] `C-CF-195` `ui` The modal keeps the entered values after a refusal `src: Core features rule 54`
- [ ] `C-CF-196` `data` A rejected reservation writes no reservation row `src: Core features rule 54`
- [ ] `C-CF-197` `contract` A refused reservation write carries `ok` false with `field` beside `message` `src: Core features rule 54`
- [ ] `C-CF-198` `contract` A reservation breaking several rules names the first failing field in the order `name`, `email`, `partySize`, `slotId` `src: Core features rule 54`
- [ ] `C-CF-199` `contract` A reservation request with no valid token is denied `src: Core features rule 55`
- [ ] `C-CF-200` `capability` A confirmed reservation sends one confirmation email to the reservation address `src: Core features rule 56`
- [ ] `C-CF-201` `constraint` The confirmation email carries no cc or bcc `src: Core features rule 56`
- [ ] `C-CF-202` `literal` The confirmation subject begins `Visit reserved:` followed by the code `src: Core features rule 56`
- [ ] `C-CF-203` `literal` The confirmation body names `Beacon Tower` `src: Core features rule 56`
- [ ] `C-CF-204` `literal` The confirmation body carries the entry date written `YYYY-MM-DD` `src: Core features rule 56`
- [ ] `C-CF-205` `literal` The confirmation body carries the entry time written `HH:MM UTC` `src: Core features rule 56`
- [ ] `C-CF-206` `capability` The confirmation body carries the party size `src: Core features rule 56`
- [ ] `C-CF-207` `capability` The confirmation body carries the reservation code `src: Core features rule 56`
- [ ] `C-CF-208` `constraint` A rejected reservation sends no email `src: Core features rule 56`
- [ ] `C-CF-209` `constraint` Cancelling a reservation sends no email `src: Core features rule 56`
- [ ] `C-CF-210` `constraint` Signing up or saving a frame sends no email `src: Core features rule 56`
- [ ] `C-CF-211` `contract` The reservation list returns the caller's reservations earliest entry first `src: Core features rule 57`
- [ ] `C-CF-212` `contract` Each reservation row carries `id`, `slotId`, `code`, `status`, `name`, `email`, `partySize`, `startsAt` `src: Core features rule 57`
- [ ] `C-CF-213` `contract` The reservation list includes cancelled reservations `src: Core features rule 57`
- [ ] `C-CF-214` `ui` Your visits lists each reservation code with the date, time, party size, status `src: Core features rule 58`
- [ ] `C-CF-215` `literal` An empty Your visits reads `No visits reserved yet` `src: Core features rule 58`
- [ ] `C-CF-216` `capability` `Cancel visit` asks for confirmation before cancelling `src: Core features rule 59`
- [ ] `C-CF-217` `capability` A confirmed visit whose entry time has started shows no `Cancel visit` control `src: Core features rule 59`
- [ ] `C-CF-218` `literal` The cancel confirmation asks the pinned cancel question `src: Core features rule 59`
- [ ] `C-CF-219` `literal` The cancel confirmation offers `Yes, cancel` `src: Core features rule 59`
- [ ] `C-CF-220` `literal` The cancel confirmation offers the pinned keep choice `src: Core features rule 59`
- [ ] `C-CF-221` `contract` Cancelling a reservation returns status `cancelled` `src: Core features rule 59`
- [ ] `C-CF-222` `contract` The cancel response carries `id`, `slotId`, `code`, `status` `src: Core features rule 59`
- [ ] `C-CF-223` `data` Cancelling a reservation returns its places to the entry time at once `src: Core features rule 59`
- [ ] `C-CF-224` `contract` Cancelling an already cancelled reservation is rejected `src: Core features rule 60`
- [ ] `C-CF-225` `contract` Cancelling a reservation whose entry time has started is rejected with the reservation staying confirmed `src: Core features rule 60`
- [ ] `C-CF-226` `contract` Cancelling an id that matches no reservation answers not-found `src: Core features rule 60`
- [ ] `C-CF-227` `contract` An unknown path answers not-found with the not-found document `src: Core features rule 61`
- [ ] `C-CF-228` `literal` The not-found document shows `404` `src: Core features rule 62`
- [ ] `C-CF-229` `literal` The not-found document shows `Page Not Found` `src: Core features rule 62`
- [ ] `C-CF-230` `literal` The not-found document shows `You may have made a mistake.` `src: Core features rule 62`
- [ ] `C-CF-231` `literal` The not-found document shows the pinned second apology line `src: Core features rule 62`
- [ ] `C-CF-232` `ui` The not-found copy shows centred in the window `src: Core features rule 62`
- [ ] `C-CF-233` `capability` `Back to Homepage` on the not-found document returns to the landing route `src: Core features rule 62`
- [ ] `C-CF-234` `ui` The letters of `Back to Homepage` reveal one at a time `src: Core features rule 62`
- [ ] `C-CF-235` `constraint` The not-found document carries no header `src: Core features rule 62`
- [ ] `C-CF-236` `constraint` The not-found document carries no gallery body `src: Core features rule 62`
- [ ] `C-CF-237` `capability` The privacy page names the email address as kept `src: Core features rule 63`
- [ ] `C-CF-238` `capability` The privacy page names the display name as kept `src: Core features rule 63`
- [ ] `C-CF-239` `capability` The privacy page names the saved frames as kept `src: Core features rule 63`
- [ ] `C-CF-240` `capability` The privacy page names the reservations as kept `src: Core features rule 63`
- [ ] `C-CF-241` `capability` The privacy page says mail is sent only to confirm a reservation `src: Core features rule 63`
- [ ] `C-CF-242` `capability` The privacy page says the site runs no analytics `src: Core features rule 63`
- [ ] `C-CF-243` `capability` The terms page states one reservation per visitor per entry time `src: Core features rule 64`
- [ ] `C-CF-244` `capability` The terms page states a party of up to four `src: Core features rule 64`
- [ ] `C-CF-245` `capability` The terms page states arrival within the hour that begins at the reserved entry time `src: Core features rule 64`
- [ ] `C-CF-246` `capability` The terms page states that a cancelled visit returns its places `src: Core features rule 64`
- [ ] `C-CF-247` `capability` The signup form links to the terms page `src: Core features rule 64`
- [ ] `C-CF-248` `capability` The signup form links to the privacy page `src: Core features rule 63`
- [ ] `C-CF-249` `literal` The signup form reads `By creating an account you accept the Terms` `src: Core features rule 64`
- [ ] `C-CF-250` `capability` The signup form rejects invalid input inline naming the field `src: Core features rule 65`
- [ ] `C-CF-251` `capability` The sign-in form rejects invalid input inline naming the field `src: Core features rule 65`
- [ ] `C-CF-252` `capability` The sign-in form keeps what was typed after a refusal `src: Core features rule 65`
- [ ] `C-CF-253` `capability` The signup form keeps what was typed after a refusal `src: Core features rule 65`
- [ ] `C-CF-254` `literal` The sound control starts at `Sound: off` `src: Core features rule 66`
- [ ] `C-CF-255` `capability` Pressing the sound control changes the label to `Sound: on` `src: Core features rule 66`
- [ ] `C-CF-256` `capability` Pressing the sound control again returns the label to `Sound: off` `src: Core features rule 66`
- [ ] `C-CF-257` `capability` The sound control sits in the header of every route with a header `src: Core features rule 66`
- [ ] `C-CF-258` `capability` The sound control sits in the menu overlay `src: Core features rule 66`
- [ ] `C-CF-259` `constraint` No sound plays before a gesture `src: Core features rule 66`

## C-UF User flow

- [ ] `C-UF-01` `contract` Every route in the route table answers for a signed-out visitor `src: User flow route table`
- [ ] `C-UF-02` `capability` A successful signup lands on the landing route `src: User flow entry and redirects`
- [ ] `C-UF-03` `capability` Signing in from the selection redirect returns to the selection route `src: User flow entry and redirects`
- [ ] `C-UF-04` `ui` Every page shows the turning ring during data loading `src: User flow states`
- [ ] `C-UF-05` `capability` An error appears as a message in place `src: User flow states`
- [ ] `C-UF-06` `constraint` No page shows a raw error `src: User flow states`

## C-UX UI/UX notes

- [ ] `C-UX-01` `ui` The landing ground is a near-black neutral `src: UI/UX notes palette paragraph`
- [ ] `C-UX-02` `ui` The visit, selection, sign-in, signup pages sit on the deep neutral ground `src: UI/UX notes mode paragraph`
- [ ] `C-UX-03` `ui` The introductions, privacy, terms pages sit on the deep neutral ground `src: UI/UX notes mode paragraph`
- [ ] `C-UX-04` `ui` The not-found page sits on the near-black ground `src: UI/UX notes mode paragraph`
- [ ] `C-UX-05` `constraint` The product offers no alternate colour scheme `src: UI/UX notes mode paragraph`
- [ ] `C-UX-06` `literal` The script connector names `Pinyon Script` first `src: UI/UX notes typography paragraph`
- [ ] `C-UX-07` `literal` The Gazette wordmark names `Playfair Display` in italic first `src: UI/UX notes typography paragraph`
- [ ] `C-UX-08` `ui` Hot pink appears only on the Gazette masthead with the interactive highlight `src: UI/UX notes colour paragraph`
- [ ] `C-UX-09` `ui` Unavailable states are said in words rather than by colour alone `src: UI/UX notes components paragraph`
- [ ] `C-UX-10` `ui` Wordmarks sit in a thin high-contrast serif at its thinnest cut `src: UI/UX notes typography paragraph`
- [ ] `C-UX-11` `literal` Display type names `Bodoni Moda` first with `Didot`, `Times New Roman`, serif behind `src: UI/UX notes typography paragraph`
- [ ] `C-UX-12` `literal` The manifesto names `Bodoni Moda` first `src: UI/UX notes typography paragraph`
- [ ] `C-UX-13` `constraint` The manifesto is set as thin as the AURA wordmark, at the serif's thinnest cut `src: UI/UX notes typography paragraph`
- [ ] `C-UX-14` `literal` The chooser prompt names `Inter` first, set light at `300` `src: UI/UX notes typography paragraph`
- [ ] `C-UX-15` `literal` The not-found apology lines name `Inter` first, set light at `300` `src: UI/UX notes typography paragraph`
- [ ] `C-UX-16` `literal` Interface controls name `Inter` light at 300 `src: UI/UX notes typography paragraph`
- [ ] `C-UX-17` `literal` Body copy grows from `16px` at 375 wide or narrower to `20px` at 1920 wide or wider `src: UI/UX notes typography paragraph`
- [ ] `C-UX-18` `literal` Form field labels grow from `12px` to `14px` `src: UI/UX notes typography paragraph`
- [ ] `C-UX-19` `literal` Calls to action such as `Go to Gallery` grow from `14px` to `16px` `src: UI/UX notes typography paragraph`
- [ ] `C-UX-20` `literal` The `Your visits` heading grows from `20px` to `30px` `src: UI/UX notes typography paragraph`
- [ ] `C-UX-21` `literal` Menu overlay links grow from `36px` to `54px` `src: UI/UX notes typography paragraph`
- [ ] `C-UX-22` `literal` `Page Not Found` grows from `35px` to `60px` `src: UI/UX notes typography paragraph`
- [ ] `C-UX-23` `literal` The chooser prompt grows from `30px` to `40px` `src: UI/UX notes typography paragraph`
- [ ] `C-UX-24` `literal` The introduction heading grows from `50px` to `100px` `src: UI/UX notes typography paragraph`
- [ ] `C-UX-25` `constraint` Type never steps at a breakpoint `src: UI/UX notes typography paragraph`
- [ ] `C-UX-26` `literal` The micro interface face is `Inter` at 400 or 500 `src: UI/UX notes typography paragraph`
- [ ] `C-UX-27` `literal` Wordmarks grow from `50px` at 375 wide or narrower to `100px` at 1920 wide or wider `src: UI/UX notes typography paragraph`
- [ ] `C-UX-28` `constraint` Places left in the calendar grid use tabular numerals `src: UI/UX notes typography paragraph`
- [ ] `C-UX-29` `constraint` Reservation dates, times, codes under `Your visits` use tabular numerals `src: UI/UX notes typography paragraph`
- [ ] `C-UX-30` `ui` Only two corner treatments appear, soft on filled buttons, fully round on pointer dots `src: UI/UX notes shape paragraph`
- [ ] `C-UX-31` `ui` Tone changes on controls glide slowly with colour, background, border moving together `src: UI/UX notes motion paragraph`
- [ ] `C-UX-32` `ui` Under a reduced-motion preference letter reveals become a plain fade `src: UI/UX notes motion paragraph`
- [ ] `C-UX-33` `constraint` Under a reduced-motion preference the page text keeps its content in the same order `src: UI/UX notes motion paragraph`
- [ ] `C-UX-34` `ui` Under a reduced-motion preference photographs present already clear `src: UI/UX notes motion paragraph`
- [ ] `C-UX-35` `ui` Under a reduced-motion preference drawn strokes present fully drawn `src: UI/UX notes motion paragraph`
- [ ] `C-UX-36` `capability` Under a reduced-motion preference the landing presents the two covers settled `src: UI/UX notes motion paragraph`
- [ ] `C-UX-37` `ui` Body text meets WCAG AA contrast against its ground `src: UI/UX notes accessibility paragraph`
- [ ] `C-UX-38` `ui` Copy laid over a photograph sits on a translucent scrim `src: UI/UX notes accessibility paragraph`
- [ ] `C-UX-39` `literal` The frame detail `Close`, `Previous`, `Next` controls carry text labels `src: UI/UX notes components paragraph`
- [ ] `C-UX-40` `literal` Touch targets measure at least `44` by `44` `src: UI/UX notes accessibility paragraph`
- [ ] `C-UX-41` `ui` Every listed control works by keyboard in a logical order `src: UI/UX notes accessibility paragraph`
- [ ] `C-UX-42` `ui` A visible focus ring shows on the near-black ground `src: UI/UX notes accessibility paragraph`
- [ ] `C-UX-43` `ui` The page is weighted toward grey, white kept as the exception `src: UI/UX notes palette paragraph`
- [ ] `C-UX-44` `ui` Interface copy on dark grounds is white `src: UI/UX notes palette paragraph`
- [ ] `C-UX-45` `ui` Body copy on dark grounds is a mid neutral grey `src: UI/UX notes palette paragraph`
- [ ] `C-UX-46` `ui` Captions, fine rules are a darker mid neutral grey `src: UI/UX notes palette paragraph`
- [ ] `C-UX-47` `ui` Panel, filled control surfaces are a deep neutral `src: UI/UX notes palette paragraph`
- [ ] `C-UX-48` `ui` Pointing at a control lifts its tone toward a light neutral grey `src: UI/UX notes palette paragraph`
- [ ] `C-UX-49` `ui` The run dates in the menu overlay are a blue-leaning slate grey `src: UI/UX notes palette paragraph`
- [ ] `C-UX-50` `ui` Interface copy on the pale Gazette room rests in a deep neutral ink `src: UI/UX notes palette paragraph`
- [ ] `C-UX-51` `ui` Dividers on the pale ground are near-white `src: UI/UX notes palette paragraph`
- [ ] `C-UX-52` `ui` Hot pink highlights the control the visitor is about to use `src: UI/UX notes colour paragraph`
- [ ] `C-UX-53` `ui` Refusal, sending, success on the visit page each pair words with a small drawn mark `src: UI/UX notes colour paragraph`
- [ ] `C-UX-54` `ui` Small state changes use a quick transition rather than the slow glide `src: UI/UX notes motion paragraph`
- [ ] `C-UX-55` `ui` Filled buttons show a pressed state `src: UI/UX notes components paragraph`
- [ ] `C-UX-56` `ui` A visible focus ring shows on the pale Gazette ground `src: UI/UX notes accessibility paragraph`
- [ ] `C-UX-57` `ui` On a device without hover the pointer mark is absent `src: UI/UX notes responsive paragraph`
- [ ] `C-UX-58` `capability` On a device without hover the landing presents settled on the two covers `src: UI/UX notes responsive paragraph`
- [ ] `C-UX-59` `ui` On a device without hover a tap opens a frame `src: UI/UX notes responsive paragraph`
- [ ] `C-UX-60` `constraint` At a narrow viewport nothing scrolls sideways `src: UI/UX notes responsive paragraph`
- [ ] `C-UX-61` `ui` At a narrow viewport the gallery stays a single full-bleed column `src: UI/UX notes responsive paragraph`
- [ ] `C-UX-62` `ui` At a narrow viewport the gallery header keeps `Menu` beside a compact `View` `src: UI/UX notes responsive paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `literal` The root element gains `is-fonts-ready` once fonts resolve `src: Front-end specification root state`
- [ ] `C-FE-02` `literal` The root element gains `has-scrolled` after the first scroll `src: Front-end specification root state`
- [ ] `C-FE-03` `ui` The pointer mark stays visible above an open frame detail `src: Front-end specification layering`
- [ ] `C-FE-04` `ui` The pointer mark stays visible above the open menu overlay `src: Front-end specification layering`
- [ ] `C-FE-05` `ui` The gallery header sits above the column of photographs `src: Front-end specification layering`
- [ ] `C-FE-06` `ui` Decorative ground layers sit beneath the page content `src: Front-end specification layering`
- [ ] `C-FE-07` `ui` The pointer dot inverts the tone beneath the pointer `src: Front-end specification pointer mark`
- [ ] `C-FE-08` `ui` A larger soft halo trails the pointer dot a beat behind `src: Front-end specification pointer mark`
- [ ] `C-FE-09` `ui` Over an open-able frame the pointer grows into a `View` badge `src: Front-end specification pointer mark`
- [ ] `C-FE-10` `ui` Over a chooser cover the pointer grows into a `View` badge `src: Front-end specification pointer mark`
- [ ] `C-FE-11` `ui` Over a save control the pointer becomes a plus mark `src: Front-end specification pointer mark`
- [ ] `C-FE-12` `constraint` The pointer mark never intercepts pointer events `src: Front-end specification pointer mark`
- [ ] `C-FE-13` `ui` Wheel input eases into one continuous gliding scroll `src: Front-end specification scroll system`
- [ ] `C-FE-14` `capability` Under a reduced-motion preference the page scrolls natively `src: Front-end specification scroll system`
- [ ] `C-FE-15` `capability` Keyboard scrolling with the arrow keys, Page Down, the space bar still moves the page `src: Front-end specification scroll system`
- [ ] `C-FE-16` `ui` The chooser prompt resolves out of a blur as the covers settle `src: Front-end specification title sequence`
- [ ] `C-FE-17` `ui` Each photograph rises into focus out of a blurred stand-in of the same shape `src: Front-end specification photographs`
- [ ] `C-FE-18` `ui` Each generated photograph shows a grey gradient with a soft centred mass `src: Front-end specification photographs`
- [ ] `C-FE-19` `literal` Frame crops are drawn from `240x320`, `320x240`, `280x320`, `320x200`, `200x320`, `320x160` `src: Front-end specification photographs`
- [ ] `C-FE-20` `ui` A fine film grain shivers over every route `src: Front-end specification film grain`
- [ ] `C-FE-21` `constraint` The grain layer never intercepts pointer events `src: Front-end specification film grain`
- [ ] `C-FE-22` `ui` The grain drifts slightly with scroll `src: Front-end specification film grain`
- [ ] `C-FE-23` `ui` The grain textures the dark grounds more strongly than the pale gallery `src: Front-end specification film grain`
- [ ] `C-FE-24` `literal` The tab icon is an inline vector data address beginning `data:image/svg+xml` `src: Front-end specification drawn marks`
- [ ] `C-FE-25` `ui` The close control is drawn as a thin two-stroke cross `src: Front-end specification drawn marks`
- [ ] `C-FE-26` `ui` Loose hand-drawn strokes draw themselves on under words in the display headings `src: Front-end specification drawn marks`
- [ ] `C-FE-27` `ui` The ring is nudged aside across the first moments of scrolling `src: Front-end specification title sequence`
- [ ] `C-FE-28` `constraint` The title sequence exists only on the landing route `src: Front-end specification title sequence`
- [ ] `C-FE-29` `ui` The introduction heading reveals one character at a time `src: Front-end specification character reveal`
- [ ] `C-FE-30` `ui` The character reveal ramps smoothly across neighbouring characters rather than in discrete steps `src: Front-end specification character reveal`
- [ ] `C-FE-31` `ui` Every hover affordance has a tap equivalent `src: Front-end specification touch`
- [ ] `C-FE-32` `ui` A revealed phrase stays one readable node for assistive technology `src: Front-end specification character reveal`
- [ ] `C-FE-33` `ui` Scrolling stays smooth with every effect running `src: Front-end specification performance`
- [ ] `C-FE-34` `ui` The page copy is readable before the loader ring stops turning `src: Front-end specification performance`
- [ ] `C-FE-35` `capability` Under a reduced-motion preference no looping animation keeps running `src: Front-end specification performance`

## C-TR Technical requirements

- [ ] `C-TR-01` `capability` Every route arrives server-rendered with its copy in the first HTML response `src: Technical requirements rendering model`
- [ ] `C-TR-02` `capability` Seeded rows live in the PostgreSQL database at `DATABASE_URL` `src: Technical requirements database`
- [ ] `C-TR-03` `capability` Confirmation mail leaves over SMTP into Mailpit `src: Technical requirements email`
- [ ] `C-TR-04` `contract` The health route answers with status ok without a token `src: Technical requirements health`
- [ ] `C-TR-05` `constraint` No image, font, audio or video file loads on any route `src: Technical requirements asset paragraph`
- [ ] `C-TR-06` `constraint` No browser request leaves the app origin at run time `src: Technical requirements asset paragraph`
- [ ] `C-TR-07` `constraint` Nothing the browser downloads carries a credential `src: Technical requirements secrets paragraph`
- [ ] `C-TR-08` `ui` Go to Gallery, Reserve a visit, the save control share one soft-cornered filled button look `src: Technical requirements shared piece paragraph`
- [ ] `C-TR-09` `ui` Every frame, cover, plane arrives with the same blurred rise `src: Technical requirements shared piece paragraph`

## C-DM Data model

- [ ] `C-DM-01` `data` The database holds the eight named tables `src: Data model opening`
- [ ] `C-DM-02` `data` Identifiers are integers `src: Data model opening`
- [ ] `C-DM-03` `data` The seed holds exactly twelve frames `src: Data model frames`
- [ ] `C-DM-04` `data` `exhibitions` holds exactly one row `src: Data model exhibitions`
- [ ] `C-DM-05` `data` The aura gallery row carries serif, dark, white, order 1 `src: Data model galleries`
- [ ] `C-DM-06` `data` The gazette gallery row carries swash, pale, pink, order 2 `src: Data model galleries`
- [ ] `C-DM-07` `data` The AURA introduction credits `Celine Armand` `src: Data model seed data`
- [ ] `C-DM-08` `data` The Gazette introduction credits `Tomas Ekwueme` `src: Data model seed data`
- [ ] `C-DM-09` `literal` Each introduction heading reads `THE NEW HOLLYWOOD` `src: Data model introductions`
- [ ] `C-DM-10` `data` The twelve seeded frames match the pinned frame table `src: Data model seed data`
- [ ] `C-DM-11` `data` Each frame publication equals its gallery title `src: Data model frames`
- [ ] `C-DM-12` `data` Slot rows store no places left or status column `src: Data model slots`
- [ ] `C-DM-13` `data` `visitor@example.com` holds a seeded selection of `Odessa Vane` `src: Data model seed data`
- [ ] `C-DM-14` `data` `visitor@example.com` holds a seeded selection of `Rafe Okonkwo` `src: Data model seed data`
- [ ] `C-DM-15` `data` `visitor2@example.com` holds a seeded selection of `Lilou Marchetti` `src: Data model seed data`
- [ ] `C-DM-16` `data` `visitor@example.com` saved `Odessa Vane` before `Rafe Okonkwo`, so `Rafe Okonkwo` lists first `src: Data model seed data`
- [ ] `C-DM-17` `data` `SEEDA14B` holds tomorrow 14:00 for `visitor2@example.com` as `Omar Lindgren`, a party of 4 `src: Data model seed data`
- [ ] `C-DM-18` `data` `SEEDC14D` holds tomorrow 14:00 for `visitor3@example.com` as `Hana Petrov`, a party of 3 `src: Data model seed data`
- [ ] `C-DM-19` `data` `SEEDE16F` holds tomorrow 16:00 for `visitor2@example.com` as `Omar Lindgren`, a party of 4 `src: Data model seed data`
- [ ] `C-DM-20` `data` `SEEDG16H` holds tomorrow 16:00 for `visitor3@example.com` as `Hana Petrov`, a party of 4 `src: Data model seed data`
- [ ] `C-DM-21` `data` `SEEDP10Q` holds the first run day 10:00 for `visitor3@example.com` as `Hana Petrov`, a party of 2 `src: Data model seed data`
- [ ] `C-DM-22` `data` Seeded rows appear exactly once `src: Data model seed data`
- [ ] `C-DM-23` `data` Two simultaneous saves of one frame by one visitor leave one selection row `src: Data model selections`
- [ ] `C-DM-24` `data` Entry times are stored in UTC `src: Data model opening`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The site holds one exhibition with two galleries `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The exhibition site shows no price or payment step `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` An administrator address answers not-found `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` The site offers no editing of galleries, frames, introductions, entry times or capacities `src: Constraints bullet 3`
- [ ] `C-CN-05` `constraint` The site offers no upload control `src: Constraints bullet 4`
- [ ] `C-CN-06` `constraint` The site offers no comment, like, share, feed or messaging control `src: Constraints bullet 5`
- [ ] `C-CN-07` `constraint` The sign-in form offers no password reset or third-party sign-in `src: Constraints bullet 6`
- [ ] `C-CN-08` `constraint` The site makes no analytics or external network call at run time `src: Constraints bullet 7`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` `startsAt` with `savedAt` are written ISO 8601 UTC `src: Deployment contract API shapes`
- [ ] `C-DC-02` `contract` `runStart` with `runEnd` are written `YYYY-MM-DD` `src: Deployment contract API shapes`
- [ ] `C-DC-03` `contract` The app answers at the public url environment variable `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The container-internal port is `4173` `src: Deployment contract bullet 1`
- [ ] `C-DC-05` `contract` The backend serves JSON under the `/api` prefix `src: Deployment contract bullet 2`
- [ ] `C-DC-06` `contract` `GET /api/health` returns `200` `src: Deployment contract bullet 3`
- [ ] `C-DC-07` `contract` A production build is served rather than a development debug page `src: Deployment contract bullet 7`
- [ ] `C-DC-08` `contract` The server outlives the session that started the process `src: Deployment contract bullet 8`
- [ ] `C-DC-09` `contract` The server binds every interface rather than loopback `src: Deployment contract bullet 9`
- [ ] `C-DC-10` `constraint` Backing services are reached rather than started `src: Deployment contract bullet 10`
- [ ] `C-DC-11` `contract` Every list endpoint returns a top-level JSON array `src: Deployment contract API shapes`
- [ ] `C-DC-12` `contract` Health, signup, login, exhibition, galleries, frames, slots answer without a token `src: Deployment contract API shapes`
- [ ] `C-DC-13` `contract` An unauthorized call is rejected as a client error `src: Deployment contract API shapes`
- [ ] `C-DC-14` `constraint` Places left come from confirmed reservation rows rather than a stored counter `src: Deployment contract no mocks`
- [ ] `C-DC-15` `contract` `GET /api/galleries/{slug}` returns `id`, `slug`, `title`, `wordmarkFace`, `ground`, `mastheadColour`, `order`, `introduction`, `frames` `src: Deployment contract API shapes`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | Every seeded visitor signs in with deku-demo-pw-2026 | C-RL-13 | User roles signup paragraph |
| `visitor@example.com` | visitor@example.com is seeded with display name Nadia Rowe | C-RL-14 | User roles signup paragraph |
| `Nadia Rowe` | visitor@example.com is seeded with display name Nadia Rowe | C-RL-14 | User roles signup paragraph |
| `visitor2@example.com` | visitor2@example.com is seeded with display name Omar Lindgren | C-RL-15 | User roles signup paragraph |
| `Omar Lindgren` | visitor2@example.com is seeded with display name Omar Lindgren | C-RL-15 | User roles signup paragraph |
| `visitor3@example.com` | visitor3@example.com is seeded with display name Hana Petrov | C-RL-16 | User roles signup paragraph |
| `Hana Petrov` | visitor3@example.com is seeded with display name Hana Petrov | C-RL-16 | User roles signup paragraph |
| `Create account` | The signup form submits with a Create account button | C-CF-19 | Core features rule 8 |
| `Sign in` | The sign-in form submits with a Sign in button | C-CF-20 | Core features rule 8 |
| `Create an account` | The sign-in form links to the signup route with Create an account | C-CF-22 | Core features rule 8 |
| `The New Hollywood Photography Exhibition` | The landing route carries the document title The New Hollywood Phot... | C-CF-23 | Core features rule 9 |
| `THE` | The landing lock-up carries THE, AURA, Gazette, HOLLYWOOD | C-CF-24 | Core features rule 9 |
| `AURA` | The landing lock-up carries THE, AURA, Gazette, HOLLYWOOD | C-CF-24 | Core features rule 9 |
| `Gazette` | The landing lock-up carries THE, AURA, Gazette, HOLLYWOOD | C-CF-24 | Core features rule 9 |
| `HOLLYWOOD` | The landing lock-up carries THE, AURA, Gazette, HOLLYWOOD | C-CF-24 | Core features rule 9 |
| `As seen in the Beacon Tower, located in` | The landing subtitle reads As seen in the Beacon Tower, located in... | C-CF-27 | Core features rule 10 |
| `New York City` | The landing subtitle reads As seen in the Beacon Tower, located in... | C-CF-27 | Core features rule 10 |
| `Choose which gallery you want to explore` | The chooser prompt reads Choose which gallery you want to explore | C-CF-31 | Core features rule 12 |
| `AURA: The New Hollywood` | The AURA introduction route carries the document title AURA: The Ne... | C-CF-39 | Core features rule 14 |
| `Gazette Goes to Hollywood` | The Gazette introduction route carries the document title Gazette G... | C-CF-40 | Core features rule 14 |
| `Photographs by Celine Armand` | The AURA introduction credit reads Photographs by Celine Armand the... | C-CF-46 | Core features rule 17 |
| `for AURA` | The AURA introduction credit reads Photographs by Celine Armand the... | C-CF-46 | Core features rule 17 |
| `Photographs by Tomas Ekwueme` | The Gazette introduction credit reads Photographs by Tomas Ekwueme... | C-CF-47 | Core features rule 17 |
| `for Gazette` | The Gazette introduction credit reads Photographs by Tomas Ekwueme... | C-CF-47 | Core features rule 17 |
| `AURA: The New Hollywood` | The AURA gallery route carries the document title AURA: The New Hol... | C-CF-50 | Core features rule 19 |
| `Gazette Goes to Hollywood` | The Gazette gallery route carries the document title Gazette Goes t... | C-CF-51 | Core features rule 19 |
| `Scroll to explore` | Each gallery carries the prompt Scroll to explore shown in capitals | C-CF-55 | Core features rule 20 |
| `photographed by` | Frame alternative text names the subject followed by photographed b... | C-CF-66 | Core features rule 23 |
| `AURA gallery` | The overlay link AURA gallery goes to /aura | C-CF-97 | Core features rule 32 |
| `/aura` | The overlay link AURA gallery goes to /aura | C-CF-97 | Core features rule 32 |
| `AURA introduction` | The overlay link AURA introduction goes to /aura-intro | C-CF-98 | Core features rule 32 |
| `/aura-intro` | The overlay link AURA introduction goes to /aura-intro | C-CF-98 | Core features rule 32 |
| `Gazette gallery` | The overlay link Gazette gallery goes to /gazette | C-CF-99 | Core features rule 32 |
| `/gazette` | The overlay link Gazette gallery goes to /gazette | C-CF-99 | Core features rule 32 |
| `Gazette introduction` | The overlay link Gazette introduction goes to /gazette-intro | C-CF-100 | Core features rule 32 |
| `/gazette-intro` | The overlay link Gazette introduction goes to /gazette-intro | C-CF-100 | Core features rule 32 |
| `Reserve a visit` | The overlay link Reserve a visit goes to /visit | C-CF-101 | Core features rule 32 |
| `/visit` | The overlay link Reserve a visit goes to /visit | C-CF-101 | Core features rule 32 |
| `Your selection` | The overlay link Your selection goes to /selection | C-CF-102 | Core features rule 32 |
| `/selection` | The overlay link Your selection goes to /selection | C-CF-102 | Core features rule 32 |
| `Privacy` | The overlay link Privacy goes to /privacy | C-CF-103 | Core features rule 32 |
| `/privacy` | The overlay link Privacy goes to /privacy | C-CF-103 | Core features rule 32 |
| `Terms` | The overlay link Terms goes to /terms | C-CF-104 | Core features rule 32 |
| `/terms` | The overlay link Terms goes to /terms | C-CF-104 | Core features rule 32 |
| `The New Hollywood Photography Exhibition` | The overlay states The New Hollywood Photography Exhibition | C-CF-108 | Core features rule 34 |
| `Beacon Tower` | The overlay states the venue Beacon Tower | C-CF-109 | Core features rule 34 |
| `New York City` | The overlay states the city New York City | C-CF-110 | Core features rule 34 |
| `to` | The overlay states the run as the first date, to, the last date in... | C-CF-111 | Core features rule 34 |
| `YYYY-MM-DD` | The overlay states the run as the first date, to, the last date in... | C-CF-111 | Core features rule 34 |
| `Sign in` | The overlay Sign in link goes to /login | C-CF-114 | Core features rule 35 |
| `/login` | The overlay Sign in link goes to /login | C-CF-114 | Core features rule 35 |
| `Nothing saved yet` | An empty selection page reads Nothing saved yet | C-CF-141 | Core features rule 43 |
| `10:00` | Every run day has entry times 10:00, 12:00, 14:00, 16:00, 18:00 UTC | C-CF-146 | Core features rule 44 |
| `12:00` | Every run day has entry times 10:00, 12:00, 14:00, 16:00, 18:00 UTC | C-CF-146 | Core features rule 44 |
| `14:00` | Every run day has entry times 10:00, 12:00, 14:00, 16:00, 18:00 UTC | C-CF-146 | Core features rule 44 |
| `16:00` | Every run day has entry times 10:00, 12:00, 14:00, 16:00, 18:00 UTC | C-CF-146 | Core features rule 44 |
| `18:00` | Every run day has entry times 10:00, 12:00, 14:00, 16:00, 18:00 UTC | C-CF-146 | Core features rule 44 |
| `8` | Each entry time holds 8 places | C-CF-147 | Core features rule 44 |
| `open` | An entry time not yet started with a place left reads status open | C-CF-150 | Core features rule 45 |
| `past` | A started entry time reads status past | C-CF-152 | Core features rule 45 |
| `full` | An entry time with no place left reads status full | C-CF-153 | Core features rule 45 |
| `8 places left` | An open cell with several places reads from 8 places left down to 2... | C-CF-156 | Core features rule 46 |
| `2 places left` | An open cell with several places reads from 8 places left down to 2... | C-CF-156 | Core features rule 46 |
| `1 place left` | An open cell with one place reads 1 place left | C-CF-157 | Core features rule 46 |
| `data-slot-id` | Grid cells carry data-slot-id set to the entry time id | C-CF-158 | Core features rule 46 |
| `data-slot-state` | Grid cells carry data-slot-state set to open, full or past | C-CF-159 | Core features rule 46 |
| `open` | Grid cells carry data-slot-state set to open, full or past | C-CF-159 | Core features rule 46 |
| `full` | Grid cells carry data-slot-state set to open, full or past | C-CF-159 | Core features rule 46 |
| `past` | Grid cells carry data-slot-state set to open, full or past | C-CF-159 | Core features rule 46 |
| `Party size` | The reservation modal carries a field labelled Party size | C-CF-166 | Core features rule 47 |
| `Reserve a visit` | The reservation modal submit reads Reserve a visit | C-CF-167 | Core features rule 47 |
| `Reserved` | The confirmation banner reads Reserved beside the date with the time | C-CF-173 | Core features rule 48 |
| `Visit reserved:` | The confirmation subject begins Visit reserved: followed by the code | C-CF-202 | Core features rule 56 |
| `Beacon Tower` | The confirmation body names Beacon Tower | C-CF-203 | Core features rule 56 |
| `YYYY-MM-DD` | The confirmation body carries the entry date written YYYY-MM-DD | C-CF-204 | Core features rule 56 |
| `HH:MM UTC` | The confirmation body carries the entry time written HH:MM UTC | C-CF-205 | Core features rule 56 |
| `No visits reserved yet` | An empty Your visits reads No visits reserved yet | C-CF-215 | Core features rule 58 |
| `Cancel this visit?` | The cancel confirmation asks the pinned cancel question | C-CF-218 | Core features rule 59 |
| `Yes, cancel` | The cancel confirmation offers Yes, cancel | C-CF-219 | Core features rule 59 |
| `Keep it` | The cancel confirmation offers the pinned keep choice | C-CF-220 | Core features rule 59 |
| `404` | The not-found document shows 404 | C-CF-228 | Core features rule 62 |
| `Page Not Found` | The not-found document shows Page Not Found | C-CF-229 | Core features rule 62 |
| `You may have made a mistake.` | The not-found document shows You may have made a mistake. | C-CF-230 | Core features rule 62 |
| `This page does not exist.` | The not-found document shows the pinned second apology line | C-CF-231 | Core features rule 62 |
| `By creating an account you accept the Terms` | The signup form reads By creating an account you accept the Terms | C-CF-249 | Core features rule 64 |
| `Sound: off` | The sound control starts at Sound: off | C-CF-254 | Core features rule 66 |
| `Pinyon Script` | The script connector names Pinyon Script first | C-UX-06 | UI/UX notes typography paragraph |
| `Playfair Display` | The Gazette wordmark names Playfair Display in italic first | C-UX-07 | UI/UX notes typography paragraph |
| `Bodoni Moda` | Display type names Bodoni Moda first with Didot, Times New Roman, s... | C-UX-11 | UI/UX notes typography paragraph |
| `Didot` | Display type names Bodoni Moda first with Didot, Times New Roman, s... | C-UX-11 | UI/UX notes typography paragraph |
| `Times New Roman` | Display type names Bodoni Moda first with Didot, Times New Roman, s... | C-UX-11 | UI/UX notes typography paragraph |
| `Bodoni Moda` | The manifesto names Bodoni Moda first | C-UX-12 | UI/UX notes typography paragraph |
| `Inter` | The chooser prompt names Inter first, set light at 300 | C-UX-14 | UI/UX notes typography paragraph |
| `300` | The chooser prompt names Inter first, set light at 300 | C-UX-14 | UI/UX notes typography paragraph |
| `Inter` | The not-found apology lines name Inter first, set light at 300 | C-UX-15 | UI/UX notes typography paragraph |
| `300` | The not-found apology lines name Inter first, set light at 300 | C-UX-15 | UI/UX notes typography paragraph |
| `Inter` | Interface controls name Inter light at 300 | C-UX-16 | UI/UX notes typography paragraph |
| `16px` | Body copy grows from 16px at 375 wide or narrower to 20px at 1920 w... | C-UX-17 | UI/UX notes typography paragraph |
| `20px` | Body copy grows from 16px at 375 wide or narrower to 20px at 1920 w... | C-UX-17 | UI/UX notes typography paragraph |
| `12px` | Form field labels grow from 12px to 14px | C-UX-18 | UI/UX notes typography paragraph |
| `14px` | Form field labels grow from 12px to 14px | C-UX-18 | UI/UX notes typography paragraph |
| `Go to Gallery` | Calls to action such as Go to Gallery grow from 14px to 16px | C-UX-19 | UI/UX notes typography paragraph |
| `14px` | Calls to action such as Go to Gallery grow from 14px to 16px | C-UX-19 | UI/UX notes typography paragraph |
| `16px` | Calls to action such as Go to Gallery grow from 14px to 16px | C-UX-19 | UI/UX notes typography paragraph |
| `Your visits` | The Your visits heading grows from 20px to 30px | C-UX-20 | UI/UX notes typography paragraph |
| `20px` | The Your visits heading grows from 20px to 30px | C-UX-20 | UI/UX notes typography paragraph |
| `30px` | The Your visits heading grows from 20px to 30px | C-UX-20 | UI/UX notes typography paragraph |
| `36px` | Menu overlay links grow from 36px to 54px | C-UX-21 | UI/UX notes typography paragraph |
| `54px` | Menu overlay links grow from 36px to 54px | C-UX-21 | UI/UX notes typography paragraph |
| `Page Not Found` | Page Not Found grows from 35px to 60px | C-UX-22 | UI/UX notes typography paragraph |
| `35px` | Page Not Found grows from 35px to 60px | C-UX-22 | UI/UX notes typography paragraph |
| `60px` | Page Not Found grows from 35px to 60px | C-UX-22 | UI/UX notes typography paragraph |
| `30px` | The chooser prompt grows from 30px to 40px | C-UX-23 | UI/UX notes typography paragraph |
| `40px` | The chooser prompt grows from 30px to 40px | C-UX-23 | UI/UX notes typography paragraph |
| `50px` | The introduction heading grows from 50px to 100px | C-UX-24 | UI/UX notes typography paragraph |
| `100px` | The introduction heading grows from 50px to 100px | C-UX-24 | UI/UX notes typography paragraph |
| `Inter` | The micro interface face is Inter at 400 or 500 | C-UX-26 | UI/UX notes typography paragraph |
| `50px` | Wordmarks grow from 50px at 375 wide or narrower to 100px at 1920 w... | C-UX-27 | UI/UX notes typography paragraph |
| `100px` | Wordmarks grow from 50px at 375 wide or narrower to 100px at 1920 w... | C-UX-27 | UI/UX notes typography paragraph |
| `Close` | The frame detail Close, Previous, Next controls carry text labels | C-UX-39 | UI/UX notes components paragraph |
| `Previous` | The frame detail Close, Previous, Next controls carry text labels | C-UX-39 | UI/UX notes components paragraph |
| `Next` | The frame detail Close, Previous, Next controls carry text labels | C-UX-39 | UI/UX notes components paragraph |
| `44` | Touch targets measure at least 44 by 44 | C-UX-40 | UI/UX notes accessibility paragraph |
| `is-fonts-ready` | The root element gains is-fonts-ready once fonts resolve | C-FE-01 | Front-end specification root state |
| `has-scrolled` | The root element gains has-scrolled after the first scroll | C-FE-02 | Front-end specification root state |
| `240x320` | Frame crops are drawn from 240x320, 320x240, 280x320, 320x200, 200x... | C-FE-19 | Front-end specification photographs |
| `320x240` | Frame crops are drawn from 240x320, 320x240, 280x320, 320x200, 200x... | C-FE-19 | Front-end specification photographs |
| `280x320` | Frame crops are drawn from 240x320, 320x240, 280x320, 320x200, 200x... | C-FE-19 | Front-end specification photographs |
| `320x200` | Frame crops are drawn from 240x320, 320x240, 280x320, 320x200, 200x... | C-FE-19 | Front-end specification photographs |
| `200x320` | Frame crops are drawn from 240x320, 320x240, 280x320, 320x200, 200x... | C-FE-19 | Front-end specification photographs |
| `320x160` | Frame crops are drawn from 240x320, 320x240, 280x320, 320x200, 200x... | C-FE-19 | Front-end specification photographs |
| `data:image/svg+xml` | The tab icon is an inline vector data address beginning data:image/... | C-FE-24 | Front-end specification drawn marks |
| `THE NEW HOLLYWOOD` | Each introduction heading reads THE NEW HOLLYWOOD | C-DM-09 | Data model introductions |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the short message shown when a save fails | C-CF-119 | the wording is left to the builder |
| the sender address of the confirmation email | C-CF-200 | only the recipient and subject are fixed |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 1 | 2 |
| User roles | 9 | 16 |
| Core features | 138 | 259 |
| User flow | 6 | 6 |
| UI/UX notes | 38 | 62 |
| Front-end specification | 32 | 35 |
| Technical requirements | 9 | 9 |
| Data model | 24 | 24 |
| Constraints | 8 | 8 |
| Deployment contract | 15 | 15 |

Overview: 13 sentences. The primary-actions sentence is the one new ask. The rest are audience and framing sentences with no ask of their own, or restate asks itemized under Constraints (not a shop, no uploads), Technical requirements (generated stand-ins), UI/UX notes (the ground and the accent) and Core features rule 50 (the last place).
User roles: Two role rows (the signed-out row split into one denial per visitor-only call), the server-side authorization sentence, the hidden-button sentence, the ownership sentence, the own-rows sentence, the open-signup sentence, the seeded-visitors sentence and the password sentence: nine asks, several split into more than one item.
Core features: 67 numbered rules holding 138 sentences, read one by one; most sentences carry two or more checkable clauses, so items outnumber sentences.
User flow: Six new asks: the route table as a whole, signup returning to the landing, the selection redirect returning to the selection, the loading ring, an error shown in place and no raw error. The route rows restate the per-route rules under Core features and User roles; the seven journeys restate Core features rules 9 to 64; the empty states restate rules 43 and 58.
UI/UX notes: 45 sentences. The north-star, register and three-stances sentences state character with no ask; Overlays close on Escape and Cancelling a visit asks first restate Core features rules 28, 31, 47 and 59. One gentle decelerating arrival names no element a visitor could watch, so no observation can pin it. The remaining 38 asks are itemized, several as more than one item: the palette roles, the single pink and its highlight job, the drawn marks beside the visit-page states, the type faces and their bound sizes, tabular numerals, the dark commitment, the two corner shapes, the glide, the quick default, reduced motion, the button states, the accessibility floors and the responsive rules.
Front-end specification: 32 asks: root state; four layering sentences (the pointer above everything, the overlay and detail below it, the header above the column, the ground layers at the bottom); the pointer-mark lead and its states, including the View badge over a cover; the eased scroll, native scroll under reduced motion and keyboard scrolling; the ring nudged aside; the title sequence existing only on the landing; the prompt blur; the heading reveal, the smooth ramp across neighbouring characters and the phrase node; the planes, the blurred stand-in and the crops; the grain, its drift with scroll, its stronger texture on dark grounds and its pointer freedom; the drawn marks with the loose strokes and the close cross; the tab icon; the tap equivalent for every hover affordance; and the three performance sentences. The other sentences restate Core features or UI/UX notes asks (the title-sequence field, the lock-up at rest, the manifesto and menu reveals, the cover fit, the gallery grounds, the absent pointer and settled landing on touch, the reduced-motion fallbacks) or describe mechanism no black-box observation confirms (the viewport slope and base unit, the breakpoint widths, the five motion mechanisms and the heading-span lift, the single scroll driver, clip groups, turbulence). The two tiny partner glyphs at label scale name no place on the page where a visitor could find them, so no observation can pin them.
Technical requirements: Server rendering, the database, SMTP into Mailpit, health, the zero-asset rule, the no-outside-request rule, no secrets in the browser and the two shared-piece sentences: nine asks. The stack names, no front-end framework, the library limit and the no-second-service rule are source facts no black-box observation confirms; Auth and Base URL restate Core features rules 1 to 7 and the Deployment contract.
Data model: 24 asks: the eight tables, integer identifiers, UTC timestamps, the one exhibition row, the gallery fields, the introduction heading and shape, the frame shape and publication, derived places and status, the frame table, 150 slots, the seeded selections and their order, the five seeded reservations, and idempotent seeding. The uniqueness and capacity invariants restate Core features rules 1, 40, 50 and 53; the seeded visitors restate User roles.
Constraints: Eight bullets, eight items.
Deployment contract: 15 asks: the public url, the port, the api prefix, health, a production build, outliving the session, binding every interface, reaching the backing services, top-level arrays, public endpoints, client-error refusals, no mocks, the single-gallery shape, the ISO 8601 timestamp format and the run date format. Each API shapes row restates the Core features rule that already itemized its shape; the compose, Dockerfile, readme and volume bullets are source facts no black-box observation confirms.

Stack names, the credentials file, the reserved directories, edge functions and persistent volumes state environment or source facts that no black-box observation can confirm, so they carry no item. Definition of done restates Overview and Core features items, so it has no block.
