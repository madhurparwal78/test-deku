# Checklist: Creative Studio Archive

Items: 182
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` One codebase serves the public scroll sequence plus the private studio console `src: Overview`
- [ ] `C-OV-02` `capability` The archive is a second mode over the same document rather than a separate page `src: Overview`
- [ ] `C-OV-03` `constraint` Nothing is sold on the public site, so no cart exists anywhere `src: Overview`
- [ ] `C-OV-04` `capability` A visitor sends a work inquiry that reaches the console queue `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A `writer` signs in to the console `src: User roles`
- [ ] `C-RL-02` `role` A `writer` creates a draft case `src: User roles`
- [ ] `C-RL-03` `role` A `writer` cannot publish a case `src: User roles`
- [ ] `C-RL-04` `role` A `lead` publishes a case `src: User roles`
- [ ] `C-RL-05` `role` A `lead` reads the inquiry queue `src: User roles`
- [ ] `C-RL-06` `role` A `writer` requesting the inquiry queue is refused by the server `src: User roles`
- [ ] `C-RL-07` `role` No route creates an account `src: User roles`
- [ ] `C-RL-08` `role` A client reviewer holds a signed token rather than an account `src: User roles`
- [ ] `C-RL-09` `literal` Every seeded account uses the password `deku-demo-pw-2026` `src: User roles`
- [ ] `C-RL-10` `literal` The seeded lead signs in as `lead@example.com` `src: User roles`
- [ ] `C-RL-11` `literal` The second seeded lead signs in as `lead2@example.com` `src: User roles`
- [ ] `C-RL-12` `literal` The seeded writer signs in as `writer@example.com` `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` A member signs in with an email plus a password to receive a bearer token `src: Core features`
- [ ] `C-CF-02` `capability` Signing out stops the bearer token working `src: Core features`
- [ ] `C-CF-03` `ui` The home sequence renders eight blocks in the stored order `src: Core features`
- [ ] `C-CF-04` `contract` Each sequence block carries `data-block` with its own component value `src: Core features`
- [ ] `C-CF-05` `contract` `GET /api/page` returns the enabled sequence blocks in order `src: Core features`
- [ ] `C-CF-06` `capability` A block naming a component the app does not have is skipped `src: Core features`
- [ ] `C-CF-07` `ui` The hero renders four display lines stacked over each other `src: Core features`
- [ ] `C-CF-08` `ui` The services run renders the eight disciplines in their stored order `src: Core features`
- [ ] `C-CF-09` `contract` Each menu label carries `data-menu` with its own value `src: Core features`
- [ ] `C-CF-10` `ui` The first four menu labels move the reader without changing the address `src: Core features`
- [ ] `C-CF-11` `contract` The document element carries `data-mode` reading `sequence` on the home route `src: Core features`
- [ ] `C-CF-12` `contract` `GET /api/cases` returns only published cases ordered by `stack_order` `src: Core features`
- [ ] `C-CF-13` `data` Twelve published cases are seeded at contiguous stack positions `src: Core features`
- [ ] `C-CF-14` `contract` Each case card carries `data-case-order` carrying its own stack position `src: Core features`
- [ ] `C-CF-15` `contract` Each case card carries `data-veil` carrying its computed veil value `src: Core features`
- [ ] `C-CF-16` `data` The veil of the first seeded card reads `0.9625` `src: Core features`
- [ ] `C-CF-17` `data` The veil of the last seeded card reads `0.5500` `src: Core features`
- [ ] `C-CF-18` `capability` Reordering the published cases recomputes every veil value `src: Core features`
- [ ] `C-CF-19` `data` Two published cases never hold one stack position `src: Core features`
- [ ] `C-CF-20` `capability` Publishing a thirteenth case moves the first card's veil to `0.9654` `src: Core features`
- [ ] `C-CF-21` `ui` The archive card renders last in the case stack `src: Core features`
- [ ] `C-CF-22` `data` The archive card never appears in the published case list `src: Core features`
- [ ] `C-CF-23` `capability` With no published case the stack region collapses to nothing `src: Core features`
- [ ] `C-CF-24` `contract` `GET /api/cases/{slug}` returns one published case with its neighbouring slugs `src: Core features`
- [ ] `C-CF-25` `data` A case body carries blocks of seven kinds only `src: Core features`
- [ ] `C-CF-26` `capability` A body block of an unknown kind is skipped `src: Core features`
- [ ] `C-CF-27` `capability` An unpublished case answers a stranger as an unknown address does `src: Core features`
- [ ] `C-CF-28` `capability` A signed in member reads an unpublished case `src: Core features`
- [ ] `C-CF-29` `contract` `GET /api/archive` returns the seed, the plane, plus every wall item `src: Core features`
- [ ] `C-CF-30` `data` The archive layout seed reads `halftone-wall-2026` `src: Core features`
- [ ] `C-CF-31` `capability` No two archive item rectangles overlap on the plane `src: Core features`
- [ ] `C-CF-32` `capability` Two reads of the archive return identical item positions `src: Core features`
- [ ] `C-CF-33` `capability` Adding an archive item regenerates the layout without overlap `src: Core features`
- [ ] `C-CF-34` `contract` Each wall item carries `data-archive-item` with its own id `src: Core features`
- [ ] `C-CF-35` `capability` An archive item linked to a published case offers a control opening that case `src: Core features`
- [ ] `C-CF-36` `contract` `GET /api/showreel` returns a poster address plus its renditions `src: Core features`
- [ ] `C-CF-37` `ui` The showreel starts muted with a visible unmute control `src: Core features`
- [ ] `C-CF-38` `capability` The space key toggles showreel playback `src: Core features`
- [ ] `C-CF-39` `contract` `GET /api/awards` returns each body with its types carrying a count `src: Core features`
- [ ] `C-CF-40` `data` The seeded count of the `Site of the Day` type at `Prixel` reads `24` `src: Core features`
- [ ] `C-CF-41` `capability` Recording one more win moves that award count up by exactly one `src: Core features`
- [ ] `C-CF-42` `ui` An award type carrying no records renders its name alone `src: Core features`
- [ ] `C-CF-43` `ui` The contact block leads with the studio address `hey@halftone.studio` `src: Core features`
- [ ] `C-CF-44` `contract` `POST /api/inquiries` stores an accepted inquiry `src: Core features`
- [ ] `C-CF-45` `capability` An invalid inquiry is refused with a message per field `src: Core features`
- [ ] `C-CF-46` `capability` An invalid inquiry writes no row at all `src: Core features`
- [ ] `C-CF-47` `capability` A repeated `submission_key` produces exactly one stored inquiry `src: Core features`
- [ ] `C-CF-48` `capability` A repeated `submission_key` returns the first inquiry's id `src: Core features`
- [ ] `C-CF-49` `capability` An accepted submission renders the confirmation copy in place of the form `src: Core features`
- [ ] `C-CF-50` `capability` A submission carrying the decoy field is refused without telling the sender `src: Core features`
- [ ] `C-CF-51` `capability` A submission arriving under the minimum fill time is refused `src: Core features`
- [ ] `C-CF-52` `capability` Submissions past the hourly ceiling for one address are refused with a retry hint `src: Core features`
- [ ] `C-CF-53` `capability` A high scoring submission is stored in the `spam` state `src: Core features`
- [ ] `C-CF-54` `contract` `GET /api/console/cases` returns every case in any state `src: Core features`
- [ ] `C-CF-55` `contract` Each console case row carries `data-state` with its own state word `src: Core features`
- [ ] `C-CF-56` `capability` A save carrying a stale revision is refused with the current revision `src: Core features`
- [ ] `C-CF-57` `capability` Two saves from one loaded revision never both succeed `src: Core features`
- [ ] `C-CF-58` `contract` `GET /api/console/inquiries` returns the queue newest first `src: Core features`
- [ ] `C-CF-59` `capability` An inquiry at the `over-200k` band is assigned to `lead@example.com` `src: Core features`
- [ ] `C-CF-60` `capability` An inquiry naming a discipline held by one lead is assigned to that lead `src: Core features`
- [ ] `C-CF-61` `capability` Erasing an inquiry keeps its row with every event `src: Core features`
- [ ] `C-CF-62` `data` An erased inquiry's personal fields each read `[erased]` `src: Core features`
- [ ] `C-CF-63` `capability` The trail sequence values increase with no gaps `src: Core features`
- [ ] `C-CF-64` `capability` Each trail row's `prev_hash` equals the previous row's `hash` `src: Core features`
- [ ] `C-CF-65` `capability` Deleting a referenced media asset is refused with the referencing records `src: Core features`
- [ ] `C-CF-66` `capability` A lead issues a review link bound to one case revision `src: Core features`
- [ ] `C-CF-67` `capability` Issuing a second review link revokes the previous tokens `src: Core features`
- [ ] `C-CF-68` `capability` A preview token reaches no case beyond the one bound to the token `src: Core features`
- [ ] `C-CF-69` `capability` Publication is refused until a client approval matches the published revision `src: Core features`
- [ ] `C-CF-70` `capability` Publication is refused until a lead approval matches the published revision `src: Core features`
- [ ] `C-CF-71` `capability` A refused publication leaves the stored state unchanged `src: Core features`
- [ ] `C-CF-72` `capability` Editing an approved case writes a new revision `src: Core features`
- [ ] `C-CF-73` `capability` A minor revision carries the existing client approval forward `src: Core features`
- [ ] `C-CF-74` `capability` A minor revision changing the client name is refused `src: Core features`
- [ ] `C-CF-75` `capability` An expired token renders the page an unknown token renders `src: Core features`
- [ ] `C-CF-76` `data` Every uploaded case cover lives at `cases/{case_slug}/{sha256_of_bytes}.{ext}` `src: Core features`
- [ ] `C-CF-77` `capability` An uploaded file renamed to another extension is refused on inspection `src: Core features`
- [ ] `C-CF-78` `capability` The cover object of an unpublished case is refused to a stranger `src: Core features`
- [ ] `C-CF-79` `ui` Every content image carries alternative text `src: Core features`
- [ ] `C-CF-80` `ui` The privacy page is reachable from the footer of every route `src: Core features`
- [ ] `C-CF-81` `capability` The privacy page states the retention window for a stored inquiry `src: Core features`
- [ ] `C-CF-82` `capability` An unknown address renders the studio not-found page reporting itself as not found `src: Core features`
- [ ] `C-CF-83` `ui` The not-found page carries one control returning to the sequence root `src: Core features`
- [ ] `C-CF-84` `capability` Every internal link on every public route resolves `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `contract` `/` serves the home sequence to anybody `src: User flow`
- [ ] `C-UF-02` `contract` `/case/<slug>` serves one published case to anybody `src: User flow`
- [ ] `C-UF-03` `contract` `/showreel` serves the showreel to anybody `src: User flow`
- [ ] `C-UF-04` `contract` `/legal/privacy` serves the privacy page to anybody `src: User flow`
- [ ] `C-UF-05` `contract` `/preview/<token>` serves one unpublished case revision to the token holder `src: User flow`
- [ ] `C-UF-06` `contract` `/console/cases` serves the case list to a signed in member `src: User flow`
- [ ] `C-UF-07` `contract` `/console/inquiries` serves the inquiry queue to a lead only `src: User flow`
- [ ] `C-UF-08` `capability` An anonymous request for a console route lands on the sign in route `src: User flow`
- [ ] `C-UF-09` `capability` A sign in with no return path lands on the console case list `src: User flow`
- [ ] `C-UF-10` `capability` An absolute return path on sign in is refused `src: User flow`
- [ ] `C-UF-11` `ui` Every list carries an empty state naming what would be there `src: User flow`
- [ ] `C-UF-12` `ui` A failed save keeps the values already typed into the form `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The ground is a near-black neutral under the whole sequence `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The signal colour appears only on an interactive element plus the contact address `src: UI/UX notes`
- [ ] `C-UX-03` `ui` No shadow appears anywhere in the product `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Display sizes set a line height of four fifths of their size `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Caption sizes set a line height equal to their size or a tenth above `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Body copy sits at a line height half again above the size of the copy `src: UI/UX notes`
- [ ] `C-UX-07` `ui` One transition speed carries every state change on every control `src: UI/UX notes`
- [ ] `C-UX-08` `ui` A block reveals exactly once rather than replaying on a second pass `src: UI/UX notes`
- [ ] `C-UX-09` `ui` A reduced motion preference stops every continuous movement `src: UI/UX notes`
- [ ] `C-UX-10` `ui` The console carries no atmosphere, reading quiet against the public sequence `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Body text meets a contrast ratio of `4.5:1` against its ground `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Every focusable element carries a visible focus ring `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Every gesture carries a keyboard equivalent `src: UI/UX notes`
- [ ] `C-UX-14` `ui` At a narrow viewport no route scrolls sideways `src: UI/UX notes`
- [ ] `C-UX-15` `ui` The case stack sits in a centred column with empty ground either side `src: UI/UX notes`
- [ ] `C-UX-16` `ui` One polite live region announces the outcome of an inquiry `src: UI/UX notes`
- [ ] `C-UX-17` `ui` The composition changes once, around the width of a tablet held upright `src: UI/UX notes`
- [ ] `C-UX-18` `ui` Below that width the hero lines stop overlapping, dropping to heading size `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `capability` Every public route renders as a complete document from the server `src: Technical requirements`
- [ ] `C-TR-02` `capability` Every word, image, link survives with scripting switched off `src: Technical requirements`
- [ ] `C-TR-03` `contract` The datastore address is read from `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-04` `contract` The object store address is read from `STORAGE_ENDPOINT` `src: Technical requirements`
- [ ] `C-TR-05` `contract` `GET /api/health` returns a `status` field once the app is ready `src: Technical requirements`
- [ ] `C-TR-06` `contract` Every response carries a nosniff content type security header `src: Technical requirements`
- [ ] `C-TR-07` `capability` No credential appears in anything the browser downloads `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Sixteen tables hold the product's records `src: Data model`
- [ ] `C-DM-02` `data` A case revision is immutable once written `src: Data model`
- [ ] `C-DM-03` `data` `submission_key` is unique across stored inquiries `src: Data model`
- [ ] `C-DM-04` `data` An award count is derived on read rather than stored `src: Data model`
- [ ] `C-DM-05` `data` An erased inquiry keeps its identifier plus its events `src: Data model`
- [ ] `C-DM-06` `data` Trail rows are append only, never updated, never removed `src: Data model`
- [ ] `C-DM-07` `data` A refused reorder leaves every stack position unchanged `src: Data model`
- [ ] `C-DM-08` `data` Seeding is idempotent across a restart `src: Data model`
- [ ] `C-DM-09` `data` Two unpublished cases are seeded beside the twelve published ones `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Every mark is drawn from coordinates rather than loaded as a file `src: Front-end specification`
- [ ] `C-FE-02` `ui` The diagonal arrow appears after the archive label, nowhere else `src: Front-end specification`
- [ ] `C-FE-03` `ui` The top band repeats text without ever showing a seam `src: Front-end specification`
- [ ] `C-FE-04` `ui` The bottom band appears once the sequence has passed the first case `src: Front-end specification`
- [ ] `C-FE-05` `ui` The link treatment tears a label into offset copies that re-converge `src: Front-end specification`
- [ ] `C-FE-06` `ui` The scroll position is owned by the application rather than the platform `src: Front-end specification`
- [ ] `C-FE-07` `ui` The scroll hold counts rather than toggling between two states `src: Front-end specification`
- [ ] `C-FE-08` `ui` Returning to the sequence restores the exact rendered position `src: Front-end specification`
- [ ] `C-FE-09` `ui` The moving surface lights a cloth from a second hidden copy of the cloth `src: Front-end specification`
- [ ] `C-FE-10` `ui` The moving surface failing leaves every block readable `src: Front-end specification`
- [ ] `C-FE-11` `ui` The arrival counter reports real loading progress rather than a timer `src: Front-end specification`
- [ ] `C-FE-12` `ui` The arrival counter never runs backwards `src: Front-end specification`
- [ ] `C-FE-13` `ui` A key press during the arrival sequence completes the arrival at once `src: Front-end specification`
- [ ] `C-FE-14` `ui` The two bottom statements hold position through the arrival exit `src: Front-end specification`
- [ ] `C-FE-15` `ui` The archive wall wraps in both axes without a visible jump `src: Front-end specification`
- [ ] `C-FE-16` `ui` The archive wall is desaturated at rest, returning to colour under the pointer `src: Front-end specification`
- [ ] `C-FE-17` `ui` The archive wall is draggable before every image has arrived `src: Front-end specification`
- [ ] `C-FE-18` `ui` The quality ladder holds a step once taken downward `src: Front-end specification`
- [ ] `C-FE-19` `ui` The replacement pointer is not mounted for a coarse pointer `src: Front-end specification`
- [ ] `C-FE-20` `ui` Opening a case grows the pressed card to fill the window `src: Front-end specification`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No email, no SMS, no push is sent by the product `src: Constraints`
- [ ] `C-CN-02` `constraint` No payment surface exists anywhere in the product `src: Constraints`
- [ ] `C-CN-03` `constraint` No route calls out to another service at runtime `src: Constraints`
- [ ] `C-CN-04` `constraint` One language, English, carries the whole product `src: Constraints`
- [ ] `C-CN-05` `constraint` No second tenant exists, so one studio owns every record `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `contract` The container-internal port is `4173` `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served under the `/api` prefix `src: Deployment contract`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the app is ready `src: Deployment contract`
- [ ] `C-DC-05` `contract` Login credentials are written to `/app/USER_README.md` `src: Deployment contract`
- [ ] `C-DC-06` `contract` The reserved `.browser_screenshots/` directory exists at the app root `src: Deployment contract`
- [ ] `C-DC-07` `contract` The reserved `.downloads/` directory exists at the app root `src: Deployment contract`
- [ ] `C-DC-08` `contract` A production build is served rather than a development server `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0` rather than a loopback address `src: Deployment contract`
- [ ] `C-DC-11` `contract` A list endpoint returns a top-level JSON array `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the brief pins it in User roles | `C-RL-09` |
| `lead@example.com` | the brief pins it in User roles | `C-RL-10` |
| `lead2@example.com` | the brief pins it in User roles | `C-RL-11` |
| `writer@example.com` | the brief pins it in User roles | `C-RL-12` |
| `0.9625` | the veil of the first seeded card | `C-CF-16` |
| `0.5500` | the veil of the last seeded card | `C-CF-17` |
| `0.9654` | the first veil with thirteen published cases | `C-CF-20` |
| `halftone-wall-2026` | the archive layout seed | `C-CF-30` |
| `[erased]` | the erasure marker | `C-CF-62` |
| `hey@halftone.studio` | the studio contact address | `C-CF-43` |
| `4173` | the container-internal port | `C-DC-02` |
| `Thank you, it arrived` | the accepted-submission confirmation | `C-CF-49` |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 4 |
| User roles | 3 | 12 |
| Core features | 38 | 84 |
| User flow | 10 | 12 |
| UI and UX notes | 8 | 18 |
| Technical requirements | 5 | 7 |
| Data model | 7 | 9 |
| Front-end specification | 13 | 20 |
| Constraints | 0 | 5 |
| Deployment contract | 9 | 11 |
