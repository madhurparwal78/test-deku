# Checklist: Rookery

Items: 152
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC
Unpinned values flagged: 2

Every item restates one obligation of `instruction.md`. Nothing here adds a requirement the brief does not carry.

## C-OV Overview

- [ ] `C-OV-01` `capability` Rookery serves a public marketing site together with a signed-in client on one origin `src: Overview`
- [ ] `C-OV-02` `capability` A visitor ends by joining a space, then sending a message into a channel `src: Overview`
- [ ] `C-OV-03` `capability` A reaction count is derived from the set of members who reacted, never stored as a tally `src: Overview`
- [ ] `C-OV-04` `capability` An unread channel is derived by comparing its newest message against the newest message read `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `contract` Authorization is enforced server-side on every mutating endpoint `src: User roles`
- [ ] `C-RL-02` `contract` A denied request leaves the protected state unchanged `src: User roles`
- [ ] `C-RL-03` `role` A signed-out visitor can never read a channel `src: User roles`
- [ ] `C-RL-04` `role` A moderator can time out a member within their own authority `src: User roles`
- [ ] `C-RL-05` `capability` Signup is open to any visitor `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `contract` Email plus password exchange for a bearer token sent on every signed-in request `src: Core features`
- [ ] `C-CF-02` `contract` An absent, expired or revoked bearer token is rejected `src: Core features`
- [ ] `C-CF-03` `contract` A rejected request mutates nothing `src: Core features`
- [ ] `C-CF-04` `capability` Signup refuses an address already registered `src: Core features`
- [ ] `C-CF-05` `literal` A password is at least `8` characters long `src: Core features`
- [ ] `C-CF-06` `capability` A malformed address is refused with the address field named `src: Core features`
- [ ] `C-CF-07` `capability` A refused signup writes no account row `src: Core features`
- [ ] `C-CF-08` `contract` A password is stored under a memory-hard hash with a unique salt per account `src: Core features`
- [ ] `C-CF-09` `capability` A refresh token rotates on every exchange `src: Core features`
- [ ] `C-CF-10` `capability` Presenting a spent refresh token revokes the whole family at once `src: Core features`
- [ ] `C-CF-11` `capability` Redeeming an invite code joins the account to the space named by the code `src: Core features`
- [ ] `C-CF-12` `literal` The invite `NIGHTJAR-ONE` carries a use limit of `1` `src: Core features`
- [ ] `C-CF-13` `capability` A successful redemption lands on a confirmation page naming the space `src: Core features`
- [ ] `C-CF-14` `literal` The seeded space `Nightjar Collective` carries a member cap of `4` `src: Core features`
- [ ] `C-CF-15` `capability` Two simultaneous redemptions of one single-use invite produce exactly one join `src: Core features`
- [ ] `C-CF-16` `literal` A refused redemption reports `That invite has already been used.` `src: Core features`
- [ ] `C-CF-17` `capability` A refused redemption writes no membership row `src: Core features`
- [ ] `C-CF-18` `capability` A space never holds more members than its cap `src: Core features`
- [ ] `C-CF-19` `capability` A space the account has not joined reads as not found rather than forbidden `src: Core features`
- [ ] `C-CF-20` `capability` A channel the account cannot see reads as not found rather than forbidden `src: Core features`
- [ ] `C-CF-21` `capability` A space the account has not joined is absent from that account's own space list `src: Core features`
- [ ] `C-CF-22` `capability` A send into a space the account has not joined writes no message row `src: Core features`
- [ ] `C-CF-23` `contract` A permission set is carried over the wire as a decimal string rather than a number `src: Core features`
- [ ] `C-CF-24` `data` The role `@everyone` is always present at position `0` `src: Core features`
- [ ] `C-CF-25` `capability` A member's own permissions are the union of every role held `src: Core features`
- [ ] `C-CF-26` `capability` A role positioned lowest can grant a permission the highest does not `src: Core features`
- [ ] `C-CF-27` `capability` Every role deny is applied before every role allow, as one pass `src: Core features`
- [ ] `C-CF-28` `capability` Where one role denies what another allows, the allow wins `src: Core features`
- [ ] `C-CF-29` `capability` Reordering two roles does not change a resolved permission answer `src: Core features`
- [ ] `C-CF-30` `capability` Role position orders authority over other members rather than a member's own permissions `src: Core features`
- [ ] `C-CF-31` `capability` An administrator cannot be denied by a channel overwrite `src: Core features`
- [ ] `C-CF-32` `capability` A resolved set without `VIEW_CHANNEL` is empty rather than partial `src: Core features`
- [ ] `C-CF-33` `capability` A member under a timeout keeps `VIEW_CHANNEL` plus `READ_HISTORY` `src: Core features`
- [ ] `C-CF-34` `capability` A member under a timeout is refused sending `src: Core features`
- [ ] `C-CF-35` `capability` A member under a timeout loses `ADD_REACTIONS` `src: Core features`
- [ ] `C-CF-36` `capability` A refused send by a timed-out member writes no message row `src: Core features`
- [ ] `C-CF-37` `capability` A timeout carries an absolute expiry rather than a duration `src: Core features`
- [ ] `C-CF-38` `contract` An identifier encodes its own creation moment, so sorting by identifier sorts by time `src: Core features`
- [ ] `C-CF-39` `contract` An identifier is carried over the wire as a string `src: Core features`
- [ ] `C-CF-40` `literal` A message carries at most `4000` extended grapheme clusters of content `src: Core features`
- [ ] `C-CF-41` `capability` A sent message is stored as exactly one row carrying the sent content `src: Core features`
- [ ] `C-CF-42` `literal` History pages carry `1` to `100` rows, defaulting to `50` `src: Core features`
- [ ] `C-CF-43` `capability` A page of newer messages is returned newest first rather than ascending `src: Core features`
- [ ] `C-CF-44` `capability` A page of older messages is returned newest first `src: Core features`
- [ ] `C-CF-45` `contract` A history cursor is an identifier rather than an offset `src: Core features`
- [ ] `C-CF-46` `capability` A retried send carrying a stored nonce returns the original message `src: Core features`
- [ ] `C-CF-47` `capability` A retried send carrying a stored nonce creates no second message `src: Core features`
- [ ] `C-CF-48` `literal` A nonce is held for `300` seconds per channel per author `src: Core features`
- [ ] `C-CF-49` `capability` A reaction count equals the size of the set of members who reacted `src: Core features`
- [ ] `C-CF-50` `capability` Concurrent reaction additions leave a count equal to the set exactly `src: Core features`
- [ ] `C-CF-51` `capability` Mentions are computed by the service at send time `src: Core features`
- [ ] `C-CF-52` `capability` A message another member sends into an open channel appears without a reload `src: Core features`
- [ ] `C-CF-53` `capability` An acknowledgement naming an identifier below the stored mark changes nothing `src: Core features`
- [ ] `C-CF-54` `capability` An acknowledgement repeated has the effect of the acknowledgement made once `src: Core features`
- [ ] `C-CF-55` `capability` A mention of a member with no live session sends exactly one mail `src: Core features`
- [ ] `C-CF-56` `contract` The mention mail reaches the mentioned member's address alone, no cc, no bcc `src: Core features`
- [ ] `C-CF-57` `literal` The mention mail subject begins `Rookery mention:` then a space then the channel name `src: Core features`
- [ ] `C-CF-58` `capability` A reaction sends no mail `src: Core features`
- [ ] `C-CF-59` `literal` The plan `Loft Monthly` costs `1000` minor units in `usd` `src: Core features`
- [ ] `C-CF-60` `literal` The gift code `LOFT-ONE-SEAT` grants `Loft Yearly` `src: Core features`
- [ ] `C-CF-61` `capability` A feature gate reads an entitlement rather than a subscription `src: Core features`
- [ ] `C-CF-62` `capability` Two simultaneous redemptions of one gift code produce exactly one entitlement `src: Core features`
- [ ] `C-CF-63` `capability` The losing gift redemption is refused clearly `src: Core features`
- [ ] `C-CF-64` `capability` A terms page is reachable from the footer of every page `src: Core features`
- [ ] `C-CF-65` `capability` Every internal link on every public route resolves `src: Core features`
- [ ] `C-CF-66` `capability` An unknown address renders the product's own not-found page `src: Core features`
- [ ] `C-CF-67` `capability` An unknown address answers not-found rather than answering as though fine `src: Core features`
- [ ] `C-CF-68` `capability` Every form rejects invalid input inline, naming the field at fault `src: Core features`
- [ ] `C-CF-69` `capability` A visitor without a session is sent to sign in carrying the intended address `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `ui` Every public route listed is reachable without a session `src: User flow`
- [ ] `C-UF-02` `capability` A signed-out request for a client route lands on sign-in carrying the intended address `src: User flow`
- [ ] `C-UF-03` `ui` Every list carries an empty state naming what would fill the list `src: User flow`
- [ ] `C-UF-04` `ui` Every page carries a loading state reserving the space its content occupies `src: User flow`
- [ ] `C-UF-05` `ui` Every error renders as a page or an inline message rather than a blank screen `src: User flow`
- [ ] `C-UF-06` `capability` A visitor can complete the join journey from the home page to a sent message `src: User flow`
- [ ] `C-UF-07` `capability` The health route answers ready once the app has started `src: User flow`

## C-UX UI/UX notes

- [ ] `C-UX-01` `ui` One primary colour carries the primary action, worn by nothing else `src: UI/UX notes`
- [ ] `C-UX-02` `ui` Display leading sits tighter than the display type size `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Motion runs eased, on one family of curves, at one speed per size `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Depth comes from blur plus one perspective rather than a shadow scale `src: UI/UX notes`
- [ ] `C-UX-05` `ui` A visible focus ring differs from the hover treatment `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Nothing overflows sideways at a narrow viewport `src: UI/UX notes`
- [ ] `C-UX-07` `ui` The client reads as operational, quiet, dense but organised `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The client shell carries four columns `src: Front-end specification`
- [ ] `C-FE-02` `ui` The space rail carries one control per joined space `src: Front-end specification`
- [ ] `C-FE-03` `ui` The member list sits to the side of the conversation at a wide viewport `src: Front-end specification`
- [ ] `C-FE-04` `ui` The two leftmost columns become a drawer at a narrow viewport `src: Front-end specification`
- [ ] `C-FE-05` `ui` Loading older messages leaves the anchored row's screen position unchanged `src: Front-end specification`
- [ ] `C-FE-06` `ui` An arriving message scrolls the list only when the list sits at the bottom `src: Front-end specification`
- [ ] `C-FE-07` `ui` A jump control carries the count of unseen messages `src: Front-end specification`
- [ ] `C-FE-08` `ui` The marquee translates by exactly one repeat of its own content `src: Front-end specification`
- [ ] `C-FE-09` `ui` The marquee carries four short words in capitals `src: Front-end specification`
- [ ] `C-FE-10` `ui` Each feature movement nests a sharp scene inside a frosted card `src: Front-end specification`
- [ ] `C-FE-11` `ui` The starfield behind a feature card reads as a soft field of light `src: Front-end specification`
- [ ] `C-FE-12` `ui` The home page carries nine full-height movements `src: Front-end specification`
- [ ] `C-FE-13` `ui` The six feature movements alternate their text side strictly `src: Front-end specification`
- [ ] `C-FE-14` `ui` Display headlines are set in capitals in an extended grotesque `src: Front-end specification`
- [ ] `C-FE-15` `ui` The footer carries four link columns beside a language control `src: Front-end specification`
- [ ] `C-FE-16` `ui` The not-found page carries the numerals as live type rather than artwork `src: Front-end specification`
- [ ] `C-FE-17` `ui` The policy route carries no motion of any kind `src: Front-end specification`
- [ ] `C-FE-18` `literal` The hero headline reads `A ROOM THAT IS ALWAYS OPEN` `src: Front-end specification`
- [ ] `C-FE-19` `literal` The not-found headline reads `NOTHING LIVES HERE` `src: Front-end specification`
- [ ] `C-FE-20` `literal` The terms document is served at `/legal/terms` `src: Front-end specification`
- [ ] `C-FE-21` `ui` Moving between channels does not unmount the rail, the sidebar or the composer draft `src: Front-end specification`
- [ ] `C-FE-22` `ui` A confirmation moment overshoots further than every other movement `src: Front-end specification`
- [ ] `C-FE-23` `constraint` No image, video, font binary or vector-animation file ships `src: Front-end specification`
- [ ] `C-FE-24` `ui` The member list shows a count for each group above its rows `src: Front-end specification`
- [ ] `C-FE-25` `ui` A completed redemption ends on a full page confirmation naming what was granted `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The backend serves the API under the `/api` prefix on one origin `src: Technical requirements`
- [ ] `C-TR-02` `contract` The datastore is PostgreSQL, reached at `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-03` `contract` Mail goes over real SMTP to Mailpit at `SMTP_HOST` plus `SMTP_PORT` `src: Technical requirements`
- [ ] `C-TR-04` `contract` Every host is read from the environment rather than hardcoded `src: Technical requirements`
- [ ] `C-TR-05` `literal` Every list endpoint defaults `page_size` to `50`, capping at `100` `src: Technical requirements`
- [ ] `C-TR-06` `capability` A page size above the cap is refused with the cap named `src: Technical requirements`
- [ ] `C-TR-07` `capability` Two requests racing to write one row produce exactly one winner `src: Technical requirements`
- [ ] `C-TR-08` `capability` The losing request receives a refusal naming what was taken `src: Technical requirements`
- [ ] `C-TR-09` `capability` A failed attempt leaves no partial state `src: Technical requirements`
- [ ] `C-TR-10` `constraint` No credential appears in anything the browser downloads `src: Technical requirements`
- [ ] `C-TR-11` `capability` Every public route declares its own preview image `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded account uses the password `deku-demo-pw-2026` `src: Data model`
- [ ] `C-DM-02` `data` All timestamps are UTC `src: Data model`
- [ ] `C-DM-03` `data` An account carries an email unique, compared case-insensitively `src: Data model`
- [ ] `C-DM-04` `data` A reaction row is unique across message, emoji, account `src: Data model`
- [ ] `C-DM-05` `capability` A read mark never moves backwards `src: Data model`
- [ ] `C-DM-06` `capability` An invite use count never exceeds its use limit under concurrent redemptions `src: Data model`
- [ ] `C-DM-07` `capability` A gift code moves to redeemed exactly once `src: Data model`
- [ ] `C-DM-08` `literal` The seeded roles are `@everyone`, `Regulars`, `Archivists`, `Moderators` `src: Data model`
- [ ] `C-DM-09` `literal` The channel `#build-log` denies `SEND_MESSAGES` to `Regulars` `src: Data model`
- [ ] `C-DM-10` `capability` Seeding is idempotent, so restarting duplicates no rows `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `literal` The app stays responsive with `100000` messages in one channel `src: Constraints`
- [ ] `C-CN-02` `constraint` No payment provider exists, so the paid tier is granted inside the app itself `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173` `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served on that same origin under the `/api` prefix `src: Deployment contract`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the app is ready `src: Deployment contract`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-06` `contract` A production build is served behind a static or preview server `src: Deployment contract`
- [ ] `C-DC-07` `contract` The server keeps running after the session ends, never a child of the shell `src: Deployment contract`
- [ ] `C-DC-08` `contract` The server binds `0.0.0.0` rather than a loopback address `src: Deployment contract`
- [ ] `C-DC-09` `contract` The named backing services are already running, never installed by the app `src: Deployment contract`
- [ ] `C-DC-10` `contract` Bearer auth is required on everything except signup, login, refresh, health `src: Deployment contract`
- [ ] `C-DC-11` `contract` An invalid or unauthorized call is rejected as a client error rather than a `5xx` `src: Deployment contract`
- [ ] `C-DC-12` `constraint` Mail is never simulated by an in-memory list or a self-answered response `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `8` | pinned in the brief | `C-CF-05` |
| `NIGHTJAR-ONE` | pinned in the brief | `C-CF-12` |
| `1` | pinned in the brief | `C-CF-12` |
| `Nightjar Collective` | pinned in the brief | `C-CF-14` |
| `4` | pinned in the brief | `C-CF-14` |
| `That invite has already been used.` | pinned in the brief | `C-CF-16` |
| `4000` | pinned in the brief | `C-CF-40` |
| `100` | pinned in the brief | `C-CF-42` |
| `50` | pinned in the brief | `C-CF-42` |
| `300` | pinned in the brief | `C-CF-48` |
| `Rookery mention:` | pinned in the brief | `C-CF-57` |
| `Loft Monthly` | pinned in the brief | `C-CF-59` |
| `1000` | pinned in the brief | `C-CF-59` |
| `usd` | pinned in the brief | `C-CF-59` |
| `LOFT-ONE-SEAT` | pinned in the brief | `C-CF-60` |
| `Loft Yearly` | pinned in the brief | `C-CF-60` |
| `A ROOM THAT IS ALWAYS OPEN` | pinned in the brief | `C-FE-18` |
| `NOTHING LIVES HERE` | pinned in the brief | `C-FE-19` |
| `/legal/terms` | pinned in the brief | `C-FE-20` |
| `page_size` | pinned in the brief | `C-TR-05` |
| `deku-demo-pw-2026` | pinned in the brief | `C-DM-01` |
| `@everyone` | pinned in the brief | `C-DM-08` |
| `Regulars` | pinned in the brief | `C-DM-08` |
| `Archivists` | pinned in the brief | `C-DM-08` |
| `Moderators` | pinned in the brief | `C-DM-08` |
| `#build-log` | pinned in the brief | `C-DM-09` |
| `SEND_MESSAGES` | pinned in the brief | `C-DM-09` |
| `100000` | pinned in the brief | `C-CN-01` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact shade of every colour role | `C-UX-01` |
| the exact duration of every moment | `C-UX-03` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 1 | 4 |
| User roles | 3 | 5 |
| Core features | 56 | 69 |
| User flow | 6 | 7 |
| UI/UX notes | 6 | 7 |
| Front-end specification | 23 | 25 |
| Technical requirements | 10 | 11 |
| Data model | 8 | 10 |
| Constraints | 1 | 2 |
| Deployment contract | 12 | 12 |
| Definition of done | 1 | 1 |

