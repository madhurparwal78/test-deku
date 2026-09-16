# Checklist: Doodlerush

Items: 340
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC
Unpinned values flagged: 3

Every item restates one obligation of `instruction.md`. Nothing here adds a requirement the brief does not carry.

## C-OV Overview

- [ ] `C-OV-01` `capability` Doodlerush is a browser party game where one player draws a secret word `src: Overview`
- [ ] `C-OV-02` `capability` Every player who is not the drawer races to type the word into the chat `src: Overview`
- [ ] `C-OV-03` `capability` Playing requires no account, no download, no payment `src: Overview`
- [ ] `C-OV-04` `capability` A public room is reachable only through matchmaking `src: Overview`
- [ ] `C-OV-05` `capability` A private room is reachable only through an eight-character code `src: Overview`
- [ ] `C-OV-06` `constraint` No room of either kind is listed anywhere in the product `src: Overview`
- [ ] `C-OV-07` `capability` An account adds a reserved display name, owned-room settings, the report queue `src: Overview`
- [ ] `C-OV-08` `capability` The drawer's copy of the room carries the word, every other copy carries a mask `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `contract` Authorization is enforced server-side on every mutating endpoint `src: User roles`
- [ ] `C-RL-02` `contract` A denied request leaves the protected state unchanged `src: User roles`
- [ ] `C-RL-03` `role` A guest plays without an account `src: User roles`
- [ ] `C-RL-04` `role` A guest cannot read the report queue `src: User roles`
- [ ] `C-RL-05` `role` A `player` cannot read the report queue `src: User roles`
- [ ] `C-RL-06` `role` A `player` cannot mark a report reviewed `src: User roles`
- [ ] `C-RL-07` `role` A `moderator` reads the report queue `src: User roles`
- [ ] `C-RL-08` `role` A `moderator` cannot read the current word of any room `src: User roles`
- [ ] `C-RL-09` `capability` Signup is open to any visitor `src: User roles`
- [ ] `C-RL-10` `capability` The `moderator` role is granted only by seeding `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `contract` Email plus password exchange for a bearer token sent on every signed-in request `src: Core features`
- [ ] `C-CF-02` `contract` A missing, malformed, expired bearer token is denied `src: Core features`
- [ ] `C-CF-03` `capability` Signup on an address already registered is rejected as invalid `src: Core features`
- [ ] `C-CF-04` `capability` A rejected signup creates no account `src: Core features`
- [ ] `C-CF-05` `contract` Passwords are stored hashed `src: Core features`
- [ ] `C-CF-06` `literal` The literal `deku-demo-pw-2026` works at login for every seeded account `src: Core features`
- [ ] `C-CF-07` `literal` A bearer token expires `24h` after issue `src: Core features`
- [ ] `C-CF-08` `contract` A seat token is a separate credential from a bearer token `src: Core features`
- [ ] `C-CF-09` `contract` A bearer token does not admit a holder to a room `src: Core features`
- [ ] `C-CF-10` `literal` A display name is `1` to `16` characters `src: Core features`
- [ ] `C-CF-11` `capability` A name outside the length band is rejected inline with the field named `src: Core features`
- [ ] `C-CF-12` `capability` A rejected name creates nothing `src: Core features`
- [ ] `C-CF-13` `capability` The language control selects the word list rather than the interface language `src: Core features`
- [ ] `C-CF-14` `literal` The seeded word-list language is `English` `src: Core features`
- [ ] `C-CF-15` `capability` An avatar is assembled from four independently chosen layers `src: Core features`
- [ ] `C-CF-16` `capability` One control sets all four avatar layers at random `src: Core features`
- [ ] `C-CF-17` `capability` An avatar is fixed for the session once a player joins `src: Core features`
- [ ] `C-CF-18` `capability` The primary action joins a public room by matchmaking `src: Core features`
- [ ] `C-CF-19` `capability` The secondary action opens `/create` `src: Core features`
- [ ] `C-CF-20` `ui` The primary action is larger, more prominent than the secondary action `src: Core features`
- [ ] `C-CF-21` `capability` A how-to-play panel states five steps in a fixed order `src: Core features`
- [ ] `C-CF-22` `capability` The rule against writing the word is enforced by the server, not only stated `src: Core features`
- [ ] `C-CF-23` `capability` A privacy page at `/privacy` states what Doodlerush stores `src: Core features`
- [ ] `C-CF-24` `ui` The privacy page is linked from the footer of every page `src: Core features`
- [ ] `C-CF-25` `capability` A terms page at `/terms` carries a contact address at the head `src: Core features`
- [ ] `C-CF-26` `ui` Every internal link on every public route resolves to a page the app serves `src: Core features`
- [ ] `C-CF-27` `capability` An unknown address renders the product's own not-found page `src: Core features`
- [ ] `C-CF-28` `capability` The not-found page answers not-found rather than serving the landing route `src: Core features`
- [ ] `C-CF-29` `data` A room is `public` or `private` `src: Core features`
- [ ] `C-CF-30` `constraint` No endpoint returns a set of live rooms `src: Core features`
- [ ] `C-CF-31` `capability` A request for a room list is answered not-found rather than with an empty list `src: Core features`
- [ ] `C-CF-32` `capability` A caller holding neither a seat nor the code cannot learn a room's name `src: Core features`
- [ ] `C-CF-33` `capability` A caller holding neither a seat nor the code cannot learn a room's player count `src: Core features`
- [ ] `C-CF-34` `capability` A caller holding neither a seat nor the code cannot learn whether a room exists `src: Core features`
- [ ] `C-CF-35` `capability` A signed-in `player` without a seat calling the state endpoint for `PARROT42` is denied `src: Core features`
- [ ] `C-CF-36` `literal` A room code is `8` characters `src: Core features`
- [ ] `C-CF-37` `data` A room code uses an alphabet with no lookalike characters `src: Core features`
- [ ] `C-CF-38` `constraint` A room code is never sequential, never derived from a counter `src: Core features`
- [ ] `C-CF-39` `capability` A room code collision is regenerated `src: Core features`
- [ ] `C-CF-40` `literal` A room code is retired for `1h` after the room closes `src: Core features`
- [ ] `C-CF-41` `capability` Creating a private room returns the code, the name, the invite link `src: Core features`
- [ ] `C-CF-42` `capability` An invite link opens the room route without joining the visitor directly `src: Core features`
- [ ] `C-CF-43` `capability` An invite link always stops at the name step `src: Core features`
- [ ] `C-CF-44` `capability` Matchmaking places a player in the fullest room that is not full `src: Core features`
- [ ] `C-CF-45` `capability` Matchmaking never places a player in a room at `game_end` `src: Core features`
- [ ] `C-CF-46` `capability` Matchmaking never places a player in a room more than half through a round `src: Core features`
- [ ] `C-CF-47` `capability` Matchmaking is partitioned by the room's word-list language `src: Core features`
- [ ] `C-CF-48` `capability` A new room is created only when no eligible room exists `src: Core features`
- [ ] `C-CF-49` `capability` Two joins racing for the last seat produce exactly one join `src: Core features`
- [ ] `C-CF-50` `capability` The loser of a join race is offered another room rather than an error `src: Core features`
- [ ] `C-CF-51` `literal` The seeded room `Friday Night Doodles` carries a player cap of `4` `src: Core features`
- [ ] `C-CF-52` `capability` A room never holds more players than the cap `src: Core features`
- [ ] `C-CF-53` `capability` A failed join leaves no seat held, no partial player record `src: Core features`
- [ ] `C-CF-54` `capability` The host is the room's creator, or the first player in a matchmade room `src: Core features`
- [ ] `C-CF-55` `capability` The longest-present connected player becomes host when the host leaves `src: Core features`
- [ ] `C-CF-56` `capability` Host migration happens immediately without anybody acting `src: Core features`
- [ ] `C-CF-57` `capability` The room is told who the host now is `src: Core features`
- [ ] `C-CF-58` `literal` The player cap setting ranges `2` to `20`, defaulting to `8` `src: Core features`
- [ ] `C-CF-59` `literal` The round count setting ranges `2` to `10`, defaulting to `3` `src: Core features`
- [ ] `C-CF-60` `literal` The turn length setting ranges `30` to `180` seconds, defaulting to `80` `src: Core features`
- [ ] `C-CF-61` `literal` The word-choice setting ranges `1` to `5`, defaulting to `3` `src: Core features`
- [ ] `C-CF-62` `literal` The hint setting ranges `0` to `5`, defaulting to `2` `src: Core features`
- [ ] `C-CF-63` `data` The word mode is `normal`, `hidden`, `combination`, defaulting to `normal` `src: Core features`
- [ ] `C-CF-64` `capability` An out-of-range settings change is rejected, changing nothing `src: Core features`
- [ ] `C-CF-65` `capability` A settings change from a player who is not the host is rejected `src: Core features`
- [ ] `C-CF-66` `capability` A settings change after the game starts is rejected `src: Core features`
- [ ] `C-CF-67` `constraint` Settings do not change between the start, the end of a game `src: Core features`
- [ ] `C-CF-68` `literal` A room with no players is retained for `60s` `src: Core features`
- [ ] `C-CF-69` `capability` A retained room resumes with the standings, the settings kept `src: Core features`
- [ ] `C-CF-70` `capability` A room below two players mid-game returns to `lobby` `src: Core features`
- [ ] `C-CF-71` `literal` A room older than `6h` is closed with notice `src: Core features`
- [ ] `C-CF-72` `data` A room is in exactly one of six states `src: Core features`
- [ ] `C-CF-73` `contract` Every state transition is the server's decision `src: Core features`
- [ ] `C-CF-74` `constraint` No endpoint accepts an award, a turn advance, a timer value from a client `src: Core features`
- [ ] `C-CF-75` `constraint` No endpoint accepts a client claim that a guess was correct `src: Core features`
- [ ] `C-CF-76` `capability` A game starts only when at least `2` players are present `src: Core features`
- [ ] `C-CF-77` `literal` The word-choice window lasts `15s` `src: Core features`
- [ ] `C-CF-78` `capability` The server chooses a word when the choice window expires `src: Core features`
- [ ] `C-CF-79` `capability` A drawer leaving before choosing ends the turn `src: Core features`
- [ ] `C-CF-80` `capability` A turn ends the instant every non-drawer has guessed correctly `src: Core features`
- [ ] `C-CF-81` `literal` The reveal interval at turn end lasts `6s` `src: Core features`
- [ ] `C-CF-82` `literal` The standings interval at game end lasts `12s` `src: Core features`
- [ ] `C-CF-83` `capability` A game returns to `lobby` with standings cleared, settings kept `src: Core features`
- [ ] `C-CF-84` `capability` A round is one turn per player in a fixed order `src: Core features`
- [ ] `C-CF-85` `constraint` The drawer is never picked at random per turn `src: Core features`
- [ ] `C-CF-86` `capability` A player joining mid-round enters the order at the next round `src: Core features`
- [ ] `C-CF-87` `capability` A player leaving is removed from the order, shortening the round `src: Core features`
- [ ] `C-CF-88` `capability` Over four rounds with four players everybody draws four times `src: Core features`
- [ ] `C-CF-89` `contract` The server computes an absolute deadline, sending the deadline to clients `src: Core features`
- [ ] `C-CF-90` `constraint` No client tells the server that time is up `src: Core features`
- [ ] `C-CF-91` `literal` A client measures its clock offset every `30s` `src: Core features`
- [ ] `C-CF-92` `capability` A client recomputes the countdown from the deadline when the tab is focused `src: Core features`
- [ ] `C-CF-93` `capability` A player may opt out of drawing turns, staying in the room `src: Core features`
- [ ] `C-CF-94` `contract` The current word reaches the current drawer only, until the turn ends `src: Core features`
- [ ] `C-CF-95` `constraint` The word is never sent scrambled, never sent with a hide flag `src: Core features`
- [ ] `C-CF-96` `contract` The room snapshot is built per recipient `src: Core features`
- [ ] `C-CF-97` `data` The drawer's snapshot carries `word` with the real word `src: Core features`
- [ ] `C-CF-98` `data` A non-drawer's snapshot omits `word`, carrying `word_mask` `src: Core features`
- [ ] `C-CF-99` `capability` No event a non-drawer receives contains the word `src: Core features`
- [ ] `C-CF-100` `data` The mask shows one placeholder per character, spaces shown literally `src: Core features`
- [ ] `C-CF-101` `capability` The mask counts characters rather than bytes `src: Core features`
- [ ] `C-CF-102` `capability` Hints are sent by the server at the moment each hint is due `src: Core features`
- [ ] `C-CF-103` `constraint` The hint schedule is never sent to a client `src: Core features`
- [ ] `C-CF-104` `literal` Letters are revealed at `50%`, `75%` of the turn elapsed `src: Core features`
- [ ] `C-CF-105` `capability` Never more than half the letters of a word are revealed `src: Core features`
- [ ] `C-CF-106` `capability` A correct guess is announced with the guesser, never the text typed `src: Core features`
- [ ] `C-CF-107` `constraint` No response carries the word list, the upcoming words, the seed `src: Core features`
- [ ] `C-CF-108` `constraint` No response carries another player's seat token `src: Core features`
- [ ] `C-CF-109` `constraint` No response carries any player's network address `src: Core features`
- [ ] `C-CF-110` `data` A guess returns an outcome of `correct`, `close`, `chat` `src: Core features`
- [ ] `C-CF-111` `capability` A guess from the current drawer is rejected `src: Core features`
- [ ] `C-CF-112` `capability` A guess from a player who already guessed correctly is rejected `src: Core features`
- [ ] `C-CF-113` `literal` Guesses are limited to `4` per `2s` per player `src: Core features`
- [ ] `C-CF-114` `literal` Guess text beyond `100` characters is rejected `src: Core features`
- [ ] `C-CF-115` `capability` Normalization is applied identically to the guess, to the word `src: Core features`
- [ ] `C-CF-116` `capability` A guess typed without an accent matches the accented word `src: Core features`
- [ ] `C-CF-117` `literal` A near-miss is an edit distance of `1` against a word of `5` characters or more `src: Core features`
- [ ] `C-CF-118` `capability` A near-miss reaches the guesser alone, never the room `src: Core features`
- [ ] `C-CF-119` `capability` A near-miss message does not repeat the guess back `src: Core features`
- [ ] `C-CF-120` `constraint` A correct guess is never echoed to the room as chat `src: Core features`
- [ ] `C-CF-121` `capability` A player who guessed correctly is routed to a separate chat channel `src: Core features`
- [ ] `C-CF-122` `capability` The separate channel reaches other correct guessers plus the drawer only `src: Core features`
- [ ] `C-CF-123` `capability` A drawer message containing the word is rejected, told to the drawer alone `src: Core features`
- [ ] `C-CF-124` `capability` Simultaneous correct guesses are ordered by server arrival stamp `src: Core features`
- [ ] `C-CF-125` `literal` A correct guess earns an award decaying linearly from `500` to `50` `src: Core features`
- [ ] `C-CF-126` `contract` The award basis is the server's arrival stamp, never a client time `src: Core features`
- [ ] `C-CF-127` `literal` The drawer's award is each guesser's award divided by the non-drawer count, capped at `500` `src: Core features`
- [ ] `C-CF-128` `capability` Nobody is awarded when nobody guesses `src: Core features`
- [ ] `C-CF-129` `capability` Nobody is awarded when the drawer leaves mid-turn `src: Core features`
- [ ] `C-CF-130` `literal` A guess arriving within `250ms` after the deadline is accepted `src: Core features`
- [ ] `C-CF-131` `capability` Standings sort by award descending, then by earliest join `src: Core features`
- [ ] `C-CF-132` `constraint` Standings update at turn end, never during a turn `src: Core features`
- [ ] `C-CF-133` `contract` The wire carries stroke geometry, never pixels `src: Core features`
- [ ] `C-CF-134` `constraint` A whole-canvas image is forbidden on the wire `src: Core features`
- [ ] `C-CF-135` `constraint` A changed-region image is forbidden on the wire `src: Core features`
- [ ] `C-CF-136` `data` Colour travels as an index into the fixed palette `src: Core features`
- [ ] `C-CF-137` `data` Brush width travels as an index rather than a pixel width `src: Core features`
- [ ] `C-CF-138` `literal` Stroke coordinates are normalized to the range `0` to `1` at `4` decimal places `src: Core features`
- [ ] `C-CF-139` `capability` The server retains the ordered stroke list for the current turn `src: Core features`
- [ ] `C-CF-140` `capability` A player joining mid-turn receives the stroke list inside the snapshot `src: Core features`
- [ ] `C-CF-141` `capability` The stroke buffer is discarded at turn end `src: Core features`
- [ ] `C-CF-142` `literal` A turn accepts at most `4000` strokes `src: Core features`
- [ ] `C-CF-143` `data` A canvas operation is `undo`, `clear`, `fill` `src: Core features`
- [ ] `C-CF-144` `capability` Undo removes the last stroke by the drawer in the current turn `src: Core features`
- [ ] `C-CF-145` `capability` A fill produces the same result on every device in the room `src: Core features`
- [ ] `C-CF-146` `literal` A fill covering more than `95%` of the canvas is rejected `src: Core features`
- [ ] `C-CF-147` `literal` A drawer sends at most `60` stroke batches per second `src: Core features`
- [ ] `C-CF-148` `literal` A turn accepts at most `20` canvas operations `src: Core features`
- [ ] `C-CF-149` `capability` A stroke from anybody but the current drawer is rejected server-side `src: Core features`
- [ ] `C-CF-150` `capability` A repeated stroke identifier is dropped `src: Core features`
- [ ] `C-CF-151` `capability` A repeated guess is scored once per player per turn `src: Core features`
- [ ] `C-CF-152` `capability` The first word choice wins, later choices are ignored `src: Core features`
- [ ] `C-CF-153` `contract` A seat token is opaque, high-entropy, never guessable `src: Core features`
- [ ] `C-CF-154` `literal` A seat token lasts `24h` from last use `src: Core features`
- [ ] `C-CF-155` `capability` Reconnecting restores the seat with the standing award, the display name `src: Core features`
- [ ] `C-CF-156` `capability` Reconnecting restores the already-guessed mark for the current turn `src: Core features`
- [ ] `C-CF-157` `capability` A returning player who already guessed cannot guess again `src: Core features`
- [ ] `C-CF-158` `literal` A seat is held `45s` after an unexpected disconnection `src: Core features`
- [ ] `C-CF-159` `ui` A disconnected player is shown as present but disconnected `src: Core features`
- [ ] `C-CF-160` `capability` An explicit leave releases the seat at once `src: Core features`
- [ ] `C-CF-161` `capability` A disconnecting drawer ends the turn immediately, the seat still held `src: Core features`
- [ ] `C-CF-162` `capability` A duplicate display name in a room is suffixed by the server `src: Core features`
- [ ] `C-CF-163` `literal` A display name changes at most `3` times per room `src: Core features`
- [ ] `C-CF-164` `capability` A second join on one seat token displaces the older connection `src: Core features`
- [ ] `C-CF-165` `capability` A displaced connection is told plainly that the session moved `src: Core features`
- [ ] `C-CF-166` `literal` A word list holds at least `2000` entries per language `src: Core features`
- [ ] `C-CF-167` `data` Every word entry is tagged `easy`, `medium`, `hard` `src: Core features`
- [ ] `C-CF-168` `constraint` A word entry is a concrete drawable noun `src: Core features`
- [ ] `C-CF-169` `capability` The drawer alone receives the offered words `src: Core features`
- [ ] `C-CF-170` `capability` A word already used in the current game is never offered again `src: Core features`
- [ ] `C-CF-171` `literal` A custom word is `1` to `100` characters `src: Core features`
- [ ] `C-CF-172` `literal` A room accepts at most `500` custom words `src: Core features`
- [ ] `C-CF-173` `literal` Custom-words-only requires at least `10` words `src: Core features`
- [ ] `C-CF-174` `capability` Custom words are scoped to one room, never kept beyond the room `src: Core features`
- [ ] `C-CF-175` `capability` The filter matches on normalized text `src: Core features`
- [ ] `C-CF-176` `capability` A filtered name is rejected at entry with a reason `src: Core features`
- [ ] `C-CF-177` `capability` A filtered chat message is dropped, told to the sender alone `src: Core features`
- [ ] `C-CF-178` `capability` A guess matching the filter is still evaluated as a guess `src: Core features`
- [ ] `C-CF-179` `literal` An address opens at most `8` concurrent connections `src: Core features`
- [ ] `C-CF-180` `literal` An address makes at most `20` joins per minute `src: Core features`
- [ ] `C-CF-181` `literal` An address creates at most `5` rooms per minute `src: Core features`
- [ ] `C-CF-182` `literal` A message beyond `8KB` closes the connection `src: Core features`
- [ ] `C-CF-183` `capability` Exceeding an in-room limit produces a message rather than a disconnection `src: Core features`
- [ ] `C-CF-184` `literal` A kicked player cannot rejoin that room for `10m` `src: Core features`
- [ ] `C-CF-185` `literal` A vote expires after `60s` `src: Core features`
- [ ] `C-CF-186` `capability` A majority vote ends the current turn early, awarding nobody `src: Core features`
- [ ] `C-CF-187` `constraint` Drawn content is never judged automatically `src: Core features`
- [ ] `C-CF-188` `literal` A player files at most `3` reports per hour `src: Core features`
- [ ] `C-CF-189` `data` A report captures the stroke buffer rather than a rendered picture `src: Core features`
- [ ] `C-CF-190` `literal` A report is kept `30d`, then deleted `src: Core features`
- [ ] `C-CF-191` `capability` The report queue is readable by a `moderator` alone `src: Core features`
- [ ] `C-CF-192` `constraint` No player is acted against automatically on a behavioural signal `src: Core features`
- [ ] `C-CF-193` `capability` A mute hides the muted player's chat for the muting player alone `src: Core features`
- [ ] `C-CF-194` `constraint` A mute is never announced to the room `src: Core features`
- [ ] `C-CF-195` `constraint` The like control, the dislike control change no award `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `capability` The landing route is reachable without an account `src: User flow`
- [ ] `C-UF-02` `capability` The route `/create` is reachable without an account `src: User flow`
- [ ] `C-UF-03` `capability` The route `/account` requires an account `src: User flow`
- [ ] `C-UF-04` `capability` The route `/reports` requires the `moderator` role `src: User flow`
- [ ] `C-UF-05` `capability` An unauthenticated request for `/account` goes to `/login` `src: User flow`
- [ ] `C-UF-06` `capability` The original destination is restored after a successful sign in `src: User flow`
- [ ] `C-UF-07` `capability` A signed-in `player` requesting `/reports` is refused rather than redirected `src: User flow`
- [ ] `C-UF-08` `capability` A refused report request carries no queue in the response `src: User flow`
- [ ] `C-UF-09` `capability` Signing out ends the account session, leaving a seat token valid `src: User flow`
- [ ] `C-UF-10` `capability` A room route for a code that is not live answers not-found `src: User flow`
- [ ] `C-UF-11` `capability` A visitor joins a public room in one press from the landing route `src: User flow`
- [ ] `C-UF-12` `capability` Creating a private room lands on a full-page confirmation `src: User flow`
- [ ] `C-UF-13` `ui` The confirmation names the room, showing the code plus the invite link `src: User flow`
- [ ] `C-UF-14` `ui` The confirmation offers a control that copies the invite link `src: User flow`
- [ ] `C-UF-15` `ui` Every list carries an empty state `src: User flow`
- [ ] `C-UF-16` `ui` The loading overlay names the step rather than spinning silently `src: User flow`

## C-UX UI/UX notes

- [ ] `C-UX-01` `ui` The interface derives every dimension from one layout unit `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The page ground is a deep, soft blue tiled with hand-drawn doodles `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Panels are translucent so the doodle ground shows through `src: UI/UX notes`
- [ ] `C-UX-04` `ui` A near-miss wears a mid, vivid amber worn by nothing else `src: UI/UX notes`
- [ ] `C-UX-05` `ui` A player row turns a light, vivid green once that player has guessed `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Keyboard focus is a light, vivid orange that is never removed `src: UI/UX notes`
- [ ] `C-UX-07` `literal` Type is `Nunito` with a stated fallback stack `src: UI/UX notes`
- [ ] `C-UX-08` `literal` Body text sets at `16px`, controls at `14px` `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Shadows are hard, offset, unblurred everywhere but the avatar arrows `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Motion is springy, overshooting then settling `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Nothing responds more slowly than about an eighth of a second `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Reduced motion stills every animation except the countdown `src: UI/UX notes`
- [ ] `C-UX-13` `ui` The product carries no menu, no header links, no navigation `src: UI/UX notes`
- [ ] `C-UX-14` `ui` The game room never scrolls at any size `src: UI/UX notes`
- [ ] `C-UX-15` `ui` Layout answers the shape of the window rather than the width `src: UI/UX notes`
- [ ] `C-UX-16` `ui` Nothing overflows sideways at a narrow viewport `src: UI/UX notes`
- [ ] `C-UX-17` `ui` The canvas letterboxes into its space, never stretching `src: UI/UX notes`
- [ ] `C-UX-18` `ui` Body text meets WCAG AA contrast against the background `src: UI/UX notes`
- [ ] `C-UX-19` `ui` Colour alone conveys nothing, every state carrying a text equivalent `src: UI/UX notes`
- [ ] `C-UX-20` `ui` The countdown is never announced to a screen reader `src: UI/UX notes`
- [ ] `C-UX-21` `ui` Tool shortcuts never fire when the chat input holds focus `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` A custom property holds the real measured viewport height `src: Front-end specification`
- [ ] `C-FE-02` `ui` The measured height is recomputed on resize, on orientation change `src: Front-end specification`
- [ ] `C-FE-03` `ui` The chat input is never covered when the on-screen keyboard opens `src: Front-end specification`
- [ ] `C-FE-04` `ui` The landing route stacks wordmark, join panel, three columns, footer `src: Front-end specification`
- [ ] `C-FE-05` `ui` The join panel carries a name field, a language control, an avatar builder `src: Front-end specification`
- [ ] `C-FE-06` `ui` The discovery panel sits beside the join panel, never above `src: Front-end specification`
- [ ] `C-FE-07` `constraint` The discovery panel never expands, never overlays, never delays the join panel `src: Front-end specification`
- [ ] `C-FE-08` `literal` The footer carries the links `Contact`, `Terms of Service`, `Credits`, `Privacy` `src: Front-end specification`
- [ ] `C-FE-09` `ui` The footer notice disclaims responsibility for player-generated content `src: Front-end specification`
- [ ] `C-FE-10` `ui` The game bar carries the round counter, the clock, the word or mask `src: Front-end specification`
- [ ] `C-FE-11` `ui` The player list ranks rows of avatar, name, award, rank `src: Front-end specification`
- [ ] `C-FE-12` `ui` The owner's avatar wears a crown, the owner state also in text `src: Front-end specification`
- [ ] `C-FE-13` `ui` The toolbar is present only for the drawer `src: Front-end specification`
- [ ] `C-FE-14` `literal` Toolbar targets are at least `44px` at the rendered scale `src: Front-end specification`
- [ ] `C-FE-15` `ui` A single-finger drag draws, two-finger gestures do not draw `src: Front-end specification`
- [ ] `C-FE-16` `ui` The canvas prevents the page scrolling under a drag `src: Front-end specification`
- [ ] `C-FE-17` `ui` The chat pins to the newest line unless the reader has scrolled up `src: Front-end specification`
- [ ] `C-FE-18` `ui` The already-guessed channel is visibly distinct from an ordinary row `src: Front-end specification`
- [ ] `C-FE-19` `ui` A modal closes on Escape, returning focus to the control that opened the modal `src: Front-end specification`
- [ ] `C-FE-20` `ui` Game end is a full-page podium with the winner emphasised `src: Front-end specification`
- [ ] `C-FE-21` `constraint` No image file ships with the product `src: Front-end specification`
- [ ] `C-FE-22` `constraint` No audio file ships with the product `src: Front-end specification`
- [ ] `C-FE-23` `ui` Avatars are drawn as inline vector geometry `src: Front-end specification`
- [ ] `C-FE-24` `ui` The doodle ground is generated with seamlessly wrapping edges `src: Front-end specification`
- [ ] `C-FE-25` `ui` All seven sounds are synthesised at play time `src: Front-end specification`
- [ ] `C-FE-26` `ui` The audio context is created on first interaction, never before `src: Front-end specification`
- [ ] `C-FE-27` `ui` Every synthesised sound carries an attack, a release `src: Front-end specification`
- [ ] `C-FE-28` `literal` Body text meets a contrast ratio of at least `4.5:1` `src: Front-end specification`
- [ ] `C-FE-29` `ui` The four room regions are labelled landmarks `src: Front-end specification`
- [ ] `C-FE-30` `literal` The landing title reads `Doodlerush - Free Multiplayer Drawing & Guessing Game` `src: Front-end specification`
- [ ] `C-FE-31` `literal` The primary action reads `Play!` `src: Front-end specification`
- [ ] `C-FE-32` `literal` The secondary action reads `Create Private Room` `src: Front-end specification`
- [ ] `C-FE-33` `ui` The game bar carries a fixed uppercase instruction label for the drawer `src: Front-end specification`
- [ ] `C-FE-34` `literal` The reveal line reads `The word was` `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The rendering model is server-rendered HTML with interactive islands `src: Technical requirements`
- [ ] `C-TR-02` `contract` The front end is SolidStart, the API is Hono, on one origin `src: Technical requirements`
- [ ] `C-TR-03` `contract` PostgreSQL at `DATABASE_URL` is the only datastore `src: Technical requirements`
- [ ] `C-TR-04` `constraint` No second database, cache, queue, object store, identity provider is introduced `src: Technical requirements`
- [ ] `C-TR-05` `capability` A live event stream pushes another player's stroke without a reload `src: Technical requirements`
- [ ] `C-TR-06` `literal` A client heartbeat arrives every `15s` `src: Technical requirements`
- [ ] `C-TR-07` `literal` The server closes a silent connection after `45s` `src: Technical requirements`
- [ ] `C-TR-08` `constraint` Polling is never used as a fallback for game state `src: Technical requirements`
- [ ] `C-TR-09` `literal` A guess reaches every other player in well under `200ms` `src: Technical requirements`
- [ ] `C-TR-10` `contract` The server owns the room, the word, the clock, the turn order `src: Technical requirements`
- [ ] `C-TR-11` `constraint` The client holds no secret, decides no outcome, runs no game clock `src: Technical requirements`
- [ ] `C-TR-12` `contract` Every response carries a strict transport policy header `src: Technical requirements`
- [ ] `C-TR-13` `contract` Every response carries a content-type policy forbidding sniffing `src: Technical requirements`
- [ ] `C-TR-14` `constraint` Nothing the browser downloads contains a credential, an API key, an admin token `src: Technical requirements`
- [ ] `C-TR-15` `contract` Player text is rendered as text, never as markup `src: Technical requirements`
- [ ] `C-TR-16` `capability` Player text is normalized before storage against spoofing characters `src: Technical requirements`
- [ ] `C-TR-17` `capability` Incoming strokes paint incrementally rather than by full re-render `src: Technical requirements`
- [ ] `C-TR-18` `literal` First-load script stays at or under `250000` bytes `src: Technical requirements`
- [ ] `C-TR-19` `capability` Aggregate counts are recorded without identities `src: Technical requirements`
- [ ] `C-TR-20` `contract` A room's state is owned by one process `src: Technical requirements`
- [ ] `C-TR-21` `capability` A lost room tells players the room ended rather than hanging `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded account uses the password `deku-demo-pw-2026` `src: Data model`
- [ ] `C-DM-02` `contract` The seeded logins are written into `/app/USER_README.md` `src: Data model`
- [ ] `C-DM-03` `constraint` No table stores chat text outside a report `src: Data model`
- [ ] `C-DM-04` `constraint` No table stores a network address `src: Data model`
- [ ] `C-DM-05` `constraint` No table stores the current word of a live room `src: Data model`
- [ ] `C-DM-06` `data` Rate-limit counters are keyed by a salted hash of the address `src: Data model`
- [ ] `C-DM-07` `data` The seeded account `player@example.com` carries the display name `Ivy` `src: Data model`
- [ ] `C-DM-08` `data` The seeded account `player2@example.com` carries the display name `Bo` `src: Data model`
- [ ] `C-DM-09` `data` The seeded account `player3@example.com` carries the display name `Ren` `src: Data model`
- [ ] `C-DM-10` `data` The seeded account `moderator@example.com` carries the display name `Wren` `src: Data model`
- [ ] `C-DM-11` `data` The seeded private room `Friday Night Doodles` carries the code `PARROT42` `src: Data model`
- [ ] `C-DM-12` `data` The seeded private room holds three players against a cap of `4` `src: Data model`
- [ ] `C-DM-13` `data` The seeded public room `Open Table` sits in `lobby` `src: Data model`
- [ ] `C-DM-14` `data` One report is seeded unreviewed against a seat in `Friday Night Doodles` `src: Data model`
- [ ] `C-DM-15` `capability` Standings, ranks are computed on read rather than stored `src: Data model`
- [ ] `C-DM-16` `constraint` Seeding is idempotent, so restarting duplicates no row `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product carries no voice, no video, no media transport `src: Constraints`
- [ ] `C-CN-02` `constraint` The product carries no image upload, no file attachment `src: Constraints`
- [ ] `C-CN-03` `constraint` The product carries no payment, no paid tier `src: Constraints`
- [ ] `C-CN-04` `constraint` The product carries no private messaging outside a room `src: Constraints`
- [ ] `C-CN-05` `constraint` The product carries no email, no push notification `src: Constraints`
- [ ] `C-CN-06` `constraint` The product makes no external network call at run time `src: Constraints`
- [ ] `C-CN-07` `constraint` The app stays responsive with `20` players in a room `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `contract` The container-internal port is `4173` `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served under the `/api` prefix on the same origin `src: Deployment contract`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the app is ready `src: Deployment contract`
- [ ] `C-DC-05` `contract` Reserved `.browser_screenshots/`, `.downloads/` directories exist empty at the app root `src: Deployment contract`
- [ ] `C-DC-06` `contract` A production build is served rather than a dev server `src: Deployment contract`
- [ ] `C-DC-07` `contract` The server outlives the session, never a child of the shell `src: Deployment contract`
- [ ] `C-DC-08` `contract` The listener binds `0.0.0.0` `src: Deployment contract`
- [ ] `C-DC-09` `contract` A list endpoint returns a top-level JSON array `src: Deployment contract`
- [ ] `C-DC-10` `contract` An invalid call is rejected as a client error rather than a `5xx` `src: Deployment contract`
- [ ] `C-DC-11` `contract` Room endpoints authenticate by the seat token in `X-Seat-Token` `src: Deployment contract`
- [ ] `C-DC-12` `constraint` A report is never stored in memory alone, disappearing on restart `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | pinned in the brief | `C-CF-06` |
| `24h` | pinned in the brief | `C-CF-07` |
| `1` | pinned in the brief | `C-CF-10` |
| `16` | pinned in the brief | `C-CF-10` |
| `English` | pinned in the brief | `C-CF-14` |
| `8` | pinned in the brief | `C-CF-36` |
| `1h` | pinned in the brief | `C-CF-40` |
| `Friday Night Doodles` | pinned in the brief | `C-CF-51` |
| `4` | pinned in the brief | `C-CF-51` |
| `2` | pinned in the brief | `C-CF-58` |
| `20` | pinned in the brief | `C-CF-58` |
| `10` | pinned in the brief | `C-CF-59` |
| `3` | pinned in the brief | `C-CF-59` |
| `30` | pinned in the brief | `C-CF-60` |
| `180` | pinned in the brief | `C-CF-60` |
| `80` | pinned in the brief | `C-CF-60` |
| `5` | pinned in the brief | `C-CF-61` |
| `0` | pinned in the brief | `C-CF-62` |
| `60s` | pinned in the brief | `C-CF-68` |
| `6h` | pinned in the brief | `C-CF-71` |
| `15s` | pinned in the brief | `C-CF-77` |
| `6s` | pinned in the brief | `C-CF-81` |
| `12s` | pinned in the brief | `C-CF-82` |
| `30s` | pinned in the brief | `C-CF-91` |
| `50%` | pinned in the brief | `C-CF-104` |
| `75%` | pinned in the brief | `C-CF-104` |
| `2s` | pinned in the brief | `C-CF-113` |
| `100` | pinned in the brief | `C-CF-114` |
| `500` | pinned in the brief | `C-CF-125` |
| `50` | pinned in the brief | `C-CF-125` |
| `250ms` | pinned in the brief | `C-CF-130` |
| `4000` | pinned in the brief | `C-CF-142` |
| `95%` | pinned in the brief | `C-CF-146` |
| `60` | pinned in the brief | `C-CF-147` |
| `45s` | pinned in the brief | `C-CF-158` |
| `2000` | pinned in the brief | `C-CF-166` |
| `8KB` | pinned in the brief | `C-CF-182` |
| `10m` | pinned in the brief | `C-CF-184` |
| `30d` | pinned in the brief | `C-CF-190` |
| `Nunito` | pinned in the brief | `C-UX-07` |
| `16px` | pinned in the brief | `C-UX-08` |
| `14px` | pinned in the brief | `C-UX-08` |
| `Contact` | pinned in the brief | `C-FE-08` |
| `Terms of Service` | pinned in the brief | `C-FE-08` |
| `Credits` | pinned in the brief | `C-FE-08` |
| `Privacy` | pinned in the brief | `C-FE-08` |
| `44px` | pinned in the brief | `C-FE-14` |
| `4.5:1` | pinned in the brief | `C-FE-28` |
| `Doodlerush - Free Multiplayer Drawing & Guessing Game` | pinned in the brief | `C-FE-30` |
| `Play!` | pinned in the brief | `C-FE-31` |
| `Create Private Room` | pinned in the brief | `C-FE-32` |
| `The word was` | pinned in the brief | `C-FE-34` |
| `DATABASE_URL` | pinned in the brief | `C-TR-03` |
| `200ms` | pinned in the brief | `C-TR-09` |
| `250000` | pinned in the brief | `C-TR-18` |
| `APP_PUBLIC_URL` | pinned in the brief | `C-DC-01` |
| `4173` | pinned in the brief | `C-DC-02` |
| `200` | pinned in the brief | `C-DC-04` |
| `player@example.com` | pinned in the brief | `C-DM-07` |
| `Ivy` | pinned in the brief | `C-DM-07` |
| `player2@example.com` | pinned in the brief | `C-DM-08` |
| `Bo` | pinned in the brief | `C-DM-08` |
| `player3@example.com` | pinned in the brief | `C-DM-09` |
| `Ren` | pinned in the brief | `C-DM-09` |
| `moderator@example.com` | pinned in the brief | `C-DM-10` |
| `Wren` | pinned in the brief | `C-DM-10` |
| `PARROT42` | pinned in the brief | `C-DM-11` |
| `Open Table` | pinned in the brief | `C-DM-13` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact shade of every colour role | `C-UX-04` |
| the exact size of the layout unit | `C-UX-01` |
| the exact duration of every moment | `C-UX-11` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 2 | 8 |
| User roles | 1 | 10 |
| Core features | 33 | 195 |
| User flow | 7 | 16 |
| UI/UX notes | 6 | 21 |
| Front-end specification | 5 | 34 |
| Technical requirements | 6 | 21 |
| Data model | 4 | 16 |
| Constraints | 1 | 7 |
| Deployment contract | 9 | 12 |
| Definition of done | 1 | 1 |
