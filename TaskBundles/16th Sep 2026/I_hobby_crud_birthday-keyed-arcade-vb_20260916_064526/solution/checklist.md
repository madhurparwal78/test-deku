# Checklist: deku/birthday-keyed-arcade-vb

Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC
Items: 114
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` A day plus a month resolve to one character in each of sixteen series `src: Overview, resolve to one character in each of sixteen series`
- [ ] `C-OV-02` `constraint` Nothing a reader produces leaves the device `src: Overview, nothing a reader does leaves their device`
- [ ] `C-OV-03` `capability` The server publishes a read-only catalogue `src: Overview, The catalogue is content the product ships and is read-only`

## C-RL User roles

- [ ] `C-RL-01` `role` A Visitor reaches every route without signing in `src: User roles, There is one role, **Visitor**, and no sign-in of any kind`
- [ ] `C-RL-02` `constraint` A pasted share link is validated on arrival `src: User roles, every field re-validated; a link carries inputs, never a result`
- [ ] `C-RL-03` `constraint` An import file is validated whole before anything is written `src: User roles, validated whole before anything is written`
- [ ] `C-RL-04` `constraint` A stored shape that does not validate is discarded `src: User roles, a shape that does not validate is discarded, and the product opens`

## C-CF Core features

- [ ] `C-CF-01` `capability` The resolver returns an ordinal within the 366-day cycle `src: Core features, resolve to an ordinal from `1` to `366``
- [ ] `C-CF-02` `constraint` No year is asked for anywhere `src: Core features, **No year is asked for and none may be required.**`
- [ ] `C-CF-03` `capability` The twenty-ninth of February carries an ordinary character `src: Core features, The twenty-ninth of February is an ordinary day with an ordinary character`
- [ ] `C-CF-04` `constraint` A pair is valid when that day exists in that month in a leap year `src: Core features, A pair is valid when that day exists in that month in a leap year`
- [ ] `C-CF-05` `constraint` The thirty-first of April is refused `src: Core features, The thirty-first of April is refused`
- [ ] `C-CF-06` `capability` A resolved character can be kept on the device `src: Core features, A resolved character can be kept on the device`
- [ ] `C-CF-07` `constraint` The same character kept twice is one entry `src: Core features, The same character kept twice is one entry`
- [ ] `C-CF-08` `capability` Ten games are reachable from a hub `src: Core features, Ten games from a hub`
- [ ] `C-CF-09` `capability` One seed per local day drives every source of chance `src: Core features, One seed per local day drives every source of chance`
- [ ] `C-CF-10` `capability` A shard balance derives from a ledger of credits plus debits `src: Core features, derived from a ledger of credits and debits`
- [ ] `C-CF-11` `constraint` A shard balance never falls below zero `src: Core features, never goes below zero`
- [ ] `C-CF-12` `capability` Published odds sit where the prices are `src: Core features, Odds are published where the prices are`
- [ ] `C-CF-13` `capability` A share link carries the inputs `src: Core features, encode into a link that carries the inputs`
- [ ] `C-CF-14` `capability` An import merges rather than replaces `src: Core features, imports back as a **merge**`
- [ ] `C-CF-15` `capability` A privacy page plus a terms page sit in every footer `src: Core features, A privacy page and a terms page reachable from every footer`

## C-UF User flow

- [ ] `C-UF-01` `ui` The chrome is a top navigation on all fifteen routes `src: User flow, The chrome is a **top navigation** present on every route`
- [ ] `C-UF-02` `ui` Keeping a character happens on a route of its own `src: User flow, each happen on **their own route**`
- [ ] `C-UF-03` `ui` A kept entry appears at once before the write confirms `src: User flow, The kept entry appears **at once**, marked as kept`
- [ ] `C-UF-04` `ui` A refused write returns the entry to unkept with its reason `src: User flow, the entry returns to unkept with the reason in place`
- [ ] `C-UF-05` `ui` Every list carries an empty state naming what to do `src: User flow, empty state naming what to do`

## C-UX UI/UX notes

- [ ] `C-UX-01` `ui` Each route declares its own ground, ink plus accent `src: UI/UX notes, A route declares its ground, ink and accent`
- [ ] `C-UX-02` `ui` The primary display face is Playfair Display `src: UI/UX notes, Type is **Playfair Display** for ceremony`
- [ ] `C-UX-03` `ui` The arcade face is Comfortaa `src: UI/UX notes, **Comfortaa** for the arcade`
- [ ] `C-UX-04` `ui` Motion is springy, overshooting slightly before settling `src: UI/UX notes, the house curve overshoots slightly and settles back`
- [ ] `C-UX-05` `ui` Every transition names the properties moved `src: UI/UX notes, every transition names the properties it moves`
- [ ] `C-UX-06` `ui` Focus is visible against the route's own ground `src: UI/UX notes, Focus is visible against that route's own ground`
- [ ] `C-UX-07` `ui` No state is carried by colour alone `src: UI/UX notes, No state is carried by colour alone`
- [ ] `C-UX-08` `constraint` Every content image carries alternative text `src: UI/UX notes, Every content image carries alternative text`
- [ ] `C-UX-09` `ui` Targets measure at least 44px both ways `src: UI/UX notes, Targets measure at least 44px both ways`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The server is built with Flask `src: Technical requirements, The server is **Flask**`
- [ ] `C-TR-02` `contract` The browser half is Vue 3 built with Vite `src: Technical requirements, the browser half is **Vue 3 built with Vite**`
- [ ] `C-TR-03` `contract` The datastore is reached at DATABASE_URL `src: Technical requirements, `DATABASE_URL` and `DB_URL``
- [ ] `C-TR-04` `capability` The resolver is published for exercise without a browser `src: Technical requirements, published at `GET /api/resolve` so it can be exercised without a browser`
- [ ] `C-TR-05` `constraint` The resolver consults no clock, locale or stored state `src: Technical requirements, no randomness, no clock, no locale, no stored state`
- [ ] `C-TR-06` `capability` A member number derives from its series plus its ordinal `src: Technical requirements, `number = (s - 1) * 366 + o``
- [ ] `C-TR-07` `constraint` The twenty-ninth of February is ordinal 60 `src: Technical requirements, The twenty-ninth of February is ordinal `60``
- [ ] `C-TR-08` `constraint` The thirty-first of December is ordinal 366 `src: Technical requirements, the thirty-first of December is `366``
- [ ] `C-TR-09` `capability` The colour rule accounts for the remainder `src: Technical requirements, the rule accounts for the remainder`
- [ ] `C-TR-10` `capability` A catalogue read accepts a page size chosen by the caller `src: Technical requirements, accepts a `page_size` the caller chooses`
- [ ] `C-TR-11` `capability` Paging uses a keyset cursor over a stable ordering `src: Technical requirements, Paging is by keyset cursor over a stable ordering`
- [ ] `C-TR-12` `capability` A paginated response carries cursor metadata `src: Technical requirements, alongside `next_cursor`, `has_more` and `total_count``
- [ ] `C-TR-13` `capability` Structured logs are written to stdout `src: Technical requirements, written to stdout`
- [ ] `C-TR-14` `capability` Every log line carries the request identifier of its request `src: Technical requirements, carries the request_id assigned to that request`
- [ ] `C-TR-15` `constraint` Two tabs share one shard balance `src: Technical requirements, **Two tabs are one reader**`
- [ ] `C-TR-16` `constraint` A clock moved backwards destroys nothing the reader earned `src: Technical requirements, must not include destroying anything the reader earned`
- [ ] `C-TR-17` `constraint` A shuffle of the sliding tiles is always solvable `src: Technical requirements, The board is a permutation of the tiles and it is **solvable**`
- [ ] `C-TR-18` `capability` An undo returns the board plus the move count together `src: Technical requirements, an undo returns the board and the counter together`
- [ ] `C-TR-19` `constraint` Exactly two cards may be face up at once `src: Technical requirements, Exactly two cards may be face up at once`
- [ ] `C-TR-20` `constraint` The wheel result is decided before the animation `src: Technical requirements, The result is decided by the model and the wheel animates to it`
- [ ] `C-TR-21` `constraint` No credential appears in anything the browser downloads `src: Technical requirements, No credential, key or token appears in anything the browser downloads`
- [ ] `C-TR-22` `constraint` The home document answers a permanent redirect from its duplicate `src: Technical requirements, `/index.html` answers a permanent redirect to `/``
- [ ] `C-TR-23` `constraint` The five phases are named Wood, Fire, Earth, Metal plus Water, in that order `src: Technical requirements, The five phases are named `Wood`, `Fire`, `Earth`, `Metal` and`
- [ ] `C-TR-24` `capability` The catalogue offers a phase ordering broken by member number `src: Technical requirements, `phase` orders members by their day's phase`
- [ ] `C-TR-25` `constraint` A catalogue read the server cannot serve as asked answers 400 with an error `src: Technical requirements, A read the catalogue cannot serve as asked answers `400``
- [ ] `C-TR-26` `constraint` A refused store is announced once in a notice left on the page `src: Technical requirements, shown once on the page and left in place until the reader leaves the page`
- [ ] `C-TR-27` `contract` The finder is a group named Birthday holding Day, Month plus a Find button `src: Technical requirements, The finder is a group named `Birthday``
- [ ] `C-TR-28` `capability` A kept character records the background plus colour in force when kept `src: Technical requirements, The choices in force when a character is kept are the ones it records`
- [ ] `C-TR-29` `contract` The collection route lists each entry with number, kept date, background plus colour `src: Technical requirements, `/collection` lists what is kept in a list named `Collection``
- [ ] `C-TR-30` `contract` The menu control plus the panel opened by the menu control are both named Menu `src: Technical requirements, The menu's three-bar control is a button named `Menu``
- [ ] `C-TR-31` `capability` A ledger with no welcome entry receives a credit of 300 when the prize machine opens `src: Technical requirements, A ledger holding no entry with the id `welcome` receives one`
- [ ] `C-TR-32` `constraint` A daily claim of 50 shards is offered once per local day `src: Technical requirements, Once per local day the machine offers `Claim daily shards``
- [ ] `C-TR-33` `constraint` Two quick presses of an exchange are one exchange `src: Technical requirements, two quick presses are one exchange`
- [ ] `C-TR-34` `constraint` An unaffordable exchange draws nothing, stating the price beside the balance `src: Technical requirements, An exchange the balance cannot afford draws nothing`
- [ ] `C-TR-35` `constraint` A spend in one open tab shows in every other open tab without a reload `src: Technical requirements, A spend in one open tab shows as the balance in every other open tab`
- [ ] `C-TR-36` `constraint` The local day is the reader's own calendar date in the reader's own timezone `src: Technical requirements, The local day is the reader's own calendar date in the reader's own timezone`
- [ ] `C-TR-37` `constraint` The daily claim is offered only for the latest local day the product has seen `src: Technical requirements, The daily shard claim is offered only for the latest local day the product has seen`
- [ ] `C-TR-38` `contract` A created character link carries exactly seven input fields `src: Technical requirements, A link the product creates carries exactly those seven fields and no other`
- [ ] `C-TR-39` `constraint` A field in a link beyond the inputs never reaches the screen `src: Technical requirements, Any other field is ignored`
- [ ] `C-TR-40` `constraint` An older or failing link is refused with a reason `src: Technical requirements, A link whose `v` is `1` reads`
- [ ] `C-TR-41` `constraint` The birthday warning appears before the link exists `src: Technical requirements, Only pressing that button produces the link`
- [ ] `C-TR-42` `contract` The store file declares format daykin-store at version 2 `src: Technical requirements, `/import` offers `Export store`, which saves one JSON file`
- [ ] `C-TR-43` `constraint` A store file failing anywhere is unreadable, changing nothing `src: Technical requirements, changes nothing, even where the rest of the file is sound`
- [ ] `C-TR-44` `capability` An import is previewed, can be declined, applied, then undone `src: Technical requirements, Choosing a readable file shows a region named `Import preview``
- [ ] `C-TR-45` `constraint` A character on both sides keeps the entry with the earlier keeping time `src: Technical requirements, keeps whichever entry has the earlier `keptAt`, whole`
- [ ] `C-TR-46` `constraint` When both devices spent, the reader keeps one purse whole `src: Technical requirements, the chosen ledger is kept whole`
- [ ] `C-TR-47` `constraint` Ledgers without a two-sided spend combine by id, counting each entry once `src: Technical requirements, Otherwise the two ledgers combine by id, each entry counted once`
- [ ] `C-TR-48` `capability` Removal lists each kind of stored state with a size on a route of its own `src: Technical requirements, That route is `/my-data``
- [ ] `C-TR-49` `constraint` Deleting one kind of stored state leaves every other kind unchanged `src: Technical requirements, Deleting one kind leaves every other kind exactly as it was`
- [ ] `C-TR-50` `contract` The puzzle board is a four by four grid named Puzzle board `src: Technical requirements, It is a grid named `Puzzle board``
- [ ] `C-TR-51` `capability` An arrow key moves the empty cell, an arrow off the board counting as no move `src: Technical requirements, an arrow that would take it off the board is ignored and not counted`
- [ ] `C-TR-52` `capability` Opening the puzzle deals the day's shared board at once `src: Technical requirements, Opening `/puzzle` deals the day's shared board at once`
- [ ] `C-TR-53` `constraint` Wheel landings come from the wheel's own stream of the day seed `src: Technical requirements, Landings are drawn from the wheel's own stream of the day seed`
- [ ] `C-TR-54` `capability` The challenge route states the day, listing previous days with their prompts `src: Technical requirements, Earlier days sit in a list named `Previous days``
- [ ] `C-TR-55` `constraint` Only finder submissions carrying website count toward the flood limit `src: Technical requirements, A resolution without `website` is the product re-deriving a character`

## C-DM Data model

- [ ] `C-DM-01` `data` Sixteen series carry labels from 366 through 5856 `src: Data model, sixteen rows, labels `366` to `5856``
- [ ] `C-DM-02` `data` The catalogue holds 5856 characters `src: Data model, 5856 rows, 366 per series`
- [ ] `C-DM-03` `data` Every ordinal from one to 366 carries a phase `src: Data model, every ordinal 1 to 366 present, each with a phase`
- [ ] `C-DM-04` `data` Ten games are seeded in hub order `src: Data model, ten rows in hub order`
- [ ] `C-DM-05` `data` Sixteen wheel categories are seeded `src: Data model, sixteen rows`
- [ ] `C-DM-06` `data` Six oracle decks of differing size are seeded `src: Data model, six rows of differing size`
- [ ] `C-DM-07` `data` Three prize tiers carry prices plus odds `src: Data model, three rows: `COMMON` at `10``
- [ ] `C-DM-08` `constraint` The awards scene plus the timeline read the same record `src: Data model, render from the **same** `Award` rows in one date format`
- [ ] `C-DM-09` `data` The reader's store sits under one namespaced root `src: Data model, Under one namespaced root with a declared version`
- [ ] `C-DM-10` `constraint` The shard ledger merges by neither union nor sum `src: Data model, **The shard ledger is none of these.**`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The arcade palette is neon at full saturation `src: Front-end specification, The arcade set is neon at full saturation`
- [ ] `C-FE-02` `ui` Elevation keeps depth, pressed metal plus emission separate `src: Front-end specification, three separate systems and they stay separate`
- [ ] `C-FE-03` `ui` The reference stack defect of two library versions is not reproduced `src: Front-end specification, **One version of each library.**`
- [ ] `C-FE-04` `ui` Looping idle animations stop under a reduced-motion request `src: Front-end specification, looping idles stop at rest`
- [ ] `C-FE-05` `ui` No character ships as an animated GIF `src: Front-end specification, **No character ships as an animated GIF.**`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No account exists anywhere in the product `src: Constraints, No account, no sign-in, no shared leaderboard`
- [ ] `C-CN-02` `constraint` No source map is published `src: Constraints, no source map is published`
- [ ] `C-CN-03` `constraint` No page route nests, no page route takes a path parameter `src: Constraints, No page route nests and no page route takes a path parameter`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app answers at the public URL on the mapped port `src: Deployment contract, `${APP_PUBLIC_PORT}:4173``
- [ ] `C-DC-02` `contract` The API is served on the same origin under the api prefix `src: Deployment contract, served on that same origin under the `/api` prefix`
- [ ] `C-DC-03` `contract` A readiness route returns 200 once the app is ready `src: Deployment contract, `GET /api/health` returns `200``
- [ ] `C-DC-04` `contract` The server outlives the session that started the server `src: Deployment contract, must keep running after this session ends`
- [ ] `C-DC-05` `contract` The listener binds all interfaces `src: Deployment contract, Bind `0.0.0.0``

## Pinned literals

- `366` the length of the cycle
- `5856` the size of the whole collection
- `60` the ordinal of the twenty-ninth of February
- `4173` the container-internal port
- `COMMON` `RARE` `LEGENDARY` the three prize tiers
- `Oops! This date doesn't exist.` the refusal copy

### Referenced but not pinned

- the exact colour values, carried by family plus tone plus shade
- the default page size

## Coverage ledger

- sections carried: 10
- obligations recorded: 114
