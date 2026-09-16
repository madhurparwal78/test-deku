# Doodlerush

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, type a name, build an avatar, open the private-room route, create a room, land on a confirmation carrying its invite link, and a second stranger must be able to open `/room/PARROT42`, take the last seat in `Friday Night Doodles`, and guess a word that a third person is drawing, all without hitting an error page. Two things in that sentence cannot be arranged inside the app's own screens. The word belongs to one player at a time: everything the app sends to a player who is not the drawer, for the whole of that turn, must be free of the word in every field and in every form, and a word that is present in the response but hidden by the interface is the same as a word that was never protected. And `Friday Night Doodles` opens with exactly one seat left against a player cap of `4`, so two strangers taking that seat at the same instant must not both get in: one joins, the other is sent to another room, and the room never holds five players.

## Overview

Doodlerush is a free browser party game for friends and for strangers. One player is given a secret word and draws it on a shared canvas. Everybody else races to type it into the chat. Points go to whoever guesses fastest, and to the drawer for being guessed, and the player with the most points after a set number of rounds wins.

There is no download and no payment, and nothing needs to be signed up for in order to play: a visitor types a name, picks a language, flicks through a four-layer avatar and presses one control. Rooms come in two kinds. A public room is reached only by matchmaking; a private room is reached only by its eight-character code or the invite link that carries it. Neither kind is listed anywhere, and there is deliberately no way to browse into a room a person was not sent to.

An account is optional and adds three things and no more: a reserved display name, the settings of private rooms that account owns, and, for a moderator, the queue of reports players have filed. Playing never requires one.

The genuinely hard part is that the room is one thing showing different things to different people at the same instant. The drawer's copy of the room carries the word; every other copy carries a mask of the same shape. Building one copy and sending it to the room is the obvious implementation and it hands the answer to anybody who reads what their own browser was sent. Six further rules protect the same secret and each of them is the natural implementation of something else: echoing a correct guess back as chat, announcing a near miss to the room, sending the reveal schedule instead of the reveals, letting a player who has guessed talk to players who have not, letting the drawer type the word, and letting scores move while the turn is running.

Doodlerush deliberately is not several things. There is no voice or video, no image upload of any kind, no private messaging between players outside a room, no paid tier and no payment, no browsable directory of rooms, and no automated judgement of what somebody has drawn.

## User roles

| Role | Can do |
|---|---|
| Guest | Play without an account: join a public room by matchmaking, join a private room with its code, draw, guess, vote, mute another player locally, and report a player. **Cannot** read the report queue, **cannot** own a room across sessions, and **cannot** reserve a display name. |
| `player` | Everything a guest can do, plus: sign in, reserve a display name, own private rooms whose settings survive between sessions, and see the rooms that account owns. **Cannot** read the report queue, **cannot** mark a report reviewed, and **cannot** read or join a private room they hold neither a seat in nor the code for. |
| `moderator` | Everything a `player` can do, plus: read the report queue, replay the strokes captured with a report, and mark a report reviewed. **Cannot** change any room's settings they do not own, **cannot** score, start, skip or end a turn, and **cannot** read the current word of any room. |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a control in the UI is not authorization: a direct API call from a `player` session to any `moderator`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is open: anybody may create a `player` account. The `moderator` role is granted only by seeding and there is no path in the product that raises a `player` to it.

Four accounts are seeded, all of them at the password `deku-demo-pw-2026`:

| Email | Display name | Role |
|---|---|---|
| `player@example.com` | `Ivy` | `player` |
| `player2@example.com` | `Bo` | `player` |
| `player3@example.com` | `Ren` | `player` |
| `moderator@example.com` | `Wren` | `moderator` |

## Core features

### Auth

Accounts are email and password, implemented by this app. There is no external identity provider.

1. `POST /api/auth/signup` takes an email, a password and a display name, and creates a `player`. A second signup on an email that already exists is rejected as invalid and creates nothing.
2. `POST /api/auth/login` returns a bearer token. Every authenticated call carries it in an `Authorization` header. A call with a missing, malformed or expired token is denied.
3. Passwords are stored hashed. The literal `deku-demo-pw-2026` must work at login for every seeded account.
4. A bearer token expires `24h` after it was issued. An expired token on a mutating call leaves the state unchanged.
5. A seat in a room is a **separate** credential from a bearer token, and the two are never interchangeable. A bearer token does not admit its holder to a room, and a seat token does not authenticate an account.

### The front door

The landing route is the whole front of the product, and it is four controls plus a footer.

1. A name field accepts `1` to `16` characters. A name outside that band is rejected inline, the field is named in the message, and nothing is created.
2. A language control selects the **word list**, not the interface language, and it is chosen before joining because rooms are partitioned by it. `English` is seeded; the control sits beside the name field and never inside a settings panel.
3. An avatar is assembled from four independently chosen layers: a body colour, an eye set, a mouth and an optional accessory. Arrows step each layer and one control sets all four at random. The avatar is fixed for the session once a player joins.
4. The primary action joins a public room by matchmaking. The secondary action opens `/create`. The primary action is the larger and more prominent of the two.
5. A five-step how-to-play panel states, in order: choose a word when it is your turn; draw it, and do not write the word itself; let the others guess; guess when it is not your turn; score the most points to win. Step two is a rule of the game and the server enforces it, not a hint.
6. A privacy page at `/privacy`, linked from the footer of every page, states what Doodlerush stores, what it does not store, and how long each kind of record is kept. A terms page at `/terms` carries a contact address at its head. Both are reachable from every route in the product.
7. Every internal link on `/`, `/create`, `/privacy`, `/terms`, `/login` and `/signup` resolves to a page the app serves. A footer link that answers not-found is a defect.
8. An unknown address renders Doodlerush's own not-found page, which carries a way back into a game, and answers not-found rather than serving the landing route.

### Rooms

1. A room is `public` or `private`. A `public` room is reachable only through `POST /api/matchmake`. A `private` room is reachable only through its code. **Nothing in this product lists rooms of either kind**: there is no endpoint, no page and no search that returns a set of live rooms, and a request for one is answered not-found rather than with an empty list.
2. **This is the rule the product is built around.** `GET /api/rooms/{code}` and `GET /api/rooms/{code}/state` describe a room only to a caller who has supplied that room's code in the path, and `state` further requires a seat token for that room. A caller who has neither a seat nor the code cannot learn a room's name, its player count, its settings, its language, its state or whether it exists at all. The negative case: a signed-in `player` who holds no seat in `Friday Night Doodles` and who calls `GET /api/rooms/PARROT42/state` without that room's seat token is denied, and the response carries no room name, no player list and no word. Hiding the room from the interface is not enough; the denial is at the API.
3. A room code is `8` characters drawn at random from an alphabet with no characters that look alike in ordinary typefaces. Codes are never sequential and never derived from a counter, because a sequential code lets anybody walk into the one place in this product where people are entitled not to meet a stranger. A code collision is regenerated. A code is retired for `1h` after its room closes before it can be issued again.
4. `POST /api/rooms` creates a `private` room and returns its code, its name and its invite link. The invite link opens `/room/<code>` and **never joins the visitor directly**: it always stops at the name and avatar step, because a player who lands inside a room without choosing a name is a player with no name.
5. Matchmaking places a player in the **fullest** room that is not full, that is in `lobby` or early `drawing`, and that matches their language, because matchmaking is partitioned by `lang`. It never places them in a room in `game_end` or one whose current round is more than half elapsed. A new room is created only when no eligible room exists. Preferring the fullest room gathers players into playable games rather than scattering them across rooms of two.
6. Seat allocation is one indivisible operation per room. Two joins racing for the last seat of `Friday Night Doodles` produce exactly one join and one redirect: the loser is offered another room rather than an error, and the player count never exceeds the cap. A failed join leaves no seat held and no partial player record.
7. The host is the room's creator, or the first player in a matchmade room. When the host leaves, the longest-present connected player becomes host immediately and without anybody acting, and the room is told who the host now is. A room whose host has left and which nobody can start is a dead room.
8. Settings are host-only and `lobby`-only, and every one of them is validated server-side against its range: players `2` to `20` (default `8`), rounds `2` to `10` (default `3`), turn length `30` to `180` seconds (default `80`), word choices offered `1` to `5` (default `3`), hints revealed `0` to `5` (default `2`), word mode one of `normal`, `hidden` or `combination` (default `normal`), custom words, and a custom-words-only switch. A settings change that is out of range, that arrives from a player who is not the host, or that arrives once the game has started, is rejected and changes nothing.
9. Settings are frozen for the duration of a game. Changing them mid-game would change the scoring basis under players who have already scored.
10. Room lifecycle: when the last player leaves, the room is retained for `60s` and resumes with its scores and settings if anybody returns within that window; after that the room and its stroke buffers are destroyed. If the player count drops below `2` mid-game the room returns to `lobby` with scores retained. A room older than `6h` is closed with notice.

### The turn

A room is in exactly one of six states: `lobby`, `choosing`, `drawing`, `turn_end`, `round_end`, `game_end`.

1. **Every transition is the server's.** No client action advances the game. There is no endpoint that accepts a score, a turn advance, a timer value or a claim that a guess was correct, and there is nothing for the server to reject because there is nothing to send.
2. `lobby` becomes `choosing` when the host starts and at least `2` players are present. `choosing` becomes `drawing` when the drawer chooses, or when the `15s` choice window expires and the server chooses for them, preferring the middle difficulty. `choosing` becomes `turn_end` if the drawer leaves before choosing.
3. `drawing` becomes `turn_end` when the turn deadline expires, **or** when every non-drawer has guessed correctly, **or** when the drawer leaves. The middle condition is not optional: a turn that only ends on its deadline leaves the room watching a finished drawing for the rest of the clock.
4. `turn_end` lasts `6s`, then becomes `choosing` if players in the round remain, or `round_end` if everybody has drawn this round. `round_end` becomes `choosing` while rounds remain, or `game_end` when the configured round count is complete. `game_end` lasts `12s` and returns to `lobby` with scores cleared and settings kept.
5. A round is **one turn per player in a fixed order**, established when the round begins from the player list. It is not a random pick per turn. A player who joins mid-round enters the order at the next round and does not draw in the current one. A player who leaves is removed from the order and the round shortens. Over four rounds with four players, every player draws exactly four times.
6. The clock is the server's. The server computes an absolute deadline and sends it; the client renders the difference between that deadline and its own corrected clock. A client never tells the server that time is up, and the server decides expiry on its own clock. A client whose displayed countdown disagrees is cosmetically wrong and functionally irrelevant.
7. A client measures its offset from the server clock on joining and every `30s` after, and **recomputes the countdown from the deadline whenever the tab is focused again** rather than resuming it. A tab that has been in the background has had its timers slowed, and a countdown resumed from where it was left is wrong by however long the player was away.
8. A player may opt out of drawing turns and stay in the room. The turn order skips them, and the round shortens exactly as it does for a player who left.

### The word, and who may see it

This is the product's central rule and the rest of this section is subordinate to it. Secret handling starts from one fact: the code running in a player's browser is not on the product's side. It runs on their machine, they can read every byte it receives and change every byte it sends, so every anti-cheat rule below is a server rule and none of them is a client rule.

1. The current word is sent to the current drawer and to nobody else, in no field and in no form, until the turn ends. It is not sent scrambled, not sent alongside a flag telling the client to hide it, and not sent inside any list, any log line or any settings object.
2. `GET /api/rooms/{code}/state` is built **per recipient**. The drawer's snapshot carries `word` with the real word. Every other player's snapshot omits `word` entirely and carries `word_mask`. The negative case: while `Friday Night Doodles` is in `drawing`, a snapshot fetched with a non-drawer's seat token contains the word nowhere, and neither does any event that seat receives on `GET /api/rooms/{code}/events`.
3. The mask shows one placeholder per character, with spaces and hyphens shown literally, because the length structure is part of the puzzle. It counts characters, not bytes, so it is correct for a non-Latin word list.
4. Hints are computed and sent by the server at the moment they are due, as individual reveals carrying a position and a character. The schedule is never sent to a client. By default letters are revealed at `50%` and at `75%` of the turn elapsed, positions are chosen at random and seeded per turn, and never more than half the letters are revealed.
5. When a guess is correct, the room is told **who** guessed and never **what** they typed. The text a player typed to guess correctly is the word.
6. The word list lives on the server. No response in this product contains the list, the upcoming words, or the seed that picks them.
7. Word modes: in `normal` the mask shows the letter count; in `hidden` the mask shows nothing until the first hint; in `combination` the drawer receives two words and draws both.
8. No response to any caller ever carries another player's seat token, and no response carries any player's network address.

### The guess pipeline

`POST /api/rooms/{code}/guess` takes text and returns an outcome of `correct`, `close` or `chat`. Every guess passes through eight steps in this order.

1. **Authorise.** A guess from the current drawer is not a guess and is rejected.
2. **Deduplicate.** A guess from a player who has already guessed correctly this turn is rejected, and scores nothing.
3. **Rate limit.** At most `4` guesses per `2s` per player. Beyond that the player is told, and is never disconnected for it.
4. **Length.** Text beyond `100` characters is rejected.
5. **Normalize.** Normalization is applied identically to the guess and to the word, and that symmetry is the requirement: case folded, accents stripped so an accented character matches its unaccented form in both directions, apostrophes and hyphens and full stops removed, whitespace collapsed then trimmed, full-width forms folded to half-width. A player who types a word without its accent is correct.
6. **Compare** against the normalized word.
7. **Near-miss.** A near-miss is a guess within an edit distance of `1` of the normalized word, where the word is `5` characters or longer, is close. Shorter words have no near miss, because at four characters an edit distance of one is a different word.
8. **Route.** Routing has three outcomes and no fourth. A correct guess produces `correct` and the room is told who guessed, without the text. A close guess produces `close` and **only the guesser is told**, and the message does not repeat their guess back at them. Anything else produces `chat` and the room sees the text.

Three further rules, each of which leaks the word if it is missed:

9. A correct guess is **never** echoed to the room as chat. This is the most common way the word escapes, and it escapes to exactly the players who have not worked it out.
10. Once a player has guessed correctly, their chat is routed to a separate channel visible only to other correct guessers and to the drawer. They can talk; they cannot talk to the players still guessing.
11. The drawer's chat is filtered against the word: a drawer message containing the word, or a near miss against it, is rejected and only the drawer is told. The natural thing for a struggling drawer to type is the word.

Two guesses arriving in the same instant are ordered by server arrival stamp and tie-broken by seat identifier, deterministically. Both players are told they were correct, and identical arrival times give identical scores.

### Scoring

1. A correct guess scores on a **linear** decay across the turn, from `500` at the start to `50` for a correct guess in the final moments. The basis is the server's arrival stamp and never a time the client supplied, because a client-supplied timestamp is a client-supplied score.
2. The drawer scores as well, in proportion to how many people guessed and how fast: each guesser's own award divided by the number of non-drawers, summed, capped at `500`. Without this term the winning play is to draw something nobody can guess, because a drawer who cannot score can only lose ground while everybody else gains.
3. Nobody scores when nobody guesses, the drawer included, and the turn is recorded as a failed turn. Nobody scores when the drawer leaves mid-turn, including players who had already guessed. Nobody scores for a turn ended by the room emptying or by a vote to skip.
4. A guess arriving within `250ms` after the deadline is still accepted. Without that grace the player on the worst connection is systematically robbed of guesses they made in time and has no way of telling.
5. Standings sort by score descending, then by earliest join, and ties are shown at the same rank. **Standings update at `turn_end` and never during a turn**, because a score moving mid-turn announces that somebody has already got it and roughly when.

### The canvas

1. The wire carries stroke geometry and never pixels. Sending the whole canvas as an image costs hundreds of kilobytes a second and is forbidden; sending a changed-region image costs tens of kilobytes and is forbidden too; coalesced stroke deltas cost under one kilobyte and are the requirement. A stroke is a monotonic identifier for the turn, a palette index, a brush-size index, and an array of points.
2. Colour and brush width travel as **indices into the fixed palette**, never as values. A client that could send an arbitrary colour could send the background colour as a brush and erase another player's work in a way undo cannot reach.
3. Every point is a pair in the range `0` to `1` relative to the canvas's logical area, at a fixed aspect ratio, to `4` decimal places. Raw pixel coordinates produce a drawing that is correct on the drawer's screen and wrong on every other screen, and the drawer never finds out because their own screen looks right.
4. The server retains the full ordered stroke list for the current turn and returns it inside the snapshot, so a player joining or reconnecting mid-turn sees the drawing as it stands, in one pass before their first paint, rather than watching it redraw itself. The buffer is discarded at `turn_end` and is capped at `4000` strokes per turn, beyond which further strokes are refused and the drawer is told.
5. `POST /api/rooms/{code}/canvas-op` carries `undo`, `clear` or `fill`. Undo removes the last stroke or operation by this drawer this turn and is broadcast as an operation rather than as a redraw. Clear removes everything this turn.
6. **Fill must produce the same result on every device in the room.** A flood fill is a pixel operation and pixel operations depend on smoothing and rounding, which differ per device, so a fill run on a phone and on a laptop lands its boundary in different places and from that moment the players are looking at different pictures. Either the server computes the fill against an authoritative raster and broadcasts the region, or every client rasterises the stroke list into an offscreen buffer at one fixed internal resolution with antialiasing disabled and fills there: pick one and be consistent, and if it is the second, the internal size is identical on every client regardless of display size. A fill that would cover more than `95%` of the canvas is rejected as either a mistake or an attempt to erase.
7. Points are coalesced and flushed once per animation frame rather than once per pointer event, collinear points within a tolerance are dropped before sending, and batches are re-broadcast in arrival order without being re-batched. At most `60` stroke batches per second per drawer and at most `20` canvas operations per turn.
8. **Only the current drawer may draw.** A stroke or a canvas operation from anybody else is rejected by the server and counted against that player's abuse budget. Hiding the toolbar from non-drawers is a convenience, not the control.
9. Delivery may repeat, so every handler tolerates a duplicate: a repeated stroke identifier is dropped, a repeated canvas-operation identifier is dropped, a repeated guess is scored once per player per turn, the first word choice wins and the rest are ignored, and a repeated join carrying the same seat token is a reconnection. Without the guess rule, one duplicated frame during a network hiccup awards a player two correct answers and nothing shows it but a wrong leaderboard.

### Sessions and reconnection

1. A seat token is issued by the server on first join. It is opaque and high-entropy, never a name, never a sequence number and never anything guessable. A sequential player identifier used as a seat token is a way to take over another player's seat and their score.
2. A seat token is stored by the client, identifies one player across reconnections and nothing more, lasts `24h` from last use, and is returned to its owner and to no other caller.
3. Reconnecting sends the seat token and the room code. The server matches it to a seat held open and restores the score, the name, and **the already-guessed mark for the current turn**. A returning player who had already guessed cannot guess again; without that, dropping out after guessing and returning scores the same word twice.
4. A seat is held for `45s` after an unexpected disconnection and the player is shown as present but disconnected rather than removed. An explicit leave releases the seat at once, because holding a seat open in a full room for somebody who deliberately walked out only stops somebody else getting in.
5. If the disconnected player was drawing, the turn ends immediately and the seat is still held.
6. Names are `1` to `16` characters and unique within a room. A duplicate is suffixed by the server rather than rejected, and the server assigns the suffix, so two players cannot both appear under one name. Names change in `lobby` only, at most `3` times per room.
7. A seat token already seated in a room and joining again is a reconnection that displaces the older connection. It does not create a second seat, and the older connection is told plainly that the session moved.

### Words and content

1. The word list is server-side, at least `2000` entries per language, each tagged `easy`, `medium` or `hard`. Entries are concrete drawable nouns, never abstractions, proper nouns or brands: an undrawable word produces a turn where nobody scores including the drawer, and one of those is enough to sour a room.
2. At `choosing` the drawer alone is offered the room's configured number of words, one easy, one medium and one hard where the list allows. A word already used this game is never offered again. If the list is exhausted, used words are recycled oldest first.
3. Custom words are host-supplied free text, parsed comma-separated, trimmed and deduplicated, `1` to `100` characters each, at most `500` words. They pass the same filter as names and chat, they are rendered as text and never as markup, and they are scoped to the room and never kept beyond it. Custom-words-only requires at least `10` words or the room cannot fill a round.
4. Names, chat and custom words are matched against a per-language filter list **on the normalized text**, so obfuscation with punctuation and lookalike characters does not evade it. A filtered name is rejected at entry with a reason; a filtered chat message is dropped and only its sender is told; a filtered custom word is dropped and the host is told which.
5. **A guess that matches the filter is still evaluated as a guess**, and if it is the word it is correct. A filter that discards a guess before comparing it means an ordinary word resembling a filtered term can never be guessed, and no player would ever work out why.

### Moderation and limits

1. Per address: at most `8` concurrent connections, `20` joins per minute, `5` rooms created per minute, `40` messages per second and a message size of `8KB`. The first three are generous because a school or an office behind one address is an ordinary case.
2. In room: `4` guesses per `2s`, `4` non-guessing chat messages per `2s`, `60` stroke batches per second, `4000` strokes per turn, `20` canvas operations per turn, `10` settings changes per `10s`, `3` name changes per room. Exceeding a limit produces a message to that player and never a disconnection, because disconnecting a player for typing quickly is worse than the typing.
3. Kicking and voting are the room's own controls. The host may kick a player, and a kicked player cannot rejoin that room for `10m`. Any player may open a vote to kick, which needs a simple majority of connected non-target players and expires after `60s`. Any player may open a vote to skip the current turn, which scores nobody.
4. **Drawn content is not judged automatically, and this product does not pretend otherwise.** The controls are structural: no browsable room list, a vote to skip that works in seconds, a vote to kick, a host kick in private rooms, and a report.
5. Reporting is available to any player against any player, at most `3` per player per hour. It captures the reported seat, the current turn's **stroke buffer**, the recent chat tail, the room and the timestamp, and it is kept `30d` and then deleted. A report captures the strokes rather than a rendered picture, because strokes are smaller and can be replayed at review time. Reports never act on their own: `GET /api/reports` is readable by a `moderator` and by nobody else.
6. Automation is bounded by the per-address limits above and by a human-check on the join path alone, raised only above a per-address threshold so that ordinary players never meet one. A player behaving impossibly, for instance guessing correctly within `500ms` of every turn start repeatedly, is flagged for review and is never acted against automatically. A fast player on a good connection and an automated one look alike for a few rounds, and wrongly removing a real player is worse than tolerating the other for a while.
7. Mute is local to the muting player: it hides that player's chat for them alone, it is not announced, and it does not affect scoring. A mute the room was told about would become a way to bully somebody.
8. Like and dislike controls sit on the canvas. They carry no score and must not, because a drawing scored by a vote of the room is a popularity contest.
9. Children play this game. Nothing personal is collected, there are no profiles, there is no private messaging outside a room, there is no image upload, and the language filter is on by default with no control that turns it off.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the landing route: wordmark, join panel, three columns, footer | none |
| `/create` | the private-room route: settings, then create | none |
| `/room/PARROT42` | a room, addressed by its code | the code, then the name step |
| `/privacy` | what Doodlerush stores, and for how long | none |
| `/terms` | the terms document, contact address at its head | none |
| `/login` | sign in to an optional account | none |
| `/signup` | open registration | none |
| `/account` | the rooms this account owns, and its reserved name | account |
| `/reports` | the report queue and the strokes captured with each one | `moderator` |

**Entry and redirects.** An unauthenticated request for `/account` or `/reports` goes to `/login`, and the original destination is restored after signing in. A signed-in `player` requesting `/reports` is refused rather than redirected, and the queue is not in the response. Signing out returns to `/` and ends the account session; a seat token is a separate credential and survives it. An expired bearer token mid-action returns the player to `/login` with the work not performed. `/room/<code>` for a code that is not live renders the not-found page and answers not-found.

**Journeys.**

1. **Play with strangers.** Open `/`. Type `Ivy` into the name field, leave the language at `English`, step the avatar layers, press the primary action. The loading overlay names the step it is on: connecting, then finding a room, then joining. The room opens in `lobby`.
2. **Make a private room.** Open `/`, press the secondary action, land on `/create`. Set players to `4`, rounds to `3`, turn length to `80`, word choices to `3`, hints to `2`, word mode `normal`. Create. A full-page confirmation names the room, shows the code and the invite link, and offers a control that copies the link. Press through into the room.
3. **Join by link.** Open `/room/PARROT42`. The name and avatar step appears first, every time. Enter a name, join, and take the last seat in `Friday Night Doodles`.
4. **Take a turn.** As the drawer, the bar drops the word in and three words are offered. Choose one, draw, watch player rows turn green as each guesser gets it. The turn ends the moment the last non-drawer has guessed, and the standings move only then.
5. **Guess.** As a non-drawer, type into the chat. A near miss is answered privately and does not repeat the guess. A correct guess turns the row green, adds a text state beside it, and moves the guesser into the already-guessed channel.
6. **Reconnect.** Close the tab mid-turn after guessing correctly. Reopen `/room/PARROT42` within the grace window, return to the same seat with the same score, still marked as having guessed, and with the drawing as it now stands.
7. **Report and review.** Open a player row, report, confirm. Sign in as `moderator@example.com`, open `/reports`, replay the captured strokes, mark the report reviewed.
8. **Finish.** After the configured rounds, the podium takes the whole page with the winner emphasised, then the room returns to `lobby` with scores cleared and settings kept.

**States.** A lobby with one player says the game needs a second before it can start. Every list has an empty state: no rooms owned, no reports filed, no chat yet. The loading overlay names its step rather than spinning silently. A refused action produces a message in the room and never a disconnection or a blank screen. An unknown address is a designed page with a way back.

## UI/UX notes

The north star: somebody arriving should understand in the first moment that this is a game rather than an application, and that one press puts them in it. The register is a game, and it is loud on purpose: it is played by children and by adults being childish, and a restrained version of it would be a worse product. Expressive over tasteful, and speed over polish.

The whole interface derives from one layout unit and one base text size. Every panel, control, avatar and toolbar is a multiple or a fraction of that unit, and when space runs short the unit shrinks and the entire interface shrinks with it in proportion rather than rearranging itself. Hand over the unit: the size is yours, so long as every dimension in the product is derived from it and the game fits one screen at every shape.

The ground is a deep, soft blue, tiled edge to edge with a repeating pattern of hand-drawn single-stroke doodles set one step lighter than the ground. Panels over it are translucent so the doodles show faintly through, and that is why the page reads as one surface rather than as cards on wallpaper. Panel borders are a near-black, muted blue and panel text a near-white neutral.

Colour carries meaning here and each meaning is exclusive. A near miss is a mid, vivid amber worn by nothing else. A correct guess is a mid, vivid green, and a player who has guessed has their whole row turn a light, vivid green, alternating to a mid, vivid green. The channel for players who have already guessed is a mid, soft lime on a green-tinted near-white neutral row, and an ordinary chat row is a plain near-white neutral. A message about the drawer is a mid, vivid blue; a player leaving is a mid, vivid orange; the room owner is a light, vivid orange. The viewing player's own row is a light, vivid blue, and a mid, vivid blue once they have guessed. The selected tool is a light, soft indigo and a tool tooltip sits on a light, vivid blue ground. The primary control is a mid, vivid blue that darkens on point and again on press. Keyboard focus is a light, vivid orange chosen deliberately against a blue interface, and it is never removed. A focused field border is a light, vivid cyan, a resting field border a mid neutral, placeholder text a light neutral, and field text, the word caption and canvas text a deep neutral. The exact values are yours, so long as each role keeps its meaning and no other element borrows it.

Typography is one family throughout, a rounded humanist sans: `Nunito`, with the fallback stack `"Nunito", "Trebuchet MS", "Segoe UI", system-ui, sans-serif`, at weights `400`, `600`, `700` and `800` plus a `400` italic. Body and chat set at `16px`, controls and labels at `14px`, headings at `18px`, section headings at `19.5px`, the heaviest heading at `18px` in `800`, and the largest text on the page at `25.2px` in `800`. The heaviest weight is used across the smallest range of sizes, and that is what gives the interface its toy-like solidity.

Corners are barely softened, because the interface is built from blocks rather than pills, and only two shapes escape that: the avatar bubble's inner shape is fully round, and the modal container carries the one genuinely large radius in the product. The most repeated effect in the whole interface is a hard offset shadow with no blur at all, down and to the right, on the clock, the avatars and almost every drawn mark. Exactly one soft variant exists, on the avatar arrows. A blurred shadow anywhere else in this interface is wrong, and that single detail is most of why the product reads as a toy rather than an app. Density is comfortable on the landing route and tight inside the room, because the room has to hold four regions at once. Layering runs in a fixed order from back to front: the doodle ground furthest back, ordinary content above it, the game surfaces above that, the on-screen keyboard above those, modals above that, and the loading overlay above everything; the modal and the keyboard blur what is behind them, and the loading overlay blurs it further.

The product commits to one mode and designs it fully: the deep blue ground is the only mode there is, and no light alternative is offered or implied. Every control carries five states and each is distinguishable without moving the pointer: at rest, pointed at, pressed, focused, unavailable. Unavailable is never signalled by colour alone, an icon-only control always carries a label, a field states its error beside the field rather than in a banner elsewhere, Escape closes any modal and returns focus to the control that opened it, and an action that removes somebody from a room asks once before it happens.

Motion is `springy`: things overshoot and settle rather than gliding to a stop. It is also fast, and the speed is the requirement rather than the curve. Nothing in this product takes longer than about an eighth of a second to respond and a hover lift is faster still, quick enough to read as instant rather than as animation; a build that eases everything over a third of a second will feel sluggish in a way nobody can name. The moments that carry meaning: the word bar drops in when a turn starts; each revealed letter jumps up, grows, flashes the owner orange and falls back past its place before settling, which is why a reveal reads as one letter arriving rather than as the word being redrawn; a message over the canvas arrives fast, overshoots, snaps back, holds still for almost its whole life and then fades; every chat line fades in; the podium celebrates the winner with a squash-and-stretch sequence. Two controls kick sideways when used and do their whole movement in the first twentieth of their time, which is the shape of a flick rather than a swing, and smoothing that out evenly stops it reading as a reaction. Behind everything two waves drift in opposite directions and bubbles scale past their size and settle, a parallax made from one repeating pattern rather than from layers. Uniformity over novelty: one character everywhere, and nothing moves differently to feel special.

Under `prefers-reduced-motion` nothing is removed, only stilled: waves and bubbles stop, avatars stop, icons sit in their settled state, a revealed letter appears without its jump, the podium is shown settled, and chat and canvas messages appear without movement. The countdown is the one exception in the other direction and keeps running, because a stopped clock in a timed game is a broken game. The background also stops entirely during a turn on a narrow screen, because it competes with the drawing for the same budget and the drawing wins.

There is no navigation anywhere: no menu, no header links, no tabs. The landing route has one job, the primary action does it, and a navigation bar would be more things between a player and a game. What chrome exists is the wordmark, set as type with each letter in a different saturated colour and a drawn pencil standing in for the final character, which is the only multicoloured element in the product; a row of eight avatars beneath it, one crowned; and a footer of four centred links with a notice beneath disclaiming responsibility for player-generated drawings, messages and names. That notice is load-bearing and is never trimmed.

In the room, four regions share one screen and **the game never scrolls**: a bar across the top carrying the round counter, the clock and the word or its mask with a caption beneath; the player list down the left, ranked, each row an avatar, a name, a score and a rank; the canvas in the centre, dominant, its toolbar beneath it; the chat down the right as a continuous stream pinned to the newest line, which leaves the reader alone the moment they scroll up. A player forced to scroll to see the chat cannot play, because guesses arrive while they are looking away.

Layout answers the **shape** of the window rather than its width, and there is no width breakpoint set at all, because a wide short window and a tall narrow one need different arrangements at the same width, and a width-only rule produces a game that works on a phone held upright and falls apart when it is turned sideways, which is how people hold a phone to draw. Three arrangements: landscape, a narrowed landscape where the player list pages, and portrait where the player list collapses to a strip and the chat moves below the canvas. In portrait the canvas and the chat compete and the canvas wins while a turn runs, but the chat input is never covered and never scrolled away, including when the on-screen keyboard opens. At a narrow viewport nothing overflows sideways and every control stays reachable without a horizontal scroll. The canvas holds a fixed logical shape and letterboxes into whatever space it is given; it never stretches, because a stretched canvas turns the drawer's circle into the viewer's ellipse.

Every player has an avatar built from four independently chosen layers, a body colour, an eye set, a mouth and an optional accessory, stepped by arrows or set at random by one control, with a crown overlaid on the room owner. Avatars are not still: a small dip early in a loop, a squash on click, and effects that make one glow, blink, cycle hue, or wobble by orbiting a tiny circle while counter-rotating at the same rate so it shivers in place rather than tumbling. Interface marks are drawn geometry and never image files: a crown, a clock, a pen that rocks while somebody draws, a brush-size control, a settings mark, a randomise die, a selection arrow which is a triangle clipped from a square, and a thumb up and a thumb down. A single-colour mark is produced by crushing a coloured shape to a silhouette rather than by drawing it twice, and an unavailable mark is the same shape desaturated, never signalled by colour alone.

Sound belongs to seven events and every one of them is synthesised rather than played from a file: a turn beginning, a tick through the last stretch, a correct guess, a turn ending with somebody having guessed, a turn ending with nobody having guessed, a join and a leave. Two distinct endings, because a turn nobody guessed is a real outcome rather than a turn with no points. One mute control, remembered between sessions and respected by every sound. Nothing sounds before the first interaction. The guess sound can fire several times in a second and must not clip or stack into a queue. The tick stops the instant a turn ends, including when it ends early because everybody guessed. Sound is never the only signal for anything.

Accessibility is a floor, not a preference. Body text and its background meet WCAG AA contrast, everywhere the product is used, and the orange focus ring holds that bar against the blue ground. Touch targets are comfortably sized and stay comfortable in the toolbar at the shrunk unit. Every control is reachable and operable by keyboard with a visible focus ring that is never removed, and the tool shortcuts never fire while the chat input has focus, which matters because the chat input is focused almost all the time. Icon-only controls carry labels. The four room regions are labelled landmarks. The chat announces new lines politely and a correct guess announces; the countdown never announces, because a number read out every second makes the page unusable. Colour alone conveys nothing: the guessed state, the near-miss, the room owner and the active tool each carry a text equivalent beside the colour, so the active tool is conveyed in text and not only by its indigo highlight. A player who cannot see the canvas can still join, chat, follow the game and receive the revealed letters, and can opt out of drawing turns without leaving the room.

What this must not look like: an application. No page dominated by a single hue family with no second signal, no decoration standing in for content, no marketing composition where the working interface belongs, no blurred shadow, and nothing eased slowly enough that a press feels like a wait.

## Technical requirements

The rendering model is **server-rendered HTML with interactive islands**. The landing route, the create route, the privacy route, the terms route and the not-found page arrive as complete HTML on first paint and need no script to be readable. The room is the one island: it hydrates and then owns its canvas, its chat and its clock.

The stack is **SolidStart** on the front end and **Hono** for the JSON API, both served from one origin, with **PostgreSQL** as the only datastore, reached at `DATABASE_URL`. Authentication is email and password implemented in this app, with bearer tokens. `GET /api/health` answers once the app is ready. Requests are logged as one structured line each to stdout, carrying no player name, no chat text and no address.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing service available in this environment is PostgreSQL, and reaching for anything else is a contract violation.

**The real-time transport and its protocol.** The live connection is the app's own. The server holds a connection open per seated player at `GET /api/rooms/{code}/events` and pushes events down it as they happen: another player's stroke appears without a reload, a guess appears without a reload, the clock's deadline arrives once and is not polled for. Ordering is preserved per connection in both directions, delivery may repeat so every handler tolerates a duplicate, and a client that cannot keep up is dropped rather than buffered without bound. A client sends a heartbeat every `15s` and the server closes a silent connection after `45s`. A dropped connection is retried with exponential backoff from `500ms` to `10s`, with jitter. **Long-polling fallbacks are excluded, deliberately**: a player receiving strokes in one-second batches guesses late every round and cannot tell that the game is broken rather than that they are slow, so a player who cannot hold an open connection is told so plainly instead.

A guess must reach every other player in the room in well under `200ms` of the app receiving it. That is the promise the whole product rests on.

**The architecture boundary that governs everything else: the client renders, the server decides.** The server owns the room, the word, the clock, the scores and the turn order, and trusts no client statement about any of them; the client owns rendering, input capture, local mute and local preferences, and holds no secret, decides no outcome and runs no game clock. Keep the module that holds the current word small and separate, with exactly one place in the whole program allowed to put a word into an outbound message, so that one module can be read and trusted rather than the whole program having to be watched forever. Do not build a second copy of the rules on the client, do not run a countdown there, and do not build one shared state object and send it to everybody.

Every response carries the standard security headers, including a strict transport policy and a content-type policy that forbids sniffing, on every route including the not-found page. Nothing the browser downloads contains a credential, an API key or an administrative token.

Player-supplied text reaches other players' screens in four places: a display name, a chat line, a custom word and a room code. All four are rendered as text and never as markup, are length-checked on the server, are normalized before storage so bidirectional-override and zero-width characters cannot be used to spoof a name, and have control characters stripped. A name appears in the player list, in the chat and in the turn banner, and each of those is a separate place to get it wrong.

Performance is a frame problem on the client and a fan-out problem on the server. One drawer in a room of twenty multiplies every batch by twenty, and that ratio sets the cost of the whole product. Incoming strokes are painted incrementally on top of what is already there rather than by re-rendering the whole list, and a full re-render happens only on resize and on replay. The deterministic raster behind a fill is computed once per fill, not per frame. Audio nodes are pooled. The player list re-renders on change rather than on every clock tick, and chat rows are recycled beyond a cap. First-load script stays at or under `250000` bytes, stylesheets at or under `50000` bytes, one subset font face at or under `120000` bytes, and **no image file and no audio file ships at all**: every avatar layer, every interface mark, the doodle tile and all seven sounds are generated. Non-Latin ranges load on demand keyed by the selected language, because a Latin-only subset renders the mask as empty boxes for a large share of the audience.

**Metrics.** Aggregate counts are recorded without identities: rooms live and by state, players live, stroke batches per second and the fan-out ratio, guess latency from arrival to broadcast, turns ending with nobody guessing, reconnections and reconnections that missed the grace window, rate-limit rejections by kind, and reports filed. The turns-with-no-guesses count earns its place: a rising value means the word list has bad entries in it and it is the only signal that says so.

**Routing and leases.** A join carrying a code is routed to the process the registry names for that code; a join without one is matchmade first and then routed the same way. The owning process refreshes its registry lease every `10s`, and leases that expire mean the room is presumed dead, its registry entry is removed and its code is retired.

**Failure, stated as a deliberate limit.** A room's state is owned by one process and every message for that room is handled there. If that process is lost, the room is lost: players are told plainly that the room ended and are offered a new one with their name intact, rather than being left on a silent hang. Replicating a live room would mean replicating its stroke buffer and its clock at full rate, which roughly doubles the cost of the product to guard a party game against minutes a month, so the trade is refused on purpose. A process holds a bounded number of rooms, so one failure affects a known number of games, and a deploy drains rather than kills: it stops accepting new rooms, lets the games it holds run to completion, moves players to a new room at `game_end`, and exits when empty or after `2h`.

## Data model

Nine tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a person can sign in.

**What is never written to any table.** Chat text, except inside a report. Drawings, except as the stroke buffer captured inside a report. Network addresses: the rate-limit counters are keyed by a salted hash of the address with a rotating salt and they expire. The current word of any live room. No table holds a row per guest player, and a room's live state - its players, its scores, its drawer, its word, its deadline and its stroke buffer - lives in the memory of the process that owns the room and in no table.

`accounts` - id, email (unique), display name (unique), password hash, role (`player` or `moderator`), created at.

`rooms` - the registry row: code (unique among live rooms), kind (`public` or `private`), `lang` for the room's word-list language, which is what matchmaking partitioning reads, state (`lobby`, `choosing`, `drawing`, `turn_end`, `round_end`, `game_end`), player count, cap, owner account (nullable, set for a room created by a signed-in player), lease expiry, created at, closed at, retired until. The registry is a directory and holds no game state: if it is lost, running rooms continue and only new joins are affected.

`room_settings` - room code, max players, rounds, turn seconds, word choices, hints, word mode, custom words only. One row per room.

`custom_words` - room code, text, position. Filtered and length-checked before insert.

`words` - id, language, text, difficulty (`easy`, `medium` or `hard`). At least `2000` English rows.

`filter_terms` - id, language, term. Matched against normalized text.

`reports` - id, room code, reporter seat identifier, reported seat identifier, captured stroke buffer, captured chat tail, created at, expires at (`30d` after creation), reviewed at, reviewed by account. Readable by a `moderator` only.

`rate_counters` - salted address hash, bucket, count, window start. Rows expire in minutes.

`turn_results` - id, room code, round, whether anybody guessed, guesser count, created at. Counts only: no seat identifier, no name and no word.

**Invariants, stated as properties of the running system.**

- A room code is unique among live rooms, and a code stays unusable for `1h` after its room closes.
- A room's player count never exceeds its cap. Two joins arriving at the same instant for the last seat of `Friday Night Doodles` do not both succeed: exactly one is seated, the other is sent to another room, and the room never holds five players. This holds under real concurrency, and a failed join leaves no seat held and no partial record behind.
- A guess is scored at most once per seat per turn, however many times the same guess arrives.
- A report is readable only by an account whose role is `moderator`.
- A private room's existence, name, player count, settings and state are not readable by a caller holding neither its code nor a seat token for it.
- Settings are within their stated ranges at all times, and do not change between the start and the end of a game.
- Derived values are computed on read: standings, ranks, a player's rank and the fan-out ratio are never stored.

**Seed data.** Four accounts as listed in User roles. One private room named `Friday Night Doodles`, code `PARROT42`, cap `4`, language `English`, owned by `player@example.com`, seated by `Ivy`, `Bo` and `Ren`, so exactly one seat is left. One public room named `Open Table`, cap `8`, language `English`, in `lobby`, with one seat used. An English word list of at least `2000` entries across the three difficulties. A filter list for `English`. One report already filed against a seat in `Friday Night Doodles` and not yet reviewed.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

Everything in this section is the visual and structural detail the room and the landing route need. It carries no colour values and no motion timings: those are described in `## UI/UX notes` by role and by character, and the values are yours.

### Information architecture

The information architecture is deliberately flat: two documents, a front door, a create route and a room. There is no menu, no header, no tab strip and no breadcrumb anywhere in the product, and the only outbound links in it are the four in the footer.

### The scaling rule

One layout unit and one base text size generate the whole interface, and every panel, control, avatar and toolbar is a multiple or a fraction of the unit. A custom property holds the **real measured viewport height** in pixels, recomputed on resize and on orientation change, and the layout uses it instead of the browser's own viewport-height unit. Mobile browsers report a height that includes chrome which then hides, and report it again wrongly when the on-screen keyboard opens, and a game that must fit exactly on one screen cannot use a unit that is wrong by the height of a toolbar. The case that matters most is the keyboard opening to type a guess: the canvas gives up space and the input is never covered.

A second custom property holds how many player rows fit at the current unit. It is a sentinel meaning unpaged on a large screen, and it engages only when the list cannot show every player.

### The landing route

Top to bottom: the wordmark and the avatar row; the join panel; a boxed discovery panel beside the join panel and never above it; three columns headed `About`, `News` and `How to play`; the footer.

The join panel is the front door and it is four controls. A name field with a placeholder inviting a name. A language control listing the supported word lists. The avatar builder: four layers, each with a left and a right arrow, plus one control that sets all four at random. Then the primary action, full width, and the secondary action beneath it, full width and quieter. The primary action is the largest control on the page and is visually dominant, because most arrivals want a game immediately and the private room is the considered choice.

The `How to play` column is five steps with position dots, in the order given in `## Core features`. The `About` and `News` columns are containers for the operator's own prose: build the container and its styling, and supply your own words. `News` is a dated, titled, list-formatted changelog with a signature. The discovery panel is a boxed list of three outbound links under a discovery heading; it is the only commercial surface in the product, it never expands, never overlays anything and never delays the join panel, and any commercial or analytics code loads after the game is already playable and never on the path to it.

The footer is four centred links - `Contact`, `Terms of Service`, `Credits`, `Privacy` - with the responsibility notice beneath them.

### The room

Four regions, one screen, no page scroll at any size.

**The game bar** spans the top and carries the round counter, the clock with its drawn clock mark and the house shadow, and the word or its mask with a caption beneath it. This element is the single place in the interface where the secret is most likely to leak, because the drawer's version and a guesser's version are the same component fed different data. The bar drops in at turn start, and each revealed letter animates individually.

**The player list** runs down the left. A row is an avatar, a name, a score and a rank. Rows alternate. A row turns green the moment that player has guessed, and carries a text state beside the colour. The viewing player's own row is distinctly coloured so they can find themselves at a glance, and takes a second, deeper colour once they have guessed. The owner's avatar wears a crown, and the owner state is also in text. Clicking a row opens the player modal. The list pages when it cannot show every player at the current unit.

**The canvas** sits in the centre and dominates. Its toolbar sits beneath it and is present only for the drawer, which the server enforces independently. The toolbar carries a pen with several size steps, a fill, an eraser which is the background colour as a brush, an undo, a clear, and a fixed colour grid. Colours are selectable with both pointer buttons, so a player holds a primary and a secondary colour at once, and pressure is used where the device reports it, mapping within the current size step. Toolbar targets are at least `44px` at the rendered scale. A single-finger drag draws; two-finger gestures do not draw; a stroke that begins with a large contact area is ignored as a palm; and the canvas prevents the page from scrolling or bouncing under a drag, without which drawing on a phone drags the whole page around and the game is unplayable.

**The chat** runs down the right. Rows alternate and fade in on arrival. Kind is carried by colour and by text together. The already-guessed channel is a visibly distinct channel with its own row background, not a styled variant of an ordinary row. The input carries a character counter. The list is pinned to the newest line unless the reader has scrolled up, in which case it leaves them alone: a chat that pulls a reader back to the bottom while they are reading is a chat they cannot read.

**The player modal** opens from a row and carries kick and ban for the owner, vote-kick for anybody, a local mute, a report and an invite control. It closes on Escape and returns focus to the row that opened it. Modals blur what is behind them and carry the product's one large radius.

**Game end** is a full-page podium with the top players, the winner's name emphasised and celebrated, then a return to the lobby.

### The loading overlay

Shown while the room connects. It fades in while blurring the page behind it and its content drops into place from above. It carries a state message naming which of connecting, finding a room and joining is happening. A bare spinner in front of somebody waiting on a busy matchmaker reads as a broken game.

### Zero-asset substitution

Nothing in this product is fetched as a binary, and every asset class the product would otherwise ship has a substitution here. Avatars are drawn as inline vector geometry: a rounded blob outline with a heavy stroke filled from the palette, an eye set and a mouth drawn from coordinate tables at common origins, and an accessory drawn at a common anchor above the head with an empty variant. That makes the number of avatar variants a data question rather than an asset question. Interface marks are drawn the same way: the crown a five-point zigzag on a base bar, the clock a circle with two hands and four ticks, the pen a sheared rectangle with a nib triangle, the size control three filled circles at increasing radii, the randomise mark a rounded square with five dots, the selection arrow a triangle clipped from a square and rotated per side, and the thumbs a rounded rectangle plus a curved hand shape mirrored for the second.

The doodle ground is generated: simple single-stroke doodles, each a short path, scattered on a grid with per-cell rotation and jitter, seeded so the tile is stable between builds, and generated so its edges wrap seamlessly when it repeats. It is sparse enough that panel text over it stays legible, and two copies at different offsets drive the drifting waves. The doodles are drawn from the same vocabulary as the word list, which costs nothing and is worth keeping.

All seven sounds are synthesised at play time: a rising two-note interval with a soft attack for a turn beginning; a short quiet filtered noise burst once per second for the tick, starting when `10s` remain; a bright ascending three-note arpeggio through a low-pass filter for a correct guess; that arpeggio extended and resolved upward for a turn that ended with somebody guessing; a descending filtered minor interval for a turn that ended with nobody guessing; a short rising blip for a join and its falling twin for a leave. The audio context is created on first interaction and never before. Every sound has an attack and a release, because a bare oscillator started and stopped clicks, and that one rule is the difference between synthesised audio that sounds intentional and synthesised audio that sounds broken. One master gain node is driven by the mute control.

One type face is loaded, subset to Latin plus the ranges the offered languages need, with the swap behaviour so text is readable before it arrives.

### Accessibility floors

Body text and its background meet a contrast ratio of at least `4.5:1`, on the landing route and inside the room. Interactive targets are at least `44px` in their smallest dimension at the rendered scale. Every content image equivalent carries a text alternative, and a purely decorative shape declares itself decorative rather than being announced. One heading per route with no skipped levels. The document declares its language, and the mask declares the word list's language. The four room regions are labelled landmarks. New chat lines are announced politely; a correct guess is announced; the countdown is never announced.

### Copy and in-game strings

| Slot | Copy |
|---|---|
| Landing title | `Doodlerush - Free Multiplayer Drawing & Guessing Game` |
| Primary action | `Play!` |
| Secondary action | `Create Private Room` |
| Discovery panel heading | `Discover more` |
| Column headings | `About`, `News`, `How to play` |
| Footer links | `Contact`, `Terms of Service`, `Credits`, `Privacy` |
| Footer notice | a disclaimer that the operator is not responsible for player-generated drawings, messages and names |
| Drawer instruction | `DRAW THIS` |
| Reveal | `The word was` |
| Room settings labels | `Players`, `Language`, `Rounds`, `Draw time`, `Word Count`, `Hints`, `Word Mode`, `Custom Words`, `Use custom words only` |

System messages in the chat, each in its own colour role and each carrying its meaning in text as well: a player joined; a player left; a player guessed the word, **without the word**; a private note that a guess was close, **without repeating it**; a player is now drawing; a player is now the room owner.

The `About` prose, the `News` posts and the terms and privacy documents are the operator's own writing. Build the containers and supply your own text; do not copy another operator's legal text.

## Constraints

- Single tenancy. There are no organisations, no workspaces and no tenant boundary beyond the room.
- No voice, no video and no media transport of any kind. A voice channel is not in this product and none may be added.
- No image upload, no file attachment and no object store. Every visual in the product is drawn or generated.
- No payment, no paid tier, no subscription and no commercial transaction.
- No private messaging between players outside a room.
- No browsable list of rooms, public or private, and no search that reaches one.
- No automated classification of drawn content, and no claim to have any.
- No email, no push notification and no messaging channel leaving the product.
- No multi-process room ownership, no failover of a live room, no resharding and no multi-region placement.
- No native application and no installable package.
- No external network calls at run time. Everything the product needs is in this environment.
- The app stays responsive with `20` players in a room, `4000` strokes in a turn and `60` stroke batches per second per drawer.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{ "email", "password", "display_name" }` | the created account |
| `POST /api/auth/login` | `{ "email", "password" }` | `{ "token", "account" }` |
| `GET /api/me` | - | the signed-in account |
| `POST /api/matchmake` | `{ "language" }` | `{ "code" }` |
| `POST /api/rooms` | `{ "name", "language", "settings" }` | `{ "code", "name", "invite_url", "settings" }` |
| `GET /api/rooms/{code}` | - | `{ "code", "name", "kind", "state", "players", "cap", "language" }` |
| `POST /api/rooms/{code}/join` | `{ "display_name", "avatar", "seat_token" }` | `{ "seat_token", "player_id", "room" }` |
| `GET /api/rooms/{code}/state` | header `X-Seat-Token` | the per-recipient snapshot |
| `GET /api/rooms/{code}/events` | header `X-Seat-Token` | the open event stream for this seat |
| `POST /api/rooms/{code}/start` | - | the room state |
| `PATCH /api/rooms/{code}/settings` | a settings patch | the settings |
| `POST /api/rooms/{code}/word-choice` | `{ "index" }` | the room state |
| `POST /api/rooms/{code}/guess` | `{ "text" }` | `{ "outcome" }`, one of `correct`, `close` or `chat` |
| `POST /api/rooms/{code}/strokes` | `{ "batch": [ { "sid", "c", "w", "p" } ] }` | the accepted count |
| `POST /api/rooms/{code}/canvas-op` | `{ "sid", "op" }`, `op` one of `undo`, `clear`, `fill` | the operation |
| `POST /api/rooms/{code}/votes` | `{ "kind", "target" }` | the open vote |
| `POST /api/rooms/{code}/leave` | - | no content |
| `POST /api/reports` | `{ "code", "target" }` | the created report |
| `GET /api/reports` | - | a top-level JSON array of reports |
| `PATCH /api/reports/{id}` | `{ "reviewed": true }` | the report |

The snapshot returned by `GET /api/rooms/{code}/state` carries `state`, `settings`, `players`, `round`, `rounds`, `drawer`, `word_mask`, `deadline`, `canvas`, `chat` and `you`. It carries `word` **only** when the caller's seat is the current drawer's, or once the turn has ended. A player record carries an id, a name, an avatar, a score, whether they have guessed this turn, whether they are the host and whether they are connected. It never carries a seat token or an address.

Bearer authentication is required on `GET /api/me`, `GET /api/reports`, `PATCH /api/reports/{id}` and `/account`. Room endpoints authenticate by the seat token for that room, supplied in `X-Seat-Token`. `GET /api/health`, `POST /api/auth/login` and `POST /api/auth/signup` need neither. A list endpoint returns a top-level JSON array. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never as a server error and never as a silent success.

### No mocks

PostgreSQL is where this product's durable records actually live. An in-memory list of reports that disappears on restart, a word list compiled into the application bundle instead of read from the database, a seeded room that exists only as a constant in the front end, or a report whose captured strokes are written to the app container's own filesystem are all contract violations however good the interface looks. The named provider is the fact - the app's UI and its own tables can only reflect what lives in the provider, never substitute for it.

The one deliberate exception is the live room itself, which is memory by design: a room's players, scores, drawer, word, deadline and stroke buffer belong to the process that owns the room, and the word in particular is written to no table.

## Definition of done

A visitor types a name, builds an avatar and is in a game with strangers in one press, or makes a private room and shares its link. While a turn runs, the drawer sees the word and nobody else can find it anywhere in what their browser receives. Guesses score on speed, the drawer scores when the room works it out, the turn ends the moment everybody has, and a player who drops mid-turn returns to their own seat with their score and their guess intact.
