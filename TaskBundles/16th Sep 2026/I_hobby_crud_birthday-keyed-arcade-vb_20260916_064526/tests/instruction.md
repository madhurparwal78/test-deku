# Daykin

Build and deploy a working web application from this brief. There is no
starting codebase. When you are done, a stranger must be able to open the app
in a browser, type the twenty-ninth of February into the birthday finder,
receive their sixteen characters, keep one, reload the page, and find it still
there, without hitting an error page.

The same stranger must then be able to change their device clock to any date in
any year, type the same day and month again, and receive **exactly the same
sixteen characters**. Resolution is arithmetic, not a lookup and not a guess. A
build whose answer moves when the clock moves has failed the one promise this
product makes, and a check that resolves the same pair twice across a clock
change will see it.

## Overview

Daykin is a character playground and a small arcade. A day and a month resolve
to one character in each of sixteen series, and around that sit ten browser
games, a hub, a timeline and an awards scene.

**The browser is the entire runtime for everything the reader does.** There are
no accounts, no sign-in, no other readers, and nothing a reader does leaves
their device. Their collection, their scores, their currency and their
preferences live on the device and nowhere else.

The server serves the built application and publishes the **catalogue**: the
sixteen series, the colour for each of the 366 days, the hub order, the awards
record, the wheel categories, the oracle decks, the daily prompts and the prize
odds. The catalogue is content the product ships and is read-only. Nothing a
reader produces is ever sent to it.

Daykin is not: an account system, a shared leaderboard, a shop, or a social
feed.

## User roles

There is one role, **Visitor**, and no sign-in of any kind. Every route is
public and every reader is anonymous.

The trust boundary is not a login, it is the edge of the device. **Everything
arriving from outside is untrusted input, validated on arrival exactly as if it
had been typed**: a pasted share link, an imported file, and a blob read back
from storage that an older version wrote or a person hand-edited.

| Surface | Trusted | Rule |
|---|---|---|
| The birthday finder | no | validity is a property of the pair, never of either field |
| A share link | no | every field re-validated; a link carries inputs, never a result |
| An import file | no | validated whole before anything is written |
| Stored state | no | a shape that does not validate is discarded, and the product opens |
| The catalogue | yes | read-only, served by the application |

A refusal always says which part is impossible. It never fails silently and it
never leaves the reader on a blank screen.

## Core features

### The resolver
A day and a month resolve to an ordinal from `1` to `366`, counting from the
first of January in a leap year, and that ordinal selects one member from each
of the sixteen series. **No year is asked for and none may be required.** The
twenty-ninth of February is an ordinary day with an ordinary character.

### Validity
A pair is valid when that day exists in that month in a leap year. The
thirty-first of April is refused; the same thirty-first beside January is not.
A day of zero and a month outside one to twelve are refused. The refusal reads
`Oops! This date doesn't exist.` and names what is impossible.

### The collection
A resolved character can be kept on the device, with the background and colour
it was seen with. The same character kept twice is one entry. The collection is
browsable, can run to several hundred entries, and a view over it does not hold
every character at once.

### The arcade
Ten games from a hub: Shaking, Memory, Rocket, Puzzle, Challenge, Wheel, Wiggle,
Picks, Gotcha, Love. Each carries the way back plus the next and previous game in
that order, has ready, running, paused and over, and one shell owns the clock,
the score readout and the end state.

### The shared board
One seed per local day drives every source of chance, so two readers playing on
the same day meet the same boards and a reader who reloads meets the board they
left. Each game draws from its own named stream, so spinning the wheel does not
change what the tapper does next.

### The currency
Gotcha exchanges soul shards at `COMMON`, `RARE` and `LEGENDARY`. A balance is
derived from a ledger of credits and debits, never stored as a total, never goes
below zero, and is one balance across two open tabs. Odds are published where
the prices are.

### Sharing and moving
A character, a passport and a finished run each encode into a link that carries
the inputs and re-derives the result. The whole store exports to one file and
imports back as a **merge**, and each kind of state merges by its own rule.

### The record
An awards scene and a dated timeline render from one award record in one date
format. The series list renders from the same data on the home route and the hub.

### The site
A privacy page and a terms page reachable from every footer. The birthday finder
refuses a submission arriving faster than a person can type, or one that fills a
field no person can see.

## User flow

The chrome is a **top navigation** present on every route, carrying a menu, an
awards badge, a footer and the legal notice. The collection, an import and
removal each happen on **their own route**, never in a layer over the page.

| Route | Purpose |
|---|---|
| `/` | the birthday finder, the origin story, the sixteen series |
| `/index.html` | redirects permanently to `/` |
| `/games` | the hub carousel of ten covers |
| `/universe` | the awards scene |
| `/roadmap` | the dated timeline |
| `/whack-a-mole` `/memory` `/puzzle` `/rocket` `/wiggle` | five games |
| `/wheel` `/picks` `/challenge` `/love` `/gotcha` | five games |
| `/collection` `/import` `/my-data` | the reader's own store |

**Entry.** Every route is public and opens directly. A route already visited
opens again without a network, and a game already loaded stays playable offline.
There is nowhere to sign in and nothing asks.

**Journeys.**
1. A reader types `29` and `02`, sees sixteen characters, chooses a background
   and a colour, and keeps one. The kept entry appears **at once**, marked as
   kept, before the write to storage has confirmed; if the write is refused the
   entry returns to unkept with the reason in place.
2. The reader reloads and the kept character is still in the collection, with
   the background it was kept with.
3. The reader types `31` and `04` and reads the refusal.
4. The reader opens `/puzzle`, shuffles, and solves it. Every shuffle is
   solvable. An undo returns the board and the move count together.
5. The reader opens `/gotcha`, exchanges at `COMMON`, and the balance falls by
   the published price. Pressing exchange twice quickly leaves a balance they
   could have predicted.

**States.** Every list has an empty state naming what to do; every asynchronous
surface a loading state shaped like what replaces it; every refusal names what
failed. Nothing crashes to a blank page.

## UI/UX notes

Daykin is playful and a little loud, and the arcade is louder than the front
door. The north star is that a reader understands what they are looking at
before they touch anything.

**Each route paints its own world, and that is the design.** A route declares
its ground, ink and accent, and the chrome inherits them. One palette across all
fifteen routes removes what makes the arcade feel like ten machines.

Colour is carried by role, never as a value. The home ground is a **mid, soft
orange**, the passport a **mid, vivid violet** haze, the prize machine
**near-black neutral**. The arcade set is neon at full strength: **mid, vivid
teal**, **mid, vivid green**, **mid, vivid magenta**, **mid, vivid amber**.
Surfaces and text are **near-white neutral** and **near-black neutral**; the
chrome hover is a **light, soft magenta**.

Type is **Playfair Display** for ceremony and **Comfortaa** for the arcade.
That pairing is the voice and it survives, on a named scale stated under
`## Front-end specification`.

Motion is springy: the house curve overshoots slightly and settles back. Nothing
is quite still, yet every transition names the properties it moves rather than
animating everything. Under a request for less motion the idles hold, the
carousel changes selection without travelling, and **every game stays playable
rather than merely still**.

Every control declares its resting, hover, active, focus and disabled
appearance. Focus is visible against that route's own ground, which is hard when
the ground is saturated and dark, and contrast is checked against that ground
rather than a notional white. No state is carried by colour alone: the neon teal
and green read alike to many people.

Every content image carries alternative text. Targets measure at least 44px both
ways. The layout holds at four named **breakpoints**, and at the narrow
**viewport** the hub becomes a swipe and the prize machine asks to be turned.

## Technical requirements

### The stack

Build Daykin as a **single-page application over a JSON catalogue**. The server
is **Flask**; the browser half is **Vue 3 built with Vite**. The server has two
jobs and no others: serve the production build, and publish the read-only
catalogue below. It holds no reader state, accepts no reader write, and has no
session of any kind.

### Providers

| Slot | Provider | Read from |
|---|---|---|
| Datastore | `postgres` | `DATABASE_URL` and `DB_URL`, which carry the same value |

`postgres` holds the catalogue only. It is already running and reachable at
those variables; do not download, install, compile or start a copy of it. On
first start the application creates its schema and loads the catalogue described
under `## Data model` from a stated seed, so two builds publish identical
content.

### The resolver, and why it is server-testable

The resolver is a pure function of the day and the month: no randomness, no
clock, no locale, no stored state. It is published at `GET /api/resolve` so it
can be exercised without a browser, and the browser half calls the same
endpoint rather than carrying a second copy of the arithmetic.

`GET /api/resolve?day=<1-31>&month=<1-12>` returns, for a valid pair:

```
{"valid": true, "ordinal": <1-366>,
 "members": [{"series": <1-16>, "label": <366..5856>, "number": <1-5856>}, ...],
 "colour": {"phase": "<one of five>", "name": "<string>"}}
```

`members` carries exactly sixteen entries, one per series, in series order. A
member's `number` is its position in the whole collection, so series `s` and
ordinal `o` give `number = (s - 1) * 366 + o`, and the sixteenth series ends at
`5856`. The `label` is the series upper bound and the sixteen labels are `366`,
`732`, `1098`, `1464`, `1830`, `2196`, `2562`, `2928`, `3294`, `3660`, `4026`,
`4392`, `4758`, `5124`, `5490` and `5856`.

For an invalid pair the endpoint answers `400` with
`{"valid": false, "error": "Oops! This date doesn't exist.", "impossible": "<which part>"}`.

**The ordinal counts from the first of January in a leap year.** The
twenty-ninth of February is ordinal `60`, the first of March is `61`, and the
thirty-first of December is `366`. A build that counts in a common year is
wrong from the first of March onward and wrong about the one date this product
is named for. The first of each month resolves to `1`, `32`, `61`, `92`, `122`,
`153`, `183`, `214`, `245`, `275`, `306` and `336` in order.

Validity is a property of the pair. A day of `31` is good beside month `01` and
impossible beside month `04`; neither field is individually wrong. The
thirtieth of February is impossible, a day of `0` is impossible, and a month
outside `1` to `12` is impossible.

### The colour of a day, and the remainder

Every one of the 366 days carries a colour drawn from the Five Phases, and the
assignment is data a person who cannot write code can edit. **366 does not
divide by 5.** The build states the rule it uses and the rule accounts for the
remainder; a scheme that silently truncates has got the last day of the cycle
wrong, and the last day is the thirty-first of December. `GET /api/colours`
returns all 366 assignments with the rule stated in a `rule` field.

The five phases are named `Wood`, `Fire`, `Earth`, `Metal` and `Water`, in that
order. Every `phase` the API publishes, on a day colour, a resolution or a
catalogue row, is one of those five names.

### Reading the catalogue at scale

Catalogue reads are paginated. `GET /api/characters` walks all 5856 members and
accepts a `page_size` the caller chooses, from `1` to `500`, returning a keyset
cursor beside the rows. Each row carries `number`, `series`, `ordinal` and
`phase`.
Paging is by keyset cursor over a stable ordering and never by an offset cursor over a large result, because an offset cursor re-scans everything it skips.
Where the ordering is not unique the build appends a deterministic tiebreak, since an unstable keyset cursor makes paging skip and repeat rows.
Every response carries an opaque cursor the caller never parses, alongside `next_cursor`, `has_more` and `total_count`.

Two orderings are offered through an `order` parameter. `number`, the default,
orders by member number. `phase` orders members by their day's phase, in the
phase order above, and within one phase by `number` ascending. Hundreds of
members share each phase, which is exactly the ordering a keyset cursor with no
tiebreak pages wrongly. A cursor belongs to the ordering that issued it.

A read the catalogue cannot serve as asked answers `400` with
`{"error": "<reason>"}` rather than guessing or failing: a cursor this server did
not issue, a cursor issued under the other ordering, a `page_size` outside `1` to
`500`, and an `order` other than `number` or `phase`.

Walking `/api/characters` by following `next_cursor` until `has_more` is false
must yield exactly `5856` members, each `number` appearing once, and exactly
`366` members in each of the sixteen series. The same walk under `order=phase`
yields the same `5856`, each once, in phase order and then number order.

### What the application records

The application emits structured logs, one JSON object per line, for every request it serves.
Those structured logs are written to stdout and are also appended to /tmp/app.log, so the same record survives in both places.
Every line written to /tmp/app.log carries the request_id assigned to that request on arrival, including lines written by work the request starts.
A line reaching stdout without that identifier cannot be joined to the request that caused it, so the JSON logs treat the field as mandatory.
Every HTTP response also carries that same identifier in an `X-Request-Id` header, so a reader, a proxy or an operator outside the process can quote the request without reading the log at all. Two requests never share an identifier.

Page views are recorded with their route and the time, readable at
`GET /api/page-views`. Nothing else about a reader is recorded anywhere.

### Client state and persistence: everything a reader does stays on the device

The collection, the per-game bests and recent attempts, the daily prompt
history, the shard ledger and the preferences live in the browser under a single
namespaced root with a declared version. Reading is defensive: a stored shape
that does not validate is discarded and replaced with the default, and the
product opens. The store can be unavailable, and every feature degrades to its
session-only behaviour and says so once rather than failing at the moment the
reader finishes something. Nothing stored is required to render the first paint.

A day-and-month in storage is stored as a day and a month, never as a date
object, and survives a round trip unchanged in every locale.

When the browser refuses to store anything at all, the product says so in a
notice reading `This device won't let the page save anything, so nothing will be kept after you leave.`,
shown once on the page and left in place until the reader leaves the page, and
every feature carries on for the rest of the visit, including keeping, the
purse and its welcome grant.

### The birthday finder and the collection, as a keyboard and a screen reader meet them

The finder is a group named `Birthday` holding two text fields named `Day` and
`Month` and a `Find` button. Beside it sit two radio groups: `Background`,
offering `plain`, `confetti`, `stripes` and `clouds`, and `Colour`, offering the
five phases. The choices in force when a character is kept are the ones it
records. A valid pair lists its sixteen characters in series order in a list
named `Your sixteen`. Each item shows `Daykin #<number>` as its own text and
offers a `Keep Daykin #<number>` button and a `Share Daykin #<number>` button.
Keeping shows `Kept. It's in your collection.`, and keeping a character that is
already kept adds nothing.

`/collection` lists what is kept in a list named `Collection`. Each item shows
`Daykin #<number>`, `Kept <YYYY-MM-DD>` in the reader's local date,
`Background: <background>` and `Colour: <colour>`. With nothing kept the route
reads `No characters kept yet. Find one from your birthday.`

The menu's three-bar control is a button named `Menu`, and the panel it opens is
a dialog also named `Menu`.

### The shard ledger

A balance is derived from a ledger of credits and debits rather than stored as a
total. It never goes below zero. A change is atomic: a reader closing the tab
mid-exchange leaves either the debit and the reward, or neither. **Two tabs are
one reader**: the same game open twice shares one balance, and spending in one
becomes visible in the other. An exchange the balance cannot afford is refused
before anything is drawn, and the refusal states both the price and the balance.
Pressing exchange twice quickly leaves a balance the reader could have
predicted, by the rule stated below.

`/gotcha` opens on its boot screen with an `ENTER` button, and pressing it shows
the machine. The machine states `Today is <YYYY-MM-DD>` for the device's local
day, shows the balance as `Balance: <n> SOUL SHARDS`, and offers
`Exchange COMMON`, `Exchange RARE` and `Exchange LEGENDARY`.

A ledger holding no entry with the id `welcome` receives one, a credit of `300`,
when `/gotcha` opens. A first visit therefore starts with something to spend,
and two devices whose ledgers are combined count that welcome once.

Once per local day the machine offers `Claim daily shards`, a credit of `50`.
The button stays on screen and is disabled whenever there is nothing to claim,
and after a claim the machine reads `Claimed for <YYYY-MM-DD>`.

An exchange the balance can afford debits the price and shows what was drawn in
a region named `Reward` with a `Continue` button. From the press until
`Continue`, the exchange buttons accept no further press: two quick presses are
one exchange. An exchange the balance cannot afford draws nothing and reads
`This costs <price> SOUL SHARDS and your balance is <balance>.`

A spend in one open tab shows as the balance in every other open tab without a
reload, and a spend pressed in a tab still showing an old balance is taken from
the true one.

### The day seed

One seed per local day drives every source of chance. It is derived from the
local date alone and is never stored, because a derived value that is also
stored can disagree with itself. Each consumer draws from its own named stream,
seeded from the day seed and the stream's own name, and advanced only by its own
consumer; ten games sharing one sequence entangle each other. A stream is
reproducible from its start, which is what makes replay possible at all. The
day's **first** attempt at a game is the shared board; later attempts advance a
per-attempt counter, and the build states which of its randomness is shared and
which is free.

The local day is the reader's own calendar date in the reader's own timezone.
Two readers in different timezones whose calendars read the same date meet one
board, and a reader whose calendar has turned over meets a new one.

### Clock integrity

The local day is the reader's own, and crossing a timezone is a normal event
rather than an error. The product records the latest local day it has seen; a
day earlier than that is a clock correction, a flight, or a replay attempt, and
the build states which it assumes and what it does. **What it does must not
include destroying anything the reader earned.** Nothing irreversible keys off
the clock alone: where an entitlement is once a day, the record of having
claimed it is keyed to the day it was claimed for, so moving the clock forward
and back yields one claim per day rather than one per adjustment. The interface
states which day it believes it is wherever a daily thing is shown.

The daily shard claim is offered only for the latest local day the product has
seen, and only once for that day. While the device reads a day earlier than
that, the claim button is disabled, the latest seen day stays where it was, and
the machine reads `Your device's date went backwards. Nothing you've earned has been touched.`
Nothing stored is removed or rewritten because the date moved.

### Links, export and merge

A character, a passport and a finished run each encode into a link. **A link
carries the inputs, never the outputs**: a shared character carries the day, the
month, the series, the background and the colour, and the recipient's device
re-derives the character. A link that carried the rendered result would let a
sender claim a character the resolver would never produce. The encoding is
versioned and the version travels inside the link; a link from an older version
either decodes to something the current product understands or is refused with a
reason, and never decodes into a shape the product then treats as current. Every
field is validated on arrival exactly as if typed. The interface warns that the
link contains a birthday **before** the link exists.

**The character link.** A character link is the product's own home address with
one query parameter, `/?share=<token>`. The token is the URL-safe base64 of a
JSON object, with or without padding:

```
{"v": 2, "kind": "character", "day": 29, "month": 2, "series": 3,
 "background": "stripes", "colour": "Fire"}
```

`v` is the link version, and `2` is current. A link the product creates carries
exactly those seven fields and no other. On arrival the day and month must be a
valid pair, `series` a whole number from `1` to `16`, `background` one of the
four backgrounds and `colour` one of the five phases. Any other field is
ignored, so a number, a label or a name placed inside a link never reaches the
screen. A valid link shows a region named `Shared character` holding
`Daykin #<number>` re-derived from its inputs, with `Background: <background>`
and `Colour: <colour>`. A link whose `v` is `1` reads
`That link was made by an older version of this page.`; any other link that
fails reads `That link doesn't describe anything this page can show.` Either way
the birthday finder is still there to use. A passport and a finished run choose
their own `kind` and fields under the same rules.

Pressing `Share Daykin #<number>` shows
`The link will contain your birthday. Anyone you send it to will see it.` and a
`Create link` button. Only pressing that button produces the link, in a text
field named `Link`.

The whole store exports to one file and imports back, and **import is a merge,
not a replacement**. Each kind of state merges by its own rule and the rules
differ: the collection is a set and merges by union, keeping the earlier
keeping-time; a best score is a maximum; recent attempts are a union ordered by
time and truncated; the daily history is keyed by day and two records for one
day is a conflict the reader is asked about. **The shard ledger is none of
these.** Both sides have spent independently, and adding two balances together
invents currency that was never earned; the rule is stated below. An import is
validated whole before anything is written, is previewed before it is applied,
can be declined, and is undoable to the state immediately before it. A file that
fails leaves the store untouched.

**The store file.** `/import` offers `Export store`, which saves one JSON file,
and the same shape is what `/import` reads:

```
{"format": "daykin-store", "version": 2,
 "collection": [{"series": 3, "day": 29, "month": 2, "background": "stripes",
                 "colour": "Fire", "keptAt": "2026-03-05T12:00:00Z"}],
 "bests": {"<game key>": {"best": 41, "timed": true}},
 "attempts": {"<game key>": [{"score": 12, "timed": true, "at": "<ISO 8601>"}]},
 "dailyHistory": {"2026-10-14": "<prompt key>"},
 "shardLedger": [{"id": "welcome", "kind": "credit", "amount": 300,
                  "reason": "welcome", "at": "2026-10-01T09:00:00Z"}],
 "preferences": {"mute": false, "reducedMotion": false, "background": "plain",
                 "savedAt": "<ISO 8601>", "device": "<name>"},
 "seenDay": "2026-10-14"}
```

A kind may be left out, which means empty. A collection entry records its inputs
and never its number, which the product re-derives.

A file is unreadable when it is not JSON; when `format` is not `daykin-store` or
`version` is not `2`; when any collection entry carries an impossible day and
month, a series outside `1` to `16`, a background or colour outside the stated
sets, or a `keptAt` that is not a timestamp; when any ledger entry lacks an id,
repeats one, has a `kind` other than `credit` or `debit`, or an `amount` that is
not a positive whole number; or when the file's ledger, replayed in time order,
goes below zero at any point. An unreadable file reads
`That file isn't readable, so nothing was changed.`, offers nothing to apply, and
changes nothing, even where the rest of the file is sound.

**The import, as the reader meets it.** `/import` carries a file field named
`Store file`. Choosing a readable file shows a region named `Import preview`
saying what will be added, what is kept and what conflicts, with an
`Apply import` button and a `Decline import` button. Declining changes nothing.
Applying merges, then reads `Merged. Undo is available until you leave.` beside
an `Undo import` button that returns the store to its state immediately before.

**The merge rules, exactly.**

- The collection is keyed by series, day and month. A character present on both
  sides keeps whichever entry has the earlier `keptAt`, whole, with that entry's
  background and colour.
- A best is the maximum within its own game. Attempts are the union ordered by
  time, and the newest twenty per game are kept.
- A day in `dailyHistory` holding different prompts on the two sides is listed
  in the preview, and the reader picks one.
- The shard ledger is keyed by entry id. When each side holds a debit the other
  lacks, both devices spent independently: the preview reads
  `Both devices spent shards. Choose which purse to keep.`, offers two radio
  choices named `This device's purse` and `The imported purse`, keeps
  `Apply import` disabled until one is chosen, and the chosen ledger is kept
  whole. Otherwise the two ledgers combine by id, each entry counted once.
- The `preferences` with the later `savedAt` win, and the preview names the
  device they came from. `seenDay` is the later of the two.

### Replay

A finished run can be replayed by storing the reader's inputs and the seed, not
the frames, and feeding the same inputs to the same simulation. That requires
each game to be a deterministic function of seed and input, which is why the
shell owns the clock. A replay that no longer matches what it recorded says so
rather than playing on. Replay is not required of every game: the oracle, the
wheel and the daily prompt have nothing to replay, and a game declares whether
it is replayable.

### The game shell

One shell owns what is common and each game supplies only its own rules.
**Interruption is the shell's business, not each game's.** A game
is a state machine over ready, running, paused and over, and every game has all
four. The shell owns the clock: elapsed time comes from a monotonic source, not
from a frame counter, so thirty seconds is thirty seconds on a fast display and
a slow one, and the displayed remainder is derived rather than accumulated by
subtraction. The last second is a whole second, and a countdown showing zero
accepts no further input.

A running game pauses when the tab is hidden, when the window loses focus, or
when the menu opens over it, and resuming returns the same state with the same
time remaining. Sound stops when the game pauses. Nothing plays before the
reader has interacted. There is one mute, it is global, it is reachable on every
route that makes sound, and its setting survives navigation and a reload. Audio
is never the only carrier of information, and no audio is fetched before an
interaction that will play it.

### The ten games, and the rules that decide them

**Puzzle.** The board is a permutation of the tiles and it is **solvable**. Half
of all random permutations of a sliding puzzle cannot be solved, and a shuffle
that produces one hands the reader an impossible board that looks exactly like a
possible one; shuffle by applying legal moves from the solved state, or test the
permutation before offering it. A move is legal only into the empty cell, and an
illegal attempt is not a move. Time runs from the first move, not from the press
of Start. Moves are undoable as a stack, so an undo returns the board and the
counter together.

The board is `4` by `4`: fifteen tiles numbered `1` to `15` and one empty cell.
It is a grid named `Puzzle board` of four rows of four cells, each cell showing
its tile's number and the empty cell showing nothing. Opening `/puzzle` deals the
day's shared board at once and reads `Everyone gets this same board today.`, and
reopening the route that day deals that board again. `Shuffle` starts the next
attempt, deals the next board of the day's per-attempt sequence, and reads
`Practice run. Today's shared board was your first go.` The grid takes keyboard
focus, and while it has focus each arrow key moves the empty cell one cell in the
arrow's direction by swapping it with the tile there; an arrow that would take
it off the board is ignored and not counted. The count reads `Movements: <n>`,
and `Undo` takes back the last move and one from the count together.

**Memory.** The board is dealt solvable and no two deals in a session are
identical. Exactly two cards may be face up at once, and a third click during the
comparison pause is refused rather than queued. A matched pair is inert. A card
is face up when the model says so, not when its transform has finished.

**Shaking.** A hit registers once: the same target struck twice before it
withdraws scores once, and a strike landing as the target withdraws counts or
does not by a stated rule. Nine holes map to a numeric keypad, and the mapping
is offered rather than left to be discovered.

**Wheel, the spinner.** The result is decided by the model and the wheel animates to it; a
wheel that reads off whatever segment lands under the pointer has made the
animation authoritative and a dropped frame changes the answer. All sixteen
segments are reachable, and the result is readable as text. `GO` spins. It is
unavailable while the wheel turns and becomes available again only once a live
status named `Wheel result` states where it landed. Landings are drawn from the
wheel's own stream of the day seed, so two readers spinning on the same day land
in the same places.

**Picks.** A category owns its own deck, switching category does not carry a
drawn card across, and deck sizes differ. Two rapid taps draw one card.

**Challenge.** The same local day yields the same prompt however many times the
route is opened, a prompt already seen today is shown again rather than
replaced, and previous days are readable. The day boundary is the reader's own
local midnight, stated in the interface. `/challenge` states
`Today is <YYYY-MM-DD>`. Pressing `challenge` shows the day's prompt in a region
named `Today's challenge`; pressing it again on that day shows the same prompt
with `Today's challenge, again. A new one arrives at midnight.` Earlier days sit
in a list named `Previous days`, each item showing its date and its prompt.

**Gotcha.** The shop was captured and **the gallery of rewards behind it was
not**, so the build designs what a tier yields and publishes it. The three tiers
are prices, not rarities: what a tier yields is a
separate question from what it costs. Odds are published where the prices are.
The route requires landscape, recovers by itself when the device is rotated
without a reload, and does not show the refusal on a desktop window that merely
happens to be tall. Fullscreen can be refused and can be exited by the browser
without asking, and the game state survives both.

**Rocket, Wiggle and Love.** The launcher's only captured end state is the word
`Lose` beside a `Restart` control, and how it is played was never established
from outside, so the build decides the mechanic and states it. That end state
reports how far, how long or how many rather than only naming the outcome: a
game with a losing state and no measure gives a reader no reason to press
`Restart`. If the input is device motion then a device without a motion sensor,
a device that refuses the permission, and a desktop with neither are all
first-class cases with an equivalent control rather than an apology. The movement prompts state what
happens when a two-digit counter reaches one hundred, and do not repeat a prompt
until the set is exhausted. The passport resolves its six fields and its verse
together, or says it is still working.

### Compound cases

These collide, and satisfying each requirement separately does not satisfy any
of them. Choose one answer per case, apply it consistently, and be able to say
what was chosen: a collection opened while storage is full; a game abandoned by
closing the tab as the timer expires; a shard spent in one tab while the other
shows the old balance; the daily prompt opened at 23:59 and again at 00:01;
stored state written by an older version read by a newer one; an import arriving
from a device that spent the same shards; the clock moved back a day after a
daily entitlement was claimed; a shared link carrying the thirtieth of February;
the menu opened while a timed game runs; the carousel dragged as the window
crosses a breakpoint; a card turned at the instant the timer expires; the prize
machine rotated to portrait mid-exchange; focus resting on a target the game
removes; and the day rolling over mid-attempt.

### Removal, and what the product has kept

The reader can see everything the product has stored about them and delete it,
wholly or by part. A product keeping a collection, a score history, a daily
record and a currency, all invisibly, has accumulated a profile whether it meant
to or not. Removal is a route of its own, it names each kind of stored state and
its size, and it confirms before it deletes.

That route is `/my-data`. It carries a list named `Stored on this device` with
one item per kind of stored state, each reading `<kind>: <entries>` under the
kind names the store file uses, where a kind held as a single value counts `1`
when set, with a `Delete <kind>` button in the item, and a `Delete everything`
button below the list. Every delete first opens an alert dialog offering
`Delete` and `Cancel`. Deleting one kind leaves every other kind exactly as it
was, and deleting everything reads
`Everything this page had kept has been deleted.`

### The record routes

The timeline carries four parts with their own sub-navigation: **Plan**, a
display case, **Executor**, and the dated roadmap.

**Plan** is five numbered phases, each a record with a number, a title and a
body, rendered from data rather than five hand-written blocks. The fifth phase
is the most concrete and names six theme areas and a free-entry rule for
children under twelve.

The display case holds twenty-four captioned items marked `Display Only`.
Several captions repeat, so a caption is a type rather than a name and each item
needs its own identity to be addressable.

**Executor** is a short first-person statement, a collaboration address, and a
five-word list joined by ideographic middle dots.

### Additions this build owes beyond the reference

The reference keeps nothing: no collection, no score between visits, no record
of a prize, no way back to a character once the field is retyped. Every
obligation about persistence in this brief is an **addition**, specified on
purpose and kept inside this product's tier. The four that carry the most weight
are the day seed, clock integrity, links and merge, and replay, and they are
deliberately interdependent: one seed per local day makes boards shared and
reproducible; a clock the reader owns makes that seed contestable; a link
carrying inputs makes a board portable; a merge makes two devices reconcilable;
and replay is possible only because the first of those made the games
deterministic. Specified separately they are five features. Specified together
they are one constraint on how every game is built, which is the point.

### The acceptance checklist

`## Definition of done` is the acceptance checklist for this build, and every
line on it is checkable by a person in front of the running product at all three
widths.

### The site surface

Every public route declares a social preview title and description, and the
preview image it names resolves. No two routes share a preview title.

The birthday finder refuses a submission that fills a field no person can see:
the finder carries a decoy parameter named `website`, no person is shown it, every
submission from the finder sends it empty, and any resolution carrying a
non-empty `website` is refused. It also refuses a caller sending the same form
repeatedly in quick succession: more than `30` resolutions carrying `website`
inside `10` seconds from one caller answers `429` until the window passes. A
resolution without `website` is the product re-deriving a character it already
holds, for the collection or a link, and is never limited. No credential, key or token appears in anything the
browser downloads, and no source map is published. `/index.html` answers a
permanent redirect to `/`, so the home document has one address. The route table
is declared once and both the navigation and the hub read from it.

### The API

| Route | Purpose |
|---|---|
| `GET /api/health` | readiness |
| `GET /api/resolve` | the resolver, shape above |
| `GET /api/series` | the sixteen series with their labels |
| `GET /api/colours` | 366 day-colour assignments plus the remainder `rule` |
| `GET /api/characters` | the whole catalogue, paginated |
| `GET /api/games` | the hub order, ten entries |
| `GET /api/awards` | the one award record |
| `GET /api/roadmap` | the dated timeline, from the same record |
| `GET /api/prompts` | the daily prompt set |
| `GET /api/wheel-categories` | sixteen categories |
| `GET /api/oracle-decks` | six decks of differing size |
| `GET /api/odds` | the published prize odds |
| `GET /api/page-views` | recorded page views |

Every one of these is a read. The application exposes no route that writes
anything belonging to a reader. In particular `/api/collection`, `/api/scores`
and `/api/shards` do not exist: a reader's kept characters, their bests and
their shard ledger live on the device, and a request to create any of them is
refused.

## Data model

Two stores, and the split is the product's central architectural fact.

### The catalogue, in `postgres`, read-only

Loaded on first start from a stated seed. Nothing a reader does writes here.

| Entity | Fields |
|---|---|
| `Series` | ordinal 1 to 16, label (`366` through `5856`), name |
| `Character` | series, day ordinal 1 to 366, number 1 to 5856, phase, part set, palette role |
| `DayColour` | day ordinal, phase (one of the five names), colour name |
| `Game` | key, title, hub position 1 to 10, route, accent role, declares sound, timer, minimum play area, orientation, replayable |
| `Award` | subject, body, kind, kind name, date, status |
| `RoadmapPhase` | number, title, body |
| `Prompt` | key, text |
| `WheelCategory` | key, label, segments |
| `OracleDeck` | key, label, cards |
| `PrizeTier` | key, price, published odds |
| `PageView` | route, at |

**Seeded content, and the tests reach all of it:**

| Object | Seed |
|---|---|
| `Series` | sixteen rows, labels `366` to `5856` in steps of `366` |
| `Character` | 5856 rows, 366 per series, `number = (series - 1) * 366 + ordinal` |
| `DayColour` | 366 rows, every ordinal 1 to 366 present, each with a phase, plus the stated remainder `rule` |
| `Game` | ten rows in hub order: Shaking, Memory, Rocket, Puzzle, Challenge, Wheel, Wiggle, Picks, Gotcha, Love |
| `Award` | four rows, one subject carrying more than one, two with status `Results Pending` |
| `RoadmapPhase` | five rows, numbered 01 to 05 |
| `WheelCategory` | sixteen rows |
| `OracleDeck` | six rows of differing size, the smallest holding two cards |
| `PrizeTier` | three rows: `COMMON` at `10`, `RARE` at `100`, `LEGENDARY` at `250`, each with odds that sum to one |

The awards scene and the timeline render from the **same** `Award` rows in one
date format. Two routes rendering one award list from two copies is how they
come to disagree about how many awards there are.

### The reader's store, on the device

Under one namespaced root with a declared version. The server never sees it.

| Kind | Shape | Merge rule |
|---|---|---|
| `collection` | entries of character, series, day, month, background, colour, kept-at | union, earlier kept-at wins |
| `bests` | per game, one best plus whether it was timed | maximum, within that game only |
| `attempts` | per game, recent attempts with time | union by time, truncated |
| `dailyHistory` | keyed by local day, the prompt issued | two records for one day is a conflict the reader resolves |
| `shardLedger` | credits and debits, each with an id, a reason and a time | never a sum of balances: combined by id, or one purse kept whole when both sides spent |
| `preferences` | mute, reduced motion, chosen background | the later save replaces the earlier one, and the reader is told which device it came from |
| `seenDay` | the latest local day observed | maximum |

A best is comparable only within its own game: thirty seconds of tapping and a
tile count are not the same quantity and are never ranked together. An attempt
is recorded when the game ends, never while it runs, so a reader who reloads
mid-play has no attempt. An untimed run is recorded as untimed rather than
ranked against timed ones.

## Front-end specification

The visual detail in full. It reaches the builder complete and nothing here is
optional.

### Per-route theming

A route declares three tokens, `ground`, `ink` and `accent`, and the chrome
inherits them. The token layer is per route, not global: a value meaningful on
one route is inert on the other fourteen, and publishing every route's tokens on
the root is how a value for a game that no longer exists survives.

| Route | Ground |
|---|---|
| `/` | a warm **mid, soft orange** |
| `/games` | a saturated warm red |
| `/love` | a blurred **mid, vivid violet** cloudscape |
| `/gotcha` | **near-black neutral** |
| the legal and awards surfaces | **near-white neutral** |

The arcade set is neon at full saturation and maximum value: **mid, vivid
teal**, **mid, vivid green**, **mid, vivid magenta**, **mid, vivid amber** and a
**mid, vivid violet**. The passport's controls sit on a **mid, soft orange**
that reads as muted gold. Two hover systems run in the chrome: a sand hover
applied identically whether the resting ink is light or dark, and a **light,
soft magenta** hover on the navigation and the carousel controls. A **mid cool
neutral** carries secondary text.

No hex value appears anywhere in this brief. The exact values are the builder's,
subject to the roles and relationships stated here.

**Three colours in the reference were chosen by nobody** and are not
reproduced: a browser's unvisited-link blue on the active carousel item, and the
untouched default primary blue and default green of two component libraries.
Every interactive element declares its own resting and hover appearance.

### Typography

| Family | Weights | Style |
|---|---|---|
| Playfair Display | 400, 600 | normal and italic |
| Comfortaa | 600 | normal |

A high-contrast display serif with a true italic, and a rounded geometric sans
at a single heavy weight. The serif is the ceremony of the passport scene; the
rounded sans is the arcade. Both are openly licensed substitutes, `woff2` only,
subset to the characters the copy uses, **and the subset includes the
Traditional Chinese** of the wheel, which is where most of the weight goes and
which cannot be dropped because one whole game is written in it.

The rendered scale, which is the scale that ships: `16px` regular for body,
`15px` at 700 and at 900, `14.4px`, `13.6px`, `13.5px`, `12px`, `22px`, `24px`
at 900 and `28px`. Declare it as a named set of steps and use it. The reference
carries `14.4px`, `13.5px`, `13.6px` and `13.3333px` within one and a half
pixels of each other, which are relative units compounding through three levels
of nesting rather than four decisions.

**The minimum rendered size is `12px`.** The reference sets a counter at `10px`
at weight 700 in sixty-nine places; the build raises it and finds the room.

One icon mechanism, not nine `@font-face` declarations across three generations
of one icon set. Icons that are decoration are inline vectors; icons that carry
meaning carry a text alternative regardless of how they are drawn, and an icon
font that fails to load must not silently remove a control's only label.

**The chromatic fringe stays and is checked.** Every navigation link carries a
teal shadow half a pixel to one side and a magenta shadow half a pixel to the
other, at low alpha: the colour fringing of a misconverged screen, applied as a
permanent state. It is a good joke and it lowers effective contrast against the
panel behind, on the one control present on all fifteen routes.

### Radius, elevation and blur

Reduce thirteen measured radii to a named scale plus a `50%` case for discs; the
background switch, the sound toggle and the party-mode control are all discs.

Elevation is three separate systems and they stay separate. **Ordinary depth**
deepens with the surface: a card, then the menu, then the legal panel. **Pressed
metal** is the passport's controls, and it is the most considered piece of
visual design in the capture: a white inset highlight along the top, a gold
inset shade along the bottom, and an outer drop, which together make a flat
rectangle read as a lit physical object. **Emission** is shadow used as light on
the lasers and on the dust particles. An emission shadow must not come from the
same token as a depth shadow, or a theme change that darkens the interface will
extinguish the lasers.

Every overlay is a frosted panel. Blended elements are additive, so a glow that
lightens needs something dark behind it: those blobs are legible only on the
dark routes and must not be placed on a light one.

### Motion

Name four curves and retire the rest. The house style is springy: the dominant
curve overshoots its target slightly and settles back, one overshoots harder,
and one undershoots below zero before overshooting. Two of the reference's
curves differ in the second control point by a tenth and appear once each;
nobody can see the difference and nobody chose it twice.

**Transitioning every property is the defect this build does not reproduce.**
The reference declares it more than five thousand times, and separately animates
width, height, top and left together, which forces layout on every frame where a
transform would not. Every transition names its properties.

The keyframe families:

| Family | Behaviour |
|---|---|
| Idle life | a breathe that scales and rides opacity, and a badge that rises three pixels while its shadow deepens; both loop forever |
| Colour cycling | four sets cycling text between a pale yellow and white at two alphas and two sizes, so adjacent elements cycle out of phase |
| Impact | a shockwave expanding a shadow to sixty pixels at zero alpha, a screen flash, and a trophy jump that is a loop disguised as a bounce |
| Disruption | a burst splitting text into teal and magenta shadows and snapping back square, a double glow, and a highlight sweeping across |
| Rotation | a coin flip through a full turn in perspective, declared twice under two names, and a rotating gradient |
| Instructional | a hand animating through a tap and through a drag |

**The instructional animations are functional, not decorative.** Where one
teaches the only gesture that operates a game, the game is also operable by a
means that needs no demonstration, and the equivalent is discoverable in the
same place the hand appears.

Under a reduced-motion request: looping idles stop at rest; the carousel changes
selection without travelling; impact and disruption resolve to their end state
without playing; particle scenes hold a static frame; scroll-driven motion
becomes a static layout; and instructional hands are replaced by their text
equivalent. **Games remain playable, not merely still**: a game whose only
feedback is a particle burst needs a second, still channel for the same
information.

### The hub carousel

Ten covers in a cover-flow ring. The neighbours are rotated sixty degrees about
the vertical axis, pushed out and pushed back; the active card comes forward and
stays square to the reader. Selection transitions run half a second on an eased
curve.

The ring is operable by keyboard: arrow keys move the selection, the selected
cover is the one that receives focus, and the focused cover is always the one
brought to the front. It is operable by swipe and by the edge controls, and all
three paths change one piece of state rather than three. Position is announced,
because a ring of ten showing three tells a reader using assistive technology
neither how many there are nor where they are. The covers behind the active one
are not reachable by pointer and are not read out as though on screen.

The hub also carries the birthday finder, and it is the **same component** as the
home route's, not a second implementation.

### Chrome

A three-bar control opens a panel of five destinations. The panel is a modal
surface: opening it moves focus into it, Escape closes it, focus returns to the
control that opened it, and the page behind is inert to pointer and keyboard
while it is open. **A destination that leaves the product says so, consistently**;
the reference marks one of its two external links and not the other.

An awards badge sits persistently and breathes. The footer carries a copyright
line whose **year is derived, never printed into the markup**, because a typed
year is wrong from the first of January until somebody notices.

The legal notice is reachable from every route and exists **once**. The
reference renders it through two separate mechanisms, which can drift, and a
legal notice saying two different things on two routes is worse than either. The
tribute paragraph is not boilerplate: a build carrying no tribute artwork must
not carry the paragraph claiming it does.

### Responsive behaviour, the queries and scroll

Four named breakpoints, declared once, used everywhere. The reference uses
eleven distinct widths, with `767`, `768` and `769` serving as one boundary in
three files. A game needing a minimum play area asks for that in its own terms
rather than guessing a device.

One route pins its scroll: the page does not move and scroll input drives a
scene in place. A pinned scene owes three things. It has a stated end so a
reader can get past it. It is not the only way to reach anything below it. And
it responds to the keyboard and to a scrollbar drag, not only to a wheel, since
a scene consuming wheel events and nothing else is unreachable without one.

An orientation refusal is a designed state: it says what to do, recovers by
itself on rotation without a reload, and does not appear on a desktop window
that merely happens to be tall.

### Accessibility

Everything doable with a pointer is doable with a keyboard, and that rule is
load-bearing here because the reference's whole interaction vocabulary is tap,
drag, swipe, spin and shake. The hub moves with arrow keys. The tapper maps its
holes to a keypad. The matcher moves a cursor and turns a card with an explicit
key, not by focus alone, so a reader tabbing through does not reveal the board.
The puzzle moves the empty cell with the arrow keys. The oracle draws and
changes category with a key. The wheel spins with a key. The pinned scene
advances with the keyboard.

Focus is always visible against the route's own ground, is managed at every
transition, and is never lost to a removed element: cards, targets and tiles are
removed during play and focus must land somewhere deliberate.

No game state is carried by colour alone. A matched pair, a correct answer, a
live target and a spent shard each need a second channel. The neon teal, green
and green-teal are all near maximum luminance and are nearly indistinguishable
under the most common colour deficiency, and all three are used as state
colours.

Live values are announced at a rate a person can use: the score when it changes,
the timer at intervals and at its end rather than sixty times a minute, the
carousel position, and the balance after an exchange.

A thirty-second limit is a barrier for some readers, so the limit is adjustable
or an untimed mode exists.

Language is declared per element where it differs from the document, so a screen
reader pronounces the wheel's Chinese as Chinese. Where a string exists in both
languages, both are marked. The wheel's sixteen categories are content, not
markup, and are translatable without touching the game.

### Performance and weight

Per route, uncached, at desktop: the character above the fold within 150,000
bytes; all images above the fold within 400,000; script within 300,000; style
within 60,000; fonts within 120,000; and **audio before first interaction at
zero bytes**. A game's own assets sit outside the route budget and are fetched
when the game is entered, not when the hub is rendered.

**No character ships as an animated GIF.** The reference serves 241 of them at
sixty megabytes, averaging a quarter of a megabyte each, in a format from 1987
with a 256-colour palette. These characters are flat-coloured line art with a
stroke, which is the case that compresses best as vector. Draw a character as a
vector composition from a small set of parts: a head shape, a hair mass, two
ringed eyes, a mouth, four limbs and a rounded torso, each a primitive with a
stroke. A character is then a record of which parts, which colours and which
pose, so 5856 characters are a table of parameters rather than 5856 files, and
the idle animation drives the parts, which is why they stay separate.

Sprite art is served as a small number of atlases rather than nine hundred
separate requests. Game feedback tones are synthesised rather than downloaded.
The blurred cloudscape is a layered gradient with a soft noise field, carrying
its day and night variants as two sets of stops rather than two photographs.

### The reference stack, and the defects not to reproduce

The reference loads **two versions of GSAP together**, each installing its own
global, and **two versions of three.js thirty-two releases apart**, one reported
by a bundle revision literal and one by the runtime global. It also still
carries **AngularJS 1.5.8**, whose line reached end of life in 2021, apparently
to bind two numeric readouts on one route. GSAP ScrollTrigger and GSAP SplitText
survive as identifiers, a WebGL shader source survives as a `glPosition`
reference, and Google Fonts is loaded from `fonts.googleapis.com`.

**One version of each library.** The 3D work is needed by two surfaces and both
can use one version. Two numeric readouts are two numbers and need no framework.
Source maps are not published; the reference publishes three, which is how its
whole stack was identified from outside.

**A stacking value of `2147483647` appears thirty-six times**, which is the
maximum signed 32-bit integer used as a stacking order. Stacking is a small
named set, and the topmost layer is named explicitly so nothing competes with it.

### The queries, as measured

Twenty-one distinct media queries were parsed across eleven distinct widths:
`360`, `430`, `480`, `500`, `600`, `650`, `767`, `768`, `769`, `1024`, `1200`,
`1699` and `1920`. Three are inconsistencies rather than decisions: `767`, `768`
and `769` serve as one boundary in different files; `max-width: 1024` and
`min-width: 1024` overlap at exactly `1024`; and `max-width: 768` appears both
with and without the `screen` keyword. One query is genuinely specific rather
than sloppy, targeting a small phone by both width and height, which is a game
asking for a minimum play area rather than a layout asking for a column count.
`prefers-reduced-motion: reduce` appears exactly once against seventy-six
keyframe sets.

### The carousel geometry, as measured

The container declares a perspective and the items preserve 3D. A cover left of
centre is rotated sixty degrees about the vertical axis, pushed `135` out and
`50` back; the cover right of centre is its mirror; the active cover comes `150`
forward and stays square. Selection transitions are CSSTransition on `transform`
for the item and on `opacity` for its image, both `500`, the transform on an
eased curve and the image on a plain ease.

### The zero-asset substitution guide

The manifest below is the asset census the guide replaces, class by class.

| Class | Count | Substitution |
|---|---|---|
| Animated characters | 241 GIF, 60MB | vector parts, drawn from a record |
| Sprite art and plates | 920 PNG, 34MB | inline vectors in the route palette, atlased |
| Cover art | ten JPEG | generated per game from its record, deterministic |
| Photographic backgrounds | day and night JPEG | layered gradient plus a soft noise field |
| Spoken phrases and game audio | 112 MP3, 31.5MB | feedback tones synthesised; spoken phrases are not |
| Icon fonts | woff2, three generations | inline vectors |
| Text typefaces | two woff2 | openly licensed equivalents, subset |
| Inline vectors | seven SVG, one `image/svg+xml` served | transcribed whole |
| Tribute artwork | unknown count | **not replaced, omitted** |

**The spoken phrases are different and are not synthesised.** A phrase in
Taiwanese spoken by a person is a recording of a language, and generating an
approximation of it is worse than omitting it: ship a small set of genuinely
licensed or self-recorded phrases, or ship the feature with the phrases the
build actually has and say how many.

**Typefaces.** Openly licensed equivalents of a high-contrast display serif with
a true italic and a rounded geometric sans at one heavy weight, `woff2` only,
subset to the characters the copy uses.

### Motion and vestibular safety

A perpetual pulse at the edge of vision is precisely what a reduced-motion
preference exists to prevent, and the reference runs a breathing scale, a
rising badge and four colour-cycling sets forever on elements present on every
route. Under the preference those stop. **Vestibular safety is the reason, and
the games stay playable rather than merely still.**

### Announcements

Live values are announced at a rate a person can use. A score changing on every
hit and a timer ticking every second are both live regions, and an announcement
sixty times a minute is worse than none: announce the timer at intervals and at
its end, the score when it changes, the carousel position, the passport when its
seven asynchronous values resolve, and the balance after an exchange.

### The spelling and spacing the reference shipped

Three defects are recorded rather than silently corrected, because this brief
describes a rebuild and not a transcription. The home copy spells `comercial`
for commercial. The display case spells `Vinil Figure` for Vinyl. And the phase
numbering uses an ideographic space between number and title on the first four
phases and an ordinary space on the fifth. The build fixes all three and states
that it did.

### Copy

These strings are requirements, not decoration. Each is the moment a reader
learns why the product behaves as it does, and replacing one with a generic
message undoes the work behind it:

`Oops! This date doesn't exist.` ·
`No characters kept yet. Find one from your birthday.` ·
`Kept. It's in your collection.` ·
`This device won't let the page save anything, so nothing will be kept after you leave.` ·
`There's no room to keep another one. Remove a few to make space.` ·
`Everything this page had kept has been deleted.` · `First run at this one.` ·
`Best yet.` · `Untimed run, kept separately from timed ones.` ·
`Chances are published below.` ·
`Turn your device sideways to play. It'll start again by itself.` ·
`You're offline. This game already loaded, so it still works.` ·
`Paused. Come back when you're ready.` ·
`Today's challenge, again. A new one arrives at midnight.` · `Previous days` ·
`Animation is turned down because you asked your device for less. Everything still works.` ·
`Everyone gets this same board today.` ·
`Practice run. Today's shared board was your first go.` ·
`Your device's date went backwards. Nothing you've earned has been touched.` ·
`The link will contain your birthday. Anyone you send it to will see it.` ·
`That link doesn't describe anything this page can show.` ·
`That link was made by an older version of this page.` ·
`Both devices spent shards. Choose which purse to keep.` ·
`Merged. Undo is available until you leave.` ·
`That file isn't readable, so nothing was changed.` ·
`Nothing to replay in this one.` ·
`This replay stopped matching the run it recorded.` ·
`EXCHANGE YOUR SOUL SHARDS` · `LANDSCAPE MODE ONLY` ·
`Your browser does not support the audio element.`

The register is warm, direct, second person, and not afraid of a joke. The
personal-use restriction on the characters is a real licence term: wherever a
character can leave the product, as a saved image, a share or an export, the
same restriction travels with it.

## Constraints

- Nothing a reader produces leaves the device. No account, no sign-in, no shared
  leaderboard, no server-held collection, no purchase of anything.
- The catalogue is read-only. The application accepts no write from a reader.
- No character ships as an animated GIF, and no source map is published.
- One version of each library. Two versions of one animation library loaded
  together is the defect this build does not reproduce.
- No tribute artwork, no reproduction of any reference character, and no award
  the build has not itself won.
- A generated character must look generated.
- `Display Only` is a disclaimer, not a heading style: nothing in it acquires
  the affordances of a shop.
- No page route nests and no page route takes a path parameter. The documents
  are flat; catalogue reads carry query parameters.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written
  to `/app/USER_README.md`. Daykin has none: every route is public.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the
  app root, empty.
- Serve a production build behind a static or preview server, never a dev
  server.
- The server must keep running after this session ends and must not be a child
  of the shell. An ordinary background job dies with its shell, and the app will
  not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

## Definition of done

Daykin is done when the app is deployed and healthy, the twenty-ninth of February
resolves to ordinal `60` with sixteen members whatever year the device believes,
and a kept character survives a reload with the background it was kept with. The
hardest guarantee is that what a reader holds stays on the device and stays true:
one daily claim per day however the clock moves, one purse across open tabs, and
an import that merges rather than replaces.
