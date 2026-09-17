# Checklist: Vesper

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, techrequirements, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 538
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public studio site together with a private client area on one origin. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The home route presents nine blocks in one continuous scroll. `src: Overview para 2`
- [ ] `C-OV-03` `literal` The archive holds `15` published projects. `src: Overview para 2`
- [ ] `C-OV-04` `literal` The journal holds `10` published entries. `src: Overview para 2`
- [ ] `C-OV-05` `capability` A signed-in client collects projects into one named reel. `src: Overview para 3`
- [ ] `C-OV-06` `capability` The studio reads a sent reel in the client's own order. `src: Overview para 3`
- [ ] `C-OV-07` `capability` The home route serves four audiences from four different blocks. `src: Overview para 2`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out visitor reads every public route. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A signed-out visitor cannot add an item to any reel. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A signed-out visitor cannot read any reel. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A client adds items to the reel owned by the client's own account. `src: User roles table row 2`
- [ ] `C-RL-05` `role` A client reorders the items of the reel owned by the client's own account. `src: User roles table row 2`
- [ ] `C-RL-06` `role` A client cannot read a reel owned by another account. `src: User roles table row 2`
- [ ] `C-RL-07` `role` A client cannot read the studio queue. `src: User roles table row 2`
- [ ] `C-RL-08` `role` A client cannot mark any reel answered. `src: User roles table row 2`
- [ ] `C-RL-09` `role` A curator reads the queue of sent reels. `src: User roles table row 3`
- [ ] `C-RL-10` `role` A curator reads any reel in state `sent`. `src: User roles table row 3`
- [ ] `C-RL-11` `role` A curator cannot read a reel in state `draft`. `src: User roles table row 3`
- [ ] `C-RL-12` `role` A curator cannot delete any reel. `src: User roles para after table`
- [ ] `C-RL-13` `role` A curator cannot edit a client's title, note, brief or ordering. `src: User roles table row 3`
- [ ] `C-RL-14` `constraint` The server rejects a direct API call from a client session to a curator-only endpoint. `src: User roles para 3`
- [ ] `C-RL-15` `constraint` A rejected curator-only call leaves the protected state unchanged. `src: User roles para 3`
- [ ] `C-RL-16` `capability` The app resolves a request's reel from the session account. `src: User roles para 5`
- [ ] `C-RL-17` `constraint` No client-facing address carries a reel identifier. `src: User roles para 5`
- [ ] `C-RL-18` `constraint` Signup is open to any visitor. `src: User roles para 6`
- [ ] `C-RL-19` `literal` The app seeds the account `client@example.com` with display name `Nadia Fell` in role `client`. `src: User roles seeded table row 1`
- [ ] `C-RL-20` `literal` The app seeds the account `client2@example.com` with display name `Tomas Renn` in role `client`. `src: User roles seeded table row 2`
- [ ] `C-RL-21` `literal` The app seeds the account `client3@example.com` with display name `Priya Sandoval` in role `client`. `src: User roles seeded table row 3`
- [ ] `C-RL-22` `literal` The app seeds the account `curator@example.com` with display name `Imogen Shaw` in role `curator`. `src: User roles seeded table row 4`
- [ ] `C-RL-23` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles para 6`

## C-CF Core features

- [ ] `C-CF-01` `capability` The app exchanges an email address plus a password for a session token. `src: Core features, Auth para 1`
- [ ] `C-CF-02` `capability` Sign-in returns the session token in the response body. `src: Core features, Auth para 1`
- [ ] `C-CF-03` `capability` Sign-in also sets the session token as an HTTP-only, secure, same-site cookie. `src: Core features, Auth para 1`
- [ ] `C-CF-04` `capability` The app authenticates a request carrying either the bearer token or the cookie. `src: Core features, Auth para 1`
- [ ] `C-CF-05` `constraint` The app stores a password only under a memory-hard hash with a per-account salt. `src: Core features, Auth para 1`
- [ ] `C-CF-06` `constraint` The app never returns a password in any readable form. `src: Core features, Auth para 1`
- [ ] `C-CF-07` `literal` A session lasts `30` days. `src: Core features rule 1`
- [ ] `C-CF-08` `literal` An authenticated request older than `24` hours renews the session. `src: Core features rule 1`
- [ ] `C-CF-09` `capability` Signing out revokes every session for the account. `src: Core features rule 1`
- [ ] `C-CF-10` `constraint` An absent, expired or revoked session mutates nothing. `src: Core features rule 1`
- [ ] `C-CF-11` `literal` Sign-up takes a display name of `1` to `60` characters after trimming. `src: Core features rule 2`
- [ ] `C-CF-12` `literal` Sign-up takes a password of `8` to `200` characters. `src: Core features rule 2`
- [ ] `C-CF-13` `capability` The app trims, lowercases, then caps a submitted address at `254` characters. `src: Core features rule 2`
- [ ] `C-CF-14` `constraint` The app has no email verification step before an account is usable. `src: Core features rule 2`
- [ ] `C-CF-15` `literal` A sign-up against a registered address is refused with `That email is already registered`. `src: Core features rule 3`
- [ ] `C-CF-16` `capability` A failed sign-in is refused with one message naming neither field as wrong. `src: Core features rule 4`
- [ ] `C-CF-17` `constraint` A wrong password refusal is indistinguishable from an unknown address refusal. `src: Core features rule 4`
- [ ] `C-CF-18` `constraint` A sign-in refusal takes the same time for a known address as for an unknown one. `src: Core features rule 4`
- [ ] `C-CF-19` `capability` A reset request shows the same success surface whatever the address. `src: Core features rule 5`
- [ ] `C-CF-20` `literal` A reset link is single use, valid for `60` minutes. `src: Core features rule 5`
- [ ] `C-CF-21` `constraint` No reset message is sent for an address with no account. `src: Core features rule 5`
- [ ] `C-CF-22` `capability` Using a reset link invalidates every earlier reset link for the address. `src: Core features rule 5`
- [ ] `C-CF-23` `capability` Using a reset link destroys every session for the account. `src: Core features rule 5`
- [ ] `C-CF-24` `capability` The app creates one reel per account at account creation, in state `empty`. `src: Core features rule 6`
- [ ] `C-CF-25` `constraint` The app offers no reel index, no create control, no default reel to choose. `src: Core features rule 6`
- [ ] `C-CF-26` `capability` The archive route lists every published project in the authored order. `src: Core features rule 7`
- [ ] `C-CF-27` `constraint` No collection in the app can be re-sorted by a visitor. `src: Core features rule 7`
- [ ] `C-CF-28` `literal` The archive filter controls read `All`, `Brand Identity`, `Website`, `Visuals`, `Extended Reality`. `src: Core features rule 8`
- [ ] `C-CF-29` `capability` Activating a filter narrows the mosaic to that practice field. `src: Core features rule 8`
- [ ] `C-CF-30` `literal` Activating a filter writes `?category=<slug>` into the address. `src: Core features rule 8`
- [ ] `C-CF-31` `literal` The practice field slugs are `brand-identity`, `website`, `visuals`, `extended-reality`. `src: Core features rule 8`
- [ ] `C-CF-32` `capability` Activating `All` writes the bare path into the address. `src: Core features rule 8`
- [ ] `C-CF-33` `capability` A project belonging to two practice fields appears under both filters. `src: Core features rule 9`
- [ ] `C-CF-34` `constraint` The filter set is single-select. `src: Core features rule 10`
- [ ] `C-CF-35` `constraint` Activating a filter does not scroll the page. `src: Core features rule 11`
- [ ] `C-CF-36` `capability` Filtering pushes a history entry. `src: Core features rule 11`
- [ ] `C-CF-37` `capability` The app reads the address once on first paint, then sets the filter to match. `src: Core features rule 11`
- [ ] `C-CF-38` `constraint` The app renders a filter control only for a practice field with published members. `src: Core features rule 12`
- [ ] `C-CF-39` `capability` A project detail route shows the project's introduction, media run, credit list. `src: Core features rule 13`
- [ ] `C-CF-40` `capability` A project detail route places the next project underneath the page. `src: Core features rule 13`
- [ ] `C-CF-41` `capability` An unknown project slug renders the not-found screen. `src: Core features rule 13`
- [ ] `C-CF-42` `capability` The journal route lists every published entry newest first. `src: Core features rule 14`
- [ ] `C-CF-43` `literal` The journal filter controls read `All`, `Editorial`, `Events`, `News`. `src: Core features rule 14`
- [ ] `C-CF-44` `literal` An entry's kind is one of `editorial`, `events`, `news`. `src: Core features rule 14`
- [ ] `C-CF-45` `literal` Every date the app shows is written `DD/MM/YY`, zero-padded, slash-separated. `src: Core features rule 15`
- [ ] `C-CF-46` `constraint` No date anywhere in the app is relative. `src: Core features rule 15`
- [ ] `C-CF-47` `capability` A journal entry route shows the entry, then three related entries. `src: Core features rule 16`
- [ ] `C-CF-48` `capability` An `Add` control sits on every archive tile, on the project hero, in the home navigator. `src: Core features rule 17`
- [ ] `C-CF-49` `constraint` No `Add` control appears on a journal tile. `src: Core features rule 17`
- [ ] `C-CF-50` `literal` The tile control reads `Add` before the project is in the reel, `Added` after. `src: Core features rule 17`
- [ ] `C-CF-51` `capability` Pressing `Add` without a session opens the sign-in surface carrying `next`. `src: Core features rule 18`
- [ ] `C-CF-52` `capability` The app holds a pending add across the sign-in, then applies the held add. `src: Core features rule 18`
- [ ] `C-CF-53` `capability` The app returns the visitor to the address that was being read before the held add. `src: Core features rule 18`
- [ ] `C-CF-54` `capability` The first add moves the reel from `empty` to `draft`. `src: Core features rule 19`
- [ ] `C-CF-55` `constraint` Item positions are zero-based, contiguous, unique within one reel. `src: Core features rule 19`
- [ ] `C-CF-56` `literal` A reel holds at most `12` items. `src: Core features rule 20`
- [ ] `C-CF-57` `literal` An add beyond the ceiling shows `A reel holds twelve projects at most`. `src: Core features rule 20`
- [ ] `C-CF-58` `constraint` An add beyond the ceiling leaves the tile control unchanged. `src: Core features rule 20`
- [ ] `C-CF-59` `literal` A reel title is `1` to `80` characters after trimming. `src: Core features rule 21`
- [ ] `C-CF-60` `literal` A reel title defaults to `Untitled reel`. `src: Core features rule 21`
- [ ] `C-CF-61` `literal` An item note is at most `280` characters. `src: Core features rule 21`
- [ ] `C-CF-62` `literal` A reel brief is at most `2000` characters. `src: Core features rule 21`
- [ ] `C-CF-63` `literal` The title, the note, the brief write on blur or after `800` milliseconds of idle. `src: Core features rule 21`
- [ ] `C-CF-64` `constraint` The client area carries no save control. `src: Core features rule 21`
- [ ] `C-CF-65` `literal` A character counter appears once `80%` of a field's limit is reached. `src: Core features rule 22`
- [ ] `C-CF-66` `ui` A character counter changes to the failure ink once the limit is passed. `src: Core features rule 22`
- [ ] `C-CF-67` `capability` A reel row reorders by pointer drag. `src: Core features rule 23`
- [ ] `C-CF-68` `capability` A reel row reorders by touch drag after a long press. `src: Core features rule 23`
- [ ] `C-CF-69` `capability` A reel row reorders by keyboard arrow from its focused handle. `src: Core features rule 23`
- [ ] `C-CF-70` `constraint` All three reorder inputs produce the same position write. `src: Core features rule 23`
- [ ] `C-CF-71` `literal` A touch drag begins after a long press of `300` milliseconds. `src: Core features rule 23`
- [ ] `C-CF-72` `literal` A keyboard move announces `<project title> moved to position <n> of <total>`. `src: Core features rule 23`
- [ ] `C-CF-73` `constraint` The order write is one whole ordered list of item identifiers. `src: Core features rule 24`
- [ ] `C-CF-74` `capability` The service rewrites every position from the order list's own indices. `src: Core features rule 24`
- [ ] `C-CF-75` `constraint` A reorder survives a page reload with the client's order intact. `src: Core features rule 24`
- [ ] `C-CF-76` `capability` Removing an item rewrites the remaining positions to stay contiguous. `src: Core features rule 25`
- [ ] `C-CF-77` `constraint` Removing an item asks for no confirmation. `src: Core features rule 25`
- [ ] `C-CF-78` `literal` Removing an item shows `Removed.` with a `Retry` for `5` seconds. `src: Core features rule 25`
- [ ] `C-CF-79` `literal` Emptying the reel needs a second press within `3` seconds, the label reading `Press again`. `src: Core features rule 26`
- [ ] `C-CF-80` `capability` Deleting an account requires typing the account's own address into a field. `src: Core features rule 26`
- [ ] `C-CF-81` `capability` Deleting an account deletes its reel, its items, its snapshots. `src: Core features rule 26`
- [ ] `C-CF-82` `constraint` Deleting an account retains the subscriber row. `src: Core features rule 26`
- [ ] `C-CF-83` `constraint` Send validates in a fixed order, stopping at the first failure. `src: Core features rule 27`
- [ ] `C-CF-84` `literal` A send with no item is refused with `Add at least one project`. `src: Core features rule 27`
- [ ] `C-CF-85` `literal` A send with a blank title is refused with `Give the reel a name`. `src: Core features rule 27`
- [ ] `C-CF-86` `literal` A send with an over-long brief is refused with `The brief is too long`. `src: Core features rule 27`
- [ ] `C-CF-87` `literal` A send with an over-long note is refused with `A note is too long`. `src: Core features rule 27`
- [ ] `C-CF-88` `literal` A send naming a withdrawn project is refused with `One of your projects is no longer available`. `src: Core features rule 27`
- [ ] `C-CF-89` `capability` A send against a non-draft reel is refused as already sent. `src: Core features rule 27`
- [ ] `C-CF-90` `constraint` A failing send leaves the reel in state `draft`. `src: Core features rule 27`
- [ ] `C-CF-91` `capability` A passing send moves the reel to state `sent`, writing its sent date. `src: Core features rule 28`
- [ ] `C-CF-92` `capability` A passing send freezes the reel into a snapshot at its current version. `src: Core features rule 28`
- [ ] `C-CF-93` `capability` A sent reel's surface becomes read-only. `src: Core features rule 28`
- [ ] `C-CF-94` `literal` A sent reel shows a block reading `Sent` beside a control reading `Reopen`. `src: Core features rule 28`
- [ ] `C-CF-95` `constraint` The studio reads the snapshot rather than the live reel. `src: Core features rule 28`
- [ ] `C-CF-96` `constraint` Send is never applied before the service confirms. `src: Core features rule 29`
- [ ] `C-CF-97` `constraint` Marking answered is never applied before the service confirms. `src: Core features rule 29`
- [ ] `C-CF-98` `capability` Reopening a sent reel returns the reel to state `draft`, clearing the sent date. `src: Core features rule 30`
- [ ] `C-CF-99` `capability` Reopening a sent reel discards the snapshot, dropping the reel from the queue. `src: Core features rule 30`
- [ ] `C-CF-100` `literal` Reopening shows a strip message saying the studio no longer sees the reel. `src: Core features rule 30`
- [ ] `C-CF-101` `constraint` A reel in state `answered` can never be reopened. `src: Core features rule 30`
- [ ] `C-CF-102` `capability` Editing after `answered` starts a new send cycle at the next version. `src: Core features rule 30`
- [ ] `C-CF-103` `capability` The queue lists every reel in state `sent`, newest sent first. `src: Core features rule 31`
- [ ] `C-CF-104` `capability` A queue row carries the client's display name, the reel title, the item count, the sent date. `src: Core features rule 31`
- [ ] `C-CF-105` `capability` The queue pages by cursor rather than by page number. `src: Core features rule 31`
- [ ] `C-CF-106` `literal` The empty queue reads `No reels waiting`. `src: Core features rule 31`
- [ ] `C-CF-107` `capability` A studio reel route renders one reel read-only in the client's order. `src: Core features rule 32`
- [ ] `C-CF-108` `literal` A studio reel route carries a control reading `Mark answered`. `src: Core features rule 32`
- [ ] `C-CF-109` `constraint` The studio side carries no reply field. `src: Core features rule 32`
- [ ] `C-CF-110` `capability` Marking a reel answered moves the reel to state `answered`, writing the answered date. `src: Core features rule 33`
- [ ] `C-CF-111` `literal` An answered reel shows the owner a block reading `The studio has your reel`. `src: Core features rule 33`
- [ ] `C-CF-112` `constraint` The answered block does not dismiss. `src: Core features rule 33`
- [ ] `C-CF-113` `capability` A client requesting a studio address sees the denied screen at that address. `src: Core features rule 34`
- [ ] `C-CF-114` `capability` A curator requesting a draft reel sees the not-found screen. `src: Core features rule 34`
- [ ] `C-CF-115` `constraint` Adding, removing, reordering, renaming, noting are applied on screen first. `src: Core features rule 35`
- [ ] `C-CF-116` `capability` A failed reorder animates the row back to the service order. `src: Core features rule 36`
- [ ] `C-CF-117` `literal` A failed reorder shows `Could not reorder. Put back.` `src: Core features rule 36`
- [ ] `C-CF-118` `literal` A failed add shows `Could not add that.` `src: Core features rule 36`
- [ ] `C-CF-119` `capability` A failed add returns the tile control from `Added` to `Add`. `src: Core features rule 36`
- [ ] `C-CF-120` `capability` A failed remove returns the row to the list. `src: Core features rule 36`
- [ ] `C-CF-121` `constraint` A failed text write never replaces what the client typed. `src: Core features rule 37`
- [ ] `C-CF-122` `literal` A failed text write shows `Not saved.` offering `Retry`. `src: Core features rule 37`
- [ ] `C-CF-123` `constraint` Two sessions reordering one reel resolve as one whole list winning. `src: Core features rule 38`
- [ ] `C-CF-124` `constraint` Two sessions editing different fields do not clobber each other. `src: Core features rule 38`
- [ ] `C-CF-125` `capability` A send against a reel already sent reconciles the surface to read-only. `src: Core features rule 38`
- [ ] `C-CF-126` `capability` The studio queue polls for new reels rather than holding a connection open. `src: Core features rule 39`
- [ ] `C-CF-127` `constraint` No surface polls when the document is hidden. `src: Core features rule 39`
- [ ] `C-CF-128` `constraint` No public route updates without a reload. `src: Core features rule 39`
- [ ] `C-CF-129` `constraint` Every form uses one grammar: field, submit, pending, success, failure. `src: Core features rule 40`
- [ ] `C-CF-130` `constraint` The app shows no spinner anywhere. `src: Core features rule 40`
- [ ] `C-CF-131` `constraint` A submit control is disabled only during a request in flight. `src: Core features rule 41`
- [ ] `C-CF-132` `capability` An empty required field produces a message on submit. `src: Core features rule 41`
- [ ] `C-CF-133` `capability` A rejected submit keeps every field value. `src: Core features rule 42`
- [ ] `C-CF-134` `capability` A rejected submit moves focus to the field the response names. `src: Core features rule 42`
- [ ] `C-CF-135` `capability` The newsletter field accepts an address from the footer of every long public route. `src: Core features rule 43`
- [ ] `C-CF-136` `ui` The newsletter field displays whatever is typed in lower case. `src: Core features rule 43`
- [ ] `C-CF-137` `literal` A newsletter success replaces the form with `Thanks for subscribing`. `src: Core features rule 43`
- [ ] `C-CF-138` `literal` A newsletter failure without a named reason reads `Something went wrong`. `src: Core features rule 43`
- [ ] `C-CF-139` `constraint` The app renders every visitor-supplied string as text, never as markup. `src: Core features rule 44`
- [ ] `C-CF-140` `constraint` The app returns a pasted string with the characters that were typed, unedited. `src: Core features rule 44`
- [ ] `C-CF-141` `constraint` A `next` value must begin with one slash, never two. `src: Core features rule 45`
- [ ] `C-CF-142` `capability` An unknown `category` value is treated as absent. `src: Core features rule 45`
- [ ] `C-CF-143` `capability` A repeat newsletter submission for one address inside an hour is accepted, then discarded. `src: Core features rule 46`
- [ ] `C-CF-144` `literal` A repeat reset request for one address inside `15` minutes answers as the first did. `src: Core features rule 46`
- [ ] `C-CF-145` `capability` The app limits sign-in, sign-up, send with a visible refusal. `src: Core features rule 46`
- [ ] `C-CF-146` `literal` Account creation writes a message with subject `Vesper: your reel`. `src: Core features rule 47`
- [ ] `C-CF-147` `literal` A reset request writes a message with subject `Vesper: reset your password`. `src: Core features rule 47`
- [ ] `C-CF-148` `literal` Sending a reel writes the client a message with subject `Vesper: we have your reel`. `src: Core features rule 47`
- [ ] `C-CF-149` `literal` Sending a reel writes `contact@vesper.works` a message with subject `New reel from <display name>`. `src: Core features rule 47`
- [ ] `C-CF-150` `constraint` No transactional message carries note text. `src: Core features rule 47`
- [ ] `C-CF-151` `constraint` The app has no notification centre, no unread count, no bell, no digest. `src: Core features rule 48`
- [ ] `C-CF-152` `constraint` The notification strip shows one message at a time. `src: Core features rule 48`
- [ ] `C-CF-153` `literal` A strip message leaves after `5` seconds. `src: Core features rule 48`
- [ ] `C-CF-154` `constraint` A second strip message replaces the first without re-animating the strip. `src: Core features rule 48`
- [ ] `C-CF-155` `capability` The app records a page view carrying the route with the moment of the view. `src: Core features rule 49`
- [ ] `C-CF-156` `capability` The app records the twenty named events. `src: Core features rule 49`
- [ ] `C-CF-157` `literal` A project opening carries `surface`, one of eight values. `src: Core features rule 49`
- [ ] `C-CF-158` `constraint` The app records only a curator-readable event log. `src: Core features rule 49`
- [ ] `C-CF-159` `constraint` No recorded event carries an address, a display name, a title, a note, a brief. `src: Core features rule 50`
- [ ] `C-CF-160` `literal` A note event records `length_bucket` of `short`, `medium` or `long`. `src: Core features rule 50`
- [ ] `C-CF-161` `capability` A first-time visitor is asked once about measurement in the notification strip. `src: Core features rule 51`
- [ ] `C-CF-162` `capability` The measurement answer survives a reload. `src: Core features rule 51`
- [ ] `C-CF-163` `constraint` Refusing measurement leaves the whole product working identically. `src: Core features rule 51`
- [ ] `C-CF-164` `capability` The app keeps four counts regardless of the measurement answer. `src: Core features rule 52`
- [ ] `C-CF-165` `literal` An imprint plus privacy page lives at `/legal/imprint-privacy-policy`. `src: Core features rule 53`
- [ ] `C-CF-166` `capability` The privacy page states what the product stores about a client. `src: Core features rule 53`
- [ ] `C-CF-167` `literal` A terms page lives at `/legal/terms`. `src: Core features rule 53`
- [ ] `C-CF-168` `capability` The terms page is linked from the sign-up form beside the submit control. `src: Core features rule 53`
- [ ] `C-CF-169` `constraint` Every internal link on every public route resolves. `src: Core features rule 54`
- [ ] `C-CF-170` `capability` An address matching nothing renders the studio's own not-found screen. `src: Core features rule 55`
- [ ] `C-CF-171` `constraint` An address matching nothing answers with a not-found status. `src: Core features rule 55`
- [ ] `C-CF-172` `constraint` No two public routes share a title. `src: Core features rule 56`
- [ ] `C-CF-173` `capability` Each public route carries the exact title pinned for that route. `src: Core features rule 56`

## C-UF User flow

- [ ] `C-UF-01` `capability` The app serves the thirteen routes named in the route table. `src: User flow route table`
- [ ] `C-UF-02` `literal` The navigation reads `PROJECTS`, `SIGNALS`, `CONTACT` over the addresses `/work`, `/blog`, `/contact`. `src: User flow para after table`
- [ ] `C-UF-03` `capability` A signed-out request for a studio address redirects to `/sign-in` carrying `next`. `src: User flow, Entry and redirects bullet 1`
- [ ] `C-UF-04` `capability` The app returns the visitor to the `next` path once the session exists. `src: User flow, Entry and redirects bullet 1`
- [ ] `C-UF-05` `constraint` A signed-in client requesting a studio address is not redirected. `src: User flow, Entry and redirects bullet 2`
- [ ] `C-UF-06` `literal` The denied screen reads `Not your reel` above a control reading `back to yours`. `src: User flow, Entry and redirects bullet 2`
- [ ] `C-UF-07` `capability` The reel route renders for a signed-out visitor. `src: User flow, Entry and redirects bullet 3`
- [ ] `C-UF-08` `literal` The signed-out reel surface reads `Sign in to start a reel` above a control reading `Sign in`. `src: User flow, Entry and redirects bullet 3`
- [ ] `C-UF-09` `capability` The sign-in route redirects a signed-in client to `/reel`. `src: User flow, Entry and redirects bullet 4`
- [ ] `C-UF-10` `capability` The sign-in route redirects a curator to `/studio/reels`. `src: User flow, Entry and redirects bullet 4`
- [ ] `C-UF-11` `capability` A session expiring mid-edit holds the pending write, then replays that write. `src: User flow, Entry and redirects bullet 5`
- [ ] `C-UF-12` `capability` Signing out returns the visitor to the home route. `src: User flow, Entry and redirects bullet 6`
- [ ] `C-UF-13` `capability` The sign-in surface carries four modes in its query. `src: User flow route table row 9`
- [ ] `C-UF-14` `ui` Every collection has an empty surface built from a mark, one line, one optional control. `src: User flow, States bullet 1`
- [ ] `C-UF-15` `literal` A filtered archive with no members offers a control reading `Show all projects`. `src: User flow, States bullet 1`
- [ ] `C-UF-16` `literal` A filtered journal with no members offers a control reading `Show all entries`. `src: User flow, States bullet 1`
- [ ] `C-UF-17` `literal` An empty signed-in reel reads `Your reel is empty` with `Browse projects`. `src: User flow, States bullet 1`
- [ ] `C-UF-18` `constraint` Related entries, the client wall, the awards wall are not rendered when empty. `src: User flow, States bullet 2`
- [ ] `C-UF-19` `ui` Every loading surface is a placeholder at exactly the size of the element replaced. `src: User flow, States bullet 3`
- [ ] `C-UF-20` `literal` A failed load offers a control reading `Try again`. `src: User flow, States bullet 4`
- [ ] `C-UF-21` `literal` A row that lost its project reads `No longer available`, keeping only its remove control. `src: User flow, States bullet 4`
- [ ] `C-UF-22` `literal` Losing the connection raises a strip reading `You are offline`. `src: User flow, States bullet 5`
- [ ] `C-UF-23` `literal` A held reel edit reads `You are offline. Changes will be saved.` `src: User flow, States bullet 5`
- [ ] `C-UF-24` `capability` Held writes replay in order when the connection returns. `src: User flow, States bullet 5`
- [ ] `C-UF-25` `literal` A send with no connection is blocked, reading `Could not send. Your reel is safe.` `src: User flow, States bullet 5`
- [ ] `C-UF-26` `constraint` A surface never shows two states at once. `src: User flow, States bullet 6`
- [ ] `C-UF-27` `constraint` An error renders a surface rather than a blank page. `src: User flow, States bullet 7`
- [ ] `C-UF-28` `capability` The graded journey ends with a curator reading the client's order with the client's note. `src: User flow, Journey 2`

## C-UX UI/UX notes

- [ ] `C-UX-01` `ui` The product is built to one north star: a visitor believes the studio can make something rare. `src: UI/UX notes, north star`
- [ ] `C-UX-02` `ui` The register is consumer editorial, never an operational dashboard. `src: UI/UX notes, register`
- [ ] `C-UX-03` `ui` The ground is a near-black neutral on every route except the foot of the page. `src: UI/UX notes, palette para 1`
- [ ] `C-UX-04` `ui` The ink is a near-white neutral used for body text, hairlines, icon fills. `src: UI/UX notes, palette para 1`
- [ ] `C-UX-05` `ui` One mid, vivid red is the only accent on the ground. `src: UI/UX notes, palette para 1`
- [ ] `C-UX-06` `ui` A second red one step hotter marks emphasis inside project introduction copy only. `src: UI/UX notes, palette para 1`
- [ ] `C-UX-07` `ui` Three translucent tints exist: a panel fill, a rule line, one divider. `src: UI/UX notes, palette para 1`
- [ ] `C-UX-08` `constraint` No colour family outside neutral, red appears anywhere in the product. `src: UI/UX notes, palette para 1`
- [ ] `C-UX-09` `ui` Type is one grotesque at three cuts, with no italic, no second family. `src: UI/UX notes, type para 1`
- [ ] `C-UX-10` `ui` Journal body copy is set visibly looser than display type. `src: UI/UX notes, type para 2`
- [ ] `C-UX-11` `ui` Display sizes grow smoothly between two anchor widths rather than stepping. `src: UI/UX notes, type para 3`
- [ ] `C-UX-12` `ui` Small uppercase labels never grow at any width. `src: UI/UX notes, type para 3`
- [ ] `C-UX-13` `ui` Every heading honours the line breaks its copy was written with. `src: UI/UX notes, type para 3`
- [ ] `C-UX-14` `constraint` Nothing in the product has a rounded corner. `src: UI/UX notes, shape para 1`
- [ ] `C-UX-15` `constraint` Nothing in the product casts a shadow. `src: UI/UX notes, shape para 1`
- [ ] `C-UX-16` `ui` A frosting sits behind every control so a hairline stays legible over moving media. `src: UI/UX notes, shape para 1`
- [ ] `C-UX-17` `ui` One gap separates every two pieces of media at every width. `src: UI/UX notes, shape para 2`
- [ ] `C-UX-18` `ui` Every fractional tile subtracts its own share of that gap. `src: UI/UX notes, shape para 2`
- [ ] `C-UX-19` `ui` Sections are separated by space rather than by dividing rules. `src: UI/UX notes, shape para 2`
- [ ] `C-UX-20` `ui` The wordmark sits under the navigation, over the scroll marker. `src: UI/UX notes, layering para`
- [ ] `C-UX-21` `ui` Almost every clickable thing is one bar with a hairline outline plus a rising fill. `src: UI/UX notes, the one interactive shape`
- [ ] `C-UX-22` `ui` The control has resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes, the one interactive shape`
- [ ] `C-UX-23` `constraint` Unavailable is never signalled by colour alone. `src: UI/UX notes, the one interactive shape`
- [ ] `C-UX-24` `ui` The control's fill arrives faster than its ink changes. `src: UI/UX notes, the one interactive shape`
- [ ] `C-UX-25` `ui` The control's outline changes colour only, never width. `src: UI/UX notes, the one interactive shape`
- [ ] `C-UX-26` `ui` A section declares one accent that every control inside reads. `src: UI/UX notes, accent declaration`
- [ ] `C-UX-27` `ui` Four curve roles carry every movement in the product. `src: UI/UX notes, motion para 1`
- [ ] `C-UX-28` `ui` A headline reveals as a soft window travelling up through the letters, staggered per line. `src: UI/UX notes, motion para 2`
- [ ] `C-UX-29` `ui` Scrolling back up un-reveals a headline rather than replaying the reveal. `src: UI/UX notes, motion para 2`
- [ ] `C-UX-30` `ui` Every named motion moment is built, from the control fill to the category pan. `src: UI/UX notes, motion para 3`
- [ ] `C-UX-31` `ui` Reduced motion stops continuous movement at its first frame. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-32` `ui` Reduced motion applies every reveal at once, keeping the text readable. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-33` `ui` Reduced motion keeps every response to a direct action. `src: UI/UX notes, reduced motion`
- [ ] `C-UX-34` `ui` The letterform lean, the curtain split, the contact band share one angle. `src: UI/UX notes, the diagonal`
- [ ] `C-UX-35` `ui` The diagonal is defined against the height of the window rather than its width. `src: UI/UX notes, the diagonal`
- [ ] `C-UX-36` `constraint` All text meets the WCAG AA contrast bar against the ground behind the text. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-37` `constraint` Small text is never set in the red on the near-black ground. `src: UI/UX notes, accessibility para 1`
- [ ] `C-UX-38` `ui` Focus thickens a control's outline where hover raises its fill. `src: UI/UX notes, accessibility para 2`
- [ ] `C-UX-39` `constraint` Nothing removes focus visibility without replacing the treatment. `src: UI/UX notes, accessibility para 2`
- [ ] `C-UX-40` `capability` The first focusable element on every route is a skip control. `src: UI/UX notes, accessibility para 2`
- [ ] `C-UX-41` `capability` The mobile panel traps focus, releasing on Escape to the button that opened the panel. `src: UI/UX notes, accessibility para 2`
- [ ] `C-UX-42` `constraint` Meaning is never carried by colour alone. `src: UI/UX notes, accessibility para 2`
- [ ] `C-UX-43` `capability` One polite live region per route carries exactly four kinds of message. `src: UI/UX notes, accessibility para 3`
- [ ] `C-UX-44` `constraint` The product is dark only, surviving a forced-colours mode. `src: UI/UX notes, accessibility para 4`
- [ ] `C-UX-45` `ui` The opening headline's region carries a darkening layer over a bright picture. `src: UI/UX notes, accessibility para 4`
- [ ] `C-UX-46` `ui` The layout holds at every width between the three named widths. `src: UI/UX notes, responsive para 1`
- [ ] `C-UX-47` `constraint` At a narrow viewport nothing overflows sideways. `src: UI/UX notes, responsive para 1`
- [ ] `C-UX-48` `constraint` The media gap, the control height, the label size, the icon size never change with width. `src: UI/UX notes, responsive para 2`
- [ ] `C-UX-49` `constraint` Every hover effect is gated on a device with a pointer. `src: UI/UX notes, responsive para 3`
- [ ] `C-UX-50` `ui` Full-height surfaces use a height the page computes, rewritten on every resize. `src: UI/UX notes, responsive para 4`
- [ ] `C-UX-51` `capability` The product refuses to print every route except the legal routes, the journal body. `src: UI/UX notes, responsive para 5`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app is a server-rendered multi-page product built on Express with Nunjucks. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` Alpine.js progressively enhances the filter row, the tile expand, the reel editing. `src: Technical requirements para 1`
- [ ] `C-TR-03` `capability` A route's content is present in the first response. `src: Technical requirements para 1`
- [ ] `C-TR-04` `capability` A visitor with script disabled reads every public route. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` The datastore is PostgreSQL, reached at `DATABASE_URL`. `src: Technical requirements para 2`
- [ ] `C-TR-06` `contract` The app reads `APP_PUBLIC_URL` plus `APP_PUBLIC_PORT` from the environment. `src: Technical requirements para 2`
- [ ] `C-TR-07` `constraint` The app introduces no second database, cache, queue, object store, identity provider, mail vendor. `src: Technical requirements, blockquote`
- [ ] `C-TR-08` `contract` `GET /api/health` returns `200` once the app holds a database connection. `src: Technical requirements para 4`
- [ ] `C-TR-09` `constraint` A log line never carries a session token, a password, a reel title, a note, a brief. `src: Technical requirements para 4`
- [ ] `C-TR-10` `capability` Every public route carries its own meta description. `src: Technical requirements para 5`
- [ ] `C-TR-11` `constraint` Nothing the browser downloads carries a credential. `src: Technical requirements para 6`
- [ ] `C-TR-12` `constraint` The app fetches nothing from outside its own origin. `src: Technical requirements para 8`
- [ ] `C-TR-13` `capability` Every picture is generated in the browser from a seed derived from a slug. `src: Technical requirements para 8`
- [ ] `C-TR-14` `capability` The same project always produces the same generated picture. `src: Technical requirements para 8`
- [ ] `C-TR-15` `capability` The particle form is a subdivided icosahedron with displaced vertices, flat normals. `src: Technical requirements para 9`
- [ ] `C-TR-16` `literal` The contact object's parts keep the prefixes `Shell`, `WindShield`, `Vent`, `Sticker`, `Trim`. `src: Technical requirements para 9`
- [ ] `C-TR-17` `constraint` The app runs exactly one scroll subscriber. `src: Technical requirements para 10`
- [ ] `C-TR-18` `capability` The scroll subscriber reads all geometry first, then writes every derived value. `src: Technical requirements para 10`
- [ ] `C-TR-19` `constraint` Every transition names the properties each transition applies to. `src: Technical requirements para 10`
- [ ] `C-TR-20` `capability` Media loads only once within one viewport height of the visible area. `src: Technical requirements para 11`
- [ ] `C-TR-21` `constraint` At most two pieces of moving media play at once. `src: Technical requirements para 11`
- [ ] `C-TR-22` `constraint` All moving media is muted, playing inline. `src: Technical requirements para 11`
- [ ] `C-TR-23` `constraint` Both real-time surfaces stop rendering when the document is hidden. `src: Technical requirements para 12`
- [ ] `C-TR-24` `capability` The real-time surfaces reduce resolution before dropping a frame. `src: Technical requirements para 12`
- [ ] `C-TR-25` `constraint` The real-time surface is never removed entirely. `src: Technical requirements para 12`
- [ ] `C-TR-26` `capability` The five particle lighting values are read once at start from one configuration source. `src: Technical requirements para 13`
- [ ] `C-TR-27` `constraint` No control surface for the lighting values is reachable in the running product. `src: Technical requirements para 13`
- [ ] `C-TR-28` `contract` Every response carries a strict transport policy plus a nosniff content-type policy. `src: Technical requirements para 14`
- [ ] `C-TR-29` `contract` Every response refuses framing by another origin. `src: Technical requirements para 14`
- [ ] `C-TR-30` `constraint` The app accepts no cross-origin request. `src: Technical requirements para 14`

## C-DM Data model

- [ ] `C-DM-01` `data` The app holds sixteen tables. `src: Data model para 1`
- [ ] `C-DM-02` `data` All timestamps are UTC. `src: Data model para 1`
- [ ] `C-DM-03` `literal` The seeded password `deku-demo-pw-2026` works at login. `src: Data model blockquote`
- [ ] `C-DM-04` `contract` Each seeded account is written into `/app/USER_README.md`. `src: Data model blockquote`
- [ ] `C-DM-05` `data` A category carries `id`, `slug`, `name`, `scope`, `position`. `src: Data model, category`
- [ ] `C-DM-06` `data` A project carries `slug`, `title`, `subtitle`, `intro`, `credits`, `published`, `position`, `tile_width`. `src: Data model, project`
- [ ] `C-DM-07` `data` A project belongs to any number of practice fields through a join. `src: Data model, project_category`
- [ ] `C-DM-08` `data` A signal carries `slug`, `title`, `kind`, `published_on`, `body`, `published`. `src: Data model, signal`
- [ ] `C-DM-09` `data` An entry holds up to three related entries. `src: Data model, signal_related`
- [ ] `C-DM-10` `data` The app holds twelve client marks. `src: Data model, client_mark`
- [ ] `C-DM-11` `data` The app holds four awards, each with two caption lines. `src: Data model, award`
- [ ] `C-DM-12` `data` An account carries `email`, `display_name`, `password_hash`, `role`, `created_at`, `last_seen_at`. `src: Data model, account`
- [ ] `C-DM-13` `constraint` Every identifier is an opaque string, never a sequential integer. `src: Data model, account`
- [ ] `C-DM-14` `data` A session row stores only the hash of a session token. `src: Data model, session`
- [ ] `C-DM-15` `data` A reset token is single use, compared in constant time, deleted on use. `src: Data model, reset_token`
- [ ] `C-DM-16` `data` A reel carries `title`, `brief`, `state`, `version`, `sent_at`, `answered_at`, `updated_at`. `src: Data model, reel`
- [ ] `C-DM-17` `constraint` One account owns exactly one reel. `src: Data model, reel`
- [ ] `C-DM-18` `literal` A reel state is one of `empty`, `draft`, `sent`, `answered`. `src: Data model, reel`
- [ ] `C-DM-19` `data` A reel version starts at `1`, incrementing per send cycle. `src: Data model, reel`
- [ ] `C-DM-20` `constraint` A reel's positions are always the integers from zero to one less than its item count. `src: Data model, reel_item`
- [ ] `C-DM-21` `constraint` Two simultaneous reorders leave no gap, no duplicate, no thirteenth row. `src: Data model, reel_item`
- [ ] `C-DM-22` `constraint` One project never appears twice in one reel. `src: Data model, reel_item`
- [ ] `C-DM-23` `data` A snapshot holds the ordered items with their notes as stored at the send. `src: Data model, reel_snapshot`
- [ ] `C-DM-24` `data` An outbox message carries `to_address`, `subject`, `body`, `created_at`. `src: Data model, outbox_message`
- [ ] `C-DM-25` `data` An event log row carries `name`, `route`, `properties`, `created_at`. `src: Data model, event_log`
- [ ] `C-DM-26` `constraint` The item count of a reel is derived rather than stored. `src: Data model, derived para`
- [ ] `C-DM-27` `capability` A withdrawn project leaves its reel item in place, rendered as unavailable. `src: Data model, reference para`
- [ ] `C-DM-28` `constraint` Deleting a project never deletes a reel item. `src: Data model, deleting para`
- [ ] `C-DM-29` `constraint` Seeding is idempotent, so restarting the app duplicates no row. `src: Data model, final line`
- [ ] `C-DM-30` `literal` The app seeds fifteen projects, the first four being the home run. `src: Front-end specification, Archive copy table`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Scaling works in three regimes: a fixed low anchor, an interpolation, a fixed high anchor. `src: Front-end specification, token layer`
- [ ] `C-FE-02` `ui` The page gutter steps at the tablet breakpoint, then becomes proportional above the desktop breakpoint. `src: Front-end specification, token layer`
- [ ] `C-FE-03` `ui` Six glyphs exist, every one drawn as inline vector geometry. `src: Front-end specification, iconography`
- [ ] `C-FE-04` `ui` The arrow is one closed filled outline rather than a line plus a caret. `src: Front-end specification, iconography 1`
- [ ] `C-FE-05` `ui` The outbound arrow marks the contact address, the social destinations, the legal link. `src: Front-end specification, iconography 2`
- [ ] `C-FE-06` `ui` A six-pointed asterisk in an outlined box opens every section on every route. `src: Front-end specification, iconography 3`
- [ ] `C-FE-07` `ui` The menu bars fold into a cross about the bar already centred when closed. `src: Front-end specification, iconography 4`
- [ ] `C-FE-08` `ui` The scroll indicator is a mouse body with a wheel dot inside a dashed ring. `src: Front-end specification, iconography 5`
- [ ] `C-FE-09` `ui` The not-found numerals are one path filled in the signal red. `src: Front-end specification, iconography 6`
- [ ] `C-FE-10` `ui` A seventh glyph keeps one constant stroke measure expressed as a fraction of its canvas. `src: Front-end specification, iconography rules`
- [ ] `C-FE-11` `ui` The wordmark is set edge to edge across the window twice on the home route. `src: Front-end specification, the wordmark`
- [ ] `C-FE-12` `ui` Every wordmark stroke is a parallelogram sheared about the vertical at the page's angle. `src: Front-end specification, the wordmark`
- [ ] `C-FE-13` `ui` Wordmark counters are cut as parallel slots rather than as curves. `src: Front-end specification, the wordmark`
- [ ] `C-FE-14` `ui` The curtain mark is two sheared blades stacked with a diagonal gap between. `src: Front-end specification, the wordmark`
- [ ] `C-FE-15` `ui` The tiling lockup closes the seam between repeats. `src: Front-end specification, the wordmark`
- [ ] `C-FE-16` `ui` The wordmark layer is fixed at the top left, padded by the gutter of its width. `src: Front-end specification, global chrome`
- [ ] `C-FE-17` `ui` The navigation row occupies exactly the right half of the screen above the desktop width. `src: Front-end specification, global chrome`
- [ ] `C-FE-18` `constraint` No home link sits in the navigation bar. `src: Front-end specification, global chrome`
- [ ] `C-FE-19` `constraint` Below the desktop width the three bars are removed from the document. `src: Front-end specification, global chrome`
- [ ] `C-FE-20` `ui` The mobile panel is revealed by clipping so the page behind never shifts. `src: Front-end specification, global chrome`
- [ ] `C-FE-21` `ui` The mobile panel's contents settle a fraction behind its wipe. `src: Front-end specification, global chrome`
- [ ] `C-FE-22` `ui` The mobile panel rows read `PROJECTS`, `SIGNALS`, `CONTACT`, then the two social destinations. `src: Front-end specification, global chrome`
- [ ] `C-FE-23` `ui` The native scrollbar is replaced by a fixed rail taking no pointer events. `src: Front-end specification, global chrome`
- [ ] `C-FE-24` `ui` The scroll rail fades in during a gesture, then fades out again. `src: Front-end specification, global chrome`
- [ ] `C-FE-25` `ui` The footer field is the signal red, present on the home, archive, journal routes. `src: Front-end specification, global chrome`
- [ ] `C-FE-26` `ui` The footer carries a main column, a links column, an address column. `src: Front-end specification, global chrome`
- [ ] `C-FE-27` `ui` The footer wordmark drifts sideways below the desktop width, spanning the page above. `src: Front-end specification, global chrome`
- [ ] `C-FE-28` `ui` The opening loader is two diagonal half-curtains, a counter, a compressed wordmark. `src: Front-end specification, global chrome`
- [ ] `C-FE-29` `ui` The two loader curtain halves overlap by a hair so no line of page shows through. `src: Front-end specification, global chrome`
- [ ] `C-FE-30` `ui` The loader counter converges a live percentage against a fixed full figure. `src: Front-end specification, global chrome`
- [ ] `C-FE-31` `ui` The loader wordmark fills in from the left in step with progress. `src: Front-end specification, global chrome`
- [ ] `C-FE-32` `ui` The loader stops animating near completion rather than easing the last stretch. `src: Front-end specification, global chrome`
- [ ] `C-FE-33` `ui` The route curtain sweeps the same diagonal on a tighter curve, carrying the mark. `src: Front-end specification, global chrome`
- [ ] `C-FE-34` `literal` The section labels read `Projects`, `Services`, `Clients`, `Awards`, `Latest Signals`, `Newsletter`, `Work`, `Blog`, `Your reel`, `Sign in`, `Reels`. `src: Front-end specification, the section label`
- [ ] `C-FE-35` `ui` The control's label is drawn twice so the second copy arrives with the fill. `src: Front-end specification, control primitive`
- [ ] `C-FE-36` `ui` The control's icon well is drawn twice so a fresh arrow arrives from the left. `src: Front-end specification, control primitive`
- [ ] `C-FE-37` `ui` The control has four variants plus a bare variant that drops the frosting. `src: Front-end specification, control primitive`
- [ ] `C-FE-38` `ui` Where there is no pointer, a control whose readable state is its filled state stays filled. `src: Front-end specification, control primitive`
- [ ] `C-FE-39` `ui` The word reveal splits a headline into lines, words, characters on the laid-out text. `src: Front-end specification, motion vocabulary`
- [ ] `C-FE-40` `ui` A revealing word rises half its own height as its window travels. `src: Front-end specification, motion vocabulary`
- [ ] `C-FE-41` `ui` The resting travel of a revealing word is instantaneous with a delay. `src: Front-end specification, motion vocabulary`
- [ ] `C-FE-42` `ui` The paragraph reveal carries emphasis by hue at the surrounding boldness. `src: Front-end specification, motion vocabulary`
- [ ] `C-FE-43` `ui` Only two named keyframe sets exist: the travelling window, the foot band drift. `src: Front-end specification, motion vocabulary`
- [ ] `C-FE-44` `ui` The diagonal is authored once, shared by loader, curtain, not-found, denied. `src: Front-end specification, the diagonal`
- [ ] `C-FE-45` `ui` The diagonal degrades to a straight vertical split on a very tall window. `src: Front-end specification, the diagonal`
- [ ] `C-FE-46` `capability` Wheel input is interpolated so the document approaches its target rather than jumping. `src: Front-end specification, scroll system`
- [ ] `C-FE-47` `capability` Native scroll stays the source of truth for anchors, keyboard paging, assistive technology. `src: Front-end specification, scroll system`
- [ ] `C-FE-48` `capability` The app releases native overflow if the interpolation layer has not mounted. `src: Front-end specification, scroll system`
- [ ] `C-FE-49` `ui` Every media surface moves against the page at one shared factor of scroll speed. `src: Front-end specification, scroll system`
- [ ] `C-FE-50` `ui` A parallax wrapper is over-scanned so the depth factor never reveals an edge. `src: Front-end specification, scroll system`
- [ ] `C-FE-51` `constraint` The navigator's label, thumbnail, destination come from one computed index. `src: Front-end specification, scroll system`
- [ ] `C-FE-52` `ui` The rolling label runs two copies one line apart so the loop has no seam. `src: Front-end specification, scroll system`
- [ ] `C-FE-53` `ui` The particle field places instances evenly over a sphere by a spiral distribution. `src: Front-end specification, real-time layers`
- [ ] `C-FE-54` `ui` Each particle instance carries its own orientation, velocity, size, drift speed. `src: Front-end specification, real-time layers`
- [ ] `C-FE-55` `ui` The particle field is fully populated on its first frame rather than marching in. `src: Front-end specification, real-time layers`
- [ ] `C-FE-56` `ui` A single pointer-driven lamp in the signal red is the only light in the scene. `src: Front-end specification, real-time layers`
- [ ] `C-FE-57` `ui` Each particle carries a wide soft sheen plus a small hard hot spot. `src: Front-end specification, real-time layers`
- [ ] `C-FE-58` `ui` The lamp lags the pointer by interpolating a small fraction each frame. `src: Front-end specification, real-time layers`
- [ ] `C-FE-59` `capability` The particle field is not drawn at all when the manifesto block is off screen. `src: Front-end specification, real-time layers`
- [ ] `C-FE-60` `constraint` The development lamp marker is never visible in the shipped product. `src: Front-end specification, real-time layers`
- [ ] `C-FE-61` `ui` The contact object's environment counter-rotates against the object. `src: Front-end specification, real-time layers`
- [ ] `C-FE-62` `constraint` The contact object takes no pointer events, leaving the copy selectable. `src: Front-end specification, real-time layers`
- [ ] `C-FE-63` `ui` The home opening pins four superimposed layers inside one full-height block. `src: Front-end specification, home route 1`
- [ ] `C-FE-64` `ui` The opening media swells slightly, fading out, holding that end state. `src: Front-end specification, home route 1`
- [ ] `C-FE-65` `ui` The scroll indicator appears once at the top, never returning. `src: Front-end specification, home route 2`
- [ ] `C-FE-66` `ui` The manifesto sentence is pinned for two full screens. `src: Front-end specification, home route 3`
- [ ] `C-FE-67` `ui` The four project items each fill one screen inside a clipping block. `src: Front-end specification, home route 4`
- [ ] `C-FE-68` `ui` The navigator's thumbnail column, label column carry one shared travel. `src: Front-end specification, home route 5`
- [ ] `C-FE-69` `ui` The navigator's label column fades at its top edge, its bottom edge. `src: Front-end specification, home route 5`
- [ ] `C-FE-70` `constraint` Only the navigator's active row takes pointer events. `src: Front-end specification, home route 5`
- [ ] `C-FE-71` `ui` The four practice fields carry a numeral, a two-line title, a short body. `src: Front-end specification, home route 6`
- [ ] `C-FE-72` `ui` The practice field divider disappears above the desktop width. `src: Front-end specification, home route 6`
- [ ] `C-FE-73` `constraint` The client wall takes no pointer events anywhere in the block. `src: Front-end specification, home route 7`
- [ ] `C-FE-74` `capability` Each client mark carries its owner's name as its accessible name. `src: Front-end specification, home route 7`
- [ ] `C-FE-75` `constraint` An award caption holds its two authored lines without reflowing. `src: Front-end specification, home route 8`
- [ ] `C-FE-76` `ui` The latest-entries band takes a fixed proportion of its own width above the desktop width. `src: Front-end specification, home route 9`
- [ ] `C-FE-77` `ui` The footer meets the last tile with no gap, no separator. `src: Front-end specification, home route 9`
- [ ] `C-FE-78` `ui` The filter row is draggable below the tablet width, springing back past its start. `src: Front-end specification, archive route`
- [ ] `C-FE-79` `ui` The active filter control holds its fill permanently. `src: Front-end specification, archive route`
- [ ] `C-FE-80` `ui` The mosaic mixes full-width tiles with half-width tiles above the desktop width. `src: Front-end specification, archive route`
- [ ] `C-FE-81` `ui` Below the desktop width every archive tile is full width at a taller proportion. `src: Front-end specification, archive route`
- [ ] `C-FE-82` `constraint` A tile expand grows a layer inside the tile, never the tile itself. `src: Front-end specification, archive route`
- [ ] `C-FE-83` `constraint` An expanding tile moves no tile on a row below the expanding tile. `src: Front-end specification, archive route`
- [ ] `C-FE-84` `ui` An expanding tile fades out its own label control. `src: Front-end specification, archive route`
- [ ] `C-FE-85` `capability` The expanded state is reachable, reversible by keyboard. `src: Front-end specification, archive route`
- [ ] `C-FE-86` `ui` The archive's closing block blends one wash rising from its bottom edge. `src: Front-end specification, archive route`
- [ ] `C-FE-87` `ui` The project opening carries a half-opacity measurement copy hidden from assistive technology. `src: Front-end specification, project detail`
- [ ] `C-FE-88` `ui` Project body media runs at four widths, each subtracting its share of the gap. `src: Front-end specification, project detail`
- [ ] `C-FE-89` `ui` A video player expresses progress as a transform rather than as a width. `src: Front-end specification, project detail`
- [ ] `C-FE-90` `ui` A credit row carries the role on the left, the name on the right, both uppercase. `src: Front-end specification, project detail`
- [ ] `C-FE-91` `ui` A credit row rule is drawn thinner than a hairline. `src: Front-end specification, project detail`
- [ ] `C-FE-92` `ui` The next project is a fixed layer revealed as the main block scrolls off. `src: Front-end specification, project detail`
- [ ] `C-FE-93` `ui` A journal tile carries its date at the top right, its title control at the bottom left. `src: Front-end specification, journal`
- [ ] `C-FE-94` `ui` Above the desktop width a journal tile grows inside its own row. `src: Front-end specification, journal`
- [ ] `C-FE-95` `ui` Below the desktop width a journal tile grows its picture behind a fixed frame. `src: Front-end specification, journal`
- [ ] `C-FE-96` `constraint` A journal tile hover never reflows the rows below the tile. `src: Front-end specification, journal`
- [ ] `C-FE-97` `ui` The journal entry body is the only measured reading column in the product. `src: Front-end specification, journal`
- [ ] `C-FE-98` `ui` A journal body link carries a hairline rule rather than an underline. `src: Front-end specification, journal`
- [ ] `C-FE-99` `constraint` Nothing on the contact route is vertically centred. `src: Front-end specification, contact route`
- [ ] `C-FE-100` `ui` The contact address block is set upright rather than italic. `src: Front-end specification, contact route`
- [ ] `C-FE-101` `ui` The contact band's wordmarks are knocked out of a red block. `src: Front-end specification, contact route`
- [ ] `C-FE-102` `ui` The contact band translates continuously, wrapping by one repeat width. `src: Front-end specification, contact route`
- [ ] `C-FE-103` `ui` The legal column is left-aligned against the gutter rather than centred. `src: Front-end specification, legal routes`
- [ ] `C-FE-104` `ui` The legal column honours the source text's own line breaks. `src: Front-end specification, legal routes`
- [ ] `C-FE-105` `ui` The legal paragraphs are the only justified text in the product. `src: Front-end specification, legal routes`
- [ ] `C-FE-106` `ui` The not-found numerals shear apart along the diagonal. `src: Front-end specification, not-found`
- [ ] `C-FE-107` `ui` The not-found diagonal band pulses faintly rather than holding still. `src: Front-end specification, not-found`
- [ ] `C-FE-108` `literal` The not-found screen reads `Page not found` above a control reading `back home`. `src: Front-end specification, not-found`
- [ ] `C-FE-109` `constraint` The not-found screen carries no footer. `src: Front-end specification, not-found`
- [ ] `C-FE-110` `ui` The denied screen drops the numerals, keeping the diagonal static. `src: Front-end specification, denied screen`
- [ ] `C-FE-111` `constraint` The client area adds no colour, no curve, no spacing step, no type step, no icon. `src: Front-end specification, client area`
- [ ] `C-FE-112` `ui` The sign-in surface is built to the contact route's one-screen shape. `src: Front-end specification, client area`
- [ ] `C-FE-113` `ui` The reel title is edited in place, the field ground appearing only on focus. `src: Front-end specification, client area`
- [ ] `C-FE-114` `ui` A reel row is built as the project navigator's label row. `src: Front-end specification, client area`
- [ ] `C-FE-115` `ui` A dragged reel row lifts above its neighbours as the rows passed translate. `src: Front-end specification, client area`
- [ ] `C-FE-116` `constraint` Per reel row the controls come before the content in the document. `src: Front-end specification, client area`
- [ ] `C-FE-117` `capability` Sending fires the route curtain without a navigation. `src: Front-end specification, client area`
- [ ] `C-FE-118` `ui` A queue row is built as the latest-entries header row repeated. `src: Front-end specification, client area`
- [ ] `C-FE-119` `constraint` The notification strip never becomes a corner card at any width. `src: Front-end specification, client area`
- [ ] `C-FE-120` `ui` The skeleton sweeps the word reveal's own window across its width. `src: Front-end specification, client area`
- [ ] `C-FE-121` `ui` The reel row's drag handle is absent below the desktop width. `src: Front-end specification, responsive table`
- [ ] `C-FE-122` `ui` The client wall steps from three columns to four to six. `src: Front-end specification, responsive table`
- [ ] `C-FE-123` `ui` The awards wall steps from two columns to four. `src: Front-end specification, responsive table`
- [ ] `C-FE-124` `ui` The journal grid steps from one column to two to three. `src: Front-end specification, responsive table`
- [ ] `C-FE-125` `ui` Sign-in rows stay stacked at every width. `src: Front-end specification, responsive table`
- [ ] `C-FE-126` `ui` A short landscape window drops the opening headline a step, keeping the wordmark's width. `src: Front-end specification, responsive`
- [ ] `C-FE-127` `capability` Focus order follows document order on every route. `src: Front-end specification, focus order`
- [ ] `C-FE-128` `constraint` The home navigator comes after the project run in the document. `src: Front-end specification, focus order`
- [ ] `C-FE-129` `constraint` A fixed overlay carrying no action is absent from the focus order. `src: Front-end specification, focus order`
- [ ] `C-FE-130` `capability` The whole reel workflow is reachable without a pointer. `src: Front-end specification, focus order`
- [ ] `C-FE-131` `constraint` The product builds no second grid system. `src: Front-end specification, build these once`
- [ ] `C-FE-132` `constraint` The product builds no modal or dialog layer. `src: Front-end specification, build these once`
- [ ] `C-FE-133` `constraint` The product builds no queue of notifications. `src: Front-end specification, build these once`
- [ ] `C-FE-134` `constraint` The product builds no rich text editor, no spinner, no icon library, no theme switcher. `src: Front-end specification, build these once`
- [ ] `C-FE-135` `literal` The opening headline reads `Creative Innovation` then `and Digital Futures`. `src: Front-end specification, copy, home`
- [ ] `C-FE-136` `literal` The manifesto block carries one sentence about brands being felt, explored, remembered. `src: Front-end specification, copy, home`
- [ ] `C-FE-137` `literal` The practice headline reads `Fields of Practice`. `src: Front-end specification, copy, home`
- [ ] `C-FE-138` `literal` The four practice fields are numbered `01` to `04` with the titles given. `src: Front-end specification, copy, practice table`
- [ ] `C-FE-139` `literal` The four award captions hold their two authored lines each. `src: Front-end specification, copy, home`
- [ ] `C-FE-140` `literal` The twelve client marks are seeded in the order listed. `src: Front-end specification, copy, home`
- [ ] `C-FE-141` `literal` The fifteen projects carry the titles, slugs, subtitles, practice fields listed. `src: Front-end specification, copy, archive table`
- [ ] `C-FE-142` `literal` The ten journal entries carry the titles, slugs, kinds, dates listed. `src: Front-end specification, copy, journal table`
- [ ] `C-FE-143` `literal` The shared closing block reads `The best projects start with a good conversation.` above `Let's talk`. `src: Front-end specification, copy, closing`
- [ ] `C-FE-144` `literal` The archive's closing headline reads `Let's shape what's next in digital together.` `src: Front-end specification, copy, closing`
- [ ] `C-FE-145` `literal` The contact block reads `contact@vesper.works`, `14 Kiln Street`, `E2 8HD London`. `src: Front-end specification, copy, contact`
- [ ] `C-FE-146` `literal` The two social destinations read `Instagram`, `Behance`. `src: Front-end specification, copy, contact`
- [ ] `C-FE-147` `literal` The newsletter placeholder reads `your@email.com` above the control `Subscribe`. `src: Front-end specification, copy, footer`
- [ ] `C-FE-148` `literal` The footer legal links read `Imprint & Privacy` plus `Terms`. `src: Front-end specification, copy, footer`
- [ ] `C-FE-149` `literal` The client area copy strings are used exactly as listed. `src: Front-end specification, copy, client area`
- [ ] `C-FE-150` `ui` Every message is a short declarative sentence with no exclamation mark, no apology, no emoji. `src: Front-end specification, copy, register`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product carries one locale, declared on the document. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The product has no free-text search. `src: Constraints bullet 3`
- [ ] `C-CN-03` `constraint` The product has no visitor-facing sort. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` The product has no filter that intersects with another. `src: Constraints bullet 3`
- [ ] `C-CN-05` `constraint` The public collections return whole rather than paging. `src: Constraints bullet 4`
- [ ] `C-CN-06` `constraint` The product has no messaging, no comments, no likes, no follows. `src: Constraints bullet 6`
- [ ] `C-CN-07` `constraint` The product carries no payment, no price, no currency value. `src: Constraints bullet 7`
- [ ] `C-CN-08` `constraint` The product parses no markup from anything a visitor supplied. `src: Constraints bullet 8`
- [ ] `C-CN-09` `constraint` The product has one theme with no theme switcher. `src: Constraints bullet 10`
- [ ] `C-CN-10` `constraint` The product ships no native application, no installable offline mode. `src: Constraints bullet 11`
- [ ] `C-CN-11` `constraint` The product plays no audio. `src: Constraints bullet 12`
- [ ] `C-CN-12` `constraint` The product loads no third-party measurement tag, no identification pixel. `src: Constraints bullet 13`
- [ ] `C-CN-13` `constraint` The product makes no external network call at run time. `src: Constraints bullet 14`
- [ ] `C-CN-14` `constraint` The product has no administrative console, no role-granting route, no invitation flow. `src: Constraints bullet 15`
- [ ] `C-CN-15` `constraint` The product stays responsive at the stated data volume. `src: Constraints bullet 16`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` Reserved `.browser_screenshots/` directories exist at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` Reserved `.downloads/` directories exist at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` The app serves a production build behind a static or preview server. `src: Deployment contract bullet 7`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-11` `contract` The server binds `0.0.0.0` rather than a loopback address. `src: Deployment contract bullet 9`
- [ ] `C-DC-12` `contract` The app does not download, install, compile or start a copy of a backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-13` `contract` The app uses no edge functions. `src: Deployment contract bullet 11`
- [ ] `C-DC-14` `contract` The app uses no persistent volume, no fixed container name, no custom network. `src: Deployment contract bullet 12`
- [ ] `C-DC-15` `literal` `GET /api/projects` returns a top-level JSON array of published projects. `src: Deployment contract, API shapes row 1`
- [ ] `C-DC-16` `literal` `GET /api/signals` returns a top-level JSON array of published entries, newest first. `src: Deployment contract, API shapes row 3`
- [ ] `C-DC-17` `literal` `POST /api/newsletter` accepts a body carrying `email`. `src: Deployment contract, API shapes row 5`
- [ ] `C-DC-18` `literal` `POST /api/auth/sign-up` accepts `display_name`, `email`, `password`. `src: Deployment contract, API shapes row 6`
- [ ] `C-DC-19` `literal` `GET /api/auth/me` returns the account without a password hash. `src: Deployment contract, API shapes row 9`
- [ ] `C-DC-20` `literal` `GET /api/reel` returns the session's reel with its items in `position` order. `src: Deployment contract, API shapes row 12`
- [ ] `C-DC-21` `literal` `POST /api/reel/items` accepts `project_id`, creating the item at the next position. `src: Deployment contract, API shapes row 14`
- [ ] `C-DC-22` `literal` `PUT /api/reel/order` accepts `order`, the complete array of item identifiers. `src: Deployment contract, API shapes row 17`
- [ ] `C-DC-23` `literal` `POST /api/reel/send` returns the reel in state `sent` with its `sent_at`. `src: Deployment contract, API shapes row 18`
- [ ] `C-DC-24` `literal` `GET /api/studio/reels` returns a top-level JSON array of sent reels newest first. `src: Deployment contract, API shapes row 20`
- [ ] `C-DC-25` `literal` `POST /api/studio/reels/{reel_id}/answer` returns the reel in state `answered`. `src: Deployment contract, API shapes row 22`
- [ ] `C-DC-26` `constraint` A session is required on every path except the public reads, newsletter, sign-up, sign-in, reset, health. `src: Deployment contract, API shapes para after table`
- [ ] `C-DC-27` `constraint` The curator role is required on every studio path. `src: Deployment contract, API shapes para after table`
- [ ] `C-DC-28` `constraint` An invalid or unauthorized call is rejected as a client error, never a `5xx`. `src: Deployment contract, API shapes para after table`
- [ ] `C-DC-29` `constraint` A write against a reel not in state `draft` is refused as a conflict. `src: Deployment contract, API shapes para after table`
- [ ] `C-DC-30` `constraint` Rows held in a process rather than in PostgreSQL are a contract violation. `src: Deployment contract, No mocks para`
- [ ] `C-DC-31` `constraint` A snapshot recomputed from the live reel at read time is a contract violation. `src: Deployment contract, No mocks para`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | seeded password for every account | C-DM-03 | Data model blockquote |
| `client@example.com` | seeded client address | C-RL-19 | User roles seeded table |
| `client2@example.com` | second seeded client address | C-RL-20 | User roles seeded table |
| `client3@example.com` | seeded client at the reel ceiling boundary | C-RL-21 | User roles seeded table |
| `curator@example.com` | seeded curator address | C-RL-22 | User roles seeded table |
| `Nadia Fell` | display name of the first seeded client | C-RL-19 | User roles seeded table |
| `Tomas Renn` | display name of the second seeded client | C-RL-20 | User roles seeded table |
| `Priya Sandoval` | display name of the third seeded client | C-RL-21 | User roles seeded table |
| `Imogen Shaw` | display name of the seeded curator | C-RL-22 | User roles seeded table |
| `client` | the ordinary account role | C-RL-19 | User roles seeded table |
| `curator` | the studio account role | C-RL-22 | User roles seeded table |
| `15` | published project count | C-OV-03 | Overview para 2 |
| `10` | published journal entry count | C-OV-04 | Overview para 2 |
| `30` | session lifetime in days | C-CF-07 | Core features rule 1 |
| `24` | hours after which a session renews | C-CF-08 | Core features rule 1 |
| `1` | lower bound of a display name, a reel title, a version | C-CF-11 | Core features rule 2 |
| `60` | upper bound of a display name in characters | C-CF-11 | Core features rule 2 |
| `8` | lower bound of a password in characters | C-CF-12 | Core features rule 2 |
| `200` | upper bound of a password in characters | C-CF-12 | Core features rule 2 |
| `254` | cap on a stored address in characters | C-CF-13 | Core features rule 2 |
| `That email is already registered` | sign-up refusal for a known address | C-CF-15 | Core features rule 3 |
| `That email and password do not match` | sign-in refusal | C-CF-16 | Core features rule 4 |
| `empty` | reel state before the first add | C-CF-24 | Core features rule 6 |
| `draft` | reel state while it is editable | C-CF-54 | Core features rule 19 |
| `sent` | reel state after a passing send | C-CF-91 | Core features rule 28 |
| `answered` | reel state after a curator picks it up | C-CF-110 | Core features rule 33 |
| `All` | the archive filter that clears the query | C-CF-28 | Core features rule 8 |
| `Brand Identity` | archive filter label | C-CF-28 | Core features rule 8 |
| `Website` | archive filter label | C-CF-28 | Core features rule 8 |
| `Visuals` | archive filter label | C-CF-28 | Core features rule 8 |
| `Extended Reality` | archive filter label | C-CF-28 | Core features rule 8 |
| `brand-identity` | practice field slug | C-CF-31 | Core features rule 8 |
| `website` | practice field slug | C-CF-31 | Core features rule 8 |
| `visuals` | practice field slug | C-CF-31 | Core features rule 8 |
| `extended-reality` | practice field slug | C-CF-31 | Core features rule 8 |
| `?category=<slug>` | the filter query the archive writes | C-CF-30 | Core features rule 8 |
| `Editorial` | journal filter label | C-CF-43 | Core features rule 14 |
| `Events` | journal filter label | C-CF-43 | Core features rule 14 |
| `News` | journal filter label | C-CF-43 | Core features rule 14 |
| `editorial` | journal entry kind | C-CF-44 | Core features rule 14 |
| `events` | journal entry kind | C-CF-44 | Core features rule 14 |
| `news` | journal entry kind | C-CF-44 | Core features rule 14 |
| `DD/MM/YY` | the date format used everywhere | C-CF-45 | Core features rule 15 |
| `Add` | tile control before the project is in the reel | C-CF-50 | Core features rule 17 |
| `Added` | tile control after the project is in the reel | C-CF-50 | Core features rule 17 |
| `12` | the reel item ceiling | C-CF-56 | Core features rule 20 |
| `A reel holds twelve projects at most` | ceiling refusal | C-CF-57 | Core features rule 20 |
| `80` | upper bound of a reel title in characters | C-CF-59 | Core features rule 21 |
| `Untitled reel` | default reel title | C-CF-60 | Core features rule 21 |
| `280` | upper bound of an item note in characters | C-CF-61 | Core features rule 21 |
| `2000` | upper bound of a reel brief in characters | C-CF-62 | Core features rule 21 |
| `800` | idle milliseconds before an autosave | C-CF-63 | Core features rule 21 |
| `80%` | share of a limit at which a counter appears | C-CF-65 | Core features rule 22 |
| `300` | long-press milliseconds before a touch drag | C-CF-71 | Core features rule 23 |
| `<project title> moved to position <n> of <total>` | reorder announcement | C-CF-72 | Core features rule 23 |
| `Removed.` | strip message after a remove | C-CF-78 | Core features rule 25 |
| `Retry` | strip control offering another attempt | C-CF-78 | Core features rule 25 |
| `5` | seconds a strip message dwells | C-CF-78 | Core features rule 25 |
| `3` | seconds allowed for a second press | C-CF-79 | Core features rule 26 |
| `Press again` | label of a control awaiting its second press | C-CF-79 | Core features rule 26 |
| `Add at least one project` | send refusal for an empty reel | C-CF-84 | Core features rule 27 |
| `Give the reel a name` | send refusal for a blank title | C-CF-85 | Core features rule 27 |
| `The brief is too long` | send refusal for an over-long brief | C-CF-86 | Core features rule 27 |
| `A note is too long` | send refusal for an over-long note | C-CF-87 | Core features rule 27 |
| `One of your projects is no longer available` | send refusal for a withdrawn project | C-CF-88 | Core features rule 27 |
| `This reel has already been sent` | send refusal for a non-draft reel | C-CF-89 | Core features rule 27 |
| `Sent` | the block replacing the send control | C-CF-94 | Core features rule 28 |
| `Reopen` | the control returning a sent reel to draft | C-CF-94 | Core features rule 28 |
| `Reopened. The studio no longer sees it.` | strip message after a reopen | C-CF-100 | Core features rule 30 |
| `No reels waiting` | empty studio queue line | C-CF-106 | Core features rule 31 |
| `Mark answered` | the control a curator presses | C-CF-108 | Core features rule 32 |
| `The studio has your reel` | the answered notice | C-CF-111 | Core features rule 33 |
| `Could not reorder. Put back.` | strip message after a failed reorder | C-CF-117 | Core features rule 36 |
| `Could not add that.` | strip message after a failed add | C-CF-118 | Core features rule 36 |
| `Not saved.` | strip message after a failed text write | C-CF-122 | Core features rule 37 |
| `Thanks for subscribing` | newsletter success block | C-CF-137 | Core features rule 43 |
| `Something went wrong` | newsletter default failure | C-CF-138 | Core features rule 43 |
| `15` | minutes between reset requests for one address | C-CF-144 | Core features rule 46 |
| `Vesper: your reel` | welcome message subject | C-CF-146 | Core features rule 47 |
| `Vesper: reset your password` | reset message subject | C-CF-147 | Core features rule 47 |
| `Vesper: we have your reel` | client send confirmation subject | C-CF-148 | Core features rule 47 |
| `New reel from <display name>` | studio notice subject | C-CF-149 | Core features rule 47 |
| `contact@vesper.works` | the studio enquiry address | C-CF-149 | Core features rule 47 |
| `length_bucket` | the note-length property recorded | C-CF-160 | Core features rule 50 |
| `short` | a note length bucket | C-CF-160 | Core features rule 50 |
| `medium` | a note length bucket | C-CF-160 | Core features rule 50 |
| `long` | a note length bucket | C-CF-160 | Core features rule 50 |
| `surface` | the property carried by a project opening | C-CF-157 | Core features rule 49 |
| `/legal/imprint-privacy-policy` | the imprint and privacy route | C-CF-165 | Core features rule 53 |
| `/legal/terms` | the terms route | C-CF-167 | Core features rule 53 |
| `Vesper - Creative Innovation and Digital Futures` | the home route title | C-CF-173 | Core features rule 56 |
| `Our Portfolio - Vesper` | the archive route title | C-CF-173 | Core features rule 56 |
| `Signals` | the journal route title | C-CF-173 | Core features rule 56 |
| `Your reel - Vesper` | the reel route title | C-CF-173 | Core features rule 56 |
| `PROJECTS` | first navigation label | C-UF-02 | User flow para after table |
| `SIGNALS` | second navigation label | C-UF-02 | User flow para after table |
| `CONTACT` | third navigation label | C-UF-02 | User flow para after table |
| `/work` | the archive address | C-UF-02 | User flow route table |
| `/blog` | the journal address | C-UF-02 | User flow route table |
| `/contact` | the contact address | C-UF-02 | User flow route table |
| `/sign-in` | the identity address | C-UF-03 | User flow, Entry and redirects |
| `/reel` | the client's own reel address | C-UF-09 | User flow, Entry and redirects |
| `/studio/reels` | the curator queue address | C-UF-10 | User flow, Entry and redirects |
| `Not your reel` | the denied screen line | C-UF-06 | User flow, Entry and redirects |
| `back to yours` | the denied screen control | C-UF-06 | User flow, Entry and redirects |
| `Sign in to start a reel` | the signed-out reel line | C-UF-08 | User flow, Entry and redirects |
| `Sign in` | the signed-out reel control | C-UF-08 | User flow, Entry and redirects |
| `No projects in this field` | the filtered archive empty line | C-UF-15 | User flow, States |
| `Show all projects` | the filtered archive empty control | C-UF-15 | User flow, States |
| `No entries of this kind` | the filtered journal empty line | C-UF-16 | User flow, States |
| `Show all entries` | the filtered journal empty control | C-UF-16 | User flow, States |
| `Your reel is empty` | the empty reel line | C-UF-17 | User flow, States |
| `Browse projects` | the empty reel control | C-UF-17 | User flow, States |
| `Could not load this` | the failed load line | C-UF-20 | User flow, States |
| `Try again` | the failed load control | C-UF-20 | User flow, States |
| `No longer available` | the lost-project row line | C-UF-21 | User flow, States |
| `You are offline` | the offline bar line | C-UF-22 | User flow, States |
| `You are offline. Changes will be saved.` | the offline bar line while a write is held | C-UF-23 | User flow, States |
| `Could not send. Your reel is safe.` | the offline send refusal | C-UF-25 | User flow, States |
| `DATABASE_URL` | the datastore variable | C-TR-05 | Technical requirements para 2 |
| `APP_PUBLIC_URL` | the public address variable | C-TR-06 | Technical requirements para 2 |
| `APP_PUBLIC_PORT` | the public port variable | C-TR-06 | Technical requirements para 2 |
| `Shell` | contact object part prefix | C-TR-16 | Technical requirements para 9 |
| `WindShield` | contact object part prefix | C-TR-16 | Technical requirements para 9 |
| `Vent` | contact object part prefix | C-TR-16 | Technical requirements para 9 |
| `Sticker` | contact object part prefix | C-TR-16 | Technical requirements para 9 |
| `Trim` | contact object part prefix | C-TR-16 | Technical requirements para 9 |
| `200` | the health response status | C-TR-08 | Technical requirements para 4 |
| `Projects` | home section label above the project run | C-FE-34 | Front-end specification, section label |
| `Services` | home section label above the practice fields | C-FE-34 | Front-end specification, section label |
| `Clients` | home section label above the client wall | C-FE-34 | Front-end specification, section label |
| `Awards` | home section label above the awards wall | C-FE-34 | Front-end specification, section label |
| `Latest Signals` | home section label above the recent entries | C-FE-34 | Front-end specification, section label |
| `Newsletter` | footer section label | C-FE-34 | Front-end specification, section label |
| `Work` | archive section label | C-FE-34 | Front-end specification, section label |
| `Blog` | journal section label | C-FE-34 | Front-end specification, section label |
| `Your reel` | reel section label | C-FE-34 | Front-end specification, section label |
| `Reels` | studio queue section label | C-FE-34 | Front-end specification, section label |
| `Creative Innovation` | first line of the opening headline | C-FE-135 | Front-end specification, copy |
| `and Digital Futures` | second line of the opening headline | C-FE-135 | Front-end specification, copy |
| `The future of digital belongs to brands that are felt, explored and remembered.` | the manifesto sentence | C-FE-136 | Front-end specification, copy |
| `Fields of Practice` | the practice headline | C-FE-137 | Front-end specification, copy |
| `01` | first practice field numeral | C-FE-138 | Front-end specification, copy |
| `04` | fourth practice field numeral | C-FE-138 | Front-end specification, copy |
| `The best projects start with a good conversation.` | the shared closing headline | C-FE-143 | Front-end specification, copy |
| `Let's talk` | the shared closing control | C-FE-143 | Front-end specification, copy |
| `Let's shape what's next in digital together.` | the archive closing headline | C-FE-144 | Front-end specification, copy |
| `14 Kiln Street` | the studio street line | C-FE-145 | Front-end specification, copy |
| `E2 8HD London` | the studio postcode line | C-FE-145 | Front-end specification, copy |
| `Instagram` | first social destination | C-FE-146 | Front-end specification, copy |
| `Behance` | second social destination | C-FE-146 | Front-end specification, copy |
| `your@email.com` | the newsletter placeholder | C-FE-147 | Front-end specification, copy |
| `Subscribe` | the newsletter control | C-FE-147 | Front-end specification, copy |
| `Imprint & Privacy` | the footer privacy link | C-FE-148 | Front-end specification, copy |
| `Terms` | the footer terms link | C-FE-148 | Front-end specification, copy |
| `Page not found` | the not-found line | C-FE-108 | Front-end specification, not-found |
| `back home` | the not-found control | C-FE-108 | Front-end specification, not-found |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | C-DC-02 | Deployment contract bullet 1 |
| `/api` | the API prefix | C-DC-03 | Deployment contract bullet 2 |
| `GET /api/health` | the health route | C-DC-04 | Deployment contract bullet 3 |
| `/app/USER_README.md` | the credentials file | C-DC-06 | Deployment contract bullet 5 |
| `.browser_screenshots/` | a reserved directory | C-DC-07 | Deployment contract bullet 6 |
| `.downloads/` | a reserved directory | C-DC-08 | Deployment contract bullet 6 |
| `0.0.0.0` | the bind address | C-DC-11 | Deployment contract bullet 9 |
| `GET /api/projects` | the project collection path | C-DC-15 | API shapes row 1 |
| `GET /api/signals` | the journal collection path | C-DC-16 | API shapes row 3 |
| `POST /api/newsletter` | the subscribe path | C-DC-17 | API shapes row 5 |
| `email` | the newsletter request field | C-DC-17 | API shapes row 5 |
| `POST /api/auth/sign-up` | the account creation path | C-DC-18 | API shapes row 6 |
| `display_name` | the sign-up display name field | C-DC-18 | API shapes row 6 |
| `password` | the sign-up password field | C-DC-18 | API shapes row 6 |
| `GET /api/auth/me` | the session identity path | C-DC-19 | API shapes row 9 |
| `GET /api/reel` | the client reel path | C-DC-20 | API shapes row 12 |
| `position` | the reel item order field | C-DC-20 | API shapes row 12 |
| `POST /api/reel/items` | the add path | C-DC-21 | API shapes row 14 |
| `project_id` | the add request field | C-DC-21 | API shapes row 14 |
| `PUT /api/reel/order` | the reorder path | C-DC-22 | API shapes row 17 |
| `order` | the reorder request field | C-DC-22 | API shapes row 17 |
| `POST /api/reel/send` | the send path | C-DC-23 | API shapes row 18 |
| `sent_at` | the send timestamp field | C-DC-23 | API shapes row 18 |
| `GET /api/studio/reels` | the queue path | C-DC-24 | API shapes row 20 |
| `POST /api/studio/reels/{reel_id}/answer` | the answer path | C-DC-25 | API shapes row 22 |
| `5xx` | the status class a rejection never uses | C-DC-28 | API shapes para after table |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the twenty named events | C-CF-156 | the names are listed in prose but no canonical casing table pins them |
| the four counts kept regardless of consent | C-CF-164 | named in prose, with no field names given |
| the stated data volume | C-CN-15 | the queue bound is given as a few hundred rather than as a number |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 5 | 7 |
| User roles | 18 | 23 |
| Core features | 150 | 173 |
| User flow | 22 | 28 |
| UI/UX notes | 40 | 51 |
| Technical requirements | 26 | 30 |
| Data model | 26 | 30 |
| Front-end specification | 130 | 150 |
| Constraints | 14 | 15 |
| Deployment contract | 28 | 31 |
