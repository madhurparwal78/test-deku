# Checklist: Marketscope
Items: 172
Unpinned values flagged: 6
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-1` `capability` The product is a public storefront for a multi-market charting platform `src: Overview p1`
- [ ] `C-OV-2` `capability` The storefront also carries the community publishing surface `src: Overview p1`
- [ ] `C-OV-3` `capability` A draft idea stays closed until the owning author publishes `src: Overview p4`
- [ ] `C-OV-4` `constraint` Publishing is the single act that opens the idea row, the idea page, the snapshot object `src: Overview p4`

## C-RL User roles

- [ ] `C-RL-1` `role` A signed-out visitor reads any published idea `src: User roles table`
- [ ] `C-RL-2` `role` A signed-out visitor cannot boost `src: User roles table`
- [ ] `C-RL-3` `role` A signed-out visitor cannot reach the studio `src: User roles table`
- [ ] `C-RL-4` `role` A reader boosts a published idea once `src: User roles table`
- [ ] `C-RL-5` `role` A reader cannot compose an idea `src: User roles table`
- [ ] `C-RL-6` `role` An author composes ideas in the studio `src: User roles table`
- [ ] `C-RL-7` `role` An author cannot publish an idea owned by another account `src: User roles table`

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
- [ ] `C-CF-14` `constraint` An invalid form submission writes nothing to the database `src: Core features rule 2`
- [ ] `C-CF-15` `capability` The home route carries a streaming market summary block `src: Core features live market summary`
- [ ] `C-CF-16` `capability` A ticker card updates in place as ticks arrive `src: Core features rule 3`
- [ ] `C-CF-17` `ui` A tick never re-lays out the neighbouring cards `src: Core features rule 3`
- [ ] `C-CF-18` `constraint` Rising values render in the rising signal colour `src: Core features rule 3`
- [ ] `C-CF-19` `constraint` Falling values render in the falling signal colour `src: Core features rule 3`
- [ ] `C-CF-20` `contract` The market summary endpoint returns a top-level JSON array `src: Core features rule 4`
- [ ] `C-CF-21` `data` Each market summary entry carries a direction of up or down `src: Core features rule 4`
- [ ] `C-CF-22` `data` Each market summary entry carries a session of open, closed, holiday `src: Core features rule 4`
- [ ] `C-CF-23` `data` Each market summary entry carries an authoritative server timestamp `src: Core features rule 4`
- [ ] `C-CF-24` `ui` The primary chart preview pans its visible window as ticks arrive `src: Core features rule 5`
- [ ] `C-CF-25` `capability` An author creates an idea as a draft from the compose dialog `src: Core features rule 6`
- [ ] `C-CF-26` `literal` A snapshot object is written under the key scheme `ideas/{idea_id}/{sha256_of_bytes}.{ext}` `src: Core features rule 6`
- [ ] `C-CF-27` `constraint` The idea row stores the object key rather than the image bytes `src: Core features rule 6`
- [ ] `C-CF-28` `constraint` Attaching a snapshot to another account's idea is denied `src: Core features rule 6`
- [ ] `C-CF-29` `constraint` A denied snapshot attach writes no object `src: Core features rule 6`
- [ ] `C-CF-30` `capability` Publishing moves the idea to the published status `src: Core features rule 7`
- [ ] `C-CF-31` `constraint` Publishing an idea with no snapshot is rejected as invalid `src: Core features rule 7`
- [ ] `C-CF-32` `constraint` Publishing another account's idea is denied `src: Core features rule 7`
- [ ] `C-CF-33` `constraint` A draft idea answers only the owning author's session `src: Core features rule 8`
- [ ] `C-CF-34` `constraint` A draft snapshot returns no bytes to an anonymous request `src: Core features rule 8`
- [ ] `C-CF-35` `constraint` A draft never appears in the published ideas listing `src: Core features rule 8`
- [ ] `C-CF-36` `constraint` A published idea answers any requester `src: Core features rule 8`
- [ ] `C-CF-37` `constraint` A repeated publish leaves exactly one published idea `src: Core features rule 9`
- [ ] `C-CF-38` `constraint` A repeated publish leaves the stored object key unchanged `src: Core features rule 9`
- [ ] `C-CF-39` `constraint` Two simultaneous publishes of one draft accept exactly one `src: Core features rule 9`
- [ ] `C-CF-40` `contract` The ideas listing returns published ideas newest first `src: Core features rule 10`
- [ ] `C-CF-41` `capability` A signed-in account raises an idea's boost count by one `src: Core features rule 11`
- [ ] `C-CF-42` `constraint` A repeated boost from one account leaves the count unmoved `src: Core features rule 11`
- [ ] `C-CF-43` `constraint` An anonymous boost is denied `src: Core features rule 11`
- [ ] `C-CF-44` `capability` The futures route carries the partner real-time futures landing `src: Core features rule 12`
- [ ] `C-CF-45` `literal` The futures price reads `591 INR per month` `src: Core features rule 12`
- [ ] `C-CF-46` `literal` The futures price is held in minor units as `59100` `src: Core features rule 12`
- [ ] `C-CF-47` `capability` The asset-class matrix carries nine named tabs `src: Core features rule 13`
- [ ] `C-CF-48` `ui` Selecting an asset-class tab swaps the card without navigating away `src: Core features rule 13`
- [ ] `C-CF-49` `capability` The closing data-access band repeats the subscribe action `src: Core features rule 14`
- [ ] `C-CF-50` `capability` The platform route states six product capabilities `src: Core features rule 15`
- [ ] `C-CF-51` `constraint` No marketing route hard-codes a value that should be live `src: Core features rule 15`
- [ ] `C-CF-52` `capability` A first-time visitor is asked once about non-essential cookies `src: Core features rule 16`
- [ ] `C-CF-53` `constraint` A recorded cookie answer survives a reload `src: Core features rule 16`
- [ ] `C-CF-54` `ui` Refusing cookies is as easy to press as accepting `src: Core features rule 16`
- [ ] `C-CF-55` `capability` An unknown address renders the product's own not-found page `src: Core features rule 17`
- [ ] `C-CF-56` `contract` An unknown address answers not found `src: Core features rule 17`
- [ ] `C-CF-57` `ui` The not-found page offers a round button back to the home route `src: Core features rule 17`
- [ ] `C-CF-58` `constraint` The cookie band stays away on every later route once answered `src: Core features rule 16`

## C-UF User flow

- [ ] `C-UF-1` `contract` The home route serves the hero, the market summary, the ideas river `src: User flow route table`
- [ ] `C-UF-2` `contract` The markets route lists every tracked symbol by asset class `src: User flow route table`
- [ ] `C-UF-3` `contract` The studio route is reachable only by an author account `src: User flow route table`
- [ ] `C-UF-4` `contract` A publish lands the author on a confirmation route `src: User flow route table`
- [ ] `C-UF-5` `capability` A signed-out request for the studio lands on the sign-in route `src: User flow entry and redirects`
- [ ] `C-UF-6` `capability` A successful sign in returns to the route that was asked for `src: User flow entry and redirects`
- [ ] `C-UF-7` `capability` Signing out returns the visitor to the home route `src: User flow entry and redirects`
- [ ] `C-UF-8` `constraint` A reader who reaches the studio is refused with a message `src: User flow entry and redirects`
- [ ] `C-UF-9` `constraint` A signed-out request for a draft idea page renders the not-found chrome `src: User flow entry and redirects`
- [ ] `C-UF-10` `ui` Every list has an empty state naming what would appear there `src: User flow states`
- [ ] `C-UF-11` `capability` The hero paints before the market feed has connected `src: User flow states`
- [ ] `C-UF-12` `constraint` An error renders inside the page chrome rather than a blank screen `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-1` `ui` The marketing routes are painted on a near-black neutral ground `src: UI/UX notes two-faced`
- [ ] `C-UX-2` `ui` The data surfaces invert to near-white neutral cards `src: UI/UX notes two-faced`
- [ ] `C-UX-3` `ui` One vivid blue carries every primary action `src: UI/UX notes colour by role`
- [ ] `C-UX-4` `ui` The brand blue appears on nothing other than a primary action `src: UI/UX notes colour by role`
- [ ] `C-UX-5` `ui` A falling price wears the vivid red signal colour `src: UI/UX notes colour by role`
- [ ] `C-UX-6` `ui` A rising price wears the soft teal signal colour `src: UI/UX notes colour by role`
- [ ] `C-UX-7` `ui` Accent gradient stops appear only inside gradients `src: UI/UX notes colour by role`
- [ ] `C-UX-8` `ui` Type is one geometric grotesque in two weights `src: UI/UX notes typography`
- [ ] `C-UX-9` `ui` Figures align in a column wherever prices stack `src: UI/UX notes typography`
- [ ] `C-UX-10` `ui` Every reveal shares one motion character `src: UI/UX notes motion`
- [ ] `C-UX-11` `ui` A reduced-motion preference stills every looping animation `src: UI/UX notes motion`
- [ ] `C-UX-12` `ui` A skip-to-content control is the first focusable element `src: UI/UX notes accessibility`
- [ ] `C-UX-13` `ui` Every content image carries alternative text `src: UI/UX notes accessibility`
- [ ] `C-UX-14` `ui` At a narrow viewport nothing overflows sideways `src: UI/UX notes responsive`
- [ ] `C-UX-15` `ui` Each route leads with exactly one primary action `src: UI/UX notes one primary action`
- [ ] `C-UX-16` `ui` At a narrow viewport every navigation target stays reachable `src: UI/UX notes responsive`
- [ ] `C-UX-17` `ui` Escape closes the compose dialog `src: UI/UX notes component states`
- [ ] `C-UX-18` `ui` An unavailable control is never signalled by colour alone `src: UI/UX notes component states`
- [ ] `C-UX-19` `ui` The product commits to dark, with the light data surfaces reading as inversions inside one mode `src: UI/UX notes mode`

## C-TR Technical requirements

- [ ] `C-TR-1` `contract` The frontend is server-rendered with hydrating islands `src: Technical requirements p1`
- [ ] `C-TR-2` `contract` The HTTP API is served under the same origin `src: Technical requirements p1`
- [ ] `C-TR-3` `literal` The datastore is reached through `DATABASE_URL` `src: Technical requirements p1`
- [ ] `C-TR-4` `literal` The object store is reached through `STORAGE_ENDPOINT` `src: Technical requirements p1`
- [ ] `C-TR-5` `literal` The bucket name is read from `STORAGE_BUCKET` `src: Technical requirements p1`
- [ ] `C-TR-6` `contract` The health endpoint answers once the app is ready `src: Technical requirements p1`
- [ ] `C-TR-7` `constraint` No host, port, credential is hardcoded in the app `src: Technical requirements p2`
- [ ] `C-TR-8` `constraint` No second datastore is introduced beyond the two named services `src: Technical requirements p3`
- [ ] `C-TR-9` `constraint` Market updates reach the browser without a page reload `src: Technical requirements content and market data`
- [ ] `C-TR-10` `constraint` No credential appears in anything the browser downloads `src: Technical requirements no secret`
- [ ] `C-TR-11` `constraint` The object store is reached by the server alone `src: Technical requirements no secret`
- [ ] `C-TR-12` `constraint` No binary asset ships with the build `src: Technical requirements performance`

## C-DM Data model

- [ ] `C-DM-1` `data` The schema carries six tables `src: Data model p1`
- [ ] `C-DM-2` `data` Every timestamp is stored in UTC `src: Data model p1`
- [ ] `C-DM-3` `data` An account row carries a role of reader or author `src: Data model accounts`
- [ ] `C-DM-4` `data` An account email is unique, stored lowercase `src: Data model accounts`
- [ ] `C-DM-5` `data` An idea row carries a unique kebab-case slug `src: Data model ideas`
- [ ] `C-DM-6` `data` An idea row carries a bias of long or short `src: Data model ideas`
- [ ] `C-DM-7` `data` An idea row carries a status of draft or published `src: Data model ideas`
- [ ] `C-DM-8` `data` An idea's published timestamp is null until the idea is published `src: Data model ideas`
- [ ] `C-DM-9` `data` A boost row exists at most once per account per idea `src: Data model boosts`
- [ ] `C-DM-10` `data` A tick row's direction agrees with the sign of the change `src: Data model ticks`
- [ ] `C-DM-11` `constraint` A failed publish leaves no orphaned object in the bucket `src: Data model invariants`
- [ ] `C-DM-12` `literal` The seeded published idea is `Gold Breakout Watch` `src: Data model seed data`
- [ ] `C-DM-13` `literal` The second seeded published idea is `Yen Carry Unwind` `src: Data model seed data`
- [ ] `C-DM-14` `literal` The seeded draft idea is `Copper Squeeze Setup` `src: Data model seed data`
- [ ] `C-DM-15` `constraint` Seeding is idempotent across a restart `src: Data model closing line`

## C-FE Front-end specification

- [ ] `C-FE-1` `ui` A sticky header spans the full width on every route `src: Front-end specification header`
- [ ] `C-FE-2` `ui` The header condenses once the page scrolls past the first viewport `src: Front-end specification header`
- [ ] `C-FE-3` `ui` The header blurs whatever passes beneath `src: Front-end specification header`
- [ ] `C-FE-4` `literal` The header carries five primary menu entries starting with `Products` `src: Front-end specification header`
- [ ] `C-FE-5` `literal` The search control carries the placeholder `Search` `src: Front-end specification search`
- [ ] `C-FE-6` `literal` The offer button is labelled `Get started` `src: Front-end specification offer button`
- [ ] `C-FE-7` `capability` One global footer link map appears on every route `src: Front-end specification footer`
- [ ] `C-FE-8` `literal` The footer badge reads `Made by humans` `src: Front-end specification footer`
- [ ] `C-FE-9` `constraint` Every icon is inline vector geometry rather than a bitmap `src: Front-end specification iconography`
- [ ] `C-FE-10` `ui` Shadows stay rare, shallow across the product `src: Front-end specification elevation`
- [ ] `C-FE-11` `ui` Accent gradients appear on headline words, card titles, the offer wash `src: Front-end specification gradients`
- [ ] `C-FE-12` `ui` The futures glow card's coloured shadow tracks scroll position `src: Front-end specification scroll system`
- [ ] `C-FE-13` `literal` The home hero sub-headline reads `The best trades require research, then commitment.` `src: Front-end specification home route`
- [ ] `C-FE-14` `literal` The home hero primary action reads `Get started for free` `src: Front-end specification home route`
- [ ] `C-FE-15` `literal` The home hero reassurance line reads `$0 forever, no credit card needed` `src: Front-end specification home route`
- [ ] `C-FE-16` `ui` The idea card preview is drawn procedurally as seeded candles `src: Front-end specification ideas and stories`
- [ ] `C-FE-17` `literal` The futures hero sub-line reads `Highly liquid futures markets mean oh-so-many more possibilities.` `src: Front-end specification futures route`
- [ ] `C-FE-18` `capability` Root-level state carries the theme, the authentication state, the pointer kind `src: Front-end specification component architecture`
- [ ] `C-FE-19` `constraint` Components are scoped so no styling leaks between them `src: Front-end specification component architecture`
- [ ] `C-FE-20` `ui` The header menu collapses into a hamburger below the primary breakpoint `src: Front-end specification responsive behaviour`

## C-CN Constraints

- [ ] `C-CN-1` `constraint` Every account sees the same public catalogue of markets `src: Constraints p1`
- [ ] `C-CN-2` `constraint` No money movement exists anywhere in the product `src: Constraints p2`
- [ ] `C-CN-3` `constraint` No in-browser script editor ships with the storefront `src: Constraints p2`
- [ ] `C-CN-4` `constraint` An idea's comment count is seeded, read-only `src: Constraints p2`
- [ ] `C-CN-5` `constraint` No message of any kind is sent to a visitor `src: Constraints p2`
- [ ] `C-CN-6` `constraint` The six platform capabilities are linked rather than rebuilt `src: Constraints p3`
- [ ] `C-CN-7` `constraint` The app stays responsive at the stated data volume `src: Constraints p5`
- [ ] `C-CN-8` `constraint` No external network call leaves the app at runtime beyond the font host `src: Constraints p2`

## C-DC Deployment contract

- [ ] `C-DC-1` `contract` The app is reachable at the public URL from the environment `src: Deployment contract`
- [ ] `C-DC-2` `literal` The container-internal port is `4173` `src: Deployment contract`
- [ ] `C-DC-3` `contract` The HTTP API is served under the same origin prefix `src: Deployment contract`
- [ ] `C-DC-4` `contract` The health endpoint returns a success status once ready `src: Deployment contract`
- [ ] `C-DC-5` `contract` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-6` `literal` Credentials are written to `/app/USER_README.md` `src: Deployment contract`
- [ ] `C-DC-7` `literal` An empty `.browser_screenshots/` directory exists at the app root `src: Deployment contract`
- [ ] `C-DC-8` `literal` An empty `.downloads/` directory exists at the app root `src: Deployment contract`
- [ ] `C-DC-9` `contract` A production build is served behind a static or preview server `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server outlives the session that started the server `src: Deployment contract`
- [ ] `C-DC-11` `literal` The listener binds `0.0.0.0` `src: Deployment contract`
- [ ] `C-DC-12` `constraint` No backing service is downloaded, installed, started by the app `src: Deployment contract`
- [ ] `C-DC-13` `constraint` No persistent volume is declared by the app `src: Deployment contract`
- [ ] `C-DC-14` `contract` A list endpoint returns a top-level JSON array `src: Deployment contract api shapes`
- [ ] `C-DC-15` `contract` An invalid call is rejected as a client error `src: Deployment contract api shapes`
- [ ] `C-DC-16` `contract` An unauthorized call is never answered with a success shape `src: Deployment contract api shapes`
- [ ] `C-DC-17` `constraint` Snapshot bytes live in the bucket rather than the app's own disk `src: Deployment contract no mocks`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the password every seeded account uses | `C-CF-2` |
| `author@example.com` | the seeded author account | `C-CF-3` |
| `author2@example.com` | the second seeded author account | `C-CF-4` |
| `reader@example.com` | the seeded reader account | `C-CF-5` |
| `ideas/{idea_id}/{sha256_of_bytes}.{ext}` | the snapshot object key scheme | `C-CF-26` |
| `591 INR per month` | the futures subscription price as shown | `C-CF-45` |
| `59100` | the futures subscription price in minor units | `C-CF-46` |
| `DATABASE_URL` | the datastore connection variable | `C-TR-3` |
| `STORAGE_ENDPOINT` | the object-store address variable | `C-TR-4` |
| `STORAGE_BUCKET` | the object-store bucket variable | `C-TR-5` |
| `Gold Breakout Watch` | the first seeded published idea | `C-DM-12` |
| `Yen Carry Unwind` | the second seeded published idea | `C-DM-13` |
| `Copper Squeeze Setup` | the seeded draft idea | `C-DM-14` |
| `Products` | the first header menu entry | `C-FE-4` |
| `Search` | the search control placeholder | `C-FE-5` |
| `Get started` | the offer button label | `C-FE-6` |
| `Made by humans` | the footer badge label | `C-FE-8` |
| `The best trades require research, then commitment.` | the home hero sub-headline | `C-FE-13` |
| `Get started for free` | the home hero primary action label | `C-FE-14` |
| `$0 forever, no credit card needed` | the home hero reassurance line | `C-FE-15` |
| `Highly liquid futures markets mean oh-so-many more possibilities.` | the futures hero sub-line | `C-FE-17` |
| `4173` | the container-internal port | `C-DC-2` |
| `/app/USER_README.md` | the credential file path | `C-DC-6` |
| `.browser_screenshots/` | the reserved screenshot directory | `C-DC-7` |
| `.downloads/` | the reserved download directory | `C-DC-8` |
| `0.0.0.0` | the bind address | `C-DC-11` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact colour values behind every named role | `C-UX-3` |
| the exact type sizes beyond the stated scale | `C-UX-8` |
| the exact motion timings behind the stated character | `C-UX-10` |
| the exact breakpoint widths behind the stated behaviour | `C-UX-14` |
| the exact corner radius base unit | `C-FE-10` |
| the sample asset-class metric figures | `C-CF-47` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 0 | 4 |
| User roles | 1 | 7 |
| Core features | 14 | 58 |
| User flow | 3 | 12 |
| UI and UX notes | 4 | 19 |
| Technical requirements | 6 | 12 |
| Data model | 4 | 15 |
| Front-end specification | 5 | 20 |
| Constraints | 2 | 8 |
| Deployment contract | 10 | 17 |
