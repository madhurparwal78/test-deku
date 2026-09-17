# Checklist: deku/constellation-drawing-canvas-vb

Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC
Items: 118
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` A stargazer draws figures onto a full-screen star map `src: Overview, a single-screen night sky that a stargazer draws on`
- [ ] `C-OV-02` `constraint` A published sky stays frozen once published `src: Overview, a published sky is a frozen artifact rather than a live view`
- [ ] `C-OV-03` `constraint` Each stargazer sees only a collection of their own `src: Overview, Each stargazer sees only their own collection`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-in stargazer creates skies of their own `src: User roles, create, rename and delete their own skies`
- [ ] `C-RL-02` `constraint` A stargazer is refused any sky owned by another stargazer `src: User roles, Cannot read, render, modify, publish or delete any sky owned by another stargazer`
- [ ] `C-RL-03` `constraint` A stargazer is refused another stargazer's rendered image `src: User roles, Cannot read another stargazer's rendered image`
- [ ] `C-RL-04` `constraint` A visitor who is not signed in reads only a published link `src: User roles, Open a published link and read the frozen sky behind`
- [ ] `C-RL-05` `constraint` A refusal at the server leaves the protected state unchanged `src: User roles, leaving the protected state unchanged`
- [ ] `C-RL-06` `constraint` Signup is closed `src: User roles, Signup is closed`
- [ ] `C-RL-07` `literal` The seeded stargazer signs in as `stargazer@example.com` `src: User roles, stargazer@example.com`
- [ ] `C-RL-08` `literal` The second seeded stargazer signs in as `stargazer2@example.com` `src: User roles, stargazer2@example.com`

## C-CF Core features

- [ ] `C-CF-01` `capability` A stargazer signs in with an email address plus a password `src: Core features, signs in with email and password`
- [ ] `C-CF-02` `capability` A bearer token issued at sign-in authorises later requests `src: Core features, receives a bearer token`
- [ ] `C-CF-03` `constraint` A request carrying no token is refused `src: Core features, A request carrying no token`
- [ ] `C-CF-04` `constraint` A password is stored hashed `src: Core features, Passwords are stored hashed`
- [ ] `C-CF-05` `literal` The catalogue holds `10000` stars `src: Core features, The catalogue holds exactly`
- [ ] `C-CF-06` `data` A smaller apparent magnitude marks a brighter star `src: Core features, a smaller magnitude is a brighter star`
- [ ] `C-CF-07` `data` Star tint follows the colour index `src: Core features, Star tint follows a colour-index formula`
- [ ] `C-CF-08` `constraint` Reading the catalogue is refused to a visitor `src: Core features, It is not open to a Visitor`
- [ ] `C-CF-09` `capability` Resolution considers every star inside the angular radius `src: Core features, considers every catalogue star whose great-circle angular separation`
- [ ] `C-CF-10` `data` The brightest candidate inside the radius wins resolution `src: Core features, the star that wins is the brightest`
- [ ] `C-CF-11` `data` A tie on magnitude resolves to the lower catalogue id `src: Core features, the one with the lower catalogue id wins`
- [ ] `C-CF-12` `data` An empty radius resolves to no star `src: Core features, no star is resolved`
- [ ] `C-CF-13` `data` A segment stores two catalogue star ids rather than a screen position `src: Core features, A segment stores the two catalogue star ids`
- [ ] `C-CF-14` `constraint` A segment naming an unknown star id is refused as invalid `src: Core features, is not a catalogue id is refused as invalid`
- [ ] `C-CF-15` `constraint` A segment joining a star to itself is refused as invalid `src: Core features, joining a star to itself is refused`
- [ ] `C-CF-16` `capability` Undo removes the most recently added segment `src: Core features, Undo removes the most recently added segment`
- [ ] `C-CF-17` `constraint` Undo on an empty sky is refused as invalid `src: Core features, Undo on a sky with no segments is refused`
- [ ] `C-CF-18` `data` Segments are returned in the order the segments were added `src: Core features, The order they were added in is the order`
- [ ] `C-CF-19` `constraint` An empty sky name is refused with the offending field named `src: Core features, refused inline with the`
- [ ] `C-CF-20` `constraint` A sky name longer than `80` characters is refused `src: Core features, A name longer than`
- [ ] `C-CF-21` `data` A collection lists the owner's skies newest first `src: Core features, lists that Stargazer's skies newest first`
- [ ] `C-CF-22` `ui` An empty collection states an empty state `src: Core features, sees a stated empty state`
- [ ] `C-CF-23` `capability` Publishing stores a frozen copy of the sky `src: Core features, stores a frozen copy`
- [ ] `C-CF-24` `data` A server-minted share token addresses the frozen copy `src: Core features, Both tokens are minted by the server`
- [ ] `C-CF-25` `constraint` A caller-supplied token in the publish body is ignored `src: Core features, sent in the publish request body is ignored entirely`
- [ ] `C-CF-26` `data` A stored frozen copy is never edited afterwards `src: Core features, a frozen copy is never edited`
- [ ] `C-CF-27` `data` Republishing mints a new share token `src: Core features, Publishing the same sky again mints a`
- [ ] `C-CF-28` `constraint` A publish carrying a filled decoy field is refused `src: Core features, filled in is refused`
- [ ] `C-CF-29` `capability` A visitor opens a published link without signing in `src: Core features, Anybody may open a published link without signing in`
- [ ] `C-CF-30` `capability` A render is stored as an object in the bucket `src: Core features, stored as an object in the MinIO bucket`
- [ ] `C-CF-31` `data` A render revision starts at `1` then increases by one `src: Core features, starts at`
- [ ] `C-CF-32` `data` A later render leaves every earlier render in place `src: Core features, never replaces or removes an earlier one`
- [ ] `C-CF-33` `data` A rendered image carries one line element per segment `src: Core features, carries one line element per segment`
- [ ] `C-CF-34` `constraint` Render bytes on the app filesystem do not stand in for the object `src: Core features, may not keep the bytes on its own filesystem`
- [ ] `C-CF-35` `ui` The sky fills the viewport without scrolling `src: Core features, fills the viewport, never scrolls`
- [ ] `C-CF-36` `literal` The opening readout reads `RA 06h 00m 00s   Dec -00° 00'` `src: Core features, At first load it reads exactly`
- [ ] `C-CF-37` `literal` The opening hint reads `Select two stars to connect them` `src: Core features, A one-line hint sits bottom centre`
- [ ] `C-CF-38` `ui` Every content image carries alternative text `src: Core features, carries alternative text`
- [ ] `C-CF-39` `capability` Every internal link resolves to a real route `src: Core features, Every internal link on every route resolves`
- [ ] `C-CF-40` `constraint` Signing out refuses that session's token from then on `src: Core features, Signing out ends that session`
- [ ] `C-CF-41` `constraint` Another session of the same stargazer survives a sign out `src: Core features, any other session of the same Stargazer keeps working`
- [ ] `C-CF-42` `data` Simultaneous segments each take a position of their own `src: Core features, Segments sent to one sky at the same instant`
- [ ] `C-CF-43` `data` Simultaneous undos each remove a segment of their own `src: Core features, Undos arriving at the same instant`
- [ ] `C-CF-44` `data` Simultaneous renders each take a revision of their own `src: Core features, Renders of one sky requested at the same instant`

## C-UF User flow

- [ ] `C-UF-01` `contract` A sign-in screen answers at `/login` `src: User flow, Sign in`
- [ ] `C-UF-02` `contract` The canvas answers at `/` for a signed-in stargazer `src: User flow, The sky canvas with the collection beside`
- [ ] `C-UF-03` `contract` One sky opens at `/skies/:sky_id` for the owner only `src: User flow, One sky open on the canvas`
- [ ] `C-UF-04` `contract` A published sky answers at `/c/:share_token` for anyone `src: User flow, A published sky, frozen`
- [ ] `C-UF-05` `constraint` A visitor asking for a protected route is sent to sign in `src: User flow, is sent to`
- [ ] `C-UF-06` `constraint` A stargazer asking for another owner's sky is refused `src: User flow, for a sky they do not own is denied`
- [ ] `C-UF-07` `ui` A created sky is confirmed with a toast `src: User flow, a toast reports the sky was created`
- [ ] `C-UF-08` `ui` Every refusal states what was wrong `src: User flow, Every refusal states what was wrong`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The product commits to a dark presentation `src: UI/UX notes, The product is`
- [ ] `C-UX-02` `ui` The drawing palette offers eight distinguishable line colours `src: UI/UX notes, The drawing palette is eight fixed line colours`
- [ ] `C-UX-03` `ui` Body text meets the WCAG AA contrast bar against a background `src: UI/UX notes, meet WCAG AA contrast`
- [ ] `C-UX-04` `ui` The interface sets type in the `Roboto` family `src: UI/UX notes, One family does the whole interface`
- [ ] `C-UX-05` `ui` A collection panel sits beside the canvas as a split detail pane `src: UI/UX notes, collection list sits alongside the canvas`
- [ ] `C-UX-06` `ui` Meaning never rests on colour alone `src: UI/UX notes, Colour is never the only signal`
- [ ] `C-UX-07` `ui` Nothing overflows sideways at any width `src: UI/UX notes, Nothing overflows sideways at any width`
- [ ] `C-UX-08` `ui` An arriving panel settles into place rather than snapping `src: UI/UX notes, things arriving settle with a decisive ease-out`
- [ ] `C-UX-09` `ui` A keyboard focus ring stays visible on every control `src: UI/UX notes, keyboard with a visible focus ring`
- [ ] `C-UX-10` `ui` The chrome holds at every width between the named tiers `src: UI/UX notes, The surface fills the viewport at every width`
- [ ] `C-UX-11` `ui` The colour currently drawn with is readable from the toolbar `src: UI/UX notes, an active-colour dot filled with the current palette colour`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The coordinate readout writes the declination sign always `src: Front-end specification, a sign that is always written`
- [ ] `C-FE-02` `data` Right ascension in hours is the centre degrees divided by fifteen `src: Front-end specification, divided by fifteen`
- [ ] `C-FE-03` `ui` A segment draws as a thin glowing line in the palette colour `src: Front-end specification, a thin line in the sky's palette colour`
- [ ] `C-FE-04` `ui` A completed connection carries a visible confirmation beyond sound `src: Front-end specification, plays one soft sampled piano note`
- [ ] `C-FE-05` `literal` A clear confirmation reads `Clear all constellations?` `src: Front-end specification, The clear confirmation reads`
- [ ] `C-FE-06` `literal` A share sheet is titled `Share your Constellation` `src: Front-end specification, titled`
- [ ] `C-FE-07` `ui` A segment carries a faint outer glow of its own colour `src: Front-end specification, with a faint outer glow of the same colour`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Persistent state lives in PostgreSQL behind `DATABASE_URL` `src: Technical requirements, reached through`
- [ ] `C-TR-02` `contract` Rendered images live in MinIO behind `STORAGE_BUCKET` `src: Technical requirements, Rendered images live in`
- [ ] `C-TR-03` `contract` A paged read sets page length from `limit` `src: Technical requirements, Every paged read takes`
- [ ] `C-TR-04` `contract` A paged read walks pages by an opaque cursor `src: Technical requirements, Every paged read also takes an`
- [ ] `C-TR-05` `data` A page response reports the matching row count in `total_count` `src: Technical requirements, is the number of rows matching`
- [ ] `C-TR-06` `data` A last page reports `has_more` as false `src: Technical requirements, is true only when a further page genuinely exists`
- [ ] `C-TR-07` `data` A walk of the pages yields every matching row exactly once `src: Technical requirements, must yield every matching row exactly once`
- [ ] `C-TR-08` `data` Filtering by `max_magnitude` selects before the page is taken `src: Technical requirements, The filter selects across the whole catalogue`
- [ ] `C-TR-09` `data` Simultaneous publishes on one share key create exactly one record `src: Technical requirements, exactly one of them creates a published sky`
- [ ] `C-TR-10` `data` The losing simultaneous publish receives a conflict response `src: Technical requirements, rejected with a`
- [ ] `C-TR-11` `data` A replayed publish returns the first share token `src: Technical requirements, returns the`
- [ ] `C-TR-12` `data` A render revision leaves earlier revisions byte-for-byte unchanged `src: Technical requirements, leaves every render from`

## C-DM Data model

- [ ] `C-DM-01` `data` A star row derives from the stated whole-number rule `src: Data model, The catalogue is generated, not supplied as a file`
- [ ] `C-DM-02` `literal` Star `HD00800` carries magnitude `-1.50` `src: Data model, HD00800`
- [ ] `C-DM-03` `literal` Stars at magnitude `2.00` or brighter number `4412` `src: Data model, Counts that follow from the rule`
- [ ] `C-DM-04` `data` A sky belongs to one stargazer for the whole life of the sky `src: Data model, A sky belongs to exactly one Stargazer`
- [ ] `C-DM-05` `data` A segment position is unique inside one sky `src: Data model, is unique within a sky`
- [ ] `C-DM-06` `data` A published row is written once, never updated `src: Data model, A row here is written once and never updated`
- [ ] `C-DM-07` `literal` Every seeded account uses the password `deku-demo-pw-2026` `src: Data model, Every seeded account uses the password`
- [ ] `C-DM-08` `literal` The seeded published sky answers at share token `lantern-7f3a91` `src: Data model, is seeded already published`
- [ ] `C-DM-09` `data` Seeding a second time duplicates no row `src: Data model, Seeding must be idempotent`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No route discovers another stargazer's work `src: Constraints, No public gallery`
- [ ] `C-CN-02` `constraint` The product sends no message of any kind `src: Constraints, no email of any kind`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app answers at the public URL on the mapped port `src: Deployment contract, The port mapping is`
- [ ] `C-DC-02` `contract` The API is served on the same origin under the api prefix `src: Deployment contract, served on that same origin under the`
- [ ] `C-DC-03` `contract` A readiness route returns `200` once the app is ready `src: Deployment contract, returns`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual step `src: Deployment contract, starts from the environment image`
- [ ] `C-DC-05` `contract` A denied call answers as a client error rather than a server fault `src: Deployment contract, never as a`
- [ ] `C-DC-06` `contract` A successful catalogue read returns the star fields the contract names `src: Deployment contract, A successful call returns the named resource`
- [ ] `C-DC-07` `contract` The server outlives the session that started the server `src: Deployment contract, must keep running after this session ends`
- [ ] `C-DC-08` `contract` The listener binds all interfaces `src: Deployment contract, Bind`
- [ ] `C-DC-09` `contract` The named backing services are used as-is `src: Deployment contract, are already running and reachable`
- [ ] `C-DC-10` `contract` A list endpoint returns rows under `items` `src: Deployment contract, List endpoints return their rows under`
- [ ] `C-DC-11` `contract` An invalid call is refused as a client error `src: Deployment contract, rejected as a client error`
- [ ] `C-DC-12` `contract` Bearer authorisation guards every route except the three named `src: Deployment contract, Bearer auth is required on everything except`
- [ ] `C-DC-13` `contract` The bucket object is the render, never an app-side stand-in `src: Deployment contract, MinIO is the fact`
- [ ] `C-DC-14` `contract` Signing out answers at `POST /api/auth/logout` `src: Deployment contract, POST /api/auth/logout`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `stargazer@example.com` | the seeded stargazer | `C-RL-07` |
| `stargazer2@example.com` | the second seeded stargazer | `C-RL-08` |
| `deku-demo-pw-2026` | the seeded password | `C-DM-07` |
| `10000` | the catalogue row count | `C-CF-05` |
| `RA 06h 00m 00s   Dec -00° 00'` | the opening coordinate readout | `C-CF-36` |
| `Select two stars to connect them` | the opening hint | `C-CF-37` |
| `Clear all constellations?` | the clear confirmation prompt | `C-FE-05` |
| `Share your Constellation` | the share sheet title | `C-FE-06` |
| `80` | the longest legal sky name | `C-CF-20` |
| `1` | the first render revision | `C-CF-31` |
| `HD00800` | the worked catalogue row | `C-DM-02` |
| `-1.50` | the brightest seeded magnitude | `C-DM-02` |
| `2.00` | the worked brightness filter bound | `C-DM-03` |
| `4412` | the count of stars at that bound | `C-DM-03` |
| `lantern-7f3a91` | the seeded share token | `C-DM-08` |
| `200` | the readiness response | `C-DC-03` |
| `items` | the list envelope key | `C-DC-10` |
| `limit` | the page-length parameter | `C-TR-03` |
| `total_count` | the matching row count key | `C-TR-05` |
| `has_more` | the further-page key | `C-TR-06` |
| `max_magnitude` | the brightness filter parameter | `C-TR-08` |
| `DATABASE_URL` | the database address | `C-TR-03` |
| `STORAGE_BUCKET` | the object bucket | `C-TR-04` |
| `Roboto` | the interface family | `C-UX-04` |
| `/login` | the sign-in route | `C-UF-01` |
| `/` | the canvas route | `C-UF-02` |
| `/skies/:sky_id` | the single sky route | `C-UF-03` |
| `/c/:share_token` | the published sky route | `C-UF-04` |

### Referenced but not pinned

| Value | Item |
|---|---|
| the exact colour values, carried by family plus tone plus shade | `C-UX-02` |
| the exact corner radii, carried by relative softness | `C-UX-01` |
| the exact motion durations, carried by character | `C-FE-03` |

## Coverage ledger

| Section | Obligation sentences | Items |
|---|---|---|
| Overview | 1 | 3 |
| User roles | 1 | 8 |
| Core features | 8 | 44 |
| User flow | 6 | 8 |
| UI/UX notes | 4 | 11 |
| Front-end specification | 4 | 7 |
| Technical requirements | 8 | 12 |
| Data model | 5 | 9 |
| Constraints | 1 | 2 |
| Deployment contract | 13 | 14 |
